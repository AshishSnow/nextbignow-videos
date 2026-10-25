"""Upbeat funk score for 'Costco's $1.50 hot dog' (GeneralUser GS): clav, slap bass, brass, claps — hits on every reveal."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
CLAV, BASS, BRS, GLK, PAD, STR, TIMP, TAIKO, PIZ, VIB, SBR, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {CLAV: 7, BASS: 36, BRS: 61, GLK: 9, PAD: 89, STR: 48, TIMP: 47, TAIKO: 116, PIZ: 45, VIB: 11, SBR: 62, SUB: 38}
VOL = {CLAV: 92, BASS: 108, BRS: 94, GLK: 84, PAD: 66, STR: 80, TIMP: 110, TAIKO: 116, PIZ: 92, VIB: 84, SBR: 86, SUB: 100, DR: 100}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"G6": (43, [59, 62, 64, 67]), "Em7": (40, [59, 62, 64, 67]), "Cmaj7": (36, [59, 60, 64, 67]), "D7": (38, [57, 60, 62, 66]),
      "Am7": (45, [57, 60, 64, 67]), "B7": (47, [59, 63, 66, 69]), "F": (41, [57, 60, 65, 69])}
PROGS = {"main": ["G6", "Em7", "Cmaj7", "D7"], "tense": ["Em7", "Cmaj7", "Am7", "B7"], "money": ["Cmaj7", "D7", "G6", "G6"]}
BASSPAT = [(0, 0, 100), (0.75, 12, 70), (1.5, 10, 84), (2, 7, 90), (2.75, 12, 72), (3.25, 10, 80), (3.5, 5, 76)]


def groove(t0, t1, prog="main", bpm=112, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for off, iv, vel in BASSPAT:
            tq = t + off * beat
            if tq < t1 - 0.03: n(tq, BASS, root - 12 + iv, vel, beat * 0.42)
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.02: break
            if q in (0, 2): n(tq, DR, 36, 112, 0.2)
            if level >= 2 and q == 1: n(tq + beat * 0.5, DR, 36, 84, 0.2)
            if q in (1, 3): n(tq, DR, 39, 92, 0.2); n(tq, DR, 38, 70 if level >= 2 else 50, 0.15)
            for e in range(2 if level < 3 else 4):
                n(tq + e * beat / (2 if level < 3 else 4), DR, 42, 60 + (14 if e % 2 == 0 else 0), 0.08)
        for off in (0.5, 1.25, 2.5, 3.25):
            if t + off * beat < t1 - 0.03:
                for k in tri: n(t + off * beat, CLAV, k, 72 + 4 * level, beat * 0.22)
        if level >= 3 and b % 2 == 1:
            for k in tri: n(t + 3.5 * beat, BRS, k + 12, 96, beat * 0.35)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 40, v - 10, 1.4); n(t, DR, 49, v - 16, 2.0)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="G6", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k + 12, v, d); n(t, SBR, k, v - 16, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.07)
    for j in range(m): n(t_end - dur + j * 0.07, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((62, 66, 69, 72, 74)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


# ---- cues ----
td = T("i1", "dollar") - 0.12
groove(0.0, S["S0b"] - 0.05, "main", 112, 2)
stab(td, "Cmaj7", 114); hit(td, 112); sparkle(td + 0.1, 86)
stab(S["S0b"] + 0.02, "D7", 108); groove(S["S0b"] + 0.25, S["S1"] - 0.05, "main", 112, 3)
n(T("i2", "forty") - 0.1, DR, 49, 100, 1.5)
groove(S["S1"], S["S1b"] - 0.05, "money", 112, 2)
stab(T("i3", "make") - 0.1, "Am7", 104)
groove(S["S1b"], S["S2a"] - 0.05, "tense", 112, 2)
riser(T("i4", "genius.") - 0.15, 1.1); hit(T("i4", "genius.") - 0.15, 116, True); sparkle(T("i4", "genius.") - 0.05, 88)
# secret 1
stab(S["S2a"] + 0.02, "G6", 112); hit(S["S2a"] + 0.02, 104)
groove(S["S2a"] + 0.3, S["S2b"] - 0.05, "main", 112, 3)
for i, k in enumerate((74, 71, 67, 62)): n(T("a1", "loses") - 0.1 + i * 0.12, BRS, k, 96, 0.14)
# the founder quote: tension vamp, then stop-time + hit on "kill"
tk = T("a2", "kill") - 0.15
groove(S["S2b"], T("a2", "if") - 0.15, "tense", 112, 1)
for j in range(int((tk - T("a2", "if") + 0.15) / 0.134)): n(T("a2", "if") - 0.15 + j * 0.134, PIZ, 52 + (j % 4) * 3, 90, 0.1)
hit(tk, 124, True); stab(tk, "B7", 118, 0.6)
groove(S["S2c"], S["S3a"] - 0.05, "main", 112, 2)
for i in range(6): n(T("a3", "trust") - 0.05 + i * 0.12, GLK, 79 + (i % 3) * 5, 84, 0.3)
# secret 2: chicken
stab(S["S3a"] + 0.02, "Cmaj7", 110); hit(S["S3a"] + 0.02, 100)
groove(S["S3a"] + 0.3, S["S3c"] - 0.05, "main", 112, 3)
stab(T("b1", "four") - 0.1, "G6", 108); sparkle(T("b2", "hundred") - 0.1, 84)
# store walk: pizzicato walking line over light groove
groove(S["S3c"], S["S4a"] - 0.05, "tense", 112, 1)
for j in range(int((S["S4a"] - S["S3c"]) / 0.268)): n(S["S3c"] + j * 0.268, PIZ, [55, 59, 62, 64, 62, 59][j % 6], 92, 0.2)
# secret 3: markup cap
stab(S["S4a"] + 0.02, "D7", 110)
groove(S["S4a"] + 0.3, S["S5a"] - 0.05, "main", 112, 2)
hit(T("c1", "caps") + 0.1, 116); stab(T("c2", "deal.") - 0.2, "G6", 112); sparkle(T("c2", "deal.") - 0.1, 88)
# secret 4: genius -> the card -> money
for k in CH["Em7"][1]: n(S["S5a"], PAD, k, 70, S["S5b"] - S["S5a"]); n(S["S5a"], STR, k, 70, S["S5b"] - S["S5a"])
sparkle(S["S5a"] + 0.1, 84); sparkle(T("d1", "genius") - 0.1, 91); hit(T("d1", "genius") - 0.1, 100)
groove(S["S5b"], T("d2", "card.") - 0.3, "tense", 112, 1)
riser(T("d2", "card.") - 0.25, 1.0); hit(T("d2", "card.") - 0.25, 120, True); stab(T("d2", "card.") - 0.25, "Cmaj7", 116, 0.8)
groove(S["S5c"], S["S5d"] - 0.05, "money", 112, 3)
stab(T("d3", "six") - 0.15, "D7", 112); stab(T("d3", "half") - 0.2, "G6", 114); hit(T("d3", "half") - 0.2, 104)
groove(S["S5d"], S["S6"] - 0.05, "main", 112, 2)
for i in range(9): n(T("d4", "nine") - 0.1 + i * 0.06, GLK, 76 + i, 80, 0.25)
# payoff + outro
groove(S["S6"], T("e1", "ad…") - 0.2, "tense", 112, 1)
hit(T("e1", "ad…") - 0.15, 118, True); stab(T("e1", "ad…") - 0.15, "Cmaj7", 114)
stab(T("e1", "card.") - 0.2, "D7", 110)
groove(S["S7"], END - 1.6, "main", 112, 3)
for k in CH["G6"][1]: n(END - 1.6, CLAV, k, 90, 1.2); n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, BRS, k + 12, 100, 0.8)
n(END - 1.6, BASS, 31, 104, 1.6); hit(END - 1.6, 104); sparkle(END - 1.5, 91)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S0b", "S1", "S1b", "S2a", "S2b", "S2c", "S3a", "S3c", "S4a", "S5a", "S5b", "S5c", "S5d", "S6", "S7")] + [END + 3]))
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
