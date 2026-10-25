"""Mix: energetic narrator VO + ducked/carved bluegrass-pop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
# S0 hook: door sign, padlock clank, sandwich reveal
add(pop(-23, 900), 0.15); add(thud(-15), T("i1", "closed") + 0.2); clink(T("i1", "closed") + 0.22, -20)
tb = T("i1", "beating") - 0.12; add(ding(-23, 1568), tb); add(ding(-25, 2093), tb + 0.08)
# S0b week tiles, lock, money up
add(pop(-22, 800), SHOT["S0b"]["start"] + 0.05); add(thud(-15), T("i2", "locked.") - 0.05); clink(T("i2", "locked."), -21)
tm = T("i2", "more") - 0.15; add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3500, level=-25), tm - 0.1); add(chaching(-21), tm + 0.1)
# S1 size
add(pop(-24, 700), SHOT["S1"]["start"] + 0.1); tt = T("a1", "twenty-four") - 0.15; add(thud(-17), tt); add(chaching(-20), tt + 0.05)
for j in range(8): add(pop(-31, 900 + 60 * j), tt + 0.15 + 0.12 * j)
# S1b podium
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=2500, level=-27), SHOT["S1b"]["start"]); add(thud(-18), T("a2", "three") - 0.12)
add(pop(-23, 1000), T("a2", "Only") + 0.13); add(pop(-23, 1200), T("a2", "Only") + 0.48)
# S2a grids
add(boom(-19, 0.3), SHOT["S2a"]["start"] + 0.15)
for i in range(14): add(pop(-30, 700 + 40 * i), T("b1", "fourteen") - 0.15 + 0.05 * i)
for i in range(4): add(pop(-27, 1300 + 80 * i), T("b2", "About") - 0.05 + 0.1 * i)
# S2b drive-thru
add(honk(-27, 0.3), SHOT["S2b"]["start"] + 0.4)
add(thud(-15), T("b3", "does!") - 0.05)
# S3 stacks
for j in range(4): add(thud(-26), T("c1", "four") - 0.1 + 0.15 * j)
for j in range(8): add(thud(-26), T("c2", "seven") - 0.1 + 0.1 * j)
add(chaching(-21), T("c2", "seven") + 0.7); add(thud(-15), T("c2", "six") - 0.1)
# S4 deal
add(creak(-24), SHOT["S4a"]["start"] + 0.1); clink(T("d1", "Want"), -22); add(thud(-17), T("d1", "ten") - 0.15); add(chaching(-21), T("d1", "ten") - 0.1)
add(thud(-14), T("d2", "keeps") - 0.05); add(pop(-24, 900), T("d2", "equipment.") - 0.1)
add(whoosh(0.5, peak=0.8, f_lo=300, f_hi=3000, level=-27), T("d3", "fifteen") - 0.15); add(boom(-19, 0.3), T("d3", "half") - 0.15)
# S5 why Sundays
add(ding(-24, 1318.5), SHOT["S5a"]["start"] + 0.2); add(pop(-23, 700), T("f1", "nineteen") - 0.15)
add(whoosh(0.6, peak=0.7, f_lo=200, f_hi=1800, level=-28), T("f1", "workers") - 0.2)
for j in range(10): add(click(-30), SHOT["S5c"]["start"] + 0.1 * j)
add(thud(-14), T("f2", "changed") - 0.05)
# S6 payoff
add(pop(-23, 800), SHOT["S6"]["start"] + 0.08); add(ding(-23, 1568), T("e1", "busiest") - 0.1)
add(chaching(-19), T("e1", "twenty") - 0.15); add(boom(-19, 0.3), T("e1", "twenty") - 0.15)
# S7 send + sting
add(pop(-21, 900), SHOT["S7"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
