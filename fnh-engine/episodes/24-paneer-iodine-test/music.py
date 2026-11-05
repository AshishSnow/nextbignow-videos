"""70s CRIME-FILM FUNK score for FreshNestHub 24 "does the iodine test catch fake paneer?" (GeneralUser GS): a guard, a disguise, a suspect in a moustache: think an old Bollywood cop-show chase. D minor at 108 bpm: fingered bass, wah-ish clean guitar, Hammond organ, flute hook (original), brass stabs, bongos + congas, vibes for the chemistry. New genre for the channel.
FOLLOWS THE STORY: the opener is NO band, only a heartbeat + a held organ while the drop falls in slow motion (speed ramp); the band crashes in when it lands. Sneaky bass + bongos for the guard; a held organ + clock for the guess; brass down-glide on 'Brown'; full chase at the three tips; final hit + audio logo."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}; TP = T("i1", "pass") - 0.04
GTR, BAS, ORG, FLU, BRS, VIB, STR, TPT, TIM, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {GTR: 28, BAS: 33, ORG: 17, FLU: 73, BRS: 61, VIB: 11, STR: 48, TPT: 59, TIM: 47}
VOL = {GTR: 84, BAS: 108, ORG: 74, FLU: 84, BRS: 86, VIB: 90, STR: 66, TPT: 86, TIM: 92, DR: 82}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 108
CH = {"Dm": (38, [62, 65, 69]), "Gm": (43, [62, 67, 70]), "A": (45, [61, 64, 69]), "Bb": (46, [62, 65, 70]), "F": (41, [60, 65, 69]), "C": (36, [60, 64, 67])}
PROGS = {"main": ["Dm", "Dm", "Gm", "A"], "bright": ["F", "C", "Bb", "C"], "tense": ["Dm", "Bb", "Gm", "A"]}
BASSLINE = [(0, 0), (0.75, 0), (1.5, 7), (2, 10), (2.5, 12), (3, 7), (3.5, 10)]


def funk(t0, t1, prog="main", level=2):
    """1: bass + hat + bongos (thin, for explanations). 2: + kick/snare + guitar chank + organ pad. 3: + brass stabs + flute answer."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for off, st in BASSLINE:
            if t + off * BEAT < t1: n(t + off * BEAT, BAS, root + st, 100 if off == 0 else 84, BEAT * 0.42)
        for q in range(8):
            tq = t + q * BEAT / 2
            if tq >= t1 - 0.03: break
            n(tq, DR, 42, 56 if q % 2 else 70, 0.05)
            if level == 1 and q % 4 == 3: n(tq, DR, 61, 58, 0.08)
            if level == 1 and q % 4 == 1: n(tq, DR, 60, 50, 0.08)
        if level >= 2:
            for off in (0, 1.5, 2.5): n(t + off * BEAT, DR, 36, 96, 0.1)
            for off in (1, 3): n(t + off * BEAT, DR, 38, 90, 0.1)
            for off in (0.5, 1.75, 2.25, 3.5):
                for k in vo: n(t + off * BEAT, GTR, k + 12, 70, BEAT * 0.14)
            for k in vo: n(t, ORG, k, 54, BEAT * 3.6)
            for off in (1.25, 3.25): n(t + off * BEAT, DR, 63, 60, 0.08)
        if level >= 3:
            for off in (1.5, 3.5):
                for k in vo: n(t + off * BEAT, BRS, k + 12, 92, BEAT * 0.32)
        t += 4 * BEAT; b += 1


HOOK = [(0, 74), (0.5, 77), (1, 81), (1.75, 82), (2, 81), (2.5, 77), (3, 74), (3.5, 73), (4, 74)]


def hook(t0, v=88, ch=FLU, tr=0, gap=BEAT):
    for off, k in HOOK: n(t0 + off * gap, ch, k + tr, v, gap * 0.45)


def hit(t, chord="Dm", v=112, d=0.45):
    root, vo = CH[chord]
    n(t, BAS, root, v, d); n(t, TIM, root + 12, v, 0.35); n(t, DR, 49, v - 22, 0.3); n(t, DR, 36, v, 0.1)
    for k in vo: n(t, BRS, k + 12, v - 6, d)


