"""Mix: narrator VO + ducked/carved lo-fi cafe score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 14, also added to sfx_lib): gulp (throat bloop gliding down), rip (sticker peeling off), rattle (a key jiggling
in a lock that won't turn), buzz (bee: buzzy saw with flutter), tick (clock), charge (rising battery bleeps), plus reused
sip/pop/ding/thud/boom/whoosh/buzzer/boing/lock_click/clang."""
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
TD = T("i1", "doesn't") - 0.1
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


def gulp(level=-20):
    t2 = np.arange(int(0.22 * SR)) / SR; f = 420 * np.exp(-t2 / 0.08) + 120
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t2 / 0.22) ** 0.5
    return _st(y / np.abs(y).max() * db(level))


def rip(level=-20, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [1200, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.35)) * np.minimum(1, (dur - t2) / 0.1)
    return _st(y / np.abs(y).max() * db(level))


def rattle(level=-20, dur=0.6, rate=22):
    out = np.zeros(int(dur * SR))
    for k in range(int(dur * rate)):
        t2 = np.arange(int(0.03 * SR)) / SR; f0 = 2600 + 400 * (k % 2)
        y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.006) + 0.5 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.002)
        i0 = int(k / rate * SR); out[i0:i0 + len(y)] += y[: len(out) - i0]
    return _st(out / np.abs(out).max() * db(level))


def buzz(level=-26, dur=1.0, f0=230):
    t2 = np.arange(int(dur * SR)) / SR; f = f0 + 12 * np.sin(2 * np.pi * 7 * t2)
    y = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.7 + 0.3 * np.sin(2 * np.pi * 31 * t2))
    y = signal.sosfilt(signal.butter(2, [200, 3000], "band", fs=SR, output="sos"), y) * np.minimum(1, np.minimum(t2 / 0.08, (dur - t2) / 0.15))
    return _st(y / np.abs(y).max() * db(level), 120)


def tick(level=-27):
    t2 = np.arange(int(0.04 * SR)) / SR; y = np.sin(2 * np.pi * 3200 * t2) * np.exp(-t2 / 0.004)
    return _st(y / np.abs(y).max() * db(level))


def charge(t0, t1, level=-27):
    k = 0; tt = t0
    while tt < t1: add(beep(level, 900 + 160 * k, 0.05), tt); tt += 0.12; k += 1


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


