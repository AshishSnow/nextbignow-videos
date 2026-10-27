"""TTS engine bake-off on one project's script: same lines, same pauses, scored the same way.
Usage:
  python3 tts_bakeoff.py <project_dir> <engine> [--ref ref.wav] [--tag name] [--lm q8|q4|fp32]
    engine = kokoro      -> current narrator blend (VMIX/SPD/SPLIT env like make_vo.py), dry, no PSOLA
             chatterbox  -> Chatterbox-Turbo ONNX (MIT, ResembleAI/chatterbox-turbo-ONNX) conditioned on --ref
                            (use only a SYNTHETIC reference, e.g. our own Kokoro narrator — never a real person)
  python3 tts_bakeoff.py <project_dir> score <wav> [<wav> ...]   -> score already-made files (needs <wav>.json line map)
Writes $P/work/bake_<tag>.wav (+ .json line map) and prints/appends a score row to $P/work/bakeoff.jsonl:
  utmos (whole file), utmos_line (mean of per-line UTMOS = length-fair), f0 range (st), q_rise_st / low_fall_st (line-end melody),
  speaking wpm, ASR bad lines, RTF.
Needs models from setup.sh (+ $STUDIO/models/cbturbo for chatterbox)."""
import sys, os, re, json, time, difflib, importlib.util, numpy as np, soundfile as sf
from scipy import signal

R = os.environ.get("STUDIO", "/home/claude/studio")
SR = 48000; LEAD = 0.25
SPD = float(os.environ.get("SPD", "0.88")); PZ = float(os.environ.get("PZ", "1.6")); PMIN = float(os.environ.get("PMIN", "0.3"))
SPLIT = float(os.environ.get("SPLIT", "0.12"))


