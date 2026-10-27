"""Chatterbox-Turbo (Resemble AI, MIT licence) on onnxruntime CPU — no torch.
Model: huggingface.co/ResembleAI/chatterbox-turbo-ONNX (setup.sh downloads embed_tokens fp32, language_model q4, conditional_decoder fp32).
q4 language model = 7x faster than q8 (RTF ~1.8 vs ~12.7 on 2 CPUs) at the same UTMOS (R&D 27 Oct 2026).
Voice = a precomputed speaker conditioning (.cbcond.npz) made from a SYNTHETIC reference (our Kokoro narrator) — never a real person.
The model copies the reference's pace and melody: a slow, expressive reference gives ~165 wpm with no time-stretching.
Greedy decoding with repetition penalty 1.2, as in the official model card (deterministic: same text -> same audio)."""
import os, numpy as np

R = os.environ.get("STUDIO", "/home/claude/studio")
SR = 24000
START, STOP, SIL, KVH, HD = 6561, 6562, 4299, 16, 64


def _trim(a, db=-42, pad=0.03):
    w = int(0.01 * SR); e = np.convolve(a ** 2, np.ones(w) / w, "same"); idx = np.where(e > e.max() * 10 ** (db / 10))[0]
    return a if not len(idx) else a[max(0, idx[0] - int(pad * SR)): idx[-1] + int(pad * SR)]


class Turbo:
    def __init__(self, cond, lm="q4", threads=2, rep=1.2):
        """cond = path to a .cbcond.npz (speaker conditioning) or a reference .wav (needs speech_encoder.onnx; result cached next to it)."""
        import onnxruntime as ort
        from tokenizers import Tokenizer
        d = f"{R}/models/cbturbo"; so = ort.SessionOptions(); so.intra_op_num_threads = threads
        S = lambda n: ort.InferenceSession(f"{d}/{n}.onnx", so, providers=["CPUExecutionProvider"])
        self.embed = S("embed_tokens"); self.lm = S("language_model" + {"q8": "_quantized", "q4": "_q4", "fp32": ""}[lm]); self.dec = S("conditional_decoder")
        self.tok = Tokenizer.from_file(f"{d}/tokenizer.json"); self.rep = rep
        if not cond.endswith(".npz"):
            npz = os.path.splitext(cond)[0] + ".cbcond.npz"
            if not os.path.exists(npz):
                import soundfile as sf
                from scipy import signal
                a, sr = sf.read(cond); a = a if a.ndim == 1 else a.mean(1)
                a = signal.resample_poly(a, SR, sr).astype(np.float32)[None]
                c = S("speech_encoder").run(None, {"audio_values": a})
                np.savez_compressed(npz, cond_emb=c[0], prompt_token=c[1], spk=c[2], feat=c[3])
            cond = npz
        z = np.load(cond); self.cond = [z[k] for k in ("cond_emb", "prompt_token", "spk", "feat")]

    def say(self, text):
        """-> float64 mono @ 24 kHz, leading/trailing silence trimmed"""
        cond_emb, prompt_token, spk, feat = self.cond
        x = np.array([self.tok.encode(text).ids], np.int64); gen = np.array([[START]], np.int64)
        for i in range(60 + 50 * len(text.split())):
            emb = self.embed.run(None, {"input_ids": x})[0]
            if i == 0:
                emb = np.concatenate((cond_emb, emb), 1); n = emb.shape[1]
                pkv = {j.name: np.zeros([1, KVH, 0, HD], np.float16 if j.type == "tensor(float16)" else np.float32)
                       for j in self.lm.get_inputs() if "past_key_values" in j.name}
                am = np.ones((1, n), np.int64); pos = np.arange(n, dtype=np.int64)[None]
            logits, *pres = self.lm.run(None, dict(inputs_embeds=emb, attention_mask=am, position_ids=pos, **pkv))
            lg = logits[:, -1, :].copy(); sc = np.take_along_axis(lg, gen, 1)
            np.put_along_axis(lg, gen, np.where(sc < 0, sc * self.rep, sc / self.rep), 1)
            x = np.argmax(lg, -1, keepdims=True).astype(np.int64); gen = np.concatenate((gen, x), -1)
            if x[0, 0] == STOP: break
            am = np.concatenate([am, np.ones((1, 1), np.int64)], 1); pos = pos[:, -1:] + 1
            for j, k in enumerate(pkv): pkv[k] = pres[j]
        sp = gen[:, 1:-1] if gen[0, -1] == STOP else gen[:, 1:]
        tok = np.concatenate([prompt_token, sp, np.full((1, 3), SIL, np.int64)], 1)
        wav = self.dec.run(None, dict(speech_tokens=tok, speaker_embeddings=spk, speaker_features=feat))[0].squeeze()
        return _trim(wav.astype(np.float64))
