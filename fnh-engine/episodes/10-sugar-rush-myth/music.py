"""Spooky SURF-ROCK score for FreshNestHub 10 "the sugar rush myth" (Halloween week; GeneralUser GS): reverb-drenched
tremolo-picked clean guitar in E Phrygian-dominant (the Misirlou colour), driving surf beat (16th hats, snare 2+4),
picked electric bass, haunted-house organ stabs, an ocarina 'theremin' that glides on the mystery beats.
Thin bed (bass + hats) under explanation lines (coherence), full band on reveals, stop-time hits on the busts."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

GTR, GTR2, BASS, ORG, THR, CEL, TIMP, SUB, PAD, BRS, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9
PROG = {GTR: 27, GTR2: 28, BASS: 34, ORG: 19, THR: 79, CEL: 8, TIMP: 47, SUB: 38, PAD: 91, BRS: 61}
VOL = {GTR: 96, GTR2: 84, BASS: 110, ORG: 70, THR: 92, CEL: 86, TIMP: 98, SUB: 94, PAD: 56, BRS: 88, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# E Phrygian dominant progression: E - F - E - Dm/G-ish ; chords (root, tones)
CH = {"E": (40, [52, 56, 59, 64]), "F": (41, [53, 57, 60, 65]), "Am": (45, [57, 60, 64, 69]), "G": (43, [55, 59, 62, 67]), "Dm": (38, [50, 53, 57, 62])}
PROGS = {"main": ["E", "F", "E", "F"], "go": ["Am", "G", "F", "E"], "soft": ["E", "E", "F", "E"], "tense": ["E", "F", "E", "F"]}
BPM = 150
MEL = [64, 65, 68, 69, 71, 72, 71, 69, 68, 69, 68, 65, 64, 65, 64, 64]  # tremolo melody (8ths)


def surf(t0, t1, prog="main", level=2, bpm=BPM):
    """surf beat. level 1: bass + hats; 2: + snare/kick + rhythm guitar; 3: + tremolo lead melody + organ pad."""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(8):
            tq = t + q * beat / 2
            if tq >= t1 - 0.03: break
            n(tq, BASS, root + (12 if q % 4 == 3 else 0) + (7 if q in (2, 6) else 0), 100 - 8 * (q % 2), beat * 0.42)
            n(tq, DR, 42, 46 + (12 if q % 2 == 0 else 0), 0.05); n(tq + beat / 4, DR, 42, 36, 0.04)
            if level >= 2:
                if q in (0, 4): n(tq, DR, 36, 96, 0.1)
                if q in (2, 6): n(tq, DR, 38, 90, 0.1)
                if q in (1, 3, 5, 7):
                    for i, k in enumerate(tri[:3]): n(tq + i * 0.008, GTR2, k, 66 + 6 * level, beat * 0.3)
            if level >= 3:
                mk = MEL[(b % 2) * 8 + q] + (0 if PROGS[prog][b % 4] in ("E", "F") else -2)
                for r in range(4): n(tq + r * beat / 8, GTR, mk, 86 - 8 * (r % 2), beat / 8 * 0.9)
        if level >= 3:
            for k in tri[:3]: n(t, ORG, k, 52, bar * 0.95)
        t += bar; b += 1


def tremolo(t0, t1, k=64, v=84):
    t = t0
    while t < t1 - 0.03: n(t, GTR, k, v, 0.045); t += 0.05


def glide(t0, k0, k1, d=0.6, v=86, ch=THR):
    """'theremin' slide: chromatic notes from k0 to k1 over d seconds."""
    steps = abs(k1 - k0) or 1
    for i in range(steps + 1): n(t0 + d * i / steps, ch, k0 + (i if k1 > k0 else -i), v, d / steps * 1.6)


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.8); n(t, DR, 36, v, 0.3); n(t, TIMP, 40, v - 14, 0.8)
    if big: n(t, SUB, 28, 108, 1.0); n(t, DR, 57, v - 14, 2.0)


def stab(t, chord="E", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, ORG, k + 12, v - 14, d); n(t, BRS, k, v - 20, d); n(t, GTR2, k, v - 20, d)
    n(t, BASS, root, 106, d)


def sparkle(t, base=88):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 90, 0.5)


def roll(t, d=0.6, v=80):
    for i in range(int(d / 0.05)): n(t + i * 0.05, DR, 38, v + i * 2, 0.06)


def run(t, k0=64, step=1, nn=8, dt=0.05, ch=GTR):
    for i in range(nn): n(t + i * dt, ch, k0 + i * step, 92, 0.1)


def drip(t, nn=6, base=76):
    for i in range(nn): n(t + i * 0.16, CEL, base - (i % 3) * 3, 70, 0.3)


TFZ = T("i1", "myth?") - 0.12
# hook: full surf at t=0 (motion already happening) -> freeze (record scratch, everything stops)
surf(0.0, TFZ - 0.02, "main", 2)
hit(TFZ, 108, True); glide(TFZ + 0.1, 76, 64, 0.8, 90)
for k in (52, 53, 59): n(TFZ + 0.05, PAD, k, 60, S["S1"] - TFZ - 0.1)
# bounce off the walls
hit(S["S1"] + 0.02, 104); surf(S["S1"] + 0.03, S["S1b"] - 0.05, "go", 2)
surf(S["S1b"], S["S2"] - 0.05, "soft", 2); stab(T("i2", "tested") - 0.1, "E", 100, 0.3)
# open loop (curtain): theremin + organ, drum roll to "weirder"
for k in (52, 53, 59): n(S["S2"], ORG, k, 64, S["S3"] - S["S2"])
glide(S["S2"] + 0.2, 64, 71, 0.9, 84); glide(S["S2"] + 1.4, 71, 65, 0.9, 84)
roll(T("i3", "weirder.") - 0.75, 0.55, 74); hit(T("i3", "weirder.") - 0.2, 110); stab(T("i3", "weirder.") - 0.2, "F", 104, 0.4)
# the myth: bright, cheesy, full band; BOOM
surf(S["S3"], S["S3b"] - 0.05, "go", 3)
hit(S["S3b"] + 0.02, 120, True); stab(S["S3b"] + 0.02, "E", 112, 0.5); run(S["S3b"] + 0.08, 64, 1, 10)
surf(S["S3b"] + 0.3, S["S4"] - 0.05, "main", 3)
# BUSTED: stop-time + buzzer-ish brass fall
hit(S["S4"] + 0.15, 116, True)
for i, k in enumerate((59, 58, 57, 56)): n(S["S4"] + 0.2 + i * 0.12, BRS, k, 96, 0.14 if i < 3 else 0.5)
surf(S["S4"] + 0.9, S["S5"] - 0.05, "soft", 1)
# science section: thin bed + small signals on each new term
surf(S["S5"], S["S6"] - 0.05, "soft", 1); drip(S["S5"] + 0.3, 6, 79); sparkle(T("b1", "riding") - 0.1, 84)
sparkle(T("b1", "fuel") - 0.1, 88)
surf(S["S6"], S["S7"] - 0.05, "soft", 1); glide(T("b2", "rises,") - 0.3, 60, 67, 0.5, 70)
sparkle(T("b2", "wakes") - 0.1, 86); stab(T("b2", "pancreas") - 0.1, "Am", 92, 0.25)
surf(S["S7"], S["S8"] - 0.05, "soft", 2)
for j in range(5): n(T("b3", "insulin.") - 0.3 + j * 0.18, CEL, 83 + j * 2, 82, 0.3)
hit(T("b3", "key.") - 0.2, 100); sparkle(T("b3", "key.") - 0.15, 88)
surf(S["S8"], S["S8b"] - 0.05, "soft", 1); n(T("b4", "cells,") - 0.1, CEL, 95, 96, 0.4); n(T("b4", "cells,") + 0.05, CEL, 100, 96, 0.5)
surf(S["S8b"], S["S9"] - 0.05, "soft", 2)
surf(S["S9"], S["S10"] - 0.05, "soft", 1)
for k in (52, 59, 64): n(S["S9b"], PAD, k, 60, S["S10"] - S["S9b"])
# PART 2 re-hook: blind tests
hit(S["S10"] + 0.05, 112, True); stab(S["S10"] + 0.05, "Am", 108, 0.35)
surf(S["S10"] + 0.3, S["S11"] - 0.05, "go", 2); hit(T("c1", "blind"), 110); stab(T("c1", "blind"), "E", 106, 0.4)
surf(S["S11"], S["S12"] - 0.05, "soft", 1); sparkle(T("c2", "same.") - 0.15, 86)
surf(S["S12"], S["S13"] - 0.05, "soft", 2); glide(T("c3", "scientists.") - 0.2, 72, 60, 0.5, 86)
surf(S["S13"], S["S14"] - 0.05, "soft", 1)
for j in range(12): n(T("c4", "pooled") - 0.2 + j * 0.13, CEL, 76 + (j % 4) * 3, 70 + j * 2, 0.15)
roll(S["S14"] + 0.05, max(0.2, T("c5", "didn't") - S["S14"] - 0.2), 70)
hit(T("c5", "didn't") - 0.1, 118, True); stab(T("c5", "didn't") - 0.1, "F", 108, 0.5)
surf(T("c5", "didn't") + 0.4, S["S15"] - 0.05, "soft", 1)
# PART 3 re-hook: the parent test (spooky)
for k in (52, 53, 59): n(S["S15"], ORG, k, 70, S["S16"] - S["S15"])
glide(S["S15"] + 0.3, 64, 72, 0.8, 86); hit(T("d1", "wild.") - 0.15, 112, True); stab(T("d1", "wild.") - 0.15, "E", 110, 0.4)
surf(S["S16"], S["S17"] - 0.05, "main", 2)
for j in range(10): n(S["S16"] + 0.05 + j * 0.09, CEL, 88 + (j % 2) * 2, 64 + j * 3, 0.08)
stab(T("d2", "sugar-free.") - 0.15, "Am", 104, 0.35)
surf(S["S17"], S["S18"] - 0.05, "tense", 1); tremolo(T("d3", "told...") - 0.2, T("d3", "big") - 0.1, 64, 70)
hit(T("d3", "big") - 0.1, 104)
surf(S["S18"], S["S18b"] - 0.05, "tense", 2); hit(T("d4", "hyper.") - 0.3, 108)
surf(S["S18b"], S["S19"] - 0.05, "tense", 1)
hit(S["S19"] + 0.02, 100); hit(T("d5", "Different") - 0.15, 104)
for k in (52, 53, 59): n(S["S19b"], PAD, k, 64, S["S20"] - S["S19b"])
glide(S["S19b"] + 0.2, 64, 76, 1.0, 88); hit(T("d5", "heads!") - 0.2, 116, True); stab(T("d5", "heads!") - 0.2, "E", 112, 0.5)
# payoff: the real rush = party surf
surf(S["S20"], S["S21"] - 0.05, "soft", 2); roll(T("e1", "where") - 0.4, 0.4, 70)
surf(S["S21"], S["S22"] - 0.05, "go", 3)
hit(T("e2", "Halloween.") - 0.12, 108); glide(T("e2", "Halloween.") - 0.05, 76, 70, 0.4, 86)
hit(T("e2", "real") - 0.15, 120, True); stab(T("e2", "real") - 0.15, "E", 112, 0.4); run(T("e2", "real") - 0.1, 64, 2, 8)
# honest catch + teeth: soft
surf(S["S22"], S["S24"] - 0.05, "soft", 1); n(T("f2", "teeth.") - 0.2, BRS, 52, 90, 0.5)
# recap 1-2-3 then sting
surf(S["S24"], S["S25"] - 0.05, "soft", 2)
for j, tw in enumerate((T("g1", "insulin") - 0.15, T("g1", "blind") - 0.15, T("g1", "party") - 0.15)): n(tw, CEL, (76, 80, 83)[j], 96, 0.4)
hit(T("g1", "rest.") - 0.1, 112)
surf(S["S25"], END - 1.6, "main", 3)
for k in CH["E"][1]: n(END - 1.6, ORG, k + 12, 84, 2.0)
n(END - 1.6, BASS, 40, 110, 1.2); hit(END - 1.6, 116, True); run(END - 1.55, 64, 1, 12, 0.04); glide(END - 1.2, 71, 76, 0.5, 90)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 44), (GTR2, 86), (ORG, 60), (THR, 74), (CEL, 54)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = np.zeros((int((END + 3) * SR), 2), np.float32)
cuts = sorted(set([0.0] + [S[k] for k in S if k != "S0"] + [END + 3]))
evs = sorted(ev)
for a, b in zip(cuts[:-1], cuts[1:]):
    part = render([e for e in evs if a - 0.01 <= e[0] < b - 0.01], END)
    nb = int(b * SR); tail = int(0.22 * SR)
    if nb < len(part): part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]
# surf = lots of spring reverb: longer, brighter tail than ep 09
rng = np.random.default_rng(4); irl = int(2.0 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.45)[:, None] * (1 + 0.3 * np.sin(2 * np.pi * 9 * tt))[:, None]; ir[: int(0.015 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, [400, 7000], "band", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.22 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
