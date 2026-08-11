# AAOP Production Release Contract

AAOP does not become production-ready because a version number changes or because one pull request is green. Production eligibility is the conjunction of package, lifecycle, human-agent interaction, continuity, platform, supply-chain, and downstream-consumer evidence.

## Production release line

AAOP v1.0 establishes the first production release line.

The user-facing production channel is:

```text
stable
```

`main` remains the development/edge branch. A commit landing on `main` never promotes itself to production automatically.

## Release candidate gate

A candidate is eligible for production promotion only when all of the following are true on the final candidate tree:

1. `.aaop/VERSION` matches `.aaop/PRODUCTION_RELEASE.json`;
2. README Status identifies the same production release line;
3. `idea-to-production` Journey has canonical, non-experimental status;
4. the Human-Agent Working Contract surfaces declared in `.aaop/PRODUCTION_RELEASE.json` exist and its regression gate passes;
5. Working Contract behavior does not silently choose autonomous/collaborative mode for a new project and does not allow sustained execution while human-owned open questions remain;
6. Task Pods remain bounded to 1–5 members, have one accountable owner, and use explicit handoff when a materially different Pod takes over;
7. external role/orchestration providers remain delegated capability surfaces rather than competing Working Contract/Journey control planes;
8. every workflow listed in `.aaop/PRODUCTION_RELEASE.json` exists;
9. all required workflows pass on the final candidate head;
10. external GitHub Actions are pinned to reviewed immutable commit SHAs;
11. long-lived validation workflows retain read-only repository contents permission;
12. transactional lifecycle fault injection passes;
13. Journey CAS/lock/schema/recovery regressions pass;
14. platform support matrix passes across the declared Python/OS surfaces;
15. install provenance regressions pass without expanding ownership authority;
16. a real downstream consumer validates the **exact candidate tree** while preserving that consumer's own project authority, Working Contract/runtime continuity, and executable project validation;
17. if the PR base/head changes after any material review evidence, affected validation is rerun before merge.

The machine-readable static portion of this contract is validated by:

```text
validate-production-release
```

The Human-Agent interaction behavior is separately exercised by:

```text
validate-working-contract
```

The final merge/promotion controller must additionally verify current GitHub workflow conclusions and downstream-consumer evidence; a repository file cannot truthfully certify a future GitHub run by itself.

## Human-Agent production behavior

AAOP v1 is not production-ready merely because its internal engineering routes work. A newly installed consumer must support this interaction model:

```text
ordinary-language goal
  → inspect available project/idea evidence
  → establish/reuse autonomous or collaborative working mode
  → resolve evidence-resolvable facts without asking the human
  → let Agent/CTO decide expert-decidable engineering choices
  → ask only genuinely human-owned product/domain/authorization questions
  → confirm observable outcome + success evidence
  → enter sustained execution
  → use one Agent by default; create a bounded Task Pod only when justified
  → verify outcome
  → hand off bounded evidence when responsibility materially changes
```

The persistent Working Contract lives under `.aaop/runtime/working-contract.json` and is intentionally separate from the Journey checkpoint:

- Working Contract: collaboration mode, aligned intent, decision ownership and interaction gate;
- Journey: long-horizon Route/gate/evidence/release-cycle continuity.

Both are continuity evidence. Neither may override fresher authoritative project/runtime/target evidence.

A saved collaboration preference survives ordinary AAOP upgrade because `.aaop/runtime/` is project-owned continuity state. An aligned contract must be explicitly reopened when material new evidence changes intent; it must not be silently rewritten by a later Agent session.

See `docs/HUMAN_AGENT_WORKING_CONTRACT.md`.

## Task Pod production boundary

AAOP is single-Agent by default. Multi-Agent execution is not itself a success criterion.

When a responsibility split is justified:

- a Task Pod has 1–5 members maximum;
- exactly one accountable owner integrates evidence and owns acceptance;
- specialists receive bounded responsibilities and least-privilege tools;
- consequential work should use an independent reviewer when practical;
- specialist/parallel contexts do not independently mutate Working Contract or Journey state;
- a materially different next Pod receives a handoff conforming to `.aaop/schemas/task-handoff.schema.json`;
- the receiving Pod re-reads current evidence before continuing.

If a role library such as `agency-agents-zh` is used, select only the minimum justified role subset. If `agency-orchestrator` or another runtime is used, it may execute one bounded delegated Pod but AAOP retains goal, decision ownership, authorization, acceptance, Journey and handoff authority.

