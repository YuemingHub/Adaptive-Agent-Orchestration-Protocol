#!/usr/bin/env python3
"""Install or safely upgrade AAOP from the official GitHub repository.

This script is intentionally standard-library only so it can be executed directly
from stdin, for example:

    curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target .

Windows PowerShell (with the Python launcher):

    curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | py - --target .

The bootstrap downloads one official repository archive into a temporary directory,
validates the expected AAOP source shape, delegates all target mutation to the
canonical state-preserving scripts/install.py, then runs the installed AAOP ready
check. It installs no third-party provider and requests no secret.
"""

from __future__ import annotations

import argparse
import io
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

OWNER = "YuemingHub"
REPO = "Adaptive-Agent-Orchestration-Protocol"
DEFAULT_REF = "main"
MAX_ARCHIVE_BYTES = 50 * 1024 * 1024
USER_AGENT = "AAOP-bootstrap/1"


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
                f"AAOP bootstrap: official archive exceeded safety limit of {limit} bytes"
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
            f"AAOP bootstrap: archive exceeded safety limit of {MAX_ARCHIVE_BYTES} bytes"
        )
    return data


def validate_zip_member(name: str) -> None:
    normalized = name.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part not in ("", ".")]
    if normalized.startswith("/") or any(part == ".." for part in parts):
        raise SystemExit(f"AAOP bootstrap: unsafe archive path {name!r}")


def extract_source(data: bytes, destination: Path) -> Path:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if not names:
                raise SystemExit("AAOP bootstrap: downloaded archive is empty")
            for name in names:
                validate_zip_member(name)
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


def target_mode(target: Path) -> str:
    package = target / ".aaop"
    if not package.exists():
        return "install"

    recognizable = (
        (package / ".install-manifest.json").is_file()
        or (package / "ORCHESTRATOR.md").is_file()
        or (package / "VERSION").is_file()
    )
    if not recognizable:
        raise SystemExit(
            f"AAOP bootstrap: {package} already exists but is not recognizable as AAOP. "
            "Refusing to claim it automatically; review the directory and use the canonical "
            "installer explicitly if migration is intended."
        )
    return "upgrade"


def run_install(source: Path, target: Path, mode: str) -> None:
    command = [sys.executable, str(source / "scripts" / "install.py"), str(target)]
    if mode == "upgrade":
        command.append("--upgrade")
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
        description="Install or safely upgrade AAOP in a project without cloning the AAOP repository"
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
        help="Official GitHub ref to install (default: main; use a commit/tag for pinning)",
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

    target = args.target.expanduser().resolve()
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
        print(f"AAOP bootstrap: {mode} {version} from {source_label}")
        run_install(source, target, mode)

    if args.skip_ready:
        print("AAOP bootstrap complete")
        print(f"  target: {target}")
        print(f"  ready check: {sys.executable} .aaop/tools/aaop.py ready .")
        return 0

    ready_code = run_ready(target)
    if ready_code != 0:
        print(
            "AAOP bootstrap: installation completed, but readiness check found something to review.",
            file=sys.stderr,
        )
        return ready_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
