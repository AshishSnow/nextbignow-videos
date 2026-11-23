"""INFOGRAPHIC look (owner reference 23 Nov 2026): flat vector illustration with bold dark outlines, limited palette
(navy / blue / red / yellow / sky on warm off-white), rounded panels, a stylised city skyline behind the hero object,
bold Inter Display headings, small callout cards with icons, check / cross marks, quick-glance tables. No mascot."""
import os, re, json, math, random
import numpy as np
import skia

W, H, FPS = 1080, 1920, 30
BG = (247, 245, 239); INK = (26, 28, 36); NAVY = (30, 58, 118); BLUE = (58, 108, 186); RED = (214, 50, 52)
YEL = (245, 192, 44); SKY = (204, 226, 243); SKY2 = (176, 206, 232); GREY = (120, 124, 132); WHITE = (255, 255, 255); GREEN = (52, 160, 90)
FD = '/usr/share/fonts/opentype/inter/'
_TF = {}
THEME = os.environ.get('OMB_THEME', 'paper')   # 'paper' = owner's pick 23 Nov 2026: sketch-reel font + colours + cream paper
if THEME == 'paper':
    BG = (244, 238, 224); INK = (40, 36, 34); NAVY = (52, 48, 46); BLUE = (128, 118, 106); RED = (150, 22, 34)
    YEL = (212, 160, 46); SKY = (234, 226, 208); SKY2 = (218, 206, 182); GREY = (110, 102, 94); WHITE = (252, 249, 241); GREEN = (96, 116, 64)
CARD_SKY, SKY3 = ((238, 230, 212), (244, 238, 224)) if THEME == 'paper' else ((232, 242, 250), (220, 234, 246))
_SW = {'Black': 700, 'ExtraBold': 700, 'Bold': 700, 'SemiBold': 600, 'Medium': 500, 'Regular': 400}


def font(size, w='Bold', disp=True, italic=False):
    if THEME == 'paper':
        k = ('serif', w, italic)
        if k not in _TF:
            base = skia.Typeface.MakeFromFile('/home/claude/studio/fonts_serif/' + ('LibreCaslonText-Italic-VF.ttf' if italic else 'LibreCaslonText-VF.ttf'))
            co = skia.FontArguments.VariationPosition.Coordinate(0x77676874, float(_SW.get(w, 600)))
            fa = skia.FontArguments(); fa.setVariationDesignPosition(skia.FontArguments.VariationPosition(skia.FontArguments.VariationPosition.Coordinates([co])))
            _TF[k] = base.makeClone(fa)
        f = skia.Font(_TF[k], size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True); return f
    k = (w, disp)
    if k not in _TF: _TF[k] = skia.Typeface.MakeFromFile(FD + ('InterDisplay-' if disp else 'Inter-') + w + '.otf')
    f = skia.Font(_TF[k], size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True); return f


_PAPER = [None]


