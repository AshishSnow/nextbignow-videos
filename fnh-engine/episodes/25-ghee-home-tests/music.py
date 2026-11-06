"""COURTROOM QAWWALI score for FreshNestHub 25 "can you test ghee at home?" (GeneralUser GS): a trial with handclaps. D Bhairav-flavoured (D Eb F# G A Bb C#) at 108 bpm, keherwa 8-beat on a tabla stand-in (congas + bongo + low tom), reed-organ harmonium, sitar answers, pan-flute bansuri, tanpura-ish drone, a small chorus 'aah' on verdicts.
FOLLOWS THE STORY: the hook has no band, a held harmonium + tabla roll under the sliding ghee; the band hits when the palm tree shoots up. Every test gets a thin groove and its verdict gets a harmonium stab + a chorus note. The band stops dead on 'no winners'. Chemistry = sneaky pizzicato. The fridge: the band drops to a cold celesta + bansuri, the clue. Lab: a ticking thin groove. Tips: full qawwali with claps."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}; TI = T("i1", "oil") - 0.08
HAR, BAS, SIT, FLU, CHO, CEL, STR, PIZ, TIM, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {HAR: 20, BAS: 32, SIT: 104, FLU: 75, CHO: 52, CEL: 8, STR: 48, PIZ: 45, TIM: 47}
VOL = {HAR: 86, BAS: 106, SIT: 78, FLU: 84, CHO: 72, CEL: 90, STR: 60, PIZ: 92, TIM: 90, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 108
CH = {"D": (38, [62, 66, 69]), "Eb": (39, [63, 67, 70]), "Gm": (43, [62, 67, 70]), "A": (45, [61, 64, 69]), "Dm": (38, [62, 65, 69])}
PROGS = {"main": ["D", "Eb", "D", "A"], "tense": ["D", "Gm", "Eb", "A"], "bright": ["D", "D", "Gm", "D"]}
# keherwa: dha ge na ti | na ka dhi na : 8 eighth-note strokes (drum keys: 64 low conga = bayan, 62 mute conga = na, 60 hi bongo = ti, 63 open conga = dhi)
KEH = [(64, 92), (61, 60), (62, 78), (60, 58), (62, 76), (61, 54), (63, 88), (62, 70)]


def groove(t0, t1, prog="main", level=2):
    """1: tabla + bass (thin, for explanations). 2: + claps + harmonium chords. 3: + sitar riff + chorus pad."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q, (k, v) in enumerate(KEH):
            tq = t + q * BEAT / 2
            if tq < t1 - 0.03: n(tq, DR, k, v - (10 if level == 1 else 0), 0.08)
        for off, st in ((0, 0), (2, 7)):
            if t + off * BEAT < t1: n(t + off * BEAT, BAS, root + st, 94, BEAT * 0.8)
        if level >= 2:
            for off in (0, 1, 2, 2.5, 3):
                if t + off * BEAT < t1: n(t + off * BEAT, DR, 39, 76 if off in (0, 2) else 58, 0.05)
            for off in (0, 1.5, 2, 3.5):
                for k in vo:
                    if t + off * BEAT < t1: n(t + off * BEAT, HAR, k, 62, BEAT * (0.6 if off in (1.5, 3.5) else 0.9))
        if level >= 3:
            for k in vo: n(t, CHO, k + 12, 50, BEAT * 3.6)
            riff(t + BEAT * 2, 76, SIT, 0, BEAT * 0.5)
        t += 4 * BEAT; b += 1


# the original tune: rises through the augmented step, the Bhairav colour
TUNE = [(0, 74), (0.5, 75), (1, 78), (1.5, 79), (2, 81), (2.5, 79), (3, 78), (3.5, 75), (4, 74)]


def riff(t0, v=84, ch=FLU, tr=0, gap=BEAT):
    for off, k in TUNE: n(t0 + off * gap, ch, k + tr, v, gap * 0.48)


def stab(t, chord="D", v=108, d=0.4):
    """a verdict: harmonium stab, chorus note, low tom."""
    root, vo = CH[chord]
    n(t, BAS, root, v, d); n(t, TIM, root + 12, v, 0.3); n(t, DR, 64, v - 4, 0.1); n(t, DR, 39, v - 20, 0.06)
    for k in vo: n(t, HAR, k + 12, v - 8, d); n(t, CHO, k + 12, v - 34, d * 1.4)


