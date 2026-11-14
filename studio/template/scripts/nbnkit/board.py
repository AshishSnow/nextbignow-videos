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


_BOIL = [0, 0.45]   # 14 Nov 2026 (childminding): LINE BOIL — state 0 = off; 1..n = which re-drawn variant of every marker line is shown


def set_boil(state, strength=0.45):
    """line boil (borrowed from the owner's 13 Nov doodle look, which opened at 78 % past 3 s): call once per frame from rs() with a state that
    changes every few frames (e.g. 1 + (n // 3) % 3); every wob() line then gets a small extra wobble that differs per state, so a held drawing
    looks re-inked by hand instead of frozen. state 0 turns it off (lab frames, contact sheets)."""
    _BOIL[0] = int(state); _BOIL[1] = strength


def wob(pts, seed=1, amp=2.2, step=26):
    """resample a polyline and add a small hand wobble (deterministic; plus the line boil when set_boil() is on)"""
    out = []; r = _rng(seed)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(1, int(d / step))
        for i in range(n):
            k = i / n; out.append((x0 + (x1 - x0) * k, y0 + (y1 - y0) * k))
    out.append(pts[-1])
    noise = r.normal(0, amp, (len(out), 2)); noise = np.cumsum(noise, 0) * 0.35; noise -= np.linspace(noise[0], noise[-1], len(out))
    if _BOIL[0] and len(out) > 2:
        rb = _rng(seed * 31.7 + _BOIL[0] * 7.13); nb = np.cumsum(rb.normal(0, max(amp, 0.6), (len(out), 2)), 0) * 0.35 * _BOIL[1]
        nb -= np.linspace(nb[0], nb[-1], len(out)); noise = noise + nb
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
    """board two-tier: a small Kalam line written on, then ONE big Permanent Marker word written on; optional marker underline.
    7 Nov: centred on the SAFE zone (x 60..960 -> centre 510), big word capped at 840 px, so layout_check finds 0 right-zone pixels."""
    if t < t0 or (t1 is not None and t > t1): return
    CX = 510
    fb = font("pm", size); wb = tw(fb, big)
    if wb > 840: size *= 840 / wb; fb = font("pm", size); wb = tw(fb, big)
    k1 = pr(t, t0, 0.32); k2 = pr(t, t0 + 0.14, max(0.28, 0.035 * len(big)))
    if small:   # small line shrinks to fit the safe width (left 60 / right 120 px) — 6 Nov fix
        ss = 52; fs_ = font("kb", ss)
        while tw(fs_, small) > 820 and ss > 34: ss -= 2; fs_ = font("kb", ss)
        mtext(c, small, CX, y - size * 0.98, ss, smallc, k1, "kb")
    mtext(c, big, CX, y, size, col, k2, "pm")
    if under is not None and k2 >= 1:
        ku = pr(t, t0 + 0.14 + max(0.28, 0.035 * len(big)), 0.25)
        ink(c, [wob([(CX - wb / 2, y + 26), (CX + wb / 2, y + 20)], seed=len(big), amp=1.4)], ku, under, 10, pen_=False)


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


def browser_m(c, x, y, t, t0, url="AnnualCreditReport.com", title="YOUR REPORT", w=760, h=470):
    """a browser window; url/title default to the credit-score episode (7 Nov: made generic, same defaults)"""
    k = pr(t, t0, 0.7)
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 91, 1.4),
            wob([(x - w / 2, y - h / 2 + 70), (x + w / 2, y - h / 2 + 70)], 92, 0.8)], k, MK, 8)
    if k >= 1:
        for i, col in enumerate((RD, OR, GR)): c.drawCircle(x - w / 2 + 40 + i * 36, y - h / 2 + 35, 11, paint(col))
        c.drawRoundRect(R.MakeXYWH(x - w / 2 + 150, y - h / 2 + 14, w - 190, 42), 21, 21, stroke(MK, 4))
        if url: mtext(c, url, x + 50, y - h / 2 + 47, 34, BLU, pr(t, t0 + 0.7, 0.6), "kb")
        if title: mtext(c, title, x, y + 30, 64, MK, pr(t, t0 + 1.0, 0.4), "pm")
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


# ---------------------------------------------------------------- export props (HOW TO START EP 7, examples/export-start, 7 Nov 2026): US outline, TAX toll gate, parchment scroll write-on, candle jar, clipboard checklist, digit boxes, 10x10 grid, buyer card, restricted list, agency folders, search bar, laptop form, EU door + VAT tag
PARCH = (246, 236, 208); PARCH_D = (196, 170, 120); WAX = (250, 222, 160); FLAME = (255, 168, 40)
US_PTS = [(-1.00, -0.30), (-0.86, -0.52), (-0.40, -0.50), (0.10, -0.46), (0.36, -0.40), (0.50, -0.50), (0.70, -0.56), (0.84, -0.66),
          (0.96, -0.58), (0.86, -0.36), (0.72, -0.10), (0.66, 0.12), (0.74, 0.40), (0.62, 0.30), (0.46, 0.14), (0.22, 0.20),
          (0.06, 0.44), (-0.06, 0.24), (-0.30, 0.18), (-0.56, 0.16), (-0.80, 0.02), (-1.00, -0.30)]


def us_m(c, x, y, s, k, col=BLU, label="USA"):
    """a hand-drawn, simplified outline of the lower 48 (no flag, no map data)"""
    pts = [(x + px * s, y + py * s) for px, py in US_PTS]
    ink(c, [wob(pts, 7, 1.4)], k, MK, 7)
    if k > 0.8: hatch(c, _path(pts), pr(k, 0.8, 0.2), col, gap=20, w=6, bbox=(x - s, y - 0.7 * s, x + s, y + 0.5 * s), a=0.35)
    if k >= 1: mtext(c, label, x - 0.05 * s, y + 0.02 * s, int(s * 0.26), MK, 1, "pm")


def tollgate_m(c, x, y, t, t0, arm=0.0, word="TAX"):
    k = pr(t, t0, 0.5)
    post = [(x - 40, y), (x - 40, y - 220), (x + 40, y - 220), (x + 40, y)]
    ink(c, [wob(post, 41, 0.8)], k, MK, 7)
    if k >= 1:
        mtext(c, word, x, y - 250, 64, RD, 1, "pm")
        a = math.radians(-78 * arm); bx, by = x + 40, y - 150; L = 300
        c.drawPath(_path([(bx, by), (bx + L * math.cos(a), by + L * math.sin(a))]), stroke(RD, 16)); c.drawCircle(bx, by, 14, paint(MK))


def scroll_m(c, x, y, w, h, t, t0, lines_, t_lines, col=MK, size=50):
    """parchment that unrolls downward, then handwritten lines write on (each line at its own time)"""
    u = eo(pr(t, t0, 0.7)); hh = max(30, h * u)
    top, bot = y - h / 2, y - h / 2 + hh
    body = [(x - w / 2, top), (x + w / 2, top), (x + w / 2, bot), (x - w / 2, bot), (x - w / 2, top)]
    c.drawPath(_path(body), paint(PARCH)); c.drawPath(_path(body), stroke(PARCH_D, 5))
    for yy in (top, bot):   # the two rolls
        c.drawRoundRect(R.MakeXYWH(x - w / 2 - 26, yy - 22, w + 52, 44), 22, 22, paint((236, 220, 180)))
        c.drawRoundRect(R.MakeXYWH(x - w / 2 - 26, yy - 22, w + 52, 44), 22, 22, stroke(MK, 6))
    for i, (ln, tl) in enumerate(zip(lines_, t_lines)):
        yy = top + 110 + i * size * 1.35
        if yy < bot - 30: mtext(c, ln, x, yy, size, col, pr(t, tl, 0.3), "kb", pen_=True)


def candle_m(c, x, y, s, t, t0, col=OR):
    """a jar candle with a flickering marker flame"""
    k = pr(t, t0, 0.5); w, h = 150 * s, 190 * s
    jar = [(x - w / 2, y - h), (x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h)]
    ink(c, [wob(jar, 11, 0.8), [(x, y - h), (x, y - h - 26 * s)]], k, MK, 7)
    if k > 0.7: hatch(c, _path([(x - w / 2, y - h * 0.82), (x + w / 2, y - h * 0.82), (x + w / 2, y), (x - w / 2, y)]), pr(t, t0 + 0.4, 0.3), col, gap=16, w=6, bbox=(x - w / 2, y - h, x + w / 2, y), a=0.55)
    if k >= 1:
        fl = 1 + 0.12 * math.sin(t * 13) + 0.06 * math.sin(t * 29)
        c.save(); c.translate(x, y - h - 30 * s); c.scale(1, fl)
        c.drawPath(poly([(0, -62 * s), (22 * s, -10 * s), (0, 8 * s), (-22 * s, -10 * s)], True), paint(FLAME, 0.95))
        c.drawPath(poly([(0, -30 * s), (9 * s, -4 * s), (0, 4 * s), (-9 * s, -4 * s)], True), paint((255, 236, 140)))
        c.restore()


def clipboard_m(c, x, y, t, t0, items, ticks, hot=None, hot_t=None):
    """a clipboard checklist: numbered boxes; ticks = list of times each box gets its green tick; hot = index circled red"""
    w, h = 520, 640; k = pr(t, t0, 0.5)
    c.drawRoundRect(R.MakeXYWH(x - w / 2 + 10, y - h / 2 + 14, w, h), 24, 24, paint((0, 0, 0), 0.10 * k, blur=10))
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 24, 24, paint((214, 176, 120), k))
    c.drawRect(R.MakeXYWH(x - w / 2 + 30, y - h / 2 + 50, w - 60, h - 80), paint(WHITE, k))
    c.drawRoundRect(R.MakeXYWH(x - 90, y - h / 2 - 20, 180, 60), 14, 14, paint((150, 156, 170), k))
    for i, lab in enumerate(items):
        yy = y - h / 2 + 150 + i * 125; ki = pr(t, t0 + 0.3 + i * 0.18, 0.3)
        ink(c, [wob([(x - 200, yy - 40), (x - 130, yy - 40), (x - 130, yy + 30), (x - 200, yy + 30), (x - 200, yy - 40)], 50 + i, 0.6)], ki, MK, 6, pen_=False)
        mtext(c, lab, x - 100, yy + 14, 46, MK, ki, "kb", align="l")
        if i < len(ticks) and ticks[i] is not None and t > ticks[i]:
            ink(c, [[(x - 190, yy - 4), (x - 168, yy + 22), (x - 120, yy - 56)]], pr(t, ticks[i], 0.25), GR, 11, pen_=False)
        if hot == i and hot_t is not None and t > hot_t:
            ink(c, [wob(circ_pts(x + 10, yy - 4, 250, -160, 200, 44, ry=72), 77, 1.3)], pr(t, hot_t, 0.4), RD, 9, pen_=False)


def digits_m(c, x, y, t, t0, step=0.14, col=BLU, fill="•"):
    """ten digit boxes grouped 4.2.4 that fill one by one"""
    bw, gap = 64, 10; groups = [4, 2, 4]; xs = []
    tot = sum(groups) * (bw + gap) + 2 * 26; cx = x - tot / 2
    for gi, g in enumerate(groups):
        for _ in range(g): xs.append(cx); cx += bw + gap
        cx += 26
    for i, bx in enumerate(xs):
        k = pr(t, t0 + i * step * 0.5, 0.2)
        if k <= 0: continue
        c.drawRect(R.MakeXYWH(bx, y - 44, bw, 88), paint(WHITE)); ink(c, [wob([(bx, y - 44), (bx + bw, y - 44), (bx + bw, y + 44), (bx, y + 44), (bx, y - 44)], 60 + i, 0.5)], k, MK, 5, pen_=False)
        if t > t0 + 0.6 + i * step: mtext(c, fill, bx + bw / 2, y + 22, 64, col, 1, "pm")


def grid100_m(c, x, y, t, t0, red_t, cell=46):
    """10x10 boxes; ticks wave in green; the last five turn red at red_t"""
    x0 = x - 5 * cell; y0 = y - 5 * cell
    for i in range(100):
        r, q = divmod(i, 10); bx, by = x0 + q * cell, y0 + r * cell
        k = pr(t, t0 + i * 0.012, 0.15)
        if k <= 0: continue
        red = i >= 95 and t > red_t
        c.drawRect(R.MakeXYWH(bx + 4, by + 4, cell - 8, cell - 8), paint((255, 236, 232) if red else (232, 246, 236), k))
        c.drawRect(R.MakeXYWH(bx + 4, by + 4, cell - 8, cell - 8), stroke(RD if red else GR, 3, k))
        if k >= 1 and not red: c.drawPath(_path([(bx + 12, by + 24), (bx + 20, by + 33), (bx + 34, by + 13)]), stroke(GR, 4))
        if red: c.drawPath(_path([(bx + 13, by + 13), (bx + 33, by + 33)]), stroke(RD, 4)); c.drawPath(_path([(bx + 33, by + 13), (bx + 13, by + 33)]), stroke(RD, 4))


def namecard_m(c, x, y, t, t0, tilt=-4, label="BUYER"):
    w, h = 460, 250; k = pr(t, t0, 0.5)
    c.save(); c.translate(x, y); c.rotate(tilt)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18, paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 88, 1.0)], k, MK, 6)
    mtext(c, label, 0, -40, 50, BLU, pr(t, t0 + 0.3, 0.3), "pm")
    ink(c, [wob([(-150, 40), (-80, 10), (-30, 50), (30, 12), (90, 46), (150, 20)], 89, 1.5, 14)], pr(t, t0 + 0.6, 0.5), MK, 6, pen_=False)
    c.restore()


def list_m(c, x, y, t, t0, n=6, hit=None, hit_t=None, col=RD, title="RESTRICTED"):
    """a long list of scribbled names; one row lights up as a match"""
    w = 420; h = 120 + n * 62; k = pr(t, t0, 0.4)
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint((255, 248, 246), k)); ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 90, 1.0)], k, col, 6)
    mtext(c, title, x, y - h / 2 + 70, 46, col, pr(t, t0 + 0.2, 0.3), "pm")
    for i in range(n):
        yy = y - h / 2 + 130 + i * 62; L = 260 - (i * 37) % 90
        if hit == i and hit_t is not None and t > hit_t:
            c.drawRect(R.MakeXYWH(x - w / 2 + 14, yy - 26, w - 28, 44), paint((255, 214, 120), min(1, pr(t, hit_t, 0.2))))
        ink(c, [wob([(x - L / 2 - 40, yy), (x + L / 2 - 40, yy)], 91 + i, 1.4, 14)], pr(t, t0 + 0.4 + i * 0.08, 0.2), (120, 120, 130), 6, pen_=False)


def folder_m(c, x, y, t, t0, label, col):
    k = pop_(t, t0)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawPath(poly([(-110, -70), (-40, -70), (-25, -90), (110, -90), (110, 70), (-110, 70)], True), paint(col, 0.22))
    c.drawPath(poly([(-110, -70), (-40, -70), (-25, -90), (110, -90), (110, 70), (-110, 70)], True), stroke(col, 6))
    mtext(c, label, 0, 20, 36, col, 1, "pm"); c.restore()


def searchbar_m(c, x, y, w, t, t0, text, col=BLU):
    k = pr(t, t0, 0.4)
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - 50, w, 100), 50, 50, paint(WHITE, k))
    ink(c, [wob([(x - w / 2 + 50, y - 50), (x + w / 2 - 50, y - 50)], 3, 0.5), wob([(x - w / 2 + 50, y + 50), (x + w / 2 - 50, y + 50)], 4, 0.5),
            circ_pts(x - w / 2 + 50, y, 50, 90, 270, 18), circ_pts(x + w / 2 - 50, y, 50, -90, 90, 18)], k, col, 7, pen_=False)
    ink(c, [circ_pts(x + w / 2 - 70, y - 6, 20, 0, 360, 20), [(x + w / 2 - 56, y + 8), (x + w / 2 - 40, y + 26)]], pr(t, t0 + 0.3, 0.3), MK, 6, pen_=False)
    mtext(c, text, x - 30, y + 14, 38, MK, pr(t, t0 + 0.5, 0.9), "kb", pen_=True)


def laptop_m(c, x, y, t, t0, title="EXPORT FORM (EEI)", rows=3):
    k = pr(t, t0, 0.5); w, h = 440, 290
    scr = [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y), (x - w / 2, y - h)]
    base = [(x - w / 2 - 50, y + 10), (x + w / 2 + 50, y + 10), (x + w / 2 + 20, y + 44), (x - w / 2 - 20, y + 44), (x - w / 2 - 50, y + 10)]
    c.drawPath(_path(scr), paint(WHITE, k))
    ink(c, [wob(scr, 21, 0.8), wob(base, 22, 0.8)], k, MK, 7)
    mtext(c, title, x, y - h + 64, 38, BLU, pr(t, t0 + 0.4, 0.4), "pm")
    for i in range(rows):
        yy = y - h + 130 + i * 50
        ink(c, [[(x - w / 2 + 40, yy), (x + w / 2 - 60 - (i % 2) * 60, yy)]], pr(t, t0 + 0.7 + i * 0.12, 0.25), (150, 156, 170), 7, pen_=False)


def eu_door_m(c, x, y, t, t0, t_tag):
    """a doorway marked EU with a VAT price tag swinging on it"""
    k = pr(t, t0, 0.5)
    fr = [(x - 130, y), (x - 130, y - 380), (x + 130, y - 380), (x + 130, y)]
    ink(c, [wob(fr, 71, 0.8)], k, MK, 8)
    if k >= 1:
        c.drawRect(R.MakeXYWH(x - 110, y - 360, 220, 360), paint(BLU, 0.12))
        mtext(c, "EU", x, y - 400, 64, BLU, 1, "pm")
        c.drawCircle(x + 80, y - 180, 10, paint(MK))
    kt = pop_(t, t_tag)
    if kt > 0:
        sw = 6 * math.sin(t * 4)
        c.save(); c.translate(x - 20, y - 300); c.rotate(sw); c.scale(kt, kt)
        c.drawPath(_path([(0, 0), (0, 50)]), stroke(MK, 4))
        c.drawRoundRect(R.MakeXYWH(-90, 50, 180, 92), 14, 14, paint(WHITE)); c.drawRoundRect(R.MakeXYWH(-90, 50, 180, 92), 14, 14, stroke(RD, 7))
        mtext(c, "VAT", 0, 118, 58, RD, 1, "pm"); c.restore()


# ---------------------------------------------------------------- shop + subscription props (R&D writers' room 7 Nov 2026: HOW IT WORKS
# "same cart" (queue/15-same-cart) + "Prime Iliad" (queue/16-prime-iliad)): egg carton, price tag, phone, cart, coin flip, mouse cursor,
# big button, door, maze, Greek helmet. All marker line art with hatch fills; every one draws on with (t, t0).
EGG = (250, 240, 214); CARD_BOARD = (214, 186, 140)


def _sc(x, y, s, pts): return [(x + px * s, y + py * s) for px, py in pts]


