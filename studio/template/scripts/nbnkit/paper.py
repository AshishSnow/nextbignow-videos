"""NOTEBOOK look for OopsMyBusiness (owner, 7 Nov 2026: "make like this which looks real and realistic, paper texture, pencil animation",
two reference shots of a hand-written ruled notebook filmed on a phone).
Drop-in over the whiteboard kit: an episode written for board.py becomes a notebook episode by adding ONE line at the very end of its
anim_shots.py (after compose):
    exec(open(f"{_D}/nbnkit/paper.py").read())
What it changes (everything else in the episode stays as written):
  * paper  — a photographed ruled page: warm off-white stock, fibre noise + tooth, dotted ruled lines, a printed header rule with our own
             wordmark (no real notebook brand), faint show-through from the back of the page, phone-camera light fall-off.
  * pencil — marker colours map to graphite / blue ballpoint / red pen / coloured pencils; strokes are thinner and carry paper-tooth grain;
             hatch fills become light pencil shading; a real-looking pencil (or a ballpoint for blue ink) rides the stroke tip with its shadow.
  * type   — Permanent Marker -> Caveat Bold, Kalam -> Caveat (handwriting), sized up to match.
  * camera — no slow zoom inside the page (writing must stay on the lines); instead the whole page drifts like a hand-held phone,
             with a slow push-in per shot, impact shakes, sensor grain.
  * cuts   — "wipe" becomes a pink eraser rubbing the old page out, leaving a fading ghost of the erased pencil.
"""
import math as _m
import numpy as _np, skia as _sk, cv2 as _cv2
import nbn_gfx as _ngx      # the configured module (nbnkit/__init__ sets FONTDIR on this one)
_ngx._TF.update({"cv": "Caveat-Medium.ttf", "cb": "Caveat-Bold.ttf", "gh": "GochiHand.ttf"})

# ---------------------------------------------------------------- inks
GRAPH = (54, 54, 60); BALL = (30, 44, 132); REDP = (172, 34, 40); GRP = (34, 112, 70); ORP = (198, 104, 36); PUP = (94, 60, 150)
_PMAP = {(26, 30, 42): GRAPH, (30, 96, 220): BALL, (224, 50, 46): REDP, (22, 152, 86): GRP, (244, 132, 28): ORP, (126, 74, 206): PUP,
         (251, 251, 249): (255, 255, 255)}


def pcol(col):
    """board marker colour -> notebook ink colour (known ones mapped; anything else darkened and calmed like a coloured pencil)"""
    col = tuple(int(x) for x in col[:3])
    if col in _PMAP: return _PMAP[col]
    if min(col) > 235: return col
    hsv = _cv2.cvtColor(_np.uint8([[col]]), _cv2.COLOR_RGB2HSV)[0, 0].astype(float)
    hsv[1] *= 0.82; hsv[2] *= 0.74
    return tuple(int(x) for x in _cv2.cvtColor(_np.uint8([[hsv]]), _cv2.COLOR_HSV2RGB)[0, 0])


def _is_graph(col): return abs(col[0] - col[2]) < 14 and max(col) < 110


# ---------------------------------------------------------------- tooth textures (paper grain the pencil skips over)
_TR = _np.random.default_rng(7)
_tooth = _cv2.GaussianBlur(_TR.random((256, 256)).astype(_np.float32), (0, 0), 0.9)
_tooth = (_tooth - _tooth.min()) / (_tooth.max() - _tooth.min())
_TSH = {}


def _tshader(col, lo, hi):
    k = (col, lo, hi)
    if k not in _TSH:
        a = (lo + (hi - lo) * _np.clip((_tooth - 0.18) / 0.7, 0, 1)) * 255
        img = _np.zeros((256, 256, 4), _np.uint8); img[..., 0], img[..., 1], img[..., 2] = col; img[..., 3] = a.astype(_np.uint8)
        # premultiplied for skia
        img[..., :3] = (img[..., :3].astype(_np.float32) * img[..., 3:4] / 255).astype(_np.uint8)
        im = _sk.Image.fromarray(img, colorType=_sk.ColorType.kRGBA_8888_ColorType, alphaType=_sk.AlphaType.kPremul_AlphaType)
        _TSH[k] = im.makeShader(_sk.TileMode.kRepeat, _sk.TileMode.kRepeat)
    return _TSH[k]


