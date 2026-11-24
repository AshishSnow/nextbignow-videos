import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/voyager'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.05, '1202', .45), (.3, '2604', .35), (wfind(0, 'tomorrow'), '1143', .5), (S[1] - .05, '2627', .4), (wfind(1, 'light'), '2357', .35),
 (S[2] - .1, '1461', .4), (wfind(2, 'never'), '788', .4), (S[3] - .1, '1461', .4), (S[3] + .2, '788', .4), (wfind(3, 'sixteen'), '2357', .35),
 (S[4] - .1, '1461', .4), (wfind(4, 'twenty'), '1143', .5), (S[5] - .05, '2627', .4), (wfind(5, 'two'), '2357', .35), (S[6] - .1, '1461', .4),
 (wfind(6, 'watts'), '788', .4), (S[7] - .1, '1461', .4), (wfind(7, 'no data'), '1143', .45), (S[8] - .05, '2627', .4), (wfind(8, 'silent'), '2357', .3),
 (S[9] - .1, '1202', .4), (wfind(9, 'tomorrow'), '788', .45), (END, '1471', .5)]
N = int((TOTAL + .5) * SR); fx = np.zeros(N, np.float32)
for t, i, g in EV:
    a = snd(i)[:int(2.2 * SR)].copy(); n = min(len(a), N - int(t * SR)); fo = int(.15 * SR)
    if len(a) > fo: a[-fo:] *= np.linspace(1, 0, fo)
    fx[int(t * SR):int(t * SR) + n] += a[:n] * g * .55
vo = sf.read(D + '/vo.wav', dtype='float32')[0]
if vo.ndim > 1: vo = vo.mean(1)
v = np.zeros(N, np.float32); v[:len(vo)] = vo[:N]
env = np.convolve(np.abs(v), np.ones(2400) / 2400, 'same'); duck = 1 - .45 * np.clip(env / (env.max() * .25), 0, 1)
mix = v + fx * duck; sf.write('/tmp/mix_pre.wav', np.stack([mix, mix], 1), SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/mix_pre.wav', '-af', 'alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', D + '/mix.wav'], check=True); print('ok', len(EV))
