#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSE = ROOT / "publishing-house"
PERMISSIONS = {"OBSERVE", "PROPOSE", "ACT"}
SHARED = {
    "README.md",
    "00-agent-map.md",
    "00-permission-model.md",
    "00-publishing-house.md",
    "00-quality-standard.md",
    "00-shared-contracts.md",
    "publishing-house-catalog.json",
}
HEADINGS = [
    "Agent Contract",
    "Use This Agent When",
    "Do Not Use This Agent When",
    "Inputs Expected",
    "Outputs Required",
    "Allowed Tools And Workflows",
    "Workflow",
    "Evidence Requirements",
    "Quality Standard",
    "Handoff Rules",
    "Escalation Rules",
    "Stop Conditions",
    "Anti-Scope",
]


def main() -> int:
    errors: list[str] = []
    for name in sorted(SHARED):
        if not (HOUSE / name).is_file():
            errors.append(f"missing shared contract: {name}")

    catalog_path = HOUSE / "publishing-house-catalog.json"
    if not catalog_path.is_file():
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1

    catalog = json.loads(catalog_path.read_text())
    agents = catalog.get("agents", [])
    if catalog.get("agent_count") != 23 or len(agents) != 23:
        errors.append("catalog must contain exactly 23 agents")
    if catalog.get("independence") != "standalone":
        errors.append("catalog must declare standalone independence")
    if catalog.get("evaluation_fixtures") != "deferred" or catalog.get("tool_inventory") != "deferred":
        errors.append("steps 4 and 5 must remain explicitly deferred")

    expected = {agent["slug"] for agent in agents}
    actual = {path.name for path in HOUSE.iterdir() if path.is_dir()}
    if expected != actual:
        errors.append(
            f"agent directories differ from catalog: missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )

    skill_names: set[str] = set()
    for agent in agents:
        slug = agent["slug"]
        folder = HOUSE / slug
        contract = folder / "AGENT.md"
        skill = folder / "SKILL.md"
        interface = folder / "agents" / "openai.yaml"
        for path in (contract, skill, interface):
            if not path.is_file():
                errors.append(f"{slug}: missing {path.relative_to(folder)}")
        if not contract.is_file() or not skill.is_file():
            continue

        body = contract.read_text()
        skill_body = skill.read_text()
        for heading in HEADINGS:
            if f"## {heading}" not in body:
                errors.append(f"{slug}: missing heading {heading}")
        for phrase in (
            "Maximum permission mode",
            "Independence: Operates inside Publishing House",
            "External team handoffs are optional",
        ):
            if phrase not in body:
                errors.append(f"{slug}: missing contract phrase {phrase}")
        permission = agent.get("maximum_permission")
        if permission not in PERMISSIONS or f"- Maximum permission mode: {permission}." not in body:
            errors.append(f"{slug}: invalid or mismatched maximum permission")

        match = re.search(r"^name:\s*([^\s]+)$", skill_body, re.MULTILINE)
        expected_skill = f"publishing-house-{slug}"
        if not match:
            errors.append(f"{slug}: missing skill frontmatter name")
        elif match.group(1) != expected_skill:
            errors.append(f"{slug}: expected skill {expected_skill}, got {match.group(1)}")
        elif match.group(1) in skill_names:
            errors.append(f"{slug}: duplicate skill name {match.group(1)}")
        else:
            skill_names.add(match.group(1))
        if "Publishing House is standalone" not in skill_body:
            errors.append(f"{slug}: skill does not preserve standalone boundary")
        if "TODO" in body or "TODO" in skill_body:
            errors.append(f"{slug}: unresolved TODO")
        if interface.is_file() and f"$publishing-house-{slug}" not in interface.read_text():
            errors.append(f"{slug}: openai.yaml default prompt does not invoke its skill")

    publishing_ops = next((item for item in agents if item["slug"] == "publishing-operations-director"), None)
    act_roles = [item["slug"] for item in agents if item.get("maximum_permission") == "ACT"]
    if not publishing_ops or act_roles != ["publishing-operations-director"]:
        errors.append(f"Publishing Operations Director must be the only ACT-capable role; got {act_roles}")

    secret_pattern = re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}"
    )
    for path in HOUSE.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".json", ".yaml"}:
            if secret_pattern.search(path.read_text(errors="ignore")):
                errors.append(f"possible secret material: {path.relative_to(ROOT)}")

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "valid": True,
                "publishing_house_agents": len(agents),
                "role_skills": len(skill_names),
                "standalone": True,
                "act_roles": act_roles,
                "evaluation_fixtures": "deferred",
                "tool_inventory": "deferred",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
