"""Mix ep 61: VO + foley in the room -> work/mix.wav (-11 LUFS, -1.5 dBTP). NO music bed (owner 9 Nov; BED stays 0). Places: the night TV ROOM = ONE
continuous room tone ('tv' hum) + the TV PROGRAMME itself as the craft's SOUND TWIN (tv_babble: a muffled cartoon show whose timbre jumps at the same
scene cuts as the screen light, and that goes FAR (persp) when Chubby sits back); the 1960s ROOM = film crackle + a GEIGER counter that speeds up
with the radiation; the board = dry. Big hits: SIT BACK, the 1960s reveal, LEAKED, RECALLED."""

import sys, json, math, subprocess, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))); _D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
sys.path.insert(0, f"{R}/lib"); import bed_carve
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(61)
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







SCENES = [0] * 6
exec('def tv_scene' + open(f'{_D}/anim_props6.py').read().split('def tv_scene')[1].split('\n\n\n')[0])


def tv_babble(n_, t0=0.0, level=-34):
    """the TV programme heard in the room: band-limited 'voices' (formant-ish noise bursts at syllable rate) + a little music, whose pitch/colour
    changes at every SCENE CUT of tv_scene (the same cuts as the screen light)."""
    tt = t0 + np.arange(n_) / SR
    out = np.zeros(n_, np.float32); i0 = None; a = 0
    for k in range(0, n_, int(0.05 * SR)):
        i, _ = tv_scene(tt[k])
        if i != i0 and k > 0:
            seg = slice(a, k); fc = 600 + 220 * i0; syl = 3.5 + 0.7 * i0
            out[seg] = (_bp(rng.standard_normal(k - a), fc, fc * 2.6) * (0.5 + 0.5 * np.sin(2 * np.pi * syl * tt[seg]) ** 4)
                        + 0.4 * np.sin(2 * np.pi * (220 + 40 * i0) * tt[seg]) * (np.sin(2 * np.pi * 2 * tt[seg]) > 0))
            a = k
        i0 = i
    fc = 600 + 220 * i0
    out[a:] = _bp(rng.standard_normal(n_ - a), fc, fc * 2.6) * (0.5 + 0.5 * np.sin(2 * np.pi * 4 * tt[a:]) ** 4)
    out = _lp(out, 3200)
    return (out / (np.abs(out).max() + 1e-9) * db(level)).astype(np.float32)


def geiger(level=-28, dur=2.0, rate0=4, rate1=40, seed=1):
    """a Geiger counter: random clicks whose rate climbs from rate0 to rate1 per second."""
    n_ = int(dur * SR); y = np.zeros(n_, np.float32); r = np.random.default_rng(seed); t_ = 0.0
    while t_ < dur:
        rate = rate0 + (rate1 - rate0) * (t_ / dur); t_ += r.exponential(1 / rate)
        k = int(t_ * SR)
        if k < n_ - 200: y[k:k + 200] += (r.standard_normal(200) * np.exp(-np.arange(200) / 18)).astype(np.float32)
    y = _hp(y, 1500)
    return y / (np.abs(y).max() + 1e-9) * db(level)


TVR = ("S0", "S0b", "S1", "S1b", "S6", "S6b", "S9", "S10", "S11")
OLD = ("S3", "S4", "S4b", "S5")
def kind_of(sid): return "tv" if sid in TVR else "old" if sid in OLD else "board"
PLACE = {sid: kind_of(sid) for sid in ORDER}
VERB = {"tv": "party", "old": "party", "board": "board"}


def place_at(t):
    sid = next((k for k in reversed(ORDER) if S[k] <= t), ORDER[0]); return VERB[PLACE[sid]]


LVL = {"tv": -42, "old": -44, "board": -52}
home = room_tone("tv", NS) * db(LVL["tv"])
show = tv_babble(NS, 0.0, -36)
# distance: Chubby sits back in S1b (and stays back in S9) -> the show goes 'far' relative to the camera? no: the camera stays with him -> the TV
# is further from US = persp(0.5) from the 'Sit' word on in S1b, near again in S6.
far = np.zeros(NS, np.float32)
tsb = T("i2", "Sit") + 0.15
for a_, b_, d_ in ((tsb, S["S2"], 0.5), (S["S9"], END - 0.8, 0.35)):
    far[int(a_ * SR):int(b_ * SR)] = d_
show_far = persp(show, 0.5)
home = home + show * (1 - far / 0.5 * 0.0) * (far == 0) + show_far * (far > 0)
oldt = (room_tone("tv", NS) * db(-50) + film_crackle(NS) * db(-40)).astype(np.float32)
amb = np.zeros(NS, np.float32)
for sid, st, _ in SHOTLIST:
    en = SEND(sid); a, b = int(st * SR), min(NS, int(en * SR)); kind = PLACE[sid]
    if kind == "tv": seg = home[a:b].copy()
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
    if s[0] in ("S10", "S11"): continue
    if k == "whip": place(whoosh(0.4, level=-25), st - 0.22, 540)
    elif k == "erase": place(eraser(-27), st - 0.02, 540)
    elif k in ("punch", "flash"): place(pop(-26, 700 + 40 * i), st + 0.02, 540)
