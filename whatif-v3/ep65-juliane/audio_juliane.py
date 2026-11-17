"""Audio for ep 65 (Juliane, cinematic): no music. Voice + cinematic SFX: thunder, wind of the fall, soft hits on cuts."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_juliane as RH
from render_juliane import ph, END, DURATION
A.set_duration(DURATION)
N = A.N; SR = A.SR
def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out
def thunder(d=3.0, g=1.0):
    t = A.tt(d); n = rng.standard_normal(len(t))
    crack = A.bp(n, 800, 6000) * np.exp(-t / 0.08) * 0.5
    roll = A.bp(n, 30, 300) * (np.exp(-t / 0.9) * (1 + 0.5 * np.sin(2 * np.pi * 1.7 * t))) * 1.2
    return (crack + roll) * g
def wind(d=4.0, g=1.0):
    t = A.tt(d); n = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / d) ** 0.6
    return A.bp(n, 200, 2500) * env * 0.35 * g
def hit(g=1.0):
    t = A.tt(1.2)
    return np.sin(2 * np.pi * (48 + 25 * np.exp(-t / 0.04)) * t) * np.exp(-t / 0.4) * 0.6 * g
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
mixin(fx, thunder(3.0, 0.6), 0.0)
for S in RH.SCENES[1:]: mixin(fx, hit(0.45), S['t0'])
mixin(fx, thunder(3.5, 1.0), ph('lightning hits'))
mixin(fx, hit(0.9), ph('breaks apart'))
mixin(fx, wind(4.5, 1.0), ph('she falls ten thousand') - 0.2)
mixin(fx, hit(0.7), ph('alone in the jungle'))
mixin(fx, A.ding(1318), ph('find water'), 0.08)
mixin(fx, hit(1.0), ph('only survivor'))
mixin(fx, hit(0.8), END + 0.4)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
