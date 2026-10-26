"""Mariachi-style ranchera score for FreshNestHub 09 "spicy food doesn't burn you" (GeneralUser GS): trumpets in thirds,
violins, nylon-guitar vihuela strums, guitarron bass, maracas/guiro; thin bed (bass + strum) under explanation lines
(coherence principle), full band on reveals, tense tremolo-strings + timpani for the alarm/FIRE, flute for the birds."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

TRP, TRP2, VLN, STR, GTR, BASS, FLT, MAR, TIMP, SUB, PAD, CEL, DR, TRB = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 9, 13
PROG = {TRP: 56, TRP2: 56, VLN: 40, STR: 44, GTR: 24, BASS: 32, FLT: 73, MAR: 12, TIMP: 47, SUB: 38, PAD: 89, CEL: 8, TRB: 57}
VOL = {TRP: 92, TRP2: 80, VLN: 84, STR: 82, GTR: 96, BASS: 108, FLT: 86, MAR: 88, TIMP: 98, SUB: 94, PAD: 54, CEL: 84, DR: 90, TRB: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"D": (38, [62, 66, 69, 74]), "G": (43, [62, 67, 71, 74]), "A7": (45, [61, 64, 67, 69]), "Bm": (47, [62, 66, 71, 74]),
      "F#": (42, [61, 66, 70, 73]), "Em": (40, [64, 67, 71, 76]), "A": (45, [61, 64, 69, 73])}
PROGS = {"main": ["D", "A7", "A7", "D"], "go": ["G", "D", "A7", "D"], "soft": ["Bm", "G", "D", "A"], "tense": ["Bm", "Bm", "F#", "F#"]}
BPM = 124
MOT = [(0, 2), (0.5, 1), (1, 0), (1.5, 1), (2, 2), (3, 3)]


def ranchera(t0, t1, prog="main", level=2, bpm=BPM):
    """2-feel ranchera: guitarron on 1 + 3, vihuela strums on 2 + 4; level 2 adds maracas/guiro + violins; 3 adds trumpets."""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            if q in (0, 2): n(tq, BASS, root if q == 0 else root + 7, 104, beat * 0.8)
            else:
                for i, k in enumerate(tri[:3]): n(tq + i * 0.012, GTR, k, 78 + 6 * level, beat * 0.4)
            if level >= 2:
                n(tq, DR, 70, 52 + (10 if q % 2 else 0), 0.06); n(tq + beat / 2, DR, 70, 44, 0.05)
                if q == 3: n(tq, DR, 73, 60, 0.2)
        if level >= 2:
            for k in tri[:2]: n(t, VLN, k + 12, 58 + 6 * level, bar * 0.95)
        if level >= 3:
            for off, idx in MOT:
                if t + off * beat < t1 - 0.05:
                    k = tri[idx % 4] + 12; n(t + off * beat, TRP, k, 92, beat * 0.45); n(t + off * beat, TRP2, k - 3 if idx % 2 else k - 4, 80, beat * 0.45)
        t += bar; b += 1


def tremolo(t0, t1, keys=(59, 62, 66), v=80):
    t = t0
    while t < t1 - 0.03:
        for k in keys: n(t, STR, k, v, 0.07)
        t += 0.075


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.8); n(t, DR, 36, v, 0.3); n(t, TIMP, 38, v - 14, 0.8)
    if big: n(t, SUB, 26, 108, 1.0); n(t, DR, 57, v - 14, 2.0)


def stab(t, chord="D", v=106, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, TRP, k + 12, v - 10, d); n(t, TRB, k, v - 16, d); n(t, VLN, k + 12, v - 20, d)
    n(t, BASS, root, 106, d)


def fanfare(t, notes=(74, 78, 81, 86), v=98, step=0.11):
    for i, k in enumerate(notes): n(t + i * step, TRP, k, v, step * 1.6); n(t + i * step, TRP2, k - 4, v - 10, step * 1.6)


def sparkle(t, base=86):
    for i, k in enumerate((base, base + 4, base + 7, base + 12)): n(t + i * 0.07, CEL, k, 90, 0.5)


def roll(t, d=0.6, v=80):
    for i in range(int(d / 0.05)): n(t + i * 0.05, TIMP, 38, v + i * 2, 0.08)


def run(t, k0=74, step=2, nn=6, dt=0.05, ch=TRP):
    for i in range(nn): n(t + i * dt, ch, k0 + i * step, 88, 0.12)


TF0 = T("i1", "food...") - 0.1
# hook: bouncy intro (munch) -> fire hit
ranchera(0.0, TF0 - 0.02, "main", 1)
hit(TF0, 104, True); stab(TF0, "D", 98, 0.35); run(TF0 + 0.05, 74, 3, 6)
tremolo(TF0 + 0.3, S["S1"] - 0.05, (62, 66, 69), 56)
hit(S["S1"] + 0.02, 108); ranchera(S["S1"] + 0.05, S["S1b"] - 0.05, "go", 3)
for k in (59, 62, 66): n(S["S1b"], PAD, k, 70, S["S2"] - S["S1b"])
for i in range(5): n(S["S1b"] + 0.25 + i * 0.3, MAR, (74, 71, 69, 66, 64)[i], 84, 0.2)
hit(T("i2", "trick!") - 0.15, 112); stab(T("i2", "trick!") - 0.15, "Bm", 108, 0.4)
# science: thin bed under explanations (coherence), small signals on each new term
ranchera(S["S2"], S["S3"] - 0.05, "soft", 1); sparkle(T("a1", "capsaicin.") - 0.1, 86); stab(T("a1", "capsaicin.") - 0.1, "G", 96, 0.25)
ranchera(S["S3"], S["S4"] - 0.05, "soft", 1)
for i in range(4): n(T("a2", "nerve") - 0.1 + i * 0.12, MAR, 81 + i * 2, 80, 0.15)
for i in range(6): n(T("a2", "wires") - 0.1 + i * 0.09, CEL, 86 + (i % 3) * 3, 70, 0.2)
ranchera(S["S4"], S["S5"] - 0.05, "soft", 2); sparkle(T("a3", "alarms.") - 0.3, 81)
ranchera(S["S5"], T("a4", "painful") - 0.15, "soft", 1)
for i in range(8): n(S["S5"] + 0.3 + i * 0.18, VLN, 62 + i * 2, 70 + i * 3, 0.2)
hit(T("a4", "painful") - 0.1, 110); stab(T("a4", "painful") - 0.1, "F#", 106, 0.4)
ranchera(S["S5b"], S["S6"] - 0.05, "go", 2); hit(T("a4", "scalding") + 0.25, 104)
ranchera(S["S6"], S["S6b"] - 0.05, "soft", 1)
for i in range(6): n(S["S6"] + 0.4 + i * 0.3, FLT, (74, 76, 78, 79, 81, 83)[i], 78, 0.25)
sparkle(T("a5", "perfectly.") - 0.25, 86); stab(T("a5", "perfectly.") - 0.25, "D", 96, 0.25)
ranchera(S["S6b"], S["S7"] - 0.05, "main", 2)
# CLICK -> alarm -> FIRE (tense)
hit(S["S7"] + 0.1, 116, True); tremolo(S["S7"] + 0.15, T("a6", "FIRE!") - 0.2, (59, 62, 66, 71), 64)
for k in (47, 54): n(S["S7"] + 0.1, SUB, k - 12, 100, T("a6", "FIRE!") - S["S7"] - 0.3)
roll(T("a6", "FIRE!") - 0.75, 0.6, 84)
hit(T("a6", "FIRE!") - 0.15, 124, True); stab(T("a6", "FIRE!") - 0.15, "Bm", 118, 0.6); run(T("a6", "FIRE!") - 0.1, 71, 3, 6)
ranchera(S["S8"], S["S8b"] - 0.05, "tense", 2)
ranchera(S["S8b"], S["S9"] - 0.05, "soft", 1)
# re-hook: Nobel
for k in (62, 66, 71): n(S["S9"], PAD, k, 66, S["S9b"] - S["S9"])
for i in range(8): n(S["S9"] + 0.2 + i * 0.32, CEL, (74, 78, 81, 86, 81, 78, 81, 86)[i], 74, 0.3)
hit(T("b1", "Nobel") - 0.15, 116, True); fanfare(T("b1", "Nobel") - 0.15, (74, 78, 81, 86, 90), 100, 0.12)
ranchera(T("b1", "Nobel") + 0.5, S["S10"] - 0.05, "go", 3)
# milk test
for k in (59, 62, 66): n(S["S10"], PAD, k, 66, S["S11"] - S["S10"])
n(T("c1", "fire?") - 0.1, TRP, 69, 90, 0.2); n(T("c1", "fire?") + 0.12, TRP, 73, 90, 0.35)
ranchera(S["S11"], S["S12"] - 0.05, "soft", 1)
for i in range(7): n(T("c2", "seven") - 0.2 + i * (T("c2", "drinks") - T("c2", "seven") + 0.1) / 7, MAR, 74 + i * 2, 86, 0.12)
for i in range(10): n(S["S11b"] + 0.05 + i * 0.09, MAR, 86 + (i % 2) * 2, 64 + i * 3, 0.06)
ranchera(S["S12"], S["S12b"] - 0.05, "soft", 2)
n(T("c3", "badly.") - 0.2, TRB, 50, 96, 0.25); n(T("c3", "badly.") + 0.05, TRB, 49, 96, 0.25); n(T("c3", "badly.") + 0.3, TRB, 48, 96, 0.6)
roll(S["S12b"] + 0.05, T("c3", "milk!") - S["S12b"] - 0.25, 80)
hit(T("c3", "milk!") - 0.15, 120, True); fanfare(T("c3", "milk!") - 0.12, (74, 78, 81, 86), 104, 0.11)
ranchera(T("c3", "milk!") + 0.4, S["S13b"] - 0.05, "main", 3)
ranchera(S["S13b"], S["S14"] - 0.05, "soft", 1)
for i in range(6): n(T("c4", "proteins") - 0.2 + i * 0.2, MAR, (81, 79, 78, 76, 74, 81)[i], 84, 0.15)
# weirdest part -> birds (flute) -> mice
hit(S["S14"] + 0.7, 112); stab(S["S14"] + 0.7, "F#", 108, 0.4)
ranchera(S["S14b"], S["S16"] - 0.05, "go", 2)
for i in range(16): n(S["S14b"] + 0.2 + i * 0.24, FLT, (86, 88, 90, 88, 86, 83, 81, 83)[i % 8], 80, 0.18)
for i in range(4): n(T("d2", "grow.") - 0.1 + i * 0.08, CEL, 86 + i * 3, 80, 0.4)
ranchera(S["S16"], S["S17"] - 0.05, "tense", 1)
for i in range(6): n(S["S16"] + 0.1 + i * 0.25, MAR, 64 + (i % 2), 90, 0.08)
hit(S["S16b"] + 0.35, 112, True); run(S["S16b"] + 0.45, 86, -3, 7, 0.05, FLT)
ranchera(S["S17"], S["S18"] - 0.05, "main", 3)
# recap: build 1-2-3 then sting
ranchera(S["S18"], S["S19"] - 0.05, "soft", 1)
for j in range(3): n(S["S18"] + 0.2 + 0.35 * j, MAR, (74, 78, 81)[j], 96, 0.3)
hit(T("e1", "burn.") - 0.2, 108); sparkle(T("e1", "milk") - 0.15, 86)
ranchera(S["S19"], END - 1.6, "main", 3)
for k in CH["D"][1]: n(END - 1.6, PAD, k, 74, 2.0); n(END - 1.6, TRP, k + 12, 96, 0.9)
n(END - 1.6, BASS, 38, 108, 1.2); hit(END - 1.6, 114, True); run(END - 1.55, 74, 3, 8, 0.05)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((TRP, 54), (TRP2, 74), (VLN, 40), (GTR, 84), (FLT, 70), (MAR, 50)): syn.control_change(ch, 10, pan)
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
rng = np.random.default_rng(4); irl = int(1.4 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.3)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.4) / np.tanh(1.4)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
