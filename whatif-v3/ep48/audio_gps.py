"""Audio for ep 48 (GPS): NO background music. Voice + a few light sound effects only."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_gps as RG
from render_gps import ph, END, DURATION

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


def static(d=0.8, g=1.0):
    t = A.tt(d)
    return A.bp(rng.standard_normal(len(t)), 1200, 6000) * (0.5 + 0.5 * (np.sin(2 * np.pi * 13 * t) > 0)) * np.exp(-t / (d * 0.6)) * 0.25 * g


T = {S['k']: S['t0'] for S in RG.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

mixin(fx, static(1.0, 1.0), ph('jamming their gps') - 0.1); mixin(fx, sub(0.8), ph('jamming their gps'))
mixin(fx, A.whoosh(0.5), ph('turn around') - 0.1, 0.4)
mixin(fx, A.whoosh(0.5), ph('so what happens') - 0.15, 0.4)
for k_ in ('what', 'tartu', 'cost', 'backup', 'ask'): mixin(fx, swish(0.8), T[k_] + 0.2)
for p_ in ('banks', 'cell towers', 'power grids'): mixin(fx, A.pop(800, 400), ph(p_), 0.25)
mixin(fx, static(0.6, 0.7), ph("simply couldn't come in")); mixin(fx, sub(0.7), ph("simply couldn't come in"))
mixin(fx, A.whoosh(0.5), T['worse'] - 0.1, 0.4)
mixin(fx, static(0.8, 0.6), ph('one day in july'))
mixin(fx, sub(0.8), ph('seven and a half billion'))
mixin(fx, A.ding(1568), ph('emergency services'), 0.2)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.4); mixin(fx, sub(0.8), ph("doesn't switch off"))
mixin(fx, A.pop(900, 450), ph('comments'), 0.3)
mixin(fx, sub(0.8), END + 0.9)

out = A.mixdown(RG.D, mus, fx, os.path.join(RG.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
