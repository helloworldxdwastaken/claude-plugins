# Direct Fish speech and repeatable scene audio

Use this reference for an explicitly requested Fish remake, automatic scene-audio processing, or a requested silence-trimmed derivative. It is independent of project location or deployment environment. Adapt to the project's existing producer/manifest schema rather than creating incompatible parallel records.

## Prepare the Fish performance

Resolve the authorized target voice from the request or maintained project decisions. Record provider, model/version, voice identifier or conditioning-reference hash, and synthesis settings. Reuse the same resolved identity across scenes; a matching identifier alone does not prove audible identity. Do not hardcode another project's voice, provider endpoint, credential location or default budget.

Use the wording statuses in the main skill. Keep source audio/excerpts for comparison when remaking recorded dialogue; preserve the supplied script and its provenance for newly authored lines. A normalized take is not a verbatim source remake. Hold unclear clauses rather than inventing, dropping or silently rewriting them. Quiet/nonlexical regions need source review, not fabricated speech.

Before synthesis, verify the actual video exists and matches its declared hash, streams, interval and measured timing. Establish the intended speech onset/window using samples, frames or rational PTS. Check text readiness and voice availability before spending. Reuse established permission and usage limits; a workflow restart does not reset them or require a repeated approval for unchanged authorized work.

Keep the original Fish response and a lossless decoded master. Place the new performance on its declared working clock with explicit delay and sample-rate handling. A take that does not fit needs a bounded correction or a held result; do not truncate words to fit. Tempo changes require support in the requested edit and a recorded factor. Silence padding cannot conceal missing content. Compare each take's actual words, numbers/names and identity, then check the delivered video pairing. New TTS timing and identical duration do not establish matching lip movement.

## Automatic scene processing

For requested automation, have the scene producer publish an atomic completion record only after the intended video bytes are finished. Each record needs:

- A unique scene ID and version; detect duplicate IDs across ready, pending and silent records before processing.
- The video asset path/identity and actual hash, selected interval and measured stream/time-base information.
- The source-audio interval or supplied-script provenance, dialogue text and wording status. Conversion additionally needs the actual acoustic source and its hash.
- The selected workflow, resolved voice/model/settings, intended speech offset/window and evidence that the source-to-video mapping was checked.
- An explicit audio policy: speech to process, unclear/pending, quiet/nonlexical to inspect, or intentionally silent. Identify reference-only pictures separately from finished target footage.

The consumer validates the record and its current files, then prepares only ready work. Seeing a new MP4 filename is not evidence of its dialogue. A reused motion-template interval, including in a wheel-only render, must never supply recorded speech. Recheck inputs if the producer changes bytes; use new versions for changed wording rather than reusing an old request identity.

Use one processing owner/lock for an output namespace, with sequential processing as a simple default; honor the job's resource/concurrency limits. Do not start a second watcher over the same work. Preserve incremental state and report queued, processing, ready, held and failed work honestly. Register output paths, hashes and actual video/audio pairing in the project's manifest. Starting a watcher is part of an automation request, not a side effect of reading this recipe.

## Reuse and interruption recovery

Separate synthesis identity from video-pairing identity:

- **Synthesis fingerprint:** exact text, provider/model/version, fixed voice/reference identity and every synthesis-affecting setting, including requested output format. For acoustic conversion, also bind the exact source interval/hash and converter configuration.
- **Pairing fingerprint:** actual video and generated-audio hashes, selected source interval, onset/window, sample rate/time base, any permitted speed adjustment and the processing recipe version. Trimming additionally binds thresholds, padding and the retained-interval map.

Verify cached file hashes and relevant decoded properties before reuse. A new video with the same exact speech request may reuse verified audio while receiving a new pairing; a changed processing recipe may rebuild local outputs without another synthesis request. A cache hit must restore the correct ready status, not leave a completed derivative marked pending.

Write durable request state before sending, hold the request lock, and retain sanitized request/response identifiers, usage and successful output hashes. Never assume a timeout means the provider did no work. Started or unknown requests require reconciliation before resubmission; do not automatically repay for ambiguous work. Record explicit rejections and use only a justified retry policy for known-safe failures. Use provider idempotency only when its actual guarantees are known.

Keep one cumulative usage/retry ledger across restarts and a bounded repair envelope. Distinguish estimated character-based cost from verified billing; local character limits are not provider-enforced dollar caps. Keep credentials and signed media URLs out of records. These controls apply within the existing task authorization and do not authorize new purchases, downloads or infrastructure.

## Silence trimming and timing checks

Always retain the full source-clock master and original inputs. A requested shortened version is a separate derivative: remove only verified excess quiet, retain configurable boundary padding and meaningful breaths/pauses, and cut picture and audio using the same retained intervals. Quiet music residue and soft consonants make energy thresholds fallible; inspect questionable cuts against the source. Do not prescribe one universal threshold or pause length.

Store a reversible map of half-open retained source-video/frame and audio/sample intervals to contiguous edited-output intervals, with time bases and hashes. Check bounds, order, no missing retained content and complete output coverage. Compose this with the source-to-video map and recompute all dependent cues on the shortened clock. Do not use shortened audio against unchanged full-length pictures or programme timing.

Verify actual decoded sample/frame counts, leading silence, speech onsets/ends, both sides of cuts and the compressed delivery's delay/duration. Compare the clean PCM against the retained master samples; account explicitly for any mastering/resampling that prevents bit-exact comparison. Check complete decoding, levels and the selected audio stream, not merely a container duration or a ready flag. Recheck these properties after recipe changes and on verified cache reuse.

### Timing regression: tempo followed by delay

A measured FFmpeg 9 failure combined tempo processing with a nonzero delay: discontinuous audio PTS caused a later trim to discard intended leading silence and shorten the output. Rebuilding the working sample clock **after** delay repaired it; resetting timestamps only before delay did not. Treat this as a reproducible regression case for the actual installed build, not a claim that every FFmpeg version fails.

For a normalized 48 kHz working clip with a permitted tempo change, a representative repaired chain is:

```text
aresample=48000,atempo=1.1,adelay=24000S:all=1,asetpts=N/SR/TB,apad,atrim=end_sample=240000
```

The delay is 24,000 samples (0.5 s) and the intended output length is 240,000 samples (5 s). With an appropriate synthetic tone input that fits, independently decode the result and assert the exact sample count, 24,000 leading zero samples and intact subsequent audible content. Also test nonzero-delay-plus-tempo, delay-only and zero-delay cases on representative inputs. Replace these example values with the measured job contract; the chain is not permission to change delivery speed.

Preserve original provider takes while repairing timing locally. Re-run affected boundaries and dependent pair/trim/cache checks, then apply the skill's two-pass recheck protocol to the final hashes. Technical timing success remains separate from audible wording, identity and perceptual lip review.
