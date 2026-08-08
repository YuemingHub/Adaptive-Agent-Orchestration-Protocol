# AAOP Architecture

## 1. What AAOP is

AAOP is a **control protocol**, not a permanent collection of persona prompts.

Its central transformation is:

```text
Outcome + Project State + Host Capability
                 ↓
          Capability Graph
                 ↓
     Ownership + Provider Binding
                 ↓
          Execution Graph
                 ↓
        Evidence / Replanning
```

## 2. Control plane vs execution plane

### Control plane

Owned by the Meta-Orchestrator:

- environment discovery;
- project discovery;
- intent/constraint resolution;
- capability decomposition;
- provider matching;
- team construction;
- permission/autonomy decisions;
- DAG construction;
- verification strategy;
- replanning and final synthesis.

### Execution plane

Owned by one or more execution contexts:

- implementation;
- research;
- browser/runtime operation;
- data/API access;
- test execution;
- review;
- repository/deployment operations.

A host may implement both planes in one model/context. AAOP describes responsibility boundaries even when physical process boundaries do not exist.

## 3. Why capability-first matters

Role-first orchestration tends to recreate a human organization chart:

```text
request → PM → architect → frontend → backend → QA
```

This produces unnecessary handoffs and often chooses tools before the problem is understood.

AAOP instead asks:

```text
What must be possible?
What is already possible here?
What capability is genuinely missing?
Which responsibilities need isolation?
```

Only then does it create owners.

## 4. Progressive disclosure

Persistent bootstrap files must remain compact. Long procedures consume context and become stale.

AAOP therefore separates:

- `AGENTS.md` / `CLAUDE.md` — persistent bootstrap;
- `.aaop/ORCHESTRATOR.md` — normative control flow;
- `.aaop/skills/*/SKILL.md` — on-demand procedures;
- `.aaop/policies/` — risk and tool rules;
- `.aaop/registries/` — machine-readable vocabulary/hints;
- `.aaop/schemas/` — optional runtime interoperability;
- `adapters/` — host-specific mappings.

This follows the Agent Skills principle that metadata can be discovered first and detailed instructions loaded only when relevant.

## 5. Runtime state is derived state

Files in `.aaop/runtime/` are optional materializations of the orchestrator's working model. They should be treated like generated planning state unless the project deliberately adopts them as durable records.

Do not confuse:

- **source of truth:** product requirements, architecture, code, tests, policies, user decisions;
- **derived state:** project profile, capability matrix, team plan, execution plan.

Derived state must be refreshed when source evidence changes.

## 6. Host abstraction

AAOP does not require every host to implement the same primitives.

The same Team Plan can map to:

```text
Claude Code subagents
Codex tasks/background work
Cursor sessions/worktrees
workflow-engine workers
a single LLM executing sequential isolated roles
```

This is why host-specific configuration stays in `adapters/`.

## 7. Tool and MCP boundary

A Skill may explain how to review a PR. It cannot make GitHub accessible.

An MCP/tool may expose GitHub. It does not automatically contain the project's review methodology.

AAOP intentionally composes them:

```text
Review owner
  + code-review methodology Skill
  + GitHub read provider
  + repository policy
  = bounded review capability
```

## 8. Safety and autonomy

AAOP is designed for high autonomy **inside reversible project work**, not indiscriminate external autonomy.

The control plane evaluates reversibility, blast radius, external effects, sensitive data, permission escalation, monetary cost, production impact and ambiguity. This lets the agent continue ordinary work without repeatedly asking the user, while preserving confirmation boundaries where consequences are material.

## 9. Verification as a first-class phase

The implementation context is not the final authority on its own success.

AAOP requires an evidence phase that can use tests, runtime behavior, browser validation, schema checks, security review, independent review or release smoke tests depending on the outcome.

Failure feeds back into capability/team/tool selection. Verification is therefore part of orchestration, not a final checklist.

## 10. Future evolution

AAOP v0.1 is executable directly by AI hosts as Markdown + Skills + policies + schemas.

Potential later layers, without changing the core ontology:

- a CLI that generates runtime plans;
- a provider/plugin registry with trust metadata;
- adapter generators for additional AI IDEs;
- conformance tests and orchestration benchmarks;
- signed Skill/provider packages;
- machine-executable orchestration graphs;
- telemetry for measuring unnecessary handoffs, intervention rate and verification success.

The protocol should only absorb these features when they improve real outcomes rather than adding orchestration ceremony.
