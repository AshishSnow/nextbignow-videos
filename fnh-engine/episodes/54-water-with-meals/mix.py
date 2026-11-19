"""Mix ep 54: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the dining corner = kit reverb + kit room tone (ONE continuous noise for the loop), the capsule = cap tone, the board = dry. Inside-the-body squeezes use occlude(x, 'body')."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(54)
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



def splash_sfx(level=-20, size=1.0, seed=0):
    """ep 54 (liquid FX in sound): a SPLASH = impact (short low thump + a bright noise burst that dies in ~0.15 s) then droplets landing at
    UNEVEN times (random gaps, random pitch, the late ones quieter) - the sound twin of 'every drop has its own speed'."""
    r_ = np.random.default_rng(seed + 54); n_ = int((0.25 + 0.5 * size) * SR); t2 = np.arange(n_) / SR
    y = _bp(r_.standard_normal(n_), 700, 6500) * np.exp(-t2 / (0.05 + 0.05 * size)) * 0.9
    y += np.sin(2 * np.pi * (120 - 60 * t2) * t2) * np.exp(-t2 / 0.06) * 0.6 * size
    for j in range(int(4 + 6 * size)):
        t0_ = r_.uniform(0.06, 0.2 + 0.45 * size); f0 = r_.uniform(900, 2600); i0 = int(t0_ * SR); m = min(n_ - i0, int(0.05 * SR))
        if m <= 0: continue
        tt_ = np.arange(m) / SR
        y[i0:i0 + m] += np.sin(2 * np.pi * (f0 + 1800 * tt_ / 0.05) * tt_) * np.exp(-tt_ / 0.012) * r_.uniform(0.15, 0.45) * (1 - t0_ / (0.8 + size))
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


PLACE = {sid: ("board" if sid in ("S2", "S3", "S3b", "S4", "S5") else "street") for sid in ORDER}
VERB = {"street": "street", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the dhaba tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"street": -40, "board": -52}
home = room_tone("street", NS) * db(LVL["street"])
_ck = crackle(-56, NS / SR)[:, 0]; home[:len(_ck)] += _ck[:NS]                    # the tandoor ticking under the dhaba
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = home[a:b].copy() if kind == "street" else room_tone(kind, b - a) * db(LVL[kind])
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
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
TS0_ = -0.18                      # = anim_shots TS0 (the snatch started before frame 0)
TGR = T("i2", "grabs") - 0.08; TWA = T("a1", "water") - 0.1; TMO = T("b2", "more") - 0.12; TTH = T("c1", "thin") - 0.12
BIG = [TGR, TWA, TMO, TTH]
# S0 hook (frame 0, mid-accident): the snatch whoosh is already ending, water SPLASHES on the table (two splashes, uneven), drips on Chubby
place(whoosh(0.25, peak=0.2, f_lo=900, f_hi=4500, level=-26), 0.0, 700)
place(splash_sfx(-19, 1.0, 1), TS0_ + 0.32, 600); place(splash_sfx(-25, 0.5, 4), TS0_ + 0.52, 470)
for j in range(3): place(plip(-30, 1300 + 200 * j), TS0_ + 0.9 + 0.37 * j + 0.05 * j * j, 330)
place(clank(-31, 1900), 0.35, 820)
# S0b: drip... drip on the close-up, the pour into the thought bubble
for j in range(3): place(plip(-29, 1000 + 180 * j), S["S0b"] + 0.3 + 0.55 * j, 330)
place(pour(-29, 0.9), T("i1", "waters") - 0.1, 730)
# S1 the uncle: finger-wag swishes
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-32), S["S1"] + 0.2 + 0.26 * j, 450)
# S1b BIG the grab: a fast whoosh + glass clank in his hand; '0.5 SEC' stamp; NO WATER (buzzer)
place(whoosh(0.2, peak=0.3, f_lo=1200, f_hi=6000, level=-21), TGR - 0.05, 640); place(clank(-23, 2100), TGR + 0.16, 800)
layered_hit(TGR, -26, (110, 55), (300, 2200), 0.3, 1.2)
place(press(-21), T("i2", "second") - 0.05, 300); place(buzzer(-29, 0.3), T("i2", "sit") - 0.1, 540)
# S2 BIG 'made with WATER': a bright water drop plink + the acid drop
place(plip(-20, 1500), TWA, 330); place(plip(-22, 900), TWA + 0.25, 610); layered_hit(TWA, -27, (100, 50), (500, 3200), 0.35, 1.3)
# S3 food falling in (soft plops), the stream, the stretch (rubbery creak)
for j in range(3): place(occlude(dunk(-24, 0.4), "body"), S["S3"] + 0.7 + 0.25 * j, 540)
place(pour(-28, 1.2), T("b1", "water") - 0.05, 545); place(stretch(-23, 0.7), T("b1", "stretch") - 0.1, 600)
# S3b the sensors: dial ticks, then the bells ring on 'notice'
dial_ticks(S["S3b"] + 0.2, T("b1", "notice.") - 0.15, -29)
for j, x_ in enumerate((260, 540, 820)): place(bell(-27, 1760 + 120 * j, 0.6), T("b1", "notice.") - 0.1 + 0.06 * j, x_)
# S4 the gastrin courier hops along (footsteps), the tap squeaks open, BIG: acid gushes
for tt in np.arange(S["S4"] + 0.15, TMO - 0.2, 0.17): place(footstep(-32, 0.4), tt, 400)
place(squeak(-24), TMO - 0.05, 880); place(tap_run(-23, 1.0), TMO + 0.05, 820); layered_hit(TMO, -26, (100, 48), (300, 2000), 0.35, 1.0)
# S5 water pours in (pitch-down = it's weakening), the alarm bell, the tap again, the tick on 'normal'
place(pour(-27, 1.2), T("b3", "Water") - 0.05, 545); place(bell(-24, 1760, 0.7), T("b3", "alarm,") - 0.12, 190)
place(tap_run(-25, 1.0), T("b3", "more") - 0.05, 900); place(ding(-23, 2093), T("b3", "normal.") - 0.1, 820)
# S6 the doctor sips (a calm sip), BIG 'thin': MYTH stamp; the uncle's jaw drop (a boing down)
place(sip(-24, 0.35), S["S6"] + 0.7, 400); place(press(-19), TTH + 0.3, 870); layered_hit(TTH, -25, (110, 55), (300, 2400), 0.35, 1.2)
place(boing(-29, 260, 0.35), TTH + 0.05, 810)
# S7 the sip: tiny and polite
place(sip(-22, 0.4), S["S7"] + 0.3, 470)
# S7b the chug: glugs from the jug, the belly inflating (stretch up), 'bloated' = a wobbly slosh + deflating sigh
place(glug(-21, 6, 0.28), S["S7b"] + 0.15, 520); place(stretch(-26, 1.2, up=True), S["S7b"] + 0.5, 520)
place(squelch(-24, 0.5), T("c2", "bloated.") - 0.1, 520); place(deflate(-29, 0.6), T("c2", "bloated.") + 0.35, 520)
# S8 the send: ding; the uncle's glass clinks
place(ding(-24, 2093), T("c3", "Send") + 0.3, 540); place(clank(-28, 2300), T("c3", "glass.") - 0.1, 800)
# S8b the POUR (the run's liquid craft): the stream starts, the glass fills (pitch rises), a tiny splash at the start
place(splash_sfx(-30, 0.25, 9), S["S8b"] + 0.45, 360); place(pour(-23, 1.6), S["S8b"] + 0.35, 360)
# S10 the logo sting (ends before the seam)
audio_logo(S["S10"] + 0.03, -18)

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
