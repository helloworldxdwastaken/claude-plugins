#!/usr/bin/env bash
# project-memory — SessionStart hook.
#
# If the current repo has a PROJECT_MEMORY.md, inject it (plus the standing
# capture directive) into the session context — so the agent treats the
# project's recorded knowledge as authoritative and never needs it re-explained.
# Fires on `startup`, `compact`, and `clear` (see hooks.json): on compact/clear
# the prior injection has been removed from context, so re-injecting restores
# both the memory and the capture directive (it is not redundant repetition).
# If there's no PROJECT_MEMORY.md, print a single-line opt-in nudge (silence with
# PROJECT_MEMORY_NUDGE=0). Everything this prints to stdout is added to context.
#
# No `set -e`: a failed wc/cat must never abort the session.
set -uo pipefail

DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
FILE="$DIR/PROJECT_MEMORY.md"

if [ -f "$FILE" ]; then
  echo "# Project memory"
  echo
  echo "This repo records its durable knowledge in PROJECT_MEMORY.md. Treat it as authoritative context for this project — you do not need it re-explained."
  echo "Capture durable facts as you go: the moment you learn something durable about THIS project (architecture, build/run/deploy, a gotcha, a decision, a convention, a non-obvious file location), record it immediately with the \`/project-memory:memo\` skill — don't wait to be asked or batch it to the end of the session. Keep entries terse and deduped. Never put project facts in personal/global memory; never record secrets."
  echo

  bytes=$(wc -c < "$FILE" 2>/dev/null | tr -d ' ')
  if [ -n "${bytes:-}" ] && [ "$bytes" -le 8192 ]; then
    echo "Current contents of PROJECT_MEMORY.md:"
    echo
    echo '<PROJECT_MEMORY.md>'
    cat "$FILE"
    echo '</PROJECT_MEMORY.md>'
  else
    echo "(PROJECT_MEMORY.md is large — read it with the Read tool before doing project work.)"
  fi
elif [ "${PROJECT_MEMORY_NUDGE:-1}" != "0" ]; then
  echo "No PROJECT_MEMORY.md in this repo yet — run \`/project-memory:memo\` to start recording durable project facts, so future sessions don't need re-explaining."
fi

exit 0
