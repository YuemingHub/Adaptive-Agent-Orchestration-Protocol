# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer**.

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or an operations problem, describe it in ordinary language, and let AAOP determine the smallest justified engineering path without first learning the agent ecosystem.

AAOP does **not** try to become another all-in-one agent framework.

```text
Natural-language request
        ↓
Host-native bootstrap
        ↓
Developer Intake → one primary Route
        ↓
Bounded project / instruction / cross-repository evidence
        ↓
Desired outcome vs current evidence
        ↓
Proven execution delta?
  local delta       → prepare smallest change
  verified no-op    → stop without cosmetic diff
  reroute / blocked → correct scope or legitimate unblock
        ↓
At write boundary: baseline/precondition still current?
  yes → write / merge / operate → verify
  no  → re-read → preserve concurrent work → re-prove delta
        ↓
Only a proven capability gap may justify a Provider
```

## Developer front door

Minimal requests are enough:

```text
“I have an idea but don't know how to build it.”
“This repo is a mess. Understand it and continue.”
“Login returns 500. Fix it.”
“Add family invitations.”
“Review this before I merge.”
“Should we adopt this agent framework?”
“Get this ready to deploy.”
```

The developer does **not** choose an Agent, Skill, MCP server, runtime, workflow mode, team topology, or AAOP host mode.

| Situation | Route | First correct move |
| --- | --- | --- |
| idea / no trustworthy implementation | `idea-to-build` | outcome + first evidence-bearing slice before architecture |
| messy/unfamiliar/contradictory repo | `repo-recovery` | reconstruct current truth before broad edits |
| failure/error/regression | `bug-fix` | baseline → reproduce/evidence → root cause → narrow fix |
| new/changed behavior | `feature-change` | behavior contract → current path → smallest coherent change |
| explanation/review/audit/adoption decision | `understand-review` | frame the decision; no mutation by default |
| deploy/release/migration/incident | `release-operations` | environment truth + authorization + rollback/blocker boundary |

See [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md).

## One canonical policy, host-native entry

AAOP uses project-instruction surfaces the developer's existing coding host already supports:

| Host | Native entry | AAOP mapping |
| --- | --- | --- |
| Codex | `AGENTS.md` / scoped AGENTS files | root `AGENTS.md` common bridge |
| Claude Code | project `CLAUDE.md` | thin Claude-specific bridge |
| Cursor | root `AGENTS.md`; CLI also reads root `CLAUDE.md` | common bridge + deliberately thin Claude bridge |

All converge on:

```text
.aaop/ORCHESTRATOR.md
→ .aaop/skills/developer-intake/SKILL.md
→ .aaop/skills/route-execution/SKILL.md
→ .aaop/routes/<route-id>.json
```

AAOP does not generate `.cursor/rules` merely to repeat root bootstrap context.

See [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md).

## One package release identity

AAOP has exactly one installable package release identity:

```text
.aaop/VERSION
```

Other version-like fields have narrower meanings:

```text
.aaop/VERSION                  → installable package release
ORCHESTRATOR Protocol-Revision → orchestration document revision
Route Pack version             → route component revision
Recipe last_verified           → upstream integration-evidence freshness
Skill history                  → Git unless component-specific metadata is genuinely needed
```

The installer, manifest, and health contract never infer the package release from component documents. A source package with a missing, unreadable, or empty `.aaop/VERSION` is **incomplete** and installation fails closed before AAOP-managed package files are copied.

Do not mechanically rewrite every Route, Skill, Recipe, or protocol component to match the package release. Component revisions can evolve independently; they simply must not masquerade as the package release.

See [`.aaop/VERSIONING.md`](.aaop/VERSIONING.md).

## Instruction topology

Mature repositories can contain scoped host rules below the root. When that scope can materially change the task:

```bash
python .aaop/tools/instructions.py .
python .aaop/tools/instructions.py . --json
```

**Topology is evidence, not conflict resolution.** A nested/newer rule is not automatically correct, globally active, or safe to rewrite.

