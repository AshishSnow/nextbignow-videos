"""Winter jazz waltz for HOW TO START ep 4, Christmas lights (GeneralUser GS): 3/4 upright bass + brushes, comp piano, celesta + clarinet tune (original, no carol), soft sleigh bells; minor frost section for the ladder step."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
PNO, BASS, CEL, VIB, CLA, PAD, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {PNO: 0, BASS: 32, CEL: 8, VIB: 11, CLA: 71, PAD: 49}
VOL = {PNO: 76, BASS: 104, CEL: 92, VIB: 78, CLA: 78, PAD: 54, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67, 71]), "Am": (33, [60, 64, 67, 69]), "Dm": (38, [60, 62, 65, 69]), "G": (43, [59, 62, 65, 67]), "F": (41, [60, 64, 65, 69]), "E7": (40, [59, 62, 64, 68]),
      "Ab": (32, [60, 63, 67, 68]), "Fm": (41, [60, 63, 65, 68]), "Bb": (34, [58, 62, 65, 69]), "Em": (40, [59, 62, 64, 67])}
PROGS = {"main": ["C", "Am", "Dm", "G"], "lift": ["F", "Em", "Dm", "G"], "frost": ["Am", "F", "Dm", "E7"], "end": ["F", "G", "C", "C"]}
BPM = 138
TUNES = {"main": [(0, 76), (1, 79), (2, 84), (3, 83), (5, 79), (6, 77), (7, 74), (8, 76), (9, 72), (11, 74)], "lift": [(0, 81), (1, 84), (2, 81), (3, 79), (5, 76), (6, 77), (7, 81), (8, 79), (9, 74), (11, 79)], "end": [(0, 77), (1, 81), (2, 84), (3, 79), (4, 83), (5, 86), (6, 88), (8, 84), (9, 84)]}


def waltz(t0, t1, prog="main", level=2, tune=None):
    """one chord per 3/4 bar: bass on 1 (and walks on 3), piano on 2-3, brushes + soft sleigh bells on all three; tune phrases on celesta (level>=2) or clarinet (level 3)"""
    beat = 60 / BPM; bar = 3 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % 4]]
        n(t, BASS, root - 12, 104, beat * 1.6); n(t + 2 * beat, BASS, root - 12 + 7, 86, beat * 0.8)
        for q in (1, 2):
            if t + q * beat < t1 - 0.03:
                for k in tones[:3]: n(t + q * beat, PNO, k, 56 + (6 if q == 1 else 0), beat * 0.5)
        for q in range(3):
            if t + q * beat < t1 - 0.03:
                n(t + q * beat, DR, 44, 40 if q else 52, 0.05); n(t + q * beat, DR, 54, 40 if q else 50, 0.08)
                if level >= 2: n(t + (q + 0.5) * beat, DR, 54, 26, 0.05)
        if level >= 1 and b % 2 == 0:
            for k in tones[:3]: n(t, PAD, k - 12, 40 + 4 * level, bar * 1.9)
        if tune:
            for bt, k in TUNES[tune]:
                bb = b % 4 * 3 + 0
                if bb <= bt < bb + 3:
                    tq = t + (bt - bb) * beat
                    if tq < t1 - 0.1:
                        n(tq, CEL, k + 12 if level < 3 else k + 12, 74, beat * 0.85)
                        if level >= 3: n(tq, CLA, k, 68, beat * 0.9)
        t += bar; b += 1


def frost(t0, t1):
    """step 3: slower, minor; bass + celesta only, no bells"""
    beat = 60 / BPM; bar = 3 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS["frost"][b % 4]]
        n(t, BASS, root - 12, 100, beat * 2.4); n(t, DR, 44, 40, 0.05)
        for k in tones[:3]: n(t + beat, PNO, k, 50, beat * 1.2)
        if b % 2 == 0: n(t, CLA, tones[2], 58, bar * 1.6)
        n(t + 2 * beat, CEL, tones[1] + 24, 52, beat * 0.8)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 26, 1.8); n(t, DR, 36, v - 8, 0.3)
    if big: n(t, BASS, 28, 106, 1.2)


def stab(t, chord="C", v=98, d=0.35):
    root, tones = CH[chord]
    for k in tones: n(t, PNO, k + 12, v, d); n(t, VIB, k + 12, v - 16, d + 0.3)
    n(t, BASS, root - 12, 100, d)


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 84, 0.5)


def bells_up(t):
    for i, k in enumerate((72, 76, 79, 84, 88)): n(t + i * 0.05, CEL, k, 82, 0.45)


# ---- cues ----
stab(0.0, "C", 94); bells_up(0.02)
waltz(0.3, S["S2"] - 0.05, "main", 2, "main")
hit(S["S2"] + 0.02, 96); stab(Tw("i3", "fifteen", -0.1), "Dm", 92, 0.6); frost(S["S2"] + 0.4, S["S4"] - 0.05)
waltz(S["S4"], S["S6"] - 0.1, "main", 2, "lift")
for i, k in enumerate((72, 74, 76, 79, 84)): n(S["S5"] + 0.15 + 0.14 * i, VIB, k + 12, 84, 0.4)
for sid in ("S6", "S10", "S13", "S17", "S22"): bells_up(S[sid] + 0.02)
waltz(S["S6"] + 0.4, S["S10"] - 0.1, "lift", 1)
stab(Tw("a2", "won't", -0.15), "Am", 96)
waltz(S["S10"] + 0.4, S["S13"] - 0.1, "main", 2, "main")
stab(Tw("b2", "fail", -0.1), "Dm", 90)
frost(S["S13"] + 0.4, S["S17"] - 0.1)
waltz(S["S17"] + 0.4, S["S22"] - 0.1, "lift", 2, "lift")
sparkle(Tw("d4", "three", -0.15), 84); stab(Tw("d4", "Seven", -0.15), "G", 100)
waltz(S["S22"] + 0.4, S["S26"] - 0.1, "main", 2, "main")
stab(Tw("e5", "next", -0.2), "C", 100); sparkle(Tw("e5", "next", -0.1), 88)
frost(S["S26"], S["S27"] - 0.05)
waltz(S["S27"], S["S28"] - 0.05, "lift", 2, "lift"); sparkle(Tw("t3", "street.", -0.3), 86)
waltz(S["S28"], END - 1.2, "end", 3, "end")
for k in CH["C"][1]: n(END - 1.2, PNO, k + 12, 88, 0.6); n(END - 1.2, PAD, k, 62, 1.4)
n(END - 1.2, BASS, 24, 100, 1.2); hit(END - 1.2, 88); sparkle(END - 1.1, 84)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S2", "S4", "S6", "S10", "S13", "S17", "S22", "S26", "S28")] + [END + 3]))
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
