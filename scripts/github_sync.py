"""Idempotent GitHub issue/project mirror. Dry run unless --apply is supplied."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

import project

REPOSITORY = "trinhan2106/mmo-workspace"
MARKER = re.compile(r"<!-- mmo-workspace-task:(T\d{3,}) -->")
BEGIN = "<!-- mmo-workspace-managed:start -->"
END = "<!-- mmo-workspace-managed:end -->"


def gh(*args, payload=None, parse=True):
    proc = subprocess.run(
        ["gh", *map(str, args)],
        cwd=project.ROOT,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    if proc.returncode:
        raise project.StateError(
            f"gh {args[0]} failed (exit {proc.returncode}); inspect gh authentication/network permissions. No blind retry performed."
        )
    return json.loads(proc.stdout) if parse and proc.stdout.strip() else proc.stdout.strip()


def verify_remote(remote, expected):
    allowed = {
        f"https://github.com/{expected}",
        f"https://github.com/{expected}.git",
        f"git@github.com:{expected}.git",
        f"ssh://git@github.com/{expected}.git",
    }
    if expected != REPOSITORY or remote.strip() not in allowed:
        raise project.StateError("Remote/config does not match this project's GitHub repository")


def index_issues(issues):
    result = {}
    for issue in issues:
        if "pull_request" in issue:
            continue
        ids = set(MARKER.findall(issue.get("body") or ""))
        title = re.match(r"^(?:\[)?(T\d{3,})(?:\]|:|\s)", issue.get("title", ""))
        if title:
            ids.add(title[1])
        if len(ids) > 1:
            raise project.StateError(f"Issue #{issue['number']} has conflicting task identities")
        for task_id in ids:
            if task_id in result:
                raise project.StateError(
                    f"Duplicate remote task {task_id}; reconcile instead of creating more issues"
                )
            result[task_id] = issue
    return result


def managed_body(task, state):
    source = f"https://github.com/{REPOSITORY}/blob/main/"
    lines = [
        BEGIN,
        f"<!-- mmo-workspace-task:{task['id']} -->",
        "This issue mirrors `project/tasks.json`. Change lifecycle in the repository and run the sync script.",
        "",
        f"**Lifecycle:** {project.lifecycle(task, state)}",
        f"**Dependencies:** {', '.join(task['depends_on']) or 'None'}",
        f"**Requirements:** {', '.join(task['requirements'])}",
        f"**Specification:** [spec]({source}{task['spec']}) · [plan]({source}{task['plan']})",
        "",
        "Acceptance criteria:",
    ]
    lines += [
        f"- [{'x' if task['status'] == 'done' else ' '}] {item}" for item in task["acceptance"]
    ]
    if task["status"] in project.ACTIVE:
        lines += ["", f"**Claim:** `{task['owner']}` on `{task['branch']}`"]
    if task["status"] == "blocked":
        lines += [
            "",
            f"**Blocked:** {task['blocked_reason']}",
            f"**Next action:** {task['next_action']}",
        ]
    if task.get("evidence"):
        lines += ["", f"**Evidence:** [{task['evidence']}]({source}{task['evidence']})"]
    if task.get("checks"):
        lines += [f"**Checks:** {task['checks']}"]
    if task.get("summary"):
        lines += [f"**Outcome:** {task['summary']}"]
    return "\n".join(lines + [END])


def replace_managed(old, new):
    old = old or ""
    if BEGIN not in old and END not in old:
        return new + ("\n\n" + old if old.strip() else "")
    if old.count(BEGIN) != 1 or old.count(END) != 1 or old.index(BEGIN) >= old.index(END):
        raise project.StateError("Invalid managed issue-body markers; refusing to overwrite notes")
    start, end = old.index(BEGIN), old.index(END) + len(END)
    return old[:start] + new + old[end:]


def sync(apply=False):
    root = project.ROOT
    with project.mutex(root):
        state = project.load_json(root / project.STATE)
        project.validate(state, root)
        project.check_artifacts(state, root)
        config = project.load_json(root / "project/github.json")
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=root, text=True
        ).strip()
        verify_remote(remote, config["repository"])
        board = config["project"]
        live_board = gh(
            "project", "view", board["number"], "--owner", board["owner"], "--format", "json"
        )
        if live_board["id"] != board["id"]:
            raise project.StateError("Project identity mismatch")
        pages = gh(
            "api", "--paginate", "--slurp", f"repos/{REPOSITORY}/issues?state=all&per_page=100"
        )
        remote_issues = index_issues([issue for page in pages for issue in page])
        fields = gh(
            "project",
            "field-list",
            board["number"],
            "--owner",
            board["owner"],
            "--format",
            "json",
            "--limit",
            "100",
        )["fields"]
        field_map = {f["name"]: f for f in fields}
        for name, options in {
            "Lifecycle": {"Todo", "Ready", "In progress", "Blocked", "Review", "Done"},
            "Status": {"Todo", "In Progress", "Done"},
        }.items():
            if name not in field_map or not options.issubset(
                {o["name"] for o in field_map[name].get("options", [])}
            ):
                raise project.StateError(f"Project field {name} missing expected options")
        items = gh(
            "project",
            "item-list",
            board["number"],
            "--owner",
            board["owner"],
            "--format",
            "json",
            "--limit",
            "10000",
        )
        if len(items["items"]) < items["totalCount"]:
            raise project.StateError("Project items truncated; increase pagination before syncing")
        item_map = {}
        for item in items["items"]:
            url = item.get("content", {}).get("url")
            if url:
                if url in item_map:
                    raise project.StateError("Duplicate project item for the same issue")
                item_map[url] = item
        changes = 0
        for task in state["tasks"]:
            issue = remote_issues.get(task["id"])
            saved = config["tasks"].get(task["id"])
            if saved and (not issue or issue["number"] != saved["issue_number"]):
                raise project.StateError(
                    f"{task['id']}: saved/remote identity mismatch; manual reconciliation required"
                )
            title = f"[{task['id']}] {task['title']}"
            body = replace_managed(issue.get("body") if issue else "", managed_body(task, state))
            desired_state = "closed" if task["status"] == "done" else "open"
            operations = []
            if issue is None:
                operations.append("create issue")
                if apply:
                    issue = gh(
                        "api",
                        f"repos/{REPOSITORY}/issues",
                        "--input",
                        "-",
                        payload={"title": title, "body": body},
                    )
            elif (
                issue["title"] != title
                or (issue.get("body") or "") != body
                or issue["state"] != desired_state
            ):
                operations.append("update issue")
                if apply:
                    issue = gh(
                        "api",
                        "--method",
                        "PATCH",
                        f"repos/{REPOSITORY}/issues/{issue['number']}",
                        "--input",
                        "-",
                        payload={"title": title, "body": body, "state": desired_state},
                    )
            if apply and issue["state"] != desired_state:
                issue = gh(
                    "api",
                    "--method",
                    "PATCH",
                    f"repos/{REPOSITORY}/issues/{issue['number']}",
                    "--input",
                    "-",
                    payload={"state": desired_state},
                )
            url = issue["html_url"] if issue else None
            item = item_map.get(url)
            if item is None:
                operations.append("add project item")
                if apply:
                    item = gh(
                        "project",
                        "item-add",
                        board["number"],
                        "--owner",
                        board["owner"],
                        "--url",
                        url,
                        "--format",
                        "json",
                    )
            status = (
                "Done"
                if task["status"] == "done"
                else "In Progress"
                if task["status"] in project.ACTIVE
                else "Todo"
            )
            for name, value, current_key in (
                ("Lifecycle", project.lifecycle(task, state), "lifecycle"),
                ("Status", status, "status"),
            ):
                if item and item.get(current_key) == value:
                    continue
                operations.append(f"{name}={value}")
                if apply:
                    field = field_map[name]
                    option = next(o["id"] for o in field["options"] if o["name"] == value)
                    gh(
                        "project",
                        "item-edit",
                        "--id",
                        item["id"],
                        "--project-id",
                        board["id"],
                        "--field-id",
                        field["id"],
                        "--single-select-option-id",
                        option,
                        parse=False,
                    )
            if operations:
                changes += 1
            print(
                f"{task['id']}: {', '.join(operations) if operations else 'unchanged'}", flush=True
            )
            if apply:
                mapping = {
                    "issue_number": issue["number"],
                    "url": url,
                    "item_id": item["id"],
                }
                if config["tasks"].get(task["id"]) != mapping:
                    config["tasks"][task["id"]] = mapping
                    project.write_json(root / "project/github.json", config)
        if apply:
            config["last_sync"] = datetime.now(timezone.utc).isoformat()
            config["synced_revision"] = state["revision"]
            project.write_json(root / "project/github.json", config)
        print(
            f"{'Applied' if apply else 'Dry run'}: {len(state['tasks'])} tasks, {changes} with pending changes"
        )


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        sync(args.apply)
    except (project.StateError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
