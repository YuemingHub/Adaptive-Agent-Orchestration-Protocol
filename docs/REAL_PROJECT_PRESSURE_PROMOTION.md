# Real-Project Pressure Promotion Gate

Status: source-repository evolution contract for AAOP maintainers and agents improving AAOP from real consumer work.

## Purpose

AAOP should improve because real projects expose failures, but it must not become customized to whichever project is currently supplying pressure.

A consumer project is a **pressure source**, not an AAOP schema template, roadmap owner, or permanent fixture. The objective is to let production work challenge AAOP continuously while promoting only reusable protocol lessons into Core.

## Classification before Core changes

Every material finding from a real consumer must be classified before changing AAOP:

1. **consumer-only** — the defect, product decision, naming rule, deployment convention, domain invariant, or test belongs only to the consumer. Fix it there; do not change AAOP Core.
2. **existing-AAOP-coverage** — AAOP already contains the necessary invariant/route/policy/provider behavior. Use the consumer as evidence that the mechanism matters; strengthen an existing pressure case or validation only when recurrence evidence justifies it. Do not create a duplicate mechanism.
3. **candidate-generic-gap** — the consumer exposed a failure class that can be stated without consumer-specific nouns/paths and the missing responsibility belongs to AAOP's orchestration/evidence/policy/integration layer.
4. **promoted-invariant** — a candidate generic gap has been implemented minimally, pressure-tested, proven project-independent, passed the existing production workflow set, and can be explained without making the original consumer a dependency.

If classification is uncertain, keep the finding outside Core until the generic responsibility is defensible.

## Promotion criteria

Promote a real-project finding only when all applicable checks hold:

- **Real evidence exists.** The failure/near-miss or repaired behavior was observed in a real consumer, not invented only to justify a new feature.
- **The statement generalizes.** The failure can be described in project-independent engineering language without product names, domain actors, fixed paths, private infrastructure details, or consumer-specific status vocabulary.
- **AAOP owns the missing layer.** The gap concerns developer intake, route/evidence handling, source authority, coordination, autonomy, provider integration, execution continuity, acceptance/release truth, or another explicit AAOP responsibility.
- **No existing mechanism already closes it.** Search current policies, routes, pressure guards, Skills, Provider seams, and validations before creating a new concept.
- **The fix is the smallest reusable invariant.** Prefer strengthening an existing guard/policy over adding a new workflow engine, schema, state store, Provider, fixed team, or mandatory artifact.
- **Consumer authority stays local.** AAOP must not absorb project product truth, branding, domain rules, deployment facts, credentials, or project-owned state.
- **Pressure evidence is safe to retain.** Use public provenance when the source is public; otherwise anonymize the case and remove repository/reference identifiers and private data.
- **Regression exists.** A promoted invariant must have a source-level validation or pressure case that would fail if AAOP regressed to the observed failure mode.
- **Compatibility is proven.** The exact candidate must pass the existing AAOP production workflow set, including downstream/consumer compatibility where applicable.

## Feedback loop

```text
real consumer work
  -> observe failure / near-miss / successful repair
  -> classify consumer-only vs existing-AAOP-coverage vs candidate-generic-gap
  -> if candidate: generalize the invariant
  -> implement the smallest AAOP-owned change
  -> add/strengthen anonymized or public pressure evidence
  -> run exact-candidate production gates
  -> merge only when green
  -> continue the consumer project
  -> observe again
```

The loop is intentionally asymmetric: many consumer findings should **not** change AAOP.

## What must not be promoted

Do not promote merely because a pattern worked well in one project:

- product names, roles, vocabulary, UX flows, business rules, data models, or release numbers;
- a consumer's chosen status filename, script name, branch convention, hosting layout, or CI cost policy;
- one project's framework/database/agent preference;
- a local workaround for a provider or environment unless the generic blocker/capability distinction belongs in AAOP;
- a new AAOP state artifact when current project evidence, Journey state, or an existing Provider already supplies the needed continuity;
- a duplicate policy with a new name when an existing invariant already owns the failure class.

## Completion evidence for one promotion

A pressure promotion is complete when:

- the original consumer repair remains owned by the consumer;
- the AAOP change contains no dependency on that consumer;
- the generalized failure is represented by public/anonymized pressure evidence;
- the new/strengthened invariant is machine-guarded where practical;
- all AAOP production gates pass on the exact candidate;
- the consumer can continue development using AAOP without requiring AAOP to know its domain identity.

This is the intended path for AAOP to become production-tested: real projects repeatedly attack the protocol, while the promotion gate prevents those projects from colonizing the protocol.
