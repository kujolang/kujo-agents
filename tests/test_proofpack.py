import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOFPACK = ROOT / "tools" / "proofpack.py"


class ProofPackTests(unittest.TestCase):
    def test_markdown_report_contains_required_sections_for_non_git_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            (target / "README.md").write_text("# Sample\n", encoding="utf-8")
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ProofPack wrote", result.stdout)
            report = out.read_text(encoding="utf-8")
            for heading in [
                "# ProofPack Evidence Packet",
                "## File Inventory",
                "## Git Status",
                "## Commands Run And Evidence Artifacts",
                "## Risks And Unknowns",
                "## Next Reviewer Actions",
                "## Terminal Summary",
            ]:
                self.assertIn(heading, report)
            self.assertIn("- Git repository: no", report)
            self.assertIn("README.md", report)

    def test_json_output_is_deterministic_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            (target / "app.py").write_text("print('ok')\n", encoding="utf-8")
            out = Path(tmp) / "proofpack-report.md"
            json_out = Path(tmp) / "proofpack-report.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROOFPACK),
                    str(target),
                    "--out",
                    str(out),
                    "--json-out",
                    str(json_out),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(data["generated_by"], "proofpack")
            self.assertIsNone(data["timestamp"])
            self.assertEqual(data["inventory"]["files"], 1)
            self.assertEqual(data["inventory"]["extensions"], {".py": 1})

    def test_dry_run_does_not_write_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out), "--dry-run"],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("ProofPack dry run", result.stdout)
            self.assertFalse(out.exists())

    def test_secret_like_path_segments_are_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            secret_dir = target / "api_key_material"
            secret_dir.mkdir(parents=True)
            (secret_dir / "note.txt").write_text("secret-value\n", encoding="utf-8")
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = out.read_text(encoding="utf-8")
            self.assertIn("[REDACTED]/note.txt", report)
            self.assertNotIn("api_key_material", report)
            self.assertNotIn("secret-value", report)

    def test_out_parent_inside_target_must_already_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            out = target / "missing" / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing extra target mutation", result.stderr)
            self.assertFalse((target / "missing").exists())

    def test_json_out_inside_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            out = Path(tmp) / "proofpack-report.md"
            json_out = target / "proofpack-report.json"

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROOFPACK),
                    str(target),
                    "--out",
                    str(out),
                    "--json-out",
                    str(json_out),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--json-out must be outside the target", result.stderr)
            self.assertFalse(json_out.exists())

    @unittest.skipIf(shutil.which("git") is None, "git is not installed")
    def test_git_repo_status_is_reported_without_file_contents(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            subprocess.run(["git", "-C", str(target), "init"], check=True, capture_output=True)
            (target / "README.md").write_text("# Sample\n", encoding="utf-8")
            (target / ".env").write_text("SECRET_SHOULD_NOT_APPEAR=1\n", encoding="utf-8")
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = out.read_text(encoding="utf-8")
            self.assertIn("- Git repository: yes", report)
            self.assertIn("README.md", report)
            self.assertIn(".env", report)
            self.assertNotIn("SECRET_SHOULD_NOT_APPEAR", report)

    @unittest.skipUnless(hasattr(Path, "symlink_to"), "symlinks are not supported")
    def test_symlinked_out_path_inside_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            outside = Path(tmp) / "outside"
            target.mkdir()
            outside.mkdir()
            link = target / "linked-out"
            try:
                link.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink creation failed: {exc}")

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(link / "report.md")],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing symlinked --out path inside target", result.stderr)
            self.assertFalse((outside / "report.md").exists())

    @unittest.skipUnless(hasattr(Path, "symlink_to"), "symlinks are not supported")
    def test_outside_symlink_to_target_cannot_create_missing_target_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            link = Path(tmp) / "target-link"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"symlink creation failed: {exc}")

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(link / "missing" / "report.md")],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing extra target mutation", result.stderr)
            self.assertFalse((target / "missing").exists())

    @unittest.skipUnless(hasattr(Path, "symlink_to"), "symlinks are not supported")
    def test_symlinked_files_are_not_inventoried(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            outside = Path(tmp) / "outside.txt"
            target.mkdir()
            outside.write_text("SECRET_SHOULD_NOT_APPEAR=1\n", encoding="utf-8")
            try:
                (target / "outside-link.txt").symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"symlink creation failed: {exc}")
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = out.read_text(encoding="utf-8")
            self.assertIn("- Files: 0", report)
            self.assertNotIn("outside-link.txt", report)
            self.assertNotIn("SECRET_SHOULD_NOT_APPEAR", report)

    def test_adversarial_filenames_are_rendered_as_single_safe_list_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sample"
            target.mkdir()
            bad_name = "bad`name\n## injected heading.md"
            (target / bad_name).write_text("content\n", encoding="utf-8")
            out = Path(tmp) / "proofpack-report.md"

            result = subprocess.run(
                [sys.executable, str(PROOFPACK), str(target), "--out", str(out)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = out.read_text(encoding="utf-8")
            self.assertIn("bad`name\\n## injected heading.md", report)
            self.assertNotIn("\n## injected heading.md", report)


if __name__ == "__main__":
    unittest.main()
