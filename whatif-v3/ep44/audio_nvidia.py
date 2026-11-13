"""Audio for ep 44 (Nvidia, editorial look): restrained news-style bed, paper swishes on cards, glitch on 'stopped', soft bass hits."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_nvidia as RO
from render_nvidia import ph, END, DURATION

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


def glitch(d=0.6, g=1.0):
    t = A.tt(d); x = np.zeros(len(t))
    for k in range(8):
        i0 = A.sec(rng.random() * d * 0.9); n = A.sec(0.02 + 0.05 * rng.random())
        f = 200 + 1800 * rng.random()
        x[i0:i0 + n] += np.sign(np.sin(2 * np.pi * f * A.tt(n / SR)[:len(x[i0:i0 + n])])) * 0.25
    return A.lp(x, 6000) * g


def sub(g=1.0):
    t = A.tt(0.9)
    return np.sin(2 * np.pi * (55 + 30 * np.exp(-t / 0.05)) * t) * np.exp(-t / 0.35) * 0.6 * g


T = {S['k']: S['t0'] for S in RO.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['slow'], 'minor', 'light', 'pluck')
section(mus, T['slow'], T['history'], 'space', 'light', 'bell')
section(mus, T['history'], T['predict'], 'up', 'groove', 'marimba')
section(mus, T['predict'], DURATION, 'minor', 'groove', 'pluck')

for i in range(12): mixin(fx, A.tick(2400, 0.5), 0.3 + i * 0.1, 0.35)
mixin(fx, sub(1.0), ph('he was gone')); mixin(fx, A.click(), ph('he was gone') - 0.05, 0.6)
mixin(fx, A.whoosh(0.5), ph('so what happens now') - 0.15, 0.5); mixin(fx, sub(0.8), ph('so what happens now'))
for k_ in ('catch', 'week', 'stock', 'kress', 'history', 'test', 'ask'):
    mixin(fx, swish(1.0), T[k_] + 0.2)
for p_ in ('nineteen ninety three',): mixin(fx, A.pop(900, 400), ph(p_), 0.3)
mixin(fx, A.riser(0.8), ph('ninety percent') - 0.7, 0.3); mixin(fx, sub(0.8), ph('ninety percent'))
for p_ in ('he admitted', 'reports linked', "nvidia didn't give"): mixin(fx, swish(1.1), ph(p_) - 0.15)
mixin(fx, A.thump(), ph('effective immediately'), 0.6)
mixin(fx, glitch(0.6, 0.5), ph('fourteen percent') - 0.1); mixin(fx, A.boom(1.0, 70, 30), ph('fourteen percent'), 0.5)
mixin(fx, A.whoosh(0.5, up=True), ph('buyers jumped'), 0.4)
mixin(fx, A.riser(1.0), ph('revenue went') - 0.2, 0.3); mixin(fx, A.ding(1568), ph('two hundred billion'), 0.35)
mixin(fx, A.whoosh(0.5), T['slow'] - 0.1, 0.5); mixin(fx, sub(0.9), ph('not soon'))
for p_ in ('planned years', 'already designed', 'huge orders'): mixin(fx, swish(1.0), ph(p_) - 0.15)
mixin(fx, sub(0.6), ph('weird bets'))
for p_ in ('steve jobs', "uber's founder", 'bill gates'): mixin(fx, swish(1.0), ph(p_) - 0.15)
mixin(fx, A.ding(1318), ph('trillion dollars'), 0.3); mixin(fx, A.ding(1568), ph('first yearly profit'), 0.3); mixin(fx, A.womp(), ph('barely moved'), 0.4)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.5); mixin(fx, sub(1.0), ph("doesn't collapse"))
mixin(fx, A.shimmer(1.2), ph('king of ai'), 0.4); mixin(fx, A.womp(), ph('used to be'), 0.5)
mixin(fx, A.click(), ph('watch that'), 0.6)
mixin(fx, A.pop(900, 450), ph('yes or no'), 0.4)
mixin(fx, A.riser(1.2), END, 0.5); mixin(fx, sub(1.0), END + 0.9)

out = A.mixdown(RO.D, mus, fx, os.path.join(RO.D, 'vo48.wav'), music_lufs=-34.0)
print('mix ->', out)
