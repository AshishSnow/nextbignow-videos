"""Cinematic action score for FreshNestHub "The man who survived 46 G" (GeneralUser GS): string ostinato, brass stabs, taiko,
timpani, driving rock kit, synth bass; eerie pad for the eye section, bright major lift for the ending."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TS0 = T("i1", "stopped") - 0.12; TS5 = T("b3", "stop") - 0.1

OST, BASS, BRS, TRP, PAD, STR, TIMP, TAIKO, LOW, GLK, SUB, DR, CEL, PIZ = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9, 12, 13
PROG = {OST: 48, BASS: 38, BRS: 61, TRP: 56, PAD: 89, STR: 49, TIMP: 47, TAIKO: 116, LOW: 58, GLK: 9, SUB: 39, CEL: 8, PIZ: 45}
VOL = {OST: 88, BASS: 104, BRS: 92, TRP: 84, PAD: 62, STR: 84, TIMP: 100, TAIKO: 108, LOW: 90, GLK: 82, SUB: 100, DR: 94, CEL: 84, PIZ: 90}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Dm": (38, [57, 62, 65, 69]), "Bb": (34, [58, 62, 65, 70]), "C": (36, [55, 60, 64, 67]), "A": (33, [57, 61, 64, 69]),
      "Gm": (43, [55, 58, 62, 67]), "F": (41, [57, 60, 65, 69]), "D": (38, [57, 62, 66, 69]), "G": (43, [55, 59, 62, 67])}
PROGS = {"main": ["Dm", "Bb", "C", "A"], "tense": ["Dm", "Gm", "Dm", "A"], "lift": ["F", "C", "Dm", "Bb"], "hero": ["D", "G", "D", "A"]}
BPM = 132


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            if level >= 2:
                n(tq, DR, 36, 100 if q in (0, 2) else 70, 0.2)
                if q % 2 == 1: n(tq, DR, 38, 86, 0.15)
                n(tq + beat / 2, DR, 42, 54, 0.08)
            if level >= 3: n(tq, TAIKO, 41 if q % 2 == 0 else 45, 92, 0.4)
            for e in range(2):  # 8th-note string ostinato
                te = tq + e * beat / 2
                if te < t1 - 0.03: n(te, OST, tri[0] if (q + e) % 2 == 0 else tri[2], 70 + 8 * level, beat * 0.42)
            n(tq, BASS, root - 12, 92, beat * 0.45); n(tq + beat / 2, BASS, root - 12, 80, beat * 0.3)
        for k in tri: n(t, PAD, k, 40 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[1], tri[2], tri[3])): n(t + (2.5 + 0.5 * i) * beat, BRS, k, 92, beat * 0.45)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v - 6, 0.8); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3); n(t, TIMP, 38, v - 10, 1.0)
    if big: n(t, SUB, 26, 112, 1.2); n(t, DR, 57, v - 10, 2.4); n(t, LOW, 26, 100, 0.8)


def stab(t, chord="Dm", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, STR, k + 12, v - 10, d); n(t, BRS, k, v - 16, d)
    n(t, LOW, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, TIMP, 38, 20 + int(90 * (j / m) ** 1.8), 0.06)
    for i, p in enumerate((62, 65, 69, 72, 74)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=86):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 92, 0.5)


def fanfare(t, notes=(62, 69, 74, 72, 74), v=96, step=0.12):
    for i, k in enumerate(notes): n(t + i * step, TRP, k, v, step * 1.6)


def blip(t, k, v=90): n(t, GLK, k, v, 0.25)


# ---- cues ----
groove(0.0, TS0 - 0.02, "main", BPM, 3); riser(TS0, 1.4)
hit(T("i1", "six") - 0.1, 112); stab(T("i1", "six") - 0.1, "Dm", 108)
hit(TS0, 124, True); stab(TS0, "A", 116, 0.6)
n(TS0 + 0.2, PAD, 57, 70, 1.6); n(TS0 + 0.2, PAD, 64, 66, 1.6)
for i in range(4): n(TS0 + 0.5 + i * 0.32, TIMP, 38, 60 + 12 * i, 0.3)
hit(T("i1", "seconds?") - 0.25, 112); stab(T("i1", "seconds?") - 0.25, "Bb", 110)
# S0b on purpose / body
hit(S["S0b"] + 0.02, 114); stab(T("i2", "purpose!") - 0.15, "C", 110); fanfare(T("i2", "purpose!"), (69, 74, 76), 90)
groove(S["S0b"] + 0.4, S["S1"] - 0.05, "tense", BPM, 1); stab(T("i2", "body.") - 0.2, "Dm", 110, 0.5)
# S1 meet Stapp
groove(S["S1"], S["S1b"] - 0.05, "main", BPM, 2); fanfare(S["S1"] + 0.1, (62, 69, 74), 96); stab(T("a1", "Air") - 0.15, "F", 106)
groove(S["S1b"], S["S2"] - 0.05, "main", BPM, 2); hit(T("a1", "himself!") - 0.15, 116, True); stab(T("a1", "himself!") - 0.15, "A", 112)
# S2 18 G (tense, sparse)
for k in CH["Dm"][1]: n(S["S2"], PAD, k, 66, T("a2", "kill") - S["S2"])
n(S["S2"], SUB, 26, 88, 1.5); groove(S["S2"] + 0.2, T("a2", "kill") - 0.2, "tense", 112, 1)
stab(T("a2", "eighteen") - 0.15, "Gm", 104); riser(T("a2", "kill") - 0.1, 1.0)
hit(T("a2", "kill") - 0.1, 122, True); stab(T("a2", "kill") - 0.1, "A", 116, 0.6)
# S2b wrong / S2c rocket sled
hit(S["S2b"] + 0.02, 110); stab(T("a3", "wrong.") - 0.15, "Bb", 112); hit(T("a3", "wrong.") - 0.15, 118)
groove(S["S2c"], S["S3a"] - 0.05, "main", BPM, 2); riser(S["S3a"] - 0.02, 1.4); stab(T("a3", "rocket") - 0.2, "C", 110)
# S3a 1954 New Mexico (big, open)
hit(S["S3a"] + 0.02, 112, True)
for k in CH["F"][1]: n(S["S3a"] + 0.02, STR, k, 84, S["S3b"] - S["S3a"]); n(S["S3a"] + 0.02, BRS, k - 12, 70, S["S3b"] - S["S3a"])
fanfare(T("b1", "New") - 0.1, (69, 72, 77, 76), 92)
# S3b nine rockets -> fire
for i in range(9): blip(T("b1", "Nine") - 0.05 + 0.065 * i, 74 + i, 80 + 2 * i)
riser(T("b1", "fire!") - 0.15, 0.8); hit(T("b1", "fire!") - 0.15, 126, True); stab(T("b1", "fire!") - 0.15, "Dm", 120, 0.6)
# S4 5 seconds -> 632 (full drive)
groove(S["S4"] + 0.05, S["S5"] - 0.05, "main", 140, 3); riser(T("b2", "six") - 0.1, 1.6)
hit(T("b2", "six") - 0.1, 124, True); stab(T("b2", "six") - 0.1, "A", 118); fanfare(T("b2", "six"), (74, 76, 77, 81), 100, 0.1)
# S5 water brakes stop
groove(S["S5"], TS5 - 0.03, "main", 140, 3); hit(TS5, 126, True); stab(TS5, "Bb", 118, 0.8)
for i in range(5): n(TS5 + 0.4 + i * 0.28, TIMP, 38, 50 + 10 * i, 0.25)
stab(T("b3", "seconds.") - 0.2, "A", 112); hit(T("b3", "seconds.") - 0.2, 116)
# S6 46.2 G — the biggest hit
riser(T("c1", "forty-six") - 0.12, 0.5); hit(T("c1", "forty-six") - 0.12, 127, True); stab(T("c1", "forty-six") - 0.12, "Dm", 124, 0.9)
n(T("c1", "forty-six"), DR, 49, 110, 2.5); sparkle(T("c1", "forty-six") + 0.1, 86)
# S7 weighed (tense build)
groove(S["S7"], S["S8"] - 0.05, "tense", BPM, 2); riser(T("c2", "thousand") + 0.2, 1.4)
hit(T("c2", "thousand") + 0.2, 122, True); stab(T("c2", "thousand") + 0.2, "A", 116)
# S8 eyes (eerie)
for k in (50, 57, 62, 65): n(S["S8"], PAD, k, 70, S["S9"] - S["S8"] - 0.1)
n(S["S8"], SUB, 26, 92, 2.0)
for i in range(int((S["S9"] - S["S8"]) / 0.9)): n(S["S8"] + 0.3 + i * 0.9, TIMP, 38, 64, 0.2); n(S["S8"] + 0.52 + i * 0.9, TIMP, 38, 50, 0.2)
stab(T("c3", "burst.") - 0.2, "Gm", 110); hit(T("c3", "burst.") - 0.2, 116)
stab(T("c3", "filled") - 0.1, "Dm", 104, 0.6); hit(T("c3", "couldn't") - 0.1, 118, True); n(T("c3", "couldn't"), LOW, 26, 96, 1.2)
# S9 tooth (comic pizzicato)
for i in range(8): n(S["S9"] + 0.1 + i * 0.227, PIZ, (62, 65, 69, 65, 62, 65, 69, 74)[i], 92, 0.2)
hit(T("c4", "pulled...") - 0.05, 116); stab(T("c4", "pulled...") - 0.05, "A", 110)
for i in range(6): n(T("c4", "pulled...") + 0.25 + i * 0.227, PIZ, (74, 69, 65, 62, 65, 69)[i], 88, 0.2)
stab(T("c4", "no") - 0.15, "Bb", 112); hit(T("c4", "no") - 0.15, 118)
# S10 sight back (bright major)
for k in CH["D"][1]: n(S["S10"], STR, k, 80, S["S11a"] - S["S10"]); n(S["S10"], PAD, k, 70, S["S11a"] - S["S10"])
sparkle(T("d1", "sight") - 0.1, 86); fanfare(T("d1", "back!") - 0.15, (69, 74, 78, 81), 96)
# S11a myth / S11b seat belts (hero groove)
hit(S["S11a"] + 0.02, 116); groove(S["S11a"] + 0.1, S["S11b"] - 0.05, "hero", BPM, 2); stab(T("e1", "G.") - 0.25, "A", 116)
hit(T("e1", "G.") - 0.25, 120, True)
groove(S["S11b"], S["S12"] - 0.05, "hero", BPM, 3); stab(T("e1", "belts") - 0.05, "D", 116); sparkle(T("e1", "belts"), 90)
# S12 outro
groove(S["S12"], END - 1.6, "hero", BPM, 2)
for k in CH["D"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, STR, k + 12, 92, 0.8); n(END - 1.6, BRS, k, 90, 0.9)
n(END - 1.6, LOW, 26, 104, 1.6); hit(END - 1.6, 110, True); fanfare(END - 1.5, (74, 78, 81, 86), 96, 0.1)


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
rng = np.random.default_rng(4); irl = int(1.8 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.42)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.2 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
