#!/usr/bin/env python3
"""Generate provider-neutral manifests and I/O schemas for every Kujo role."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
HANDOFF_FIELDS = ["assignment", "current_owner", "next_owner", "goal", "scope", "evidence", "decisions", "unresolved_questions", "allowed_next_actions", "stop_condition"]
CHAIN_TOOLS = ["Spec", "Dispatch", "RunLedger", "ShipCheck", "Concord", "Relay", "Tribunal", "CaseFile", "Scent", "Muzzle", "Scout", "Fence", "Eval", "PatchBrief", "ChangeBucket", "Lens", "SSG", "SiteKit", "Kujo Docs", "MCP", "Watchdog", "Agents SDK", "AI SDK", "RAG", "Capsule", "PackWrite", "Redact", "Workcell", "Kennel", "Howl", "Kujo Doctor"]


def bullets(body: str, heading: str) -> list[dict[str, str]]:
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    if not match:
        return []
    result = []
    for line in match.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            text = line[2:].strip()
            name, _, description = text.partition(":")
            name = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
            result.append({"name": name or "item", "description": (description.strip() or text)})
    return result


def first(body: str, pattern: str, default: str = "") -> str:
    match = re.search(pattern, body, re.M)
    return match.group(1).strip() if match else default


def yaml_safe(value: str) -> str:
    return value.replace("\n", " ").replace('"', '\\"')


def chain_agents() -> list[dict]:
    layers = {}
    text = (ROOT / "chain-of-command/00-chain-of-command.md").read_text()
    current = ""
    for line in text.splitlines():
        match = re.match(r"## (.+) Layer", line)
        if match:
            current = match.group(1).lower()
        match = re.match(r"- `([^`]+)`:", line)
        if match:
            layers[match.group(1)] = current
    result = []
    for folder in sorted((ROOT / "chain-of-command").iterdir()):
        if not folder.is_dir() or folder.name == "00-docs":
            continue
        body = (folder / "AGENT.md").read_text()
        name = first(body, r"^- Agent name:\s*(.+)$", folder.name.replace("-", " ").title())
        tier = first(body, r"^- Best model tier:\s*(.+)$", "standard")
        allowed = re.search(r"^## Allowed Tools And Workflows\n(.*?)(?=^## |\Z)", body, re.M | re.S)
        tool_text = allowed.group(1) if allowed else ""
        tools = [tool for tool in CHAIN_TOOLS if tool in tool_text]
        result.append({"package": "chain-of-command", "slug": folder.name, "id": f"chain.{folder.name}", "name": name, "layer": layers.get(folder.name, "unspecified"), "model_tier": tier, "minimum": "OBSERVE", "maximum": "PROPOSE", "capabilities": {"required": [], "recommended": [], "optional": []}, "tools": {"allowed": tools}, "workflows": []})
    return result


def catalog_agents(package: str, catalog_name: str) -> list[dict]:
    catalog = json.loads((ROOT / package / catalog_name).read_text())
    result = []
    for item in catalog["agents"]:
        result.append({
            "package": package, "slug": item["slug"], "id": f"{package}.{item['slug']}", "name": item.get("name") or item.get("agent"),
            "layer": item.get("category") or item.get("desk", "unspecified"), "category": item.get("category"), "desk": item.get("desk"),
            "model_tier": item.get("model_tier", "standard"), "minimum": item.get("permission_min", "OBSERVE"),
            "maximum": item.get("permission_max", item.get("maximum_permission", "PROPOSE")),
            "capabilities": {"required": item.get("required_capabilities", []), "recommended": item.get("recommended_capabilities", []), "optional": item.get("optional_capabilities", [])},
            "tools": {"primary": item.get("primary_tools", []), "secondary": item.get("secondary_tools", [])}, "workflows": item.get("recommended_workflows", [])
        })
    return result


def publishing_tools() -> dict[str, dict[str, list[str]]]:
    """Read the reviewed role-binding table instead of duplicating it in manifests."""
    text = (ROOT / "publishing-house/00-tool-workflow-map.md").read_text()
    result: dict[str, dict[str, list[str]]] = {}
    for line in text.splitlines():
        if not line.startswith("|") or line.count("|") < 3 or line.startswith("| Role") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3:
            continue
        role, tools, workflows = cells
        slug = re.sub(r"[^a-z0-9]+", "-", role.lower()).strip("-")
        result[slug] = {"primary": [x.strip() for x in tools.split(",") if x.strip()], "workflows": [x.strip().lower().replace(" ", "-") for x in workflows.split(",") if x.strip()]}
    return result


def write_role(item: dict) -> None:
    folder = ROOT / item["package"] / item["slug"]
    body = (folder / "AGENT.md").read_text()
    inputs = bullets(body, "Inputs Expected")
    outputs = bullets(body, "Outputs Required")
    if not inputs:
        inputs = [{"name": "assignment", "description": "The bounded assignment and its constraints."}]
    if not outputs:
        outputs = [{"name": "result", "description": "The role's contract-defined result and evidence."}]
    stop = bullets(body, "Stop Conditions")
    manifest = {
        "schema": "kujo.agent.manifest/v1", "id": item["id"], "name": item["name"], "version": VERSION,
        "contract": {"agent": "AGENT.md", "skill": "SKILL.md"},
        "classification": {"package": item["package"], "layer": item["layer"], "model_tier": item["model_tier"]},
        "permissions": {"minimum": item["minimum"], "maximum": item["maximum"], "enforcement": "runtime-adapter"},
        "capabilities": item["capabilities"], "tools": item["tools"], "workflows": item["workflows"],
        "inputs": inputs, "outputs": outputs,
        "handoff": {"schema": "kujo.handoff/v1", "required_fields": HANDOFF_FIELDS},
        "stop_conditions": [x["description"] for x in stop] or ["The contract-defined result is complete.", "Required evidence or authority is missing."],
        "adapters": ["hermes", "paperclip", "openai", "mcp", "generic"]
    }
    if item.get("category"): manifest["classification"]["category"] = item["category"]
    if item.get("desk"): manifest["classification"]["desk"] = item["desk"]
    (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for filename, fields, title in (("input.schema.json", inputs, "Input"), ("output.schema.json", outputs, "Output")):
        properties = {field["name"]: {"type": "string", "description": field["description"]} for field in fields if field["name"]}
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"https://kujolang.dev/schemas/{item['id']}/{filename}", "title": f"{item['name']} {title}", "type": "object", "properties": properties, "additionalProperties": True}
        (folder / filename).write_text(json.dumps(schema, indent=2) + "\n")


def main() -> None:
    items = chain_agents() + catalog_agents("webops", "webops-catalog.json") + catalog_agents("publishing-house", "publishing-house-catalog.json")
    house_tools = publishing_tools()
    for item in items:
        if item["package"] == "publishing-house":
            binding = house_tools.get(item["slug"], {"primary": [], "workflows": []})
            item["tools"] = {"allowed": binding["primary"]}
            item["workflows"] = binding["workflows"]
    for item in items:
        write_role(item)
    index = {"schema": "kujo.agent.registry/v1", "version": VERSION, "agent_count": len(items), "agents": [{"id": x["id"], "name": x["name"], "package": x["package"], "path": f"{x['package']}/{x['slug']}"} for x in items]}
    (ROOT / "agent-registry.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"generated {len(items)} agent packages")


if __name__ == "__main__":
    main()
