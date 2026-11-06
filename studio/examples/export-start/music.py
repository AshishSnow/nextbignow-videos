"""Baroque chamber groove for HOW TO START ep 7 (exporting; new genre, GeneralUser GS): harpsichord running sixteenths, pizzicato strings, a walking cello/bass line, a soft string pad and a recorder motif that gains one note per step; it drops to harpsichord alone for the twist ('only covers your side')."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
HPS, PIZZ, BASS, REC, PAD, CEL, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {HPS: 6, PIZZ: 45, BASS: 43, REC: 74, PAD: 48, CEL: 42}
VOL = {HPS: 84, PIZZ: 70, BASS: 96, REC: 78, PAD: 40, CEL: 70, DR: 60}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"D": (38, [62, 66, 69, 74]), "A": (45, [61, 64, 69, 73]), "Bm": (47, [62, 66, 71, 74]), "F#m": (42, [61, 66, 69, 73]),
      "G": (43, [62, 67, 71, 74]), "Em": (40, [64, 67, 71, 76]), "A7": (45, [61, 64, 67, 69])}
PROGS = {"main": ["D", "A", "Bm", "F#m", "G", "D", "G", "A"], "lift": ["G", "A", "D", "Bm", "Em", "A", "D", "A7"],
         "dark": ["Bm", "F#m", "G", "F#m", "Em", "Bm", "Em", "F#m"], "end": ["G", "A7", "D", "D"]}
BPM = 104; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 harpsichord alone, 2 + walking bass + pad, 3 + pizzicato answers + tambourine ticks"""
    half = 2 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        pat = [tones[0], tones[2], tones[1], tones[2], tones[3], tones[2], tones[1], tones[2]]   # Alberti-style sixteenths
        for i, k in enumerate(pat):
            ts = t + i * beat / 4
            if ts < t1 - 0.04: n(ts, HPS, k, 70 + (10 if i % 4 == 0 else 0), beat * 0.3)
        n(t, HPS, root, 66, half * 0.9)
        if level >= 2:
            for q, off in ((0, 0), (1, 7 if b % 2 == 0 else 4)):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, root - 12 + off if root > 40 else root + off, 88, beat * 0.8)
            n(t, PAD, tones[0], 30, half * 0.95); n(t, PAD, tones[2], 26, half * 0.95)
        if level >= 3:
            if b % 2 == 1:
                for q, k in ((0.5, tones[3] + 12), (1, tones[2] + 12), (1.5, tones[1] + 12)):
                    if t + q * beat < t1 - 0.05: n(t + q * beat, PIZZ, k, 66, beat * 0.4)
            for q in (0.5, 1.5):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 54, 34, 0.05)
        t += half; b += 1


GM = [81, 83, 85, 86]     # the step motif (recorder): step n plays n notes


def motif(t, k, v=84):
    for i in range(k): n(t + i * 0.15, REC, GM[i], v, 0.4)


def stab(t, chord="D", v=82, d=0.5):
    root, tones = CH[chord]
    for k in tones: n(t, HPS, k, v, d); n(t, PIZZ, k + 12, v - 20, d)
    n(t, BASS, root - 12 if root > 40 else root, 96, d); n(t, CEL, root + 12, 70, d)


# ---- cues ----
stab(0.0, "D", 78)
band(0.15, S["S_i2"] - 0.03, "main", 2); stab(TT("i1", "tax", 0.6) - 0.03, "Bm", 86)
band(S["S_i2"], S["S_i3"] - 0.03, "dark", 1); n(S["S_i2"] + 0.1, CEL, 50, 60, 2.5)
band(S["S_i3"], S["S_i4"] - 0.03, "main", 2)
band(S["S_i4"], S["S_a1"] - 0.04, "lift", 2); motif(TT("i4", "four", 0.3), 4, 78); stab(TT("i4", "beginners.", 0.4) - 0.03, "F#m", 82)
for i, sid in enumerate(("S_a1", "S_b1", "S_c1", "S_d1")):
    nxt = ("S_b1", "S_c1", "S_d1", "S_e1")[i]
    motif(S[sid] + 0.2, i + 1, 86)
    if sid == "S_c1":
        band(S[sid] + 0.15, S["S_c3"] - 0.04, "dark", 2); band(S["S_c3"], S[nxt] - 0.04, "lift", 3)
    else:
        band(S[sid] + 0.15, S[nxt] - 0.04, "main" if i % 2 == 0 else "lift", 3)
stab(TT("c2", "all.", 0.3) - 0.03, "Bm", 88)
stab(TT("c4", "hundreds", 0.3) - 0.03, "F#m", 86)
stab(TT("d3", "over", 0.4) - 0.03, "A", 84)
# the twist: harpsichord alone
band(S["S_e1"], S["S_t1"] - 0.05, "dark", 1); stab(TT("e2", "every", 0.4) - 0.03, "Em", 90, 0.9)
band(S["S_t1"], S["S_end"] - 0.05, "main", 3)
band(S["S_end"], END - 1.3, "end", 3); motif(TT("z2", "send", 0.2), 4, 80)
for k in CH["D"][1]: n(END - 1.3, HPS, k, 80, 1.0); n(END - 1.3, PAD, k, 40, 1.3)
n(END - 1.3, BASS, 38, 96, 1.2); motif(END - 1.25, 4, 84)


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
