"""Mix: narrator VO + ducked/carved swing score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 17, also added to sfx_lib): crunch (a candy bite: two crisp noise bursts with a low knock), fizz (sour sweet: hissy
crackle with random pops), nibble (tiny bug munching: fast soft clicks), tooth_crack (a dry snap + splintering creak), wash (saliva
wave: filtered noise swell with a wet gurgle), scrub (toothbrush: rhythmic bristle noise), squeak (a clean tooth squeak: rising
sine chirp); reused doorbell/pop/ding/thud/boom/whoosh/boing/buzzer/stamp/tick/gulp/plip/clang/melt."""
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
TBITE = T("i1", "sugar") - 0.05; TROT = T("i1", "rot") - 0.08
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


def crunch(level=-16):
    t2 = np.arange(int(0.22 * SR)) / SR
    nz = signal.sosfilt(signal.butter(2, [900, 7000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    envl = np.exp(-t2 / 0.03) + 0.7 * np.exp(-((t2 - 0.09) / 0.02) ** 2)
    knock = np.sin(2 * np.pi * 160 * t2) * np.exp(-t2 / 0.03)
    y = nz * envl + 0.6 * knock
    return _st(y / np.abs(y).max() * db(level))


def fizz(level=-24, dur=0.8):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.5
    for k in rng.integers(0, len(t2) - 400, 40): y[k:k + 300] += np.sin(2 * np.pi * rng.uniform(1500, 4000) * t2[:300]) * np.exp(-t2[:300] / 0.004) * 1.5
    return _st(y / np.abs(y).max() * db(level), 90)


def nibble(level=-26, dur=0.5, rate=14):
    t2 = np.arange(int(dur * SR)) / SR
    y = np.zeros(len(t2))
    for k in range(int(dur * rate)):
        i = int(k / rate * SR); seg = t2[: int(0.02 * SR)]
        y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [1200, 5000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.004)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 70)


def tooth_crack(level=-14):
    t2 = np.arange(int(0.6 * SR)) / SR
    sn = signal.sosfilt(signal.butter(2, [1800, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.012)
    cr = signal.sosfilt(signal.butter(2, [300, 2500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.5 + 0.5 * signal.square(2 * np.pi * 38 * t2)) * np.exp(-t2 / 0.18)
    y = sn * 2 + cr * 0.8 + np.sin(2 * np.pi * 90 * t2) * np.exp(-t2 / 0.05)
    return _st(y / np.abs(y).max() * db(level))


def wash(level=-22, dur=1.0):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [300, 3000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    y += 0.5 * np.sin(2 * np.pi * np.cumsum(180 + 60 * np.sin(2 * np.pi * 7 * t2)) / SR) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 2
    return _st(y / np.abs(y).max() * db(level), 150)


def scrub(level=-26, dur=1.2, rate=5.5):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.25 + 0.75 * np.abs(np.sin(np.pi * rate * t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.4
    return _st(y / np.abs(y).max() * db(level), 60)


def squeak(level=-22):
    t2 = np.arange(int(0.3 * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(1800 + 1400 * t2 / 0.3) / SR) * np.sin(np.pi * np.clip(t2 / 0.3, 0, 1)) ** 0.6
    return _st(y / np.abs(y).max() * db(level))


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k == "iris": add(whoosh(0.45, peak=0.6, f_lo=400, f_hi=6000, level=-25), st - 0.05); add(pop(-24, 1600), st + 0.3)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * (i % 8)), st + 0.02); add(thud(-21), st + 0.02)
# hook
add(doorbell(-24), 0.0); add(crinkle(-28, 0.3), TBITE - 0.3); add(crunch(-16), TBITE); add(crunch(-19), TBITE + 0.38)
for j in range(4): add(plip(-28, 700 + 80 * j), TBITE + 0.15 + 0.12 * j)
add(tooth_crack(-13), TROT); add(boom(-19, 0.4), TROT); add(buzzer(-26, 0.3), TROT + 0.3)
for j in range(3): add(pop(-23, 600 + 150 * j), S["S1"] + 0.1 + 0.18 * j)
add(plip(-24, 500), S["S1"] + 0.6)
for j in range(3): add(pop(-24, 900 + 200 * j), S["S1b"] + 0.15 + 0.12 * j)
add(nibble(-27, 0.6, 12), S["S1b"] + 0.6)
add(creak(-26, 0.6), S["S2"] + 0.2); add(ding(-24, 2093), T("i3", "kindest") - 0.1); add(boing(-24, 180), T("i3", "worst.") - 0.15)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(pop(-23, 1200), S["S3"] + 0.2)
add(squelch(-26, 1.2), T("a1", "film") - 0.1); stamp(T("a1", "plaque.") - 0.15, -18)
for j in range(5): add(nibble(-29, 0.4, 16), S["S4"] + 0.2 + 0.5 * j)
add(boom(-21, 0.3), T("a2", "city") - 0.1)
for j in range(4): add(clang(-23, 1400, 0.3), S["S5"] + 0.3 + 0.62 * j); add(boing(-27, 300, 0.3), S["S5"] + 0.33 + 0.62 * j)
add(thud(-20), S["S5b"] + 0.4); add(boing(-22, 220, 0.5), S["S5b"] + 0.42); sparkle_sfx(T("a3", "love") - 0.05, -22); add(ding(-22, 1568), T("a3", "love") - 0.1)
add(crunch(-19), S["S6"] + 0.3); add(crunch(-20), S["S6"] + 1.0)
for j in range(6): add(plip(-29, 800 + 60 * j), S["S6"] + 0.5 + 0.12 * j)
add(nibble(-24, 0.9, 14), T("a4", "leftovers.") - 0.1)
for j in range(3): add(squirt(-24, 0.3), T("a4", "acid.") - 0.15 + 0.1 * j); add(plip(-22, 400), T("a4", "acid.") + 0.3 + 0.1 * j)
add(boom(-18, 0.45), T("a4", "acid.") - 0.15); add(fizz(-26, 1.0), T("a4", "acid.") + 0.4)
add(fizz(-25, 1.6), S["S7"] + 0.2)
for j in range(6): add(pop(-27, 1500 + 100 * j), T("a5", "minerals") - 0.1 + 0.15 * j)
add(squeak(-24), S["S7b"] + 0.3); sparkle_sfx(S["S7b"] + 0.35, -25); add(pop(-24, 1000), T("a5", "shell") - 0.1)
for j in range(8): add(tick(-28), S["S8"] + 0.2 + 0.2 * j)
add(tooth_crack(-12), T("a6", "breaks.") - 0.1); add(boom(-17, 0.5), T("a6", "breaks.") - 0.1)
add(boom(-19, 0.4), T("a6", "cavity.") - 0.15); add(buzzer(-25, 0.4), T("a6", "cavity.") - 0.1)
# rescue
add(rec_scratch(-22), T("b1", "wait.") - 0.25); add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=4000, level=-24), T("b1", "rescue") - 0.3)
add(chaching(-22), T("b1", "rescue") - 0.1); sparkle_sfx(T("b1", "rescue"), -23)
add(whoosh(0.5, peak=0.9, f_lo=2500, f_hi=300, level=-25), S["S10"] + 0.1); add(thud(-18), S["S10"] + 0.55); add(boing(-22, 200, 0.5), S["S10"] + 0.56)
add(pop(-24, 1300), S["S10"] + 0.7); add(pop(-23, 700), T("b2", "No,") - 0.1)
add(wash(-20, 1.4), T("b3", "washes") - 0.1); add(ding(-24, 2093), T("b3", "washes") + 0.5)
for j in range(6): add(plip(-27, 1100 + 100 * j), S["S11b"] + 0.1 + 0.18 * j)
add(squeak(-26), T("b3", "back") - 0.05)
for j in range(5): add(click(-30), T("b4", "patch") - 0.1 + 0.15 * j)
sparkle_sfx(T("b4", "patch") + 0.9, -22); add(ding(-22, 2093), T("b4", "patch") + 0.9)
add(whoosh(0.35, level=-27, f_lo=700, f_hi=5000), S["S12b"] + 0.05); add(pop(-24, 900), T("b4", "fluoride") - 0.1)
add(ding(-23, 1568), T("b5", "heal.") - 0.15); add(buzzer(-24, 0.35), T("b5", "can't.") - 0.15)
# part 2: timer
add(boom(-19, 0.35), S["S14"] + 0.02); card_in(S["S14"] + 0.1, -26); add(crt_off(-30, 0.4), S["S14"] + 0.02)
stamp(S["S14b"] + 0.02, -15); add(clang(-24, 900, 0.5), S["S14b"] + 0.05)
for j in range(int((S["S19"] - S["S15"]) / 0.5)): add(tick(-30), S["S15"] + 0.3 + 0.5 * j)
add(pop(-22, 1000), T("c2", "thirty") - 0.15); add(pop(-22, 1200), T("c2", "sixty") - 0.1)
add(crunch(-22), S["S16"] + 0.05); add(ding(-25, 1318.5), S["S16"] + 0.5)
for j in range(3): add(crunch(-24), S["S17"] + 0.1 * j)
add(boing(-22, 260, 0.5), T("c4", "Still") - 0.1); add(pop(-22, 800), T("c4", "Still") - 0.05)
for j in range(6): add(pop(-25, 900 + 60 * j), S["S18"] + 0.2 + 0.35 * j); add(fizz(-30, 0.5), S["S18"] + 0.25 + 0.35 * j)
add(fizz(-24, 2.0), S["S18b"] + 0.2); add(thud(-16), T("c5", "No") - 0.1); add(buzzer(-23, 0.4), T("c5", "No") - 0.05)
add(whoosh(0.35, level=-26, f_lo=600, f_hi=4800), S["S19"] + 0.05); stamp(T("c6", "much") + 0.15, -17); add(buzzer(-26, 0.25), T("c6", "much") - 0.1)
add(boom(-18, 0.45), T("c6", "often.") - 0.15); sparkle_sfx(T("c6", "often.") - 0.1, -22)
add(pop(-24, 900), S["S19b"] + 0.2); add(pop(-24, 1100), S["S19b"] + 0.5)
# part 3: ranking
add(boom(-19, 0.35), S["S20"] + 0.02); card_in(S["S20"] + 0.1, -26)
for j in range(3): add(whoosh(0.45, peak=0.4, f_lo=500, f_hi=3500, level=-26), T("d1", "ranking.") - 0.15 + 0.15 * j); add(rustle(-26, 0.3), T("d1", "ranking.") - 0.1 + 0.15 * j)
add(stretch(-22, 0.9, True), T("d2", "stick") - 0.1); add(squelch(-25, 0.6), T("d2", "stick") + 0.3); stamp(T("d2", "stick") + 0.05, -19)
add(nibble(-23, 1.2, 15), S["S21b"] + 0.2); add(tick(-28), S["S21b"] + 0.3); add(tick(-28), S["S21b"] + 0.8)
add(fizz(-20, 1.2), T("d3", "own") - 0.1); add(boing(-24, 300, 0.3), T("d3", "own") - 0.05)
add(melt(-24, 0.9), T("d4", "melts") - 0.1); add(wash(-22, 1.2), T("d4", "washes") - 0.1); add(ding(-25, 2093), T("d4", "washes") + 0.4)
add(ding(-21, 1568), S["S23b"] + 0.3); add(pop(-20, 1300), T("d4", "Told") - 0.1); sparkle_sfx(T("d4", "Told") - 0.05, -23)
# part 4: plan
add(boom(-19, 0.35), S["S24"] + 0.02); card_in(S["S24"] + 0.1, -26); add(crinkle(-27, 0.4), S["S24"] + 0.4)
add(clack(-26, 1900), S["S25"] + 0.1)
for j in range(3): add(pop(-25, 800 + 100 * j), T("e2", "one") - 0.1 + 0.1 * j)
add(ding(-24, 1318.5), T("e2", "meal,") - 0.1); add(pop(-24, 1000), T("e2", "saliva.") - 0.2)
add(gulp(-20), S["S25b"] + 0.5); add(gulp(-22), S["S25b"] + 0.9); clink(S["S25b"] + 0.05, -26)
add(fizz(-28, 0.5), S["S26"] + 0.05); stamp(T("e3", "wait") - 0.1, -18)
for j in range(8): add(tick(-28), T("e3", "wait") + 0.2 * j)
add(squelch(-28, 0.8), S["S26b"] + 0.2); add(buzzer(-25, 0.3), T("e3", "scrub") - 0.1); add(rattle(-28, 0.4), T("e3", "scrub") - 0.05)
add(scrub(-24, 1.6, 5.5), S["S27"] + 0.1); add(scrub(-26, 1.4, 5.5), S["S27"] + 1.8); add(ding(-24, 1568), T("e4", "twice") - 0.1)
add(pop(-24, 700), T("e4", "hurts,") - 0.1); add(pop(-24, 600), T("e4", "patch,") - 0.1); stamp(T("e4", "dentist.") - 0.15, -18); add(ding(-22, 2093), T("e4", "dentist.") - 0.1)
for j, w in enumerate(("bacteria", "acid,", "spit", "often")): add(pop(-21, 900 + 150 * j), T("f1", w) - 0.15)
add(pop(-21, 900), S["S29"] + 0.05)
add(pop(-18, 1300), T("f2", "Send") + 0.3); add(ding(-22, 2093), T("f2", "Send") + 0.32)
vend = LINES["f2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2); add(squeak(-26), vend + 0.5)
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
