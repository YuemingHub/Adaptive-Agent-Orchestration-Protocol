# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, decision, policy, and integration layer**.

Its purpose is simple:

> A developer should be able to arrive with an idea, a messy repository, a bug, a feature request, a review question, or a deployment problem — describe it in ordinary language — and let AAOP route the work without first learning the agent ecosystem.

AAOP does not try to become another all-in-one agent framework.

```text
Natural-language developer request
              ↓
What do they have right now?
idea / repo / files / runtime
              ↓
What situation are they in?
idea / recovery / bug / feature / review / operations
              ↓
What should observably become true?
              ↓
Route-specific discovery
              ↓
Required capabilities
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
                │ Skill / MCP / ARD / A2A
                │ Runtime / Workspace
                ↓
        Execute → Verify → Replan
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

The user does **not** choose a workflow, Agent, Skill, MCP server, or runtime.

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

The internal intake object is defined by `.aaop/schemas/intake-envelope.schema.json`; the user never fills it out.

## Why AAOP exists

The agent ecosystem is capable but fragmented. Developers may encounter Agent Skills, MCP, A2A, ARD, AutoAgent, Deep Agents, Microsoft Agent Framework, CAMEL, AgentSpace, and many other systems — each solving a real layer of the problem.

The answer should not be to reinstall or reimplement all of them in every project.

AAOP's job is:

> **Understand the developer's actual situation first, then reuse the current environment and integrate only the mature capability that becomes necessary.**

## Progressive adoption

AAOP defaults to **zero third-party provider installation**.

```text
Level 0  AAOP protocol only
Level 1  Existing AI IDE / host-native capabilities
Level 2  Agent Skills / MCP / local scripts
Level 3  ARD / A2A / trusted discovery
Level 4  One justified specialized runtime
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
python .aaop/tools/recipe.py show deepagents
```

Current recipes include Agent Skills, MCP, ARD, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace.

## What AAOP owns

- natural-language developer intake and internal routing;
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
| MCP discovery metadata | Official MCP Registry |
| Cross-agent interoperability | A2A |
| Broad agentic resource discovery | ARD |
| Long-horizon/subagent harness | Deep Agents or another justified runtime |
| Production workflow runtime | Microsoft Agent Framework or another justified runtime |
| Dynamic workforce patterns | CAMEL or another justified runtime |
| Generate/test new agents/tools/workflows | AutoAgent when justified |
| Shared agents, permissions, approvals, audit, routing | AgentSpace or another mature control plane |

See [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md).

## Quick start

Install AAOP into an existing project:

```bash
python scripts/install.py /path/to/project
```

The installer:

- copies the `.aaop` protocol package;
- appends a compact bootstrap to existing `AGENTS.md` / `CLAUDE.md` without replacing project rules;
- installs **no** third-party runtime, MCP server, or Skill marketplace;
- requests **no** secret.

Optional inventory:

```bash
python .aaop/tools/doctor.py .
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
│   ├── routes.json                  # developer situation → primary route
│   ├── capabilities.json
│   ├── providers.json
│   └── adoption-profiles.json
├── recipes/
├── schemas/
│   ├── intake-envelope.schema.json  # internal intake state
│   └── ...
├── skills/
│   ├── developer-intake/            # natural-language front door
│   ├── project-discovery/
│   ├── capability-planning/
│   ├── provider-selection/
│   ├── team-construction/
│   ├── tool-resolution/
│   └── verification-loop/
└── tools/
    ├── doctor.py
    └── recipe.py

docs/DEVELOPER_ENTRYPOINT.md
adapters/
examples/
scripts/
```

## Core design principles

1. Situation before machinery.
2. Read available evidence before asking the user.
3. Route by the next observable outcome, not by developer jargon.
4. Derive capabilities before inventing roles.
5. Start with what the developer already has.
6. Install nothing new without a proven capability gap.
7. Prefer open standards and mature upstream implementations over copies.
8. Use the minimum sufficient team and integration surface.
9. Discovery never equals silent installation.
10. Verify outcomes; correct the route/plan when evidence changes the situation.
11. Hide orchestration complexity from the user without lowering engineering rigor.

## Status

**v0.4.0 — developer intake and natural-language routing baseline.**

v0.4 makes the developer's real situation the first-class entry point. AAOP now routes ideas, repository recovery, bugs, features, reviews, and release/operations work before capability/provider orchestration.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
