#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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
    "00-tool-workflow-map.md",
    "publishing-house-catalog.json",
}
EVALS = HOUSE / "evals"
EVAL_REQUIRED = {
    "README.md",
    "eval.json",
    "evaluation-manifest.json",
    "judge-output.schema.json",
    "judge-prompt.md",
    "quality-rubric.json",
}
DIMENSIONS = {
    "consequence",
    "distinctiveness",
    "insight",
    "defensibility",
    "craft",
    "brand_integrity",
    "format_fidelity",
    "strategic_purpose",
}
RATINGS = {"EXCEPTIONAL", "STRONG", "ADEQUATE", "WEAK", "FAILED", "UNVERIFIED"}
CLASSIFICATIONS = {"PREMIUM", "STRONG_NOT_PREMIUM", "COMPETENT_GENERIC", "FAILED"}
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
    if catalog.get("evaluation_fixtures") != "calibration":
        errors.append("catalog must mark evaluation fixtures as calibration")
    expected_tools = {"storydesk", "dossier", "galleypack", "bluepencil", "versionseal", "presswire", "readersignal", "assetworks"}
    if set(catalog.get("tool_inventory", [])) != expected_tools:
        errors.append("Publishing House tool inventory must contain the eight canonical tools")
    expected_workflows = {"house-governance", "daily-desk", "commissioning", "evidence-dossier", "primary-piece", "asset-production", "editorial-review", "adaptation", "format-production", "approval-publication", "post-publication"}
    if set(catalog.get("workflow_inventory", [])) != expected_workflows:
        errors.append("Publishing House workflow inventory must contain the eleven lifecycle workflows")

    expected = {agent["slug"] for agent in agents}
    actual = {
        path.name
        for path in HOUSE.iterdir()
        if path.is_dir() and (path / "AGENT.md").is_file()
    }
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
        manifest = folder / "manifest.json"
        input_schema = folder / "input.schema.json"
        output_schema = folder / "output.schema.json"
        for path in (contract, skill, interface, manifest, input_schema, output_schema):
            if not path.is_file():
                errors.append(f"{slug}: missing {path.relative_to(folder)}")
        if not contract.is_file() or not skill.is_file():
            continue
        permission = agent.get("maximum_permission")
        if manifest.is_file():
            try:
                manifest_data = json.loads(manifest.read_text())
                if manifest_data.get("id") != f"publishing-house.{slug}": errors.append(f"{slug}: manifest id mismatch")
                if manifest_data.get("classification", {}).get("package") != "publishing-house": errors.append(f"{slug}: manifest package mismatch")
                if manifest_data.get("permissions", {}).get("maximum") != permission: errors.append(f"{slug}: manifest permission mismatch")
            except json.JSONDecodeError as exc:
                errors.append(f"{slug}: invalid manifest JSON: {exc}")

        body = contract.read_text()
        skill_body = skill.read_text()
        for heading in HEADINGS:
            if f"## {heading}" not in body:
                errors.append(f"{slug}: missing heading {heading}")
        for phrase in (
            "Maximum permission mode",
            "Independence: Operates inside Publishing House",
            "External team handoffs are optional",
            "Canonical bindings: resolve this role in `../00-tool-workflow-map.md`",
        ):
            if phrase not in body:
                errors.append(f"{slug}: missing contract phrase {phrase}")
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

    validate_evaluations(errors, expected)

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
                "evaluation_fixtures": "calibration",
                "evaluation_cases": 18,
                "evaluation_role_coverage": len(expected),
                "tool_inventory": sorted(expected_tools),
                "workflow_inventory": sorted(expected_workflows),
            },
            indent=2,
        )
    )
    return 0


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path.relative_to(ROOT)}")
        return None
    return value


