"""NextBigNow 'editorial' design kit (Nov 2026 rebrand): cream paper + deep red, Inter Display Black type with
tight tracking, marker highlights, floating paper cards with soft shadows, mono labels, redaction bars, clean charts.
No real logos or photos of real people: sources are named in plain type."""
import math
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp

CREAM = (246, 240, 231); CREAM_D = (233, 224, 211); PAPER = (255, 255, 255)
INK = (17, 17, 17); GREY = (120, 116, 110); LIGHT = (200, 194, 186)
RED = (222, 32, 44); RED_D = (150, 8, 22); RED_L = (255, 90, 90)
GREEN = (30, 205, 120); YEL = (255, 214, 60); BLUE = (40, 110, 240)

_FILES = {
    'blk': '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf',
    'xb': '/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf',
    'b': '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf',
    'sb': '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf',
    'md': '/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf',
    'mono': '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
    'serif': '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf',
}
_tf, _fc = {}, {}


def F(key, size):
    k = (key, round(size, 1))
    if k not in _fc:
        if key not in _tf: _tf[key] = skia.Typeface.MakeFromFile(_FILES[key])
        f = skia.Font(_tf[key], size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True)
        _fc[k] = f
    return _fc[k]


def tw(text, key, size, track=-0.03):
    f = F(key, size)
    return sum(f.measureText(ch) for ch in text) + track * size * max(0, len(text) - 1)


def text(c, s, x, y, key='blk', size=100, col=INK, align='l', track=-0.03, a=1.0, maxw=None):
    """tracked text; returns width. align l/c/r; y = baseline."""
    if maxw:
        while tw(s, key, size, track) > maxw and size > 10: size *= 0.95
    w = tw(s, key, size, track)
    x0 = x - (w / 2 if align == 'c' else w if align == 'r' else 0)
    f = F(key, size); p = paint(col, a)
    for ch in s:
        c.drawString(ch, x0, y, f, p); x0 += f.measureText(ch) + track * size
    return w


def mono(c, s, x, y, size=26, col=GREY, align='l', a=1.0):
    return text(c, s.upper(), x, y, 'mono', size, col, align, track=0.18, a=a)


def bg_cream(c, t=0.0):
    c.drawRect(R.MakeWH(W, H), paint(CREAM))
    c.drawCircle(W / 2, H * 0.45, 1100, paint(shader=skia.GradientShader.MakeRadial((W / 2, H * 0.45), 1100, [argb((255, 252, 246)), argb(CREAM_D)])))
    _grain(c, 0.035)


def bg_red(c, t=0.0):
    c.drawRect(R.MakeWH(W, H), paint(RED_D))
    c.drawCircle(W / 2, H * 0.42, 1250, paint(shader=skia.GradientShader.MakeRadial((W / 2, H * 0.42), 1250, [argb((238, 46, 58)), argb((120, 0, 14))])))
    _grain(c, 0.05)


def bg_ink(c, t=0.0):
    c.drawRect(R.MakeWH(W, H), paint((14, 14, 16)))
    c.drawCircle(W / 2, H * 0.45, 1100, paint(shader=skia.GradientShader.MakeRadial((W / 2, H * 0.45), 1100, [argb((44, 44, 50)), argb((10, 10, 12))])))
    _grain(c, 0.05)


_GR = None
def _grain(c, a):
    global _GR
    if _GR is None:
        import numpy as np
        rng = np.random.default_rng(3)
        n = (rng.random((480, 270)) * 255).astype('uint8')
        arr = np.stack([n, n, n, np.full_like(n, 255)], -1)
        _GR = skia.Image.fromarray(arr)
    p = skia.Paint(); p.setAlphaf(a); p.setBlendMode(skia.BlendMode.kOverlay)
    c.drawImageRect(_GR, R.MakeWH(W, H), skia.SamplingOptions(), p)


def highlight(c, x, y, w, h, k, col=GREEN):
    """marker bar that sweeps left->right behind text (draw BEFORE text)."""
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x, y, w * eo(cl(k)), h), paint(col))


