"""Orchestral pizzicato caper score for "Printer ink costs more than champagne" (GeneralUser GS): pizz strings, tuba, bassoon, clarinet, celesta."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}



# Sneaky orchestral pizzicato caper (heist feel): pizz strings walking, tuba/bassoon bass, clarinet lead, brushed snare, celesta/glock sparkles
PZ, BASS, BSN, CLA, VLN, PAD, STR, TIMP, TAIKO, TUBA, GLK, SUB, DR, CEL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9, 13
PROG = {PZ: 45, BASS: 32, BSN: 70, CLA: 71, VLN: 40, PAD: 48, STR: 49, TIMP: 47, TAIKO: 116, TUBA: 58, GLK: 9, SUB: 39, CEL: 8}
VOL = {PZ: 100, BASS: 104, BSN: 84, CLA: 86, VLN: 80, PAD: 56, STR: 76, TIMP: 104, TAIKO: 110, TUBA: 100, GLK: 86, SUB: 100, DR: 92, CEL: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Dm": (38, [57, 62, 65, 69]), "Bb": (34, [58, 62, 65, 70]), "Gm": (43, [58, 62, 67, 70]), "A7": (45, [57, 61, 64, 67]),
      "F": (41, [57, 60, 65, 69]), "C": (36, [55, 60, 64, 67]), "E7": (40, [56, 59, 62, 64])}
PROGS = {"main": ["Dm", "Bb", "Gm", "A7"], "tense": ["Dm", "E7", "Dm", "A7"], "money": ["F", "C", "Bb", "A7"]}
BPM = 118


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            # tiptoe bass: root / fifth staccato on tuba + pizz bass
            n(tq, TUBA if q % 2 == 0 else BASS, root - 12 + (7 if q % 2 else 0), 98 if q % 2 == 0 else 88, beat * 0.35)
            # brushed snare backbeat, soft kick
            if q % 2 == 0: n(tq, DR, 36, 96 if level >= 2 else 76, 0.2)
            else: n(tq, DR, 38, 62 if level >= 2 else 44, 0.15)
            n(tq + beat / 2, DR, 42, 48, 0.08)
            if level >= 3: n(tq + beat / 4, DR, 42, 34, 0.05); n(tq + 3 * beat / 4, DR, 44, 40, 0.05)
            # pizzicato chord stabs on the off-beat
            for k in tri[1:]: n(tq + beat / 2, PZ, k, 76, beat * 0.25)
        if level >= 2:
            walk_ = [tri[0], tri[1], tri[2], tri[3], tri[2] + 12, tri[3], tri[2], tri[1]]
            for e in range(8):
                tq = t + e * beat / 2
                if tq < t1 - 0.03: n(tq, PZ, walk_[e] + 12, 70 + 8 * (e % 2 == 0), beat * 0.3)
        for k in tri: n(t, PAD, k, 46 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[3] + 12, tri[2] + 12, tri[1] + 12, tri[0] + 12)): n(t + (2.0 + 0.5 * i) * beat, CLA, k, 84, beat * 0.45)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 38, v - 10, 1.4); n(t, DR, 49, v - 16, 2.0)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="Dm", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, STR, k + 12, v - 10, d); n(t, BSN, k - 12, v - 16, d)
    n(t, TUBA, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((62, 65, 69, 74, 77)): n(t_end - dur + i * dur / 5, VLN, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=86):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def lick(t, notes=(74, 77, 81, 79, 77), v=88, step=0.09):
    for i, k in enumerate(notes): n(t + i * step, CLA, k, v, step * 1.4)


def tiptoe(t, notes=(62, 64, 65, 67), v=90, step=0.12):
    for i, k in enumerate(notes): n(t + i * step, BSN, k - 12, v, step * 0.8); n(t + i * step, PZ, k + 12, v - 6, step * 0.6)


# ---- cues ----
ts = T("i1", "seven") - 0.12; tc = T("i1", "champagne?") - 0.15
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2)
hit(ts + 0.05, 112); stab(ts + 0.05, "Dm", 108); sparkle(tc, 86); lick(tc + 0.1)
hit(S["S0b"] + 0.02, 114, True); stab(S["S0b"] + 0.02, "A7", 110, 0.5)
groove(S["S0b"] + 0.4, T("i2", "plan!") - 0.2, "tense", BPM, 1)
stab(T("i2", "mistake.") - 0.1, "E7", 108); hit(T("i2", "plan!") - 0.15, 118, True); stab(T("i2", "plan!") - 0.15, "Dm", 114); sparkle(T("i2", "plan!") - 0.05, 88)
# step 1
groove(S["S1"], S["S1b"] - 0.05, "main", BPM, 2); stab(S["S1"] + 0.02, "Bb", 106)
tiptoe(T("a1", "cheap.") - 0.4); sparkle(T("a1", "cheap.") - 0.1, 90)
groove(S["S1b"], S["S2"] - 0.05, "money", BPM, 3); lick(T("a2", "deal!") - 0.1, (69, 72, 77, 81), 90)
# step 2
hit(S["S2"] + 0.02, 112); stab(S["S2"] + 0.02, "Gm", 108); groove(S["S2"] + 0.3, S["S3a"] - 0.05, "tense", BPM, 2)
stab(T("b1", "out.") - 0.1, "E7", 110); hit(T("b1", "more.") - 0.15, 110); stab(T("b1", "again.", 0) - 0.15, "Dm", 108); stab(T("b1", "again.", 1) - 0.15, "A7", 112)
# price per ml
groove(S["S3a"], S["S3b"] - 0.05, "tense", BPM, 1)
for j in range(5): n(S["S3a"] + 0.4 + 0.3 * j, GLK, 81 - j, 84, 0.3)
hit(T("c1", "eighty,") - 0.2, 118, True); stab(T("c1", "eighty,") - 0.2, "Dm", 114)
groove(S["S3b"], S["S3c"] - 0.05, "money", BPM, 2); sparkle(S["S3b"] + 0.1, 88); stab(T("c2", "twenty-four") - 0.2, "F", 108)
riser(S["S3c"] + 0.02, 0.6); groove(S["S3c"] + 0.1, S["S4a"] - 0.05, "main", BPM, 3)
hit(T("c3", "seven") - 0.15, 120, True); stab(T("c3", "seven") - 0.15, "A7", 116, 0.5)
# the money
hit(S["S4a"] + 0.02, 114); stab(S["S4a"] + 0.02, "F", 108); groove(S["S4a"] + 0.3, S["S4b"] - 0.05, "money", BPM, 3)
hit(T("d1", "eleven") - 0.15, 120, True); stab(T("d1", "eleven") - 0.15, "C", 114); sparkle(T("d1", "eleven") - 0.05, 90)
groove(S["S4b"], S["S4c"] - 0.05, "main", BPM, 2); stab(T("d2", "two") - 0.2, "Gm", 108)
groove(S["S4c"], S["S5a"] - 0.05, "money", BPM, 3); hit(T("d3", "fifty") - 0.15, 114); stab(T("d3", "fifty") - 0.15, "F", 112)
stab(T("d3", "half") - 0.2, "A7", 112); hit(T("d3", "half") - 0.2, 116, True)
# the boss said it — sparse, sneaky
for k in CH["Dm"][1]: n(S["S5a"], STR, k, 66, S["S6"] - S["S5a"])
n(S["S5a"], TUBA, 26, 96, 1.6); tiptoe(S["S5a"] + 0.3, (62, 65, 69, 72))
groove(S["S5b"] + 0.3, S["S6"] - 0.05, "tense", BPM, 1)
hit(T("f2", "bad") + 0.3, 118, True); stab(T("f2", "bad") + 0.3, "E7", 112, 0.5)
# payoff + outro
hit(S["S6"] + 0.02, 112); groove(S["S6"] + 0.2, S["S7"] - 0.05, "main", BPM, 3)
stab(T("e1", "product.") - 0.1, "Gm", 110); hit(T("e1", "ink") - 0.2, 120, True); stab(T("e1", "ink") - 0.2, "Dm", 116); sparkle(T("e1", "ink") - 0.1, 90)
groove(S["S7"], END - 1.6, "money", BPM, 3)
for k in CH["Dm"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, STR, k + 12, 92, 0.8)
n(END - 1.6, TUBA, 26, 104, 1.6); hit(END - 1.6, 104); lick(END - 1.5, (74, 77, 81, 86), 90)

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
