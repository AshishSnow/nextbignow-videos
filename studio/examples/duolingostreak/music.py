"""8-bit chiptune 'video-game' score for "Duolingo's streak" (GeneralUser GS): square-wave lead, saw arps, synth bass, punchy kit, level-up jingles on every reveal."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

# chiptune: square lead (80), saw arp (81), synth bass (38), square harmony (80), poly pad (90), xylophone blips (13), sub (38), kit
LEAD, ARP, BASS, HARM, PAD, XYL, SUB, BRS, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {LEAD: 80, ARP: 81, BASS: 38, HARM: 80, PAD: 90, XYL: 13, SUB: 38, BRS: 62}
VOL = {LEAD: 70, ARP: 62, BASS: 104, HARM: 58, PAD: 50, XYL: 92, SUB: 100, BRS: 84, DR: 100}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67]), "G": (43, [59, 62, 67]), "Am": (45, [60, 64, 69]), "F": (41, [60, 65, 69]),
      "Em": (40, [59, 64, 67]), "Dm": (38, [62, 65, 69]), "E": (40, [59, 64, 68]), "Bb": (46, [62, 65, 70])}
PROGS = {"main": ["C", "G", "Am", "F"], "tense": ["Am", "E", "Am", "E"], "win": ["F", "G", "C", "C"], "sad": ["Am", "Dm", "Em", "Am"]}
BPM = 132
MEL = {"main": [76, 79, 81, 79, 76, 74, 72, 74], "win": [72, 76, 79, 84, 83, 79, 81, 84], "tense": [69, 71, 72, 71, 69, 68, 69, 64], "sad": [69, 67, 65, 64, 62, 64, 65, 64]}


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    beat = 60 / bpm; bar = 4 * beat; s16 = beat / 4; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for i in range(16):
            tq = t + i * s16
            if tq >= t1 - 0.03: break
            if i % 4 == 0: n(tq, DR, 36, 96 if level >= 2 else 80, 0.1)              # kick on beats
            if i in (4, 12) and level >= 1: n(tq, DR, 38, 92, 0.1)                   # snare 2 and 4
            if i % 2 == 0 and level >= 2: n(tq, DR, 42, 52 + 8 * (i % 4 == 2), 0.05)  # hats
            if i % 2 == 0: n(tq, BASS, root - 12 + (12 if i % 4 == 2 else 0), 98, s16 * 1.6)  # octave bass
            if level >= 1: n(tq, ARP, tri[i % 3] + 12, 46 + 6 * level, s16 * 0.8)          # arpeggio
        if level >= 3:
            mel = MEL.get(prog, MEL["main"])
            for j, k in enumerate(mel):
                if t + j * 2 * s16 < t1 - 0.05: n(t + j * 2 * s16, LEAD, k, 64, s16 * 1.7)
        if level >= 2:
            for k in tri: n(t, PAD, k, 34, min(bar, t1 - t) * 0.98)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 18, 1.6); n(t, DR, 36, v, 0.2); n(t, DR, 38, v - 14, 0.2)
    if big: n(t, SUB, 31, 112, 0.8); n(t, DR, 57, v - 16, 2.0)


def stab(t, chord="C", v=104, d=0.25):
    root, tri = CH[chord]
    for k in tri: n(t, HARM, k + 12, v - 20, d); n(t, BRS, k, v - 30, d)
    n(t, BASS, root - 12, 104, d)


def levelup(t, base=72, v=96):
    for i, k in enumerate((base, base + 4, base + 7, base + 12, base + 16)): n(t + i * 0.06, LEAD, k, v, 0.09 if i < 4 else 0.35)


def coin(t, v=100):
    n(t, XYL, 83, v, 0.07); n(t + 0.07, XYL, 88, v, 0.3)


def fail(t, v=96):
    for i, k in enumerate((67, 66, 65, 64)): n(t + i * 0.16, LEAD, k, v, 0.15 if i < 3 else 0.6)


def riser(t_end, dur):
    m = int(dur / 0.05)
    for j in range(m): n(t_end - dur + j * 0.05, ARP, 60 + int(24 * j / m), 30 + int(70 * (j / m)), 0.045)
    for j in range(int(dur / 0.1)): n(t_end - dur + j * 0.1, DR, 38, 30 + int(70 * j / (dur / 0.1)), 0.05)


# ---- cues ----
tf = T("i1", "free…") - 0.2; tb = T("i1", "billion") - 0.25
groove(0.0, S["S0b"] - 0.05, "main", 2); stab(0.02, "C", 104); n(0.0, DR, 49, 90, 1.6)
hit(tf, 108); coin(tf + 0.05); riser(tb, 0.8); hit(tb, 120, True); stab(tb, "C", 112, 0.5); levelup(tb + 0.1, 72)
for j in range(5): coin(tb + 0.3 + 0.15 * j, 80)
hit(S["S0b"] + 0.02, 108); groove(S["S0b"] + 0.2, S["S1"] - 0.05, "tense", 1); stab(S["S0b"] + 0.3, "E", 106)
hit(S["S1"] + 0.02, 108); groove(S["S1"] + 0.2, T("i2", "streak.") - 0.3, "tense", 1); riser(T("i2", "streak.") - 0.25, 0.7)
hit(T("i2", "streak.") - 0.25, 122, True); stab(T("i2", "streak.") - 0.25, "C", 112, 0.6); levelup(T("i2", "streak.") - 0.1, 76)
groove(S["S2"], S["S3"] - 0.05, "main", 3); stab(S["S2"] + 0.02, "F", 104)
for j in range(6): coin(T("a1", "free.") - 0.25 + 0.06 * j, 84)
stab(T("a1", "ad") - 0.25, "Am", 108); hit(T("a1", "ad") - 0.25, 112)
groove(S["S3"], S["S4"] - 0.05, "tense", 1); hit(T("a2", "eight") - 0.25, 118, True); stab(T("a2", "eight") - 0.25, "E", 108, 0.5)
groove(S["S4"], S["S5"] - 0.05, "main", 2); hit(T("a3", "nine") - 0.25, 116); stab(T("a3", "nine") - 0.25, "G", 108)
for j in range(9): coin(T("a3", "nine") - 0.1 + 0.08 * j, 82)
groove(S["S5"], S["S6"] - 0.05, "win", 2); riser(T("a4", "twelve") - 0.3, 1.1); hit(T("a4", "twelve") - 0.3, 122, True)
stab(T("a4", "twelve") - 0.3, "C", 112, 0.5); levelup(T("a4", "twelve") - 0.2, 72)
groove(S["S6"], S["S7"] - 0.05, "main", 3)
for j in range(3): n(S["S6"] + 0.35 + 0.55 * j, XYL, 91, 96, 0.12); n(S["S6"] + 0.45 + 0.55 * j, XYL, 86, 90, 0.2)
stab(T("b1", "Every") - 0.2, "G", 106)
groove(S["S7"], T("b2", "zero.") - 0.35, "main", 2)
for j in range(6): coin(S["S7"] + 0.32 * j + 0.02, 78)
hit(T("b2", "Miss") - 0.15, 112); stab(T("b2", "Miss") - 0.15, "Am", 106); fail(T("b2", "zero.") - 0.3); n(T("b2", "zero.") - 0.3, SUB, 28, 110, 1.0)
groove(S["S8"], T("b3", "hundred,") - 0.35, "sad", 1); hit(T("b3", "hundred,") - 0.3, 118, True); stab(T("b3", "hundred,") - 0.3, "E", 110, 0.5)
groove(T("b3", "hundred,"), S["S9"] - 0.05, "tense", 2)
# re-hook: drumroll + envelope
hit(S["S9"] + 0.02, 112); riser(T("c0", "Wait") + 0.9, 1.6); stab(T("c0", "Wait") - 0.15, "E", 104)
hit(S["S10"] + 0.02, 120, True); groove(S["S10"] + 0.2, S["S11"] - 0.05, "win", 3); stab(T("c1", "forty") - 0.3, "C", 112, 0.5); levelup(T("c1", "forty") - 0.2, 76)
groove(S["S11"], S["S12"] - 0.05, "main", 3); riser(T("c2", "year!") - 0.3, 1.0); hit(T("c2", "year!") - 0.3, 122, True); levelup(T("c2", "year!") - 0.2, 79)
groove(S["S12"], T("c3", "revived") - 0.25, "sad", 1)
for j in range(3): n(S["S12"] + 0.2 + 0.6 * j, XYL, 96, 70, 0.08)
hit(T("c3", "revived") - 0.2, 118, True); stab(T("c3", "revived") - 0.2, "F", 108); levelup(T("c3", "revived") - 0.1, 77)
groove(T("c3", "revived") + 0.3, S["S13"] - 0.05, "win", 2)
# twist
hit(S["S13"] + 0.02, 116, True); stab(S["S13"] + 0.02, "Am", 110, 0.5); groove(S["S13"] + 0.3, S["S14"] - 0.05, "tense", 2)
stab(T("d1", "ad…") - 0.25, "E", 106); coin(T("d1", "pay.") - 0.3, 100)
groove(S["S14"], S["S15"] - 0.05, "main", 2); stab(T("d2", "habit") - 0.25, "C", 110, 0.5); hit(T("d2", "habit") - 0.25, 116, True)
hit(S["S15"] + 0.02, 110); groove(S["S15"] + 0.1, S["S15b"] - 0.05, "tense", 1)
for j in range(6): n(S["S15"] + 0.1 + 0.18 * j, XYL, (72, 75, 72, 75, 72, 79)[j], 84, 0.12)
groove(S["S15b"], S["S16"] - 0.05, "win", 2); riser(T("d3", "three") - 0.3, 1.0); hit(T("d3", "three") - 0.3, 124, True)
stab(T("d3", "three") - 0.3, "C", 114, 0.6); levelup(T("d3", "three") - 0.2, 72)
groove(S["S16"], S["S17"] - 0.05, "main", 3)
for j in range(7): coin(T("e1", "Start") - 0.2 + j * max(0.2, (T("e1", "seven") - T("e1", "Start")) / 6), 84)
hit(T("e1", "seven") - 0.3, 122, True); levelup(T("e1", "seven") - 0.2, 76)
hit(S["S17"] + 0.02, 110); groove(S["S17"] + 0.1, END - 1.6, "win", 3)
for k in CH["C"][1]: n(END - 1.6, PAD, k, 70, 2.0); n(END - 1.6, HARM, k + 12, 90, 0.8)
n(END - 1.6, BASS, 24, 104, 1.6); hit(END - 1.6, 104); levelup(END - 1.5, 72, 90)


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
cuts = sorted(set([0.0] + [S[k] for k in S if k != "S0"] + [END + 3]))
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
