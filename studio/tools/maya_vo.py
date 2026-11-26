"""Build a full voiceover with Maya1 in natural paragraphs (flowing delivery, few pauses), then align words with Whisper.
usage: python3 maya_vo.py <project dir> [desc-file]
reads scripts/maya_paras.py: DESC (str), PARAS = [(text, gap_after_s, seed), ...]
writes work/vo.wav (48 kHz, cleaned, -16 LUFS-ish), comic/cd/align.json ([word, start, end]), comic/cd/script.txt"""
import sys, os, re, json, difflib, numpy as np, soundfile as sf
from scipy import signal
P = sys.argv[1]; sys.path.insert(0, f'{P}/scripts'); sys.path.insert(0, '/home/claude/studio/lib')
from maya_paras import DESC, PARAS
import maya_tts
import utmos_score

SR = 48000; LEAD = 0.25
cache = f'{P}/work/maya'; os.makedirs(cache, exist_ok=True)
pieces = [np.zeros(int(LEAD * SR), np.float32)]
for i, (text, gap, seed) in enumerate(PARAS):
    f = f'{cache}/p{i:02d}_{seed}.wav'
    best = None
    if not os.path.exists(f):
        a = maya_tts.generate(DESC, text, seed); sf.write(f, a, 24000)
    a, sr = sf.read(f, dtype='float32')
    # trim leading/trailing silence
    e = np.abs(a) > 0.01; idx = np.where(e)[0]
    if len(idx): a = a[max(0, idx[0] - 600): idx[-1] + 2400]
    a = signal.resample_poly(a, SR, sr).astype(np.float32)
    n = int(0.01 * SR); a[:n] *= np.linspace(0, 1, n); a[-n:] *= np.linspace(1, 0, n)
    pieces += [a, np.zeros(int(gap * SR), np.float32)]
    print('para', i, f'{len(a) / SR:.1f}s', flush=True)
x = np.concatenate(pieces)
# gentle polish: high-pass 70 Hz, light presence, peak normalise; loudness done in mix
b, a_ = signal.butter(2, 70 / (SR / 2), 'high'); x = signal.lfilter(b, a_, x).astype(np.float32)
x = x / (np.abs(x).max() + 1e-6) * 0.89
os.makedirs(f'{P}/work', exist_ok=True); sf.write(f'{P}/work/vo.wav', x, SR)

# ---- align: whisper word stamps -> script tokens
from faster_whisper import WhisperModel
m = WhisperModel('small.en', device='cpu', compute_type='int8')
a16 = signal.resample_poly(x, 16000, SR).astype(np.float32)
segs, _ = m.transcribe(a16, word_timestamps=True, beam_size=5)
ws = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())
script = ' '.join(t for t, _, _ in PARAS)
toks = re.findall(r"[A-Za-z0-9'%]+", script)
wt = [norm(w) for w, _, _ in ws]; st = [norm(t) for t in toks]
sm = difflib.SequenceMatcher(None, st, wt, autojunk=False)
times = [None] * len(toks)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): times[i1 + k] = (ws[j1 + k][1], ws[j1 + k][2])
    elif tag == 'replace' and j2 > j1:
        s0, e0 = ws[j1][1], ws[j2 - 1][2]; n = i2 - i1
        for k in range(n): times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
# fill gaps by interpolation
for i in range(len(times)):
    if times[i] is None:
        prv = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prv + 0.3)
        times[i] = (prv, max(prv + 0.05, min(nxt, prv + 0.3)))
out = [[t, round(a, 3), round(b, 3)] for t, (a, b) in zip(toks, times)]
os.makedirs(f'{P}/comic/cd', exist_ok=True)
json.dump(out, open(f'{P}/comic/cd/align.json', 'w')); open(f'{P}/comic/cd/script.txt', 'w').write(script)
print('align', len(out), out[-1], 'dur', round(len(x) / SR, 2))
print('utmos', round(utmos_score.score(f'{P}/work/vo.wav'), 3) if len(x) / SR < 80 else 'skip')
