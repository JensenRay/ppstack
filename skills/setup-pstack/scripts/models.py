"""Inspect and update ppstack's Pi worker preferences."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sys
import tempfile


ROLE_NAMES = (
    "feature, refactoring",
    "bug-fix",
    "perf-issue",
    "hillclimb",
    "judgment and prose",
    "arena runners",
    "arena cross-judge pool",
    "swarm workers",
    "interrogate reviewers",
)
PANEL_ROLES = {"arena runners", "arena cross-judge pool", "interrogate reviewers"}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def validate_seat(role, settings):
    if not isinstance(settings, dict) or settings.keys() != {"model", "effort"}:
        raise ValueError(f"{role!r} requires model and effort")
    for key, token in settings.items():
        if not isinstance(token, str) or not token or any(c.isspace() for c in token):
            raise ValueError(f"{role!r} {key} must be a nonempty identifier without whitespace")


def validate(data, *, patch=False):
    if not isinstance(data, dict) or data.keys() - {"roles", "max_parallel"}:
        raise ValueError("expected an object containing roles and optional max_parallel")
    if not patch and "roles" not in data:
        raise ValueError("missing roles object")
    roles = data.get("roles", {})
    if not isinstance(roles, dict):
        raise ValueError("roles must be an object")
    for role, settings in roles.items():
        if role not in ROLE_NAMES:
            raise ValueError(f"unrecognized role {role!r}")
        if patch and settings is None:
            continue
        if isinstance(settings, list):
            if role not in PANEL_ROLES or not settings:
                raise ValueError(f"{role!r} cannot use this panel list")
            for seat in settings:
                validate_seat(role, seat)
        else:
            validate_seat(role, settings)
    if "max_parallel" in data:
        limit = data["max_parallel"]
        if not (patch and limit is None) and (type(limit) is not int or limit < 1):
            raise ValueError("max_parallel must be a positive integer")
    return data


def read(path):
    try:
        with path.open(encoding="utf-8") as stream:
            return validate(json.load(stream, object_pairs_hook=unique_keys))
    except FileNotFoundError:
        return {"roles": {}}


@contextmanager
def edit_lock(path):
    # Keep the lock outside models.json: atomic replacement changes its inode.
    with path.with_name(".models.lock").open("a+b") as lock:
        if os.name == "nt":
            import msvcrt

            if lock.tell() == 0:
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        yield  # Closing the handle releases the OS lock.


def update(path, patch):
    validate(patch, patch=True)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with edit_lock(path):
        data = read(path)
        for role, settings in patch.get("roles", {}).items():
            if settings is None:
                data["roles"].pop(role, None)
            else:
                data["roles"][role] = settings
        if "max_parallel" in patch:
            if patch["max_parallel"] is None:
                data.pop("max_parallel", None)
            else:
                data["max_parallel"] = patch["max_parallel"]
        rendered = json.dumps(data, indent=2, sort_keys=True) + "\n"
        temp = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        )
        tmp_path = Path(temp.name)
        try:
            with temp:
                temp.write(rendered)
                temp.flush()
                os.fsync(temp.fileno())
            os.replace(tmp_path, path)
        finally:
            tmp_path.unlink(missing_ok=True)
        return read(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("show", "roles", "update"))
    args = parser.parse_args()
    home = Path(os.environ.get("PI_CODING_AGENT_DIR") or Path.home() / ".pi" / "agent").expanduser()
    path = home / "ppstack" / "models.json"
    if args.action == "roles":
        print("\n".join(ROLE_NAMES))
    elif args.action == "show":
        print(json.dumps(read(path), indent=2, sort_keys=True))
    else:
        patch = json.load(sys.stdin, object_pairs_hook=unique_keys)
        print(json.dumps(update(path, patch), indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        sys.exit(f"ppstack models: {exc}")
