# Ecosystem Map: Integrate, Do Not Reimplement

Verified: 2026-08-08

AAOP sits above existing developer tools, agent standards, SDLC harnesses, verification tools, runtimes, discovery systems, and workspaces. Its role is to understand **what is needed now**, select the smallest sufficient provider surface, constrain permissions, and verify the result.

## Boundary

AAOP owns:

- natural-language developer intake and route selection;
- Route Capability Packs;
- project/environment discovery policy;
- outcome and constraint resolution;
- capability-first planning;
- progressive integration decisions;
- least-privilege / autonomy policy;
- provider selection criteria;
- normalized Integration Recipes;
- evidence, verification, rerouting, and replanning contracts;
- graceful degradation across hosts.

AAOP does **not** own:

- six replacement software-development workflow engines;
- a new coding-agent runtime;
- a new MCP protocol or registry;
- a new Skill format;
- a new agent-to-agent protocol;
- a global capability registry;
- a new extension/package marketplace;
- a new organizational agent workspace.

## Host / repository layer — default

### Host-native AI development environments

Examples: Codex, Claude Code, Cursor and other agentic development hosts.

**AAOP preference:** use these first when they already satisfy the current Route Capability Pack. The developer should not install another runtime merely because one exists.

### Existing repository capabilities

Before any external provider, inspect and reuse:

- package/build tools;
- unit/integration/E2E tests;
- linters/type checkers/static analyzers;
- local scripts and CLIs;
- CI/CD workflows;
- deployment scripts;
- architecture/specification artifacts already trusted by the project.

A repository's existing capability is usually cheaper and safer than another framework.

## Standards layer

### Agent Skills

Upstream: https://agentskills.io/

Use for reusable procedural knowledge. AAOP's canonical Skills follow the `SKILL.md` format and should remain compatible with the open specification.

### MCP

Upstream: https://modelcontextprotocol.io/
Official registry: https://registry.modelcontextprotocol.io/

Use for external tool/service access only when the host or repository does not already expose the needed capability.

### A2A

Upstream: https://a2a-protocol.org/

Use when independent agent systems need interoperable discovery/task exchange. AAOP references A2A rather than inventing a competing public agent identity or transport format.

### ARD — Agentic Resource Discovery

Upstream: https://agenticresourcediscovery.org/
Repository: https://github.com/ards-project/ard-spec

Use ARD-compatible discovery when the capability is known but the provider is not. Discovery returns candidates; it does not create trust or installation authorization.

## Structured development / SDLC harnesses

### GitHub Spec Kit

Upstream: https://github.com/github/spec-kit
Docs: https://github.github.com/spec-kit/

Spec Kit already provides a broad agent-agnostic specification-driven development workflow and an extension/catalog/bundle model.

AAOP may select it when durable product intent, specification/plan/task artifacts, or an existing supported extension materially improves a route such as `idea-to-build`, `feature-change`, or an already-Spec-Kit-managed bug workflow.

**AAOP must not:**

- recreate Spec Kit's CLI or lifecycle;
- create a second competing specification tree beside a healthy existing one;
- treat every small edit as a reason to initialize Spec Kit;
- trust a community extension merely because it appears in a catalog.

Community extensions/plugins/bundles are separate trust surfaces and require provenance, install-hook, permission, credential/data-egress, and rollback review.

## Verification / browser tool family

### Playwright

Upstream: https://github.com/microsoft/playwright
MCP: https://github.com/microsoft/playwright-mcp

Playwright is modeled as a **capability family**, not as one mandatory MCP server.

Select the smallest surface:

- **Playwright Test** — durable browser E2E/regression evidence;
- **Playwright CLI + Skills** — concise agent-driven browser interaction in coding workflows;
- **Playwright MCP** — persistent/introspective browser-agent loops where continuous page state is valuable.

Do not install all surfaces by default. Existing project Playwright coverage should be reused before adding another interface.

## Software-engineering agent/runtime providers

### mini-SWE-agent

