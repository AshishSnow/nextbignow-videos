"""Editorial 'field notes' toolkit: paper, grid, fog, ink strokes, handwriting, captions, footage helpers."""
import sys, os, math, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'qday'))
import numpy as np
import skia
import gfx
from gfx import *
from PIL import Image

gfx._TF.update({'mss': 'Montserrat-SemiBold.ttf', 'msm': 'Montserrat-Medium.ttf', 'mxb': 'Montserrat-ExtraBold.ttf',
                'mbk': 'Montserrat-Black.ttf', 'cav': 'Caveat-Bold.ttf', 'cas': 'Caveat-SemiBold.ttf',
                'bcb': 'BarlowCondensed-Bold.ttf', 'bcm': 'BarlowCondensed-Medium.ttf', 'mkr': 'PermanentMarker.ttf'})

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
PAPER = (214, 206, 193)
INK = (34, 31, 28)
ORANGE = (232, 86, 32)
ORANGE2 = (255, 130, 56)
GREY = (118, 110, 98)
CREAM = (247, 243, 235)
DARK = (13, 13, 14)
SAMP = skia.SamplingOptions(skia.CubicResampler.Mitchell())
LINS = skia.SamplingOptions(skia.FilterMode.kLinear)

def img_from(arr, unpremul=False):
    return skia.Image.fromarray(np.ascontiguousarray(arr), colorType=skia.kRGBA_8888_ColorType,
                                alphaType=skia.kUnpremul_AlphaType if unpremul else skia.kPremul_AlphaType)

