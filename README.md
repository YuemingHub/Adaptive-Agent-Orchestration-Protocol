# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **decision and policy layer** for turning a user goal into the **smallest sufficient agent system** using capabilities that already exist whenever possible.

It does not try to become another all-in-one agent framework.

```text
User Goal + Current Project
          ↓
Environment / Project Discovery
          ↓
Required Capabilities
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

## Why AAOP exists

The agent ecosystem is becoming capable but fragmented. Developers may encounter Agent Skills, MCP, A2A, ARD, AutoAgent, Deep Agents, Microsoft Agent Framework, CAMEL, AgentSpace, and many other systems — each solving a real layer of the problem.

The answer should not be to reinstall or reimplement all of them in every project.

AAOP's job is:

> **Start from the developer's current tool, understand the real project, identify the capability gap, then integrate only the mature component that is justified now.**

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

These are not mandatory cumulative layers. A project may stay at Level 0/1 indefinitely or skip directly to a higher layer when the outcome truly requires it.

See [`docs/PROGRESSIVE_ADOPTION.md`](docs/PROGRESSIVE_ADOPTION.md).

## Integration Recipes: one integration shape, upstream implementation

AAOP does not build a new package manager. Instead it carries **lazy Integration Recipes** for selected mature providers.

A recipe normalizes:

- when the provider is appropriate / inappropriate;
- how to detect whether it is already present;
- the smallest known upstream install/configuration path;
- credentials and permissions;
- verification of the original capability gap;
- rollback/removal;
- upstream source of truth and the date the recipe was last verified.

The agent should re-check the upstream source before consequential installation because external projects evolve independently.

Browse the installed recipes without installing anything:

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show deepagents
```

Current recipes include Agent Skills, MCP, ARD, Deep Agents, Microsoft Agent Framework, CAMEL Workforce, AutoAgent, and AgentSpace. Recipes are glue metadata, not endorsements and not automatic installs.

## What AAOP owns

- project/environment discovery policy;
- outcome and constraint resolution;
- capability-first planning;
- progressive integration decisions;
- provider selection and least-privilege policy;
- normalized integration recipes;
- dynamic ownership/team decisions;
- verification and replanning contracts;
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

Inspect the environment and recipes after installation:

```bash
python .aaop/tools/doctor.py .
python .aaop/tools/recipe.py list
```

Then open the project in the AI host you already use and state the desired outcome.

AAOP should attempt to complete the task with the current environment first. If a real capability gap appears, it selects one provider and uses its recipe so the developer does not need to hunt across repositories for setup/verification steps.

## Repository map

```text
AGENTS.md
CLAUDE.md
.aaop/
├── ORCHESTRATOR.md                 # normative decision/policy protocol
├── policies/
│   ├── autonomy.md
│   ├── mcp-and-tools.md
│   └── progressive-integration.md
├── registries/
│   ├── capabilities.json
│   ├── providers.json              # upstream resolver hints, not packages
│   └── adoption-profiles.json
├── recipes/
│   ├── README.md                   # recipe safety/contract
│   └── *.json                      # lazy upstream integration recipes
├── schemas/
│   ├── environment-profile.schema.json
│   ├── project-profile.schema.json
│   ├── capability-matrix.schema.json
│   ├── integration-plan.schema.json
│   ├── integration-recipe.schema.json
│   ├── team-plan.schema.json
│   └── execution-plan.schema.json
├── skills/
│   ├── project-discovery/
│   ├── capability-planning/
│   ├── provider-selection/
│   ├── team-construction/
│   ├── tool-resolution/
│   └── verification-loop/
└── tools/
    ├── doctor.py                    # zero-dependency environment inventory
    └── recipe.py                    # zero-dependency recipe browser

adapters/                            # host-specific guidance
docs/                               # architecture + ecosystem + adoption model
examples/                            # worked orchestration examples
scripts/install.py                  # safe AAOP bootstrap
scripts/validate.py                 # structural/provider/recipe validation
.github/workflows/validate.yml      # clean-environment CI
```

## Standards posture

AAOP uses existing open standards rather than inventing competing formats:

- Agent Skills: https://agentskills.io/
- MCP: https://modelcontextprotocol.io/
- Official MCP Registry: https://registry.modelcontextprotocol.io/
- A2A: https://a2a-protocol.org/
- ARD: https://agenticresourcediscovery.org/

External providers evolve independently. `.aaop/registries/providers.json` and `.aaop/recipes/*.json` are resolver hints, not allowlists, lockfiles, endorsements, or silent installers. Current upstream status and security must be re-verified before consequential use.

## Core design principles

1. Understand the project before changing it.
2. Derive capabilities before inventing roles.
3. Start with what the developer already has.
4. Install nothing new without a proven capability gap.
5. Prefer open standards and mature upstream implementations over copies.
6. Give integrations one normalized recipe shape instead of vendoring their implementations.
7. Use the minimum sufficient team and integration surface.
8. Discovery never equals silent installation.
9. Apply least privilege to external capabilities.
10. Verify that every added provider actually closes the gap it was added for, and remove unnecessary machinery again.

## Status

**v0.3.0 — lazy integration recipe baseline.**

v0.2 established progressive ecosystem integration. v0.3 adds a normalized recipe contract and recipe browser so agents can use upstream mature components without forcing developers to manually collect setup, credential, verification, and rollback instructions from scattered repositories.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
