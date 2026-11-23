"""ESSAY look (owner reference 23 Nov 2026): editorial magazine slides.
Cream paper with 4 faint accent-coloured vertical grid lines, tiny tracked label 'N° 01 - ESSAY' + page counter,
heavy condensed caps headlines (Anton) with ONE word on an accent highlight block, Inter body text,
engraved/hatched illustrations, and DARK slides in between (near-black, cream text) for rhythm.
Accent colour is per video (purple here). Ends on a full-accent slide."""
import os
os.environ.setdefault('OMB_THEME', 'flat')
import sys
sys.path.insert(0, '/home/claude/studio')
from info_lib import *   # P, S, pr, eo, eio, eback, pop, rr, path, Timing, font (Inter), W, H, FPS
import info_lib as _il

CREAM = (236, 229, 216); DARK = (24, 23, 22); INKE = (20, 20, 20); MUTE = (150, 142, 132); CREAM_T = (236, 229, 216)
ACC = [(138, 66, 214)]          # accent, set per video
ANTON = '/home/claude/studio/fonts/ttf/Anton.ttf'
_AT = [None]


def anton(size):
    if _AT[0] is None: _AT[0] = skia.Typeface.MakeFromFile(ANTON)
    f = skia.Font(_AT[0], size); f.setEdging(skia.Font.Edging.kAntiAlias); return f


def acc(): return ACC[0]


_GRAIN = {}


def page(c, dark=False, label='N° 01 — ESSAY', num=None, prog=None, fill=None):
    """background + grid lines + header. fill overrides the background colour (full-accent slide)."""
    bg = fill or (DARK if dark else CREAM)
    c.drawRect(skia.Rect.MakeWH(W, H), P(bg))
    key = (dark, fill is not None)
    if key not in _GRAIN:
        rnd = np.random.default_rng(3); n = rnd.normal(0, 1, (H, W)) * (5 if not dark else 3)
        img = np.clip(np.array(bg, np.float32)[None, None, :] + n[..., None], 0, 255).astype(np.uint8)
        _GRAIN[key] = skia.Image.fromarray(np.ascontiguousarray(np.dstack([img, np.full((H, W), 255, np.uint8)])), colorType=skia.kRGBA_8888_ColorType)
    c.drawImage(_GRAIN[key], 0, 0)
    gl = WHITE if fill else acc()
    for x in (150, 418, 686, 930): c.drawLine(x, 0, x, H, S(gl, 1.6, 0.35 if not dark else 0.45))
    tc = (CREAM_T if (dark or fill) else INKE)
    f = font(26, 'Medium', False); sp = 5.0
    def tracked(s, x, y, align='l'):
        tw = sum(f.measureText(ch) + sp for ch in s) - sp; xx = x if align == 'l' else x - tw
        for ch in s: c.drawString(ch, xx, y, f, P(tc, 0.75)); xx += f.measureText(ch) + sp
    tracked(label, 80, 300)
    if num: tracked(num, 1000, 300, 'r')
    if prog is not None:
        c.drawLine(80, 330, 1000, 330, S(tc, 3, 0.15)); c.drawLine(80, 330, 80 + 920 * cl(prog), 330, S(tc, 3, 0.85))


def headline(c, lines, x=150, y=520, size=130, k=1.0, dark=False, gap=1.02, maxw=880):
    """lines: list of [(text, hl)] segments per line; hl=True -> cream text on accent block. Left aligned at x."""
    tc = CREAM_T if dark else INKE
    yy = y
    for li, segs in enumerate(lines):
        kk = eo(cl(k * 1.6 - li * 0.25))
        if kk <= 0: yy += size * gap; continue
        f = anton(size); tw = sum(f.measureText(s) for s, h in segs) + f.measureText(' ') * (len(segs) - 1)
        ff = f
        if tw > maxw: ff = anton(size * maxw / tw)
        xx = x; c.save(); c.translate(0, 30 * (1 - kk))
        for s, hl in segs:
            w = ff.measureText(s)
            if hl:
                c.drawRect(skia.Rect.MakeXYWH(xx - 12, yy - ff.getSize() * 0.86, (w + 24) * min(1, kk * 1.3), ff.getSize() * 1.0), P(acc()))
                c.drawString(s, xx, yy, ff, P(CREAM_T, kk))
            else:
                c.drawString(s, xx, yy, ff, P(tc if hl is not None else MUTE, kk))
            xx += w + ff.measureText(' ')
        c.restore(); yy += ff.getSize() * gap
    return yy


