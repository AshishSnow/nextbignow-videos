"""Mix ep 35: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: THE RING = 'stadium' reverb (big arena, slap-back) + a new 'arena' room tone (crowd murmur, ONE continuous noise so the loop tail
and the opening share it); the worktop = 'kit'; the board = dry. Craft skill (ep 35, SECONDARY ACTION) on the audio side: the small supporting sounds
(glove taps, the rope creak after a hit, the cuffed seed's rattle) sit 8-10 dB under the main hit of each beat, so they add life without competing."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(35)
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

PLACE = {}
for sid in ORDER:
    if sid in ("S0", "S0b", "S2", "S4", "S8", "S9", "S10"): PLACE[sid] = "stadium"
    elif sid in ("S5", "S5b", "S7"): PLACE[sid] = "kit"
    else: PLACE[sid] = "board"


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return PLACE[sid]


# ---------------- ROOM TONE per place (the arena tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"stadium": -39, "kit": -46, "board": -52}
arena = room_tone("arena", NS) * db(LVL["stadium"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = arena[a:b].copy() if kind == "stadium" else room_tone(kind, b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + arena[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S10": continue                                            # the loop tail enters silently
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
KO_T = T("i2", "knockout") - 0.12; CUFF_T = T("a2", "handcuffs") - 0.1
BIG = [KO_T, CUFF_T, T("b2", "third") - 0.15]
# S0 hook: the boxing bell at frame 0 (two strikes), the crowd, glove taps (secondary, low)
place(clang(-20, 1250, 0.9), 0.02, 540); place(clang(-22, 1250, 0.9), 0.32, 540)
place(crowd(-27, 2.0, 0.5), 0.0, 540)
for j in range(3): place(thud(-33), 0.55 + 1.3 * j, 470); place(thud(-34), 1.1 + 1.3 * j, 840)
# S0b face-off: a low rumble + a glove bump
place(slowmo_swell(-28, 1.4), S["S0b"] + 0.05, 540); place(thud(-24), T("i1", "milk") - 0.1, 540)
# S1 board: bars grow (stretch up), a count tick-run, the 8x ding
place(stretch(-27, 0.6, True), T("i2", "hundred") + 0.2, 770)
for j in range(10): place(tick(-31), T("i2", "sesame") - 0.1 + 0.11 * j, 310)
place(stretch(-25, 1.0, True), T("i2", "sesame"), 310)
place(ding(-22, 1568), T("i2", "eight") - 0.1, 540); place(boing_up(-26), T("i2", "eight") + 0.05, 610)
# S2 ON PAPER slap, the punch (BIG 1) + the crowd roars, rope creak (secondary)
place(press(-22), T("i2", "paper") - 0.15, 540)
place(whoosh(0.25, peak=0.8, level=-24), KO_T - 0.2, 600)
layered_hit(KO_T, -15, (85, 40), (200, 1600), 0.9, 1.1)
place(crowd(-22, 1.6, 1.0), KO_T + 0.05, 540)
place(creak(-31, 0.5), KO_T + 0.25, 980)
# S3 board: pebbles pop in, the skin hatches (scratch)
for j in range(12): place(pop(-31, 1000 + 60 * j), T("a1", "calcium") - 0.1 + 0.05 * j, 300 + 40 * j)
place(scratch(-29, 0.4), T("a1", "skin") - 0.3, 760)
# S3b cuffs click on (lock clicks, quiet), the oxalate label
for j in range(7): place(lock_click(-29), T("a1", "stuck") - 0.1 + 0.07 * j, 300 + 70 * j)
# S4 the cuffs fly in (whoosh), SNAP (BIG 2), the seed struggles = chain rattle (secondary)
place(whoosh(0.5, peak=0.7, level=-24), CUFF_T - 0.5, 700)
layered_hit(CUFF_T, -16, (110, 55), (400, 3000), 0.5, 1.4); place(lock_click(-17), CUFF_T, 520)
place(rattle(-27, max(0.3, SEND("S4") - CUFF_T - 0.3), 18), CUFF_T + 0.2, 520)
place(crowd(-28, 1.0, 0.0), CUFF_T + 0.1, 540)
# S4b gut: a soft gurgle under the ride, two 'pulled in' plips
place(squelch(-30, 0.8), S["S4b"] + 0.2, 540)
place(plip(-24, 700), T("a2", "pull") - 0.05, 300); place(plip(-24, 820), T("a2", "pull") + 0.05, 700)
place(deflate(-27, 0.6), T("a2", "small") - 0.15, 540)
# S5 the big bowl lands, the head shake 'nope' giggle
place(thud(-24), S["S5"] + 0.08, 760); place(rustle(-30, 0.6), S["S5"] + 0.15, 760)
place(giggle(-27, 0.5), T("b1", "nobody") - 0.1, 330)
# S5b deadpan: the tiny spoon clink
clink(T("b1", "spoonful") - 0.15, -24)
# S6 the third fills (BIG 3: a soft but full hit)
place(pour(-29, 0.6), S["S6"] + 0.3, 770)
layered_hit(BIG[2], -19, (100, 50), (300, 2200), 0.4, 1.0)
# S7 sprinkle (shaker) + a sparkle on BONUS
place(shaker_rattle(-27, SEND("S7") - S["S7"] - 0.2, 9), S["S7"] + 0.1, 640)
place(shimmer(-25, 1.0), T("c1", "bonus") - 0.15, 540)
# S7b the X stamp + buzzer
place(scratch(-24, 0.25), T("c1", "swap") - 0.15, 540); place(buzzer(-27, 0.3), T("c1", "swap") - 0.05, 540)
# S8 the friend lifts the laddoo: crowd cheer, the belt clank; a phone ping on 'send'
place(crowd(-25, 1.6, 0.8), T("c2", "luddoo") - 0.2, 790); place(clank(-26, 520), T("c2", "beats") - 0.1, 790)
place(ding(-24, 2093), T("c2", "Send") + 0.3, 540)
# S9 the logo sting (ends ~0.4 s before the seam)
audio_logo(S["S9"] + 0.05, -18)

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
