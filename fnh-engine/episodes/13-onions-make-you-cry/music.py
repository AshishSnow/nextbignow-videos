"""ORCHESTRAL CAPER score for FreshNestHub 13 "why onions make you cry" (GeneralUser GS): a sneaky heist / spy-caper band -
pizzicato strings walking bass (2-feel, 116 BPM), staccato bassoon tiptoe melody, clarinet answers, harpsichord off-beat
chords, side-stick + closed hats, timpani hits + glockenspiel 'sparkle' on the reveals, tremolo strings for the tension.
Story-following: the onion's TRAP is the heist - sneaky D-minor caper while the trap is explained, the band DROPS to
pizz bass + harpsichord under explanation lines (coherence), tremolo + timpani rolls as the chain reaction builds
(cut -> mix -> acid -> gas -> nerves -> tears), stop-time hits on every link, and the band turns BRIGHT (D major,
clarinet tune) for the tear-free onion and the takeaways."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}

PZ, BSN, CLA, HPS, TIM, GLK, TRM, TUB, FLT, SUB, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9
PROG = {PZ: 45, BSN: 70, CLA: 71, HPS: 6, TIM: 47, GLK: 9, TRM: 44, TUB: 58, FLT: 72, SUB: 38}
VOL = {PZ: 112, BSN: 96, CLA: 92, HPS: 84, TIM: 110, GLK: 86, TRM: 72, TUB: 90, FLT: 80, SUB: 92, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BPM = 116
CH = {"Dm": (38, [62, 65, 69]), "Gm": (43, [62, 67, 70]), "A7": (45, [61, 64, 67]), "Bb": (46, [62, 65, 70]),
      "D": (38, [62, 66, 69]), "G": (43, [62, 67, 71]), "A": (45, [61, 64, 69]), "Edim": (40, [64, 67, 70])}
PROGS = {"sneak": ["Dm", "Dm", "Gm", "A7"], "soft": ["Dm", "Bb", "Gm", "A7"], "tense": ["Dm", "Edim", "Dm", "Edim"],
         "bright": ["D", "G", "A", "D"]}
WALK = {"Dm": [38, 41, 45, 44], "Gm": [43, 46, 50, 49], "A7": [45, 49, 52, 51], "Bb": [46, 50, 53, 52], "Edim": [40, 43, 46, 45],
        "D": [38, 42, 45, 44], "G": [43, 47, 50, 49], "A": [45, 49, 52, 51]}
TIPTOE = [62, None, 65, None, 64, 65, 67, None, 69, None, 68, None, 67, 65, 64, None]      # bassoon, 16ths -> staccato 8ths
ANSWER = [74, 72, 70, 69, 70, 69, 67, 65]
BRIGHT = [74, 76, 78, 81, 79, 78, 76, 74]


def band(t0, t1, prog="sneak", level=2, bpm=BPM):
    """level 1: pizz walking bass + harpsichord off-beats; 2: + kit + bassoon tiptoe; 3: + clarinet answer + tuba."""
    beat = 60 / bpm; bar = 4 * beat; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * beat
            if tq < t1 - 0.03: n(tq, PZ, WALK[ch][q], 104 if q % 2 == 0 else 88, beat * 0.5)
            if tq + beat / 2 < t1 - 0.03:
                for k in vo: n(tq + beat / 2, HPS, k, 62, beat * 0.3)
        if level >= 2:
            for q in range(8):
                tq = t + q * beat / 2
                if tq < t1 - 0.03: n(tq, DR, 42, 44 + 10 * (q % 2 == 0), 0.06)
            for q in (1, 3):
                if t + q * beat < t1 - 0.03: n(t + q * beat, DR, 37, 70, 0.08)
            if prog != "bright":
                for j, k in enumerate(TIPTOE[(b % 2) * 8:(b % 2) * 8 + 8]):
                    tj = t + j * beat / 2
                    if k and tj < t1 - 0.03: n(tj, BSN, k - (0 if b % 4 < 2 else 2) + (2 if ch == "A7" else 0), 92, beat * 0.22)
        if level >= 3:
            mel = BRIGHT if prog == "bright" else ANSWER
            for j, k in enumerate(mel):
                tj = t + j * beat / 2
                if tj < t1 - 0.03 and (j % 4 != 3 or prog == "bright"): n(tj, CLA, k - (2 if b % 2 else 0), 88, beat * 0.4)
            if t < t1 - 0.03: n(t, TUB, root - 12 + 12, 86, beat * 0.6)
        if prog == "tense":
            for k in vo: n(t, TRM, k - 12, 58, min(bar, t1 - t))
        t += bar; b += 1


def hit(t, v=110, big=False):
    n(t, TIM, 38, v, 0.8); n(t, DR, 49, v - 24, 1.4); n(t, PZ, 26 + 12, v, 0.3)
    if big: n(t, SUB, 26, 104, 1.0); n(t, TIM, 45, v - 10, 0.8)


def stab(t, chord="Dm", v=104, d=0.3):
    root, vo = CH[chord]
    for k in vo: n(t, HPS, k + 12, v - 10, d); n(t, PZ, k, v - 8, d); n(t, CLA, k + 12, v - 26, d * 1.5)
    n(t, PZ, root, 112, d)


def sparkle(t, base=84, nn=6, v=86):
    for i in range(nn): n(t + i * 0.045, GLK, base + (0, 3, 7, 10, 12, 15, 19)[i % 7], v, 0.4)


def troll(t, d=0.6, v=60):     # timpani roll
    for i in range(int(d / 0.05)): n(t + i * 0.05, TIM, 38, v + i * 2, 0.05)


def tiptoe_run(t, k0, k1, d=0.5, ch=BSN, v=92):
    m = 6
    for i in range(m): n(t + d * i / m, ch, k0 + (k1 - k0) * i // (m - 1), v, d / m * 0.8)


def pad(t0, t1, keys=(62, 65, 69), v=50, ch=None):
    for k in keys: n(t0, TRM if ch is None else ch, k, v, max(0.2, t1 - t0))


TC = T("i1", "cry...") - 0.1; TP = T("i1", "purpose?") - 0.1
# hook: caper already going at t=0 (chopping), stop-time + sob glide on "cry", sting on "purpose"
band(0.0, TC - 0.02, "sneak", 2)
hit(TC, 108, True); tiptoe_run(TC + 0.05, 74, 62, 0.6, CLA, 90); pad(TC, S["S1"] - 0.05, (62, 65, 68), 52)
stab(TP, "A7", 108, 0.4); sparkle(TP + 0.05, 86, 5)
band(S["S1"], S["S1b"] - 0.05, "sneak", 3); stab(T("i2", "trap!") - 0.1, "Edim", 108, 0.4)
band(S["S1b"], S["S2"] - 0.05, "tense", 1); hit(T("i2", "knife") - 0.05, 116, True)
band(S["S2"], S["S3"] - 0.05, "bright", 1); sparkle(T("i3", "can't") - 0.1, 88, 7)
# PART 1: the trap (soft caper under the explanations)
hit(S["S3"] + 0.05, 100); band(S["S3"], S["S4"] - 0.05, "soft", 1)
for j in range(6): n(T("a1", "An") - 0.2 + j * 0.13, GLK, 96 - j * 3, 72, 0.2)          # the zoom-in dive
band(S["S4"], S["S5"] - 0.05, "soft", 1); n(T("a2", "two") - 0.1, CLA, 74, 90, 0.3); n(T("a2", "two") + 0.15, CLA, 77, 90, 0.3)
band(S["S5"], S["S5b"] - 0.05, "sneak", 2)
band(S["S5b"], S["S6"] - 0.05, "soft", 1)
for j in range(6): n(S["S5b"] + 0.2 + j * 0.15, GLK, 79 + 2 * j, 66, 0.2)                 # sulfur climbing the roots
band(S["S6"], S["S6b"] - 0.05, "soft", 1); stab(T("a4", "enzyme.") - 0.3, "Gm", 100, 0.3)
band(S["S6b"], S["S6c"] - 0.05, "bright", 1); sparkle(T("a5", "helper.") - 0.15, 86, 5)
band(S["S6c"], S["S7"] - 0.05, "sneak", 2)
band(S["S7"], S["S8"] - 0.05, "soft", 1); pad(S["S7"], S["S8"] - 0.05, (57, 62, 65), 40, FLT)
# PART 2: the knife -> the chain reaction (tension builds, a hit on every link)
hit(T("b1", "cut") - 0.08, 118, True); stab(T("b1", "cut") - 0.08, "Dm", 110, 0.4)
band(S["S9"], S["S10"] - 0.05, "tense", 1); hit(T("b2", "breaks") - 0.15, 104); stab(T("b2", "mix.") - 0.05, "Edim", 104, 0.3)
band(S["S10"], S["S11"] - 0.05, "sneak", 2); stab(T("b3", "snips") - 0.1, "Gm", 102, 0.2); sparkle(T("b3", "acid.") - 0.2, 80, 5)
band(S["S11"], S["S12"] - 0.05, "tense", 1); troll(T("b4", "wobbly.") - 0.15, 0.6, 58); hit(T("b4", "grabs") - 0.1, 104)
band(S["S12"], S["S12b"] - 0.05, "tense", 2); hit(T("b5", "gas.") - 0.2, 112, True); sparkle(T("b5", "gas.") - 0.15, 82, 6)
band(S["S12b"], S["S13"] - 0.05, "sneak", 3); stab(T("b5", "tear") - 0.15, "A7", 106, 0.4)
band(S["S13"], S["S14"] - 0.05, "sneak", 1); tiptoe_run(S["S13"] + 0.2, 62, 74, max(0.4, T("b6", "eyes.") - S["S13"] - 0.4), FLT, 80)
hit(T("b6", "eyes.") - 0.1, 110)
band(S["S14"], S["S15"] - 0.05, "tense", 1); stab(T("b7", "sting.") - 0.15, "Edim", 106, 0.3)
band(S["S15"], S["S16"] - 0.05, "sneak", 2); hit(T("b8", "flood") - 0.15, 112, True); tiptoe_run(T("b8", "flood") - 0.1, 81, 62, 0.8, CLA, 92)
# PART 3: why? (question, then the defence)
hit(S["S16"] + 0.02, 100); band(S["S16"], S["S17"] - 0.05, "soft", 1); n(T("c1", "this?") - 0.1, BSN, 57, 96, 0.5); n(T("c1", "this?") + 0.25, BSN, 56, 96, 0.6)
band(S["S17"], S["S17b"] - 0.05, "sneak", 3); hit(T("c2", "protect") - 0.1, 104)
band(S["S17b"], S["S18"] - 0.05, "soft", 1); stab(T("c2", "bite") - 0.15, "Gm", 96, 0.2); stab(T("c2", "knife.") - 0.15, "Gm", 96, 0.2)
band(S["S18"], S["S19"] - 0.05, "sneak", 2)
# PART 4: the tear-free onion (bright)
hit(S["S19"] + 0.02, 108, True); sparkle(S["S19"] + 0.1, 86, 7); band(S["S19"], S["S20"] - 0.05, "bright", 3)
band(S["S20"], S["S20b"] - 0.05, "soft", 1); band(S["S20b"], S["S21"] - 0.05, "bright", 2); hit(S["S20b"] + 0.25, 104); sparkle(S["S20b"] + 0.3, 88, 5)
band(S["S21"], S["S21b"] - 0.05, "soft", 1)
band(S["S21b"], S["S22"] - 0.05, "soft", 1); hit(T("d3", "off.") - 0.2, 108)
band(S["S22"], S["S23"] - 0.05, "bright", 2); troll(T("d4", "crushed") - 0.1, max(0.3, T("d4", "never") - T("d4", "crushed") - 0.1), 56)
hit(T("d4", "never") - 0.15, 112, True); sparkle(T("d4", "never") - 0.1, 86, 7)
# PART 5: beat the trap (caper returns, then bright takeaways)
hit(S["S23"] + 0.02, 108); band(S["S23"], S["S24"] - 0.05, "sneak", 3)
band(S["S24"], S["S25"] - 0.05, "soft", 1); pad(S["S24"], S["S25"] - 0.05, (62, 69, 74), 46, FLT)
for j in range(10): n(S["S24b"] + 0.1 + j * 0.16, GLK, 98 - (j % 5) * 2, 60, 0.3)          # slow-mo droplets
band(S["S25"], S["S26"] - 0.05, "sneak", 2); stab(T("e3", "juice") - 0.15, "Edim", 100, 0.3)
band(S["S26"], S["S27"] - 0.05, "tense", 2); troll(S["S26"] + 0.2, max(0.3, T("e4", "forty") - S["S26"] - 0.7), 56); hit(T("e4", "forty") + 0.1, 116, True)
band(S["S27"], S["S28"] - 0.05, "bright", 2); sparkle(T("e5", "sharp") - 0.15, 88, 5)
band(S["S28"], S["S28b"] - 0.05, "soft", 1); stab(T("e6", "Heat") - 0.15, "Bb", 98, 0.3)
band(S["S28b"], S["S29"] - 0.05, "bright", 2); hit(T("e6", "can't") - 0.1, 108)
band(S["S29"], S["S30"] - 0.05, "soft", 1)
for j, tw in enumerate((T("f1", "two") - 0.15, T("f1", "knife") - 0.15, T("f1", "gas") - 0.15)): n(tw, GLK, (86, 90, 93)[j], 100, 0.5)
band(S["S30"], END - 1.6, "bright", 3)
stab(END - 1.6, "D", 112, 1.6); hit(END - 1.6, 114, True); sparkle(END - 1.55, 86, 7)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((PZ, 58), (BSN, 44), (CLA, 80), (HPS, 70), (GLK, 84), (TRM, 64), (TUB, 50), (FLT, 40)): syn.control_change(ch, 10, pan)
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
# small wooden chamber room (caper band in a kitchen)
rng = np.random.default_rng(13); irl = int(0.8 * SR); tt = np.arange(irl) / SR
ir = rng.standard_normal((irl, 2)) * np.exp(-tt / 0.16)[:, None]; ir[: int(0.008 * SR)] = 0
ir = signal.sosfilt(signal.butter(2, [250, 6500], "band", fs=SR, output="sos"), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
mus = mus + 0.14 * np.stack([signal.fftconvolve(mus[:, c], ir[:, c])[: len(mus)] for c in (0, 1)], 1)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.3) / np.tanh(1.3)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
