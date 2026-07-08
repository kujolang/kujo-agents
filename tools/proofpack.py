#!/usr/bin/env python3
"""Create a deterministic local evidence packet for a project folder."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}

DEFAULT_OUT = "proofpack-report.md"
MAX_LISTED_FILES = 50
SENSITIVE_SEGMENT = re.compile(
    r"(secret|token|password|passwd|pwd|api[-_]?key|access[-_]?key|private[-_]?key|credential|auth)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Inventory:
    file_count: int
    dir_count: int
    total_bytes: int
    extensions: dict[str, int]
    sample_files: list[str]
    skipped_dirs: list[str]


@dataclass(frozen=True)
class GitStatus:
    is_repo: bool
    command: str
    output: list[str]
    error: str | None = None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="proofpack",
        description="Write a deterministic Markdown evidence packet for a local project.",
    )
    parser.add_argument("target", help="Project folder to scan.")
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
        help=f"Markdown report path to write. Defaults to ./{DEFAULT_OUT}.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional JSON artifact path containing the same report data.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned artifact paths without writing files.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=MAX_LISTED_FILES,
        help="Maximum sample inventory paths to include in the report.",
    )
    return parser.parse_args(argv)


def normalize_target(target: str) -> Path:
    path = Path(target).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"proofpack: target does not exist: {redact_text(str(path))}")
    if not path.is_dir():
        raise SystemExit(f"proofpack: target is not a directory: {redact_text(str(path))}")
    return path


def should_skip_dir(dirname: str) -> bool:
    return dirname in EXCLUDED_DIRS


def absolute_path(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def resolved_absolute_path(path: Path) -> Path:
    return absolute_path(path).resolve(strict=False)


def redact_text(value: str) -> str:
    redacted_parts = []
    for part in value.replace(os.sep, "/").split("/"):
        redacted_parts.append("[REDACTED]" if SENSITIVE_SEGMENT.search(part) else part)
    return "/".join(redacted_parts)


def display_text(value: str) -> str:
    redacted = redact_text(value)
    safe_chars = []
    for char in redacted:
        if char == "\n":
            safe_chars.append("\\n")
        elif char == "\r":
            safe_chars.append("\\r")
        elif char == "\t":
            safe_chars.append("\\t")
        elif ord(char) < 32 or ord(char) == 127:
            safe_chars.append(f"\\x{ord(char):02x}")
        else:
            safe_chars.append(char)
    return "".join(safe_chars)


def markdown_code(value: str) -> str:
    safe = display_text(value)
    longest_run = max((len(match.group(0)) for match in re.finditer(r"`+", safe)), default=0)
    fence = "`" * (longest_run + 1)
    if safe.startswith("`") or safe.endswith("`"):
        return f"{fence} {safe} {fence}"
    return f"{fence}{safe}{fence}"


def safe_relative(path: Path, root: Path) -> str:
    return redact_text(path.relative_to(root).as_posix())


def collect_inventory(root: Path, max_files: int, excluded_paths: set[Path] | None = None) -> Inventory:
    file_count = 0
    dir_count = 0
    total_bytes = 0
    extensions: dict[str, int] = {}
    sample_files: list[str] = []
    skipped_dirs: set[str] = set()
    excluded_resolved = {path.resolve() for path in (excluded_paths or set())}

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        dirs[:] = sorted(d for d in dirs if not should_skip_dir(d) and not (current_path / d).is_symlink())
        try:
            skipped_dirs.update(
                d for d in os.listdir(current_path) if should_skip_dir(d) and (current_path / d).is_dir()
            )
        except OSError:
            pass
        dir_count += len(dirs)

        for filename in sorted(files):
            file_path = current_path / filename
            if file_path.is_symlink():
                continue
            if file_path.resolve() in excluded_resolved:
                continue
            try:
                stat = file_path.lstat()
            except OSError:
                continue
            if not file_path.is_file():
                continue

            file_count += 1
            total_bytes += stat.st_size
            suffix = file_path.suffix.lower() or "[no extension]"
            extensions[suffix] = extensions.get(suffix, 0) + 1
            if len(sample_files) < max_files:
                sample_files.append(safe_relative(file_path, root))

    return Inventory(
        file_count=file_count,
        dir_count=dir_count,
        total_bytes=total_bytes,
        extensions=dict(sorted(extensions.items())),
        sample_files=sample_files,
        skipped_dirs=sorted(skipped_dirs),
    )


def run_git_status(root: Path) -> GitStatus:
    git_base = ["git", "-C", str(root), "-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false"]
    inside_cmd = [*git_base, "rev-parse", "--is-inside-work-tree"]
    status_cmd = [*git_base, "status", "--short", "--branch", "--untracked-files=normal", "--", "."]
    git_env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
    command_display = "GIT_OPTIONAL_LOCKS=0 git -c core.fsmonitor=false -c core.untrackedCache=false status --short --branch --untracked-files=normal -- ."

    try:
        inside = subprocess.run(inside_cmd, text=True, capture_output=True, check=False, timeout=10, env=git_env)
    except (OSError, subprocess.SubprocessError) as exc:
        return GitStatus(False, command_display, [], f"Git unavailable or failed: {redact_text(str(exc))}")

    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return GitStatus(False, command_display, ["Target is not inside a git work tree."])

    try:
        status = subprocess.run(status_cmd, text=True, capture_output=True, check=False, timeout=10, env=git_env)
    except subprocess.SubprocessError as exc:
        return GitStatus(True, command_display, [], f"Git status failed: {redact_text(str(exc))}")

    if status.returncode != 0:
        return GitStatus(True, command_display, [], redact_text(status.stderr.strip()) or "git status returned non-zero.")

    lines = [redact_text(line) for line in status.stdout.splitlines()]
    return GitStatus(True, command_display, lines or ["## clean"])


def markdown_list(items: Iterable[str], empty: str) -> list[str]:
    values = [redact_text(item) for item in items]
    if not values:
        return [f"- {empty}"]
    return [f"- {markdown_code(item)}" for item in values]


def build_report(target: Path, out_path: Path, inventory: Inventory, git_status: GitStatus) -> str:
    extension_lines = [
        f"- `{ext}`: {count}" for ext, count in sorted(inventory.extensions.items(), key=lambda item: (-item[1], item[0]))
    ]
    git_lines = [f"- {markdown_code(line)}" for line in git_status.output]
    if git_status.error:
        git_lines.append(f"- Error: {display_text(git_status.error)}")

    lines = [
        "# ProofPack Evidence Packet",
        "",
        "## Summary",
        "",
        f"- Target: {markdown_code(str(target))}",
        f"- Report artifact: {markdown_code(str(out_path))}",
        "- Generated by: `proofpack`",
        "- Timestamp: omitted for deterministic output",
        "",
        "## File Inventory",
        "",
        f"- Files: {inventory.file_count}",
        f"- Directories: {inventory.dir_count}",
        f"- Total bytes: {inventory.total_bytes}",
        "",
        "### Extensions",
        "",
        *(extension_lines or ["- No files found."]),
        "",
        "### Sample Files",
        "",
        *markdown_list(inventory.sample_files, "No files found."),
        "",
        "### Skipped Directories",
        "",
        *markdown_list(inventory.skipped_dirs, "No known generated/cache directories skipped."),
        "",
        "## Git Status",
        "",
        f"- Git repository: {'yes' if git_status.is_repo else 'no'}",
        f"- Command: {markdown_code(git_status.command)}",
        "",
        *git_lines,
        "",
        "## Commands Run And Evidence Artifacts",
        "",
        "- `proofpack` collected file metadata using Python standard-library filesystem APIs.",
        f"- {markdown_code(git_status.command)} was attempted for repository state evidence.",
        f"- Markdown evidence packet: {markdown_code(str(out_path))}",
        "",
        "## Risks And Unknowns",
        "",
        "- ProofPack records file paths and metadata, not file contents.",
        "- ProofPack does not print file contents and redacts path segments with secret-like names.",
        "- Generated/cache directories are skipped to keep the packet concise; review them manually if relevant.",
        "- Command evidence beyond internal inventory and git status must be added by a reviewer or future extension.",
        "",
        "## Next Reviewer Actions",
        "",
        "- Inspect the git status section for unexpected modified or untracked files.",
        "- Open the changed or suspicious files identified by git before approving the project state.",
        "- Run the project-specific tests, linters, or release checks that ProofPack cannot infer.",
        "- Decide whether any skipped generated/cache directory needs separate evidence.",
        "",
        "## Terminal Summary",
        "",
        f"- Wrote Markdown report: {markdown_code(str(out_path))}",
        f"- Scanned files: {inventory.file_count}",
        f"- Git repository: {'yes' if git_status.is_repo else 'no'}",
        "",
    ]
    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def resolved_path_is_inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def lexical_path_is_inside(path: Path, root: Path) -> bool:
    try:
        os.path.commonpath([str(path), str(root)])
    except ValueError:
        return False
    return os.path.commonpath([str(path), str(root)]) == str(root)


def has_symlink_component_between(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False

    current = root
    for part in relative.parts:
        current = current / part
        if current.exists() and current.is_symlink():
            return True
    return False


def validate_artifact_paths(
    target: Path,
    target_lexical: Path,
    out_path: Path,
    out_lexical: Path,
    json_path: Path | None,
    json_lexical: Path | None,
) -> None:
    if (out_lexical.exists() and out_lexical.is_symlink()) or (out_path.exists() and out_path.is_symlink()):
        raise SystemExit(f"proofpack: refusing to write through symlinked --out path: {redact_text(str(out_lexical))}")
    out_inside_by_input = lexical_path_is_inside(out_lexical, target_lexical)
    out_resolved_inside = resolved_path_is_inside(out_path, target)
    if out_inside_by_input and has_symlink_component_between(target_lexical, out_lexical):
        raise SystemExit(f"proofpack: refusing symlinked --out path inside target: {redact_text(str(out_lexical))}")
    if out_inside_by_input and not out_resolved_inside:
        raise SystemExit(f"proofpack: refusing --out path that resolves outside target: {redact_text(str(out_lexical))}")
    if out_resolved_inside and not out_path.parent.exists():
        raise SystemExit(
            "proofpack: refusing extra target mutation for missing --out parent inside target: "
            f"{redact_text(str(out_lexical.parent))}"
        )
    if json_path:
        if (json_lexical and json_lexical.exists() and json_lexical.is_symlink()) or (
            json_path.exists() and json_path.is_symlink()
        ):
            raise SystemExit(f"proofpack: refusing to write through symlinked --json-out path: {redact_text(str(json_lexical or json_path))}")
        json_inside_by_input = bool(json_lexical and lexical_path_is_inside(json_lexical, target_lexical))
        if json_inside_by_input or resolved_path_is_inside(json_path, target):
            raise SystemExit("proofpack: --json-out must be outside the target to keep target mutation to --out only")


def build_json(target: Path, out_path: Path, inventory: Inventory, git_status: GitStatus) -> dict[str, object]:
    return {
        "target": redact_text(str(target)),
        "report_artifact": redact_text(str(out_path)),
        "generated_by": "proofpack",
        "timestamp": None,
        "inventory": {
            "files": inventory.file_count,
            "directories": inventory.dir_count,
            "total_bytes": inventory.total_bytes,
            "extensions": inventory.extensions,
            "sample_files": inventory.sample_files,
            "skipped_directories": inventory.skipped_dirs,
        },
        "git_status": {
            "is_repo": git_status.is_repo,
            "command": git_status.command,
            "output": git_status.output,
            "error": git_status.error,
        },
        "risks": [
            "File paths and metadata can reveal sensitive names even when file contents are not read.",
            "Generated/cache directories are skipped by default.",
            "Project-specific validation commands are not inferred.",
        ],
        "next_reviewer_actions": [
            "Inspect git status.",
            "Review changed or suspicious files.",
            "Run project-specific checks.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.max_files < 0:
        raise SystemExit("proofpack: --max-files must be 0 or greater")

    target_lexical = absolute_path(Path(args.target))
    target = normalize_target(args.target)
    out_lexical = absolute_path(Path(args.out))
    out_path = resolved_absolute_path(Path(args.out))
    json_lexical = absolute_path(Path(args.json_out)) if args.json_out else None
    json_path = resolved_absolute_path(Path(args.json_out)) if args.json_out else None
    validate_artifact_paths(target, target_lexical, out_path, out_lexical, json_path, json_lexical)
    inventory = collect_inventory(target, args.max_files, {out_path})
    git_status = run_git_status(target)
    report = build_report(target, out_path, inventory, git_status)
    json_payload = build_json(target, out_path, inventory, git_status)

    if args.dry_run:
        print(f"ProofPack dry run: would write {redact_text(str(out_path))}")
        if json_path:
            print(f"ProofPack dry run: would write {redact_text(str(json_path))}")
        print(f"Scanned {inventory.file_count} files in {redact_text(str(target))}")
        return 0

    write_text(out_path, report)
    if json_path:
        write_text(json_path, json.dumps(json_payload, indent=2, sort_keys=True) + "\n")

    print(f"ProofPack wrote {redact_text(str(out_path))}")
    if json_path:
        print(f"ProofPack wrote {redact_text(str(json_path))}")
    print(f"Scanned {inventory.file_count} files; git repo: {'yes' if git_status.is_repo else 'no'}")
    print("Next: inspect the report's git status, risks, and reviewer actions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
