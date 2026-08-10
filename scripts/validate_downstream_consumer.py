#!/usr/bin/env python3
"""Validate a real downstream MingOS snapshot against the exact AAOP candidate tree.

The workflow resolves/pins the consumer commit and creates the checkout. This script
then proves stable-AAOP -> candidate-AAOP upgrade compatibility without writing to
the downstream repository remote.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

AAOP_BEGIN = "<!-- AAOP:BEGIN -->"
AAOP_END = "<!-- AAOP:END -->"
ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_STABLE_COMMIT = "036412c4446447cf2170f2aeadf9320450f7481a"
EXPECTED_CANDIDATE_VERSION = "1.0.0"
AUTHORITY_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "CURRENT_PROJECT_STATUS.md",
    "CURRENT_STATE.md",
    "README.md",
    "package.json",
    "package-lock.json",
    "pyproject.toml",
)


def run(*args: object, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = [str(arg) for arg in args]
    completed = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    if completed.returncode != 0:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"cwd={cwd}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def strip_aaop_block(text: str) -> str:
    begin_count = text.count(AAOP_BEGIN)
    end_count = text.count(AAOP_END)
    if begin_count == 0 and end_count == 0:
        return text
    if begin_count != 1 or end_count != 1:
        raise AssertionError(
            f"consumer bootstrap markers malformed: begin={begin_count} end={end_count}"
        )
    start = text.index(AAOP_BEGIN)
    end = text.index(AAOP_END, start) + len(AAOP_END)
    before = text[:start]
    after = text[end:]
    # upsert_block inserts exactly one separator before a new AAOP block when a
    # project file already exists. Normalize only that installer-owned separator.
    if before.endswith("\n\n") and not after:
        before = before[:-1]
    return before + after


def tracked_authority_snapshot(consumer: Path) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for relative in AUTHORITY_FILES:
        path = consumer / relative
        if path.is_file():
            result[relative] = path.read_bytes()
    if "AGENTS.md" not in result:
        raise AssertionError("real MingOS consumer snapshot must provide AGENTS.md project authority")
    return result


def assert_authority_preserved(consumer: Path, before: dict[str, bytes]) -> None:
    for relative, original in before.items():
        path = consumer / relative
        if not path.is_file():
            raise AssertionError(f"consumer authority file disappeared after AAOP upgrade: {relative}")
        if relative in {"AGENTS.md", "CLAUDE.md"}:
            current = path.read_text(encoding="utf-8")
            stripped = strip_aaop_block(current).encode("utf-8")
            if stripped != original:
                raise AssertionError(f"AAOP changed consumer-owned text outside its markers: {relative}")
        elif path.read_bytes() != original:
            raise AssertionError(f"AAOP changed consumer authority/product file: {relative}")


def build_candidate_archive(path: Path) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in ROOT.rglob("*"):
            if not source.is_file() or ".git" in source.parts:
                continue
            relative = source.relative_to(ROOT)
            archive.write(source, (Path("aaop-source") / relative).as_posix())


def discover_consumer_validation(consumer: Path) -> list[list[str]]:
    package = consumer / "package.json"
    commands: list[list[str]] = []
    if package.is_file():
        payload = json.loads(package.read_text(encoding="utf-8"))
        scripts = payload.get("scripts", {}) if isinstance(payload, dict) else {}
        if not isinstance(scripts, dict):
            scripts = {}
        for name in ("test:ci", "test", "check", "lint"):
            if isinstance(scripts.get(name), str) and scripts[name].strip():
                commands.append(["npm", "run", name])
        if not commands and isinstance(scripts.get("build"), str) and scripts["build"].strip():
            commands.append(["npm", "run", "build"])
    for candidate in (
        ["python", "scripts/validate.py"],
        ["python", "scripts/test.py"],
    ):
        if (consumer / candidate[1]).is_file():
            commands.append(candidate)
    if not commands:
        raise AssertionError(
            "MingOS consumer snapshot exposes no executable validation script among "
            "npm test:ci/test/check/lint/build or scripts/validate.py/scripts/test.py"
        )
    return commands


def prepare_node_dependencies(consumer: Path) -> None:
    if not (consumer / "package.json").is_file():
        return
    if (consumer / "package-lock.json").is_file():
        run("npm", "ci", cwd=consumer)
    elif (consumer / "npm-shrinkwrap.json").is_file():
        run("npm", "ci", cwd=consumer)
    else:
        run("npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", cwd=consumer)


def run_consumer_validation(consumer: Path, commands: list[list[str]], phase: str) -> None:
    for command in commands:
        completed = run(*command, cwd=consumer)
        print(f"PASS downstream {phase}: {' '.join(command)}")
        if completed.stdout.strip():
            print(completed.stdout[-2000:])


def assert_no_unexpected_tracked_diff(consumer: Path) -> None:
    completed = run("git", "diff", "--name-only", cwd=consumer)
    changed = {line.strip() for line in completed.stdout.splitlines() if line.strip()}
    unexpected = changed - {"AGENTS.md", "CLAUDE.md"}
    if unexpected:
        raise AssertionError(f"AAOP consumer upgrade changed unexpected tracked files: {sorted(unexpected)}")


def bootstrap_previous_stable(consumer: Path) -> None:
    url = (
        "https://raw.githubusercontent.com/YuemingHub/"
        "Adaptive-Agent-Orchestration-Protocol/"
        f"{PREVIOUS_STABLE_COMMIT}/scripts/bootstrap.py"
    )
    script = consumer.parent / "aaop-stable-bootstrap.py"
    run("curl", "-fsSL", url, "-o", script)
    run(
        sys.executable,
        script,
        "--target",
        consumer,
        "--ref",
        PREVIOUS_STABLE_COMMIT,
    )
    version = (consumer / ".aaop" / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.27.0":
        raise AssertionError(f"previous stable consumer install expected 0.27.0, got {version}")


def seed_consumer_continuity(consumer: Path) -> dict[str, object]:
    journey = consumer / ".aaop" / "tools" / "journey.py"
    run(
        sys.executable,
        journey,
        "start",
        "idea-to-production",
        "--goal",
        "Preserve MingOS project authority while validating AAOP v1 upgrade compatibility",
        "--route",
        "understand-review",
        "--reason",
        "real downstream stable-to-v1 release pressure test",
    )
    runtime = consumer / ".aaop" / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "consumer-release-sentinel.txt").write_text("preserve-me\n", encoding="utf-8")
    local_note = consumer / ".aaop" / "consumer-owned-note.txt"
    local_note.write_text("consumer-owned\n", encoding="utf-8")
    status = run(
        sys.executable,
        journey,
        "status",
        "idea-to-production",
        "--json",
    )
    payload = json.loads(status.stdout)
    if payload.get("revision") != 1:
        raise AssertionError(f"expected seeded Journey revision 1, got {payload}")
    return payload


def upgrade_to_candidate(consumer: Path, archive: Path) -> None:
    run(
        sys.executable,
        ROOT / "scripts" / "bootstrap.py",
        "--archive",
        archive,
        "--target",
        consumer,
    )
    version = (consumer / ".aaop" / "VERSION").read_text(encoding="utf-8").strip()
    if version != EXPECTED_CANDIDATE_VERSION:
        raise AssertionError(f"candidate consumer upgrade expected {EXPECTED_CANDIDATE_VERSION}, got {version}")


def assert_candidate_state(consumer: Path, seeded: dict[str, object]) -> None:
    ready = json.loads(
        run(
            sys.executable,
            consumer / ".aaop" / "tools" / "aaop.py",
            "ready",
            consumer,
            "--json",
        ).stdout
    )
    if ready.get("ready") is not True or ready.get("health_state") != "healthy":
        raise AssertionError(f"candidate consumer is not READY/healthy: {ready}")
    if ready.get("provenance_state") != "verified":
        raise AssertionError(f"candidate consumer provenance is not verified: {ready}")
    source = ready.get("provenance_source")
    if source != {"kind": "local-archive", "ref": None}:
        raise AssertionError(f"candidate provenance should identify exact local candidate archive: {source}")

    journey = json.loads(
        run(
            sys.executable,
            consumer / ".aaop" / "tools" / "journey.py",
            "status",
            "idea-to-production",
            "--json",
        ).stdout
    )
    for field in ("goal", "revision", "cycle", "current_route"):
        if journey.get(field) != seeded.get(field):
            raise AssertionError(
                f"Journey continuity changed during package upgrade: {field}: before={seeded.get(field)!r} after={journey.get(field)!r}"
            )
    if (consumer / ".aaop" / "runtime" / "consumer-release-sentinel.txt").read_text(encoding="utf-8") != "preserve-me\n":
        raise AssertionError("AAOP runtime continuity sentinel was not preserved")
    if (consumer / ".aaop" / "consumer-owned-note.txt").read_text(encoding="utf-8") != "consumer-owned\n":
        raise AssertionError("consumer-owned .aaop file was not preserved")


def main() -> int:
    consumer_env = os.environ.get("AAOP_DOWNSTREAM_CONSUMER")
    if not consumer_env:
        raise SystemExit("AAOP_DOWNSTREAM_CONSUMER must point to the checked-out MingOS snapshot")
    consumer = Path(consumer_env).resolve()
    if not (consumer / ".git").exists():
        raise SystemExit(f"downstream consumer is not a Git checkout: {consumer}")

    consumer_sha = run("git", "rev-parse", "HEAD", cwd=consumer).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", consumer_sha):
        raise AssertionError(f"invalid downstream commit SHA: {consumer_sha}")
    print(f"DOWNSTREAM_CONSUMER_REPO=YuemingHub/MingOS")
    print(f"DOWNSTREAM_CONSUMER_SHA={consumer_sha}")
    print(f"AAOP_CANDIDATE_SHA={os.environ.get('AAOP_CANDIDATE_SHA', 'unknown')}")

    before = tracked_authority_snapshot(consumer)
    validation = discover_consumer_validation(consumer)
    print("DOWNSTREAM_VALIDATION_COMMANDS=" + json.dumps(validation, ensure_ascii=False))

    prepare_node_dependencies(consumer)
    run_consumer_validation(consumer, validation, "baseline")
    if run("git", "diff", "--name-only", cwd=consumer).stdout.strip():
        raise AssertionError("downstream baseline validation itself changed tracked files; cannot attribute later diff to AAOP")

    bootstrap_previous_stable(consumer)
    seeded = seed_consumer_continuity(consumer)
    assert_authority_preserved(consumer, before)
    assert_no_unexpected_tracked_diff(consumer)

    with tempfile.TemporaryDirectory(prefix="aaop-v1-consumer-") as tmp:
        archive = Path(tmp) / "aaop-candidate.zip"
        build_candidate_archive(archive)
        upgrade_to_candidate(consumer, archive)

    assert_candidate_state(consumer, seeded)
    assert_authority_preserved(consumer, before)
    assert_no_unexpected_tracked_diff(consumer)
    run_consumer_validation(consumer, validation, "after-aaop-v1-upgrade")

    print("PASS real downstream consumer stable-to-v1 compatibility")
    print(f"PASS downstream repo=YuemingHub/MingOS commit={consumer_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
