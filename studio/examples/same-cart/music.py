"""'Checkout cha-cha' for HOW IT WORKS ep 5 (same cart, five prices; new genre, GeneralUser GS): a supermarket-radio cha-cha-cha —
vibraphone melody, piano montuno, upright-bass tumbao, guiro + cowbell + claves + congas, the 'cha-cha' kick on 4-and; a 5-note
cash-register marimba run on the five price tags (each a different note), a muted-trumpet 'wah' on the money lines, and a
flute lift when the tests end."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
VIB, PNO, BASS, MAR, TPT, FLU, PAD, DR = 0, 1, 2, 3, 4, 5, 6, 9
PROG = {VIB: 11, PNO: 0, BASS: 32, MAR: 12, TPT: 59, FLU: 73, PAD: 89}
VOL = {VIB: 84, PNO: 80, BASS: 92, MAR: 86, TPT: 70, FLU: 72, PAD: 34, DR: 66}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67, 71]), "Dm": (38, [60, 62, 65, 69]), "G7": (43, [59, 62, 65, 67]), "Am": (45, [60, 64, 67, 69]),
      "F": (41, [60, 64, 65, 69]), "E7": (40, [59, 62, 64, 68]), "Bb": (46, [62, 65, 69, 70]), "A7": (45, [61, 64, 67, 69])}
PROGS = {"main": ["C", "Am", "Dm", "G7"], "test": ["Am", "E7", "Am", "E7"], "side": ["F", "C", "Dm", "G7"], "money": ["Dm", "G7", "C", "A7"],
         "end": ["F", "G7", "C", "C"], "big": ["Dm", "Bb", "C", "E7"]}
BPM = 118; beat = 60 / BPM


def band(t0, t1, prog="main", level=2, guiro=True):
    """level 1 piano montuno + guiro, 2 + tumbao bass + cowbell + cha-cha kick, 3 + congas + vibes answer"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for e8, on in enumerate((1, 0, 1, 1, 0, 1, 1, 0)):   # montuno: syncopated 8ths
            ts = t + e8 * beat / 2
            if on and ts < t1 - 0.04:
                for j, k in enumerate(tones[1:] if e8 % 2 else tones[:3]): n(ts, PNO, k + 12, 66 - j * 4, beat * 0.4)
        if guiro:
            for q in range(4):
                if t + q * beat < t1 - 0.04: n(t + q * beat, DR, 74 if q % 2 == 0 else 73, 46, 0.12)
        if level >= 2:
            for tt_, k in ((1.5, root + 7), (3.0, root + 12), (3.5, root)):   # tumbao
                if t + tt_ * beat < t1 - 0.05: n(t + tt_ * beat, BASS, k, 82, beat * 0.45)
            if b == 0 and t < t1 - 0.05: n(t, BASS, root, 80, beat * 0.9)
            for q in range(4):
                if t + q * beat < t1 - 0.04: n(t + q * beat, DR, 56, 50 if q else 60, 0.1)
            for tt_ in (3.0, 3.5):
                if t + tt_ * beat < t1 - 0.04: n(t + tt_ * beat, DR, 36, 64, 0.1)
            if t < t1 - 0.04: n(t, DR, 36, 70, 0.1)
        if level >= 3:
            for tt_, k in ((1.0, 63), (2.0, 64), (2.5, 64), (3.5, 63)):
                if t + tt_ * beat < t1 - 0.04: n(t + tt_ * beat, DR, k, 54, 0.1)
            if t + 1.5 * beat < t1 - 0.04 and b % 2 == 0: n(t + 1.5 * beat, DR, 75, 58, 0.08)
            if b % 2 == 1 and t + 2 * beat < t1 - 0.04:
                for i, k in enumerate((tones[3], tones[2], tones[1])): n(t + (2 + i * 0.5) * beat, VIB, k + 12, 62, beat * 0.5)
        t += bar; b += 1


def till(t, notes=(72, 76, 79, 83, 84), step=0.11, v=86):
    for i, k in enumerate(notes): n(t + i * step, MAR, k, v, 0.4)


def ding_(t, k=84, v=80): n(t, VIB, k, v, 1.0); n(t, MAR, k + 12, 60, 0.3)


def stab(t, chord="C", v=88, d=0.6):
    root, tones = CH[chord]
    for k in tones: n(t, PNO, k + 12, v, d)
    n(t, BASS, root, 96, d); n(t, DR, 49 if v > 90 else 57, 70, 0.6)


def wah(t, k=(65, 64, 63), v=80):
    for i, kk in enumerate(k): n(t + i * 0.22, TPT, kk, v, 0.22 if i < len(k) - 1 else 0.6)


def flute(t, notes=(72, 74, 76, 79), step=0.16, v=78):
    for i, k in enumerate(notes): n(t + i * step, FLU, k, v, step * (3 if i == len(notes) - 1 else 0.95))


# ---- cues ----
ding_(0.0, 72); ding_(0.35, 76); ding_(0.7, 79)          # tags 4 + 5 land with a till ding (frame 0 move)
band(0.9, L0("i2") - 0.05, "main", 1)
till(TT("i1", "five", 0.6) - 0.05)
band(S["S_i2"], S["S_i4"] - 0.04, "main", 2)
stab(TT("i3", "four", 0.3) - 0.03, "Am", 86, 0.5)
band(S["S_i4"], S["S_a1"] - 0.04, "main", 1); stab(TT("i4", "Who", 0.3) - 0.03, "Dm", 88); stab(TT("i4", "still", 0.3) - 0.03, "E7", 88)
band(S["S_a1"], S["S_b1"] - 0.04, "test", 3)
ding_(TT("a3", "different", 0.3), 79); wah(TT("a4", "twenty-three", 0.3) + 0.2, (67, 66, 65)); ding_(TT("a5", "seven", 0.3), 84)
band(S["S_b1"], S["S_c2"] - 0.04, "side", 2)
for i, k in enumerate((79, 74, 79)): n(TT("b1", "coin", 0.3) + i * 0.12, MAR, k, 70, 0.2)
band(S["S_c2"], S["S_c4"] - 0.04, "money", 3); stab(TT("c3", "twelve", 0.3) - 0.03, "C", 92, 0.8); till(TT("c3", "twelve", 0.3) + 0.1, (84, 88, 91), 0.09)
band(S["S_c4"], S["S_d1"] - 0.04, "main", 1, guiro=False)
band(S["S_d1"], S["S_e1"] - 0.04, "end", 2); stab(TT("d1", "ended", 0.3) - 0.1, "C", 94, 0.8); flute(TT("d1", "ended", 0.3) + 0.2)
stab(TT("d2", "Period.", 0.3) - 0.03, "C", 90, 0.6)
band(S["S_e1"], S["S_t1"] - 0.04, "big", 2); wah(TT("e2", "mouse", 0.3) + 0.3, (62, 61, 60), 74)
band(S["S_t1"], S["S_end"] - 0.05, "main", 3); ding_(TT("t1", "Compare", 0.3), 79); ding_(TT("t2", "phones.", 0.3), 84)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["C"][1]: n(END - 1.3, PNO, k + 12, 88, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
till(END - 1.25, (72, 76, 79, 84), 0.08); n(END - 1.3, BASS, 36, 96, 1.0)


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
