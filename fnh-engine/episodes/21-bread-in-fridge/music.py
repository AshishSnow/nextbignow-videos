"""RAGTIME BAKERY score for FreshNestHub 21 "does the fridge make bread go stale faster?" (GeneralUser GS): a bouncy stride / ragtime at 112 bpm: honky-tonk piano (left-hand oom-pah, right-hand syncopated figures),
tuba bass, banjo chords, a cheeky clarinet + trombone for the jokes. Opening idea: a solo woodblock + tuba locks to Chubby's hammer swings and the band falls in on FASTER. New genre for the channel (ragtime).
The score FOLLOWS THE STORY (craft note, also the curriculum's 'music that follows the story'): a lullaby music-box for the tucked-in loaf; a varispeed 'aging' ritard; a thin oom-pah under explanations (voice first); the guess
drops to one piano note + a tick; the race is double-time rag; the cold is celesta + pizzicato; THE FREEZER LITERALLY FREEZES THE BAND (a ritard to a held glass chord); the toaster's POP restarts the full band."""
import sys, json, math, numpy as np, soundfile as sf, tinysoundfont
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SF2 = f"{R}/assets/sf/gugs/GeneralUser-GS.sf2"; SR = 48000
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
exec(open(f"{_D}/anim_shots.py").read().split("def lt(")[0])
S = {k: st for k, st, _ in SHOTLIST}
PNO, TUB, BAN, CLA, TBN, CEL, PIZ, STR, DR = 0, 1, 2, 3, 4, 5, 6, 7, 9
PROG = {PNO: 3, TUB: 58, BAN: 105, CLA: 71, TBN: 57, CEL: 8, PIZ: 45, STR: 49}
VOL = {PNO: 98, TUB: 104, BAN: 74, CLA: 86, TBN: 82, CEL: 92, PIZ: 92, STR: 72, DR: 70}
ev = []


def n(t, ch, k, v, d):
    if 0 <= t < END + 3 and d > 0: ev.append((t, ch, int(k), int(max(1, min(127, v))), d))


BEAT = 60 / 112.0
CH = {"C": (36, [60, 64, 67]), "F": (41, [60, 65, 69]), "G7": (43, [59, 62, 65, 67]), "A7": (45, [61, 64, 67]), "D7": (38, [60, 62, 66]), "Am": (45, [60, 64, 69]), "Dm": (38, [62, 65, 69]), "E7": (40, [59, 62, 68]), "Eb": (39, [63, 67, 70])}
PROGS = {"rag": ["C", "A7", "D7", "G7"], "turn": ["C", "F", "G7", "C"], "minor": ["Am", "E7", "Am", "Dm"], "cold": ["Am", "F", "Dm", "E7"], "big": ["F", "D7", "G7", "C"]}
RH = [(0, 0), (0.5, 2), (0.75, 1), (1.25, 3), (1.75, 2), (2.25, 1), (2.75, 3), (3.5, 2)]


def rag(t0, t1, prog="rag", level=2, half=False):
    """level 1: oom-pah only (voice first); 2: + banjo + a soft right hand; 3: + the full syncopated right hand + clarinet fills."""
    bt = BEAT * (2 if half else 1); bar = 4 * bt; b = 0; t = t0
    while t < t1 - 0.05:
        ch = PROGS[prog][b % 4]; root, vo = CH[ch]
        for q in range(4):
            tq = t + q * bt
            if tq >= t1 - 0.05: break
            if q % 2 == 0:
                n(tq, TUB, root - (0 if q == 0 else 5) + 12 * (root < 40), 100, bt * 0.7); n(tq, PNO, root + 12, 66 if level == 1 else 80, bt * 0.5)
            else:
                for k in vo: n(tq, PNO, k, 54 if level == 1 else 68, bt * 0.4)
                if level >= 2: n(tq, DR, 42, 50, 0.08)
            if level >= 2 and q % 2 == 1:
                for k in vo: n(tq + 0.002, BAN, k + 12, 62, bt * 0.3)
        if level >= 3:
            top = sorted(vo) + [vo[0] + 12]
            for off, ix in RH:
                tq = t + off * bt
                if tq < t1 - 0.05: n(tq, PNO, top[ix % len(top)] + 12, 96 if off in (0, 0.75) else 84, bt * 0.3)
            if b % 4 == 3:
                for j, k in enumerate((72, 74, 76, 79)): n(t + (2 + j * 0.5) * bt, CLA, k, 80, bt * 0.45)
        t += bar; b += 1


def hit(t, chord="C", v=112, d=0.5):
    root, vo = CH[chord]
    n(t, TUB, root, v, d); n(t, TBN, root + 12, v - 6, d)
    for k in vo: n(t, PNO, k + 12, v - 4, d); n(t, CLA, k + 12, v - 26, d * 0.8)
    n(t, DR, 49, v - 14, 0.3)