def tag_m(c, x, y, text, t, t0, col=BLU, tilt=-8, s=1.0, hot=False):
    """a swing price tag with a string hole; the price writes itself on (hot=True: red ink + a small shake)"""
    k = pr(t, t0, 0.35)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt + (3 * math.sin(t * 9) if hot and k >= 1 else 0)); c.scale(s, s)
    body = [(-120, -60), (90, -60), (140, 0), (90, 60), (-120, 60), (-120, -60)]
    c.drawPath(_path(body), paint(WHITE)); ink(c, [wob(body, 61, 0.8)], k, MK, 6, pen_=False)
    if k > 0.6: c.drawCircle(98, 0, 11, stroke(MK, 4)); ink(c, [wob([(108, 0), (150, -40), (175, -90)], 62, 1)], pr(k, 0.6, 0.4), MK, 3, pen_=False)
    mtext(c, text, -12, 24, 66, RD if hot else col, pr(t, t0 + 0.2, 0.35), "pm")
    c.restore()


def carton_m(c, x, y, t, t0, s=1.0, open_=1.0):
    """a dozen-egg carton: box with bumps, lid open (open_ 0..1) showing 2 rows of eggs"""
    k = pr(t, t0, 0.6); w, h = 460, 120
    base = _sc(x, y, s, [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2 - 20, h / 2), (-w / 2 + 20, h / 2), (-w / 2, -h / 2)])
    if k > 0.5: hatch(c, _path(base), pr(k, 0.5, 0.5), CARD_BOARD, gap=16, w=6, bbox=(x - w * s, y - h * s, x + w * s, y + h * s), a=0.8)
    bumps = [wob(circ_pts(x + (-w / 2 + 38 + i * 77) * s, y + 30 * s, 26 * s, 180, 360, 12), 70 + i, 0.5) for i in range(6)]
    ink(c, [wob(base, 71, 1.0)] + bumps, k, MK, 7)
    if open_ > 0 and k >= 1:
        lid = _sc(x, y, s, [(-w / 2 + 10, -h / 2 - 66), (-w / 2 + 30, -h / 2 - 66 - 170 * open_), (w / 2 - 30, -h / 2 - 66 - 170 * open_), (w / 2 - 10, -h / 2 - 66)])
        ink(c, [wob(lid, 72, 0.8)], pr(t, t0 + 0.6, 0.3), MK, 6, pen_=False)
        for row in range(2):
            for i in range(6):
                ex, ey = x + (-w / 2 + 38 + i * 77) * s + row * 10 * s, y - (34 + row * 34) * s
                c.drawOval(R.MakeXYWH(ex - 30 * s, ey - 38 * s, 60 * s, 70 * s), paint(EGG, open_)); c.drawOval(R.MakeXYWH(ex - 30 * s, ey - 38 * s, 60 * s, 70 * s), stroke(MK, 4, open_))


def phone_m(c, x, y, t, t0, s=1.0, screen=None, buzz_t=None, caller=None):
    """a phone outline (no brand); screen(c, cx, cy, w, h) draws inside the screen clip; buzz_t: shakes + 'bzz' marks; caller: name on top"""
    k = pr(t, t0, 0.5); w, h = 300 * s, 560 * s
    if k <= 0: return
    dx = 6 * math.sin(t * 60) if buzz_t is not None and buzz_t <= t <= buzz_t + 1.2 else 0
    x += dx
    c.drawRoundRect(R.MakeXYWH(x - w / 2 + 8, y - h / 2 + 12, w, h), 40 * s, 40 * s, paint((0, 0, 0), 0.10 * k, blur=10))
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 40 * s, 40 * s, paint(WHITE, k))
    ink(c, [wob([(x - w / 2 + 40 * s, y - h / 2), (x + w / 2 - 40 * s, y - h / 2), (x + w / 2, y - h / 2 + 40 * s), (x + w / 2, y + h / 2 - 40 * s),
                 (x + w / 2 - 40 * s, y + h / 2), (x - w / 2 + 40 * s, y + h / 2), (x - w / 2, y + h / 2 - 40 * s), (x - w / 2, y - h / 2 + 40 * s),
                 (x - w / 2 + 40 * s, y - h / 2)], 81, 0.8)], k, MK, 8)
    if k >= 1:
        c.drawRoundRect(R.MakeXYWH(x - 40 * s, y - h / 2 + 20 * s, 80 * s, 14 * s), 7, 7, paint(MK))
        if screen:
            c.save(); c.clipRect(R.MakeXYWH(x - w / 2 + 18 * s, y - h / 2 + 50 * s, w - 36 * s, h - 100 * s)); screen(c, x, y, w - 36 * s, h - 100 * s); c.restore()
        if caller: mtext(c, caller, x, y - h / 2 + 130 * s, int(54 * s), MK, pr(t, t0 + 0.4, 0.3), "pm")
        if buzz_t is not None and t >= buzz_t:
            kb = pr(t, buzz_t, 0.3)
            for side in (-1, 1):
                for j in range(2):
                    xx = x + side * (w / 2 + 26 + j * 24); ink(c, [[(xx, y - 60 + j * 10), (xx + side * 10, y - 20), (xx, y + 20 - j * 10)]], kb, RD, 6, pen_=False)


def cart_m(c, x, y, t, t0, s=1.0, items=0, col=GR):
    """a shopping cart (side view); items 0..1 fills it with hatched boxes/bottles"""
    k = pr(t, t0, 0.7)
    basket = _sc(x, y, s, [(-210, -200), (190, -200), (150, -40), (-170, -40), (-210, -200)])
    frame = _sc(x, y, s, [(-260, -240), (-210, -200)]); under = _sc(x, y, s, [(-170, -40), (-180, 10), (170, 10)])
    grid = [_sc(x, y, s, [(-210 + i * 80, -200), (-170 + i * 64, -40)]) for i in range(1, 5)] + [_sc(x, y, s, [(-200, -120), (170, -120)])]
    ink(c, [wob(frame, 91, 0.6), wob(basket, 92, 1.0), wob(under, 93, 0.8)] + [wob(g, 94 + i, 0.4) for i, g in enumerate(grid)], k, MK, 7)
    for wx in (-140, 130):
        kw = pr(t, t0 + 0.55, 0.2)
        if kw > 0: ink(c, [circ_pts(x + wx * s, y + 40 * s, 28 * s, 0, 360, 20)], kw, MK, 7, pen_=False)
    if items > 0 and k >= 1:
        boxes = [(-160, -290, 90, 110, OR), (-50, -270, 70, 90, BLU), (40, -300, 60, 120, RD), (120, -260, 60, 70, PU)]
        n = int(len(boxes) * items + 0.999)
        for i, (bx, by, bw, bh, bc) in enumerate(boxes[:n]):
            pth = _path(_sc(x, y, s, [(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh), (bx, by)]))
            c.drawPath(pth, paint(WHITE)); hatch(c, pth, 1, bc, gap=14, w=5, bbox=(x + bx * s, y + by * s, x + (bx + bw) * s, y + (by + bh) * s), a=0.6)
            c.drawPath(pth, stroke(MK, 5))


def coin_m(c, x, y, t, t0, r=90, land=0.9, face="?"):
    """a coin tossed up from (x, y): flips (squashes) on the way, lands at t0+land and writes its face"""
    if t < t0: return
    u = min(1.0, (t - t0) / land); hy = -320 * 4 * u * (1 - u)
    sq = abs(math.cos((t - t0) * 18)) if u < 1 else 1.0
    c.save(); c.translate(x, y + hy); c.scale(1, max(0.08, sq))
    c.drawCircle(0, 0, r, paint((252, 206, 70))); c.drawCircle(0, 0, r, stroke(MK, 7)); c.drawCircle(0, 0, r * 0.74, stroke((190, 140, 30), 4))
    c.restore()
    if u >= 1: mtext(c, face, x, y + r * 0.35, int(r * 0.95), MK, pr(t, t0 + land, 0.25), "pm")


def cursor_m(c, x, y, t, t0, s=1.0, wiggle=True):
    """a mouse arrow cursor that draws on, then wanders a little"""
    k = pr(t, t0, 0.35)
    if k <= 0: return
    if wiggle and k >= 1: x += 26 * math.sin((t - t0) * 2.3); y += 18 * math.sin((t - t0) * 3.1)
    pts = _sc(x, y, s, [(0, 0), (0, 120), (30, 92), (54, 146), (76, 136), (52, 84), (92, 84), (0, 0)])
    if k >= 1: c.drawPath(_path(pts), paint(WHITE))
    ink(c, [pts], k, MK, 6, pen_=False)


