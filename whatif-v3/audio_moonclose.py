"""Audio for episode 33 (Moon 10x closer): chapter score + SFX on every visual beat, clean VO on top."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import place, section, NOTE, rng
import render_moonclose as RM
from render_moonclose import ph, END, DURATION

A.set_duration(DURATION)
N = A.N
SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def rumble(d, g=1.0, f=36):
    t = A.tt(d)
    x = A.lp(rng.standard_normal(len(t)), 110) * 1.4 + np.sin(2 * np.pi * f * t) * 0.35
    return x * np.minimum(1, t / (d * 0.5)) * np.clip((d - t) / 0.4, 0, 1) * g


def surf(d, g=1.0):
    t = A.tt(d)
    env = np.minimum(1, t / (d * 0.35)) * np.clip((d - t) / (d * 0.5), 0, 1)
    return A.lp(rng.standard_normal(len(t)), 1400) * env * 0.5 * g


def quindar(g=1.0):
    t = A.tt(0.25)
    return np.sin(2 * np.pi * 2525 * t) * 0.25 * np.clip((0.25 - t) / 0.02, 0, 1) * np.minimum(1, t / 0.01) * g


def laser(g=1.0):
    t = A.tt(0.5); f = 2400 * np.exp(-t / 0.12) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.18) * 0.5 * g


def rewind_snd(d=1.6, g=1.0):
    t = A.tt(d)
    trem = (np.sin(2 * np.pi * (14 + 10 * t / d) * t) > 0).astype(float)
    x = A.bp(rng.standard_normal(len(t)), 1800, 5200) * trem * 0.35
    f = 600 + 900 * t / d
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.08
    return x * np.minimum(1, t / 0.05) * np.clip((d - t) / 0.1, 0, 1) * g


def crack(g=1.0):
    t = A.tt(0.6)
    return (A.hp(rng.standard_normal(len(t)), 1500) * np.exp(-t / 0.04) * 0.9 + A.lp(rng.standard_normal(len(t)), 300) * np.exp(-t / 0.2)) * g


def crickets(d, g=1.0):
    t = A.tt(d); x = np.zeros(len(t))
    for k, (f, rate, ph_) in enumerate(((4300, 13, 0.0), (4700, 11, 0.3), (3900, 15, 0.6))):
        gate = (np.sin(2 * np.pi * rate * t + ph_) > 0.2) * (np.sin(2 * np.pi * 0.7 * t + k) > -0.2)
        x += np.sin(2 * np.pi * f * t) * gate * 0.05
    return A.lp(x, 6000) * np.minimum(1, t / 0.5) * np.clip((d - t) / 0.4, 0, 1) * g


def tiptoe(n=6, gap=0.22, g=1.0):
    out = np.zeros(A.sec(n * gap + 0.4))
    for i in range(n):
        s = A.pluck(NOTE(72 + (0 if i % 2 == 0 else 3)), 0.15, 0.7)
        i0 = A.sec(i * gap); out[i0:i0 + len(s)] += s[:len(out) - i0]
    return out * g


T = {S['k']: S['t0'] for S in RM.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

# ---------------------------------------------------------------- score by chapter
section(mus, 0.0, T['apollo'], 'space', 'light', 'bell')
section(mus, T['apollo'], T['wider'], 'space', 'air', 'bell')
section(mus, T['wider'], T['ground'], 'up', 'groove', 'pluck')
section(mus, T['ground'], T['roche'], 'minor', 'groove', 'marimba')
section(mus, T['roche'], T['yes'], 'minor', 'light', 'bell')
section(mus, T['yes'], DURATION, 'up', 'groove', 'pluck')

# ---------------------------------------------------------------- SFX
mixin(fx, crickets(T['beautiful'], 0.6), 0.0)
mixin(fx, A.riser(1.2), ph('came ten') - 0.4, 0.6)
mixin(fx, rumble(2.2, 1.0), ph('came ten'))
mixin(fx, A.boom(2.0, 80, 30), ph('came ten') + 0.5, 0.9)
mixin(fx, A.shimmer(1.6), T['beautiful'] + 0.1, 0.5)
mixin(fx, A.whoosh(0.4), T['ocean'] - 0.15, 0.8)
mixin(fx, surf(2.6, 1.2), T['ocean'] + 0.1)
mixin(fx, A.boom(1.8, 70, 28), T['happened'], 0.8); mixin(fx, rumble(3.0, 0.7, 30), T['happened'])
mixin(fx, quindar(), T['apollo'] + 0.3, 0.8); mixin(fx, quindar(), ph('apollo') + 0.6, 0.6)
mixin(fx, laser(), ph('fire lasers') + 0.15, 0.9)
mixin(fx, laser(0.8), ph('and it showed') - 0.1, 0.6)
mixin(fx, A.whoosh(0.6, up=False), ph('drifting away'), 0.6)
mixin(fx, rewind_snd(1.6), T['rewind'] + 0.1, 0.8)
mixin(fx, A.whoosh(0.5), ph('ten times closer', after=T['rewind']) - 0.2, 0.8)
mixin(fx, A.riser(1.0), ph('ten times wider') - 0.9, 0.6); mixin(fx, A.boom(1.4, 90, 40), ph('ten times wider') + 0.2, 0.6)
mixin(fx, A.shimmer(1.4), ph('a hundred'), 0.6); mixin(fx, A.ding(), ph('a hundred') + 0.1, 0.5)
mixin(fx, A.click(), ph('never really') + 0.4, 0.8); mixin(fx, A.ding(2093), ph('never really') + 0.5, 0.5)
mixin(fx, crickets(T['tides'] - T['sleep'], 0.7), T['sleep'])
mixin(fx, A.womp(), ph('trying to sleep') + 0.1, 0.6)
mixin(fx, surf(2.5, 0.7), T['tides'] + 0.3)
mixin(fx, A.riser(1.2), ph('a thousand times') - 1.2, 0.7); mixin(fx, A.boom(2.2, 70, 26), ph('a thousand times'), 1.0)
mixin(fx, surf(3.5, 1.6), ph('the sea would') - 0.2)
mixin(fx, A.whoosh(0.8, up=False), ph('pull back out'), 0.7)
mixin(fx, A.bubbles(2.5), T['sub'], 0.7); mixin(fx, A.boing(0.6, 220, 520), ph('submarine'), 0.6)
mixin(fx, A.thump(), ph('twenty centimeters'), 0.6)
mixin(fx, A.boing(0.5, 500, 160), ph('squeezed like') + 0.2, 0.7); mixin(fx, crack(), ph('squeezed like') + 0.5, 0.6)
mixin(fx, rumble(2.4, 1.0), ph('more earthquakes')); mixin(fx, A.boom(2.0, 80, 30), ph('more volcanoes'), 1.0)
mixin(fx, A.roar(2.0), ph('more volcanoes') + 0.1, 0.3)
mixin(fx, rumble(3.0, 0.5, 28), T['io'] + 0.3)
mixin(fx, A.riser(1.5), ph('rip the moon') - 1.4, 0.7); mixin(fx, crack(1.2), ph('rip the moon'), 1.0); mixin(fx, A.boom(2.2, 70, 26), ph('rip the moon') + 0.05, 0.9)
mixin(fx, A.shimmer(2.0), ph('the pieces would'), 0.5)
mixin(fx, A.shimmer(1.8), T['ringsky'] + 0.1, 0.6)
mixin(fx, rumble(4.0, 0.35, 40), T['phobos'] + 0.2)
mixin(fx, A.shimmer(1.6), ph('become a ring'), 0.5)
mixin(fx, A.pop(), ph('yes'), 0.8); mixin(fx, A.ding(), ph('yes') + 0.05, 0.6)
mixin(fx, rumble(3.0, 0.7, 30), T['born'] + 0.1); mixin(fx, A.boom(1.6, 70, 30), T['born'], 0.6)
for i in range(10):
    mixin(fx, A.tick(), T['day18'] + 0.3 + i * 0.18, 0.5)
mixin(fx, tiptoe(8, 0.24, 0.8), T['sneak'] + 0.2)
mixin(fx, A.pop(800, 400), ph('fingernails'), 0.6)
mixin(fx, A.shimmer(1.6), ph('the perfect distance'), 0.6)
mixin(fx, A.whoosh(0.4), T['ask'] - 0.1, 0.6)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, rumble(1.6, 0.7), END + 0.4)
# caption pops on key captions
for t_ in (ph('came ten'), ph('drifting away'), ph('a hundred'), ph('a thousand times'), ph('submarine'), ph('most volcanic'), ph('a giant ring'), ph('eighteen hours')):
    mixin(fx, A.pop(1100, 500), t_, 0.35)

out = A.mixdown(RM.D, mus, fx, os.path.join(RM.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
