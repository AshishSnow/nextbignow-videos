"""BRIGHT EXPLAINER kit for OopsMyBusiness (owner, 11 Nov 2026: "make my video colourful, not like anime, not like paper ... well explainer,
colourful, nice intro"). Built on the look he approved on the McDonald's reel v3 ("this what I want"): designed bright sets with a big colour
circle, real-looking objects (3D renders cut out), big words tucked behind objects, editorial two-tier type, cards with a subtle 3D lift,
graphs; screen shake on impacts. Clean (no grain, no outlines), vibrant, soft shadows. Skia.
"""
import math, os
import numpy as np, skia, cv2

W, H = 1080, 1920
_S = os.environ.get("STUDIO", "/home/claude/studio"); _FD = f"{_S}/fonts/ttf"; _TFC = {}


def tf(name):
    if name not in _TFC: _TFC[name] = skia.Typeface.MakeFromFile(f"{_FD}/{name}")
    return _TFC[name]


def font(name, size): return skia.Font(tf(name), size)


BLACK_F, XB_F, SB_F, ANTON = "Montserrat-Black.ttf", "Montserrat-ExtraBold.ttf", "Montserrat-SemiBold.ttf", "Anton.ttf"
NAVY = (18, 22, 48); WHITE = (255, 255, 255); YEL = (255, 206, 0); RED = (240, 52, 60); GRN = (20, 200, 110); BLU = (20, 120, 255)
ORG = (255, 128, 20); PNK = (255, 70, 150); TEAL = (0, 196, 190); PUR = (124, 60, 255); CREAM = (255, 246, 230)


def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)


def P(col, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor4f(C(col, a)); return p


def S(col, w, a=1.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    p.setColor4f(C(col, a)); return p


def lin(x0, y0, x1, y1, cols, pos=None):
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [C(c) for c in cols], pos)); return p


def rad(x, y, r, cols, pos=None):
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), r, [C(c[:3], c[3] if len(c) > 3 else 1) for c in cols], pos)); return p


def path(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p


def rrect(x0, y0, x1, y1, r):
    p = skia.Path(); p.addRoundRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), r, r); return p


def ease(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def eout(x): x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3


def back(x, s=1.7): x = min(1.0, max(0.0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def pr(t, t0, d): return min(1.0, max(0.0, (t - t0) / d)) if d > 0 else float(t >= t0)


def shade(col, k): return tuple(int(max(0, min(255, v * k))) for v in col)


def shadow(c, pth, dx=0, dy=24, blur=30, a=0.35, col=NAVY):
    p = P(col, a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    c.save(); c.translate(dx, dy); c.drawPath(pth, p); c.restore()


# ------------------------------------------------------------------ sets
def set_bg(c, top, bot, circle=None, cx=540, cy=900, r=440, t=0.0, rays=False):
    """designed bright set: rich gradient, soft light, a big colour circle, optional slow rays"""
    c.drawRect(skia.Rect.MakeWH(W, H), lin(0, 0, 0, H, [top, bot]))
    c.drawRect(skia.Rect.MakeWH(W, H), rad(540, 700, 1100, [(255, 255, 255, 0.22), (255, 255, 255, 0.0)]))
    if rays:
        c.save(); c.translate(cx, cy); c.rotate(t * 6)
        for i in range(16):
            c.drawPath(path([(0, 0), (1600 * math.cos(math.radians(i * 22.5 - 4)), 1600 * math.sin(math.radians(i * 22.5 - 4))),
                             (1600 * math.cos(math.radians(i * 22.5 + 4)), 1600 * math.sin(math.radians(i * 22.5 + 4)))]), P(WHITE, 0.07))
        c.restore()
    if circle:
        cp = skia.Path(); cp.addCircle(cx, cy, r); shadow(c, cp, 0, 30, 50, 0.25)
        c.drawCircle(cx, cy, r, rad(cx - r * 0.35, cy - r * 0.4, r * 1.6, [shade(circle, 1.18), circle, shade(circle, 0.8)], [0, 0.55, 1]))


def floor_shadow(c, x, y, w, a=0.28):
    p = P(NAVY, a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)); c.drawOval(skia.Rect.MakeLTRB(x - w / 2, y - w * 0.07, x + w / 2, y + w * 0.07), p)


# ------------------------------------------------------------------ images (3D renders cut out)
_IMG = {}


def load_img(path_):
    if path_ not in _IMG:
        a = cv2.imread(path_, cv2.IMREAD_UNCHANGED); a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA)
        ys, xs = np.where(a[..., 3] > 8); a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1].copy()   # trim
        _IMG[path_] = skia.Image.fromarray(np.ascontiguousarray(a), colorType=skia.kRGBA_8888_ColorType)
    return _IMG[path_]


def obj(c, path_, x, y, h, rot=0.0, a=1.0, shadow_=True, flip=False):
    """draw a cut-out with its bottom-centre at (x, y), height h"""
    im = load_img(path_); s = h / im.height(); w = im.width() * s
    if shadow_: floor_shadow(c, x, y - 6, w * 0.95)
    c.save(); c.translate(x, y); c.rotate(rot)
    if flip: c.scale(-1, 1)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(a)
    c.drawImageRect(im, skia.Rect.MakeLTRB(-w / 2, -h, w / 2, 0), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear), p)
    c.restore()


