"""Mix ep 60: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the noon DHABA = ONE
continuous room tone (street + the tandoor crackle) so the loop tail and the opening share it, plus a soft STEAM hiss under the steaming curry
(the craft sound twin); the 1982 LAB = fluorescent buzz in a tiled room; the board = dry. Big hits: NOT GUILTY, ON PURPOSE, the prize."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(60)
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





def steam_hiss(n_, level=-40):
    """the steam's sound twin: soft airy noise (band 2-7 kHz) with slow, uneven swells (like the ribbons rising)."""
    tt = np.arange(n_) / SR
    y = _bp(rng.standard_normal(n_), 2000, 7000) * (0.6 + 0.25 * np.sin(2 * np.pi * 0.37 * tt) + 0.15 * np.sin(2 * np.pi * 0.61 * tt + 1))
    return y / (np.abs(y).max() + 1e-9) * db(level)


DHABA = ("S0", "S0b", "S1", "S1b", "S7b", "S8", "S9", "S10")
LAB = ("S4", "S4b", "S5", "S5b", "S6", "S6b")
def kind_of(sid): return "dhaba" if sid in DHABA else "lab" if sid in LAB else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"dhaba": "street", "lab": "lineup", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


LVL = {"dhaba": -36, "lab": -42, "board": -52}
home = room_tone("street", NS) * db(LVL["dhaba"])
_ck = crackle(-56, NS / SR)[:, 0]; home[:len(_ck)] += _ck[:NS]
hs = steam_hiss(NS, -44); home = home + hs
labt = room_tone("lineup", NS) * db(LVL["lab"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    if kind == "dhaba": seg = home[a:b].copy()
    elif kind == "lab": seg = labt[a:b].copy()
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
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)


def crunches(t0, t1, x, level=-24, rate=0.36):
    k = math.ceil((t0 / rate) - 0.35)
    while True:
        tc = (k + 0.35) * rate
        if tc >= t1: break
        if tc >= t0: place(crunch(level + rng.uniform(-2, 1)), tc, x)
        k += 1


# ---------------- spotting ----------------
TNG = T("i2", "chilli.") - 0.05; TPUR = T("b2", "purpose.") - 0.1; TNOB = T("b3", "Nobel") - 0.1
BIG = [TNG, TPUR, TNOB]
# S0/S0b: chilli crunches from frame 0, the uncle's finger wags (tiny whooshes), a sizzle under the curry
crunches(0.0, S["S1"], 380, -25)
for j in range(4): place(whoosh(0.12, peak=0.5, f_lo=1500, f_hi=5000, level=-36), 0.3 + 0.7 * j, 760)
place(simmer(-36, S["S1"]), 0.0, 560)
place(boing(-30, 500, 0.25), T("i1", "stomach") - 0.12, 540)
# S1 uncle: YES press
place(press(-24), T("i2", "yes.") - 0.1, 540)
# S1b: the lamp clicks on the chilli, NOT GUILTY = gavel + layered hit
place(torch_click(-26), S["S1b"] + 0.05, 540)
layered_hit(TNG, -22, (100, 50), (300, 2400), 0.5, 1.2); place(gavel(-24), TNG + 0.02, 560)
# S2: the germ swims in (squelchy wriggle) and drills (scrub)
tg = T("a1", "germ") - 0.1
place(squelch(-28, 0.9), tg, 200); place(scrub(-30, 0.6, 9), tg + 1.1, 420)
# S2b: pills rattle in, the second sore = a soft thud
place(rattle(-28, 0.8), T("a1", "painkillers") - 0.1, 900); place(thud(-28), T("a1", "painkillers") + 0.9, 760)
# S3: chilli bits plip onto the sore, the sting = a sizzle + buzzer-ish OUCH
for j in range(4): place(plip(-28, 700 + 90 * j), S["S3"] + 0.8 + 0.18 * j, 290)
place(spill_sizzle(-28, 0.8), T("a2", "sting") + 0.1, 290); place(press(-26), T("a2", "sting") + 0.2, 300)
# S3b: chilli bits bounce off healthy lining (boings), NO ULCER ding
for j in range(4): place(boing_up(-32, 300 + 40 * j, 0.25), S["S3b"] + 0.5 + 0.18 * j, 790)
place(ding(-25, 1568), T("a2", "make") + 0.1, 790)
# S4: 1982 lab: STRESS = a buzzer
place(buzzer(-31), T("b1", "stress.") - 0.1, 540)
# S4b: microscope focus clicks + shimmer when the germ is found
for j in range(3): place(knob(-30), S["S4b"] + 0.1 + 0.12 * j, 560)
place(shimmer(-28, 0.9), T("b1", "found") - 0.1, 700)
# S5: the glass is raised (clink), a question 'boing'
place(clink(S["S5"] + 0.2, -28)) if False else place(ding(-32, 2600), S["S5"] + 0.25, 400)
# S5b: the GULP (big), ON PURPOSE = stamp + layered hit
place(drink(-24, 3, 0.22), T("b2", "drank") + 0.05, 360); place(gulp(-22), T("b2", "drank") + 0.5, 360)
layered_hit(TPUR, -22, (90, 45), (250, 2200), 0.5, 1.1); place(press(-22), TPUR + 0.02, 560)
# S6: the stomach growls + an uneasy swell
place(growl(-26, 1.0), T("b3", "later,") + 0.1, 540); place(slowmo_swell(-32, 0.6), T("b3", "inflamed.") - 0.1, 540)
# S6b: the prize: drumroll -> layered hit + far cheer
place(drumroll(-30, 0.5), TNOB - 0.6, 540); layered_hit(TNOB, -20, (110, 55), (300, 2800), 0.6, 1.4); place(crowd(-30, 1.4, 1.0), TNOB + 0.1, 540)
# S7: the board: a heartbeat-ish pulse on the upper belly, the doctor pops in
for j in range(3): place(thud(-36), S["S7"] + 0.9 + 0.55 * j, 330)
place(pop(-24, 900), T("c1", "doctor.") - 0.45, 810); place(ding(-25, 1318.5), T("c1", "doctor.") - 0.15, 810)
# S7b: he crunches the chilli again, the uncle gasps (a sniff)
crunches(S["S7b"], S["S8"], 380, -25); place(sniff(-26), T("c1", "chilli.") - 0.1, 790)
# S8: the katori scrapes across the table + a ding on the send line
place(scrub(-30, 0.7, 6), T("c2", "pushes") - 0.1, 700); place(ding(-25, 2093), T("c2", "Send") + 0.3, 540)
# S9 logo sting
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
