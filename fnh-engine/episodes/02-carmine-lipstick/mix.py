"""Mix (carmine-lipstick reel, Nessa): clean VO + ducked score + short SFX (no noise beds) -> work/mix.wav"""
import json, subprocess, numpy as np, soundfile as sf
from scipy import signal
B = "/home/claude/reel-kit/english"
SR = 48000
TL = json.load(open(f"{B}/work/timeline.json")); EV, LN, END = TL["events"], TL["lines"], TL["END"]
SH = {s["id"]: s for s in TL["shots"]}
NS = int(round(END * SR)); rng = np.random.default_rng(31)
db = lambda x: 10 ** (x / 20)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/vo.wav", "-af",
                "highpass=f=75,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3400:t=q:w=1.2:g=3,highshelf=f=9000:g=1.5,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=6:release=120:makeup=2,deesser=i=0.35",
                "-ar", str(SR), "-c:a", "pcm_f32le", f"{B}/work/vo_proc.wav"], check=True)
v, _ = sf.read(f"{B}/work/vo_proc.wav", dtype="float32"); v = v if v.ndim == 1 else v[:, 0]
vo = np.zeros(NS, np.float32); i0 = int(TL["LEAD"] * SR); j0 = min(NS, i0 + len(v)); vo[i0:j0] = v[: j0 - i0]
# restore wide dynamics after compression: loud lines louder, whispers softer (smooth 60 ms ramps)
LG = {"intro": 1.0, "name": 2.5, "cactus": 0.0, "crush": -4.0, "count": 3.0, "wait": 1.0, "allergy": -1.0, "tip": 0.0, "loop": -5.5}
gl = np.zeros(NS, np.float32)
for lid, L in LN.items():
    a_, b_ = int((L["start"] - 0.06) * SR), int((L["end"] + 0.1) * SR)
    gl[max(0, a_):min(NS, b_)] = LG.get(lid, 0.0)
rw = int(0.06 * SR); gl = np.convolve(gl, np.ones(rw) / rw, "same")
vo_dry = vo.copy()
vo = vo * (10 ** (gl / 20)).astype(np.float32)
VO = np.stack([vo, vo], 1)

m, _ = sf.read(f"{B}/work/music.wav", dtype="float32"); m = m[:NS]
if len(m) < NS: m = np.pad(m, ((0, NS - len(m)), (0, 0)))
win = int(0.03 * SR); env = np.sqrt(np.convolve(vo_dry ** 2, np.ones(win) / win, "same"))
env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9) * 1.6, 0, 1)
env = np.maximum(env, (gl < -2).astype(np.float32) * (env > 0.05))  # whispers duck the music fully
g = np.zeros_like(env); prev = 0.0; aa, ar = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.4 * SR))
for i in range(0, NS, 48):
    x = env[i]; a = aa if x > prev else ar; prev = a * prev + (1 - a) * x; g[i:i + 48] = prev
M = m * (1 - 0.66 * g)[:, None]

sfx = np.zeros((NS, 2), np.float32)


def add(x, t, gain=1.0):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(NS, i + len(x))
    if j > i: sfx[i:j] += x[: j - i] * gain


# clip ambience (normalised, low)
AMB = {}
for sid, (clip, st, lev) in AMB.items():
    s = SH[sid]; dur = s["end"] - s["start"] + 0.2
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{st:.3f}", "-stream_loop", "1", "-i", f"{B}/src/{clip}.mp4", "-vn", "-af", "highpass=f=100",
                        "-t", f"{dur:.3f}", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
    if len(x) == 0: continue
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * db(-20)
    f = min(len(x) // 3, int(0.08 * SR))
    if f > 0: x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
    i0a = max(0, int((s["start"] - 0.05) * SR)); gg = g[i0a:i0a + len(x)]
    if len(gg) < len(x): gg = np.pad(gg, (0, len(x) - len(gg)))
    add(x * (1 - 0.5 * gg)[:, None], s["start"] - 0.05, db(lev))


def whoosh(dur=0.5, peak=0.55, f_lo=300, f_hi=3800, level=-21):
    n = int(dur * SR); noise = rng.standard_normal(n).astype(np.float32)
    f, t2, Z = signal.stft(noise, SR, nperseg=1024); x = t2 / dur
    fc = np.where(x < peak, f_lo * (f_hi / f_lo) ** (x / peak), f_hi * (f_lo * 1.6 / f_hi) ** ((x - peak) / (1 - peak)))
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f, 20))[:, None] - np.log2(fc)[None]) / 0.8) ** 2)
    _, w = signal.istft(Z * mask, SR, nperseg=1024); w = w[:n]; te = np.arange(n) / n
    w = w * np.where(te < peak, (te / peak) ** 2.5, np.exp(-(te - peak) / 0.12)); w = w / (np.abs(w).max() + 1e-9) * db(level)
    p = np.linspace(0, 1, n); return np.stack([w * (1 - 0.5 * p), w * (0.5 + 0.5 * p)], 1)


