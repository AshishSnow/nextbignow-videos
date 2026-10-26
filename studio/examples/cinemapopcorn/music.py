"""Retro big-band swing score for "Why movie theaters make money on popcorn" (GeneralUser GS): walking bass, brushed swing kit, piano comping, muted trumpet, brass, vibes."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}



# Retro swing / old-Hollywood lobby energy: walking upright bass, ride + hat swing kit, piano comps, muted trumpet riffs, brass stabs, vibes
PZ, BASS, BSN, CLA, VLN, PAD, STR, TIMP, TAIKO, TUBA, GLK, SUB, DR, CEL = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9, 13
PROG = {PZ: 0, BASS: 32, BSN: 57, CLA: 59, VLN: 48, PAD: 49, STR: 61, TIMP: 47, TAIKO: 116, TUBA: 58, GLK: 11, SUB: 32, CEL: 8}
VOL = {PZ: 88, BASS: 110, BSN: 92, CLA: 88, VLN: 76, PAD: 56, STR: 92, TIMP: 96, TAIKO: 100, TUBA: 92, GLK: 86, SUB: 104, DR: 100, CEL: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (45, [57, 60, 64, 67]), "F": (41, [57, 60, 64, 65]), "C": (36, [55, 59, 64, 69]), "G": (43, [53, 59, 62, 65]),
      "Em": (40, [55, 59, 62, 64]), "Dm": (38, [57, 60, 62, 65]), "E": (40, [56, 59, 62, 64])}
PROGS = {"main": ["C", "Am", "Dm", "G"], "tense": ["Am", "Em", "Dm", "E"], "money": ["F", "G", "Em", "Am"]}
BPM = 138


def groove(t0, t1, prog="main", bpm=BPM, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0; sw = beat * 2 / 3
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        walk = [root - 12, root - 12 + (3 if prog == "tense" else 4), root - 12 + 7, root - 12 + 9 if b % 2 == 0 else root - 12 + 10]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            n(tq, DR, 51, 74 if level >= 2 else 58, 0.3)                      # ride
            if q % 2 == 1:
                n(tq + sw, DR, 51, 60, 0.2); n(tq, DR, 44, 70, 0.1)              # swung skip + hat pedal
                if level >= 2: n(tq, DR, 38, 50 if level == 2 else 68, 0.1)      # brush/snare on 2 & 4
            if q in (0, 2) and level >= 2: n(tq, DR, 36, 78, 0.2)
            n(tq, BASS, walk[q], 100, beat * 0.85)
        # piano comps: Charleston (1, and-of-2)
        for tq, v_ in ((t, 66), (t + beat + sw, 72)):
            if tq < t1 - 0.03:
                for k in tri: n(tq, PZ, k, v_ + 4 * level, beat * 0.45)
        if level >= 2:
            for k in tri: n(t, PAD, k, 34 + 5 * level, min(bar, t1 - t) * 0.98)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tri[3] + 12, tri[2] + 12, tri[1] + 12, tri[2] + 12)): n(t + 2 * beat + i * sw / 1.0 * 0.5 + (sw / 2 if i % 2 else 0), CLA, k, 84, beat * 0.35)
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
tp = T("i1", "popcorn…") - 0.15; tt = T("i1", "ticket") - 0.15
groove(0.0, S["S0b"] - 0.05, "main", BPM, 2); n(0.0, DR, 49, 96, 2.0); stab(0.05, "C", 104)
hit(tp, 110); stab(tp, "F", 108); sparkle(tp + 0.05, 88); hit(tt, 118, True); stab(tt, "G", 112); lick(tt + 0.3)
hit(S["S0b"] + 0.02, 110); groove(S["S0b"] + 0.3, S["S1"] - 0.05, "money", BPM, 1)
stab(T("i2", "crazy.") - 0.2, "Em", 104); hit(T("i2", "math!") - 0.2, 118, True); stab(T("i2", "math!") - 0.2, "C", 112, 0.5); sparkle(T("i2", "math!") - 0.1, 90)
# step 1: ticket
groove(S["S1"], S["S1b"] - 0.05, "main", BPM, 2); stab(S["S1"] + 0.02, "C", 106)
hit(T("a1", "twelve") - 0.15, 116, True); stab(T("a1", "twelve") - 0.15, "F", 110); blip(T("a1", "twelve") - 0.05)
groove(S["S1b"], S["S2"] - 0.05, "tense", BPM, 2); stab(T("a2", "half") - 0.2, "Am", 106); riser(T("a2", "studio!") - 0.2, 0.8)
hit(T("a2", "studio!") - 0.2, 118, True); stab(T("a2", "studio!") - 0.2, "E", 112)
stab(T("a3", "keeps") - 0.15, "C", 108); sparkle(T("a3", "fifty-two") - 0.1, 88)
# step 2: snack bar
hit(S["S2"] + 0.02, 112); stab(S["S2"] + 0.02, "F", 108); groove(S["S2"] + 0.3, S["S2b"] - 0.05, "money", BPM, 3)
hit(T("b1", "sixty") - 0.2, 118, True); stab(T("b1", "sixty") - 0.2, "G", 112); lick(T("b1", "sixty"))
groove(S["S2b"], S["S3"] - 0.05, "main", BPM, 2); stab(T("b2", "itself?") - 0.2, "Dm", 104); hit(T("b2", "twenty") - 0.15, 112)
riser(T("b3", "eighty") - 0.15, 1.0); hit(T("b3", "eighty") - 0.15, 122, True); stab(T("b3", "eighty") - 0.15, "C", 116, 0.5); sparkle(T("b3", "eighty") - 0.05, 90)
# step 3: add it up
hit(S["S3"] + 0.02, 110); groove(S["S3"] + 0.2, S["S3b"] - 0.05, "main", BPM, 2)
for i in range(3): n(S["S3"] + 0.25 + 0.15 * i, GLK, 72 + 4 * i, 84, 0.3)
hit(T("c1", "third") - 0.15, 116, True); stab(T("c1", "third") - 0.15, "Am", 110)
# balance scale: suspense then tie
groove(S["S3b"], T("c3", "tie!") - 0.35, "tense", BPM, 1); n(S["S3b"], SUB, 33, 96, 2.0)
stab(T("c2", "billion") - 0.4, "F", 110); hit(T("c2", "billion") - 0.4, 112)
stab(T("c3", "billion") - 0.3, "G", 110); riser(T("c3", "tie!") - 0.3, 0.9)
hit(T("c3", "tie!") - 0.3, 124, True); stab(T("c3", "tie!") - 0.3, "C", 118, 0.6); sparkle(T("c3", "tie!") - 0.2, 90)
# door -> bills
groove(S["S4"], S["S5"] - 0.05, "money", BPM, 3); stab(T("d1", "door…") - 0.15, "Em", 106)
hit(T("d1", "popcorn") - 0.2, 116, True); stab(T("d1", "popcorn") - 0.2, "Am", 112)
for i in range(3): n(T("d1", "popcorn") + 0.05 + 0.18 * i, GLK, 79 + 5 * i, 90, 0.3)
# twist: the loss — minor, sparse
hit(S["S5"] + 0.02, 110); groove(S["S5"] + 0.2, T("f1", "lost") - 0.25, "tense", BPM, 1)
hit(T("f1", "lost") - 0.2, 126, True); stab(T("f1", "lost") - 0.2, "E", 118, 0.8)
for k in CH["Am"][1]: n(T("f1", "lost"), PAD, k, 70, S["S6"] - T("f1", "lost"))
for j, k in enumerate((76, 74, 72, 69)): n(T("f1", "lost") + 0.4 + 0.25 * j, CLA, k, 82, 0.3)
n(S["S5b"], SUB, 33, 96, 1.8)
for w_ in ("Rent,", "staff", "debt"): stab(T("f2", w_) - 0.1, "Dm", 100, 0.2)
# payoff + outro
hit(S["S6"] + 0.02, 112); groove(S["S6"] + 0.2, S["S7"] - 0.05, "main", BPM, 3)
riser(T("e1", "blockbuster!") - 0.3, 1.0); hit(T("e1", "blockbuster!") - 0.3, 124, True); stab(T("e1", "blockbuster!") - 0.3, "C", 118, 0.6); sparkle(T("e1", "blockbuster!") - 0.2, 90)
groove(S["S7"], END - 1.6, "money", BPM, 3)
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
