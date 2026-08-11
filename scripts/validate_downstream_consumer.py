#!/usr/bin/env python3
"""Validate one pinned real MingOS snapshot against the exact AAOP candidate tree.

The workflow checks out both AAOP and MingOS at explicit commits. This script then
proves stable-AAOP -> candidate-AAOP upgrade compatibility without writing to the
downstream remote. It preserves project authority, Journey continuity, a pre-seeded
Human-Agent Working Contract, project-owned AAOP/runtime state, and downstream tests.
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
EXPECTED_CONSUMER_REPO = "YuemingHub/MingOS"
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


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def candidate_version() -> str:
    path = ROOT / ".aaop" / "VERSION"
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise AssertionError(f"cannot read exact AAOP candidate VERSION: {exc}") from exc
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", value):
        raise AssertionError(f"invalid exact AAOP candidate VERSION: {value!r}")
    return value


def current_candidate_sha() -> str:
    sha = run("git", "rev-parse", "HEAD", cwd=ROOT).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise AssertionError(f"invalid AAOP candidate commit SHA: {sha!r}")
    return sha


def assert_bootstrap_text_preserved(current: str, original: str, *, relative: str) -> None:
    """Prove that only the installer-owned separator + AAOP block were added/updated.

    The old downstream validator deleted only the marker span and accidentally left
    the append separator/block trailing newline behind, producing a false positive on
    normal files that ended in one newline. This check instead models the installer's
    exact append contract and therefore remains strict about every project-owned byte.
    """

    begin_count = current.count(AAOP_BEGIN)
    end_count = current.count(AAOP_END)
    if begin_count != 1 or end_count != 1:
        raise AssertionError(
            f"consumer bootstrap markers malformed after AAOP mutation: {relative}: "
            f"begin={begin_count} end={end_count}"
        )
    start = current.index(AAOP_BEGIN)
    end = current.index(AAOP_END, start) + len(AAOP_END)
    before = current[:start]
    after = current[end:]

    # scripts/install.py::upsert_block appends exactly this separator when the
    # original project file has no AAOP block. The block itself always ends in one
    # newline. Candidate upgrades replace only marker-delimited content and preserve
    # this outside structure byte-for-byte.
    separator = "" if not original or original.endswith("\n\n") else "\n\n"
    expected_before = original + separator
    if before != expected_before:
        raise AssertionError(
            f"AAOP changed consumer-owned text before its marker block: {relative}"
        )
    if after != "\n":
        raise AssertionError(
            f"AAOP changed consumer-owned text after its marker block: {relative}: {after!r}"
        )


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
            raise AssertionError(f"consumer authority file disappeared after AAOP mutation: {relative}")
        if relative in {"AGENTS.md", "CLAUDE.md"}:
            assert_bootstrap_text_preserved(
                path.read_text(encoding="utf-8"),
                original.decode("utf-8"),
                relative=relative,
            )
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
    for candidate in (["python", "scripts/validate.py"], ["python", "scripts/test.py"]):
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
    if (consumer / "package-lock.json").is_file() or (consumer / "npm-shrinkwrap.json").is_file():
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
    run(sys.executable, script, "--target", consumer, "--ref", PREVIOUS_STABLE_COMMIT)
    version = (consumer / ".aaop" / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.27.0":
        raise AssertionError(f"previous stable consumer install expected 0.27.0, got {version}")


def working_contract_fixture() -> dict[str, object]:
    version = candidate_version()
    return {
        "schema_version": "1.0",
        "revision": 7,
        "collaboration": {
            "mode": "collaborative",
            "confirmed": True,
            "confirmed_at": "2026-08-11T00:00:00Z",
            "notes": ["real downstream continuity fixture"],
        },
        "alignment": {
            "state": "collecting",
            "goal": f"Preserve MingOS authority while validating AAOP {version}",
            "actor": "MingOS project owner",
            "situation": "real repository upgrade",
            "outcome": f"AAOP {version} can be adopted without losing project or collaboration continuity",
            "must": ["preserve MingOS project authority"],
            "non_goals": ["do not alter MingOS product behavior"],
            "constraints": ["downstream repository remains read-only remotely"],
            "success_evidence": ["MingOS tests remain green after upgrade"],
            "human_open_questions": ["fixture intentionally remains unaligned"],
            "confirmed_at": None,
        },
        "decision_ownership": {
            "human_owned": ["product intent and value tradeoffs"],
            "agent_owned": ["technical architecture within established constraints"],
            "joint": ["high-impact production or destructive change not already authorized"],
        },
        "task_pod_policy": {
            "default_single_agent": True,
            "max_members": 5,
            "accountable_owner_required": True,
            "independent_review_when_consequential": True,
            "handoff_required_between_pods": True,
            "role_provider_order": ["host-native", "project-local", "agency-agents-zh"],
        },
        "updated_at": "2026-08-11T00:00:00Z",
    }


def seed_consumer_continuity(consumer: Path) -> dict[str, object]:
    version = candidate_version()
    journey = consumer / ".aaop" / "tools" / "journey.py"
    run(
        sys.executable,
        journey,
        "start",
        "idea-to-production",
        "--goal",
        f"Preserve MingOS project authority while validating AAOP {version} upgrade compatibility",
        "--route",
        "understand-review",
        "--reason",
        "real downstream stable-to-candidate release pressure test",
    )
    runtime = consumer / ".aaop" / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "consumer-release-sentinel.txt").write_text("preserve-me\n", encoding="utf-8")
    local_note = consumer / ".aaop" / "consumer-owned-note.txt"
    local_note.write_text("consumer-owned\n", encoding="utf-8")

    contract_bytes = (json.dumps(working_contract_fixture(), ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    contract_path = runtime / "working-contract.json"
    contract_path.write_bytes(contract_bytes)

    status = run(sys.executable, journey, "status", "idea-to-production", "--json")
    payload = json.loads(status.stdout)
    if payload.get("revision") != 1:
        raise AssertionError(f"expected seeded Journey revision 1, got {payload}")
    return {
        "journey": payload,
        "working_contract_sha256": sha256_bytes(contract_bytes),
    }


def upgrade_to_candidate(consumer: Path, archive: Path) -> None:
    expected = candidate_version()
    run(sys.executable, ROOT / "scripts" / "bootstrap.py", "--archive", archive, "--target", consumer)
    version = (consumer / ".aaop" / "VERSION").read_text(encoding="utf-8").strip()
    if version != expected:
        raise AssertionError(f"candidate consumer upgrade expected {expected}, got {version}")


def assert_candidate_state(consumer: Path, seeded: dict[str, object]) -> None:
    ready = json.loads(
        run(sys.executable, consumer / ".aaop" / "tools" / "aaop.py", "ready", consumer, "--json").stdout
    )
    if ready.get("ready") is not True or ready.get("health_state") != "healthy":
        raise AssertionError(f"candidate consumer is not READY/healthy: {ready}")
    if ready.get("provenance_state") != "verified":
        raise AssertionError(f"candidate consumer provenance is not verified: {ready}")
    source = ready.get("provenance_source")
    if source != {"kind": "local-archive", "ref": None}:
        raise AssertionError(f"candidate provenance should identify exact local candidate archive: {source}")

    contract = ready.get("working_contract")
    if not isinstance(contract, dict):
        raise AssertionError(f"candidate readiness did not expose Working Contract state: {ready}")
    expected_contract_summary = {
        "state": "present",
        "mode": "collaborative",
        "alignment_state": "collecting",
        "execution_allowed": False,
        "revision": 7,
    }
    for key, expected in expected_contract_summary.items():
        if contract.get(key) != expected:
            raise AssertionError(
                f"Working Contract continuity changed during package upgrade: {key}: "
                f"expected={expected!r} actual={contract.get(key)!r}"
            )
    contract_path = consumer / ".aaop" / "runtime" / "working-contract.json"
    if sha256_bytes(contract_path.read_bytes()) != seeded["working_contract_sha256"]:
        raise AssertionError("Working Contract runtime bytes changed during package upgrade")

    journey = json.loads(
        run(
            sys.executable,
            consumer / ".aaop" / "tools" / "journey.py",
            "status",
            "idea-to-production",
            "--json",
        ).stdout
    )
    seeded_journey = seeded["journey"]
    assert isinstance(seeded_journey, dict)
    for field in ("goal", "revision", "cycle", "current_route"):
        if journey.get(field) != seeded_journey.get(field):
            raise AssertionError(
                f"Journey continuity changed during package upgrade: {field}: "
                f"before={seeded_journey.get(field)!r} after={journey.get(field)!r}"
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
    expected_consumer_sha = os.environ.get("AAOP_DOWNSTREAM_CONSUMER_SHA")
    if expected_consumer_sha and consumer_sha != expected_consumer_sha:
        raise AssertionError(
            f"downstream consumer checkout drifted: expected {expected_consumer_sha}, got {consumer_sha}"
        )

    candidate_sha = current_candidate_sha()
    version = candidate_version()
    expected_candidate_sha = os.environ.get("AAOP_CANDIDATE_SHA")
    if expected_candidate_sha and candidate_sha != expected_candidate_sha:
        raise AssertionError(
            f"AAOP candidate checkout drifted: expected {expected_candidate_sha}, got {candidate_sha}"
        )

    print(f"DOWNSTREAM_CONSUMER_REPO={EXPECTED_CONSUMER_REPO}")
    print(f"DOWNSTREAM_CONSUMER_SHA={consumer_sha}")
    print(f"AAOP_CANDIDATE_SHA={candidate_sha}")
    print(f"AAOP_CANDIDATE_VERSION={version}")

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

    with tempfile.TemporaryDirectory(prefix="aaop-candidate-consumer-") as tmp:
        archive = Path(tmp) / "aaop-candidate.zip"
        build_candidate_archive(archive)
        upgrade_to_candidate(consumer, archive)

    assert_candidate_state(consumer, seeded)
    assert_authority_preserved(consumer, before)
    assert_no_unexpected_tracked_diff(consumer)
    run_consumer_validation(consumer, validation, f"after-aaop-{version}-upgrade")

    print(f"PASS real downstream consumer stable-to-{version} compatibility")
    print(f"PASS downstream repo={EXPECTED_CONSUMER_REPO} commit={consumer_sha}")
    print(f"PASS exact AAOP candidate commit={candidate_sha} version={version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
