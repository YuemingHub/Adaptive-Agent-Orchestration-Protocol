# AAOP Project Completion Benchmark

This benchmark tests whether AAOP can take responsibility for a whole software project, not merely complete one route, patch, report, or test suite.

It is intentionally **not wired into GitHub Actions**. The default execution model is local or self-hosted so the benchmark can be run repeatedly without GitHub-hosted runner cost.

## What it measures

The benchmark records and scores a real AAOP run against an explicit case contract. The primary failure signals are:

- **false completion** — the run claims completion without proving the required outcome contract;
- **wrong stop** — the run terminates while a safe authorized executable project frontier remains;
- **unnecessary human interruption** — the run asks the person to resolve work AAOP should own;
- **forbidden behavior** — for example forcing a non-technical person to choose a stack, rewriting a messy repository before recovering value, or treating provider installation as task success;
- **weak outcome evidence** — required outcomes are asserted without enough evidence.

The benchmark deliberately scores **project outcomes**, not code volume, agent count, prompt quality, or number of tools used.

## Initial classes

1. `greenfield-human-forward` — a person has only an idea and may or may not have deep lived/domain experience.
2. `brownfield-rescue` — a non-technical owner brings a messy AI-built project that may still contain real value.
3. `frontier-continuation` — one scope is blocked or locally green while another current authorized frontier remains executable.
4. `capability-fabric` — the main model can reason/write code but the task needs capabilities such as browser observation or independent acceptance that the current execution system may not actually have.

## Run locally

Validate the benchmark contract and built-in scorer fixtures:

```bash
python scripts/validate_project_completion_benchmark.py
```

Score a recorded run:

```bash
python scripts/score_project_completion_run.py \
  benchmarks/project-completion/cases/greenfield-human-forward.json \
  path/to/run.json --json
```

A run record is intentionally small. It contains:

- required outcome results and evidence;
- human interruptions and whether they were genuinely necessary;
- forbidden events that actually occurred;
- the final status and completion claim;
- any remaining project frontier with an `executable` flag.

## Interpretation

A high score is not by itself proof that AAOP is good. The underlying evidence must still be credible.

The benchmark should be used against real projects and controlled fixtures. When a real project exposes a repeatable AAOP orchestration defect, first classify it as consumer-only, existing-AAOP-coverage, or candidate-generic-gap. Only the last class is eligible for a new AAOP invariant.

## Cost boundary

Do not open a pull request merely to run this benchmark. Do not manually dispatch GitHub-hosted workflows for routine benchmark iterations. Prefer local execution or a user-owned/self-hosted runner when continuous execution is needed.
