"""Mix: narrator VO + ducked/carved bluegrass score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 19, also added to sfx_lib): creep (the browning spreading: a soft granular crackle that thickens and darkens), machine_whir
(PPO the enzyme machine: a tiny motor whir + a click), dunk (a slice dropped into water: plop + slosh), squeeze (a lemon half squeezed:
squirt + drips), shimmer (the Arctic apple: a cold high sparkle); reused: whoosh/pop/ding/thud/boom/boing/buzzer/plip/sizzle/hiss/fizz/
wash/squelch/clang/tick/crinkle/clack/crunch/chop/snap/rec_scratch/chaching/simmer/knob/fridge_hum."""
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
TTAN = T("i1", "tan?") - 0.15; TCUT = T("b1", "cut") - 0.08
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-5)
exec(open(f"{_D}/sfx_lib.py").read())


def creep(level=-26, dur=2.0):
    """the browning spreading: a soft granular crackle whose grains get denser and lower as it goes."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k in range(int(dur * 60)):
        i = int((rng.uniform(0, 1) ** 0.6) * (dur - 0.05) * SR); seg = t2[: int(0.02 * SR)]; f0 = rng.uniform(1800, 4200) * (1 - 0.5 * i / len(t2))
        y[i:i + len(seg)] += np.sin(2 * np.pi * f0 * seg) * np.exp(-seg / 0.004) * rng.uniform(0.3, 1.0)
    drone = signal.sosfilt(signal.butter(2, [90, 260], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (t2 / dur) ** 1.5 * 0.5
    y = y + drone
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.4
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 90)


def machine_whir(level=-26, dur=0.6, f0=140):
    """PPO the tiny machine: a motor whir (buzzy saw at f0 rising) + a little click at the end."""
    t2 = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.6 * t2 / dur)) / SR
    y = (signal.sawtooth(ph) * 0.5 + np.sin(ph * 2) * 0.3) * np.exp(-t2 / (dur * 0.6))
    y = signal.sosfilt(signal.butter(2, 2200, "low", fs=SR, output="sos"), y)
    i = int((dur - 0.05) * SR); seg = t2[: int(0.03 * SR)]
    y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [2000, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.004) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def dunk(level=-20, dur=0.7):
    """a slice dropped into water: a plop (pitched blip down) + a slosh (band-passed noise swell)."""
    t2 = np.arange(int(dur * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(420 * (1 + 1.5 * np.exp(-t2 / 0.02))) / SR) * np.exp(-t2 / 0.05) * 1.2
    sl = signal.sosfilt(signal.butter(2, [300, 2600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-((t2 - 0.14) / 0.12) ** 2) * 0.7
    y = y + sl
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 70)


def squeeze(level=-24, dur=0.8):
    """a lemon squeezed: a wet squirt + three drips."""
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [900, 5000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.12) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 23 * t2)))
    for k in range(3):
        i = int((0.25 + 0.16 * k) * SR); seg = t2[: int(0.06 * SR)]
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum((1500 + 300 * k) * (1 + 0.8 * np.exp(-seg / 0.008))) / SR) * np.exp(-seg / 0.015) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def shimmer(level=-26, dur=1.2):
    """a cold high sparkle (the Arctic apple): detuned high sines with a slow flutter."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k, f0 in enumerate((2637, 3136, 3951, 5274)):
        y += np.sin(2 * np.pi * f0 * (1 + 0.002 * np.sin(2 * np.pi * (5 + k) * t2)) * t2) * np.exp(-t2 / (0.5 + 0.1 * k)) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + k) * t2)) / (k + 1)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 110)


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


def pops_at(t0, n_=5, gap=0.12, lv=-25):
    for j in range(n_): add(pop(lv, 900 + 200 * (j % 4)), t0 + gap * j)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * (i % 8)), st + 0.02); add(thud(-21), st + 0.02)
