#!/usr/bin/env python3
"""Fail if GitHub workflows execute unreviewed or mutable third-party Actions."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)(?:\s*#.*)?$")

# These are the exact Action revisions observed in the AAOP production gate set
# immediately before pinning. Updating either pin is a deliberate review event:
# change this registry, update workflows, and rerun the full release gate.
APPROVED_EXTERNAL_ACTIONS = {
    "actions/checkout": "d23441a48e516b6c34aea4fa41551a30e30af803",  # v6
    "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",  # v6
}


def validate() -> None:
    if not WORKFLOWS.is_dir():
        raise SystemExit(f"workflow directory missing: {WORKFLOWS}")

    errors: list[str] = []
    observed: set[str] = set()
    workflow_files = sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    if not workflow_files:
        errors.append("no GitHub workflows found")

    for path in workflow_files:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = USES_RE.match(line)
            if not match:
                continue
            target = match.group(1)
            if target.startswith("./"):
                continue
            if "@" not in target:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: external uses target has no ref: {target}")
                continue
            action, ref = target.rsplit("@", 1)
            observed.add(action)
            if not SHA_RE.fullmatch(ref):
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: mutable/non-SHA Action ref forbidden: {target}"
                )
                continue
            approved = APPROVED_EXTERNAL_ACTIONS.get(action)
            if approved is None:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: external Action is not in reviewed pin registry: {action}@{ref}"
                )
            elif ref != approved:
                errors.append(
                    f"{path.relative_to(ROOT)}:{line_number}: unreviewed Action revision: {action}@{ref}; approved={approved}"
                )

    missing = sorted(set(APPROVED_EXTERNAL_ACTIONS) - observed)
    if missing:
        errors.append(f"approved Action registry entries are unused: {', '.join(missing)}")

    if errors:
        print("FAIL GitHub Actions supply-chain pinning")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        "PASS GitHub Actions supply-chain pinning: "
        f"{len(workflow_files)} workflows, {len(observed)} reviewed external Actions"
    )


if __name__ == "__main__":
    validate()
