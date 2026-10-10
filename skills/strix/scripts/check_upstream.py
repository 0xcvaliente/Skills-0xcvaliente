#!/usr/bin/env python3
"""Read-only usestrix/strix freshness check; Python 3.9+, standard library only.

Exit 0: reviewed head is current. Exit 10: upstream has changes to review.
Exit 2: freshness could not be established. Never writes or executes fetched data.
"""

import argparse
import json
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPOSITORY = "usestrix/strix"
REPOSITORY_URL = "https://github.com/" + REPOSITORY
API_ROOT = "https://api.github.com/repos/" + REPOSITORY
DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "references" / "upstream.json"
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
SHA_PATTERN = re.compile(r"[0-9a-f]{40}\Z")
FILE_MODES = {"blob": {"100644", "100755", "120000"}, "commit": {"160000"}}


class CheckError(Exception):
    """A failed check, never evidence that the installed baseline is current."""


def valid_sha(value):
    return isinstance(value, str) and SHA_PATTERN.fullmatch(value) is not None


def valid_path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and str(path) == value
        and all(ord(char) >= 32 and ord(char) != 127 for char in value)
    )


def validate_file(path, entry):
    if not valid_path(path) or not isinstance(entry, dict):
        raise CheckError("Invalid file inventory entry")
    kind = entry.get("type")
    if (
        not valid_sha(entry.get("sha"))
        or not isinstance(kind, str)
        or kind not in FILE_MODES
        or not isinstance(entry.get("mode"), str)
        or entry.get("mode") not in FILE_MODES[kind]
    ):
        raise CheckError("Invalid file inventory metadata")
    return {key: entry[key] for key in ("sha", "mode", "type")}


def validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise CheckError("Baseline must be a JSON object")
    if manifest.get("schema_version") != 1 or manifest.get("repository") != REPOSITORY:
        raise CheckError("Unsupported baseline schema or repository")
    if not valid_sha(manifest.get("reviewed_commit")) or not valid_sha(manifest.get("reviewed_tree")):
        raise CheckError("Invalid reviewed revision")
    files = manifest.get("files")
    if not isinstance(files, dict) or not files:
        raise CheckError("Baseline file inventory is missing")
    return {path: validate_file(path, entry) for path, entry in files.items()}


def fetch_json(endpoint):
    # Fixed public repository, no credentials and no project data in requests.
    if not endpoint.startswith(API_ROOT + "/") and endpoint != API_ROOT:
        raise CheckError("Request outside the upstream repository")
    request = Request(endpoint, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "strix-upstream-check",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urlopen(request, timeout=10) as response:
            data = response.read(MAX_RESPONSE_BYTES + 1)
        if len(data) > MAX_RESPONSE_BYTES:
            raise CheckError("GitHub response exceeds the checker size limit")
        return json.loads(data)
    except HTTPError as exc:
        if exc.code in (403, 429):
            raise CheckError("GitHub API access or rate limit prevented the check") from None
        raise CheckError("GitHub API returned HTTP {}".format(exc.code)) from None
    except (URLError, socket.timeout, TimeoutError, OSError):
        raise CheckError("GitHub API could not be reached") from None
    except (ValueError, UnicodeError):
        raise CheckError("GitHub API returned invalid JSON") from None


def normalize_tree(payload, expected_sha):
    if not isinstance(payload, dict) or payload.get("sha") != expected_sha:
        raise CheckError("GitHub returned an unexpected tree revision")
    if payload.get("truncated") is not False:
        raise CheckError("GitHub tree is truncated or completeness is unknown")
    entries = payload.get("tree")
    if not isinstance(entries, list) or not entries:
        raise CheckError("GitHub file inventory is missing")
    files = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise CheckError("Invalid GitHub tree entry")
        if entry.get("type") == "tree":
            continue
        path = entry.get("path")
        normalized = validate_file(path, entry)
        if path in files:
            raise CheckError("Duplicate GitHub tree path")
        files[path] = normalized
    if not files:
        raise CheckError("GitHub file inventory is empty")
    return files


def category(path):
    if path.startswith("skills/"):
        return "consumer_skills"
    if path.startswith("strix/skills/"):
        return "knowledge_packs"
    if path.startswith(("strix/agents/", "strix/tools/", "strix/report/")):
        return "methodology_and_tools"
    if path.startswith(("strix/interface/", "strix/runtime/", "strix/config/", "strix/core/", "strix/utils/", "scripts/", "containers/")) or path in ("pyproject.toml", "uv.lock"):
        return "runtime_and_integration"
    if path.startswith("docs/") or path in ("README.md", "AGENTS.md", "LICENSE", "NOTICE"):
        return "documentation_and_license"
    return "other"


def compare_files(before, after):
    changes = []
    for path in sorted(set(before) | set(after)):
        old, new = before.get(path), after.get(path)
        if old == new:
            continue
        status = "added" if old is None else "removed" if new is None else "modified"
        changes.append({"path": path, "status": status, "category": category(path)})
    return changes


def check_upstream(manifest, get_json=None):
    get_json = get_json or fetch_json
    baseline = validate_manifest(manifest)
    metadata = get_json(API_ROOT)
    branch = metadata.get("default_branch") if isinstance(metadata, dict) else None
    if not isinstance(branch, str) or not branch or any(ord(char) < 32 for char in branch):
        raise CheckError("GitHub default branch could not be resolved")
    # Resolve the default branch every time; do not assume it is still main.
    commit = get_json(API_ROOT + "/commits/" + quote(branch, safe=""))
    if not isinstance(commit, dict) or not valid_sha(commit.get("sha")):
        raise CheckError("GitHub head revision is invalid")
    latest = commit["sha"]
    details = commit.get("commit")
    tree = details.get("tree") if isinstance(details, dict) else None
    tree_sha = tree.get("sha") if isinstance(tree, dict) else None
    if not valid_sha(tree_sha):
        raise CheckError("GitHub head tree is invalid")
    reviewed = manifest["reviewed_commit"]
    result = {
        "status": "current" if latest == reviewed else "updates_available",
        "repository": REPOSITORY_URL,
        "default_branch": branch,
        "reviewed_commit": reviewed,
        "latest_commit": latest,
        "reviewed_at": manifest.get("reviewed_at"),
        "compare_url": REPOSITORY_URL + "/compare/" + reviewed + "..." + latest,
        "changes": [],
    }
    if latest == reviewed:
        if tree_sha != manifest["reviewed_tree"]:
            raise CheckError("Baseline commit and tree do not agree with GitHub")
    elif tree_sha != manifest["reviewed_tree"]:
        latest_tree = get_json(API_ROOT + "/git/trees/" + tree_sha + "?recursive=1")
        result["changes"] = compare_files(baseline, normalize_tree(latest_tree, tree_sha))
    result["change_count"] = len(result["changes"])
    result["review_required"] = latest != reviewed
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Reviewed baseline JSON (default: bundled upstream.json)")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = check_upstream(manifest)
        code = 0 if result["status"] == "current" else 10
    except (CheckError, OSError, ValueError, UnicodeError, RecursionError) as exc:
        # Only our deliberately sanitized error text is exposed, not an API body.
        reason = str(exc) if isinstance(exc, CheckError) else "Baseline could not be read or parsed"
        result = {"status": "unknown", "repository": REPOSITORY_URL, "reason": reason}
        code = 2
    result["checked_at"] = datetime.now(timezone.utc).isoformat()
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
