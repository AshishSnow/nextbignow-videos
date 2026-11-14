"""Vintage comic + modern editorial kit: newsprint paper, Ben-Day dots, inked panels with hard shadows, caption boxes,
burst balloons, speech bubbles, outlined comic titles (Luckiest Guy) paired with clean Inter sublines."""
import os, math
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text as etext, mono, PAPER, INK, RED, RED_D, YEL, BLUE, GREEN, GREY

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fonts')
_TF = {}
def tf(name):
    if name not in _TF: _TF[name] = skia.Typeface.MakeFromFile(os.path.join(FD, name))
    return _TF[name]

NEWS = (252, 241, 210); NEWS_D = (240, 214, 160); KINK = (18, 16, 20)
CRED = (230, 40, 46); CYEL = (255, 210, 50); CBLU = (40, 120, 220); CCYN = (60, 200, 230)


def font(name, size):
    f = skia.Font(tf(name), size); f.setEdging(skia.Font.Edging.kAntiAlias); return f


def width(s, name, size): return font(name, size).measureText(s)


def dots(c, rect, col, cell=18, rmax=6.5, grad=(0.0, 1.0), angle=45, a=1.0):
    """Ben-Day dot field inside rect; dot radius ramps across grad (0..1 along the diagonal)."""
    x, y, w, h = rect
    c.save(); c.clipRect(R.MakeXYWH(x, y, w, h)); c.translate(x + w / 2, y + h / 2); c.rotate(angle)
    L = int(math.hypot(w, h) / 2) + cell
    p = paint(col, a)
    for i in range(-L, L, cell):
        for j in range(-L, L, cell):
            u = (i + L) / (2 * L)
            k = cl((u - grad[0]) / max(1e-6, grad[1] - grad[0]))
            r = rmax * k
            if r > 0.6: c.drawCircle(i, j, r, p)
    c.restore()


def paper(c, t=0.0, tint=NEWS):
    c.drawRect(R.MakeWH(W, H), paint(tint))
    dots(c, (0, 0, W, H), NEWS_D, cell=22, rmax=7, grad=(0.55, 1.0), angle=30)
    for i in range(260):  # paper fibres / speckle
        c.drawCircle(hsh(i, 71) * W, hsh(i, 72) * H, 0.8 + 1.6 * hsh(i, 73), paint((120, 100, 70), 0.08 + 0.1 * hsh(i, 74)))
    c.drawRect(R.MakeWH(W, H), paint(shader=skia.GradientShader.MakeRadial((W / 2, H / 2), 1250, [argb((0, 0, 0), 0), argb((90, 50, 10), 0.12)])))


def bg_flat(c, col, dotcol, t=0.0):
    c.drawRect(R.MakeWH(W, H), paint(col))
    dots(c, (0, 0, W, H), dotcol, cell=20, rmax=7.5, grad=(0.2, 1.0), angle=45)
    c.drawRect(R.MakeWH(W, H), paint(shader=skia.GradientShader.MakeRadial((W / 2, H / 2), 1250, [argb((0, 0, 0), 0), argb((0, 0, 0), 0.25)])))


def panel(c, x, y, w, h, fill=PAPER, rot=0.0, k=1.0, draw=None, border=9, shadow=14):
    if k <= 0: return
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot); s = 0.85 + 0.15 * eback(cl(k), 1.6); c.scale(s, s)
    c.translate(-w / 2, -h / 2)
    c.drawRect(R.MakeXYWH(shadow, shadow, w, h), paint(KINK, cl(k)))
    c.drawRect(R.MakeXYWH(0, 0, w, h), paint(fill, cl(k)))
    if draw:
        c.save(); c.clipRect(R.MakeXYWH(0, 0, w, h)); draw(c); c.restore()
    c.drawRect(R.MakeXYWH(0, 0, w, h), stroke(KINK, border, cl(k)))
    c.restore()


def caption(c, s, x, y, k=1.0, col=CYEL, size=30, rot=-2):
    if k <= 0: return
    f = font('SpecialElite.ttf', size); w = f.measureText(s) + 40; h = size * 1.6
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(R.MakeXYWH(7, 7, w, h), paint(KINK, k))
    c.drawRect(R.MakeXYWH(0, 0, w, h), paint(col, k))
    c.drawRect(R.MakeXYWH(0, 0, w, h), stroke(KINK, 5, k))
    c.drawString(s, 20, h * 0.68, f, paint(KINK, k))
    c.restore()


