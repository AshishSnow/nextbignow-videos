"""DOODLE kit for OopsMyBusiness (owner, 13 Nov 2026, sent 4 doodle-explainer screenshots: "Create this type of animation").
Graph-paper page, thick wobbly black ink outlines with flat vibrant fills, line boil on twos (outlines re-jitter every 2 frames),
hatched ground band, object characters with eyes and stick limbs, torn-paper transcript strip, orange tape labels, red stamps,
hand-drawn speech bubbles, scribble circles and arrows. Our own drawing code, generic objects only — no logos, no brand trade dress.
Skia. Used by exec() from anim_shots.py (needs W, H; defines BOIL which the renderer sets per frame).
"""
import math, os
import numpy as np, skia, cv2

W, H = 1080, 1920
_S = os.environ.get("STUDIO", "/home/claude/studio"); _FD = f"{_S}/fonts/ttf"; _TFC = {}


def tf(name):
    if name not in _TFC: _TFC[name] = skia.Typeface.MakeFromFile(f"{_FD}/{name}")
    return _TFC[name]


def font(name, size): return skia.Font(tf(name), size)


BLK_F, XB_F, HAND_F, MARK_F, TYPE_F, ANTON_F = "Montserrat-Black.ttf", "Montserrat-ExtraBold.ttf", "Kalam-Bold.ttf", "PermanentMarker.ttf", "SpecialElite.ttf", "Anton.ttf"
INK = (26, 24, 30); PAPER = (250, 249, 243); WHITE = (255, 255, 255)
RED = (238, 58, 56); ORG = (255, 138, 28); YEL = (255, 212, 38); GRN = (58, 196, 104); BLU = (48, 136, 255); SKY = (120, 200, 255)
PNK = (255, 110, 170); PUR = (140, 92, 255); TAN = (240, 190, 116); SAUS = (212, 84, 62); MUST = (255, 200, 20); GREY = (190, 190, 196)
DGRN = (30, 150, 80); CREAM = (255, 244, 214); BROWN = (150, 96, 60); TEAL = (30, 196, 186)
BOIL = 0


def C(rgb, a=1.0): return skia.Color4f(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255, a)


def P(col, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor4f(C(col, a)); return p


def S(col, w, a=1.0):
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
    p.setColor4f(C(col, a)); return p


def ease(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def eout(x): x = min(1.0, max(0.0, x)); return 1 - (1 - x) ** 3


def back(x, s=1.7): x = min(1.0, max(0.0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def pr(t, t0, d): return min(1.0, max(0.0, (t - t0) / d)) if d > 0 else float(t >= t0)


def shade(col, k): return tuple(int(max(0, min(255, v * k))) for v in col)


# ------------------------------------------------------------------ wobble (line boil)
def h01(i, seed):
    x = math.sin(i * 12.9898 + seed * 78.233) * 43758.5453; return x - math.floor(x)


def jit(i, seed, amp): return (h01(i, seed + BOIL * 7.131) - 0.5) * 2 * amp


def _smooth(pts, closed=True):
    p = skia.Path(); n = len(pts)
    if n < 3:
        p.moveTo(*pts[0]); [p.lineTo(*q) for q in pts[1:]]; return p
    if closed:
        m0 = ((pts[-1][0] + pts[0][0]) / 2, (pts[-1][1] + pts[0][1]) / 2); p.moveTo(*m0)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]; p.quadTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        p.close()
    else:
        p.moveTo(*pts[0])
        for i in range(1, n - 1):
            a, b = pts[i], pts[i + 1]; p.quadTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        p.lineTo(*pts[-1])
    return p


def wpts(pts, closed=True, seed=0, amp=2.4, step=30, corners=True):
    """subdivide edges and jitter: hand-drawn edge that re-boils on twos."""
    out = []; n = len(pts); k = 0
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]; L = math.hypot(b[0] - a[0], b[1] - a[1]); m = max(1, int(L / step))
        for j in range(m):
            u = j / m; x = a[0] + (b[0] - a[0]) * u; y = a[1] + (b[1] - a[1]) * u
            if j == 0 and corners: out.append((x + jit(k, seed, amp * 0.5), y + jit(k + 99, seed, amp * 0.5))); out.append((x + 0.01, y + 0.01))
            else: out.append((x + jit(k, seed, amp), y + jit(k + 99, seed, amp)))
            k += 1
    if not closed: out.append((pts[-1][0] + jit(k, seed, amp), pts[-1][1] + jit(k + 99, seed, amp)))
    return out


def wpoly(pts, seed=0, amp=2.4, closed=True, step=30):
    if closed:   # corners stay sharp-ish: repeat the corner point so the quad smoothing hugs it
        out = []; n = len(pts); k = 0
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]; L = math.hypot(b[0] - a[0], b[1] - a[1]); m = max(1, int(L / step))
            ca = (a[0] + jit(k, seed, amp * 0.6), a[1] + jit(k + 51, seed, amp * 0.6)); out += [ca, ca]
            for j in range(1, m):
                u = j / m; out.append((a[0] + (b[0] - a[0]) * u + jit(k + j, seed, amp), a[1] + (b[1] - a[1]) * u + jit(k + j + 77, seed, amp)))
            k += m + 3
        return _smooth(out, True)
    return _smooth(wpts(pts, False, seed, amp, step), False)


def wellipse(cx, cy, rx, ry, seed=0, amp=2.4, a0=0.0):
    n = max(14, int((rx + ry) * 0.16)); pts = []
    for i in range(n):
        a = a0 + i / n * math.tau; r = 1 + jit(i, seed, amp) / max(rx, ry)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return _smooth(pts, True)


def wrrect(x0, y0, x1, y1, r=24, seed=0, amp=2.4):
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2); pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for j in range(4): a = math.radians(a0 + j * 30); pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    out = []; n = len(pts); k = 0
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]; L = math.hypot(b[0] - a[0], b[1] - a[1]); m = max(1, int(L / 34))
        for j in range(m):
            u = j / m; out.append((a[0] + (b[0] - a[0]) * u + jit(k, seed, amp), a[1] + (b[1] - a[1]) * u + jit(k + 77, seed, amp))); k += 1
    return _smooth(out, True)


def ink(c, pth, fill=None, w=9, col=INK, a=1.0):
    if fill is not None: c.drawPath(pth, P(fill, a))
    if w: c.drawPath(pth, S(col, w, a))


def wline(c, pts, seed=0, w=8, col=INK, amp=2.0, a=1.0):
    c.drawPath(_smooth(wpts(pts, False, seed, amp, 26, False), False), S(col, w, a))


def quad_pts(x0, y0, x1, y1, bend=0.0, n=8):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) + 1e-6
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    return [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1) for u in (i / n for i in range(n + 1))]


# ------------------------------------------------------------------ page
_PAGE = None


