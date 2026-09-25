> ⚠️ **FROZEN HISTORICAL RELEASE · 2026-09-25**
>
> This `stable` branch is preserved for reproducibility/provenance. AAOP is no longer an active YueMing runtime/protocol development line.
>
> Do not treat this branch as the recommended current YueMing software-development control plane. Current work should prefer mature coding Agents + GitHub / Spec-driven tooling, with YueMing-specific authority/evidence rules kept thin in `YuemingHub/agent-workspace`.
>
> Existing bootstrap/install artifacts remain available so old experiments can be reproduced, not as a promise of ongoing support or compatibility.

---

# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, human-agent working contract, routing, evidence, decision, policy, and integration layer** for AI-assisted software work.

The intended experience is simple:

> Open a project, speak in ordinary language, let AAOP understand the project/idea and resolve what it can itself, confirm your collaboration style once, then let the Agent carry the engineering process through verified delivery.

AAOP is **not** another agent runtime, package manager, workflow engine, or multi-agent framework.

## Use AAOP now

### 1. Open a terminal in your project

For normal/production use, install from the deliberately promoted `stable` channel rather than the fast-moving `main` development branch.

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target .
```

**Windows PowerShell**

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target .
```

If your Windows Python command is `python`, replace `py` with `python`.

The stable bootstrap downloads the AAOP archive from the same deliberately promoted channel into a temporary directory, validates compressed and expanded archive resource limits plus path safety, delegates all project mutation to the canonical state-preserving installer, then runs a readiness check. It installs no third-party provider and asks for no secret.

If you prefer to inspect the stable bootstrap before running it:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py -o aaop-bootstrap.py
python3 aaop-bootstrap.py --target .
```

### Exact-revision installation

`stable` is a release channel: it changes only when a candidate has passed the release gates, but it is intentionally movable. When the exact source revision must be reproducible, resolve and use one commit SHA for **both** the bootstrap script and package archive:

```bash
AAOP_REF=<validated-commit-sha>
curl -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/${AAOP_REF}/scripts/bootstrap.py" | python3 - --target . --ref "${AAOP_REF}"
```

PowerShell:

```powershell
$AAOP_REF = '<validated-commit-sha>'
curl.exe -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/$AAOP_REF/scripts/bootstrap.py" | py - --target . --ref $AAOP_REF
```

Using the same commit for both steps prevents a bootstrap from one revision from silently installing a package from another.

### Development / edge channel

`main` is the development channel. Opt into it explicitly only when testing unreleased AAOP changes:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target . --ref main
```

Do not use `main` merely because it is newer. A consumer should upgrade because a concrete compatibility, safety, or capability delta justifies the change.

### 2. Confirm that the project is ready

```bash
python .aaop/tools/aaop.py ready .
```

A usable installation prints:

```text
AAOP READY
  version: ...
  project: ...
  health: healthy
  working contract: ...
  ...
```

The same command also gives you a starter prompt.

For an installation whose bootstrap provenance is `official-ref@stable`, a non-trivial takeover also checks whether that internally healthy package is still the current deliberately promoted stable control plane:

```bash
python .aaop/tools/source_freshness.py --json
```

`current` means the local package release identity matches official `stable`. `stale` means reuse the canonical stable bootstrap above, which preserves AAOP runtime/project-owned state, then rerun project compatibility evidence before trusting takeover/no-op/completion semantics. Network/source failure is `unknown`, not proof of either freshness or staleness. Exact/pinned/local sources are preserved rather than silently moved to `stable`.

### 3. Open the project in Codex, Claude Code, Cursor, or another host that reads project instructions

Then speak normally. A recommended first sentence is:

```text
Take responsibility for this project from the current evidence. First understand the project and reconcile AAOP continuity state. If my autonomous/collaborative working mode is not already established, ask me that one question once. Resolve everything the repository or your engineering judgment can resolve without asking me, ask only for genuinely human-owned product/domain decisions or authorization, then continue through implementation and verification without making me schedule the engineering process.
```