for sid in ORDER:
    if PLACE[sid] == "board": place(pen_draw(-31, min(1.2, SEND(sid) - S[sid] - 0.2), seed=len(sid) + ORDER.index(sid)), S[sid] + 0.15, 540)

# ---------------- spotting ----------------
TSIT = T("i2", "Sit") - 0.1; T60 = T("a1", "nineteen") - 0.1; TLK = T("a1", "leaked") - 0.1; TREC = T("a2", "recalled") - 0.1
BIG = [TSIT, T60, TLK, TREC]
# S0: mom's yell is the voice-over; the TV show plays (room); a boing on 'TV'
place(boing(-32, 400, 0.25), T("i1", "TV") - 0.1, 200)
# S1: mom's finger wag (tiny whooshes)
for j in range(3): place(whoosh(0.12, peak=0.5, f_lo=1500, f_hi=5000, level=-36), S["S1"] + 0.4 + 0.5 * j, 700)
# S1b: SIT BACK = layered hit + his slide back (scrub on the floor) + a soft flop
layered_hit(TSIT, -22, (100, 50), (300, 2400), 0.5, 1.2); place(scrub(-30, 0.4, 9), TSIT + 0.3, 560); place(soft_flop(-28), TSIT + 0.6, 600)
# S2: NO DAMAGE ding + stamp
place(ding(-25, 1568), T("i3", "won't") - 0.05, 540); place(press(-26), T("i3", "won't") + 0.25, 760)
# S3: the silhouette: a low drone-ish creak; S4 reveal: lamp click + layered hit + crackle
place(creak(-32, 0.6), S["S3"] + 0.2, 540)
place(torch_click(-24), T60 - 0.03, 540); layered_hit(T60, -24, (90, 45), (250, 2000), 0.4, 1.0)
# S4b: radiation: Geiger counter speeding up + a hum, the kid's take (boing), meter needle creak
place(geiger(-27, SEND("S4b") - TLK, 6, 45), TLK, 680); layered_hit(TLK, -23, (80, 40), (200, 2200), 0.5, 1.0)
place(boing(-30, 300, 0.3), TLK + 0.2, 250); place(creak(-30, 0.7), T("a1", "way") - 0.1, 250)
# S5: RECALLED stamp (press + hit), FIXED: a clank, the geiger stops, a ding
place(geiger(-30, T("a2", "fixed,") - S["S5"], 40, 30, seed=2), S["S5"], 540)
layered_hit(TREC, -23, (100, 50), (300, 2400), 0.4, 1.0); place(press(-22), TREC + 0.02, 540)
place(clank(-28, 520), T("a2", "fixed,") - 0.1, 560); place(ding(-26, 1760), T("a2", "fixed,") + 0.15, 560)
# S5b: calendar pages flip, the modern TV pops in with a ding
for j in range(6): place(page_flip(-32), S["S5b"] + 0.15 + 0.16 * j, 300)
place(pop(-26, 1000), T("a2", "don't") - 0.1, 780); place(ding(-27, 2093), T("a2", "don't") + 0.15, 640)
# S6: a yawn-ish sigh (snore, short + soft) on 'tired'
place(snore(-34, 0.8), T("b1", "tired,") + 0.2, 470)
# S6b: the blink = a tiny click; BLINK word drops
place(click(-28) if "click" in globals() else tick(-28), T("b1", "blink.") - 0.02, 560); place(boing(-32, 200, 0.3), T("b1", "blink.") + 0.25, 540)
# S7: book page rustle (kid) + a ding on 'better'
place(page_flip(-30), S["S7"] + 0.3, 280); place(ding(-26, 1568), T("b2", "better") - 0.05, 540)
# S8: the eyeball stretches (stretch), NEARSIGHTED = a soft buzzer
place(stretch(-30) if "stretch" in globals() else creak(-30, 0.6), T("b3", "nearsighted.") - 0.3, 600); place(buzzer(-32, 0.35), T("b3", "nearsighted.") - 0.1, 540)
# S8b: the doctor's pointer taps the chart (ticks), CHECKED ding
for j in range(3): place(tick(-30), S["S8b"] + 0.2 + 0.25 * j, 800)
place(ding(-25, 1318.5), T("b3", "checked.") - 0.05, 540)
# S9: send line: a ding; mom's 'SIT BACK' = a press
place(ding(-25, 2093), T("c1", "Send") + 0.3, 540); place(press(-26), T("c1", "sit") - 0.1, 900)
# S10 logo sting
audio_logo(S["S10"] + 0.02, -18)

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
