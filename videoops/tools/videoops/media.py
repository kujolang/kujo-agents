"""Bounded media execution shared by CLI, Agent Projects, and harness handoffs.

This is an asset service, not a creative orchestrator or an audio mixer. Local
SQLite reservations serialize dispatch budgets; uncertain calls never replay.
"""
from __future__ import annotations
import json
import fcntl
import os
import shutil
import sqlite3
import subprocess
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from .media_contracts import (MediaError, artifact, canonical, contained, digest, now,
                              read_json, validate, verify_ref, write_json)
from .media_providers import (CAPABILITIES, SUPPORTED, Transport, credential, prepare,
                              decode, inspect_account)

MANIFEST = 'assets/asset-manifest.json'

def fingerprint(request):
    validate('media-request',request)
    payload={k:v for k,v in request.items() if k not in ('request_id','attempt','retry_of','authorization_id','budget')}
    return digest(canonical(payload).encode())

def future(value):
    try: return datetime.fromisoformat(value.replace('Z','+00:00')) > datetime.now(timezone.utc)
    except (ValueError,TypeError): return False

def probe(path):
    try:
        reply = subprocess.run(['ffprobe','-v','error','-protocol_whitelist','file,pipe',
            '-format_whitelist','wav,mp3,mov,matroska,webm,ogg,flac,aac','-show_streams','-show_format','-of','json',str(path)],capture_output=True,timeout=30)
        if reply.returncode: raise MediaError('INVALID_MEDIA')
        info = json.loads(reply.stdout); streams = info['streams']
        if not streams or not all(s['codec_type'] in ('audio','video') for s in streams):
            raise MediaError('INVALID_MEDIA')
        duration = float(info['format'].get('duration',0))
        if not 0 < duration <= 86400: raise MediaError('INVALID_MEDIA')
        audio = next((s for s in streams if s['codec_type']=='audio'),{})
        return {'duration_seconds':duration,'sample_rate':int(audio['sample_rate']) if audio.get('sample_rate') else None,
                'channels':audio.get('channels'),'codec':streams[0]['codec_name'],
                'streams':[{'type':s['codec_type'],'codec':s['codec_name']} for s in streams]}
    except (OSError,ValueError,KeyError,subprocess.TimeoutExpired): raise MediaError('INVALID_MEDIA') from None

