"""Mix ep 63: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
NEW CRAFT (ep 63) = SPLIT EDITS: the ambience changes place OFF the picture cut - a J-cut into every story place (the door's winter room tone + wind
leads the cut by 0.45 s; the lab hum too), an L-cut out of a story place into the board (the old room trails 0.4 s under the explanation) - and three
PRE-LAPPED foley (the neighbour's sneeze inhale starts under the board before we see him; the ice clinks before the lab; the tap runs before the basin).
Places: the DOOR = room_tone('winter') + wind through the open door + a far scooter; the LAB = fluorescent buzz ('lineup'); the BOARD = dry pen + eraser.
Big hits: COLD?, NO., the SNEEZE, HALF RIGHT, 29 %, SQUEEZES, HEAD START, CAN'T, the towel."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(63)
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

DOOR = ("S0", "S0b", "S2", "S2b", "S3", "S8", "S8b", "S9", "S10")
LAB = ("S4", "S4b")
def kind_of(sid): return "door" if sid in DOOR else "lab" if sid in LAB else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"door": "winter", "lab": "lineup", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ambience with SPLIT EDITS ----------------
door_bed = room_tone("winter", NS) * db(-43)
wd = wind(-44, END + 0.5); wd = np.asarray(wd, np.float32); wd = (wd.mean(1) if wd.ndim == 2 else wd)[:NS]
door_bed[:len(wd)] += wd
for k_ in range(0, int(END), 7):                                                          # a far scooter passes outside now and then
    sc = whoosh(2.2, peak=0.5, f_lo=120, f_hi=900, level=-46); sc = sc.mean(1); a_ = int((k_ + 3.1) * SR); b_ = min(NS, a_ + len(sc)); door_bed[a_:b_] += sc[:b_ - a_]
lab_bed = (room_tone("lineup", NS) * db(-48)).astype(np.float32)
board_bed = (room_tone("board", NS) * db(-54)).astype(np.float32)
TL = [(S[sid], PLACE[sid]) for sid in ORDER]
amb, WTS = split_edit({"door": door_bed, "lab": lab_bed, "board": board_bed}, TL, NS, story=("door", "lab"), lead=0.45, tail=0.4)
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + door_bed[:LOOPN] * np.linspace(0, 1, LOOPN)
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

# ---------------- spotting ----------------
TCOLD = T("i1", "cold?") - 0.1; TNO = T("i2", "No.") - 0.1; TZ = T("a1", "sneezes,") - 0.1; THALF = T("a2", "half") - 0.1
T29 = T("a4", "twenty-nine") - 0.1; TSQ = T("a5", "squeezes") - 0.1; THEAD = T("a5", "head") - 0.1; TCANT = T("c1", "can't") - 0.1
TTOW = T("c2", "yells,") - 0.1
BIG = [TCOLD, TNO, TZ, THEAD, TCANT]
# S0/S0b: drips plip on the tiles (uneven), teeth chatter, a cold gust through the door, mom's towel flaps
for j, tt in enumerate([0.3, 0.75, 1.32, 1.6, 2.2, 2.9, 3.4]): place(plip(-31 - 2 * (j % 2), 1300 + 180 * (j % 3)), tt, 720 + 60 * ((j % 3) - 1))
place(chatter(-28, 1.2, 14), 0.5, 700); place(chatter(-27, 1.4, 16), S["S0b"] + 0.1, 560)
place(wind(-30, 1.6), 0.6, 900)
for j in range(4): place(whoosh(0.18, peak=0.5, f_lo=500, f_hi=3000, level=-36), 0.4 + 0.29 * j, 260)
layered_hit(TCOLD, -24, (90, 45), (250, 2200), 0.4, 1.0)
# S1: magnifier pops in, a single drop 'plink', NO. hit + stamp
place(pop(-26, 900), S["S1"] + 0.15, 690); place(drip_big(-26), S["S1"] + 0.5, 690)
layered_hit(TNO, -22, (100, 50), (300, 2400), 0.45, 1.1); place(press(-24), TNO + 0.22, 700)
# S1b: equation terms pop on their words; the virus giggles; COLD ding / 'just wet' drip
for wd_, x in (("virus,", 220), ("wet", 220)): place(pop(-27, 1000), T("i2", wd_) - 0.15, x)
place(ding(-29, 1318.5), T("i2", "virus,") + 0.35, 840); place(plip(-28, 1600), T("i2", "wet") + 0.45, 840)
# S2: PRE-LAP (J) the neighbour's inhale under the board, then the SNEEZE (layered) + the spray
prelap(stretch(-29, 0.55, True), S["S2"], 0.5, 860, where="winter")
place(stretch(-28, 0.5, True), TZ - 0.5, 860); place(sneeze(-19), TZ, 860)
layered_hit(TZ + 0.02, -26, (80, 40), (220, 2000), 0.35, 0.9)
for j in range(5): place(plip(-34, 1800 + 200 * j), TZ + 0.25 + 0.09 * j, 600 - 60 * j)
# S2b: a sniffle, the virus hops onto the nose (boing_up)
place(sniffle(-26, 0.35), S["S2b"] + 0.25, 560); place(boing_up(-28, 330, 0.35), T("a1", "nose.") - 0.3, 560)
# S3: mom's take (whoosh), HALF RIGHT ding + towel flap
place(whoosh(0.3, level=-30), S["S3"] + 0.05, 560); place(ding(-26, 1568), THALF, 560); layered_hit(THALF, -28, (90, 45), (250, 1800), 0.3, 0.8)
# S4: PRE-LAP (J) the ice clinking before we see the lab; 2005 pop; feet go in (splash + shiver chatter)
clink(S["S4"] - 0.35, -30, 3400); clink(S["S4"] - 0.18, -32, 2900)
place(pop(-24, 900), T("a3", "two") - 0.1, 540)
place(splash_sfx(-25, 0.7, 3), T("a3", "feet") - 0.05, 380); place(ice_crack(-30, 0.5), T("a3", "ice") - 0.05, 380)
place(chatter(-30, 1.0, 15), T("a3", "water") + 0.1, 380)
# S4b: the timer ticks fast to 20 MIN + a ding; ice bobs
for j in range(8): place(tick(-30), S["S4b"] + 0.1 + 0.14 * j, 830)
place(ding(-27, 2093), S["S4b"] + 1.3, 830); clink(S["S4b"] + 0.5, -33, 3100)
# S5/S5b: people icons 'catch' it (three little sneezes = pops), 29% = count tick roll + hit; 9 = a single soft pop
for j in range(3): place(pop(-28, 600 + 80 * j), T29 + 0.15 * j, 300 + 200 * j)
for j in range(8): place(tick(-33), T29 + 0.1 * j, 540)
layered_hit(T29 + 0.8, -27, (90, 45), (250, 2000), 0.3, 0.8)
place(pop(-29, 700), T("a4", "nine.") - 0.1, 660); place(soft_flop(-28), T("a4", "nine.") + 0.4, 540)
# S6: the vessel squeezes (stretch down + creak), the flow slows (squelch)
place(stretch(-27, 0.5, False), TSQ, 520); place(creak(-30, 0.45), TSQ + 0.05, 520); place(squelch(-31, 0.7), TSQ + 0.4, 520)
# S6b: fighters bump into the pinch (soft pops), a sad deflate
for j in range(3): place(pop(-31, 500 + 60 * j), S["S6b"] + 0.4 + 0.25 * j, 430)
# S6c: the virus wakes (boing up) and grows; HEAD START hit
place(boing_up(-27, 220, 0.5), T("a5", "already") - 0.05, 600); layered_hit(THEAD, -22, (100, 50), (300, 2400), 0.45, 1.1)
# S7: the drop, the red X (two pen slashes), CAN'T hit; S7b recap pops
place(drip_big(-26), S["S7"] + 0.1, 540)
for j in range(2): place(pen_draw(-27, 0.25, seed=70 + j), TCANT + 0.15 * j, 540)
layered_hit(TCANT, -24, (90, 45), (250, 2200), 0.35, 1.0)
for tt in (S["S7b"] + 0.1, T("c1", "might") - 0.1, T("c1", "already") - 0.1): place(pop(-27, 950), tt, 540)
# S8: PRE-LAP (J) the tap running before the basin shot; scrub + foam bubbles
prelap(faucet(-27, 1.6), S["S8"], 0.4, 360, where="winter")
for j in range(5): place(pop_bubble(-33, 1300 + 150 * j), S["S8"] + 0.3 + 0.12 * j, 360)
# S8b: the towel flies (whoosh) and lands (soft flop) on 'yells'; a muffled 'hm!' boing
place(whoosh(0.35, peak=0.6, f_lo=400, f_hi=3000, level=-26), TTOW - 0.25, 600); place(soft_flop(-22), TTOW + 0.05, 720)
layered_hit(TTOW + 0.05, -28, (80, 40), (200, 1600), 0.3, 0.7); place(ding(-27, 2093), T("c2", "first!") - 0.05, 540)
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