def _make_page():
    s = skia.Surface(W, H); c = s.getCanvas(); c.clear(skia.Color(*PAPER))
    rng = np.random.default_rng(5)
    for x in range(0, W + 1, 40):
        major = x % 200 == 0; c.drawLine(x + 0.5, 0, x + 0.5, H, S((150, 196, 236) if major else (196, 222, 244), 2.4 if major else 1.4))
    for y in range(0, H + 1, 40):
        major = y % 200 == 0; c.drawLine(0, y + 0.5, W, y + 0.5, S((150, 196, 236) if major else (196, 222, 244), 2.4 if major else 1.4))
    img = s.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).astype(np.float32)
    n = cv2.GaussianBlur(rng.standard_normal((H // 4, W // 4)).astype(np.float32), (0, 0), 1.2); n = cv2.resize(n, (W, H)) * 3.2
    img[..., :3] += n[..., None]; img = np.clip(img, 0, 255).astype(np.uint8)
    return skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType)


def page(c, tint=None):
    global _PAGE
    if _PAGE is None: _PAGE = _make_page()
    c.drawImage(_PAGE, 0, 0)
    if tint: c.drawRect(skia.Rect.MakeWH(W, H), P(tint, 0.10))


def hatch(c, clip_path, gap=22, w=4, col=INK, ang=45, a=0.85):
    c.save(); c.clipPath(clip_path, doAntiAlias=True); b = clip_path.getBounds(); d = b.width() + b.height()
    k = math.tan(math.radians(ang)); x = b.left() - b.height() * k
    while x < b.right() + 10:
        c.drawLine(x, b.bottom(), x + b.height() * k, b.top(), S(col, w, a)); x += gap
    c.restore()


def ground(c, y=1440, depth=64, seed=3):
    band = skia.Path(); band.addRect(skia.Rect.MakeLTRB(-20, y, W + 20, y + depth)); hatch(c, band, 24, 4, INK, 50, 0.75)
    wline(c, [(-10, y), (W + 10, y)], seed, 9); wline(c, [(-10, y + depth), (W + 10, y + depth)], seed + 1, 5, a=0.8)


def hshadow(c, x, y, w, seed=0):
    if w < 4: return
    pth = wellipse(x, y, w / 2, w * 0.09, seed, 1.5); hatch(c, pth, 13, 3, INK, 50, 0.7)


# ------------------------------------------------------------------ text helpers
def text(c, s, x, y, size, col=INK, fnt=BLK_F, align="c", a=1.0, maxw=None):
    f = font(fnt, size); w = f.measureText(s)
    if maxw and w > maxw: f = font(fnt, size * maxw / w); w = maxw
    xx = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    c.drawString(s, xx, y, f, P(col, a)); return w


def wrap(s, fnt, size, maxw):
    f = font(fnt, size); out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if f.measureText(t) <= maxw or not cur: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out


def tape(c, s, x, y, size=46, rot=-3, k=1.0, col=ORG, fg=INK, seed=1):
    """torn orange masking-tape label with bold text (key-moment caption)."""
    if k <= 0: return
    f = font(BLK_F, size); tw = f.measureText(s); w, h = tw + 2 * size * 0.6, size * 1.55
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2)]
    for i in range(1, 6): pts.append((w / 2 + (6 if i % 2 else -4), -h / 2 + h * i / 6))
    pts += [(w / 2, h / 2), (-w / 2, h / 2)]
    for i in range(5, 0, -1): pts.append((-w / 2 + (-6 if i % 2 else 4), -h / 2 + h * i / 6))
    pth = wpoly(pts, seed, 1.2, True, 60); c.drawPath(pth, P(col)); c.drawPath(pth, S(shade(col, 0.75), 3))
    c.drawString(s, -tw / 2, size * 0.36, f, P(fg)); c.restore()


def stamp(c, s, x, y, size=70, rot=-8, k=1.0, col=RED, seed=2, fnt=ANTON_F):
    """red rubber stamp box: slams in (k from stamp_k)."""
    if k <= 0: return
    f = font(fnt, size); lines = s.split("\n"); tw = max(f.measureText(l) for l in lines); lh = size * 1.05
    w, h = tw + size * 0.9, lh * len(lines) + size * 0.55
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); a = 0.92
    ink(c, wrrect(-w / 2, -h / 2, w / 2, h / 2, 10, seed, 2.0), None, 9, col, a)
    ink(c, wrrect(-w / 2 + 12, -h / 2 + 12, w / 2 - 12, h / 2 - 12, 6, seed + 5, 1.6), None, 4, col, a)
    for i, l in enumerate(lines):
        c.drawString(l, -f.measureText(l) / 2, -h / 2 + size * 0.28 + lh * (i + 0.82), f, P(col, a))
    c.restore()


def stamp_k(t, t0, d=0.22):
    if t < t0: return 0.0
    u = (t - t0) / d
    return 1.8 - 0.8 * eout(u) if u < 1 else 1.0


def pop_k(t, t0, d=0.3): return back(pr(t, t0, d)) if t >= t0 else 0.0


def bubble(c, s, x, y, k=1.0, tail=(0, 120), size=54, maxw=640, fnt=HAND_F, seed=4, bg=WHITE, fg=INK, think=False):
    """hand-drawn speech bubble centred at x,y; tail points to (x+tail[0], y+tail[1])."""
    if k <= 0: return
    lines = wrap(s, fnt, size, maxw); f = font(fnt, size); lh = size * 1.18
    tw = max(f.measureText(l) for l in lines); w, h = tw + size * 1.3, lh * len(lines) + size * 0.9
    c.save(); c.translate(x, y); c.scale(k, k)
    body = wrrect(-w / 2, -h / 2, w / 2, h / 2, min(60, h / 2), seed, 2.2)
    if not think:
        tx, ty = tail; bx = max(-w / 2 + 60, min(w / 2 - 60, tx * 0.35)); by = h / 2 - 8 if ty > 0 else -h / 2 + 8
        tl = wpoly([(bx - 34, by), (tx, ty), (bx + 34, by)], seed + 3, 1.5, True, 40)
        body = skia.Op(body, tl, skia.PathOp.kUnion_PathOp)
    ink(c, body, bg, 8)
    if think:
        for j, (u, r) in enumerate(((0.55, 18), (0.8, 11))): ink(c, wellipse(tail[0] * u, tail[1] * u, r, r, seed + j, 1), bg, 6)
    for i, l in enumerate(lines):
        c.drawString(l, -f.measureText(l) / 2, -h / 2 + size * 0.45 + lh * (i + 0.78), f, P(fg))
    c.restore()


def arrow(c, x0, y0, x1, y1, bend=60, col=INK, w=9, seed=7, k=1.0, head=34):
    pts = quad_pts(x0, y0, x1, y1, bend, 12)
    if k < 1: pts = pts[:max(2, int(len(pts) * k))]
    wline(c, pts, seed, w, col, 1.4)
    if k >= 0.98:
        (ax, ay), (bx, by) = pts[-2], pts[-1]; a = math.atan2(by - ay, bx - ax)
        for s_ in (-1, 1):
            wline(c, [(bx, by), (bx - head * math.cos(a + s_ * 0.5), by - head * math.sin(a + s_ * 0.5))], seed + s_, w, col, 1)


