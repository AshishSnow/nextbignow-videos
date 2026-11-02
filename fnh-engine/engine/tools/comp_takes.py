#!/usr/bin/env python3
"""ep 21 VOICE craft: TAKE COMPING. A voice actor records several takes and the editor keeps the best read of each line; same here. make_vo takes differ line by line (±0.1 UTMOS) even
with the same text. Usage: comp_takes.py <project> <alt_tag> [margin=0.03]  - alt take = work/vo_<alt_tag>.wav, work/align_<alt_tag>.json, work/vr_<alt_tag>.log (voice_report json).
The current take (work/vo.wav, align.json, voice_report.json) stays the base; a line is swapped in when its text is identical and it scores > margin higher. Lines are cut in the pauses
(with a 6 ms crossfade) and the original gaps are kept, so word timing just shifts; align.json is rewritten. Run voice_report afterwards to confirm the gate."""
import json, re, shutil, sys
import numpy as np, soundfile as sf
P, tag = sys.argv[1], sys.argv[2]; M = float(sys.argv[3]) if len(sys.argv) > 3 else 0.03
W = f"{P}/work"
y, sr = sf.read(f"{W}/vo.wav"); ya, _ = sf.read(f"{W}/vo_{tag}.wav")
A = json.load(open(f"{W}/align.json")); B = json.load(open(f"{W}/align_{tag}.json"))
ra = json.load(open(f"{W}/voice_report.json"))["utmos_lines"]; rb = json.loads(open(f"{W}/vr_{tag}.log").read().replace("DONE", ""))["utmos_lines"]
shutil.copy(f"{W}/vo.wav", f"{W}/vo_precomp.wav"); shutil.copy(f"{W}/align.json", f"{W}/align_precomp.json")
ids = list(A["lines"]); out = []; words = []; lines = {}; swapped = []; cur = 0; PAD0, PAD1 = 0.03, 0.06
fade = int(0.006 * sr)
for i, k in enumerate(ids):
    L = A["lines"][k]; src, Sa, s, e = y, A, L["start"], L["end"]
    if k in B["lines"] and B["lines"][k]["text"] == L["text"] and rb.get(k, 0) > ra.get(k, 0) + M:
        src, Sa, s, e = ya, B, B["lines"][k]["start"], B["lines"][k]["end"]; swapped.append((k, ra.get(k), rb.get(k)))
    if i == 0: gap = np.zeros(int((s - PAD0) * sr))
    else:
        pe = A["lines"][ids[i - 1]]["end"]; gap = np.zeros(max(0, int(round((L["start"] - pe - PAD0 - PAD1) * sr))))
    seg = src[int((s - PAD0) * sr):int((e + PAD1) * sr)].copy()
    seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
    out.append(gap); cur += len(gap); off = cur / sr + PAD0 - s
    lines[k] = dict(L); lines[k]["start"] = round(s + off, 3); lines[k]["end"] = round(e + off, 3)
    for w in Sa["words"]:
        if w["line"] == k: words.append(dict(w, t=round(w["t"] + off, 3)))
    out.append(seg); cur += len(seg)
tail = y[int((A["lines"][ids[-1]]["end"] + PAD1) * sr):]; out.append(tail)
z = np.concatenate(out).astype(np.float32); sf.write(f"{W}/vo.wav", z, sr, subtype="FLOAT")
A["lines"] = lines; A["words"] = words; A["dur"] = round(len(z) / sr, 3); json.dump(A, open(f"{W}/align.json", "w"), indent=0)
print("swapped", swapped, "dur", A["dur"])
