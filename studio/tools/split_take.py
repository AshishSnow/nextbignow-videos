"""split_take.py <audio> <out_dir> <first-words-1> <first-words-2> ...
Transcribes one long take with word timestamps, cuts it where each script's opening words start,
writes <out_dir>/part_<i>.wav (48 kHz mono)."""
import sys, os, re, subprocess
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]; heads = [h.lower().split() for h in sys.argv[3:]]
os.makedirs(out, exist_ok=True)
m = WhisperModel('small.en', compute_type='int8')
segs, _ = m.transcribe(src, word_timestamps=True)
W = [(re.sub(r"[^\w']", '', w.word.lower()), w.start, w.end) for s in segs for w in s.words]
starts = []
for h in heads:
    for i in range(len(W)):
        if all(i + j < len(W) and W[i + j][0] == h[j] for j in range(len(h))) and (not starts or W[i][1] > starts[-1]):
            starts.append(W[i][1]); break
    else: sys.exit(f'head not found: {h}')
end = W[-1][2] + 0.4
for k, t0 in enumerate(starts):
    t1 = starts[k + 1] - 0.05 if k + 1 < len(starts) else end
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-ss', f'{max(0, t0 - 0.08):.3f}', '-to', f'{t1:.3f}', '-ac', '1', '-ar', '48000', f'{out}/part_{k}.wav'], check=True)
    print(f'part_{k}: {t0:.2f}-{t1:.2f}')
