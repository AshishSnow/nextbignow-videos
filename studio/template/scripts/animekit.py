"""RETRO ANIME kit for OopsMyBusiness (owner, 8 Nov 2026: "Create video on retro anime and give character from start").
80s/90s TV-anime look drawn with skia: cel shading (one hard shadow tone + hair highlight band), ink line art, big glossy eyes,
painted gradient skies, speed lines, impact frames, title-card eyecatches; finished with film grain, soft bloom, slight chromatic
fringe, gate weave and a warm grade. Animation is held on twos (12 drawings a second), like the real thing.
Host: KAI, our own character (not based on any existing anime character): messy navy hair with one tall strand, amber eyes,
teal jacket with orange lining over a white tee, headphones round his neck.
"""
import math, os
import numpy as np, skia, cv2

W, H = 1080, 1920
_S = os.environ.get("STUDIO", "/home/claude/studio")
_FD = f"{_S}/fonts/ttf"
_TFC = {}


def tf(name):
    if name not in _TFC: _TFC[name] = skia.Typeface.MakeFromFile(f"{_FD}/{name}")
    return _TFC[name]


def font(name, size): return skia.Font(tf(name), size)


INK = (34, 22, 30)
SKIN, SKIN_S, SKIN_B = (252, 222, 196), (232, 168, 150), (246, 150, 150)
HAIR, HAIR_S, HAIR_H = (40, 46, 96), (26, 28, 64), (96, 112, 190)
JACK, JACK_S, LINING = (24, 160, 160), (14, 108, 120), (250, 136, 40)
TEE, TEE_S = (250, 248, 244), (196, 200, 220)
IRIS_T, IRIS_B = (150, 64, 10), (255, 186, 70)


def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)


def P(col, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor4f(C(col, a)); return p


def S(col, w, a=1.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap,
                   StrokeJoin=skia.Paint.kRound_Join); p.setColor4f(C(col, a)); return p


def path(pts, close=True, smooth=False):
    p = skia.Path(); p.moveTo(*pts[0])
    if smooth and len(pts) > 2:
        Q = pts + ([pts[0]] if close else [])
        for i in range(1, len(Q) - 1):
            mx, my = (Q[i][0] + Q[i + 1][0]) / 2, (Q[i][1] + Q[i + 1][1]) / 2
            p.quadTo(Q[i][0], Q[i][1], mx, my)
        p.lineTo(*Q[-1])
    else:
        for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p


def cel(c, pth, base, shade=None, shade_path=None, line=4.5, lc=INK):
    """fill, one hard shadow tone clipped inside, then the ink line"""
    c.drawPath(pth, P(base))
    if shade is not None and shade_path is not None:
        c.save(); c.clipPath(pth, doAntiAlias=True); c.drawPath(shade_path, P(shade)); c.restore()
    if line: c.drawPath(pth, S(lc, line))


def ell(cx, cy, rx, ry):
    p = skia.Path(); p.addOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry)); return p


