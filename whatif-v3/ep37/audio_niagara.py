"""Audio for episode 37 (Niagara barrel): river + falls roar, barrel knocks, cat meow, pump squeaks, crowd cheer, cannon."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_niagara as RN
from render_niagara import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def falls(d, g=1.0):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 900) * 0.6 + A.lp(rng.standard_normal(len(t)), 200)
    return x * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.6, 0, 1) * 0.18 * g


def river_amb(d, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 300, 2500) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * t))
    return x * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.6, 0, 1) * 0.08 * g


def knock(g=1.0):
    t = A.tt(0.25)
    return (np.sin(2 * np.pi * 180 * t) + 0.5 * np.sin(2 * np.pi * 330 * t)) * np.exp(-t / 0.04) * 0.5 * g


def meow(g=1.0):
    t = A.tt(0.6)
    f = 600 + 350 * np.sin(np.pi * t / 0.6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR) + 0.2 * np.sin(6 * np.pi * np.cumsum(f) / SR)
    return A.bp(x, 400, 4000) * np.sin(np.pi * t / 0.6) ** 1.5 * 0.25 * g


def squeak(g=1.0):
    t = A.tt(0.18)
    return np.sin(2 * np.pi * (1800 + 900 * t / 0.18) * t) * np.sin(np.pi * t / 0.18) * 0.12 * g


def cheer(d=2.0, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 500, 3500) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3 * t)))
    return x * np.minimum(1, t / 0.2) * np.clip((d - t) / 0.8, 0, 1) * 0.25 * g


T = {S['k']: S['t0'] for S in RN.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['barrel'], 'up', 'groove', 'pluck')
section(mus, T['barrel'], T['ride'], 'space', 'light', 'marimba')
section(mus, T['ride'], T['out'], 'minor', 'air', 'bell')
section(mus, T['out'], T['rich'], 'up', 'groove', 'marimba')
section(mus, T['rich'], DURATION, 'minor', 'light', 'pluck')

mixin(fx, falls(ph('sixty three') - 0.2), 0.0, 1.0)
for i in range(int((ph('sixty three') - 0.4) / 3.0) + 1):
    mixin(fx, A.whoosh(0.5, up=False), 0.35 * 3.0 + i * 3.0, 0.5)
mixin(fx, A.pop(900, 400), ph('inside a barrel'), 0.6)
mixin(fx, A.ding(1568), ph('on her birthday') + 0.2, 0.5)
mixin(fx, A.whoosh(0.45), T['annie'] - 0.1, 0.6)
mixin(fx, A.womp(), ph('almost broke') + 0.1, 0.5)
for p_ in ('survived', 'get famous', 'worry about money'):
    mixin(fx, A.pop(1000, 500), ph(p_) - 0.15, 0.6)
mixin(fx, A.boing(0.5, 250, 600), ph('forty three'), 0.5)
mixin(fx, A.ding(1318), ph('bold move') + 0.1, 0.5)
for p_ in ('oak wood', 'iron rings'): mixin(fx, knock(0.8), ph(p_))
for p_ in ('a mattress', 'leather harness'): mixin(fx, A.pop(800, 400), ph(p_), 0.6)
mixin(fx, A.thump(), ph('heavy anvil') + 0.3, 0.9)
mixin(fx, meow(1.0), ph('on her cat') + 0.3)
mixin(fx, falls(ph('came back alive') - ph('the cat went over') + 0.5), ph('the cat went over'), 1.0)
mixin(fx, A.fall_whistle(1.2), ph('the cat went over') + 0.2, 0.5)
mixin(fx, meow(1.0), ph('came back alive') + 0.4); mixin(fx, A.ding(2093), ph('came back alive') + 0.2, 0.5)
mixin(fx, river_amb(T['bottom'] - T['ride']), T['ride'])
for i in range(5): mixin(fx, squeak(), ph('bicycle pump') - 0.6 + i * 0.25)
mixin(fx, A.whoosh(0.5), ph('into the river') + 0.1, 0.5); mixin(fx, A.bubbles(1.5), ph('into the river') + 0.6, 0.5)
for i in range(4): mixin(fx, knock(0.5), T['float'] + 0.5 + i * 0.9)
mixin(fx, A.riser(1.2), ph('then she went over') - 0.4, 0.6)
mixin(fx, falls(ph("at the bottom you're") - ph('then she went over') + 1, 1.3), ph('then she went over'))
mixin(fx, A.fall_whistle(1.2), ph('then she went over') + 0.2, 0.6)
mixin(fx, A.boom(1.6, 80, 32), ph('then she went over') + 1.2, 0.9)
mixin(fx, A.pop(1100, 500), ph('seventeen story'), 0.5)
mixin(fx, A.boom(1.2, 90, 40), ph("at the bottom you're") + 0.4, 0.7)
mixin(fx, falls(T['out'] - ph('more than an olympic') + 0.3, 1.4), ph('more than an olympic') - 0.4)
mixin(fx, knock(0.9), T['out'] + 0.5); mixin(fx, knock(0.7), T['out'] + 0.8)
mixin(fx, cheer(2.5), ph('but alive'))
mixin(fx, A.shimmer(1.4), ph('the first person ever'), 0.6)
mixin(fx, A.boom(1.2, 90, 40), ph('walk up to a cannon') + 0.3, 0.7)
mixin(fx, A.womp(), ph('nope'), 0.6)
mixin(fx, A.whoosh(0.6), ph('manager ran off') + 0.2, 0.6)
for i in range(3): mixin(fx, A.click(), ph('posing for photos') + 0.2 + i * 1.25, 0.6)
mixin(fx, A.ding(784), ph('died broke'), 0.4)
mixin(fx, A.thump(), ph('illegal'), 0.8)
mixin(fx, meow(0.8), ph('after the cat') + 0.3)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RN.D, mus, fx, os.path.join(RN.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
