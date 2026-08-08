# Example: Long-Running Multi-Repository Product

## User outcome

> Continue advancing a long-running product composed of a foundation/standards repository, a core platform repository, and a user-facing product repository. Preserve the product's governing principles. Review what matters now, choose the next highest-leverage work, execute it, and keep the repositories coherent.

## Why this is harder

The immediate request is intentionally broad. Existing code volume is not a reliable proxy for priority. The orchestration layer must recover:

- the governing principles;
- the role of each repository;
- current release/roadmap state;
- recent work and open PRs;
- where duplicated or contradictory decisions exist;
- which project outcome is currently blocked.

## Capability plan

```text
multi-repo project discovery     → project-discovery Skill + repository provider
principle/intent reconciliation  → lead reasoning context
cross-repo architecture          → architecture owner if needed
priority selection               → lead based on evidence, not code aesthetics
implementation                   → only for the selected leverage point
repository operations            → existing GitHub provider
cross-repo verification          → verification-loop + independent reviewer
release/merge validation         → repository/CI provider as authorized
```

## Team decision

Do not permanently create one agent per repository.

A likely temporary structure is:

1. **Portfolio Orchestrator** — holds the cross-repo outcome, constraints, dependency graph and next-leverage decision.
2. **Focused Implementation Owner** — works only in the repository/repositories required by the selected slice.
3. **Cross-Repo Reviewer / Merge Gate** — checks consistency with the governing foundation and verifies that the change improves the product rather than merely refactors code.

Create additional repository specialists only if a concrete workstream is large and independent enough to justify the context split.

## Priority selection rule

Rank candidate work by something like:

```text
User / product leverage
× reduction of real blocking risk
× coherence with governing principles
× verifiability
────────────────────────────────
implementation cost × regression risk
```

Do not rank by:

- easiest visible code cleanup;
- number of files that can be changed;
- agent utilization;
- novelty of architecture.

## Execution pattern

```text
Read governing foundation
        ↓
Recover current state across repos
        ↓
Identify contradictions / blockers / leverage points
        ↓
Choose one bounded cross-repo outcome
        ↓
Implement only required changes
        ↓
Run repo-local checks + cross-repo contract checks
        ↓
Independent merge-gate review
        ↓
Update durable docs only where a real decision changed
```

## User interruptions

Ask only when the next move depends on a true product/value decision, new external credential/cost, production/destructive action, or an ambiguity that repository evidence cannot resolve.

Do not ask the user to manually schedule each repository or approve ordinary sequential work if they already authorized autonomous project advancement.

## Completion evidence

A slice is complete when:

- the selected product-level outcome is demonstrably improved;
- touched repositories remain coherent with the governing standards;
- tests/CI/contracts relevant to the slice pass;
- the independent merge gate finds no material principle or integration regression;
- remaining work is reprioritized from the new state rather than blindly continuing the old plan.
