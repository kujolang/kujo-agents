"""Review-state tests use opaque candidate bytes, never claim decoded video QA."""
import copy
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from videoops.errors import ConflictError, PolicyError
from videoops.review import ReviewService, validate_decision


class ReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'output').mkdir()
        self.candidate = self.root / 'output/draft.mp4'
        self.candidate.write_bytes(b'opaque candidate revision 1')
        (self.root / 'qa.json').write_text('{"test_evidence":true}')
        self.service = ReviewService(self.root)
        self.service.submit_candidate('output/draft.mp4')

    def tearDown(self):
        self.temp.cleanup()

    def decision(self, identity='review-1', technical='PASS', perceptual='REVIEW_INCOMPLETE'):
        caps = ['deterministic_validation']
        if perceptual in ('PASS', 'FAIL'):
            caps += ['visual_playback', 'audio_listening']
        return {'version':'videoops-review-decision/v1', 'id':identity,
                'candidate_sha256':self.service.status()['candidate']['sha256'],
                'technical':technical, 'perceptual':perceptual,
                'reviewer':{'identity':'test reviewer attestation', 'type':'human', 'capabilities_exercised':caps},
                'reviewed_at':datetime.now(timezone.utc).isoformat(), 'evidence':['qa.json'],
                'defects':[{'gate':g, 'description':'A test defect requires correction'} for g, v in [('technical',technical),('perceptual',perceptual)] if v == 'FAIL']}

    def record(self, value):
        return self.service.record(value, local_authorized=True)

    def test_incomplete_resume_preserves_candidate_and_counters(self):
        result = self.record(self.decision())
        self.assertEqual(result['state'], 'REVIEW_INCOMPLETE')
        self.assertEqual(result['next_action'], 'review')
        for _ in range(5):
            self.assertEqual(self.service.resume(), result)
        self.assertEqual(result['counters']['technical_repairs'], 0)
        self.assertEqual(result['counters']['critic_failures'], 0)
        self.assertEqual(self.candidate.read_bytes(), b'opaque candidate revision 1')
        with self.assertRaises(ConflictError):
            self.service.promote(local_authorized=True)

    def test_later_human_pass_combines_technical_and_perceptual(self):
        self.record(self.decision())
        result = self.record(self.decision('human-2', technical='NOT_REVIEWED', perceptual='PASS'))
        self.assertEqual(result['state'], 'APPROVED')
        promoted = self.service.promote(local_authorized=True)
        self.assertEqual((self.root/'output/final.mp4').read_bytes(), self.candidate.read_bytes())
        self.assertEqual(promoted['final']['sha256'], result['candidate']['sha256'])
        self.assertEqual(ReviewService(self.root).status()['state'], 'APPROVED')

    def test_mixed_technical_fail_and_missing_listening_routes_repair(self):
        result = self.record(self.decision(technical='FAIL'))
        self.assertEqual(result['state'], 'REVISION_REQUIRED')
        self.assertEqual(result['next_action'], 'repair')
        self.assertEqual(result['counters']['critic_failures'], 0)
        self.candidate.write_bytes(b'corrected candidate 2')
        new = self.service.submit_candidate('output/draft.mp4', repair_kind='technical')
        self.assertEqual(new['state'], 'REVIEW_INCOMPLETE')
        self.assertEqual(new['counters']['technical_repairs'], 1)
        self.assertEqual(new['counters']['render_attempts'], 2)
        self.assertEqual(self.record(self.decision('corrected', perceptual='PASS'))['state'], 'APPROVED')

    def test_actual_perceptual_failure_consumes_critic_counter(self):
        failed = self.record(self.decision(perceptual='FAIL'))
        self.assertEqual(failed['state'], 'REVISION_REQUIRED')
        self.assertEqual(failed['counters']['critic_failures'], 1)

    def test_stale_hash_and_in_place_changed_bytes_rejected(self):
        stale = self.decision(perceptual='PASS')
        self.record(stale)
        self.candidate.write_bytes(b'new audio same filename')
        with self.assertRaises(ConflictError):
            self.service.promote(local_authorized=True)
        self.service.submit_candidate('output/draft.mp4', user_revision=True)
        with self.assertRaises(ConflictError):
            self.record(stale)
        self.assertEqual(self.service.status()['counters']['user_revisions'], 1)
        ledger = json.loads((self.root/'review/runtime/ledger.json').read_text())
        self.assertEqual(len(ledger['history']), 1)
        self.assertEqual(len(ledger['decisions']), 1)

    def test_mutated_promoted_output_loses_approval(self):
        self.record(self.decision(perceptual='PASS'))
        self.service.promote(local_authorized=True)
        (self.root/'output/final.mp4').write_bytes(b'modified exported sound')
        with self.assertRaises(ConflictError):
            self.service.status()

    def test_evidence_mutation_invalidates_promotion(self):
        self.record(self.decision(perceptual='PASS'))
        (self.root/'qa.json').write_text('changed evidence')
        with self.assertRaises(ConflictError):
            self.service.promote(local_authorized=True)

    def test_operator_authority_is_not_artifact_data(self):
        decision = self.decision(perceptual='PASS')
        with self.assertRaises(PolicyError):
            self.service.record(decision)
        decision['local_authorized'] = True
        with self.assertRaises(PolicyError):
            self.record(decision)
        self.record(self.decision(perceptual='PASS'))
        with self.assertRaises(PolicyError):
            self.service.promote()

    def test_capability_claims_checked_for_configured_gates(self):
        decision = self.decision(perceptual='PASS')
        decision['reviewer']['capabilities_exercised'].remove('audio_listening')
        with self.assertRaises(PolicyError):
            self.record(decision)
        decision = self.decision(perceptual='PASS')
        decision['reviewer']['type'] = 'technical_tool'
        with self.assertRaises(PolicyError):
            self.record(decision)

    def test_fixture_approval_is_not_migrated(self):
        with self.assertRaises(PolicyError):
            self.record({'status':'PASS'})

    def test_review_idempotency_and_conflict(self):
        decision = self.decision()
        first = self.record(decision)
        self.assertEqual(self.record(copy.deepcopy(decision)), first)
        decision['perceptual'] = 'NOT_REVIEWED'
        with self.assertRaises(ConflictError):
            self.record(decision)
        self.assertEqual(self.service.status()['counters']['review_attempts'], 1)

    def test_paths_reject_absolute_traversal_symlink(self):
        for path in (str(self.candidate), '../elsewhere.mp4'):
            with self.assertRaises(PolicyError):
                self.service.submit_candidate(path)
        (self.root/'link.mp4').symlink_to(self.candidate)
        with self.assertRaises(PolicyError):
            self.service.submit_candidate('link.mp4')
        decision = self.decision()
        decision['evidence'] = ['../external.json']
        with self.assertRaises(PolicyError):
            self.record(decision)

    def test_missing_evidence_and_fail_without_defect_rejected(self):
        decision = self.decision(technical='FAIL')
        decision['defects'] = []
        with self.assertRaises(PolicyError):
            self.record(decision)
        decision = self.decision()
        decision['evidence'] = ['absent.json']
        with self.assertRaises(PolicyError):
            self.record(decision)

    def test_defect_cycle_limit_survives_candidate_changes(self):
        for number in range(4):
            self.candidate.write_bytes(f'bad candidate {number}'.encode())
            self.service.submit_candidate('output/draft.mp4', repair_kind='technical')
            result = self.record(self.decision(f'failure-{number}', technical='FAIL'))
        self.assertEqual(result['state'], 'BLOCKED')
        self.assertIsNone(result['next_action'])

    def test_unchanged_submit_does_not_consume_render(self):
        self.service.submit_candidate('output/draft.mp4')
        self.assertEqual(self.service.status()['counters']['render_attempts'], 1)

    def test_failed_render_attempts_recorded_once_and_success_bound(self):
        initial = self.service.status()['counters']['render_attempts']
        self.service.record_render_attempt('render-failed', 'failed', repair_kind='technical')
        self.service.record_render_attempt('render-failed', 'failed', repair_kind='technical')
        self.service.record_render_attempt('render-success', 'succeeded', repair_kind='technical')
        self.candidate.write_bytes(b'new corrected candidate after renderer failure')
        result = self.service.submit_candidate('output/draft.mp4', render_attempt_id='render-success')
        self.assertEqual(result['counters']['render_attempts'], initial + 2)
        self.assertEqual(result['counters']['technical_repairs'], 2)
        self.candidate.write_bytes(b'another candidate cannot reuse renderer receipt')
        with self.assertRaises(ConflictError):
            self.service.submit_candidate('output/draft.mp4', render_attempt_id='render-success')

    def test_concurrent_records_keep_all_decisions(self):
        from concurrent.futures import ThreadPoolExecutor
        decisions = [self.decision(f'concurrent-{i}') for i in range(8)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda d: ReviewService(self.root).record(d, local_authorized=True), decisions))
        result = self.service.status()
        self.assertEqual(result['counters']['review_attempts'], 8)
        self.assertEqual(len(result['review_ids']), 8)

    def test_final_cannot_overwrite_review_evidence(self):
        self.record(self.decision(perceptual='PASS'))
        with self.assertRaises(PolicyError):
            self.service.promote('qa.json', local_authorized=True)

    def test_promotion_alias_cannot_overwrite_evidence_or_runtime(self):
        (self.root/'output/qa.json').write_text('evidence under output')
        decision = self.decision(perceptual='PASS')
        decision['evidence'] = ['output/qa.json']
        self.record(decision)
        for target in ('./output/qa.json', 'output/./qa.json', './qa.json', '.videoops-media/state.sqlite3', 'output/.videoops-state/db'):
            with self.assertRaises(PolicyError):
                self.service.promote(target, local_authorized=True)
        self.assertEqual((self.root/'output/qa.json').read_text(), 'evidence under output')

    def test_future_unknown_version_and_unknown_fields(self):
        for field, value in [('version','v999'), ('reviewed_at','2999-01-01T00:00:00Z'), ('unsupported',True)]:
            decision = self.decision()
            decision[field] = value
            with self.assertRaises(PolicyError):
                validate_decision(decision)

