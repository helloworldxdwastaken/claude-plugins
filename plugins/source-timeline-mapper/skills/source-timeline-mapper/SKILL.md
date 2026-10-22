---
name: source-timeline-mapper
description: Prepare and verify source-to-output video/audio timing maps, shot boundaries, exact sample/frame offsets and genuine source handles for reference-based media workflows. Use before generation or when reconciling generated, paired or silence-trimmed footage; mapping does not authorize generation or live integration.
---

# Source Timeline Mapper

Produce an evidence-backed map from original footage/audio to prepared or finished media. Preserve source chronology and full utterances unless the requested edit says otherwise. Distinguish planned ranges, provisional estimates and measurements of actual output. Read the current project's canonical plan before using old offsets or paths.

## Inventory the real inputs

Locate original video, original audio counterpart, candidate outputs and existing cut/shot maps. Record hashes, stream indexes, dimensions, rational frame rate/time base, start PTS, duration and actual decoded frame/sample counts. Identify silent video, separate recordings and unrelated audio. Missing original audio blocks source-word mapping but does not prevent visual work.

Keep container start times, decoder/encoder delay, original-recording coordinates and normalized working coordinates distinct. A nominal FPS or container duration is insufficient evidence of exact frame/sample boundaries. Preserve variable-frame-rate PTS; do not silently assume CFR or convert the master to fix arithmetic. Probe selected streams explicitly when files contain multiple tracks.

For AI casino work read [current project recipe](references/casino-mapping.md), including the existing direct-Fish cut maps. Do not infer host dialogue from a wheel renderer's reused motion-template range.

## Construct and verify the map

1. Detect candidate shot boundaries, then inspect both adjacent decoded frames. Note transitions, hard cuts, genuine source endings, speech onsets/ends, gestures/contact and usable following footage. Scene detectors and ASR produce candidates, not verified boundaries or words.
2. Represent half-open intervals `[start,end)` in integer native coordinates with a rational time base. Record source and output coordinates, stream identity, intended speed and the evidence establishing each correspondence. Keep original-clock, programme-clock and silence-trimmed-clock maps separate and composable.
3. Prepare source excerpts with genuine before/after handles when needed. Record the retained core separately from handles. A final source tail cannot be created by looping, freezing or borrowing unrelated footage. If an engine needs more input than exists, report that limit.
4. Match actual generated output using cuts and recognizable performance landmarks. Measure drift before deriving any alignment correction; do not align away the error you are checking. A requested mapping is provisional until the actual output supports it. Reject missing core footage; do not stretch speech to disguise truncation.
5. For speech, map exact decoded samples and retain uncertain/quiet/nonlexical regions for review. Compare original, isolated and converted or resynthesized lanes separately. Direct TTS is a new performance and needs its own placement/word check; it is not sample-identical source conversion.
6. For silence trimming, cut picture and audio together, retain stated boundary padding and preserve a reversible retained-interval map. Recompute all downstream cue/cut offsets on the trimmed clock. Do not feed trimmed speech offsets into an untrimmed game programme or treat reference-only pictures as finished target footage.

Use [map format and checks](references/map-format.md) when a portable map is useful. The bundled `scripts/verify_timeline.py` checks asset hashes, rational interval math, explicit speed, bounds and complete nonoverlapping output coverage. It checks declarations, not decoded count accuracy, semantic correspondence, silence or lips. Adapt existing project maps through a separate export rather than overwriting their schemas. Use `--require-verified` only after actual source/output checks support that status.

## Check, then recheck

Apply [the two-pass recheck protocol](references/recheck-protocol.md). First check all mappings and prepared media. The second checker reopens final bytes, independently probes/decodes relevant streams and verifies first/last retained frames, both sides of every cut/trim, speech boundaries and representative interior landmarks. Compare native coordinates and rational arithmetic independently of the first checker; running the same validator twice is insufficient.

Give a fresh checker raw sources, final outputs, required map format and edit contract, without the first checker's proposed verdict. Reconcile disagreements against evidence. When a separate agent cannot run, use a separate verification method/pass and state that limitation. Stop after two repair/recheck cycles unless the user has authorized a larger bound; unresolved ranges remain held. Any subsequent hash/map change invalidates the affected checks and downstream handoff.

## Deliver

Provide the asset/shot inventory, source-to-output map, core/handle ledger, evidence of checked boundaries and two check records bound to final hashes. Separate intentional gaps/silence from missing footage, provisional ranges and unresolved source words. Summarize observed drift and unusable intervals. No unqualified verified map if required correspondences are unassessed. Do not upload, generate, start a watcher or activate live assets as a side effect of mapping.
