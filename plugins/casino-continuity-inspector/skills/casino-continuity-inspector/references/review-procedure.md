# Review procedure

## Prepare evidence

Probe source/output dimensions, rational FPS/time base, actual decoded frame count, audio sample rates/channels/counts, start offsets and complete decoding. Save checks against actual hashes. Keep immutable inputs and use a new local evidence directory; do not overwrite producer masters.

Build a source-to-output interval map that identifies cut correspondences, trims, handles and any retiming. For every event record both native coordinates. Align appearance comparisons at corresponding performance moments; also measure their actual displacement so the comparison does not conceal timing errors.

Extract actual first/last frames, both sides of each cut, shot start/middle/end and high-risk motion/occlusion points. Inspect every frame in short suspect intervals, including appearance ramps. Use separate face/clothing/environment crops at native resolution; a tiny thumbnail cannot reveal a missing cuff button. Inspect across shots and after reappearance. For recurring sets, apply [room/camera comparison](room-camera-continuity.md) and include accepted earlier footage in the evidence, not only the source actor and isolated target portraits. Watch all shots normally for flicker and unnatural movement; report any unviewed intervals.

For speech, prepare original, isolated and converted lanes on one clock. Listen to each retained utterance and its boundaries, with source context for unclear words. Compare voice identity to the authorized reference. Inspect support gaps for lost quiet calls and non-speech noise. Use ASR only as an additional flag. Verify final compressed preview alignment separately from the lossless working master, accounting for encoder delay.

Check AV sync at beginning, middle, end and every cut/utterance boundary, plus pause/seek/restart in the intended player when accessible. Timestamp clocks establish delivery behavior; heard words plus visible articulation establish perceptual observations. Keep those conclusions separate.

## Report fields

Record artifact hashes, references/roles, tool/model versions used for analysis, source/output coordinates, full-viewed/listened coverage, sampled/dense frame ranges and inaccessible checks.

Use a findings table with these columns:

| Output time/frame | Source time/frame/sample | Dimension | Expected reference/detail | Observed discrepancy | Evidence | Impact/status | Smallest repair |
| --- | --- | --- | --- | --- | --- | --- | --- |

Attach a separate dimension summary for face, clothing, room, props/hands, performance/cuts, speech content, voice/levels and AV sync. Do not average these into one score that hides a failed requirement. Mark absent/occluded details not visible and checks you could not perform not assessed.

Keep the actual candidate and its verdict bound to hashes. A repaired take needs a new review record with changed intervals/neighbors inspected; preserve previous evidence. Avoid publishing local private excerpts or signed URLs merely to make a report shareable.

## Casino examples motivating this review

Local AI casino evidence includes a first-16-frame appearance ramp, cropped torso/invented props, rug versus parquet conflicts across reference angles, shifted cuts, terminal footage loss and source words garbled by conversion. These motivate dense boundary review and same-moment listening; they are examples, not proof that every new output has the same defects.

For current facts read the checkout's README and `references/generated/RECIPES.md`; older production URLs, funding caps, approval holds and source offsets may have been superseded. Producer receipt status does not grant new upload or deployment permission.
