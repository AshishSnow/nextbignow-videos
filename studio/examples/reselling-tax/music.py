"""Lo-fi hip-hop score for HOW TO START ep 5 (new genre, GeneralUser GS): dusty Rhodes 7ths, upright bass, soft swung boom-bap, kalimba motif that gains one note per step; the room goes minor for the tax step; everything stops for 'a form doesn't mean you owe'. Tape wow + vinyl crackle on the master."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
EP, GTR, BASS, KAL, PAD, VIB, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {EP: 4, GTR: 26, BASS: 32, KAL: 108, PAD: 89, VIB: 11}
VOL = {EP: 80, GTR: 62, BASS: 104, KAL: 88, PAD: 50, VIB: 72, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Fm9": (41, [60, 63, 65, 68, 72]), "Bbm9": (46, [60, 61, 65, 68, 72]), "Eb9": (39, [61, 65, 67, 70, 72]), "Abmaj7": (44, [60, 63, 67, 68, 72]), "Dbmaj7": (49, [60, 61, 65, 68, 72]),
      "C7": (48, [58, 60, 64, 67, 70]), "Gm7b5": (43, [58, 61, 65, 67, 70]), "Ab6": (44, [60, 63, 65, 68, 72])}
PROGS = {"main": ["Abmaj7", "Fm9", "Dbmaj7", "Eb9"], "lift": ["Dbmaj7", "Eb9", "Abmaj7", "Ab6"], "dark": ["Fm9", "Gm7b5", "Bbm9", "C7"], "end": ["Dbmaj7", "Eb9", "Abmaj7", "Abmaj7"]}
BPM = 76; beat = 60 / BPM; SW = 0.24   # lazy swung sixteenths, behind the beat


def lofi(t0, t1, prog="main", level=2):
    """level 1 Rhodes + pad, 2 + upright + kick/rim, 3 + hats + muted-guitar answers"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, tones = CH[ch]
        for q, vv in ((0, 66), (1.75, 50), (2.5, 56)):
            if t + q * beat < t1 - 0.05:
                for j, k in enumerate(tones[:5]): n(t + q * beat + 0.018 + j * 0.006, EP, k, vv - j * 2, beat * (1.3 if q == 0 else 0.7))
        n(t, PAD, tones[0], 40, bar * 0.98); n(t, PAD, tones[3], 36, bar * 0.98)
        if level >= 2:
            for q, off in ((0, 0), (1.75, 0), (2.5, 7), (3.5, 10 if prog == "dark" else 12)):
                if t + q * beat < t1 - 0.05: n(t + q * beat + 0.02, BASS, root - 12 + off - (12 if root > 44 else 0), 98, beat * 0.7)
            for q in (0, 1.75, 2.5):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 36, 88 if q == 0 else 70, 0.12)
            for q in (1, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat + 0.025, DR, 38, 62, 0.08); n(t + q * beat + 0.012, DR, 37, 54, 0.05)
        if level >= 3:
            for s_ in range(8):
                ts = t + s_ * beat / 2 + (SW * beat / 2 if s_ % 2 else 0)
                if ts < t1 - 0.03: n(ts, DR, 42, 38 + (10 if s_ % 2 == 0 else 0), 0.04)
            if b % 2 == 1:
                for q, k in ((2.75, tones[2] + 12), (3.25, tones[3] + 12), (3.5, tones[4] + 12)):
                    if t + q * beat < t1 - 0.05: n(t + q * beat, GTR, k, 58, beat * 0.25)
        t += bar; b += 1


KALM = [80, 82, 84, 87]     # the step motif: step n plays n notes


def motif(t, steps, v=86):
    for i in range(steps): n(t + i * 0.16, KAL, KALM[i], v, 0.5); n(t + i * 0.16, VIB, KALM[i] - 12, v - 34, 0.6)


def hit(t, v=100):
    n(t, DR, 49, v - 40, 1.4); n(t, DR, 36, v - 10, 0.25); n(t, BASS, 29, 96, 1.0)


def stab(t, chord="Fm9", v=80, d=0.6):
    root, tones = CH[chord]
    for k in tones[:4]: n(t, EP, k + 12, v, d); n(t, VIB, k + 12, v - 26, d + 0.2)
    n(t, BASS, root - 24 if root > 44 else root - 12, 96, d)


