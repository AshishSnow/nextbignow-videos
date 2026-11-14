"""Shared photo helpers for the editorial look: load, cover-crop, cut-outs with shadow, framed photo cards, credits."""
import os, math
import numpy as np
import skia
from PIL import Image
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
LX = 90
IMG = os.environ.get('PK_IMG', '')
# ------------------------------------------------------------------ photos
_IM = {}
def img(name, maxw=2000):
    if name not in _IM:
        im = Image.open(name if os.path.isabs(name) else os.path.join(IMG, name)).convert('RGBA')
        im.thumbnail((maxw, maxw * 2))
        _IM[name] = skia.Image.fromarray(np.ascontiguousarray(np.array(im)), colorType=skia.kRGBA_8888_ColorType)
    return _IM[name]


SAMP = skia.SamplingOptions(skia.FilterMode.kLinear)


def cover(c, im, x, y, w, h, zoom=1.0, fx=0.5, fy=0.5, a=1.0):
    """draw image to fill rect (x,y,w,h), cropped; zoom>1 pushes in around focus (fx,fy)."""
    iw, ih = im.width(), im.height()
    s = max(w / iw, h / ih) * zoom
    sw, sh = w / s, h / s
    sx = cl(fx * iw - sw / 2, 0, iw - sw) if iw > sw else 0
    sy = cl(fy * ih - sh / 2, 0, ih - sh) if ih > sh else 0
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, R.MakeXYWH(sx, sy, sw, sh), R.MakeXYWH(x, y, w, h), SAMP, p)


def cutout(c, name, cx, by, h, k=1.0, shadow=True, bw=False, a=1.0):
    """cut-out PNG standing with its bottom at by, height h, centred on cx; rises in with k."""
    if k <= 0: return
    im = img(name, 1600)
    w = h * im.width() / im.height()
    yy = by - h + 80 * (1 - eo(cl(k)))
    p = skia.Paint(); p.setAlphaf(cl(k * 1.5) * a)
    if bw: p.setColorFilter(skia.ColorFilters.Matrix([0.3, 0.59, 0.11, 0, 0, 0.3, 0.59, 0.11, 0, 0, 0.3, 0.59, 0.11, 0, 0, 0, 0, 0, 1, 0]))
    if shadow:
        sp = skia.Paint(); sp.setImageFilter(skia.ImageFilters.DropShadowOnly(0, 24, 26, 26, skia.ColorSetARGB(int(255 * 0.35 * cl(k)), 0, 0, 0)))
        c.saveLayer(None, sp); c.drawImageRect(im, R.MakeXYWH(cx - w / 2, yy, w, h), SAMP); c.restore()
    c.drawImageRect(im, R.MakeXYWH(cx - w / 2, yy, w, h), SAMP, p)
    return (cx - w / 2, yy, w, h)


def photo_card(c, name, cx, cy, w, h, rot, k, zoom=1.0, fx=0.5, fy=0.5, pad=18, after=None):
    def dr(cc):
        cover(cc, img(name), pad, pad, w - 2 * pad, h - 2 * pad, zoom, fx, fy)
        if after: after(cc)
    card(c, cx, cy, w, h, rot, k, dr, rad=10)


def credit(c, s, a=1.0, col=GREY, y=1480):
    c.save(); c.translate(80, y); c.rotate(-90)
    mono(c, s, 0, 0, 17, col, a=a * 0.9)
    c.restore()


def shade(c, a, col=(0, 0, 0)):
    c.drawRect(R.MakeWH(W, H), paint(col, a))


def kicker(c, s, t, t0, y=400, col=GREY):
    k = pr(t, t0, 0.3)
    if k > 0:
        c.drawRect(R.MakeXYWH(LX, y - 22, 14, 14), paint(RED, k))
        mono(c, s, LX + 30, y - 8, 26, col, a=k)


