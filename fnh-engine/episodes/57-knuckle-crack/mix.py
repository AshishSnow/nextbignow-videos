"""Mix ep 57: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the study desk at night = kit reverb +
ONE continuous 'study' room tone (laptop fan + a far road through the wall) so the loop tail and the opening share it; the board = dry; the MRI = a hum + knocking."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(57)
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


def knuckle_pop(level=-18, seed=0, size=1.0):
    """ep 57: a KNUCKLE CRACK = cavitation, so it is FAST: a 1-2 ms broadband click (the pocket snapping open), an 8 ms bright 2-6 kHz burst, and a tiny damped
    'knock' of the finger (280-420 Hz, ~20 ms). No lead-in (a snap has no anticipation); every crack varies in pitch + brightness (seed)."""
    r_ = np.random.default_rng(seed + 570); n_ = int(0.09 * SR); t2 = np.arange(n_) / SR
    click = np.zeros(n_); k = int(0.0015 * SR); click[:k] = r_.standard_normal(k) * np.linspace(1, 0, k)
    burst = _bp(r_.standard_normal(n_), 2000 * r_.uniform(0.9, 1.2), 6000) * np.exp(-t2 / (0.006 * size)) * 0.7
    f0 = r_.uniform(280, 420); knock = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / (0.018 * size)) * 0.55
    y = click * 1.2 + burst + knock
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def mri_knock(level=-30, dur=2.0, rate=7.0, f0=1100):
    """ep 57: an MRI scanner = a steady low hum + loud rhythmic knocking bursts (gradient coils), heard in the room."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    hum = np.sin(2 * np.pi * 60 * t2) * 0.25 + _lp(rng.standard_normal(n_), 400) * 0.2
    gate = ((t2 * rate) % 1 < 0.35).astype(float)
    knock = np.sign(np.sin(2 * np.pi * f0 * t2)) * gate * 0.35
    y = hum + _bp(knock, 400, 4000)
    fd = int(0.05 * SR); y[:fd] *= np.linspace(0, 1, fd); y[-fd:] *= np.linspace(1, 0, fd)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def page_flip(level=-28):
    n_ = int(0.12 * SR); t2 = np.arange(n_) / SR
    y = _bp(rng.standard_normal(n_), 1500, 7000) * np.sin(np.pi * t2 / t2[-1]) ** 2
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


BOARD = ("S1b", "S2", "S2b", "S3", "S3b", "S6b")
PLACE = {sid: ("board" if sid in BOARD else ("mri" if sid in ("S4", "S7") else "study")) for sid in ORDER}
VERB = {"study": "kit", "board": "board", "mri": "kit"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the study tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
def study_tone(n_):
    tt = np.arange(n_) / SR
    fan = _bp(rng.standard_normal(n_), 300, 1400) * 0.35 + 0.12 * np.sin(2 * np.pi * 118 * tt)
    road = np.asarray(occlude(_bp(rng.standard_normal(n_), 80, 1500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * tt) ** 4), "wall")).reshape(n_, -1)[:, 0] * 2.0
    x = _lp(rng.standard_normal(n_), 1600) * 0.25 + fan + road
    return x / (np.abs(x).max() + 1e-9)


