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
# S0 hook: parcels land, price tag
for t0 in (0.05, 0.2, 0.38): add(thud(-19), t0 + 0.35)
ts = T("i1", "selling") - 0.1; add(pop(-22, 900), ts); add(chaching(-23), ts + 0.05)
# S0b NOPE stamp + mystery cloud
add(thud(-14), S["S0b"] + 0.15); add(boom(-19, 0.3), S["S0b"] + 0.15)
add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=3000, level=-26), T("i2", "never") - 0.4); add(ding(-25, 1760), T("i2", "never") - 0.1)
# S1 cash trail
for j in range(6): add(pop(-29, 700 + 90 * j), S["S1"] + 0.18 * j + 0.05)
# S2a conveyor
for j in range(12): add(click(-31), S["S2a"] + 0.2 + j * 0.25)
add(chaching(-21), T("a1", "hundred") - 0.1)
# S2b bars
add(whoosh(0.5, peak=0.8, f_lo=200, f_hi=2500, level=-26), S["S2b"]); add(thud(-20), T("a2", "eleven") - 0.15); add(buzzer(-27, 0.3), T("a2", "eleven"))
# S2c grid fill
for j in range(7): add(pop(-29, 800 + 80 * j), T("a3", "seven") - 0.15 + j * 0.05)
# S3a racks rise
add(boom(-17, 0.4), S["S3a"] + 0.05)
for i in range(3): add(beep(-30, 2400 + 300 * i, 0.08), S["S3a"] + 0.4 + 0.12 * i)
# S3b network
for i in range(4): add(beep(-31, 1800 + 200 * i, 0.07), T("b2", "other") - 0.05 + 0.1 * i); add(pop(-28, 1000 + 100 * i), T("b2", "other") + 0.15 + 0.1 * i)
add(pop(-25, 700), T("b2", "warehouses") - 0.1)
# S3c numbers
add(thud(-18), T("b3", "forty-two") - 0.15); add(thud(-15), T("b3", "sixteen") - 0.15); add(chaching(-20), T("b3", "sixteen") - 0.1)
# S3d grid fill
for j in range(10): add(pop(-30, 900 + 60 * j), T("b4", "forty") - 0.15 + j * 0.06)
add(ding(-24, 2093), T("b4", "forty") + 0.5)
# S4 twist + pies
add(boom(-16, 0.35), S["S4a"] + 0.05); add(scratch(-26, 0.2), S["S4a"] - 0.1)
add(whoosh(0.5, peak=0.8, f_lo=300, f_hi=3000, level=-27), T("c2", "fifth") - 0.15)
add(boom(-18, 0.3), T("c3", "six") - 0.15); add(ding(-23, 1568), T("c3", "six") + 0.3)
# S5 ads
add(pop(-22, 1000), S["S5a"] + 0.08); add(thud(-17), T("d1", "Ads!") - 0.12)
add(ding(-25, 1318.5), T("d1", "sponsored") - 0.05); add(ding(-25, 1568), T("d1", "sponsored") + 0.1)
for j in range(10): add(thud(-30), S["S5b"] + 0.2 + j * 0.15)
add(chaching(-20), T("d2", "twenty") - 0.15)
# S6 payoff
add(pop(-24, 800), S["S6"] + 0.1); add(whoosh(0.4, level=-25), T("e1", "cloud") - 0.3); add(chaching(-21), T("e1", "bills.") - 0.15)
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
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
