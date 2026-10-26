"""Mix: energetic narrator VO + ducked/carved mariachi score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
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
TF0 = T("i1", "food...") - 0.1
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


def fire_roar(dur=1.2, level=-19):
    """flame burst: low rumbling noise swell + crackles."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.sosfilt(signal.butter(2, [80, 900], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t2) ** 2)
    cr = signal.sosfilt(signal.butter(2, [2000, 8000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.01))
    x = x / (np.abs(x).max() + 1e-9) + 0.5 * cr / (np.abs(cr).max() + 1e-9)
    x *= np.minimum(1, t2 / 0.04) * np.clip((dur - t2) / 0.4, 0, 1)
    x = x / np.abs(x).max() * db(level); return np.stack([x, np.roll(x, 120)], 1)


def lock_click(level=-15):
    out = np.zeros((int(0.12 * SR), 2), np.float32)
    for k, (d0, f0) in enumerate(((0.0, 3200), (0.045, 2400))):
        n_ = int(0.05 * SR); t2 = np.arange(n_) / SR
        x = (np.sin(2 * np.pi * f0 * t2) + 0.6 * signal.sosfilt(signal.butter(2, [1500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))) * np.exp(-t2 / 0.006)
        i = int(d0 * SR); out[i:i + n_] += np.stack([x, x], 1)
    return out / np.abs(out).max() * db(level)


def siren(dur=1.2, level=-24):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = np.where((t2 * 4) % 1 < 0.5, 950, 720)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.5 + np.sin(2 * np.pi * np.cumsum(fr) / SR)
    x = signal.sosfilt(signal.butter(2, 3000, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.03) * np.clip((dur - t2) / 0.2, 0, 1)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def slurp(level=-24, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.sosfilt(signal.butter(2, [300, 2500], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    x *= (0.5 + 0.5 * np.sin(2 * np.pi * (12 + 10 * t2) * t2)) * np.minimum(1, t2 / 0.05) * np.clip((dur - t2) / 0.1, 0, 1)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def gulp(level=-18):
    n_ = int(0.2 * SR); t2 = np.arange(n_) / SR; fr = 420 * np.exp(-t2 / 0.08) + 90
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.07) * np.minimum(1, t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def chirp(level=-22, n_notes=3):
    out = []
    for j in range(n_notes):
        n_ = int(0.07 * SR); t2 = np.arange(n_) / SR; fr = 2600 + 1800 * t2 / 0.07
        x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t2 / 0.07); out += [x, np.zeros(int(0.04 * SR))]
    x = np.concatenate(out); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def squeak(level=-22):
    n_ = int(0.16 * SR); t2 = np.arange(n_) / SR; fr = 2200 + 1400 * np.sin(np.pi * t2 / 0.16)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t2 / 0.16) * (1 + 0.3 * np.sin(2 * np.pi * 40 * t2))
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def tick(level=-28, f0=2400):
    return pop(level, f0)


# hook: munch crunches -> FIRE
for j in range(int(TF0 / 0.32)): add(crunch(-29), j * 0.32 + 0.02)
add(boom(-19, 0.35), TF0); add(fire_roar(1.5, -24), TF0 + 0.02)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
add(fire_roar(1.5, -25), S["S1"])
add(fire_roar(0.6, -26), S["S1b"]); add(thud(-15), T("i2", "nothing") + 0.05); add(buzzer(-26, 0.3), T("i2", "nothing") + 0.08)
add(pop(-19, 1200), T("i2", "trick!") - 0.15); add(ding(-24, 1760), T("i2", "trick!") - 0.1)
# science
add(whoosh(0.35, level=-27), T("a1", "chemical") - 0.2); add(pop(-23, 1300), T("a1", "chemical") + 0.2)
add(pop(-20, 900), S["S2b"] + 0.05); add(ding(-25, 2093), T("a1", "capsaicin.") - 0.05)
add(pop(-24, 800), S["S3"] + 0.05); add(whoosh(0.35, level=-27), T("a2", "nerve") - 0.4); add(pop(-23, 1500), T("a2", "nerve"))
for j in range(3): add(tick(-27, 1800 + 300 * j), T("a2", "wires") - 0.15 + 0.08 * j)
for j in range(3): add(pop(-23, 1000 + 200 * j), T("a3", "heat") - 0.2 + 0.12 * j)
card_in(T("a3", "alarms.") + 0.1, -26)
add(siren(0.9, -31), T("a4", "painful") - 0.1); add(thud(-15), T("a4", "painful") - 0.1)
add(slurp(-23, 0.45), S["S5b"] + 0.02); add(siren(0.8, -27), T("a4", "scalding") + 0.25); add(pop(-20, 600), T("a4", "scalding") + 0.3)
add(whoosh(0.6, peak=0.6, level=-26), S["S6"] + 0.1); add(lock_click(-19), T("a5", "perfectly.") - 0.25); add(ding(-24, 1568), T("a5", "perfectly.") - 0.1)
add(lock_click(-21), S["S6b"] + 0.75); add(lock_click(-21), S["S6b"] + 1.05)
# CLICK -> alarm -> FIRE
add(lock_click(-15), S["S7"] + 0.1); add(siren(S["S7b"] - S["S7"] + 1.0, -32), S["S7"] + 0.15)
for j in range(3): add(tick(-25, 2600), S["S7b"] + 0.05 + 0.3 * j)
add(boom(-14, 0.45), T("a6", "FIRE!") - 0.15); add(fire_roar(1.6, -24), T("a6", "FIRE!") - 0.1)
add(fire_roar(1.3, -25), S["S8"])
add(whoosh(0.4, level=-27), S["S8b"] + 0.3); add(ding(-24, 2093), T("a7", "no") - 0.1)
# Nobel
bubbles(S["S9"] + 0.2, 4, -28); add(boom(-17, 0.4), T("b1", "Nobel") - 0.15); add(chaching(-21), T("b1", "Nobel") - 0.05)
# drinks
add(fire_roar(1.0, -26), S["S10"]); add(pop(-22, 1100), T("c1", "how") - 0.1)
dt7 = (T("c2", "drinks") - S["S11"] - 0.1) / 7
for j in range(7): clink(S["S11"] + 0.15 + j * dt7, -25, 2600 + 120 * j)
for j in range(12): add(tick(-29, 2000 + 60 * j), S["S11b"] + 0.05 + j * 0.075)
add(gulp(-21), T("c3", "Water")); add(pop(-23, 500), T("c3", "Fizzy")); add(buzzer(-25, 0.35), T("c3", "badly.") - 0.2)
add(boom(-16, 0.4), T("c3", "milk!") - 0.15); add(ding(-22, 2093), T("c3", "milk!"))
add(pop(-22, 900), T("c4", "skim") - 0.15); add(pop(-22, 1100), T("c4", "whole") - 0.15); add(ding(-25, 1568), T("c4", "whole") + 0.3)
for j in range(3): add(pop(-24, 700 + 150 * j), T("c4", "proteins") - 0.2 + 0.15 * j)
# birds + mice
add(thud(-15), S["S14"] + 0.7); add(pop(-20, 400), S["S14"] + 0.72)
add(chirp(-22), S["S14b"] + 0.1); add(fire_roar(0.9, -26), S["S14b"] + 0.2)
for j in range(int((S["S15b"] - S["S15"]) * 1.6)): add(gulp(-21), S["S15"] + (j + 0.6) / 1.6)
add(chirp(-23, 4), S["S15"] + 0.2)
for j in range(3): add(chirp(-26, 2), S["S15b"] + 0.3 + 0.6 * j)
for j in range(3): add(pop(-26, 1300 - 100 * j), S["S15b"] + 0.6 + 0.12 * j + 0.5)
add(ding(-25, 1760), T("d2", "grow.") - 0.1)
for j in range(int((S["S16b"] - S["S16"]) / 0.22)): add(crunch(-25, 0.08), S["S16"] + 0.05 + 0.22 * j)
add(squeak(-21), S["S16"] + 0.3)
add(fire_roar(0.9, -20), S["S16b"] + 0.35); add(squeak(-18), S["S16b"] + 0.4); add(whoosh(0.4, level=-23), S["S16b"] + 0.85)
add(ding(-24, 1568), T("d4", "spicy.") - 0.2)
add(chirp(-23), S["S17b"] + 0.2); add(pop(-22, 1300), S["S17b"] + 0.3); add(buzzer(-25, 0.3), S["S17b"] + 0.8); add(squeak(-22), S["S17b"] + 0.85)
# recap + send
for j in range(3): add(pop(-21, 900 + 200 * j), S["S18"] + 0.2 + 0.35 * j)
add(thud(-15), T("e1", "burn.") - 0.2); add(pop(-22, 1000), T("e1", "milk") - 0.15)
add(pop(-21, 900), S["S19"] + 0.05); add(gulp(-21), S["S19"] + 0.5); add(gulp(-21), S["S19"] + 0.85)
add(pop(-18, 1300), T("e2", "Send") + 0.3); add(ding(-22, 2093), T("e2", "Send") + 0.32)
vend = LINES["e2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1174.7, 1480, 1760, 2349)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

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