LVL = {"study": -41, "board": -52, "mri": -44}
home = study_tone(NS) * db(LVL["study"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = home[a:b].copy() if kind == "study" else room_tone("kit" if kind == "mri" else "board", b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + home[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S11": continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
CRACK0 = [-0.05, 0.62, 1.2]; CX, NX = 440, 850     # = anim_shots
TGV = T("i1", "give") - 0.05; TNO = T("i2", "no.") - 0.12; TSN = T("a2", "snaps") - 0.06; TCP = T("a2", "coming") + 0.05; TNT = T("b3", "Not") - 0.1
BIG = [TNO, TSN, TNT]
# S0 hook (frame 0, mid-crack): the cracks of the opening (the first one already ringing at frame 0), nani's yell is a VO-free mouth: a short 'tsk'
for j, tp in enumerate(CRACK0):
    if tp >= 0: place(knuckle_pop(-17 - 2 * j, j), tp, CX + 20)
place(knuckle_pop(-22, 9, 0.6), 0.0, CX + 20)
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-33), 0.3 + 0.45 * j, NX)          # nani's finger wag
# S0b the close-up pull: fabric + skin creak as the wrist leads, then the POP (layered)
place(stretch(-30, 0.5, up=True), S["S0b"] + 0.15, 560); place(knuckle_pop(-15, 3, 1.3), TGV, 560); layered_hit(TGV, -28, (120, 60), (500, 3200), 0.25, 1.4)
# S1 nani: finger wag swishes; YES = a stamp-like press
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-32), S["S1"] + 0.2 + 0.26 * j, 700)
place(press(-24), T("i2", "yes.") - 0.1, 540)
# S1b BIG: the doctor's 'no' = layered hit + the MYTH stamp
layered_hit(TNO, -24, (110, 55), (300, 2400), 0.35, 1.2); place(press(-19), TNO + 0.25, 860)
# S2 'what's that pop?' a tiny pop as the ring is drawn; S2b the fluid sloshes in
place(pop(-26, 1200), T("a1", "pop?") - 0.1, 540)
place(occlude(squelch(-26, 0.6), "body"), T("a1", "slippery") - 0.05, 540)
# S3 the pull: a rubbery stretch, then BIG: the gas pocket SNAPS (knuckle pop + layered hit), heard inside the finger a little
place(stretch(-24, 0.9), S["S3"] + 0.15, 540); place(knuckle_pop(-14, 5, 1.4), TSN, 540); layered_hit(TSN, -24, (130, 60), (600, 3600), 0.35, 1.5)
place(occlude(bubble_pop(-26), "body"), TSN + 0.03, 540)
# S3b the suction cup: rubber creak while it stretches, then the real 'thwock' (suction) on 'coming off'
place(squeak(-28), S["S3b"] + 0.3, 400); place(stretch(-27, 0.6), S["S3b"] + 0.4, 400); place(suction(-15), TCP, 400); place(knuckle_pop(-24, 7), TCP, 400)
# S4 the MRI: hum + knocking, a ping when the dark pocket appears
place(mri_knock(-31, SEND("S4") - S["S4"] - 0.1), S["S4"] + 0.05, 290); place(ding(-25, 1568), T("a3", "happening") - 0.05, 760)
# S5 Chubby tries again: the stretch... nothing (a sad boing down), the timer ticks
place(stretch(-27, 0.6), S["S5"] + 0.25, 560); place(boing(-28, 200, 0.4), T("b1", "won't") + 0.45, 540)
for j in range(5): place(tick(-27), T("b1", "twenty") - 0.1 + 0.2 * j, 540)
# S6 the old doctor cracks his LEFT hand again and again (each one different)
for j in range(5): place(knuckle_pop(-21 - (j % 2) * 2, 20 + j), S["S6"] + 0.4 + 0.7 * j, 470)
# S6b split: cracks on the left (panned left), the calendar pages flipping in the middle, BIG-ish: 50
for j in range(9): place(knuckle_pop(-23, 40 + j), S["S6b"] + 0.2 + 0.45 * j, 270)
tf_ = T("b2", "fifty") - 0.1
for j in range(12):
    tt_ = S["S6b"] + 0.2 + (tf_ + 0.4 - S["S6b"] - 0.2) * math.sqrt(j / 11)
    place(page_flip(-29), tt_, 540)
place(ding(-24, 2093), tf_ + 0.4, 540)
# S7 BIG: the X-ray lightbox clicks on (flicker), two ticks, 'no arthritis' hit
place(torch_click(-22), S["S7"] + 0.05, 540); place(buzz(-34, 0.4, 120), S["S7"] + 0.08, 540)
layered_hit(TNT, -25, (100, 50), (400, 2600), 0.3, 1.2)
place(pen_draw(-27, 0.25, seed=3), TNT + 0.15, 330); place(pen_draw(-27, 0.25, seed=4), TNT + 0.4, 760)
# S8 the swollen knuckle throbs (low pulses), then a soft ding on 'doctor'
for j in range(3): place(_st(_lp(rng.standard_normal(int(0.18 * SR)), 180) * np.hanning(int(0.18 * SR)) * db(-24)), T("c1", "swells") + 0.4 * j, 700)
place(ding(-25, 1318.5), T("c1", "doctor.") - 0.1, 540)
# S9 the send: ding + one last crack
place(ding(-25, 2093), T("c2", "Send") + 0.3, 540); place(knuckle_pop(-18, 60), T("c2", "knuckles"), CX)
# S10 the logo sting (ends before the seam)
audio_logo(S["S10"] + 0.02, -18)

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
