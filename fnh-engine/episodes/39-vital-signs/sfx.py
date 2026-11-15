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
for l in TL[1:]:
    put(whoosh(), l['start'] - .15, .2)
    if l['id'].endswith('0') and l['id'][0] in 'pbcot': put(boom(), l['start'] + .05, .45); put(ding(), l['start'] + .3, .25)
put(pop(), .05, .3)
for a in (.2, .96, 1.78, 2.74, 3.48): put(pop(), S['i3'] + a, .3)
put(pop(), S['p2'] + 5.6, .35); put(ding(), S['p4'] + 4.6, .3); put(ding(), S['p5'] + .4, .3)
for a in (.2, 1.0, 2.2): put(pop(), S['p6'] + a, .3)
put(ding(), S['b1'] + 3.0, .3); put(pop(), S['b2'] + 7.0, .3)
put(pop(), S['c2'] + 1.8, .3); put(pop(), S['c2'] + 5.3, .3); put(ding(), S['c3'] + .2, .3); put(boom(), S['c3'] + 3.5, .4); put(pop(), S['c4'] + 3.2, .3)
for a in (1.7, 5.8, 7.2, 10.8, 12.8, 15.5, 18.3, 20.4): put(pop(), S['c6'] + a, .25)
put(ding(), S['o2'] + .4, .3)
for a in (1.2, 2.3, 3.5, 4.7): put(pop(), S['o3'] + a, .3)
put(pop(), S['o5'] + .2, .3); put(boom(), S['o5'] + 3.4, .45)
put(ding(), S['t1'] + .8, .3); put(ding(), S['t4'] + 4.9, .35); put(boom(), S['t5'] + .2, .35); put(pop(), S['t5'] + 3.6, .3)
for a in (2.5, 4.5, 6.8, 10.0, 12.3): put(pop(), S['r1'] + a, .3)
B = TL[-1]['start'] + TL[-1]['dur'] + .2; put(ding(), B + .2, .35); put(pop(), B + .05, .4)
mix = out + fx * .5
st = np.stack([mix, mix], 1); sf.write('work/mix_pre.wav', st, SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'work/mix_pre.wav', '-af', 'loudnorm=I=-12:TP=-1.5:LRA=9', '-ar', '48000', 'work/mix.wav'], check=True)
print('ok', round(TOTAL, 2))
