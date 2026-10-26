#!/usr/bin/env python3
"""Lower-face contact sheets for every face-on-screen frame range, to look at with your own eyes.

Usage: python3 mouth_sheets.py VIDEO.mp4 OUT_DIR START-END [START-END ...] [--fps 24] [--voice AS_PLAYED.flac]

One JPEG per range (8 crops per row, up to ~56 crops, each stamped with its time). With
--voice, a crop whose 1/fps audio frame is voiced gets a green "V" so silent mouthing and
voice over a closed mouth stand out at a glance.
Look at every sheet: a mouth open and shaping words with no "V" is silent mouthing; "V" over a
closed mouth is voice without lips. Pixel-motion or mouth-aperture numbers were too noisy to
trust (head turns, cuts to wide shots); they are not a substitute for looking.
Crops of a wall or a sleeve mean the face detector lost her (a cut to a wide shot) - not a defect.
"""
import argparse, sys
from pathlib import Path
import cv2, numpy as np

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('out'); ap.add_argument('ranges', nargs='+')
    ap.add_argument('--fps', type=float, default=24.0); ap.add_argument('--voice')
    ap.add_argument('--per-sheet', type=int, default=56)
    a = ap.parse_args()
    voiced = None
    if a.voice:
        import soundfile as sf
        v, sr = sf.read(a.voice, dtype='float32', always_2d=True); v = v.mean(1); spf = int(sr / a.fps)
        n = len(v) // spf
        voiced = np.sqrt((v[:n * spf].reshape(n, spf) ** 2).mean(1)) > 10 ** (-40 / 20)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(a.video); W = cap.get(cv2.CAP_PROP_FRAME_WIDTH); scale = W / 960
    for spec in a.ranges:
        s, e = map(int, spec.split('-')); tiles = []; box = None
        for f in range(s, e, max(1, (e - s) // a.per_sheet)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, img = cap.read()
            if not ok: break
            small = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (960, int(img.shape[0] / scale)))
            faces = cas.detectMultiScale(small, 1.1, 5, minSize=(40, 40))
            if len(faces): box = (max(faces, key=lambda q: q[2] * q[3]) * scale).astype(int)
            if box is None: continue
            x, y, w, h = box
            crop = cv2.resize(img[max(0, y + int(h * .45)):y + int(h * 1.05), max(0, x + int(w * .1)):x + int(w * .9)], (200, 120))
            cv2.putText(crop, f'{f / a.fps:.1f}s', (4, 14), cv2.FONT_HERSHEY_SIMPLEX, .45, (0, 255, 255), 1)
            if voiced is not None and f < len(voiced) and voiced[f]:
                cv2.putText(crop, 'V', (178, 16), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 255, 0), 2)
            tiles.append(crop)
        if not tiles: print(spec, 'no face found'); continue
        while len(tiles) % 8: tiles.append(np.zeros_like(tiles[0]))
        sheet = np.vstack([np.hstack(tiles[i:i + 8]) for i in range(0, len(tiles), 8)])
        cv2.imwrite(str(out / f'{s}-{e}.jpg'), sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
        print(spec, len(tiles), 'crops')

if __name__ == '__main__':
    sys.exit(main())
