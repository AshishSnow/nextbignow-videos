"""OopsMyBusiness logo concepts in the ESSAY system (cream / near-black / condensed caps / one accent block that changes colour per reel)."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
from essay_lib import *

OUT = os.path.dirname(os.path.abspath(__file__))
ACCS = [(138, 66, 214), (214, 52, 44), (34, 140, 92), (232, 150, 20), (36, 98, 214)]


def surf(w, h): s = skia.Surface(w, h); return s, s.getCanvas()


def tracked(c, s, x, y, size, col, sp=6, w='SemiBold', center=True):
    f = font(size, w, False); tw = sum(f.measureText(ch) + sp for ch in s) - sp; xx = x - tw / 2 if center else x
    for ch in s: c.drawString(ch, xx, y, f, P(col)); xx += f.measureText(ch) + sp
    return tw


def grain(c, w, h, col, amt=4):
    rnd = np.random.default_rng(1); n = rnd.normal(0, 1, (h, w)) * amt
    img = np.clip(np.array(col, np.float32)[None, None, :] + n[..., None], 0, 255).astype(np.uint8)
    c.drawImage(skia.Image.fromarray(np.ascontiguousarray(np.dstack([img, np.full((h, w), 255, np.uint8)])), colorType=skia.kRGBA_8888_ColorType), 0, 0)


# ---- A: THE BLOCK  (OOPS over an accent block reading MY BUSINESS)
def a_avatar(acc_):
    s, c = surf(1080, 1080); grain(c, 1080, 1080, CREAM)
    f = anton(400); t = 'OOPS'; c.drawString(t, 540 - f.measureText(t) / 2, 600, f, P(INKE))
    c.drawRect(skia.Rect.MakeXYWH(170, 650, 740, 170), P(acc_))
    tracked(c, 'MY BUSINESS', 540, 765, 84, CREAM_T, 10, 'Bold')
    return s


def a_wordmark(acc_):
    s, c = surf(2000, 600); grain(c, 2000, 600, CREAM)
    f = anton(280); t = 'OOPS,'; c.drawString(t, 100, 420, f, P(INKE)); x = 100 + f.measureText(t) + 30
    g = anton(210); gw = g.measureText('MY BUSINESS'); c.drawRect(skia.Rect.MakeXYWH(x, 170, gw + 60, 270), P(acc_)); c.drawString('MY BUSINESS', x + 30, 400, g, P(CREAM_T))
    return s


# ---- B: THE SQUARE DOT  (oops. on black; the full stop is the accent square = the brand device)
def b_avatar(acc_):
    s, c = surf(1080, 1080); grain(c, 1080, 1080, DARK, 3)
    f = anton(640); c.drawString('O', 300, 820, f, P(CREAM_T)); ow = f.measureText('O')
    c.drawRect(skia.Rect.MakeXYWH(300 + ow + 30, 690, 130, 130), P(acc_))
    return s


def b_wordmark(acc_):
    s, c = surf(2000, 600); grain(c, 2000, 600, DARK, 3)
    f = anton(330); t = 'OOPS'; c.drawString(t, 130, 440, f, P(CREAM_T)); x = 130 + f.measureText(t) + 26
    c.drawRect(skia.Rect.MakeXYWH(x, 370, 74, 74), P(acc_))
    tracked(c, 'MY BUSINESS', x + 120, 440, 64, CREAM_T, 14, 'Bold', center=False)
    tracked(c, 'BUSINESS, EXPLAINED.', x + 120, 360, 30, MUTE, 8, 'Medium', center=False)
    return s


# ---- C: THE ESSAY MONOGRAM  (OMB with the M on the block, grid lines, N° tag)
def c_avatar(acc_):
    s, c = surf(1080, 1080); grain(c, 1080, 1080, CREAM)
    for x in (180, 900): c.drawLine(x, 0, x, 1080, S(acc_, 3, 0.45))
    f = anton(460); o, m, b = 'O', 'M', 'B'; wo, wm, wb = f.measureText(o), f.measureText(m), f.measureText(b); gap = 18
    tw = wo + wm + wb + 2 * gap; x = 540 - tw / 2; y = 720
    c.drawString(o, x, y, f, P(INKE)); x += wo + gap
    c.drawRect(skia.Rect.MakeXYWH(x - 26, y - 420, wm + 52, 470), P(acc_)); c.drawString(m, x, y, f, P(CREAM_T)); x += wm + gap
    c.drawString(b, x, y, f, P(INKE))
    tracked(c, 'N° 01 — OOPS, MY BUSINESS', 540, 850, 36, INKE, 6, 'Medium')
    return s


def c_wordmark(acc_):
    s, c = surf(2000, 600); grain(c, 2000, 600, CREAM)
    f = anton(330); x = 120; y = 440
    for ch, hl in (('O', 0), ('M', 1), ('B', 0)):
        w = f.measureText(ch)
        if hl: c.drawRect(skia.Rect.MakeXYWH(x - 20, y - 300, w + 40, 340), P(acc_))
        c.drawString(ch, x, y, f, P(CREAM_T if hl else INKE)); x += w + 14
    c.drawLine(x + 40, 150, x + 40, 460, S(INKE, 3))
    g = anton(120); c.drawString('OOPS,', x + 90, 300, g, P(INKE)); c.drawString('MY BUSINESS', x + 90, 430, g, P(INKE))
    return s


def circle_preview(img, size=300):
    s, c = surf(size, size); c.clear(skia.ColorTRANSPARENT)
    c.save(); p = skia.Path(); p.addCircle(size / 2, size / 2, size / 2); c.clipPath(p, doAntiAlias=True)
    c.drawImageRect(img, skia.Rect.MakeWH(size, size), skia.SamplingOptions(skia.FilterMode.kLinear)); c.restore()
    return s.makeImageSnapshot()


if __name__ == '__main__':
    sets = [('A', 'The Block', a_avatar, a_wordmark), ('B', 'The Square Dot', b_avatar, b_wordmark), ('C', 'The Monogram', c_avatar, c_wordmark)]
    for k, name, av, wm in sets:
        av(ACCS[0]).makeImageSnapshot().save(os.path.join(OUT, 'logo_%s_avatar.png' % k), skia.kPNG)
        wm(ACCS[0]).makeImageSnapshot().save(os.path.join(OUT, 'logo_%s_wordmark.png' % k), skia.kPNG)
    # presentation sheet
    SW, SH = 2400, 3000
    s, c = surf(SW, SH); grain(c, SW, SH, (226, 220, 208))
    f = anton(110); c.drawString('OOPS, MY BUSINESS — LOGO OPTIONS', 120, 200, f, P(INKE))
    tracked(c, 'ONE ACCENT BLOCK THAT CHANGES COLOUR WITH EVERY REEL', 120, 270, 34, INKE, 6, 'Medium', center=False)
    y = 360
    for k, name, av, wm in sets:
        c.drawString(k + '  ' + name.upper(), 120, y + 70, anton(70), P(INKE))
        a = av(ACCS[0]).makeImageSnapshot(); w = wm(ACCS[0]).makeImageSnapshot()
        c.drawImage(circle_preview(a, 380), 120, y + 110)
        c.drawImageRect(w, skia.Rect.MakeXYWH(560, y + 150, 1260, 378), skia.SamplingOptions(skia.FilterMode.kLinear))
        for i, ac in enumerate(ACCS):   # colour rotation
            c.drawImage(circle_preview(av(ac).makeImageSnapshot(), 150), 1880 + (i % 2) * 170, y + 100 + (i // 2) * 160)
        y += 860
    s.makeImageSnapshot().save(os.path.join(OUT, 'logo_options.png'), skia.kPNG)
    print('ok')
