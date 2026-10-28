"""Audio for the Mars what-if: clean VO on top, playful bright score, cartoon SFX on each moment."""
import os, sys, json, subprocess
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy import signal
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SR = 48000
N = 1
def set_duration(d):
    global N
    N = int(round(d * SR))
rng = np.random.default_rng(11)
def sec(t): return int(round(t * SR))
def db(x): return 10 ** (x / 20)
def lp(x, fc, o=2): return signal.sosfilt(signal.butter(o, fc, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, fc, o=2): return signal.sosfilt(signal.butter(o, fc, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b, o=2): return signal.sosfilt(signal.butter(o, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def tt(d): return np.arange(sec(d)) / SR

def place(buf, snd, t, g=1.0, pan=0.0):
    i = sec(t)
    if snd.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4) * 1.414; r = np.sin((pan + 1) * np.pi / 4) * 1.414
        snd = np.stack([snd * l, snd * r], 1)
    if i < 0: snd = snd[-i:]; i = 0
    n = min(len(snd), N - i)
    if n > 0: buf[i:i + n] += snd[:n] * g

def mk_ir(d=1.6, tau=0.35, seed=3):
    r = np.random.default_rng(seed); n = sec(d); e = np.exp(-np.arange(n) / SR / tau)
    ir = np.stack([r.standard_normal(n) * e, r.standard_normal(n) * e], 1); ir = lp(ir, 6000)
    return ir / np.sqrt(np.sum(ir ** 2))
IR = mk_ir(); IRS = mk_ir(0.6, 0.12, 5)
def verb(x, wet=0.25, ir=IR):
    if x.ndim == 1: x = np.stack([x, x], 1)
    y = np.stack([signal.fftconvolve(x[:, k], ir[:, k])[:len(x)] for k in range(2)], 1)
    return x * (1 - wet) + y * wet * 2.0

NOTE = lambda m: 440.0 * 2 ** ((m - 69) / 12)

# ---------------------------------------------------------------- instruments
def kick(g=1.0):
    t = tt(0.45); f = 50 + 120 * np.exp(-t / 0.03)
    return (np.tanh(1.6 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)) + hp(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.002) * 0.3) * g
def clap(g=1.0):
    t = tt(0.4); nz = bp(rng.standard_normal(len(t)), 1000, 5000); e = np.zeros(len(t))
    for k, d in enumerate([0, 0.01, 0.02]):
        e += (t >= d) * np.exp(-np.clip(t - d, 0, None) / (0.006 if k < 2 else 0.1))
    return verb(nz * e * 0.7 * g, 0.15, IRS)
def hat(g=1.0):
    t = tt(0.07); return hp(rng.standard_normal(len(t)), 8000) * np.exp(-t / 0.02) * 0.28 * g
def snare(g=1.0):
    t = tt(0.25); return (np.sin(2 * np.pi * 200 * t) * np.exp(-t / 0.05) * 0.5 + bp(rng.standard_normal(len(t)), 1500, 9000) * np.exp(-t / 0.08) * 0.6) * g
def bass(f, d, g=1.0):
    t = tt(d); x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    return np.tanh(1.3 * x) * np.minimum(1, t / 0.005) * np.clip((d - t) / 0.04, 0, 1) * np.exp(-t / max(0.3, d)) * 0.7 * g
def pluck(f, d=0.4, g=1.0, bright=1.0):
    t = tt(d); x = np.zeros(len(t))
    for k in range(1, 9):
        if f * k > 14000: break
        x += np.sin(2 * np.pi * f * k * t) / k ** 1.15 * np.exp(-t * (4 + 3.5 * k / bright))
    return x * np.minimum(1, t / 0.002) * np.clip((d - t) / 0.03, 0, 1) * 0.45 * g
def marimba(f, d=0.5, g=1.0):
    t = tt(d)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.22) + 0.3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t / 0.04)
    return x * np.minimum(1, t / 0.002) * 0.5 * g
