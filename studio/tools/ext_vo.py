"""Use an externally generated voiceover (e.g. an ElevenLabs take the owner downloaded): clean it, cap over-long pauses,
then align words with Whisper against the project's script (scripts/maya_paras.py PARAS text).
usage: python3 ext_vo.py <project dir> <audio file> [max_pause_s]"""
import sys, os, re, json, difflib, subprocess, numpy as np, soundfile as sf
from scipy import signal
P, SRC = sys.argv[1], sys.argv[2]; MAXP = float(sys.argv[3]) if len(sys.argv) > 3 else 0.75
sys.path.insert(0, f'{P}/scripts'); from maya_paras import PARAS
SR = 48000; LEAD = 0.25
tmp = f'{P}/work/_ext.wav'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', SRC, '-ac', '1', '-ar', str(SR), tmp], check=True)
x, _ = sf.read(tmp, dtype='float32'); os.remove(tmp)
# cap silences longer than MAXP (keeps natural pauses, removes dead air)
hop = int(0.01 * SR); n = len(x) // hop; e = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)); thr = max(1e-4, np.percentile(e, 95) * 0.03)
sil = e < thr; keep = np.ones(n, bool); i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        L = j - i; cap = int(MAXP / 0.01)
        if i == 0: keep[i:max(i, j - 2)] = False                     # leading silence
        elif j == n: keep[i + 10:j] = False                           # trailing
        elif L > cap: keep[i + cap // 2: j - cap // 2] = False
        i = j
    else: i += 1
m = np.repeat(keep, hop); x = np.concatenate([x[:n * hop][m], x[n * hop:]])
b, a_ = signal.butter(2, 70 / (SR / 2), 'high'); x = signal.lfilter(b, a_, x).astype(np.float32)
x = np.concatenate([np.zeros(int(LEAD * SR), np.float32), x]); x = x / (np.abs(x).max() + 1e-6) * 0.89
sf.write(f'{P}/work/vo.wav', x, SR)
from faster_whisper import WhisperModel
wm = WhisperModel('small.en', device='cpu', compute_type='int8')
segs, _ = wm.transcribe(signal.resample_poly(x, 16000, SR).astype(np.float32), word_timestamps=True, beam_size=5)
ws = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
print('heard:', ' '.join(w for w, _, _ in ws))
norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())
script = ' '.join(t for t, _, _ in PARAS); toks = re.findall(r"[A-Za-z0-9'%]+", script)
wt = [norm(w) for w, _, _ in ws]; st = [norm(t) for t in toks]
times = [None] * len(toks)
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, st, wt, autojunk=False).get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1): times[i1 + k] = (ws[j1 + k][1], ws[j1 + k][2])
    elif tag == 'replace' and j2 > j1:
        s0, e0 = ws[j1][1], ws[j2 - 1][2]; nn = i2 - i1
        for k in range(nn): times[i1 + k] = (s0 + (e0 - s0) * k / nn, s0 + (e0 - s0) * (k + 1) / nn)
for i in range(len(times)):
    if times[i] is None:
        prv = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
        nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prv + 0.3)
        times[i] = (prv, max(prv + 0.05, min(nxt, prv + 0.3)))
out = [[t, round(a, 3), round(b, 3)] for t, (a, b) in zip(toks, times)]
os.makedirs(f'{P}/comic/cd', exist_ok=True)
json.dump(out, open(f'{P}/comic/cd/align.json', 'w')); open(f'{P}/comic/cd/script.txt', 'w').write(script)
dur = len(x) / SR; print('align', len(out), out[-1], 'dur', round(dur, 2), 'wpm', round(len(toks) / dur * 60))
