"""Score for FreshNestHub ep04 (tattoo ink cells). Based on ep03 'a fungus is eating your scalp' (Malassezia, Nessa). Adapted from ep02: — glam-pop mystery hook, bouncy groove for facts,
music-box whisper for 'females... dried... crushed', big hit on 'crushed', disco-ish count, hard stop on 'but wait',
dark pulse for allergies, warm groove for the tip, soft music box loop."""
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
CH.update({"Gm": (43, [62, 67, 70]), "Em": (40, [59, 64, 67])})


def musicbox(t0, t1, seq, vel=70, step=None):
    step = step or BEAT / 2
    t = t0; i = 0
    while t < t1 - 0.05:
        root, tri = CH[seq[int((t - t0) / BAR) % len(seq)]]
        n(t, CEL, [tri[0] + 12, tri[2] + 12, tri[1] + 12, tri[2] + 12][i % 4], vel - (8 if i % 2 else 0), step * 1.6)
        t += step; i += 1


def disco(t0, t1, seq):
    t = t0; b = 0
    while t < t1 - 0.05:
        root, tri = CH[seq[b % len(seq)]]
        for q in range(8):
            tt = t + q * BEAT / 2
            if tt >= t1 - 0.02: break
            if q % 2 == 0: n(tt, DR, 36, 118, 0.2)
            else: n(tt, DR, 46, 84, 0.12)
            if q in (2, 6): n(tt, DR, 39, 104, 0.2)
            n(tt, BASS, root + (12 if q % 2 else 0), 104 if q % 2 == 0 else 90, BEAT * 0.4)
        for q in (0.5, 1.5, 2.5, 3.5):
            if t + q * BEAT < t1 - 0.02:
                for kk in tri: n(t + q * BEAT, STR, kk, 74, BEAT * 0.3)
        for kk in tri: n(t, BRASS, kk, 86, BEAT * 0.5)
        t += BAR; b += 1


# ---- intro: mysterious tension -> EATEN hit ----
hit(0.0, 104, crash=False)
tension(0.05, E["t_eaten0"] - 0.08, 45, tick=True, pulse=False)
for i, kk in enumerate((69, 72, 76, 72, 74, 71)):
    n(0.15 + i * BEAT / 2, CEL, kk, 80, 0.4)
riser(E["t_eaten0"] - 0.05, 0.9)
braam(E["t_eaten0"] - 0.05, minor=True)
for kk in (81, 84, 88): n(E["t_own"] - 0.03, GLOCK, kk, 84, 0.9)
# ---- name: bouncy, curious ----
groove(S_["AN"] + 0.02, S_["ND"] - 0.05, ["Am", "F", "C", "G"], 2)
hit(E["t_macro"] - 0.03, 110, crash=True)
for i, kk in enumerate((72, 76, 79, 84)): n(E["t_holding"] - 0.05 + i * 0.07, GLOCK, kk, 84, 0.6)
# ---- steps 1-2 (needle, shedding): driving but light ----
groove(S_["ND"] + 0.02, S_["IV"] - 0.05, ["C", "G", "Am", "F"], 2)
hit(E["t_dermis"] - 0.03, 112, crash=True)
for i, kk in enumerate((72, 76, 79, 84, 88)): n(E["t_sheds"] - 0.05 + i * 0.06, GLOCK, kk, 80, 0.6)
hit(E["t_stays"] - 0.03, 96, crash=False)
# ---- invader: dark pulse ----
tension(S_["IV"] + 0.05, E["t_sends"] - 0.1, 40, tick=True, pulse=True)
hit(E["t_invader"] - 0.03, 112, crash=False)
groove(E["t_sends"] - 0.05, S_["SW"] - 0.05, ["Am", "G"], 2)
# ---- swallow / hold: cheeky groove ----
groove(S_["SW"] + 0.02, S_["SE"] - 0.05, ["F", "C", "Dm", "G"], 2)
hit(E["t_cant"] - 0.03, 98, crash=False)
for kk in (79, 84, 88): n(E["t_hold"] - 0.03, GLOCK, kk, 80, 0.9)
# ---- the tattoo you see: big groove ----
groove(S_["SE"] + 0.02, S_["WT"] - 0.05, ["Am", "F", "C", "E"], 3)
hit(E["t_see"] - 0.03, 118, crash=True)
# ---- but wait: hard stop, sly pizz + clock ticks ----
hit(E["t_wait"] - 0.03, 102, crash=False)
t_ = E["t_wait"] + 0.3; i_ = 0
while t_ < S_["DI"] - 0.1:
    n(t_, PIZ, [57, 60, 64, 63, 62, 60][i_ % 6], 82, 0.25); n(t_, WOOD, 76 if i_ % 2 else 77, 60, 0.05); t_ += BEAT / 2; i_ += 1
