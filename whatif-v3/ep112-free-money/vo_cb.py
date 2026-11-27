"""Chatterbox voice (natural prosody), timbre cloned from our male reference; per-line acting via exaggeration/cfg.
Each line is checked with Whisper and regenerated (new seed) if words are missing."""
import re, json, subprocess, numpy as np, soundfile as sf, torch, torchaudio as ta
src = open('/home/claude/cash/vo.py').read(); ns = {}
exec(src[src.index('L=['):src.index('SR=48000')], ns); L = ns['L']
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel
m = ChatterboxTTS.from_pretrained(device='cpu'); wh = WhisperModel('small.en', device='cpu', compute_type='int8')
ACT = {'hype': (.7, .4), 'punchline': (.55, .45), 'story': (.5, .5), 'tease': (.6, .45), 'reveal': (.75, .4), 'fast': (.55, .5), 'excited': (.8, .35)}
GAP = {'hype': .12, 'punchline': .2, 'story': .12, 'tease': .15, 'reveal': .14, 'fast': .08, 'excited': .1}
def norm(t): return re.sub(r'[^a-z ]', '', t.lower().replace('-', ' ')).split()
SR = 48000; parts = []; lines = []; t = 0.0
CHAIN = "highpass=f=80,lowpass=f=11000,equalizer=f=3000:t=q:w=1.5:g=1.5,deesser=i=0.4,acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120"
for i, (tag, text, extra) in enumerate(L):
    ex, cfg = ACT[tag]; best = None
    for seed in range(3):
        torch.manual_seed(100 + i * 7 + seed)
        w = m.generate(text, audio_prompt_path='/home/claude/cb/ref.wav', exaggeration=ex, cfg_weight=cfg)
        a = w.squeeze().numpy().astype(np.float32); sf.write('/tmp/cb.wav', a, m.sr)
        from scipy.signal import resample_poly; a16 = resample_poly(a, 16000, m.sr).astype(np.float32)
        hyp = ' '.join(s.text for s in wh.transcribe(a16, language='en')[0])
        want, got = norm(text), set(norm(hyp)); miss = [x for x in want if x not in got and len(x) > 3]
        score = len(miss); print(i, seed, 'miss', miss, flush=True)
        if best is None or score < best[0]: best = (score, a)
        if score == 0: break
    a = best[1]; idx = np.where(np.abs(a) > .01)[0]; a = a[max(0, idx[0] - 240):idx[-1] + 2400]
    sf.write('/tmp/cb.wav', a, m.sr)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/tmp/cb.wav', '-af', 'aresample=48000:resampler=soxr,' + CHAIN, '-ar', '48000', '-ac', '1', '/tmp/cb2.wav'], check=True)
    b = sf.read('/tmp/cb2.wav', dtype='float32')[0]; fo = int(.03 * SR); b[-fo:] *= np.linspace(1, 0, fo)
    lines.append(dict(i=i, tag=tag, text=text, start=round(t, 3), dur=round(len(b) / SR, 3)))
    pa = GAP[tag] + extra * .8; parts += [b, np.zeros(int(pa * SR), np.float32)]; t += len(b) / SR + pa
sf.write('/home/claude/cash/vo_raw.wav', np.concatenate(parts), SR)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', '/home/claude/cash/vo_raw.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9', '-ar', '48000', '/home/claude/cash/vo.wav'], check=True)
json.dump(lines, open('/home/claude/cash/lines.json', 'w'), indent=1); print('dur', round(t, 2))
