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

**Upgrade trigger:** the host lacks a repeatable procedure, an external capability, discovery, durable orchestration, or governance needed by the project.

### Level 2 — Standard capability extensions

Add only the missing capability using open interfaces:

- **Agent Skills** for repeatable procedural knowledge;
- **MCP** for external tools/services;
- repository scripts/libraries when they are simpler than an MCP server.

Do not add a runtime merely because a Skill or MCP is needed.

**Upgrade trigger:** the system repeatedly does not know which resource to use, or the task needs agent-to-agent interoperability or a more durable runtime.

### Level 3 — Discovery and interoperability

Use standards instead of private registries where possible:

- **ARD (Agentic Resource Discovery)** to discover MCP servers, A2A agents, Skills, APIs, and other resources from catalogs;
- **A2A** when independent agent systems need to discover and communicate with one another;
- the **Official MCP Registry** for MCP server metadata and installation information.

Discovery does not imply installation. Discovery returns candidates; AAOP still applies provenance, permission, cost, and least-privilege policy before selection.

**Upgrade trigger:** the current host cannot reliably execute the needed long-running/multi-agent pattern, or the user needs organizational governance.

### Level 4 — Specialized runtime

Select a mature runtime only for a concrete reason.

Examples:

- **Deep Agents** when long-horizon execution, context isolation, Skills, subagents, persistence, or MCP-heavy work benefits from a dedicated harness;
- **Microsoft Agent Framework** when typed production workflows, sessions, hosting, and explicit orchestration patterns are a better fit;
- **CAMEL Workforce** when dynamic worker composition is useful;
- **AutoAgent** when the task specifically benefits from natural-language generation/testing of new tools, agents, or workflows.

AAOP does not reimplement these runtimes. It selects and constrains them.

**Upgrade trigger:** multiple people/agents/runtimes must share persistent work, approvals, permissions, audit history, and ownership.

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

## Downgrade rule

AAOP must also remove unnecessary machinery.

Downgrade when:

- a temporary MCP/runtime is no longer needed;
- a workflow can be replaced by a simpler native host path;
- an experiment becomes a stable local Skill or script;
- organizational governance is not required for a local project;
- duplicate providers exist for the same capability.

The target state is not maximum capability. It is the **minimum sufficient integration surface**.

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

The developer should not have to understand the entire agent ecosystem before doing useful work.

## Anti-patterns

AAOP should reject these patterns by default:

- install five frameworks “for completeness”;
- preload every Skill or MCP into context;
- create a permanent multi-agent team before project discovery;
- replace a working host-native feature with an AAOP implementation;
- maintain a private copy of a standard registry;
- turn optional integrations into hard dependencies;
- introduce Docker/databases/control planes for tasks that need only repository-local execution.

## Principle

> **AAOP is progressively enhanced, not comprehensively installed.**
