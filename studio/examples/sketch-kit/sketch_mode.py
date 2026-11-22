# ===================================================================== EDITORIAL SKETCH MODE (owner reference 21 Nov 2026)
# Appended after a day-comic renderer: re-skins the same scenes as cream paper + pen-and-ink crosshatch, serif headlines
# (Libre Caslon), deep-red italic accents, antique-gold tags. Subtitles stay crisp on top.
import sys as _sys
_sys.path.insert(0, '/home/claude/studio')
from lib_sketch import ink as _ink

_TFV = {}
END = TOK[-1][2] + 0.25; DUR = END + 0.05   # abrupt end on the payoff (playbook v2: no outro wipe, loop restarts)


def serif(size, weight=400, italic=False):
    key = (weight, italic)
    if key not in _TFV:
        base = skia.Typeface.MakeFromFile(os.path.join(FD, 'LibreCaslonText-Italic-VF.ttf' if italic else 'LibreCaslonText-VF.ttf'))
        coord = skia.FontArguments.VariationPosition.Coordinate(0x77676874, float(weight))
        fa = skia.FontArguments(); fa.setVariationDesignPosition(skia.FontArguments.VariationPosition(skia.FontArguments.VariationPosition.Coordinates([coord])))
        _TFV[key] = base.makeClone(fa)
    f = skia.Font(_TFV[key], size); f.setEdging(skia.Font.Edging.kAntiAlias); return f


INK_D, RED_D, GOLD_D = (34, 32, 30), (150, 22, 34), (190, 135, 30)


def _tone(rgb):
    r, g, b = rgb
    if r > 200 and g < 140 and b < 150: return RED_D, True          # reds/pinks -> deep red italic
    if r > 200 and g > 150 and b < 120: return GOLD_D, False         # yellows -> gold
    return INK_D, False


def neon_text(c, s, x, y, size, rgb, flick=1.0, fontname=None, rot=0):
    col, it = _tone(rgb)
    if rgb == (255, 255, 255): col = INK_D
    f = serif(size * 0.95, 700 if not it else 400, it); tw = f.measureText(s); a = max(0.0, min(1.0, flick))
    lim = 900
    if _LB[0] and abs(x - (_LB[0][0] + _LB[0][2] / 2)) < 8 and _LB[0][1] - 20 < y < _LB[0][1] + _LB[0][3] + 20: lim = min(lim, _LB[0][2] - 70)
    while tw > lim and f.getSize() > 20: f = serif(f.getSize() * 0.94, 700 if not it else 400, it); tw = f.measureText(s)
    c.save(); c.translate(x, y); c.rotate(rot); c.drawString(s, -tw / 2, 0, f, P(col, a)); c.restore(); return tw


def ctext(c, s, x, y, size, rgb, fn='Montserrat-Black.ttf', a=1.0):
    col = INK_D if (rgb[0] + rgb[1] + rgb[2]) > 600 or rgb[2] > rgb[0] else _tone(rgb)[0]
    f = serif(size * 0.92, 600)
    while f.measureText(s) > 900 and f.getSize() > 16: f = serif(f.getSize() * 0.94, 600)
    c.drawString(s, x - f.measureText(s) / 2, y, f, P(col, a))


_LB = [None]


def board(c, x, y, w, h, col=(255, 255, 255)):
    _LB[0] = (x, y, w, h)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 6, 6)
    c.drawRRect(r, P(col if col != (255, 255, 255) else (252, 250, 244)))
    c.drawRRect(r, S(INK_D, 3)); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 8, y + 8, w - 16, h - 16), 4, 4), S(INK_D, 1.2, 0.7))


def screen(c, x, y, w, h, draw, glowc=None, on=1.0):
    board(c, x - 16, y - 16, w + 32, h + 32)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h)); c.translate(x, y); draw(c); c.restore()


_person_full = person


def person(c, x, y, s, *a, **k):
    if y > 1520: return          # bottom zone is covered by IG/YT captions + buttons: skip decorative mascot
    _person_full(c, x, y, s, *a, **k)


def sparkle(c, x, y, r, a=1.0): pass
def vignette(c, a=0.5): pass


