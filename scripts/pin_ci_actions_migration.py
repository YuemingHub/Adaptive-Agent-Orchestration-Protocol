#!/usr/bin/env python3
"""One-time deterministic migration from reviewed v6 tags to validated SHAs.

This script intentionally has no general dependency-update behavior. It replaces
only the two exact mutable refs already observed in AAOP workflows and fails if a
workflow contains another external mutable Action ref.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
REPLACEMENTS = {
    "actions/checkout@v6": "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6",
    "actions/setup-python@v6": "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6",
}
USES_RE = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def main() -> int:
    changed: list[str] = []
    errors: list[str] = []
    for path in sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")]):
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in REPLACEMENTS.items():
            updated = updated.replace(old, new)

        for number, line in enumerate(updated.splitlines(), 1):
            match = USES_RE.match(line)
            if not match:
                continue
            target = match.group(1)
            if target.startswith("./"):
                continue
            if "@" not in target:
                errors.append(f"{path.relative_to(ROOT)}:{number}: external action missing ref: {target}")
                continue
            action, ref = target.rsplit("@", 1)
            if not SHA_RE.fullmatch(ref):
                errors.append(f"{path.relative_to(ROOT)}:{number}: external action remains mutable: {action}@{ref}")

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    if errors:
        print("FAIL one-time Action pin migration")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"PASS one-time Action pin migration; changed={len(changed)}")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