def bell(f, d=1.4, g=1.0):
    t = tt(d)
    x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / dd) for r, a, dd in [(1, 1, 0.9), (2.0, 0.35, 0.5), (3.01, 0.2, 0.25)])
    return x * np.minimum(1, t / 0.002) * 0.28 * g
def pad(fs, d, g=1.0, fc=1600, att=0.3):
    t = tt(d); x = np.zeros(len(t))
    for f in fs:
        for det in (-0.004, 0, 0.004):
            ph = (np.arange(len(t)) * f * (1 + det) / SR + rng.random()) % 1.0
            x += 2 * ph - 1
    x = lp(lp(x, fc), fc)
    return x * np.minimum(1, t / att) * np.clip((d - t) / 0.35, 0, 1) * 0.05 * g

CH = {'C': (36, [60, 64, 67]), 'G': (31, [55, 59, 62]), 'Am': (33, [57, 60, 64]), 'F': (29, [53, 57, 60]),
      'Dm': (38, [62, 65, 69]), 'E': (28, [52, 56, 59]), 'Em': (28, [55, 59, 64])}
PROG = {'up': ['C', 'G', 'Am', 'F'], 'minor': ['Am', 'F', 'C', 'G'], 'sad': ['Am', 'Dm', 'F', 'E'], 'space': ['F', 'C', 'G', 'Am']}
BPM = 112; BEAT = 60 / BPM; BAR = BEAT * 4
ARP = [0, 1, 2, 1, 3, 2, 1, 2]

def section(m, t0, t1, prog, kind='groove', inst='pluck'):
    b = 0
    while t0 + b * BAR < t1 - 0.05:
        tb = t0 + b * BAR; name = PROG[prog][b % 4]; root, tones = CH[name]
        be = min(t1, tb + BAR)
        place(m, pad([NOTE(x) for x in tones], be - tb + 0.05, 1.0 if kind != 'air' else 1.4), tb)
        for s in range(16):
            ts = tb + s * BAR / 16
            if ts >= t1 - 0.02: break
            if kind == 'groove':
                if s in (0, 8) or (s == 10 and b % 2): place(m, kick(), ts)
                if s in (4, 12): place(m, clap(0.8), ts)
                if s % 2 == 0: place(m, hat(0.9 if s % 4 == 2 else 0.5), ts, pan=0.3)
                if s in (0, 6, 8, 14): place(m, bass(NOTE(root + 12), BAR / 16 * (3 if s in (0, 8) else 2)), ts)
            elif kind == 'light':
                if s in (0, 8): place(m, kick(0.6), ts)
                if s % 4 == 2: place(m, hat(0.5), ts, pan=0.3)
                if s == 0: place(m, bass(NOTE(root + 12), BAR * 0.9, 0.8), ts)
            elif kind == 'air':
                if s == 0: place(m, bass(NOTE(root + 12), BAR, 0.6), ts)
            if s % 2 == 0 and kind != 'air':
                a = ARP[(s // 2) % 8]
                mm = tones[a % 3] + (12 if a == 3 else 0) + 12
                snd = marimba(NOTE(mm), 0.45, 0.6) if inst == 'marimba' else pluck(NOTE(mm), 0.38, 0.55, 1.2)
                place(m, snd, ts, pan=0.35 * np.sin(s))
            if inst == 'bell' and s in (0, 6, 12):
                place(m, bell(NOTE(tones[(s // 6) % 3] + 24), 1.2, 0.55), ts, pan=-0.4)
        b += 1

# ---------------------------------------------------------------- SFX
def whoosh(d=0.45, up=True):
    t = tt(d); nz = rng.standard_normal(len(t)); out = np.zeros(len(t)); seg = 512
    for k in range(0, len(t), seg):
        p = k / len(t); fc = (300 + 4500 * p ** 1.6) if up else (4800 - 4400 * p ** 0.7)
        b_ = bp(nz[max(0, k - 2048):k + seg], max(80, fc * 0.6), min(20000, fc * 1.5))[-min(seg, len(t) - k):]
        out[k:k + len(b_)] = b_
    return verb(out * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.5 * 0.8, 0.25)
def pop(f0=900, f1=420, g=1.0):
    t = tt(0.15); f = f1 + (f0 - f1) * np.exp(-t / 0.025)
    return verb(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.045) * g, 0.2, IRS)
def boom(d=1.8, f0=95, f1=32, g=1.0):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / 0.18)
    x = np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.7)) * 0.8 + lp(rng.standard_normal(len(t)), 1800) * np.exp(-t / 0.05) * 0.3
    return verb(x * g, 0.2)
def thump(g=1.0):
    t = tt(0.4); x = np.sin(2 * np.pi * (60 + 90 * np.exp(-t / 0.02)) * t) * np.exp(-t / 0.12)
    return np.tanh(2 * x) * 0.8 * g
def ding(f=1568, g=1.0):
    t = tt(1.5); x = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d) for r, a, d in [(1, 1, 0.9), (2.0, 0.4, 0.5), (2.76, 0.25, 0.3)])
    return verb(x * np.minimum(1, t / 0.002) * 0.35 * g, 0.35)
def tick(f=2800, g=1.0):
    t = tt(0.04); return (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.004) + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.002) * 0.4) * g
