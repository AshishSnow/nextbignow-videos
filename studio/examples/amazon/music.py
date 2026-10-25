"""Synth-pop score for 'Amazon's real money machine is AWS' (GeneralUser GS): synth bass, saw lead arps, poly pad, four-on-the-floor — hits on every reveal."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

ARP, BASS, LEAD, GLK, PAD, STR, TIMP, TAIKO, PIZ, VIB, SBR, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {ARP: 81, BASS: 38, LEAD: 80, GLK: 9, PAD: 90, STR: 50, TIMP: 47, TAIKO: 116, PIZ: 45, VIB: 11, SBR: 62, SUB: 39}
VOL = {ARP: 74, BASS: 108, LEAD: 70, GLK: 84, PAD: 70, STR: 78, TIMP: 108, TAIKO: 114, PIZ: 90, VIB: 84, SBR: 88, SUB: 100, DR: 100}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (45, [57, 60, 64, 69]), "F": (41, [57, 60, 65, 69]), "C": (36, [55, 60, 64, 67]), "G": (43, [55, 59, 62, 67]),
      "Dm": (38, [57, 62, 65, 69]), "E": (40, [56, 59, 64, 68]), "Fmaj7": (41, [57, 60, 64, 65])}
PROGS = {"main": ["Am", "F", "C", "G"], "tense": ["Dm", "Am", "Dm", "E"], "money": ["F", "G", "C", "C"]}
BPM = 120


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for e in range(8):
            tq = t + e * beat / 2
            if tq < t1 - 0.03: n(tq, BASS, root - 12 + (12 if e % 2 else 0), 96 if e % 2 == 0 else 78, beat * 0.4)
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.02: break
            n(tq, DR, 36, 112 if level >= 2 else 90, 0.2)
            if q in (1, 3): n(tq, DR, 39, 96, 0.2); n(tq, DR, 38, 64 if level >= 2 else 44, 0.15)
            n(tq + beat / 2, DR, 46 if level >= 2 else 42, 66, 0.12)
            if level >= 3: n(tq + beat / 4, DR, 42, 50, 0.06); n(tq + 3 * beat / 4, DR, 42, 50, 0.06)
        if level >= 2:
            for e in range(8):
                tq = t + e * beat / 2
                if tq < t1 - 0.03: n(tq, ARP, tri[e % 4] + 12, 64 + 6 * (e % 2 == 0), beat * 0.3)
        for k in tri: n(t, PAD, k, 58 + 6 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[3] + 12, tri[2] + 12, tri[1] + 12)): n(t + (2.5 + 0.5 * i) * beat, LEAD, k, 84, beat * 0.4)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 40, v - 10, 1.4); n(t, DR, 49, v - 16, 2.0)
    if big: n(t, SUB, 33, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="Am", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, SBR, k + 12, v, d); n(t, LEAD, k + 12, v - 26, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((64, 67, 69, 72, 76)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


# ---- cues ----
ts = T("i1", "selling") - 0.1
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2)
stab(ts, "F", 112); hit(ts, 108); sparkle(ts + 0.1, 86)
hit(S["S0b"] + 0.02, 118, True); stab(S["S0b"] + 0.02, "E", 114, 0.5)
groove(S["S0b"] + 0.4, S["S1"] - 0.05, "tense", BPM, 1)
sparkle(T("i2", "never") - 0.1, 88)
groove(S["S1"], S["S2a"] - 0.05, "money", BPM, 2)
for j in range(6): n(S["S1"] + 0.1 + j * 0.18, PIZ, [69, 72, 76, 72, 76, 81][j], 90, 0.15)
# shopping side
stab(S["S2a"] + 0.02, "Am", 110); groove(S["S2a"] + 0.25, S["S2b"] - 0.05, "main", BPM, 3)
hit(T("a1", "hundred") - 0.15, 110); sparkle(T("a1", "hundred") - 0.05, 84)
groove(S["S2b"], S["S2c"] - 0.05, "tense", BPM, 1)
for i, k in enumerate((76, 72, 69, 64)): n(T("a2", "eleven") - 0.15 + i * 0.12, LEAD, k, 92, 0.14)
groove(S["S2c"], S["S3a"] - 0.05, "tense", BPM, 1)
n(T("a3", "seven") - 0.15, SUB, 28, 96, 1.0)
# the secret: AWS
riser(S["S3a"] + 0.02, 1.0); hit(S["S3a"] + 0.02, 122, True); stab(S["S3a"] + 0.02, "C", 116, 0.7); sparkle(S["S3a"] + 0.1, 88)
groove(S["S3a"] + 0.6, S["S3c"] - 0.05, "main", BPM, 2)
for i in range(4): n(T("b2", "other") - 0.1 + i * 0.1, GLK, 81 + i * 2, 84, 0.3)
groove(S["S3c"], S["S3d"] - 0.05, "money", BPM, 3)
stab(T("b3", "forty-two") - 0.15, "F", 108); stab(T("b3", "sixteen") - 0.15, "G", 116); hit(T("b3", "sixteen") - 0.15, 112, True)
groove(S["S3d"], S["S4a"] - 0.05, "main", BPM, 2)
sparkle(T("b4", "forty") - 0.1, 86)
# twist
hit(S["S4a"] + 0.02, 120, True); stab(S["S4a"] + 0.02, "E", 116, 0.6)
groove(S["S4b"], T("c3", "six") - 0.3, "tense", BPM, 1)
riser(T("c3", "six") - 0.15, 0.9); hit(T("c3", "six") - 0.15, 120, True); stab(T("c3", "six") - 0.15, "C", 116, 0.5)
groove(T("c3", "six") + 0.3, S["S5a"] - 0.05, "money", BPM, 3)
# ads
stab(S["S5a"] + 0.02, "Am", 108); groove(S["S5a"] + 0.25, S["S5b"] - 0.05, "main", BPM, 2)
hit(T("d1", "Ads!") - 0.12, 112); for_ = [n(T("d1", "sponsored") - 0.05 + i * 0.09, GLK, 88 + i, 84, 0.3) for i in range(3)]
groove(S["S5b"], S["S6"] - 0.05, "money", BPM, 3)
stab(T("d2", "twenty") - 0.15, "G", 114); sparkle(T("d2", "twenty") - 0.05, 88)
# payoff + outro
groove(S["S6"], T("e1", "cloud") - 0.2, "tense", BPM, 1)
stab(T("e1", "cloud") - 0.15, "F", 110); hit(T("e1", "bills.") - 0.15, 116, True); stab(T("e1", "bills.") - 0.15, "C", 114)
groove(S["S7"], END - 1.6, "main", BPM, 3)
for k in CH["Am"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, SBR, k + 12, 100, 0.8)
n(END - 1.6, BASS, 33, 104, 1.6); hit(END - 1.6, 104); sparkle(END - 1.5, 93)


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
