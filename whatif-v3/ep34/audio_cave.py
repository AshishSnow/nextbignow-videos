"""Audio for episode 34 (500 days in a cave): cave ambience with drips, clock ticks, rope creaks, flies, score per chapter."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import place, section, NOTE, rng
import render_cave as RC
from render_cave import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def drip(g=1.0, f=1800):
    t = A.tt(0.25)
    x = np.sin(2 * np.pi * (f + 600 * np.exp(-t / 0.01)) * t) * np.exp(-t / 0.05)
    return A.verb(x * 0.4 * g, wet=0.5)


def cave_air(d, g=1.0):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 240) * 0.35
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.08 * t)
    return x * np.minimum(1, t / 0.8) * np.clip((d - t) / 0.8, 0, 1) * g


def ticks(d, period=1.0, g=1.0, speedup=1.0):
    out = np.zeros(A.sec(d))
    t = 0.0; i = 0
    while t < d:
        s = A.tick(2600 if i % 2 == 0 else 2200, 0.9)
        i0 = A.sec(t); out[i0:i0 + len(s)] += s[:len(out) - i0]
        t += period / (1 + (speedup - 1) * t / d); i += 1
    return out * g


def creak(g=1.0):
    t = A.tt(0.6)
    f = 120 + 40 * np.sin(2 * np.pi * 7 * t)
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.2
    return A.lp(x, 900) * np.exp(-t / 0.25) * g


def buzz_swarm(d, g=1.0):
    t = A.tt(d)
    x = np.zeros(len(t))
    for k in range(6):
        f = 180 + 60 * rng.random() + 25 * np.sin(2 * np.pi * (0.3 + rng.random()) * t + k)
        x += np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR + k)) * 0.08
    x = A.bp(x, 150, 2500)
    env = np.minimum(1, t / 0.6) * np.clip((d - t) / 0.6, 0, 1)
    return x * env * g


def snore(d=1.8, g=1.0):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.55 * t)) ** 3
    return x * 0.5 * g


def yawn(g=1.0):
    t = A.tt(0.9)
    f = 300 + 120 * np.sin(np.pi * t / 0.9)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.3 + 0.2 * np.sin(2 * np.pi * 2 * np.cumsum(f) / SR))
    return A.lp(x, 1500) * np.sin(np.pi * t / 0.9) * 0.25 * g


def rewind_zip(d=0.6, g=1.0):
    t = A.tt(d); f = 1400 - 1000 * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.clip((d - t) / 0.1, 0, 1) * np.minimum(1, t / 0.02) * 0.25 * g


T = {S['k']: S['t0'] for S in RC.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

# ---------------------------------------------------------------- score
section(mus, 0.0, T['clock'], 'minor', 'light', 'marimba')
section(mus, T['clock'], T['memory'], 'space', 'groove', 'pluck')
section(mus, T['memory'], T['rescue'], 'up', 'groove', 'marimba')
section(mus, T['rescue'], T['why'], 'minor', 'light', 'bell')
section(mus, T['why'], DURATION, 'up', 'groove', 'pluck')

# ---------------------------------------------------------------- cave ambience in every cave scene
for k, nxt in (('hook', 'clock'), ('siffre', '48'), ('count', 'memory'), ('hobbies', 'rescue'), ('rescue', 'why'), ('ask', None)):
    t0 = T[k]; t1 = T[nxt] if nxt else DURATION
    mixin(fx, cave_air(t1 - t0, 0.8), t0)
    for i in range(int((t1 - t0) / 1.7)):
        tt_ = t0 + 0.4 + i * 1.7 + 0.5 * rng.random()
        if tt_ < t1 - 0.3: mixin(fx, drip(0.6, 1500 + 700 * rng.random()), tt_)

# ---------------------------------------------------------------- SFX by beat
for i, phr in enumerate(('no sunlight', 'no clock', 'no phone', 'nobody')):
    mixin(fx, A.pop(900 - i * 80, 400), ph(phr), 0.7); mixin(fx, A.buzz(0.5), ph(phr) + 0.05, 0.5)
mixin(fx, A.riser(1.0), ph('one woman') - 0.8, 0.6)
mixin(fx, creak(), T['early'] + 0.3, 0.8); mixin(fx, creak(0.7), T['early'] + 1.0, 0.8)
mixin(fx, snore(1.6, 0.7), T['early'] + 0.2)
mixin(fx, A.pop(1200, 600), ph('she thought'), 0.8); mixin(fx, A.boing(0.5, 300, 700), ph('early'), 0.7)
mixin(fx, A.wind(2.5, 0.5), T['descent'] + 0.1)
mixin(fx, creak(0.8), ph('climbed down') + 0.2); mixin(fx, creak(0.6), ph('climbed down') + 0.9)
mixin(fx, A.thump(), ph('seventy meters'), 0.7)
mixin(fx, A.click(), ph('the rule was') + 0.2, 0.8)
mixin(fx, A.womp(), ph('family dies') + 0.1, 0.5)
mixin(fx, A.pop(700, 300), ph('panic button'), 0.8)
mixin(fx, A.ding(1046), ph('never touched') + 0.1, 0.5)
mixin(fx, ticks(ph('twenty-four hours') - T['clock'], 1.0, 0.7), T['clock'])
mixin(fx, A.boom(1.2, 90, 40), ph('your clock breaks') + 0.1, 0.6); mixin(fx, A.click(), ph('your clock breaks') + 0.15, 0.9)
mixin(fx, A.shimmer(1.4), ph('sunlight resets'), 0.6); mixin(fx, A.ding(), ph('sunlight resets') + 0.1, 0.5)
mixin(fx, A.whoosh(0.5, up=False), ph('in a cave'), 0.6)
mixin(fx, ticks(2.2, 0.5, 0.8, speedup=3.0), ph('drifts') - 0.2); mixin(fx, A.boing(0.6, 400, 150), ph('drifts') + 0.2, 0.6)
mixin(fx, A.whoosh(0.45), T['siffre'] - 0.1, 0.7)
mixin(fx, A.pop(), ph('texas'), 0.6)
mixin(fx, A.pop(1100, 500), ph('two hundred'), 0.6)
mixin(fx, ticks(ph("didn't even") - ph('sometimes his body'), 0.45, 0.7, speedup=2.0), ph('sometimes his body'))
mixin(fx, A.ding(1318), ph('forty-eight') + 0.2, 0.6)
mixin(fx, yawn(), ph('imagine staying') + 0.4, 0.8); mixin(fx, A.boing(0.5, 250, 500), ph('tuesday'), 0.6)
for i in range(8):
    mixin(fx, A.tick(3200, 0.6), ph('count the days') + 0.2 + i * 0.22, 0.6)
mixin(fx, A.pop(1300, 600), ph('sixty-five'), 0.8)
mixin(fx, A.womp(), ph('gave up') + 0.1, 0.6); mixin(fx, A.click(), ph('gave up') + 0.5, 0.6)
mixin(fx, A.whoosh(0.5), T['memory'] - 0.1, 0.7)
mixin(fx, A.chatter(1.0), ph('goes weird') + 0.2, 0.3)
mixin(fx, A.pop(600, 300), ph('the day before'), 0.6)
mixin(fx, ticks(ph('five minutes') - ph('counted to one'), 1.0, 0.8), ph('counted to one'))
mixin(fx, A.ding(2093), ph('five minutes') + 0.1, 0.6)
mixin(fx, A.pop(1000, 500), ph('five real'), 0.5)
for phr, snd in (('sixty books', A.pop(900, 450)), ('knitted', A.tick(2400, 0.8)), ('exercised', A.thump(0.7)), ('talked to herself', A.pop(1200, 700))):
    mixin(fx, snd, ph(phr), 0.7)
mixin(fx, creak(0.8), T['service'] + 0.3); mixin(fx, creak(0.6), T['service'] + 1.0)
mixin(fx, A.ding(1568), ph('best room') + 0.1, 0.6); mixin(fx, A.shimmer(1.0), ph('best room'), 0.4)
mixin(fx, A.riser(1.0), ph('flies') - 0.9, 0.6)
mixin(fx, buzz_swarm(ph('finally in april') - ph('flies', end=True) - 0.3, 0.9), ph('flies', end=True) + 0.1)
mixin(fx, creak(0.8), T['rescue'] + 0.3); mixin(fx, snore(2.0, 0.6), T['rescue'] + 0.5)
mixin(fx, A.pop(1200, 600), ph('already'), 0.8); mixin(fx, A.boing(0.5, 300, 700), ph('no way'), 0.6)
mixin(fx, A.whoosh(0.5), T['160'] - 0.1, 0.7)
mixin(fx, A.riser(1.2), ph('five hundred', after=ph('one hundred and sixty')) - 1.1, 0.7)
mixin(fx, A.boom(1.6, 80, 32), ph('five hundred', after=ph('one hundred and sixty')) + 0.1, 0.9)
mixin(fx, A.pop(800, 400), ph('almost a year'), 0.6)
mixin(fx, A.ding(1318), ph("didn't want to") + 0.1, 0.5); mixin(fx, A.boing(0.5, 250, 550), ph("hadn't finished") + 0.2, 0.6)
mixin(fx, A.shimmer(1.6), T['why'] + 0.1, 0.5)
for i in range(3): mixin(fx, A.pop(1000 + i * 150, 500), T['why'] + 0.3 + i * 0.25, 0.6)
mixin(fx, A.whoosh(0.6), ph('astronauts') - 0.2, 0.7)
mixin(fx, A.pop(700, 350), ph('long missions') + 0.3, 0.6)
mixin(fx, A.click(), T['phone'] + 0.3, 0.7); mixin(fx, A.ding(2093), ph('see the sun') + 0.1, 0.6)
mixin(fx, A.whoosh(0.4), T['ask'] - 0.1, 0.6)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)
for phr in ('five hundred', 'your clock breaks', 'forty-eight', 'sixty-five', 'flies', 'already', 'astronauts'):
    mixin(fx, A.pop(1100, 500), ph(phr), 0.3)

out = A.mixdown(RC.D, mus, fx, os.path.join(RC.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
