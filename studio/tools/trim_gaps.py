#!/usr/bin/env python3
"""Cap dead air INSIDE a line (8 Nov 2026, Prime 'Iliad'): Chatterbox sometimes leaves 2.1-2.4 s of silence between two sentences of the
same line (b3, i5, b2 there), which breaks VOICE.md's pause rule (sentence ends 350-500 ms, never > 1 s) and drags the picture.
Usage: trim_gaps.py <project> [max_s=0.65] [to_s=0.45] [--dry]
Finds silent runs (20 ms RMS < -40 dBFS) longer than max_s that lie strictly between two words of one line, shortens each to to_s (cut from the
middle, 10 ms crossfade), and shifts every later word/line time in work/align.json. Pauses BETWEEN lines (the designed beats) are left alone.
Backs up work/vo_pretrim.wav + align_pretrim.json. Run voice_report afterwards."""
import sys, json, shutil
import numpy as np, soundfile as sf

P = sys.argv[1]; args = [a for a in sys.argv[2:] if not a.startswith("--")]
MAX = float(args[0]) if args else 0.65; TO = float(args[1]) if len(args) > 1 else 0.45; DRY = "--dry" in sys.argv
W = f"{P}/work"
y, sr = sf.read(f"{W}/vo.wav", dtype="float32"); A = json.load(open(f"{W}/align.json"))
mono = y.mean(1) if y.ndim > 1 else y
h = int(0.02 * sr); thr = 10 ** (-40 / 20)
cuts = []   # (cut_start_s, cut_len_s, line)
for k, L in A["lines"].items():
    ws = sorted(w["t"] for w in A["words"] if w["line"] == k)
    if len(ws) < 2: continue
    a0, a1 = int(L["start"] * sr), int(L["end"] * sr); s = mono[a0:a1]
    e = np.array([np.sqrt(np.mean(s[i:i + h] ** 2)) for i in range(0, max(0, len(s) - h), h)])
    run = 0
    for i, v in enumerate(list(e < thr) + [False]):
        if v: run += 1; continue
        if run * 0.02 > MAX:
            r0 = L["start"] + (i - run) * 0.02; r1 = L["start"] + i * 0.02
            if ws[0] < r0 and r1 < ws[-1] + 0.05 and any(t >= r1 - 0.05 for t in ws):
                cut = (r1 - r0) - TO; cuts.append((r0 + TO / 2, cut, k))
        run = 0
print("cuts:", [(k, round(c0, 2), round(c, 2)) for c0, c, k in cuts])
if DRY or not cuts: sys.exit(0)
shutil.copy(f"{W}/vo.wav", f"{W}/vo_pretrim.wav"); shutil.copy(f"{W}/align.json", f"{W}/align_pretrim.json")
fade = int(0.01 * sr); out = []; pos = 0
for c0, c, _ in sorted(cuts):
    i0, i1 = int(c0 * sr), int((c0 + c) * sr)
    seg = y[pos:i0].copy(); seg[-fade:] *= np.linspace(1, 0, fade)[:, None] if y.ndim > 1 else np.linspace(1, 0, fade)
    out.append(seg); pos = i1
    nxt = y[pos:pos + fade].copy(); y[pos:pos + fade] = nxt * (np.linspace(0, 1, fade)[:, None] if y.ndim > 1 else np.linspace(0, 1, fade))
out.append(y[pos:]); z = np.concatenate(out)


def shift(t):
    return t - sum(c for c0, c, _ in cuts if c0 + c <= t + 1e-6)


for w in A["words"]: w["t"] = round(shift(w["t"]), 3)
for L in A["lines"].values(): L["start"] = round(shift(L["start"]), 3); L["end"] = round(shift(L["end"]), 3)
A["dur"] = round(len(z) / sr, 3)
sf.write(f"{W}/vo.wav", z, sr, subtype="FLOAT"); json.dump(A, open(f"{W}/align.json", "w"), indent=0)
print("trimmed", round(sum(c for _, c, _ in cuts), 2), "s; dur", A["dur"])
