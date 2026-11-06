"""Whiteboard / marker kit for OopsMyBusiness (owner, 6 Nov 2026: "whiteboard + chalkboard style, white background, better font").
Use in anim_shots.py after `from nbnkit import *`:  `from nbnkit.board import *`.  Everything is drawn on with a marker pen:
ink() write-on strokes with the pen at the tip, hatch() marker fills, mtext() handwritten type (Permanent Marker 'pm', Kalam 'kb'/'kr'),
say() = board two-tier caption, board_bg() = the white board, plus marker props (gauge, car, pie, card, house, calendar, stamp, month strip,
report, browser, heads row). First used: HOW IT WORKS EP 2 (credit score), examples/credit-board."""
import math
import numpy as np, skia
from nbnkit import *        # noqa
from nbnkit import _rot_stick   # noqa
W, H = 1080, 1920
# ---------------------------------------------------------------- marker palette (on a white board)
BOARD = (251, 251, 249); MK = (26, 30, 42); BLU = (30, 96, 220); RD = (224, 50, 46); GR = (22, 152, 86); OR = (244, 132, 28); PU = (126, 74, 206)
GHOST = (226, 230, 236)
SL_COLS = [BLU, GR, PU, RD, OR]; SL_VALS = [10, 10, 15, 35, 30]; SL_NAMES = ["NEW CREDIT", "MIX", "HISTORY", "ON TIME", "OWED"]


def _rng(seed): return np.random.default_rng(abs(int(seed * 9973)) % (2 ** 31))


def wob(pts, seed=1, amp=2.2, step=26):
    """resample a polyline and add a small hand wobble (deterministic)"""
    out = []; r = _rng(seed)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(1, int(d / step))
        for i in range(n):
            k = i / n; out.append((x0 + (x1 - x0) * k, y0 + (y1 - y0) * k))
    out.append(pts[-1])
    noise = r.normal(0, amp, (len(out), 2)); noise = np.cumsum(noise, 0) * 0.35; noise -= np.linspace(noise[0], noise[-1], len(out))
    return [(x + nx, y + ny) for (x, y), (nx, ny) in zip(out, noise)]


def circ_pts(cx, cy, r, a0=-90, a1=270, n=64, ry=None):
    ry = ry or r
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _path(pts):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    return p


def ink(c, polys, prog, col=MK, w=9, a=1.0, pen_=True):
    """draw a list of polylines on, in order, by total length; returns the pen tip (or None when done)"""
    if prog <= 0: return None
    paths = [_path(p) for p in polys]; lens = [skia.PathMeasure(p, False).getLength() for p in paths]; tot = sum(lens) or 1
    left = prog * tot; tip = None
    for p, L in zip(paths, lens):
        if left <= 0: break
        pa = stroke(col, w, a)
        if left < L:
            eff = skia.TrimPathEffect.Make(0.0, float(max(1e-4, min(0.9999, left / L))))
            if eff is not None: pa.setPathEffect(eff); c.drawPath(p, pa)
            pos, tan = skia.PathMeasure(p, False).getPosTan(left); tip = (pos.x(), pos.y())
        else:
            c.drawPath(p, pa)
        left -= L
    if pen_ and tip is not None and prog < 1: pen(c, *tip)
    return tip


def pen(c, x, y, col=BLU):
    """the marker pen at the stroke tip (barrel up-right, like a hand drawing)"""
    c.save(); c.translate(x, y); c.rotate(-38)
    c.drawRoundRect(R.MakeXYWH(-4, -150, 34, 120), 10, 10, paint((0, 0, 0), 0.18, blur=8))
    c.drawPath(poly([(-7, -2), (7, -2), (13, -30), (-13, -30)], True), paint((40, 40, 46)))
    c.drawRoundRect(R.MakeXYWH(-17, -150, 34, 122), 9, 9, paint((246, 246, 248))); c.drawRoundRect(R.MakeXYWH(-17, -150, 34, 122), 9, 9, stroke(MK, 3))
    c.drawRoundRect(R.MakeXYWH(-18, -112, 36, 40), 6, 6, paint(col))
    c.restore()


