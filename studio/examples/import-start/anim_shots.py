# ================= HOW TO START EP 6: How to start importing (whiteboard; new drawings: cargo route, permit, tariff code, landed-cost receipt, customs booth, $800 parcel). WHITEBOARD look (owner 6 Nov: "whiteboard +
# chalkboard style, white background, better font, voice and script"). nbnkit rig + a marker kit: everything is drawn on with a
# marker pen in front of you (write-on strokes, hatch fills, handwritten type), erased with a wipe between ideas. =================
L0 = lambda i: LINES[i]["start"]; L1 = lambda i: LINES[i]["end"]


def TT(lid, w, frac=0.5, nth=0):
    try: return T(lid, w, nth)
    except Exception: return L0(lid) + (L1(lid) - L0(lid)) * frac


import sys as _sys, os as _os
_sys.path.insert(0, _D if "_D" in globals() else f"{B}/scripts")
from nbnkit import *        # noqa
import nbnkit.nbn_gfx as _ng
import skia
_ng._TF.update({"pm": "PermanentMarker.ttf", "kb": "Kalam-Bold.ttf", "kr": "Kalam-Regular.ttf"})

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


# ---------------------------------------------------------------- import props (new for this episode)
SEA = (40, 130, 210); TEAL2 = (20, 150, 140)
from nbnkit.board import house_m, stamp_m   # noqa (also defined above)


def doc_m(c, x, y, w, h, t, t0, title, lines_=3, col=MK, tilt=-3):
    k = pr(t, t0, 0.5)
    c.save(); c.translate(x, y); c.rotate(tilt)
    c.drawRect(R.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), paint((0, 0, 0), 0.10 * k, blur=10)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], len(title), 1.2)], k, col, 7)
    mtext(c, title, 0, -h / 2 + 76, 52, col, pr(t, t0 + 0.35, 0.4), "pm")
    for i in range(lines_):
        yy = -h / 2 + 140 + i * 52
        if yy < h / 2 - 30: ink(c, [[(-w / 2 + 40, yy), (w / 2 - 40 - (i % 2) * 70, yy)]], pr(t, t0 + 0.6 + i * 0.1, 0.25), (150, 156, 170), 7, pen_=False)
    c.restore()


def box_m(c, x, y, w, t, t0, col=OR, label=None, tilt=0):
    h = w * 0.8; k = pr(t, t0, 0.6)
    c.save(); c.translate(x, y); c.rotate(tilt)
    body = [(-w / 2, -h), (w / 2, -h), (w / 2, 0), (-w / 2, 0), (-w / 2, -h)]
    if k > 0.5: hatch(c, _path(body), pr(t, t0 + 0.4, 0.4), col, gap=18, w=6, bbox=(-w / 2, -h, w / 2, 0), a=0.5)
    ink(c, [wob(body, 31, 1.0), [(-w / 2, -h * 0.72), (w / 2, -h * 0.72)], [(0, -h), (0, -h * 0.72)]], k, MK, 7)
    if label: mtext(c, label, 0, -h * 0.3, int(w * 0.17), MK, pr(t, t0 + 0.6, 0.3), "kb")
    c.restore()


def ship_m(c, x, y, s, t, t0, col=SEA):
    k = pr(t, t0, 0.6); sc = lambda P: [(x + px * s, y + py * s) for px, py in P]
    hull = [(-150, -40), (150, -40), (115, 20), (-125, 20), (-150, -40)]
    ink(c, [wob(sc(hull), 51, 1.0)], k, MK, 7)
    if k > 0.6: hatch(c, _path(sc(hull)), pr(t, t0 + 0.4, 0.3), col, gap=16, w=6, bbox=(x - 160 * s, y - 50 * s, x + 160 * s, y + 30 * s), a=0.6)
    for i, cc in enumerate((OR, RD, GR, BLU)):
        kk = pop_(t, t0 + 0.5 + i * 0.1)
        if kk > 0: c.save(); c.translate(x + (-100 + i * 58) * s, y - 70 * s); c.scale(kk, kk); c.drawRect(R.MakeXYWH(-26 * s, -28 * s, 52 * s, 56 * s), paint(cc, 0.85)); c.drawRect(R.MakeXYWH(-26 * s, -28 * s, 52 * s, 56 * s), stroke(MK, 4)); c.restore()