def headline(c, lines, x, y, size, t, t0, col=INK, hl=None, hl_col=GREEN, hl_col_txt=None, lead=1.02, align='l', stagger=0.08, key='blk'):
    """multi-line big headline; lines rise in one by one. hl = (line_index, word) to mark with a highlight bar.
    Size shrinks so every line fits inside the safe width (x 90..930)."""
    maxw = 930 - (x if align == 'l' else 0) if align == 'l' else 840
    while max(tw(ln, key, size) for ln in lines) > maxw and size > 40: size *= 0.96
    for i, ln in enumerate(lines):
        k = pr(t, t0 + i * stagger, 0.35)
        if k <= 0: continue
        yy = y + i * size * lead + 40 * (1 - eo(k))
        if hl and hl[0] == i:
            w = tw(ln, key, size)
            x0 = x - (w / 2 if align == 'c' else 0)
            pre, word = hl[1]
            px = tw(pre, key, size) + (-0.03 * size if pre else 0)
            ww = tw(word, key, size)
            highlight(c, x0 + px - size * 0.06, yy - size * 0.78, ww + size * 0.14, size * 0.94, pr(t, t0 + i * stagger + 0.2, 0.35), hl_col)
            text(c, ln, x, yy, key, size, col, align, a=eo(k))
        else:
            text(c, ln, x, yy, key, size, col, align, a=eo(k))


def shadow_rrect(c, r, rad, blur=28, a=0.18, dy=18):
    rr = skia.RRect.MakeRectXY(r.makeOffset(0, dy), rad, rad)
    c.drawRRect(rr, paint((0, 0, 0), a, blur=blur))


def card(c, cx, cy, w, h, rot, k, draw=None, col=PAPER, rad=26, drop=60):
    """floating paper card: drops in (k 0..1), soft shadow, slight rotation. draw(cc) gets local coords with (0,0)=top-left."""
    if k <= 0: return
    kk = eback(cl(k), 1.3)
    c.save(); c.translate(cx, cy + drop * (1 - eo(cl(k)))); c.rotate(rot * (0.6 + 0.4 * kk)); s = 0.92 + 0.08 * kk; c.scale(s, s)
    r = R.MakeXYWH(-w / 2, -h / 2, w, h)
    shadow_rrect(c, r, rad, a=0.22 * cl(k))
    c.drawRRect(skia.RRect.MakeRectXY(r, rad, rad), paint(col, cl(k * 1.5)))
    if draw:
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(r, rad, rad), True); c.translate(-w / 2, -h / 2)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * cl(k * 1.3)))
            draw(c); c.restore()
        else: draw(c)
        c.restore()
    c.restore()


def redact(c, x, y, widths, h=34, gap=14, line_gap=50, k=1.0, col=INK):
    """rows of black redaction bars; widths = list of rows, each a list of bar widths. k reveals bars."""
    n = sum(len(r) for r in widths); i = 0
    for ri, row in enumerate(widths):
        xx = x
        for bw in row:
            kk = cl(k * n - i)
            if kk > 0: c.drawRect(R.MakeXYWH(xx, y + ri * line_gap, bw * eo(kk), h), paint(col))
            xx += bw + gap; i += 1


def source_card(c, cx, cy, w, h, rot, k, outlet, date, head_lines, t, body_rows=3, head_size=64, label='AS REPORTED BY', underline=None):
    """news card: mono label, outlet in plain bold type (no logos), mono date, rule, bold headline, redacted body."""
    def dr(cc):
        mono(cc, label, 56, 74, 24)
        text(cc, outlet, 56, 136, 'b', 46, INK, track=-0.02)
        mono(cc, date, w - 56, 132, 24, INK, align='r')
        cc.drawLine(56, 162, w - 56, 162, stroke(INK, 3))
        yy = 162 + head_size * 1.25
        for i, ln in enumerate(head_lines):
            text(cc, ln, 56, yy + i * head_size * 1.08, 'blk', head_size, INK, maxw=w - 112)
        rows = [[(w - 112) * f for f in fr] for fr in ((0.32, 0.6), (0.5, 0.42), (0.22, 0.4, 0.28))[:body_rows]]
        redact(cc, 56, yy + len(head_lines) * head_size * 1.08 + 10, rows, h=26, line_gap=44, col=(30, 30, 30))
    card(c, cx, cy, w, h, rot, k, dr)



def pill(c, x, y, s, k, col=INK, txt=PAPER, size=40, key='b'):
    if k <= 0: return
    kk = eback(cl(k), 1.5)
    w = tw(s, key, size, -0.01) + size * 1.1; h = size * 1.7
    c.save(); c.translate(x, y); c.scale(kk, kk)
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2), paint(col))
    text(c, s, 0, size * 0.36, key, size, txt, 'c', track=-0.01)
    c.restore()


