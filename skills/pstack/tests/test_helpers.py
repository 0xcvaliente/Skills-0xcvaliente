import csv
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("package_checker", ROOT / "scripts/check_package.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class PackageIntegrityTests(unittest.TestCase):
    def test_complete_package(self):
        manifest, problems = CHECKER.verify(ROOT)
        self.assertEqual(problems, [])
        self.assertEqual(len(manifest["files"]), 164)

    def test_changed_missing_and_unlisted_source_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "package"
            shutil.copytree(ROOT, copy)
            retained = copy / "references/upstream"
            (retained / "LICENSE").write_text("damaged notice")
            (retained / "README.md").unlink()
            (retained / "unexpected.txt").write_text("not in the source snapshot")
            _, problems = CHECKER.verify(copy)
            self.assertTrue(any("Changed retained bytes:" in p for p in problems))
            self.assertTrue(any("Missing retained file:" in p for p in problems))
            self.assertTrue(any("Unlisted retained file:" in p for p in problems))

    def test_accidentally_discoverable_cursor_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "package"
            shutil.copytree(ROOT, copy)
            source = copy / "references/upstream/skills/how/SKILL.md.source"
            source.rename(source.with_name("SKILL.md"))
            _, problems = CHECKER.verify(copy)
            self.assertTrue(any("Expected one live SKILL.md" in p for p in problems))

    def test_independent_original_source_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path(directory)
            manifest, _ = CHECKER.verify(ROOT)
            for entry in manifest["files"]:
                target = original / entry["original_path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / entry["stored_path"], target)
            _, problems = CHECKER.verify(ROOT, original)
            self.assertEqual(problems, [])
            (original / "omitted.txt").write_text("new source")
            _, problems = CHECKER.verify(ROOT, original)
            self.assertIn("Source file omitted from manifest: omitted.txt", problems)


class DecisionLogTests(unittest.TestCase):
    def test_append_preserves_records_and_sanitizes_cells(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "nested/decisions.tsv"
            helper = ROOT / "scripts/decision-log.sh"
            subprocess.run(["bash", str(helper), str(log), "fix", "=formula", "why\tnewline\n", "@evidence", "pass"], check=True)
            subprocess.run(["bash", str(helper), str(log), "verify", "second", "reason", "probe", "pass"], check=True)
            with log.open(newline="") as stream:
                rows = list(csv.reader(stream, delimiter="\t"))
            self.assertEqual(rows[0], ["ts", "phase", "decision", "why", "evidence", "result"])
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(len(row) == 6 for row in rows))
            self.assertEqual(rows[1][2], "'=formula")
            self.assertEqual(rows[1][3], "why newline ")
            self.assertEqual(rows[1][4], "'@evidence")
            self.assertEqual(rows[2][2], "second")


if __name__ == "__main__":
    unittest.main()
