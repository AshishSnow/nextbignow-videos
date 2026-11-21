import sys, subprocess, numpy as np, soundfile as sf, json
D = '/home/claude/altar'; L = json.load(open(D + '/lines.json'))
S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]; END = E[-1] + .3; TOTAL = END + 2.6
def wt(i, f): return S[i] + L[i]['dur'] * f
def wfind(i, w): tx = L[i]['text'].lower(); return wt(i, tx.find(w.lower()) / len(tx))
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000; C = {}
def snd(i):
    if i not in C:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True); C[i] = sf.read('/tmp/s.wav', dtype='float32')[0]
    return C[i]
EV = [(0.05, '1202', .45), (.3, '1133', .35), (.45, '2364', .4), (wfind(0, 'again'), '788', .45), (S[1] - .1, '2627', .45), (wfind(1, 'no.'), '1143', .55),
 (S[2] - .1, '1461', .45), (wfind(2, 'six'), '2357', .4), (wfind(2, 'sixteen'), '2357', .4), (wfind(2, 'center'), '2354', .35),
 (S[3] - .1, '2627', .45), (wfind(3, 'over'), '790', .4), (S[4] - .1, '1471', .4)] + [(S[4] + .3 + k * .7, '1494', .35) for k in range(4)] + [
 (S[5] - .1, '1461', .45), (wfind(5, 'twist'), '788', .5), (wfind(5, 'seventy'), '2357', .4)] + [(S[5] + 2.3 + k * .18, '2354', .14) for k in range(10)] + [
 (S[6] - .1, '2627', .45), (wfind(6, 'grains'), '2358', .4), (wfind(6, 'minerals'), '2358', .4), (wfind(6, 'chemistry'), '2358', .4),
 (S[7] - .05, '1143', .55)] + [(S[7] + .1 + k * .12, '2364', .12) for k in range(8)] + [(wfind(7, 'not one'), '788', .45),
 (S[8] - .1, '1471', .45), (wfind(8, 'no home'), '2068', .4), (S[9] - .05, '790', .45), (S[10] - .1, '2627', .45),
 (wfind(10, 'england'), '1133', .4), (wfind(10, 'scotland'), '1133', .4), (wfind(10, 'ireland'), '1133', .4),
 (S[11] - .1, '1461', .45), (wfind(11, 'who'), '2357', .4), (wfind(11, 'how'), '788', .4),
 (S[12] - .1, '1202', .4), (S[13], '2364', .45), (S[13] + .15, '2364', .45), (END, '1471', .5), (END + .3, '2068', .45)]
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
