"""80s AEROBICS SYNTH-POP score for FreshNestHub 28 "do you need a detox after Diwali?" (GeneralUser GS; new genre): the detox fad as a cheesy workout tape.
A major-ish (A / F#m / D / E) at 118 bpm: octave synth bass, gated-snare backbeat (snare + clap), 16th hats, synth brass stabs, a square-lead hook, a warm pad, glassy EP.
FOLLOWS THE STORY: the fad (juice, posts, products) = the full aerobics band; every debunk DEFLATES it (a pitch glide down + tape-stop style drop of the band);
the REAL organs get a steady FACTORY groove (muted synth-bass ostinato, closed hats like a ticking machine, EP plucks, a 'clank' on 2 and 4 in the mix);
the kidneys = bubbly glock arpeggios; the caution lines = pad only; what helps = warm EP + soft beat; the recap + send = the full band, but now in a calm 'cool-down' voicing."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
S = {k: st for k, st, _ in SHOTLIST}; TD = T("i1", "detox") - 0.05
SB, BR, LD, PAD, EP, GL, HIT, STR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {SB: 38, BR: 62, LD: 80, PAD: 89, EP: 4, GL: 9, HIT: 55, STR: 48}
VOL = {SB: 100, BR: 84, LD: 78, PAD: 70, EP: 84, GL: 80, HIT: 76, STR: 60, DR: 84}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 118
CH = {"A": (33, [57, 61, 64, 69]), "F#m": (30, [57, 61, 66, 69]), "D": (38, [57, 62, 66, 69]), "E": (40, [56, 59, 64, 68]), "Bm": (35, [59, 62, 66, 71]), "C#m": (37, [56, 61, 64, 68])}
PROGS = {"pop": ["A", "F#m", "D", "E"], "work": ["F#m", "D", "A", "E"], "calm": ["D", "A", "Bm", "E"], "dark": ["F#m", "C#m", "D", "C#m"]}


def aerobics(t0, t1, prog="pop", level=3):
    """level 1: bass + hats. 2: + gated backbeat + pad. 3: + brass stabs + square-lead hook (the full workout tape)."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(8):
            tq = t + q * BEAT / 2
            if tq >= t1: break
            n(tq, SB, root + (12 if q % 2 else 0), 92 if q % 2 == 0 else 78, BEAT * 0.4)
            n(tq, DR, 42, 40 + (14 if q % 2 == 0 else 0), 0.04)
            if level >= 2 and q in (2, 6): n(tq, DR, 38, 96, 0.1); n(tq, DR, 39, 70, 0.1)
            if level >= 2 and q in (0, 4): n(tq, DR, 36, 104, 0.1)
        if level >= 2:
            for k in vo: n(t, PAD, k, 46, BEAT * 3.8)
        if level >= 3:
            for off in (0, 1.5, 3):
                if t + off * BEAT < t1:
                    for k in vo[1:]: n(t + off * BEAT, BR, k + 12, 70, BEAT * 0.3)
        t += 4 * BEAT; b += 1


HOOK = [(0, 76, 0.5), (0.5, 73, 0.5), (1, 76, 0.5), (1.5, 78, 1.0), (2.5, 76, 0.5), (3, 73, 1.0)]


def hook(t0, v=84, tr=0, ch=LD):
    for off, k, d in HOOK: n(t0 + off * BEAT, ch, k + tr, v, d * BEAT * 0.9)


