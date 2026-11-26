"""PAPER look (from reference 4): one signature paper colour per series, paper-sticker cut-outs with white borders and soft
shadows dropped in like they were placed by hand, hand-drawn 'boiling' hero words (12 fps redraw, scribble -> word),
small italic serif captions low-centre, warm film finish."""
import math
import numpy as np
from PIL import Image, ImageFilter
from doc_kit import *
import doc_kit as _dk
_FC = _dk._FC
FD = _dk.FD

SERIF_I = _dk.FD + 'InstrumentSerif-Italic.ttf'
CREAM = (246, 238, 224)


def serif(size):
    k = ('si', size)
    if k not in _FC: _FC[k] = skia.Font(skia.Typeface.MakeFromFile(SERIF_I), size)
    return _FC[k]


# ---------------------------------------------------------------- paper stage
_PAPER = {}


def paper_img(col):
    if col in _PAPER: return _PAPER[col]
    rng = np.random.default_rng(7)
    n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 18) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)).resize((W, H)), np.float32) - 128
    fib = np.zeros((H, W), np.float32)
    for _ in range(900):
        x, y = rng.integers(0, W), rng.integers(0, H); L = rng.integers(10, 60); a = rng.uniform(0, math.pi)
        for s in range(L):
            xx, yy = int(x + s * math.cos(a)), int(y + s * math.sin(a))
            if 0 <= xx < W and 0 <= yy < H: fib[yy, xx] += rng.uniform(4, 10)
    yy, xx = np.mgrid[0:H, 0:W]; light = 1.08 - 0.28 * (((xx - W * 0.45) / W) ** 2 + ((yy - H * 0.4) / H) ** 2) ** 0.5 * 2
    base = np.array(col, np.float32)[None, None, :] * light[..., None] + (n * 0.55 + fib * 0.6)[..., None]
    im = Image.fromarray(base.clip(0, 255).astype(np.uint8)); _PAPER[col] = sk(im); return _PAPER[col]


def paper(c, col, t=0.0, drift=0.0):
    img = paper_img(col); s = 1.04 + drift * 0.02
    c.save(); c.translate(W / 2, H / 2); c.scale(s, s); c.translate(-W / 2 + 10 * math.sin(t * 0.3), -H / 2)
    c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear)); c.restore()


# ---------------------------------------------------------------- stickers
def drop_k(t, t0, d=0.35):
    """placed-by-hand: overshoot scale, settle, tiny rotation wobble"""
    u = cl((t - t0) / d); return u


def sticker_img(c, img, cx, cy, w, k, rot=0.0, border=16, shadow=1.0, radius=10):
    """photo sticker: white border, rounded corners, soft drop shadow, drop-in from slightly larger + higher"""
    if k <= 0 or img is None: return
    h = w * img.height() / img.width(); s = 1.0 + 0.18 * (1 - eback(k)); lift = 40 * (1 - eo(k))
    c.save(); c.translate(cx, cy - lift); c.rotate(rot + 4 * (1 - eo(k))); c.scale(s, s)
    R = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h); RB = R.makeOutset(border, border)
    sh = P((20, 8, 30), 0.45 * shadow * eo(k)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16 + 18 * (1 - eo(k))))
    c.drawRRect(skia.RRect.MakeRectXY(RB.makeOffset(10, 18 + 30 * (1 - eo(k))), radius, radius), sh)
    c.drawRRect(skia.RRect.MakeRectXY(RB, radius, radius), P((250, 248, 242)))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(R, radius * 0.6, radius * 0.6), doAntiAlias=True)
    cover(c, img, 1.0, rect=R); c.restore(); c.restore()


