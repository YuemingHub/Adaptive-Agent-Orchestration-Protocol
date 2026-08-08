#!/usr/bin/env python3
"""Install, safely upgrade, or safely remove AAOP without external dependencies.

Usage:
    python scripts/install.py /path/to/project
    python scripts/install.py /path/to/project --upgrade
    python scripts/install.py /path/to/project --uninstall

AAOP owns only manifest-tracked package files and marked bootstrap blocks. Upgrade
and uninstall preserve `.aaop/runtime/`, target-only `.aaop` files, and project
rules outside AAOP markers. No third-party provider is installed or removed.
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
MANIFEST_SCHEMA_VERSION = 2

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

Before relying on an existing AAOP installation when integrity is uncertain, use
`python .aaop/tools/health.py . --json`. Treat `drifted`, `incomplete`, or invalid
manifest/bootstrap states as evidence to review, not permission to overwrite local
state. The health check is best-effort accidental-drift detection, not a security
trust root.

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
## AAOP Claude Code bridge

For non-trivial developer work, read `.aaop/ORCHESTRATOR.md`, then start with
`.aaop/skills/developer-intake/SKILL.md`. After routing, load
`.aaop/skills/route-execution/SKILL.md` and only the current
`.aaop/routes/<route-id>.json`.

If AAOP install integrity is uncertain, use `python .aaop/tools/health.py . --json`
before repair. Prefer current project evidence and existing Claude Code/native
capability before adding providers.

This block is intentionally small. Canonical orchestration policy lives under
`.aaop/`; common cross-host bootstrap guidance lives in `AGENTS.md`.
{AAOP_END}
"""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def aaop_version(source_package: Path) -> str:
    """Return the sole installable AAOP package release identity.

    `.aaop/VERSION` is authoritative. Component documents may carry independent
    revision markers and must never be used to infer an install/manifest version.
    """
    version_file = source_package / "VERSION"
    if not version_file.is_file():
        raise SystemExit(
            "AAOP source package is incomplete: missing authoritative release identity "
            f"{version_file}. Do not infer package version from component documents."
        )
    try:
        version = version_file.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"Cannot read AAOP release identity {version_file}: {exc}") from exc
    if not version:
        raise SystemExit(
            f"AAOP source package is incomplete: authoritative release identity {version_file} is empty."
        )
    return version


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
        raise SystemExit(f"Cannot safely manage AAOP: invalid {path}: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), dict):
        raise SystemExit(f"Cannot safely manage AAOP: unsupported manifest shape in {path}")
    return payload


def write_manifest(destination: Path, version: str, files: dict[str, Path]) -> None:
    payload = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "aaop_version": version,
        "managed_by": "AAOP installer",
        "files": {relative: sha256_file(destination / relative) for relative in sorted(files)},
        "bootstrap_blocks": {
            "AGENTS.md": sha256_text(AGENTS_BLOCK.rstrip("\n")),
            "CLAUDE.md": sha256_text(CLAUDE_BLOCK.rstrip("\n")),
        },
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
            f"Cannot safely update {path}: expected exactly one matching AAOP marker pair, "
            f"found begin={begin_count}, end={end_count}."
        )
    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END)
    if end <= start:
        raise SystemExit(f"Cannot safely update {path}: malformed AAOP marker order")


def extract_block(path: Path) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if AAOP_BEGIN not in text and AAOP_END not in text:
        return None
    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    return text[start:end]


def backup_bootstrap_block(
    destination: Path,
    project_file: Path,
    expected_hash: str | None,
    backup_root: Path,
) -> str | None:
    block = extract_block(project_file)
    if block is None:
        return None
    current_hash = sha256_text(block)
    if expected_hash is not None and current_hash == expected_hash:
        return None

    target = backup_root / "project-rules" / f"{project_file.name}.aaop-block.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(block + "\n", encoding="utf-8")
    return target.relative_to(destination).as_posix()


def copy_managed_files(
    source_package: Path,
    target: Path,
    upgrade: bool,
) -> tuple[str, list[str], bool]:
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
            f"AAOP already exists at {destination}. Re-run with --upgrade to update managed files "
            "while preserving runtime and project-owned files."
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
        for relative, previous_hash in previous_files.items():
            target_file = destination / relative
            if not target_file.is_file():
                continue
            if sha256_file(target_file) != previous_hash:
                backups.append(backup_file(destination, relative, backup_root))

        for relative in sorted(set(files) - set(previous_files)):
            target_file = destination / relative
            if target_file.is_file():
                backups.append(backup_file(destination, relative, backup_root))

        for relative in sorted(set(previous_files) - set(files)):
            target_file = destination / relative
            if target_file.is_file():
                target_file.unlink()

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

    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    existing = text[start:end]
    replacement = block.rstrip("\n")
    if existing == replacement:
        return "already-current"

    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    return "updated"


def remove_block(path: Path) -> str:
    if not path.exists():
        return "missing-file"
    text = path.read_text(encoding="utf-8")
    if AAOP_BEGIN not in text and AAOP_END not in text:
        return "absent"

    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    path.write_text(text[:start] + text[end:], encoding="utf-8")
    return "removed"


def prune_empty_package_dirs(destination: Path) -> None:
    if not destination.exists():
        return
    directories = [path for path in destination.rglob("*") if path.is_dir()]
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        relative = path.relative_to(destination)
        if relative.parts and relative.parts[0] == "runtime":
            continue
        try:
            path.rmdir()
        except OSError:
            pass
    try:
        destination.rmdir()
    except OSError:
        pass


