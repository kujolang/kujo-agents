#!/usr/bin/env python3
"""Render provider-specific, credential-free runtime descriptors."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def manifests() -> list[tuple[Path, dict]]:
    registry = json.loads((ROOT / "agent-registry.json").read_text())
    result = []
    for entry in registry["agents"]:
        path = ROOT / entry["path"] / "manifest.json"
        result.append((path, json.loads(path.read_text())))
    return result


def hermes(out: Path) -> None:
    for path, manifest in manifests():
        folder = out / manifest["id"]
        folder.mkdir(parents=True, exist_ok=True)
        contract = path.parent
        soul = f"""# {manifest['name']}\n\nYou are the Kujo {manifest['name']} agent.\n\nRead and follow the canonical role contract at `{manifest['contract']['agent']}` and the invocation skill at `{manifest['contract']['skill']}`.\n\nRuntime identity: `{manifest['id']}`\nPermission ceiling: `{manifest['permissions']['maximum']}`\nPermission enforcement: external runtime adapter; prompts do not grant authority.\n\nRequired capabilities: {', '.join(manifest['capabilities']['required']) or 'none'}\nRecommended capabilities: {', '.join(manifest['capabilities']['recommended']) or 'none'}\n\nAlways preserve evidence, handoffs, stop conditions, and approval boundaries from the canonical contract.\n"""
        (folder / "SOUL.md").write_text(soul)
        (folder / "profile.json").write_text(json.dumps({"schema": "kujo.hermes.profile/v1", "agent_id": manifest["id"], "name": manifest["name"], "contract_root": str(contract.relative_to(ROOT)), "permission_ceiling": manifest["permissions"]["maximum"], "model_tier": manifest["classification"]["model_tier"], "enabled_adapters": ["mcp", "generic"]}, indent=2) + "\n")
        (folder / "config.yaml.example").write_text(f"# Credential-free Hermes example for {manifest['id']}\nmodel:\n  provider: custom\n  default: YOUR_MODEL\n# Configure provider credentials outside this repository.\nagent:\n  permission_ceiling: {manifest['permissions']['maximum']}\n")


def paperclip(out: Path) -> None:
    agents = []
    for path, manifest in manifests():
        agents.append({"agent_id": manifest["id"], "display_name": manifest["name"], "contract_root": str(path.parent.relative_to(ROOT)), "prompt_files": [manifest["contract"]["agent"], manifest["contract"]["skill"]], "permission_ceiling": manifest["permissions"]["maximum"], "required_capabilities": manifest["capabilities"]["required"], "heartbeat": {"context": "issue and handoff context", "must_preserve": ["status", "comments", "artifacts", "approvals", "receipts"], "credential_env": ["PAPERCLIP_API_URL", "PAPERCLIP_API_KEY", "PAPERCLIP_AGENT_ID", "PAPERCLIP_COMPANY_ID", "PAPERCLIP_RUN_ID"]}})
    out.mkdir(parents=True, exist_ok=True)
    (out / "agents.json").write_text(json.dumps({"schema": "kujo.paperclip.registry/v1", "credential_policy": "runtime-only", "agents": agents}, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["hermes", "paperclip"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.target == "hermes": hermes(args.output)
    else: paperclip(args.output)
    print(f"rendered {args.target} adapters to {args.output}")


if __name__ == "__main__": main()
