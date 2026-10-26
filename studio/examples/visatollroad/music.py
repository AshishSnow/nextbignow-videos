"""Latin salsa score for "Visa never lends you a dollar" (GeneralUser GS): piano montuno, tumbao bass, congas, timbales, cowbell, clave, brass mambo hits."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}




# Salsa / mambo: 2-3 clave, piano montuno, tumbao bass (anticipated), congas tumbao, cowbell, timbale fills, brass section stabs
PZ, BASS, BSN, CLA, VLN, PAD, STR, TIMP, TAIKO, TUBA, GLK, SUB, DR, CEL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9, 13
PROG = {PZ: 0, BASS: 33, BSN: 57, CLA: 56, VLN: 48, PAD: 89, STR: 61, TIMP: 47, TAIKO: 116, TUBA: 57, GLK: 11, SUB: 38, CEL: 8}
VOL = {PZ: 92, BASS: 112, BSN: 90, CLA: 86, VLN: 74, PAD: 50, STR: 94, TIMP: 96, TAIKO: 96, TUBA: 90, GLK: 86, SUB: 100, DR: 100, CEL: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (45, [57, 60, 64, 69]), "F": (41, [57, 60, 65, 69]), "C": (36, [55, 60, 64, 67]), "G": (43, [55, 59, 62, 67]),
      "Em": (40, [55, 59, 64, 67]), "Dm": (38, [57, 62, 65, 69]), "E": (40, [56, 59, 64, 68]), "D7": (38, [54, 57, 60, 62])}
PROGS = {"main": ["Am", "Dm", "G", "C"], "tense": ["Am", "E", "Am", "E"], "money": ["C", "F", "G", "C"]}
BPM = 180   # half-time feel per 2-beat cell: 8 eighths per bar


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; e = beat / 2; b = 0; t = t0
    clave = (0, 3, 6, 10, 12) if b % 2 else (2, 4, 8, 11, 14)
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][(b // 2) % 4]]
        for i in range(8):
            tq = t + i * e
            if tq >= t1 - 0.03: break
            # cowbell on beats, congas tumbao (slaps 2, open tones 4 and 4&)
            if level >= 2: n(tq, DR, 56, 70 if i % 2 == 0 else 52, 0.1)
            if i in (2,): n(tq, DR, 62, 80, 0.1)
            if i in (6, 7): n(tq, DR, 63 if i == 6 else 64, 86, 0.15)
            if i in (0, 4): n(tq, DR, 36, 60 + 8 * level, 0.2)
            # tumbao bass: anticipated '2&' and '4'
            if i == 3: n(tq, BASS, root - 12, 104, e * 2.8)
            if i == 6: n(tq, BASS, root - 12 + 7, 100, e * 1.8)
            # montuno: syncopated broken chord
            pat = [tri[0], tri[2], tri[1], tri[3], tri[1], tri[2], tri[0], tri[3]]
            if i in (0, 1, 3, 4, 6, 7) and level >= 1: n(tq, PZ, pat[i] + 12, 70 + 5 * level, e * 0.8)
        for c in (0, 3, 6) if b % 2 == 0 else (2, 4):
            n(t + c * e, DR, 75, 74, 0.1)            # clave
        if level >= 2:
            for k in tri: n(t, PAD, k, 30 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for k in tri: n(t + 3 * e, STR, k + 12, 92, e * 0.9); n(t + 3 * e, TUBA, k, 82, e * 0.9)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 65, v - 6, 0.3); n(t, DR, 66, v - 10, 0.3); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 33, 112, 1.0); n(t, DR, 57, v - 10, 2.4); n(t, TAIKO, 41, v - 14, 0.8)


def stab(t, chord="Am", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, STR, k + 12, v - 8, d); n(t, TUBA, k, v - 22, d)
    n(t, BSN, root - 12, 100, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 65 if j % 2 else 66, 24 + int(80 * (j / m) ** 1.6), 0.05)
    for i, p in enumerate((57, 60, 64, 69, 72)): n(t_end - dur + i * dur / 5, VLN, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=88):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def lick(t, notes=(76, 79, 81, 84, 81), v=88, step=0.09):
    for i, k in enumerate(notes): n(t + i * step, CLA, k, v, step * 1.4)


def blip(t, notes=(72, 76, 79, 84), v=90, step=0.1):
    for i, k in enumerate(notes): n(t + i * step, GLK, k, v, step * 1.5)


# ---- cues ----
tn = T("i1", "never") - 0.15; th = T("i1", "half") - 0.2
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2); n(0.0, DR, 49, 96, 2.0); stab(0.05, "Am", 104)
hit(tn + 0.25, 112); stab(tn + 0.25, "Dm", 106); hit(th, 120, True); stab(th, "C", 112, 0.5); sparkle(th + 0.05, 88); lick(th + 0.3)
hit(S["S0b"] + 0.02, 110); groove(S["S0b"] + 0.3, S["S1"] - 0.05, "tense", BPM, 1)
hit(T("i2", "loans.") - 0.25, 112); stab(T("i2", "loans.") - 0.25, "Am", 104); hit(T("i2", "interest.") - 0.25, 112); stab(T("i2", "interest.") - 0.25, "E", 106)
riser(T("i2", "trick?") - 0.3, 0.7); hit(T("i2", "trick?") - 0.3, 120, True); stab(T("i2", "trick?") - 0.3, "E", 110, 0.5)
# bank makes card, lends, risk
groove(S["S1"], S["S1b"] - 0.05, "main", BPM, 2); stab(S["S1"] + 0.02, "Am", 104)
stab(T("a1", "doesn't") - 0.2, "Dm", 102); hit(T("a1", "bank") - 0.25, 116, True); stab(T("a1", "bank") - 0.25, "G", 110); blip(T("a1", "bank") - 0.1)
groove(S["S1b"], S["S1c"] - 0.05, "tense", BPM, 2); stab(T("a2", "lends") - 0.2, "Am", 104)
hit(T("a2", "risk") - 0.25, 120, True); stab(T("a2", "risk") - 0.25, "E", 112, 0.5)
groove(S["S1c"], S["S2"] - 0.05, "money", BPM, 2); stab(T("a3", "road") - 0.2, "C", 108); sparkle(T("a3", "road") - 0.1, 88)
# toll road
hit(S["S2"] + 0.02, 112); stab(S["S2"] + 0.02, "F", 108); groove(S["S2"] + 0.3, S["S2b"] - 0.05, "money", BPM, 3)
hit(T("b1", "toll") - 0.2, 116, True); stab(T("b1", "toll") - 0.2, "G", 110); lick(T("b1", "toll"))
groove(S["S2b"], S["S3"] - 0.05, "main", BPM, 2)
hit(T("b2", "banks.") - 0.3, 112); stab(T("b2", "banks.") - 0.3, "Dm", 106); riser(T("b2", "million") - 0.3, 0.9)
hit(T("b2", "million") - 0.3, 120, True); stab(T("b2", "million") - 0.3, "C", 112, 0.5); sparkle(T("b2", "million") - 0.2, 90)
groove(S["S3"], S["S4"] - 0.05, "money", BPM, 3); stab(T("b3", "tiny") - 0.25, "G", 108); blip(T("b3", "tiny") - 0.1, (84, 88, 91, 96))
# multiply -> 257.5B, 8,000/s
hit(S["S4"] + 0.02, 110); groove(S["S4"] + 0.2, S["S4b"] - 0.05, "tense", BPM, 1); riser(T("c1", "billion") - 0.5, 1.3)
hit(T("c1", "billion") - 0.5, 124, True); stab(T("c1", "billion") - 0.5, "Am", 116, 0.6); sparkle(T("c1", "billion") - 0.4, 90)
groove(S["S4b"], S["S5"] - 0.05, "main", BPM, 3); hit(T("c2", "eight") - 0.2, 116, True); stab(T("c2", "eight") - 0.2, "G", 110)
for i in range(6): n(T("c2", "eight") + 0.3 + 0.12 * i, GLK, 79 + 2 * i, 84, 0.2)
groove(S["S5"], S["S6"] - 0.05, "money", BPM, 3); stab(T("c3", "billions…") - 0.2, "F", 106); riser(T("c3", "forty") - 0.2, 0.9)
hit(T("c3", "forty") - 0.2, 124, True); stab(T("c3", "forty") - 0.2, "C", 118, 0.6); sparkle(T("c3", "forty") - 0.1, 90); lick(T("c3", "forty") + 0.2)
# twist: profit
hit(S["S6"] + 0.02, 110); groove(S["S6"] + 0.2, T("d1", "profit.") - 0.45, "tense", BPM, 1); n(S["S6"], SUB, 33, 96, 1.5)
riser(T("d1", "profit.") - 0.4, 0.9); hit(T("d1", "profit.") - 0.4, 126, True); stab(T("d1", "profit.") - 0.4, "C", 118, 0.7)
groove(T("d1", "profit.") + 0.2, S["S7"] - 0.05, "money", BPM, 3); hit(T("d2", "Half") - 0.2, 118); stab(T("d2", "Half") - 0.2, "F", 112); sparkle(T("d2", "Half") - 0.1, 92)
stab(T("d2", "cheap…") - 0.2, "G", 104)
# payoff + outro
hit(S["S7"] + 0.02, 112); groove(S["S7"] + 0.2, S["S8"] - 0.05, "main", BPM, 3)
riser(T("e1", "toll!") - 0.3, 1.0); hit(T("e1", "toll!") - 0.3, 124, True); stab(T("e1", "toll!") - 0.3, "C", 118, 0.6); sparkle(T("e1", "toll!") - 0.2, 90)
groove(S["S8"], END - 1.6, "money", BPM, 3)
for k in CH["C"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, STR, k + 12, 96, 0.8)
n(END - 1.6, BSN, 36, 104, 1.6); hit(END - 1.6, 104); lick(END - 1.5, (76, 79, 81, 84), 90)

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
