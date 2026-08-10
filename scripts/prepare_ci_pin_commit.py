#!/usr/bin/env python3
"""Upload reviewed workflow-pin contents as unreferenced Git blobs.

GitHub Actions' App token may create blob objects but is intentionally not granted
the separate workflow permission required to assemble/update a workflow tree/ref.
This one-time helper therefore stops after uploading blobs and prints the exact
base tree plus ``path -> blob SHA`` mapping. A separately authorized repository
control surface may decide whether to assemble those immutable objects.

No tree, commit, or branch ref is created/updated here.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    )
    return completed.stdout.strip()


def api(method: str, path: str, payload: dict[str, object] | None = None) -> dict[str, object]:
    if not REPOSITORY or not TOKEN:
        raise SystemExit("GITHUB_REPOSITORY/GITHUB_TOKEN are required")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API}{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AAOP-ci-pin-blob-preparer/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub API {method} {path} failed: HTTP {exc.code}: {body}") from exc
    if not isinstance(result, dict):
        raise SystemExit(f"GitHub API returned non-object for {method} {path}")
    return result


def main() -> int:
    parent = git("rev-parse", "HEAD")
    changed = [
        line.strip()
        for line in git("diff", "--name-only", "--", ".github/workflows").splitlines()
        if line.strip()
    ]
    if not changed:
        raise SystemExit("No workflow changes to prepare")
    if any(not path.startswith(".github/workflows/") for path in changed):
        raise SystemExit(f"Refusing non-workflow migration paths: {changed}")

    parent_commit = api("GET", f"/repos/{REPOSITORY}/git/commits/{parent}")
    tree_obj = parent_commit.get("tree")
    if not isinstance(tree_obj, dict) or not isinstance(tree_obj.get("sha"), str):
        raise SystemExit("Parent commit did not expose a tree SHA")
    base_tree = tree_obj["sha"]

    print(f"prepared_parent={parent}")
    print(f"prepared_base_tree={base_tree}")

    for relative in sorted(changed):
        path = ROOT / relative
        blob = api(
            "POST",
            f"/repos/{REPOSITORY}/git/blobs",
            {
                "content": base64.b64encode(path.read_bytes()).decode("ascii"),
                "encoding": "base64",
            },
        )
        sha = blob.get("sha")
        if not isinstance(sha, str):
            raise SystemExit(f"Blob creation returned no SHA for {relative}")
        print(f"prepared_blob={relative}\t{sha}")

    print(f"prepared_workflow_count={len(changed)}")
    print("No tree, commit, or branch ref was created/updated by this helper.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
