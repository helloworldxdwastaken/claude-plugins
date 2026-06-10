# tokyo — Claude Code plugins

A small Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugins.md).

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

## Layout

```
.claude-plugin/marketplace.json        # this marketplace
plugins/project-memory/
├── .claude-plugin/plugin.json
├── skills/memo/SKILL.md               # /project-memory:memo
└── hooks/
    ├── hooks.json                     # SessionStart (startup|compact|clear) → session-start.sh
    └── session-start.sh
```

## License

MIT — see [LICENSE](LICENSE).
