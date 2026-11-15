"""Audio for long-form (Social Security 2027 COLA): NO background music. Voice + a few light comic sound effects."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_cola as RH
from render_cola import ph, END, DURATION

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
mixin(fx, A.ding(1568), ph('three point six percent'), 0.15)
mixin(fx, A.boom(1.0, 70, 30), ph('smaller than that'), 0.25)
for p_ in ('exactly how much', 'when it hits', 'the one thing'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
for k_ in ('how', 'dollars', 'when', 'history', 'workers', 'todo'): mixin(fx, swish(0.8), T[k_] + 0.2)
for k_ in ('catch', 'fund', 'end'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.35)
mixin(fx, A.ding(1760), ph('prices were up'), 0.15)
mixin(fx, A.pop(800, 400), ph('about seventy five dollars'), 0.25)
mixin(fx, A.pop(900, 400), ph('nine hundred extra'), 0.22)
for p_ in ('january thirteenth', 'january twentieth', 'january twenty seventh'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
mixin(fx, sub(0.8), ph('sixty eight dollars'))
mixin(fx, A.ding(1568), ph('hold harmless'), 0.15)
mixin(fx, A.boom(1.0, 60, 30), ph('eight point seven'), 0.25)
mixin(fx, A.pop(800, 400), ph('one hundred ninety two thousand'), 0.2)
mixin(fx, sub(0.8), ph('eighty three percent'))
for p_ in ('first look for', 'second when you budget', 'and third'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
mixin(fx, A.pop(900, 450), ph('comments'), 0.3)
mixin(fx, sub(0.8), END + 0.9)

out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