See [`docs/INSTRUCTION_TOPOLOGY.md`](docs/INSTRUCTION_TOPOLOGY.md).

## Bounded discovery

The target is **minimum sufficient evidence for the current decision**, not maximum repository coverage.

```text
current request
→ governing instructions
→ declared current/canonical entrypoints
→ material unknown
→ one supporting reference if needed
→ relevant implementation/test/runtime evidence
→ stop
```

Treat `related` / `depends_on` graphs, registries, indexes, ADR/RFC collections, historical release lists, directory inventories, generated documentation, and repository maps as navigation rather than mandatory reading lists.

Follow an edge only when it can change the route, current baseline, implementation target, acceptance evidence, dependency status, or risk boundary. This is not a fixed file/token budget; deeper reading is appropriate when a concrete material question remains unresolved.

`repo-recovery` protects this with `bounded-evidence-traversal`.

## Cross-repository scope

A repository map can express directional authority without creating a multi-repository task.

```text
local decision
→ active repository/work target
→ identify external claim owner
→ check local dependency/coordination record
→ current + sufficient? stay local
→ stale / ambiguous / insufficient?
    read minimum authoritative external source/revision
    record source + revision + status
    return to local decision
```

Hard boundaries:

- a referenced repository is not automatically an active work target;
- coordination/navigation material does not replace each repository's own current fact sources;
- a current downstream dependency snapshot can be sufficient for ordinary local work;
- **read access does not authorize mutation**;
- product evidence can become an upstream proposal, but does not silently become shared protocol/governance through incidental edits.

AAOP does not provide a multi-repository runtime, repository graph crawler, or synchronized commit mechanism. `repo-recovery` protects this with `cross-repository-scope-boundary`.

## Prove the execution delta before mutation

Authorization to continue work is not evidence that a change is necessary. Before material mutation, compare the requested/route outcome with current evidence:

```text
local-delta
→ a current difference exists in the active work target
→ prepare the smallest coherent change

verified-no-op
→ the desired state already holds, or no current local mutation is justified
→ record evidence and do not manufacture a diff

reroute
→ the real delta belongs to another route, repository, or action class

blocked
→ legitimate execution lacks evidence, environment, authorization,
   credential, external dependency, or product decision
```

The rule cuts both ways:

- **no proven delta** → do not edit merely to demonstrate progress;
- **proven local authorized delta** → do not remain in analysis mode;
- project-declared planning, test, review, permission, and release gates still apply once a delta is proven.

The general behavior lives in `.aaop/skills/route-execution/SKILL.md`; `repo-recovery` protects it with `prove-delta-before-mutation`.

## Revalidate the baseline at the write boundary

A delta can be correct when discovered and stale by the time the write lands.

```text
read baseline A
→ prove delta
→ before consequential write require/revalidate A
→ still A?
     write + verify
→ target is now B?
     re-read B
     preserve concurrent work
     recompute the intended delta
     rerun the execution-delta gate
     re-check authorization/risk if the action changed
     retry conditionally from B only if still justified
```

Prefer the strongest native precondition available:

- Git content/blob SHA;
- expected branch/PR head or ref ancestry;
- ETag / `If-Match`;
- resource version/generation;
- database row/version;
- lease/lock token;
- deployment revision.

A failed precondition is **new evidence**, not a nuisance retry. It is first a baseline/concurrency problem—not automatically a capability gap.

`force` is a separate, higher-risk action class. It is appropriate only when repository policy and user authorization intentionally permit replacement and the overwritten state has been understood/preserved as required.

The general contract lives in `.aaop/policies/autonomy.md` and `.aaop/skills/route-execution/SKILL.md`. `feature-change` and `release-operations` protect consequential writes with `revalidate-write-precondition`.

## Idea-to-build: outcome before architecture

Early solution vocabulary such as Agent, MCP, RAG, vector DB, graph, or memory is classified as a **hard constraint**, **preference**, or **solution hypothesis** rather than automatically becoming architecture.