# ------------------------------------------------------------------ paper
def _upnoise(rng, gh, gw, h, w):
    a = rng.normal(0, 1, (gh, gw)).astype(np.float32)
    im = Image.fromarray(((a - a.min()) / (a.max() - a.min()) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(im, np.float32) / 255 - 0.5

def make_paper():
    rng = np.random.default_rng(11)
    mott = _upnoise(rng, 24, 14, H, W) * 1.0 + _upnoise(rng, 96, 54, H, W) * 0.5
    fine = rng.normal(0, 1, (H, W)).astype(np.float32)
    # fibres: horizontal streaks
    fib = _upnoise(rng, 900, 12, H, W) * 0.6
    y = np.linspace(-1, 1, H)[:, None]; x = np.linspace(-1, 1, W)[None, :]
    vig = np.clip(np.sqrt((x / 1.15) ** 2 + (y / 1.25) ** 2) - 0.45, 0, 1) ** 1.6
    out = np.zeros((H, W, 4), np.float32)
    for k in range(3):
        out[..., k] = PAPER[k] + mott * 9 + fine * 2.2 + fib * 4 - vig * 40
    out[..., 3] = 255
    return img_from(np.clip(out, 0, 255).astype(np.uint8))

def make_halftone(w, h, sp=15, rmax=3.6, direction=(1, 1)):
    surf = skia.Surface(w, h); c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    p = paint(INK, 1.0)
    for j in range(0, h + sp, sp):
        for i in range(0, w + sp, sp):
            off = (sp / 2) if (j // sp) % 2 else 0
            u = ((i + off) / w) * direction[0] + (j / h) * direction[1]
            u = u / (abs(direction[0]) + abs(direction[1]))
            r = rmax * (1 - u) ** 1.3
            if r > 0.35:
                c.drawCircle(i + off, j, r, p)
    return surf.makeImageSnapshot()

def make_fog(seed, w=1100, h=420):
    rng = np.random.default_rng(seed)
    n = sum(_upnoise(rng, max(2, int(h / s)), max(2, int(w / s)), h, w) * a for s, a in [(210, 1.0), (90, 0.55), (40, 0.3), (18, 0.15)])
    n = (n - n.min()) / (n.max() - n.min())
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(-1, 1, w)[None, :]
    body = np.clip((y - 0.08) / 0.55, 0, 1) ** 0.9                 # denser at bottom
    side = np.clip(1 - np.abs(x) ** 2.2, 0, 1)
    a = np.clip((n - 0.38) / 0.35, 0, 1) * body * side
    a = np.clip(a * 1.25 + body ** 3 * side * 0.35, 0, 1) * np.clip((1 - y) / 0.22, 0, 1)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., 0] = 246; out[..., 1] = 241; out[..., 2] = 233
    out[..., 3] = (a * 255).astype(np.uint8)
    return img_from(out, True)

PAPER_IMG = make_paper()
HALF_TR = make_halftone(420, 520, direction=(-1, 1))
HALF_BL = make_halftone(380, 460, direction=(1, -1))
FOG = [make_fog(s) for s in (3, 7, 19)]

def draw_paper(c):
    c.drawImage(PAPER_IMG, 0, 0)

def draw_dark(c):
    c.drawRect(skia.Rect.MakeWH(W, H), paint(DARK))
    c.drawCircle(540, 900, 900, paint(shader=rad(540, 900, 900, [argb((40, 40, 42), 0.9), argb(DARK, 0)])))

def grid(c, t, a=1.0, dark=False, labels=('NEXTBIGNOW', 'FIELD NOTES 07', 'MAMMUTHUS', 'PRIMIGENIUS'), t0=0.0, halftone=True):
    """design-layout guides; draws on from t0"""
    if a <= 0.01: return
    col = (235, 230, 222) if dark else INK
    la = (0.16 if dark else 0.30) * a
    k = eo(pr(t, t0, 0.6))
    lines = [((72, 0), (72, H)), ((W - 72, 0), (W - 72, H)), ((0, 196), (W, 196)), ((0, 1720), (W, 1720)),
             ((0, 260), (W, 260)), ((300, 0), (300, 196))]
    for i, (p0, p1) in enumerate(lines):
        kk = cl(k * 1.3 - i * 0.06)
        if kk <= 0: continue
        c.drawLine(p0[0], p0[1], lerp(p0[0], p1[0], kk), lerp(p0[1], p1[1], kk), paint(col, la, stroke=1.3))
    if halftone and not dark:
        p = skia.Paint(); p.setAlphaf(0.16 * a * k)
        c.drawImage(HALF_TR, W - 420, 0, LINS, p)
        c.drawImage(HALF_BL, 0, H - 460, LINS, p)
    ta = (0.55 if dark else 0.62) * a * pr(t, t0 + 0.2, 0.4)
    if ta > 0:
        text(c, labels[0], 92, 236, 'bcm', 26, col, ta, align='l', sp=3)
        text(c, labels[1], W - 92, 236, 'bcm', 26, col, ta, align='r', sp=3)
        for (x, ang, s) in [(36, -90, labels[2]), (W - 36, 90, labels[3])]:
            c.save(); c.translate(x, 960); c.rotate(ang)
            text(c, s, 0, 9, 'bcm', 24, col, ta, sp=6)
            c.restore()
        text(c, '0.5X', 330, 176, 'bcm', 20, col, ta * 0.8, align='l', sp=2)
        # crop marks
        for (x, y, sx, sy) in [(72, 1720, 1, -1), (W - 72, 1720, -1, -1)]:
            c.drawLine(x - 14 * sx, y, x + 14 * sx, y, paint(col, ta, stroke=1.5))
            c.drawLine(x, y - 14 * sy, x, y + 14 * sy, paint(col, ta, stroke=1.5))

# ------------------------------------------------------------------ fog
def fog(c, cx, y, w, a, t, seed=0, layers=3, rgb=None):
    """soft cloud bank whose base sits at y (cloud body above y)."""
    if a <= 0.01: return
    for i in range(layers):
        img = FOG[(seed + i) % 3]
        sc = w / img.width() * (1.0 + 0.18 * i)
        drift = math.sin(t * 0.25 + i * 2.1 + seed) * 40 + (t * 12 * (1 if i % 2 else -1)) % 80 - 40
        ww, hh = img.width() * sc, img.height() * sc * (0.75 + 0.15 * i)
        dst = skia.Rect.MakeXYWH(cx - ww / 2 + drift, y - hh * (0.78 - 0.1 * i), ww, hh)
        p = skia.Paint(); p.setAlphaf(cl(a * (0.95 - 0.18 * i)))
        if rgb is not None:
            p.setColorFilter(skia.ColorFilters.Blend(argb(rgb), skia.BlendMode.kModulate))
        c.drawImageRect(img, dst, LINS, p)

# ------------------------------------------------------------------ ink
def wob(pts, seed=0, amp=1.6, step=7.0):
    if len(pts) < 2: return pts
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg); n = max(6, int(L / step))
    out = []
    for i in range(n + 1):
        q = partial(pts, i / n)[-1]
        d1 = amp * (math.sin(i * 0.37 + seed * 1.7) + 0.5 * math.sin(i * 1.13 + seed * 3.1))
        d2 = amp * (math.cos(i * 0.29 + seed * 2.3) + 0.5 * math.sin(i * 0.83 + seed))
        out.append((q[0] + d1, q[1] + d2))
    return out

def ink(c, pts, prog, rgb=INK, w=4.0, a=1.0, marker=False):
    if a <= 0.01 or prog <= 0: return
    pp = partial(pts, cl(prog))
    if len(pp) < 2: return
    path = poly(pp)
    if marker:
        c.drawPath(path, paint(rgb, a * 0.85, stroke=w))
        q = paint(mix(rgb, (255, 255, 255), 0.25), a * 0.35, stroke=w * 0.45)
        c.save(); c.translate(w * 0.18, -w * 0.12); c.drawPath(path, q); c.restore()
    else:
        c.drawPath(path, paint(rgb, a * 0.92, stroke=w))

def ell_pts(cx, cy, rx, ry, seed=0, turns=1.12, a0=-2.3):
    n = 90; out = []
    for i in range(n + 1):
        u = i / n
        ang = a0 + u * turns * 2 * math.pi
        rr = 1 + 0.035 * math.sin(3 * ang + seed) - 0.05 * u
        out.append((cx + math.cos(ang) * rx * rr, cy + math.sin(ang) * ry * rr))
    return out

def rect_pts(x0, y0, x1, y1, seed=0, over=10):
    j = lambda k: (hsh(seed, k) - 0.5) * 8
    return [(x0 - over, y0 + j(1)), (x1 + j(2), y0 + j(3)), (x1 + j(4), y1 + j(5)), (x0 + j(6), y1 + j(7)), (x0 + j(8), y0 - over)]

def arrow_ink(c, pts, prog, rgb=INK, w=4.0, a=1.0, head=26, marker=False, seed=0):
    p1 = min(1.0, prog / 0.8)
    wp = wob(pts, seed, 1.2)
    ink(c, wp, p1, rgb, w, a, marker)
    hk = pr(prog, 0.8, 0.2)
    if hk > 0:
        (x0, y0), (x1, y1) = wp[-4], wp[-1]
        ang = math.atan2(y1 - y0, x1 - x0)
        for s in (-1, 1):
            hp_ = [(x1, y1), (x1 - math.cos(ang + s * 0.5) * head, y1 - math.sin(ang + s * 0.5) * head)]
            ink(c, hp_, hk, rgb, w, a, marker)

def check_ink(c, x, y, s, prog, rgb=ORANGE, w=6, a=1.0):
    pts = wob([(x - s * 0.5, y), (x - s * 0.1, y + s * 0.4), (x + s * 0.6, y - s * 0.55)], 3, 0.8, 5)
    ink(c, pts, prog, rgb, w, a, True)

def scribble_out(c, x0, y0, x1, y1, prog, rgb=ORANGE, w=7, a=1.0, n=7):
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append((lerp(x0, x1, u), y0 if i % 2 == 0 else y1))
    ink(c, wob(pts, 5, 1.5, 6), prog, rgb, w, a, True)

def hand(c, s, x, y, size, rgb=INK, prog=1.0, a=1.0, align='l', key='cav', rot=0.0):
    """handwritten text revealed left->right"""
    if a <= 0.01 or prog <= 0: return 0
    w = tw(s, key, size)
    x0 = x if align == 'l' else (x - w / 2 if align == 'c' else x - w)
    c.save()
    if rot:
        c.translate(x0, y); c.rotate(rot); c.translate(-x0, -y)
    c.clipRect(skia.Rect.MakeLTRB(x0 - 10, y - size * 1.2, x0 + (w + 20) * cl(prog), y + size * 0.6))
    c.drawString(s, x0, y, font(key, size), paint(rgb, a))
    c.restore()
    return w

def stamp_box(c, cx, cy, s, size, rgb, a, angle=-8, scale=1.0, seed=2):
    if a <= 0.01: return
    w = tw(s, 'bcb', size, 3) + size * 1.2; h = size * 1.55
    c.save(); c.translate(cx, cy); c.rotate(angle); c.scale(scale, scale)
    c.saveLayer(None)
    rrect(c, -w / 2, -h / 2, w, h, 10, paint(rgb, a, stroke=5))
    rrect(c, -w / 2 + 9, -h / 2 + 9, w - 18, h - 18, 6, paint(rgb, a, stroke=2))
    text(c, s, 0, size * 0.36, 'bcb', size, rgb, a, sp=3)
    q = paint(WHITE, 1.0); q.setBlendMode(skia.BlendMode.kDstOut)
    for i in range(90):
        c.drawCircle((hsh(i, seed) - 0.5) * w, (hsh(i, seed + 1) - 0.5) * h, 1 + 3 * hsh(i, seed + 2), q)
    c.restore(); c.restore()

def tape(c, cx, cy, w, h, angle, a=1.0):
    c.save(); c.translate(cx, cy); c.rotate(angle)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), paint((236, 228, 205), 0.72 * a))
    for i in range(-int(w / 2), int(w / 2), 9):
        c.drawLine(i, -h / 2, i + 3, -h / 2 - 3, paint((236, 228, 205), 0.72 * a, stroke=2))
        c.drawLine(i, h / 2, i + 3, h / 2 + 3, paint((236, 228, 205), 0.72 * a, stroke=2))
    c.restore()

