# Example: Software Feature

## User outcome

> Make the signup flow production-ready. Preserve the current product behavior unless a change is needed for correctness. Handle ordinary engineering decisions autonomously and verify the end-to-end flow.

## Discovery result

Assume project evidence shows:

- existing web application;
- signup UI and API already exist;
- validation logic is duplicated;
- unit tests exist but no browser flow test;
- CI can run tests/build;
- host already has filesystem, shell and browser automation;
- GitHub access is connected.

## Capability plan

```text
project-discovery             → native + project-discovery Skill
requirement-reasoning         → main agent
frontend/backend implementation → main implementation owner
browser-validation            → existing browser tool
verification                  → verification-loop Skill + CI/test harness
repository-operations         → existing GitHub provider
security-review               → reviewer context
```

There is **no MCP gap**, so AAOP must not ask the user to install Playwright/GitHub MCP merely because those tools are common.

## Team decision

Use three responsibility contexts, not a company org chart:

1. **Lead / Orchestrator** — project model, acceptance evidence, dependency plan, synthesis.
2. **Implementation Owner** — consolidate validation and fix signup behavior.
3. **Independent Reviewer** — review security/regression/intent and browser evidence.

If the host lacks native subagents, execute these sequentially with role isolation.

## Execution graph

```text
Discovery → Acceptance criteria → Implementation → Unit/integration tests
                                            ↘
                                      Browser flow
                                            ↓
                                  Independent review
                                            ↓
                                     Build / CI proof
```

## User interruptions

None unless implementation discovers a genuine product decision, new paid/credentialed service, production write, or irreversible migration.

## Completion evidence

- relevant unit/integration tests pass;
- browser signup flow succeeds and error cases behave correctly;
- build passes;
- reviewer finds no unresolved material regression/security issue;
- repository delivery matches the user's requested scope.
