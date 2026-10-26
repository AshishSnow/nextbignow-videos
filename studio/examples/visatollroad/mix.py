"""Mix: energetic narrator VO + ducked/carved salsa score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
exec(open(f"{_D}/sfx_lib.py").read())

for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 hook: card + $0 stamp + coins
add(pop(-23, 900), 0.05); add(whoosh(0.35, level=-26), 0.0)
tn = T("i1", "never") - 0.15; add(thud(-14), tn + 0.25); add(boom(-20, 0.25), tn + 0.25)
th = T("i1", "half") - 0.2; add(chaching(-19), th); add(ding(-24, 1568), th + 0.05)
for j in range(6): clink(th + 0.15 + 0.1 * j, -28, 3000 + 150 * j)
# S0b stamps + ???
add(thud(-14), T("i2", "loans.") - 0.25); add(thud(-14), T("i2", "interest.") - 0.25)
add(pop(-21, 1100), T("i2", "trick?") - 0.3); add(scratch(-26), T("i2", "trick?") - 0.35)
# S1 bank -> card
add(pop(-22, 800), SHOT["S1"]["start"] + 0.05); add(buzzer(-30), T("a1", "doesn't") - 0.15)
add(whoosh(0.4, peak=0.7, f_lo=400, f_hi=4000, level=-23), T("a1", "bank") - 0.3); card_in(T("a1", "bank") - 0.05); add(ding(-24, 2093), T("a1", "bank") + 0.1)
# S1b loan + risk weight
clink(T("a2", "lends") - 0.1, -24); add(chaching(-23), T("a2", "lends") + 0.3)
add(whoosh(0.3, level=-26), T("a2", "risk") - 0.35); add(thud(-12), T("a2", "risk") - 0.05); add(boom(-19, 0.3), T("a2", "risk") - 0.05)
# S1c road
add(honk(-27, 0.3), SHOT["S1c"]["start"] + 0.5); add(pop(-21, 1200), T("a3", "road") - 0.2)
# S2 toll booth: car approaches, barrier lifts
add(pop(-22, 900), SHOT["S2"]["start"] + 0.05); add(whoosh(0.9, peak=0.6, f_lo=150, f_hi=1200, level=-26), SHOT["S2"]["start"] + 0.2)
add(creak(-22), T("b1", "toll") - 0.2); add(click(-24), T("b1", "toll") + 0.2)
# S2b grids pop in
for j in range(12): add(pop(-31, 800 + 40 * j), SHOT["S2b"]["start"] + 0.1 + 0.05 * j)
add(thud(-16), T("b2", "banks.") - 0.3)
for j in range(12): add(pop(-31, 1100 + 40 * j), T("b2", "other,") - 0.2 + 0.05 * j)
add(boom(-18, 0.3), T("b2", "million") - 0.3); add(ding(-24, 1568), T("b2", "million") - 0.2)
# S3 cars + toll coins
for i in range(4):
    tq = SHOT["S3"]["start"] + i * 0.9 + 0.75
    if tq < SHOT["S4"]["start"] - 0.2: clink(tq + 0.45, -24, 3200); add(click(-28), tq)
add(pop(-20, 1300), T("b3", "tiny") - 0.25)
# S4 odometer roll
for j in range(int(1.4 / 0.07)): add(click(-31), T("c1", "billion") - 1.9 + j * 0.07)
add(thud(-13), T("c1", "billion") - 0.5); add(chaching(-20), T("c1", "billion") - 0.4)
# S4b terminals beeping
for j in range(int((SHOT["S5"]["start"] - SHOT["S4b"]["start"]) / 0.375)): add(beep(-29, 2900), SHOT["S4b"]["start"] + 0.05 + j * 0.375)
add(thud(-15), T("c2", "eight") - 0.2)
# S5 cash stacks + coins -> $40B
for j in range(9): add(pop(-29, 600 + 60 * j), SHOT["S5"]["start"] + 0.2 + 0.24 * j)
for j in range(6): clink(SHOT["S5"]["start"] + 0.1 + 0.15 * j, -29, 2800 + 200 * j)
add(boom(-16, 0.4), T("c3", "forty") - 0.2); add(chaching(-18), T("c3", "forty") - 0.1)
# S6 pie -> profit
swish(T("d1", "profit.") - 0.45, -22); add(boom(-15, 0.45), T("d1", "profit.") - 0.4); add(ding(-22, 2093), T("d1", "profit.") - 0.1)
add(pop(-20, 1200), T("d2", "Half") - 0.2); add(chaching(-21), T("d2", "Half") - 0.1); add(thud(-15), T("d2", "cheap…") - 0.2)
# S7 tap -> paid -> toll coin
add(beep(-21, 2600), T("e1", "tap") + 0.1); add(beep(-23, 3200), T("e1", "tap") + 0.22)
add(boom(-18, 0.3), T("e1", "toll!") - 0.3); clink(T("e1", "toll!") + 0.15, -22, 3300); add(ding(-23, 1568), T("e1", "toll!") - 0.2)
# S8 send + sting
add(pop(-21, 900), SHOT["S8"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-12.0) + sfx, vo)
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