def line_chart(c, x, y, w, h, pts, k, col=RED, grid=True, labels=None, ymax=None, fill=True):
    """pts = list of (fx 0..1, value). k reveals left->right."""
    ymax = ymax or max(v for _, v in pts) * 1.1
    if grid:
        for i in range(5):
            gy = y + h - h * i / 4
            c.drawLine(x, gy, x + w, gy, stroke(LIGHT, 2))
    path = skia.Path(); first = True; lastx = lasty = None
    n = 120
    for j in range(n + 1):
        fx = j / n
        if fx > k: break
        for a_, b_ in zip(pts, pts[1:]):
            if a_[0] <= fx <= b_[0]:
                u = (fx - a_[0]) / max(1e-6, b_[0] - a_[0]); u = u * u * (3 - 2 * u)
                v = a_[1] + (b_[1] - a_[1]) * u; break
        px, py = x + w * fx, y + h - h * v / ymax
        (path.moveTo if first else path.lineTo)(px, py); first = False; lastx, lasty = px, py
    if lastx is None: return
    if fill:
        fp = skia.Path(path); fp.lineTo(lastx, y + h); fp.lineTo(x, y + h); fp.close()
        c.drawPath(fp, paint(shader=lin(0, y, 0, y + h, [argb(col, 0.28), argb(col, 0.0)])))
    c.drawPath(path, stroke(col, 7))
    c.drawCircle(lastx, lasty, 12, paint(col)); c.drawCircle(lastx, lasty, 24, paint(col, 0.25))
    if labels:
        for fx, s in labels:
            mono(c, s, x + w * fx, y + h + 44, 22, GREY, 'c')


def spinner(c, x, y, r, t, col=GREY):
    for i in range(10):
        a = i / 10 * 6.283 + t * 6
        c.drawCircle(x + math.cos(a) * r, y + math.sin(a) * r, r * 0.16, paint(col, (i + 1) / 10))


def inbox(c, cx, cy, w, h, rot, k, t, broken=0.0, title='Inbox'):
    """generic email client window (no brand marks). broken 0..1 fades rows and shows an error banner + spinner."""
    def dr(cc):
        cc.drawRect(R.MakeXYWH(0, 0, w, 90), paint((242, 242, 246)))
        for i, col_ in enumerate(((255, 95, 87), (255, 189, 46), (40, 200, 64))):
            cc.drawCircle(46 + i * 40, 45, 13, paint(col_))
        text(cc, title, 190, 60, 'b', 36, INK)
        cc.drawRect(R.MakeXYWH(0, 90, 210, h - 90), paint((248, 248, 250)))
        for i, s in enumerate(('Inbox', 'Sent', 'Drafts', 'Calendar', 'Teams')):
            text(cc, s, 34, 160 + i * 64, 'md', 30, GREY if i else INK)
        for i in range(7):
            yy = 120 + i * 108; a_ = 1 - 0.75 * broken
            cc.drawCircle(262, yy + 40, 24, paint([(255, 160, 80), (90, 160, 250), (120, 210, 150), (230, 120, 200)][i % 4], a_))
            cc.drawRect(R.MakeXYWH(304, yy + 18, (w - 360) * (0.45 + 0.2 * hsh(i, 2)), 20), paint((40, 40, 40), a_))
            cc.drawRect(R.MakeXYWH(304, yy + 52, (w - 360) * (0.7 + 0.2 * hsh(i, 3)), 16), paint((190, 190, 196), a_))
            cc.drawLine(230, yy + 96, w, yy + 96, stroke((236, 236, 240), 2))
        if broken > 0:
            cc.drawRect(R.MakeXYWH(210, 90, w - 210, h - 90), paint((255, 255, 255), 0.55 * broken))
            spinner(cc, 210 + (w - 210) / 2, h / 2 - 20, 46, t)
            bh = 120
            cc.drawRect(R.MakeXYWH(210, h - bh, w - 210, bh), paint(RED, broken))
            text(cc, "We can't connect right now", 210 + (w - 210) / 2, h - bh / 2 + 14, 'b', 36, PAPER, 'c', a=broken)
    card(c, cx, cy, w, h, rot, k, dr, rad=22)


