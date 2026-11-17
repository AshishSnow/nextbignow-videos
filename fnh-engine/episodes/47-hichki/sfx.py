"""Light comic SFX only (no music): pop/ding/whoosh/boom on key moments. VO + sfx -> work/mix.wav"""
import json, numpy as np, soundfile as sf, subprocess
from scipy import signal
SR = 48000; rng = np.random.default_rng(5)
TL = json.load(open('timing.json')); S = {l['id']: l['start'] for l in TL}
vo, _ = sf.read('work/vo.wav', dtype='float32'); TOTAL = TL[-1]['start'] + TL[-1]['dur'] + 3.2
N = int((TOTAL + .5) * SR); out = np.zeros(N, np.float32); out[:min(N, len(vo))] += vo[:N]
fx = np.zeros(N, np.float32)
def tt(d): return np.arange(int(d * SR)) / SR
def put(x, at, g):
    i = int(at * SR); n = min(len(x), N - i)
    if n > 0: fx[i:i + n] += x[:n] * g
def hp(x, f): return signal.sosfilt(signal.butter(2, f, 'hp', fs=SR, output='sos'), x)
def lp(x, f): return signal.sosfilt(signal.butter(2, f, 'lp', fs=SR, output='sos'), x)
def pop(): t = tt(.1); return np.sin(2 * np.pi * np.cumsum(900 - 5000 * t) / SR) * np.exp(-t * 35)
def ding(): t = tt(.7); return (np.sin(2 * np.pi * 1568 * t) + .4 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 6)
def whoosh(d=.35): t = tt(d); return lp(hp(rng.normal(0, 1, len(t)), 600), 5000) * np.sin(np.pi * t / d) ** 2 * .6
def boom(): t = tt(.6); return (np.sin(2 * np.pi * np.cumsum(90 - 60 * t) / SR) + .3 * lp(rng.normal(0, 1, len(t)), 300)) * np.exp(-t * 6)
def boing(): t = tt(.45); return np.sin(2 * np.pi * np.cumsum(240 + 150 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)) / SR) * np.exp(-t * 6)
for l in TL[1:]: put(whoosh(), l['start'] - .15, .22)
put(pop(), .3, .3); put(boing(), .4, .35); put(pop(), 1.5, .25)
put(boom(), S['h2'] + 3.1, .45)
put(whoosh(.6), S['s1'] + .2, .2); put(ding(), S['s1'] + 3.6, .3)
put(boing(), S['s2'] + .6, .3); put(boing(), S['s2'] + 3.0, .3); put(boom(), S['s2'] + 4.6, .35); put(boing(), S['s2'] + 6.6, .4)
for dt in (2.0, 3.4, 4.6, 6.3): put(pop(), S['s3'] + dt, .3)
put(boom(), S['s4'] + 3.8, .5); put(ding(), S['s4'] + 8.4, .35)
put(pop(), S['s5'] + .3, .3); put(pop(), S['s5'] + 1.2, .25)
for k in range(20): put(pop(), S['s5'] + 6.3 + k * .1, .1)
put(ding(), S['s5'] + 8.4, .4)
put(pop(), S['w1'] + .8, .25); put(pop(), S['w1'] + 2.6, .25)
put(boing(), S['e1'] + 3.4, .3)
B = TL[-1]['start'] + TL[-1]['dur'] + .2; put(ding(), B + .2, .35); put(pop(), B + .05, .4)
mix = out + fx * .5
st = np.stack([mix, mix], 1); sf.write('work/mix_pre.wav', st, SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/mix_pre.wav', '-af', 'loudnorm=I=-12:TP=-1.5:LRA=9', '-ar', '48000', 'work/mix.wav'], check=True)
print('ok', round(TOTAL, 2))