def shadow_rect(c, x, y, w, h, r=6, a=0.35, blur=18, dy=12):
    rrect(c, x, y + dy, w, h, r, paint((40, 30, 20), a, blur=blur))

# ------------------------------------------------------------------ captions
def _measure_words(words, key, size, sp):
    ws_ = [tw(wd, key, size) for wd in words]
    gap = size * 0.28
    return ws_, sum(ws_) + gap * (len(words) - 1), gap

def caption(c, t, cap, dark=False):
    t0, t1 = cap['t0'], cap['t1']
    if not (t0 - 0.05 <= t < t1): return
    out = 1 - pr(t, t1 - 0.22, 0.22)
    y = cap['y']
    col = (238, 236, 232) if dark else INK
    # line 1: word by word
    words, times = cap['l1'], cap['l1t']
    size = cap.get('s1', 54)
    key = 'mss'
    wsz, total, gap = _measure_words(words, key, size, 0)
    while total > 960:
        size -= 2; wsz, total, gap = _measure_words(words, key, size, 0)
    x = 540 - total / 2
    for wd, wt, ww in zip(words, times, wsz):
        k = pr(t, wt - 0.06, 0.22)
        if k > 0:
            e = eo(k)
            p = paint(col, e * out)
            if k < 1:
                p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5 * (1 - e) + 0.01))
            if dark:
                c.drawString(wd, x, y + 14 * (1 - e) + 3, font(key, size), paint((0, 0, 0), 0.5 * e * out, blur=6))
            c.drawString(wd, x, y + 14 * (1 - e), font(key, size), p)
        x += ww + gap
    # line 2: accent
    s2, t2, style = cap['l2'], cap['l2t'], cap.get('style', 'script')
    k = pr(t, t2 - 0.05, 0.28)
    if k > 0 and s2:
        e = eo(k)
        if style == 'script':
            key2, size2, dy = 'cav', cap.get('s2', 132), size * 1.95
        else:
            key2, size2, dy = 'mbk', cap.get('s2', 104), size * 1.85
        while tw(s2, key2, size2) > 1000:
            size2 -= 4
        w2 = tw(s2, key2, size2)
        sc = 0.9 + 0.1 * eback(k, 2.2)
        cy2 = y + dy
        c.save(); c.translate(540, cy2 - size2 * 0.35); c.scale(sc, sc); c.translate(-540, -(cy2 - size2 * 0.35))
        x2 = 540 - w2 / 2
        if style == 'script':
            # handwritten reveal + fade
            c.save(); c.clipRect(skia.Rect.MakeLTRB(x2 - 20, cy2 - size2, x2 + (w2 + 40) * cl(k * 1.4), cy2 + size2 * 0.5))
            if dark:
                c.drawString(s2, x2, cy2 + 4, font(key2, size2), paint((0, 0, 0), 0.45 * out, blur=8))
            c.drawString(s2, x2, cy2, font(key2, size2), paint(ORANGE, out))
            c.restore()
        else:
            p = paint(WHITE, e * out, shader=lin(0, cy2 - size2 * 0.75, 0, cy2, [argb(ORANGE2, e * out), argb(ORANGE, e * out)]))
            if k < 1:
                p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 7 * (1 - e) + 0.01))
            if dark:
                c.drawString(s2, x2, cy2 + 5, font(key2, size2), paint((0, 0, 0), 0.5 * e * out, blur=10))
            c.drawString(s2, x2, cy2, font(key2, size2), p)
        c.restore()