# ------------------------------------------------------------------ type
def text(c, s, x, y, size, col=WHITE, fnt=BLACK_F, align="c", a=1.0, shadow_=True, track=0, maxw=None):
    f = font(fnt, size)
    if maxw:
        while f.measureText(s) > maxw and size > 20: size -= 3; f = font(fnt, size)
    w = f.measureText(s); xs = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    if shadow_:
        sp = P(NAVY, 0.35 * a); sp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8)); c.drawString(s, xs, y + size * 0.06, f, sp)
    c.drawString(s, xs, y, f, P(col, a)); return w


def big_word(c, s, y, col, size=330, a=0.95, x=540):
    """a huge editorial word drawn BEHIND the object (call before obj)"""
    f = font(ANTON, size)
    while f.measureText(s) > 1000 and size > 120: size -= 10; f = font(ANTON, size)
    w = f.measureText(s); c.drawString(s, x - w / 2, y, f, P(col, a))


def tag(c, s, x, y, size=46, bg=YEL, fg=NAVY, rot=0.0, k=1.0, pad=26):
    """pill label (the small tier of the two-tier type)"""
    if k <= 0: return
    f = font(XB_F, size); w = f.measureText(s)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    p = rrect(-w / 2 - pad, -size * 0.85, w / 2 + pad, size * 0.45, size * 0.65); shadow(c, p, 0, 10, 14, 0.3)
    c.drawPath(p, P(bg)); c.drawString(s, -w / 2, size * 0.12, f, P(fg)); c.restore()


def headline(c, t, t0, small, big, y=430, col=YEL, size=120, t1=None, small_bg=WHITE, small_fg=NAVY):
    """two-tier editorial caption: small pill + one big punch line; slides up + pops"""
    if t < t0 or (t1 is not None and t > t1): return
    k = back(pr(t, t0, 0.28), 1.8); dy = 40 * (1 - eout(pr(t, t0, 0.28)))
    if small: tag(c, small, 540, y - size * 0.95 + dy, 44, small_bg, small_fg, k=k)
    c.save(); c.translate(540, y + dy); c.scale(k, k); text(c, big, 0, size * 0.3, size, col, BLACK_F, maxw=900); c.restore()


def sticker(c, s, x, y, size=80, bg=RED, fg=WHITE, rot=-8, k=1.0):
    """price sticker: thick white border, slight tilt, pops in"""
    if k <= 0: return
    f = font(BLACK_F, size); w = f.measureText(s)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    p = rrect(-w / 2 - 34, -size * 0.95, w / 2 + 34, size * 0.5, 26); shadow(c, p, 0, 14, 16, 0.35)
    c.drawPath(p, P(WHITE)); c.drawPath(rrect(-w / 2 - 22, -size * 0.83, w / 2 + 22, size * 0.38, 18), P(bg))
    c.drawString(s, -w / 2, size * 0.12, f, P(fg)); c.restore()


