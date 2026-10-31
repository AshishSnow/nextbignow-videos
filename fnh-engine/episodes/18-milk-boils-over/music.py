"""KITCHEN BOSSA NOVA score for FreshNestHub 18 "why does milk boil over?" (GeneralUser GS): a breezy morning-kitchen bossa at 126 bpm
— nylon-string guitar comping the bossa clave, acoustic bass on the 1 and the and-of-2, shaker eighths, rimstick clave, soft hi-hat,
vibraphone colour, a flute melody for the sunny bits, a marimba for the 'bubbles' (the opening = a rising marimba bubble run that climbs
with the foam + a string tremolo swell, then a cymbal splash and a low hit on OVER), tremolo strings for the tension chapter (worse /
skin / lid), a celesta for the mint 'fixes', a tape-stop (varispeed) on 'still came over'. New genre for the channel (bossa nova)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TOVER = T("i1", "over,") - 0.1

GTR, FLT, BS, VIB, STR, MAR, CEL, PNO, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {GTR: 24, FLT: 73, BS: 32, VIB: 11, STR: 44, MAR: 12, CEL: 8, PNO: 0}
VOL = {GTR: 96, FLT: 84, BS: 108, VIB: 74, STR: 80, MAR: 88, CEL: 80, PNO: 70, DR: 74}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 126.0; E8 = BEAT / 2
CH = {"Cmaj7": (48, [60, 64, 67, 71]), "Dm7": (50, [62, 65, 69, 72]), "G7": (43, [59, 62, 65, 67]), "Am7": (45, [60, 64, 67, 69]),
      "Fmaj7": (41, [60, 65, 69, 72]), "E7": (40, [59, 62, 64, 68]), "A7": (45, [61, 64, 67, 69]), "Dm6": (50, [62, 65, 69, 71]),
      "Bbmaj7": (46, [62, 65, 69, 70]), "Em7": (40, [59, 62, 64, 67]), "Gm7": (43, [58, 62, 65, 67]), "C7": (48, [60, 64, 67, 70])}
PROGS = {"sun": ["Cmaj7", "Am7", "Dm7", "G7"], "walk": ["Cmaj7", "Em7", "Fmaj7", "G7"], "minor": ["Dm7", "Gm7", "A7", "Dm6"],
         "tense": ["Dm6", "Bbmaj7", "E7", "A7"], "fix": ["Fmaj7", "G7", "Em7", "Am7"], "end": ["Fmaj7", "G7", "Cmaj7", "Cmaj7"]}
MEL = {"Cmaj7": [76, 79, 83, 79, 76], "Am7": [76, 79, 81, 79, 72], "Dm7": [74, 77, 81, 77, 74], "G7": [74, 77, 79, 83, 79],
       "Fmaj7": [77, 81, 84, 81, 77], "Em7": [76, 79, 83, 79, 76], "E7": [76, 80, 83, 80, 76], "A7": [73, 76, 79, 81, 79],
       "Dm6": [74, 77, 83, 77, 74], "Bbmaj7": [74, 77, 81, 77, 74], "Gm7": [74, 77, 82, 77, 74], "C7": [76, 79, 82, 79, 76]}
CLAVE = (0, 3, 6, 10, 12)        # bossa clave in 8ths over 2 bars (16 eighths): x..x..x...x.x...


def bossa(t0, t1, prog="sun", level=2, half=False, tense=False):
    """level 1: guitar + bass + shaker; 2: + rimstick clave + hat + vibes; 3: + flute melody. tense = tremolo strings pad."""
    bt = BEAT * (2 if half else 1); e8 = bt / 2; bar = 4 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        n(t, BS, root, 104, bt * 1.4); n(t + 1.5 * bt, BS, root + 7, 92, bt * 0.9); n(t + 3 * bt, BS, root, 96, bt * 0.9)
        for e in range(8):                                                   # guitar comping on the bossa pattern, shaker 8ths
            te = t + e * e8
            if te >= t1 - 0.05: break
            n(te, DR, 82, 46 if e % 2 == 0 else 34, 0.08)
            if (e + 8 * (b % 2)) in CLAVE:
                for j, k in enumerate(vo): n(te + 0.006 * j, GTR, k - 12, 78 if e == 0 else 66, e8 * 1.6)
            if level >= 2:
                if (e + 8 * (b % 2)) in CLAVE: n(te, DR, 37, 52, 0.1)
                if e % 2 == 0: n(te, DR, 42, 38, 0.08)
            if e == 0 and not half: n(te, DR, 36, 64, 0.2)
        if level >= 2 and b % 2 == 0:
            for j, k in enumerate(vo[1:]): n(t + 2.5 * bt + 0.008 * j, VIB, k + 12, 54, bt * 1.2)
        if level >= 3 and b % 2 == 1:
            for j, k in enumerate(MEL[ch]):
                tj = t + j * bt * 0.75
                if tj < t1 - 0.05: n(tj, FLT, k, 82 if j in (0, 2) else 70, bt * 0.6)
        if tense:
            for k in vo[:3]: n(t, STR, k - 12, 56, bar * 0.98)
        t += bar; b += 1


def stab(t, chord="Cmaj7", v=104, d=0.5):
    root, vo = CH[chord]
    for j, k in enumerate(vo): n(t + 0.004 * j, GTR, k, v, d); n(t + 0.004 * j, VIB, k + 12, v - 22, d)
    n(t, BS, root, 110, d); n(t, DR, 49, v - 26, 1.2); n(t, DR, 36, v, 0.25)


def hit(t, v=110): n(t, DR, 57, v - 30, 1.4); n(t, DR, 36, v, 0.3); n(t, BS, 36, v, 0.6)


def bells(t, base=84, nn=6, v=80, ch=CEL):
    for i in range(nn): n(t + i * 0.07, ch, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.5)


def bubble_run(t0, dur=1.6, k0=60, nn=14, v=84):
    """rising marimba 'bubble' run (the foam climbing): accelerating notes up a major pentatonic."""
    pent = (0, 2, 4, 7, 9)
    for i in range(nn):
        ti = t0 + dur * (i / nn) ** 1.3
        n(ti, MAR, k0 + pent[i % 5] + 12 * (i // 5), v - 10 + i, 0.18)


def swell(t0, t1, chord="Dm6", v0=30, v1=90):
    """string tremolo swell (tension) from v0 to v1 over t0..t1."""
    root, vo = CH[chord]; nseg = max(2, int((t1 - t0) / 0.25))
    for i in range(nseg):
        ti = t0 + (t1 - t0) * i / nseg; v = v0 + (v1 - v0) * (i / nseg) ** 1.5
        for k in vo[:3]: n(ti, STR, k - 12, v, 0.26)


def fall(t, k0=84, nn=6, d=0.07):
    for i in range(nn): n(t + i * d, FLT, k0 - 2 * i, 80 - 4 * i, d * 1.4)


def splash(t, v=100): n(t, DR, 49, v, 1.5); n(t, DR, 55, v - 10, 1.0)


SLOW = []
# HOOK: marimba bubble run climbing with the foam from frame 0 + a string swell, cymbal splash + low hit on OVER, then the bossa starts
bubble_run(0.0, TOVER - 0.1, 60, 16, 80); swell(0.0, TOVER, "Dm6", 24, 84)
splash(TOVER, 104); hit(TOVER, 112); stab(TOVER, "A7", 104, 0.7)
bubble_run(T("i1", "water") - 0.1, 0.5, 72, 5, 60)
bossa(S["S1"], S["S2"] - 0.05, "sun", 2); n(T("i2", "climbs") - 0.1, MAR, 84, 90, 0.3); bubble_run(T("i2", "climbs") - 0.1, 0.6, 72, 7, 76)
bossa(S["S2"], S["S2b"] - 0.05, "walk", 1); fall(T("i3", "seconds.") - 0.15, 84, 5)
bossa(S["S2b"], S["S3"] - 0.05, "minor", 1, True); bells(T("i3", "works") - 0.1, 84, 5, 70, VIB)
# part 1 water: airy bossa + flute
hit(S["S3"] + 0.05, 96); bossa(S["S3"], S["S4"] - 0.05, "sun", 3); n(T("a1", "pop.") - 0.1, MAR, 96, 96, 0.15); n(T("a1", "Gone.") - 0.1, MAR, 72, 70, 0.3)
bossa(S["S4"], S["S5"] - 0.05, "sun", 2)
# part 2 milk: a little fuller
hit(S["S5"] + 0.05, 96); bossa(S["S5"], S["S5b"] - 0.05, "walk", 2)
bossa(S["S5b"], S["S6"] - 0.05, "walk", 3); stab(T("b1", "everything.") - 0.15, "Fmaj7", 104, 0.6); bells(T("b1", "everything.") - 0.1, 84, 6, 80, VIB)
bossa(S["S6"], S["S6b"] - 0.05, "sun", 1)
for j, w in enumerate(("protein", "fat,", "sugar.")): n(T("b2", w) - 0.1, MAR, (84, 88, 91)[j], 88, 0.4)
bossa(S["S6b"], S["S7"] - 0.05, "sun", 2); bells(T("b2", "edge") - 0.1, 86, 5, 72, VIB)
bossa(S["S7"], S["S7b"] - 0.05, "walk", 2); bubble_run(S["S7"] + 0.1, 1.2, 60, 8, 70); stab(T("b3", "jacket.") - 0.15, "Cmaj7", 100, 0.5)
bossa(S["S7b"], S["S8"] - 0.05, "walk", 2); n(T("b3", "doesn't") - 0.1, MAR, 79, 90, 0.2); n(T("b3", "doesn't") + 0.15, MAR, 79, 70, 0.2)
bossa(S["S8"], S["S8b"] - 0.05, "sun", 3); stab(T("b4", "surfactant.") - 0.15, "Am7", 100, 0.6)
bossa(S["S8b"], S["S9"] - 0.05, "sun", 2); bubble_run(S["S8b"] + 0.3, 1.4, 67, 10, 72); bells(T("b4", "foam.") - 0.15, 84, 6, 76, VIB)
# part 3 foam + skin: minor, then tension
hit(S["S9"] + 0.05, 96); bossa(S["S9"], S["S10"] - 0.05, "minor", 2); bubble_run(T("c1", "pile") - 0.1, 1.6, 55, 18, 80); stab(T("c1", "foam.") - 0.15, "Dm7", 104, 0.6)
bossa(S["S10"], S["S10b"] - 0.05, "tense", 1, True, True); hit(T("c2", "worse.") - 0.1, 100)
bossa(S["S10b"], S["S11"] - 0.05, "tense", 1, True, True); swell(S["S10b"], T("c2", "thicker.") - 0.1, "E7", 30, 80)
bossa(S["S11"], S["S12"] - 0.05, "tense", 1, True, True); n(T("c3", "skin.") - 0.12, STR, 50, 84, 1.4); n(T("c3", "skin.") - 0.12, STR, 56, 70, 1.4)
bossa(S["S12"], S["S12b"] - 0.05, "tense", 1, True, True); stab(T("c4", "lid.") - 0.12, "E7", 102, 0.7)
swell(S["S12b"], T("c4", "over") - 0.1, "A7", 36, 96); bubble_run(S["S12b"], T("c4", "over") - 0.15 - S["S12b"], 55, 18, 84)
splash(T("c4", "over") - 0.1, 108); hit(T("c4", "over") - 0.1, 114); stab(T("c4", "over") - 0.1, "Dm6", 108, 0.9)
bossa(S["S13"], S["S14"] - 0.05, "minor", 2); stab(T("c5", "lid.") - 0.12, "A7", 96, 0.5)
# part 4 proof: sunny again
hit(S["S14"] + 0.05, 96); bossa(S["S14"], S["S14b"] - 0.05, "sun", 2)
bossa(S["S14b"], S["S15"] - 0.05, "walk", 1); n(T("d1", "drop") - 0.1, CEL, 96, 90, 0.4); n(T("d1", "boil") - 0.1, MAR, 72, 80, 0.3)
swell(S["S15"], T("d2", "over.") - 0.15, "G7", 30, 88); bubble_run(S["S15"], T("d2", "over.") - 0.2 - S["S15"], 60, 14, 80)
splash(T("d2", "over.") - 0.15, 100); stab(T("d2", "over.") - 0.15, "Cmaj7", 106, 0.8); bells(T("d2", "different") - 0.1, 84, 6, 78, VIB)
bossa(T("d2", "over.") + 0.3, S["S16"] - 0.05, "sun", 2)
# part 5 the fixes: celesta sparkle
hit(S["S16"] + 0.1, 100); bossa(S["S16"], S["S17"] - 0.05, "fix", 3)
for j, w in enumerate(("America's", "tried", "classics.")): n(T("e1", w) - 0.1, CEL, (84, 86, 88)[j], 78, 0.4)
bossa(S["S17"], S["S17b"] - 0.05, "minor", 2); fall(S["S17"] + 1.2, 81, 5)
bossa(S["S17b"], S["S17c"] - 0.05, "minor", 2); fall(S["S17b"] + 1.0, 81, 5)
bossa(S["S17c"], S["S18"] - 0.05, "tense", 2); hit(T("e2", "still") - 0.1, 104); SLOW.append((T("e2", "still") - 0.1, 0.6))
hit(S["S18"] + 0.02, 98); bossa(S["S18"], S["S18b"] - 0.05, "fix", 3); stab(T("e3", "wide") - 0.12, "Fmaj7", 110, 0.9); bells(T("e3", "wide") - 0.08, 84, 7, 92)
bossa(S["S18b"], S["S19"] - 0.05, "fix", 2); n(T("e3", "four") - 0.1, CEL, 88, 88, 0.4); n(T("e3", "half") - 0.1, CEL, 84, 80, 0.4)
bossa(S["S19"], S["S20"] - 0.05, "walk", 2); bubble_run(S["S19"] + 0.2, 1.6, 55, 10, 76); n(T("e4", "pop,") - 0.1, MAR, 96, 96, 0.15)
bossa(S["S20"], S["S20b"] - 0.05, "fix", 2); n(T("e5", "moderate") - 0.1, CEL, 86, 84, 0.4)
bossa(S["S20b"], S["S21"] - 0.05, "fix", 2); bells(T("e5", "stir") - 0.1, 86, 5, 80); bells(T("e5", "skin") - 0.1, 88, 5, 74)
bossa(S["S21"], S["S22"] - 0.05, "minor", 1); fall(T("e6", "phone.") - 0.1, 84, 6)
bossa(S["S22"], S["S23"] - 0.05, "walk", 2); bubble_run(S["S22"] + 0.3, 1.4, 60, 10, 76); stab(T("f1", "starch.") - 0.15, "Dm7", 100, 0.6)
bossa(S["S23"], S["S24"] - 0.05, "sun", 3)
for j, w in enumerate(("proteins", "skin", "foam")): n(T("g1", w) - 0.15, CEL, (84, 86, 88)[j], 88, 0.5)
for j, w in enumerate(("Wide", "lower", "stir.")): n(T("g1", w) - 0.1, VIB, (88, 91, 95)[j], 90, 0.5)
bossa(S["S24"], END - 1.8, "end", 2)
stab(END - 1.8, "Cmaj7", 112, 1.8); hit(END - 1.8, 112); bells(END - 1.75, 84, 7, 92); n(END - 1.8, FLT, 84, 86, 1.6)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 50), (FLT, 76), (BS, 64), (VIB, 86), (STR, 60), (MAR, 40), (CEL, 90), (PNO, 56)): syn.control_change(ch, 10, pan)
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
    nb = int(b * SR); tail = int(0.3 * SR)
    if nb < len(part): part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]


def ritard(x, t0, dur, floor=0.55):
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = 1 - (1 - floor) * np.linspace(0, 1, L) ** 1.4
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.4, L)[:, None]
    x[i0:i0 + L] = seg


for t0, d in SLOW: ritard(mus, t0, d)
mus = signal.sosfilt(signal.butter(2, 9500, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
