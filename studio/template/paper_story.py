"""PAPER look, data-driven (built from the cart reel, MIND TRICKS N° 07): one paper colour per series, real public-domain
photos as die-cut stickers, hand-drawn boiling hero words, italic serif captions, OMB brand (badge + series tag + wordmark).
A project module defines SERIES/NUM/palette + SCENES (list of dicts) and calls run(...).

Scene dict keys (every 'at' is a phrase from the script, a float offset from the scene start, or None = scene start):
  at       phrase where the scene starts (first scene: 0.0)
  bg       paper colour
  photos   [(asset, x, y, w, rot, at), ...]          die-cut photo stickers (slow push-in)
  props    [(drawfn, x, y, w, h, rot, at, bg), ...]  vector props on die-cut cards (drawfn(c) draws around 0,0)
  labels   [(text, x, y, size, rot, at, bg, fg), ...] condensed label stickers
  words    [(text, x, y, size, col, at), ...]        hand-drawn boiling hero words
  big      [(text, x, y, size, 'serif'|'cond', col, at), ...] plain big type
  cap      (y, size, col, until)                     serif caption of the words spoken from scene start until 'until'
  arrow    (x0, y0, x1, y1, at)                      hand-drawn arrow
  shake    phrase                                    small hit-shake on that word
"""
import os, math
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from paper_kit import *

YEL = (255, 214, 92); RED_ = (232, 70, 60); INK = (30, 16, 44); PAPER_C = (240, 232, 216)
SERIES_PAL = {   # paper, dark paper, tag accent, hero accent
    'MIND TRICKS': ((88, 40, 146), (40, 18, 70), (150, 84, 230), YEL),
    'CASE STUDY': ((168, 34, 42), (62, 12, 18), (236, 72, 64), YEL),
    'FOUNDER MINDSET': ((206, 98, 30), (78, 32, 8), (255, 140, 50), (255, 236, 190)),
    'BUSINESS IDEA': ((34, 110, 68), (12, 44, 26), (80, 196, 124), YEL),
    'MONEY EXPLAINED': ((30, 72, 156), (12, 26, 64), (84, 144, 244), YEL),
}


def load_img(path, mode='warm', crop=None):
    try:
        im = Image.open(path); im.load(); im = im.convert('RGB')
    except Exception: return None
    if crop: w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if mode == 'sepia':
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1); a = np.asarray(g, np.float32)[..., None] / 255
        im = Image.fromarray((np.concatenate([a * 245 + 8, a * 228 + 12, a * 200 + 18], -1)).clip(0, 255).astype(np.uint8))
        im = ImageEnhance.Contrast(im).enhance(1.12)
    else:
        im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.06)
    return sk(im)


def label(c, txt, x, y, k, rot=-3, size=64, bg=(250, 246, 236), fg=INK):
    f = cond(size); w = f.measureText(txt)
    sticker_draw(c, lambda cc: cc.drawString(txt, -w / 2, size * 0.36, f, P(fg)), x, y, w + 70, size * 1.5, k, rot, radius=14, bg=bg)


def hand_arrow(c, x0, y0, x1, y1, t, k=1.0, col=YEL, w=10):
    if k <= 0: return
    seed = int(t * 12); mx, my = (x0 + x1) / 2 + 80, (y0 + y1) / 2 - 120
    ex, ey = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    p = skia.Path(); p.moveTo(x0, y0); p.quadTo(x0 + (mx - x0) * k, y0 + (my - y0) * k, ex, ey)
    pen = S(col, w); pen.setStrokeCap(skia.Paint.kRound_Cap); pen.setPathEffect(skia.DiscretePathEffect.Make(12, 2.5, seed)); c.drawPath(p, pen)
    if k >= 1:
        a = math.atan2(y1 - my, x1 - mx)
        for da in (2.6, -2.6): c.drawLine(x1, y1, x1 + 60 * math.cos(a + da), y1 + 60 * math.sin(a + da), pen)


