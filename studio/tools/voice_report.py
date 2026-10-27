"""Voice quality report for a project: naturalness (UTMOS, if available), pitch, pace, pauses, ASR read-back accuracy.
Usage: python3 voice_report.py <project_dir> [vo.wav]   -> prints a summary and writes work/voice_report.json"""
import sys, os, json, re, difflib, numpy as np, soundfile as sf
from scipy import signal
P = sys.argv[1]; R = os.environ.get("STUDIO", "/home/claude/studio")
wav = sys.argv[2] if len(sys.argv) > 2 else f"{P}/work/vo.wav"
x, sr = sf.read(wav); x = x if x.ndim == 1 else x.mean(1)
A = json.load(open(f"{P}/work/align.json")); L = A["lines"]; Wd = A["words"]
rep = {}
# naturalness (UTMOS22 strong, ONNX; 1 = bad, 5 = excellent) — optional
try:
    import onnxruntime as ort
    a16 = signal.resample_poly(x, 16000, sr).astype(np.float32)
    k_ = (len(a16) - 400) // 320 + 1; k_ -= k_ % 2; a16 = a16[: 400 + 320 * (k_ - 1)]   # even frame count (export has no padding)
    so = ort.SessionOptions(); so.intra_op_num_threads = 2
    sess = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
    rep["utmos"] = round(float(sess.run(None, {"wave": a16[None]})[0].ravel()[0]), 3)
except Exception as e:
    rep["utmos"] = None; rep["utmos_note"] = f"unavailable: {type(e).__name__}"
# pitch
import parselmouth
pt = parselmouth.Sound(x, sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400).selected_array["frequency"]; v = pt[pt > 0]
st = 12 * np.log2(v / np.median(v))
rep["f0_median_hz"] = round(float(np.median(v)), 1); rep["f0_range_st"] = round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1)
# pace and pauses
speech = sum(l["end"] - l["start"] for l in L.values()); total = max(l["end"] for l in L.values()) - min(l["start"] for l in L.values())
nw = len(Wd); rep["words"] = nw; rep["duration_s"] = round(total, 1)
rep["wpm_overall"] = round(nw / total * 60, 1); rep["wpm_speaking"] = round(nw / speech * 60, 1); rep["pause_ratio"] = round(1 - speech / total, 3)
# ASR read-back
try:
    import sherpa_onnx
    d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx", joiner=f"{d}/joiner.int8.onnx", tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=2)
    try:
        from num2words import num2words as _n2w
    except Exception:
        _n2w = None
    def _num(m):
        t = m.group(0).replace(",", "")
        try:
            if _n2w and re.fullmatch(r"(19|20)\d\d", t): return " " + _n2w(int(t), to="year") + " "   # "2020" == "twenty twenty"
            return " " + (_n2w(float(t) if "." in t else int(t)) if _n2w else t) + " "
        except Exception: return " " + t + " "
    def _cents(m):
        a, b = m.group(1), m.group(2)
        w = lambda v: _n2w(int(v)) if _n2w else v
        return " " + ("a" if a == "1" else w(a)) + " " + w(b) + " "
    def norm(s):
        # compare words, not formatting: "$1.7 billion" == "one point seven billion dollars", "Step 1." == "step one"
        s = s.lower().replace("%", " percent ").replace(" and a half", " point five")   # "ten and a half" == "10.5"
        s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)   # "U.S." == "US"
        s = re.sub(r"\$(\d+)\.(\d\d)\b", _cents, s)   # "$1.50" (ASR) == "a dollar fifty" (script)
        s = re.sub(r"\d[\d,]*(\.\d+)?", _num, s)
        s = re.sub(r"[^a-z ]", " ", s.replace("-", " "))
        return [w for w in s.split() if w not in ("dollar", "dollars", "and")]
    errs = 0; tot = 0; bad = []
    for lid, l in L.items():
        a = signal.resample_poly(x[int((l["start"] - 0.05) * sr):int((l["end"] + 0.1) * sr)], 16000, sr).astype(np.float32)
        s_ = rec.create_stream(); s_.accept_waveform(16000, a); rec.decode_stream(s_)
        ref, hyp = norm(l["text"]), norm(s_.result.text)
        sm = difflib.SequenceMatcher(a=ref, b=hyp); match = sum(b.size for b in sm.get_matching_blocks())
        e = max(len(ref), len(hyp)) - match; errs += e; tot += len(ref)
        if e > 1: bad.append((lid, s_.result.text))
    rep["asr_word_error_approx"] = round(errs / max(1, tot), 3); rep["asr_bad_lines"] = bad
except Exception as e:
    rep["asr_note"] = f"unavailable: {type(e).__name__}"
json.dump(rep, open(f"{P}/work/voice_report.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
