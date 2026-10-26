"""Local narrator voice (Kokoro blend) + expressive prosody (Praat PSOLA) -> natural, warm, clean VO + word timings.
Outputs: work/vo_flat.wav (before prosody), work/vo_raw.wav (dry, expressive), work/vo.wav (processed 48 kHz), work/align.json"""
import sys, json, re, difflib, numpy as np, soundfile as sf
from scipy import signal
import os
R = os.environ.get("STUDIO", "/home/claude/studio"); B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{R}/lib"); sys.path.insert(0, f"{B}/scripts")
from vo_lines import LINES
from kokoro_onnx import Kokoro
import voice_clean
from num2words import num2words
import parselmouth
from parselmouth.praat import call

SR = 48000; LEAD = 0.25
k = Kokoro(f"{R}/models/kokoro/kokoro-v1.0.onnx", f"{R}/models/kokoro/voices-v1.0.bin"); V = k.get_voice_style
import os
EW = float(os.environ.get("EW", "0.75")); _GT = os.environ.get("GT", "165"); BS = float(os.environ.get("BS", "0.6"))
_VS = os.environ.get("VOICES", "")   # e.g. "am_eric:0.75,am_fenrir:0.25" (overrides EW)
if _VS:
    VOICE = sum(float(w) * V(n) for n, w in (x.split(":") for x in _VS.split(",")))
else:
    VOICE = (1 - EW) * V("am_fenrir") + EW * V("am_eric")   # young, bright, energetic
CFG = {L[0]: L for L in LINES}

import os, hashlib
EXS = float(os.environ.get("EXS", "0.5")); BMP = float(os.environ.get("BMP", "0.8")); STR = float(os.environ.get("STR", "1.0"))
_key = hashlib.md5(repr([L[:3] for L in LINES] + [EW, os.environ.get("VOICES", "")]).encode()).hexdigest()
_cache = f"{B}/work/flat_{_key}.npz"
pieces, lines = [np.zeros(int(LEAD * SR), np.float32)], {}
t = LEAD
for lid, text, sp, pause, *_ in ([] if os.path.exists(_cache) else LINES):
    a, sr = k.create(text, voice=VOICE, speed=sp, lang="en-us", trim=True)
    a = signal.resample_poly(a.astype(np.float64), SR, sr).astype(np.float32)
    f = int(0.012 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    lines[lid] = dict(start=round(t, 3), end=round(t + len(a) / SR, 3), text=text)
    pieces.append(a); t += len(a) / SR
    pieces.append(np.zeros(int(pause * SR), np.float32)); t += pause
if os.path.exists(_cache):
    _z = np.load(_cache, allow_pickle=True); flat = _z["flat"]; lines = _z["lines"].item()
else:
    flat = np.concatenate(pieces + [np.zeros(int(0.3 * SR), np.float32)])
sf.write(f"{B}/work/vo_flat.wav", flat, SR, subtype="FLOAT")

# ---- word timings: parakeet ASR per line, matched to script words ----
import sherpa_onnx
d = f"{R}/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{d}/encoder.int8.onnx", decoder=f"{d}/decoder.int8.onnx",
                                                    joiner=f"{d}/joiner.int8.onnx", tokens=f"{d}/tokens.txt", model_type="nemo_transducer", num_threads=4)


def toks(w):
    w = w.lower().replace("-", " ").replace("…", " ").replace("’", "'")
    out = []
    for p in w.split():
        p = re.sub(r"[^a-z0-9']", "", p).strip("'")
        if not p: continue
        out += num2words(int(p)).replace("-", " ").split() if p.isdigit() else [p.replace("'", "")]
    return out