def hatch(c, clip, prog, col, gap=17, w=7, ang=-35, bbox=(0, 0, W, H), seed=3, a=0.85):
    """marker hatch fill inside a clip path, laid down stroke by stroke"""
    if prog <= 0: return
    x0, y0, x1, y1 = bbox; c.save(); c.clipPath(clip, doAntiAlias=True)
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang)); L = (x1 - x0) + (y1 - y0)
    lines = []; d = -L
    while d < L:
        cx, cy = (x0 + x1) / 2 + d * sa, (y0 + y1) / 2 - d * ca
        lines.append([(cx - ca * L, cy - sa * L), (cx + ca * L, cy + sa * L)]); d += gap
    n = int(len(lines) * prog + 0.999); r = _rng(seed)
    for i, ln in enumerate(lines[:n]):
        jx = r.normal(0, 1.2); c.drawPath(_path([(ln[0][0] + jx, ln[0][1]), (ln[1][0] - jx, ln[1][1])]), stroke(col, w, a))
    c.restore()


def mtext(c, s, x, y, size=80, col=MK, prog=1.0, key="pm", align="c", pen_=False, a=1.0):
    """handwritten text revealed left to right (write-on)"""
    if prog <= 0 or not s: return
    f = font(key, size); w = f.measureText(s); xs = x - w / 2 if align == "c" else x
    c.save(); c.clipRect(R.MakeLTRB(xs - 10, y - size * 1.3, xs - 10 + (w + 20) * min(1, prog), y + size * 0.5))
    c.drawString(s, xs, y, f, paint(col, a)); c.restore()
    if pen_ and prog < 1: pen(c, xs + w * prog, y - size * 0.3)


def tw(f, s): return f.measureText(s)


# ---------------------------------------------------------------- the board + two-tier marker captions
def board_bg(c, t, seed=0):
    c.clear(skia.Color(*BOARD))
    c.drawRect(R.MakeXYWH(0, 0, W, H), paint((214, 220, 232), 1.0, shader=None) if False else paint(BOARD))
    # soft studio light + edges, and the erased-marker ghosts every real whiteboard has
    c.drawCircle(W / 2, H * 0.42, 900, paint((255, 255, 255), 0.9, blur=160))
    for i, (gx, gy, gr) in enumerate(((160, 520, 120), (920, 1260, 150), (240, 1620, 110), (880, 420, 90))):
        r = _rng(seed + i)
        pts = [(gx + gr * math.cos(a_) * (0.7 + 0.3 * r.random()), gy + gr * 0.5 * math.sin(a_)) for a_ in np.linspace(0, 5.2, 14)]
        c.drawPath(_path(pts), stroke(GHOST, 10, 0.55))
    c.drawRect(R.MakeXYWH(0, 0, W, H), paint((120, 130, 150), 0.10, blur=0) if False else paint((0, 0, 0), 0.0))
    edge = skia.GradientShader.MakeRadial(skia.Point(W / 2, H * 0.48), H * 0.75, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0.35, 0.38, 0.45, 0.16)], [0.6, 1.0])
    pe = skia.Paint(); pe.setShader(edge); c.drawRect(R.MakeXYWH(0, 0, W, H), pe)


def say(c, t, t0, small, big, col=MK, t1=None, size=170, y=640, smallc=BLU, under=None):
    """board two-tier: a small Kalam line written on, then ONE big Permanent Marker word written on; optional marker underline"""
    if t < t0 or (t1 is not None and t > t1): return
    fb = font("pm", size); wb = tw(fb, big)
    if wb > 860: size *= 860 / wb; fb = font("pm", size); wb = tw(fb, big)
    k1 = pr(t, t0, 0.32); k2 = pr(t, t0 + 0.14, max(0.28, 0.035 * len(big)))
    if small: mtext(c, small, W / 2, y - size * 0.98, 52, smallc, k1, "kb")
    mtext(c, big, W / 2, y, size, col, k2, "pm")
    if under is not None and k2 >= 1:
        ku = pr(t, t0 + 0.14 + max(0.28, 0.035 * len(big)), 0.25)
        ink(c, [wob([(W / 2 - wb / 2, y + 26), (W / 2 + wb / 2, y + 20)], seed=len(big), amp=1.4)], ku, under, 10, pen_=False)


def note(c, t, t0, text, t1=None, y=1478):
    if t < t0 or (t1 is not None and t > t1): return
    src_chip(c, text, min(1, pr(t, t0, 0.25)), y=y)


def floor_line(c, t, t0, y=FLOOR, x0=90, x1=990):
    ink(c, [wob([(x0, y + 4), (x1, y)], seed=7, amp=1.2)], pr(t, t0, 0.35), MK, 6, pen_=False)


