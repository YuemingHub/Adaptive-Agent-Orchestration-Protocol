#!/usr/bin/env python3
"""Validate AAOP stable-managed release identity and source-freshness behavior without network."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / ".aaop" / "tools" / "source_freshness.py"
VERSION_PATH = ROOT / ".aaop" / "VERSION"
VERSIONING_PATH = ROOT / ".aaop" / "VERSIONING.md"
RELEASE_PATH = ROOT / ".aaop" / "PRODUCTION_RELEASE.json"
INTAKE_PATH = ROOT / ".aaop" / "skills" / "developer-intake" / "SKILL.md"
README_PATH = ROOT / "README.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_tool() -> ModuleType:
    spec = importlib.util.spec_from_file_location("aaop_source_freshness_test", TOOL_PATH)
    require(spec is not None and spec.loader is not None, "cannot load source_freshness tool")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_package(root: Path, *, version: str, kind: str, ref: str | None) -> Path:
    package = root / ".aaop"
    (package / "runtime").mkdir(parents=True)
    (package / "VERSION").write_text(version + "\n", encoding="utf-8")
    payload = {
        "schema_version": 1,
        "aaop_version": version,
        "source": {"kind": kind, "ref": ref},
        "manifest_schema_version": 2,
        "managed_file_count": 1,
        "package_fingerprint": "0" * 64,
        "recorded_at": "2026-08-11T00:00:00Z",
        "authority": "diagnostic-only",
    }
    (package / "runtime" / "install-provenance.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return package


def main() -> int:
    require(TOOL_PATH.is_file(), "missing source_freshness tool")
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    require(version == "1.1.0", f"v1.1 source-freshness release expected, got {version!r}")

    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    require(release.get("package_version") == version, "production release identity must match VERSION")
    serialized_release = json.dumps(release, ensure_ascii=False).lower()
    for phrase in (
        "new package release identity",
        "stable-managed source freshness",
        "do not move stable",
    ):
        require(phrase in serialized_release, f"production release contract missing stable identity invariant: {phrase}")

    versioning = VERSIONING_PATH.read_text(encoding="utf-8").lower()
    for phrase in (
        "do not fast-forward `stable`",
        "new semver release identity",
        "stable-managed",
        "health` / `ready",
    ):
        require(phrase in versioning, f"VERSIONING missing stable freshness rule: {phrase}")

    intake = INTAKE_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Control-plane source freshness before takeover",
        "python .aaop/tools/source_freshness.py --json",
        "canonical state-preserving **stable bootstrap**",
        "Do not build another updater",
    ):
        require(phrase in intake, f"developer intake missing source-freshness behavior: {phrase}")

    readme = README_PATH.read_text(encoding="utf-8")
    require("**v1.1.0 — production release line" in readme, "README status must identify v1.1.0")
    require("source_freshness.py" in readme, "README must document source freshness")

    tool = load_tool()
    original_fetch = tool.fetch_stable_version
    try:
        with tempfile.TemporaryDirectory(prefix="aaop-source-freshness-") as tmp:
            root = Path(tmp)

            current = write_package(root / "current", version="1.1.0", kind="official-ref", ref="stable")
            tool.fetch_stable_version = lambda timeout=5.0: "1.1.0"
            report = tool.inspect(current)
            require(report["state"] == "current" and report["policy"] == "stable-managed", f"current stable classification failed: {report}")

            stale = write_package(root / "stale", version="1.0.0", kind="official-ref", ref="stable")
            report = tool.inspect(stale)
            require(report["state"] == "stale", f"stale stable classification failed: {report}")
            require(report["stable_version"] == "1.1.0", f"stale report missing stable identity: {report}")
            require("state-preserving stable bootstrap" in report["next_action"], f"stale report must reuse canonical lifecycle: {report}")

            def offline(timeout: float = 5.0) -> str:
                raise RuntimeError("simulated offline")

            tool.fetch_stable_version = offline
            offline_package = write_package(root / "offline", version="1.1.0", kind="official-ref", ref="stable")
            report = tool.inspect(offline_package)
            require(report["state"] == "unknown", f"offline stable must remain unknown: {report}")
            require("continuing independent authorized work" in report["next_action"], f"offline unknown must remain scoped: {report}")

            exact = write_package(root / "exact", version="1.0.0", kind="official-ref", ref="a" * 40)
            report = tool.inspect(exact)
            require(report["state"] == "frozen" and report["policy"] == "exact-frozen", f"exact pin must remain frozen: {report}")

            local = write_package(root / "archive", version="1.0.0", kind="local-archive", ref=None)
            report = tool.inspect(local)
            require(report["state"] == "not-managed", f"local archive must not auto-follow stable: {report}")
    finally:
        tool.fetch_stable_version = original_fetch

    print(
        "PASS source freshness: v1.1 release identity is distinct; stable-managed current/stale/offline and exact-frozen/local policies remain separate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
