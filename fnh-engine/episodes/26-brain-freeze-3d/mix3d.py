"""Ep 26 (3D): VO + procedural 'curious lo-fi synth' bed (ducked) + per-moment SFX -> work/mix.wav (-11 LUFS, -1.5 dBTP)."""
import json, subprocess, numpy as np, soundfile as sf, sys
from scipy import signal
B = "/home/claude/studio/projects/26-brain-freeze-3d"; Z = sys.argv[1]
TL = json.load(open(f"{Z}/tl.json")); END = TL["end"]
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
bpm = 84; beat = 60 / bpm; t = np.arange(NS) / SR
def note(m): return 440 * 2 ** ((m - 69) / 12)
prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]
mus = np.zeros(NS, np.float32)
tA3, tAlarm, tB1, tFore, tB3, tBF, tC1, tC3, tSlow = L("a3"), WT("a3", "alarm"), L("b1"), WT("b2", "forehead"), L("b3"), WT("b3", "brain"), L("c1"), L("c3"), WT("c3", "slower")
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
mask = np.clip(np.minimum((t - tAlarm) / 0.2, (tB3 - 0.2 - t) / 0.3), 0, 1)
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
tBite, tFreeze, tA1, tPanic, tSq, tSnap = WT("i2", "bite"), WT("i2", "freezing"), L("a1"), WT("a1", "panic"), WT("a2", "squeeze"), WT("a2", "snap")
tNerve, tWrong, tTongue, tWarm = WT("a3", "trigeminal"), WT("b1", "wrong"), WT("c2", "tongue"), WT("c2", "warmth")
add(crunch(-15), tBite - 0.04); add(nibble(-24, 0.4), tBite + 0.1)
add(ice_crack(-15), tFreeze - 0.05); add(wind(-26, 1.4), tFreeze)
for c in (tA1 - 0.15, tA3 - 0.15, tB1 - 0.15, tB3 - 0.35, tC1 + 0.45, tC3 - 0.5): add(whoosh(level=-22), c - 0.2)
add(chatter(-25, 0.9), tPanic - 0.1); add(stretch(-23, 0.4, up=False), tSq - 0.05); add(snap(-15), tSnap - 0.02); add(boom(-20, 0.3), tSnap)
add(buzz(-28, LE("a3") - tNerve + 0.3), tNerve - 0.1); add(boom(-13), tAlarm - 0.03); add(beep(-26), tAlarm + 0.05)
add(glitch(tWrong - 0.05, -23) if False else boing(-24, 180, 0.4), tWrong - 0.05); add(boom(-13), tFore - 0.03)
add(ice_crack(-17), tBF - 0.05); add(boom(-17, 0.6), tBF)
add(squelch(-24, 0.5), tTongue); add(sizzle(-29, 2.0), tWarm)
add(pop(-22), tSlow + 0.4); add(ding(-25), tSlow + 0.45)
mix = np.stack([vo, vo], 1) + np.stack([mus, mus], 1) * np.array([0.98, 1.0], np.float32) + sfx
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", "loudnorm=I=-11:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af", f"loudnorm=I=-11:TP=-1.5:LRA=9:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true", "-ar", "48000", f"{B}/work/mix.wav"], check=True)
vb = 20 * np.log10((np.sqrt(np.mean(vo[vo != 0] ** 2)) + 1e-9) / (np.sqrt(np.mean(mus ** 2)) + 1e-9)); print("VO/bed dB ~", round(vb, 1), "END", END)
