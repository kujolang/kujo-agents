"""Canonical package schema regression tests; no model or runtime execution."""
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class AgentContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roles = read('agent-registry.json')['agents']
        cls.manifest = Draft202012Validator(read('schemas/agent-manifest.schema.json'))

    def test_every_canonical_manifest(self):
        self.assertEqual(len(self.roles), 85)
        for role in self.roles:
            with self.subTest(role=role['id']):
                manifest = read(role['path'] + '/manifest.json')
                self.manifest.validate(manifest)
                self.assertEqual(role['id'], manifest['id'])
                self.assertEqual(role['package'], manifest['classification']['package'])

    def test_every_io_and_shared_schema_is_valid(self):
        paths = list((ROOT / 'schemas').rglob('*.schema.json'))
        for role in self.roles:
            paths.extend(ROOT / role['path'] / name for name in ('input.schema.json', 'output.schema.json'))
        for path in paths:
            with self.subTest(schema=str(path.relative_to(ROOT))):
                schema = json.loads(path.read_text())
                Draft202012Validator.check_schema(schema)
                validator = Draft202012Validator(schema)
                self.assertFalse(validator.is_valid('not an object'))

    def test_invalid_common_fields_are_rejected_for_every_role(self):
        for role in self.roles:
            original = read(role['path'] + '/manifest.json')
            for field, value in [('version', '1x0x0'), ('id', '../escape'), ('unexpected', True)]:
                with self.subTest(role=role['id'], field=field):
                    manifest = copy.deepcopy(original)
                    manifest[field] = value
                    self.assertFalse(self.manifest.is_valid(manifest))

    def test_package_specific_contracts_remain_strict(self):
        for role in self.roles:
            original = read(role['path'] + '/manifest.json')
            if role['package'] == 'videoops':
                mutations = [
                    ('inputs', [{'name': 'x', 'description': 'x'}]),
                    ('skills', ['']),
                    ('model_policy', {**original['model_policy'], 'max_economical_attempts': 3}),
                    ('model_policy', {**original['model_policy'], 'provider_binding': 'unauthorized-provider'}),
                    ('model_policy', {**original['model_policy'], 'stage_local_escalation': False}),
                ]
            else:
                mutations = [('inputs', ['loose input']), ('outputs', ['loose output']), ('skills', []), ('model_policy', {})]
            for field, value in mutations:
                with self.subTest(role=role['id'], field=field):
                    manifest = copy.deepcopy(original)
                    manifest[field] = value
                    self.assertFalse(self.manifest.is_valid(manifest))

    def test_shared_handoff_requires_evidence_and_ownership(self):
        validator = Draft202012Validator(read('schemas/handoff.schema.json'))
        handoff = {
            'schema': 'kujo.handoff/v1', 'assignment': 'review',
            'current_owner': 'core-developer', 'next_owner': 'code-reviewer',
            'goal': 'Review the bounded change', 'scope': 'proposed files',
            'evidence': [], 'decisions': [], 'unresolved_questions': [],
            'allowed_next_actions': ['Review'], 'stop_condition': 'Report findings',
            'permission_mode': 'PROPOSE',
        }
        validator.validate(handoff)
        for field in ('current_owner', 'next_owner', 'evidence', 'stop_condition'):
            invalid = dict(handoff)
            del invalid[field]
            self.assertFalse(validator.is_valid(invalid), field)
        handoff['permission_mode'] = 'ROOT'
        self.assertFalse(validator.is_valid(handoff))


if __name__ == '__main__':
    unittest.main()
