"""Mix: energetic narrator VO + ducked/carved calypso score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
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
TB0 = T("i1", "it's") - 0.15
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
    x *= np.minimum(1, t2 / 0.002) * np.exp(-t2 / 0.05)
    lo = np.sin(2 * np.pi * 180 * t2) * np.exp(-t2 / 0.02)
    x = x / (np.abs(x).max() + 1e-9) + 0.3 * lo; x = x / np.abs(x).max() * db(level)
    return np.stack([x, x * 0.92], 1)


def chomp(level=-17):
    """jaw snap: short low thump + click + wet crunch."""
    n_ = int(0.22 * SR); t2 = np.arange(n_) / SR
    th = np.sin(2 * np.pi * (140 - 60 * t2 / 0.22) * t2) * np.exp(-t2 / 0.04)
    cl = signal.sosfilt(signal.butter(2, [2500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.006)
    x = th + 0.6 * cl / (np.abs(cl).max() + 1e-9); x = x / np.abs(x).max() * db(level)
    cr = np.pad(crunch(level - 4, 0.12), ((int(0.03 * SR), 0), (0, 0))); out = np.stack([x, x], 1)
    out[:len(cr)] += cr[:n_]; return out


def zap(level=-24, dur=0.5):
    """tingly electric crackle."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.06)
    x = signal.sosfilt(signal.butter(2, [3000, 11000], "band", fs=SR, output="sos"), x)
    x = x + 0.3 * np.sign(np.sin(2 * np.pi * 1800 * t2)) * (np.sin(2 * np.pi * 23 * t2) > 0.3)
    x *= np.minimum(1, t2 / 0.01) * np.clip((dur - t2) / 0.1, 0, 1)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, np.roll(x, 90)], 1)


def sizzle(dur, level=-24):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (0.6 + 0.4 * (rng.random(n_) < 0.15))
    x = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.15) * np.clip((dur - t2) / 0.3, 0, 1)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x[::-1]], 1)


def squish(level=-20):
    n_ = int(0.35 * SR); t2 = np.arange(n_) / SR; fr = 300 - 220 * t2 / 0.35
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (1 + 0.6 * np.sin(2 * np.pi * 34 * t2)) * np.exp(-t2 / 0.12)
    x = x + 0.25 * signal.sosfilt(signal.butter(2, [400, 2500], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.08)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def drip(level=-22):
    n_ = int(0.18 * SR); t2 = np.arange(n_) / SR; fr = 600 + 1400 * (t2 / 0.18)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.05) * np.minimum(1, t2 / 0.002)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def wobble(level=-20, dur=0.9):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR; fr = 140 + 60 * np.sin(2 * np.pi * 11 * t2) * np.exp(-t2 / 0.4)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.35) * np.minimum(1, t2 / 0.005)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-23), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-26), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-25), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-21, 700 + 120 * i), st + 0.02); add(thud(-20), st + 0.02)
# S0 munching crunches -> CHOMP back
for j in range(int(TB0 / 0.42)): add(crunch(-27), j * 0.42 + 0.02)
add(boom(-19, 0.35), TB0); add(chomp(-17), TB0 + 0.05)
for j in range(1, 4): add(chomp(-23), TB0 + 0.05 + j * 0.29)
# S1 tingle
add(zap(-22, 0.9), T("i2", "tingly") - 0.1); add(thud(-14), T("i2", "real!") - 0.2); add(ding(-24, 2093), T("i2", "real!"))
# S2 enzymes pop out
add(pop(-22, 900), S["S2"] + 0.08)
for j in range(8): add(pop(-27, 1100 + 110 * j), T("a1", "bromelain.") - 0.2 + 0.06 * j)
card_in(T("a1", "enzymes") - 0.1, -25)
# S2b snips
for j in range(3): clink(S["S2b"] + 0.35 + 0.25 * j, -25, 3400 - 250 * j); add(chomp(-24), S["S2b"] + 0.35 + 0.25 * j)
# S3 slime
bubbles(S["S3"] + 0.3, 6, -27); add(squish(-24), T("a2", "slimy") - 0.05)
# S3b chewing
for j in range(8): add(chomp(-25), T("a2", "chewing") - 0.4 + 0.18 * j)
# S4 acid drips + sizzle + OUCH
for j in range(5): add(drip(-22), T("a3", "acid") - 0.2 + 0.14 * j + 0.55)
add(sizzle(0.9, -27), T("a3", "bare") - 0.1)
add(boom(-15, 0.4), T("a3", "Ouch!") - 0.15); add(zap(-20, 0.8), T("a3", "Ouch!") - 0.1); add(pop(-20, 500), T("a3", "Ouch!"))
for j in range(3): add(crunch(-25), T("a4", "So") + 0.05 + 0.5 * j)
# S5 pineapple chews you
for j in range(5): add(chomp(-17), S["S5"] + 0.05 + 0.31 * j)
# S6 meat
for j in range(4): add(pop(-25, 800 + 90 * j), T("b1", "strong,") - 0.15 + 0.08 * j)
add(thud(-15), T("b1", "tough") - 0.15); add(squish(-18), T("b1", "tender.") - 0.2); add(ding(-24, 1568), T("b1", "tender."))
# S7 heal
for j in range(5): add(ding(-29, 1760 + 200 * j), T("c1", "fixes") + 0.15 * j)
add(ding(-22, 2093), T("c1", "fades") - 0.1)
# S8 how?
add(pop(-22, 1100), S["S8"] + 0.25)
# S8b grill sizzle + KO
add(sizzle(S["S9"] - S["S8b"] + 0.2, -22), S["S8b"])
for j in range(4): add(pop(-23, 500 - 50 * j), T("d1", "off.") - 0.25 + 0.06 * j)
add(thud(-14), T("d1", "off.") - 0.25)
# S9 crunch + check
for j in range(int((S["S10"] - S["S9"]) / 0.42)): add(crunch(-25), S["S9"] + 0.05 + 0.42 * j)
add(pop(-22, 900), T("d2", "grilled") - 0.15); add(pop(-22, 1100), T("d2", "canned") - 0.15); add(ding(-22, 1568), T("d2", "totally") - 0.1)
# S10 jelly wobble -> chunks drop -> melt
add(wobble(-24, 1.2), S["S10"] + 0.1)
for j in range(3): add(drip(-22), T("f1", "fresh") - 0.15 + 0.12 * j + 0.45)
add(squish(-16), T("f1", "ruins") - 0.2); add(boom(-18, 0.35), T("f1", "ruins") - 0.2)
# S10b net snips
for j in range(10): add(ding(-30, 2800 + 90 * j), T("f2", "breaks") - 0.2 + 0.07 * j)
add(chomp(-21), T("f2", "breaks") - 0.2)
# S10c sad drip + stamp
for j in range(3): add(drip(-25), S["S10c"] + 0.2 + 0.77 * j)
add(thud(-14), T("f2", "never") - 0.15); add(buzzer(-24, 0.35), T("f2", "never") - 0.1)
# S11 wobbles
add(pop(-22, 900), S["S11"] + 0.1); add(wobble(-17, 1.1), T("f3", "wobbles") - 0.2)
# S12 send + sting
for j in range(5): add(crunch(-28), S["S12"] + 0.05 + 0.45 * j)
add(pop(-21, 900), S["S12"] + 0.05); add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
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
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.1f}" for lid, L in LINES.items()))
