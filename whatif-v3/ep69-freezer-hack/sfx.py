import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/freeze'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.05, '3005', .5), (.3, '2409', .35), (S[1] - .1, '1461', .5), (S[1] + .4, '2357', .4), (S[2] - .1, '2627', .45), (S[3] - .2, '645', .35), (S[3] + .2, '788', .55), (S[3] + .4, '2364', .45),
 (S[4], '2354', .4), (S[5] - .1, '1471', .45), (wfind(5, 'broke'), '2358', .4), (wfind(5, 'cut'), '2358', .4), (S[6] - .1, '2627', .45), (S[6] + .3, '1133', .4),
 (S[7], '1092', .5), (S[7] + .3, '1143', .5), (S[8] - .1, '1471', .45), (wfind(8, 'seven'), '2068', .35)] + [(wfind(8, 'seven') - .2 + k * .2, '2354', .2) for k in range(8)] + [
 (S[9] - .1, '2627', .45), (wfind(9, 'meat') + .7, '1989', .45), (wfind(9, 'ice') + .7, '1989', .45), (wfind(9, 'milk') + .7, '1989', .45), (wfind(9, 'fifteen'), '788', .5),
 (S[10] - .1, '1177', .25), (S[11] + .2, '1143', .5)] + [(S[11] + .2 + k * .25, '2354', .2) for k in range(10)] + [(wfind(11, 'overnight'), '2364', .45),
 (S[12] - .1, '1461', .45), (S[12] + .6, '2357', .45), (S[13] - .1, '790', .45), (S[13] + .1, '2364', .45), (S[14] - .1, '1471', .45), (wfind(14, 'wide open'), '1133', .5),
 (S[15] - .1, '2627', .45), (wfind(15, 'warehouses'), '3005', .4), (wfind(15, 'medicine'), '3005', .4), (wfind(15, 'delivery'), '1538', .35),
 (S[16] - .1, '1461', .45), (S[16] + .4, '2354', .35), (S[17], '1143', .5), (S[17] + .3, '1202', .35), (S[18] - .1, '2627', .45), (S[19], '2364', .45), (S[19] + .15, '2364', .45), (END, '1471', .5), (END + .3, '2068', .45)]
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