def body(c, s, x, y, size=40, col=None, w='Regular', a=1.0, italic=False):
    f = font(size, w, False); c.drawString(s, x, y, f, P(col or INKE, a)); return f.measureText(s)


# ------------------------------------------------------------------ engraved cow (side view), hatched
def cow(c, x, y, s=1.0, flip=False, col=None, hatch=True, a=1.0, head_down=0.0, seed=0):
    """engraved Holstein-ish cow, side view: boxy body, hip bump, long head, ears + horns, udder, hooves, tufted tail, patches."""
    purple = col is not None and col != MUTE
    col = col or (248, 244, 234)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    c.drawOval(skia.Rect.MakeXYWH(-130, 112, 270, 26), P(INKE, 0.16 * a))
    legs = [rr(lx - 10, 18, 20, 100, 6) for lx in (-96, -72, 66, 90)]
    for l in legs:
        c.drawRRect(l, P(col, a)); c.drawRRect(l, S(INKE, 3, a))
        c.drawRect(skia.Rect.MakeXYWH(l.rect().left() - 1, 106, 22, 12), P(INKE, a))
    body = skia.Path(); body.moveTo(-118, -46); body.lineTo(-100, -70); body.cubicTo(-80, -66, -40, -60, 0, -62)
    body.cubicTo(40, -64, 80, -66, 104, -62); body.lineTo(118, -50); body.cubicTo(124, -10, 118, 18, 104, 30)
    body.cubicTo(60, 40, -40, 40, -100, 34); body.cubicTo(-122, 20, -126, -20, -118, -46); body.close()
    c.drawPath(body, P(col, a))
    hd = head_down; hx, hy = 116, -56 + 46 * hd
    head = skia.Path(); head.moveTo(hx - 10, hy - 8); head.cubicTo(hx + 10, hy - 24, hx + 30, hy - 20, hx + 44, hy - 10)
    head.lineTo(hx + 78, hy + 30); head.cubicTo(hx + 84, hy + 44, hx + 70, hy + 56, hx + 56, hy + 52)
    head.cubicTo(hx + 30, hy + 44, hx + 4, hy + 30, hx - 10, hy + 22); head.close()
    c.drawPath(head, P(col, a))
    clip = skia.Path(body); clip.addPath(head)
    c.save(); c.clipPath(clip, doAntiAlias=True)
    if not purple:
        rnd = random.Random(seed)
        for i in range(3):   # patches
            px, py = rnd.uniform(-90, 80), rnd.uniform(-50, 20); pw, ph_ = rnd.uniform(40, 80), rnd.uniform(26, 50)
            pp = skia.Path(); pp.moveTo(px, py)
            for j in range(7):
                ang = j * 2 * math.pi / 7; rr_ = 1 + rnd.uniform(-0.3, 0.25)
                pp.lineTo(px + pw / 2 * rr_ * math.cos(ang), py + ph_ / 2 * rr_ * math.sin(ang))
            pp.close(); c.drawPath(pp, P((52, 50, 48), 0.9 * a))
        c.drawPath(skia.Path.Rect(skia.Rect.MakeXYWH(hx + 20, hy - 30, 80, 90)) if False else skia.Path(), P(INKE))
    if hatch:
        for i in range(-220, 280, 8): c.drawLine(i, -10, i - 50, 60, S(INKE, 1.3, 0.4 * a))   # belly shading
        for i in range(-220, 280, 12): c.drawLine(i, -80, i + 30, -40, S(INKE, 1.0, 0.18 * a))
    c.restore()
    c.drawPath(body, S(INKE, 3.2, a)); c.drawPath(head, S(INKE, 3.2, a))
    c.drawLine(-60, -60, -62, -10, S(INKE, 1.5, 0.35 * a)); c.drawLine(70, -62, 74, -14, S(INKE, 1.5, 0.35 * a))   # hip / shoulder lines
    ud = skia.Path(); ud.addOval(skia.Rect.MakeXYWH(-52, 26, 40, 22)); c.drawPath(ud, P((230, 180, 180) if not purple else col, a)); c.drawPath(ud, S(INKE, 2.5, a))
    c.drawPath(skia.Path(), P(INKE))
    ear = skia.Path(); ear.moveTo(hx + 2, hy - 2); ear.cubicTo(hx - 20, hy - 6, hx - 30, hy + 8, hx - 18, hy + 14); ear.close(); c.drawPath(ear, P(col, a)); c.drawPath(ear, S(INKE, 2.5, a))
    hn = skia.Path(); hn.moveTo(hx + 14, hy - 14); hn.cubicTo(hx + 8, hy - 34, hx - 4, hy - 42, hx - 16, hy - 40); c.drawPath(hn, S(INKE, 6, a)); c.drawPath(hn, S((240, 236, 226), 3, a))
    c.drawCircle(hx + 34, hy + 4, 4.5, P(INKE, a))
    mz = skia.Path(); mz.addOval(skia.Rect.MakeXYWH(hx + 56, hy + 28, 30, 26)); c.drawPath(mz, P((60, 56, 54) if not purple else tuple(max(0, v - 50) for v in col), a))
    t_ = skia.Path(); t_.moveTo(-118, -40); t_.cubicTo(-136, -10, -132, 40, -130, 80); c.drawPath(t_, S(INKE, 3, a))
    tf = skia.Path(); tf.moveTo(-130, 76); tf.lineTo(-140, 100); tf.lineTo(-122, 100); tf.close(); c.drawPath(tf, P(INKE, a))
    c.restore()


