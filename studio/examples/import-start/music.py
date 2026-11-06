"""Trade-route groove for HOW TO START ep 6 (importing; new genre, GeneralUser GS): steel drums, marimba, nylon guitar, bass, congas + shaker; a steel-drum motif that gains one note per step; the band drops to marimba + pad for the rule change."""
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
PROG = {UKE: 24, PIZZ: 114, BASS: 33, GLK: 114, PAD: 89, MAR: 12}
VOL = {UKE: 74, PIZZ: 70, BASS: 100, GLK: 86, PAD: 42, MAR: 82, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"D": (50, [62, 66, 69, 74]), "G": (43, [62, 67, 71, 74]), "A": (45, [61, 64, 69, 73]), "Bm": (47, [62, 66, 71, 74]),
      "Em": (40, [64, 67, 71, 76]), "F#m": (42, [61, 66, 69, 73]), "A7": (45, [61, 64, 67, 69])}
PROGS = {"main": ["D", "G", "A", "D"], "lift": ["G", "A", "Bm", "A"], "dark": ["Bm", "Em", "F#m", "Bm"], "end": ["G", "A7", "D", "D"]}
BPM = 100; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 marimba + pad, 2 + guitar + bass + congas, 3 + steel-drum answers + shaker"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % 4]]
        for q in (0, 0.75, 1.5, 2, 2.75, 3.5):
            if t + q * beat < t1 - 0.05: n(t + q * beat, MAR, tones[int(q * 4) % 4], 72 - (8 if q % 1 else 0), beat * 0.35)
        n(t, PAD, tones[0], 32, bar * 0.95)
        if level >= 2:
            for q in (0, 1.5, 2.5):
                if t + q * beat < t1 - 0.05:
                    for j, k in enumerate(tones[:3]): n(t + q * beat + j * 0.01, UKE, k - 12, 58 - j * 3, beat * 0.5)
            for q, off in ((0, 0), (1.5, 7), (2, 0), (3, 12)):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, root - 12 + off if root > 44 else root + off, 94, beat * 0.6)
            for q, k in ((0, 64), (1, 63), (1.5, 62), (2.5, 63), (3, 64), (3.5, 62)):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, k, 66, 0.08)
        if level >= 3:
            for s_ in range(8):
                ts = t + s_ * beat / 2
                if ts < t1 - 0.03: n(ts, DR, 82, 40 + (10 if s_ % 2 else 0), 0.05)
            if b % 2 == 1:
                for q, k in ((2.5, tones[2] + 12), (3, tones[3] + 12), (3.5, tones[1] + 12)):
                    if t + q * beat < t1 - 0.05: n(t + q * beat, PIZZ, k, 70, beat * 0.4)
        t += bar; b += 1


GM = [74, 78, 81, 86]     # the step motif (steel drum): step n plays n notes


def motif(t, k, v=88):
    for i in range(k): n(t + i * 0.14, GLK, GM[i], v, 0.5)


def stab(t, chord="D", v=82, d=0.5):
    root, tones = CH[chord]
    for k in tones: n(t, MAR, k, v, d); n(t, GLK, k + 12, v - 26, d)
    n(t, BASS, root - 12 if root > 44 else root, 96, d)


# ---- cues ----
stab(0.0, "Bm", 76)
band(0.2, S["S_i2"] - 0.03, "dark", 1); stab(TT("i1", "license?", 0.85) - 0.04, "A", 86)
band(S["S_i2"], S["S_i3"] - 0.03, "main", 2)
band(S["S_i3"], S["S_a1"] - 0.04, "lift", 2); motif(TT("i3", "four", 0.3), 4, 80); stab(TT("i3", "trips", 0.6) - 0.03, "F#m", 82)
for i, sid in enumerate(("S_a1", "S_b1", "S_c1", "S_d1")):
    nxt = ("S_b1", "S_c1", "S_d1", "S_e1")[i]
    motif(S[sid] + 0.2, i + 1, 90); band(S[sid] + 0.15, S[nxt] - 0.04, "main" if i % 2 == 0 else "lift", 3)
stab(TT("b3", "wrong", 0.3) - 0.03, "Bm", 84)
stab(TT("c3", "cheap.", 0.9) - 0.03, "F#m", 80)
# the rule change: band out, marimba + pad only
band(S["S_e1"], S["S_f1"] - 0.05, "dark", 1); stab(TT("e2", "suspended.", 0.5) - 0.03, "F#m", 92, 0.9)
band(S["S_f1"], S["S_t1"] - 0.04, "lift", 2)
band(S["S_t1"], S["S_end"] - 0.05, "main", 3)
band(S["S_end"], END - 1.3, "end", 3); motif(TT("z2", "send", 0.2), 4, 82)
for k in CH["D"][1]: n(END - 1.3, MAR, k, 80, 1.0); n(END - 1.3, PAD, k, 44, 1.3)
n(END - 1.3, BASS, 38, 96, 1.2); motif(END - 1.25, 4, 86)


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
