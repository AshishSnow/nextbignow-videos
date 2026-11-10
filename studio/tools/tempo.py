#!/usr/bin/env python3
"""Pace fix for Chatterbox (11 Nov 2026, Netflix 2011): the narrator_hype reference speaks ~170 wpm inside phrases, so even after
trim_gaps the overall pace sat at ~155 wpm (VOICE.md target 165-180). Chatterbox Turbo has no speed knob and Praat PSOLA re-timing cost
0.06-0.09 per-line UTMOS (R&D 10 Nov, rejected). ffmpeg's `atempo` (WSOLA, pitch kept) at 1.05 on the same trimmed take cost only
-0.021 per-line UTMOS (4.380 -> 4.359) for +7.7 wpm (155.2 -> 162.9); range 20.1 st unchanged; rubberband was far worse (2.47).
Usage: tempo.py <project> [factor=1.05]   (run after comp_takes + trim_gaps, before voice_report / music / mix)
Backs up work/vo_pretempo.wav + align_pretempo.json, stretches work/vo.wav, scales every time in work/align.json by 1/factor."""
import sys, json, shutil, subprocess
P = sys.argv[1]; F = float(sys.argv[2]) if len(sys.argv) > 2 else 1.05
W = f"{P}/work"
shutil.copy(f"{W}/vo.wav", f"{W}/vo_pretempo.wav"); shutil.copy(f"{W}/align.json", f"{W}/align_pretempo.json")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W}/vo_pretempo.wav", "-af", f"atempo={F}", "-c:a", "pcm_f32le", f"{W}/vo.wav"], check=True)
A = json.load(open(f"{W}/align_pretempo.json")); k = 1 / F
for L in A["lines"].values():
    for key in ("start", "end"): L[key] = round(L[key] * k, 3)
for w in A["words"]: w["t"] = round(w["t"] * k, 3)
for key in ("dur", "duration"):
    if key in A: A[key] = round(A[key] * k, 3)
json.dump(A, open(f"{W}/align.json", "w"))
print(f"tempo x{F}: dur {A.get('dur', '?')}")
