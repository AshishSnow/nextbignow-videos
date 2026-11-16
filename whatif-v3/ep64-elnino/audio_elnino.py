"""Audio for ep 64 (elnino): NO background music. Voice + a few light comic sound effects."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_elnino as RH
from render_elnino import ph, END, DURATION

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


T = {S['k']: S['t0'] for S in RH.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
mixin(fx, A.boom(1.0, 60, 30), 0.15, 0.3)
mixin(fx, A.whoosh(0.6), ph('so hot'), 0.3)
for k_ in ('what', 'y1997', 'storm', 'catch', 'peak', 'ask'): mixin(fx, swish(0.8), T[k_] + 0.1)
mixin(fx, A.pop(800, 400), ph('super el nino'), 0.22)
mixin(fx, A.ding(1568), ph('two degrees celsius'), 0.13)
mixin(fx, A.boom(1.0, 55, 28), ph('nineteen ninety seven'), 0.2)
for p_ in ('floods hit peru', 'fires burned across', 'hottest ever recorded'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
mixin(fx, A.pop(900, 450), ph('just one hurricane'), 0.22)
mixin(fx, sub(0.9), ph('rip storms apart'))
for p_ in ('american south', 'weaker rains to india', 'higher food prices'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
mixin(fx, A.boom(1.0, 55, 28), ph('forty nine million'), 0.22)
mixin(fx, A.ding(1318), ph('hottest year ever measured'), 0.13)
mixin(fx, A.pop(900, 450), ph('yes or no'), 0.3)
mixin(fx, sub(0.8), END + 0.9)

out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
