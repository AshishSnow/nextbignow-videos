"""Mix ep 58: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the POWER-CUT study = ONE continuous
'night' room tone (crickets through the wall + the candle's own flutter, which follows the flame's flick() = the sound twin of the ep 58 flame craft) so the loop
tail and the opening share it; the board = dry; the dark curtain room = near silence + a thin line of outdoor birds through the glass; the PARK = birds + far kids."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(58)
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


def _flick(t, seed=1):                     # = anim_props6.flick (on twos, irregular)
    u = math.floor(t * 12 + 1e-6) / 12.0 + seed * 0.37
    v_ = 0.95 + 0.07 * math.sin(u * 7.3) + 0.05 * math.sin(u * 12.9 + 1.1) + 0.03 * math.sin(u * 23.7 + 2.3)
    return v_ - max(0.0, math.sin(u * 0.9 + seed) - 0.93) * 2.2


def candle_flutter(n_, t0=0.0):
    """ep 58: the CANDLE's sound = a soft low 'breathing' rustle (lowpassed noise, 60-500 Hz) whose level follows the flame's flick() frame by frame,
    plus rare tiny wick crackles. Quiet: it is felt more than heard, but it moves with the picture."""
    tt = t0 + np.arange(n_) / SR
    lv = np.array([_flick(x) for x in tt[::480]]); lv = np.interp(np.arange(n_), np.arange(len(lv)) * 480, lv)
    x = _bp(rng.standard_normal(n_), 60, 500) * (0.4 + 0.9 * (lv - 0.78))
    cr = (rng.random(n_) < 0.00004).astype(float); cr = _bp(np.convolve(cr, np.exp(-np.arange(200) / 30), "same"), 1500, 6000) * 0.8
    y = x + cr
    return y / (np.abs(y).max() + 1e-9)


def crickets(n_):
    tt = np.arange(n_) / SR
    gate = ((tt * 16) % 1 < 0.45) * ((tt * 0.9) % 1 < 0.55)
    y = np.sin(2 * np.pi * 4300 * tt) * gate + 0.6 * np.sin(2 * np.pi * 4700 * tt + 1) * ((tt * 13 + 0.3) % 1 < 0.4) * ((tt * 0.7 + 0.4) % 1 < 0.5)
    return _lp(y, 6000)


def birds(n_, density=1.0, seed=0):
    """daytime birds: short FM chirps (2-5 kHz sweeps, 40-120 ms) in little phrases at random times."""
    r_ = np.random.default_rng(580 + seed); y = np.zeros(n_)
    tt0 = 0.0
    while True:
        tt0 += r_.uniform(0.35, 1.4) / density
        if tt0 > n_ / SR - 0.5: break
        for k in range(r_.integers(2, 5)):
            d = r_.uniform(0.04, 0.12); m = int(d * SR); t2 = np.arange(m) / SR
            f0 = r_.uniform(2400, 4200); f1 = f0 * r_.uniform(0.7, 1.5)
            ph = 2 * np.pi * np.cumsum(f0 + (f1 - f0) * t2 / d) / SR
            c = np.sin(ph) * np.sin(np.pi * t2 / d) ** 2 * r_.uniform(0.4, 1.0)
            a = int((tt0 + k * r_.uniform(0.08, 0.16)) * SR)
            if a + m < n_: y[a:a + m] += c
    return y


def blow_out(level=-24):
    """a short breath 'fff' + the flame gutters out (a tiny low flap)."""
    n_ = int(0.45 * SR); t2 = np.arange(n_) / SR
    br = _bp(rng.standard_normal(n_), 700, 5000) * np.sin(np.pi * np.clip(t2 / 0.35, 0, 1)) ** 2
    flap = _lp(rng.standard_normal(n_), 300) * np.exp(-((t2 - 0.25) / 0.05) ** 2) * 1.2
    y = br + flap
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def curtain_rip(level=-20):
    """curtains yanked open on a rail: rings sliding (a fast metallic rattle) + a cloth swoosh."""
    n_ = int(0.5 * SR); t2 = np.arange(n_) / SR
    rings = _bp(rng.standard_normal(n_), 2500, 8000) * (np.sin(2 * np.pi * 38 * t2) > 0.6) * np.exp(-t2 / 0.25)
    cloth = _bp(rng.standard_normal(n_), 300, 2500) * np.sin(np.pi * t2 / t2[-1]) ** 1.5
    y = rings * 0.6 + cloth
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


DARK = ("S1c", "S4")
BOARD = ("S1b", "S2", "S2b", "S5b_", "S6", "S7b")
PARK = ("S5", "S5b")
DAY = ("S4b", "S7", "S9")
def kind_of(sid): return "board" if sid in BOARD else "dark" if sid in DARK else "park" if sid in PARK else "day" if sid in DAY else "night"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"night": "kit", "board": "board", "dark": "kit", "park": "street", "day": "kit"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the night tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
def night_tone(n_):
    x = np.asarray(occlude(crickets(n_) * 0.5, "wall")).reshape(n_, -1)[:, 0] * 1.4 + candle_flutter(n_) * 0.8 + _lp(rng.standard_normal(n_), 900) * 0.12
    return x / (np.abs(x).max() + 1e-9)


LVL = {"night": -38, "board": -52, "dark": -48, "park": -36, "day": -46}
home = night_tone(NS) * db(LVL["night"])
day_tone = (birds(NS, 0.6, 1) * 0.5 + _lp(rng.standard_normal(NS), 1200) * 0.15)
park_tone = birds(NS, 1.6, 2) + np.asarray(far_cheer(-6, NS / SR)).reshape(NS, -1)[:NS, 0] * 0.0 + _bp(rng.standard_normal(NS), 200, 2500) * 0.12
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    if kind == "night": seg = home[a:b].copy()
    elif kind == "park": seg = park_tone[a:b] / (np.abs(park_tone).max() + 1e-9) * db(LVL["park"])
    elif kind in ("day", "dark"): seg = np.asarray(occlude(day_tone[a:b], "glass")).reshape(b - a, -1)[:, 0] / (np.abs(day_tone).max() + 1e-9) * db(LVL[kind]) if kind == "dark" else day_tone[a:b] / (np.abs(day_tone).max() + 1e-9) * db(LVL[kind])
    else: seg = room_tone("board", b - a) * db(LVL[kind])
    seg = np.asarray(seg, np.float32)
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + home[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S10": continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash") and s[0] != "S4b": place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
NX = 930
TRU = T("i1", "ruin") - 0.12; TNO = T("i2", "no.") - 0.12; TSUN = S["S4b"] + 0.12; TGR = T("b3", "growing") - 0.1
BIG = [TNO, TSUN]
# S0 hook (frame 0): a page turn already happening, mom's finger-wag swishes, the candle flutter (in the room tone)
place(page_flip(-26), 0.0, 470)
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-33), 0.3 + 0.45 * j, NX)
place(pop(-24, 900), TRU, 540)
# S0b close-up: a squint creak (tiny), the flame big = the flutter louder here
place(_st(candle_flutter(int(1.6 * SR), S["S0b"]) * db(-30)), S["S0b"], 180)
# S1 mom: finger wag + YES press
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-32), S["S1"] + 0.2 + 0.26 * j, 700)
place(press(-24), T("i2", "yes.") - 0.1, 540)
# S1b BIG: the doctor's 'no' = layered hit + the MYTH stamp
layered_hit(TNO, -24, (110, 55), (300, 2400), 0.35, 1.2); place(press(-19), TNO + 0.25, 830)
# S1c the shut curtain: a low hush, the '?' pops
place(sniff(-34), T("i2", "hiding") - 0.1, 860); place(boing(-28, 300, 0.3), T("i2", "else.") - 0.2, 540)
# S2 ache?: a little sad note; S2b: the pupil 'opens' (iris whir), the focus muscle strains (creak + squeak) and sweats (drips)
place(boing(-29, 220, 0.35), T("a1", "ache?") - 0.1, 540)
place(machine_whir(-32, 0.5), T("a1", "dim") + 0.0, 420)
place(creak(-28), T("a1", "work") - 0.1, 640); place(stretch(-28, 0.8), T("a1", "work"), 640)
for j in range(2): place(plip(-30), T("a1", "work") + 0.4 + 0.35 * j, 600)
# S3 blinks get rarer (soft ticks), DRY = a parched crackle
for j, tb in enumerate([S["S3"] + 0.15, S["S3"] + 0.55]): place(tick(-31), tb, 600)
place(crackle(-28, 0.6), T("a2", "dry") - 0.1, 540)
# S3b eye rub (cloth squeaks), EYE STRAIN shake
for j in range(3): place(squeak(-33), S["S3b"] + 0.1 + 0.18 * j, 470)
# S3c the BLOW-OUT (breath + gutter), smoke hiss, a snore, then morning birds swell in, TEMPORARY ding
place(blow_out(-22), S["S3c"] + 0.05, 160); place(hiss(-36), S["S3c"] + 0.4, 160)
place(snore(-30), S["S3c"] + 0.9, 470)
tr_ = T("a2", "rest.") - 0.1
place(_st(birds(int(1.2 * SR), 2.0, 5) * db(-34)), tr_ + 0.1, 200); place(ding(-25, 1568), tr_, 540)
# S4 back in the dark room: the X on the candle = two pen strikes + a deflate for 'not dim light'
tn_ = T("b1", "not") - 0.1
place(pen_draw(-26, 0.2, seed=8), tn_, 200); place(pen_draw(-26, 0.2, seed=9), tn_ + 0.12, 200); place(deflate(-28), tn_ + 1.0, 650)
# S4b BIG: the curtains are YANKED open: rail rattle + cloth, a layered hit, a warm shimmer as daylight floods in
place(curtain_rip(-19), TSUN - 0.05, 540); layered_hit(TSUN, -23, (100, 50), (400, 3000), 0.4, 1.4); place(shimmer(-30, 1.2), TSUN + 0.05, 540)
# S5 park: footsteps of the run, ball bounces, a kid's cheer; S5b the world blurs (a soft 'wub' down)
for j, tp in enumerate([S["S5"] + 0.31 * k for k in range(int((S["S5b"] - S["S5"]) / 0.31))]): place(footstep(-31), tp, 300 + 140 * (tp - S["S5"]))
for j in range(6): place(boing(-34, 500, 0.12), S["S5"] + 0.35 + 0.35 * j, 500)
place(giggle(-30, 0.5), S["S5"] + 0.6, 860)
place(slowmo_swell(-28, 0.6), T("b2", "nearsighted.") - 0.1, 540)
# S6 the eye tries to stretch (rubber), the sun is drawn (pen), STOP (a clamp), TOO LONG (a long stretch + a low buzzer)
place(stretch(-30, 1.2), S["S6"] + 0.4, 560); place(clip_snap(-24), T("b3", "stop") - 0.1, 860)
place(stretch(-26, 0.7), TGR, 560); place(buzzer(-30), T("b3", "long.") - 0.1, 540)
# S7 the blurry page (a soft wub), S7b CHECKED ding
place(slowmo_swell(-30, 0.5), T("c1", "blurry") - 0.1, 540); place(ding(-25, 1318.5), T("c1", "checked.") - 0.1, 540)
# S8 the send: mom yells (whoosh of the wag), ding
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-33), S["S8"] + 0.3 + 0.3 * j, NX)
place(ding(-25, 2093), T("c2", "Send") + 0.3, 540)
# S9 the logo sting (ends before the seam)
audio_logo(S["S9"] + 0.02, -18)

reverb_returns()

# ---------------- DROP-OUTS before the big hits ----------------
dip = np.ones(NS, np.float32)
for tb in BIG:
    a, b = int((tb - 0.27) * SR), int((tb - 0.01) * SR); r = int(0.04 * SR)
    dip[a:b] = db(-15); dip[a - r:a] = np.linspace(1, db(-15), r); dip[b:b + r] = np.linspace(db(-15), 1, r)
sfx *= db(-2.0) * dip[:, None]; AMB *= dip[:, None]
cut = int((END - 0.8) * SR); sfx[cut:] *= np.linspace(1, 0, NS - cut)[:, None] ** 2     # nothing but room tone crosses the seam
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
m2, _ = sf.read(f"{B}/work/mix.wav"); e0 = np.sqrt(np.mean(m2[:int(0.3 * SR)] ** 2)); e1 = np.sqrt(np.mean(m2[-int(0.3 * SR):] ** 2))
print(f"loop seam: first 0.3 s {20*np.log10(e0+1e-9):.1f} dBFS vs last 0.3 s {20*np.log10(e1+1e-9):.1f} dBFS")
