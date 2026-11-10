"""'Red-envelope whistle-pop' for HOW THEY GOT SO BIG ep 4 (Netflix 2011; new genre, GeneralUser GS): a 2011 indie-pop band —
whistled hook, nylon-guitar strum, glockenspiel answers, finger bass, hand claps + tambourine; the band drops out under the
Oops (record scratch in the mix), a minor turn for the count, a low brass slide on the share drop, and a bright major lift
when streaming wins."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
WHI, GTR, GLK, BASS, STR, BRS, PAD, DR = 0, 1, 2, 3, 4, 5, 6, 9
PROG = {WHI: 78, GTR: 24, GLK: 9, BASS: 33, STR: 48, BRS: 57, PAD: 89}
VOL = {WHI: 70, GTR: 84, GLK: 78, BASS: 92, STR: 60, BRS: 74, PAD: 34, DR: 64}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"G": (43, [55, 59, 62, 67]), "D": (38, [54, 57, 62, 66]), "Em": (40, [55, 59, 64, 67]), "C": (36, [55, 60, 64, 67]),
      "Am": (45, [57, 60, 64, 69]), "Bm": (47, [54, 59, 62, 66]), "B7": (47, [54, 59, 63, 69]), "Cm": (36, [55, 60, 63, 67])}
PROGS = {"main": ["G", "D", "Em", "C"], "move": ["C", "G", "D", "G"], "trouble": ["Em", "C", "Am", "B7"], "count": ["Em", "Bm", "C", "B7"],
         "lift": ["C", "D", "G", "Em"], "end": ["C", "D", "G", "G"]}
BPM = 112; beat = 60 / BPM
HOOK = [(0, 74, 1), (1, 71, 0.5), (1.5, 74, 0.5), (2, 76, 1), (3, 74, 1), (4, 71, 1.5), (5.5, 69, 0.5), (6, 67, 2)]


def band(t0, t1, prog="main", level=2, hook=False):
    """level 1 strum + tambourine, 2 + bass + kick/clap, 3 + glock answers"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tones = CH[PROGS[prog][b % len(PROGS[prog])]]
        for e8, (dn, v) in enumerate(((1, 70), (0, 0), (1, 52), (0, 48), (0, 0), (0, 50), (1, 60), (0, 46))):   # D - D U - U D U strum
            ts = t + e8 * beat / 2
            if v and ts < t1 - 0.04:
                for j, k in enumerate(tones if dn else tones[::-1]): n(ts + j * 0.012, GTR, k, v - j * 3, beat * 0.45)
        for q in range(8):
            if t + q * beat / 2 < t1 - 0.04: n(t + q * beat / 2, DR, 54, 40 if q % 2 else 30, 0.08)
        if level >= 2:
            for tt_, k in ((0, root), (1.5, root), (2, root + 7), (3, root + 12), (3.5, root + 7)):
                if t + tt_ * beat < t1 - 0.05: n(t + tt_ * beat, BASS, k, 84, beat * 0.45)
            for q in (0, 2):
                if t + q * beat < t1 - 0.04: n(t + q * beat, DR, 36, 66, 0.1)
            for q in (1, 3):
                if t + q * beat < t1 - 0.04: n(t + q * beat, DR, 39, 60, 0.1)
        if level >= 3 and b % 2 == 1:
            for i, k in enumerate((tones[3] + 12, tones[2] + 12, tones[3] + 12)):
                if t + (2 + i * 0.5) * beat < t1 - 0.04: n(t + (2 + i * 0.5) * beat, GLK, k, 66, beat * 0.5)
        t += bar; b += 1
    if hook:
        for tt_, k, d in HOOK:
            if t0 + tt_ * beat < t1 - 0.1: n(t0 + tt_ * beat, WHI, k, 76, d * beat * 0.95)


def glk(t, notes=(79, 83, 86), step=0.1, v=80):
    for i, k in enumerate(notes): n(t + i * step, GLK, k, v, 0.5)


def stab(t, chord="G", v=86, d=0.6):
    root, tones = CH[chord]
    for k in tones: n(t, STR, k + 12, v, d)
    n(t, BASS, root, 96, d); n(t, DR, 49 if v > 90 else 57, 66, 0.6)


def slide_down(t, k0=58, n_=5, v=82):
    for i in range(n_): n(t + i * 0.09, BRS, k0 - i * 2, v - i * 4, 0.12 if i < n_ - 1 else 0.7)


# ---- cues ----
for i, k in enumerate((67, 64, 62, 59, 55)): n(0.15 + i * 0.3, GLK, k + 12, 70, 0.4)   # frame 0: the counter runs down (falling glock)
band(0.0, L0("i2") - 0.05, "main", 1)
band(S["S_i2"], S["S_a1"] - 0.04, "main", 2, hook=True)
stab(TT("i4", "Neither", 0.3) - 0.03, "Em", 84, 0.5)
band(S["S_a1"], S["S_a4"] - 0.04, "move", 3)
glk(TT("a3", "fifteen", 0.3) - 0.05, (79, 83, 86, 91), 0.08)
band(S["S_a4"], S["S_b1"] - 0.04, "trouble", 2)
band(S["S_b1"], S["S_b4"] - 0.04, "trouble", 1)
stab(L0("b3") - 0.03, "C", 90, 0.6); glk(L0("b3") + 0.1, (84, 88, 91), 0.09)
band(S["S_b4"], S["S_b5"] - 0.06, "trouble", 2)
# the Oops: band stops dead (scratch in the mix), then a lone glock 'uh-oh'
n(TT("b5", "Oops.", 0.2) + 0.25, GLK, 76, 70, 0.4); n(TT("b5", "Oops.", 0.2) + 0.5, GLK, 72, 70, 0.8)
band(S["S_b6"], S["S_c1"] - 0.04, "move", 2)
band(S["S_c1"], S["S_c3"] - 0.04, "count", 2)
band(S["S_c3"], S["S_c4"] - 0.04, "count", 1)
slide_down(TT("c3", "thirty-five", 0.3) - 0.05)
band(S["S_c4"], S["S_d1"] - 0.04, "count", 1)
band(S["S_d1"], S["S_d3"] - 0.04, "move", 2)
band(S["S_d3"], S["S_t1"] - 0.04, "lift", 3, hook=True)
stab(TT("d3", "More", 0.3) - 0.03, "G", 94, 0.9); glk(TT("d3", "More", 0.3) + 0.1)
band(S["S_t1"], S["S_end"] - 0.05, "main", 2)
band(S["S_end"], END - 1.3, "end", 3, hook=True)
for k in CH["G"][1]: n(END - 1.3, GTR, k, 84, 1.2); n(END - 1.3, PAD, k, 40, 1.3)
glk(END - 1.25, (79, 83, 86, 91), 0.08); n(END - 1.3, BASS, 43, 96, 1.0)


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
