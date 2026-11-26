"""DOC look (documentary kinetic edit) for vertical Shorts: full-bleed photos with push-ins, film grade + grain,
kinetic per-word captions placed beside the subject, big condensed words tucked behind subjects, red name boxes,
flip counters, typewriter, highlighter, RGB-split glitch, whip cuts. Built from the 26 Nov reference breakdown."""
import sys, os, math, random
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from essay_lib import *          # skia, W, H, FPS, P, S, rr, pr, eo, eio, eback, cl, Timing-compatible helpers
from essay_kit import to_np, main  # noqa

FD = '/home/claude/studio/fonts/doc/'
_FC = {}


def dfont(name, size):
    k = (name, size)
    if k not in _FC: _FC[k] = skia.Font(skia.Typeface.MakeFromFile(FD + name + '.ttf'), size)
    return _FC[k]


def cond(size): return dfont('ArchivoCond-Black', size)       # big tucked words (Helvetica Condensed feel)
def capf(size): return dfont('Archivo-Bold', size)            # kinetic captions
def mono(size):
    k = ('mono', size)
    if k not in _FC: _FC[k] = skia.Font(skia.Typeface.MakeFromFile('/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'), size)
    return _FC[k]


RED = (226, 30, 38); WHITE_ = (255, 255, 255); BLACK = (8, 8, 8); PAPER = (236, 232, 222); HL = (255, 226, 60)


# ------------------------------------------------------------------ images
def grade(im, mode='bw', contrast=1.25, warm=0.0):
    im = im.convert('RGB')
    if mode == 'bw':
        g = ImageOps.grayscale(im); g = ImageOps.autocontrast(g, cutoff=1); im = Image.merge('RGB', (g, g, g))
    elif mode == 'warm':
        im = ImageEnhance.Color(im).enhance(1.15)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    if warm:
        a = np.asarray(im).astype(np.float32); a[..., 0] *= 1 + warm; a[..., 2] *= 1 - warm; im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im


def sk(im):
    """PIL -> skia image (RGBA)"""
    a = np.ascontiguousarray(np.asarray(im.convert('RGBA')))
    return skia.Image.fromarray(a, colorType=skia.kRGBA_8888_ColorType)


def cover(c, img, z=1.0, ox=0.0, oy=0.0, a=1.0, blur=0.0, rect=None):
    """draw img cover-fitted into rect (default full frame), zoom z, pan ox/oy in fraction of overflow"""
    R = rect or skia.Rect.MakeWH(W, H); rw, rh = R.width(), R.height()
    s = max(rw / img.width(), rh / img.height()) * z; w, h = img.width() * s, img.height() * s
    x = R.left() + (rw - w) / 2 + ox * (w - rw) / 2; y = R.top() + (rh - h) / 2 + oy * (h - rh) / 2
    p = skia.Paint(AntiAlias=True, Alphaf=a)
    if blur > 0.3: p.setImageFilter(skia.ImageFilters.Blur(blur, blur * 0.15))
    c.save(); c.clipRect(R); c.drawImageRect(img, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), p); c.restore()
    return x, y, s


def sticker(im_rgba, outline=10):
    """cut-out with a white outline (reference: subject sticker over halftone bg)"""
    a = im_rgba.split()[-1]
    big = a.filter(ImageFilter.MaxFilter(outline * 2 + 1))
    base = Image.new('RGBA', im_rgba.size, (255, 255, 255, 0)); white = Image.new('RGBA', im_rgba.size, (255, 255, 255, 255))
    base.paste(white, (0, 0), big); base.alpha_composite(im_rgba); return base


def key_white(im, thr=236):
    """object on white background -> RGBA cut-out"""
    im = im.convert('RGB'); a = np.asarray(im).astype(np.int16)
    m = ~((a[..., 0] > thr) & (a[..., 1] > thr) & (a[..., 2] > thr))
    mk = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert('RGBA'); out.putalpha(mk); return out.crop(mk.getbbox())


