import sys, soundfile as sf
from faster_whisper import WhisperModel
wav = sys.argv[1]
m = WhisperModel('medium', device='cpu', compute_type='int8')
a, sr = sf.read(wav, dtype='float32'); segs, info = m.transcribe(a, language='hi', vad_filter=True, vad_parameters=dict(min_silence_duration_ms=250), word_timestamps=False, beam_size=5)
d = sf.info(wav).duration; print(f"{d:.6f}")
for s in segs: print(f"{s.start:.2f}-{s.end:.2f}  {s.text.strip()}")
