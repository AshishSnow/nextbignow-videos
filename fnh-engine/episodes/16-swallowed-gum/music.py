"""BUBBLEGUM SKA score for FreshNestHub 16 "does swallowed gum stay in your stomach for 7 years?" (GeneralUser GS): a bouncy 2-tone
ska at 160 bpm — off-beat guitar 'skank' chops + bubbly organ on the 'and', walking bass, rim-shot drums, a trumpet + trombone horn
section for the hits. Story-following: already skanking at t=0 (the bubble), a horn blast on POP and GULP; minor + slow 'rocksteady'
half-time for the myth (7 years in the dark stomach) and the catch; the INSIDE-THE-GUT shots drop to a dubby half-time with echo
organ (the squeeze wave = a rising trombone swell); glockenspiel bubbles for sparkles; a big horn shout for HOUSEKEEPING, 40 HOURS and
BIN IT; a warm golden half-time for the Stone-Age twist; full band for the recap + a cadence sting. New genre for the channel (ska)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TPOP = T("i1", "gum") - 0.05; TGULP = T("i1", "swallow") + 0.05

GTR, ORG, BS, TPT, TBN, GLK, PAD, SAX, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {GTR: 27, ORG: 17, BS: 33, TPT: 56, TBN: 57, GLK: 9, PAD: 89, SAX: 65}
VOL = {GTR: 86, ORG: 74, BS: 110, TPT: 88, TBN: 88, GLK: 84, PAD: 60, SAX: 80, DR: 82}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 160.0
CH = {"C": (36, [60, 64, 67]), "F": (41, [60, 65, 69]), "G": (43, [59, 62, 67]), "Am": (33, [60, 64, 69]), "Dm": (38, [62, 65, 69]),
      "E7": (40, [59, 62, 68]), "Em": (40, [59, 64, 67]), "Bb": (46, [58, 62, 65])}
PROGS = {"main": ["C", "F", "G", "C"], "lift": ["F", "G", "C", "Am"], "minor": ["Am", "Dm", "E7", "Am"], "gut": ["Am", "F", "C", "G"],
         "gold": ["C", "Em", "F", "G"]}
MEL = {"C": [72, 76, 79, 76], "F": [72, 77, 81, 77], "G": [71, 74, 79, 74], "Am": [72, 76, 81, 76], "Dm": [74, 77, 81, 77],
       "E7": [71, 74, 80, 74], "Em": [71, 76, 79, 76], "Bb": [70, 74, 77, 74]}


def ska(t0, t1, prog="main", level=2, half=False):
    """level 1: drums + bass + skank; 2: + organ bubble; 3: + horn riff. half=True: rocksteady / dub half-time."""
    bt = BEAT * (2 if half else 1); bar = 4 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * bt
            if tq >= t1 - 0.05: break
            n(tq, BS, root + (0, 7, 12, 7)[q], 100 if q == 0 else 84, bt * 0.8)
            n(tq, DR, 42, 50, 0.1)
            if q in (1, 3): n(tq, DR, 37 if not half else 38, 70, 0.1)
            if q == 0 and not half: n(tq, DR, 36, 80, 0.2)
            if half and q == 2: n(tq, DR, 36, 84, 0.2)
            off = tq + bt / 2
            if off < t1 - 0.05:
                for j, k in enumerate(vo): n(off + 0.004 * j, GTR, k, 78, bt * 0.18)
                if level >= 2:
                    for k in vo: n(off, ORG, k - 12, 50, bt * 0.22)
                    if half: n(off + bt * 0.25, ORG, vo[-1], 30, bt * 0.15)
        if level >= 3 and b % 2 == 0:
            for j, k in enumerate(MEL[ch]):
                tj = t + j * bt * 0.75
                if tj < t1 - 0.05: n(tj, TPT, k, 84, bt * 0.6); n(tj, TBN, k - 12, 72, bt * 0.6)
        t += bar; b += 1


def horn(t, chord="C", v=104, d=0.5):
    root, vo = CH[chord]
    for k in vo: n(t, TPT, k + 12, v, d); n(t, TBN, k, v - 10, d)
    n(t, BS, root + 12, 110, d); n(t, DR, 49, v - 20, 1.2); n(t, DR, 36, v, 0.2)


def swell(t, d=0.8, chord="Am", v=80):
    root, vo = CH[chord]
    for i in range(6):
        for k in vo[:2]: n(t + i * d / 6, TBN, k - 12 + i, v - 20 + 6 * i, d / 6)


def bubbles(t, base=84, nn=6, v=86):
    for i in range(nn): n(t + i * 0.06, GLK, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.4)


def pad(t0, t1, keys=(57, 60, 64), v=46):
    for k in keys: n(t0, PAD, k, v, max(0.2, t1 - t0))


def hit(t, v=110): n(t, DR, 57, v - 30, 1.4); n(t, DR, 36, v, 0.3)


SLOW = []
ska(0.0, S["S1"] - 0.05, "main", 2); bubbles(0.2, 79, 4, 70); horn(TPOP, "F", 106, 0.4); bubbles(TPOP + 0.05, 86, 6, 92)
horn(TGULP, "G", 108, 0.6); n(TGULP, BS, 31, 110, 0.6)
ska(S["S1"], S["S2"] - 0.05, "minor", 1, True); pad(S["S1"], S["S2"], (57, 60, 64), 50)
for j in range(6): n(S["S1"] + 0.4 + 0.45 * j, GLK, 88 - 2 * j, 64, 0.3)
horn(T("i2", "seven") - 0.1, "E7", 100, 0.7)
horn(T("i3", "myth.") - 0.05, "C", 110, 0.5); ska(S["S2"], S["S2b"] - 0.05, "main", 2)
ska(S["S2b"], S["S3"] - 0.05, "minor", 1, True); pad(S["S2b"], S["S3"], (57, 64, 69), 46); swell(T("i3", "six") - 0.6, 0.6, "Am", 84)
hit(S["S3"] + 0.05, 100); ska(S["S3"], S["S4"] - 0.05, "main", 2)
ska(S["S4"], S["S5"] - 0.05, "lift", 2); bubbles(T("a2", "digests") + 0.2, 84, 6)
ska(S["S5"], S["S6"] - 0.05, "main", 3); horn(T("a3", "called") - 0.1, "C", 104, 0.5)
ska(S["S6"], S["S6b"] - 0.05, "lift", 1)
ska(S["S6b"], S["S7"] - 0.05, "main", 1); bubbles(S["S6b"] + 0.7, 79, 7, 70)
ska(S["S7"], S["S7b"] - 0.05, "minor", 1); n(T("a5", "break") - 0.15, TBN, 43, 100, 0.6)
ska(S["S7b"], S["S8"] - 0.05, "lift", 2)
ska(S["S8"], S["S9"] - 0.05, "gut", 2, True); pad(S["S8"], S["S9"], (57, 60, 64), 52)
hit(S["S9"] + 0.02, 100); ska(S["S9"], S["S10"] - 0.05, "minor", 1, True); horn(T("b1", "stuck") - 0.15, "E7", 100, 0.5)
ska(S["S10"], S["S11"] - 0.05, "gut", 2, True); swell(S["S10"] + 0.5, 2.5, "Am", 84)
ska(S["S11"], S["S11b"] - 0.05, "main", 1)
ska(S["S11b"], S["S12"] - 0.05, "main", 2); n(T("b3", "squeezes") - 0.1, TBN, 48, 96, 0.4); n(T("b3", "relaxes") - 0.1, TPT, 79, 80, 0.5)
ska(S["S12"], S["S12b"] - 0.05, "lift", 2)
ska(S["S12b"], S["S13"] - 0.05, "gut", 2, True); horn(T("b4", "peristalsis.") - 0.2, "Am", 104, 0.8)
ska(S["S13"], S["S14"] - 0.05, "main", 2)
ska(S["S14"], S["S14b"] - 0.05, "gut", 2, True); swell(S["S14"] + 0.3, 2.6, "Am", 90)
ska(S["S14b"], S["S15"] - 0.05, "main", 1)
ska(S["S15"], S["S15b"] - 0.05, "main", 3); horn(T("b7", "housekeeping") - 0.15, "C", 110, 0.8)
ska(S["S15b"], S["S16"] - 0.05, "lift", 2)
ska(S["S16"], S["S16b"] - 0.05, "minor", 1, True); bubbles(S["S16"] + 0.1, 84, 5)
ska(S["S16b"], S["S17"] - 0.05, "minor", 1, True)
for j in range(4): n(T("b8", "growls") - 0.15 + 0.12 * j, TBN, 36 + (j % 2), 110, 0.15)
hit(S["S17"] + 0.02, 100); ska(S["S17"], S["S18"] - 0.05, "main", 2)
ska(S["S18"], S["S19"] - 0.05, "gut", 2, True)
ska(S["S19"], S["S19b"] - 0.05, "main", 3); horn(T("c3", "forty") - 0.2, "G", 104, 0.5)
ska(S["S19b"], S["S20"] - 0.05, "lift", 2)
ska(S["S20"], S["S20b"] - 0.05, "minor", 1); swell(S["S20"] + 0.2, 1.4, "E7", 90)
ska(S["S20b"], S["S21"] - 0.05, "main", 3); horn(T("c4", "forty.") - 0.2, "C", 112, 0.9); bubbles(T("c4", "forty.") - 0.1, 84, 7)
hit(S["S21"] + 0.02, 104); ska(S["S21"], S["S22"] - 0.05, "minor", 1, True); pad(S["S21"], S["S24"], (57, 60, 64), 50)
ska(S["S22"], S["S23"] - 0.05, "minor", 1, True)
ska(S["S23"], S["S23b"] - 0.05, "minor", 1, True); horn(T("d3", "blocks") - 0.15, "E7", 108, 0.8); SLOW.append((T("d3", "blocks") - 0.5, 0.5))
ska(S["S23b"], S["S24"] - 0.05, "minor", 1, True)
ska(S["S24"], S["S24b"] - 0.05, "main", 3); horn(T("d4", "bin.") - 0.15, "C", 110, 0.6)
ska(S["S24b"], S["S25"] - 0.05, "lift", 1)
hit(S["S25"] + 0.02, 100); ska(S["S25"], S["S26"] - 0.05, "minor", 1, True); bubbles(S["S25"] + 1.2, 84, 6)
ska(S["S26"], S["S26b"] - 0.05, "gold", 2, True); pad(S["S26"], S["S28"], (60, 64, 67), 46)
ska(S["S26b"], S["S27"] - 0.05, "gold", 3, True); horn(T("e2", "years") - 0.2, "C", 108, 1.0)
ska(S["S27"], S["S27b"] - 0.05, "gold", 2, True)
ska(S["S27b"], S["S28"] - 0.05, "gold", 2, True); bubbles(T("e3", "complete") - 0.15, 84, 7)
ska(S["S28"], S["S29"] - 0.05, "main", 3); horn(T("e4", "stuck") - 0.15, "F", 106, 0.5)
ska(S["S29"], S["S30"] - 0.05, "main", 3)
for j, w in enumerate(("can't", "moves", "two")): n(T("f1", w) - 0.15, GLK, (84, 88, 91)[j], 92, 0.5)
ska(S["S30"], END - 1.6, "lift", 2)
horn(END - 1.6, "C", 114, 1.6); hit(END - 1.6, 112); bubbles(END - 1.55, 84, 7)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 84), (ORG, 44), (BS, 64), (TPT, 52), (TBN, 76), (GLK, 90), (PAD, 64), (SAX, 40)): syn.control_change(ch, 10, pan)
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
