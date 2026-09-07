"""Provider behavior with mocked HTTP; real ffmpeg validates returned synthetic WAV."""
import base64
import copy
import io
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from videoops.media import MediaService, fingerprint
from videoops.media_contracts import MediaError, artifact, read_json, validate, write_json
from videoops.media_providers import Response, Transport, prepare, inspect_account, NoRedirect

ROOT=Path(__file__).resolve().parents[1]
def wav_bytes():
    buffer=io.BytesIO()
    with wave.open(buffer,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
        w.writeframes(b''.join(struct.pack('<h',int(4000*math.sin(i*.12))) for i in range(16000)))
    return buffer.getvalue()
class Fake:
    def __init__(self,status=200,body=None,error=None):
        self.status=status; self.body=body; self.error=error; self.calls=[]
    def request(self,method,path,**kwargs):
        self.calls.append((method,path,kwargs.get('body')))
        if self.error: raise MediaError(self.error)
        data=self.body
        if data is None:
            data=wav_bytes()
            if 'with-timestamps' in path:
                data=json.dumps({'audio_base64':base64.b64encode(data).decode(),'alignment':{'characters':['H','i'],'character_start_times_seconds':[0,.2],'character_end_times_seconds':[.2,.5]}}).encode()
        return Response(self.status,{'request-id':'mock-request','character-cost':'2'},data)

class MediaTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        (self.root/'input.wav').write_bytes(wav_bytes());(self.root/'script.txt').write_text('Hello, this is a test.')
        (self.root/'rights.txt').write_text('Synthetic original test asset. No licensed provider output.')
        (self.root/'entitlement.txt').write_text('Mock account, TTS/SFX/music allowed; no overage; test only.')
        (self.root/'estimate.txt').write_text('Mock fixed upper bound 10 credits, zero currency cost.')
        self.fake=Fake();self.service=MediaService(self.root,transport=self.fake)
        self.env=patch.dict(os.environ,{'VIDEOOPS_TEST_KEY':'dummy-not-a-real-key'});self.env.start()
        write_json(self.root,'assets/asset-manifest.json',{'assets':[{'id':'A1','type':'audio','origin':'original','status':'GENERATE','usage_status':'pending','requirement_id':'R1'}]})
    def tearDown(self): self.env.stop();self.tmp.cleanup()
    def request(self,cap='speech',rid='one'):
        local=cap=='local_import'
        return {'schema':'videoops-media-request/v1','request_id':rid,'job_id':'test','asset_id':'A1','requirement_id':'R1','shot_ids':['S1'],'capability':cap,'provider':'local' if local else 'elevenlabs','model':None if local else 'test-model','voice':'test-voice' if cap=='speech' else None,'settings':{},'input':artifact(self.root,'input.wav' if local else 'script.txt'),'language':'en' if cap=='speech' else None,'target_duration_seconds':3 if cap=='music' else 1,'output_format':'wav_16000','alignment':'required' if cap=='speech' else 'none','authorization_id':None if local else 'grant','budget':{'max_credits':0 if local else 10,'max_cost':0,'currency':'USD','estimate_evidence':None if local else artifact(self.root,'estimate.txt')},'attempt':1,'retry_of':None,'rights':{'evidence':artifact(self.root,'rights.txt'),'license':'original','attribution':None,'restrictions':[],'intended_use':'offline test'}}
    def grant(self,**overrides):
        expiry=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat()
        a={'schema':'videoops-media-authorization/v1','authorization_id':'grant','workspace':str(self.root),'provider':'elevenlabs','capabilities':['speech','sound_effects','music'],'models':['test-model'],'voices':[],'output_formats':['wav_16000'],'request_bounds':[{'fingerprint':fingerprint(self.request(c)),'max_credits':10,'max_cost':0,'evidence':artifact(self.root,'estimate.txt')} for c in ['speech','sound_effects','music']],'max_calls':3,'max_credits':30,'max_cost':0,'currency':'USD','expires_at':expiry,'credential_ref':{'kind':'env','name':'VIDEOOPS_TEST_KEY','account':None},'entitlements':[{'capability':c,'allowed':True,'expires_at':expiry,'evidence':artifact(self.root,'entitlement.txt'),'remaining_credits':30,'no_overage':True} for c in ['speech','sound_effects','music']]}
        a.update(overrides); self.service.authorize(a,local_authorized=True);return a
    def test_local_import_without_network(self):
        r=self.service.execute(self.request('local_import'),operation='import')
        self.assertEqual(r['state'],'SUCCESS'); self.assertEqual(self.fake.calls,[])
        self.assertEqual(r['original']['sha256'],artifact(self.root,'input.wav')['sha256'])
        m=read_json(self.root/'assets/asset-manifest.json')['assets'][0]
        self.assertEqual(m['status'],'GENERATE'); self.assertEqual(m['usage_status'],'pending'); self.assertEqual(m['acquisition_status'],'resolved')
        self.assertTrue((self.root/r['handoff_path']).is_file()); validate('media-result',r)
    def test_three_actual_http_shapes(self):
        self.grant()
        for index,cap in enumerate(('speech','sound_effects','music')):
            request=self.request(cap,str(index)); result=self.service.execute(request)
            self.assertEqual(result['state'],'SUCCESS',result)
            method,path,body=self.fake.calls[-1];self.assertEqual(method,'POST');self.assertEqual(body['model_id'],'test-model')
            if cap=='speech': self.assertIn('/with-timestamps?',path);self.assertEqual(result['alignment']['availability'],'available')
            if cap=='sound_effects': self.assertIn('/sound-generation?',path);self.assertEqual(body['duration_seconds'],1)
            if cap=='music': self.assertIn('/music?',path);self.assertEqual(body['music_length_ms'],3000)
            self.assertEqual(result['usage']['credits'],2);self.assertIsNone(result['usage']['cost'])
    def test_contract_unknown_fields_and_versions(self):
        for mut in ({'api_key':'do-not-accept'},{'schema':'v99'},{'attempt':0},{'settings':{'api_key':'no'}},{'input':{'path':'../escape','sha256':'a'*64}}):
            r=self.request();r.update(mut)
            with self.assertRaises(MediaError): self.service.execute(r)
        self.assertFalse(self.fake.calls)
    def test_doctor_no_auth(self):
        with patch('videoops.media.credential',side_effect=AssertionError('no credential reads')):
            self.assertTrue(self.service.doctor()['offline'])
        self.assertFalse(self.fake.calls)
    def test_missing_authorization(self):
        r=self.service.execute(self.request());self.assertEqual(r['error'],'AUTHORIZATION_REQUIRED');self.assertFalse(self.fake.calls)
    def test_auth_requires_local_consent(self):
        with self.assertRaisesRegex(MediaError,'LOCAL_AUTHORIZATION_REQUIRED'):self.service.authorize({})
    def test_revoked_and_expired(self):
        self.grant();self.service.revoke('grant',local_authorized=True)
        self.assertEqual(self.service.execute(self.request())['error'],'AUTHORIZATION_INVALID')
        with self.assertRaisesRegex(MediaError,'AUTHORIZATION_INVALID'):
            self.grant(authorization_id='expired',expires_at='2000-01-01T00:00:00Z')
    def test_denied_music_entitlement(self):
        g=self.grant(); self.service.revoke('grant',local_authorized=True)
        g['authorization_id']='music-denied';g['entitlements'][2]['allowed']=False
        self.service.authorize(g,local_authorized=True);r=self.request('music');r['authorization_id']='music-denied'
        self.assertEqual(self.service.execute(r)['error'],'ENTITLEMENT_DENIED');self.assertFalse(self.fake.calls)
    def test_unknown_allowance_and_price_block(self):
        self.grant();r=self.request();r['budget']['estimate_evidence']=None
        self.assertEqual(self.service.execute(r)['error'],'ENTITLEMENT_UNKNOWN');self.assertFalse(self.fake.calls)
    def test_duplicate_is_not_another_call(self):
        self.grant();r=self.request();a=self.service.execute(r);b=MediaService(self.root,transport=self.fake).execute(r)
        self.assertEqual(a,b);self.assertEqual(len(self.fake.calls),1)
        r['request_id']='different'
        with self.assertRaisesRegex(MediaError,'DUPLICATE_REQUEST'):self.service.execute(r)
    def test_ambiguous_timeout_never_replayed(self):
        self.grant();self.fake.error='UNKNOWN_DISPATCH_OUTCOME';r=self.request()
        self.assertEqual(self.service.execute(r)['state'],'UNKNOWN_OUTCOME')
        self.service.execute(r);self.assertEqual(len(self.fake.calls),1)
        self.service.reconcile('one','confirmed-failed',local_authorized=True)
        self.fake.error=None;r.update(request_id='retry',retry_of='one',attempt=2)
        self.assertEqual(self.service.execute(r)['state'],'SUCCESS');self.assertEqual(len(self.fake.calls),2)
    def test_missing_key_no_dispatch_count(self):
        self.grant(max_calls=1)
        with patch.dict(os.environ,{'VIDEOOPS_TEST_KEY':''}): self.assertEqual(self.service.execute(self.request())['error'],'CREDENTIAL_UNAVAILABLE')
        self.service.reconcile('one','confirmed-failed',local_authorized=True)
        r=self.request(rid='retry');r.update(attempt=2,retry_of='one')
        self.assertEqual(self.service.execute(r)['state'],'SUCCESS')
    def test_concurrent_budget_only_one_dispatch(self):
        self.grant(max_calls=1)
        a=self.request(rid='a');b=self.request('sound_effects',rid='b')
        with ThreadPoolExecutor(2) as pool:
            values=list(pool.map(lambda r:MediaService(self.root,transport=self.fake).execute(r),[a,b]))
        self.assertEqual(len(self.fake.calls),1);self.assertEqual(sorted(v['state'] for v in values),['BLOCKED','SUCCESS'])
    def test_http_failures_and_no_secret_echo(self):
        self.grant()
        for n,(status,code) in enumerate([(401,'HTTP_UNAUTHORIZED'),(429,'HTTP_RATE_LIMIT'),(422,'HTTP_REJECTED')]):
            self.fake.status=status;r=self.request(rid=str(n));r['input']=artifact(self.root,'script.txt')
            if n: r.update(attempt=n+1,retry_of=str(n-1));self.service.reconcile(str(n-1),'confirmed-failed',local_authorized=True)
            result=self.service.execute(r);self.assertEqual(result['error'],code)
            self.assertNotIn('dummy-not-a-real-key',json.dumps(result))
    def test_missing_alignment_preserves_original(self):
        self.grant();self.fake.body=json.dumps({'audio_base64':base64.b64encode(wav_bytes()).decode()}).encode()
        result=self.service.execute(self.request());self.assertEqual(result['error'],'MISSING_ALIGNMENT');self.assertTrue((self.root/result['original']['path']).is_file())
    def test_malformed_media_does_not_resolve(self):
        self.grant();self.fake.body=b'not audio'
        result=self.service.execute(self.request('music'));self.assertEqual(result['state'],'FAILED');self.assertEqual(result['error'],'INVALID_MEDIA')
    def test_malformed_timestamp_json(self):
        self.grant();self.fake.body=b'[]';result=self.service.execute(self.request());self.assertEqual(result['error'],'MALFORMED_RESPONSE')
    def test_alignment_nonmonotonic_end_rejected(self):
        with self.assertRaisesRegex(MediaError,'ALIGNMENT_INVALID'):
            self.service._alignment({'characters':['a','b'],'character_start_times_seconds':[0,.1],'character_end_times_seconds':[.9,.2]},1)
    def test_symlink_and_hash_escape(self):
        (self.root/'alias.wav').symlink_to(self.root/'input.wav');r=self.request('local_import');r['input']['path']='alias.wav'
        with self.assertRaisesRegex(MediaError,'SYMLINK'):self.service.execute(r,operation='import')
        r=self.request('local_import');r['input']['sha256']='0'*64
        with self.assertRaisesRegex(MediaError,'HASH_MISMATCH'):self.service.execute(r,operation='import')
    def test_explicit_generate_only(self):
        m=read_json(self.root/'assets/asset-manifest.json');m['assets'][0]['status']='FOUND';write_json(self.root,'assets/asset-manifest.json',m)
        with self.assertRaisesRegex(MediaError,'EXPLICIT_GENERATE_REQUIRED'):self.service.execute(self.request())
    def test_no_redirect_or_arbitrary_origin(self):
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,None,{},'https://attacker.invalid'))
        with self.assertRaises(MediaError):Transport().request('POST','https://attacker.invalid',key='dummy')
    def test_account_inspection_explicit_and_bounded(self):
        self.grant(max_calls=1)
        with self.assertRaises(MediaError):self.service.inspect('grant')
        self.fake.body=json.dumps({'character_count':2,'character_limit':10,'api_key':'never persisted'}).encode()
        result=self.service.inspect('grant',local_authorized=True);self.assertEqual(result['remaining_credits'],8);self.assertNotIn('api_key',result)
        self.assertEqual(self.service.execute(self.request())['error'],'BUDGET_EXHAUSTED')
    def test_account_plan_is_bounded_and_not_inferred(self):
        r=inspect_account(Fake(body=json.dumps({'tier':'free','character_count':10,'character_limit':100,'max_credit_limit_extension':0}).encode()),'dummy')
        self.assertEqual(r['tier'],'free');self.assertTrue(r['no_overage']);self.assertEqual(r['remaining_credits'],90)
        self.assertEqual(r['entitlement'],'unknown')
        r=inspect_account(Fake(body=b'{"tier":"unrecognized-private-value"}'),'dummy')
        self.assertIsNone(r['tier']);self.assertIsNone(r['remaining_credits']);self.assertIsNone(r['no_overage'])

    def test_account_array_response_normalized(self):
        with self.assertRaisesRegex(MediaError,'MALFORMED_RESPONSE'):inspect_account(Fake(body=b'[]'),'dummy')
    def test_under_reservation_rejected(self):
        self.grant();r=self.request();r['budget']['max_credits']=1
        self.assertEqual(self.service.execute(r)['error'],'AUTHORIZATION_INVALID');self.assertFalse(self.fake.calls)
    def test_reconcile_blocks_active_dispatch(self):
        self.grant();started=threading.Event();release=threading.Event();original=self.fake.request
        def blocked(*args,**kwargs):
            started.set();release.wait(10);return original(*args,**kwargs)
        self.fake.request=blocked
        with ThreadPoolExecutor(1) as pool:
            future=pool.submit(self.service.execute,self.request())
            try:
                self.assertTrue(started.wait(5))
                with self.assertRaisesRegex(MediaError,'REQUEST_ACTIVE'):
                    self.service.reconcile('one','confirmed-failed',local_authorized=True)
            finally: release.set()
            self.assertEqual(future.result()['state'],'SUCCESS')
        self.assertEqual(len(self.fake.calls),1)
    def test_abandoned_dispatch_can_be_reconciled(self):
        self.grant();r=self.request()
        with self.service.transaction() as db:
            db.execute('INSERT INTO requests VALUES (?,?,?,?,1,?,?,NULL,NULL,?)',('one',fingerprint(r),'grant','DISPATCHING',10,0,json.dumps(r,sort_keys=True,separators=(',',':'))))
        result=self.service.reconcile('one','confirmed-failed',local_authorized=True)
        self.assertEqual(result['state'],'FAILED');self.assertFalse(self.fake.calls)
    def test_input_mutation_does_not_change_authorized_body(self):
        self.grant();r=self.request();original=Path.read_bytes;count=0
        def mutate(path):
            nonlocal count
            data=original(path)
            if path.resolve()==(self.root/'script.txt').resolve():
                count+=1
                if count==1:path.write_text('Different text after validation')
            return data
        with patch.object(Path,'read_bytes',mutate):
            with self.assertRaisesRegex(MediaError,'HASH_MISMATCH'): self.service.execute(r)
        self.assertFalse(self.fake.calls)
    def test_offline_doctor_evaluates_scope_and_reports_evidence(self):
        self.grant();r=self.request();d=self.service.doctor(r)
        self.assertTrue(d['executable']);self.assertFalse(self.fake.calls)
        self.service.execute(r);d=self.service.doctor()
        self.assertEqual(d['test_evidence'][0]['verification'],'mock')
    def test_playlist_rejected_before_resolution(self):
        (self.root/'playlist.txt').write_text('ffconcat version 1.0\nfile input.wav\n')
        r=self.request('local_import');r['input']=artifact(self.root,'playlist.txt')
        result=self.service.execute(r,operation='import');self.assertEqual(result['error'],'INVALID_MEDIA')

    def test_provider_secret_echo_rejected(self):
        self.grant();self.fake.body=b'dummy-not-a-real-key'
        result=self.service.execute(self.request('music'))
        self.assertEqual(result['error'],'MALFORMED_RESPONSE');self.assertIsNone(result['original'])
        self.assertNotIn('dummy-not-a-real-key',(self.root/result['receipt_path']).read_text())
    def test_provider_secret_echo_in_request_id_and_characters(self):
        self.grant()
        secret='dummy-not-a-real-key'
        for n,variant in enumerate(('request_id','characters')):
            alignment={'characters':list(secret) if variant=='characters' else ['a'],'character_start_times_seconds':[0],'character_end_times_seconds':[.2]}
            body=json.dumps({'audio_base64':base64.b64encode(wav_bytes()).decode(),'alignment':alignment}).encode()
            self.fake.request=lambda *a, **k: Response(200,{'request-id':'trace-'+secret if variant=='request_id' else 'mock-id'},body)
            r=self.request(rid=str(n))
            if n:
                self.service.reconcile('0','confirmed-failed',local_authorized=True);r.update(attempt=2,retry_of='0')
            result=self.service.execute(r)
            self.assertEqual(result['error'],'MALFORMED_RESPONSE');self.assertIsNone(result['original'])
            self.assertNotIn(secret,(self.root/result['receipt_path']).read_text())

    def test_secret_bearing_request_never_persisted(self):
        r=self.request();r['rights']['license']='dummy-not-a-real-key'
        self.grant(request_bounds=[{'fingerprint':fingerprint(r),'max_credits':10,'max_cost':0,'evidence':artifact(self.root,'estimate.txt')}])
        with self.assertRaisesRegex(MediaError,'CREDENTIAL_UNAVAILABLE'):self.service.execute(r)
        with self.service.transaction() as db:self.assertEqual(db.execute('SELECT count(*) FROM requests').fetchone()[0],0)
        self.assertFalse((self.root/'media').exists());self.assertFalse(self.fake.calls)

    def test_mutated_entitlement_blocks_without_dispatch(self):
        self.grant();(self.root/'entitlement.txt').write_text('changed')
        result=self.service.execute(self.request())
        self.assertEqual(result['state'],'BLOCKED');self.assertEqual(result['error'],'AUTHORIZATION_INVALID');self.assertFalse(self.fake.calls)

    def test_cached_success_rechecks_asset_hash(self):
        r=self.request('local_import');result=self.service.execute(r,operation='import')
        (self.root/result['original']['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(MediaError,'HASH_MISMATCH'):self.service.execute(r,operation='import')
        with self.assertRaisesRegex(MediaError,'HASH_MISMATCH'):self.service.status(r['request_id'])
        self.assertFalse(self.fake.calls)

    def test_cli_arbitrary_local_handoff(self):
        write_json(self.root,'request.json',self.request('local_import'))
        done=subprocess.run([sys.executable,'-m','videoops.cli','media','import','--workspace',str(self.root),'--request',str(self.root/'request.json')],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(done.returncode,0,done.stdout+done.stderr);self.assertEqual(json.loads(done.stdout)['state'],'SUCCESS')

    def test_standalone_tools_copy_imports_without_retired_repository(self):
        import shutil
        with tempfile.TemporaryDirectory() as isolated:
            tool_root = Path(isolated) / "canonical-tools"
            shutil.copytree(ROOT, tool_root, ignore=shutil.ignore_patterns("__pycache__", "*.egg-info", "build", ".venv"))
            write_json(self.root, 'request.json', self.request('local_import'))
            env = dict(os.environ)
            env.pop('PYTHONPATH', None)
            done = subprocess.run([sys.executable, str(tool_root / 'bin/videoops'), 'media', 'import', '--workspace', str(self.root), '--request', str(self.root / 'request.json')], cwd=isolated, env=env, capture_output=True, text=True)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            self.assertEqual(json.loads(done.stdout)['state'], 'SUCCESS')
            help_result = subprocess.run([sys.executable, str(tool_root / 'bin/videoops'), '--help'], cwd=isolated, env=env, capture_output=True, text=True)
            self.assertEqual(help_result.returncode, 0)
            self.assertNotIn('init-db', help_result.stdout)
            self.assertNotIn('serve', help_result.stdout)

if __name__=='__main__':unittest.main()
