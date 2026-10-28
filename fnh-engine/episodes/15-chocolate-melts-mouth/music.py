"""PARIS CAFE MUSETTE WALTZ score for FreshNestHub 15 "why chocolate melts in your mouth" (GeneralUser GS): a 3/4 chocolatier
waltz (oom-pah-pah: upright bass on 1, nylon guitar + accordion chords on 2 and 3), musette accordion melody, clarinet answers,
pizzicato strings, celesta + glockenspiel for the invisible CRYSTAL world, soft brushes. Story-following: waltz already turning at
t=0 (the snap), a sweet golden lift on 'melt'; minor + low clarinet for MOULD? / the catch / the fridge; celesta crystals for the
six shapes; a triumphant brass-and-accordion fanfare for 'winner'; a slowing 'ritardando' (waltz slows and drops a step) when the
chocolate cools and again at bloom; full waltz for the takeaways + a cadence sting. New genre for the channel (musette)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TSNAP = 0.85; TMELT = T("i1", "melt...") - 0.05

ACC, BS, GT, CL, PZ, CEL, GLK, BRS, PAD, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {ACC: 21, BS: 32, GT: 24, CL: 71, PZ: 45, CEL: 8, GLK: 9, BRS: 61, PAD: 89}
VOL = {ACC: 92, BS: 110, GT: 84, CL: 84, PZ: 92, CEL: 88, GLK: 80, BRS: 86, PAD: 58, DR: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 0.4                                   # 150 bpm waltz, bar = 3 beats = 1.2 s
CH = {"C": (36, [55, 60, 64]), "Am": (33, [57, 60, 64]), "Dm": (38, [57, 62, 65]), "G7": (31, [55, 59, 65]), "F": (41, [57, 60, 65]),
      "E7": (40, [56, 59, 62]), "Fm": (41, [56, 60, 65]), "Ab": (44, [56, 60, 63])}
PROGS = {"main": ["C", "Am", "Dm", "G7"], "sweet": ["F", "C", "Dm", "G7"], "minor": ["Am", "Dm", "E7", "Am"], "dark": ["Am", "Fm", "E7", "Am"],
         "gold": ["C", "F", "G7", "C"]}
MEL = {"C": [76, 74, 72, 74, 76, 79], "Am": [76, 72, 69, 72, 76, 77], "Dm": [77, 74, 69, 74, 77, 81], "G7": [79, 77, 74, 71, 74, 77],
       "F": [77, 76, 72, 76, 77, 81], "E7": [76, 74, 71, 68, 71, 74], "Fm": [77, 75, 72, 75, 77, 80], "Ab": [75, 72, 68, 72, 75, 79]}


def waltz(t0, t1, prog="main", level=2, slow=1.0):
    """level 1: bass + guitar/accordion chords (oom-pah-pah); 2: + musette melody on accordion + brushes; 3: + clarinet answers."""
    bt = BEAT * slow; bar = 3 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        n(t, BS, root + 12, 104, bt * 0.9)
        for q in (1, 2):
            tq = t + q * bt
            if tq < t1 - 0.05:
                for j, k in enumerate(vo): n(tq + 0.008 * j, GT, k, 70, bt * 0.6); n(tq, ACC, k, 52, bt * 0.5)
        n(t, DR, 36, 60, 0.2)
        for q in (1, 2):
            if t + q * bt < t1 - 0.05: n(t + q * bt, DR, 38 if q == 1 else 37, 34, 0.1)
        if level >= 2:
            mel = MEL[ch]
            for j in range(6):
                tj = t + j * bt / 2
                if tj < t1 - 0.05: n(tj, ACC, mel[j] + (12 if prog == "gold" else 0), 84 if j % 2 == 0 else 70, bt * 0.45)
        if level >= 3 and b % 2 == 1:
            for j, k in enumerate(MEL[ch][::-1][:3]):
                tj = t + j * bt
                if tj < t1 - 0.05: n(tj, CL, k - 12, 76, bt * 0.9)
        t += bar; b += 1


def crystal(t0, t1, v=74, gap=0.2, base=(84, 88, 91, 96, 91, 88)):
    i = 0; t = t0
    while t < t1 - 0.05:
        n(t, CEL, base[i % len(base)], v, 0.5); t += gap; i += 1


def pad(t0, t1, keys=(57, 60, 64), v=44):
    for k in keys: n(t0, PAD, k, v, max(0.2, t1 - t0))


def hit(t, v=110, root=36):
    n(t, DR, 57, v - 30, 1.4); n(t, DR, 36, v, 0.3); n(t, BS, root + 12, v, 0.5)


def stab(t, chord="C", v=100, d=0.4, brass=False):
    root, vo = CH[chord]
    for k in vo: n(t, ACC, k + 12, v - 10, d); n(t, PZ, k, v - 20, d)
    if brass:
        for k in vo: n(t, BRS, k, v - 10, d)
    n(t, BS, root + 12, 110, d)


def sparkle(t, base=84, nn=6, v=84):
    for i in range(nn): n(t + i * 0.05, GLK, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.5)


def pizz_walk(t0, t1, keys=(60, 64, 67, 72), v=80, gap=0.2):
    i = 0; t = t0
    while t < t1 - 0.05:
        n(t, PZ, keys[i % len(keys)], v, 0.2); t += gap; i += 1


SLOW = []                                   # (t0, dur) ritardando (varispeed slow-down) applied after rendering
# HOOK: waltz turning at t=0, the snap, a sweet lift on MELT
waltz(0.0, S["S0b"] - 0.05, "main", 2); hit(TSNAP, 100); sparkle(TMELT, 84, 6, 90); stab(TMELT, "F", 98, 0.8)
waltz(S["S0b"], S["S1"] - 0.05, "sweet", 2)
waltz(S["S1"], S["S2"] - 0.05, "main", 1); hit(T("i2", "snaps.") - 0.1, 100); sparkle(T("i2", "melts") - 0.1, 79, 5)
waltz(S["S2"], S["S3"] - 0.05, "minor", 1, 1.15); stab(T("i3", "It's") - 0.1, "E7", 104, 0.6); n(T("i3", "It's") - 0.1, CL, 52, 90, 1.2)
# PART 1: the fat + six crystals
hit(S["S3"] + 0.05, 98); waltz(S["S3"], S["S4"] - 0.05, "main", 1)
for j in range(6): n(T("a1", "The") - 0.2 + j * 0.13, GLK, 96 - j * 3, 72, 0.25)                     # the zoom-in dive
waltz(S["S4"], S["S4b"] - 0.05, "sweet", 3)
waltz(S["S4b"], S["S5"] - 0.05, "main", 1); sparkle(T("a2", "strange") - 0.1, 86, 7)
crystal(S["S5"] + 0.1, T("a3", "six") - 0.15, 60, 0.4); pad(S["S5"], S["S6"] - 0.05, (57, 64, 71), 46)
for j in range(6): n(T("a3", "six") - 0.15 + 0.13 * j, CEL, (84, 86, 88, 91, 93, 96)[j], 86, 0.5)
waltz(S["S6"], S["S6b"] - 0.05, "main", 1); pizz_walk(S["S6"] + 0.1, S["S6b"] - 0.05, (64, 67, 72, 67), 74, 0.3)
waltz(S["S6b"], S["S7"] - 0.05, "sweet", 2)
# shapes 1-4 weak / 5 the winner
waltz(S["S7"], S["S7b"] - 0.05, "minor", 1); n(T("b1", "weak") - 0.1, CL, 45, 96, 0.8)
waltz(S["S7b"], S["S8"] - 0.05, "minor", 1, 1.1)
for j in range(5): n(T("b1", "melt") - 0.1 + 0.25 * j, PZ, 72 - 2 * j, 74, 0.3)                       # melting slide
hit(S["S8"] + 0.02, 104); stab(T("b2", "winner.") - 0.1, "C", 112, 1.2, True); sparkle(T("b2", "winner.") - 0.05, 84, 7, 96)
for j, k in enumerate((67, 72, 76, 79)): n(S["S8"] + 0.1 + 0.14 * j, BRS, k, 96, 0.3)
waltz(S["S9"], S["S9b"] - 0.05, "gold", 2); sparkle(T("b3", "shiny.") - 0.15, 88, 6); hit(T("b3", "snaps.") - 0.1, 104)
waltz(S["S9b"], S["S10"] - 0.05, "main", 1); sparkle(T("b3", "thirty-four") - 0.2, 84, 5)
waltz(S["S10"], S["S11"] - 0.05, "sweet", 2)
waltz(S["S11"], S["S11b"] - 0.05, "main", 1); waltz(S["S11b"], S["S12"] - 0.05, "sweet", 3); sparkle(T("b5", "melts") - 0.1, 79, 6)
# PART 2: the catch -> tempering
hit(S["S12"] + 0.02, 100, 33); stab(S["S12"] + 0.05, "Am", 96, 0.8); n(S["S12"] + 0.05, CL, 45, 90, 1.4)
waltz(S["S13"], S["S13b"] - 0.05, "main", 1); SLOW.append((T("c2", "cool,") - 0.6, 0.6))
waltz(S["S13b"], S["S14"] - 0.05, "minor", 1)
for j in range(8): n(S["S13b"] + 0.1 + 0.18 * j, CEL, (96, 85, 91, 88, 93, 84, 90, 86)[j], 70, 0.3)        # messy crystals
waltz(S["S14"], S["S15"] - 0.05, "main", 2); stab(T("c3", "tempering.") - 0.15, "C", 104, 0.6, True)
waltz(S["S15"], S["S16"] - 0.05, "main", 1)
for w, k in (("melt", 79), ("cool", 72), ("warm", 76)): n(T("c4", w) - 0.15, GLK, k + 12, 92, 0.5); n(T("c4", w) - 0.15, CL, k - 12, 80, 0.6)
waltz(S["S16"], S["S16b"] - 0.05, "minor", 1)
for j in range(4): n(T("c5", "melts") - 0.1 + 0.2 * j, PZ, 67 - 3 * j, 74, 0.3)
waltz(S["S16b"], S["S17"] - 0.05, "gold", 2); sparkle(S["S16b"] + 0.1, 86, 7, 92)
crystal(S["S17"], S["S17b"] - 0.05, 66, 0.4, (84, 91, 88, 96)); waltz(S["S17"], S["S17b"] - 0.05, "sweet", 1)
waltz(S["S17b"], S["S18"] - 0.05, "sweet", 2); crystal(S["S17b"] + 0.1, T("c6", "way.") - 0.1, 70, 0.12, (72, 76, 79, 84, 88, 91, 96))
stab(T("c6", "way.") - 0.1, "C", 104, 0.8); sparkle(T("c6", "way.") - 0.05, 84, 6)
# PART 3: the white dust
hit(S["S18"] + 0.02, 98, 33); waltz(S["S18"], S["S19"] - 0.05, "dark", 1, 1.1); n(S["S18"] + 0.1, CL, 45, 84, 2.0)
stab(T("d2", "mould.") + 0.05, "E7", 106, 0.5); SLOW.append((T("d2", "mould.") - 0.45, 0.45))
stab(T("d2", "bloom.") - 0.15, "C", 106, 0.9); sparkle(T("d2", "bloom.") - 0.1, 84, 6)
waltz(S["S20"], S["S20b"] - 0.05, "main", 1); pizz_walk(T("d3", "rises") - 0.15, S["S20b"] - 0.05, (60, 64, 67, 72, 76, 79), 80, 0.12)
waltz(S["S20b"], S["S21"] - 0.05, "sweet", 1)
waltz(S["S21"], S["S21b"] - 0.05, "main", 1, 1.2)
waltz(S["S21b"], S["S22"] - 0.05, "minor", 1)
waltz(S["S22"], S["S22b"] - 0.05, "dark", 1, 1.1); pad(S["S22"], S["S22b"], (57, 64, 69), 50)
crystal(S["S22b"] + 0.05, S["S23"] - 0.05, 66, 0.12, (91, 96, 93, 98, 88))
hit(S["S23"] + 0.02, 100); waltz(S["S23"], S["S23b"] - 0.05, "gold", 2); stab(T("d6", "safe") - 0.15, "C", 106, 0.8)
waltz(S["S23b"], S["S24"] - 0.05, "main", 1); n(T("d6", "chalky.") - 0.15, CL, 50, 80, 0.5); n(T("d6", "chalky.") + 0.2, CL, 48, 80, 0.6)
waltz(S["S24"], S["S25"] - 0.05, "sweet", 2); stab(T("e1", "Not") - 0.15, "E7", 100, 0.4)
waltz(S["S25"], S["S25b"] - 0.05, "sweet", 3); stab(T("e2", "cake.") - 0.15, "F", 106, 0.8, True); sparkle(T("e2", "cake.") - 0.1, 84, 7, 92)
waltz(S["S25b"], S["S26"] - 0.05, "main", 2)
waltz(S["S26"], S["S27"] - 0.05, "gold", 3)
for j, w in enumerate(("built", "mouth.", "bloom")): n(T("f1", w) - 0.15, GLK, (84, 88, 91)[j], 92, 0.5)
waltz(S["S27"], END - 1.6, "main", 2)
stab(END - 1.6, "C", 112, 1.6, True); hit(END - 1.6, 112); sparkle(END - 1.55, 84, 7)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 40, True)                 # brush kit
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((ACC, 58), (BS, 64), (GT, 76), (CL, 46), (PZ, 82), (CEL, 72), (GLK, 88), (BRS, 52), (PAD, 64)): syn.control_change(ch, 10, pan)
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
    """varispeed slow-down (the band 'cools'): speed falls from 1 to `floor` over dur, then the segment fades."""
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = 1 - (1 - floor) * np.linspace(0, 1, L) ** 1.4
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.4, L)[:, None]
    x[i0:i0 + L] = seg


for t0, d in SLOW: ritard(mus, t0, d)
mus = signal.sosfilt(signal.butter(2, 9000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
