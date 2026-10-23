---
name: casino-voice-cloner
description: Clean and replace recorded speech through performance-preserving voice conversion, or remake checked or supplied dialogue directly in Fish when requested. Match speech to video, including repeatable scene processing and requested silence trimming. Use for voice replacement and scene audio; standalone transcription or script writing is outside scope.
---

# Casino Voice Cloner

Choose the requested voice workflow, then deliver a voice-only master, the requested video pairing and a same-moment comparison where source speech exists. Cleanup, voice similarity, word fidelity and lip synchronization are separate checks, each with its own evidence and limits.

## Choose the workflow

- **Source-performance conversion:** preserve the original words, delivery and source timing while replacing the speaker's timbre. Follow the isolation/conversion steps below. A transcript is supporting evidence, not the acoustic input.
- **Direct Fish remake, when requested:** synthesize checked source dialogue or user-supplied words using the resolved authorized Fish voice. This is a new performance with its own timing and word checks; it does not preserve the original delivery or establish lip sync. Follow [the Fish scene workflow](references/fish-scene-workflow.md) instead of requiring a local voice converter.

Use the request and existing project decisions to select the workflow. Do not silently substitute Fish TTS because conversion is unavailable, or substitute conversion when the user requested Fish. Resolve only material ambiguity; reuse existing authorization and voice choices.

## Establish inputs and clock

Locate the source recording/audio or supplied script, authorized target voice/reference and the video to pair. Record the target's provenance. An existing approved synthetic voice is reusable conditioning; do not call it a newly recorded human clone. Ask for a target only if it cannot be resolved from the project/request.

Probe actual streams rather than assuming audio exists. For conversion or a remake of original dialogue, a silent video needs its authorized original audio counterpart; report the missing source if none exists. User-supplied words can support an explicitly requested new Fish performance without original audio. Do not reconstruct original words from lips or invent a TTS transcript as a substitute.

Read [the casino recipe](references/casino-recipe.md) for Katie or existing AI casino work. For source-performance conversion, prefer installed local isolation/conversion tools and cached weights. Inspect versions, model hashes and actual device support; never execute old scripts with hardcoded project paths blindly. If no usable converter exists, prepare the timeline and missing-dependency report without claiming conversion has occurred.

Define source audio sample rate, decoded sample origin, programme offset/length and mapping to the output video. Use integer sample/frame or rational PTS coordinates. Generated-video cut drift requires an explicit source-to-output map; muxing at time zero is insufficient. Preserve unchanged source and intermediate masters with hashes.

## Record wording status

Track wording per utterance, or per clause where certainty differs: **exact** (checked against the source), **normalized** (edited wording with the changes recorded), **unclear** (unrecovered words with their source ranges), **quiet/nonlexical** (breaths, laughter or uncertain soft sounds), or **intentionally silent** (no dialogue is intended). For supplied scripts, record that provenance separately; supplied words are not a verified source transcript.

Do not silently omit unclear clauses to make a fluent supposedly complete line. Keep the original excerpt and leave that remake pending unless the user resolves the words or requests an alternative. Normalization needs support in the requested edit; it cannot stand in for exact transcription. A quiet detector result does not establish intentional silence. Conversion can preserve uncertain original speech acoustically while its wording remains unverified.

## Isolate, level and convert

1. **Extract losslessly.** Decode the exact intended source interval to a PCM working master. Preserve the full programme clock, including pauses, breaths, laughs and quiet calls; do not concatenate only detected speech. Keep the original mix for A/B listening.
2. **Separate speech.** Use the installed local vocal separator; the casino recipe uses Hybrid Demucs. Reconstruct overlapping analysis windows with normalized weights and account for resampling/filter delay. Inspect original versus isolated spans, especially quiet/off-camera phrases, starts/ends, music overlaps and laughter. A vocal stem can retain music/noise or lose speech.
3. **Clean conservatively.** Use light denoising and source-supported speech regions where needed. Check uncertain detector exclusions against both original and isolated audio, preserve handles and soft speech, and fade outer boundaries. Never use a VAD mask as proof of complete speech coverage. Keep raw isolation and a support map.
4. **Control levels.** Measure source, isolated, target and candidate loudness/peaks over speech as well as the full programme. Match the intended target/playback level using smooth gain and headroom. Keep pauses quiet without boosting separation residue, pumping or flattening deliberate emphasis. Do not hard-gate every source zero crossing. Choose conversion input level for the engine; aggressive normalization can harm conversion. Measure/master the converted track after conversion too. If delivery has a loudness/true-peak spec, use it and measure compliance; otherwise document the selected level rather than inventing a universal LUFS target.
5. **Convert the acoustic performance.** Condition an installed direct voice-conversion model on the fixed target reference. Convert whole utterances with genuine neighboring context; retain their original core placements. Prefer identity/content-preserving settings and no duration adjustment. Do not rewrite, correct an accent, translate, insert missing words with TTS or change the delivery unless asked. Separate optional model-conditioning silence from retained source speech.
6. **Inspect each take.** Check every utterance against original and isolated versions at the same source moment. Identify missing/repeated/changed words, numbers/names, onset/consonant loss, pauses, breaths/laughs, robotic timbre and identity drift. ASR disagreements or speaker embeddings are supporting signals; listen and flag ambiguity. A file can have the correct duration while garbling speech.
7. **Repair bounded failures.** Reuse the source utterance and same target identity. Try a justified parameter or installed-engine alternative within scope; preserve old takes and actual selection evidence. Prefer complete coherent takes rather than stitching unrelated syllables. Stop at the agreed local retry envelope or before new uploads/spend/downloads requiring additional scope. Do not run an unbounded sweep.

