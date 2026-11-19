import math, functools, os
import numpy as np, cairo, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
W, H = 1080, 1920; CX = W // 2
F = '/home/claude/fonts/'
LUCKY = F + 'LuckiestGuy-Regular.ttf'; ELITE = F + 'SpecialElite-Regular.ttf'; ANTON = F + 'Anton-Regular.ttf'; INTER = F + 'Inter.ttf'
CREAM = (252, 241, 210); INK = (28, 22, 20)
RED = 'E63946'; YEL = 'FFC93C'; BLUE = '2D6CDF'; CYAN = '3EC1D3'; GREEN = '3FAE5A'; PINK = 'FF7AA8'
def hx(h, a=1.0): return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)
def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x, s=1.7):
    x = clamp(x); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t

@functools.lru_cache(maxsize=24)
def paper(tint=None, mix=.72):
    a = np.zeros((H, W, 3), np.float32); a[:] = CREAM
    if tint: a[:] = a * (1 - mix) + np.array(rgb(tint), np.float32) * mix
    base = a[0, 0].copy(); im = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(im)
    dc = tuple(int(v * .86) for v in base)
    for y in range(0, H, 22):
        for x in range((y // 22 % 2) * 11, W, 22):
            r = 2.0 + 1.6 * math.sin(x * .004 + y * .003)
            d.ellipse((x - r, y - r, x + r, y + r), fill=dc)
    a = np.array(im).astype(np.int16) + np.random.default_rng(3).integers(-6, 7, (H, W, 1))
    return np.clip(a, 0, 255).astype(np.uint8)

def put_rgba(fr, rgba, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if scale <= 0.01 or alpha <= 0.01: return
    h, w = rgba.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale); M[0, 2] += cx - w / 2; M[1, 2] += cy - h / 2
    c = [(0, 0), (w, 0), (0, h), (w, h)]; pts = np.array([M @ np.array([x, y, 1]) for x, y in c])
    x0, y0 = max(0, int(pts[:, 0].min()) - 2), max(0, int(pts[:, 1].min()) - 2); x1, y1 = min(W, int(pts[:, 0].max()) + 2), min(H, int(pts[:, 1].max()) + 2)
    if x1 <= x0 or y1 <= y0: return
    M2 = M.copy(); M2[0, 2] -= x0; M2[1, 2] -= y0
    out = cv2.warpAffine(rgba, M2, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    a = out[..., 3:4].astype(np.float32) / 255 * alpha
    reg = fr[y0:y1, x0:x1].astype(np.float32); fr[y0:y1, x0:x1] = (reg * (1 - a) + out[..., :3] * a).astype(np.uint8)

@functools.lru_cache(maxsize=512)
def ttext(txt, size, font=LUCKY, fill='FFFFFF', stroke='1C1614', sw=None, shadow=True):
    sw = max(4, size // 9) if sw is None else sw
    f = ImageFont.truetype(font, size); bb = f.getbbox(txt, stroke_width=sw)
    w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow: d.text((20 - bb[0] + 9, 20 - bb[1] + 10), txt, font=f, fill=INK + (255,), stroke_width=sw, stroke_fill=INK + (255,))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill='#' + fill, stroke_width=sw, stroke_fill='#' + stroke)
    return np.array(im)

SAFE_W = 840
def title(fr, txt, cy, t, size=120, fill=YEL, rot=-2.0, font=LUCKY, cx=CX, maxw=SAFE_W):
    if t <= 0: return
    im = ttext(txt, size, font, fill); k = min(1.0, maxw / im.shape[1])
    put_rgba(fr, im, cx, cy, back(t / .3) * k, clamp(t / .1), rot)

@functools.lru_cache(maxsize=128)
def tape_img(txt, size, col, font, tcol='1C1614'):
    f = ImageFont.truetype(font, size); bb = f.getbbox(txt); w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 34
    im = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w + 14, h + 14), fill=INK + (150,))
    d.polygon([(4, 6), (w, 2), (w + 4, h), (8, h + 4)], fill=rgb(col) + (245,))
    d.text((30 - bb[0], 17 - bb[1]), txt, font=f, fill='#' + tcol)
    return np.array(im)

def tape(fr, txt, cx, cy, t, col=YEL, size=46, font=ELITE, rot=-3, tcol='1C1614'):
    if t <= 0: return
    im = tape_img(txt, size, col, font, tcol); k = min(1.0, SAFE_W / im.shape[1])
    put_rgba(fr, im, cx, cy, back(t / .3) * k, clamp(t / .1), rot)

@functools.lru_cache(maxsize=32)
def burst_img(txt, r, col, size, n=14):
    s = int(r * 2.6); im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c0 = s / 2; pts = []
    for i in range(n * 2):
        a = i * math.pi / n; rr = r if i % 2 == 0 else r * .68; pts.append((c0 + math.cos(a) * rr, c0 + math.sin(a) * rr))
    d.polygon([(x + 10, y + 12) for x, y in pts], fill=INK + (255,)); d.polygon(pts, fill='#' + col, outline=INK + (255,), width=8)
    ti = Image.fromarray(ttext(txt, size, LUCKY, 'FFFFFF', shadow=False)); im.alpha_composite(ti, (int(c0 - ti.width / 2), int(c0 - ti.height / 2)))
    return np.array(im)

def burst(fr, txt, cx, cy, t, r=150, col=RED, size=80, rot=8):
    if t <= 0: return
    put_rgba(fr, burst_img(txt, r, col, size), cx, cy, back(t / .28), 1.0, rot + 4 * math.sin(t * 6))

def comic_photo(path, w, h, focus=(.5, .5), sat=1.35, cont=1.15):
    im = Image.open(path).convert('RGB'); sc = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    l = int((im.width - w) * focus[0]); t = int((im.height - h) * focus[1]); im = im.crop((l, t, l + w, t + h))
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(cont); im = ImageOps.posterize(im, 5)
    a = np.array(im).astype(np.float32); g = cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    e = cv2.Canny(g, 80, 160); e = cv2.dilate(e, np.ones((2, 2), np.uint8)); a[e > 0] *= .35
    yy, xx = np.mgrid[0:h, 0:w]; cell = 9
    cxg = (xx // cell) * cell + cell / 2; cyg = (yy // cell) * cell + cell / 2
    lum = g.astype(np.float32) / 255; r = (1 - lum) * cell * .55
    dot = ((xx - cxg) ** 2 + (yy - cyg) ** 2) < r ** 2
    a[dot & (lum < .45)] *= .72
    return np.clip(a, 0, 255).astype(np.uint8)

def panel_img(img, border=10, shadow=(18, 20)):
    h, w = img.shape[:2]; can = Image.new('RGBA', (w + 2 * border + shadow[0], h + 2 * border + shadow[1]), (0, 0, 0, 0)); d = ImageDraw.Draw(can)
    d.rectangle((shadow[0], shadow[1], w + 2 * border + shadow[0] - 1, h + 2 * border + shadow[1] - 1), fill=INK + (255,))
    d.rectangle((0, 0, w + 2 * border - 1, h + 2 * border - 1), fill=INK + (255,)); can.paste(Image.fromarray(img).convert('RGBA'), (border, border))
    return np.array(can)

def load_st(n, h=None, w=None):
    im = Image.open('/home/claude/freeze/st/' + n + '.png').convert('RGBA')
    if h: im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    if w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return np.array(im)

def sticker(fr, rgba, cx, cy, T, k=0, sc=1.0, rot=0.0, t=1.0, bob=10):
    if t <= 0: return
    put_rgba(fr, rgba, cx, cy + bob * math.sin(T * 2.2 + k), sc * back(t / .3), 1.0, rot + 2 * math.sin(T * 1.6 + k))

def cairo_layer(draw):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND); draw(c)
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data()).copy(); a = buf[..., 3:4].astype(np.float32)
    out = np.empty_like(buf); out[..., :3] = np.clip(np.where(a > 0, buf[..., 2::-1] * 255.0 / np.maximum(a, 1), 0), 0, 255); out[..., 3] = buf[..., 3]
    return out

def overlay(fr, rgba):
    a = rgba[..., 3:4].astype(np.float32) / 255; fr[:] = (fr * (1 - a) + rgba[..., :3] * a).astype(np.uint8)

def ink(c, w=7, a=1.0): c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(w)

def rays(fr, T, col='FFFFFF', a=.16, cx=CX, cy=960, n=18):
    def dr(c):
        c.save(); c.translate(cx, cy); c.rotate(T * .12)
        for k in range(n):
            ang = k * 2 * math.pi / n; c.move_to(0, 0); c.arc(0, 0, 1700, ang, ang + math.pi / n); c.close_path(); c.set_source_rgba(*hx(col, a)); c.fill()
        c.restore()
    overlay(fr, cairo_layer(dr))

def shake(T, at, dur=.35, amp=18):
    k = (T - at) / dur
    return (amp * (1 - k) * math.sin(T * 90), amp * (1 - k) * math.cos(T * 77)) if 0 <= k < 1 else (0, 0)