def _ipaint(col, w=None, a=1.0, fill=False):
    """pencil / ballpoint paint with paper-tooth grain"""
    p = _sk.Paint(); p.setAntiAlias(True)
    g = _is_graph(col)
    p.setShader(_tshader(col, 0.42 if g else 0.80, 0.95 if g else 1.0)); p.setAlphaf(min(1.0, a * (0.92 if g else 0.95)))
    if not fill:
        p.setStyle(_sk.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeCap(_sk.Paint.kRound_Cap); p.setStrokeJoin(_sk.Paint.kRound_Join)
    return p


def _pw(w, col): return max(2.6, w * (0.58 if _is_graph(col) else 0.5))


# ---------------------------------------------------------------- fonts: marker -> handwriting
_FMAP = {"pm": ("cb", 1.16), "kb": ("cv", 1.14), "kr": ("cv", 1.12)}


def font(key, size):
    k2, s = _FMAP.get(key, (key, 1.0))
    return _ngx.font(k2, size * s)


# ---------------------------------------------------------------- the writing tools at the stroke tip
def _shadow_quad(c, x, y, ang, L, wd):
    ex, ey = x + L * _m.sin(_m.radians(ang)), y - L * _m.cos(_m.radians(ang))
    nx, ny = _m.cos(_m.radians(ang)), _m.sin(_m.radians(ang))
    sh = _sk.Path(); sh.moveTo(x + 4, y + 2)
    sh.lineTo(ex + 70 + nx * wd, ey + 60 + ny * wd); sh.lineTo(ex + 70 - nx * wd, ey + 60 - ny * wd); sh.close()
    p = _sk.Paint(); p.setAntiAlias(True); p.setColor(_sk.Color(20, 16, 10)); p.setAlphaf(0.20)
    p.setMaskFilter(_sk.MaskFilter.MakeBlur(_sk.kNormal_BlurStyle, 16)); c.drawPath(sh, p)


def _lin(c, rect, cols, horiz=True):
    x0, y0, x1, y1 = rect.left(), rect.top(), rect.right(), rect.bottom()
    pts = [_sk.Point(x0, y0), _sk.Point(x1, y0) if horiz else _sk.Point(x0, y1)]
    sh = _sk.GradientShader.MakeLinear(pts, [_sk.Color(*cc) for cc in cols])
    p = _sk.Paint(); p.setAntiAlias(True); p.setShader(sh); return p


def pencil(c, x, y, ang=26):
    """a yellow HB pencil, tip on the paper, body up and to the right (a right hand)"""
    _shadow_quad(c, x, y, ang, 640, 26)
    c.save(); c.translate(x, y); c.rotate(ang)
    pa = _sk.Paint(); pa.setAntiAlias(True)
    # graphite point + sharpened wood cone (scalloped where the blade cut the paint)
    cone = _sk.Path(); cone.moveTo(-6, -20); cone.lineTo(-25, -96)
    for i in range(6): cone.quadTo(-25 + 8.3 * i + 4, -104, -25 + 8.3 * (i + 1), -96)
    cone.lineTo(6, -20); cone.close()
    c.drawPath(cone, _lin(c, _sk.Rect.MakeLTRB(-25, -100, 25, -20), [(236, 204, 160), (214, 176, 128), (176, 136, 92)]))
    tip = _sk.Path(); tip.moveTo(0, 0); tip.lineTo(-7, -24); tip.lineTo(7, -24); tip.close()
    pa.setColor(_sk.Color(46, 46, 52)); c.drawPath(tip, pa)
    # hexagonal yellow body: three faces
    body = _sk.Rect.MakeLTRB(-25, -560, 25, -98)
    c.drawRect(body, _lin(c, body, [(250, 214, 92), (240, 190, 40), (226, 168, 24), (184, 128, 14)]))
    pa.setColor(_sk.Color(255, 236, 160)); pa.setAlphaf(0.55); c.drawRect(_sk.Rect.MakeLTRB(-14, -560, -9, -100), pa)
    pa.setAlphaf(1.0)
    # ferrule + eraser
    fr = _sk.Rect.MakeLTRB(-26, -616, 26, -560); c.drawRect(fr, _lin(c, fr, [(214, 214, 218), (150, 150, 158), (226, 226, 230), (120, 120, 128)]))
    pa.setColor(_sk.Color(96, 96, 104))
    for yy in (-572, -586, -600): c.drawRect(_sk.Rect.MakeLTRB(-26, yy, 26, yy + 2.5), pa)
    er = _sk.Rect.MakeLTRB(-24, -664, 24, -614); c.drawRoundRect(er, 12, 12, _lin(c, er, [(240, 150, 150), (226, 118, 122), (196, 92, 98)]))
    c.restore()


def ballpen(c, x, y, ang=24):
    """a plain blue-ink ballpoint (no brand), tip on the paper"""
    _shadow_quad(c, x, y, ang, 620, 20)
    c.save(); c.translate(x, y); c.rotate(ang)
    pa = _sk.Paint(); pa.setAntiAlias(True)
    tip = _sk.Path(); tip.moveTo(-2, -4); tip.lineTo(-15, -70); tip.lineTo(15, -70); tip.lineTo(2, -4); tip.close()
    c.drawPath(tip, _lin(c, _sk.Rect.MakeLTRB(-15, -70, 15, 0), [(226, 226, 230), (160, 160, 168), (110, 110, 118)]))
    pa.setColor(_sk.Color(40, 40, 46)); c.drawCircle(0, -2, 3, pa)
    grip = _sk.Rect.MakeLTRB(-19, -190, 19, -70); c.drawRoundRect(grip, 8, 8, _lin(c, grip, [(70, 74, 84), (40, 42, 50), (24, 26, 32)]))
    body = _sk.Rect.MakeLTRB(-19, -600, 19, -186)
    c.drawRect(body, _lin(c, body, [(84, 100, 170), (40, 56, 132), (24, 34, 92)]))
    pa.setColor(_sk.Color(255, 255, 255)); pa.setAlphaf(0.35); c.drawRect(_sk.Rect.MakeLTRB(-10, -590, -6, -196), pa); pa.setAlphaf(1)
    cap = _sk.Rect.MakeLTRB(-20, -640, 20, -596); c.drawRoundRect(cap, 14, 14, _lin(c, cap, [(60, 76, 150), (26, 36, 96)]))
    c.restore()


_TOOL = {"col": GRAPH}


def pen(c, x, y, col=None):
    col = col or _TOOL["col"]
    (pencil if _is_graph(col) else ballpen)(c, x, y)


# ---------------------------------------------------------------- strokes, fills, text
def ink(c, polys, prog, col=None, w=9, a=1.0, pen_=True):
    col = pcol(col if col is not None else (26, 30, 42))
    if prog <= 0 or not polys: return None
    paths = [_path(p) for p in polys]; lens = [_sk.PathMeasure(p, False).getLength() for p in paths]; tot = sum(lens) or 1
    left = prog * tot; tip = None; pw = _pw(w, col)
    for p, L in zip(paths, lens):
        if left <= 0: break
        pa = _ipaint(col, pw, a)
        if left < L:
            eff = _sk.TrimPathEffect.Make(0.0, float(max(1e-4, min(0.9999, left / L))))
            if eff is not None: pa.setPathEffect(eff); c.drawPath(p, pa)
            pos, tan = _sk.PathMeasure(p, False).getPosTan(left); tip = (pos.x(), pos.y())
        else:
            c.drawPath(p, pa)
        left -= L
    if pen_ and tip is not None and prog < 1:
        _TOOL["col"] = col; _TOOL["tip"] = (tip, c.getTotalMatrix())
    return tip


def hatch(c, clip, prog, col, gap=17, w=7, ang=-35, bbox=(0, 0, 1080, 1920), seed=3, a=0.85):
    """pencil shading: close, light, slightly uneven strokes laid down one by one"""
    if prog <= 0: return
    col = pcol(col); x0, y0, x1, y1 = bbox; c.save(); c.clipPath(clip, doAntiAlias=True)
    ca, sa = _m.cos(_m.radians(ang - 10)), _m.sin(_m.radians(ang - 10)); L = (x1 - x0) + (y1 - y0)
    lines = []; d = -L; g = max(6, gap * 0.55)
    while d < L:
        cx, cy = (x0 + x1) / 2 + d * sa, (y0 + y1) / 2 - d * ca
        lines.append([(cx - ca * L, cy - sa * L), (cx + ca * L, cy + sa * L)]); d += g
    n = int(len(lines) * prog + 0.999); r = _np.random.default_rng(seed)
    # clip each hatch line to the bbox first (they were drawn 2x the diagonal long), and draw them as two paths, not one call per line
    groups = [_sk.Path(), _sk.Path()]
    for i, ln in enumerate(lines[:n]):
        jx = r.normal(0, 1.5); (ax, ay), (bx, by) = ln
        ok = _clipseg(ax + jx, ay, bx - jx, by, x0 - 20, y0 - 20, x1 + 20, y1 + 20)
        if ok: groups[i % 2].moveTo(ok[0], ok[1]); groups[i % 2].lineTo(ok[2], ok[3])
    for gi, gp in enumerate(groups):
        c.drawPath(gp, _ipaint(col, max(2.4, w * 0.42), a * (0.5 + 0.12 * gi)))
    c.restore()


def _clipseg(ax, ay, bx, by, x0, y0, x1, y1):
    """Liang-Barsky: clip segment to a box; None if outside"""
    dx, dy = bx - ax, by - ay; u0, u1 = 0.0, 1.0
    for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
        if p == 0:
            if q < 0: return None
        else:
            u = q / p
            if p < 0: u0 = max(u0, u)
            else: u1 = min(u1, u)
    if u0 > u1: return None
    return (ax + u0 * dx, ay + u0 * dy, ax + u1 * dx, ay + u1 * dy)


def mtext(c, s, x, y, size=80, col=None, prog=1.0, key="pm", align="c", pen_=False, a=1.0):
    if prog <= 0 or not s: return
    col = pcol(col if col is not None else (26, 30, 42))
    f = font(key, size); w = f.measureText(s); xs = x - w / 2 if align == "c" else x
    c.save(); c.clipRect(_sk.Rect.MakeLTRB(xs - 10, y - size * 1.5, xs - 10 + (w + 20) * min(1, prog), y + size * 0.7))
    c.drawString(s, xs, y, f, _ipaint(col, a=a, fill=True)); c.restore()
    if prog < 1: _TOOL["col"] = col; _TOOL["tip"] = ((xs + w * prog, y - size * 0.25), c.getTotalMatrix())


def tw(f, s): return f.measureText(s)


def stamp_m(c, x, y, text, k, col=(224, 50, 46), tilt=-9, size=70):
    """a red-pen box drawn round a word (no rubber stamp in a notebook)"""
    if k <= 0: return
    col = pcol(col); f = font("pm", size); w = tw(f, text) + 60; h = size * 1.45
    c.save(); c.translate(x, y); c.rotate(tilt * 0.5)
    mtext(c, text, 0, size * 0.36, size, col, min(1, k * 1.6), "pm")
    ink(c, [wob([(-w / 2, -h / 2), (w / 2, -h / 2 - 6), (w / 2 + 6, h / 2), (-w / 2, h / 2 + 4), (-w / 2 - 4, -h / 2 + 10)], seed=len(text), amp=2.0)],
        pr(k, 0.5, 0.5) if k < 1 else 1, col, 8, pen_=False)
    c.restore()


# ---------------------------------------------------------------- the page
def _make_paper(seed=3):
    W_, H_ = 1080, 1920; r = _np.random.default_rng(seed)
    base = _np.array((236, 231, 219), _np.float32) / 255
    lo = _cv2.GaussianBlur(r.normal(0, 1, (H_, W_)).astype(_np.float32), (0, 0), 90); lo /= (_np.abs(lo).max() + 1e-6)
    mid = _cv2.GaussianBlur(r.normal(0, 1, (H_, W_)).astype(_np.float32), (0, 0), 6); mid /= (_np.abs(mid).max() + 1e-6)
    fine = r.normal(0, 1, (H_, W_)).astype(_np.float32)
    lum = 1 + 0.022 * lo + 0.012 * mid + 0.016 * fine
    # fibres: short, faint, mostly horizontal
    fib = _np.zeros((H_, W_), _np.float32)
    for _ in range(2600):
        x, y = r.uniform(0, W_), r.uniform(0, H_); a = r.normal(0, 0.5); L = r.uniform(8, 40)
        _cv2.line(fib, (int(x), int(y)), (int(x + L * _m.cos(a)), int(y + L * _m.sin(a))), float(r.choice((-1, 1)) * r.uniform(0.3, 1)), 1, _cv2.LINE_AA)
    lum += 0.018 * _cv2.GaussianBlur(fib, (0, 0), 0.6)
    img = _np.ones((H_, W_, 3), _np.float32) * base * lum[..., None]
    # dotted ruled lines (as printed: grey, broken) + the header rule
    rule = _np.ones((H_, W_), _np.float32)
    for yy in range(398, 1890, 76):
        for xx in range(62, 1030, 7): _cv2.line(rule, (xx, yy), (xx + 3, yy), 0.0, 2, _cv2.LINE_AA)
    _cv2.line(rule, (56, 326), (1024, 322), 0.0, 3, _cv2.LINE_AA)
    rule = 1 - (1 - rule) * 0.42
    ink_ = _np.array((112, 112, 122), _np.float32) / 255
    img = img * rule[..., None]
    # show-through: mirrored, blurred scribble lines from the back of the page
    st = _np.ones((H_, W_), _np.float32)
    for row in range(8):
        yy = 470 + row * 152 + r.integers(-10, 10); x = 120 + r.integers(0, 80)
        while x < 900:
            L = r.integers(40, 160); _cv2.line(st, (x, yy), (x + L, yy + r.integers(-4, 4)), 0.0, 9, _cv2.LINE_AA); x += L + r.integers(20, 60)
    st = _cv2.GaussianBlur(st, (0, 0), 5); img *= (1 - (1 - st) * 0.035)[..., None]
    # phone-camera light: brighter upper middle, warm, falls off to the corners and the bottom right
    yy, xx = _np.mgrid[0:H_, 0:W_].astype(_np.float32)
    d = _np.sqrt(((xx - W_ * 0.42) / (W_ * 0.95)) ** 2 + ((yy - H_ * 0.40) / (H_ * 0.80)) ** 2)
    light = 1.03 - 0.30 * _np.clip(d, 0, 1.4) ** 2.2
    img *= light[..., None]; img *= _np.array((1.0, 0.985, 0.955), _np.float32)
    return _np.clip(img, 0, 1)


PAPER = _make_paper()
_GR = [(_np.random.default_rng(100 + i).normal(0, 1, (1920, 1080, 1)).astype(_np.float32) * 0.010) for i in range(6)]
_TOOTH_FULL = 1 - 0.30 * _np.clip((_cv2.resize(_np.tile(_tooth, (8, 5)), (1080, 1920)) - 0.55) * 2.0, 0, 1)


def board_bg(c, t, seed=0): c.clear(_sk.Color(255, 255, 255))


def pill(c, text):
    """the printed page header: our own wordmark + 'Date' (printed grey), and the series written in blue ballpoint on the rule"""
    f = _ngx.font("ins", 30); p = _sk.Paint(); p.setAntiAlias(True); p.setColor(_sk.Color(96, 96, 106))
    for i, (dx, dy) in enumerate(((0, 0), (14, 0), (0, 14), (14, 14))):
        c.drawRect(_sk.Rect.MakeXYWH(66 + dx, 278 + dy, 10, 10), p)
    c.drawString("OOPSMYBUSINESS", 102, 304, f, p)
    ser = text.split("·")[-1].strip().title() if "·" in text else text.title()
    mtext(c, ser, 400, 318, 56, (30, 96, 220), 1, "kb", align="l")


# ---------------------------------------------------------------- shots -> frames
PUSH = 0.022   # push-in over a shot, applied to the whole page (writing stays on its lines)


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    c = SURF.getCanvas(); c.resetMatrix(); _TOOL["tip"] = None
    board_bg(c, tt)
    RENDER[sid](c, tt)
    pill(c, topline(sid))
    if _TOOL.get("tip"):   # the tool goes on last, above everything it is drawing
        (x, y), M = _TOOL["tip"]; c.save(); c.setMatrix(M); pen(c, x, y); c.restore()
    o = to_rgb(SURF); return o.astype(_np.float32) / (255.0 if o.dtype == _np.uint8 else 1.0)


def _eraser_sprite(img, x, y, ang):
    """pink rubber eraser seen from above, with its contact shadow (drawn on the final float frame)"""
    rect = ((x, y), (150, 290), ang)
    pts = _cv2.boxPoints(rect).astype(_np.int32)
    sh = _np.zeros(img.shape[:2], _np.float32); _cv2.fillConvexPoly(sh, pts + _np.array([26, 22], _np.int32), 1.0, _cv2.LINE_AA)
    sh = _cv2.GaussianBlur(sh, (0, 0), 14); img *= (1 - 0.28 * sh)[..., None]
    m = _np.zeros(img.shape[:2], _np.float32); _cv2.fillConvexPoly(m, pts, 1.0, _cv2.LINE_AA)
    col = _np.array((232, 128, 132), _np.float32) / 255
    yy = _np.linspace(1.06, 0.86, img.shape[0], dtype=_np.float32)[:, None, None]
    img[:] = img * (1 - m[..., None]) + (col * yy) * m[..., None]
    pts2 = _cv2.boxPoints(((x, y - 70 * _m.cos(_m.radians(ang))), (150, 110), ang)).astype(_np.int32)
    m2 = _np.zeros(img.shape[:2], _np.float32); _cv2.fillConvexPoly(m2, pts2, 1.0, _cv2.LINE_AA)
    img[:] = img * (1 - 0.9 * m2[..., None]) + _np.array((70, 100, 170), _np.float32) / 255 * 0.9 * m2[..., None]   # paper sleeve


def _finish(content, t, n, sh_i, er=None):
    """content (ink on white) -> grain -> onto the paper -> hand-held phone camera"""
    a = 1 - content
    a *= _TOOTH_FULL[..., None]
    img = PAPER * (1 - a)
    if er is not None: _eraser_sprite(img, *er)
    s = SHOTS[sh_i]; u = pr(t, s["start"], max(0.5, s["end"] - s["start"]))
    z = 1.035 + PUSH * eio(u)
    dx = 5 * _m.sin(t * 0.63) + 3 * _m.sin(t * 1.71 + 1); dy = 4 * _m.sin(t * 0.47 + 2) + 2.5 * _m.sin(t * 1.33)
    rot = 0.35 * _m.sin(t * 0.39 + 0.5)
    for ti, d, amp in IMPACTS:
        if ti <= t < ti + d:
            k = 1 - (t - ti) / d; dx += amp * 1.6 * k * _m.sin(t * 97); dy += amp * 1.6 * k * _m.cos(t * 83)
    M = _cv2.getRotationMatrix2D((540, 1000), rot, z); M[0, 2] += dx; M[1, 2] += dy
    img = _cv2.warpAffine(img, M, (1080, 1920), flags=_cv2.INTER_LINEAR, borderMode=_cv2.BORDER_REFLECT)
    img += _GR[n % 6]
    return img


ERASE = 0.55


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); dt = t - sh["start"]; er = None
    if i > 0 and sh["trans"] == "wipe" and dt < 1.3:
        prv = rs(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n)
        ghost = 0.16 * max(0.0, 1 - dt / 1.3)
        f = f * (1 - ghost * (1 - prv))          # the erased pencil never quite goes
        if dt < ERASE:                           # the eraser rubs the old page out, top to bottom in a zigzag
            p = eio(dt / ERASE); yb = int(-120 + 2160 * p)
            keep = f.copy(); keep[max(0, yb):] = prv[max(0, yb):]
            band0, band1 = max(0, yb - 160), max(0, min(1920, yb))
            if band1 > band0: keep[band0:band1] = 1 - (1 - prv[band0:band1]) * 0.25
            f = keep
            er = (540 + 330 * _m.sin(dt * 34), yb - 40, 18 * _m.sin(dt * 34))
    return (_np.clip(_finish(f, t, n, i, er), 0, 1) * 255 + 0.5).astype(_np.uint8)


def note(c, t, t0, text, t1=None, y=1478):
    """the source, jotted in pencil in the margin of the page (not a printed chip)"""
    if t < t0 or (t1 is not None and t > t1): return
    s = "source: " + text.lower() if not text.lower().startswith(("source", "comment")) else text.lower()
    size = 40; f = font("kr", size)
    while tw(f, s) > 860 and size > 26: size -= 2; f = font("kr", size)
    mtext(c, s, 540, y + 14, size, (26, 30, 42), pr(t, t0, 0.6), "kr")

# Props imported from the module (`from nbnkit.board import house_m, stamp_m, carton_m …`) look up ink/hatch/mtext in nbnkit.board's own
# namespace, so on paper they stayed marker drawings. Point that namespace at the pencil versions too (R&D 7 Nov 2026; only runs when the
# NOTEBOOK look is on, OMB_LOOK=board never executes this file).
try:
    import nbnkit.board as _bdm
    globals().setdefault("_path", _bdm._path)
    for _n in ("ink", "hatch", "mtext", "pen", "tw", "stamp_m"):
        if _n in globals(): setattr(_bdm, _n, globals()[_n])
    del _n
except Exception as _e:   # never break a render over the look
    print("paper.py: board props stay marker:", _e)
