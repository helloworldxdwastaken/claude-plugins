# opencode — project-memory

The `project-memory` plugin for [opencode](https://opencode.ai), ported from the Claude Code plugin in the parent directory. Keep durable project knowledge **in the repo** (`PROJECT_MEMORY.md`), auto-loaded into every opencode session, captured with one command — so you never re-explain a project's history. Works in **any** repo, on **any** machine. Install once.

Claude Code users: see the parent directory's plugin (`.claude-plugin/` + `plugins/project-memory/`) and install via `/plugin marketplace add helloworldxdwastaken/claude-plugins`.

## What it does

- **`memo` skill** — append a durable fact (architecture, build/run/deploy steps, gotchas, decisions, conventions) to this repo's `PROJECT_MEMORY.md`, creating the file from a template if it doesn't exist. De-duplicates, uses absolute dates, never writes to personal/global memory, never stores secrets.
- **Global `AGENTS.md` directive** — at the start of each session, the agent is told that if the repo has a `PROJECT_MEMORY.md` it must read it and treat it as authoritative, and to capture durable facts as it goes. No `PROJECT_MEMORY.md`? You get a one-line nudge to create one (silence with `PROJECT_MEMORY_NUDGE=0`).
- **Compaction re-injection plugin** *(optional)* — re-injects the capture directive after session compaction, so facts keep getting recorded even late in a long session. (The Claude Code original also fires on `/clear`; opencode has no `clear` event, so this covers compaction only.)

## Install (per machine)

```bash
# 1. Skill — the `memo` capture command
mkdir -p ~/.config/opencode/skills/memo
cp skills/memo/SKILL.md ~/.config/opencode/skills/memo/SKILL.md

# 2. Global directive — auto-loads every session, any repo
#    (if ~/.config/opencode/AGENTS.md already exists, merge the contents manually)
cp AGENTS.md ~/.config/opencode/AGENTS.md

# 3. Optional — compaction re-injection
mkdir -p ~/.config/opencode/plugins
cp plugin/project-memory.ts ~/.config/opencode/plugins/project-memory.ts
```

Restart opencode (config loads at session start). Verify with `opencode run "list your available skills and quote your AGENTS.md directives"` from any repo.

## Use

- **New project:** run the `memo` skill (e.g. "memo first fact") — it scaffolds `PROJECT_MEMORY.md` and records the fact.
- **Thereafter:** "memo ..." whenever something durable is learned. Commit `PROJECT_MEMORY.md` along with your code so the memory travels with the repo.

## Notes

- `PROJECT_MEMORY.md` is committed to your repo — **never put secrets/keys in it**.
- The global `AGENTS.md` is conditional: it only reads/creates the memory when the repo has (or needs) one. No repo changes required.
- Differences from the Claude Code original: no `/plugin` marketplace install (manual copy instead), no `/clear` re-injection (opencode has no `clear` event), and the directive is always present rather than injected by a shell hook.