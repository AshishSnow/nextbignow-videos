"""City-pop score for the retro anime pilot (HOW THEY GOT SO BIG ep 3, Michelin; new genre, GeneralUser GS): 112 bpm, Rhodes chords,
slap/synth bass, gated-snare drum machine with claps, synth-brass stabs on every eyecatch, a square-lead hook; drops to Rhodes + pad for
the workbench 'ouch', a bright key-change lift for the stars, and a big ending."""
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
PROG = {EP: 4, BASS: 38, BRASS: 62, LEAD: 80, PAD: 89, GTR: 28}
VOL = {EP: 84, BASS: 104, BRASS: 82, LEAD: 70, PAD: 52, GTR: 64, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# major-7 city-pop changes (in F, lift to G)
CH = {"Fmaj7": (41, [64, 65, 69, 72]), "Em7": (40, [62, 64, 67, 71]), "Dm7": (38, [60, 62, 65, 69]), "Bbmaj7": (46, [62, 65, 69, 70]),
      "C7sus": (36, [60, 65, 67, 70]), "Am7": (45, [60, 64, 67, 69]), "Gmaj7": (43, [66, 67, 71, 74]), "F#m7": (42, [64, 66, 69, 73]),
      "Em7b": (40, [64, 67, 71, 74]), "Cmaj7": (36, [64, 67, 71, 72]), "D7sus": (38, [62, 67, 69, 72])}
PROGS = {"main": ["Fmaj7", "Em7", "Dm7", "C7sus"], "push": ["Bbmaj7", "Am7", "Dm7", "C7sus"], "dark": ["Dm7", "Bbmaj7", "Dm7", "Am7"],
         "lift": ["Gmaj7", "F#m7", "Em7b", "D7sus"], "end": ["Cmaj7", "D7sus", "Gmaj7", "Gmaj7"]}
BPM = 112; beat = 60 / BPM
HOOK = [(0, 72, 0.5), (0.5, 74, 0.5), (1, 76, 0.75), (2, 74, 0.5), (2.5, 72, 0.5), (3, 69, 1.0)]


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
stab(0.0, "Fmaj7", 90)
band(0.15, S["S_i2"] - 0.03, "main", 1)
stab(S["S_i2"], "C7sus", 104); band(S["S_i2"] + 0.05, S["S_i3"] - 0.04, "main", 2)
for ti, kind in CUES:
    if kind == "slam": stab(ti - 0.02, "C7sus", 96)
band(S["S_i3"], S["S_s1"] - 0.04, "main", 3, hook=True)
band(S["S_s1"], S["S_a1"] - 0.04, "push", 2)
band(S["S_a1"], S["S_b1"] - 0.04, "main", 3, hook=True); riser(S["S_a4b"] - 0.6); stab(S["S_a4b"], "Fmaj7", 104)
band(S["S_b1"], S["S_b2b"] - 0.04, "dark", 1)
stab(S["S_b2b"], "Bbmaj7", 110); band(S["S_b2b"] + 0.3, S["S_c1"] - 0.04, "dark", 2)
band(S["S_c1"], S["S_c4"] - 0.04, "push", 2)
riser(S["S_c4"] - 0.6); band(S["S_c4"], S["S_d1"] - 0.04, "lift", 3, hook=True, shift=0)
band(S["S_d1"], S["S_z1"] - 0.04, "lift", 2)
band(S["S_z1"], END - 1.4, "end", 3, hook=True)
for k in CH["Gmaj7"][1]: n(END - 1.4, EP, k, 80, 1.2); n(END - 1.4, PAD, k, 50, 1.4); n(END - 1.4, BRASS, k, 90, 0.8)
n(END - 1.4, BASS, 31, 110, 1.2); n(END - 1.4, DR, 49, 110, 1.0)


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
mus = mus + 0.22 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)   # big 80s plate
d_ = int(0.012 * SR); mus[:, 1] = np.concatenate([np.zeros(d_, np.float32), mus[:-d_, 1]])                    # stereo chorus-ish width
mus = signal.sosfilt(signal.butter(2, [38, 15000], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.25) / np.tanh(1.25)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
