"""Audio for episode 38 (trapped in an air bubble): storm wave, hull creaks, underwater drone, drips, diver bubbles, heartbeat."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_bubble as RB
from render_bubble import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def under(d, g=1.0):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 180) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.15 * t)) + 0.3 * np.sin(2 * np.pi * 50 * t)
    return x * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.8, 0, 1) * 0.2 * g


def creak(g=1.0):
    t = A.tt(0.9)
    f = 70 + 25 * np.sin(2 * np.pi * 4 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.2
    return A.lp(x, 600) * np.exp(-t / 0.4) * g


def drip(g=1.0, f=1600):
    t = A.tt(0.25)
    x = np.sin(2 * np.pi * (f + 600 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.05)
    return A.verb(x * 0.35 * g, wet=0.5)


def heartbeat(g=1.0):
    t = A.tt(0.6)
    b = lambda t0: np.sin(2 * np.pi * 55 * (t - t0)) * np.exp(-np.maximum(0, t - t0) / 0.06) * (t >= t0)
    return (b(0.0) + 0.7 * b(0.22)) * 0.5 * g


def splashes(d, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 400, 3000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 0.7 * t)) ** 4)
    return x * np.minimum(1, t / 0.3) * np.clip((d - t) / 0.4, 0, 1) * 0.12 * g


T = {S['k']: S['t0'] for S in RB.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['pocket'], 'minor', 'air', 'bell')
section(mus, T['pocket'], T['co2'], 'space', 'light', 'marimba')
section(mus, T['co2'], T['divers'], 'minor', 'light', 'pluck')
section(mus, T['divers'], T['chamber'], 'minor', 'air', 'bell')
section(mus, T['chamber'], DURATION, 'up', 'groove', 'pluck')

mixin(fx, A.wind(T['sink'], 0.5), 0.0)
mixin(fx, A.whoosh(0.6, up=False), ph('flipped over'), 0.6); mixin(fx, creak(), ph('flipped over') + 0.3)
mixin(fx, A.bubbles(2.0), ph('and sank'), 0.6)
mixin(fx, A.womp(), ph('no way out'), 0.5)
mixin(fx, A.pop(900, 400), ph('harrison okene'), 0.5)
mixin(fx, A.pop(1100, 500), ph('four thirty'), 0.5)
mixin(fx, A.riser(1.0), ph('a huge wave') - 0.8, 0.6); mixin(fx, A.roar(2.0), ph('a huge wave'), 0.6)
mixin(fx, A.boom(1.6, 80, 32), ph('a huge wave') + 0.6, 0.9); mixin(fx, creak(1.0), ph('a huge wave') + 1.0)
mixin(fx, A.thump(), ph('in the bathroom'), 0.6)
mixin(fx, under(T['divers'] - T['sink']), T['sink'])
mixin(fx, A.bubbles(3.0), T['sink'] + 0.2, 0.7)
mixin(fx, A.boom(1.4, 70, 30), ph('on the seafloor'), 0.8); mixin(fx, creak(0.9), ph('on the seafloor') + 0.4)
mixin(fx, splashes(ph('a pocket of air') - T['pocket']), T['pocket'])
mixin(fx, A.shimmer(1.4), ph('a pocket of air'), 0.6)
for i in range(int((T['co2'] - T['wait']) / 1.8)):
    mixin(fx, drip(0.7, 1400 + 500 * rng.random()), T['wait'] + 0.5 + i * 1.8)
for i in range(4): mixin(fx, heartbeat(0.9), ph('carbon dioxide') + 0.2 + i * 0.85)
mixin(fx, A.womp(), ph('can kill you'), 0.6)
mixin(fx, A.ding(1568), ph('got lucky'), 0.5)
mixin(fx, A.thump(), ph('water pressure'), 0.6); mixin(fx, A.pop(1200, 600), ph('more oxygen'), 0.5)
mixin(fx, splashes(1.6, 1.5), ph('splashing water'))
mixin(fx, A.wind(2.0, 0.4), T['cold'] + 0.1)
mixin(fx, A.pop(700, 300), ph('pulled a mattress') + 0.3, 0.6)
for p_ in ('bottle of', 'life jacket', 'tiny flashlights'): mixin(fx, A.pop(1000, 500), ph(p_), 0.6)
mixin(fx, A.click(), ph('total darkness'), 0.8)
for i in range(3): mixin(fx, heartbeat(0.7), ph('total darkness') + 0.6 + i * 0.9)
mixin(fx, A.bubbles(3.0), T['divers'] + 0.3, 0.8)
mixin(fx, A.womp(), ph('recover bodies'), 0.5)
for i in range(4): mixin(fx, A.bubbles(0.8), T['hand'] + 0.3 + i * 1.0, 0.4)
mixin(fx, A.riser(1.0), ph('a hand grabbed') - 0.9, 0.6)
mixin(fx, A.boom(1.2, 90, 40), ph('a hand grabbed'), 0.8); mixin(fx, A.pop(1400, 700), ph('a hand grabbed'), 0.7)
mixin(fx, A.shimmer(2.0), ph('harrison was alive'), 0.7); mixin(fx, A.ding(2093), ph('harrison was alive') + 0.3, 0.6)
mixin(fx, A.click(), ph('decompression chamber'), 0.7); mixin(fx, A.whoosh(0.6, up=True), ph('decompression chamber') + 0.3, 0.4)
mixin(fx, A.boing(0.5, 300, 700), ph('one day'), 0.6)
mixin(fx, A.pop(1100, 500), ph('almost three', after=T['ask']), 0.6)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RB.D, mus, fx, os.path.join(RB.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
