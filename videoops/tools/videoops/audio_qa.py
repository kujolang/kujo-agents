"""Source-aware, read-only audio evidence. No mixing, trimming or listening claims.

All times are seconds from the start of the decoded audio stream. PCM comparison
uses sample frames; clipped-sample counts count channel samples, not frames.
"""
from __future__ import annotations

import array
import hashlib
import json
import math
import os
import re
import subprocess
import selectors
import time
import sys
from pathlib import Path
from typing import Any

CONTRACT = "kujo-videoops/audio-qa/v1"


def contained(workspace: Path, relative: str) -> Path:
    root = Path(workspace).resolve()
    path = Path(relative)
    if path.is_absolute() or not relative or ".." in path.parts:
        raise ValueError("media path must be workspace-relative")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("media path escapes workspace")
    if not resolved.is_file():
        raise ValueError("media file does not exist")
    return resolved


def _run(args: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(args, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("audio measurement tool unavailable or timed out") from None
    if result.returncode:
        # Never reflect paths, metadata or arbitrary decoder diagnostics to logs.
        raise ValueError("audio probe or decode failed")
    return result


def _db(value: float) -> float | None:
    return 20 * math.log10(value) if value > 0 else None


def _finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _bounded_decode(args: list[str], maximum_bytes: int, timeout: float = 120) -> bytes:
    """Drain incrementally with a hard decoded-byte ceiling, including bad headers."""
    process = None
    selector = selectors.DefaultSelector()
    data = bytearray()
    deadline = time.monotonic() + timeout
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        selector.register(process.stdout, selectors.EVENT_READ)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not selector.select(remaining):
                raise ValueError("audio decode timed out")
            chunk = os.read(process.stdout.fileno(), min(65536, maximum_bytes + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
            if len(data) > maximum_bytes:
                raise ValueError("decoded audio exceeds memory limit")
        if process.wait(timeout=max(.01, deadline-time.monotonic())):
            raise ValueError("audio decode failed")
        return bytes(data)
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("audio decode unavailable or timed out") from None
    finally:
        selector.close()
        if process is not None:
            if process.poll() is None:
                process.kill()
            process.wait()
            if process.stdout is not None:
                process.stdout.close()


def decode(path: Path, *, max_decoded_bytes: int = 128 * 1024 * 1024, max_duration_seconds: float = 600) -> tuple[array.array, dict]:
    if type(max_decoded_bytes) is not int or max_decoded_bytes <= 0 or _finite(max_duration_seconds) is None or max_duration_seconds <= 0:
        raise ValueError("invalid audio resource limits")
    # Reject manifests/playlists before probing: the file protocol alone would
    # still allow them to reference another local file outside the workspace.
    with path.open("rb") as source:
        header = source.read(16)
    binary_media = (header.startswith((b"RIFF", b"RF64", b"fLaC", b"OggS", b"ID3", b"\x1a\x45\xdf\xa3"))
                    or header[4:8] in (b"ftyp", b"moov", b"mdat", b"wide", b"free")
                    or (len(header) >= 2 and header[0] == 255 and header[1] & 224 == 224))
    if not binary_media:
        raise ValueError("unsupported binary media container; playlists are not allowed")
    # Protocol allowlist prevents playlist input from contacting external URLs.
    info = json.loads(_run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_streams", "-show_format", "-of", "json", str(path)]).stdout)
    stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    if not stream:
        raise ValueError("audio stream missing")
    rate, channels = int(stream["sample_rate"]), int(stream["channels"])
    if not 1 <= channels <= 32 or not 1 <= rate <= 384000:
        raise ValueError("unsupported audio dimensions")
    duration = _finite(stream.get("duration", info.get("format", {}).get("duration")))
    if duration is not None and (duration > max_duration_seconds or duration * rate * channels * 8 > max_decoded_bytes):
        raise ValueError("audio exceeds duration or decoded memory limit")
    data = _bounded_decode(["ffmpeg", "-v", "error", "-xerror", "-protocol_whitelist", "file,pipe", "-i", str(path), "-map", "0:a:0", "-vn", "-f", "f64le", "-acodec", "pcm_f64le", "pipe:1"], min(max_decoded_bytes, int(max_duration_seconds * rate * channels * 8)))
    samples = array.array("d")
    samples.frombytes(data)
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples or len(samples) % channels or any(not math.isfinite(x) for x in samples):
        raise ValueError("invalid decoded PCM")
    metadata = {"sample_rate": rate, "channels": channels, "codec": stream["codec_name"], "duration_seconds": len(samples) / channels / rate,
                "channel_samples": len(samples), "bits_per_raw_sample": int(stream.get("bits_per_raw_sample") or stream.get("bits_per_sample") or 0), "audio_stream_count": sum(s.get("codec_type") == "audio" for s in info["streams"])}
    return samples, metadata


def integer_rail_hits(samples, codec: str, bits: int) -> dict:
    """Integer extrema are symmetric evidence, not proof of audible distortion."""
    signed = codec.startswith("pcm_s")
    unsigned = codec.startswith("pcm_u")
    if not (signed or unsigned) or not 1 <= bits <= 32:
        return {"available": False, "positive": None, "negative": None, "total": None,
                "classification": "integer quantization rails unavailable for this codec"}
    step = 2 ** (1-bits)
    positive = sum(abs(x - (1-step)) < step/4 for x in samples)
    negative = sum(abs(x + 1) < step/4 for x in samples)
    return {"available": True, "positive": positive, "negative": negative, "total": positive + negative,
            "classification": "rail hits; a single full-scale sample does not establish clipping distortion"}


def levels(samples) -> dict:
    peak = max((abs(x) for x in samples), default=0)
    rms = math.sqrt(sum(x * x for x in samples) / len(samples)) if samples else 0
    return {"peak": peak, "peak_dbfs": _db(peak), "rms": rms, "rms_dbfs": _db(rms),
            "clipped_channel_samples": sum(abs(x) >= 1.0 for x in samples)}


def validate_segments(segments: list[dict], duration: float, *, allow_overlap: bool = False) -> list[str]:
    failures = []
    previous_start = previous_end = 0.0
    if not isinstance(segments, list):
        return ["segments must be an array"]
    for index, item in enumerate(segments):
        if not isinstance(item, dict):
            failures.append(f"segment {index} must be an object")
            continue
        start, end = _finite(item.get("start")), _finite(item.get("end"))
        if start is None or end is None or start < 0 or end <= start or end > duration + 1e-6:
            failures.append(f"segment {index} has invalid bounds")
            continue
        if start < previous_start or end < previous_end or (not allow_overlap and start < previous_end):
            failures.append(f"segment {index} is not monotonic")
        if not isinstance(item.get("text"), str) or not item["text"].strip():
            failures.append(f"segment {index} has no text")
        previous_start, previous_end = start, end
    return failures


def parse_srt(text: str) -> list[dict]:
    segments = []
    def stamp(value):
        h, m, s, ms = map(int, re.split(r"[:,]", value))
        if m >= 60 or s >= 60:
            raise ValueError("invalid caption timestamp")
        return h * 3600 + m * 60 + s + ms / 1000
    for block in re.split(r"\n\s*\n", text.strip().replace("\r\n", "\n")):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit():
            raise ValueError("invalid SRT caption block")
        match = re.fullmatch(r"(\d{2,}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2,}:\d{2}:\d{2},\d{3})", lines[1])
        if not match:
            raise ValueError("invalid SRT caption timing")
        segments.append({"start": stamp(match[1]), "end": stamp(match[2]), "text": "\n".join(lines[2:])})
    return segments


def _window(samples, rate, channels, start, end):
    return samples[round(start * rate) * channels:round(end * rate) * channels]


def phrase_findings(samples, rate: int, channels: int, segments: list[dict], *, silence_dbfs: float = -50, gap_seconds: float = .08,
                    boundary_amplitude: float = .05, alignment_margin: float = .06) -> list[dict]:
    """Energy anomalies are review candidates, never permission to remove speech."""
    findings = []
    duration = len(samples) / channels / rate
    size = max(1, round(rate * .01)) * channels
    silent_limit = 10 ** (silence_dbfs / 20)
    active = []
    for begin in range(0, len(samples), size):
        chunk = samples[begin:begin + size]
        if levels(chunk)["rms"] > silent_limit:
            active.append((begin / channels / rate, (begin + len(chunk)) / channels / rate))
    bursts = []
    for start, end in active:
        if bursts and start - bursts[-1][1] < .011:
            bursts[-1][1] = end
        else:
            bursts.append([start, end])
    for i, (start, end) in enumerate(bursts):
        preceding = start - (bursts[i - 1][1] if i else 0)
        aligned = any(start < s["end"] + alignment_margin and end > s["start"] - alignment_margin for s in segments)
        if segments and not aligned and preceding >= gap_seconds:
            findings.append({"code": "UNALIGNED_BURST_AFTER_SILENCE", "range_seconds": [start, end], "preceding_silence_seconds": preceding,
                             "repair_candidate": {"inspect_range_seconds": [max(0, start - alignment_margin), min(duration, end + alignment_margin)], "automatic_trim_allowed": False}})
    # Only physical file boundaries: phrase alignment boundaries are not actual edits.
    for name, frame in (("start", samples[:channels]), ("end", samples[-channels:])):
        if max(map(abs, frame), default=0) > boundary_amplitude:
            findings.append({"code": "ABRUPT_NONZERO_CUT", "boundary": name, "amplitude": max(map(abs, frame))})
    for i, segment in enumerate(segments):
        hit = [b for b in bursts if b[0] < segment["end"] and b[1] > segment["start"]]
        if not hit:
            findings.append({"code": "ALIGNED_PHRASE_WITHOUT_DETECTED_ENERGY", "segment_index": i, "range_seconds": [segment["start"], segment["end"]]})
    # Compare bounded isolated bursts of similar length. Identical room tone or
    # repeated words can legitimately trigger this heuristic; never a hard fail.
    for i, first in enumerate(bursts[:100]):
        a = _window(samples, rate, channels, *first)
        if first[1] - first[0] < .04:
            continue
        for second in bursts[i + 1:100]:
            b = _window(samples, rate, channels, *second)
            if len(a) != len(b):
                continue
            dot = sum(x * y for x, y in zip(a, b))
            energy = math.sqrt(sum(x*x for x in a) * sum(y*y for y in b))
            similarity = dot / energy if energy else 0
            if similarity > .995:
                findings.append({"code": "POTENTIAL_DUPLICATE_FRAGMENT", "ranges_seconds": [first, second], "cosine_similarity": similarity})
    return findings


def compare_preservation(original, derived, rate: int, channels: int, edit_ranges: list[list[float]], *, tolerance: float = 1e-6, expected_gain: float = 1) -> dict:
    """Aligned, equal-length PCM proof outside declared edits; no time warping."""
    if not math.isfinite(tolerance) or tolerance < 0 or not math.isfinite(expected_gain) or expected_gain <= 0:
        raise ValueError("invalid preservation tolerance or gain")
    duration = len(original) / rate / channels
    for bounds in edit_ranges:
        if len(bounds) != 2 or any(_finite(x) is None for x in bounds) or not 0 <= bounds[0] < bounds[1] <= duration:
            raise ValueError("invalid declared edit range")
    if len(original) != len(derived):
        return {"passed": False, "reason": "sample counts differ; explicit time mapping is required", "compared_channel_samples": 0}
    excluded = [(round(start*rate)*channels, round(end*rate)*channels) for start, end in edit_ranges]
    count = changed = 0
    max_error = 0.0
    for i, (a, b) in enumerate(zip(original, derived)):
        if any(start <= i < end for start, end in excluded):
            continue
        count += 1
        error = abs(a * expected_gain - b)
        max_error = max(max_error, error)
        changed += error > tolerance
    return {"passed": count > 0 and changed == 0, "compared_channel_samples": count, "changed_channel_samples": changed, "max_absolute_error": max_error,
            "tolerance": tolerance, "expected_gain": expected_gain, "declared_edit_ranges_seconds": edit_ranges,
            "scope": "sample preservation only; not pronunciation or listening approval"}


def _overlap(start: float, end: float, segments: list[dict]) -> float:
    merged = []
    for segment in segments:
        a, b = max(start, segment["start"]), min(end, segment["end"])
        if b <= a:
            continue
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return sum(b - a for a, b in merged)


def compare_cue(before, after, rate: int, channels: int, start: float, end: float, *, maximum_peak_increase_db: float = 0, maximum_rms_increase_db: float = 0) -> dict:
    if any(_finite(x) is None for x in (start, end, maximum_peak_increase_db, maximum_rms_increase_db)):
        raise ValueError("cue limits must be finite")
    if not 0 <= start < end <= min(len(before), len(after)) / rate / channels:
        raise ValueError("cue window outside comparable audio")
    a, b = levels(_window(before, rate, channels, start, end)), levels(_window(after, rate, channels, start, end))
    def delta(key):
        return b[key] - a[key] if a[key] is not None and b[key] is not None else None
    peak, rms = delta("peak_dbfs"), delta("rms_dbfs")
    # Silence in a reference followed by energy is an increase, not unavailable pass.
    passed = ((peak is None and b["peak"] <= a["peak"]) or (peak is not None and peak <= maximum_peak_increase_db + 1e-6)) and ((rms is None and b["rms"] <= a["rms"]) or (rms is not None and rms <= maximum_rms_increase_db + 1e-6))
    return {"range_seconds": [start, end], "before": a, "after": b, "peak_change_db": peak, "rms_change_db": rms, "passed": passed}


def _validate_requirements(requirements: dict) -> None:
    numbers = {"sample_rate", "channels", "duration_seconds", "duration_tolerance_seconds", "maximum_clipped_samples", "maximum_true_peak_dbtp", "cut_jump_amplitude"}
    for key in numbers & requirements.keys():
        if isinstance(requirements[key], bool) or not isinstance(requirements[key], (float, int)) or _finite(requirements[key]) is None:
            raise ValueError("audio thresholds must be finite numbers")
        if key != "maximum_true_peak_dbtp" and requirements[key] < 0:
            raise ValueError("audio threshold must be nonnegative")
    for key in ("sample_rate", "channels", "maximum_clipped_samples"):
        if key in requirements and int(requirements[key]) != requirements[key]:
            raise ValueError("audio dimensions and sample limits must be integers")
    bounds = requirements.get("loudness_range_lufs")
    if bounds is not None and (not isinstance(bounds, list) or len(bounds) != 2 or any(_finite(x) is None or isinstance(x, bool) or not isinstance(x, (int, float)) for x in bounds) or bounds[0] > bounds[1]):
        raise ValueError("invalid loudness bounds")
    thresholds = requirements.get("heuristic_thresholds", {})
    if not isinstance(thresholds, dict) or set(thresholds) - {"silence_dbfs", "gap_seconds", "boundary_amplitude", "alignment_margin"}:
        raise ValueError("unknown heuristic threshold")
    if any(_finite(x) is None or isinstance(x, bool) or not isinstance(x, (int, float)) for x in thresholds.values()):
        raise ValueError("heuristic thresholds must be finite numbers")
    if any(thresholds.get(x, 0) < 0 for x in ("gap_seconds", "boundary_amplitude", "alignment_margin")):
        raise ValueError("negative heuristic range or amplitude")


def inspect_audio(workspace: Path | str, relative_path: str, *, requirements: dict | None = None, alignment: list[dict] | None = None,
                  captions: str | None = None, preservation: dict | None = None, stems: list[dict] | None = None, cues: list[dict] | None = None) -> dict:
    """Inspect a local asset. Optional declarations are described in docs/audio-qa.md.

    A deterministic PASS never implies perceptual PASS. Files are never modified.
    """
    workspace = Path(workspace)
    requirements = {} if requirements is None else requirements
    report = {"contract": CONTRACT, "asset": relative_path, "deterministic": {"status": "FAIL", "failures": []}, "heuristic_findings": [],
              "perceptual": {"status": "REVIEW_INCOMPLETE", "listening_exercised": False, "required": ["pronunciation", "speech completeness", "audible cuts", "mix comfort"]}, "checks": {}}
    failures, checks = report["deterministic"]["failures"], report["checks"]
    try:
        if not isinstance(requirements, dict) or (preservation is not None and not isinstance(preservation, dict)):
            raise ValueError("requirements and preservation must be objects")
        _validate_requirements(requirements)
        for items in (stems, cues):
            if items is not None and (not isinstance(items, list) or any(not isinstance(item, dict) for item in items)):
                raise ValueError("stems and cues must be arrays of objects")
        path = contained(workspace, relative_path)
        pcm, meta = decode(path)
        report["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        checks["stream"] = meta
        checks["levels"] = levels(pcm)
        checks["integer_pcm_rail_hits"] = integer_rail_hits(pcm, meta["codec"], meta["bits_per_raw_sample"])
        if checks["integer_pcm_rail_hits"]["total"]:
            report["heuristic_findings"].append({"code": "INTEGER_PCM_RAIL_HITS", **checks["integer_pcm_rail_hits"]})
        for key in ("sample_rate", "channels", "codec"):
            if key in requirements and meta[key] != requirements[key]:
                failures.append(f"{key} does not match required value")
        if "duration_seconds" in requirements and abs(meta["duration_seconds"] - requirements["duration_seconds"]) > requirements.get("duration_tolerance_seconds", .05):
            failures.append("duration outside required tolerance")
        if checks["levels"]["clipped_channel_samples"] > requirements.get("maximum_clipped_samples", 0):
            failures.append("clipped channel samples exceed limit")
        if meta["audio_stream_count"] != 1:
            failures.append("unexpected additional audio streams")
        measurement = _run(["ffmpeg", "-hide_banner", "-nostats", "-protocol_whitelist", "file,pipe", "-i", str(path), "-map", "0:a:0", "-af", "loudnorm=I=-14:TP=-1:print_format=json", "-f", "null", "-"])
        match = re.search(rb'\{\s*"input_i".*?\}', measurement.stderr, re.S)
        if not match:
            raise ValueError("loudness and true peak unavailable")
        measured = json.loads(match.group())
        loudness, true_peak = _finite(measured["input_i"]), _finite(measured["input_tp"])
        checks["integrated_loudness_lufs"], checks["true_peak_dbtp"] = loudness, true_peak
        checks["true_peak_method"] = "FFmpeg loudnorm input_tp (oversampled measurement)"
        if "loudness_range_lufs" in requirements and (loudness is None or not requirements["loudness_range_lufs"][0] <= loudness <= requirements["loudness_range_lufs"][1]):
            failures.append("integrated loudness outside required range")
        if true_peak is not None and true_peak > requirements.get("maximum_true_peak_dbtp", 0):
            failures.append("true peak exceeds required ceiling")
        checks["alignment"] = "unavailable" if alignment is None else "supplied"
        if requirements.get("alignment_required") and not alignment:
            failures.append("required alignment unavailable")
        if alignment is not None:
            alignment_errors = validate_segments(alignment, meta["duration_seconds"], allow_overlap=True)
            failures.extend("alignment: " + x for x in alignment_errors)
        else:
            alignment_errors = []
        if captions:
            caption_segments = parse_srt(contained(workspace, captions).read_text())
            failures.extend("captions: " + x for x in validate_segments(caption_segments, meta["duration_seconds"]))
            checks["caption_count"] = len(caption_segments)
        elif requirements.get("captions_required"):
            failures.append("required captions unavailable")
        if not alignment_errors:
            report["heuristic_findings"] += phrase_findings(pcm, meta["sample_rate"], meta["channels"], alignment or [], **requirements.get("heuristic_thresholds", {}))
        for cut in requirements.get("cut_times_seconds", []):
            if _finite(cut) is None or not 0 < cut < meta["duration_seconds"]:
                raise ValueError("invalid declared cut time")
            frame = round(cut * meta["sample_rate"])
            before = pcm[(frame-1)*meta["channels"]:frame*meta["channels"]]
            after = pcm[frame*meta["channels"]:(frame+1)*meta["channels"]]
            jump = max((abs(a-b) for a, b in zip(before, after)), default=0)
            if jump > requirements.get("cut_jump_amplitude", .1):
                report["heuristic_findings"].append({"code": "ABRUPT_DECLARED_CUT", "time_seconds": cut, "maximum_channel_jump": jump, "automatic_trim_allowed": False})
        if preservation:
            source = contained(workspace, preservation["original"])
            if source == path:
                raise ValueError("preserved original and derivative must be different files")
            original, original_meta = decode(source)
            if (meta["sample_rate"], meta["channels"]) != (original_meta["sample_rate"], original_meta["channels"]):
                raise ValueError("preservation requires equal sample rate and channels")
            checks["preservation"] = compare_preservation(original, pcm, meta["sample_rate"], meta["channels"], preservation.get("edit_ranges", []), tolerance=preservation.get("tolerance", 1e-6), expected_gain=preservation.get("expected_gain", 1))
            checks["preservation"]["original_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
            if not checks["preservation"]["passed"]:
                failures.append("speech samples changed outside declared edits")
        checks["stems"] = []
        if requirements.get("stems_required") and not stems:
            failures.append("required stem provenance unavailable")
        for stem in stems or []:
            if stem.get("role") not in ("voice", "music", "sfx", "source_video"):
                raise ValueError("unknown stem role")
            stem_path = contained(workspace, stem["path"])
            actual_hash = hashlib.sha256(stem_path.read_bytes()).hexdigest()
            if stem.get("sha256") != actual_hash or not stem.get("receipt"):
                failures.append("stem provenance hash or receipt missing/mismatched")
            else:
                contained(workspace, stem["receipt"])
            if stem["role"] == "source_video" and stem.get("included", True) and not stem.get("audio_authorized", False):
                failures.append("unauthorized source-video audio declared in mix")
            checks["stems"].append({"role": stem["role"], "path": stem["path"], "sha256": actual_hash, "included": bool(stem.get("included", True))})
        checks["stem_provenance_scope"] = "declared traceability only; cannot prove a mixed waveform excludes undeclared sources"
        checks["cues"] = []
        for cue in cues or []:
            before_path = contained(workspace, cue["reference"])
            after_path = contained(workspace, cue.get("candidate", relative_path))
            before, before_meta = decode(before_path)
            after, after_meta = decode(after_path)
            if (before_meta["sample_rate"], before_meta["channels"]) != (after_meta["sample_rate"], after_meta["channels"]):
                raise ValueError("cue comparison requires equal sample rate and channels")
            result = compare_cue(before, after, before_meta["sample_rate"], before_meta["channels"], cue["start"], cue["end"], maximum_peak_increase_db=cue.get("maximum_peak_increase_db", 0), maximum_rms_increase_db=cue.get("maximum_rms_increase_db", 0))
            result.update({"reference_sha256": hashlib.sha256(before_path.read_bytes()).hexdigest(), "candidate_sha256": hashlib.sha256(after_path.read_bytes()).hexdigest(),
                           "reference_stream": before_meta, "candidate_stream": after_meta, "id": cue["id"], "stage": cue.get("stage", "final_encoded"), "scope": cue.get("scope", "mixed-window; energy not attributable to SFX alone"),
                           "narration_overlap_seconds": _overlap(cue["start"], cue["end"], alignment or []) if not alignment_errors else None})
            # Threshold activity shows synchronization evidence, not which source caused it.
            window = _window(after, after_meta["sample_rate"], after_meta["channels"], cue["start"], cue["end"])
            threshold = 10 ** (cue.get("activity_dbfs", -45) / 20)
            active = [i // after_meta["channels"] for i, value in enumerate(window) if abs(value) > threshold]
            result["first_activity_seconds"] = cue["start"] + min(active) / after_meta["sample_rate"] if active else None
            if cue.get("activity_required") and not active:
                failures.append(f"cue {cue['id']}: expected activity absent")
            if active and "maximum_onset_delay_seconds" in cue and result["first_activity_seconds"] - cue["start"] > cue["maximum_onset_delay_seconds"]:
                failures.append(f"cue {cue['id']}: activity onset late")
            checks["cues"].append(result)
            if not result["passed"]:
                failures.append(f"cue {cue['id']}: peak/RMS increase exceeds declared limit")
    except (ValueError, KeyError, TypeError, OverflowError, json.JSONDecodeError) as exc:
        # Static diagnostics only; no raw ffmpeg/provider output.
        failures.append(str(exc) if isinstance(exc, ValueError) and not isinstance(exc, json.JSONDecodeError) else "invalid audio QA declaration")
    report["deterministic"]["status"] = "PASS" if not failures else "FAIL"
    report["passed"] = not failures
    return report