def ease(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def back(x, s=1.7): x = min(1.0, max(0.0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def pr(t, t0, d): return min(1.0, max(0.0, (t - t0) / d)) if d > 0 else float(t >= t0)


# ------------------------------------------------------------------ KAI
def _face_path():
    return path([(-150, -120), (-152, -20), (-146, 40), (-128, 100), (-92, 148), (-44, 178), (0, 186), (44, 178), (92, 148), (128, 100),
                 (146, 40), (152, -20), (150, -120), (100, -190), (0, -210), (-100, -190)], smooth=True)


def _eye(c, sx, ex, ey, kind, look, blink):
    """sx = -1 left / +1 right as seen by the viewer"""
    lx, ly = look
    if kind == "happy" or blink > 0.85:     # ^ ^ closed arcs
        a = skia.Path(); a.moveTo(ex - 44, ey + 6); a.quadTo(ex, ey - (34 if kind == "happy" else 4), ex + 44, ey + 6)
        c.drawPath(a, S(INK, 9)); return
    shock = kind == "shock"
    top = ey - 52 * (1 - blink * 0.9); bot = ey + 40
    white = path([(ex - 50, ey - 6), (ex - 42, top + 8), (ex - 10, top), (ex + 30, top + 2), (ex + 52, top + 14), (ex + 52, ey + 10),
                  (ex + 34, bot - 4), (ex, bot + 2), (ex - 34, bot - 6)], smooth=True)
    c.drawPath(white, P((255, 255, 255)))
    c.save(); c.clipPath(white, doAntiAlias=True)
    ir = 20 if shock else 34; irh = 30 if shock else 48
    ix, iy = ex + lx * 12 + sx * 2, ey + 2 + ly * 10
    g = skia.GradientShader.MakeLinear([skia.Point(ix, iy - irh), skia.Point(ix, iy + irh)], [C(IRIS_T), C(IRIS_B)])
    ip = skia.Paint(AntiAlias=True); ip.setShader(g); c.drawPath(ell(ix, iy, ir, irh), ip)
    c.drawPath(ell(ix, iy, ir, irh), S(INK, 3))
    c.drawPath(ell(ix, iy - 4, ir * 0.45, irh * 0.5), P((60, 20, 10)))
    c.drawPath(ell(ix + ir * 0.35, iy - irh * 0.45, ir * 0.38, irh * 0.26), P((255, 255, 255)))     # big catch-light
    c.drawCircle(ix - ir * 0.4, iy + irh * 0.45, ir * 0.16, P((255, 255, 255)))
    c.drawPath(path([(ex - 60, top - 20), (ex + 60, top - 20), (ex + 60, top + 14), (ex - 60, top + 14)]), P(SKIN_S, 0.55))   # lid shadow
    c.restore()
    lash = skia.Path(); lash.moveTo(ex - 54, ey - 2 + (top - (ey - 52)) * 0.3); lash.quadTo(ex - 20, top - 10, ex + 30, top - 2); lash.quadTo(ex + 50, top + 4, ex + 60, top + 22)
    c.drawPath(lash, S(INK, 11)); c.drawLine(ex + sx * 0 + 52, top + 14, ex + 64, top + 2, S(INK, 6))
    low = skia.Path(); low.moveTo(ex - 30, bot - 4); low.quadTo(ex, bot + 6, ex + 32, bot - 6); c.drawPath(low, S(INK, 3.5))


def _brow(c, sx, ex, ey, kind):
    dy = {"up": -26, "angry": 4, "worried": -14, "neutral": -6, "smug": -10}.get(kind, -6)
    tilt = {"angry": 16, "worried": -16, "smug": 8 * sx}.get(kind, 0)
    x0, x1 = ex - 46, ex + 46
    y0 = ey - 82 + dy + (tilt if sx < 0 else -tilt) * 0.5
    y1 = ey - 82 + dy - (tilt if sx < 0 else -tilt) * 0.5
    b = skia.Path(); b.moveTo(x0, y0 + 6); b.quadTo((x0 + x1) / 2, min(y0, y1) - 10, x1, y1 + 4)
    c.drawPath(b, S(HAIR_S, 10))


def _mouth(c, kind, k):
    y = 128
    if kind in ("closed", "smile") and k < 0.15:
        m = skia.Path(); m.moveTo(-30, y); m.quadTo(0, y + (16 if kind == "smile" else 4), 30, y - (2 if kind == "smile" else 0)); c.drawPath(m, S(INK, 5)); return
    if kind == "smirk" and k < 0.15:
        m = skia.Path(); m.moveTo(-26, y + 4); m.quadTo(4, y + 10, 30, y - 8); c.drawPath(m, S(INK, 5)); return
    k = max(k, 0.25)
    w = 34 + 14 * k if kind != "shout" else 46 + 10 * k; h = 10 + 46 * k if kind != "shout" else 30 + 50 * k
    if kind in ("smile", "grin"):
        m = path([(-w, y - 6), (w, y - 6), (w * 0.6, y + h * 0.8), (0, y + h), (-w * 0.6, y + h * 0.8)], smooth=True)
    else:
        m = path([(-w * 0.8, y), (0, y - 6), (w * 0.8, y), (w * 0.5, y + h), (0, y + h + 4), (-w * 0.5, y + h)], smooth=True)
    c.drawPath(m, P((110, 24, 40)))
    c.save(); c.clipPath(m, doAntiAlias=True)
    c.drawPath(ell(0, y + h + 6, w * 0.6, h * 0.45), P((236, 110, 120)))          # tongue
    if kind in ("smile", "grin"): c.drawRect(skia.Rect.MakeLTRB(-w, y - 10, w, y + 4), P((255, 255, 255)))   # teeth
    c.restore(); c.drawPath(m, S(INK, 4.5))


def _hair_back(c):
    pts = [(-200, 60), (-232, -40), (-262, -150), (-210, -150), (-230, -250), (-150, -230), (-140, -330), (-60, -280), (0, -360),
           (50, -290), (150, -340), (150, -250), (240, -260), (212, -160), (262, -130), (224, -40), (200, 60), (150, -60), (-150, -60)]
    cel(c, path(pts), HAIR, HAIR_S, path([(-300, -100), (300, -100), (300, 100), (-300, 100)]), 5)


def _hair_front(c, t):
    sway = 4 * math.sin(t * 2.3)
    # one clean silhouette: cap over the crown, then a zig-zag of locks along the fringe (tips low, notches high)
    tips = [(-206, 40), (-150, 66), (-96, 52), (-44, 34), (8, 40), (62, 30), (116, 58), (170, 70), (208, 36)]
    notch = [(-176, -40), (-122, -30), (-70, -50), (-16, -36), (36, -54), (90, -34), (144, -26), (190, -40)]
    fr = skia.Path(); fr.moveTo(214, 40)
    fr.cubicTo(250, -120, 170, -290, 0, -296); fr.cubicTo(-170, -290, -250, -120, -214, 40)
    for i in range(len(tips)):
        x, y = tips[i]; fr.lineTo(x + sway * (0.5 + 0.5 * math.sin(i)), y)
        if i < len(notch): fr.lineTo(*notch[i])
    fr.close()
    cel(c, fr, HAIR, HAIR_S, path([(30, -320), (280, -320), (280, 120), (60, 120), (110, -40)]), 5.5)
    # glossy highlight band across the crown: a soft arc with a few nicks (classic cel hair)
    c.save(); c.clipPath(fr, doAntiAlias=True)
    hb = skia.Path(); hb.moveTo(-180, -150); hb.cubicTo(-100, -230, 100, -230, 180, -150)
    hb.lineTo(150, -128); hb.lineTo(118, -150); hb.lineTo(84, -170); hb.lineTo(40, -152); hb.lineTo(-6, -176); hb.lineTo(-50, -156)
    hb.lineTo(-96, -172); hb.lineTo(-136, -146); hb.close(); c.drawPath(hb, P(HAIR_H))
    c.drawPath(path([(-120, -196), (-80, -214), (-70, -204), (-112, -186)]), P((200, 210, 255)))
    c.restore()
    # a couple of inner strand lines so the fringe reads as hair, not a hat
    for (x0, y0, x1, y1) in ((-130, -120, -150, 40), (-40, -150, -44, 20), (60, -150, 62, 14), (140, -110, 160, 50)):
        st = skia.Path(); st.moveTo(x0, y0); st.quadTo((x0 + x1) / 2 + 14, (y0 + y1) / 2, x1, y1 - 20); c.drawPath(st, S(HAIR_S, 4))
    # the tall strand
    ah = skia.Path(); ah.moveTo(-10, -292); ah.cubicTo(-30, -390, 60, -430, 70 + sway * 2, -368); ah.cubicTo(30, -388, 20, -336, 22, -292); ah.close()
    cel(c, ah, HAIR, line=5)


def _body(c, t, breathe):
    b = 4 * breathe
    # torso / jacket
    jk = path([(-330, 1400), (-300, 560), (-290, 330), (-230, 250 - b), (-120, 214 - b), (120, 214 - b), (230, 250 - b), (290, 330), (300, 560), (330, 1400)])
    cel(c, jk, JACK, JACK_S, path([(-340, 300), (-40, 230), (-60, 1400), (-340, 1400)]), 5.5)
    tee = path([(-110, 220 - b), (110, 220 - b), (80, 1400), (-80, 1400)])
    cel(c, tee, TEE, TEE_S, path([(-120, 220), (120, 220), (120, 300), (-120, 280)]), 4.5)
    for sx in (-1, 1):   # open jacket fronts with orange lining
        lap = path([(sx * 110, 218 - b), (sx * 150, 240), (sx * 104, 1400), (sx * 80, 1400)])
        cel(c, lap, LINING, line=4.5)
        col = path([(sx * 110, 216 - b), (sx * 196, 236 - b), (sx * 176, 300), (sx * 128, 300)])
        cel(c, col, JACK, JACK_S, path([(sx * 100, 260), (sx * 200, 260), (sx * 200, 320), (sx * 100, 320)]), 5)
    # neck + headphones resting round it
    nk = path([(-58, 120), (58, 120), (66, 230), (0, 250), (-66, 230)])
    cel(c, nk, SKIN, SKIN_S, path([(-80, 100), (80, 100), (80, 170), (0, 196), (-80, 170)]), 4.5)
    band = skia.Path(); band.moveTo(-122, 196); band.cubicTo(-100, 290, 100, 290, 122, 196); c.drawPath(band, S((54, 54, 66), 22)); c.drawPath(band, S(INK, 3))
    for sx in (-1, 1):
        cup = ell(sx * 130, 200, 46, 58); cel(c, cup, (60, 60, 74), (36, 36, 48), ell(sx * 130 + sx * 18, 210, 40, 58), 5)
        c.drawPath(ell(sx * 130, 196, 20, 26), P(LINING))


def _arm(c, kind, t):
    """his right arm (viewer's right), raised in front of the jacket: wave / point / think / fist"""
    if not kind: return
    sw = 10 * math.sin(t * 9) if kind == "wave" else 0
    sh = (250, 420); el = {"wave": (330, 160), "point": (300, 170), "think": (150, 260), "fist": (300, 200)}[kind]
    hd = {"wave": (300 + sw, -60), "point": (250, -40), "think": (60, 160), "fist": (300, 20)}[kind]
    for a_, b_ in ((sh, el), (el, hd)):
        d = math.hypot(b_[0] - a_[0], b_[1] - a_[1]); nx, ny = -(b_[1] - a_[1]) / d * 52, (b_[0] - a_[0]) / d * 52
        sl = path([(a_[0] + nx, a_[1] + ny), (b_[0] + nx * 0.8, b_[1] + ny * 0.8), (b_[0] - nx * 0.8, b_[1] - ny * 0.8), (a_[0] - nx, a_[1] - ny)])
        cel(c, sl, JACK, JACK_S, path([(a_[0], a_[1]), (b_[0], b_[1]), (b_[0] + 80, b_[1]), (a_[0] + 80, a_[1])]), 5)
    c.drawPath(ell(hd[0], hd[1] + 40, 46, 22), P(LINING)); c.drawPath(ell(hd[0], hd[1] + 40, 46, 22), S(INK, 4))   # cuff
    hx, hy = hd
    palm = path([(hx - 44, hy + 30), (hx - 50, hy - 20), (hx - 30, hy - 50), (hx + 30, hy - 50), (hx + 50, hy - 20), (hx + 44, hy + 30)], smooth=True)
    if kind in ("wave",):
        for i, fx in enumerate((-36, -12, 12, 36)):
            cel(c, path([(hx + fx - 11, hy - 30), (hx + fx - 9, hy - 96 + abs(fx) * 0.6), (hx + fx + 9, hy - 96 + abs(fx) * 0.6), (hx + fx + 11, hy - 30)], smooth=True), SKIN, line=4)
        cel(c, path([(hx - 44, hy + 4), (hx - 92, hy - 34), (hx - 80, hy - 50), (hx - 40, hy - 24)], smooth=True), SKIN, line=4)
    elif kind == "point":
        cel(c, path([(hx - 10, hy - 30), (hx - 8, hy - 140), (hx + 12, hy - 140), (hx + 14, hy - 30)], smooth=True), SKIN, line=4)
    cel(c, palm, SKIN, SKIN_S, path([(hx, hy - 60), (hx + 60, hy - 60), (hx + 60, hy + 40), (hx, hy + 40)]), 4.5)
    if kind in ("fist", "think", "point"):
        for k in range(3): c.drawLine(hx - 30 + k * 22, hy - 20, hx - 30 + k * 22, hy + 6, S(INK, 3.5))


def kai(c, x, y, s=1.0, t=0.0, mouth=0.0, mouth_kind="talk", eyes="open", brows="neutral", look=(0, 0), blink=0.0,
        tilt=0.0, blush=False, sweat=False, sparkle=False, body=True, arm=None):
    """draw Kai's bust. (x, y) = centre of his face; s = scale (1.0 ≈ face 300 px wide)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    br = math.sin(t * 2.4)
    if body: _body(c, t, br)
    c.rotate(tilt); c.translate(0, -3 * br)
    _hair_back(c)
    for sx in (-1, 1):   # ears
        e = ell(sx * 150, 30, 26, 40); cel(c, e, SKIN, SKIN_S, ell(sx * 150 + sx * 6, 34, 16, 28), 4.5)
    f = _face_path()
    cel(c, f, SKIN, SKIN_S, path([(40, -200), (220, -200), (220, 220), (110, 180), (60, 60)]), 5.5)   # shade on his left side
    c.save(); c.clipPath(f, doAntiAlias=True)   # the fringe throws a jagged shadow on the forehead
    sh = skia.Path(); sh.moveTo(-200, -200)
    for i in range(10): sh.lineTo(-180 + i * 40, -40 + (i % 2) * 34)
    sh.lineTo(220, -200); sh.close(); c.drawPath(sh, P(SKIN_S)); c.restore()
    if blush or mouth_kind in ("grin",):
        for sx in (-1, 1):
            c.drawPath(ell(sx * 92, 92, 34, 14), P(SKIN_B, 0.6))
            for k in range(3): c.drawLine(sx * 78 + k * 12, 84, sx * 70 + k * 12, 100, S((220, 90, 100), 3))
    for sx in (-1, 1):
        _eye(c, sx, sx * 70, 32, eyes, look, blink); _brow(c, sx, sx * 70, 32, brows)
    c.drawLine(4, 84, -4, 98, S(SKIN_S, 5))
    _mouth(c, mouth_kind, mouth)
    _hair_front(c, t)
    if sweat:
        d = path([(176, -60), (196, -10), (186, 14), (166, 14), (158, -10)], smooth=True); cel(c, d, (170, 220, 255), line=4)
        c.drawPath(ell(176, 0, 6, 9), P((255, 255, 255)))
    if sparkle:
        for (sx_, sy_, r_) in ((-230, -260, 40), (240, -200, 28)): star4(c, sx_, sy_, r_, (255, 250, 200))
    c.restore()
    if body and arm:
        c.save(); c.translate(x, y); c.scale(s, s); _arm(c, arm, t); c.restore()


def star4(c, x, y, r, col):
    p = path([(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r), (x - r * 0.22, y + r * 0.22),
              (x - r, y), (x - r * 0.22, y - r * 0.22)])
    c.drawPath(p, P(col))


def star5(c, x, y, r, col, line=5, rot=0):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + i * 36); rr = r if i % 2 == 0 else r * 0.45; pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    cel(c, path(pts), col, line=line)


# ------------------------------------------------------------------ backgrounds (painted, no line art — like real anime BGs)
def sky(c, top, mid, bot, y0=0, y1=H):
    g = skia.GradientShader.MakeLinear([skia.Point(0, y0), skia.Point(0, y1)], [C(top), C(mid), C(bot)], [0, 0.55, 1])
    p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeLTRB(0, y0, W, y1), p)


def retro_sun(c, x, y, r, top=(255, 230, 90), bot=(255, 70, 120), stripes=7, gap_col=None):
    g = skia.GradientShader.MakeLinear([skia.Point(x, y - r), skia.Point(x, y + r)], [C(top), C(bot)])
    p = skia.Paint(AntiAlias=True); p.setShader(g)
    c.save()
    clip = skia.Path(); clip.addCircle(x, y, r)
    for i in range(stripes):
        yy = y + r * (0.15 + i * 0.13); hh = 4 + i * 3.2
        hole = skia.Path(); hole.addRect(skia.Rect.MakeLTRB(x - r - 2, yy, x + r + 2, yy + hh)); clip = skia.Op(clip, hole, skia.PathOp.kDifference_PathOp)
    c.drawPath(clip, p); c.restore()


def skyline(c, base_y, col, seed=1, hmin=120, hmax=460, wmin=60, wmax=150, windows=None):
    r = np.random.default_rng(seed); x = -20
    while x < W + 20:
        w = r.integers(wmin, wmax); h = r.integers(hmin, hmax)
        c.drawRect(skia.Rect.MakeLTRB(x, base_y - h, x + w, base_y + 4), P(col))
        if r.random() < 0.3: c.drawRect(skia.Rect.MakeLTRB(x + w * 0.4, base_y - h - 40, x + w * 0.45, base_y - h), P(col))
        if windows:
            for wy in range(int(base_y - h + 20), int(base_y - 10), 28):
                for wx in range(int(x + 10), int(x + w - 12), 22):
                    if r.random() < 0.35: c.drawRect(skia.Rect.MakeLTRB(wx, wy, wx + 9, wy + 12), P(windows, 0.85))
        x += w + r.integers(-10, 16)


def hills(c, y, col, amp=60, seed=2, freq=1.0):
    r = np.random.default_rng(seed); ph = r.random(3) * 6
    pts = [(0, H)]
    for xx in range(0, W + 41, 40):
        pts.append((xx, y - amp * (0.6 * math.sin(xx / 260 * freq + ph[0]) + 0.3 * math.sin(xx / 120 * freq + ph[1]) + 0.1 * math.sin(xx / 50 + ph[2]))))
    pts.append((W, H)); c.drawPath(path(pts), P(col))


def speed_lines(c, cx, cy, col=(255, 255, 255), n=90, r0=380, seed=0, a=0.9, wmax=16):
    r = np.random.default_rng(seed)
    for i in range(n):
        ang = r.random() * math.tau; w = r.uniform(3, wmax); rr = r0 * r.uniform(0.8, 1.5)
        x0, y0 = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr; x1, y1 = cx + math.cos(ang) * 1800, cy + math.sin(ang) * 1800
        nx, ny = -math.sin(ang), math.cos(ang)
        c.drawPath(path([(x0, y0), (x1 + nx * w * 6, y1 + ny * w * 6), (x1 - nx * w * 6, y1 - ny * w * 6)]), P(col, a * r.uniform(0.5, 1)))


def flow_lines(c, col=(255, 255, 255), n=40, seed=0, t=0.0, a=0.7, speed=2400):
    """horizontal motion lines (a fast pan / driving)"""
    r = np.random.default_rng(seed)
    for i in range(n):
        y = r.uniform(0, H); L = r.uniform(200, 700); x = (r.uniform(0, W + L) - t * speed * r.uniform(0.7, 1.3)) % (W + L * 2) - L
        c.drawRect(skia.Rect.MakeLTRB(x, y, x + L, y + r.uniform(2, 7)), P(col, a * r.uniform(0.4, 1)))


def halftone(c, rect, col, step=22, rmax=7, a=0.35, vertical=True):
    x0, y0, x1, y1 = rect
    for yy in np.arange(y0, y1, step):
        k = (yy - y0) / max(1, (y1 - y0)) if vertical else 1
        for xx in np.arange(x0 + (step / 2 if int((yy - y0) / step) % 2 else 0), x1, step):
            r_ = rmax * (k if vertical else (xx - x0) / max(1, x1 - x0))
            if r_ > 0.5: c.drawCircle(xx, yy, r_, P(col, a))


# ------------------------------------------------------------------ type: title cards, captions
def title_card(c, t, t0, lines, bg=(250, 70, 110), fg=(255, 250, 240), sub=None, y=960, rot=-4):
    """80s eyecatch: a slab of colour slams in with stripes, big outlined type"""
    k = back(pr(t, t0, 0.28), 2.2)
    if k <= 0: return
    c.save(); c.translate(W / 2, y); c.rotate(rot); c.scale(k, k)
    c.drawRect(skia.Rect.MakeLTRB(-640, -230, 640, 230), P(bg))
    for i in range(6): c.drawRect(skia.Rect.MakeLTRB(-640, 180 + i * 9, 640, 183 + i * 9), P(fg, 0.5))
    for i in range(6): c.drawRect(skia.Rect.MakeLTRB(-640, -230 + i * 9, 640, -227 + i * 9), P(fg, 0.5))
    yy = -40 * (len(lines) - 1)
    for ln, size in lines:
        outline_text(c, ln, 0, yy + size * 0.36, size, fg, INK, 14); yy += size * 1.02
    if sub: outline_text(c, sub, 0, 175, 46, (255, 236, 120), INK, 8, fnt="Bangers.ttf")
    c.restore()


def outline_text(c, s, x, y, size, fill, line=INK, lw=12, fnt="Bangers.ttf", align="c", shadow=True, a=1.0):
    f = font(fnt, size); w = f.measureText(s); xs = x - w / 2 if align == "c" else x
    blob = skia.TextBlob.MakeFromString(s, f)
    if shadow: c.drawTextBlob(blob, xs + size * 0.06, y + size * 0.07, P(INK, 0.9 * a))
    st = S(line, lw, a); c.drawTextBlob(blob, xs, y, st); c.drawTextBlob(blob, xs, y, P(fill, a))
    return w


def caption(c, t, t0, small, big, col=(255, 214, 60), t1=None, y=1390, size=150):
    """key-moment caption: small line + one big punch word, slammed in"""
    if t < t0 or (t1 is not None and t > t1): return
    k = back(pr(t, t0, 0.22), 2.4)
    c.save(); c.translate(W / 2, y); c.scale(k, k)
    if small:
        sz = 54; f = font("Bangers.ttf", sz)
        while f.measureText(small) > 820 and sz > 34: sz -= 2; f = font("Bangers.ttf", sz)
        outline_text(c, small, 0, -size * 0.9, sz, (255, 255, 255), INK, 9)
    sz = size; f = font("Bangers.ttf", sz)
    while f.measureText(big) > 860 and sz > 70: sz -= 4; f = font("Bangers.ttf", sz)
    outline_text(c, big, 0, sz * 0.3, sz, col, INK, 16)
    c.restore()


def nameplate(c, t, t0, name, role):
    k = ease(pr(t, t0, 0.3))
    if k <= 0: return
    x = -700 + 760 * k
    c.save(); c.translate(x, 1330); c.rotate(-3)
    c.drawRect(skia.Rect.MakeLTRB(0, -110, 620, 40), P((250, 70, 110)))
    c.drawRect(skia.Rect.MakeLTRB(0, 40, 620, 110), P((24, 160, 160)))
    outline_text(c, name, 60, 6, 120, (255, 250, 240), INK, 12, align="l")
    outline_text(c, role, 60, 92, 48, (255, 236, 120), INK, 7, align="l")
    c.restore()


# ------------------------------------------------------------------ film finish
_R = np.random.default_rng(11)
_GRAIN = [(_R.normal(0, 1, (H // 2, W // 2)).astype(np.float32)) for _ in range(8)]
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = (1.0 - 0.42 * (((_xx - W / 2) / (W * 0.75)) ** 2 + ((_yy - H / 2) / (H * 0.75)) ** 2))[..., None]
_SCAN = (1 - 0.035 * (np.arange(H) % 4 == 0).astype(np.float32))[:, None, None]


def finish(img, n, flash=0.0):
    """img float RGB 0..1 -> retro TV-anime film look"""
    # soft bloom from the bright parts (cel paint glows a little on old film)
    small = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    br = np.clip(small - 0.62, 0, 1); br = cv2.GaussianBlur(br, (0, 0), 9)
    img = img + 0.55 * cv2.resize(br, (W, H), interpolation=cv2.INTER_LINEAR)
    # chromatic fringe + gate weave
    dx = int(round(math.sin(n * 1.7) * 1.2)); dy = int(round(math.sin(n * 2.3) * 1.0))
    img = np.roll(img, (dy, dx), axis=(0, 1))
    img[..., 0] = np.roll(img[..., 0], 2, axis=1); img[..., 2] = np.roll(img[..., 2], -2, axis=1)
    # grade: lifted, slightly purple blacks; warm highlights; a touch more saturation
    img = 0.035 + img * 0.95
    img = img * np.array((1.04, 1.0, 0.95), np.float32) + np.array((0.012, 0.0, 0.03), np.float32) * (1 - img)
    lum = img.mean(2, keepdims=True); img = lum + (img - lum) * 1.12
    img *= _VIG; img *= _SCAN
    g = cv2.resize(_GRAIN[n % 8], (W, H), interpolation=cv2.INTER_LINEAR)[..., None] * 0.028
    img = img + g
    if flash: img = img * (1 - flash) + flash
    return np.clip(img, 0, 1)


# ------------------------------------------------------------------ supporting cast (generic, invented people — never likenesses)
SUIT, SUIT_S = (60, 56, 76), (38, 34, 52)


def gent(c, x, y, s=1.0, t=0.0, mouth=0.0, variant=0, eyes="open", look=(0, 0), shock=False, sweat=False):
    """a 1900s businessman bust. variant 0: bowler hat + big moustache; 1: bare head + short beard"""
    c.save(); c.translate(x, y); c.scale(s, s)
    br = math.sin(t * 2.0 + variant)
    body = path([(-320, 1400), (-300, 520), (-280, 320), (-200, 240), (-90, 210), (90, 210), (200, 240), (280, 320), (300, 520), (320, 1400)])
    cel(c, body, SUIT, SUIT_S, path([(-340, 300), (-40, 230), (-60, 1400), (-340, 1400)]), 5.5)
    shirt = path([(-90, 212), (90, 212), (40, 520), (-40, 520)]); cel(c, shirt, (250, 248, 240), line=4.5)
    tie = path([(-30, 236), (30, 236), (18, 260), (36, 430), (0, 470), (-36, 430), (-18, 260)]); cel(c, tie, (180, 40, 50) if variant == 0 else (40, 90, 160), line=4)
    for sx in (-1, 1):
        lap = path([(sx * 90, 212), (sx * 200, 250), (sx * 120, 420), (sx * 52, 520)]); cel(c, lap, SUIT, SUIT_S, path([(sx * 60, 400), (sx * 220, 400), (sx * 220, 600), (sx * 60, 600)]), 5)
    nk = path([(-60, 110), (60, 110), (70, 220), (-70, 220)]); cel(c, nk, SKIN, SKIN_S, path([(-80, 100), (80, 100), (80, 170), (-80, 170)]), 4.5)
    for sx in (-1, 1): cel(c, path([(sx * 30, 196), (sx * 96, 206), (sx * 90, 240), (sx * 24, 226)]), (255, 255, 255), line=4)   # wing collar
    c.translate(0, -3 * br)
    for sx in (-1, 1): cel(c, ell(sx * 150, 30, 26, 40), SKIN, SKIN_S, ell(sx * 156, 34, 16, 28), 4.5)
    f = path([(-150, -120), (-152, -20), (-146, 50), (-124, 116), (-80, 160), (0, 178), (80, 160), (124, 116), (146, 50), (152, -20), (150, -120), (100, -190), (0, -210), (-100, -190)], smooth=True)
    cel(c, f, SKIN, SKIN_S, path([(40, -200), (220, -200), (220, 220), (110, 180), (60, 60)]), 5.5)
    for sx in (-1, 1):
        ex = sx * 66
        if eyes == "closed" or shock is False and eyes == "narrow":
            c.drawLine(ex - 34, 34, ex + 34, 30, S(INK, 7))
        else:
            r_ = 14 if shock else 20
            c.drawPath(ell(ex, 34, 36, 22 if not shock else 30), P((255, 255, 255))); c.drawPath(ell(ex, 34, 36, 22 if not shock else 30), S(INK, 4))
            c.drawCircle(ex + look[0] * 8, 36 + look[1] * 6, r_, P((70, 50, 40))); c.drawCircle(ex + look[0] * 8 + 6, 30, 5, P((255, 255, 255)))
            ln = skia.Path(); ln.moveTo(ex - 40, 22); ln.quadTo(ex, 4, ex + 40, 20); c.drawPath(ln, S(INK, 8))
        bw = skia.Path(); bw.moveTo(ex - 40, -16 - (14 if shock else 0)); bw.quadTo(ex, -30 - (14 if shock else 0), ex + 40, -12 - (14 if shock else 0)); c.drawPath(bw, S((60, 40, 30), 12))
    c.drawLine(6, 70, -6, 96, S(SKIN_S, 6))
    k = max(mouth, 0.55 if shock else 0)
    if k > 0.1: c.drawPath(ell(0, 132, 22 + 6 * k, 6 + 26 * k), P((110, 24, 40))); c.drawPath(ell(0, 132, 22 + 6 * k, 6 + 26 * k), S(INK, 4))
    else: c.drawLine(-24, 132, 24, 132, S(INK, 5))
    hc = (70, 46, 34) if variant == 0 else (120, 90, 70)
    if variant == 0:
        mo = path([(-10, 104), (-60, 98), (-110, 120), (-120, 104), (-70, 84), (0, 92), (70, 84), (120, 104), (110, 120), (60, 98), (10, 104)], smooth=True)
        cel(c, mo, hc, line=4.5)
        hat = path([(-220, -96), (220, -96), (196, -128), (150, -136), (140, -250), (90, -310), (0, -322), (-90, -310), (-140, -250), (-150, -136), (-196, -128)], smooth=False)
        cel(c, hat, (36, 34, 40), (20, 18, 24), path([(40, -330), (240, -330), (240, -90), (40, -90)]), 5.5)
        c.drawRect(skia.Rect.MakeLTRB(-148, -160, 148, -132), P((110, 30, 40)))
    else:
        hr = path([(-156, -40), (-170, -150), (-110, -220), (0, -236), (110, -220), (170, -150), (156, -40), (120, -150), (0, -170), (-120, -150)], smooth=True)
        cel(c, hr, hc, (90, 64, 50), path([(40, -260), (200, -260), (200, 0), (40, 0)]), 5)
        bd = path([(-140, 70), (-120, 150), (-60, 210), (0, 226), (60, 210), (120, 150), (140, 70), (100, 150), (40, 160), (0, 152), (-40, 160), (-100, 150)], smooth=True)
        cel(c, bd, hc, line=4.5)
    if sweat:
        d = path([(176, -60), (196, -10), (186, 14), (166, 14), (158, -10)], smooth=True); cel(c, d, (170, 220, 255), line=4)
    c.restore()


def inspector(c, x, y, s=1.0, t=0.0, glint=0.0):
    """the anonymous inspector: fedora, turned-up trench collar, face in shadow, glasses catching the light"""
    c.save(); c.translate(x, y); c.scale(s, s)
    coat = path([(-340, 1400), (-320, 480), (-260, 300), (-150, 230), (150, 230), (260, 300), (320, 480), (340, 1400)])
    cel(c, coat, (176, 140, 90), (130, 98, 60), path([(-360, 300), (-30, 230), (-50, 1400), (-360, 1400)]), 5.5)
    for sx in (-1, 1): cel(c, path([(sx * 40, 260), (sx * 190, 150), (sx * 230, 330), (sx * 90, 480)]), (196, 160, 110), (150, 116, 76), path([(sx * 40, 300), (sx * 240, 300), (sx * 240, 500), (sx * 40, 500)]), 5)
    f = path([(-140, -100), (-142, 40), (-110, 130), (0, 176), (110, 130), (142, 40), (140, -100), (0, -150)], smooth=True)
    cel(c, f, (150, 118, 120), line=5)
    c.save(); c.clipPath(f, doAntiAlias=True); c.drawRect(skia.Rect.MakeLTRB(-200, -200, 200, 60), P((60, 40, 60))); c.restore()   # hat shadow over the eyes
    for sx in (-1, 1):
        lens = skia.Path(); lens.addRoundRect(skia.Rect.MakeLTRB(sx * 64 - 46, -6, sx * 64 + 46, 44), 10, 10)
        c.drawPath(lens, P((255, 255, 255), 0.35 + 0.65 * glint)); c.drawPath(lens, S(INK, 5))
        if glint > 0.2: star4(c, sx * 64 + 24, 4, 34 * glint, (255, 255, 255))
    c.drawLine(-18, 18, 18, 18, S(INK, 5))
    c.drawLine(-30, 120, 30, 120, S(INK, 5))
    hat = path([(-260, -70), (260, -70), (230, -110), (160, -120), (150, -230), (60, -270), (0, -246), (-60, -270), (-150, -230), (-160, -120), (-230, -110)])
    cel(c, hat, (70, 64, 70), (44, 40, 46), path([(30, -300), (300, -300), (300, -60), (30, -60)]), 5.5)
    c.drawRect(skia.Rect.MakeLTRB(-156, -150, 156, -118), P((30, 28, 34)))
    c.restore()


# ------------------------------------------------------------------ props (generic shapes, no real logos or trade dress)
def tyre(c, x, y, r, rot=0.0, worn=0.0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(0, 0, r, P((36, 34, 40), a)); c.drawCircle(0, 0, r, S(INK, 5, a))
    nt = 22
    for i in range(nt):   # tread blocks (they fade as the tyre wears)
        ang = i * math.tau / nt; ca, sa = math.cos(ang), math.sin(ang)
        q = path([(ca * r * 0.86 - sa * 10, sa * r * 0.86 + ca * 10), (ca * r * 0.99 - sa * 10, sa * r * 0.99 + ca * 10),
                  (ca * r * 0.99 + sa * 10, sa * r * 0.99 - ca * 10), (ca * r * 0.86 + sa * 10, sa * r * 0.86 - ca * 10)])
        c.drawPath(q, P((70, 66, 78), a * (1 - worn)))
    c.drawCircle(0, 0, r * 0.62, P((180, 186, 200), a)); c.drawCircle(0, 0, r * 0.62, S(INK, 4, a))
    c.drawCircle(0, 0, r * 0.2, P((120, 124, 140), a)); c.drawCircle(0, 0, r * 0.2, S(INK, 4, a))
    for i in range(5):
        ang = i * math.tau / 5; c.drawCircle(math.cos(ang) * r * 0.38, math.sin(ang) * r * 0.38, r * 0.05, P((90, 94, 110), a))
    c.drawArc(skia.Rect.MakeLTRB(-r * 0.9, -r * 0.9, r * 0.9, r * 0.9), 200, 60, False, S((255, 255, 255), 6, 0.35 * a))
    c.restore()


def red_book(c, x, y, s=1.0, rot=0.0, open_=0.0, label="GUIDE"):
    """a little red travel guide (generic). open_ 0..1 swings the cover open onto a map page"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.translate(150 * (1 - min(1.0, open_)), 0)   # centred closed or open
    if open_ > 0:
        pg = path([(0, -200), (300 * max(0.05, open_), -196), (300 * max(0.05, open_), 196), (0, 200)])
        cel(c, pg, (250, 244, 226), line=5)
        if open_ > 0.6:
            c.save(); c.clipPath(pg)
            for i in range(5):
                rd = skia.Path(); rd.moveTo(20, -160 + i * 70); rd.cubicTo(100, -190 + i * 70, 180, -100 + i * 60, 280, -140 + i * 76); c.drawPath(rd, S((200, 80, 60), 5))
            c.drawCircle(150, -40, 14, P((40, 140, 200))); c.drawCircle(220, 80, 14, P((40, 140, 200)))
            c.restore()
    cov = path([(-300 * (1 - open_ * 2) if open_ < 0.5 else 0, -200), (0, -200), (0, 200), (-300 * (1 - open_ * 2) if open_ < 0.5 else 0, 200)]) if open_ > 0 else None
    body = path([(-300, -200), (0, -200), (0, 200), (-300, 200)])
    cel(c, body, (200, 30, 40), (150, 18, 30), path([(-300, 120), (0, 120), (0, 210), (-300, 210)]), 5.5)
    c.drawRect(skia.Rect.MakeLTRB(-290, -200, -262, 200), P((150, 18, 30)))
    c.drawRect(skia.Rect.MakeLTRB(-240, -150, -40, -144), P((255, 210, 100))); c.drawRect(skia.Rect.MakeLTRB(-240, 140, -40, 146), P((255, 210, 100)))
    outline_text(c, label, -150, 20, 70, (255, 210, 100), INK, 0.1, shadow=False)
    c.restore()


def old_car(c, x, y, s=1.0, t=0.0, wheel_rot=0.0, body_col=(30, 110, 70)):
    """an early-1900s open motor car, side view (generic)"""
    c.save(); c.translate(x, y); c.scale(s, s)
    bob = 3 * math.sin(t * 22)
    for wx in (-210, 210): spoke_wheel(c, wx, -10, 120, wheel_rot)
    c.translate(0, bob)
    chassis = path([(-330, -70), (330, -70), (350, -30), (-350, -30)]); cel(c, chassis, (60, 50, 50), line=5)
    body = path([(-280, -60), (-280, -190), (-120, -200), (-60, -140), (150, -140), (170, -220), (290, -220), (300, -60)])
    cel(c, body, body_col, tuple(int(v * 0.7) for v in body_col), path([(-300, -110), (320, -110), (320, -50), (-300, -50)]), 5.5)
    seat = path([(-250, -190), (-250, -300), (-150, -300), (-140, -200)]); cel(c, seat, (110, 50, 40), line=5)
    c.drawLine(120, -150, 60, -280, S(INK, 9)); c.drawPath(ell(56, -290, 46, 14), S(INK, 8))     # steering column + wheel
    c.drawPath(ell(310, -170, 22, 22), P((255, 236, 160))); c.drawPath(ell(310, -170, 22, 22), S(INK, 5))   # lamp
    c.restore()


def spoke_wheel(c, x, y, r, rot=0.0):
    """early motor-car wheel: thin rubber tyre on a wooden spoked rim"""
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(0, 0, r, P((36, 34, 40))); c.drawCircle(0, 0, r, S(INK, 5))
    c.drawCircle(0, 0, r * 0.84, P((200, 150, 90))); c.drawCircle(0, 0, r * 0.84, S(INK, 4))
    c.drawCircle(0, 0, r * 0.74, P((250, 230, 190)))
    for i in range(12):
        a = i * math.tau / 12; c.drawLine(0, 0, math.cos(a) * r * 0.76, math.sin(a) * r * 0.76, S((170, 120, 70), 9))
    c.drawCircle(0, 0, r * 0.16, P((120, 90, 60))); c.drawCircle(0, 0, r * 0.16, S(INK, 4))
    c.restore()


def workbench(c, x, y, s=1.0, books=True, wobble=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    top = path([(-360, -40), (360, -40), (360, 10), (-360, 10)]); c.save(); c.rotate(wobble)
    cel(c, top, (180, 120, 70), (140, 90, 50), path([(-380, -10), (380, -10), (380, 20), (-380, 20)]), 5.5)
    for xx in (-200, 0, 180): tyre(c, xx, -130, 80, 10 * xx)
    c.restore()
    cel(c, path([(-330, 10), (-290, 10), (-290, 330), (-330, 330)]), (150, 100, 60), line=5)
    cel(c, path([(290, 10), (330, 10), (330, 240), (290, 240)]), (150, 100, 60), line=5)   # the short leg
    if books:
        for i in range(3):   # the stack of little red guides under the short leg
            yy = 330 - (i + 1) * 30
            cel(c, path([(260 + i * 4, yy), (360 - i * 6, yy), (360 - i * 6, yy + 30), (260 + i * 4, yy + 30)]), (200, 30, 40), line=4.5)
            c.drawRect(skia.Rect.MakeLTRB(268 + i * 4, yy + 12, 350 - i * 6, yy + 15), P((255, 210, 100)))
    c.restore()


def book_stack(c, x, y, n, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(n):
        yy = -i * 34; dx = 6 * math.sin(i * 1.7)
        cel(c, path([(-120 + dx, yy - 32), (120 + dx, yy - 32), (120 + dx, yy), (-120 + dx, yy)]), (200, 30, 40), (150, 18, 30), path([(-130, yy - 10), (130, yy - 10), (130, yy + 2), (-130, yy + 2)]), 4.5)
        c.drawRect(skia.Rect.MakeLTRB(-90 + dx, yy - 18, 90 + dx, yy - 14), P((255, 210, 100)))
    c.restore()


def price_tag(c, x, y, text, s=1.0, rot=-12):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    tg = path([(-150, -70), (110, -70), (170, 0), (110, 70), (-150, 70)]); cel(c, tg, (255, 230, 120), line=5.5)
    c.drawCircle(108, 0, 14, P((255, 255, 255))); c.drawCircle(108, 0, 14, S(INK, 4))
    outline_text(c, text, -30, 26, 76, (40, 30, 30), INK, 0.1, shadow=False)
    c.restore()


def plate(c, x, y, s=1.0, t=0.0, steam=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(ell(0, 0, 260, 70), P((250, 250, 250))); c.drawPath(ell(0, 0, 260, 70), S(INK, 5))
    c.drawPath(ell(0, -6, 190, 46), S((200, 200, 210), 4))
    food = path([(-120, -10), (-90, -70), (-30, -96), (40, -90), (110, -50), (124, -6), (0, 10)], smooth=True); cel(c, food, (200, 110, 60), (160, 80, 40), path([(0, -100), (140, -100), (140, 20), (0, 20)]), 5)
    for (fx, fy, fc) in ((-50, -70, (60, 160, 70)), (30, -82, (230, 60, 60)), (80, -52, (60, 160, 70))): c.drawCircle(fx, fy, 16, P(fc)); c.drawCircle(fx, fy, 16, S(INK, 3.5))
    if steam:
        for i in range(3):
            st = skia.Path(); x0 = -60 + i * 60; st.moveTo(x0, -120)
            for k in range(4): st.quadTo(x0 + 20 * math.sin(t * 4 + i + k), -150 - k * 40, x0, -180 - k * 40)
            c.drawPath(st, S((255, 255, 255), 7, 0.6))
    c.restore()


def chef_hat(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    puff = path([(-120, 0), (-150, -90), (-100, -170), (-30, -190), (40, -200), (110, -160), (150, -80), (120, 0)], smooth=True); cel(c, puff, (255, 255, 255), (220, 224, 236), path([(40, -220), (200, -220), (200, 20), (40, 20)]), 5.5)
    cel(c, path([(-120, 0), (120, 0), (120, 70), (-120, 70)]), (255, 255, 255), (220, 224, 236), path([(40, 0), (140, 0), (140, 80), (40, 80)]), 5.5)
    c.restore()


def road_sign(c, x, y, text, s=1.0, col=(255, 200, 40)):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeLTRB(-14, 0, 14, 600), P((150, 150, 160))); c.drawRect(skia.Rect.MakeLTRB(-14, 0, 14, 600), S(INK, 4))
    sg = path([(-300, -120), (240, -120), (320, -40), (240, 40), (-300, 40)]); cel(c, sg, col, line=6)
    sz = 80; f = font("Bangers.ttf", sz)
    while f.measureText(text) > 480 and sz > 40: sz -= 4; f = font("Bangers.ttf", sz)
    outline_text(c, text, -30, -40 + sz * 0.34, sz, (40, 30, 30), INK, 0.1, shadow=False)
    c.restore()


# ------------------------------------------------------------------ more props (8 Nov v3: "show things more")
def gift_box(c, x, y, s=1.0, col=(250, 70, 110), rib=(255, 214, 60)):
    c.save(); c.translate(x, y); c.scale(s, s)
    cel(c, path([(-130, -60), (130, -60), (130, 130), (-130, 130)]), col, tuple(int(v * 0.75) for v in col), path([(40, -70), (140, -70), (140, 140), (40, 140)]), 6)
    cel(c, path([(-150, -110), (150, -110), (150, -50), (-150, -50)]), col, line=6)
    c.drawRect(skia.Rect.MakeLTRB(-22, -110, 22, 130), P(rib)); c.drawRect(skia.Rect.MakeLTRB(-22, -110, 22, 130), S(INK, 4))
    for sx in (-1, 1): cel(c, ell(sx * 50, -140, 56, 30), rib, line=5)
    c.restore()


def shop_bag(c, x, y, s=1.0, col=(24, 160, 160)):
    c.save(); c.translate(x, y); c.scale(s, s)
    h = skia.Path(); h.moveTo(-60, -110); h.cubicTo(-60, -200, 60, -200, 60, -110); c.drawPath(h, S(INK, 12))
    cel(c, path([(-130, -110), (130, -110), (150, 150), (-150, 150)]), col, tuple(int(v * 0.75) for v in col), path([(40, -120), (160, -120), (160, 160), (40, 160)]), 6)
    outline_text(c, "$", 0, 70, 150, (255, 214, 60), INK, 10, shadow=False)
    c.restore()


def coin(c, x, y, r=50, rot=0.0):
    c.save(); c.translate(x, y); c.scale(max(0.15, abs(math.cos(rot))), 1)
    c.drawCircle(0, 0, r, P((255, 200, 50))); c.drawCircle(0, 0, r * 0.78, S((220, 150, 30), 5)); c.drawCircle(0, 0, r, S(INK, 5))
    outline_text(c, "$", 0, r * 0.38, r * 1.1, (220, 150, 30), INK, 0.1, shadow=False)
    c.restore()


def bookmark(c, x, y, s=1.0, col=(255, 214, 60)):
    c.save(); c.translate(x, y); c.scale(s, s)
    cel(c, path([(-70, -100), (70, -100), (70, 110), (0, 60), (-70, 110)]), col, line=7); c.restore()


def bubble(c, x, y, s=1.0, text="...", col=(255, 250, 240)):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = skia.Path(); b.addRoundRect(skia.Rect.MakeLTRB(-200, -110, 200, 90), 60, 60)
    b = skia.Op(b, path([(-120, 60), (-40, 60), (-150, 170)]), skia.PathOp.kUnion_PathOp); cel(c, b, col, line=7)
    outline_text(c, text, 0, 22, 90, INK, INK, 0.1, shadow=False); c.restore()


def share_arrow(c, x, y, s=1.0, col=(120, 240, 220)):
    c.save(); c.translate(x, y); c.scale(s, s)
    cel(c, path([(-110, 80), (-110, 10), (-40, -60), (40, -60), (40, -120), (140, -20), (40, 80), (40, 20), (-20, 20), (-60, 60)]), col, line=7); c.restore()


def magnifier(c, x, y, s=1.0, rot=-30):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    cel(c, path([(-18, 90), (18, 90), (22, 260), (-22, 260)]), (120, 70, 40), line=6)
    c.drawCircle(0, 0, 100, P((200, 235, 255), 0.6)); c.drawCircle(0, 0, 100, S((90, 90, 110), 18)); c.drawCircle(0, 0, 100, S(INK, 5))
    c.drawArc(skia.Rect.MakeLTRB(-70, -70, 70, 70), 200, 60, False, S((255, 255, 255), 10)); c.restore()


def banner(c, t, lines, y=330, col=(255, 214, 60), bg=(40, 20, 70), t0=-1.0, width=980):
    """the episode title: on screen from the very first frame"""
    k = back(pr(t, t0, 0.3), 1.8)
    if k <= 0: return
    c.save(); c.translate(W / 2, y); c.scale(k, k)
    hgt = sum(sz for _, sz in lines) * 1.1 + 40
    c.drawRoundRect(skia.Rect.MakeLTRB(-width / 2, -40, width / 2, hgt - 40), 26, 26, P(bg, 0.92)); c.drawRoundRect(skia.Rect.MakeLTRB(-width / 2, -40, width / 2, hgt - 40), 26, 26, S(col, 7))
    yy = 0
    for ln, sz in lines:
        f_ = font("Bangers.ttf", sz); s_ = sz
        while f_.measureText(ln) > width - 70 and s_ > 40: s_ -= 3; f_ = font("Bangers.ttf", s_)
        outline_text(c, ln, 0, yy + s_ * 0.82, s_, col if yy else (255, 250, 240), INK, 9); yy += sz * 1.1
    c.restore()