def validate_evaluations(errors: list[str], agent_slugs: set[str]) -> None:
    for name in sorted(EVAL_REQUIRED):
        if not (EVALS / name).is_file():
            errors.append(f"missing evaluation contract: {name}")
    cases_dir = EVALS / "cases"
    expected_dir = EVALS / "expected"
    if not cases_dir.is_dir() or not expected_dir.is_dir():
        errors.append("evaluation corpus requires cases/ and expected/ directories")
        return

    rubric = load_json(EVALS / "quality-rubric.json", errors)
    manifest = load_json(EVALS / "evaluation-manifest.json", errors)
    schema = load_json(EVALS / "judge-output.schema.json", errors)
    suite = load_json(EVALS / "eval.json", errors)
    if not all((rubric, manifest, schema, suite)):
        return
    if rubric.get("schema_version") != "publishing-house-quality-rubric-v1":
        errors.append("evaluation rubric schema version mismatch")
    if set(rubric.get("dimensions", {})) != DIMENSIONS:
        errors.append("evaluation rubric must define exactly the eight quality dimensions")
    if set(rubric.get("ratings", [])) != RATINGS:
        errors.append("evaluation rubric rating language mismatch")
    if set(rubric.get("classifications", [])) != CLASSIFICATIONS:
        errors.append("evaluation rubric classifications mismatch")
    if "Do not average" not in rubric.get("no_average_rule", ""):
        errors.append("evaluation rubric must preserve the no-average blocking rule")
    if schema.get("title") != "Publishing House Blind Quality Judgment":
        errors.append("judge output schema identity mismatch")
    if suite.get("name") != "publishing-house-quality-calibration":
        errors.append("Kujo Eval suite identity mismatch")

    entries = manifest.get("cases", [])
    if manifest.get("schema_version") != "publishing-house-evaluation-manifest-v1":
        errors.append("evaluation manifest schema version mismatch")
    if manifest.get("status") != "calibration":
        errors.append("evaluation manifest must remain explicitly in calibration")
    if manifest.get("blind_labels") != ["A", "B"]:
        errors.append("evaluation manifest must use blind labels A and B")
    if set(manifest.get("dimensions", [])) != DIMENSIONS:
        errors.append("evaluation manifest dimension coverage mismatch")
    if set(manifest.get("role_coverage", [])) != agent_slugs:
        errors.append("evaluation manifest must cover all 23 Publishing House roles")
    if manifest.get("case_count") != len(entries) or len(entries) != 18:
        errors.append("evaluation manifest must contain exactly 18 cases")

    manifest_ids: set[str] = set()
    winners: set[str] = set()
    fixture_names: set[str] = set()
    expected_names: set[str] = set()
    covered_roles: set[str] = set()
    for entry in entries:
        case_id = entry.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            errors.append("evaluation entry missing case_id")
            continue
        if case_id in manifest_ids:
            errors.append(f"duplicate evaluation case: {case_id}")
        manifest_ids.add(case_id)
        roles = set(entry.get("roles_under_test", []))
        if not roles or not roles <= agent_slugs:
            errors.append(f"{case_id}: invalid roles_under_test")
        covered_roles.update(roles)

        fixture_rel = entry.get("fixture")
        expected_rel = entry.get("expected")
        if fixture_rel != f"cases/{case_id}.json" or expected_rel != f"expected/{case_id}.json":
            errors.append(f"{case_id}: fixture paths must be canonical")
            continue
        fixture_names.add(Path(fixture_rel).name)
        expected_names.add(Path(expected_rel).name)
        fixture_path = EVALS / fixture_rel
        expected_path = EVALS / expected_rel
        if not fixture_path.is_file() or not expected_path.is_file():
            errors.append(f"{case_id}: fixture or expected judgment missing")
            continue

        digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
        if entry.get("fixture_sha256") != digest:
            errors.append(f"{case_id}: manifest fixture checksum mismatch")
        fixture = load_json(fixture_path, errors)
        judgment = load_json(expected_path, errors)
        if not fixture or not judgment:
            continue
        if fixture.get("schema_version") != "publishing-house-blind-pair-v1":
            errors.append(f"{case_id}: fixture schema version mismatch")
        if fixture.get("case_id") != case_id or judgment.get("case_id") != case_id:
            errors.append(f"{case_id}: case identifier mismatch")
        if set(fixture.get("roles_under_test", [])) != roles:
            errors.append(f"{case_id}: fixture role coverage differs from manifest")
        candidates = fixture.get("candidates", {})
        if set(candidates) != {"A", "B"}:
            errors.append(f"{case_id}: fixture must contain only blind candidates A and B")
        else:
            for label, candidate in candidates.items():
                content = candidate.get("content", "") if isinstance(candidate, dict) else ""
                if not isinstance(content, str) or len(content.strip()) < 80:
                    errors.append(f"{case_id}: candidate {label} is too short for calibration")
        if judgment.get("schema_version") != "publishing-house-expected-judgment-v1":
            errors.append(f"{case_id}: expected judgment schema version mismatch")
        if judgment.get("fixture_sha256") != digest:
            errors.append(f"{case_id}: expected judgment checksum mismatch")
        winner = judgment.get("expected_winner")
        if winner not in {"A", "B"}:
            errors.append(f"{case_id}: expected winner must be A or B")
        else:
            winners.add(winner)
        classifications = judgment.get("expected_classification", {})
        if set(classifications) != {"A", "B"} or not set(classifications.values()) <= CLASSIFICATIONS:
            errors.append(f"{case_id}: expected classifications are incomplete or invalid")
        decisive = set(judgment.get("decisive_dimensions", []))
        if len(decisive) < 2 or not decisive <= DIMENSIONS:
            errors.append(f"{case_id}: requires at least two valid decisive dimensions")
        ratings = judgment.get("expected_ratings", {})
        for label in ("A", "B"):
            candidate_ratings = ratings.get(label, {})
            if set(candidate_ratings) != DIMENSIONS or not set(candidate_ratings.values()) <= RATINGS:
                errors.append(f"{case_id}: {label} must have all eight valid expected ratings")
        loser = "B" if winner == "A" else "A"
        generic_signals = judgment.get("generic_signals", {}).get(loser, [])
        if classifications.get(loser) == "COMPETENT_GENERIC" and len(generic_signals) < 3:
            errors.append(f"{case_id}: generic loser requires at least three concrete signals")
        blockers = judgment.get("blocking_failures", {})
        if set(blockers) != {"A", "B"}:
            errors.append(f"{case_id}: blocking-failure records must cover A and B")
        if len(judgment.get("rationale", "").strip()) < 80:
            errors.append(f"{case_id}: expected rationale is too short")

    actual_fixtures = {path.name for path in cases_dir.glob("*.json")}
    actual_expected = {path.name for path in expected_dir.glob("*.json")}
    if fixture_names != actual_fixtures:
        errors.append("case files differ from evaluation manifest")
    if expected_names != actual_expected:
        errors.append("expected judgment files differ from evaluation manifest")
    if covered_roles != agent_slugs:
        errors.append("evaluation case assignments do not cover all Publishing House roles")
    if winners != {"A", "B"}:
        errors.append("blind corpus winner placement must include both A and B")


if __name__ == "__main__":
    raise SystemExit(main())
