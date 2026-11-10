"""Repository-local task lifecycle. Python stdlib only; no account/runtime actions."""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
STATE = Path("project/tasks.json")
STATUSES = {"todo", "in_progress", "blocked", "review", "done"}
ACTIVE = {"in_progress", "review"}


class StateError(ValueError):
    pass


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


@contextmanager
def mutex(root):
    path = root / ".work/registry.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise StateError(f"Registry locked: {path}. Inspect owner/process; no automatic takeover.") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "host": socket.gethostname()}, stream)
        yield
    finally:
        path.unlink()


def local_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise StateError("Expected a non-empty repository-relative path")
    path = (root / value).resolve()
    if Path(value).is_absolute() or not path.is_relative_to(root.resolve()):
        raise StateError(f"Path escapes repository: {value}")
    if not path.is_file():
        raise StateError(f"Missing file: {value}")
    return path


def validate(state, root):
    if state.get("schema_version") != 1 or type(state.get("revision")) is not int or state["revision"] < 1:
        raise StateError("Invalid schema_version/revision")
    tasks = state.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise StateError("Registry must contain tasks")
    ids = [t.get("id") for t in tasks]
    if any(not isinstance(i, str) or not re.fullmatch(r"T\d{3,}", i) for i in ids) or len(set(ids)) != len(ids):
        raise StateError("Invalid or duplicate task IDs")
    by_id = {t["id"]: t for t in tasks}
    if sum(t.get("status") in ACTIVE for t in tasks) > 1:
        raise StateError("Only one active task per checkout")
    for task in tasks:
        task_id = task["id"]
        if task.get("status") not in STATUSES or not str(task.get("title", "")).strip():
            raise StateError(f"{task_id}: invalid title/status")
        for field in ("spec", "plan"):
            local_file(root, task.get(field))
        for field in ("acceptance", "requirements"):
            if not isinstance(task.get(field), list) or not task[field] or any(not isinstance(s, str) or not s.strip() for s in task[field]):
                raise StateError(f"{task_id}: {field} must be non-empty strings")
        spec_text = local_file(root, task["spec"]).read_text(encoding="utf-8-sig")
        if any(not re.search(r"\b" + re.escape(req) + r"\b", spec_text) for req in task["requirements"]):
            raise StateError(f"{task_id}: requirement missing from linked spec")
        deps = task.get("depends_on")
        if not isinstance(deps, list) or any(not isinstance(d, str) or d not in by_id for d in deps) or len(deps) != len(set(deps)) or task_id in deps:
            raise StateError(f"{task_id}: invalid dependencies")
        if task["status"] in ACTIVE | {"done"} and any(by_id[d]["status"] != "done" for d in deps):
            raise StateError(f"{task_id}: unfinished dependency")
        if task["status"] in ACTIVE and (not task.get("owner") or not task.get("branch")):
            raise StateError(f"{task_id}: active task needs owner and branch")
        if task["status"] == "blocked" and (not task.get("blocked_reason") or not task.get("next_action")):
            raise StateError(f"{task_id}: blocker needs reason and next_action")
        if task["status"] == "done":
            evidence = local_file(root, task.get("evidence"))
            if evidence.suffix != ".md" or not evidence.read_text(encoding="utf-8-sig").strip() or not task.get("checks") or not task.get("summary"):
                raise StateError(f"{task_id}: done requires Markdown evidence, checks and summary")
    visited, visiting = set(), set()

    def visit(task_id):
        if task_id in visiting:
            raise StateError(f"Dependency cycle at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dep in by_id[task_id]["depends_on"]:
            visit(dep)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        visit(task_id)
    return by_id


def ready_tasks(state):
    by_id = {t["id"]: t for t in state["tasks"]}
    return [t for t in state["tasks"] if t["status"] == "todo" and all(by_id[d]["status"] == "done" for d in t["depends_on"])]


def next_task(state):
    return next((t for t in state["tasks"] if t["status"] in ACTIVE), None) or next(iter(ready_tasks(state)), None)


def lifecycle(task, state):
    names = {"todo": "Todo", "in_progress": "In progress", "review": "Review", "blocked": "Blocked", "done": "Done"}
    return "Ready" if task in ready_tasks(state) else names[task["status"]]


def artifacts(state):
    result = {}
    for spec in sorted({t["spec"] for t in state["tasks"]}):
        lines = ["# Tasks — generated from project/tasks.json", "", f"Registry revision: {state['revision']}. Do not edit this checklist directly.", ""]
        for task in (t for t in state["tasks"] if t["spec"] == spec):
            lines += [f"- [{'x' if task['status'] == 'done' else ' '}] {task['id']} {task['title']}",
                      f"  - State: {lifecycle(task, state)}; dependencies: {', '.join(task['depends_on']) or 'none'}; requirements: {', '.join(task['requirements'])}"]
            lines += [f"  - Acceptance: {item}" for item in task["acceptance"]]
            if task.get("evidence"):
                lines.append(f"  - Evidence: `{task['evidence']}`")
            if task["status"] == "blocked":
                lines.append(f"  - Blocker: {task['blocked_reason']}; next: {task['next_action']}")
        result[str(Path(spec).with_name("tasks.md")).replace("\\", "/")] = "\n".join(lines) + "\n"
    task = next_task(state)
    lines = ["# Prompt cho chat kế tiếp", "", f"Registry revision: {state['revision']}. Sinh tự động; đọc lại state trước khi làm.", "", "```text",
             "Tiếp tục dự án tại D:/MMO-Plus-UPI/mmo-workspace. Đọc AGENTS.md và docs/START-HERE.md; dùng skill workspace-handoff.",
             "Chạy py -3.12 scripts/project.py status và đối chiếu registry hiện tại. Prompt cũ không thay trạng thái mới."]
    if task:
        lines += [f"Task dự kiến: {task['id']} — {task['title']}. Đọc {task['spec']} và {task['plan']}, acceptance trong registry và docs/handoffs/{task['id']}.md nếu có."]
        if task["status"] in ACTIVE:
            lines += [f"Task đang {task['status']}, owner {task['owner']}, branch {task['branch']}. Đây là bàn giao tiếp tục task dở; không claim task khác hoặc chiếm owner không rõ tình trạng."]
        else:
            lines += [f"Nếu {task['id']} vẫn ready và chưa có task active, chọn branch phù hợp rồi claim bằng project.py start {task['id']} --owner <nhãn-chat-mới> --revision <revision-vừa-đọc>."]
        lines += ["Chỉ làm task này, kiểm tra đúng phạm vi, cập nhật evidence/registry. Chạy render/check và sync GitHub khi có quyền; cuối chat trả prompt mới từ docs/handoffs/NEXT.md."]
    else:
        pending = [t for t in state["tasks"] if t["status"] != "done"]
        if pending:
            lines += ["Không có task sẵn sàng. Đọc blockers/dependencies, báo điều kiện cần giải quyết; không tự đánh dấu done hoặc chiếm task."]
            lines += [f"{t['id']}: {t.get('blocked_reason', 'waiting for dependencies')} — {t.get('next_action', 'check dependency graph')}" for t in pending]
        else:
            lines += ["Toàn bộ task hiện tại đã xong. Báo kết quả và chờ yêu cầu mới; không tự tạo phạm vi tiếp theo."]
    result["docs/handoffs/NEXT.md"] = "\n".join(lines + ["```", ""])
    return result


def render(state, root):
    for path, content in artifacts(state).items():
        write_text(root / path, content)
    task = next_task(state)
    if task and (root / ".specify").is_dir():
        write_json(root / ".specify/feature.json", {"feature_directory": Path(task["spec"]).parent.as_posix()})


def check_artifacts(state, root):
    for path, content in artifacts(state).items():
        if not (root / path).is_file() or (root / path).read_text(encoding="utf-8") != content:
            raise StateError(f"Generated artifact drift: {path}; run project.py render")


def transition(state, root, action, task_id, *, revision=None, owner=None, branch=None, **fields):
    validate(state, root)
    if revision is not None and revision != state["revision"]:
        raise StateError(f"Stale revision {revision}; current is {state['revision']}")
    result = copy.deepcopy(state)
    task = next((t for t in result["tasks"] if t["id"] == task_id), None)
    if task is None:
        raise StateError(f"Unknown task: {task_id}")
    if action == "start":
        if any(t["status"] in ACTIVE for t in result["tasks"]) or task not in ready_tasks(result):
            raise StateError("Task not ready or another task is active")
        if not owner or not branch:
            raise StateError("Owner and branch required")
        task.update(status="in_progress", owner=owner, branch=branch)
    elif action in {"complete", "block"}:
        if task["status"] not in ACTIVE or task["owner"] != owner or task["branch"] != branch:
            raise StateError("Active task owner/branch mismatch")
        if action == "complete":
            task.update(status="done", **{key: fields.get(key) for key in ("evidence", "checks", "summary")})
        else:
            task.update(status="blocked", blocked_reason=fields.get("reason"), next_action=fields.get("next_action"))
    elif action == "resume":
        if task["status"] != "blocked":
            raise StateError("Only a blocked task can be resumed")
        task["status"] = "todo"
        for key in ("owner", "branch", "blocked_reason", "next_action"):
            task.pop(key, None)
    else:
        raise StateError(f"Unknown action {action}")
    result["revision"] += 1
    validate(result, root)
    return result


def add_task(state, task, root, revision):
    if revision != state["revision"]:
        raise StateError("Stale revision")
    if task.get("status") != "todo":
        raise StateError("New task must start as todo")
    existing = {t["id"] for t in state["tasks"]}
    if task.get("id") in existing:
        raise StateError("Invalid or duplicate task IDs")
    expected_id = f"T{max(int(i[1:]) for i in existing) + 1:03d}"
    if task.get("id") != expected_id:
        raise StateError(f"Next stable ID must be {expected_id}")
    result = copy.deepcopy(state)
    result["tasks"].append(task)
    result["revision"] += 1
    validate(result, root)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "check", "render"):
        sub.add_parser(command)
    for command in ("start", "complete", "block", "resume"):
        cmd = sub.add_parser(command)
        cmd.add_argument("task_id")
        if command in {"start", "resume"}:
            cmd.add_argument("--revision", type=int, required=True)
        if command != "resume":
            cmd.add_argument("--owner", required=True)
        for field in ({"complete": ("evidence", "checks", "summary"), "block": ("reason", "next-action")}.get(command, ())):
            cmd.add_argument("--" + field, required=True)
    cmd = sub.add_parser("add")
    cmd.add_argument("--file", required=True)
    cmd.add_argument("--revision", type=int, required=True)
    args = parser.parse_args()
    with mutex(ROOT):
        state = load_json(ROOT / STATE)
        validate(state, ROOT)
        if args.command == "check":
            check_artifacts(state, ROOT)
            print(f"OK: {len(state['tasks'])} tasks, revision {state['revision']}; artifacts consistent")
        elif args.command == "status":
            print(f"Revision: {state['revision']}")
            for task in state["tasks"]:
                print(f"{task['id']} [{lifecycle(task, state)}] {task['title']}" + (f" | owner={task['owner']} branch={task['branch']}" if task["status"] in ACTIVE else ""))
            task = next_task(state)
            print(f"Next: {task['id'] if task else 'none; inspect blockers/completion'}")
        elif args.command == "render":
            render(state, ROOT)
            print("Generated checklist(s) and NEXT.md")
        else:
            if args.command == "add":
                state = add_task(state, load_json(ROOT / args.file), ROOT, args.revision)
            else:
                branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
                if not branch:
                    raise StateError("Detached HEAD: select an appropriate branch first")
                fields = vars(args).copy()
                action, task_id = fields.pop("command"), fields.pop("task_id")
                state = transition(state, ROOT, action, task_id, branch=branch, **fields)
            write_json(ROOT / STATE, state)
            render(state, ROOT)
            print(f"Saved revision {state['revision']}; artifacts rendered")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (StateError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
