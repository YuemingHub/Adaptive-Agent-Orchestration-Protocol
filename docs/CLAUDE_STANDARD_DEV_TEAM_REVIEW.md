# Review: `xuanbingbingo/claude-standard-dev-team`

Reviewed: 2026-08-11

Upstream repository: `https://github.com/xuanbingbingo/claude-standard-dev-team`

Reviewed upstream commit: `d1aa5006d6b6ecb7430950a966b1d31cd6574a39`

License: MIT

## Decision

**Absorb selected mechanisms into AAOP Core; do not register or install the repository as an AAOP Provider.**

The upstream project is an opinionated Claude Code team configuration: a main-session orchestration Skill plus a fixed catalog of specialist agents and an 11-phase application-development script. AAOP already owns the broader control-plane responsibilities that this repository packages together:

- human/agent decision ownership through the Working Contract;
- current-problem routing;
- end-to-end Journey/release-cycle continuity;
- minimum 1–5 member Task Pods;
- direct specialist-role Provider selection;
- optional delegated Pod runtime selection;
- optional LoopX execution-continuity control;
- evidence and production-target verification.

Installing the whole repository beside AAOP would therefore create a second workflow/topology and reintroduce the fixed-team duplication AAOP just retired.

The repository nevertheless contains several concrete, experience-derived mechanisms that improve AAOP's ability to finish development work. Those mechanisms are absorbed below without importing the fixed topology.

## Mechanisms absorbed

### 1. Shared-contract fan-out and stale-evidence invalidation

Upstream's strongest lesson is not merely “write an API contract first.” It records a real failure mode: an interface field/type/envelope changed, while dependent frontend types/usages remained on the old shape.

AAOP generalizes this into a route-level rule:

1. a material shared contract/interface/schema/data/deployment contract changes;
2. inspect the current repository to identify real consumers;
3. classify consumers as unaffected, must-update, or must-reverify;
4. invalidate tests/reviews/acceptance evidence that was produced against the stale contract for affected consumers;
5. reopen only the affected slices;
6. prove the new baseline before accepting the outcome.

This is broader than frontend `types.ts`: it applies to APIs, schemas, event contracts, public types, configuration/deployment contracts, security invariants, and any other shared baseline.

Implementation: `.aaop/routes/feature-change.json` and `.aaop/skills/team-construction/SKILL.md`.

### 2. Builder–verifier pair for consequential slices

Upstream validates implementation tasks in a separate context instead of accepting the implementer's completion claim. That separation is useful when a slice is contract-sensitive, high-blast-radius, security/privacy relevant, hard to observe, or has a history of false completion.

AAOP generalizes the pattern without requiring a QA agent for every edit:

- builder receives objective, governing acceptance/contract, allowed write surface, expected deliverables;
- verifier starts from current artifacts/diff/runtime evidence rather than builder narrative;
- verifier runs/reads the strongest practical project-native evidence;
- unknown/unverified is not PASS;
- verifier may not invent extra product requirements merely to be adversarial;
- FAIL returns bounded evidence to the accountable owner for repair/replan/reroute/block;
- repeated unchanged failure is diagnosed before retry.

This preserves AAOP's default of one capable agent while making independent proof an explicit Pod pattern where it creates measurable value.

Implementation: `.aaop/skills/team-construction/SKILL.md`.

### 3. Partial-delivery salvage after interrupted workers

Upstream distinguishes two fundamentally different situations:

- a worker completed but QA found the output wrong;
- a worker never completed because the host/network/context/runtime interrupted it after some files were already written.

Its useful mechanism is to declare expected deliverables before long delegation, inspect what actually exists after interruption, validate important surviving outputs, and resume only the missing/invalid delta instead of replaying the whole task and overwriting durable work.

AAOP generalizes this into interruption recovery:

- record expected deliverables/mutation refs, acceptance commands, allowed surface, current baseline, and successor condition where useful;
- on interruption, do not blindly replay;
- inspect current reality and validate surviving outputs;
- preserve verified durable work;
- recompute only the missing/invalid delta;
- resume with explicit “do not overwrite verified work without new evidence” boundaries;
- if this frontier cannot survive sessions reliably, classify `execution-continuity` and evaluate LoopX instead of creating another AAOP task database.

Implementation: `.aaop/skills/team-construction/SKILL.md`.

### 4. Verification-baseline-aware parallelism

Upstream intentionally serializes some apparently parallel phases because one stream can mutate the exact code/contract another reviewer is evaluating. The underlying principle is stronger than “serial is safer.”

