import sys, numpy as np, soundfile as sf, onnxruntime as ort
from scipy import signal
so = ort.SessionOptions(); so.intra_op_num_threads = 2
S = ort.InferenceSession('/home/claude/studio/models/utmos/utmos22.onnx', so, providers=['CPUExecutionProvider'])
def score(f):
    x, sr = sf.read(f, dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    a = signal.resample_poly(x, 16000, sr).astype(np.float32); k = (len(a) - 400) // 320 + 1; k -= k % 2; a = a[:400 + 320 * (k - 1)]
    return float(S.run(None, {'wave': a[None]})[0].ravel()[0])
if __name__ == "__main__":
    for f in sys.argv[1:]: print(f'{score(f):.3f}  {f}')
