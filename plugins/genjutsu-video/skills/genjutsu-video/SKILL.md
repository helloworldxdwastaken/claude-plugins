---
name: genjutsu-video
description: Recreate a reference video's performance using supplied character, clothing, environment and object images, with Genjutsu-style video replacement and detailed continuity checks. Use when asked to make or revise a video replacement, character swap or environment swap; research alone does not authorize generation.
---

# Genjutsu Video

Produce the requested replacement video and an honest comparison against its references. Aim for exact character and environment continuity, including small details. Generation cannot guarantee that fidelity: inspect the finished output, repair bounded failures and disclose unresolved differences.

## Establish reference authority

Inventory the driving video and supplied images before rendering. Resolve ambiguous roles from the request or existing project decisions; ask only for consequential missing choices. Save a compact reference ledger containing file hashes and these roles:

- **Driving video:** performance, gestures, expressions, blocking, camera movement, shot order and source timing.
- **Face authority:** one approved identity image or explicitly approved multi-view identity set. The recorded actor and outfit/model photos are not alternate face authorities.
- **Clothing authority:** silhouette, fabric, exact color, collar, sleeves, cuffs, seams, buttons, fastenings, embroidery, jewelry and accessories. Preserve visible placement and counts; mark details obscured in references as unknown.
- **Environment authority:** floor plan and master views establish layout, scale, materials, furniture, equipment, light direction and reflections. Distinguish reference camera perspective from actual room geometry.
- **Object/hand authorities:** props, equipment, manicure and other close-up details where supplied.

Separate what must change from what must survive. For an object-only edit, preserve the original person and environment. For complete character/room replacement, do not retain the source actor or room by default. A target room blueprint can require a different composition; explain the conflict before imposing incompatible framing constraints.

For AI casino work, read the project's current README and [casino recipe](references/casino-recipe.md). Its current decisions supersede older prompts.

## Select a real execution path

Follow a user-selected provider. Discover current tools, model schemas, limits and accessible local adapters; record the actual path. Do not invent an Asta endpoint or claim this skill installs a video model. If no available engine accepts both the driving video and the requested reference/edit controls, complete local preparation and report the concrete missing capability. Text-to-video is not evidence of matching a source performance.

When using Higgsfield, read its available Genjutsu/preset instructions as needed. The checked CLI exposes `hf_mult_replace_object` and `hf_mult_motion_control`: each requires exactly one video reference and at least one image reference, with 480p/720p/1080p choices. Read the current schema again before execution; inspect current official mode guidance in [provider notes](references/provider-notes.md). These names do not establish the underlying model or guarantee identical behavior.

Use Motion Transfer for rebuilding the character and/or environment around the original performance; use Object Swap for targeted replacement while retaining the surrounding shot. Assign separate identity references to each recurring character so their faces, clothes and roles are not blended or swapped. Character replacement alone does not prove room replacement succeeded. A separate background pass or tracked composite may be necessary; verify that it preserves hair edges, hands, contact, shadows and foreground occlusions. Do not silently switch providers or resolutions.

Quotes and upload operations have separate effects: the installed Higgsfield `generate cost` command auto-uploads local file arguments. Check destination authorization before passing private paths. Use authorized existing media IDs where suitable. Build quote calls explicitly; never derive them by slicing a submission command. Skill creation is not permission for uploads, paid jobs or deployment. Honor existing scope/budgets without repeatedly asking for approvals already given.

## Prepare and execute

1. Probe the actual source: dimensions, rational frame rate, time base, duration, frame count, audio presence and cuts. Use frame/sample or PTS mappings rather than rounded decimal timing. Map all trims, crops and source handles.
2. Inspect reference conflicts before spending. For each camera family, use or prepare an authorized shot-angle guide with the correct face, clothing, pose, chair height, room layout and prop placement. Keep one approved reference set across related shots. Correct a wrong plate rather than repeatedly prompting against it. When continuing an established video, extract accepted earlier camera-family views, including the beginning when specified by the owner, and verify room landmarks and camera axis before using a guide or spending. A newly generated shot is not its own room authority.
3. Build a shot-specific prompt assigning each reference a role. Describe the intended replacement and the preserved performance/camera timing concretely. Include visible fine details and object counts. Keep natural source expressions rather than copying a portrait's fixed expression.
4. Start with a representative pilot within the authorized work: visible face turn, detailed clothes, hand/object contact and a camera transition if present. Inspect it before expanding. Do not infer acceptance of an entire batch from a still.
5. Keep source order, speed and cuts unless an edit was requested. Use genuine adjacent source handles for engines that truncate outputs. Preserve a mapping from each generated interval to the original. Never conceal missing footage by stretching speech, freezing a presenter or deleting a failed beginning.
6. Save prompt, reference hashes/order/roles, provider/model/version or revision if exposed, parameters, seed if supported, quotes, job IDs, attempts and actual output hash/properties. Fetch the documented result field; do not scrape the first MP4 URL, which may be the input. Recover an existing timed-out job by ID before considering a resubmission.

## Verify before calling it matched

Read and apply [fine-detail review](references/fine-detail-review.md). Inspect decoded output at native resolution and play every shot at normal speed. A contact sheet supports review but cannot prove continuity between its samples. Review face, clothing, environment, props and timing separately; a passing face cannot compensate for the wrong room.

Record timestamped discrepancies with expected reference, observed output, severity and action. A missed identity, garment feature, room landmark, required prop, cut or occlusion is a repair item. Mark invisible/ambiguous details unverified. Similar palette, embedding scores and successful rendering are insufficient acceptance evidence.

Repair the smallest failing shot or region, keep previous versions and recheck the changed interval, its neighbors and cross-shot consistency. Agree a bounded retry/cost envelope from the existing task authorization; if unspecified, do one permitted pilot and report failures before expanding into paid retries. Track cumulative actual spend plus outstanding quoted/reserved cost across the pilot and all retries; a 30-credit ceiling means 30 total, not per attempt. Stop when the remaining defect requires a new reference, unavailable capability or additional budget.

## Audio and handoff

Keep original/generated audio out of a voice-replacement export unless requested. When source speech is converted separately, preserve the shared source clock and use Casino Voice Cloner if available. Synchronizing audio timestamps does not establish that generated lips pronounce the words. Any lip-sync pass needs its own identity, clothing, timing and mouth review.

Deliver the actual video, reference ledger, source/output timing map and a concise timestamped review. State what was inspected, fixed and remains uncertain. Keep technical, perceptual and owner-approval status separate. Do not publish, replace live media or change game state merely because a review export exists.


## Check and recheck

Apply [the two-pass recheck protocol](references/recheck-protocol.md) to this skill's final artifacts and conclusions. The worker checks first; a separate checker reopens the frozen final bytes and independently challenges the result. Recheck changed intervals and dependencies after repairs. Record actual coverage and unresolved checks; two passes do not create a guarantee of perfection.
