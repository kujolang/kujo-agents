#!/usr/bin/env python3
"""Validate the provider-neutral agent package layer."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {"chain-of-command": 28, "webops": 28, "publishing-house": 23, "videoops": 6}
PERMS = {"OBSERVE": 0, "PROPOSE": 1, "ACT": 2}


def main() -> int:
    errors: list[str] = []
    registry_path = ROOT / "agent-registry.json"
    if not registry_path.is_file():
        errors.append("missing agent-registry.json")
        registry = {}
    else:
        registry = json.loads(registry_path.read_text())
    if registry.get("agent_count") != sum(PACKAGES.values()):
        errors.append(f"registry agent_count does not equal {sum(PACKAGES.values())}")
    ids: set[str] = set()
    for package, expected in PACKAGES.items():
        folders = [path for path in (ROOT / package).iterdir() if path.is_dir() and (path / "AGENT.md").is_file()]
        if len(folders) != expected:
            errors.append(f"{package}: expected {expected} role directories, found {len(folders)}")
        for folder in folders:
            paths = [folder / name for name in ("AGENT.md", "SKILL.md", "manifest.json", "input.schema.json", "output.schema.json")]
            for path in paths:
                if not path.is_file(): errors.append(f"{folder.name}: missing {path.name}")
            if not (folder / "manifest.json").is_file(): continue
            try: manifest = json.loads((folder / "manifest.json").read_text())
            except json.JSONDecodeError as exc:
                errors.append(f"{folder.name}: invalid manifest JSON: {exc}"); continue
            required = {"schema", "id", "name", "version", "contract", "classification", "permissions", "capabilities", "inputs", "outputs", "handoff", "stop_conditions", "adapters"}
            missing = required - set(manifest)
            if missing: errors.append(f"{folder.name}: manifest missing {sorted(missing)}")
            agent_id = manifest.get("id")
            if agent_id in ids: errors.append(f"duplicate agent id: {agent_id}")
            ids.add(agent_id)
            if manifest.get("schema") != "kujo.agent.manifest/v1": errors.append(f"{folder.name}: manifest schema mismatch")
            perms = manifest.get("permissions", {})
            if perms.get("minimum") not in PERMS or perms.get("maximum") not in PERMS or PERMS.get(perms.get("minimum"), 99) > PERMS.get(perms.get("maximum"), -1): errors.append(f"{folder.name}: invalid permission range")
            if perms.get("enforcement") != "runtime-adapter": errors.append(f"{folder.name}: permission enforcement must be runtime-adapter")
            if manifest.get("contract") != {"agent": "AGENT.md", "skill": "SKILL.md"}: errors.append(f"{folder.name}: contract paths mismatch")
            for schema_name in ("input.schema.json", "output.schema.json"):
                try: json.loads((folder / schema_name).read_text())
                except (OSError, json.JSONDecodeError) as exc: errors.append(f"{folder.name}: invalid {schema_name}: {exc}")
    if len(ids) != sum(PACKAGES.values()): errors.append(f"expected {sum(PACKAGES.values())} unique agent ids, found {len(ids)}")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2)); return 1
    print(json.dumps({"valid": True, "agents": len(ids), "packages": PACKAGES}, indent=2)); return 0


if __name__ == "__main__": sys.exit(main())
