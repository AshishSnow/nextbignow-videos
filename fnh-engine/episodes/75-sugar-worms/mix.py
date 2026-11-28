"""Mix ep 75: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Sound for the NEW CRAFT (eyeline match + inserts): the POV / insert shots are CLOSE in sound too - their foley is dry, bright and a few dB up (persp d=0),
the wide shot before them is the same kind of sound further away (persp d=0.35), so the cut into his eyes feels like leaning in.
Places: the DINING corner = room_tone('kit') + a ceiling-fan tick; the BACKYARD = room_tone('street') + far birds + the hand-pump creak; the BOARD = dry pen + eraser.
Split edits kept (J-cut into story places, L-cut out to the board). Big hits: WORMS?, NOPE/MYTH, POOP, BARE FEET, NOT ON THE MAP, HIDES."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(75)
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

DIN = ("S0", "S0b", "S0c", "S8", "S8b", "S9", "S10")
YARD = ("S3", "S4", "S4b", "S5", "S5b", "S7", "S7b", "S7c")
INSERTS = ("S0b", "S4b", "S5b", "S7b", "S7c", "S8b")
def kind_of(sid): return "din" if sid in DIN else "yard" if sid in YARD else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"din": "kit", "yard": "street", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


def birds(level=-40, dur=10.0, seed=5):
    """far backyard birds: short chirp groups (sine sweeps 2.6-5 kHz) at uneven times."""
    n = int(dur * SR); y = np.zeros(n, np.float32); r = np.random.default_rng(seed); t_ = 0.2
    while t_ < dur - 0.4:
        f0 = r.uniform(2600, 4200); f1 = f0 * r.uniform(1.1, 1.35)
        for k in range(int(r.integers(2, 4))):
            L = int(r.uniform(0.04, 0.08) * SR)
            fr = np.linspace(f0, f1, L); ph = 2 * np.pi * np.cumsum(fr) / SR
            a = int((t_ + k * 0.11) * SR)
            if a + L < n: y[a:a + L] += (np.sin(ph) * np.hanning(L)).astype(np.float32)
        t_ += r.uniform(0.6, 1.8)
    return y * db(level)


def fan_tick(level=-48, dur=10.0):
    n = int(dur * SR); tt = np.arange(n) / SR
    return ((np.sin(2 * np.pi * 3.1 * tt) ** 8) * rng.normal(0, 1, n) * 0.3).astype(np.float32) * db(level)


# ---------------- ambience with SPLIT EDITS ----------------
din_bed = (room_tone("kit", NS) * db(-46)).astype(np.float32); din_bed += fan_tick(-50, END)[:NS]
yard_bed = (room_tone("street", NS) * db(-47)).astype(np.float32); yard_bed += birds(-41, END, 7)[:NS]
board_bed = (room_tone("board", NS) * db(-54)).astype(np.float32)
TL = [(S[sid], PLACE[sid]) for sid in ORDER]
amb, WTS = split_edit({"din": din_bed, "yard": yard_bed, "board": board_bed}, TL, NS, story=("din", "yard"), lead=0.45, tail=0.4)
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + din_bed[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)
print("split edits:", " ".join(f"{p}@{t:.2f}" for t, p in TL))

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] in ("S9", "S10"): continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)


def near(x, sid):
    """inserts = close + dry + bright; wides = a touch further (sound perspective follows the framing)."""
    return persp(x, 0.0 if sid in INSERTS else 0.35)


# ---------------- spotting ----------------
TW = T("i1", "worms?") - 0.1; TNOPE = T("i2", "Nope.") - 0.05; TMYTH = T("i2", "myth.") - 0.1; TPOOP = T("a1", "poop.") - 0.1
TBARE = T("a4", "bare") - 0.1; TJ = T("a4", "feet.") + 0.25; TMAP = T("a5", "map.") - 0.15; THIDE = T("c2", "hides") - 0.15
BIG = [TNOPE, TMYTH, TPOOP, TBARE, TMAP]
# S0: munching from frame 0, the tin lid clank, the FREEZE take at 0.9
place(near(munch_sfx(-27, 0.9), "S0"), 0.0, 330); place(clank(-30, 900), 0.18, 575)
place(stretch(-28, 0.25, False), 0.82, 330); layered_hit(0.9, -27, (80, 40), (220, 1800), 0.3, 0.8)
# S0b INSERT: the hand rattles a laddoo out of the tin (close + dry)
place(near(rattle(-27, 0.5), "S0b"), S["S0b"] + 0.05, 540); place(near(crinkle(-30, 0.3), "S0b"), S["S0b"] + 0.4, 540)
# S0c: WORMS sneaks in (tiptoe ticks), the hit on worms?
for j in range(5): place(tick(-31), TW + 0.05 + 0.07 * j, 300 + 80 * j)
layered_hit(TW, -25, (90, 45), (250, 2000), 0.35, 0.9)
# S1: NOPE hit, the worm wriggles (squelch), the X + MYTH stamp
layered_hit(TNOPE, -22, (100, 50), (300, 2400), 0.45, 1.1); place(squelch(-31, 0.4), S["S1"] + 0.3, 900)
for j in range(2): place(pen_draw(-26, 0.2, seed=60 + j), TMYTH + 0.1 * j, 800)
place(press(-21), TMYTH + 0.1, 540); layered_hit(TMYTH + 0.1, -26, (90, 45), (250, 2000), 0.3, 0.9)
# S1b: laddoos pop onto the pile (rising pops), '= 0 WORMS' drops
for j in range(15): place(pop(-31, 500 + 40 * j), S["S1b"] + 0.08 * j, 380 + 20 * j)
place(soft_flop(-25), T("i2", "worm.") + 0.6, 540)
# S2: the magnifier swoop (whoosh + ding)
place(whoosh(0.3, level=-30, f_lo=800), T("a1", "eggs,") - 0.4, 700); place(ding(-28, 1568), T("a1", "eggs,") - 0.1, 700)
# S2b: the plop + tiny pops for the eggs, POOP hit
place(soft_flop(-24), TPOOP - 0.12, 780); layered_hit(TPOOP, -25, (80, 40), (200, 1600), 0.3, 0.8)
for j in range(3): place(pop(-30, 1300 + 200 * j), TPOOP + 0.1 + 0.08 * j, 730 + 50 * j)
# S3: the magnifier inset swoops in on 'soil'
place(whoosh(0.3, level=-30, f_lo=600), T("a2", "soil,") - 0.3, 740); place(ding(-29, 1318.5), T("a2", "soil,"), 740)
# S3b: three ticks on the week boxes, wriggling eggs, READY sting
for j in range(3): place(pen_draw(-27, 0.15, seed=70 + j), T("a2", "three") - 0.05 + 0.25 * j, 390 + 150 * j)
place(squelch(-30, 0.5), T("a2", "ready.") - 0.2, 540); place(boing_up(-26, 300, 0.35), T("a2", "ready.") - 0.1, 540)
# S4: digging in mud (far-ish squelches), the look (a soft stretch up); EYELINE cut -> S4b close: egg pops, dry + near
for j in range(4): place(near(squelch(-29, 0.25), "S4"), S["S4"] + 0.05 + 0.22 * j, 480 + 40 * j)
place(stretch(-31, 0.3, True), LOOK_T - 0.1, 540)
for j in range(3): place(near(pop(-26, 1500 + 300 * j), "S4b"), T("a3", "hands,") - 0.1 + 0.15 * j, 330 if j == 0 else 750)
# S4c: an egg hop per ride
for wd, x in (("on", 200), ("veggies,", 540), ("water.", 880)):
    tt = (T("a3", "on", 1) - 0.1) if wd == "on" else T("a3", wd) - 0.15
    place(boing_up(-28, 340, 0.3), tt + 0.1, x)
# S5: hand over the mouth; S5b INSERT: the larva wriggles in the soil (close squelch), BARE FEET hit, the foot jerks up
place(press(-27), T("a4", "mouth.") - 0.3, 600)
place(near(squelch(-27, 0.8), "S5b"), S["S5b"] + 0.1, 300); layered_hit(TBARE, -24, (90, 45), (250, 2000), 0.35, 0.9)
place(near(whoosh(0.2, level=-27, f_lo=500), "S5b"), TJ - 0.02, 560); place(boing_up(-24, 360, 0.3), TJ, 560)
# S6: stations light up (rising dings), the laddoo shuffles in, the X + NOT ON THE MAP hit + buzzer
for j, wd in enumerate(("soil.", "Hands.", "Mouth.")): place(ding(-27, (1046.5, 1318.5, 1568)[j]), T("a5", wd) - 0.1, (215, 540, 865)[j])
for j in range(4): place(footstep(-31, 0.5), T("a5", "Sugar") + 0.12 * j, 540)
place(whoosh(0.15, level=-26, f_lo=600), S["S6b"] + 0.02, 540)
place(buzzer(-27, 0.35), TMAP + 0.05, 540); layered_hit(TMAP, -22, (100, 50), (300, 2200), 0.45, 1.0)
# S7: the hand-pump creak (J pre-lap) + water running + scrubbing; S7b INSERT: water on the spinach (close), eggs tumble; S7c: the chappal slap + a tick
prelap(creak(-28, 0.5), S["S7"], 0.35, 830, where="street")
place(tap_run(-27, SEND("S7") - S["S7"]), S["S7"] + 0.05, 800); place(scrub(-28, 1.4), S["S7"] + 0.3, 520)
place(near(faucet(-25, SEND("S7b") - S["S7b"]), "S7b"), S["S7b"], 540); place(near(splash_sfx(-26, 0.6, 3), "S7b"), S["S7b"] + 0.05, 540)
for j in range(3): place(pop(-30, 900 - 120 * j), S["S7b"] + 0.4 + 0.12 * j, 470 + 70 * j)
place(near(soft_flop(-24), "S7c"), T("c1", "chuppuls") - 0.1, 600); place(ding(-28, 1568), T("c1", "chuppuls") + 0.15, 840)
# S8: Chubby's giggle; S8b INSERT: the tin slides behind her back (scrape) + a clank, hit on 'hides'
place(giggle(-27, 0.6), S["S8"] + 0.5, 320)
place(near(stretch(-27, 0.4, False), "S8b"), THIDE, 900); place(clank(-28, 700), THIDE + 0.42, 980); layered_hit(THIDE + 0.05, -27, (80, 40), (220, 1800), 0.3, 0.8)
place(giggle(-26, 0.8), THIDE + 0.5, 180)
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
