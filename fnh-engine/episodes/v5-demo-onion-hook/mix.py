"""Mix: narrator VO + ducked/carved orchestral-caper score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 13, also added to sfx_lib): chop (knife through an onion onto a wooden board: crunch + wood knock), hiss (gas
escaping), snip (scissor blades: two metallic ticks), plip (water drop), sizzle (pan: fry noise with crackles), squirt
(juice spray), plus reused pop/ding/thud/boom/whoosh/buzzer/boing/clang."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(42)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
TC = T("i1", "cry...") - 0.1; TP = T("i1", "purpose?") - 0.1
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


def _st(y, d=60): return np.stack([y, np.roll(y, d)], 1)


def chop(level=-20):
    """knife through an onion onto a board: wet crunch + a low wooden knock."""
    n_ = int(0.25 * SR); t2 = np.arange(n_) / SR
    cr = signal.sosfilt(signal.butter(2, [900, 6000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.3)) * np.exp(-t2 / 0.04)
    kn = np.sin(2 * np.pi * 180 * t2) * np.exp(-t2 / 0.05) + 0.5 * np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.02)
    y = 0.7 * cr / (np.abs(cr).max() + 1e-9) + kn / np.abs(kn).max()
    return _st(y / np.abs(y).max() * db(level))


def hiss(level=-24, dur=0.8):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.sin(np.pi * t2 / dur) ** 0.6
    return _st(y / np.abs(y).max() * db(level), 200)


def snip(level=-20):
    out = np.zeros(int(0.2 * SR))
    for k, f0 in ((0, 3800), (int(0.07 * SR), 4300)):
        t2 = np.arange(int(0.05 * SR)) / SR; y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.008) + 0.4 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.003)
        out[k:k + len(y)] += y
    return _st(out / np.abs(out).max() * db(level))


def plip(level=-24, f0=900):
    t2 = np.arange(int(0.12 * SR)) / SR; f = f0 + 1400 * np.exp(-t2 / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 / 0.03)
    return _st(y / np.abs(y).max() * db(level))


def sizzle(level=-26, dur=2.0):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [3000, 11000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * 0.4
    cr = (rng.random(n_) < 0.0015) * rng.uniform(-1, 1, n_); y += signal.sosfilt(signal.butter(2, 2000, "high", fs=SR, output="sos"), cr) * 3
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 300)


def squirt(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [600, 4000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.08)
    return _st(y / np.abs(y).max() * db(level), 90)


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


# hook: chopping at 0.5 s period (hit at 35 % of each cycle), gas hiss, sob + tear plips on "cry"
tt = 0.35 * 0.5
while tt < S["S1"] - 0.05:
    add(chop(-22), tt); tt += 0.5
add(hiss(-27, 1.2), 0.3)
add(boom(-20, 0.3), TC); add(boing(-24, 300), TC + 0.02)
for j in range(8): add(plip(-27, 800 + 90 * j), TC + 0.1 + 0.11 * j)
add(pop(-20, 500), TP); add(scratch(-25, 0.2), TP + 0.05)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k == "iris": add(whoosh(0.45, peak=0.6, f_lo=400, f_hi=6000, level=-25), st - 0.05); add(pop(-24, 1600), st + 0.3)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
add(buzzer(-26, 0.25), T("i2", "trap!") - 0.1); add(pop(-20, 400), T("i2", "trap!") - 0.05)
add(boom(-15, 0.45), T("i2", "knife") - 0.05); add(hiss(-21, 1.0), T("i2", "knife"))
sparkle_sfx(T("i3", "can't") - 0.1, -24); stamp(T("i3", "can't") - 0.1, -19)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(whoosh(0.8, peak=0.7, f_lo=200, f_hi=6000, level=-24), T("a1", "An") - 0.2)
add(pop(-21, 1300), END - 1.2); add(ding(-24, 2093), END - 1.18)

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