def pop_(t, t0, d=0.3, s=1.7): return eback(pr(t, t0, d), s) if t >= t0 else 0.0


# ---------------------------------------------------------------- marker props
def gauge_m(c, x, y, r, t, t0, frac=0.8, col_n=MK):
    segs = [(RD, 180, 240), (OR, 240, 300), (GR, 300, 360)]
    for i, (col, a0, a1) in enumerate(segs):
        ink(c, [wob(circ_pts(x, y, r, a0, a1, 24), seed=i + 1, amp=1.0)], pr(t, t0 + i * 0.22, 0.25), col, 26, pen_=True)
    k = pr(t, t0 + 0.75, 0.3)
    if k > 0:
        mtext(c, "300", x - r, y + 64, 40, MK, k, "kb"); mtext(c, "850", x + r, y + 64, 40, MK, k, "kb")
        ang = math.radians(180 + 180 * frac * eo(k) + 3 * math.sin(t * 3))
        ink(c, [[(x, y), (x + (r - 34) * math.cos(ang), y + (r - 34) * math.sin(ang))]], 1, col_n, 10, pen_=False)
        c.drawCircle(x, y, 16, paint(MK))


def payslip(c, x, y, k=1.0, tilt=-6, label="SALARY"):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRect(R.MakeXYWH(-150, -95, 300, 190), paint((0, 0, 0), 0.10, blur=8)); c.drawRect(R.MakeXYWH(-150, -95, 300, 190), paint(WHITE))
    c.drawPath(_path(wob([(-150, -95), (150, -95), (150, 95), (-150, 95), (-150, -95)], seed=5, amp=1)), stroke(MK, 5))
    mtext(c, label, 0, -38, 46, GR, 1, "pm"); mtext(c, "$ $ $", 0, 30, 54, GR, 1, "pm")
    c.restore()


def car_m(c, x, y, w, t, t0, col=BLU):
    s = w / 520
    body = [(-250, 0), (-250, -70), (-170, -82), (-110, -150), (90, -150), (160, -84), (250, -64), (256, 0), (-250, 0)]
    win = [(-96, -88), (-66, -132), (10, -132), (10, -88), (-96, -88)]; win2 = [(30, -88), (30, -132), (80, -132), (122, -88), (30, -88)]
    sc = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    k = pr(t, t0, 0.8)
    if k >= 0.6:
        cp = _path(sc(body)); hatch(c, cp, pr(t, t0 + 0.5, 0.4), col, gap=19, w=6, bbox=(x - 260 * s, y - 160 * s, x + 260 * s, y), a=0.55)
    ink(c, [wob(sc(body), seed=11, amp=1.3), wob(sc(win), 12, 0.8), wob(sc(win2), 13, 0.8)], k, MK, 7)
    kw = pr(t, t0 + 0.6, 0.3)
    for wx in (-140, 150):
        if kw > 0:
            c.drawCircle(x + wx * s, y, 44 * s * eo(kw), paint(BOARD)); ink(c, [circ_pts(x + wx * s, y, 44 * s, 0, 360, 28)], kw, MK, 8, pen_=False)
            c.drawCircle(x + wx * s, y, 14 * s * eo(kw), paint(MK))


def cross(c, x0, y0, x1, y1, prog, col=RD, w=12, seed=1):
    ink(c, [wob([(x0, y0), (x1, y1)], seed, 1.5)], prog, col, w, pen_=False)


def boxed(c, x, y, wbox, hbox, prog, col=MK, seed=2, w=6):
    ink(c, [wob([(x - wbox / 2, y - hbox / 2), (x + wbox / 2, y - hbox / 2), (x + wbox / 2, y + hbox / 2), (x - wbox / 2, y + hbox / 2), (x - wbox / 2, y - hbox / 2)], seed, 1.2)], prog, col, w, pen_=False)