## Downstream consumer validation

The consumer check is not “can Python import AAOP?” It must exercise a real project boundary.

At minimum:

- use a real AAOP consumer repository with its own project instructions/authority surfaces;
- validate the exact release-candidate commit/ref, not whatever `stable` happens to point to before promotion;
- install or upgrade without overwriting consumer-owned project rules;
- run `aaop.py ready` and health/provenance checks;
- preserve existing `.aaop/runtime` continuity when upgrading an existing consumer, including Journey/Working Contract state when present;
- verify that project-specific authority/current-state files still outrank AAOP history/checkpoints/handoffs;
- verify the Working Contract surfaces are installed and observational readiness does not silently fabricate a collaboration preference;
- run the consumer's own relevant validation when its CI/runtime is available;
- if consumer executable validation is externally blocked, do not count static inspection as the downstream production gate.

A failure found downstream returns to the AAOP release candidate as a real compatibility defect. Do not waive it merely because AAOP's own workflows are green.

## Stable promotion

Promotion is deliberately separate from merge:

```text
candidate PR head
  ↓ all AAOP gates green + downstream exact-candidate validation
merge to main
  ↓ verify merged tree preserves candidate tree / no base drift
stable fast-forward → merged validated commit
```

Rules:

- `stable` is moved only after the candidate is merged;
- promotion is a non-force fast-forward;
- never make ordinary `main` pushes auto-advance `stable`;
- re-read the merged commit before promotion;
- if the merged tree differs materially from the consumer-validated candidate, revalidate before moving `stable`.

## Rollback / bad production release

`stable` is a monotonic production channel. Do not silently force-move it backward to an old commit as routine rollback.

If a production defect is discovered:

1. classify the defect and affected release;
2. prepare a minimal repair or explicit revert **as a new forward commit**;
3. run the same relevant AAOP gates plus downstream compatibility evidence;
4. merge the repair;
5. fast-forward `stable` to the repaired/reverted tree.

Consumers pinned to an exact commit remain pinned until they deliberately change that pin. Consumers following `stable` receive the next promoted repair when they next upgrade.

Emergency repository-owner intervention may require a different control-plane action, but it must be recorded explicitly as an emergency exception rather than becoming the normal release mechanism.

## Required production evidence classes

### Package lifecycle

- bounded bootstrap download/extraction;
- explicit stable/edge/exact-ref semantics;
- transactional install/upgrade/uninstall;
- interrupted lifecycle detection and explicit recovery;
- manifest path/schema fail-closed behavior.

### Human-Agent interaction

- explicit collaboration mode instead of silent autonomous-mode selection;
- evidence-first alignment rather than a technical questionnaire;
- decision ownership separating human-owned, agent-owned and joint choices;
- observable success evidence before sustained execution;
- unresolved human-owned questions block alignment;
- Working Contract revision/CAS + OS locking;
- one-Agent default and Task Pod 1–5 bound;
- one accountable Pod owner and bounded handoff;
- external role/runtime providers remain subordinate to AAOP.

### Journey continuity

- one current Route under a long-horizon Journey;
- cross-session continuation;
- revision CAS + OS locking;
- completed release-cycle isolation;
- future checkpoint schema fail-closed behavior;
- explicit last-good recovery with damaged-state preservation.

### Platform

See `docs/PLATFORM_SUPPORT.md`.

### Provenance

See `docs/INSTALL_PROVENANCE.md`.

### CI supply chain

See `docs/CI_SUPPLY_CHAIN.md`.

## Why v1.0 does not freeze all future design

Production-ready means the current contracts are safe and operationally supportable for their declared surfaces. It does not mean AAOP will never evolve.

Future changes may add providers, schemas, interaction modes, or release capabilities, but they must preserve versioning/upgrade boundaries. A future schema must not be silently downgrade-managed by an older tool; a new provider must not become a default dependency merely because it exists; a new release gate must be added explicitly to the machine-readable production contract. New Routes should be added only when a genuinely different developer situation cannot be represented by the existing six, not to encode every new collaboration feature.

## Production declaration

A v1.0 source tree may describe the production release contract before it is promoted. The authoritative runtime distribution statement is:

> **A commit is an AAOP production release only when the `stable` channel points to that fully gated commit after the required downstream consumer validation.**

The README Status and package version describe the release line; `stable` + release evidence determine actual production promotion.
