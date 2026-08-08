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
  local delta       → execute / reroute → verify
  verified no-op    → stop without cosmetic diff
  blocked           → precise legitimate unblock
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

## Instruction topology

Mature repositories can contain scoped host rules below the root:

```text
AGENTS.md
backend/AGENTS.override.md
CLAUDE.md
services/CLAUDE.md
.cursor/rules/global.mdc
frontend/.cursor/rules/ui.mdc
```

When that scope can materially change the task:

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

The `repo-recovery` route protects this with `bounded-evidence-traversal`.

## Cross-repository scope

A repository map can express directional authority without creating a multi-repository task.

```text
local decision
→ active repository/work target
→ identify external claim owner
→ check local dependency/coordination record
→ current + sufficient? → stay local
→ stale / ambiguous / insufficient?
     ↓
  read minimum authoritative external source/revision
     ↓
  record source + revision + status
     ↓
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

v0.17 closes the gap between “understand” and “act”.

Authorization to continue work is not evidence that a change is necessary. Before material mutation, compare the requested/route outcome with current evidence:

```text
local-delta
→ a current difference exists in the active work target
→ execute the smallest coherent change and verify

verified-no-op
→ the desired state already holds, or no current local mutation is justified
→ record evidence and do not manufacture a diff

reroute
→ the real delta belongs to another route, repository, or action class

blocked
→ legitimate execution lacks evidence, environment, authorization,
   credential, external dependency, or product decision
```

This rule cuts both ways:

- **no proven delta** → do not edit merely to demonstrate progress;
- **proven local authorized delta** → do not remain in analysis mode;
- project-declared planning, test, review, permission, and release gates still apply once a delta is proven.

For `repo-recovery`, recovery can therefore end in a verified `no-local-mutation-justified` result, or transition directly into the smallest local stabilization / `bug-fix` / `feature-change` path.

The general behavior lives in `.aaop/skills/route-execution/SKILL.md`; `repo-recovery` protects it with `prove-delta-before-mutation`.

## Idea-to-build: outcome before architecture

Early solution vocabulary such as Agent, MCP, RAG, vector DB, graph, or memory is classified as a **hard constraint**, **preference**, or **solution hypothesis** rather than automatically becoming architecture.

AAOP first finds one actor, one real situation, one observable improvement, the riskiest assumption worth testing, and the smallest end-to-end slice that buys useful evidence. Only then should it choose the minimum reversible technical shape.

## Review: decision before coverage

`understand-review` starts from the decision it must support and distinguishes:

```text
current verified facts
historical/external claims
inference
assumptions
unknowns
recommendations
```

Review is read-only by default. A finding does not authorize a patch. Risk is contextualized to actual exposure and permissions rather than copied from a headline.

## Route Capability Packs + real pressure guards

After routing, AAOP loads one pack from `.aaop/routes/`. A pack contains engineering stages/evidence, required/optional capabilities, exit conditions, real-project **Pressure Guards**, justified provider escalation candidates, verification, and reroute signals.

A pack is an engineering map, not a workflow engine.

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show repo-recovery
python scripts/validate_pressure.py
```

`tests/pressure/` contains privacy-safe real-project replay contracts. Current lessons include:

- source authority/freshness and conflict preservation;
- stop-when-sufficient discovery;
- cross-repository evidence vs work scope;
- **prove delta before mutation / verified no-op vs action paralysis**;
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

Only `capability-gap` directly justifies adding another provider.

```text
network policy blocks target → install tunnel/runtime      ✗
missing deployment auth      → find another write path     ✗
product decision unresolved  → create more agents          ✗
no current local delta       → invent cleanup/refactor      ✗
```

Sometimes the correct result is a precise blocker; sometimes it is a verified no-op. Neither should be disguised as a need for more machinery.

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

`.aaop/recipes/` contains lazy integration knowledge, not vendored dependencies or an AAOP package manager:

- when a provider is/is not appropriate;
- detection hints;
- smallest current upstream integration path;
- credentials/permissions;
- optional scoped `adoption_review` debt;
- verification and rollback/removal;
- source of truth + last verified date.

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

Health asks only:

> Does this local AAOP installation still match the baseline installed/upgraded here?

It is best-effort accidental-drift detection, not a cryptographic trust root and not a latest-version checker.

## What AAOP owns

- natural-language developer intake and routing;
- host-native bootstrap conformance;
- read-only instruction-topology discovery;
- bounded project and cross-repository evidence resolution;
- **execution-delta proof before mutation and verified no-op discipline**;
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

## What AAOP deliberately reuses

| Need | Mature ecosystem layer |
| --- | --- |
| reusable procedure | Agent Skills |
| external tools/services | MCP |
| independent agent interoperability | A2A |
| broad agentic resource discovery | ARD |
| structured spec-driven SDLC | GitHub Spec Kit when justified |
| browser testing/automation | appropriate Playwright surface |
| bounded SWE issue solver | mini-SWE-agent when justified |
| autonomous coding runtime/SDK | OpenHands when justified |
| long-horizon/subagent harness | Deep Agents or equivalent |
| production workflow runtime | Microsoft Agent Framework or equivalent |
| dynamic workforce patterns | CAMEL or equivalent |
| agent/tool/workflow generation | AutoAgent when justified |
| multi-user governance/workspace | AgentSpace or equivalent |

See [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md).

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
├── VERSION
├── ORCHESTRATOR.md
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
4. Define the immediate decision horizon and active repository/work target before broad discovery.
5. Treat instruction/reference/repository graphs as navigation, not automatic authority or execution scope.
6. Stop discovery when additional evidence is unlikely to change the current decision.
7. Keep cross-repository evidence access separate from mutation authorization.
8. **Prove a current execution delta before material mutation.**
9. Accept verified no-op when no mutation is justified; never create a cosmetic diff for progress theater.
10. When a current authorized local delta is proven, execute/reroute rather than remaining in analysis.
11. Preserve repository-specific planning, test, review, permission, and release gates.
12. For ideas: outcome and evidence-bearing first slice before architecture.
13. For reviews: decision before coverage; current evidence before conclusion; no mutation by default.
14. Current source authority/freshness before stale artifacts.
15. Detect/reuse existing capability before concluding there is a gap.
16. Classify blockers before provider escalation.
17. Install nothing new without a proven technical capability gap.
18. Preserve runtime/project-owned state across AAOP lifecycle operations.
19. Remove only what AAOP can prove it owns.
20. Prefer mature upstream implementations and the minimum provider surface.
21. Verify outcomes; do not fabricate completion when safely blocked.
22. Let real-project regressions improve the protocol before theoretical completeness.
23. Hide orchestration complexity without lowering engineering rigor.

## Status

**v0.17.0 — prove execution delta before mutation.**

v0.17 is grounded in two opposite public-repository pressure cases. Current MingOS coordination showed that “continue autonomously” can correctly resolve to no local mutation when the next shared-protocol change is conditional on evidence not yet available. `ymai-website` showed the opposite: when recovery finds a concrete current local stale reference inside the requested action class, AAOP must leave analysis and move into the bounded fix/verification path.

The release makes `verified-no-op` a first-class successful engineering result while simultaneously requiring execution when a real current local delta is proven. It adds no Route, Provider, Recipe, runtime, tool, mandatory diff, or bypass around project-specific gates.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
