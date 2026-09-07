"""Canonical, deterministic media/v1 schema source; run after changes."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
S = {'type':'string','minLength':1,'maxLength':4096}
ID = {'type':'string','pattern':'^[A-Za-z0-9][A-Za-z0-9_.-]{0,99}$'}
PATH = {'type':'string','minLength':1,'maxLength':512,'pattern':r'^(?!/)(?!.*(?:^|/)\.\.(?:/|$))(?!.*\\).+$'}
SHA = {'type':'string','pattern':'^[a-f0-9]{64}$'}
N = {'type':'number','minimum':0}
I = {'type':'integer','minimum':0}
B = {'type':'boolean'}
DT = {'type':'string','format':'date-time'}
def enum(*values): return {'enum':list(values)}
def arr(item): return {'type':'array','items':item,'maxItems':10000}
def obj(props, required=None): return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':False}
def nullable(schema): return {'anyOf':[schema,{'type':'null'}]}
REF = obj({'path':PATH,'sha256':SHA})
C = enum('speech','sound_effects','music','transcription','alignment','catalog','local_import')
RIGHTS = obj({'evidence':REF,'license':S,'attribution':nullable(S),'restrictions':arr(S),'intended_use':S})
BUDGET = obj({'max_credits':N,'max_cost':N,'currency':enum('USD'),'estimate_evidence':nullable(REF)})
SETTINGS = obj({'stability':{'type':'number','minimum':0,'maximum':1},'similarity_boost':{'type':'number','minimum':0,'maximum':1},'style':{'type':'number','minimum':0,'maximum':1},'speed':{'type':'number','minimum':0.7,'maximum':1.2},'use_speaker_boost':B,'prompt_influence':{'type':'number','minimum':0,'maximum':1},'loop':B,'force_instrumental':B},[])
REQUEST = obj({'schema':{'const':'videoops-media-request/v1'},'request_id':ID,'job_id':ID,'asset_id':ID,'requirement_id':ID,'shot_ids':arr(ID),'capability':C,'provider':ID,'model':nullable(ID),'voice':nullable(ID),'settings':SETTINGS,'input':REF,'language':nullable(ID),'target_duration_seconds':nullable(N),'output_format':ID,'alignment':enum('required','optional','none'),'authorization_id':nullable(ID),'budget':BUDGET,'attempt':{'type':'integer','minimum':1},'retry_of':nullable(ID),'rights':RIGHTS})
AUTH = obj({'schema':{'const':'videoops-media-authorization/v1'},'authorization_id':ID,'workspace':S,'provider':ID,'capabilities':arr(C),'models':arr(ID),'voices':arr(ID),'output_formats':arr(ID),'request_bounds':arr(obj({'fingerprint':SHA,'max_credits':N,'max_cost':N,'evidence':REF})),'max_calls':I,'max_credits':N,'max_cost':N,'currency':enum('USD'),'expires_at':DT,'credential_ref':nullable(obj({'kind':enum('env','keychain','secret-service'),'name':S,'account':nullable(S)})),'entitlements':arr(obj({'capability':C,'allowed':B,'expires_at':DT,'evidence':REF,'remaining_credits':nullable(N),'no_overage':B}))})
ALIGN = obj({'availability':enum('available','unavailable','not_requested'),'units':{'const':'seconds'},'time_origin':{'const':'original_media_start'},'source':nullable(S),'artifact':nullable(REF)})
METADATA = obj({'duration_seconds':N,'sample_rate':nullable(I),'channels':nullable(I),'codec':S,'streams':arr(obj({'type':S,'codec':S}))})
RESULT = obj({'schema':{'const':'videoops-media-result/v1'},'request_id':ID,'job_id':ID,'asset_id':ID,'requirement_id':ID,'shot_ids':arr(ID),'fingerprint':SHA,'attempt':I,'retry_of':nullable(ID),'state':enum('SUCCESS','BLOCKED','UNSUPPORTED','FAILED','CANCELLED','UNKNOWN_OUTCOME'),'provider':ID,'capability':C,'model':nullable(ID),'voice':nullable(ID),'settings':SETTINGS,'output_format':ID,'authorization_id':nullable(ID),'original':nullable(REF),'derived':arr(REF),'metadata':nullable(METADATA),'alignment':ALIGN,'provider_request_id':nullable(ID),'usage':obj({'credits':nullable(N),'cost':nullable(N),'currency':enum('USD'),'source':enum('provider_header','local','unavailable'),'reserved_credits':N,'reserved_cost':N}),'latency_seconds':N,'retries':I,'rights':RIGHTS,'verification':enum('local','mock','live'),'created_at':DT,'error':nullable(enum('AUTHORIZATION_REQUIRED','AUTHORIZATION_INVALID','BUDGET_EXHAUSTED','ENTITLEMENT_UNKNOWN','ENTITLEMENT_DENIED','CREDENTIAL_UNAVAILABLE','HTTP_UNAUTHORIZED','HTTP_RATE_LIMIT','HTTP_REJECTED','HTTP_SERVER_ERROR','UNSUPPORTED_CAPABILITY','UNSUPPORTED_SETTINGS','MALFORMED_RESPONSE','INVALID_MEDIA','MISSING_ALIGNMENT','ALIGNMENT_INVALID','UNKNOWN_DISPATCH_OUTCOME','CANCELLED_BY_OPERATOR')),'receipt_path':PATH,'manifest_path':PATH,'handoff_path':PATH})
for name,schema in [('media-request',REQUEST),('media-result',RESULT),('media-authorization',AUTH)]:
    schema = {'$schema':'https://json-schema.org/draft/2020-12/schema','$id':f'https://kujolang.ai/contracts/videoops/{name}/v1',**schema}
    destination=ROOT/'contracts'/f'{name}.schema.json'
    text=json.dumps(schema,indent=2)+'\n'
    if '--check' in sys.argv:
        if not destination.exists() or destination.read_text()!=text: raise SystemExit(f'{name} schema drift')
    else: destination.write_text(text)