def boom(level=-14, tau=0.45):
    n = int(1.3 * SR); t2 = np.arange(n) / SR; fr = 32 + 80 * np.exp(-t2 / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / tau) * np.minimum(1, t2 / 0.003)
    cl = signal.sosfilt(signal.butter(2, 1800, "low", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.015)
    x = s + 0.3 * cl / np.abs(cl).max(); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def click(level=-30):
    n = int(0.03 * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def pop(level=-26, f0=900):
    n = int(0.12 * SR); t2 = np.arange(n) / SR; fr = f0 * (1 + 1.2 * np.exp(-t2 / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.03) * np.minimum(1, t2 / 0.001)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def ding(level=-26, f0=1318.5):
    n = int(1.2 * SR); t2 = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / d) for r, a, d in ((1, 1, 0.5), (2.0, 0.35, 0.25), (2.76, 0.2, 0.15)))
    x *= np.minimum(1, t2 / 0.002); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def scratch(level=-24, dur=0.32):
    n = int(dur * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [800, 5000], "band", fs=SR, output="sos"), rng.standard_normal(n))
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t2)) * np.minimum(1, t2 / 0.01) * np.exp(-t2 / 0.2)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)


def paper_tear(level=-22, dur=0.7):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = signal.sosfilt(signal.butter(2, [600, 7000], "band", fs=SR, output="sos"), rng.standard_normal(nn))
    crk = (rng.random(nn) < 0.004).astype(np.float32); crk = signal.sosfilt(signal.butter(2, 3000, "high", fs=SR, output="sos"), crk) * 6
    env = np.minimum(1, t2 / 0.03) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 9 * t2))) * np.exp(-t2 / (dur * 0.7))
    y = (x + crk) * env; y = y / (np.abs(y).max() + 1e-9) * db(level)
    return np.stack([y * 0.9, y], 1)



def ticks(t0, dur, step=0.05, level=-33):
    t = t0
    while t < t0 + dur: add(click(level), t); t += step


def thump(level=-16):
    x = boom(level, 0.12); y = click(level - 2)
    x[: len(y)] += y
    return x


def bubble(f0=600, dur=0.05, level=-28, up=True):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    fr = f0 * (1 + (1.8 if up else -0.45) * t2 / dur)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t2 / dur) ** 1.5
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def bubbles(dur, f_lo=300, f_hi=900, rate=18, level=-30, seed=1, rise=0.0):
    r = np.random.default_rng(seed); nn = int(dur * SR); out = np.zeros((nn, 2), np.float32)
    t = 0.0
    while t < dur - 0.08:
        u = t / dur
        f0 = r.uniform(f_lo, f_hi) * (1 + rise * u)
        b_ = bubble(f0, r.uniform(0.03, 0.07), level + r.uniform(-4, 2))
        i = int(t * SR); j = min(nn, i + len(b_)); pan = r.uniform(0.3, 1.0)
        out[i:j, 0] += b_[: j - i, 0] * pan; out[i:j, 1] += b_[: j - i, 1] * (1.3 - pan)
        t += r.exponential(1 / rate)
    return out


def splash(level=-18, dur=0.9, seed=3):
    r = np.random.default_rng(seed); nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = signal.sosfilt(signal.butter(2, [500, 9000], "band", fs=SR, output="sos"), r.standard_normal(nn))
    x *= np.minimum(1, t2 / 0.004) * (np.exp(-t2 / 0.09) + 0.25 * np.exp(-t2 / 0.4))
    y = np.stack([x, x], 1) / (np.abs(x).max() + 1e-9)
    y[: len(y)] += bubbles(dur, 700, 2200, 40, -14, seed)[: len(y)] * 1.0
    return y / (np.abs(y).max() + 1e-9) * db(level)