AAOP first finds one actor, one real situation, one observable improvement, the riskiest assumption worth testing, and the smallest end-to-end slice that buys useful evidence. Only then should it choose the minimum reversible technical shape.

## Review: decision before coverage

`understand-review` starts from the decision it must support and distinguishes current verified facts, historical/external claims, inference, assumptions, unknowns, and recommendations.

Review is read-only by default. A finding does not authorize a patch. Risk is contextualized to actual exposure and permissions rather than copied from a headline.

## Route Capability Packs + real pressure guards

After routing, AAOP loads one pack from `.aaop/routes/`. A pack contains engineering stages/evidence, required/optional capabilities, exit conditions, real-project **Pressure Guards**, justified provider escalation candidates, verification, and reroute signals.

A pack is an engineering map, not a workflow engine.

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show feature-change
python scripts/validate_pressure.py
```

`tests/pressure/` contains privacy-safe real-project replay contracts. Current lessons include:

- source authority/freshness and conflict preservation;
- stop-when-sufficient discovery;
- cross-repository evidence vs work scope;
- prove delta before mutation / verified no-op vs action paralysis;
- **write-precondition revalidation / stale-write reconciliation**;
- stale bug/PR baselines;
- operational blockers;
- broad-vision overbuild and solution-vocabulary capture;
- decision-oriented review.

Removing an earned guard breaks CI until the regression is deliberately re-evaluated.

See [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md).

## Blocker before capability gap

When progress stops, classify why:

```text
missing-evidence
environment
authorization
credential
external-dependency
product-decision
capability-gap
```

A stale/moved write target is handled first by revalidation/reconciliation, not by adding another Provider.

Only a genuine `capability-gap` directly justifies adding machinery.

## Environment resolution and progressive adoption

Before concluding a capability is missing:

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/doctor.py . --route feature-change --json
```

**Detection means presence, not recommendation, trust, authorization, configuration correctness, or task fitness.**

Default: **install nothing new**.

```text
Level 0  AAOP protocol only
Level 1  existing host-native capability
Level 2  existing/local Skills, tests, scripts, tools, MCP
Level 3  ARD / A2A / trusted discovery
Level 4  one justified specialized runtime/harness
Level 5  governed workspace/control plane
```

These are not mandatory cumulative levels.

## Integration Recipes

`.aaop/recipes/` contains lazy integration knowledge, not vendored dependencies or an AAOP package manager: selection conditions, detection hints, smallest upstream integration path, credentials/permissions, scoped adoption-review debt, verification, rollback/removal, and source-of-truth metadata.

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show playwright
python .aaop/tools/recipe.py show autoagent
```

Current coverage includes Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace.

## Safe lifecycle

```bash
# install
python scripts/install.py /path/to/project

# state-preserving upgrade
python scripts/install.py /path/to/project --upgrade

# local integrity/drift check
python /path/to/project/.aaop/tools/health.py /path/to/project

