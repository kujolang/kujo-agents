# Source-aware audio QA

Run the relative commands below from `kujo-agents/videoops/tools`.

`videoops.audio_qa.inspect_audio(workspace, relative_path, **declarations)` and
`python3 scripts/qa_media.py WORKSPACE --video output/candidate.mp4 --audio-config review/audio-input.json`
measure media without changing it. For standalone audio use `--audio-only`.
`--output` must stay inside the workspace. All input file references are relative,
with traversal and symlink escapes rejected. FFmpeg/ffprobe must be installed;
they use a file/pipe protocol allowlist (no remote URLs). Playlists are rejected
before probing; supported binary container families are WAV, FLAC, Ogg, MP3/AAC,
MP4/MOV and WebM/Matroska. Unsupported formats fail explicitly. No provider calls occur. Decoding defaults to a 600-second duration ceiling and
128 MiB of float64 PCM (whichever is smaller). Probe metadata is checked before
decoding, and the decoder pipe is drained with a hard byte cap and 120-second
timeout even if duration metadata is missing or dishonest. `decode()` exposes
explicit `max_duration_seconds` and `max_decoded_bytes` overrides to trusted
Python callers; the CLI uses bounded defaults. Longer inputs must be intentionally
partitioned or measured with a separately reviewed resource policy.
The legacy workspace/video/output script interface remains available; platform
checks use `intake/platform.json`. If present, repository `config/media-quality.json`
retains its output matrix, tolerances and loudness bounds; otherwise no matrix
validation is claimed, and default video loudness bounds are -16..-12 LUFS. This is not a new mixer or generation adapter.

Reports use `kujo-videoops/audio-qa/v1`, with the outer compatibility CLI report
`kujo-videoops/media-qa/v1`. `passed` means deterministic requirements only.
`perceptual.status` is always `REVIEW_INCOMPLETE`: a capable reviewer still checks
pronunciation, actual speech completeness, cut quality and comfort. Heuristic
findings never trim audio and never establish a deterministic failure by themselves.

Example declarations (JSON; omit fields not needed):

```json
{
  "requirements": {
    "sample_rate": 48000,
    "channels": 2,
    "codec": "aac",
    "duration_seconds": 15,
    "duration_tolerance_seconds": 0.05,
    "loudness_range_lufs": [-16, -12],
    "maximum_true_peak_dbtp": -1,
    "maximum_clipped_samples": 0,
    "alignment_required": true,
    "captions_required": true,
    "stems_required": true,
    "heuristic_thresholds": {
      "silence_dbfs": -50,
      "gap_seconds": 0.08,
      "boundary_amplitude": 0.05,
      "alignment_margin": 0.06
    }
  },
  "alignment": [{"start": 0.2, "end": 2.0, "text": "An original phrase."}],
  "captions": "output/captions.srt",
  "stems": [{"role": "voice", "path": "assets/voice.wav", "sha256": "actual hash", "receipt": "assets/voice-receipt.json", "included": true}],
  "cues": [{"id": "transition-1", "reference": "audio/before-master.wav", "candidate": "audio/after-master.wav", "stage": "post_master", "start": 2.0, "end": 2.4, "maximum_peak_increase_db": 0, "maximum_rms_increase_db": 0, "activity_required": true, "maximum_onset_delay_seconds": 0.04}]
}
```

Alignment is a list of nonempty text segments in seconds from the decoded stream
start, monotonic by start and end and bounded by decoded duration. Overlap is
allowed for alignment but not SRT captions. Provider-native character alignment
should be converted into nonzero-duration word/phrase segments by the caller.
Missing alignment is explicit, and only fails when required. Energy before/after
alignment may be valid breaths or consonants; suspicious bursts provide bounded
inspection ranges, not an automatic repair decision. Duplicate detection compares
at most the first 100 isolated energy bursts with equal sample lengths and high
positive cosine similarity. It can flag repeated words or tones and miss time-
stretched fragments; it is evidence for listening, not a speech recognizer.

`checks.levels.clipped_channel_samples` counts decoded floating samples with
absolute amplitude >= 1.0 (per channel). It does not count only frames or infer historical clipping below full scale.
`checks.integer_pcm_rail_hits` separately counts positive and negative integer
quantization rails symmetrically, with codec/bit-depth evidence. Rail hits produce
a heuristic finding; a single maximum sample is not proof of audible distortion.
This evidence is unavailable for lossy/float formats, never fabricated as zero.
`true_peak_dbtp` is FFmpeg loudnorm's oversampled `input_tp`, separately reported
from sample peak. Silence/nonfinite logarithmic values are JSON null, never an
invented zero. Loudness is `input_i`, not normalized output. No normalization is
performed. Multiple audio streams fail rather than quietly ignoring possible
source-video sound.

For a speech derivative, supply `preservation`:

```json
{"original": "assets/original-voice.wav", "edit_ranges": [[2.8, 3.0]], "tolerance": 0.000001, "expected_gain": 1}
```

The original must be a different file. Its SHA-256 is recorded; all samples outside
declared edit ranges are compared. Sample counts, rate and channels must match.
Changing duration requires an explicit timing-map implementation and currently
fails. A known uniform gain may be declared; strict sample comparison is unsuitable
for lossy encoding or arbitrary mastering and must not be passed off as semantic
speech preservation. Preserve the original and rerun this check after any repair.
An edit covering the entire original does not prove preservation and fails.
Optional `requirements.cut_times_seconds` lists internal edit boundaries; jumps
above `requirements.cut_jump_amplitude` (default 0.1 linear amplitude) produce
heuristic `ABRUPT_DECLARED_CUT` findings, never automatic fades or cuts.

Stem roles are `voice`, `music`, `sfx`, `source_video`, each with its own file hash
and existing receipt. Included source-video audio additionally requires
`audio_authorized: true`. This validates declared provenance, not rights approval
or forensic source separation: a final mix cannot prove absence of undeclared
sources from waveform correlation alone. HyperFrames remains responsible for the
actual track graph and composition/mixing.

Use separate cue comparisons for `post_master` and `final_encoded` candidates,
with equal rate/channels and the same bounded time window in both assets. Each
comparison records both actual hashes and stream metadata; the stage label is
a caller declaration, not proof that a WAV has undergone a delivery encode. Both
peak and RMS changes must satisfy thresholds. An increase from silence fails.
These measurements describe the entire window unless stems isolated SFX upstream;
do not attribute a mixed-window rise solely to an effect. `first_activity_seconds`
measures threshold crossing against the cue start; `narration_overlap_seconds`
records union overlap with supplied speech alignment. An absent/late activity
fails only when requested. None of these measurements proves pleasant sound.

Tests: `python3 -m unittest discover -s tests -p test_audio_qa.py -v`.
Synthetic fixtures cover an isolated post-phrase tail, duplicated fragment,
nonzero edit boundary, edits leaking into preserved speech, invalid captions,
clipping, true peak versus sample peak, post-master energy growth, source-video
provenance and cue timing. They do not rely on a private narrator or production.
