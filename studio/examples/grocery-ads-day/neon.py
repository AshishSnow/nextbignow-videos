"""NEON STORY look (owner reference 18 Nov: detailed cartoon room, moody purple/magenta neon + warm lamp, a character with a feeling,
one prop that tells the story). Everything drawn in code so it can be animated (parallax layers, blinking neon, sweat drops, camera drift).
Text lives *in the world* (neon signs, sticky notes, screens) instead of floating captions."""
import os, math, random
import numpy as np
import skia

W, H = 1080, 1920
FD = '/home/claude/studio/fonts/ttf'
_TF = {}
INK = (14, 10, 22)


def font(name, size):
    if name not in _TF: _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FD, name))
    f = skia.Font(_TF[name], size); f.setEdging(skia.Font.Edging.kAntiAlias); return f


def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)


def P(rgb, a=1.0, blur=0):
    p = skia.Paint(AntiAlias=True); p.setColor4f(C(rgb, a))
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def S(rgb, w, a=1.0, blur=0):
    p = P(rgb, a, blur); p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w)
    p.setStrokeJoin(skia.Paint.kRound_Join); p.setStrokeCap(skia.Paint.kRound_Cap); return p


def LG(p0, p1, cols, pos=None):
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([p0, p1], [C(c) if len(c) == 3 else C(c[:3], c[3]) for c in cols], pos)); return p


def RG(cx, cy, r, cols, pos=None):
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeRadial((cx, cy), r, [C(c) if len(c) == 3 else C(c[:3], c[3]) for c in cols], pos)); return p


def path(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p


def inked(c, shape, fill, ow=7):
    """draw shape (Path/RRect/Rect) with fill paint then a black ink outline."""
    d = {skia.Path: c.drawPath, skia.RRect: c.drawRRect, skia.Rect: c.drawRect}[type(shape)]
    d(shape, fill); d(shape, S(INK, ow))


def glow(c, shape, rgb, r=40, a=0.8):
    d = {skia.Path: c.drawPath, skia.RRect: c.drawRRect, skia.Rect: c.drawRect}[type(shape)]
    d(shape, P(rgb, a, r))


def light_cone(c, x, y, w0, w1, h, rgb, a=0.22):
    c.drawPath(path([(x - w0 / 2, y), (x + w0 / 2, y), (x + w1 / 2, y + h), (x - w1 / 2, y + h)]),
               LG((x, y), (x, y + h), [rgb + (a,), rgb + (0.0,)]))


def neon_text(c, s, x, y, size, rgb, flick=1.0, fontname='Montserrat-Black.ttf', rot=0):
    """DAY look: bold comic lettering - colour fill, thick ink outline, hard drop shadow, white shine."""
    f = font(fontname, size); tw = f.measureText(s); a = max(0.0, min(1.0, flick))
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawString(s, -tw / 2 + size * 0.06, size * 0.07, f, P(INK, 0.85 * a))
    c.drawString(s, -tw / 2, 0, f, S(INK, size * 0.16, a))
    c.drawString(s, -tw / 2, 0, f, P(rgb, a))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-tw / 2 - 10, -size * 0.75, tw + 20, size * 0.28)); c.drawString(s, -tw / 2, 0, f, P((255, 255, 255), 0.35 * a)); c.restore()
    c.restore(); return tw


def board(c, x, y, w, h, col=(255, 255, 255)):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 30, 30)
    c.drawRRect(r.makeOffset(10, 12) if hasattr(r, 'makeOffset') else r, P(INK, 0.25, 6)); inked(c, r, P(col), 7)


