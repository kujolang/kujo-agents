"""Exact-candidate review ledger for harness-owned production.

The local CLI caller is the authority boundary; artifacts cannot grant themselves
permission. Review outcomes are attestations, not a claim that this process can
watch or listen. Legacy fixture approvals are deliberately not accepted here.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .errors import ConflictError, PolicyError

VERSION = 'videoops-review-decision/v1'
CAPABILITIES = {'deterministic_validation', 'visual_playback', 'audio_listening', 'embedded_feed_review'}
COUNTERS = ('user_revisions', 'render_attempts', 'technical_repairs', 'critic_failures', 'review_attempts')


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def validate_decision(value):
    fields = {'version', 'id', 'candidate_sha256', 'technical', 'perceptual', 'reviewer', 'evidence', 'defects', 'reviewed_at'}
    if not isinstance(value, dict) or set(value) != fields or value.get('version') != VERSION:
        raise PolicyError('expected strict videoops-review-decision/v1 artifact')
    if not isinstance(value['id'], str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', value['id']):
        raise PolicyError('invalid review id')
    if not isinstance(value['candidate_sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', value['candidate_sha256']):
        raise PolicyError('invalid candidate checksum')
    if value['technical'] not in ('PASS', 'FAIL', 'NOT_REVIEWED') or value['perceptual'] not in ('PASS', 'FAIL', 'REVIEW_INCOMPLETE', 'NOT_REVIEWED'):
        raise PolicyError('invalid review outcome')
    reviewer = value['reviewer']
    if not isinstance(reviewer, dict) or set(reviewer) != {'identity', 'type', 'capabilities_exercised'}:
        raise PolicyError('reviewer identity/type/capabilities required')
    if not isinstance(reviewer['identity'], str) or not reviewer['identity'].strip() or len(reviewer['identity']) > 256:
        raise PolicyError('invalid reviewer identity')
    if reviewer['type'] not in ('human', 'agent', 'technical_tool'):
        raise PolicyError('invalid reviewer type')
    caps = reviewer['capabilities_exercised']
    if not isinstance(caps, list) or any(not isinstance(c, str) or c not in CAPABILITIES for c in caps) or len(caps) != len(set(caps)):
        raise PolicyError('invalid exercised capabilities')
    if value['technical'] != 'NOT_REVIEWED' and 'deterministic_validation' not in caps:
        raise PolicyError('technical outcome requires exercised deterministic validation')
    if reviewer['type'] == 'technical_tool' and value['perceptual'] in ('PASS', 'FAIL'):
        raise PolicyError('technical tool cannot attest perceptual review')
    try:
        timestamp = datetime.fromisoformat(value['reviewed_at'].replace('Z', '+00:00'))
        if timestamp.tzinfo is None or timestamp > datetime.now(timezone.utc):
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise PolicyError('reviewed_at must be a non-future timezone-aware timestamp') from None
    if not isinstance(value['evidence'], list) or not value['evidence'] or any(not isinstance(p, str) or not p for p in value['evidence']):
        raise PolicyError('review requires local evidence references')
    if not isinstance(value['defects'], list):
        raise PolicyError('defects must be an array')
    for defect in value['defects']:
        if not isinstance(defect, dict) or set(defect) != {'gate', 'description'} or defect['gate'] not in ('technical', 'perceptual') or not isinstance(defect['description'], str) or not defect['description'].strip():
            raise PolicyError('invalid artifact defect')
        if value[defect['gate']] != 'FAIL':
            raise PolicyError('artifact defects require corresponding FAIL outcome')
    for gate in ('technical', 'perceptual'):
        if value[gate] == 'FAIL' and not any(d['gate'] == gate for d in value['defects']):
            raise PolicyError('FAIL requires an actionable artifact defect')
    return value


class ReviewService:
    def __init__(self, workspace: Path):
        self.workspace = Path(workspace).resolve(strict=True)
        if not self.workspace.is_dir():
            raise PolicyError('review workspace must be a directory')
        self.directory = self._path('review/runtime', exists=False)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, relative, *, exists=True):
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise PolicyError('artifact paths must be workspace relative')
        path = self.workspace / relative
        if not path.resolve().is_relative_to(self.workspace):
            raise PolicyError('artifact escapes workspace')
        # Reject symlinks even when currently contained: prevent replace/redirect surprises.
        cursor = path
        while cursor != self.workspace:
            if cursor.is_symlink():
                raise PolicyError('symlink artifacts are not accepted')
            cursor = cursor.parent
        if exists and not path.is_file():
            raise PolicyError('required artifact is not a regular file')
        return path

    @contextmanager
    def _ledger(self):
        lock = self._path('review/runtime/.lock', exists=False)
        with lock.open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            path = self._path('review/runtime/ledger.json', exists=False)
            data = json.loads(path.read_text()) if path.exists() else {
                'version': 'videoops-review-ledger/v1', 'active': None, 'history': [],
                'decisions': [], 'render_attempts': [], 'counters': dict.fromkeys(COUNTERS, 0), 'max_defect_cycles': 3,
            }
            if data.get('version') != 'videoops-review-ledger/v1':
                raise PolicyError('unsupported review ledger version')
            yield data
            fd, name = tempfile.mkstemp(dir=self.directory, prefix='.ledger-')
            try:
                with os.fdopen(fd, 'w') as output:
                    json.dump(data, output, indent=2)
                    output.write('\n')
                    output.flush()
                    os.fsync(output.fileno())
                os.replace(name, path)
            finally:
                if os.path.exists(name):
                    os.unlink(name)

    def submit_candidate(self, relative_path: str, *, mandatory_capabilities=None, user_revision=False, repair_kind=None, max_defect_cycles=3, render_attempt_id=None):
        caps = ['visual_playback', 'audio_listening'] if mandatory_capabilities is None else mandatory_capabilities
        if not isinstance(caps, list) or not caps or any(not isinstance(c, str) or c not in CAPABILITIES - {'deterministic_validation'} for c in caps) or len(set(caps)) != len(caps):
            raise PolicyError('declare nonempty mandatory perceptual capabilities')
        if type(max_defect_cycles) is not int or max_defect_cycles < 1:
            raise PolicyError('max_defect_cycles must be positive')
        if repair_kind not in (None, 'technical', 'perceptual'):
            raise PolicyError('invalid repair kind')
        candidate = self._path(relative_path)
        sha = digest(candidate)
        with self._ledger() as data:
            active = data['active']
            if active and active['sha256'] == sha:
                if active['mandatory_capabilities'] != caps or data['max_defect_cycles'] != max_defect_cycles:
                    raise ConflictError('cannot change configured gates on an active candidate')
                return self._status(data)
            if active:
                data['history'].append(active)
            data['active'] = {'path': relative_path, 'sha256': sha, 'mandatory_capabilities': caps,
                              'submitted_at': datetime.now(timezone.utc).isoformat()}
            if active is None:
                data['max_defect_cycles'] = max_defect_cycles
            elif data['max_defect_cycles'] != max_defect_cycles:
                raise ConflictError('cannot change defect cycle limits during review')
            if render_attempt_id is not None:
                attempt = next((a for a in data.get('render_attempts', []) if a['id'] == render_attempt_id), None)
                if not attempt or attempt['outcome'] != 'succeeded':
                    raise PolicyError('candidate requires a recorded successful render attempt')
                if attempt.get('candidate_sha256') not in (None, sha):
                    raise ConflictError('render attempt already binds another candidate')
                attempt['candidate_sha256'] = sha
            else:
                data['counters']['render_attempts'] += 1
                data['counters']['user_revisions'] += int(bool(user_revision))
                data['counters']['technical_repairs'] += int(repair_kind == 'technical')
            return self._status(data)

    def record_render_attempt(self, attempt_id, outcome, *, user_revision=False, repair_kind=None):
        """Harness records actual failed/successful renderer attempts without new media."""
        if not isinstance(attempt_id, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', attempt_id):
            raise PolicyError('invalid render attempt id')
        if outcome not in ('succeeded', 'failed') or repair_kind not in (None, 'technical', 'perceptual'):
            raise PolicyError('invalid render attempt outcome or repair kind')
        record = {'id': attempt_id, 'outcome': outcome, 'user_revision': bool(user_revision), 'repair_kind': repair_kind}
        with self._ledger() as data:
            attempts = data.setdefault('render_attempts', [])
            existing = next((a for a in attempts if a['id'] == attempt_id), None)
            if existing:
                if any(existing[k] != v for k, v in record.items()):
                    raise ConflictError('render attempt id has conflicting evidence')
            else:
                attempts.append(record)
                data['counters']['render_attempts'] += 1
                data['counters']['user_revisions'] += int(bool(user_revision))
                data['counters']['technical_repairs'] += int(repair_kind == 'technical')
            return {'render_attempt': record, 'counters': dict(data['counters'])}

    def record(self, decision: dict, *, local_authorized=False):
        if local_authorized is not True:
            raise PolicyError('recording review requires explicit local operator authorization')
        validate_decision(decision)
        with self._ledger() as data:
            self._current(data)
            if decision['candidate_sha256'] != data['active']['sha256']:
                raise ConflictError('review checksum does not match active candidate')
            for existing in data['decisions']:
                if existing['decision']['id'] == decision['id']:
                    if existing['decision'] != decision:
                        raise ConflictError('review id already has a different decision')
                    return self._status(data)
            if decision['perceptual'] == 'PASS' and not set(data['active']['mandatory_capabilities']).issubset(decision['reviewer']['capabilities_exercised']):
                raise PolicyError('perceptual PASS requires all configured capabilities exercised')
            evidence = [{'path': relative, 'sha256': digest(self._path(relative))} for relative in decision['evidence']]
            data['decisions'].append({'decision': decision, 'evidence': evidence,
                                      'authority': 'explicit-local-operator', 'recorded_at': datetime.now(timezone.utc).isoformat()})
            data['counters']['review_attempts'] += 1
            if decision['perceptual'] == 'FAIL':
                data['counters']['critic_failures'] += 1
            return self._status(data)

    def _current(self, data):
        if data['active'] is None:
            raise ConflictError('no candidate submitted')
        if digest(self._path(data['active']['path'])) != data['active']['sha256']:
            raise ConflictError('candidate bytes changed; submit the corrected candidate for new review')
        promotion = data['active'].get('promotion')
        if promotion and digest(self._path(promotion['path'])) != promotion['sha256']:
            raise ConflictError('promoted output bytes changed; output no longer has exact-candidate approval')

    def _status(self, data):
        self._current(data)
        technical = perceptual = 'NOT_REVIEWED'
        selected = {}
        current = [r for r in data['decisions'] if r['decision']['candidate_sha256'] == data['active']['sha256']]
        for record in current:
            decision = record['decision']
            for gate in ('technical', 'perceptual'):
                if decision[gate] != 'NOT_REVIEWED':
                    selected[gate] = record
        if 'technical' in selected:
            technical = selected['technical']['decision']['technical']
        if 'perceptual' in selected:
            perceptual = selected['perceptual']['decision']['perceptual']
            if perceptual == 'PASS' and not set(data['active']['mandatory_capabilities']).issubset(selected['perceptual']['decision']['reviewer']['capabilities_exercised']):
                perceptual = 'REVIEW_INCOMPLETE'
        for record in selected.values():
            for evidence in record['evidence']:
                if digest(self._path(evidence['path'])) != evidence['sha256']:
                    raise ConflictError('review evidence changed; record a new review with preserved evidence')
        # Technical defects take priority over an unavailable listening review.
        if 'FAIL' in (technical, perceptual):
            failed_candidates = {r['decision']['candidate_sha256'] for r in data['decisions'] if 'FAIL' in (r['decision']['technical'], r['decision']['perceptual'])}
            state = 'REVISION_REQUIRED' if len(failed_candidates) <= data['max_defect_cycles'] else 'BLOCKED'
            next_action = 'repair' if state == 'REVISION_REQUIRED' else None
        elif technical == perceptual == 'PASS':
            state, next_action = 'APPROVED', 'promote'
        else:
            state, next_action = 'REVIEW_INCOMPLETE', 'review'
        return {'state': state, 'next_action': next_action, 'technical': technical, 'perceptual': perceptual,
                'candidate': data['active'], 'counters': dict(data['counters']),
                'review_ids': [r['decision']['id'] for r in current]}

    def status(self):
        with self._ledger() as data:
            return self._status(data)

    def resume(self):
        """Return the next harness action; never regenerate assets or rerender."""
        return self.status()

    def promote(self, destination='output/final.mp4', *, local_authorized=False):
        if local_authorized is not True:
            raise PolicyError('promotion requires explicit local operator authorization')
        with self._ledger() as data:
            result = self._status(data)
            if result['state'] != 'APPROVED':
                raise ConflictError('all configured exact-candidate gates must PASS before promotion')
            source = self._path(data['active']['path'])
            target = self._path(destination, exists=False)
            used_evidence = {self._path(e['path'], exists=False) for r in data['decisions'] for e in r['evidence']}
            # Promotion is an output operation, never an arbitrary workspace write.
            # Compare normalized Paths so './qa.json' cannot alias protected evidence.
            output_root = self._path('output', exists=False)
            if (target == source or not target.is_relative_to(output_root)
                    or target == output_root or target in used_evidence
                    or any(part.startswith('.videoops') for part in target.relative_to(self.workspace).parts)):
                raise PolicyError('final must be a distinct output artifact, never evidence or runtime metadata')
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(dir=target.parent, prefix='.promote-')
            os.close(fd)
            try:
                shutil.copyfile(source, name)
                if digest(name) != data['active']['sha256']:
                    raise ConflictError('candidate changed during promotion')
                self._current(data)
                os.replace(name, target)
            finally:
                if os.path.exists(name):
                    os.unlink(name)
            data['active']['promotion'] = {'path': destination, 'sha256': digest(target), 'promoted_at': datetime.now(timezone.utc).isoformat()}
            return {**result, 'final': data['active']['promotion']}
