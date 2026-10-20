# opencode — plugins ported from Claude Code

Ports of the Claude Code plugins in the parent directory for [opencode](https://opencode.ai).

- **`memo`** (from `project-memory`) — keep durable project knowledge **in the repo** (`PROJECT_MEMORY.md`), auto-loaded into every opencode session, captured with one command — so you never re-explain a project's history. Works in **any** repo, on **any** machine. Install once.
- **`code-to-lottie`** — convert tagged SVG + CSS-keyframe animations into true-vector Lottie JSON (bodymovin) with three-stage verification (keyframe timing, geometry round-trip, ≥99% browser pixel-diff). Port of the Claude Code plugin of the same name; identical pipeline, same scripts.

Claude Code users: see the parent directory's plugin (`.claude-plugin/` + `plugins/project-memory/`) and install via `/plugin marketplace add helloworldxdwastaken/claude-plugins`.

## What it does

- **`memo` skill** — save or correct a durable fact (architecture, build/run/deploy steps, gotchas, decisions, conventions) to this repo's `PROJECT_MEMORY.md`, creating the file from a template if it doesn't exist. Corrects stale entries, removes confirmed obsolete facts, and de-duplicates by meaning. Skips temporary progress, speculation, and secrets; keeps project facts out of personal/global memory.
- **`code-to-lottie` skill** — SVG + CSS keyframes → Lottie JSON, with verification baked in. Scripts ship with the skill (`scripts/svg2lottie.py`, `scripts/verify_lottie.py`); the SKILL.md is the full pipeline contract.
- **Global `AGENTS.md` directive** — at the start of each session, the agent is told that if the repo has a `PROJECT_MEMORY.md` it must read it as maintained notes, with current user instructions and verified repository evidence taking precedence, and to capture durable facts as it goes. No `PROJECT_MEMORY.md`? You get a one-line nudge to create one (silence with `PROJECT_MEMORY_NUDGE=0`).
- **Directive re-injection plugin** *(optional, OpenCode V2)* — injects the
  capture directive into the system context of **every agent model request**
  through the V2 `session.hook("context")` API, so it always survives session
  compaction (stronger than re-adding it once after a compact). Requires
  OpenCode V2's plugin API; V1 named-export plugins do not load in V2.

## Install (per machine)

```bash
# 1. Skill — the `memo` capture command
mkdir -p ~/.config/opencode/skills/memo
cp skills/memo/SKILL.md ~/.config/opencode/skills/memo/SKILL.md

# 1b. Skill — `code-to-lottie` (SKILL.md + python scripts)
mkdir -p ~/.config/opencode/skills/code-to-lottie
cp -R skills/code-to-lottie/. ~/.config/opencode/skills/code-to-lottie/

# 2. Global directive — auto-loads every session, any repo
#    (if ~/.config/opencode/AGENTS.md already exists, merge the contents manually)
cp AGENTS.md ~/.config/opencode/AGENTS.md

# 3. Optional — directive re-injection (OpenCode V2 plugin API)
npm install --prefix ~/.config/opencode @opencode/plugin
mkdir -p ~/.config/opencode/plugins
cp plugin/project-memory.ts ~/.config/opencode/plugins/project-memory.ts
```

Restart opencode (config loads at session start). Verify: run
`grep "project-memory" ~/.local/share/opencode/log/opencode.log` — you should
see `msg="loading plugin" id=…/plugins/project-memory.ts` and **no**
`failed to load plugin` warnings. Verify with `opencode run "list your
available skills and quote your AGENTS.md directives"` from any repo.

## Use

- **New project:** run the `memo` skill (e.g. "memo first fact") — it scaffolds `PROJECT_MEMORY.md` and records the fact.
- **Thereafter:** "memo ..." whenever something durable is learned. Commit `PROJECT_MEMORY.md` along with your code so the memory travels with the repo.

## Notes

- `PROJECT_MEMORY.md` is committed to your repo — **never put secrets/keys in it**.
- Existing `PROJECT_MEMORY.md` files and custom headings work without migration. Above roughly 8 KB, keep an overview and move useful long details to linked Markdown files under `project-memory/` when needed.
- The global `AGENTS.md` is conditional: it only reads/creates the memory when the repo has (or needs) one. No repo changes required.
- Differences from the Claude Code original: no `/plugin` marketplace install (manual copy instead), no `/clear` re-injection (opencode has no `clear` event), and the directive is always present rather than injected by a shell hook.
