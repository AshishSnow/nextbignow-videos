"""Tropical-house score for HOW TO START ep 1, drone business (GeneralUser GS): marimba offbeats, pan flute, kalimba stabs, dark half-time for step 5."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
MAR, BASS, PLK, GLK, PAD, STR, TIMP, FLU, SUB, LEAD, SBR, KAL, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9
PROG = {MAR: 12, BASS: 38, PLK: 45, GLK: 9, PAD: 89, STR: 48, TIMP: 47, FLU: 75, SUB: 38, LEAD: 80, SBR: 62, KAL: 108}
VOL = {MAR: 96, BASS: 104, PLK: 86, GLK: 82, PAD: 64, STR: 78, TIMP: 104, FLU: 84, SUB: 100, LEAD: 70, SBR: 84, KAL: 90, DR: 96}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# tropical house in A major / F#m: I - V - vi - IV, bright and hopeful (new genre for the channel)
CH = {"A": (45, [61, 64, 69, 73]), "E": (40, [59, 64, 68, 71]), "F#m": (42, [61, 66, 69, 73]), "D": (38, [62, 66, 69, 74]),
      "Bm": (47, [62, 66, 71, 74]), "C#m": (49, [61, 64, 68, 73]), "Dm": (38, [62, 65, 69, 74]), "Bb": (46, [62, 65, 70, 74])}
PROGS = {"main": ["A", "E", "F#m", "D"], "lift": ["D", "E", "C#m", "F#m"], "dark": ["F#m", "D", "Bb", "C#m"], "end": ["D", "E", "A", "A"]}
BPM = 106


def groove(t0, t1, prog="main", level=2):
    beat = 60 / BPM; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            if level >= 1: n(tq, DR, 36, 96 if q % 2 == 0 else 84, 0.2)
            if level >= 2 and q in (1, 3): n(tq, DR, 39, 78, 0.15)
            n(tq + beat * 0.5, BASS, root - 12 + (12 if q % 2 else 0), 92, beat * 0.42)
            for k in tri[:3]: n(tq + beat * 0.5, MAR, k + 12, 70 + 6 * level, beat * 0.3)
            if level >= 2: n(tq + beat * 0.5, DR, 42, 58, 0.06); n(tq + beat * 0.75, DR, 70, 40, 0.05)
        for k in tri: n(t, PAD, k, 48 + 4 * level, bar * 0.95)
        if level >= 3:
            mel = [tri[3] + 12, tri[2] + 12, tri[3] + 12, tri[1] + 12 + 2]
            for i, k in enumerate(mel): n(t + i * beat * (1.5 if i % 2 else 1.0) , FLU, k, 70, beat * 0.8)
        t += bar; b += 1


def dark(t0, t1):
    beat = 60 / BPM * 2; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS["dark"][b % 4]]
        n(t, SUB, root - 12, 100, beat * 1.8); n(t, DR, 36, 104, 0.3); n(t + beat, DR, 38, 80, 0.2)
        for k in tri: n(t, STR, k - 12, 70, beat * 1.9)
        for j in range(4): n(t + j * beat * 0.5, PLK, tri[j % 4], 62, 0.2)
        t += beat * 2; b += 1


def hit(t, v=110, big=False):
    n(t, TIMP, 40, v - 10, 1.2); n(t, DR, 49, v - 16, 1.8); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 33, 110, 1.2); n(t, DR, 57, v - 10, 2.2)


def stab(t, chord="A", v=104, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, LEAD, k + 12, v - 20, d); n(t, SBR, k, v - 24, d); n(t, KAL, k + 12, v, d)
    n(t, BASS, root - 12, 100, d)


def riser(t_end, dur):
    m = int(dur / 0.06)
    for j in range(m): n(t_end - dur + j * 0.06, DR, 38, 20 + int(78 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((64, 66, 68, 69, 71, 73)): n(t_end - dur + i * dur / 6, STR, p, 50 + 8 * i, t_end - (t_end - dur + i * dur / 6))


def sparkle(t, base=81):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.06, GLK, k, 90, 0.5)


# ---- cues ----
for k in CH["A"][1]: n(0.0, PAD, k, 60, S["S1"]); n(0.0, KAL, k + 12, 84, 0.6)
n(0.0, BASS, 33, 92, 1.2); sparkle(0.05, 81)
groove(0.9, S["S1b"] - 0.05, "main", 2)
tc = Tw("i2", "three", -0.15); stab(tc, "A", 110); hit(tc, 106); sparkle(tc + 0.1, 85)
groove(S["S1b"] + 0.3, S["S2"] - 0.05, "main", 2)
groove(S["S2"], Tw("i3", "lose", -0.15), "lift", 1)
hit(Tw("i3", "lose", -0.1), 112, True); stab(Tw("i3", "lose", -0.1), "F#m", 110, 0.5)
for sid, ch in (("S3", "A"), ("S9", "D"), ("S12", "E"), ("S15", "A")):
    riser(S[sid], 0.7); stab(S[sid] + 0.02, ch, 110); sparkle(S[sid] + 0.1, 81)
groove(S["S3"] + 0.3, S["S9"] - 0.75, "main", 3)
for w_, l_ in (("seventy", "a4"), ("free", "a5")): sparkle(Tw(l_, w_, 0.15), 86)
hit(Tw("a2", "Part", -0.12), 100)
groove(S["S9"] + 0.3, S["S12"] - 0.75, "lift", 2)
stab(Tw("b2", "five", -0.15), "E", 106); sparkle(Tw("b3", "Remote", 0.0), 84)
groove(S["S12"] + 0.3, S["S13"] - 0.05, "main", 2)
hit(Tw("c2", "new", 0.25), 108); groove(S["S13"] + 0.4, S["S15"] - 0.75, "lift", 2)
groove(S["S15"] + 0.3, S["S19"] - 0.75, "main", 3)
for w_ in ("agents,", "roofers", "planners"): n(Tw("d2", w_, -0.05), KAL, 81, 96, 0.4)
riser(S["S19"], 0.9); hit(S["S19"], 116, True)
dark(S["S19"] + 0.1, S["S21"] - 0.05)
hit(Tw("t1", "seventy", -0.2), 122, True); stab(Tw("t1", "seventy", -0.2), "Bb", 112, 0.6)
stab(Tw("t2", "every", -0.2), "A", 110); sparkle(Tw("t2", "every", -0.1), 85)
groove(S["S21"] + 0.2, S["S23"] - 0.05, "main", 3)
groove(S["S23"], END - 1.4, "end", 3)
for k in CH["A"][1]: n(END - 1.4, MAR, k + 12, 92, 1.0); n(END - 1.4, PAD, k, 70, 1.8); n(END - 1.4, KAL, k + 12, 96, 1.2)
n(END - 1.4, BASS, 33, 104, 1.4); hit(END - 1.4, 100); sparkle(END - 1.3, 81)


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
cuts = sorted(set([0.0] + [S[k] for k in ("S1", "S2", "S3", "S9", "S12", "S15", "S19", "S21", "S23")] + [END + 3]))
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
