import sys, subprocess, numpy as np, soundfile as sf
sys.argv = ['x']; exec(open('/home/claude/glasses/scenes.py').read().split("if __name__")[0].split("G = load_st")[0])
M = '/home/claude/nextbignow-videos/sfx-library/mixkit/mk_%s.mp3'; SR = 48000
def load(i):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', M % i, '-ac', '1', '-ar', str(SR), '/tmp/s.wav'], check=True)
    return sf.read('/tmp/s.wav', dtype='float32')[0]
C = {}
def snd(i):
    if i not in C: C[i] = load(i)
    return C[i]
tc = wfind(17, 'phone cases'); tr = wfind(17, 'screen'); ts = wfind(18, 'selfie'); t75 = wfind(7, 'seventy')
cam = wfind(8, 'camera'); ai = wfind(8, 'google'); bat = wfind(8, 'nine')
EV = [(0.05, '3005', .5), (S[1] + .05, '2627', .55), (S[1] + .33, '1143', .6), (S[1] + .45, '2364', .45),
 (S[2] - .1, '1461', .5), (S[2] + .6, '2354', .4), (S[2] + 1.0, '2354', .4), (S[2] + 1.4, '2357', .4),
 (S[3] - .1, '2627', .5), (wfind(4, 'six'), '2358', .45), (wfind(5, 'twenty'), '2358', .5), (t75, '2358', .5), (t75 + .4, '788', .5),
 (t75 + .55, '2364', .4), (S[8] - .1, '1471', .5), (cam + .2, '1133', .55), (ai + .2, '2357', .4), (bat + .2, '2068', .4), (S[9], '2364', .45),
 (S[10] - .1, '1461', .45), (S[11] - .1, '2627', .45), (S[11] + .7, '3005', .45), (S[12] - .1, '1471', .45), (S[13], '2358', .45), (S[13] + .3, '2364', .45),
 (S[14] - .1, '2627', .45), (S[14] + .2, '2354', .4), (S[14] + .55, '2354', .4), (S[14] + .9, '2354', .4), (S[15], '2364', .45), (S[15] + .4, '1143', .4),
 (S[16] - .1, '2604', .5), (tc - .1, '3005', .4), (tc + .5, '1143', .45), (tr - .1, '3005', .4), (tr + .5, '1143', .45), (ts - .1, '3005', .4), (ts + .7, '788', .45),
 (S[19] - .1, '1461', .45), (S[20] - .1, '2364', .4), (wfind(20, 'millions'), '1992', .45), (wfind(20, 'normal'), '2357', .4),
 (S[21] - .1, '2627', .5), (S[21] + .2, '2364', .45), (S[22], '2354', .45), (END, '1471', .5), (END + .3, '2068', .45)]
N = int((TOTAL + .5) * SR); fx = np.zeros(N, np.float32)
for t, i, g in EV:
    a = snd(i)[:int(2.2 * SR)].copy(); n = min(len(a), N - int(t * SR)); fo = int(.15 * SR)
    if len(a) > fo: a[-fo:] *= np.linspace(1, 0, fo)
    fx[int(t * SR):int(t * SR) + n] += a[:n] * g * .55
vo = sf.read('/home/claude/glasses/vo.wav', dtype='float32')[0]
if vo.ndim > 1: vo = vo.mean(1)
v = np.zeros(N, np.float32); v[:len(vo)] = vo[:N]
env = np.convolve(np.abs(v), np.ones(2400) / 2400, 'same'); duck = 1 - .45 * np.clip(env / (env.max() * .25), 0, 1)
mix = v + fx * duck
sf.write('/tmp/mix_pre.wav', np.stack([mix, mix], 1), SR, subtype='FLOAT')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/mix_pre.wav', '-af', 'alimiter=limit=0.89,loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '/home/claude/glasses/mix.wav'], check=True)
print('ok', len(EV))
