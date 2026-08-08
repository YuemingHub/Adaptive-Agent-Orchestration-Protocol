# AAOP v0.5 ecosystem research notes

This file records the evidence behind the v0.5 route-capability design. It is not a product roadmap and should be revised when upstream projects materially change.

## Key finding

Route execution should not become six new AAOP workflow engines. Mature systems already cover substantial parts of the software-development lifecycle.

### GitHub Spec Kit

Source of truth: https://github.com/github/spec-kit and https://github.github.com/spec-kit/

Current upstream capabilities relevant to AAOP include:

- agent-agnostic Spec → Plan → Tasks → Implement workflows;
- support for existing projects and evolving specifications;
- an opt-in Agentic Bug Fix extension with assess → fix → validate;
- extension/catalog/bundle machinery with provenance and removal support;
- community extensions for brownfield discovery, code review, security review, release shipping, and other SDLC concerns.

AAOP implication: use Spec Kit as a mature optional structured-development provider when a route benefits from durable specifications or an existing supported extension. Do not duplicate its CLI, extension system, bundle manager, or SDD artifacts.

Community extensions are not automatically trusted merely because they appear in a catalog. Current Spec Kit documentation explicitly states that community components are independently maintained and are not necessarily audited or endorsed. AAOP must retain provenance and permission review.

### mini-SWE-agent

Source of truth: https://github.com/SWE-agent/mini-swe-agent

The SWE-agent maintainers recommend mini-SWE-agent over the older SWE-agent for new usage. It is intentionally minimal and oriented around solving well-defined GitHub/software-engineering issues with an agent loop.

AAOP implication: it is a useful optional bug/issue execution provider when the issue is reproducible, bounded, and testable, especially when the current host is not the desired execution environment. It should not replace route intake, product ambiguity resolution, or project recovery.

### OpenHands

Source of truth: https://github.com/OpenHands and https://github.com/OpenHands/software-agent-sdk

OpenHands provides a general autonomous coding platform plus a modular Software Agent SDK, CLI/canvas/runtime ecosystem, skills/extensions, and automation patterns.

AAOP implication: treat OpenHands as an optional autonomous software-engineering runtime when a dedicated coding-agent environment is itself the missing capability. Do not introduce it merely because a task involves code.

### Playwright

Source of truth: https://github.com/microsoft/playwright and https://github.com/microsoft/playwright-mcp

Playwright exposes several distinct surfaces relevant to agentic development:

- Playwright Test for durable browser E2E tests;
- Playwright CLI + Skills, which upstream currently recommends for high-throughput coding-agent workflows because it is more context/token efficient;
- Playwright MCP for persistent, introspective browser-agent loops where continuous page state is valuable.

AAOP implication: model browser verification as a capability and choose the smallest Playwright surface that closes the gap; do not always default to MCP.

## v0.5 decision

Introduce **Route Capability Packs**. A pack is not a workflow engine or install bundle. It describes the route's engineering stages, required capabilities, evidence, escalation triggers, and optional mature providers.

Selection order remains:

1. current host/repository capabilities;
2. existing local tests/scripts/skills/tools;
3. route capability pack guidance;
4. one justified upstream provider/recipe;
5. verify that the provider closed the original gap.

The developer still interacts through minimal natural language. Route packs are internal execution metadata.
