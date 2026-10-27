"""Mix: narrator VO + ducked/carved surf-rock score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 10): vinyl record scratch for the freeze-frame hook, candy-wrapper crinkle, cartoon boing, key jingle."""
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
TFZ = T("i1", "myth?") - 0.12
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


def rec_scratch(level=-16):
    """vinyl record scratch ('wikka'): two fast strokes = band-passed noise + a buzzy tone whose pitch follows the hand speed."""
    out = []
    for d, up in ((0.11, True), (0.16, False)):
        n_ = int(d * SR); t2 = np.arange(n_) / SR; k = t2 / d
        sp = np.sin(np.pi * k) if up else np.sin(np.pi * k) ** 0.7
        fr = 120 + 1400 * sp
        tone = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * 0.6
        noi = rng.standard_normal(n_)
        f_, t_, Z = signal.stft(noi, SR, nperseg=256)
        fc = 400 + 3000 * np.interp(t_ / d, k, sp)
        mask = np.exp(-0.5 * ((np.log2(np.maximum(f_, 20))[:, None] - np.log2(fc)[None]) / 0.6) ** 2)
        _, w_ = signal.istft(Z * mask, SR, nperseg=256); w_ = w_[:n_]
        x = (tone + 1.5 * w_ / (np.abs(w_).max() + 1e-9)) * sp
        out.append(x)
    x = np.concatenate(out); x = signal.sosfilt(signal.butter(2, [150, 6000], "band", fs=SR, output="sos"), x)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def crinkle(level=-24, dur=0.45):
    """candy-wrapper crinkle: sparse bright crackles with a slow envelope."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.02)
    x = signal.sosfilt(signal.butter(2, [2500, 11000], "band", fs=SR, output="sos"), x)
    x = signal.lfilter([1], [1, -0.6], x) * np.sin(np.pi * t2 / dur)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, np.roll(x, 90)], 1)


def boing(level=-20, f0=220, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = f0 * (1 + 0.35 * np.sin(2 * np.pi * 14 * t2) * np.exp(-t2 / 0.25)) * (1 + 0.6 * np.exp(-t2 / 0.03))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.22) * np.minimum(1, t2 / 0.003)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def jingle(level=-24):
    out = np.zeros((int(0.55 * SR), 2), np.float32)
    for j in range(5):
        y = ding(level - 4, 3200 + 500 * rng.random())[: int(0.25 * SR)] * np.exp(-np.arange(int(0.25 * SR)) / SR / 0.05)[:, None]
        i = int(j * 0.05 * SR); out[i:i + len(y)] += y
    return out


def lock_click(level=-15):
    out = np.zeros((int(0.12 * SR), 2), np.float32)
    for k, (d0, f0) in enumerate(((0.0, 3200), (0.045, 2400))):
        n_ = int(0.05 * SR); t2 = np.arange(n_) / SR
        x = (np.sin(2 * np.pi * f0 * t2) + 0.6 * signal.sosfilt(signal.butter(2, [1500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))) * np.exp(-t2 / 0.006)
        i = int(d0 * SR); out[i:i + n_] += np.stack([x, x], 1)
    return out / np.abs(out).max() * db(level)


def tick(level=-28, f0=2400): return pop(level, f0)


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


# hook: candy + boings under the bounce -> record scratch freeze
add(crinkle(-29, 0.6), 0.05)
for j in range(int(TFZ * 1.9) + 1): add(boing(-28, 200 + 30 * j), j / 1.9 + 0.02)
add(rec_scratch(-14), TFZ - 0.02); add(thud(-18), TFZ)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
# bounce off the walls
uu = 0.0
for j in range(8):
    th = S["S1"] + (j * 0.5 + 0.25 - 0.25 * 0) / 0.85 - 0.25 / 0.85
    if S["S1"] <= th < S["S1b"]: add(boing(-23, 260 - 10 * j), th); add(thud(-25), th)
add(crinkle(-26), S["S1"] + 0.3)
add(pop(-22, 1100), T("i2", "tested") - 0.1); add(ding(-25, 1568), T("i2", "tested"))
# curtain tease
add(creak(-26, 0.7), S["S2"] + 0.2); add(whoosh(0.5, peak=0.6, f_lo=200, f_hi=1500, level=-25), T("i3", "weirder.") - 0.3); add(boom(-19, 0.35), T("i3", "weirder.") - 0.2)
# the myth
add(pop(-20, 800), T("a1", "myth.") - 0.15); add(crinkle(-24), S["S3"] + 0.1)
for j in range(8): add(tick(-27, 1800 + 120 * j), T("a1", "Sugar") + 0.1 * j)
add(boom(-14, 0.45), S["S3b"] + 0.02); add(boing(-18, 330), S["S3b"] + 0.1); add(boing(-20, 280), S["S3b"] + 0.5)
# busted
add(scratch(-20, 0.25), S["S4"] + 0.1); stamp(S["S4"] + 0.15, -14); add(buzzer(-24, 0.4), S["S4"] + 0.2)
add(whoosh(0.5, peak=0.7, f_lo=200, f_hi=2000, level=-25), T("a2", "why.") - 0.2)
# science
bubbles(S["S5"] + 0.2, 6, -28); add(ding(-24, 2093), T("b1", "riding") - 0.1)
add(pop(-23, 1000), S["S5b"] + 0.1)
for j in range(5): add(pop(-26, 1300 + 100 * j), S["S5b"] + 0.4 + 0.3 * j)
add(whoosh(0.4, peak=0.6, f_lo=400, f_hi=3000, level=-27), T("b2", "rises,") - 0.3)
add(ding(-23, 1760), T("b2", "wakes") - 0.1); add(pop(-21, 900), T("b2", "wakes"))
add(pop(-23, 700), T("b2", "behind") - 0.1)
for j in range(5): add(jingle(-27), T("b3", "insulin.") - 0.3 + j * 0.18)
add(ding(-22, 2093), T("b3", "key.") - 0.15); add(jingle(-24), T("b3", "key.") - 0.1)
add(jingle(-25), S["S8"] + 0.2); add(lock_click(-15), T("b4", "cells,") - 0.1); add(creak(-24, 0.5), T("b4", "cells,") + 0.3)
for j in range(6): add(pop(-25, 900 + 80 * j), T("b4", "moves") - 0.1 + 0.18 * j)
add(pop(-22, 1200), T("b4", "used") - 0.1); add(whoosh(0.3, level=-26), T("b4", "used")); add(thud(-21), T("b4", "stored.") - 0.1)
add(tick(-27, 2000), S["S9"] + 0.6); add(tick(-27, 2000), S["S9"] + 2.0); add(ding(-24, 1568), T("b5", "tight") - 0.1)
add(beep(-26, 2400, 0.12), T("b5", "thermostat.") - 0.1); add(beep(-28, 2400, 0.08), T("b5", "thermostat.") + 0.1)
# part 2: blind tests
add(boom(-17, 0.4), S["S10"] + 0.05); card_in(S["S10"] + 0.1, -26)
add(buzzer(-26, 0.3), T("c1", "trust") - 0.1); stamp(T("c1", "blind") + 0.15, -15)
add(pop(-21, 900), T("c2", "sugar.") - 0.2)
clink(T("c2", "sugar.") + 0.2, -23, 3000); add(crinkle(-24, 0.4), T("c2", "sweetener") - 0.1)
add(ding(-23, 1760), T("c2", "same.") - 0.15)
add(pop(-23, 600), T("c3", "nobody") - 0.15); add(pop(-23, 650), T("c3", "nobody") + 0.1)
add(boing(-20, 300), T("c3", "scientists.") - 0.15); add(pop(-21, 500), T("c3", "scientists.") - 0.1)
add(pop(-21, 900), T("c4", "nineteen") - 0.15)
for j in range(23):
    tj = T("c4", "pooled") - 0.25 + j * max(0.4, T("c4", "tests.") + 0.1 - T("c4", "pooled") + 0.25) / 23
    add(tick(-29, 1500 + 40 * j), tj)
add(boom(-15, 0.4), T("c5", "didn't") - 0.1); stamp(T("c5", "didn't") - 0.1, -16)
# part 3: parent test
add(creak(-24, 0.6), S["S15"] + 0.2); add(pop(-21, 800), S["S15"] + 0.35); add(boom(-17, 0.35), T("d1", "wild.") - 0.15)
for j in range(12): add(tick(-28, 2000 + 50 * j), S["S16"] + 0.05 + j * 0.08)
stamp(T("d2", "sugar-free.") - 0.15, -15); add(ding(-24, 2093), T("d2", "sugar-free."))
add(whoosh(0.3, level=-27), T("d3", "told...") - 0.15); add(pop(-22, 700), T("d3", "told...")); add(pop(-21, 1100), T("d3", "told...") + 0.15)
add(thud(-18), T("d3", "big") - 0.1)
for j in range(5): add(tick(-26, 1200 + 300 * j), T("d4", "hyper.") - 0.3 + 0.1 * j)
stamp(T("d4", "hyper.") + 0.0, -17)
add(pop(-22, 500), T("d4", "controlled") - 0.15)
add(pop(-21, 900), S["S19"] + 0.05); add(pop(-21, 900), S["S19"] + 0.15); add(ding(-24, 1568), S["S19"] + 0.4)
add(buzzer(-27, 0.25), T("d5", "Different") - 0.1)
add(boom(-16, 0.4), T("d5", "heads!") - 0.2); add(ding(-22, 2093), T("d5", "heads!") - 0.15)
# the real rush
add(whoosh(0.9, peak=0.8, f_lo=200, f_hi=2500, level=-25), T("e1", "where") - 0.6)
for j in range(4): add(pop(-25, 1100 + 150 * j), T("e1", "where") + 0.5 + 0.15 * j)
add(pop(-19, 1400), S["S21"] + 0.03); add(chaching(-26), S["S21"] + 0.1); add(creak(-25, 0.4), T("e2", "Halloween.") - 0.1)
for j in range(3): add(boing(-23, 250 + 40 * j), S["S21c"] + 0.05 + 0.25 * j)
add(beep(-27, 1800, 0.1), S["S21d"] + 0.2); add(boom(-14, 0.45), T("e2", "real") - 0.15); stamp(T("e2", "real") - 0.15, -16)
# catch + teeth + recap
add(pop(-24, 700), T("f1", "small") - 0.05); add(pop(-24, 800), T("f1", "small") + 0.15)
add(thud(-19), T("f2", "teeth.") - 0.2); add(pop(-22, 400), T("f2", "teeth.") - 0.15)
for j, tw in enumerate((T("g1", "insulin") - 0.15, T("g1", "blind") - 0.15, T("g1", "party") - 0.15)): add(pop(-21, 900 + 200 * j), tw)
add(scratch(-22, 0.22), T("g1", "rest.") - 0.12); stamp(T("g1", "rest.") + 0.05, -16)
# send + sting
add(pop(-21, 900), S["S25"] + 0.05); add(crinkle(-25), S["S25"] + 0.3)
add(pop(-18, 1300), T("g2", "Send") + 0.3); add(ding(-22, 2093), T("g2", "Send") + 0.32)
vend = LINES["g2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
for j, f0 in enumerate((1318.5, 1568, 1976, 2637)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

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
