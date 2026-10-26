import sys, json, numpy as np, soundfile as sf, sherpa_onnx
from scipy import signal
B=sys.argv[1]; R="/home/claude/studio"
d=f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx",decoder=f"{d}/decoder.int8.onnx",joiner=f"{d}/joiner.int8.onnx",tokens=f"{d}/tokens.txt",model_type="nemo_transducer",num_threads=4)
y,sr=sf.read(f"{B}/work/vo.wav"); y=y if y.ndim==1 else y.mean(1)
L=json.load(open(f"{B}/work/align.json"))["lines"]
for k,v in L.items():
    a=y[int((v['start']-0.05)*sr):int((v['end']+0.1)*sr)]
    a=signal.resample_poly(a,16000,sr).astype(np.float32)
    s=rec.create_stream(); s.accept_waveform(16000,a); rec.decode_stream(s)
    print(k,"|",s.result.text)
