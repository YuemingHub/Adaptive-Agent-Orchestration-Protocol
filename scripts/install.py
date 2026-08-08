#!/usr/bin/env python3
"""Install or safely upgrade AAOP in another project without external dependencies.

Usage:
    python scripts/install.py /path/to/project
    python scripts/install.py /path/to/project --upgrade

The installer copies only AAOP-managed protocol files, preserves `.aaop/runtime/`,
leaves target-only files untouched, and owns only the marked AAOP blocks inside
AGENTS.md / CLAUDE.md. It installs no third-party provider and requests no secret.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

AAOP_BEGIN = "<!-- AAOP:BEGIN -->"
AAOP_END = "<!-- AAOP:END -->"
MANIFEST_NAME = ".install-manifest.json"
MANIFEST_SCHEMA_VERSION = 1

AGENTS_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

For non-trivial developer work, read `.aaop/ORCHESTRATOR.md`, begin with
`.aaop/skills/developer-intake/SKILL.md`, select one primary route, then load
`.aaop/skills/route-execution/SKILL.md` plus only `.aaop/routes/<route-id>.json`.

Accept ordinary developer language. Read accessible project evidence before asking
for facts already present. For greenfield ideas, separate the observable outcome
from technology names: Agent/MCP/RAG/vector DB/graph/memory and similar terms are
candidate solutions unless explicitly established as hard constraints. Define an
evidence-bearing first slice before architecture and do not make a non-technical
user choose a stack the system can derive later.

For review/adoption/audit requests, define the decision first, verify material
external claims against current source/status when practical, contextualize risk,
and remain read-only unless mutation is explicitly requested.

Establish the relevant current baseline/source authority before treating old issues,
PRs, branches, status files, or prior AI conclusions as current truth. Apply route
pressure guards when their condition is present.

Reuse current host/repository capabilities first. If work is blocked, distinguish
missing evidence, environment/network limits, authorization, credentials, external
dependencies, and product decisions from a genuine technical capability gap. Only
a proven capability gap justifies provider selection, and then choose the smallest
provider surface. When a selected Recipe has an applicable `adoption_review`,
re-check it against current upstream and the actual deployment context rather than
using it as a permanent provider verdict. Do not widen access or install workaround
machinery to bypass a non-capability blocker. Verify the outcome; if safely blocked,
preserve unknown state and report the smallest legitimate unblock rather than
claiming completion.

Canonical orchestration Skills live under `.aaop/skills/`.
{AAOP_END}
"""

CLAUDE_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

Read `AGENTS.md`, `.aaop/ORCHESTRATOR.md`, and start developer requests with
`.aaop/skills/developer-intake/SKILL.md`. After routing, load
`.aaop/skills/route-execution/SKILL.md` and only the current route pack. Prefer
current project evidence and existing Claude Code/native capabilities.

For ideas, outcome and a learning-bearing first slice come before architecture;
implementation vocabulary is not automatically a requirement. For reviews, frame
the decision, verify current evidence, contextualize risk, and do not mutate by
default. Reconcile stale artifacts with the current baseline, apply route pressure
guards, and classify blockers before calling them capability gaps. Do not add
providers merely because they are listed; prove a technical gap first. Re-check any
applicable Recipe `adoption_review` against current upstream/context before adoption.
Do not fabricate completion when an environment/permission/evidence blocker requires
a legitimate unblock.
{AAOP_END}
"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def aaop_version(source_package: Path) -> str:
    version_file = source_package / "VERSION"
    if version_file.exists():
        version = version_file.read_text(encoding="utf-8").strip()
        if version:
            return version

    # Backward-compatible fallback for source trees created before VERSION existed.
    orchestrator = source_package / "ORCHESTRATOR.md"
    for line in orchestrator.read_text(encoding="utf-8").splitlines():
        if line.startswith("Version:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def source_files(source_package: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in sorted(source_package.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source_package)
        if "runtime" in relative.parts or relative.as_posix() == MANIFEST_NAME:
            continue
        files[relative.as_posix()] = path
    return files


def read_manifest(destination: Path) -> dict[str, object] | None:
    path = destination / MANIFEST_NAME
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Cannot safely upgrade: invalid {path}: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), dict):
        raise SystemExit(f"Cannot safely upgrade: unsupported manifest shape in {path}")
    return payload


def write_manifest(destination: Path, version: str, files: dict[str, Path]) -> None:
    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "aaop_version": version,
        "managed_by": "AAOP installer",
        "files": {relative: sha256_file(destination / relative) for relative in sorted(files)},
    }
    (destination / MANIFEST_NAME).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def backup_file(destination: Path, relative: str, backup_root: Path) -> str:
    source = destination / relative
    target = backup_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return relative


def validate_block_markers(path: Path) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    begin_count = text.count(AAOP_BEGIN)
    end_count = text.count(AAOP_END)
    if begin_count == 0 and end_count == 0:
        return
    if begin_count != 1 or end_count != 1:
        raise SystemExit(
            f"Cannot safely update {path}: expected exactly one matching AAOP marker pair, found begin={begin_count}, end={end_count}."
        )
    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END)
    if end <= start:
        raise SystemExit(f"Cannot safely update {path}: malformed AAOP marker order")