# ------------------------------------------------------------------ footage
VF_GRADE = 'eq=contrast=1.04:saturation=1.0'

class Decoder:
    def __init__(self, clip, src_t, size=(1188, 2112), blur=0):
        self.fw, self.fh = size
        self.start = max(0.0, src_t - 0.05)
        vf = 'scale=%d:%d:flags=lanczos,unsharp=5:5:0.35:5:5:0.0,%s' % (self.fw, self.fh, VF_GRADE)
        if blur: vf += ',gblur=sigma=%g' % blur
        vf += ',format=rgba'
        cmd = ['ffmpeg', '-v', 'error', '-ss', '%.3f' % self.start, '-i', os.path.join(HERE, 'src', clip + '.mp4'),
               '-vf', vf, '-r', '24', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-']
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=self.fw * self.fh * 8)
        self.frames = {}; self.n = -1; self.eof = False

    def _read(self):
        if self.eof: return False
        need = self.fw * self.fh * 4
        buf = self.p.stdout.read(need)
        if len(buf) < need:
            self.eof = True; return False
        self.n += 1
        self.frames[self.n] = np.frombuffer(buf, np.uint8).reshape(self.fh, self.fw, 4)
        for k in list(self.frames):
            if k < self.n - 2: del self.frames[k]
        return True

    def get(self, src_t, blend=True):
        rel = max(0.0, (src_t - self.start) * 24.0)
        i0 = int(math.floor(rel))
        while self.n < i0 + 1 and self._read():
            pass
        last = self.n
        a = self.frames.get(min(i0, last)); b = self.frames.get(min(i0 + 1, last))
        if a is None: a = self.frames[last]
        if b is None: b = a
        f = rel - i0
        if not blend: return a if f < 0.5 else b
        if f < 0.04: return a
        if f > 0.96: return b
        return ((a.astype(np.uint16) * int(256 * (1 - f)) + b.astype(np.uint16) * int(256 * f)) >> 8).astype(np.uint8)

    def close(self):
        try: self.p.stdout.close(); self.p.kill()
        except Exception: pass