## Assemble and match video

Place the selected utterance cores on their original sample coordinates. Use genuine same-source handles for overlaps and smooth joins; remove only verified model padding outside retained speech. Preserve expected full timeline length and silence in excluded windows. Never hide lost speech by arbitrary padding, stretching or moving it.

Export a lossless voice-only WAV/FLAC master before making compressed previews. Check decoded sample count, placement, complete decoding, peaks, clipping, nonfinite samples where applicable, support leakage, joins and final encoding delay. Recheck these on the actual delivered bytes. Report measured timing resolution; do not declare a universal zero-lag result from one metric.

When a placed or replaced utterance lands in a shared stem: transcribe each changed span of the final mixed file with a local ASR pass and compare word-for-word with the intended text (also spot-check neighbouring, previously accepted lines — garbles can hide in old takes); match loudness to the adjacent lines and to any runtime voice on the same output, measured, not only to a fixed target; and fade every clip edge so no clip steps to or from digital silence.

Pair with the final video using its source mapping, keeping duplicate original/generated speech muted. Review phrase onsets/ends, audible events and visible lip closures throughout, including both sides of cuts, long-run drift and seek/pause/restart in the actual player. A stretched or shifted generated performance may need a separate mouth-animation pass; conversion alone does not repair invented lip movement. Do not claim natural lip sync from matching timestamps or mouth-opening curves.

Music/noise removed from source speech stays out of the voice master. Add separately authorized music only when requested; distinguish the music stem and its gain/ducking from the speech treatment.

## Repeated scenes and edited derivatives

When automatic processing is requested, connect each finished video to its checked dialogue, fixed voice identity and measured timing through a versioned completion record. Validate the actual video before requesting synthesis; keep unresolved scenes pending and genuinely silent scenes explicit. Use the [completion and recovery procedure](references/fish-scene-workflow.md#automatic-scene-processing) for atomic records, verified reuse and interruption recovery. For conversion jobs, retain the source audio interval as the conversion input rather than replacing it with the text.

When silence trimming is requested, keep the full master and create a separate derivative. Cut picture and audio together, retain speech/breath handles and save a reversible frame/sample map. Recompute dependent timings on the edited clock. Follow [the silence-trimming checks](references/fish-scene-workflow.md#silence-trimming-and-timing-checks); the untrimmed-master requirements above still apply.

## Casino integration constraints

Classify recorded neutral commentary separately from outcome/deadline/balance calls. Private review can preserve the complete original performance. Live casino playback must gate or replace incompatible recorded claims using authoritative game events; matching the original announcement does not make it correct for the current round. Preserve one public voice, round-call priority, cancellation, expiry and private-balance exclusion. Asset preparation is not live activation.

## Handoff and truthfulness

Provide original/isolated/converted comparison lanes for conversion, or source/Fish lanes for a remake of recorded dialogue, aligned to the same moment. For a supplied-script Fish take without original speech, provide the script and resulting take instead of inventing source comparisons. Deliver the final voice-only master, requested paired-video preview and an artifact manifest. Bind applicable source/target/output hashes, source offsets/sample counts, utterance/support map, model versions/hashes/parameters, take selections, level measurements, clipping/decoding checks, timing measurements and timestamped wording/listening/lip uncertainties. Keep secrets and signed media URLs out of reusable docs.

Report technical checks, audible word/identity review, perceptual lip review and owner approval separately. Preserve prior approvals for unchanged artifacts without upgrading them into unperformed certification. Never claim every detail passed if only sampled checks ran.


## Check and recheck

Apply [the two-pass recheck protocol](references/recheck-protocol.md) to this skill's final artifacts and conclusions. The worker checks first; a separate checker reopens the frozen final bytes and independently challenges the result. Recheck changed intervals and dependencies after repairs. Record actual coverage and unresolved checks; two passes do not create a guarantee of perfection.
