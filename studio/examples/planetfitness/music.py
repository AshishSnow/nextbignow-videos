"""Synth-pop workout score for "Planet Fitness: $15 a month" (GeneralUser GS): synth bass, saw lead, poly pad, four-on-the-floor drums, bells."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}



# Upbeat synth-pop / gym-class energy: pumping synth bass, four-on-floor kick, claps, saw lead hooks, glassy bells
PZ, BASS, BSN, CLA, VLN, PAD, STR, TIMP, TAIKO, TUBA, GLK, SUB, DR, CEL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9, 13
PROG = {PZ: 81, BASS: 38, BSN: 39, CLA: 80, VLN: 50, PAD: 89, STR: 62, TIMP: 47, TAIKO: 118, TUBA: 87, GLK: 98, SUB: 39, CEL: 11}
VOL = {PZ: 84, BASS: 104, BSN: 90, CLA: 80, VLN: 76, PAD: 60, STR: 84, TIMP: 96, TAIKO: 104, TUBA: 92, GLK: 84, SUB: 100, DR: 96, CEL: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (45, [57, 60, 64, 69]), "F": (41, [57, 60, 65, 69]), "C": (36, [55, 60, 64, 67]), "G": (43, [55, 59, 62, 67]),
      "Em": (40, [55, 59, 64, 67]), "Dm": (38, [57, 62, 65, 69]), "E": (40, [56, 59, 64, 68])}
PROGS = {"main": ["Am", "F", "C", "G"], "tense": ["Am", "Em", "Dm", "E"], "money": ["F", "G", "Am", "C"]}
BPM = 124


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            n(tq, DR, 36, 104 if level >= 2 else 84, 0.2)
            if q % 2 == 1: n(tq, DR, 39, 78 if level >= 2 else 56, 0.15)
            n(tq + beat / 2, DR, 42, 58, 0.08)
            if level >= 3: n(tq + beat / 4, DR, 42, 34, 0.05); n(tq + 3 * beat / 4, DR, 42, 40, 0.05)
            # pumping offbeat octave bass
            n(tq, BASS, root - 12, 92, beat * 0.3); n(tq + beat / 2, BASS, root, 100, beat * 0.4)
        for k in tri: n(t, PAD, k, 44 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 2:
            arp = [tri[0], tri[2], tri[3], tri[1] + 12, tri[3], tri[2], tri[1] + 12, tri[2] + 12]
            for e in range(8):
                tq = t + e * beat / 2
                if tq < t1 - 0.03: n(tq, PZ, arp[e] + 12, 58 + 6 * (e % 2 == 0), beat * 0.22)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[3] + 12, tri[2] + 12, tri[3] + 12, tri[0] + 24)): n(t + (2.0 + 0.5 * i) * beat, CLA, k, 80, beat * 0.4)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v - 10, 0.8); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 21, 112, 1.2); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="Am", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, STR, k + 12, v - 10, d); n(t, TUBA, k, v - 24, d)
    n(t, BSN, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 39, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((57, 60, 64, 69, 72)): n(t_end - dur + i * dur / 5, VLN, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=88):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def lick(t, notes=(76, 79, 81, 84, 81), v=88, step=0.09):
    for i, k in enumerate(notes): n(t + i * step, CLA, k, v, step * 1.4)


def blip(t, notes=(72, 76, 79, 84), v=90, step=0.1):
    for i, k in enumerate(notes): n(t + i * step, GLK, k, v, step * 1.5)


# ---- cues ----
tf = T("i1", "fifteen") - 0.12; tm = T("i1", "million") - 0.2
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2)
hit(tf, 110); stab(tf, "Am", 106); hit(tm, 118, True); stab(tm, "F", 112); sparkle(tm + 0.05, 88); lick(tm + 0.3)
hit(S["S0b"] + 0.02, 112); groove(S["S0b"] + 0.3, S["S1"] - 0.05, "money", BPM, 1)
stab(T("i2", "genius.") - 0.2, "C", 106); sparkle(T("i2", "genius.") - 0.1, 90)
hit(T("i2", "you!") - 0.15, 120, True); stab(T("i2", "you!") - 0.15, "G", 114, 0.5)
# secret 1
groove(S["S1"], S["S1b"] - 0.05, "main", BPM, 2); stab(S["S1"] + 0.02, "Am", 106)
stab(T("a1", "pointless.") - 0.15, "E", 110); hit(T("a1", "pointless.") - 0.15, 112)
groove(S["S1b"], S["S2"] - 0.05, "money", BPM, 3); blip(T("a2", "Fifteen")); stab(T("a2", "yearly") - 0.15, "C", 108); sparkle(T("a2", "yearly") - 0.05)
# secret 2
hit(S["S2"] + 0.02, 112); stab(S["S2"] + 0.02, "Am", 108); riser(T("b1", "twenty-one") - 0.15, 1.2)
groove(S["S2"] + 0.3, S["S2b"] - 0.05, "main", BPM, 2)
hit(T("b1", "twenty-one") - 0.15, 120, True); stab(T("b1", "twenty-one") - 0.15, "F", 114); sparkle(T("b1", "twenty-one"), 90)
groove(S["S2b"], S["S2c"] - 0.05, "tense", BPM, 2); stab(T("b2", "clubs.") - 0.2, "Em", 106)
hit(T("b2", "seven") - 0.15, 120, True); stab(T("b2", "seven") - 0.15, "E", 114)
groove(S["S2c"], S["S3a"] - 0.05, "tense", BPM, 3); riser(T("b3", "chaos!") - 0.15, 1.0)
hit(T("b3", "chaos!") - 0.15, 124, True); stab(T("b3", "chaos!") - 0.15, "Dm", 118, 0.5)
# secret 3 — sneaky, sparse
hit(S["S3a"] + 0.02, 108); groove(S["S3a"] + 0.2, S["S3b"] - 0.05, "tense", BPM, 1)
stab(T("c1", "report.") - 0.25, "Am", 106); blip(T("c1", "report.") - 0.1, (84, 79, 76, 72))
for k in CH["Am"][1]: n(S["S3b"], PAD, k, 70, S["S4a"] - S["S3b"])
n(S["S3b"], SUB, 33, 92, 2.0)
for j, w_ in enumerate(("A", "member", "not")): n(T("c2", w_), CEL, (81, 84, 88)[j], 80, 0.5)
hit(T("c2", "regularly") - 0.1, 116, True); stab(T("c2", "regularly") - 0.1, "E", 110, 0.6)
# the study
hit(S["S4a"] + 0.02, 112); groove(S["S4a"] + 0.2, S["S4b"] - 0.05, "main", BPM, 2); stab(T("d1", "seventy") - 0.2, "C", 108); sparkle(T("d1", "seventy") - 0.1)
groove(S["S4b"], S["S4c"] - 0.05, "tense", BPM, 2)
for i in range(5): n(S["S4b"] + 0.25 + 0.22 * i, GLK, 76 + 3 * i, 84, 0.25)
hit(T("d2", "seventeen") - 0.15, 120, True); stab(T("d2", "seventeen") - 0.15, "Dm", 114)
groove(S["S4c"], S["S4d"] - 0.05, "money", BPM, 2); stab(T("d3", "ten") - 0.2, "F", 106); blip(T("d3", "there.") - 0.25)
groove(S["S4d"], S["S5"] - 0.05, "main", BPM, 3); hit(T("d4", "Eighty") - 0.15, 114); hit(T("d4", "saved") - 0.15, 118, True); stab(T("d4", "saved") - 0.15, "G", 112)
# money
riser(S["S5"] + 0.02, 0.6); groove(S["S5"] + 0.1, S["S6"] - 0.05, "money", BPM, 3)
hit(T("f1", "billion") - 0.2, 116); stab(T("f1", "billion") - 0.2, "F", 110)
hit(T("f1", "twenty") - 0.15, 122, True); stab(T("f1", "twenty") - 0.15, "C", 116); sparkle(T("f1", "twenty") - 0.05, 90)
# payoff + outro
hit(S["S6"] + 0.02, 112); groove(S["S6"] + 0.2, S["S7"] - 0.05, "main", BPM, 3)
stab(T("e1", "workouts.") - 0.1, "Dm", 110); hit(T("e1", "plan") - 0.2, 122, True); stab(T("e1", "plan") - 0.2, "Am", 116); sparkle(T("e1", "plan") - 0.1, 90)
groove(S["S7"], END - 1.6, "money", BPM, 3)
for k in CH["Am"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, STR, k + 12, 92, 0.8)
n(END - 1.6, BSN, 33, 104, 1.6); hit(END - 1.6, 104); lick(END - 1.5, (76, 79, 81, 88), 90)

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
