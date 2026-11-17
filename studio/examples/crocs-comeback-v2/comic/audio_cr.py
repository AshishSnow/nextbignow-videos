"""Audio for the Crocs Short: NO background music. Voice + light comic SFX (same mix for both platform cuts)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_cr as RH
from render_cr import ph, END, DURATION

A.set_duration(DURATION)
N = A.N


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
mixin(fx, A.pop(900, 450), ph('one dollar'), 0.24)
mixin(fx, A.ding(1568), ph('whole business'), 0.14)
for k_ in ('crash', 'cut'): mixin(fx, swish(0.8), T[k_] + 0.15)
for k_ in ('tried', 'now', 'end'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.35)
mixin(fx, A.pop(800, 400), ph('seventy dollars'), 0.22)
mixin(fx, sub(0.7), ph('about one dollar'))
mixin(fx, A.boom(1.0, 60, 30), ph('eighty-five million'), 0.26)
for p_ in ('dress shoes', 'golf shoes', 'high heels'): mixin(fx, A.pop(850, 420), ph(p_), 0.22)
mixin(fx, A.boom(1.0, 55, 30), ph('become a joke'), 0.24)
for i in range(5): mixin(fx, A.pop(950 + 50 * i, 470), ph('decorate it') + i * 0.25, 0.16)
mixin(fx, A.ding(1760), ph('seventy-one million'), 0.14)
mixin(fx, A.boom(1.0, 60, 30), ph('three point three'), 0.28)
mixin(fx, A.pop(900, 450), ph('would you wear'), 0.24)
mixin(fx, sub(0.8), END + 0.6)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
