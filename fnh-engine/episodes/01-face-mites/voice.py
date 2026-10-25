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
# v2 (owner feedback 25 Oct): slower, clearer, more natural. Kokoro sounds best near speed 0.95 with little/no pitch
# shifting, so emotion comes mainly from the style blend + gain (loud highs / soft lows), not from speed or pitch.
MOOD = {
    "hook":    (mix(heart=0.90, bella=0.10), 0.97, 1.0, 0.0),
    "excited": (mix(heart=0.75, bella=0.25), 1.01, 2.5, 0.3),
    "curious": (mix(heart=1.0), 0.95, 0.0, 0.0),
    "whisper": (mix(heart=0.70, nicole=0.30), 0.88, -4.5, -0.3),
    "cheeky":  (mix(heart=0.85, bella=0.15), 0.98, 0.5, 0.0),
    "serious": (mix(heart=0.90, sarah=0.10), 0.93, -1.0, 0.0),
    "warm":    (mix(heart=1.0), 0.95, 0.5, 0.0),
}
# PLAN rules: split a line into phrases ONLY at a real dramatic pause ("…") or a sentence end — never cut a question
# or a clause in half (it breaks the intonation). Pauses: 0.30-0.45 s inside a line, 0.55-0.75 s between lines.


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
    ("hook", "hook", [("There are tiny bugs,", 0.16), ("living inside your face.", 0.26), ("Right now.", 0)], 0.42),
    ("name", "excited", [("They're called Demodex mites,", 0.14), ("and almost every adult has them!", 0)], 0.40),
    ("day", "curious", [("All day, they hide head-down in your pores,", 0.16), ("eating your face oil.", 0)], 0.46),
    ("night", "whisper", [("But at night,", 0.28), ("while you sleep,", 0.3), ("they crawl out.", 0)], 0.34),
    ("mate", "excited", [("To mate!", 0.16), ("On your face!", 0)], 0.46),
    ("party", "cheeky", [("They even use the sleep hormone your skin makes at night,", 0.12), ("to party till morning!", 0)], 0.40),
    ("wake", "excited", [("The second you wake up?", 0.16), ("They dive right back in!", 0)], 0.44),
    ("mom", "excited", [("And you got them,", 0.34), ("from your mom!", 0)], 0.50),
    ("itchy", "serious", [("Too many of them?", 0.2), ("Red, itchy skin.", 0)], 0.40),
    ("lashes", "warm", [("And they love your eyelashes,", 0.14), ("so always take your eye makeup off before bed.", 0)], 0.48),
    ("loop", "whisper", [("Because tonight,", 0.3), ("you're not sleeping alone.", 0)], 0.0),
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