# ---- small vector props (drawn around 0,0 on a die-cut card)
def D_text(txt, size=200, col=INK, font='cond', sub=None, subcol=(120, 90, 150)):
    def d(c):
        f = cond(size) if font == 'cond' else serif(size); w = f.measureText(txt)
        c.drawString(txt, -w / 2, size * 0.34 - (24 if sub else 0), f, P(col))
        if sub:
            g = capf(30); c.drawString(sub, -g.measureText(sub) / 2, size * 0.34 + 34, g, P(subcol))
    return d


def D_pie(frac, col=RED_, rest=(220, 210, 196), r=150, txt=None):
    def d(c):
        c.drawCircle(0, 0, r, P(rest)); p = skia.Path(); p.moveTo(0, 0)
        p.arcTo(skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r), -90, 360 * frac, False); p.close(); c.drawPath(p, P(col))
        c.drawCircle(0, 0, r, S(INK, 5))
        if txt: f = cond(70); c.drawString(txt, -f.measureText(txt) / 2, r + 90, f, P(INK))
    return d


def D_bars(vals, cols, labels, h=300, bw=120, gap=60):
    def d(c):
        n = len(vals); x0 = -(n * bw + (n - 1) * gap) / 2; mx = max(vals)
        for i, (v, col, lb) in enumerate(zip(vals, cols, labels)):
            x = x0 + i * (bw + gap); hh = h * v / mx
            c.drawRect(skia.Rect.MakeXYWH(x, h / 2 - hh, bw, hh), P(col)); c.drawRect(skia.Rect.MakeXYWH(x, h / 2 - hh, bw, hh), S(INK, 4))
            g = capf(30); c.drawString(lb, x + bw / 2 - g.measureText(lb) / 2, h / 2 + 44, g, P(INK))
    return d


