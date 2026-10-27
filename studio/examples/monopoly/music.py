"""Ragtime / stride-piano score for "Monopoly was invented to warn against monopolies" (GeneralUser GS): 1900s-1930s parlour feel —
honky-tonk stride piano (oom-pah left hand, syncopated right hand), tuba on the downbeats, banjo strum, clarinet answers, woodblock;
a slow music-box minor section for Lizzie's $500 / income-zero beat; glockenspiel coins on every money moment; timpani hits on reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

PNO, TUBA, BANJO, CLAR, GLK, BOX, STR, TIMP, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {PNO: 3, TUBA: 58, BANJO: 105, CLAR: 71, GLK: 9, BOX: 10, STR: 48, TIMP: 47, SUB: 38}
VOL = {PNO: 84, TUBA: 96, BANJO: 60, CLAR: 70, GLK: 82, BOX: 90, STR: 56, TIMP: 108, SUB: 96, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [52, 55, 60]), "A7": (33, [52, 55, 61]), "D7": (38, [54, 57, 60]), "G7": (31, [53, 55, 59]), "F": (41, [53, 57, 60]),
      "Fm": (41, [53, 56, 60]), "E7": (40, [52, 56, 59]), "Am": (33, [52, 57, 60]), "Dm": (38, [53, 57, 62])}
PROGS = {"main": ["C", "A7", "D7", "G7"], "lift": ["F", "Fm", "C", "G7"], "tense": ["Am", "E7", "Am", "E7"], "rich": ["C", "E7", "F", "G7"],
         "sad": ["Am", "Dm", "E7", "Am"]}
RH = {"main": [12, 16, 19, None, 24, 19, None, 16], "lift": [17, 21, 24, None, 21, 17, None, 12], "tense": [12, 15, 19, None, 15, 12, None, 11],
      "rich": [19, 24, 28, None, 24, 28, None, 31]}
BPM = 104


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    """stride: tuba + piano bass on 1 & 3, piano chord on 2 & 4; syncopated RH at level >= 2; banjo + woodblock at 2; clarinet at 3"""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for i in range(4):
            tq = t + i * beat
            if tq >= t1 - 0.03: break
            if i in (0, 2):
                bn = root if i == 0 else root + 7 - (12 if root + 7 > 40 else 0)
                n(tq, TUBA, bn, 98, beat * 0.8); n(tq, PNO, bn, 72 + 4 * level, beat * 0.5)
                if level >= 1: n(tq, DR, 36, 50, 0.1)
            else:
                for k in tri: n(tq, PNO, k, 58 + 4 * level, beat * 0.4)
                if level >= 2:
                    n(tq, DR, 76, 52, 0.05)
                    for j, k in enumerate(tri): n(tq + 0.012 * j, BANJO, k + 12, 48, beat * 0.3)
        if level >= 2:
            fig = RH.get(prog, RH["main"])
            for j, iv in enumerate(fig):
                tq = t + j * beat / 2
                if iv is None or tq >= t1 - 0.05: continue
                d = beat / 2 * (1.9 if (j + 1 < 8 and fig[j + 1] is None) else 0.9)
                n(tq, PNO, (root % 12) + 60 + iv - 12, 66 + 4 * level - 4 * (j % 2), d)
        if level >= 3 and b % 2 == 1:
            for j, iv in enumerate((12, 11, 9, 7)): n(t + 2 * beat + j * beat / 2, CLAR, (root % 12) + 60 + iv, 70, beat * 0.45)
        t += bar; b += 1


def sad(t0, t1):
    """slow music-box minor: arpeggios + soft strings"""
    beat = 60 / 72; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS["sad"][b % 4]]
        for k in tri: n(t, STR, k, 46, min(4 * beat, t1 - t) * 0.98)
        for j, k in enumerate([tri[0] + 12, tri[1] + 12, tri[2] + 12, tri[1] + 12, tri[0] + 24, tri[2] + 12]):
            tq = t + j * beat * 2 / 3
            if tq < t1 - 0.05: n(tq, BOX, k, 70, beat)
        n(t, TUBA, root, 60, beat * 2)
        t += 4 * beat; b += 1


def hit(t, v=110, big=False):
    n(t, TIMP, 40, v, 1.4); n(t, DR, 49, v - 20, 2.0)
    if big: n(t, SUB, 28, 108, 1.2); n(t, DR, 57, v - 16, 2.4)


def stab(t, chord="C", v=104, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, PNO, k + 12, v, d); n(t, CLAR, k + 12, v - 26, d)
    n(t, TUBA, root, 104, d * 1.4)


def coins(t, base=84, v=88):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.06, GLK, k, v, 0.5)


def gliss(t, d=0.5):
    ks = list(range(60, 96, 3))
    for i, k in enumerate(ks): n(t + i * d / len(ks), PNO, k, 64 + i, 0.12)


def seg(a, b, prog="main", level=2):
    groove(a + 0.02, b - 0.05, prog, level)


# ---- cues ----
T0 = T("i2", "five") - 0.2
seg(0.0, S["S1"], "main", 2); coins(0.4, 86); stab(T("i1", "monopolies") - 0.1, "G7", 100)
seg(S["S1"], S["S2"], "tense", 1); hit(T0, 108); coins(T0 + 0.05, 84)
tf = T("i3", "flipped") - 0.3; seg(S["S2"], S["S3"], "main", 1); gliss(tf - 0.3, 0.4); hit(tf + 0.2, 112, True)
seg(S["S3"], S["S4"], "main", 1); stab(S["S3"] + 0.02, "C", 100)
seg(S["S4"], S["S6"], "lift", 2); hit(T("a1", "patent") - 0.1, 100)
seg(S["S6"], S["S7"], "main", 2); coins(T("a3", "rent") - 0.15, 86); stab(T("a3", "jail") - 0.45, "E7", 110); hit(T("a3", "jail") - 0.45, 104)
seg(S["S7"], S["S8"], "lift", 2); stab(T("a4", "message") - 0.3, "G7", 104)
seg(S["S8"], S["S9"], "tense", 2); hit(T("a5", "everyone") - 0.25, 104)
seg(S["S9"], S["S10"], "main", 2); stab(S["S9"] + 0.25, "C", 100); stab(S["S9"] + 0.45, "G7", 100)
seg(S["S10"], S["S11"], "tense", 3); hit(T("b2", "crushing") - 0.05, 116, True); stab(T("b2", "crushing") - 0.05, "E7", 112)
seg(S["S11"], S["S12"], "lift", 2); coins(T("b3", "everyone") - 0.25, 88); coins(T("b3", "everyone") + 0.1, 91)
seg(S["S12"], S["S13"], "main", 1)
hit(S["S13"] + 0.05, 118, True); stab(S["S13"] + 0.05, "Am", 112, 0.5); seg(S["S13"] + 0.3, S["S14"], "tense", 1)
te = T("c1", "escaped") - 0.3; seg(S["S14"], S["S15"], "main", 1); gliss(te, 0.5); stab(te + 0.5, "G7", 104)
seg(S["S15"], S["S17"], "main", 3)
seg(S["S17"], S["S18"], "tense", 1); stab(T("c3", "friend") - 0.35, "C", 96)
seg(S["S18"], S["S19"], "lift", 2)
ts = T("c4", "sold") - 0.25; seg(S["S19"], S["S20"], "main", 3); hit(ts, 108); coins(ts + 0.3, 86)
seg(S["S20"], S["S21"], "rich", 2); hit(T("c5", "invention") - 0.3, 112); stab(T("c5", "invention") - 0.3, "G7", 108)
seg(S["S21"], S["S22"], "rich", 3); coins(S["S21"] + 0.3, 88); coins(S["S21b"] + 0.2, 91); hit(S["S21b"] + 0.05, 110)
seg(S["S22"], S["S23"], "rich", 3); stab(S["S22"] + 0.05, "C", 112); coins(S["S22"] + 0.2, 93)
sad(S["S23"] + 0.05, S["S27"] - 0.05); hit(T("d1", "five") - 0.3, 100)
n(T("d3", "Zero") - 0.25, BOX, 69, 96, 1.5); n(T("d3", "Zero") - 0.25, TIMP, 33, 100, 2.0)
seg(S["S27"], S["S28"], "tense", 1); stab(S["S27"] + 0.02, "E7", 100)
tc = T("f2", "court") - 0.1; seg(S["S28"], S["S29"], "tense", 2); hit(tc, 116, True)
seg(S["S29"], S["S29b"], "main", 1); gliss(T("f3", "found") - 0.4, 0.4); stab(T("f3", "found") - 0.05, "C", 104)
seg(S["S29b"], S["S30"], "main", 2)
tw = T("t1", "became") - 0.25; seg(S["S30"], S["S31"], "tense", 1); hit(tw, 118, True); stab(tw, "C", 114, 0.6); coins(tw + 0.2, 91)
seg(S["S31"], S["S32"], "lift", 2); hit(T("t2", "first") - 0.35, 104)
seg(S["S32"], S["S33"], "main", 1); coins(S["S32"] + 0.1, 86); stab(T("e1", "don't") - 0.15, "G7", 104)
seg(S["S33"], END - 1.6, "main", 3)
for k in CH["C"][1]: n(END - 1.6, PNO, k + 12, 96, 1.6); n(END - 1.6, CLAR, k + 12, 82, 0.9)
n(END - 1.6, TUBA, 36, 104, 1.6); hit(END - 1.6, 104); coins(END - 1.5, 91)


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
