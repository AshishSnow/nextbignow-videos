"""SFX bed for the car-dealer neon Short (free sources only: Kenney CC0 + numpy-designed sounds), ducked under the voice, no music.
Writes mix.wav (stereo 48 kHz, -14 LUFS). Cue times come from the final word alignment via render_neon.ph()."""
import os, sys, random
import numpy as np, soundfile as sf
from scipy.signal import butter, lfilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_gas as R

HERE = os.path.dirname(os.path.abspath(__file__)); SR = 48000
X = os.path.join(HERE, 'sfx')


def load(n):
    y, sr = sf.read(os.path.join(X, n + '.wav'), dtype='float32'); return y if y.ndim == 1 else y.mean(1)


def env(n, a=0.005, r=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e


def lp(y, f): b, a = butter(2, f / (SR / 2)); return lfilter(b, a, y)


def whoosh(d=0.45):
    n = int(d * SR); y = np.random.randn(n); out = np.zeros(n); k = 512
    for i in range(0, n, k):
        u = i / n; f = 300 + 5000 * np.sin(np.pi * u) ** 2; out[i:i + k] = lp(y[i:i + k], f)
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 2 * 0.6


def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (70 * np.exp(-t * 3) + 30) * t) * np.exp(-t * 3.5)
    thump = lp(np.random.randn(n), 180) * np.exp(-t * 14) * 3
    crack = np.random.randn(n) * np.exp(-t * 40) * 0.5
    return (sub + thump + crack) * 0.8


def riser(d=1.0):
    n = int(d * SR); t = np.arange(n) / SR; u = t / d
    y = lp(np.random.randn(n), 400) * u ** 2 * 0.5 + np.sin(2 * np.pi * (200 + 600 * u ** 2) * t) * u ** 3 * 0.25
    return y


def neon_on():
    n = int(0.5 * SR); t = np.arange(n) / SR
    hum = (np.sign(np.sin(2 * np.pi * 120 * t)) * 0.15 + np.sin(2 * np.pi * 240 * t) * 0.2) * np.exp(-t * 3)
    flick = np.zeros(n)
    for s in (0.0, 0.06, 0.13):
        i = int(s * SR); flick[i:i + 900] += np.random.randn(900) * np.exp(-np.arange(900) / 200) * 0.6
    return hum + flick


def ching():
    n = int(1.4 * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for f, a in ((2093, 0.5), (2637, 0.35), (3136, 0.25), (4186, 0.15)):
        y += np.sin(2 * np.pi * f * t + 2 * np.sin(2 * np.pi * f * 1.41 * t) * np.exp(-t * 6)) * a * np.exp(-t * 3.5)
    y[:int(0.08 * SR)] += np.random.randn(int(0.08 * SR)) * 0.3 * np.exp(-np.arange(int(0.08 * SR)) / 800)
    return y * 0.6


def engine(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR; u = t / d
    f = 40 + 90 * u ** 0.6; ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sign(np.sin(ph)) * 0.4 + np.sin(ph * 2) * 0.3); y = lp(y + np.random.randn(n) * 0.1, 900)
    return y * np.minimum(1, t * 6) * (1 - u) ** 0.7 * 0.7


def drone(d):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 82.4 * t)) * 0.15 * env(n, 0.6, 0.6)


def mix(voice_path, out_path):
    v, sr = sf.read(voice_path, dtype='float32'); v = v if v.ndim == 1 else v.mean(1)
    N = int((R.DUR + 0.5) * SR); bed = np.zeros((N, 2)); nod = np.zeros((N, 2)); rnd = random.Random(3)

    def put(y, t, db, pan=0.0, duck=True, rate=1.0):
        if rate != 1.0: y = np.interp(np.arange(0, len(y), rate), np.arange(len(y)), y)
        i = int(t * SR); y = y[:max(0, N - i)] * 10 ** (db / 20)
        L, Rr = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
        tgt = bed if duck else nod; tgt[i:i + len(y), 0] += y * L; tgt[i:i + len(y), 1] += y * Rr
    ph = R.ph
    # scene changes: whoosh + pop on every cut (FNH-style punchy cuts)
    for t0, _ in R.SCENES[1:]: put(whoosh(0.35), t0 - 0.1, -17, rnd.uniform(-0.5, 0.5), rate=rnd.uniform(0.9, 1.1)); put(load('click2'), t0 + 0.02, -16)
    put(load('switch3'), 0.05, -15); put(neon_on(), 0.1, -17)
    put(load('cardPlace1'), ph('short answer') + 0.3, -14); put(load('cardSlide1'), ph('pays the station') - 0.2, -15)
    put(load('cardPlace3'), ph('it started back'), -14); put(load('switch7'), ph('nineteen thirties') - 0.1, -15); put(load('cardSlide3'), ph('gas taxes') - 0.2, -15)
    put(engine(1.4), ph('drivers on the') - 0.2, -16, -0.4); put(load('metalClick'), ph('first digits') - 0.2, -15)
    put(load('cardPlace1'), ph('two ninety nine') - 0.2, -14); put(load('cardPlace3'), ph('two ninety nine') + 0.6, -14)
    put(load('powerUp2'), ph('way cheaper') - 0.1, -17); put(impact(), ph('three dollars'), -12, duck=False)
    put(drone(1.2), ph('but that tiny') - 0.2, -19); put(load('switch3'), ph("isn't tiny") - 0.2, -14)
    put(load('cardSlide1'), ph('ten to fifteen') - 0.5, -15)
    for i in range(4): put(load('chipsStack1' if i % 2 else 'chipsStack3'), ph('ten to fifteen') - 0.1 + i * 0.12, -17, rnd.uniform(-0.5, 0.5), rate=rnd.uniform(0.9, 1.15))
    put(riser(0.7), ph('ten percent') - 0.75, -15); put(impact(), ph('ten percent'), -6, duck=False); put(ching(), ph('ten percent') + 0.05, -11, duck=False)
    put(load('cardPlace1'), ph('one station owner'), -14); put(load('switch7'), ph('dropped it') + 0.2, -14)
    put(impact(), ph('twenty three dollars'), -9, duck=False); put(load('handleCoins'), ph('twenty three dollars') + 0.1, -14)
    put(load('powerUp2'), ph('price trick') - 0.2, -15); put(impact(), ph('price trick'), -12, duck=False)
    put(load('click2'), ph('did you ever') - 0.1, -14); put(load('click2'), ph('comments') - 0.3, -15, 0.4)
    put(whoosh(0.6), R.END, -15)
    # duck the bed under the voice
    vv = np.zeros(N); vv[:min(N, len(v))] = v[:N]
    e = np.abs(vv); k = int(0.03 * SR); e = np.convolve(e, np.ones(k) / k, 'same')
    g = np.where(e > 0.02, 10 ** (-7 / 20), 1.0)
    out = np.zeros_like(g); a_att, a_rel = 1 / (0.03 * SR), 1 / (0.25 * SR); cur = 1.0
    for i in range(0, N, 64):
        tgt = g[i]; cur += (tgt - cur) * (min(1, 64 * a_att) if tgt < cur else min(1, 64 * a_rel)); out[i:i + 64] = cur
    m = bed * out[:, None] + nod + np.stack([vv, vv], 1)
    m = np.tanh(m * 0.9) / 0.9
    sf.write(out_path + '.tmp.wav', m.astype('float32'), SR)
    os.system(f"ffmpeg -nostdin -v error -y -i {out_path}.tmp.wav -af alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=11 -ar 48000 {out_path} && rm {out_path}.tmp.wav")


if __name__ == '__main__':
    mix(sys.argv[1], sys.argv[2])