def title(c, s, x, y, size, col=CRED, k=1.0, align='l', outline=None, shadow=10, rot=0.0):
    """comic title: Luckiest Guy, thick black outline, hard offset shadow; pops in with k."""
    if k <= 0: return
    f = font('LuckiestGuy.ttf', size); w = f.measureText(s)
    ox = {'l': 0, 'c': -w / 2, 'r': -w}[align]
    sc = eback(cl(k), 2.2)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    ol = outline if outline is not None else size * 0.09
    c.drawString(s, ox + shadow, shadow, f, paint(KINK, cl(k)))
    c.drawString(s, ox, 0, f, stroke(KINK, ol * 2, cl(k)))
    c.drawString(s, ox, 0, f, paint(col, cl(k)))
    c.restore()


def burst(c, x, y, r, s, k=1.0, col=CYEL, txt=CRED, size=None, spikes=14, rot=0.0):
    if k <= 0: return
    sc = eback(cl(k), 2.5)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    pts = []
    for i in range(spikes * 2):
        a = i / (spikes * 2) * math.tau
        rr = r * (1.0 if i % 2 == 0 else 0.68) * (0.92 + 0.16 * hsh(i, 81))
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    c.save(); c.translate(10, 10); c.drawPath(poly(pts, True), paint(KINK)); c.restore()
    c.drawPath(poly(pts, True), paint(col)); c.drawPath(poly(pts, True), stroke(KINK, 7))
    c.restore()
    title(c, s, x, y + (size or r * 0.38) * 0.36, size or r * 0.38, txt, k, 'c', shadow=5, rot=rot)


def bubble(c, x, y, w, h, s, tail, k=1.0, size=40):
    if k <= 0: return
    sc = eback(cl(k), 2)
    c.save(); c.translate(x, y); c.scale(sc, sc)
    rr = skia.RRect.MakeOval(R.MakeXYWH(-w / 2, -h / 2, w, h))
    tp = poly([(-30, h / 2 - 20), (30, h / 2 - 20), (tail[0] - x, tail[1] - y)], True)
    for dx in (8,):
        c.save(); c.translate(dx, dx); c.drawRRect(rr, paint(KINK)); c.drawPath(tp, paint(KINK)); c.restore()
    c.drawPath(tp, paint(PAPER)); c.drawPath(tp, stroke(KINK, 6))
    c.drawRRect(rr, paint(PAPER)); c.drawRRect(rr, stroke(KINK, 6))
    c.drawRect(R.MakeXYWH(-26, h / 2 - 26, 52, 16), paint(PAPER))
    c.restore()
    title(c, s, x, y + size * 0.36, size, KINK, k, 'c', outline=0.01, shadow=0)


def bars(c, x, y, w, h, items, k, ymax):
    n = len(items); bw = w / n * 0.6
    c.drawLine(x, y + h, x + w, y + h, stroke(KINK, 6))
    for i, (lab, v, vs, col) in enumerate(items):
        kk = cl(k * n - i * 0.7)
        bh = h * v / ymax * eo(kk)
        bx = x + (i + 0.2) * w / n
        c.drawRect(R.MakeXYWH(bx + 10, y + h - bh + 10, bw, bh), paint(KINK))
        c.drawRect(R.MakeXYWH(bx, y + h - bh, bw, bh), paint(col))
        dots(c, (bx, y + h - bh, bw, bh), KINK, cell=14, rmax=3.4, grad=(0.0, 1.0), a=0.35)
        c.drawRect(R.MakeXYWH(bx, y + h - bh, bw, bh), stroke(KINK, 6))
        if kk > 0.6: title(c, vs, bx + bw / 2, y + h - bh - 24, 52, col, 1.0, 'c', shadow=5)
        c.drawString(lab, bx + bw / 2 - width(lab, 'SpecialElite.ttf', 28) / 2, y + h + 44, font('SpecialElite.ttf', 28), paint(KINK))
