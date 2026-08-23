#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; WEBOPS=ROOT/"webops"; SIBLING=ROOT.parent
CAPS={"website","repository","browser","web-search","site-crawl","content-graph","search-performance-provider","analytics-provider","keyword-data-provider","backlink-data-provider","url-inspection-provider","page-performance-provider","field-performance-provider","search-submission-provider","publishing-provider","distribution-provider"}
PERMS={"OBSERVE":0,"PROPOSE":1,"ACT":2}
TOOLS={"SiteProbe":"siteprobe","SearchBridge":"searchbridge","ContentGraph":"contentgraph","RAG":"rag","RunLedger":"runledger","CaseFile":"casefile","Lens":"lens","Eval":"eval","Dispatch":"dispatch","Howl":"howl","CMS":"cms","SSG":"ssg"}
WORKFLOWS={"webops-site-bootstrap","webops-weekly-site-health","webops-weekly-search-intelligence","webops-weekly-content-intelligence","webops-post-publish","webops-content-refresh","webops-monthly-seo-review","webops-quarterly-content-portfolio","webops-ai-visibility-benchmark","webops-finding-to-fix"}
HEADINGS=["Agent Contract","Use This Agent When","Do Not Use This Agent When","Inputs Expected","Outputs Required","Allowed Tools And Workflows","Workflow","Evidence Requirements","Degraded Operation","Handoff Rules","Escalation Rules","Stop Conditions","Anti-Scope"]

def main():
    errors=[]; data=json.loads((WEBOPS/"webops-catalog.json").read_text()); agents=data.get("agents",[])
    if data.get("agent_count")!=28 or len(agents)!=28: errors.append("catalog must contain exactly 28 agents")
    dirs={x.name for x in WEBOPS.iterdir() if x.is_dir()}; slugs={a["slug"] for a in agents}
    if dirs!=slugs: errors.append(f"agent directories differ from catalog: missing={sorted(slugs-dirs)} extra={sorted(dirs-slugs)}")
    role_skills=set()
    for agent in agents:
        slug=agent["slug"]; folder=WEBOPS/slug; contract=folder/"AGENT.md"; skill=folder/"SKILL.md"
        manifest=folder/"manifest.json"
        input_schema=folder/"input.schema.json"
        output_schema=folder/"output.schema.json"
        if not contract.is_file() or not skill.is_file(): errors.append(f"{slug}: missing AGENT.md or SKILL.md"); continue
        pmin=agent["permission_min"]; pmax=agent["permission_max"]
        for path in (manifest,input_schema,output_schema):
            if not path.is_file(): errors.append(f"{slug}: missing {path.name}")
        if manifest.is_file():
            try:
                manifest_data=json.loads(manifest.read_text())
                if manifest_data.get("id") != f"webops.{slug}": errors.append(f"{slug}: manifest id mismatch")
                if manifest_data.get("classification",{}).get("package") != "webops": errors.append(f"{slug}: manifest package mismatch")
                if manifest_data.get("permissions",{}).get("maximum") != pmax: errors.append(f"{slug}: manifest permission mismatch")
            except json.JSONDecodeError as exc: errors.append(f"{slug}: invalid manifest JSON: {exc}")
        body=contract.read_text(); skill_body=skill.read_text()
        for heading in HEADINGS:
            if f"## {heading}" not in body: errors.append(f"{slug}: missing heading {heading}")
        for label in ("Minimum Permission Mode","Maximum Permission Mode","Required Capabilities","Recommended Capabilities","Optional Capabilities","Historical Inputs"):
            if f"- {label}:" not in body: errors.append(f"{slug}: missing {label}")
        if pmin not in PERMS or pmax not in PERMS or PERMS.get(pmin,99)>PERMS.get(pmax,-1): errors.append(f"{slug}: invalid permission range")
        for cap in agent["required_capabilities"]+agent["recommended_capabilities"]+agent["optional_capabilities"]:
            if cap not in CAPS: errors.append(f"{slug}: unknown capability {cap}")
        for tool in agent["primary_tools"]+agent["secondary_tools"]:
            if tool not in TOOLS: errors.append(f"{slug}: unknown tool {tool}")
            elif not (SIBLING/TOOLS[tool]).is_dir(): errors.append(f"{slug}: missing sibling tool repo {TOOLS[tool]}")
        for workflow in agent["recommended_workflows"]:
            if workflow not in WORKFLOWS: errors.append(f"{slug}: unknown workflow {workflow}")
            elif (SIBLING/"kujo-workflows").is_dir() and not (SIBLING/"kujo-workflows"/workflow).is_dir(): errors.append(f"{slug}: missing workflow directory {workflow}")
        match=re.search(r"^name:\s*(\S+)$",skill_body,re.M)
        if not match: errors.append(f"{slug}: missing role skill frontmatter name")
        elif match.group(1) in role_skills: errors.append(f"duplicate role skill {match.group(1)}")
        else: role_skills.add(match.group(1))
        for global_skill in agent["existing_kujo_skills"]+agent["webops_domain_skills"]:
            if (SIBLING/"kujo-skills").is_dir() and not (SIBLING/"kujo-skills"/"skills"/global_skill/"SKILL.md").is_file(): errors.append(f"{slug}: missing global skill {global_skill}")
    if len(role_skills)!=28: errors.append("role skill names are not uniquely complete")
    coc=[x for x in (ROOT/"chain-of-command").iterdir() if x.is_dir() and x.name!="00-docs"]
    for folder in coc:
        if not (folder/"AGENT.md").is_file() or not (folder/"SKILL.md").is_file(): errors.append(f"Chain of Command regression: {folder.name}")
    secret_pattern=re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}")
    for path in WEBOPS.rglob("*"):
        if path.is_file() and path.suffix in {".md",".json"} and secret_pattern.search(path.read_text(errors="ignore")): errors.append(f"possible secret material: {path}")
    if errors:
        print(json.dumps({"valid":False,"errors":errors},indent=2)); return 1
    print(json.dumps({"valid":True,"webops_agents":28,"role_skills":28,"chain_of_command_agents":len(coc),"capabilities":sorted(CAPS),"workflows":sorted(WORKFLOWS)},indent=2)); return 0

if __name__=="__main__": raise SystemExit(main())