def pour(dur, level=-26, seed=5, rise=0.0):
    r = np.random.default_rng(seed); nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = r.standard_normal(nn)
    f, tt, Z = signal.stft(x, SR, nperseg=1024); u = tt / dur
    fc = 900 * (1 + rise * u)
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f, 20))[:, None] - np.log2(fc)[None]) / 0.9) ** 2)
    _, w = signal.istft(Z * mask, SR, nperseg=1024); w = w[:nn]
    w *= (0.7 + 0.3 * np.sin(2 * np.pi * 7 * t2)) * np.minimum(1, t2 / 0.08) * np.minimum(1, (dur - t2) / 0.12)
    y = np.stack([w, w * 0.9], 1) / (np.abs(w).max() + 1e-9)
    y += bubbles(dur, 400, 1100, 22, -12, seed, rise)[: nn]
    return y / (np.abs(y).max() + 1e-9) * db(level)


def glug(f0=220, level=-22):
    nn = int(0.16 * SR); t2 = np.arange(nn) / SR; fr = f0 * (1 + 0.8 * t2 / 0.16)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.05) * np.minimum(1, t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def beep(f0=880, dur=0.09, level=-28, sq=True):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = np.sign(np.sin(2 * np.pi * f0 * t2)) * 0.6 + np.sin(2 * np.pi * f0 * t2) if sq else np.sin(2 * np.pi * f0 * t2)
    x = signal.sosfilt(signal.butter(2, 4000, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.003) * np.minimum(1, (dur - t2) / 0.01)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def tape_stop(dur=0.7, level=-20, f0=520):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; u = t2 / dur
    fr = f0 * (1 - u) ** 2 + 30
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.5 * np.sign(np.sin(2 * np.pi * np.cumsum(fr * 0.5) / SR))
    x = signal.sosfilt(signal.butter(2, 2500, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.01) * (1 - u) ** 0.6
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def zap(level=-24, dur=0.35):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; fr = 1800 * np.exp(-t2 / 0.08) + 120
    x = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.12) + 0.4 * rng.standard_normal(nn) * np.exp(-t2 / 0.03)
    x = signal.sosfilt(signal.butter(2, 6000, "low", fs=SR, output="sos"), x)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def power_down(level=-24, dur=0.8):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; fr = 700 * (1 - t2 / dur) ** 1.5 + 60
    x = signal.square(2 * np.pi * np.cumsum(fr) / SR) * (1 - t2 / dur)
    x = signal.sosfilt(signal.butter(2, 1800, "low", fs=SR, output="sos"), x)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def wobble(level=-26, dur=0.9):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; fr = 500 + 220 * np.sin(2 * np.pi * 6 * t2)
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.sin(np.pi * t2 / dur)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x * 0.8, x], 1)


def siren(dur=1.0, level=-26):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; fr = np.where((t2 * 4) % 1 < 0.5, 960, 720)
    x = signal.square(2 * np.pi * np.cumsum(fr) / SR) * 0.5 + np.sin(2 * np.pi * np.cumsum(fr) / SR)
    x = signal.sosfilt(signal.butter(2, 3500, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.01) * np.minimum(1, (dur - t2) / 0.05)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def bell_ring(dur=1.4, level=-24, vol_env=None):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = sum(a * np.sin(2 * np.pi * 1180 * r_ * t2) for r_, a in ((1, 1), (2.4, 0.5), (3.9, 0.3), (5.4, 0.2)))
    trem = 0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t2))
    x = x * trem * np.minimum(1, t2 / 0.004) * np.minimum(1, (dur - t2) / 0.1)
    if vol_env is not None: x *= vol_env(t2)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def jingle(level=-20):
    out = np.zeros((int(1.4 * SR), 2), np.float32)
    for i, f0 in enumerate((1046.5, 1318.5, 1568.0, 2093.0)):
        d = ding(level - 2, f0); a = int(i * 0.08 * SR); out[a:a + len(d)] += d[: len(out) - a]
    sp = bubbles(1.0, 2500, 6000, 30, level - 10, 9)
    out[int(0.3 * SR):int(0.3 * SR) + len(sp)] += sp[: len(out) - int(0.3 * SR)]
    return out


def buzzer(level=-22, dur=0.45):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = signal.square(2 * np.pi * 110 * t2) + 0.6 * signal.square(2 * np.pi * 116 * t2)
    x = signal.sosfilt(signal.butter(2, 1600, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.005) * np.minimum(1, (dur - t2) / 0.03)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def clink(level=-28, f0=2600):
    nn = int(0.25 * SR); t2 = np.arange(nn) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * r_ * t2) * np.exp(-t2 / d) for r_, a, d in ((1, 1, 0.06), (1.48, 0.6, 0.04), (2.3, 0.4, 0.03)))
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1)


