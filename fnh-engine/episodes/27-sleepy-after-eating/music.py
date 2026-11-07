"""SLEEPY HAWAIIAN LOUNGE score for FreshNestHub 27 "why do you feel sleepy after a big meal?" (GeneralUser GS; new genre): the lazy after-lunch hour.
G major at 76 bpm, a slack-key steel guitar picking pattern, ukulele chunks on 2 and 4, upright bass, brushes, vibraphone answers and a 'lap steel' = an original
melody that SLIDES (chromatic glissandos into every target note, a slide DOWN whenever someone nods off).
FOLLOWS THE STORY: the hook sags on 'meal' (slide down + bass drop); the myth part is sneaky pizzicato; 'you're out' = the band stops dead; the board explanations get a thin
groove (bass + brushes + soft uke); the meal brings the full lounge; 'turned down' / 'nudges it down' = the score itself DIMS (a low-pass sweep, the music is the dimmer);
part 3 (staying awake) brightens with marimba and a fuller kit; the doctor line is held strings only; the recap + send = full band and a last slide up."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("SHOTS = [")[0])
S = {k: st for k, st, _ in SHOTLIST}; TN = T("i1", "meal") - 0.05
GTR, UKE, BAS, STL, VIB, MAR, STR, PIZ, CLA, DR = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
PROG = {GTR: 25, UKE: 24, BAS: 32, STL: 26, VIB: 11, MAR: 12, STR: 48, PIZ: 45, CLA: 71}
VOL = {GTR: 84, UKE: 74, BAS: 104, STL: 88, VIB: 82, MAR: 86, STR: 62, PIZ: 90, CLA: 80, DR: 76}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 76
CH = {"G": (43, [55, 59, 62, 67]), "Em": (40, [55, 59, 64, 67]), "C": (36, [55, 60, 64, 67]), "D7": (38, [54, 57, 60, 62]), "Am": (45, [57, 60, 64, 69]), "Cm": (36, [55, 60, 63, 67])}
PROGS = {"main": ["G", "Em", "C", "D7"], "lazy": ["G", "C", "G", "D7"], "sneak": ["Em", "Am", "Em", "D7"], "dim": ["G", "Cm", "G", "D7"]}


def groove(t0, t1, prog="main", level=2):
    """1: bass + brushes + soft uke (explanations). 2: + slack-key picking. 3: + vibes pad + marimba (part 3 / the end)."""
    t = t0; b = 0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for off, st in ((0, 0), (1.5, 7), (2, 12), (3, 7)):
            if t + off * BEAT < t1: n(t + off * BEAT, BAS, root + st, 90 if off in (0, 2) else 70, BEAT * 0.7)
        for q in range(8):
            tq = t + q * BEAT / 2
            if tq < t1: n(tq, DR, 42, 34 + (12 if q % 2 == 0 else 0), 0.05)
            if q in (2, 6) and tq < t1: n(tq, DR, 38, 48 if level == 1 else 62, 0.06)
        for off in (1, 3):
            if t + off * BEAT < t1:
                for k in vo[1:]: n(t + off * BEAT, UKE, k + 12, 46 if level == 1 else 60, BEAT * 0.25)
        if level >= 2:
            pat = [vo[0] + 12, vo[2] + 12, vo[1] + 12, vo[3] + 12, vo[2] + 12, vo[1] + 12, vo[3] + 12, vo[2] + 12]
            for q, k in enumerate(pat):
                tq = t + q * BEAT / 2
                if tq < t1: n(tq, GTR, k, 62 if q % 2 == 0 else 50, BEAT * 0.45)
        if level >= 3:
            for k in vo: n(t, VIB, k + 12, 40, BEAT * 3.5)
            for q in (0, 1.5, 2.5, 3):
                if t + q * BEAT < t1: n(t + q * BEAT, MAR, vo[int(q * 2) % 4] + 24, 70, BEAT * 0.3)
        t += 4 * BEAT; b += 1


def slide(t, k0, k1, ch=STL, v=88, hold=0.5, rate=0.035):
    """a lap-steel slide: chromatic run from k0 to k1, then hold k1."""
    st = 1 if k1 > k0 else -1; ks = list(range(k0, k1, st))
    for j, k in enumerate(ks): n(t + j * rate, ch, k, v - 12, rate * 1.1)
    n(t + len(ks) * rate, ch, k1, v, hold)


TUNE = [(0, 71, 74, 1.0), (1.5, 72, 71, 0.4), (2, 67, 69, 0.9), (3, 64, 67, 1.4), (4.5, 69, 71, 0.4), (5, 72, 74, 0.9), (6, 76, 79, 1.6)]


def tune(t0, v=86, ch=STL, tr=0, gap=BEAT, n_=7):
    for off, k0, k1, d in TUNE[:n_]: slide(t0 + off * gap, k0 + tr, k1 + tr, ch, v, d * gap)


def nod(t, v=92):
    """somebody nods off: a long slide down + a soft low bass."""
    slide(t, 74, 62, STL, v, 0.8, 0.05); n(t + 0.6, BAS, 38, 80, 0.8)


def stab(t, chord="G", v=104, d=0.4):
    root, vo = CH[chord]
    n(t, BAS, root, v, d); n(t, DR, 36, v - 10, 0.1); n(t, DR, 49, v - 30, 0.4)
    for k in vo: n(t, GTR, k + 12, v - 14, d); n(t, VIB, k + 12, v - 30, d * 1.5)


def sneak(t0, t1, v=84):
    t = t0; b = 0; line = [52, 55, 57, 58, 59, 57, 55, 50]
    while t < t1 - 0.05:
        n(t, PIZ, line[b % 8], v, BEAT * 0.3); n(t + BEAT / 2, DR, 42, 40, 0.05); t += BEAT; b += 1


def hold(t0, t1, chord="G", v=54):
    root, vo = CH[chord]
    for k in vo[:3]: n(t0, STR, k, v, t1 - t0)
    n(t0, BAS, root, v + 20, t1 - t0)


# ---- hook: uke + steel tune already playing; on 'meal' it sags (slide down) and the bass drops
groove(0.0, TN, "lazy", 1); tune(0.05, 80, STL, 0, BEAT * 0.55, 4); nod(TN, 96)
hold(TN + 0.2, S["S1"], "Em", 48); n(T("i1", "brain"), VIB, 79, 80, 0.8)
# the myth: sneaky
groove(S["S1"], S["S1b"], "lazy", 1); sneak(S["S1b"], S["S2"] - 0.05, 86)
stab(T("i2", "steals") - 0.1, "Em", 92, 0.3)
for j, k in enumerate((67, 64, 60, 55)): n(T("i2", "dry") - 0.1 + j * 0.12, PIZ, k, 84, 0.12)
n(T("i2", "out") - 0.05, BAS, 31, 110, 1.2); n(T("i2", "out") - 0.05, DR, 35, 110, 0.3)
# scientists checked: vibes question; the bust
for j, k in enumerate((71, 74, 76, 79)): n(S["S2"] + 0.1 + j * 0.18, VIB, k, 76, 0.3)
sneak(S["S2"] + 0.8, S["S2b"], 74); stab(T("i3", "myth") - 0.05, "C", 118, 0.6)
# the nap excuse: lazy steel
groove(S["S3"], S["S4"], "lazy", 2); nod(T("i4", "nap") - 0.1, 86); stab(T("i4", "new") - 0.1, "G", 96, 0.4)
# two things: thin groove on the board
groove(S["S4"], S["S5"], "main", 1); n(T("a0", "two") - 0.1, VIB, 79, 80, 0.4); n(T("a0", "two") + 0.2, VIB, 83, 80, 0.4)
# part 1, body clock: the tune
groove(S["S5"], S["S6"], "main", 2); tune(S["S5"] + 0.1, 92, STL, 0, BEAT * 0.5, 5)
groove(S["S6"], S["S7"], "main", 1); n(T("a2", "waves"), VIB, 74, 70, 1.0); nod(T("a2", "dip") - 0.15, 80)
groove(S["S7"], S["S8"], "lazy", 1); slide(T("a3", "ease") - 0.1, 79, 67, STL, 70, 0.8, 0.06); nod(T("a3", "still") - 0.1, 86)
groove(S["S8"], S["S9"], "main", 1); stab(T("a4", "top") - 0.12, "C", 108, 0.5)
# part 2, the meal: full lounge
groove(S["S9"], S["S10"], "main", 2); stab(T("b1", "meal") - 0.15, "G", 112, 0.4); tune(T("b1", "meal") + 0.2, 88, STL, 0, BEAT * 0.5, 3)
groove(S["S10"], S["S11"], "main", 1)
for j in range(3): n(T("b2", "messages") - 0.2 + j * 0.3, VIB, 79 + j * 2, 70, 0.3)
groove(S["S11"], S["S12"], "dim", 1); n(T("b3", "orexin") - 0.25, VIB, 86, 90, 0.8); n(T("b3", "orexin") - 0.2, MAR, 91, 80, 0.4)
slide(T("b3", "turned") - 0.2, 79, 62, STL, 80, 1.0, 0.07)
groove(S["S12"], S["S13"], "dim", 2)
groove(S["S13"], S["S14"], "main", 1); stab(T("b5", "further") + 0.35, "Cm", 104, 0.5)
# the pizza study: a cheeky clarinet, then the time card + the snoozing sofa
groove(S["S14"], S["S15"], "lazy", 1)
for j, k in enumerate((67, 71, 74, 79, 78, 74)): n(S["S14"] + 0.2 + j * 0.25, CLA, k, 78, 0.22)
stab(T("c1", "twice") - 0.15, "C", 100, 0.3)
for j in range(8): n(S["S15"] + j * 0.2, DR, 76 if j % 2 else 77, 70, 0.05)
nod(T("c2", "Still") - 0.1, 94); hold(T("c2", "Still"), S["S16"], "Em", 50)
# not fully known: thin; settled: a stab
sneak(S["S16"], S["S16b"], 70); groove(S["S16b"], S["S17"], "main", 1); stab(T("c3", "settled") - 0.1, "G", 110, 0.5)
# part 3, stay awake: brighter, marimba, fuller kit
groove(S["S17"], S["S22"], "main", 3); stab(T("d0", "awake") - 0.15, "D7", 104, 0.4)
tune(S["S19"] + 0.05, 84, MAR, 12, BEAT * 0.45, 5)
stab(T("d4", "dont") - 0.1, "Cm", 112, 0.5)
# the doctor line: held strings only
hold(S["S22"], S["S22b"], "Am", 52); hold(S["S22b"], S["S23"], "C", 50)
# recap + send: full band, a last slide UP
groove(S["S23"], END - 1.6, "main", 3); tune(S["S23"] + 0.1, 90, STL, 0, BEAT * 0.5, 7)
slide(END - 1.7, 67, 79, STL, 100, 1.4, 0.04); stab(END - 1.6, "G", 112, 1.4)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((GTR, 44), (UKE, 84), (BAS, 64), (STL, 56), (VIB, 90), (MAR, 36), (STR, 50), (PIZ, 76), (CLA, 70)): syn.control_change(ch, 10, pan)
    acts = sorted([(t, 1, c, k, v) for t, c, k, v, d in evts] + [(t + d, 0, c, k, 0) for t, c, k, v, d in evts], key=lambda a: (a[0], a[1]))
    total = int((dur + 3) * SR); out = np.zeros((total, 2), np.float32); pos = 0
    for t, on, c, k, v in acts:
        tg = min(total, max(pos, int(t * SR)))
        if tg > pos: out[pos:tg] = np.frombuffer(syn.generate(tg - pos), np.float32).reshape(-1, 2); pos = tg
        syn.noteon(c, k, v) if on else syn.noteoff(c, k)
    if pos < total: out[pos:] = np.frombuffer(syn.generate(total - pos), np.float32).reshape(-1, 2)
    return out


def dim_sweep(x, keys, lo=520.0):
    """THE SCORE IS THE DIMMER (ep 27): crossfade to a low-passed copy where the story turns the lights down. keys = [(t, amount 0..1), ...]."""
    lp = signal.sosfiltfilt(signal.butter(2, lo, "low", fs=SR, output="sos"), x, axis=0) * 1.15
    tt = np.arange(len(x)) / SR; ks, vs = zip(*keys); w = np.interp(tt, ks, vs)[:, None]
    return x * (1 - w) + lp * w


mus = render(sorted(ev), END)
mus = signal.sosfilt(signal.butter(2, 10000, "low", fs=SR, output="sos"), mus, axis=0)
mus = dim_sweep(mus, [(0, 0), (T("i2", "out") - 0.1, 0), (T("i2", "out"), 0.9), (S["S2"], 0.9), (S["S2"] + 0.3, 0),
                      (T("b3", "turned") - 0.3, 0), (T("b3", "turned") + 0.8, 0.6), (S["S12"], 0.6), (S["S12"] + 0.4, 0.1), (T("b4", "nudges") - 0.1, 0.1), (T("b4", "down") + 0.3, 0.85), (S["S13"], 0.85), (S["S13"] + 0.4, 0),
                      (T("c2", "Still"), 0), (T("c2", "Still") + 0.6, 0.5), (S["S16"], 0.5), (S["S16"] + 0.3, 0), (END + 3, 0)])
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
