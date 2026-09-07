"""Executable synchronous ElevenLabs endpoints, with an injectable test transport.

No retries, redirects, alternate API origins, or provider-independent fake audio.
These endpoints do not expose cancellable asynchronous generation jobs.
"""
from __future__ import annotations
import base64
import json
import os
import platform
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from .media_contracts import MediaError

ORIGIN = 'https://api.elevenlabs.io'
CAPABILITIES = ('speech','sound_effects','music','transcription','alignment','catalog','local_import')
SUPPORTED = {'elevenlabs':('speech','sound_effects','music'), 'local':('local_import',)}

@dataclass
class Response:
    status: int
    headers: dict
    body: bytes

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

class Transport:
    def request(self, method, path, *, key, body=None):
        if not path.startswith('/v1/') or path.startswith('//') or '\\' in path:
            raise MediaError('HTTP_REJECTED')
        url = ORIGIN + path
        request = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
            headers={'xi-api-key':key,'Content-Type':'application/json'}, method=method)
        # Do not inherit proxy credentials or follow untrusted media download URLs.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        try:
            with opener.open(request, timeout=120) as reply:
                payload = reply.read(128_000_001)
                if len(payload) > 128_000_000: raise MediaError('MALFORMED_RESPONSE')
                return Response(reply.status, dict(reply.headers), payload)
        except urllib.error.HTTPError as exc:
            # Never export raw provider messages: they may echo prompts or secrets.
            return Response(exc.code, {}, b'')
        except (TimeoutError, OSError, urllib.error.URLError):
            raise MediaError('UNKNOWN_DISPATCH_OUTCOME') from None

def credential(ref):
    if not ref: raise MediaError('CREDENTIAL_UNAVAILABLE')
    value = None
    if ref['kind'] == 'env':
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',ref['name']): raise MediaError('CREDENTIAL_UNAVAILABLE')
        value = os.environ.get(ref['name'])
    elif ref['kind'] == 'keychain' and platform.system() == 'Darwin' and shutil.which('security'):
        args = ['security','find-generic-password','-s',ref['name'],'-w']
        if ref.get('account'): args.extend(['-a',ref['account']])
        p = subprocess.run(args,capture_output=True,timeout=15)
        if p.returncode == 0: value = p.stdout.decode().strip()
    elif ref['kind'] == 'secret-service' and shutil.which('secret-tool'):
        args = ['secret-tool','lookup','service',ref['name']]
        if ref.get('account'): args.extend(['account',ref['account']])
        p = subprocess.run(args,capture_output=True,timeout=15)
        if p.returncode == 0: value = p.stdout.decode().strip()
    if not value or '\n' in value or '\r' in value: raise MediaError('CREDENTIAL_UNAVAILABLE')
    return value

def response_error(response):
    if response.status in (401,403): return 'HTTP_UNAUTHORIZED'
    if response.status == 429: return 'HTTP_RATE_LIMIT'
    if response.status >= 500: return 'HTTP_SERVER_ERROR'
    if response.status != 200: return 'HTTP_REJECTED'
    return None

def prepare(request, text):
    cap = request['capability']; settings = request['settings']; model = request['model']
    if request['provider'] != 'elevenlabs' or cap not in SUPPORTED['elevenlabs']:
        raise MediaError('UNSUPPORTED_CAPABILITY')
    if not model: raise MediaError('UNSUPPORTED_SETTINGS')
    query = '?'+urllib.parse.urlencode({'output_format':request['output_format']})
    if not request['output_format'].startswith(('mp3_','wav_')):
        raise MediaError('UNSUPPORTED_SETTINGS')  # raw PCM requires explicit decoding contract
    if cap == 'speech':
        if not request['voice'] or set(settings)-{'stability','similarity_boost','style','speed','use_speaker_boost'}:
            raise MediaError('UNSUPPORTED_SETTINGS')
        path = '/v1/text-to-speech/'+urllib.parse.quote(request['voice'],safe='')
        if request['alignment'] != 'none': path += '/with-timestamps'
        body = {'text':text,'model_id':model,'voice_settings':settings}
        if request['language']: body['language_code'] = request['language']
    elif cap == 'sound_effects':
        if set(settings)-{'prompt_influence','loop'}: raise MediaError('UNSUPPORTED_SETTINGS')
        if request['alignment'] == 'required': raise MediaError('UNSUPPORTED_CAPABILITY')
        path = '/v1/sound-generation'
        body = {'text':text,'model_id':model,**settings}
        duration = request['target_duration_seconds']
        if duration is not None:
            if not .5 <= duration <= 30: raise MediaError('UNSUPPORTED_SETTINGS')
            body['duration_seconds'] = duration
    else:
        if set(settings)-{'force_instrumental'}: raise MediaError('UNSUPPORTED_SETTINGS')
        if request['alignment'] == 'required': raise MediaError('UNSUPPORTED_CAPABILITY')
        path = '/v1/music'; body = {'prompt':text,'model_id':model,**settings}
        duration = request['target_duration_seconds']
        if duration is not None:
            if not 3 <= duration <= 600: raise MediaError('UNSUPPORTED_SETTINGS')
            body['music_length_ms'] = round(duration*1000)
    return path+query, body

def decode(request, response):
    err = response_error(response)
    if err: raise MediaError(err)
    alignment = None
    payload = response.body
    if request['capability'] == 'speech' and request['alignment'] != 'none':
        try:
            raw = json.loads(payload)
            if not isinstance(raw,dict): raise MediaError('MALFORMED_RESPONSE')
            payload = base64.b64decode(raw['audio_base64'],validate=True)
            alignment = raw.get('alignment')
        except (ValueError, KeyError, TypeError): raise MediaError('MALFORMED_RESPONSE') from None
    headers = {k.lower():v for k,v in response.headers.items()}
    rid = headers.get('request-id') or headers.get('x-request-id')
    if rid and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}',rid): rid = None
    credits = None
    raw_usage = headers.get('character-cost')
    if raw_usage is not None:
        try:
            credits = float(raw_usage)
            if not 0 <= credits < 1e12: credits = None
        except (ValueError, TypeError): pass
    return payload, alignment, rid, credits

def inspect_account(transport, key):
    response = transport.request('GET','/v1/user/subscription',key=key)
    err = response_error(response)
    if err: raise MediaError(err)
    try:
        value = json.loads(response.body)
        if not isinstance(value,dict): raise MediaError('MALFORMED_RESPONSE')
        # Bounded allowlist, no raw user/account data or credential-bearing payloads.
        count,limit = value.get('character_count'),value.get('character_limit')
        remaining = max(0,limit-count) if type(count) in (int,float) and type(limit) in (int,float) else None
        tier=value.get('tier') if value.get('tier') in ('free','starter','creator','pro','scale','business','enterprise','growing_business','professional') else None
        return {'authentication':'established','remaining_credits':remaining,'tier':tier,
                'entitlement':'unknown','no_overage':value.get('max_credit_limit_extension') == 0 if 'max_credit_limit_extension' in value else None,'note':'Subscription allowance does not prove capability-specific music or output-format entitlement.'}
    except (ValueError, TypeError): raise MediaError('MALFORMED_RESPONSE') from None
