# Codex Adapter

Purpose: map AAOP concepts onto Codex without making Codex-specific behavior part of the core protocol.

## Bootstrap

Codex supports repository `AGENTS.md` instructions. AAOP therefore uses root `AGENTS.md` as the primary Codex bootstrap.

For a task:

1. load the governing `AGENTS.md` instruction scope;
2. read `.aaop/ORCHESTRATOR.md` for non-trivial work;
3. load only the relevant `.aaop/skills/*/SKILL.md` files;
4. discover the actual tools/apps/skills exposed to the current Codex session before planning providers.

## Skills

AAOP Skills follow the open Agent Skills format. Codex Skill installation/discovery can vary by product surface and workspace configuration, so this repository does not assume a single global installation path.

Two valid modes:

- **Direct protocol mode:** `AGENTS.md` explicitly references the canonical `.aaop/skills/.../SKILL.md` paths and the agent reads them when relevant.
- **Native Skill mode:** install/copy the canonical Skills into the Skill location supported by the current Codex surface. Keep `.aaop/skills/` canonical; do not fork their meaning silently.

If native Skill discovery and repository instructions disagree, follow the actual capabilities presented by the current host session rather than assuming a Skill is installed.

## Subagents / parallel work

Do not require a particular Codex multi-agent primitive. Apply AAOP host degradation:

- use available task/agent/worktree/background primitives when they provide isolation or safe parallelism;
- otherwise keep a single orchestrator and execute ownership contexts sequentially;
- preserve an independent review pass even if implemented by the same underlying model in a fresh review context.

## Tools and apps

Treat every connected Codex app/tool as a provider in the capability matrix. Discover current availability first. Do not tell the user to install MCP if Codex already exposes an equivalent first-party/native connector.

## Repository guidance

Keep `AGENTS.md` concise enough to serve as persistent bootstrap context. Put procedures in Skills and normative orchestration behavior in `.aaop/ORCHESTRATOR.md` so they are loaded progressively.
