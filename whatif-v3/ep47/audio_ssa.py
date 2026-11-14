"""Audio for ep 47 (Social Security): low bed, paper snip on the cut, coin ticks, swishes on cards."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_ssa as RS
from render_ssa import ph, END, DURATION

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


def snip(g=1.0):
    out = np.zeros(A.sec(0.3))
    for k in range(2):
        t = A.tt(0.06); i = A.sec(0.11 * k)
        out[i:i + len(t)] += A.bp(rng.standard_normal(len(t)), 2500, 9000) * np.exp(-t / 0.012) * 0.5
    return out * g


T = {S['k']: S['t0'] for S in RS.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
section(mus, 0.0, T['how'], 'space', 'air', 'bell')
section(mus, T['how'], T['y1983'], 'minor', 'light', 'pluck')
section(mus, T['y1983'], T['predict'], 'space', 'light', 'bell')
section(mus, T['predict'], DURATION, 'minor', 'groove', 'pluck')

mixin(fx, snip(1.0), ph('pay cut') - 0.05); mixin(fx, sub(0.9), ph('pay cut'))
mixin(fx, A.pop(800, 400), ph('automatically'), 0.35)
mixin(fx, A.whoosh(0.5), ph('so what happens') - 0.15, 0.5); mixin(fx, sub(0.8), ph('runs dry'))
for k_ in ('how', 'report', 'why', 'options', 'ask'): mixin(fx, swish(1.0), T[k_] + 0.2)
mixin(fx, A.ding(1568), ph('trust fund'), 0.22)
mixin(fx, A.riser(0.8), ph("now it's shrinking") - 0.5, 0.3); mixin(fx, sub(0.8), ph('fast'))
mixin(fx, sub(0.9), ph('runs dry in late'))
mixin(fx, A.pop(700, 400), ph('one year sooner'), 0.35)
for i in range(10): mixin(fx, A.tick(1900, 0.5), ph('seventy eight cents') + i * 0.12, 0.3)
mixin(fx, A.boom(1.0, 70, 30), ph('eighteen thousand'), 0.35)
for p_ in ('in nineteen sixty', "today it's under", 'keeps falling'): mixin(fx, A.pop(700, 400), ph(p_), 0.3)
for p_ in ('fewer babies', 'living longer', 'giant wave'): mixin(fx, swish(0.9), ph(p_) - 0.1)
mixin(fx, A.whoosh(0.5), T['y1983'] - 0.1, 0.5); mixin(fx, sub(1.0), ph('nineteen eighty three'))
mixin(fx, A.boing(0.4, 300, 600), ph('panicked'), 0.3)
for p_ in ('retirement age', 'taxing some', 'payroll taxes sooner'): mixin(fx, A.click(), ph(p_), 0.6)
mixin(fx, A.ding(1568), ph('just in time'), 0.25)
mixin(fx, A.pop(800, 400), ph('about a third'), 0.35); mixin(fx, A.pop(700, 400), ph('about a quarter'), 0.35)
mixin(fx, A.riser(1.0), ph('fix gets bigger') - 0.8, 0.3)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.5); mixin(fx, sub(1.0), ph("doesn't disappear"))
for p_ in ('more money coming', 'smaller promises'): mixin(fx, A.ding(1568), ph(p_), 0.22)
mixin(fx, A.pop(900, 450), ph('comments'), 0.4)
mixin(fx, A.riser(1.2), END, 0.5); mixin(fx, sub(1.0), END + 0.9)

out = A.mixdown(RS.D, mus, fx, os.path.join(RS.D, 'vo48.wav'), music_lufs=-34.0)
print('mix ->', out)
