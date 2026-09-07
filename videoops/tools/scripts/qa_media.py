#!/usr/bin/env python3
"""Read-only output-profile and source-aware audio QA; never audiovisual approval."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from videoops.audio_qa import contained, inspect_audio


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--video", default="output/final.mp4")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--audio-config", help="Workspace-relative JSON containing inspect_audio keyword declarations")
    parser.add_argument("--audio-only", action="store_true")
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    output = args.output or workspace / "review" / "media-qa.json"
    if not output.is_absolute():
        output = workspace / output
    if not output.resolve().is_relative_to(workspace):
        parser.error("output must remain inside workspace")
    failures, checks = [], {}
    try:
        candidate = contained(workspace, args.video)
        config = json.loads(contained(workspace, args.audio_config).read_text()) if args.audio_config else {}
        audio_report = None
        if args.audio_only:
            audio_report = inspect_audio(workspace, args.video, **config)
        else:
            platform = json.loads(contained(workspace, "intake/platform.json").read_text())
            quality_path = ROOT / "config/media-quality.json"
            quality = json.loads(quality_path.read_text()) if quality_path.is_file() else {}
            supported = quality.get("supported_outputs")
            checks["supported_output_profile"] = "not_configured"
            if supported is not None:
                matched = any(item["aspect_ratio"] == platform["aspect_ratio"] and item["width"] == platform["width"] and item["height"] == platform["height"] and platform["fps"] in item["fps"] for item in supported)
                checks["supported_output_profile"] = matched
                if not matched:
                    failures.append("platform output profile is not in the tested compatibility matrix")
            probe = subprocess.run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-show_streams", "-show_format", "-of", "json", str(candidate)], capture_output=True, timeout=120)
            if probe.returncode:
                raise ValueError("ffprobe failed")
            raw = json.loads(probe.stdout)
            visual = next((s for s in raw["streams"] if s.get("codec_type") == "video"), None)
            if not visual:
                failures.append("video stream missing")
            else:
                num, den = map(int, visual["r_frame_rate"].split("/"))
                fps = num / den if den else 0
                checks.update({"width": visual["width"], "height": visual["height"], "fps": fps, "video_codec": visual["codec_name"]})
                if any(visual[key] != platform[key] for key in ("width", "height")):
                    failures.append("render dimensions do not match platform contract")
                if abs(fps - platform["fps"]) > platform.get("fps_tolerance", quality.get("fps_tolerance", .01)):
                    failures.append("render FPS does not match platform contract")
                if platform.get("video_codec") and platform["video_codec"] != visual["codec_name"]:
                    failures.append("video codec does not match platform contract")
            duration = float(raw["format"].get("duration", 0))
            expected = platform.get("render_duration_seconds", platform.get("fixture_duration_seconds", platform["target_duration_seconds"]))
            checks["duration_seconds"] = duration
            if abs(duration - expected) > platform.get("duration_tolerance_seconds", quality.get("duration_tolerance_seconds", .1)):
                failures.append("render duration outside platform tolerance")
            audio = next((s for s in raw["streams"] if s.get("codec_type") == "audio"), None)
            checks["audio_present"] = bool(audio)
            if audio:
                required = config.setdefault("requirements", {})
                if platform.get("audio_codec"):
                    required.setdefault("codec", platform["audio_codec"])
                loudness = quality.get("integrated_loudness_lufs", {"minimum": -16, "maximum": -12})
                required.setdefault("loudness_range_lufs", [loudness["minimum"], loudness["maximum"]])
                required.setdefault("captions_required", platform.get("captions") == "sidecar")
                if (workspace / "output/captions.srt").is_file():
                    config.setdefault("captions", "output/captions.srt")
                audio_report = inspect_audio(workspace, args.video, **config)
            elif platform.get("audio_required"):
                failures.append("required audio stream missing")
        if audio_report:
            checks["audio"] = audio_report
            failures.extend(audio_report["deterministic"]["failures"])
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired):
        failures.append("invalid or unavailable media/configuration")
    report = {"contract": "kujo-videoops/media-qa/v1", "passed": not failures, "video": args.video, "checks": checks, "failures": failures,
              "perceptual_review": "REVIEW_INCOMPLETE", "listening_exercised": False}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
