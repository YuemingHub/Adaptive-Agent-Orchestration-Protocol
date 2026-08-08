# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer**.

Its purpose is simple:

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or an operations problem — describe it in ordinary language — and let AAOP route and compose the work without first learning the agent ecosystem.

AAOP does **not** try to become another all-in-one agent framework.

```text
Natural-language developer request
              ↓
Developer intake
              ↓
Primary route
              ↓
Route Capability Pack + Pressure Guards
              ↓
Environment/project evidence
  • what already exists?
  • what is actually current/authoritative?
  • which named technologies are real constraints vs hypotheses?
              ↓
Required capabilities / decision frame
              ↓
Blocked?
  environment / authorization / credential /
  external dependency / product decision
       ↓ no provider workaround
  or genuine capability gap
       ↓
Reuse current capability first
       ↓ only if gap remains
Mature provider + Recipe
       ↓
Applicable scoped adoption review?
  no → continue
  yes → re-check current upstream + actual context
       ↓
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

The developer does **not** choose an Agent, Skill, MCP server, runtime, or workflow mode.

AAOP routes internally:

| Situation | Route | First correct move |
| --- | --- | --- |
| idea / no trustworthy implementation | `idea-to-build` | outcome + first evidence-bearing slice before architecture |
| messy/unfamiliar/contradictory repo | `repo-recovery` | reconstruct current truth before broad edits |
| failure/error/regression | `bug-fix` | baseline → reproduce/evidence → root cause → narrow fix |
| new/changed behavior | `feature-change` | behavior contract → current path → smallest coherent change |
| explanation/review/audit/adoption decision | `understand-review` | frame the decision, inspect current material evidence, no mutation by default |
| deploy/release/migration/incident | `release-operations` | environment truth + authorization + rollback/blocker boundary |

See [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md).

## Idea-to-build: outcome before architecture

A greenfield user may describe a vision together with technologies they have heard about:

```text
“Build it with agents, MCP, RAG, memory, a vector database and graph orchestration.”
```

AAOP does not automatically turn those nouns into architecture requirements.

Classify each named technology as:

```text
hard constraint
preference
solution hypothesis
```

Then find:

1. one actor;
2. one real situation;
3. one observable improvement;
4. the riskiest assumption worth testing now;
5. the smallest end-to-end slice that can produce evidence;
6. only then, the minimum reversible technical shape.

A large future vision is direction, not first-slice scope.

The first slice must **buy learning**. A generated codebase, architecture diagram, ten-agent organization, or polished demo that tests no important assumption is activity, not product evidence.

The non-technical user should not be asked to choose a stack the system can derive later.

## Understand-review: decision before coverage

A review should answer a decision, not maximize how much repository content was read.

For review/adoption/audit work, AAOP asks internally:

```text
What decision are we supporting?
What usage/deployment context changes materiality?
Which claims are current verified facts?
Which are external reports or historical evidence?
What is inference/assumption/unknown?
What recommendation follows for this context?
```

Review is read-only by default. Finding a fixable issue does not authorize a patch, PR, configuration change, or upstream mutation.

Security/reliability severity must be contextualized. An issue headline is not a present-tense conclusion; when practical, material external claims should be checked against the current relevant source/status first.

## Route Capability Packs

AAOP loads exactly one current pack from `.aaop/routes/` after routing.

A pack contains:

- engineering stages and evidence;
- required/optional capabilities;
- exit conditions;
- **pressure guards** learned from real-project failures;
- provider escalation candidates for proven gaps;
- verification and reroute signals.

A pack remains useful even if every named external provider disappears. It is an engineering map, not a workflow engine or install bundle.

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show idea-to-build
python .aaop/tools/route.py show understand-review
```

See [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md).

## Real-project pressure tests

AAOP evolves by **real developer failures before speculative completeness**.

`tests/pressure/` contains replay contracts derived from real repositories/issues. Public sources may be named; lessons from private projects are anonymized before entering this public repository.

The current pressure baseline covers all six routes, including repository authority/freshness, stale bug reports, stale PR salvage, operational blockers, broad-vision overbuild, solution-vocabulary capture, and decision-oriented review.

Every case binds to Route `pressure_guards`; CI prevents those learned invariants from disappearing silently.

```bash
python scripts/validate_pressure.py
```

See [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md).

## Evidence authority and freshness

For messy/long-running projects, a file inventory is not enough. Material claims should be evaluated by the project's own authority/freshness model.

Useful generic roles are:

```text
current-fact
governance
reference
draft/proposed
historical
unknown
```

Project-defined terminology takes precedence.

Hard rules:

- merge-to-main does not automatically make a Draft policy accepted;
- newest timestamp does not automatically beat an explicit current-fact source;
- old PRs/branches/issues are historical evidence until reconciled with current baseline;
- prior AI conclusions and issue comments are not current facts by default;
- external issue/advisory claims should be checked against current source/status when practical;
- deployment/runtime facts require target-environment evidence;
- unresolved conflicts should remain explicit rather than being silently overwritten.

## Blocker before capability gap

When progress stops, AAOP first asks **why**:

```text
missing-evidence
environment
authorization
credential
external-dependency
product-decision
capability-gap
```

Only `capability-gap` directly justifies looking for another provider.

This prevents bad escalation such as:

```text
network policy blocks target
→ install tunnel/VPN/runtime        ✗

no deployment authorization
→ find another write path          ✗

product decision unresolved
→ create more agents               ✗

user mentioned vector DB in an idea
→ install retrieval stack          ✗
```

The correct result can be: preserve unknown state, stop safely, and state the smallest legitimate unblock.

## Recipe-driven environment resolution

