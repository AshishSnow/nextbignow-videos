"""Mix: narrator VO + ducked/carved ska score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 16, also added to sfx_lib): bubble_pop (a rubbery bubble-gum pop: a thump + a short pitch-down snap), squelch (wet gut
squeeze: band-passed noise with a slow wobble + a low glide), stretch (rubbery creak: a gliding nasal tone with tremolo), growl
(stomach rumble: low filtered noise + 60-90 Hz wobble), spit (a 'ptoo': short air burst + lip pop); reused gulp/pop/ding/thud/boom/
whoosh/boing/buzzer/stamp."""
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
TPOP = T("i1", "gum") - 0.05; TGULP = T("i1", "swallow") + 0.05
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-6)
exec(open(f"{_D}/sfx_lib.py").read())


def bubble_pop(level=-14):
    t2 = np.arange(int(0.25 * SR)) / SR
    thump = np.sin(2 * np.pi * (140 * np.exp(-t2 / 0.05) + 60) * t2) * np.exp(-t2 / 0.05)
    snap_ = np.sin(2 * np.pi * np.cumsum(1400 * np.exp(-t2 / 0.02) + 300) / SR) * np.exp(-t2 / 0.025)
    air = signal.sosfilt(signal.butter(2, [1500, 8000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.01)
    y = thump + 0.7 * snap_ + 0.5 * air
    return _st(y / np.abs(y).max() * db(level))


def squelch(level=-22, dur=0.6):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [200, 1800], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    y *= (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t2)) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    y += 0.6 * np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t2 / 0.3) + 70) / SR) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    return _st(y / np.abs(y).max() * db(level), 120)


def stretch(level=-24, dur=0.7, up=True):
    t2 = np.arange(int(dur * SR)) / SR
    f = (180 + 220 * t2 / dur) if up else (400 - 220 * t2 / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t2)) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    return _st(y / np.abs(y).max() * db(level))


