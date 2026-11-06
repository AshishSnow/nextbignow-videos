"""Audio for episode 41 (Hiroo Onoda): jungle ambience (insects, birds), plane drone, paper flutter, loudspeaker, page turns."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_onoda as RO
from render_onoda import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def jungle_amb(d, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 4000, 7000) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t) ** 2) * 0.25
    for k in range(int(d / 2.3)):
        t0 = k * 2.3 + rng.random()
        i0 = A.sec(t0); tb = A.tt(0.25)
        ch = np.sin(2 * np.pi * (2200 + 900 * np.sin(2 * np.pi * 12 * tb)) * tb) * np.sin(np.pi * tb / 0.25) * 0.3
        x[i0:i0 + len(ch)] += ch[:max(0, len(x) - i0)]
    return x * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.8, 0, 1) * 0.12 * g


def plane(d, g=1.0):
    t = A.tt(d)
    x = np.sin(2 * np.pi * 90 * t) + 0.5 * np.sin(2 * np.pi * 180 * t) + 0.3 * A.lp(rng.standard_normal(len(t)), 300)
    return x * np.sin(np.pi * t / d) * 0.12 * g


def flutter(d=1.5, g=1.0):
    t = A.tt(d)
    return A.bp(rng.standard_normal(len(t)), 1500, 6000) * (0.5 + 0.5 * np.sin(2 * np.pi * 18 * t)) * np.sin(np.pi * t / d) * 0.12 * g


T = {S['k']: S['t0'] for S in RO.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['harm'], 'minor', 'light', 'bell')
section(mus, T['harm'], T['suzuki'], 'minor', 'air', 'bell')
section(mus, T['suzuki'], T['orders'], 'up', 'groove', 'marimba')
section(mus, T['orders'], DURATION, 'space', 'light', 'pluck')

for k_, nxt in (('hook', 'harm'), ('found', 'cmdr'), ('orders', 'missed'), ('ask', None)):
    t0 = T[k_]; t1 = T[nxt] if nxt else DURATION
    mixin(fx, jungle_amb(t1 - t0), t0)
for i in range(12): mixin(fx, A.tick(2600, 0.6), 0.4 + i * 0.25, 0.4)
mixin(fx, A.pop(900, 400), ph('hiroo onoda'), 0.5)
mixin(fx, A.thump(), ph('never surrender'), 0.8)
mixin(fx, plane(3.0), ph('dropped leaflets') - 0.6, 1.0)
mixin(fx, flutter(2.0), ph('dropped leaflets') + 0.4, 1.0)
mixin(fx, A.womp(), ph('were fake'), 0.6)
for i in range(3): mixin(fx, A.pop(800 + i * 150, 400), T['family'] + 0.3 + i * 0.4, 0.5)
mixin(fx, A.chatter(1.2), ph('loudspeakers'), 0.3)
for i in range(10): mixin(fx, A.tick(2200, 0.5), T['stayed'] + 0.4 + i * 0.45, 0.4)
mixin(fx, A.womp(), ph('he was alone'), 0.5)
mixin(fx, A.whoosh(0.5), T['suzuki'] - 0.1, 0.6)
for p_ in ('lieutenant onoda', 'a panda', 'abominable snowman'): mixin(fx, A.pop(1000, 500), ph(p_), 0.6)
mixin(fx, A.ding(1568), ph('in just four days'), 0.5)
mixin(fx, A.boing(0.5, 400, 150), ph('refused to give up'), 0.6)
mixin(fx, A.whoosh(0.6), T['cmdr'] - 0.1, 0.6)
mixin(fx, flutter(0.6, 1.5), ph('bookshop'), 1.0)
mixin(fx, A.riser(1.0), ph('stop fighting') - 0.9, 0.5); mixin(fx, A.boom(1.2, 80, 34), ph('stop fighting'), 0.6)
mixin(fx, A.shimmer(1.4), ph('handed over'), 0.5)
for p_ in ('moon landing', 'color tv', 'the beatles'): mixin(fx, A.pop(1100, 500), ph(p_), 0.6)
mixin(fx, A.ding(1318), ph('nature school'), 0.5)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RO.D, mus, fx, os.path.join(RO.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