def copy_managed_files(source_package: Path, target: Path, upgrade: bool) -> tuple[str, list[str], bool]:
    destination = target / ".aaop"
    files = source_files(source_package)
    version = aaop_version(source_package)
    backups: list[str] = []
    legacy_upgrade = False

    if not destination.exists():
        destination.mkdir(parents=True)
        for relative, source in files.items():
            target_file = destination / relative
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target_file)
        write_manifest(destination, version, files)
        return "installed", backups, legacy_upgrade

    if not upgrade:
        raise SystemExit(
            f"AAOP already exists at {destination}. Re-run with --upgrade to update managed files while preserving runtime and project-owned files."
        )

    manifest = read_manifest(destination)
    previous_files: dict[str, str] = {}
    if manifest is not None:
        raw_files = manifest.get("files", {})
        previous_files = {str(key): str(value) for key, value in raw_files.items()}
    else:
        legacy_upgrade = True

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = destination / "runtime" / "upgrade-backups" / f"to-{version}-{stamp}"

    if previous_files:
        # Back up locally modified previously-managed files before replacement/removal.
        for relative, previous_hash in previous_files.items():
            target_file = destination / relative
            if not target_file.is_file():
                continue
            if sha256_file(target_file) != previous_hash:
                backups.append(backup_file(destination, relative, backup_root))

        # A path can be project-owned today and become AAOP-managed in a future release.
        # Back it up before claiming that path.
        for relative in sorted(set(files) - set(previous_files)):
            target_file = destination / relative
            if target_file.is_file():
                backups.append(backup_file(destination, relative, backup_root))

        # Remove files that the previous installer managed but the new package no longer owns.
        for relative in sorted(set(previous_files) - set(files)):
            target_file = destination / relative
            if target_file.is_file():
                target_file.unlink()

    # A legacy installation has no hash manifest, so we cannot distinguish edits to old
    # managed files. Preserve runtime/ and target-only paths, then refresh only paths that
    # exist in the current source package.
    for relative, source in files.items():
        target_file = destination / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_file)

    write_manifest(destination, version, files)
    return "upgraded", sorted(set(backups)), legacy_upgrade


def upsert_block(path: Path, block: str) -> str:
    block = block.rstrip() + "\n"
    if not path.exists():
        path.write_text(block, encoding="utf-8")
        return "created"

    text = path.read_text(encoding="utf-8")
    begin_count = text.count(AAOP_BEGIN)
    end_count = text.count(AAOP_END)

    if begin_count == 0 and end_count == 0:
        separator = "" if not text or text.endswith("\n\n") else "\n\n"
        path.write_text(text + separator + block, encoding="utf-8")
        return "appended"

    # Marker shape was preflighted before package mutation.
    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    existing = text[start:end]
    replacement = block.rstrip("\n")
    if existing == replacement:
        return "already-current"

    new_text = text[:start] + replacement + text[end:]
    path.write_text(new_text, encoding="utf-8")
    return "updated"


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or safely upgrade AAOP in a project")
    parser.add_argument("target", type=Path, help="Target project directory")
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Upgrade AAOP-managed files while preserving .aaop/runtime, project-owned files, and non-AAOP rule text.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Legacy alias for --upgrade. No destructive directory replacement is performed.",
    )
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    source_package = source / ".aaop"
    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    required = source_package / "ORCHESTRATOR.md"
    if not required.exists():
        raise SystemExit(f"AAOP source package is incomplete: missing {required}")

    # Preflight project-owned rule files before mutating the installed package.
    validate_block_markers(target / "AGENTS.md")
    validate_block_markers(target / "CLAUDE.md")

    mode, backups, legacy_upgrade = copy_managed_files(
        source_package,
        target,
        upgrade=args.upgrade or args.force,
    )
    agents_status = upsert_block(target / "AGENTS.md", AGENTS_BLOCK)
    claude_status = upsert_block(target / "CLAUDE.md", CLAUDE_BLOCK)

    print(f"AAOP {mode}")
    print(f"  version: {aaop_version(source_package)}")
    print(f"  package: {target / '.aaop'}")
    print(f"  AGENTS.md: {agents_status}")
    print(f"  CLAUDE.md: {claude_status}")
    print("  .aaop/runtime preserved: yes")
    print("  target-only .aaop files preserved: yes")
    print(f"  modified/colliding managed files backed up: {len(backups)}")
    if backups:
        print("  backup scope: .aaop/runtime/upgrade-backups/")
    if legacy_upgrade:
        print("  legacy upgrade: no prior install manifest; runtime/target-only files were preserved, current managed paths were refreshed")
    print("  third-party providers installed: none")
    print("  secrets requested: none")
    print("Optional inventory: python .aaop/tools/doctor.py .")
    print("Optional route packs: python .aaop/tools/route.py list")
    print("Optional provider recipes: python .aaop/tools/recipe.py list")
    print("Next: open the target project in your existing AI host and describe what you want in ordinary language.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
