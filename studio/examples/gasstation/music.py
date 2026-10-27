"""Surf-rock / rockabilly road-trip score for "Your gas station barely makes money on gas" (GeneralUser GS): twangy clean guitar
tremolo lead, slapback-style rhythm guitar, walking upright-ish bass, organ, train-beat kit, horn stabs on every reveal."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

LEAD, RHY, BASS, ORG, BRS, GLK, SUB, MUT, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {LEAD: 27, RHY: 28, BASS: 33, ORG: 16, BRS: 61, GLK: 9, SUB: 38, MUT: 28}
VOL = {LEAD: 74, RHY: 66, BASS: 104, ORG: 46, BRS: 84, GLK: 84, SUB: 100, MUT: 60, DR: 100}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"E": (40, [56, 59, 64]), "A": (45, [57, 61, 64]), "B": (47, [59, 63, 66]), "C#m": (49, [56, 61, 64]),
      "G": (43, [55, 59, 62]), "D": (38, [57, 62, 66]), "Em": (40, [55, 59, 64])}
PROGS = {"main": ["E", "E", "A", "B"], "cruise": ["E", "A", "E", "B"], "tense": ["Em", "G", "Em", "D"], "win": ["A", "B", "E", "E"]}
BPM = 150
MEL = {"main": [64, 67, 68, 71, 68, 67, 64, 62], "cruise": [71, 68, 66, 64, 66, 68, 71, 73], "win": [64, 68, 71, 76, 75, 71, 73, 76],
       "tense": [64, 66, 67, 66, 64, 62, 64, 59]}


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    """train beat: kick on 1&3, snare backbeat, 8th-note hats/brush; walking bass; muted-guitar chug; organ pad; tremolo lead at level 3"""
    beat = 60 / bpm; bar = 4 * beat; e8 = beat / 2; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        walk = [root, root + 4, root + 7, root + 9, root + 12, root + 9, root + 7, root + 4]
        for i in range(8):
            tq = t + i * e8
            if tq >= t1 - 0.03: break
            if i in (0, 4): n(tq, DR, 36, 98 if level >= 2 else 82, 0.1)
            if i in (2, 6) and level >= 1: n(tq, DR, 38, 90, 0.1)
            if level >= 2: n(tq, DR, 42 if i % 2 else 44, 50 + 10 * (i % 2 == 0), 0.05)
            n(tq, BASS, walk[i] - 12, 96, e8 * 0.9)
            if level >= 1: n(tq, MUT, tri[i % 3] - 12 + (12 if i % 4 == 3 else 0), 58 + 6 * level, e8 * 0.45)
        if level >= 2:
            for k in tri: n(t, ORG, k, 36, min(bar, t1 - t) * 0.98)
        if level >= 3:
            mel = MEL.get(prog, MEL["main"])
            for j, k in enumerate(mel):
                for r in range(4):   # surf tremolo picking
                    tq = t + j * e8 + r * e8 / 4
                    if tq < t1 - 0.05: n(tq, LEAD, k, 66 - 6 * r, e8 / 4.2)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.6); n(t, DR, 36, v, 0.2); n(t, DR, 38, v - 14, 0.2)
    if big: n(t, SUB, 28, 112, 0.8); n(t, DR, 57, v - 16, 2.0)


def stab(t, chord="E", v=104, d=0.25):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k + 12, v - 18, d); n(t, RHY, k, v - 26, d)
    n(t, BASS, root - 12, 104, d)


def twang(t, base=64, v=100):   # guitar slide-up lick
    for i, k in enumerate((base - 5, base - 3, base, base + 3, base + 4)): n(t + i * 0.055, LEAD, k, v, 0.08 if i < 4 else 0.5)


def bell(t, v=96, k=88):
    n(t, GLK, k, v, 0.4); n(t + 0.08, GLK, k + 7, v - 10, 0.5)


def riser(t_end, dur):
    m = int(dur / 0.05)
    for j in range(m): n(t_end - dur + j * 0.05, LEAD, 52 + int(24 * j / m), 30 + int(70 * (j / m)), 0.045)
    for j in range(int(dur / 0.1)): n(t_end - dur + j * 0.1, DR, 38, 30 + int(70 * j / (dur / 0.1)), 0.05)


def drumroll(t0, dur):
    for j in range(int(dur / 0.06)): n(t0 + j * 0.06, DR, 38, 40 + int(60 * j * 0.06 / dur), 0.04)


# ---- cues ----
tm = T("i1", "money…") - 0.15; tg = T("i1", "gas?") - 0.2
groove(0.0, S["S1"] - 0.05, "main", 2); stab(0.02, "E", 104); n(0.0, DR, 49, 92, 1.6)
bell(tm, 92); stab(tg, "B", 108); hit(tg, 112)
hit(S["S1"] + 0.02, 108); groove(S["S1"] + 0.1, S["S1b"] - 0.05, "cruise", 1)
for j in range(8): n(S["S1"] + 0.06 * 2 * j, GLK, 76 + (j % 4) * 3, 70, 0.1)
tf = T("i2", "forty") - 0.25
groove(S["S1b"], tf - 0.05, "tense", 1); riser(tf, 0.6); hit(tf, 120, True); stab(tf, "E", 112, 0.5); bell(tf + 0.1, 100)
groove(tf + 0.4, S["S2"] - 0.05, "main", 1)
ts6 = T("a1", "six") - 0.25
groove(S["S2"], ts6 - 0.05, "cruise", 2); hit(ts6, 118, True); stab(ts6, "A", 110, 0.4); twang(ts6 + 0.1, 64)
groove(ts6 + 0.35, S["S3"] - 0.05, "cruise", 1)
tl = T("a2", "Look") - 0.15
groove(S["S3"], S["S4"] - 0.05, "tense", 1); stab(tl, "G", 104); bell(tl + 0.2, 90, 84)
tt = T("a3", "ten") - 0.25; ti = T("a3", "inside") - 0.5
groove(S["S4"], S["S5"] - 0.05, "main", 2); hit(tt, 112); stab(tt, "E", 106); stab(ti, "A", 104)
tw = T("a4", "twice") - 0.25
hit(S["S5"] + 0.02, 108); drumroll(S["S5"] + 0.1, max(0.3, tw - S["S5"] - 0.15)); hit(tw, 124, True); stab(tw, "E", 114, 0.6); twang(tw + 0.1, 69)
groove(tw + 0.4, S["S6"] - 0.05, "win", 2)
t14 = T("b1", "fourteen") - 0.25; t42 = T("b2", "Forty") - 0.25; t59 = T("b3", "fifty") - 0.25
groove(S["S6"], S["S7"] - 0.05, "main", 2); hit(t14, 112); stab(t14, "B", 104); bell(t14 + 0.1, 80, 79)
groove(S["S7"], S["S8"] - 0.05, "main", 2); hit(t42, 116); stab(t42, "A", 108); bell(t42 + 0.1, 92, 84)
groove(S["S8"], t59 - 0.05, "cruise", 2); riser(t59, 0.7); hit(t59, 124, True); stab(t59, "E", 114, 0.6); bell(t59 + 0.1, 100, 88); twang(t59 + 0.2, 71)
groove(t59 + 0.4, S["S9"] - 0.05, "win", 3)
t5 = T("c1", "fifth") - 0.25
hit(S["S9"] + 0.02, 110); groove(S["S9"] + 0.1, t5 - 0.05, "tense", 1); drumroll(t5 - 0.8, 0.75); hit(t5, 124, True); stab(t5, "E", 114, 0.6)
groove(t5 + 0.3, S["S10"] - 0.05, "win", 3)
# re-hook: stop, drumroll under the curtain, big reveal
tgi = T("c2", "giant") - 0.2
hit(S["S10"] + 0.02, 108); stab(S["S10"] + 0.02, "Em", 104, 0.6); drumroll(S["S10"] + 0.5, max(0.4, tgi - S["S10"] - 0.55)); hit(tgi, 126, True); stab(tgi, "E", 116, 0.7); twang(tgi + 0.15, 64)
groove(tgi + 0.5, S["S11"] - 0.05, "main", 2)
groove(S["S11"], S["S11b"] - 0.05, "cruise", 3)
groove(S["S11b"], S["S12"] - 0.05, "main", 2)
for j in range(5): bell(S["S11b"] + 0.12 + 0.18 * j, 76, 84 + j * 2)
t6 = T("d1", "sixty") - 0.3; tu = T("d1", "under") - 0.25
hit(S["S12"] + 0.02, 108); groove(S["S12"] + 0.1, tu - 0.05, "tense", 1); stab(t6, "Em", 104); hit(tu, 122, True); stab(tu, "D", 112, 0.5)
groove(tu + 0.3, S["S13"] - 0.05, "tense", 2)
tp = T("d2", "pay") - 0.2
groove(S["S13"], S["S13b"] - 0.05, "cruise", 2); stab(tp, "A", 106); bell(tp + 0.55, 96, 88)
groove(S["S13b"], S["S14"] - 0.05, "main", 1)
for j in range(8): n(S["S13b"] + 0.25 * j, GLK, 76 + (j % 4) * 2, 58, 0.12)
tsn = T("e1", "snack") - 0.2; tgs = T("e1", "giant") - 0.2
hit(S["S14"] + 0.02, 108); groove(S["S14"] + 0.1, S["S14b"] - 0.05, "tense", 1)
hit(S["S14b"] + 0.02, 116, True); stab(S["S14b"] + 0.02, "A", 110, 0.5); groove(S["S14b"] + 0.3, tgs - 0.05, "win", 2)
hit(tgs, 120, True); stab(tgs, "E", 112, 0.5); twang(tgs + 0.1, 64)
hit(S["S15"] + 0.02, 110); groove(S["S15"] + 0.1, END - 1.6, "win", 3)
for k in CH["E"][1]: n(END - 1.6, ORG, k, 70, 2.0); n(END - 1.6, BRS, k + 12, 90, 0.8)
n(END - 1.6, BASS, 28, 104, 1.6); hit(END - 1.6, 104); twang(END - 1.5, 64, 92)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = np.zeros((int((END + 3) * SR), 2), np.float32)
cuts = sorted(set([0.0] + [S[k] for k in S if k != "S0"] + [END + 3]))
evs = sorted(ev)
for a, b in zip(cuts[:-1], cuts[1:]):
    part = render([e for e in evs if a - 0.01 <= e[0] < b - 0.01], END)
    nb = int(b * SR); tail = int(0.22 * SR)
    if nb < len(part): part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]
rng = np.random.default_rng(4); irl = int(1.6 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.35)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