def sparkle(c, x, y, r, a=1.0):
    if a <= 0: return
    c.drawCircle(x, y, r * 0.9, P((255, 255, 255), 0.45 * a, r * 0.6))
    for ang in (0, 90):
        c.save(); c.translate(x, y); c.rotate(ang)
        p = skia.Path(); p.moveTo(0, -r); p.quadTo(r * 0.12, -r * 0.12, r, 0); p.quadTo(r * 0.12, r * 0.12, 0, r); p.quadTo(-r * 0.12, r * 0.12, -r, 0); p.quadTo(-r * 0.12, -r * 0.12, 0, -r); p.close()
        c.drawPath(p, P((255, 255, 255), a)); c.restore()


def cloud(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for (cx, cy, r) in ((0, 0, 80), (90, -40, 100), (200, -10, 85), (280, 20, 60), (-80, 25, 55)): p.addCircle(cx, cy, r)
    p.addRect(skia.Rect.MakeXYWH(-130, 20, 470, 60))
    p2 = skia.Op(p, skia.Path(), skia.PathOp.kUnion_PathOp) or p
    c.drawPath(p2, P((255, 255, 255))); c.drawPath(p2, S((120, 170, 220), 5))
    c.drawRect(skia.Rect.MakeXYWH(-130, 50, 470, 30), P((215, 235, 252)))
    c.restore()


def grain(c, seed=1, a=0.06):
    rnd = np.random.default_rng(seed); n = (rnd.random((H // 2, W // 2)) * 255).astype(np.uint8)
    img = np.dstack([n, n, n, np.full_like(n, int(255 * a))])
    im = skia.Image.fromarray(np.ascontiguousarray(img), colorType=skia.kRGBA_8888_ColorType)
    c.drawImageRect(im, skia.Rect.MakeWH(W, H))


def vignette(c, a=0.55):
    c.drawRect(skia.Rect.MakeWH(W, H), RG(540, 960, 1250, [(0, 0, 0, 0.0), (0, 0, 0, 0.0), (0, 0, 0, a)], [0, 0.55, 1]))


# ------------------------------------------------------------------ characters
SKIN = (255, 214, 170)


def drop(c, x, y, s=1.0, a=1.0):
    p = skia.Path(); p.moveTo(x, y - 26 * s); p.cubicTo(x + 16 * s, y - 2 * s, x + 16 * s, y + 14 * s, x, y + 14 * s)
    p.cubicTo(x - 16 * s, y + 14 * s, x - 16 * s, y - 2 * s, x, y - 26 * s); p.close()
    c.drawPath(p, P((120, 220, 255), a)); c.drawPath(p, S(INK, 3.5, a)); c.drawCircle(x - 4 * s, y + 2 * s, 3.5 * s, P((255, 255, 255), 0.9 * a))


def head(c, x, y, r, base, mood='happy', look=(0, 0), sweat=0, t=0.0, blink=False):
    hi = tuple(min(255, v + 90) for v in base); lo = tuple(int(v * 0.55) for v in base)
    c.drawCircle(x, y, r, RG(x - r * 0.35, y - r * 0.45, r * 1.5, [hi, base, lo], [0, 0.45, 1]))
    c.drawCircle(x, y, r, S(INK, 7))
    c.drawOval(skia.Rect.MakeXYWH(x - r * 0.62, y - r * 0.78, r * 0.55, r * 0.28), P((255, 255, 255), 0.55))
    c.drawCircle(x + r * 0.3, y - r * 0.62, r * 0.07, P((255, 255, 255), 0.5))
    ex, ey, ew, eh = r * 0.33, y - r * 0.05, r * 0.27, r * 0.34
    for sgn in (-1, 1):
        cx = x + sgn * ex + look[0] * 4
        if blink:
            c.drawLine(cx - ew, ey, cx + ew, ey, S(INK, 6)); continue
        o = skia.Rect.MakeXYWH(cx - ew, ey - eh, ew * 2, eh * 2)
        c.drawOval(o, P((255, 250, 235))); c.drawOval(o, S(INK, 5))
        px, py = cx + look[0] * ew * 0.45, ey + look[1] * eh * 0.4
        c.drawCircle(px, py, ew * 0.48, P(INK)); c.drawCircle(px - ew * 0.15, py - ew * 0.18, ew * 0.16, P((255, 255, 255)))
        if mood == 'worried':
            c.drawLine(cx - ew * 0.9, ey - eh * 1.25 + sgn * (-8), cx + ew * 0.9, ey - eh * 1.25 + sgn * 8, S(INK, 7))
        elif mood == 'happy':
            a = skia.Path(); a.addArc(skia.Rect.MakeXYWH(cx - ew, ey - eh * 1.7, ew * 2, eh * 1.0), 200, 140); c.drawPath(a, S(INK, 6))
    m = skia.Path()
    if mood == 'happy':
        m.moveTo(x - r * 0.32, y + r * 0.38); m.cubicTo(x - r * 0.2, y + r * 0.72, x + r * 0.2, y + r * 0.72, x + r * 0.32, y + r * 0.38); m.close()
        c.drawPath(m, P((120, 20, 30))); c.drawPath(m, S(INK, 6))
        c.save(); c.clipPath(m, doAntiAlias=True); c.drawOval(skia.Rect.MakeXYWH(x - r * 0.18, y + r * 0.5, r * 0.36, r * 0.3), P((255, 110, 120))); c.restore()
    elif mood == 'worried':
        m.moveTo(x - r * 0.2, y + r * 0.55); m.cubicTo(x - r * 0.08, y + r * 0.42, x + r * 0.08, y + r * 0.42, x + r * 0.2, y + r * 0.55); c.drawPath(m, S(INK, 7))
    elif mood == 'shock':
        o = skia.Rect.MakeXYWH(x - r * 0.15, y + r * 0.32, r * 0.3, r * 0.38); c.drawOval(o, P((120, 20, 30))); c.drawOval(o, S(INK, 6))
        c.drawOval(skia.Rect.MakeXYWH(x - r * 0.08, y + r * 0.52, r * 0.16, r * 0.14), P((255, 110, 120)))
    else:
        m.moveTo(x - r * 0.25, y + r * 0.45); m.cubicTo(x - r * 0.1, y + r * 0.58, x + r * 0.1, y + r * 0.58, x + r * 0.25, y + r * 0.45); c.drawPath(m, S(INK, 7))
    for i in range(sweat):
        ph = (t * 0.6 + i * 0.37) % 1.0
        drop(c, x + r * (0.55 + 0.12 * i) * (1 if i % 2 == 0 else -0.9), y - r * 0.35 + ph * r * 0.9, 1.1, 1 - ph ** 3)


def limb(c, pts, w, col):
    p = skia.Path(); p.moveTo(*pts[0])
    if len(pts) == 3: p.quadTo(*pts[1], *pts[2])
    else: p.lineTo(*pts[1])
    c.drawPath(p, S(INK, w + 12)); c.drawPath(p, S(col, w))


def hand(c, x, y, r=26):
    c.drawCircle(x, y, r, P(SKIN)); c.drawCircle(x, y, r, S(INK, 6)); c.drawCircle(x - r * 0.3, y - r * 0.35, r * 0.25, P((255, 240, 220), 0.7))


def person(c, x, y, s, headcol, jacket, pants=(40, 44, 70), mood='happy', look=(0, 0), sweat=0, t=0.0, arm_r=None, arm_l=None, tie=None, shirt=None, prop=None, blink=False, lean=0.0):
    """standing character, feet at (x, y). s = scale (1 = about 640 px tall). arm_* = hand target relative to shoulder."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-130, -18, 260, 40), P((0, 0, 0), 0.35, 8))
    for sx in (-1, 1):
        limb(c, [(sx * 40, -270), (sx * 48, -150), (sx * 52, -40)], 58, pants)
        sh = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx * 52 - 46 + sx * 10, -52, 92, 50), 24, 24)
        inked(c, sh, P((245, 245, 250)), 6); c.drawLine(sx * 52 - 40 + sx * 10, -14, sx * 52 + 40 + sx * 10, -14, S((200, 200, 215), 6))
    body = skia.Path(); body.moveTo(-105, -470); body.cubicTo(-125, -380, -112, -300, -95, -250); body.lineTo(95, -250)
    body.cubicTo(112, -300, 125, -380, 105, -470); body.cubicTo(60, -505, -60, -505, -105, -470); body.close()
    hi = tuple(min(255, v + 50) for v in jacket)
    c.drawPath(body, LG((-100, -500), (100, -250), [hi, jacket, tuple(int(v * 0.7) for v in jacket)]))
    if shirt:
        v = path([(-40, -495), (40, -495), (0, -380)]); c.drawPath(v, P(shirt))
        if tie: c.drawPath(path([(-14, -480), (14, -480), (22, -370), (0, -340), (-22, -370)]), P(tie)); c.drawPath(path([(-14, -480), (14, -480), (22, -370), (0, -340), (-22, -370)]), S(INK, 4))
    else:
        c.drawLine(0, -490, 0, -255, S(INK, 4)); c.drawLine(-60, -300, -60, -260, S(INK, 3)); c.drawLine(60, -300, 60, -260, S(INK, 3))
    c.drawPath(body, S(INK, 7))
    c.drawRect(skia.Rect.MakeXYWH(-98, -272, 196, 26), P(tuple(int(v * 0.6) for v in jacket))); c.drawRect(skia.Rect.MakeXYWH(-98, -272, 196, 26), S(INK, 5))
    arm_r = arm_r or (40, 200); arm_l = arm_l or (-40, 200)
    for (sx, tgt) in ((1, arm_r), (-1, arm_l)):
        sxp, syp = sx * 98, -455; ex, ey = sxp + tgt[0], syp + tgt[1]
        mx, my = (sxp + ex) / 2 + sx * 40, (syp + ey) / 2 + 20
        limb(c, [(sxp, syp), (mx, my), (ex, ey)], 46, jacket)
        hand(c, ex, ey)
        if prop and prop[0] == sx: prop[1](c, ex, ey)
    c.restore()
    head(c, x + lean * s, y - 640 * s, 185 * s, headcol, mood, look, sweat, t, blink)


def keys(c, x, y):
    c.drawCircle(x, y - 40, 22, S((230, 230, 240), 8)); c.drawCircle(x, y - 40, 22, S(INK, 3))
    for i, a in enumerate((-40, 10)):
        c.save(); c.translate(x, y - 40); c.rotate(a)
        k = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-10, 18, 20, 70), 6, 6); inked(c, k, P((250, 220, 90) if i else (210, 215, 225)), 4)
        c.restore()
    fob = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 14, y - 110, 44, 64), 14, 14); inked(c, fob, P((30, 30, 40)), 4)
    c.drawCircle(x + 36, y - 90, 7, P((255, 60, 90)))


# ------------------------------------------------------------------ props
def car(c, x, y, w, body=(232, 38, 60), t=0.0, refl=True):
    s = w / 760; c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-380, 40, 760, 70), P((0, 0, 0), 0.55, 18))
    p = skia.Path(); p.moveTo(-370, 50); p.cubicTo(-385, -10, -360, -50, -280, -62); p.lineTo(-170, -72)
    p.cubicTo(-110, -165, -50, -178, 70, -178); p.cubicTo(160, -178, 200, -130, 245, -75); p.cubicTo(335, -66, 385, -35, 378, 50); p.close()
    hi = tuple(min(255, v + 80) for v in body); lo = tuple(int(v * 0.45) for v in body)
    c.drawPath(p, LG((0, -178), (0, 60), [hi, body, body, lo], [0, 0.35, 0.6, 1]))
    c.save(); c.clipPath(p, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(-400, -30, 800, 14), P((255, 255, 255), 0.35))
    c.drawRect(skia.Rect.MakeXYWH(-400, 10, 800, 60), P((60, 20, 80), 0.35))
    for i in range(3): c.drawRect(skia.Rect.MakeXYWH(-300 + i * 230 + 40 * math.sin(t * 0.8), -170, 30, 300), P((255, 150, 255), 0.12, 6))
    c.restore()
    w1 = path([(-150, -72), (-95, -150), (-5, -156), (-5, -72)]); w2 = path([(18, -72), (18, -156), (105, -154), (165, -110), (195, -72)])
    for wp in (w1, w2):
        c.drawPath(wp, LG((0, -156), (0, -72), [(150, 110, 220), (40, 30, 80)])); c.drawPath(wp, S(INK, 6))
        c.save(); c.clipPath(wp, doAntiAlias=True); c.drawPath(path([(-60, -160), (-20, -160), (-90, -60), (-130, -60)]), P((255, 255, 255), 0.25)); c.restore()
    c.drawPath(p, S(INK, 8))
    c.drawLine(10, -66, 10, 30, S(INK, 4)); c.drawLine(-160, -66, -180, 30, S(INK, 3))
    c.drawRoundRect(skia.Rect.MakeXYWH(40, -20, 40, 10), 5, 5, P(INK)); c.drawRoundRect(skia.Rect.MakeXYWH(-120, -20, 40, 10), 5, 5, P(INK))
    hl = skia.Path(); hl.addOval(skia.Rect.MakeXYWH(335, -40, 42, 26)); glow(c, hl, (255, 240, 180), 16, 0.9); inked(c, hl, P((255, 250, 220)), 4)
    c.drawRoundRect(skia.Rect.MakeXYWH(-382, -38, 22, 30), 6, 6, P((255, 40, 60))); c.drawRoundRect(skia.Rect.MakeXYWH(-382, -38, 22, 30), 6, 6, S(INK, 4))
    for wx in (-230, 225):
        c.drawCircle(wx, 48, 78, P(INK)); c.drawCircle(wx, 48, 70, P((34, 30, 44)))
        c.drawCircle(wx, 48, 44, RG(wx - 12, 34, 60, [(250, 250, 255), (150, 150, 170), (70, 70, 90)]))
        for k in range(5):
            a = t * 3 + k * 2 * math.pi / 5; c.drawLine(wx, 48, wx + 38 * math.cos(a), 48 + 38 * math.sin(a), S((90, 90, 110), 6))
        c.drawCircle(wx, 48, 44, S(INK, 5)); c.drawCircle(wx, 48, 10, P(INK))
    if refl:
        c.save(); c.translate(0, 210); c.scale(1, -0.45); c.drawPath(p, P(body, 0.16, 6)); c.restore()
    c.restore()


def coin(c, x, y, r=22, a=1.0):
    c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * 0.45 + 6, r * 2, r * 0.9), P((120, 80, 0), a))
    c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * 0.45, r * 2, r * 0.9), RG(x - r * 0.3, y - r * 0.3, r * 1.4, [(255, 245, 160), (255, 196, 40), (200, 130, 10)]))
    c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * 0.45, r * 2, r * 0.9), S(INK, 3.5, a))


def lamp(c, x, y, s=1.0, on=1.0):
    c.drawCircle(x, y - 120 * s, 260 * s, P((255, 170, 60), 0.35 * on, 60))
    shade = path([(x - 70 * s, y - 70 * s), (x + 70 * s, y - 70 * s), (x + 45 * s, y - 170 * s), (x - 45 * s, y - 170 * s)])
    c.drawPath(shade, LG((x, y - 170 * s), (x, y - 70 * s), [(255, 230, 150), (255, 160, 60)])); c.drawPath(shade, S(INK, 6))
    c.drawLine(x, y - 70 * s, x, y - 10 * s, S(INK, 10)); c.drawOval(skia.Rect.MakeXYWH(x - 45 * s, y - 20 * s, 90 * s, 26 * s), P((60, 40, 30))); c.drawOval(skia.Rect.MakeXYWH(x - 45 * s, y - 20 * s, 90 * s, 26 * s), S(INK, 5))


def sticky(c, x, y, s, rot, txt, size=60, col=(255, 236, 90), tc=(220, 30, 40)):
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.Rect.MakeXYWH(-90 * s, -90 * s, 180 * s, 180 * s); c.drawRect(r.makeOffset(8, 10), P((0, 0, 0), 0.35, 6)); inked(c, r, P(col), 4)
    f = font('PermanentMarker.ttf' if os.path.exists(os.path.join(FD, 'PermanentMarker.ttf')) else 'Anton.ttf', size * s)
    for i, line in enumerate(txt.split('\n')):
        c.drawString(line, -f.measureText(line) / 2, (-10 + i * size * 1.0) * s + size * 0.3 * s, f, P(tc))
    c.restore()


# ------------------------------------------------------------------ scenes
def skyline(c, x0, y0, w, h, t, seed=4):
    """DAY: bright blue sky, white clouds, sun sparkle, pastel city with white windows."""
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x0, y0, w, h))
    c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), LG((0, y0), (0, y0 + h), [(20, 130, 235), (70, 180, 250), (170, 225, 255), (225, 245, 255)], [0, 0.4, 0.8, 1]))
    c.drawCircle(x0 + w * 0.78, y0 + h * 0.18, 70, P((255, 255, 230))); c.drawCircle(x0 + w * 0.78, y0 + h * 0.18, 160, P((255, 255, 220), 0.5, 60))
    rnd = random.Random(seed)
    for k in range(3): cloud(c, x0 + (k * 0.36 + 0.05) * w + 20 * math.sin(t * 0.2 + k), y0 + h * (0.22 + 0.12 * (k % 2)), 0.55 + 0.15 * (k % 2))
    for layer, (col, hmax, win) in enumerate([((150, 195, 240), 0.5, (230, 245, 255)), ((90, 150, 220), 0.6, (255, 255, 255))]):
        x = x0 - 20
        while x < x0 + w:
            bw = rnd.randint(50, 120); bh = h * rnd.uniform(0.18, hmax)
            r = skia.Rect.MakeXYWH(x, y0 + h - bh, bw, bh); c.drawRect(r, P(col)); c.drawRect(r, S((60, 100, 170), 3))
            for wy in range(int(y0 + h - bh + 16), int(y0 + h), 26):
                for wx in range(int(x + 10), int(x + bw - 10), 22):
                    if rnd.random() < 0.55: c.drawRect(skia.Rect.MakeXYWH(wx, wy, 9, 12), P(win, 0.9))
            x += bw + rnd.randint(0, 12)
    c.restore()


def showroom(t=0.0):
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, 1100), [(18, 12, 34), (38, 22, 66)]))
    # back wall window
    wx, wy, ww, wh = 60, 420, 960, 600
    skyline(c, wx, wy, ww, wh, t)
    for i in range(1, 4): c.drawRect(skia.Rect.MakeXYWH(wx + i * ww / 4 - 7, wy, 14, wh), P((24, 16, 44)))
    c.drawRect(skia.Rect.MakeXYWH(wx, wy + wh * 0.38, ww, 12), P((24, 16, 44)))
    c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), S((24, 16, 44), 22)); c.drawRect(skia.Rect.MakeXYWH(wx - 11, wy - 11, ww + 22, wh + 22), S(INK, 6))
    c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), P((90, 40, 160), 0.12))
    # neon title sign on the wall above the window
    fl = 1.0 if (t % 3.1) > 0.12 else 0.35
    c.drawRoundRect(skia.Rect.MakeXYWH(90, 250, 900, 150), 30, 30, P((10, 6, 20), 0.7))
    neon_text(c, 'THE CAR BARELY PAYS', 540, 345, 70, (255, 60, 200), fl)
    # floor
    fy = wy + wh + 10
    c.drawRect(skia.Rect.MakeXYWH(0, fy, W, H - fy), LG((0, fy), (0, H), [(60, 30, 90), (24, 14, 40)]))
    for i in range(-8, 9): c.drawLine(540 + i * 40, fy, 540 + i * 260, H, S((255, 150, 255), 2, 0.12))
    for j, yy in enumerate([fy + 40, fy + 110, fy + 210, fy + 350, fy + 540, fy + 800]): c.drawLine(0, yy, W, yy, S((255, 150, 255), 2, 0.10))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(wx + 40 + i * 170, fy, 60, 500), LG((0, fy), (0, fy + 500), [(255, 140, 200, 0.18), (255, 140, 200, 0.0)]))
    # ceiling spots
    for sx in (360, 720):
        light_cone(c, sx, 0, 60, 520, fy + 240, (255, 210, 255), 0.13)
    # salesman desk (left)
    lamp(c, 120, 1180, 0.9)
    desk = skia.Rect.MakeXYWH(20, 1180, 360, 40); inked(c, desk, LG((0, 1240), (0, 1280), [(120, 70, 50), (70, 40, 30)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(40, 1220, 320, 200), P((60, 34, 26))); c.drawRect(skia.Rect.MakeXYWH(40, 1220, 320, 200), S(INK, 6))
    person(c, 250, 1440, 0.56, (70, 140, 255), (235, 235, 245), pants=(50, 50, 70), mood='worried', look=(0.6, 0.8), sweat=3, t=t,
           arm_r=(10, 250), arm_l=(70, 255), tie=(230, 40, 60), shirt=(250, 250, 255))
    coin(c, 330, 1172, 18)
    sticky(c, 95, 1100, 0.55, -8, '5%', size=90)
    # car + hero
    car(c, 560, 1440, 800, t=t)
    person(c, 880, 1790, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(-0.5, -0.4), t=t,
           arm_r=(150, -170), arm_l=(-30, 230), prop=(1, keys))
    c.drawRect(skia.Rect.MakeWH(W, H), P((255, 40, 180), 0.05))
    vignette(c); grain(c, int(t * 24) % 7)
    return s


def bay(t=0.0):
    s = skia.Surface(W, H); c = s.getCanvas()
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, 1100), [(8, 20, 34), (20, 40, 70)]))
    for i in range(7): c.drawRect(skia.Rect.MakeXYWH(i * 160, 500, 150, 520), P((14, 30, 52))); c.drawRect(skia.Rect.MakeXYWH(i * 160, 500, 150, 520), S((40, 90, 130), 4))
    for i in range(6):
        for j in range(4): c.drawRect(skia.Rect.MakeXYWH(i * 160 + 18, 520 + j * 120, 114, 90), P((60, 200, 255), 0.06))
    fl = 1.0 if (t % 2.3) > 0.1 else 0.3
    c.drawRoundRect(skia.Rect.MakeXYWH(120, 250, 840, 190), 30, 30, P((4, 10, 18), 0.75))
    neon_text(c, 'SERVICE', 400, 380, 92, (40, 230, 255), fl)
    neon_text(c, '50%', 790, 395, 130, (80, 255, 140), 1.0)
    fy = 1020
    c.drawRect(skia.Rect.MakeXYWH(0, fy, W, H - fy), LG((0, fy), (0, H), [(40, 60, 80), (14, 20, 30)]))
    for i in range(-8, 9): c.drawLine(540 + i * 40, fy, 540 + i * 260, H, S((120, 220, 255), 2, 0.1))
    c.drawPath(path([(380, fy + 160), (700, fy + 160), (760, fy + 900), (320, fy + 900)]), P((255, 210, 0), 0.10))
    for sx in (300, 780): light_cone(c, sx, 0, 50, 460, fy + 200, (190, 240, 255), 0.13)
    # lift + car
    for px in (330, 760):
        c.drawRect(skia.Rect.MakeXYWH(px - 22, 760, 44, 420), LG((px - 22, 0), (px + 22, 0), [(255, 200, 40), (200, 140, 0)])); c.drawRect(skia.Rect.MakeXYWH(px - 22, 760, 44, 420), S(INK, 6))
    c.drawRect(skia.Rect.MakeXYWH(230, 1000, 620, 26), P((90, 100, 120))); c.drawRect(skia.Rect.MakeXYWH(230, 1000, 620, 26), S(INK, 6))
    car(c, 545, 930, 700, body=(232, 38, 60), t=t, refl=False)
    # tires stack + oil drums
    for i in range(4):
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(40, 1300 - i * 62, 190, 60), 28, 28); inked(c, r, LG((0, 0), (190, 0), [(30, 30, 36), (70, 70, 80), (30, 30, 36)]), 6)
    for i, dx in enumerate((900, 990)):
        d = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(dx - 50, 1180, 100, 150), 12, 12); inked(c, d, LG((dx - 50, 0), (dx + 50, 0), [(20, 90, 160), (60, 160, 230), (20, 90, 160)]), 6)
        c.drawLine(dx - 50, 1220, dx + 50, 1220, S(INK, 4)); c.drawLine(dx - 50, 1290, dx + 50, 1290, S(INK, 4))
    # cash register fountain
    rx, ry = 560, 1560
    c.drawCircle(rx, ry - 140, 300, P((255, 200, 60), 0.30, 70))
    reg = path([(rx - 170, ry), (rx + 170, ry), (rx + 140, ry - 170), (rx - 140, ry - 170)]); inked(c, reg, LG((0, ry - 170), (0, ry), [(255, 210, 90), (200, 120, 20)]), 7)
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(rx - 80, ry - 260, 160, 80), 10, 10); inked(c, scr, P((20, 30, 30)), 6)
    c.drawString('$$$', rx - 52, ry - 202, font('Anton.ttf', 52), P((80, 255, 140)))
    for i in range(3):
        for j in range(4): c.drawRoundRect(skia.Rect.MakeXYWH(rx - 110 + j * 58, ry - 150 + i * 44, 44, 32), 6, 6, P((90, 50, 10), 0.6))
    drw = skia.Rect.MakeXYWH(rx - 190, ry, 380, 60); inked(c, drw, P((170, 100, 20)), 7)
    rnd = random.Random(2)
    for k in range(40):
        ph = (t * 0.7 + rnd.random()) % 1.0; ang = rnd.uniform(-1.2, 1.2); v = rnd.uniform(500, 900)
        x = rx + math.sin(ang) * v * ph; y = ry - 20 - (math.cos(ang) * v * ph - 900 * ph * ph)
        coin(c, x, y, rnd.uniform(16, 26), 1.0)
    # mechanic + hero reacting
    person(c, 920, 1760, 0.58, (70, 140, 255), (110, 120, 140), pants=(80, 90, 110), mood='happy', look=(-0.8, -0.2), t=t,
           arm_r=(-60, 150), arm_l=(-80, 120))
    person(c, 170, 1800, 0.66, (255, 140, 40), (36, 44, 90), mood='worried', look=(0.8, -0.3), sweat=2, t=t, arm_r=(40, 220), arm_l=(-40, 220))
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 200, 255), 0.04))
    vignette(c); grain(c, 3)
    return s


if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lab'); os.makedirs(out, exist_ok=True)
    showroom(1.0).makeImageSnapshot().save(os.path.join(out, 'N_showroom.png'), skia.kPNG)
    bay(1.0).makeImageSnapshot().save(os.path.join(out, 'N_bay.png'), skia.kPNG)
    print('ok')
