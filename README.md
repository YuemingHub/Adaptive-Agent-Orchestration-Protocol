# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer**.

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or an operations problem, describe it in ordinary language, and let AAOP route and compose the work without first learning the agent ecosystem.

AAOP does **not** try to become another all-in-one agent framework.

```text
Natural-language request
        ↓
Host-native project bootstrap
        ↓
Developer Intake
        ↓
Primary Route
        ↓
Route Capability Pack + Pressure Guards
        ↓
Bounded project/environment/instruction evidence
        ↓
Required capabilities / decision frame
        ↓
Blocker classification
        ↓
Reuse current capability first
        ↓ only for a proven capability gap
Mature Provider + Integration Recipe
        ↓
Applicable adoption-review debt?
        ↓ re-check current upstream/context when needed
Execute → Verify → Re-route/Replan
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

The developer does **not** choose an Agent, Skill, MCP server, runtime, workflow mode, or AAOP host mode.

| Situation | Route | First correct move |
| --- | --- | --- |
| idea / no trustworthy implementation | `idea-to-build` | outcome + first evidence-bearing slice before architecture |
| messy/unfamiliar/contradictory repo | `repo-recovery` | reconstruct current truth before broad edits |
| failure/error/regression | `bug-fix` | baseline → reproduce/evidence → root cause → narrow fix |
| new/changed behavior | `feature-change` | behavior contract → current path → smallest coherent change |
| explanation/review/audit/adoption decision | `understand-review` | frame the decision; no mutation by default |
| deploy/release/migration/incident | `release-operations` | environment truth + authorization + rollback/blocker boundary |

See [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md).

## Host-native bootstrap

AAOP activates through project-instruction surfaces already supported by coding hosts:

| Host | Native project entry | AAOP mapping |
| --- | --- | --- |
| Codex | `AGENTS.md` / scoped instruction files | root `AGENTS.md` is the common bridge |
| Claude Code | project `CLAUDE.md` | root `CLAUDE.md` is a thin Claude-specific bridge |
| Cursor | root `AGENTS.md`; Cursor CLI also reads root `CLAUDE.md` | common bridge in `AGENTS.md`, thin `CLAUDE.md` bridge |

All converge on:

```text
.aaop/ORCHESTRATOR.md
→ .aaop/skills/developer-intake/SKILL.md
→ .aaop/skills/route-execution/SKILL.md
→ .aaop/routes/<route-id>.json
```

AAOP does not generate `.cursor/rules` merely to duplicate root instructions. Host-specific facts and verification dates stay in `adapters/`, not in the host-neutral Orchestrator.

See [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md).

## Instruction topology

A mature repository can already contain multiple instruction layers:

```text
AGENTS.md
backend/AGENTS.md
backend/AGENTS.override.md

CLAUDE.md
services/CLAUDE.md

