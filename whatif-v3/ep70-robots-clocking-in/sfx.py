import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/robots'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.05, '3005', .5), (.2, '2627', .45), (2.3, '1143', .5), (2.35, '2364', .45), (S[1] - .1, '1461', .45), (S[1] + .1, '2357', .35), (S[1] + .4, '2357', .35), (S[1] + .6, '2364', .4),
 (S[2] - .1, '2627', .45)] + [(S[2] + k * .2, '2354', .25) for k in range(7)] + [(S[3] - .1, '1471', .45), (S[3] + .3, '2358', .4),
 (S[4] - .1, '2627', .45)] + [(S[4] + .3 + k * .28, '3005', .2) for k in range(14)] + [(wfind(4, 'hundred thousand'), '1143', .5), (wfind(4, 'hundred thousand') + .1, '2068', .35),
 (S[5] - .1, '1461', .45), (wfind(5, 'nine'), '2358', .45), (wfind(6, 'five'), '2358', .5), (wfind(6, 'five') + .3, '2364', .4),
 (S[7] - .1, '1471', .45), (wfind(7, 'million'), '788', .5), (wfind(7, 'million') + .1, '2364', .45), (S[8] - .05, '790', .45),
 (S[9] - .1, '2627', .45), (wfind(10, 'breaks'), '2354', .4), (wfind(10, 'sick'), '2354', .4), (S[11], '1143', .5), (S[11] + .1, '2357', .4),
 (S[12] - .1, '1461', .45), (wfind(12, 'thirty'), '1992', .45), (wfind(12, 'thirty') + .2, '2364', .4), (S[13] - .05, '790', .45),
 (S[14] - .1, '2627', .45), (wfind(14, 'lifting') + .35, '1143', .4), (wfind(14, 'sorting') + .35, '1143', .4), (wfind(14, 'carrying') + .35, '1143', .4),
 (S[15] - .1, '1471', .45), (wfind(15, 'fix'), '3005', .35), (wfind(15, 'train'), '3005', .35), (wfind(15, 'run'), '3005', .35), (S[16], '2068', .45),
 (S[17] - .1, '2627', .45), (S[18], '2364', .45), (S[18] + .15, '2364', .45), (END, '1471', .5), (END + .3, '2068', .45)]
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