DEC = {}
USED = set()

def frame(key, clip, src_t, blend=True, size=(1188, 2112), blur=0):
    USED.add(key)
    d = DEC.get(key)
    if d is None or src_t < d.start - 0.01:
        if d: d.close()
        d = DEC[key] = Decoder(clip, src_t, size, blur)
    return d.get(src_t, blend)

def gc_decoders():
    for k in list(DEC):
        if k not in USED:
            DEC[k].close(); del DEC[k]
    USED.clear()

def grade_filter(mode):
    if mode == 'warm':       # matte warm editorial
        s = 0.78; lr, lg, lb = 0.299, 0.587, 0.114
        m = [[s + (1 - s) * lr, (1 - s) * lg, (1 - s) * lb], [(1 - s) * lr, s + (1 - s) * lg, (1 - s) * lb], [(1 - s) * lr, (1 - s) * lg, s + (1 - s) * lb]]
        gain = [1.03, 1.0, 0.93]; off = [0.035, 0.03, 0.02]; con = 0.94
        rows = []
        for i in range(3):
            rows += [m[i][0] * gain[i] * con, m[i][1] * gain[i] * con, m[i][2] * gain[i] * con, 0, off[i]]
        rows += [0, 0, 0, 1, 0]
        return skia.ColorFilters.Matrix(rows)
    if mode == 'bw':
        k = 1.18; o = -0.07
        r = [0.299 * k, 0.587 * k, 0.114 * k, 0, o]
        return skia.ColorFilters.Matrix(r + r + r + [0, 0, 0, 1, 0])
    return None

def draw_cover(c, arr, dst, focus=(540, 960), zoom=1.0, mode='warm', a=1.0, unpremul=False):
    """cover-fit the frame (1080x1920 space) into dst around focus point."""
    fh, fw = arr.shape[:2]
    k = fw / 1080.0
    da = dst.width() / dst.height()
    sh = 1920 / zoom; sw = sh * da
    if sw > 1080 / zoom:
        sw = 1080 / zoom; sh = sw / da
    sx = cl(focus[0] - sw / 2, 0, 1080 - sw); sy = cl(focus[1] - sh / 2, 0, 1920 - sh)
    src = skia.Rect.MakeXYWH(sx * k, sy * k, sw * k, sh * k)
    p = skia.Paint(); p.setAlphaf(a)
    f = grade_filter(mode)
    if f: p.setColorFilter(f)
    c.drawImageRect(img_from(arr, unpremul), src, dst, SAMP, p, skia.Canvas.SrcRectConstraint.kFast_SrcRectConstraint)
    return (sx, sy, sw, sh)

