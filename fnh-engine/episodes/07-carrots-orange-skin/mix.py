"""Mix: energetic narrator VO + ducked/carved food-funk score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
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
TO0 = T("i1", "orange?") - 0.25
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


def crunch(level=-20, dur=0.16):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.35)
    x = signal.sosfilt(signal.butter(2, [1200, 8000], "band", fs=SR, output="sos"), x)
    x *= np.minimum(1, t2 / 0.002) * np.exp(-t2 / 0.05) * (0.6 + 0.4 * (rng.random(n_) < 0.1))
    lo = np.sin(2 * np.pi * 180 * t2) * np.exp(-t2 / 0.02)
    x = x / (np.abs(x).max() + 1e-9) + 0.3 * lo; x = x / np.abs(x).max() * db(level)
    return np.stack([x, x * 0.92], 1)


def ping(level=-20, f0=1500):
    n_ = int(1.6 * SR); t2 = np.arange(n_) / SR
    x = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.25) * np.minimum(1, t2 / 0.003)
    x = x + 0.35 * np.roll(x, int(0.35 * SR)) + 0.15 * np.roll(x, int(0.7 * SR))
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def drone(dur, level=-24):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.sawtooth(2 * np.pi * 92 * t2) * (0.7 + 0.3 * np.sin(2 * np.pi * 22 * t2))
    x = signal.sosfilt(signal.butter(2, 900, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.3) * np.clip((dur - t2) / 0.3, 0, 1)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)


def boing(level=-22):
    n_ = int(0.45 * SR); t2 = np.arange(n_) / SR; fr = 220 + 160 * np.sin(2 * np.pi * 9 * t2) * np.exp(-t2 / 0.2)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.18) * np.minimum(1, t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 munching crunches -> ORANGE
for j in range(int(TO0 / 0.42)): add(crunch(-22), j * 0.42 + 0.02)
add(boom(-16, 0.35), TO0); add(boing(-19), TO0 + 0.05); add(pop(-20, 1200), TO0 + 0.1); add(ding(-24, 1568), TO0 + 0.12)
# S0b mirror + real stamp
add(ding(-25, 2093), S["S0b"] + 0.1); add(thud(-14), T("i2", "real.") - 0.2); add(pop(-22, 1000), T("i2", "real.") + 0.05)
# S1 carrot + pigment dots
add(pop(-22, 900), S["S1"] + 0.08)
for j in range(8): add(pop(-31, 1400 + 90 * j), T("a1", "beta-carotene.") - 0.2 + 0.08 * j)
add(pop(-21, 1200), T("a1", "beta-carotene.") - 0.1)
# S2 machine: dots dropping, capsules, FULL
for j in range(6): add(click(-27), S["S2"] + 0.2 + 0.3 * j)
for j in range(4): add(pop(-25, 700 + 100 * j), T("a2", "vitamin") - 0.15 + 0.31 * j)
add(buzzer(-24, 0.4), T("a2", "limit.") - 0.2); add(thud(-14), T("a2", "limit.") - 0.15)
# S3 blood flow + settle
add(whoosh(1.4, peak=0.5, f_lo=150, f_hi=700, level=-26), S["S3"] + 0.1)
bubbles(S["S3"] + 0.4, 6, -28)
for j in range(10): add(pop(-29, 900 + 60 * j), T("a3", "settles") - 0.1 + 0.12 * j)
# palms / feet / nose
add(pop(-21, 800), T("b1", "palms") - 0.1); add(ding(-24, 1318.5), T("b1", "palms"))
add(pop(-21, 1000), T("b1", "feet...") - 0.1); add(ding(-24, 1568), T("b1", "feet..."))
add(boing(-18), T("b1", "nose!") - 0.12); add(ding(-23, 2093), T("b1", "nose!"))
# S5 count carrots
for j in range(10): add(pop(-25, 900 + 70 * j), T("c1", "ten") - 0.15 + 0.05 * j)
add(thud(-15), T("c1", "ten") - 0.15); card_in(T("c1", "weeks.") - 0.2, -24)
# S6 baby spoon
for j in range(3): add(whoosh(0.3, peak=0.6, f_lo=800, f_hi=3000, level=-29), S["S6"] + 0.9 * j + 0.1); add(pop(-25, 600), S["S6"] + 0.9 * j + 0.5)
# S7 harmless check + fade shimmer
add(ding(-22, 1568), T("d1", "harmless.") - 0.15); add(ding(-24, 2093), T("d1", "harmless.") - 0.05)
add(scratch(-25, 0.25), T("d1", "Eat"))
# S8 eyes
add(ding(-24, 1760), T("d2", "whites") - 0.05); add(boom(-18, 0.3), S["S8b"] + 0.02); add(buzzer(-26, 0.35), S["S8b"] + 0.05)
add(thud(-14), T("d2", "see") - 0.15)
# S9 night: crickets-ish ticks, NOPE buzzer
for j in range(8): add(click(-33), S["S9"] + 0.2 + 0.25 * j)
add(buzzer(-19, 0.5), T("f1", "Nope!") - 0.15); add(thud(-14), T("f1", "Nope!") - 0.15)
# S10 plane drone + crunches, S10b radar pings
add(drone(S["S10b"] - S["S10"] + 0.3, -24), S["S10"] - 0.1)
for j in range(int((S["S10b"] - S["S10"]) / 0.36)): add(crunch(-26), S["S10"] + 0.05 + 0.36 * j)
add(ping(-21, 1500), S["S10b"] + 0.15); add(ping(-19, 1700), T("f2", "Radar!") - 0.2); add(thud(-15), T("f2", "Radar!") - 0.1)
# S11 send + sting
for j in range(5): add(crunch(-28), S["S11"] + 0.05 + 0.4 * j)
add(pop(-21, 900), S["S11"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1046.5, 1318.5, 1568, 2093)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-2.0)
bed = bed_carve.carve(M * db(-10.5) + sfx, vo)
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
