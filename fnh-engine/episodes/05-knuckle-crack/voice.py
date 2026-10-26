"""BODY FILES narrator (v3, owner-approved 26 Oct): mature British female = Kokoro bf_emma, en-gb, calm documentary pace.
Emotion comes from pace + gain (no pitch shifting, no voice blending). -> work/take.wav (24 kHz)"""
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

S = "/home/claude/reel-kit"
k = Kokoro(f"{S}/models/kokoro/kokoro-v1.0.onnx", f"{S}/models/kokoro/voices-v1.0.bin")
EMMA = k.get_voice_style("bf_emma")
LANG = "en-gb"
# mood: (speed, gain dB)
MOOD = {
    "hook":     (0.95, 1.0),    # opening question
    "calm":     (0.94, 0.0),    # explaining
    "emph":     (0.98, 2.5),    # the big reveal lines
    "soft":     (0.89, -3.5),   # low, intimate lines
    "question": (0.93, 0.5),
    "warm":     (0.93, 0.5),    # safe tip
}
# (line id, mood, [(phrase, pause_after_s)], gap_after_line_s)
# Split a line only at a real pause or sentence end — never cut a question or clause in half.
PLAN = [
    ("intro", "hook", [("Do you know what really happens when you crack your knuckles?", 0)], 0.75),
    ("myth", "calm", [("Most people think it's bones grinding together.", 0.45), ("It isn't.", 0)], 0.7),
    ("joint", "calm", [("Every knuckle is a joint: two bones, wrapped in a capsule,", 0)], 0.3),
    ("fluid", "calm", [("filled with a slippery liquid called synovial fluid.", 0)], 0.7),
    ("pull", "calm", [("When you bend or pull your finger, the two bones move apart,", 0)], 0.3),
    ("pressure", "soft", [("and the pressure inside the capsule suddenly drops.", 0)], 0.55),
    ("cavity", "emph", [("In a split second, a gas-filled pocket forms in the fluid,", 0.35), ("and that's the crack you hear!", 0)], 0.75),
    ("mri", "calm", [("In twenty fifteen, scientists filmed it happening inside an MRI scanner.", 0)], 0.65),
    ("wait", "calm", [("That's why you have to wait about half an hour to crack the same knuckle again.", 0)], 0.75),
    ("question", "question", [("So, does it cause arthritis?", 0)], 0.65),
    ("unger", "calm", [("One doctor cracked the knuckles of only his left hand,", 0.3), ("twice a day, for over sixty years.", 0)], 0.6),
    ("result", "emph", [("His X-rays?", 0.4), ("No arthritis in either hand.", 0)], 0.7),
    ("nuance", "soft", [("But one study did link frequent cracking to more hand swelling and a weaker grip.", 0)], 0.6),
    ("tip", "warm", [("So if your knuckles ever hurt or swell, talk to a doctor.", 0)], 0.75),
    ("loop", "soft", [("Now you know what really happens every time you crack your knuckles.", 0)], 0.0),
]


def trim(a, sr, th=-48):
    h = sr // 100
    n = len(a) // h
    db = 20 * np.log10(np.sqrt((a[: n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    on = np.where(db > th)[0]
    if not len(on):
        return a
    return a[max(0, on[0] - 2) * h: min(n, on[-1] + 4) * h]


out, sr = [np.zeros(int(0.10 * 24000), np.float32)], 24000
for lid, mood, phrases, gap in PLAN:
    spd, gdb = MOOD[mood]
    for txt, pz in phrases:
        a, sr = k.create(txt, voice=EMMA, speed=spd, lang=LANG)
        a = trim(a.astype(np.float32), sr) * (10 ** (gdb / 20))
        f = int(0.008 * sr)
        a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
        out += [a, np.zeros(int(pz * sr), np.float32)]
    out.append(np.zeros(int(gap * sr), np.float32))
x = np.concatenate(out)
x = x / (np.abs(x).max() + 1e-9) * 0.89
sf.write(f"{S}/english/work/take.wav", x, sr, subtype="FLOAT")
print("take", round(len(x) / sr, 2), "s")
