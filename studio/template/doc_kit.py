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


# ================================================================== v2 (26 Nov, after owner's frame-by-frame notes)
# Grade: faded/matte film look like the references (lifted blacks, softened whites, ~35% desaturated, cool shadows).
def grade_filter(desat=0.38, lift=0.075, gain=0.85, cool=0.018):
    s = 1 - desat; lr, lg, lb = 0.2126 * desat, 0.7152 * desat, 0.0722 * desat
    m = [gain * (s + lr), gain * lg, gain * lb, 0, lift - cool * 0.4,
         gain * lr, gain * (s + lg), gain * lb, 0, lift + cool * 0.2,
         gain * lr, gain * lg, gain * (s + lb), 0, lift + cool,
         0, 0, 0, 1, 0]
    return skia.ColorFilters.Matrix(m)


GRADE = grade_filter()


def soft_edges(surf, amt=9.0):
    """tilt-shift: blur the top and bottom bands of the finished frame (references keep only the middle sharp)"""
    img = surf.makeImageSnapshot(); c = surf.getCanvas()
    c.saveLayer(None, None)
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(amt, amt)); c.drawImage(img, 0, 0, skia.SamplingOptions(), p)
    m = skia.Paint(BlendMode=skia.BlendMode.kDstIn)
    m.setShader(skia.GradientShader.MakeLinear([(0, 0), (0, H)], [skia.Color4f(0, 0, 0, 1), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 1)], [0, 0.26, 0.74, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), m); c.restore()


def halation(surf, a=0.22, r=26):
    """bloom on highlights (soft glow around bright areas / white text)"""
    img = surf.makeImageSnapshot(); c = surf.getCanvas()
    p = skia.Paint(Alphaf=a, BlendMode=skia.BlendMode.kScreen)
    p.setImageFilter(skia.ImageFilters.Blur(r, r, skia.TileMode.kDecal, skia.ImageFilters.ColorFilter(skia.ColorFilters.Matrix([2.2, 0, 0, 0, -1.25, 0, 2.2, 0, 0, -1.25, 0, 0, 2.2, 0, -1.25, 0, 0, 0, 1, 0]))))
    c.drawImage(img, 0, 0, skia.SamplingOptions(), p)


OFFW = (236, 236, 232)   # references never use pure white text: soft off-white


def draw_tight(c, s, x, y, f, paint, track=-0.035):
    """Helvetica-style tight tracking (letters almost touching) — skia has no letter-spacing, so place glyphs"""
    g = f.textToGlyphs(s); ws = f.getWidths(g); tr = track * f.getSize(); pos = []; xx = 0.0
    for w in ws: pos.append(skia.Point(xx, 0)); xx += w + tr
    blob = skia.TextBlob.MakeFromPosText(s, pos, f) if hasattr(skia.TextBlob, 'MakeFromPosText') else None
    if blob is None:
        xx = 0.0
        for ch, w in zip(s, ws): c.drawString(ch, x + xx, y, f, paint); xx += w + tr
    else: c.drawTextBlob(blob, x, y, paint)
    return xx - tr


def tight_w(s, f, track=-0.035): return sum(f.getWidths(f.textToGlyphs(s))) + track * f.getSize() * (len(s) - 1)


def glow_paint(col=OFFW, a=1.0):
    p = P(col, a); p.setImageFilter(skia.ImageFilters.DropShadow(0, 0, 9, 9, skia.Color4f(0, 0, 0, 0.55 * a))); return p


def cap2(size): return dfont('Archivo-SemiBold', size)


def kword2(c, T, t, t0, t1, x, y, size=58, col=OFFW, maxw=760, lh=1.02, spread=False):
    """reference captions: small off-white tight grotesk, 1-3 words, centred in frame; spread=True places each word
    at evenly spaced columns across the frame (hook frame 'This   is   the   most')"""
    ws = [(w, a) for (w, a, b) in T.AL if t0 - 0.01 <= a < t1]
    shown = [(w, a) for (w, a) in ws if a - 0.03 <= t]
    if not shown or t > t1 + 0.2: return
    f = cap2(size)
    if spread:
        n = len(ws); x0 = 140; step = (W - 280) / max(1, n - 1) if n > 1 else 0
        for i, (w, a) in enumerate(ws):
            if a - 0.03 > t: continue
            k = cl((t - a + 0.03) / 0.1); ww = tight_w(w, f); cx = x0 + i * step if n > 1 else W / 2
            draw_tight(c, w, cx - ww / 2, y, f, glow_paint(col, k)); 
        return
    lines = [[]]; cw = 0; sp = f.measureText(' ') * 0.8
    for w, a in shown:
        ww = tight_w(w, f)
        if lines[-1] and cw + sp + ww > maxw: lines.append([]); cw = 0
        lines[-1].append((w, a)); cw += (sp if cw else 0) + ww
    for li, L in enumerate(lines):
        tw = sum(tight_w(w, f) for w, a in L) + sp * (len(L) - 1); xx = x - tw / 2; yy = y + li * size * lh
        for w, a in L:
            k = cl((t - a + 0.03) / 0.1)
            draw_tight(c, w, xx, yy, f, glow_paint(col, k)); xx += tight_w(w, f) + sp