Once the Working Contract is established, a later session can be as short as:

```text
Continue.
```

Or give AAOP a concrete task:

```text
Login returns 500. Fix it and verify the regression.
```

```text
This repository is messy. Understand the current state and continue the most important existing work without rewriting things for appearance.
```

```text
Review this PR and tell me whether it is safe to merge. Do not change code unless I ask.
```

```text
Add family invitations while preserving the existing product rules and tests.
```

For a broad novice goal, ordinary language is enough too:

```text
I have an idea for an app. Help me think it through, ask only what I truly need to decide, then turn it into a real verified release.
```

AAOP first establishes/reuses the **Human-Agent Working Contract**: autonomous vs collaborative mode, aligned outcome, success evidence, and decision ownership. It then keeps one current Route at a time. A broad idea-to-production goal uses the end-to-end Delivery Journey only to preserve continuity across Route transitions; it does not create a seventh Route or a second workflow engine.

On a later session, the user may simply say `continue`, `keep going`, or `what next?`. Existing Working Contract + Journey checkpoints are continuity evidence. Developer intake reconciles them against current project/runtime/target facts rather than restarting discovery from the short new message or blindly trusting stale saved state.

## What happens internally

```text
Natural-language request
        ↓
Developer Intake + project evidence
        ↓
Human-Agent Working Contract
  evidence-resolvable → Agent inspects
  expert-decidable    → Agent/CTO decides
  human-owned         → ask only this
        ↓
Alignment Gate
        ↓
One primary Route
        ↓
Minimum sufficient project evidence
        ↓
Desired outcome vs current evidence
        ↓
Proven execution delta?
  yes → smallest coherent change
  no  → scope-level verified no-op / correct blocker
        ↓
Reconcile current project frontier before project-level no-op/pause
        ↓
One Agent by default
  justified specialization → bounded Task Pod (1–5, one accountable owner)
        ↓
Use existing capability first
        ↓
Only a real capability gap may justify a Provider
        ↓
Resolve explicit write target
        ↓
Execute conditionally → verify destination + outcome
        ↓
Handoff to next bounded Pod when responsibility materially changes
        ↓
Reroute if evidence changes
```

Current primary routes:

| Situation | Route |
| --- | --- |
| idea / no trustworthy implementation | `idea-to-build` |
| messy or contradictory repository | `repo-recovery` |
| error / regression / failure | `bug-fix` |
| new or changed behavior | `feature-change` |
| explanation / review / adoption decision | `understand-review` |
| deploy / release / migration / incident | `release-operations` |

You do **not** choose the route, Agent count, Skill, MCP server, runtime, framework, database, or workflow engine yourself.

For a multi-route product goal, `.aaop/skills/end-to-end-delivery/SKILL.md` coordinates these existing Routes. A lightweight checkpoint under `.aaop/runtime/journeys/` preserves long-horizon continuity. `.aaop/runtime/working-contract.json` separately preserves the human/agent collaboration and alignment contract. Current repository/runtime/target evidence remains authoritative over both.

## One user command surface

After installation, the main human-facing command is:

```bash
python .aaop/tools/aaop.py <command>
```

Useful commands:

```bash
python .aaop/tools/aaop.py ready .
python .aaop/tools/aaop.py status .
python .aaop/tools/aaop.py doctor .
python .aaop/tools/aaop.py prompt
python .aaop/tools/aaop.py version
python .aaop/tools/source_freshness.py --json
```

Lower-level tools such as `health.py`, `doctor.py`, `source_freshness.py`, `route.py`, `recipe.py`, `journey.py`, `working_contract.py`, and `instructions.py` remain available for orchestration and debugging, but a normal user should not need to memorize them.

## Human-Agent Working Contract

The Working Contract prevents both under-autonomy and over-autonomy.

- **Autonomous delivery** — after alignment, ordinary reversible engineering continues without repeatedly asking the human to approve steps.
- **Collaborative delivery** — implementation still belongs to the Agent, but material product/architecture tradeoffs are surfaced at meaningful checkpoints.