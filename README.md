# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer**.

Its purpose is simple:

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or an operations problem — describe it in ordinary language — and let AAOP route and compose the work without first learning the agent ecosystem.

AAOP does **not** try to become another all-in-one agent framework.

```text
Natural-language developer request
              ↓
Host-native project bootstrap
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

The developer does **not** choose an Agent, Skill, MCP server, runtime, workflow mode, or AAOP host mode.

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

## Host-native bootstrap

AAOP should become active through the project-instruction surfaces the developer's existing coding host already supports. The developer should not have to say “read `.aaop` first” or select a host-specific AAOP mode.

Current verified strategy:

| Host | Native project entry | AAOP mapping |
| --- | --- | --- |
| Codex | root/scoped `AGENTS.md` | root `AGENTS.md` is the common AAOP bridge |
| Claude Code | project `CLAUDE.md` | root `CLAUDE.md` is a thin Claude-specific bridge |
| Cursor | root `AGENTS.md`; Cursor CLI also reads root `CLAUDE.md` | use `AGENTS.md` as common bridge; keep `CLAUDE.md` deliberately small |

All paths converge on:

```text
.aaop/ORCHESTRATOR.md
        ↓
.aaop/skills/developer-intake/SKILL.md
        ↓
.aaop/skills/route-execution/SKILL.md
        ↓
.aaop/routes/<route-id>.json
```

AAOP does **not** generate `.cursor/rules` merely to repeat the root bootstrap. Cursor-specific rules remain available when a project genuinely needs Cursor-native scoping.

Why the thin `CLAUDE.md` bridge matters: Cursor CLI reads both root `AGENTS.md` and root `CLAUDE.md`; maintaining the full bootstrap in both would duplicate persistent context without improving capability.

Host behavior changes independently of AAOP. First-party sources and the last verification date live in `adapters/`, and static CI protects AAOP's side of the contract without pretending it can prove proprietary-host runtime behavior.

See [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md).

## Idea-to-build: outcome before architecture

A greenfield user may describe a vision together with technologies they have heard about:

```text
“Build it with agents, MCP, RAG, memory, a vector database and graph orchestration.”
```

AAOP does not automatically turn those nouns into architecture requirements. Classify each as a **hard constraint**, **preference**, or **solution hypothesis**.

Then find:

1. one actor;
2. one real situation;
3. one observable improvement;
4. the riskiest assumption worth testing now;
5. the smallest end-to-end slice that can produce evidence;
6. only then, the minimum reversible technical shape.

A large future vision is direction, not first-slice scope. The first slice must **buy learning**; scaffolding, diagrams, a large generated codebase, or a polished demo that tests no material assumption is activity, not product evidence.

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

The current baseline covers all six routes, including:

- repository authority/freshness;
- stale bug reports;
- stale PR salvage;
- operational blockers;
- broad-vision overbuild;
- solution-vocabulary capture;
- decision-oriented review.

Every case binds to Route `pressure_guards`; CI prevents those learned invariants from disappearing silently.

```bash
python scripts/validate_pressure.py
```

See [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md).

## Evidence authority and freshness

For messy or long-running projects, a file inventory is not enough. Material claims should be evaluated by the project's own authority/freshness model.

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

Examples of bad escalation:

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

A correct result may be: preserve unknown state, stop safely, and state the smallest legitimate unblock.

## Recipe-driven environment resolution

Before concluding that a route lacks capability, AAOP inspects what already exists.

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/doctor.py . --route bug-fix --json
```

The Doctor reads provider-specific detection hints from Integration Recipes rather than maintaining a separate provider catalog.

**Detection means presence, not recommendation, trust, configuration correctness, authorization, or task fitness.**

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

### Provider Adoption Review

Recipes may carry scoped adoption review debt when a real adoption decision uncovers a provider-specific concern that future use should re-check.

AAOP stores the date, scope, reason, observations, evidence sources, and required re-checks. It does **not** store permanent labels such as `SAFE`, `UNSAFE`, `APPROVED`, or `BANNED`.

When a selected surface matches the recorded scope, AAOP re-checks current upstream source/status and the actual deployment/permission/network context before consequential adoption.

If the concern is fixed upstream or irrelevant to the selected surface, it should not block adoption. If it remains relevant and cannot be mitigated, narrow/isolate the provider, choose another provider, or defer adoption.

This is **remembered review debt**, not a vulnerability database or provider certification system.

## Safe lifecycle: install, upgrade, inspect, remove

AAOP should not become easy to try but risky to keep current—or difficult to leave.

```bash
# initial install
python scripts/install.py /path/to/project

# state-preserving upgrade
python scripts/install.py /path/to/project --upgrade

# read-only local integrity/drift check
python /path/to/project/.aaop/tools/health.py /path/to/project

# manifest-scoped safe removal
python scripts/install.py /path/to/project --uninstall
```

The lifecycle keeps AAOP-owned state separate from project-owned state:

```text
AAOP-managed protocol files        → upgrade/remove by manifest ownership
.aaop/runtime/                     → preserved
project-only files inside .aaop/   → preserved
AGENTS/CLAUDE text outside markers → preserved
AAOP text inside markers           → update/remove only inside marker boundary
third-party providers              → untouched
```

