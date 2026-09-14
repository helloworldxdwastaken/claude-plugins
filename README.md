# tokyo — Claude Code plugins

A small Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugins.md).

> **Using [opencode](https://opencode.ai)?** See [`opencode/`](opencode/) for a port of `project-memory` (global `memo` skill + `AGENTS.md` directive + optional compaction re-injection plugin).

## `project-memory`

Keep durable project knowledge **in the repo** (`PROJECT_MEMORY.md`), auto-loaded into every Claude Code
session, captured with one command — so you never re-explain a project's history. Works in **any** repo,
on **any** machine. Install once.

### What it does

- **`/project-memory:memo "<fact>"`** — appends a durable fact (architecture, build/run/deploy steps, gotchas,
  decisions, conventions) to this repo's `PROJECT_MEMORY.md`, creating the file from a template if it doesn't
  exist. De-duplicates, uses absolute dates, never writes to personal/global memory, never stores secrets.
- **SessionStart hook** — at the start of each session, if the repo has a `PROJECT_MEMORY.md`, its contents
  (plus a directive to capture durable facts as you go) are injected into context automatically. It also
  **re-injects after a compaction or `/clear`**, so when a long session is auto-compacted the memory and the
  capture directive aren't lost — facts keep getting recorded even late in the session. No `PROJECT_MEMORY.md`?
  You get a one-line nudge to create one (silence it with `PROJECT_MEMORY_NUDGE=0`).

### Install (per machine)

```
/plugin marketplace add helloworldxdwastaken/claude-plugins
/plugin install project-memory@tokyo
/reload-plugins
```

To get updates automatically: in the `/plugin` UI → **Marketplaces** → `tokyo` → **Enable auto-update**.
(Or pull the latest manually with `/plugin marketplace update tokyo`.)

### Use

- **New project:** run `/project-memory:memo "first fact"` — it scaffolds `PROJECT_MEMORY.md` and records the fact.
- **Thereafter:** `/project-memory:memo "..."` whenever something durable is learned. Commit `PROJECT_MEMORY.md`
  along with your code so the memory travels with the repo.

### Notes

- `PROJECT_MEMORY.md` is committed to your repo — **never put secrets/keys in it**.
- The hook inlines `PROJECT_MEMORY.md` only when it's ≤ 8 KB; larger files are pointed to and read on demand.
- The hook fires on `startup`, `compact`, and `clear` — re-injecting after a compaction/`/clear` (which remove
  the earlier injection from context) but **not** on `resume` (where context is retained), so it restores lost
  memory without redundant mid-session repetition.

## `code-to-lottie`

Convert **coded animations** (tagged SVG + CSS `@keyframes`) into **true-vector Lottie JSON**
(bodymovin) — no After Effects — and *prove* the export matches the source before shipping.

### What it does

- **Pipeline skill** — tag each animated piece `class="lottie-part"` + `--i` stagger order,
  convert with `scripts/svg2lottie.py` (parses `@keyframes` opacity/scale/translate, easing,
  stagger; paths/rects/circles/ellipses/groups; `<text>` → real glyph outlines via fontTools).
- **Three-stage verification** — the skill refuses to call it done without:
  1. **timing** — keyframe times/values/easing re-parsed from the source CSS and diffed;
  2. **geometry** — sampled curve round-trip vs the source SVG (≤ 0.05px);
  3. **pixel diff** — self-contained `diff.html` (player + JSON inlined) rendered headless;
     ≥ 99% pixel match passes.
- Encodes the gotchas that silently break Lottie exports (relative tangents, anchor-relative
  vertices, loop-seam clamping, `file://` fetch, canvas renderer sizing).

### Install

```
/plugin marketplace add helloworldxdwastaken/claude-plugins
/plugin install code-to-lottie@tokyo
```

Then: *"export this animation as a lottie"* / *"convert this svg loader to lottie"* — the skill
triggers on the task and runs the pipeline + verification itself.

## Layout

```
.claude-plugin/marketplace.json        # this marketplace
plugins/project-memory/
├── .claude-plugin/plugin.json
├── skills/memo/SKILL.md               # /project-memory:memo
└── hooks/
    ├── hooks.json                     # SessionStart (startup|compact|clear) → session-start.sh
    └── session-start.sh
plugins/code-to-lottie/
├── .claude-plugin/plugin.json
└── skills/code-to-lottie/
    ├── SKILL.md                       # pipeline + verification protocol
    └── scripts/
        ├── svg2lottie.py              # tagged SVG + CSS keyframes → Lottie JSON
        └── verify_lottie.py           # timing + geometry + pixel-diff verification
```

## License

MIT — see [LICENSE](LICENSE).
