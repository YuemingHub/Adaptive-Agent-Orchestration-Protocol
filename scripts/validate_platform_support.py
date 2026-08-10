#!/usr/bin/env python3
"""Cross-platform production support smoke test for the current Python runtime."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_bootstrap():
    path = ROOT / "scripts" / "bootstrap.py"
    spec = importlib.util.spec_from_file_location("aaop_bootstrap_platform", path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(*args: object) -> subprocess.CompletedProcess[str]:
    command = [str(arg) for arg in args]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


def build_archive(path: Path) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in ROOT.rglob("*"):
            if not source.is_file() or ".git" in source.parts:
                continue
            relative = source.relative_to(ROOT)
            archive.write(source, (Path("aaop-source") / relative).as_posix())


def main() -> int:
    bootstrap = load_bootstrap()
    current = sys.version_info[:2]
    assert bootstrap.MIN_SUPPORTED_PYTHON <= current <= bootstrap.MAX_SUPPORTED_PYTHON, (
        current,
        bootstrap.MIN_SUPPORTED_PYTHON,
        bootstrap.MAX_SUPPORTED_PYTHON,
    )
    bootstrap.ensure_supported_python()

    with tempfile.TemporaryDirectory(prefix="aaop-platform-support-") as tmp:
        root = Path(tmp)
        archive = root / "aaop-source.zip"
        target = root / "project"
        target.mkdir()
        (target / "AGENTS.md").write_text("# Platform smoke project\n\nKEEP-PLATFORM-RULE\n", encoding="utf-8")
        build_archive(archive)

        install = run(
            sys.executable,
            ROOT / "scripts" / "bootstrap.py",
            "--archive",
            archive,
            "--target",
            target,
        )
        assert "AAOP bootstrap: install" in install.stdout, install.stdout
        assert "AAOP READY" in install.stdout, install.stdout
        assert "KEEP-PLATFORM-RULE" in (target / "AGENTS.md").read_text(encoding="utf-8")

        ready = run(
            sys.executable,
            target / ".aaop" / "tools" / "aaop.py",
            "ready",
            target,
            "--json",
        )
        payload = json.loads(ready.stdout)
        assert payload["ready"] is True, payload
        assert payload["health_state"] == "healthy", payload

        upgrade = run(
            sys.executable,
            ROOT / "scripts" / "bootstrap.py",
            "--archive",
            archive,
            "--target",
            target,
        )
        assert "AAOP bootstrap: upgrade" in upgrade.stdout, upgrade.stdout
        assert "AAOP READY" in upgrade.stdout, upgrade.stdout

        uninstall = run(
            sys.executable,
            ROOT / "scripts" / "bootstrap.py",
            "--archive",
            archive,
            "--target",
            target,
            "--uninstall",
        )
        assert "AAOP bootstrap removal complete" in uninstall.stdout, uninstall.stdout
        assert "KEEP-PLATFORM-RULE" in (target / "AGENTS.md").read_text(encoding="utf-8")
        assert not (target / ".aaop-install-transaction").exists()

    print(
        "PASS AAOP platform support smoke: "
        f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} "
        f"on {sys.platform}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
