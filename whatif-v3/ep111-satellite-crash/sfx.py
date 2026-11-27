import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/sat'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.2, '1461', .3), (wfind(0, 'right over'), '788', .6), (S[1] - .05, '1461', .3), (wfind(1, 'ten times'), '2627', .35),
 (S[2] - .05, '1461', .3), (S[3] - .05, '1461', .3), (wfind(3, 'and a dead'), '2627', .3), (S[4] + .15, '788', .65),
 (S[5] - .05, '1471', .25), (wfind(6, 'had to hide'), '1643', .2), (S[7] - .05, '1471', .3),
 (S[8] - .05, '1461', .3), (wfind(8, 'like a highway'), '1538', .3), (S[9] - .05, '1461', .3), (S[10] - .05, '1461', .3),
 (wfind(10, 'under three'), '2364', .45), (S[11] - .05, '1461', .3), (S[11] + .3, '788', .3), (S[11] + 1.1, '788', .3),
 (S[12] - .05, '1461', .3), (wfind(13, 'every single') + .6, '788', .55), (END, '1471', .35)]
N = int((TOTAL + .5) * SR); fx = np.zeros(N, np.float32)
for t, i, g in EV:
    a = snd(i)[:int(2.2 * SR)].copy(); n = min(len(a), N - int(t * SR)); fo = int(.15 * SR)
    if len(a) > fo: a[-fo:] *= np.linspace(1, 0, fo)
    fx[int(t * SR):int(t * SR) + n] += a[:n] * g * .55
vo = sf.read(D + '/vo.wav', dtype='float32')[0]
if vo.ndim > 1: vo = vo.mean(1)
v = np.zeros(N, np.float32); v[:len(vo)] = vo[:N]
env = np.convolve(np.abs(v), np.ones(2400) / 2400, 'same'); duck = 1 - .45 * np.clip(env / (env.max() * .25), 0, 1)
mu = np.zeros(N, np.float32); m_ = sf.read(D + '/music.wav', dtype='float32')[0][:N]; mu[:len(m_)] = m_
duck2 = 1 - .5 * np.clip(env / (env.max() * .25), 0, 1)
mix = v + fx * duck + mu * .5 * duck2; sf.write('/tmp/mix_pre.wav', np.stack([mix, mix], 1), SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/mix_pre.wav', '-af', 'alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', D + '/mix.wav'], check=True); print('ok', len(EV))