An install manifest records hashes for AAOP-managed files and canonical bootstrap blocks. Locally modified managed files are backed up before canonical replacement/removal. Modified bootstrap blocks are also preserved before uninstall.

Malformed or duplicated bootstrap markers fail preflight **before package mutation/removal**.

`--force` remains a backward-compatible alias for `--upgrade`; it no longer replaces the whole `.aaop` directory.

Legacy installations without a manifest can be safely upgraded, but automatic uninstall refuses to guess ownership. Upgrade first to establish explicit ownership, then uninstall.

Safe AAOP removal does **not** remove Playwright, MCP servers, AutoAgent, Deep Agents, project dependencies, or other provider resources.

See [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Installation health: observe drift before repair

```bash
python .aaop/tools/health.py .
python .aaop/tools/health.py . --json
```

Health answers one narrow question:

> **Does the current local AAOP installation still match the baseline that was installed/upgraded here?**

Typical states:

```text
healthy
upgrade-recommended
legacy-install
drifted
incomplete
invalid-manifest
unsupported-manifest
```

A `drifted` result is evidence to review, not permission to overwrite. When canonical repair is intended, run `--upgrade` from a trusted AAOP source; locally modified managed files are backed up first.

Important boundary: health is **best-effort accidental-drift detection**, not a cryptographic/adversarial trust root, and it does not claim the package is the latest upstream version.

## What AAOP owns

- natural-language developer intake and routing;
- host-native bootstrap conformance and duplicate-context minimization;
- Route Capability Packs and real-project Pressure Guards;
- greenfield outcome/solution-hypothesis discipline;
- decision-oriented read-only review discipline;
- evidence authority/freshness discipline;
- recipe-driven environment/provider presence inventory;
- blocker classification;
- progressive provider selection and least privilege;
- scoped provider-adoption review debt and re-verification policy;
- manifest-scoped install/upgrade/uninstall semantics with low lock-in;
- read-only AAOP installation health and accidental-drift visibility;
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

The installer adds the `.aaop` package plus host-native marked bootstrap blocks without replacing unrelated project rules. It installs no third-party runtime/MCP/provider and requests no secret.

Then open the project in the AI host you already use and describe what you want in ordinary language. No AAOP host-mode selection is required.

## Repository map

```text
AGENTS.md                            # common cross-host bootstrap in source repo
CLAUDE.md                            # thin Claude-specific source bridge
.aaop/
├── VERSION
├── ORCHESTRATOR.md                  # canonical orchestration policy
├── policies/
├── registries/
├── routes/                          # route capability packs + pressure guards
├── recipes/                         # lazy integration/detection + adoption review debt
├── schemas/
├── skills/
└── tools/
    ├── doctor.py                    # project/provider environment evidence
    ├── health.py                    # installed AAOP drift/health evidence
    ├── route.py
    └── recipe.py

adapters/
├── codex.md
├── claude-code.md
└── cursor.md

tests/pressure/
scripts/install.py
scripts/validate.py
scripts/validate_pressure.py
scripts/validate_host_bootstrap.py
docs/HOST_BOOTSTRAP_CONFORMANCE.md
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. Use host-native instruction discovery; do not make the user activate AAOP manually.
4. Keep one canonical policy and minimize duplicate persistent host context.
5. For ideas: outcome and evidence-bearing first slice before architecture.
6. Treat early solution vocabulary as hypothesis unless established as a constraint.
7. For reviews: decision before coverage; current evidence before conclusion; no mutation by default.
8. Current baseline and source authority before trusting stale artifacts.
9. Route by observable outcome, not developer jargon.
10. Route Packs are thin engineering maps, not proprietary workflows.
11. Detect/reuse existing capability before concluding there is a gap.
12. Classify blockers before provider escalation.
13. Install nothing new without a proven technical capability gap.
14. Re-check applicable provider adoption debt before consequential use; never turn it into a permanent label.
15. Upgrade AAOP-owned files without deleting runtime or project-owned state.
16. Observe AAOP installation drift before repairing it; never treat health evidence as authorization to overwrite.
17. Remove only what AAOP can prove it owns; preserve runtime, project-owned state, and provider independence.
18. Prefer mature upstream implementations over copies.
19. Select the minimum provider surface.
20. Verify outcomes; do not fabricate completion when safely blocked.
21. Let real-project regressions improve the protocol before adding theoretical completeness.
22. Hide orchestration complexity without lowering engineering rigor.

## Status

**v0.13.0 — host-native bootstrap conformance and duplicate-context minimization.**

v0.13 verifies the current Codex, Claude Code, and Cursor project-instruction surfaces; uses `AGENTS.md` as the common bridge; reduces `CLAUDE.md` to a thin host-specific bridge because Cursor CLI reads both root files; adds first-party-source/date-backed adapters and static host-bootstrap conformance validation; and still generates no Cursor-specific rule layer or AAOP host plugin by default.

This is an activation/portability release. It adds no new Route, Provider, runtime, package registry, remote updater, or proprietary host extension.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
