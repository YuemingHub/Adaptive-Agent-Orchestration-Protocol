# AAOP Quick Start

This guide is for a developer who wants to **use AAOP now**, not study the whole protocol first.

## 1. Install AAOP into the project you want to work on

Open a terminal in that project. Normal/production use follows the deliberately promoted `stable` channel, not the fast-moving `main` development branch.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target .
```

### Windows PowerShell

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target .
```

If your Python command is `python`, use it instead of `py` / `python3`.

The bootstrap:

- downloads the AAOP repository archive for the selected ref into a temporary directory;
- rejects unsafe paths, encrypted members, excessive archive member counts, excessive per-member expanded size, and excessive total expanded size before extraction;
- validates that the archive contains a recognizable AAOP source package;
- uses the canonical `scripts/install.py` for all target mutation;
- preserves unrelated project rules in `AGENTS.md` / `CLAUDE.md`;
- writes AAOP under `.aaop/` and records ownership in `.aaop/.install-manifest.json`;
- installs no third-party provider;
- requests no secret;
- runs a readiness check after installation.

### Inspect-first option

If you do not want to pipe a remote script directly into Python:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py -o aaop-bootstrap.py
python3 aaop-bootstrap.py --target .
```

Review the downloaded file before executing it.

### Pin an exact revision

`stable` is a deliberately promoted release channel and may move when a new candidate passes all release gates. For immutable revision reproducibility, use the same exact commit for both the bootstrap script and archive:

```bash
AAOP_REF=<validated-commit-sha>
curl -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/${AAOP_REF}/scripts/bootstrap.py" | python3 - --target . --ref "${AAOP_REF}"
```

PowerShell:

```powershell
$AAOP_REF = '<validated-commit-sha>'
curl.exe -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/$AAOP_REF/scripts/bootstrap.py" | py - --target . --ref $AAOP_REF
```

### Opt into development / edge

`main` is not the production default. Use it explicitly only when testing unreleased AAOP changes:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target . --ref main
```

## 2. Confirm AAOP is ready

```bash
python .aaop/tools/aaop.py ready .
```

A normal installed project should report:

```text
AAOP READY
  version: <installed version>
  project: <your project>
  health: healthy
```

The readiness command also summarizes visible project evidence and prints a starter prompt.

If it says `REVIEW REQUIRED`, follow the `Next:` line instead of blindly reinstalling.

## 3. Open the project in your normal AI coding host

AAOP is designed to enter through project instruction surfaces your host already understands.

Supported target shapes include:

- Codex → `AGENTS.md` and scoped project rules;
- Claude Code → `CLAUDE.md` plus project rules;
- Cursor → root project instructions and relevant scoped rules;
- other coding agents that can read project files/instructions → generic AAOP bootstrap path.

You do not select an “AAOP mode.”

## 4. Say what you want in ordinary language

A broad continuation prompt:

```text
Understand this project and its current rules, determine the highest-value current executable step toward my goal, and continue autonomously. Reuse what already exists, preserve project intent, make ordinary engineering decisions yourself, verify the result, and ask only for genuinely missing authorization, credentials, or material product decisions.
```

Concrete tasks are better when you have one:

```text
Login returns 500. Fix it and verify the regression.
```

```text
Add family invitations while preserving the existing product rules and tests.
```

```text
This repository is messy. Reconstruct the current state, identify the real next executable work, and continue without cosmetic rewrites.
```

```text
Review this change and tell me whether it is safe to merge. Stay read-only unless I ask for implementation.
```

You do **not** need to tell AAOP which Agent, Skill, MCP server, runtime, framework, or team topology to use.

## 5. The one user CLI

Normal human-facing commands use:

```bash
python .aaop/tools/aaop.py <command>
```

### Readiness

```bash
python .aaop/tools/aaop.py ready .
```

### Installation health

```bash
python .aaop/tools/aaop.py status .
```

### Environment/project evidence

```bash
python .aaop/tools/aaop.py doctor .
```

For one known route:

```bash
python .aaop/tools/aaop.py doctor . --route feature-change
```

### Starter prompt

```bash
python .aaop/tools/aaop.py prompt
```

### Version

```bash
python .aaop/tools/aaop.py version
```

Lower-level tools remain available under `.aaop/tools/`, but ordinary use should not require memorizing them.

## 6. What the agent should do after your request

Internally, expect approximately this reasoning shape:

```text
your request
→ understand current project/rules
→ select one primary route
→ read only enough evidence for the current decision
→ compare desired outcome with current state
→ prove whether a real execution delta exists
→ reuse current capabilities
→ add a provider only for a real capability gap
→ execute
→ revalidate the target before consequential write/merge
→ verify
→ reroute/replan if evidence changes the problem
```

Important consequences:

- “continue” does not mean “manufacture a diff”;
- finding a fix does not authorize mutation during a read-only review;
- a referenced repository does not automatically become a mutation target;
- a stale write precondition means re-read/reconcile, not force overwrite;
- a network/credential/product-decision blocker is not automatically a capability gap;
- a detected provider is not automatically needed.

