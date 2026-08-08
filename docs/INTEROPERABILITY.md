# Interoperability Notes

Last reviewed: 2026-08-08

AAOP keeps host-specific behavior in adapters because AI IDE capabilities and configuration formats change faster than the core orchestration concepts.

## Agent Skills

AAOP canonical Skills follow the Agent Skills specification:

- Specification: https://agentskills.io/specification
- Core shape: a skill directory containing `SKILL.md` with YAML frontmatter (`name`, `description`) plus Markdown instructions.
- Optional skill resources can include scripts, references and assets.
- Progressive disclosure is intentional: discover metadata first, load full instructions when relevant.

AAOP's zero-dependency validator checks the portable naming/metadata constraints most important for these core Skills. A host may apply stricter or extended fields.

## Model Context Protocol

AAOP treats MCP as a provider of external tools/context, not as a methodology layer.

- Official MCP Registry: https://registry.modelcontextprotocol.io/
- Registry API/reference: https://registry.modelcontextprotocol.io/docs

A registry listing is useful for discovery but is not treated as a blanket security endorsement. `.aaop/policies/mcp-and-tools.md` still requires provenance and permission review.

## OpenAI Codex

AAOP uses `AGENTS.md` as the durable repository bootstrap because Codex supports repository guidance through `AGENTS.md`.

Reference:

- https://openai.com/index/introducing-codex/

Codex Skill/app availability can differ by product surface and workspace configuration; the adapter therefore requires runtime capability discovery rather than hard-coding a single installation path.

## Claude Code

Claude Code provides native project instructions, Skills, subagents, agent teams, permissions and MCP integration.

References:

- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/slash-commands
- Extension model overview: https://code.claude.com/docs/en/features-overview

Relevant mapping facts at the review date:

- project subagents can live under `.claude/agents/`;
- project Skills can live under `.claude/skills/`;
- subagents can have bounded tools, preloaded Skills and selected MCP servers;
- isolated subagents are distinct from agent teams that coordinate with one another.

AAOP uses these features opportunistically; they are not protocol requirements.

## Cursor

Cursor supports project rules and root agent instruction files, plus MCP configuration.

References:

- Rules: https://docs.cursor.com/context/rules-for-ai
- MCP: https://docs.cursor.com/context/model-context-protocol
- CLI behavior: https://docs.cursor.com/en/cli/using

Relevant mapping facts at the review date:

- project rules can live under `.cursor/rules/`;
- root `AGENTS.md` is supported as project guidance;
- Cursor CLI also reads root `AGENTS.md` / `CLAUDE.md`;
- project MCP configuration can live in `.cursor/mcp.json`;
- external tool permissions still need to be evaluated independently of protocol instructions.

## Drift policy

When a host changes:

1. update only the corresponding adapter and this interoperability note where possible;
2. change `.aaop/ORCHESTRATOR.md` only if the underlying host-neutral orchestration concept has changed;
3. prefer current official documentation over remembered configuration syntax;
4. keep examples credential-free and avoid committing real MCP secrets.