def card(c, x, y, w, h, col=WHITE, k=1.0, tilt=0.0, r=36, body=None, a=1.0):
    """card with a subtle 3D lift: soft shadow, top highlight, slight perspective tilt (tilt in -1..1)"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    m = skia.Matrix(); m.setAll(1, 0, 0, 0, 1, 0, tilt * 0.00035, 0, 1); c.concat(m)
    p = rrect(-w / 2, -h / 2, w / 2, h / 2, r); shadow(c, p, 0, 26, 30, 0.3 * a)
    c.drawPath(p, lin(0, -h / 2, 0, h / 2, [shade(col, 1.04), shade(col, 0.93)]))
    c.save(); c.clipPath(p, doAntiAlias=True); c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, -h / 2 + 8), P(WHITE, 0.5)); c.restore()
    if body: body(c)
    c.restore()


# ------------------------------------------------------------------ icons (flat, shaded, no outlines)
def icon_building(c, x, y, s=1.0, col=BLU, lit=0.6):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = path([(-140, 0), (-140, -380), (140, -380), (140, 0)]); shadow(c, body, 10, 16, 18, 0.25)
    c.drawPath(body, lin(-140, 0, 140, 0, [shade(col, 1.12), shade(col, 0.85)]))
    for r_ in range(6):
        for k in range(4):
            c.drawRoundRect(skia.Rect.MakeXYWH(-112 + k * 60, -350 + r_ * 56, 40, 36), 6, 6, P(CREAM if (r_ * 4 + k) % 3 else (180, 220, 255), lit))
    c.drawRect(skia.Rect.MakeLTRB(-40, -60, 40, 0), P(NAVY, 0.7)); c.restore()


def icon_truck(c, x, y, s=1.0, col=GRN, t=0.0, label=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    box = rrect(-220, -230, 90, -40, 18); shadow(c, box, 8, 14, 14, 0.25); c.drawPath(box, lin(0, -230, 0, -40, [shade(col, 1.1), shade(col, 0.85)]))
    cab = path([(90, -40), (90, -190), (180, -190), (230, -110), (230, -40)]); c.drawPath(cab, P(shade(col, 0.95)))
    c.drawPath(path([(110, -170), (170, -170), (205, -115), (110, -115)]), P((200, 235, 255)))
    for wx in (-150, 150):
        c.save(); c.translate(wx, -30); c.rotate(t * 600); c.drawCircle(0, 0, 46, P((30, 30, 36))); c.drawCircle(0, 0, 20, P((180, 186, 200)))
        c.drawRect(skia.Rect.MakeLTRB(-4, -20, 4, 20), P((120, 124, 140))); c.restore()
    if label: text(c, label, -65, -110, 52, WHITE, BLACK_F, shadow_=False)
    c.restore()


def icon_van(c, x, y, s=1.0, col=WHITE, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = path([(-230, -40), (-230, -230), (110, -230), (190, -140), (230, -120), (230, -40)]); shadow(c, body, 8, 14, 16, 0.25)
    c.drawPath(body, lin(0, -230, 0, -40, [shade(col, 1.0), shade(col, 0.86)]))
    c.drawPath(path([(120, -210), (180, -145), (120, -145)]), P((170, 215, 255)))
    c.drawRect(skia.Rect.MakeLTRB(-230, -110, 230, -96), P(ORG))
    for wx in (-140, 140):
        c.save(); c.translate(wx, -36); c.rotate(t * 600); c.drawCircle(0, 0, 44, P((30, 30, 36))); c.drawCircle(0, 0, 18, P((180, 186, 200))); c.restore()
    c.restore()


def icon_bin(c, x, y, s=1.0, col=(80, 90, 110), lid=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    b = path([(-150, -300), (150, -300), (120, 0), (-120, 0)]); shadow(c, b, 6, 14, 16, 0.25)
    c.drawPath(b, lin(-150, 0, 150, 0, [shade(col, 1.15), shade(col, 0.8)]))
    for k in range(4): c.drawRect(skia.Rect.MakeLTRB(-110 + k * 70, -260, -96 + k * 70, -40), P(shade(col, 0.7)))
    c.save(); c.translate(-160, -300); c.rotate(-lid * 40); c.drawRoundRect(skia.Rect.MakeLTRB(0, -36, 320, 0), 12, 12, P(shade(col, 1.25))); c.restore()
    c.restore()


def icon_coin(c, x, y, r=46, rot=0.0):
    c.save(); c.translate(x, y); c.scale(max(0.12, abs(math.cos(rot))), 1)
    c.drawCircle(0, 4, r, P((200, 140, 0))); c.drawCircle(0, 0, r, rad(-r * 0.3, -r * 0.3, r * 1.4, [(255, 236, 120), (255, 196, 0), (230, 160, 0)]))
    f = font(BLACK_F, r * 1.1); w = f.measureText("$"); c.drawString("$", -w / 2, r * 0.38, f, P((200, 130, 0))); c.restore()


def icon_spray(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    bt = rrect(-60, -200, 60, 0, 30); shadow(c, bt, 6, 12, 12, 0.25); c.drawPath(bt, lin(-60, 0, 60, 0, [(120, 220, 255), (40, 150, 230)]))
    c.drawRect(skia.Rect.MakeLTRB(-30, -260, 30, -200), P(WHITE)); c.drawPath(path([(30, -260), (110, -250), (110, -224), (30, -224)]), P(WHITE))
    for i in range(8):
        a_ = (t * 3 + i * 0.13) % 1; c.drawCircle(130 + a_ * 160, -240 + (i - 4) * 10 * a_, 8 * (1 - a_), P((200, 240, 255), 0.8))
    c.restore()


def icon_wrench(c, x, y, s=1.0, rot=-40):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(skia.Rect.MakeLTRB(-20, -40, 20, 220), 18, 18, lin(-20, 0, 20, 0, [(220, 224, 236), (140, 146, 160)]))
    hp = skia.Path(); hp.addCircle(0, -70, 62); cut = skia.Path(); cut.addRect(skia.Rect.MakeLTRB(-24, -150, 24, -70)); hp = skia.Op(hp, cut, skia.PathOp.kDifference_PathOp)
    c.drawPath(hp, lin(-60, 0, 60, 0, [(230, 234, 244), (150, 156, 170)])); c.restore()


def icon_wheel(c, x, y, r=60, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(0, 0, r, P((34, 34, 40))); c.drawCircle(0, 0, r * 0.45, P((160, 166, 180))); c.drawRect(skia.Rect.MakeLTRB(-r, -6, r, 6), P((60, 60, 70)))
    c.restore()


def people_icon(c, kind, x, y, s=1.0, col=BLU):
    """buyer types as round badges: startup laptop, tutoring board, clinic cross, co-working desks"""
    c.save(); c.translate(x, y); c.scale(s, s)
    cp = skia.Path(); cp.addCircle(0, 0, 110); shadow(c, cp, 0, 12, 16, 0.3)
    c.drawCircle(0, 0, 110, rad(-40, -40, 180, [shade(col, 1.2), col, shade(col, 0.82)]))
    if kind == "startup":
        c.drawRoundRect(skia.Rect.MakeLTRB(-60, -46, 60, 26), 8, 8, P(WHITE)); c.drawRect(skia.Rect.MakeLTRB(-50, -36, 50, 16), P((40, 60, 120)))
        c.drawRoundRect(skia.Rect.MakeLTRB(-80, 26, 80, 40), 6, 6, P(CREAM)); text(c, "</>", 0, 0, 34, YEL, XB_F, shadow_=False)
    elif kind == "tutor":
        c.drawRoundRect(skia.Rect.MakeLTRB(-70, -56, 70, 30), 8, 8, P((30, 90, 60))); c.drawRect(skia.Rect.MakeLTRB(-70, -56, 70, 30), S(CREAM, 6))
        text(c, "A+", 0, 6, 50, WHITE, BLACK_F, shadow_=False); c.drawRect(skia.Rect.MakeLTRB(-6, 30, 6, 66), P(CREAM))
    elif kind == "clinic":
        c.drawRect(skia.Rect.MakeLTRB(-22, -66, 22, 66), P(WHITE)); c.drawRect(skia.Rect.MakeLTRB(-66, -22, 66, 22), P(WHITE))
    elif kind == "cowork":
        for k in (-1, 1):
            c.drawRoundRect(skia.Rect.MakeLTRB(k * 50 - 34, -40, k * 50 + 34, -4), 6, 6, P(CREAM)); c.drawCircle(k * 50, 30, 20, P(WHITE))
    c.restore()


def badge(c, n, x, y, k=1.0, col=YEL, size=120):
    """STEP n badge"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    cp = skia.Path(); cp.addCircle(0, 0, size); shadow(c, cp, 0, 16, 20, 0.35)
    c.drawCircle(0, 0, size, rad(-size * 0.3, -size * 0.4, size * 1.6, [shade(col, 1.15), col, shade(col, 0.85)]))
    text(c, "STEP", 0, -size * 0.28, size * 0.26, NAVY, XB_F, shadow_=False)
    text(c, str(n), 0, size * 0.62, size * 0.95, NAVY, BLACK_F, shadow_=False); c.restore()