class Story:
    def __init__(self, HERE, series, num, scenes_fn, assets, light_last=True, cover_at=None):
        self.HERE = HERE; self.T = Timing(HERE); self.ph = self.T.ph; self.END, self.DUR = self.T.END, self.T.DUR
        self.SERIES, self.NUM = series, num
        self.PAPER, self.DARK, self.ACC, self.HERO = SERIES_PAL[series]
        A = os.path.join(HERE, 'assets')
        self.IM = {k: load_img(os.path.join(A, v[0]), v[1] if len(v) > 1 else 'warm', v[2] if len(v) > 2 else None) for k, v in assets.items()}
        self.SC = scenes_fn(self)
        self.starts = []; prev = 0.0
        for i, sc in enumerate(self.SC):
            t0 = self.res(sc.get('at', 0.0), prev, after=prev) - (0.1 if i else 0); self.starts.append(t0); prev = t0 + 0.1
        self.SCENES = [(t0, None) for t0 in self.starts]
        self.LIGHT = {len(self.SC) - 1} if light_last else set()
        self.WARM = grade_filter(desat=0.05, lift=0.02, gain=0.98, cool=-0.01)
        self.cover_at = cover_at

    def res(self, at, t0, after=None):
        """phrase -> its first occurrence at/after the scene start (so repeated words resolve locally)"""
        if at is None: return t0
        if isinstance(at, (int, float)): return t0 + at
        try: return self.ph(at, after=(t0 - 0.3) if after is None else after)
        except KeyError: return self.ph(at)

    def scene(self, c, t, i):
        sc = self.SC[i]; t0 = self.starts[i]; t1 = self.starts[i + 1] if i + 1 < len(self.SC) else self.END + 1
        paper(c, sc.get('bg', self.PAPER), t)
        sh = sc.get('shake')
        if sh:
            ts = self.res(sh, t0); u = (t - ts)
            if 0 <= u < 0.4: c.translate(14 * math.sin(u * 70) * (1 - u / 0.4), 8 * math.cos(u * 55) * (1 - u / 0.4))
        for (name, x, y, w, rot, at) in sc.get('photos', []):
            ta = self.res(at, t0)
            if t >= ta - 0.05: sticker_img(c, self.IM.get(name), x, y, w * (1 + 0.05 * cl((t - ta) / max(0.5, t1 - ta))), drop_k(t, ta - 0.05, 0.3), rot)
        for pr_ in sc.get('props', []):
            fn, x, y, w, h, rot, at = pr_[:7]; bg = pr_[7] if len(pr_) > 7 else (250, 248, 242); ta = self.res(at, t0)
            if t >= ta - 0.05: sticker_draw(c, fn, x, y, w, h, drop_k(t, ta - 0.05, 0.3), rot, bg=bg)
        for lb in sc.get('labels', []):
            txt, x, y, size, rot, at = lb[:6]; bg = lb[6] if len(lb) > 6 else (250, 246, 236); fg = lb[7] if len(lb) > 7 else INK
            ta = self.res(at, t0)
            if t >= ta - 0.08: label(c, txt, x, y, drop_k(t, ta - 0.08), rot, size, bg, fg)
        if 'arrow' in sc:
            x0, y0, x1, y1, at = sc['arrow']; ta = self.res(at, t0)
            if t >= ta: hand_arrow(c, x0, y0, x1, y1, t, eo(cl((t - ta) / 0.3)), self.HERO)
        for (txt, x, y, size, fn, col, at) in sc.get('big', []):
            ta = self.res(at, t0)
            if t >= ta - 0.05:
                f = (serif if fn == 'serif' else cond)(size); w = f.measureText(txt); k = eo(cl((t - ta + 0.05) / 0.2))
                c.save(); c.translate(x, y); c.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k); c.drawString(txt, -w / 2, 0, f, P(col, k)); c.restore()
        for (txt, x, y, size, col, at) in sc.get('words', []):
            ta = self.res(at, t0)
            if t >= ta - 0.08: boil_text(c, txt, x, y, size, t, ta - 0.08, col or self.HERO, scribble=0.14)
        if 'cap' in sc:
            y, size, col, until = sc['cap']; te = self.res(until, t0) if until is not None else t1
            if t < te: scap(c, self.T, t, t0, te - 0.02, y, size, col or CREAM)

    def frame(self, t):
        s = skia.Surface(W, H); c = s.getCanvas()
        i = max(j for j, t0 in enumerate(self.starts) if t >= t0); t0 = self.starts[i]
        gp = skia.Paint(); gp.setColorFilter(self.WARM); c.saveLayer(None, gp)
        w = whip(t, t0, 0.1) if i > 0 else 0.0
        c.save()
        if w > 0:
            c.translate(0, -H * 0.12 * w)
            p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(0.5, 50 * w)); c.saveLayer(None, p); self.scene(c, t, i); c.restore()
        else: self.scene(c, t, i)
        c.restore(); c.restore()
        if i == len(self.SC) - 1:   # brand end card
            k = pr(t, self.ph('send this') + 1.2, 0.4)
            if k > 0:
                wordmark(c, 540, 1365, 400, i not in self.LIGHT, k)
                g = capf(24); s_ = 'FOLLOW FOR DAILY BUSINESS BREAKDOWNS'
                c.drawString(s_, 540 - g.measureText(s_) / 2, 1470, g, P((30, 30, 30) if i in self.LIGHT else CREAM, k))
        halation(s, 0.14, 22)
        film(c, t, 0.06, 0.3 if i in self.LIGHT else 0.5)
        brand_badge(c)
        if i not in self.LIGHT and t > 0.8: series_tag(c, self.SERIES, self.NUM, self.ACC, t, self.DUR, dark=True)
        return s

    def cover(self, c):
        ca = self.cover_at(self) if callable(self.cover_at) else self.cover_at
        s = self.frame(ca if ca is not None else 2.0); c.drawImage(s.makeImageSnapshot(), 0, 0)

    def run(self):
        main(self.HERE, self.frame, self.cover, self.DUR)
