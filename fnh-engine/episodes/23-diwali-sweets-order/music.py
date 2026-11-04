"""SPAGHETTI-WESTERN score for FreshNestHub 23 "which Diwali sweet goes bad first?" (GeneralUser GS): a lit fuse is a showdown. Am at 100 bpm: a galloping acoustic-guitar and bass figure, tremolo-twang electric guitar, a lone whistle (an original tune), muted trumpet, choir swells, timpani, castanets. New genre for the channel.
The score FOLLOWS THE STORY: opener = whistle + gallop under the burning fuses; POOF stops the band dead; thin gallop under explanations; a cold celesta in the fridge; the re-gift corridor is the full gallop passed from instrument to instrument; the list is a triumphant trumpet."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}; TF = T("i1", "first") - 0.22
GTR, BAS, TWG, WHS, TPT, CHO, STR, CEL, TIM, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {GTR: 25, BAS: 32, TWG: 27, WHS: 78, TPT: 56, CHO: 52, STR: 48, CEL: 8, TIM: 47}
VOL = {GTR: 88, BAS: 104, TWG: 84, WHS: 84, TPT: 84, CHO: 72, STR: 72, CEL: 90, TIM: 96, DR: 74}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 0.6
CH = {"Am": (33, [57, 60, 64]), "G": (31, [55, 59, 62]), "F": (29, [53, 57, 60]), "E": (28, [56, 59, 64]), "Dm": (38, [57, 62, 65]), "C": (36, [55, 60, 64])}
PROGS = {"main": ["Am", "G", "F", "E"], "bright": ["C", "G", "Am", "E"], "tense": ["Am", "Dm", "Am", "E"]}


def gallop(t0, t1, prog="main", level=2):
    """1: bass + muted gallop. 2: + castanets + guitar strum. 3: + twang riff + trumpet stabs."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * BEAT
            if tq >= t1 - 0.05: break
            n(tq, BAS, root, 100 if q % 2 == 0 else 84, BEAT * 0.5)
            for off, vv in ((0, 62), (0.5, 46), (0.75, 54)): n(tq + off * BEAT, GTR, vo[0], vv, BEAT * 0.14)
            if level >= 2:
                for off in (0.5, 0.75): n(tq + off * BEAT, DR, 85, 50, 0.05)
                if q % 2:
                    for k in vo: n(tq, GTR, k + 12, 64, BEAT * 0.3)
        if level >= 3:
            for off, dd in ((0, 0), (1.5, 2), (2, 0), (3, 7)): n(t + off * BEAT, TWG, root + 24 + dd, 86, BEAT * 0.5)
            if b % 2: 
                for k in vo: n(t + 2 * BEAT, TPT, k + 12, 88, BEAT * 0.5)
        t += 4 * BEAT; b += 1


WHISTLE = [(0, 76), (0.5, 76), (1, 81), (2, 79), (3, 76), (3.5, 74), (4, 72), (5, 71), (6, 69)]


def whistle(t0, v=90, tr=0, ch=WHS, gap=BEAT):
    for off, k in WHISTLE: n(t0 + off * gap, ch, k + tr, v, gap * 0.8)


def hit(t, chord="Am", v=112, d=0.5):
    root, vo = CH[chord]
    n(t, BAS, root, v, d); n(t, TIM, root + 12, v, 0.4); n(t, DR, 49, v - 22, 0.3)
    for k in vo: n(t, TPT, k + 12, v - 8, d); n(t, STR, k + 24, v - 26, d)


def tremolo(t0, t1, k, v=70):
    t = t0
    while t < t1: n(t, TWG, k, v, 0.06); t += 0.09


def bells(t, base=84, nn=6, v=82, ch=CEL):
    for j in range(nn): n(t + j * 0.07, ch, base + (0, 3, 7, 10, 12, 15, 19)[j % 7], v, 0.3)


def choir(t0, t1, ch="Am", v=64):
    _, vo = CH[ch]
    for k in vo: n(t0, CHO, k, v, t1 - t0)


