"""TARANTELLA score for FreshNestHub 29 "why does garlic breath last so long?" (GeneralUser GS; new genre): a garlic-kitchen Italian folk dance in 6/8.
A minor (Am / E7 / Dm / G / C) at dotted-quarter 126 (one 6/8 bar = 0.952 s): mandolin-style tremolo melody (steel guitar re-struck 16ths), accordion chords on the off-beats,
tuba-ish bass on 1 and 4, tambourine + castanets, pizzicato strings.
FOLLOWS THE STORY: the garlic + the crush = the full tarantella; the chemistry (cell, meet, allicin) = pizzicato plucks that speed up into the 'falls apart' run;
AMS the sneaky gas = a tiptoe bassoon staccato motif (its own theme, comes back every time it moves); the lungs = the accordion BREATHING (slow bellows swells);
the lab test = a clockwork pizz + celesta tick, every food result gets its own chord; 'nothing at all' = a deflating trombone wah; recap + send = the band, triumphant."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
S = {k: st for k, st, _ in SHOTLIST}
MD, AC, BS, PZ, BN, CE, TB, STR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {MD: 25, AC: 21, BS: 58, PZ: 45, BN: 70, CE: 8, TB: 57, STR: 48}
VOL = {MD: 92, AC: 74, BS: 92, PZ: 88, BN: 92, CE: 80, TB: 84, STR: 62, DR: 82}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


E8 = 0.952 / 6                      # one eighth note in 6/8
BAR = 6 * E8
CH = {"Am": (45, [57, 60, 64]), "E7": (40, [56, 59, 62, 64]), "Dm": (38, [57, 62, 65]), "G": (43, [55, 59, 62]), "C": (48, [55, 60, 64]), "F": (41, [57, 60, 65])}
PROGS = {"tar": ["Am", "Am", "E7", "Am", "Dm", "Am", "E7", "Am"], "lift": ["C", "G", "Am", "E7"], "home": ["F", "C", "E7", "Am"]}
MEL = [(0, 76, 2), (2, 77, 1), (3, 76, 2), (5, 74, 1), (6, 72, 2), (8, 74, 1), (9, 76, 3), (12, 71, 2), (14, 72, 1), (15, 74, 2), (17, 72, 1), (18, 71, 2), (20, 69, 1), (21, 68, 3)]


def tremolo(t, k, v, dur):
    """mandolin: re-strike the note every 1/16 for its whole length."""
    q = 0.0; j = 0
    while q < dur - 0.02: n(t + q, MD, k, v - 8 * (j % 2), 0.07); q += E8 / 2; j += 1


def tarantella(t0, t1, prog="tar", level=3, mel=True):
    """level 1: bass + tambourine. 2: + accordion off-beats. 3: + mandolin tremolo melody + castanets."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % len(PROGS[prog])]; root, vo = CH[ch]
        for e in range(6):
            te = t + e * E8
            if te >= t1: break
            if e in (0, 3): n(te, BS, root - 12 + (7 if e == 3 else 0), 96 if e == 0 else 84, E8 * 1.6)
            n(te, DR, 54, 52 + (20 if e in (0, 3) else 0), 0.05)
            if level >= 2 and e in (1, 2, 4, 5):
                for k in vo: n(te, AC, k, 56, E8 * 0.7)
            if level >= 3 and e in (0, 2, 3, 5): n(te, DR, 85, 46, 0.05)
        if level >= 3 and mel:
            for off, k, d in MEL:
                if (b % 2) * 12 <= off < (b % 2) * 12 + 12:
                    tt = t + (off - (b % 2) * 12) * E8
                    if tt < t1: tremolo(tt, k - (12 if prog == "home" else 0), 80, min(d * E8 * 0.95, t1 - tt))
        t += BAR; b += 1


def pizz(t0, t1, ch="Am", rate=1.0, v=74):
    root, vo = CH[ch]; t = t0; j = 0; arp = vo + [vo[0] + 12]
    while t < t1 - 0.04: n(t, PZ, arp[j % len(arp)] + 12, v, 0.12); t += E8 / rate; j += 1


def run_up(t, v=86, n_=10):
    for j in range(n_): n(t + j * 0.04, PZ, 69 + j * 2, v, 0.08)


SNEAK = [(0, 45, 0.5), (1, 48, 0.5), (2, 52, 0.5), (3, 51, 1.0), (5, 47, 0.5), (6, 45, 0.5), (7, 44, 1.0)]


def sneak(t0, v=88, tr=0):
    """AMS's theme: a tiptoe bassoon staccato (chromatic, sly)."""
    for off, k, d in SNEAK: n(t0 + off * E8, BN, k + 12 + tr, v, d * E8 * 0.55)
    n(t0, PZ, 57, 60, 0.1); n(t0 + 4 * E8, PZ, 52, 60, 0.1)


def breathe(t0, t1, ch="Am", v=60, period=2.4):
    """the lungs: the accordion swells in and out like bellows (velocity steps)."""
    root, vo = CH[ch]; t = t0
    while t < t1 - 0.2:
        for j in range(4):
            vv = int(v * (0.5 + 0.5 * math.sin(math.pi * j / 3)))
            for k in vo: n(t + j * period / 8, AC, k, vv, period / 8)
        n(t, BS, root - 12, 60, period / 2); t += period / 2


def hit(t, ch="Am", v=108, d=0.35):
    root, vo = CH[ch]
    n(t, BS, root - 12, v, d); n(t, DR, 36, v, 0.1); n(t, DR, 49, v - 24, 0.4); n(t, TB, vo[0], v - 10, d)
    for k in vo: n(t, AC, k + 12, v - 20, d); n(t, STR, k, v - 30, d * 1.5)


