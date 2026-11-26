"""Synthesised suspense score (royalty-free, made here): drone + heartbeat/tick pulse + risers + sub hits + silence drop.
Cues come from the voice-line timings so the music follows the story."""
import json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
D = '/home/claude/docu'; SR = 48000
L = json.load(open(D + '/lines.json')); S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
END = E[-1] + .35; TOTAL = END + 1.8; N = int((TOTAL + .5) * SR); t = np.arange(N) / SR
def wfind(i, w): tx = L[i]['text'].lower(); return S[i] + L[i]['dur'] * tx.find(w.lower()) / len(tx)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def env(a, b, fade=.4):
    e = np.clip((t - a) / fade, 0, 1) * np.clip((b - t) / fade, 0, 1); return e
rs = np.random.RandomState(1); out = np.zeros(N)

# 1) drone: D minor (D2 + A2 + F3), detuned saws, low-passed; filter opens as the story escalates
def saw(f): return 2 * ((t * f) % 1) - 1
dr = sum(saw(f * d) for f in (73.42, 110.0, 174.6) for d in (.997, 1.0, 1.004)) / 9
dr_lo = lp(dr, 380); dr_hi = lp(dr, 1100)
open_amt = np.clip((t - S[6]) / (S[9] - S[6]), 0, 1)               # brighter from the time jump on
drone = (dr_lo * (1 - open_amt) + dr_hi * open_amt) * (.55 + .15 * np.sin(2 * np.pi * .18 * t))
air = hp(lp(rs.randn(N), 2500), 600) * .06
out += (drone * .32 + air) * env(0, END + .2, .8)

# 2) heartbeat pulse during the mechanism (tar -> pollen -> fingerprint), ~72 bpm
def thump(at, g=1.0):
    n = int(.25 * SR); k = np.arange(n) / SR; s = np.sin(2 * np.pi * (60 - 25 * k / .25) * k) * np.exp(-k * 18)
    i = int(at * SR); out[i:i + n] += s[:max(0, min(n, N - i))] * g
bt = 60 / 72
x = S[2]
while x < S[6] - .2: thump(x, .9); thump(x + .22, .55); x += bt
# 3) clock tick during evidence (samples, coats, Italy/Croatia), 120 bpm, gets denser
def tick(at, g=.35):
    n = int(.02 * SR); s = hp(rs.randn(n), 3000) * np.exp(-np.arange(n) / SR * 300); i = int(at * SR); out[i:i + n] += s[:max(0, min(n, N - i))] * g
x = S[6]
while x < S[9] - .1: tick(x); x += .5 if x < S[8] else .25
# 4) risers into the big reveals
def riser(at, dur=1.2, g=.5):
    a = int((at - dur) * SR); n = int(dur * SR); k = np.arange(n) / SR
    nz = hp(rs.randn(n), 800) * (k / dur) ** 2; tone = np.sin(2 * np.pi * (200 + 900 * (k / dur) ** 2) * k) * (k / dur) ** 3 * .3
    seg = (nz * .5 + tone) * g; out[a:a + n] += seg[:max(0, min(n, N - a))]
for at in (wfind(2, 'glued'), wfind(4, 'pollen'), S[6], wfind(9, 'different'), wfind(11, 'did')): riser(at, 1.1, .45)
# 5) sub hits (boom) on key words
def hit(at, g=1.0):
    n = int(1.4 * SR); k = np.arange(n) / SR; s = np.sin(2 * np.pi * (55 * np.exp(-k * 3) + 30) * k) * np.exp(-k * 3.5)
    s += lp(rs.randn(n), 900) * np.exp(-k * 14) * .5; i = int(at * SR); out[i:i + n] += s[:max(0, min(n, N - i))] * g
for at in (0.0, wfind(2, 'glued'), wfind(4, 'pollen'), S[6], wfind(9, 'different'), wfind(11, 'did')): hit(at, .9)
# 6) the drop: silence the bed for 0.45 s right before the payoff word, then hit
d = wfind(11, 'did'); gate = 1 - np.clip(1 - np.abs(t - (d - .22)) / .25, 0, 1)
out *= np.where(t < d, gate, 1)
# 7) tail ring-out on the end card
out += np.sin(2 * np.pi * 146.8 * t) * np.exp(-np.clip(t - END, 0, None) * 1.5) * (t > END) * .15
out = out / (np.abs(out).max() + 1e-9) * .9
sf.write(D + '/music.wav', out.astype(np.float32), SR); print('music ok', round(TOTAL, 1))