def scribble(c, x, y, rx, ry, k=1.0, col=RED, w=8, seed=9):
    """marker circle drawn on (k 0..1), slightly more than one loop."""
    n = int(40 * k) + 2; pts = []
    for i in range(n):
        u = i / 40 * 1.15; a = -2.2 + u * math.tau; r = 1 + 0.06 * math.sin(u * 7 + seed) + jit(i, seed, 0.02)
        pts.append((x + math.cos(a) * rx * r, y + math.sin(a) * ry * r))
    if len(pts) > 2: c.drawPath(_smooth(pts, False), S(col, w, 0.95))


def strike(c, x0, y, x1, k=1.0, col=RED, w=12, seed=3):
    if k > 0: wline(c, [(x0, y + 6), (x0 + (x1 - x0) * k, y - 6)], seed, w, col, 1.5)


# ------------------------------------------------------------------ transcript strip (torn paper at the top)
def strip(c, words, t_cursor=True, y0=262, size=50, t=0.0):
    """words: list of display words already spoken (typewriter reveal). Two lines max, left aligned, inside the safe zone."""
    if not words: return
    lines = wrap(" ".join(words), TYPE_F, size, 860)[-2:]; f = font(TYPE_F, size); lh = size * 1.32
    h = lh * 2 + 46; y1 = y0 + h
    top = [(-10, y0 + jit(i, 41, 4)) for i in range(0)] + [(x, y0 + (5 if (x // 27) % 2 else -3) + jit(x, 41, 2.5)) for x in range(20, 1061, 27)]
    bot = [(x, y1 + (7 if (x // 23) % 2 else -5) + jit(x, 43, 3)) for x in range(1060, 19, -23)]
    pth = wpoly(top + bot, 40, 0.5, True, 200)
    c.save(); c.translate(0, 8); c.drawPath(pth, P(INK, 0.16)); c.restore()
    c.drawPath(pth, P((255, 255, 252))); c.drawPath(pth, S((200, 200, 200), 2))
    yy = y0 + 23 + size * 0.95
    for i, l in enumerate(lines):
        c.drawString(l, 84, yy + i * lh, f, P(INK))
    if t_cursor and int(t * 3) % 2 == 0:
        lw = f.measureText(lines[-1]); c.drawRect(skia.Rect.MakeXYWH(84 + lw + 8, yy + (len(lines) - 1) * lh - size * 0.75, size * 0.42, size * 0.85), P(INK, 0.8))


# ------------------------------------------------------------------ faces & limbs
def eyes(c, x, y, s=1.0, look=(0, 0), blink=False, sep=44, r=26, mood="neutral", seed=11):
    for j, sx in enumerate((-1, 1)):
        ex = x + sx * sep * s; rr = r * s * (1.25 if mood == "shock" else 1.0)
        if blink and mood != "shock":
            wline(c, [(ex - rr, y), (ex + rr, y)], seed + j, 7 * s)
            continue
        ink(c, wellipse(ex, y, rr * 0.86, rr, seed + j, 1.2), WHITE, 6.5 * s)
        pr_ = rr * (0.32 if mood == "shock" else 0.46)
        c.drawCircle(ex + look[0] * rr * 0.4, y + look[1] * rr * 0.4 + 2, pr_, P(INK))
        c.drawCircle(ex + look[0] * rr * 0.4 - pr_ * 0.35, y + look[1] * rr * 0.4 - pr_ * 0.3, pr_ * 0.3, P(WHITE))
        if mood == "angry": wline(c, [(ex - sx * rr * 1.0, y - rr * 1.35), (ex + sx * rr * 0.9, y - rr * 0.9)], seed + 5 + j, 8 * s)
        if mood == "worried": wline(c, [(ex - sx * rr * 0.9, y - rr * 1.0), (ex + sx * rr * 1.0, y - rr * 1.4)], seed + 5 + j, 7 * s)


def mouth(c, x, y, s=1.0, open_=0.0, mood="neutral", seed=13):
    w = 40 * s
    if open_ > 0.05 or mood == "shock":
        o = max(open_, 0.7 if mood == "shock" else 0)
        if mood == "shock": pth = wellipse(x, y + 6 * s, w * 0.5, w * 0.55 * (0.6 + o * 0.6), seed, 1.2)
        else: pth = wpoly([(x - w, y - 4 * s), (x + w, y - 4 * s), (x + w * 0.6, y + (10 + 30 * o) * s), (x - w * 0.6, y + (10 + 30 * o) * s)], seed, 1.2, True, 30)
        ink(c, pth, (150, 30, 40), 6.5 * s)
        if o > 0.4: c.save(); c.clipPath(pth, doAntiAlias=True); c.drawCircle(x, y + (16 + 30 * o) * s, w * 0.5, P((246, 110, 120))); c.restore()
    elif mood in ("sad", "worried", "angry"):
        wline(c, quad_pts(x - w * 0.8, y + 10 * s, x + w * 0.8, y + 10 * s, -16 * s, 6), seed, 7 * s)
    else:
        wline(c, quad_pts(x - w, y, x + w, y, 22 * s, 6), seed, 7 * s)


def limb(c, x0, y0, x1, y1, bend=20, w=8, hand=True, seed=17, foot=False, s=1.0):
    wline(c, quad_pts(x0, y0, x1, y1, bend, 6), seed, w * s, INK, 1.2)
    if foot: ink(c, wellipse(x1 + 10 * s * (1 if x1 >= x0 else -1), y1 - 6 * s, 24 * s, 13 * s, seed, 1), INK, 0)
    elif hand: ink(c, wellipse(x1, y1, 13 * s, 13 * s, seed, 1), WHITE, 6 * s)


# ------------------------------------------------------------------ object characters (invented, generic, no logos)
# every character is drawn standing with its feet on (x, y); s = scale; arms: dict side->(dx, dy) hand target relative to shoulder, or preset name
ARM_PRESETS = {"down": ((-40, 110), (40, 110)), "up": ((-90, -120), (90, -120)), "hips": ((40, 60), (-40, 60)), "wave": ((-50, 110), (100, -110)),
               "point": ((-40, 110), (150, -20)), "shrug": ((-110, -40), (110, -40)), "hold": ((60, 40), (-60, 40)), "cheer": ((-60, -140), (60, -140)),
               "stop": ((-40, 110), (160, -60))}


def _arms(c, sx_l, sx_r, sy, preset, t, s, seed, wave=True):
    (lx, ly), (rx, ry) = ARM_PRESETS.get(preset, preset) if isinstance(preset, str) else preset
    if preset == "wave" and wave: rx += 40 * math.sin(t * 9); ry += 20 * math.cos(t * 9)
    limb(c, sx_l, sy, sx_l + lx * s, sy + ly * s, 24 * s * (1 if ly > 0 else -1), 8, True, seed, s=s)
    limb(c, sx_r, sy, sx_r + rx * s, sy + ry * s, -24 * s * (1 if ry > 0 else -1), 8, True, seed + 3, s=s)


def _legs(c, x, hip_y, foot_y, s, t, walk, seed, spread=34):
    for j, sx in enumerate((-1, 1)):
        ph = math.sin(t * 12 + j * math.pi) if walk else 0; lift = max(0, ph) * 22 * s
        limb(c, x + sx * spread * s, hip_y, x + sx * (spread + 8) * s + ph * 20 * s, foot_y - lift, 8 * sx * s, 8, False, seed + j, foot=True, s=s)


def char(c, kind, x, y, s=1.0, t=0.0, talk=0.0, look=(0, 0), mood="neutral", arms="down", walk=False, blink=False, seed=21, rot=0.0, **kw):
    bob = (abs(math.sin(t * 12)) * 10 if walk else math.sin(t * 2.6 + seed) * 4) * s
    c.save(); c.translate(x, y); c.rotate(rot); c.translate(-x, -y)
    hshadow(c, x, y + 4, 230 * s * kw.get("shadow_w", 1.0), seed)
    fn = {"hotdog": _hotdog, "soda": _soda, "tag": _tag, "card": _card, "bill": _bill, "cart": _cart_char, "box": _box, "mattress": _mattress}[kind]
    fn(c, x, y - bob, s, t, talk, look, mood, arms, walk, blink, seed, **kw)
    c.restore()


def _hotdog(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    leg = 92 * s; by = y - leg - 70 * s   # body centre
    _legs(c, x, y - leg - 10 * s, y, s, t, walk, seed)
    # sausage (back), bun (front), mustard zigzag
    ink(c, wrrect(x - 225 * s, by - 72 * s, x + 225 * s, by + 8 * s, 40 * s, seed, 2.2), SAUS, 9 * s)
    c.save(); c.clipPath(wrrect(x - 225 * s, by - 72 * s, x + 225 * s, by + 8 * s, 40 * s, seed, 0), doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(x - 230 * s, by - 72 * s, x + 230 * s, by - 52 * s), P(shade(SAUS, 1.18))); c.restore()
    zz = [(x - 170 * s + i * 34 * s, by - 46 * s + (-10 if i % 2 else 10) * s) for i in range(11)]; wline(c, zz, seed + 4, 13 * s, MUST, 1.2)
    bun = wrrect(x - 190 * s, by - 34 * s, x + 190 * s, by + 70 * s, 52 * s, seed + 1, 2.4); ink(c, bun, TAN, 9 * s)
    c.save(); c.clipPath(bun, doAntiAlias=True); c.drawRect(skia.Rect.MakeLTRB(x - 200 * s, by + 40 * s, x + 200 * s, by + 80 * s), P(shade(TAN, 0.86))); c.restore()
    _arms(c, x - 180 * s, x + 180 * s, by + 18 * s, arms, t, s, seed + 7)
    eyes(c, x - 8 * s, by - 40 * s, s, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x - 8 * s, by + 26 * s, s * 0.9, talk, mood, seed + 2)
    if kw.get("cheeks", True): c.drawCircle(x - 92 * s, by + 18 * s, 14 * s, P(PNK, 0.55)); c.drawCircle(x + 76 * s, by + 18 * s, 14 * s, P(PNK, 0.55))


def _soda(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=RED, label="SODA", **kw):
    leg = 84 * s; cb = y - leg; ct = cb - 300 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 30)
    cup = wpoly([(x - 120 * s, ct), (x + 120 * s, ct), (x + 88 * s, cb), (x - 88 * s, cb)], seed, 2.2, True, 40); ink(c, cup, WHITE, 9 * s)
    c.save(); c.clipPath(cup, doAntiAlias=True)
    for i in range(-3, 4): c.drawPath(wpoly([(x + i * 70 * s - 18 * s, ct - 10), (x + i * 70 * s + 18 * s, ct - 10), (x + i * 56 * s + 14 * s, cb + 10), (x + i * 56 * s - 14 * s, cb + 10)], seed + i, 1.2, True, 80), P(col))
    c.restore(); ink(c, cup, None, 9 * s)
    ink(c, wrrect(x - 132 * s, ct - 30 * s, x + 132 * s, ct + 4 * s, 14 * s, seed + 2, 1.6), WHITE, 8 * s)                 # lid
    wline(c, [(x + 30 * s, ct - 28 * s), (x + 60 * s, ct - 150 * s), (x + 110 * s, ct - 170 * s)], seed + 3, 22 * s, INK, 0.8)  # straw outline
    wline(c, [(x + 30 * s, ct - 28 * s), (x + 60 * s, ct - 150 * s), (x + 110 * s, ct - 170 * s)], seed + 3, 12 * s, YEL, 0.8)
    lab = wrrect(x - 92 * s, ct + 150 * s, x + 92 * s, ct + 214 * s, 12 * s, seed + 4, 1.4); ink(c, lab, WHITE, 6 * s)
    f = font(BLK_F, 40 * s); c.drawString(label, x - f.measureText(label) / 2, ct + 197 * s, f, P(col))
    _arms(c, x - 108 * s, x + 108 * s, ct + 120 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 64 * s, s, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x, ct + 112 * s, s * 0.8, talk, mood, seed + 5)


def _tag(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, price="$1.50", col=YEL, **kw):
    leg = 84 * s; cb = y - leg; ct = cb - 330 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 40)
    tg = wpoly([(x, ct), (x + 130 * s, ct + 90 * s), (x + 130 * s, cb), (x - 130 * s, cb), (x - 130 * s, ct + 90 * s)], seed, 2.2, True, 40); ink(c, tg, col, 9 * s)
    ink(c, wellipse(x, ct + 62 * s, 18 * s, 18 * s, seed, 1), PAPER, 7 * s)
    wline(c, [(x, ct + 50 * s), (x - 30 * s, ct - 40 * s), (x + 10 * s, ct - 90 * s)], seed + 2, 6 * s)
    f = font(BLK_F, 74 * s); tw = f.measureText(price)
    if tw > 230 * s: f = font(BLK_F, 74 * s * 230 * s / tw); tw = 230 * s
    c.drawString(price, x - tw / 2, cb - 40 * s, f, P(INK))
    _arms(c, x - 124 * s, x + 124 * s, ct + 190 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 130 * s, s * 0.9, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x, ct + 176 * s, s * 0.7, talk, mood, seed + 5)


def _card(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    leg = 80 * s; cb = y - leg; ct = cb - 220 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 50)
    cd = wrrect(x - 170 * s, ct, x + 170 * s, cb, 26 * s, seed, 2.0); ink(c, cd, BLU, 9 * s)
    c.save(); c.clipPath(cd, doAntiAlias=True); c.drawRect(skia.Rect.MakeLTRB(x - 180 * s, ct + 26 * s, x + 180 * s, ct + 62 * s), P(INK, 0.85)); c.restore()
    f = font(BLK_F, 34 * s); c.drawString("MEMBER", x - f.measureText("MEMBER") / 2, cb - 22 * s, f, P(WHITE))
    ink(c, wrrect(x - 140 * s, ct + 84 * s, x - 86 * s, ct + 124 * s, 6 * s, seed + 3, 1), YEL, 5 * s)
    _arms(c, x - 166 * s, x + 166 * s, ct + 130 * s, arms, t, s, seed + 7)
    eyes(c, x + 24 * s, ct + 104 * s, s * 0.85, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x + 24 * s, ct + 148 * s, s * 0.7, talk, mood, seed + 5)


def _bill(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    leg = 80 * s; cb = y - leg; ct = cb - 190 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 50)
    bl = wrrect(x - 170 * s, ct, x + 170 * s, cb, 12 * s, seed, 2.0); ink(c, bl, (140, 214, 140), 9 * s)
    ink(c, wrrect(x - 146 * s, ct + 20 * s, x + 146 * s, cb - 20 * s, 8 * s, seed + 2, 1.4), None, 4 * s, DGRN)
    f = font(BLK_F, 50 * s); c.drawString("$", x - 150 * s + 10 * s, ct + 66 * s, f, P(DGRN)); c.drawString("$", x + 110 * s, cb - 26 * s, f, P(DGRN))
    _arms(c, x - 166 * s, x + 166 * s, ct + 110 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 76 * s, s * 0.85, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x, ct + 124 * s, s * 0.7, talk, mood, seed + 5)


def _cart_char(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    cart(c, x, y, s, seed)


def _box(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=(52, 52, 60), label="PARTY GAME", fg=WHITE, lid=0.0, empty=False,
         poop=False, **kw):
    """generic product box character. lid 0..1 opens the top flap; empty shows an empty inside; poop adds a swirl + flies."""
    leg = 84 * s; cb = y - leg; ct = cb - 300 * s; w = 150 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 40)
    if lid > 0 or empty:   # opening: inside back wall
        ink(c, wpoly([(x - w, ct), (x + w, ct), (x + w * 0.86, ct - 40 * s), (x - w * 0.86, ct - 40 * s)], seed + 5, 1.6, True, 40), shade(col, 0.55), 8 * s)
    body = wpoly([(x - w, ct), (x + w, ct), (x + w, cb), (x - w, cb)], seed, 2.2, True, 40); ink(c, body, col, 9 * s)
    ink(c, wpoly([(x + w, ct), (x + w + 40 * s, ct - 30 * s), (x + w + 40 * s, cb - 30 * s), (x + w, cb)], seed + 1, 1.6, True, 40), shade(col, 0.7), 8 * s)
    if lid > 0:   # lid flap hinged on the back top edge, swinging up and back
        hgt = 2 * w * 0.55 * ease(lid); lean = 60 * s * ease(lid)
        ink(c, wpoly([(x - w + 40 * s, ct - 30 * s), (x + w + 40 * s, ct - 30 * s), (x + w + 40 * s - lean, ct - 30 * s - hgt), (x - w + 40 * s - lean, ct - 30 * s - hgt)], seed + 6, 1.4, True, 40), shade(col, 1.2), 7 * s)
    else:
        ink(c, wpoly([(x - w, ct), (x + w, ct), (x + w + 40 * s, ct - 30 * s), (x - w + 40 * s, ct - 30 * s)], seed + 2, 1.4, True, 40), shade(col, 1.25), 8 * s)
    if poop:
        sw = [(x - 30 * s, ct - 40 * s, 84 * s), (x - 20 * s, ct - 92 * s, 60 * s), (x - 10 * s, ct - 132 * s, 36 * s)]
        for i, (px, py, r) in enumerate(sw): ink(c, wellipse(px + 30 * s, py, r, r * 0.5, seed + i, 1.5), BROWN, 7 * s)
        for i in range(3):   # flies on little loops
            a = t * (5 + i) + i * 2.1; fx = x + 30 * s + math.cos(a) * 110 * s; fy = ct - 140 * s + math.sin(a * 1.3) * 50 * s
            c.drawCircle(fx, fy, 7 * s, P(INK)); wline(c, [(fx - 4, fy - 4), (fx - 14, fy - 16)], seed + i, 3); wline(c, [(fx + 4, fy - 4), (fx + 14, fy - 16)], seed + i, 3)
            wline(c, quad_pts(fx - 30 * s, fy + 10 * s, fx - 8 * s, fy, 10, 4), seed + i, 3, INK, 1, 0.5)
    ls = label.split("\n"); f = font(BLK_F, 34 * s)
    for i, l in enumerate(ls):
        tw = f.measureText(l); f2 = f if tw <= 2 * w - 30 * s else font(BLK_F, 34 * s * (2 * w - 30 * s) / tw); tw = min(tw, 2 * w - 30 * s)
        c.drawString(l, x - tw / 2, cb - 30 * s - (len(ls) - 1 - i) * 40 * s, f2, P(fg))
    _arms(c, x - w + 4 * s, x + w - 4 * s, ct + 150 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 70 * s, s, look, blink, 42, 27, mood, seed + 9)
    mouth(c, x, ct + 124 * s, s * 0.8, talk, mood, seed + 5)


def megaphone(c, x, y, s=1.0, rot=0.0, seed=191, word="SALE!", k=1.0, col=RED):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ink(c, wpoly([(-90, -40), (40, -100), (40, 100), (-90, 40)], seed, 2, True, 40), col, 9)
    ink(c, wrrect(-130, -40, -88, 40, 8, seed + 1, 1.2), WHITE, 8); ink(c, wrrect(-80, 30, -40, 110, 8, seed + 2, 1.2), INK, 0)
    if k > 0:
        for j in range(3): wline(c, quad_pts(70 + j * 26, -60 - j * 14, 70 + j * 26, 60 + j * 14, -30 - j * 8, 6), seed + j, 6, INK, 1, k)
        f = font(BLK_F, 64); c.drawString(word, 160, 22, f, P(col, k))
    c.restore()


def newspaper(c, x, y, s=1.0, rot=0.0, head="NEWS", seed=201):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ink(c, wrrect(-170, -220, 170, 220, 8, seed, 2), WHITE, 9)
    f = font(BLK_F, 40); tw = f.measureText(head); f = f if tw < 300 else font(BLK_F, 40 * 300 / tw); c.drawString(head, -min(tw, 300) / 2, -150, f, P(INK))
    wline(c, [(-150, -126), (150, -126)], seed + 1, 5)
    ink(c, wrrect(-150, -100, 10, 40, 6, seed + 2, 1.2), GREY, 5)
    for j in range(8): wline(c, [(30 if j < 5 else -150, -90 + j * 26), (150, -90 + j * 26)], seed + j, 4, GREY)
    c.restore()


def longbow(c, x, y, s=1.0, seed=211):
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, quad_pts(0, -220, 0, 220, -110, 10), seed, 16, BROWN, 1); wline(c, [(0, -220), (0, 220)], seed + 1, 3)
    wline(c, [(-60, 0), (150, 0)], seed + 2, 6, INK); ink(c, wpoly([(150, -16), (190, 0), (150, 16)], seed, 1, True, 20), GREY, 5)
    c.restore()


def glasses_eye(c, x, y, s=1.0, seed=221, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wellipse(0, 0, 150, 90, seed, 2), WHITE, 9); c.drawCircle(0, 0, 52, P(BLU)); c.drawCircle(0, 0, 24, P(INK)); c.drawCircle(-14, -14, 10, P(WHITE))
    for j in range(5):
        a = -0.5 + j * 0.25; wline(c, [(math.cos(a) * 180, -math.sin(a) * 120 - 40), (math.cos(a) * 240, -math.sin(a) * 160 - 60)], seed + j, 7, RED, 1, 0.5 + 0.5 * math.sin(t * 9 + j))
    c.restore()


def shovel_hole(c, x, y, k=1.0, seed=231): pass


def _mattress(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=(120, 190, 255), **kw):
    """inflatable air mattress standing up like a character: puffy quilted rectangle with a valve."""
    leg = 70 * s; cb = y - leg; ct = cb - 330 * s; w = 140 * s; puff = 1 + 0.02 * math.sin(t * 3)
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 50)
    body = wrrect(x - w * puff, ct, x + w * puff, cb, 60 * s, seed, 2.4); ink(c, body, col, 9 * s)
    c.save(); c.clipPath(body, doAntiAlias=True)
    for j in range(1, 4): wline(c, quad_pts(x - w, ct + j * 82 * s, x + w, ct + j * 82 * s, 10 * s, 8), seed + j, 5 * s, shade(col, 0.7))
    c.drawRect(skia.Rect.MakeLTRB(x - w * 1.1, ct, x - w * 0.55, cb), P(WHITE, 0.18)); c.restore(); ink(c, body, None, 9 * s)
    ink(c, wellipse(x + w * 0.62, ct + 30 * s, 12 * s, 12 * s, seed + 3, 1), WHITE, 5 * s)
    _arms(c, x - w + 6 * s, x + w - 6 * s, ct + 190 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 120 * s, s, look, blink, 42, 27, mood, seed + 9)
    mouth(c, x, ct + 176 * s, s * 0.8, talk, mood, seed + 5)


def cockroach(c, x, y, s=1.0, t=0.0, seed=241):
    c.save(); c.translate(x, y); c.scale(s, s)
    for j in range(3):
        for sx in (-1, 1):
            a = math.sin(t * 20 + j + sx) * 8; wline(c, [(sx * 30, -20 + j * 30), (sx * 80, -40 + j * 40 + a), (sx * 100, -10 + j * 40 + a)], seed + j, 6)
    ink(c, wellipse(0, 20, 50, 80, seed, 1.5), BROWN, 8); ink(c, wellipse(0, -70, 34, 28, seed + 1, 1), shade(BROWN, 0.8), 7)
    wline(c, [(-14, -94), (-60, -170)], seed + 2, 5); wline(c, [(14, -94), (60, -170)], seed + 3, 5)
    eyes(c, 0, -76, 0.55, (0, -0.3), False, 40, 26, "happy", seed + 4); c.restore()


def camera(c, x, y, s=1.0, seed=251, flash=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-170, -100, 170, 120, 26, seed, 2), (60, 62, 70), 9); ink(c, wrrect(-80, -150, 40, -96, 10, seed + 1, 1.2), (60, 62, 70), 8)
    ink(c, wellipse(0, 10, 80, 80, seed + 2, 1.5), GREY, 9); ink(c, wellipse(0, 10, 48, 48, seed + 3, 1.2), INK, 6)
    c.drawCircle(-16, -8, 12, P(WHITE, 0.9)); ink(c, wrrect(100, -80, 150, -50, 6, seed + 4, 1), YEL, 5)
    if flash > 0:
        for j in range(8):
            a = j / 8 * math.tau; wline(c, [(125 + math.cos(a) * 50, -65 + math.sin(a) * 50), (125 + math.cos(a) * 110, -65 + math.sin(a) * 110)], seed + j, 8, YEL, 1, flash)
    c.restore()


def photo(c, x, y, w, h, good=True, rot=0.0, seed=261, k=1.0):
    """listing photo: good = bright room with bed + window; bad = dark, blurry, crooked."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    ink(c, wrrect(-w / 2 - 16, -h / 2 - 16, w / 2 + 16, h / 2 + 40, 6, seed, 1.6), WHITE, 7)
    inner = skia.Path(); inner.addRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2))
    c.save(); c.clipPath(inner, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), P((255, 236, 200) if good else (70, 66, 64)))
    c.drawRect(skia.Rect.MakeLTRB(-w / 2, h * 0.15, w / 2, h / 2), P((230, 170, 110) if good else (52, 48, 46)))
    ink(c, wrrect(w * 0.08, -h * 0.38, w * 0.4, -h * 0.02, 6, seed + 1, 1), SKY if good else (90, 96, 104), 5)
    ink(c, wrrect(-w * 0.42, -h * 0.02, w * 0.02, h * 0.3, 10, seed + 2, 1), (255, 255, 255) if good else (120, 116, 110), 5)
    ink(c, wrrect(-w * 0.42, -h * 0.12, -w * 0.28, h * 0.02, 6, seed + 3, 1), PNK if good else (100, 90, 90), 4)
    if good:
        for j in range(4): wline(c, [(w * 0.24, -h * 0.5), (w * (-0.1 + j * 0.15), h * 0.5)], seed + j, 5, YEL, 1, 0.35)
    c.restore()
    if not good:
        c.drawRect(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), P((20, 20, 20), 0.25))
    c.restore()


def binder(c, x, y, s=1.0, seed=271, n=6, k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-230, -170, 230, 170, 16, seed, 2), (40, 70, 160), 9); wline(c, [(0, -170), (0, 170)], seed + 1, 8)
    for r in range(3): ink(c, wellipse(0, -110 + r * 110, 12, 12, seed + r, 1), GREY, 5)
    for i in range(min(n, int(n * k + 0.999))):
        q, r = divmod(i, 3); cx = -115 + q * 230; cy = -105 + r * 105
        ink(c, wrrect(cx - 90, cy - 44, cx + 90, cy + 44, 10, seed + i, 1.2), (YEL, GRN, PNK, ORG, SKY, PUR)[i % 6], 6)
        c.drawRect(skia.Rect.MakeLTRB(cx - 90, cy - 26, cx + 90, cy - 10), P(INK, 0.8))
        f = font(BLK_F, 22); c.drawString("MAXED", cx - f.measureText("MAXED") / 2, cy + 30, f, P(RED))
    c.restore()


def laptop(c, x, y, s=1.0, seed=281, title_="AirBed & Breakfast", k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-260, -320, 260, 0, 18, seed, 2), (70, 72, 80), 9); ink(c, wrrect(-230, -295, 230, -25, 8, seed + 1, 1.2), WHITE, 0)
    ink(c, wpoly([(-310, 0), (310, 0), (350, 50), (-350, 50)], seed + 2, 1.6, True, 60), GREY, 9)
    if k > 0:
        f = font(BLK_F, 34); c.drawString(title_, -f.measureText(title_) / 2, -240, f, P(RED, k))
        for j in range(3):
            bx = -200 + j * 140; ink(c, wrrect(bx, -200, bx + 120, -110, 8, seed + j, 1), SKY, 5)
            f2 = font(BLK_F, 28); c.drawString("$80", bx + 30, -70, f2, P(INK, k))
    c.restore()


# ------------------------------------------------------------------ props
def building(c, x, y, w=360, h=520, col=SKY, seed=31, label=None, lit=True):
    """office tower standing on (x, y)."""
    ink(c, wpoly([(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)], seed, 2.4, True, 50), col, 9)
    for r in range(int((h - 140) / 90)):
        for q in range(3):
            wx = x - w / 2 + 40 + q * (w - 80) / 3 + 8; wy = y - h + 40 + r * 90
            ink(c, wrrect(wx, wy, wx + (w - 80) / 3 - 16, wy + 56, 6, seed + r * 3 + q, 1.2), YEL if (lit and (r + q) % 3 == 0) else WHITE, 5)
    ink(c, wrrect(x - 44, y - 110, x + 44, y, 6, seed + 9, 1.2), shade(col, 0.7), 7)
    if label: tape(c, label, x, y - h - 10, 40, -3, 1.0, seed=seed)


def factory(c, x, y, t, s=1.0, seed=41, run=True):
    w, h = 560 * s, 300 * s; x0 = x - w / 2
    roof = [(x0, y - h)]
    for i in range(3): roof += [(x0 + i * w / 3, y - h - 90 * s), (x0 + (i + 1) * w / 3, y - h)]
    ink(c, wpoly([(x0, y)] + roof + [(x0 + w, y)], seed, 2.4, True, 50), (232, 104, 84), 9)
    ink(c, wpoly([(x0 + w - 120 * s, y - h - 40 * s), (x0 + w - 120 * s, y - h - 230 * s), (x0 + w - 60 * s, y - h - 230 * s), (x0 + w - 60 * s, y - h)], seed + 1, 2, True, 40), GREY, 8)
    for i in range(4):   # smoke puffs drift up
        u = ((t * 0.5 + i * 0.25) % 1.0) if run else i * 0.25; r = (26 + 40 * u) * s
        ink(c, wellipse(x0 + w - 90 * s + 40 * u * s, y - h - 260 * s - u * 240 * s, r, r * 0.8, seed + i, 2), (236, 236, 240), 6, a=1 - u * 0.7)
    for q in range(3): ink(c, wrrect(x0 + 50 * s + q * 170 * s, y - h + 50 * s, x0 + 150 * s + q * 170 * s, y - h + 130 * s, 8, seed + q, 1.2), SKY, 6)
    # conveyor out the front with little hot dogs
    by = y - 30 * s; ink(c, wrrect(x0 - 40 * s, by - 26 * s, x0 + w + 40 * s, by + 10 * s, 18 * s, seed + 7, 1.4), GREY, 7)
    for i in range(7):
        hx = x0 - 20 * s + ((i * 100 + (t * 160 if run else 0)) % (w + 40)) * s / s
        ink(c, wrrect(hx, by - 64 * s, hx + 80 * s, by - 30 * s, 16 * s, seed + i, 1), SAUS, 5)
        ink(c, wrrect(hx + 6 * s, by - 50 * s, hx + 74 * s, by - 26 * s, 12 * s, seed + i + 9, 1), TAN, 5)


def calendar(c, x, y, year, s=1.0, k=1.0, seed=51, col=RED):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k * s, k * s)
    ink(c, wrrect(-170, -190, 170, 190, 18, seed, 2), WHITE, 9)
    c.save(); c.clipPath(wrrect(-170, -190, 170, 190, 18, seed, 0), doAntiAlias=True); c.drawRect(skia.Rect.MakeLTRB(-180, -200, 180, -90), P(col)); c.restore()
    wline(c, [(-170, -90), (170, -90)], seed + 1, 8)
    for i in range(5): ink(c, wrrect(-130 + i * 60, -214, -114 + i * 60, -170, 8, seed + i, 1), GREY, 5)
    f = font(BLK_F, 116); s_ = str(year); c.drawString(s_, -f.measureText(s_) / 2, 90, f, P(INK))
    f2 = font(BLK_F, 40); c.drawString("YEAR", -f2.measureText("YEAR") / 2, -128, f2, P(WHITE))
    c.restore()


def balloon(c, x, y, r, s_="$4+", seed=61, col=RED, t=0.0):
    yy = y + math.sin(t * 2) * 8
    wline(c, [(x, yy + r * 1.1), (x - 20, yy + r * 1.6), (x + 14, yy + r * 2.1), (x, yy + r * 2.7)], seed, 5)
    ink(c, wpoly([(x - 14, yy + r * 1.1), (x + 14, yy + r * 1.1), (x, yy + r * 0.96)], seed, 1, True, 20), col, 6)
    ink(c, wellipse(x, yy, r * 0.92, r * 1.06, seed, 2.4), col, 9)
    c.drawPath(wellipse(x - r * 0.38, yy - r * 0.45, r * 0.14, r * 0.24, seed + 2, 1), P(WHITE, 0.8))
    f = font(BLK_F, r * 0.62); c.drawString(s_, x - f.measureText(s_) / 2, yy + r * 0.22, f, P(WHITE))


def padlock(c, x, y, s=1.0, k=1.0, seed=71):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    wline(c, quad_pts(-60, 0, 60, 0, -150, 10), seed, 26, INK, 1); wline(c, quad_pts(-60, 0, 60, 0, -150, 10), seed, 12, GREY, 1)
    ink(c, wrrect(-100, -10, 100, 150, 24, seed + 1, 2), YEL, 9); ink(c, wellipse(0, 60, 16, 16, seed, 1), INK, 0)
    c.drawRect(skia.Rect.MakeLTRB(-7, 60, 7, 104), P(INK)); c.restore()


def ice(c, x, y, w, h, seed=81, a=0.55):
    pth = wrrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 30, seed, 3); ink(c, pth, (170, 226, 255), 8, (60, 140, 210), a)
    c.drawPath(pth, S((60, 140, 210), 8, 0.9))
    for i in range(3): wline(c, [(x - w / 2 + 30 + i * 26, y - h / 2 + 40), (x - w / 2 + 60 + i * 26, y - h / 2 + 120)], seed + i, 7, WHITE, 1, 0.8)


def pie(c, x, y, r, frac, k=1.0, seed=91, cols=(GRN, GREY), labels=None):
    ink(c, wellipse(x, y, r, r, seed, 2), cols[1], 9)
    f = frac * min(1.0, k)
    if f > 0:
        pth = skia.Path(); pth.moveTo(x, y); pth.arcTo(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -90, 360 * f, False); pth.close()
        c.save(); c.clipPath(wellipse(x, y, r, r, seed, 2), doAntiAlias=True); c.drawPath(pth, P(cols[0])); c.restore()
        a = math.radians(-90 + 360 * f); wline(c, [(x, y), (x, y - r)], seed + 1, 8); wline(c, [(x, y), (x + r * math.cos(a), y + r * math.sin(a))], seed + 2, 8)
    ink(c, wellipse(x, y, r, r, seed, 2), None, 9)


def wallet(c, x, y, s=1.0, seed=101, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-200, -40 - 60 * open_, 200, 150, 30, seed, 2), BROWN, 9)
    ink(c, wrrect(-200, 10, 200, 150, 26, seed + 1, 2), shade(BROWN, 1.15), 9)
    wline(c, [(-170, 40), (170, 40)], seed + 2, 4, shade(BROWN, 0.6)); c.restore()


def tray(c, x, y, s=1.0, seed=111):
    ink(c, wpoly([(x - 300 * s, y - 30 * s), (x + 300 * s, y - 30 * s), (x + 270 * s, y + 20 * s), (x - 270 * s, y + 20 * s)], seed, 2, True, 60), RED, 9)


def cart(c, x, y, s=1.0, seed=121, items=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    if items:
        for i, (ix, col) in enumerate(((-90, GRN), (-10, YEL), (70, PNK), (-50, BLU), (30, ORG))):
            iy = -230 - (40 if i >= 3 else 0); ink(c, wrrect(ix - 40, iy - 70, ix + 40, iy + 20, 10, seed + i, 1.4), col, 7)
    basket = wpoly([(-170, -260), (170, -260), (130, -110), (-130, -110)], seed, 2, True, 40); ink(c, basket, WHITE, 9)
    c.save(); c.clipPath(basket, doAntiAlias=True)
    for i in range(-6, 7): c.drawLine(i * 30, -270, i * 30 + 20, -100, S(INK, 4))
    for j in range(4): c.drawLine(-180, -230 + j * 36, 180, -230 + j * 36, S(INK, 4))
    c.restore(); ink(c, basket, None, 9)
    wline(c, [(170, -260), (220, -320), (260, -320)], seed + 1, 10)
    wline(c, [(-120, -110), (-110, -40), (130, -40), (130, -110)], seed + 2, 9)
    for wx in (-100, 110): ink(c, wellipse(wx, -18, 20, 20, seed + wx, 1), INK, 0)
    c.restore()


def store(c, x, y, w=760, h=420, seed=131, sign=None):
    ink(c, wpoly([(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)], seed, 2.4, True, 60), (236, 236, 228), 9)
    ink(c, wpoly([(x - w / 2 - 20, y - h), (x - w / 2 - 20, y - h - 70), (x + w / 2 + 20, y - h - 70), (x + w / 2 + 20, y - h)], seed + 1, 2, True, 60), RED, 9)
    if sign: f = font(BLK_F, 50); c.drawString(sign, x - f.measureText(sign) / 2, y - h - 18, f, P(WHITE))
    ink(c, wrrect(x - 110, y - 190, x + 110, y, 6, seed + 2, 1.4), SKY, 8); wline(c, [(x, y - 190), (x, y)], seed + 3, 6)
    for sx in (-1, 1):
        for q in range(2): ink(c, wrrect(x + sx * (170 + q * 120) - 50, y - 300, x + sx * (170 + q * 120) + 50, y - 220, 8, seed + q * 3 + sx, 1.2), SKY, 6)


def mic(c, x, y, s=1.0, seed=141):
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, [(0, 0), (0, -300)], seed, 12); ink(c, wellipse(0, 6, 90, 18, seed, 1), INK, 0)
    ink(c, wrrect(-46, -460, 46, -300, 46, seed + 1, 2), GREY, 9)
    for j in range(4): wline(c, [(-40, -430 + j * 30), (40, -430 + j * 30)], seed + j, 4, shade(GREY, 0.6))
    c.restore()


def phone(c, x, y, s=1.0, seed=151, screen=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-120, -230, 120, 230, 34, seed, 2), INK, 9)
    ink(c, wrrect(-100, -190, 100, 190, 16, seed + 1, 1.4), WHITE, 0)
    if screen: screen(c)
    c.restore()


def checklist(c, x, y, items, k_list, seed=161, w=820):
    h = 120 + 150 * len(items)
    ink(c, wrrect(x - w / 2, y, x + w / 2, y + h, 20, seed, 2), WHITE, 9)
    for i, (s_, k) in enumerate(zip(items, k_list)):
        yy = y + 90 + i * 150; ink(c, wrrect(x - w / 2 + 50, yy - 40, x - w / 2 + 120, yy + 30, 8, seed + i, 1.4), WHITE, 7)
        if k > 0:
            wline(c, [(x - w / 2 + 58, yy - 4), (x - w / 2 + 84, yy + 24), (x - w / 2 + 134, yy - 56)][:2 + (k > 0.5)], seed + i, 11, GRN, 1)
            ls = wrap(s_, HAND_F, 54, w - 220); f = font(HAND_F, 54)
            for j, l in enumerate(ls): c.drawString(l, x - w / 2 + 160, yy + 14 + j * 58 - (len(ls) - 1) * 29, f, P(INK, min(1, k * 2)))


def coin_rain(c, t, t0, n=10, seed=171, y_end=1400):
    if t < t0: return
    for i in range(n):
        u = (t - t0) * (1.0 + h01(i, seed) * 0.6) - h01(i + 9, seed) * 0.8
        if u <= 0: continue
        x = 140 + h01(i + 3, seed) * 800; y = 520 + u * 900
        if y > y_end: continue
        c.save(); c.translate(x, y); c.rotate(u * 200 * (1 if i % 2 else -1))
        ink(c, wrrect(-60, -30, 60, 30, 6, seed + i, 1), (140, 214, 140), 6); f = font(BLK_F, 34); c.drawString("$", -10, 12, f, P(DGRN))
        c.restore()


def finish(img, flash=0.0):
    if flash: img = img * (1 - flash) + flash
    return np.clip(img, 0, 1)
