"""Mix ep 52: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the dining corner = kit reverb + kit room tone (ONE continuous noise for the loop), the capsule = cap tone, the board = dry. Inside-the-body squeezes use occlude(x, 'body')."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(48)
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



PLACE = {sid: ("board" if sid in ("S2", "S3", "S3b", "S4", "S6", "S7") else ("cap" if sid == "S5" else "kit")) for sid in ORDER}
VERB = {"kit": "kit", "board": "board", "cap": "kit"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the home tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"kit": -42, "board": -52, "cap": -40}
home = room_tone("kit", NS) * db(LVL["kit"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = home[a:b].copy() if kind == "kit" else room_tone(kind, b - a) * db(LVL[kind])
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
TMY = T("i2", "myth.") - 0.1; TSL = T("a1", "slams") - 0.1; TMU = T("a2", "muscle,") - 0.12; TMAT = T("b2", "matter.") - 0.12
BIG = [TMY, TSL, TMU, TMAT]
# S0 hook (frame 0): Chubby GULPS from the steel tumbler (glugs, already going), nani's tut-tut + finger wag
place(glug(-22, 4, 0.5), 0.02, 400); place(click(-24), 0.6, 820); place(click(-24), 0.75, 820)
place(clank(-30, 1800), 1.6, 640)
# S0b close-up: one more gulp, then the '?' pops on 'knees'
place(gulp(-20), S["S0b"] + 0.1, 480); place(boing(-27, 300, 0.3), T("i1", "knees?") - 0.1, 880)
# S1 nani: finger-wag swishes, a palm-on-heart thump on 'swears'
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-32), S["S1"] + 0.15 + 0.25 * j, 400)
place(thud(-26), T("i2", "swears") - 0.1, 500)
# S1b the doctor: x-ray film flap, MYTH stamp (BIG)
place(rustle(-27, 0.3), S["S1b"] + 0.15, 840); place(press(-18), TMY, 540); layered_hit(TMY, -24, (110, 55), (300, 2200), 0.35, 1.2)
# S2 the myth: water falling (pour), SPLASH + crack on the knees (BIG)
place(pour(-27, max(0.4, TSL - T("a1", "falls"))), T("a1", "falls") - 0.1, 540)
place(squirt(-20, 0.35), TSL, 540); place(crunch(-22), TSL + 0.08, 540); layered_hit(TSL, -22, (130, 60), (400, 3000), 0.4, 1.3)
# S3 the slide: a playground slide whee (whoosh down), the X scratch
place(whoosh(1.0, peak=0.4, f_lo=600, f_hi=2600, level=-28), S["S3"] + 0.35, 640)
for j in range(2): place(scratch(-24, 0.18), T("a2", "slide.") + 0.05 + 0.1 * j, 540)
# S3b THE SQUEEZE (BIG on 'muscle'): a wet squeeze + the sip travelling down, heard from inside the body; a plip when it lands
layered_hit(TMU, -26, (100, 50), (300, 2000), 0.35, 1.0)
for j in range(3): place(occlude(squeeze(-18, 0.7), "body"), T("a2", "squeezes") - 0.2 + 0.7 * j, 540)
place(occlude(plip(-16, 700), "body"), T("a2", "wave.") + 0.25, 540)
# S4 three ticks (stand / sit / lie)
for w_, x_ in (("Standing,", 200), ("sitting,", 540), ("lying", 880)): place(ding(-27, 1568), T("a3", w_) + 0.15, x_)
place(shimmer(-29, 0.8), T("a3", "same.") - 0.1, 540)
# S5 the capsule: the hum is the room tone; the water ball wobbles (bubbles), Chubby sips it (slurp)
bubbles(S["S5"] + 0.2, 6, -29); place(sip(-22, 0.4), S["S5"] + 1.7, 470); place(boing_up(-27, 320, 0.35), T("a3", "no") - 0.1, 540)
# S6 the gut: a drop plops into the gut, the X scratch on 'never', soaking into blood = a soft fizz
place(plip(-22, 600), S["S6"] + 0.75, 540)
for j in range(2): place(scratch(-25, 0.16), T("b1", "never") + 0.35 + 0.1 * j, 540)
place(fizz(-30, 1.2), T("b1", "soaks") - 0.1, 660)
# S7 the knee: fluid hatches in (shimmer), drops arrive (plips)
place(shimmer(-28, 0.7), T("b2", "fluid") - 0.1, 540)
for j in range(3): place(plip(-28, 900 + 150 * j), T("b2", "made") + 0.2 + 0.3 * j, 300)
# S7b BIG 'doesn't matter': both gulp, two dings
place(glug(-26, 3, 0.4), S["S7b"] + 0.05, 290); place(glug(-27, 2, 0.45), S["S7b"] + 0.3, 790)
place(ding(-24, 2093), TMAT, 290); place(ding(-24, 2349), TMAT + 0.1, 790); layered_hit(TMAT, -27, (100, 50), (300, 2400), 0.3, 1.2)
# S8 knee ache (a low throb), the doctor ding, NOT GUILTY stamp on the steel glass (a clink)
for j in range(3): place(thud(-30), S["S8"] + 0.2 + 0.4 * j, 440)
place(ding(-25, 1568), T("c1", "doctor.") - 0.1, 540)
place(clink(0.0, -26, 3000) if False else clank(-27, 2200), T("c1", "glass.") - 0.1, 760); place(press(-21), T("c1", "glass.") + 0.05, 760)
# S9 the send: ding; nani's SIT DOWN (a shout-like buzz)
place(ding(-24, 2093), T("c2", "Send") + 0.3, 540); place(buzzer(-30, 0.25), T("c2", "sit") - 0.1, 790)
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
