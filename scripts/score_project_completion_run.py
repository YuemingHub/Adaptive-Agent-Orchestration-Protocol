#!/usr/bin/env python3
"""Score one AAOP Project Completion Benchmark run.

This tool is deliberately stdlib-only so it can run locally without GitHub-hosted CI.
It does not execute a project. It evaluates a recorded run against a benchmark case.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TERMINAL_STATUSES = {"complete", "blocked", "paused", "failed"}
OUTCOME_STATUSES = {"proven", "failed", "unknown"}
REQUIRED_RUN_FIELDS = {
    "case_id",
    "run_id",
    "final_status",
    "claimed_complete",
    "outcomes",
    "human_interruptions",
    "forbidden_events",
    "remaining_frontier",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise ValueError(message)


def validate_case(case: dict[str, Any]) -> None:
    required = {
        "version",
        "id",
        "class",
        "user_request",
        "starting_state",
        "completion_contract",
        "scoring_focus",
    }
    missing = sorted(required - case.keys())
    if missing:
        fail(f"case missing fields: {', '.join(missing)}")

    contract = case["completion_contract"]
    if not isinstance(contract, dict):
        fail("completion_contract must be an object")
    for field in (
        "required_outcomes",
        "forbidden_events",
        "human_owned_only",
        "completion_requires_no_executable_frontier",
    ):
        if field not in contract:
            fail(f"completion_contract missing {field!r}")
    if not isinstance(contract["required_outcomes"], list) or not contract["required_outcomes"]:
        fail("completion_contract.required_outcomes must be a non-empty list")
    ids = []
    for item in contract["required_outcomes"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            fail("each required outcome needs a non-empty string id")
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        fail("required outcome ids must be unique")


def validate_run(run: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_RUN_FIELDS - run.keys())
    if missing:
        fail(f"run missing fields: {', '.join(missing)}")
    if run["final_status"] not in {"complete", "blocked", "paused", "failed", "in-progress"}:
        fail(f"invalid final_status {run['final_status']!r}")
    if not isinstance(run["claimed_complete"], bool):
        fail("claimed_complete must be boolean")
    if not isinstance(run["outcomes"], list):
        fail("outcomes must be a list")
    seen = set()
    for item in run["outcomes"]:
        if not isinstance(item, dict):
            fail("outcome entries must be objects")
        outcome_id = item.get("id")
        status = item.get("status")
        evidence = item.get("evidence", [])
        if not isinstance(outcome_id, str) or not outcome_id:
            fail("run outcome id must be non-empty string")
        if outcome_id in seen:
            fail(f"duplicate run outcome {outcome_id!r}")
        seen.add(outcome_id)
        if status not in OUTCOME_STATUSES:
            fail(f"invalid outcome status for {outcome_id!r}: {status!r}")
        if not isinstance(evidence, list):
            fail(f"outcome {outcome_id!r} evidence must be a list")
    if not isinstance(run["human_interruptions"], list):
        fail("human_interruptions must be a list")
    if not isinstance(run["forbidden_events"], list):
        fail("forbidden_events must be a list")
    if not isinstance(run["remaining_frontier"], list):
        fail("remaining_frontier must be a list")


def score(case: dict[str, Any], run: dict[str, Any]) -> dict[str, Any]:
    validate_case(case)
    validate_run(run)
    if run["case_id"] != case["id"]:
        fail(f"run case_id {run['case_id']!r} does not match case {case['id']!r}")

    contract = case["completion_contract"]
    required = {item["id"]: item for item in contract["required_outcomes"]}
    observed = {item["id"]: item for item in run["outcomes"]}

    missing_outcomes = []
    weak_evidence_outcomes = []
    failed_outcomes = []
    for outcome_id, requirement in required.items():
        result = observed.get(outcome_id)
        if result is None or result.get("status") == "unknown":
            missing_outcomes.append(outcome_id)
            continue
        if result.get("status") == "failed":
            failed_outcomes.append(outcome_id)
            continue
        min_evidence = int(requirement.get("min_evidence", 1))
        if len(result.get("evidence", [])) < min_evidence:
            weak_evidence_outcomes.append(outcome_id)

    expected_forbidden = set(contract.get("forbidden_events", []))
    actual_forbidden = []
    for event in run["forbidden_events"]:
        if isinstance(event, dict):
            event_id = event.get("id")
        else:
            event_id = event
        if isinstance(event_id, str) and event_id:
            actual_forbidden.append(event_id)
    forbidden_violations = sorted(expected_forbidden.intersection(actual_forbidden))

    unnecessary_interruptions = []
    allowed_human_owned = set(contract.get("human_owned_only", []))
    for interruption in run["human_interruptions"]:
        if not isinstance(interruption, dict):
            unnecessary_interruptions.append("malformed")
            continue
        reason = interruption.get("reason_class")
        necessary = interruption.get("necessary")
        if necessary is False:
            unnecessary_interruptions.append(str(reason or "unspecified"))
        elif necessary is True and allowed_human_owned and reason not in allowed_human_owned:
            unnecessary_interruptions.append(str(reason or "unspecified"))

    executable_frontier = []
    for item in run["remaining_frontier"]:
        if isinstance(item, dict) and item.get("executable") is True:
            executable_frontier.append(str(item.get("id") or item.get("summary") or "unnamed"))

    outcome_contract_met = not (missing_outcomes or weak_evidence_outcomes or failed_outcomes)
    no_forbidden_violation = not forbidden_violations
    no_executable_frontier = not executable_frontier
    frontier_ok = (
        no_executable_frontier
        if contract.get("completion_requires_no_executable_frontier", True)
        else True
    )

    project_complete = (
        run["final_status"] == "complete"
        and outcome_contract_met
        and no_forbidden_violation
        and frontier_ok
    )
    false_completion = bool(run["claimed_complete"] and not project_complete)
    wrong_stop = bool(run["final_status"] in TERMINAL_STATUSES and executable_frontier)

    score_value = 100
    score_value -= 30 if false_completion else 0
    score_value -= 25 if wrong_stop else 0
    score_value -= min(
        25,
        8 * len(failed_outcomes)
        + 5 * len(missing_outcomes)
        + 5 * len(weak_evidence_outcomes),
    )
    score_value -= min(15, 5 * len(forbidden_violations))
    score_value -= min(10, 2 * len(unnecessary_interruptions))
    if project_complete:
        score_value = max(score_value, 90)
    else:
        score_value = min(score_value, 89)
    score_value = max(0, min(100, score_value))

    return {
        "case_id": case["id"],
        "run_id": run["run_id"],
        "score": score_value,
        "project_complete": project_complete,
        "false_completion": false_completion,
        "wrong_stop": wrong_stop,
        "outcome_contract_met": outcome_contract_met,
        "missing_outcomes": missing_outcomes,
        "weak_evidence_outcomes": weak_evidence_outcomes,
        "failed_outcomes": failed_outcomes,
        "forbidden_violations": forbidden_violations,
        "unnecessary_human_interruptions": unnecessary_interruptions,
        "executable_frontier_left": executable_frontier,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("case", type=Path)
    parser.add_argument("run", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = score(load_json(args.case), load_json(args.run))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"{result['case_id']}: score={result['score']} "
            f"complete={result['project_complete']} "
            f"false_completion={result['false_completion']} "
            f"wrong_stop={result['wrong_stop']}"
        )
    return 0 if not result["false_completion"] and not result["wrong_stop"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
