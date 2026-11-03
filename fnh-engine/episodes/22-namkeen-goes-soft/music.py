"""INDO-DISCO score for FreshNestHub 22 "why does namkeen go soft?" (GeneralUser GS): a 1970s filmi disco at 111 bpm (one beat = one walk step): four-on-the-floor kick, octave slap bass, off-beat hats, bongos standing in for tabla,
sitar riff, string stabs, wah Rhodes. New genre for the channel. The BACKBEAT is food: mix.py lays a real CRUNCH on beats 2 and 4 while the snack is crisp and a SOGGY thud once it has gone soft; the oven brings the crunch back.
The score FOLLOWS THE STORY: the band locks to Chubby's footsteps and SAGS (tape stop) when the chakli flops; thin bass + bongos under explanations; celesta drops for water; a dark drone for the trap; the full band returns for the fixes."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
SIT, BAS, STR, RHO, BRS, CEL, FLU, TBN, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {SIT: 104, BAS: 36, STR: 48, RHO: 4, BRS: 61, CEL: 8, FLU: 73, TBN: 57}
VOL = {SIT: 86, BAS: 108, STR: 74, RHO: 78, BRS: 80, CEL: 90, FLU: 76, TBN: 84, DR: 74}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 0.54
CH = {"Dm": (38, [62, 65, 69]), "Bb": (34, [62, 65, 70]), "C": (36, [60, 64, 67]), "A7": (33, [61, 64, 67]), "Gm": (31, [62, 67, 70]), "F": (29, [60, 65, 69]), "Am": (33, [60, 64, 69]), "D": (38, [62, 66, 69]), "G": (31, [62, 67, 71])}
PROGS = {"main": ["Dm", "Bb", "C", "A7"], "bright": ["F", "C", "Dm", "Bb"], "tense": ["Dm", "Gm", "Dm", "A7"], "up": ["G", "D", "F", "C"]}
SITAR = [(0, 74), (0.5, 77), (1, 76), (1.5, 74), (2, 69), (3, 72), (3.5, 74)]


def disco(t0, t1, prog="main", level=2):
    """1: bass + bongos only (voice first). 2: + kick, hats, soft Rhodes. 3: + strings, sitar riff, brass."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * BEAT
            if tq >= t1 - 0.05: break
            n(tq, BAS, root + (12 if q % 2 else 0), 104 if q == 0 else 92, BEAT * 0.42); n(tq + BEAT * 0.5, BAS, root + (0 if q % 2 else 12), 86, BEAT * 0.3)
            n(tq + BEAT * 0.5, DR, 61, 62, 0.08); n(tq + BEAT * 0.75, DR, 60, 50, 0.06)
            if level >= 2:
                n(tq, DR, 36, 100, 0.1); n(tq + BEAT * 0.5, DR, 46, 58, 0.12)
                if q % 2: 
                    for k in vo: n(tq + BEAT * 0.5, RHO, k, 58, BEAT * 0.3)
        if level >= 3:
            for k in vo: n(t, STR, k + 12, 70, BEAT * 1.5); n(t + BEAT * 2.5, STR, k + 12, 62, BEAT * 0.5)
            if b % 2 == 0:
                for off, k in SITAR: n(t + off * BEAT, SIT, k + (root - 38 if b % 4 == 2 else 0), 92, BEAT * 0.45)
        t += 4 * BEAT; b += 1


def hit(t, chord="Dm", v=112, d=0.5):
    root, vo = CH[chord]
    n(t, BAS, root, v, d); n(t, DR, 49, v - 12, 0.3); n(t, DR, 36, v, 0.1)
    for k in vo: n(t, BRS, k + 12, v - 4, d); n(t, STR, k + 24, v - 20, d)


def bells(t, base=84, nn=6, v=82, ch=CEL):
    for j in range(nn): n(t + j * 0.07, ch, base + (0, 3, 7, 10, 12, 15, 19)[j % 7], v, 0.3)


