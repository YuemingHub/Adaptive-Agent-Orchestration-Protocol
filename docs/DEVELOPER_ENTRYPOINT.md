# Developer Entry Point

AAOP should feel like one simple developer interface, not a framework selector.

The developer may arrive with very different states:

```text
“I have an idea...”
“I want to use agents, MCP, memory and RAG...”
“I don't know what this repo is doing...”
“This codebase is a mess...”
“Login is broken...”
“Add this feature...”
“Review this before I merge...”
“Should we adopt this framework?”
“Deploy this safely...”
```

The surface interaction is intentionally the same:

> **State what you want in ordinary language and provide any asset you already have.**

AAOP handles the internal route.

### Default autonomous takeover

For a project the owner does not understand, the entire entry can be:

```text
AAOP: take over this project.
```

That delegates ordinary development responsibility. AAOP recovers current evidence and
intent, selects the highest-value safe next goal, implements and verifies the smallest
delta, then reassesses and continues. The owner does not need to know the roadmap,
current stage, routes, stack, providers, or test commands.

AAOP asks only when a material product/domain choice cannot be recovered or safely
tested, or for credentials, cost, external-account access, production authorization,
or irreversible/high-impact actions. An unfamiliar codebase, technical ambiguity,
failed test, architecture choice, and ordinary debugging are not reasons to send the
work back to a novice. This entry composes the existing Working Contract, discovery,
Route, and Journey mechanisms; it is not a new workflow engine or state store.

## 1. The real entry model

Do not start from:

```text
What framework?
What agent team?
Which MCP?
Which workflow mode?
Which database?
```

Start from:

```text
What does the developer have right now?
        +
What situation are they in?
        +
What should become true next?
        +
Which words are outcomes/constraints,
and which are only proposed solutions?
```

Then:

```text
Natural-language request
        ↓
Available asset/evidence
        ↓
Developer Intake
        ↓
Primary route
        ↓
Route-specific discovery
        ↓
Outcome / decision + acceptance evidence
        ↓
Capability planning
        ↓
Reuse current environment
        ↓
Only if a real gap exists:
Skill / MCP / discovery / runtime / workspace
        ↓
Execute or Review
        ↓
Verify
```

## 2. Six primary routes

The route taxonomy is deliberately small. It is not meant to describe every software activity. It exists only to change the **first correct move**.

### A. Idea → Build

Typical language:

- “I have an idea but I don't know how to make it.”
- “I want an app that...”
- “Can AI build this for me?”
- “Use agents, MCP, RAG, memory and a vector DB to make...”

First responsibility:

**Do not choose architecture first.** Understand the human/product outcome and find the smallest real slice that will teach us something important.

Typical path:

```text
Idea / long-term vision
→ actor + real situation
→ observable outcome
→ hard constraints vs preferences vs solution hypotheses
→ key uncertainty
→ smallest evidence-bearing slice
→ minimum reversible technical shape
→ build
→ validate with real behavior
```

#### Solution vocabulary rule

Early technology names are not automatically requirements.

Classify them:

```text
hard constraint  = required for a concrete reason
preference       = useful if it fits
hypothesis       = possible solution not yet justified
```

Example:

> “I want Agents + MCP + Vector DB + Graph + Memory.”

The system should not install five layers immediately. It first asks internally what user workflow needs coordination, external tools, retrieval, state, or branching. Technologies enter only where the first slice proves the need.

#### First-proof rule

A first slice is not just “something that runs.” It should reduce one material uncertainty.

Good evidence can answer:

- Will the target user complete this workflow?
- Can one natural-language request become the required verified result?
- Is the proposed interaction understandable?
- Does the existing host already solve enough of the problem?
- Which part actually fails before we build infrastructure around it?

A roadmap, architecture diagram, large scaffold, or multi-agent team can still be useful later, but none of them proves the idea works by itself.

A beginner should not be forced to produce a PRD or choose a stack before the system can help.

---

### B. Repository Recovery

Typical language:

- “I made this with AI and now I don't understand it.”
- “The repository is messy. Help me continue.”
- “This project has been changed by several agents.”
- “Figure out what is going on and take over.”

First responsibility:

**Establish trustworthy current state before broad changes.**

Typical path:

```text
Preserve state
→ instructions / candidate current-fact sources
→ authority + freshness
→ code / manifests / tests / CI / deployment
→ current-state map
→ contradictions / historical paths / active paths
→ highest-leverage blocker
→ stabilize one path
→ verify
→ reassess
```

Do not start with mass refactoring or “clean architecture.”

---

### C. Bug Fix

Typical language:

- “This button doesn't work.”
- “Login returns 500.”
- “CI started failing.”
- “It worked yesterday.”

First responsibility:

**Establish the reported baseline and failure evidence before guessing at a fix.**

Typical path:

```text
Reported version/environment
→ reconcile with current baseline
→ observed vs expected
→ reproduce / logs / failing test
→ root-cause hypotheses
→ narrow durable fix
→ regression evidence
```

Old traceback lines and issue comments are evidence/hypotheses, not current truth by default.

---

### D. Feature Change

Typical language:

- “Add invitations.”
- “I want dark mode.”
- “Support another payment method.”
- “Change this workflow.”

First responsibility:

