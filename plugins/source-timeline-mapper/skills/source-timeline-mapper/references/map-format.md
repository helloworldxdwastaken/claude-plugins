# Portable map export

The helper accepts a JSON export with `schema_version: 1`, a nonempty `assets` list and a nonempty `mappings` list. Each asset has unique `id`, `role` (`source` or `output`), `path`, lowercase SHA256 `sha256`, positive rational-string `time_base`, and positive integer `duration_ticks`. Paths are resolved against the map file. Normalized coordinate zero is the beginning of the decoded working asset; preserve original absolute PTS/origin/stream metadata separately in the same export if needed.

For CFR video one tick may be one frame (`time_base: "1/24"`); audio may use one sample (`"1/48000"`). For VFR use the actual presentation time base and duration, plus a separately inspected frame-PTS list. The checker does not inspect codec streams or validate supplied counts/time bases; the second checker must independently establish them.

Each mapping has unique `id`, `output` asset ID, integer `output_range: [start,end]`, and `status` (`provisional` or `verified`). A source-based mapping also has `source` asset ID, integer `source_range`, and rational-string `speed`: source elapsed seconds divided by output elapsed seconds. `"1"` means unchanged speed. Different native tick units are converted before comparison. Overlapping source ranges are permitted for explicitly mapped replays; output ranges may not overlap and must cover every output asset exactly.

An interval without source correspondence has `source: null`, no `source_range` or `speed`, and explicit `intent` of `intentional_silence` or `generated_cutaway`. This declares editorial intent only; it does not prove that audio is silent or that an unmapped shot is acceptable. Record the reason and validate the actual content separately. Do not label unknown/missing correspondence a cutaway to obtain a pass.

Example structure for one second of unchanged video:

```json
{
  "schema_version": 1,
  "assets": [
    {"id":"source","role":"source","path":"source.mp4","sha256":"replace-with-actual-hash","time_base":"1/24","duration_ticks":24},
    {"id":"candidate","role":"output","path":"candidate.mp4","sha256":"replace-with-actual-hash","time_base":"1/24","duration_ticks":24}
  ],
  "mappings": [
    {"id":"shot-1","source":"source","source_range":[0,24],"output":"candidate","output_range":[0,24],"speed":"1","status":"provisional"}
  ]
}
```

Run `python3 scripts/verify_timeline.py /absolute/path/map.json`. Run with `--require-verified` when verified mappings are required. Success establishes declared map structure/arithmetic and actual file hashes only. A provisional map may pass structural validation; the printed result identifies it. The helper does not set verification status, generate media, rewrite maps or activate assets.
