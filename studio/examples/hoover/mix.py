"""Mix: narrator VO + ducked/carved ska score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
LINE_DB = {"i1": +1.0, "c1": -1.5, "b5": -1.0, "i2": +1.0, "d7": +1.0, "t1": +1.0, "a7": +0.5}   # quiet build-ups, louder reveals
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
# new SFX for this video: vacuum motor whirr + jet fly-by (generic synthesis)
def whirr(dur=1.2, level=-28, f0=180.0):
    tt = np.arange(int(dur * SR)) / SR; env = np.clip(tt / 0.25, 0, 1) * np.clip((dur - tt) / 0.3, 0, 1)
    tone = sum(np.sin(2 * np.pi * f0 * h * tt * (1 + 0.04 * np.sin(2 * np.pi * 3 * tt))) / h for h in (1, 2, 3, 5))
    noise = signal.sosfilt(signal.butter(2, [600, 5000], "band", fs=SR, output="sos"), np.random.default_rng(3).standard_normal(len(tt)))
    x = (0.6 * tone / 2 + 0.4 * noise) * env; x = (x / (np.abs(x).max() + 1e-9) * db(level)).astype(np.float32); return np.stack([x, x], 1)


def jet(dur=2.2, level=-24):
    tt = np.arange(int(dur * SR)) / SR; env = np.exp(-((tt - dur * 0.55) / (dur * 0.28)) ** 2)
    nz = np.random.default_rng(9).standard_normal(len(tt))
    lo = signal.sosfilt(signal.butter(2, [200, 2400], "band", fs=SR, output="sos"), nz)
    x = lo * env; x = (x / (np.abs(x).max() + 1e-9) * db(level)).astype(np.float32); p = np.linspace(0, 1, len(x)); return np.stack([x * (1 - 0.6 * p), x * (0.4 + 0.6 * p)], 1)


# S0: winged vacuum flies in, tickets flutter
add(whirr(1.6, -31), 0.0); add(whoosh(0.6, peak=0.6, f_lo=250, f_hi=2500, level=-26), 0.1)
for j in range(6): add(scratch(-34, 0.1), 0.3 + j * 0.11)
add(pop(-24, 1100), T("i1", "free") - 0.1)
# S0b: crowd 'yes'
for j in range(5): add(pop(-27, 600 + 110 * j), SHOTS[1]["start"] + 0.05 * j)
# S1a fired stamps, S1b SOLD
tf = T("i2", "fired,") - 0.1
for j in range(3): add(thud(-17), tf + 0.12 * j)
add(thud(-13), T("i2", "sold.") - 0.1); add(boom(-18, 0.3), T("i2", "sold.") - 0.1)
# S2 three cards, the third shakes
for j in range(3): add(pop(-23, 700 + 200 * j), SHOT["S2"]["start"] + 0.15 + 0.28 * j)
add(buzzer(-26, 0.3), T("i3", "cruelest.") - 0.15)
# S4 shop door bell + poster, S4b tickets
add(doorbell(-26), SHOT["S4"]["start"] + 0.1); add(pop(-22, 900), T("a2", "Spend") - 0.1)
for j in range(7): add(scratch(-33, 0.1), T("a3", "free") - 0.05 + j * 0.11)
# S5 jet across the ocean
add(jet(2.0, -25), T("a4", "bigger.") - 0.1); add(pop(-23, 1000), T("a4", "America.") - 0.3)
# S6 price tag, S7 the scale tips
add(click(-20), T("a5", "nineteen") - 0.2); add(ding(-24, 1318.5), T("a5", "nineteen"))
add(creak(-24, 0.5), T("a6", "several") - 0.2); add(thud(-17), T("a6", "several") + 0.35)
# S8 box opens into a holiday
add(whoosh(0.5, level=-26), T("a7", "holidays.") - 0.4); add(chaching(-22), T("a7", "holidays.") - 0.3)
# S10 footsteps, S11 boxes stacking
for j in range(10): add(click(-31), SHOT["S10"]["start"] + 0.2 + 0.32 * j)
for j in range(15): add(thud(-30), T("b4", "eighty") - 0.2 + j * 0.066)
# S12 tickets raining
for j in range(10): add(scratch(-34, 0.09), SHOT["S12"]["start"] + 0.2 + j * 0.25)
# S13 dark sting, S14 airport PA chime, 'sorry, full'
add(boom(-17, 0.5), SHOT["S13"]["start"])
add(buzzer(-25, 0.3), T("c2", "hard") - 0.2)
for w_ in ("Airports", "Dates", "Expensive"): add(thud(-19), T("c3", w_) - 0.12)
# S16 crowd chant pops, S17 gavel
for j in range(6): add(pop(-29, 400 + 90 * j), T("c4", "furious.") + 0.12 * j)
for j in range(3): add(thud(-15), SHOT["S17"]["start"] + 0.25 + j * 0.385)
# S18 receipt unrolls
add(scratch(-26, 1.0), SHOT["S18"]["start"] + 0.1)
# S19 fired, S20 cheque, S21 jet + counter, S22 cash, S23 flapboard, S23b SOLD, S24 crash
add(thud(-15), T("d2", "fired") - 0.15)
add(chaching(-20), T("d3", "thirty") - 0.15)
add(jet(2.6, -24), SHOT["S21"]["start"] + 0.2)
for j in range(8): add(click(-28), T("d4", "twenty") - 0.6 + j * 0.11)
for j in range(10): add(thud(-31), SHOT["S22"]["start"] + 0.15 + j * 0.2)
add(chaching(-22), T("d5", "forty") - 0.2)
for j in range(14): add(click(-27), SHOT["S23"]["start"] + 0.05 + j * 0.05)
add(thud(-13), T("d6", "sold") - 0.1)
add(whoosh(0.8, peak=0.7, f_lo=200, f_hi=1500, level=-24), SHOT["S24"]["start"] + 0.2); add(boom(-16, 0.5), T("d7", "thirty") - 0.5)
# S25 twist: SOLD OUT, box avalanche
add(pop(-21, 900), T("t1", "sold") - 0.12)
for j in range(14): add(thud(-24 - (j % 3)), T("t1", "Far") - 0.15 + j * 0.07)
# S26 rules + magnifier
add(scratch(-30, 0.2), T("t2", "claim") - 0.2); add(ding(-25, 1568), T("t2", "claim"))
# S27 the vacuum flies again (loop)
add(whirr(1.4, -28), SHOT["S27"]["start"])
# S28 send + sting
add(pop(-21, 900), SHOTS[-1]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-12.0) + sfx, vo)
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.0:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.0:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