SLOW = []
# ---- hook: gallop + the whistle under burning fuses; the poof stops the band dead
gallop(0.0, TF, "main", 2); whistle(0.15, 88, 0, WHS, 0.3); tremolo(0.0, TF, 69, 40); hit(TF, "Dm", 110, 0.3); SLOW.append((TF + 0.05, 0.6))
# tonight / a month
choir(S["S1"], S["S1b"], "Am", 58); n(T("i2", "tonight") - 0.15, TIM, 45, 90, 0.4)
gallop(S["S1b"], S["S2"], "bright", 1); hit(T("i2", "month") - 0.2, "C", 100, 0.3)
# the cracker
gallop(S["S2"], S["S2b"], "tense", 1); n(T("i3", "fuse") - 0.15, TWG, 57, 90, 0.5)
tremolo(S["S2b"], S["S3"], 57, 56); hit(T("i3", "lit") - 0.2, "E", 112, 0.5)
# the list: the scroll, trumpet call, each row a step
gallop(S["S3"], S["S4"], "bright", 1); n(T("a1", "list") - 0.3, TPT, 69, 92, 0.5); n(T("a1", "list") - 0.05, TPT, 76, 96, 0.5)
gallop(S["S4"], S["S4b"], "main", 1); hit(T("a2", "kalaakund") - 0.15, "Am", 100, 0.3); gallop(S["S4b"], S["S5"], "main", 2)
gallop(S["S5"], S["S6"], "bright", 1); bells(T("a3", "fridge") - 0.2, 84, 6, 84)
gallop(S["S6"], S["S8"], "bright", 2)
gallop(S["S8"], S["S8b"], "main", 3); whistle(S["S8"] + 0.1, 92, 0, WHS, 0.25); hit(T("a6", "month") - 0.2, "C", 108, 0.4); gallop(S["S8b"], S["S9"], "bright", 2)
# why? the band thins
choir(S["S9"], S["S10"], "Dm", 58); n(T("b1", "month") - 0.15, TIM, 40, 90, 0.5); n(T("b1", "month") - 0.1, TWG, 52, 92, 0.6)
bells(T("b2", "water") - 0.1, 79, 7, 92); gallop(S["S10b"], S["S11"], "bright", 1)
gallop(S["S11"], S["S12"], "bright", 1); hit(T("b3", "No") - 0.1, "G", 96, 0.25)
gallop(S["S12"], S["S12b"], "main", 1); gallop(S["S12b"], S["S13"], "main", 2); hit(T("b4", "meal") - 0.15, "F", 96, 0.3)
# the plank
gallop(S["S13"], S["S15b"], "bright", 1); n(T("c2", "nine") - 0.3, CEL, 84, 92, 0.3); n(T("c2", "seven") - 0.3, CEL, 76, 92, 0.3); n(T("c3", "zero") - 0.1, CEL, 80, 96, 0.3)
tremolo(S["S15b"], S["S16"], 64, 58); choir(T("c3", "mould") - 0.2, S["S16"] + 0.5, "Am", 60)
# fuzz / roots: a dark choir and one twang
gallop(S["S16"], S["S17"], "tense", 1); hit(T("c4", "fuzz") - 0.15, "Dm", 104, 0.4)
gallop(S["S17"], S["S17b"], "tense", 1); hit(T("c5", "scrape") - 0.1, "E", 104, 0.3)
choir(S["S17b"], S["S18b"], "Am", 66); n(S["S18"], STR, 45, 58, S["S18b"] - S["S18"]); n(T("c6", "roots") - 0.15, TWG, 40, 96, 1.1); hit(T("c6", "bin") - 0.25, "Am", 104, 0.4)
# fridge: cold celesta
for j in range(10): n(S["S19"] + j * 0.2, CEL, (84, 88, 91, 96)[j % 4], 78, 0.25)
hit(T("d1", "Nearly") - 0.1, "E", 100, 0.3); SLOW.append((T("d1", "Nearly") - 0.05, 0.4))
gallop(S["S20"], S["S21"], "bright", 1); n(T("d2", "nine") - 0.1, TPT, 69, 84, 0.3)
for j in range(6): n(T("d2", "thirty", 1) + j * 0.12, CEL, 84 + j * 2, 86, 0.14)
choir(S["S21"], S["S22"], "Dm", 56)
for w, k in (("dry", 48), ("hard", 45), ("sandy", 40)): n(T("d3", w) - 0.1, TWG, k, 96, 0.4)
hit(T("d4", "rock") - 0.15, "Am", 114, 0.25); gallop(S["S22b"], S["S23"], "bright", 2)
# the re-gift: full gallop, whistle tune passed from instrument to instrument
hit(T("e1", "regift") - 0.3, "C", 112, 0.4); gallop(T("e1", "regift") + 0.3, S["S24"], "main", 2)
gallop(S["S24"], S["S25"], "main", 3); whistle(T("e2", "gives") - 0.1, 86, 0, WHS, 0.2); whistle(T("e2", "pass") - 0.1, 84, -12, TWG, 0.2); whistle(T("e2", "gives", 1) - 0.1, 90, -12, TPT, 0.2)
hit(T("e3", "resets") - 0.15, "E", 110, 0.4); choir(S["S25b"], S["S26"], "Am", 70); n(S["S25b"], TIM, 33, 92, 0.6); n(S["S25b"] + 0.6, TIM, 33, 84, 0.6); hit(T("e3", "Tuesday") - 0.15, "Am", 108, 0.5)
gallop(S["S26"], S["S27"], "bright", 1); n(T("e4", "tray") - 0.2, TPT, 76, 90, 0.4)
gallop(S["S27"], S["S27b"], "bright", 1); gallop(S["S27b"], S["S28"], "tense", 2); tremolo(T("e5", "hot") - 0.15, S["S28"], 69, 60)
gallop(S["S28"], S["S29"], "bright", 2); hit(T("f1", "first") - 0.15, "C", 96, 0.25); hit(T("f1", "last") - 0.15, "G", 96, 0.25)
gallop(S["S29"], S["S30"], "bright", 2); whistle(S["S29"] + 0.4, 74, 0, TPT, 0.45)
gallop(S["S30"], S["S31"], "tense", 1); hit(T("f3", "bin") - 0.15, "Am", 100, 0.3)
gallop(S["S31"], END - 1.8, "main", 3); hit(END - 1.8, "Am", 114, 1.6); bells(END - 1.75, 84, 7, 92)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 44), (BAS, 64), (TWG, 84), (WHS, 56), (TPT, 70), (CHO, 64), (STR, 74), (CEL, 90), (TIM, 60)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = render(sorted(ev), END)


def ritard(x, t0, dur, floor=0.4):
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = 1 - (1 - floor) * np.linspace(0, 1, L) ** 1.4
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.1, L)[:, None]
    x[i0:i0 + L] = seg


for t0, d in SLOW: ritard(mus, t0, d)
mus = signal.sosfilt(signal.butter(2, 10000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
