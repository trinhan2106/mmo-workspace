import copy
from pathlib import Path
import sys
import shutil
import unittest
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import project
import github_sync


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        temp_root = project.ROOT / ".work/tests"
        temp_root.mkdir(parents=True, exist_ok=True)
        # Windows sandbox identities can lose access to mkdir(mode=0700) used by
        # TemporaryDirectory. Inherit the workspace ACL for fixture directories.
        self.root = temp_root / ("case-" + uuid.uuid4().hex)
        self.root.mkdir()
        def cleanup():
            if not self.root.resolve().is_relative_to(temp_root.resolve()):
                raise RuntimeError("Fixture cleanup target escaped test workspace")
            shutil.rmtree(self.root)
        self.addCleanup(cleanup)
        for name in ("specs/001-test/spec.md", "specs/001-test/plan.md", "docs/handoffs/T001.md"):
            project.write_text(self.root / name, "# Fixture\nFR-001: acceptance evidence\n")
        task = {"id": "T001", "title": "First", "status": "todo", "depends_on": [],
                "spec": "specs/001-test/spec.md", "plan": "specs/001-test/plan.md",
                "requirements": ["FR-001"], "acceptance": ["Fixture passes"]}
        second = dict(copy.deepcopy(task), id="T002", title="Second", depends_on=["T001"])
        self.state = {"schema_version": 1, "revision": 1, "tasks": [task, second]}

    def start(self, task="T001", state=None, **kwargs):
        return project.transition(state or self.state, self.root, "start", task,
                                  owner="chat-a", branch="feature-a", revision=1, **kwargs)

    def test_dependency_order_and_completion_select_next(self):
        self.assertEqual(project.next_task(self.state)["id"], "T001")
        state = self.start()
        state = project.transition(state, self.root, "complete", "T001", owner="chat-a", branch="feature-a",
                                   evidence="docs/handoffs/T001.md", checks="fixture: passed", summary="Implemented")
        self.assertEqual(state["revision"], 3)
        self.assertEqual(project.next_task(state)["id"], "T002")
        self.assertEqual(self.state["revision"], 1)

    def test_start_rejects_stale_prompt(self):
        with self.assertRaisesRegex(project.StateError, "Stale"):
            project.transition(self.state, self.root, "start", "T001", owner="chat", branch="x", revision=0)

    def test_start_rejects_unfinished_dependencies(self):
        with self.assertRaisesRegex(project.StateError, "not ready"):
            self.start("T002")

    def test_second_chat_cannot_claim_or_complete_first(self):
        state = self.start()
        with self.assertRaisesRegex(project.StateError, "active"):
            project.transition(state, self.root, "start", "T002", owner="chat-b", branch="x", revision=2)
        with self.assertRaisesRegex(project.StateError, "mismatch"):
            project.transition(state, self.root, "complete", "T001", owner="chat-b", branch="feature-a")

    def test_wrong_branch_cannot_complete(self):
        with self.assertRaisesRegex(project.StateError, "mismatch"):
            project.transition(self.start(), self.root, "complete", "T001", owner="chat-a", branch="different")

    def test_completion_requires_real_evidence_and_checks(self):
        for fields in ({"evidence": "missing.md", "checks": "passed", "summary": "done"},
                       {"evidence": "docs/handoffs/T001.md", "checks": "", "summary": "done"}):
            with self.assertRaises(project.StateError):
                project.transition(self.start(), self.root, "complete", "T001", owner="chat-a", branch="feature-a", **fields)

    def test_duplicate_missing_and_cycle_are_rejected(self):
        bad_states = []
        bad = copy.deepcopy(self.state)
        bad["tasks"].append(copy.deepcopy(bad["tasks"][0]))
        bad_states.append(bad)
        for deps in (["T999"], ["T002"]):
            bad = copy.deepcopy(self.state)
            bad["tasks"][0]["depends_on"] = deps
            bad_states.append(bad)
        for bad in bad_states:
            with self.assertRaises(project.StateError):
                project.validate(bad, self.root)

    def test_blocked_handoff_and_resume(self):
        state = project.transition(self.start(), self.root, "block", "T001", owner="chat-a", branch="feature-a",
                                   reason="SDK missing", next_action="Operator installs SDK")
        self.assertIsNone(project.next_task(state))
        self.assertIn("SDK missing", project.artifacts(state)["docs/handoffs/NEXT.md"])
        state = project.transition(state, self.root, "resume", "T001", revision=3)
        self.assertEqual(project.next_task(state)["id"], "T001")
        self.assertNotIn("owner", state["tasks"][0])

    def test_active_handoff_keeps_owner_and_task(self):
        text = project.artifacts(self.start())["docs/handoffs/NEXT.md"]
        self.assertIn("owner chat-a", text)
        self.assertIn("Task dự kiến: T001", text)

    def test_render_check_detects_drift_and_recovers(self):
        project.render(self.state, self.root)
        project.check_artifacts(self.state, self.root)
        project.write_text(self.root / "docs/handoffs/NEXT.md", "stale prompt")
        with self.assertRaisesRegex(project.StateError, "drift"):
            project.check_artifacts(self.state, self.root)
        project.render(self.state, self.root)
        project.check_artifacts(self.state, self.root)

    def test_mutex_refuses_overlapping_writer(self):
        with project.mutex(self.root):
            with self.assertRaisesRegex(project.StateError, "locked"):
                with project.mutex(self.root):
                    self.fail("second writer acquired lock")
        self.assertFalse((self.root / ".work/registry.lock").exists())

    def test_mutex_cleanup_on_error(self):
        with self.assertRaises(RuntimeError):
            with project.mutex(self.root):
                raise RuntimeError("fixture")
        self.assertFalse((self.root / ".work/registry.lock").exists())

    def test_paths_cannot_escape_repository(self):
        bad = copy.deepcopy(self.state)
        bad["tasks"][0]["spec"] = "../private.md"
        with self.assertRaisesRegex(project.StateError, "escapes"):
            project.validate(bad, self.root)

    def test_add_task_retains_stable_ids_and_checks_revision(self):
        new = dict(copy.deepcopy(self.state["tasks"][1]), id="T003", depends_on=["T002"])
        state = project.add_task(self.state, new, self.root, 1)
        self.assertEqual([t["id"] for t in state["tasks"]], ["T001", "T002", "T003"])
        with self.assertRaisesRegex(project.StateError, "duplicate"):
            project.add_task(self.state, self.state["tasks"][0], self.root, 1)
        with self.assertRaisesRegex(project.StateError, "Stale"):
            project.add_task(self.state, new, self.root, 0)