def node_graph(c, t, k_fail, cx=540, cy=1180, seed=5, n=26):
    """hub-and-spoke dependency map: a central 'cloud' node feeding many service nodes; k_fail turns it red and spreads."""
    import numpy as np
    pts = []
    for i in range(n):
        a = i / n * 6.283 + 0.3 * hsh(i, seed)
        r = 250 + 160 * hsh(i, seed + 1)
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.95))
    for i, (x, y) in enumerate(pts):
        d = math.hypot(x - cx, y - cy) / 410
        red = cl((k_fail * 1.6 - d))
        c.drawLine(cx, cy, x, y, stroke(lerp_col(LIGHT, RED, red), 4))
    for i, (x, y) in enumerate(pts):
        d = math.hypot(x - cx, y - cy) / 410
        red = cl((k_fail * 1.6 - d))
        c.drawCircle(x, y, 22, paint(lerp_col(INK, RED, red))); c.drawCircle(x, y, 22, stroke(PAPER, 4))
    pulse = 1 + 0.06 * math.sin(t * 6) * cl(k_fail * 3)
    c.drawCircle(cx, cy, 96 * pulse, paint(RED if k_fail > 0 else INK))
    c.drawCircle(cx, cy, 96 * pulse, stroke(PAPER, 8))
    cloud_icon(c, cx, cy + 6, 1.0, PAPER)


def lerp_col(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def cloud_icon(c, x, y, s, col=PAPER):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for (dx, dy, r) in ((-28, 6, 26), (0, -12, 34), (30, 4, 26)): p.addCircle(dx, dy, r)
    p.addRect(R.MakeXYWH(-54, 4, 108, 28))
    c.drawPath(p, paint(col)); c.restore()


def server(c, x, y, s, t, down=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(4):
        r = R.MakeXYWH(-90, -160 + i * 82, 180, 70)
        c.drawRRect(skia.RRect.MakeRectXY(r, 10, 10), paint((34, 34, 40)));
        on = down < 0.5 or (i % 2 == 0 and math.sin(t * 9 + i) > 0)
        c.drawCircle(60, -125 + i * 82, 9, paint(RED if down > 0.5 else GREEN, 1.0 if on else 0.25))
        for j in range(4): c.drawLine(-70, -140 + i * 82 + j * 12, 10, -140 + i * 82 + j * 12, stroke((80, 80, 90), 4))
    c.restore()


def domino(c, x, y, s, ang, col=INK):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    r = R.MakeXYWH(-30, -200, 60, 200)
    c.drawRRect(skia.RRect.MakeRectXY(r.makeOffset(10, 6), 10, 10), paint((0, 0, 0), 0.15, blur=8))
    c.drawRRect(skia.RRect.MakeRectXY(r, 10, 10), paint(col))
    c.drawCircle(0, -150, 9, paint(PAPER)); c.drawCircle(0, -50, 9, paint(PAPER))
    c.restore()


def bar_split(c, x, y, w, h, parts, k, t):
    """horizontal stacked bar: parts = [(label, frac, col)]."""
    xx = x
    for i, (lbl, fr, col) in enumerate(parts):
        kk = pr(k, i * 0.18, 0.4) if False else cl(k * len(parts) - i)
        ww = w * fr * eo(kk)
        c.drawRect(R.MakeXYWH(xx, y, ww, h), paint(col))
        if kk > 0.6 and lbl:
            text(c, lbl, xx + ww / 2, y + h + 56, 'b', 36, INK, 'c')
            mono(c, '%d%%' % round(fr * 100), xx + ww / 2, y + h / 2 + 10, 28, PAPER, 'c')
        xx += w * fr


# ------------------------------------------------------------------ added for ep 44
def donut(c, cx, cy, r, frac, k, col=GREEN, back=LIGHT, width=70, label=None):
    c.drawArc(R.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), 0, 360, False, stroke(back, width))
    sw = 360 * frac * eo(cl(k))
    if sw > 0: c.drawArc(R.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90, sw, False, stroke(col, width, cap=True) if False else stroke(col, width))
    if label: text(c, label, cx, cy + 50, 'blk', 150, INK, 'c')


def chair(c, x, y, s, light=1.0):
    """empty executive chair, side-lit."""
    c.save(); c.translate(x, y); c.scale(s, s)
    if light > 0:
        c.drawPath(poly([(-60, -900), (60, -900), (360, 40), (-360, 40)], True), paint(shader=lin(0, -900, 0, 40, [argb((255, 250, 230), 0.0), argb((255, 250, 230), 0.22 * light)])))
        c.drawOval(R.MakeXYWH(-300, 10, 600, 60), paint((0, 0, 0), 0.3, blur=12))
    back = skia.Path(); back.addRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-120, -520, 240, 300), 60, 60))
    c.drawPath(back, paint((28, 28, 32)))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-150, -230, 300, 70), 30, 30), paint((36, 36, 42)))
    for sx in (-1, 1):
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(sx * 150 - 20, -320, 40, 120), 16, 16), paint((40, 40, 46)))
    c.drawRect(R.MakeXYWH(-14, -160, 28, 110), paint((70, 70, 78)))
    for i in range(5):
        a = math.radians(-90 + i * 72)
        c.drawLine(0, -50, math.cos(a) * 140, -20 + math.sin(a) * 18, stroke((70, 70, 78), 14))
        c.drawCircle(math.cos(a) * 140, -10 + math.sin(a) * 18, 14, paint((20, 20, 24)))
    c.drawPath(back, stroke((255, 255, 255), 3, 0.15))
    c.restore()


