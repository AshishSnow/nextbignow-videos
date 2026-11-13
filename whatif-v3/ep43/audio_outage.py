"""Audio for ep 43 (editorial look): restrained news-style bed, paper swishes on cards, glitch on 'stopped', soft bass hits."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_outage as RO
from render_outage import ph, END, DURATION

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

section(mus, 0.0, T['three'], 'minor', 'light', 'pluck')
section(mus, T['three'], T['predict'], 'space', 'light', 'bell')
section(mus, T['predict'], T['fear'], 'minor', 'groove', 'pluck')
section(mus, T['fear'], DURATION, 'space', 'air', 'bell')

mixin(fx, swish(1.2), 0.2)
mixin(fx, glitch(0.7, 0.7), ph('stopped') - 0.05); mixin(fx, sub(0.9), ph('stopped'))
for i, p_ in enumerate(('outlook', 'teams', 'microsoft')): mixin(fx, A.pop(900 + i * 120, 400), ph(p_), 0.35)
mixin(fx, A.whoosh(0.5), ph("here's the real question") - 0.15, 0.5); mixin(fx, sub(0.8), ph("here's the real question"))
for i in range(9): mixin(fx, A.tick(1800, 0.5), ph('break everything') + i * 0.12, 0.5)
for k_ in ('numbers', 'who', 'cause', 'three', 'rent', 'pattern', 'gov', 'planb', 'ask'):
    mixin(fx, swish(1.0), T[k_] + 0.2)
mixin(fx, A.riser(1.0), ph('at the peak') - 0.6, 0.35); mixin(fx, sub(0.8), ph('at the peak') + 0.4)
for p_ in ('schools', 'banks', 'hospitals', 'parliament'): mixin(fx, swish(0.9), ph(p_) - 0.1)
mixin(fx, sub(0.8), ph('not hackers'))
mixin(fx, glitch(0.5, 0.5), ph('unexpectedly went offline'))
mixin(fx, A.boom(1.0, 70, 30), ph('got crushed'), 0.5)
mixin(fx, A.pop(800, 400), ph('sixty percent'), 0.4)
mixin(fx, glitch(0.8, 0.4), T['rent'] + 0.6)
mixin(fx, sub(0.7), ph('they rent it'))
for p_ in ('july twenty', 'october twenty twenty'): mixin(fx, swish(1.0), ph(p_) - 0.15)
mixin(fx, A.boing(0.4, 300, 600), ph('yes beds'), 0.4)
mixin(fx, A.whoosh(0.5), T['predict'] - 0.1, 0.5); mixin(fx, sub(1.0), ph('going to get bigger'))
for p_ in ('in europe', 'the uk is moving'): mixin(fx, swish(1.0), ph(p_) - 0.15)
for p_ in ('a backup cloud', 'backup way to talk', 'plain old paper'): mixin(fx, A.ding(1568), ph(p_), 0.25)
mixin(fx, A.click(), ph('until the day') + 0.3, 0.8)
mixin(fx, A.pop(900, 450), ph('comments') if 'comments' in [w for w, _, _ in RO.TOK] else END - 1.0, 0.4)
mixin(fx, A.riser(1.2), END, 0.5); mixin(fx, sub(1.0), END + 0.9)

out = A.mixdown(RO.D, mus, fx, os.path.join(RO.D, 'vo48.wav'), music_lufs=-26.0)
print('mix ->', out)
