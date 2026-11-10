"""Fetch one catalogued source checkout at its pinned commit; never execute it."""

import argparse
import re
import subprocess
import sys

import project


def fetch(name):
    entries = project.load_json(project.ROOT / "references/manifest.json")["repositories"]
    entry = next((e for e in entries if e["name"] == name), None)
    if entry is None or not re.fullmatch(r"[a-z0-9-]+", name):
        raise project.StateError("Choose a name from references/manifest.json")
    repo, commit = entry["repository"], entry["commit"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo) or not re.fullmatch(
        r"[0-9a-f]{40}", commit
    ):
        raise project.StateError("Invalid repository/commit in manifest")
    dest = project.ROOT / ".reference" / name
    if dest.exists():
        actual = subprocess.check_output(
            ["git", "-C", str(dest), "rev-parse", "HEAD"], text=True
        ).strip()
        if actual != commit:
            raise project.StateError(
                "Existing checkout differs from pin; preserve it and reconcile manually"
            )
        print(f"{name}: pinned checkout already available")
        return
    dest.mkdir(parents=True)
    # Disable repository hooks for these operations; do not recurse submodules or install code.
    subprocess.run(
        ["git", "-c", "core.hooksPath=", "init", str(dest)], check=True, capture_output=True
    )
    subprocess.run(
        ["git", "-C", str(dest), "remote", "add", "origin", f"https://github.com/{repo}.git"],
        check=True,
    )
    subprocess.run(
        [
            "git",
            "-C",
            str(dest),
            "-c",
            "core.hooksPath=",
            "fetch",
            "--depth",
            "1",
            "origin",
            commit,
        ],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(dest), "-c", "core.hooksPath=", "checkout", "--detach", "FETCH_HEAD"],
        check=True,
        capture_output=True,
    )
    print(f"{name}: downloaded {commit}; not executed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    args = parser.parse_args()
    try:
        fetch(args.name)
    except (project.StateError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