def vibes(t, base=74, nn=5, v=80, gap=0.1, steps=(0, 3, 7, 10, 12, 15, 19)):
    for j in range(nn): n(t + j * gap, VIB, base + steps[j % 7], v, 0.3)


def downglide(t, k=74, v=96):
    """the sad trombone-ish muted-trumpet fall, for 'it passes'."""
    for j, dk in enumerate((0, -1, -2, -3, -5)): n(t + j * 0.14, TPT, k + dk, v, 0.16 if j < 4 else 0.5)


def sneak(t0, t1, v=88):
    """the guard's corridor: walking bass + staccato strings + a bongo."""
    t = t0; b = 0; line = [38, 41, 43, 44, 45, 44, 43, 41]
    while t < t1 - 0.05:
        n(t, BAS, line[b % 8], v, BEAT * 0.4)
        n(t + BEAT / 2, DR, 60 if b % 2 else 61, 54, 0.06); n(t, DR, 42, 50, 0.05)
        if b % 4 == 2: n(t, STR, 62 + line[b % 8] % 12, 62, BEAT * 0.25)
        t += BEAT; b += 1


SLOW = []
# ---- hook: heartbeat under the slow-motion drop (speed ramp): no band; band crashes in on landing
for j in range(int(TP / (BEAT * 1.5)) + 1):
    tb_ = j * BEAT * 1.5
    if tb_ < TP - 0.1: n(tb_, DR, 36, 86, 0.1); n(tb_ + 0.22, DR, 36, 64, 0.1)
