# Developer Entry Point

AAOP should feel like one simple developer interface, not a framework selector.

The developer may arrive with very different states:

```text
“I have an idea...”
“I don't know what this repo is doing...”
“This codebase is a mess...”
“Login is broken...”
“Add this feature...”
“Review this before I merge...”
“Deploy this safely...”
```

The surface interaction is intentionally the same:

> **State what you want in ordinary language and provide any asset you already have.**

AAOP handles the internal route.

## 1. The real entry model

Do not start from:

```text
What framework?
What agent team?
Which MCP?
Which workflow mode?
```

Start from:

```text
What does the developer have right now?
        +
What situation are they in?
        +
What should become true next?
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
Outcome + acceptance evidence
        ↓
Capability planning
        ↓
Reuse current environment
        ↓
Only if a real gap exists:
Skill / MCP / discovery / runtime / workspace
        ↓
Execute
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

First responsibility:

**Do not choose architecture first.** Understand the human/product outcome and find the smallest real slice worth building.

Typical path:

```text
Idea
→ intended user/outcome
→ key uncertainty
→ smallest buildable/testable slice
→ capability/stack decisions
→ build
→ validate with real behavior
```

A beginner should not be forced to produce a PRD before the system can help.

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
→ instructions / product intent
→ code / manifests / tests / CI / deployment
→ current-state map
→ contradictions / dead paths / active paths
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

**Establish failure evidence before guessing at a fix.**

Typical path:

```text
Observed vs expected
→ reproduce / logs / failing test
→ trace failing path
→ root cause
→ narrow durable fix
→ regression evidence
```

The system should not ask the user for information already visible in supplied logs or the repository.

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
Requested behavior
→ existing primitives/path
→ product ambiguity that actually matters
→ impacted contracts/data/UI/tests
→ smallest coherent change
→ acceptance behavior
→ regression verification
```

Avoid creating parallel architecture just because the existing structure is unfamiliar.

---

### E. Understand / Review

Typical language:

- “Explain this repo.”
- “Review this PR.”
- “Is this architecture reasonable?”
- “Tell me what is risky before I continue.”

First responsibility:

**Understand which decision the review needs to support.**

Typical path:

```text
Decision/question
→ targeted evidence
→ facts vs inference
→ material risks
→ recommendation
```

No repository mutation by default.

---

### F. Release / Operations

Typical language:

- “Deploy this.”
- “Production is broken.”
- “Migrate the database.”
- “Fix the CI/CD pipeline.”
- “Get this ready to ship.”

First responsibility:

**Understand the target environment, blast radius, and rollback before consequential writes.**

Typical path:

```text
Target/current state
→ operational evidence
→ reversible validation
→ rollback
→ authorization boundary
→ execute
→ smoke/runtime validation
```

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

> “Understand this old repo and continue building it.”

Route:

```text
Primary: repo-recovery
then re-route to feature-change once the current state is trustworthy
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

> “Should invitations allow only parents, or any family member?”

Bad:

> “Please provide stack, architecture, requirements, constraints, target users, desired workflow, deployment platform, and acceptance criteria.”

## 5. Beginner does not mean simplified engineering

The user experience can be simple while the internal engineering remains rigorous.

The system can internally perform:

- repository archaeology;
- dependency analysis;
- root-cause debugging;
- architecture impact analysis;
- capability discovery;
- independent review;
- testing and rollback planning;

without exposing those as prerequisites the user must learn.

The target UX is:

```text
User: “Fix login.”

System internally:
intake → bug route → inspect → reproduce → trace → fix → regression

System externally:
“I found the failing session-refresh path, fixed the cause, and added a regression check. Here is what changed and what was verified.”
```

## 6. Internal intake envelope

AAOP may keep a small derived state object:

```json
{
  "raw_request": "This repo is a mess and login is broken. Fix login first.",
  "asset_state": "current-workspace",
  "situation": "mixed",
  "desired_outcome": "Restore the login path before broader repository recovery.",
  "evidence_present": ["repository", "tests"],
  "route": "bug-fix",
  "route_confidence": 0.94,
  "question_needed": false,
  "queued_secondary_intents": ["repo-recovery"],
  "initial_risk": "low"
}
```

This is internal coordination state. Do not make the user fill it out.

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
“Checkout broke after yesterday's change. Fix it.”
```

Everything after that—route selection, project understanding, capability matching, provider integration, execution, and verification—is orchestration work, not user homework.
