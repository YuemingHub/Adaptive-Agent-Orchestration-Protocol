#!/usr/bin/env python3
"""Install, upgrade, recover, or safely remove AAOP from the official GitHub repository.

This script is intentionally standard-library only so it can be executed directly
from stdin. Production/default usage follows the deliberately promoted ``stable``
branch rather than the fast-moving ``main`` development branch:

    curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target .

Windows PowerShell (with the Python launcher):

    curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target .

Use ``--ref main`` only when intentionally opting into the development/edge
channel. Use an exact commit ref when byte-for-byte source revision reproducibility
matters.

Re-running the same stable install command upgrades a recognizable AAOP installation
only when the stable channel itself has been deliberately promoted. Add --uninstall
for manifest-scoped removal. If a journaled lifecycle operation was interrupted,
use --recover-interrupted from a trusted AAOP source before retrying. The bootstrap
installs no third-party provider and requests no secret.
"""

from __future__ import annotations

import argparse
import io
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

OWNER = "YuemingHub"
REPO = "Adaptive-Agent-Orchestration-Protocol"
DEFAULT_REF = "stable"
TRANSACTION_DIR_NAME = ".aaop-install-transaction"
MAX_ARCHIVE_BYTES = 50 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 4096
MAX_MEMBER_UNCOMPRESSED_BYTES = 32 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED_BYTES = 128 * 1024 * 1024
USER_AGENT = "AAOP-bootstrap/2"
LEGACY_ORCHESTRATOR_MARKERS = (
    "# AAOP Runtime Protocol",
    "Adaptive Agent Orchestration Protocol (AAOP)",
)


def official_archive_url(ref: str) -> str:
    clean = ref.strip()
    if not clean:
        raise SystemExit("AAOP bootstrap: --ref must not be empty")
    encoded = urllib.parse.quote(clean, safe="")
    return f"https://github.com/{OWNER}/{REPO}/archive/{encoded}.zip"


def read_limited(response: object, limit: int = MAX_ARCHIVE_BYTES) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(1024 * 1024, limit + 1 - total))  # type: ignore[attr-defined]
        if not chunk:
            break
        total += len(chunk)
        if total > limit:
            raise SystemExit(
                f"AAOP bootstrap: official archive exceeded compressed safety limit of {limit} bytes"
            )
        chunks.append(chunk)
    return b"".join(chunks)


def download_archive(ref: str) -> bytes:
    url = official_archive_url(ref)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return read_limited(response)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"AAOP bootstrap: failed to download {url}: {exc}") from exc


def load_archive(path: Path) -> bytes:
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise SystemExit(f"AAOP bootstrap: cannot read archive {path}: {exc}") from exc
    if len(data) > MAX_ARCHIVE_BYTES:
        raise SystemExit(
            f"AAOP bootstrap: archive exceeded compressed safety limit of {MAX_ARCHIVE_BYTES} bytes"
        )
    return data


def validate_zip_member(name: str) -> None:
    normalized = name.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part not in ("", ".")]
    has_windows_drive = bool(parts and len(parts[0]) == 2 and parts[0][1] == ":")
    if (
        normalized.startswith("/")
        or normalized.startswith("//")
        or has_windows_drive
        or any(part == ".." for part in parts)
    ):
        raise SystemExit(f"AAOP bootstrap: unsafe archive path {name!r}")


