"""Style test A: PAPER CUT-OUT stop-motion (construction paper, torn edges, split-pin puppets, real shadows). One frame of the Coca-Cola hook."""
import math, numpy as np, skia, cv2, sys
W, H = 1080, 1920
FD = "/home/claude/studio/fonts/ttf"
rng = np.random.default_rng(4)


def F(name, size): return skia.Font(skia.Typeface.MakeFromFile(f"{FD}/{name}"), size)


def noise_tex(h, w, sig, amp, seed):
    r = np.random.default_rng(seed); n = cv2.GaussianBlur(r.normal(0, 1, (h, w)).astype(np.float32), (0, 0), sig)
    return n / (np.abs(n).max() + 1e-6) * amp


def torn(pts, seed, amp=3.0, step=6):
    """resample a closed outline and roughen it like cut/torn paper"""
    r = np.random.default_rng(seed); out = []
    P = pts + [pts[0]]
    for (x0, y0), (x1, y1) in zip(P, P[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(1, int(d / step))
        nx, ny = (-(y1 - y0) / (d + 1e-6), (x1 - x0) / (d + 1e-6))
        for i in range(n):
            k = i / n; o = r.normal(0, amp) * 0.6
            out.append((x0 + (x1 - x0) * k + nx * o, y0 + (y1 - y0) * k + ny * o))
    return out


def path(pts):
    p = skia.Path(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; p.close(); return p


def circle_pts(cx, cy, rx, ry=None, n=90, a0=0, a1=360):
    ry = ry or rx
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n)]


def rect_pts(x, y, w, h, r=0):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


class Layer:
    """every piece of paper: colour, outline; drawn with a lifted shadow, a white torn core rim and grain"""
    def __init__(s, c): s.c = c

    def piece(s, pts, col, seed=0, lift=10, rim=True, rough=2.4, grain=True):
        P = torn(pts, seed, rough); p = path(P)
        sh = skia.Paint(AntiAlias=True, Color=skia.Color(30, 20, 10), Alphaf=0.38)
        sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, lift * 0.7))
        s.c.save(); s.c.translate(lift * 0.55, lift * 0.9); s.c.drawPath(p, sh); s.c.restore()
        if rim:   # the white fibre core of torn paper, peeking out on one side
            rp = skia.Paint(AntiAlias=True, Color=skia.Color(250, 246, 236))
            s.c.save(); s.c.translate(-1.6, -1.8); s.c.drawPath(p, rp); s.c.restore()
        fp = skia.Paint(AntiAlias=True, Color=skia.Color(*col)); s.c.drawPath(p, fp)
        # soft top light across the piece
        b = p.computeTightBounds()
        g = skia.GradientShader.MakeLinear([skia.Point(b.left(), b.top()), skia.Point(b.left(), b.bottom())],
                                           [skia.Color4f(1, 1, 1, 0.10), skia.Color4f(0, 0, 0, 0.10)])
        gp = skia.Paint(AntiAlias=True); gp.setShader(g); s.c.drawPath(p, gp)
        return p

    def pin(s, x, y):   # brass split pin at a puppet joint
        s.c.drawCircle(x + 2, y + 3, 9, skia.Paint(AntiAlias=True, Color=skia.Color(0, 0, 0), Alphaf=0.35, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)))
        g = skia.GradientShader.MakeRadial(skia.Point(x - 3, y - 3), 10, [skia.Color(255, 236, 160), skia.Color(176, 126, 40)])
        p = skia.Paint(AntiAlias=True); p.setShader(g); s.c.drawCircle(x, y, 8, p)

    def word(s, text, x, y, size, col, bg, tilt, seed, font="RubikMonoOne.ttf"):
        """cut-out word: letters printed on a torn paper strip"""
        f = F(font, size); w = f.measureText(text)
        s.c.save(); s.c.translate(x, y); s.c.rotate(tilt)
        s.piece(rect_pts(-w / 2 - 34, -size * 0.95, w + 68, size * 1.35), bg, seed, lift=12, rough=3)
        s.c.drawString(text, -w / 2, size * 0.18, f, skia.Paint(AntiAlias=True, Color=skia.Color(*col)))
        s.c.restore()


