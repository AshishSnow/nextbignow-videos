"""'Coin-op disco' for HOW IT WORKS ep 6 (cash vs card rewards; new genre, GeneralUser GS): four-on-the-floor kick, open hats on the
off-beats, octave-jumping finger bass, string-section stabs, clavinet chops, glockenspiel coin-chimes on every coin hop and a 'cha-ching'
marimba run on the money lines; the band drops to bass + hats for the 'nothing back' beat and the economists' caveat."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
GLK, CLV, BASS, MAR, STR, BRS, PAD, DR = 0, 1, 2, 3, 4, 5, 6, 9
PROG = {GLK: 9, CLV: 7, BASS: 33, MAR: 12, STR: 48, BRS: 61, PAD: 89}
VOL = {GLK: 80, CLV: 74, BASS: 96, MAR: 84, STR: 78, BRS: 72, PAD: 34, DR: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (33, [57, 60, 64, 67]), "Dm": (38, [57, 60, 62, 65]), "G": (31, [55, 59, 62, 67]), "C": (36, [55, 60, 64, 67]),
      "F": (41, [57, 60, 65, 69]), "E7": (40, [56, 59, 62, 64]), "Bb": (34, [58, 62, 65, 70])}
PROGS = {"main": ["Am", "Dm", "G", "C"], "fee": ["Dm", "Am", "E7", "Am"], "bank": ["F", "G", "Am", "Am"], "you": ["Am", "F", "C", "G"],
         "other": ["C", "F", "C", "G"], "end": ["F", "G", "C", "C"]}
BPM = 116; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 kick + hats + bass, 2 + clav chops + strings pad stab, 3 + claps + glock answers"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.04: break
            n(tq, DR, 36, 78 if q == 0 else 70, 0.1)
            if tq + beat / 2 < t1 - 0.04: n(tq + beat / 2, DR, 46, 50, 0.12)
            for e in (0, 0.5):   # octave bass
                if tq + e * beat < t1 - 0.04: n(tq + e * beat, BASS, root + (12 if e else 0), 84 if e == 0 else 72, beat * 0.42)
            if level >= 3 and q in (1, 3): n(tq, DR, 39, 56, 0.1)
        if level >= 2:
            for e16 in (1, 3, 6, 9, 11, 14):
                ts = t + e16 * beat / 4
                if ts < t1 - 0.04:
                    for k in tones[1:]: n(ts, CLV, k + 12, 58, beat * 0.18)
            if t < t1 - 0.04:
                for k in tones: n(t, STR, k + 12, 56, min(bar * 0.9, t1 - t))
        if level >= 3 and b % 2 == 1 and t + 2.5 * beat < t1 - 0.04:
            for i, k in enumerate((tones[3], tones[2], tones[3] + 5)): n(t + (2.5 + i * 0.25) * beat, GLK, k + 12, 64, beat * 0.4)
        t += bar; b += 1


def chime(t, k=84, v=72): n(t, GLK, k, v, 0.8)


def kaching(t, notes=(72, 76, 79, 84), step=0.08, v=86):
    for i, k in enumerate(notes): n(t + i * step, MAR, k, v, 0.4)


def stab(t, chord="Am", v=90, d=0.5):
    root, tones = CH[chord]
    for k in tones: n(t, STR, k + 12, v, d); n(t, BRS, k, v - 14, d * 0.7)
    n(t, BASS, root, 98, d); n(t, DR, 49 if v > 90 else 57, 72, 0.6)


def drop(t, d=1.2):
    """band drop: bass + hats only"""
    for q in range(int(d / (beat / 2))):
        n(t + q * beat / 2, DR, 42, 40, 0.08)


# ---- cues ----
for i in range(int((L0("i2") - 0.1) / 1.15) + 1): chime(i * 1.15 + 0.55, 84 if i % 2 == 0 else 88, 70)   # coin hop landings (frame 0 loop)
band(0.0, L0("i2") - 0.05, "main", 1)
kaching(TT("i1", "rewards?", 0.85) - 0.05)
band(S["S_i2"], S["S_i4"] - 0.04, "main", 2)
chime(TT("i2", "taps", 0.4), 91, 78)
stab(TT("i3", "Only", 0.3) - 0.03, "E7", 86, 0.5)
band(S["S_i4"], S["S_a1"] - 0.04, "main", 2)
for i in range(4): chime(TT("i4", "Four", 0.3) - 0.5 + i * 0.25, (72, 76, 79, 84)[i], 70)
band(S["S_a1"], S["S_b1"] - 0.04, "fee", 3)
stab(TT("a3", "billion", 0.3) - 0.03, "Dm", 94, 0.7); kaching(TT("a3", "billion", 0.3) + 0.1, (84, 88, 91), 0.07)
band(S["S_b1"], S["S_c1"] - 0.04, "main", 2)
stab(TT("b2", "baked", 0.3) - 0.03, "Am", 88, 0.5)
band(S["S_c1"], S["S_d1"] - 0.04, "bank", 3); kaching(TT("c2", "rewards.", 0.3) - 0.05, (79, 84, 88, 91), 0.07)
band(S["S_d1"], TT("d2", "His", 0.3) - 0.05, "you", 2)
drop(TT("d2", "His", 0.3) - 0.05, 1.6)
stab(TT("d2", "nothing", 0.3) - 0.03, "E7", 90, 0.7)
band(S["S_d3"], S["S_d5"] - 0.04, "you", 2); stab(TT("d4", "hundred", 0.3) - 0.03, "Am", 92, 0.6); kaching(TT("d4", "hundred", 0.3) + 0.1)
band(S["S_d5"], S["S_e1"] - 0.04, "main", 1)
band(S["S_e1"], S["S_e2"] - 0.04, "other", 2)
drop(S["S_e2"], max(1.0, S["S_f2"] - S["S_e2"] - 0.1)); band(S["S_e2"], S["S_f2"] - 0.04, "fee", 1)
band(S["S_f2"], S["S_t1"] - 0.04, "other", 3); stab(TT("f2", "Banned", 0.3) - 0.03, "C", 94, 0.6)
band(S["S_t1"], S["S_end"] - 0.05, "you", 3); chime(TT("t1", "Ask", 0.3), 88, 80)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["C"][1]: n(END - 1.3, STR, k + 12, 88, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
kaching(END - 1.25); n(END - 1.3, BASS, 36, 96, 1.0)


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
