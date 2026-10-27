"""COOL-JAZZ score for FreshNestHub 11 "mint feels cold" (GeneralUser GS): swung ride cymbal + brushes, walking upright bass,
vibraphone comping on a ii-V-I-VI loop in C (Dm9 - G13 - Cmaj9 - A7), a muted-trumpet hook on reveals, celesta/glockenspiel
'ice sparkles' on every cold moment, a high string pad when the brain feels cold.
Story-following (ep 11 colour script in sound): warm full band when we talk about real temperature, the band DROPS to
bass + ride (coherence) under explanations, icy celesta + pad on every 'cold' feeling, stop-time hits on the reveals."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

VIB, BASS, TPT, PNO, CEL, GLK, STR_, TIMP, SUB, FLT, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9
PROG = {VIB: 11, BASS: 32, TPT: 59, PNO: 0, CEL: 8, GLK: 9, STR_: 49, TIMP: 47, SUB: 38, FLT: 73}
VOL = {VIB: 100, BASS: 116, TPT: 86, PNO: 70, CEL: 92, GLK: 80, STR_: 58, TIMP: 96, SUB: 92, FLT: 72, DR: 96}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


# ii - V - I - VI  (root, rootless jazz voicing)
CH = {"Dm9": (38, [53, 57, 60, 64]), "G13": (43, [53, 59, 64, 69]), "Cmaj9": (36, [52, 55, 59, 62]), "A7": (45, [55, 61, 64, 70]),
      "Fmaj7": (41, [52, 57, 60, 64]), "Em7": (40, [55, 59, 62, 67])}
PROGS = {"main": ["Dm9", "G13", "Cmaj9", "A7"], "soft": ["Dm9", "G13", "Dm9", "G13"], "warm": ["Fmaj7", "Em7", "Dm9", "Cmaj9"]}
BPM = 132
SW = 0.62  # swing ratio of the 8th pair
HOOK = [76, 74, 72, 69, 72, 74, 76, 79]   # muted-trumpet motif (8ths)


def walk(root, b, beat, t, v=104):
    tones = [root, root + 7, root + 12 if b % 2 else root + 10, root + 5 if b % 2 == 0 else root + 11]
    for q in range(4): n(t + q * beat, BASS, tones[q], v - 6 * (q % 2), beat * 0.85)


def band(t0, t1, prog="main", level=2, bpm=BPM):
    """level 1: walking bass + ride; 2: + brushes + vibes comp; 3: + trumpet motif + piano."""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        root, vo = CH[PROGS[prog][b % 4]]
        walk(root, b, beat, t)
        for q in range(4):
            tq = t + q * beat
            if tq >= t1 - 0.03: break
            n(tq, DR, 51, 58 + (10 if q % 2 else 0), 0.2)                  # ride: ding  ding-a ding  ding-a
            if q % 2: n(tq + beat * SW, DR, 51, 44, 0.12); n(tq, DR, 44, 50, 0.05)
            if level >= 2:
                n(tq, DR, 38, 30 + (10 if q % 2 else 0), 0.12)              # brush swish
                if q in (1, 3) and b % 2 == 0: n(tq + beat * SW, DR, 38, 46, 0.08)
        if level >= 2:
            for i, k in enumerate(vo): n(t + beat * SW + i * 0.006, VIB, k, 62 + 6 * level, beat * 1.2)
            for i, k in enumerate(vo[1:]): n(t + 2 * beat + beat * SW, VIB, k, 52, beat * 0.8)
        if level >= 3:
            for j in range(8):
                tj = t + (j // 2) * beat + (beat * SW if j % 2 else 0)
                if j % 4 != 3: n(tj, TPT, HOOK[(j + 4 * (b % 2)) % 8] - (0 if b % 4 < 2 else 2), 84, beat * 0.45)
            for k in vo[:3]: n(t, PNO, k - 12, 52, bar * 0.5)
        t += bar; b += 1


def ice(t, base=84, nn=5, ch=CEL, v=86):   # upward ice glissando
    for i in range(nn): n(t + i * 0.045, ch, base + (0, 4, 7, 11, 14, 16, 19)[i % 7] + 12 * (i // 7), v, 0.5)


def sparkle(t, base=88): ice(t, base, 4, GLK, 80)


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 20, 1.6); n(t, DR, 36, v, 0.3); n(t, TIMP, 43, v - 16, 0.8)
    if big: n(t, SUB, 31, 104, 1.0); n(t, DR, 57, v - 16, 1.8)


def stab(t, chord="A7", v=104, d=0.3):
    root, vo = CH[chord]
    for k in vo: n(t, VIB, k + 12, v - 10, d * 2); n(t, TPT, k, v - 24, d); n(t, PNO, k, v - 20, d)
    n(t, BASS, root, 110, d)


def pad(t0, t1, keys=(76, 79, 83, 88), v=58):
    for k in keys: n(t0, STR_, k, v, max(0.2, t1 - t0))


def whistle(t, k0=84, k1=96, d=0.5):   # flute 'cold wind'
    for i in range(6): n(t + d * i / 6, FLT, k0 + (k1 - k0) * i // 5, 64, d / 6 * 1.6)


def roll(t, d=0.6, v=60):
    for i in range(int(d / 0.05)): n(t + i * 0.05, DR, 38, v + i * 2, 0.06)


TF0_ = T("i1", "mint...") + 0.05
# hook: warm little band at t=0 (motion already happening) -> FREEZE: band stops, ice gliss + high pad + cold wind
band(0.0, TF0_ - 0.02, "warm", 1)
hit(TF0_, 96, True); ice(TF0_ + 0.02, 84, 7, CEL, 70); pad(TF0_ + 0.05, S["S1"] - 0.05, v=36)
# chew -> sip -> BRRR
band(S["S1"], S["S2"] - 0.05, "soft", 1); n(T("i2", "Chew") - 0.05, VIB, 74, 90, 0.4); n(T("i2", "sip") - 0.05, VIB, 77, 90, 0.4)
hit(T("i2", "whoa,") - 0.1, 106); ice(T("i2", "whoa,") - 0.05, 86, 6); pad(T("i2", "whoa,"), S["S2"] - 0.05)
# nothing got colder (warm, dry) -> TRICK
band(S["S2"], S["S3"] - 0.05, "warm", 1); stab(T("i3", "trick!") - 0.15, "A7", 108, 0.35)
# open loop: the nose teaser (suspended vibes + flute)
for k in (62, 67, 72): n(S["S3"], VIB, k, 70, S["S4"] - S["S3"])
whistle(T("i4", "nose.") - 0.2, 79, 91, 0.6); hit(T("i4", "nose.") - 0.15, 96)
# PART 1: full band for the chapter, then thin under the explanation
band(S["S4"], S["S4b"] - 0.05, "main", 3); hit(S["S4"] + 0.05, 106)
band(S["S4b"], S["S5"] - 0.05, "soft", 1); sparkle(T("a1", "menthol,") - 0.1, 86)
band(S["S5"], S["S6"] - 0.05, "soft", 1)
for j in range(5): n(S["S5"] + 0.15 + j * 0.2, CEL, 72 + j * 3, 78, 0.3)   # the zoom
sparkle(T("a2", "nerve") - 0.2, 84); n(T("a2", "wires") - 0.1, VIB, 79, 88, 0.5)
band(S["S6"], S["S7"] - 0.05, "soft", 2); ice(T("a3", "cold") - 0.2, 84, 5); pad(T("a3", "cold"), S["S7"] - 0.05, (79, 83, 88))
band(S["S7"], S["S7b"] - 0.05, "warm", 1)
for j in range(6): n(S["S7"] + 0.3 + j * 0.25, VIB, 79 - j * 2, 70, 0.3)   # temperature sliding down
ice(T("a4", "twenty-five") - 0.1, 86, 5)
band(S["S7b"], S["S7c"] - 0.05, "warm", 2)
hit(S["S7c"] + 0.02, 108); ice(S["S7c"] + 0.05, 88, 7, GLK); pad(S["S7c"], S["S8"] - 0.05)
band(S["S8"], S["S8b"] - 0.05, "soft", 1); ice(T("a6", "fits") - 0.15, 84, 4)
band(S["S8b"], S["S9"] - 0.05, "main", 2)
# CLICK -> COLD! (big)
hit(S["S9"] + 0.1, 116, True); stab(S["S9"] + 0.1, "A7", 110, 0.4)
band(S["S9"] + 0.5, S["S9b"] - 0.05, "soft", 1); roll(S["S9b"] + 0.1, max(0.2, T("a7", "COLD!") - S["S9b"] - 0.3), 56)
hit(T("a7", "COLD!") - 0.15, 118, True); ice(T("a7", "COLD!") - 0.1, 84, 7); pad(T("a7", "COLD!"), S["S10b"] - 0.05); whistle(T("a7", "COLD!"), 84, 98, 0.9)
# brain believes it -> the temperature didn't change (warm band back, stop on 'didn't')
band(S["S10b"], S["S11"] - 0.05, "warm", 2); hit(T("a8", "didn't") - 0.05, 108); stab(T("a8", "didn't") - 0.05, "Dm9", 100, 0.3)
# PART 2
hit(S["S11"] + 0.02, 106); band(S["S11"] + 0.02, S["S12"] - 0.05, "main", 3)
band(S["S12"], S["S12b"] - 0.05, "soft", 1)
for j in range(8): n(T("b2", "jumpy.") - 0.15 + j * 0.07, VIB, 84 + (j % 2) * 3, 74, 0.08)   # nervous tremble
band(S["S12b"], S["S13"] - 0.05, "warm", 1)
for j in range(5): n(T("b2", "warmer") - 0.2 + j * 0.1, VIB, 74 + j * 2, 78, 0.2)
band(S["S13"], S["S13b"] - 0.05, "soft", 1); pad(T("b3", "half") - 0.1, S["S13b"], (76, 79), 50)
roll(S["S13b"] + 0.05, max(0.2, T("b3", "screams!") - S["S13b"] - 0.25), 60)
hit(T("b3", "screams!") - 0.15, 120, True); ice(T("b3", "screams!") - 0.1, 84, 7); ice(T("b3", "screams!"), 96, 5, GLK); whistle(T("b3", "screams!"), 86, 100, 0.8)
band(S["S14"], S["S15"] - 0.05, "warm", 2); ice(T("b4", "cool") - 0.1, 86, 5)
# PART 3: the proof
hit(S["S15"] + 0.05, 106); band(S["S15"] + 0.05, S["S16"] - 0.05, "main", 2); stab(T("c1", "two") - 0.1, "Cmaj9", 104, 0.35)
band(S["S16"], S["S16b"] - 0.05, "soft", 1); n(T("c2", "without") - 0.1, TPT, 70, 90, 0.2); n(T("c2", "without") + 0.15, TPT, 66, 90, 0.4)
band(S["S16b"], S["S17"] - 0.05, "soft", 2); hit(T("c3", "gone!") - 0.15, 104)
hit(T("c4", "Nobel") - 0.15, 116, True); stab(T("c4", "Nobel") - 0.15, "Cmaj9", 112, 0.5); sparkle(T("c4", "Nobel"), 88)
band(S["S17"] + 0.3, S["S17c"] - 0.05, "main", 3)
band(S["S17c"], S["S18"] - 0.05, "main", 2); n(T("c5", "heat") - 0.1, TPT, 74, 92, 0.3); ice(T("c5", "cold") - 0.1, 86, 5)
hit(LINES["c5"]["end"] - 0.35, 112); stab(LINES["c5"]["end"] - 0.35, "A7", 106, 0.4)
# PART 4: the nose trick (pay-off of the open loop)
for k in (62, 67, 72): n(S["S18"], VIB, k, 70, S["S19"] - S["S18"])
whistle(S["S18"] + 0.3, 79, 91, 0.6); hit(S["S18"] + 0.05, 100)
band(S["S19"], S["S20"] - 0.05, "soft", 1); sparkle(T("d2", "menthol") - 0.1, 84); n(T("d2", "plain") - 0.1, VIB, 67, 86, 0.4)
band(S["S20"], S["S21"] - 0.05, "soft", 2)
for j in range(10): n(S["S20"] + 0.2 + j * 0.12, GLK, 84 + (j % 2) * 5, 60, 0.1)   # clock ticks
stab(T("d3", "clearer.") - 0.2, "Cmaj9", 100, 0.4)
band(S["S21"], S["S21b"] - 0.05, "soft", 1); hit(T("d4", "no") - 0.15, 112, True); stab(T("d4", "no") - 0.15, "A7", 106, 0.35)
band(S["S21b"], S["S22"] - 0.05, "soft", 1); ice(S["S21b"] + 0.3, 84, 4); stab(T("d5", "breathe!") - 0.2, "Cmaj9", 102, 0.5)
# takeaway + recap 1-2-3-4 + sting
band(S["S22"], S["S23"] - 0.05, "warm", 2); ice(T("e1", "feel.") - 0.2, 86, 5)
band(S["S23"], S["S24"] - 0.05, "main", 2)
for j, tw in enumerate((S["S23"] + 0.25, T("e2", "rings") - 0.15, T("e2", "jumpy,") - 0.15, T("e2", "nose.") - 0.15)): n(tw, GLK, (79, 83, 86, 91)[j], 96, 0.4)
band(S["S24"], END - 1.6, "main", 3)
stab(END - 1.6, "Cmaj9", 112, 1.6); hit(END - 1.6, 116, True); ice(END - 1.55, 84, 7); ice(END - 1.2, 96, 5, GLK)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    try: syn.program_select(DR, sid, 128, 40, True)        # brush kit
    except Exception: syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((VIB, 46), (TPT, 80), (PNO, 70), (CEL, 54), (GLK, 74), (STR_, 64), (FLT, 40)): syn.control_change(ch, 10, pan)
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
# jazz club room: warm, short, darker reverb than the surf spring
rng = np.random.default_rng(11); irl = int(1.2 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.28)[:, None]; ir[: int(0.012 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, [250, 5200], "band", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.18 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.3) / np.tanh(1.3)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