class RemoteIdentityTests(unittest.TestCase):
    def test_closed_issues_still_deduplicated(self):
        issue = {"number": 1, "state": "closed", "title": "[T001] Done", "body": ""}
        self.assertEqual(github_sync.index_issues([issue])["T001"]["number"], 1)

    def test_duplicate_remote_ids_stop_sync(self):
        with self.assertRaisesRegex(project.StateError, "Duplicate"):
            github_sync.index_issues([{"number": n, "title": "[T001] Same", "body": ""} for n in (1, 2)])

    def test_conflicting_title_marker_stop_sync(self):
        with self.assertRaisesRegex(project.StateError, "conflicting"):
            github_sync.index_issues([{"number": 1, "title": "[T001] A", "body": "<!-- mmo-workspace-task:T002 -->"}])

    def test_pull_requests_and_references_do_not_become_tasks(self):
        self.assertEqual(github_sync.index_issues([{"number": 1, "title": "Discuss T001", "body": "depends on T002"},
                                                 {"number": 2, "title": "[T001] PR", "pull_request": {}}]), {})

    def test_ids_above_999_supported(self):
        index = github_sync.index_issues([{"number": 1, "title": "[T1000] A", "body": ""}])
        self.assertIn("T1000", index)
        self.assertNotIn("T100", index)

    def test_notes_outside_managed_section_preserved(self):
        new = github_sync.BEGIN + "\nnew\n" + github_sync.END
        old = "human note\n" + github_sync.BEGIN + "\nold\n" + github_sync.END + "\nkeep this"
        self.assertEqual(github_sync.replace_managed(old, new), "human note\n" + new + "\nkeep this")
        with self.assertRaises(project.StateError):
            github_sync.replace_managed(github_sync.BEGIN, new)

    def test_remote_is_strictly_scoped(self):
        github_sync.verify_remote("https://github.com/trinhan2106/mmo-workspace.git", github_sync.REPOSITORY)
        for remote in ("https://github.com/other/repo.git", "https://evil.example/trinhan2106/mmo-workspace.git"):
            with self.assertRaises(project.StateError):
                github_sync.verify_remote(remote, github_sync.REPOSITORY)


if __name__ == "__main__":
    unittest.main()