def riser(d=1.5):
    t = tt(d); p = t / d; f = 220 * (1 + 5 * p ** 2)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3 + bp(rng.standard_normal(len(t)), 800, 6000) * 0.3
    return verb(x * p ** 2, 0.3)
def roar(d=2.6):
    t = tt(d); nz = rng.standard_normal(len(t))
    x = lp(nz, 900) * 1.0 + bp(nz, 900, 4000) * 0.25
    rum = np.sin(2 * np.pi * 38 * t + 3 * np.sin(2 * np.pi * 3 * t)) * 0.6
    e = np.minimum(1, t / 0.15) * np.clip((d - t) / 1.2, 0, 1)
    return verb(np.tanh((x + rum) * 1.4) * e * 0.6, 0.25)
def bubbles(d=3.0, g=1.0):
    out = np.zeros(sec(d))
    for i in range(int(d * 22)):
        t0 = rng.uniform(0, d - 0.08); L = sec(0.05); t = np.arange(L) / SR
        f = rng.uniform(400, 1300) * (1 + 2.5 * t / 0.05)
        b_ = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.05) * rng.uniform(0.3, 1)
        out[sec(t0):sec(t0) + L] += b_
    return verb(out * 0.25 * g, 0.2, IRS)
def wind(d=4.0, g=1.0):
    t = tt(d); nz = rng.standard_normal(len(t)); out = np.zeros(len(t)); seg = 2048
    for k in range(0, len(t), seg):
        fc = 700 + 300 * np.sin(2 * np.pi * 0.3 * k / SR) + 150 * np.sin(2 * np.pi * 0.7 * k / SR)
        b_ = bp(nz[max(0, k - 4096):k + seg], fc * 0.6, fc * 1.6)[-min(seg, len(t) - k):]
        out[k:k + len(b_)] = b_
    return out * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.6, 0, 1) * 0.35 * g
def boing(d=0.7, f0=180, f1=520, g=1.0):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** 0.6
    f = f * (1 + 0.08 * np.sin(2 * np.pi * 14 * t))
    return verb(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d * 0.6)) * 0.45 * g, 0.15, IRS)
def womp():
    out = np.zeros(sec(2.0))
    for i, (f0, f1, d) in enumerate([(233.08, 220.0, 0.3), (220.0, 207.65, 0.3), (207.65, 196.0, 0.3), (196.0, 165.0, 0.9)]):
        t = tt(d); f = f0 + (f1 - f0) * t / d
        ph = 2 * np.pi * np.cumsum(f) / SR; x = sum(np.sin(k * ph) / k for k in range(1, 9))
        x = lp(x, 1500) * np.minimum(1, t / 0.03) * np.clip((d - t) / 0.08, 0, 1)
        out[sec(0.3 * i):sec(0.3 * i) + len(t)] += x * 0.4
    return verb(out, 0.25)