def arrow_m(c, a, b, prog, col=MK, w=9, seed=4, bend=0.0):
    mx, my = (a[0] + b[0]) / 2 - bend * (b[1] - a[1]), (a[1] + b[1]) / 2 + bend * (b[0] - a[0])
    pts = [(a[0] + (mx - a[0]) * 2 * u * (1 - u) * 1 + 0, 0) for u in ()]  # placeholder (kept simple below)
    pts = [((1 - u) ** 2 * a[0] + 2 * u * (1 - u) * mx + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * u * (1 - u) * my + u * u * b[1]) for u in np.linspace(0, 1, 24)]
    ink(c, [pts], min(1, prog * 1.25), col, w, pen_=False)
    if prog >= 0.8:
        ang = math.atan2(b[1] - pts[-3][1], b[0] - pts[-3][0]); hl = 34
        hp = [(b[0] - hl * math.cos(ang - 0.5), b[1] - hl * math.sin(ang - 0.5)), b, (b[0] - hl * math.cos(ang + 0.5), b[1] - hl * math.sin(ang + 0.5))]
        ink(c, [hp], pr(prog, 0.8, 0.2), col, w, pen_=False)


def pie_m(c, cx, cy, r, t, t_out, slices, hl=None, labels=True, qmarks=False):
    """slices: list of (index, t_start) — each slice hatches in from its time. t_out: when the outline is drawn."""
    ink(c, [wob(circ_pts(cx, cy, r, -90, 270, 72), seed=21, amp=1.4)], pr(t, t_out, 0.7), MK, 9)
    acc = 0
    for i, v in enumerate(SL_VALS):
        a0 = -90 + 360 * acc / 100; a1 = -90 + 360 * (acc + v) / 100; acc += v
        st = dict(slices).get(i)
        if st is not None and t >= st:
            off = 26 * eo(pr(t, st, 0.3)) if hl == i else 0
            am = math.radians((a0 + a1) / 2); ox, oy = off * math.cos(am), off * math.sin(am)
            wedge = skia.Path(); wedge.moveTo(cx + ox, cy + oy); wedge.arcTo(R.MakeXYWH(cx + ox - r, cy + oy - r, 2 * r, 2 * r), a0, a1 - a0, False); wedge.close()
            hatch(c, wedge, pr(t, st + 0.15, 0.55), SL_COLS[i], gap=15, w=8, bbox=(cx - r - 40, cy - r - 40, cx + r + 40, cy + r + 40), seed=i + 3, a=0.8)
            edge = [(cx + ox, cy + oy), (cx + ox + r * math.cos(math.radians(a0)), cy + oy + r * math.sin(math.radians(a0)))]
            edge2 = [(cx + ox, cy + oy), (cx + ox + r * math.cos(math.radians(a1)), cy + oy + r * math.sin(math.radians(a1)))]
            ink(c, [edge, edge2], pr(t, st, 0.25), MK, 7, pen_=False)
            if hl == i: ink(c, [wob(circ_pts(cx + ox, cy + oy, r, a0, a1, 20), seed=i + 30, amp=0.8)], pr(t, st, 0.3), SL_COLS[i], 14, pen_=False)
            if labels:
                lr = r * (0.62 if v >= 15 else 0.66); lx, ly = cx + ox + lr * math.cos(am), cy + oy + lr * math.sin(am)
                kk = pr(t, st + 0.5, 0.3)
                if kk > 0:
                    c.drawCircle(lx, ly - 18, 52 if v < 15 else 64, paint(BOARD, 0.92 * kk))
                    mtext(c, f"{v}%", lx, ly, 52 if v < 15 else 64, SL_COLS[i], kk, "pm")
        elif qmarks:
            am = math.radians((a0 + a1) / 2); lx, ly = cx + r * 0.62 * math.cos(am), cy + r * 0.62 * math.sin(am)
            edge = [(cx, cy), (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))]
            pa = stroke(MK, 5, 0.6); pa.setPathEffect(skia.DashPathEffect.Make([18, 14], 0))
            if t > t_out + 0.6: c.drawPath(_path(edge), pa)
            kq = pop_(t, t_out + 0.7 + i * 0.16)
            if kq > 0:
                c.save(); c.translate(lx, ly - 20); c.scale(kq, kq); mtext(c, "?", 0, 30, 84, RD if i == 4 else MK, 1, "pm"); c.restore()


def card_m(c, x, y, w=210, k=1.0, col=BLU, tilt=0):
    if k <= 0: return
    h = w * 0.62; c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k, k)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18, paint(WHITE))
    cp = skia.Path(); cp.addRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18); hatch(c, cp, 1, col, gap=16, w=6, bbox=(-w / 2, -h / 2, w / 2, h / 2), a=0.45)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18, stroke(MK, 6))
    c.drawRect(R.MakeXYWH(-w / 2, -h / 2 + h * 0.2, w, h * 0.16), paint(MK)); c.drawRoundRect(R.MakeXYWH(-w / 2 + 22, h * 0.08, w * 0.24, h * 0.2), 5, 5, paint((250, 200, 60)))
    c.restore()


