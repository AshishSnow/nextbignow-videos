"""kokoro_vo.py <proj> [voice] [speed]
In-house voice with Kokoro-82M (Apache-2.0, commercial OK, fast on CPU).
Reads <proj>/scripts/maya_paras.py PARAS, speaks sentence by sentence with natural gaps,
masters (high-pass, presence lift, gentle compression, -16 LUFS), writes <proj>/work/kokoro_raw.wav,
then runs ext_vo.py so vo.wav + align.json are produced exactly like an external take.
Voices: af_heart (warm female, best graded), af_bella (bright female), am_michael (male), am_puck (young male).
A blend like 'af_heart+af_bella' averages the two style vectors."""
import sys, os, re, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
proj = sys.argv[1]; voice = sys.argv[2] if len(sys.argv) > 2 else 'af_heart'; speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
sys.path.insert(0, os.path.join(proj, 'scripts')); from maya_paras import PARAS
M = '/home/claude/models/kokoro/'; k = Kokoro(M + 'kokoro-v1.0.onnx', M + 'voices-v1.0.bin')
if '+' in voice:
    vs = [k.get_voice_style(v) for v in voice.split('+')]; style = sum(vs) / len(vs)
else:
    style = voice
SR = 24000; out = []
def sil(s): return np.zeros(int(SR * s), np.float32)
for pi, (txt, pause, _) in enumerate(PARAS):
    sents = [s for s in re.split(r'(?<=[.?!])\s+', txt.strip()) if s]
    for si, s in enumerate(sents):
        a, sr = k.create(s, voice=style, speed=speed, lang='en-us'); assert sr == SR
        a = a.astype(np.float32)
        nz = np.where(np.abs(a) > 0.01)[0]
        if len(nz): a = a[max(0, nz[0] - 240): nz[-1] + 1200]
        out.append(a)
        q = s.rstrip()[-1]
        out.append(sil(0.32 if q in '?!' else 0.24))
    out.append(sil(max(0.15, pause)))
raw = np.concatenate(out)
os.makedirs(os.path.join(proj, 'work'), exist_ok=True)
tmp = os.path.join(proj, 'work', 'kokoro_dry.wav'); dst = os.path.join(proj, 'work', 'kokoro_raw.wav')
sf.write(tmp, raw, SR)
af = 'highpass=f=70,equalizer=f=220:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=9000:t=q:w=1:g=-1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', tmp, '-af', af, '-ar', '48000', '-ac', '1', dst], check=True)
print('kokoro', voice, f'{len(raw) / SR:.1f}s ->', dst)
if '--no-align' not in sys.argv:
    subprocess.run(['python3', '/home/claude/studio/lib/ext_vo.py', proj, dst], check=True)
