"""Mix: narrator VO + ducked/carved tropical-house score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1.5 dBTP)."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
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
LINE_DB = {"i1": +1.0, "t1": +1.0, "d5": +0.5, "c2": -1.0}   # reveals up, the "heads up" aside a touch quieter
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
# S0: drone buzz under the hook, shutter + cash on the $300
add(rotor(3.0, -35), 0.0); add(rotor(2.2, -33, 230.0), S["S1"])
add(shutter(-20), S["S1b"] + 0.02); tc = Tw("i2", "three", -0.15); add(chaching(-21), tc); add(ding(-25, 1568), tc + 0.08)
# S2 waypoints pop, lose $$$ thud
for i in range(5): add(pop(-25, 700 + 120 * i), Tw("i3", "five", -0.1) + 0.25 * i)
add(thud(-16), Tw("i3", "lose", -0.1)); add(buzzer(-27, 0.3), Tw("i3", "lose", -0.05))
# STEP 1: door, stamp, pencil, price, ping
add(creak(-28, 0.5), S["S3"] + 0.1)
add(thud(-17), Tw("a2", "Part", -0.12))
for j in range(10): add(scratch(-34, 0.08), Tw("a3", "sixty", 0.0) + 0.22 * j)
add(chaching(-21), Tw("a4", "seventy", -0.25)); add(thud(-20), Tw("a4", "seventy", 0.0))
add(thud(-18), Tw("a5", "free", -0.12)); add(ding(-23, 1760), Tw("a5", "current.", -0.1))
add(pop(-23, 800), Tw("a6", "UK", -0.12)); add(pop(-23, 1000), Tw("a6", "Europe,", -0.12))
# STEP 2: lift, $5 slap, calendar, Remote ID beeps
add(rotor(1.6, -32), S["S9"] + 0.3)
add(thud(-16), Tw("b2", "five", -0.15)); add(pop(-23, 900), Tw("b2", "three", -0.15))
for j in range(3): add(beep(-27, 2600, 0.08), Tw("b3", "Remote", -0.15) + 0.3 * j)
add(rotor(2.4, -34, 240.0), S["S11"])
# STEP 3: shelf, sign drops, check, shield
add(buzzer(-25, 0.4), Tw("c2", "new", 0.25)); add(thud(-18), Tw("c2", "new", 0.3))
add(rotor(2.0, -32), S["S13b"]); add(ding(-23, 1568), Tw("c2", "still", -0.15))
add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=6000, level=-25), Tw("c3", "insurance.", -0.4)); add(ding(-24, 1318.5), Tw("c3", "twelve", -0.2))
# STEP 4: clients pop, prices, shutters, portfolio
for w_ in ("agents,", "roofers", "planners"): add(pop(-23, 900), Tw("d2", w_, -0.12))
add(pop(-22, 800), Tw("d3", "home", -0.12)); add(pop(-22, 1000), Tw("d3", "roof", -0.12))
for i in range(3): add(shutter(-21), S["S18"] + 0.5 + 0.55 * i)
add(ding(-23, 2093), Tw("d4", "portfolio.", 0.15))
# STEP 5: drift into the no-fly zone, alarm, fine stamp, phone check
add(rotor(3.5, -31, 200.0), S["S19"] + 0.2)
for j in range(4): add(beep(-24, 1800, 0.12), Tw("d5", "flying", -0.2) + 0.32 * j)
add(boom(-15, 0.4), Tw("t1", "seventy", -0.2)); add(thud(-14), Tw("t1", "seventy", -0.15))
add(click(-20), Tw("t2", "check", -0.1)); add(ding(-22, 1760), Tw("t2", "every", -0.2))
# end: high five, choice whoosh, rotor fades out
add(pop(-20, 1300), S["S22"] + 0.6); add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), S["S23"] - 0.2)
add(rotor(2.0, -33, 250.0), S["S23"] + 3.0)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-25, f0), END - 1.4 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
# word guard: no SFX hit / loud note within 12 dB of a word on a phone speaker (GUARD=0 disables; studio/tools/mix_check.py measures it)
if float(os.environ.get("GUARD", 12)) > 0: bed = bed_carve.guard(bed, vo, ld=float(os.environ.get("GUARD", 12)))
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
sf.write(f"{B}/work/stem_vo.wav", vo, SR, subtype="FLOAT"); sf.write(f"{B}/work/stem_bed.wav", bed, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
print("loudnorm mode:", ln["normalization_type"], "| pre-master I", ln["input_i"], "TP", ln["input_tp"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
