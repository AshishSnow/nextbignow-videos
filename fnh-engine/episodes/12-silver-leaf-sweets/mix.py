"""Mix: narrator VO + ducked/carved Bollywood-festive score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 12): clang (metal strike with inharmonic partials, for hammer hits on silver), rustle (paper sheets),
det_beep (metal-detector beeps that speed up), plus reused pop/ding/thud/stamp/buzzer/whoosh."""
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
TB = T("i1", "silver") - 0.1
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


def clang(level=-20, f0=1250, dur=0.5):
    """metal strike: a few inharmonic partials (bar/plate modes) with fast attack + a click of noise."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR; y = np.zeros(n_)
    for r, a, tau in ((1.0, 1.0, 0.18), (2.76, 0.6, 0.09), (5.4, 0.35, 0.05), (8.93, 0.2, 0.03)):
        y += a * np.sin(2 * np.pi * f0 * r * t2 + rng.uniform(0, 6)) * np.exp(-t2 / tau)
    y += 0.5 * signal.sosfilt(signal.butter(2, [2000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.004)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 40)], 1)


def rustle(level=-26, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (0.4 + 0.6 * (rng.random(n_) < 0.08))
    y = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), x) * np.sin(np.pi * t2 / dur) ** 0.7
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 120)], 1)


def det_beep(t0, t1, level=-25, f0=1900):
    """metal detector: beeps that get faster and higher until t1."""
    tt = t0; k = 0
    while tt < t1:
        q = clamp((tt - t0) / max(0.1, t1 - t0)); add(beep(level, f0 + 700 * q, 0.06), tt); tt += 0.32 - 0.24 * q; k += 1


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def shine(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


# hook: detector sweeping -> BEEP BEEP on the silver
det_beep(0.1, TB, -30, 1500)
for j in range(10): add(beep(-21, 3100, 0.07), TB + 0.02 + 0.11 * j)
add(boom(-21, 0.3), TB); shine(TB + 0.05, -23)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k == "iris": add(whoosh(0.45, peak=0.6, f_lo=400, f_hi=6000, level=-25), st - 0.05); add(pop(-24, 1600), st + 0.3)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
add(clang(-20, 1500, 0.6), T("i2", "Real") - 0.1); shine(T("i2", "Real"), -25)
for j in range(4): add(crinkle(-25, 0.15) if "crinkle" in globals() else pop(-26, 400), S["S1b"] + 0.1 + 0.3 * j)
add(pop(-19, 300), T("i2", "eat") - 0.05)
add(buzzer(-27, 0.25), T("i3", "not") - 0.1); add(boing(-26, 260), S["S2"] + 0.3)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); shine(T("a1", "vark.") - 0.1, -23)
add(rustle(-24, 0.6), S["S3b"] + 0.2); add(pop(-24, 1300), S["S3b"] + 0.7)
stamp(S["S4"] + 0.15, -16)
for j in range(8): add(tick(-29, 1600 + 150 * j) if "tick" in globals() else pop(-29, 1600 + 150 * j), S["S4b"] + 0.1 + 0.12 * j)
add(ding(-22, 2093), S["S4b"] + 1.1)
add(pop(-23, 600), T("a3", "lump") - 0.15); add(whoosh(0.3, level=-27), T("a3", "sheet") - 0.15)
for j, tw in enumerate((S["S6"] + 0.15, T("a4", "small") - 0.1, T("a4", "silver") - 0.1)): add(pop(-21, 800 + 200 * j), tw)
for j in range(5): add(rustle(-27, 0.25), S["S6b"] + 0.1 + 0.3 * j)
# hammering: clang + thud on every hit (same timing as the animation)
for t0, per, t1 in ((T("a5", "hammer") - 0.35, 0.55, S["S7b"]), (S["S7b"] - 0.2, 0.42, S["S8"])):
    tt = t0 + per * 0.98
    while tt < t1 - 0.02:
        if tt > S["S7"]: add(clang(-24, 1100 + 80 * rng.random(), 0.35), tt); add(thud(-22), tt)
        tt += per
for j in range(10): add(tick(-28, 2000) if "tick" in globals() else pop(-28, 2000), S["S7b"] + 0.15 + 0.15 * j)
u0 = S["S8"] + 0.2
for j in range(6): add(clang(-26, 1300 + 60 * j, 0.25), u0 + j * 0.45)
# part 2: how thin
add(boom(-19, 0.35), S["S9"] + 0.02); card_in(S["S9"] + 0.1, -26)
add(rustle(-24, 0.5), S["S9b"] + 0.15); add(thud(-20), S["S9b"] + 0.55)
for j in range(6): add(beep(-29, 2200, 0.05), T("b1", "eighty") - 0.65 + 0.1 * j)
stamp(T("b1", "eighty") - 0.15, -18)
add(rustle(-27, 0.4), S["S10"] + 0.2)
add(boom(-17, 0.4), T("b2", "three") - 0.15); shine(T("b2", "three") - 0.1, -22)
add(pop(-23, 1400), S["S11"] + 0.4); add(ding(-24, 1760), T("b3", "hair.") - 0.2)
add(beep(-26, 2600, 0.1), S["S12"] + 0.3); shine(S["S12"] + 0.4, -27)
# part 3: the secret
add(boom(-19, 0.35), S["S13"] + 0.02); card_in(S["S13"] + 0.1, -26); add(lock_click(-17), T("c1", "secret.") - 0.15)
add(creak(-24, 0.5) if "creak" in globals() else whoosh(0.4, level=-26), S["S14"] + 0.2)
add(boom(-15, 0.45), S["S14b"] + 0.05); add(scratch(-22, 0.25), S["S14b"] + 0.05)
add(rec_scratch(-20) if "rec_scratch" in globals() else buzzer(-24, 0.3), T("c3", "wasn't") - 0.15)
stamp(T("c4", "banned") - 0.1, -14); add(buzzer(-24, 0.35), T("c4", "banned") - 0.05)
add(rustle(-25, 0.4), T("c5", "paper") - 0.15); add(rustle(-25, 0.4), T("c5", "plastic") - 0.15); add(ding(-22, 2093), T("c5", "plastic") + 0.15)
# part 4: the fakes
add(boom(-19, 0.35), S["S18"] + 0.02); card_in(S["S18"] + 0.1, -26)
for j in range(14): add(pop(-30, 1800 + 40 * j), T("d2", "hundred") - 0.15 + 0.07 * j)
add(ding(-24, 1760), T("d3", "ten") - 0.1); add(buzzer(-25, 0.3), T("d3", "ten") + 0.1)
add(clang(-18, 700, 0.5), T("d3", "aluminum!") - 0.2); add(boom(-16, 0.4), T("d3", "aluminum!") - 0.2)
stamp(T("d4", "half") - 0.15, -16)
add(pop(-22, 500), T("d5", "lead") - 0.15); add(pop(-22, 650), T("d5", "nickel.") - 0.15)
# part 5: the twist
add(boom(-17, 0.4), S["S23"] + 0.02); card_in(S["S23"] + 0.1, -26)
add(pop(-22, 900), S["S23b"] + 0.05); shine(T("e1", "food") - 0.1, -24)
stamp(T("e2", "can't") - 0.1, -15); add(buzzer(-26, 0.3), T("e2", "can't"))
add(pop(-23, 900), T("e3", "harmful.") - 0.2); add(pop(-23, 1100), T("e3", "data.") - 0.2)
# takeaway, recap, send, sting
shine(S["S26"] + 0.1, -22); add(ding(-22, 2093), T("f1", "shine,") - 0.15); add(buzzer(-27, 0.25), T("f1", "health.") - 0.15)
for j, tw in enumerate((T("f2", "real") - 0.15, T("f2", "hammered") - 0.15, T("f2", "sometimes") - 0.15)): add(pop(-21, 900 + 200 * j), tw)
add(clang(-26, 1400, 0.3), T("f2", "hammered") - 0.1)
add(chaching(-25), T("f3", "treat.") - 0.15)
add(pop(-21, 900), S["S29"] + 0.05)
add(pop(-18, 1300), T("f4", "Send") + 0.3); add(ding(-22, 2093), T("f4", "Send") + 0.32)
vend = LINES["f4"]["end"] + 0.35
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
