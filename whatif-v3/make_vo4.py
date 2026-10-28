"""VO v4 (voice C, slower + expressive): python make_vo4.py <dir> [--tempo 0.9] [--seed 11] [--reuse]
paras.txt: one paragraph per line. Inside, sentences may start with Chatterbox Turbo style tags, e.g.
  [surprised] He was inside a whale's mouth!   [whispering] And in there... it's dark.   [chuckle] ...
'...' = dramatic beat. Each sentence/beat is generated separately (so tags apply per sentence),
time-stretched with Rubber Band (tempo<1 = slower, pitch kept), joined with research-based pauses.
Long chunks spoken faster than 3.5 words/s are slowed to ~3.3 (even pacing).
Outputs: vo_raw.wav, vo48.wav, vo16.wav, script.txt (tags stripped), segments.json, chunks.json (per-chunk timing)."""
import sys, os, re, json, subprocess, argparse, glob
import numpy as np, soundfile as sf
from scipy import signal

ap = argparse.ArgumentParser(); ap.add_argument('D'); ap.add_argument('--tempo', type=float, default=0.9)
ap.add_argument('--seed', type=int, default=11); ap.add_argument('--reuse', action='store_true')
A = ap.parse_args(); D = os.path.abspath(A.D)
T2 = '/tmp/claude-0/-home-claude/239c7fbe-0e4b-5b82-aefc-aed1893525c4/scratchpad/tts2/'
REF = T2 + 'ref_voice.wav'
TAG = re.compile(r'\[[a-z ]+\]\s*')
raw = [l.strip() for l in open(os.path.join(D, 'paras.txt')) if l.strip()]
paras = []; breaks = set()
for l in raw:
    if l == '---': breaks.add(len(paras) - 1)
    else: paras.append(l)

plan = []   # (para_idx, text_with_tags, pause_after, whisper)
for pi, p in enumerate(paras):
    sents = re.split(r'(?<=[.!?])\s+(?=[\[A-Z"\'])', p)
    for si, s in enumerate(sents):
        tag = TAG.match(s); tg = tag.group(0) if tag else ''
        body = s[len(tg):] if tg else s
        beats = [b.strip() for b in body.split('...') if b.strip()]
        for bi, b in enumerate(beats):
            lastb = bi == len(beats) - 1
            txt = (tg if bi == 0 else tg) + b + ('...' if not lastb else '')
            if not lastb: gap = 0.6
            elif b.endswith('?'): gap = 0.5
            elif b.endswith('!'): gap = 0.42
            else: gap = 0.4
            if lastb and si == len(sents) - 1: gap += (0.25 + (1.3 if pi in breaks else 0)) if pi < len(paras) - 1 else -gap
            plan.append((pi, txt, gap, 'whisper' in tg))
cd = os.path.join(D, 'vo_chunks')
if not A.reuse or not os.path.isdir(cd):
    if os.path.isdir(cd):
        for f in glob.glob(os.path.join(cd, '*.wav')): os.remove(f)
    json.dump([x[1] for x in plan], open(os.path.join(D, 'vo_chunks.json'), 'w'), indent=0)
    subprocess.run([T2 + 'cb/bin/python', T2 + 'cb_chunks.py', os.path.join(D, 'vo_chunks.json'), cd, REF, str(A.seed)], check=True)

sr = 24000
def load(f, tempo=None):
    tempo = A.tempo if tempo is None else tempo
    if tempo != 1.0:
        tmp = f.replace('.wav', '_t.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-af', 'rubberband=tempo=%.3f:pitchq=quality:window=standard:formant=preserved' % tempo, '-ar', str(sr), tmp], check=True)
        f = tmp
    a, s_ = sf.read(f, dtype='float64')
    if a.ndim > 1: a = a.mean(1)
    if s_ != sr: a = signal.resample_poly(a, sr, s_)
    return a
def trim(a, thr=0.015):
    e = np.abs(a); idx = np.where(e > thr * e.max())[0]
    if len(idx) == 0: return a
    return a[max(0, idx[0] - int(0.02 * sr)): min(len(a), idx[-1] + int(0.08 * sr))]
fade = lambda a, n=240: a * np.concatenate([np.linspace(0, 1, n), np.ones(len(a) - 2 * n), np.linspace(1, 0, n)])

files = sorted(f for f in glob.glob(os.path.join(cd, 'c_*.wav')) if not f.endswith('_t.wav'))
assert len(files) == len(plan), (len(files), len(plan))
out = [np.zeros(int(0.2 * sr))]; pos = len(out[0]); segs = {}; ch = []
for (pi, text, gap, wh), f in zip(plan, files):
    a = fade(trim(load(f)))
    # even pacing: Chatterbox sometimes rushes long sentences; slow any chunk of 5+ words above 3.5 words/s down to ~3.3
    nw = len(re.findall(r"[A-Za-z']+", TAG.sub('', text)))
    rate = nw / (len(a) / sr)
    if nw >= 5 and rate > 3.5:
        a = fade(trim(load(f, tempo=A.tempo * max(0.82, 3.3 / rate))))
        print('even-pacing chunk %r: %.2f -> %.2f w/s' % (TAG.sub('', text)[:40], rate, nw / (len(a) / sr)))
    a = a / (np.sqrt(np.mean(a ** 2)) + 1e-9) * (0.055 if wh else 0.08)
    if pi not in segs: segs[pi] = [pos / sr, 0]
    ch.append(dict(text=TAG.sub('', text), t0=round(pos / sr, 3), t1=round((pos + len(a)) / sr, 3)))
    out.append(a); pos += len(a)
    segs[pi][1] = pos / sr
    g = int(max(0, gap) * sr); out.append(np.zeros(g)); pos += g
x = np.concatenate(out)
sf.write(os.path.join(D, 'vo_raw.wav'), (x / np.abs(x).max() * 0.9).astype(np.float32), sr)
af = ('aresample=48000:resampler=soxr,highpass=f=75,equalizer=f=200:t=q:w=1:g=1.0,equalizer=f=350:t=q:w=1:g=-1.0,'
      'equalizer=f=3200:t=q:w=1.4:g=1.0,deesser=i=0.2,acompressor=threshold=-20dB:ratio=2:attack=10:release=160:makeup=1.4,'
      'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'vo_raw.wav'), '-af', af, '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s24le', os.path.join(D, 'vo48.wav')], check=True)
json.dump([dict(text=TAG.sub('', paras[k]), t0=round(v[0], 3), t1=round(v[1], 3)) for k, v in sorted(segs.items())], open(os.path.join(D, 'segments.json'), 'w'), indent=1)
json.dump(ch, open(os.path.join(D, 'chunks.json'), 'w'), indent=1)
clean = ' '.join(TAG.sub('', p) for p in paras).replace('...', ' ')
open(os.path.join(D, 'script.txt'), 'w').write(clean)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(D, 'vo48.wav'), '-ac', '1', '-ar', '16000', '-sample_fmt', 's16', os.path.join(D, 'vo16.wav')], check=True)
nw = len(re.findall(r"[A-Za-z']+", clean))
print('total %.1f s, %d words, %.0f wpm (incl. pauses)' % (len(x) / sr, nw, nw / (len(x) / sr) * 60))