def chip(c, x, y, s, t, glow=1.0, col=GREEN):
    c.save(); c.translate(x, y); c.scale(s, s)
    if glow > 0: c.drawCircle(0, 0, 260, paint(col, 0.18 * glow, blur=40))
    for i in range(9):
        o = -160 + i * 40
        for (x0, y0, x1, y1) in ((o, -200, o, -150), (o, 150, o, 200), (-200, o, -150, o), (150, o, 200, o)):
            c.drawLine(x0, y0, x1, y1, stroke((180, 160, 110), 10))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-160, -160, 320, 320), 26, 26), paint((26, 26, 30)))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-110, -110, 220, 220), 16, 16), paint(shader=lin(-110, -110, 110, 110, [argb((60, 60, 70)), argb((30, 30, 36))])))
    for i in range(4):
        for j in range(4):
            on = (int(t * 4) + i * 3 + j) % 5 != 0
            c.drawRect(R.MakeXYWH(-90 + i * 48, -90 + j * 48, 36, 36), paint(col if on else (60, 60, 70), 0.85 if on else 1))
    c.restore()


def bars(c, x, y, w, h, items, k, ymax=None):
    """vertical bars: items = [(label, value, value_label, col)]."""
    ymax = ymax or max(v for _, v, _, _ in items) * 1.08
    n = len(items); bw = w / n * 0.56
    for i, (lbl, v, vl, col) in enumerate(items):
        kk = cl(k * n - i * 0.6)
        bh = h * v / ymax * eo(kk)
        bx = x + w / n * (i + 0.5) - bw / 2
        c.drawRect(R.MakeXYWH(bx, y + h - max(bh, 4 * (kk > 0)), bw, max(bh, 4 * (kk > 0))), paint(col))
        if kk > 0.3:
            text(c, vl, bx + bw / 2, y + h - bh - 24, 'blk', 54, INK, 'c', a=cl(kk * 2 - 0.6))
        mono(c, lbl, bx + bw / 2, y + h + 46, 22, GREY, 'c')


def timeline(c, x0, x1, y, marks, k, t):
    """horizontal timeline with labelled dots; marks = [(frac, top_label, bottom_label)]."""
    c.drawLine(x0, y, x0 + (x1 - x0) * eo(cl(k)), y, stroke(INK, 6))
    for i, (fr, top, bot) in enumerate(marks):
        kk = cl(k * 1.4 - fr)
        if kk <= 0: continue
        x = x0 + (x1 - x0) * fr
        c.drawCircle(x, y, 18 * eback(cl(kk * 3), 1.8), paint(RED if i == len(marks) - 1 else INK))
        text(c, top, x, y - 44, 'blk', 54, INK, 'c', a=cl(kk * 3))
        mono(c, bot, x, y + 64, 22, GREY, 'c', a=cl(kk * 3))


def arrow(c, x, y, s, up=True, col=GREEN):
    c.save(); c.translate(x, y); c.scale(s, s if up else -s)
    c.drawPath(poly([(0, -60), (50, 0), (18, 0), (18, 60), (-18, 60), (-18, 0), (-50, 0)], True), paint(col))
    c.restore()


def crown(c, x, y, s, col=YEL):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = poly([(-120, 60), (-140, -60), (-70, 0), (0, -90), (70, 0), (140, -60), (120, 60)], True)
    c.drawPath(p, paint(col)); c.drawPath(p, stroke(INK, 8))
    for dx in (-140, 0, 140): c.drawCircle(dx, -70 if dx else -100, 16, paint(col)); c.drawCircle(dx, -70 if dx else -100, 16, stroke(INK, 6))
    c.restore()
