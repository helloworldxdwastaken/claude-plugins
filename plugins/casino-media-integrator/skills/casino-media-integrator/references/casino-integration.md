# Local integration entrypoints — checked 21 October 2026

Locate the current checkout and read README first. At authoring the local checkout was `/Users/enmanuel/Desktop/Desktop/AI casino`; the current VPS is a separate deployment. Do not copy local play-money prompts, state or old AIMODULE procedures into it without comparing actual contracts.

Discover current contracts and their callers in:

- `app/src/streamProgram.ts`, `programFrames.ts`, `programPrefix.ts`, `programPresentationRevision.ts`: programme/frame/prefix/version relationships.
- `app/server/programAssets.ts`, `programCueAssets.ts`: byte/hash and readiness admission; verify actual consumers before changing manifests.
- `app/src/programDialogueAdmission.ts`, `recordedProgramSpeech.ts`, `verifiedProgramAudio.ts`, `ProgramRecordedSpeech.tsx`, `programReplyWindow.ts`: dialogue eligibility, identity-bound assets, source-window and voice playback rules.
- `app/src/programWheelTimeline.ts`, `programWheelView.ts`, `programRound.ts`, `ProgramCamera.tsx`: picture/result phase relationship and camera composition. Inspect server result/event contracts as well; presentation code is not outcome authority.

Relevant existing tests include `app/tests/program-dialogue-admission.test.ts`, `program-assets.test.ts`, `program-assets-metadata-collision.test.ts`, `verified-program-audio.test.ts`, `program-result-voice.test.ts`, `program-replay.test.ts`, `program-transition.test.ts`, `program-append.test.ts` and `ref1-complete-audio-admission.test.ts`. Select tests from the actual changed dependencies and current package scripts; filenames alone do not prove a change is covered. Use the current pinned runtime, not arbitrary global Node.

Direct Fish scene review is separate from live admission. `audio/fish-scenes/README.md`, maintained scene/talk plans, manifest/CSV and per-scene cut maps describe review pairs. Completion descriptors require actual video hashes, verified timing, unique IDs and checked text. `scripts/media/fish_scene_watch.py --watch --run` can spend on synthesis; do not start it while staging existing assets. Existing review routes/readers are disabled in production and should remain scoped accordingly.

Snapshot limitations in the current README: later source units use reference-only pictures because selected target video ends468.916667s; some wording is unresolved; quiet/nonlexical detector spans are not dialogue. Review assets are not automatically the selected game's soundtrack. An empty-wheel render's motion-template range does not carry source-number speech. A successful paired clip does not prove live round/voice/cut eligibility.

Inspect scripts such as `scripts/media/append-native-program.py` before use; historical paths/version assumptions and write/service effects require checking. Work on an isolated candidate; do not invoke a script merely because its name sounds like an admission test.

`append-native-program.py --prefix ... --append ... --output ...` assembles review-only native 1080p24 video and verifies decoded prefix/frame/PTS preservation. It removes audio and leaves camera/HUD/wheel/audio admission pending. It does not produce a live-ready programme by itself. `app/scripts/audit-program-timing.mts` defaults to an old version 3; discover and pass the actual candidate version explicitly. Likewise use `getStreamProgram(actualVersion)` rather than old top-level frame-count defaults. The checked local v9 has 11254 frames at 24 fps / eight wheel slots; resolve current metadata rather than hardcoding those snapshot values.

Current recorded-speech contracts require unique IDs, nonoverlapping half-open frame ranges, exact 48 kHz whole-utterance samples and neutral/open-only policy. Admission additionally fences source epoch/version/generation/cycle, recent painted frame, readiness, seeking/visibility/recovery, playback rate and competing runtime voice. Open-only and reply windows need their real reservation/exit guards; retaining equivalent wall-clock duration alone does not establish eligibility.
