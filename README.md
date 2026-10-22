# tokyo — Claude Code plugins

A small Claude Code [plugin marketplace](https://code.claude.com/docs/en/plugins.md), with project-memory ports for OpenCode and Codex.

> **Using [opencode](https://opencode.ai)?** See [`opencode/`](opencode/) for a port of `project-memory` (global `memo` skill + `AGENTS.md` directive + optional compaction re-injection plugin).

> **Using Codex?** See [`codex/`](codex/) for the `memo` skill and `AGENTS.md` loading instructions.

## `project-memory`

Keep durable project knowledge **in the repo** (`PROJECT_MEMORY.md`), auto-loaded into every Claude Code
session, captured with one command — so you never re-explain a project's history. Works in **any** repo,
on **any** machine. Install once.

### What it does

- **`/project-memory:memo "<fact>"`** — saves or corrects a durable fact (architecture, build/run/deploy steps, gotchas,
  decisions, conventions) to this repo's `PROJECT_MEMORY.md`, creating the file from a template if it doesn't
  exist. Updates superseded entries, removes confirmed obsolete facts, de-duplicates by meaning, and skips temporary progress and speculation. Uses absolute dates when relevant; never writes project facts to personal/global memory or stores secrets.
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
- Existing `PROJECT_MEMORY.md` files and custom headings keep working without migration. Current user instructions and verified repository evidence take precedence over stale memory; recorded notes do not grant permission for external actions.
- The hook resolves the Git worktree root, including when started from a subfolder. Without Git, it uses `$CLAUDE_PROJECT_DIR` or the current directory.
- The hook inlines `PROJECT_MEMORY.md` only when it's ≤ 8 KB; larger files are pointed to for reading before project work. Keep an overview and, when useful, move long details to linked Markdown files under `project-memory/` without losing content.
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

## Reference video and audio skills

Added locally on 21 October 2026. The original three are now version 1.1.1; the two preparation/integration skills are version 1.0.1 and the coordinator is version 1.0.0.

| Skill | Recipe |
| --- | --- |
| [Casino Media Coordinator](plugins/casino-media-coordinator/skills/casino-media-coordinator/SKILL.md) | Read current project plan/memory, route work to the needed skills, assign owners/budgets and reconcile independent checks and handoffs. |
| [Genjutsu Video](plugins/genjutsu-video/skills/genjutsu-video/SKILL.md) | Recreate source performance using character/clothing/room images; inspect identity, garment features, layout, props and timing. Includes official Genjutsu mode guidance and qualified local casino recipes. |
| [Casino Voice Cloner](plugins/casino-voice-cloner/skills/casino-voice-cloner/SKILL.md) | Isolate original speech, level it, convert toward the authorized target voice and preserve source timing; compare words, voice and actual AV sync separately. |
| [Casino Continuity Inspector](plugins/casino-continuity-inspector/skills/casino-continuity-inspector/SKILL.md) | Independent final comparison and timestamped repair list, with explicit coverage and unverified checks. |
| [Source Timeline Mapper](plugins/source-timeline-mapper/skills/source-timeline-mapper/SKILL.md) | Exact source/shot/sample/trim maps and genuine handles, with a local map arithmetic/hash checker. |
| [Casino Media Integrator](plugins/casino-media-integrator/skills/casino-media-integrator/SKILL.md) | Isolated candidate assembly and admission checks for authoritative results, one voice, safe joins and actual player delivery. |

Canonical sources live in `plugins/<name>/skills/<name>/`. Codex can discover these through local symlinks in its active profile's `skills` directory; each includes `agents/openai.yaml` metadata. Start a new chat after installation and invoke `$casino-media-coordinator` for a multi-step task, or `$genjutsu-video`, `$casino-voice-cloner`, `$casino-continuity-inspector`, `$source-timeline-mapper` or `$casino-media-integrator` for a focused task. Claude plugin manifests and this local marketplace include all six; no public release is implied by these local files.

All six apply a two-pass recheck protocol: worker verification followed by a separate check of frozen final artifacts against raw evidence. Changed bytes/maps invalidate affected checks. Missing listening/viewing/runtime evidence stays unassessed; repeating the same command does not count as independent verification. At most two repair/recheck cycles are the default, within the existing task budget. Each skill bundles the protocol so it works independently when installed alone.

The coordinator uses available subagent tools and gives workers explicit skill paths, artifacts, ownership and evidence requirements. It respects current concurrency limits, project swarm roles and one shared cumulative budget. It chooses direct TTS or original-performance conversion according to the request; neither is an automatic substitute for the other. Missing delegation/tools are reported honestly, and creating/installing the coordinator does not run a media pipeline.

The mapper's `scripts/verify_timeline.py` validates a portable JSON export using exact rational arithmetic, native interval bounds, explicit speed, complete output coverage and actual file hashes. It does not certify decoded clocks, semantic correspondence or audiovisual sync. Run its regression checks with `python3 -m unittest discover -s tests -p test_timeline_mapper.py -v`; they include synthetic local media and invalidated-final-byte cases.

These are executable-agent recipes, not bundled video/voice models. They use available tools, verify actual inputs/outputs and report missing capabilities. No media, private source recordings, model weights, embeddings or credentials are included. Structural validation and scenario review do not establish successful new video generation, voice conversion or lip sync.

## License

MIT — see [LICENSE](LICENSE).
