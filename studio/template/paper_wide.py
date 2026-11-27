"""16:9 long-form version of the PAPER look (YouTube 5-6 min case studies). Run modules with OMB_WIDE=1.
Adds to paper_story scenes:
  cuts     [(asset, x, y, h, rot, at), ...]   person cut-outs (RGBA png): white die-cut outline + soft shadow, gentle sway
  chapter  ('CHAPTER 2', 'The highway moved')  chapter card (number + serif title)
Brand: 'O.' badge top-right, series tag top-left, wordmark on the end card."""
import os
os.environ.setdefault('OMB_WIDE', '1')
from paper_story import *
import numpy as np
from PIL import Image, ImageFilter

assert W == 1920 and H == 1080, 'run with OMB_WIDE=1'


def load_cut(path, mode='sepia'):
    try: im = Image.open(path).convert('RGBA')
    except Exception: return None
    a = im.split()[-1]
    rgb = im.convert('RGB')
    if mode == 'sepia':
        g = np.asarray(rgb.convert('L'), np.float32)[..., None] / 255
        rgb = Image.fromarray(np.concatenate([g * 245 + 8, g * 228 + 12, g * 200 + 18], -1).clip(0, 255).astype(np.uint8))
    # white die-cut border: dilate alpha
    border = a.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(1.2))
    W_, H_ = im.size; out = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    out.paste(Image.new('RGBA', (W_, H_), (250, 248, 242, 255)), (0, 0), border)
    rgb.putalpha(a); out.alpha_composite(rgb)
    return sk(out), sk(Image.merge('RGBA', [Image.new('L', (W_, H_), 20), Image.new('L', (W_, H_), 8), Image.new('L', (W_, H_), 30), border.filter(ImageFilter.GaussianBlur(14))]))


def draw_cut(c, pair, x, y, h, k, t, rot=0.0):
    if not pair or k <= 0: return
    img, sh = pair; w = h * img.width() / img.height(); s = 1.0 + 0.12 * (1 - eback(k)); lift = 50 * (1 - eo(k))
    sway = 1.2 * math.sin(t * 0.9)
    c.save(); c.translate(x, y - lift); c.rotate(rot + sway + 3 * (1 - eo(k))); c.scale(s, s)
    R = skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h); smp = skia.SamplingOptions(skia.FilterMode.kLinear)
    c.drawImageRect(sh, R.makeOffset(14, 22), smp, skia.Paint(Alphaf=0.6 * eo(k)))
    c.drawImageRect(img, R, smp, skia.Paint(AntiAlias=True))
    c.restore()


class WideStory(Story):
    def __init__(self, HERE, series, num, scenes_fn, assets, cuts=None, **kw):
        A = os.path.join(HERE, 'assets'); self.CUT = {k: load_cut(os.path.join(A, v[0]), v[1] if len(v) > 1 else 'sepia') for k, v in (cuts or {}).items()}
        super().__init__(HERE, series, num, scenes_fn, assets, **kw)

    def scene(self, c, t, i):
        super().scene(c, t, i)
        sc = self.SC[i]; t0 = self.starts[i]
        for (name, x, y, h, rot, at) in sc.get('cuts', []):
            ta = self.res(at, t0)
            if t >= ta - 0.05: draw_cut(c, self.CUT.get(name), x, y, h, drop_k(t, ta - 0.05, 0.35), t, rot)
        if 'chapter' in sc:
            num, title = sc['chapter']; k = eo(cl((t - t0) / 0.4))
            f = capf(34); c.drawString(num, W / 2 - f.measureText(num) / 2, 430, f, P(self.HERO, k))
            c.drawRect(skia.Rect.MakeXYWH(W / 2 - 60 * k, 455, 120 * k, 4), P(self.HERO, k))
            g = serif(130); c.drawString(title, W / 2 - g.measureText(title) / 2, 610, g, glow_paint(CREAM, k))

    def frame(self, t):
        s = skia.Surface(W, H); c = s.getCanvas()
        i = max(j for j, t0 in enumerate(self.starts) if t >= t0); t0 = self.starts[i]
        gp = skia.Paint(); gp.setColorFilter(self.WARM); c.saveLayer(None, gp)
        w = whip(t, t0, 0.1) if i > 0 else 0.0
        c.save()
        if w > 0:
            c.translate(-W * 0.06 * w, 0)
            p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(50 * w, 0.5)); c.saveLayer(None, p); self.scene(c, t, i); c.restore()
        else: self.scene(c, t, i)
        c.restore(); c.restore()
        if i == len(self.SC) - 1:
            k = pr(t, t0 + 0.6, 0.4)
            if k > 0:
                wordmark(c, W / 2, 760, 520, i not in self.LIGHT, k)
                g = capf(26); s_ = 'ONE BUSINESS STORY EVERY DAY'
                c.drawString(s_, W / 2 - g.measureText(s_) / 2, 870, g, P((30, 30, 30) if i in self.LIGHT else CREAM, k))
        halation(s, 0.14, 22)
        film(c, t, 0.06, 0.3 if i in self.LIGHT else 0.5)
        brand_badge(c, W - 100, 92, 48)
        if i not in self.LIGHT and t > 0.8: series_tag(c, self.SERIES, self.NUM, self.ACC, t, self.DUR, x=70, y=100, dark=True)
        return s
