#!/usr/bin/env bash
# project-memory — SessionStart hook.
#
# If the current repo has a PROJECT_MEMORY.md, inject it (plus the standing
# convention) into the session context at startup — so the agent treats the
# project's recorded knowledge as authoritative and never needs it re-explained.
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
  echo "When you learn a new durable project fact, append it via the \`/project-memory:memo\` skill — never to personal/global memory."
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
