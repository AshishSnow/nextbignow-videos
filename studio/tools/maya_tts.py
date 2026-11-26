"""Maya1 (Apache-2.0, maya-research/maya1) voice-designed TTS on CPU: llama.cpp GGUF Q4_K_M + SNAC-24k ONNX decoder.
The voice is designed from a text description (no reference speaker, no cloning).
usage: python3 maya_tts.py "<description>" "<text>" out.wav [seed]"""
import sys, os, time, numpy as np, soundfile as sf
import onnxruntime as ort
from llama_cpp import Llama

M = os.environ.get('MAYA_DIR', '/home/claude/studio/models/maya1')
CODE_START, CODE_END, OFF = 128257, 128258, 128266
SOH, EOH, SOA, BOS, EOT = 128259, 128260, 128261, 128000, 128009
_llm = None; _dec = None


def llm():
    global _llm
    if _llm is None:
        _llm = Llama(model_path=f'{M}/maya1.Q4_K_M.gguf', n_ctx=4096, n_threads=os.cpu_count(), n_batch=256, verbose=False, logits_all=False)
    return _llm


def dec():
    global _dec
    if _dec is None: _dec = ort.InferenceSession(f'{M}/snac_decoder.onnx', providers=['CPUExecutionProvider'])
    return _dec


def prompt_ids(desc, text):
    L = llm(); body = L.tokenize(f'<description="{desc}"> {text}'.encode(), add_bos=False, special=True)
    return [SOH, BOS] + body + [EOT, EOH, SOA, CODE_START]


def generate(desc, text, seed=0, temp=0.4, top_p=0.9, rep=1.1, max_tokens=None):
    L = llm(); ids = prompt_ids(desc, text)
    n_words = len(text.split()); max_tokens = max_tokens or int(7 * 12 * (n_words / 2.2 + 3))
    L.reset(); L.set_seed(seed) if hasattr(L, 'set_seed') else None
    out = []
    for tok in L.generate(ids, temp=temp, top_p=top_p, top_k=50, repeat_penalty=rep, reset=True):
        if tok == CODE_END or len(out) >= max_tokens: break
        out.append(tok)
    codes = [t for t in out if OFF <= t <= 156937]
    return decode(codes)


def decode(codes):
    f = len(codes) // 7; codes = codes[:f * 7]
    if f == 0: return np.zeros(2400, np.float32)
    l1, l2, l3 = [], [], []
    for i in range(f):
        s = [(c - OFF) % 4096 for c in codes[i * 7:(i + 1) * 7]]
        l1.append(s[0]); l2 += [s[1], s[4]]; l3 += [s[2], s[3], s[5], s[6]]
    o = dec().run(None, {'audio_codes.0': np.array([l1], np.int64), 'audio_codes.1': np.array([l2], np.int64), 'audio_codes.2': np.array([l3], np.int64)})[0]
    return o.reshape(-1).astype(np.float32)


if __name__ == '__main__':
    d, t, out = sys.argv[1], sys.argv[2], sys.argv[3]; seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    t0 = time.time(); a = generate(d, t, seed); sf.write(out, a, 24000)
    print(f'{len(a) / 24000:.2f}s audio in {time.time() - t0:.1f}s')
