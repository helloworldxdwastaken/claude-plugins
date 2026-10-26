#!/usr/bin/env python3
"""Check every scheduled speech window exactly as a window-gated player lets it through.

Usage: python3 speech_windows_pass.py STEM.flac WINDOWS.json OUT_DIR [--fps 24] [--models large-v3-turbo,small.en]

WINDOWS.json: [{"id": str, "startFrame": int, "endFrame": int,
                "clipStartSample48k": int?, "clipEndSample48k": int?}, ...] on the stem's clock.

Writes OUT_DIR/voice-as-played.flac (stem inside windows, silence elsewhere) and
OUT_DIR/speech-windows.json, and prints one row per window:
  - text from each ASR model (audio resampled to 16 kHz with 0.5 s padding: faster-whisper
    treats a raw numpy array as 16 kHz, so 48 kHz input returns confident nonsense);
  - head/tail RMS of the first/last 50 ms (above about -60 dB = audible cut or click at the gate);
  - peak and active-speech RMS (clipping, level jumps between lines);
  - lead/slack between the window and the clip bounds; overlap with the previous window.
ASR is a flag for listening, not a verdict: two models disagreeing on a soft first word is
normal; a line that reads as different words in both models needs a listen.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np, soundfile as sf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('stem'); ap.add_argument('windows'); ap.add_argument('out')
    ap.add_argument('--fps', type=float, default=24.0)
    ap.add_argument('--models', default='large-v3-turbo,small.en')
    a = ap.parse_args()
    import librosa
    from faster_whisper import WhisperModel
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    x, sr = sf.read(a.stem, dtype='float32', always_2d=True)
    mono = x.mean(1)
    windows = sorted(json.load(open(a.windows)), key=lambda w: w['startFrame'])
    models = {name: WhisperModel(name, device='cpu', compute_type='int8') for name in a.models.split(',')}
    db = lambda v: round(20 * np.log10(max(float(v), 1e-9)), 1)
    rms = lambda s: float(np.sqrt(np.mean(s ** 2))) if len(s) else 0.0
    played = np.zeros_like(x); rows = []; prev_end = -1
    for w in windows:
        s0, s1 = round(w['startFrame'] / a.fps * sr), round(w['endFrame'] / a.fps * sr)
        seg = mono[s0:s1]; played[s0:s1] = x[s0:s1]
        frames = seg[:len(seg) // 480 * 480].reshape(-1, 480); energy = np.sqrt((frames ** 2).mean(1))
        active = energy[energy > energy.max() * 0.1] if len(energy) else energy
        edge = int(0.05 * sr)
        padded = np.concatenate([np.zeros(sr // 2, 'float32'), seg, np.zeros(sr // 2, 'float32')])
        audio16 = librosa.resample(padded, orig_sr=sr, target_sr=16000)
        text = {}
        for name, m in models.items():
            segments, _ = m.transcribe(audio16, language='en', beam_size=5, temperature=0, condition_on_previous_text=False)
            text[name] = ' '.join(t.text.strip() for t in segments)
        cs, ce = w.get('clipStartSample48k'), w.get('clipEndSample48k')
        row = dict(id=w.get('id'), t=round(s0 / sr, 2), frames=[w['startFrame'], w['endFrame']], text=text,
                   head_db=db(rms(seg[:edge])), tail_db=db(rms(seg[-edge:])), peak_db=db(np.abs(seg).max() if len(seg) else 0),
                   speech_rms_db=db(np.sqrt((active ** 2).mean())) if len(active) else None, overlap_prev=s0 < prev_end,
                   lead_s=round(cs / 48000 - s0 / sr, 3) if cs is not None else None,
                   slack_s=round(s1 / sr - ce / 48000, 3) if ce is not None else None)
        rows.append(row); prev_end = s1
        print(f"{row['t']:8.2f} {str(row['id'])[:32]:32} head {row['head_db']:6} tail {row['tail_db']:6} peak {row['peak_db']:5} "
              f"rms {row['speech_rms_db']} | " + ' | '.join(text.values()), flush=True)
    sf.write(out / 'voice-as-played.flac', played, sr)
    json.dump(rows, open(out / 'speech-windows.json', 'w'), indent=1)
    flags = [r for r in rows if r['head_db'] > -60 or r['tail_db'] > -60 or r['peak_db'] > -1 or r['overlap_prev']]
    print(f"{len(rows)} windows; {len(flags)} with edge/peak/overlap flags: {[r['id'] for r in flags]}")

if __name__ == '__main__':
    sys.exit(main())
