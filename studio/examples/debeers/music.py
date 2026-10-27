"""Film-noir / heist-jazz score for "De Beers: how a rock became forever" (GeneralUser GS): swung walking upright bass, brushed ride,
muted-trumpet answers, vibraphone + celesta glints for every diamond sparkle, smoky piano comping, string swells on reveals; minor key."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

PNO, BASS, VIB, TPT, CEL, STR, SUB, SAX, DR = 0, 1, 3, 4, 5, 7, 6, 2, 9
PROG = {PNO: 0, BASS: 32, VIB: 11, TPT: 59, CEL: 8, STR: 49, SUB: 38, SAX: 66}
VOL = {PNO: 70, BASS: 110, VIB: 74, TPT: 80, CEL: 72, STR: 52, SUB: 100, SAX: 62, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"Cm6": (36, [51, 55, 57, 60]), "Fm7": (41, [51, 56, 60, 63]), "G7b9": (43, [50, 53, 56, 59]), "Abmaj7": (44, [51, 55, 56, 60]),
      "Dm7b5": (38, [50, 53, 56, 60]), "Ebmaj7": (39, [50, 55, 58, 62]), "Bb7": (46, [50, 53, 56, 58]), "Cmaj7": (36, [52, 55, 59, 60])}
PROGS = {"main": ["Cm6", "Fm7", "Dm7b5", "G7b9"], "lift": ["Ebmaj7", "Abmaj7", "Fm7", "Bb7"], "tense": ["Cm6", "G7b9", "Cm6", "G7b9"],
         "win": ["Abmaj7", "Bb7", "Ebmaj7", "Cmaj7"]}
BPM = 108
MEL = {"main": [67, 70, 72, 75, 74, 72, 70, 67], "lift": [70, 74, 75, 79, 77, 75, 74, 70], "win": [75, 79, 82, 84, 82, 79, 75, 74],
       "tense": [67, 68, 67, 66, 67, 71, 72, 74]}


def groove(t0, t1, prog="main", level=2, bpm=BPM):
    """swing: walking bass on every beat, brushed ride with swung 'and', soft kick 1/3, piano comps on 2 and the 'and' of 3;
    string pad at level >= 2; vibraphone line at level 3"""
    beat = 60 / bpm; bar = 4 * beat; sw = beat * 0.66; b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[PROGS[prog][b % 4]]
        walk = [root - 12, root - 12 + (3 if "m" in PROGS[prog][b % 4] else 4), root - 12 + 7, root - 12 + 8]
        for i in range(4):
            tq = t + i * beat
            if tq >= t1 - 0.03: break
            n(tq, BASS, walk[i] if root >= 36 else walk[i] + 12, 100 - 6 * (i % 2), beat * 0.9)
            if level >= 1:
                n(tq, DR, 51, 52 + 6 * (i % 2 == 0), 0.2)
                if i % 2 == 1: n(tq + sw, DR, 51, 40, 0.1); n(tq, DR, 44, 46, 0.05)
            if i in (0, 2) and level >= 2: n(tq, DR, 36, 58, 0.1)
            if level >= 1 and i == 1:
                for k in tri: n(tq, PNO, k + 12, 50 + 4 * level, beat * 0.4)
            if level >= 1 and i == 2:
                for k in tri: n(tq + sw, PNO, k + 12, 44 + 4 * level, beat * 0.3)
        if level >= 2:
            for k in tri: n(t, STR, k, 36, min(bar, t1 - t) * 0.98)
        if level >= 3:
            mel = MEL.get(prog, MEL["main"])
            for j, k in enumerate(mel):
                tq = t + (j // 2) * beat + (sw if j % 2 else 0)
                if tq < t1 - 0.05: n(tq, VIB, k, 72 - 6 * (j % 2), beat * 0.5)
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 30, 1.6); n(t, DR, 36, v, 0.2); n(t, DR, 38, v - 26, 0.2)
    if big: n(t, SUB, 31, 108, 0.8)


def stab(t, chord="Cm6", v=104, d=0.3):
    root, tri = CH[chord]
    for k in tri: n(t, TPT, k + 12, v - 22, d); n(t, PNO, k, v - 34, d)
    n(t, BASS, root - 12 if root >= 36 else root, 104, d)


def glint(t, base=88, v=88):   # celesta + vibraphone sparkle, for diamonds
    for i, k in enumerate((base, base + 4, base + 7, base + 11, base + 14)): n(t + i * 0.055, CEL, k, v - 4 * i, 0.4); n(t + i * 0.055, VIB, k - 12, v - 20, 0.3)


def swell(t, chord="Cm6", d=1.2, v=70):
    root, tri = CH[chord]
    for j in range(6):
        for k in tri: n(t + j * d / 6, STR, k + 12, int(v * (0.3 + 0.7 * j / 5)), d / 6 + 0.05)


def sax(t, notes, v=80, d=0.28):
    for i, k in enumerate(notes): n(t + i * d, SAX, k, v, d * 0.95)


def riser(t_end, dur):
    m = int(dur / 0.05)
    for j in range(m): n(t_end - dur + j * 0.05, STR, 52 + int(24 * j / m), 30 + int(60 * (j / m)), 0.06)
    for j in range(int(dur / 0.1)): n(t_end - dur + j * 0.1, DR, 38, 30 + int(60 * j / (dur / 0.1)), 0.05)


def drumroll(t0, dur):
    for j in range(int(dur / 0.06)): n(t0 + j * 0.06, DR, 38, 36 + int(56 * j * 0.06 / dur), 0.04)


def seg(a, b, prog, lvl): groove(a, b - 0.05, prog, lvl)


# ---- cues (every reveal gets a hit / stab / glint) ----
tt = T("i1", "two") - 0.2
seg(0.0, S["S1"], "main", 1); n(0.0, DR, 49, 70, 1.6); glint(0.05, 88, 84); stab(tt, "G7b9", 104, 0.5); hit(tt, 108)
tr = T("i2", "rare") - 0.15
seg(S["S1"], S["S2"], "main", 2); hit(tr, 114, True); stab(tr, "Cm6", 108, 0.5)
seg(S["S2"], S["S3"], "lift", 2)
for i in range(3): n(S["S2"] + 0.25 + 0.18 * i, VIB, 79 + 3 * i, 84, 0.3)
hit(S["S3"] + 0.02, 108); stab(S["S3"] + 0.02, "Fm7", 100); seg(S["S3"] + 0.2, S["S4"], "tense", 1)
tn = T("a2", "ninety") - 0.25
seg(S["S4"], S["S5"], "main", 2); hit(tn, 116, True); stab(tn, "Abmaj7", 108, 0.5); glint(tn + 0.9, 91)
tl = T("a3", "locked") - 0.1; tsl = T("a3", "slowly") - 0.25
seg(S["S5"], S["S5b"], "tense", 1); hit(tl, 112); stab(tl, "G7b9", 104, 0.4)
for j in range(4): n(tsl + 0.35 * j, CEL, 91 - 2 * j, 80, 0.4)
seg(S["S5b"], S["S6"], "tense", 1); swell(S["S5b"], "Dm7b5", 1.2, 60)
t22 = T("a4", "twenty") - 0.25
seg(S["S6"], S["S6b"], "main", 2); hit(t22, 112); stab(t22, "Cm6", 104)
trr = T("a4", "rare") - 0.15
seg(S["S6b"], S["S7"], "tense", 1); hit(trr, 122, True); stab(trr, "G7b9", 112, 0.6); sax(trr + 0.3, [67, 70, 66, 67], 76)
hit(S["S7"] + 0.02, 108); seg(S["S7"] + 0.1, S["S8"], "lift", 3); swell(S["S7"] + 0.2, "Ebmaj7", 1.5, 66)
t10 = T("b2", "ten") - 0.2
seg(S["S8"], S["S9"], "main", 1); stab(t10, "Fm7", 100); glint(t10 + 0.05, 86, 76)
seg(S["S9"], S["S9b"], "lift", 2); for_ = [n(S["S9"] + 0.2 + 0.25 * i, VIB, 77 + 2 * i, 76, 0.3) for i in range(3)]
t4 = T("b3", "four") - 0.2
seg(S["S9b"], t4, "main", 1); drumroll(t4 - 0.6, 0.6); hit(t4, 112); stab(t4, "G7b9", 104, 0.5)
# S10: the four words — music drops to a held string chord + celesta, then a big lift
swell(S["S10"], "Abmaj7", 1.6, 62); glint(T("b4", "forever") - 0.1, 86, 90)
hit(S["S11"] + 0.02, 112, True); stab(S["S11"] + 0.02, "Ebmaj7", 108, 0.6); seg(S["S11"] + 0.2, S["S11b"], "win", 3)
tc = T("b5", "century") - 0.7; glint(tc + 0.1, 91, 90)
t8 = T("b5", "eight") - 0.25
seg(S["S11b"], S["S12"], "lift", 2); hit(t8, 114); stab(t8, "Abmaj7", 106); glint(t8 + 0.1, 88, 80)
# re-hook: drumroll under the gold folder, then the stab on 'sneakiest'
ts = T("c1", "sneakiest") - 0.2
drumroll(S["S12"] + 0.1, max(0.3, ts - S["S12"] - 0.15)); hit(ts, 122, True); stab(ts, "G7b9", 112, 0.6)
seg(S["S12b"], S["S13"], "tense", 1); sax(S["S12b"] + 0.2, [72, 70, 67, 66], 72)
seg(S["S13"], S["S13b"], "main", 2)
seg(S["S13b"], S["S14"], "lift", 2); glint(T("c2", "forever") - 0.2, 88, 84)
tsel = T("c3", "seller") - 0.2
seg(S["S14"], tsel, "tense", 1); hit(tsel, 122, True); stab(tsel, "Cm6", 112, 0.6); sax(tsel + 0.4, [60, 63, 62, 59], 70)
# the trick is breaking: everything stops, a glassy crack
tb = T("d1", "breaking") - 0.2
riser(tb, 0.8); hit(tb, 124, True); stab(tb, "G7b9", 114, 0.7)
for j in range(6): n(tb + 0.04 * j, CEL, 100 - 3 * j, 90, 0.15)
seg(S["S16"], S["S16b"], "lift", 1); glint(S["S16"] + 0.8, 84, 80); glint(S["S16"] + 1.6, 88, 80)
seg(S["S16b"], S["S17"], "lift", 2); stab(T("d2", "sparkle") - 0.2, "Ebmaj7", 100)
t96 = T("d3", "ninety") - 0.25
seg(S["S17"], S["S18"], "tense", 1)
for j in range(8): n(S["S17"] + 0.2 + 0.2 * j, VIB, 84 - 2 * j, 74, 0.25)
hit(t96, 120, True); stab(t96, "Dm7b5", 110, 0.5)
t800 = T("d4", "eight") - 0.25
seg(S["S18"], S["S18b"], "main", 2); stab(t800, "Fm7", 104); glint(t800 + 0.1, 88, 80)
tsh = T("d4", "shut") - 0.2
seg(S["S18b"], tsh, "tense", 1); hit(tsh + 0.2, 122, True); stab(tsh + 0.2, "G7b9", 112, 0.5)
th = T("d5", "half") - 0.25
seg(S["S19"], S["S19b"], "tense", 1); hit(th, 118, True); stab(th, "Cm6", 108, 0.5); sax(th + 0.5, [55, 58, 54, 55], 70)
tsell = T("d5", "selling") - 0.45
seg(S["S19b"], S["S20"], "main", 2); hit(tsell, 116); stab(tsell, "Abmaj7", 106)
hit(S["S20"] + 0.02, 108); stab(S["S20"] + 0.02, "Ebmaj7", 102, 0.5); seg(S["S20"] + 0.2, S["S20b"], "lift", 2)
seg(S["S20b"], S["S21"], "tense", 1); hit(S["S20b"] + 0.15, 116, True); stab(S["S20b"] + 0.15, "G7b9", 108, 0.5)
seg(S["S21"], S["S22"], "main", 2); glint(T("t2", "What") - 0.2, 86, 78)
seg(S["S22"], S["S23"], "main", 1); glint(S["S22"] + 0.1, 88, 84)
tst = T("e1", "story") - 0.2; hit(tst, 118, True); stab(tst, "Cm6", 110, 0.6); swell(tst, "Cm6", 1.0, 70)
hit(S["S23"] + 0.02, 108); seg(S["S23"] + 0.1, END - 1.6, "win", 3)
for k in CH["Cmaj7"][1]: n(END - 1.6, STR, k + 12, 70, 2.0); n(END - 1.6, TPT, k + 12, 82, 0.8)
n(END - 1.6, BASS, 24, 104, 1.6); hit(END - 1.6, 104); glint(END - 1.5, 91, 88)


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
