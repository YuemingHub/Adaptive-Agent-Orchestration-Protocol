# Ecosystem Map: Integrate, Do Not Reimplement

Verified: 2026-08-08

AAOP sits above existing agent standards, runtimes, discovery systems, and workspaces. Its role is to decide **what is needed now**, select the smallest sufficient provider set, constrain permissions, and verify the result.

## Boundary

AAOP owns:

- project and environment discovery policy;
- outcome and constraint resolution;
- capability-first planning;
- progressive integration decisions;
- least-privilege / autonomy policy;
- provider selection criteria;
- evidence and verification contracts;
- replanning rules;
- graceful degradation across hosts.

AAOP does **not** own:

- a new agent runtime;
- a new MCP protocol or registry;
- a new Skill format;
- a new agent-to-agent protocol;
- a global capability registry;
- a new multi-agent workflow engine;
- a new organizational agent workspace.

## Standards layer

### Agent Skills

Upstream: https://agentskills.io/

Use for reusable procedural knowledge. AAOP's canonical skills follow the `SKILL.md` format and should remain compatible with the open specification.

### MCP

Upstream: https://modelcontextprotocol.io/

Use for external tool/service access. Prefer already-connected MCP servers, first-party integrations, and the Official MCP Registry before community sources.

Official registry: https://registry.modelcontextprotocol.io/

### A2A

Upstream: https://a2a-protocol.org/

Use when independent agent systems need interoperable discovery, task exchange, and communication. AAOP should reference A2A Agent Cards rather than inventing a competing public agent identity format.

### ARD — Agentic Resource Discovery

Upstream: https://agenticresourcediscovery.org/
Repository: https://github.com/ards-project/ard-spec

ARD is a federated discovery standard for agentic resources including MCP servers, A2A Agent Cards, Skills, APIs, and other callable services. AAOP should use ARD-compatible discovery when broad resource search is needed rather than maintaining a private global catalog.

GitHub Agent Finder is an ARD implementation and demonstrates the desired separation: discovery finds ranked candidates but does not silently install them.

## Runtime / execution providers

### Host-native AI IDE runtimes

Examples: Codex, Claude Code, Cursor and other agentic IDEs.

**AAOP preference:** use these first when they already satisfy the task. They are Level 0/1 dependencies because the developer is already there.

### Deep Agents

Upstream: https://github.com/langchain-ai/deepagents
Docs: https://docs.langchain.com/oss/python/deepagents/overview

Useful when a dedicated harness is justified by long-horizon planning, subagent context isolation, Skills, persistence, MCP-heavy execution, or agent filesystem patterns.

AAOP should consume it as a runtime provider, not reproduce its harness.

### Microsoft Agent Framework

Upstream docs: https://learn.microsoft.com/en-us/agent-framework/

Useful for production agent applications requiring explicit sessions, memory/persistence, workflows, orchestration patterns, and hosting.

AAOP should map execution plans to it when its typed workflow/runtime model materially improves the project.

### CAMEL / Workforce

Upstream: https://github.com/camel-ai/camel

Useful when dynamic workforce composition or established multi-agent society patterns fit the task.

AAOP should treat CAMEL as an optional execution provider rather than implement its own workforce engine.

### AutoAgent

Upstream: https://github.com/HKUDS/AutoAgent

AutoAgent can generate and test tools, agents, and workflows from natural-language requirements. This overlaps strongly with any hypothetical AAOP “agent/tool/workflow generator.”

**Decision:** AAOP must not build a competing generator. When self-generation is genuinely useful, AutoAgent is a candidate provider subject to project fit and dependency/security review.

## Workspace / governance providers

### AgentSpace

Upstream: https://github.com/HKUDS/AgentSpace

AgentSpace is an agent-native workspace with persistent tasks, shared agents, permissions, approvals, audit history, scheduling, knowledge, and AgentRouter runtime normalization across multiple provider CLIs.

This overlaps with any hypothetical AAOP team workspace, permissions dashboard, task queue, or cross-runtime execution control plane.

**Decision:** AAOP should not build those product surfaces. For teams that need them, integrate with or deploy a mature workspace provider such as AgentSpace.

## Optimization / architecture search

Frameworks and research systems such as AFlow and AgentSquare explore automated workflow/agent architecture search.

AAOP should not make optimization search part of the baseline. It may delegate to such systems when the cost of repeated workflow optimization is justified by a measurable workload.

## The AAOP integration stack

```text
User outcome + current project
            │
            ▼
┌───────────────────────────────┐
│ AAOP Decision / Policy Plane  │
│ discover → decide → constrain │
│ compose → verify → replan     │
└───────────────┬───────────────┘
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
  Standards   Discovery  Runtime/Workspace
     │          │          │
Skills/MCP   ARD/A2A    Host-native
                         Deep Agents
                         MS Agent Framework
                         CAMEL
                         AutoAgent
                         AgentSpace
```

## Provider selection principle

Never ask “Which framework is best?” in the abstract.

Ask:

1. What capability is missing from the current project/host?
2. Is the gap temporary or recurring?
3. Can an open standard surface satisfy it without adding a runtime?
4. Which mature provider adds the smallest operational surface?
5. What permissions, credentials, infrastructure, and lock-in does it introduce?
6. What evidence will prove the provider actually improved the outcome?

The answer may be **no additional provider**.
