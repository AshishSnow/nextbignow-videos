"""Drawn props for 9:16 PAPER reels (generic, no logos). Each returns drawfn(c) drawn around 0,0 for the 'props' scene key."""
from paper_story import *

INK2 = (40, 24, 60)


def D_phone(screen='blank', label=None, accent=(232, 70, 60), w=300, h=600, txt=None):
    def d(c):
        c.drawRRect(rr(-w / 2, -h / 2, w, h, 44), P((24, 22, 30)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 14, -h / 2 + 18, w - 28, h - 36), 32, 32), P((246, 242, 234)))
        c.drawRRect(rr(-40, -h / 2 + 26, 80, 18, 9), P((24, 22, 30)))
        if txt:
            f = cond(64)
            for i, s_ in enumerate(txt): c.drawString(s_, -f.measureText(s_) / 2, -30 + i * 70, f, P(accent))
    return d


def D_bar(gaps=1.0, n=7, w=720, h=210, col=(214, 170, 92), label=None):
    """triangular chocolate bar, generic. gaps: 1.0 = normal, 2.2 = wide gaps"""
    def d(c):
        base = h * 0.32; c.drawRRect(rr(-w / 2, h / 2 - base, w, base, 10), P((120, 72, 40)))
        fr = 0.1 * (gaps - 1); tw = w / (n + (n - 1) * fr); gap = tw * fr
        for i in range(n):
            x = -w / 2 + i * (tw + gap); p = skia.Path(); p.moveTo(x, h / 2 - base); p.lineTo(x + tw / 2, -h / 2); p.lineTo(x + tw, h / 2 - base); p.close()
            c.drawPath(p, P((120, 72, 40))); p2 = skia.Path(); p2.moveTo(x + tw / 2, -h / 2); p2.lineTo(x + tw, h / 2 - base); p2.lineTo(x + tw / 2, h / 2 - base); p2.close()
            c.drawPath(p2, P((92, 52, 28)))
        if label:
            g = capf(34); c.drawString(label, -g.measureText(label) / 2, h / 2 + 52, g, P(INK2))
    return d


def D_cups(sizes=(('SHORT', 8), ('TALL', 12), ('GRANDE', 16), ('VENTI', 20)), hide=None, hi=None, col=(250, 248, 242), accent=(232, 70, 60)):
    """row of paper cups scaled by ounces. hide: index drawn faded/dashed; hi: index highlighted"""
    def d(c):
        n = len(sizes); xs = [(i - (n - 1) / 2) * 210 for i in range(n)]
        for i, ((nm, oz), x) in enumerate(zip(sizes, xs)):
            h = 120 + oz * 16; wt = 80 + oz * 4; wb = wt * 0.74; yb = 190
            p = skia.Path(); p.moveTo(x - wt / 2, yb - h); p.lineTo(x + wt / 2, yb - h); p.lineTo(x + wb / 2, yb); p.lineTo(x - wb / 2, yb); p.close()
            a = 0.28 if hide == i else 1.0
            c.drawPath(p, P(accent if hi == i else col, a)); c.drawPath(p, S(INK2, 5, a))
            c.drawRRect(rr(x - wt / 2 - 10, yb - h - 22, wt + 20, 24, 8), P((60, 40, 30), a))
            g = capf(30); s_ = f'{oz} OZ'; c.drawString(s_, x - g.measureText(s_) / 2, yb - h / 2 + 10, g, P(INK2, a))
            g2 = capf(28); c.drawString(nm, x - g2.measureText(nm) / 2, yb + 50, g2, P(INK2, a))
    return d


def D_mattress(name, price=None, w=720, h=300, tag=(255, 214, 64)):
    def d(c):
        c.drawRRect(rr(-w / 2, -h / 2 + 60, w, h - 60, 40), P((246, 244, 240))); c.drawRRect(rr(-w / 2, -h / 2 + 60, w, h - 60, 40), S(INK2, 5))
        for i in range(1, 6):
            x = -w / 2 + i * w / 6; c.drawLine(x, -h / 2 + 90, x, h / 2 - 30, S((200, 196, 210), 3))
        c.drawLine(-w / 2 + 20, -h / 2 + 120, w / 2 - 20, -h / 2 + 120, S((200, 196, 210), 3))
        f = cond(54); tw = f.measureText(name) + 60
        c.save(); c.rotate(-4); c.drawRRect(rr(-tw / 2, -h / 2 - 40, tw, 100, 14), P(tag)); c.drawRRect(rr(-tw / 2, -h / 2 - 40, tw, 100, 14), S(INK2, 4))
        c.drawString(name, -f.measureText(name) / 2, -h / 2 + 28, f, P(INK2)); c.restore()
        if price:
            g = cond(60); c.drawString(price, w / 2 - 40 - g.measureText(price), h / 2 - 50, g, P((200, 60, 50)))
    return d
