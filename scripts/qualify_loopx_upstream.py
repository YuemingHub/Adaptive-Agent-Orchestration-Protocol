#!/usr/bin/env python3
"""Qualify the reviewed LoopX upstream surface from an exact local checkout.

This is intentionally NOT part of AAOP's normal validation workflow. LoopX is
an optional provider, so AAOP's baseline CI must not depend on fetching or
executing an external repository. Run this harness when refreshing the LoopX
Recipe or before a real adoption pilot.

The harness reuses LoopX's own public stable smoke tests instead of copying its
CLI/state-machine behavior into AAOP.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / ".aaop" / "recipes" / "loopx.json"

CORE_SMOKES = [
    "examples/control_plane/quota-contract-smoke.py",
    "examples/control_plane/todo-cli-smoke.py",
    "examples/control_plane/todo-durability-fixture-smoke.py",
    "examples/blocker-push-runtime-smoke.py",
    "examples/project/project-uninstall-smoke.py",
]
INSTALL_SMOKE = "examples/fresh-clone-quickstart-smoke.py"


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def run(
    args: list[str],
    *,
    cwd: Path,
    expected: int = 0,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != expected:
        fail(
            f"command failed ({completed.returncode}, expected {expected}): {' '.join(args)}\n"
            f"cwd: {cwd}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def recipe_identity() -> tuple[str, str, str]:
    payload = json.loads(RECIPE.read_text(encoding="utf-8"))
    reviewed = payload.get("reviewed_upstream")
    if not isinstance(reviewed, dict):
        fail("LoopX Recipe is missing reviewed_upstream identity")
    tag = reviewed.get("stable_tag")
    commit = reviewed.get("stable_commit")
    version = reviewed.get("stable_package_version")
    if not all(isinstance(value, str) and value for value in (tag, commit, version)):
        fail("LoopX Recipe reviewed_upstream identity is incomplete")
    return tag, commit, version


def checkout_identity(checkout: Path) -> dict[str, object]:
    if not (checkout / ".git").exists():
        fail(f"LoopX qualification requires a git checkout: {checkout}")
    head = run(["git", "rev-parse", "HEAD"], cwd=checkout).stdout.strip()
    status = run(["git", "status", "--porcelain"], cwd=checkout).stdout.splitlines()
    pyproject_path = checkout / "pyproject.toml"
    if not pyproject_path.is_file():
        fail(f"missing LoopX pyproject.toml: {pyproject_path}")
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    project = pyproject.get("project")
    version = project.get("version") if isinstance(project, dict) else None
    requires_python = project.get("requires-python") if isinstance(project, dict) else None
    return {
        "head": head,
        "dirty_paths": status,
        "package_version": version,
        "requires_python": requires_python,
    }


def smoke_plan(checkout: Path, include_install_smoke: bool) -> list[Path]:
    relatives = list(CORE_SMOKES)
    if include_install_smoke:
        relatives.append(INSTALL_SMOKE)
    paths = [checkout / relative for relative in relatives]
    missing = [str(path.relative_to(checkout)) for path in paths if not path.is_file()]
    if missing:
        fail("reviewed LoopX smoke surface is missing: " + ", ".join(missing))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Qualify an exact LoopX checkout using upstream-owned public smokes"
    )
    parser.add_argument("--checkout", required=True, type=Path, help="local LoopX git checkout")
    parser.add_argument(
        "--include-install-smoke",
        action="store_true",
        help="also run LoopX's fresh-clone/install quickstart smoke (may use network/install wrappers)",
    )
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="verify identity and smoke availability, but only print the qualification plan",
    )
    parser.add_argument("--json", action="store_true", help="emit a machine-readable receipt")
    args = parser.parse_args()

    checkout = args.checkout.expanduser().resolve()
    reviewed_tag, reviewed_commit, reviewed_version = recipe_identity()
    identity = checkout_identity(checkout)

    if identity["head"] != reviewed_commit:
        fail(
            "LoopX checkout does not match the Recipe-reviewed immutable revision: "
            f"expected {reviewed_commit}, got {identity['head']}"
        )
    if identity["dirty_paths"]:
        fail("LoopX qualification requires a clean checkout; dirty paths: " + ", ".join(identity["dirty_paths"]))
    if identity["package_version"] != reviewed_version:
        fail(
            "LoopX package version does not match Recipe-reviewed identity: "
            f"expected {reviewed_version}, got {identity['package_version']!r}"
        )
    if reviewed_tag != f"v{reviewed_version}":
        fail(f"LoopX Recipe tag/version mismatch: {reviewed_tag} vs {reviewed_version}")

    smokes = smoke_plan(checkout, args.include_install_smoke)
    receipts: list[dict[str, object]] = []

    if not args.no_execute:
        for path in smokes:
            relative = path.relative_to(checkout).as_posix()
            completed = run([sys.executable, str(path)], cwd=checkout)
            receipts.append(
                {
                    "smoke": relative,
                    "status": "passed",
                    "stdout_tail": completed.stdout.strip().splitlines()[-1:][0]
                    if completed.stdout.strip()
                    else "",
                }
            )

    payload = {
        "schema_version": "aaop-loopx-upstream-qualification-v1",
        "provider": "loopx",
        "reviewed_tag": reviewed_tag,
        "reviewed_commit": reviewed_commit,
        "package_version": reviewed_version,
        "requires_python": identity["requires_python"],
        "checkout_clean": True,
        "mode": "plan-only" if args.no_execute else "executed",
        "smokes": [path.relative_to(checkout).as_posix() for path in smokes],
        "results": receipts,
        "boundary": (
            "This receipt qualifies the reviewed upstream control-plane mechanisms only. "
            "It does not prove AAOP selected LoopX correctly, that a real consumer has an "
            "execution-continuity gap, or that the AAOP<->LoopX real-development pilot passed."
        ),
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"PASS LoopX upstream qualification ({payload['mode']}): "
            f"{reviewed_tag}@{reviewed_commit}, {len(smokes)} upstream-owned smoke(s)"
        )
        if args.no_execute:
            for smoke in payload["smokes"]:
                print(f"  - {smoke}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