def frame():
    surf = skia.Surface(W, H); c = surf.getCanvas(); L = Layer(c)
    # backdrop: deep blue construction paper + a lighter sky sheet + a kraft-paper counter
    c.clear(skia.Color(28, 70, 160))
    L.piece([(-40, -40), (1120, -40), (1120, 1150), (-40, 1210)], (38, 104, 214), 1, lift=16, rim=False)
    for i, (cx, cy, r) in enumerate(((180, 520, 90), (880, 430, 70))):   # paper clouds
        pts = []
        for k in range(5): pts += circle_pts(cx - 90 + k * 45, cy - (20 if k % 2 else 0), r * (0.7 + 0.15 * (k % 3)), n=20, a0=180, a1=360)
        L.piece(pts + [(cx + 120, cy + 30), (cx - 140, cy + 30)], (244, 246, 250), 10 + i, lift=8)
    # the big sun-burst circle behind the hero object
    L.piece(circle_pts(540, 1060, 380), (255, 196, 46), 5, lift=14)
    ray = []
    for k in range(24):
        a = math.radians(k * 15); r_ = 430 if k % 2 == 0 else 372
        ray.append((540 + r_ * math.cos(a), 1010 + r_ * math.sin(a)))
    c.save(); c.translate(0, 0)
    L.piece(circle_pts(540, 1060, 310), (255, 150, 30), 6, lift=10)
    c.restore()
    # kraft counter top
    L.piece([(-40, 1530), (1120, 1500), (1120, 2000), (-40, 2000)], (176, 128, 80), 3, lift=18)
    L.piece([(-40, 1500), (1120, 1472), (1120, 1540), (-40, 1566)], (206, 160, 104), 4, lift=8)
    # the dollar bill (green paper, layered details), tilted
    c.save(); c.translate(600, 1020); c.rotate(-7); c.scale(0.92, 0.92)
    L.piece(rect_pts(-330, -150, 660, 300), (120, 178, 110), 20, lift=22)
    L.piece(rect_pts(-300, -122, 600, 244), (164, 206, 146), 21, lift=4, rim=False, rough=1.4)
    L.piece(circle_pts(0, 0, 100, 112), (98, 150, 92), 22, lift=4)
    f = F("RubikMonoOne.ttf", 130); c.drawString("1", -f.measureText("1") / 2, 46, f, skia.Paint(AntiAlias=True, Color=skia.Color(236, 244, 226)))
    for sx in (-1, 1):
        L.piece(circle_pts(sx * 230, -70, 40), (98, 150, 92), 23 + sx, lift=3)
        f2 = F("RubikMonoOne.ttf", 46); c.drawString("1", sx * 230 - 16, -52, f2, skia.Paint(AntiAlias=True, Color=skia.Color(236, 244, 226)))
    c.restore()
    # a plain soda bottle (generic shape, red paper + white label strip)
    c.save(); c.translate(880, 1515); c.rotate(6)
    bot = [(-26, -330), (26, -330), (30, -250), (64, -170), (70, 0), (-70, 0), (-64, -170), (-30, -250)]
    L.piece(bot, (120, 40, 30), 30, lift=16)
    L.piece(rect_pts(-70, -150, 140, 70), (250, 246, 236), 31, lift=4, rough=1.6)
    L.piece(rect_pts(-30, -362, 60, 34), (210, 40, 40), 32, lift=4)
    c.restore()
    # split-pin paper puppet (our own guy): head, torso, jointed arms, legs
    px, py = 250, 1530
    c.save(); c.translate(px, py)
    L.piece(rect_pts(-46, -150, 36, 150), (40, 44, 70), 40, lift=12); L.piece(rect_pts(10, -150, 36, 150), (40, 44, 70), 41, lift=12)
    L.piece([(-70, -360), (70, -360), (80, -140), (-80, -140)], (232, 60, 60), 42, lift=14)            # red jumper
    L.piece(rect_pts(-18, -392, 36, 40), (232, 182, 140), 43, lift=6)                                 # neck
    L.piece(circle_pts(0, -470, 92, 100), (240, 194, 150), 44, lift=14)                               # head
    L.piece(circle_pts(0, -540, 96, 52, a0=180, a1=360) + [(96, -520), (-96, -520)], (60, 40, 30), 45, lift=6)  # hair
    for ex in (-32, 32):
        c.drawCircle(ex, -470, 15, skia.Paint(AntiAlias=True, Color=skia.Color(250, 250, 246))); c.drawCircle(ex + 4, -468, 8, skia.Paint(AntiAlias=True, Color=skia.Color(20, 20, 30)))
    mouth = skia.Path(); mouth.addOval(skia.Rect.MakeXYWH(-26, -430, 52, 44)); c.drawPath(mouth, skia.Paint(AntiAlias=True, Color=skia.Color(90, 20, 30)))
    # arms raised in shock (two segments each, pinned)
    for sgn in (-1, 1):
        c.save(); c.translate(sgn * 60, -340); c.rotate(-sgn * 150)
        L.piece(rect_pts(-16, 0, 32, 120), (232, 60, 60), 46 + sgn, lift=10); L.pin(0, 8)
        c.translate(0, 110); c.rotate(sgn * 30); L.piece(rect_pts(-14, 0, 28, 100), (240, 194, 150), 48 + sgn, lift=10); L.pin(0, 6)
        c.restore()
    c.restore()
    # headline: cut-out words on paper strips, in the top band (below 250 px)
    L.word("COCA-COLA SOLD", 540, 420, 64, (30, 30, 40), (250, 246, 236), -3, 60)
    L.word("FOR $1", 560, 580, 130, (255, 255, 255), (224, 40, 48), 2, 61)
    img = np.asarray(surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType))[..., :3].astype(np.float32) / 255
    # construction-paper grain over everything + soft light + slight lens vignette
    g = noise_tex(H, W, 0.8, 0.05, 1) + noise_tex(H, W, 3, 0.03, 2)
    img *= (1 + g)[..., None]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.45) / H) ** 2)
    img *= (1.08 - 0.45 * d ** 2)[..., None]
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


if __name__ == "__main__":
    out = frame(); cv2.imwrite(sys.argv[1] if len(sys.argv) > 1 else "cutout.jpg", cv2.cvtColor(out, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
