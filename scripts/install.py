#!/usr/bin/env python3
"""Install, safely upgrade, recover, or remove AAOP without external dependencies.

Usage:
    python scripts/install.py /path/to/project
    python scripts/install.py /path/to/project --upgrade
    python scripts/install.py /path/to/project --uninstall
    python scripts/install.py /path/to/project --recover-interrupted

AAOP owns only manifest-tracked package files and marked bootstrap blocks. Lifecycle
mutation is journaled outside ``.aaop`` so a failed or interrupted promotion cannot
silently masquerade as a coherent installation. Upgrade and uninstall preserve
``.aaop/runtime/``, target-only ``.aaop`` files, and project rules outside AAOP
markers. No third-party provider is installed or removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

AAOP_BEGIN = "<!-- AAOP:BEGIN -->"
AAOP_END = "<!-- AAOP:END -->"
MANIFEST_NAME = ".install-manifest.json"
MANIFEST_SCHEMA_VERSION = 2
TRANSACTION_DIR_NAME = ".aaop-install-transaction"
TRANSACTION_SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BOOTSTRAP_FILES = ("AGENTS.md", "CLAUDE.md")

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


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.aaop-{os.getpid()}.tmp")
    try:
        temporary.write_text(value, encoding="utf-8")
        temporary.replace(path)
    finally:
        try:
            if temporary.exists():
                temporary.unlink()
        except OSError:
            pass


def atomic_copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.aaop-{os.getpid()}.tmp")
    try:
        shutil.copy2(source, temporary)
        temporary.replace(target)
    finally:
        try:
            if temporary.exists():
                temporary.unlink()
        except OSError:
            pass


def aaop_version(source_package: Path) -> str:
    """Return the sole installable AAOP package release identity."""
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
    """Return only canonical source files that AAOP may own in an installation."""
    files: dict[str, Path] = {}
    for path in sorted(source_package.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(source_package)
        if "runtime" in relative.parts or relative.as_posix() == MANIFEST_NAME:
            continue
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        files[relative.as_posix()] = path
    return files


def validate_managed_relative(relative: object) -> str:
    raw = str(relative)
    normalized = raw.replace("\\", "/")
    parts = normalized.split("/")
    has_drive = bool(parts and len(parts[0]) == 2 and parts[0][1] == ":")
    if (
        not normalized
        or normalized.startswith("/")
        or normalized.startswith("//")
        or has_drive
        or any(part in {"", ".", ".."} for part in parts)
    ):
        raise SystemExit(f"Cannot safely manage AAOP: unsafe managed path in manifest: {raw!r}")
    if parts[0] == "runtime" or normalized == MANIFEST_NAME:
        raise SystemExit(
            "Cannot safely manage AAOP: manifest may not claim runtime or its own manifest "
            f"as a managed package file: {raw!r}"
        )
    return "/".join(parts)


def validate_sha256(value: object, *, field: str) -> str:
    text = str(value)
    if not SHA256_RE.fullmatch(text):
        raise SystemExit(f"Cannot safely manage AAOP: {field} must be a lowercase SHA-256 hex digest")
    return text


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

    schema_version = payload.get("schema_version")
    if not isinstance(schema_version, int) or schema_version < 1:
        raise SystemExit(
            f"Cannot safely manage AAOP: manifest schema_version must be a positive integer in {path}"
        )
    if schema_version > MANIFEST_SCHEMA_VERSION:
        raise SystemExit(
            "Cannot safely manage AAOP: installed manifest schema is newer than this installer "
            f"understands ({schema_version} > {MANIFEST_SCHEMA_VERSION}). Use a matching/newer "
            "trusted AAOP installer; do not downgrade-manage newer ownership metadata."
        )

    raw_files = payload.get("files", {})
    normalized_files: dict[str, str] = {}
    assert isinstance(raw_files, dict)
    for raw_relative, raw_hash in raw_files.items():
        relative = validate_managed_relative(raw_relative)
        if relative in normalized_files:
            raise SystemExit(
                f"Cannot safely manage AAOP: duplicate normalized managed path in manifest: {relative}"
            )
        normalized_files[relative] = validate_sha256(
            raw_hash, field=f"manifest.files[{raw_relative!r}]"
        )
    payload["files"] = normalized_files

    bootstrap = payload.get("bootstrap_blocks")
    if bootstrap is not None:
        if not isinstance(bootstrap, dict):
            raise SystemExit(f"Cannot safely manage AAOP: manifest.bootstrap_blocks must be an object in {path}")
        normalized_bootstrap: dict[str, str] = {}
        for name, raw_hash in bootstrap.items():
            if str(name) not in BOOTSTRAP_FILES:
                raise SystemExit(
                    f"Cannot safely manage AAOP: unsupported bootstrap ownership key in manifest: {name!r}"
                )
            normalized_bootstrap[str(name)] = validate_sha256(
                raw_hash, field=f"manifest.bootstrap_blocks[{name!r}]"
            )
        payload["bootstrap_blocks"] = normalized_bootstrap
    return payload


def manifest_payload(destination: Path, version: str, files: dict[str, Path]) -> dict[str, object]:
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "aaop_version": version,
        "managed_by": "AAOP installer",
        "files": {relative: sha256_file(destination / relative) for relative in sorted(files)},
        "bootstrap_blocks": {
            "AGENTS.md": sha256_text(AGENTS_BLOCK.rstrip("\n")),
            "CLAUDE.md": sha256_text(CLAUDE_BLOCK.rstrip("\n")),
        },
    }


def write_manifest(destination: Path, version: str, files: dict[str, Path]) -> None:
    payload = manifest_payload(destination, version, files)
    atomic_write_text(
        destination / MANIFEST_NAME,
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )


def backup_file(destination: Path, relative: str, backup_root: Path) -> str:
    relative = validate_managed_relative(relative)
    source = destination / relative
    target = backup_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return relative


def validate_block_markers(path: Path) -> None:
    if not path.exists():
        return
    if not path.is_file():
        raise SystemExit(f"Cannot safely update {path}: expected a file")
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


def transaction_root(target: Path) -> Path:
    return target / TRANSACTION_DIR_NAME


def transaction_metadata_path(transaction: Path) -> Path:
    return transaction / "transaction.json"


def write_transaction_metadata(transaction: Path, payload: dict[str, object]) -> None:
    atomic_write_text(
        transaction_metadata_path(transaction),
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )


def read_transaction_metadata(transaction: Path) -> dict[str, object]:
    path = transaction_metadata_path(transaction)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Cannot safely recover interrupted AAOP transaction {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != TRANSACTION_SCHEMA_VERSION:
        raise SystemExit(f"Cannot safely recover interrupted AAOP transaction: unsupported metadata in {path}")
    managed = payload.get("managed")
    project_files = payload.get("project_files")
    if not isinstance(managed, dict) or not isinstance(project_files, dict):
        raise SystemExit(f"Cannot safely recover interrupted AAOP transaction: invalid shape in {path}")
    normalized_managed: dict[str, object] = {}
    for raw_relative, entry in managed.items():
        relative = validate_managed_relative(raw_relative)
        if not isinstance(entry, dict) or not isinstance(entry.get("existed"), bool):
            raise SystemExit(f"Cannot safely recover interrupted AAOP transaction: invalid entry for {relative}")
        normalized_managed[relative] = entry
    payload["managed"] = normalized_managed
    for name, entry in project_files.items():
        if str(name) not in BOOTSTRAP_FILES or not isinstance(entry, dict) or not isinstance(entry.get("existed"), bool):
            raise SystemExit(f"Cannot safely recover interrupted AAOP transaction: invalid project-file entry {name!r}")
    if not isinstance(payload.get("manifest_existed"), bool):
        raise SystemExit("Cannot safely recover interrupted AAOP transaction: invalid manifest state")
    return payload


def ensure_no_interrupted_transaction(target: Path) -> None:
    transaction = transaction_root(target)
    if transaction.exists():
        raise SystemExit(
            f"Cannot start AAOP lifecycle mutation: interrupted transaction exists at {transaction}. "
            "Inspect it and run the trusted installer/bootstrap with --recover-interrupted before retrying."
        )


def snapshot_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def begin_transaction(target: Path, managed_paths: set[str], action: str) -> tuple[Path, dict[str, object]]:
    transaction = transaction_root(target)
    if transaction.exists():
        ensure_no_interrupted_transaction(target)
    transaction.mkdir(parents=False)
    destination = target / ".aaop"
    metadata: dict[str, object] = {
        "schema_version": TRANSACTION_SCHEMA_VERSION,
        "id": f"{now_stamp()}-{os.getpid()}",
        "action": action,
        "state": "prepared",
        "managed": {},
        "manifest_existed": (destination / MANIFEST_NAME).is_file(),
        "project_files": {},
    }
    try:
        managed_meta: dict[str, object] = {}
        for raw_relative in sorted(managed_paths):
            relative = validate_managed_relative(raw_relative)
            path = destination / relative
            if path.exists() and not path.is_file():
                raise SystemExit(
                    f"Cannot safely mutate AAOP: managed path collides with a non-file: {path}"
                )
            existed = path.is_file()
            managed_meta[relative] = {"existed": existed}
            if existed:
                snapshot_file(path, transaction / "before" / "aaop" / relative)
        metadata["managed"] = managed_meta

        manifest = destination / MANIFEST_NAME
        if manifest.is_file():
            snapshot_file(manifest, transaction / "before" / "manifest.json")

        project_meta: dict[str, object] = {}
        for name in BOOTSTRAP_FILES:
            path = target / name
            if path.exists() and not path.is_file():
                raise SystemExit(f"Cannot safely mutate AAOP bootstrap file: expected file at {path}")
            existed = path.is_file()
            project_meta[name] = {"existed": existed}
            if existed:
                snapshot_file(path, transaction / "before" / "project" / name)
        metadata["project_files"] = project_meta
        write_transaction_metadata(transaction, metadata)
        metadata["state"] = "promoting"
        write_transaction_metadata(transaction, metadata)
        return transaction, metadata
    except BaseException:
        shutil.rmtree(transaction, ignore_errors=True)
        raise


def snapshot_interrupted_current(target: Path, transaction: Path, metadata: dict[str, object]) -> None:
    destination = target / ".aaop"
    managed = metadata.get("managed", {})
    assert isinstance(managed, dict)
    for relative in managed:
        safe_relative = validate_managed_relative(relative)
        path = destination / safe_relative
        if path.is_file():
            snapshot_file(path, transaction / "interrupted-current" / "aaop" / safe_relative)
    manifest = destination / MANIFEST_NAME
    if manifest.is_file():
        snapshot_file(manifest, transaction / "interrupted-current" / "manifest.json")
    for name in BOOTSTRAP_FILES:
        path = target / name
        if path.is_file():
            snapshot_file(path, transaction / "interrupted-current" / "project" / name)


def rollback_transaction(
    target: Path,
    transaction: Path,
    metadata: dict[str, object],
    *,
    preserve_interrupted_current: bool,
) -> None:
    destination = target / ".aaop"
    if preserve_interrupted_current:
        snapshot_interrupted_current(target, transaction, metadata)

    managed = metadata.get("managed", {})
    assert isinstance(managed, dict)
    for relative, raw_entry in managed.items():
        safe_relative = validate_managed_relative(relative)
        assert isinstance(raw_entry, dict)
        path = destination / safe_relative
        existed = bool(raw_entry.get("existed"))
        if existed:
            backup = transaction / "before" / "aaop" / safe_relative
            if not backup.is_file():
                raise SystemExit(f"Cannot rollback AAOP transaction: missing snapshot {backup}")
            atomic_copy_file(backup, path)
        else:
            if path.exists() and not path.is_file():
                raise SystemExit(f"Cannot rollback AAOP transaction over non-file path {path}")
            if path.is_file():
                path.unlink()

    manifest = destination / MANIFEST_NAME
    if bool(metadata.get("manifest_existed")):
        backup_manifest = transaction / "before" / "manifest.json"
        if not backup_manifest.is_file():
            raise SystemExit("Cannot rollback AAOP transaction: manifest snapshot is missing")
        atomic_copy_file(backup_manifest, manifest)
    elif manifest.is_file():
        manifest.unlink()

    project_files = metadata.get("project_files", {})
    assert isinstance(project_files, dict)
    for name, raw_entry in project_files.items():
        assert isinstance(raw_entry, dict)
        path = target / str(name)
        existed = bool(raw_entry.get("existed"))
        if existed:
            backup = transaction / "before" / "project" / str(name)
            if not backup.is_file():
                raise SystemExit(f"Cannot rollback AAOP transaction: project snapshot is missing for {name}")
            atomic_copy_file(backup, path)
        elif path.is_file():
            path.unlink()

    prune_empty_package_dirs(destination)
    metadata["state"] = "rolled-back"
    write_transaction_metadata(transaction, metadata)


def archive_recovered_transaction(target: Path, transaction: Path, metadata: dict[str, object]) -> Path:
    txid = str(metadata.get("id") or now_stamp())
    destination = target / ".aaop"
    if destination.exists():
        archive_root = destination / "runtime" / "install-recovery"
        archive_root.mkdir(parents=True, exist_ok=True)
        archive = archive_root / txid
    else:
        archive = target / f".aaop-install-recovery-{txid}"
    if archive.exists():
        raise SystemExit(f"Cannot archive recovered transaction because destination exists: {archive}")
    transaction.replace(archive)
    return archive


def recover_interrupted_transaction(target: Path) -> Path:
    transaction = transaction_root(target)
    if not transaction.is_dir():
        raise SystemExit(f"No interrupted AAOP transaction found at {transaction}")
    metadata = read_transaction_metadata(transaction)
    state = str(metadata.get("state") or "unknown")
    if state not in {"prepared", "promoting", "rollback-failed"}:
        raise SystemExit(
            f"Interrupted AAOP transaction has non-recoverable state {state!r}; inspect {transaction} manually"
        )
    try:
        rollback_transaction(
            target,
            transaction,
            metadata,
            preserve_interrupted_current=True,
        )
    except BaseException:
        metadata["state"] = "rollback-failed"
        try:
            write_transaction_metadata(transaction, metadata)
        except Exception:
            pass
        raise
    return archive_recovered_transaction(target, transaction, metadata)


def commit_transaction(transaction: Path) -> None:
    shutil.rmtree(transaction)


def upsert_block(path: Path, block: str) -> str:
    block = block.rstrip() + "\n"
    if not path.exists():
        atomic_write_text(path, block)
        return "created"

    text = path.read_text(encoding="utf-8")
    begin_count = text.count(AAOP_BEGIN)
    end_count = text.count(AAOP_END)

    if begin_count == 0 and end_count == 0:
        separator = "" if not text or text.endswith("\n\n") else "\n\n"
        atomic_write_text(path, text + separator + block)
        return "appended"

    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    existing = text[start:end]
    replacement = block.rstrip("\n")
    if existing == replacement:
        return "already-current"

    atomic_write_text(path, text[:start] + replacement + text[end:])
    return "updated"


def remove_block(path: Path) -> str:
    if not path.exists():
        return "missing-file"
    text = path.read_text(encoding="utf-8")
    if AAOP_BEGIN not in text and AAOP_END not in text:
        return "absent"

    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    atomic_write_text(path, text[:start] + text[end:])
    return "removed"


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
            atomic_copy_file(source, target_file)
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
        assert isinstance(raw_files, dict)
        previous_files = {str(key): str(value) for key, value in raw_files.items()}
    else:
        legacy_upgrade = True

    stamp = now_stamp()
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
        atomic_copy_file(source, target_file)

    write_manifest(destination, version, files)
    return "upgraded", sorted(set(backups)), legacy_upgrade


def planned_managed_paths(source_package: Path, target: Path, upgrade: bool) -> set[str]:
    planned = set(source_files(source_package))
    destination = target / ".aaop"
    if destination.exists() and upgrade:
        manifest = read_manifest(destination)
        if manifest is not None:
            raw_files = manifest.get("files", {})
            assert isinstance(raw_files, dict)
            planned.update(str(key) for key in raw_files)
    return {validate_managed_relative(relative) for relative in planned}


def install_or_upgrade(
    source_package: Path,
    target: Path,
    *,
    upgrade: bool,
) -> tuple[str, list[str], bool, str, str]:
    ensure_no_interrupted_transaction(target)
    planned = planned_managed_paths(source_package, target, upgrade)
    transaction, metadata = begin_transaction(
        target,
        planned,
        "upgrade" if upgrade else "install",
    )
    try:
        mode, backups, legacy_upgrade = copy_managed_files(source_package, target, upgrade)
        agents_status = upsert_block(target / "AGENTS.md", AGENTS_BLOCK)
        claude_status = upsert_block(target / "CLAUDE.md", CLAUDE_BLOCK)
    except BaseException:
        try:
            rollback_transaction(
                target,
                transaction,
                metadata,
                preserve_interrupted_current=False,
            )
            shutil.rmtree(transaction, ignore_errors=True)
        except BaseException as rollback_exc:
            metadata["state"] = "rollback-failed"
            try:
                write_transaction_metadata(transaction, metadata)
            except Exception:
                pass
            raise SystemExit(
                f"AAOP lifecycle mutation failed and rollback also failed. Preserve {transaction} "
                f"for explicit recovery. Rollback error: {rollback_exc}"
            ) from rollback_exc
        raise
    commit_transaction(transaction)
    return mode, backups, legacy_upgrade, agents_status, claude_status


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
    assert isinstance(raw_files, dict)
    files = {str(key): str(value) for key, value in raw_files.items()}
    raw_bootstrap = manifest.get("bootstrap_blocks", {})
    bootstrap_hashes = (
        {str(key): str(value) for key, value in raw_bootstrap.items()}
        if isinstance(raw_bootstrap, dict)
        else {}
    )
    version = str(manifest.get("aaop_version") or "unknown")
    stamp = now_stamp()
    backup_root = destination / "runtime" / "uninstall-backups" / f"from-{version}-{stamp}"

    backups: list[str] = []
    bootstrap_backups: list[str] = []
    removed: list[str] = []
    missing: list[str] = []

    for relative, installed_hash in sorted(files.items()):
        path = destination / validate_managed_relative(relative)
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

    for name in BOOTSTRAP_FILES:
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
        path = destination / validate_managed_relative(relative)
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


def transactional_uninstall(target: Path) -> dict[str, object]:
    ensure_no_interrupted_transaction(target)
    destination = target / ".aaop"
    manifest = read_manifest(destination)
    if manifest is None:
        raise SystemExit(
            "Cannot safely uninstall a legacy AAOP package without .aaop/.install-manifest.json; "
            "upgrade first to establish ownership."
        )
    raw_files = manifest.get("files", {})
    assert isinstance(raw_files, dict)
    planned = {validate_managed_relative(relative) for relative in raw_files}
    transaction, metadata = begin_transaction(target, planned, "uninstall")
    try:
        result = uninstall_aaop(target)
    except BaseException:
        try:
            rollback_transaction(
                target,
                transaction,
                metadata,
                preserve_interrupted_current=False,
            )
            shutil.rmtree(transaction, ignore_errors=True)
        except BaseException as rollback_exc:
            metadata["state"] = "rollback-failed"
            try:
                write_transaction_metadata(transaction, metadata)
            except Exception:
                pass
            raise SystemExit(
                f"AAOP uninstall failed and rollback also failed. Preserve {transaction} for "
                f"explicit recovery. Rollback error: {rollback_exc}"
            ) from rollback_exc
        raise
    commit_transaction(transaction)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install, safely upgrade, recover, or safely remove AAOP in a project"
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
    actions.add_argument(
        "--recover-interrupted",
        action="store_true",
        help=(
            "Explicitly roll back an interrupted journaled AAOP lifecycle mutation. The "
            "interrupted current state is backed up before restoration."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Legacy alias for --upgrade. No destructive directory replacement is performed.",
    )
    args = parser.parse_args()

    if (args.uninstall or args.recover_interrupted) and args.force:
        parser.error("--force is an upgrade alias and cannot be combined with uninstall/recovery")

    source = Path(__file__).resolve().parents[1]
    source_package = source / ".aaop"
    target = args.target.expanduser().resolve()

    if args.recover_interrupted:
        if not target.exists():
            raise SystemExit(f"Target project does not exist: {target}")
        archive = recover_interrupted_transaction(target)
        print("AAOP interrupted lifecycle mutation rolled back")
        print(f"  preserved interrupted-state backup: {archive}")
        print("  next: run health/ready, then retry the intended lifecycle action from a trusted source")
        return 0

    if args.uninstall:
        if not target.exists():
            raise SystemExit(f"Target project does not exist: {target}")
        validate_block_markers(target / "AGENTS.md")
        validate_block_markers(target / "CLAUDE.md")
        result = transactional_uninstall(target)
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

    mode, backups, legacy_upgrade, agents_status, claude_status = install_or_upgrade(
        source_package,
        target,
        upgrade=args.upgrade or args.force,
    )

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
    print("Safe removal/recovery: use the trusted bootstrap lifecycle surface")
    print(
        "Next: open the target project in your existing AI host and describe what you "
        "want in ordinary language."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
