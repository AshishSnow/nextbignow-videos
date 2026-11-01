"""MIDNIGHT TANGO score for FreshNestHub 20 "is leftover rice safe?" (GeneralUser GS): a sly, dramatic tango at 116 bpm — bandoneon-style
tango accordion stabs on the marcato (4 heavy beats) and the 3-3-2 habanera for tension, pizzicato contrabass, a violin that sings the
long melodic lines, piano for the bright bits, clarinet for the comic germs, celesta for the cold/fridge chapter, string swells + timpani
on the reveals, castanets for the germ party. Opening idea: a lone accordion breathing a minor chord while a clock ticks under the CCTV
night shot; a violin slides up to 'isn't' and the whole orquesta lands a hard 'tango stop' (everyone hits beat 1 and stops dead). The GUESS
beat drops to one held violin note + the tick; 'Nope' comes back with a pizzicato flourish. New genre for the channel (tango)."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
TISNT = T("i1", "isn't") - 0.12

ACD, BS, VLN, PNO, CLA, CEL, STR, TMP, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {ACD: 23, BS: 45, VLN: 40, PNO: 0, CLA: 71, CEL: 8, STR: 48, TMP: 47}
VOL = {ACD: 96, BS: 110, VLN: 84, PNO: 76, CLA: 82, CEL: 84, STR: 74, TMP: 92, DR: 66}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 116.0
CH = {"Dm": (38, [57, 62, 65, 69]), "A7": (45, [57, 61, 64, 67]), "Gm": (43, [55, 58, 62, 67]), "Bb": (46, [58, 62, 65, 70]),
      "E7": (40, [56, 59, 62, 64]), "Am": (45, [57, 60, 64, 69]), "F": (41, [57, 60, 65, 69]), "C": (48, [60, 64, 67, 72]),
      "D": (38, [57, 62, 66, 69]), "G": (43, [55, 59, 62, 67])}
PROGS = {"noir": ["Dm", "Dm", "A7", "A7"], "walk": ["Dm", "Gm", "A7", "Dm"], "dark": ["Dm", "Bb", "E7", "A7"], "germ": ["Am", "Dm", "E7", "Am"],
         "cold": ["Am", "F", "C", "E7"], "fix": ["F", "C", "G", "C"], "major": ["D", "G", "A7", "D"], "end": ["F", "G", "C", "C"]}
MEL = {"Dm": [74, 72, 69, 65, 69], "A7": [73, 76, 79, 76, 73], "Gm": [74, 70, 67, 70, 74], "Bb": [74, 77, 74, 70, 65],
       "E7": [71, 74, 76, 74, 68], "Am": [76, 72, 69, 72, 76], "F": [77, 72, 69, 72, 77], "C": [76, 79, 84, 79, 76],
       "D": [78, 74, 69, 74, 78], "G": [79, 74, 71, 74, 79]}


def tango(t0, t1, prog="noir", level=2, hab=False, half=False):
    """level 1: pizz bass + soft accordion; 2: + marcato accordion chords + castanet ticks; 3: + violin melody. hab = 3-3-2 habanera feel."""
    bt = BEAT * (2 if half else 1); bar = 4 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        hits = [0, 1.5, 3] if hab else [0, 1, 2, 3]
        for j, q in enumerate(hits):
            tq = t + q * bt
            if tq >= t1 - 0.05: break
            n(tq, BS, root - 12 + (7 if j == 2 and not hab else 0), 108 if j == 0 else 92, bt * 0.5)
            if level >= 2:
                for i_, k in enumerate(vo): n(tq + 0.004 * i_, ACD, k, (92 if j == 0 else 76) + (8 if hab else 0), bt * (0.45 if not hab else 0.6))
            elif j in (0, 2):
                for i_, k in enumerate(vo[:3]): n(tq, ACD, k, 64, bt * 0.9)
        if level >= 2 and b % 2 == 1: n(t + 3.5 * bt, DR, 85, 56, 0.1); n(t + 3.75 * bt, DR, 85, 50, 0.1)          # castanet pickup
        if level >= 3 and b % 2 == 0:
            for j, k in enumerate(MEL[ch]):
                tj = t + j * bt * 0.8
                if tj < t1 - 0.05: n(tj, VLN, k, 86 if j in (0, 3) else 74, bt * 0.75)
        t += bar; b += 1


def stop_hit(t, chord="Dm", v=112, d=0.5):
    """the 'tango stop': everyone hits one chord and stops dead."""
    root, vo = CH[chord]
    for i_, k in enumerate(vo): n(t + 0.003 * i_, ACD, k, v, d); n(t + 0.003 * i_, STR, k, v - 20, d * 1.6)
    n(t, BS, root - 12, 116, d); n(t, TMP, root - 12, v, 0.8); n(t, PNO, root - 12, v - 10, d); n(t, PNO, root + 12, v - 16, d)


def swell(t0, dur, chord="Dm", v=70):
    root, vo = CH[chord]
    for k in vo[:3]: n(t0, STR, k - 12, v, dur)


def violin_long(t0, dur, k=81, v0=46, v1=96):
    nseg = max(2, int(dur / 0.22))
    for i in range(nseg):
        v = v0 + (v1 - v0) * (i / nseg) ** 1.4; n(t0 + i * dur / nseg, VLN, k, v, 0.26)


def bells(t, base=84, nn=6, v=80, ch=CEL):
    for i in range(nn): n(t + i * 0.07, ch, base + (0, 4, 7, 12, 16, 19, 24)[i % 7], v, 0.5)


def fall(t, k0=84, nn=6, d=0.07, ch=CLA):
    for i in range(nn): n(t + i * d, ch, k0 - 2 * i, 84 - 4 * i, d * 1.4)


def clar_lick(t0, k0=72, v=88):
    """the germ motif: a cheeky clarinet chromatic wiggle."""
    for i, (dk, dd) in enumerate(((0, 0), (1, 0.09), (0, 0.18), (-1, 0.27), (4, 0.4), (7, 0.55))): n(t0 + dd, CLA, k0 + dk, v - 3 * i, 0.16)


def pizz_run(t0, k0=62, nn=5, d=0.08):
    for i in range(nn): n(t0 + i * d, BS, k0 + (0, 3, 7, 10, 12, 15)[i % 6], 96, 0.15)


def tick(t0, t1, gap=0.5, v=48):
    t = t0
    while t < t1: n(t, DR, 37, v, 0.1); t += gap


SLOW = []
# HOOK: lone accordion breathing Dm + clock tick under the CCTV night; violin slides up to ISN'T; tango stop
for e in range(int(max(0.5, TISNT - 0.2) / (BEAT * 2)) + 1):
    te = e * BEAT * 2
    if te < TISNT - 0.15:
        for k in CH["Dm"][1][:3]: n(te, ACD, k, 58 + 6 * (e % 2), BEAT * 1.8)
tick(0.0, TISNT - 0.1, 0.5, 46); violin_long(max(0.0, TISNT - 1.5), 1.4, 81, 36, 96)
stop_hit(TISNT, "Dm", 116, 0.6)
tango(S["S0b"], S["S1"] - 0.05, "noir", 2, True); swell(T("i2", "hours") - 0.12, 2.0, "Dm", 66)
tango(S["S1"], S["S2"] - 0.05, "walk", 2); stop_hit(T("i3", "pebbles") - 0.12, "A7", 104, 0.4)
# part 1: the stowaway
stop_hit(S["S2"] + 0.05, "Dm", 96, 0.3); tango(S["S2"] + 0.3, S["S2b"] - 0.05, "walk", 2); bells(T("a1", "stowaway,") - 0.12, 86, 5, 74)
tango(S["S2b"], S["S3"] - 0.05, "germ", 1); clar_lick(T("a1", "germ") - 0.05, 72, 90)
tango(S["S3"], S["S3b"] - 0.05, "germ", 2, True); fall(T("a2", "hides") - 0.1, 81, 5, 0.08, CLA); n(T("a2", "spore,") - 0.12, TMP, 38, 96, 0.6)
tango(S["S3b"], S["S4"] - 0.05, "walk", 1); pizz_run(T("a2", "seed") - 0.1, 62); stop_hit(T("a2", "armour.") - 0.12, "Gm", 100, 0.35)
tango(S["S4"], S["S4b"] - 0.05, "major", 2); stop_hit(T("a3", "crack") - 0.12, "A7", 104, 0.4)
tango(S["S4b"], S["S5"] - 0.05, "walk", 1); bells(T("a3", "asleep.") - 0.15, 79, 4, 66)
tango(S["S5"], S["S6"] - 0.05, "major", 1, False, True); n(T("a4", "fine.") - 0.12, PNO, 74, 84, 0.6)
# part 2: the warm hours — habanera tension
stop_hit(S["S6"] + 0.05, "Dm", 106, 0.4); tango(S["S6"] + 0.4, S["S6b"] - 0.05, "dark", 2, True); swell(S["S6"] + 0.4, max(0.6, S["S6b"] - S["S6"] - 0.4), "Bb", 64)
tango(S["S6b"], S["S7"] - 0.05, "dark", 2, True); stop_hit(T("b1", "wakes") - 0.12, "E7", 110, 0.5)
tango(S["S7"], S["S7b"] - 0.05, "germ", 2)
for j, w in enumerate(("hatch,", "eat,", "multiply.")): n(T("b2", w) - 0.1, CLA, (69, 72, 76)[j], 90, 0.25)
tango(S["S7b"], S["S8"] - 0.05, "germ", 2, True); clar_lick(T("b2", "double") - 0.12, 76, 88)
tango(S["S8"], S["S8b"] - 0.05, "germ", 2)
for j, w in enumerate(("four", "eight,")): pizz_run(T("b3", w) - 0.1, 62 + 5 * j, 4)
tango(S["S8b"], S["S9"] - 0.05, "dark", 2, True); stop_hit(T("b3", "crowd.") - 0.12, "A7", 106, 0.4)
tango(S["S9"], S["S10"] - 0.05, "germ", 3); clar_lick(S["S9"] + 0.2, 76, 92); stop_hit(T("b4", "toxin.") - 0.12, "Dm", 112, 0.5); n(T("b4", "toxin.") - 0.12, TMP, 38, 110, 1.0)
tango(S["S10"], S["S10b"] - 0.05, "dark", 2, True); stop_hit(T("b5", "shrugs") - 0.12, "E7", 108, 0.4)
tango(S["S10b"], S["S11"] - 0.05, "walk", 2); stop_hit(T("b5", "still") - 0.12, "Dm", 112, 0.5); SLOW.append((T("b5", "still") + 0.4, 0.5))
tango(S["S11"], S["S12"] - 0.05, "noir", 2, True); swell(T("b6", "earlier,") - 0.12, 1.6, "Dm", 70)
tango(S["S12"], S["S12b"] - 0.05, "dark", 1, False, True); fall(T("b7", "throwing") - 0.12, 76, 6, 0.1, CLA)
tango(S["S12b"], S["S13"] - 0.05, "noir", 2); stop_hit(T("b7", "classic") - 0.12, "A7", 104, 0.4)
# the guess: one held violin note + tick; NOPE = pizz flourish + cold celesta
violin_long(S["S13"], max(0.8, S["S13b"] - 0.1 - S["S13"]), 76, 46, 80); tick(S["S13"] + 0.2, S["S13b"] - 0.1, 0.5, 50)
stop_hit(S["S13b"] + 0.02, "Am", 108, 0.4); pizz_run(S["S13b"] + 0.05, 69, 5, 0.06)
tango(S["S13b"] + 0.4, S["S14"] - 0.05, "cold", 1, False, True); bells(T("c2", "slows") - 0.1, 84, 6, 80)
# part 3: the pebbles — cold, celesta
stop_hit(S["S14"] + 0.05, "Am", 100, 0.3); tango(S["S14"] + 0.3, S["S15"] - 0.05, "cold", 2); stop_hit(T("d1", "hard") - 0.12, "E7", 108, 0.4)
tango(S["S15"], S["S16"] - 0.05, "cold", 1); bells(T("d2", "swells.") - 0.12, 79, 5, 76)
tango(S["S16"], S["S16b"] - 0.05, "cold", 2, True)
for j in range(4): n(T("d3", "squeeze") - 0.1 + 0.15 * j, CEL, 88 - 3 * j, 80, 0.3)
tango(S["S16b"], S["S17"] - 0.05, "cold", 2); n(T("d4", "retrogradation.") - 0.15, TMP, 45, 104, 0.8); stop_hit(T("d4", "retrogradation.") - 0.15, "Am", 100, 0.35)
tango(S["S17"], S["S17b"] - 0.05, "major", 2); violin_long(S["S17"] + 0.1, 1.2, 78, 40, 88)
tango(S["S17b"], S["S18"] - 0.05, "major", 2); n(T("d5", "cold") - 0.1, PNO, 81, 86, 0.6)
# part 4: the fix — major, piano + violin
stop_hit(S["S18"] + 0.05, "F", 100, 0.3); tango(S["S18"] + 0.3, S["S19"] - 0.05, "fix", 2)
tango(S["S19"], S["S19b"] - 0.05, "fix", 2); bells(T("e2", "hour.") - 0.12, 84, 5, 80)
tango(S["S19b"], S["S20"] - 0.05, "fix", 1); n(T("e2", "quicker.") - 0.12, PNO, 84, 86, 0.5)
for j, sid in enumerate(("S20", "S20b", "S20c")):
    tango(S[sid], (S["S20b"], S["S20c"], S["S21"])[j] - 0.05, "fix", 2 + (j == 2))
    n(S[sid] + 0.12, PNO, (72, 76, 79)[j], 92, 0.5); n(S[sid] + 0.12, CEL, (84, 88, 91)[j], 80, 0.5)
tango(S["S21"], S["S22"] - 0.05, "noir", 2, True); stop_hit(T("e4", "Bin") - 0.1, "Dm", 112, 0.5); n(T("e4", "Bin") - 0.1, TMP, 38, 112, 1.0)
tango(S["S22"], S["S23"] - 0.05, "major", 3); bells(T("f1", "fine,") - 0.12, 86, 6, 82)
# recap + end
tango(S["S23"], S["S24"] - 0.05, "fix", 3)
for j, w in enumerate(("cool", "eat", "once,", "hot.")): n(T("g1", w) - 0.1, PNO, (72, 76, 79, 84)[j], 94, 0.5); n(T("g1", w) - 0.1, CEL, (84, 88, 91, 96)[j], 80, 0.5)
tango(S["S24"], END - 1.8, "end", 2)
stop_hit(END - 1.8, "C", 114, 1.6); bells(END - 1.75, 84, 7, 90); n(END - 1.8, VLN, 84, 90, 1.5)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((ACD, 54), (BS, 64), (VLN, 82), (PNO, 44), (CLA, 36), (CEL, 90), (STR, 64), (TMP, 60)): syn.control_change(ch, 10, pan)
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
