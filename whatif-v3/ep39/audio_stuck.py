"""Audio for episode 39 (stuck in space for a year): launch roar, station hum, impact + hiss, sunrise chimes, treadmill, landing."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_stuck as RS
from render_stuck import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def hum(d, g=1.0):
    t = A.tt(d)
    x = 0.4 * np.sin(2 * np.pi * 60 * t) + 0.2 * np.sin(2 * np.pi * 120 * t) + 0.4 * A.lp(rng.standard_normal(len(t)), 400)
    return x * np.minimum(1, t / 0.6) * np.clip((d - t) / 0.6, 0, 1) * 0.08 * g


def hiss(d, g=1.0):
    t = A.tt(d)
    return A.hp(rng.standard_normal(len(t)), 3000) * np.minimum(1, t / 0.1) * np.clip((d - t) / 0.4, 0, 1) * 0.12 * g


def steps(d, rate=4.0, g=1.0):
    out = np.zeros(A.sec(d))
    for i in range(int(d * rate)):
        s = A.thump(0.4); i0 = A.sec(i / rate); out[i0:i0 + len(s)] += s[:len(out) - i0]
    return out * g


T = {S['k']: S['t0'] for S in RS.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['hit'], 'space', 'light', 'bell')
section(mus, T['hit'], T['days'], 'minor', 'air', 'bell')
section(mus, T['days'], T['home'], 'up', 'groove', 'marimba')
section(mus, T['home'], DURATION, 'up', 'groove', 'pluck')

mixin(fx, A.shimmer(1.4), 0.2, 0.5)
mixin(fx, A.womp(), ph("can't come home"), 0.6)
mixin(fx, A.pop(900, 400), ph('frank rubio'), 0.5)
mixin(fx, A.roar(3.0), T['launch'] + 0.6, 0.8); mixin(fx, A.boom(1.6, 70, 30), T['launch'] + 0.6, 0.7)
mixin(fx, A.whoosh(0.5), ph('the plan was simple') - 0.1, 0.5)
mixin(fx, A.ding(1318), ph('six months', after=ph('the plan was simple')), 0.5)
mixin(fx, hum(T['days'] - T['hit']), T['hit'])
mixin(fx, A.fall_whistle(1.0), ph('tiny space rock'), 0.4)
mixin(fx, A.boom(1.2, 90, 40), ph('tiny space rock') + 0.9, 0.9); mixin(fx, A.pop(1500, 700), ph('tiny space rock') + 0.9, 0.7)
mixin(fx, hiss(ph('without that coolant') - ph('coolant started') + 0.3), ph('coolant started') - 0.2)
mixin(fx, A.riser(1.0), ph('overheat') - 0.8, 0.5)
mixin(fx, A.thump(), ph('the answer was no'), 0.9)
mixin(fx, A.whoosh(0.6), T['wait'] + 0.2, 0.6)
mixin(fx, A.boing(0.6, 300, 700), ph('six months turned') + 0.6, 0.6)
for i in range(16):
    mixin(fx, A.ding(1046 * 2 ** ((i % 8) / 12)), ph('sixteen sunrises') - 0.2 + i * 0.1, 0.25)
mixin(fx, hum(T['taller'] - T['life'], 1.2), T['life'])
mixin(fx, A.pop(700, 300), ph('drinking water'), 0.6); mixin(fx, A.bubbles(1.5), ph('recycled') + 0.2, 0.5)
mixin(fx, A.boing(0.5, 250, 600), ph('sweat and pee'), 0.6)
mixin(fx, A.ding(1568), ph("yesterday's coffee") + 0.4, 0.5)
mixin(fx, A.riser(1.2), ph('spine stretches'), 0.5); mixin(fx, A.pop(1200, 600), ph('a few centimeters'), 0.6)
mixin(fx, A.womp(), ph('lose strength'), 0.5)
mixin(fx, steps(T['home'] - ph('exercise about two'), 4.0, 0.5), ph('exercise about two'))
mixin(fx, A.wind(2.5, 0.5), T['home'] + 0.2)
mixin(fx, A.thump(), T['home'] + 3.4, 0.9)
mixin(fx, A.riser(1.0), ph('three hundred seventy one') - 0.8, 0.5); mixin(fx, A.boom(1.4, 80, 32), ph('three hundred seventy one'), 0.7)
mixin(fx, A.shimmer(1.4), ph('the longest'), 0.6)
for i in range(6): mixin(fx, A.tick(2600, 0.6), T['dist'] + 0.4 + i * 0.25, 0.5)
mixin(fx, A.whoosh(0.5), ph('to the moon and back'), 0.6)
mixin(fx, A.boing(0.5, 300, 700), ph('would have said no'), 0.6)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RS.D, mus, fx, os.path.join(RS.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
