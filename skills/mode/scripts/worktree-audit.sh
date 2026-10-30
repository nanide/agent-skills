#!/usr/bin/env bash
set -euo pipefail
exec python3 - "$@" <<'PY'
import argparse
import json
import os
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description="Read-only local git worktree audit. Ownership and ignored files require separate review.")
parser.add_argument("-b", "--base")
parser.add_argument("repo", nargs="?", default=".")
args = parser.parse_args()

def git(*argv, cwd=args.repo, check=True):
    return subprocess.run(["git", *argv], cwd=cwd, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})

def commit(ref):
    result = git("rev-parse", "--verify", ref + "^{commit}", check=False)
    return result.stdout.decode().strip() if result.returncode == 0 else None

try:
    git("rev-parse", "--git-dir")
    base = args.base
    if base is None:
        result = git("symbolic-ref", "--short", "refs/remotes/origin/HEAD", check=False)
        base = result.stdout.decode().strip() if result.returncode == 0 else None
        if not base:
            parser.error("no origin/HEAD; pass --base with the actual target ref")
    base_sha = commit(base)
    if not base_sha:
        parser.error("base is not a local commit ref: " + base)
    records = git("worktree", "list", "--porcelain", "-z").stdout.split(b"\0\0")
    rows = []
    for index, record in enumerate(records):
        if not record:
            continue
        fields = {}
        for field in record.split(b"\0"):
            key, _, value = field.partition(b" ")
            fields[os.fsdecode(key)] = os.fsdecode(value)
        path = fields["worktree"]
        if "bare" in fields:
            rows.append({"path": path, "review": "hold-bare"})
            continue
        status = git("status", "--porcelain=v1", "-z", "--untracked-files=all", cwd=path, check=False)
        ignored = git("ls-files", "--others", "--ignored", "--exclude-standard", "-z", cwd=path, check=False)
        head = fields.get("HEAD")
        merged = bool(head) and git("merge-base", "--is-ancestor", head, base_sha, check=False).returncode == 0
        if index == 0:
            review = "hold-primary"
        elif "locked" in fields or "prunable" in fields:
            review = "hold-locked-or-unavailable"
        elif status.returncode or ignored.returncode:
            review = "hold-unreadable"
        elif status.stdout or ignored.stdout:
            review = "hold-files"
        elif not merged:
            review = "hold-unmerged"
        else:
            review = "verify-ownership"
        rows.append({"path": path, "head": head, "branch": fields.get("branch"), "ancestor_of_base": merged, "dirty": bool(status.stdout) if not status.returncode else None, "has_ignored_files": bool(ignored.stdout) if not ignored.returncode else None, "review": review})
    print(json.dumps({"base": base, "base_sha": base_sha, "local_refs_only": True, "worktrees": rows}, indent=2))
except (OSError, subprocess.CalledProcessError) as error:
    parser.exit(1, "audit failed: " + str(error) + "\n")
PY