def herd(c, seed=7, purple_at=None, t=0.0, fade=0.0, y0=760, y1=1380, n_rows=6, grey_purple=False, sway=True):
    """field of cows; purple_at = (row, col) index for the purple one. fade -> 1 makes the herd ghostly."""
    rnd = random.Random(seed); out = None
    for r in range(n_rows):
        yy = y0 + (y1 - y0) * r / (n_rows - 1); sc = 0.5 + 0.36 * r / (n_rows - 1)
        cols = 4 if r % 2 == 0 else 3
        for k in range(cols):
            xx = 140 + (k + (0.5 if r % 2 else 0)) * 800 / 3 + rnd.uniform(-40, 40)
            fl = rnd.random() < 0.5; dy = rnd.uniform(-20, 20)
            hd = (0.5 + 0.5 * math.sin(t * 1.5 + k + r)) if sway else 0.0
            if purple_at == (r, k):
                out = (xx, yy + dy, sc, fl)
                cow(c, xx, yy + dy, sc, fl, MUTE if grey_purple else acc(), True, 1.0, hd * 0.4)
            else:
                cow(c, xx, yy + dy, sc, fl, None, True, 1.0 - 0.7 * fade, hd * 0.4, seed=r * 10 + k)
    return out


def eye(c, x, y, r=34, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(eback(cl(k)), eback(cl(k)))
    p = skia.Path(); p.moveTo(-r, 0); p.quadTo(0, -r * 0.9, r, 0); p.quadTo(0, r * 0.9, -r, 0); p.close()
    c.drawPath(p, P(CREAM)); c.drawPath(p, S(INKE, 3)); c.drawCircle(0, 0, r * 0.38, P(acc())); c.drawCircle(0, 0, r * 0.16, P(INKE)); c.restore()


def dotted(c, x0, y0, x1, y1, k, col=None):
    if k <= 0: return
    col = col or acc(); ex, ey = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5); p.setColor4f(C(col)); p.setStrokeCap(skia.Paint.kRound_Cap)
    p.setPathEffect(skia.DashPathEffect.Make([2, 14], 0)); c.drawLine(x0, y0, ex, ey, p)
    if k > 0.97:
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6): c.drawLine(ex, ey, ex + 26 * math.cos(a + da), ey + 26 * math.sin(a + da), S(col, 5))


def esubs(c, T, t, dark=False, y=1440):
    for ch in T.CH:
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.15:
            f = font(40, 'SemiBold', False); sp = f.measureText(' ')
            tw = sum(f.measureText(w) for w, a, b in ch) + sp * (len(ch) - 1); x = 540 - tw / 2
            bg, fg = ((40, 38, 36), CREAM_T) if dark else (CREAM, INKE)
            c.drawRRect(rr(x - 26, y - 46, tw + 52, 66, 33), P(bg, 0.95)); c.drawRRect(rr(x - 26, y - 46, tw + 52, 66, 33), S(acc(), 2.5, 0.8))
            for w, a, b in ch:
                on = a - 0.03 <= t <= b + 0.08
                c.drawString(w, x, y, f, P(acc() if on else fg)); x += f.measureText(w) + sp
            return
