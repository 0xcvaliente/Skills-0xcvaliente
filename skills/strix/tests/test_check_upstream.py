"""Offline behavioral regression tests; never contact a target or GitHub."""

import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError


SKILL = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_upstream", SKILL / "scripts" / "check_upstream.py")
upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(upstream)

BASE, HEAD, TREE, NEW_TREE = (char * 40 for char in "abcd")


def file_entry(sha="e" * 40, mode="100644", kind="blob"):
    return {"sha": sha, "mode": mode, "type": kind}


def baseline():
    return {
        "schema_version": 1,
        "repository": "usestrix/strix",
        "reviewed_commit": BASE,
        "reviewed_tree": TREE,
        "reviewed_at": "2026-10-08",
        "files": {
            "skills/existing/SKILL.md": file_entry(),
            "strix/skills/old.md": file_entry(),
            "strix/agents/prompts/system_prompt.jinja": file_entry(),
            "scripts/install.sh": file_entry(),
        },
    }


def responses(files=None, latest=HEAD, tree_sha=NEW_TREE, branch="main", truncated=False):
    files = baseline()["files"] if files is None else files
    tree = [{"path": path, **entry} for path, entry in files.items()]
    return Mock(side_effect=[
        {"default_branch": branch},
        {"sha": latest, "commit": {"tree": {"sha": tree_sha}}},
        {"sha": tree_sha, "truncated": truncated, "tree": tree},
    ])


