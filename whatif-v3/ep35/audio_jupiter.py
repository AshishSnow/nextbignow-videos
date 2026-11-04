"""Audio for episode 35 (falling into Jupiter): space score, entry roar, radio beeps, wind, pressure creaks, metal drone."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import place, section, NOTE, rng
import render_jupiter as RJ
from render_jupiter import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def beep(f=1800, d=0.12, g=1.0):
    t = A.tt(d)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.005) * np.clip((d - t) / 0.01, 0, 1) * 0.3 * g


def beeps(n, gap, f=1800, g=1.0):
    out = np.zeros(A.sec(n * gap + 0.2))
    for i in range(n):
        s = beep(f if i % 2 == 0 else f * 1.25, 0.1, g); i0 = A.sec(i * gap); out[i0:i0 + len(s)] += s
    return out


def roar_long(d, g=1.0):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 700) * 0.6 + A.lp(rng.standard_normal(len(t)), 160)
    return x * np.minimum(1, t / 0.3) * np.clip((d - t) / 0.6, 0, 1) * 0.6 * g


def creak(g=1.0):
    t = A.tt(0.8)
    f = 90 + 30 * np.sin(2 * np.pi * 5 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.2
    return A.lp(x, 700) * np.exp(-t / 0.35) * g


def drone(d, f=55, g=1.0):
    t = A.tt(d)
    x = sum(np.sin(2 * np.pi * f * k * t + k) / k for k in (1, 2, 3, 5))
    x = x * (0.7 + 0.3 * np.sin(2 * np.pi * 0.2 * t))
    return x * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.8, 0, 1) * 0.15 * g


def sniff(g=1.0):
    t = A.tt(0.5)
    return A.bp(rng.standard_normal(len(t)), 1500, 5000) * (np.sin(np.pi * t / 0.5) ** 2) * 0.3 * g


def spray(d=0.6, g=1.0):
    t = A.tt(d)
    return A.hp(rng.standard_normal(len(t)), 3000) * np.minimum(1, t / 0.02) * np.clip((d - t) / 0.2, 0, 1) * 0.3 * g


def grunt(g=1.0):
    t = A.tt(0.35); f = 160 - 40 * t
    return A.lp(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.25, 900) * np.sin(np.pi * t / 0.35) * g


T = {S['k']: S['t0'] for S in RJ.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['turn'], 'space', 'light', 'bell')
section(mus, T['turn'], T['squeeze'], 'up', 'groove', 'pluck')
section(mus, T['squeeze'], T['orbiter'], 'minor', 'air', 'bell')
section(mus, T['orbiter'], T['become'], 'space', 'light', 'marimba')
section(mus, T['become'], DURATION, 'up', 'groove', 'pluck')

mixin(fx, A.whoosh(0.6, up=False), 0.3, 0.6)
mixin(fx, A.boing(0.6, 400, 150), ph('never hit'), 0.6)
mixin(fx, A.pop(800, 400), ph("there isn't") + 0.1, 0.7)
mixin(fx, beeps(4, 0.25), ph('talked to us') - 0.1, 0.7)
mixin(fx, A.riser(1.0), T['entry'] - 0.6, 0.6)
mixin(fx, roar_long(ph('the air in front') - T['entry'] + 1.5, 1.0), T['entry'] + 0.3)
mixin(fx, A.pop(1100, 500), ph('one hundred seventy'), 0.5)
mixin(fx, A.whoosh(0.5), T['india'] + 0.3, 0.8)
for i in range(6): mixin(fx, A.tick(2600, 0.7), T['india'] + 0.4 + i * 0.3, 0.5)
mixin(fx, A.ding(1568), T['india'] + 2.3, 0.5)
mixin(fx, A.roar(2.0), T['heat'] + 0.1, 0.4)
mixin(fx, A.boom(1.6, 80, 32), ph('braked so hard'), 0.9)
mixin(fx, A.womp(), ph('imagine your seatbelt') + 0.5, 0.7)
mixin(fx, A.whoosh(0.5, up=False), T['turn'] + 0.1, 0.6)
mixin(fx, A.thump(), ph('you get heavy'), 0.8)
mixin(fx, A.tick(2200, 0.9), ph('one hundred and twenty') - 0.3, 0.6)
mixin(fx, A.ding(1046), ph('one hundred and twenty') + 0.2, 0.6)
for i in range(4): mixin(fx, grunt(0.7), ph('leg day') + 0.3 + i * 0.52)
mixin(fx, spray(0.6), ph('ammonia') + 0.1, 0.9); mixin(fx, sniff(), ph('ammonia') + 0.8, 0.8)
mixin(fx, A.boing(0.5, 250, 550), ph('bathroom floor') + 0.2, 0.6)
mixin(fx, A.wind(ph('the deeper you fall') - T['wind'], 1.2), T['wind'])
mixin(fx, A.pop(1000, 500), ph('strongest hurricane'), 0.5)
mixin(fx, creak(), ph('squeezes you') if False else T['squeeze'] + 0.6, 0.8)
mixin(fx, beeps(6, 0.35, 1600, 0.8), T['squeeze'] + 0.5)
mixin(fx, beep(900, 1.2, 0.8), ph('went silent') + 0.1, 0.7)
mixin(fx, creak(0.8), ph('twenty-three') + 0.1)
mixin(fx, A.boom(1.4, 70, 30), ph('only the first hour'), 0.6)
mixin(fx, drone(T['metal'] - T['black'], 45, 1.0), T['black'])
mixin(fx, A.bubbles(2.5), ph('slowly sink'), 0.6)
mixin(fx, A.shimmer(1.6), T['metal'] + 0.1, 0.6)
mixin(fx, drone(T['core'] - T['metal'], 82, 1.0), T['metal'])
mixin(fx, A.zap(), ph('magnetic field'), 0.6)
mixin(fx, A.riser(1.5), T['core'] + 0.3, 0.5)
for w in ('crushed', 'cooked', 'melted'):
    mixin(fx, A.thump(), ph(w), 0.6)
mixin(fx, A.whoosh(0.5), T['orbiter'] - 0.1, 0.7)
mixin(fx, roar_long(2.0, 0.8), ph('crashed it'))
mixin(fx, A.boom(1.6, 80, 32), ph('on purpose') - 0.2, 0.7)
mixin(fx, A.shimmer(1.4), ph('maybe life'), 0.6)
mixin(fx, A.buzz(0.6), ph('earth germ') + 0.6, 0.5)
mixin(fx, A.shimmer(2.0), T['become'] + 0.2, 0.5)
mixin(fx, A.ding(2093), ph('few atoms'), 0.5)
mixin(fx, A.whoosh(0.4), T['ask'] - 0.1, 0.6)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RJ.D, mus, fx, os.path.join(RJ.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
