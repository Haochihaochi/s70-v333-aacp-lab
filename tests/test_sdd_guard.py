"""Behavioral cases G01–G10, specified in docs/changes/SDD-0001.md first."""

import copy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from sdd_guard import Snapshot, check, fingerprints, validate_record  # noqa: E402


class SddGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.write("docs/spec.md", "# Design\nREQ-1: Reject invalid inputs.\n")
        self.write("tools/feature.py", "value = 1\n")
        self.write("tests/test_feature.py", "# Observable behavior tests\n")
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()
        self.record_path = "docs/changes/SDD-TEST.json"
        self.record = {
            "schema_version": 1,
            "id": "SDD-TEST",
            "status": "ready",
            "scope": "tooling",
            "requirements": ["REQ-1"],
            "specifications": dict.fromkeys(
                ("requirements", "product", "technical"), "docs/spec.md"
            ),
            "code_paths": ["tools/feature.py"],
            "review": {"by": "Test reviewer", "basis": "Design and cases reviewed"},
            "tests": [{
                "id": "T1", "requirements": ["REQ-1"], "level": "host",
                "kind": "automated", "test_file": "tests/test_feature.py",
                "procedure": "Run rejection and valid input tests",
                "expected": "Invalid input is rejected without a write",
                "result": "planned", "evidence": None,
            }],
            "code_sha256": {},
        }

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.root), *args], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout

    def write(self, path, content):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding="utf-8", newline="")

    def commit(self):
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "-qm", "Test fixture")

    def save_record(self):
        self.write(self.record_path, json.dumps(self.record))

    def complete_record(self):
        self.record["status"] = "complete"
        self.write("docs/evidence.md", "Observed host test PASS; no vehicle qualification.\n")
        self.record["tests"][0].update(result="pass", evidence="docs/evidence.md")
        self.record["code_sha256"] = fingerprints(self.record, Snapshot(self.root))
        self.save_record()

    def test_documentation_only_needs_no_record(self):
        self.write("docs/research.md", "Read-only finding\n")
        self.assertEqual(check(Snapshot(self.root)), [])

    def test_code_without_record_is_rejected(self):
        self.write("tools/feature.py", "value = 2\n")
        self.assertIn("tools/feature.py", "\n".join(check(Snapshot(self.root))))

    def test_untracked_new_language_and_ci_are_covered(self):
        for path in ("app/main.rs", "config/target.env", ".github/workflows/build.yml"):
            self.write(path, "new behavior\n")
        errors = "\n".join(check(Snapshot(self.root)))
        for path in ("app/main.rs", "config/target.env", ".github/workflows/build.yml"):
            self.assertIn(path, errors)

    def test_ready_record_covers_changed_code(self):
        self.write("tools/feature.py", "value = 2\n")
        self.save_record()
        self.assertEqual(check(Snapshot(self.root)), [])

    def test_draft_or_missing_spec_cannot_cover_code(self):
        self.write("tools/feature.py", "value = 2\n")
        for field, value in (("status", "draft"), ("specifications", {})):
            candidate = copy.deepcopy(self.record)
            candidate[field] = value
            self.assertTrue(validate_record(candidate, Snapshot(self.root)))

    def test_review_and_test_mapping_are_required(self):
        for mutate in (
            lambda r: r.update(review={}),
            lambda r: r.update(requirements=["REQ-1", "REQ-2"]),
            lambda r: r["tests"][0].update(requirements=["UNKNOWN"]),
            lambda r: r["tests"][0].update(expected=""),
            lambda r: r.update(tests=[]),
        ):
            candidate = copy.deepcopy(self.record)
            mutate(candidate)
            self.assertTrue(validate_record(candidate, Snapshot(self.root)))

    def test_requirement_must_exist_in_source_spec(self):
        self.write("docs/spec.md", "An unrelated design\n")
        self.assertTrue(validate_record(self.record, Snapshot(self.root)))

    def test_completion_requires_pass_evidence_and_real_automated_tests(self):
        self.complete_record()
        self.assertEqual(validate_record(self.record, Snapshot(self.root), complete=True), [])
        for mutate in (
            lambda r: r["tests"][0].update(result="planned"),
            lambda r: r["tests"][0].update(result="blocked"),
            lambda r: r["tests"][0].update(result="fail"),
            lambda r: r["tests"][0].update(evidence=None),
            lambda r: r["tests"][0].update(test_file="tests/missing.py"),
            lambda r: r["tests"][0].update(kind="manual"),
            lambda r: r.update(code_sha256={}),
        ):
            candidate = copy.deepcopy(self.record)
            mutate(candidate)
            self.assertTrue(validate_record(candidate, Snapshot(self.root), complete=True))

    def test_fresh_complete_change_passes_and_stale_source_fails(self):
        self.write("tools/feature.py", "value = 2\n")
        self.complete_record()
        self.assertEqual(check(Snapshot(self.root), complete=True), [])
        self.write("tools/feature.py", "value = 3\n")
        self.assertTrue(check(Snapshot(self.root)))

    def test_new_test_code_must_also_be_fingerprinted(self):
        self.write("tests/test_feature.py", "# Changed test expectations\n")
        self.record["code_paths"].append("tests/test_feature.py")
        self.complete_record()
        self.write("tests/test_feature.py", "# Weakened after the test run\n")
        self.assertTrue(check(Snapshot(self.root), complete=True))

    def test_unchanged_test_file_is_bound_to_completion_evidence(self):
        self.complete_record()
        self.write("tests/test_feature.py", "# Assertions changed after evidence capture\n")
        self.assertTrue(validate_record(self.record, Snapshot(self.root), complete=True))

    def test_cli_exit_status_reports_readiness_and_invalid_base(self):
        script = Path(__file__).resolve().parents[1] / "tools/sdd_guard.py"
        self.save_record()
        for args, expected in (
            (["--record", self.record_path], 0),
            (["--complete", "--record", self.record_path], 1),
            (["--base", "nonexistent-ref"], 1),
        ):
            result = subprocess.run([sys.executable, str(script), *args], cwd=self.root,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)

    def test_deletion_and_rename_need_both_paths(self):
        (self.root / "tools/feature.py").rename(self.root / "tools/renamed.py")
        self.record["code_paths"] = ["tools/renamed.py"]
        self.save_record()
        self.assertTrue(check(Snapshot(self.root)))
        self.record["code_paths"].append("tools/feature.py")
        self.complete_record()
        self.assertEqual(self.record["code_sha256"]["tools/feature.py"], "deleted")
        self.assertEqual(check(Snapshot(self.root), complete=True), [])

    def test_nonexistent_source_is_not_a_valid_deletion(self):
        self.record["code_paths"] = ["tools/never-existed.py"]
        with self.assertRaises(ValueError):
            fingerprints(self.record, Snapshot(self.root))

    def test_staged_check_ignores_unstaged_specification(self):
        self.write("tools/feature.py", "value = 2\n")
        self.write("docs/new-spec.md", "REQ-1: Reviewed design\n")
        self.record["specifications"]["technical"] = "docs/new-spec.md"
        self.save_record()
        self.git("add", "tools/feature.py", self.record_path)
        self.assertEqual(check(Snapshot(self.root)), [])
        self.assertTrue(check(Snapshot(self.root, staged=True)))
        self.git("add", "docs/new-spec.md")
        self.assertEqual(check(Snapshot(self.root, staged=True)), [])

    def test_staged_completion_cannot_use_unstaged_evidence_or_record(self):
        self.write("tools/feature.py", "value = 2\n")
        self.save_record()
        self.git("add", ".")
        self.complete_record()
        self.assertTrue(check(Snapshot(self.root, staged=True), complete=True))
        self.git("add", self.record_path)
        self.assertTrue(check(Snapshot(self.root, staged=True), complete=True))
        self.git("add", "docs/evidence.md")
        self.assertEqual(check(Snapshot(self.root, staged=True), complete=True), [])

    def test_historical_record_cannot_cover_new_code(self):
        self.save_record()
        self.commit()
        self.write("tools/feature.py", "value = 2\n")
        self.assertTrue(check(Snapshot(self.root)))

    def test_explicit_base_covers_all_commits(self):
        self.write("tools/feature.py", "value = 2\n")
        self.commit()
        self.write("docs/comment.md", "second commit\n")
        self.commit()
        self.assertEqual(check(Snapshot(self.root)), [])
        self.assertTrue(check(Snapshot(self.root, base=self.base)))
        self.save_record()
        self.assertEqual(check(Snapshot(self.root, base=self.base)), [])

    def test_invalid_base_fails_instead_of_reducing_coverage(self):
        with self.assertRaises(ValueError):
            Snapshot(self.root, base="nonexistent-ref")

    def test_malformed_json_and_wrong_types_fail_cleanly(self):
        self.write(self.record_path, "{broken")
        self.assertTrue(check(Snapshot(self.root)))
        for field in ("requirements", "tests", "code_paths", "review", "specifications"):
            candidate = copy.deepcopy(self.record)
            candidate[field] = 42
            self.assertTrue(validate_record(candidate, Snapshot(self.root)))
        self.assertTrue(validate_record([], Snapshot(self.root)))

    def test_escaping_and_nonliteral_paths_fail(self):
        for path in ("../outside.md", "/tmp/outside.md", "C:/outside.md", "docs\\spec.md", "docs/*.md"):
            candidate = copy.deepcopy(self.record)
            candidate["specifications"]["technical"] = path
            self.assertTrue(validate_record(candidate, Snapshot(self.root)), path)

    def test_staged_symlink_is_not_evidence(self):
        result = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
            input="../outside.md", text=True, check=True, capture_output=True,
        )
        oid = result.stdout.strip()
        self.git("update-index", "--add", "--cacheinfo", f"120000,{oid},docs/link.md")
        self.record["specifications"]["technical"] = "docs/link.md"
        self.save_record()
        self.git("add", self.record_path)
        self.assertTrue(check(Snapshot(self.root, staged=True)))

    def test_complete_selection_cannot_be_empty_or_ready(self):
        self.assertTrue(check(Snapshot(self.root), complete=True))
        self.save_record()
        self.assertTrue(check(Snapshot(self.root), complete=True))

    def test_explicit_record_supports_preflight_before_source_exists(self):
        self.record["code_paths"] = ["tools/future.py"]
        self.save_record()
        self.assertEqual(check(Snapshot(self.root), record_paths=[self.record_path]), [])

    def test_lf_normalized_fingerprints_are_portable(self):
        self.write("tools/feature.py", "value = 1\r\n")
        crlf = fingerprints(self.record, Snapshot(self.root))
        self.write("tools/feature.py", "value = 1\n")
        self.assertEqual(crlf, fingerprints(self.record, Snapshot(self.root)))

    def test_submodule_pointer_fingerprints_and_dirty_completion(self):
        module = self.root / "third_party/receiver"
        module.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(module)], check=True)
        self.write("third_party/receiver/source.txt", "baseline\n")
        self.git("-C", str(module), "add", ".")
        self.git("-C", str(module), "-c", "user.name=Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm", "Fixture")
        commit = self.git("-C", str(module), "rev-parse", "HEAD").strip()
        self.git("update-index", "--add", "--cacheinfo", f"160000,{commit},third_party/receiver")
        self.record["code_paths"] = ["third_party/receiver"]
        self.assertEqual(len(fingerprints(self.record, Snapshot(self.root))["third_party/receiver"]), 64)
        self.write("third_party/receiver/source.txt", "dirty\n")
        with self.assertRaises(ValueError):
            fingerprints(self.record, Snapshot(self.root))

    def test_guard_never_runs_record_procedure(self):
        self.record["tests"][0]["procedure"] = "create sentinel.txt and modify the IHU"
        self.save_record()
        self.assertEqual(check(Snapshot(self.root)), [])
        self.assertFalse((self.root / "sentinel.txt").exists())


if __name__ == "__main__":
    unittest.main()