def waves(c, y, t, x0=90, x1=990, amp=10):
    pts = [(x, y + amp * math.sin(x / 40 + t * 2)) for x in range(x0, x1, 12)]
    c.drawPath(_path(pts), stroke(SEA, 6, 0.8))


def booth_m(c, x, y, t, t0, arm=0.0):
    k = pr(t, t0, 0.7)
    house = [(x - 120, y), (x - 120, y - 260), (x + 120, y - 260), (x + 120, y), (x - 120, y)]
    roof = [(x - 150, y - 260), (x, y - 340), (x + 150, y - 260)]
    win = [(x - 80, y - 200), (x + 80, y - 200), (x + 80, y - 120), (x - 80, y - 120), (x - 80, y - 200)]
    ink(c, [wob(house, 61, 1.0), wob(roof, 62, 1.0), wob(win, 63, 0.6)], k, MK, 7)
    mtext(c, "CUSTOMS", x, y - 280 + 4, 40, BLU, pr(t, t0 + 0.6, 0.3), "pm")
    if k >= 1:   # the barrier arm
        a = math.radians(-80 * arm); bx, by = x + 130, y - 90; L = 330
        c.drawPath(_path([(bx, by), (bx + L * math.cos(a), by + L * math.sin(a))]), stroke(RD, 16)); c.drawCircle(bx, by, 14, paint(MK))


def receipt_m(c, x, y, t, rows, total_t=None):
    w, h = 520, 560
    c.save(); c.translate(x, y); c.rotate(2)
    c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 71, 1.2)], 1, MK, 6, pen_=False)
    for i, (lab, tm) in enumerate(rows):
        yy = -h / 2 + 80 + i * 70; k = pr(t, tm, 0.3)
        mtext(c, lab, -w / 2 + 50, yy, 44, MK, k, "kb", align="l")
        if k >= 1: ink(c, [[(w / 2 - 110, yy - 16), (w / 2 - 92, yy + 2), (w / 2 - 56, yy - 36)]], pr(t, tm + 0.3, 0.2), GR, 8, pen_=False)
    if total_t is not None:
        yy = -h / 2 + 80 + len(rows) * 70 + 10; kt = pr(t, total_t, 0.4)
        ink(c, [[(-w / 2 + 40, yy - 40), (w / 2 - 40, yy - 40)]], kt, MK, 6, pen_=False)
        mtext(c, "LANDED COST", 0, yy + 20, 56, RD, pr(t, total_t + 0.2, 0.4), "pm")
    c.restore()


