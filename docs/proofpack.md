# ProofPack

`proofpack` is a small local-first CLI script that scans a project folder and writes a deterministic Markdown evidence packet for human review.

## Usage

```bash
python3 tools/proofpack.py ./some-project --out ./proofpack-report.md
```

Optional JSON output:

```bash
python3 tools/proofpack.py ./some-project --out ./proofpack-report.md --json-out ./proofpack-report.json
```

`--json-out` must be outside the scanned target so ProofPack only mutates the target through the requested Markdown report artifact.

Dry run:

```bash
python3 tools/proofpack.py ./some-project --out ./proofpack-report.md --dry-run
```

## Report Contents

- File inventory summary with counts, extensions, sample files, and skipped generated/cache directories.
- Git status from `git status --short --branch --untracked-files=normal`, or a clear non-git note.
- Commands run and evidence artifacts.
- Risks, unknowns, and next reviewer actions.
- Terminal summary.

## Safety Notes

ProofPack reads file metadata and runs local git status checks with `GIT_OPTIONAL_LOCKS=0`, `core.fsmonitor=false`, and `core.untrackedCache=false`. It does not read file contents, use the network, install tools, commit, push, deploy, or mutate the target project except by writing the requested Markdown output artifact.

Path segments with secret-like names are redacted before they are printed or written, control characters in Markdown path output are rendered visibly, and symlinked files/directories are skipped during inventory. Reviewers should still treat generated packets as project evidence.
