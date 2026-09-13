#!/usr/bin/env python3
"""Validate SDD change records against a read-only Git snapshot.

This checks declared evidence and source consistency, not vehicle qualification.
Record-supplied procedures are documentation and are never executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def literal_path(value: object) -> str:
    if (not isinstance(value, str) or not value.strip()
            or any(c in value for c in "\\:*?[]#\x00\n\r")
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise ValueError(f"Expected a literal repository-relative path: {value!r}")
    return value


def is_record(path: str) -> bool:
    return bool(re.fullmatch(r"docs/changes/[^/]+\.json", path))


def is_implementation(path: str) -> bool:
    return not (path.lower().endswith(".md") or is_record(path)
                or (path.startswith("docs/development/templates/") and path.endswith(".json"))
                or path in (".gitignore", ".gitattributes"))


class Snapshot:
    def __init__(self, root: Path, *, staged: bool = False, base: str | None = None):
        if staged and base is not None:
            raise ValueError("--staged and --base are mutually exclusive")
        self.root = Path(root).resolve()
        self.staged = staged
        actual_root = Path(self.git("rev-parse", "--show-toplevel").decode().strip()).resolve()
        if actual_root != self.root:
            raise ValueError("Run the SDD guard from the repository root")
        self.base = self.git("rev-parse", "--verify", "--end-of-options",
                             f"{base or 'HEAD'}^{{commit}}").decode().strip()

    def git(self, *args: str) -> bytes:
        result = subprocess.run(["git", "-C", str(self.root), *args],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode:
            raise ValueError(f"Git snapshot failed: {result.stderr.decode(errors='replace').strip()}")
        return result.stdout

    def changed(self) -> set[str]:
        args = ["diff", "--no-renames", "--name-only", "-z"]
        if self.staged:
            args.append("--cached")
        paths = self.git(*args, self.base, "--").split(b"\0")
        if not self.staged:
            paths += self.git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
        return {p.decode("utf-8", errors="surrogateescape") for p in paths if p}

    def entry(self, path: str) -> tuple[str, str] | None:
        raw = self.git("ls-files", "--stage", "-z", "--", path)
        if not raw:
            return None
        entries = raw.rstrip(b"\0").split(b"\0")
        if len(entries) != 1:
            raise ValueError(f"Unmerged or non-file index path: {path}")
        fields = entries[0].split(b"\t", 1)[0].split()
        if fields[2] != b"0":
            raise ValueError(f"Unmerged index path: {path}")
        return fields[0].decode(), fields[1].decode()

    def read(self, path: str) -> bytes:
        path = literal_path(path)
        entry = self.entry(path)
        if self.staged:
            if entry is None:
                raise FileNotFoundError(f"Not staged: {path}")
            mode, oid = entry
            if mode == "120000":
                raise ValueError(f"Symlink cannot be SDD evidence: {path}")
            if mode == "160000":
                return f"gitlink:{oid}".encode()
            return self.git("show", f":{path}")
        local = self.root / path
        if local.is_symlink() or not local.resolve().is_relative_to(self.root):
            raise ValueError(f"Outside-repository path or symlink: {path}")
        if entry and entry[0] == "160000" and local.is_dir():
            if (local / ".git").exists():
                if self.git("-C", str(local), "status", "--porcelain"):
                    raise ValueError(f"Submodule must be clean before fingerprinting: {path}")
                oid = self.git("-C", str(local), "rev-parse", "HEAD").decode().strip()
            else:
                oid = entry[1]  # Uninitialized but indexed gitlink.
            return f"gitlink:{oid}".encode()
        return local.read_bytes()

    def fingerprint(self, path: str) -> str:
        try:
            content = self.read(path)
        except FileNotFoundError:
            result = subprocess.run(
                ["git", "-C", str(self.root), "cat-file", "-e", f"{self.base}:{literal_path(path)}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            if result.returncode:
                raise ValueError(f"Missing source was never present in base: {path}") from None
            return "deleted"
        if b"\0" not in content:
            content = content.replace(b"\r\n", b"\n")
        return hashlib.sha256(content).hexdigest()


def fingerprints(record: dict, snapshot: Snapshot) -> dict[str, str]:
    paths = record.get("code_paths")
    if not isinstance(paths, list) or not paths:
        raise ValueError("code_paths must be a nonempty list")
    paths = list(paths)
    cases = record.get("tests")
    if not isinstance(cases, list):
        raise ValueError("tests must be a list before fingerprinting")
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Each test must be an object")
        if case.get("kind") == "automated":
            paths.append(literal_path(case.get("test_file")))
    return {path: snapshot.fingerprint(path) for path in sorted({literal_path(p) for p in paths})}


def validate_record(record: object, snapshot: Snapshot, *, complete: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["Record must be a JSON object"]

    def require_text(value: object, label: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label} must be nonempty text")
            return False
        return True

    def string_list(value: object, label: str) -> list[str]:
        if (not isinstance(value, list) or not value
                or any(not isinstance(v, str) or not v.strip() for v in value)):
            errors.append(f"{label} must be a nonempty list of strings")
            return []
        if len(value) != len(set(value)):
            errors.append(f"{label} contains duplicates")
        return value

    def local_file(value: object, label: str, *, markdown: bool = False) -> str:
        try:
            path = literal_path(value)
            if path.startswith("docs/development/templates/"):
                raise ValueError("A template is not completed specification/evidence")
            if markdown and not path.lower().endswith(".md"):
                raise ValueError("Use a local Markdown specification/evidence file")
            raw = snapshot.read(path)
            if not raw.strip():
                raise ValueError("File is empty")
            return raw.decode("utf-8")
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: {exc}")
            return ""

    if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        errors.append("schema_version must be 1")
    require_text(record.get("id"), "id")
    status = record.get("status")
    if status not in ("ready", "complete"):
        errors.append("Implementation requires a ready or complete record; draft cannot authorize code")
    if complete and status != "complete":
        errors.append("Completion requires status=complete")
    closing = complete or status == "complete"
    if record.get("scope") not in ("tooling", "integration"):
        errors.append("scope must be tooling or integration; neither certifies the whole system")
    requirements = string_list(record.get("requirements"), "requirements")
    code_paths = string_list(record.get("code_paths"), "code_paths")
    for path in code_paths:
        try:
            literal_path(path)
        except ValueError as exc:
            errors.append(str(exc))
    specs = record.get("specifications")
    if not isinstance(specs, dict):
        specs = {}
    req_text = ""
    for kind in ("requirements", "product", "technical"):
        text = local_file(specs.get(kind), f"specifications.{kind}", markdown=True)
        if kind == "requirements":
            req_text = text
    for req in requirements:
        if not re.search(rf"(?<![\w-]){re.escape(req)}(?![\w-])", req_text):
            errors.append(f"Requirement {req} is absent from the requirement specification")
    review = record.get("review")
    if not isinstance(review, dict):
        review = {}
    for field in ("by", "basis"):
        require_text(review.get(field), f"review.{field}")

    tests = record.get("tests")
    if not isinstance(tests, list) or not tests:
        errors.append("tests must contain prewritten cases")
        tests = []
    mapped: set[str] = set()
    test_ids: set[str] = set()
    automated = 0
    for index, case in enumerate(tests):
        label = f"tests[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be an object")
            continue
        if require_text(case.get("id"), f"{label}.id"):
            if case["id"] in test_ids:
                errors.append(f"Duplicate test ID: {case['id']}")
            test_ids.add(case["id"])
        links = string_list(case.get("requirements"), f"{label}.requirements")
        mapped.update(links)
        if set(links) - set(requirements):
            errors.append(f"{label} refers to undeclared requirements")
        for field in ("procedure", "expected"):
            require_text(case.get(field), f"{label}.{field}")
        if case.get("level") not in ("host", "emulator", "reference", "bench", "vehicle"):
            errors.append(f"{label}.level must identify the actual test environment")
        if case.get("kind") not in ("automated", "manual"):
            errors.append(f"{label}.kind must be automated or manual")
        if case.get("kind") == "automated":
            automated += 1
            if closing:
                local_file(case.get("test_file"), f"{label}.test_file")
            else:
                try:
                    literal_path(case.get("test_file"))
                except ValueError as exc:
                    errors.append(f"{label}.test_file: {exc}")
        result = case.get("result")
        if result not in ("planned", "pass", "fail", "blocked", "not_run"):
            errors.append(f"{label}.result is invalid")
        if closing and result != "pass":
            errors.append(f"{label} is {result!r}; only pass permits completion")
        if result == "pass":
            local_file(case.get("evidence"), f"{label}.evidence", markdown=True)
    for req in set(requirements) - mapped:
        errors.append(f"Requirement {req} has no test case")
    if closing:
        if not automated:
            errors.append("Code completion requires at least one automated test case")
        recorded = record.get("code_sha256")
        try:
            actual = fingerprints(record, snapshot)
            if not isinstance(recorded, dict) or recorded != actual:
                errors.append("code_sha256 is missing or stale; rerun applicable tests and capture final fingerprints")
        except (OSError, ValueError) as exc:
            errors.append(f"Source fingerprints: {exc}")
    return errors


def check(snapshot: Snapshot, *, record_paths: list[str] | None = None,
          complete: bool = False) -> list[str]:
    changed = snapshot.changed()
    selected = record_paths if record_paths is not None else sorted(p for p in changed if is_record(p))
    errors: list[str] = []
    covered: set[str] = set()
    count = 0
    for path in selected:
        try:
            if not is_record(path):
                raise ValueError("Select a JSON record directly under docs/changes/")
            record = json.loads(snapshot.read(path))
            count += 1
            problems = validate_record(record, snapshot, complete=complete)
            if isinstance(record, dict) and record.get("id") != Path(path).stem:
                problems.append("Record id must match its filename")
            errors.extend(f"{path}: {message}" for message in problems)
            if not problems:
                covered.update(record["code_paths"])
        except FileNotFoundError as exc:
            if record_paths is not None:
                errors.append(f"{path}: {exc}")
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: {exc}")
    if complete and not count:
        errors.append("Completion needs at least one selected change record")
    if record_paths is None:
        for path in sorted(p for p in changed if is_implementation(p) and p not in covered):
            errors.append(f"No changed ready SDD record covers implementation: {path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    snapshot_args = parser.add_mutually_exclusive_group()
    snapshot_args.add_argument("--staged", action="store_true", help="Read only the Git index")
    snapshot_args.add_argument("--base", help="Compare against this commit; fail if it does not resolve")
    parser.add_argument("--record", action="append", help="Validate only this change record (repeatable)")
    output_args = parser.add_mutually_exclusive_group()
    output_args.add_argument("--complete", action="store_true", help="Require fresh passing completion evidence")
    output_args.add_argument("--fingerprints", action="store_true", help="Print code_sha256 for one record; does not validate readiness")
    args = parser.parse_args()
    try:
        snapshot = Snapshot(Path.cwd(), staged=args.staged, base=args.base)
        if args.fingerprints:
            if not args.record or len(args.record) != 1 or not is_record(args.record[0]):
                raise ValueError("--fingerprints requires exactly one --record under docs/changes/")
            record = json.loads(snapshot.read(args.record[0]))
            if not isinstance(record, dict):
                raise ValueError("Record must be an object")
            print(json.dumps(fingerprints(record, snapshot), indent=2, sort_keys=True))
            return 0
        errors = check(snapshot, record_paths=args.record, complete=args.complete)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        print("SDD guard failed:", file=sys.stderr)
        for message in errors:
            print(f"- {message}", file=sys.stderr)
        return 1
    print("SDD records passed structural checks. This is not S70 system or vehicle qualification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
