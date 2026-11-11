"""Audio for episode 42 (33 miners): rock rumble + collapse, drips, drill grind, tool clanks, capsule winch, crowd cheer."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_mine as RM
from render_mine import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def rumble(d, g=1.0):
    t = A.tt(d)
    return A.lp(rng.standard_normal(len(t)), 120) * np.minimum(1, t / 0.4) * np.clip((d - t) / 0.6, 0, 1) * 0.6 * g


def drip(g=1.0, f=1600):
    t = A.tt(0.25)
    x = np.sin(2 * np.pi * (f + 600 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.05)
    return A.verb(x * 0.35 * g, wet=0.5)


def grind(d, g=1.0):
    t = A.tt(d)
    x = np.sign(np.sin(2 * np.pi * 70 * t)) * 0.2 + A.bp(rng.standard_normal(len(t)), 400, 2500) * 0.4
    return A.lp(x, 2500) * np.minimum(1, t / 0.3) * np.clip((d - t) / 0.3, 0, 1) * 0.15 * g


def clank(g=1.0, f=900):
    t = A.tt(0.4)
    x = sum(np.sin(2 * np.pi * f * k * t) / k for k in (1, 2.7, 4.1)) * np.exp(-t / 0.08)
    return x * 0.3 * g


def winch(d, g=1.0):
    t = A.tt(d)
    x = np.sin(2 * np.pi * (180 + 20 * np.sin(2 * np.pi * 0.5 * t)) * t) * 0.3 + A.bp(rng.standard_normal(len(t)), 300, 1200) * 0.2
    return x * np.minimum(1, t / 0.5) * np.clip((d - t) / 0.5, 0, 1) * 0.1 * g


def cheer(d=2.5, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 500, 3500) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 3 * t)))
    return x * np.minimum(1, t / 0.2) * np.clip((d - t) / 0.8, 0, 1) * 0.25 * g


T = {S['k']: S['t0'] for S in RM.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['shelter'], 'minor', 'air', 'bell')
section(mus, T['shelter'], T['note'], 'minor', 'light', 'pluck')
section(mus, T['note'], T['capsule'], 'up', 'groove', 'marimba')
section(mus, T['capsule'], T['out'], 'space', 'light', 'bell')
section(mus, T['out'], DURATION, 'up', 'groove', 'pluck')

mixin(fx, A.whoosh(0.8, up=False), 0.2, 0.6)
mixin(fx, A.pop(900, 400), ph('thirty three miners'), 0.6)
mixin(fx, A.boom(1.4, 80, 32), ph('sixty nine days'), 0.6)
mixin(fx, A.pop(1100, 500), ph('august fifth'), 0.5)
mixin(fx, rumble(1.5, 0.6), ph('collapsed') - 0.9)
mixin(fx, A.boom(2.0, 60, 28), ph('collapsed'), 1.0); mixin(fx, rumble(2.5, 1.0), ph('collapsed') + 0.1)
mixin(fx, A.thump(), ph('sealed the only'), 0.9)
for k_, nxt in (('shelter', 'ration'), ('heat', 'drill'), ('doves', 'capsule'), ('ask', None)):
    t0 = T[k_]; t1 = T[nxt] if nxt else DURATION
    for i in range(int((t1 - t0) / 1.8)):
        mixin(fx, drip(0.6, 1400 + 500 * rng.random()), t0 + 0.4 + i * 1.8)
for p_ in ('two spoonfuls', 'sip of milk', 'a cracker'): mixin(fx, A.pop(1000, 500), ph(p_), 0.6)
mixin(fx, A.womp(), ph("that's it"), 0.5)
mixin(fx, A.pop(1200, 600), ph('eight kilos'), 0.5)
mixin(fx, grind(T['note'] - T['drill']), T['drill'], 1.0)
mixin(fx, A.boom(1.0, 100, 40), ph('broke through'), 0.6)
for i in range(6): mixin(fx, clank(0.8, 800 + 100 * (i % 3)), ph('banged on the drill') + 0.2 + i * 0.22)
mixin(fx, A.riser(1.0), ph('when the drill came back') - 0.4, 0.5)
mixin(fx, A.shimmer(1.6), ph('we are fine'), 0.7); mixin(fx, cheer(2.5, 1.0), ph('went crazy') - 0.3)
mixin(fx, A.womp(), ph('take months'), 0.5)
mixin(fx, winch(T['capsule'] - T['doves'], 0.8), T['doves'])
for p_ in ('food water', 'medicine', 'letters from home', 'tiny projector'): mixin(fx, A.pop(1100, 500), ph(p_), 0.5)
mixin(fx, A.ding(1568), ph('the doves'), 0.5)
mixin(fx, A.shimmer(1.4), ph('the phoenix'), 0.6)
mixin(fx, winch(T['shades'] - T['ride'], 1.2), T['ride'])
for i in range(5): mixin(fx, clank(0.5, 600), T['ride'] + 0.5 + i * 1.2)
mixin(fx, A.ding(2093), ph('sunglasses'), 0.5)
mixin(fx, cheer(3.0, 1.2), T['out'] + 0.2)
for i in range(8): mixin(fx, A.tick(2600, 0.6), T['out'] + 0.4 + i * 0.3, 0.5)
mixin(fx, A.ding(1318), ph('luis urzua'), 0.5)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RM.D, mus, fx, os.path.join(RM.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
