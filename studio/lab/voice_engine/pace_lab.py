"""Pace lab (R&D 10 Nov 2026): re-time an already-made bake-off take, line by line, so pace can be compared on the SAME audio.
Usage: python3 pace_lab.py <bake.wav> <speed> [<speed> ...]
  For each speed s writes <bake>_s<speed>.wav (+ .json line map): every line time-stretched by 1/s with Praat PSOLA
  (pitch kept), in-line silences capped at GAP s first (what tools/trim_gaps.py does), between-line pauses unchanged.
  speed 1.0 = gap trim only (the fair baseline). Prints phrase rate = words / summed line durations after the trim.
Score the outputs with: python3 tools/tts_bakeoff.py <project> score <wav> ..."""
import sys, json, numpy as np, soundfile as sf, parselmouth
from parselmouth.praat import call

GAP, KEEP = 0.65, 0.42   # same defaults as tools/trim_gaps.py (cap in-line silences > 0.65 s at 0.42 s)


def trim_inline(a, sr):
    w = int(0.02 * sr); e = np.convolve(a ** 2, np.ones(w) / w, "same"); quiet = e < e.max() * 10 ** (-40 / 10)
    out, i, n = [], 0, len(a)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            seg = a[i:j]
            if (j - i) / sr > GAP and i > 0 and j < n:
                k = int(KEEP * sr); seg = np.concatenate([seg[:k // 2], seg[-(k - k // 2):]])
            out.append(seg); i = j
        else:
            j = i
            while j < n and not quiet[j]: j += 1
            out.append(a[i:j]); i = j
    return np.concatenate(out)


def stretch(a, sr, s):
    if abs(s - 1) < 1e-3: return a
    snd = parselmouth.Sound(a.astype(np.float64), sr); m = call(snd, "To Manipulation", 0.01, 65, 400)
    dt = call("Create DurationTier", "d", 0, snd.duration); call(dt, "Add point", 0, 1 / s); call([dt, m], "Replace duration tier")
    return call(m, "Get resynthesis (overlap-add)").values[0]


wav = sys.argv[1]; x, sr = sf.read(wav); meta = json.load(open(wav + ".json")); L = meta["lines"]
lv = sorted(L.items(), key=lambda kv: kv[1]["start"])
for s in map(float, sys.argv[2:]):
    pieces = [x[:int(lv[0][1]["start"] * sr)]]; t = lv[0][1]["start"]; out = {}
    for i, (lid, l) in enumerate(lv):
        seg = stretch(trim_inline(x[int(l["start"] * sr):int(l["end"] * sr)], sr), sr, s)
        out[lid] = dict(start=round(t, 3), end=round(t + len(seg) / sr, 3), text=l["text"]); pieces.append(seg); t += len(seg) / sr
        nxt = lv[i + 1][1]["start"] if i + 1 < len(lv) else l["end"] + 0.3
        gap = x[int(l["end"] * sr):int(nxt * sr)]; pieces.append(gap); t += len(gap) / sr
    y = np.concatenate(pieces); o = wav[:-4] + f"_s{s:.2f}.wav"
    sf.write(o, y.astype(np.float32), sr, subtype="FLOAT"); json.dump(dict(lines=out), open(o + ".json", "w"))
    nw = sum(len(l["text"].split()) for l in out.values()); sp_ = sum(l["end"] - l["start"] for l in out.values())
    print(f"{o}: phrase rate {nw / sp_ * 60:.1f} wpm, overall {nw / (len(y) / sr) * 60:.1f} wpm, {len(y) / sr:.1f} s")
