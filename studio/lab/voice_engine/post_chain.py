"""Apply make_vo.py's shipped post chain (EQ body/presence, voice_clean, short room) and optional global PSOLA slow-down
to a bake-off wav, so engines are compared 'as shipped'. Usage: post_chain.py <in.wav> <out.wav> [stretch=1.0]"""
import sys, os, json, shutil, numpy as np, soundfile as sf
from scipy import signal
R = os.environ.get("STUDIO", "/home/claude/studio"); sys.path.insert(0, f"{R}/lib")
import voice_clean
inp, out = sys.argv[1], sys.argv[2]; k = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
x, SR = sf.read(inp); x = x.astype(np.float64)
if abs(k - 1) > 1e-3:
    import parselmouth
    from parselmouth.praat import call
    s = parselmouth.Sound(x, SR); m = call(s, "To Manipulation", 0.01, 65, 400)
    dt = call("Create DurationTier", "d", 0, s.duration); call(dt, "Add point", 0, k); call([dt, m], "Replace duration tier")
    x = call(m, "Get resynthesis (overlap-add)").values[0]
def peq(f0, g, q):
    A = 10 ** (g / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a_ = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return signal.tf2sos(np.array(b) / a_[0], np.array(a_) / a_[0])
x = signal.sosfilt(peq(160, 1.0, 0.8), x); x = signal.sosfilt(peq(3100, 1.0, 1.0), x)
y = voice_clean.clean(x, 1.0, verbose=False).astype(np.float64)
rng = np.random.default_rng(5); n = int(0.32 * SR); tt = np.arange(n) / SR
ir = rng.standard_normal(n) * np.exp(-tt / 0.07); ir[: int(0.006 * SR)] = 0
for d_, g in ((0.009, 0.6), (0.014, 0.45), (0.021, 0.35), (0.029, 0.25)): ir[int(d_ * SR)] += g * 6
ir = signal.sosfilt(signal.butter(2, [250, 5500], "band", fs=SR, output="sos"), ir); ir /= np.sqrt((ir ** 2).sum())
wet = signal.fftconvolve(y, ir)[: len(y)]
y = y + wet * (np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-12)) * 10 ** (-21 / 20)
y = y / (np.abs(y).max() + 1e-9) * 10 ** (-1 / 20)
sf.write(out, y.astype(np.float32), SR, subtype="FLOAT")
m = json.load(open(inp + ".json"))
for l in m["lines"].values(): l["start"] = round(l["start"] * k, 3); l["end"] = round(l["end"] * k, 3)
json.dump(m, open(out + ".json", "w"))
