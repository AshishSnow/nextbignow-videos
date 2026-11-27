"""Story score for the GTA reel, synthesised (royalty-free): every section has a job.
hook: neon synth pad + plucked motif | reveal: riser + boom | 1997: tape-rewind into a lo-fi beat
scandals: full trap beat (808, clap, hats -> 1/16 rolls) | 'kept selling': DEAD SILENCE, then boom
court/preorder: beat back, brighter | ending: motif alone, silence before the last line, final hit + ring."""
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = '/home/claude/cash'; SR = 48000
L = json.load(open(D + '/lines.json')); S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + .35; TOTAL = END + 2.6; N = int((TOTAL + .5) * SR); t = np.arange(N) / SR
def wfind(i, w): tx = L[i]['text'].lower(); return S[i] + L[i]['dur'] * tx.find(w.lower()) / len(tx)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
rs = np.random.RandomState(4); out = np.zeros(N)
def add(at, sig, g=1.0):
    i = int(at * SR)
    if i >= N or i + len(sig) <= 0: return
    a = max(0, -i); n = min(len(sig) - a, N - i - a); out[i + a:i + a + n] += sig[a:a + n] * g
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
BPM = 96; B = 60 / BPM

# --- instruments
def pluck(f, dur=.6):                                 # Karplus-Strong pluck (synth-guitar/marimba feel)
    n = int(dur * SR); p = int(SR / f); buf = rs.uniform(-1, 1, p); o = np.zeros(n)
    for i in range(n):
        o[i] = buf[i % p]; buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    return lp(o, 4000) * np.exp(-np.arange(n) / SR * 2.5)
def kick808(f0=55, dur=.7):
    k = np.arange(int(dur * SR)) / SR; f = f0 + 90 * np.exp(-k * 30)
    return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-k * 3.2))
def clap():
    n = int(.25 * SR); k = np.arange(n) / SR; nz = hp(lp(rs.randn(n), 6000), 900)
    env = sum(np.exp(-np.clip(k - d, 0, None) * 60) * (k >= d) for d in (0, .012, .024)) * .5 + np.exp(-k * 18) * .6
    return nz * env
def hat(o=False):
    n = int((.18 if o else .05) * SR); return hp(rs.randn(n), 7000) * np.exp(-np.arange(n) / SR * (18 if o else 90))
def boom():
    k = np.arange(int(1.6 * SR)) / SR; s = np.sin(2 * np.pi * (48 * np.exp(-k * 2.5) + 28) * k) * np.exp(-k * 3)
    return s + lp(rs.randn(len(k)), 700) * np.exp(-k * 12) * .5
def riser(dur=1.2):
    n = int(dur * SR); k = np.arange(n) / SR; u = k / dur
    return hp(rs.randn(n), 900) * u ** 2 * .6 + np.sin(2 * np.pi * np.cumsum(220 + 1400 * u ** 2) / SR) * u ** 3 * .35
def pad(t0, t1, notes, g=.12, cutoff=1400):
    seg = t[int(t0 * SR):int(t1 * SR)] - t0
    if len(seg) == 0: return
    s = sum(np.sign(np.sin(2 * np.pi * mtof(m) * d * seg)) * .5 + np.sin(2 * np.pi * mtof(m) * seg) for m in notes for d in (.996, 1.004))
    s = lp(s, cutoff) / (len(notes) * 2); fade = np.clip(seg / .5, 0, 1) * np.clip((t1 - t0 - seg) / .5, 0, 1)
    add(t0, s * fade, g)

MOTIF = [69, 72, 76, 74, 72, 67]                         # A minor neon hook: A C E D C G
def motif(t0, t1, g=.35, step=B / 2):
    x = t0; k = 0
    while x < t1:
        add(x, pluck(mtof(MOTIF[k % len(MOTIF)])), g); x += step * (2 if k % len(MOTIF) == len(MOTIF) - 1 else 1); k += 1
def beat(t0, t1, g=1.0, rolls=False, sparse=False):
    x = t0; bar = 0
    while x < t1:
        for s16 in range(16):
            tt = x + s16 * B / 4
            if tt >= t1: break
            if s16 in (0, 10) or (not sparse and s16 == 7): add(tt, kick808(), .55 * g)
            if s16 in (4, 12) and not sparse: add(tt, clap(), .35 * g)
            if s16 % 2 == 0 or (rolls and s16 >= 12): add(tt, hat(s16 == 14), .12 * g)
        x += 4 * B; bar += 1

# --- v2 arrangement: punch reward early -> doubt -> warm Alaska -> answer -> lift-off
MOTIF[:] = [72, 76, 79, 77, 76, 72]
pad(0, S[3], [48, 55, 60, 64], .10, 1800); motif(0.1, S[3] - .3, .24, B / 2)
add(0.0, boom(), .6); beat(S[1], S[3] - .2, .6); add(wfind(1, 'to forty'), boom(), .9)
pad(S[3], S[4], [45, 52, 57, 60], .09, 900)
pad(S[4], S[6], [41, 48, 57, 60], .09, 1600); motif(S[4], S[6] - .3, .2, B); beat(S[5], S[6] - .3, .5, sparse=True)
add(wfind(6, 'jobs'), boom(), 1.0)
pad(S[6], END + 1.5, [48, 55, 60, 64], .1, 2400); beat(S[6] + .3, S[8] - .3, .75); motif(S[7], S[8] - .3, .22, B / 2)
add(wfind(8, "it's what"), boom(), 1.0); motif(wfind(8, "it's what"), END, .3, B / 2)
add(END, pluck(mtof(60), 2.2), .5)
for t0, t1 in ((S[3] - .3, S[3]), (wfind(6, 'jobs') - .35, wfind(6, 'jobs')), (wfind(8, "it's what") - .4, wfind(8, "it's what"))):
    a, b = int(t0 * SR), int(t1 * SR); out[a:b] *= np.linspace(1, 0, b - a) ** 3
a, b = int((S[3]) * SR), int((S[4] - .05) * SR); out[a:b] *= .15
out = out / (np.abs(out).max() + 1e-9) * .9
sf.write(D + '/music.wav', out.astype(np.float32), SR); print('music ok', round(TOTAL, 1))
