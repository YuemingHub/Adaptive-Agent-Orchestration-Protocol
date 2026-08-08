# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, decision, policy, and integration layer**.

Its purpose is simple:

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or a deployment problem — describe it in ordinary language — and let AAOP route and compose the work without first learning the agent ecosystem.

AAOP does not try to become another all-in-one agent framework.

```text
Natural-language developer request
              ↓
Developer intake
              ↓
Primary development route
              ↓
Route Capability Pack
              ↓
Environment inventory: what already exists?
              ↓
What capabilities are still needed now?
              ↓
Reuse what already exists
              ↓
┌────────────────────────────────────┐
│ Is there a proven capability gap?  │
└───────────────┬────────────────────┘
        no      │       yes
        ↓       │        ↓
   keep it      │   select one mature
   simple       │   provider + recipe
                │        ↓
                │ upstream implementation
                ↓
        Execute → Verify → Re-route/Replan
```

## The developer front door

AAOP accepts minimal language such as:

```text
“I have an idea but don't know how to build it.”
“This repo is a mess. Understand it and continue.”
“Login returns 500. Fix it.”
“Add family invitations.”
“Review this before I merge.”
“Get this ready to deploy.”
```

The user does **not** choose a workflow, Agent, Skill, MCP server, runtime, or framework.

AAOP first routes internally to one primary development path:

| Situation | Internal route | First correct move |
| --- | --- | --- |
| idea / no trustworthy implementation yet | `idea-to-build` | understand outcome and smallest buildable slice before architecture |
| messy, abandoned, unfamiliar, contradictory repo | `repo-recovery` | establish trustworthy current state before broad edits |
| observed failure / error / regression | `bug-fix` | reproduce/evidence → root cause → narrow fix → regression check |
| new or changed behavior | `feature-change` | behavior contract → existing path → smallest coherent change |
| explanation / review / audit / assessment | `understand-review` | inspect for the decision the review must support; no mutation by default |
| deploy / migration / CI / production / incident | `release-operations` | environment evidence + rollback + authorization before consequential writes |

See [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md).

### Read before asking

If the workspace, repository, logs, tests, issue, or deployment evidence can answer a question, AAOP should inspect it rather than asking the user to restate it.

When clarification is genuinely necessary, ask **one concrete question** only when the answer can materially change the route, observable outcome, product choice, or safety/permission class.

## Route Capability Packs

Once a route is selected, AAOP loads exactly one internal Route Capability Pack from `.aaop/routes/`.

A pack describes:

- the route's engineering stages and purpose;
- normally required capabilities;
- the evidence that should move the work forward;
- stage exit conditions;
- specific capability gaps that may justify escalation;
- mature provider candidates for those gaps;
- route-level verification;
- signals that mean evidence has changed the situation and the route should change.

A Route Capability Pack is **not** a workflow engine or install bundle. The same pack must still describe sound engineering if every external provider disappeared tomorrow.

Browse the installed packs:

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show bug-fix
```

See [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md).

## Recipe-driven environment resolution

Before AAOP concludes that a route is missing a capability, it should first inspect what the developer already has.

`.aaop/tools/doctor.py` now reads provider `detect` hints directly from Integration Recipes instead of maintaining a second hard-coded provider list.

It can inventory:

- visible Codex / Claude Code / Cursor host commands;
- basic toolchain commands such as Git, Python, Node, package managers and Docker;
- project manifests, test signals, CI and deployment signals;
- Skill and MCP configuration surfaces;
- provider-specific command/file/Python-package/Node-package evidence;
- provider presence relevant to one current Route Capability Pack.

Examples:

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/doctor.py . --route bug-fix --json
```

The output answers **“what appears to be present?”**, not **“what should we use?”**

A detected provider may be irrelevant, misconfigured, under-permissioned, or unsafe for the current route. A provider that is not detected may still be unnecessary. Route capability matching and provider-selection policy remain authoritative.

Recipe detection hints are intentionally narrow. Generic manifests such as `package.json`, `pyproject.toml`, or `requirements.txt` cannot by themselves prove a specific provider exists.

## Why AAOP exists

The agent ecosystem is capable but fragmented. Developers may encounter Agent Skills, MCP, A2A, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, AutoAgent, Deep Agents, Microsoft Agent Framework, CAMEL, AgentSpace, and many other systems — each solving a real layer of the problem.

The answer should not be to reinstall or reimplement all of them in every project.

AAOP's job is:

> **Understand the developer's actual situation first, inventory existing capability, derive what the route still needs, then integrate only the mature capability that is actually missing.**

## Progressive adoption

AAOP defaults to **zero third-party provider installation**.

```text
Level 0  AAOP protocol only
Level 1  Existing AI IDE / host-native capabilities
Level 2  Existing/local Skills, tests, scripts, tools, MCP
Level 3  ARD / A2A / trusted discovery
Level 4  One justified specialized runtime/harness
Level 5  Governed workspace/control plane
```

These are not mandatory cumulative layers. A project may stay at Level 0/1 indefinitely.

See [`docs/PROGRESSIVE_ADOPTION.md`](docs/PROGRESSIVE_ADOPTION.md).

## Integration Recipes: one integration shape, upstream implementation

