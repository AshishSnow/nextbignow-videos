"""Pick the best of several TTS takes of one line: exact read-back first (parakeet ASR), then naturalness (UTMOS22, ONNX).
Used by make_vo.py when TAKES > 1. Models live in $STUDIO/models (setup.sh)."""
import os, re, difflib, numpy as np
from scipy import signal

R = os.environ.get("STUDIO", "/home/claude/studio")
_utm = _rec = None


def _norm(s):
    from num2words import num2words
    s = s.lower().replace("%", " percent ")
    s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)
    def num(m):
        t = m.group(0).replace(",", "")
        try: return " " + num2words(float(t) if "." in t else int(t)) + " "
        except Exception: return " " + t + " "
    s = re.sub(r"\d[\d,]*(\.\d+)?", num, s)
    s = re.sub(r"[^a-z ]", " ", s.replace("-", " "))
    return [w for w in s.split() if w not in ("dollar", "dollars", "and")]


def utmos(a, sr):
    global _utm
    import onnxruntime as ort
    if _utm is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = os.cpu_count() or 2
        _utm = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
    x = signal.resample_poly(np.asarray(a, np.float64), 16000, sr).astype(np.float32)
    k = (len(x) - 400) // 320 + 1; k -= k % 2
    return float(_utm.run(None, {"wave": x[: 400 + 320 * (k - 1)][None]})[0].ravel()[0])


def asr_errors(a, sr, text):
    global _rec
    import sherpa_onnx
    if _rec is None:
        d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
        _rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx",
                                                             joiner=f"{d}/joiner.int8.onnx", tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=2)
    x = signal.resample_poly(np.asarray(a, np.float64), 16000, sr).astype(np.float32)
    st = _rec.create_stream(); st.accept_waveform(16000, np.concatenate([np.zeros(4000, np.float32), x, np.zeros(4000, np.float32)])); _rec.decode_stream(st)
    ref, hyp = _norm(text), _norm(st.result.text)
    m = sum(b.size for b in difflib.SequenceMatcher(a=ref, b=hyp).get_matching_blocks())
    return max(len(ref), len(hyp)) - m, st.result.text


def pick(takes, sr, text, log=None):
    """takes: list of float arrays. Returns (index, scores)."""
    sc = []
    for i, a in enumerate(takes):
        e, heard = asr_errors(a, sr, text); u = utmos(a, sr)
        sc.append((e, -u, i))
        if log: log(f"   take {i}: asr_err {e} utmos {u:.2f} | {heard}")
    best = min(sc)[2]
    return best, sc