def button_m(c, x, y, text, t, t0, w=520, h=120, col=OR, glow=True, small=False):
    """a big rounded call-to-action button (marker hatch fill); small=True draws a tiny text-link instead"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    if small:
        mtext(c, text, x, y, 40, BLU, k, "kb", pen_=True)
        if k >= 1: ink(c, [wob([(x - tw(font("kb", 40), text) / 2, y + 8), (x + tw(font("kb", 40), text) / 2, y + 8)], 101, 0.6)], 1, BLU, 3, pen_=False)
        return
    if glow and k >= 1: c.drawRoundRect(R.MakeXYWH(x - w / 2 - 20, y - h / 2 - 20, w + 40, h + 40), 50, 50, paint(col, 0.18 + 0.08 * math.sin(t * 5), blur=22))
    rr = skia.Path(); rr.addRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 44, 44)
    c.drawPath(rr, paint(WHITE)); hatch(c, rr, pr(t, t0 + 0.25, 0.3), col, gap=14, w=7, bbox=(x - w / 2, y - h / 2, x + w / 2, y + h / 2), a=0.75)
    c.drawPath(rr, stroke(MK, 7, k))
    mtext(c, text, x, y + 24, 64, MK, pr(t, t0 + 0.3, 0.3), "pm")


def door_m(c, x, y, t, t0, w=300, h=520, label=None, open_=0.0, col=BLU):
    """a door in a frame, standing on y; open_ 0..1 swings it (the leaf narrows, the dark gap shows); label written above"""
    k = pr(t, t0, 0.6)
    fr = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
    if open_ > 0: c.drawRect(R.MakeLTRB(x - w / 2, y - h, x + w / 2, y), paint((60, 66, 80), 0.85 * k))
    lw = w * (1 - 0.78 * eo(min(1, open_)))
    leaf = [(x - w / 2, y), (x - w / 2, y - h), (x - w / 2 + lw, y - h + 30 * open_), (x - w / 2 + lw, y - 30 * open_ * 0), (x - w / 2, y)]
    if k > 0.5:
        c.drawPath(_path(leaf), paint(WHITE)); hatch(c, _path(leaf), pr(k, 0.5, 0.5), col, gap=18, w=6, bbox=(x - w / 2, y - h, x + w / 2, y), a=0.35)
    ink(c, [wob(fr, 111, 0.8), wob(leaf, 112, 0.6)], k, MK, 8)
    if k >= 1: c.drawCircle(x - w / 2 + lw - 30, y - h / 2, 12, paint(MK))
    if label: mtext(c, label, x, y - h - 30, 70, MK, pr(t, t0 + 0.5, 0.3), "pm")


def maze_m(c, x, y, t, t0, size=560, n=6, solve_t=None, seed=7):
    """a square maze drawn wall by wall (deterministic depth-first maze); solve_t: a green path from entry to exit draws on"""
    r = _rng(seed); cell = size / n; x0, y0 = x - size / 2, y - size / 2
    seen = [[False] * n for _ in range(n)]; walls = {(i, j, d): True for i in range(n) for j in range(n) for d in "NESW"}
    stack = [(0, 0)]; seen[0][0] = True; parent = {(0, 0): None}
    D = {"N": (0, -1, "S"), "S": (0, 1, "N"), "E": (1, 0, "W"), "W": (-1, 0, "E")}
    while stack:
        i, j = stack[-1]; opts = [(d, i + dx, j + dy, o) for d, (dx, dy, o) in D.items() if 0 <= i + dx < n and 0 <= j + dy < n and not seen[i + dx][j + dy]]
        if not opts: stack.pop(); continue
        d, ni, nj, o = opts[int(r.integers(len(opts)))]; walls[(i, j, d)] = False; walls[(ni, nj, o)] = False
        seen[ni][nj] = True; parent[(ni, nj)] = (i, j); stack.append((ni, nj))
    segs = []
    for i in range(n):
        for j in range(n):
            cx, cy = x0 + i * cell, y0 + j * cell
            if walls[(i, j, "N")] and not (i == 0 and j == 0): segs.append([(cx, cy), (cx + cell, cy)])
            if walls[(i, j, "W")]: segs.append([(cx, cy), (cx, cy + cell)])
            if j == n - 1 and not (i == n - 1): segs.append([(cx, cy + cell), (cx + cell, cy + cell)])
            if i == n - 1: segs.append([(cx + cell, cy), (cx + cell, cy + cell)])
    ink(c, [wob(sg, 120 + q, 0.5, step=30) for q, sg in enumerate(segs)], pr(t, t0, 1.2), MK, 7, pen_=False)
    if solve_t is not None and t >= solve_t:
        node, path = (n - 1, n - 1), []
        while node is not None: path.append((x0 + (node[0] + 0.5) * cell, y0 + (node[1] + 0.5) * cell)); node = parent[node]
        path = path[::-1]; path = [(path[0][0], y0 - 20)] + path + [(path[-1][0], y0 + size + 30)]
        ink(c, [path], pr(t, solve_t, 1.0), GR, 12, pen_=True)


def helmet_m(c, x, y, t, t0, s=1.0, col=RD):
    """a simple Greek (Corinthian-style) helmet, front view: dome, T-shaped face opening, cheek guards, hatched crest on top"""
    k = pr(t, t0, 0.6)
    dome = _sc(x, y, s, [(-110, 120)] + [(px, py) for px, py in circ_pts(0, 0, 115, 180, 360, 30, ry=125)] + [(110, 120), (40, 130), (34, 30),
                                                                                                             (70, 0), (70, -30), (-70, -30), (-70, 0), (-34, 30), (-40, 130), (-110, 120)])
    crest = _sc(x, y, s, [(-100, -110), (-60, -230), (60, -230), (100, -110), (0, -128), (-100, -110)])
    if k > 0.5:
        hatch(c, _path(crest), pr(k, 0.5, 0.5), col, gap=12, w=7, bbox=(x - 110 * s, y - 240 * s, x + 110 * s, y - 100 * s), a=0.85)
        hatch(c, _path(dome), pr(k, 0.6, 0.4), OR, gap=20, w=6, bbox=(x - 120 * s, y - 130 * s, x + 120 * s, y + 140 * s), a=0.4)
    ink(c, [wob(crest, 131, 0.8), wob(dome, 132, 0.8)] + [[(x + px * s, y - 230 * s), (x + px * 1.4 * s, y - 116 * s)] for px in (-30, 0, 30)], k, MK, 7)


GOLD = (236, 176, 40); LIGHT = (150, 156, 170)


# ---------------------------------------------------------------- HOW IT WORKS EP 4 (Prime 'Iliad', 8 Nov 2026): spears, door map, office,
# highlighted memo, courthouse, gavel, money bag, heads, quote card, balance scale, envelope, mailbox, straight hallway, claim form, laptop with a screen callback
def spears_m(c, x, y, t, t0, s=1.0):
    """two crossed spears (an X with leaf tips)"""
    k = pr(t, t0, 0.5)
    for i, (a, b) in enumerate((((-150, 150), (150, -150)), ((150, 150), (-150, -150)))):
        p0 = (x + a[0] * s, y + a[1] * s); p1 = (x + b[0] * s, y + b[1] * s)
        ink(c, [wob([p0, p1], 140 + i, 0.8)], k, (120, 84, 50), 9, pen_=False)
        if k >= 1:
            ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0]); ca, sa = math.cos(ang), math.sin(ang)
            tip = [(p1[0] + 46 * ca * s, p1[1] + 46 * sa * s), (p1[0] - 14 * sa * s, p1[1] + 14 * ca * s), (p1[0] - 10 * ca * s, p1[1] - 10 * sa * s), (p1[0] + 14 * sa * s, p1[1] - 14 * ca * s)]
            c.drawPath(poly(tip, True), paint(LIGHT)); c.drawPath(poly(tip, True), stroke(MK, 4))


def doormap(c, active, fixed=(False, False), a=1.0):
    """mini map under the pill: two small doors IN / OUT; the active one is coloured, a rebuilt one gets a green tick"""
    if a <= 0: return
    for i, (lab, x) in enumerate((("IN", 470), ("OUT", 610))):
        on = (active == i) or active == 2
        w, h = (46, 64) if on else (38, 54); y = 392
        rr = R.MakeXYWH(x - w / 2, y - h, w, h)
        c.drawRect(rr, paint(WHITE, a)); c.drawRect(rr, paint((BLU if i == 0 else RD), (0.35 if on else 0.0) * a))
        c.drawRect(rr, stroke(MK if on else LIGHT, 5 if on else 3, a)); c.drawCircle(x + w / 2 - 10, y - h / 2, 4, paint(MK if on else LIGHT, a))
        f = font("pm", 30 if on else 24); c.drawString(lab, x + w / 2 + 10, y - 12, f, paint(MK if on else LIGHT, a))
        if fixed[i]: ink(c, [[(x - 16, y - 30), (x - 4, y - 16), (x + 22, y - 50)]], 1, GR, 7, pen_=False)


def office_m(c, x, y, t, t0, label="INSIDE AMAZON"):
    k = pr(t, t0, 0.6); w, h = 420, 520
    body = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
    ink(c, [wob(body, 151, 0.8)], k, MK, 8)
    for r_ in range(4):
        for q in range(3):
            kk = pr(t, t0 + 0.4 + (r_ * 3 + q) * 0.03, 0.2)
            if kk > 0:
                bx, by = x - w / 2 + 50 + q * 120, y - h + 60 + r_ * 100
                c.drawRect(R.MakeXYWH(bx, by, 80, 60), paint((255, 236, 170), 0.8 * kk)); c.drawRect(R.MakeXYWH(bx, by, 80, 60), stroke(MK, 4, kk))
    mtext(c, label, x, y - h - 30, 52, MK, pr(t, t0 + 0.5, 0.4), "pm")


def memo_m(c, x, y, t, t0, hl_t, quote="\"a bit of a shady world\"", tilt=-3):
    w, h = 640, 380; k = pr(t, t0, 0.5)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    c.drawRect(R.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), paint((0, 0, 0), 0.10 * k, blur=10)); c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 161, 1.0)], k, MK, 6)
    mtext(c, "INTERNAL", -w / 2 + 40, -h / 2 + 70, 46, LIGHT, pr(t, t0 + 0.3, 0.3), "pm", align="l")
    for i in range(2): ink(c, [[(-w / 2 + 40, -h / 2 + 120 + i * 46), (w / 2 - 60 - i * 90, -h / 2 + 120 + i * 46)]], pr(t, t0 + 0.5 + i * 0.1, 0.25), LIGHT, 7, pen_=False)
    yy = -h / 2 + 250
    if t > hl_t:
        fq = font("kb", 50); wq = tw(fq, quote)
        c.drawRect(R.MakeXYWH(-wq / 2 - 14, yy - 52, (wq + 28) * min(1, pr(t, hl_t, 0.5)), 72), paint((255, 222, 60), 0.8))
    mtext(c, quote, 0, yy, 50, MK, pr(t, t0 + 0.7, 0.6), "kb")
    ink(c, [[(-w / 2 + 40, yy + 70), (w / 2 - 160, yy + 70)]], pr(t, t0 + 0.9, 0.25), LIGHT, 7, pen_=False)
    c.restore()


def court_m(c, x, y, t, t0, label="SEATTLE"):
    k = pr(t, t0, 0.7); w = 560
    roof = [(x - w / 2 - 30, y - 420), (x, y - 560), (x + w / 2 + 30, y - 420), (x - w / 2 - 30, y - 420)]
    steps = [[(x - w / 2 - 40, y), (x + w / 2 + 40, y)], [(x - w / 2 - 20, y - 30), (x + w / 2 + 20, y - 30)]]
    cols = [[(x - w / 2 + 50 + i * 115, y - 30), (x - w / 2 + 50 + i * 115, y - 400)] for i in range(5)]
    beam = [[(x - w / 2 - 10, y - 400), (x + w / 2 + 10, y - 400)]]
    if k > 0.6: hatch(c, _path(roof), pr(k, 0.6, 0.4), GOLD, gap=16, w=6, bbox=(x - w, y - 570, x + w, y - 410), a=0.5)
    ink(c, [wob(roof, 171, 0.8)] + [wob(p, 172 + i, 0.6) for i, p in enumerate(steps + cols + beam)], k, MK, 8)
    mtext(c, label, x, y - 446, 44, MK, pr(t, t0 + 0.6, 0.3), "pm")


def gavel_m(c, x, y, t, t_hit, s=1.0):
    """a gavel that swings down at t_hit (rests raised before)"""
    u = eo(pr(t, t_hit - 0.35, 0.35)); ang = -55 + 55 * u
    c.drawRoundRect(R.MakeXYWH(x - 130, y + 74, 180, 40), 10, 10, paint((150, 100, 60))); c.drawRoundRect(R.MakeXYWH(x - 130, y + 74, 180, 40), 10, 10, stroke(MK, 5))
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-14, -10, 260, 26), 10, 10, paint((150, 100, 60))); c.drawRoundRect(R.MakeXYWH(-14, -10, 260, 26), 10, 10, stroke(MK, 5))
    c.drawRoundRect(R.MakeXYWH(-70, -70, 110, 140), 18, 18, paint((120, 76, 44))); c.drawRoundRect(R.MakeXYWH(-70, -70, 110, 140), 18, 18, stroke(MK, 6))
    c.restore()
    if t > t_hit:
        kb = pr(t, t_hit, 0.3)
        for dx_ in (-1, 1): ink(c, [[(x - 40 + dx_ * 120, y + 80), (x - 40 + dx_ * 170, y + 40)]], kb, MK, 6, pen_=False)


def bag_m(c, x, y, t, t0, text, col=GR, s=1.0, label=None):
    k = pr(t, t0, 0.5)
    body = _sc(x, y, s, [(-90, -150), (-150, -40), (-150, 60), (-100, 120), (100, 120), (150, 60), (150, -40), (90, -150), (-90, -150)])
    neck = _sc(x, y, s, [(-70, -150), (-50, -200), (50, -200), (70, -150)])
    if k > 0.5: hatch(c, _path(body), pr(k, 0.5, 0.5), col, gap=17, w=6, bbox=(x - 160 * s, y - 210 * s, x + 160 * s, y + 130 * s), a=0.45)
    ink(c, [wob(body, 181, 1.0), wob(neck, 182, 0.6)], k, MK, 8)
    mtext(c, text, x, y + 30 * s, int(76 * s), MK, pr(t, t0 + 0.4, 0.3), "pm")
    if label: mtext(c, label, x, y + 200 * s, int(48 * s), col, pr(t, t0 + 0.6, 0.3), "pm")


def heads_m(c, x0, x1, y, t, t0, n=9, col=BLU):
    for i in range(n):
        kk = pop_(t, t0 + i * 0.05)
        if kk <= 0: continue
        hx = x0 + (x1 - x0) * i / (n - 1)
        c.save(); c.translate(hx, y); c.scale(kk, kk)
        c.drawCircle(0, -40, 22, paint(WHITE)); c.drawCircle(0, -40, 22, stroke(MK, 5))
        c.drawPath(_path([(-28, 20), (-22, -10), (22, -10), (28, 20)]), stroke(col, 6)); c.restore()


def quote_m(c, x, y, t, t0, lines_, who):
    w, h = 820, 330; k = pr(t, t0, 0.5)
    if k <= 0: return
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), 30, 30, paint(WHITE, k))
    ink(c, [wob([(x - w / 2 + 30, y - h / 2), (x + w / 2 - 30, y - h / 2), (x + w / 2, y - h / 2 + 30), (x + w / 2, y + h / 2 - 30), (x + w / 2 - 30, y + h / 2),
                 (x - w / 2 + 30, y + h / 2), (x - w / 2, y + h / 2 - 30), (x - w / 2, y - h / 2 + 30), (x - w / 2 + 30, y - h / 2)], 191, 0.8)], k, BLU, 7)
    mtext(c, "“", x - w / 2 + 60, y - h / 2 + 110, 120, BLU, k, "pm")
    for i, ln in enumerate(lines_): mtext(c, ln, x + 20, y - 50 + i * 70, 54, MK, pr(t, t0 + 0.2 + i * 0.25, 0.3), "kb")
    mtext(c, who, x, y + h / 2 - 40, 40, BLU, pr(t, t0 + 0.7, 0.3), "pm")


def scale_m(c, x, y, t, t0, tilt=0.0):
    k = pr(t, t0, 0.5)
    ink(c, [wob([(x, y), (x, y - 260)], 201, 0.5), wob([(x - 90, y), (x + 90, y)], 202, 0.5)], k, MK, 8)
    if k < 1: return
    a = math.radians(tilt); L = 200
    lx, ly = x - L * math.cos(a), y - 260 - L * math.sin(a); rx, ry = x + L * math.cos(a), y - 260 + L * math.sin(a)
    c.drawPath(_path([(lx, ly), (rx, ry)]), stroke(MK, 8)); c.drawCircle(x, y - 260, 12, paint(MK))
    for px, py in ((lx, ly), (rx, ry)):
        c.drawPath(_path([(px, py), (px - 60, py + 110)]), stroke(MK, 4)); c.drawPath(_path([(px, py), (px + 60, py + 110)]), stroke(MK, 4))
        c.drawPath(_path(circ_pts(px, py + 110, 70, 0, 180, 16, ry=26)), stroke(MK, 6))


def envelope_m(c, x, y, t, t0, s=1.0, text="$"):
    k = pr(t, t0, 0.4); w, h = 260 * s, 170 * s
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 211, 0.6),
            [(x - w / 2, y - h / 2), (x, y + 10 * s), (x + w / 2, y - h / 2)]], k, MK, 6, pen_=False)
    mtext(c, text, x, y + 60 * s, int(56 * s), GR, k, "pm")


def mailbox_m(c, x, y, t, t0, flag=0.0):
    k = pr(t, t0, 0.5)
    box = [(x - 130, y - 300), (x + 130, y - 300), (x + 130, y - 160), (x - 130, y - 160)]
    ink(c, [wob([(x, y), (x, y - 160)], 221, 0.5), wob(box + [box[0]], 222, 0.6), wob(circ_pts(x, y - 300, 130, 180, 360, 18, ry=60), 223, 0.6)], k, MK, 8)
    if k >= 1:
        hatch(c, _path(box + [box[0]]), 1, BLU, gap=18, w=6, bbox=(x - 140, y - 310, x + 140, y - 150), a=0.3)
        a = math.radians(-90 * flag); fx, fy = x + 130, y - 220
        c.drawPath(_path([(fx, fy), (fx + 110 * math.cos(a), fy + 110 * math.sin(a))]), stroke(RD, 10))
        c.drawRect(R.MakeXYWH(fx + 110 * math.cos(a) - 18, fy + 110 * math.sin(a) - 18, 36, 36), paint(RD))


def hallway_m(c, x, y, t, t0, w=300, h=520):
    """the OUT door redrawn as a short straight hallway with EXIT at the end"""
    k = pr(t, t0, 0.6)
    fr = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
    inner = [(x - 50, y - 180), (x - 50, y - 340), (x + 50, y - 340), (x + 50, y - 180), (x - 50, y - 180)]
    lines_ = [[(x - w / 2, y - h), (x - 50, y - 340)], [(x + w / 2, y - h), (x + 50, y - 340)], [(x - w / 2, y), (x - 50, y - 180)], [(x + w / 2, y), (x + 50, y - 180)]]
    ink(c, [wob(fr, 231, 0.8), wob(inner, 232, 0.5)] + lines_, k, MK, 7)
    if k >= 1:
        c.drawRect(R.MakeXYWH(x - 50, y - 340, 100, 160), paint(GR, 0.3)); mtext(c, "EXIT", x, y - 250, 34, GR, 1, "pm")
        ink(c, [[(x, y - 30), (x, y - 160)], [(x - 22, y - 136), (x, y - 166), (x + 22, y - 136)]], pr(t, t0 + 0.6, 0.3), GR, 8, pen_=False)


def form_m(c, x, y, t, t0, cross_t=None):
    w, h = 260, 320; k = pr(t, t0, 0.4)
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 241, 0.6)], k, MK, 6, pen_=False)
    mtext(c, "CLAIM FORM", x, y - h / 2 + 56, 34, MK, k, "pm")
    for i in range(4):
        yy = y - h / 2 + 110 + i * 50
        c.drawRect(R.MakeXYWH(x - w / 2 + 30, yy - 14, 24, 24), stroke(MK, 3, k)); ink(c, [[(x - w / 2 + 70, yy), (x + w / 2 - 30, yy)]], k, LIGHT, 5, pen_=False)
    if cross_t is not None and t > cross_t:
        cross(c, x - w / 2 - 20, y - h / 2 - 20, x + w / 2 + 20, y + h / 2 + 20, pr(t, cross_t, 0.2), RD, 14, 3)
        cross(c, x + w / 2 + 20, y - h / 2 - 20, x - w / 2 - 20, y + h / 2 + 20, pr(t, cross_t + 0.15, 0.2), RD, 14, 4)


def laptop2(c, x, y, t, t0, w=440, h=290, screen=None):
    k = pr(t, t0, 0.5)
    scr = [(x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y), (x - w / 2, y - h)]
    base = [(x - w / 2 - 50, y + 10), (x + w / 2 + 50, y + 10), (x + w / 2 + 20, y + 44), (x - w / 2 - 20, y + 44), (x - w / 2 - 50, y + 10)]
    c.drawPath(_path(scr), paint(WHITE, k)); ink(c, [wob(scr, 251, 0.8), wob(base, 252, 0.8)], k, MK, 7)
    if screen and k >= 1: screen(c, x, y - h / 2)


# ---------------------------------------------------------------- 8 Nov 2026 R&D writers' room: dropshipping (EP 17) + cash rewards (EP 18) props
def parcel_m(c, x, y, t, t0, s=1.0, label=None, label_t=None, label_col=RD, open_=0.0):
    """a cardboard shipping box (3/4 view) with packing tape and a white label; `label` writes on at label_t; open_ 0..1 lifts the flaps"""
    k = pr(t, t0, 0.6)
    if k <= 0: return
    w, h, d = 300 * s, 210 * s, 90 * s
    front = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
    top = [(x - w / 2, y - h / 2), (x - w / 2 + d, y - h / 2 - d * 0.6), (x + w / 2 + d, y - h / 2 - d * 0.6), (x + w / 2, y - h / 2)]
    side = [(x + w / 2, y - h / 2), (x + w / 2 + d, y - h / 2 - d * 0.6), (x + w / 2 + d, y + h / 2 - d * 0.6), (x + w / 2, y + h / 2)]
    c.drawPath(_path(front), paint(WHITE, k))
    if k > 0.5:
        hatch(c, _path(front), pr(k, 0.5, 0.5), CARD_BOARD, gap=17, w=6, bbox=(x - w / 2, y - h / 2, x + w / 2, y + h / 2), a=0.7)
        hatch(c, _path(side + [side[0]]), pr(k, 0.5, 0.5), CARD_BOARD, gap=12, w=6, bbox=(x + w / 2, y - h / 2 - d, x + w / 2 + d, y + h / 2), a=0.95)
    tape = [(x - 18 * s, y - h / 2), (x - 18 * s + d, y - h / 2 - d * 0.6)]
    ink(c, [wob(front, 301, 0.9), wob(top, 302, 0.7), wob(side, 303, 0.7), tape, [(x - 18 * s, y - h / 2), (x - 18 * s, y - h / 2 + 50 * s)]], k, MK, 7)
    if open_ > 0 and k >= 1:
        ink(c, [[(x - w / 2, y - h / 2), (x - w / 2 - 40 * s, y - h / 2 - 120 * s * open_)], [(x + w / 2, y - h / 2), (x + w / 2 + 50 * s, y - h / 2 - 120 * s * open_)]], 1, MK, 6, pen_=False)
    if k >= 1:   # the label (always drawn white; text optional)
        lb = R.MakeXYWH(x - 120 * s, y - 10 * s, 200 * s, 92 * s); c.drawRoundRect(lb, 8, 8, paint(WHITE)); c.drawRoundRect(lb, 8, 8, stroke(MK, 4))
        if label and (label_t is None or t >= label_t):
            sz = int(52 * s); f = font("pm", sz)
            while tw(f, label) > 180 * s and sz > 20: sz -= 2; f = font("pm", sz)
            mtext(c, label, x - 20 * s, y + 52 * s, sz, label_col, pr(t, label_t if label_t is not None else t0 + 0.6, 0.35), "pm")


def lamp_m(c, x, y, t, t0, s=1.0, on=0.0, col=OR):
    """a desk lamp (base, two arm segments, cone shade); on 0..1 = a soft light cone under the shade"""
    k = pr(t, t0, 0.55)
    if k <= 0: return
    P = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    base = P([(-80, 0), (80, 0), (60, -24), (-60, -24), (-80, 0)])
    arm = P([(0, -24), (-50, -150), (40, -250)])
    shade = P([(40, -250), (150, -210), (100, -150), (40, -250)])
    if k >= 1 and on > 0:
        cone = _path(P([(125, -180), (230, 0), (40, 0), (110, -165)])); c.drawPath(cone, paint((255, 214, 90), 0.35 * on, blur=8))
    c.drawPath(_path(shade), paint(WHITE, k))
    if k > 0.6: hatch(c, _path(shade), pr(k, 0.6, 0.4), col, gap=14, w=6, bbox=(x + 30 * s, y - 260 * s, x + 160 * s, y - 140 * s), a=0.85)
    ink(c, [wob(base, 311, 0.6), wob(arm, 312, 0.6), wob(shade, 313, 0.6)], k, MK, 7)
    if k >= 1: c.drawCircle(x - 50 * s, y - 150 * s, 9 * s, paint(MK)); c.drawCircle(x + 40 * s, y - 250 * s, 9 * s, paint(MK))


def ship_m(c, x, y, t, t0, s=1.0, label="SUPPLIER", bob=True):
    """a small cargo ship on a wavy water line with three stacked containers; bobs gently"""
    k = pr(t, t0, 0.7)
    if k <= 0: return
    dy = 6 * math.sin(t * 2.2) * s if bob and k >= 1 else 0
    P = lambda pts: [(x + px * s, y + dy + py * s) for px, py in pts]
    hull = P([(-220, -40), (220, -40), (170, 40), (-190, 40), (-220, -40)])
    bridge = P([(-190, -40), (-190, -130), (-120, -130), (-120, -40)])
    c.drawPath(_path(hull), paint(WHITE, k))
    if k > 0.5: hatch(c, _path(hull), pr(k, 0.5, 0.5), BLU, gap=15, w=6, bbox=(x - 230 * s, y + dy - 50 * s, x + 230 * s, y + dy + 50 * s), a=0.55)
    boxes = []
    for i, (bx, by, bc) in enumerate(((-90, -40, RD), (0, -40, GR), (90, -40, OR), (-45, -100, BLU), (45, -100, RD))):
        bp = P([(bx - 42, by), (bx - 42, by - 58), (bx + 42, by - 58), (bx + 42, by), (bx - 42, by)]); boxes.append(wob(bp, 330 + i, 0.4))
        if k > 0.7: hatch(c, _path(bp), pr(k, 0.7, 0.3), bc, gap=12, w=5, bbox=(x + (bx - 45) * s, y + dy + (by - 60) * s, x + (bx + 45) * s, y + dy + by * s), a=0.6)
    waves = [wob([(x + (-260 + i * 40) * s, y + 44 * s + (8 if i % 2 else -4) * s) for i in range(14)], 340, 0.3)]
    ink(c, [wob(hull, 321, 0.7), wob(bridge, 322, 0.6)] + boxes, k, MK, 6)
    ink(c, waves, k, BLU, 6, pen_=False)
    if label and k >= 1: mtext(c, label, x, y + dy + 120 * s, int(46 * s), MK, pr(t, t0 + 0.7, 0.3), "kb")


def giftcard_m(c, x, y, t, t0, s=1.0, label="GIFT CARD", col=PU, tilt=-6, cross_t=None):
    """a gift card with a ribbon bow and a handwritten label; cross_t: red X over it"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    w, h = 300 * s, 190 * s
    c.save(); c.translate(x, y); c.rotate(tilt)
    body = skia.Path(); body.addRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), 20 * s, 20 * s)
    c.drawPath(body, paint(WHITE, k)); hatch(c, body, k, col, gap=16, w=6, bbox=(-w / 2, -h / 2, w / 2, h / 2), a=0.35)
    c.drawPath(body, stroke(MK, 6, k))
    c.drawRect(R.MakeXYWH(-w / 2 + 28 * s, -h / 2, 18 * s, h), paint(RD, k))
    for sx in (-1, 1): c.drawOval(R.MakeXYWH(-w / 2 + 37 * s + (sx * 34 - 17) * s, -h / 2 - 20 * s, 34 * s, 26 * s), stroke(RD, 6, k))
    sz = int(40 * s); f = font("pm", sz)
    while tw(f, label) > w - 110 * s and sz > 18: sz -= 2; f = font("pm", sz)
    mtext(c, label, 24 * s, 14 * s, sz, MK, pr(t, t0 + 0.3, 0.35), "pm")
    c.restore()
    if cross_t is not None and t > cross_t:
        cross(c, x - w / 2 - 20, y - h / 2 - 20, x + w / 2 + 20, y + h / 2 + 20, pr(t, cross_t, 0.2), RD, 14, 3)
        cross(c, x + w / 2 + 20, y - h / 2 - 20, x - w / 2 - 20, y + h / 2 + 20, pr(t, cross_t + 0.15, 0.2), RD, 14, 4)


