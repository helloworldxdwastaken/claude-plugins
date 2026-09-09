// project-memory — compaction re-injection.
//
// The global AGENTS.md directive tells the agent to read PROJECT_MEMORY.md and
// capture durable facts. On session compaction the directive stays in context,
// but the earlier memory content may be dropped — so re-inject the standing
// directive after compaction to restore the capture behavior.
//
// Faithful port of the Claude Code plugin's SessionStart hook (compact event).
// opencode has no `clear` event; compaction is the equivalent case.
export const ProjectMemory = async () => {
  return {
    "experimental.session.compacting": async (_input, output) => {
      output.context.push(`## Project memory

This repo records its durable knowledge in PROJECT_MEMORY.md at the repo root (git worktree root, else current working directory). Treat it as authoritative context for this project.

Capture durable facts as you go: the moment you learn something durable about THIS project (architecture, build/run/deploy, a gotcha, a decision, a convention, a non-obvious file location), record it immediately with the \`memo\` skill — don't wait to be asked or batch it to the end of the session. Keep entries terse and deduped. Never put project facts in personal/global memory; never record secrets.

- If PROJECT_MEMORY.md exists: read it with the Read tool before doing project work.
- If it does not exist: one-line nudge to the user — run the \`memo\` skill to start recording durable project facts.`)
    },
  }
}