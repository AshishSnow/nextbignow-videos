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
    so = ort.SessionOptions(); so.intra_op_num_threads = 2
    sess = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
    def _ut(seg):
        a16 = signal.resample_poly(seg, 16000, sr).astype(np.float32)
        k_ = (len(a16) - 400) // 320 + 1; k_ -= k_ % 2; a16 = a16[: 400 + 320 * (k_ - 1)]   # even frame count (export has no padding)
        return float(sess.run(None, {"wave": a16[None]})[0].ravel()[0])
    # whole file: > 80 s gets OOM-killed on the 7 GB box (27 Oct, 117 s VO) -> duration-weighted mean of <= 60 s chunks cut at line gaps
    if len(x) / sr <= 80:
        rep["utmos"] = round(_ut(x), 3)
    else:
        cuts = [0.0]; lv = sorted(L.values(), key=lambda l: l["start"])
        for a_, b_ in zip(lv, lv[1:]):
            if b_["start"] - cuts[-1] > 60: cuts.append((a_["end"] + b_["start"]) / 2)
        cuts.append(len(x) / sr); sc_ = [(_ut(x[int(c0 * sr):int(c1 * sr)]), c1 - c0) for c0, c1 in zip(cuts, cuts[1:])]
        rep["utmos"] = round(sum(u * d for u, d in sc_) / sum(d for _, d in sc_), 3); rep["utmos_mode"] = f"chunked x{len(sc_)}"
    # per line (VOICE.md: trust the per-line mean; whole-file moves +-0.1 on long files)
    ul = {lid: _ut(x[int((l["start"] - 0.05) * sr):int((l["end"] + 0.1) * sr)]) for lid, l in L.items()}
    rep["utmos_line"] = round(float(np.mean(list(ul.values()))), 3); rep["utmos_line_min"] = round(min(ul.values()), 2)
    rep["utmos_weak_lines"] = {k: round(v, 2) for k, v in ul.items() if v < 4.2}
except Exception as e:
    rep["utmos"] = None; rep["utmos_note"] = f"unavailable: {type(e).__name__}"
# pitch
import parselmouth
pt = parselmouth.Sound(x, sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400).selected_array["frequency"]; v = pt[pt > 0]
st = 12 * np.log2(v / np.median(v))
rep["f0_median_hz"] = round(float(np.median(v)), 1); rep["f0_range_st"] = round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1)
# line-end melody (same metric as tts_bakeoff): q_rise over "q" lines (want > +1.5 st), low_fall over "low" lines (want < -3 st)
try:
    sys.path.insert(0, f"{P}/scripts"); from vo_lines import LINES as _VL
    _end = {Ln[0]: Ln[7] for Ln in _VL}
    _pp = parselmouth.Sound(x, sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400); _tx = _pp.xs()
    _pv = _pp.selected_array["frequency"]; qs, lows = [], []
    for lid, l in L.items():
        m = (_tx >= l["start"]) & (_tx <= l["end"]) & (_pv > 0); vv = _pv[m]
        if len(vv) < 20: continue
        d = 12 * np.log2(np.median(vv[-max(5, len(vv) // 6):]) / np.median(vv))
        (qs if _end.get(lid) == "q" else lows if _end.get(lid) == "low" else []).append(d)
    rep["q_rise_st"] = round(float(np.mean(qs)), 1) if qs else None; rep["low_fall_st"] = round(float(np.mean(lows)), 1) if lows else None
except Exception as e:
    rep["melody_note"] = f"unavailable: {type(e).__name__}"
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
    def _decade(m):
        w = (_n2w(int(m.group(1)), to="year") if _n2w else m.group(1)).split()
        w[-1] = w[-1][:-1] + "ies" if w[-1].endswith("y") else w[-1] + "s"
        return " " + " ".join(w) + " "
    def norm(s):
        # compare words, not formatting: "$1.7 billion" == "one point seven billion dollars", "Step 1." == "step one"
        s = s.lower().replace("%", " percent ").replace(" and a half", " point five")   # "ten and a half" == "10.5"
        s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)   # "U.S." == "US"
        s = re.sub(r"\$(\d+)\.(\d\d)\b", _cents, s)   # "$1.50" (ASR) == "a dollar fifty" (script)
        s = re.sub(r"\b((?:19|20)\d0)'?s\b", _decade, s)   # "1980s" == "nineteen eighties"
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
