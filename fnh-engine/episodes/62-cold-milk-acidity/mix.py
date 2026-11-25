"""Mix ep 62: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the night BEDROOM =
one continuous quiet room tone (soft room + wind behind the window) + a far wall-clock tick; the heartburn flames CRACKLE whenever they show (level
follows the burn); the 1970s room = film crackle; the board = dry pen + eraser. The CLOCK WIPE gets its sound twin: a clock that ticks fast across the
sweep (time passing) and a soft bell when it lands. Big hits: CURE?, MORE ACID, THE BURN IS BACK, RAISED, NOT A CURE."""


import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(62)
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

BEDR = ("S0", "S0b", "S1", "S1b", "S3c", "S5b", "S7", "S7b", "S8", "S9")
OLD = ("S4",)
def kind_of(sid): return "bed" if sid in BEDR else "old" if sid in OLD else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"bed": "kit", "old": "party", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


LVL = {"bed": -44, "old": -46, "board": -52}
home = room_tone("winter", NS) * db(LVL["bed"])
for k_ in range(int(END)):                                                   # a far wall clock in the bedroom
    a_ = int((k_ + 0.5) * SR); tk_ = tick(-44); b_ = min(NS, a_ + len(tk_)); home[a_:b_] += np.asarray(tk_, np.float32).reshape(len(tk_), -1).mean(1)[:b_ - a_] * 0.7
oldt = (room_tone("tv", NS) * db(-52) + film_crackle(NS) * db(-40)).astype(np.float32)
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    if kind == "bed": seg = home[a:b].copy()
    elif kind == "old": seg = oldt[a:b].copy()
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
    if s[0] in ("S8", "S9"): continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- the CLOCK WIPE sound twin: ticks that speed up across the sweep, a soft bell when it lands ----------------
TC = S["S3"]; CLOCK_D = 0.6
for j in range(10):
    u = j / 9; tt_ = TC + CLOCK_D * (0.5 - 0.5 * math.cos(math.pi * u))
    place(tick(-27 + 3 * math.sin(math.pi * u)), tt_, 540 + 200 * math.sin(2 * math.pi * u))
place(ding(-30, 1046.5), TC + CLOCK_D, 540)

# ---------------- the heartburn crackle (follows the flames on screen) ----------------
FL = [("S0", 0.6), ("S0b", 0.8), ("S1b", 0.4), ("S2", 0.5), ("S3b", 0.7), ("S3c", 1.0), ("S5", 0.5), ("S5b", 0.7)]
for sid, lv in FL:
    d_ = SEND(sid) - S[sid]
    if d_ > 0.1: place(crackle(-30 + 6 * lv, d_), S[sid], 470)