def bells(t, base=84, nn=6, v=80, ch=CEL):
    for j in range(nn): n(t + j * 0.07, ch, base + (0, 4, 7, 12, 16, 19, 24)[j % 7], v, 0.3)


def fall(t, k0=84, nn=6, d=0.07, ch=CLA):
    for j in range(nn): n(t + j * d, ch, k0 - j * 2, 82, d * 1.1)


def trom_slide(t, k0=55, up=True, nn=7):
    for j in range(nn): n(t + j * 0.05, TBN, k0 + (j if up else -j), 86, 0.07)


def tick(t0, t1, gap=0.5, v=48):
    t = t0
    while t < t1: n(t, DR, 76, v, 0.05); t += gap


def lullaby(t0, t1):
    t = t0; mel = [79, 76, 72, 76, 79, 84, 79, 76]; j = 0
    while t < t1: n(t, CEL, mel[j % 8], 78, 0.4); t += BEAT * 0.75; j += 1


SLOW = []
# ---- hook: woodblock + tuba lock to the hammer; band on FASTER
tf = T("i1", "faster") - 0.12; tstop = T("i1", "than")
tq = 0.28
while tq < tstop:
    n(tq, DR, 76, 100, 0.08); n(tq, TUB, 36, 96, 0.2); tq += 0.62
hit(tf, "G7", 116, 0.45); rag(tf + 0.5, S["S1"] - 0.1, "rag", 2)
# tucked-in loaf: lullaby, then the ageing ritard
lullaby(S["S1"], S["S1b"]); trom_slide(S["S1b"], 60, False, 8); hit(T("i2", "aging") - 0.1, "Am", 100, 0.6); SLOW.append((T("i2", "aging") + 0.2, 0.9))
n(S["S2"], STR, 48, 56, S["S3"] - S["S2"]); n(S["S2"], STR, 55, 50, S["S3"] - S["S2"]); n(T("i3", "isn't"), CLA, 67, 74, 0.5); n(T("i3", "dry.") - 0.1, CLA, 60, 74, 0.8)
# myth + sealed box
rag(S["S3"], S["S3b"], "turn", 1); fall(T("a1", "dried") - 0.1, 84, 5)
rag(S["S3b"], S["S3c"], "minor", 1); hit(T("a1", "hard") - 0.15, "Dm", 110, 0.4)
rag(S["S3c"] + 0.45, S["S4"], "minor", 1)
tick(S["S4"], T("a2", "Nowhere."), 0.5, 52); n(S["S4"], PIZ, 45, 88, 0.3); n(S["S4"] + 0.5, PIZ, 48, 88, 0.3); n(S["S4"] + 1, PIZ, 52, 88, 0.3); hit(T("a2", "Nowhere.") - 0.1, "E7", 104, 0.35)
rag(S["S4b"], S["S5"], "cold", 1); n(T("a2", "locked") - 0.1, CEL, 60, 90, 0.4); n(T("a2", "locked") + 0.1, CEL, 55, 90, 0.4)
# culprit
rag(S["S5"], S["S5b"], "minor", 1); hit(T("a3", "starch") - 0.1, "Am", 114, 0.6); n(T("a3", "starch"), TBN, 45, 96, 0.8)
# baking, cooling, setting
rag(S["S6"], S["S6b"], "turn", 1, half=False); bells(T("b1", "swells,") - 0.1, 72, 6, 74)
rag(S["S6b"], S["S7"], "turn", 2); trom_slide(T("b1", "soft.") - 0.2, 60, True, 6)
rag(S["S7"], S["S7b"], "cold", 1); rag(S["S7b"], S["S8"], "cold", 1, True); bells(T("b2", "crystals.") - 0.12, 84, 7, 90)
rag(S["S8"], S["S8b"], "cold", 1); hit(T("b3", "feels") - 0.1, "Dm", 108, 0.3); rag(T("b3", "feels") + 0.4, S["S9"], "minor", 1)
rag(S["S9"], T("b4", "setting.") - 0.15, "turn", 1); hit(T("b4", "setting.") - 0.12, "G7", 112, 0.8)
# the guess: band stops, a tick + one piano note per place
tick(S["S10"], S["S10b"] - 0.1, 0.5, 56)
for w, k in (("counter,", 60), ("freezer,", 64), ("fridge?", 67)): n(T("c1", w) - 0.1, PNO, k + 12, 96, 0.4)
# the race: double-time rag
hit(S["S10b"] + 0.05, "C", 118, 0.25); rag(S["S10b"] + 0.3, S["S11"], "rag", 3)
rag(S["S11"], S["S12"], "cold", 1); bells(T("c2", "cold") - 0.1, 76, 6, 78)
rag(S["S12"], S["S13"], "rag", 2); hit(T("c3", "twice") - 0.12, "G7", 106, 0.3)
rag(S["S13"], S["S13b"], "turn", 1); n(S["S13b"], TBN, 48, 88, 0.3); trom_slide(S["S13b"] + 0.1, 48, True, 10); bells(T("c4", "weird") - 0.1, 84, 7, 88)
# the freezer freezes the band
rag(S["S14"], S["S14b"] + 1.2, "cold", 2); SLOW.append((S["S14b"] + 0.1, 1.2))
for k in (64, 69, 72, 76): n(S["S14b"] + 1.3, STR, k, 58, S["S15"] - S["S14b"] - 1.3); n(S["S14b"] + 1.3, CEL, k + 12, 66, 0.8)
# recap: slow + fast + paused in the band
for w, k in (("slow,", 60), ("fast,", 67), ("paused.", 72)): n(T("d2", w) - 0.1, PNO, k + 12, 96, 0.5)
rag(S["S15"], T("d2", "paused.") - 0.2, "turn", 1)
# back from the dead: a spooky organ-ish tremolo, then the band wakes
for j in range(int((T("e1", "back") - S["S16"]) / 0.12)): n(S["S16"] + j * 0.12, STR, 57 + (j % 2) * 3, 50, 0.11)
hit(T("e1", "back") - 0.12, "C", 118, 0.5); rag(T("e1", "back") + 0.35, S["S17"], "turn", 2)
rag(S["S17"], S["S17b"], "turn", 1); rag(S["S17b"], S["S17c"], "big", 2); n(S["S17c"], DR, 49, 110, 0.4)
rag(S["S17c"] + 0.05, S["S18"], "rag", 3)
hit(T("e3", "one-time") + 0.08, "F", 104, 0.3); rag(S["S18"] + 0.3, S["S18b"], "turn", 1); rag(S["S18b"], S["S18c"], "minor", 1); fall(T("e3", "faster") - 0.1, 76, 6, 0.06, TBN)
rag(S["S18c"], S["S19"], "turn", 2)
rag(S["S19"], S["S19b"], "minor", 1); rag(S["S19b"], S["S20"], "minor", 1, True); hit(T("f1", "crime") - 0.12, "F", 96, 0.3)
rag(S["S20"], S["S20b"], "cold", 1); bells(S["S20"] + 0.1, 84, 7, 84)
for w, k in (("Slice", 72), ("wrap", 76), ("freeze", 79)): n(T("f2", w) - 0.1, CEL, k, 92, 0.5)
rag(S["S20b"], S["S21"], "turn", 1)
rag(S["S21"], S["S21b"], "turn", 2); hit(S["S21b"] + 0.05, "C", 118, 0.2); n(S["S21b"] + 0.1, TBN, 48, 80, 0.5)
rag(S["S21b"] + 0.5, S["S22"], "turn", 1)
rag(S["S22"], S["S23"], "big", 2)
for w, k in (("now,", 72), ("later,", 76), ("else.", 84)): n(T("g1", w) - 0.2, PNO, k, 100, 0.5)
rag(S["S23"], END - 1.8, "rag", 3); hit(END - 1.8, "C", 116, 1.6); bells(END - 1.75, 84, 7, 92)


