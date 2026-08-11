#!/usr/bin/env python3
"""Validate the static AAOP production-release contract.

This validator cannot certify GitHub conclusions or downstream consumer behavior by
reading repository files. It proves that the candidate declares one coherent
production release line and that the required gate topology/safety/interaction
contracts are present. The release controller must still require live green workflow
results and real downstream candidate validation before stable promotion.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_PATH = ROOT / ".aaop" / "PRODUCTION_RELEASE.json"
VERSION_PATH = ROOT / ".aaop" / "VERSION"
JOURNEY_PATH = ROOT / ".aaop" / "journeys" / "idea-to-production.json"
WORKFLOW_ROOT = ROOT / ".github" / "workflows"
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
WORKFLOW_NAME_RE = re.compile(r"^name:\s*(.+?)\s*$", re.MULTILINE)
CONTENTS_READ_RE = re.compile(r"^\s*contents\s*:\s*read\s*(?:#.*)?$", re.MULTILINE | re.IGNORECASE)
CONTENTS_WRITE_RE = re.compile(r"^\s*contents\s*:\s*write\s*(?:#.*)?$", re.MULTILINE | re.IGNORECASE)


def load_json(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"JSON object required: {path}")
    return payload


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    require(RELEASE_PATH.is_file(), f"missing production release contract: {RELEASE_PATH}", errors)
    require(VERSION_PATH.is_file(), f"missing package VERSION: {VERSION_PATH}", errors)
    require(JOURNEY_PATH.is_file(), f"missing canonical Journey: {JOURNEY_PATH}", errors)
    if errors:
        raise SystemExit("\n".join(errors))

    release = load_json(RELEASE_PATH)
    journey = load_json(JOURNEY_PATH)
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    semver = SEMVER_RE.fullmatch(version)

    require(release.get("schema_version") == 1, "production release schema_version must be 1", errors)
    require(release.get("package_version") == version, "PRODUCTION_RELEASE package_version must equal .aaop/VERSION", errors)
    require(semver is not None, f"VERSION must be strict x.y.z SemVer: {version!r}", errors)
    if semver:
        require(int(semver.group(1)) >= 1, "production release line requires major version >= 1", errors)
    require(release.get("release_line") == "production", "release_line must be production", errors)
    require(release.get("stable_channel") == "stable", "stable_channel must be stable", errors)
    require(
        release.get("stable_promotion") == "post-merge-fast-forward-only",
        "stable promotion must remain post-merge-fast-forward-only",
        errors,
    )
    require(
        release.get("downstream_consumer_validation_required") is True,
        "real downstream consumer validation must remain a production requirement",
        errors,
    )

    canonical = release.get("canonical_journey")
    require(isinstance(canonical, dict), "canonical_journey contract must be an object", errors)
    if isinstance(canonical, dict):
        require(canonical.get("path") == ".aaop/journeys/idea-to-production.json", "canonical Journey path changed unexpectedly", errors)
        require(canonical.get("required_status") == "canonical", "production Journey required_status must be canonical", errors)
    require(journey.get("status") == "canonical", "idea-to-production Journey must graduate from experimental to canonical", errors)

    working = release.get("human_agent_working_contract")
    require(isinstance(working, dict), "human_agent_working_contract contract must be an object", errors)
    if isinstance(working, dict):
        require(working.get("skill") == ".aaop/skills/working-contract/SKILL.md", "working-contract Skill path drifted", errors)
        require(working.get("tool") == ".aaop/tools/working_contract.py", "working-contract tool path drifted", errors)
        require(working.get("schema") == ".aaop/schemas/working-contract.schema.json", "working-contract schema path drifted", errors)
        require(working.get("task_pod_max_members") == 5, "production Task Pod maximum must remain five", errors)
        require(working.get("handoff_schema") == ".aaop/schemas/task-handoff.schema.json", "Task Pod handoff schema path drifted", errors)

    platform = release.get("production_platform")
    require(isinstance(platform, dict), "production_platform contract must be an object", errors)
    if isinstance(platform, dict):
        require(platform.get("python_implementation") == "CPython", "production Python implementation must remain CPython", errors)
        require(platform.get("python_min") == "3.11", "production python_min must match tested 3.11 boundary", errors)
        require(platform.get("python_max") == "3.14", "production python_max must match tested 3.14 boundary", errors)
        operating_systems = platform.get("operating_systems")
        require(
            isinstance(operating_systems, list) and set(operating_systems) == {"linux", "windows", "macos"},
            "production OS set must match tested linux/windows/macos matrix",
            errors,
        )

    required_workflows = release.get("required_workflows")
    require(isinstance(required_workflows, list) and bool(required_workflows), "required_workflows must be a non-empty list", errors)
    actual_workflows = sorted(
        [path.name for path in WORKFLOW_ROOT.glob("*.yml")]
        + [path.name for path in WORKFLOW_ROOT.glob("*.yaml")]
    )
    if isinstance(required_workflows, list):
        declared = sorted(str(item) for item in required_workflows)
        require(len(declared) == len(set(declared)), "required_workflows contains duplicates", errors)
        require(declared == actual_workflows, f"production workflow topology drift: declared={declared} actual={actual_workflows}", errors)
        for filename in declared:
            path = WORKFLOW_ROOT / filename
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            match = WORKFLOW_NAME_RE.search(text)
            require(match is not None and bool(match.group(1).strip()), f"workflow has no top-level name: {filename}", errors)
            require(CONTENTS_READ_RE.search(text) is not None, f"workflow must explicitly declare contents: read: {filename}", errors)
            require(CONTENTS_WRITE_RE.search(text) is None, f"production workflow must not retain contents: write: {filename}", errors)

    if isinstance(required_workflows, list):
        require("validate-working-contract.yml" in required_workflows, "production topology must include validate-working-contract.yml", errors)
        require("validate-downstream-consumer.yml" in required_workflows, "production topology must include validate-downstream-consumer.yml", errors)

    required_docs = release.get("required_docs")
    require(isinstance(required_docs, list) and bool(required_docs), "required_docs must be a non-empty list", errors)
    if isinstance(required_docs, list):
        for relative in required_docs:
            path = ROOT / str(relative)
            require(path.is_file(), f"missing required production documentation: {relative}", errors)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    quickstart = (ROOT / "docs" / "QUICKSTART.md").read_text(encoding="utf-8")
    production_doc = (ROOT / "docs" / "PRODUCTION_RELEASE.md").read_text(encoding="utf-8")
    working_doc = (ROOT / "docs" / "HUMAN_AGENT_WORKING_CONTRACT.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "scripts" / "bootstrap.py").read_text(encoding="utf-8")

    status_match = re.search(r"## Status\s+\*\*v([^*\s]+)", readme)
    require(status_match is not None, "README Status must begin with a machine-checkable **v<version> marker", errors)
    if status_match:
        require(status_match.group(1) == version, f"README Status version {status_match.group(1)} != VERSION {version}", errors)

    require("/stable/scripts/bootstrap.py" in readme, "README production bootstrap must use stable channel", errors)
    require("/stable/scripts/bootstrap.py" in quickstart, "Quick Start production bootstrap must use stable channel", errors)
    require('DEFAULT_REF = "stable"' in bootstrap, "bootstrap DEFAULT_REF must remain stable", errors)
    require("MIN_SUPPORTED_PYTHON = (3, 11)" in bootstrap, "bootstrap minimum Python support drifted", errors)
    require("MAX_SUPPORTED_PYTHON = (3, 14)" in bootstrap, "bootstrap maximum Python support drifted", errors)
    require("a real downstream consumer" in production_doc.lower(), "production release doc must preserve downstream validation gate", errors)
    require("fast-forward" in production_doc.lower(), "production release doc must preserve stable fast-forward policy", errors)
    require("force-move" in production_doc.lower(), "production release doc must preserve no-routine-force-rollback policy", errors)
    require("autonomous delivery" in working_doc.lower(), "Working Contract doc must preserve autonomous collaboration mode", errors)
    require("collaborative delivery" in working_doc.lower(), "Working Contract doc must preserve collaborative collaboration mode", errors)
    require("1–5 members" in working_doc, "Working Contract doc must preserve Task Pod 1–5 bound", errors)
    require("agency-agents-zh" in working_doc, "Working Contract doc must preserve optional specialist-role provider boundary", errors)
    require("agency-orchestrator" in working_doc, "Working Contract doc must preserve delegated orchestration provider boundary", errors)

    required_runtime_surfaces = [
        ".aaop/tools/health.py",
        ".aaop/tools/provenance.py",
        ".aaop/tools/journey.py",
        ".aaop/tools/journey_state.py",
        ".aaop/tools/working_contract.py",
        ".aaop/schemas/working-contract.schema.json",
        ".aaop/schemas/team-plan.schema.json",
        ".aaop/schemas/task-handoff.schema.json",
        ".aaop/skills/working-contract/SKILL.md",
        "scripts/validate_install_transaction.py",
        "scripts/validate_journey_recovery.py",
        "scripts/validate_platform_support.py",
        "scripts/validate_provenance.py",
        "scripts/validate_working_contract.py",
        "scripts/validate_downstream_consumer.py",
        "scripts/validate_ci_supply_chain.py",
    ]
    for relative in required_runtime_surfaces:
        require((ROOT / relative).is_file(), f"missing production safety surface: {relative}", errors)

    if errors:
        print("FAIL AAOP production release contract")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS AAOP production release contract: "
        f"v{version}, canonical Journey, Human-Agent Working Contract, {len(actual_workflows)} read-only workflow gates"
    )
    print("LIVE GATE STILL REQUIRED: all workflow conclusions green + exact-candidate downstream consumer validation before stable promotion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
