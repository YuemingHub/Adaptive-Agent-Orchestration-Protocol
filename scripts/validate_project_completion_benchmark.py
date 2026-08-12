#!/usr/bin/env python3
"""Validate the zero-cost Project Completion Benchmark contract and scorer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from score_project_completion_run import score


CASE_DIR = "benchmarks/project-completion/cases"
FIXTURE_DIR = "benchmarks/project-completion/fixtures"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    cases = sorted((root / CASE_DIR).glob("*.json"))
    if len(cases) < 5:
        errors.append(f"{CASE_DIR}: expected at least 5 benchmark cases")

    case_ids = set()
    classes = set()
    for path in cases:
        try:
            payload = load(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: invalid JSON: {exc}")
            continue
        try:
            neutral = {
                "case_id": payload.get("id", ""),
                "run_id": "validator-neutral",
                "final_status": "in-progress",
                "claimed_complete": False,
                "outcomes": [],
                "human_interruptions": [],
                "forbidden_events": [],
                "remaining_frontier": [],
            }
            score(payload, neutral)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path}: invalid benchmark case: {exc}")
            continue
        case_id = payload["id"]
        if case_id in case_ids:
            errors.append(f"{path}: duplicate case id {case_id!r}")
        case_ids.add(case_id)
        classes.add(payload["class"])

    expected_classes = {
        "greenfield-human-forward",
        "brownfield-rescue",
        "frontier-continuation",
        "capability-fabric",
        "deliverable-aware-completion",
    }
    missing_classes = expected_classes - classes
    if missing_classes:
        errors.append(f"{CASE_DIR}: missing benchmark classes {sorted(missing_classes)}")

    good_case = load(root / CASE_DIR / "greenfield-human-forward.json")
    good_run = load(root / FIXTURE_DIR / "greenfield-complete-run.json")
    good = score(good_case, good_run)
    if not good["project_complete"] or good["false_completion"] or good["wrong_stop"]:
        errors.append(f"good fixture did not score as complete: {good}")

    bad_case = load(root / CASE_DIR / "brownfield-rescue.json")
    bad_run = load(root / FIXTURE_DIR / "brownfield-false-complete-run.json")
    bad = score(bad_case, bad_run)
    if not bad["false_completion"]:
        errors.append(f"false-complete fixture was not detected: {bad}")
    if not bad["wrong_stop"]:
        errors.append(f"wrong-stop fixture was not detected: {bad}")
    if not bad["executable_frontier_left"]:
        errors.append(f"wrong-stop fixture lost executable frontier evidence: {bad}")

    deliverable_case = load(root / CASE_DIR / "non-application-deliverable.json")
    invented_deploy_run = load(root / FIXTURE_DIR / "non-application-invented-deploy-run.json")
    invented = score(deliverable_case, invented_deploy_run)
    if not invented["false_completion"]:
        errors.append(
            "invented Web-deployment fixture was not detected as false completion: "
            f"{invented}"
        )
    expected_forbidden = {
        "invent-web-deployment",
        "treat-auxiliary-demo-as-product-target",
    }
    actual_forbidden = set(invented["forbidden_violations"])
    if not expected_forbidden <= actual_forbidden:
        errors.append(
            "invented Web-deployment fixture did not preserve deliverable-target violations: "
            f"expected={sorted(expected_forbidden)} actual={sorted(actual_forbidden)}"
        )
    if invented["project_complete"]:
        errors.append(f"invented Web-deployment fixture incorrectly scored complete: {invented}")

    if errors:
        print("AAOP project completion benchmark validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(
        "AAOP project completion benchmark validation passed "
        f"({len(cases)} cases; classes={','.join(sorted(classes))}; "
        "false completion detects both unfinished brownfield work and invented deliverable targets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
