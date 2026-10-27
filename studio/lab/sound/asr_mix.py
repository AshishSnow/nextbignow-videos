import sys, json, re, numpy as np, soundfile as sf, sherpa_onnx, difflib
from scipy import signal
B, tag = sys.argv[1], sys.argv[2]; R="/home/claude/studio"
d=f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
rec=sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx",decoder=f"{d}/decoder.int8.onnx",joiner=f"{d}/joiner.int8.onnx",tokens=f"{d}/tokens.txt",model_type="nemo_transducer",num_threads=2)
y,sr=sf.read(f"{B}/work/mix_{tag}.wav"); y=y.mean(1)
y=signal.sosfilt(signal.butter(4,[300,10000],"band",fs=sr,output="sos"),y)
L=json.load(open(f"{B}/work/align.json"))["lines"]
txt={}
exec(open(f"{B}/scripts/vo_lines.py").read()); 
for t in LINES: txt[t[0]]=t[1]
norm=lambda s: re.sub(r"[^a-z0-9 ]"," ",s.lower().replace("-"," ")).split()
err=tot=0; bad=[]
for k,v in L.items():
    a=y[int((v['start']-0.05)*sr):int((v['end']+0.1)*sr)]
    a=signal.resample_poly(a,1,3).astype(np.float32)
    s=rec.create_stream(); s.accept_waveform(16000,a); rec.decode_stream(s)
    r,h=norm(txt.get(k,"")),norm(s.result.text)
    sm=difflib.SequenceMatcher(a=r,b=h); e=len(r)-sum(m.size for m in sm.get_matching_blocks()) + max(0,len(h)-len(r))
    err+=e; tot+=len(r)
    if e: bad.append((k,e))
print(B,tag,"approx WER %.3f"%(err/max(tot,1)),"lines with errors",bad)