**Translate the feature sentence into observable behavior and inspect the existing path before designing a new one.**

Typical path:

```text
Requested behavior/invariants
→ current baseline
→ existing primitives/path
→ stale artifact salvage if relevant
→ impacted contracts/data/UI/tests
→ smallest coherent change
→ acceptance behavior
→ regression verification
```

When old PRs or branches contain useful intent, preserve behavior/tests/rationale rather than carrying old implementation wholesale.

---

### E. Understand / Review

Typical language:

- “Explain this repo.”
- “Review this PR.”
- “Is this architecture reasonable?”
- “Tell me what is risky before I continue.”
- “Should we adopt this framework?”

First responsibility:

**Understand which decision the review needs to support and keep the review read-only unless implementation is requested.**

Typical path:

```text
Decision + usage context
→ targeted current evidence
→ verify material external claims when practical
→ verified facts vs external claims vs inference vs unknowns
→ contextual material risks
→ recommendation / acceptance conditions
```

#### Review is not repository-summary mode

The goal is not to read everything. Inspect the minimum evidence that can change the decision.

#### Current-source rule

A security issue, advisory, previous review, or comment is an evidence lead. For material present-tense claims, inspect the relevant current implementation/status when practical.

#### Contextual-risk rule

Do not simply copy severity labels. Separate:

```text
verified mechanism
plausible impact
usage/deployment assumptions
actual exposure/permissions
unknowns
```

The same mechanism may support different adoption decisions in a single-user isolated sandbox versus a shared networked developer environment.

#### Mutation boundary

No project, PR, issue, configuration, or upstream mutation by default. Discovering an obvious fix does not silently turn the task into implementation.

---

### F. Release / Operations

Typical language:

- “Deploy this.”
- “Production is broken.”
- “Migrate the database.”
- “Fix the CI/CD pipeline.”
- “Get this ready to ship.”

First responsibility:

**Understand the target environment, authorization, blocker class, blast radius, and rollback before consequential writes.**

Typical path:

```text
Target/current state
→ operational evidence + reachability
→ blocker classification
→ reversible validation
→ rollback
→ authorization boundary
→ execute
→ smoke/runtime validation
```

Environment/network policy, credentials, permissions, unavailable dependencies, product decisions, and missing evidence do not automatically become capability gaps.

## 3. Mixed requests: route by the blocking outcome

Real requests frequently contain several intents.

Example:

> “This repo is a mess, checkout is broken, and later I want to add coupons.”

Do not launch three workflows.

Route:

```text
Primary: bug-fix (checkout blocks current use)
Queued: repo-recovery
Queued: feature-change (coupons)
```

Another example:

> “Review this framework; if it is safe enough, integrate it.”

Route:

```text
Primary: understand-review
Decision: adopt / reject / conditionally adopt
then, only after the adoption decision:
feature-change / integration work
```

AAOP routes are **state transitions**, not permanent project labels.

## 4. The clarification rule

A beginner-friendly system fails if it makes the user answer ten technical questions before doing anything.

Use this order:

```text
Can existing evidence answer it?
  yes → inspect
  no
  ↓
Can a low-risk experiment answer it?
  yes → test
  no
  ↓
Would the missing answer materially change outcome/route/safety?
  no → use a reversible assumption
  yes → ask one concrete question
```

Good:

> “For the first version, what is the one thing a user must be able to complete?”

> “Should invitations allow only parents, or any family member?”

Bad:

> “Please provide stack, architecture, requirements, constraints, target users, desired workflow, deployment platform, and acceptance criteria.”

## 5. Beginner does not mean simplified engineering

The user experience can be simple while the internal engineering remains rigorous.

The system can internally perform:

- product assumption testing;
- repository archaeology;
- dependency analysis;
- root-cause debugging;
- architecture impact analysis;
- capability discovery;
- current-source verification;
- contextual security review;
- independent review;
- testing and rollback planning;

without exposing those as prerequisites the user must learn.

The target UX is:

```text
User: “Fix login.”

System internally:
intake → bug route → baseline → reproduce → trace → fix → regression

System externally:
“I found the failing session-refresh path, fixed the cause, and added a regression check. Here is what changed and what was verified.”
```

or:

```text
User: “I want to build this idea with lots of agents.”

System internally:
idea route → outcome → hypothesis classification → first proof → minimal implementation

System externally:
“I reduced the first version to one end-to-end workflow we can actually test. We don't need a multi-agent runtime yet; the current host is enough for this proof.”
```

## 6. Internal intake envelope

AAOP may keep a small derived state object. This is internal coordination state; do not make the user fill it out.

The envelope should capture enough to preserve route/outcome/constraints, but technical solution hypotheses should not silently become hard constraints.

## 7. Product principle

AAOP should progressively hide complexity from the developer, not remove rigor from development.

The ideal entry is eventually as small as:

```text
“Here's my idea. Help me make it real.”
```

or:

```text
“Here's the repo. Continue it.”
```

or:

```text
“Should we use this framework?”
```

or:

```text
“Checkout broke after yesterday's change. Fix it.”
```

Everything after that—route selection, evidence classification, product slicing, project understanding, capability matching, provider integration, review boundaries, execution, and verification—is orchestration work, not user homework.
