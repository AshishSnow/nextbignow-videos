"""Classroom acoustic-pop score for HOW IT WORKS ep 2 (whiteboard episode; new genre, GeneralUser GS): ukulele strums, pizzicato strings, glockenspiel, upright bass, claps + shaker; a glock motif that gains one note per pie slice; the band drops to pizz only for the catch. Clean master (no lo-fi dust) to match the white board."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
UKE, PIZZ, BASS, GLK, PAD, MAR, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {UKE: 24, PIZZ: 45, BASS: 32, GLK: 9, PAD: 49, MAR: 12}
VOL = {UKE: 78, PIZZ: 82, BASS: 100, GLK: 84, PAD: 44, MAR: 70, DR: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (48, [60, 64, 67, 72]), "G": (43, [59, 62, 67, 71]), "Am": (45, [60, 64, 69, 72]), "F": (41, [60, 65, 69, 72]),
      "Dm": (50, [62, 65, 69, 74]), "E7": (40, [59, 62, 64, 68]), "Fmaj7": (41, [60, 64, 65, 69]), "G7": (43, [59, 62, 65, 67])}
PROGS = {"main": ["C", "G", "Am", "F"], "lift": ["F", "G", "C", "Am"], "dark": ["Am", "Dm", "E7", "Am"], "end": ["F", "G7", "C", "C"]}
BPM = 108; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 pizz + pad, 2 + uke strums + bass + claps, 3 + shaker + marimba answers"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % 4]]
        for q in (0, 1, 2, 3):
            if t + q * beat < t1 - 0.05: n(t + q * beat, PIZZ, tones[q % 3] + (0 if q % 2 else 12) - 12, 70 - 6 * (q % 2), beat * 0.4)
        n(t, PAD, tones[0], 34, bar * 0.95)
        if level >= 2:
            for q, d_ in ((0, 1), (1, -1), (1.5, 1), (2.5, -1), (3, 1)):
                if t + q * beat < t1 - 0.05:
                    for j, k in enumerate(tones if d_ > 0 else tones[::-1]): n(t + q * beat + j * 0.012, UKE, k, 64 - j * 3 - (8 if q % 1 else 0), beat * 0.45)
            for q in (0, 2):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, root - 12 if root > 44 else root, 96, beat * 0.8)
            for q in (1, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 39, 64, 0.08)
            n(t, DR, 36, 70, 0.1)
        if level >= 3:
            for s_ in range(8):
                ts = t + s_ * beat / 2
                if ts < t1 - 0.03: n(ts, DR, 70, 40 + (12 if s_ % 2 else 0), 0.05)
            if b % 2 == 1:
                for q, k in ((3, tones[1] + 12), (3.5, tones[2] + 12)):
                    if t + q * beat < t1 - 0.05: n(t + q * beat, MAR, k, 66, beat * 0.4)
        t += bar; b += 1


GM = [84, 86, 88, 91, 93]     # the slice motif: slice n plays n notes


def motif(t, k, v=86):
    for i in range(k): n(t + i * 0.13, GLK, GM[i], v, 0.6)


def stab(t, chord="C", v=82, d=0.5):
    root, tones = CH[chord]
    for k in tones: n(t, PIZZ, k, v, d); n(t, GLK, k + 12, v - 30, d)
    n(t, BASS, root - 12 if root > 44 else root, 96, d)


# ---- cues ----
stab(0.0, "Am", 76)
band(0.2, S["S_i2"] - 0.03, "dark", 1); stab(TT("i1", "earn?", 0.85) - 0.04, "E7", 86)
band(S["S_i2"], S["S_i3"] - 0.03, "main", 2)
band(S["S_i3"], S["S_i4"] - 0.03, "dark", 2); stab(TT("i3", "age.", 0.9) - 0.03, "Am", 84)
band(S["S_i4"], S["S_i5"] - 0.03, "main", 2)
band(S["S_i5"], S["S_a1"] - 0.05, "lift", 2); motif(TT("i5", "Five", 0.4) - 0.05, 5, 80); stab(TT("i5", "last", 0.6) - 0.03, "E7", 80)
ids = ["S_a1", "S_b1", "S_c1", "S_d1", "S_e1"]
nxt = {"S_a1": "S_a2", "S_b1": "S_b2", "S_c1": "S_c2", "S_d1": "S_d3", "S_e1": "S_e2"}
for i, sid in enumerate(ids):
    motif(S[sid] + 0.25, i + 1, 90)
    band(S[sid] + 0.2, S[nxt[sid]] - 0.04, "main" if i % 2 == 0 else "lift", 3)
band(S["S_a2"], S["S_b1"] - 0.05, "main", 3)
band(S["S_b2"], S["S_c1"] - 0.05, "lift", 2)
band(S["S_c2"], S["S_c3"] - 0.04, "main", 3)
band(S["S_c3"], S["S_d1"] - 0.05, "dark", 2); stab(TT("c3", "rest", 0.6) - 0.03, "E7", 86, 0.8)
band(S["S_d3"], S["S_e1"] - 0.05, "main", 2)
band(S["S_e2"], S["S_e3"] - 0.04, "main", 2); stab(TT("e1", "catch.", 0.85) - 0.03, "E7", 90, 0.9)
# the catch: band out, pizz + pad only, then back in for the fix
band(S["S_e3"], L0("e5") - 0.05, "dark", 1)
band(L0("e5") - 0.02, S["S_f1"] - 0.05, "lift", 2)
band(S["S_f1"], S["S_f2"] - 0.05, "main", 2); stab(TT("f1", "income", 0.75) - 0.03, "Am", 82)
band(S["S_f2"], S["S_t1"] - 0.05, "dark", 2); stab(TT("f2", "five", 0.7) - 0.03, "E7", 86)
band(S["S_t1"], S["S_end"] - 0.05, "lift", 3)
band(S["S_end"], END - 1.3, "end", 3); motif(TT("z2", "Send", 0.1), 5, 80)
for k in CH["C"][1]: n(END - 1.3, UKE, k, 76, 1.0); n(END - 1.3, PAD, k, 46, 1.3)
n(END - 1.3, BASS, 36, 96, 1.2); motif(END - 1.25, 5, 84)


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