def house_m(c, x, y, s, t, t0, col=GR):
    pts = [(-110, 0), (-110, -120), (0, -200), (110, -120), (110, 0), (-110, 0)]; door = [(-26, 0), (-26, -70), (26, -70), (26, 0)]
    sc = lambda P: [(x + px * s, y + py * s) for px, py in P]
    cp = _path(sc(pts)); hatch(c, cp, pr(t, t0 + 0.4, 0.4), col, gap=18, w=6, bbox=(x - 120 * s, y - 210 * s, x + 120 * s, y), a=0.5)
    ink(c, [wob(sc(pts), 41, 1.0), wob(sc(door), 42, 0.6)], pr(t, t0, 0.55), MK, 7)


def calendar_m(c, x, y, t, t0, marks):
    cw, ch, cols, rows = 104, 92, 7, 4; x0, y0 = x - cw * cols / 2, y - ch * rows / 2
    grid = [[(x0, y0), (x0 + cw * cols, y0), (x0 + cw * cols, y0 + ch * rows), (x0, y0 + ch * rows), (x0, y0)]]
    grid += [[(x0 + cw * i, y0), (x0 + cw * i, y0 + ch * rows)] for i in range(1, cols)] + [[(x0, y0 + ch * j), (x0 + cw * cols, y0 + ch * j)] for j in range(1, rows)]
    ink(c, [wob(g, i + 50, 0.6) for i, g in enumerate(grid)], pr(t, t0, 0.8), MK, 5)
    for n, (kind, tm) in enumerate(marks):
        if kind is None or t < tm: continue
        i, j = n % cols, n // cols; cx, cy = x0 + cw * (i + 0.5), y0 + ch * (j + 0.5); k = pr(t, tm, 0.18)
        if kind == "ok": ink(c, [[(cx - 22, cy), (cx - 6, cy + 18), (cx + 26, cy - 22)]], k, GR, 8, pen_=False)
        else: ink(c, [[(cx - 24, cy - 24), (cx + 24, cy + 24)], [(cx + 24, cy - 24), (cx - 24, cy + 24)]], k, RD, 10, pen_=False)


def stamp_m(c, x, y, text, k, col=RD, tilt=-9, size=70):
    if k <= 0: return
    f = font("pm", size); w = tw(f, text) + 60; h = size * 1.45
    c.save(); c.translate(x, y); c.rotate(tilt); s = 1 + 0.6 * (1 - eback(min(1, k), 2.4)); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, paint(WHITE, 0.92)); c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, stroke(col, 9))
    c.drawString(text, -tw(f, text) / 2, size * 0.36, f, paint(col)); c.restore()


def month_strip(c, y, t, t0, stmt_k=0.0, pay_x=None, bar=None, bar_col=RD, bar_label=None):
    x0, x1 = 120, 960
    ink(c, [wob([(x0, y), (x1, y)], 61, 1.0)], pr(t, t0, 0.5), MK, 8)
    k = pr(t, t0 + 0.3, 0.3)
    if k > 0:
        mtext(c, "DAY 1", x0 + 20, y + 70, 40, MK, k, "kb"); mtext(c, "DAY 30", x1 - 40, y + 70, 40, MK, k, "kb")
        for i in range(0, 31, 5): ink(c, [[(x0 + (x1 - x0) * i / 30, y - 14), (x0 + (x1 - x0) * i / 30, y + 14)]], k, MK, 5, pen_=False)
    sx = x0 + (x1 - x0) * 25 / 30
    if stmt_k > 0:   # the statement date: where the balance is reported
        ink(c, [[(sx, y), (sx, y - 230)]], stmt_k, RD, 8, pen_=False)
        if stmt_k >= 1:
            c.drawPath(poly([(sx, y - 230), (sx + 150, y - 205), (sx, y - 180)], True), paint(RD, 0.9))
        mtext(c, "STATEMENT ENDS", sx, y - 262, 40, RD, pr(stmt_k, 0.6, 0.4), "kb")
    if pay_x is not None:
        px = x0 + (x1 - x0) * pay_x / 30
        c.drawPath(_path([(px, y), (px, y - 140)]), stroke(GR, 8)); c.drawPath(poly([(px, y - 140), (px - 120, y - 120), (px, y - 100)], True), paint(GR, 0.9))
        mtext(c, "YOU PAY", px - 30, y - 162, 40, GR, 1, "kb")
    if bar is not None:   # the balance that gets reported
        bw = 660 * bar; bx = 540 - 330
        c.drawRect(R.MakeXYWH(bx, y + 170, bw, 80), paint(bar_col, 0.85)); boxed(c, 540, y + 210, 660, 80, 1, MK, 70, 6)
        if bar_label: mtext(c, bar_label, 540, y + 320, 46, bar_col, 1, "kb")


