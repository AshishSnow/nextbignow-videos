"""Disco score for "One company behind your glasses" (GeneralUser GS) — new genre: 1970s disco / Philly soul.
Four-on-the-floor kick, open hi-hat on the off-beats, handclaps, octave-jumping bass, clavinet + muted "chicken-scratch" guitar,
string swells and brass stabs; a minor half-time strings + timpani section for the Oakley story; glockenspiel sparkles on reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
CLV, BASS, GTR, STR, BRS, GLK, PAD, TIMP, SUB, EP, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9
PROG = {CLV: 7, BASS: 36, GTR: 28, STR: 48, BRS: 61, GLK: 9, PAD: 89, TIMP: 47, SUB: 38, EP: 4}
VOL = {CLV: 76, BASS: 106, GTR: 70, STR: 74, BRS: 84, GLK: 84, PAD: 60, TIMP: 108, SUB: 98, EP: 70, DR: 88}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Am": (33, [57, 60, 64]), "Dm": (38, [57, 62, 65]), "G": (31, [55, 59, 62]), "C": (36, [55, 60, 64]), "F": (41, [57, 60, 65]),
      "Em": (40, [55, 59, 64]), "E7": (40, [56, 59, 62]), "Bb": (34, [58, 62, 65]), "D": (38, [57, 62, 66])}
PROGS = {"main": ["Am", "D", "G", "C"], "lift": ["F", "G", "Em", "Am"], "dark": ["Am", "F", "Dm", "E7"], "win": ["F", "G", "C", "C"]}
BPM = 118


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for i in range(8):                                   # octave-jumping disco bass
            tq = t + i * beat / 2
            if tq < t1 - 0.03: n(tq, BASS, root - 12 + (12 if i % 2 else 0), 98 if i % 2 == 0 else 84, beat * 0.4)
        for i in range(4):                                   # four on the floor + off-beat open hat
            tq = t + i * beat
            if tq >= t1 - 0.03: break
            n(tq, DR, 36, 104 if level >= 2 else 80, 0.15)
            if level >= 2: n(tq + beat / 2, DR, 46, 64, 0.12)
            else: n(tq + beat / 2, DR, 42, 50, 0.08)
            if i in (1, 3) and level >= 2: n(tq, DR, 39, 86, 0.1)
        if level >= 1:
            for off in (0.5, 1.5, 2.5, 3.5):                 # clavinet off-beat chords
                tq = t + off * beat
                if tq < t1 - 0.03:
                    for k in tri: n(tq, CLV, k, 66 + 6 * min(level, 3), beat * 0.25)
            for i in range(16):                              # muted 16th guitar scratch
                tq = t + i * beat / 4
                if tq < t1 - 0.03 and level >= 2: n(tq, GTR, tri[1] + 12, 50 + 18 * (i % 4 == 2), 0.06)
        if level >= 3:
            for k in tri: n(t, STR, k + 12, 64, bar * 0.95)
            if b % 2 == 1:
                for j, iv in enumerate((12, 16, 19, 24)): n(t + (2 + j * 0.25) * beat, STR, root + 36 + iv - 12, 70, beat * 0.3)
        t += bar; b += 1


def halftime(t0, t1, prog="dark", bpm=BPM):
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        n(t, BASS, root - 12, 92, beat * 1.8); n(t + 2.5 * beat, BASS, root - 12, 80, beat * 1.2)
        n(t, DR, 36, 90, 0.2); n(t + 2 * beat, DR, 38, 70, 0.2)
        for i in range(4): n(t + i * beat, DR, 42, 44, 0.06)
        for k in tri: n(t, STR, k, 64, bar * 0.95); n(t, PAD, k - 12, 54, bar * 0.95)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TIMP, 40, v, 1.4); n(t, DR, 49, v - 16, 2.0); n(t, DR, 36, v, 0.3)
    if big: n(t, SUB, 26, 112, 1.4); n(t, DR, 57, v - 10, 2.4)


def stab(t, chord="C", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, BRS, k + 12, v, d); n(t, STR, k + 12, v - 14, d); n(t, CLV, k, v - 10, d)
    n(t, BASS, root - 12, 104, d)


def riser(t_end, dur):
    m = int(dur / 0.07)
    for j in range(m): n(t_end - dur + j * 0.07, DR, 38, 20 + int(80 * (j / m) ** 1.8), 0.05)
    for i, p in enumerate((60, 63, 67, 70, 72)): n(t_end - dur + i * dur / 5, STR, p, 54 + 9 * i, t_end - (t_end - dur + i * dur / 5))


def sparkle(t, base=84):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, GLK, k, 92, 0.5)


def pad(t0, t1, chord, v=56):
    for k in CH[chord][1]: n(t0, PAD, k - 12, v, max(0.1, t1 - t0))


def swell(t0, t1, chord, v=62):
    for k in CH[chord][1]: n(t0, STR, k + 12, v, max(0.1, t1 - t0))


# ---- cues ----
pad(0.0, S["S1"], "Am", 58); sparkle(0.05, 84)
groove(0.3, S["S1"] - 0.05, "main", 2)
hit(T("i1", "one") - 0.1, 106); stab(T("i1", "one") - 0.1, "Am", 104)
groove(S["S1"], S["S3"] - 0.05, "main", 1)
riser(T("i3", "sneakiest") - 0.15, 1.0); hit(T("i3", "sneakiest") - 0.15, 116, True); stab(T("i3", "sneakiest") - 0.15, "E7", 110, 0.5)
stab(S["S3"] + 0.02, "C", 108); sparkle(S["S3"] + 0.4, 88)
groove(S["S3"] + 0.25, S["S8"] - 0.05, "main", 3)
for w_ in ("Ray-Ban.", "Oakley.", "Persol.", "Oliver"): stab(T("a2", w_) - 0.1, "G", 96, 0.15)
hit(T("a2", "All") - 0.1, 108)
for w_ in ("Chanel,", "Prada,", "Armani,", "Versace,", "Michael"): sparkle(T("a3", w_) - 0.1, 90)
hit(T("a5", "one") - 0.2, 110); stab(T("a5", "one") - 0.2, "Am", 106)
stab(S["S8"] + 0.02, "F", 106); sparkle(S["S8"] + 0.4, 86)
groove(S["S8"] + 0.25, S["S11"] - 0.05, "lift", 2)
hit(T("b2", "joined") + 0.55, 110); stab(T("b2", "joined") + 0.55, "C", 104)
hit(T("b3", "same") - 0.15, 106)
stab(S["S11"] + 0.02, "G", 106); sparkle(S["S11"] + 0.4, 88)
groove(S["S11"] + 0.25, S["S14"] - 0.05, "main", 3)
hit(T("c2", "same") - 0.15, 110); stab(T("c2", "same") - 0.15, "Am", 104)
riser(T("c3", "twenty") - 0.15, 0.8); hit(T("c3", "twenty") - 0.15, 112)
pad(S["S14"], S["S15"], "Dm", 62); swell(S["S14"], S["S15"], "Dm", 60); hit(T("c4", "Oakley.") - 0.2, 108)
halftime(S["S15"], S["S19"] - 0.05, "dark")
hit(T("s2", "bought") - 0.15, 112); stab(T("s2", "bought") - 0.15, "Dm", 104, 0.5)
riser(T("s4", "fell") - 0.15, 1.2); hit(T("s4", "fell") - 0.15, 122, True); stab(T("s4", "fell") - 0.15, "E7", 114, 0.7)
groove(S["S19"], S["S20"] - 0.05, "win", 2)
hit(T("s5", "billion") - 0.25, 116, True); stab(T("s5", "billion") - 0.25, "C", 110, 0.5); sparkle(T("s5", "billion") - 0.1, 90)
stab(S["S20"] + 0.02, "Am", 108); sparkle(S["S20"] + 0.5, 84)
groove(S["S20"] + 0.25, S["S24"] - 0.05, "dark", 2)
hit(T("d3", "same") - 0.1, 118, True); stab(T("d3", "same") - 0.1, "E7", 110, 0.5)
sparkle(T("d4", "smart") - 0.1, 92); hit(T("d4", "three") - 0.15, 108)
hit(S["S24"], 116, True); stab(S["S24"] + 0.02, "Am", 110)
groove(S["S24"] + 0.3, S["S25"] - 0.05, "main", 3)
for w_ in ("frame,", "lens,", "shop,", "plan"): stab(T("t1", w_) - 0.15, "Am", 100, 0.18)
hit(T("t1", "pays.") - 0.15, 116, True)
groove(S["S25"], END - 1.6, "win", 3)
sparkle(T("e0", "free") - 0.15, 88); hit(T("e1", "one") - 0.15, 110); stab(T("e1", "one") - 0.15, "G", 104)
for k in CH["C"][1]: n(END - 1.6, STR, k + 12, 92, 1.6); n(END - 1.6, PAD, k - 12, 72, 2.0); n(END - 1.6, BRS, k + 12, 96, 0.8)
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
cuts = sorted(set([0.0] + [S[k] for k in ("S1", "S3", "S8", "S11", "S14", "S15", "S19", "S20", "S24", "S25")] + [END + 3]))
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
