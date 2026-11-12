#!/usr/bin/env python3
"""Pace fix for Chatterbox (11 Nov 2026, Netflix 2011): the narrator_hype reference speaks ~170 wpm inside phrases, so even after
trim_gaps the overall pace sat at ~155 wpm (VOICE.md target 165-180). Chatterbox Turbo has no speed knob and Praat PSOLA re-timing cost
0.06-0.09 per-line UTMOS (R&D 10 Nov, rejected). ffmpeg's `atempo` (WSOLA, pitch kept) at 1.05 on the same trimmed take cost only
-0.021 per-line UTMOS (4.380 -> 4.359) for +7.7 wpm (155.2 -> 162.9); range 20.1 st unchanged; rubberband was far worse (2.47).
13 Nov (7-Eleven): x1.07 on a 3-take comp cost -0.025 per-line (4.463 -> 4.438) for 153.8 -> 164.9 wpm, but ASR then heard "ice dock" as
"iStock" (two short words fused when sped up, WRITING rule 25) -> `--keep i6` leaves the listed lines at normal speed (cut halfway into the
gaps around them) and stretches everything else: ASR clean, per-line 4.441, 164.6 wpm.
Usage: tempo.py <project> [factor=1.05] [--keep id1,id2]   (run after comp_takes + trim_gaps, before voice_report / music / mix)
Backs up work/vo_pretempo.wav + align_pretempo.json, stretches work/vo.wav, re-times every line/word in work/align.json."""
import sys, json, shutil, subprocess
import numpy as np, soundfile as sf
args = [a for a in sys.argv[1:] if not a.startswith("--keep")]
keep = []
for i, a in enumerate(sys.argv):
    if a.startswith("--keep"):
        v = a.split("=", 1)[1] if "=" in a else sys.argv[i + 1]
        keep = [x for x in v.split(",") if x]
        if "=" not in a and v in args: args.remove(v)
P = args[0]; F = float(args[1]) if len(args) > 1 else 1.05
W = f"{P}/work"
shutil.copy(f"{W}/vo.wav", f"{W}/vo_pretempo.wav"); shutil.copy(f"{W}/align.json", f"{W}/align_pretempo.json")
A = json.load(open(f"{W}/align_pretempo.json")); y, sr = sf.read(f"{W}/vo_pretempo.wav", dtype="float32")
L = A["lines"]; ids = list(L)
segs = []   # (t0, t1, stretch?) covering the file
cur = 0.0
for k in keep:
    if k not in L: continue
    i = ids.index(k)
    a = (L[ids[i - 1]]["end"] + L[k]["start"]) / 2 if i > 0 else 0.0
    b = (L[k]["end"] + L[ids[i + 1]]["start"]) / 2 if i + 1 < len(ids) else len(y) / sr
    if a > cur: segs.append((cur, a, True))
    segs.append((a, b, False)); cur = b
segs.append((cur, len(y) / sr, True))


def stretch(seg):
    sf.write(f"{W}/_t_in.wav", seg, sr, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/_t_in.wav", "-af", f"atempo={F}", "-c:a", "pcm_f32le", f"{W}/_t_out.wav"], check=True)
    return sf.read(f"{W}/_t_out.wav", dtype="float32")[0]


out, maps, pos = [], [], 0.0
for t0, t1, st in sorted(segs):
    seg = y[int(t0 * sr):int(t1 * sr)]
    o = stretch(seg) if st and len(seg) > 0 else seg
    maps.append((t0, t1, pos, len(o) / sr)); out.append(o); pos += len(o) / sr
sf.write(f"{W}/vo.wav", np.concatenate(out).astype(np.float32), sr, subtype="FLOAT")


def m(t):
    for t0, t1, p0, d in maps:
        if t0 <= t <= t1: return p0 + (t - t0) * (d / max(1e-9, t1 - t0))
    return pos
for Lx in L.values():
    for key in ("start", "end"): Lx[key] = round(m(Lx[key]), 3)
for w in A["words"]: w["t"] = round(m(w["t"]), 3)
for key in ("dur", "duration"):
    if key in A: A[key] = round(pos, 3)
json.dump(A, open(f"{W}/align.json", "w"))
print(f"tempo x{F}{' keep ' + ','.join(keep) if keep else ''}: dur {round(pos, 3)}")