class MediaService:
    def __init__(self, workspace, *, transport=None):
        self.root = Path(workspace).resolve(strict=True)
        self.transport = transport or Transport()
        state = contained(self.root,'.videoops-media/state.sqlite3')
        state.parent.mkdir(parents=True,exist_ok=True)
        self.db = state
        with self.transaction() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS grants (id TEXT PRIMARY KEY, body TEXT NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
                CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, authorization_id TEXT,
                 state TEXT NOT NULL, dispatched INTEGER NOT NULL DEFAULT 0, credits REAL NOT NULL, cost REAL NOT NULL, result TEXT, disposition TEXT, request TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS audit (at TEXT NOT NULL, action TEXT NOT NULL, resource TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS inspections (id INTEGER PRIMARY KEY, authorization_id TEXT, at TEXT, result TEXT);
                ''')
        os.chmod(state,0o600)

    @contextmanager
    def transaction(self):
        # Re-check containment on every open, not only at construction.
        contained(self.root,'.videoops-media/state.sqlite3')
        db = sqlite3.connect(self.db,timeout=30,isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except BaseException:
            db.rollback(); raise
        finally: db.close()

    def authorize(self, value, *, local_authorized=False):
        if not local_authorized: raise MediaError('LOCAL_AUTHORIZATION_REQUIRED')
        validate('media-authorization',value)
        if Path(value['workspace']).resolve() != self.root or not future(value['expires_at']):
            raise MediaError('AUTHORIZATION_INVALID')
        for e in value['entitlements'] + value['request_bounds']: verify_ref(self.root,e['evidence'])
        with self.transaction() as db:
            old = db.execute('SELECT body,revoked FROM grants WHERE id=?',(value['authorization_id'],)).fetchone()
            if old and (old['body'] != canonical(value) or old['revoked']):
                raise MediaError('AUTHORIZATION_ID_IMMUTABLE')
            db.execute('INSERT OR IGNORE INTO grants(id,body) VALUES (?,?)',(value['authorization_id'],canonical(value)))
            db.execute('INSERT INTO audit VALUES (?,?,?)',(now(),'authorize',value['authorization_id']))
        return {'authorization_id':value['authorization_id'],'authorized':True}

    def revoke(self, aid, *, local_authorized=False):
        if not local_authorized: raise MediaError('LOCAL_AUTHORIZATION_REQUIRED')
        with self.transaction() as db:
            count = db.execute('UPDATE grants SET revoked=1 WHERE id=?',(aid,)).rowcount
            db.execute('INSERT INTO audit VALUES (?,?,?)',(now(),'revoke',aid))
        return {'revoked':bool(count),'authorization_id':aid}

    def _grant(self, db, aid):
        row = db.execute('SELECT * FROM grants WHERE id=?',(aid,)).fetchone()
        if not row: raise MediaError('AUTHORIZATION_REQUIRED')
        grant = json.loads(row['body'])
        if row['revoked'] or not future(grant['expires_at']) or Path(grant['workspace']).resolve()!=self.root:
            raise MediaError('AUTHORIZATION_INVALID')
        return grant

    def _scope(self, db, request):
        g = self._grant(db,request['authorization_id'])
        if (g['provider'] != request['provider'] or request['capability'] not in g['capabilities']
            or request['model'] not in g['models'] or (g['voices'] and request['voice'] not in g['voices'])
            or request['output_format'] not in g['output_formats']): raise MediaError('AUTHORIZATION_INVALID')
        entitlement = next((e for e in g['entitlements'] if e['capability']==request['capability']),None)
        if not entitlement or not future(entitlement['expires_at']): raise MediaError('ENTITLEMENT_UNKNOWN')
        verify_ref(self.root,entitlement['evidence'])
        if not entitlement['allowed']: raise MediaError('ENTITLEMENT_DENIED')
        if not entitlement['no_overage']: raise MediaError('ENTITLEMENT_UNKNOWN')
        allowance = entitlement['remaining_credits']
        budget = request['budget']
        bound = next((b for b in g['request_bounds'] if b['fingerprint']==fingerprint(request)),None)
        if not bound: raise MediaError('AUTHORIZATION_INVALID')
        verify_ref(self.root,bound['evidence'])
        if budget['max_credits'] != bound['max_credits'] or budget['max_cost'] != bound['max_cost']:
            raise MediaError('AUTHORIZATION_INVALID')
        if not budget['estimate_evidence']: raise MediaError('ENTITLEMENT_UNKNOWN')
        verify_ref(self.root,budget['estimate_evidence'])
        if allowance is None or budget['max_credits']<=0: raise MediaError('ENTITLEMENT_UNKNOWN')
        calls, credits, cost = db.execute('SELECT count(*),coalesce(sum(credits),0),coalesce(sum(cost),0) FROM requests WHERE authorization_id=? AND dispatched=1', (g['authorization_id'],)).fetchone()
        inspections = db.execute('SELECT count(*) FROM inspections WHERE authorization_id=?',(g['authorization_id'],)).fetchone()[0]
        if (calls+inspections+1>g['max_calls'] or credits+budget['max_credits']>min(g['max_credits'],allowance)
            or cost+budget['max_cost']>g['max_cost']): raise MediaError('BUDGET_EXHAUSTED')
        return g

    def providers(self):
        return {'schema':'videoops-media-capabilities/v1','providers':[
            {'provider':p,'capabilities':[{'capability':c,'implemented':c in enabled,
                'authentication':'not_checked' if p!='local' else 'not_required',
                'entitlement':'unknown' if p!='local' else 'not_required',
                'authorization':'not_checked','live_tested':False,
                'async_jobs':False,'provider_idempotency':False} for c in CAPABILITIES]}
            for p,enabled in SUPPORTED.items()]}

    def doctor(self, request=None):
        # Offline: never even resolve a credential, including OS secret stores.
        deps = {name:bool(shutil.which(name)) for name in ('ffmpeg','ffprobe')}
        result = {'schema':'videoops-media-doctor/v1','offline':True,'dependencies':deps,
            'available':all(deps.values()),'authentication':'not_checked','entitlement':'unknown',
            'authorization':'not_checked','executable':False,'tested':'not_checked',
            'providers':self.providers()['providers']}
        with self.transaction() as db:
            rows=db.execute('SELECT result FROM requests WHERE result IS NOT NULL').fetchall()
            results=[json.loads(row[0]) for row in rows]
            result['test_evidence']=[{'provider':v['provider'],'capability':v['capability'],
                'verification':v['verification'],'state':v['state'],'at':v['created_at'],'receipt':v['receipt_path']}
                for v in results]
            if request is not None:
                validate('media-request',request)
                try:
                    if request['provider']=='local' and request['capability']=='local_import':
                        result.update(authorization='not_required',entitlement='not_required',executable=all(deps.values()))
                    else:
                        grant=self._scope(db,request)
                        ref=grant['credential_ref']
                        configured=bool(ref) and (ref['kind']!='env' or bool(os.environ.get(ref['name'])))
                        result.update(authorization='present',entitlement='operator_evidence',executable=all(deps.values()) and configured,
                            credential_configured=configured)
                except MediaError as exc:
                    result.update(authorization='absent_or_invalid',executable=False,reason=exc.code)
        return result

    def inspect(self, aid, *, local_authorized=False):
        if not local_authorized: raise MediaError('LOCAL_AUTHORIZATION_REQUIRED')
        with self.transaction() as db:
            g = self._grant(db,aid)
            if g['provider']!='elevenlabs': raise MediaError('UNSUPPORTED_CAPABILITY')
            used = db.execute('SELECT count(*) FROM requests WHERE authorization_id=? AND dispatched=1',(aid,)).fetchone()[0]
            used += db.execute('SELECT count(*) FROM inspections WHERE authorization_id=?',(aid,)).fetchone()[0]
            if used >= g['max_calls']: raise MediaError('BUDGET_EXHAUSTED')
            key = credential(g['credential_ref'])
            cursor = db.execute('INSERT INTO inspections(authorization_id,at,result) VALUES (?,?,?)',(aid,now(),canonical({'state':'UNKNOWN_OUTCOME'})))
            iid = cursor.lastrowid
        try: result = inspect_account(self.transport,key)
        except MediaError as exc: result={'state':'FAILED','error':exc.code}
        with self.transaction() as db: db.execute('UPDATE inspections SET result=? WHERE id=?',(canonical(result),iid))
        return result

    def _cached(self, row):
        result=json.loads(row['result'])
        validate('media-result',result)
        if result['state']=='SUCCESS':
            for ref in [result['original']]+result['derived']:
                verify_ref(self.root,ref)
            if result['alignment']['artifact']: verify_ref(self.root,result['alignment']['artifact'])
        return result

    def status(self, request_id):
        with self.transaction() as db:
            row=db.execute('SELECT * FROM requests WHERE id=?',(request_id,)).fetchone()
            if not row: raise MediaError('REQUEST_NOT_FOUND')
            if row['result']: return self._cached(row)
            return {'request_id':request_id,'state':'UNKNOWN_OUTCOME',
                    'dispatch_state':row['state'],'retry_allowed':False}

    def reconcile(self, request_id, disposition, *, local_authorized=False):
        with self._request_lock(request_id,blocking=False):
            return self._reconcile(request_id,disposition,local_authorized=local_authorized)

    def _reconcile(self, request_id, disposition, *, local_authorized=False):
        if not local_authorized: raise MediaError('LOCAL_AUTHORIZATION_REQUIRED')
        if disposition not in ('confirmed-failed','confirmed-cancelled'): raise MediaError('INVALID_DISPOSITION')
        with self.transaction() as db:
            row=db.execute('SELECT * FROM requests WHERE id=?',(request_id,)).fetchone()
            if not row or row['state'] not in ('UNKNOWN_OUTCOME','DISPATCHING','FAILED','BLOCKED'):
                raise MediaError('INVALID_DISPOSITION')
            # This records operator disposition, never claims remote cancellation or refunds.
            state='CANCELLED' if disposition=='confirmed-cancelled' else 'FAILED'
            result=json.loads(row['result']) if row['result'] else self._result(json.loads(row['request']),row['fingerprint'])
            result.update(state=state,error='CANCELLED_BY_OPERATOR' if state=='CANCELLED' else 'UNKNOWN_DISPATCH_OUTCOME')
            db.execute('UPDATE requests SET state=?,disposition=?,result=? WHERE id=?',(state,disposition,canonical(result),request_id))
            db.execute('INSERT INTO audit VALUES (?,?,?)',(now(),disposition,request_id))
            write_json(self.root,result['receipt_path'],result)
        return result

    def _result(self, r, fp):
        base=f"media/{r['request_id']}"
        return {'schema':'videoops-media-result/v1',**{k:r[k] for k in ('request_id','job_id','asset_id','requirement_id','shot_ids','attempt','retry_of','provider','capability','model','voice','settings','output_format','authorization_id','rights')},
            'fingerprint':fp,'state':'BLOCKED','original':None,'derived':[],'metadata':None,
            'alignment':{'availability':'not_requested' if r['alignment']=='none' else 'unavailable','units':'seconds','time_origin':'original_media_start','source':None,'artifact':None},
            'provider_request_id':None,'usage':{'credits':None,'cost':None,'currency':'USD','source':'unavailable',
                'reserved_credits':r['budget']['max_credits'],'reserved_cost':r['budget']['max_cost']},
            'verification':'local' if r['provider']=='local' else 'live' if type(self.transport) is Transport else 'mock','latency_seconds':0,'retries':r['attempt']-1,'created_at':now(),'error':None,
            'receipt_path':base+'/result.json','manifest_path':MANIFEST,'handoff_path':base+'/handoff.json'}

    @contextmanager
    def _request_lock(self, request_id, *, blocking=True):
        import re
        if not isinstance(request_id,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}',request_id):
            raise MediaError('INVALID_REQUEST_ID')
        path=contained(self.root,f'.videoops-media/{request_id}.lock')
        fd=os.open(path,os.O_CREAT | os.O_RDWR | getattr(os,'O_NOFOLLOW',0),0o600)
        try:
            try: fcntl.flock(fd,fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
            except BlockingIOError: raise MediaError('REQUEST_ACTIVE') from None
            yield
        finally:
            fcntl.flock(fd,fcntl.LOCK_UN); os.close(fd)

    def execute(self, request, *, operation='generate'):
        validate('media-request',request)
        with self._request_lock(request['request_id']):
            return self._execute(request,operation=operation)

    def _execute(self, request, *, operation='generate'):
        r=validate('media-request',request)
        local=operation=='import'
        if operation not in ('generate','import'): raise MediaError('UNSUPPORTED_CAPABILITY')
        if local != (r['provider']=='local' and r['capability']=='local_import'):
            raise MediaError('UNSUPPORTED_CAPABILITY')
        # Explicit entry and lineage must precede generation. Usage approval is independent.
        manifest=read_json(contained(self.root,MANIFEST,must_exist=True))
        matches=[a for a in manifest['assets'] if a['id']==r['asset_id']]
        if len(matches)!=1 or matches[0].get('requirement_id')!=r['requirement_id']:
            raise MediaError('MANIFEST_REQUIREMENT_MISMATCH')
        if not local and matches[0]['status']!='GENERATE': raise MediaError('EXPLICIT_GENERATE_REQUIRED')
        source=verify_ref(self.root,r['input']); verify_ref(self.root,r['rights']['evidence'])
        input_bytes=source.read_bytes()
        if digest(input_bytes)!=r['input']['sha256']: raise MediaError('ARTIFACT_HASH_MISMATCH')
        if local and (r['authorization_id'] is not None or r['budget']['max_cost'] or r['budget']['max_credits']):
            raise MediaError('LOCAL_IMPORT_REQUIRES_ZERO_BUDGET')
        fp=fingerprint(r); result=self._result(r,fp)
        path=body=key=None
        started=time.monotonic()
        if not local:
            try: path,body=prepare(r,input_bytes.decode('utf-8'))
            except UnicodeError: raise MediaError('INVALID_TEXT_ARTIFACT') from None
            except MediaError as exc:
                result.update(state='UNSUPPORTED',error=exc.code)
                return self._store_preflight(r,fp,result)
        with self.transaction() as db:
            prior=db.execute('SELECT * FROM requests WHERE id=?',(r['request_id'],)).fetchone()
            if prior:
                if prior['request']!=canonical(r): raise MediaError('REQUEST_ID_CONFLICT')
                return self._cached(prior) if prior['result'] else {'request_id':r['request_id'],'state':'UNKNOWN_OUTCOME','retry_allowed':False}
            duplicates=db.execute('SELECT * FROM requests WHERE fingerprint=?',(fp,)).fetchall()
            if duplicates:
                prior=duplicates[-1]
                if not prior['disposition'] or r['retry_of']!=prior['id'] or r['attempt']!=json.loads(prior['request'])['attempt']+1:
                    raise MediaError('DUPLICATE_REQUEST_REQUIRES_DISPOSITION')
            elif r['attempt']!=1 or r['retry_of'] is not None: raise MediaError('INVALID_ATTEMPT_LINEAGE')
            if not local:
                try:
                    grant=self._scope(db,r); key=credential(grant['credential_ref'])
                except MediaError as exc:
                    result.update(state='BLOCKED',error=exc.code if exc.code in ('AUTHORIZATION_REQUIRED','AUTHORIZATION_INVALID','BUDGET_EXHAUSTED','ENTITLEMENT_UNKNOWN','ENTITLEMENT_DENIED','CREDENTIAL_UNAVAILABLE') else 'AUTHORIZATION_INVALID')
                    # No dispatch/reservation; retry needs a new request after fixing scope.
                    return self._persist(db,r,fp,result,credits=0,cost=0)
                if key in canonical(r) or key.encode() in input_bytes:
                    raise MediaError('CREDENTIAL_UNAVAILABLE')
            db.execute('INSERT INTO requests VALUES (?,?,?,?,1,?,?,NULL,NULL,?)',
                (r['request_id'],fp,r['authorization_id'],'DISPATCHING',r['budget']['max_credits'],r['budget']['max_cost'],canonical(r)))
        try:
            if local:
                payload=input_bytes; alignment=rid=credits=None
                result['usage'].update(credits=0,cost=0,source='local')
            else:
                response=self.transport.request('POST',path,key=key,body=body)
                payload,alignment,rid,credits=decode(r,response)
                aligned_text=''.join(c for c in alignment.get('characters',[]) if isinstance(c,str)) if isinstance(alignment,dict) and isinstance(alignment.get('characters'),list) else ''
                if key.encode() in payload or (alignment is not None and key in canonical(alignment)) or key in aligned_text or (rid and key in rid):
                    raise MediaError('MALFORMED_RESPONSE')
                result['provider_request_id']=rid
                if credits is not None: result['usage'].update(credits=credits,source='provider_header')
            base=Path('media')/r['request_id']
            original=str(base/'original.media')
            p=contained(self.root,original); p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f: f.write(payload)
            result['original']=artifact(self.root,original)
            result['metadata']=probe(p)
            if not local:
                meta=result['metadata']
                if not any(s['type']=='audio' for s in meta['streams']): raise MediaError('INVALID_MEDIA')
                parts=r['output_format'].split('_')
                if len(parts)<2 or not parts[1].isdigit() or meta['sample_rate']!=int(parts[1]): raise MediaError('INVALID_MEDIA')
                if parts[0]=='mp3' and meta['codec']!='mp3': raise MediaError('INVALID_MEDIA')
                if parts[0]=='wav' and not meta['codec'].startswith('pcm_'): raise MediaError('INVALID_MEDIA')
            # Decode entire input to reject a valid header followed by damaged packets.
            decode_check=subprocess.run(['ffmpeg','-v','error','-xerror','-protocol_whitelist','file,pipe','-format_whitelist','wav,mp3,mov,matroska,webm,ogg,flac,aac','-i',str(p),'-f','null','-'],capture_output=True,timeout=120)
            if decode_check.returncode: raise MediaError('INVALID_MEDIA')
            if not local:
                normalized=str(base/'normalized.wav'); n=contained(self.root,normalized)
                cmd=['ffmpeg','-v','error','-xerror','-n','-protocol_whitelist','file,pipe','-format_whitelist','wav,mp3,mov,matroska,webm,ogg,flac,aac','-i',str(p),'-map','0:a:0','-c:a','pcm_s24le',str(n)]
                if subprocess.run(cmd,capture_output=True,timeout=120).returncode: raise MediaError('INVALID_MEDIA')
                probe(n); result['derived']=[artifact(self.root,normalized)]
            if alignment is not None:
                self._alignment(alignment,result['metadata']['duration_seconds'])
                ap=str(base/'alignment.json'); write_json(self.root,ap,alignment)
                result['alignment'].update(availability='available',source='elevenlabs.character_alignment',artifact=artifact(self.root,ap))
            elif r['alignment']=='required': raise MediaError('MISSING_ALIGNMENT')
            result.update(state='SUCCESS',error=None)
        except MediaError as exc:
            result.update(state='UNKNOWN_OUTCOME' if exc.code in ('UNKNOWN_DISPATCH_OUTCOME','HTTP_SERVER_ERROR') else 'FAILED',error=exc.code)
        except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired):
            result.update(state='UNKNOWN_OUTCOME' if not local else 'FAILED',error='UNKNOWN_DISPATCH_OUTCOME' if not local else 'INVALID_MEDIA')
        result['latency_seconds']=time.monotonic()-started
        with self.transaction() as db:
            # Conservative reservations stay charged unless observed provider usage exists.
            amount=result['usage']['credits']
            db.execute('UPDATE requests SET state=?,result=?,credits=? WHERE id=?',
                (result['state'],canonical(result),amount if amount is not None else r['budget']['max_credits'],r['request_id']))
            self._artifacts(result)
        return result

    def _alignment(self, a, duration):
        if not isinstance(a,dict) or set(a)!={'characters','character_start_times_seconds','character_end_times_seconds'}:
            raise MediaError('ALIGNMENT_INVALID')
        chars,starts,ends=(a[k] for k in ('characters','character_start_times_seconds','character_end_times_seconds'))
        if not all(isinstance(x,list) for x in (chars,starts,ends)) or not chars or len(chars)!=len(starts) or len(chars)!=len(ends): raise MediaError('ALIGNMENT_INVALID')
        previous=previous_end=0
        for c,s,e in zip(chars,starts,ends):
            if not isinstance(c,str) or type(s) not in (int,float) or type(e) not in (int,float) or not previous<=s<=e<=duration+.05 or e<previous_end:
                raise MediaError('ALIGNMENT_INVALID')
            previous=s; previous_end=e

    def _store_preflight(self,r,fp,result):
        with self.transaction() as db:
            prior=db.execute('SELECT * FROM requests WHERE id=?',(r['request_id'],)).fetchone()
            if prior:
                if prior['request']!=canonical(r): raise MediaError('REQUEST_ID_CONFLICT')
                return self._cached(prior) if prior['result'] else {'state':'UNKNOWN_OUTCOME','request_id':r['request_id']}
            return self._persist(db,r,fp,result,credits=0,cost=0)

    def _persist(self,db,r,fp,result,*,credits,cost):
        db.execute('INSERT INTO requests VALUES (?,?,?,?,0,?,?,?,NULL,?)',
            (r['request_id'],fp,r['authorization_id'],result['state'],credits,cost,canonical(result),canonical(r)))
        self._artifacts(result)
        return result

    def _artifacts(self,result):
        validate('media-result',result)
        write_json(self.root,result['receipt_path'],result)
        manifest=read_json(contained(self.root,MANIFEST,must_exist=True))
        for entry in manifest['assets']:
            if entry['id']==result['asset_id']:
                entry['media_result']=result['receipt_path']
                entry['acquisition_status']='resolved' if result['state']=='SUCCESS' else 'blocked' if result['state'] in ('BLOCKED','UNSUPPORTED','UNKNOWN_OUTCOME') else 'failed'
                if result['state']=='SUCCESS': entry['path']=(result['derived'] or [result['original']])[0]['path']
        write_json(self.root,MANIFEST,manifest)
        write_json(self.root,result['handoff_path'],{'schema':'videoops-media-handoff/v1',
            'request_id':result['request_id'],'asset_id':result['asset_id'],'state':result['state'],
            'media_result':artifact(self.root,result['receipt_path']),
            'next_role':'video-hyperframes-editor' if result['state']=='SUCCESS' else 'producer',
            'usage_approval':'unchanged','perceptual_review':'REVIEW_INCOMPLETE'})