for k in (50, 57, 62): n(0.0, ORG, k, 62, TP); 
n(0.0, STR, 74, 40, TP); n(0.2, STR, 81, 36, TP - 0.2)
hit(TP, "Dm", 118, 0.5)
funk(S["S1"], S["S1b"], "main", 2); hook(S["S1"] + 0.1, 86, FLU, 0, BEAT * 0.5)
n(S["S1b"], ORG, 62, 56, S["S1c"] - S["S1b"]); vibes(T("i2", "blue") - 0.3, 74, 7, 92, 0.07)
funk(S["S1c"], S["S2"], "tense", 3); hit(T("i2", "fake") - 0.15, "A", 114, 0.4)
funk(S["S2"], S["S2b"], "bright", 1); n(T("i3", "real") - 0.15, BRS, 69, 90, 0.4)
sneak(S["S2b"], S["S3"], 80); n(T("i3", "think") - 0.15, VIB, 81, 84, 0.6)
# paneer: warm kitchen funk
funk(S["S3"], S["S4"], "bright", 1); vibes(T("a1", "sour") - 0.2, 79, 4, 78)
funk(S["S4"], S["S5"], "bright", 1); n(T("a2", "clump") - 0.15, VIB, 74, 90, 0.3); n(T("a2", "catch") - 0.1, VIB, 79, 90, 0.3); hook(S["S4b"], 70, FLU, 0, BEAT * 0.5)
funk(S["S5"], S["S5b"], "bright", 1); hit(T("a3", "press") + 0.04, "F", 104, 0.3); funk(T("a3", "press") + 0.4, S["S6"], "bright", 1); n(T("a3", "block") - 0.2, BRS, 77, 86, 0.4)
funk(S["S6"], S["S7"], "main", 1); hit(T("a4", "No") + 0.05, "Dm", 104, 0.3)
# the lookalike
sneak(S["S7"], S["S8"], 86); funk(S["S8"], S["S8b"], "tense", 1); hook(T("b2", "analogue") - 0.1, 82, FLU, 0, BEAT * 0.4)
funk(S["S8b"], S["S9"], "tense", 2); hit(T("b2", "half") - 0.2, "Bb", 96, 0.3)
funk(S["S9"], S["S10"], "bright", 1); hit(T("b3", "legal") - 0.15, "C", 106, 0.4)
sneak(S["S10"], S["S11"], 84); hit(T("b4", "label") - 0.15, "A", 100, 0.3)
# blue: chemistry on vibes
n(S["S11"], STR, 62, 62, S["S12"] - S["S11"]); n(S["S11"], STR, 69, 56, S["S12"] - S["S11"]); hit(T("c1", "blue") - 0.15, "Gm", 94, 0.4)
funk(S["S12"], S["S13"], "main", 1); vibes(T("c2", "coils"), 74, 7, 72, 0.12); 
for j in range(7): n(T("c2", "Iodine") + j * 0.16, VIB, 79 + (j % 3) * 2, 76, 0.14)
funk(S["S13"], S["S14"], "main", 1); vibes(T("c3", "blue") - 0.15, 69, 7, 92, 0.06)
funk(S["S14"], S["S15"], "bright", 1); n(T("c4", "brown") - 0.2, TPT, 62, 78, 0.5)
# the guard
sneak(S["S15"], S["S16"], 92); hit(T("c5", "Starch") - 0.1, "Dm", 96, 0.3); hook(S["S15b"], 82, TPT, 0, BEAT * 0.4)
sneak(S["S16"], S["S16b"], 84)
for k in (50, 62, 65): n(S["S16b"], ORG, k, 60, S["S17"] - S["S16b"])
for j in range(int((S["S17"] - S["S16b"]) / 0.3)): n(S["S16b"] + j * 0.3, DR, 75, 66, 0.05)
hit(T("d2", "Brown") - 0.05, "Bb", 106, 0.3); downglide(T("d2", "passes") - 0.1, 74, 100)
sneak(S["S18"], S["S19"], 80)
funk(S["S19"], S["S19c"], "tense", 1); hit(T("d4", "blue") - 0.15, "A", 104, 0.4)
n(S["S20"], ORG, 62, 56, S["S20b"] - S["S20"]); hit(T("d5", "starch") - 0.1, "F", 116, 0.5); hook(T("d5", "starch") + 0.3, 84, FLU, 0, BEAT * 0.4)
funk(S["S21"], S["S22"], "main", 1); n(T("e1", "rubbery") - 0.15, GTR, 50, 94, 0.3)
funk(S["S22"], S["S24"], "bright", 1)
n(S["S24"], STR, 62, 60, S["S24b"] - S["S24"]); n(S["S24"], STR, 65, 56, S["S24b"] - S["S24"]); n(T("e4", "no") - 0.1, TIM, 45, 90, 0.5)
funk(S["S24b"], S["S25"], "main", 1); vibes(T("e4", "lab") - 0.15, 79, 4, 80)
# tips: the chase
funk(S["S25"], S["S26"], "bright", 2); hit(T("f1", "Three") - 0.12, "F", 100, 0.3)
funk(S["S26"], S["S27"], "bright", 2); hit(T("f2", "analogue") - 0.15, "C", 96, 0.3)
funk(S["S27"], S["S28"], "main", 2); funk(S["S28"], S["S29"], "tense", 2); n(T("f4", "why") - 0.15, TPT, 70, 90, 0.4)
funk(S["S29"], S["S29c"], "main", 1); vibes(T("f5", "add") - 0.1, 79, 3, 84)
hit(T("f5", "dont") - 0.1, "A", 100, 0.3); funk(T("f5", "dont") + 0.3, S["S30"], "tense", 1)
funk(S["S30"], S["S31"], "bright", 1); hit(T("f6", "draft") - 0.2, "Gm", 90, 0.3)
n(S["S31"], ORG, 62, 56, S["S32"] - S["S31"]); funk(S["S31"], S["S32"], "bright", 1); vibes(T("g1", "Blue") - 0.1, 74, 3, 80); n(T("g1", "real") - 0.1, TPT, 69, 76, 0.5)
funk(S["S32"], END - 1.6, "main", 3); hook(S["S32"] + 0.15, 92, FLU, 0, BEAT * 0.5); hit(END - 1.6, "Dm", 114, 1.2)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 40), (BAS, 64), (ORG, 84), (FLU, 56), (BRS, 72), (VIB, 92), (STR, 50), (TPT, 66), (TIM, 60)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = render(sorted(ev), END)
mus = signal.sosfilt(signal.butter(2, 10000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
