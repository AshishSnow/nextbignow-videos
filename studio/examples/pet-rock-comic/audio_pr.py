"""Audio for the Pet Rock episode: NO background music. Voice + light comic sound effects."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_pr as RH
from render_pr import ph, END, DURATION

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
mixin(fx, A.boom(1.0, 70, 30), ph('one and a half million'), 0.3)
mixin(fx, A.pop(800, 400), ph('four bucks'), 0.25)
for k_ in ('question', 'korea'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.4)
for k_ in ('dahl', 'product', 'catch', 'moves'): mixin(fx, swish(0.8), T[k_] + 0.2)
for p_ in ('ruined furniture', 'walks feeding', 'feeding'): mixin(fx, A.pop(700, 400), ph(p_), 0.2)
mixin(fx, A.pop(900, 450), ph('so dahl joked'), 0.25)
mixin(fx, A.ding(1568), ph('about a penny'), 0.15)
mixin(fx, A.pop(800, 400), ph('air holes'), 0.22)
mixin(fx, sub(0.6), ph('play dead'))
mixin(fx, A.pop(800, 400), ph('neiman marcus'), 0.22)
mixin(fx, A.ding(1760), ph('hundred thousand a day'), 0.15)
mixin(fx, A.pop(700, 400), ph('three ninety five'), 0.2)
mixin(fx, A.ding(1568), ph("that's genius"), 0.15)
mixin(fx, A.boom(1.0, 60, 30), ph('a millionaire'), 0.3)
mixin(fx, sub(0.8), ph('off a cliff'))
mixin(fx, A.pop(900, 450), ph('his verdict'), 0.25)
for p_ in ('name them', 'dress them', 'talk to them'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
for p_ in ('one sell the joke', 'two let the packaging', 'three launch before'): mixin(fx, A.pop(900, 450), ph(p_), 0.28)
mixin(fx, A.whoosh(0.5), T['end'] - 0.1, 0.4)
mixin(fx, A.pop(900, 450), ph('yes or no'), 0.3)
mixin(fx, sub(0.8), END + 0.9)

out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