def cup_m(c, x, y, t, t0, s=1.0, steam=True, col=OR):
    """a takeaway coffee cup with lid and sleeve; steam curls wiggle"""
    k = pr(t, t0, 0.55)
    if k <= 0: return
    P = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    body = P([(-80, -200), (80, -200), (62, 0), (-62, 0), (-80, -200)])
    lid = P([(-92, -200), (92, -200), (86, -232), (-86, -232), (-92, -200)])
    sleeve = P([(-76, -150), (76, -150), (70, -70), (-70, -70), (-76, -150)])
    c.drawPath(_path(body), paint(WHITE, k))
    if k > 0.5: hatch(c, _path(sleeve), pr(k, 0.5, 0.5), col, gap=13, w=6, bbox=(x - 80 * s, y - 155 * s, x + 80 * s, y - 65 * s), a=0.85)
    ink(c, [wob(body, 351, 0.6), wob(lid, 352, 0.5), wob(sleeve, 353, 0.5)], k, MK, 7)
    if steam and k >= 1:
        for i, sx in enumerate((-30, 10, 45)):
            ph = t * 2.4 + i
            pts = [(x + (sx + 12 * math.sin(ph + j * 0.9)) * s, y + (-250 - j * 22) * s) for j in range(6)]
            ink(c, [pts], 1, GHOST if i % 2 else (190, 196, 206), 6, pen_=False)


def cash_m(c, x, y, t, t0, s=1.0, text="$5", tilt=-5, n=1):
    """a banknote (or a small fanned stack of n): green hatched note, oval centre, value in the corners"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    w, h = 300 * s, 140 * s
    for i in range(n - 1, -1, -1):
        c.save(); c.translate(x + i * 16 * s, y - i * 12 * s); c.rotate(tilt + i * 4)
        body = skia.Path(); body.addRect(R.MakeXYWH(-w / 2, -h / 2, w, h))
        c.drawPath(body, paint(WHITE, k)); hatch(c, body, k, GR, gap=15, w=6, bbox=(-w / 2, -h / 2, w / 2, h / 2), a=0.45)
        c.drawPath(body, stroke(MK, 6, k)); c.drawOval(R.MakeXYWH(-46 * s, -46 * s, 92 * s, 92 * s), stroke(MK, 5, k))
        if i == 0:
            mtext(c, text, 0, 22 * s, int(54 * s), GR, pr(t, t0 + 0.3, 0.3), "pm")
            for cx_, cy_ in ((-w / 2 + 34 * s, -h / 2 + 40 * s), (w / 2 - 34 * s, h / 2 - 14 * s)):
                mtext(c, text.strip("$£€") or "$", cx_, cy_, int(28 * s), MK, k, "pm")
        c.restore()


def wallet_m(c, x, y, t, t0, s=1.0, empty=False, col=(150, 96, 52)):
    """a folded wallet; empty=True shows the open pocket with a written 0"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: [(x + px * s, y + py * s) for px, py in pts]
    body = P([(-150, -95), (150, -95), (150, 95), (-150, 95), (-150, -95)])
    flap = P([(150, -40), (40, -40), (40, 40), (150, 40)])
    c.drawPath(_path(body), paint(WHITE, k))
    if k > 0.5: hatch(c, _path(body), pr(k, 0.5, 0.5), col, gap=16, w=6, bbox=(x - 150 * s, y - 95 * s, x + 150 * s, y + 95 * s), a=0.6)
    ink(c, [wob(body, 361, 0.7), wob(flap, 362, 0.5)], k, MK, 7)
    if k >= 1: c.drawCircle(x + 70 * s, y, 10 * s, paint(MK))
    if empty and k >= 1:
        ink(c, [wob(P([(-150, -95), (-110, -150), (110, -150), (150, -95)]), 363, 0.5)], pr(t, t0 + 0.5, 0.3), MK, 6, pen_=False)
        mtext(c, "0", x - 40 * s, y + 30 * s, int(110 * s), RD, pr(t, t0 + 0.7, 0.3), "pm")


# ---------------------------------------------------------------- HOW TO START EP 8 (dropshipping 30-day rule, 9 Nov 2026)
# stepmap = generalised door map (n numbered parcels under the pill); relabel = rub out + rewrite the held parcel's label;
# grid30_m = a 30-day month; strip_m = day boxes that fill; gov_m, stopwatch_m, snail_m, tagpill_m, store_page, dash_line.
PINK = (236, 92, 150)


def stepmap(c, n, active, done=(), a=1.0, x0=None, y=392, labels=None):
    """mini map under the pill: n small numbered parcels; the active one coloured + bigger, finished ones ticked"""
    if a <= 0: return
    gap = 120; x0 = x0 if x0 is not None else 510 - gap * (n - 1) / 2
    for i in range(n):
        x = x0 + i * gap; on = (i == active)
        w, h = (78, 56) if on else (62, 44)
        rr = R.MakeXYWH(x - w / 2, y - h, w, h)
        c.drawRect(rr, paint(WHITE, a))
        if on: c.drawRect(rr, paint(CARD_BOARD, 0.85 * a))
        c.drawRect(rr, stroke(MK if on else LIGHT, 5 if on else 3, a))
        c.drawLine(x, y - h, x, y - h + 14, stroke(MK if on else LIGHT, 3, a))
        mtext(c, str(i + 1), x, y - h * 0.22, 38 if on else 30, RD if on else LIGHT, a, "pm")
        if i in done: ink(c, [[(x - 20, y - 70), (x - 6, y - 56), (x + 24, y - 92)]], 1, GR, 7, pen_=False)


def gov_m(c, x, y, t, t0, label="FTC", sign="CONSUMER WATCHDOG", s=1.0):
    k = pr(t, t0, 0.7); w = 440 * s
    roof = [(x - w / 2 - 30 * s, y - 330 * s), (x, y - 440 * s), (x + w / 2 + 30 * s, y - 330 * s), (x - w / 2 - 30 * s, y - 330 * s)]
    steps = [[(x - w / 2 - 40 * s, y), (x + w / 2 + 40 * s, y)], [(x - w / 2 - 20 * s, y - 26 * s), (x + w / 2 + 20 * s, y - 26 * s)]]
    cols = [[(x - w / 2 + 40 * s + i * 90 * s, y - 26 * s), (x - w / 2 + 40 * s + i * 90 * s, y - 312 * s)] for i in range(5)]
    beam = [[(x - w / 2 - 10 * s, y - 312 * s), (x + w / 2 + 10 * s, y - 312 * s)]]
    if k > 0.6: hatch(c, _path(roof), pr(k, 0.6, 0.4), BLU, gap=16, w=6, bbox=(x - w, y - 450 * s, x + w, y - 320 * s), a=0.4)
    ink(c, [wob(roof, 401, 0.8)] + [wob(p, 402 + i, 0.6) for i, p in enumerate(steps + cols + beam)], k, MK, 8)
    mtext(c, label, x, y - 350 * s, int(54 * s), MK, pr(t, t0 + 0.6, 0.3), "pm")
    if sign:
        ks = pr(t, t0 + 0.8, 0.3)
        if ks > 0:
            f = font("pm", int(30 * s)); sw = tw(f, sign) + 40
            c.drawRoundRect(R.MakeXYWH(x - sw / 2, y + 24 * s, sw, 54 * s), 10, 10, paint(WHITE, ks)); c.drawRoundRect(R.MakeXYWH(x - sw / 2, y + 24 * s, sw, 54 * s), 10, 10, stroke(BLU, 5, ks))
            mtext(c, sign, x, y + 62 * s, int(30 * s), BLU, ks, "pm")


def stopwatch_m(c, x, y, t, t0, r=90, run_t=None, stop_t=None, col=RD):
    """a stopwatch; the hand sweeps from run_t until stop_t"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, r, -90, 270, 40), 411, 0.6), [(x - 18, y - r - 26), (x + 18, y - r - 26)], [(x, y - r), (x, y - r - 26)]], k, MK, 7)
    if k < 1: return
    for i in range(12):
        a_ = math.radians(i * 30); c.drawLine(x + 0.78 * r * math.sin(a_), y - 0.78 * r * math.cos(a_), x + 0.9 * r * math.sin(a_), y - 0.9 * r * math.cos(a_), stroke(MK, 3))
    el = 0.0
    if run_t is not None and t > run_t: el = (min(t, stop_t) if stop_t else t) - run_t
    a_ = math.radians(el * 140)
    c.drawLine(x, y, x + 0.72 * r * math.sin(a_), y - 0.72 * r * math.cos(a_), stroke(col, 7)); c.drawCircle(x, y, 8, paint(col))


def snail_m(c, x, y, t, t0, s=1.0):
    k = pr(t, t0, 0.5)
    if k <= 0: return
    sp = [(x + (14 + 4.2 * a_ / 30) * s * math.cos(math.radians(a_)), y - 60 * s + (14 + 4.2 * a_ / 30) * s * math.sin(math.radians(a_))) for a_ in range(0, 720, 20)]
    body = [(x - 90 * s, y), (x + 90 * s, y), (x + 120 * s, y - 30 * s), (x + 96 * s, y - 40 * s)]
    if k >= 1: c.drawCircle(x, y - 60 * s, 62 * s, paint(GOLD, 0.45))
    ink(c, [wob(body, 421, 0.6), sp, wob(circ_pts(x, y - 60 * s, 62 * s, -90, 270, 30), 422, 0.6), [(x + 104 * s, y - 36 * s), (x + 120 * s, y - 90 * s)], [(x + 90 * s, y - 36 * s), (x + 96 * s, y - 92 * s)]], k, MK, 6)
    if k >= 1: c.drawCircle(x + 120 * s, y - 94 * s, 6 * s, paint(MK)); c.drawCircle(x + 96 * s, y - 96 * s, 6 * s, paint(MK))


def strip_m(c, x, y, n, t, t0, fill_t=None, step=0.12, cell=None, col=GR, label=None, lab_col=MK, mark_last=None):
    """a row of n day-boxes; from fill_t they fill one by one; mark_last = text on the last box"""
    cell = cell or min(96, 880 / n); x0 = x - cell * n / 2
    k = pr(t, t0, 0.5)
    grid = [[(x0, y), (x0 + cell * n, y), (x0 + cell * n, y + cell), (x0, y + cell), (x0, y)]] + [[(x0 + cell * i, y), (x0 + cell * i, y + cell)] for i in range(1, n)]
    ink(c, [wob(g, 430 + i, 0.4) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    if fill_t is not None and t > fill_t and k >= 1:
        m_ = min(n, int((t - fill_t) / step) + 1)
        for i in range(m_):
            ki = pr(t, fill_t + i * step, 0.12)
            c.drawRect(R.MakeXYWH(x0 + cell * i + 6, y + 6, (cell - 12) * ki, cell - 12), paint(col, 0.55))
            mtext(c, str(i + 1), x0 + cell * (i + 0.5), y + cell * 0.66, int(cell * 0.42), MK, ki, "kb")
    if label: mtext(c, label, x, y + cell + 64, 44, lab_col, pr(t, t0 + 0.4, 0.3), "pm")


def tagpill_m(c, x, y, text, k, col=BLU, size=46, fill=False):
    if k <= 0: return
    f = font("pm", size); w = tw(f, text) + 56; h = size * 1.55
    c.save(); c.translate(x, y); s = eback(min(1, k), 1.7); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, paint(col if fill else WHITE, 0.95))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -h / 2, w, h), h / 2, h / 2, stroke(col, 7))
    c.drawString(text, -tw(f, text) / 2, size * 0.36, f, paint(WHITE if fill else col)); c.restore()


def relabel(c, x, y, t, t0, old, new, t_sw, s=1.0, old_col=RD, new_col=RD, open_=0.0):
    """the held parcel: its label reads `old`; at t_sw a tiny eraser rubs it out (0.35 s) and `new` is written on"""
    if t < t_sw:
        parcel_m(c, x, y, t, t0, s, label=old, label_t=None if old else None, label_col=old_col, open_=open_)
        return
    parcel_m(c, x, y, t, t0, s, label=None, open_=open_)
    u = pr(t, t_sw, 0.35)
    lb_x, lb_y = x - 120 * s, y - 10 * s
    if u < 1 and old:   # the old word fades under the eraser's strokes
        mtext(c, old, x - 20 * s, y + 52 * s, int(40 * s), old_col, 1, "pm", a=1 - u)
        ex = lb_x + 200 * s * (0.5 + 0.5 * math.sin(u * 9))
        c.drawRoundRect(R.MakeXYWH(ex - 28 * s, lb_y + 10 * s, 56 * s, 70 * s), 8, 8, paint((60, 66, 84)))
        c.drawRect(R.MakeXYWH(ex - 28 * s, lb_y + 66 * s, 56 * s, 14 * s), paint((210, 210, 214)))
    else:
        parcel_m(c, x, y, t, t0, s, label=new, label_t=t_sw + 0.35, label_col=new_col, open_=open_)


def store_page(c, x, y, t, t0, line=None, line_t=None, line_col=GR, strike_t=None):
    """laptop with a tiny shop page: a lamp photo, a price, and one shipping line that can be written / struck through"""
    def scr(c_, cx, cy):
        lamp_m(c_, cx - 150, cy + 110, t, t0 + 0.3, 0.45)
        mtext(c_, "MY STORE", cx + 60, cy - 70, 40, MK, pr(t, t0 + 0.4, 0.3), "pm")
        mtext(c_, "$39", cx + 80, cy, 46, BLU, pr(t, t0 + 0.6, 0.3), "pm")
        if line and line_t is not None and t > line_t:
            mtext(c_, line, cx + 70, cy + 76, 34, line_col, pr(t, line_t, 0.4), "pm")
            if strike_t is not None and t > strike_t:
                ink(c_, [[(cx - 30, cy + 64), (cx + 180, cy + 60)]], pr(t, strike_t, 0.2), RD, 8, pen_=False)
    laptop2(c, x, y, t, t0, w=460, h=300, screen=scr)


def grid30_m(c, x, y, t, t0, fill_t=None, step=0.07, upto=0, hl=None, cw=128, ch=78):
    """a 30-day month (6 x 5 boxes): days count on from fill_t (or `upto` days already written); hl = time day 30 gets circled red"""
    x0 = x - cw * 3; k = pr(t, t0, 0.6)
    grid = [[(x0, y), (x0 + cw * 6, y), (x0 + cw * 6, y + ch * 5), (x0, y + ch * 5), (x0, y)]]
    grid += [[(x0 + cw * i, y), (x0 + cw * i, y + ch * 5)] for i in range(1, 6)] + [[(x0, y + ch * j), (x0 + cw * 6, y + ch * j)] for j in range(1, 5)]
    ink(c, [wob(g, i + 470, 0.5) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    if k < 1: return
    m_ = upto
    if fill_t is not None and t > fill_t: m_ = max(m_, min(30, int((t - fill_t) / max(step, 1e-3)) + 1))
    for d in range(m_):
        i, j = d % 6, d // 6
        mtext(c, str(d + 1), x0 + cw * (i + 0.5), y + ch * (j + 0.5) + 14, 38, (BLU if d < 29 else RD) if upto == 0 else LIGHT, 1, "kb")
    if hl is not None and t > hl - 0.05:
        cx, cy = x0 + cw * 5.5, y + ch * 4.5
        c.drawRect(R.MakeXYWH(cx - cw / 2 + 4, cy - ch / 2 + 4, cw - 8, ch - 8), paint(RD, 0.15 * pr(t, hl, 0.3)))
        ink(c, [wob(circ_pts(cx, cy, 64, -150, 215, 30, ry=44), 12, 1.0)], pr(t, hl, 0.35), RD, 9, pen_=False)
        mtext(c, "30", cx, cy + 16, 48, RD, pr(t, hl + 0.1, 0.25), "pm")


def dash_line(c, a, b, prog, col=MK, w=7):
    if prog <= 0: return
    n = 14; (x0, y0), (x1, y1) = a, b
    for i in range(int(n * prog)):
        u0, u1 = i / n, (i + 0.55) / n
        c.drawLine(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0, x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1, stroke(col, w))


# ---- R&D writers' room 9 Nov 2026: props for B6 Netflix 2011 (queue/19) + T8 childminding (queue/20) ----
def disc_m(c, x, y, t, t0, r=110, label=None, col=RD, spin=0.0):
    """a DVD-style disc: outer ring, hub, a hatched label band; spin = degrees/s for the shine tick"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, r, -90, 270, 48), 501, 0.6), wob(circ_pts(x, y, r * 0.22, -90, 270, 20), 502, 0.3)], k, MK, 7)
    if k < 1: return
    c.drawCircle(x, y, r * 0.09, paint(MK))
    a_ = math.radians(30 + spin * max(0.0, t - t0))
    for d_ in (0.0, 0.18):
        c.drawLine(x + r * 0.42 * math.cos(a_ + d_), y + r * 0.42 * math.sin(a_ + d_), x + r * 0.82 * math.cos(a_ + d_), y + r * 0.82 * math.sin(a_ + d_), stroke(LIGHT, 5))
    if label: mtext(c, label, x, y + r + 58, 44, col, pr(t, t0 + 0.35, 0.3), "pm")


def tv_m(c, x, y, t, t0, w=420, h=260, play=True, col=RD, text=None):
    """a flat screen on a small stand; a play triangle (or `text`) drawn in the middle"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    x0, y0 = x - w / 2, y - h / 2
    ink(c, [wob([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], 511, 0.6),
            [(x - 40, y0 + h), (x - 60, y0 + h + 44), (x + 60, y0 + h + 44), (x + 40, y0 + h)]], k, MK, 7)
    if k < 1: return
    k2 = pr(t, t0 + 0.4, 0.35)
    if play:
        tri = [(x - 38, y - 50), (x + 52, y), (x - 38, y + 50), (x - 38, y - 50)]
        p = skia.Path(); p.addPoly([skia.Point(*q) for q in tri], True)
        hatch(c, p, k2, col, gap=12, w=6, bbox=(x - 60, y - 70, x + 70, y + 70), seed=513)
        ink(c, [wob(tri, 512, 0.4)], k2, col, 7, pen_=False)
    if text: mtext(c, text, x, y + 18, 56, col, k2, "pm")


def clock_m(c, x, y, t, t0, r=120, h0=15.0, hours=2.0, fill_t=None, col=RD, label=None):
    """a wall clock; from fill_t a wedge sweeps from hour h0 for `hours` hours (the 'two-hour line'), hand follows"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, r, -90, 270, 48), 521, 0.7)], k, MK, 8)
    if k < 1: return
    for i in range(12):
        a_ = math.radians(i * 30); L = 0.14 if i % 3 == 0 else 0.08
        c.drawLine(x + (0.92 - L) * r * math.sin(a_), y - (0.92 - L) * r * math.cos(a_), x + 0.92 * r * math.sin(a_), y - 0.92 * r * math.cos(a_), stroke(MK, 4))
    u = 0.0
    if fill_t is not None and t > fill_t: u = min(1.0, (t - fill_t) / 1.6)
    a0 = (h0 % 12) * 30 - 90; sweep = hours * 30 * u
    if u > 0:
        p = skia.Path(); p.moveTo(x, y); p.arcTo(R.MakeXYWH(x - 0.86 * r, y - 0.86 * r, 1.72 * r, 1.72 * r), a0, sweep, False); p.close()
        c.drawPath(p, paint(col, 0.28))
    am = math.radians(a0 + 90 + sweep)
    c.drawLine(x, y, x + 0.62 * r * math.sin(am), y - 0.62 * r * math.cos(am), stroke(MK, 8))
    c.drawLine(x, y, x, y - 0.82 * r, stroke(MK, 5)); c.drawCircle(x, y, 9, paint(col))
    if label: mtext(c, label, x, y + r + 62, 46, col, pr(t, t0 + 0.4, 0.3), "pm")


