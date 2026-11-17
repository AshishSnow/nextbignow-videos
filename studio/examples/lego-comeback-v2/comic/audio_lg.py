"""Audio for the Lego Short: NO background music. Voice + light comic SFX (same mix for both platform cuts)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_lg as RH
from render_lg import ph, END, DURATION

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
mixin(fx, A.boom(1.0, 70, 30), ph('three hundred million'), 0.26)
mixin(fx, sub(0.7), ph('almost went broke'))
mixin(fx, A.ding(1568), ph('two and a half billion'), 0.15)
for k_ in ('focus', 'cut'): mixin(fx, swish(0.8), T[k_] + 0.15)
for k_ in ('loss', 'back', 'end'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.35)
for p_ in ('theme parks', 'video games', 'even clothes'): mixin(fx, A.pop(850, 420), ph(p_), 0.22)
mixin(fx, A.boom(1.0, 60, 30), ph('twenty-five percent'), 0.24)
mixin(fx, A.boom(1.0, 55, 30), ph('biggest loss'), 0.28)
mixin(fx, swish(1.0), ph('cut its costs'))
mixin(fx, A.pop(800, 400), ph('a fifth'), 0.22); mixin(fx, A.boom(1.0, 60, 30), ph('legoland parks'), 0.22)
mixin(fx, A.ding(1760), ph('the brick', after=T['cut']), 0.15)
mixin(fx, A.pop(900, 450), ph('profitable again'), 0.26)
mixin(fx, A.pop(900, 450), ph('sixteen percent'), 0.22); mixin(fx, A.ding(1568), ph('twelve billion'), 0.14)
mixin(fx, A.pop(900, 450), ph('what would you cut'), 0.24)
mixin(fx, sub(0.8), END + 0.6)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