# ---- cues ----
stab(0.0, "Fm9", 76); motif(0.02, 2, 74)
lofi(0.25, S["S_closet"] - 0.03, "dark", 1)
stab(TT("i1", "Why?", 0.95) - 0.05, "C7", 82)
lofi(S["S_closet"], S["S_old"] - 0.03, "main", 2)
lofi(S["S_old"], S["S_thrift"] - 0.05, "main", 2); stab(TT("i3", "lost", 0.75) - 0.04, "Fm9", 72); stab(TT("i3", "no", 0.92) - 0.02, "Abmaj7", 80)
lofi(S["S_thrift"], S["S_income"] - 0.03, "lift", 3); stab(TT("i4", "thirty.", 0.88) - 0.04, "Eb9", 84)
lofi(S["S_income"], S["S_steps"] - 0.04, "lift", 2); stab(TT("i5", "income.", 0.32) - 0.03, "Dbmaj7", 88)
lofi(S["S_steps"], S["S_s1"] - 0.06, "main", 3); motif(TT("i5", "four", 0.75) - 0.1, 4, 88); stab(TT("i5", "Step", 0.82) - 0.03, "C7", 84, 0.9)
motif(S["S_s1"] + 0.02, 1); lofi(S["S_s1"] + 0.2, S["S_s2"] - 0.06, "main", 3)
motif(S["S_s2"] + 0.02, 2); lofi(S["S_s2"] + 0.2, S["S_rcpt"] - 0.04, "lift", 3)
lofi(S["S_rcpt"], S["S_s3"] - 0.06, "main", 3); stab(TT("b4", "twenty,", 0.42) - 0.03, "Abmaj7", 84)
stab(TT("b4", "postage", 0.68) - 0.03, "Fm9", 76)
motif(S["S_s3"] + 0.02, 3); lofi(S["S_s3"] + 0.2, S["S_s4"] - 0.06, "lift", 3)
stab(TT("c2", "profit,", 0.66) - 0.05, "Ab6", 82)
# step 4: the room goes minor + half the kit drops out
hit(S["S_s4"] + 0.02, 100); motif(S["S_s4"] + 0.04, 4, 74); lofi(S["S_s4"] + 0.3, S["S_irs"] - 0.03, "dark", 2)
lofi(S["S_irs"], S["S_uk"] - 0.06, "dark", 2); stab(TT("d3", "all", 0.55) - 0.03, "C7", 88, 0.9)
lofi(S["S_uk"], S["S_old30"] - 0.03, "dark", 3)
lofi(S["S_old30"], S["S_buy"] - 0.06, "main", 2); stab(TT("d6", "nothing.", 0.95) - 0.2, "Abmaj7", 84, 0.9)
lofi(S["S_buy"], S["S_both"] - 0.1, "dark", 3); stab(TT("d7", "thousand", 0.68), "Gm7b5", 84)
# the line of the episode: band out, one held chord under each half
for k in CH["Fm9"][1][:4]: n(S["S_both"], EP, k, 56, L0("t1") - S["S_both"] + 2.2); n(S["S_both"], PAD, k, 38, 2.6)
tt_ = TT("t1", "No", 0.5) - 0.05
for k in CH["C7"][1][:4]: n(tt_, EP, k, 60, 2.2); n(tt_, PAD, k, 40, 2.4)
lofi(S["S_keep2"], S["S_end"] - 0.06, "main", 2)
lofi(S["S_end"], END - 1.3, "end", 3); motif(TT("z2", "Save", 0.1) - 0.05, 4, 78)
for k in CH["Abmaj7"][1][:4]: n(END - 1.3, EP, k + 12, 76, 0.9); n(END - 1.3, PAD, k, 50, 1.3)
n(END - 1.3, BASS, 32, 96, 1.2); motif(END - 1.25, 4, 84)


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
rng = np.random.default_rng(6); irl = int(1.2 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.28)[:, None]; ir[: int(0.01 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 4200, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
# lo-fi master: tape wow, dusty band limit, soft saturation, vinyl crackle + hiss
N_ = len(mus); idx = np.arange(N_) + 0.0016 * SR * np.sin(2 * np.pi * 0.37 * np.arange(N_) / SR) + 0.0005 * SR * np.sin(2 * np.pi * 2.1 * np.arange(N_) / SR)
mus = np.stack([np.interp(idx, np.arange(N_), mus[:, c]) for c in (0, 1)], 1)
mus = signal.sosfilt(signal.butter(2, [70, 6800], "band", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.6) / np.tanh(1.6)
hiss = signal.sosfilt(signal.butter(2, [800, 6000], "band", fs=SR, output="sos"), rng.standard_normal((N_, 2)), axis=0)
cr = np.zeros((N_, 2))
for i_ in rng.integers(0, N_ - 300, int(N_ / SR * 7)):
    ln = int(rng.integers(30, 180)); cr[i_:i_ + ln] += rng.standard_normal((ln, 2)) * np.exp(-np.arange(ln) / (ln / 5))[:, None] * rng.uniform(0.2, 1.0)
cr = signal.sosfilt(signal.butter(2, 1400, "high", fs=SR, output="sos"), cr, axis=0)
mus = mus + 0.0035 * hiss / (np.std(hiss) + 1e-9) + 0.05 * cr
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus / (np.abs(mus).max() + 1e-9) * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
