# project-memory plugin — Project Memory

> Durable project knowledge lives here — not in any agent's personal/global memory.
> Agents: read this before working; append new durable facts via `/project-memory:memo`.
> One fact per bullet, keep it terse. No secrets (this file is committed).

## Architecture
- One GitHub repo `helloworldxdwastaken/claude-plugins` is BOTH a Claude Code plugin **marketplace** AND hosts the `project-memory` **plugin**.
- Marketplace manifest: `.claude-plugin/marketplace.json` (marketplace name: **`tokyo`**, renamed from `wasta` 2026-06-10).
- Plugin lives in `plugins/project-memory/`: manifest `.claude-plugin/plugin.json`; skill `skills/memo/SKILL.md` (invoked **`/project-memory:memo`**); SessionStart hook `hooks/hooks.json` → `hooks/session-start.sh`.
- The hook resolves the Git worktree root and injects `PROJECT_MEMORY.md` (up to 8 KB) plus a capture/correction directive. Current instructions and verified repository evidence take precedence over stale notes. Fires on `startup|compact|clear` (v1.1.0): re-injects after compaction/`/clear` so a long auto-compacted session doesn't lose the memory or the capture directive; excludes `resume` to avoid repetition when context is retained. Silent (one-line nudge) when the file is absent; nudge silenceable with `PROJECT_MEMORY_NUDGE=0`. Inlines the file only when ≤ 8 KB, else points to it.
- Local working copy (verified 2026-10-20): `/Users/enmanuel/Desktop/Desktop/claude-plugins`.
- OpenCode port: `opencode/skills/memo/SKILL.md`, `opencode/AGENTS.md`, and optional V2 directive re-injection plugin `opencode/plugin/project-memory.ts`. Codex port: `codex/skills/memo/SKILL.md` and `codex/AGENTS.md`; install instructions in `codex/README.md`. All use the same Markdown memory format without migration.

## Build / Run / Deploy
- No build step. Hook regression checks: `python3 -m unittest discover -s tests -v`; shell syntax: `bash -n plugins/project-memory/hooks/session-start.sh`.
- **Standing rule (per user, 2026-06-10):** after ANY plugin change, bump `version` in BOTH `marketplace.json` and `plugins/project-memory/.claude-plugin/plugin.json`, then commit and **push to `origin`** — don't wait to be asked. (Docs/PROJECT_MEMORY-only edits: still push, but no version bump.)
- Install per machine — **in the Claude Code chat input, NOT a terminal**: `/plugin marketplace add helloworldxdwastaken/claude-plugins` → `/plugin install project-memory@tokyo` → `/reload-plugins`. Updates: `/plugin marketplace update tokyo`, or the auto-update toggle in the `/plugin` UI.

## Gotchas / lessons learned
- Plugin skills are **always namespaced** → the command is `/project-memory:memo`; a bare `/memo` is impossible from a plugin.
- Plugins **cannot auto-load a CLAUDE.md rule** — the "always read PROJECT_MEMORY.md" behavior is delivered by the SessionStart hook (its stdout is injected into context).
- `/plugin` commands run in the Claude Code chat input, not the zsh terminal (running them in zsh errors with "no such file or directory").
- Hook paths: `${CLAUDE_PLUGIN_ROOT}` = the plugin's install dir; `$CLAUDE_PROJECT_DIR` = the current repo root.

## Log
- 2026-06-10 — v1.0.0 scaffolded, validated, and pushed public to `helloworldxdwastaken/claude-plugins`. Local copy moved to `~/Desktop/claude-plugins` to develop separately from Asta. Added this PROJECT_MEMORY.md (dogfooding).
- 2026-06-10 — marketplace renamed `wasta` → `tokyo`.
- 2026-06-10 — v1.1.0: SessionStart hook broadened to `startup|compact|clear` (re-injects memory + capture directive after compaction/`/clear`); strengthened "capture as you go" directive in `session-start.sh`; sharpened `/project-memory:memo` skill description toward proactive capture. Rejected a background-LLM auto-capture design (would pollute the committed/auto-injected file, risk 8 KB bloat + unreviewed/secret writes + invisible cost); chose model-driven in-session capture instead.
- 2026-10-20 — v1.3.0: aligned Claude/OpenCode memory maintenance, added Codex port, corrected Git-root discovery, preserved legacy Markdown and commands, and added isolated hook regression checks.