def sticker_draw(c, draw, cx, cy, w, h, k, rot=0.0, border=16, bg=(250, 248, 242), radius=26):
    """vector-drawn prop on a white-bordered die-cut card"""
    if k <= 0: return
    s = 1.0 + 0.18 * (1 - eback(k)); lift = 40 * (1 - eo(k))
    c.save(); c.translate(cx, cy - lift); c.rotate(rot + 4 * (1 - eo(k))); c.scale(s, s)
    R = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h)
    sh = P((20, 8, 30), 0.45 * eo(k)); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16 + 18 * (1 - eo(k))))
    c.drawRRect(skia.RRect.MakeRectXY(R.makeOffset(10, 18 + 30 * (1 - eo(k))), radius, radius), sh)
    c.drawRRect(skia.RRect.MakeRectXY(R, radius, radius), P(bg))
    draw(c); c.restore()


# ---------------------------------------------------------------- hand-drawn boiling text
def text_path(txt, f, track=-0.02):
    g = f.textToGlyphs(txt); ws = f.getWidths(g); p = skia.Path(); x = 0.0
    for gi, w in zip(g, ws):
        gp = f.getPath(gi)
        if gp is not None: p.addPath(gp, x, 0)
        x += w + track * f.getSize()
    return p, x


def boil_text(c, txt, x, y, size, t, t0, col=CREAM, ink=(40, 16, 60), align='c', font=None, fps=12, scribble=0.28):
    """word drawn by hand: scribble grows into the word over ~scribble s, then 'boils' (re-drawn at 12 fps)"""
    if t < t0: return
    f = font or cond(size); p, w = text_path(txt, f)
    xx = x - w / 2 if align == 'c' else x
    seed = int((t - t0) * fps) + 1; u = (t - t0) / scribble
    c.save(); c.translate(xx, y)
    if u < 1:   # scribble phase: loopy line that grows across the word box
        rng = np.random.default_rng(seed); sp = skia.Path(); n = int(6 + 30 * u); sp.moveTo(0, -size * 0.35)
        for i in range(n):
            px = w * (i + 1) / 36; py = -size * 0.35 + size * 0.38 * math.sin(i * 1.9 + seed) + rng.uniform(-10, 10)
            sp.quadTo(px - 20, py - size * 0.4 * rng.uniform(-1, 1), px, py)
        pen = S(col, max(6, size * 0.06)); pen.setPathEffect(skia.DiscretePathEffect.Make(10, 3, seed)); c.drawPath(sp, pen)
        c.restore(); return
    fill = P(col); fill.setPathEffect(skia.DiscretePathEffect.Make(9, size * 0.012 + 1.2, seed))
    sh = P(ink, 0.55); sh.setPathEffect(skia.DiscretePathEffect.Make(9, size * 0.012 + 1.2, seed + 7))
    c.save(); c.translate(5, 7); c.drawPath(p, sh); c.restore()
    c.drawPath(p, fill)
    edge = S(ink, max(2.0, size * 0.012), 0.5); edge.setPathEffect(skia.DiscretePathEffect.Make(7, 1.6, seed + 3)); c.drawPath(p, edge)
    c.restore()


def scap(c, T, t, t0, t1, y=1360, size=58, col=CREAM, maxw=860):
    """italic serif caption, one phrase at a time (words appear as spoken)"""
    ws = [(w, a) for (w, a, b) in T.AL if t0 - 0.01 <= a < t1]
    shown = [w for (w, a) in ws if a - 0.03 <= t]
    if not shown or t > t1 + 0.15: return
    f = serif(size); s = ' '.join(shown); full = ' '.join(w for w, a in ws)
    lines = []; cur = ''
    for w in full.split(' '):
        if f.measureText((cur + ' ' + w).strip()) > maxw: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    lines.append(cur)
    n = len(shown); k = 0
    for li, L in enumerate(lines):
        words = L.split(' '); vis = ' '.join(words[:max(0, min(len(words), n - k))]); k += len(words)
        if not vis: continue
        lw = f.measureText(vis); yy = y + li * size * 1.05
        c.drawString(vis, W / 2 - lw / 2, yy, f, glow_paint(col, 1.0))
