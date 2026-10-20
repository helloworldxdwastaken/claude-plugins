// project-memory — directive re-injection for OpenCode V2.
//
// The global AGENTS.md directive tells the agent to read PROJECT_MEMORY.md and
// capture durable facts. When a long session is compacted, the earlier memory
// content and directive can be dropped from the summarized context — so this
// plugin re-injects the standing directive, keeping the capture behavior alive
// even late in a session.
//
// OpenCode V2 plugin API (V1 named-export plugins do not load in V2):
// a default export via Plugin.define with a stable id and a setup(ctx).
// The V1 `experimental.session.compacting` event maps to the V2 session hooks
// (see the V1→V2 plugin migration guide). We register the `context` hook,
// which runs immediately before every agent model request and lets us edit
// `event.system` — so the directive is present on every model call and
// therefore always survives compaction, instead of being re-added once
// afterwards. Port of the Claude Code plugin's SessionStart hook.
import { Plugin } from "@opencode/plugin"

const DIRECTIVE = `## Project memory

This repo records its durable knowledge in PROJECT_MEMORY.md at the repo root (git worktree root, else current working directory). Treat it as authoritative context for this project.

Capture durable facts as you go: the moment you learn something durable about THIS project (architecture, build/run/deploy, a gotcha, a decision, a convention, a non-obvious file location), record it immediately with the \`memo\` skill — don't wait to be asked or batch it to the end of the session. Keep entries terse and deduped. Never put project facts in personal/global memory; never record secrets.

- If PROJECT_MEMORY.md exists: read it with the Read tool before doing project work.
- If it does not exist: one-line nudge to the user — run the \`memo\` skill to start recording durable project facts.`

export default Plugin.define({
  id: "project-memory",
  async setup(ctx) {
    await ctx.session.hook("context", (event) => {
      event.system.push({ type: "text", text: DIRECTIVE })
    })
  },
})
