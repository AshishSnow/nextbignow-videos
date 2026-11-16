"""Audio for L02 (measles long-form): NO music. Voice + light SFX."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_mlong as RH
from render_mlong import ph, END, DURATION
A.set_duration(DURATION)
N = A.N; SR = A.SR
def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out
def swish(g=1.0):
    t = A.tt(0.28)
    return A.bp(rng.standard_normal(len(t)), 1500, 7000) * np.sin(np.pi * t / 0.28) ** 2 * 0.12 * g
def sub(g=1.0):
    t = A.tt(0.9)
    return np.sin(2 * np.pi * (55 + 30 * np.exp(-t / 0.05)) * t) * np.exp(-t / 0.35) * 0.6 * g
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
for S in RH.SCENES[1:]: mixin(fx, swish(0.8), S['t0'] + 0.15)
mixin(fx, A.boom(1.0, 60, 30), ph('no longer eliminated'), 0.25)
for p_, g in (('three to four million', 0.2), ('forty eight thousand', 0.2), ('four to five hundred', 0.2), ('twelve to eighteen', 0.2), ('ninety two point four', 0.2),
              ('two thousand two hundred eighty nine', 0.2), ('five thousand four hundred twelve', 0.2), ('sixty thousand', 0.22)):
    mixin(fx, A.pop(800, 400), ph(p_), g)
mixin(fx, A.ding(1568), ph('measles was eliminated'), 0.13)
mixin(fx, sub(0.6), ph('two school age children died'))
mixin(fx, sub(0.6), ph('and ten deaths'))
mixin(fx, sub(0.9), ph('the us lost it too'))
mixin(fx, A.ding(1760), ph('broken by august'), 0.14)
mixin(fx, A.pop(900, 450), ph('tell me in the comments'), 0.3)
mixin(fx, sub(0.8), END + 0.9)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