def paper(c):
    """cream paper: fibre noise + soft blotches + vignette, built once."""
    if _PAPER[0] is None:
        rnd = np.random.default_rng(7)
        n = rnd.normal(0, 1, (H // 4, W // 4)); from scipy.ndimage import gaussian_filter, zoom
        low = zoom(gaussian_filter(n, 6), 4, order=1)[:H, :W]; fine = rnd.normal(0, 1, (H, W))
        yy, xx = np.mgrid[0:H, 0:W]; vig = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2
        base = np.array(BG, np.float32)[None, None, :]
        img = base + (low[..., None] * 14) + (fine[..., None] * 4) - (vig[..., None] * 26)
        img = np.clip(img, 0, 255).astype(np.uint8)
        _PAPER[0] = skia.Image.fromarray(np.ascontiguousarray(np.dstack([img, np.full((H, W), 255, np.uint8)])), colorType=skia.kRGBA_8888_ColorType)
    c.drawImage(_PAPER[0], 0, 0)


def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)


def P(rgb, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor4f(C(rgb, a)); return p


def S(rgb, w, a=1.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w); p.setColor4f(C(rgb, a))
    p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join); return p


def cl(x): return max(0.0, min(1.0, x))
def pr(t, t0, d): return cl((t - t0) / d)
def eo(x): return 1 - (1 - x) ** 3
def eio(x): return 3 * x * x - 2 * x * x * x
def eback(x, s=1.9): x -= 1; return x * x * ((s + 1) * x + s) + 1


def path(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p


def shape(c, sh, fill, ow=5, oc=INK):
    if isinstance(sh, skia.Rect): c.drawRect(sh, P(fill)); c.drawRect(sh, S(oc, ow))
    elif isinstance(sh, skia.RRect): c.drawRRect(sh, P(fill)); c.drawRRect(sh, S(oc, ow))
    else: c.drawPath(sh, P(fill)); c.drawPath(sh, S(oc, ow))


def rr(x, y, w, h, r): return skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)


def pop(c, k, x, y, fn):
    if k <= 0: return
    s = eback(cl(k)); c.save(); c.translate(x, y); c.scale(s, s); c.translate(-x, -y); fn(); c.restore()


def text(c, s, x, y, size, rgb=INK, w='Bold', align='c', a=1.0, maxw=940, disp=True):
    f = font(size, w, disp); tw = f.measureText(s)
    while tw > maxw and f.getSize() > 14: f = font(f.getSize() * 0.95, w, disp); tw = f.measureText(s)
    xx = x - tw / 2 if align == 'c' else (x if align == 'l' else x - tw)
    c.drawString(s, xx, y, f, P(rgb, a)); return tw


def title(c, t, lines, t0=0.0, size=74, y0=330):
    """two-line heading at the top, line by line fade-up. paper theme: line 2 = italic deep red (the sketch-reel headline)."""
    for i, s in enumerate(lines):
        k = eo(pr(t, t0 + i * 0.12, 0.35))
        if k <= 0: continue
        it = THEME == 'paper' and i == len(lines) - 1 and len(lines) > 1
        c.save(); c.translate(0, 24 * (1 - k))
        if it:
            f = font(size * 1.08, 'Medium', italic=True); tw = f.measureText(s)
            while tw > 940: f = font(f.getSize() * 0.95, 'Medium', italic=True); tw = f.measureText(s)
            c.drawString(s, 540 - tw / 2, y0 + i * (size * 1.1), f, P(RED, k))
        else: text(c, s, 540, y0 + i * (size * 1.1), size, INK, 'Bold', a=k)
        c.restore()


def rule(c, x0, x1, y): c.drawLine(x0, y, x1, y, S(INK, 3))


def chip(c, s, x, y, fill=YEL, size=34, tc=INK, ow=4):
    f = font(size, 'Bold'); tw = f.measureText(s)
    shape(c, rr(x - tw / 2 - 22, y - size * 0.95, tw + 44, size * 1.45, size * 0.72), fill, ow)
    c.drawString(s, x - tw / 2, y + size * 0.05, f, P(tc))


def check(c, x, y, r=26, ok=True, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); s = eback(cl(k)); c.scale(s, s)
    c.drawCircle(0, 0, r, P(GREEN if ok else RED)); c.drawCircle(0, 0, r, S(INK, 3))
    if ok: c.drawPath(path([(-r * 0.45, 0), (-r * 0.1, r * 0.35), (r * 0.5, -r * 0.35)], False), S(WHITE, r * 0.22))
    else:
        for sx in (-1, 1): c.drawLine(-r * 0.38, -r * 0.38 * sx, r * 0.38, r * 0.38 * sx, S(WHITE, r * 0.22))
    c.restore()


def skyline(c, x, y, w, h, seed=3, col=SKY2, k=1.0):
    """flat stylised city: towers in sky blues with thin dark outlines and window strips."""
    rnd = random.Random(seed); xx = x; c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y - h, w, h))
    while xx < x + w:
        bw = rnd.randint(70, 140); bh = rnd.randint(int(h * 0.35), int(h * 0.95)) * k
        cc = [col, SKY, SKY3, BLUE][rnd.randint(0, 3) if rnd.random() < 0.85 else 3]
        r = skia.Rect.MakeXYWH(xx, y - bh, bw, bh); c.drawRect(r, P(cc)); c.drawRect(r, S(INK, 2.5))
        if cc != BLUE:
            for wy in np.arange(y - bh + 22, y - 10, 30): c.drawLine(xx + 14, wy, xx + bw - 14, wy, S(INK, 1.6, 0.35))
        else:
            for wx in np.arange(xx + 16, xx + bw - 10, 22): c.drawLine(wx, y - bh + 20, wx, y - 12, S(WHITE, 2, 0.6))
        if rnd.random() < 0.25:   # spire
            c.drawLine(xx + bw / 2, y - bh, xx + bw / 2, y - bh - 60 * k, S(INK, 3))
        xx += bw + rnd.randint(-8, 6)
    c.restore()


