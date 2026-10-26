---
name: casino-continuity-inspector
description: Independently review finished reference-based video and converted speech for face identity, garment details, room geometry, performance timing, word preservation and audiovisual sync. Produce evidence and timestamped repair findings; inspection alone does not authorize regeneration, paid calls or publishing.
---

# Casino Continuity Inspector

Check whether the actual final picture and audio meet the supplied references. Build evidence and a repair list. Keep source-performance matching, target-appearance matching, technical timing and perceptual judgments distinct. Small details matter; invisible details and uninspected intervals remain unverified.

## Establish the review contract

Inventory the source video/audio, final candidate, approved face/clothes/room/prop references and source-to-output map. Bind actual file hashes and decoded stream properties so a report cannot accidentally certify a different take. Resolve intended edits and accepted deviations from the user/project; a deliberate character swap should differ from the recorded actor.

For recurring scenes, read [cross-shot room and camera review](references/room-camera-continuity.md). Establish the accepted room from actual earlier footage, especially the beginning when the owner identifies it as the reference. Compare each new shot with that room and its neighbors; a matching face or color palette cannot pass a different floor plan or camera axis.

Read the current canonical project plan for casino work. Preserve existing owner approvals without treating them as measurements. A current owner rejection supersedes an older acceptance for that defect; reopen the affected shot and dependent continuity review. Resolve missing/stale reference paths explicitly. Do not choose a new target face, garment, room or voice to make a candidate pass.

If no mapping exists, derive a provisional map from source/output cuts, recognizable gestures and audio events. Record its uncertainty; avoid circularly aligning away the cut/gesture drift being measured. Missing source audio prevents original-word comparison, but visual review can continue. Missing face reference prevents identity certification, but clothing/layout review can continue.

## Conduct an independent pass

Make observations from the raw source, target references and actual output before adopting a producer's success claims. When an independent reviewer is requested and delegation is available, give a fresh reviewer the artifacts and review contract, keeping prior proposed verdicts out of its initial context. Otherwise perform a separate pass and state its independence limits. A small review need not launch a full swarm.

Use [review procedure and report fields](references/review-procedure.md). Prepare source/output paired native frames and detailed crops, contact sheets, mapped audio comparison lanes and short local diagnostic excerpts. Inspect the evidence; extraction by itself is not review. Review tools that upload private media require the appropriate existing destination authorization. Prefer local processing.

Watch the whole output at normal speed. Inspect dense frames around cuts, first-frame appearance ramps, face turns, hand/prop contact and joins; use native-resolution crops for small clothing/face/background details. Listen to all retained utterances against original and isolated speech at the same moment. Track coverage honestly and mark unsupported sensory checks as not assessed if actual viewing/listening tools are unavailable.

## Proven checks for scheduled speech and lips

For a programme whose voice plays in scheduled windows over a picture timeline, run these local scripts (faster-whisper, librosa, soundfile, OpenCV). They found real defects that frame sampling and summary reading missed.

1. **Every window as played:** `python3 scripts/speech_windows_pass.py STEM WINDOWS.json OUT`. It renders the stem only inside the windows (what the gate lets through), then reports each line's text from two ASR models, head/tail edge level, peak, active-speech level and overlaps. Read the text against the intended wording. An edge above about −60 dB is an audible cut. A line several dB off its neighbours is a level jump.
2. **Every face shot, not only voiced ones:** list the frame ranges where the face is on screen, then `python3 scripts/mouth_sheets.py VIDEO OUT RANGES… --voice OUT/voice-as-played.flac`. Look at every sheet. A mouth shaping words without the green **V** is silent mouthing; a **V** over a closed mouth is voice without lips. Most findings live in shots that carry no voice at all.
3. **Lip timing:** when the picture copies an original performance, `python3 scripts/word_onsets.py DELIVERED ORIGINAL WINDOWS.json` gives each window's median word-onset difference against the original speech. Negative means the voice is ahead of the lips. Treat medians beyond ±150 ms over a visible face as findings; fewer than 3 matched words is no evidence.

ASR input must be 16 kHz: faster-whisper treats a raw array as 16 kHz, so 48 kHz audio returns fluent nonsense. The scripts resample. Pixel-motion or mouth-aperture scores were too noisy (head turns, cuts to wides) to give a sync number; report sync only from word onsets plus looking.

## Findings that require attention

- **Identity:** wrong/blended/swapped person, face drift in profile/speech, hair/skin/age changes and inconsistent hands/body.
- **Clothing:** missing/changed buttons, seams, collar/cuffs, fabric/prints, jewelry, accessories, nail details or features that detach/flicker during motion.
- **Room/props:** layout inconsistency across angles, rug/floor changes, mirrored furniture, equipment scale/design, duplicate/missing objects, floating contact, incorrect shadows/reflections and occlusion failures.
- **Performance/timing:** changed camera order/framing, shifted cuts or gesture/contact times, dropped beginnings/ends, unexplained freezes/stretching and long-run clock drift.
- **Speech:** lost/repeated/invented words, incorrect numbers/names, lost quiet phrases or laughs, target-voice inconsistency, residual music/noise, clicks/clipping, gain pumping or audible joins.
- **AV relationship:** duplicate speech, lip closures/onsets inconsistent with delivered words, pause/seek/restart drift, wrong source mapping or animation that mouths unrelated words.

Automated metrics support observations; they do not replace them. Similar face embeddings cannot certify all facial features, ASR cannot settle ambiguous source wording, and correlated envelopes cannot establish phoneme sync. Report the method, actual measurements and uncertainty rather than inventing confidence scores.

For casino assets, inspect source HUD/result contamination and wheel/felt details. Recorded winning numbers, balances or cutoffs cannot become current game facts; note this as an integration constraint even if the source was reproduced perfectly. Private balances must stay outside shared footage. Review does not reroll outcomes, edit ledgers, activate assets or change services.

## Verdict and handoff

Provide a concise outcome with a timestamped finding list, evidence links and coverage summary. Give each required dimension a status: pass within inspected coverage, mismatch/hold, not visible or not assessed. State the evaluated frame/sample/time mapping and any tolerances supplied by the project; otherwise report observed deviations and their visible/audible effect rather than inventing universal thresholds.

When matching is incomplete, recommend the smallest specific repair: correct an authority image, replace a shot/region, select another whole utterance, repair a same-source join or request a separate lip-sync pass. Do not regenerate, spend, download models, publish or alter source assets as part of inspection unless separately authorized. If the task includes repairs, hand the findings to the appropriate creator and recheck changed intervals, neighbors and cross-shot continuity on the new final hashes.

An overall pass applies only to explicitly checked requirements and coverage. Any required unassessed dimension prevents an unqualified 'everything matches' verdict. Preserve evidence of accepted cosmetic deviations and keep owner approval distinct from technical or perceptual checks.


## Check and recheck

Apply [the two-pass recheck protocol](references/recheck-protocol.md) to this skill's final artifacts and conclusions. The worker checks first; a separate checker reopens the frozen final bytes and independently challenges the result. Recheck changed intervals and dependencies after repairs. Record actual coverage and unresolved checks; two passes do not create a guarantee of perfection.