def render(evts, dur):
    syn = tinysoundfont.Synth(samplerate=SR, gain=-9); sid = syn.sfload(SF2, max_voices=384)
    for ch, p in PROG.items(): syn.program_select(ch, sid, 0, p)
    syn.program_select(DR, sid, 128, 0, True)
    for ch, v in VOL.items(): syn.control_change(ch, 7, v)
    for ch, pan in ((PNO, 56), (TUB, 64), (BAN, 82), (CLA, 40), (TBN, 76), (CEL, 90), (PIZ, 44), (STR, 64)): syn.control_change(ch, 10, pan)
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


def ritard(x, t0, dur, floor=0.45):
    i0 = int(t0 * SR); L = int(dur * SR)
    if i0 + L >= len(x): return
    sp = 1 - (1 - floor) * np.linspace(0, 1, L) ** 1.4
    pos = i0 + np.cumsum(sp)
    seg = np.stack([np.interp(pos, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1) * np.linspace(1, 0.3, L)[:, None]
    x[i0:i0 + L] = seg


for t0, d in SLOW: ritard(mus, t0, d)
mus = signal.sosfilt(signal.butter(2, 9500, "low", fs=SR, output="sos"), mus, axis=0)
mus = np.tanh(mus / (np.abs(mus).max() + 1e-9) * 1.2) / np.tanh(1.2)
mus = mus[: int((END + 0.05) * SR)]; f = int(0.8 * SR); mus[-f:] *= np.linspace(1, 0, f)[:, None]
sf.write(f"{B}/work/music.wav", (mus * 0.89).astype(np.float32), SR, subtype="FLOAT")
print("score", round(len(mus) / SR, 2))
