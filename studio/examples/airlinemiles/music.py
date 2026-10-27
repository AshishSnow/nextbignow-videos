"""Bossa-nova / airport-lounge jazz score for "Your airline's real money machine is your credit card" (GeneralUser GS): nylon guitar comping,
upright bass on roots and fifths, Rhodes pad, vibraphone melody, cross-stick clave + brushed hats, muted-trumpet stabs and flute sparkles on reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

GTR, BASS, EP, VIB, TPT, FLT, SUB, STR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {GTR: 24, BASS: 32, EP: 4, VIB: 11, TPT: 59, FLT: 73, SUB: 38, STR: 48}
VOL = {GTR: 84, BASS: 108, EP: 56, VIB: 70, TPT: 82, FLT: 70, SUB: 100, STR: 50, DR: 96}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Cmaj7": (36, [52, 55, 59, 60]), "Am7": (45, [52, 55, 57, 60]), "Dm7": (38, [53, 57, 60, 62]), "G7": (43, [53, 55, 59, 62]),
      "Fmaj7": (41, [52, 57, 60, 64]), "E7": (40, [52, 56, 59, 62]), "Bb7": (46, [50, 53, 56, 58]), "Ebmaj7": (39, [50, 55, 58, 62])}
PROGS = {"main": ["Cmaj7", "Am7", "Dm7", "G7"], "lift": ["Fmaj7", "G7", "Cmaj7", "Am7"], "tense": ["Am7", "E7", "Am7", "E7"],
         "win": ["Fmaj7", "G7", "Ebmaj7", "G7"]}
BPM = 132
MEL = {"main": [67, 69, 71, 72, 71, 69, 67, 64], "lift": [72, 71, 69, 67, 69, 72, 76, 74], "win": [72, 74, 76, 79, 76, 74, 72, 71],
       "tense": [64, 65, 64, 62, 64, 68, 69, 71]}
CLAVE = (0, 3, 6, 10, 13)   # bossa clave on 16ths over two bars


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    """bossa: kick on 1 and the 'and' of 2, cross-stick clave, 8th-note brushed hats; bass root-fifth; nylon guitar syncopated comp;
    Rhodes pad at level >= 2; vibraphone melody at level 3"""
    beat = 60 / bpm; bar = 4 * beat; s16 = beat / 4; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        for i in range(16):
            tq = t + i * s16
            if tq >= t1 - 0.03: break
            if i in (0, 6, 8, 14): n(tq, DR, 36, 84 if level >= 2 else 70, 0.1)
            if level >= 1 and (i + 16 * (b % 2)) % 32 in [c + 16 * ((b % 2)) for c in CLAVE if c < 16] and i in CLAVE: n(tq, DR, 37, 70, 0.05)
            if level >= 1 and i % 2 == 0: n(tq, DR, 42, 34 + 8 * (i % 4 == 0), 0.04)
            if i in (0, 6): n(tq, BASS, root - 12 if root >= 36 else root, 98, s16 * 5.5)
            if i in (8, 14): n(tq, BASS, root - 5, 90, s16 * 5.5)
            if i in (0, 3, 6, 10, 12) and level >= 1:
                for k in tri: n(tq, GTR, k, 60 + 4 * level - (6 if i == 12 else 0), s16 * 1.6)
        if level >= 2:
            for k in tri: n(t, EP, k + 12, 40, min(bar, t1 - t) * 0.98)
        if level >= 3:
            mel = MEL.get(prog, MEL["main"])
            for j, k in enumerate(mel):
                tq = t + j * beat / 2
                if tq < t1 - 0.05: n(tq, VIB, k + 12, 70 - 4 * (j % 2), beat * 0.45)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 26, 1.6); n(t, DR, 36, v, 0.2); n(t, DR, 38, v - 20, 0.2)
    if big: n(t, SUB, 31, 108, 0.8)


def stab(t, chord="Cmaj7", v=104, d=0.25):
    root, tri = CH[chord]
    for k in tri: n(t, TPT, k + 12, v - 22, d); n(t, GTR, k, v - 30, d)
    n(t, BASS, root - 12 if root >= 36 else root, 104, d)


def flute(t, base=79, v=92):   # quick flute flourish
    for i, k in enumerate((base - 7, base - 5, base - 3, base, base + 5)): n(t + i * 0.06, FLT, k, v, 0.09 if i < 4 else 0.5)


def bell(t, v=96, k=84):
    n(t, VIB, k, v, 0.6); n(t + 0.09, VIB, k + 7, v - 10, 0.7)


def riser(t_end, dur):
    m = int(dur / 0.05)
    for j in range(m): n(t_end - dur + j * 0.05, STR, 52 + int(24 * j / m), 30 + int(60 * (j / m)), 0.06)
    for j in range(int(dur / 0.1)): n(t_end - dur + j * 0.1, DR, 38, 30 + int(60 * j / (dur / 0.1)), 0.05)


def drumroll(t0, dur):
    for j in range(int(dur / 0.06)): n(t0 + j * 0.06, DR, 38, 36 + int(56 * j * 0.06 / dur), 0.04)


# ---- cues (every reveal gets a hit/stab/bell) ----
def seg(a, b, prog, lvl): groove(a, b - 0.05, prog, lvl)


te = T("i1", "eight") - 0.2
seg(0.0, S["S1"], "main", 1); stab(0.02, "Cmaj7", 96); n(0.0, DR, 49, 70, 1.6); hit(te, 110); stab(te, "G7", 104, 0.5); flute(te + 0.1, 79, 80)
hit(S["S1"] + 0.02, 106); seg(S["S1"] + 0.1, S["S2"], "lift", 2); td = T("i2", "Delta") - 0.1; stab(td, "Fmaj7", 108); bell(td + 0.1)
tf = T("a1", "Five") - 0.15
seg(S["S2"], S["S2b"], "tense", 1); hit(tf, 116, True); stab(tf, "Am7", 108, 0.4)
seg(S["S2b"] + 0.2, S["S3"], "tense", 1)
tb = T("a2", "bigger") - 0.2 + 0.4
seg(S["S3"], tb - 0.4, "tense", 1); drumroll(S["S3"] + 0.2, max(0.3, tb - S["S3"] - 0.3)); hit(tb, 124, True); stab(tb, "G7", 114, 0.6); flute(tb + 0.1, 84)
seg(tb + 0.3, S["S4"], "win", 2)
seg(S["S4"], S["S5"], "lift", 3)
t54 = T("b1", "fifty") - 0.25
seg(S["S5"], S["S6"], "main", 2); hit(t54, 112); stab(t54, "Cmaj7", 106); bell(t54 + 0.1, 88, 88)
tm = T("b2", "million") - 0.3
seg(S["S6"], tm, "tense", 1); hit(tm, 118, True); stab(tm, "E7", 108, 0.5); seg(tm + 0.4, S["S7"], "tense", 1)
t62 = T("b3", "six") - 0.25
seg(S["S7"], t62, "main", 1); riser(t62, 0.6); hit(t62, 120, True); stab(t62, "G7", 112, 0.5); hit(t62 + 0.9, 118); stab(t62 + 0.9, "Cmaj7", 110, 0.5); flute(t62 + 1.0, 86)
seg(t62 + 0.5, S["S8"], "win", 2)
seg(S["S8"], S["S8b"], "tense", 1); tym = T("c1", "Your") - 0.15; hit(tym, 116, True); stab(tym, "Fmaj7", 110, 0.5); bell(tym + 0.1, 100, 88)
seg(S["S8b"] + 0.3, S["S9"], "lift", 2)
tsw = T("c2", "swipe") - 0.1; tpy = T("c2", "pays") - 0.1
seg(S["S9"], S["S10"], "main", 2); bell(tsw, 86, 91); stab(tpy, "G7", 106); n(tpy + 0.3, VIB, 96, 80, 0.5)
for j in range(4): n(S["S9b"] + 0.3 + 0.2 * j, VIB, 84 + 3 * j, 70, 0.3)
seg(S["S10"], S["S10b"], "lift", 3); flute(S["S10"] + 0.1, 84)
seg(S["S10b"], S["S10c"], "main", 2); stab(S["S10b"] + 0.02, "Am7", 100)
tn = T("c3", "number") - 0.2
seg(S["S10c"], S["S11"], "main", 2); stab(tn, "Dm7", 106); bell(T("c3", "adds") - 0.1, 90, 88)
# re-hook: music stops, a drumroll under the departures board, big reveal on 2020
t20 = T("d1", "twenty") - 0.3
hit(S["S11"] + 0.02, 106); stab(S["S11"] + 0.02, "E7", 100, 0.6); hit(t20, 124, True); stab(t20, "Am7", 114, 0.6)
tpk = T("d2", "parked") - 0.2
seg(S["S12"], S["S12b"], "tense", 1); hit(tpk, 120, True); stab(tpk, "E7", 108, 0.4)
t68 = T("d2", "six") - 0.25
seg(S["S12b"], S["S12c"], "main", 2); hit(t68, 116); stab(t68, "G7", 108); bell(t68 + 0.1, 92, 88)
tsec = T("d2", "security") - 0.2
seg(S["S12c"], S["S13"], "tense", 1); riser(tsec, 0.5); hit(tsec, 122, True); stab(tsec, "E7", 112, 0.5)
t22 = T("d3", "twenty") - 0.25
seg(S["S13"], t22, "lift", 1); hit(t22, 124, True); stab(t22, "Cmaj7", 114, 0.6); flute(t22 + 0.1, 86); seg(t22 + 0.4, S["S14"], "win", 3)
hit(S["S14"] + 0.02, 108); stab(S["S14"] + 0.02, "E7", 104, 0.5); seg(S["S14"] + 0.2, S["S14b"], "tense", 1)
tw = T("t1", "worth") - 0.2
seg(S["S14b"], S["S14c"], "tense", 1); for_ = [n(tw + 0.12 * j, VIB, 84 - 3 * j, 80, 0.2) for j in range(5)]
tay = T("t1", "any") - 0.2
seg(S["S14c"], S["S15"], "tense", 1); hit(tay, 120, True); stab(tay, "E7", 110, 0.5)
t10 = T("t2", "ten") - 0.25
seg(S["S15"], S["S16"], "main", 2); hit(t10, 116); stab(t10, "Fmaj7", 108); bell(t10 + 0.1, 92, 88)
tsh = T("t3", "shrink") - 0.2
seg(S["S16"], S["S16b"], "lift", 1); stab(tsh, "Dm7", 104)
for j in range(5): n(tsh + 0.1 + 0.14 * j, VIB, 88 - 4 * j, 76, 0.25)
seg(S["S16b"], S["S17"], "win", 2)
for nm in ("Earn", "use"): bell(T("t3", nm) - 0.1, 86, 88)
stab(T("t3", "hoard") - 0.15, "E7", 104)
seg(S["S17"], S["S17b"], "main", 1); stab(T("e1", "isn't") - 0.1, "Am7", 104)
hit(S["S17b"] + 0.02, 116, True); stab(S["S17b"] + 0.02, "Cmaj7", 110, 0.5); flute(S["S17b"] + 0.1, 84); seg(S["S17b"] + 0.3, S["S18"], "main", 2)
hit(S["S18"] + 0.02, 108); seg(S["S18"] + 0.1, END - 1.6, "win", 3)
for k in CH["Cmaj7"][1]: n(END - 1.6, EP, k + 12, 70, 2.0); n(END - 1.6, TPT, k + 12, 86, 0.8)
n(END - 1.6, BASS, 24, 104, 1.6); hit(END - 1.6, 104); flute(END - 1.5, 84, 88)


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
