# Higgsfield capability notes — 21 October 2026

## Official product behavior

The [official Genjutsu page](https://higgsfield.ai/genjutsu) describes keeping source motion, camera and timing while rebuilding appearance from reference images. Its separate Lite offering has different duration limits.

The [official Genjutsu guide](https://higgsfield.ai/blog/higgsfield-genjutsu) distinguishes:

- **Motion Transfer:** extract the performance and rebuild the character and/or scene using supplied references.
- **Object Swap:** replace a specified element while preserving the surrounding shot.

The guide advertises one 4–30 s source video, up to 30 reference images (including character, outfit, object, product, location and style), an optional prompt/preset, and output up to 1080p. These are documented product limits, not fields enforced by the inspected CLI schema. Recheck the exact selected variant and route before splitting/uploading a job; do not transfer Lite limits or assume all providers implement the same inputs.

Additional official references: [editing existing footage](https://higgsfield.ai/blog/edit-ai-video-without-regenerating), [AI Influencer update](https://higgsfield.ai/blog/new-ai-influencer), and [multiple-character reference guidance](https://higgsfield.ai/blog/two-characters-one-scene-ai-video). These describe intended behavior; they do not prove face, garment, room or frame-exact fidelity on a specific render.

## Actual local CLI inspection

Read-only local checks actually ran:

```text
higgsfield model get hf_mult_replace_object --json
higgsfield model get hf_mult_motion_control --json
higgsfield generate cost --help
```

Both model schemas identify the display name as Genjutsu and accept image_references, video_references, prompt and resolution. The enforced schema rules require at least one image and exactly one video. Resolution choices are 480p, 720p and 1080p; default is 720p. The schema does not expose the underlying engine, duration limits, a scene_mode control, an identity guarantee or a lip-sync guarantee.

`generate cost --help` explicitly says local file paths are auto-uploaded. It estimates credits without creating a job. Inspecting a model is a different operation from quoting with private inputs.

Current capability discovery can begin with those read-only model/help commands. Follow current available tool/provider documentation for actual generation flags; the schema is not evidence that an invented `--scene_mode` flag works. It exposes no masks, seed, dedicated garment-detail controls or audio-preservation guarantee.

Historical project measurements demonstrate both performance-driven character replacement and October object/environment replacement attempts. They also demonstrate room, clothing, identity and cut drift. The old project assertion that Motion Transfer cannot replace rooms is superseded by current product guidance and newer attempts. Record current official documentation links and the exact mode selected in each new job receipt; product claims are separate from measurements on that job.