def firstaid_m(c, x, y, t, t0, s=1.0, col=GR, label=None):
    """a first-aid box with a handle and a cross"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    w, h = 220 * s, 150 * s; x0, y0 = x - w / 2, y - h / 2
    ink(c, [wob([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], 531, 0.6),
            [(x - 40 * s, y0), (x - 40 * s, y0 - 26 * s), (x + 40 * s, y0 - 26 * s), (x + 40 * s, y0)]], k, MK, 7)
    if k < 1: return
    a, b = 18 * s, 50 * s
    cr = [(x - a, y - b), (x + a, y - b), (x + a, y - a), (x + b, y - a), (x + b, y + a), (x + a, y + a), (x + a, y + b),
          (x - a, y + b), (x - a, y + a), (x - b, y + a), (x - b, y - a), (x - a, y - a), (x - a, y - b)]
    p = skia.Path(); p.addPoly([skia.Point(*q) for q in cr], True)
    k2 = pr(t, t0 + 0.35, 0.35)
    hatch(c, p, k2, col, gap=11, w=6, bbox=(x - b - 4, y - b - 4, x + b + 4, y + b + 4), seed=532)
    ink(c, [wob(cr, 533, 0.3)], k2, col, 6, pen_=False)
    if label: mtext(c, label, x, y + h / 2 + 60, 44, col, pr(t, t0 + 0.5, 0.3), "pm")

# ---------------------------------------------------------------- same-cart props (HOW IT WORKS EP 5, examples/same-cart, 10 Nov 2026): shop front with striped awning, a hand from the top with a word on its cuff, a growing till receipt, newspaper, location pin, sticky note, plain state shape (ny_m: no map data), falling coin pile, and the QUESTION MAP (qmap: the hook's two questions as pills under the brand pill, current coloured, answered ticked)
YEL = (255, 232, 110)


def shopfront_m(c, x, y, t, t0, s=1.0, label="STORE", col=RD):
    """a small shop front: striped awning (hatched), window, door; label written on the sign"""
    k = pr(t, t0, 0.6); w, h = 360 * s, 300 * s
    body = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y)]
    awn = [(x - w / 2 - 20 * s, y - h), (x + w / 2 + 20 * s, y - h), (x + w / 2, y - h + 70 * s), (x - w / 2, y - h + 70 * s), (x - w / 2 - 20 * s, y - h)]
    sign = [(x - w / 2 + 20 * s, y - h - 90 * s), (x + w / 2 - 20 * s, y - h - 90 * s), (x + w / 2 - 20 * s, y - h - 10 * s), (x - w / 2 + 20 * s, y - h - 10 * s), (x - w / 2 + 20 * s, y - h - 90 * s)]
    door = [(x + 40 * s, y), (x + 40 * s, y - 170 * s), (x + 130 * s, y - 170 * s), (x + 130 * s, y)]
    win = [(x - 140 * s, y - 70 * s), (x - 140 * s, y - 190 * s), (x - 10 * s, y - 190 * s), (x - 10 * s, y - 70 * s), (x - 140 * s, y - 70 * s)]
    if k > 0.6:
        c.save(); c.clipPath(_path(awn))
        for i in range(9):
            if i % 2 == 0: c.drawRect(R.MakeXYWH(x - w / 2 - 20 * s + i * 45 * s, y - h, 45 * s, 70 * s), paint(col, 0.55 * pr(k, 0.6, 0.4)))
        c.restore()
    ink(c, [wob(body, 501, 0.8), wob(awn, 502, 0.8), wob(sign, 503, 0.6), wob(door, 504, 0.6), wob(win, 505, 0.6)], k, MK, 7)
    if label: mtext(c, label, x, y - h - 34 * s, int(48 * s), MK, pr(t, t0 + 0.5, 0.3), "pm")


def hand_m(c, x, y, t, t0, word=None, col=BLU, reach=1.0):
    """a big drawn hand coming down from the top (cuff up, fingers pointing down); word written on the cuff"""
    k = pr(t, t0, 0.5); y = y - 260 * (1 - eio(min(1.0, reach)))
    arm = [[(x - 70, 730), (x - 70, y - 220)], [(x + 70, 730), (x + 70, y - 220)]]
    cuff = [(x - 90, y - 220), (x + 90, y - 220), (x + 90, y - 120), (x - 90, y - 120), (x - 90, y - 220)]
    palm = [(x - 80, y - 120), (x - 95, y - 20), (x - 60, y + 40), (x - 30, y + 70), (x + 10, y + 75), (x + 50, y + 55), (x + 80, y + 10), (x + 85, y - 120)]
    fingers = [[(x - 40, y + 10), (x - 44, y + 110)], [(x - 4, y + 20), (x - 2, y + 130)], [(x + 34, y + 14), (x + 40, y + 110)]]
    if k >= 1: c.drawPath(_path(cuff), paint(col, 0.25)); c.drawPath(_path(palm), paint(WHITE))
    ink(c, [wob(p, 510 + i, 0.6) for i, p in enumerate(arm)] + [wob(cuff, 515, 0.6), wob(palm, 516, 0.8)] + [wob(f, 517 + i, 0.5) for i, f in enumerate(fingers)], k, MK, 7)
    if word: mtext(c, word, x, y - 150, 52, col, pr(t, t0 + 0.4, 0.3), "pm")


def receipt_m(c, x, y, t, t0, length=300, grow_t=None, grow=0.0, total=None, col=MK):
    """a till receipt hanging down from (x, y); from grow_t it gets `grow` px longer; zig-zag bottom edge"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    L = length + (grow * eio(pr(t, grow_t, 0.9)) if grow_t is not None else 0)
    w = 150; Lk = L * k
    zz = [(x - w / 2 + i * w / 8, y + Lk + (10 if i % 2 else 0)) for i in range(9)]
    outline = [(x - w / 2, y), (x + w / 2, y)] + zz[::-1] + [(x - w / 2, y)]
    outline = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + Lk)] + zz[::-1][1:] + [(x - w / 2, y)]
    c.drawPath(_path(outline), paint(WHITE)); c.drawPath(_path(outline), stroke(col, 5))
    for i in range(max(0, int(Lk // 38) - 1)):
        yy = y + 30 + i * 38; ww = 90 if i % 3 else 60
        c.drawLine(x - w / 2 + 20, yy, x - w / 2 + 20 + ww, yy, stroke(LIGHT, 5))
    if total and k >= 1: mtext(c, total, x, y + Lk - 22, 34, RD, 1, "pm")


def newspaper_m(c, x, y, t, t0, head="PRICES", tilt=-5):
    k = pr(t, t0, 0.5); w, h = 400, 300
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    pg = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
    if k >= 1: c.drawPath(_path(pg), paint(WHITE))
    ink(c, [wob(pg, 531, 0.6), [(-w / 2 + 20, -h / 2 + 90), (w / 2 - 20, -h / 2 + 90)]], k, MK, 6, pen_=False)
    mtext(c, head, 0, -h / 2 + 70, 50, MK, pr(t, t0 + 0.3, 0.3), "pm")
    for i in range(4):
        for col_ in range(2):
            c.drawLine(-w / 2 + 24 + col_ * 190, -h / 2 + 125 + i * 36, -w / 2 + 24 + col_ * 190 + 150 - (i % 2) * 40, -h / 2 + 125 + i * 36, stroke(LIGHT, 6, pr(t, t0 + 0.4 + i * 0.05, 0.2)))
    c.restore()


def pin_m(c, x, y, t, t0, s=1.0, col=RD):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    pts = [(x, y)] + [(x + 60 * s * math.cos(math.radians(a_)), y - 110 * s + 60 * s * math.sin(math.radians(a_))) for a_ in range(150, 391, 15)] + [(x, y)]
    if k >= 1: c.drawPath(_path(pts), paint(col, 0.75)); c.drawCircle(x, y - 110 * s, 22 * s, paint(WHITE))
    ink(c, [wob(pts, 541, 0.5)], k, MK, 6, pen_=False)


def sticky_m(c, x, y, t, t0, text, s=1.0, tilt=6, col=RD):
    k = pop_(t, t0)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k * s, k * s)
    c.drawRect(R.MakeXYWH(-170 + 6, -110 + 10, 340, 220), paint((0, 0, 0), 0.12, blur=8))
    c.drawRect(R.MakeXYWH(-170, -110, 340, 220), paint(YEL)); c.drawRect(R.MakeXYWH(-170, -110, 340, 34), paint((240, 210, 80)))
    sz = 50; f = font("pm", sz)
    while tw(f, text) > 300: sz -= 2; f = font("pm", sz)
    c.drawString(text, -tw(f, text) / 2, 30, f, paint(col)); c.restore()


def ny_m(c, x, y, t, t0, label="NEW YORK"):
    """a plain hand-drawn state shape (not map data): a rough box with one bumpy side, label inside"""
    k = pr(t, t0, 0.6)
    pts = [(x - 200, y + 70), (x - 200, y - 20), (x - 110, y - 40), (x - 40, y - 110), (x + 140, y - 120), (x + 170, y - 40), (x + 200, y + 70), (x - 200, y + 70)]
    if k > 0.6: hatch(c, _path(pts), pr(k, 0.6, 0.4), BLU, gap=18, w=5, bbox=(x - 210, y - 130, x + 210, y + 80), a=0.35)
    ink(c, [wob(pts, 551, 1.0)], k, MK, 7)
    mtext(c, label, x, y + 30, 46, MK, pr(t, t0 + 0.5, 0.3), "pm")


def coinpile_m(c, x, y, t, t0, n=9):
    for i in range(n):
        tk = t0 + i * 0.07
        if t < tk: continue
        u = pr(t, tk, 0.3); row = 0 if i < 4 else (1 if i < 7 else 2); col_ = i if i < 4 else (i - 4 if i < 7 else i - 7)
        cx = x - 90 + col_ * 60 + row * 30; cy = y - row * 40
        coin(c, cx, cy - 200 * (1 - eio(u)), 34, spin=t * 3 if u < 1 else 0)


def qmap(c, active, done=(), a=1.0, y=380):
    """the hook's two questions as small pills under the brand pill; active coloured, done ticked"""
    if a <= 0: return
    for i, (txt, x) in enumerate((("WHO PICKS?", 360), ("STILL?", 690))):
        on = (i == active); col = RD if on else (GR if i in done else LIGHT)
        sz = 36 if on else 30; f = font("pm", sz); w = tw(f, txt) + 50; h = 60 if on else 50
        c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, paint(WHITE, a))
        c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, stroke(col, 5 if on else 3, a))
        c.drawString(txt, x - tw(f, txt) / 2, y + sz * 0.36, f, paint(col, a))
        if i in done: ink(c, [[(x + w / 2 - 6, y - 4), (x + w / 2 + 10, y + 14), (x + w / 2 + 40, y - 26)]], 1, GR, 7, pen_=False)


# ---------------------------------------------------------------- HOW THEY GOT SO BIG EP 4 (Netflix 2011, 11 Nov 2026)
# redenv_m (hatched red envelope), plancard_m (plan card that tears in two), wall_m (erasable brick wall), atbubble_m (plain @ bubble, no logo),
# chart_drop_m (line chart off a cliff), tally (one-row live COUNTER pill under the brand pill: tick a number down/up through the middle
# of a video = a moving re-hook), dashed_tv (a screen still only planned), qwik_label (word label card). Example: examples/netflix-2011.


def redenv_m(c, x, y, t, t0, s=1.0, text="DVD", tilt=0.0, a=1.0):
    """the red envelope: outline + flap drawn on, then hatched red; word on a small white card"""
    k = pr(t, t0, 0.45); w, h = 260 * s, 170 * s
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt)
    box = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
    c.drawPath(_path(box), paint(WHITE, a))
    if k > 0.5:
        hatch(c, _path(box), pr(k, 0.5, 0.5), RD, gap=13, w=6, bbox=(-w / 2, -h / 2, w / 2, h / 2), seed=701, a=0.8 * a)
    ink(c, [wob(box, 702, 0.6), [(-w / 2, -h / 2), (0, 10 * s), (w / 2, -h / 2)]], k, MK, 6, a=a, pen_=False)
    if text and k >= 1:
        f = font("pm", int(50 * s)); tw_ = tw(f, text) + 30 * s
        c.drawRoundRect(R.MakeXYWH(-tw_ / 2, 22 * s, tw_, 60 * s), 10, 10, paint(WHITE, 0.95 * a))
        mtext(c, text, 0, 70 * s, int(50 * s), MK, 1, "pm", a=a)
    c.restore()


def plancard_m(c, x, y, t, t0, title="STREAMING + 1 DVD", split=0.0, s=1.0):
    """a plan card; split 0..1 tears it in two along a zig-zag and slides the halves apart"""
    k = pr(t, t0, 0.5); w, h = 620 * s, 300 * s
    if k <= 0: return
    zz = [((14 if i % 2 else -14) * s, -h / 2 + i * h / 10) for i in range(11)]
    gap = 80 * eio(split)
    for side in ((-1,) if split <= 0 else (-1, 1)):
        c.save(); c.translate(x + side * gap, y)
        if split <= 0:
            box = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
        elif side < 0:
            box = [(-w / 2, -h / 2)] + zz + [(-w / 2, h / 2), (-w / 2, -h / 2)]
        else:
            box = [(w / 2, -h / 2)] + zz + [(w / 2, h / 2), (w / 2, -h / 2)]
        c.drawPath(_path(box), paint(WHITE))
        ink(c, [wob(box, 711 + side, 0.6)], k if split <= 0 else 1, MK, 7, pen_=False)
        c.restore()
    if split <= 0 and title:
        mtext(c, title, x, y - h / 2 + 70 * s, int(46 * s), MK, pr(t, t0 + 0.4, 0.4), "pm")


def wall_m(c, x, y0, y1, t, t0, erase=0.0):
    """a brick wall drawn between two things; erase 0..1 rubs it out from the top"""
    k = pr(t, t0, 0.6)
    if k <= 0 or erase >= 1: return
    yb = y0 + (y1 - y0) * erase; w = 70
    rows = int((y1 - y0) / 50)
    polys = [[(x - w / 2, y0), (x - w / 2, y1)], [(x + w / 2, y0), (x + w / 2, y1)]]
    for r_ in range(rows + 1): polys.append([(x - w / 2, y0 + r_ * 50), (x + w / 2, y0 + r_ * 50)])
    for r_ in range(rows):
        xo = x if r_ % 2 else x - 12
        polys.append([(xo, y0 + r_ * 50), (xo, y0 + r_ * 50 + 50)])
    c.save(); c.clipRect(R.MakeLTRB(x - w, yb, x + w, y1 + 10))
    c.drawRect(R.MakeLTRB(x - w / 2, y0, x + w / 2, y1), paint((246, 226, 214), k))
    ink(c, polys, k, (150, 70, 50), 6, pen_=False)
    c.restore()


def atbubble_m(c, x, y, t, t0, handle="@QWIKSTER"):
    """a plain speech bubble with an @handle (no platform logo)"""
    k = pop_(t, t0)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    speech(c, 0, 0, 470, 140, handle, 1, 56, BLU, tail=1)
    c.restore()


def chart_drop_m(c, x, y, t, t0, drop_t, w=620, h=330, col=RD):
    """a hand-drawn line chart: wiggles sideways, then falls off a cliff at drop_t"""
    k = pr(t, t0, 0.4)
    ink(c, [wob([(x - w / 2, y + h / 2), (x + w / 2, y + h / 2)], 721, 0.6), wob([(x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 722, 0.6)], k, MK, 6, pen_=False)
    pts = [(x - w / 2 + 20 + i * (w - 140) / 10, y - h / 2 + 60 + 22 * math.sin(i * 1.3)) for i in range(11)]
    ink(c, [wob(pts, 723, 0.8)], pr(t, t0 + 0.2, 0.8), BLU, 8, pen_=False)
    if t > drop_t:
        lx, ly = pts[-1]
        ink(c, [[(lx, ly), (lx + 30, ly + 40), (lx + 50, y + h / 2 - 40), (lx + 80, y + h / 2 - 30)]], pr(t, drop_t, 0.35), col, 9, pen_=False)


def tally(c, val, a=1.0, falling=False, x=765, y=372, label="US MEMBERS", fmt="{:.2f}M"):
    """story upgrade 11 Nov: the member counter under the pill (US members, in millions), one row so it never meets the caption"""
    if a <= 0: return
    f1 = font("pm", 22); f2 = font("pm", 40)
    txt = fmt.format(val); w1 = tw(f1, label); w2 = tw(f2, txt); w = w1 + w2 + 54; h = 58
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, paint(WHITE, a))
    c.drawRoundRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), h / 2, h / 2, stroke(RD if falling else MK, 4, a))
    c.drawString(label, x - w / 2 + 20, y + 8, f1, paint(BLU, a))
    c.drawString(txt, x - w / 2 + 34 + w1, y + 14, f2, paint(RD if falling else MK, a))


def dashed_tv(c, x, y, t, t0, w=360, h=230):
    """the screen Netflix wants to become, still only a dashed outline"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    x0, y0 = x - w / 2, y - h / 2
    for (a_, b_) in (((x0, y0), (x0 + w, y0)), ((x0 + w, y0), (x0 + w, y0 + h)), ((x0 + w, y0 + h), (x0, y0 + h)), ((x0, y0 + h), (x0, y0))):
        dash_line(c, a_, b_, k, LIGHT, 6)
    tri = [(x - 30, y - 40), (x + 42, y), (x - 30, y + 40), (x - 30, y - 40)]
    if k >= 1: ink(c, [tri], 1, LIGHT, 5, pen_=False)


def qwik_label(c, x, y, k=1.0):
    c.drawRoundRect(R.MakeXYWH(x - 150, y - 50, 300, 76), 12, 12, paint(WHITE, k))
    c.drawRoundRect(R.MakeXYWH(x - 150, y - 50, 300, 76), 12, 12, stroke(RD, 4, k))
    mtext(c, "QWIKSTER", x, y + 10, 56, RD, k, "pm")


# ---------------------------------------------------------------- R&D 11 Nov 2026: 7-Eleven props (HOW THEY GOT SO BIG, queue/21-seven-eleven)
def ice_m(c, x, y, t, t0, s=1.0, col=BLU):
    """a block of ice: a 3-D box in outline, light-blue hatch on the front, two shine ticks; a few drip marks"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    w, h, d = 220 * s, 170 * s, 60 * s
    front = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y), (x - w / 2, y)]
    top = [(x - w / 2, y - h), (x - w / 2 + d, y - h - d * 0.7), (x + w / 2 + d, y - h - d * 0.7), (x + w / 2, y - h)]
    side = [(x + w / 2, y), (x + w / 2 + d, y - d * 0.7), (x + w / 2 + d, y - h - d * 0.7)]
    if k >= 1: hatch(c, _path(front), pr(t, t0 + 0.4, 0.35), col, gap=20, w=6, bbox=(x - w / 2, y - h, x + w / 2, y), seed=611, a=0.45)
    ink(c, [wob(front, 601, 0.6), wob(top, 602, 0.5), wob(side, 603, 0.5)], k, MK, 7)
    if k < 1: return
    for i, (dx, dy) in enumerate(((-60, -120), (-30, -130))):
        c.drawLine(x + dx * s, y + dy * s, x + (dx + 26) * s, y + (dy - 22) * s, stroke(WHITE, 8))
    for i, dx in enumerate((-50, 30, 80)):
        c.drawCircle(x + dx * s, y + (18 + 10 * i) * s, 7 * s, paint(col, 0.6 * pr(t, t0 + 0.6 + 0.15 * i, 0.3)))


