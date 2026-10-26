"""Mix: energetic narrator VO + ducked/carved synth-pop score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
# S0 hook: gym pops in, price tag, cash
add(pop(-23, 900), 0.1); add(thud(-17), 0.3)
tf = T("i1", "fifteen") - 0.12; add(pop(-21, 1200), tf); add(ding(-25, 1568), tf + 0.05)
tm = T("i1", "million") - 0.2; add(thud(-14), tm); add(chaching(-19), tm + 0.05)
# S0b genius / you
add(pop(-23, 1000), T("i2", "genius.") - 0.2); add(ding(-24, 2093), T("i2", "genius."))
add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3500, level=-25), T("i2", "you!") - 0.4); add(boom(-18, 0.3), T("i2", "you!") - 0.15)
# S1 cancel phone
add(click(-22), T("a1", "pointless.") - 0.25); add(thud(-15), T("a1", "pointless.") - 0.15); add(buzzer(-27), T("a1", "pointless.") - 0.1)
# S1b card + tags
add(pop(-22, 900), T("a2", "Fifteen") - 0.05); card_in(SHOT["S1b"]["start"] + 0.05, -24); add(pop(-21, 1300), T("a2", "yearly") - 0.2); add(chaching(-22), T("a2", "yearly") - 0.1)
# S2 crowd fills
for j in range(12): add(pop(-31, 600 + 50 * j), SHOT["S2"]["start"] + 0.15 + 0.12 * j)
add(thud(-14), T("b1", "twenty-one") - 0.15); add(ding(-24, 1568), T("b1", "twenty-one"))
# S2b clubs + per gym
for j in range(9): add(pop(-29, 700 + 60 * j), SHOT["S2b"]["start"] + 0.05 + 0.05 * j)
add(thud(-14), T("b2", "seven") - 0.15); add(pop(-21, 1100), T("b2", "seven") - 0.05)
# S2c chaos
for j in range(6): add(pop(-29, 500 + 80 * j), SHOT["S2c"]["start"] + 0.2 + 0.2 * j)
add(boom(-16, 0.4), T("b3", "chaos!") - 0.15); add(thud(-13), T("b3", "chaos!") - 0.12); add(honk(-24), T("b3", "chaos!"))
# S3a treadmill dust, report
add(creak(-26), SHOT["S3a"]["start"] + 0.6); add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3000, level=-26), T("c1", "report.") - 0.4); add(thud(-18), T("c1", "report.") - 0.2)
# S3b quote lines + highlighter
for w_ in ("A", "member", "not"): add(click(-27), T("c2", w_) - 0.1)
swish(T("c2", "regularly") - 0.1, -22); add(thud(-15), T("c2", "regularly"))
# S4a study
add(pop(-23, 900), SHOT["S4a"]["start"] + 0.08); add(pop(-21, 1200), T("d1", "seventy") - 0.2)
# S4b calendar ticks then price
for j in range(5): add(ding(-29, 1318.5 + 120 * j), SHOT["S4b"]["start"] + 0.25 + 0.22 * j)
add(thud(-14), T("d2", "seventeen") - 0.15); add(buzzer(-27), T("d2", "seventeen") - 0.1)
# S4c bars + ticket
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=2500, level=-27), SHOT["S4c"]["start"] + 0.05); add(pop(-21, 1300), T("d3", "there.") - 0.25)
# S4d 80%
for j in range(10): add(pop(-31, 800 + 40 * j), SHOT["S4d"]["start"] + 0.04 * j)
add(thud(-15), T("d4", "saved") - 0.15)
for j in range(8): add(click(-30), T("d4", "saved") - 0.2 + 0.06 * j)
# S5 money
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=2500, level=-27), SHOT["S5"]["start"] + 0.05); add(thud(-17), T("f1", "billion") - 0.2)
add(thud(-14), T("f1", "twenty") - 0.15); add(chaching(-19), T("f1", "twenty") - 0.05)
# S6 payoff
add(thud(-15), T("e1", "workouts.") - 0.15); add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3500, level=-24), T("e1", "plan") - 0.35)
add(boom(-18, 0.3), T("e1", "plan") - 0.2); add(ding(-23, 1568), T("e1", "plan") - 0.1); add(ding(-25, 2093), T("e1", "plan"))
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