class UpstreamTests(unittest.TestCase):
    def test_current_commit_needs_no_tree_fetch(self):
        request = responses(latest=BASE, tree_sha=TREE)
        result = upstream.check_upstream(baseline(), request)
        self.assertEqual(result["status"], "current")
        self.assertFalse(result["review_required"])
        self.assertEqual(result["changes"], [])
        self.assertEqual(request.call_count, 2)

    def test_add_remove_edit_and_mode_changes_are_detected(self):
        files = copy.deepcopy(baseline()["files"])
        del files["strix/skills/old.md"]
        files["skills/brand-new/SKILL.md"] = file_entry("f" * 40)
        files["strix/agents/prompts/system_prompt.jinja"] = file_entry("f" * 40)
        files["scripts/install.sh"]["mode"] = "100755"
        files["vendor/module"] = file_entry("f" * 40, "160000", "commit")
        result = upstream.check_upstream(baseline(), responses(files))
        changes = {item["path"]: item for item in result["changes"]}
        self.assertEqual(result["status"], "updates_available")
        self.assertEqual(result["change_count"], 5)
        self.assertEqual(changes["skills/brand-new/SKILL.md"]["status"], "added")
        self.assertEqual(changes["skills/brand-new/SKILL.md"]["category"], "consumer_skills")
        self.assertEqual(changes["strix/skills/old.md"]["status"], "removed")
        self.assertEqual(changes["strix/skills/old.md"]["category"], "knowledge_packs")
        self.assertEqual(changes["scripts/install.sh"]["status"], "modified")

    def test_resolves_renamed_default_branch_with_safe_encoding(self):
        request = responses(branch="stable/next", latest=BASE, tree_sha=TREE)
        result = upstream.check_upstream(baseline(), request)
        self.assertEqual(result["default_branch"], "stable/next")
        self.assertEqual(request.call_args_list[1].args[0], upstream.API_ROOT + "/commits/stable%2Fnext")

    def test_different_commit_same_tree_still_requires_review(self):
        request = responses(tree_sha=TREE)
        result = upstream.check_upstream(baseline(), request)
        self.assertEqual(result["status"], "updates_available")
        self.assertTrue(result["review_required"])
        self.assertEqual(result["changes"], [])
        self.assertEqual(request.call_count, 2)

    def test_unrelated_repository_changes_are_visible(self):
        files = copy.deepcopy(baseline()["files"])
        files["tests/new_test.py"] = file_entry()
        result = upstream.check_upstream(baseline(), responses(files))
        self.assertEqual(result["status"], "updates_available")
        self.assertEqual(result["changes"][0]["category"], "other")

    def test_rewritten_history_is_compared_without_ancestry_assumptions(self):
        files = {"README.md": file_entry()}
        result = upstream.check_upstream(baseline(), responses(files, latest="0" * 40))
        self.assertEqual(result["change_count"], 5)
        self.assertEqual(result["latest_commit"], "0" * 40)

    def test_truncated_inventory_is_not_a_success(self):
        with self.assertRaisesRegex(upstream.CheckError, "truncated"):
            upstream.check_upstream(baseline(), responses(truncated=True))

    def test_missing_default_branch_or_head_is_not_a_success(self):
        for payload in ({}, [], {"default_branch": ""}):
            with self.subTest(payload=payload), self.assertRaises(upstream.CheckError):
                upstream.check_upstream(baseline(), Mock(return_value=payload))
        request = Mock(side_effect=[{"default_branch": "main"}, {"sha": "invalid"}])
        with self.assertRaises(upstream.CheckError):
            upstream.check_upstream(baseline(), request)

    def test_current_commit_tree_must_agree(self):
        with self.assertRaisesRegex(upstream.CheckError, "do not agree"):
            upstream.check_upstream(baseline(), responses(latest=BASE))

    def test_malformed_inventory_is_rejected(self):
        invalid_entries = [
            ("../escape", file_entry()),
            ("/absolute", file_entry()),
            ("path", {"sha": [], "mode": "100644", "type": "blob"}),
            ("path", {"sha": "f" * 40, "mode": [], "type": "blob"}),
            ("path", {"sha": "f" * 40, "mode": "100644", "type": []}),
            ("line\nbreak", file_entry()),
        ]
        for path, entry in invalid_entries:
            with self.subTest(path=path, entry=entry), self.assertRaises(upstream.CheckError):
                upstream.normalize_tree({"sha": TREE, "truncated": False, "tree": [{"path": path, **entry}]}, TREE)

    def test_wrong_repository_baseline_is_rejected_before_network(self):
        manifest = baseline()
        manifest["repository"] = "someone/else"
        request = Mock()
        with self.assertRaises(upstream.CheckError):
            upstream.check_upstream(manifest, request)
        request.assert_not_called()

    def test_timeout_and_rate_limit_have_sanitized_errors(self):
        with patch.object(upstream, "urlopen", side_effect=TimeoutError("private detail")):
            with self.assertRaisesRegex(upstream.CheckError, "could not be reached"):
                upstream.fetch_json(upstream.API_ROOT)
        error = HTTPError(upstream.API_ROOT, 403, "private detail", {}, None)
        with patch.object(upstream, "urlopen", side_effect=error):
            with self.assertRaisesRegex(upstream.CheckError, "rate limit"):
                upstream.fetch_json(upstream.API_ROOT)

    def test_outside_endpoint_rejected_without_network(self):
        with patch.object(upstream, "urlopen") as request:
            with self.assertRaises(upstream.CheckError):
                upstream.fetch_json("https://example.com/project")
            request.assert_not_called()

    def test_unknown_cli_status_preserves_baseline_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "upstream.json"
            raw = json.dumps(baseline()).encode("utf-8")
            path.write_bytes(raw)
            output = io.StringIO()
            with patch.object(upstream, "urlopen", side_effect=TimeoutError()), contextlib.redirect_stdout(output):
                code = upstream.main(["--manifest", str(path)])
            result = json.loads(output.getvalue())
            self.assertEqual(code, 2)
            self.assertEqual(result["status"], "unknown")
            self.assertIn("checked_at", result)
            self.assertEqual(path.read_bytes(), raw)

    def test_cli_update_exit_and_inventory_are_preserved(self):
        manifest = baseline()
        original = copy.deepcopy(manifest)
        files = copy.deepcopy(manifest["files"])
        files["strix/skills/new.md"] = file_entry()
        result = upstream.check_upstream(manifest, responses(files))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "upstream.json"
            raw = json.dumps(manifest).encode("utf-8")
            path.write_bytes(raw)
            with patch.object(upstream, "check_upstream", return_value=result), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(upstream.main(["--manifest", str(path)]), 10)
            self.assertEqual(path.read_bytes(), raw)
        self.assertEqual(manifest, original)

    def test_invalid_manifest_cli_is_unknown_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("broken json", encoding="utf-8")
            output = io.StringIO()
            with patch.object(upstream, "urlopen") as request, contextlib.redirect_stdout(output):
                self.assertEqual(upstream.main(["--manifest", str(path)]), 2)
                request.assert_not_called()
            self.assertEqual(json.loads(output.getvalue())["status"], "unknown")

    def test_bundled_baseline_and_future_pack_detection(self):
        manifest = json.loads((SKILL / "references" / "upstream.json").read_text(encoding="utf-8"))
        files = upstream.validate_manifest(manifest)
        self.assertIn("skills/penetration-testing-with-strix/SKILL.md", files)
        self.assertIn("strix/skills/analysis/counterevidence.md", files)
        self.assertIn("LICENSE", files)
        self.assertEqual(upstream.compare_files(files, dict(files)), [])
        changed = dict(files)
        changed["strix/skills/custom/future-pack.md"] = file_entry()
        self.assertEqual(upstream.compare_files(files, changed)[0]["status"], "added")


if __name__ == "__main__":
    unittest.main()
