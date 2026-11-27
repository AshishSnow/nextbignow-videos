"""Mix ep 71: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
NEW CRAFT (ep 71) = MATCH ON ACTION in sound: the lift's whoosh + the gulp run straight ACROSS the cut (one sound, two shots), so the ear stitches the
wide and the close-up together; same for the friend's chug. Split edits kept (J-cut into story places, L-cut out to the board).
Places: the KITCHEN worktop = room_tone('kit') + a fridge hum + birds outside; the 1970 SHOP = room_tone('shop') + a far till; the PARK = 'street' + a far
crowd cheering the runners; the BOARD = dry pen + eraser. Big hits: COLD?, NOPE, JUST AS OFTEN, SOLD OUT, HALF, SHIELD, the last sneeze."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(71)
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

KIT = ("S0", "S0b", "S3", "S7", "S8", "S8b", "S9", "S10")
SHOP = ("S4", "S4b")
PARK = ("S6",)
def kind_of(sid): return "kit" if sid in KIT else "shop" if sid in SHOP else "park" if sid in PARK else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"kit": "kit", "shop": "shop", "park": "street", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ambience with SPLIT EDITS ----------------
kit_bed = (room_tone("kit", NS) * db(-46)).astype(np.float32)
fh = fridge_hum(-50, END + 0.5); fh = np.asarray(fh, np.float32); fh = (fh.mean(1) if fh.ndim == 2 else fh)[:NS]; kit_bed[:len(fh)] += fh
shop_bed = (room_tone("shop", NS) * db(-44)).astype(np.float32)
park_bed = (room_tone("street", NS) * db(-46)).astype(np.float32)
cr = crowd(-40, END + 0.5, 0.6); cr = np.asarray(cr, np.float32); cr = (cr.mean(1) if cr.ndim == 2 else cr)[:NS]; park_bed[:len(cr)] += cr
board_bed = (room_tone("board", NS) * db(-54)).astype(np.float32)
TL = [(S[sid], PLACE[sid]) for sid in ORDER]
amb, WTS = split_edit({"kit": kit_bed, "shop": shop_bed, "park": park_bed, "board": board_bed}, TL, NS, story=("kit", "shop", "park"), lead=0.45, tail=0.4)
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + kit_bed[:LOOPN] * np.linspace(0, 1, LOOPN)
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
LIFT_T0, LIFT_D = 1.56, 0.78; LIFT2_T0, LIFT2_D = 42.12, 0.8
TCOLD = T("i1", "cold?") - 0.1; TNOPE = T("i2", "Nope.") - 0.1; TJUST = T("a1", "just") - 0.1; TCRAZY = T("a3", "crazy") - 0.1
THALF = T("a5", "half.") - 0.05; TSH = T("c1", "shield.") - 0.1; TSN = T("c2", "sneeze!") - 0.05
BIG = [TCOLD, TNOPE, TCRAZY, THALF, TSN]
# S0: the inhale + SNEEZE at 0.55, a sniffle, a tissue; then the MATCH-ON-ACTION lift: ONE whoosh spans the cut, the gulps land in the close-up
place(stretch(-30, 0.4, True), 0.12, 540); place(sneeze(-19), 0.55, 560); layered_hit(0.56, -28, (80, 40), (220, 1800), 0.3, 0.8)
place(sniffle(-27, 0.35), 1.1, 540)
place(whoosh(LIFT_D * 0.9, peak=0.45, f_lo=300, f_hi=2400, level=-29), LIFT_T0, 620)
place(gulp(-22), LIFT_T0 + LIFT_D + 0.02, 560); place(gulp(-24), LIFT_T0 + LIFT_D + 0.52, 560)
layered_hit(TCOLD, -26, (90, 45), (250, 2000), 0.35, 0.9)
# S1: the shield clanks into place, the virus hop (boing_up), the shield cracks on NOPE
place(clank(-28, 520), S["S1"] + 0.25, 600)
place(boing_up(-26, 240, 0.45), TNOPE - 0.05, 700); layered_hit(TNOPE, -22, (100, 50), (300, 2400), 0.45, 1.1)
place(ice_crack(-28, 0.4), TNOPE + 0.25, 600)
# S1b: seven tablets click into the week, the virus pops in on 'catching'
for j in range(7): place(click(-27 + (j % 2)), S["S1b"] + 0.1 + 0.2 * j, 150 + 130 * j)
place(pop(-24, 600), T("i2", "catching") - 0.1, 800); place(giggle(-30, 0.4), T("i2", "catching") + 0.1, 800)
# S2: papers stack (page flips), people pop in (ticks), the count
for j in range(7): place(page_flip(-32), T("a1", "twenty-nine") - 0.1 + 0.1 * j, 290)
for j in range(10): place(tick(-34), T("a1", "eleven") - 0.1 + 0.06 * j, 790)
# S2b: the sick ones sniffle in (pops), the '=' sign = two pen strokes + a hit
for j in range(6): place(pop(-31, 700 + 60 * j), T("a1", "colds") - 0.1 + 0.12 * (j % 3) + 0.3 * (j // 3), 300 + 100 * j)
for j in range(2): place(pen_draw(-27, 0.2, seed=40 + j), TJUST + 0.1 * j, 540)
layered_hit(TJUST, -28, (90, 45), (250, 1800), 0.3, 0.8)
# S3: the double take (whoosh), three question-mark pops
place(whoosh(0.25, level=-31), S["S3"] + 0.1, 540)
for j in range(3): place(pop(-29, 1100 + 150 * j), T("a2", "everyone") - 0.1 + 0.15 * j, 800 + 70 * j)
# S4: PRE-LAP (J) the shop door bell before the 1970 shop; medals clink on 'two-time'; the book whoosh up
prelap(bell(-30, 2349, 0.8, 14), S["S4"], 0.35, 540, where="shop")
for j in range(2): clink(T("a3", "two-time") - 0.1 + 0.28 * j, -27, 3000 + 400 * j)
place(whoosh(0.3, level=-30), T("a3", "book") - 0.2, 760)
# S4b: footsteps rushing in, a crowd 'ooh', books grabbed (soft flops), the till CHA-CHING + SOLD OUT stamp
for j in range(10): place(footstep(-28, 0.8), S["S4b"] + 0.08 + 0.13 * j, 200 + 70 * j)
for j in range(4): place(soft_flop(-28), S["S4b"] + 0.5 + 0.25 * j, 540)
place(chaching(-22), TCRAZY - 0.15, 700); place(press(-22), TCRAZY + 0.1, 540); layered_hit(TCRAZY, -24, (90, 45), (250, 2200), 0.4, 1.0)
# S5: the bar draws in, the circle, the slice drops (whoosh down + soft thud)
place(stretch(-29, 0.5, False), T("a4", "sooner.") - 0.1, 900); place(soft_flop(-25), T("a4", "sooner.") + 0.45, 900)
# S6: the runners' quick footsteps (doubled pace), the crowd cheer swells
for j in range(10): place(footstep(-27, 0.6), S["S6"] + 0.08 + 0.26 * j, 400 + 30 * j)
place(far_cheer(-30, 1.6), T("a5", "marathon") - 0.1, 540)
# S6b: icons pop, then cold wind + chattering teeth on 'freezing cold'
for wd_, x in (("skiers,", 540), ("soldiers", 830)): place(pop(-27, 900), T("a5", wd_) - 0.05, x)
place(wind(-30, 1.2), T("a5", "freezing") - 0.1, 540); place(chatter(-30, 0.8, 15), T("a5", "freezing") + 0.2, 540)
# S6c: the bars grow (rising stretch), the second stops at half (a drop-stress thunk), HALF hit
place(stretch(-29, 0.4, True), S["S6c"] + 0.05, 340); place(stretch(-29, 0.5, True), T("a5", "dropped") - 0.1, 760)
layered_hit(THALF, -23, (100, 50), (300, 2000), 0.4, 1.0); place(ding(-27, 1046.5), THALF + 0.1, 760)
# S7: a juicy bite + munch, juice drops
place(squirt(-26, 0.3), S["S7"] + 0.2, 640); place(munch_sfx(-27, 1.0), S["S7"] + 0.3, 560); place(ding(-28, 1568), T("c1", "good") - 0.05, 540)
# S7b: the tick (pen) on good food, the X slashes on the shield + a buzzer
place(pen_draw(-28, 0.3, seed=81), S["S7b"] + 0.4, 330)
for j in range(2): place(pen_draw(-26, 0.25, seed=82 + j), TSH + 0.12 * j, 760)
place(buzzer(-27, 0.35), TSH + 0.05, 760)
# S8: the friend sneezes, Chubby laughs (giggle), the CHUG: one whoosh across the cut + glugs in the close-up; the last sneeze
place(stretch(-30, 0.3, True), S["S8"] + 0.05, 700); place(sneeze(-21), S["S8"] + 0.35, 700); place(giggle(-27, 0.6), S["S8"] + 0.8, 250)
place(whoosh(LIFT2_D * 0.9, peak=0.45, f_lo=300, f_hi=2400, level=-29), LIFT2_T0, 700)
place(glug(-22, 4, 0.22), LIFT2_T0 + LIFT2_D + 0.02, 560)
place(stretch(-27, 0.3, True), TSN - 0.3, 560); place(sneeze(-18), TSN, 560); layered_hit(TSN + 0.02, -26, (80, 40), (220, 2000), 0.35, 0.9)
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