## 7. Upgrade

Run the current **stable bootstrap command** again.

The `stable` branch moves only after a release candidate passes the required release gates; ordinary `main` commits therefore do not silently change the production install path. A consumer pinned to an exact commit remains pinned until that exact revision is deliberately changed.

The bootstrap recognizes an existing AAOP installation and delegates to safe `--upgrade` behavior.

Upgrade preserves:

- `.aaop/runtime/`;
- project-owned files under `.aaop/`;
- project text outside AAOP markers in `AGENTS.md` / `CLAUDE.md`;
- local managed-file edits as backups before canonical replacement;
- third-party providers and project dependencies.

Install, upgrade, and uninstall are journaled lifecycle mutations. AAOP snapshots the package ownership surface and project bootstrap files before promotion, uses atomic per-file replacement, and rolls back caught failures. Malformed/duplicated AAOP marker pairs and unsupported ownership metadata fail before destructive mutation.

### If install / upgrade / uninstall was interrupted

A process or machine can stop without giving AAOP a chance to roll back. To avoid treating a mixed package as healthy, AAOP leaves the project-root journal:

```text
.aaop-install-transaction/
```

While that journal exists:

- health reports `interrupted-install`;
- normal install / upgrade / uninstall refuses to continue;
- do **not** manually delete the journal or blindly reinstall over the package.

Recover with the same trusted release source you intend to use.

Stable channel, macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target . --recover-interrupted
```

Stable channel, Windows PowerShell:

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target . --recover-interrupted
```

For an exact-revision consumer, use that matching/newer trusted exact revision for both the bootstrap URL and `--ref`.

Recovery first preserves the interrupted current files, then restores the pre-transaction package / manifest / `AGENTS.md` / `CLAUDE.md` state. After recovery, run:

```bash
python .aaop/tools/aaop.py status .
python .aaop/tools/aaop.py ready .
```

Only retry the original lifecycle operation after health/readiness reflects the restored current state.

## 8. Remove AAOP

Use the stable bootstrap surface with `--uninstall`.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target . --uninstall
```

### Windows PowerShell

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target . --uninstall
```

Safe removal:

- removes only files listed as AAOP-owned in the install manifest;
- removes only marked AAOP blocks from `AGENTS.md` / `CLAUDE.md`;
- preserves text outside those markers;
- preserves `.aaop/runtime/`;
- preserves project-owned files under `.aaop/`;
- backs up modified managed files before removal;
- leaves Playwright, MCP servers, OpenHands, AutoAgent, Deep Agents, and other providers untouched;
- refuses automatic uninstall when ownership cannot be established safely;
- rejects future manifest schemas or unsafe managed paths instead of downgrade-managing unknown ownership metadata.

## 9. Health semantics

`aaop.py status` / `health.py` answer:

> Does this local AAOP package still match the baseline installed or upgraded here?

Typical states include:

```text
healthy
upgrade-recommended
legacy-install
drifted
incomplete
interrupted-install
invalid-manifest
unsupported-manifest
source-tree
```

`interrupted-install` takes precedence over ordinary package health. Recover the journaled lifecycle mutation before relying on the package or attempting another mutation.

Health is best-effort accidental-drift detection. It is **not**:

- a cryptographic trust root;
- a guarantee that your package is the latest upstream version;
- permission to overwrite local changes.

## 10. If a provider is genuinely needed

AAOP should first determine the missing **capability**, then check what is already present.

Only a real `capability-gap` directly justifies provider selection.

When an external provider is actually needed, AAOP should tell you:

- what capability is missing;
- why existing options are insufficient;
- which upstream provider/surface is recommended;
- minimum permissions required;
- credentials/cost/data exposure;
- current verification/adoption checks;
- rollback/removal path.

The user should not have to answer “Which MCP do you want?” as the first step.

## 11. Developing AAOP itself

Inside the AAOP source repository:

```bash
python scripts/validate.py
python scripts/validate_pressure.py
python scripts/validate_install_transaction.py
python .aaop/tools/aaop.py ready .
```

Source-tree readiness is valid but is different from a manifest-tracked installation.

The end-to-end usability gate additionally exercises bootstrap archive safety, injected lifecycle failures + rollback/recovery, install → READY → repeat upgrade → safe refusal of unrelated `.aaop` → manifest-scoped removal.

## Release channels

- `main`: development/edge.
- `stable`: deliberately promoted production channel.
- exact commit: immutable consumer pin when exact source identity is required.

A green `main` commit does not automatically promote `stable`.

## More detail

- `docs/DEVELOPER_ENTRYPOINT.md`
- `docs/ROUTE_CAPABILITY_PACKS.md`
- `docs/REAL_PROJECT_PRESSURE_TESTS.md`
- `docs/PROGRESSIVE_ADOPTION.md`
- `docs/HOST_BOOTSTRAP_CONFORMANCE.md`
- `docs/INSTRUCTION_TOPOLOGY.md`
- `docs/ECOSYSTEM_MAP.md`
