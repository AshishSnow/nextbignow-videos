"""SFX bed for full Sahara video: air bed, bat flaps, storm wind + rumble, plane drone, soft whooshes at cuts. No music."""
import json, numpy as np, soundfile as sf, scipy.signal as sg
D = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/whatif/sahara/full/'
T = json.load(open(D + 'times.json'))
v, SR = sf.read(D + 'mix.wav'); N = len(v); dur = N / SR + 1.8
N2 = int(dur * SR); out = np.zeros((N2, 2)); out[:N] = v
rng = np.random.default_rng(7)
def bp(x, lo, hi): return sg.sosfilt(sg.butter(4, [lo, hi], 'band', fs=SR, output='sos'), x)
def env(t0, t1, a, fi=.6, fo=.8):
    e = np.zeros(N2); i0, i1 = int(t0 * SR), min(N2, int(t1 * SR))
    if i1 <= i0: return e
    n = i1 - i0; x = np.arange(n) / SR
    e[i0:i1] = a * np.clip(x / fi, 0, 1) * np.clip((n / SR - x) / fo, 0, 1); return e
noise = rng.standard_normal(N2)
LIB = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/sfxlib/'
WIND, _ = sf.read(LIB + 'wm_wind.wav'); THUN, _ = sf.read(LIB + 'wm_thunder.wav')   # real recordings, 48 kHz mono
def clip(src, start, t0, length):
    seg = np.zeros(N2); a = src[int(start * SR): int((start + length) * SR)]; i = int(t0 * SR); n = min(len(a), N2 - i)
    seg[i:i + n] = a[:n] / (np.sqrt(np.mean(a ** 2)) + 1e-9); return seg
fx = np.zeros(N2)
# soft desert air bed whole video
fx += bp(clip(WIND, 40, 0, dur), 120, 2500) * env(0, dur, .022, 1.0, 1.5)   # real desert-air bed
# bat flaps after line 1 ("bats")
for k in range(9):
    t = T[1][0] + .55 + k * .09 + rng.uniform(0, .03); i = int(t * SR); n = int(.05 * SR)
    fx[i:i + n] += bp(rng.standard_normal(n), 300, 1800) * np.hanning(n) * .05
# storm: wind swell from line 3 to line 4 + rumble at hit
hit, calm = T[3][0] + .9, T[4][0]
fx += bp(clip(WIND, 24, T[3][0] - .3, calm - T[3][0] + 1.4), 90, 6000) * env(T[3][0] - .3, calm + .8, .065, 1.0, 1.6)   # real howling storm wind
fx += sg.sosfilt(sg.butter(4, 220, 'low', fs=SR, output='sos'), clip(THUN, 1.0, hit - .4, calm - hit + .6)) * env(hit - .4, calm, .10, .3, 1.2)   # real thunder rumble (CC BY Bidgee)
# bats again inside shrine (line 6)
for k in range(7):
    t = T[6][0] + .2 + k * .11; i = int(t * SR); n = int(.05 * SR)
    fx[i:i + n] += bp(rng.standard_normal(n), 300, 1800) * np.hanning(n) * .035
# plane drone passing over (line 9)
t = np.arange(N2) / SR; drone = np.sin(2 * np.pi * 95 * t) + .5 * np.sin(2 * np.pi * 190 * t) + .3 * bp(noise, 80, 600)
fx += drone * env(T[9][0] - .3, T[9][1] + .6, .025, 1.2, 1.4)
# soft whooshes at shot cuts
for s in [T[2][0], T[5][0] - .3, T[8][0], T[10][0], T[11][0], T[13][0], T[14][0]]:
    fx += bp(noise, 600, 5000) * env(s - .35, s + .25, .03, .3, .25)
out[:, 0] += fx; out[:, 1] += fx
out *= .97 / np.abs(out).max()
sf.write(D + 'mix_fx2.wav', out, SR); print('ok', round(dur, 1))