.cursor/rules/global.mdc
frontend/.cursor/rules/ui.mdc
```

Use the read-only inventory when instruction scope can materially change the task:

```bash
python .aaop/tools/instructions.py .
python .aaop/tools/instructions.py . --json
```

**Topology is evidence, not conflict resolution.** A nested/newer rule is not automatically correct, globally active, or safe to rewrite.

See [`docs/INSTRUCTION_TOPOLOGY.md`](docs/INSTRUCTION_TOPOLOGY.md).

## Bounded discovery: know when to stop reading

v0.15 adds a rule learned from three real repository shapes: a governance-heavy reference graph, a small handoff repository, and a long-running product repository with explicit first-read/history exclusions.

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

Treat these as navigation, not mandatory reading lists:

- `related` / `depends_on` graphs;
- source registries and indexes;
- ADR/RFC link collections;
- historical release/deployment lists;
- directory inventories;
- generated documentation surfaces.

Follow a reference only when it can change the immediate route, current baseline, implementation target, acceptance evidence, or risk boundary.

Three practical rules:

1. **Explicitly governed long-running repo:** obey the project's declared first-read/current-source order and explicit historical exclusions before broad search.
2. **Governance/reference-heavy repo:** use current/canonical state + source-role registry as navigation anchors; do not recursively traverse the whole governance graph.
3. **Small repo/handoff:** if README + handoff/current-status + manifest already establish current state and one next target, stop discovery and inspect implementation only as that target requires.

This is not a fixed file/token budget. Sometimes deeper reading is necessary; it must be justified by a concrete unresolved question.

The canonical procedure lives in `.aaop/skills/project-discovery/SKILL.md`. The `repo-recovery` route protects it with the real-project `bounded-evidence-traversal` Pressure Guard.

## Idea-to-build: outcome before architecture

Early solution vocabulary such as Agent, MCP, RAG, vector DB, graph, or memory is classified as a **hard constraint**, **preference**, or **solution hypothesis** rather than automatically becoming architecture.

AAOP first finds:

1. one actor;
2. one real situation;
3. one observable improvement;
4. the riskiest assumption worth testing now;
5. the smallest end-to-end slice that buys useful evidence;
6. only then, the minimum reversible technical shape.

A broad future vision is direction, not first-slice scope. The non-technical user should not be asked to choose a stack the system can derive later.

## Understand-review: decision before coverage

Review starts from the decision it must support, then inspects the minimum evidence necessary to distinguish:

```text
current verified facts
historical/external claims
inference
assumptions
unknowns
recommendations
```

Review is read-only by default. Finding a fixable issue does not authorize a patch or upstream mutation. Security/reliability risk must be contextualized to actual exposure and permissions rather than copied from a headline.

## Route Capability Packs

After routing, AAOP loads one pack from `.aaop/routes/` containing:

- engineering stages and evidence;
- required/optional capabilities;
- exit conditions;
- real-project **Pressure Guards**;
- provider escalation candidates for proven gaps;
- verification and reroute signals.

A pack is an engineering map, not a workflow engine or install bundle.

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show repo-recovery
```

See [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md).

## Real-project pressure tests

AAOP evolves by **real developer failures before speculative completeness**.

`tests/pressure/` contains privacy-safe replay contracts covering all six routes. Current lessons include:

- repository authority/freshness;
- bounded evidence traversal / stop-when-sufficient discovery;
- stale bug reports;
- stale PR salvage;
- operational blockers;
- broad-vision overbuild;
- solution-vocabulary capture;
- decision-oriented review.

Each case binds to Route `pressure_guards`; removing an earned guard breaks CI until the regression is deliberately re-evaluated.

```bash
python scripts/validate_pressure.py
```

See [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md).

## Evidence authority and freshness

Material claims are evaluated by the project's own authority/freshness model. Useful generic roles are:

```text
current-fact
governance
reference
draft/proposed
historical
unknown
```

Hard rules:

- merged/main/newest does not automatically mean authoritative;
- canonical/current documents can be navigation anchors without making every linked artifact mandatory reading;
- explicit first-read and historical-exclusion rules narrow discovery unless the task needs the excluded evidence;
- old PRs/issues/branches are historical evidence until reconciled with the current baseline;
- prior AI conclusions and issue comments are hypotheses/reference by default;
- runtime/deployment facts require target-environment evidence;
- unresolved conflicts remain explicit instead of being silently flattened.

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
user mentioned vector DB     → install retrieval stack     ✗
```

Sometimes the correct result is to preserve unknown state and state the smallest legitimate unblock.

## Environment resolution

Before concluding a capability is missing:

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/doctor.py . --route feature-change --json
```

The Doctor reads provider-specific detection hints from Integration Recipes instead of maintaining a second provider catalog.

**Detection means presence, not recommendation, trust, authorization, configuration correctness, or task fitness.**

## Progressive adoption

Default: **install nothing new**.

```text
Level 0  AAOP protocol only
Level 1  existing host-native capability
Level 2  existing/local Skills, tests, scripts, tools, MCP
Level 3  ARD / A2A / trusted discovery
Level 4  one justified specialized runtime/harness
Level 5  governed workspace/control plane
```

