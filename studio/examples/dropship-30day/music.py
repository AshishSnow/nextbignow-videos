"""'Packing-tape skiffle' for HOW TO START ep 8 (dropshipping 30-day rule; new genre, GeneralUser GS): a strummed nylon-string "uke" in a bouncy 2-step shuffle, walking upright bass, hand-claps + brushed snare, a tin whistle hook on the reveals, a ticking woodblock clock under the deadline lines, and a tuba "uh-oh" on the penalty and the blame rule."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
UKE, BASS, WHI, GLK, TUBA, PAD, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {UKE: 24, BASS: 32, WHI: 78, GLK: 9, TUBA: 58, PAD: 89}
VOL = {UKE: 96, BASS: 92, WHI: 70, GLK: 64, TUBA: 78, PAD: 34, DR: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67, 72]), "F": (41, [60, 65, 69, 72]), "G": (43, [62, 67, 71, 74]), "Am": (45, [60, 64, 69, 72]),
      "Dm": (38, [62, 65, 69, 74]), "E7": (40, [62, 64, 68, 71]), "D7": (38, [60, 62, 66, 69]), "Bb": (46, [62, 65, 70, 74])}
PROGS = {"main": ["C", "Am", "F", "G"], "late": ["Am", "E7", "Am", "E7"], "money": ["F", "G", "C", "C"], "blame": ["Dm", "Bb", "Dm", "E7"],
         "uk": ["F", "C", "D7", "G"], "end": ["F", "G", "C", "C"]}
BPM = 112; beat = 60 / BPM; SW = 0.62   # shuffle: the off-beat 8th lands at 62 % of the beat


def band(t0, t1, prog="main", level=2, clock=False):
    """level 1 uke alone, 2 + walking bass + claps on 2 & 4, 3 + brushed snare shuffle + glock sparkle"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for q in range(4):
            for half in (0, SW):
                ts = t + (q + half) * beat
                if ts >= t1 - 0.04: continue
                down = half == 0; v = (78 if q in (0, 2) else 66) if down else 52
                for j, k in enumerate(tones): n(ts + j * 0.012 * (1 if down else -1), UKE, k, v - j * 3, beat * (0.42 if down else 0.3))
        if level >= 2:
            walk = [root, root + 4 if tones[1] - 60 in (4, 5) else root + 3, root + 7, root + 9 - (0 if b % 2 else 2)]
            for q, k in enumerate(walk):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, k, 84 if q == 0 else 72, beat * 0.8)
            for q in (1, 3):
                if t + q * beat < t1 - 0.05: n(t + q * beat, DR, 39, 64, 0.1)
        if level >= 3:
            for q in range(4):
                for half in (0, SW):
                    if t + (q + half) * beat < t1 - 0.04: n(t + (q + half) * beat, DR, 38 if (q in (1, 3) and half == 0) else 42, 40 if half else 48, 0.08)
            if b % 2 == 1: n(t + 3.5 * beat, GLK, tones[3] + 12, 58, 0.4)
        if clock:
            for q in range(8):
                if t + q * beat / 2 < t1 - 0.04: n(t + q * beat / 2, DR, 76 if q % 2 == 0 else 77, 54, 0.05)
        t += bar; b += 1


def whistle(t, notes=(76, 79, 81, 79), v=82, step=0.2):
    for i, k in enumerate(notes): n(t + i * step, WHI, k, v, step * (2.6 if i == len(notes) - 1 else 0.95))


def stab(t, chord="C", v=88, d=0.6):
    root, tones = CH[chord]
    for k in tones: n(t, UKE, k, v, d)
    n(t, BASS, root, 96, d); n(t, DR, 49 if v > 90 else 57, 70, 0.6)


def uhoh(t, k=(41, 36), v=88):
    n(t, TUBA, k[0], v, 0.28); n(t + 0.3, TUBA, k[1], v, 0.7)


# ---- cues ----
for i, k in enumerate((60, 64, 67, 72, 76)): n(0.0 + i * 0.03, UKE, k, 84, 1.2)    # frame 0: a bright strum
band(0.3, L0("i2") - 0.05, "main", 1, clock=True)
stab(L0("i2") - 0.03, "Am", 92, 1.0); uhoh(TT("i2", "fifty-three", 0.6) - 0.1)
band(L0("i2") + 1.0, S["S_i4"] - 0.04, "main", 2)
whistle(TT("i3", "straight", 0.6), (79, 81, 84, 81))
band(S["S_i4"], S["S_a1"] - 0.04, "main", 2); stab(TT("i4", "Four", 0.3) - 0.03, "F", 88)
band(S["S_a1"], S["S_a3"] - 0.04, "main", 3)
band(S["S_a3"], S["S_b1"] - 0.04, "main", 2, clock=True); stab(TT("a3", "thirty", 0.5) - 0.03, "G", 90)
band(S["S_b1"], S["S_c1"] - 0.04, "late", 2)
whistle(TT("b2", "new", 0.4), (76, 79, 81))
band(S["S_c1"], S["S_d1"] - 0.04, "money", 3); n(TT("c2", "seven", 0.4), GLK, 84, 70, 0.5)
uhoh(TT("c2", "doesn't", 0.5) - 0.1, (43, 38), 80); stab(TT("c3", "twenty", 0.3) - 0.2, "C", 94, 0.8)
band(S["S_d1"], S["S_d2"] - 0.04, "blame", 1)
stab(TT("d2", "seller.", 0.4) - 0.03, "Dm", 94, 0.9); uhoh(TT("d2", "seller.", 0.4) + 0.1, (38, 33), 90)
band(S["S_d2"] + 0.8, S["S_e1"] - 0.04, "blame", 2)
band(S["S_e1"], S["S_t1"] - 0.04, "uk", 3); whistle(S["S_e1"] + 0.1, (74, 78, 81, 79))
band(S["S_t1"], S["S_end"] - 0.05, "main", 2, clock=True)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["C"][1]: n(END - 1.3, UKE, k, 90, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
whistle(END - 1.25, (79, 84), 84); n(END - 1.3, BASS, 36, 96, 1.0)


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
