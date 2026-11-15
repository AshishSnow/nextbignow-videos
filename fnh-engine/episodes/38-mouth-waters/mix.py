"""Mix ep 38: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: THE SWEET SHOP = new 'shop' reverb + room tone (murmur + the glass case's hum; ONE continuous noise so the loop tail and the opening share it),
the worktop + lunch table = 'kit', the board = dry. Craft skill (ep 38): SOUND PERSPECTIVE — the jalebi kadhai frying at the back of the shop is
FAR (persp d 0.85: -10 dB, low-passed to ~3.3 kHz, extra wet), the drool / lick / gulp at Chubby's mouth are NEAR (dry, bright); things that fly
past the camera (the ORDER ticket, the memo, the scissors' entrance) are Doppler fly-bys (pitch up on approach, down as they leave, brightest + driest
at the closest point, pan following the path)."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(36)
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


GULP1 = T("i1", "food") + 0.35
LICK1 = T("i1", "look") - 0.05
PLACE = {}
for sid in ORDER:
    PLACE[sid] = "shop" if sid in ("S0", "S0b", "S1", "S3", "S7", "S8", "S9") else ("kit" if sid in ("S4", "S4b", "S6") else "board")


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return PLACE[sid]


# ---------------- ROOM TONE per place (the shop tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"shop": -40, "kit": -44, "board": -52}
shopt = room_tone("shop", NS) * db(LVL["shop"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = shopt[a:b].copy() if kind == "shop" else room_tone(kind, b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + shopt[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S9": continue                                             # the loop tail enters silently
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
    elif k == "morph": place(shimmer(-30, 0.5), st, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- SOUND PERSPECTIVE: the kadhai frying FAR at the back of the shop (under every shop shot, continuous like the room tone) ----------------
fry = persp(sizzle(-20, END + 1.0)[: int((END + 1.0) * SR)] + crackle(-22, END + 1.0)[: int((END + 1.0) * SR)], 0.85)
fryb = np.zeros(NS, np.float32); fryb[:min(NS, len(fry))] = fry[:NS]
fmask = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    if PLACE[sid] == "shop":
        a, b = int(st * SR), min(NS, int(SEND(sid) * SR)); fmask[a:b] = 1
fmask = np.convolve(fmask, np.ones(int(0.02 * SR)) / int(0.02 * SR), "same").astype(np.float32)
fryb = fryb * fmask * (1 - 0.45 * g)
fryb[-LOOPN:] = fryb[-LOOPN:] * np.linspace(1, 0, LOOPN) + fry[:LOOPN] * np.linspace(0, 1, LOOPN)       # the loop: same frying as frame 0
AMB += np.stack([fryb * 0.9, fryb * 1.0], 1)
BUS["shop"] += (np.stack([fryb, fryb], 1) * db(-12) * 2.0)                     # far = wetter

# ---------------- spotting (NEAR = dry + bright at the mouth) ----------------
BIG = [T("i2", "order") - 0.1, T("a2", "sugar") - 0.12, T("a3", "sweet") - 0.15, T("b2", "tripled") - 0.1]
# S0 hook: a long slurp of drool already going at frame 0, the lick, the gulp
place(slurp(-25, 0.5), 0.05, 420); place(lick(-22), LICK1, 430); place(gulp(-19), GULP1, 420)
place(stretch(-31, 0.8, True), 0.0, 600)                                      # the aroma ribbon hooking the nose
# S1: hand hovers (a soft swish), '0 bites' pop
place(whoosh(0.4, peak=0.6, f_lo=400, f_hi=2500, level=-30), S["S1"] + 0.1, 600)
place(pop(-24, 820), T("i2", "bite") - 0.15, 540)
# S1b BIG 1: the ORDER ticket flies in past the camera (Doppler) and the kitchen bell rings
flyby(whoosh(0.5, peak=0.5, f_lo=500, f_hi=6000, level=-20), T("i2", "order") - 0.45, 0.42, 140, 940, 200, where="board")
place(chef_bell(-17), T("i2", "order") - 0.08, 540); layered_hit(BIG[0], -20, (110, 50), (300, 2200), 0.5, 1.2)
# S2: three triggers (pen ticks), the sniff on 'smell', a think 'pop'
place(pop(-27, 1100), T("a1", "sight") - 0.1, 230); place(sniff(-23), T("a1", "smell") - 0.1, 230); place(pop(-27, 900), T("a1", "thought") - 0.1, 230)
# S2b: the taps squeak open and run
for sg, x in ((-1, 280), (1, 800)): place(squeak(-28), T("a1", "glands") - 0.1 + (0.1 if sg > 0 else 0), x)
place(tap_run(-23, 1.3), T("a1", "open") - 0.05, 300); place(tap_run(-24, 1.3), T("a1", "open"), 780)
# S3: the drool strand stretches; NOT just water = a buzzer-ish scratch
place(stretch(-27, 0.9, False), S["S3"] + 0.1, 560); place(slurp(-26, 0.45), S["S3"] + 0.9, 560)
place(scratch(-24, 0.3), T("a2", "water") + 0.45, 540)
# S3b BIG 2: the cook pops in (fly-by from the right), snip-snip-snip, sugar = sparkle + hit
flyby(whoosh(0.45, peak=0.5, f_lo=500, f_hi=5000, level=-23), T("a2", "enzyme") - 0.35, 0.4, 980, 360, 160, where="board")
for j in range(5): place(snip(-22 - (j % 2)), T("a2", "cuts") - 0.05 + 0.22 * j, 700)
layered_hit(BIG[1], -22, (140, 70), (400, 3000), 0.4, 1.4); place(shimmer(-25, 0.8), BIG[1] + 0.05, 740)
# S4 worktop: tear the roti, chew (near, dry), the timer ticks
place(rip(-26, 0.3), T("a3", "Chew") - 0.1, 600)
place(munch_sfx(-25, 2.0), T("a3", "Chew") + 0.3, 430)
for j in range(6): place(tick(-30), T("a3", "Chew") + 0.1 + 0.4 * j, 830)
# S4b BIG 3: SWEET = a bright ding + sparkle burst
layered_hit(BIG[2], -23, (160, 80), (600, 4000), 0.3, 1.6); place(ding(-21, 1568), BIG[2] + 0.02, 540); place(shimmer(-24, 1.0), BIG[2] + 0.05, 540)
# S5: the memo flies to the stomach (Doppler fly-by left -> right), the stove LIGHTS, acid drips
flyby(whoosh(0.5, peak=0.5, f_lo=400, f_hi=5000, level=-22), T("b1", "memo") - 0.15, 0.48, 120, 700, 170, where="board")
place(rustle(-26, 0.35), T("b1", "memo") + 0.3, 700)
place(gas_light(-19), T("b1", "acid") - 0.4, 560)
for j in range(4): place(plip(-27, 900 + 120 * j), T("b1", "acid") + 0.3 + 0.35 * j, 470 + 40 * j)
# S5b BIG 4: the bar counts up (rising ticks) and lands on 'tripled'
for j in range(9): place(tick(-31 + j * 0.4), T("b2", "half") + 0.1 + j * (max(0.6, T("b2", "tripled") - T("b2", "half")) / 9), 730)
layered_hit(BIG[3], -18, (90, 45), (220, 1800), 0.6, 1.0)
# S6 lunch table: plate, glass, spoon clink onto the table on the rhythm
for j, x in enumerate((540, 820, 280)): place(pop(-27, 600 + 200 * j), T("c1", "setting") - 0.1 + 0.22 * j, x)
for j, (x, f0) in enumerate(((540, 2600), (820, 3300), (280, 3900))): clink(T("c1", "setting") - 0.08 + 0.22 * j, -25, f0)
place(thud(-28), T("c1", "greed") - 0.15, 540)
# S7 shop: the friend's lick + gulp, Chubby's giggle, the send ping
place(lick(-24), T("c2", "staring") - 0.05, 660); place(gulp(-21), T("c2", "now") - 0.1, 660)
place(giggle(-27, 0.5), T("c2", "shop") + 0.2, 230)
place(ding(-24, 2093), T("c2", "Send") + 0.3, 540)
# S8 the logo sting (ends before the seam)
audio_logo(S["S8"] + 0.03, -18)

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
