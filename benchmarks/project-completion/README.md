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
4. `capability-fabric` — the execution system may or may not need an additional capability/provider; paired cases test both escalation and correct non-escalation.
5. `non-application-deliverable` — the accepted project target is a package, Skill/plugin, CLI, library consumer, infrastructure state, or another non-service deliverable and must not be silently replaced by a Web/application deployment target.
6. `human-boundary` — all independent engineering frontier is exhausted and a genuine credential/authorization/value boundary remains; safe stopping and a minimal human request are the correct behavior.

## Evaluation method

### A run record is not a fact verifier

`scripts/score_project_completion_run.py` is a **contract scorer**. It can detect contradictions such as a completion claim with missing required outcomes or executable frontier, but it cannot independently prove that an evidence sentence is true.

The eval harness that creates a real run owns evidence collection. Prefer outcome/state graders that inspect the repository, runtime, browser, installed artifact, external target, or other accepted environment directly. Agent narration such as “I verified it” is transcript evidence at most; it is not direct outcome evidence merely because it appears in the run JSON.

Do not promote a manually written high-scoring run into release/completion proof. For consequential benchmark claims, retain enough external references or harness output that a reviewer can trace the scored outcome back to the real state that produced it.

### One run is pressure evidence, not reliability

Agent behavior is non-deterministic. A single run can prove a concrete failure or near-miss, but it is weak evidence for a general reliability rate.

When comparing AAOP versions/models/providers or claiming reliable project completion behavior:

- run multiple independent trials per material case;
- report the trial count and distribution rather than only the best run;
- prefer first-attempt reliability for autonomous engineering paths where users should not need repeated lucky retries;
- use stricter all-trials/consistency views for safety, authorization, false-completion, and other behaviors that must not fail intermittently;
- keep capability/quality cases separate from regression cases as suites mature.

The benchmark does not prescribe a universal fixed `k`; choose enough trials for the claim/risk and cost boundary. A zero-cost/manual development run may remain a single pressure observation without pretending to be a reliability estimate.

### Trials must be independent enough to mean something

Start each controlled trial from a clean, declared baseline when practical. Shared leftovers such as modified files, cached outputs, old credentials, previous trial git history, reused ports/processes, or retained provider state can make one trial influence another and can create both false failures and false success.

Record material environment/provider/model/revision identity when comparing trials. If the environment changes, treat that as a changed condition rather than silently pooling unlike runs.

### Balance trigger and non-trigger behavior

For important autonomy policies, test both directions. A one-sided benchmark can optimize AAOP into a new failure mode.

Examples in this suite include:

- capability gap proven → add/select the smallest required provider path;
- capability already available → **do not** add a provider;
- one blocker with independent frontier → continue autonomously;
- all independent frontier exhausted at a genuine human boundary → stop safely and ask only for the human-owned fact;
- non-application deliverable → do not invent a Web deploy target;
- application target where deployment is part of acceptance → direct deployment/target evidence remains required.

As new invariants are promoted, add the inverse/control case when over-triggering would itself be harmful.

## Evidence lifetime and authority

Benchmark records are **historical evaluation evidence**, not current project control state.

- `cases/` defines reusable benchmark contracts and forbidden/required outcome semantics.
- `fixtures/` contains controlled scorer examples.
- `observed/` contains timestamped observations from a particular host/project state.
- `runs/` contains scored or scoreable execution records for a particular run.

An `observed/` or `runs/` record may contain a blocker, branch, capability gap, target state, or remaining frontier that was true when that run was captured and is false later. **Never resume a real project from these files as if they were CURRENT_STATE, Journey state, issue authority, or a live frontier.** Before another real run, re-read the current repository/runtime/target/provider evidence and create a new run record when the material state changed.

Do not rewrite an older observation merely because the real project later advanced. Keeping the old result immutable is useful for measuring whether AAOP learned from the failure. If a benchmark report needs a current conclusion, score the newest applicable run after current-evidence reconciliation rather than promoting the newest timestamped file into project truth automatically.

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

- required outcome results and evidence references/descriptions;
- human interruptions and whether they were genuinely necessary;
- forbidden events that actually occurred;
- the final status and completion claim;
- any remaining project frontier with an `executable` flag.

A richer harness may separately preserve a transcript/trace, environment snapshot, command logs, target-state checks, or artifact provenance. Do not inflate the compact score record by copying all of that data into it; reference the owning evidence instead.

## Interpretation

A high score is not by itself proof that AAOP is good. The underlying evidence must still be credible.

The benchmark should be used against real projects and controlled fixtures. When a real project exposes a repeatable AAOP orchestration defect, first classify it as consumer-only, existing-AAOP-coverage, or candidate-generic-gap. Only the last class is eligible for a new AAOP invariant.

A benchmark failure is pressure evidence, not automatic permission to change AAOP Core. Prefer the smallest existing owner and require a machine-regressable cross-project lesson before promotion.

## Cost boundary

Do not open a pull request merely to run this benchmark. Do not manually dispatch GitHub-hosted workflows for routine benchmark iterations. Prefer local execution or a user-owned/self-hosted runner when continuous execution is needed.
