"""Local line-ending melody for TTS takes ("hybrid endings").
Moves pitch ONLY on the last word of lines marked "low" (fall) or "q" (rise); everything else stays the engine's original samples.
The last word is found with parakeet ASR timestamps; that slice is PSOLA-resynthesised (Praat) with a 0-st start, so it can be
cross-faded back into the untouched audio without a pitch jump. Made for Chatterbox-Turbo takes, whose reveal lines don't land low
(R&D 27 Oct 2026: global PSOLA on Chatterbox cost -0.23 UTMOS; this touches ~4 % of the audio).

  apply(x, sr, lines, ends, low=-4.0, q=0.0, gate=0.05) -> y   (lines = {id: {start, end, text}}, ends = {id: "low"|"q"|None};
  q rises are off by default: on Chatterbox they made questions sound worse; gate = max per-line UTMOS loss to keep a move)
CLI (lab): python3 end_contour.py <in.wav> <out.wav> <vo_lines.py> [low_st] [q_st]   (needs <in.wav>.json line map)"""
import os, re, numpy as np

R = os.environ.get("STUDIO", "/home/claude/studio")
_rec = None
FLOOR = float(os.environ.get("END_FLOOR", "85"))   # Hz
END_WIN = float(os.environ.get("END_WIN", "0.5"))   # s: the move starts at least this long before the last voiced frame


def _asr():
    global _rec
    if _rec is None:
        import sherpa_onnx
        d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
        _rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx",
                                                             joiner=f"{d}/joiner.int8.onnx", tokens=f"{d}/tokens.txt",
                                                             model_type="nemo_transducer", num_threads=2)
    return _rec


_utm = None


def _utmos(a, sr):
    """UTMOS22 (onnx, from setup.sh) on one line"""
    global _utm
    import onnxruntime as ort
    from scipy import signal
    if _utm is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        _utm = ort.InferenceSession(f"{R}/models/utmos/utmos22.onnx", so, providers=["CPUExecutionProvider"])
    a16 = signal.resample_poly(a, 16000, sr).astype(np.float32)
    k = (len(a16) - 400) // 320 + 1; k -= k % 2; a16 = a16[: 400 + 320 * (k - 1)]
    return float(_utm.run(None, {"wave": a16[None]})[0].ravel()[0])


def last_word_start(seg, sr):
    """time (s, relative to seg) where the last spoken word begins"""
    from scipy import signal
    a = signal.resample_poly(seg, 16000, sr).astype(np.float32); pad = np.zeros(8000, np.float32)
    s = _asr().create_stream(); s.accept_waveform(16000, np.concatenate([pad, a, pad])); _asr().decode_stream(s)
    starts = [ts - 0.5 for tk, ts in zip(s.result.tokens, s.result.timestamps) if tk.startswith(" ")]
    starts = [t for t in starts if t > 0.05]
    return max(0.0, starts[-1]) if starts else max(0.0, len(seg) / sr - 0.45)


def _move(seg, sr, t0, st, shape, cap=None):
    """PSOLA: pitch multiplied by 2^(st*ramp/12), ramp 0 at t0 -> 1 at the end of seg"""
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(seg.astype(np.float64), sr)
    m = call(snd, "To Manipulation", 0.01, 65, 400); pt = call(m, "Extract pitch tier")
    n = call(pt, "Get number of points"); new = call("Create PitchTier", "p", 0, snd.duration)
    pts = [(call(pt, "Get time from index", i), call(pt, "Get value at index", i)) for i in range(1, n + 1)]
    tv = max([t for t, _ in pts if t > t0] or [snd.duration])   # last voiced point: the move must be complete by then
    for t, f in pts:
        if shape == "fall":   # land early on the last word's vowel, then hold low (a nuclear fall, not a slide into silence)
            u = np.clip((t - t0) / max(0.06, 0.45 * (tv - t0)), 0, 1); r = u * u * (3 - 2 * u)
        else:                 # question: rise accelerating to the last voiced frame
            r = np.clip((t - t0) / max(0.08, tv - t0), 0, 1) ** 1.3
        if shape == "fall" and cap and f > cap: f = f * (cap / f) ** r   # Chatterbox sometimes ends a statement with uptalk: pull it down to the line median
        g = f * 2 ** (st * r / 12)
        if shape == "fall": g = max(g, min(f, FLOOR))   # never push below ~85 Hz: creak + pitch-tracker octave errors (lab 27 Oct)
        call(new, "Add point", t, g)
    call([new, m], "Replace pitch tier")
    return call(m, "Get resynthesis (overlap-add)").values[0][: len(seg)]


def apply(x, sr, lines, ends, low=-4.0, q=0.0, pre=0.12, xf=0.03, gate=0.05, log=None):
    log = [] if log is None else log
    y = x.astype(np.float64).copy()
    for lid, L in lines.items():
        e = ends.get(lid)
        if e not in ("low", "q") or (e == "q" and abs(q) < 0.01) or (e == "low" and abs(low) < 0.01): continue
        a0, a1 = int(L["start"] * sr), min(len(x), int((L["end"] + 0.03) * sr))
        tw = last_word_start(x[a0:a1], sr)
        import parselmouth
        f0 = parselmouth.Sound(x[a0:a1].astype(np.float64), sr).to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400).selected_array["frequency"]
        med = float(np.median(f0[f0 > 0])) if (f0 > 0).sum() > 10 else None
        if e == "low" and (f0 > 0).any():   # ASR word starts run ~0.2 s late -> also start the move END_WIN before the last voiced frame
            tv = (np.where(f0 > 0)[0][-1] + 1) * 0.01; tw = max(0.0, min(tw, tv - END_WIN))
        s0 = a0 + max(0, int((tw - pre) * sr))           # slice starts a little before the last word (0 st there)
        seg = x[s0:a1]
        mv = _move(seg, sr, (a0 + int(tw * sr) - s0) / sr, low if e == "low" else q, "fall" if e == "low" else "rise", med if e == "low" else None)
        n = int(xf * sr); w = np.ones(len(seg)); w[:n] = np.linspace(0, 1, n)
        cand = seg * (1 - w) + mv * w
        if gate is not None:   # keep the move only if this line's UTMOS doesn't drop by more than `gate` (lab 27 Oct: most lines lose < 0.04, a few lose 0.1-0.2)
            l0 = max(0, int((L["start"] - 0.05) * sr)); before = _utmos(y[l0:a1], sr); z = y[l0:a1].copy(); z[s0 - l0:] = cand
            after = _utmos(z, sr); log.append((lid, e, round(before, 3), round(after, 3)))
            if after < before - gate: continue
        y[s0:a1] = cand
    return y


if __name__ == "__main__":
    import sys, json, importlib.util, soundfile as sf
    inp, out, vl = sys.argv[1:4]; lo = float(sys.argv[4]) if len(sys.argv) > 4 else -4.0; qq = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    sp = importlib.util.spec_from_file_location("vl", vl); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    ends = {L[0]: L[7] for L in m.LINES}
    x, sr = sf.read(inp); meta = json.load(open(inp + ".json"))
    lg = []; y = apply(x, sr, meta["lines"], ends, lo, qq, gate=None if os.environ.get("END_GATE") == "off" else 0.05, log=lg)
    print("gate:", lg)
    sf.write(out, y.astype(np.float32), sr, subtype="FLOAT"); json.dump(meta, open(out + ".json", "w"))
    print("wrote", out)
