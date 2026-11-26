import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/docu'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
END = E[-1] + .35; TOTAL = END + 1.8
rs = np.random.RandomState(3)
def click():
    n = int(.03 * SR); a = rs.randn(n).astype(np.float32) * np.exp(-np.linspace(0, 9, n)).astype(np.float32)
    a = np.convolve(a, [1, -.9], 'same'); return a * .9
def glitch_s():
    n = int(.18 * SR); a = (np.sign(np.sin(np.linspace(0, 2 * np.pi * 900 * .18, n))) * .3 + rs.randn(n) * .25).astype(np.float32)
    a = np.round(a * 4) / 4; a *= np.exp(-np.linspace(0, 4, n)).astype(np.float32); return a
SYN = {'CLK': click, 'GL': glitch_s}
def typing(t0, s, cps): return [(t0 + k / cps, 'CLK', .5) for k, ch in enumerate(s) if ch != ' ']
W_ = wfind
EV = ([(0.0, '1143', .5), (0.05, '788', .3), (S[1] - .06, '2627', .45), (W_(1, 'service'), '2364', .35), (W_(1, 'history'), '2364', .35),
 (S[2] - .06, '1461', .45), (W_(2, 'hot') - .06, 'GL', .45), (W_(2, 'pine'), '1494', .5), (S[3] - .06, '2627', .45), (W_(3, 'pollen'), '788', .45),
 (S[4] - .06, '1461', .45)] + [(S[4] + .1 + k * .22, '2364', .3) for k in range(4)] + [(W_(4, 'where'), '2357', .3),
 (S[5] - .02, 'GL', .5)] + typing(S[5] - .05, '2,200 years later...', 16) + [(S[6] - .02, '1143', .35), (W_(6, 'ten'), '1494', .4), (W_(6, 'four'), '1494', .4),
 (S[7] - .06, '2627', .45), (W_(7, 'some from') - .06, '1461', .45), (S[8] - .02, 'GL', .45), (W_(8, 'different'), '1494', .5),
 (S[9] - .06, '1461', .45)] + typing(W_(9, 'friend') - .25, 'tag the friend who', 30) + typing(W_(9, 'never'), 'never services their car.', 30) +
 [(S[10] - .06, '2627', .45), (W_(10, 'did'), '788', .5), (END, '1143', .4)] + typing(END + .2, 'send this to someone', 30))
N = int((TOTAL + .5) * SR); fx = np.zeros(N, np.float32)
for t, i, g in EV:
    a = SYN[i]() if i in SYN else snd(i)[:int(2.2 * SR)].copy(); n = min(len(a), N - int(t * SR)); fo = int(.15 * SR)
    if len(a) > fo: a[-fo:] *= np.linspace(1, 0, fo)
    fx[int(t * SR):int(t * SR) + n] += a[:n] * g * .55
vo = sf.read(D + '/vo.wav', dtype='float32')[0]
if vo.ndim > 1: vo = vo.mean(1)
v = np.zeros(N, np.float32); v[:len(vo)] = vo[:N]
env = np.convolve(np.abs(v), np.ones(2400) / 2400, 'same'); duck = 1 - .45 * np.clip(env / (env.max() * .25), 0, 1)
mix = v + fx * duck; sf.write('/tmp/mix_pre.wav', np.stack([mix, mix], 1), SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/mix_pre.wav', '-af', 'alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', D + '/mix.wav'], check=True); print('ok', len(EV))
