"""Audio for ep 46 (AI vs the power grid): low bed, electrical hum + zap on the fault, power-down on 'vanished', swishes on cards."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_grid as RG
from render_grid import ph, END, DURATION

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


def powerdown(d=1.4, g=1.0):
    t = A.tt(d); f = 120 * np.exp(-t / 0.5) + 30
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (d * 0.5)) * 0.35 * g


def zap(g=1.0):
    t = A.tt(0.5)
    return A.bp(rng.standard_normal(len(t)), 2000, 9000) * (np.sin(2 * np.pi * 50 * t) > 0) * np.exp(-t / 0.12) * 0.5 * g


def hum(d=3.0, g=1.0):
    t = A.tt(d)
    return (np.sin(2 * np.pi * 60 * t) + 0.4 * np.sin(2 * np.pi * 120 * t)) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.5) * 0.06 * g


T = {S['k']: S['t0'] for S in RG.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['alley'], 'space', 'air', 'bell')
section(mus, T['alley'], T['share'], 'minor', 'light', 'pluck')
section(mus, T['share'], T['predict'], 'space', 'light', 'bell')
section(mus, T['predict'], DURATION, 'minor', 'groove', 'pluck')

mixin(fx, hum(ph('vanished') - 0.5, 1.0), 0.3)
mixin(fx, powerdown(1.4, 1.0), ph('vanished')); mixin(fx, sub(1.0), ph('vanished'))
mixin(fx, A.boom(1.0, 70, 30), ph('all at the same'), 0.35)
mixin(fx, A.whoosh(0.5), ph('so what happens') - 0.15, 0.5)
for k_ in ('alley', 'scramble', 'map', 'race', 'ask'):
    mixin(fx, swish(1.0), T[k_] + 0.2)
for i in range(9): mixin(fx, A.pop(700 + 40 * i, 400), ph('biggest clusters') - 0.3 + i * 0.12, 0.18)
mixin(fx, A.whoosh(0.5), T['night'] - 0.1, 0.5)
mixin(fx, hum(2.0, 1.2), T['night'] + 0.2)
mixin(fx, zap(1.0), ph('one small part failed') + 0.4); mixin(fx, sub(0.9), ph('one small part failed') + 0.4)
mixin(fx, zap(0.6), ph('flickered'))
mixin(fx, powerdown(1.2, 0.8), ph('fifteen hundred megawatts')); mixin(fx, sub(0.9), ph('gone', after=ph('fifteen hundred')))
mixin(fx, A.ding(1568), ph('no blackout'), 0.25)
mixin(fx, A.riser(1.0), ph('twenty percent') - 0.8, 0.3); mixin(fx, sub(0.8), ph('twenty percent'))
mixin(fx, A.pop(800, 400), ph('same power lines'), 0.35)
for i in range(6): mixin(fx, A.tick(1800, 0.5), ph('twenty nine dollars') + i * 0.15, 0.35)
mixin(fx, sub(1.0), ph('two hundred seventy')); mixin(fx, A.boom(1.0, 70, 30), ph('two hundred seventy'), 0.35)
mixin(fx, A.pop(700, 400), ph('close to half'), 0.35)
mixin(fx, A.pop(900, 400), ph('five times'), 0.35)
mixin(fx, sub(0.9), ph('three mile island')); mixin(fx, A.boing(0.4, 300, 600), ph('yes that three'), 0.3)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.5); mixin(fx, sub(1.0), ph("doesn't collapse"))
mixin(fx, powerdown(1.2, 0.7), ph('more close calls') - 0.2)
for p_ in ('bills keep climbing', 'bring your own power', 'wait in line'): mixin(fx, A.ding(1568), ph(p_), 0.22)
mixin(fx, A.pop(900, 450), ph('comments'), 0.4)
mixin(fx, A.riser(1.2), END, 0.5); mixin(fx, sub(1.0), END + 0.9)

out = A.mixdown(RG.D, mus, fx, os.path.join(RG.D, 'vo48.wav'), music_lufs=-34.0)
print('mix ->', out)
