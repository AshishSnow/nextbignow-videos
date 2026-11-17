"""Mix ep 48: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: THE WINTER WEDDING TENT = new 'tent' reverb (cloth walls, short + dark) + room tone 'tent' (chatter inside + the crowd OUTSIDE heard THROUGH
the tent cloth = occluded; ONE continuous noise so the loop tail and the opening share it), the board = dry.
Craft skill (ep 48) = SOUND OCCLUSION (sfx_lib occlude(x, material)): the baraat cheer + firecrackers outside the tent come through the cloth (dull, quieter),
the scoop going down the throat on the board is heard 'from inside the body' (low-passed + chesty), the cold wind outside is behind the cloth."""

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



PLACE = {sid: ("board" if sid in ("S2", "S2b", "S4", "S6", "S6b", "S7") else "tent") for sid in ORDER}
VERB = {"tent": "tent", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the tent tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"tent": -40, "board": -52}
tent = room_tone("tent", NS) * db(LVL["tent"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = tent[a:b].copy() if kind == "tent" else room_tone(kind, b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + tent[:LOOPN] * np.linspace(0, 1, LOOPN)
AMB = np.stack([amb, np.roll(amb, 240)], 1)

# ---------------- transitions ----------------
for i, s in enumerate(SHOTLIST[1:], 1):
    k = s[2]; st = s[1]
    if s[0] == "S11": continue                                            # the loop tail enters silently
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-25, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
TNO = T("i2", "no") - 0.1; TFINE = T("i2", "fine") - 0.1; TV1 = T("a1", "virus", 1) - 0.12; TSN = T("a2", "sneeze") - 0.05; TSO = T("b2", "soothe") - 0.12
BIG = [TNO, TFINE, TSN, TSO]
# S0 hook (frame 0): teeth CHATTER + a breath of cold wind behind the cloth (occluded), a far firecracker OUTSIDE the tent (through the cloth)
place(chatter(-27, 1.3, 15), 0.02, 380); place(occlude(wind(-24, 2.2), "cloth"), 0.0, 120, far=0.5)
place(occlude(firecracker(-14), "cloth"), 0.9, 980, far=0.6)
place(clink(0.0, -32, 3800) if False else pop(-34, 2600), 0.05, 470)
# S0b: close-up chatter + a shiver 'brrr' (wind-ish lip trill = chatter at a lower rate)
place(chatter(-25, 1.4, 11), S["S0b"] + 0.05, 470); place(whoosh(0.3, peak=0.5, f_lo=900, f_hi=4000, level=-31), S["S0b"] + 0.45, 600)
# S1: the relatives: a tut-tut (two clicks) + finger wag swishes; BIG NO (layered hit)
for j in range(2): place(click(-22), S["S1"] + 0.25 + 0.14 * j, 300)
for j in range(3): place(whoosh(0.15, peak=0.5, f_lo=1500, f_hi=5000, level=-33), S["S1"] + 0.6 + 0.3 * j, 760)
place(buzzer(-27, 0.35), TNO, 540); layered_hit(TNO, -23, (120, 60), (300, 2400), 0.4, 1.2)
# S1b: the doctor's calm 'mm-hm' moment: a stethoscope clink, then FINE stamp + a warm ding
place(clink(S["S1b"] + 0.3, -30, 2600) if False else pop(-32, 1800), S["S1b"] + 0.3, 720)
place(press(-19), TFINE, 540); place(ding(-25, 1568), TFINE + 0.12, 540); layered_hit(TFINE, -25, (110, 55), (300, 2200), 0.35, 1.2)
# S2: the virus draws on, pops in
place(pop(-26, 900), T("a1", "virus") - 0.05, 800); place(boing(-29, 180, 0.35), T("a1", "virus") + 0.3, 800)
# S2b: the magnifier swish, snowflakes tinkle, red X scratch on 'no virus', a frosty shimmer on 'just cold'
place(whoosh(0.3, peak=0.5, f_lo=700, f_hi=3200, level=-30), S["S2b"] + 0.2, 700)
place(shimmer(-30, 0.6), S["S2b"] + 0.35, 700)
for j in range(2): place(scratch(-24, 0.18), TV1 + 0.25 + 0.1 * j, 700)
place(ice_crack(-26, 0.5), T("a1", "just") - 0.1, 470)
# S3 BIG: the sneeze ('ah... CHOO') from the guest on the right; the cough; Chubby's recoil
place(sneeze(-17), TSN - 0.34, 760); layered_hit(TSN, -24, (140, 70), (500, 3200), 0.4, 1.4)
for j in range(2): place(thud(-31), T("a2", "cough") - 0.05 + 0.14 * j, 760)
# S3b: the ladle clanks against the steel bowl each time a hand grabs it; viruses hop on (tiny pops)
for j in range(5): place(clank(-27, 520 + 30 * j), S["S3b"] + 0.2 + 0.42 * j, 640)
for j in range(4): place(pop(-33, 1500 + 200 * j), S["S3b"] + 0.25 + 0.3 * j, 560 + 60 * j)
# S4: the tent flaps drop shut (two soft cloth thumps + rustle); the crowd outside goes MORE muffled once the flaps close; the virus hops (boing)
for j, x in enumerate((150, 930)): place(rustle(-25, 0.35), T("a3", "indoors") - 0.4 + 0.08 * j, x); place(thud(-29), T("a3", "indoors") - 0.1 + 0.08 * j, x)
place(occlude(far_cheer(-22, 1.4), "cloth"), S["S4"] + 0.1, 980, far=0.5)
for j in range(3): place(boing(-29, 240 + 40 * j, 0.3), T("a3", "hops") + 0.6 * j, 300 + 200 * j)
# S5: the TAKE ('wait'): a record-scratch-free stop: drop-out + a bright sting + the cone held up into the light (shimmer)
place(boing_up(-24, 300, 0.35), T("b1", "wait") - 0.08, 540); place(shimmer(-28, 0.9), T("b1", "help") - 0.1, 700)
# S6: the sore throat: a dry cough + sizzle (heat zigzags)
place(thud(-30), T("b2", "sore"), 560); place(sizzle(-33, 1.4), T("b2", "throat"), 640)
# S6b: the scoop slides DOWN the throat, heard from INSIDE the body (occluded gulp), then the cool-down shimmer on 'soothe' (BIG)
place(occlude(gulp(-14), "body"), T("b2", "cold") + 0.05, 560); place(occlude(slurp(-22, 0.6), "body"), T("b2", "cold") + 0.2, 560)
place(shimmer(-26, 1.0), TSO, 560); layered_hit(TSO, -27, (100, 50), (400, 3000), 0.5, 1.3)
# S7: card writes (pen already), a tick per row, the lolly pops in with a ding
for j in range(2): place(tick(-27), S["S7"] + 0.85 + 0.35 * j, 270)
place(pop(-24, 1100), T("b3", "lollies") - 0.12, 800); place(ding(-25, 2093), T("b3", "lollies"), 800)
# S8: Chubby munches happily; the aunty gasps (a tiny sniff)
place(munch_sfx(-25, min(1.4, SEND("S8") - S["S8"] - 0.1)), S["S8"] + 0.1, 470); place(sniff(-28, 0.3), S["S8"] + 0.4, 860)
# S8b: water poured from the lota over the hands, soap squelch + bubbles
place(pour(-24, min(1.8, SEND("S8b") - S["S8b"])), S["S8b"] + 0.05, 600); bubbles(S["S8b"] + 0.3, 8, -28)
# S9: the send ding, the aunty's sneaky spoon (a sly pizzicato-like pop pair)
place(ding(-24, 2093), T("c2", "Send") + 0.3, 540)
for j in range(2): place(pop(-27, 700 + 300 * j), T("c2", "winter") - 0.1 + 0.18 * j, 790)
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
