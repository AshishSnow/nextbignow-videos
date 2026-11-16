"""Audio for ep 63 (captcha): NO background music. Voice + a few light comic sound effects."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import rng
import render_captcha as RH
from render_captcha import ph, END, DURATION

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


T = {S['k']: S['t0'] for S in RH.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))
mixin(fx, A.pop(900, 450), ph('not a robot'), 0.25)
mixin(fx, A.boom(1.0, 60, 30), ph('handed a hacker'), 0.25)
for k_ in ('how', 'trick', 'stats', 'rule', 'fix', 'ask'): mixin(fx, swish(0.8), T[k_] + 0.2)
for p_ in ('press windows and r', 'press control and v', 'press enter', 'windows plus r opens', 'control v pastes', 'enter runs it'):
    mixin(fx, A.pop(1100, 600), ph(p_) + 0.5, 0.2)
mixin(fx, sub(1.0), ph('you just hacked yourself'))
mixin(fx, A.ding(1318), ph('secretly copied a command'), 0.12)
for p_ in ('saved passwords', 'banking logins', 'even your crypto'): mixin(fx, A.pop(800, 400), ph(p_), 0.2)
mixin(fx, A.boom(1.0, 55, 28), ph('forty seven percent'), 0.22)
mixin(fx, A.pop(800, 400), ph('seventeen thousand'), 0.22)
mixin(fx, A.ding(1568), ph('close the tab'), 0.14)
mixin(fx, A.pop(900, 450), ph('yes or no'), 0.3)
mixin(fx, sub(0.8), END + 0.9)

out = A.mixdown(RH.D, mus, fx, os.path.join(RH.D, 'vo48.wav'), music_lufs=None)
print('mix ->', out)
