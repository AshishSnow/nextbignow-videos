"""Continuous English VO take -> pause-trimmed work/vo.wav + word times (parakeet ASR aligned to the script).
Usage: align_en.py take.(mp3|wav) [tempo]  -> work/vo.wav, work/align.json"""
import sys, json, re, subprocess, difflib
import numpy as np, soundfile as sf, sherpa_onnx
from num2words import num2words
from scipy import signal
sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from vo_lines import LINES

R = "/home/claude/reel-kit"
S = f"{R}/english"
src = sys.argv[1]
tempo = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
SR = 48000
af = "aresample=48000" + (f",rubberband=tempo={tempo}:pitchq=quality" if abs(tempo - 1) > 1e-3 else "")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-af", af, f"{S}/work/vo_raw.wav"], check=True)
a, _ = sf.read(f"{S}/work/vo_raw.wav", dtype="float32")
HOP = SR // 100


def env_db(x):
    n = len(x) // HOP
    return 20 * np.log10(np.sqrt((x[: n * HOP].reshape(n, HOP) ** 2).mean(1)) + 1e-9)


def runs(b):
    out, s = [], None
    for i, x in enumerate(b):
        if x and s is None: s = i
        if not x and s is not None: out.append([s, i]); s = None
    if s is not None: out.append([s, len(b)])
    return out


db = env_db(a)
v = db > max(-50.0, np.percentile(db, 95) - 36)
for s_, e_ in runs(v):
    if e_ - s_ < 4: v[s_:e_] = False
for s_, e_ in runs(~v):
    if e_ - s_ < 8 and s_ > 0 and e_ < len(v): v[s_:e_] = True
vr = runs(v)
# compress long pauses (keep natural breaths up to ~0.55 s)
pieces = [np.zeros(int(0.05 * SR), np.float32)]
for i, (s_, e_) in enumerate(vr):
    pieces.append(a[s_ * HOP:e_ * HOP])
    if i + 1 < len(vr):
        g0, g1 = e_, vr[i + 1][0]; gap = (g1 - g0) / 100
        tgt = min(gap if gap <= 0.55 else 0.45 + 0.25 * (gap - 0.55), 0.7)
        seg = a[g0 * HOP:g1 * HOP]
        if tgt < gap:
            n = int(tgt * SR); h = n // 2; seg = np.concatenate([seg[:h], seg[-(n - h):]])
        pieces.append(seg)
pieces.append(a[vr[-1][1] * HOP: vr[-1][1] * HOP + int(0.15 * SR)])
vo = np.concatenate(pieces).astype(np.float32)
sf.write(f"{S}/work/vo.wav", vo, SR, subtype="FLOAT")

# ---- ASR in chunks split at quiet points ----
d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx",
                                                    joiner=f"{d}/joiner.int8.onnx", tokens=f"{d}/tokens.txt",
                                                    model_type="nemo_transducer", num_threads=4)
a16 = signal.resample_poly(vo, 16000, SR).astype(np.float32)
h16 = 160
db16 = np.array([20 * np.log10(np.sqrt(np.mean(a16[i:i + h16] ** 2)) + 1e-9) for i in range(0, len(a16), h16)])
words, pos = [], 0
while pos < len(a16):
    end = min(len(a16), pos + 16000 * 18)
    if end < len(a16):
        lo, hi = (pos + 16000 * 12) // h16, end // h16
        end = (lo + int(np.argmin(db16[lo:hi]))) * h16
    pad = np.zeros(8000, np.float32)
    st = rec.create_stream(); st.accept_waveform(16000, np.concatenate([pad, a16[pos:end], pad])); rec.decode_stream(st)
    r = st.result
    first = True
    for tk, ts in zip(r.tokens, r.timestamps):
        tt = pos / 16000 + max(0.0, ts - 0.5)
        if tk.startswith(" ") or first:
            words.append([tk.strip(), tt]); first = False
        else:
            words[-1][0] += tk
    pos = end
print("ASR:", " ".join(w[0] for w in words))


def ntoks(word):
    w = word.lower().replace("%", " percent ").replace("-", " ").replace("…", " ").replace("’", "'")
    out = []
    for p in w.split():
        p = re.sub(r"[^a-z0-9.']", "", p).strip(".'")
        if not p:
            continue
        if re.fullmatch(r"\d{4}", p) and 1900 < int(p) < 2100:
            out += num2words(int(p), to="year").replace("-", " ").replace(",", "").split()
        elif re.fullmatch(r"\d+(\.\d+)?", p):
            out += num2words(float(p) if "." in p else int(p)).replace("-", " ").replace(",", "").split()
        else:
            out.append(p.replace("'", ""))
    return out


sc = []  # (token, line_idx, word_idx)
for li, (lid, text) in enumerate(LINES):
    for wi, w in enumerate(text.split()):
        for tk in ntoks(w):
            sc.append((tk, li, wi))
at = [(tk, t) for w, t in words for tk in ntoks(w)]
sm = difflib.SequenceMatcher(a=[x[0] for x in sc], b=[x[0] for x in at], autojunk=False)
got = {}
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        _, li, wi = sc[blk.a + k]
        got.setdefault((li, wi), at[blk.b + k][1])
allw = [(li, wi, w) for li, (lid, text) in enumerate(LINES) for wi, w in enumerate(text.split())]
times = [got.get((li, wi)) for li, wi, _ in allw]
print(f"matched {sum(t is not None for t in times)}/{len(times)} words")
if times[0] is None: times[0] = vr and 0.05 or 0.0
known = [i for i, t in enumerate(times) if t is not None]
for i in range(len(times)):
    if times[i] is None:
        lo = max(k for k in known if k < i); hi = [k for k in known if k > i]
        times[i] = times[lo] + ((times[hi[0]] - times[lo]) * (i - lo) / (hi[0] - lo) if hi else 0.3 * (i - lo))
# snap onsets forward to energy rise within +-90ms
db = env_db(vo)
for i in range(len(times)):
    c = int(round(times[i] * 100)); lo, hi = max(1, c - 6), min(len(db) - 1, c + 9)
    if hi > lo:
        rise = np.diff(db[lo - 1:hi])
        k = int(np.argmax(rise)); times[i] = (lo + k) / 100 if rise[k] > 4 else times[i]
for i in range(1, len(times)):
    times[i] = max(times[i], times[i - 1] + 0.07)
out_words = []
for (li, wi, w), t in zip(allw, times):
    out_words.append(dict(line=LINES[li][0], li=li, wi=wi, w=w, t=round(float(t), 3)))
vd = env_db(vo) > -45
lines = {}
for lid, _ in LINES:
    ws = [x for x in out_words if x["line"] == lid]
    nxt = [x["t"] for x in out_words if x["li"] == ws[-1]["li"] + 1]
    t_last = ws[-1]["t"]; lim = nxt[0] if nxt else len(vo) / SR
    e = int(t_last * 100) + 10
    while e < int(lim * 100) - 1 and e < len(vd) and vd[e]: e += 1
    lines[lid] = dict(start=ws[0]["t"], end=round(min(lim, e / 100 + 0.02), 3))
json.dump(dict(words=out_words, lines=lines, dur=round(len(vo) / SR, 3)), open(f"{S}/work/align.json", "w"), indent=0)
print(f"take {len(a)/SR:.2f}s -> vo {len(vo)/SR:.2f}s")
for lid, L in lines.items():
    print(f"{lid:8s} {L['start']:6.2f} - {L['end']:6.2f}")
