# Existing casino audio recipe — checked 21 October 2026

Locate the current checkout; at authoring it was `/Users/enmanuel/Desktop/Desktop/AI casino`. Read its current `README.md` before adapting scripts. Paths below refer to that checkout. No media, voice embeddings, weights or secrets are bundled in this skill.

## Voice identity and scope

Katie's reference is `assets/review/ref1-katie-voice-2026-10-01/katie-reference.wav`, 6.269388 s, SHA256 `5b7bc2d7f72289765861260f64a92cb4bb31d35a5383c1438b7d8f3f73962c8a`. It was generated with Fish S2.1-Pro using voice ID `e50892cb63894e289aded9ebd961ec66`; it is a synthetic library-voice sample. Preserve it rather than regenerating/changing the target. Recheck actual bytes and the current project decision before reuse.

Current Local DEV has live Fish TTS through OpenRouter for new replies/announcements and a separate recorded source-converted stem. The selected programme9 v3 FLAC is 468.916667 s with eight admitted cue spans, not full original-word coverage. The owner-approved private 600 s hybrid is another artifact; it contains recorded results and is unsuitable as unconditional live speech. Prior owner approval remains valid, while exact-word/heard-identity/perceptual-lip certification remains a separate question.

## Proven local mechanics and bounded alternatives

The 600 s source extraction used 48 kHz stereo samples `[156800,28956800)` mapped to programme `[0,28800000)`, an offset of 3.266666667 s. This is specific to that recording; measure new sources.

Existing reproducible scripts live under `assets/review/ref1-complete-katie-audio-2026-10-08/audio-worker/`. Inspect/adapt their hardcoded historical paths and receipts before any execution:

| Stage | Existing script and decision |
| --- | --- |
| Extraction/separation | `prepare_original_isolated.py`: cached TorchAudio HDEMUCS_HIGH_MUSDB_PLUS, matching Torch/TorchAudio 2.3.0; 44.1 kHz separator, 10 s windows/1 s overlap with weighted reconstruction, return to programme clock |
| Speech support | `build_speech_support.py`: union of original/isolated Silero probabilities, thresholds .25/.12, 750 ms padding, 5 ms outer fades. These are measured project settings, not guaranteed preservation thresholds |
| Primary conversion | `convert_source_contexts.py`: Seed-VC, real context handles plus distinct 250 ms zero guards, length 1.0, seed 711, 30 steps, guidance .7. Reject native output loss entering retained speech |
| Local retries | `convert_source_spans.py`: FP32 semantic loading and selected 50-step/1.2 guidance attempts; some improved words, some failed. More steps are not a guarantee |
| Alternate converter | `convert_openvoice_direct_pilots.py`: OpenVoice v2 direct acoustic conversion with natural amplitude, tau 0, utterance-specific source embedding and fixed Katie target embedding; no TTS |
| Dynamics | `reshape_project_dynamics.py`: continuous 10 ms RMS-based shaping with 5 ms smoothing; addresses clicks from per-zero-crossing masking and excessive quiet-residue gain |
| Assembly | `assemble_private_katie600.py`: selected whole cores and genuine same-source overlap joins; independently reconstructed on the fixed sample clock |

The earlier Seed-VC installation used commit `51383efd921027683c89e5348211d93ff12ac2a8`, Whisper-small conditioning, FP32 CPU; later measured MPS conversion was faster with the same cached weights. A process-only workaround addressed disabled FP32 MPS autocast with old Torch. Do not edit upstream tools or assume this compatibility workaround is still needed. Current hardware/runtime decides feasibility.

Silero 6.2.3 was pinned to commit `5cd7945676eb32225748052e2e6a0580e4686a08` and model SHA256 `e1122837f4154c511485fe0b9c64455f7b929c96fbb8d79fbdb336383ebd3720`. Preserve source privacy and exact model provenance; do not blindly redownload.

The final historical 600 s selection combined 32 OpenVoice and 22 Seed-VC units. Independent checks covered all 28.8 million stereo frames, complete FLAC decoding, same-source joins and zero samples outside selected support. Browser picture/audio clock observations reached about 94 ms; they did not establish phoneme or perceptual lip sync. Early ASR audits found lost/garbled words; later owner acceptance does not erase those limitations.

Do not install the full recorded result calls into live game audio. Do not replace direct conversion with a rewritten Fish script merely because the reference was made by Fish. For an explicitly requested new direct-Fish performance, use [the Fish scene workflow](fish-scene-workflow.md) with its own timing and wording checks. Existing authorization persists within its scope; the new workflow does not imply an extra approval for unchanged authorized work.

## Direct sources

- Local: README entries 1 October source-to-Katie conversion, 8 October complete source speech/hybrid assembly, 21 October audio audit; `docs/audits/2026-10-21-local-dev-audio-and-deepseek.md`; `audio-worker/FINAL-PRIVATE600-HANDOFF.md` and assembly/word-review receipts in the same review tree.
- [TorchAudio Hybrid Demucs tutorial](https://docs.pytorch.org/audio/main/tutorials/hybrid_demucs_tutorial.html): separation implementation, not a promise of clean speech.
- [Seed-VC](https://github.com/Plachtaa/seed-vc): direct voice-conversion implementation.
- [Seed-VC v2 preservation wrapper](https://github.com/Plachtaa/seed-vc/blob/main/modules/v2/vc_wrapper.py): `convert_style=False` is a content-preservation option; not established as the winning selected casino take.
- [OpenVoice pinned implementation](https://github.com/myshell-ai/OpenVoice/blob/74a1d147b17a8c3092dd5430504bd83ef6c7eb23/openvoice/models.py): acoustic conversion path.
- [Silero VAD](https://github.com/snakers4/silero-vad): speech support inference, not a word-preservation oracle.

These upstream links explain algorithms; successful installation, identity match, source-word preservation and synchronization require evidence from the actual local output.
