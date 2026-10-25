"""Southern bluegrass-pop score for "Closed every Sunday, still winning" (GeneralUser GS): banjo rolls, boom-chick bass, fiddle, harmonica."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}


# Southern bluegrass-pop hoedown: banjo rolls, boom-chick upright bass, steel-guitar strums, fiddle licks, harmonica stabs
BNJ, BASS, GTR, FID, HARM, PAD, STR, TIMP, TAIKO, PIZ, GLK, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {BNJ: 105, BASS: 32, GTR: 25, FID: 110, HARM: 22, PAD: 48, STR: 49, TIMP: 47, TAIKO: 116, PIZ: 45, GLK: 9, SUB: 39}
VOL = {BNJ: 92, BASS: 112, GTR: 84, FID: 80, HARM: 86, PAD: 58, STR: 78, TIMP: 104, TAIKO: 110, PIZ: 90, GLK: 84, SUB: 100, DR: 96}
LEAD, SBR, ARP = FID, HARM, BNJ
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"G": (43, [55, 59, 62, 67]), "C": (36, [55, 60, 64, 67]), "D": (38, [57, 62, 66, 69]), "Em": (40, [55, 59, 64, 67]),
      "Am": (45, [57, 60, 64, 69]), "B7": (47, [54, 59, 63, 69])}
PROGS = {"main": ["G", "C", "G", "D"], "tense": ["Em", "Am", "Em", "B7"], "money": ["C", "D", "G", "G"]}
BPM = 126


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            # boom-chick bass: root / fifth
            n(tq, BASS, root - 12 + (7 if q % 2 else 0), 100 if q % 2 == 0 else 86, beat * 0.5)
            # train-beat drums: kick on 1/3, snare on 2/4 (brushy), hats on 8ths
            if q % 2 == 0: n(tq, DR, 36, 104 if level >= 2 else 84, 0.2)
            else: n(tq, DR, 38, 70 if level >= 2 else 50, 0.15); n(tq, DR, 39, 60 if level >= 2 else 0, 0.15)
            n(tq + beat / 2, DR, 42, 54, 0.08)
            if level >= 3: n(tq + beat / 4, DR, 42, 36, 0.05); n(tq + 3 * beat / 4, DR, 42, 40, 0.05)
            # guitar chop on the off-beats
            for k in tri[1:]: n(tq + beat / 2, GTR, k - 12, 70, beat * 0.3)
        if level >= 2:
            roll = [tri[0], tri[2], tri[3] + 12, tri[0], tri[2], tri[3] + 12, tri[0], tri[2]]
            for e in range(16):
                tq = t + e * beat / 4
                if tq < t1 - 0.03: n(tq, BNJ, roll[e % 8] + 12 * (e % 3 == 2), 66 + 10 * (e % 4 == 0), beat * 0.25)
        for k in tri: n(t, PAD, k, 50 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[3] + 12, tri[2] + 12, tri[1] + 12, tri[3] + 12)): n(t + (2.0 + 0.5 * i) * beat, FID, k, 80, beat * 0.45)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 43, v - 10, 1.4); n(t, DR, 49, v - 16, 2.0)
    if big: n(t, SUB, 31, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="G", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, HARM, k + 12, v - 10, d); n(t, GTR, k, v - 10, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((62, 66, 69, 74, 78)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=86):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


def lick(t, notes=(74, 76, 79, 81, 79), v=88, step=0.09):
    for i, k in enumerate(notes): n(t + i * step, FID, k, v, step * 1.4)


# ---- cues ----
tl = T("i1", "closed") - 0.1; tb = T("i1", "beating") - 0.12
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2)
hit(tl + 0.3, 110); stab(tl + 0.3, "Em", 108); sparkle(tb, 86); lick(tb + 0.1)
hit(S["S0b"] + 0.02, 116, True); stab(S["S0b"] + 0.02, "D", 112, 0.5)
groove(S["S0b"] + 0.4, T("i2", "more") - 0.2, "tense", BPM, 1)
hit(T("i2", "locked.") - 0.1, 112); stab(T("i2", "more") - 0.15, "G", 114); sparkle(T("i2", "more") - 0.05, 88)
groove(T("i2", "more") + 0.2, S["S1"] - 0.05, "money", BPM, 2)
# size
stab(S["S1"] + 0.02, "C", 108); groove(S["S1"] + 0.25, S["S1b"] - 0.05, "main", BPM, 3)
hit(T("a1", "twenty-four") - 0.15, 116, True); stab(T("a1", "twenty-four") - 0.15, "G", 114); sparkle(T("a1", "twenty-four") - 0.05, 86)
groove(S["S1b"], S["S2a"] - 0.05, "money", BPM, 2)
stab(T("a2", "three") - 0.12, "D", 110); lick(T("a2", "Only") - 0.1, (67, 71, 74, 79), 84)
# counts
hit(S["S2a"] + 0.02, 118, True); stab(S["S2a"] + 0.02, "B7", 112, 0.6)
groove(S["S2a"] + 0.5, S["S2b"] - 0.05, "tense", BPM, 1)
for j in range(6): n(T("b1", "fourteen") - 0.2 + 0.1 * j, PIZ, [67, 71, 74, 79, 83, 86][j], 88, 0.12)
for j in range(4): n(T("b2", "About") - 0.1 + 0.12 * j, PIZ, [79, 74, 71, 67][j], 92, 0.14)
groove(S["S2b"], S["S3a"] - 0.05, "main", BPM, 3)
hit(T("b3", "does!") - 0.1, 112); stab(T("b3", "does!") - 0.1, "G", 112)
# averages
groove(S["S3a"], S["S3b"] - 0.05, "tense", BPM, 1)
for j in range(4): n(T("c1", "four") - 0.15 + 0.15 * j, GLK, 79 + 2 * j, 88, 0.3)
riser(S["S3b"] + 0.02, 0.8); hit(S["S3b"] + 0.02, 116); groove(S["S3b"] + 0.3, S["S4a"] - 0.05, "money", BPM, 3)
for j in range(8): n(T("c2", "seven") - 0.15 + 0.1 * j, GLK, 79 + j, 86, 0.3)
hit(T("c2", "six") - 0.12, 120, True); stab(T("c2", "six") - 0.12, "D", 116, 0.5)
# hidden deal
hit(S["S4a"] + 0.02, 116, True); stab(S["S4a"] + 0.02, "Em", 110, 0.6)
groove(S["S4a"] + 0.5, S["S4b"] - 0.05, "tense", BPM, 1)
stab(T("d1", "ten") - 0.15, "G", 116); sparkle(T("d1", "ten") - 0.05, 88)
groove(S["S4b"], S["S4c"] - 0.05, "tense", BPM, 2)
hit(T("d2", "keeps") - 0.1, 116, True); stab(T("d2", "keeps") - 0.1, "B7", 112)
groove(S["S4c"], S["S5a"] - 0.05, "tense", BPM, 1)
stab(T("d3", "fifteen") - 0.15, "Am", 106); stab(T("d3", "half") - 0.15, "Em", 112); hit(T("d3", "half") - 0.15, 112)
# why Sundays: slow, warm
for k in CH["C"][1]: n(S["S5a"], STR, k, 70, S["S5c"] - S["S5a"])
n(S["S5a"], BASS, 24, 96, 2.0); sparkle(S["S5a"] + 0.2, 84)
groove(S["S5b"], S["S5c"] - 0.05, "main", BPM, 1)
lick(T("f1", "forty-six") - 0.15, (67, 71, 74, 76, 79), 82, 0.11)
riser(S["S5c"] + 0.02, 0.6); groove(S["S5c"], S["S6"] - 0.05, "money", BPM, 2)
hit(T("f2", "changed") - 0.1, 118, True); stab(T("f2", "changed") - 0.1, "G", 114)
# payoff + outro
hit(S["S6"] + 0.02, 114); groove(S["S6"] + 0.2, S["S7"] - 0.05, "main", BPM, 3)
stab(T("e1", "busiest") - 0.15, "C", 110); hit(T("e1", "twenty") - 0.15, 120, True); stab(T("e1", "twenty") - 0.15, "D", 116); sparkle(T("e1", "twenty") - 0.05, 90)
groove(S["S7"], END - 1.6, "main", BPM, 3)
for k in CH["G"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, HARM, k + 12, 96, 0.8)
n(END - 1.6, BASS, 31, 104, 1.6); hit(END - 1.6, 104); lick(END - 1.5, (74, 79, 83, 86), 90)

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
