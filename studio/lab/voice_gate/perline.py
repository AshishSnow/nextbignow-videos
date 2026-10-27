"""Per-line UTMOS of a VO file. Usage: perline.py <project> <wav> [flat]  (flat -> line map from the make_vo cache npz)"""
import sys, os, json, glob, numpy as np, soundfile as sf
sys.path.insert(0, "/home/claude/nextbignow-videos/studio/tools"); import tts_bakeoff as tb
P, wav = sys.argv[1], sys.argv[2]
x, sr = sf.read(wav); x = x if x.ndim == 1 else x.mean(1)
if len(sys.argv) > 3:
    z = np.load(max(glob.glob(f"{P}/work/flat_*.npz"), key=os.path.getmtime), allow_pickle=True); L = z["lines"].item()
else: L = json.load(open(f"{P}/work/align.json"))["lines"]
out = {lid: round(tb.utmos(x[int((l["start"] - 0.05) * sr): int((l["end"] + 0.1) * sr)], sr), 3) for lid, l in L.items()}
print(json.dumps(out))