def card(c, x, y, w, h, fill=WHITE, r=36, ow=4):
    c.drawRRect(rr(x + 8, y + 10, w, h, r), P(INK, 0.12)); shape(c, rr(x, y, w, h, r), fill, ow)


def sky_card(c, x, y, w, h, seed=3, sky_k=1.0):
    """the centre stage: rounded panel with sky fill + skyline at its bottom third."""
    card(c, x, y, w, h, CARD_SKY)
    c.save(); c.clipRRect(rr(x, y, w, h, 36))
    c.drawCircle(x + w * 0.78, y + h * 0.22, 70, P(WHITE, 0.9))
    skyline(c, x, y + h, w, h * 0.62, seed, k=sky_k)
    c.drawRect(skia.Rect.MakeXYWH(x, y + h - 90, w, 90), P((236, 232, 222))); c.drawLine(x, y + h - 90, x + w, y + h - 90, S(INK, 3))
    c.restore(); c.drawRRect(rr(x, y, w, h, 36), S(INK, 4))


# ------------------------------------------------------------------ hero objects
def sneaker(c, x, y, s=1.0, col=RED, acc=BLUE, rot=0.0, flip=False, shadow=True):
    """generic flat-vector sneaker (no logo, no brand stripes): coloured upper, toe cap, laces, white midsole, navy outsole."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(-s if flip else s, s)
    if shadow: c.drawOval(skia.Rect.MakeXYWH(-230, 70, 460, 34), P(INK, 0.12))
    out = skia.Path(); out.moveTo(-235, 40); out.lineTo(215, 40); out.cubicTo(250, 40, 262, 66, 236, 82); out.lineTo(-220, 82); out.cubicTo(-250, 82, -258, 40, -235, 40); out.close()
    shape(c, out, NAVY, 5)
    mid = skia.Path(); mid.moveTo(-232, 6); mid.lineTo(200, 10); mid.cubicTo(240, 12, 252, 30, 240, 44); mid.lineTo(-230, 44); mid.cubicTo(-250, 44, -250, 8, -232, 6); mid.close()
    shape(c, mid, WHITE, 5); c.drawLine(-225, 28, 236, 30, S(acc, 5))
    up = skia.Path(); up.moveTo(-232, 8); up.cubicTo(-246, -70, -220, -128, -160, -140); up.lineTo(-92, -146); up.cubicTo(-70, -96, -10, -72, 60, -56)
    up.cubicTo(150, -38, 222, -16, 232, 10); up.close(); shape(c, up, WHITE, 5)
    toe = skia.Path(); toe.moveTo(130, -40); toe.cubicTo(185, -28, 226, -10, 232, 10); toe.lineTo(120, 10); toe.close(); shape(c, toe, col, 4)
    heel = skia.Path(); heel.moveTo(-232, 8); heel.cubicTo(-246, -70, -220, -128, -160, -140); heel.lineTo(-150, 8); heel.close(); shape(c, heel, col, 4)
    swoop = skia.Path(); swoop.moveTo(-140, -10); swoop.cubicTo(-80, -40, 0, -30, 90, -6); swoop.lineTo(84, 6); swoop.cubicTo(0, -12, -80, -18, -134, 4); swoop.close()
    shape(c, swoop, acc, 3.5)   # one plain accent band (generic, not any brand's mark)
    c.drawPath(path([(-160, -140), (-92, -146), (-98, -128), (-158, -122)]), P(INK, 0.85))
    for i in range(5):
        lx = -78 + i * 34; ly = -112 + i * 13
        c.drawLine(lx - 14, ly - 8, lx + 14, ly + 8, S(INK, 4)); c.drawLine(lx - 14, ly + 8, lx + 14, ly - 8, S(INK, 4))
    c.drawLine(-218, -30, -160, -34, S(INK, 2, 0.4)); c.restore()


def factory(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, cx in enumerate((-190, -110)):
        shape(c, skia.Rect.MakeXYWH(cx, -380, 52, 200), RED, 4); c.drawRect(skia.Rect.MakeXYWH(cx, -350, 52, 16), P(WHITE))
        for j in range(3):
            u = (t * 0.5 + j / 3 + i * 0.17) % 1
            c.drawCircle(cx + 26 + 40 * u, -400 - 130 * u, 20 + 26 * u, P(WHITE, 0.95 * (1 - u))); c.drawCircle(cx + 26 + 40 * u, -400 - 130 * u, 20 + 26 * u, S(INK, 2.5, 0.6 * (1 - u)))
    roof = [(-250, -170)]
    for k in range(5): roof += [(-250 + k * 100 + 100, -250), (-250 + k * 100 + 100, -170)]
    shape(c, path(roof), NAVY, 4)
    shape(c, skia.Rect.MakeXYWH(-250, -170, 500, 170), WHITE, 5)
    for k in range(5): shape(c, rr(-230 + k * 96, -145, 70, 56, 8), YEL, 3)
    shape(c, rr(-48, -72, 96, 72, 6), BLUE, 4)
    c.restore()


def conveyor(c, x, y, w, t, speed=1.0, n=5, s=0.32):
    shape(c, rr(x, y, w, 46, 23), (210, 212, 218), 4)
    for i in range(int(w / 70)): c.drawCircle(x + 30 + i * 70, y + 23, 12, P(WHITE)); c.drawCircle(x + 30 + i * 70, y + 23, 12, S(INK, 2.5))
    cols = [(RED, BLUE), (BLUE, YEL), (YEL, NAVY), ((60, 160, 110), RED), (NAVY, RED)]
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y - 200, w, 220))
    for i in range(n):
        u = (t * speed * 0.18 + i / n) % 1
        sneaker(c, x - 80 + (w + 160) * u, y - 34, s, cols[i % 5][0], cols[i % 5][1], shadow=False)
    c.restore()


def pricetag(c, x, y, txt, rot=-10, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    shape(c, path([(-40, -70), (210, -70), (210, 70), (-40, 70), (-100, 0)]), YEL, 5)
    c.drawCircle(-48, 0, 14, P(BG)); c.drawCircle(-48, 0, 14, S(INK, 4))
    f = font(92, 'Black'); c.drawString(txt, 85 - f.measureText(txt) / 2, 32, f, P(INK)); c.restore()


def stopwatch(c, x, y, r, t):
    shape(c, skia.Rect.MakeXYWH(x - 16, y - r - 34, 32, 28), NAVY, 3)
    c.drawCircle(x, y, r, P(WHITE)); c.drawCircle(x, y, r, S(INK, 5))
    for i in range(12): a = i * math.pi / 6; c.drawLine(x + r * 0.78 * math.sin(a), y - r * 0.78 * math.cos(a), x + r * 0.9 * math.sin(a), y - r * 0.9 * math.cos(a), S(INK, 3))
    a = t * 2 * math.pi; c.drawLine(x, y, x + r * 0.7 * math.sin(a), y - r * 0.7 * math.cos(a), S(RED, 6)); c.drawCircle(x, y, 7, P(INK))


def pin(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(0, 40); p.cubicTo(-40, -5, -34, -50, 0, -50); p.cubicTo(34, -50, 40, -5, 0, 40); p.close(); shape(c, p, RED, 4)
    c.drawCircle(0, -18, 12, P(WHITE)); c.drawCircle(0, -18, 12, S(INK, 3)); c.restore()


def arrow(c, x0, y0, x1, y1, k, col=INK, w=6, curve=0.0):
    if k <= 0: return
    mx, my = (x0 + x1) / 2 - (y1 - y0) * curve, (y0 + y1) / 2 + (x1 - x0) * curve
    p = skia.Path(); p.moveTo(x0, y0); p.quadTo(mx, my, x1, y1)
    meas = skia.PathMeasure(p, False); L = meas.getLength(); seg = skia.Path(); meas.getSegment(0, L * k, seg, True)
    c.drawPath(seg, S(col, w))
    if k > 0.97:
        pos, tan = meas.getPosTan(L); a = math.atan2(tan.y(), tan.x())
        for da in (2.6, -2.6): c.drawLine(pos.x(), pos.y(), pos.x() + 30 * math.cos(a + da), pos.y() + 30 * math.sin(a + da), S(col, w))


def vs_badge(c, x, y, r=70):
    shape(c, path([(x + r * math.cos(i * math.pi / 8) * (1 if i % 2 else 0.78), y + r * math.sin(i * math.pi / 8) * (1 if i % 2 else 0.78)) for i in range(16)]), YEL, 4)
    text(c, 'VS', x, y + 22, 64, INK, 'Black')


# ------------------------------------------------------------------ timing + subtitles
class Timing:
    def __init__(self, proj):
        D = os.path.join(proj, 'comic', 'cd')
        self.AL = [x for x in json.load(open(os.path.join(D, 'align.json'))) if x[0] not in ('<s>', '</s>', '<sil>')]
        self.TOK = [(w.lower().strip("'"), a, b) for w, a, b in self.AL]
        words = open(os.path.join(D, 'script.txt')).read().split(); k = 0; subw = []
        for wd in words:
            n = len(re.findall(r"[A-Za-z0-9'%]+", wd))
            if n == 0: continue
            seg = self.AL[k:k + n]; k += n
            if seg: subw.append((wd, seg[0][1], seg[-1][2]))
        self.CH = []; cur = []
        for w in subw:
            cur.append(w)
            if len(cur) >= 3 or w[0][-1] in '.,?!': self.CH.append(cur); cur = []
        if cur: self.CH.append(cur)
        self.END = self.TOK[-1][2] + 0.25; self.DUR = self.END + 0.05

    def ph(self, text_, after=0.0, end=False):
        q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
        for i in range(len(self.TOK) - len(q) + 1):
            if self.TOK[i][1] + 1e-6 < after: continue
            if all(self.TOK[i + j][0] == q[j] for j in range(len(q))): return self.TOK[i + len(q) - 1][2] if end else self.TOK[i][1]
        raise KeyError(text_)


def subs(c, T, t, y=1440):
    for ch in T.CH:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.15:
            f = font(42, 'Medium', False, italic=(THEME == 'paper')); sp = f.measureText(' ')
            tw = sum(f.measureText(w) for w, a, b in ch) + sp * (len(ch) - 1); x = 540 - tw / 2
            c.drawRRect(rr(x - 26, y - 46, tw + 52, 66, 33), P(WHITE, 0.96)); c.drawRRect(rr(x - 26, y - 46, tw + 52, 66, 33), S(INK, 3))
            for w, a, b in ch:
                on = a - 0.03 <= t <= b + 0.08
                c.drawString(w, x, y, f, P(RED if on else INK)); x += f.measureText(w) + sp
            return
