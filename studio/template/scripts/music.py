"""Boom-bap hip-hop score for 'Starbucks is secretly a bank' (GeneralUser GS): jazzy EP, sub bass, crisp drums, brass hits."""
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
PROG = {CLAV: 4, BASS: 33, BRS: 61, GLK: 9, PAD: 89, STR: 48, TIMP: 47, TAIKO: 116, PIZ: 45, VIB: 11, SBR: 62, SUB: 38}
VOL = {CLAV: 92, BASS: 108, BRS: 94, GLK: 84, PAD: 66, STR: 80, TIMP: 110, TAIKO: 116, PIZ: 92, VIB: 84, SBR: 86, SUB: 100, DR: 100}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Fm9": (41, [56, 60, 63, 67]), "Bbm9": (46, [56, 61, 65, 68]), "Eb9": (39, [55, 58, 61, 65]), "Abmaj9": (44, [55, 60, 63, 67]),
      "Dbmaj7": (37, [56, 60, 61, 65]), "C7": (36, [55, 58, 64, 67])}
PROGS = {"main": ["Fm9", "Bbm9", "Eb9", "Abmaj9"], "tense": ["Fm9", "Dbmaj7", "C7", "Fm9"], "money": ["Abmaj9", "Dbmaj7", "Eb9", "Fm9"]}


def groove(t0, t1, prog="main", bpm=92, level=2):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0; sw = 0.58
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for off, iv, vel in ((0, 0, 104), (1.5 + (sw - 0.5), 0, 86), (2.5, 7, 92), (3.5 + (sw - 0.5), 10, 80)):
            if t + off * beat < t1 - 0.03: n(t + off * beat, BASS, root - 12 + iv, vel, beat * 0.7)
        for off, k, v in ((0, 36, 116), (1.5 + (sw - 0.5), 36, 92), (2.25, 36, 84), (1, 38, 104), (3, 38, 108)):
            if t + off * beat < t1 - 0.03: n(t + off * beat, DR, k, v, 0.2)
        if level >= 2:
            for q in range(8):
                tq = t + (q // 2 + (0 if q % 2 == 0 else sw)) * beat
                if tq < t1 - 0.03: n(tq, DR, 42, 64 + (16 if q % 2 == 0 else 0), 0.08)
        if level >= 3 and b % 2 == 1: n(t + 3.5 * beat, DR, 46, 80, 0.3)
        if t < t1 - 0.05:
            for k in tri: n(t, CLAV, k, 70 + 4 * level, bar * 0.9)
        if level >= 3 and b % 2 == 1:
            for k in tri: n(t + 3.5 * beat, BRS, k + 12, 92, beat * 0.35)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 40, v - 10, 1.4); n(t, DR, 49, v - 16, 2.0)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="Fm9", v=106, d=0.32):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k + 12, v, d); n(t, SBR, k, v - 16, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.07)
    for j in range(m): n(t_end - dur + j * 0.07, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((60, 63, 67, 70, 72)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 3, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


# ---- cues ----
to = T("i1", "one") - 0.15
for k in CH["Fm9"][1]: n(0.0, PAD, k, 56, S["S0b"]); n(0.0, CLAV, k, 70, 1.6)
n(0.0, BASS, 29, 90, 1.5); n(0.62, DR, 57, 70, 1.5); n(0.62, TIMP, 40, 90, 1.0)
for i in range(6): n(0.62 + i * 0.09, GLK, 84 + [0, 3, 7, 10, 12, 15][i], 86, 0.4)
groove(1.4, S["S0b"] - 0.05, "main", 92, 2)
stab(to, "Abmaj9", 112); hit(to, 108); sparkle(to + 0.1, 87)
stab(S["S0b"] + 0.02, "Eb9", 104); groove(S["S0b"] + 0.2, S["S1"] - 0.05, "main", 92, 3)
groove(S["S1"], S["S2a"] - 0.05, "tense", 92, 1)
riser(T("i3", "became") - 0.2, 0.9); hit(T("i3", "became") - 0.2, 114, True); stab(T("i3", "became") - 0.2, "Abmaj9", 110)
stab(S["S2a"] + 0.02, "Fm9", 108); groove(S["S2a"] + 0.25, S["S2c"] - 0.05, "main", 92, 3)
for tt_ in (T("a2", "Twenty-five"), T("a2", "Fifty")): sparkle(tt_ + 0.25, 86)
hit(T("a2", "Millions") - 0.12, 104)
groove(S["S2c"], S["S3a"] - 0.05, "money", 92, 2)
stab(S["S3a"] + 0.02, "Bbm9", 110); groove(S["S3a"] + 0.25, S["S3b"] - 0.05, "main", 92, 2)
hit(T("b1", "zero") + 0.06, 120, True)
groove(S["S3b"], T("b2", "nothing!") - 0.25, "tense", 92, 2)
hit(T("b2", "nothing!") - 0.2, 116); stab(T("b2", "nothing!") - 0.2, "C7", 112, 0.5)
stab(S["S4a"] + 0.02, "Dbmaj7", 104)
for k in CH["Fm9"][1]: n(S["S4a"], PAD, k, 66, S["S4c"] - S["S4a"]); n(S["S4a"], STR, k, 60, S["S4c"] - S["S4a"])
for j in range(int((S["S4c"] - S["S4a"]) / 0.33)): n(S["S4a"] + j * 0.33, GLK, [72, 75, 79, 77, 75, 72][j % 6] + 12, 66, 0.4)
groove(S["S4c"], S["S4d"] - 0.05, "money", 92, 3)
stab(T("c3", "two") - 0.15, "Abmaj9", 114); hit(T("c3", "two") - 0.15, 112, True); sparkle(T("c3", "two") - 0.05, 89)
groove(S["S4d"], S["S5"] - 0.05, "main", 92, 2)
stab(T("c4", "revenue…") - 0.2, "Eb9", 106); hit(T("c4", "no") - 0.12, 106)
groove(S["S5"], S["S6"] - 0.05, "main", 92, 2)
for i in range(4): n(T("d1", "four") - 0.1 + i * 0.08, GLK, 79 + i * 3, 88, 0.3)
groove(S["S6"], T("e1", "funding") - 0.25, "tense", 92, 1)
riser(T("e1", "funding") - 0.2, 0.9); hit(T("e1", "funding") - 0.2, 118, True); stab(T("e1", "funding") - 0.2, "Abmaj9", 114, 0.6)
groove(S["S7"], END - 1.6, "main", 92, 3)
for k in CH["Abmaj9"][1]: n(END - 1.6, CLAV, k, 90, 1.6); n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, BRS, k + 12, 100, 0.8)
n(END - 1.6, BASS, 32, 104, 1.6); hit(END - 1.6, 104); sparkle(END - 1.5, 87)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S0b", "S1", "S2a", "S2c", "S3a", "S3b", "S4a", "S4c", "S4d", "S5", "S6", "S7")] + [END + 3]))
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
