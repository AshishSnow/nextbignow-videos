"""Mix: narrator VO + ducked/carved musette-waltz score + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP).
New foley (ep 15, also added to sfx_lib): snap (a crisp chocolate snap: sharp broadband crack + bright ring), melt (soft gooey
glide: low-passed noise swell sliding down), clack (crystal bricks landing: short hard woody tick), fridge_hum (50 Hz-ish hum +
compressor whine), suction (fridge door seal pop), plus reused pop/ding/thud/boom/whoosh/sparkle/boing/stamp."""
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
TSNAP = 0.85; TMELT = T("i1", "melt...") - 0.05
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
M[: int(LINES["i1"]["end"] * SR)] *= db(-3.5)          # hook line: keep the question clear (VO/bed >= 14 dB)
exec(open(f"{_D}/sfx_lib.py").read())


def snap(level=-14):
    t2 = np.arange(int(0.18 * SR)) / SR
    crack = rng.standard_normal(len(t2)) * np.exp(-t2 / 0.006)
    crack = signal.sosfilt(signal.butter(2, [1800, 12000], "band", fs=SR, output="sos"), crack)
    ring = (np.sin(2 * np.pi * 3100 * t2) + 0.6 * np.sin(2 * np.pi * 4700 * t2)) * np.exp(-t2 / 0.02) * 0.35
    body = np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.015) * 0.5
    y = crack + ring + body
    return _st(y / np.abs(y).max() * db(level))


def melt(level=-24, dur=0.9):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, 700, "low", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    f = 320 * np.exp(-t2 / 0.4) + 90
    y = y * 0.6 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 1.5
    return _st(y / np.abs(y).max() * db(level), 90)


def clack(level=-24, f0=1900):
    t2 = np.arange(int(0.06 * SR)) / SR
    y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.008) + 0.4 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.003)
    return _st(y / np.abs(y).max() * db(level))


