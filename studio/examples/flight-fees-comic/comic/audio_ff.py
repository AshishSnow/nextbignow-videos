"""Audio for the flight-fees Short: NO background music. Voice + light comic SFX (same mix for both platform cuts)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_ff as RH
from render_ff import ph, END, DURATION

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
mixin(fx, A.boom(1.0, 70, 30), ph('ninety-nine dollars more') - 0.05, 0.3)
mixin(fx, A.pop(800, 400), ph('for one bag'), 0.22)
for k_ in ('bag', 'seat', 'europe', 'money', 'move'): mixin(fx, swish(0.8), T[k_] + 0.15)
for k_ in ('senate', 'end'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.4)
mixin(fx, A.pop(800, 400), ph('twenty-nine dollars'), 0.22)
mixin(fx, A.pop(900, 450), ph('wait until the gate'), 0.24)
mixin(fx, sub(0.6), ph('ninety-nine to'))
mixin(fx, A.ding(1568), ph('ten dollars'), 0.15)
mixin(fx, A.pop(700, 400), ph('fifty dollars'), 0.2); mixin(fx, A.pop(900, 450), ph('forty-one'), 0.24)
mixin(fx, A.boom(1.0, 60, 30), ph('fifty-five pounds'), 0.26)
mixin(fx, A.pop(800, 400), ph('fifty-one euros'), 0.2); mixin(fx, A.pop(800, 400), ph('twenty-four euros'), 0.2)
mixin(fx, A.boom(1.0, 60, 30), ph('five billion'), 0.28); mixin(fx, A.ding(1760), ph('five billion') + 0.1, 0.13)
for p_ in ('add your bag', 'check in online', 'measure your bag'): mixin(fx, A.pop(900, 450), ph(p_, after=T['move']), 0.26)
mixin(fx, A.pop(900, 450), ph('worst fee'), 0.28)
mixin(fx, sub(0.8), END + 0.6)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
