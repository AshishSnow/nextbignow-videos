"""Mix ep 44: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: the WINTER LUNCH TABLE = 'kit' room + a soft winter wind behind the window (ONE continuous noise so the loop tail and the opening share it),
THE LINEUP ROOM = new 'lineup' reverb (a small bare concrete room: early slap at 6-14 ms, 0.5 s bright tail) + room tone (the strip light's 120 Hz
fluorescent buzz + a ventilation hiss), the TV room = 'party' (living room), the worktop + bathroom = 'kit', the board = dry.
Craft skill (ep 44) = the SILHOUETTE REVEAL, in sound too: the lineup room tone DROPS OUT under the silhouette (only the buzz), a held low drone, then
the lamp CLICK + layered hit land exactly on 'viruses' when the light comes on."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(44)
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


# ---------------- NEW ROOM: the lineup room (ep 44) ----------------
_ir_prev44 = ir
def ir(kind):
    if kind == "lineup":                                                            # bare concrete + glass: early slaps, a bright 0.5 s tail
        n_ = int(0.62 * SR); out = np.zeros((n_, 2), np.float32); tt = np.arange(n_) / SR
        for ch in range(2):
            r = np.random.default_rng(144 + ch)
            tail = r.standard_normal(n_) * np.exp(-6.9 * np.maximum(0, tt - 0.006) / 0.5) * (tt >= 0.006)
            tail = signal.sosfilt(signal.butter(2, 7500, "low", fs=SR, output="sos"), tail); tail = tail / (np.sqrt(np.sum(tail ** 2)) + 1e-9) * 0.55
            for d_, a_ in ((0.006, 0.6), (0.011, 0.45), (0.014, 0.35), (0.023, 0.2)):
                k = int((d_ + 0.003 * ch) * SR); tail[k] += a_
            out[:, ch] = tail
        return out
    return _ir_prev44(kind)


WET["lineup"] = -11; BUS["lineup"] = np.zeros((NS, 2), np.float32)
_rt_prev44 = room_tone
def room_tone(kind, n_):
    if kind == "lineup":                                                            # fluorescent strip light: 120 Hz + harmonics buzz + ventilation hiss
        tt = np.arange(n_) / SR
        x = (0.3 * np.sin(2 * np.pi * 120 * tt) + 0.12 * np.sin(2 * np.pi * 240 * tt) + 0.06 * np.sign(np.sin(2 * np.pi * 120 * tt)) * 0.4
             + _bp(rng.standard_normal(n_), 300, 3000) * 0.35)
        return x / (np.abs(x).max() + 1e-9)
    if kind == "winter":                                                            # the lunch table in winter: a soft kitchen room + wind behind glass
        tt = np.arange(n_) / SR
        x = _lp(rng.standard_normal(n_), 1500) * 0.35 + _bp(rng.standard_normal(n_), 250, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * tt) ** 2) * 0.6
        return x / (np.abs(x).max() + 1e-9)
    return _rt_prev44(kind, n_)


VX = 750
PLACE = {}
for sid in ORDER:
    PLACE[sid] = ("winter" if sid in ("S0", "S0b", "S8", "S9", "S10") else "lineup" if sid in ("S1", "S1b", "S2", "S5")
                  else "party" if sid in ("S3", "S3b") else "kit" if sid in ("S6", "S7") else "board")
VERB = {"winter": "kit", "lineup": "lineup", "party": "party", "kit": "kit", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


# ---------------- ROOM TONE per place (the winter table tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"winter": -40, "lineup": -42, "party": -44, "kit": -44, "board": -52}
wint = room_tone("winter", NS) * db(LVL["winter"])
amb = np.zeros(NS, np.float32)
TV = T("a1", "viruses") - 0.15
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = wint[a:b].copy() if kind == "winter" else room_tone(kind, b - a) * db(LVL[kind])
    if sid == "S2":                                                                 # the silhouette beat: lights down = the room goes thin (buzz only)
        tt = st + np.arange(b - a) / SR; seg = seg * np.where(tt < TV, 0.45, 1.0).astype(np.float32)
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + wint[:LOOPN] * np.linspace(0, 1, LOOPN)
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
BIG = [T("i2", "blame") - 0.12, TV, T("a2", "sneeze") - 0.05, T("b1", "innocent") - 0.12]
# S0 hook (frame 0): the spoon already at his lips (a tiny clink of steel), the aunty's palm (a sharp 'tch' = click), a held shiver
clink(0.04, -27, 3600); place(click(-24), 0.12, 860); place(wind(-31, 1.6), 0.0, 760)
# S0b: double take (a quick whoosh of the eyes), the spoon wobbles
place(whoosh(0.25, peak=0.5, f_lo=900, f_hi=4000, level=-30), S["S0b"] + 0.3, 600)
# S1: lineup; the strip light thunks on, the curd's sweat drop plips, the MUGSHOT flash on 'blame' (BIG 1)
place(clank(-28, 300), S["S1"] + 0.02, 540); place(plip(-27, 1300), S["S1"] + 0.6, 380)
place(click(-18), BIG[0] - 0.02, 540); place(shimmer(-30, 0.4), BIG[0], 540); layered_hit(BIG[0], -22, (120, 60), (300, 2400), 0.4, 1.3)
# S1b: detective footsteps in, the magnifier swish, the stamp on 'wrong'
for j in range(2): place(footstep(-27), S["S1b"] + 0.05 + 0.3 * j, 290)
place(whoosh(0.3, peak=0.5, f_lo=600, f_hi=3000, level=-29), S["S1b"] + 0.7, 380)
place(press(-20), T("i2", "wrong") - 0.1, 540)
# S2 BIG 2: lights DOWN (a low hum swell under the silhouette), then the lamp CLICK + hit exactly on 'viruses'
place(stretch(-30, max(0.4, TV - S["S2"] - 0.1), True), S["S2"] + 0.05, VX)
place(torch_click(-16), TV - 0.02, VX); layered_hit(TV, -19, (90, 42), (220, 1800), 0.7, 1.0)
place(boing(-28, 160, 0.4), TV + 0.35, VX)
# S2b: on the board, the virus pops in, red X slashes on 'food'
place(pop(-26, 1000), S["S2b"] + 0.25, 540)
for j, x in enumerate((330, 760)): place(scratch(-25, 0.2), T("a1", "food") - 0.1 + 0.12 * j, x)
# S3 BIG 3: the sneeze ('ah... CHOO') from the cousin on the left; the cough; Chubby's 'eww' recoil
place(sneeze(-17), BIG[2] - 0.34, 360); layered_hit(BIG[2], -24, (140, 70), (500, 3200), 0.4, 1.4)
place(slurp(-30, 0.3), BIG[2] + 0.25, 720)
for j in range(2): place(thud(-31), T("a2", "cough") - 0.05 + 0.14 * j, 360)
place(whoosh(0.3, peak=0.4, f_lo=1500, f_hi=6000, level=-32), T("a2", "cough"), 500)
# S3b: the handshake pumps (rustle on each pump), little viruses hop (tiny pops)
for j in range(3): place(rustle(-28, 0.12), S["S3b"] + 0.05 + 0.26 * j, 540)
for j in range(4): place(pop(-33, 1500 + 200 * j), S["S3b"] + 0.25 + 0.22 * j, 400 + 80 * j)
# S4: the windows SLAM shut (two clanks), the air swirl (soft wind), the virus hops (boing)
for j, x in enumerate((290, 790)): place(clank(-24, 380), T("a3", "windows") - 0.1 + 0.1 * j, x)
place(wind(-30, 1.2), T("a3", "same") - 0.1, 540); place(boing(-29, 260, 0.35), T("a3", "same") + 0.3, 540)
# S5 BIG 4: the cuffs lock on the virus, INNOCENT stamp, the curd's footsteps out, the hat tip
place(lock_click(-20), S["S5"] + 0.15, VX); place(rattle(-28, 0.4), S["S5"] + 0.3, VX)
place(press(-19), BIG[3], 540); layered_hit(BIG[3], -23, (110, 55), (300, 2200), 0.4, 1.2)
for j in range(4): place(footstep(-30, 0.5), T("b1", "Doctors") + 0.3 + 0.28 * j, 300 - 60 * j)
place(whoosh(0.25, peak=0.5, f_lo=700, f_hi=3000, level=-30), T("b1", "Doctors") + 0.2, 190)
# S5b: the friendly bacteria giggle; the arrow to the gut
place(giggle(-29, 0.5), T("b1", "bacteria"), 700); place(pop(-27, 900), T("b1", "gut") - 0.15, 540)
# S6: fridge-cold (a frosty shimmer), the throat (a small cough), the timer ticks while it sits
place(shimmer(-30, 0.8), S["S6"] + 0.1, 800); place(thud(-32), T("b2", "throat") - 0.05, 400)
for j in range(5): place(tick(-29), T("b2", "sit") - 0.1 + 0.35 * j, 800)
place(ding(-26, 1568), T("b2", "sit") + 1.7, 800)
# S7: the tap runs, soap squelch + bubbles while he scrubs, viruses swirl down the drain
place(tap_run(-25, min(3.5, SEND("S7") - S["S7"] - 0.3)), S["S7"] + 0.2, 540)
bubbles(T("c1", "wash") - 0.05, 9, -27)
place(slurp(-31, 0.4), T("c1", "hands") + 0.1, 540)
# S8: the curd slides away on the cloth, Chubby's smirk 'hm', the send ding
place(rustle(-26, 0.5), T("c2", "curd") - 0.15, 620); place(ding(-24, 2093), T("c2", "Send") + 0.3, 540)
# S9 the logo sting (ends before the seam)
audio_logo(S["S9"] + 0.03, -18)

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
