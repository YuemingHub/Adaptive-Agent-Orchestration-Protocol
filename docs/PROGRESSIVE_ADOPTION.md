# Progressive Adoption: Add Capability Only When the Work Demands It

AAOP is not a distribution that asks developers to install every agent framework, MCP server, skill collection, and workspace up front.

The default is the opposite:

> **Start with the host the developer already uses. Add exactly one new layer only when evidence shows the current layer cannot satisfy the outcome well enough.**

This document defines the progressive-adoption model used by AAOP.

## The ladder

The levels are a diagnostic model, not a mandatory sequence. A project may skip levels or use capabilities from more than one level.

### Level 0 — Protocol only

**What exists:** `AGENTS.md` / `CLAUDE.md` + `.aaop/ORCHESTRATOR.md`.

**External installs:** none.

Use when the existing AI host already has enough file, shell, web, Git, and reasoning capability for the task.

This should be the default for small and medium tasks.

### Level 1 — Host-native orchestration

Use the AI IDE or coding agent's own primitives first:

- native tools;
- native subagents/workers;
- project instructions;
- native approvals and sandbox;
- native task/background execution.

**Upgrade trigger:** the host lacks a repeatable procedure, an external capability, discovery, durable execution continuity, specialized runtime property, or governance needed by the project.

### Level 2 — Standard capability extensions

Add only the missing capability using open interfaces:

- **Agent Skills** for repeatable procedural knowledge;
- **MCP** for external tools/services;
- repository scripts/libraries when they are simpler than an MCP server.

Do not add a runtime merely because a Skill or MCP is needed.

**Upgrade trigger:** the system repeatedly does not know which resource to use, or the task needs agent-to-agent interoperability or a more durable runtime/control surface.

### Level 3 — Discovery and interoperability

Use standards instead of private registries where possible:

- **ARD (Agentic Resource Discovery)** to discover MCP servers, A2A agents, Skills, APIs, and other resources from catalogs;
- **A2A** when independent agent systems need to discover and communicate with one another;
- the **Official MCP Registry** for MCP server metadata and installation information.

Discovery does not imply installation. Discovery returns candidates; AAOP still applies provenance, permission, cost, and least-privilege policy before selection.

**Upgrade trigger:** the current host cannot reliably execute or continue the needed long-running/multi-agent pattern, or the user needs organizational governance.

### Level 4 — Specialized runtime or execution control

Select one specialized runtime/control surface only for a concrete, proven capability gap.

Examples:

- **LoopX** when the current agent can perform the engineering work but durable cross-turn/session execution control is missing: todo/evidence/gates, `should-run`, wait/quiet behavior, scheduler/monitor hints, restart and handoff;
- **Deep Agents** when the agent runtime itself needs stronger long-horizon execution, context isolation, persistence, filesystem, Skills, subagents, or MCP-heavy mechanics;
- **agency-orchestrator** when a justified AAOP Task Pod specifically needs bounded multi-role DAG/resume execution beyond the current host;
- **Microsoft Agent Framework** when typed production workflows, sessions, hosting, and explicit orchestration patterns are a better fit;
- **CAMEL Workforce** when dynamic worker composition is useful;
- **AutoAgent** when the task specifically benefits from natural-language generation/testing of new tools, agents, or workflows.

AAOP does not reimplement these runtimes/control planes. It selects and constrains them.

Do not treat the words “long-running” or “multi-agent” as sufficient selection evidence. First classify the missing mechanism:

```text
Agent can do the work, but continuation/control is unreliable
→ execution-continuity gap
→ LoopX-style provider

Agent runtime itself cannot reliably do the long-horizon work
→ runtime gap
→ Deep Agents-style provider

A justified Task Pod needs explicit multi-role DAG/resume execution
→ team-execution gap
→ agency-orchestrator-style delegated runtime

Multiple humans/runtimes need shared audit/approval/permissions/ownership
→ organizational-governance gap
→ Level 5 workspace/control plane
```

Do not install multiple Level-4 providers merely because their feature lists overlap. Pick the smallest primary mechanism that closes the proven gap and verify that gap before adding anything else.

**Upgrade trigger:** multiple people/agents/runtimes must share persistent work, approvals, permissions, audit history, and ownership beyond a bounded project-local execution loop.

### Level 5 — Governed workspace

Use a workspace/control plane such as **AgentSpace** when the problem is no longer merely agent execution, but organizational coordination:

- persistent task queues;
- shared agents and knowledge;
- approvals;
- permission boundaries;
- audit trails;
- schedules;
- runtime routing across multiple provider CLIs.

Do not deploy an organizational workspace for a solo task that a local AI IDE can complete safely.

## Upgrade decision rule

Move upward only when all three are true:

1. **Observed gap** — the current layer demonstrably lacks a capability or reliability property the outcome requires.
2. **Material benefit** — adding the layer improves success probability, safety, maintainability, or human effort enough to justify its complexity.
3. **Bounded cost** — installation, credentials, permissions, operational burden, and lock-in are understood and acceptable.

If any condition is false, stay at the current layer.

For control-plane/runtime escalation, add a fourth question:

4. **Primary mechanism match** — does the selected provider primarily solve the proven gap, or are we installing a neighboring orchestration product because its marketing vocabulary sounds similar?

If the mechanism does not match, do not install it.

## Downgrade rule

AAOP must also remove unnecessary machinery.

Downgrade when:

- a temporary MCP/runtime/control-plane provider is no longer needed;
- a workflow can be replaced by a simpler native host path;
- an experiment becomes a stable local Skill or script;
- organizational governance is not required for a local project;
- duplicate providers exist for the same capability;
- a provider was adopted for a gap that current host capabilities now satisfy natively.

The target state is not maximum capability. It is the **minimum sufficient integration surface**.

For LoopX specifically, disabling/removing it must not destroy AAOP Working Contract/Journey authority. AAOP continuity remains recoverable from AAOP/project state plus accepted evidence references; LoopX owns only the selected bounded execution-control state.

## Typical developer experience

A developer should be able to begin with:

```text
1. Add AAOP to the repository.
2. Open the repository in the AI tool they already use.
3. State the outcome.
4. Let AAOP inspect existing capabilities.
5. Continue with no new installation when possible.
6. If a capability gap appears, receive one recommended next integration with the reason and permission/cost implications.
```

For a long-running task, the user should not be asked to choose between LoopX, Deep Agents, or another runtime by brand. AAOP should identify the missing capability class first and recommend the smallest matching surface.

## Anti-patterns

AAOP should reject these patterns by default:

- install five frameworks “for completeness”;
- preload every Skill or MCP into context;
- create a permanent multi-agent team before project discovery;
- replace a working host-native feature with an AAOP implementation;
- maintain a private copy of a standard registry;
- turn optional integrations into hard dependencies;
- introduce Docker/databases/control planes for tasks that need only repository-local execution;
- install LoopX merely because the task is long even though host-native continuation is already sufficient;
- stack LoopX and another long-horizon runtime before proving which missing mechanism each one closes;
- allow an external execution-control provider to become a second source of truth for AAOP Working Contract, Route/Journey, authorization, or release completion.

## Principle

> **AAOP is progressively enhanced, not comprehensively installed.**
