"""'After-school uke' for HOW TO START ep 9 (childminding; new genre: playground ukulele pop, GeneralUser GS): a strummed high nylon
'ukulele' (GM 24 an octave up, 4-stroke down-down-up-down strum) over a bouncy plucked upright bass, marimba off-beat answers, a
glockenspiel on every tick and step, soft hand claps on 2 and 4 from step 1; the band drops to bass + uke for the rules that bite
(checks, the offence) and stops dead on 'criminal offence', then the bright end returns in F major. Frame 0 has a clock-tick pulse."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("RENDER = {")[0])
S = {k: st for k, st, _ in SHOTLIST}
UKE, BAS, MAR, GLK, WHS, PAD, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {UKE: 24, BAS: 32, MAR: 12, GLK: 9, WHS: 78, PAD: 89}
VOL = {UKE: 88, BAS: 92, MAR: 70, GLK: 74, WHS: 52, PAD: 30, DR: 62}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67, 72]), "F": (41, [60, 65, 69, 72]), "G": (43, [62, 67, 71, 74]), "Am": (45, [60, 64, 69, 72]),
      "Dm": (38, [62, 65, 69, 74]), "E": (40, [59, 64, 68, 71]), "Bb": (34, [62, 65, 70, 74])}
PROGS = {"main": ["C", "G", "Am", "F"], "step": ["F", "C", "G", "C"], "tense": ["Am", "Dm", "E", "Am"], "end": ["F", "C", "G", "F"]}
BPM = 120; beat = 60 / BPM


def band(t0, t1, prog="main", level=2):
    """level 1 = bass + uke strum; 2 + marimba answers + shaker; 3 + claps on 2/4 + glock sparkle"""
    b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.04: break
            n(tq, BAS, root + (0, 7, 12, 7)[q], 88 if q == 0 else 74, beat * 0.55)
            for j, off in enumerate((0, 0.5) if q in (1, 3) else (0,)):   # strum: down / down-up
                ts = tq + off * beat
                if ts >= t1 - 0.04: continue
                for i, k in enumerate(tones): n(ts + i * 0.012, UKE, k + 12, (68 if q == 0 else 56) - 6 * j, beat * 0.4)
            if level >= 2:
                n(tq + beat / 2, DR, 70, 30, 0.08)
                if q == 2 and tq + beat / 2 < t1 - 0.04: n(tq + beat / 2, MAR, tones[(b + q) % 4] + 12, 60, 0.3)
            if level >= 3 and q in (1, 3): n(tq, DR, 39, 52, 0.1)
            if level >= 3 and q == 0: n(tq, DR, 36, 44, 0.1)
        if level >= 3 and b % 2 == 1 and t + 3.5 * beat < t1 - 0.04: n(t + 3.5 * beat, GLK, tones[3] + 12, 52, 0.4)
        t += 4 * beat; b += 1


def chime(t, k=84, v=72): n(t, GLK, k, v, 0.8)


def stab(t, chord="C", v=90, d=0.6):
    root, tones = CH[chord]
    for k in tones: n(t, UKE, k + 12, v, d); n(t, MAR, k, v - 16, d)
    n(t, BAS, root, 100, d); n(t, DR, 49 if v > 90 else 57, 60, 0.6)


def run(t, notes, step=0.07, ch=GLK, v=72):
    for i, k in enumerate(notes): n(t + i * step, ch, k, v, 0.25)


TQ = lambda lid, w, f=0.3: TT(lid, w, f)
# ---- cues ----
for i in range(int(S["S_i3"] / 0.5)): n(i * 0.5, DR, 76 if i % 2 else 77, 38, 0.05)   # frame 0: the clock ticks (wood blocks)
band(0.6, S["S_i3"] - 0.05, "main", 1)
stab(TQ("i1", "two-hour", 0.6) - 0.03, "Am", 86, 0.5)
chime(TQ("i2", "register", 0.4), 84); chime(TQ("i2", "checks.", 0.3), 88)
band(S["S_i3"], S["S_a1"] - 0.04, "main", 2)
for i in range(4): chime(TQ("i4", "Four") + i * 0.22, (72, 76, 79, 84)[i], 64)
band(S["S_a1"], S["S_b1"] - 0.04, "step", 3)
for w_ in (("a3", "eight."), ("a3", "two"), ("a3", "paid.")): chime(TQ(*w_, 0.5) + 0.05, 88, 70)
chime(TQ("a4", "counts.", 0.4), 91, 74)
n(TQ("a5", "Evening", 0.3), WHS, 79, 50, 0.8)
band(S["S_b1"], S["S_c1"] - 0.04, "main", 2)
run(TQ("b2", "thirty-five", 0.3) - 0.1, (72, 76, 79, 84), 0.06)
band(S["S_c1"], S["S_c4"] - 0.04, "tense", 1)
stab(TQ("c3", "teenager", 0.3) - 0.03, "E", 82, 0.4)
band(S["S_c4"], S["S_d1"] - 0.04, "step", 2); chime(TQ("c4", "forty-one", 0.3), 91, 76)
band(S["S_d1"], S["S_e1"] - 0.04, "main", 3)
for i in range(6): chime(TQ("d2", "Six", 0.3) - 0.3 + i * 0.12, (72, 74, 76, 79, 81, 84)[i], 58)
band(S["S_e1"], TQ("e2", "criminal", 0.3) - 0.25, "tense", 1)
stab(TQ("e2", "criminal", 0.3) - 0.2, "Am", 96, 0.9)
band(TQ("e2", "fine.", 0.3) + 0.6, S["S_f2"] - 0.04, "tense", 1)
stab(TQ("e3", "closed", 0.3) - 0.03, "Dm", 84, 0.5)
band(S["S_f2"], S["S_t1"] - 0.04, "main", 2)
band(S["S_t1"], S["S_end"] - 0.05, "step", 2)
band(S["S_end"], END - 1.3, "end", 3)
for k in CH["F"][1]: n(END - 1.3, UKE, k + 12, 86, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
run(END - 1.3, (72, 77, 81, 84, 89), 0.06); n(END - 1.3, BAS, 41, 96, 1.0)


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
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.28)[:, None]; ir[: int(0.010 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 5000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = signal.sosfilt(signal.butter(2, [45, 14000], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
