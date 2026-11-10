"""Atomic repository files and a per-checkout mutex; no remote operations."""

import json
import os
import socket
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path


class StateError(ValueError):
    pass


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _replace_with_retry(source, target):
    for attempt in range(5):
        try:
            os.replace(source, target)
            return
        except PermissionError as error:
            # Windows scanners/readers may briefly hold a sharing lock. Do not
            # change ACLs or protections; persistent failures remain errors.
            if getattr(error, "winerror", None) not in {5, 32, 33} or attempt == 4:
                raise
            time.sleep(0.05 * (2**attempt))


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        _replace_with_retry(temp, path)
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
        raise StateError(
            f"Registry locked: {path}. Inspect owner/process; no automatic takeover."
        ) from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "host": socket.gethostname()}, stream)
        yield
    finally:
        path.unlink()
