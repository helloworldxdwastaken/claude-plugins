# Project memory for Codex

The `memo` skill maintains the same `PROJECT_MEMORY.md` used by the Claude Code
and OpenCode versions. Existing Markdown files, custom headings, and linked
notes work without migration.

## Install locally

From the root of this repository, copy the skill into Codex's user skill directory:

```sh
mkdir -p ~/.agents/skills/memo
cp codex/skills/memo/SKILL.md ~/.agents/skills/memo/SKILL.md
```

If a `memo` skill already exists there, review it before replacing it.
For one project instead, copy the skill to `<project>/.agents/skills/memo/SKILL.md`.
Choose one scope to avoid duplicate skills named `memo`.

To load project memory before work, merge the contents of `codex/AGENTS.md` into
`$CODEX_HOME/AGENTS.md` (or `~/.codex/AGENTS.md` when `CODEX_HOME` is unset), or
into the target project's root `AGENTS.md`. Preserve existing instructions.
If `AGENTS.override.md` exists at that scope, merge into the active override:
Codex uses it instead of `AGENTS.md`.

Start a new Codex chat after changing instructions. Invoke `$memo remember that
we run the integration suite with ...`, or ask it to remember a project fact.
The skill can also capture confirmed durable facts during normal work.
Verify in a new chat by asking Codex to identify the memory path and summarize
one existing entry. With no memory file, ask it to save a fact, then inspect
`PROJECT_MEMORY.md` at the worktree root.

## Behavior

The skill corrects or removes stale facts, deduplicates by meaning, and skips
speculation, temporary progress, and secrets. Current user instructions and
verified repository evidence take precedence over old notes. Larger files can
keep an overview and link to details under `project-memory/`.

This port uses a skill and `AGENTS.md` guidance; it does not install the Claude
SessionStart hook or the OpenCode re-injection plugin. After compaction, the
guidance tells Codex to re-read the overview if needed; this is agent behavior,
not a separate hook guaranteeing re-injection.

See the official OpenAI documentation for [skills](https://developers.openai.com/codex/build-skills)
and [AGENTS.md](https://developers.openai.com/codex/agent-configuration/agents-md).
