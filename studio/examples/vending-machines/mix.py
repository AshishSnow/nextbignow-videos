"""Mix: narrator VO + ducked/carved funk score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
def st0(sid): return S[sid]
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(31)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
v, _ = sf.read(f"{B}/work/vo.wav", dtype="float32")
vo = np.zeros(NS, np.float32); vo[: min(NS, len(v))] = v[:NS]
VO = np.stack([vo, vo], 1)
m, _ = sf.read(f"{B}/work/music.wav", dtype="float32"); m = m[:NS]
if len(m) < NS: m = np.pad(m, ((0, NS - len(m)), (0, 0)))
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
M = m * (1 - 0.7 * g)[:, None]
# ---- VO level automation: per-line dB offsets (quiet "secret" lines ~-2.5, reveal lines ~+1) + -60 dB room tone in the gaps ----
LINE_DB = {"i1": +2.0, "t1": +1.0, "e3": +0.5, "e2": -1.0}   # hook + singer reveal up, the 1998 setup a touch quieter
gl = np.zeros(NS, np.float32)
for lid, L in LINES.items():
    a0, a1 = int(L["start"] * SR), int(L["end"] * SR); gl[a0:a1] = LINE_DB.get(lid, 0.0)
ramp = int(0.08 * SR); gl = np.convolve(gl, np.ones(ramp) / ramp, "same").astype(np.float32)
vo = vo * 10 ** (gl / 20)
_rt = np.random.default_rng(77).standard_normal(NS); _rt = signal.sosfilt(signal.butter(2, [120, 3500], "band", fs=SR, output="sos"), _rt)
_rt = (_rt / np.sqrt(np.mean(_rt ** 2)) * 10 ** (-60 / 20)).astype(np.float32)
vo = vo + _rt * (np.clip(np.arange(NS) / (0.3 * SR), 0, 1) * np.clip((NS - np.arange(NS)) / (0.8 * SR), 0, 1)).astype(np.float32)
VO = np.stack([vo, vo], 1)
exec(open(f"{_D}/sfx_lib.py").read())

for i, s_ in enumerate(SHOTS[1:], 1):
    k = s_["trans"]; st = s_["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0: coin drop on the hook, machine hum
add(clink(0, -26, 2600) if False else ding(-28, 2349), 0.05); add(whirr(3.0, -36, 120.0), 0.0)
add(chaching(-21), Tw("i3", "thousand", -0.25)); add(thud(-19), Tw("i3", "thousand", -0.2))
for i in range(4): add(pop(-25, 700 + 140 * i), st0("S2b") + 0.12 * i)
add(buzzer(-26, 0.35), Tw("i4", "four", -0.1)); add(thud(-16), Tw("i4", "thousands.", -0.1))
for i in range(6): add(ding(-30, 2637 - 90 * i), Tw("i4", "thousands.", -0.4) + 0.09 * i)
# step cards: coin drop + ding
for sid in ("S4", "S7", "S9", "S12"):
    add(ding(-25, 2093), st0(sid) + 0.05); add(ding(-29, 2637), st0(sid) + 0.12)
# STEP 1
add(whirr(1.6, -34, 90.0), st0("S4") + 0.1)
add(pop(-22, 600), Tw("a2", "nothing.", -0.2))
for w_ in ("morning,", "lunch", "evening."):
    tj = Tw("a2", w_, -0.1); add(pop(-23, 1000), tj)
    for m in range(5): add(click(-30), tj + 0.12 * (m + 1))
add(whoosh(0.4, peak=0.6, f_lo=400, f_hi=4000, level=-25), Tw("a3", "cut", -0.15)); add(chaching(-23), Tw("a3", "cut", 0.2))
add(pop(-22, 800), Tw("a3", "rent", -0.2))
# STEP 2
for i in range(4): add(thud(-24), st0("S7") + 0.15 * i + 0.2)
add(thud(-15), Tw("b2", "check", -0.1)); add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=6000, level=-24), Tw("b2", "insurance.", -0.4))
add(ding(-24, 1568), Tw("b2", "insurance.", -0.05))
# STEP 3
add(beep(-30, 1400, 0.15), Tw("c1", "singers", -0.2)); add(beep(-30, 1400, 0.15), Tw("c1", "singers", 0.15))
add(whoosh(0.3, peak=0.5, f_lo=800, f_hi=5000, level=-26), Tw("c2", "few", -0.2))
for w_ in ("coin", "bill", "cooler"): add(beep(-26, 2600, 0.08), Tw("c3", w_, 0.0))
add(buzzer(-30, 0.2), Tw("c3", "bill", -0.15))
# STEP 4: deal, flashback, stamps, scratch, back to today
for i in range(3): add(pop(-25, 900 + 100 * i), st0("S12") + 0.5 + 0.15 * i)
add(scratch(-26, 0.4), st0("S13") + 0.05)
tf = Tw("e3", "forty", -0.2)
for i in range(0, 40, 2): add(thud(-27), tf + i * 1.4 / 40)
add(boom(-17, 0.4), tf)
add(scratch(-22), Tw("e4", "spots", -0.4))
add(whoosh(0.5, peak=0.7, f_lo=300, f_hi=5000, level=-23), st0("S16") - 0.1); add(ding(-24, 1760), Tw("e5", "week", -0.1))
for i in range(5): add(pop(-27, 1100 + 80 * i), Tw("e5", "buyers,", -0.3) + 0.1 * i)
for i, f0 in enumerate((784, 988, 1175)): add(ding(-27, f0), st0("S17") + 0.25 + 0.18 * i)
add(boom(-16, 0.35), Tw("t1", "singers,", -0.15)); add(scratch(-24), Tw("t1", "paid", -0.2))
add(beep(-28, 425, 0.6), Tw("t2", "Call", -0.1)); add(beep(-28, 425, 0.6), Tw("t2", "Call", 0.9))
# end
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), st0("S20") - 0.2)
add(ding(-24, 2349), Tw("z2", "friend", -0.1)); add(thud(-24), Tw("z2", "friend", 0.25))
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-25, f0), END - 1.4 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 12)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 12)))
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
sf.write(f"{B}/work/stem_vo.wav", vo, SR, subtype="FLOAT"); sf.write(f"{B}/work/stem_bed.wav", bed, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.0:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
print("loudnorm mode:", ln["normalization_type"], "| pre-master I", ln["input_i"], "TP", ln["input_tp"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.0:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
