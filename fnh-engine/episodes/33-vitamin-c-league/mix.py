"""Mix ep 33: VO + foley PLACED IN THE ROOM -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
CRAFT SKILL (ep 33): PUT THE FOLEY IN THE ROOM (Designing Sound 'Panning reverb returns' 2012; Production Expert 'How to use reverb in drama production' +
'Placing foley sounds in a scene with LiquidSonics Cinematic Rooms'; Krotos 'How to pan spatial audio'):
 - pan each DRY effect to where its source is on screen (equal-power, kept inside +-0.55 so nothing jumps hard left/right on a phone); the VOICE stays centred.
 - send every effect to the reverb of the PLACE it happens in, so all sounds in one place share one room: the board = dry (a quiet paper room), the kitchen =
   a small room (8 ms pre-delay, short 0.35 s tail), the stove = the same kitchen a bit wetter, the STADIUM = outdoors: a slap-back echo off the stands
   (~140 ms + ~260 ms) and a long, darker diffuse tail (1.4 s, low-passed); far=0..1 = more wet, less dry (distance). Reverb returns are wide (decorrelated L/R).
 - keep it subtle ('exaggerated levels call attention to themselves'); the dry layer carries the mix in mono (printed L/R correlation).
Kept from ep 31: layered hits on the 5 biggest moments, room tone per place ducked under the voice, a 0.25 s drop-out before each big hit."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
from scipy.signal import fftconvolve
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(33)
db = lambda x: 10 ** (x / 20)
S = {k: st for k, st, _ in SHOTLIST}
ORDER = [k for k, _, _ in SHOTLIST]
SEND = lambda sid: (SHOTLIST[ORDER.index(sid) + 1][1] if ORDER.index(sid) + 1 < len(SHOTLIST) else END)
v, _ = sf.read(f"{B}/work/vo.wav", dtype="float32")
vo = np.zeros(NS, np.float32); vo[: min(NS, len(v))] = v[:NS]
VO = np.stack([vo, vo], 1)
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
exec(open(f"{_D}/sfx_lib.py").read())
ROWS = [("orange", 0, 0, ("f0", "orange")), ("lemon", 0, 0, ("f0", "lemon")), ("papaya", 0, 0, ("f0", "papaya")),
        ("capsicum", 0, 0, ("f0", "capsicum")), ("guava", 0, 0, ("f0", "guava")), ("chilli", 0, 0, ("f0", "green"))]

# ---------------- the ep 33 skill: place() = pan by screen x + a send to the place's reverb ----------------
PLACE = {}
for sid in ORDER:
    if sid in ("S0", "S0b", "S1b", "S11", "S14", "S14b", "S17b", "S19", "S20"): PLACE[sid] = "kit"
    elif sid in ("S15", "S16", "S16b"): PLACE[sid] = "stove"
    elif sid in ("S2", "S2b", "S3", "S3b", "S4", "S4b", "S5", "S6", "S7", "S8", "S9", "S10", "S13", "S13b"): PLACE[sid] = "stadium"
    else: PLACE[sid] = "board"


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return PLACE[sid]


def ir(kind):
    """a synthetic stereo impulse response per place: early reflections (taps) + a diffuse decaying noise tail; L/R decorrelated."""
    spec = {"kit": dict(pre=0.008, rt=0.35, taps=((0.011, 0.5), (0.019, 0.35), (0.027, 0.25)), lp=6000),
            "stove": dict(pre=0.008, rt=0.45, taps=((0.012, 0.5), (0.021, 0.35), (0.031, 0.25)), lp=5000),
            "stadium": dict(pre=0.03, rt=1.4, taps=((0.14, 0.45), (0.26, 0.28), (0.39, 0.14)), lp=2800)}[kind]
    n_ = int((spec["pre"] + spec["rt"] * 1.2) * SR); out = np.zeros((n_, 2), np.float32)
    tt = np.arange(n_) / SR
    for ch in range(2):
        r = np.random.default_rng(100 + ch + len(kind))
        tail = r.standard_normal(n_) * np.exp(-6.9 * np.maximum(0, tt - spec["pre"]) / spec["rt"]) * (tt >= spec["pre"])
        tail = signal.sosfilt(signal.butter(2, spec["lp"], "low", fs=SR, output="sos"), tail)
        tail = tail / (np.sqrt(np.sum(tail ** 2)) + 1e-9) * 0.6
        for d_, a_ in spec["taps"]:
            k = int((d_ + 0.004 * ch) * SR)
            if k < n_: tail[k] += a_
        out[:, ch] = tail
    return out


WET = {"kit": -13, "stove": -11, "stadium": -10, "board": None}
BUS = {k: np.zeros((NS, 2), np.float32) for k in ("kit", "stove", "stadium")}


def place(x, t, xpos=540, gain=1.0, far=0.0, where=None):
    """add an effect at time t, panned to its on-screen x, sent to the reverb of the place it happens in (far 0..1 = more wet, less dry)."""
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(NS, i + len(x))
    if j <= i: return
    m = x[: j - i].mean(1) if x.ndim == 2 else x[: j - i]
    p = clamp((xpos - 540) / 540, -1, 1) * 0.55                                     # equal-power pan, max +-0.55 of the width
    th = (p + 1) * math.pi / 4
    dry = 1.0 - 0.45 * far
    sfx[i:j, 0] += m * math.cos(th) * math.sqrt(2) * gain * dry
    sfx[i:j, 1] += m * math.sin(th) * math.sqrt(2) * gain * dry
    kind = where or place_at(t)
    if WET.get(kind) is not None: BUS[kind][i:j] += (m * gain * db(WET[kind]) * (1 + 1.5 * far))[:, None]


def _bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def _lp(x, f0): return signal.sosfilt(signal.butter(2, f0, "low", fs=SR, output="sos"), x)


def mono(y): return np.stack([y, y], 1).astype(np.float32)


def whistle_blow(level=-20, dur=0.5):
    """a referee's pea whistle: a ~2.6 kHz tone with a fast warble (the pea) + breath noise."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    fr = 2600 + 120 * np.sin(2 * np.pi * 34 * tt)
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 34 * tt))) + 0.15 * _bp(rng.standard_normal(n_), 2000, 6000)
    y *= np.minimum(1, tt / 0.02) * np.clip((dur - tt) / 0.05, 0, 1)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def crowd(level=-26, dur=2.0, cheer=0.0):
    """a stadium crowd: band-limited murmur; cheer 0..1 swells into a roar."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 300, 3000) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * tt) ** 2)
    if cheer > 0: x = x * (1 + 3 * cheer * np.minimum(1, tt / 0.25) * np.exp(-np.maximum(0, tt - 0.6) / (dur * 0.5)))
    x *= np.minimum(1, tt / 0.1) * np.clip((dur - tt) / 0.3, 0, 1)
    return mono(x / (np.abs(x).max() + 1e-9) * db(level))


def drumroll(level=-24, dur=1.5):
    n_ = int(max(0.3, dur) * SR); tt = np.arange(n_) / SR
    hits = (np.sin(2 * np.pi * 14 * tt) > 0.9).astype(np.float32)
    x = _bp(rng.standard_normal(n_), 200, 5000) * np.convolve(hits, np.exp(-np.arange(400) / 80), "same")
    x *= (0.4 + 0.6 * tt / tt[-1])
    return mono(x / (np.abs(x).max() + 1e-9) * db(level))


def boing_up(level=-22, f0=260, dur=0.4):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = f0 * (1 + 1.6 * tt / dur) * (1 + 0.06 * np.sin(2 * np.pi * 18 * tt))
    return mono(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (dur * 0.7)) * np.minimum(1, tt / 0.004) * db(level))


def mat_land(level=-18):
    n_ = int(0.45 * SR); tt = np.arange(n_) / SR
    y = _lp(rng.standard_normal(n_), 500) * np.exp(-tt / 0.08) * 1.5 + np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.12)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def bar_rattle(level=-24):
    n_ = int(0.6 * SR); tt = np.arange(n_) / SR
    y = sum(np.sin(2 * np.pi * f_ * tt) * a_ for f_, a_ in ((620, 1), (1490, 0.5), (2710, 0.3))) * np.exp(-tt / 0.18) * (0.6 + 0.4 * np.sin(2 * np.pi * 22 * tt))
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def sneeze(level=-20):
    n_ = int(0.6 * SR); tt = np.arange(n_) / SR
    y = _bp(rng.standard_normal(n_), 800, 3000) * np.clip(tt / 0.3, 0, 1) * (tt < 0.32) * 0.3 + _bp(rng.standard_normal(n_), 600, 6000) * np.exp(-np.maximum(0, tt - 0.34) / 0.08) * (tt >= 0.34)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def boil(level=-28, dur=3.0):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; y = np.zeros(n_)
    for k in range(int(dur * 22)):
        p = int(rng.uniform(0, n_ - 2000)); f_ = rng.uniform(300, 900); m_ = np.arange(1500) / SR
        y[p:p + 1500] += np.sin(2 * np.pi * f_ * (1 + 3 * m_) * m_) * np.exp(-m_ / 0.01) * rng.uniform(0.3, 1)
    y += 0.3 * _lp(rng.standard_normal(n_), 1500)
    y *= np.minimum(1, tt / 0.2) * np.clip((dur - tt) / 0.3, 0, 1)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


# ---------------- ROOM TONE per place ----------------
def tone(kind, n_):
    tt = np.arange(n_) / SR; w = rng.standard_normal(n_)
    if kind == "stadium": x = _bp(w, 250, 2500) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.25 * tt)) + 0.2 * _lp(rng.standard_normal(n_), 300)
    elif kind == "stove": x = _lp(w, 1500) * 0.5
    elif kind == "kit": x = _lp(w, 1800) * 0.4 + 0.2 * np.sin(2 * np.pi * 100 * tt)
    else: x = _bp(w, 200, 2500) * 0.3
    return x / (np.abs(x).max() + 1e-9)


LVL = {"stadium": -38, "stove": -42, "kit": -46, "board": -52}
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = tone(kind, b - a) * db(LVL[kind]); fd = min(int(0.02 * SR), (b - a) // 2)
    seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)


def jump_sfx(tj, dur, x0=250, x1=700, lvl=0.0, rattle=False):
    """run-up footsteps, the take-off boing, the whoosh over the bar, the mat landing (panned along the arc)."""
    for k in range(3): place(footstep(-28 + lvl, 0.6), tj - 0.9 + 0.3 * k, x0 - 200 + 70 * k)
    place(boing_up(-23 + lvl), tj + 0.12, x0)
    place(whoosh(dur * 0.8, peak=0.5, f_lo=400, f_hi=3000, level=-26 + lvl), tj + 0.2, (x0 + x1) / 2)
    place(mat_land(-19 + lvl), tj + 0.18 + dur, x1)
    if rattle: place(bar_rattle(-24 + lvl), tj + 0.18 + dur * 0.55, 540, far=0.3)


# ---------------- spotting: one sound per action, placed where it happens ----------------
BIG = [T("i1", "close") - 0.05, T("b2", "Red") - 0.1 + 0.25 + 0.18 + 1.05, T("c0", "clears") - 0.45 + 0.18 + 1.25,
       T("d0", "green") - 0.15 + 0.55 + 0.18 + 1.15, T("e1", "gone") - 0.3]
# S0 hook: shimmer on the crowned orange, the guava flies in from the right, SMACK (BIG 1)
place(shimmer(-28, 1.2), 0.05, 700)
place(whoosh(0.35, peak=0.8, f_lo=500, f_hi=4000, level=-25), T("i1", "close") - 0.3, 950)
layered_hit(BIG[0], -15, (90, 42), (300, 2200), 0.6, 1.2)
place(ding(-22, 2093), BIG[0] + 0.05, 820); place(boing(-22, 300, 0.45), BIG[0] + 0.1, 540)
place(thud(-22), S["S0b"] + 0.55, 760)                                                    # the crown lands
# S1 board: the X, the foods arrive
place(scratch(-27, 0.3), T("i2", "make") + 0.1, 540)
for j in range(4): place(pop(-27, 1000 + 120 * j), T("i2", "food") - 0.3 + 0.1 * j, (150, 930, 140, 940)[j])
# S1b thought bubble + the orange glow
place(pop(-24, 600), S["S1b"] + 0.15, 720); place(shimmer(-27, 1.0), T("i2", "orange") - 0.3, 720)
# STADIUM: a crowd bed far away under each stadium stretch
for a_, b_ in (("S2", "S8"), ("S9", "S10"), ("S13", "S13b")):
    place(crowd(-31, SEND(b_) - S[a_]), S[a_], 540, far=0.6, where="stadium")
place(crowd(-24, 2.0, 0.8), T("i3", "Six") - 0.4, 540, far=0.5, where="stadium")      # the wave
for i in range(6): place(boing(-27, 260 + 40 * i, 0.25), T("i3", "Six") - 0.15 + 0.12 * i, 110 + 136 * i)
place(thud(-20), T("i3", "jump") - 0.15, 540)
place(stretch(-26, 0.6, False), S["S2b"] + 0.15, 540); place(whistle_blow(-21, 0.45), T("i3", "bar") - 0.3, 260)
place(rustle(-26, 0.4), S["S3"] + 0.1, 760)
per = max(0.35, (T("a0", "hundred") - 0.2 - S["S3b"]) / 6)
for j in range(6): place(tick(-26), S["S3b"] + per * j + 0.1, 540)
place(ding(-22, 1568), T("a0", "hundred") - 0.2, 540)
# the jumps
jump_sfx(T("a1", "clears") - 0.35, 1.05, 230, 740)
place(thud(-22), T("a1", "bar") - 0.1, 540); place(whistle_blow(-26, 0.25), T("a1", "bar") - 0.05, 300, far=0.4)
place(squeeze(-25), T("a2", "sour") - 0.2, 300); place(pop(-25, 900), T("a2", "right") - 0.3, 540)
jump_sfx(S["S6"] + 0.02, 1.05, 230, 740, rattle=True)
place(buzzer(-24, 0.35), T("a3", "same") - 0.2, 540)
jump_sfx(S["S7"] + 0.05, 1.05, 230, 740); place(bar_rattle(-26), T("b0", "over") - 0.2, 540)
place(crowd(-28, 1.2, 0.5), T("b0", "Okay") - 0.3, 540, far=0.5, where="stadium")
# S8 the lights go down: a big switch clunk + a creak + a drumroll
place(thud(-17), S["S8"] + 0.02, 540); place(creak(-27, 0.8), S["S8"] + 0.5, 540)
place(drumroll(-28, T("b1", "fruit") - S["S8"] - 0.4), S["S8"] + 0.4, 540, far=0.2)
# S9 capsicum (BIG 2)
place(thud(-16), S["S9"] + 0.02, 540)
jump_sfx(S["S9"] + 0.25, 1.05, 300, 720)
layered_hit(BIG[1], -15, (80, 40), (150, 900), 1.0)
place(crowd(-22, 2.2, 1.0), BIG[1] - 0.1, 540, far=0.5, where="stadium")
place(stretch(-25, 0.5, True), T("b2", "double") - 0.3, 750)
# S10 guava (BIG 3)
for k in range(4): place(footstep(-27, 0.7), S["S10"] + 0.2 + 0.4 * k, 300)
jump_sfx(T("c0", "clears") - 0.45, 1.25, 300, 720)
layered_hit(BIG[2], -14, (75, 38), (150, 800), 1.3)
place(crowd(-21, 2.6, 1.0), BIG[2] - 0.1, 540, far=0.5, where="stadium")
for j in range(4): place(pop(-27, 900 + 100 * j), T("c1", "four") - 0.5 + 0.12 * j, 290)
# S11 the guava on the scale; S11b bar rises
place(thud(-24), S["S11"] + 0.55, 740); place(beep(-26, 2400, 0.08), T("c1", "fifty-five") - 0.2, 740)
place(stretch(-25, 0.6, True), T("c1", "whole") - 0.3, 750)
# S12 buddies fill the jar
nb_t0 = S["S12"] + 0.4; nb_t1 = T("c2", "day")
for j in range(14): place(plip(-29, 700 + 40 * j), nb_t0 + (nb_t1 - nb_t0) * j / 14, 400 + 140 * (j % 3))
place(boing(-24, 400, 0.4), T("c2", "day") - 0.1, 540)
# S13 drumroll -> the chilli (BIG 4)
place(drumroll(-23, S["S13b"] + 0.55 - S["S13"]), S["S13"] + 0.05, 540)
jump_sfx(S["S13b"] + 0.55, 1.15, 300, 720)
layered_hit(BIG[3], -14, (85, 40), (200, 1500), 1.2, 1.2)
place(crowd(-20, 2.6, 1.0), BIG[3] - 0.1, 540, far=0.5, where="stadium")
# S14 the chilli mountain: sweat drip + a gulp; S14b the nibble + steam hisses from his ears
place(drip_big(-24), T("d1", "nobody") + 0.1, 420); place(gulp(-24), T("d1", "chilli", 1) - 0.1, 300)
place(munch_sfx(-24, 0.8), T("d1", "few") - 0.2, 600); place(hiss(-27), T("d1", "few") + 0.4, 240); place(hiss(-27), T("d1", "few") + 0.5, 840)
place(ding(-23, 1760), T("d1", "guava") - 0.2, 750)
# S15-S16b stove: the boil underneath, TWIST, buddies crack in the heat, the clock races, GONE (BIG 5, soft)
place(boil(-30, SEND("S16b") - S["S15"]), S["S15"], 640, where="stove")
place(thud(-19), T("e0", "twist") - 0.2, 540)
place(plip(-26, 600), T("e0", "water") - 0.2, 300)
for j in range(3): place(shell_crack(-26), T("e0", "heat") - 0.2 + 0.08 * (2 * j + 1), 880)
for j in range(int((SEND("S16") - S["S16"]) / 0.18)): place(tick(-31), S["S16"] + 0.2 + 0.18 * j, 880)
for j in range(5): place(pop(-27, 1400 - 120 * j), T("e1", "gone") + 0.06 * j, 200 + 170 * j)
layered_hit(BIG[4], -21, (60, 35), (100, 500), 0.8, 0.6)
# S17 steam + microwave hum + ding; S17b calendar flips
place(hiss(-29), S["S17"] + 0.3, 280); place(micro_hum(-30, 1.2), T("e2", "microwave") - 0.1, 790); place(oven_ding(-26), T("e2", "less") - 0.4, 790)
for j in range(3): place(rustle(-27, 0.25), T("e2", "not") - 0.2 + 0.4 * j, 800)
# S18 leaderboard: a rising ding per row
for j, (kd, _a, _b, (lid, w)) in enumerate(ROWS): place(ding(-26, (1046.5, 1174.7, 1318.5, 1568, 1760, 2093)[j]), T(lid, w) - 0.25, 300)
# S19 bag on the counter; S20 sneeze, phone ping, logo
place(thud(-22), S["S19"] + 0.15, 760); place(rustle(-26, 0.5), S["S19"] + 0.2, 760)
place(sneeze(-21), T("f1", "cold") - 0.6, 760); place(ding(-24, 2093), T("f1", "send") + 0.4, 540)
vend = LINES["f1"]["end"] + 0.35
place(whoosh(0.4, peak=0.8, f_lo=300, f_hi=3000, level=-24), vend - 0.2, 540); audio_logo(vend + 0.25, -17)

# ---------------- reverb returns (one room per place) ----------------
for kind, bus in BUS.items():
    if np.abs(bus).max() < 1e-7: continue
    h = ir(kind); wet = np.zeros_like(bus)
    for ch in range(2): wet[:, ch] = fftconvolve(bus[:, ch], h[:, ch])[:NS]
    sfx += wet.astype(np.float32)
    print(f"reverb {kind}: wet peak {20 * np.log10(np.abs(wet).max() + 1e-9):.1f} dBFS")

# ---------------- DROP-OUTS before the big hits ----------------
dip = np.ones(NS, np.float32)
for tb in BIG:
    a, b = int((tb - 0.27) * SR), int((tb - 0.01) * SR); r = int(0.04 * SR)
    dip[a:b] = db(-15); dip[a - r:a] = np.linspace(1, db(-15), r); dip[b:b + r] = np.linspace(db(-15), 1, r)
sfx *= db(-2.0) * dip[:, None]; AMB *= dip[:, None]
BED = float(os.environ.get('BED', '0'))          # owner 9 Nov: no music bed
bed = bed_carve.carve(sfx + AMB, vo)
mix = VO + bed
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
TGT = -11.0
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I={TGT}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I={TGT}:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
hp = signal.butter(2, 150, "high", fs=SR, output="sos"); vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed.mean(1))
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int(L['start']*SR):int(L['end']*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LINES.items()))
print("mono check: L/R corr", round(float(np.corrcoef(mix[:, 0], mix[:, 1])[0, 1]), 3))
