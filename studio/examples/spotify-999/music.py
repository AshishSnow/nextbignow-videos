"""Bedroom-pop score for HOW IT WORKS ep 1 (new genre, GeneralUser GS): Rhodes + muted guitar arpeggio + soft drum machine + warm bass; one bright glockenspiel motif (the 'play' note) that climbs through each gate and DROPS OUT when the barrier falls at 999."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
EP, GTR, BASS, GLO, PAD, VIB, DR = 0, 1, 2, 3, 4, 5, 9
PROG = {EP: 4, GTR: 28, BASS: 33, GLO: 9, PAD: 89, VIB: 11}
VOL = {EP: 78, GTR: 74, BASS: 100, GLO: 84, PAD: 56, VIB: 74, DR: 86}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"F": (41, [60, 65, 69, 72, 76]), "Am": (45, [60, 64, 67, 69, 72]), "Dm": (38, [60, 62, 65, 69, 72]), "Bb": (46, [58, 62, 65, 69, 72]), "Gm": (43, [58, 62, 65, 67, 70]), "A": (45, [61, 64, 67, 69, 73]), "C": (48, [60, 64, 67, 70, 72])}
PROGS = {"main": ["F", "Am", "Dm", "Bb"], "lift": ["Bb", "C", "Am", "Dm"], "dark": ["Dm", "Bb", "Gm", "A"], "end": ["Bb", "C", "F", "F"]}
BPM = 84; beat = 60 / BPM; SW = 0.16   # lazy swung sixteenths


def pop_bar(t0, t1, prog="main", level=2, motif=0):
    """level 1 Rhodes + pad, 2 + guitar + bass + soft kick/rim, 3 + hats + glock motif"""
    bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, tones = CH[ch]
        for q, vv in ((0, 62), (1.5, 50), (2.5, 54)):
            if t + q * beat < t1 - 0.05:
                for k in tones[:4]: n(t + q * beat + 0.012, EP, k, vv, beat * 0.9)
        n(t, PAD, tones[0], 44, bar * 0.98); n(t, PAD, tones[2], 40, bar * 0.98)
        if level >= 2:
            for s_ in range(16):
                ts = t + s_ * beat / 4 + (SW * beat / 4 if s_ % 2 else 0)
                if ts < t1 - 0.04 and s_ % 2 == 0:
                    n(ts, GTR, tones[[0, 2, 3, 2, 4, 2, 3, 1][s_ // 2 % 8]] + 12, 52 + (8 if s_ % 4 == 0 else 0), beat * 0.22)
            for q, off in ((0, 0), (1.5, 0), (2.5, 7), (3.5, 12)):
                if t + q * beat < t1 - 0.05: n(t + q * beat, BASS, root - 12 + off - (12 if root > 44 else 0), 92, beat * 0.55)
            for q in (0, 2.5):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 36, 72, 0.1)
            for q in (1, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 37, 56, 0.06)
        if level >= 3:
            for s_ in range(8):
                ts = t + s_ * beat / 2 + (SW * beat / 2 if s_ % 2 else 0)
                if ts < t1 - 0.03: n(ts, DR, 42, 40 + (8 if s_ % 2 == 0 else 0), 0.04)
            if motif:
                for q, k in ((0, 84), (0.75, 86), (1.5, 88 if motif < 2 else 89), (3, 84)):
                    if b % 2 == 0 and t + q * beat < t1 - 0.05: n(t + q * beat, GLO, k, 70, beat * 0.7)
        t += bar; b += 1


def play_note(t, k=84, v=90):
    n(t, GLO, k, v, 0.9); n(t, VIB, k - 12, v - 24, 1.0)


def hit(t, v=100):
    n(t, DR, 49, v - 32, 1.6); n(t, DR, 36, v - 10, 0.25); n(t, BASS, 29, 96, 1.0)


def stab(t, chord="Dm", v=86, d=0.5):
    root, tones = CH[chord]
    for k in tones[:4]: n(t, EP, k + 12, v, d); n(t, VIB, k + 12, v - 20, d + 0.2)
    n(t, BASS, root - 24 if root > 44 else root - 12, 96, d)


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.08, GLO, k, 74, 0.5)


# ---- cues ----
stab(0.0, "Dm", 84); play_note(0.02, 84)
pop_bar(0.3, S["S_singer"] - 0.03, "dark", 1)
stab(T("i1", "Why") - 0.05, "A", 86); 
pop_bar(S["S_singer"] + 0.1, S["S_four"] - 0.04, "main", 3, 1)
stab(T("i3", "It") - 0.05, "Gm", 80)
pop_bar(S["S_four"], S["S_pot"] - 0.06, "main", 2)
for i in range(4): play_note(S["S_four"] + 0.2 + i * 0.3, 84 + (0, 2, 4, 5)[i], 84)
stab(T("i4", "three") - 0.05, "A", 92, 0.8)
# gate 1: the pot fills: climb
play_note(S["S_pot"] + 0.05, 84); pop_bar(S["S_pot"] + 0.2, S["S_many"] - 0.04, "main", 3, 1)
sparkle(S["S_many"] + 0.05, 84); pop_bar(S["S_many"] + 0.1, S["S_slice"] - 0.05, "lift", 3, 2); stab(T("a3", "eleven") - 0.08, "Bb", 92)
# gate 2
play_note(S["S_slice"] + 0.05, 86); pop_bar(S["S_slice"] + 0.2, S["S_100"] - 0.05, "main", 2)
pop_bar(S["S_100"], S["S_200"] - 0.05, "lift", 3, 1); stab(T("b4", "So") - 0.05, "C", 88); sparkle(T("b4", "five") - 0.05, 88)
pop_bar(S["S_200"], L0("b6") - 0.05, "lift", 2); stab(L0("b6") - 0.03, "Dm", 94, 0.9); pop_bar(L0("b6") + 0.4, S["S_line"] - 0.05, "dark", 1)
# gate 3: tension, then the motif is cut dead on the slam
play_note(S["S_line"] + 0.05, 88); pop_bar(S["S_line"] + 0.2, T("c2", "thousand") - 0.05, "dark", 2)
pop_bar(T("c2", "thousand"), S["S_out"] - 0.03, "main", 3, 1); sparkle(T("c2", "thousand"), 88)
hit(S["S_out"] + 0.02, 112); stab(S["S_out"] + 0.02, "Dm", 100, 1.3)
pop_bar(S["S_out"] + 1.5, S["S_penny"] - 0.05, "dark", 1)
# pennies: empty room, one lone note
for i in range(3): play_note(S["S_penny"] + 0.8 + i * 2.2, 84, 60)
for k in (62, 69): n(S["S_penny"], PAD, k, 44, S["S_share"] - S["S_penny"])
pop_bar(S["S_share"], S["S_booth"] - 0.05, "dark", 2)
# gate 4
play_note(S["S_booth"] + 0.05, 89); pop_bar(S["S_booth"] + 0.2, S["S_deal"] - 0.04, "lift", 2)
pop_bar(S["S_deal"], S["S_sofa"] - 0.06, "dark", 2); stab(T("d3", "Spotify") - 0.05, "Gm", 78)
# sofa: back to the cosy room, main loop, lighter
pop_bar(S["S_sofa"] + 0.05, S["S_study"] - 0.05, "main", 2)
pop_bar(S["S_study"], S["S_swing"] - 0.05, "dark", 1)
pop_bar(S["S_swing"], S["S_take"] - 0.05, "lift", 3, 2); stab(S["S_swing"] + 0.5, "C", 84); stab(S["S_swing"] + 0.9, "Dm", 84)
pop_bar(S["S_take"], S["S_end"] - 0.05, "main", 3, 1); stab(T("t1", "Making") - 0.05, "Bb", 86)
pop_bar(S["S_end"], END - 1.3, "end", 3, 2); sparkle(T("z2", "Save") - 0.05, 84)
for k in CH["F"][1][:4]: n(END - 1.3, EP, k + 12, 84, 0.9); n(END - 1.3, PAD, k, 56, 1.3)
n(END - 1.3, BASS, 29, 96, 1.2); play_note(END - 1.25, 84, 92)


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
rng = np.random.default_rng(4); irl = int(1.8 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.4)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 5200, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.2 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
# bedroom-pop: a touch of tape softness on top
mus = signal.sosfilt(signal.butter(1, 9000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
