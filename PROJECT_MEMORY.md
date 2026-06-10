# project-memory plugin — Project Memory

> Durable project knowledge lives here — not in any agent's personal/global memory.
> Agents: read this before working; append new durable facts via `/project-memory:memo`.
> One fact per bullet, keep it terse. No secrets (this file is committed).

## Architecture
- One GitHub repo `helloworldxdwastaken/claude-plugins` is BOTH a Claude Code plugin **marketplace** AND hosts the `project-memory` **plugin**.
- Marketplace manifest: `.claude-plugin/marketplace.json` (marketplace name: **`wasta`**).
- Plugin lives in `plugins/project-memory/`: manifest `.claude-plugin/plugin.json`; skill `skills/memo/SKILL.md` (invoked **`/project-memory:memo`**); SessionStart hook `hooks/hooks.json` → `hooks/session-start.sh`.
- The hook injects a repo's `PROJECT_MEMORY.md` into context at session `startup`. Silent (one-line nudge) when the file is absent; nudge silenceable with `PROJECT_MEMORY_NUDGE=0`. Inlines the file only when ≤ 8 KB, else points to it.
- Local working copy: `~/Desktop/claude-plugins` (moved here to keep it separate from the Asta repo).

## Build / Run / Deploy
- No build step — declarative: JSON manifests + a bash hook + a markdown skill.
- Release: bump `version` in BOTH `marketplace.json` and `plugins/project-memory/.claude-plugin/plugin.json`, commit, push to `origin` (already public via gh).
- Install per machine — **in the Claude Code chat input, NOT a terminal**: `/plugin marketplace add helloworldxdwastaken/claude-plugins` → `/plugin install project-memory@wasta` → `/reload-plugins`. Updates: `/plugin marketplace update wasta`, or the auto-update toggle in the `/plugin` UI.

## Gotchas / lessons learned
- Plugin skills are **always namespaced** → the command is `/project-memory:memo`; a bare `/memo` is impossible from a plugin.
- Plugins **cannot auto-load a CLAUDE.md rule** — the "always read PROJECT_MEMORY.md" behavior is delivered by the SessionStart hook (its stdout is injected into context).
- `/plugin` commands run in the Claude Code chat input, not the zsh terminal (running them in zsh errors with "no such file or directory").
- Hook paths: `${CLAUDE_PLUGIN_ROOT}` = the plugin's install dir; `$CLAUDE_PROJECT_DIR` = the current repo root.

## Log
- 2026-06-10 — v1.0.0 scaffolded, validated, and pushed public to `helloworldxdwastaken/claude-plugins`. Local copy moved to `~/Desktop/claude-plugins` to develop separately from Asta. Added this PROJECT_MEMORY.md (dogfooding).
