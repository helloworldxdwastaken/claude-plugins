# Project memory

This repo records its durable knowledge in `PROJECT_MEMORY.md` at the repo root (git worktree root, else current working directory). Treat it as authoritative context for this project — you do not need it re-explained.

Capture durable facts as you go: the moment you learn something durable about THIS project (architecture, build/run/deploy, a gotcha, a decision, a convention, a non-obvious file location), record it immediately with the `memo` skill — don't wait to be asked or batch it to the end of the session. Keep entries terse and deduped. Never put project facts in personal/global memory; never record secrets.

- **If `PROJECT_MEMORY.md` exists:** read it with the Read tool before doing project work. If it is large (> 8 KB), still read it — it holds authoritative project knowledge.
- **If it does not exist:** one-line nudge to the user — run the `memo` skill (e.g. `memo "first fact"`) to start recording durable project facts, so future sessions don't need re-explaining. Silence the nudge with `PROJECT_MEMORY_NUDGE=0` (optional).