def report_m(c, x, y, t, t0, rows, err=None, wq=False):
    w, h = 520, 640
    c.save(); c.translate(x, y); c.rotate(-2)
    k = pr(t, t0, 0.6)
    c.drawRect(R.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), paint((0, 0, 0), 0.10 * k, blur=10)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 81, 1.2)], k, MK, 7)
    mtext(c, "CREDIT REPORT", 0, -h / 2 + 80, 50, MK, pr(t, t0 + 0.4, 0.4), "pm")
    for i, (label, ok, tm) in enumerate(rows):
        yy = -h / 2 + 180 + i * 104; kk = pr(t, tm, 0.35)
        mtext(c, label, -w / 2 + 50, yy, 46, MK if ok else RD, kk, "kb", align="l")
        if kk >= 1:
            kx = pr(t, tm + 0.35, 0.2)
            if ok: ink(c, [[(w / 2 - 110, yy - 16), (w / 2 - 92, yy + 2), (w / 2 - 56, yy - 36)]], kx, GR, 9, pen_=False)
            else: ink(c, [[(w / 2 - 110, yy - 40), (w / 2 - 60, yy + 6)], [(w / 2 - 60, yy - 40), (w / 2 - 110, yy + 6)]], kx, RD, 10, pen_=False)
    if err is not None:
        ke = pr(t, err, 0.45); yy = -h / 2 + 180 + 1 * 104 - 16
        ink(c, [wob(circ_pts(0, yy, 240, -160, 210, 40, ry=56), 88, 1.6)], ke, RD, 9, pen_=False)
    c.restore()
    if wq:
        kq = pop_(t, wq)
        if kq > 0:
            c.save(); c.translate(x + 250, y - 250); c.scale(kq, kq); mtext(c, "?", 0, 50, 200, RD, 1, "pm"); c.restore()


def browser_m(c, x, y, t, t0):
    w, h = 760, 470
    k = pr(t, t0, 0.7)
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 91, 1.4),
            wob([(x - w / 2, y - h / 2 + 70), (x + w / 2, y - h / 2 + 70)], 92, 0.8)], k, MK, 8)
    if k >= 1:
        for i, col in enumerate((RD, OR, GR)): c.drawCircle(x - w / 2 + 40 + i * 36, y - h / 2 + 35, 11, paint(col))
        c.drawRoundRect(R.MakeXYWH(x - w / 2 + 150, y - h / 2 + 14, w - 190, 42), 21, 21, stroke(MK, 4))
        mtext(c, "AnnualCreditReport.com", x + 50, y - h / 2 + 47, 34, BLU, pr(t, t0 + 0.7, 0.6), "kb")
        mtext(c, "YOUR REPORT", x, y + 30, 64, MK, pr(t, t0 + 1.0, 0.4), "pm")
        for i in range(3): ink(c, [[(x - 230, y + 90 + i * 40), (x + 230 - i * 70, y + 90 + i * 40)]], pr(t, t0 + 1.2 + i * 0.1, 0.25), (150, 156, 170), 8, pen_=False)


def heads_row(c, y, t, t0, hl_t):
    for i in range(5):
        x = 170 + i * 185; k = pop_(t, t0 + i * 0.12)
        if k <= 0: continue
        c.save(); c.translate(x, y); c.scale(k, k)
        hero_like = (i == 3)
        draw_stick(c, 0, 200, 0.95, POSES["stand"], Face("open", "smile"), t=t, scarf=RD if (hero_like and t > hl_t) else (120, 128, 146), blink=blink_at(t, i * 0.2))
        c.restore()
        if hero_like and t > hl_t: ink(c, [wob(circ_pts(x, y + 60, 115, -100, 255, 40, ry=200), 77, 1.5)], pr(t, hl_t, 0.4), RD, 9, pen_=False)