def paper_bg(c, t, skyline=True, ground=True):
    c.drawRect(skia.Rect.MakeWH(W, H), P((252, 250, 244)))
    if skyline:
        rnd = random.Random(11); x = 30
        while x < W:
            w = rnd.randint(70, 150); h = rnd.randint(200, 430)
            r = skia.Rect.MakeXYWH(x, 1240 - h, w, h); c.drawRect(r, P((222, 222, 222))); c.drawRect(r, S((120, 120, 120), 2))
            for wy in range(int(1240 - h + 24), 1220, 46): c.drawLine(x + 10, wy, x + w - 10, wy, S((150, 150, 150), 1.5))
            x += w + rnd.randint(-10, 30)
    if ground:
        c.drawLine(0, 1240, W, 1240, S(INK_D, 3)); c.drawLine(0, 1252, W, 1250, S(INK_D, 1.2, 0.6))


def _sk_bg(c, t, *a, **k): paper_bg(c, t)
for _n in ('street', 'sky_bg', 'sky_air', 'city_bg', 'store_inside', 'counter_bg', 'kitchen_bg'):
    if _n in globals(): globals()[_n] = _sk_bg
_FULL = skia.Rect.MakeWH(W, H)


class _PaperCanvas:
    """proxy that swaps any full-screen gradient wash for paper (scenes often start with drawRect(MakeWH(W,H), LG(...)))."""
    def __init__(self, c): self._c = c
    def drawRect(self, r, p):
        if abs(r.width() - W) < 1 and abs(r.height() - H) < 1 and r.left() == 0 and r.top() == 0 and p.getAlphaf() > 0.9:
            return self._c.drawRect(r, P((252, 250, 244)))
        return self._c.drawRect(r, p)
    def __getattr__(self, n): return getattr(self._c, n)


def frame(t):
    s = skia.Surface(W, H); c0 = s.getCanvas(); c = _PaperCanvas(c0)
    c0.drawRect(_FULL, P((252, 250, 244)))
    sx = sy = 0.0
    for (ts, a, d) in SHAKES:
        if ts <= t < ts + d:
            k = 1 - (t - ts) / d; sx += a * k * math.sin(t * 90); sy += a * k * math.cos(t * 77)
    c0.save(); c0.translate(sx, sy)
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0)
    draw_scene(c, i, t)
    if i > 0 and t < SCENES[i][0] + TR:     # page-turn wipe: old page slides out
        k = eio((t - SCENES[i][0]) / TR)
        c0.saveLayer(paint=None); c0.translate(-W * k, 0); c0.drawRect(_FULL, P((252, 250, 244))); draw_scene(c, i - 1, t); c0.restore()
        c0.drawRect(skia.Rect.MakeXYWH(W * (1 - k) - 6, 0, 12, H), P((0, 0, 0), 0.25, 8))
    if t > END:
        r = 1500 * eio(pr(t, END, 0.8)); c0.drawCircle(540, 900, r, P((252, 250, 244)))
    c0.restore()
    return s


def subs(c, t, y):
    for ch in CH:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.15:
            f = serif(42, 500, True); sp = f.measureText(' ')
            ws = [w for w, a, b in ch]; tw = sum(f.measureText(w) for w in ws) + sp * (len(ws) - 1)
            x = 540 - tw / 2
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 22, y - 44, tw + 44, 62), 8, 8, P((252, 250, 244), 0.92))
            for w, a, b in ch:
                on = a - 0.03 <= t <= b + 0.08
                if on: c.drawRect(skia.Rect.MakeXYWH(x, y + 6, f.measureText(w), 5), P(GOLD_D))
                c.drawString(w, x, y, f, P(RED_D if on else INK_D))
                x += f.measureText(w) + sp
            return


def both(t):
    raw = frame(t).makeImageSnapshot()
    arr = raw.toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]
    sk = _ink(np.ascontiguousarray(arr))
    rgba = np.dstack([sk, np.full(sk.shape[:2], 255, np.uint8)])
    base = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
    ig = skia.Surface(W, H); c = ig.getCanvas(); c.drawImage(base, 0, 0)
    if 0.3 < t < END + 0.1: subs(c, t, 1442)
    yt = skia.Surface(W, H); c = yt.getCanvas(); c.drawImage(base, 0, 0)
    if 0.3 < t < END + 0.1: subs(c, t, 1320)
    return ig.makeImageSnapshot(), yt.makeImageSnapshot()
