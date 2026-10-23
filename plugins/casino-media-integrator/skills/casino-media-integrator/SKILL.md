---
name: casino-media-integrator
description: Integrate approved casino video/audio into an isolated local candidate, preserving source maps, authoritative outcomes, safe speech scheduling and private state. Use for programme assembly, media admission or replacement integration with two verification passes; preparation alone does not authorize live activation or deployment.
---

# Casino Media Integrator

Prepare a concrete local candidate from approved media, then prove it fits the current casino contracts. Read the current README and relevant operational memory before touching assets: Local DEV, staging and production can have different code, providers and state. Identify the actual checkout, version, active programme/revision and destination; historical hostnames and old release recipes are not defaults.

Use [project integration entrypoints](references/casino-integration.md) for the existing repository. Discover actual APIs and schemas before making a change; do not create parallel game rules or weaken admission checks to accommodate unfinished footage.

## Pin inputs and stage separately

Inventory approved final media and references with hashes, measured frame/sample counts, source/trim maps, dialogue text/provenance and owner approvals. Keep technical, perceptual and approval status distinct. Missing references, reference-only pictures, unknown wording and provisional mappings stay explicitly held; preserve partial progress rather than claiming a complete programme.

Build in an isolated working directory or checkout with new versioned media/manifests. Preserve current reviewed prefixes and original assets. Do not overwrite on-air folders, point an active server at drafts, start a second game writer or copy live private state as a shortcut. Test fixtures use synthetic state with clearly marked committed outcomes; production wallets/results/epoch are never disposable fixtures.

Compose original→programme→trimmed mappings explicitly. A review clip with removed silence changes both picture and audio clocks; its cues need recomputing and it may be unsuitable for unchanged live round timing. Require real source tails and safe joins; do not freeze a talking presenter, invent dialogue or stretch footage to fill gaps.

## Enforce the game/media boundary

- One authoritative result object owns number, color, wheel stop, displayed result and settlement. Reproducing a recorded source result cannot establish a new round outcome. Never reroll to recover a missing asset or renderer failure.
- Inspect and classify recorded speech: neutral, phase-sensitive, outcome-sensitive or dynamic reply. Exclude or event-gate conflicting number, balance and cutoff claims. Unresolved original words cannot silently become approved TTS text. Code-owned verified critical announcements keep priority.
- Keep one public voice/camera: no duplicate native video audio, source music speech bleed, recorded/runtime overlaps or stale replies. Check whole-utterance fit, cancellation, expiry, camera eligibility, reduced-motion behavior and source-lease changes.
- Preserve wheel appearance and phase/contact across entry, result, replay and coast; replay presents the same committed event. Do not relabel a numbered clip to match another result, admit garbled pocket numerals or conceal a stale result with a cosmetic overlay.
- Keep credentials, private wallets/player data and debug controls outside shared pictures and distributable manifests. Preserve clear AI/virtual and play-money identification in this project's prototype. Do not assume another deployment shares this prototype's wallet/bet contracts.

## First verification: construct and exercise the candidate

Verify selection exhaustively, not by spot checks: scan every frame/time of the candidate and record which asset or renderer actually paints it and which speech window can play, so fall-through gaps (e.g. to a fallback renderer) and unreachable cues show up. Check that origin/host allow-lists for asset playback include the real deployment hosts. For scheduled speech, check each clip against the phase it describes, the code-owned announcements it could duplicate or crowd, and the player's start-lag tolerance.

Run current asset readiness/hash/byte admission and appropriate focused game/media/voice regression checks. Recompute cues and validate coverage, cut/trim boundaries, source prefix preservation and final encoded bytes. Use synthetic replay/fault fixtures to verify game-result/media agreement and failure behavior without modifying live outcomes.

Exercise the actual candidate in its intended local player: natural playback through a complete candidate cycle and wrap; all new/replaced result/cue intervals; sound on/off; cut/cancellation/expiry; buffering or missing media; pause/seek/reconnect where supported. Check private-state exclusion and route separation. For claimed High/Saver delivery, test each actual delivered variant; a source master cannot certify transcoded bytes. Do not claim device/capacity/shared encoded streaming support that the actual system does not exercise.

Listen and inspect changed speech/pictures; clocks/RMS are technical evidence, not word/voice/lip certification. If browsing/listening or required checks are unavailable, keep a qualified staging result and identify the missing evidence. Apply relevant existing test commands to the actual changed modules; do not fabricate an acceptance report from old suite totals.

## Second verification: recheck final artifacts

Apply [the two-pass recheck protocol](references/recheck-protocol.md). A fresh checker receives raw final candidate bytes/maps, current game contracts and required outcomes/cues; it recomputes hashes and critical mappings, independently inspects boundaries and challenges runtime admission using replay/fault evidence. The first checker's summary is not the source of truth. Reopen the actual local candidate/delivered assets and confirm the final version is what the player uses.

If a fix changes bytes, mapping or scheduling, invalidate affected evidence, check the changed intervals and neighbors, rerun relevant failures, then perform the second check again. Default to at most two repair/recheck cycles; report remaining holds rather than retrying indefinitely. A missing required test or a disagreement cannot be converted into a pass by running the same command a second time.

## Handoff and activation boundary

Deliver the staged candidate, exact change list, assets/map/version hashes, first and second check records, actual tests and perceptual limitations, held intervals and a rollback/latest-state plan suitable for the identified destination. Rollback must preserve the latest authoritative game state, never restore stale balances/results merely to revert media.

Carry out live activation/deployment only when already authorized for that destination; otherwise the reviewable tested candidate is the handoff. Creating this skill is not permission to deploy it. Existing explicit destination approval persists within scope; do not ask again merely because a skill mentions this boundary. Maintain one writer and use current safe-transition contracts. Record actual research, tests and decisions in the casino README.
