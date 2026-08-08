---
name: developer-intake
description: Convert a developer's minimal natural-language request into the correct AAOP development route before capability/provider selection. Use for vague ideas, messy repositories, bug reports, feature requests, code understanding/review, or release/operations work. Ask only when one missing fact would materially change the route or outcome.
---

# Developer Intake

This is the front door of AAOP.

The user should not need to know the route names, Agent types, Skills, MCP servers, runtimes, or orchestration model. Accept ordinary developer language such as:

- “I have an idea but I don't know how to build it.”
- “This repo is a mess; understand it and keep going.”
- “Login returns 500. Fix it.”
- “Add family invitations.”
- “Review this PR/repo and tell me what matters.”
- “Get this ready to deploy.”

## Principle

First understand **the user's situation and desired observable outcome**. Then route. Do not make the user classify their own task or design the technical solution unless they explicitly want to.

Routing is not keyword matching. Consider together:

1. **Asset state** — idea only, current workspace, repository reference, snippets/files, or deployed system.
2. **Situation** — greenfield, recovery, bug, feature, understanding/review, or release/operations.
3. **Desired outcome** — what should be true when the work is done.
4. **Evidence** — repository, tests, failures, logs, issues/specs, runtime/deployment context.
5. **Risk** — whether the first meaningful action is local/reversible or externally consequential.
6. **Solution vocabulary status** — whether named technologies are hard constraints, preferences, or merely hypotheses the user is exploring.

When useful, materialize `.aaop/runtime/intake-envelope.json` against `../../schemas/intake-envelope.schema.json`.

## Step 1 — Read before asking

If a workspace, repo URL, issue, file, logs, or other accessible evidence is already available, inspect enough of it to resolve the situation before asking the user to restate what the environment can answer.

Do not ask “What stack is this?” when manifests can answer.
Do not ask “What error do you see?” when the supplied logs show it.
Do not ask the user to summarize a repository you can inspect.

## Step 2 — Infer the primary route

Read `../../registries/routes.json`.

Choose one primary route:

- `idea-to-build`
- `repo-recovery`
- `bug-fix`
- `feature-change`
- `understand-review`
- `release-operations`

### Priority rules for mixed requests

Choose the route that unlocks the user's most immediate outcome.

Examples:

- “This repo is messy and checkout is broken; fix checkout first” → `bug-fix`, queue recovery/cleanup.
- “Understand this old repo and then continue development” → `repo-recovery`.
- “Review this repo and if the architecture is sound add X” → `understand-review` first if the review gates the feature decision; otherwise `feature-change` with an inspection phase.
- “Add X and deploy it” → `feature-change` first; queue `release-operations` unless deployment is already the blocking task.

Do not create parallel routes merely because the sentence contains multiple verbs.

## Step 3 — Translate language into an observable outcome

Do not treat the literal wording as the complete specification.

Convert it into a provisional statement of success.

Examples:

- “Make it better” → identify which current pain/decision defines better.
- “Fix login” → user can complete the login path that currently fails; the observed failure no longer reproduces and regression evidence passes.
- “Add invitation” → identify who can invite whom, the visible workflow, and the smallest acceptance path.
- “Continue this project” → understand current state, find the highest-leverage next blocker, improve it with evidence.

### Early technical vocabulary is not automatically a requirement

For greenfield requests, classify named technology before using it:

- **hard constraint** — the user explicitly requires it for compatibility, policy, contract, existing ecosystem, or another concrete reason;
- **preference** — useful to honor when it does not conflict with the outcome;
- **solution hypothesis** — a technology name proposed before the need is evidenced.

If a user says “use agents, MCP, RAG, memory, a vector DB, and graph orchestration,” do not silently turn all of those terms into architecture requirements. First identify the user-visible workflow and what capability each term would need to supply.

If the outcome can be safely inferred from project evidence and the request, proceed.

## Step 4 — Ask only a route-changing or outcome-blocking question

Ask at most one intake question at a time, and only when the answer could materially change:

- the primary route;
- the user-visible outcome;
- a major product choice;
- whether a proposed technology is actually a hard constraint;
- or the safety/permission class of the next action.

Good intake questions are concrete:

- “Which user should be able to invite whom?”
- “Is the failure in production or only local?”
- “Which of these two behaviors do you want to preserve?”
- “For the first version, what is the one task a user must be able to complete?”

Avoid process questions:

- “Do you want analysis or implementation?” when the request already says “fix”.
- “Should I continue?”
- “Do you want me to inspect the repo?”
- “Which agent team should I use?”
- “Which database/framework should I choose?” when the system can derive it later.

If a reversible experiment can resolve the ambiguity, prefer the experiment over asking.

## Step 5 — Preserve review boundaries

When the request is primarily “review / assess / tell me whether we should …”, the default route is read-only `understand-review` unless the user explicitly authorizes implementation.

Do not convert a review finding into a patch, PR, configuration change, issue update, or upstream mutation merely because the fix looks obvious. The review should first support the decision the user actually asked to make.

## Step 6 — Set route confidence

Use a practical confidence estimate:

- `0.85–1.0`: route and outcome are clear enough to start.
- `0.65–0.84`: route is clear; some details can be learned during discovery.
- `<0.65`: ask one high-leverage question only if inspection cannot resolve it.

Confidence does not need to be shown to the user unless useful; it exists to prevent ceremonial clarification.

## Step 7 — Hand off, don't over-orchestrate

After routing:

- `idea-to-build` → outcome discovery → first evidence-bearing slice → minimal architecture → real evaluation.
- `repo-recovery` → project discovery/recovery before broad implementation.
- `bug-fix` → reconcile baseline → reproduce/evidence → localize → minimal fix → regression verification.
- `feature-change` → behavior contract → impact discovery → implementation → acceptance/regression verification.
- `understand-review` → decision-oriented inspection; current evidence; no mutation by default.
- `release-operations` → environment/runtime evidence + blocker classification + rollback + autonomy policy before consequential action.

Only after the route exposes a real capability gap should AAOP run provider selection.

## Step 8 — Keep the interaction natural

Do not announce internal machinery unless it helps the user.

Prefer:

> “I found the failing login path and I'm tracing it from the API boundary before changing code.”

Not:

> “I classified you into Route bug-fix with confidence 0.93 and spawned the debugging capability.”

The route is an internal coordination mechanism, not a form the user must operate.

## Completion criterion

Developer intake is complete when:

- the current situation is sufficiently understood;
- one primary route is selected;
- a provisional observable outcome is defined;
- proposed solution vocabulary is not being mistaken for requirements without evidence;
- review/mutation boundaries are explicit where relevant;
- only material unknowns remain;
- and work can move into the route-specific discovery/execution loop without making the user manage orchestration.