def drip(t0, t1, gap=0.27, v=84):
    t = t0; j = 0; mel = [84, 88, 86, 91, 84, 93]
    while t < t1: n(t, CEL, mel[j % 6], v, 0.2); t += gap; j += 1


def slide(t, k0=55, up=True, nn=7, d=0.05, ch=TBN):
    for j in range(nn): n(t + j * d, ch, k0 + (j if up else -j), 88, d * 1.4)


SLOW = []
# ---- hook: the band is locked to his feet; it sags when the chakli flops
ts = T("i1", "soft") - 0.25
disco(0.0, ts + 0.05, "main", 3); SLOW.append((ts - 0.02, 0.8))
n(ts + 0.2, TBN, 50, 96, 0.5); slide(ts + 0.12, 58, False, 9, 0.05)
# not old / drinking
for j in range(4): n(S["S1"] + j * 0.27, DR, 76, 58, 0.05)
n(S["S1"], SIT, 62, 74, 0.4)
disco(S["S1b"], S["S2"], "bright", 1); drip(T("i2", "drinking") - 0.1, S["S2"], 0.2)
disco(S["S2"], S["S3"], "tense", 1); hit(T("i3", "opposite") - 0.1, "Bb", 106, 0.3)
# fried / crunch / thirsty
disco(S["S3"], S["S4"], "main", 1); hit(T("a2", "crunch") - 0.2, "Dm", 114, 0.25); disco(T("a2", "crunch") + 0.1, S["S4b"], "main", 2)
n(S["S4b"], SIT, 62, 76, 1.2); n(S["S4b"] + 0.02, STR, 50, 58, S["S5"] - S["S4b"]); hit(T("a2", "thirsty") - 0.1, "Gm", 96, 0.3)
# the air is full of water
disco(S["S5"], S["S6"], "bright", 1); bells(T("a3", "full") - 0.1, 84, 7, 90)
disco(S["S6"], S["S7"], "bright", 1); slide(T("a4", "more") - 0.05, 60, False, 8, 0.08, FLU)
# the thirst meter: he walks on, band falls in on his feet
disco(S["S7"], S["S7b"], "up", 2); hit(T("b1", "meter") - 0.1, "G", 104, 0.3); disco(S["S7b"], S["S8"], "up", 1)
n(T("b2", "three") - 0.2, CEL, 72, 92, 0.3); n(T("b2", "seven") - 0.2, CEL, 84, 92, 0.3); disco(S["S8"], S["S9"], "up", 1)
# lid off: strings climb, drops
disco(S["S9"], S["S10"], "tense", 2)
for j in range(10): n(T("b3", "lid") - 0.1 + j * 0.12, STR, 62 + j, 72, 0.14)
drip(T("b3", "lid") + 0.2, S["S10"], 0.14, 80); hit(T("b3", "one") - 0.1, "A7", 112, 0.4)
disco(S["S10"], S["S11"], "bright", 1)
# the kill: band out, one drop
n(S["S11"], STR, 50, 54, S["S12"] - S["S11"]); n(S["S11"], STR, 57, 48, S["S12"] - S["S11"]); n(T("c1", "kill") - 0.3, CEL, 91, 104, 0.4); hit(T("c1", "kill") - 0.1, "Dm", 98, 0.35)
# spaghetti
for j in range(3): n(S["S12"] + j * 0.27, DR, 61, 70, 0.06)
hit(T("c2", "snaps") - 0.12, "Dm", 116, 0.2); slide(T("c2", "bends") - 0.2, 62, False, 12, 0.06)
disco(S["S12c"], S["S13"], "main", 1); bells(T("c2", "water") - 0.12, 79, 6, 88)
# glass -> rubber: thin celesta, then a boingy bass
disco(S["S13"], S["S13b"], "tense", 1); hit(T("c3", "like"), "Gm", 96, 0.2); bells(T("c3", "like") + 0.05, 96, 5, 82); disco(S["S13b"] + 0.3, S["S14"], "tense", 1)
disco(S["S14"], S["S14b"], "bright", 1); drip(S["S14"] + 0.2, T("c4", "loosens"), 0.2)
slide(T("c4", "rubbery") - 0.2, 40, True, 10, 0.04, BAS); slide(T("c4", "rubbery") + 0.2, 50, False, 10, 0.04, BAS)
disco(S["S15"], T("c5", "No") - 0.1, "tense", 1); hit(T("c5", "crunch") - 0.12, "Dm", 100, 0.5); SLOW.append((T("c5", "crunch") + 0.1, 0.6))
# two steps: bass + feet
disco(S["S16"], S["S17"], "tense", 1); hit(T("d1", "rejected") - 0.1, "A7", 106, 0.3)
n(S["S17"], STR, 50, 54, S["S18"] - S["S17"]); ts17 = T("d2", "only") - 0.05
n(ts17, BAS, 38, 112, 0.25); n(ts17 + 0.54, BAS, 41, 112, 0.25); hit(ts17 + 1.08, "Dm", 110, 0.4)
# the trap: drone + sitar
n(S["S18"], STR, 38, 66, S["S19"] - S["S18"]); n(S["S18"], STR, 45, 56, S["S19"] - S["S18"]); hit(T("e1", "trap") - 0.1, "Dm", 110, 0.5)
for off, k in SITAR[:5]: n(T("e1", "Diwali") + off * 0.25, SIT, k, 84, 0.2)
disco(S["S19"], S["S20"], "bright", 1); disco(S["S20"], S["S21"], "tense", 1); drip(S["S20b"], S["S21"], 0.27, 74)
disco(S["S21"], T("e4", "closed") + 0.1, "tense", 1); hit(T("e4", "closed") + 0.25, "A7", 110, 0.5); n(T("e4", "closed") + 0.4, STR, 45, 58, S["S22"] - T("e4", "closed") - 0.4)
# the fixes: the band comes back
hit(T("f1", "three") - 0.1, "F", 112, 0.3); disco(T("f1", "three") + 0.25, S["S22b"], "bright", 2); disco(S["S22b"], S["S23"], "bright", 2); disco(S["S23"], S["S24"], "bright", 2)
n(S["S24"], STR, 53, 56, S["S24b"] - S["S24"]); hit(T("f3", "dont") - 0.1, "C", 104, 0.3)
disco(S["S24b"], S["S25"], "up", 1); disco(S["S25"], S["S25b"], "up", 2)
for j in range(9): n(S["S25"] + j * 0.2, STR, 62 + j * 2, 70, 0.22)
disco(S["S25b"], S["S26"], "bright", 1)
disco(S["S26"], S["S26b"], "tense", 1); n(S["S26b"], STR, 50, 50, S["S26d"] - S["S26b"]); n(S["S26b"], STR, 51, 44, S["S26d"] - S["S26b"])
hit(T("g1", "bin") - 0.12, "Dm", 110, 0.4)
disco(S["S27"], S["S28"], "bright", 3)
for w, k in (("lid", 72), ("sweets", 76), ("heat", 84)): n(T("h1", w) - 0.2, CEL, k, 104, 0.5)
disco(S["S28"], END - 1.8, "main", 3); hit(END - 1.8, "Dm", 116, 1.6); bells(END - 1.75, 84, 7, 92)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((SIT, 44), (BAS, 64), (STR, 70), (RHO, 84), (BRS, 56), (CEL, 90), (FLU, 40), (TBN, 76)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = render(sorted(ev), END)


def ritard(x, t0, dur, floor=0.4):
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = 1 - (1 - floor) * np.linspace(0, 1, L) ** 1.4
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.1, L)[:, None]
    x[i0:i0 + L] = seg


for t0, d in SLOW: ritard(mus, t0, d)
mus = signal.sosfilt(signal.butter(2, 10000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
