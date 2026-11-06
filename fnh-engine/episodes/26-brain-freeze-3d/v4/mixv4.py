"""Ep 26 (3D): VO + procedural 'curious lo-fi synth' bed (ducked) + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
import json, subprocess, numpy as np, soundfile as sf, sys
from scipy import signal
B = "/home/claude/studio/projects/26-brain-freeze-v4"; Z = sys.argv[1]
TL = json.load(open(f"{Z}/tl4.json")); END = TL["end"]
SR = 48000; NS = int(round(END * SR)); rng = np.random.default_rng(26); db = lambda x: 10 ** (x / 20)
L = lambda i: TL["lines"][i][0]; LE = lambda i: TL["lines"][i][1]
def WT(i, w):
    for q in TL["words"]:
        if q[2] == i and ''.join(c for c in q[0].lower() if c.isalpha() or c == "'").startswith(w): return q[1]
    return L(i)
exec(open(f"{B}/scripts/sfx_lib.py").read())
v, _ = sf.read(f"{B}/work/vo.wav", dtype="float32"); v = v if v.ndim == 1 else v.mean(1)
vo = np.zeros(NS, np.float32); vo[:min(NS, len(v))] = v[:NS]
# ---------------- music: 84 bpm, Am7 Fmaj7 Cmaj7 G6, warm pad + pluck arp + soft kick/hat ----------------
bpm = 118; beat = 60 / bpm; t = np.arange(NS) / SR
def note(m): return 440 * 2 ** ((m - 69) / 12)
prog = [[60, 64, 67, 72], [57, 60, 64, 69], [53, 57, 60, 65], [55, 59, 62, 67]]
mus = np.zeros(NS, np.float32)
tAlarm = WT("b2", "picks"); tB3 = L("b3"); tB4 = L("b3"); tBF = WT("b3", "brain"); tC3 = L("c2"); tSlow = WT("c2", "stop")
bar = 4 * beat; nb = int(END / bar) + 2
for b in range(nb):
    ch = prog[b % 4]; s0 = int(b * bar * SR); s1 = min(NS, int((b + 1) * bar * SR))
    if s0 >= NS: break
    tt = np.arange(s1 - s0) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * tt * (1 + d)) for m in ch for d in (-0.003, 0.003)) / 8
    env = np.minimum(1, tt / 0.4) * np.minimum(1, (bar - tt) / 0.3)
    mus[s0:s1] += pad * env * 0.5
    for k in range(8):   # eighth-note pluck arp
        ts = b * bar + k * beat / 2; i0 = int(ts * SR)
        if i0 >= NS: break
        m = ch[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12; n = int(0.5 * SR); te = np.arange(n) / SR
        pl = (np.sin(2 * np.pi * note(m) * te) + 0.3 * np.sin(4 * np.pi * note(m) * te)) * np.exp(-te / 0.18) * 0.22
        j = min(NS, i0 + n); mus[i0:j] += pl[:j - i0]
    for k in range(4):   # soft kick on 1/3, hat on off-beats
        ts = b * bar + k * beat; i0 = int(ts * SR)
        if i0 >= NS: break
        if k in (0, 2):
            n = int(0.3 * SR); te = np.arange(n) / SR; kk = np.sin(2 * np.pi * np.cumsum(50 + 90 * np.exp(-te / 0.03)) / SR) * np.exp(-te / 0.12) * 0.55
            j = min(NS, i0 + n); mus[i0:j] += kk[:j - i0]
        i1 = int((ts + beat / 2) * SR); n = int(0.05 * SR)
        if i1 + n < NS: mus[i1:i1 + n] += signal.sosfilt(signal.butter(2, 7000, "high", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-np.arange(n) / SR / 0.012) * 0.08
mus = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), mus).astype(np.float32)
# x-ray tension: low-pass the band from the nerve alarm to the forehead + a drone; drop out before "Or, you know"
def seg(a, b): return (t >= a) & (t < b)
lp = signal.sosfilt(signal.butter(2, 700, "low", fs=SR, output="sos"), mus).astype(np.float32)
mask = np.clip(np.minimum((t - tAlarm + 0.2) / 0.2, (tB4 - 0.1 - t) / 0.3), 0, 1)
mus = mus * (1 - mask) + lp * mask * 1.3
drone = (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t)) * 0.25 * mask
mus += drone.astype(np.float32)
stop = np.clip((tC3 - 0.05 - t) / 0.15, 0, 1) + np.clip((t - (tSlow + 0.35)) / 0.05, 0, 1); mus *= np.clip(stop, 0, 1)
# ducking under the voice
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo ** 2, np.ones(win) / win, "same")); env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a_ = aa if x > prev else ar; prev = a_ * prev + (1 - a_) * x; g[i:i + 48] = prev
mus = mus / (np.abs(mus).max() + 1e-9) * db(-17) * (1 - 0.62 * g)
# ---------------- SFX ----------------
def ring(t0, n=3, level=-27):
    for k in range(n):
        m = int(0.38 * SR); te = np.arange(m) / SR
        x = (np.sign(np.sin(2 * np.pi * 22 * te)) * 0.5 + 0.5) * (np.sin(2 * np.pi * 1400 * te) + 0.6 * np.sin(2 * np.pi * 1750 * te)) * np.exp(-te / 0.5) * db(level)
        add(np.stack([x, x], 1).astype(np.float32), t0 + k * 0.62)
tBite = WT("i1", "bite"); tHurt = WT("i1", "hurt"); tNot = WT("i1", "not"); iw = [q for q in TL["words"] if q[2] == "i1" and q[0].lower().startswith("your")]; tYF = iw[1][1] if len(iw) > 1 else L("a1") - 0.6
tCold = L("a1"); tPanic = WT("a1", "and"); tSq = L("a2"); tBurst = WT("a2", "then"); tB1 = L("b1"); tBas = WT("b1", "basically"); tB2 = L("b2"); tSends = WT("b2", "sends")
yw = [q for q in TL["words"] if q[2] == "b2" and q[0].lower().startswith("your")]; tYF2 = yw[-1][1] if yw else LE("b2") - 0.5
tDoc = WT("b3", "doctors"); tC1 = L("c1"); tIts = WT("c1", "it's"); tAnd = WT("c1", "and"); tC2 = L("c2")
def ring(t0, n=3, level=-27):
    for k in range(n):
        m = int(0.38 * SR); te = np.arange(m) / SR
        x = (np.sign(np.sin(2 * np.pi * 22 * te)) * 0.5 + 0.5) * (np.sin(2 * np.pi * 1400 * te) + 0.6 * np.sin(2 * np.pi * 1750 * te)) * np.exp(-te / 0.5) * db(level)
        add(np.stack([x, x], 1).astype(np.float32), t0 + k * 0.62)
add(crunch(-14), tBite); add(boom(-16, 0.3), tHurt - 0.05); add(ice_crack(-17), tHurt); add(whoosh(0.3, level=-22), tNot - 0.15); add(boing(-24, 220, 0.3), tNot + 0.1)
add(boom(-15, 0.35), tYF - 0.05); add(whoosh(0.35, level=-20), tCold - 0.2); add(ice_crack(-14), tCold + 0.15); add(wind(-26, 1.2), tCold + 0.2)
add(chatter(-23, 0.9), tPanic); add(stretch(-21, 0.4, up=False), tSq); add(boom(-14, 0.3), tBurst); add(squelch(-21, 0.5), tBurst + 0.05)
add(whoosh(level=-21), tB1 - 0.2); ring(tB1 + 0.1, 3); add(buzz(-29, 1.6), tB1); add(whoosh(0.6, level=-20), tBas - 0.05)
add(buzzer(-20, 0.45), tB2); add(whoosh(0.3, level=-22), tSends - 0.1); add(boing(-21, 160, 0.45), tSends + 0.5); add(lock_click(-17), tSends + 0.75)
add(boom(-15, 0.35), tYF2 - 0.05); add(thud(-12), L("b3")); add(ice_crack(-16), L("b3") + 0.05); add(boom(-17, 0.5), L("b3") + 0.02)
add(whoosh(level=-22), tC1 - 0.2); add(squelch(-22, 0.4), WT("c1", "tongue")); add(sizzle(-27, 2.0), tIts); add(ding(-24, 1568), tAnd + 0.3)
add(whoosh(level=-22), tC2 - 0.2); add(pop(-21), tSlow); add(crunch(-16), END - 0.4)
mix = np.stack([vo, vo], 1) + np.stack([mus, mus], 1) * np.array([0.98, 1.0], np.float32) + sfx
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", "loudnorm=I=-11:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I=-11:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true", "-ar", "48000", f"{B}/work/mix.wav"], check=True)
vb = 20 * np.log10((np.sqrt(np.mean(vo[vo != 0] ** 2)) + 1e-9) / (np.sqrt(np.mean(mus ** 2)) + 1e-9)); print("VO/bed dB ~", round(vb, 1), "END", END)
