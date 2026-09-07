"""Strict shared media contracts and contained artifact I/O. No provider secrets."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import Draft202012Validator, FormatChecker

CONTRACTS = Path(__file__).resolve().parents[1] / 'contracts'
if not CONTRACTS.is_dir(): CONTRACTS = Path(__file__).resolve().parent / 'schemas'
class MediaError(ValueError):
    """Only stable, non-sensitive codes cross the media CLI boundary."""
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def now(): return datetime.now(timezone.utc).isoformat()
def digest(data): return hashlib.sha256(data).hexdigest()
def canonical(value): return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
def validate(kind, value):
    try:
        schema = json.loads((CONTRACTS / f'{kind}.schema.json').read_text())
        if list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)):
            raise MediaError('INVALID_CONTRACT')
        canonical(value)
    except (TypeError, ValueError) as exc:
        raise MediaError('INVALID_CONTRACT') from None
    return value

def contained(workspace, relative, *, must_exist=False):
    root = Path(workspace).resolve(strict=True)
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts or '\\' in str(p) or not p.parts:
        raise MediaError('PATH_OUTSIDE_WORKSPACE')
    current = root
    for part in p.parts:
        current /= part
        if current.is_symlink(): raise MediaError('SYMLINK_REJECTED')
    try: current.resolve(strict=must_exist).relative_to(root)
    except (ValueError, FileNotFoundError): raise MediaError('PATH_OUTSIDE_WORKSPACE') from None
    return current

def read_json(path):
    try:
        if Path(path).stat().st_size > 8_000_000: raise MediaError('ARTIFACT_TOO_LARGE')
        return json.loads(Path(path).read_text())
    except (OSError, ValueError): raise MediaError('INVALID_JSON_ARTIFACT') from None

def write_json(workspace, relative, value):
    path = contained(workspace, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Refuse replacement through a symlink, including a stale temporary path.
    tmp = contained(workspace, str(Path(relative).with_suffix('.tmp')))
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    with os.fdopen(fd, 'w') as f: f.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')
    os.replace(tmp, path)

def artifact(workspace, relative):
    p = contained(workspace, relative, must_exist=True)
    if not p.is_file() or p.stat().st_size > 128_000_000: raise MediaError('INVALID_ARTIFACT')
    return {'path':relative,'sha256':digest(p.read_bytes())}

def verify_ref(workspace, ref):
    if artifact(workspace, ref['path']) != ref: raise MediaError('ARTIFACT_HASH_MISMATCH')
    return contained(workspace, ref['path'], must_exist=True)
