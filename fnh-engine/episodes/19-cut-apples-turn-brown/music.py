"""APPLE-ORCHARD BLUEGRASS score for FreshNestHub 19 "why do cut apples turn brown?" (GeneralUser GS): a sunny porch bluegrass at 138 bpm —
banjo forward rolls (the 'PPO machine' motif = a 4-note banjo lick), steel-string guitar boom-chick, upright bass walking root-fifth,
fiddle for the sunny bits and long tremolo notes for the tension, harmonica for the fixes, hammered dulcimer for the 'on purpose' chapter,
brushed snare + shaker. Opening idea: a lone banjo plucking a slow roll while a rimstick 'clock' ticks as the apple browns, a fiddle note
rising to the TAN reveal, then a big strum + crash and the boom-chick train leaves. The GUESS beat drops everything to one held fiddle
note + the clock tick (comic pause), the band crashes back on NOPE. New genre for the channel (bluegrass / country-folk)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TTAN = T("i1", "tan?") - 0.15; TCUT = T("b1", "cut") - 0.08

BJO, GTR, BS, FID, HRM, DUL, PNO, STR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {BJO: 105, GTR: 25, BS: 32, FID: 110, HRM: 22, DUL: 15, PNO: 0, STR: 44}
VOL = {BJO: 92, GTR: 86, BS: 108, FID: 80, HRM: 82, DUL: 84, PNO: 70, STR: 78, DR: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 138.0; E8 = BEAT / 2
CH = {"G": (43, [55, 59, 62, 67]), "C": (48, [60, 64, 67, 72]), "D": (50, [57, 62, 66, 69]), "Em": (40, [55, 59, 64, 67]),
      "Am": (45, [57, 60, 64, 69]), "D7": (50, [57, 60, 62, 66]), "Bm": (47, [59, 62, 66, 71]), "F": (41, [57, 60, 65, 69]),
      "Gm": (43, [55, 58, 62, 67]), "Cm": (48, [60, 63, 67, 72]), "Eb": (39, [58, 63, 67, 70]), "A7": (45, [57, 61, 64, 67])}
PROGS = {"porch": ["G", "C", "G", "D"], "walk": ["G", "Em", "C", "D7"], "minor": ["Em", "C", "G", "D"], "dark": ["Em", "Am", "Bm", "D"],
         "sepia": ["Gm", "Eb", "Cm", "D7"], "fix": ["C", "G", "D", "G"], "end": ["C", "D", "G", "G"]}
MEL = {"G": [79, 81, 83, 86, 83], "C": [79, 84, 88, 84, 79], "D": [81, 86, 90, 86, 81], "Em": [79, 83, 88, 83, 79], "Am": [81, 84, 88, 84, 81],
       "D7": [81, 84, 86, 90, 86], "Bm": [83, 86, 90, 86, 83], "F": [81, 84, 89, 84, 81], "Gm": [79, 82, 86, 82, 79], "Cm": [79, 84, 87, 84, 79],
       "Eb": [82, 87, 91, 87, 82], "A7": [81, 85, 88, 85, 81]}


def roll(t0, chord, bars=1, v=78, fast=True):
    """banjo forward-backward roll on the chord tones (8 eighth notes per bar)."""
    root, vo = CH[chord]; pat = [0, 1, 2, 3, 2, 1, 0, 2]
    for e in range(8 * bars):
        te = t0 + e * E8
        n(te, BJO, vo[pat[e % 8]] + 12, v - 8 + 10 * (e % 2 == 0), E8 * 1.3)


def bluegrass(t0, t1, prog="porch", level=2, tense=False, half=False):
    """level 1: guitar boom-chick + bass; 2: + banjo rolls + brushes + shaker; 3: + fiddle melody. tense = string tremolo pad under it."""
    bt = BEAT * (2 if half else 1); bar = 4 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        n(t, BS, root, 106, bt * 0.9); n(t + 2 * bt, BS, root + 7, 98, bt * 0.9)                      # root - fifth
        if b % 2 == 1: n(t + 3 * bt, BS, root + 5, 90, bt * 0.5); n(t + 3.5 * bt, BS, root + 7, 86, bt * 0.5)   # walk-up
        for q in (1, 3):                                                                                # chick on 2 and 4
            for j, k in enumerate(vo): n(t + q * bt + 0.005 * j, GTR, k, 72 if q == 1 else 66, bt * 0.45)
        n(t, GTR, root + 12, 70, bt * 0.5); n(t + 2 * bt, GTR, root + 19, 66, bt * 0.5)             # boom
        if level >= 2:
            roll(t, ch, 1, 76)
            for e in range(8):
                te = t + e * bt / 2
                if te < t1 - 0.05: n(te, DR, 82, 44 if e % 2 == 0 else 32, 0.08)
            n(t + bt, DR, 38, 46, 0.15); n(t + 3 * bt, DR, 38, 50, 0.15); n(t, DR, 36, 54, 0.2); n(t + 2 * bt, DR, 36, 48, 0.2)
        if level >= 3 and b % 2 == 0:
            for j, k in enumerate(MEL[ch]):
                tj = t + j * bt * 0.75
                if tj < t1 - 0.05: n(tj, FID, k, 84 if j in (0, 2) else 72, bt * 0.7)
        if tense:
            for k in vo[:3]: n(t, STR, k - 12, 52, bar * 0.98)
        t += bar; b += 1


def stab(t, chord="G", v=108, d=0.6):
    root, vo = CH[chord]
    for j, k in enumerate(vo): n(t + 0.004 * j, GTR, k, v, d); n(t + 0.004 * j, BJO, k + 12, v - 14, d)
    n(t, BS, root, 112, d); n(t, DR, 49, v - 28, 1.2); n(t, DR, 36, v, 0.25)


def hit(t, v=110): n(t, DR, 57, v - 30, 1.4); n(t, DR, 36, v, 0.3); n(t, BS, 31, v, 0.6)


def lick(t0, k0=79, v=90, ch=BJO):
    """the PPO machine motif: a 4-note banjo lick (up a 5th, back, up a 6th) — reused on every PPO moment."""
    for i, (dk, dd) in enumerate(((0, 0), (7, 0.14), (5, 0.28), (9, 0.42))): n(t0 + dd, ch, k0 + dk, v - 4 * i, 0.3)


def fiddle_long(t0, dur, k=86, v0=40, v1=92):
    """a fiddle note that swells (tremolo re-triggers)."""
    nseg = max(2, int(dur / 0.22))
    for i in range(nseg):
        v = v0 + (v1 - v0) * (i / nseg) ** 1.4; n(t0 + i * dur / nseg, FID, k, v, 0.26)


def bells(t, base=84, nn=6, v=80, ch=DUL):
    for i in range(nn): n(t + i * 0.07, ch, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.5)


def fall(t, k0=84, nn=6, d=0.07, ch=HRM):
    for i in range(nn): n(t + i * d, ch, k0 - 2 * i, 84 - 4 * i, d * 1.4)


def tick(t0, t1, gap=0.5, v=48):
    t = t0
    while t < t1: n(t, DR, 37, v, 0.1); t += gap


def harm_mel(t0, t1, chord_list, v=84):
    """harmonica melody over the fixes."""
    t = t0; i = 0
    while t < t1 - 0.3:
        ch = chord_list[i % len(chord_list)]
        for j, k in enumerate(MEL[ch][:4]): n(t + j * BEAT * 0.5, HRM, k - 12, v - 6 * (j % 2), BEAT * 0.5)
        t += 2 * BEAT; i += 1


SLOW = []
# HOOK: lone banjo slow roll + rimstick clock as the apple browns; a fiddle note rises to TAN; big strum + crash on TAN
for e in range(int((TTAN - 0.2) / (E8 * 2))):
    te = e * E8 * 2; n(te, BJO, [67, 71, 74, 79, 74, 71][e % 6], 66 + 4 * (e % 2), E8 * 2.2)
tick(0.0, TTAN - 0.1, 0.5, 46); fiddle_long(max(0.0, TTAN - 1.6), 1.5, 86, 36, 92)
stab(TTAN, "G", 112, 0.8); hit(TTAN, 114); bells(TTAN + 0.05, 91, 6, 86, DUL)
bluegrass(S["S0b"], S["S1"] - 0.05, "porch", 2); n(T("i2", "melanin,") - 0.15, FID, 83, 90, 0.5)
bluegrass(S["S1"], S["S2"] - 0.05, "walk", 3); bells(T("i3", "dip") - 0.1, 84, 5, 76)
# part 1 inside the apple: lighter
hit(S["S2"] + 0.05, 96); bluegrass(S["S2"], S["S2b"] - 0.05, "porch", 2); n(T("a1", "millions") - 0.15, FID, 91, 86, 0.6)
bluegrass(S["S2b"], S["S3"] - 0.05, "walk", 1)
bluegrass(S["S3"], S["S3b"] - 0.05, "walk", 1); n(T("a2", "apart.") - 0.12, GTR, 55, 90, 0.4)
bluegrass(S["S3b"], S["S3c"] - 0.05, "walk", 2); lick(T("a2", "PPO:") - 0.12, 79, 96)
bluegrass(S["S3c"], S["S4"] - 0.05, "porch", 2); lick(T("a2", "job.") - 0.12, 84, 90)
bluegrass(S["S4"], S["S4b"] - 0.05, "walk", 1); stab(T("a3", "polyphenols.") - 0.15, "C", 96, 0.5)
bluegrass(S["S4b"], S["S5"] - 0.05, "walk", 2); n(T("a3", "never") - 0.12, FID, 86, 84, 0.5)
# the cut: stop, hit, tremolo
stab(TCUT, "Em", 112, 0.9); hit(TCUT, 116); SLOW.append((T("b1", "smashes") - 0.12, 0.5))
bluegrass(TCUT + 0.4, S["S5b"] - 0.05, "minor", 2, True)
bluegrass(S["S5b"], S["S6"] - 0.05, "minor", 2, True); lick(T("b1", "meets") - 0.12, 76, 92)
bluegrass(S["S6"], S["S7"] - 0.05, "minor", 1, True); fiddle_long(S["S6"], max(0.6, T("b2", "Oxygen.") - 0.2 - S["S6"]), 88, 40, 90); stab(T("b2", "Oxygen.") - 0.15, "D", 100, 0.6)
bluegrass(S["S7"], S["S7b"] - 0.05, "minor", 2); lick(T("b3", "grabs") - 0.1, 79, 94); stab(T("b3", "mashes") - 0.12, "Em", 104, 0.6)
bluegrass(S["S7b"], S["S8"] - 0.05, "walk", 1); fall(T("b3", "colourless.") - 0.15, 84, 5, 0.08, DUL)
bluegrass(S["S8"], S["S8b"] - 0.05, "dark", 1, True); fiddle_long(S["S8"], max(0.6, S["S8b"] - S["S8"]), 83, 36, 84)
stab(T("b4", "brown.") - 0.12, "Em", 108, 0.8); hit(T("b4", "brown.") - 0.12, 110)
bluegrass(T("b4", "brown.") + 0.3, S["S9"] - 0.05, "sepia", 1, True); n(T("b4", "melanin.") - 0.15, STR, 40, 88, 1.6); n(T("b4", "melanin.") - 0.15, STR, 47, 72, 1.6)
# the tan: sunny again
hit(S["S9"] + 0.05, 96); bluegrass(S["S9"], S["S9b"] - 0.05, "porch", 3)
bluegrass(S["S9b"], S["S10"] - 0.05, "porch", 2); bells(T("c1", "faster.") - 0.12, 84, 6, 80)
bluegrass(S["S10"], S["S10b"] - 0.05, "walk", 1); n(S["S10"] + 0.3, FID, 86, 70, 0.4); n(S["S10"] + 0.6, FID, 88, 74, 0.6)
bluegrass(S["S10b"], S["S11"] - 0.05, "minor", 2); stab(T("c2", "defence") - 0.12, "Em", 100, 0.6)
# the guess: everything drops to one fiddle note + the clock tick; NOPE = band back
fiddle_long(S["S11"], max(0.8, S["S11b"] - 0.1 - S["S11"]), 81, 46, 80); tick(S["S11"] + 0.2, S["S11b"] - 0.1, 0.5, 50)
stab(S["S11b"] + 0.02, "G", 112, 0.8); hit(S["S11b"] + 0.02, 112); bells(T("c4", "harmless.") - 0.1, 91, 6, 86)
bluegrass(S["S11b"] + 0.3, S["S11c"] - 0.05, "porch", 3)
bluegrass(S["S11c"], S["S12"] - 0.05, "walk", 2); fall(T("c4", "sad.") - 0.12, 81, 5, 0.09, FID)
# part 2 the fixes: harmonica
hit(S["S12"] + 0.1, 100); bluegrass(S["S12"], S["S13"] - 0.05, "fix", 2)
for j, w in enumerate(("oxygen", "slows", "switches")): n(T("d1", w) - 0.12, HRM, (72, 76, 79)[j], 86, 0.4)
bluegrass(S["S13"], S["S13b"] - 0.05, "fix", 2); harm_mel(S["S13"] + 0.2, S["S13b"] - 0.3, ["C", "G"], 80); lick(T("d2", "sluggish,") - 0.12, 72, 80, DUL)
bluegrass(S["S13b"], S["S14"] - 0.05, "fix", 2); bells(T("d2", "vitamin") - 0.1, 88, 5, 80); n(T("d2", "done.") - 0.1, HRM, 79, 88, 0.5)
bluegrass(S["S14"], S["S14b"] - 0.05, "porch", 2); harm_mel(S["S14"] + 0.3, S["S14b"] - 0.3, ["G", "C"], 78); stab(T("d3", "dunk") - 0.1, "G", 98, 0.5)
bluegrass(S["S14b"], S["S15"] - 0.05, "fix", 1); bells(T("d3", "coat") - 0.1, 84, 5, 76)
bluegrass(S["S15"], S["S15b"] - 0.05, "minor", 1, True, True); fiddle_long(S["S15"], 1.4, 76, 36, 70)
stab(T("d4", "Heat") - 0.1, "D", 100, 0.6); bluegrass(S["S15b"], S["S16"] - 0.05, "fix", 2); lick(T("d4", "off") - 0.1, 67, 84, DUL)
# part 3 on purpose: dulcimer + minor
bluegrass(S["S16"], S["S16b"] - 0.05, "dark", 1, True); fiddle_long(S["S16"], max(0.6, T("e1", "purpose.") - 0.2 - S["S16"]), 83, 36, 86)
stab(T("e1", "purpose.") - 0.15, "Em", 104, 0.7); hit(T("e1", "purpose.") - 0.15, 104)
bluegrass(S["S16b"], S["S16c"] - 0.05, "sepia", 2); bells(S["S16b"] + 0.1, 79, 6, 84); lick(T("e2", "reaction,") - 0.12, 74, 86)
bluegrass(S["S16c"], S["S17"] - 0.05, "sepia", 2); bells(S["S16c"] + 0.05, 82, 5, 80); bells(T("e2", "cocoa") - 0.1, 86, 5, 80)
bluegrass(S["S17"], S["S17b"] - 0.05, "walk", 2)
for j, w in enumerate(("Avocados,", "bananas,", "potatoes:")): n(T("e3", w) - 0.12, DUL, (84, 86, 88)[j], 86, 0.4)
bluegrass(S["S17b"], S["S18"] - 0.05, "minor", 2); stab(T("e3", "Melanin.") - 0.15, "Em", 104, 0.7)
# the arctic apple: cool, sparkly
hit(S["S18"] + 0.05, 96); bluegrass(S["S18"], S["S18b"] - 0.05, "porch", 2); bells(T("f1", "Arctic") - 0.12, 91, 7, 86)
bluegrass(S["S18b"], S["S18c"] - 0.05, "walk", 2); n(T("f1", "switched") - 0.1, GTR, 55, 88, 0.4); bells(T("f1", "white") - 0.12, 88, 5, 82)
bluegrass(S["S18c"], S["S19"] - 0.05, "walk", 2); stab(T("f2", "fifteen.") - 0.15, "C", 96, 0.5); fall(T("f2", "blushes.") - 0.15, 84, 5, 0.08, FID)
# recap + end
bluegrass(S["S19"], S["S20"] - 0.05, "porch", 3)
for j, w in enumerate(("cut", "enzyme", "melanin.")): n(T("g1", w) - 0.15, DUL, (84, 86, 88)[j], 88, 0.5)
for j, w in enumerate(("Lemon,", "honey", "cold", "heat")): n(T("g1", w) - 0.1, HRM, (76, 79, 81, 84)[j], 86, 0.4)
bluegrass(S["S20"], END - 1.8, "end", 2)
stab(END - 1.8, "G", 112, 1.8); hit(END - 1.8, 112); bells(END - 1.75, 91, 7, 92); n(END - 1.8, FID, 91, 86, 1.6); roll(END - 1.7, "G", 1, 84)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((BJO, 46), (GTR, 76), (BS, 64), (FID, 84), (HRM, 40), (DUL, 90), (PNO, 56), (STR, 60)): syn.control_change(ch, 10, pan)
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