def roll(t0, t1, v0=46, v1=96):
    """a tabla roll that accelerates to the hit."""
    t = t0; j = 0
    while t < t1:
        k = (t - t0) / max(0.01, t1 - t0); n(t, DR, 62 if j % 2 else 60, v0 + (v1 - v0) * k, 0.05); t += 0.2 - 0.14 * k; j += 1


def sneak(t0, t1, v=84):
    """chemistry: pizzicato walking on the Bhairav scale + a soft mute conga."""
    t = t0; b = 0; line = [50, 51, 54, 55, 57, 55, 54, 51]
    while t < t1 - 0.05:
        n(t, PIZ, line[b % 8], v, BEAT * 0.3); n(t + BEAT / 2, DR, 62, 52, 0.06)
        t += BEAT; b += 1


def cold(t0, t1):
    """the fridge: a drone + celesta, bansuri above; no drums."""
    n(t0, STR, 50, 54, t1 - t0); n(t0, STR, 57, 50, t1 - t0)
    t = t0; b = 0; seq = [86, 81, 79, 78, 81, 75, 78, 74]
    while t < t1 - 0.1:
        n(t, CEL, seq[b % 8], 74, 0.5); t += BEAT; b += 1


def downfall(t, k=74, v=92):
    """a sitar slide down for USELESS / FOOLED."""
    for j, dk in enumerate((0, -1, -4, -5, -7)): n(t + j * 0.12, SIT, k + dk, v, 0.14 if j < 4 else 0.5)


