"""Chain-only A/B on one fixed vo_raw.wav (removes PSOLA/gate run noise): same chain as make_vo.py, varying
de-esser target (DEESS) and room send (ROOM_DB). Usage: python3 chain_ab.py <project> "DEESS,ROOM_DB[,RATIO]" ...
Writes work/chain_<deess>_<room>.wav and prints per-line UTMOS mean/min + the 6 shortest lines' mean."""
import sys, os, json, numpy as np, soundfile as sf
from scipy import signal
R = os.environ.get("STUDIO", "/home/claude/studio"); sys.path.insert(0, f"{R}/lib")
import voice_clean, onnxruntime as ort
P = sys.argv[1]; SR = 48000
raw, sr = sf.read(f"{P}/work/vo_raw.wav"); assert sr == SR
L = json.load(open(f"{P}/work/align.json"))["lines"]
so = ort.SessionOptions(); so.intra_op_num_threads = 2
sess = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
def ut(seg):
    a16 = signal.resample_poly(seg, 16000, SR).astype(np.float32); k_ = (len(a16) - 400) // 320 + 1; k_ -= k_ % 2
    return float(sess.run(None, {"wave": a16[: 400 + 320 * (k_ - 1)][None]})[0].ravel()[0])
def peq(f0, g, q):
    A = 10 ** (g / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a_ = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.tf2sos(np.array(b) / a_[0], np.array(a_) / a_[0])
def chain(deess, room, ratio=2.2):
    x = signal.sosfilt(peq(3100, 1.0, 1.0), signal.sosfilt(peq(160, 1.0, 0.8), raw.astype(np.float64)))
    y = voice_clean.clean(x, 1.0, deess_target=deess, verbose=False, ratio=ratio).astype(np.float64)
    rng = np.random.default_rng(5); n = int(0.32 * SR); tt = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-tt / 0.07); ir[: int(0.006 * SR)] = 0
    for d_, g in ((0.009, 0.6), (0.014, 0.45), (0.021, 0.35), (0.029, 0.25)): ir[int(d_ * SR)] += g * 6
    ir = signal.sosfilt(signal.butter(2, [250, 5500], "band", fs=SR, output="sos"), ir); ir /= np.sqrt((ir ** 2).sum())
    if room > -90:
        wet = signal.fftconvolve(y, ir)[: len(y)]
        y = y + wet * (np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-12)) * 10 ** (room / 20)
    return y / (np.abs(y).max() + 1e-9) * 10 ** (-1 / 20)
short = sorted(L, key=lambda k: L[k]["end"] - L[k]["start"])[:6]
for arg in sys.argv[2:]:
    v_ = [float(v) for v in arg.split(",")]; de, ro = v_[:2]; ra = v_[2] if len(v_) > 2 else 2.2
    y = chain(de, ro, ra); sf.write(f"{P}/work/chain_{int(de)}_{int(ro)}.wav", y.astype(np.float32), SR, subtype="FLOAT")
    ul = {k: ut(y[int((l["start"] - 0.05) * SR):int((l["end"] + 0.1) * SR)]) for k, l in L.items()}
    print(json.dumps(dict(deess=de, room=ro, ratio=ra, line_mean=round(np.mean(list(ul.values())), 3), line_min=round(min(ul.values()), 3),
                          short6=round(np.mean([ul[k] for k in short]), 3), worst=min(ul, key=ul.get))), flush=True)
