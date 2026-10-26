"""Score for BODY FILES 05 knuckle crack — calm documentary piano + tension build + reveals; base helpers from FreshNestHub 'face mites' (Nessa) — creepy-cute mystery, sunny groove, music-box night, disco party; was: 'Whale vomit / ambergris' — adventure + mystery;
based on the water score — bright, bouncy, high-energy (GeneralUser GS):
tense ticking hook -> riser -> burst hit; pop groove (marimba / pizz / synth bass / claps) for the facts;
hard stops on the re-hooks ('But wait', 'what if you DON'T', 'don't go crazy'); dark pulse for the danger parts; big major finish."""
import json, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
R = "/home/claude/reel-kit"
B = f"{R}/english"
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"
SR = 48000
TL = json.load(open(f"{B}/work/timeline.json")); EV = TL["events"]; S = {s["id"]: s for s in TL["shots"]}; END = TL["END"]
BPM = 120.0; BEAT = 60 / BPM; BAR = 4 * BEAT
MAR, PIZ, STR, TREM, BASS, BRASS, CHOIR, GLOCK, TAIKO, TIMP, PAD, SBRASS, WOOD, CEL = range(14)
DR = 9
PROG = {MAR: 12, PIZ: 45, STR: 48, TREM: 44, BASS: 38, BRASS: 61, CHOIR: 52, GLOCK: 9, TAIKO: 116, TIMP: 47, PAD: 89, SBRASS: 62, WOOD: 115, CEL: 8}
VOL = {MAR: 108, PIZ: 100, STR: 92, TREM: 96, BASS: 104, BRASS: 112, CHOIR: 90, GLOCK: 86, TAIKO: 120, TIMP: 116, PAD: 84, SBRASS: 96, WOOD: 92,
       CEL: 90, DR: 108}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


CH = {"C": (36, [60, 64, 67]), "G": (43, [59, 62, 67]), "Am": (45, [60, 64, 69]), "F": (41, [60, 65, 69]), "Dm": (38, [62, 65, 69]),
      "E": (40, [59, 64, 68]), "Cm": (36, [60, 63, 67]), "Ab": (44, [60, 63, 68]), "Bb": (46, [62, 65, 70]), "Fm": (41, [60, 65, 68])}


def hit(t, v=120, crash=True):
    n(t, TAIKO, 41, v, 1.2); n(t, TIMP, 36, v - 6, 1.8); n(t, DR, 36, v, 0.3)
    if crash: n(t, DR, 49, v - 10, 2.5)


def braam(t, minor=True):
    for k in ((36, 43, 48, 51) if minor else (36, 43, 48, 52)): n(t, BRASS, k, 122, 2.0); n(t, SBRASS, k + 12, 100, 1.8)
    hit(t, 124)


def riser(t_end, dur):
    steps = [48, 51, 55, 58, 60, 63, 67, 70]
    for i, p in enumerate(steps):
        t = t_end - dur + i * dur / len(steps); n(t, TREM, p, 64 + 7 * i, t_end - t)
    m = int(dur / (BEAT / 4))
    for j in range(m): n(t_end - dur + j * BEAT / 4, DR, 38, 30 + int(85 * (j / m) ** 1.6), 0.05)


def groove(t0, t1, seq, level=2, mar=True):
    b = 0; t = t0
    while t < t1 - 0.05:
        root, tri = CH[seq[b % len(seq)]]; dur = min(BAR, t1 - t)
        steps = int(dur / (BEAT / 2)) + 1
        arp = [tri[0], tri[1], tri[2], tri[1] + 12, tri[2], tri[1], tri[0] + 12, tri[2]]
        for i in range(steps):
            tt = t + i * BEAT / 2
            if tt >= t + dur - 0.02: break
            if mar: n(tt, MAR, arp[i % 8] + 12, 70 + (16 if i % 2 == 0 else 0), 0.3)
            n(tt, BASS, root - (0 if i % 4 != 3 else -12), 92 if i % 2 == 0 else 74, BEAT * 0.42)
            n(tt, DR, 42, 54 + (14 if i % 2 == 0 else 0), 0.05)
        for off in (0, 1.5, 2.5):
            if off * BEAT < dur and level >= 1: n(t + off * BEAT, PIZ, tri[0] - 12, 82, 0.2); n(t + off * BEAT, PIZ, tri[2] - 12, 76, 0.2)
        if level >= 2:
            for off in (0, 2, 2.5):
                if off * BEAT < dur: n(t + off * BEAT, DR, 36, 112 if off == 0 else 100, 0.2)
            for off in (1, 3):
                if off * BEAT < dur: n(t + off * BEAT, DR, 39, 96, 0.2); n(t + off * BEAT, DR, 38, 70, 0.2)
        if level >= 3:
            for k in tri: n(t, STR, k, 86, dur * 0.98); n(t, BRASS, k - 12, 84, BEAT * 0.9)
            n(t + 3.5 * BEAT, DR, 46, 70, 0.3) if 3.5 * BEAT < dur else None
        n(t, PAD, tri[0], 52 + 6 * level, dur * 0.95); n(t, PAD, tri[2], 48 + 6 * level, dur * 0.95)
        t += BAR; b += 1


