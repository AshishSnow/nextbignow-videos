"""ep 33: NO music (owner 9 Nov: he adds the track in-app). Writes a silent work/music.wav so the build chain stays the same; every musical sting lives in mix.py as foley."""
import os, numpy as np, soundfile as sf
B = os.environ.get("PROJ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_D = f"{B}/scripts"
exec(open(f"{_D}/anim_base.py").read().split("# ---------------- sets:")[0])
sf.write(f"{B}/work/music.wav", np.zeros((int((END + 1) * 48000), 2), np.float32), 48000)
print("music: none (silent placeholder)")