def riceball_m(c, x, y, t, t0, s=1.0, col=MK):
    """a rice ball (onigiri): rounded triangle in outline with a few grain ticks, a dark hatched seaweed band at the bottom"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    r = 120 * s
    tri = []
    for i in range(3):
        a0 = math.radians(-90 + 120 * i)
        cx_, cy_ = x + 0.55 * r * math.cos(a0), y + 0.55 * r * math.sin(a0)
        tri += circ_pts(cx_, cy_, 0.45 * r, -90 + 120 * i - 60, -90 + 120 * i + 60, 12)
    tri.append(tri[0])
    band = [(x - 0.42 * r, y + 0.95 * r), (x - 0.30 * r, y + 0.15 * r), (x + 0.30 * r, y + 0.15 * r), (x + 0.42 * r, y + 0.95 * r), (x - 0.42 * r, y + 0.95 * r)]
    if k >= 1: hatch(c, _path(band), pr(t, t0 + 0.4, 0.3), col, gap=10, w=6, bbox=(x - r, y, x + r, y + r), seed=621, a=0.9)
    ink(c, [wob(tri, 620, 0.5), wob(band, 622, 0.4)], k, MK, 7)
    if k < 1: return
    for i, (dx, dy) in enumerate(((-30, -40), (10, -60), (35, -20), (-55, 0), (55, 20))):
        c.drawLine(x + dx * s, y + dy * s, x + (dx + 8) * s, y + (dy + 4) * s, stroke(LIGHT, 4))


def truck_m(c, x, y, t, t0, s=1.0, label=None, col=GR, drive=0.0):
    """a small delivery truck (box + cab + two wheels); `drive` = px it has rolled to the right; label on the box"""
    k = pr(t, t0, 0.55)
    if k <= 0: return
    x = x + drive
    box = [(x - 220 * s, y - 40 * s), (x - 220 * s, y - 230 * s), (x + 60 * s, y - 230 * s), (x + 60 * s, y - 40 * s), (x - 220 * s, y - 40 * s)]
    cab = [(x + 60 * s, y - 40 * s), (x + 60 * s, y - 170 * s), (x + 150 * s, y - 170 * s), (x + 200 * s, y - 100 * s), (x + 200 * s, y - 40 * s), (x + 60 * s, y - 40 * s)]
    win = [(x + 80 * s, y - 110 * s), (x + 80 * s, y - 150 * s), (x + 140 * s, y - 150 * s), (x + 168 * s, y - 110 * s), (x + 80 * s, y - 110 * s)]
    if k >= 1: hatch(c, _path(cab), pr(t, t0 + 0.45, 0.3), col, gap=16, w=6, bbox=(x + 60 * s, y - 170 * s, x + 200 * s, y), seed=631, a=0.55)
    ink(c, [wob(box, 630, 0.7), wob(cab, 632, 0.6), wob(win, 633, 0.4),
            wob(circ_pts(x - 150 * s, y - 20 * s, 34 * s, -90, 270, 20), 634, 0.3), wob(circ_pts(x + 130 * s, y - 20 * s, 34 * s, -90, 270, 20), 635, 0.3)], k, MK, 7)
    if label and k >= 1: mtext(c, label, x - 80 * s, y - 120 * s, int(46 * s), col, pr(t, t0 + 0.5, 0.3), "pm")


def sunglasses_m(c, x, y, t, t0, s=1.0, col=MK, tag=None):
    """a pair of sunglasses: two hatched lenses, a bridge, short arms; optional price tag word under them"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    L = [(x - 190 * s, y - 50 * s), (x - 30 * s, y - 50 * s), (x - 40 * s, y + 20 * s), (x - 90 * s, y + 55 * s), (x - 160 * s, y + 45 * s), (x - 190 * s, y - 10 * s), (x - 190 * s, y - 50 * s)]
    Rr = [(2 * x - px, py) for px, py in L]
    if k >= 1:
        for i, poly in enumerate((L, Rr)):
            hatch(c, _path(poly), pr(t, t0 + 0.35, 0.3), col, gap=9, w=6, bbox=(x - 200 * s, y - 60 * s, x + 200 * s, y + 60 * s), seed=641 + i, a=0.9)
    ink(c, [wob(L, 640, 0.4), wob(Rr, 642, 0.4), [(x - 30 * s, y - 40 * s), (x, y - 52 * s), (x + 30 * s, y - 40 * s)],
            [(x - 190 * s, y - 45 * s), (x - 240 * s, y - 60 * s)], [(x + 190 * s, y - 45 * s), (x + 240 * s, y - 60 * s)]], k, MK, 7)
    if k >= 1:
        c.drawLine(x - 160 * s, y - 30 * s, x - 130 * s, y - 10 * s, stroke(WHITE, 6)); c.drawLine(x + 60 * s, y - 30 * s, x + 90 * s, y - 10 * s, stroke(WHITE, 6))
    if tag: mtext(c, tag, x, y + 130 * s, int(46 * s), RD, pr(t, t0 + 0.5, 0.3), "pm")


