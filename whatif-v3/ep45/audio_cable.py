"""Audio for ep 45 (undersea cables): low, deep bed; underwater rumble on the eruption, snap + sub on cuts, swishes on cards."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_cable as RC
from render_cable import ph, END, DURATION

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


def rumble(d=2.5, g=1.0):
    t = A.tt(d)
    return A.lp(rng.standard_normal(len(t)), 180) * np.minimum(1, t / 0.15) * np.exp(-t / (d * 0.4)) * 1.4 * g


def snap(g=1.0):
    t = A.tt(0.25)
    return A.bp(rng.standard_normal(len(t)), 900, 6000) * np.exp(-t / 0.03) * 0.5 * g


T = {S['k']: S['t0'] for S in RC.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['catch'], 'space', 'air', 'bell')
section(mus, T['catch'], T['repair'], 'minor', 'light', 'pluck')
section(mus, T['repair'], T['predict'], 'space', 'light', 'bell')
section(mus, T['predict'], DURATION, 'minor', 'groove', 'pluck')

mixin(fx, rumble(2.8, 1.0), ph('blew up') - 0.1)
mixin(fx, snap(1.0), ph('fell off')); mixin(fx, sub(1.0), ph('fell off'))
mixin(fx, A.boom(1.0, 70, 30), ph('gone'), 0.4)
mixin(fx, A.whoosh(0.5), ph('so what happens') - 0.15, 0.5)
for k_ in ('catch', 'tonga', 'faults', 'sat', 'watch', 'ask'):
    mixin(fx, swish(1.0), T[k_] + 0.2)
mixin(fx, A.pop(900, 400), ph('ninety nine percent'), 0.4)
mixin(fx, A.ding(1568), ph('garden hose'), 0.25)
mixin(fx, snap(0.8), ph('ninety kilometers') + 0.4); mixin(fx, sub(0.7), ph('ninety kilometers') + 0.4)
for p_ in ('calls abroad', 'card payments', 'news from family'): mixin(fx, A.click(), ph(p_) + 0.3, 0.7)
mixin(fx, A.riser(1.0), ph('more than five weeks') - 0.8, 0.3)
mixin(fx, A.whoosh(0.5), T['redsea'] - 0.1, 0.5)
ta = ph('dragged its anchor')
for i in range(4): mixin(fx, snap(0.7), ta + 0.5 + i * 0.6); mixin(fx, sub(0.5), ta + 0.5 + i * 0.6)
for p_ in ('india', 'pakistan', 'uae'): mixin(fx, A.pop(800, 400), ph(p_), 0.3)
for i in range(10): mixin(fx, A.tick(1800, 0.5), ph('two hundred') + i * 0.2, 0.4)
mixin(fx, sub(0.8), ph("aren't spies"))
mixin(fx, A.whoosh(0.5), T['repair'] - 0.1, 0.5); mixin(fx, sub(0.9), ph('only about sixty'))
mixin(fx, A.pop(700, 400), ph('more than doubled'), 0.4)
for p_ in ('baltic sea', 'perth'): mixin(fx, swish(1.0), ph(p_) - 0.15)
mixin(fx, A.boing(0.4, 300, 600), ph('not really'), 0.35)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.5); mixin(fx, sub(1.0), ph("doesn't collapse"))
mixin(fx, snap(0.7), ph('go dark')); mixin(fx, sub(0.8), ph('go dark'))
for p_ in ('more repair ships', 'navies guarding', 'big tech companies'): mixin(fx, A.ding(1568), ph(p_), 0.22)
mixin(fx, A.pop(900, 450), ph('comments'), 0.4)
mixin(fx, A.riser(1.2), END, 0.5); mixin(fx, sub(1.0), END + 0.9)

out = A.mixdown(RC.D, mus, fx, os.path.join(RC.D, 'vo48.wav'), music_lufs=-34.0)
print('mix ->', out)
