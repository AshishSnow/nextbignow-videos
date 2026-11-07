"""'Epic but small' for HOW IT WORKS ep 4 (Prime 'Iliad'; new genre, GeneralUser GS): a lyre-like harp arpeggio in D dorian over pizzicato strings and a low frame-drum pulse, a solo horn call for the two doors, a lone timpani roll + gavel stop at the settlement, and the harp turning bright major (D Lydian lift) when the doors are rebuilt."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
HRP, PIZZ, HRN, PAD, TIM, FLU, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {HRP: 46, PIZZ: 45, HRN: 60, PAD: 49, TIM: 47, FLU: 73}
VOL = {HRP: 92, PIZZ: 70, HRN: 72, PAD: 38, TIM: 80, FLU: 66, DR: 64}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Dm": (38, [62, 65, 69, 74]), "C": (36, [60, 64, 67, 72]), "G": (43, [62, 67, 71, 74]), "Am": (45, [60, 64, 69, 72]),
      "F": (41, [60, 65, 69, 72]), "Bb": (46, [62, 65, 70, 74]), "D": (38, [62, 66, 69, 74]), "E": (40, [64, 68, 71, 76])}
PROGS = {"main": ["Dm", "C", "Dm", "G"], "dark": ["Dm", "Bb", "Am", "Dm"], "lift": ["D", "E", "D", "G"], "end": ["F", "G", "D", "D"]}
BPM = 92; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 harp alone, 2 + pizzicato + pad, 3 + frame-drum pulse"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        arp = [tones[0], tones[1], tones[2], tones[3], tones[2] + 12, tones[3], tones[2], tones[1]]
        for i, k in enumerate(arp):
            ts = t + i * beat / 2
            if ts < t1 - 0.04: n(ts, HRP, k, 74 + (12 if i == 0 else 0), beat * 1.2)
        n(t, HRP, root, 70, bar * 0.9)
        if level >= 2:
            for q in (0, 2):
                if t + q * beat < t1 - 0.05: n(t + q * beat, PIZZ, root + (0 if q == 0 else 7), 80, beat * 0.5)
            n(t, PAD, tones[0], 30, bar * 0.95); n(t, PAD, tones[2], 26, bar * 0.95)
        if level >= 3:
            for q in (0, 1.5, 2, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 41 if q in (0, 2) else 45, 50 if q == 0 else 36, 0.1)
        t += bar; b += 1


def horn(t, notes=(62, 69, 67, 69), v=80, step=0.32):
    for i, k in enumerate(notes): n(t + i * step, HRN, k, v, step * (2.4 if i == len(notes) - 1 else 1.0))


def stab(t, chord="Dm", v=86, d=0.8):
    root, tones = CH[chord]
    for k in tones: n(t, HRP, k, v, d); n(t, PIZZ, k, v - 18, d * 0.5)
    n(t, TIM, root, 96, d)


def roll(t, d=1.2, k=38, v0=40, v1=96):
    m_ = int(d / 0.06)
    for i in range(m_): n(t + i * 0.06, TIM, k, v0 + (v1 - v0) * i / m_, 0.07)


# ---- cues ----
for i, k in enumerate((62, 65, 69, 74, 77)): n(0.0 + i * 0.07, HRP, k, 80, 2.0)     # frame 0: a strummed lyre chord
band(0.4, L0("i2") - 0.05, "dark", 1)
stab(L0("i2") - 0.03, "Dm", 92, 1.4); horn(L0("i2") + 0.15, (62, 69, 74), 82)
band(L0("i2") + 1.2, S["S_i4"] - 0.04, "main", 2)
roll(TT("i4", "two", 0.3) - 1.0, 0.95); stab(TT("i4", "two", 0.3) - 0.03, "Bb", 92)
band(S["S_i4"] + 0.2, S["S_a1"] - 0.04, "main", 2); horn(L0("i5") + 0.1, (62, 69), 76)
band(S["S_a1"], S["S_b1"] - 0.04, "main", 3); n(S["S_a1"] + 0.1, FLU, 74, 70, 0.5)
band(S["S_b1"], S["S_c1"] - 0.04, "dark", 3); horn(S["S_b1"] + 0.1, (62, 69, 68), 76)
band(S["S_c1"], S["S_d1"] - 0.04, "dark", 1)
band(S["S_d1"], S["S_d2"] - 0.05, "dark", 2); roll(TT("d1", "settled.", 0.4) - 1.1, 1.05, 38, 36, 100)
stab(TT("d1", "settled.", 0.4) - 0.03, "Dm", 96, 1.0)
band(S["S_d2"] + 0.1, S["S_d3"] - 0.04, "main", 2)
band(S["S_d3"], S["S_e1"] - 0.04, "main", 1)
band(S["S_e1"], S["S_t1"] - 0.04, "lift", 3); horn(S["S_e1"] + 0.1, (62, 66, 69, 74), 84); n(TT("e2", "same", 0.3), FLU, 81, 72, 0.6)
band(S["S_t1"], S["S_end"] - 0.05, "dark", 2)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["D"][1]: n(END - 1.3, HRP, k, 84, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
horn(END - 1.25, (62, 69, 74), 82); n(END - 1.3, TIM, 38, 90, 1.0)


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


mus = render(sorted(ev), END)
rng = np.random.default_rng(6); irl = int(0.9 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.28)[:, None]; ir[: int(0.01 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 4200, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
N_ = len(mus)
mus = signal.sosfilt(signal.butter(2, [45, 14000], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