def manual_m(c, x, y, t, t0, s=1.0, label="MANUAL", open_=0.0, col=BLU):
    """a thick ring binder; open_ 0→1 swings the cover open to show ruled pages (and an empty '?' where the secret should be)"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    w, h = 230 * s, 300 * s
    back = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
    spine = [(x - w / 2 - 30 * s, y - h / 2 + 10 * s), (x - w / 2 - 30 * s, y + h / 2 + 10 * s), (x - w / 2, y + h / 2)]
    ink(c, [wob(back, 650, 0.6), wob(spine, 651, 0.5)], k, MK, 7)
    if k < 1: return
    o = eio(min(1.0, max(0.0, open_)))
    if o < 0.02:
        hatch(c, _path(back), pr(t, t0 + 0.4, 0.3), col, gap=18, w=6, bbox=(x - w / 2, y - h / 2, x + w / 2, y + h / 2), seed=652, a=0.35)
        if label: mtext(c, label, x, y + 12 * s, int(44 * s), MK, pr(t, t0 + 0.5, 0.3), "pm")
        return
    cx = x - w / 2 - (w + 10 * s) * o           # the cover swings out to the left
    cov = [(x - w / 2, y - h / 2), (cx, y - h / 2 + 12 * s * o), (cx, y + h / 2 + 12 * s * o), (x - w / 2, y + h / 2)]
    c.drawPath(_path(cov + [cov[0]]), paint(col, 0.22))
    ink(c, [wob(cov + [cov[0]], 653, 0.4)], 1, MK, 6, pen_=False)
    for i in range(7):
        yy = y - h / 2 + 50 * s + i * 34 * s
        c.drawLine(x - w / 2 + 30 * s, yy, x + w / 2 - 30 * s, yy, stroke(LIGHT, 4))
    for i in range(3):
        c.drawCircle(x - w / 2 + 16 * s, y - h / 3 + i * h / 3, 8 * s, stroke(MK, 4))
    mtext(c, "?", x + 10 * s, y + 40 * s, int(110 * s), RD, pr(o, 0.6, 0.4), "pm")


# ---------------------------------------------------------------- R&D 11 Nov 2026: print-on-demand props (HOW TO START, queue/22-print-on-demand)
def tee_m(c, x, y, t, t0, s=1.0, col=OR, design=True, ghost=False):
    """a plain t-shirt in outline (sleeves, collar); design=True scribbles a small star-sun doodle on the chest in `col`;
    ghost=True draws it as a faint dashed-feel outline (a shirt that doesn't exist yet)"""
    k = pr(t, t0, 0.55)
    if k <= 0: return
    sh = [(x - 90 * s, y - 200 * s), (x - 210 * s, y - 140 * s), (x - 260 * s, y - 40 * s), (x - 180 * s, y), (x - 150 * s, y - 60 * s),
          (x - 150 * s, y + 220 * s), (x + 150 * s, y + 220 * s), (x + 150 * s, y - 60 * s), (x + 180 * s, y), (x + 260 * s, y - 40 * s),
          (x + 210 * s, y - 140 * s), (x + 90 * s, y - 200 * s)]
    collar = circ_pts(x, y - 205 * s, 90 * s, 10, 170, 16)
    if ghost:
        ink(c, [wob(sh, 660, 0.6), collar], k, LIGHT, 5, pen_=False); return
    if k >= 1: c.drawPath(_path(sh + [sh[0]]), paint(WHITE))
    ink(c, [wob(sh, 660, 0.7), wob(collar, 661, 0.3)], k, MK, 7)
    if design and k >= 1:
        kd = pr(t, t0 + 0.45, 0.45)
        ray = [[(x + 70 * s * math.cos(math.radians(a)), y - 40 * s + 70 * s * math.sin(math.radians(a))),
                (x + 105 * s * math.cos(math.radians(a)), y - 40 * s + 105 * s * math.sin(math.radians(a)))] for a in range(0, 360, 45)]
        ink(c, [wob(circ_pts(x, y - 40 * s, 48 * s, -90, 270, 24), 662, 0.4)] + ray, kd, col, 7, pen_=False)


def costbar_m(c, x, y, t, parts, total=25.0, w=900, h=96, t0=0.0, label_y=None, money="${:.2f}"):
    """where the price goes: one long bar = `total`; parts = [(label, value, col, t_start)] hatch in left→right at their times,
    each with its label + amount under it; whatever is left at the right end stays white and is labelled 'LEFT' in green"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    x0 = x - w / 2; box = [(x0, y), (x0 + w, y), (x0 + w, y + h), (x0, y + h), (x0, y)]
    ink(c, [wob(box, 670, 0.5)], k, MK, 7)
    if k < 1: return
    acc = 0.0; ly = label_y or (y + h + 52); used = 0.0
    for i, (lab, val, col, ts) in enumerate(parts):
        u = pr(t, ts, 0.5)
        if u <= 0: break
        a_ = x0 + w * acc / total; b_ = x0 + w * (acc + val * u) / total
        hatch(c, _path([(a_, y), (b_, y), (b_, y + h), (a_, y + h), (a_, y)]), 1.0, col, gap=12, w=6, bbox=(a_, y, b_ + 1, y + h), seed=671 + i, a=0.8)
        c.drawLine(b_, y, b_, y + h, stroke(MK, 4))
        if u >= 1:
            mid = (a_ + b_) / 2; dy = (i % 2) * 70
            mtext(c, lab, mid, ly + dy, 30, col, pr(t, ts + 0.3, 0.3), "pm")
            mtext(c, money.format(val), mid, ly + dy + 34, 30, MK, pr(t, ts + 0.4, 0.3), "kb")
        acc += val * u; used = acc
    if used > 0 and all(pr(t, p[3], 0.5) >= 1 for p in parts):
        left = total - used; mid = x0 + w * (used + left / 2) / total
        mtext(c, "LEFT", mid, y - 26, 34, GR, 1.0, "pm")
        mtext(c, money.format(left), mid, y + h / 2 + 14, 40, GR, 1.0, "pm")


# ---------------------------------------------------------------- HOW IT WORKS EP 6 (cash vs card rewards, 12 Nov 2026)
# COLOUR SPOTS (owner 11 Nov "make my video colourful"): spot() = big hatched highlighter disc behind the key drawing (+45 % colourfulness);
# route_map = 4-stop money route under the pill; terminal_m (card reader + contactless beep), gift_m, feetag (price tag with a FEE slice that
# can slide back in), pricebd_m (cafe price board with a crossed-out line), coin_hop (looping coin for frame-0 motion).
SP_OR = (255, 196, 120); SP_YE = (255, 226, 90); SP_PU = (196, 170, 255); SP_GR = (150, 226, 170); SP_BL = (150, 196, 255); SP_PK = (255, 170, 200)


# ---------------------------------------------------------------- new marker drawings (this episode)
def spot(c, x, y, r, col, k, seed=1, a=0.55):
    """COLOUR SPOT: a big highlighter disc laid in with wide diagonal strokes; pops from the centre"""
    if k <= 0: return
    rr = r * eback(min(1.0, k), 1.3)
    p = skia.Path(); p.addCircle(x, y, rr)
    c.drawCircle(x, y, rr, paint(col, a * 0.55))
    hatch(c, p, 1.0, col, gap=34, w=30, ang=-30, bbox=(x - rr, y - rr, x + rr, y + rr), seed=seed, a=a)


def route_map(c, active, done=(), a=1.0, y=392):
    """the money route under the pill: 4 stops (SHOP, PRICE, BANK, YOU) on a dashed line; active = coloured + bigger, done = ticked"""
    if a <= 0: return
    names = ("SHOP", "PRICE", "BANK", "YOU"); cols = (OR, GOLD, PU, GR); xs = (210, 410, 610, 810)
    for i in range(3):
        x0, x1 = xs[i] + 40, xs[i + 1] - 40
        for j in range(5):
            u0, u1 = j / 5, (j + 0.55) / 5
            c.drawLine(x0 + (x1 - x0) * u0, y - 22, x0 + (x1 - x0) * u1, y - 22, stroke(GR if i in done else LIGHT, 4, a))
    for i, (nm, col, x) in enumerate(zip(names, cols, xs)):
        on = (i == active); r = 30 if on else 22
        c.drawCircle(x, y - 22, r, paint(col if on else WHITE, a))
        c.drawCircle(x, y - 22, r, stroke(MK if on else (col if i in done else LIGHT), 5 if on else 3, a))
        f = font("pm", 30 if on else 24); c.drawString(str(i + 1), x - tw(f, str(i + 1)) / 2, y - 22 + (11 if on else 9), f, paint(WHITE if on else (col if i in done else LIGHT), a))
        mtext(c, nm, x, y + 34, 30 if on else 24, col if (on or i in done) else LIGHT, a, "pm")
        if i in done: ink(c, [[(x + 14, y - 40), (x + 26, y - 28), (x + 50, y - 62)]], 1, GR, 6, pen_=False)


def terminal_m(c, x, y, t, t0, s=1.0, beep_t=None):
    """a small card terminal on the counter; screen flashes green on the tap, contactless arcs"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    body = P([(-70, 0), (-80, -230), (80, -230), (70, 0), (-70, 0)])
    scr = P([(-55, -205), (55, -205), (55, -140), (-55, -140), (-55, -205)])
    c.drawPath(_path(body), paint(WHITE, k))
    if beep_t is not None and t > beep_t: c.drawPath(_path(scr), paint(GR, 0.6 * (1 - pr(t, beep_t + 0.5, 0.6)) + 0.2))
    ink(c, [wob(body, 801, 0.6), wob(scr, 802, 0.4)], k, MK, 6)
    for r_ in range(3):
        for q in range(3):
            c.drawCircle(x + (-34 + q * 34) * s, y + (-105 + r_ * 30) * s, 8 * s, paint(MK, k))
    if beep_t is not None and beep_t < t < beep_t + 0.6:
        u = pr(t, beep_t, 0.6)
        for j in range(3):
            rr = (40 + 30 * j + 40 * u) * s
            c.drawArc(R.MakeXYWH(x - rr, y - 300 * s - rr, 2 * rr, 2 * rr), 220, 100, False, stroke(GR, 5, 1 - u))


def gift_m(c, x, y, t, t0, s=1.0, label="REWARDS", col=PU):
    """a little gift box with a bow, label written under"""
    k = pop_(t, t0, 0.3, 1.6)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    box = [(-80, -60), (80, -60), (80, 70), (-80, 70), (-80, -60)]; lid = [(-92, -95), (92, -95), (92, -60), (-92, -60), (-92, -95)]
    c.drawPath(_path(box), paint(WHITE)); hatch(c, _path(box), 1, col, gap=16, w=6, bbox=(-80, -60, 80, 70), a=0.5)
    c.drawPath(_path(lid), paint(WHITE)); hatch(c, _path(lid), 1, col, gap=12, w=5, bbox=(-92, -95, 92, -60), a=0.35)
    ink(c, [box, lid, [(0, -95), (0, 70)], [(0, -95), (-40, -140), (-50, -110), (0, -95)], [(0, -95), (40, -140), (50, -110), (0, -95)]], 1, MK, 6, pen_=False)
    c.restore()
    if label: mtext(c, label, x, y + 130 * s, int(42 * s), col, pr(t, t0 + 0.2, 0.3), "pm")


def feetag(c, x, y, t, t0, price="$5", fee_t=None, inside=0.0, s=1.0, col=BLU, tilt=-8, fee_col=RD):
    """the cup's $5 swing tag; from fee_t a hatched FEE slice sits off its right end; inside (0..1) slides it back into the tag"""
    tag_m(c, x, y, price, t, t0, col, tilt, s)
    if fee_t is None or t < fee_t: return
    k = pr(t, fee_t, 0.4)
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    out = (1 - eio(min(1.0, inside))) * 110
    sl = [(70 + out, -60), (90 + out, -60), (140 + out, 0), (90 + out, 60), (70 + out, 60), (70 + out, -60)]
    hatch(c, _path(sl), k, fee_col, gap=10, w=5, bbox=(60 + out, -62, 142 + out, 62), a=0.8)
    ink(c, [sl], k, fee_col, 5, pen_=False)
    mtext(c, "FEE", 100 + out, 105, 34, fee_col, pr(t, fee_t + 0.2, 0.3), "pm")
    c.restore()


def pricebd_m(c, x, y, t, t0, item="COFFEE", price="$5", fee_line="+ CARD FEE", cross_t=None, w=440):
    """a cafe price board: item + price, and a second line (written, then crossed out at cross_t)"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    h = 300; rr = R.MakeXYWH(x - w / 2, y - h / 2, w, h)
    c.drawRoundRect(rr, 16, 16, paint((44, 52, 60), k)); c.drawRoundRect(rr, 16, 16, stroke(MK, 7, k))
    mtext(c, item, x - 70, y - 40, 54, WHITE, pr(t, t0 + 0.2, 0.3), "kb"); mtext(c, price, x + 130, y - 40, 60, SP_YE, pr(t, t0 + 0.35, 0.3), "pm")
    if fee_line:
        mtext(c, fee_line, x, y + 70, 46, (255, 170, 160), pr(t, t0 + 0.5, 0.35), "kb")
        if cross_t is not None and t > cross_t:
            ink(c, [wob([(x - 170, y + 60), (x + 170, y + 50)], 811, 1.0)], pr(t, cross_t, 0.3), RD, 10, pen_=False)


def coin_hop(c, t, x0, x1, y, period=1.1, h=150, r=30, t_start=-9.0):
    """a coin hopping from x0 to x1 on a loop (keeps something moving)"""
    if t < t_start: return
    u = ((t - t_start) % period) / period
    coin(c, x0 + (x1 - x0) * eio(u), y - 4 * h * u * (1 - u), r, spin=t * 6)


# ---------------------------------------------------------------- overbooking kit (R&D writers' room 12 Nov 2026, HOW IT WORKS W7)
def plane_m(c, x, y, t, t0, s=1.0, n=10, filled=0, extra=0, col=BLU, label=None):
    """side-view airliner: fuselage, tail, wing; `n` windows = seats, the first `filled` hatched (taken); `extra` red stick
    passengers queue on the steps beside it (tickets sold past the seats)"""
    k = pr(t, t0, 0.6)
    if k <= 0: return
    L, Rr = x - 380 * s, x + 330 * s
    body = [(L + 60 * s, y - 70 * s), (Rr - 40 * s, y - 70 * s), (Rr + 30 * s, y - 20 * s), (Rr - 40 * s, y + 45 * s),
            (L + 40 * s, y + 45 * s), (L, y), (L + 60 * s, y - 70 * s)]
    tail = [(L + 60 * s, y - 70 * s), (L + 10 * s, y - 190 * s), (L + 80 * s, y - 190 * s), (L + 160 * s, y - 70 * s)]
    wing = [(x - 40 * s, y + 20 * s), (x - 150 * s, y + 140 * s), (x - 70 * s, y + 140 * s), (x + 60 * s, y + 20 * s)]
    if k >= 1:
        hatch(c, _path(tail + [tail[0]]), pr(t, t0 + 0.5, 0.3), col, gap=14, w=6, bbox=(L, y - 195 * s, L + 165 * s, y - 65 * s), seed=901, a=0.55)
    ink(c, [wob(body, 900, 0.8), wob(tail, 902, 0.6), wob(wing, 903, 0.6), [(Rr - 30 * s, y - 45 * s), (Rr + 5 * s, y - 20 * s)]], k, MK, 7)
    if k < 1: return
    gap = (Rr - L - 200 * s) / max(1, n)
    for i in range(n):
        wx = L + 150 * s + i * gap; kk = pr(t, t0 + 0.55 + i * 0.03, 0.15)
        if kk <= 0: continue
        rr = R.MakeXYWH(wx - 14 * s, y - 42 * s, 28 * s, 34 * s)
        if i < filled: c.drawRoundRect(rr, 10 * s, 10 * s, paint(col, 0.75 * kk))
        c.drawRoundRect(rr, 10 * s, 10 * s, stroke(MK, 4, kk))
    for j in range(extra):
        px = Rr + 90 * s + j * 46 * s; py = y + 40 * s; kk = pr(t, t0 + 0.9 + j * 0.12, 0.2)
        if kk <= 0: continue
        c.drawCircle(px, py - 62 * s, 13 * s, stroke(RD, 5, kk))
        ink(c, [[(px, py - 49 * s), (px, py - 10 * s)], [(px, py - 10 * s), (px - 12 * s, py + 15 * s)], [(px, py - 10 * s), (px + 12 * s, py + 15 * s)],
                [(px - 15 * s, py - 38 * s), (px + 15 * s, py - 38 * s)]], kk, RD, 5, pen_=False)
    if label: mtext(c, label, x, y + 230 * s, int(48 * s), col, pr(t, t0 + 0.7, 0.3), "pm")


def boardpass_m(c, x, y, t, t0, s=1.0, seat="12C", stamp=None, stamp_t=None, col=BLU, tilt=-6):
    """a boarding pass: stub line, a tiny plane, FLIGHT / SEAT fields; `stamp` (e.g. 'BUMPED') slams on at stamp_t"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(s, s)
    w, h = 520, 240
    box = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)]
    c.drawPath(_path(box), paint(WHITE, k))
    ink(c, [wob(box, 911, 0.6)], k, MK, 7, pen_=False)
    if k >= 1:
        for yy in range(-h // 2 + 12, h // 2 - 8, 22): c.drawLine(w / 2 - 120, yy, w / 2 - 120, yy + 11, stroke(MK, 4))
        c.drawPath(_path([(-w / 2 + 4, -h / 2 + 4), (w / 2 - 4, -h / 2 + 4), (w / 2 - 4, -h / 2 + 48), (-w / 2 + 4, -h / 2 + 48), (-w / 2 + 4, -h / 2 + 4)]), paint(col, 0.9))
        mtext(c, "BOARDING PASS", -60, -h / 2 + 38, 30, WHITE, 1, "pm")
        mtext(c, "FLIGHT", -160, 0, 30, MK, 1, "kb"); mtext(c, "OB 261", -160, 55, 46, MK, pr(t, t0 + 0.3, 0.3), "pm")
        mtext(c, "SEAT", 30, 0, 30, MK, 1, "kb"); mtext(c, seat, 30, 55, 50, RD if seat in ("?", "??") else MK, pr(t, t0 + 0.4, 0.3), "pm")
        ink(c, [[(w / 2 - 95, 25), (w / 2 - 25, 25)], [(w / 2 - 65, 25), (w / 2 - 80, 0)], [(w / 2 - 65, 25), (w / 2 - 80, 50)], [(w / 2 - 92, 25), (w / 2 - 100, 12)]], 1, col, 6, pen_=False)
    c.restore()
    if stamp and stamp_t is not None and t >= stamp_t:
        stamp_m(c, x + 110 * s, y + 75 * s, stamp, pr(t, stamp_t, 0.35), size=int(52 * s))


def gatedesk_m(c, x, y, t, t0, s=1.0, sign="GATE 12", bubble=None, bubble_t=None, col=OR):
    """a gate desk with a little screen sign on a pole; optional speech bubble from the desk ('VOLUNTEERS?')"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    desk = [(x - 200 * s, y), (x - 200 * s, y - 150 * s), (x + 200 * s, y - 150 * s), (x + 200 * s, y), (x - 200 * s, y)]
    top = [(x - 220 * s, y - 150 * s), (x + 220 * s, y - 150 * s)]
    pole = [(x + 150 * s, y - 150 * s), (x + 150 * s, y - 330 * s)]
    scr = [(x + 40 * s, y - 330 * s), (x + 260 * s, y - 330 * s), (x + 260 * s, y - 430 * s), (x + 40 * s, y - 430 * s), (x + 40 * s, y - 330 * s)]
    if k >= 1: hatch(c, _path(desk), pr(t, t0 + 0.4, 0.3), col, gap=18, w=7, bbox=(x - 200 * s, y - 150 * s, x + 200 * s, y), seed=921, a=0.5)
    ink(c, [wob(desk, 920, 0.6), top, pole, wob(scr, 922, 0.5)], k, MK, 7)
    if k >= 1 and sign: mtext(c, sign, x + 150 * s, y - 365 * s, int(34 * s), BLU, pr(t, t0 + 0.5, 0.3), "pm")
    if bubble and bubble_t is not None and t >= bubble_t:
        bw = tw(font("pm", int(50 * s)), bubble) + 70 * s
        speech(c, x - 150 * s, y - 330 * s, bw, 110 * s, bubble, pr(t, bubble_t, 0.3), size=int(50 * s), col=RD)


# ---------------------------------------------------------------- episode run 13 Nov 2026: 7-Eleven (HOW THEY GOT SO BIG EP 5, examples/seven-eleven)
# rubtext/ownertag = a word that a tiny eraser rubs out and rewrites (any held object's state tag, not only the parcel); citypin = map pin + name;
# mini_store/store_stack = counts you can see as towers of tiny shops; yearcard = calendar page whose year is rubbed + rewritten (time jumps);
# pan_trans(f, prev, p, dir) = TWO-CITY camera pan transition (use in compose for trans 'panR'/'panL'; pill band stays put).
SP_BL_ = (150, 196, 255); SP_OR_ = (255, 196, 120)

def rubtext(c, x, y, old, new, t, t_sw, size=46, col=MK, new_col=None, key="pm"):
    """a word that a tiny eraser rubs out at t_sw (0.35 s) and the new word is written on"""
    new_col = new_col or col
    if t < t_sw or new is None:
        if old: mtext(c, old, x, y, size, col, 1, key)
        return
    u = pr(t, t_sw, 0.35)
    if u < 1:
        if old: mtext(c, old, x, y, size, col, 1, key, a=1 - u)
        f = font(key, size); wv = max(tw(f, old or "X"), 60)
        ex = x - wv / 2 + wv * (0.5 + 0.5 * math.sin(u * 9))
        c.drawRoundRect(R.MakeXYWH(ex - 26, y - size * 0.9, 52, size * 1.1), 8, 8, paint((60, 66, 84)))
        c.drawRect(R.MakeXYWH(ex - 26, y + size * 0.05, 52, 12), paint((210, 210, 214)))
    else:
        mtext(c, new, x, y, size, new_col, pr(t, t_sw + 0.35, 0.35), key)

def ownertag(c, x, y, t, t0, text, new=None, t_sw=1e9, col=RD, new_col=None, w=None):
    """the OWNER tag hanging under the store on a string; its word is rubbed out and rewritten (the held object's state)"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    f = font("pm", 42)
    ww = w or max(tw(f, text), tw(f, new or "")) + 70
    c.drawLine(x, y - 70, x, y - 30, stroke(MK, 4, k))
    rr = R.MakeXYWH(x - ww / 2, y - 30, ww, 74)
    c.drawRoundRect(rr, 14, 14, paint(WHITE, k)); c.drawRoundRect(rr, 14, 14, stroke(MK, 5, k))
    c.drawCircle(x, y - 14, 6, stroke(MK, 3, k))
    if k >= 1: rubtext(c, x, y + 26, text, new, t, t_sw, 40, col, new_col)

def citypin(c, x, y, t, t0, name, col):
    pin_m(c, x, y, t, t0, 1.0, col)
    mtext(c, name, x, y + 60, 44, col, pr(t, t0 + 0.3, 0.3), "pm")

def mini_store(c, x, y, s, col, k=1.0):
    """a tiny shop icon (for counts): box + hatched awning stripe"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    c.drawRect(R.MakeXYWH(-24, -40, 48, 40), paint(WHITE)); c.drawRect(R.MakeXYWH(-28, -52, 56, 14), paint(col, 0.6))
    c.drawRect(R.MakeXYWH(-24, -40, 48, 40), stroke(MK, 3)); c.drawRect(R.MakeXYWH(-28, -52, 56, 14), stroke(MK, 3))
    c.drawRect(R.MakeXYWH(4, -24, 12, 24), stroke(MK, 2)); c.restore()

def store_stack(c, x, base, n, t, t0, col, step=0.05, cols=4):
    """n tiny shops stacked into a tower, popping one by one"""
    for i in range(n):
        tk = t0 + i * step
        if t < tk: continue
        r_, q = divmod(i, cols)
        mini_store(c, x + (q - (cols - 1) / 2) * 62, base - r_ * 56, 1.0, col, pop_(t, tk, 0.25))

def grocery_m(c, x, y, kind, k):
    """milk bottle / egg pair / bread loaf, drawn small, popping in"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    if kind == "milk":
        p = [(-34, 0), (-34, -110), (-18, -140), (-18, -170), (18, -170), (18, -140), (34, -110), (34, 0), (-34, 0)]
        c.drawPath(_path(p), paint(WHITE)); c.drawRect(R.MakeXYWH(-34, -90, 68, 40), paint(SP_BL_, 0.8))
        ink(c, [p, [(-22, -170), (22, -170)]], 1, MK, 6, pen_=False); mtext(c, "MILK", 0, -60, 22, BLU, 1, "pm")
    elif kind == "eggs":
        for dx in (-30, 30):
            c.drawOval(R.MakeXYWH(dx - 28, -80, 56, 76), paint(EGG)); c.drawOval(R.MakeXYWH(dx - 28, -80, 56, 76), stroke(MK, 5))
    else:
        p = circ_pts(0, -40, 70, 180, 360, 24, ry=50) + [(70, 0), (-70, 0), (-70, -40)]
        c.drawPath(_path(p), paint(SP_OR_, 0.7)); ink(c, [p], 1, MK, 6, pen_=False)
        for dx in (-30, 0, 30): c.drawLine(dx - 10, -70, dx + 10, -50, stroke(MK, 4))
    c.restore()

def desk_m(c, x, y, t, t0, sign, sub):
    """a planner's desk: table top + legs, a name sign standing on it"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    ink(c, [wob([(x - 260, y), (x + 260, y)], 901, 0.6), wob([(x - 230, y), (x - 230, y + 150)], 902, 0.4), wob([(x + 230, y), (x + 230, y + 150)], 903, 0.4)], k, MK, 8)
    if k < 1: return
    sw = 400; rr = R.MakeXYWH(x - sw / 2, y - 130, sw, 120)
    c.drawRoundRect(rr, 10, 10, paint(WHITE)); c.drawRoundRect(rr, 10, 10, stroke(BLU, 5))
    mtext(c, sign, x, y - 78, 40, BLU, pr(t, t0 + 0.4, 0.3), "pm"); mtext(c, sub, x, y - 30, 30, MK, pr(t, t0 + 0.6, 0.3), "kb")

def license_m(c, x, y, t, t0, s=1.0, signed=0.0, tilt=-5, title="LICENSE"):
    """a license document: title, three lines, a signature line that gets signed (signed 0..1)"""
    k = pop_(t, t0, 0.35, 1.5)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(tilt); c.scale(k * s, k * s)
    rr = R.MakeXYWH(-170, -120, 340, 240)
    c.drawRect(R.MakeXYWH(-164, -112, 340, 240), paint((0, 0, 0), 0.10, blur=6)); c.drawRect(rr, paint(WHITE)); c.drawRect(rr, stroke(MK, 6))
    mtext(c, title, 0, -66, 40, PU, 1, "pm")
    for i in range(3): c.drawLine(-120, -24 + i * 28, 120, -24 + i * 28, stroke(LIGHT, 4))
    c.drawLine(-120, 84, 120, 84, stroke(MK, 3))
    if signed > 0:
        pts = [(-110 + 220 * j / 30, 72 - 14 * math.sin(j * 0.9) - 6 * math.cos(j * 2.1)) for j in range(31)]
        ink(c, [pts], signed, BLU, 5, pen_=False)
    c.restore()

def magnifier_m(c, x, y, r, k, col=MK):
    if k <= 0: return
    c.drawCircle(x, y, r * k, paint(SP_BL_, 0.25)); ink(c, [wob(circ_pts(x, y, r * k, -90, 270, 40), 921, 0.5)], 1, col, 8, pen_=False)
    ink(c, [[(x + r * 0.7 * k, y + r * 0.7 * k), (x + r * 1.5 * k, y + r * 1.5 * k)]], 1, col, 14, pen_=False)

def notebook_m(c, x, y, t, t0, lines_=3, label=None):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    rr = R.MakeXYWH(x - 120, y - 150, 240, 300)
    c.drawRect(rr, paint(WHITE, k)); ink(c, [wob([(x - 120, y - 150), (x + 120, y - 150), (x + 120, y + 150), (x - 120, y + 150), (x - 120, y - 150)], 931, 0.5)], k, MK, 6)
    for i in range(lines_):
        c.drawLine(x - 90, y - 90 + i * 50, x + 30 + 50 * ((i * 7) % 3) / 3, y - 90 + i * 50, stroke(BLU, 5, pr(t, t0 + 0.3 + i * 0.15, 0.2)))
    if label: mtext(c, label, x, y + 110, 34, RD, pr(t, t0 + 0.6, 0.3), "pm")

def till_m(c, x, y, t, t0, s=1.0):
    """a shop till with a small screen; a receipt grows out of its top"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    body = P([(-130, 0), (-110, -150), (110, -150), (130, 0), (-130, 0)])
    scr = P([(-60, -150), (-50, -240), (90, -240), (80, -150)])
    c.drawPath(_path(body), paint(WHITE, k)); c.drawPath(_path(scr), paint(SP_GR, 0.5 * k))
    ink(c, [wob(body, 941, 0.5), wob(scr, 942, 0.4)], k, MK, 6)
    if k >= 1:
        for r_ in range(2):
            for q in range(4): c.drawCircle(x + (-75 + q * 50) * s, y + (-95 + r_ * 45) * s, 9 * s, paint(MK))

def risingline(c, x, y, w, h, t, t0, label, col=GR):
    k = pr(t, t0, 0.8)
    if k <= 0: return
    pts = [(x + w * i / 8, y - h * (0.15 + 0.85 * (i / 8) ** 1.4) + (14 if i % 2 else 0)) for i in range(9)]
    ink(c, [[(x, y + 10), (x + w + 20, y + 10)], [(x, y + 10), (x, y - h - 20)]], 1, MK, 5, pen_=False)
    ink(c, [pts], k, col, 9, pen_=False)
    if k >= 1: mtext(c, label, x + w / 2, y + 70, 44, col, pr(t, t0 + 0.8, 0.3), "pm")

def yearcard(c, x, y, t, t0, text, col=MK, size=64, new=None, t_sw=1e9):
    """a small torn-off calendar page with the year/month written on (rubbed and rewritten for a time jump)"""
    k = pop_(t, t0, 0.3, 1.5)
    if k <= 0: return
    f = font("pm", size); wv = max(tw(f, text), tw(f, new or "")) + 60
    c.save(); c.translate(x, y); c.scale(k, k)
    rr = R.MakeXYWH(-wv / 2, -size, wv, size * 1.6)
    c.drawRect(rr, paint(WHITE)); c.drawRect(R.MakeXYWH(-wv / 2, -size, wv, 22), paint(RD, 0.8)); c.drawRect(rr, stroke(MK, 5))
    c.restore()
    if k >= 1: rubtext(c, x, y + size * 0.42, text, new, t, t_sw, size, col)

def pan_trans(f, prev, p, direction):
    """camera pans across the board: direction +1 = toward Tokyo (content moves left), -1 = toward Dallas.
    Pill + counter band (top 430 px) stays put; a light motion smear sells the move."""
    u = eio(p); sh = int(W * u)
    out = f.copy()
    if direction > 0:
        out[430:, : W - sh] = prev[430:, sh:]; out[430:, W - sh:] = f[430:, : sh] if sh > 0 else out[430:, W - sh:]
    else:
        out[430:, sh:] = prev[430:, : W - sh]; out[430:, :sh] = f[430:, W - sh:] if sh > 0 else out[430:, :sh]
    if 0.05 < p < 0.95:
        k = 9; out[430:] = sum(np.roll(out[430:], i * direction * -6, axis=1) for i in range(k)) / k
    return out


# ---------------------------------------------------------------- 14 Nov 2026 (HOW TO START EP 9, childminding): held house with a gable clock +
# rewritable door tag, small stick kids, baby basket, insurance shield, GP health form, plain notice letter, moon, price tag, hour blocks.
TEALK = (40, 170, 170); YELK = (240, 196, 40)
def home_m(c, x, y, s, t, t0, tag="?", new=None, t_sw=1e9, fill_t=-9.0, hours=2.0, col=GR, tag_col=RD, line_t=None):
    """the held house: house_m + a wall clock in the gable (red wedge from 3 pm) + a door tag that is rubbed out and rewritten"""
    house_m(c, x, y, s, t, t0, col)
    clock_m(c, x, y - 128 * s, t, t0 + 0.25, r=30 * s, h0=15.0, hours=hours, fill_t=fill_t, col=RD)
    if line_t is not None and t > line_t:   # the LINE: a thick red stroke out of the clock at the wedge's edge
        a_ = math.radians((15 % 12) * 30 + hours * 30)
        cx, cy = x, y - 128 * s
        ink(c, [[(cx + 0.2 * 30 * s * math.sin(a_), cy - 0.2 * 30 * s * math.cos(a_)), (cx + 1.6 * 30 * s * math.sin(a_), cy - 1.6 * 30 * s * math.cos(a_))]],
            pr(t, line_t, 0.3), RD, 12, pen_=False)
    if tag is not None or new is not None:
        ownertag(c, x, y - 112 * s + 40 + 60 * s, t, t0 + 0.4, tag or "", new, t_sw, tag_col, None)


def kid_m(c, x, y, s, t, look=(0, 0), girl_=False, col=TEALK, hat=None, scarf=False, pose="stand", a=1.0):
    """a small stick child (scale ~0.4-0.6 of an adult); optional little cap, or the hero's orange scarf (= yours)"""
    if s <= 0: return
    if girl_: girl(c, x, y, s, POSES[pose], Face("open", "smile", look=look), t, dress=col, scarf=ORANGE if scarf else None, a=a)
    else: hero(c, x, y, s, POSES[pose], Face("open", "smile", look=look), t, scarf=ORANGE if scarf else col, a=a)
    hy = y - 330 * s   # roughly the top of the head
    if hat: c.drawPath(_path([(x - 40 * s, hy + 6 * s), (x, hy - 50 * s), (x + 40 * s, hy + 6 * s), (x - 40 * s, hy + 6 * s)]), paint(hat, a))


def baby_m(c, x, y, s, t, t0):
    """a baby in a tiny basket (no realistic child): half-oval basket, round head, bonnet arc"""
    k = pr(t, t0, 0.4)
    if k <= 0: return
    ink(c, [wob(circ_pts(x, y, 90 * s, 0, 180, 24, ry=50 * s), 611, 0.5), [(x - 90 * s, y), (x + 90 * s, y)]], k, MK, 6)
    if k >= 1:
        hatch(c, _path(circ_pts(x, y, 88 * s, 0, 180, 20, ry=48 * s)), 1, YELK, gap=14, w=5, bbox=(x - 90 * s, y, x + 90 * s, y + 52 * s), a=0.5)
        c.drawCircle(x - 20 * s, y - 24 * s, 34 * s, paint(WHITE)); c.drawCircle(x - 20 * s, y - 24 * s, 34 * s, stroke(MK, 5))
        c.drawArc(R.MakeXYWH(x - 64 * s, y - 70 * s, 88 * s, 84 * s), 160, 200, False, stroke(PINK, 8))
        c.drawCircle(x - 30 * s, y - 28 * s, 4, paint(MK)); c.drawCircle(x - 10 * s, y - 28 * s, 4, paint(MK))


def shield_m(c, x, y, t, t0, s=1.0, col=BLU, label=None):
    k = pr(t, t0, 0.45)
    if k <= 0: return
    pts = _sc(x, y, s, [(-80, -100), (0, -130), (80, -100), (80, 0), (0, 110), (-80, 0), (-80, -100)])
    if k > 0.6: hatch(c, _path(pts), pr(k, 0.6, 0.4), col, gap=16, w=6, bbox=(x - 90 * s, y - 140 * s, x + 90 * s, y + 120 * s), a=0.45)
    ink(c, [wob(pts, 621, 0.6), [(x - 36 * s, y - 10 * s), (x - 6 * s, y + 24 * s), (x + 44 * s, y - 40 * s)]], k, MK, 7)
    if label: mtext(c, label, x, y + 190 * s, int(44 * s), col, pr(t, t0 + 0.4, 0.3), "pm")


def healthform_m(c, x, y, t, t0, s=1.0, sign_t=None, label="HEALTH FORM"):
    w, h = 230 * s, 290 * s; k = pr(t, t0, 0.4)
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], 631, 0.6)], k, MK, 6, pen_=False)
    ink(c, [[(x, y - h / 2 + 30 * s), (x, y - h / 2 + 84 * s)], [(x - 27 * s, y - h / 2 + 57 * s), (x + 27 * s, y - h / 2 + 57 * s)]], k, GR, 10, pen_=False)
    for i in range(3): ink(c, [[(x - w / 2 + 26 * s, y - 20 * s + i * 40 * s), (x + w / 2 - 26 * s, y - 20 * s + i * 40 * s)]], k, LIGHT, 5, pen_=False)
    if sign_t is not None and t > sign_t:
        sig = [(x - 70 * s + 140 * s * i / 14, y + h / 2 - 50 * s + 14 * s * math.sin(i * 1.9)) for i in range(15)]
        ink(c, [sig], pr(t, sign_t, 0.5), BLU, 5, pen_=False)
    if label: mtext(c, label, x, y + h / 2 + 64 * s, int(40 * s), MK, pr(t, t0 + 0.4, 0.3), "pm")