def halftone(im, cell=7):
    g = ImageOps.grayscale(im); w, h = g.size; sm = g.resize((w // cell, h // cell))
    out = Image.new('L', (w, h), 235); from PIL import ImageDraw; d = ImageDraw.Draw(out); A = np.asarray(sm)
    for j in range(A.shape[0]):
        for i in range(A.shape[1]):
            r = (1 - A[j, i] / 255) * cell * 0.72
            if r > 0.4: d.ellipse([i * cell + cell / 2 - r, j * cell + cell / 2 - r, i * cell + cell / 2 + r, j * cell + cell / 2 + r], fill=20)
    return out.convert('RGB')


# ------------------------------------------------------------------ film finish
_rng = np.random.default_rng(5)
_GR = [sk(Image.fromarray(np.dstack([(_rng.normal(128, 40, (480, 270))).clip(0, 255).astype(np.uint8)] * 3 + [np.full((480, 270), 255, np.uint8)])).resize((W, H), Image.NEAREST)) for _ in range(6)]


def film(c, t, grain=0.07, vig=0.55):
    p = skia.Paint(Alphaf=grain, BlendMode=skia.BlendMode.kOverlay)
    c.drawImage(_GR[int(t * 24) % len(_GR)], 0, 0, skia.SamplingOptions(), p)
    sh = skia.GradientShader.MakeRadial((W / 2, H / 2), H * 0.72, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, vig)], [0, 0.55, 1.0])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))


# ------------------------------------------------------------------ type
def shadow_paint(col, a=1.0, sh=0.55, r=10):
    p = P(col, a); p.setImageFilter(skia.ImageFilters.DropShadow(0, 4, r, r, skia.Color4f(0, 0, 0, sh * a))); return p


def kword(c, T, t, t0, t1, x, y, size=66, col=WHITE_, align='c', maxw=700, lh=1.05):
    """kinetic caption: words spoken between t0..t1 appear one at a time at (x, y); short pop-in"""
    ws = [(w, a, b) for (w, a, b) in T.AL if t0 - 0.01 <= a < t1]
    shown = [(w, a, b) for (w, a, b) in ws if a - 0.04 <= t]
    if not shown or t > t1 + 0.25: return
    f = capf(size); sp = f.measureText(' ')
    lines = [[]]; cw = 0
    for w, a, b in shown:
        ww = f.measureText(w)
        if lines[-1] and cw + sp + ww > maxw: lines.append([]); cw = 0
        lines[-1].append((w, a)); cw += (sp if cw else 0) + ww
    for li, L in enumerate(lines):
        tw = sum(f.measureText(w) for w, a in L) + sp * (len(L) - 1)
        xx = x - tw / 2 if align == 'c' else (x if align == 'l' else x - tw)
        yy = y + li * size * lh
        for w, a in L:
            k = cl((t - a + 0.04) / 0.12); s = 0.86 + 0.14 * eback(k)
            c.save(); c.translate(xx + f.measureText(w) / 2, yy); c.scale(s, s)
            c.drawString(w, -f.measureText(w) / 2, 0, f, shadow_paint(col, k)); c.restore()
            xx += f.measureText(w) + sp


def big_word(c, txt, x, y, size, k=1.0, col=WHITE_, align='c', track=0.0, sh=0.35):
    if k <= 0: return
    f = cond(size); w = f.measureText(txt)
    xx = x - w / 2 if align == 'c' else x
    c.save(); c.translate(0, 30 * (1 - eo(k)))
    c.drawString(txt, xx, y, f, shadow_paint(col, eo(k), sh, 14)); c.restore()


def name_box(c, txt, x, y, size=58, k=1.0, fill=RED, col=WHITE_):
    """red box + white condensed caps (reference: 'JAMIE DIMON' label)"""
    if k <= 0: return
    f = cond(size); w = f.measureText(txt); pad = size * 0.28
    c.save(); c.translate(x, y); c.scale(1, eo(k))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 - pad, -size * 0.92, w + 2 * pad, size * 1.16), P(fill))
    c.drawString(txt, -w / 2, 0, f, P(col)); c.restore()


def tag_boxes(c, words, x, y, size, ks):
    """black boxes with white text, stacked (reference: 'Boring / Conservative')"""
    f = capf(size)
    for i, (w, k) in enumerate(zip(words, ks)):
        if k <= 0: continue
        tw = f.measureText(w); yy = y + i * size * 1.3
        c.drawRect(skia.Rect.MakeXYWH(x - 14, yy - size * 0.95, (tw + 28) * eo(k), size * 1.22), P(BLACK, 0.92))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x - 14, yy - size, (tw + 28) * eo(k), size * 1.3)); c.drawString(w, x, yy, f, P(WHITE_)); c.restore()


def typewriter(c, txt, k, x, y, size=64, col=BLACK, cursor=True, t=0.0, f=None):
    f = f or mono(size); n = int(round(len(txt) * cl(k))); s = txt[:n]
    c.drawString(s, x, y, f, P(col))
    if cursor and (k < 1 or int(t * 2.4) % 2 == 0):
        cx = x + f.measureText(s) + 4; c.drawRect(skia.Rect.MakeXYWH(cx, y - size * 0.8, max(3, size * 0.07), size * 0.95), P(col))


