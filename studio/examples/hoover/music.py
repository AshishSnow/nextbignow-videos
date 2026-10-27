"""Ska / two-tone score for "Hoover's free flights" (GeneralUser GS) — new genre: 1990s British holiday ska.
Offbeat clean-guitar skank + organ bubble, walking bass, ska drums (cross-stick backbeat, open hats), trombone/trumpet section
answers; a dark minor half-time for mistake 3 (the travel agents) and the bill; airport PA chime; timpani/brass hits on reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
GTR, ORG, BASS, TBN, TPT, GLK, PAD, STR, TIMP, SUB, VIB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 9
PROG = {GTR: 27, ORG: 17, BASS: 33, TBN: 57, TPT: 56, GLK: 9, PAD: 89, STR: 48, TIMP: 47, SUB: 38, VIB: 11}
VOL = {GTR: 76, ORG: 62, BASS: 104, TBN: 84, TPT: 80, GLK: 84, PAD: 62, STR: 70, TIMP: 108, SUB: 98, VIB: 80, DR: 88}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67]), "Am": (33, [60, 64, 69]), "F": (41, [60, 65, 69]), "G": (31, [59, 62, 67]), "Dm": (38, [62, 65, 69]),
      "E7": (40, [59, 62, 68]), "Bb": (34, [58, 62, 65]), "Em": (40, [59, 64, 67])}
PROGS = {"main": ["C", "Am", "F", "G"], "busy": ["F", "G", "Em", "Am"], "dark": ["Am", "Dm", "E7", "Am"], "bill": ["Dm", "Bb", "E7", "Am"],
         "win": ["F", "G", "C", "C"]}
BPM = 150


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    """ska: bass on the beat (walking), guitar skank + organ bubble on the off-beats, cross-stick on 2 & 4, hats; brass riffs at level 3.
    level 0-1 = 'dark' half-time feel (bass + sparse skank + rim)"""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        walk = [0, 4, 7, 9] if level >= 2 else [0, 0, 7, 0]
        for i in range(4):
            tq = t + i * beat
            if tq >= t1 - 0.03: break
            n(tq, BASS, root - 12 + walk[i] - (12 if level < 2 and i else 0) + (12 if level < 2 and i == 0 else 0), 100 if i == 0 else 86, beat * 0.8)
            if level >= 1 or i % 2 == 1:
                for k in tri: n(tq + beat / 2, GTR, k, 74 + 6 * min(level, 3), beat * 0.22)
            if level >= 2:
                for k in tri: n(tq + beat / 2, ORG, k - 12, 58, beat * 0.3)
            if i in (1, 3): n(tq, DR, 37 if level < 3 else 38, 96, 0.1)
            if i in (0, 2) and level >= 1: n(tq, DR, 36, 104 if i == 0 else 88, 0.15)
            if level >= 2: n(tq + beat / 2, DR, 46 if level >= 3 else 42, 74, 0.12)
        if level >= 3 and b % 2 == 1:
            for j, iv in enumerate((7, 9, 12, 9)):
                n(t + (2 + j * 0.5) * beat, TBN, root + 12 + iv - 12, 92, beat * 0.4); n(t + (2 + j * 0.5) * beat, TPT, root + 24 + iv, 84, beat * 0.4)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TIMP, 40, v, 1.4); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="C", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, TBN, k, v, d); n(t, TPT, k + 12, v - 10, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.07)
    for j in range(m): n(t_end - dur + j * 0.07, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((60, 63, 67, 70, 72)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


def chime(t):   # airport PA ding-dong
    n(t, VIB, 76, 96, 0.9); n(t + 0.45, VIB, 72, 92, 1.2)


def pad(t0, t1, chord, v=56):
    for k in CH[chord][1]: n(t0, PAD, k - 12, v, max(0.1, t1 - t0))


# ---- cues ----
pad(0.0, S["S0b"], "C", 60); sparkle(0.05, 84)
groove(0.6, S["S1a"] - 0.05, "main", 2)
stab(S["S0b"] + 0.02, "F", 104); hit(T("i1", "yes?") - 0.1, 100)
groove(S["S1a"], S["S2"] - 0.05, "busy", 1)
hit(T("i2", "fired,") - 0.1, 112); stab(T("i2", "fired,") - 0.1, "Am", 108)
hit(T("i2", "sold.") - 0.1, 116, True); stab(T("i2", "sold.") - 0.1, "E7", 110, 0.5)
pad(S["S2"], S["S3"], "Am", 58)
riser(T("i3", "cruelest.") - 0.15, 1.0); hit(T("i3", "cruelest.") - 0.15, 118, True); stab(T("i3", "cruelest.") - 0.15, "E7", 112, 0.5)
stab(S["S3"] + 0.02, "C", 110)
groove(S["S3"] + 0.25, S["S9"] - 0.05, "main", 3)
chime(S["S4"] + 0.1)
sparkle(T("a3", "free") - 0.05, 86); sparkle(T("a3", "Europe.") - 0.1, 91)
chime(T("a4", "America.") - 0.4)
hit(T("a5", "nineteen") - 0.2, 106); stab(T("a5", "nineteen") - 0.2, "G", 104)
hit(T("a6", "several") + 0.3, 108)
sparkle(T("a7", "holidays.") - 0.3, 88)
stab(S["S9"] + 0.02, "F", 110)
groove(S["S9"] + 0.25, S["S12"] - 0.05, "busy", 3)
hit(T("b4", "eighty") - 0.2, 110); sparkle(T("b4", "eighty"), 84)
groove(S["S12"], T("b5", "what") - 0.2, "busy", 1)
riser(S["S13"], 1.2)
hit(S["S13"], 120, True); stab(S["S13"], "E7", 112, 0.6)
groove(S["S13"] + 0.3, S["S18"] - 0.05, "dark", 1)
chime(S["S14"] + 0.15)
for tt_ in (T("c3", "Airports"), T("c3", "Dates"), T("c3", "Expensive")): stab(tt_ - 0.12, "Dm", 100, 0.2)
hit(T("c4", "Thousands") - 0.12, 110)
hit(T("c5", "court") - 0.2, 104)
pad(S["S18"], S["S19"], "Dm", 60); hit(T("d1", "bill?") - 0.1, 108)
groove(S["S19"], S["S25"] - 0.05, "bill", 2)
hit(T("d2", "fired") - 0.15, 110); stab(T("d2", "fired") - 0.15, "Bb", 106)
hit(T("d3", "thirty") - 0.15, 112, True); sparkle(T("d3", "thirty"), 86)
chime(S["S21"] + 0.1); sparkle(T("d4", "twenty") - 0.2, 88)
hit(T("d5", "forty") - 0.2, 112); stab(T("d5", "forty") - 0.2, "E7", 108)
hit(T("d6", "sold") - 0.1, 116, True); stab(T("d6", "sold") - 0.1, "Am", 110, 0.5)
riser(T("d7", "thirty") - 0.5, 0.9); hit(T("d7", "thirty") - 0.5, 122, True); stab(T("d7", "thirty") - 0.5, "E7", 114, 0.7)
hit(S["S25"], 112); stab(S["S25"] + 0.02, "C", 110)
groove(S["S25"] + 0.3, END - 1.6, "win", 3)
hit(T("t1", "Far") - 0.15, 116, True)
for k in CH["C"][1]: n(END - 1.6, GTR, k, 90, 1.6); n(END - 1.6, PAD, k - 12, 74, 2.0); n(END - 1.6, TBN, k, 100, 0.8); n(END - 1.6, TPT, k + 12, 96, 0.8)
n(END - 1.6, BASS, 36, 104, 1.6); hit(END - 1.6, 104); sparkle(END - 1.5, 84)

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


mus = np.zeros((int((END + 3) * SR), 2), np.float32)
cuts = sorted(set([0.0] + [S[k] for k in ("S1a", "S2", "S3", "S9", "S12", "S13", "S18", "S19", "S25")] + [END + 3]))
evs = sorted(ev)
for a, b in zip(cuts[:-1], cuts[1:]):
    part = render([e for e in evs if a - 0.01 <= e[0] < b - 0.01], END)
    nb = int(b * SR); tail = int(0.22 * SR)
    if nb < len(part): part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]
rng = np.random.default_rng(4); irl = int(1.6 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.35)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
