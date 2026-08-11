# Human-Agent Working Contract

AAOP v1 treats the relationship between the human and the execution system as a production contract, not a prompt convention.

The desired experience is:

```text
ordinary-language goal
  -> inspect project / idea evidence
  -> ask only what the human truly owns
  -> confirm autonomous or collaborative working mode once
  -> align observable outcome and success evidence
  -> execute with the minimum sufficient Agent/Task Pod
  -> verify
  -> hand off between bounded Pods when responsibilities change
  -> return only genuine human decisions/authorization/final acceptance
```

## Why this exists

A capable coding Agent can still fail the user in two opposite ways:

- **under-autonomy** — it repeatedly asks the human to choose frameworks, tools, Agent counts, implementation steps, or whether to continue;
- **over-autonomy** — it guesses product intent, silently invents business/domain decisions, or treats a vague instruction as authorization for consequential actions.

AAOP therefore separates **decision ownership** from **engineering execution**.

## Collaboration modes

The project-local contract records one of two confirmed modes.

### Autonomous delivery

Once intent is aligned, the Agent owns ordinary engineering execution and continues without ceremonial approval between steps. It asks only when a genuinely human-owned decision, new authorization/credential/cost, consequential external action, or unresolved blocker requires human input.

An owner can select this mode simply by saying, for example, `AAOP: take over this
project.` That is sufficient to delegate recovery, current-goal selection, ordinary
technical decisions, implementation, verification, repair, and the next-delta loop.
It does not silently authorize credentials, spending, production writes, destructive
actions, or irrecoverable product-value decisions.

### Collaborative delivery

The Agent still owns implementation, testing, debugging and ordinary technical choices, but surfaces material product/architecture tradeoffs at useful checkpoints. Collaborative mode is not approval-per-file or approval-per-command.

AAOP never silently chooses one of these modes for a new project. If no authoritative prior choice exists, the host asks the human once and persists the answer.

Technical uncertainty is not a human-owned question. When the project is unfamiliar,
tests fail, the current goal is missing, or architecture/tool choices remain open, the
Agent first reconstructs intent and baseline from evidence, runs safe experiments, and
makes reversible engineering decisions. It asks a novice only when an unresolved value
fork materially defines the product or a real authority boundary remains.

## Project-local state

The durable state is:

```text
.aaop/runtime/working-contract.json
```

It is managed through:

```bash
python .aaop/tools/working_contract.py status --json
python .aaop/tools/working_contract.py init --goal "<goal>" --json
python .aaop/tools/working_contract.py set-mode --expected-revision <n> --mode autonomous|collaborative --json
python .aaop/tools/working_contract.py update-alignment --expected-revision <n> ... --json
python .aaop/tools/working_contract.py confirm-alignment --expected-revision <n> --json
python .aaop/tools/working_contract.py gate --json
```

The user is not expected to type these commands. They are the Agent's continuity/coordination primitives.

Mutations use an expected `revision` and an OS file lock so an old or parallel session cannot silently overwrite a newer collaboration/alignment decision.

## Alignment contract

Before sustained execution, AAOP tries to establish:

- long-horizon goal;
- actor;
- situation;
- observable outcome;
- essential `must` invariants;
- explicit non-goals for the current cycle;
- genuine constraints;
- observable success evidence;
- unresolved human-owned questions.

The system must not turn this into a fixed questionnaire.

Unknowns are classified into three buckets:

1. **Evidence-resolvable** — inspect repository/runtime/history/research; do not ask the user.
2. **Expert-decidable** — the Agent/CTO decides from constraints, reversibility, cost and project fit.
3. **Human-owned** — the answer defines intent, domain truth, business/audience boundary, or grants authority.

Only the third category should interrupt the human.

`confirm-alignment` fails while collaboration mode is unset, while goal/actor/situation/outcome are incomplete, while there is no observable success evidence, or while a human-owned open question remains.

`working_contract.py gate` returns `execution_allowed=true` only after this interaction contract is aligned. It does not override repository rules, safety policy, production authorization, missing credentials, or Journey blockers.

## Decision ownership

Default ownership is deliberately asymmetric.

### Human-owned

Typical examples:

- product intent and value tradeoffs;
- domain truth the project cannot supply;
- audience/business-model boundaries;
- credentials/secret-bearing authorization;
- new monetary commitments.

### Agent-owned

Typical examples:

- technical architecture inside established constraints;
- framework/database/tool choice when not a hard user requirement;
- code organization and implementation details;
- testing and ordinary engineering verification;
- whether one Agent is enough or a Task Pod is justified;
- specialist/provider choice within AAOP policy.

### Joint

Typical examples:

- material irreversible product behavior;
- major privacy/safety/ethics/legal boundaries;
- high-impact production/destructive actions without an already established authorization policy.

Ownership of a *decision* does not automatically authorize every resulting *action*. AAOP Autonomy Policy still applies to writes, permissions, secrets, cost and production impact.

## Task Pods

Multi-Agent work is optional and bounded.

AAOP defaults to **one capable Agent**. A Task Pod is created only when specialization, context isolation, safe parallelism, independent review, or permission boundaries create measurable value.

Production invariants:

- 1–5 members maximum;
- exactly one accountable owner;
- members exist for responsibilities, not honorary titles;
- objective acceptance criteria;
- independent reviewer for consequential work when practical;
- one Pod owns one bounded outcome;
- the Pod dissolves after acceptance;
- a materially different next Pod receives a standard handoff.

If more than five responsibility contexts appear necessary, AAOP splits the work into sequential Pods instead of creating a larger standing team.

## External role libraries

`agency-agents-zh` may be used as an optional specialist-role source. AAOP selects only the minimum justified role subset and treats role prompts as procedural input, not authority over user intent, project truth, credentials, or tools.

The full role library is never required for ordinary operation.

## External orchestration runtimes

`agency-orchestrator` may be selected only when a justified Task Pod needs DAG/resume/multi-role execution that the current host cannot provide adequately.

When used:

```text
AAOP owns:
  Working Contract
  Journey
  decision ownership
  authorization
  Task Pod outcome
  acceptance evidence
  handoff

provider owns:
  bounded delegated execution mechanics
```

Do not allow a provider DAG and AAOP Journey to become competing sources of truth.

## Handoff contract

When one Task Pod delivers to another, use `.aaop/schemas/task-handoff.schema.json`.

The handoff records:

- long-horizon goal;
- current bounded outcome;
- baseline;
- material decisions + owner + reason;
- delivered result;
- evidence;
- residual risks;
- blockers;
- human-owned open questions;
- next outcome;
- concrete references (commit/PR/test/runtime/artifact identifiers).

The receiving Pod always re-reads current project/Working Contract/Journey evidence. A handoff is continuity evidence, not current authority.

## Production validation

The contract is regression-tested by:

```bash
python scripts/validate_working_contract.py
```

CI runs the gate on Linux and Windows across the declared Python support boundaries. The regression proves at least:

- the system does not silently select autonomous/collaborative mode;
- unresolved human-owned questions block alignment;
- aligned intent permits execution;
- stale contract writes are rejected;
- reopening alignment preserves the human's collaboration preference;
- Task Pods are hard-capped at five members;
- handoff fields remain present;
- external role/orchestration providers remain subordinate to AAOP control boundaries.

AAOP v1 is not production-eligible if this gate is absent or failing.