def ghost_word(c, txt, x, y, size, k=1.0, col=OFFW, a=0.9, track=-0.05, font_name='Archivo-Bold'):
    """big grey word laid over the picture (reference: 'YEARS', 'SUBPRIME')"""
    if k <= 0: return
    f = dfont(font_name, size); w = tight_w(txt, f, track)
    c.save(); c.translate(x, y); s = 1.06 - 0.06 * eo(k); c.scale(s, s)
    draw_tight(c, txt, -w / 2, size * 0.36, f, glow_paint(col, a * eo(k)), track); c.restore()


def grid_lines(c, a=0.35, cols=3, rows=4):
    for i in range(1, cols): c.drawLine(W * i / cols, 0, W * i / cols, H, S((10, 10, 10), 2, a))
    for j in range(1, rows): c.drawLine(0, H * j / rows, W, H * j / rows, S((10, 10, 10), 2, a))


# ---------------------------------------------------------------- 3D card (perspective) with motion-blur trail
def _proj(pts3, f=1600.0, cx=W / 2, cy=H / 2):
    return [skia.Point(cx + x * f / (f + z), cy + y * f / (f + z)) for (x, y, z) in pts3]


def card3d(c, img, cx, cy, w, h, ry=0.0, rx=0.0, rz=0.0, z=0.0, border=10, a=1.0, trail=0, trail_d=(0, 0, 0)):
    """draw img on a 3D-rotated plane (degrees). trail=N draws N fading copies offset by trail_d (ry, rz, z) = motion blur"""
    for k in range(trail, -1, -1):
        ryk, rzk, zk = ry + trail_d[0] * k, rz + trail_d[1] * k, z + trail_d[2] * k
        aa = a * (1.0 if k == 0 else 0.22 * (1 - k / (trail + 1)))
        ay, ax, az = math.radians(ryk), math.radians(rx), math.radians(rzk)
        pts = []
        for (px, py) in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
            x1 = px * math.cos(az) - py * math.sin(az); y1 = px * math.sin(az) + py * math.cos(az)
            x2 = x1 * math.cos(ay); z2 = -x1 * math.sin(ay)
            y3 = y1 * math.cos(ax) - z2 * math.sin(ax); z3 = y1 * math.sin(ax) + z2 * math.cos(ax)
            pts.append((x2, y3, z3 + zk))
        dst = _proj(pts, cx=cx, cy=cy)
        src = [skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)]
        M = skia.Matrix(); 
        if not M.setPolyToPoly(src, dst): continue
        c.save(); c.concat(M)
        if border: c.drawRect(skia.Rect.MakeXYWH(-border, -border, w + 2 * border, h + 2 * border), P((240, 238, 232), aa))
        cover(c, img, 1.0, rect=skia.Rect.MakeWH(w, h), a=aa)
        c.restore()


def split3(c, imgs, t, t0, k=1.0):
    """three diagonal panes (reference: three-person triangle split)"""
    pts = [[(0, 0), (W * 0.58, 0), (W * 0.5, H * 0.52), (0, H * 0.78)],
           [(W * 0.58, 0), (W, 0), (W, H * 0.85), (W * 0.5, H * 0.52)],
           [(0, H * 0.78), (W * 0.5, H * 0.52), (W, H * 0.85), (W, H), (0, H)]]
    for i, (img, poly) in enumerate(zip(imgs, pts)):
        kk = eo(cl(k * 3 - i * 0.6))
        if kk <= 0: continue
        p = skia.Path(); p.moveTo(*poly[0]); [p.lineTo(*q) for q in poly[1:]]; p.close()
        c.save(); c.clipPath(p, doAntiAlias=True)
        b = p.getBounds(); dx = (1 - kk) * (-300 if i == 0 else 300)
        cover(c, img, 1.08 + 0.06 * cl((t - t0) / 3), rect=b.makeOffset(dx, 0))
        c.restore(); c.drawPath(p, S((10, 10, 10), 10))