AAOP does not build a new package manager. It carries **lazy Integration Recipes** for selected mature providers.

A recipe normalizes:

- when the provider is appropriate / inappropriate;
- how to detect whether it is already present;
- the smallest known upstream install/configuration path;
- credentials and permissions;
- verification of the original capability gap;
- rollback/removal;
- upstream source of truth and last-verified date.

Browse recipes without installing anything:

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show spec-kit
python .aaop/tools/recipe.py show playwright
```

Current recipes include Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace.

### Examples of progressive provider use

- **Spec Kit** — use when durable intent/specification artifacts or a reviewed route-relevant extension actually reduce drift; do not duplicate its SDD/extension/bundle machinery inside AAOP.
- **Playwright** — choose the smallest surface: Test for durable E2E, CLI+Skills for many coding-agent browser workflows, MCP for persistent introspective browser loops.
- **mini-SWE-agent** — use for a bounded, reproducible, testable software issue when a dedicated minimal SWE loop is useful; not for ambiguous product discovery or repository recovery.
- **OpenHands** — use when a dedicated autonomous coding runtime/SDK or isolated workspace is the missing capability; not simply because the task involves code.

## What AAOP owns

- natural-language developer intake and internal routing;
- Route Capability Packs;
- recipe-driven environment/provider presence inventory;
- project/environment discovery policy;
- outcome and constraint resolution;
- capability-first planning;
- progressive integration decisions;
- provider selection and least-privilege policy;
- normalized integration recipes;
- dynamic ownership/team decisions;
- verification, replanning, and route-correction contracts;
- graceful degradation across hosts.

## What AAOP deliberately does not rebuild

| Need | Prefer mature ecosystem layer |
| --- | --- |
| Reusable procedures | Agent Skills |
| External tool/service access | MCP |
| Cross-agent interoperability | A2A |
| Broad agentic resource discovery | ARD |
| Structured spec-driven SDLC | GitHub Spec Kit when justified |
| Browser E2E / agent browser automation | Playwright surface appropriate to the task |
| Bounded issue-solving SWE agent | mini-SWE-agent when justified |
| General autonomous coding runtime/SDK | OpenHands when justified |
| Long-horizon/subagent harness | Deep Agents or another justified runtime |
| Production workflow runtime | Microsoft Agent Framework or another justified runtime |
| Dynamic workforce patterns | CAMEL or another justified runtime |
| Generate/test new agents/tools/workflows | AutoAgent when justified |
| Shared agents, permissions, approvals, audit, routing | AgentSpace or another mature control plane |

See [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md) and [`docs/RESEARCH_V0_5.md`](docs/RESEARCH_V0_5.md).

## Quick start

Install AAOP into an existing project:

```bash
python scripts/install.py /path/to/project
```

The installer:

- copies the `.aaop` protocol package;
- appends a compact bootstrap to existing `AGENTS.md` / `CLAUDE.md` without replacing project rules;
- installs **no** third-party runtime, MCP server, Skill marketplace, or route provider;
- requests **no** secret.

Optional inventory/browsing:

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/route.py list
python .aaop/tools/recipe.py list
```

Then open the project in the AI host you already use and say what you want in ordinary language.

## Repository map

```text
AGENTS.md
CLAUDE.md
.aaop/
├── ORCHESTRATOR.md
├── policies/
├── registries/
│   ├── routes.json
│   ├── capabilities.json
│   ├── providers.json
│   └── adoption-profiles.json
├── routes/                          # route capability packs
├── recipes/                         # lazy integration + detection knowledge
├── schemas/
│   ├── intake-envelope.schema.json
│   ├── route-capability-pack.schema.json
│   ├── environment-inventory.schema.json
│   └── ...
├── skills/
│   ├── developer-intake/
│   ├── route-execution/
│   ├── project-discovery/
│   ├── capability-planning/
│   ├── provider-selection/
│   ├── team-construction/
│   ├── tool-resolution/
│   └── verification-loop/
└── tools/
    ├── doctor.py                    # recipe-driven read-only inventory
    ├── route.py
    └── recipe.py

docs/DEVELOPER_ENTRYPOINT.md
docs/ROUTE_CAPABILITY_PACKS.md
adapters/
examples/
scripts/
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. Route by the next observable outcome, not by developer jargon.
4. Use Route Capability Packs as thin engineering maps, not proprietary workflows.
5. **Detect/reuse existing capability before concluding there is a gap.**
6. Derive capabilities before inventing roles or choosing providers.
7. Install nothing new without a proven capability gap.
8. Prefer mature upstream implementations over copies.
9. Select the minimum provider surface, not the whole ecosystem.
10. Provider detection means presence, not relevance/trust/recommendation.
11. Community catalogs are discovery surfaces, not automatic trust boundaries.
12. Verify outcomes and verify every provider actually closes the gap that justified it.
13. Hide orchestration complexity from the user without lowering engineering rigor.

## Status

**v0.6.0 — recipe-driven environment resolution.**

v0.6 makes AAOP inspect what the developer already has before provider selection. The Doctor now derives provider-presence detection from Integration Recipes, adds project/toolchain signals and route-aware provider context, rejects generic-manifest provider detection, and keeps AAOP's own built-in Skills from inflating the observed integration level.

AAOP still does not install providers from detection results and still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
