"""Mix: narrator VO + ducked/carved cool-jazz score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 11): ice_crack (freeze-over crackle), sip (slurp), chatter (teeth chattering), wind (cold gust), plus
reused ding/clink/lock-click. Every cold moment gets an icy sound, every warm/real moment a dry one."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(41)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
TF0_ = T("i1", "mint...") + 0.05
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


def ice_crack(level=-16, dur=0.6):
    """freeze-over: dense bright crackles that thin out + a low 'crunch' body (ice forming fast)."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    dens = 0.08 * np.exp(-t2 / 0.18) + 0.004
    x = rng.standard_normal(n_) * (rng.random(n_) < dens)
    x = signal.lfilter([1], [1, -0.85], x)
    hi = signal.sosfilt(signal.butter(2, [1800, 12000], "band", fs=SR, output="sos"), x)
    lo = signal.sosfilt(signal.butter(2, [120, 900], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.06)
    y = hi / (np.abs(hi).max() + 1e-9) + 0.6 * lo / (np.abs(lo).max() + 1e-9)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 70)], 1)


def sip(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); fc = 900 + 1600 * t2 / dur
    y = np.zeros(n_)
    for i in range(0, n_, 512):
        sos = signal.butter(2, [fc[i] * 0.7, fc[i] * 1.3], "band", fs=SR, output="sos"); y[i:i + 512] = signal.sosfilt(sos, x[i:i + 512])
    y *= np.sin(np.pi * t2 / dur) ** 0.6 * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t2))
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, y], 1)


def chatter(level=-26, dur=0.6, rate=16):
    out = np.zeros(int(dur * SR))
    for j in range(int(dur * rate)):
        c = pop(level, 2200 + 300 * rng.random())[:, 0][: int(0.03 * SR)] * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.006)
        i = int(j / rate * SR); out[i:i + len(c)] += c[: len(out) - i]
    return np.stack([out, out], 1)


def wind(level=-27, dur=1.2):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); y = np.zeros(n_)
    fc = 600 + 500 * np.sin(np.pi * t2 / dur) + 200 * np.sin(2 * np.pi * 1.3 * t2)
    for i in range(0, n_, 1024):
        sos = signal.butter(2, [fc[i] * 0.8, fc[i] * 1.25], "band", fs=SR, output="sos"); y[i:i + 1024] = signal.sosfilt(sos, x[i:i + 1024])
    y *= np.sin(np.pi * t2 / dur) ** 1.2
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 300)], 1)


def lock_click(level=-15):
    out = np.zeros((int(0.12 * SR), 2), np.float32)
    for k, (d0, f0) in enumerate(((0.0, 3200), (0.045, 2400))):
        n_ = int(0.05 * SR); t2 = np.arange(n_) / SR
        x = (np.sin(2 * np.pi * f0 * t2) + 0.6 * signal.sosfilt(signal.butter(2, [1500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))) * np.exp(-t2 / 0.006)
        i = int(d0 * SR); out[i:i + n_] += np.stack([x, x], 1)
    return out / np.abs(out).max() * db(level)


def tick(level=-28, f0=2400): return pop(level, f0)


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def icy(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3136), t + 0.06); add(ding(lv - 6, 3951), t + 0.12)


