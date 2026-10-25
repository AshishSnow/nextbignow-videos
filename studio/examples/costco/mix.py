"""Mix: energetic narrator VO + ducked/carved funk score + per-moment SFX -> work/mix.wav (loud: -11 LUFS, -1 dBTP)."""
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
# S0 hook: sizzle, tag slam
add(pop(-24, 600), 0.05)
td = T("i1", "dollar") - 0.12
add(thud(-15), td); add(chaching(-21), td + 0.05); add(ding(-25, 1568), td + 0.08)
# S0b calendar flips
for j in range(14): add(click(-28), S["S0b"] + 0.05 + j * 0.11)
add(thud(-18), T("i2", "forty") - 0.1)
# S1 cash falls
for j in range(7): add(thud(-27), S["S1"] + 0.35 + j * 0.12)
add(pop(-23, 1200), S["S1"] + 0.3)
# S1b folders + genius
for i in range(4): card_in(T("i4", "four") - 0.05 + i * 0.12 + 0.2, -27)
add(ding(-22, 2093), T("i4", "genius.") - 0.1)
# S2a coins fall out
tl = T("a1", "loses") - 0.1
for j in range(5): clink(tl + 0.15 + j * 0.09, -28, 2200 + 200 * (j % 3))
add(pop(-23, 900), T("a1", "purpose.") - 0.05)
# S2b founder
add(pop(-24, 1100), T("a2", "raise") - 0.1); add(pop(-24, 800), T("a2", "if") - 0.1)
tk = T("a2", "kill") - 0.15; add(boom(-16, 0.4), tk); add(scratch(-26, 0.2), tk - 0.12)
# S2c checks
for i in range(6): add(ding(-29, 1318.5 + 120 * i), T("a3", "trust") - 0.1 + i * 0.12)
# S3a/S3b chicken
add(thud(-18), T("b1", "four") - 0.1); add(chaching(-24), T("b1", "four") - 0.05)
th = T("b2", "hundred") - 0.15
for j in range(20): add(pop(-31, 500 + 40 * j), th - 0.5 + 0.04 * (j * 7 % 20))
# S3c footsteps
tw = T("b3", "walk") - 0.3
for j in range(10): add(click(-30), tw + j * 0.2)
add(ding(-24, 1760), T("b3", "back") - 0.1)
# S4a cap slam
add(thud(-14), T("c1", "caps") + 0.1); add(clink(T("c1", "caps") + 0.1, -24, 3000), 0) if False else clink(T("c1", "caps") + 0.1, -24, 3000)
add(pop(-23, 700), T("c2", "fourteen") - 0.12); add(pop(-23, 900), T("c2", "fifteen") - 0.12); add(ding(-22, 2093), T("c2", "deal.") - 0.2)
# S5 genius / card / money / renew
add(whoosh(0.6, peak=0.6, f_lo=500, f_hi=6000, level=-25), T("d2", "card.") - 0.6)
add(boom(-17, 0.3), T("d2", "card.") - 0.25)
for j in range(10): add(thud(-29), S["S5c"] + 0.3 + j * 0.1)
add(chaching(-21), T("d3", "six") - 0.15); add(pop(-22, 800), T("d3", "half") - 0.2)
for j in range(10): add(pop(-30, 900 + 60 * j), T("d4", "nine") - 0.15 + 0.06 * j)
# S6 ad
add(boom(-18, 0.3), T("e1", "ad…") - 0.15); add(pop(-21, 1300), T("e1", "ad…") - 0.1); add(whoosh(0.35, level=-25), T("e1", "card.") - 0.25)
# S7 send + sting
add(pop(-21, 900), S["S7"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