def load_lines(P):
    spec = importlib.util.spec_from_file_location("vo_lines", f"{P}/scripts/vo_lines.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.LINES


def trim(a, sr, db=-42, pad=0.03):
    """cut leading/trailing silence (engine padding) with a little air"""
    e = np.convolve(a ** 2, np.ones(int(0.01 * sr)) / int(0.01 * sr), "same"); th = e.max() * 10 ** (db / 10)
    idx = np.where(e > th)[0]
    if not len(idx): return a
    return a[max(0, idx[0] - int(pad * sr)): idx[-1] + int(pad * sr)]


# ---------------- engines ----------------
class KokoroEng:
    def __init__(self):
        from kokoro_onnx import Kokoro
        self.k = Kokoro(f"{R}/models/kokoro/kokoro-v1.0.onnx", f"{R}/models/kokoro/voices-v1.0.bin"); V = self.k.get_voice_style
        vm = os.environ.get("VMIX", "am_michael:0.5,am_eric:0.3,am_fenrir:0.2")
        self.voice = sum(float(w) * V(n) for n, w in (p.split(":") for p in vm.split(",")))

    def say(self, text, speed):
        parts = [q for q in re.split(r"(?<=[.?!…])\s+", text) if q.strip()] if SPLIT > 0 else [text]
        segs = []
        for i, q in enumerate(parts):
            a, sr = self.k.create(q, voice=self.voice, speed=speed * SPD, lang="en-us", trim=True)
            segs.append(signal.resample_poly(a.astype(np.float64), SR, sr))
            if i < len(parts) - 1: segs.append(np.zeros(int(SPLIT * SR)))
        return np.concatenate(segs)


class ChatterboxEng:
    """Chatterbox-Turbo ONNX, greedy decoding as in the official model card (deterministic)."""
    START, STOP, SIL, KVH, HD, CSR = 6561, 6562, 4299, 16, 64, 24000

    def __init__(self, ref, lm="q8"):
        import onnxruntime as ort
        from tokenizers import Tokenizer
        d = f"{R}/models/cbturbo"; so = ort.SessionOptions(); so.intra_op_num_threads = 2
        S = lambda n: ort.InferenceSession(f"{d}/{n}.onnx", so, providers=["CPUExecutionProvider"])
        self.embed = S("embed_tokens"); self.lm = S("language_model" + {"q8": "_quantized", "q4": "_q4", "fp32": ""}[lm]); self.dec = S("conditional_decoder")
        self.tok = Tokenizer.from_file(f"{d}/tokenizer.json")
        self.rep = float(os.environ.get("CB_REP", "1.2"))
        cache = os.path.splitext(ref)[0] + ".cbcond.npz"   # speaker conditioning is computed once per reference clip
        if os.path.exists(cache):
            z = np.load(cache); self.cond = [z[k] for k in ("cond_emb", "prompt_token", "spk", "feat")]
        else:
            enc = S("speech_encoder")
            a, sr = sf.read(ref); a = a if a.ndim == 1 else a.mean(1)
            a = signal.resample_poly(a, self.CSR, sr).astype(np.float32)[None]
            self.cond = enc.run(None, {"audio_values": a}); del enc
            np.savez(cache, cond_emb=self.cond[0], prompt_token=self.cond[1], spk=self.cond[2], feat=self.cond[3])

    def say(self, text, speed=1.0):
        cond_emb, prompt_token, spk, feat = self.cond
        ids = np.array([self.tok.encode(text).ids], np.int64)
        gen = np.array([[self.START]], np.int64); x = ids
        maxn = 40 + 25 * len(text.split()) * 2
        for i in range(maxn):
            emb = self.embed.run(None, {"input_ids": x})[0]
            if i == 0:
                emb = np.concatenate((cond_emb, emb), 1); n = emb.shape[1]
                pkv = {j.name: np.zeros([1, self.KVH, 0, self.HD], np.float16 if j.type == "tensor(float16)" else np.float32)
                       for j in self.lm.get_inputs() if "past_key_values" in j.name}
                am = np.ones((1, n), np.int64); pos = np.arange(n, dtype=np.int64)[None]
            logits, *pres = self.lm.run(None, dict(inputs_embeds=emb, attention_mask=am, position_ids=pos, **pkv))
            lg = logits[:, -1, :].copy(); sc = np.take_along_axis(lg, gen, 1)
            np.put_along_axis(lg, gen, np.where(sc < 0, sc * self.rep, sc / self.rep), 1)
            x = np.argmax(lg, -1, keepdims=True).astype(np.int64); gen = np.concatenate((gen, x), -1)
            if x[0, 0] == self.STOP: break
            am = np.concatenate([am, np.ones((1, 1), np.int64)], 1); pos = pos[:, -1:] + 1
            for j, k_ in enumerate(pkv): pkv[k_] = pres[j]
        tok = np.concatenate([prompt_token, gen[:, 1:-1] if gen[0, -1] == self.STOP else gen[:, 1:], np.full((1, 3), self.SIL, np.int64)], 1)
        wav = self.dec.run(None, dict(speech_tokens=tok, speaker_embeddings=spk, speaker_features=feat))[0].squeeze()
        wav = trim(wav.astype(np.float64), self.CSR)
        if abs(speed - 1) > 0.01:   # Turbo has no speed knob -> pitch-preserving time stretch (Praat PSOLA) only if asked
            import parselmouth
            from parselmouth.praat import call
            s = parselmouth.Sound(wav, self.CSR); m = call(s, "To Manipulation", 0.01, 65, 400)
            dt = call("Create DurationTier", "d", 0, s.duration); call(dt, "Add point", 0, 1 / speed); call([dt, m], "Replace duration tier")
            wav = call(m, "Get resynthesis (overlap-add)").values[0]
        return signal.resample_poly(wav, SR, self.CSR)


def synth(P, eng, tag, line_speed=True):
    LINES = load_lines(P); pieces = [np.zeros(int(LEAD * SR))]; t = LEAD; lines = {}; t0 = time.time()
    for lid, text, sp, pause, *_ in LINES:
        a = eng.say(text, sp if line_speed else 1.0)
        f = int(0.012 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        lines[lid] = dict(start=round(t, 3), end=round(t + len(a) / SR, 3), text=text); pieces.append(a); t += len(a) / SR
        pz = max(PMIN, pause * PZ) if pause > 0 else 0.0; pieces.append(np.zeros(int(pz * SR))); t += pz
        print(f"  {lid} {len(a) / SR:5.2f}s", flush=True)
    y = np.concatenate(pieces + [np.zeros(int(0.3 * SR))]); el = time.time() - t0
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    out = f"{P}/work/bake_{tag}.wav"; sf.write(out, y.astype(np.float32), SR, subtype="FLOAT")
    json.dump(dict(lines=lines, rtf=round(el / (len(y) / SR), 2)), open(out + ".json", "w"), indent=0)
    return out


# ---------------- scoring ----------------
_utm = None


def utmos(a, sr):
    global _utm
    import onnxruntime as ort
    if _utm is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        _utm = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
    a16 = signal.resample_poly(a, 16000, sr).astype(np.float32)
    k_ = (len(a16) - 400) // 320 + 1; k_ -= k_ % 2; a16 = a16[: 400 + 320 * (k_ - 1)]
    return float(_utm.run(None, {"wave": a16[None]})[0].ravel()[0])


def score(P, wav):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    x, sr = sf.read(wav); x = x if x.ndim == 1 else x.mean(1)
    meta = json.load(open(wav + ".json")) if os.path.exists(wav + ".json") else json.load(open(f"{P}/work/align.json"))
    L = meta["lines"]; rep = dict(file=os.path.basename(wav), rtf=meta.get("rtf"))
    rep["utmos"] = round(utmos(x, sr), 3)
    ul = [utmos(x[int((l["start"] - 0.05) * sr): int((l["end"] + 0.1) * sr)], sr) for l in L.values()]
    rep["utmos_line"] = round(float(np.mean(ul)), 3); rep["utmos_line_min"] = round(float(np.min(ul)), 2)
    import parselmouth
    pt = parselmouth.Sound(x, sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400).selected_array["frequency"]; v = pt[pt > 0]
    st = 12 * np.log2(v / np.median(v))
    rep["f0_hz"] = round(float(np.median(v)), 1); rep["range_st"] = round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1)
    # melody at line ends (UTMOS can't hear this): last sixth of each line's voiced F0 vs the line median, in semitones.
    # q_rise = mean over question lines (want > +1.5), low_fall = mean over "low" lines (want < -3)
    tp = parselmouth.Sound(x, sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400); tx = tp.xs()
    end = {}
    try: end = {Ln[0]: Ln[7] for Ln in load_lines(P)}
    except Exception: pass
    qs, lows = [], []
    for lid, l in L.items():
        m = (tx >= l["start"]) & (tx <= l["end"]) & (pt > 0); vv = pt[m]
        if len(vv) < 20: continue
        d = 12 * np.log2(np.median(vv[-max(5, len(vv) // 6):]) / np.median(vv))
        (qs if end.get(lid) == "q" else lows if end.get(lid) == "low" else []).append(d)
    rep["q_rise_st"] = round(float(np.mean(qs)), 1) if qs else None; rep["low_fall_st"] = round(float(np.mean(lows)), 1) if lows else None
    nw = sum(len(l["text"].split()) for l in L.values()); speech = sum(l["end"] - l["start"] for l in L.values())
    rep["wpm_speaking"] = round(nw / speech * 60, 1); rep["dur_s"] = round(len(x) / sr, 1)
    import sherpa_onnx
    from num2words import num2words
    d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx", joiner=f"{d}/joiner.int8.onnx",
                                                        tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=2)

    def norm(s):
        s = s.lower().replace("%", " percent ")
        # "$1.50" (ASR) == "a dollar fifty" / "one fifty" (script)
        s = re.sub(r"\$(\d+)\.(\d\d)\b", lambda m: " " + ("a" if m.group(1) == "1" else num2words(int(m.group(1)))) + " " + num2words(int(m.group(2))) + " ", s)
        s = re.sub(r"\d[\d,]*(\.\d+)?", lambda m: " " + num2words(float(m.group(0).replace(",", "")) if "." in m.group(0) else int(m.group(0).replace(",", ""))) + " ", s)
        s = re.sub(r"[^a-z ]", " ", s.replace("-", " "))
        return [w for w in s.split() if w not in ("dollar", "dollars", "and")]
    errs = tot = 0; bad = []
    for lid, l in L.items():
        a = signal.resample_poly(x[int((l["start"] - 0.05) * sr): int((l["end"] + 0.1) * sr)], 16000, sr).astype(np.float32)
        s_ = rec.create_stream(); s_.accept_waveform(16000, a); rec.decode_stream(s_)
        ref, hyp = norm(l["text"]), norm(s_.result.text); sm = difflib.SequenceMatcher(a=ref, b=hyp)
        e = max(len(ref), len(hyp)) - sum(b.size for b in sm.get_matching_blocks()); errs += e; tot += len(ref)
        if e > 1: bad.append((lid, s_.result.text))
    rep["asr_wer"] = round(errs / max(1, tot), 3); rep["asr_bad"] = bad
    open(f"{P}/work/bakeoff.jsonl", "a").write(json.dumps(rep) + "\n"); print(json.dumps(rep))
    return rep


if __name__ == "__main__":
    P = sys.argv[1]; eng = sys.argv[2]; a = sys.argv[3:]
    if eng == "score":
        for w in a: score(P, w)
        sys.exit()
    opt = dict(zip(a[::2], a[1::2])); tag = opt.get("--tag", eng)
    E = KokoroEng() if eng == "kokoro" else ChatterboxEng(opt["--ref"], opt.get("--lm", "q8"))
    out = synth(P, E, tag, line_speed=(eng == "kokoro" or opt.get("--speed") == "1"))
    del E; score(P, out)