def scratch_rec(level=-18, dur=0.35):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    sp = np.where(t2 < dur * 0.45, 1.0, -0.8)
    fr = 300 + 2200 * np.abs(np.sin(np.pi * t2 / dur)) * sp
    x = signal.sosfilt(signal.butter(2, [400, 5000], "band", fs=SR, output="sos"), rng.standard_normal(nn)) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(np.abs(fr)) / SR))
    x *= np.minimum(1, t2 / 0.01) * np.minimum(1, (dur - t2) / 0.03)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x * 0.9], 1)



def kaching(level=-16):
    out = np.zeros((int(1.4 * SR), 2), np.float32)
    c = click(level + 2); out[: len(c)] += c
    for i, f0 in enumerate((2637.0, 3520.0)):
        d = ding(level, f0); a = int((0.05 + i * 0.09) * SR); out[a:a + len(d)] += d[: len(out) - a]
    for i in range(10):
        k = clink(level - 6, 2400 + 300 * (i % 4)); a = int((0.15 + i * 0.045) * SR); out[a:a + len(k)] += k[: len(out) - a]
    return out


def flutter(dur=1.0, level=-28, seed=3):
    r = np.random.default_rng(seed); nn = int(dur * SR); out = np.zeros((nn, 2), np.float32)
    t = 0.0
    while t < dur - 0.05:
        ln = int(r.uniform(0.02, 0.05) * SR); i = int(t * SR)
        x = signal.sosfilt(signal.butter(2, [1500, 8000], "band", fs=SR, output="sos"), r.standard_normal(ln)) * np.hanning(ln)
        j = min(nn, i + ln); pan = r.uniform(0.2, 1)
        out[i:j, 0] += x[: j - i] * pan; out[i:j, 1] += x[: j - i] * (1.2 - pan)
        t += r.uniform(0.03, 0.09)
    return out / (np.abs(out).max() + 1e-9) * db(level)


def spray(level=-22, dur=0.5):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = signal.sosfilt(signal.butter(2, 3500, "high", fs=SR, output="sos"), rng.standard_normal(nn)) * np.minimum(1, t2 / 0.01) * np.exp(-t2 / 0.25)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def sizzle(dur=1.2, level=-28):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    crk = (rng.random(nn) < 0.01).astype(np.float32)
    x = signal.sosfilt(signal.butter(2, 2500, "high", fs=SR, output="sos"), crk * 4 + 0.3 * rng.standard_normal(nn))
    x *= np.minimum(1, t2 / 0.1) * np.minimum(1, (dur - t2) / 0.2)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def heartbeat_sfx(t0, t1, level=-16):
    t = t0
    while t < t1 - 0.1:
        add(boom(level, 0.12), t); add(boom(level - 5, 0.1), t + 0.2); t += 0.75


def flatline(dur=1.6, level=-24):
    nn = int(dur * SR); t2 = np.arange(nn) / SR
    x = np.sin(2 * np.pi * 988 * t2) * np.minimum(1, t2 / 0.01) * np.minimum(1, (dur - t2) / 0.3)
    x = x * db(level); return np.stack([x, x], 1)


def waves(dur, level=-30, seed=7):
    r = np.random.default_rng(seed); nn = int(dur * SR); tt = np.arange(nn) / SR
    x = signal.sosfilt(signal.butter(2, [200, 2500], "band", fs=SR, output="sos"), r.standard_normal(nn))
    env = 0.35 + 0.65 * np.sin(np.pi * ((tt * 0.55) % 1)) ** 2
    x = x * env * np.minimum(1, tt / 0.3) * np.minimum(1, (dur - tt) / 0.3)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x * 0.95], 1)


def scan(level=-24, dur=0.6):
    nn = int(dur * SR); t2 = np.arange(nn) / SR; fr = 300 + 2400 * t2 / dur
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.5 + 0.3 * signal.sosfilt(signal.butter(2, 3000, "high", fs=SR, output="sos"), rng.standard_normal(nn))
    x *= np.sin(np.pi * t2 / dur)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)



E = EV
SS = {s["id"]: s["start"] for s in TL["shots"]}
for s in TL["shots"][1:]:
    k = s["trans"]
    if k in ("zoomblur", "whip"): add(whoosh(0.4, peak=0.55, f_lo=250, f_hi=4500, level=-23), s["start"] - 0.22)
    elif k == "pop": add(pop(-23, 700), s["start"] - 0.05)
    elif k == "dip": add(whoosh(0.7, peak=0.5, f_lo=150, f_hi=1500, level=-27), s["start"] - 0.35)
    elif k == "punch": add(thump(-19), s["start"])
    elif k in ("flash", "flashp"): add(click(-22), s["start"])
