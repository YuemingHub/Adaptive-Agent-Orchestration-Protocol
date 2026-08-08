# Product Principle: Hide Orchestration, Not Engineering Rigor

AAOP is successful when a developer can use increasingly simple language while the system performs increasingly rigorous internal work.

The product should move toward this experience:

```text
User: “Here's my idea. Help me make it real.”
User: “Here's the repo. Continue it.”
User: “Login broke. Fix it.”
User: “Add this feature.”
```

The developer should not need to translate those requests into:

- agent topology;
- workflow selection;
- Skill names;
- MCP servers;
- runtime choices;
- framework setup;
- verification methodology.

Those are orchestration responsibilities.

## Complexity gradient

The system may grow internally only as reality demands:

```text
Natural language
→ local host capability
→ local Skills/tools
→ external integration
→ specialized runtime
→ governed workspace
```

The user-facing interaction should not grow at the same rate.

## Beginner-friendly does not mean beginner-grade

A new developer should be protected from unnecessary ecosystem complexity, not from evidence, testing, source control, rollback, or clear product decisions.

AAOP therefore hides *mechanism selection* while preserving *engineering accountability*.

## Core product test

Whenever AAOP adds a concept, file, provider, route, or workflow, ask:

> Does this reduce the amount of orchestration the developer must understand or perform for a real task?

If not, it is likely internal complexity without user value.