def factory(t0, t1, prog="work", ep=True):
    """the REAL organs: a muted 16th synth-bass ostinato, ticking closed hats, EP plucks (a machine that never stops)."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(16):
            tq = t + q * BEAT / 4
            if tq >= t1: break
            n(tq, SB, root + (7 if q % 4 == 2 else 0), 70 if q % 4 == 0 else 52, BEAT * 0.18)
            if q % 2 == 0: n(tq, DR, 42, 36, 0.03)
            if q in (0, 8): n(tq, DR, 36, 80, 0.1)
        if ep:
            for j, k in enumerate((vo[0] + 12, vo[2] + 12, vo[1] + 12, vo[3] + 12)):
                if t + j * BEAT < t1: n(t + j * BEAT, EP, k, 64, BEAT * 0.6)
        t += 4 * BEAT; b += 1


def bubbles(t0, t1, v=70):
    t = t0; j = 0; arp = [81, 85, 88, 93, 88, 85]
    while t < t1 - 0.05: n(t, GL, arp[j % 6], v, 0.15); t += BEAT / 4; j += 1


def deflate(t, v=100):
    """a debunk: the lead glides DOWN (fast chromatic fall) + an orchestra-hit thud."""
    for j, k in enumerate(range(81, 57, -2)): n(t + j * 0.025, LD, k, v - j * 3, 0.04)
    n(t + 0.3, HIT, 45, v, 0.4); n(t + 0.3, SB, 28, v, 0.6); n(t + 0.3, DR, 49, v - 20, 0.6)


def stab(t, chord="A", v=104, d=0.35):
    root, vo = CH[chord]
    n(t, SB, root, v, d); n(t, DR, 36, v, 0.1); n(t, DR, 49, v - 24, 0.4); n(t, HIT, vo[0], v - 10, d)
    for k in vo: n(t, BR, k + 12, v - 14, d)


def hold(t0, t1, chord="D", v=50):
    root, vo = CH[chord]
    for k in vo[:3]: n(t0, PAD, k, v, t1 - t0)
    n(t0, SB, root, v + 10, min(t1 - t0, 2.0))


# ---- hook: the workout tape is already pumping as he chugs; on 'detox' (the spit-take) it stops dead with a deflate
aerobics(0.0, TD, "pop", 3); hook(0.05, 88); deflate(TD - 0.25, 104)
factory(S["S0b"], S["S1"], "work", True)
# 'no juice, no tea, no plan': three stabs on the X's, then the factory under 'it just does it'
aerobics(S["S1"], S["S1b"], "pop", 2)
for w_ in ("juice", "tea", "plan"): stab(T("i2", w_) - 0.2, "A", 96, 0.25)
factory(S["S1b"], S["S2"], "work"); n(T("i2", "free") - 0.1, GL, 93, 90, 0.6)
# the posts: the cheesy tape again; 'not impressed' = deflate
aerobics(S["S2"], S["S2b"], "pop", 3); hook(S["S2"] + 0.1, 84); deflate(T("i3", "impressed") - 0.35, 100); hold(S["S2b"] + 0.4, S["S3"], "F#m", 46)
# the 2009 investigation: dark detective groove; 'no proof' deflates
factory(S["S3"], S["S4b"], "dark", False)
for j in range(4): n(S["S3"] + 0.1 + j * 0.3, EP, (69, 73, 76, 81)[j], 70, 0.25)
for j in range(15): n(T("a2", "fifteen") - 0.2 + j * 0.05, GL, 81 + (j % 5) * 2, 60, 0.08)
deflate(T("a2", "proof") + 0.2, 104); hold(S["S4b"] + 0.9, S["S5"], "C#m", 46)
factory(S["S5"], S["S6b"], "dark", True); stab(T("a4", "soap") - 0.1, "D", 100, 0.4)
# part 1, the real cleaners: the FACTORY groove takes over (the organs' own music)
aerobics(S["S7"], S["S8"], "work", 1); stab(T("b0", "cleaning") - 0.2, "E", 100, 0.3)
factory(S["S8"], S["S11"], "work", True); hook(S["S8b"] + 0.1, 70, -12, EP)
n(T("b2", "water") - 0.15, HIT, 45, 70, 0.3); n(T("b3", "one") - 0.1, GL, 88, 80, 0.3); n(T("b3", "time") - 0.1, GL, 93, 84, 0.4)
stab(T("b4", "leave") - 0.2, "A", 96, 0.3)
# part 2, the kidneys: the factory + bubbly glock
factory(S["S11"], S["S15"], "calm", True); bubbles(S["S11"], S["S13"], 62); stab(T("c0", "kidneys") - 0.2, "D", 104, 0.35)
for j in range(10): n(T("c1", "million") - 0.3 + j * 0.06, GL, 84 + j, 64, 0.06)
stab(T("c2", "seven") - 0.25, "E", 104, 0.4); bubbles(S["S14"], S["S15"], 58)
# 24/7, no subscription: calm factory, a wink
factory(S["S15"], S["S16"], "calm", True); n(T("c4", "subscription") - 0.3, BR, 69, 90, 0.2); n(T("c4", "subscription") - 0.1, BR, 76, 90, 0.4)
# part 3, the cleanse: the tape again... and it deflates twice
aerobics(S["S16"], S["S17"], "pop", 3); hook(S["S16"] + 0.1, 84)
factory(S["S17"], S["S19"], "dark", False); deflate(T("d1", "proof") - 0.4, 100); deflate(T("d2", "back") - 0.35, 92)
# the caution lines: pad only
hold(S["S19"], S["S20"], "F#m", 48); hold(S["S20"], S["S21"], "C#m", 46)
# part 4, what helps: warm EP + soft beat
aerobics(S["S21"], S["S22b"], "calm", 1); stab(T("e0", "helps") - 0.2, "A", 96, 0.3)
factory(S["S22b"], S["S23"], "calm", True); hold(S["S23"], S["S24"], "Bm", 48)
# recap + send: the full band in a calm cool-down voicing, a last hook
aerobics(S["S24"], END - 1.6, "calm", 3); hook(S["S24"] + 0.1, 86); hook(S["S25"] + 0.1, 86)
stab(END - 1.6, "A", 112, 1.4)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((SB, 64), (BR, 46), (LD, 80), (PAD, 64), (EP, 40), (GL, 88), (HIT, 64), (STR, 50)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


def tape_drop(x, t0, dur=0.45):
    """the band stops like a tape (varispeed slow-down) at a debunk."""
    i0, i1 = int(t0 * SR), int((t0 + dur) * SR)
    if i1 >= len(x): return x
    seg = x[i0:i1]; L = len(seg); src = np.cumsum(np.linspace(1.0, 0.15, L)); src = src / src[-1] * (L * 0.57)
    idx = np.clip(src.astype(int), 0, L - 1); y = seg[idx] * np.linspace(1, 0, L)[:, None]
    x = x.copy(); x[i0:i1] = y; return x


mus = render(sorted(ev), END)
mus = signal.sosfilt(signal.butter(2, 11000, "low", fs=SR, output="sos"), mus, axis=0)
for tt in (TD - 0.3, T("i3", "impressed") - 0.45, T("d1", "proof") - 0.5):
    mus = tape_drop(mus, tt, 0.4)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
