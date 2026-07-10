#!/usr/bin/env python3
"""Deterministic structural checks for every reusable agent contract."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AGENT_MARKERS = ("# ", "## Evidence Requirements")
REQUIRED_SKILL_MARKERS = ("---", "name:", "description:", "# ")


def main() -> int:
    errors: list[str] = []
    agents = sorted(ROOT.rglob("AGENT.md"))
    skills = sorted(ROOT.rglob("SKILL.md"))
    if len(agents) != 30:
        errors.append(f"expected 30 AGENT.md contracts, found {len(agents)}")
    if len(skills) != 30:
        errors.append(f"expected 30 paired SKILL.md contracts, found {len(skills)}")
    skill_dirs = {path.parent for path in skills}
    for agent in agents:
        if agent.parent not in skill_dirs:
            errors.append(f"{agent.relative_to(ROOT)} lacks paired SKILL.md")
        text = agent.read_text(encoding="utf-8")
        if "## Agent Contract" not in text and "## Role And Mission" not in text:
            errors.append(f"{agent.relative_to(ROOT)} missing role/contract section")
        for marker in REQUIRED_AGENT_MARKERS:
            if marker not in text:
                errors.append(f"{agent.relative_to(ROOT)} missing {marker!r}")
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        for marker in REQUIRED_SKILL_MARKERS:
            if marker not in text:
                errors.append(f"{skill.relative_to(ROOT)} missing {marker!r}")
    if errors:
        print("Agent contract validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Agent contract validation passed: {len(agents)} AGENT.md / {len(skills)} SKILL.md pairs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
