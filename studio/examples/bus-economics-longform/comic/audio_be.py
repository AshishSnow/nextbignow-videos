"""Audio for the bus-economics long-form: NO background music. Voice + light comic SFX on key beats."""
import os, sys
os.environ['NBN_ORIENT'] = 'land'
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_be as RB
from render_be import L, END, DURATION

A.set_duration(DURATION)
N = A.N


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


T = {S['k']: S['t0'] for S in RB.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
for k in ('question', 'verdict'): mixin(fx, A.whoosh(0.5), T[k] - 0.1, 0.4)
for k in ('machine', 'earn', 'germany', 'money', 'rules', 'start', 'end'): mixin(fx, swish(0.9), T[k] + 0.15)
POPS = ['h3', 'h4', 'a3', 'a4', 'a7', 'a9', 'b3', 'b5', 'b6', 'b9', 'b13', 'b16', 'c3', 'c4b', 'c4c', 'c5b', 'c6', 'c7', 'c8', 'c9', 'c12', 'c13', 'c14',
        'd2', 'd6', 'd7', 'd8', 'd10', 'd11', 'm3', 'm4', 'm5', 'm6', 'e2', 'e3', 'e4', 'e6', 'e7', 'f2', 'f4', 'g2', 'g3', 'g4']
for lid in POPS: mixin(fx, A.pop(800, 400), L(lid) + 0.05, 0.2)
for lid in ('a8b', 'c13', 'c14', 'd13', 'b6'): mixin(fx, A.ding(1568), L(lid) + 0.5, 0.12)
for lid in ('h4', 'a3', 'c5b', 'd6', 'd13', 'm8', 'f7'): mixin(fx, A.boom(1.0, 60, 30), L(lid) + 0.4, 0.28)
mixin(fx, sub(0.7), L('c4d') + 0.3)
mixin(fx, sub(0.6), L('d15'))
mixin(fx, A.pop(900, 450), L('z4') + 1.4, 0.3); mixin(fx, A.pop(900, 450), L('z4') + 2.1, 0.3)
mixin(fx, sub(0.8), END + 0.9)
out = A.mixdown(RB.D, mus, fx, os.path.join(RB.D, 'vo.wav'), music_lufs=None)
print('mix ->', out)