def remaining_project_files(destination: Path) -> list[str]:
    if not destination.exists():
        return []
    found: list[str] = []
    for path in destination.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(destination)
        if relative.parts and relative.parts[0] == "runtime":
            continue
        found.append(relative.as_posix())
    return sorted(found)


def uninstall_aaop(target: Path) -> dict[str, object]:
    destination = target / ".aaop"
    if not destination.exists():
        raise SystemExit(f"AAOP is not installed at {destination}")

    manifest = read_manifest(destination)
    if manifest is None:
        raise SystemExit(
            "Cannot safely uninstall a legacy AAOP package without "
            ".aaop/.install-manifest.json; managed files cannot be distinguished from "
            "project-owned files. Upgrade first to establish ownership, then uninstall."
        )

    raw_files = manifest.get("files", {})
    files = {str(key): str(value) for key, value in raw_files.items()}
    raw_bootstrap = manifest.get("bootstrap_blocks", {})
    bootstrap_hashes = (
        {str(key): str(value) for key, value in raw_bootstrap.items()}
        if isinstance(raw_bootstrap, dict)
        else {}
    )
    version = str(manifest.get("aaop_version") or "unknown")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = destination / "runtime" / "uninstall-backups" / f"from-{version}-{stamp}"

    backups: list[str] = []
    bootstrap_backups: list[str] = []
    removed: list[str] = []
    missing: list[str] = []

    for relative, installed_hash in sorted(files.items()):
        path = destination / relative
        if not path.exists():
            missing.append(relative)
            continue
        if not path.is_file():
            continue
        try:
            changed = sha256_file(path) != installed_hash
        except OSError:
            changed = True
        if changed:
            backups.append(backup_file(destination, relative, backup_root))

    for name in ("AGENTS.md", "CLAUDE.md"):
        expected = bootstrap_hashes.get(name)
        backed_up = backup_bootstrap_block(
            destination,
            target / name,
            expected if expected else None,
            backup_root,
        )
        if backed_up:
            bootstrap_backups.append(backed_up)

    for relative in sorted(files):
        path = destination / relative
        if path.is_file():
            path.unlink()
            removed.append(relative)

    manifest_path = destination / MANIFEST_NAME
    if manifest_path.is_file():
        manifest_path.unlink()

    agents_status = remove_block(target / "AGENTS.md")
    claude_status = remove_block(target / "CLAUDE.md")
    prune_empty_package_dirs(destination)

    return {
        "version": version,
        "removed": removed,
        "missing": missing,
        "backups": sorted(set(backups)),
        "bootstrap_backups": sorted(set(bootstrap_backups)),
        "agents_status": agents_status,
        "claude_status": claude_status,
        "runtime_preserved": (destination / "runtime").exists(),
        "project_files_preserved": remaining_project_files(destination),
        "package_dir_remaining": destination.exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install, safely upgrade, or safely remove AAOP in a project"
    )
    parser.add_argument("target", type=Path, help="Target project directory")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--upgrade",
        action="store_true",
        help=(
            "Upgrade AAOP-managed files while preserving .aaop/runtime, project-owned "
            "files, and non-AAOP rule text."
        ),
    )
    actions.add_argument(
        "--uninstall",
        action="store_true",
        help=(
            "Remove only manifest-owned AAOP files and marked bootstrap blocks; preserve "
            "runtime and project-owned files."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Legacy alias for --upgrade. No destructive directory replacement is performed.",
    )
    args = parser.parse_args()

    if args.uninstall and args.force:
        parser.error("--force is an upgrade alias and cannot be combined with --uninstall")

    source = Path(__file__).resolve().parents[1]
    source_package = source / ".aaop"
    target = args.target.expanduser().resolve()

    if args.uninstall:
        if not target.exists():
            raise SystemExit(f"Target project does not exist: {target}")
        validate_block_markers(target / "AGENTS.md")
        validate_block_markers(target / "CLAUDE.md")
        result = uninstall_aaop(target)
        print("AAOP uninstalled")
        print(f"  installed version removed: {result['version']}")
        print(f"  managed files removed: {len(result['removed'])}")
        print(f"  managed files already missing: {len(result['missing'])}")
        print(f"  modified managed files backed up: {len(result['backups'])}")
        print(
            "  modified/untracked bootstrap blocks backed up: "
            f"{len(result['bootstrap_backups'])}"
        )
        if result["backups"] or result["bootstrap_backups"]:
            print("  backup scope: .aaop/runtime/uninstall-backups/")
        print(f"  AGENTS.md AAOP block: {result['agents_status']}")
        print(f"  CLAUDE.md AAOP block: {result['claude_status']}")
        print(
            f"  .aaop/runtime preserved: {'yes' if result['runtime_preserved'] else 'not present'}"
        )
        print(f"  target-only .aaop files preserved: {len(result['project_files_preserved'])}")
        print(
            f"  .aaop directory remaining: {'yes' if result['package_dir_remaining'] else 'no'}"
        )
        print("  third-party providers removed: none")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    required = source_package / "ORCHESTRATOR.md"
    if not required.exists():
        raise SystemExit(f"AAOP source package is incomplete: missing {required}")

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
        print(
            "  legacy upgrade: no prior install manifest; runtime/target-only files were "
            "preserved, current managed paths were refreshed"
        )
    print("  third-party providers installed: none")
    print("  secrets requested: none")
    print("Optional health: python .aaop/tools/health.py .")
    print("Optional inventory: python .aaop/tools/doctor.py .")
    print("Optional route packs: python .aaop/tools/route.py list")
    print("Optional provider recipes: python .aaop/tools/recipe.py list")
    print("Safe removal: python scripts/install.py /path/to/project --uninstall")
    print(
        "Next: open the target project in your existing AI host and describe what you "
        "want in ordinary language."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