# ---------------------------------------------------------------- shots
SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.1, "wipe"), ("S_i3", L0("i3") - 0.1, "wipe"),
            ("S_a1", L0("a1") - 0.1, "wipe"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_c1", L0("c1") - 0.1, "wipe"),
            ("S_d1", L0("d1") - 0.1, "wipe"), ("S_e1", L0("e1") - 0.1, "wipe"), ("S_f1", L0("f1") - 0.1, "wipe"),
            ("S_t1", L0("t1") - 0.1, "wipe"), ("S_end", L0("z1") - 0.1, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def S_i1(c, t):
    t0 = SHOT["S_i1"]["start"]; tl = TT("i1", "license", 0.7)
    doc_m(c, 540, 1080, 520, 520, t, t0 + 0.02, "IMPORT LICENSE")
    stamp_m(c, 560, 1180, "USUALLY NOT NEEDED", pr(t, tl, 0.22), col=GR, tilt=-10, size=58)
    say(c, t, t0 + 0.4, "to import into the US you usually need", "NO LICENSE", MK, under=GR)
    note(c, t, tl + 0.4, "IN MOST CASES · USA.gov")


def S_i2(c, t):
    t0 = SHOT["S_i2"]["start"]; tp = TT("i2", "twenty", 0.8)
    floor_line(c, t, t0)
    box_m(c, 300, 1250, 230, t, t0 + 0.1, OR, "MADE THERE")
    mtext(c, "$2", 300, 940, 110, GR, pr(t, TT("i2", "two", 0.6) - 0.1, 0.3), "pm")
    arrow_m(c, (440, 1120), (640, 1120), pr(t, tp - 0.5, 0.35), MK, 9, bend=-0.25)
    hero(c, 820, FLOOR, 1.0, POSES["point"] if t > tp else POSES["stand"], Face("happy", "grin", look=(-1, 0)), t, flip=True)
    mtext(c, "$20", 800, 940, 110, RD, pr(t, tp - 0.1, 0.3), "pm")
    say(c, t, t0 + 0.08, "you found a product overseas", "$2 THERE", GR, t1=tp - 0.3, under=GR)
    say(c, t, tp - 0.25, "here, it sells for", "$20", RD, under=RD)
    note(c, t, t0 + 0.6, "MADE-UP NUMBERS")


def S_i3(c, t):
    t0 = SHOT["S_i3"]["start"]; tc = TT("i3", "catches", 0.7)
    waves(c, 1250, t)
    xs = [190, 370, 550, 730]
    path = [(120, 1180), (930, 1180)]
    pa = stroke(MK, 6, 0.7); pa.setPathEffect(skia.DashPathEffect.Make([22, 16], 0)); c.drawPath(_path(path), pa)
    for i, x in enumerate(xs):
        k = pop_(t, t0 + 0.3 + i * 0.25)
        if k > 0:
            c.save(); c.translate(x, 1180); c.scale(k, k); c.drawCircle(0, 0, 46, paint(WHITE)); c.drawCircle(0, 0, 46, stroke(BLU, 7)); mtext(c, str(i + 1), 0, 22, 62, BLU, 1, "pm"); c.restore()
    kx = pop_(t, tc - 0.15)
    if kx > 0:
        c.save(); c.translate(900, 1180); c.scale(kx, kx); c.drawCircle(0, 0, 50, paint(WHITE)); c.drawCircle(0, 0, 50, stroke(RD, 8)); mtext(c, "!", 0, 30, 80, RD, 1, "pm"); c.restore()
    sx = 120 + 780 * eo(pr(t, t0 + 0.2, max(0.5, L1("i3") - t0)))
    ship_m(c, sx, 1110, 0.55, t, t0)
    say(c, t, t0 + 0.08, "four steps bring it home", "+ ONE TRAP", RD, under=RD)


def S_a1(c, t):
    t0 = SHOT["S_a1"]["start"]; t2 = L0("a2"); t3 = L0("a3")
    doc_m(c, 380, 1080, 380, 460, t, t0 + 0.1, "MOST GOODS", lines_=4, col=GR)
    if t > t2 + 0.2: ink(c, [[(300, 1190), (350, 1240), (450, 1130)]], pr(t, t2 + 0.3, 0.3), GR, 14, pen_=False)
    if t > TT("a2", "permit.", 0.5) - 0.2: doc_m(c, 760, 1110, 300, 380, t, TT("a2", "permit.", 0.5) - 0.2, "PERMIT", lines_=3, col=RD, tilt=5)
    if t > t3:   # magnifier over the permit = look up the agency
        k = pr(t, t3 + 0.1, 0.5)
        ink(c, [wob(circ_pts(760, 1090, 90, -90, 270, 30), 81, 0.8), [(824, 1154), (900, 1240)]], k, MK, 12)
    say(c, t, t0 + 0.08, "step one", "IS IT ALLOWED?", MK, t1=t2 - 0.3, under=BLU)
    say(c, t, t2 - 0.25, "most goods: no license. some need a", "PERMIT", RD, t1=t3 - 0.3, under=RD)
    say(c, t, t3 - 0.25, "food, kids' toys: extra rules", "CHECK YOURS", BLU, under=BLU)
    note(c, t, t2 + 0.3, "SOME ITEMS NEED A LICENSE, PERMIT OR CERTIFICATION · USA.gov")


def S_b1(c, t):
    t0 = SHOT["S_b1"]["start"]; t2 = L0("b2"); t3 = L0("b3")
    box_m(c, 330, 1300, 300, t, t0 + 0.05, BLU)
    code = "XXXX.XX.XXXX"
    mtext(c, code, 540, 1010, 84, MK, pr(t, t0 + 0.4, 0.9), "pm", pen_=True)
    boxed(c, 540, 985, 640, 120, pr(t, t0 + 1.3, 0.3), BLU, 91, 6)
    if t > t2:
        arrow_m(c, (700, 1070), (800, 1210), pr(t, TT("b2", "duty", 0.6) - 0.3, 0.3), MK, 9, bend=0.2)
        mtext(c, "DUTY %", 820, 1290, 80, GR if t < t3 else RD, pr(t, TT("b2", "duty", 0.6), 0.3), "pm")
    if t > t3 + 0.2: cross(c, 230, 960, 850, 1030, pr(t, t3 + 0.3, 0.2), RD, 14, seed=12)
    say(c, t, t0 + 0.08, "next", "FIND ITS CODE", MK, t1=t2 - 0.3, under=BLU)
    say(c, t, t2 - 0.25, "the tariff code decides", "YOUR DUTY", GR, t1=t3 - 0.3, under=GR)
    say(c, t, t3 - 0.25, "wrong code?", "WRONG DUTY", RD, under=RD)
    note(c, t, t0 + 0.6, "US HARMONIZED TARIFF SCHEDULE · USITC")


def S_c1(c, t):
    t0 = SHOT["S_c1"]["start"]; t2 = L0("c2"); t3 = L0("c3")
    rows = [("PRODUCT", TT("c2", "product,", 0.2)), ("SHIPPING", TT("c2", "shipping,", 0.35)), ("INSURANCE", TT("c2", "insurance,", 0.5)),
            ("DUTY", TT("c2", "duty", 0.6)), ("BROKER FEES", TT("c2", "broker", 0.7))]
    receipt_m(c, 540, 1110, t, rows, total_t=TT("c2", "All", 0.85))
    if t > t3:
        k = pop_(t, t3 + 0.2); c.save(); c.translate(850, 860); c.scale(k, k); mtext(c, "$2?", 0, 30, 90, GR, 1, "pm"); c.restore()
        cross(c, 780, 820, 930, 880, pr(t, TT("c3", "stop", 0.6), 0.2), RD, 12, seed=33)
    say(c, t, t0 + 0.08, "third · what does it", "REALLY COST?", MK, t1=t2 - 0.3, under=OR)
    say(c, t, t2 - 0.25, "add every cost before", "ANY DEPOSIT", OR, t1=t3 - 0.3, under=OR)
    say(c, t, t3 - 0.25, "where cheap deals stop", "BEING CHEAP", RD, under=RD)


def S_d1(c, t):
    t0 = SHOT["S_d1"]["start"]; t2 = L0("d2"); t3 = L0("d3"); t4 = L0("d4")
    floor_line(c, t, t0)
    arm = 0.0 if t < t2 else eo(pr(t, t2 + 0.5, 0.6)) * (1 if t < t3 else 0.0)
    booth_m(c, 330, FLOOR - 10, t, t0 + 0.05, arm)
    if t2 < t < t3:
        box_m(c, 820, FLOOR - 10, 170, t, t2 + 0.1, GR, "UNDER")
        mtext(c, "NO BOND", 820, 1170, 54, GR, pr(t, TT("d2", "bond.", 0.8) - 0.2, 0.3), "kb")
    if t > t3:
        box_m(c, 860, FLOOR - 10, 220, t, t3 + 0.1, RD, "OVER")
        doc_m(c, 860, 1020, 240, 190, t, TT("d3", "bond.", 0.8) - 0.3, "BOND", lines_=1, col=RD, tilt=6)
    if t > t4:
        hero(c, 640, FLOOR, 0.9, POSES["point"], Face("open", "smile", look=(-1, 0)), t, flip=True)
    say(c, t, t0 + 0.08, "last step · who lets it through?", "CUSTOMS", MK, t1=t2 - 0.3, under=BLU)
    say(c, t, t2 - 0.25, "$2,500 or less: usually no bond", "SIMPLER ENTRY", GR, t1=t3 - 0.3, under=GR, size=150)
    say(c, t, t3 - 0.25, "above that: a formal entry", "+ A BOND", RD, t1=t4 - 0.3, under=RD)
    say(c, t, t4 - 0.25, "most beginners hire a", "CUSTOMS BROKER", BLU, under=BLU, size=150)
    note(c, t, t2 + 0.3, "INFORMAL ENTRY LIMIT $2,500 · FEDERAL REGISTER 2012 · RULES MAY CHANGE")


def S_e1(c, t):
    t0 = SHOT["S_e1"]["start"]; t2 = L0("e2"); t3 = L0("e3")
    box_m(c, 540, 1360, 300, t, t0 + 0.1, PU)
    k = pop_(t, TT("e1", "eight", 0.4) - 0.1)
    if k > 0:
        c.save(); c.translate(540, 980); c.scale(k, k); c.rotate(-4)
        c.drawRoundRect(R.MakeXYWH(-230, -70, 460, 140), 20, 20, paint(WHITE)); c.drawRoundRect(R.MakeXYWH(-230, -70, 460, 140), 20, 20, stroke(GR, 8))
        mtext(c, "$800 DUTY-FREE", 0, 22, 62, GR, 1, "pm"); c.restore()
    stamp_m(c, 540, 1000, "SUSPENDED", pr(t, TT("e2", "suspended.", 0.5), 0.22), col=RD, tilt=-12, size=90)
    mtext(c, "EVERY COUNTRY", 540, 830, 56, RD, pr(t, TT("e2", "every", 0.5), 0.3), "pm")
    if t > t3: stamp_m(c, 760, 1260, "DUTY", pr(t, TT("e3", "duty", 0.5), 0.22), col=OR, tilt=10, size=60)
    say(c, t, t0 + 0.08, "remember", "$800 DUTY-FREE?", GR, t1=t2 - 0.3, under=GR, size=150)
    say(c, t, t2 - 0.25, "since 29 August 2025", "SUSPENDED", RD, t1=t3 - 0.3, under=RD)
    say(c, t, t3 - 0.25, "even a tiny test order can", "OWE DUTY", OR, under=OR)
    note(c, t, t2 + 0.3, "DE MINIMIS SUSPENDED FOR ALL COUNTRIES · CBP / KPMG, AUG 2025")


def S_f1(c, t):
    t0 = SHOT["S_f1"]["start"]
    k = pr(t, t0 + 0.1, 0.6)
    c.save(); c.translate(540, 1080); c.rotate(-3)
    c.drawRoundRect(R.MakeXYWH(-300, -170, 600, 340), 26, 26, paint(WHITE, k))
    ink(c, [wob([(-300, -170), (300, -170), (300, 170), (-300, 170), (-300, -170)], 99, 1.2)], k, BLU, 8)
    mtext(c, "EORI NUMBER", 0, -70, 64, BLU, pr(t, t0 + 0.6, 0.4), "pm")
    mtext(c, "GB 0000 0000 0000", 0, 40, 52, MK, pr(t, t0 + 1.0, 0.6), "kb")
    c.restore()
    box_m(c, 820, 1420, 150, t, TT("f1", "box.", 0.5) - 0.3, OR)
    say(c, t, t0 + 0.08, "importing into the UK? first get an", "EORI NUMBER", BLU, under=BLU)
    note(c, t, t0 + 0.6, "MOVING GOODS IN OR OUT OF GREAT BRITAIN · GOV.UK")


def S_t1(c, t):
    t0 = SHOT["S_t1"]["start"]
    floor_line(c, t, t0)
    hero(c, 250, FLOOR, 1.0, POSES["hold"], Face("happy", "grin", look=(1, -1)), t)
    box_m(c, 560, FLOOR - 4, 200, t, TT("t1", "product?", 0.2) - 0.2, OR)
    house_m(c, 820, FLOOR - 4, 0.9, t, TT("t1", "small.", 0.9) - 0.2, col=TEAL2)
    mtext(c, "$2 + EVERY COST", 640, 1080, 64, RD, pr(t, TT("t1", "every", 0.4) - 0.2, 0.4), "pm")
    say(c, t, t0 + 0.08, "add every cost first, then", "START SMALL", GR, under=GR)


def S_end(c, t):
    t0 = SHOT["S_end"]["start"]; tz2 = L0("z2"); ty = TT("z1", "YES", 0.75)
    floor_line(c, t, t0)
    hero(c, 300, FLOOR, 1.05, POSES["point_up"] if t > tz2 else POSES["shrug"], Face("open", "smile", look=(1, -1)), t)
    girl(c, 780, FLOOR, 1.05, POSES["wave"] if t > tz2 else POSES["stand"], Face("happy", "grin", look=(-1, 0)), t, dress=TEAL2, style="long", flip=True)
    for i, (word, col, x) in enumerate((("YES", GR, 400), ("NO", RD, 680))):
        mtext(c, word, x, 1010, 110, col, pr(t, ty - 0.1 + i * 0.25, 0.3), "pm")
        ink(c, [wob(circ_pts(x, 975, 120, -120, 245, 40, ry=86), 95 + i, 1.6)], pr(t, ty + 0.2 + i * 0.25, 0.35), col, 9, pen_=False)
    say(c, t, t0 + 0.08, "would you try importing?", "YES OR NO?", MK, t1=tz2 - 0.3, under=BLU)
    say(c, t, tz2 - 0.25, "send it to a friend who finds deals", "SAVE THIS", BLU, under=OR)
    note(c, t, t0 + 0.6, "COMMENT ONE WORD · EDUCATION ONLY")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
SURF = surface()
IMPACTS = [(TT("i1", "license", 0.7), 0.12, 4), (TT("e2", "suspended.", 0.5), 0.18, 6), (TT("b3", "wrong", 0.3), 0.12, 4)]
_TOP = {"S_a1": 1, "S_b1": 2, "S_c1": 3, "S_d1": 4}


def topline(sid): return f"HOW TO START · STEP {_TOP[sid]} OF 4" if sid in _TOP else "OOPSMYBUSINESS · HOW TO START"


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    c = SURF.getCanvas(); c.resetMatrix()
    board_bg(c, tt, seed=SHOTS.index(s) * 3)
    u = pr(tt, s["start"], max(0.5, s["end"] - s["start"])); z = 1.0 + 0.018 * u
    dx = dy = 0.0
    for ti, d, a in IMPACTS:
        if ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83)
    c.save(); c.translate(W / 2 + dx, H * 0.6 + dy); c.scale(z, z); c.translate(-W / 2, -H * 0.6)
    RENDER[sid](c, tt)
    c.restore()
    pill(c, topline(sid))
    return to_rgb(SURF).astype(np.float32)


def _eraser(f, prev, p):
    """board wipe: an eraser sweeps left to right; the old drawing is left of nothing, the new board appears behind it"""
    x = int(-200 + (W + 400) * eio(p))
    out = f.copy()
    if x < W: out[:, max(0, x):] = prev[:, max(0, x):]
    x0, x1 = max(0, x - 170), min(W, x + 30)
    if x1 > x0:
        out[:, x0:x1] = out[:, x0:x1] * 0.25 + np.array(BOARD, np.float32) / 255 * 0.75
    bx0, bx1 = max(0, x - 150), min(W, x + 10)
    if bx1 > bx0:   # the eraser block itself (felt pad + handle), mid-height
        out[820:1180, bx0:bx1] = np.array((60, 66, 84), np.float32) / 255
        out[1150:1180, bx0:bx1] = np.array((210, 210, 214), np.float32) / 255
    return out


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); dt = t - sh["start"]
    if i > 0 and sh["trans"] == "wipe" and dt < 0.34:
        prv = rs(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n); f = _eraser(f, prv, dt / 0.34)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
