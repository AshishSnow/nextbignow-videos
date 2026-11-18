"""Sahara SFX v3: real recordings from Mixkit (free license, commercial OK, no attribution). Voice stays on top; no music."""
import json, subprocess, numpy as np, soundfile as sf, scipy.signal as sg
D = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/whatif/sahara/full/'
MK = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/sfxlib/mixkit/mk_%s.mp3'
T = json.load(open(D + 'times.json')); S = [t[0] for t in T]
v, SR = sf.read(D + 'mix.wav'); dur = len(v) / SR + 1.8; N = int(dur * SR)
vo = np.zeros((N, 2)); vo[:len(v)] = v
fx = np.zeros((N, 2)); CACHE = {}


def load(i):
    if i not in CACHE:
        a = subprocess.run(['ffmpeg', '-v', 'error', '-i', MK % i, '-ar', str(SR), '-ac', '2', '-f', 'f32le', '-'], capture_output=True).stdout
        a = np.frombuffer(a, np.float32).reshape(-1, 2).astype(np.float64)
        CACHE[i] = a / (np.sqrt(np.mean(a ** 2)) + 1e-9)            # unit RMS, gains below are relative to that
    return CACHE[i]


def put(i, t0, db, src=0.0, length=None, fi=0.05, fo=0.3, hp=None, lp=None):
    a = load(i)[int(src * SR):]
    if length: a = a[:int(length * SR)]
    a = a.copy(); n = len(a)
    if hp: a = sg.sosfilt(sg.butter(2, hp, 'high', fs=SR, output='sos'), a, axis=0)
    if lp: a = sg.sosfilt(sg.butter(2, lp, 'low', fs=SR, output='sos'), a, axis=0)
    e = np.ones(n); k = int(fi * SR); e[:k] = np.linspace(0, 1, k) if k else 1
    k = int(fo * SR); e[n - k:] *= np.linspace(1, 0, k) if k else 1
    i0 = int(t0 * SR); m = min(n, N - i0)
    if m > 0: fx[i0:i0 + m] += a[:m] * e[:m, None] * 10 ** (db / 20)


VR = np.sqrt(np.mean(v[np.abs(v).max(1) > .02] ** 2))          # voice RMS
B = 20 * np.log10(VR)                                           # 0 dB here = as loud as the voice
# --- beds ---
put(2495, 0.0, B - 18, 0, S[3] - .4, fi=.8, fo=1.0)              # desert ambience (dusk + night)
put(540, 0.2, B - 17, 2, 5.4, fi=.4, fo=.8, lp=6000)              # runner footsteps on crust
put(2490, S[2] - .3, B - 21, 0, S[3] - S[2], fi=1.0, fo=1.0)      # night wind, empty world
# --- bats across the sun ---
put(63, S[1] + .35, B - 13); put(2694, S[1] + .9, B - 16)
# --- sandstorm ---
put(2408, S[3] - 1.0, B - 10, fi=.3, fo=.6)                       # storm coming whoosh
put(2407, S[3] - .2, B - 11, 0, S[4] - S[3] + 1.4, fi=.8, fo=1.6) # strong wild wind
put(2409, S[3] + .5, B - 12, fi=.1, fo=1.2, lp=900)               # rumble as it hits
put(1143, S[3] + .8, B - 12, fo=1.0)                              # deep impact at the hit
put(2490, S[4] - .2, B - 20, 0, S[5] - S[4] + .2, fi=1.0, fo=.8)  # storm clears, eerie calm
# --- shrine at noon ---
put(2495, S[5] - .3, B - 22, 20, S[6] - S[5], fi=.6, fo=.6)
put(540, S[5] - .2, B - 21, 9, 2.2, fi=.3, fo=.6, lp=6000)
# --- inside the dome: bats in the roof ---
put(2492, S[6] - .5, B - 18, 0, S[8] - S[6] + .3, fi=.5, fo=.6)    # cavern room tone
put(2703, S[6] + .2, B - 15); put(63, S[6] + 1.2, B - 17)
put(494, S[7] - .2, B - 20, 3, S[8] - S[7] + .2, fi=.4, fo=.5)    # slow heartbeat under "Raw."
# --- SOS in the sand ---
put(2495, S[8] - .3, B - 22, 35, S[10] - S[8] + .3, fi=.6, fo=.8)
for k, dt in enumerate([.35, .85, 1.35]): put(1494, S[8] + dt, B - 13 - k)
put(2494, S[8] + .2, B - 19, 0, 2.4, fo=.8)
put(1579, S[9] - 1.6, B - 11, 0, None, fi=.5, fo=1.5)            # low airplane flying over
# --- day 9: goats, girl ---
put(1758, S[10] - .3, B - 18, 2, S[11] - S[10] + .3, fi=.8, fo=.8)
put(1760, S[10] + 1.0, B - 15); put(319, S[10] + 2.3, B - 17)
# --- map ---
put(1177, S[11] - .2, B - 17, 5, S[13] - S[11], fi=.8, fo=.8)      # deep low hum under the map
# --- reruns + ending ---
put(540, S[13] - .1, B - 19, 4, S[14] - S[13], fi=.3, fo=.8, lp=6000)
put(2490, S[14] - .3, B - 20, 0, dur - S[14] + .3, fi=.8, fo=1.6)
# --- transitions ---
for t, i in [(S[2], 1461), (S[5] - .3, 1167), (S[6] - .4, 2604), (S[8], 1471), (S[10], 1461), (S[11], 1471), (S[13], 1167), (S[14], 2604)]:
    put(i, t - .45, B - 15, fo=.4)
# --- duck beds a touch under speech (sidechain-style) ---
env = np.convolve(np.abs(vo).max(1), np.ones(int(.08 * SR)) / int(.08 * SR), 'same')
duck = 1 - .35 * np.clip(env / (env.max() * .25), 0, 1)
out = vo + fx * duck[:, None]
out *= .97 / np.abs(out).max()
sf.write(D + 'mix_fx3.wav', out, SR)
print('ok', round(dur, 1), 'voice dBFS %.1f' % B)
