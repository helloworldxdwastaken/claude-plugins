---
name: code-to-lottie
description: Use when converting a coded animation to a Lottie .json (bodymovin) — "export this as lottie", "svg to lottie", "css animation to lottie", HTML/CSS keyframe loaders or logo animations for lottie-web/lottie-ios/lottie-android/Telegram — and when a generated Lottie renders broken, displaced, or must be re-verified against its source.
---

# code-to-lottie

Convert tagged SVG + CSS-keyframe animations into Lottie JSON, then **prove**
the export matches. Core principle: conversion is easy to get silently wrong —
every Lottie leaves this skill with three verification stages passing.

## When NOT to use
After Effects projects (use the bodymovin plugin); video/GIF → Lottie (those
wrap raster frames, never true vectors).

## Pipeline

1. **Tag the source.** Each animated piece gets `class="lottie-part"` and
   `style="--i: N"` (stagger order, N from 0). One part = one fill (split
   differently-colored pieces into separate parts; a `<g class="lottie-part">`
   with a transform/fill is one part). A CSS block defines ONE `@keyframes`
   rule (opacity / `scale()` / `translate()` only) and the part rule:
   `animation: <name> <dur>s <easing> infinite; animation-delay: calc(var(--i, 0) * 100ms);`
   `<text>` is NOT a Lottie shape — convert it with `text_to_paths()`
   (fontTools; macOS SFNS.ttf, variable wght) and splice the returned subpaths
   in as parts.
2. **Convert:** `python3 scripts/svg2lottie.py source.svg --out anim.json`
   (reads embedded `<style>`, or pass `--css`; `--fps`, `--pad`, `--name`).
   The comp auto-crops to the parts' union bbox + `--pad` (default 4px), so a
   smaller canvas than the source svg is expected, not clipping.
3. **Verify — REQUIRED, all three stages:**
   - `python3 scripts/verify_lottie.py source anim.json` → **stage 1 timing**
     (keyframe times/values/easing vs the source CSS) + **stage 2 geometry**
     (sampled curve round-trip, ≤ 0.05px). Fix the generator until PASS.
   - **stage 3 pixel diff:** `... --diff` writes a self-contained `diff.html`
     (needs `lottie.min.js` — download from cdnjs `bodymovin/5.12.2` once per
     project).
   - Render proof: headless chromium `--dump-dom` and read the match % in the
     page title (or open the page). **≥ 99% passes** — rasterizer
     antialiasing eats the rest. If < 99%, fix the generator, never the JSON.
4. **Deliver** a self-contained viewer page (player JS + JSON inlined) so
   anyone can open it.

## Gotchas — each was a real render-breaking bug once

- Tangents (`i`/`o`) are **relative** vectors: when repositioning a shape,
  translate vertices only, never tangents. Symptom if violated: scribbles.
- Shape vertices are stored **relative to the layer anchor**; layer position =
  the part's bbox center (so `scale()` pops around the part's own center).
  Storing absolute coords double-offsets every part. Symptom: scattered parts.
- Delayed parts: clamp keyframe times into the loop window (dedupe stops that
  land on the same frame) or the loop seam pops.
- `file://` blocks `fetch()` — inline JSON into the page or via `<script>`.
- lottie-web's canvas renderer needs its container attached to the DOM.
- Headless screenshots: prefer `setTimeout` waits over `requestAnimationFrame`
  under virtual time budgets.
- PEP 668: install fontTools in a venv, not system pip.
- Lottie keyframes: value `s` AT time `t`; easing pair `o`/`i` = css
  cubic-bezier control points (`ease-out` → o:{0,0} i:{0.58,1}).

## Red flags — stop, you are off the pipeline

- "The JSON looks right" without rendering — Lottie bugs are visual.
- Geometry passed so skipping the pixel diff — they catch different bug classes.
- Hand-editing the JSON to fix a render instead of fixing the generator
  (the verify stages re-run against the generator).
- Declaring done without the ≥99% pixel-match number printed.
