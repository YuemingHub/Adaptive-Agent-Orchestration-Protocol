# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic orchestration protocol for turning a user goal into the **smallest sufficient agent system**.

Instead of hard-coding a permanent team of agents, AAOP makes an AI host do this at runtime:

```text
User Goal
   ↓
Environment + Project Discovery
   ↓
Outcome / Constraint Resolution
   ↓
Required Capability Graph
   ↓
Capability Matching + Gap Resolution
   ↓
Dynamic Main Agent + Subagents + Skills + Tools/MCP
   ↓
Dependency-Aware Execution
   ↓
Independent Verification
   ↓
Replan / Reconfigure if needed
   ↓
Evidence-backed Delivery
```

## Why AAOP exists

Users should not need to know in advance which agent, Skill, MCP server, model, or workflow is required. They should be able to state the outcome they want. The orchestration layer should discover the project, determine the capabilities required, reuse what already exists, ask only for genuinely necessary external authorization, and then execute with verification.

AAOP deliberately separates four concepts:

- **Agent** — who owns a responsibility.
- **Skill** — how a repeatable task should be performed.
- **Tool / MCP** — what external resource or action is actually available.
- **Policy** — what may be done autonomously and what requires authorization.

## Quick start

### Codex / agents that read `AGENTS.md`

Clone this repository into a project, or copy the AAOP package into your project root. Then tell the agent what outcome you want. `AGENTS.md` bootstraps `.aaop/ORCHESTRATOR.md`.

### Claude Code

`CLAUDE.md` provides the bootstrap. The canonical skills in `.aaop/skills/` follow the open Agent Skills `SKILL.md` structure; see `adapters/claude-code.md` for native project-skill installation.

### Cursor

Cursor can read root `AGENTS.md` and `CLAUDE.md`. See `adapters/cursor.md` for optional `.cursor/rules` and MCP integration.

### Any other AI IDE / agent host

Load `AGENTS.md`, then `.aaop/ORCHESTRATOR.md`. If native subagents do not exist, AAOP requires graceful degradation to isolated task roles rather than failure.

## Repository map

```text
AGENTS.md                         # universal bootstrap
CLAUDE.md                         # Claude-compatible bootstrap
.aaop/ORCHESTRATOR.md            # normative runtime protocol
.aaop/policies/                  # autonomy + MCP/tool policy
.aaop/registries/                # capability vocabulary and resolver hints
.aaop/schemas/                   # machine-readable runtime artifacts
.aaop/skills/*/SKILL.md          # reusable orchestration skills
adapters/                        # host-specific mappings
examples/                        # worked orchestration examples
scripts/validate.py              # zero-dependency structural validator
.github/workflows/validate.yml   # CI validation
```

## Runtime artifacts

AAOP expects a host to create ephemeral or project-local runtime state under `.aaop/runtime/` when useful:

- `environment-profile.json`
- `project-profile.json`
- `capability-matrix.json`
- `team-plan.json`
- `execution-plan.json`
- `state.json`

These are **derived working state**, not universal truth. A host may keep them in memory instead. Do not commit secrets.

## Design principles

1. Understand the project before changing it.
2. Derive capabilities before inventing roles.
3. Use the minimum sufficient team.
4. Prefer existing native tools and Skills before adding MCP.
5. Treat external capability installation as a supply-chain and permission decision.
6. Ask the user only when a real decision, credential, cost, permission, or irreversible action requires them.
7. Verify outcomes, not activity.
8. Replan when evidence disproves the current plan.
9. Degrade cleanly when a host lacks multi-agent features.
10. Optimize for user intent preservation, reliability, and low unnecessary human intervention.

## Standards alignment

AAOP Skills use the open Agent Skills `SKILL.md` pattern (name + description frontmatter and progressively loaded instructions). MCP discovery policy prefers already-connected tools, official providers, and the Official MCP Registry before untrusted community sources.

Host adapters are intentionally advisory: host capabilities and configuration formats evolve faster than the core protocol. The core protocol remains stable while adapters can change independently.

## Status

**v0.1.0 — executable protocol baseline.**

This version defines the orchestration contract, core skills, runtime schemas, host adapters, examples, and validation workflow. It does not attempt to build a standalone orchestration engine yet; AI IDEs can execute the protocol directly from Markdown today.

## License

Apache-2.0. See `LICENSE`.
