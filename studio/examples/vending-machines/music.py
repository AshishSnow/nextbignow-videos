"""Funk / clavinet score for HOW TO START ep 2, vending machines (GeneralUser GS): clavinet 16ths, slap bass, brass stabs, dusty organ half-time for the 1998 flashback."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
CLV, BASS, BRS, GLK, PAD, EP, ORG, GTR, SUB, LEAD, TSX, KAL, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {CLV: 7, BASS: 36, BRS: 61, GLK: 9, PAD: 89, EP: 4, ORG: 17, GTR: 28, SUB: 38, LEAD: 80, TSX: 66, KAL: 108}
VOL = {CLV: 92, BASS: 104, BRS: 88, GLK: 82, PAD: 60, EP: 80, ORG: 74, GTR: 76, SUB: 100, LEAD: 66, TSX: 80, KAL: 88, DR: 98}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# funk in E minor (Em9 - A9 vamp), lift to G - A, flashback in D minor organ (new genre for the channel)
CH = {"Em": (40, [62, 67, 71, 74]), "A": (45, [61, 64, 67, 71]), "G": (43, [62, 66, 71, 74]), "D": (38, [62, 66, 69, 72]),
      "Dm": (38, [62, 65, 69, 72]), "Bb": (46, [62, 65, 70, 74]), "C": (36, [64, 67, 70, 74]), "B7": (47, [63, 66, 69, 71])}
PROGS = {"main": ["Em", "Em", "A", "A"], "lift": ["G", "A", "Em", "B7"], "dark": ["Dm", "Bb", "Dm", "C"], "end": ["G", "A", "Em", "Em"]}
BPM = 100
BASSPAT = [0, None, 12, 0, None, 0, 10, None, 0, None, 12, None, 7, None, 10, 12]
CLVPAT = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0]


def groove(t0, t1, prog="main", level=2):
    beat = 60 / BPM; s16 = beat / 4; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for i in range(16):
            tq = t + i * s16 + (0.018 if i % 2 else 0)        # light swing
            if tq >= t1 - 0.03: break
            if i % 4 == 0 and level >= 1: n(tq, DR, 36, 100 if i in (0, 8) else 80, 0.2)
            if i in (4, 12) and level >= 1: n(tq, DR, 38, 92, 0.15)
            if level >= 2: n(tq, DR, 42, 60 if i % 2 else 72, 0.05)
            bp = BASSPAT[i]
            if bp is not None: n(tq, BASS, root - 12 + bp, 100 if i % 4 == 0 else 84, s16 * 0.8)
            if CLVPAT[i] and level >= 1:
                for k in tri[:3]: n(tq, CLV, k, 74 + 6 * level, s16 * 0.55)
            if level >= 3 and i in (6, 14): n(tq, GTR, tri[1] - 12, 70, s16 * 0.5)
        for k in tri: n(t, EP, k - 12, 40 + 4 * level, bar * 0.9)
        t += bar; b += 1


def dark(t0, t1):
    beat = 60 / BPM * 2; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS["dark"][b % 4]]
        n(t, SUB, root - 12, 96, beat * 1.8); n(t, DR, 36, 100, 0.3); n(t + beat, DR, 38, 76, 0.2)
        for k in tri: n(t, ORG, k - 12, 66, beat * 1.9)
        for j in range(4): n(t + j * beat * 0.5, DR, 42, 50, 0.05)
        t += beat * 2; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 16, 1.8); n(t, DR, 36, v, 0.3); n(t, DR, 38, v - 10, 0.2)
    if big: n(t, SUB, 28, 110, 1.2); n(t, DR, 57, v - 10, 2.2)


def stab(t, chord="Em", v=104, d=0.25):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k, v - 6, d); n(t, TSX, k - 12, v - 20, d)
    n(t, BASS, root - 12, 100, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 38, 20 + int(78 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((64, 66, 67, 69, 71, 74)): n(t_end - dur + i * dur / 6, BRS, p, 44 + 8 * i, t_end - (t_end - dur + i * dur / 6))


def sparkle(t, base=83):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.06, GLK, k, 88, 0.5)


# ---- cues ----
for k in CH["Em"][1]: n(0.0, EP, k - 12, 60, S["S1"]); n(0.0, CLV, k, 90, 0.2)
stab(0.0, "Em", 108); n(0.0, BASS, 28, 96, 0.8)
groove(0.6, S["S2"] - 0.05, "main", 2)
tk = Tw("i3", "thousand", -0.25); stab(tk, "A", 110); sparkle(tk + 0.1, 86)
groove(S["S2"] + 0.2, S["S4"] - 0.75, "lift", 2)
hit(Tw("i4", "thousands.", -0.1), 112, True); stab(Tw("i4", "thousands.", -0.1), "B7", 110, 0.5)
for sid, ch in (("S4", "Em"), ("S7", "G"), ("S9", "A"), ("S12", "B7")):
    riser(S[sid], 0.7); stab(S[sid] + 0.02, ch, 112); n(S[sid] + 0.1, KAL, 88, 96, 0.4)
groove(S["S4"] + 0.3, S["S7"] - 0.75, "main", 3)
for w_ in ("morning,", "lunch", "evening."): n(Tw("a2", w_, -0.05), KAL, 83, 96, 0.4)
groove(S["S7"] + 0.3, S["S9"] - 0.75, "lift", 2)
stab(Tw("b2", "check", -0.1), "G", 106); sparkle(Tw("b2", "insurance.", -0.2), 86)
groove(S["S9"] + 0.3, S["S12"] - 0.75, "main", 3)
stab(Tw("c2", "few", -0.2), "A", 104)
for w_ in ("coin", "bill", "cooler"): n(Tw("c3", w_, 0.0), GLK, 88, 90, 0.3)
groove(S["S12"] + 0.3, S["S13"] - 0.05, "lift", 1)
dark(S["S13"] + 0.05, S["S16"] - 0.05)
hit(Tw("e3", "forty", -0.2), 116, True)
hit(Tw("e4", "charged", -0.2), 100)
groove(S["S16"] + 0.15, S["S17"] - 0.05, "main", 2)
sparkle(Tw("e5", "week", -0.1), 86)
dark(S["S17"], S["S18"] - 0.05); hit(Tw("t1", "singers,", -0.15), 118, True); stab(Tw("t1", "singers,", -0.15), "Bb", 110, 0.5)
stab(S["S18"] + 0.02, "Em", 112); groove(S["S18"] + 0.3, S["S19"] - 0.05, "main", 3)
groove(S["S19"], END - 1.4, "end", 3)
for k in CH["Em"][1]: n(END - 1.4, CLV, k, 96, 0.3); n(END - 1.4, EP, k - 12, 70, 1.6); n(END - 1.4, BRS, k, 100, 0.5)
n(END - 1.4, BASS, 28, 104, 1.4); hit(END - 1.4, 100); sparkle(END - 1.3, 83)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S1", "S2", "S4", "S7", "S9", "S12", "S13", "S16", "S19")] + [END + 3]))
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
