"""List Pi session metadata for a worktree, or read one session's active branch."""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def session_directories(cwd, override):
    agent = Path(os.environ.get("PI_CODING_AGENT_DIR") or "~/.pi/agent").expanduser()
    location = override or os.environ.get("PI_CODING_AGENT_SESSION_DIR")
    if not location:
        for path in (cwd / ".pi/settings.json", agent / "settings.json"):
            try:
                settings = json.loads(path.read_bytes())
            except FileNotFoundError:
                continue
            if not isinstance(settings, dict):
                raise ValueError(f"Invalid settings object in {path}")
            location = settings.get("sessionDir")
            if location:
                if not isinstance(location, str):
                    raise ValueError(f"Invalid sessionDir in {path}")
                break
    if location:
        directory = (cwd / Path(location).expanduser()).resolve()
        return directory, directory
    # Pi encodes the absolute path into a single directory name.
    project = re.sub(r"[/\\:]", "-", str(cwd).lstrip("/\\"))
    root = (agent / "sessions").resolve()
    return root / f"--{project}--", root


def session_paths(cwds, override, include_workers):
    directories = {session_directories(cwd, override) for cwd in cwds}
    for directory, _ in directories:
        yield from directory.glob("*.jsonl")
    if include_workers:
        # A child can work in a different checkout from the parent that owns its file.
        for root in {root for _, root in directories}:
            for directory, _, files in os.walk(root):
                path = Path(directory)
                if path.parent.name == "forks":
                    yield from (path / name for name in files if name.endswith(".jsonl"))
                elif path.name.startswith("run-") and "session.jsonl" in files:
                    yield path / "session.jsonl"


def sessions(paths, cwds, session_id):
    records = {}
    for path in paths:
        if path.is_symlink() or not path.is_file():
            continue
        try:
            with path.open("rb") as stream:
                header = json.loads(stream.readline(1024 * 1024))
            if not isinstance(header, dict) or header.get("type") != "session":
                continue
            recorded = header.get("cwd")
            identifier = header.get("id")
            if not isinstance(identifier, str) or not identifier or (session_id and session_id != identifier):
                continue
            if not isinstance(recorded, str) or not Path(recorded).is_absolute():
                continue
            cwd = Path(recorded).resolve()
            if cwd not in cwds:
                continue
            updated = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        except (OSError, RuntimeError, ValueError):
            continue
        row = dict(path=str(path), cwd=str(cwd), id=identifier, updated_at=updated)
        key = (cwd, identifier)
        if key not in records or updated > records[key]["updated_at"]:
            records[key] = row
    return sorted(records.values(), key=lambda row: (row["updated_at"], row["id"]), reverse=True)


def branch(path):
    with path.open("rb") as stream:
        header = json.loads(stream.readline())
        entries = []
        for line in stream:
            if not line.strip():
                continue
            try:
                entries.append(json.loads(line))
            except ValueError:
                # Pi may still be appending the final entry.
                if line.endswith(b"\n"):
                    raise
    if header.get("version", 1) == 1:
        return entries  # Version 1 sessions are linear.
    by_id = {entry["id"]: entry for entry in entries}
    leaf = entries[-1]["id"] if entries else None
    active = []
    while leaf is not None:
        # Removing visited nodes also rejects cycles in a damaged history.
        if leaf not in by_id:
            raise ValueError(f"Invalid branch link in {path}")
        entry = by_id.pop(leaf)
        active.append(entry)
        leaf = entry["parentId"]
    return reversed(active)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, nargs="+", required=True, help="recorded working directories")
    parser.add_argument("--id", help="exact Pi session ID")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--current", action="store_true", help="use PI_SESSION_FILE and PI_SESSION_ID from Pi")
    source.add_argument("--session-file", type=Path, help="read this exact Pi session file")
    parser.add_argument("--include-workers", action="store_true", help="also list pi-subagents runs and forks")
    parser.add_argument("--session-dir", help="session directory used by pi --session-dir")
    parser.add_argument("--branch", action="store_true", help="print the selected session's persisted branch as JSONL")
    opts = parser.parse_args()
    session_id = opts.id
    session_file = opts.session_file
    current_id = os.environ.get("PI_SESSION_ID")
    if opts.current:
        if not current_id or (session_id is not None and session_id != current_id):
            parser.error("--current requires a matching PI_SESSION_ID")
        session_id = current_id
    if session_file is None and session_id and session_id == current_id:
        session_file = os.environ.get("PI_SESSION_FILE")
    if opts.branch and not (session_id or session_file):
        parser.error("--branch requires --current, --id or --session-file")
    if (session_id or session_file) and len(opts.cwd) != 1:
        parser.error("exact session lookup requires one --cwd")
    try:
        cwds = {cwd.expanduser().resolve() for cwd in opts.cwd}
        if session_file:
            paths = [Path(session_file).expanduser().resolve()]
        else:
            paths = session_paths(cwds, opts.session_dir, opts.include_workers)
        rows = sessions(paths, cwds, session_id)
        if not rows and (session_file or opts.branch or opts.current):
            sys.exit(f"No matching Pi session for {opts.cwd[0]} ({session_file or session_id})")
        if opts.branch:
            rows = branch(Path(rows[0]["path"]))
        for row in rows:
            print(json.dumps(row))
    except (OSError, KeyError, RuntimeError, ValueError) as error:
        sys.exit(f"Cannot read Pi session data: {error}")
