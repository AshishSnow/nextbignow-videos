"""LO-FI HIP-HOP CAFE score for FreshNestHub 14 "coffee doesn't give you energy" (GeneralUser GS): a sleepy coffee-shop
boom-bap beat (84 BPM, swung 16ths), Rhodes electric piano 7th/9th chords (Fmaj7 Em7 Dm7 Cmaj7), round upright bass, a
music-box/celesta motif for the SLEEPY keys, muted-trumpet answers, flute for the bees bonus, vinyl crackle + gentle wow.
Story-following: beat already rolling at t=0 (coffee), a TAPE STOP (the whole band slows down and drops in pitch) on the
'fake' battery reveal and again on THE CRASH (new sound skill, ep 14: varispeed slow-down of the rendered music); the band
drops to Rhodes + bass under explanation lines (coherence), the music box takes over whenever the sleepy keys are on screen,
the beat comes back for the fake-key trick, bright flute + vibes for the bees, full band for the takeaway + sting."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

EP, BS, MB, TP, FL, VB, PAD, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {EP: 4, BS: 32, MB: 10, TP: 59, FL: 73, VB: 11, PAD: 89, SUB: 38}
VOL = {EP: 100, BS: 112, MB: 90, TP: 80, FL: 84, VB: 86, PAD: 60, SUB: 90, DR: 92}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BPM = 84; BEAT = 60 / BPM; SW = 0.58          # swing ratio for 8ths
CH = {"F": (41, [57, 60, 64, 67]), "Em": (40, [55, 59, 62, 67]), "Dm": (38, [53, 57, 60, 64]), "C": (36, [55, 59, 62, 64]),
      "Bb": (46, [58, 62, 65, 69]), "A7": (45, [55, 61, 64, 67])}
PROGS = {"cafe": ["F", "Em", "Dm", "C"], "sleep": ["F", "Dm", "Bb", "C"], "tense": ["Dm", "A7", "Dm", "A7"], "bright": ["F", "C", "Dm", "C"]}
BASSL = {"F": [41, 48, 45, 43], "Em": [40, 47, 43, 42], "Dm": [38, 45, 41, 40], "C": [36, 43, 40, 38], "Bb": [46, 41, 45, 43], "A7": [45, 40, 43, 44]}
BOX = [72, 76, 79, 76, 74, 77, 81, 77]
HOOKM = [72, 74, 76, 79, 77, 76, 74, 72]


def sw(t0, i):            # swung 8th position
    return t0 + (i // 2) * BEAT + (0 if i % 2 == 0 else BEAT * SW)


def band(t0, t1, prog="cafe", level=2):
    """level 1: Rhodes + bass; 2: + boom-bap drums; 3: + muted trumpet answer (or flute in 'bright')."""
    bar = 4 * BEAT; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in (0, 2.5):
            tq = t + q * BEAT
            if tq < t1 - 0.05:
                for j, k in enumerate(vo): n(tq + 0.012 * j, EP, k, 70 if q else 78, (1.4 if q == 0 else 1.0) * BEAT)
        for q in range(4):
            tq = t + q * BEAT
            if tq < t1 - 0.05 and q in (0, 2, 3): n(tq, BS, BASSL[ch][q] - 12 + 12, 100 if q == 0 else 84, BEAT * 0.8)
        if level >= 2:
            for i in range(8):
                ti = sw(t, i)
                if ti < t1 - 0.03: n(ti, DR, 42, 46 + 12 * (i % 2 == 0), 0.06)
            for ti in (t, t + 2.5 * BEAT):
                if ti < t1 - 0.03: n(ti, DR, 36, 104, 0.2)
            for ti in (t + BEAT, t + 3 * BEAT):
                if ti < t1 - 0.03: n(ti, DR, 38, 86, 0.15); n(ti, DR, 37, 50, 0.1)
        if level >= 3:
            mel = HOOKM if prog != "bright" else [k + 5 for k in HOOKM]
            chn = TP if prog != "bright" else FL
            for j, k in enumerate(mel[(b % 2) * 4:(b % 2) * 4 + 4]):
                tj = t + (j * 1.0 + 0.5) * BEAT
                if tj < t1 - 0.05: n(tj, chn, k, 82, BEAT * 0.7)
        t += bar; b += 1


def box(t0, t1, v=74, spd=0.5):
    i = 0; t = t0
    while t < t1 - 0.05:
        n(t, MB, BOX[i % 8], v, 0.6); t += BEAT * spd; i += 1


def pad(t0, t1, keys=(53, 57, 60, 64), v=46):
    for k in keys: n(t0, PAD, k, v, max(0.2, t1 - t0))


def hit(t, v=110, big=False):
    n(t, DR, 49, v - 20, 1.4); n(t, DR, 36, v, 0.3); n(t, BS, 29 + 12, v, 0.4)
    if big: n(t, SUB, 29, 104, 1.0)


def stab(t, chord="Dm", v=100, d=0.35):
    root, vo = CH[chord]
    for k in vo: n(t, EP, k + 12, v - 10, d); n(t, VB, k + 12, v - 20, d)
    n(t, BS, root, 110, d)


def sparkle(t, base=84, nn=6, v=84):
    for i in range(nn): n(t + i * 0.05, VB, base + (0, 4, 7, 11, 12, 16, 19)[i % 7], v, 0.5)


TD = T("i1", "doesn't") - 0.1
TSTOP = []                      # (t0, dur) tape stops applied after rendering
# hook: beat rolling at t=0 (the gulp), tape stop into the FAKE reveal
band(0.0, TD - 0.02, "cafe", 2); TSTOP.append((TD - 0.55, 0.55))
stab(TD + 0.25, "A7", 104, 0.5); n(TD + 0.25, DR, 49, 90, 1.2)
band(S["S1"], S["S1b"] - 0.05, "tense", 1); hit(T("i2", "bit.") - 0.15, 104)
band(S["S1b"], S["S2"] - 0.05, "sleep", 1); box(T("i2", "hides") - 0.1, S["S2"] - 0.05, 66, 1.0)
band(S["S2"], S["S3"] - 0.05, "tense", 2); stab(T("i3", "back") - 0.15, "Dm", 102); stab(T("i3", "interest.") - 0.2, "A7", 104)
# PART 1: the sleepy signal (soft, music box for the sleepy keys)
hit(S["S3"] + 0.05, 98); band(S["S3"], S["S4"] - 0.05, "cafe", 1)
for j in range(6): n(T("a1", "All") - 0.25 + j * 0.13, VB, 96 - j * 3, 70, 0.25)          # the zoom-in dive
band(S["S4"], S["S5"] - 0.05, "sleep", 1); box(S["S4"] + 0.3, S["S5"] - 0.05, 62, 0.5)
band(S["S5"], S["S5b"] - 0.05, "sleep", 1); box(S["S5"], S["S5b"] - 0.05, 78, 0.5); sparkle(T("a3", "keys.") - 0.2, 84, 5)
band(S["S5b"], S["S6"] - 0.05, "sleep", 1); box(S["S5b"], S["S6"] - 0.05, 66, 1.0); pad(S["S5b"], S["S6"] - 0.05)
band(S["S6"], S["S6b"] - 0.05, "cafe", 1); n(T("a4", "locks") - 0.2, VB, 84, 90, 0.4)
band(S["S6b"], S["S6c"] - 0.05, "cafe", 1); stab(T("a5", "clicks") - 0.12, "C", 100, 0.2)
pad(T("a5", "slows") - 0.15, S["S7"] - 0.05, (53, 57, 60), 50)
for j in range(5): n(S["S6c"] + 0.1 + j * 0.25, MB, 79 - 3 * j, 70, 0.5)                    # yawn glide
band(S["S7"], S["S8"] - 0.05, "sleep", 1); box(S["S7"], S["S8"] - 0.05, 70, 1.0)
# PART 2: the fake key (beat returns; the trick)
hit(S["S8"] + 0.02, 104); band(S["S8"], S["S9"] - 0.05, "cafe", 2); sparkle(T("b1", "coffee.") - 0.1, 86, 5)
band(S["S9"], S["S10"] - 0.05, "cafe", 1)
band(S["S10"], S["S11"] - 0.05, "tense", 2); stab(T("b3", "like") - 0.15, "A7", 106, 0.4)
band(S["S11"], S["S12"] - 0.05, "tense", 1); n(T("b4", "can't") - 0.15, BS, 45, 110, 0.15); n(T("b4", "can't") + 0.05, BS, 44, 110, 0.15); n(T("b4", "can't") + 0.25, BS, 43, 110, 0.4)
band(S["S12"], S["S13"] - 0.05, "cafe", 2); hit(T("b5", "blocking") - 0.15, 108)
band(S["S13"], S["S13b"] - 0.05, "cafe", 2)
band(S["S13b"], S["S14"] - 0.05, "bright", 3); sparkle(S["S13b"] + 0.05, 86, 7)
band(S["S14"], S["S15"] - 0.05, "cafe", 1)
# PART 3: the crash (piling tension, then tape stop)
hit(S["S15"] + 0.02, 100); band(S["S15"], S["S16"] - 0.05, "tense", 1)
band(S["S16"], S["S17"] - 0.05, "tense", 2); box(S["S16"], S["S17"] - 0.05, 72, 0.25)
band(S["S17"], S["S18"] - 0.05, "tense", 2); hit(T("c3", "rush") - 0.15, 116, True)
TCR = T("c4", "crash.") - 0.05
band(S["S18"], TCR, "cafe", 2); TSTOP.append((TCR - 0.8, 0.8)); hit(TCR + 0.1, 110, True); band(TCR + 0.5, S["S18b"] - 0.05, "sleep", 1)
band(S["S18b"], S["S19"] - 0.05, "sleep", 1)
# PART 4: how long (clock ticks), the study, the takeaway
hit(S["S19"] + 0.02, 100); band(S["S19"], S["S20"] - 0.05, "cafe", 2)
for j in range(int((S["S20"] - S["S19"]) / 0.5)): n(S["S19"] + 0.25 + j * 0.5, DR, 76 if j % 2 else 77, 70, 0.1)
band(S["S20"], S["S21"] - 0.05, "cafe", 1)
band(S["S21"], S["S22"] - 0.05, "sleep", 1); box(S["S21"] + 0.2, S["S22"] - 0.05, 60, 1.0)
band(S["S22"], S["S23"] - 0.05, "sleep", 1); pad(S["S22"], S["S23"] - 0.05, (50, 57, 62), 44)
band(S["S23"], S["S23b"] - 0.05, "tense", 1); hit(T("d5", "hour") - 0.1, 108)
band(S["S23b"], S["S24"] - 0.05, "cafe", 2); n(T("d5", "notice!") - 0.1, TP, 67, 90, 0.3); n(T("d5", "notice!") + 0.2, TP, 66, 90, 0.5)
band(S["S24"], S["S25"] - 0.05, "bright", 2); sparkle(T("d6", "earlier") + 0.3, 86, 6)
# PART 5: every day -> bees bonus (bright flute)
hit(S["S25"] + 0.02, 100); band(S["S25"], S["S26"] - 0.05, "cafe", 2)
band(S["S26"], S["S26b"] - 0.05, "cafe", 1); sparkle(T("e2", "extra") - 0.2, 82, 6)
band(S["S26b"], S["S27"] - 0.05, "tense", 2); stab(T("e2b", "more") - 0.15, "A7", 104)
hit(S["S27"] + 0.02, 104); band(S["S27"], S["S30b"] - 0.05, "bright", 3)
for j in range(10): n(S["S27"] + 0.3 + j * 0.09, FL, 84 + (j % 2), 60, 0.09)                  # buzz trill
sparkle(T("e5", "three") - 0.3, 88, 7)
band(S["S30b"], S["S31"] - 0.05, "cafe", 2); n(T("e6", "familiar?") - 0.1, TP, 72, 90, 0.3); n(T("e6", "familiar?") + 0.2, TP, 76, 90, 0.6)
band(S["S31"], S["S32"] - 0.05, "sleep", 1)
for j, w in enumerate(("add", "blocks", "waits")): n(T("f1", w) - 0.15, VB, (84, 88, 91)[j], 100, 0.6)
band(S["S32"], END - 1.6, "cafe", 3)
stab(END - 1.6, "F", 110, 1.6); hit(END - 1.6, 112, True); sparkle(END - 1.55, 84, 7)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((EP, 52), (BS, 64), (MB, 86), (TP, 44), (FL, 80), (VB, 76), (PAD, 64)): syn.control_change(ch, 10, pan)
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


# TAPE STOP (new sound skill, ep 14): read the music back at a speed that falls from 1 to ~0 over `dur` (pitch + tempo drop
# together, like a turntable losing power), then silence until the next event's onset.
def tape_stop(x, t0, dur):
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = (1 - np.linspace(0, 1, L)) ** 1.6
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.3, L)[:, None]
    x[i0:i0 + L] = seg
    nxt = min(len(x), i0 + L + int(0.12 * SR))
    x[i0 + L:nxt] *= 0.0


for t0, d in TSTOP: tape_stop(mus, t0, d)
# lo-fi colour: gentle low-pass, slow wow (pitch wobble via tiny delay modulation), vinyl crackle
mus = signal.sosfilt(signal.butter(2, 7000, "low", fs=SR, output="sos"), mus, axis=0)
tt = np.arange(len(mus)) / SR; dl = (0.0012 * (1 + np.sin(2 * np.pi * 0.5 * tt))) * SR
idx = np.clip(np.arange(len(mus)) - dl, 0, len(mus) - 1)
mus = np.stack([np.interp(idx, np.arange(len(mus)), mus[:, c]) for c in (0, 1)], 1)
rng = np.random.default_rng(14)
crk = (rng.random(len(mus)) < 0.0009) * rng.uniform(-1, 1, len(mus)); crk = signal.sosfilt(signal.butter(2, 1500, "high", fs=SR, output="sos"), crk)
hiss_ = signal.sosfilt(signal.butter(2, [2000, 8000], "band", fs=SR, output="sos"), rng.standard_normal(len(mus))) * 0.004
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.3) / np.tanh(1.3)
mus = mus + (0.05 * crk + hiss_)[:, None]
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