These are not mandatory cumulative levels. A project can stay at Level 0/1 indefinitely.

## Integration Recipes

`.aaop/recipes/` contains lazy integration knowledge, not vendored dependencies or an AAOP package manager:

- when a provider is/is not appropriate;
- detection hints;
- smallest current upstream integration path;
- credentials/permissions;
- optional scoped `adoption_review` debt;
- verification;
- rollback/removal;
- source of truth + last verified date.

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show playwright
python .aaop/tools/recipe.py show autoagent
```

Current coverage includes Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace.

A scoped adoption review remembers **what deserves another look**, not a permanent `SAFE/UNSAFE` verdict. If its scope applies, AAOP re-checks current upstream and the actual deployment/permission/network context before consequential adoption.

## Safe lifecycle: install, upgrade, inspect, remove

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

Typical states include `healthy`, `upgrade-recommended`, `legacy-install`, `drifted`, `incomplete`, and invalid/unsupported manifest states.

Health is **best-effort accidental-drift detection**, not a cryptographic trust root and not a latest-version checker.

## What AAOP owns

- natural-language developer intake and routing;
- host-native bootstrap conformance and duplicate-context minimization;
- read-only instruction-topology discovery for scoped host/project rules;
- bounded project discovery and evidence traversal;
- Route Capability Packs and real-project Pressure Guards;
- greenfield outcome/solution-hypothesis discipline;
- decision-oriented read-only review discipline;
- evidence authority/freshness discipline;
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
scripts/install.py
scripts/validate.py
scripts/validate_pressure.py
scripts/validate_host_bootstrap.py
docs/HOST_BOOTSTRAP_CONFORMANCE.md
docs/INSTRUCTION_TOPOLOGY.md
docs/REAL_PROJECT_PRESSURE_TESTS.md
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. Use host-native instruction discovery; do not make the user activate AAOP manually.
4. Keep one canonical policy and minimize duplicate persistent host context.
5. See scoped instruction topology before assuming root rules are the complete effective context.
6. Never treat topology inventory as automatic conflict resolution or permission to rewrite project rules.
7. Define the immediate decision horizon before broad discovery.
8. Start from explicit project first-read/current/canonical entrypoints when they exist.
9. Treat reference graphs and inventories as navigation, not mandatory coverage.
10. Stop when additional reading is unlikely to change the route, baseline, target, acceptance evidence, capability plan, or risk model.
11. For ideas: outcome and evidence-bearing first slice before architecture.
12. Treat early solution vocabulary as hypothesis unless established as a constraint.
13. For reviews: decision before coverage; current evidence before conclusion; no mutation by default.
14. Current baseline/source authority before stale artifacts.
15. Route by observable outcome, not developer jargon.
16. Detect/reuse existing capability before concluding there is a gap.
17. Classify blockers before provider escalation.
18. Install nothing new without a proven technical capability gap.
19. Re-check applicable provider adoption debt before consequential use.
20. Preserve runtime/project-owned state across AAOP lifecycle operations.
21. Remove only what AAOP can prove it owns.
22. Prefer mature upstream implementations over copies.
23. Select the minimum provider surface.
24. Verify outcomes; do not fabricate completion when safely blocked.
25. Let real-project regressions improve the protocol before theoretical completeness.
26. Hide orchestration complexity without lowering engineering rigor.

## Status

**v0.15.0 — bounded evidence traversal and stop-when-sufficient discovery.**

v0.15 is grounded in three real repository shapes inspected after v0.14: a governance-heavy public repository with a large reference graph, a small public handoff repository whose README/HANDOFF already bounded the next move, and an anonymized long-running product repository with explicit first-read/history-exclusion rules.

It adds no new tool, Route, Provider, runtime, package manager, or arbitrary scan budget. It tightens Project Discovery and `repo-recovery` so AAOP starts from explicit current/canonical entrypoints, follows references only for material unresolved questions, and stops when the immediate engineering decision is defensible.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
