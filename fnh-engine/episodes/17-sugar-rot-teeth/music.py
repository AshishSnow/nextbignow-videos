"""HAUNTED-HOUSE SWING score for FreshNestHub 17 "does sugar rot your teeth?" (GeneralUser GS): a Halloween-night big-band swing at
176 bpm — walking upright bass, brushed ride + rimshot, comping vibraphone, a muted trumpet riff, pizzicato strings for the sneaky
bits, a church organ for the spooky stings (the myth, the cavity) and a glockenspiel for the mint 'repair' sparkles. Story-following:
a doorbell-ish organ chord already ringing at t = 0 (trick or treat), a horn stab + organ sting on ROT and CAVITY, a tip-toe pizzicato
minor groove for the bacteria city, a bright major 'rescue' lift for saliva, a ticking half-time for the timer chapter with a clock
pulse, a swaggering full band for the candy ranking and the plan, a cadence sting at the end. New genre for the channel (swing)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TBITE = T("i1", "sugar") - 0.05; TROT = T("i1", "rot") - 0.08

VIB, TPT, BS, PIZ, ORG, GLK, PNO, CLAR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {VIB: 11, TPT: 59, BS: 32, PIZ: 45, ORG: 19, GLK: 9, PNO: 0, CLAR: 71}
VOL = {VIB: 80, TPT: 88, BS: 112, PIZ: 90, ORG: 70, GLK: 84, PNO: 76, CLAR: 82, DR: 78}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 176.0
CH = {"Dm": (38, [62, 65, 69]), "Gm": (43, [62, 67, 70]), "A7": (45, [61, 64, 67, 69]), "Bb": (46, [62, 65, 70]), "F": (41, [60, 65, 69]),
      "C7": (48, [60, 64, 67, 70]), "Dm6": (38, [62, 65, 69, 71]), "E7": (40, [59, 62, 64, 68]), "Am": (45, [60, 64, 69]), "G7": (43, [59, 62, 65, 67])}
PROGS = {"spook": ["Dm", "Gm", "A7", "Dm"], "walk": ["Dm", "Dm6", "Gm", "A7"], "lift": ["F", "Bb", "C7", "F"], "swing": ["F", "Dm", "Gm", "C7"],
         "tick": ["Dm", "Dm", "Bb", "A7"]}
MEL = {"Dm": [74, 77, 81, 77, 74], "Gm": [74, 79, 82, 79, 74], "A7": [73, 76, 79, 76, 73], "Bb": [74, 77, 82, 77, 74], "F": [72, 77, 81, 77, 72],
       "C7": [72, 76, 79, 82, 79], "Dm6": [74, 77, 83, 77, 74], "E7": [71, 76, 80, 76, 71], "Am": [72, 76, 81, 76, 72], "G7": [71, 74, 77, 74, 71]}


def swing(t0, t1, prog="walk", level=2, half=False, tiptoe=False):
    """level 1: bass + brushes (+ pizzicato if tiptoe); 2: + vibes comping; 3: + muted trumpet riff. half = slow, spacious."""
    bt = BEAT * (2 if half else 1); bar = 4 * bt; b = 0; t = t0; sw = bt * 0.66
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * bt
            if tq >= t1 - 0.05: break
            wk = (0, 4 if ch[1:2] != "m" else 3, 7, 10)[q] if ch not in ("Dm6",) else (0, 3, 7, 9)[q]
            n(tq, BS, root + wk, 104 if q in (0, 2) else 90, bt * 0.85)
            n(tq, DR, 51, 58 if q % 2 == 0 else 46, 0.15); n(tq + sw, DR, 51, 36, 0.1)              # ride swing
            if q in (1, 3): n(tq, DR, 37, 54, 0.1); n(tq, DR, 42, 44, 0.1)                         # rimshot + hat on 2 & 4
            if q == 0 and not half: n(tq, DR, 36, 70, 0.2)
            if tiptoe and q % 2 == 0: n(tq, PIZ, root + 24 + (0, 7)[q // 2], 86, bt * 0.5); n(tq + sw, PIZ, root + 31, 70, bt * 0.3)
            if level >= 2 and q in (1, 3):
                for j, k in enumerate(vo): n(tq + sw + 0.004 * j, VIB, k, 62, bt * 0.5)
        if level >= 3 and b % 2 == 1:
            for j, k in enumerate(MEL[ch]):
                tj = t + j * bt * 0.75
                if tj < t1 - 0.05: n(tj, TPT, k - 12, 84, bt * 0.55)
        t += bar; b += 1


def stab(t, chord="Dm", v=108, d=0.45):
    root, vo = CH[chord]
    for k in vo: n(t, TPT, k, v, d); n(t, VIB, k + 12, v - 20, d)
    n(t, BS, root, 112, d); n(t, DR, 49, v - 24, 1.2); n(t, DR, 36, v, 0.2)


def organ(t, chord="Dm", v=84, d=1.6, low=True):
    root, vo = CH[chord]
    for k in vo: n(t, ORG, k - 12, v, d)
    if low: n(t, ORG, root - 12, v - 6, d)


def bells(t, base=84, nn=6, v=84):
    for i in range(nn): n(t + i * 0.07, GLK, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.5)


def clock(t0, t1, v=58):
    t = t0
    while t < t1 - 0.05: n(t, DR, 76 if int((t - t0) / BEAT) % 2 == 0 else 77, v, 0.08); t += BEAT


def hit(t, v=110): n(t, DR, 57, v - 30, 1.4); n(t, DR, 36, v, 0.3)


def fall(t, k0=79, nn=6, d=0.07):
    for i in range(nn): n(t + i * d, CLAR, k0 - 2 * i, 80 - 4 * i, d * 1.4)


SLOW = []
# hook: spooky organ chord ringing at frame 0 (trick or treat), swing kicks in on the bite, stab + organ sting on ROT
organ(0.0, "Dm", 80, TBITE + 0.4); n(0.0, GLK, 86, 70, 0.4); n(0.25, GLK, 83, 64, 0.5)
swing(TBITE, S["S1"] - 0.05, "spook", 2); stab(TROT, "A7", 110, 0.6); organ(TROT, "A7", 86, 1.0)
swing(S["S1"], S["S2"] - 0.05, "spook", 1, False, True); stab(T("i2", "right") - 0.1, "Dm", 100, 0.4)
swing(S["S2"], S["S3"] - 0.05, "tick", 1, True, True); bells(T("i3", "kindest") - 0.1, 86, 5, 72); fall(T("i3", "worst.") - 0.15, 77, 5)
# part 1: the culprit (tip-toe minor), sugar love lift, acid organ
hit(S["S3"] + 0.05, 100); swing(S["S3"], S["S4"] - 0.05, "walk", 2)
swing(S["S4"], S["S5"] - 0.05, "spook", 1, False, True); organ(T("a2", "city") - 0.1, "Gm", 70, 1.2, False)
swing(S["S5"], S["S5b"] - 0.05, "walk", 2); n(S["S5"] + 0.5, DR, 56, 70, 0.1); n(S["S5"] + 1.1, DR, 56, 70, 0.1)
swing(S["S5b"], S["S6"] - 0.05, "lift", 3); stab(T("a3", "love") - 0.1, "F", 104, 0.5); bells(T("a3", "love") - 0.05, 84, 7)
swing(S["S6"], S["S6b"] - 0.05, "walk", 2)
swing(S["S6b"], S["S7"] - 0.05, "spook", 1, False, True); stab(T("a4", "acid.") - 0.15, "A7", 110, 0.7); organ(T("a4", "acid.") - 0.15, "A7", 88, 1.4)
swing(S["S7"], S["S7b"] - 0.05, "spook", 2, True); fall(T("a5", "minerals") - 0.1, 81, 7)
swing(S["S7b"], S["S8"] - 0.05, "lift", 2); bells(S["S7b"] + 0.3, 88, 5, 70)
swing(S["S8"], S["S8b"] - 0.05, "tick", 1, True); clock(S["S8"], T("a6", "breaks.") - 0.1, 50); stab(T("a6", "breaks.") - 0.1, "E7", 112, 0.8); organ(T("a6", "breaks.") - 0.1, "E7", 90, 1.6)
swing(S["S8b"], S["S9"] - 0.05, "spook", 1, True); organ(T("a6", "cavity.") - 0.15, "Dm", 92, 2.0)
# rescue: bright major lift
hit(S["S9"] + 0.02, 100); swing(S["S9"], S["S10"] - 0.05, "lift", 2); stab(T("b1", "rescue") - 0.1, "F", 108, 0.6); bells(T("b1", "rescue") - 0.05, 84, 7, 92)
swing(S["S10"], S["S11"] - 0.05, "swing", 2); n(S["S10"] + 0.55, DR, 49, 80, 1.0); n(T("b2", "No,") - 0.1, TPT, 69, 90, 0.3)
swing(S["S11"], S["S11b"] - 0.05, "lift", 3); bells(T("b3", "washes") - 0.1, 86, 7, 86)
swing(S["S11b"], S["S12"] - 0.05, "swing", 2); bells(T("b3", "back") - 0.1, 88, 6, 84)
swing(S["S12"], S["S12b"] - 0.05, "lift", 2); bells(T("b4", "patch") + 0.9, 91, 7, 90)
swing(S["S12b"], S["S13"] - 0.05, "swing", 2)
swing(S["S13"], S["S14"] - 0.05, "lift", 2); bells(T("b5", "heal.") - 0.15, 86, 5, 80); organ(T("b5", "can't.") - 0.15, "Dm", 70, 1.0, False)
# part 2: the timer (half-time tick)
hit(S["S14"] + 0.02, 100); swing(S["S14"], S["S14b"] - 0.05, "tick", 1, True, True); clock(S["S14"], S["S15"], 46)
stab(S["S14b"] + 0.02, "Dm", 108, 0.6); organ(S["S14b"] + 0.02, "Dm", 80, 1.2)
swing(S["S15"], S["S16"] - 0.05, "tick", 2, True); clock(S["S15"], S["S16"], 52); fall(T("c2", "sixty") - 0.1, 79, 5)
swing(S["S16"], S["S17"] - 0.05, "tick", 2, True); clock(S["S16"], S["S18"], 52)
swing(S["S17"], S["S18"] - 0.05, "tick", 2, True); stab(T("c4", "Still") - 0.1, "Gm", 100, 0.5)
swing(S["S18"], S["S18b"] - 0.05, "spook", 2); clock(S["S18"], S["S19"], 56)
for j in range(6): n(S["S18"] + 0.2 + 0.35 * j, VIB, 74 + (0, 2, 3, 5, 7, 8)[j], 80, 0.3)
swing(S["S18b"], S["S19"] - 0.05, "spook", 2, True); stab(T("c5", "No") - 0.1, "A7", 108, 0.7); organ(T("c5", "No") - 0.1, "A7", 84, 1.4)
swing(S["S19"], S["S19b"] - 0.05, "walk", 2); stab(T("c6", "much") - 0.1, "Dm", 96, 0.4); stab(T("c6", "often.") - 0.15, "F", 112, 0.9); bells(T("c6", "often.") - 0.1, 84, 7, 90)
swing(S["S19b"], S["S20"] - 0.05, "swing", 3)
# part 3: candy ranking (full band swagger)
hit(S["S20"] + 0.02, 104); swing(S["S20"], S["S21"] - 0.05, "swing", 3); stab(T("d1", "ranking.") - 0.15, "C7", 104, 0.5)
swing(S["S21"], S["S21b"] - 0.05, "walk", 2); n(T("d2", "stick") - 0.1, TPT, 62, 96, 0.8); SLOW.append((T("d2", "stick") - 0.3, 0.5))
swing(S["S21b"], S["S22"] - 0.05, "spook", 1, True, True); clock(S["S21b"], S["S22"], 46)
swing(S["S22"], S["S23"] - 0.05, "spook", 2); stab(T("d3", "own") - 0.1, "A7", 104, 0.5)
swing(S["S23"], S["S23b"] - 0.05, "lift", 2); bells(T("d4", "washes") - 0.1, 86, 7, 88)
swing(S["S23b"], S["S24"] - 0.05, "swing", 3); stab(T("d4", "Told") - 0.1, "F", 110, 0.6); bells(T("d4", "Told") - 0.05, 88, 6, 86)
# part 4: the plan
hit(S["S24"] + 0.02, 100); swing(S["S24"], S["S25"] - 0.05, "swing", 2)
swing(S["S25"], S["S25b"] - 0.05, "lift", 2); bells(T("e2", "saliva.") - 0.15, 86, 6, 80)
swing(S["S25b"], S["S26"] - 0.05, "swing", 2); bells(S["S25b"] + 0.4, 91, 5, 76)
swing(S["S26"], S["S26b"] - 0.05, "tick", 2, True); clock(S["S26"], S["S27"], 50)
swing(S["S26b"], S["S27"] - 0.05, "spook", 1, True, True); n(T("e3", "scrub") - 0.1, TPT, 64, 90, 0.5)
swing(S["S27"], S["S27b"] - 0.05, "lift", 2); bells(T("e4", "twice") - 0.1, 86, 6, 84)
swing(S["S27b"], S["S28"] - 0.05, "walk", 2); organ(T("e4", "dentist.") - 0.15, "F", 66, 1.2, False)
swing(S["S28"], S["S29"] - 0.05, "swing", 3)
for j, w in enumerate(("bacteria", "acid,", "spit", "often")): n(T("f1", w) - 0.15, GLK, (84, 86, 88, 91)[j], 92, 0.5)
swing(S["S29"], END - 1.6, "lift", 2)
stab(END - 1.6, "F", 114, 1.6); organ(END - 1.6, "F", 80, 1.6); hit(END - 1.6, 112); bells(END - 1.55, 84, 7)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((VIB, 84), (TPT, 50), (BS, 64), (PIZ, 40), (ORG, 64), (GLK, 90), (PNO, 56), (CLAR, 74)): syn.control_change(ch, 10, pan)
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