def align(raw, lines):
    words = []
    r16 = signal.resample_poly(raw, 16000, SR).astype(np.float32)
    for lid, text, *_ in LINES:
        L = lines[lid]; a0 = int((L["start"] - 0.05) * 16000); a1 = int((L["end"] + 0.05) * 16000)
        st = rec.create_stream(); st.accept_waveform(16000, np.concatenate([np.zeros(8000, np.float32), r16[a0:a1], np.zeros(8000, np.float32)])); rec.decode_stream(st)
        asr = []; first = True
        for tk, ts in zip(st.result.tokens, st.result.timestamps):
            tt_ = a0 / 16000 + max(0.0, ts - 0.5)
            if tk.startswith(" ") or first: asr.append([tk.strip(), tt_]); first = False
            else: asr[-1][0] += tk
        sc = [(tk, wi) for wi, w in enumerate(text.split()) for tk in toks(w)]
        at = [(tk, tt_) for w, tt_ in asr for tk in toks(w)]
        sm = difflib.SequenceMatcher(a=[x[0] for x in sc], b=[x[0] for x in at], autojunk=False)
        got = {}
        for blk in sm.get_matching_blocks():
            for q in range(blk.size): got.setdefault(sc[blk.a + q][1], at[blk.b + q][1])
        ws = text.split(); times = [got.get(i) for i in range(len(ws))]
        if times[0] is None: times[0] = L["start"]
        for i in range(len(times)):
            if times[i] is None:
                nxt = next((times[j] for j in range(i + 1, len(times)) if times[j] is not None), L["end"])
                times[i] = times[i - 1] + (nxt - times[i - 1]) / 2
        for i, w in enumerate(ws): words.append(dict(line=lid, w=w, t=round(max(L["start"], times[i]), 3)))
    return words


# ---- expressive prosody: wider pitch range, per-line register, stressed words, question rise / low settle ----
if os.path.exists(_cache): words0 = list(_z["words0"])
else:
    words0 = align(flat, lines); np.savez(_cache, flat=flat, lines=np.array(lines, dtype=object), words0=np.array(words0, dtype=object))
import copy; lines = copy.deepcopy(lines)
spans = []   # (line, word, start, end)
for lid, L in lines.items():
    ws = [w for w in words0 if w["line"] == lid]
    for i, w in enumerate(ws): spans.append((lid, w["w"], w["t"], ws[i + 1]["t"] if i + 1 < len(ws) else L["end"]))

snd = parselmouth.Sound(flat.astype(np.float64), SR)
pitch = snd.to_pitch_ac(0.01, 65, 15, False, 0.03, 0.45, 0.01, 0.35, 0.14, 400)
f0 = pitch.selected_array["frequency"]; tf = pitch.xs(); vo_ = f0 > 0
G = float(np.median(f0[vo_])); print("global median F0", round(G, 1))
GT = G * float(_GT[4:] or 1) if _GT.startswith("auto") else float(_GT)   # "auto" = keep the voice's own register
line_med = {}
for lid, L in lines.items():
    m = vo_ & (tf >= L["start"]) & (tf <= L["end"])
    line_med[lid] = float(np.median(f0[m])) if m.sum() > 5 else G


def rc(x, c, w):  # raised-cosine bump
    return 0.5 * (1 + np.cos(np.pi * np.clip((x - c) / w, -1, 1)))


manip = call(snd, "To Manipulation", 0.01, 65, 400)
ptier = call(manip, "Extract pitch tier")
npts = call(ptier, "Get number of points")
pts = np.array([[call(ptier, "Get time from index", i), call(ptier, "Get value at index", i)] for i in range(1, npts + 1)])
newp = call("Create PitchTier", "new", 0, snd.duration)
gain = np.zeros(len(flat)); dur_pts = []
for (tt, fv) in pts:
    lid = next((l for l, L in lines.items() if L["start"] - 0.05 <= tt <= L["end"] + 0.05), None)
    if lid is None: call(newp, "Add point", tt, fv); continue
    _, _, _, _, base, ex, stress, end = CFG[lid]
    ref = line_med[lid]; s = 12 * np.log2(fv / ref)
    s2 = s * (1 + (ex - 1) * EXS) + base * BS
    for (l2, w, ws_, we_) in spans:
        if l2 != lid: continue
        for st_ in stress:
            name, _, mode = st_.partition(":")
            if re.sub(r"\W", "", name.lower()) == re.sub(r"\W", "", w.lower()):
                ww = max(0.12, we_ - ws_)
                s2 += BMP * (-2.0 if mode == "dn" else 2.4) * rc(tt, ws_ + 0.4 * ww, 0.75 * ww)
    ws_l = [sp for sp in spans if sp[0] == lid][-1]
    if end == "q" and tt >= ws_l[2]: s2 += 4.5 * np.clip((tt - ws_l[2]) / max(0.1, ws_l[3] - ws_l[2]), 0, 1) ** 1.3
    if end == "low" and tt >= ws_l[2]: s2 -= 2.2 * np.clip((tt - ws_l[2]) / max(0.1, ws_l[3] - ws_l[2]), 0, 1)
    rel = np.clip(12 * np.log2(ref / G) + s2, -12.0, 13.0)
    call(newp, "Add point", tt, GT * 2 ** (rel / 12))