def tension(t0, t1, root=36, tick=True, pulse=True):
    n(t0, TREM, root + 12, 66, t1 - t0); n(t0, TREM, root + 19, 56, t1 - t0); n(t0, PAD, root + 12, 60, t1 - t0)
    t = t0
    while t < t1 - 0.05:
        if tick: n(t, WOOD, 76 if int(round((t - t0) / (BEAT / 2))) % 2 == 0 else 77, 56, 0.05)
        t += BEAT / 2
    if pulse:
        t = t0
        while t < t1 - 0.1:
            n(t, DR, 36, 96, 0.2); n(t + 0.17, DR, 36, 72, 0.2); n(t, BASS, root, 84, 0.3); t += BEAT * 2




S_ = {k: S[k]["start"] for k in S}
E = EV
BPM = 100.0; BEAT = 60 / BPM; BAR = 4 * BEAT
PROG[MAR] = 0; VOL[MAR] = 100       # MAR channel = acoustic grand piano for this calm documentary score
VOL[PAD] = 78; VOL[STR] = 84


def piano(t0, t1, seq, vel=62, pat=(0, 2, 1, 2, 0, 2, 1, 2)):
    t = t0; b = 0
    while t < t1 - 0.05:
        root, tri = CH[seq[b % len(seq)]]
        notes = [tri[0], tri[1], tri[2], tri[0] + 12]
        for i, p in enumerate(pat):
            tt = t + i * BEAT / 2
            if tt >= t1 - 0.03: break
            n(tt, MAR, notes[p] + (12 if i % 4 == 3 else 0), vel + (8 if i % 4 == 0 else 0), BEAT * 0.9)
        n(t, MAR, root, vel - 4, BAR * 0.95); n(t, PAD, tri[0], 46, min(BAR, t1 - t) * 0.98); n(t, PAD, tri[2], 42, min(BAR, t1 - t) * 0.98)
        t += BAR; b += 1


def soft_hit(t, v=100):
    n(t, TIMP, 36, v, 1.4); n(t, DR, 36, v - 10, 0.3); n(t, PIZ, 45, v - 6, 0.4)


# intro + myth + joint + fluid: calm curious piano
piano(0.02, S_["PL"] - 0.02, ["Am", "F", "C", "G"], 60)
for kk in (81, 84, 88): n(E["t_crack0"] - 0.02, GLOCK, kk, 84, 0.6)
soft_hit(E["t_isnt"] - 0.03, 104)
for i, tt in enumerate((E["t_two"], E["t_capsule"], E["t_synovial"])):
    n(tt - 0.05, CEL, [84, 88, 91][i], 74, 0.6)
# pull + pressure: tension builds into the crack
tension(S_["PL"] + 0.02, E["t_crack"] - 0.05, 45, tick=True, pulse=False)
riser(E["t_crack"] - 0.04, 1.6)
hit(E["t_crack"] - 0.04, 114, crash=True)
for kk in (76, 79, 84): n(E["t_pocket"] - 0.05, GLOCK, kk, 80, 0.7)
# MRI + wait: light pulse under calm piano
piano(E["t_crack"] + 0.4, S_["QU"] - 0.05, ["F", "C", "Dm", "Am"], 56)
t_ = S_["MR"] + 0.1
while t_ < S_["WT"] - 0.1:
    n(t_, WOOD, 77, 46, 0.05); t_ += BEAT / 2
# question: hard stop, one low note + chime
n(S_["QU"] + 0.02, MAR, 33, 84, 2.0); n(S_["QU"] + 0.02, PAD, 45, 60, 2.2)
for kk in (76, 71): n(E["t_arthritis"] + 0.1 + (0 if kk == 76 else 0.25), CEL, kk, 78, 0.8)
# the doctor's experiment -> warm resolution
piano(S_["UN"] + 0.02, S_["NU"] - 0.05, ["C", "G", "Am", "F"], 64)
for kk in (60, 64, 67, 72): n(E["t_no"] - 0.05, STR, kk, 88, 2.6)
for i, kk in enumerate((84, 88, 91)): n(E["t_no"] + i * 0.08, GLOCK, kk, 88, 0.9)
soft_hit(E["t_no"] - 0.05, 96)
# the catch: softer minor
piano(S_["NU"] + 0.02, S_["TP"] - 0.05, ["Am", "F"], 52)
# tip: warm
piano(S_["TP"] + 0.02, S_["LP"] - 0.05, ["F", "C"], 58)
for kk in (84, 88, 91): n(E["t_talk"] - 0.03, GLOCK, kk, 84, 1.0)
# loop: intro motif returns
piano(S_["LP"] + 0.02, END, ["Am", "F"], 58)
for kk in (81, 84, 88): n(E["t_crack2"] - 0.02, GLOCK, kk, 84, 0.6)


def render(evts, dur, prog, vol, drums=True, drum_preset=0):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in prog.items(): syn.program_select(ch, sid, 0, p)
    if drums: syn.program_select(DR, sid, 128, drum_preset, True)
    for ch, v in vol.items(): syn.control_change(ch, 7, v)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = np.zeros((int((END + 3) * SR), 2), np.float32)
cuts = [0.0, S_["QU"], S_["UN"], END + 3]
evs = sorted(ev)
for a, b in zip(cuts[:-1], cuts[1:]):
    part = render([e for e in evs if a - 0.01 <= e[0] < b - 0.01], END, PROG, VOL)
    nb = int(b * SR); tail = int(0.12 * SR)
    if nb < len(part):
        part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]
rng = np.random.default_rng(4); irl = int(2.2 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.6)[:, None]; ir[: int(0.015 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 5000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.28 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.3) / np.tanh(1.3)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.25 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2), "rms", round(float(np.sqrt(np.mean(mus ** 2))), 4))
