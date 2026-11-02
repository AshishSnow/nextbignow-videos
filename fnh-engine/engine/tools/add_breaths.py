#!/usr/bin/env python3
"""ep 21 VOICE craft: soft in-breaths in the pauses before long lines, so the narrator sounds like a person who needs air.
Writes ONLY inside existing gaps (timing and the word alignment do not change). Usage: add_breaths.py <project> [level_db=-30] [min_words=11]
A real in-breath: ~0.2-0.35 s, broadband noise shaped by the vocal tract (peaks ~900 + ~2300 Hz), a fast rise and a slower fall, ending just before the
voice starts; levels in voice-over practice are kept well under the speech (de-breathed to about -25...-35 dB relative). Only before lines of >= min_words
words (a person doesn't breathe before 'Yep.'), never at the very start, and only when the gap is long enough. Keeps work/vo_nobreath.wav for A/B."""
import json, os, shutil, sys
import numpy as np, soundfile as sf
from scipy import signal
P = sys.argv[1]; LV = float(sys.argv[2]) if len(sys.argv) > 2 else -30.0; MW = int(sys.argv[3]) if len(sys.argv) > 3 else 11
src = f"{P}/work/vo_nobreath.wav"
if not os.path.exists(src): shutil.copy(f"{P}/work/vo.wav", src)
y, sr = sf.read(src); y = y.astype(np.float64)
A = json.load(open(f"{P}/work/align.json")); L = A["lines"]; ids = list(L.keys())
rms = np.sqrt(np.mean(y[np.abs(y) > 0.01] ** 2)); rng = np.random.default_rng(21); done = []
for i, k in enumerate(ids):
    if i == 0: continue
    gap = L[k]["start"] - L[ids[i - 1]]["end"]; nw = len(L[k].get("text", "").split()) or sum(1 for w in A["words"] if w["line"] == k)
    if nw < MW or gap < 0.26: continue
    dur = min(0.34, gap - 0.08) * rng.uniform(0.85, 1.0); n = int(dur * sr)
    e = int((L[k]["start"] - 0.035) * sr); s = e - n
    if s < 0: continue
    z = rng.standard_normal(n + 2048)
    b1 = signal.sosfilt(signal.butter(2, [650, 1250], "band", fs=sr, output="sos"), z)
    b2 = signal.sosfilt(signal.butter(2, [1900, 2900], "band", fs=sr, output="sos"), z)
    b3 = signal.sosfilt(signal.butter(2, 4200, "high", fs=sr, output="sos"), z)
    br = (b1 + 0.75 * b2 + 0.12 * b3)[2048:]
    x = np.arange(n) / max(1, n - 1); env = np.minimum(x / 0.28, 1) ** 1.5 * np.minimum((1 - x) / 0.5, 1) ** 1.2
    br = br * env; br = br / (np.sqrt(np.mean(br ** 2)) + 1e-12) * rms * 10 ** (LV / 20) * rng.uniform(0.8, 1.1)
    y[s:e][: len(br)] += br[: e - s]; done.append(k)
y = np.clip(y, -0.999, 0.999); sf.write(f"{P}/work/vo.wav", y.astype(np.float32), sr, subtype="FLOAT")
print("breaths before", done, "level", LV)
