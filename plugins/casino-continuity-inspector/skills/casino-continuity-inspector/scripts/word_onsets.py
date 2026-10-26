#!/usr/bin/env python3
"""Lip-sync proxy: compare word onsets of the delivered voice with the original speech the
picture was performed to, per speech window, on the shared programme clock.

Usage: python3 word_onsets.py DELIVERED.flac ORIGINAL.wav WINDOWS.json [--fps 24] [--pad 0.6]

When the video copies the original performance's timing (motion transfer, reviewed source
footage), the original word times stand in for the lip times. A matched word's onset
difference (delivered - original) is the voice lead (negative) or lag (positive) against the
lips. Prints per-window median and matched-word count. Medians beyond about +/-150 ms over a
visible face deserve a look; fewer than 3 matched words is not evidence either way.
Both inputs are resampled to 16 kHz before ASR (faster-whisper assumes 16 kHz arrays).
"""
import argparse, difflib, json, re, sys
import numpy as np, soundfile as sf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('delivered'); ap.add_argument('original'); ap.add_argument('windows')
    ap.add_argument('--fps', type=float, default=24.0); ap.add_argument('--pad', type=float, default=0.6)
    ap.add_argument('--model', default='large-v3-turbo')
    a = ap.parse_args()
    import librosa
    from faster_whisper import WhisperModel
    m = WhisperModel(a.model, device='cpu', compute_type='int8')
    load = lambda p: (lambda x, sr: (x.mean(1), sr))(*sf.read(p, dtype='float32', always_2d=True))
    d, dsr = load(a.delivered); o, osr = load(a.original)
    def words(x, sr, t0, t1):
        if t1 * sr > len(x): return []
        seg = librosa.resample(x[int(t0 * sr):int(t1 * sr)], orig_sr=sr, target_sr=16000)
        segs, _ = m.transcribe(seg, language='en', word_timestamps=True, beam_size=5, temperature=0, condition_on_previous_text=False)
        return [(re.sub(r'[^a-z]', '', w.word.lower()), t0 + w.start) for s in segs for w in s.words]
    rows = []
    for w in sorted(json.load(open(a.windows)), key=lambda w: w['startFrame']):
        t0, t1 = max(0, w['startFrame'] / a.fps - a.pad), w['endFrame'] / a.fps + a.pad
        dw, ow = words(d, dsr, t0, t1), words(o, osr, t0, t1)
        if not ow: print(f"{t0:8.2f} {str(w.get('id'))[:32]:32} original not available/silent here"); continue
        sm = difflib.SequenceMatcher(a=[x for x, _ in dw], b=[x for x, _ in ow], autojunk=False)
        diffs = [dw[i][1] - ow[j][1] for blk in sm.get_matching_blocks() for i, j in zip(range(blk.a, blk.a + blk.size), range(blk.b, blk.b + blk.size)) if dw[i][0]]
        med = round(float(np.median(diffs)) * 1000) if diffs else None
        rows.append(dict(id=w.get('id'), t=round(t0 + a.pad, 2), matched=len(diffs), median_ms=med))
        print(f"{t0 + a.pad:8.2f} {str(w.get('id'))[:32]:32} matched {len(diffs):2} median {med} ms | D: {' '.join(x for x, _ in dw)} | O: {' '.join(x for x, _ in ow)}", flush=True)
    json.dump(rows, open('word-onsets.json', 'w'), indent=1)

if __name__ == '__main__':
    sys.exit(main())
