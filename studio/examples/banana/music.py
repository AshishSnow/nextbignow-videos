"""Calypso score for "Every banana is a clone" (GeneralUser GS) — new genre: Caribbean calypso / steel band.
Steel-pan chord strums on the 3-3-2 calypso rhythm, marimba answers, syncopated bass, congas + shaker; a dark minor half-time for
the fungus (TR4) section; a soft 1950s "mento" flashback (nylon guitar + clarinet) for the Gros Michel story; timpani/brass on reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
PAN, MAR, BASS, TBN, TPT, GLK, PAD, STR, TIMP, SUB, NYL, CLA, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {PAN: 114, MAR: 12, BASS: 33, TBN: 57, TPT: 56, GLK: 9, PAD: 89, STR: 48, TIMP: 47, SUB: 38, NYL: 24, CLA: 71}
VOL = {PAN: 84, MAR: 76, BASS: 104, TBN: 80, TPT: 76, GLK: 84, PAD: 60, STR: 70, TIMP: 108, SUB: 98, NYL: 80, CLA: 72, DR: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67]), "Am": (33, [60, 64, 69]), "F": (41, [60, 65, 69]), "G": (31, [59, 62, 67]), "Dm": (38, [62, 65, 69]),
      "E7": (40, [59, 62, 68]), "Bb": (34, [58, 62, 65]), "Em": (40, [59, 64, 67]), "G7": (31, [59, 62, 65])}
PROGS = {"main": ["C", "F", "G7", "C"], "busy": ["F", "G", "Em", "Am"], "dark": ["Am", "Dm", "E7", "Am"], "spread": ["Dm", "Bb", "E7", "Am"],
         "old": ["F", "C", "G7", "C"], "win": ["F", "G", "C", "C"]}
BPM = 112
CAL = (0, 0.75, 1.5, 2.0, 2.75, 3.5)   # 3-3-2 + push, in beats


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for j, off in enumerate((0, 1.5, 2, 3) if level >= 2 else (0, 2)):
            tq = t + off * beat
            if tq < t1 - 0.03: n(tq, BASS, root - 12 + (7 if j == 2 and level >= 2 else 0), 100 if j == 0 else 84, beat * (0.7 if level >= 2 else 1.6))
        if level >= 1:
            for off in (CAL if level >= 2 else (0, 1.5, 3)):
                tq = t + off * beat
                if tq < t1 - 0.03:
                    for k in tri: n(tq, PAN, k + 12, 70 + 6 * min(level, 3), beat * 0.45)
        if level >= 2:
            for i in range(8):
                tq = t + i * beat / 2
                if tq < t1 - 0.03: n(tq, DR, 70, 54 + 14 * (i % 2), 0.08)     # maracas
            for off, k in ((0, 64), (1, 63), (1.5, 62), (2.5, 63), (3, 64), (3.5, 62)):
                if t + off * beat < t1 - 0.03: n(t + off * beat, DR, k, 82, 0.1)   # congas
            n(t + beat, DR, 37, 70, 0.1); n(t + 3 * beat, DR, 37, 70, 0.1)
            n(t, DR, 36, 96, 0.15); n(t + 2 * beat, DR, 36, 84, 0.15)
        else:
            n(t, DR, 64, 66, 0.2); n(t + 2 * beat, DR, 62, 60, 0.2)
        if level >= 3 and b % 2 == 1:
            for j, iv in enumerate((7, 9, 12, 9, 7)):
                n(t + (0.5 + j * 0.5) * beat, MAR, root + 36 + iv - 12, 88, beat * 0.4)
        t += bar; b += 1


def mento(t0, t1, bpm=100):
    """1950s flashback: nylon guitar strums + clarinet answers, soft bass"""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS["old"][b % 4]]
        n(t, BASS, root - 12, 84, beat * 1.5); n(t + 2 * beat, BASS, root - 5, 76, beat * 1.5)
        for off in (0, 1.5, 2, 3):
            if t + off * beat < t1 - 0.03:
                for i_, k in enumerate(tri): n(t + off * beat + 0.012 * i_, NYL, k, 70, beat * 0.6)
        if b % 2 == 1:
            for j, iv in enumerate((4, 7, 9, 7)):
                if t + (j * 0.5 + 1) * beat < t1: n(t + (j * 0.5 + 1) * beat, CLA, root + 24 + iv, 74, beat * 0.45)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TIMP, 40, v, 1.4); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="C", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, TBN, k, v, d); n(t, TPT, k + 12, v - 10, d); n(t, PAN, k + 12, v - 6, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.07)
    for j in range(m): n(t_end - dur + j * 0.07, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((60, 63, 67, 70, 72)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


def pad(t0, t1, chord, v=56):
    for k in CH[chord][1]: n(t0, PAD, k - 12, v, max(0.1, t1 - t0))


# ---- cues ----
pad(0.0, S["S1"], "C", 58); sparkle(0.05, 84)
groove(0.3, S["S1"] - 0.05, "main", 2)
stab(S["S0b"] + 0.02, "F", 102)
groove(S["S1"], S["S3"] - 0.05, "busy", 1)
hit(T("i2", "worried.") - 0.15, 108); stab(T("i2", "worried.") - 0.15, "Am", 104)
riser(T("i3", "already") - 0.1, 1.0); hit(T("i3", "already") - 0.1, 116, True); stab(T("i3", "already") - 0.1, "E7", 110, 0.5)
stab(S["S3"] + 0.02, "C", 108)
groove(S["S3"] + 0.25, S["S8b"] - 0.05, "main", 3)
hit(T("a2", "never") + 0.45, 104)
sparkle(T("a3", "clone.") - 0.2, 88); hit(T("a3", "clone.") - 0.2, 106)
hit(T("a4", "half") - 0.15, 106); stab(T("a4", "half") - 0.15, "G", 102)
sparkle(T("a5", "nearly") - 0.1, 86)
stab(S["S8"] + 0.02, "Dm", 104)
pad(S["S8b"], S["S9"], "Am", 62)
riser(T("a6", "kill") - 0.2, 1.2); hit(T("a6", "kill") - 0.2, 118, True); stab(T("a6", "kill") - 0.2, "E7", 112, 0.6)
stab(S["S9"] + 0.02, "Am", 108)
groove(S["S9"] + 0.25, S["S14"] - 0.05, "dark", 1)
pad(S["S10"], S["S14"], "Dm", 52)
hit(T("b3", "blocks") - 0.15, 104); hit(T("b3", "dies.") - 0.2, 110)
hit(T("b4", "No") - 0.1, 118, True); stab(T("b4", "No") - 0.1, "E7", 110, 0.5)
hit(T("b5", "decades.") - 0.3, 106)
groove(S["S14"], S["S18"] - 0.05, "spread", 2)
for w_ in ("Colombia,", "Peru,", "Venezuela,"): hit(T("b7", w_) - 0.1, 104); stab(T("b7", w_) - 0.1, "Dm", 100, 0.2)
riser(T("b8", "Ecuador.") - 0.15, 1.2); hit(T("b8", "Ecuador.") - 0.15, 122, True); stab(T("b8", "Ecuador.") - 0.15, "E7", 114, 0.7)
hit(T("b9", "July") - 0.2, 110)
pad(S["S18"], S["S19"], "F", 58); stab(T("c0", "already") - 0.15, "Bb", 100, 0.6)
hit(S["S19"], 108); mento(S["S19"] + 0.2, S["S23"] - 0.05)
hit(T("c3", "hit") - 0.15, 104); hit(T("c4", "followed") - 0.25, 106)
riser(T("c5", "Cavendish.") - 0.2, 1.0); hit(T("c5", "Cavendish.") - 0.2, 112); sparkle(T("c5", "Cavendish.") - 0.1, 88)
groove(S["S23"], S["S24"] - 0.05, "win", 2)
hit(S["S24"], 116, True); stab(S["S24"] + 0.02, "Am", 110)
groove(S["S24"] + 0.3, S["S26"] - 0.05, "dark", 1)
stab(T("t1", "another") - 0.15, "E7", 112, 0.5)
hit(T("t2", "kills") - 0.15, 120, True)
groove(S["S26"], END - 1.6, "win", 3)
hit(T("e0", "hits") - 0.2, 112); stab(T("e0", "hits") - 0.2, "G7", 108)
sparkle(T("e1", "copy.") - 0.2, 86)
for k in CH["C"][1]: n(END - 1.6, PAN, k + 12, 92, 1.6); n(END - 1.6, PAD, k - 12, 72, 2.0); n(END - 1.6, TBN, k, 96, 0.8); n(END - 1.6, TPT, k + 12, 92, 0.8)
n(END - 1.6, BASS, 36, 104, 1.6); hit(END - 1.6, 104); sparkle(END - 1.5, 84)

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
cuts = sorted(set([0.0] + [S[k] for k in ("S1", "S3", "S8b", "S9", "S14", "S18", "S19", "S23", "S24", "S26")] + [END + 3]))
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