def bars(c, x, y, vals, cols, labels, k=1.0, hmax=420, w=150, gap=60):
    """bar chart that grows in"""
    n = len(vals); vmax = max(vals); x0 = x - (n * w + (n - 1) * gap) / 2
    for i, (v, col, lab) in enumerate(zip(vals, cols, labels)):
        h = hmax * v / vmax * eout(min(1, max(0, k * 1.4 - i * 0.2)))
        bx = x0 + i * (w + gap); p = rrect(bx, y - h, bx + w, y, 18); shadow(c, p, 0, 10, 12, 0.25)
        c.drawPath(p, lin(bx, 0, bx + w, 0, [shade(col, 1.12), shade(col, 0.86)]))
        text(c, lab, bx + w / 2, y + 56, 40, WHITE, XB_F, maxw=w + gap)


# ------------------------------------------------------------------ finish
_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = (1.0 - 0.22 * (((_xx - W / 2) / (W * 0.8)) ** 2 + ((_yy - H / 2) / (H * 0.8)) ** 2))[..., None]


def finish(img, flash=0.0):
    lum = img.mean(2, keepdims=True); img = lum + (img - lum) * 1.08   # a touch more colour
    img = img * _VIG
    if flash: img = img * (1 - flash) + flash
    return np.clip(img, 0, 1)