def notice_m(c, x, y, t, t0, s=1.0, head="NOTICE", body="STOP", col=RD):
    w, h = 460 * s, 300 * s; k = pr(t, t0, 0.45)
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(-3)
    c.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, h), paint(WHITE, k))
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)], 641, 0.6)], k, MK, 6, pen_=False)
    mtext(c, head, 0, -h / 2 + 70 * s, int(46 * s), MK, pr(t, t0 + 0.3, 0.3), "pm")
    mtext(c, body, 0, 70 * s, int(110 * s), col, pr(t, t0 + 0.5, 0.35), "pm")
    c.restore()


def moon_m(c, x, y, r, k):
    if k <= 0: return
    p = skia.Path(); p.addCircle(x, y, r); q = skia.Path(); q.addCircle(x + r * 0.45, y - r * 0.2, r * 0.85)
    m = skia.Op(p, q, skia.PathOp.kDifference_PathOp)
    c.drawPath(m, paint(YELK, 0.6 * k)); c.drawPath(m, stroke(MK, 5, k))


def pricetag_m(c, x, y, text, k, col=MK, tilt=-6, size=60, strike_t=None, t=0.0):
    if k <= 0: return
    f = font("pm", size); w = tw(f, text) + 80; h = size * 1.5
    c.save(); c.translate(x, y); c.rotate(tilt); s_ = eback(min(1, k), 1.7); c.scale(s_, s_)
    p = _path([(-w / 2, -h / 2), (w / 2 - 30, -h / 2), (w / 2, 0), (w / 2 - 30, h / 2), (-w / 2, h / 2), (-w / 2, -h / 2)])
    c.drawPath(p, paint(WHITE)); c.drawPath(p, stroke(MK, 6)); c.drawCircle(w / 2 - 34, 0, 8, stroke(MK, 4))
    c.drawString(text, -w / 2 + 28, size * 0.36, f, paint(col))
    if strike_t is not None and t > strike_t:
        ink(c, [[(-w / 2 + 14, 8), (w / 2 - 50, -10)]], pr(t, strike_t, 0.25), RD, 9, pen_=False)
    c.restore()


def hourbar_m(c, x, y, t, t0, n, fill_t=None, step=0.4, cell=150, line_at=None, line_t=None, cols=(GR, GR, RD)):
    """a row of hour blocks (3 pm → 3 pm + n); blocks fill one by one; a red LINE is drawn after block `line_at`"""
    x0 = x - cell * n / 2; k = pr(t, t0, 0.5)
    grid = [[(x0, y), (x0 + cell * n, y), (x0 + cell * n, y + 110), (x0, y + 110), (x0, y)]] + [[(x0 + cell * i, y), (x0 + cell * i, y + 110)] for i in range(1, n)]
    ink(c, [wob(g, 650 + i, 0.4) for i, g in enumerate(grid)], k, MK, 5, pen_=False)
    for i in range(n + 1): mtext(c, f"{3 + i}PM", x0 + cell * i, y + 160, 34, LIGHT, k, "kb")
    if fill_t is not None and k >= 1:
        for i in range(n):
            ki = pr(t, fill_t + i * step, 0.3)
            if ki > 0: c.drawRect(R.MakeXYWH(x0 + cell * i + 8, y + 8, (cell - 16) * ki, 94), paint(cols[min(i, len(cols) - 1)], 0.5))
    if line_at is not None and line_t is not None and t > line_t:
        lx = x0 + cell * line_at
        ink(c, [[(lx, y - 70), (lx, y + 180)]], pr(t, line_t, 0.3), RD, 14, pen_=False)


def two_houses(c, x, y, t, t0, s=0.7):
    house_m(c, x - 110, y, s, t, t0, BLU); house_m(c, x + 110, y, s, t, t0 + 0.15, OR)
    if t > t0 + 0.5:
        arrow_m(c, (x - 50, y - 210), (x + 50, y - 210), pr(t, t0 + 0.5, 0.3), MK, 7)
        arrow_m(c, (x + 50, y - 170), (x - 50, y - 170), pr(t, t0 + 0.7, 0.3), MK, 7)


def tick(c, x, y, k, col=GR, s=1.0):
    if k <= 0: return
    ink(c, [[(x - 30 * s, y), (x - 8 * s, y + 24 * s), (x + 36 * s, y - 34 * s)]], k, col, 12, pen_=False)


def box3(c, x, y, t, t0, label, tick_t=None, w=280, h=300):
    k = pr(t, t0, 0.4)
    if k <= 0: return
    ink(c, [wob([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)], int(x) % 97, 0.6)], k, MK, 6, pen_=False)
    mtext(c, label, x, y + h / 2 + 62, 42, MK, pr(t, t0 + 0.2, 0.3), "pm")
    if tick_t is not None and t > tick_t: tick(c, x + w / 2 - 20, y - h / 2 + 10, pr(t, tick_t, 0.3), GR, 1.3)


# ---------------------------------------------------------------- 14 Nov 2026 (R&D writers' room: 24 ZIP code HIW + 25 Domino's BIG):
# pizza in an open box (rewritable lid sticky), ketchup bottle, a five-box ZIP keypad screen, a dashed road that draws itself between two
# points, a gas pump. No brand marks anywhere (plain white box, no domino tile, no red/blue trade dress).
CHEESE = (250, 214, 120); CRUST = (214, 150, 70)
def pizza_m(c, x, y, t, t0, s=1.0, open_=1.0, slices=8, garlic=False, sad=False, col=RD, lid_text=None):
    """an open pizza box seen from the front-top: box base + lid swung up by `open_`; a round pizza with hatched sauce/cheese, pepperoni
    dots, slice lines; garlic=True sprinkles green herb ticks on the crust; sad=True draws a pale, flat pizza (grey hatch, no toppings);
    lid_text = a word written on the inside of the lid (e.g. 'CARDBOARD?' / 'NEW RECIPE')"""
    k = pr(t, t0, 0.55)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    base = P([(-230, 0), (-230, -40), (230, -40), (230, 0), (-230, 0)])
    lh = 300 * open_
    lid = P([(-230, -40), (-230, -40 - lh), (230, -40 - lh), (230, -40)])
    c.drawPath(_path(base), paint(WHITE, k))
    if open_ > 0.05:
        c.drawPath(_path(lid + [lid[0]]), paint(WHITE, k))
    ink(c, [wob(base, 1101, 0.5)] + ([wob(lid, 1102, 0.6)] if open_ > 0.05 else []), k, MK, 7)
    if k < 1: return
    r = 175 * s; cy = y - 40 * s - r * 0.42 * 0.55 + 40 * s   # the pizza rests on the base, its front rim just over the box's front edge
    # the pizza sits in the base, drawn as an ellipse peeking over the front edge
    rim = circ_pts(x, cy - 40 * s, r, ry=r * 0.42)
    inner = circ_pts(x, cy - 40 * s, r * 0.84, ry=r * 0.42 * 0.84)
    c.drawPath(_path(rim), paint(CRUST if not sad else (200, 190, 175), 0.9))
    c.drawPath(_path(inner), paint(CHEESE if not sad else (232, 228, 218)))
    if not sad:
        hatch(c, _path(inner), pr(t, t0 + 0.4, 0.4), col, gap=22, w=6, bbox=(x - r, cy - 40 * s - r * 0.5, x + r, cy - 40 * s + r * 0.5), seed=1103, a=0.35)
        for i, (dx, dy) in enumerate(((-80, -10), (40, -30), (90, 15), (-20, 25), (-110, 20), (20, -5))):
            c.drawCircle(x + dx * s, cy - 40 * s + dy * s, 17 * s, paint(col, 0.9 * pr(t, t0 + 0.5 + 0.06 * i, 0.2)))
    ink(c, [wob(rim, 1104, 0.6), wob(inner, 1105, 0.5)], 1, MK, 5, pen_=False)
    for i in range(slices // 2):
        a0 = math.radians(180 * i / (slices // 2))
        dx, dy = r * 0.84 * math.cos(a0), r * 0.84 * 0.42 * math.sin(a0)
        c.drawLine(x - dx, cy - 40 * s - dy, x + dx, cy - 40 * s + dy, stroke(MK, 3, 0.45))
    if garlic and not sad:
        for i in range(14):
            a0 = 2 * math.pi * i / 14
            px, py = x + r * 0.92 * math.cos(a0), cy - 40 * s + r * 0.42 * 0.92 * math.sin(a0)
            c.drawLine(px - 6, py - 3, px + 6, py + 3, stroke(GR, 5, pr(t, t0 + 0.6 + 0.03 * i, 0.2)))
    if lid_text and open_ > 0.5:
        mtext(c, lid_text, x, y - (40 + lh * 0.55) * s, int(64 * s), col, pr(t, t0 + 0.5, 0.4), "pm")


def ketchup_m(c, x, y, t, t0, s=1.0, col=RD):
    """a plain squeeze bottle (no label art): rounded body hatched red, a cap and nozzle, the word written on a white band"""
    k = pop_(t, t0, 0.3, 1.6)
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    body = [(-60, 0), (-70, -170), (-50, -210), (50, -210), (70, -170), (60, 0), (-60, 0)]
    cap = [(-34, -210), (-34, -250), (34, -250), (34, -210)]; noz = [(-10, -250), (-4, -290), (4, -290), (10, -250)]
    c.drawPath(_path(body), paint(WHITE)); hatch(c, _path(body), 1, col, gap=14, w=6, bbox=(-70, -210, 70, 0), seed=1111, a=0.7)
    c.drawRect(R.MakeXYWH(-64, -135, 128, 56), paint(WHITE))
    ink(c, [wob(body, 1112, 0.5), wob(cap, 1113, 0.4), wob(noz, 1114, 0.3)], 1, MK, 6, pen_=False)
    c.restore()
    mtext(c, "SAUCE", x, y - 95 * s * k, int(30 * s), col, pr(t, t0 + 0.2, 0.3), "pm")


def zippad_m(c, x, y, t, t0, digits="", step=0.18, s=1.0, prompt="ZIP CODE?", hot=None, col=BLU):
    """a card-terminal screen asking for a ZIP: prompt on top, five boxes; `digits` are typed in one by one every `step` s after t0+0.5;
    hot = (t_on) makes the five boxes glow red from that time (the 'this is personal information' beat)"""
    k = pr(t, t0, 0.45)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    scr = P([(-250, -170), (250, -170), (250, 110), (-250, 110), (-250, -170)])
    c.drawPath(_path(scr), paint(WHITE, k)); ink(c, [wob(scr, 1121, 0.6)], k, MK, 7)
    if k < 1: return
    mtext(c, prompt, x, y - 95 * s, int(46 * s), MK, pr(t, t0 + 0.3, 0.3), "pm")
    glow = hot is not None and t >= hot
    for i in range(5):
        bx = x + (-200 + i * 100) * s
        box = [(bx - 38 * s, y - 40 * s), (bx + 38 * s, y - 40 * s), (bx + 38 * s, y + 60 * s), (bx - 38 * s, y + 60 * s), (bx - 38 * s, y - 40 * s)]
        if glow: c.drawPath(_path(box), paint(RD, 0.18 + 0.1 * math.sin(6 * (t - hot))))
        ink(c, [box], 1, RD if glow else MK, 5, pen_=False)
        if i < len(digits) and t >= t0 + 0.5 + step * i:
            mtext(c, digits[i], bx, y + 42 * s, int(70 * s), col, pr(t, t0 + 0.5 + step * i, 0.12), "pm")


def road_m(c, a, b, t, t0, d=1.2, col=MK, w=8, bend=0.35, dash=True, seed=1131):
    """a winding road drawn on from a to b (two parallel wobbly lines with a dashed centre line); the pen rides the tip"""
    k = pr(t, t0, d)
    if k <= 0: return
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2 + (y1 - y0) * bend, (y0 + y1) / 2 - (x1 - x0) * bend
    pts = []
    for i in range(41):
        u = i / 40
        pts.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1))
    def off(o):
        out = []
        for i, (px, py) in enumerate(pts):
            qx, qy = pts[min(i + 1, 40)] if i < 40 else pts[i]; rx, ry = pts[max(i - 1, 0)]
            tx, ty = qx - rx, qy - ry; L = math.hypot(tx, ty) or 1
            out.append((px - ty / L * o, py + tx / L * o))
        return out
    ink(c, [wob(off(-22), seed, 0.8), wob(off(22), seed + 1, 0.8)], k, col, w)
    if dash and k > 0.2:
        n = int(40 * k)
        for i in range(0, n - 1, 3):
            c.drawLine(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], stroke(OR, 6))


def gaspump_m(c, x, y, t, t0, s=1.0, col=GR, screen="ZIP?"):
    """a plain fuel pump: tall box with a screen (prompt written on it), hose and nozzle hooked on the side; green hatch on the lower panel"""
    k = pr(t, t0, 0.5)
    if k <= 0: return
    P = lambda pts: _sc(x, y, s, pts)
    body = P([(-90, 0), (-90, -360), (90, -360), (90, 0), (-90, 0)])
    scr = P([(-60, -320), (60, -320), (60, -240), (-60, -240), (-60, -320)])
    low = P([(-90, -140), (90, -140), (90, 0), (-90, 0), (-90, -140)])
    hose = P([(90, -200), (150, -180), (165, -90), (140, -20)])
    noz = P([(80, -260), (125, -250), (125, -215), (95, -215)])
    c.drawPath(_path(body), paint(WHITE, k))
    if k >= 1: hatch(c, _path(low), pr(t, t0 + 0.4, 0.3), col, gap=18, w=6, bbox=(x - 90 * s, y - 140 * s, x + 90 * s, y), seed=1141, a=0.5)
    ink(c, [wob(body, 1142, 0.5), wob(scr, 1143, 0.4), wob(hose, 1144, 0.8), wob(noz, 1145, 0.4)], k, MK, 7)
    if k >= 1 and screen: mtext(c, screen, x, y - 262 * s, int(44 * s), BLU, pr(t, t0 + 0.5, 0.3), "pm")
