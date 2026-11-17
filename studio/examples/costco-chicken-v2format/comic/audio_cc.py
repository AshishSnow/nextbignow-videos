"""Audio for the Costco chicken Short: NO background music. Voice + light comic SFX (same mix for both platform cuts)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_cc as RH
from render_cc import ph, END, DURATION

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
mixin(fx, A.boom(1.0, 70, 30), ph('millions of dollars') - 0.05, 0.28)
mixin(fx, A.pop(900, 450), ph('on purpose'), 0.26)
for k_ in ('price', 'bet', 'result'): mixin(fx, swish(0.8), T[k_] + 0.15)
for k_ in ('cfo', 'plant', 'end'): mixin(fx, A.whoosh(0.5), T[k_] - 0.1, 0.35)
mixin(fx, A.ding(1568), ph('four ninety-nine'), 0.14)
mixin(fx, A.pop(700, 400), ph('five ninety-nine'), 0.2)
mixin(fx, A.boom(1.0, 60, 30), ph('thirty to forty'), 0.24)
mixin(fx, A.pop(800, 400), ph('cheap chicken'), 0.22)
for i in range(5): mixin(fx, A.pop(900 + 60 * i, 450), ph('full cart') - 1.0 + i * 0.22, 0.16)
mixin(fx, sub(0.7), ph('four hundred fifty'))
for p_ in ('a hatchery', 'a feed mill', 'a processing plant'): mixin(fx, A.pop(850, 420), ph(p_), 0.22)
mixin(fx, A.boom(1.0, 60, 30), ph('fifty-seven million'), 0.3); mixin(fx, A.ding(1760), ph('fifty-seven million') + 0.1, 0.14)
mixin(fx, A.pop(900, 450), ph('still four'), 0.28)
mixin(fx, A.pop(900, 450), ph('lose millions'), 0.24); mixin(fx, A.pop(900, 450), ph('the whole cart'), 0.24)
mixin(fx, sub(0.8), END + 0.6)
out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