def highlight(c, x, y, w, h, k, col=HL, a=0.85):
    if k <= 0: return
    p = P(col, a); p.setBlendMode(skia.BlendMode.kMultiply)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w * eo(k), h), p)


def rgb_split(c, draw, amt):
    """draw(c) three times in R/G/B channels with offsets (glitch)"""
    if amt < 0.5: draw(c); return
    for (dx, dy, col) in ((-amt, 0, (255, 0, 60)), (amt, amt * 0.3, (0, 220, 255)), (0, 0, None)):
        c.save(); c.translate(dx, dy)
        if col is not None:
            p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(skia.Color(*col), skia.BlendMode.kSrcIn)); p.setBlendMode(skia.BlendMode.kScreen)
            c.saveLayer(None, p); draw(c); c.restore()
        else: draw(c)
        c.restore()


def flip_counter(c, x, y, frm, to, k, size=150, label=None, t=0.0):
    """mechanical drum counter rolling digits from frm to to (reference: date drum)"""
    s_to = str(to); n = len(s_to); s_fr = str(frm).rjust(n, '0'); f = cond(size)
    cw = f.measureText('0') * 1.18; ch = size * 1.25; X0 = x - n * cw / 2
    shape_bg = rr(X0 - 30, y - ch / 2 - 30, n * cw + 60, ch + 60, 22)
    c.drawRRect(shape_bg, P((40, 40, 42))); c.drawRRect(shape_bg, S((120, 120, 120), 3))
    for i in range(n):
        d0, d1 = int(s_fr[i]), int(s_to[i]); kk = eo(cl(k * 1.4 - (n - 1 - i) * 0.12))
        steps = (d1 - d0) % 10 + 10 * (n - 1 - i); v = d0 + steps * kk
        cell = skia.Rect.MakeXYWH(X0 + i * cw + 6, y - ch / 2, cw - 12, ch)
        c.save(); c.clipRect(cell); c.drawRect(cell, P((232, 230, 224)))
        frac = v - math.floor(v)
        for j in (-1, 0, 1, 2):
            dig = str(int(math.floor(v) + j) % 10); yy = y + size * 0.36 + (j - frac) * ch
            c.drawString(dig, cell.centerX() - f.measureText(dig) / 2, yy, f, P(BLACK))
        sh = skia.GradientShader.MakeLinear([(0, cell.top()), (0, cell.bottom())], [skia.Color4f(0, 0, 0, .5), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, .5)], [0, .3, .7, 1])
        c.drawRect(cell, skia.Paint(Shader=sh)); c.restore()
        c.drawLine(cell.left(), y, cell.right(), y, S((0, 0, 0), 2, 0.5))
    if label: g = capf(34); c.drawString(label, x - g.measureText(label) / 2, y - ch / 2 - 56, g, P(WHITE_, 0.9))


def counter_text(c, val, x, y, size, k, prefix='', suffix='', col=WHITE_, align='c'):
    v = int(val * eo(k)); s = prefix + '{:,}'.format(v) + suffix; f = cond(size); w = f.measureText(s)
    c.drawString(s, x - w / 2 if align == 'c' else x, y, f, shadow_paint(col, 1.0, 0.4, 14))


def card(c, img, cx, cy, w, h, rot=0.0, k=1.0, border=14, z=1.0, shadow=True, persp=0.0):
    """photo print / screen card with white border, drop shadow, optional fake 3D skew"""
    if k <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(rot); s = 0.6 + 0.4 * eback(k); c.scale(s, s)
    if persp: c.skew(persp, 0)
    R = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    if shadow:
        p = P((0, 0, 0), 0.55 * k); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18)); c.drawRect(R.makeOffset(10, 18), p)
    c.drawRect(R.makeOutset(border, border), P(WHITE_, k))
    cover(c, img, z, rect=R, a=k)
    c.restore()


def whip(t, t0, d=0.16):
    """0..1 whip amount right after a cut"""
    return max(0.0, 1 - (t - t0) / d) if t0 <= t < t0 + d else 0.0


def flash(c, t, t0, d=0.08, a=0.85):
    if t0 <= t < t0 + d: c.drawRect(skia.Rect.MakeWH(W, H), P(WHITE_, a * (1 - (t - t0) / d)))
