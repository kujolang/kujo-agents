"""Production media and exact-candidate review owned by Kujo Agents."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def parser():
    root = argparse.ArgumentParser(prog="videoops")
    commands = root.add_subparsers(dest="command", required=True)
    media = commands.add_parser("media").add_subparsers(dest="media_command", required=True)
    for name in ("doctor", "providers", "fingerprint", "generate", "import", "inspect", "authorize", "revoke", "status", "reconcile"):
        item = media.add_parser(name)
        item.add_argument("--workspace", type=Path, required=True)
        if name in ("generate", "import", "fingerprint"): item.add_argument("--request", type=Path, required=True)
        if name == "doctor": item.add_argument("--request", type=Path)
        if name == "authorize": item.add_argument("--authorization", type=Path, required=True)
        if name in ("inspect", "revoke"): item.add_argument("--authorization-id", required=True)
        if name in ("status", "reconcile"): item.add_argument("--request-id", required=True)
        if name == "reconcile": item.add_argument("--disposition", choices=["confirmed-failed", "confirmed-cancelled"], required=True)
        if name in ("inspect", "authorize", "revoke", "reconcile"): item.add_argument("--authorize-local", action="store_true")
    review = commands.add_parser("review").add_subparsers(dest="review_command", required=True)
    for name in ("submit-candidate", "record", "status", "resume", "promote", "render-attempt"):
        item = review.add_parser(name)
        item.add_argument("--workspace", type=Path, required=True)
        if name == "submit-candidate":
            item.add_argument("--candidate", required=True)
            item.add_argument("--render-attempt-id")
            item.add_argument("--mandatory-capabilities", nargs="+", choices=["visual_playback", "audio_listening"], default=["visual_playback", "audio_listening"])
            item.add_argument("--max-defect-cycles", type=int, default=3)
        if name in ("submit-candidate", "render-attempt"):
            item.add_argument("--user-revision", action="store_true")
            item.add_argument("--repair-kind", choices=["technical", "perceptual"])
        if name == "record": item.add_argument("--decision", type=Path, required=True)
        if name == "promote": item.add_argument("--destination", default="output/final.mp4")
        if name in ("record", "promote"): item.add_argument("--authorize-local", action="store_true")
        if name == "render-attempt":
            item.add_argument("--attempt-id", required=True)
            item.add_argument("--outcome", choices=["failed", "succeeded"], required=True)
    return root


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def media_review_main(args):
    from .media_contracts import MediaError, read_json, contained
    from .media import MediaService, fingerprint
    from .review import ReviewService
    try:
        if args.command == "media":
            service = MediaService(args.workspace)
            cmd = args.media_command
            if cmd in ("generate", "import", "fingerprint"):
                request = args.request.resolve(strict=True)
                relative = str(request.relative_to(args.workspace.resolve(strict=True)))
                request_value = read_json(contained(args.workspace, relative, must_exist=True))
                result = {"fingerprint": fingerprint(request_value)} if cmd == "fingerprint" else service.execute(request_value, operation=cmd)
            elif cmd == "doctor" and args.request:
                relative = str(args.request.resolve(strict=True).relative_to(args.workspace.resolve(strict=True)))
                result = service.doctor(read_json(contained(args.workspace, relative, must_exist=True)))
            elif cmd == "authorize":
                relative = str(args.authorization.resolve(strict=True).relative_to(args.workspace.resolve(strict=True)))
                result = service.authorize(read_json(contained(args.workspace, relative, must_exist=True)), local_authorized=args.authorize_local)
            elif cmd == "revoke": result = service.revoke(args.authorization_id, local_authorized=args.authorize_local)
            elif cmd == "inspect": result = service.inspect(args.authorization_id, local_authorized=args.authorize_local)
            elif cmd == "status": result = service.status(args.request_id)
            elif cmd == "reconcile": result = service.reconcile(args.request_id, args.disposition, local_authorized=args.authorize_local)
            else: result = getattr(service, cmd)()
        else:
            service = ReviewService(args.workspace)
            cmd = args.review_command
            if cmd == "submit-candidate": result = service.submit_candidate(args.candidate, render_attempt_id=args.render_attempt_id, user_revision=args.user_revision, repair_kind=args.repair_kind, mandatory_capabilities=args.mandatory_capabilities, max_defect_cycles=args.max_defect_cycles)
            elif cmd == "record":
                relative = str(args.decision.resolve(strict=True).relative_to(args.workspace.resolve(strict=True)))
                result = service.record(read_json(contained(args.workspace, relative, must_exist=True)), local_authorized=args.authorize_local)
            elif cmd == "promote": result = service.promote(args.destination, local_authorized=args.authorize_local)
            elif cmd == "render-attempt": result = service.record_render_attempt(args.attempt_id, outcome=args.outcome, user_revision=args.user_revision, repair_kind=args.repair_kind)
            else: result = getattr(service, cmd)()
        emit(result)
        return 0 if result.get("state") not in ("BLOCKED", "UNSUPPORTED", "FAILED", "UNKNOWN_OUTCOME") else 2
    except Exception as exc:
        # Opaque I/O/provider failures never echo credential values or artifact text.
        emit({"ok": False, "error": exc.code if isinstance(exc, MediaError) else "MEDIA_REVIEW_OPERATION_FAILED"})
        return 1


def main(argv=None):
    return media_review_main(parser().parse_args(argv))

if __name__ == "__main__":
    raise SystemExit(main())