def wah(t, v=96):
    """'nothing at all': a deflating trombone wah-wah (three falling notes + a long low one)."""
    for j, (k, d) in enumerate(((58, 0.25), (57, 0.25), (56, 0.25), (55, 0.9))): n(t + j * 0.27, TB, k, v - j * 4, d)


def hold(t0, t1, ch="Am", v=46):
    root, vo = CH[ch]
    for k in vo: n(t0, STR, k, v, t1 - t0)
    n(t0, BS, root - 12, v + 12, min(t1 - t0, 2.0))


def tick(t0, t1, v=64):
    t = t0
    while t < t1 - 0.04: n(t, CE, 96, v, 0.06); n(t + E8 * 1.5, CE, 91, v - 10, 0.06); t += E8 * 3


TC = T("a1", "crush") - 0.15
# hook: the tarantella is already dancing at frame 0 (the office, the cloud); the lungs reveal = a hit + breathing accordion
tarantella(0.0, S["S0b"], "tar", 3); hit(T("i1", "lungs") - 0.15, "E7", 100)
breathe(S["S0b"], S["S1"], "Am", 58)
tarantella(S["S1"], S["S2"], "tar", 2); hit(T("i2", "morning") - 0.1, "Am", 96)
# the clove: light dance; the CRUSH = a full-band hit
tarantella(S["S2"], TC, "lift", 2, False); pizz(S["S2b"], TC, "C", 1.0, 64)
hit(TC, "Am", 112); tarantella(TC + 0.3, S["S4"], "tar", 3)
# the chemistry: pizzicato that speeds up; meet = celesta; falls apart = a run up + hit
pizz(S["S4"], S["S4b"], "Am", 1.0, 70); hold(S["S4"], S["S4b"], "Am", 40)
hit(T("a2", "breaks") - 0.1, "Dm", 90)
pizz(S["S4b"], S["S5"], "E7", 1.5, 74); n(T("a2", "meet") - 0.1, CE, 88, 90, 0.5); n(T("a2", "meet") - 0.1, CE, 93, 84, 0.5)
pizz(S["S5"], T("a3", "apart") - 0.2, "Am", 2.0, 78); run_up(T("a3", "apart") - 0.55); hit(T("a3", "apart") - 0.15, "E7", 104)
tarantella(T("a3", "apart") + 0.2, S["S6"], "tar", 2)
# two places: whisper = held chord, then the hit on 'two'
hold(S["S6"], S["S7"], "Dm", 46); hit(T("b0", "two") - 0.1, "Am", 104)
# place one, the mouth: light dance; brushing = the full band
tarantella(S["S7"], S["S8"], "lift", 2, False)
tarantella(S["S8"], S["S9"], "tar", 3); n(T("b2", "really") - 0.1, CE, 96, 96, 0.4)
# place two: AMS's tiptoe theme everywhere it moves
hold(S["S9"], S["S12"], "Am", 38)
sneak(S["S9"] + 0.15, 92); sneak(S["S9b"] + 0.1, 84, -2); sneak(S["S10"] + 0.5, 88); sneak(S["S10b"] + 0.1, 86, 2); sneak(S["S11"] + 0.2, 84)
pizz(S["S10"], S["S10b"], "Dm", 1.0, 56)
hit(T("b5", "lungs") - 0.2, "E7", 92); breathe(S["S11b"], S["S12"], "Am", 64)
# sweat: the dance walks home
tarantella(S["S12"], S["S13"], "home", 2, False)
breathe(S["S13"], S["S14"], "C", 58); hit(T("b7", "talking") - 0.15, "Am", 96)
# how long: the clock = celesta ticks; 24 hours = hit; meetings = the band
tick(S["S14"], S["S16"], 66); hold(S["S14"], S["S15"], "E7", 44); hit(T("c1", "twentyfour") - 0.2, "Am", 98)
tarantella(S["S16"], S["S17"], "tar", 3)
# the fight + the lab test: clockwork pizz + ticks, each result a chord
hit(T("d0", "fight") - 0.2, "E7", 110)
pizz(S["S18"], S["S19"], "Am", 1.0, 62); tick(S["S18"], S["S19"], 58)
pizz(S["S19"], S["S20"], "C", 1.0, 66); hit(T("d2", "half") - 0.3, "C", 96)
tarantella(S["S20"], T("d3", "tea") - 0.2, "lift", 2, False); hit(T("d3", "better") - 0.1, "G", 100); wah(T("d3", "tea"), 96)
pizz(S["S21"], S["S22"], "Am", 1.2, 64); hit(T("d4", "won") - 0.2, "C", 100); run_up(T("d4", "down") - 0.4, 80)
# milk with the meal: warm home progression
tarantella(S["S22"], S["S23"], "home", 2, True)
# recap: the full band; lungs need time = breathing accordion
tarantella(S["S23"], S["S24"], "tar", 3); breathe(S["S24"], S["S25"], "Am", 56, 3.0)
# worth it + the interview + send: triumphant dance to the end
tarantella(S["S25"], S["S25b"], "lift", 3); sneak(S["S25b"] + 0.1, 86)
tarantella(S["S26"], END - 1.6, "tar", 3); hit(T("f2", "close") - 0.1, "E7", 100)
hit(END - 1.6, "Am", 112)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((MD, 78), (AC, 46), (BS, 64), (PZ, 88), (BN, 56), (CE, 92), (TB, 40), (STR, 64)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = render(sorted(ev), END)
mus = signal.sosfilt(signal.butter(2, 11000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
