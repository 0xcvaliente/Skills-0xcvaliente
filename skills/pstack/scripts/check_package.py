#!/usr/bin/env python3
"""Verify that the complete pinned pstack source survives packaging unchanged."""

import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root, source=None):
    root = Path(root).resolve()
    manifest = json.loads((root / "references/upstream-manifest.json").read_text())
    entries = manifest["files"]
    problems = []
    expected = set()
    originals = set()
    for entry in entries:
        stored = entry["stored_path"]
        original = entry["original_path"]
        if stored in expected or original in originals:
            problems.append("Duplicate manifest entry: " + original)
        expected.add(stored)
        originals.add(original)
        packaged = root / stored
        if not packaged.is_file():
            problems.append("Missing retained file: " + stored)
        elif digest(packaged) != entry["sha256"]:
            problems.append("Changed retained bytes: " + stored)
        elif bool(packaged.stat().st_mode & 0o111) != (entry["git_mode"] == "100755"):
            problems.append("Changed executable mode: " + stored)
        if source is not None:
            source_file = Path(source) / original
            if not source_file.is_file() or digest(source_file) != entry["sha256"]:
                problems.append("Source snapshot mismatch: " + original)
    archive = root / "references/upstream"
    actual = {p.relative_to(root).as_posix() for p in archive.rglob("*") if p.is_file()}
    for extra in sorted(actual - expected):
        problems.append("Unlisted retained file: " + extra)
    if source is not None:
        source_files = {p.relative_to(source).as_posix() for p in Path(source).rglob("*") if p.is_file()}
        for extra in sorted(source_files - originals):
            problems.append("Source file omitted from manifest: " + extra)
    entrypoints = sorted(p.relative_to(root).as_posix() for p in root.rglob("SKILL.md"))
    if entrypoints != ["SKILL.md"]:
        problems.append("Expected one live SKILL.md; found " + repr(entrypoints))
    return manifest, problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source", type=Path, help="Optional original pstack directory for a full comparison")
    args = parser.parse_args()
    manifest, problems = verify(args.root, args.source)
    if problems:
        print("\n".join(problems))
        return 1
    print("Verified {} original files at {}; one live skill.".format(
        len(manifest["files"]), manifest["source_revision"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