Before concluding that a route lacks capability, AAOP inspects what already exists.

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/doctor.py . --route bug-fix --json
```

The Doctor reads detection hints from Integration Recipes instead of maintaining a separate provider catalog.

It can observe host/toolchain commands, project/test/CI/deployment signals, Skills/MCP surfaces, and provider-specific command/package/file evidence.

**Detection means presence, not recommendation/trust/configuration/task fitness.**

## Progressive adoption

Default: **install nothing new**.

```text
Level 0  AAOP protocol only
Level 1  Existing AI IDE / host-native capabilities
Level 2  Existing/local Skills, tests, scripts, tools, MCP
Level 3  ARD / A2A / trusted discovery
Level 4  One justified specialized runtime/harness
Level 5  Governed workspace/control plane
```

These are not mandatory cumulative levels. A project can stay at Level 0/1 indefinitely.

## Integration Recipes

AAOP is not a package manager. `.aaop/recipes/` carries lazy integration knowledge:

- when a provider is/is not appropriate;
- how to detect presence;
- smallest current upstream install/config path;
- credentials/permissions;
- optional scoped, time-stamped `adoption_review` debt;
- verification of the original gap;
- rollback/removal;
- source of truth + last verified date.

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show playwright
python .aaop/tools/recipe.py show autoagent
```

Current integrations cover standards/providers including Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace.

AAOP prefers the smallest provider **surface**, not the entire ecosystem.

### Provider Adoption Review: remember what deserves another look

v0.9 adds an optional Recipe field called `adoption_review`.

It exists for a narrow problem: a real review may uncover an adoption concern that is easy to forget, while the provider and its deployment context continue to change.

AAOP stores the concern as:

```text
reviewed_at
scope
reason
decision_effect
current observations
sources to revisit
required checks
```

It does **not** store a permanent answer such as:

```text
SAFE
UNSAFE
APPROVED
BANNED
```

When a selected provider surface matches the recorded scope, AAOP re-checks current upstream source/status and the actual deployment/permission/network context before consequential adoption.

If the concern is fixed upstream or irrelevant to the selected surface, it should not block adoption; update or retire the stale review. If it remains relevant and cannot be mitigated, narrow/isolate the provider, choose another provider, or defer adoption.

The first scoped example is the AutoAgent Docker-backed command execution path. The Recipe records the current source observations and the public issue that motivated re-verification, while explicitly avoiding a project-wide security verdict.

This is **remembered review debt**, not a security vulnerability database.

## What AAOP owns

- natural-language developer intake and routing;
- Route Capability Packs and real-project Pressure Guards;
- greenfield outcome/solution-hypothesis discipline;
- decision-oriented read-only review discipline;
- evidence authority/freshness discipline;
- recipe-driven environment/provider presence inventory;
- project/outcome/capability discovery;
- blocker classification;
- progressive provider selection and least privilege;
- scoped provider-adoption review debt and re-verification policy;
- verification, replanning, and route correction;
- graceful degradation across hosts.

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
| production agent workflow runtime | Microsoft Agent Framework or equivalent |
| dynamic workforce patterns | CAMEL or equivalent |
| agent/tool/workflow generation | AutoAgent when justified |
| multi-user governance/workspace | AgentSpace or equivalent |

See [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md).

## Quick start

```bash
python scripts/install.py /path/to/project
```

The installer copies the `.aaop` protocol package and adds a compact bootstrap to existing `AGENTS.md` / `CLAUDE.md` without replacing project rules. It installs no third-party runtime/MCP/provider and requests no secret.

Then open the project in the AI host you already use and describe what you want in ordinary language.

## Repository map

```text
AGENTS.md
CLAUDE.md
.aaop/
├── ORCHESTRATOR.md
├── policies/
├── registries/
├── routes/                          # route capability packs + pressure guards
├── recipes/                         # lazy integration/detection + optional adoption review debt
├── schemas/
│   ├── pressure-case.schema.json
│   ├── integration-recipe.schema.json
│   ├── environment-inventory.schema.json
│   └── ...
├── skills/
│   ├── developer-intake/
│   ├── provider-selection/
│   ├── route-execution/
│   └── ...
└── tools/
    ├── doctor.py
    ├── route.py
    └── recipe.py

tests/pressure/                      # source-repo regression cases
scripts/validate_pressure.py
docs/REAL_PROJECT_PRESSURE_TESTS.md
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. For ideas: outcome and evidence-bearing first slice before architecture.
4. Treat early solution vocabulary as hypothesis unless established as a constraint.
5. For reviews: decision before coverage; current evidence before conclusion; no mutation by default.
6. Current baseline and source authority before trusting stale artifacts.
7. Route by observable outcome, not developer jargon.
8. Route Packs are thin engineering maps, not proprietary workflows.
9. Detect/reuse existing capability before concluding there is a gap.
10. Classify blockers before provider escalation.
11. Install nothing new without a proven technical capability gap.
12. Re-check applicable provider adoption debt before consequential use; never turn it into a permanent label.
13. Prefer mature upstream implementations over copies.
14. Select the minimum provider surface.
15. Verify outcomes; do not fabricate completion when safely blocked.
16. Let real-project regressions improve the protocol before adding theoretical completeness.
17. Hide orchestration complexity without lowering engineering rigor.

## Status

**v0.9.0 — scoped provider adoption review debt.**

v0.9 adds an optional, schema-validated `adoption_review` to Integration Recipes and teaches provider selection to re-verify relevant concerns against current upstream and actual deployment context before adoption. The first real example is scoped to AutoAgent's Docker-backed command execution surface observed during the v0.8 adoption review.

No new provider/framework/runtime was added in v0.9, and AAOP does not become a security database or provider certification system.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
