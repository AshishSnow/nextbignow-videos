"""Motion test A: PAPER CUT-OUT stop-motion, 10.6 s of the Coca-Cola hook. Animated on twos (12 fps), every piece hand-placed
(tiny jitter per frame like real stop-motion), split-pin puppet, paper wipe between shots. Usage: python3 animcut.py OUT.mp4"""
import math, sys, wave, subprocess, numpy as np, skia, cv2
sys.path.insert(0, "/home/claude/studio/lab/styles")
from cutout import torn, path, Layer, circle_pts, rect_pts, noise_tex, F, W, H

FPS = 12; DUR = 10.6; SPLIT = 4.6
with wave.open("/home/claude/studio/projects/coke-dollar/work/mix.wav") as wf:
    sr = wf.getframerate(); ch = wf.getnchannels(); a = np.frombuffer(wf.readframes(int(sr * DUR) + sr), np.int16).astype(np.float32)
a = a.reshape(-1, ch).mean(1) / 32768; hop = sr // FPS
RMS = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(len(a) // hop)]); RMS = np.clip(RMS / np.percentile(RMS, 95), 0, 1)
GRAIN = 1 + noise_tex(H, W, 0.8, 0.05, 1) + noise_tex(H, W, 3, 0.03, 2)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); VIG = 1.08 - 0.45 * (((xx - W / 2) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
LIGHT = (GRAIN * VIG)[..., None]


def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)


def back(x, s=1.7): x = min(1, max(0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


class J:
    """stop-motion hands: every piece sits a hair differently on each new frame"""
    def __init__(s, n): s.r = np.random.default_rng(n)

    def __call__(s, c, x, y, rot=0.0, sc=1.0, amt=1.0):
        c.translate(x + s.r.normal(0, 1.1) * amt, y + s.r.normal(0, 1.1) * amt); c.rotate(rot + s.r.normal(0, 0.35) * amt); c.scale(sc, sc)


def puppet(L, j, x, y, s, armL, armR, mouth, blink, shirt=(232, 60, 60), legs=True):
    c = L.c; c.save(); j(c, x, y, sc=s)
    if legs:
        L.piece(rect_pts(-46, -150, 36, 150), (40, 44, 70), 40, lift=12); L.piece(rect_pts(10, -150, 36, 150), (40, 44, 70), 41, lift=12)
    for sgn, ang in ((-1, armL), (1, armR)):          # arms behind the body: shoulder pins
        c.save(); c.translate(sgn * 58, -330); c.rotate(-sgn * ang)
        L.piece(rect_pts(-16, 0, 32, 120), shirt, 46 + sgn, lift=10)
        c.translate(0, 112); c.rotate(-sgn * 10); L.piece(rect_pts(-14, 0, 28, 96), (240, 194, 150), 48 + sgn, lift=10)
        L.piece(circle_pts(0, 100, 22), (240, 194, 150), 50 + sgn, lift=6); c.restore()
        L.pin(sgn * 58, -322)
    L.piece([(-70, -360), (70, -360), (80, -140), (-80, -140)], shirt, 42, lift=14)
    L.piece(rect_pts(-18, -392, 36, 40), (232, 182, 140), 43, lift=6)
    L.piece(circle_pts(0, -470, 92, 100), (240, 194, 150), 44, lift=14)
    L.piece(circle_pts(0, -540, 96, 52, a0=180, a1=360) + [(96, -520), (-96, -520)], (60, 40, 30), 45, lift=6)
    for ex in (-32, 32):
        if blink: c.drawRect(skia.Rect.MakeXYWH(ex - 15, -472, 30, 5), skia.Paint(AntiAlias=True, Color=skia.Color(30, 20, 20)))
        else:
            c.drawCircle(ex, -470, 15, skia.Paint(AntiAlias=True, Color=skia.Color(250, 250, 246))); c.drawCircle(ex + 4, -468, 8, skia.Paint(AntiAlias=True, Color=skia.Color(20, 20, 30)))
    mh = 8 + 40 * mouth   # replacement mouths (paper pieces), like real cut-out animation
    L.piece(circle_pts(0, -412, 26 - 6 * mouth, mh / 2, n=30), (90, 20, 30), 51 + int(mouth * 4), lift=2, rim=False, rough=1)
    c.restore()


def shot1(L, n, t):
    c = L.c; j = J(n)
    c.clear(skia.Color(28, 70, 160))
    L.piece([(-40, -40), (1120, -40), (1120, 1150), (-40, 1210)], (38, 104, 214), 1, lift=16, rim=False)
    for i, (cx, cy, r) in enumerate(((180, 520, 90), (880, 430, 70))):
        c.save(); j(c, 40 * math.sin(t * 0.4 + i) * 0.5, 0)
        pts = []
        for k in range(5): pts += circle_pts(cx - 90 + k * 45, cy - (20 if k % 2 else 0), r * (0.7 + 0.15 * (k % 3)), n=20, a0=180, a1=360)
        L.piece(pts + [(cx + 120, cy + 30), (cx - 140, cy + 30)], (244, 246, 250), 10 + i, lift=8); c.restore()
    k = back(t / 0.5, 1.4)
    c.save(); j(c, 540, 1060, rot=t * 8, sc=max(0.01, k)); L.piece(circle_pts(0, 0, 380, n=60), (255, 196, 46), 5, lift=14)
    L.piece(circle_pts(0, 0, 310, n=60), (255, 150, 30), 6, lift=10); c.restore()
    L.piece([(-40, 1530), (1120, 1500), (1120, 2000), (-40, 2000)], (176, 128, 80), 3, lift=18)
    L.piece([(-40, 1500), (1120, 1472), (1120, 1540), (-40, 1566)], (206, 160, 104), 4, lift=8)
    # the bill drops in, swinging like paper on a string, then settles
    kb = ease((t - 0.1) / 0.6); sw = 14 * math.sin(t * 9) * (1 - ease((t - 0.3) / 1.2))
    c.save(); j(c, 600, 1020 - 1300 * (1 - kb), rot=-7 + sw, sc=0.92)
    L.piece(rect_pts(-330, -150, 660, 300), (120, 178, 110), 20, lift=22)
    L.piece(rect_pts(-300, -122, 600, 244), (164, 206, 146), 21, lift=4, rim=False, rough=1.4)
    L.piece(circle_pts(0, 0, 100, 112), (98, 150, 92), 22, lift=4)
    f = F("RubikMonoOne.ttf", 130); c.drawString("1", -f.measureText("1") / 2, 46, f, skia.Paint(AntiAlias=True, Color=skia.Color(236, 244, 226)))
    for sx in (-1, 1):
        L.piece(circle_pts(sx * 230, -70, 40), (98, 150, 92), 23 + sx, lift=3)
        f2 = F("RubikMonoOne.ttf", 46); c.drawString("1", sx * 230 - 16, -52, f2, skia.Paint(AntiAlias=True, Color=skia.Color(236, 244, 226)))
    c.restore()
    kbt = back((t - 1.0) / 0.4)
    c.save(); j(c, 880 + 400 * (1 - kbt), 1515, rot=6 + 20 * (1 - kbt))
    bot = [(-26, -330), (26, -330), (30, -250), (64, -170), (70, 0), (-70, 0), (-64, -170), (-30, -250)]
    L.piece(bot, (120, 40, 30), 30, lift=16); L.piece(rect_pts(-70, -150, 140, 70), (250, 246, 236), 31, lift=4, rough=1.6)
    L.piece(rect_pts(-30, -362, 60, 34), (210, 40, 40), 32, lift=4); c.restore()
    up = ease((t - 2.15) / 0.2)
    puppet(L, j, 250, 1530 - 30 * back((t - 2.15) / 0.3) * (1 - ease((t - 2.5) / 0.3)), 1.0, 25 + 125 * up + 8 * math.sin(t * 7), 25 + 125 * up + 8 * math.sin(t * 7 + 1),
           RMS[min(n, len(RMS) - 1)], (n % 31) in (0, 1))
    if t > 0.35:
        s_ = back((t - 0.35) / 0.25, 2.4); c.save(); j(c, 540, 420, rot=-3, sc=s_); L.word("COCA-COLA SOLD", 0, 0, 64, (30, 30, 40), (250, 246, 236), 0, 60); c.restore()
    if t > 2.15:
        s_ = back((t - 2.15) / 0.25, 2.6); c.save(); j(c, 560, 580, rot=2, sc=s_); L.word("FOR $1", 0, 0, 130, (255, 255, 255), (224, 40, 48), 0, 61); c.restore()


def glass(L, j, x, y):
    c = L.c; c.save(); j(c, x, y)
    L.piece([(-60, -200), (60, -200), (48, 0), (-48, 0)], (214, 232, 244), 70, lift=8)
    L.piece([(-54, -150), (54, -150), (46, -6), (-46, -6)], (110, 50, 22), 71, lift=2, rim=False, rough=1.4)
    L.piece(rect_pts(-46, -200, 92, 14), (240, 220, 200), 72, lift=2, rim=False, rough=1)
    c.save(); c.rotate(14); L.piece(rect_pts(10, -300, 14, 170), (250, 250, 250), 73, lift=6); L.piece(rect_pts(10, -300, 14, 22), (224, 40, 48), 74, lift=1, rim=False); c.restore()
    c.restore()


def shot2(L, n, t):
    c = L.c; j = J(n + 999)
    c.clear(skia.Color(214, 100, 24))
    L.piece([(-40, -40), (1120, -40), (1120, 1220), (-40, 1180)], (250, 140, 40), 81, lift=16, rim=False)
    for i in range(7):   # striped paper awning
        L.piece([(-20 + i * 160, 740), (140 + i * 160, 740), (140 + i * 160, 860), (-20 + i * 160, 860)], (250, 246, 236) if i % 2 else (224, 40, 48), 90 + i, lift=10)
    c.save(); j(c, 540, 1040, rot=-t * 6); L.piece(circle_pts(0, 0, 250, n=60), (255, 236, 200), 82, lift=10); c.restore()
    wave_ = 30 + 70 * max(0, math.sin(t * 7)) * ease((t - 2.5) / 0.3)
    puppet(L, j, 300, 1520, 0.95, 20, wave_ + 30, RMS[min(n, len(RMS) - 1)], (n % 29) in (0, 1), shirt=(250, 250, 246), legs=False)
    c.save(); j(c, 300, 1230); L.piece(circle_pts(0, -40, 70, 34, a0=180, a1=360) + [(70, -40), (-70, -40)], (250, 250, 246), 83, lift=6); c.restore()   # soda-jerk cap
    L.piece([(40, 1300), (1040, 1290), (1040, 1700), (40, 1710)], (130, 64, 36), 84, lift=20)
    for i in range(5): L.piece(rect_pts(80 + i * 196, 1380, 150, 260), (150, 80, 46), 85 + i, lift=4, rough=1.6)
    L.piece([(20, 1250), (1060, 1240), (1060, 1310), (20, 1320)], (246, 242, 234), 86, lift=12)
    c.save(); j(c, 560, 1250); L.piece(rect_pts(-28, -260, 56, 260), (176, 180, 190), 87, lift=10)
    for sx in (-1, 1): L.piece([(0, -230), (sx * 110, -210), (sx * 110, -180), (0, -200)], (196, 200, 210), 88 + sx, lift=6)
    c.restore()
    for i, x in enumerate((750, 900)):
        kg = back((t - 0.9 - i * 0.3) / 0.35)
        if kg > 0: glass(L, j, x, 1250 - 400 * (1 - kg))
    if t > 0.1:
        s_ = back((t - 0.1) / 0.3, 2.4); c.save(); j(c, 540, 470, rot=-2, sc=s_); L.word("1899", 0, 0, 150, (255, 255, 255), (30, 60, 150), 0, 62); c.restore()
    if t > 3.2:
        s_ = back((t - 3.2) / 0.3, 2.4); c.save(); j(c, 560, 640, rot=2, sc=s_); L.word("SODA FOUNTAINS", 0, 0, 70, (150, 30, 20), (250, 246, 236), 0, 63); c.restore()


def frame(n):
    t = n / FPS; surf = skia.Surface(W, H); L = Layer(surf.getCanvas())
    if t < SPLIT: shot1(L, n, t)
    else: shot2(L, n, t - SPLIT)
    img = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255
    if SPLIT - 0.35 <= t < SPLIT:   # paper wipe: the next sheet is slid in over the old one by hand
        p = ease((t - (SPLIT - 0.35)) / 0.35); s2 = skia.Surface(W, H); L2 = Layer(s2.getCanvas()); shot2(L2, n, 0.0)
        nxt = s2.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255
        x = int(W * (1 - p)); img[:, x:] = nxt[:, :W - x]
        if 0 < x < W: img[:, max(0, x - 30):x] *= np.linspace(1, 0.6, min(30, x))[None, :, None]
    return (np.clip(img * LIGHT, 0, 1) * 255).astype(np.uint8)


if __name__ == "__main__":
    out = sys.argv[1]; N = int(DUR * FPS)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "12", "-i", "-",
                            "-ss", "0", "-t", str(DUR), "-i", "/home/claude/studio/projects/coke-dollar/work/mix.wav",
                            "-vf", "fps=24,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "256k",
                            "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for n in range(N): enc.stdin.write(frame(n).tobytes())
    enc.stdin.close(); enc.wait(); print("done", out)
