# Developer Intake Routing Examples

These examples are behavioral fixtures for AAOP's natural-language front door. They are not keyword rules.

## 1. Rough idea

**User**

> I want to make something that helps a small team turn meeting notes into actual follow-up work. I don't know how to build it.

**Expected intake**

```yaml
asset_state: idea-only
situation: greenfield
route: idea-to-build
question_needed: false
```

**Why**

There is no trustworthy implementation baseline. The first move is to identify the smallest outcome worth making real, not select a stack or agent framework.

---

## 2. AI-generated messy repository

**User**

> I built this with several AI tools over a few months. Now there are duplicate folders and I don't know which backend is actually live. Understand it and continue from the right place.

**Expected intake**

```yaml
asset_state: current-workspace
situation: repo-recovery
route: repo-recovery
question_needed: false
```

**Why**

Repository evidence should resolve stack, active paths, tests, deployment, and history. Asking the user to describe architecture would offload repository archaeology back to the user.

---

## 3. Messy repo plus blocking bug

**User**

> This repo is messy, but the urgent thing is checkout started returning 500. Fix checkout first and then we can clean things up.

**Expected intake**

```yaml
asset_state: current-workspace
situation: mixed
route: bug-fix
queued_secondary_intents:
  - repo-recovery
question_needed: false
```

**Why**

The blocking observable outcome is restore checkout. Cleanup is secondary and must not expand the bug fix.

---

## 4. Bug with logs already supplied

**User**

> Login is broken after refresh. Here's the stack trace and the repo. Fix it.

**Expected intake**

```yaml
asset_state: mixed
situation: bug
route: bug-fix
question_needed: false
```

**Anti-pattern**

Do not respond: “What error are you seeing?” The error evidence is already available.

---

## 5. Feature with resolvable implementation details

**User**

> Add dark mode using the design system that's already in this repo.

**Expected intake**

```yaml
asset_state: current-workspace
situation: feature
route: feature-change
question_needed: false
```

**Why**

Inspect the existing design tokens/theme primitives first. Do not ask the user which CSS framework or state library to use if the repo answers it.

---

## 6. Feature with a real product ambiguity

**User**

> Add family invitations.

Repository evidence shows both parent and child accounts but no invitation policy.

**Expected intake**

```yaml
situation: feature
route: feature-change
question_needed: true
question: Which account types should be allowed to invite which family members?
```

**Why**

This is a product/permission choice that repository inspection cannot safely invent.

---

## 7. Review only

**User**

> Review PR #42 and tell me whether it is safe to merge. Don't change anything.

**Expected intake**

```yaml
situation: understand-review
route: understand-review
question_needed: false
```

**Why**

The user explicitly requested a decision-oriented review and prohibited mutation.

---

## 8. Feature then deploy

**User**

> Add CSV export and deploy it when it's ready.

**Expected intake**

```yaml
situation: mixed
route: feature-change
queued_secondary_intents:
  - release-operations
question_needed: false
```

**Why**

Implementing and verifying the feature is upstream of deployment. Production authorization can be handled when the release route becomes active.

---

## 9. Production incident

**User**

> Production started timing out after the last deploy. Find the cause and restore service.

**Expected intake**

```yaml
asset_state: deployed-system
situation: release-operations
route: release-operations
initial_risk: high
```

**Why**

Runtime state, blast radius, rollback, observability, and permission boundaries dominate the first moves.

---

## 10. “Continue the project”

**User**

> Here's the repository. I haven't touched it in six months. Continue development in the direction that makes the most sense.

**Expected intake**

```yaml
asset_state: repository-reference
situation: repo-recovery
route: repo-recovery
question_needed: false
```

**Why**

Do not ask “What feature should I build?” immediately. First reconstruct current state, product intent, unfinished work, and highest-leverage blocker. A feature route can be selected after recovery produces evidence.

---

## 11. Tiny explicit change

**User**

> Change the button text from “Send” to “Submit” on the signup screen.

**Expected behavior**

Treat this as a simple `feature-change`, but compress orchestration. Do not generate intake files, capability matrices, team plans, or external providers for a trivial local edit.

---

## 12. Route correction after evidence

**User**

> Add a retry button to fix failed uploads.

Initial route may be `feature-change`. During inspection, evidence shows uploads fail because a regression broke the existing retry mechanism.

**Correct behavior**

Re-route to `bug-fix`, restore the intended behavior, verify regression evidence, and avoid building a redundant second retry system.

## Regression principle

The route is correct when it produces the right **first engineering move**, not when it matches a phrase.
