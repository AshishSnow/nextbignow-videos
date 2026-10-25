"""NESSA voice (Kokoro, local): per-phrase delivery with blended styles for excited / whisper moments.
-> work/take.wav (24 kHz)"""
import sys, subprocess, tempfile, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

S = "/home/claude/reel-kit"
k = Kokoro(f"{S}/models/kokoro/kokoro-v1.0.onnx", f"{S}/models/kokoro/voices-v1.0.bin")
V = {n: k.get_voice_style(n) for n in ("af_heart", "af_bella", "af_nicole", "af_sarah")}


def mix(**w):
    t = sum(w.values())
    return sum(V["af_" + n] * (x / t) for n, x in w.items()).astype(np.float32)


# style, speed, gain dB, pitch semitones (formant-preserving)
MOOD = {
    "hook":    (mix(heart=0.75, bella=0.15, nicole=0.10), 1.04, 1.0, 0.6),
    "excited": (mix(heart=0.55, bella=0.45), 1.14, 3.0, 1.3),
    "curious": (mix(heart=0.85, bella=0.15), 1.06, 0.5, 0.3),
    "whisper": (mix(heart=0.40, nicole=0.60), 0.86, -6.0, -0.9),
    "cheeky":  (mix(heart=0.65, bella=0.35), 1.08, 1.0, 0.6),
    "serious": (mix(heart=0.85, sarah=0.15), 0.95, -1.0, -0.5),
    "warm":    (mix(heart=0.85, bella=0.15), 1.05, 0.5, 0.2),
}


def pitch(a, sr, st):
    if abs(st) < 0.05:
        return a
    d = tempfile.mkdtemp()
    sf.write(f"{d}/i.wav", a, sr, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/i.wav", "-af",
                    f"rubberband=pitch={2 ** (st / 12):.5f}:formant=preserved:pitchq=quality", f"{d}/o.wav"], check=True)
    b, _ = sf.read(f"{d}/o.wav", dtype="float32")
    return b
# (line id, mood, [(phrase, pause_after_s)], gap_after_line_s)
PLAN = [
    ("intro", "hook", [("Do you know your red lipstick", 0.06), ("might be made of bugs?", 0)], 0.40),
    ("name", "excited", [("It's called carmine,", 0.16), ("and it comes from tiny insects called cochineal!", 0)], 0.40),
    ("cactus", "curious", [("They live on prickly pear cactus,", 0.16), ("mostly in Peru.", 0)], 0.42),
    ("crush", "whisper", [("Only the females are used,", 0.26), ("dried,", 0.28), ("and crushed.", 0)], 0.36),
    ("count", "excited", [("Seventy thousand bugs,", 0.18), ("for just one pound of dye!", 0)], 0.46),
    ("wait", "cheeky", [("But wait,", 0.2), ("it's not just lipstick.", 0.14), ("It's in some yogurt, candy and ice cream too!", 0)], 0.42),
    ("allergy", "serious", [("And for a few people,", 0.18), ("it can cause allergic reactions.", 0)], 0.40),
    ("tip", "warm", [("So check the label for carmine,", 0.12), ("cochineal extract,", 0.12), ("or E one twenty.", 0)], 0.46),
    ("loop", "whisper", [("And next time you put on red lipstick,", 0.3), ("ask yourself.", 0)], 0.0),
]


def trim(a, sr, th=-48):
    h = sr // 100
    n = len(a) // h
    db = 20 * np.log10(np.sqrt((a[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    on = np.where(db > th)[0]
    if not len(on):
        return a
    s, e = max(0, on[0] - 2) * h, min(n, on[-1] + 4) * h
    return a[s:e]


out, sr = [np.zeros(int(0.08 * 24000), np.float32)], 24000
for lid, mood, phrases, gap in PLAN:
    style, spd, gdb, st = MOOD[mood]
    for txt, pz in phrases:
        a, sr = k.create(txt, voice=style, speed=spd, lang="en-us")
        a = trim(pitch(a.astype(np.float32), sr, st), sr) * (10 ** (gdb / 20))
        f = int(0.008 * sr)
        a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        out += [a, np.zeros(int(pz * sr), np.float32)]
    out.append(np.zeros(int(gap * sr), np.float32))
x = np.concatenate(out)
x = x / (np.abs(x).max() + 1e-9) * 0.89
sf.write(f"{S}/english/work/take.wav", x, sr, subtype="FLOAT")
print("take", round(len(x) / sr, 2), "s")
