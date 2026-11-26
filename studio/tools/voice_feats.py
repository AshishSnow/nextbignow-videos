import sys, parselmouth, numpy as np, soundfile as sf
from scipy import signal
from faster_whisper import WhisperModel
m = WhisperModel('base.en', device='cpu', compute_type='int8')
for f in sys.argv[1:]:
    x, sr = sf.read(f, dtype='float32'); x = x.mean(1) if x.ndim > 1 else x; a = signal.resample_poly(x, 16000, sr).astype(np.float32)
    snd = parselmouth.Sound(a.astype(np.float64), 16000)
    p = snd.to_pitch(time_step=0.01, pitch_floor=70, pitch_ceiling=350); f0 = p.selected_array['frequency']; v = f0[f0 > 0]; st = 12 * np.log2(v / np.median(v))
    d = np.abs(np.diff(st)); d = d[d < 3]
    segs, _ = m.transcribe(a, word_timestamps=True); ws = [w for s in segs for w in s.words]
    gaps = [b.start - a_.end for a_, b in zip(ws, ws[1:])]; pz = [g for g in gaps if g > 0.15]
    print(f"{f}: dur {snd.duration:.1f}s wpm {len(ws) / snd.duration * 60:.0f} medF0 {np.median(v):.0f} range {np.percentile(st, 95) - np.percentile(st, 5):.1f}st move {d.mean():.3f} pauses>0.15s {len(pz)} mean {np.mean(pz) if pz else 0:.2f}s")
    print('   ', ' '.join(w.word.strip() for w in ws))