def growl(level=-16, dur=1.2):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, 220, "low", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 2
    y += np.sin(2 * np.pi * np.cumsum(70 + 20 * np.sin(2 * np.pi * 3 * t2)) / SR)
    y *= (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 5 * t2))) * np.minimum(1, np.minimum(t2 / 0.1, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 200)


def spit(level=-18):
    t2 = np.arange(int(0.2 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [800, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.04)
    y[: int(0.01 * SR)] += np.sin(2 * np.pi * 300 * t2[: int(0.01 * SR)]) * 2
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
add(stretch(-33, 1.6, True), 0.0); add(bubble_pop(-18), TPOP); add(gulp(-19), TGULP); add(boing(-24, 160), TGULP + 0.2)
# myth
for j in range(6): add(rustle(-28, 0.15), S["S1"] + 0.4 + 0.45 * j)
add(boom(-19, 0.4), T("i2", "seven") - 0.1); add(buzzer(-23, 0.3), T("i3", "myth.") - 0.05); stamp(T("i3", "myth.") + 0.1, -17)
add(creak(-26, 0.6), S["S2b"] + 0.2); add(whoosh(0.6, peak=0.5, f_lo=200, f_hi=2000, level=-26), T("i3", "six") - 0.4)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(crinkle(-25, 0.4), S["S3"] + 0.4)
for j in range(3): add(pop(-22, 700 + 200 * j), S["S4"] + 0.2 + 0.25 * j)
sparkle_sfx(T("a2", "digests") + 0.2, -23)
add(stretch(-22, 1.0, True), S["S5"] + 0.2); add(stretch(-24, 0.9, False), S["S5"] + 1.4)
add(stretch(-26, 0.8, True), S["S6"] + 0.3)
add(plip(-20, 500), S["S6b"] + 0.7)
bubbles(S["S6b"] + 0.8, 6, -27); stamp(T("a4", "dissolve.") - 0.1, -18)
for j in range(4): add(chop(-26), S["S7"] + 0.3 + 0.28 * j)
add(boing(-18, 200, 0.6), T("a5", "break") - 0.15); stamp(T("a5", "down.") - 0.05, -17)
for j in range(4): add(snip(-24), T("a5", "cut") - 0.1 + 0.25 * j)
add(squelch(-24, 1.2), S["S8"] + 0.2); add(boom(-21, 0.4), T("a6", "one") - 0.15)
# part 2
add(boom(-19, 0.35), S["S9"] + 0.02); card_in(S["S9"] + 0.1, -26); add(thud(-20), T("b1", "stuck") - 0.15)
add(squelch(-20, 1.6), S["S10"] + 0.5); add(whoosh(1.2, peak=0.8, f_lo=150, f_hi=1500, level=-24), S["S11"] - 1.3)
for j in range(4): add(squelch(-25, 0.5), T("b3", "squeezes") - 0.1 + 0.6 * j)
for j in range(3): add(squelch(-25, 0.6), S["S12"] + 0.4 + 0.9 * j)
add(boom(-19, 0.4), T("b4", "peristalsis.") - 0.2); add(squelch(-22, 1.0), S["S12b"] + 0.3)
add(squirt(-22, 0.5), T("b5", "toothpaste") + 0.1)
add(squelch(-18, 2.0), S["S14"] + 0.3); add(whoosh(1.5, peak=0.8, f_lo=100, f_hi=1200, level=-22), S["S14"] + 0.8)
for j in range(6): add(ding(-29, 1046.5 + 100 * j), S["S14b"] + 0.1 + 0.27 * j)
add(pop(-22, 900), T("b6", "ninety") - 0.2)
for j in range(5): add(rustle(-24, 0.25), S["S15"] + 0.3 + 0.52 * j)
add(chaching(-23), T("b7", "housekeeping") - 0.1)
add(squelch(-25, 1.4), S["S15b"] + 0.3)
add(suction(-21), S["S16"] + 0.05); add(fridge_hum(-31, S["S17"] - S["S16"]), S["S16"] + 0.1); sparkle_sfx(S["S16"] + 0.15, -24)
add(growl(-14, 1.3), T("b8", "growls") - 0.15)
# part 3
add(boom(-19, 0.35), S["S17"] + 0.02); card_in(S["S17"] + 0.1, -26)
for j in range(3): add(pop(-23, 900 + 200 * j), S["S17"] + 0.8 + 0.8 * j)
for j, w in enumerate(("Corn", "seeds", "whole")): add(pop(-21, 700 + 250 * j), T("c2", w) - 0.15)
for j in range(16): add(tick(-28), S["S19"] + 0.3 + 0.2 * j)
add(ding(-20, 2093), T("c3", "forty") - 0.2)
add(rustle(-25, 0.2), S["S19b"] + 0.6)
charge(S["S20"] + 0.2, S["S20"] + 1.6, -30); add(boom(-18, 0.4), T("c4", "sixty") - 0.2)
add(boing(-22, 260), T("c4", "forty.") - 0.2); sparkle_sfx(T("c4", "forty.") - 0.1, -22)
# part 4
add(boom(-18, 0.45), S["S21"] + 0.02); card_in(S["S21"] + 0.1, -26)
for j in range(7): add(plip(-25, 600 + 60 * j), S["S22"] + 0.3 + 0.62 * j)
add(squelch(-20, 1.6), T("d3", "clump") - 0.15); add(thud(-15), T("d3", "blocks") - 0.15); add(buzzer(-23, 0.4), T("d3", "blocks"))
add(spit(-16), T("d4", "spit") - 0.05); add(clang(-22, 900, 0.4), T("d4", "bin.") - 0.15); add(ding(-22, 2093), T("d4", "bin.") - 0.1)
for w in ("child", "tummy", "throwing"): add(pop(-22, 800), T("d4", w) - 0.1)
add(ding(-20, 1568), T("d4", "doctor.") - 0.15)
# twist
add(boom(-19, 0.35), S["S25"] + 0.02); add(whoosh(0.8, peak=0.5, f_lo=500, f_hi=4000, level=-25), S["S25"] + 0.4); sparkle_sfx(S["S25"] + 1.2, -24)
add(wind(-30, 2.0), S["S26"] + 0.1); add(pop(-22, 700), T("e2", "birch") - 0.15)
for j in range(10): add(tick(-28), S["S26b"] + 0.3 + 0.1 * j)
add(boom(-17, 0.45), T("e2", "years") - 0.2)
add(pop(-22, 1300), S["S27"] + 0.1); sparkle_sfx(T("e3", "complete") - 0.15, -22)
add(boing(-24, 300), T("e4", "stuck") - 0.15)
for j, w in enumerate(("can't", "moves", "two")): add(pop(-21, 900 + 200 * j), T("f1", w) - 0.15)
add(pop(-21, 900), S["S30"] + 0.05)
add(pop(-18, 1300), T("f2", "Send") + 0.3); add(ding(-22, 2093), T("f2", "Send") + 0.32)
vend = LINES["f2"]["end"] + 0.35
add(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-23), vend - 0.2); add(boom(-18, 0.35), vend + 0.2)
add(stretch(-26, 1.4, True), vend + 0.4)
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
