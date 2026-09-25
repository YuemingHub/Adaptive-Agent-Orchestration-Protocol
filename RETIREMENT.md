# Retirement / Research Status

> Effective: 2026-09-25
>
> AAOP is retained as public research/provenance. It is no longer an active YueMing runtime/protocol product line.

## Why

Issue #62 `Existence Gate — prove AAOP still adds control value over mature hosts` froze feature expansion and ran a bounded kill test.

Independent review found:

- Codex alone solved the bounded bug while Codex + AAOP added Working Contract ceremony and did not solve it in that run;
- Claude + AAOP produced the same useful fix behavior as Claude alone, with no observable task-level benefit from the large AAOP surface;
- Working Contract ceremony / route-registry-runtime machinery should retire from the active product path;
- cross-provider handoff and no-op honesty remain NOT PROVEN, not justification for ongoing platform development.

## What survives

Thin portable principles, only where useful:

- current repository reality outranks stale narrative;
- Human Authority remains human-owned;
- one accountable executor / bounded effect;
- implementation or Agent self-report != verified completion;
- verify the actual target/runtime;
- say NOT PROVEN / blocked when verification is unavailable;
- borrow mature capability before building.

For YueMing's own work, these principles now live primarily in `YuemingHub/agent-workspace` and real project repositories.

## Current default stack

Generic software-development machinery should be borrowed:

- current coding Agents such as Codex / Claude Code / future stronger hosts;
- GitHub repository / Issue / PR / CI truth;
- mature Spec-driven development tooling such as GitHub Spec Kit where it helps;
- Agent.Space or another workspace only when a persistent shared workspace is useful.

AAOP is not required between those layers.

## Stable / installer status

The historical `stable` branch and bootstrap/install artifacts remain readable for reproducibility and provenance.

They are **frozen historical releases**, not the recommended YueMing path and not a promise of ongoing compatibility/support.

Do not create “AAOP Lite” as a replacement. If a future real gap reappears, start from that failure and first test host policy/config/project instructions.