# ---- dies: music box whisper, no drums ----
for kk in (57, 64, 69): n(S_["DI"] + 0.05, PAD, kk, 58, S_["RC"] - S_["DI"] + 0.3)
musicbox(S_["DI"] + 0.1, S_["RC"] - 0.1, ["Am", "F", "Am", "E"], vel=56)
n(E["t_spills"] - 0.05, TREM, 57, 62, 1.2); n(E["t_spills"] - 0.05, TREM, 63, 56, 1.2)
# ---- recapture: big bright groove ----
groove(S_["RC"] + 0.02, S_["MC"] - 0.05, ["C", "G", "Am", "F"], 3)
hit(E["t_gobbles"] - 0.03, 116, crash=True)
for i, kk in enumerate((72, 76, 79, 84, 88)): n(E["t_back"] - 0.05 + i * 0.06, GLOCK, kk, 86, 0.6)
# ---- mice + lymph: curious ----
groove(S_["MC"] + 0.02, S_["LY"] - 0.05, ["F", "C", "Dm", "G"], 1)
for kk in (84, 88, 91): n(E["t_twenty"] - 0.03, GLOCK, kk, 84, 1.0)
groove(S_["LY"] + 0.02, S_["TP"] - 0.05, ["Am", "F", "C", "G"], 2)
hit(E["t_lymph"] - 0.03, 104, crash=False)
# ---- tip: warm ----
groove(S_["TP"] + 0.02, S_["LP"] - 0.05, ["F", "C", "Dm", "Bb"], 1)
for kk in (84, 88, 91): n(E["t_studio"] - 0.03, GLOCK, kk, 84, 1.0)
for kk in (84, 88, 91): n(E["t_heal"] - 0.03, GLOCK, kk, 84, 1.0)
# ---- loop: soft music box ----
for kk in (52, 57, 60): n(S_["LP"] + 0.05, PAD, kk, 56, END - S_["LP"] + 0.4)
musicbox(S_["LP"] + 0.1, END, ["Am", "Am", "F", "E"], vel=52, step=BEAT / 2)
hit(E["t_now"] - 0.03, 94, crash=False)


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


# hard stops: whisper, but wait, loop
mus = np.zeros((int((END + 3) * SR), 2), np.float32)
cuts = [0.0, E["t_wait"] - 0.05, S_["DI"], S_["RC"], S_["LP"], END + 3]
evs = sorted(ev)
for a, b in zip(cuts[:-1], cuts[1:]):
    part = render([e for e in evs if a - 0.01 <= e[0] < b - 0.01], END, PROG, VOL)
    nb = int(b * SR); tail = int(0.12 * SR)
    if nb < len(part):
        part[nb:nb + tail] *= np.linspace(1, 0, min(tail, len(part) - nb))[:, None] ** 2; part[nb + tail:] = 0
    mus[: len(part)] += part[: len(mus)]


def crash():
    syn = tinysoundfont.Synth(samplerate=SR, gain=-6); sid = syn.sfload(SF2); syn.program_select(9, sid, 128, 0, True); syn.noteon(9, 49, 120)
    return np.frombuffer(syn.generate(int(2.0 * SR)), np.float32).reshape(-1, 2).copy()


rev = crash()[::-1]
for te, g in ((E["t_eaten0"], 0.5), (E["t_see"], 0.45), (E["t_gobbles"], 0.4)):
    a = int(te * SR) - len(rev)
    if a >= 0: mus[a:a + len(rev)] += rev * g
rng = np.random.default_rng(4); irl = int(2.0 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.45)[:, None]; ir[: int(0.015 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, 5000, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.22 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.5) / np.tanh(1.5)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.25 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2), "rms", round(float(np.sqrt(np.mean(mus ** 2))), 4))
