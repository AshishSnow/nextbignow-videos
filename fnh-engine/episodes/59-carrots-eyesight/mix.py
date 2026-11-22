"""Mix ep 59: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the NIGHT KITCHEN = ONE continuous
room tone (fridge hum + a wall clock + crickets through the wall) so the loop tail and the opening share it; the 1940 NEWSPRINT = an old-film crackle;
the BLITZ night = wind + a far propeller drone (occluded by distance); the board = dry. Craft sound twin: paper_spin() = the SPINNING NEWSPAPER whirr
that speeds the same ease-out as the picture and stops with a thump + a rustle."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(59)
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




def crickets(n_):
    tt = np.arange(n_) / SR
    gate = ((tt * 16) % 1 < 0.45) * ((tt * 0.9) % 1 < 0.55)
    y = np.sin(2 * np.pi * 4300 * tt) * gate + 0.6 * np.sin(2 * np.pi * 4700 * tt + 1) * ((tt * 13 + 0.3) % 1 < 0.4) * ((tt * 0.7 + 0.4) % 1 < 0.5)
    return _lp(y, 6000)


def paper_spin(dur=0.9, turns=4, level=-22):
    """ep 59 craft sound twin: a SPINNING NEWSPAPER. Paper flutter = band noise amplitude-modulated at the rotation rate (2 flaps per turn), the rate
    follows the same cubic ease-out as spin_paper() (fast -> 0), pitch/brightness falls with it; it lands with a paper THUMP + a short rustle."""
    n_ = int((dur + 0.5) * SR); tt = np.arange(n_) / SR
    u = np.clip(tt / dur, 0, 1)
    rate = turns * 3 * (1 - u) ** 2 / dur * 2.0                                 # flaps per second (2 per turn)
    ph = 2 * np.pi * np.cumsum(rate) / SR
    flap = (0.5 + 0.5 * np.cos(ph)) ** 3
    hi = _bp(rng.standard_normal(n_), 1200, 7000); lo = _bp(rng.standard_normal(n_), 250, 1800)
    bright = (1 - u)
    y = (hi * bright + lo * (0.6 + 0.4 * bright)) * flap * (tt < dur) * (0.3 + 0.7 * np.sin(np.pi * np.clip(u * 1.2, 0, 1)) ** 0.5)
    k = int(dur * SR); m = n_ - k; t2 = np.arange(m) / SR
    y[k:] += _lp(rng.standard_normal(m), 400) * np.exp(-t2 / 0.05) * 2.2 + _bp(rng.standard_normal(m), 2000, 6000) * np.exp(-t2 / 0.12) * 0.6
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def film_crackle(n_):
    """old newsreel: sparse dust clicks + a faint 50 Hz-ish projector rumble."""
    tt = np.arange(n_) / SR
    clicks = (rng.random(n_) < 0.0006).astype(float); clicks = _bp(np.convolve(clicks, np.exp(-np.arange(60) / 8), "same"), 1500, 8000)
    return clicks + 0.15 * _lp(rng.standard_normal(n_), 200) + 0.05 * np.sin(2 * np.pi * 48 * tt)


def drone(n_, f0=88):
    """a far propeller-plane drone (two detuned buzzes, slow beating), low-passed by distance."""
    tt = np.arange(n_) / SR
    y = np.sign(np.sin(2 * np.pi * f0 * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * (f0 * 1.03) * tt)) * 0.5
    return _lp(y, 700) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.4 * tt))


def radar_ping(level=-24):
    n_ = int(0.9 * SR); t2 = np.arange(n_) / SR
    y = np.sin(2 * np.pi * 1450 * t2) * np.exp(-t2 / 0.18) + 0.3 * np.sin(2 * np.pi * 2900 * t2) * np.exp(-t2 / 0.08)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


NIGHT = ("S0", "S0b", "S1", "S5", "S7", "S9")
NEWS = ("S1b", "S2b")
BLITZ = ("S2", "S3", "S3b")
def kind_of(sid): return "night" if sid in NIGHT else "news" if sid in NEWS else "blitz" if sid in BLITZ else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"night": "kit", "news": "board", "blitz": "street", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


def home_tone(n_):
    tt = np.arange(n_) / SR
    hum = 0.3 * np.sin(2 * np.pi * 100 * tt) + 0.12 * np.sin(2 * np.pi * 200 * tt)
    tick_ = np.zeros(n_); 
    for k in range(int(n_ / SR) + 1):
        a = int(k * SR)
        if a + 300 < n_: tick_[a:a + 300] += _bp(rng.standard_normal(300), 2000, 6000) * np.exp(-np.arange(300) / 40)
    x = hum + tick_ * 0.6 + np.asarray(occlude(crickets(n_) * 0.5, "wall")).reshape(n_, -1)[:, 0] * 1.2 + _lp(rng.standard_normal(n_), 900) * 0.1
    return x / (np.abs(x).max() + 1e-9)


LVL = {"night": -38, "news": -44, "blitz": -36, "board": -52}
home = home_tone(NS) * db(LVL["night"])
news_t = film_crackle(NS); news_t = news_t / (np.abs(news_t).max() + 1e-9) * db(LVL["news"])
bl = np.asarray(wind(0, NS / SR)).reshape(-1, 2)[:NS, 0] if False else _lp(rng.standard_normal(NS), 500) * 0.6 + drone(NS) * 0.5
bl = bl / (np.abs(bl).max() + 1e-9) * db(LVL["blitz"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    if kind == "night": seg = home[a:b].copy()
    elif kind == "news": seg = news_t[a:b].copy()
    elif kind == "blitz": seg = bl[a:b].copy()
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
    if s[0] == "S9": continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)


def crunches(t0, t1, x, level=-24, rate=0.36):
    """one carrot CRUNCH each time the munching mouth opens (lib38 munch: open at q = 0.35)."""
    k = math.ceil((t0 / rate) - 0.35)
    while True:
        tc = (k + 0.35) * rate
        if tc >= t1: break
        if tc >= t0: place(crunch(level + rng.uniform(-2, 1)), tc, x)
        k += 1


# ---------------- spotting ----------------
TSEE = T("i1", "see") - 0.12; TCOV = T("i2", "cover-up.") - 0.1; TRAD = T("a2", "radar") - 0.1; TCS = T("a2", "cover") - 0.1
BIG = [TRAD]
# S0 / S0b: carrot crunches (frame 0 already crunching), the beams 'switch on' hum, mom's happy wag
crunches(0.0, S["S1"], 680, -23)
place(machine_whir(-34, 0.6), 0.05, 700); place(boing(-30, 600, 0.25), TSEE, 540)
for j in range(2): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-34), 0.5 + 0.6 * j, 290)
# S1: mom: YES press, 'even in the dark' = a light-switch click
place(press(-25), T("i2", "yes,") - 0.1, 540); place(torch_click(-26), T("i2", "dark.") - 0.15, 540)
# S1b: SPINNING NEWSPAPER #1 + the COVER-UP stamp
place(paper_spin(0.85, 4, -21), S["S1b"] + 0.02, 540); place(press(-21), TCOV, 720)
# S2: the blitz: our plane's prop (near), searchlights hum, the hit on the bomber (a far boom + falling whistle)
place(_st(drone(int((S["S2b"] - S["S2"]) * SR), 120) * db(-30)), S["S2"], 300)
th = T("a1", "shooting") - 0.05
place(thud(-24), th, 900); place(flame_whoosh(-30), th + 0.05, 900)
# S2b: SPINNING NEWSPAPER #2 (the craft moment) + a newsboy-style 'read all about it' rustle
place(paper_spin(0.9, 5, -20), S["S2b"] + 0.02, 540); place(rustle(-30), S["S2b"] + 1.0, 540)
# S3 BIG: the radar box lights = layered hit + radar pings on every sweep
layered_hit(TRAD, -22, (110, 55), (300, 2600), 0.4, 1.3)
for j in range(3): place(radar_ping(-28 - 2 * j), TRAD + 0.25 + 2.09 * j / 3, 540)
# S3b: the spy carrot tiptoes (soft footsteps) + COVER STORY stamp
for j in range(5): place(footstep(-33), S["S3b"] + 0.1 + 0.28 * j, 300 + 50 * j)
place(press(-20), TCS, 600)
# S4 board: the carrot pops on, the arrow (pen), VITAMIN A ding
place(pop(-26, 800), S["S4"] + 0.05, 250); place(ding(-25, 1568), T("b1", "vitamin") - 0.1, 830)
# S4b: vitamin A drops travel (bubbles), the eye lights (shimmer)
place(bubbles(S["S4b"] + 0.2, -30) if False else pop_bubble(-30), S["S4b"] + 0.3, 300)
place(shimmer(-30, 1.0), T("b1", "dim") + 0.1, 760)
# S5: crunching the pile, then the take: no night vision = deflate + a sad boing
crunches(S["S5"], T("b2", "night") - 0.1, 660, -25)
place(deflate(-27), T("b2", "night") - 0.1, 540); place(boing(-29, 220, 0.35), T("b2", "night") + 0.3, 540)
# S5b: two tanks: carrots plop in (dunk), the left fills (pour), HELPS ding, NO CHANGE buzzer
place(dunk(-26), S["S5b"] + 0.5, 300); place(dunk(-27), S["S5b"] + 0.55, 780); place(pour(-30), S["S5b"] + 0.4, 300)
place(ding(-26, 1318.5), S["S5b"] + 1.2, 300); place(buzzer(-31), S["S5b"] + 1.35, 780)
# S6 crunch + blurry (a soft wub), S6b CHECKED ding
crunches(S["S6"], S["S6b"], 330, -26)
place(slowmo_swell(-30, 0.5), T("c1", "blurry,") - 0.1, 540); place(ding(-25, 1318.5), T("c1", "checked.") - 0.1, 540)
# S7 send: mom's wag whooshes + ding
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-33), S["S7"] + 0.3 + 0.3 * j, 290)
place(ding(-25, 2093), T("c2", "Send") + 0.3, 540)
# S8 the logo sting
audio_logo(S["S8"] + 0.02, -18)

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
