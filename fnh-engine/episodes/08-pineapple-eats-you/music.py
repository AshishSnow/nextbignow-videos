"""Tropical calypso / soca score for FreshNestHub "pineapple eats you back" (GeneralUser GS): steel drums, kalimba,
fingered bass, congas, shakers, claves, brass hits; tense minor dub section for the acid/ouch; sizzling grill break; wobbly jelly."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TB0 = T("i1", "it's") - 0.15

STL, BASS, KAL, BRS, PAD, STR, TIMP, TRP, GLK, SUB, DR, CEL, PIZ, WHS = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, 13
PROG = {STL: 114, BASS: 33, KAL: 108, BRS: 61, PAD: 88, STR: 48, TIMP: 47, TRP: 56, GLK: 9, SUB: 38, CEL: 8, PIZ: 45, WHS: 78}
VOL = {STL: 100, BASS: 106, KAL: 86, BRS: 92, PAD: 56, STR: 78, TIMP: 96, TRP: 88, GLK: 84, SUB: 96, DR: 96, CEL: 86, PIZ: 84, WHS: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"F": (41, [65, 69, 72, 77]), "Bb": (46, [65, 70, 74, 77]), "C": (36, [64, 67, 72, 76]), "Dm": (38, [62, 65, 69, 74]),
      "Gm": (43, [62, 67, 70, 74]), "A": (45, [61, 64, 69, 73]), "Am": (45, [60, 64, 69, 72]), "Eb": (39, [63, 67, 70, 75])}
PROGS = {"main": ["F", "Bb", "C", "F"], "sci": ["Dm", "Bb", "F", "C"], "tense": ["Dm", "Dm", "Gm", "A"], "hot": ["Bb", "C", "Dm", "C"]}
BPM = 118
MEL = [0, 2, 1, 2, 3, 2, 1, 0]


def calypso(t0, t1, prog="main", level=2, bpm=BPM):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            if level >= 2:
                n(tq, DR, 36, 92 if q in (0, 2) else 70, 0.2)
                if q in (1, 3): n(tq, DR, 39, 70, 0.1)
                for s_ in range(4): n(tq + s_ * beat / 4, DR, 70, 46 + (12 if s_ == 2 else 0), 0.05)   # maracas 16ths
                n(tq + beat / 2, DR, 63, 72, 0.1); n(tq + beat * 0.75, DR, 64, 60, 0.1)            # conga open/low
            if level >= 1 and q in (0, 1, 3): n(tq + (beat * 0.5 if q == 1 else 0), DR, 75, 66, 0.05)  # claves 3-2-ish
            # bass: 1, and-of-2, 3 (calypso)
            if q == 0: n(tq, BASS, root, 100, beat * 0.8)
            if q == 1: n(tq + beat / 2, BASS, root + 7, 90, beat * 0.4)
            if q == 2: n(tq, BASS, root + 12, 92, beat * 0.4)
            if q == 3: n(tq + beat / 2, BASS, root + 4 if prog == "main" else root + 7, 84, beat * 0.3)
            # steel pan: syncopated 3+3+2 motif from chord tones
            if level >= 1:
                for j, off in enumerate((0, 0.75)):
                    k_ = tri[MEL[(q * 2 + j + b) % 8]] + 12
                    n(tq + off * beat, STL, k_, 76 + 6 * level, beat * 0.5)
            if level >= 3: n(tq + beat * 0.5, KAL, tri[(q + 1) % 4] + 12, 70, beat * 0.3)
        for k in tri[:3]: n(t, PAD, k, 34 + 4 * level, min(bar, t1 - t) * 0.98)
        t += bar; b += 1


def dub(t0, t1, bpm=BPM):
    beat = 60 / bpm; t = t0; i = 0
    while t < t1 - 0.05:
        n(t, DR, 36, 96, 0.3) if i % 2 == 0 else n(t, DR, 40, 84, 0.2)
        n(t + beat / 2, DR, 42, 50, 0.06)
        n(t, SUB, 38 if i % 4 < 2 else 33, 100, beat * 0.9)
        t += beat; i += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.8); n(t, DR, 36, v, 0.3); n(t, TIMP, 41, v - 16, 0.8)
    if big: n(t, SUB, 29, 108, 1.0); n(t, DR, 55, v - 14, 2.0)


def stab(t, chord="F", v=104, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k, v - 12, d); n(t, STR, k, v - 20, d)
    n(t, BASS, root, 104, d)


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def run(t, k0=72, step=2, nn=6, dt=0.045, ch=STL):
    for i in range(nn): n(t + i * dt, ch, k0 + i * step, 86, 0.12)


def timb(t, nn=6):
    for i in range(nn): n(t + i * 0.06, DR, 65 if i % 2 else 66, 70 + i * 6, 0.05)


def fanfare(t, notes=(65, 69, 72, 77), v=96, step=0.12, ch=TRP):
    for i, k in enumerate(notes): n(t + i * step, ch, k, v, step * 1.6)


# ---- cues ----
calypso(0.0, TB0 - 0.02, "main", 1)
for i in range(int(TB0 / 0.42)): n(i * 0.42 + 0.05, KAL, 84 + (i % 3) * 3, 60, 0.15)
hit(TB0, 108, True); stab(TB0, "Dm", 104, 0.5); timb(TB0 - 0.32); run(TB0 + 0.1, 70, -2, 6)
for i in range(4): n(TB0 + 0.35 + i * 0.18, BRS, (62, 62, 65, 62)[i], 84, 0.12)
hit(S["S1"] + 0.02, 110); calypso(S["S1"] + 0.15, S["S2"] - 0.05, "main", 1)
for i in range(8): n(T("i2", "tingly") - 0.1 + i * 0.06, GLK, 88 + (i % 2) * 5, 76, 0.1)
stab(T("i2", "real!") - 0.2, "F", 112); fanfare(T("i2", "real!") - 0.1, (72, 77, 81), 92, 0.1)
# science
calypso(S["S2"], S["S2b"] - 0.05, "sci", 2); sparkle(T("a1", "bromelain.") - 0.2, 84); timb(T("a1", "bromelain.") - 0.5)
calypso(S["S2b"], S["S3"] - 0.05, "sci", 3); stab(T("a1", "protein.") - 0.1, "Bb", 106)
for j in range(3): n(S["S2b"] + 0.35 + 0.25 * j, PIZ, 84 - 3 * j, 96, 0.1)
calypso(S["S3"], S["S3b"] - 0.05, "sci", 1)
for i in range(6): n(S["S3"] + 0.3 + i * 0.4, CEL, (77, 81, 84, 81, 77, 72)[i], 70, 0.4)
calypso(S["S3b"], S["S4"] - 0.05, "sci", 2)
for i in range(8): n(T("a2", "chewing") - 0.3 + i * 0.12, PIZ, 60 + (i % 2) * 3, 92, 0.08)
# acid -> tense dub -> OUCH
dub(S["S4"], S["S4b"] - 0.05)
for k in (62, 65, 69): n(S["S4"], PAD, k, 70, S["S4b"] - S["S4"])
for j in range(5): n(T("a3", "acid") - 0.2 + 0.14 * j + 0.5, GLK, 96 - 2 * j, 80, 0.15)
hit(T("a3", "Ouch!") - 0.15, 126, True); stab(T("a3", "Ouch!") - 0.15, "A", 120, 0.6)
calypso(T("a4", "So") - 0.1, S["S5"] - 0.05, "tense", 1)
hit(S["S5"] + 0.02, 118, True); stab(S["S5"] + 0.02, "Dm", 116, 0.4)
for i in range(6): n(S["S5"] + 0.1 + i * 0.25, BRS, (50, 50, 53, 50, 55, 50)[i], 104, 0.18)
# meat / strong
calypso(S["S6"], S["S7"] - 0.05, "hot", 3); stab(T("b1", "strong,") - 0.15, "Bb", 110)
hit(T("b1", "tender.") - 0.2, 116); fanfare(T("b1", "tender.") - 0.15, (70, 74, 77, 82), 96, 0.11)
# heal / relax
calypso(S["S7"], S["S8"] - 0.05, "main", 1)
for i in range(8): n(T("c1", "fixes") - 0.1 + i * 0.13, CEL, (72, 77, 81, 84, 81, 84, 89, 84)[i], 80, 0.35)
sparkle(T("c1", "fades") - 0.15, 84)
# no sting? -> heat break with whistle
for k in CH["Gm"][1][:3]: n(S["S8"], PAD, k, 66, S["S8b"] - S["S8"])
for i in range(3): n(S["S8"] + 0.3 + i * 0.4, KAL, (74, 77, 79)[i], 84, 0.3)
hit(S["S8b"] + 0.02, 116, True); calypso(S["S8b"] + 0.1, S["S9"] - 0.05, "hot", 2)
n(T("d1", "off.") - 0.25, WHS, 84, 96, 0.2); n(T("d1", "off.") - 0.05, WHS, 77, 96, 0.35); stab(T("d1", "off.") - 0.25, "C", 110)
calypso(S["S9"], S["S10"] - 0.05, "main", 3); fanfare(T("d2", "totally") - 0.15, (72, 76, 79, 84), 96, 0.11)
# jelly
calypso(S["S10"], T("f1", "ruins") - 0.25, "main", 2)
for i in range(8): n(T("f1", "ruins") - 0.2 + i * 0.09, STL, 84 - i * 2, 90 - i * 4, 0.12)
hit(T("f1", "ruins") - 0.2, 118, True); stab(T("f1", "ruins") - 0.2, "Eb", 112, 0.5)
calypso(S["S10b"], S["S10c"] - 0.05, "sci", 2)
for j in range(6): n(T("f2", "breaks") - 0.2 + 0.11 * j, PIZ, 79 - 2 * j, 96, 0.1)
hit(T("f2", "never") - 0.15, 120, True); stab(T("f2", "never") - 0.15, "Dm", 112, 0.5)
for k in (62, 65, 69): n(S["S10c"], PAD, k, 66, S["S11"] - S["S10c"])
calypso(S["S11"], S["S12"] - 0.05, "main", 2)
for i in range(6): n(T("f3", "wobbles") - 0.2 + i * 0.1, KAL, (77, 72, 77, 72, 79, 77)[i], 96, 0.12)
hit(T("f3", "wobbles") - 0.2, 110)
# outro
calypso(S["S12"], END - 1.6, "main", 3)
for k in CH["F"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, BRS, k, 92, 0.8)
n(END - 1.6, BASS, 41, 104, 1.2); hit(END - 1.6, 112, True); run(END - 1.55, 77, 2, 8, 0.05)


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
rng = np.random.default_rng(4); irl = int(1.4 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.3)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.15 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