def fridge_hum(level=-30, dur=2.0):
    t2 = np.arange(int(dur * SR)) / SR
    y = 0.6 * np.sin(2 * np.pi * 100 * t2) + 0.3 * np.sin(2 * np.pi * 200 * t2) + 0.08 * np.sin(2 * np.pi * 1260 * t2) * (1 + 0.3 * np.sin(2 * np.pi * 3 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 200)


def suction(level=-22):
    t2 = np.arange(int(0.25 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [300, 2500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.05)
    y += np.sin(2 * np.pi * (180 + 600 * t2) * t2) * np.exp(-t2 / 0.06)
    return _st(y / np.abs(y).max() * db(level))


def stamp(t, lv=-15): add(thud(lv), t); add(pop(lv - 6, 500), t + 0.01)


def sparkle_sfx(t, lv=-24): add(ding(lv, 2637), t); add(ding(lv - 3, 3520), t + 0.05); add(ding(lv - 6, 4186), t + 0.1)


# transitions
for i, s in enumerate(SHOTS[1:], 1):
    k = s["trans"]; st = s["start"]
    if k == "whip": add(whoosh(0.4, level=-24), st - 0.22)
    elif k == "focus": add(whoosh(0.4, peak=0.75, f_lo=250, f_hi=2200, level=-27), st - 0.28)
    elif k == "zoom": add(whoosh(0.4, peak=0.7, f_lo=300, f_hi=4500, level=-26), st - 0.25)
    elif k == "iris": add(whoosh(0.45, peak=0.6, f_lo=400, f_hi=6000, level=-25), st - 0.05); add(pop(-24, 1600), st + 0.3)
    elif k in ("punch", "flash"): add(pop(-22, 700 + 60 * (i % 8)), st + 0.02); add(thud(-21), st + 0.02)
# hook
add(snap(-16), TSNAP); add(pop(-24, 1200), 1.45); add(melt(-26, 1.0), TMELT); sparkle_sfx(TMELT + 0.05, -25)
add(whoosh(0.5, peak=0.6, f_lo=400, f_hi=3000, level=-27), T("i1", "temperature") - 0.3)
for j in range(6): add(beep(-32, 900 + 120 * j, 0.04), T("i1", "temperature") + 0.12 * j)
add(snap(-15), T("i2", "snaps.") - 0.1); add(melt(-23, 1.0), T("i2", "melts") - 0.1)
add(boing(-26, 140), T("i3", "white") - 0.1); stamp(T("i3", "It's") - 0.1, -18)
# part 1
add(boom(-19, 0.35), S["S3"] + 0.05); card_in(S["S3"] + 0.1, -26); add(whoosh(0.8, peak=0.7, f_lo=200, f_hi=6000, level=-24), T("a1", "The") - 0.25)
add(pop(-21, 800), T("a1", "cocoa") - 0.1)
add(pop(-20, 600), T("a2", "bean.") - 0.15); add(whoosh(0.3, level=-27), T("a2", "bean.") - 0.1)
sparkle_sfx(T("a2", "strange") - 0.1, -24)
add(wind(-30, 1.0), S["S5"] + 0.1)
for j in range(6): add(clack(-23, 1700 + 120 * j), T("a3", "six") - 0.15 + 0.13 * j)
for j in range(int((S["S6b"] - S["S6"]) / 0.9) + 1):
    for q in range(4): add(clack(-29, 1500 + 200 * q), S["S6"] + 0.9 * j + 0.06 * q)
for j in range(int((S["S7"] - S["S6b"]) * 3)): add(clack(-30, 1800), S["S6b"] + 0.15 + j / 3)
stamp(T("b1", "weak") - 0.1, -16)
for j in range(4): add(melt(-27, 0.6), T("b1", "melt") - 0.1 + 0.1 * j)
add(boing(-25, 160, 0.6), T("b1", "soft") - 0.15)
add(boom(-17, 0.4), T("b2", "winner.") - 0.1); sparkle_sfx(T("b2", "winner.") - 0.05, -22); add(chaching(-22), T("b2", "winner.") + 0.1)
add(ding(-24, 3135), T("b3", "shiny.") - 0.15); add(snap(-13), T("b3", "snaps.") - 0.1)
for j in range(8): add(beep(-31, 700 + 90 * j, 0.04), S["S9b"] + 0.25 + 0.15 * j)
add(ding(-21, 1568), T("b3", "thirty-four") - 0.2); add(melt(-24, 1.0), T("b3", "thirty-four") + 0.1)
add(beep(-28, 1800, 0.08), T("b4", "thirty-seven.") - 0.15); add(pop(-22, 900), T("b4", "warmer.") - 0.15)
for j in range(2): clink(S["S11"] + 0.4 + 0.25 * j, -24, 2500)
add(melt(-21, 1.2), T("b5", "melts") - 0.1); add(pop(-22, 1300), S["S11b"] + 0.1)
# part 2
add(boom(-19, 0.35), S["S12"] + 0.02); card_in(S["S12"] + 0.1, -26); add(sizzle(-32, 1.4), S["S12"] + 0.1)
add(wind(-29, 1.2), T("c2", "cool,") - 0.15)
for j in range(10): add(clack(-28, 1400 + 260 * (j % 5)), S["S13b"] + 0.08 * j)
add(boing(-24, 220), T("c2", "messy") - 0.1)
for j in range(4): add(rustle(-30, 0.25), S["S14"] + 0.2 + 0.5 * j)
stamp(T("c3", "tempering.") - 0.15, -17)
for w in ("melt", "cool", "warm"): add(pop(-21, {"melt": 700, "cool": 500, "warm": 900}[w]), T("c4", w) - 0.15)
for j in range(4): add(melt(-27, 0.6), T("c5", "melts") - 0.1 + 0.1 * j)
sparkle_sfx(S["S16b"] + 0.1, -22); add(chaching(-24), T("c5", "survives.") - 0.2)
for j in range(4): add(ding(-26, 1318.5 + 200 * j), S["S17"] + 0.15 * j)
for j in range(14): add(clack(-30, 1800 + 60 * j), S["S17b"] + 0.15 + 0.25 * j)
add(snap(-20), T("c6", "way.") - 0.1); sparkle_sfx(T("c6", "way.") - 0.05, -24)
# part 3: bloom
add(boom(-19, 0.35), S["S18"] + 0.02); card_in(S["S18"] + 0.1, -26); add(crinkle(-25, 0.5), T("d1", "Halloween") - 0.1)
add(buzzer(-24, 0.3), T("d2", "mould.") + 0.05); stamp(T("d2", "mould.") + 0.2, -17); add(boom(-18, 0.4), T("d2", "bloom.") - 0.15)
add(sizzle(-31, 1.2), T("d3", "warm,") - 0.15)
for j in range(10): add(plip(-29, 700 + 60 * j), T("d3", "rises") - 0.1 + 0.12 * j)
add(whoosh(0.8, peak=0.5, f_lo=1500, f_hi=9000, level=-27), T("d3", "white") - 0.4)
tt = S["S21"] + 0.25
while tt < S["S21b"]: add(rustle(-28, 0.15), tt); tt += 0.6
for j in range(4): add(clack(-26, 1500 + 100 * j), T("d4", "slowly") + 0.25 * j)
add(whoosh(1.0, peak=0.5, f_lo=1200, f_hi=8000, level=-28), S["S21b"] + 0.2)
add(suction(-21), S["S22"] + 0.05); add(fridge_hum(-31, S["S22b"] - S["S22"]), S["S22"] + 0.1)
for j in range(8): add(plip(-29, 1100 + 80 * j), T("d5", "water") - 0.1 + 0.1 * j)
for j in range(10): add(ding(-31, 3000 + 150 * (j % 5)), S["S22b"] + 0.05 * j * 2)
stamp(T("d6", "safe") - 0.15, -17); add(ding(-22, 2093), T("d6", "safe"))
add(crinkle(-28, 0.4), T("d6", "chalky.") - 0.2); add(boing(-28, 180), T("d6", "chalky.") + 0.1)
clink(T("e1", "dry.") - 0.15, -22, 2200); add(buzzer(-24, 0.3), T("e1", "Not") - 0.05)
add(plip(-24, 600), T("e2", "Melt") + 0.3); add(melt(-24, 0.8), T("e2", "Melt") + 0.35)
add(boom(-19, 0.35), T("e2", "cake.") - 0.15); sparkle_sfx(T("e2", "cake.") - 0.1, -22)
add(boing(-26, 300), T("e2", "Nobody") - 0.05)
for j, w in enumerate(("built", "mouth.", "bloom")): add(pop(-21, 900 + 200 * j), T("f1", w) - 0.15)
add(pop(-21, 900), S["S27"] + 0.05)
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
