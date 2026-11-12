"""Mix ep 34: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: the CHAAT STALL = 'street' (new room in sfx_lib.ir: open street, short shopfront slaps, 0.55 s tail), the worktop = 'kit', the board = dry.
CRAFT SKILL (ep 34): THE LOOP ENDING, audio side (CapCut 'seamless loop' guide 2026: 'listen for clicks, clipped breaths, hard music endings, or voiceover
phrases that make the loop point too obvious'): the last 0.8 s is ONLY the stall's room tone at the SAME level as the opening second (no sting, no tail crossing
the seam), the logo sting finishes 0.4 s before the end, and the opening second's tone is copied from the same noise so the wrap is continuous."""
import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(34)
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
    if sid in ("S0", "S0b", "S2", "S4b", "S5b", "S6", "S9", "S10", "S11", "S12"): PLACE[sid] = "street"
    elif sid == "S8": PLACE[sid] = "kit"
    else: PLACE[sid] = "board"


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return PLACE[sid]


# ---------------- ROOM TONE per place (the street tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"street": -40, "kit": -46, "board": -52}
street = room_tone("street", NS) * db(LVL["street"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = street[a:b].copy() if kind == "street" else room_tone(kind, b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)                                                    # the seam: the last 0.33 s crossfades into the opening's tone
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + street[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S12": continue                                            # the loop tail enters silently
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
BIG = [T("a3", "trips") + 0.1, T("a3", "fire") - 0.25, T("b1", "false") - 0.2]
# S0 hook: a crunch of the puri at frame 0, a sniffle, the drip lets go on 'runs' (plip), the take
place(crunch(-22), 0.02, 600); place(sniffle(-22), 0.6, 560)
place(plip(-22, 700), T("i1", "runs") - 0.15, 560); place(boing(-25, 300, 0.3), T("i1", "runs") - 0.1, 540)
# S0b close-up: the gasp + a big sniffle; tissue box slides in
place(hiss(-28, 0.5), T("i1", "spicy") - 0.2, 540); place(sniffle(-20, 0.45), T("i1", "spicy") + 0.2, 540)
place(whoosh(0.3, peak=0.7, level=-27), T("i1", "spicy") - 0.15, 900); place(thud(-26), T("i1", "spicy") + 0.2, 860)
# S1 board: two X stamps + a buzzer
place(scratch(-25, 0.25), T("i2", "cold") + 0.1, 300); place(scratch(-25, 0.25), T("i2", "allergy") + 0.15, 780)
place(buzzer(-27, 0.3), T("i2", "cold") + 0.2, 540)
# S2 chilli: pops for each flame buddy, a sizzle on HOT
for j in range(4): place(pop(-26, 900 + 140 * j), T("a1", "capsaicin") - 0.15 + 0.12 * j, (260, 790, 210, 840)[j])
place(sizzle(-27, 1.0), T("a1", "hot") - 0.2, 540)
# S3 board: a soft ding when the sensor appears
place(ding(-27, 1046.5), T("a2", "nerve") + 0.15, 330); place(ding(-25, 1318.5), T("a2", "heat") - 0.25, 330)
# S4 the buddy creeps up, trips the nerve: ALARM (BIG 1)
place(creep(-28, max(0.3, T("a3", "trips") - S["S4"])), S["S4"] + 0.05, 760)
layered_hit(BIG[0], -18, (100, 50), (300, 2000), 0.5, 1.2)
place(bell(-21, 1760, SEND("S4") - BIG[0] + 0.1, 18), BIG[0], 330)
# S4b ON FIRE (BIG 2): flames catch round his head
place(flame_whoosh(-19, 1.0), BIG[1] - 0.05, 540)
layered_hit(BIG[1], -15, (80, 40), (150, 900), 1.0)
place(crackle(-27, 1.2), BIG[1] + 0.2, 540)
# S5 the tap turns, mucus pours
place(knob(-24), T("a4", "opens") - 0.1, 800); place(faucet(-26, SEND("S5") - T("a4", "opens")), T("a4", "opens"), 860)
place(squelch(-26, 0.5), T("a4", "Mucus") - 0.1, 860)
# S5b tissue after tissue
for j in range(int((SEND("S5b") - S["S5b"]) / 0.32) + 1): place(tissue_pull(-24), S["S5b"] + 0.32 * j, 800)
place(sniffle(-23), S["S5b"] + 0.9, 420)
# S6 lights down, the bell still rings far, footstep, extinguisher puff, FALSE ALARM stamp (BIG 3)
place(bell(-30, 1760, BIG[2] - S["S6"], 18), S["S6"], 900, far=0.6)
place(footstep(-26, 0.8), S["S6"] + 0.4, 440); place(footstep(-26, 0.8), S["S6"] + 0.8, 640)
place(spray(-26, 0.35), S["S6"] + 1.1, 700)
layered_hit(BIG[2], -16, (90, 45), (250, 1800), 0.6, 1.0)
place(boing(-26, 220, 0.5), BIG[2] + 0.3, 540)
# S7 the name writes itself; 'Big name' boing; 'runny nose' sniffle
place(stretch(-26, 0.5, True), T("b2", "Big") - 0.15, 540); place(plip(-24, 600), T("b2", "runny") - 0.1, 540); place(sniffle(-24), T("b2", "nose") - 0.1, 540)
# S8 soup: slurp + the sniffle starting
place(sip(-24, 0.35), S["S8"] + 0.3, 600); place(simmer(-31, SEND("S8") - S["S8"]), S["S8"], 760, where="kit"); place(sniffle(-24), T("b3", "set") - 0.1, 400)
# S9 the clock ticks fast, then a satisfied 'ding'
tf = T("b4", "few") - 0.2; t1 = T("b4", "eating") + 0.2
for j in range(int((t1 - tf) / 0.12)): place(tick(-29), tf + 0.12 * j, 800)
place(ding(-25, 1568), t1, 540)
# S9b board: pops for each tissue, the stethoscope ding
for j in range(5): place(pop(-28, 1000 + 80 * j), T("b4", "all") - 0.15 + 0.08 * j, 180 + 180 * j)
place(ding(-25, 1174.7), T("b4", "doctor") - 0.25, 540)
# S10: friend sniffles, box slides across, a phone ping on 'send'
place(sniffle(-22), S["S10"] + 0.6, 790); place(whoosh(0.3, peak=0.6, level=-28), T("c1", "tissue") - 0.25, 500); place(thud(-27), T("c1", "tissue") + 0.1, 580)
place(ding(-24, 2093), T("c1", "Send") + 0.3, 540)
# S11 the logo sting (ends ~0.4 s before the seam)
audio_logo(S["S11"] + 0.05, -18)

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