def photo_wall(c, imgs, t, t0, push=1.0, cols=4, rows=6, tile=(420, 300), gap=26, focus=None):
    """grid of photo tiles on a tilted wall, camera pushing in (reference: collage wall behind subject)"""
    tw, th = tile; Wd = cols * (tw + gap); Hd = rows * (th + gap)
    zc = 1400 - 900 * eo(cl(push))
    c.drawRect(skia.Rect.MakeWH(W, H), P((226, 224, 220)))
    for j in range(rows):
        for i in range(cols):
            x = -Wd / 2 + i * (tw + gap) + tw / 2; y = -Hd / 2 + j * (th + gap) + th / 2
            img = imgs[(i * 3 + j * 5) % len(imgs)]
            pts = [(x - tw / 2, y - th / 2, zc), (x + tw / 2, y - th / 2, zc + 40), (x + tw / 2, y + th / 2, zc + 40), (x - tw / 2, y + th / 2, zc)]
            dst = _proj(pts); src = [skia.Point(0, 0), skia.Point(tw, 0), skia.Point(tw, th), skia.Point(0, th)]
            M = skia.Matrix(); M.setPolyToPoly(src, dst); c.save(); c.concat(M)
            cover(c, img, 1.0, 0.3 * math.sin(i + j), 0.0, rect=skia.Rect.MakeWH(tw, th)); c.restore()


def felt(c, col=(28, 92, 52)):
    c.drawRect(skia.Rect.MakeWH(W, H), P(col))
    rng = np.random.default_rng(3)
    for _ in range(500):
        x, y = rng.uniform(0, W), rng.uniform(0, H); c.drawCircle(x, y, rng.uniform(1, 3), P((0, 0, 0) if rng.random() < .5 else (90, 160, 110), 0.12))


def pin(c, x, y, col=(80, 50, 160)):
    c.drawCircle(x + 3, y + 5, 15, P((0, 0, 0), 0.35)); c.drawCircle(x, y, 15, P(col)); c.drawCircle(x - 5, y - 5, 5, P((255, 255, 255), 0.6))


def string(c, pts, col=(70, 60, 170)):
    p = skia.Path(); p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; c.drawPath(p, S(col, 4, 0.85))


def sticky(c, x, y, txt, col=(236, 150, 160), rot=6, size=40):
    c.save(); c.translate(x, y); c.rotate(rot)
    sh = P((0, 0, 0), 0.35); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10)); c.drawRect(skia.Rect.MakeXYWH(-120, -110, 250, 240), sh)
    c.drawRect(skia.Rect.MakeXYWH(-125, -120, 250, 240), P(col))
    f = skia.Font(skia.Typeface.MakeFromFile(KALAM), size) if os.path.exists(KALAM) else capf(size)
    for i, ln in enumerate(txt.split('\n')): c.drawString(ln, -f.measureText(ln) / 2, -10 + i * size * 1.1, f, P((40, 30, 30)))
    c.restore()


def ribbons(c, txt, t, col=(214, 32, 40)):
    """two wavy red bands with repeating condensed text scrolling (reference: 'HIS NAME'S' banners)"""
    f = cond(190); unit = txt + '  '; uw = f.measureText(unit)
    for k, (y0, dirn, amp) in enumerate(((500, 1, 60), (1440, -1, 50))):
        off = (t * 240 * dirn) % uw
        pth = skia.Path(); top = []; bot = []
        for i in range(0, W + 41, 40):
            yy = y0 + amp * math.sin(i / W * math.pi * 1.4 + k * 2 + t * 0.6); top.append((i, yy - 120)); bot.append((i, yy + 120))
        pth.moveTo(*top[0]); [pth.lineTo(*q) for q in top[1:]]; [pth.lineTo(*q) for q in reversed(bot)]; pth.close()
        c.drawPath(pth, P(col))
        c.save(); c.clipPath(pth, doAntiAlias=True)
        for i in range(-2, 5):
            x = i * uw - off
            yy = y0 + amp * math.sin((x + uw / 2) / W * math.pi * 1.4 + k * 2 + t * 0.6)
            c.drawString(unit, x, yy + 68, f, P((240, 236, 230)))
        c.restore()


