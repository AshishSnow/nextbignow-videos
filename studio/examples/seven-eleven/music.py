"""'Baroque corner shop' for HOW THEY GOT SO BIG ep 5 (7-Eleven; new genre: baroque harpsichord concerto, GeneralUser GS):
harpsichord running sixteenths over a walking cello bass and string chords; the Tokyo scenes add a soft koto-like pluck as a colour
(answers on the off-beats, never a melody or a pastiche), a glockenspiel on every 'win'; the band thins to cello + harpsichord for the
Dallas debt and stops dead on 'Bankruptcy.', then the rescue brings the full band back in a major key."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
HPS, KOTO, CEL, STR, GLK, BSN, PAD, DR = 0, 1, 2, 3, 4, 5, 6, 9
PROG = {HPS: 6, KOTO: 107, CEL: 42, STR: 48, GLK: 9, BSN: 70, PAD: 89}
VOL = {HPS: 84, KOTO: 58, CEL: 92, STR: 70, GLK: 76, BSN: 66, PAD: 30, DR: 60}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (45, [57, 60, 64]), "Dm": (38, [57, 62, 65]), "E": (40, [56, 59, 64]), "F": (41, [57, 60, 65]), "C": (36, [55, 60, 64]),
      "G": (43, [55, 59, 62]), "D": (38, [57, 62, 66]), "Bb": (34, [58, 62, 65]), "A": (45, [57, 61, 64])}
PROGS = {"main": ["Am", "Dm", "G", "C", "F", "Dm", "E", "Am"], "tokyo": ["C", "G", "Am", "F", "C", "F", "G", "C"],
         "debt": ["Am", "E", "Am", "Dm"], "rise": ["D", "G", "A", "D"], "end": ["F", "G", "C", "C"]}
BPM = 112; beat = 60 / BPM


def band(t0, t1, prog="main", level=2, koto=False):
    """level 1 = cello walk + harpsichord broken chords; 2 + string chords + light shaker; 3 + bassoon line + glock answers"""
    b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for q in range(2):   # two beats per chord (baroque harmonic rhythm)
            tq = t + q * beat
            if tq >= t1 - 0.04: break
            n(tq, CEL, (root, root + 7)[q], 86, beat * 0.9)
            for e in range(4):   # harpsichord sixteenths
                ts = tq + e * beat / 4
                if ts < t1 - 0.04: n(ts, HPS, tones[(e + q) % 3] + 12 + (12 if e == 3 else 0), 66 if e == 0 else 54, beat * 0.22)
            if level >= 2: n(tq + beat / 2, DR, 70, 34, 0.08)   # maracas, very light
            if level >= 3 and q == 1: n(tq, BSN, tones[0] - 12 + 2, 58, beat * 0.8)
            if koto and q == 1 and tq + beat / 2 < t1 - 0.04: n(tq + beat / 2, KOTO, tones[2] + 12, 56, beat * 0.9)
        if level >= 2 and t < t1 - 0.04:
            for k in tones: n(t, STR, k, 50, min(2 * beat * 0.95, t1 - t))
        if level >= 3 and b % 4 == 3 and t + 1.5 * beat < t1 - 0.04: n(t + 1.5 * beat, GLK, tones[2] + 24, 58, beat * 0.5)
        t += 2 * beat; b += 1


def chime(t, k=84, v=72): n(t, GLK, k, v, 0.8)


def stab(t, chord="Am", v=90, d=0.6):
    root, tones = CH[chord]
    for k in tones: n(t, STR, k + 12, v, d); n(t, HPS, k + 12, v - 10, d * 0.5)
    n(t, CEL, root - 12 if root > 40 else root, 98, d); n(t, DR, 49 if v > 90 else 57, 62, 0.6)


def run(t, notes, step=0.07, ch=HPS, v=74):
    for i, k in enumerate(notes): n(t + i * step, ch, k, v, 0.25)


TQ = lambda lid, w, f=0.3: TT(lid, w, f)
# ---- cues ----
band(0.0, S["S_i2"] - 0.05, "main", 1)
for i in range(int((S["S_i2"] - 0.1) / (2 * beat)) + 1): n(i * 2 * beat + beat, GLK, (84, 88)[i % 2], 46, 0.4)   # frame-0 pulse on the counter
stab(TQ("i1", "owned") - 0.03, "Am", 86, 0.5); run(TQ("i1", "Tokyo?", 0.4), (76, 79, 84, 88), 0.06, GLK, 70)
band(S["S_i2"], S["S_i3"] - 0.04, "debt", 1)
band(S["S_i3"], S["S_i5"] - 0.04, "tokyo", 2, koto=True); stab(TQ("i3", "seventy-three.") - 0.03, "C", 84, 0.5)
for i in range(3): chime(TQ("i4", "Three") + i * 0.3, (79, 83, 86)[i], 66)
band(S["S_i5"], S["S_a1"] - 0.04, "main", 2)
run(TQ("i7", "eleven") - 0.1, (72, 76, 79, 84), 0.07)
band(S["S_a1"], S["S_a5"] - 0.04, "main", 2)
stab(TQ("a3", "opposed") - 0.03, "E", 86, 0.5)
band(S["S_a5"], S["S_b1"] - 0.04, "tokyo", 3, koto=True); chime(TQ("a5", "sunglasses.", 0.2), 91, 80)
band(S["S_b1"], S["S_c1"] - 0.04, "tokyo", 3, koto=True)
stab(TQ("b2", "one.", 0.2) - 0.03, "F", 82, 0.5)
for w_ in ("Rice", "truck", "computer"): chime(TQ("b4", w_) - 0.05, 88, 70)
stab(TQ("b5", "more") - 0.03, "C", 90, 0.7); run(TQ("b5", "more") + 0.1, (84, 88, 91, 96), 0.06, GLK, 72)
band(S["S_c1"], S["S_c3"] - 0.04, "debt", 2)
band(S["S_c3"], S["S_c4"] - 0.04, "debt", 1)
band(S["S_c4"], TQ("c4", "Bankruptcy.", 0.2) - 0.1, "debt", 1)
stab(TQ("c4", "Bankruptcy.", 0.2) - 0.03, "Am", 94, 0.9)
band(TQ("c4", "rescue") - 0.2, S["S_d1"] - 0.04, "rise", 2)
band(S["S_d1"], S["S_d3"] - 0.04, "rise", 3, koto=True)
stab(TQ("d1", "seventy") - 0.03, "D", 90, 0.6); stab(TQ("d2", "rest.", 0.2) - 0.03, "D", 94, 0.7); run(TQ("d2", "rest.", 0.2) + 0.1, (86, 90, 93, 98), 0.06, GLK, 72)
band(S["S_d3"], S["S_t1"] - 0.04, "tokyo", 3, koto=True)
band(S["S_t1"], S["S_end"] - 0.05, "main", 2)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["C"][1]: n(END - 1.3, STR, k + 12, 86, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
run(END - 1.3, (72, 76, 79, 84, 88), 0.06); n(END - 1.3, CEL, 36, 96, 1.0)


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
rng = np.random.default_rng(6); irl = int(1.1 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.35)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 4500, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.2 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = signal.sosfilt(signal.butter(2, [45, 14000], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
