"""Audio for episode 40 (alone on an island): waves, gulls, creaking ship, sea lion barks, goat bleats, rat squeaks, cat purrs."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_island as RI
from render_island import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def waves(d, g=1.0):
    t = A.tt(d)
    x = A.bp(rng.standard_normal(len(t)), 200, 2000) * (0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * t)) ** 2)
    return x * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.8, 0, 1) * 0.12 * g


def creak(g=1.0):
    t = A.tt(0.8)
    f = 110 + 30 * np.sin(2 * np.pi * 5 * t)
    return A.lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.2, 800) * np.exp(-t / 0.35) * g


def bark(g=1.0):
    t = A.tt(0.35); f = 260 - 80 * t / 0.35
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3 + A.bp(rng.standard_normal(len(t)), 300, 1500) * 0.3
    return A.lp(x, 1400) * np.sin(np.pi * t / 0.35) * g


def bleat(g=1.0):
    t = A.tt(0.6); f = 520 + 40 * np.sin(2 * np.pi * 14 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return A.bp(x, 300, 3500) * np.sin(np.pi * t / 0.6) * 0.2 * g


def squeak(g=1.0):
    t = A.tt(0.12)
    return np.sin(2 * np.pi * (3000 + 2000 * t / 0.12) * t) * np.sin(np.pi * t / 0.12) * 0.1 * g


def meow(g=1.0):
    t = A.tt(0.6); f = 600 + 350 * np.sin(np.pi * t / 0.6)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    return A.bp(x, 400, 4000) * np.sin(np.pi * t / 0.6) ** 1.5 * 0.22 * g


T = {S['k']: S['t0'] for S in RI.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['twist'], 'up', 'groove', 'marimba')
section(mus, T['twist'], T['lions'], 'minor', 'air', 'bell')
section(mus, T['lions'], T['spanish'], 'up', 'groove', 'pluck')
section(mus, T['spanish'], T['rescue'], 'minor', 'light', 'bell')
section(mus, T['rescue'], DURATION, 'up', 'groove', 'marimba')

mixin(fx, waves(T['lions'] + 3.0), 0.0)
mixin(fx, A.pop(900, 400), ph('your own idea'), 0.6)
mixin(fx, A.shimmer(1.2), ph('famous books'), 0.5)
for i in range(3): mixin(fx, creak(0.8), T['ship'] + 0.4 + i * 1.1)
mixin(fx, A.pop(700, 300), ph('drop me off'), 0.8)
mixin(fx, A.boing(0.6, 400, 150), ph('said fine'), 0.6)
for p_ in ('a hatchet', 'a knife', 'cooking pot', 'a bible'): mixin(fx, A.pop(1000, 500), ph(p_), 0.6)
mixin(fx, A.womp(), ph('regretted it'), 0.5)
mixin(fx, A.thump(), ph('the answer was no'), 0.9)
mixin(fx, creak(1.0), ph('it sank') - 0.3); mixin(fx, A.bubbles(2.5), ph('it sank') + 0.3, 0.7); mixin(fx, A.boom(1.2, 80, 34), ph('it sank'), 0.6)
for i in range(5): mixin(fx, bark(0.8), T['lions'] + 0.5 + i * 0.75)
mixin(fx, A.whoosh(0.5), ph('moved inland'), 0.6)
for i in range(3): mixin(fx, bleat(1.0), T['goats'] + 0.6 + i * 0.9)
mixin(fx, A.whoosh(0.6), ph('chased them down'), 0.6)
for i in range(8): mixin(fx, A.thump(0.5), ph('chased them down') + 0.2 + i * 0.22)
mixin(fx, A.ding(1568), ph('outrun them'), 0.5)
for i in range(10): mixin(fx, squeak(1.0), T['rats'] + 0.4 + i * 0.28)
for i in range(3): mixin(fx, meow(1.0), ph('tamed the wild cats') + 0.3 + i * 0.5)
mixin(fx, A.pop(1100, 500), ph('goat skins'), 0.6)
mixin(fx, A.riser(1.0), T['spanish'], 0.4)
mixin(fx, A.womp(), ph('at war'), 0.5)
mixin(fx, A.whoosh(0.5, up=True), ph('climbed a tree'), 0.6)
mixin(fx, waves(T['book'] - T['rescue']), T['rescue'])
mixin(fx, A.shimmer(1.6), T['rescue'] + 0.2, 0.6)
mixin(fx, A.boing(0.5, 250, 600), ph('looked wilder'), 0.6)
mixin(fx, A.ding(2093), ph('four years and four'), 0.5)
mixin(fx, A.shimmer(1.4), ph('robinson crusoe'), 0.6)
mixin(fx, waves(DURATION - T['ask']), T['ask'])
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RI.D, mus, fx, os.path.join(RI.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
