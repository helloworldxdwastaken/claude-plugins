---
name: memo
description: Append a durable project-specific fact (architecture, build/run/deploy steps, gotchas, decisions, conventions) to THIS repo's PROJECT_MEMORY.md. Use when the user says "/memo ...", "remember this for the project", "add to project memory", or right after learning something operational about the current project that future sessions will need. Creates PROJECT_MEMORY.md from a template if it doesn't exist. Do NOT use for cross-project facts about the user (those belong in personal memory).
---

# /project-memory:memo — capture a durable project fact

This project keeps its knowledge in **`PROJECT_MEMORY.md`** at the repo root (not in any agent's
personal/global memory). This skill appends a fact to that file, creating it if it doesn't exist.

## Steps

1. **Locate the file:** `PROJECT_MEMORY.md` at the repo root — use `$CLAUDE_PROJECT_DIR` if set, else the current working directory.
2. **If it doesn't exist, scaffold it** using the *Scaffold template* below (fill in the project name), then continue.
3. **Read it** to see its existing sections and entries.
4. **Get the fact:**
   - If the user passed text after the command, use that.
   - Otherwise, infer the single most important durable project fact just learned in this conversation, and state it back in one line so the user can confirm or correct it.
5. **Place it well:** append to the best-fit existing section (e.g. *Architecture*, *Build / Run / Deploy*, *Gotchas / lessons learned*). If nothing fits, add a dated bullet under **`## Log`** (use the real current date from the environment context — do not guess).
6. **Keep it clean:** terse, one fact per bullet; reference files as `path:line`; convert relative dates ("today") to absolute dates; **de-duplicate** — if a near-identical entry exists, update it in place rather than adding a new one.
7. **Confirm** in one line what you wrote and where.

## Rules

- **Never** write project knowledge to personal/global memory — `PROJECT_MEMORY.md` is the home.
- **Never** put secrets, API keys, or tokens in the file — it is committed to the repo.
- Make a **minimal, targeted** edit; don't reformat or churn unrelated parts.

## Scaffold template

Use this verbatim when creating a new `PROJECT_MEMORY.md` (replace `<Project>` with the repo/app name):

~~~markdown
# <Project> — Project Memory

> Durable project knowledge lives here — not in any agent's personal/global memory.
> Agents: read this before working on the project; append new durable facts via `/project-memory:memo`.
> One fact per bullet, keep it terse. No secrets/keys (this file is committed).

## Architecture
- 

## Build / Run / Deploy
- 

## Gotchas / lessons learned
- 

## Log
- <YYYY-MM-DD> — created.
~~~
