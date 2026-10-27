"""BOLLYWOOD-FESTIVE score for FreshNestHub 12 "silver on sweets" (GeneralUser GS): dhol-style groove on taiko + melodic tom
with tambourine/claps (bhangra chaal feel, 104 BPM), a sitar riff + D/A drone, a shehnai hook on reveals, strings swells,
tinkle-bell 'silver shimmer' on every silver moment, an anvil-like 'tink' on each hammer hit.
Story-following (ep 12 colour script in sound): full festive band for the sweets/celebration, the band DROPS to drone + light
dhol under explanations (coherence), the minor/phrygian mode with low strings + taiko only for the secret and the fakes,
stop-time hits on the reveals, festive band returns for the takeaway."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TB = T("i1", "silver") - 0.1

SIT, BASS, SHN, STR_, BELL, TAI, TOM, HARP, FLT, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9
PROG = {SIT: 104, BASS: 33, SHN: 111, STR_: 48, BELL: 112, TAI: 116, TOM: 117, HARP: 46, FLT: 73, SUB: 38}
VOL = {SIT: 104, BASS: 108, SHN: 92, STR_: 70, BELL: 92, TAI: 118, TOM: 100, HARP: 84, FLT: 76, SUB: 92, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BPM = 104
# festive = D mixolydian (D - C - G - D); dark = D phrygian-dominant colour (D - Eb - D - C#dim feel)
CH = {"D": (38, [62, 66, 69]), "C": (36, [60, 64, 67]), "G": (43, [62, 67, 71]), "Eb": (39, [63, 67, 70]), "Dm": (38, [62, 65, 69]), "A": (45, [61, 64, 69])}
PROGS = {"fest": ["D", "C", "G", "D"], "soft": ["D", "D", "C", "D"], "dark": ["Dm", "Eb", "Dm", "Eb"], "lift": ["G", "A", "D", "D"]}
RIFF = [74, 76, 78, 76, 74, 72, 69, 72]          # sitar riff (8ths) in D mixolydian
DRIFF = [74, 75, 78, 75, 74, 73, 70, 69]         # dark version (b2 / b6 colours)
HOOK = [81, 79, 78, 76, 78, 76, 74, 74]          # shehnai hook


def dhol(t0, t1, level=2, bpm=BPM, dark=False):
    """bhangra-style chaal: low 'dha' on taiko + high 'ta' on melodic tom; level 2 adds tambourine, 3 adds claps."""
    beat = 60 / bpm; bar = 4 * beat; t = t0
    lows = (0.0, 0.75, 1.5, 2.0, 2.75, 3.5); highs = (0.5, 1.0, 1.25, 2.5, 3.0, 3.25)
    while t < t1 - 0.05:
        for q in lows:
            if t + q * beat < t1 - 0.03: n(t + q * beat, TAI, 36, 104 if q in (0.0, 2.0) else 88, 0.3)
        if not dark or level >= 2:
            for q in highs:
                if t + q * beat < t1 - 0.03: n(t + q * beat, TOM, 62 if not dark else 58, 74, 0.12)
        if level >= 2:
            for q in range(8):
                if t + q * beat / 2 < t1 - 0.03: n(t + q * beat / 2, DR, 54, 40 + (16 if q % 2 else 0), 0.08)
        if level >= 3:
            for q in (1, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 39, 76, 0.1)
        t += bar


def band(t0, t1, prog="fest", level=2, bpm=BPM):
    """level 1: drone + bass + light dhol; 2: + sitar riff + tambourine; 3: + shehnai hook + strings + claps."""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    dark = prog == "dark"
    dhol(t0, t1, level, bpm, dark)
    n(t0, SIT, 38, 50, max(0.2, t1 - t0)); n(t0, SIT, 45, 44, max(0.2, t1 - t0))          # tanpura-like drone
    while t < t1 - 0.05:
        root, vo = CH[PROGS[prog][b % 4]]
        for q in (0, 1.5, 2, 3.5):
            if t + q * beat < t1 - 0.03: n(t + q * beat, BASS, root + (12 if q == 1.5 else 0), 100, beat * 0.45)
        if level >= 2:
            rf = DRIFF if dark else RIFF
            for j in range(8):
                tj = t + j * beat / 2
                if tj < t1 - 0.03 and (j % 4 != 3 or b % 2): n(tj, SIT, rf[(j + 2 * (b % 2)) % 8] - (0 if b % 4 < 2 else 2), 84, beat * 0.4)
        if level >= 3:
            for j in range(8):
                tj = t + j * beat / 2
                if tj < t1 - 0.03 and j % 4 != 3: n(tj, SHN, HOOK[j] - (0 if b % 2 == 0 else 2) - (1 if dark else 0), 86, beat * 0.45)
            for k in vo: n(t, STR_, k, 56, min(bar, t1 - t))
        t += bar; b += 1


def shimmer(t, base=88, nn=6, v=84):   # silver shimmer: tinkle bell upward run
    for i in range(nn): n(t + i * 0.04, BELL, base + (0, 2, 4, 7, 9, 12, 14)[i % 7] + 12 * (i // 7), v, 0.5)


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 20, 1.6); n(t, TAI, 36, v, 0.4); n(t, DR, 36, v - 10, 0.3)
    if big: n(t, SUB, 26, 104, 1.0); n(t, DR, 57, v - 16, 1.8)


def stab(t, chord="D", v=104, d=0.3):
    root, vo = CH[chord]
    for k in vo: n(t, SIT, k + 12, v - 10, d * 1.5); n(t, STR_, k, v - 24, d * 2); n(t, HARP, k + 12, v - 20, d)
    n(t, BASS, root, 110, d)


def pad(t0, t1, keys=(62, 69, 74), v=54, ch=None):
    for k in keys: n(t0, STR_ if ch is None else ch, k, v, max(0.2, t1 - t0))


def tink(t, v=90):   # hammer on silver: bright metallic tink
    n(t, BELL, 96, v, 0.2); n(t, DR, 81, v - 20, 0.1)


def roll(t, d=0.6, v=60):
    for i in range(int(d / 0.06)): n(t + i * 0.06, TOM, 60, v + i * 2, 0.06)


def glide(t, k0, k1, d=0.5, ch=SHN, v=90):   # shehnai bend-like run
    m = 6
    for i in range(m): n(t + d * i / m, ch, k0 + (k1 - k0) * i // (m - 1), v, d / m * 1.4)


# hook: festive band already playing at t=0 -> BEEP: stop-time hit + shimmer
band(0.0, TB - 0.02, "fest", 2)
hit(TB, 104, True); shimmer(TB + 0.02, 86, 7); pad(TB, S["S1"] - 0.05, (74, 78, 81), 50)
glide(T("i1", "metal?") - 0.2, 74, 81, 0.5)
band(S["S1"], S["S1b"] - 0.05, "soft", 1); shimmer(T("i2", "Real") - 0.1, 88, 6)
band(S["S1b"], S["S2"] - 0.05, "fest", 3); hit(T("i2", "eat") - 0.05, 100)
# open loop: dark sting
band(S["S2"], S["S3"] - 0.05, "dark", 1); stab(T("i3", "not") - 0.1, "Eb", 104, 0.4)
# PART 1
hit(S["S3"] + 0.05, 104); band(S["S3"], S["S3b"] - 0.05, "soft", 1); shimmer(T("a1", "vark.") - 0.1, 86, 7)
band(S["S3b"], S["S4"] - 0.05, "fest", 2)
band(S["S4"], S["S4b"] - 0.05, "soft", 1); stab(S["S4"] + 0.15, "G", 100, 0.3)
band(S["S4b"], S["S5"] - 0.05, "soft", 1)
for j in range(8): n(S["S4b"] + 0.1 + j * 0.12, BELL, 79 + j * 2, 70, 0.2)       # count-up run
band(S["S5"], S["S6"] - 0.05, "soft", 1); glide(T("a3", "eat?") - 0.25, 74, 79, 0.4, FLT, 80)
# cast card: one pluck per part (pre-training)
for j, tw in enumerate((S["S6"] + 0.15, T("a4", "small") - 0.1, T("a4", "silver") - 0.1)): n(tw, HARP, (74, 78, 81)[j], 100, 0.6)
pad(S["S6"], S["S6b"] - 0.05, (62, 69), 44)
band(S["S6b"], S["S7"] - 0.05, "soft", 1)
# hammering: the band locks to the hammer
band(S["S7"], S["S8"] - 0.05, "fest", 2)
for t0, per, t1 in ((T("a5", "hammer") - 0.35, 0.55, S["S7b"]), (S["S7b"] - 0.2, 0.42, S["S8"])):
    tt = t0 + per * 0.98
    while tt < t1 - 0.02:
        if tt > S["S7"]: tink(tt, 92)
        tt += per
band(S["S8"], S["S9"] - 0.05, "soft", 1)
u0 = S["S8"] + 0.2
for j in range(6): tink(u0 + j * 0.45, 70 + 4 * j)
# PART 2: how thin
hit(S["S9"] + 0.02, 104); band(S["S9"], S["S9b"] - 0.05, "fest", 3)
band(S["S9b"], S["S10"] - 0.05, "soft", 1); stab(T("b1", "eighty") - 0.15, "C", 100, 0.3)
band(S["S10"], S["S11"] - 0.05, "soft", 1); hit(T("b2", "three") - 0.15, 110, True); shimmer(T("b2", "three") - 0.1, 90, 7)
for j in range(5): n(S["S11"] + 0.1 + j * 0.15, HARP, 86 - j * 3, 80, 0.3)    # the iris dive
band(S["S11"] + 0.1, S["S12"] - 0.05, "soft", 1); stab(T("b3", "hair.") - 0.2, "G", 100, 0.4)
band(S["S12"], S["S13"] - 0.05, "fest", 2)
# PART 3: the secret (dark)
hit(S["S13"] + 0.02, 100); band(S["S13"], S["S14b"] - 0.05, "dark", 1); pad(S["S13"], S["S14b"] - 0.05, (50, 57), 60)
roll(S["S14"] + 0.3, max(0.2, S["S14b"] - S["S14"] - 0.4), 56)
hit(S["S14b"] + 0.05, 116, True); stab(S["S14b"] + 0.05, "Eb", 108, 0.5); band(S["S14b"] + 0.4, S["S15"] - 0.05, "dark", 2)
band(S["S15"], S["S16"] - 0.05, "soft", 1); hit(T("c3", "wasn't") - 0.15, 106)
band(S["S16"], S["S17"] - 0.05, "soft", 1); hit(T("c4", "banned") - 0.1, 112, True); stab(T("c4", "banned") - 0.1, "Dm", 104, 0.4)
band(S["S17"], S["S18"] - 0.05, "fest", 2); shimmer(T("c5", "plastic") + 0.2, 86, 5)
# PART 4: the fakes (dark detective)
hit(S["S18"] + 0.02, 100); band(S["S18"], S["S19"] - 0.05, "dark", 1)
for j in range(4): n(S["S18"] + 0.2 + j * 0.3, TOM, 55 + (j % 2) * 3, 80, 0.15)
band(S["S19"], S["S20"] - 0.05, "soft", 1)
for j in range(12): n(T("d2", "hundred") - 0.15 + j * 0.08, BELL, 84 + (j % 4) * 2, 60, 0.1)
band(S["S20"], S["S20b"] - 0.05, "dark", 1); stab(T("d3", "ten") - 0.1, "Eb", 100, 0.3)
hit(T("d3", "aluminum!") - 0.2, 116, True); stab(T("d3", "aluminum!") - 0.2, "Eb", 110, 0.5)
band(S["S21"], S["S22"] - 0.05, "dark", 1); hit(T("d4", "half") - 0.15, 104)
band(S["S22"], S["S23"] - 0.05, "dark", 1); n(T("d5", "lead") - 0.15, SIT, 50, 96, 0.4); n(T("d5", "nickel.") - 0.15, SIT, 51, 96, 0.4)
# PART 5: the twist (stop-time then shehnai)
hit(S["S23"] + 0.02, 112, True); glide(S["S23"] + 0.1, 74, 86, 0.6)
band(S["S23b"], S["S24"] - 0.05, "soft", 2); shimmer(T("e1", "food") - 0.1, 86, 5)
band(S["S24"], S["S25"] - 0.05, "soft", 1); hit(T("e2", "can't") - 0.1, 108); stab(T("e2", "can't") - 0.1, "Dm", 100, 0.4)
band(S["S25"], S["S26"] - 0.05, "soft", 1)
# takeaway: festive band returns
band(S["S26"], S["S27"] - 0.05, "fest", 3); shimmer(S["S26"] + 0.1, 88, 7)
for j, tw in enumerate((T("f2", "real") - 0.15, T("f2", "hammered") - 0.15, T("f2", "sometimes") - 0.15)): n(tw, HARP, (74, 78, 81)[j], 104, 0.5)
band(S["S27"], S["S28"] - 0.05, "lift", 2)
band(S["S28"], END - 1.6, "fest", 3)
stab(END - 1.6, "D", 112, 1.6); hit(END - 1.6, 114, True); shimmer(END - 1.55, 86, 7); glide(END - 1.5, 74, 86, 0.6)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((SIT, 50), (SHN, 76), (STR_, 64), (BELL, 82), (TOM, 44), (HARP, 70), (FLT, 40)): syn.control_change(ch, 10, pan)
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
# bright courtyard room: short, airy
rng = np.random.default_rng(12); irl = int(1.0 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.22)[:, None]; ir[: int(0.01 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, [300, 7000], "band", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.16 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.3) / np.tanh(1.3)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