AAOP generalizes it as **verification-baseline coupling**:

- parallelize only when write sets, mutable dependencies, and evidence baselines are sufficiently independent;
- serialize when one stream can invalidate another stream's contract, review snapshot, security evidence, or external state;
- use isolation plus an explicit merge/reconciliation boundary when the runtime can safely support concurrency.

The optimization target is valid evidence throughput, not maximum parallel Agent count.

Implementation: `.aaop/skills/team-construction/SKILL.md`.

### 5. Host topology must be discovered, not assumed

Upstream moved its orchestrator from a subagent to the main-session Skill after observing a Claude Code topology constraint: a delegated subagent could not itself spawn the rest of the team.

AAOP does not treat that Claude-specific behavior as a universal law. It absorbs the more general rule:

- do not assume nested delegation exists;
- keep orchestration in a context that actually has the required host primitive;
- if nested/peer delegation is unavailable, preserve the responsibility plan and execute sequential isolated roles rather than asking the user to switch tools.

Implementation: `.aaop/skills/team-construction/SKILL.md` host-degradation rules.

## Patterns intentionally not absorbed

### Fixed 12-agent team

Rejected as an AAOP default. AAOP keeps the 1–5 Task Pod ceiling and one-agent default. A fixed product-manager / architect / database / backend / frontend / security / reviewer / writer roster creates unnecessary contexts for many tasks and confuses titles with proven capability gaps.

### Fixed 11-phase workflow

Rejected as a top-level AAOP workflow. Existing repositories and small changes must route from current evidence, not be forced through greenfield PRD → architecture → DB → backend → frontend → security → deployment chronology.

### Fixed two human checkpoints

Rejected as universal policy. AAOP's Working Contract determines human-owned decisions by product/domain/authorization ownership and risk. High fan-out/reversal-cost decisions may justify a human checkpoint, but phase number does not.

### “Default NEEDS WORK” and “find 3–5 issues”

Rejected. Skeptical evidence review is useful; a required quota of defects or a default negative verdict biases evaluation and can manufacture problems. AAOP uses burden-of-proof semantics instead: unverified is not pass, but the verdict follows evidence and authoritative acceptance criteria.

### Universal fixed retry counts

Rejected. The upstream 1/2/3 retry budgets are useful examples of circuit-breaking, but AAOP classifies failure first and uses risk/cost/provider-aware retry/no-progress policy. LoopX may govern bounded run/wait/quiet semantics when a real execution-continuity gap exists.

### Ban on browser automation

Rejected. Upstream intentionally removes browser/Playwright dependencies for self-contained Claude workflows. AAOP instead selects the strongest practical evidence surface. For browser-visible behavior, existing Playwright Test or another justified browser surface may be exactly the evidence required.

### Hard-coded subpath deployment conventions

Rejected as universal AAOP policy. The upstream deployment rules reflect a specific multi-app/shared-gateway operating model and valuable local incidents, but AAOP must discover each project's actual deployment topology before applying path/base-url invariants.

### “Orchestrator never writes code”

Rejected as a universal role rule. AAOP's accountable owner may implement directly when one context is sufficient. Coordination-only ownership is selected only when it produces measurable value.

## Relationship to existing AAOP providers

This review does not create a `claude-standard-dev-team` Provider.

- **Role content gap** → existing project/host roles first, then optional `agency-agents-zh` when justified.
- **Delegated multi-role DAG/resume gap** → optional `agency-orchestrator` when justified.
- **Long-running execution-continuity gap** → optional LoopX after evidence proves that specific gap.
- **Browser acceptance gap** → existing project browser tests or the smallest justified Playwright surface.

The reviewed repository is therefore a **pattern source**, not a runtime dependency.

## Attribution and license boundary

The reviewed source is MIT licensed. AAOP paraphrases and generalizes mechanisms rather than vendoring the upstream role prompts or 11-phase Skill. The upstream repository and reviewed commit are retained here as provenance for future maintainers.

## Result

AAOP gains four practical execution improvements without adding another standing team or control plane:

```text
shared contract changes
  -> find consumers
  -> invalidate stale evidence
  -> update/reverify affected slices only

consequential implementation slice
  -> builder
  -> independent evidence verifier
  -> accept / bounded repair / replan

worker interruption
  -> inspect durable outputs
  -> validate survivors
  -> resume missing delta only

parallel candidates
  -> compare write + verification baselines
  -> parallelize only when evidence cannot become stale
```

This is the intended AAOP pattern: **absorb the invariant, retire the accidental topology**.
