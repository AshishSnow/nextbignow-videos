import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/tort'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.05, '1202', .45), (.3, '1177', .3), (.4, '790', .35), (wfind(0, 'young') - .3, '788', .45),
 (S[1] - .1, '2627', .45), (S[1] + .3, '2604', .35), (S[2] - .1, '1461', .45), (S[2] + .2, '1133', .35), (wfind(2, 'hatched'), '2357', .35), (wfind(2, 'photo'), '1133', .45),
 (S[3] - .1, '2627', .45), (S[3] + .3, '2357', .35), (wfind(3, 'doubled'), '788', .45),
 (S[4] - .1, '1471', .4), (S[4] + .4, '1494', .3), (wfind(4, 'bacteria') - .3, '1143', .5),
 (S[5] - .1, '1461', .45), (wfind(5, 'two hundred'), '790', .45)] + [(wfind(5, 'two hundred') + k * .12, '2354', .12) for k in range(9)] + [
 (S[6] - .1, '2627', .45), (wfind(6, 'fix'), '2358', .4), (wfind(6, 'protect'), '2358', .4),
 (S[7] - .1, '1461', .45), (S[7] + .2, '2357', .3), (S[7] + .4, '2357', .3), (S[7] + .6, '2357', .3), (wfind(7, 'neat'), '788', .45),
 (S[8] - .1, '2627', .45), (wfind(8, 'nobody'), '2364', .4), (S[9] - .1, '1461', .45), (wfind(9, 'blood'), '2358', .45), (wfind(9, 'all of us'), '2604', .4),
 (S[10] - .1, '1202', .45), (S[10] + .2, '1133', .4), (END, '1471', .5)]
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