# ---------------- spotting ----------------
TCURE = T("i1", "cure") - 0.1; TMORE = T("a1", "more") - 0.05; TBACK = S["S3c"] + 0.05; TRAISE = T("a2", "raised") - 0.1; TNOT = T("c1", "not") - 0.1
BIG = [TCURE, TMORE, TBACK, TRAISE]
# S0: he gulps the cold milk (gulps + a glug), a cold clink of the glass; CURE hit
for j in range(3): place(gulp(-27), 0.35 + 0.55 * j, 480)
place(clink(0.0, -32, 3600) if False else ding(-34, 3520), 0.05, 560)
layered_hit(TCURE, -24, (90, 45), (250, 2200), 0.4, 1.0)
# S0b: a wince (squelch-ish growl from the stomach)
place(growl(-30, 0.9), S["S0b"] + 0.2, 540)
# S1: mom's nods (tiny whooshes) + a ding on 'swears'
for j in range(3): place(whoosh(0.12, peak=0.5, f_lo=1500, f_hi=5000, level=-36), T("i2", "swears") + 0.1 + 0.35 * j, 700)
place(ding(-28, 1318.5), T("i2", "swears") - 0.05, 640)
# S1b: a gulp, the flames die down (hiss), the relieved exhale (wash), a calm ding on 'works'
place(gulp(-26), S["S1b"] + 0.2, 480); place(hiss(-28, 1.0), S["S1b"] + 0.5, 470); place(wash(-30, 0.9), S["S1b"] + 0.9, 560)
place(ding(-26, 1568), T("i2", "works.") - 0.05, 540)
# S2: milk pours down the pipe onto the acid (pour + a splash), the flames hiss out on 'calms'
place(pour(-26, 1.2), S["S2"] + 0.45, 545); place(splash_sfx(-28, 0.6, 2), S["S2"] + 0.8, 545)
place(hiss(-26, 1.0), T("i3", "calms") - 0.1, 600); place(ding(-27, 1568), T("i3", "calms") - 0.05, 540)
# S3: protein beads pop in, the sensor rings (bell)
for j in range(5): place(pop(-32, 1100 + 120 * j), T("a1", "notices") - 0.1 + 0.12 * j, 640 + 70 * j)
place(bell(-28, 1760, 0.9), T("a1", "protein,") - 0.1, 380)
# S3b: the tap squeaks open + clank, acid pours (glug), MORE ACID = layered hit + flame whoosh
place(squeak(-28), S["S3b"] + 0.15, 840); place(clank(-28, 520), S["S3b"] + 0.2, 840); place(pour(-25, 1.1), S["S3b"] + 0.25, 880)
layered_hit(TMORE, -22, (100, 50), (300, 2400), 0.5, 1.2); place(flame_whoosh(-24) if "flame_whoosh" in globals() else whoosh(0.5, level=-24), TMORE + 0.05, 600)
# S3c: THE BURN IS BACK = a take (boing) + a flame burst
layered_hit(TBACK, -23, (90, 45), (250, 2200), 0.4, 1.0); place(boing(-30, 300, 0.3), TBACK + 0.05, 440)
# S4: 1970s room: a projector-ish click, 1976 pop
place(torch_click(-26), T("a2", "nineteen") - 0.12, 540); place(pop(-24, 900), T("a2", "nineteen") - 0.1, 540)
# S4b: cartons land (thud) on each word
for wd, x in (("Whole", 220), ("low-fat,", 540), ("skim.", 860)): place(soft_flop(-26), T("a2", wd) - 0.08, x)
# S4c: the three meters climb (stretch up) + RAISED hit + buzzer
place(stretch(-28, 0.7, True), TRAISE, 540); layered_hit(TRAISE, -23, (100, 50), (300, 2400), 0.4, 1.0); place(buzzer(-32, 0.35), TRAISE + 0.25, 540)
# S5: fat drops plop, the valve creaks loose, acid creeps up (squelch)
for j in range(4): place(plip(-28, 700 - 60 * j), T("b1", "fat") + 0.15 * j + 0.5, 545)
place(creak(-27, 0.6), T("b1", "loosens") - 0.1, 545); place(squelch(-28, 0.8), T("b1", "loosens") + 0.5, 545)
# S5b: a small burp (a low growl blip) + the flames
place(growl(-26, 0.35), S["S5b"] + 0.6, 480)
# S6: a flame pops into each day
for wd in ("burn", "shows", "twice"): place(flame_whoosh(-30) if "flame_whoosh" in globals() else pop(-28, 800), T("c1", wd) - 0.05, 540)
# S6b: DOCTOR ding, NOT A CURE stamp
place(ding(-25, 1318.5), T("c1", "doctor,") - 0.05, 400); place(press(-22), TNOT + 0.1, 800); layered_hit(TNOT + 0.1, -26, (90, 45), (250, 2000), 0.3, 0.8)
# S7: send line ding; S7b: the glass on the table clinks
place(ding(-25, 2093), T("c2", "Send") + 0.3, 540); place(ding(-32, 3520), T("c2", "bed") - 0.05, 700)
# S8 logo sting
audio_logo(S["S8"] + 0.02, -18)

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