# ---- hook: no band: a held harmonium + a tabla roll under the sliding ghee; the band hits on the palm tree
for k in (50, 57, 62): n(0.0, HAR, k, 58, TI)
roll(0.1, TI); stab(TI, "D", 118, 0.5); n(TI, FLU, 86, 90, 0.5)
n(S["S1"], DR, 39, 70, 0.05); groove(S["S1"], S["S1b"], "bright", 1)
for k in (50, 57): n(S["S1b"], HAR, k, 50, S["S1c"] - S["S1b"])
riff(T("i2", "melts") - 0.1, 70, FLU, 0, BEAT * 0.35)
groove(S["S1c"], S["S2"], "bright", 2); stab(T("i2", "Pure") - 0.1, "D", 104, 0.4)
# the court
for k in (38, 50): n(S["S2"], BAS, k, 88, 1.4)
stab(T("i3", "trial") - 0.1, "Eb", 118, 0.6); groove(T("i3", "trial") + 0.4, S["S3"], "main", 2)
# real + fake
groove(S["S3"], S["S3c"], "bright", 1); stab(S["S3c"] + 0.05, "D", 96, 0.5); riff(S["S3c"] + 0.1, 86, FLU, 0, BEAT * 0.3)
sneak(S["S4"], S["S5"], 84); stab(T("a2", "cheaper") - 0.1, "A", 94, 0.3)
for k in (38, 45): n(S["S5"], STR, k, 58, S["S6"] - S["S5"])
for j in range(int((S["S6"] - S["S5"]) / (BEAT * 2))): n(S["S5"] + j * BEAT * 2, DR, 64, 66, 0.1)
stab(T("a3", "pure") - 0.1, "Eb", 98, 0.4)
# test 1-4: the same thin groove; a verdict each
groove(S["S6"], S["S7"], "main", 1); n(S["S7"], DR, 62, 50, 0.1); groove(S["S7"] + 0.4, S["S8"], "main", 1); stab(T("b2", "kitchen") - 0.15, "A", 104, 0.3); downfall(T("b2", "kitchen") + 0.05)
groove(S["S8"], S["S9"], "bright", 1); sneak(S["S9"], S["S9c"], 80); groove(S["S9c"], S["S10"], "main", 1); stab(T("c2", "too") - 0.12, "Eb", 104, 0.35)
sneak(S["S10"], S["S10b"], 74); stab(T("c3", "it") - 0.02, "A", 100, 0.3); downfall(T("c3", "it") + 0.15)
groove(S["S11"], S["S12"], "bright", 1); riff(S["S11"] + 0.1, 72, FLU, 0, BEAT * 0.4)
n(S["S12"], STR, 50, 56, S["S13"] - S["S12"]); stab(T("d2", "essence") + 0.05, "Eb", 102, 0.4); downfall(T("d2", "essence") + 0.2)
groove(S["S13"], S["S14"], "main", 1); groove(S["S14"], S["S14b"], "bright", 1); riff(T("e2", "white") - 0.1, 76, FLU, 0, BEAT * 0.3)
sneak(S["S14b"], S["S15"], 78); stab(T("e2", "bottle") - 0.1, "A", 104, 0.35); downfall(T("e2", "bottle") + 0.1)
# no winners: the band stops
for j in range(4): n(S["S15"] + 0.02 + j * 0.1, DR, 64, 84, 0.08)
stab(T("f1", "no") - 0.1, "Eb", 110, 0.5)
# chemistry
stab(T("f1", "chemistry") - 0.1, "D", 116, 0.5); sneak(S["S16"], S["S17"], 86); stab(T("f2", "starch") - 0.15, "A", 96, 0.3)
sneak(S["S17"], S["S18"], 80)
for k in (74, 75, 78, 81): n(T("f3", "crimson") - 0.15 + (k - 74) * 0.03, CEL, k, 82, 0.4)
sneak(S["S18"], S["S19"], 76); stab(T("f4", "through") - 0.15, "A", 96, 0.3)
for k in (38, 39): n(S["S19"], STR, k, 64, S["S20"] - S["S19"])
stab(T("f5", "kitchen") - 0.15, "Eb", 100, 0.4)
# the fridge: cold + bansuri = the clue
cold(S["S20"], S["S22"]); riff(S["S20b"] + 0.05, 92, FLU, 0, BEAT * 0.45); n(T("g1", "one") - 0.15, CHO, 74, 78, 1.2)
n(S["S22"], STR, 39, 60, S["S23"] - S["S22"]); n(S["S22"], STR, 45, 56, S["S23"] - S["S22"]); stab(T("g3", "split") - 0.1, "Eb", 100, 0.5)
groove(S["S23"], S["S24"], "main", 1); stab(T("g4", "clue") - 0.1, "D", 96, 0.3)
sneak(S["S24"], S["S25"], 72); stab(T("g5", "proof") - 0.15, "A", 96, 0.3)
# the lab: thin, ticking
sneak(S["S25"], S["S26"], 80); stab(T("h1", "miss") - 0.15, "Eb", 92, 0.3)
groove(S["S26"], S["S27b"], "bright", 1); riff(T("h2", "tiny"), 74, CEL, 0, BEAT * 0.3); stab(T("h2", "zero") - 0.1, "A", 96, 0.3)
n(T("h3", "cant") - 0.1, SIT, 62, 80, 0.5); downfall(T("h3", "count", 1) if False else T("h3", "cant") + 0.2, 74, 80)
# tips + the card: full qawwali
groove(S["S28"], S["S30"], "bright", 2); stab(T("k1", "tin") - 0.12, "D", 104, 0.3)
stab(T("k2", "batch", 1) - 0.1, "Eb", 92, 0.25); stab(T("k2", "expiry", 1) - 0.1, "A", 92, 0.25)
groove(S["S30"], S["S31"], "tense", 1); stab(T("k3", "proof") - 0.15, "Eb", 104, 0.3)
groove(S["S31"], S["S32"], "bright", 2); stab(T("k4", "why") - 0.15, "A", 94, 0.3)
groove(S["S32"], S["S33"], "bright", 2); riff(S["S32"] + 0.3, 72, FLU, 0, BEAT * 0.5)
groove(S["S33"], END - 1.6, "main", 3); riff(S["S33"] + 0.15, 92, FLU, 0, BEAT * 0.5); stab(END - 1.6, "D", 114, 1.2)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((HAR, 52), (BAS, 64), (SIT, 86), (FLU, 44), (CHO, 70), (CEL, 90), (STR, 50), (PIZ, 76), (TIM, 60)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


mus = render(sorted(ev), END)
mus = signal.sosfilt(signal.butter(2, 10000, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