Upstream: https://github.com/SWE-agent/mini-swe-agent

Useful for a bounded, reproducible, testable software issue when a dedicated minimal SWE-agent loop is genuinely preferable to the current host.

**Avoid** using an issue-solving agent as a substitute for:

- ambiguous product discovery;
- repository recovery;
- deciding expected behavior that only the product/user can determine.

### OpenHands

Upstream: https://github.com/OpenHands
SDK: https://github.com/OpenHands/software-agent-sdk
Docs: https://docs.openhands.dev/

Useful when the missing capability is a dedicated autonomous coding environment, a reusable Software Agent SDK, or an isolated/sandboxed workspace.

AAOP should choose the minimum OpenHands surface (CLI, local SDK, or broader workspace/server mode) instead of installing the entire ecosystem.

### Deep Agents

Upstream: https://github.com/langchain-ai/deepagents
Docs: https://docs.langchain.com/oss/python/deepagents/overview

Useful when a dedicated long-horizon harness is justified by persistence, context isolation, Skills/MCP-heavy execution, or filesystem/subagent patterns.

### Microsoft Agent Framework

Upstream docs: https://learn.microsoft.com/en-us/agent-framework/

Useful when a production agent application needs explicit sessions, memory/persistence, typed workflows/orchestration, or hosting. It is not an ordinary application deployment dependency.

### CAMEL / Workforce

Upstream: https://github.com/camel-ai/camel

Useful when dynamic workforce composition or established multi-agent society patterns materially improve execution.

### AutoAgent

Upstream: https://github.com/HKUDS/AutoAgent

AutoAgent can generate/test tools, agents, and workflows from natural-language requirements. This overlaps strongly with any hypothetical AAOP agent/tool/workflow generator.

**Decision:** AAOP does not build a competing generator. AutoAgent is a candidate only when creating/testing new agents/tools/workflows is itself the missing capability.

## Workspace / governance providers

### AgentSpace

Upstream: https://github.com/HKUDS/AgentSpace

Useful when multiple humans/agents/runtimes genuinely need durable shared tasks, permissions, approvals, audit, scheduling, knowledge, and runtime routing.

This is Level 5 infrastructure, not a default dependency for solo/local development.

## Optimization / architecture search

Frameworks and research systems such as AFlow and AgentSquare explore automated workflow/agent architecture search.

AAOP should not make optimization search part of the baseline. Delegate only when repeated workflow optimization has measurable value that justifies the search cost.

## Route-to-provider examples

These are **conditional candidates**, not fixed routing rules.

| Route | Capability gap | Possible mature provider surface |
| --- | --- | --- |
| `idea-to-build` | durable intent/specification lifecycle | Spec Kit core workflow |
| `idea-to-build` / `feature-change` | browser acceptance evidence | existing Playwright Test, then CLI+Skills/MCP only if needed |
| `repo-recovery` | long-horizon isolated coding context | Deep Agents or OpenHands when current host is insufficient |
| `bug-fix` | bounded autonomous issue-solving loop | mini-SWE-agent; OpenHands only if broader runtime is needed |
| `bug-fix` | browser reproduction/regression | Playwright surface matching the evidence need |
| `understand-review` | independent/long-context execution | host-native reviewer first; dedicated runtime only for proven context gap |
| `release-operations` | repeatable browser smoke | Playwright Test |
| `release-operations` | organizational approvals/audit/routing | AgentSpace only when governance is the real requirement |

## Provider selection principle

Never ask “Which framework is best?” in the abstract.

Ask:

1. Which Route Capability Pack stage are we in?
2. What capability is still missing from the current host/repository?
3. Is the gap temporary or recurring?
4. Can an existing local capability or open-standard surface solve it?
5. If an upstream provider is needed, what is its **smallest useful surface**?
6. What permissions, credentials, infrastructure, data exposure, and lock-in does it introduce?
7. What evidence will prove it closed the original gap?
8. Can it be removed again after the task/project no longer needs it?

The correct answer may be **no additional provider**.
