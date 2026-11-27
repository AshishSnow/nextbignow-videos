"""Drawn props for 16:9 long videos (generic, no logos): phone with app screens, notification, quote card, bar chart with source,
before/after card, receipt, price tag. Each returns a draw function for sticker_draw (drawn around 0,0)."""
from paper_wide import *

INK2 = (40, 24, 60)


def D_phone(screen='icons', label=None, accent=(232, 70, 60), w=300, h=600):
    def d(c):
        c.drawRRect(rr(-w / 2, -h / 2, w, h, 44), P((24, 22, 30)))
        S_ = skia.Rect.MakeXYWH(-w / 2 + 14, -h / 2 + 18, w - 28, h - 36)
        c.drawRRect(skia.RRect.MakeRectXY(S_, 32, 32), P((246, 242, 234)))
        c.drawRRect(rr(-40, -h / 2 + 26, 80, 18, 9), P((24, 22, 30)))
        if screen == 'icons':
            cols = [(232, 70, 60), (255, 196, 60), (80, 170, 230), (110, 200, 120), (160, 92, 240), (240, 140, 60)]
            for i in range(12):
                x = -w / 2 + 40 + (i % 3) * 80; y = -h / 2 + 90 + (i // 3) * 90
                col = accent if i == 4 else cols[i % 6]
                c.drawRRect(rr(x, y, 58, 58, 16), P(col if i == 4 else (*col,), 1.0 if i == 4 else 0.35))
            c.drawRRect(rr(-w / 2 + 120 - 6, -h / 2 + 270 - 6, 70, 70, 20), S(INK2, 4))
        elif screen == 'points':
            f = cond(70); g = capf(22)
            c.drawString('1,500', -f.measureText('1,500') / 2, -60, f, P(accent)); c.drawString('BONUS POINTS', -g.measureText('BONUS POINTS') / 2, -20, g, P(INK2))
            c.drawRRect(rr(-w / 2 + 40, 30, w - 80, 26, 13), P((220, 212, 200))); c.drawRRect(rr(-w / 2 + 40, 30, (w - 80) * 0.62, 26, 13), P(accent))
            c.drawString('NEXT REWARD', -g.measureText('NEXT REWARD') / 2, 100, g, P(INK2))
        elif screen == 'deal':
            f = cond(60); g = capf(22)
            c.drawRRect(rr(-w / 2 + 36, -150, w - 72, 220, 22), P(accent))
            for i, s_ in enumerate(('FREE', 'FRIES')): c.drawString(s_, -f.measureText(s_) / 2, -80 + i * 64, f, P((255, 250, 240)))
            c.drawString('APP ONLY', -g.measureText('APP ONLY') / 2, 120, g, P(INK2))
        elif screen == 'checkout':
            g = capf(24); f = cond(54)
            rows = label or [('SUBTOTAL', '$28.00'), ('SHIPPING', '$6.00'), ('TOTAL', '$34.00')]
            for i, (a, b) in enumerate(rows):
                y = -140 + i * 70; c.drawString(a, -w / 2 + 40, y, g, P(INK2)); c.drawString(b, w / 2 - 40 - g.measureText(b), y, g, P(INK2))
            c.drawRRect(rr(-w / 2 + 36, 110, w - 72, 70, 20), P(accent)); t = 'PAY'; c.drawString(t, -f.measureText(t) / 2, 165, f, P((255, 250, 240)))
    return d


def D_notif(title, body, accent=(232, 70, 60), w=560, h=130):
    def d(c):
        c.drawRRect(rr(-w / 2, -h / 2, w, h, 26), P((250, 248, 244)))
        c.drawRRect(rr(-w / 2 + 22, -h / 2 + 24, 64, 64, 16), P(accent))
        g = capf(24); f = serif(32)
        c.drawString(title, -w / 2 + 108, -h / 2 + 50, g, P(INK2)); c.drawString(body, -w / 2 + 108, -h / 2 + 94, f, P((90, 70, 100)))
    return d


def D_quote(lines, who, w=900, size=64, col=INK2):
    def d(c):
        f = serif(size); g = capf(26); n = len(lines); y0 = -(n * size * 1.15) / 2 + size * 0.7
        for i, L in enumerate(lines): c.drawString(L, -f.measureText(L) / 2, y0 + i * size * 1.15, f, P(col))
        c.drawString(who, -g.measureText(who) / 2, y0 + n * size * 1.15 + 20, g, P((150, 60, 50)))
    return d


def D_chart(vals, labels, cols, title=None, source=None, unit='', h=360, bw=150, gap=90, k=1.0):
    """bars that grow with k (pass a lambda via D_chart_t for animation)"""
    def d(c):
        n = len(vals); x0 = -(n * bw + (n - 1) * gap) / 2; mx = max(vals)
        if title: g = capf(28); c.drawString(title, -g.measureText(title) / 2, -h / 2 - 110, g, P(INK2))
        c.drawLine(x0 - 30, h / 2, -x0 + 30, h / 2, S(INK2, 4))
        for i, (v, lb, col) in enumerate(zip(vals, labels, cols)):
            x = x0 + i * (bw + gap); hh = h * v / mx * k
            c.drawRect(skia.Rect.MakeXYWH(x, h / 2 - hh, bw, hh), P(col)); c.drawRect(skia.Rect.MakeXYWH(x, h / 2 - hh, bw, hh), S(INK2, 3))
            f = cond(64); s_ = f'{v:g}{unit}'; c.drawString(s_, x + bw / 2 - f.measureText(s_) / 2, h / 2 - hh - 16, f, P(INK2))
            g = capf(24); c.drawString(lb, x + bw / 2 - g.measureText(lb) / 2, h / 2 + 40, g, P(INK2))
        if source: s2 = serif(24); c.drawString(source, -s2.measureText(source) / 2, h / 2 + 90, s2, P((110, 90, 120)))
    return d


def D_beforeafter(rows, head=('BEFORE', 'AFTER'), w=760, rowh=80):
    def d(c):
        g = capf(30); f = cond(58); n = len(rows); y0 = -(n * rowh) / 2
        c.drawString(head[0], -40 - g.measureText(head[0]), y0 - 20, g, P((120, 100, 130))); c.drawString(head[1], 150, y0 - 20, g, P((200, 60, 50)))
        for i, (lab, a, b) in enumerate(rows):
            y = y0 + 50 + i * rowh; s2 = serif(34)
            c.drawString(lab, -w / 2 + 20, y, s2, P(INK2))
            c.drawString(a, -40 - f.measureText(a), y + 8, f, P((120, 100, 130))); c.drawLine(-40 - f.measureText(a), y - 12, -40, y - 12, S((200, 60, 50), 5))
            c.drawString('→', 40, y + 6, cond(50), P(INK2)); c.drawString(b, 150, y + 8, f, P((200, 60, 50)))
    return d


def D_receipt(rows, total, w=420):
    def d(c):
        h = 140 + len(rows) * 56
        p = skia.Path(); p.moveTo(-w / 2, -h / 2)
        for i in range(12): p.lineTo(-w / 2 + (i + 0.5) * w / 12, -h / 2 + (12 if i % 2 == 0 else 0))
        p.lineTo(w / 2, -h / 2); p.lineTo(w / 2, h / 2); p.lineTo(-w / 2, h / 2); p.close(); c.drawPath(p, P((252, 250, 244)))
        g = serif(32); f = cond(50)
        for i, (a, b) in enumerate(rows):
            y = -h / 2 + 80 + i * 56; c.drawString(a, -w / 2 + 30, y, g, P(INK2)); c.drawString(b, w / 2 - 30 - g.measureText(b), y, g, P(INK2))
        c.drawLine(-w / 2 + 30, h / 2 - 70, w / 2 - 30, h / 2 - 70, S(INK2, 2))
        c.drawString('TOTAL', -w / 2 + 30, h / 2 - 22, f, P(INK2)); c.drawString(total, w / 2 - 30 - f.measureText(total), h / 2 - 22, f, P((200, 60, 50)))
    return d
