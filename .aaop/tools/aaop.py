#!/usr/bin/env python3
"""Human-facing AAOP command surface.

The lower-level tools remain available for orchestration and diagnostics. This
wrapper gives a developer one stable entrypoint for the common human workflow:

    python .aaop/tools/aaop.py ready .
    python .aaop/tools/aaop.py status .
    python .aaop/tools/aaop.py doctor .
    python .aaop/tools/aaop.py prompt
    python .aaop/tools/aaop.py version
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

# The human-facing CLI is observational. Dynamic loading of health/doctor should not
# create __pycache__ files inside an installed AAOP package merely because a user ran
# `ready`, `status`, or `doctor`.
sys.dont_write_bytecode = True

STARTER_PROMPT = (
    "Understand this project and its current rules, determine the highest-value "
    "current executable step toward the user's goal, and continue autonomously. "
    "Reuse what already exists, preserve project intent, make ordinary engineering "
    "decisions yourself, verify the result, and ask only for genuinely missing "
    "authorization, credentials, or material product decisions."
)


def tool_root() -> Path:
    return Path(__file__).resolve().parent


def package_root() -> Path:
    return tool_root().parent


def default_project_root() -> Path:
    return package_root().parent


def load_tool(name: str) -> ModuleType:
    path = tool_root() / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"aaop_{name}", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"AAOP: unable to load internal tool {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def package_version() -> str:
    path = package_root() / "VERSION"
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise SystemExit(f"AAOP: cannot read authoritative package version {path}: {exc}") from exc
    if not value:
        raise SystemExit(f"AAOP: authoritative package version is empty: {path}")
    return value


def readiness(root: Path) -> dict[str, Any]:
    health_module = load_tool("health")
    doctor_module = load_tool("doctor")

    health = health_module.inspect_installation(root)
    doctor = doctor_module.inspect(root)

    health_state = str(health.get("state") or "unknown")
    source_tree = health_state == "source-tree"
    install_ready = health_state == "healthy"
    ready = install_ready or source_tree

    hosts = doctor.get("host_commands", {})
    if not isinstance(hosts, dict):
        hosts = {}

    instructions = doctor.get("instruction_files", [])
    if not isinstance(instructions, list):
        instructions = []

    project_signals = doctor.get("project_signals", {})
    if not isinstance(project_signals, dict):
        project_signals = {}

    signal_counts: dict[str, int] = {}
    for key in ("manifests", "test_signals", "ci_signals", "deployment_signals"):
        value = project_signals.get(key, [])
        signal_counts[key] = len(value) if isinstance(value, list) else 0

    return {
        "ready": ready,
        "version": health.get("package_version") or package_version(),
        "project_root": str(root),
        "health_state": health_state,
        "health_next_action": health.get("next_action"),
        "source_tree": source_tree,
        "instruction_files": instructions,
        "host_commands": hosts,
        "observed_surface_level": doctor.get("observed_surface_level"),
        "project_signal_counts": signal_counts,
        "starter_prompt": STARTER_PROMPT,
    }


def render_ready(report: dict[str, Any]) -> None:
    state = "READY" if report["ready"] else "REVIEW REQUIRED"
    print(f"AAOP {state}")
    print(f"  version: {report['version']}")
    print(f"  project: {report['project_root']}")
    print(f"  health: {report['health_state']}")

    instructions = report.get("instruction_files", [])
    print(f"  project instructions: {', '.join(instructions) if instructions else 'none detected'}")

    hosts = report.get("host_commands", {})
    if isinstance(hosts, dict) and hosts:
        print(f"  host CLI on PATH: {', '.join(sorted(hosts))}")
    else:
        print("  host CLI on PATH: none detected (editor/desktop hosts may still work)")

    counts = report.get("project_signal_counts", {})
    if isinstance(counts, dict):
        print(
            "  project evidence: "
            f"manifests={counts.get('manifests', 0)} "
            f"tests={counts.get('test_signals', 0)} "
            f"ci={counts.get('ci_signals', 0)} "
            f"deploy={counts.get('deployment_signals', 0)}"
        )

    if report["ready"]:
        print()
        print("Open this project in Codex, Claude Code, Cursor, or another host that reads project instructions.")
        print("Then say:")
        print(f'  "{report["starter_prompt"]}"')
    else:
        print()
        print(f"Next: {report.get('health_next_action') or 'Review the AAOP installation health report.'}")


def command_ready(root: Path, as_json: bool) -> int:
    report = readiness(root)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        render_ready(report)
    return 0 if report["ready"] else 2


def command_status(root: Path, as_json: bool) -> int:
    health_module = load_tool("health")
    report = health_module.inspect_installation(root)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        health_module.render(report)
    return 0 if report.get("state") in {"healthy", "source-tree"} else 2


def command_doctor(root: Path, route: str | None, as_json: bool) -> int:
    doctor_module = load_tool("doctor")
    report = doctor_module.inspect(root, route)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        doctor_module.render(report)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AAOP user entrypoint: readiness, status, environment, starter prompt, and version"
    )
    subparsers = parser.add_subparsers(dest="command")

    ready_parser = subparsers.add_parser("ready", help="Check whether AAOP is ready to use in this project")
    ready_parser.add_argument("root", nargs="?", type=Path, default=default_project_root())
    ready_parser.add_argument("--json", action="store_true")

    status_parser = subparsers.add_parser("status", help="Show AAOP installation health")
    status_parser.add_argument("root", nargs="?", type=Path, default=default_project_root())
    status_parser.add_argument("--json", action="store_true")

    doctor_parser = subparsers.add_parser("doctor", help="Show project/environment capability evidence")
    doctor_parser.add_argument("root", nargs="?", type=Path, default=default_project_root())
    doctor_parser.add_argument("--route", help="Optionally include one route's provider candidates")
    doctor_parser.add_argument("--json", action="store_true")

    subparsers.add_parser("prompt", help="Print a starter prompt for autonomous project continuation")
    subparsers.add_parser("version", help="Print the installed AAOP package version")

    args = parser.parse_args()
    command = args.command or "ready"

    if command == "ready":
        root = args.root.expanduser().resolve() if hasattr(args, "root") else default_project_root()
        return command_ready(root, bool(getattr(args, "json", False)))
    if command == "status":
        root = args.root.expanduser().resolve()
        return command_status(root, args.json)
    if command == "doctor":
        root = args.root.expanduser().resolve()
        return command_doctor(root, args.route, args.json)
    if command == "prompt":
        print(STARTER_PROMPT)
        return 0
    if command == "version":
        print(package_version())
        return 0

    parser.error(f"unknown command {command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
