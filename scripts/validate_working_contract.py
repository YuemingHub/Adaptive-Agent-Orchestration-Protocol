#!/usr/bin/env python3
"""Regression validation for the Human-Agent Working Contract and Task Pod bounds."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / ".aaop" / "tools" / "working_contract.py"
WORKING_SCHEMA = ROOT / ".aaop" / "schemas" / "working-contract.schema.json"
TEAM_SCHEMA = ROOT / ".aaop" / "schemas" / "team-plan.schema.json"
HANDOFF_SCHEMA = ROOT / ".aaop" / "schemas" / "task-handoff.schema.json"
WORKING_SKILL = ROOT / ".aaop" / "skills" / "working-contract" / "SKILL.md"
TEAM_SKILL = ROOT / ".aaop" / "skills" / "team-construction" / "SKILL.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(root: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["AAOP_WORKING_CONTRACT_ROOT"] = str(root)
    completed = subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != expected:
        raise AssertionError(
            f"working_contract.py {' '.join(args)} returned {completed.returncode}, expected {expected}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def payload(completed: subprocess.CompletedProcess[str]) -> dict[str, object]:
    data = json.loads(completed.stdout)
    require(isinstance(data, dict), "tool JSON output must be an object")
    return data


def main() -> int:
    require(TOOL.is_file(), "missing working_contract.py")
    require(WORKING_SCHEMA.is_file(), "missing working-contract schema")
    require(TEAM_SCHEMA.is_file(), "missing team-plan schema")
    require(HANDOFF_SCHEMA.is_file(), "missing task-handoff schema")

    with tempfile.TemporaryDirectory(prefix="aaop-working-contract-") as tmp:
        runtime = Path(tmp)

        missing = payload(run(runtime, "status", "--json", expected=2))
        require(missing.get("state") == "uninitialized", "missing contract must report uninitialized")

        created = payload(run(runtime, "init", "--goal", "Ship a verified product slice", "--json"))
        require(created.get("revision") == 1, "initial revision must be 1")
        require(created["collaboration"]["mode"] == "unset", "initial mode must not be silently chosen")
        require(created["task_pod_policy"]["max_members"] == 5, "Task Pod maximum must be five")
        run(runtime, "gate", "--json", expected=3)

        selected = payload(
            run(runtime, "set-mode", "--expected-revision", "1", "--mode", "autonomous", "--json")
        )
        require(selected.get("revision") == 2, "set-mode must advance revision")
        require(selected["collaboration"]["confirmed"] is True, "selected mode must be confirmed")

        updated = payload(
            run(
                runtime,
                "update-alignment",
                "--expected-revision",
                "2",
                "--actor",
                "project owner",
                "--situation",
                "existing repository",
                "--outcome",
                "one verified release candidate",
                "--must",
                "preserve project-owned authority",
                "--non-goal",
                "do not invent a new framework",
                "--success-evidence",
                "project acceptance checks pass",
                "--open-question",
                "Should the first release be private or public?",
                "--json",
            )
        )
        require(updated.get("revision") == 3, "alignment update must advance revision")
        run(runtime, "confirm-alignment", "--expected-revision", "3", "--json", expected=1)
        blocked = payload(run(runtime, "status", "--json"))
        require(blocked.get("revision") == 3, "failed confirmation must not mutate state")

        resolved = payload(
            run(
                runtime,
                "resolve-question",
                "--expected-revision",
                "3",
                "--question",
                "Should the first release be private or public?",
                "--evidence",
                "human chose private",
                "--json",
            )
        )
        require(resolved.get("revision") == 4, "question resolution must advance revision")
        require(not resolved["alignment"]["human_open_questions"], "resolved question must be removed")

        aligned = payload(run(runtime, "confirm-alignment", "--expected-revision", "4", "--json"))
        require(aligned.get("revision") == 5, "alignment confirmation must advance revision")
        require(aligned["alignment"]["state"] == "aligned", "alignment must be marked aligned")
        gate = payload(run(runtime, "gate", "--json"))
        require(gate.get("execution_allowed") is True, "aligned contract must allow execution")

        run(
            runtime,
            "set-mode",
            "--expected-revision",
            "2",
            "--mode",
            "collaborative",
            "--json",
            expected=1,
        )
        current = payload(run(runtime, "status", "--json"))
        require(current.get("revision") == 5, "stale mutation must not change revision")
        require(current["collaboration"]["mode"] == "autonomous", "stale mutation must not change mode")

        reopened = payload(
            run(
                runtime,
                "reset-alignment",
                "--expected-revision",
                "5",
                "--reason",
                "new product evidence changed the intended outcome",
                "--json",
            )
        )
        require(reopened.get("revision") == 6, "alignment reset must advance revision")
        require(reopened["alignment"]["state"] == "collecting", "reset must reopen alignment")
        require(reopened["collaboration"]["mode"] == "autonomous", "reset must preserve collaboration mode")
        run(runtime, "gate", "--json", expected=3)

    working_schema = json.loads(WORKING_SCHEMA.read_text(encoding="utf-8"))
    require(working_schema["properties"]["task_pod_policy"]["properties"]["max_members"]["const"] == 5, "working contract schema must hard-cap pods at five")

    team_schema = json.loads(TEAM_SCHEMA.read_text(encoding="utf-8"))
    require(team_schema["properties"]["agents"]["maxItems"] == 5, "team schema must hard-cap members at five")
    for field in ("pod_id", "outcome", "accountable_owner", "acceptance_criteria", "agents"):
        require(field in team_schema["required"], f"team schema missing required field {field}")

    handoff_schema = json.loads(HANDOFF_SCHEMA.read_text(encoding="utf-8"))
    for field in (
        "long_horizon_goal",
        "current_outcome",
        "baseline",
        "decisions",
        "delivered",
        "evidence",
        "risks",
        "blockers",
        "human_open_questions",
        "next_outcome",
        "references",
    ):
        require(field in handoff_schema["required"], f"handoff schema missing required field {field}")

    working_skill = WORKING_SKILL.read_text(encoding="utf-8")
    team_skill = TEAM_SKILL.read_text(encoding="utf-8")
    require("Evidence-resolvable" in working_skill, "working contract must preserve evidence-first question policy")
    require("Human-owned" in working_skill, "working contract must preserve human decision ownership")
    require("1–5 members" in working_skill, "working contract must describe bounded Task Pods")
    require("exactly one accountable owner" in team_skill, "team construction must require one accountable owner")
    require("agency-agents-zh" in team_skill, "team construction must include optional agency-agents-zh role source")
    require("second top-level Journey/control plane" in team_skill, "external orchestrator must not become a competing control plane")

    print("PASS Human-Agent Working Contract: alignment gate, CAS, decision boundary, Task Pod cap, and handoff contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
