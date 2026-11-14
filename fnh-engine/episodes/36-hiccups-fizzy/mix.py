"""Mix ep 36: VO + foley placed in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0).
Places: THE HOUSE PARTY = new 'party' reverb (a living room full of people) + a 'party' room tone (chatter + far clinks, ONE continuous noise so the
loop tail and the opening share it); the board = dry. Craft skill (ep 36, INVOLUNTARY ACTION) on the audio side: every hic is sfx_lib.hic_sfx with NO
lead-in (full tilt from sample 0, like the 2-frame jolt) and a different pitch each time, so a run of hiccups never sounds copy-pasted."""

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

HIC0 = [T("i1", "hiccups") - 0.02, T("i1", "fizzy") + 0.25]
HIC1 = [T("i2", "stomach") + 0.45]
HIC_BIG = T("a4", "Hic") - 0.04
HIC6 = [T("b1", "Most") + 0.05]
HIC_BABY = [T("c1", "hiccupping") - 0.05, T("c1", "hiccupping") + 0.75, T("c1", "born") - 0.05]
HIC_FRIEND = [T("c2", "third") - 0.05, T("c2", "party") - 0.1]

PLACE = {}
for sid in ORDER:
    PLACE[sid] = "party" if sid in ("S0", "S0b", "S1b", "S3", "S5b", "S6", "S8", "S9", "S10") else "board"


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return PLACE[sid]


# ---------------- ROOM TONE per place (the party tone is ONE continuous noise, so the loop tail and the opening share it) ----------------
LVL = {"party": -40, "board": -52}
party = room_tone("party", NS) * db(LVL["party"])
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    seg = party[a:b].copy() if kind == "party" else room_tone(kind, b - a) * db(LVL[kind])
    fd = min(int(0.02 * SR), (b - a) // 2); seg[:fd] *= np.linspace(0, 1, fd); seg[-fd:] *= np.linspace(1, 0, fd); amb[a:b] += seg
amb *= (1 - 0.5 * g)
LOOPN = int(0.33 * SR)
amb[-LOOPN:] = amb[-LOOPN:] * np.linspace(1, 0, LOOPN) + party[:LOOPN] * np.linspace(0, 1, LOOPN)
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
def hics(times, xpos, lv=-19, p0=1.0, step=0.07, where=None):
    for j, ti in enumerate(times): place(hic_sfx(lv - 1.5 * (j % 2), p0 + step * ((j * 3) % 4 - 1.5)), ti, xpos, where=where)


BIG = [T("a3", "jerks") - 0.08, T("a4", "slam") - 0.06, HIC_BIG]
# S0 hook: the gulp + fizz already going at frame 0, then the two hics
place(fizz(-27, 1.2), 0.0, 470); place(glug(-24, 3, 0.24), 0.02, 430)
hics(HIC0, 420)
# S1 board: bubbles tickle (tiny fizz), the X scratch
place(fizz(-30, 1.0), T("i2", "bubbles") - 0.1, 540); place(scratch(-23, 0.3), T("i2", "throat") - 0.1, 540)
# S1b: deadpan 'stomach' = a soft thud + the window opening (shimmer), one hic
place(thud(-27), T("i2", "stomach") - 0.15, 400); place(shimmer(-29, 0.6), T("i2", "stomach") - 0.1, 420)
hics(HIC1, 400, -20, 0.92)
# S2 / S2b board: the dome draws on, a breath in/out under the breathing dome
place(stretch(-28, 0.6, True), T("a1", "dome") - 0.1, 540)
for j in range(3): place(whoosh(0.6, peak=0.5, f_lo=200, f_hi=1500, level=-31), T("a1", "pulls") - 0.1 + 1.5 * j, 540)
# S3 party: a big chug (glugs) + fizz; GAS
place(glug(-23, 5, 0.22), S["S3"] + 0.1, 430); place(fizz(-27, 1.4), S["S3"] + 0.1, 470)
place(boing(-27, 180, 0.4), T("a2", "gas") - 0.12, 540)
# S3b balloon inflating (rising stretch) + rubber squeak
place(stretch(-24, 1.1, True), T("a2", "stretches") - 0.1, 660); place(squeak(-28), T("a2", "balloon") - 0.1, 660)
place(press(-27), T("a2", "right") - 0.05, 700)
# S4 nerve: buzzy alarm zaps along the nerve
place(buzz(-29, 0.8, 180), T("a3", "irritated") - 0.15, 260)
for j in range(3): place(magnet_zing(-30, 0.3), T("a3", "irritated") - 0.1 + 0.25 * j, 300)
# S4b BIG 1: the dome JERKS (layered hit, no lead-in), then the air rushes (long whoosh down)
layered_hit(BIG[0], -17, (90, 45), (200, 1600), 0.6, 1.0)
place(whoosh(0.9, peak=0.3, f_lo=300, f_hi=4000, level=-23), T("a3", "Air") - 0.15, 540)
# S5 BIG 2: the doors SLAM (a real door slam = low thud + latch click)
layered_hit(BIG[1], -15, (80, 40), (150, 1200), 0.9, 1.2); place(lock_click(-20), BIG[1] + 0.01, 540)
place(creak(-30, 0.4), T("a4", "door") - 0.1, 700)
# S5b BIG 3: the big HIC (hic_sfx on top of a soft layered hit so it lands), then silence for the deadpan
place(hic_sfx(-14, 0.95), HIC_BIG, 500); layered_hit(HIC_BIG, -22, (120, 60), (300, 2400), 0.4, 1.0)
# S6: one last little hic, then a relieved exhale; the clock ticks
hics(HIC6, 380, -23, 1.05)
for j in range(6): place(tick(-29), S["S6"] + 0.2 + 0.3 * j, 800)
place(whoosh(0.7, peak=0.4, f_lo=200, f_hi=1200, level=-29), T("b1", "minutes") - 0.1, 380)
# S6b board: day boxes pop, the stethoscope ding
place(pop(-27, 900), S["S6b"] + 0.2, 340); place(pop(-27, 1050), T("b1", "two") - 0.15, 740)
place(ding(-25, 1318), T("b1", "doctor") - 0.15, 540)
# S7 ultrasound: the soft whoosh-beat of an ultrasound + three tiny high hics from the baby
place(slowmo_swell(-30, 1.6), S["S7"] + 0.1, 540)
for j, ti in enumerate(HIC_BABY): place(hic_sfx(-26, 1.6 + 0.08 * j), ti, 640)
place(shimmer(-26, 0.8), T("c1", "womb") - 0.15, 540)
# S8 party: the friend's hics (lower voice), Chubby's giggle, the send ping
hics(HIC_FRIEND, 760, -20, 0.85)
place(giggle(-27, 0.5), T("c2", "third") + 0.4, 250)
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