# intro
add(boom(-19, 0.4), 0.0); add(jingle(-28), 0.02)
add(whoosh(0.8, peak=0.8, f_lo=200, f_hi=4000, level=-24), 0.0)
add(scan(-28, 0.6), 0.15)
add(thump(-16), E["t_bugs0"] - 0.04)
for j in range(6): add(pop(-25, 900 + 120 * j), E["t_made"] - 0.2 + j * 0.09)
# carmine / cochineal
add(thump(-18), E["t_carmine"] - 0.03)
add(flutter(0.8, -29, 4), E["t_carmine"] + 0.3)
add(pop(-23, 900), E["t_cochineal"] - 0.05)
# cactus
add(ding(-27, 1568), SS["CA"] + 0.1)
add(pop(-23, 1000), E["t_mostly"] - 0.1)
# females / dried
add(ding(-30, 2093), SS["CR"] + 0.2)
for j in range(3): add(pop(-29, 1200 + 150 * j), E["t_females"] - 0.1 + j * 0.06)
add(sizzle(0.9, -34), E["t_dried"] - 0.1)
# crushed
add(whoosh(0.3, peak=0.8, f_lo=300, f_hi=3000, level=-24), E["t_crushed"] - 0.3)
add(boom(-17, 0.4), E["t_crushed"] - 0.05); add(paper_tear(-27, 0.35), E["t_crushed"] - 0.03); add(spray(-29, 0.5), E["t_crushed"])
# count
for i in range(16): add(click(-31), SS["CT"] + 0.1 + i * 0.13)
add(thump(-16), E["t_thousand"] - 0.03)
add(kaching(-20), E["t_one"] - 0.08)
# but wait
add(tape_stop(0.5, -22), E["t_but"] - 0.3)
add(pop(-22, 800), E["t_just"] - 0.15); add(pop(-20, 1300), E["t_lip2"] + 0.05)
# foods
for tk, f0 in ((E["t_yogurt"], 800), (E["t_candy"], 1000), (E["t_ice"], 1200)):
    add(pop(-21, f0), tk - 0.12); add(bubble(f0 * 0.7, 0.06, -28), tk + 0.2)
# allergy
add(beep(880, 0.12, -27), E["t_allergic"] - 0.1); add(beep(660, 0.14, -27), E["t_allergic"] + 0.06)
add(pop(-25, 700), E["t_few"] - 0.1)
# label + tip
add(scan(-27, 0.6), SS["LB"] + 0.1)
add(ding(-24, 1318.5), E["t_carmine2"] - 0.1)
add(pop(-22, 900), SS["TC"] + 0.02); add(ding(-22, 1568), E["t_twenty"] - 0.05); add(click(-22), E["t_twenty"] - 0.05)
# loop
add(ding(-30, 2093), SS["LP"] + 0.2)
add(pop(-26, 1300), E["t_yourself"] - 0.1)
add(whoosh(0.4, peak=0.85, f_lo=300, f_hi=6000, level=-23), END - 0.42)

BED = -7.5
mix = VO + M * db(BED) + sfx
sf.write(f"{B}/work/mix_pre.wav", mix, SR, subtype="FLOAT")
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{B}/work/mix_pre.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True)
ln = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{B}/work/mix_pre.wav", "-af",
                f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={ln['input_i']}:measured_TP={ln['input_tp']}:measured_LRA={ln['input_lra']}:"
                f"measured_thresh={ln['input_thresh']}:offset={ln['target_offset']}:linear=true,aresample=48000", "-c:a", "pcm_s16le", f"{B}/work/mix.wav"], check=True)
bed = (M * db(BED) + sfx).mean(1); hp = signal.butter(2, 150, "high", fs=SR, output="sos")
vv = signal.sosfilt(hp, vo); bb = signal.sosfilt(hp, bed)
print("VO/bed dB:", " ".join(f"{lid}:{20*np.log10(np.sqrt(np.mean(vv[int((L['start'])*SR):int((L['end'])*SR)]**2))/np.sqrt(np.mean(bb[int(L['start']*SR):int(L['end']*SR)]**2)+1e-12)):.0f}" for lid, L in LN.items()))
