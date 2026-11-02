"""Mix: narrator VO + ducked/carved doo-wop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
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
LINE_DB = {"i1": +2.0, "e5": +1.0, "t1": +0.5, "e4": -1.5, "t2": +0.5}   # hook + $25K reveal up, the under-the-table line quieter
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
# S0: horn on frame 0, street hum
add(honk(-24, 0.3), 0.04); add(honk(-26, 0.42), 0.40); add(whirr(3.0, -40, 110.0), 0.0)
add(chaching(-21), Tw("i1", "thousands", -0.25)); add(thud(-19), Tw("i1", "thousands", -0.2))
add(sizzle(2.0, -33), Tw("i2", "tacos", -0.3))
add(pop(-22, 700), Tw("i2", "tacos", -0.1)); add(buzzer(-27, 0.3), Tw("i3", "legally", -0.2))
for i in range(4): add(ding(-27, 1760 + 220 * i), st0("S2b") + 0.12 * i); add(pop(-25, 700 + 140 * i), st0("S2b") + 0.12 * i)
# STEP cards: truck horn
for sid in ("S3", "S6", "S9", "S12"): add(honk(-22, 0.26), st0(sid) + 0.02); add(honk(-24, 0.34), st0(sid) + 0.30)
add(thud(-22), Tw("a1", "truck", -0.2))
add(pop(-24, 900), Tw("a2", "needs", -0.1)); add(ding(-25, 1568), Tw("a2", "course", -0.1)); add(click(-26), st0("S4b") + 0.2)
add(whoosh(0.4, peak=0.6, f_lo=400, f_hi=4000, level=-27), Tw("a3", "no", -0.2)); add(ding(-25, 2093), Tw("a3", "no", -0.1))
add(rattle(1.0, -27), st0("S6") + 0.1)
add(pop(-24, 800), Tw("b2", "stored", -0.15)); add(hose(0.9, -30), Tw("b2", "cleaned", -0.15)); add(clink(Tw("b2", "serviced", -0.05), -24, 2800) if False else ding(-27, 2800), Tw("b2", "serviced", -0.05))
add(thud(-23), Tw("b3", "every", -0.2)); [add(click(-30), st0("S8") + 0.25 * i) for i in range(10)]
add(chaching(-22), Tw("c2", "thousands", -0.3))
add(scratch(-24), Tw("c3", "four", -0.1))
add(pop(-24, 700), Tw("e2", "own", -0.15)); add(click(-20), Tw("e2", "capped", -0.1)); add(thud(-16), Tw("e2", "capped", -0.05)); add(boom(-21, 0.3), Tw("e2", "capped", -0.05))
for i in range(5): add(click(-31), Tw("e3", "still", 0.0) + 0.55 * i)
add(whoosh(0.8, peak=0.5, f_lo=200, f_hi=1500, level=-27), Tw("e4", "rent", -0.3))
add(chaching(-20), Tw("e5", "twenty-five", -0.25)); add(boom(-18, 0.35), Tw("e5", "twenty-five", -0.25))
add(scratch(-25, 0.35), st0("S17") + 0.02); add(thud(-20), Tw("e6", "undercover", -0.2)); add(thud(-15), Tw("e6", "six", -0.2))
add(whirr(2.8, -33, 220.0), Tw("e7", "offers", -0.2)); [add(click(-29), Tw("e7", "offers", -0.2) + 0.2 * i) for i in range(12)]
add(ding(-24, 1760), Tw("e7", "twenty-two", -0.2))
for i in range(7): add(pop(-29, 1200 + 60 * i), st0("S19") + 0.1 + i * 0.14)
add(buzzer(-30, 0.2), Tw("t1", "only", -0.05))
add(sizzle(1.6, -33), Tw("t1", "working", -0.2)); add(ding(-25, 1760), Tw("t1", "first", -0.1))
add(pop(-23, 900), Tw("t2", "private", -0.2)); add(thud(-22), Tw("t2", "no", -0.25)); add(ding(-24, 2349), Tw("t2", "no", -0.2)); add(sizzle(2.0, -34), st0("S20") + 0.4)
# end
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), st0("S22") - 0.2)
add(honk(-26, 0.25), Tw("z2", "friend", -0.1)); add(honk(-27, 0.3), Tw("z2", "friend", 0.2))
for j, f0 in enumerate((1318.5, 1568, 1975.5, 2637)): add(ding(-25, f0), END - 1.4 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 12)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 12)))
mix = VO + bed
# pre-limiter (3 Nov): take the peaks off so loudnorm can stay linear and really reach -11 LUFS (was -11.7..-11.9 on the dynamic path). LIM=0 disables.
if float(os.environ.get("LIM", -8)) < 0:
    from pedalboard import Limiter
    _p = float(np.abs(mix).max()) + 1e-9; _r = 10 ** (-1.0 / 20) / _p   # peak-normalise to -1 dBFS first, so the threshold means the same each video
    mix = Limiter(threshold_db=float(os.environ.get("LIM", -8)), release_ms=120.0)((mix * _r).astype(np.float32).T, SR).T / _r
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
