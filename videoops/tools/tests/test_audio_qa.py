from __future__ import annotations
import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import wave

from videoops.audio_qa import (compare_cue, compare_preservation, contained, inspect_audio,
                               levels, parse_srt, phrase_findings, validate_segments, decode, _bounded_decode)


class SignalTests(unittest.TestCase):
    def test_tail_after_silence_is_bounded_heuristic_not_trim(self):
        pcm = [0.] * 1000
        pcm[100:300] = [.2] * 200
        pcm[700:750] = [.1] * 50
        findings = phrase_findings(pcm, 1000, 1, [{"start": .1, "end": .3, "text": "Hello"}])
        tails = [f for f in findings if f["code"] == "UNALIGNED_BURST_AFTER_SILENCE"]
        self.assertEqual(len(tails), 1)
        self.assertAlmostEqual(tails[0]["range_seconds"][0], .7)
        self.assertFalse(tails[0]["repair_candidate"]["automatic_trim_allowed"])
        self.assertEqual(pcm[700], .1)

    def test_alignment_margin_does_not_trim_consonant(self):
        pcm = [0.] * 1000
        pcm[100:345] = [.2] * 245
        result = phrase_findings(pcm, 1000, 1, [{"start": .1, "end": .3, "text": "word"}])
        self.assertNotIn("UNALIGNED_BURST_AFTER_SILENCE", [x["code"] for x in result])

    def test_duplicate_and_abrupt_boundary(self):
        pcm = [.2] * 100 + [0.] * 100 + [.2] * 100
        result = phrase_findings(pcm, 1000, 1, [])
        self.assertIn("POTENTIAL_DUPLICATE_FRAGMENT", [x["code"] for x in result])
        self.assertEqual(len([x for x in result if x["code"] == "ABRUPT_NONZERO_CUT"]), 2)

    def test_preservation_detects_unintended_change_outside_repair(self):
        original, derived = [.1] * 100, [.1] * 100
        derived[80:90] = [0.] * 10
        self.assertTrue(compare_preservation(original, derived, 100, 1, [[.8, .9]])["passed"])
        derived[10] = 0
        result = compare_preservation(original, derived, 100, 1, [[.8, .9]])
        self.assertFalse(result["passed"])
        self.assertEqual(result["changed_channel_samples"], 1)
        self.assertFalse(compare_preservation(original, original[:-1], 100, 1, [])["passed"])
        self.assertFalse(compare_preservation(original, original, 100, 1, [[0, 1]])["passed"])
        self.assertTrue(compare_preservation(original, [.2]*100, 100, 1, [], expected_gain=2)["passed"])
        with self.assertRaises(ValueError):
            compare_preservation(original, original, 100, 1, [[-.1, 1]])

    def test_mastering_energy_increase_even_when_peak_same(self):
        before = [.5] + [.01] * 99
        after = [.5] + [.1] * 99
        result = compare_cue(before, after, 100, 1, 0, 1)
        self.assertEqual(result["peak_change_db"], 0)
        self.assertGreater(result["rms_change_db"], 0)
        self.assertFalse(result["passed"])
        self.assertFalse(compare_cue([0.]*100, after, 100, 1, 0, 1)["passed"])
        with self.assertRaises(ValueError):
            compare_cue(before, after, 100, 1, 0, 2)

    def test_caption_and_alignment_validation(self):
        self.assertEqual(validate_segments([{"start": 0, "end": 1, "text": "a"}], 2), [])
        for segments in ([{"start": -1, "end": 1, "text": "a"}], [{"start": 0, "end": 3, "text": "a"}],
                         [{"start": float('nan'), "end": 1, "text": "a"}], [{"start": 1, "end": 1, "text": "a"}],
                         [{"start": 0, "end": 1, "text": ""}], [{"start": 0, "end": 1, "text": "a"}, {"start": .5, "end": 1.5, "text": "b"}]):
            self.assertTrue(validate_segments(segments, 2))
        self.assertEqual(parse_srt("1\n00:00:00,100 --> 00:00:00,500\nHello\n")[0]["start"], .1)
        with self.assertRaises(ValueError):
            parse_srt("1\n00:99:00,000 --> 00:99:01,000\nno")

    def test_clipping_counts_channels_and_silence_null(self):
        self.assertEqual(levels([1., -1., 1.1, -.5])["clipped_channel_samples"], 3)
        self.assertIsNone(levels([0.])["rms_dbfs"])


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/ffprobe required")
class DecodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.rate = 8000
        self.pcm = [.2 * math.sin(2 * math.pi * 400 * i / self.rate) for i in range(self.rate)]
        self.write("voice.wav", self.pcm)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, pcm):
        with wave.open(str(self.root / name), "wb") as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(self.rate)
            data = array.array("h", [round(max(-1, min(.999969, x)) * 32768) for x in pcm])
            import sys
            if sys.byteorder != "little":
                data.byteswap()
            out.writeframes(data.tobytes())

    def test_decodable_metadata_loudness_truepeak_and_caption(self):
        (self.root / "caption.srt").write_text("1\n00:00:00,000 --> 00:00:00,800\nHello\n")
        before = (self.root / "voice.wav").read_bytes()
        report = inspect_audio(self.root, "voice.wav", requirements={"sample_rate": 8000, "channels": 1, "codec": "pcm_s16le", "duration_seconds": 1}, captions="caption.srt")
        self.assertTrue(report["passed"], report)
        self.assertIsNotNone(report["checks"]["true_peak_dbtp"])
        self.assertIsNotNone(report["checks"]["integrated_loudness_lufs"])
        self.assertEqual(report["perceptual"]["status"], "REVIEW_INCOMPLETE")
        self.assertFalse(report["perceptual"]["listening_exercised"])
        self.assertEqual((self.root / "voice.wav").read_bytes(), before)
        json.dumps(report, allow_nan=False)

    def test_invalid_required_properties_alignment_captions(self):
        report = inspect_audio(self.root, "voice.wav", requirements={"sample_rate": 48000, "channels": 2, "codec": "aac", "duration_seconds": 5, "alignment_required": True, "captions_required": True})
        self.assertFalse(report["passed"])
        self.assertGreaterEqual(len(report["deterministic"]["failures"]), 6)
        (self.root / "bad.srt").write_text("not valid")
        self.assertFalse(inspect_audio(self.root, "voice.wav", captions="bad.srt")["passed"])
        (self.root / "bad.wav").write_bytes(b"not media")
        self.assertFalse(inspect_audio(self.root, "bad.wav")["passed"])

    def test_float_clipped_samples_and_truepeak_ceiling(self):
        # Encode a float WAV, retaining out-of-range samples rather than clipping
        # them with a PCM integer writer before the measurement.
        raw = array.array("f", [1.1, -1.1] * 4000)
        import sys
        if sys.byteorder != "little":
            raw.byteswap()
        subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "8000", "-ac", "1", "-i", "pipe:0", "-c:a", "pcm_f32le", str(self.root / "hot.wav")], input=raw.tobytes(), check=True, capture_output=True)
        result = inspect_audio(self.root, "hot.wav")
        self.assertEqual(result["checks"]["levels"]["clipped_channel_samples"], 8000)
        self.assertFalse(result["passed"])
        self.assertGreater(result["checks"]["true_peak_dbtp"], 0)

    def test_inter_sample_true_peak_differs_from_sample_peak(self):
        rate = 48000
        raw = array.array("f", [1.1 * math.sin(2*math.pi*12000*i/rate + math.pi/4) for i in range(rate)])
        import sys
        if sys.byteorder != "little":
            raw.byteswap()
        subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0", "-c:a", "pcm_f32le", str(self.root / "intersample.wav")], input=raw.tobytes(), check=True, capture_output=True)
        report = inspect_audio(self.root, "intersample.wav")
        self.assertEqual(report["checks"]["levels"]["clipped_channel_samples"], 0)
        self.assertLess(report["checks"]["levels"]["peak_dbfs"], 0)
        self.assertGreater(report["checks"]["true_peak_dbtp"], 0)
        self.assertFalse(report["passed"])

    def test_declared_internal_cut_and_invalid_config(self):
        pcm = [0.] * 4000 + [.3] * 4000
        self.write("cut.wav", pcm)
        report = inspect_audio(self.root, "cut.wav", requirements={"cut_times_seconds": [.5]})
        self.assertIn("ABRUPT_DECLARED_CUT", [f["code"] for f in report["heuristic_findings"]])
        for requirements in ({"maximum_true_peak_dbtp": float("nan")}, {"maximum_clipped_samples": -1}, {"loudness_range_lufs": [2, -2]}, {"heuristic_thresholds": {"gap_seconds": -1}}):
            self.assertFalse(inspect_audio(self.root, "voice.wav", requirements=requirements)["passed"])
        self.assertFalse(inspect_audio(self.root, "voice.wav", stems="invalid")["passed"])

    def test_actual_derived_file_preservation_and_source_provenance(self):
        altered = self.pcm.copy()
        altered[6400:7200] = [0.] * 800
        self.write("derived.wav", altered)
        result = inspect_audio(self.root, "derived.wav", preservation={"original": "voice.wav", "edit_ranges": [[.8, .9]]})
        self.assertTrue(result["checks"]["preservation"]["passed"])
        self.assertEqual(result["checks"]["preservation"]["original_sha256"], hashlib.sha256((self.root / "voice.wav").read_bytes()).hexdigest())
        (self.root / "receipt.json").write_text('{}')
        stem = {"role": "source_video", "path": "voice.wav", "receipt": "receipt.json", "sha256": hashlib.sha256((self.root / "voice.wav").read_bytes()).hexdigest(), "included": True}
        self.assertFalse(inspect_audio(self.root, "derived.wav", stems=[stem])["passed"])
        stem["audio_authorized"] = True
        self.assertTrue(inspect_audio(self.root, "derived.wav", stems=[stem])["passed"])
        stem["sha256"] = "wrong"
        self.assertFalse(inspect_audio(self.root, "derived.wav", stems=[stem])["passed"])

    def test_encoded_and_post_master_cues_and_overlap(self):
        self.write("louder.wav", [x*2 for x in self.pcm])
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(self.root / "louder.wav"), "-c:a", "aac", "-b:a", "48k", str(self.root / "encoded.m4a")], check=True, capture_output=True)
        cue = {"id": "fx", "reference": "voice.wav", "candidate": "louder.wav", "start": .1, "end": .8, "activity_required": True, "maximum_onset_delay_seconds": .01}
        result = inspect_audio(self.root, "voice.wav", alignment=[{"start": .2, "end": .4, "text": "word"}], cues=[dict(cue, stage="post_master"), dict(cue, stage="final_encoded", candidate="encoded.m4a")])
        self.assertFalse(result["passed"])
        self.assertEqual(len(result["checks"]["cues"]), 2)
        self.assertEqual(result["checks"]["cues"][1]["candidate_stream"]["codec"], "aac")
        self.assertAlmostEqual(result["checks"]["cues"][0]["narration_overlap_seconds"], .2)
        self.write("silence.wav", [0.]*8000)
        cue["candidate"] = "silence.wav"
        report = inspect_audio(self.root, "voice.wav", cues=[cue])
        self.assertIn("cue fx: expected activity absent", report["deterministic"]["failures"])

    def test_containment_and_symlinks(self):
        for relative in ("../voice.wav", str(self.root / "voice.wav")):
            with self.assertRaises(ValueError):
                contained(self.root, relative)
        (self.root / "escape").symlink_to(self.root.parent)
        self.assertFalse(inspect_audio(self.root, "escape/anything")["passed"])

    def test_integer_pcm_positive_negative_rails_are_reported_symmetrically(self):
        self.write("rails.wav", [32767/32768, -1.] * 4000)
        report = inspect_audio(self.root, "rails.wav")
        hits = report["checks"]["integer_pcm_rail_hits"]
        self.assertEqual(hits["positive"], 4000)
        self.assertEqual(hits["negative"], 4000)
        self.assertEqual(hits["total"], 8000)
        self.assertIn("does not establish", hits["classification"])
        self.assertIn("INTEGER_PCM_RAIL_HITS", [f["code"] for f in report["heuristic_findings"]])

    def test_decode_memory_and_duration_caps(self):
        from unittest.mock import patch
        with patch("videoops.audio_qa._bounded_decode", side_effect=AssertionError("preflight must stop decode")):
            with self.assertRaisesRegex(ValueError, "memory limit"):
                decode(self.root / "voice.wav", max_decoded_bytes=1024)
            with self.assertRaisesRegex(ValueError, "duration"):
                decode(self.root / "voice.wav", max_duration_seconds=.1)
        import sys
        with self.assertRaisesRegex(ValueError, "memory limit"):
            _bounded_decode([sys.executable, "-c", "import sys;sys.stdout.buffer.write(b'x'*1000000)"], 1024)
        with self.assertRaisesRegex(ValueError, "timed out"):
            _bounded_decode([sys.executable, "-c", "import time;time.sleep(2)"], 1024, timeout=.05)

    def test_playlist_rejected_before_decoder(self):
        from unittest.mock import patch
        (self.root / "playlist.m3u8").write_text("#EXTM3U\nfile:///etc/passwd\n")
        with patch("videoops.audio_qa._run", side_effect=AssertionError("must not probe playlist")):
            self.assertFalse(inspect_audio(self.root, "playlist.m3u8")["passed"])

    def test_cli_audio_only(self):
        result = subprocess.run(["python3", "scripts/qa_media.py", str(self.root), "--audio-only", "--video", "voice.wav"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads((self.root / "review/media-qa.json").read_text())
        self.assertTrue(report["passed"])
        self.assertEqual(report["perceptual_review"], "REVIEW_INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