# loudness lift + length on stressed words
for (lid, w, ws_, we_) in spans:
    for st_ in CFG[lid][6]:
        name, _, mode = st_.partition(":")
        if re.sub(r"\W", "", name.lower()) != re.sub(r"\W", "", w.lower()): continue
        a0, a1 = int(ws_ * SR), int(we_ * SR); r_ = int(0.03 * SR)
        env = np.zeros(len(flat)); env[a0:a1] = 1
        env = np.convolve(env, np.ones(r_) / r_, "same")
        gain += env * (1.0 if mode == "dn" else 2.2)
        stretch = 1 + STR * (0.22 if mode == "dn" else 0.08)
        dur_pts += [(ws_ - 0.012, 1.0), (ws_, stretch), (we_ - 0.02, stretch), (we_ - 0.008, 1.0)]
x = flat * 10 ** (gain / 20)
snd2 = parselmouth.Sound(x.astype(np.float64), SR)
manip = call(snd2, "To Manipulation", 0.01, 65, 400)
call([newp, manip], "Replace pitch tier")
dtier = call("Create DurationTier", "dur", 0, snd.duration)
call(dtier, "Add point", 0.0, 1.0)
for tt, v in sorted(dur_pts): call(dtier, "Add point", max(0.001, tt), v)
call(dtier, "Add point", snd.duration, 1.0)
call([dtier, manip], "Replace duration tier")
out = call(manip, "Get resynthesis (overlap-add)")
raw = out.values[0].astype(np.float32)


_dp = sorted([(0.0, 1.0)] + [(max(0.001, a), b) for a, b in dur_pts] + [(snd.duration, 1.0)])
_g = np.arange(0, snd.duration + 0.001, 0.001); _dv = np.interp(_g, [p[0] for p in _dp], [p[1] for p in _dp])
_cum = np.concatenate([[0], np.cumsum((_dv[1:] + _dv[:-1]) / 2 * 0.001)])


def tmap(t0):  # old time -> new time through the duration tier (linear interpolation, as Praat does)
    return float(np.interp(t0, _g, _cum))


for lid, L in lines.items(): L["start"], L["end"] = round(tmap(L["start"]), 3), round(tmap(L["end"]), 3)
raw = raw / (np.abs(raw).max() + 1e-9) * 0.9
sf.write(f"{B}/work/vo_raw.wav", raw, SR, subtype="FLOAT")


# ---- warm, natural, clean chain ----
def peq(f0, g, q):
    A = 10 ** (g / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a_ = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.tf2sos(np.array(b) / a_[0], np.array(a_) / a_[0])


x = raw.astype(np.float64)
x = signal.sosfilt(peq(160, 1.0, 0.8), x)          # body
x = signal.sosfilt(peq(3100, 1.0, 1.0), x)         # presence / energy
y = voice_clean.clean(x, 1.0, verbose=True).astype(np.float64)
rng = np.random.default_rng(5); n = int(0.32 * SR); tt = np.arange(n) / SR
ir = rng.standard_normal(n) * np.exp(-tt / 0.07); ir[: int(0.006 * SR)] = 0
for d_, g in ((0.009, 0.6), (0.014, 0.45), (0.021, 0.35), (0.029, 0.25)): ir[int(d_ * SR)] += g * 6
ir = signal.sosfilt(signal.butter(2, [250, 5500], "band", fs=SR, output="sos"), ir); ir /= np.sqrt((ir ** 2).sum())
wet = signal.fftconvolve(y, ir)[: len(y)]
y = y + wet * (np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-12)) * 10 ** (-21 / 20)
y = y / (np.abs(y).max() + 1e-9) * 10 ** (-1 / 20)
sf.write(f"{B}/work/vo.wav", y.astype(np.float32), SR, subtype="FLOAT")

words = align(raw, lines)
json.dump(dict(lines=lines, words=words, dur=round(len(y) / SR, 3), LEAD=LEAD), open(f"{B}/work/align.json", "w"), indent=0)
print("VO duration", round(len(y) / SR, 2))
for lid, L in lines.items(): print(f"{lid:4s} {L['start']:6.2f}-{L['end']:6.2f}")
