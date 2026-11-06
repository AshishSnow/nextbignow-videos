"""Audio for episode 36 (couldn't stop sneezing): synthesized ah-choo, ticking clock, car hum, pressure hiss, record fanfare."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import audiokit as A
from audiokit import section, rng
import render_sneeze as RS
from render_sneeze import ph, END, DURATION

A.set_duration(DURATION)
N = A.N; SR = A.SR


def mixin(out, s, t, g=1.0):
    if s.ndim == 1: s = np.stack([s, s], 1)
    i = A.sec(t)
    if i < 0: s = s[-i:]; i = 0
    n = min(len(s), len(out) - i)
    if n > 0: out[i:i + n] += s[:n] * g
    return out


def achoo(g=1.0, muffled=False, pitch=1.0):
    """'ah' inhale (rising breathy vowel) then a sharp 'CHOO' noise burst with a vowel tail. Blast lands at +0.55 s."""
    t1 = A.tt(0.5)
    f = (380 + 260 * t1 / 0.5) * pitch
    vow = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 + A.bp(rng.standard_normal(len(t1)), 900, 2600) * 0.5
    inh = A.bp(vow, 500, 3000) * np.sin(np.pi * np.minimum(1, t1 / 0.5)) ** 2 * 0.35
    t2 = A.tt(0.45)
    burst = A.bp(rng.standard_normal(len(t2)), 1800 * pitch, 7000) * np.exp(-t2 / 0.06) * 1.3
    ff = 300 * pitch * (1 - 0.3 * t2 / 0.45)
    oo = (np.sin(2 * np.pi * np.cumsum(ff) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(ff) / SR)) * np.minimum(1, t2 / 0.02) * np.exp(-t2 / 0.14) * 0.45
    ch = A.lp(burst + oo, 2500) if muffled else burst + oo
    out = np.zeros(A.sec(1.05))
    out[:len(inh)] += inh
    i0 = A.sec(0.55); out[i0:i0 + len(ch)] += ch[:len(out) - i0]
    return out * 0.6 * g


def hiss(d, g=1.0):
    t = A.tt(d)
    return A.hp(rng.standard_normal(len(t)), 2500) * np.minimum(1, t / 0.4) * np.clip((d - t) / 0.3, 0, 1) * 0.12 * g


def engine_hum(d, g=1.0):
    t = A.tt(d)
    x = np.sin(2 * np.pi * 48 * t) + 0.5 * np.sin(2 * np.pi * 96 * t + 1) + 0.3 * A.lp(rng.standard_normal(len(t)), 200)
    return x * np.minimum(1, t / 0.5) * np.clip((d - t) / 0.5, 0, 1) * 0.12 * g


def snore(d=2.0, g=1.0):
    t = A.tt(d)
    return A.lp(rng.standard_normal(len(t)), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.6 * t)) ** 3 * 0.5 * g


T = {S['k']: S['t0'] for S in RS.SCENES}
mus = np.zeros((N, 2)); fx = np.zeros((N, 2))

section(mus, 0.0, T['what'], 'up', 'groove', 'pluck')
section(mus, T['what'], T['hold'], 'space', 'light', 'marimba')
section(mus, T['hold'], T['facts'], 'minor', 'air', 'bell')
section(mus, T['facts'], T['stop'], 'up', 'groove', 'marimba')
section(mus, T['stop'], DURATION, 'up', 'groove', 'pluck')

# ---------------------------------------------------------------- sneezes (blast = event + 0.55, matching sneezer())
k = 0
while 0.5 + 1.5 * k < T['donna'] - 0.6:
    mixin(fx, achoo(0.45, pitch=0.9 + 0.1 * (k % 2)), 0.5 + 1.5 * k); k += 1
for p in ('she sneezed', 'then again', 'and again'):
    mixin(fx, achoo(0.6, pitch=1.25), ph(p) - 0.45)
k = 0
while T['million'] + 0.1 + 1.4 * k < T['perday'] - 1.0:
    mixin(fx, achoo(0.25, pitch=1.25), T['million'] + 0.1 + 1.4 * k); k += 1
mixin(fx, achoo(0.55, pitch=1.25), ph('try eating soup') + 0.3)
mixin(fx, A.pop(500, 200), ph('try eating soup') + 0.9, 0.7)
mixin(fx, achoo(0.55, pitch=1.25), ph('try doing homework') + 0.25); mixin(fx, A.whoosh(0.4), ph('try doing homework') + 0.85, 0.6)
mixin(fx, achoo(0.6, pitch=1.25), ph('hide and seek') + 0.1); mixin(fx, A.ding(1318), ph('hide and seek') + 0.9, 0.5)
mixin(fx, achoo(0.7, pitch=1.25), ph('slam it out') - 0.55)
mixin(fx, achoo(0.45), T['drops'] + 0.1)
mixin(fx, achoo(0.5, muffled=True), ph('your mom was right') + 0.6 - 0.25)
mixin(fx, achoo(0.5), ph('step into bright') + 0.5)
mixin(fx, achoo(0.45, pitch=1.25), ph('eyebrows') + 0.2 - 0.55)
mixin(fx, achoo(0.45), ph('stomach gets too full') + 0.6 - 0.55)
S0 = T['ask']; tl = ph('let it out')
for i in range(3):
    if S0 + 0.3 + 1.1 * i < tl - 0.5: mixin(fx, achoo(0.4, pitch=0.95 + 0.05 * i), S0 + 0.3 + 1.1 * i)
mixin(fx, achoo(0.5), tl - 0.3)

# ---------------------------------------------------------------- story beats
mixin(fx, A.pop(900, 400), ph('two and a half'), 0.6)
mixin(fx, A.whoosh(0.45), T['donna'] - 0.1, 0.6)
mixin(fx, A.pop(1100, 500), ph('july'), 0.5)
mixin(fx, A.riser(1.0), ph('a million') - 1.0, 0.6); mixin(fx, A.boom(1.4, 85, 34), ph('a million'), 0.7)
for i in range(int((ph('now try eating') - T['perday']) / 0.5)):
    mixin(fx, A.tick(2600 if i % 2 == 0 else 2200, 0.8), T['perday'] + 0.3 + i * 0.5, 0.6)
mixin(fx, A.whoosh(0.5), T['what'] - 0.1, 0.6)
mixin(fx, A.chirp(), ph('something tickles') + 0.2, 0.5)
mixin(fx, A.zap(), ph('a nerve fires'), 0.6)
mixin(fx, A.pop(700, 300), ph('everybody out'), 0.8); mixin(fx, A.boing(0.5, 250, 600), ph('everybody out') + 0.3, 0.5)
mixin(fx, A.click(), ph('your eyes snap'), 0.8)
mixin(fx, A.whoosh(0.6, up=True), ph('you suck in'), 0.5)
mixin(fx, A.whoosh(0.5), T['speed'] - 0.1, 0.6)
mixin(fx, A.womp(), ph('yeah no'), 0.6)
mixin(fx, A.pop(1200, 600), ph('about sixteen'), 0.6)
mixin(fx, A.boing(0.6, 400, 150), ph('not a race car'), 0.6)
mixin(fx, A.shimmer(1.2), ph('little cloud'), 0.5)
mixin(fx, A.ding(1568), ph('cover it') + 0.2, 0.5)
mixin(fx, A.riser(1.0), T['hold'] - 0.9, 0.5); mixin(fx, A.thump(), T['hold'] + 0.1, 0.8)
mixin(fx, engine_hum(ph('that trapped') - ph('in two thousand')), ph('in two thousand'))
mixin(fx, A.pop(800, 300), ph('pinched his nose'), 0.6)
mixin(fx, hiss(ph('it tore') - T['tear']), T['tear'], 1.0)
mixin(fx, A.boom(1.2, 90, 40), ph('it tore'), 0.8); mixin(fx, A.pop(1500, 700), ph('it tore') + 0.05, 0.7)
mixin(fx, hiss(1.6, 1.4), ph('it tore') + 0.2)
mixin(fx, A.womp(), ph('one sneeze', after=ph('all to stop')), 0.5)
mixin(fx, A.riser(1.0), ph('more than twenty') - 0.9, 0.5); mixin(fx, A.thump(), ph('more than twenty'), 0.7)
mixin(fx, A.shimmer(1.4), ph('the good news'), 0.5); mixin(fx, A.ding(2093), ph('five weeks') + 0.2, 0.6)
mixin(fx, A.whoosh(0.5), T['facts'] - 0.1, 0.6)
for i in range(3): mixin(fx, A.pop(900 + i * 150, 450), T['facts'] + 0.2 + i * 0.25, 0.5)
mixin(fx, A.shimmer(1.0), ph('step into bright'), 0.5)
mixin(fx, A.pop(1200, 600), ph('photic'), 0.5)
mixin(fx, A.click(), ph('pluck') + 0.4, 0.8)
mixin(fx, snore(ph('wake up first') - ph('almost never'), 0.7), ph('almost never'))
mixin(fx, A.boing(0.5, 300, 700), ph('wake up first'), 0.6)
mixin(fx, A.whoosh(0.5), T['stop'] - 0.1, 0.6)
mixin(fx, A.pop(1000, 500), ph('september sixteenth'), 0.6)
for i in range(8): mixin(fx, A.tick(3000, 0.6), ph('nine hundred seventy six') - 0.6 + i * 0.18, 0.5)
mixin(fx, A.shimmer(1.6), ph('a whole day'), 0.6); mixin(fx, A.ding(1568), ph('a whole day') + 0.3, 0.5)
mixin(fx, A.riser(1.0), ph('she still holds') - 0.9, 0.5); mixin(fx, A.boom(1.4, 80, 32), ph('she still holds'), 0.6)
mixin(fx, A.shimmer(1.4), ph('world record'), 0.6)
mixin(fx, A.whoosh(0.4), T['ask'] - 0.1, 0.6)
mixin(fx, A.pop(900, 450), ph('comments'), 0.5)
mixin(fx, A.riser(1.2), END, 0.6); mixin(fx, A.boom(1.4, 80, 32), END + 0.9, 0.6)

out = A.mixdown(RS.D, mus, fx, os.path.join(RS.D, 'vo48.wav'), music_lufs=-24.0)
print('mix ->', out)