def zap(g=1.0):
    t = tt(0.18); f = 2400 * np.exp(-t / 0.05) + 300
    return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t / 0.05) * 0.18 * g
def chirp(g=1.0):
    out = np.zeros(sec(0.5))
    for k in range(3):
        L = sec(0.06); t = np.arange(L) / SR
        f = 3200 + 1600 * np.sin(np.pi * t / t[-1])
        out[sec(k * 0.1):sec(k * 0.1) + L] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / t[-1])
    return verb(out * 0.25 * g, 0.3)
def click(g=1.0):
    t = tt(0.08); return (hp(rng.standard_normal(len(t)), 2000) * np.exp(-t / 0.004) + np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.01)) * 0.6 * g
def buzz(g=1.0):
    t = tt(0.35); x = np.sign(np.sin(2 * np.pi * 140 * t)) * 0.3 + np.sign(np.sin(2 * np.pi * 147 * t)) * 0.3
    return lp(x, 2500) * np.clip((0.35 - t) / 0.05, 0, 1) * 0.5 * g
def shimmer(d=1.2, g=1.0):
    t = tt(d); x = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) for f in [1174.7, 1396.9, 1760, 2349.3])
    return verb(x * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.sin(np.pi * t / d) ** 2 * 0.12 * g, 0.5)
def chatter(d=3.0):
    out = np.zeros(sec(d)); x = 0.0
    while x < d - 0.05:
        out[sec(x):sec(x) + sec(0.03)] += tick(1800 + rng.uniform(-200, 200), 0.6)[:sec(0.03)]
        x += 0.07 + rng.uniform(0, 0.02)
    return out * 0.5
def fall_whistle(d=1.2):
    t = tt(d); f = 1800 * (1 - 0.6 * t / d)
    return verb(np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.2 * np.minimum(1, t / 0.05) * np.clip((d - t) / 0.2, 0, 1), 0.3)

def duck_curve(vo, depth=0.65):
    e = np.abs(vo); rel = np.exp(-1 / (SR * 0.3))
    env = signal.lfilter([1 - rel], [1, -rel], e)
    env = env / (np.percentile(env[env > 1e-4], 90) + 1e-9)
    g = 1 - depth * np.clip(env, 0, 1)
    a = np.exp(-1 / (SR * 0.05))
    return signal.lfilter([1 - a], [1, -a], g)

def mixdown(D, mus, fx, vo_path, music_lufs=-23.5):
    meter = pyln.Meter(SR)
    v, sr = sf.read(vo_path, dtype='float64'); assert sr == SR, sr
    if v.ndim > 1: v = v.mean(1)
    vo = np.zeros(N); vo[:min(N, len(v))] = v[:N]
    vo = vo * db(-16 - meter.integrated_loudness(vo))
    mus = mus - bp(mus, 900, 4200) * 0.45
    mus = mus * db(music_lufs - meter.integrated_loudness(mus))
    duck = duck_curve(vo)
    fx = fx / (np.max(np.abs(fx)) + 1e-9) * db(-5)
    full = np.stack([vo, vo], 1) + mus * duck[:, None] + fx * (0.5 + 0.5 * duck[:, None])
    raw = os.path.join(D, 'mix_raw.wav'); out = os.path.join(D, 'mix.wav')
    sf.write(raw, full.astype(np.float32), SR, subtype='FLOAT')
    r = subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', raw, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}') + 1])
    af = ('loudnorm=I=-14:TP=-1.0:LRA=11:linear=true:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s,'
          'alimiter=limit=0.89:attack=3:release=60:level=false,aresample=48000') % (js['input_i'], js['input_tp'], js['input_lra'], js['input_thresh'], js['target_offset'])
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', raw, '-af', af, '-ar', '48000', '-c:a', 'pcm_s24le', out], check=True)
    assert sf.info(out).samplerate == SR
    return out
