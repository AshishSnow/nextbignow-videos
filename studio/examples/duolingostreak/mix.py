"""Mix: energetic narrator VO + ducked/carved chiptune score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
# S0 hook: phone + FREE stamp + coins
add(pop(-23, 900), 0.05); add(whoosh(0.35, level=-26), 0.0)
tf = T("i1", "free…") - 0.2; add(thud(-14), tf); add(boom(-21, 0.25), tf)
tb = T("i1", "billion") - 0.25; add(chaching(-18), tb); add(boom(-17, 0.4), tb)
for j in range(6): clink(tb + 0.15 + 0.1 * j, -28, 3000 + 150 * j)
# S0b ???
add(pop(-21, 1100), SHOT["S0b"]["start"] + 0.3); add(scratch(-27), SHOT["S0b"]["start"] + 0.25)
# S1 flame grows
add(whoosh(0.6, peak=0.8, f_lo=200, f_hi=2500, level=-24), T("i2", "streak.") - 0.6); add(boom(-17, 0.4), T("i2", "streak.") - 0.25)
# S2 course cards pop, $0 tags
for j in range(6): add(pop(-29, 700 + 90 * j), SHOT["S2"]["start"] + 0.08 * j)
for j in range(6): add(click(-27), T("a1", "free.") - 0.25 + 0.06 * j)
# S2b ad pops
add(pop(-19, 600), T("a1", "ad") - 0.25); add(buzzer(-30, 0.3), T("a1", "ad") - 0.2)
# S3 cents grid
for j in range(8): add(click(-26), T("a2", "eight") - 0.25 + 0.07 * j)
add(thud(-16), T("a2", "eight") - 0.25)
# S4 people grid
for j in range(10): add(pop(-32, 900 + 40 * j), SHOT["S4"]["start"] + 0.12 * j)
add(chaching(-21), T("a3", "nine") - 0.2)
# S5 odometer
for j in range(int(1.2 / 0.07)): add(click(-31), T("a4", "twelve") - 1.5 + j * 0.07)
add(thud(-13), T("a4", "twelve") - 0.3); add(chaching(-20), T("a4", "twelve") - 0.2)
# S6 notifications buzz
for j in range(3): add(beep(-24, 1800, 0.08), SHOT["S6"]["start"] + 0.35 + 0.55 * j); add(beep(-26, 1800, 0.08), SHOT["S6"]["start"] + 0.47 + 0.55 * j)
# S7 days tick, miss X, flame out
for j in range(6): add(pop(-29, 1000 + 80 * j), SHOT["S7"]["start"] + 0.32 * j + 0.02)
add(buzzer(-22, 0.4), T("b2", "Miss") - 0.12); add(crt_off(-20, 0.5), T("b2", "zero.") - 0.3)
# S8 split
add(pop(-22, 800), SHOT["S8"]["start"] + 0.4); add(boom(-18, 0.3), T("b3", "hundred,") - 0.3)
# S9 envelope
add(whoosh(0.5, peak=0.7, f_lo=500, f_hi=5000, level=-25), T("c0", "Wait") - 0.1); scratch_card(T("c0", "Wait") + 0.1, 0.5, -26)
# S10 heads + odometer
for j in range(18): add(pop(-33, 900 + 30 * j), SHOT["S10"]["start"] + 0.05 * j)
for j in range(int(1.0 / 0.07)): add(click(-31), T("c1", "forty") - 0.9 + j * 0.07)
add(boom(-16, 0.4), T("c1", "forty") - 0.3); add(ding(-24, 1568), T("c1", "forty") - 0.2)
# S11 heatmap fill
for j in range(16): add(click(-33), SHOT["S11"]["start"] + 0.12 * j)
add(boom(-16, 0.4), T("c2", "year!") - 0.3); add(ding(-23, 2093), T("c2", "year!") - 0.2)
# S12 heart monitor
for j in range(3): add(beep(-27, 1000, 0.09), SHOT["S12"]["start"] + 0.3 + 0.7 * j)
add(boom(-17, 0.35), T("c3", "revived") - 0.2)
for j in range(3): add(beep(-23, 1000, 0.1), T("c3", "revived") + 0.1 + 0.45 * j)
# S13 twist
add(boom(-16, 0.45), SHOT["S13"]["start"] + 0.02); add(pop(-20, 700), T("d1", "ad…") - 0.25); add(ding(-22, 1760), T("d1", "pay.") - 0.3)
# S14 $0 + loop
add(thud(-15), SHOT["S14"]["start"] + 0.5)
add(whoosh(1.4, peak=0.5, f_lo=200, f_hi=2000, level=-27), T("d2", "habit") - 0.25)
for j in range(4): add(pop(-25, 900 + 200 * j), T("d2", "habit") - 0.25 + 0.4 * j)
# S15 sneak + bars
swish(SHOT["S15"]["start"] + 0.2, -24)
add(whoosh(0.7, peak=0.6, f_lo=200, f_hi=2000, level=-24), T("d3", "three") - 0.4); add(boom(-15, 0.45), T("d3", "three") - 0.3); add(chaching(-21), T("d3", "three") + 0.2)
# S16 days fill
for j in range(7): add(ding(-29, 1046.5 * 2 ** (j / 12 * 2)), T("e1", "Start") - 0.2 + j * max(0.2, (T("e1", "seven") - T("e1", "Start")) / 6))
add(boom(-17, 0.35), T("e1", "seven") - 0.3)
# S17 send + sting
add(pop(-21, 900), SHOT["S17"]["start"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