def rolodex(c, cx, cy, txt, k, t, w=760, h=520):
    """old desk calendar / rolodex card with tabs and two rings (reference: '2007')"""
    c.drawRect(skia.Rect.MakeWH(W, H), P((18, 18, 18)))
    f = cond(300); flip = 1 - eo(cl(k))
    c.save(); c.translate(cx, cy)
    for tx, lab in ((-200, '19'), (60, 'KY')):
        c.drawRRect(rr(tx, -h / 2 - 60, 200, 80, 8), P((60, 60, 60))); g = mono(32); c.drawString(lab, tx + 100 - g.measureText(lab) / 2, -h / 2 - 8, g, P((160, 160, 160)))
    c.scale(1, max(0.02, 1 - flip)); 
    c.drawRRect(rr(-w / 2, -h / 2, w, h, 26), P((228, 226, 220)))
    shd = skia.GradientShader.MakeRadial((0, 0), w * 0.7, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0.35)], [0.5, 1]); c.drawRRect(rr(-w / 2, -h / 2, w, h, 26), skia.Paint(Shader=shd))
    c.drawString(txt, -f.measureText(txt) / 2, 100, f, P((24, 24, 24)))
    for rx_ in (-120, 120): c.drawRect(skia.Rect.MakeXYWH(rx_ - 22, h / 2 - 100, 44, 160), P((30, 30, 30)))
    c.restore()


def word3d(c, txt, t, t0, col=(226, 30, 38), bg=(214, 212, 208)):
    """big red word swinging in 3D on a pale wall with motion blur (reference: red 'AND')"""
    c.drawRect(skia.Rect.MakeWH(W, H), P(bg))
    vg = skia.GradientShader.MakeRadial((W / 2, H / 2), H * 0.6, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, 0.35)], [0.3, 1]); c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=vg))
    f = cond(330); w = f.measureText(txt); hh = 330
    u = cl((t - t0) / 0.55); ang = -70 * (1 - eo(u)) + 6 * math.sin((t - t0) * 2)
    surf_w, surf_h = int(w + 40), int(hh * 1.2)
    s = skia.Surface(surf_w, surf_h); cc = s.getCanvas(); cc.drawString(txt, 20, hh * 0.95, f, P(col)); img = s.makeImageSnapshot()
    for k in (3, 2, 1, 0):
        aa = 1.0 if k == 0 else 0.18
        card3d(c, img, W / 2, H / 2, surf_w, surf_h, ry=ang + k * 9 * (1 - u), rz=-6, border=0, a=aa)
KALAM = '/home/claude/studio/fonts/ttf/PermanentMarker.ttf'
ELITE = '/home/claude/studio/fonts/ttf/SpecialElite.ttf'


# ================================================================== brand (OOPS. MY BUSINESS) — black+cream logo stays, reel accent = series colour
_LOGO = '/home/claude/studio/logo/'
_BR = {}


def _logo(name):
    if name not in _BR: _BR[name] = sk(Image.open(_LOGO + name))
    return _BR[name]


def brand_badge(c, x=880, y=330, r=56, a=1.0):
    """'O.' avatar, top-right inside the safe zone (left of the like/share column)"""
    img = _logo('logo_final_avatar_dark.png'); p = skia.Paint(AntiAlias=True, Alphaf=a)
    p.setImageFilter(skia.ImageFilters.DropShadow(0, 4, 8, 8, skia.Color4f(0, 0, 0, 0.45 * a)))
    c.save(); pth = skia.Path(); pth.addCircle(x, y, r); c.clipPath(pth, doAntiAlias=True)
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - r * 1.0, y - r * 1.0, 2 * r, 2 * r), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True, Alphaf=a)); c.restore()
    c.drawCircle(x, y, r, S((236, 230, 218), 3, 0.8 * a))


def series_tag(c, series, num, acc, t, dur, x=80, y=330, dark=True):
    """accent block with the series name + issue number, thin progress rule (brand sheet: 'ANY TOPIC / IN COLOUR')"""
    f = cond(40); w = f.measureText(series)
    c.drawRect(skia.Rect.MakeXYWH(x - 10, y - 38, w + 20, 50), P(acc))
    c.drawString(series, x, y, f, P((240, 236, 228)))
    g = capf(28); c.drawString(num, x + w + 26, y - 4, g, P(OFFW if dark else (20, 20, 20), 0.9))
    c.drawRect(skia.Rect.MakeXYWH(x - 10, y + 22, 640 * cl(t / dur), 4), P(acc, 0.9))


def wordmark(c, cx, cy, w=620, dark_bg=False, a=1.0):
    img = _logo('logo_final_wordmark_dark.png' if dark_bg else 'logo_final_wordmark_light.png'); h = w * img.height() / img.width()
    c.drawImageRect(img, skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True, Alphaf=a))
