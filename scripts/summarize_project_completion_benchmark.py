#!/usr/bin/env python3
"""Summarize AAOP Project Completion Benchmark run records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from score_project_completion_run import load_json, score


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs_dir", type=Path)
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=Path("benchmarks/project-completion/cases"),
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cases = {}
    for path in sorted(args.cases_dir.glob("*.json")):
        payload = load_json(path)
        cases[payload["id"]] = payload

    results = []
    missing_cases = []
    for path in sorted(args.runs_dir.glob("*.json")):
        run = load_json(path)
        case = cases.get(run.get("case_id"))
        if case is None:
            missing_cases.append(str(run.get("case_id")))
            continue
        results.append(score(case, run))

    total = len(results)
    complete = sum(1 for item in results if item["project_complete"])
    false_complete = sum(1 for item in results if item["false_completion"])
    wrong_stop = sum(1 for item in results if item["wrong_stop"])
    interruptions = sum(
        len(item["unnecessary_human_interruptions"]) for item in results
    )
    avg_score = (
        round(sum(item["score"] for item in results) / total, 2) if total else 0.0
    )

    summary = {
        "runs": total,
        "average_score": avg_score,
        "project_completion_rate": round(complete / total, 4) if total else 0.0,
        "false_completion_rate": round(false_complete / total, 4) if total else 0.0,
        "wrong_stop_rate": round(wrong_stop / total, 4) if total else 0.0,
        "unnecessary_human_interruptions": interruptions,
        "case_ids": sorted({item["case_id"] for item in results}),
        "missing_case_ids": sorted(set(missing_cases)),
        "results": results,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            "AAOP Project Completion Benchmark: "
            f"runs={total} avg={avg_score} "
            f"completion={summary['project_completion_rate']:.2%} "
            f"false_completion={summary['false_completion_rate']:.2%} "
            f"wrong_stop={summary['wrong_stop_rate']:.2%} "
            f"unnecessary_interruptions={interruptions}"
        )
        if missing_cases:
            print(f"missing cases: {', '.join(sorted(set(missing_cases)))}")

    return 0 if not missing_cases else 2


if __name__ == "__main__":
    raise SystemExit(main())
