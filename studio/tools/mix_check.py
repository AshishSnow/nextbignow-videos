#!/usr/bin/env python3
"""Mix check on a simulated phone speaker (300 Hz-10 kHz): is every word clearly above the music + SFX?

Usage: python3 studio/tools/mix_check.py <project> [TAG]
Needs work/stem_vo[_TAG].wav + work/stem_bed[_TAG].wav (written by mix.py) and work/align.json; reads work/mix[_TAG].wav for loudness.
Prints and writes work/mix_check[_TAG].json:
  ld_line_min / ld_line_mean  per-line loudness difference voice - bed in LU (K-weighted, phone band). Target >= 10 LU
                              (Torcoli et al., JAES 2019: commentary over music >= 10 LU; non-experts prefer ~4 LU more).
  ld_m_p5 / ld_m_lt10         400 ms momentary LD during speech: 5th percentile, and % of windows under 10 LU (SFX hits on words).
  estoi / estoi_full          ESTOI of phone(voice) vs phone(voice + bed), and the same full-band (1.0 = bed takes nothing away).
  I / TP                      integrated loudness and true peak of the final mix (ffmpeg ebur128).
"""
import sys, json, subprocess, numpy as np, soundfile as sf
from scipy import signal
import pyloudnorm as pyln
from pystoi import stoi

B = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else ""
sfx = f"_{tag}" if tag else ""
SR = 48000
vo, _ = sf.read(f"{B}/work/stem_vo{sfx}.wav", dtype="float64"); vo = vo if vo.ndim == 1 else vo.mean(1)
bed, _ = sf.read(f"{B}/work/stem_bed{sfx}.wav", dtype="float64"); bed = bed if bed.ndim == 1 else bed.mean(1)
n = min(len(vo), len(bed)); vo, bed = vo[:n], bed[:n]
sos = signal.butter(4, [300, 10000], "band", fs=SR, output="sos")
pv, pb = signal.sosfilt(sos, vo), signal.sosfilt(sos, bed)
meter = pyln.Meter(SR)
lines = json.load(open(f"{B}/work/align.json"))["lines"]


def lufs(x):
    if len(x) < int(0.45 * SR): x = np.pad(x, (0, int(0.45 * SR) - len(x)))
    v = meter.integrated_loudness(x); return v if np.isfinite(v) else -70.0


per = {}
for k, L in lines.items():
    a, b = int(L["start"] * SR), int(L["end"] * SR)
    if b - a < int(0.2 * SR): continue
    per[k] = round(lufs(pv[a:b]) - lufs(pb[a:b]), 1)
# momentary 400 ms windows inside speech (K-weighting via pyloudnorm's filters applied once)
kv = pv.copy(); kb = pb.copy()
for f in meter._filters.values(): kv = f.apply_filter(kv) if hasattr(f, "apply_filter") else kv; kb = f.apply_filter(kb) if hasattr(f, "apply_filter") else kb
w, h = int(0.4 * SR), int(0.1 * SR); mom = []
spans = [(int(L["start"] * SR), int(L["end"] * SR)) for L in lines.values()]
for a, b in spans:
    for s in range(a, max(a + 1, b - w), h):
        ev = np.mean(kv[s:s + w] ** 2); eb = np.mean(kb[s:s + w] ** 2)
        if ev < 1e-9: continue
        mom.append(10 * np.log10(ev / (eb + 1e-14)))
mom = np.array(mom)
fs_ = 10000
es = stoi(signal.resample_poly(pv, 5, 24), signal.resample_poly(pv + pb, 5, 24), fs_, extended=True)
esf = stoi(signal.resample_poly(vo, 5, 24), signal.resample_poly(vo + bed, 5, 24), fs_, extended=True)
out = {"ld_line_min": min(per.values()), "ld_line_min_id": min(per, key=per.get), "ld_line_mean": round(float(np.mean(list(per.values()))), 2),
       "ld_lines_lt10": [k for k, v in per.items() if v < 10], "ld_m_p5": round(float(np.percentile(mom, 5)), 1),
       "ld_m_lt10_pct": round(float(np.mean(mom < 10) * 100), 1), "estoi": round(float(es), 4), "estoi_full": round(float(esf), 4), "per_line": per}
mp = f"{B}/work/mix{sfx}.wav"
try:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    t = r.stderr; out["I"] = float(t.split("I:")[-1].split("LUFS")[0]); out["TP"] = float(t.split("Peak:")[-1].split("dBFS")[0])
    out["LRA"] = float(t.split("LRA:")[-1].split("LU")[0])
except Exception as e:
    out["I"] = None
json.dump(out, open(f"{B}/work/mix_check{sfx}.json", "w"), indent=1)
print(f"{B.rstrip('/').split('/')[-1]} {tag or '-'}: LD line min {out['ld_line_min']} ({out['ld_line_min_id']}) mean {out['ld_line_mean']} "
      f"lines<10LU {len(out['ld_lines_lt10'])}/{len(per)} | momentary p5 {out['ld_m_p5']} <10LU {out['ld_m_lt10_pct']}% | ESTOI phone {out['estoi']} full {out['estoi_full']} | "
      f"I {out.get('I')} TP {out.get('TP')} LRA {out.get('LRA')}")
