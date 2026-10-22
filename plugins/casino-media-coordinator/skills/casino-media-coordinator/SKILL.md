---
name: casino-media-coordinator
description: Coordinate a multi-step casino media task across source mapping, reference-video replacement, voice work, independent continuity review and local integration. Read current project instructions/memory, assign workers the actual skills and artifacts, reconcile rechecks and track handoffs. Use for coordinating the requested work; planning or skill creation alone does not authorize production runs.
---

# Casino Media Coordinator

Act as the integration owner for the user's actual media task. Select the necessary workflows, give workers concrete instructions and inputs, and reconcile their outputs against raw evidence. This is an instruction skill, not a background service or an installed model. Do not launch a production workflow merely because the user asks to create, explain or improve this skill.

## Establish current truth and scope

Resolve the actual project root and active instructions. Read `AGENTS.md`, current `README.md` and the relevant overview/sections of `PROJECT_MEMORY.md` if present. For AI casino, README is the canonical maintained plan/research log; recent entries can supersede historical recipes. Current user instructions and verified repository evidence take precedence over stale memory. Memory documents context; it does not grant new permission to publish, spend or deploy.

Identify the requested deliverable, checkout/environment, actual current programme/revision, input artifacts, approved references/voice, output location, existing authorizations, budgets and completion criteria. Distinguish Local DEV review assets from game-admitted media and from the VPS. Verify consequential version/provider/path claims rather than copying snapshot constants or old hostnames.

Use existing approved inputs without asking again. Ask only for missing information that changes the work, and continue independent preparation while waiting. Missing authorization for one external action does not block useful local work. Never convert elapsed time into approval.

## Choose workers and dependencies

Read [routing and handoff rules](references/routing-and-handoffs.md). Discover the installed skill paths in the current environment; read the selected `SKILL.md` files before assigning work. Availability in the coordinator's context does not prove a worker read a skill or can access its tools/files. Give each worker explicit absolute skill paths and instructions to read the relevant references.

Select only the stages needed. A typical dependency chain is source mapping → picture and audio work → final continuity review → integration and runtime recheck. Video and audio may proceed in parallel after stable shared source coordinates/references; lip-related conclusions wait for both final artifacts. Original-performance voice conversion and direct Fish TTS are different branches: follow the requested performance, not a default that silently rewrites speech.

Honor the project's requested swarm composition and current concurrency limit. AI casino specifies audit roles of two adversarials plus two reviewers, and build roles of two planners, two plan reviewers, two fresh-context adversarials, two implementers and two regression reviewers. Use bounded waves when the available slots cannot host them together. For a small task skip unnecessary roles and state which and why. Do not launch every role for a single-file change. Keep one integration owner; avoid workers creating nested duplicate swarms or acquiring shared provider/watch ownership independently.

Delegate with available subagent tools when supported and authorized by the task/instructions. Do not create sidebar chats as a substitute for subtasks unless explicitly asked. If delegation is unavailable, execute the needed work sequentially where possible, state the independence limits, and leave independent-check claims unfulfilled rather than inventing workers.

## Give every worker a concrete brief

Use the [worker brief and result fields](references/worker-brief.md). Include the requested result, actual skill path(s), canonical project entrypoints, exact input/map/reference versions or hashes, owned output files/modules, dependency boundaries, required evidence, permitted actions and cumulative budget allocation. Require the worker to confirm missing files/tools/permissions before dependent actions and to report what it actually ran.

Define nonoverlapping write ownership. Workers write versioned outputs in their own staging areas; only the integration owner reconciles shared manifests, programme registrations and canonical documentation. Coordinate ownership transfers explicitly. Do not allow two game writers, provider request owners or watchers. Existing locks and exact-request caches remain authoritative.

Keep one global ledger of actual spend plus outstanding reservations across workers/retries. Allocate disjoint sub-budgets before concurrent paid work. An ambiguous request stays reserved/unknown until reconciled by receipt/job ID; never free its allocation and resubmit because it timed out. Reuse verified exact-input caches where appropriate. Skill invocation never grants unlimited retries, uploads, infrastructure rental or a provider switch.

## Integrate evidence, not success summaries

Track each needed stage as not started, running, blocked, needs repair, verified within coverage, or not applicable. Bind dependencies to exact hashes/map/config versions. An operational task ledger is run evidence, not a parallel maintained project plan. Keep durable research/tests/decisions in the canonical README and relevant maintained memory according to project instructions; do not create an AFFiNE plan.

Before accepting a worker handoff, inspect its actual artifacts, raw evidence, source/trim maps and claimed checks. Verify the final player or served candidate uses the same bytes/revision where runtime verification is required. A valid map declaration, review-ready flag, contact sheet or old test receipt cannot certify actual continuity, hearing or current game admission.

When upstream bytes, text, timing, references, voice or configuration change, invalidate affected downstream evidence. Identify the dependency closure: a trimmed picture edit can invalidate audio placement, cue windows, lip review and game admission. Preserve valid unaffected work and existing approvals; do not regenerate everything or reuse stale dependent signoff.

Maintain casino invariants: play-money/AI labeling for this prototype; server-owned results/ledger/deadlines; one public voice/camera; round priority, expiry/cancellation and whole-utterance eligibility; no private balance in shared pictures. Recorded source results never establish current outcomes. Renderer/provider failure cannot reroll the game.

## Manage first checks and independent rechecks

Apply [the two-pass protocol](references/recheck-protocol.md). The producing worker checks its work; a separate checker reopens frozen final artifacts and independently tests critical conclusions. Give fresh adversarial/reviewer contexts raw artifacts and requirements before sharing proposed verdicts. Continuity inspection and integration verification address different requirements; neither substitutes for the other.

Consolidate compatible evidence rather than spawning a recursive checker for every checker. One qualified second pass can satisfy multiple stages only if it explicitly inspects each required dimension against the same final versions. Reconcile disagreement from raw evidence, assign the smallest authorized repair and recheck its dependencies. Default to at most two repair/recheck cycles, bounded by the task budget; report persistent defects or missing capabilities instead of silently lowering standards.

Required inaccessible listening/viewing/runtime checks remain not assessed/held. Two checkers agreeing from the same summary do not establish independence. Technical decoding/timing, perceived identity/words/lips and owner approval are separate statuses. Do not call a full result verified when a required dimension remains unresolved.

## Complete the requested handoff

Deliver the actual requested artifacts, final source/map/reference versions, worker/checker evidence, cumulative budget status, remaining findings and exact scope of completed verification. Explain skipped roles and limitations concisely. Preserve recoverable source/previous candidates; no automatic cleanup of raw evidence.

Local integration ends in a reviewable candidate unless live activation is already authorized for the actual destination. Honor existing authorization without repeatedly asking; if new destination approval is necessary, finish all preparation and present the concrete tested change first. Creating/installing this coordinator does not start media jobs, watchers, deployments or recurring automation.
