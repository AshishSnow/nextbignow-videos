"""ep67 SFX: real Mixkit recordings (free license, no attribution). Voice on top, beds ducked, no music."""
import json, re, subprocess, numpy as np, soundfile as sf, scipy.signal as sg
D = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/whatif/gta6/full/'
MK = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/sfxlib/mixkit/mk_%s.mp3'
T = json.load(open(D + 'times.json')); S = [t[0] for t in T]; E = [t[1] for t in T]
AL = [[re.sub(r'\(\d\)', '', w), a, b] for w, a, b in json.load(open(D + 'align.json')) if w not in ('<s>', '</s>', '<sil>')]
v, SR = sf.read(D + 'mix.wav'); dur = E[-1] + 1.8; N = int(dur * SR)
vo = np.zeros((N, 2)); vo[:min(len(v), N)] = v[:N]
fx = np.zeros((N, 2)); bed = np.zeros((N, 2)); CACHE = {}


def wat(word, li, after=0.0):
    for w, a, b in AL:
        if S[li] - .1 <= a <= E[li] + .1 and w.lower().startswith(word): return a + after
    return S[li] + after


def load(i):
    if i not in CACHE:
        a = subprocess.run(['ffmpeg', '-v', 'error', '-i', MK % i, '-ar', str(SR), '-ac', '2', '-f', 'f32le', '-'], capture_output=True).stdout
        a = np.frombuffer(a, np.float32).reshape(-1, 2).astype(np.float64); CACHE[i] = a / (np.sqrt(np.mean(a ** 2)) + 1e-9)
    return CACHE[i]


def put(i, t0, db, src=0.0, length=None, fi=0.02, fo=0.25, lp=None, hp=None, to=None):
    to = fx if to is None else to
    a = load(i)[int(src * SR):]
    if length: a = a[:int(length * SR)]
    a = a.copy(); n = len(a)
    if n == 0: return
    if hp: a = sg.sosfilt(sg.butter(2, hp, 'high', fs=SR, output='sos'), a, axis=0)
    if lp: a = sg.sosfilt(sg.butter(2, lp, 'low', fs=SR, output='sos'), a, axis=0)
    e = np.ones(n); k = min(n, int(fi * SR))
    if k: e[:k] = np.linspace(0, 1, k)
    k = min(n, int(fo * SR))
    if k: e[n - k:] *= np.linspace(1, 0, k)
    i0 = max(0, int(t0 * SR)); m = min(n, N - i0)
    if m > 0: to[i0:i0 + m] += a[:m] * e[:m, None] * 10 ** (db / 20)


VR = np.sqrt(np.mean(v[np.abs(v).max(1) > .02] ** 2)); B = 20 * np.log10(VR)
s1, s2, s3, s4, s5, s6, s7, s8, s9, s10 = S[2] - .2, S[3] - .2, S[4] - .25, S[5] - .2, S[6] - .25, S[7] - .25, S[8] - .25, S[10] - .2, S[11] - .25, S[12] - .25
# beds
put(1185, 0, B - 20, 0, s1 + .3, fi=.6, fo=.5, to=bed)                     # sea + gulls under the neon sunset
put(1196, s6, B - 22, 5, s7 - s6 + .3, fi=.4, fo=.4, to=bed)               # sea under roleplay
put(1196, s10, B - 21, 12, dur - s10, fi=.5, fo=1.2, to=bed)               # ending sunset
put(1206 if False else 1196, s9, B - 15, 20, s10 - s9 + .3, fi=.6, fo=.5, lp=5000, to=bed)  # the wave
# opening: title hit + cash
put(790, -.05, B - 14, fo=.2); put(1991, .3, B - 24, 3, 3.5, fi=.3, fo=1.0)
put(1989, wat('rich', 0) - .05, B - 9)                                     # money bag drop on RICH
put(2354, S[1] - .1, B - 12); put(1999, wat('tomorrow', 1), B - 13)        # calendar pop + coin on TOMORROW
# three phones pop in
for kw, i in (('streamers', 2357), ('youtubers', 2354), ('clip', 1133)): put(i, wat(kw, 2) - .3, B - 12)
# rewind to 2013
put(1088, s2 - .1, B - 11, 0, s3 - s2 + .2, fo=.4)
# $1B counter: coins rattle while counting, then jackpot
put(1991, wat('billion', 4) - .4, B - 19, 0, 1.6, fo=.5); put(1936, wat('billion', 4) + .5, B - 12)
for k in range(3): put(2364, wat('three', 4) + k * .18, B - 13)            # day cards
# stack of 230M copies: soft pops as cases land
for k in range(10): put(2358, s4 + .3 + k * .22, B - 20 - (k % 3))
put(2068, wat('copies', 5) - .1, B - 15)
# streaming: chat notification pings
for k in range(8): put([2354, 2357][k % 2], s5 + .6 + k * .33, B - 22)
put(462, wat('hours', 6) - .3, B - 22, 0, 2.2, fi=.3, fo=.8)               # crowd cheer on 2.1B hours
# roleplay: siren for cop, horn for taxi, coins for robber
put(1643, wat('cops', 7) - .1, B - 18); put(1993, wat('robbers', 7), B - 14); put(1565, wat('taxi', 7), B - 16); put(1538, wat('taxi', 7) + .4, B - 20)
# forecast bars grow + 4X stamp
put(645, s7 + .3, B - 20, 0, wat('copies', 8) - s7, fi=.4, fo=.3)
put(1989, S[9] - .05, B - 10); put(790, S[9] - .3, B - 18, fo=.2)
# viewers light up
for k in range(12): put([2357, 2354, 2358][k % 3], s8 + .2 + k * .16, B - 23)
# wave
put(2627, s9 - .3, B - 13)
put(1992, wat('wave', 11), B - 14)
# question pop
put(2357, s10 + .2, B - 14); put(2354, s10 + .55, B - 16)
# transitions
for t in (s1, s3, s4, s5, s6, s7, s8, s10): put(3005, t - .15, B - 17)
env = np.convolve(np.abs(vo).max(1), np.ones(int(.08 * SR)) / int(.08 * SR), 'same')
duck = 1 - .45 * np.clip(env / (env.max() * .25), 0, 1)
out = vo + fx * (1 - .2 * (1 - duck))[:, None] + bed * duck[:, None]
out *= .97 / np.abs(out).max()
sf.write(D + 'mix_fx_raw.wav', out, SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', D + 'mix_fx_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', '48000', D + 'mix_fx.wav'], check=True)
print('ok', round(dur, 1))