def map_pt(view, dst, x, y):
    sx, sy, sw, sh = view
    return dst.left() + (x - sx) / sw * dst.width(), dst.top() + (y - sy) / sh * dst.height()

def feather_layer_end(c, dst, top=180, bottom=260, left=0, right=0):
    """call after drawing content inside c.saveLayer(); applies soft edges, then restores."""
    q = skia.Paint(); q.setBlendMode(skia.BlendMode.kDstIn)
    y0, y1 = dst.top(), dst.bottom()
    pos = [0, cl(top / dst.height()), cl(1 - bottom / dst.height()), 1]
    q.setShader(lin(0, y0, 0, y1, [argb(WHITE, 0), argb(WHITE, 1), argb(WHITE, 1), argb(WHITE, 0)], pos))
    c.drawRect(dst, q)
    if left or right:
        q2 = skia.Paint(); q2.setBlendMode(skia.BlendMode.kDstIn)
        x0, x1 = dst.left(), dst.right()
        q2.setShader(lin(x0, 0, x1, 0, [argb(WHITE, 0), argb(WHITE, 1), argb(WHITE, 1), argb(WHITE, 0)],
                         [0, cl(left / dst.width()), cl(1 - right / dst.width()), 1]))
        c.drawRect(dst, q2)
    c.restore()

def load_mask(clip, src_t):
    i = int(round(src_t * 24))
    d = os.path.join(HERE, 'masks', clip)
    for j in (i, i - 1, i + 1, i - 2):
        f = os.path.join(d, '%04d.png' % j)
        if os.path.exists(f):
            return np.asarray(Image.open(f))
    return None

def cutout_frame(clip, key, src_t):
    arr = frame(key, clip, src_t, True, size=(1080, 1920))
    m = load_mask(clip, src_t)
    out = arr.copy()
    if m is not None:
        out[..., 3] = m
    return out

def edge_sketch(arr, alpha=None, rgb=INK, gain=1.0, thr=8, half=True):
    s = arr[::2, ::2, :3].astype(np.float32) if half else arr[..., :3].astype(np.float32)
    lum = s[..., 0] * 0.299 + s[..., 1] * 0.587 + s[..., 2] * 0.114
    gx = np.zeros_like(lum); gy = np.zeros_like(lum)
    gx[:, 1:-1] = lum[:, 2:] - lum[:, :-2]; gy[1:-1, :] = lum[2:, :] - lum[:-2, :]
    e = np.clip((np.sqrt(gx * gx + gy * gy) - thr) / 40 * gain, 0, 1) ** 0.8
    if alpha is not None:
        al = alpha[::2, ::2] if half else alpha
        e = e * (al.astype(np.float32) / 255)
    out = np.empty(e.shape + (4,), np.uint8)
    out[..., 0] = rgb[0]; out[..., 1] = rgb[1]; out[..., 2] = rgb[2]
    out[..., 3] = (e * 235).astype(np.uint8)
    return img_from(out, True)

# ------------------------------------------------------------------ 3d card (subtle)
def card3d(c, cx, cy, w, h, yaw, pitch, fn, a=1.0, roll=0.0):
    d = 1600.0
    corners = []
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    for (x, y) in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        x, y = x * cr - y * sr, x * sr + y * cr
        X, Y, Z = x, y, 0.0
        cy_, sy_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        X, Z = X * cy_ + Z * sy_, -X * sy_ + Z * cy_
        cp, sp_ = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
        Y, Z = Y * cp - Z * sp_, Y * sp_ + Z * cp
        k = d / (d + Z)
        corners.append(skia.Point(cx + X * k, cy + Y * k))
    src = [skia.Point(0, 0), skia.Point(w, 0), skia.Point(w, h), skia.Point(0, h)]
    mtx = skia.Matrix()
    if not mtx.setPolyToPoly(src, corners):
        return
    c.save(); c.concat(mtx)
    fn(c, w, h, a)
    c.restore()

def paper_card(c, w, h, a, rgb=CREAM, r=8, shadow=True):
    if shadow:
        rrect(c, 4, 14, w, h, r, paint((50, 35, 20), 0.30 * a, blur=16))
    rrect(c, 0, 0, w, h, r, paint(rgb, a))
    rrect(c, 0, 0, w, h, r, paint((0, 0, 0), 0.06 * a, stroke=1.5))