# HOOK: the knife is down at frame 0 (a crunch), the browning creeps while the clock ticks; TAN = a sunny ding-chord + a boom
add(crunch(-20), 0.02); add(creep(-24, max(1.2, TTAN - 0.3)), 0.3)
for j in range(int((TTAN - 0.2) / 0.5)): add(tick(-30), 0.25 + 0.5 * j)
add(boom(-18, 0.4), TTAN); sparkle_sfx(TTAN + 0.05, -20); add(whoosh(0.3, peak=0.5, f_lo=500, f_hi=4000, level=-26), TTAN - 0.15); add(boing(-26, 260, 0.4), TTAN + 0.12)
stamp(T("i2", "melanin,") - 0.15, -18)
for j, w in enumerate(("skin,", "hair,", "eyes.")): add(pop(-24, 900 + 150 * j), T("i2", w) - 0.1); add(clack(-28, 1500), T("i2", w) - 0.08)
add(clack(-24, 1700), S["S1"] + 0.2); add(ding(-24, 2093), T("i3", "dip") - 0.1); add(tick(-28), T("i3", "lunchtime.") - 0.1); add(tick(-28), T("i3", "lunchtime.") + 0.3)
# part 1
add(boom(-19, 0.35), S["S2"] + 0.05); card_in(S["S2"] + 0.1, -26); add(whoosh(0.9, peak=0.6, f_lo=200, f_hi=3000, level=-23), T("a1", "millions") - 0.2); add(rustle(-27, 0.5), T("a1", "millions") + 0.4)
add(pop(-24, 1000), S["S2b"] + 0.2); add(clack(-26, 1600), T("a1", "walls.") - 0.1)
add(clang(-26, 900, 0.4), T("a2", "apart.") - 0.12); add(pop(-25, 700), T("a2", "apart.") - 0.1)
add(machine_whir(-23, 0.6, 140), S["S3b"] + 0.08); add(pop(-24, 1100), T("a2", "enzyme") - 0.1); stamp(T("a2", "PPO:") - 0.12, -19)
add(machine_whir(-24, 0.8, 120), S["S3c"] + 0.1); add(hiss(-30, 0.6), S["S3c"] + 0.5); stamp(T("a2", "job.") - 0.12, -20)
for j in range(3): add(boing(-27, 320 + 40 * j, 0.3), T("a3", "polyphenols.") - 0.2 + 0.08 * j)
stamp(T("a3", "polyphenols.") - 0.15, -19); add(pop(-25, 900), T("a3", "flavour") - 0.1)
add(clack(-24, 1400), T("a3", "never") - 0.12); add(pop(-24, 600), T("a3", "never") - 0.1)
# the cut
add(whoosh(0.3, peak=0.3, f_lo=400, f_hi=5000, level=-22), TCUT - 0.12); add(chop(-14), TCUT); add(boom(-17, 0.45), TCUT); add(crunch(-18), TCUT + 0.02)
add(snap(-22), T("b1", "smashes") - 0.1); add(crinkle(-22, 0.6), T("b1", "smashes") - 0.05); add(rec_scratch(-27), TCUT + 0.3)
add(squelch(-26, 0.5), S["S5b"] + 0.2); add(machine_whir(-25, 0.5, 160), T("b1", "meets") - 0.3); stamp(T("b1", "meets") - 0.12, -20)
for j in range(5): add(whoosh(0.4, peak=0.5, f_lo=400, f_hi=3500, level=-30), T("b2", "guest") - 0.1 + 0.12 * j)
add(pop(-26, 1300), T("b2", "guest") - 0.05); stamp(T("b2", "Oxygen.") - 0.15, -19); sparkle_sfx(T("b2", "Oxygen.") - 0.1, -26)
add(machine_whir(-22, 1.2, 130), T("b3", "grabs") - 0.1)
for j in range(5): add(plip(-27, 700 + 90 * j), T("b3", "grabs") + 0.18 * j + 0.5)
add(squelch(-21, 0.7), T("b3", "mashes") - 0.1); add(boom(-21, 0.35), T("b3", "mashes") - 0.1)
for j in range(4): add(pop(-26, 500 + 60 * j), S["S7b"] + 0.3 + 0.2 * j)
add(ding(-27, 1568), T("b3", "colourless.") - 0.1)
add(squelch(-24, 0.9), T("b4", "clump") - 0.1); add(stretch(-27, 0.7, True), T("b4", "bigger", 1) - 0.1); add(creep(-26, 1.0), T("b4", "bigger", 1))
add(crt_off(-28, 0.4), S["S8b"] + 0.02); add(creep(-22, 1.0), T("b4", "brown.") - 0.5); add(boom(-17, 0.5), T("b4", "brown.") - 0.12); stamp(T("b4", "melanin.") - 0.15, -17); add(boing(-25, 220, 0.5), T("b4", "melanin.") - 0.05)
# the tan
add(boom(-19, 0.35), S["S9"] + 0.05); add(whoosh(0.5, peak=0.6, f_lo=300, f_hi=3000, level=-25), S["S9"] + 0.1); sparkle_sfx(S["S9"] + 0.4, -26); add(creep(-27, 1.5), S["S9"] + 0.6)
add(tick(-27), S["S9b"] + 0.2); add(tick(-27), S["S9b"] + 0.6); add(tick(-27), S["S9b"] + 1.0); add(creep(-25, 1.4), S["S9b"] + 0.2); stamp(T("c1", "faster.") - 0.12, -20)
add(pop(-24, 800), S["S10"] + 0.3); add(boing(-27, 300, 0.4), S["S10"] + 0.5)
add(boom(-20, 0.35), T("c2", "defence") - 0.12); stamp(T("c2", "defence") - 0.12, -18)
for j in range(5): add(nibble(-29, 0.3, 12), T("c2", "bugs") - 0.1 + 0.15 * j)
add(buzzer(-27, 0.3), T("c2", "bugs") + 0.9); add(squeak(-28), T("c2", "bugs") + 1.0)
# the guess
add(crt_off(-27, 0.4), S["S11"] + 0.02); stamp(T("c3", "guess,") - 0.1, -19)
for j in range(4): add(tick(-28), S["S11"] + 0.4 + 0.5 * j)
add(pop(-24, 900), T("c3", "bad?") - 0.1)
stamp(S["S11b"] + 0.02, -15); add(boom(-18, 0.4), S["S11b"] + 0.02); add(chaching(-22), T("c4", "harmless.") - 0.12); sparkle_sfx(T("c4", "harmless.") - 0.05, -23)
add(squelch(-27, 0.5), T("c4", "soft") - 0.05); add(boing(-26, 180, 0.5), T("c4", "soft") - 0.05); add(pop(-27, 400), T("c4", "sad.") - 0.1)
# part 2 fixes
add(boom(-19, 0.35), S["S12"] + 0.1); card_in(S["S12"] + 0.15, -26)
for j, w in enumerate(("oxygen", "slows", "switches")): add(pop(-24, 900 + 120 * j), T("d1", w) - 0.12); add(clack(-28, 1600), T("d1", w) - 0.1)
add(squeeze(-22, 0.8), S["S13"] + 0.3); add(squeeze(-25, 0.8), S["S13"] + 1.3); add(plip(-26, 1300), S["S13"] + 0.9)
add(machine_whir(-26, 0.9, 90), T("d2", "acid") - 0.05); add(boing(-27, 150, 0.6), T("d2", "sluggish,") - 0.1)
add(chaching(-25), T("d2", "vitamin") - 0.1); sparkle_sfx(T("d2", "vitamin") - 0.05, -25); add(tick(-28), T("d2", "minutes") - 0.1); add(tick(-28), T("d2", "minutes") + 0.3); add(ding(-24, 2093), T("d2", "done.") - 0.08)
add(clack(-24, 1700), T("d3", "Honey") - 0.1); add(squelch(-27, 0.6), T("d3", "water,") - 0.05)
for j in range(3): add(dunk(-19, 0.7), T("d3", "dunk") - 0.1 + 0.12 * j + 0.45)
add(wash(-26, 1.0), T("d3", "dunk") + 0.6)
add(crinkle(-26, 0.5), T("d3", "coat") - 0.1)
for j in range(4): add(boing(-28, 400 + 50 * j, 0.25), T("d3", "oxygen") + 0.25 * j + 0.5)
add(buzzer(-28, 0.25), T("d3", "oxygen") + 0.2)
add(fridge_hum(-28, 3.0), S["S15"]); add(suction(-26), S["S15"] + 0.05); add(chatter(-30, 0.6, 14), S["S15"] + 0.6); stamp(T("d4", "fridge") - 0.1, -21)
add(knob(-24), S["S15b"] + 0.02); add(simmer(-28, 4.0, 9), S["S15b"] + 0.1); add(hiss(-27, 1.0), S["S15b"] + 0.3); add(crt_off(-26, 0.5), T("d4", "off") - 0.12); stamp(T("d4", "off") - 0.1, -19)
add(ding(-25, 1318.5), T("d4", "cooked") - 0.1)
# part 3 on purpose
add(crt_off(-27, 0.4), S["S16"] + 0.02); card_in(S["S16"] + 0.1, -27); stamp(T("e1", "purpose.") - 0.15, -18); add(boom(-19, 0.45), T("e1", "purpose.") - 0.15)
add(sip(-24, 0.35), S["S16b"] + 0.3); add(creep(-27, 1.2), S["S16b"] + 0.4); add(machine_whir(-27, 0.5, 150), T("e2", "reaction,") - 0.3); stamp(T("e2", "reaction,") - 0.12, -21)
add(pop(-24, 900), S["S16c"] + 0.05); add(clack(-27, 1500), S["S16c"] + 0.07); add(pop(-24, 1050), T("e2", "cocoa") - 0.1); add(clack(-27, 1500), T("e2", "cocoa") - 0.08)
for j, w in enumerate(("Avocados,", "bananas,", "potatoes:")): add(pop(-23, 800 + 150 * j), T("e3", w) - 0.12); add(creep(-29, 1.2), T("e3", w) + 0.2)
stamp(T("e3", "same") - 0.1, -21); add(squelch(-26, 0.6), T("e3", "grey") - 0.05); add(creep(-24, 1.0), T("e3", "grey")); stamp(T("e3", "Melanin.") - 0.15, -18); add(rec_scratch(-27), T("e3", "Melanin.") - 0.45)
# the arctic apple
add(boom(-20, 0.35), S["S18"] + 0.05); add(shimmer(-24, 1.4), T("f1", "Arctic") - 0.1); add(wind(-30, 1.2), S["S18"] + 0.2); stamp(T("f1", "Arctic") - 0.12, -20)
add(lock_click(-22), T("f1", "switched") - 0.08); add(crt_off(-27, 0.4), T("f1", "switched") - 0.05); add(chop(-22), T("f1", "cut") - 0.08); add(ding(-24, 2093), T("f1", "white") - 0.1); add(shimmer(-27, 1.0), T("f1", "white") - 0.05)
stamp(T("f2", "fifteen.") - 0.15, -17); add(pop(-25, 1000), T("f2", "blushes.") - 0.12); add(boing(-27, 300, 0.4), T("f2", "blushes.") - 0.1)
# recap + end
for j, w in enumerate(("cut", "enzyme", "melanin.")): add(pop(-21, 900 + 150 * j), T("g1", w) - 0.15)
for j, w in enumerate(("Lemon,", "honey", "cold", "heat")): add(ding(-24, (1318.5, 1568, 1760, 1976)[j]), T("g1", w) - 0.1)
stamp(T("g1", "fine") - 0.12, -19)
add(pop(-21, 900), S["S20"] + 0.05)
add(pop(-18, 1300), T("g2", "Send") + 0.3); add(ding(-22, 2093), T("g2", "Send") + 0.32)
vend = LINES["g2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); add(crunch(-24), vend + 0.5)
for j, f0 in enumerate((1318.5, 1568, 1976, 2637)): add(ding(-24, f0), vend + 0.25 + j * 0.09)

sfx *= db(-5.0)
bed = bed_carve.carve(M * db(-13.5) + sfx, vo)
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