# hook: gulps while the battery charges, sticker rip + record stop on the fake
for j in range(int(max(0, TD - 0.3) / 0.33)): add(gulp(-22), 0.15 + j * 0.33)
charge(0.2, TD - 0.3, -28)
add(rip(-18), TD); add(boing(-24, 300), TD + 0.05); add(buzzer(-25, 0.3), TD + 0.25); add(pop(-20, 500), TD + 0.25)
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k == "iris": add(whoosh(0.45, peak=0.6, f_lo=400, f_hi=6000, level=-25), st - 0.05); add(pop(-24, 1600), st + 0.3)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * i), st + 0.02); add(thud(-21), st + 0.02)
stamp(T("i2", "bit.") - 0.15, -17)
add(whoosh(0.35, peak=0.6, f_lo=600, f_hi=4000, level=-24), T("i2", "hides") - 0.3); add(pop(-21, 600), T("i2", "hides") - 0.05)
stamp(T("i3", "back") - 0.15, -18); add(chaching(-21), T("i3", "interest.") - 0.2)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(whoosh(0.8, peak=0.7, f_lo=200, f_hi=6000, level=-24), T("a1", "All") - 0.25)
for j in range(6): add(beep(-31, 1800 + 140 * j, 0.04), T("a1", "energy.") - 0.3 + 0.1 * j)
for j in range(9): add(pop(-27, 700 + 70 * j), S["S4"] + 0.18 * j)
sparkle_sfx(T("a3", "keys.") - 0.2, -25)
for j in range(6): add(pop(-29, 500 + 40 * j), S["S5b"] + 0.5 + 0.35 * j)
for j in range(3): clink(S["S6"] + 0.3 + 0.15 * j, -26, 2800)
add(whoosh(0.4, level=-25), S["S6b"] + 0.2); add(lock_click(-14), T("a5", "clicks") - 0.12); add(boing(-27, 120), T("a5", "slows") - 0.15)
add(sip(-30, 0.6), S["S6c"] + 0.15)          # yawn breath
for j in range(3): add(boing(-31, 140), S["S7"] + 0.4 + 0.9 * j)
# part 2
add(boom(-19, 0.35), S["S8"] + 0.02); card_in(S["S8"] + 0.1, -26); add(sip(-22, 0.45), T("b1", "coffee.") - 0.2); add(gulp(-21), T("b1", "coffee.") + 0.25)
for j in range(5): add(pop(-29, 400 + 50 * j), S["S9"] + 0.2 + 0.35 * j)
add(ding(-23, 1760), T("b2", "brain.") - 0.15)
stamp(T("b3", "like") - 0.15, -17)
add(whoosh(0.3, peak=0.7, f_lo=800, f_hi=5000, level=-24), S["S11"] + 0.1); clink(S["S11"] + 0.7, -20, 2400)
add(rattle(-19, 0.8), T("b4", "can't") - 0.15); add(buzzer(-25, 0.25), T("b4", "can't") + 0.1)
for j in range(3): clink(S["S12"] + 0.1 + 0.2 * j, -24, 2600)
stamp(T("b5", "blocking") - 0.15, -16)
for j in range(5): add(boing(-25, 260 + 30 * (j % 2)), S["S13"] + 0.45 + 0.37 * j)
add(boing(-22, 520), S["S13b"] + 0.05); sparkle_sfx(S["S13b"] + 0.1, -25)
add(ding(-25, 1568), S["S14"] + 0.3); add(pop(-22, 900), T("b7", "hidden.") - 0.2)
# part 3: crash
add(boom(-19, 0.35), S["S15"] + 0.02); card_in(S["S15"] + 0.1, -26); add(boing(-25, 240), S["S15"] + 0.6)
for j in range(12): clink(S["S16"] + 0.15 + 0.2 * j, -29, 2200 + 120 * (j % 4))
add(whoosh(0.5, peak=0.6, f_lo=800, f_hi=6000, level=-23), T("c3", "wears") - 0.15)
add(whoosh(0.4, peak=0.8, f_lo=200, f_hi=4000, level=-18), T("c3", "rush") - 0.3); add(boom(-15, 0.5), T("c3", "rush") - 0.1)
for j in range(3): add(lock_click(-18), T("c3", "rush") + 0.05 + 0.07 * j)
add(boom(-14, 0.6), T("c4", "crash.") - 0.05); add(thud(-15), T("c4", "crash.") - 0.03)
add(rustle(-24, 0.5), S["S18b"] + 0.1); stamp(T("c4", "lends") + 0.15, -17)
# part 4
add(boom(-19, 0.35), S["S19"] + 0.02); card_in(S["S19"] + 0.1, -26)
tt = S["S19"] + 0.25
while tt < S["S20"] + 1.5: add(tick(-25), tt); tt += 0.5
for j in range(6): add(pop(-28, 500 - 30 * j), S["S20"] + 0.5 + 0.25 * j)
add(ding(-22, 1318.5), T("d2", "half") - 0.3)
add(pop(-23, 700), S["S21"] + 0.1); add(whoosh(1.2, peak=0.5, f_lo=200, f_hi=1500, level=-28), S["S21"] + 0.3); add(pop(-20, 900), T("d3", "quarter") - 0.2)
for j in range(4): add(beep(-31, 1200, 0.05), S["S22"] + 0.3 + 0.6 * j)
add(pop(-21, 600), T("d4", "six") - 0.15)
add(whoosh(0.3, level=-25), S["S23"] + 0.1); stamp(T("d5", "hour") - 0.1, -16)
add(boing(-24, 200), T("d5", "notice!") - 0.1)
add(whoosh(0.5, peak=0.5, level=-24), T("d6", "earlier") - 0.3); add(ding(-22, 2093), T("d6", "earlier") + 0.3)
# part 5 + bees
add(boom(-19, 0.35), S["S25"] + 0.02); card_in(S["S25"] + 0.1, -26)
for j in range(int((S["S26"] - S["S25"]) * 3)): add(rustle(-30, 0.12), S["S25"] + 0.1 + j / 3)
for j in range(2): add(pop(-20, 900 + 300 * j), T("e2", "extra") - 0.2 + 0.2 * j)
for j in range(3): clink(T("e2b", "more") - 0.15 + 0.15 * j, -22, 2000 + 300 * j)
add(boom(-20, 0.3), S["S27"] + 0.02); add(buzz(-25, max(0.5, S["S28"] - S["S27"] - 0.1)), S["S27"] + 0.05)
sparkle_sfx(T("e4", "caffeine") - 0.15, -24); add(plip(-24, 900), T("e4", "nectar.") - 0.1)
add(buzz(-28, 1.0, 260), S["S29"] + 0.2)
for j in range(8): add(beep(-30, 1400 + 140 * j, 0.04), T("e5", "three") - 0.3 + 0.06 * j)
stamp(T("e5", "three") + 0.2, -18)
add(buzz(-25, max(0.5, S["S30b"] - S["S30"]), 240), S["S30"]); add(buzz(-30, 1.0, 280), S["S30"] + 0.3)
add(sip(-24, 0.4), S["S30b"] + 0.2)
for j, w in enumerate(("add", "blocks", "waits")): add(pop(-21, 900 + 200 * j), T("f1", w) - 0.15)
add(pop(-21, 900), S["S32"] + 0.05)
add(pop(-18, 1300), T("f2", "Send") + 0.3); add(ding(-22, 2093), T("f2", "Send") + 0.32)
vend = LINES["f2"]["end"] + 0.35
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
