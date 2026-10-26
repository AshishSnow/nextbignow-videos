"""Bouncy food-funk score for FreshNestHub "carrots turn your skin orange" (GeneralUser GS): marimba hook, slap bass,
pizzicato, clavinet, brass hits; a 1940s military snare + brass fanfare section for the WWII radar twist."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TO0 = T("i1", "orange?") - 0.25

MAR, BASS, PIZ, CLAV, BRS, PAD, STR, TIMP, TRP, GLK, SUB, DR, CEL, HORN = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9, 12, 13
PROG = {MAR: 12, BASS: 36, PIZ: 45, CLAV: 7, BRS: 61, PAD: 89, STR: 48, TIMP: 47, TRP: 56, GLK: 9, SUB: 39, CEL: 8, HORN: 60}
VOL = {MAR: 96, BASS: 104, PIZ: 88, CLAV: 74, BRS: 92, PAD: 60, STR: 80, TIMP: 98, TRP: 88, GLK: 84, SUB: 96, DR: 94, CEL: 86, HORN: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67, 72]), "Am": (33, [57, 60, 64, 69]), "F": (41, [57, 60, 65, 69]), "G": (43, [55, 59, 62, 67]),
      "Dm": (38, [57, 62, 65, 69]), "E": (40, [56, 59, 64, 68]), "Bb": (34, [58, 62, 65, 70]), "Cm": (36, [55, 60, 63, 67])}
PROGS = {"main": ["C", "Am", "F", "G"], "sci": ["F", "G", "Am", "C"], "warn": ["Am", "Dm", "E", "Am"], "war": ["Cm", "Bb", "Cm", "G"]}
BPM = 112


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            if level >= 2:
                if q in (0, 2): n(tq, DR, 36, 96, 0.2)
                if q % 2 == 1: n(tq, DR, 38, 84, 0.15); n(tq, DR, 39, 60, 0.1)
                n(tq + beat / 2, DR, 42, 56, 0.08)
            # slap bass: root + octave pop syncopation
            n(tq, BASS, root, 96, beat * 0.3)
            if q % 2 == 1: n(tq + beat * 0.75, BASS, root + 12, 90, beat * 0.2)
            # marimba hook
            hook = [tri[0], tri[2], tri[1], tri[3]]
            if level >= 1: n(tq + beat / 2, MAR, hook[q] + 12, 72 + 6 * level, beat * 0.4)
            if level >= 3: n(tq, MAR, hook[(q + 2) % 4] + 12, 70, beat * 0.3); n(tq + beat * 0.25, CLAV, tri[1], 60, beat * 0.15)
        for k in tri[:3]: n(t, PAD, k, 38 + 5 * level, min(bar, t1 - t) * 0.98)
        t += bar; b += 1


def march(t0, t1, bpm=104):
    beat = 60 / bpm; t = t0; i = 0
    while t < t1 - 0.05:
        n(t, DR, 38, 92 if i % 4 == 0 else 70, 0.1)
        n(t + beat / 2, DR, 38, 56, 0.08); n(t + beat * 0.75, DR, 38, 50, 0.06)
        if i % 2 == 0: n(t, DR, 36, 90, 0.2); n(t, TIMP, 36, 70, 0.4)
        t += beat; i += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.8); n(t, DR, 36, v, 0.3); n(t, TIMP, 36, v - 16, 0.8)
    if big: n(t, SUB, 24, 108, 1.0); n(t, DR, 57, v - 14, 2.0)


def stab(t, chord="C", v=104, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k, v - 12, d); n(t, STR, k + 12, v - 18, d)
    n(t, BASS, root, 104, d)


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def boing(t, k0=60):
    for i in range(6): n(t + i * 0.04, MAR, k0 + i * 2, 90 - i * 6, 0.1)


def fanfare(t, notes=(60, 67, 72, 67, 72, 76), v=96, step=0.13, ch=TRP):
    for i, k in enumerate(notes): n(t + i * step, ch, k, v, step * 1.6)


def pizz(t0, t1, notes, step):
    t = t0; i = 0
    while t < t1 - 0.05: n(t, PIZ, notes[i % len(notes)], 86, step * 0.8); t += step; i += 1


# ---- cues ----
groove(0.0, TO0 - 0.02, "main", BPM, 2)
for i in range(int(TO0 / 0.42)): n(i * 0.42 + 0.05, GLK, 84 + (i % 3) * 3, 70, 0.15)
hit(TO0, 122, True); stab(TO0, "F", 116, 0.5); sparkle(TO0 + 0.05, 84); boing(TO0 + 0.25, 64)
hit(S["S0b"] + 0.02, 112); groove(S["S0b"] + 0.2, S["S1"] - 0.05, "main", BPM, 2)
stab(T("i2", "real.") - 0.2, "C", 112); fanfare(T("i2", "real.") - 0.1, (72, 76, 79), 92, 0.1)
# science section
groove(S["S1"], S["S2"] - 0.05, "sci", BPM, 2); sparkle(T("a1", "beta-carotene.") - 0.2, 86); stab(T("a1", "The") - 0.1, "Am", 102)
groove(S["S2"], S["S3"] - 0.05, "sci", BPM, 3); stab(T("a2", "vitamin") - 0.15, "F", 104)
hit(T("a2", "limit.") - 0.2, 120, True); stab(T("a2", "limit.") - 0.2, "E", 114, 0.5)
pizz(S["S3"], S["S3b"] - 0.05, (60, 64, 67, 64), 60 / BPM / 2); groove(S["S3"], S["S3b"] - 0.05, "sci", BPM, 1)
groove(S["S3b"], S["S4a"] - 0.05, "sci", BPM, 2)
for i in range(10): n(T("a3", "settles") - 0.1 + i * 0.12, GLK, 72 + i, 74, 0.2)
# palms / feet / nose — three rising hits
hit(S["S4a"] + 0.02, 110); groove(S["S4a"] + 0.1, S["S5"] - 0.05, "main", BPM, 3)
stab(T("b1", "palms") - 0.1, "C", 110); sparkle(T("b1", "palms"), 84)
stab(T("b1", "feet...") - 0.1, "F", 112); sparkle(T("b1", "feet..."), 88)
hit(T("b1", "nose!") - 0.15, 122, True); stab(T("b1", "nose!") - 0.15, "G", 116); boing(T("b1", "nose!") - 0.05, 67)
# how many
groove(S["S5"], S["S6"] - 0.05, "main", BPM, 2); stab(T("c1", "many") - 0.1, "Am", 104)
for i in range(10): n(T("c1", "ten") - 0.15 + 0.05 * i, MAR, 72 + i, 86, 0.12)
hit(T("c1", "ten") - 0.15, 118, True); stab(T("c1", "weeks.") - 0.25, "F", 108)
# babies (lullaby-ish)
for i, k in enumerate((84, 79, 76, 79, 84, 88, 84, 79)): n(S["S6"] + 0.1 + i * 0.36, CEL, k, 84, 0.4)
for k in CH["F"][1][:3]: n(S["S6"], PAD, k, 66, S["S7"] - S["S6"])
# good news / fades
hit(S["S7"] + 0.02, 112); groove(S["S7"] + 0.1, S["S8"] - 0.05, "main", BPM, 2); fanfare(T("d1", "harmless.") - 0.15, (72, 76, 79, 84), 94, 0.11)
for k in (84, 81, 79, 76, 72): n(T("d1", "fades.") - 0.6 + (84 - k) * 0.06, CEL, k, 80, 0.4)
# eyes warning (minor)
groove(S["S8"], S["S8b"] - 0.05, "warn", BPM, 1); stab(T("d2", "whites") - 0.1, "Dm", 100)
hit(S["S8b"] + 0.02, 116, True); stab(S["S8b"] + 0.02, "E", 112, 0.5)
for k in CH["Am"][1][:3]: n(S["S8b"], PAD, k, 70, S["S9"] - S["S8b"])
stab(T("d2", "see") - 0.15, "Am", 112); hit(T("d2", "see") - 0.15, 118)
# night / nope
for k in (48, 55, 60, 63): n(S["S9"], PAD, k, 66, T("f1", "Nope!") - S["S9"])
for i in range(5): n(S["S9"] + 0.2 + i * 0.5, GLK, (79, 82, 84, 82, 79)[i], 72, 0.3)
hit(T("f1", "Nope!") - 0.15, 122, True); stab(T("f1", "Nope!") - 0.15, "Cm", 116)
# WWII: march snare + brass
march(T("f1", "World") - 0.15, S["S10b"] - 0.05, 104); fanfare(T("f1", "World") - 0.1, (60, 67, 72, 67, 72), 88, 0.14, HORN)
for k in CH["Cm"][1][:3]: n(S["S10"], STR, k, 76, S["S10b"] - S["S10"])
stab(T("f2", "loads") - 0.15, "Bb", 108)
riser_t = T("f2", "Radar!") - 0.2
for j in range(12): n(riser_t - 0.9 + j * 0.075, DR, 38, 40 + j * 6, 0.05)
hit(riser_t, 126, True); stab(riser_t, "G", 120, 0.6); fanfare(riser_t + 0.1, (67, 72, 76, 79), 104, 0.12, TRP)
# outro
groove(S["S11"], END - 1.6, "main", BPM, 3)
for k in CH["C"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, BRS, k, 90, 0.8)
n(END - 1.6, BASS, 36, 104, 1.2); hit(END - 1.6, 110, True); sparkle(END - 1.5, 84)


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
