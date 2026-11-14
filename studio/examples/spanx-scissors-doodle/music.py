"""Quirky doodle-explainer score for the Spanx case study (13 Nov): 112 bpm, marimba + pizzicato + tuba bounce + nylon guitar,
glockenspiel hook, light kit; brass stab on each MOVE stamp; tense minor bed for the "I will kill you" beat; bright ending."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
EP, BASS, BRASS, LEAD, PAD, GTR, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {EP: 12, BASS: 58, BRASS: 61, LEAD: 9, PAD: 45, GTR: 24}
VOL = {EP: 92, BASS: 96, BRASS: 78, LEAD: 74, PAD: 80, GTR: 70, DR: 74}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# plain bright triads in C (doodle explainer bounce)
CH = {"C": (36, [60, 64, 67, 72]), "F": (41, [60, 65, 69, 72]), "G": (43, [62, 67, 71, 74]), "Am": (45, [60, 64, 69, 72]), "Dm": (38, [62, 65, 69, 74]),
      "E7": (40, [62, 64, 68, 71]), "G7": (43, [62, 65, 67, 71]), "Bb": (46, [62, 65, 70, 74])}
PROGS = {"main": ["C", "Am", "F", "G7"], "push": ["F", "G", "Am", "G7"], "dark": ["Am", "E7", "Am", "E7"],
         "lift": ["F", "G", "C", "C"], "end": ["F", "G7", "C", "C"], "bounce": ["C", "F", "C", "G7"]}
BPM = 112; beat = 60 / BPM
HOOK = [(0, 76, 0.5), (0.5, 79, 0.5), (1, 84, 0.5), (1.5, 79, 0.5), (2, 81, 0.75), (3, 79, 0.5), (3.5, 76, 0.5)]


def band(t0, t1, prog="main", level=2, hook=False, shift=0):
    """level 1 Rhodes + pad, 2 + slap bass + drum machine, 3 + guitar cuts, claps on 2 and 4, lead hook"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % 4]]; root += shift; tones = [k + shift for k in tones]
        for q in (0, 1.5, 2.5) if level >= 2 else (0, 2):
            if t + q * beat < t1 - 0.05:
                for j, k in enumerate(tones): n(t + q * beat + j * 0.012, EP, k, 70 - j * 4, beat * (0.9 if q else 1.3))
        n(t, PAD, tones[0], 36, bar * 0.95); n(t, PAD, tones[2], 30, bar * 0.95)
        if level >= 2:
            for q, off, v in ((0, 0, 104), (0.75, 12, 84), (1.5, 0, 96), (2.5, 7, 90), (3, 12, 86), (3.5, 10, 80)):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, root - 12 + off if root > 40 else root + off, v, beat * 0.4)
            for s_ in range(8):
                ts = t + s_ * beat / 2
                if ts < t1 - 0.03: n(ts, DR, 42, 58 + (14 if s_ % 2 == 0 else 0), 0.05)
            for q in (0, 2.5): n(t + q * beat, DR, 36, 100, 0.1) if t + q * beat < t1 - 0.03 else None
            for q in (1, 3): n(t + q * beat, DR, 38, 104, 0.1) if t + q * beat < t1 - 0.03 else None
        if level >= 3:
            for q in (1, 3): n(t + q * beat, DR, 39, 86, 0.1) if t + q * beat < t1 - 0.03 else None
            for q in (0.5, 1.5, 2.5, 3.5):
                if t + q * beat < t1 - 0.05: n(t + q * beat, GTR, tones[1] + 12, 70, beat * 0.25); n(t + q * beat, GTR, tones[3] + 12, 64, beat * 0.25)
        if hook and b % 2 == 0:
            for q, k, d in HOOK:
                if t + q * beat < t1 - 0.05: n(t + q * beat, LEAD, k + shift, 78, beat * d)
        t += bar; b += 1


def stab(t, chord="Fmaj7", v=96, d=0.45, shift=0):
    root, tones = CH[chord]
    for k in tones: n(t, BRASS, k + shift, v, d)
    n(t, BASS, root - 12 + shift if root > 40 else root + shift, 110, d); n(t, DR, 49, 100, 0.5); n(t, DR, 36, 110, 0.1)


def riser(t, d=0.6):
    for i in range(8): n(t + i * d / 8, LEAD, 72 + i * 2, 50 + i * 6, d / 8)


# ---- cues ----
stab(0.0, "C", 100)
band(0.1, S["S_i3"] - 0.03, "main", 3, hook=True)
band(S["S_i3"] + 0.05, S["S_a1"] - 0.03, "push", 2)
for k_ in ("S_b1", "S_b4", "S_c1", "S_d1", "S_e1"): stab(S[k_], "G7", 104)
band(S["S_a1"] + 0.05, S["S_b1"] - 0.03, "bounce", 2, hook=True)
band(S["S_b1"] + 0.05, S["S_c1"] - 0.03, "main", 2)
band(S["S_c1"] + 0.05, S["S_d1"] - 0.03, "dark", 1)
band(S["S_d1"] + 0.05, S["S_e1"] - 0.03, "push", 2)
band(S["S_e1"] + 0.05, S["S_f1"] - 0.03, "bounce", 3, hook=True)
riser(S["S_f1"] - 0.6); stab(S["S_f1"], "C", 108); band(S["S_f1"] + 0.05, S["S_t1"] - 0.03, "lift", 3, hook=True)
band(S["S_t1"] + 0.05, S["S_z1"] - 0.03, "main", 2)
band(S["S_z1"] + 0.05, END - 1.4, "end", 3, hook=True)
for k in CH["C"][1]: n(END - 1.4, EP, k, 84, 1.2); n(END - 1.4, PAD, k, 70, 0.6); n(END - 1.4, BRASS, k, 88, 0.8)
n(END - 1.4, BASS, 36, 110, 1.2); n(END - 1.4, DR, 49, 100, 1.0)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 25, True)   # TR-808-style kit if present (falls back to standard)
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
rng = np.random.default_rng(6); irl = int(1.2 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.42)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 5200, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.12 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)   # big 80s plate
d_ = int(0.012 * SR); mus[:, 1] = np.concatenate([np.zeros(d_, np.float32), mus[:-d_, 1]])                    # stereo chorus-ish width
mus = signal.sosfilt(signal.butter(2, [38, 15000], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.25) / np.tanh(1.25)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