def validate_archive_resources(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    infos = archive.infolist()
    if not infos:
        raise SystemExit("AAOP bootstrap: downloaded archive is empty")
    if len(infos) > MAX_ARCHIVE_MEMBERS:
        raise SystemExit(
            "AAOP bootstrap: archive exceeded member-count safety limit "
            f"of {MAX_ARCHIVE_MEMBERS}"
        )

    expanded_total = 0
    for info in infos:
        validate_zip_member(info.filename)
        if info.flag_bits & 0x1:
            raise SystemExit(
                f"AAOP bootstrap: encrypted archive member is not allowed: {info.filename!r}"
            )
        if info.file_size > MAX_MEMBER_UNCOMPRESSED_BYTES:
            raise SystemExit(
                "AAOP bootstrap: archive member exceeded uncompressed safety limit "
                f"of {MAX_MEMBER_UNCOMPRESSED_BYTES} bytes: {info.filename!r}"
            )
        expanded_total += info.file_size
        if expanded_total > MAX_TOTAL_UNCOMPRESSED_BYTES:
            raise SystemExit(
                "AAOP bootstrap: archive exceeded total uncompressed safety limit "
                f"of {MAX_TOTAL_UNCOMPRESSED_BYTES} bytes"
            )
    return infos


def extract_source(data: bytes, destination: Path) -> Path:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            validate_archive_resources(archive)
            archive.extractall(destination)
    except zipfile.BadZipFile as exc:
        raise SystemExit("AAOP bootstrap: downloaded content is not a valid zip archive") from exc

    candidates: list[Path] = []
    for child in destination.iterdir():
        if not child.is_dir():
            continue
        if (child / "scripts" / "install.py").is_file() and (child / ".aaop").is_dir():
            candidates.append(child)

    if len(candidates) != 1:
        raise SystemExit(
            "AAOP bootstrap: archive did not contain exactly one recognizable AAOP source root"
        )
    return candidates[0]


def source_version(source: Path) -> str:
    path = source / ".aaop" / "VERSION"
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(
            "AAOP bootstrap: source is incomplete; authoritative .aaop/VERSION is unavailable"
        ) from exc
    if not value:
        raise SystemExit(
            "AAOP bootstrap: source is incomplete; authoritative .aaop/VERSION is empty"
        )
    return value


def legacy_aaop_identity(package: Path) -> bool:
    orchestrator = package / "ORCHESTRATOR.md"
    if not orchestrator.is_file():
        return False
    try:
        text = orchestrator.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    header = text[:4096]
    return any(marker in header for marker in LEGACY_ORCHESTRATOR_MARKERS)


def target_mode(target: Path) -> str:
    interrupted = target / TRANSACTION_DIR_NAME
    if interrupted.exists():
        raise SystemExit(
            f"AAOP bootstrap: interrupted lifecycle transaction exists at {interrupted}. "
            "Run this trusted bootstrap with --recover-interrupted before install/upgrade/uninstall."
        )

    package = target / ".aaop"
    if not package.exists():
        return "install"

    if (package / ".install-manifest.json").is_file():
        return "upgrade"
    if legacy_aaop_identity(package):
        return "upgrade"

    raise SystemExit(
        f"AAOP bootstrap: {package} already exists but AAOP ownership cannot be proven. "
        "A generic VERSION file or directory name is not sufficient. Refusing to claim "
        "it automatically; review the directory and use the canonical installer explicitly "
        "if migration is intended."
    )


def run_installer(source: Path, target: Path, mode: str) -> None:
    command = [sys.executable, str(source / "scripts" / "install.py"), str(target)]
    if mode == "upgrade":
        command.append("--upgrade")
    elif mode == "uninstall":
        command.append("--uninstall")
    elif mode == "recover":
        command.append("--recover-interrupted")
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def run_ready(target: Path) -> int:
    command = [
        sys.executable,
        str(target / ".aaop" / "tools" / "aaop.py"),
        "ready",
        str(target),
    ]
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install, safely upgrade, recover, or safely remove AAOP without cloning its repository"
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target project directory (default: current directory)",
    )
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help="Official GitHub ref to use (default: stable; use main only for edge development or a commit for exact pinning)",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Safely remove only manifest-owned AAOP files and marked bootstrap blocks",
    )
    parser.add_argument(
        "--recover-interrupted",
        action="store_true",
        help="Explicitly roll back a journaled AAOP lifecycle operation that was interrupted",
    )
    parser.add_argument(
        "--archive",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--skip-ready",
        action="store_true",
        help="Skip the post-install readiness summary",
    )
    args = parser.parse_args()

    if args.uninstall and args.recover_interrupted:
        parser.error("--uninstall and --recover-interrupted are mutually exclusive")

    target = args.target.expanduser().resolve()
    if args.recover_interrupted:
        if not target.exists():
            raise SystemExit(f"AAOP bootstrap: target project does not exist: {target}")
        mode = "recover"
    elif args.uninstall:
        if not target.exists():
            raise SystemExit(f"AAOP bootstrap: target project does not exist: {target}")
        mode = "uninstall"
    else:
        target.mkdir(parents=True, exist_ok=True)
        mode = target_mode(target)

    if args.archive:
        data = load_archive(args.archive.expanduser().resolve())
        source_label = str(args.archive)
    else:
        data = download_archive(args.ref)
        source_label = f"official {OWNER}/{REPO}@{args.ref}"

    with tempfile.TemporaryDirectory(prefix="aaop-bootstrap-") as tmp:
        source = extract_source(data, Path(tmp))
        version = source_version(source)
        print(f"AAOP bootstrap: {mode} using {version} from {source_label}")
        run_installer(source, target, mode)

    if mode == "uninstall":
        print("AAOP bootstrap removal complete")
        return 0

    if mode == "recover":
        print("AAOP bootstrap recovery complete")

    if args.skip_ready:
        print("AAOP bootstrap complete")
        print(f"  target: {target}")
        print(f"  ready check: {sys.executable} .aaop/tools/aaop.py ready .")
        return 0

    if not (target / ".aaop" / "tools" / "aaop.py").is_file():
        print(
            "AAOP bootstrap: lifecycle action completed, but no installed AAOP package remains to run readiness against.",
            file=sys.stderr,
        )
        return 0

    ready_code = run_ready(target)
    if ready_code != 0:
        print(
            "AAOP bootstrap: lifecycle action completed, but readiness check found something to review.",
            file=sys.stderr,
        )
        return ready_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
