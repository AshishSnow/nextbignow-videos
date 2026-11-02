"""Doo-wop street-corner score for HOW TO START ep 3, food truck NYC (GeneralUser GS): 12/8 piano triplets, upright bass, finger snaps, 'ooh' voices, tenor sax honks; minor after-hours walk for the rented permit block."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
PNO, BASS, SAX, VIB, OOH, BRS, BARI, GTR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {PNO: 0, BASS: 32, SAX: 66, VIB: 11, OOH: 53, BRS: 61, BARI: 67, GTR: 25}
VOL = {PNO: 88, BASS: 106, SAX: 82, VIB: 80, OOH: 66, BRS: 80, BARI: 84, GTR: 60, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# doo-wop in C (I-vi-IV-V, the street-corner changes), 12/8; after-hours walk in A minor for the rented-permit block
CH = {"C": (36, [60, 64, 67, 72]), "Am": (33, [60, 64, 69, 72]), "F": (41, [60, 65, 69, 72]), "G": (43, [59, 62, 67, 71]),
      "Dm": (38, [62, 65, 69, 74]), "E7": (40, [59, 64, 68, 74]), "G7": (43, [59, 62, 65, 71])}
PROGS = {"main": ["C", "Am", "F", "G"], "lift": ["F", "G", "C", "Am"], "dark": ["Am", "F", "Dm", "E7"], "end": ["F", "G7", "C", "C"]}
BPM = 76


def groove(t0, t1, prog="main", level=2):
    """one chord per bar of 12/8: piano triplets, bass 1-3 + walk-up, snaps on 2 and 4, 'ooh' pad"""
    beat = 60 / BPM; tri8 = beat / 3; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        ch_ = PROGS[prog][b % 4]; root, tones = CH[ch_]
        for i in range(12):
            tq = t + i * tri8
            if tq >= t1 - 0.03: break
            if level >= 1:
                v = 66 + (12 if i % 3 == 0 else 0)
                for k in (tones[:3] if i % 3 == 0 else tones[1:3]): n(tq, PNO, k + 12, v, tri8 * 0.85)
            if i in (3, 9) and level >= 1: n(tq, DR, 39, 78, 0.1)        # snaps/clap on 2 and 4
            if level >= 2 and i % 3 == 0: n(tq, DR, 42, 44, 0.05)
            if i in (0, 6): n(tq, BASS, root - 12 + (0 if i == 0 else 7), 104, beat * 1.4)
            if i == 10 and level >= 1: n(tq, BASS, root - 12 + 9, 86, tri8 * 1.5)
            if i in (0, 6) and level >= 1: n(tq, DR, 36, 74, 0.15)
        if level >= 2:
            for k in tones[:3]: n(t, OOH, k, 56 + 4 * level, bar * 0.92)
        if level >= 3 and b % 2 == 1: n(t + beat * 2, SAX, tones[2] + 12, 74, beat * 0.9); n(t + beat * 3, SAX, tones[1] + 12, 70, beat * 0.8)
        t += bar; b += 1


def dark(t0, t1):
    """after hours: bass walks alone, soft low sax, brushes"""
    beat = 60 / BPM; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS["dark"][b % 4]]
        for i, st in enumerate((0, 3, 5, 7)):
            if t + i * beat < t1 - 0.03: n(t + i * beat, BASS, root - 12 + st, 100, beat * 0.9); n(t + i * beat + beat * 2 / 3, DR, 44, 42, 0.05)
        for k in tones[:3]: n(t, OOH, k - 12, 52, bar * 0.9)
        if b % 2 == 0: n(t + beat, BARI, tones[0] - 12, 66, beat * 2.2)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 16, 1.8); n(t, DR, 36, v, 0.3); n(t, DR, 38, v - 10, 0.2)
    if big: n(t, BASS, 28, 110, 1.2); n(t, DR, 57, v - 10, 2.2)


def stab(t, chord="C", v=104, d=0.3):
    root, tones = CH[chord]
    for k in tones: n(t, BRS, k, v - 8, d); n(t, SAX, k, v - 18, d)
    n(t, BASS, root - 12, 100, d)


def sax_honk(t, k=58, v=108):
    """tenor sax honk answering the truck horn on each STEP card"""
    n(t, BARI, k, v, 0.22); n(t + 0.26, BARI, k, v - 10, 0.34)


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.06, VIB, k, 88, 0.5)


# ---- cues ----
for k in CH["C"][1]: n(0.0, PNO, k + 12, 92, 0.4); n(0.0, OOH, k, 74, S["S1"])
stab(0.0, "C", 106); n(0.0, BASS, 24, 100, 0.8)
groove(0.5, S["S2b"] - 0.05, "main", 2)
stab(Tw("i1", "thousands", -0.25), "G", 108); sparkle(Tw("i1", "thousands", -0.15), 86)
stab(Tw("i3", "legally", -0.2), "Dm", 100)
groove(S["S2b"] + 0.1, S["S3"] - 0.05, "lift", 2)
for i in range(4): n(S["S2b"] + 0.12 * i, VIB, 84 + 3 * i, 92, 0.4)
for sid, k in (("S3", 58), ("S6", 60), ("S9", 62), ("S12", 55)): sax_honk(S[sid] + 0.02, k)
groove(S["S3"] + 0.5, S["S6"] - 0.1, "main", 2)
sparkle(Tw("a3", "no", -0.1), 88)
groove(S["S6"] + 0.5, S["S9"] - 0.1, "lift", 3)
for w_ in ("stored", "cleaned", "serviced"): n(Tw("b2", w_, -0.05), VIB, 88, 94, 0.4)
groove(S["S9"] + 0.5, S["S12"] - 0.1, "main", 3)
stab(Tw("c2", "thousands", -0.3), "F", 104)
stab(Tw("c3", "four", -0.1), "Dm", 98, 0.5)
groove(S["S12"] + 0.5, S["S15"] - 0.1, "lift", 1)
hit(Tw("e2", "capped", -0.1), 112, True); stab(Tw("e2", "capped", -0.1), "E7", 104, 0.5)
dark(S["S15"], S["S18"] - 0.1)
hit(Tw("e5", "twenty-five", -0.25), 114, True); stab(Tw("e5", "twenty-five", -0.25), "F", 104, 0.5)
hit(Tw("e6", "six", -0.2), 106)
stab(S["S18"] + 0.02, "C", 110); sparkle(S["S18"] + 0.1, 84)
groove(S["S18"] + 0.3, S["S19"] - 0.05, "main", 3)
stab(S["S19"] + 0.05, "Am", 96, 0.5); dark(S["S19"] + 0.3, S["S19b"] - 0.05)
stab(S["S19b"] + 0.02, "F", 102); groove(S["S19b"] + 0.3, S["S21"] - 0.05, "main", 2)
sparkle(Tw("t2", "no", -0.2), 88)
groove(S["S21"], END - 1.4, "end", 3)
for k in CH["C"][1]: n(END - 1.4, PNO, k + 12, 96, 0.5); n(END - 1.4, OOH, k, 76, 1.6); n(END - 1.4, BRS, k, 96, 0.6)
n(END - 1.4, BASS, 24, 104, 1.4); hit(END - 1.4, 100); sparkle(END - 1.3, 84)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S2b", "S3", "S6", "S9", "S12", "S15", "S18", "S19", "S21")] + [END + 3]))
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