# hook: chewing + sip -> FREEZE
for j in range(int(TF0_ / 0.3)): add(pop(-30, 500 + 40 * j), j * 0.3 + 0.05)
add(sip(-28, 0.35), max(0.0, TF0_ - 0.4))
add(ice_crack(-17, 0.7), TF0_ - 0.02); add(boom(-21, 0.35), TF0_); add(wind(-30, 1.6), TF0_ + 0.2); add(chatter(-30, 0.8), TF0_ + 0.7)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
# chew -> sip -> brrr
add(crinkle(-25, 0.4) if "crinkle" in globals() else pop(-24, 900), T("i2", "Chew") - 0.05)
add(sip(-22), T("i2", "sip") - 0.05); add(ice_crack(-17, 0.5), T("i2", "whoa,") - 0.1); add(chatter(-25, 0.7), T("i2", "freezing!") - 0.1)
# nothing got colder -> trick
stamp(T("i3", "nothing") + 0.0, -20); add(pop(-22, 800), T("i3", "colder.") - 0.1)
add(boing(-25, 300), T("i3", "trick!") - 0.15); add(ding(-27, 2093), T("i3", "trick!"))
add(wind(-28, 0.8), T("i4", "nose.") - 0.3)
# part 1
add(boom(-19, 0.35), S["S4"] + 0.05); card_in(S["S4"] + 0.1, -26); add(pop(-23, 1000), S["S4"] + 0.6)
icy(T("a1", "menthol,") - 0.1, -24)
for j in range(5): add(tick(-28, 1400 + 200 * j), S["S5"] + 0.15 + 0.2 * j)
add(pop(-22, 1200), T("a2", "nerve") - 0.2); add(ding(-25, 1760), T("a2", "wires") - 0.1)
for j in range(3): icy(T("a3", "cold") - 0.2 + 0.12 * j, -27)
for j in range(6): add(tick(-29, 2200 - 150 * j), S["S7"] + 0.3 + 0.25 * j)
add(beep(-25, 2800, 0.12), T("a4", "twenty-five") + 0.2); add(beep(-27, 2800, 0.1), T("a4", "twenty-five") + 0.4)
add(sip(-23), T("a5", "ice") - 0.1); clink(T("a5", "ice") + 0.05, -23, 3300)
add(ding(-17, 2093), S["S7c"] + 0.05); add(ding(-20, 2637), S["S7c"] + 0.08); add(ice_crack(-22, 0.4), S["S7c"] + 0.1)
add(whoosh(0.45, peak=0.7, f_lo=500, f_hi=4000, level=-25), S["S8"] + 0.15); add(lock_click(-15), T("a6", "fits") - 0.05)
add(lock_click(-17), S["S8b"] + 0.7); add(ding(-24, 1760), S["S8b"] + 0.75)
# click -> COLD
add(lock_click(-13), S["S9"] + 0.1); add(boom(-17, 0.35), S["S9"] + 0.1)
for j in range(6): add(beep(-27, 2400 + 200 * (j % 2), 0.08), S["S9"] + 0.4 + 0.14 * j)
add(whoosh(0.5, peak=0.8, f_lo=600, f_hi=5000, level=-25), S["S9b"] + 0.05)
add(ice_crack(-14, 0.6), T("a7", "COLD!") - 0.15); add(boom(-16, 0.4), T("a7", "COLD!") - 0.15); add(wind(-25, 1.4), T("a7", "COLD!"))
add(chatter(-27, 0.8), S["S10"] + 0.3)
add(buzzer(-26, 0.3), T("a8", "didn't") - 0.05); stamp(T("a8", "didn't") + 0.0, -16)
# part 2
add(boom(-18, 0.35), S["S11"] + 0.02); card_in(S["S11"] + 0.1, -26)
for j in range(4): add(pop(-29, 500), S["S11"] + 0.1 + 0.32 * j)
for j in range(8): add(tick(-27, 1800 + 300 * (j % 2)), T("b2", "jumpy.") - 0.15 + 0.07 * j)
add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=3000, level=-26), T("b2", "warmer") - 0.2); add(beep(-25, 2600, 0.12), T("b2", "warmer") + 0.3)
for j in range(4): add(beep(-29, 2400, 0.06), T("b3", "half") - 0.1 + 0.15 * j)
add(splash_s(-18) if "splash_s" in globals() else whoosh(0.4, peak=0.5, f_lo=300, f_hi=6000, level=-20), T("b3", "water") + 0.05)
add(ice_crack(-13, 0.6), T("b3", "screams!") - 0.15); add(boom(-15, 0.45), T("b3", "screams!") - 0.15)
for j in range(6): add(beep(-24, 3000 + 300 * (j % 2), 0.07), T("b3", "screams!") + 0.05 * j)
add(sip(-24), T("b4", "hot") - 0.1); icy(T("b4", "cool") - 0.1, -23); add(wind(-28, 0.9), T("b4", "cool"))
# part 3
add(boom(-18, 0.35), S["S15"] + 0.05); card_in(S["S15"] + 0.1, -26); stamp(T("c1", "two") - 0.1, -15)
add(pop(-24, 1400), S["S16"] + 0.15); add(pop(-24, 1500), S["S16"] + 0.35); add(scratch(-22, 0.25), T("c2", "without") - 0.15)
for j in range(6): add(pop(-27, 1800 + 100 * j), S["S16b"] + 0.2 + 0.14 * j)
stamp(T("c3", "gone!") - 0.15, -16)
add(chaching(-24), T("c4", "Nobel") - 0.15); add(boom(-17, 0.4), T("c4", "Nobel") - 0.15)
for j, f0 in enumerate((1568, 1976, 2349, 3136)): add(ding(-24, f0), T("c4", "Nobel") + 0.05 + 0.08 * j)
add(whoosh(0.4, level=-25), S["S17b"] + 0.3); add(boom(-21, 0.3), S["S17b"] + 0.4)
add(pop(-22, 700), T("c5", "heat") - 0.1); icy(T("c5", "cold") - 0.1, -24); stamp(LINES["c5"]["end"] - 0.35, -15)
# part 4: the nose
add(boom(-19, 0.35), S["S18"] + 0.05); card_in(S["S18"] + 0.1, -26)
add(pop(-22, 1100), T("d2", "menthol") - 0.1); add(pop(-22, 900), T("d2", "plain") - 0.1)
for j in range(10): add(tick(-28, 2000), S["S20"] + 0.2 + 0.12 * j)
add(ding(-22, 2093), T("d3", "clearer.") - 0.2)
for j in range(5): add(beep(-28, 1500, 0.08), S["S21"] + 0.3 + 0.25 * j)
add(buzzer(-23, 0.4), T("d4", "no") - 0.15); stamp(T("d4", "no") - 0.1, -15)
add(wind(-27, 1.2), S["S21b"] + 0.1); add(ding(-22, 2637), T("d5", "breathe!") - 0.2)
# takeaway + recap + send + sting
add(pop(-23, 900), T("e1", "temperature.") - 0.2); icy(T("e1", "feel.") - 0.2, -23)
for j, tw in enumerate((S["S23"] + 0.25, T("e2", "rings") - 0.15, T("e2", "jumpy,") - 0.15, T("e2", "nose.") - 0.15)): add(pop(-21, 900 + 200 * j), tw)
add(pop(-21, 900), S["S24"] + 0.05); add(chatter(-27, 0.6), S["S24"] + 0.3)
add(pop(-18, 1300), T("e3", "Send") + 0.3); add(ding(-22, 2093), T("e3", "Send") + 0.32)
vend = LINES["e3"]["end"] + 0.35
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
