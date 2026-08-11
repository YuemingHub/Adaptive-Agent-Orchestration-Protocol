# Ecosystem Map: Integrate, Do Not Reimplement

Verified: 2026-08-11

AAOP sits above existing developer tools, agent standards, SDLC harnesses, verification tools, execution-control planes, runtimes, discovery systems, and workspaces. Its role is to understand **what is needed now**, select the smallest sufficient provider surface, constrain permissions, and verify the result.

## Boundary

AAOP owns:

- natural-language developer intake and route selection;
- Human-Agent Working Contract and decision ownership;
- Route Capability Packs;
- project/environment discovery policy;
- outcome and constraint resolution;
- capability-first planning;
- progressive integration decisions;
- least-privilege / autonomy policy;
- provider selection criteria;
- normalized Integration Recipes;
- Journey/release-cycle continuity;
- evidence, verification, rerouting, and replanning contracts;
- graceful degradation across hosts.

AAOP does **not** own:

- six replacement software-development workflow engines;
- a new coding-agent runtime;
- a duplicate todo/quota/heartbeat execution-control plane;
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

## Long-running execution-control providers

### LoopX

Upstream: https://github.com/huangruiteng/loopx

LoopX is modeled as an optional **long-running execution-control provider**, not as an AAOP replacement runtime.

Select it when the current host/agent can perform the actual engineering work but the project has a proven `execution-continuity` gap across turns, sessions, agents, or external waits. Relevant mechanisms include:

- durable todo/evidence/gate state;
- claim and handoff;
- `quota should-run` decisions;
- wait/quiet/throttled behavior that avoids useless model turns;
- scheduler/heartbeat and monitor hints;
- restartable bounded execution and validated writeback.

AAOP remains authoritative for Working Contract, product/domain truth, current Route, Journey/release-cycle state, provider selection, protected-effect authorization, Task Pod acceptance, and final target verification.

**AAOP must not:**

- copy LoopX's todo/quota/scheduler/run-history model into a parallel AAOP Execution Ledger without a separately proven AAOP-specific gap;
- initialize LoopX merely because a task is large;
- treat LoopX eligibility as permission for production, publication, credentials, billing, or destructive writes;
- use LoopX goal state as a second AAOP Journey/Working Contract;
- make its experimental Turn surface a production dependency without separate qualification;
- assume native Windows support from Python portability alone when the reviewed quick-start is macOS/Linux-shell oriented.

See `docs/LOOPX_INTEGRATION.md` and `.aaop/recipes/loopx.json` for the current authority and adoption contract.

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

Useful when a dedicated long-horizon **agent runtime** is justified by persistence, context isolation, Skills/MCP-heavy execution, or filesystem/subagent patterns.

This is distinct from LoopX: use Deep Agents when the agent runtime itself is the missing mechanism; use LoopX when the agent can already do the work and durable execution-control between bounded turns is the gap.

### agency-orchestrator

Upstream: https://github.com/jnMetaCode/agency-orchestrator

Useful only when a justified AAOP Task Pod needs bounded multi-role DAG/resume execution that the current host cannot supply adequately.

AAOP defines the Pod outcome, member responsibilities, human gates, acceptance and handoff. The delegated runtime must not become a second top-level Journey or Working Contract.

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

These are **conditional candidates**, not fixed routing rules. Some provider gaps such as execution continuity are cross-route rather than owned by one Route.

| Route / situation | Capability gap | Possible mature provider surface |
| --- | --- | --- |
| any long-running Route/Task Pod | agent can execute, but durable bounded continuation/wait/handoff is unreliable | LoopX direct CLI/custom-runner surface after host-native pressure proves `execution-continuity` gap |
| `idea-to-build` | durable intent/specification lifecycle | Spec Kit core workflow |
| `idea-to-build` / `feature-change` | browser acceptance evidence | existing Playwright Test, then CLI+Skills/MCP only if needed |
| `repo-recovery` | long-horizon isolated coding context | Deep Agents or OpenHands when current host runtime is insufficient |
| justified Task Pod on any Route | explicit multi-role DAG/resume execution | agency-orchestrator only when host-native/sequential Pod execution is insufficient |
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
3. Is the gap implementation ability, execution continuity, Task Pod execution, or organizational governance?
4. Is the gap temporary or recurring?
5. Can an existing local capability or open-standard surface solve it?
6. If an upstream provider is needed, what is its **smallest useful surface**?
7. Why is the adjacent provider family not the right primary mechanism?
8. What permissions, credentials, infrastructure, data exposure, and lock-in does it introduce?
9. Which AAOP/project state remains authoritative after integration?
10. What evidence will prove it closed the original gap?
11. Can it be removed again after the task/project no longer needs it?

The correct answer may be **no additional provider**.