# manifest-scoped removal
python scripts/install.py /path/to/project --uninstall
```

Ownership stays explicit:

```text
AAOP-managed protocol files        → upgrade/remove by manifest ownership
.aaop/runtime/                     → preserved
project-only files inside .aaop/   → preserved
AGENTS/CLAUDE text outside markers → preserved
AAOP marker blocks                 → update/remove inside boundary only
third-party providers              → untouched
```

Locally modified managed files/bootstrap blocks are backed up before canonical replacement/removal. Malformed marker pairs fail before package mutation. Legacy no-manifest installs can upgrade safely but cannot be automatically uninstalled until ownership is established.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Installation health

```bash
python .aaop/tools/health.py .
python .aaop/tools/health.py . --json
```

Health asks only whether the local AAOP installation still matches the baseline installed/upgraded here. It is best-effort accidental-drift detection, not a cryptographic trust root and not a latest-version checker.

## What AAOP owns

- natural-language developer intake and routing;
- host-native bootstrap conformance;
- **single package release identity and fail-closed source version semantics**;
- read-only instruction-topology discovery;
- bounded project and cross-repository evidence resolution;
- execution-delta proof before mutation and verified no-op discipline;
- write-baseline/precondition revalidation before consequential autonomous mutation;
- Route Capability Packs and real-project Pressure Guards;
- outcome-before-architecture and decision-before-coverage discipline;
- evidence authority/freshness;
- environment/provider presence inventory;
- blocker classification;
- progressive provider selection and least privilege;
- scoped provider-adoption review debt;
- manifest-scoped install/upgrade/uninstall with low lock-in;
- read-only AAOP installation health;
- verification, replanning, and route correction.

AAOP deliberately reuses mature upstream layers for Skills, MCP, A2A, ARD, spec-driven workflows, browser automation, coding runtimes, long-horizon harnesses, and governed workspaces rather than copying them into AAOP. See [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md).

## Quick start

```bash
python scripts/install.py /path/to/project
```

Then open the project in the AI host you already use and describe what you want in ordinary language. No AAOP host-mode selection is required.

## Repository map

```text
AGENTS.md
CLAUDE.md
.aaop/
├── VERSION                          # sole package release identity
├── VERSIONING.md                    # release vs component revision contract
├── ORCHESTRATOR.md                  # independent Protocol-Revision
├── policies/
├── registries/
├── routes/
├── recipes/
├── schemas/
├── skills/
└── tools/
    ├── doctor.py
    ├── health.py
    ├── instructions.py
    ├── route.py
    └── recipe.py

adapters/
tests/pressure/
scripts/
docs/
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. Use host-native instruction discovery and one canonical policy.
4. Keep `.aaop/VERSION` as the sole package release identity; never infer release identity from component revisions.
5. Define the immediate decision horizon and active repository/work target before broad discovery.
6. Treat instruction/reference/repository graphs as navigation, not automatic authority or execution scope.
7. Stop discovery when additional evidence is unlikely to change the current decision.
8. Keep cross-repository evidence access separate from mutation authorization.
9. Prove a current execution delta before material mutation.
10. Accept verified no-op when no mutation is justified; never create a cosmetic diff for progress theater.
11. When a current authorized local delta is proven, execute/reroute rather than remaining in analysis.
12. Revalidate the write/merge/operational baseline at the consequential write boundary.
13. A failed write precondition is new evidence: re-read, preserve concurrent work, re-prove the delta, then retry conditionally if still justified.
14. Never use force as the default recovery path for stale state.
15. Preserve repository-specific planning, test, review, permission, and release gates.
16. For ideas: outcome and evidence-bearing first slice before architecture.
17. For reviews: decision before coverage; current evidence before conclusion; no mutation by default.
18. Detect/reuse existing capability before concluding there is a gap.
19. Classify blockers before provider escalation.
20. Install nothing new without a proven technical capability gap.
21. Preserve runtime/project-owned state across AAOP lifecycle operations.
22. Remove only what AAOP can prove it owns.
23. Prefer mature upstream implementations and the minimum provider surface.
24. Verify outcomes; do not fabricate completion when safely blocked.
25. Let real-project regressions improve the protocol before theoretical completeness.
26. Hide orchestration complexity without lowering engineering rigor.

## Status

**v0.19.0 — single package release identity and fail-closed version semantics.**

v0.19 removes a real lifecycle ambiguity: the installable package could be `0.18.0` while the Orchestrator still displayed `Version: 0.9.0`, and the installer used that component header as a fallback if `.aaop/VERSION` disappeared. A damaged source tree could therefore silently write the wrong `aaop_version` into a new install manifest.

The release makes `.aaop/VERSION` the only package release identity, separates the Orchestrator's `Protocol-Revision`, removes stale Skill `aaop-version` metadata, and makes validator/health/installer fail closed on missing release identity. It adds no remote version service, Git-tag dependency, package registry, component-version registry, Route, Provider, or runtime.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
