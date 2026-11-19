"""DOODLE kit for OopsMyBusiness (owner, 13 Nov 2026, sent 4 doodle-explainer screenshots: "Create this type of animation").
Graph-paper page, thick wobbly black ink outlines with flat vibrant fills, line boil on twos (outlines re-jitter every 2 frames),
hatched ground band, object characters with eyes and stick limbs, torn-paper transcript strip, orange tape labels, red stamps,
hand-drawn speech bubbles, scribble circles and arrows. Our own drawing code, generic objects only — no logos, no brand trade dress.
Skia. Used by exec() from anim_shots.py (needs W, H; defines BOIL which the renderer sets per frame).
"""
import math, os, re
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


def page(c, tint=None, a=0.10):
    global _PAGE
    if _PAGE is None: _PAGE = _make_page()
    c.drawImage(_PAGE, 0, 0)
    if tint: c.drawRect(skia.Rect.MakeWH(W, H), P(tint, a))


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
def strip(c, words, t_cursor=True, y0=262, size=42, t=0.0):
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
    fn = {"hotdog": _hotdog, "soda": _soda, "tag": _tag, "card": _card, "bill": _bill, "cart": _cart_char, "box": _box, "mattress": _mattress, "fax": _fax, "scissors": _scissors, "tub": _tub, "pbar": _pbar, "choc": _choc, "pista": _pista, "razor": _razor, "spray": _spray, "cat": _cat, "tallcan": _tallcan, "chunky": _chunkyshoe, "sauce": _sauce, "hoodie": _hoodie}[kind]
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


def _fax(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    """old office fax machine character: beige body, paper tray, handset, a page curling out."""
    leg = 70 * s; cb = y - leg; ct = cb - 220 * s; w = 170 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 60)
    ink(c, wpoly([(x - w, cb), (x - w, ct + 40 * s), (x - w * 0.6, ct), (x + w, ct), (x + w, cb)], seed, 2.2, True, 40), (232, 222, 196), 9 * s)
    ink(c, wrrect(x - w * 0.9, ct - 70 * s, x + w * 0.3, ct + 6 * s, 30 * s, seed + 1, 1.6), (120, 116, 108), 8 * s)        # handset
    pg = math.sin(t * 3) * 6 * s
    ink(c, wpoly([(x + w * 0.35, ct + 4 * s), (x + w * 0.95, ct + 4 * s), (x + w * 0.9 + pg, ct - 120 * s), (x + w * 0.4 + pg, ct - 110 * s)], seed + 2, 1.4, True, 40), WHITE, 6 * s)
    for j in range(3): wline(c, [(x + w * 0.47 + pg, ct - 90 * s + j * 26 * s), (x + w * 0.83 + pg, ct - 94 * s + j * 26 * s)], seed + j, 3 * s, GREY)
    for q in range(3):
        for r in range(2): ink(c, wrrect(x + w * 0.3 + q * 34 * s, ct + 120 * s + r * 34 * s, x + w * 0.3 + q * 34 * s + 24 * s, ct + 120 * s + r * 34 * s + 24 * s, 4 * s, seed + q + r, 0.8), WHITE, 4 * s)
    _arms(c, x - w + 6 * s, x + w - 6 * s, ct + 130 * s, arms, t, s, seed + 7)
    eyes(c, x - 60 * s, ct + 90 * s, s * 0.9, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x - 60 * s, ct + 150 * s, s * 0.7, talk, mood, seed + 5)


def _scissors(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, snip=0.0, **kw):
    """standing scissors character: two blades (open by snip 0..1) and two finger loops as the 'head'."""
    leg = 60 * s; cb = y - leg; piv = cb - 230 * s; a = math.radians(8 + 22 * snip)
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 30)
    for sx in (-1, 1):
        tip = (x + sx * math.sin(a) * 260 * s, piv + math.cos(a) * 0 - 0 * s)
        bl = [(x, piv), (x + sx * math.sin(a) * 250 * s - sx * 10 * s, piv - math.cos(a) * 250 * s), (x + sx * math.sin(a) * 250 * s + sx * 18 * s, piv - math.cos(a) * 240 * s), (x + sx * 26 * s, piv + 10 * s)]
        ink(c, wpoly(bl, seed + sx, 1.4, True, 40), (210, 214, 222), 8 * s)
        lx = x + sx * 70 * s; ly = piv + 110 * s
        wline(c, [(x + sx * 12 * s, piv + 10 * s), (lx, ly - 40 * s)], seed + sx + 4, 22 * s, RED, 1)
        ink(c, wellipse(lx, ly, 52 * s, 64 * s, seed + sx + 6, 1.6), RED, 9 * s); ink(c, wellipse(lx, ly, 30 * s, 40 * s, seed + sx + 8, 1.2), PAPER, 6 * s)
    ink(c, wellipse(x, piv, 16 * s, 16 * s, seed + 3, 1), GREY, 6 * s)
    _arms(c, x - 110 * s, x + 110 * s, piv + 90 * s, arms, t, s, seed + 7)
    eyes(c, x, piv - 60 * s, s * 0.8, look, blink, 34, 24, mood, seed + 9)
    mouth(c, x, piv - 14 * s, s * 0.6, talk, mood, seed + 5)


def pants(c, x, y, s=1.0, seed=291, col=WHITE):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-120, -260), (120, -260), (140, 240), (30, 240), (0, -60), (-30, 240), (-140, 240)], seed, 2, True, 50), col, 9)
    wline(c, [(-120, -220), (120, -220)], seed + 1, 5, GREY); c.drawCircle(0, -240, 8, P(GREY)); c.restore()


def stockings(c, x, y, s=1.0, seed=301, cut=0.0):
    """footless tan stockings on a hanger; cut 0..1 removes the feet (the snip)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, [(-150, -300), (0, -360), (150, -300), (-150, -300)], seed, 7, GREY); wline(c, [(0, -360), (0, -400), (24, -420)], seed + 1, 7, GREY)
    for sx in (-1, 1):
        L = 300 if cut < 0.5 else 230
        pth = wpoly([(sx * 20, -300), (sx * 110, -300), (sx * 95, -300 + L), (sx * 35, -300 + L)], seed + sx, 1.6, True, 40); ink(c, pth, (232, 190, 150), 7)
        if cut < 0.5: ink(c, wellipse(sx * 75, -300 + L + 10, 50, 26, seed + sx + 3, 1.2), (232, 190, 150), 7)
        else:
            fy = -300 + 240 + 140 * min(1, (cut - 0.5) * 2); ink(c, wellipse(sx * 90, fy + 60, 50, 26, seed + sx + 3, 1.2), (232, 190, 150), 6, a=1 - (cut - 0.5))
    c.restore()


def book(c, x, y, s=1.0, title_="PATENTS", seed=311, col=(40, 90, 170)):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-150, -200, 150, 200, 12, seed, 2), col, 9); wline(c, [(-120, -200), (-120, 200)], seed + 1, 6, shade(col, 0.6))
    f = font(BLK_F, 40); tw = f.measureText(title_); c.drawString(title_, 15 - tw / 2, -60, f, P(WHITE))
    f2 = font(BLK_F, 24); c.drawString("& TRADEMARKS", 15 - f2.measureText("& TRADEMARKS") / 2, -20, f2, P(YEL)); c.restore()


def plane(c, x, y, s=1.0, rot=-12, seed=321):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ink(c, wrrect(-220, -40, 220, 40, 40, seed, 2), WHITE, 9)
    ink(c, wpoly([(-40, 0), (60, 0), (-40, 160), (-90, 160)], seed + 1, 1.4, True, 40), SKY, 8); ink(c, wpoly([(-40, 0), (60, 0), (-40, -150), (-90, -150)], seed + 2, 1.4, True, 40), SKY, 8)
    ink(c, wpoly([(-200, -20), (-170, -20), (-210, -120), (-240, -120)], seed + 3, 1.2, True, 40), RED, 7)
    for j in range(5): c.drawCircle(-100 + j * 50, -8, 9, P(SKY))
    c.restore()


def restroom_door(c, x, y, s=1.0, seed=331, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-170, 0), (-170, -520), (170, -520), (170, 0)], seed, 2, True, 50), (200, 170, 140), 9)
    ink(c, wrrect(-80, -440, 80, -330, 10, seed + 1, 1.2), WHITE, 7)
    f = font(BLK_F, 34); c.drawString("LADIES", -f.measureText("LADIES") / 2, -372, f, P(PNK))
    c.drawCircle(120, -250, 14, P(INK)); c.restore()


def register(c, x, y, s=1.0, seed=341, open_=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-200, 0), (-200, -180), (200, -180), (200, 0)], seed, 2, True, 50), (110, 200, 160), 9)
    ink(c, wpoly([(-150, -180), (-120, -320), (150, -320), (170, -180)], seed + 1, 2, True, 50), (90, 180, 140), 9)
    ink(c, wrrect(-110, -300, 120, -240, 8, seed + 2, 1), INK, 0); f = font(BLK_F, 40); c.drawString("$$$", -40, -255, f, P(GRN))
    for q in range(4):
        for r in range(2): ink(c, wrrect(-120 + q * 64, -220 + r * 40, -80 + q * 64, -190 + r * 40, 4, seed + q + r, 0.8), WHITE, 4)
    ink(c, wrrect(-210, 0, 210, 60 + 50 * open_, 8, seed + 5, 1.4), (90, 180, 140), 8); c.restore()


def envelope(c, x, y, s=1.0, seed=351, heart=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-200, -130, 200, 130, 10, seed, 2), WHITE, 9); wline(c, [(-196, -126), (0, 20), (196, -126)], seed + 1, 7)
    if heart:
        h = skia.Path(); h.moveTo(0, 90); h.cubicTo(-90, 30, -50, -40, 0, -5); h.cubicTo(50, -40, 90, 30, 0, 90); c.drawPath(h, P(RED))
    c.restore()


def magazine(c, x, y, s=1.0, seed=361, head="MAGAZINE", line2="YOUNGEST SELF-MADE"):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-200, -270, 200, 270, 8, seed, 2), (255, 220, 60), 9)
    f = font(ANTON_F, 70); c.drawString(head, -f.measureText(head) / 2, -170, f, P(RED))
    ink(c, wellipse(0, 20, 110, 130, seed + 1, 2), (255, 236, 210), 7)
    f2 = font(BLK_F, 26); c.drawString(line2, -f2.measureText(line2) / 2, 210, f2, P(INK)); c.restore()


def ticket(c, x, y, s=1.0, rot=0.0, seed=371):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    ink(c, wrrect(-170, -70, 170, 70, 12, seed, 1.6), (120, 200, 255), 8); wline(c, [(70, -70), (70, 70)], seed + 1, 4, WHITE)
    f = font(BLK_F, 30); c.drawString("1ST CLASS", -150, -10, f, P(INK)); f2 = font(BLK_F, 22); c.drawString("ANYWHERE", -150, 30, f2, P(INK, 0.7))
    c.restore()


def _tub(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=(40, 40, 52), label="PROTEIN", **kw):
    """protein powder tub character: wide jar, screw lid, scoop poking out, big label band."""
    leg = 70 * s; cb = y - leg; ct = cb - 300 * s; w = 140 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 50)
    ink(c, wrrect(x - w, ct, x + w, cb, 30 * s, seed, 2.2), col, 9 * s)
    ink(c, wrrect(x - w - 10 * s, ct - 50 * s, x + w + 10 * s, ct + 10 * s, 14 * s, seed + 1, 1.6), (240, 80, 60), 8 * s)
    for j in range(7): wline(c, [(x - w + 20 * s + j * 38 * s, ct - 44 * s), (x - w + 20 * s + j * 38 * s, ct + 4 * s)], seed + j, 3 * s, shade((240, 80, 60), 0.7))
    band = wrrect(x - w + 14 * s, ct + 150 * s, x + w - 14 * s, ct + 240 * s, 10 * s, seed + 2, 1.4); ink(c, band, (255, 214, 40), 6 * s)
    f = font(BLK_F, 42 * s); tw = f.measureText(label); f = f if tw < 2 * w - 50 * s else font(BLK_F, 42 * s * (2 * w - 50 * s) / tw)
    c.drawString(label, x - min(tw, 2 * w - 50 * s) / 2, ct + 210 * s, f, P(INK))
    _arms(c, x - w + 6 * s, x + w - 6 * s, ct + 130 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 64 * s, s * 0.9, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x, ct + 114 * s, s * 0.7, talk, mood, seed + 5)


def _pbar(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=(250, 250, 246), lines_=("EGG WHITES", "DATES", "NUTS"), **kw):
    """protein bar character standing up: plain wrapper with crimped ends, ingredients printed big on the front."""
    leg = 70 * s; cb = y - leg; ct = cb - 380 * s; w = 100 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 34)
    body = wpoly([(x - w, ct + 20 * s), (x + w, ct + 20 * s), (x + w, cb - 20 * s), (x - w, cb - 20 * s)], seed, 2, True, 40); ink(c, body, col, 9 * s)
    for yy, d in ((ct + 20 * s, -1), (cb - 20 * s, 1)):
        pts = [(x - w + i * (2 * w) / 8, yy + d * (14 if i % 2 else 2) * s) for i in range(9)]
        wline(c, pts, seed + int(yy), 7 * s)
    f = font(BLK_F, 30 * s)
    for i, l in enumerate(lines_):
        tw = f.measureText(l); ff = f if tw < 2 * w - 20 * s else font(BLK_F, 30 * s * (2 * w - 20 * s) / tw)
        c.drawString(l, x - min(tw, 2 * w - 20 * s) / 2, ct + 230 * s + i * 40 * s, ff, P(INK))
    _arms(c, x - w + 4 * s, x + w - 4 * s, ct + 170 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 100 * s, s * 0.8, look, blink, 36, 24, mood, seed + 9)
    mouth(c, x, ct + 150 * s, s * 0.6, talk, mood, seed + 5)


def pint(c, x, y, s=1.0, seed=381, col=(255, 150, 190), label="PROTEIN"):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-110, -240), (110, -240), (90, 0), (-90, 0)], seed, 2, True, 40), col, 9)
    ink(c, wrrect(-120, -280, 120, -230, 12, seed + 1, 1.4), WHITE, 8)
    f = font(BLK_F, 34); c.drawString(label, -f.measureText(label) / 2, -110, f, P(WHITE)); c.restore()


def pocket(c, x, y, s=1.0, seed=391):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-200, 0), (0, -150), (200, 0)], seed, 2, True, 40), (245, 220, 170), 9)
    for j, col in enumerate((GRN, RED, (240, 200, 160))): ink(c, wellipse(-80 + j * 70, -30, 50, 22, seed + j, 1), col, 5)
    c.restore()


def bowl(c, x, y, s=1.0, seed=401):
    c.save(); c.translate(x, y); c.scale(s, s)
    for j, (bx, col) in enumerate(((-90, GRN), (-20, (240, 200, 160)), (60, ORG), (120, RED))): ink(c, wellipse(bx, -70, 60, 34, seed + j, 1), col, 5)
    ink(c, wpoly([(-230, -60), (230, -60), (150, 40), (-150, 40)], seed + 5, 2, True, 50), WHITE, 9); c.restore()


def kettlebell(c, x, y, s=1.0, seed=411):
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, quad_pts(-60, -150, 60, -150, -110, 10), seed, 24, INK); ink(c, wellipse(0, -60, 110, 100, seed + 1, 2), (60, 62, 70), 9)
    f = font(BLK_F, 40); c.drawString("16", -24, -40, f, P(WHITE)); c.restore()


def cookie(c, x, y, s=1.0, seed=421):
    c.save(); c.translate(x, y); c.scale(s, s); ink(c, wellipse(0, 0, 120, 110, seed, 3), (220, 160, 90), 9)
    for j in range(6): c.drawCircle(-60 + (j * 47) % 120, -50 + (j * 37) % 100, 14, P(BROWN))
    c.restore()


def nutrition(c, x, y, s=1.0, seed=431, grams="10g", hl=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-200, -260, 200, 260, 8, seed, 1.6), WHITE, 8)
    f = font(BLK_F, 40); c.drawString("Nutrition Facts", -180, -200, f, P(INK)); wline(c, [(-180, -180), (180, -180)], seed + 1, 10)
    rows = [("Calories", "200"), ("Fat", "7g"), ("Carbs", "20g"), ("Protein", grams)]
    for i, (a_, b_) in enumerate(rows):
        yy = -110 + i * 80; f2 = font(BLK_F if a_ == "Protein" else XB_F, 40); c.drawString(a_, -180, yy, f2, P(INK)); c.drawString(b_, 180 - f2.measureText(b_), yy, f2, P(INK))
        wline(c, [(-180, yy + 22), (180, yy + 22)], seed + i, 3, GREY)
    if hl > 0: scribble(c, 0, 128, 220, 50, hl, RED, 8, seed + 9)
    c.restore()


def stall(c, x, y, s=1.0, seed=441, sign="SAMPLES"):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1): wline(c, [(sx * 230, 0), (sx * 230, -420)], seed + sx, 10)
    ink(c, wpoly([(-270, -420), (270, -420), (230, -320), (-230, -320)], seed, 2, True, 60), RED, 9)
    for j in range(5): c.drawRect(skia.Rect.MakeLTRB(-230 + j * 92, -410, -230 + j * 92 + 46, -330), P(WHITE, 0.85))
    ink(c, wrrect(-260, -200, 260, -140, 8, seed + 2, 1.4), (200, 150, 100), 8)
    f = font(BLK_F, 40); c.drawString(sign, -f.measureText(sign) / 2, -240, f, P(INK)); c.restore()


def _choc(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, crack=0.0, **kw):
    """thick chocolate bar character (grid of squares); crack 0..1 splits the top-right corner off and shows the green filling."""
    leg = 70 * s; cb = y - leg; ct = cb - 380 * s; w = 140 * s; MIL = (120, 70, 40)
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 50)
    body = wrrect(x - w, ct, x + w, cb, 24 * s, seed, 2.2); ink(c, body, MIL, 9 * s)
    for q in range(2):
        for r in range(3):
            if crack > 0 and q == 1 and r == 0: continue
            ink(c, wrrect(x - w + 24 * s + q * (w - 10 * s), ct + 22 * s + r * 116 * s, x - w + 24 * s + q * (w - 10 * s) + w - 34 * s, ct + 22 * s + r * 116 * s + 100 * s, 10 * s, seed + q * 3 + r, 1.2), shade(MIL, 1.18), 5 * s)
    if crack > 0:
        u = ease(crack); gx, gy = x + 10 * s, ct
        fill = wpoly([(gx, gy + 10 * s), (x + w, gy + 10 * s), (x + w, gy + 130 * s), (gx, gy + 130 * s)], seed + 7, 2, True, 30); ink(c, fill, (150, 200, 60), 6 * s)
        for j in range(6): wline(c, [(gx + 10 * s + j * 22 * s, gy + 30 * s), (gx + 20 * s + j * 22 * s, gy + 110 * s)], seed + j, 4 * s, (220, 170, 90))
        c.save(); c.translate(x + w * 0.55 + 90 * s * u, ct + 60 * s - 120 * s * u); c.rotate(28 * u)
        ink(c, wrrect(-w * 0.45, -60 * s, w * 0.45, 60 * s, 12 * s, seed + 9, 1.6), MIL, 7 * s); ink(c, wrrect(-w * 0.45, 30 * s, w * 0.45, 60 * s, 8 * s, seed + 10, 1), (150, 200, 60), 4 * s); c.restore()
    _arms(c, x - w + 6 * s, x + w - 6 * s, ct + 190 * s, arms, t, s, seed + 7)
    eyes(c, x - 10 * s, ct + 190 * s, s * 0.9, look, blink, 40, 26, mood, seed + 11)
    mouth(c, x - 10 * s, ct + 246 * s, s * 0.7, talk, mood, seed + 5)


def _pista(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, **kw):
    """pistachio character: beige split shell with a green nut peeking out."""
    leg = 70 * s; cb = y - leg; cy = cb - 150 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 40)
    ink(c, wellipse(x, cy, 130 * s, 160 * s, seed, 2.4), (236, 214, 170), 9 * s)
    ink(c, wellipse(x + 10 * s, cy - 20 * s, 80 * s, 110 * s, seed + 1, 2), (140, 196, 70), 7 * s)
    wline(c, quad_pts(x - 40 * s, cy - 150 * s, x - 30 * s, cy + 150 * s, 40 * s, 8), seed + 2, 6 * s, shade((236, 214, 170), 0.7))
    _arms(c, x - 120 * s, x + 120 * s, cy + 30 * s, arms, t, s, seed + 7)
    eyes(c, x + 10 * s, cy - 40 * s, s * 0.85, look, blink, 34, 24, mood, seed + 9)
    mouth(c, x + 10 * s, cy + 14 * s, s * 0.65, talk, mood, seed + 5)


def phone_video(c, x, y, s=1.0, seed=451, t=0.0, views=None, k=1.0, play=True):
    """phone showing a short video (generic: no app logos) with a heart + view counter."""
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-160, -300, 160, 300, 40, seed, 2), INK, 9); ink(c, wrrect(-140, -270, 140, 270, 22, seed + 1, 1.2), (40, 40, 52), 0)
    _choc(c, 0, 230, 0.48, t, 0, (0, 0), "happy", "down", False, False, seed + 2, crack=0.5 + 0.5 * math.sin(t * 3) if play else 1.0)
    h = skia.Path(); h.moveTo(110, -60); h.cubicTo(80, -90, 60, -50, 110, -20); h.cubicTo(160, -50, 140, -90, 110, -60); c.drawPath(h, P(RED))
    if views: f = font(BLK_F, 30); c.drawString(views, -f.measureText(views) / 2, -220, f, P(WHITE))
    c.restore()


def scooter(c, x, y, s=1.0, seed=461):
    c.save(); c.translate(x, y); c.scale(s, s)
    for wx in (-120, 120): ink(c, wellipse(wx, -40, 40, 40, seed + wx, 1.2), INK, 0)
    ink(c, wpoly([(-170, -60), (150, -60), (120, -120), (-140, -120)], seed, 2, True, 40), RED, 8)
    ink(c, wrrect(-170, -250, -30, -120, 12, seed + 1, 1.4), ORG, 8); text(c, "DELIVERY", -100, -175, 22, WHITE, BLK_F)
    wline(c, [(110, -120), (130, -220), (100, -230)], seed + 2, 9); c.restore()


def cover_title(c, kicker, title, k=1.0, y=640, col=RED, seed=501):
    """Big hook title card for frame 0 / the grid cover (owner 15 Nov: "first image need to be title so it attracts people").
    Sits inside the 3:4 profile-grid crop (y 240..1680) and below the top safe zone; centred at x=540."""
    if k <= 0: return
    lines = wrap(title, MARK_F, 108, 860)[:3]; f = font(MARK_F, 108); lh = 112
    fk = font(HAND_F, 46); kw = fk.measureText(kicker) if kicker else 0
    w = max([f.measureText(l) for l in lines] + [kw]) + 90; h = lh * len(lines) + (70 if kicker else 0) + 70
    c.save(); c.translate(540, y); c.rotate(-2); c.scale(k, k)
    c.save(); c.translate(10, 14); c.drawPath(wrrect(-w / 2, -h / 2, w / 2, h / 2, 26, seed, 2.2), P(INK, 0.18)); c.restore()
    ink(c, wrrect(-w / 2, -h / 2, w / 2, h / 2, 26, seed, 2.2), WHITE, 10)
    yy = -h / 2 + 40
    if kicker:
        c.drawString(kicker, -kw / 2, yy + 34, fk, P(INK)); yy += 70
    for i, l in enumerate(lines):
        c.drawString(l, -f.measureText(l) / 2, yy + 92 + i * lh, f, P(col if i == len(lines) - 1 else INK))
    wline(c, [(-w / 2 + 50, h / 2 - 26), (w / 2 - 50, h / 2 - 32)], seed + 3, 10, YEL, 1.2)
    c.restore()


def strip_chunk(c, words, hl=(), y0=268, size=40, t=0.0, maxw=760, seed=40):
    """Subtitle v2 (learned from the owner's 15 Nov reference reel): a SMALL torn-paper strip that types only the current 2-5 word
    chunk in uppercase typewriter letters, with the key word(s) under a yellow marker highlight. Centred at x=540."""
    if not words: return
    f = font(TYPE_F, size); sp = f.measureText(" ")
    toks = [w.upper() for w in words]; widths = [f.measureText(w) for w in toks]
    lines, cur, cw = [], [], 0
    for i, (w, ww) in enumerate(zip(toks, widths)):
        if cur and cw + sp + ww > maxw: lines.append(cur); cur, cw = [], 0
        cur.append(i); cw += (sp if cw else 0) + ww
    if cur: lines.append(cur)
    lines = lines[-2:]; lh = size * 1.35
    bw = max(sum(widths[i] for i in L) + sp * (len(L) - 1) for L in lines) + 70; bh = lh * len(lines) + 34
    x0, x1, y1 = 540 - bw / 2, 540 + bw / 2, y0 + bh
    top = [(x, y0 + (3 if (int(x) // 23) % 2 else -2)) for x in np.arange(x0, x1 + 1, 23)]
    bot = [(x, y1 + (5 if (int(x) // 19) % 2 else -4)) for x in np.arange(x1, x0 - 1, -19)]
    pth = wpoly(top + bot, seed, 0.4, True, 400)
    c.save(); c.translate(0, 6); c.drawPath(pth, P(INK, 0.14)); c.restore(); c.drawPath(pth, P((255, 254, 248))); c.drawPath(pth, S((205, 205, 200), 2))
    for li, L in enumerate(lines):
        lw = sum(widths[i] for i in L) + sp * (len(L) - 1); xx = 540 - lw / 2; yy = y0 + 17 + size * 0.98 + li * lh
        for i in L:
            if re.sub(r"[^a-z0-9$%]", "", words[i].lower()) in hl:
                c.drawRect(skia.Rect.MakeLTRB(xx - 4, yy - size * 0.62, xx + widths[i] + 4, yy + size * 0.12), P((255, 222, 40), 0.85))
            c.drawString(toks[i], xx, yy, f, P(INK)); xx += widths[i] + sp


# ------------------------------------------------------------------ razors + launch-video props (Dollar Shave Club episode, 15 Nov 2026)
def _razor(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, fancy=False, case=False, shades=False, **kw):
    """razor character: tall handle body with a wide twin-blade head on top. fancy = chrome + gold + monocle (pricey store razor);
    case = locked plastic display case around it. Generic doodle, no brand."""
    leg = 60 * s; cb = y - leg; ht = cb - 330 * s; hw = 62 * s
    body_col = (200, 206, 216) if fancy else ORG; trim = (236, 186, 40) if fancy else BLU
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 28)
    ink(c, wrrect(x - hw, ht, x + hw, cb, 40 * s, seed, 2), body_col, 9 * s)
    for j in range(4): wline(c, [(x - hw + 16 * s, cb - 60 * s - j * 30 * s), (x + hw - 16 * s, cb - 60 * s - j * 30 * s)], seed + 20 + j, 4 * s, shade(body_col, 0.75))
    wline(c, [(x, ht + 4 * s), (x, ht - 40 * s)], seed + 1, 22 * s, trim, 1)
    hx0, hx1, hy0, hy1 = x - 170 * s, x + 170 * s, ht - 120 * s, ht - 36 * s
    ink(c, wrrect(hx0, hy0, hx1, hy1, 22 * s, seed + 2, 1.6), trim, 9 * s)
    for j in range(2): wline(c, [(hx0 + 26 * s, hy0 + 26 * s + j * 28 * s), (hx1 - 26 * s, hy0 + 26 * s + j * 28 * s)], seed + 3 + j, 6 * s, (235, 240, 248), 1)
    if fancy:
        for gx in (hx0 + 30 * s, hx1 - 30 * s): c.drawCircle(gx, hy1 - 14 * s, 7 * s, P(WHITE))
    _arms(c, x - hw + 4 * s, x + hw - 4 * s, ht + 170 * s, arms, t, s, seed + 7)
    eyes(c, x, ht + 70 * s, s * 0.75, look, blink, 30, 22, mood, seed + 9)
    mouth(c, x, ht + 130 * s, s * 0.6, talk, mood, seed + 5)
    if fancy:
        ink(c, wellipse(x + 15 * s, ht + 70 * s, 30 * s, 30 * s, seed + 30, 1), None, 6 * s, (236, 186, 40))
        wline(c, [(x + 44 * s, ht + 80 * s), (x + 60 * s, ht + 200 * s)], seed + 31, 3 * s, (236, 186, 40))
    if shades:
        for sx in (-1, 1): ink(c, wrrect(x + sx * 15 * s - 26 * s, ht + 52 * s, x + sx * 15 * s + 26 * s, ht + 88 * s, 10 * s, seed + 40 + sx, 0.8), INK, 4 * s)
        wline(c, [(x - 12 * s, ht + 62 * s), (x + 12 * s, ht + 62 * s)], seed + 43, 4 * s)
    if case:
        ink(c, wrrect(x - 240 * s, hy0 - 60 * s, x + 240 * s, y + 10 * s, 20 * s, seed + 50, 1.6), None, 7 * s, (120, 170, 220))
        for j in range(3): wline(c, [(x - 200 * s + j * 40 * s, hy0 - 20 * s), (x - 230 * s + j * 40 * s, hy0 + 80 * s)], seed + 51 + j, 5 * s, WHITE, 1, 0.7)
        padlock(c, x + 190 * s, y - 200 * s, s * 0.8, 1.0, seed + 55)


def fence(c, x0, x1, y, h=420, seed=601, col=(120, 124, 134)):
    """chain-link fence on the ground line y (posts + diamond mesh)."""
    for px in np.arange(x0, x1 + 1, (x1 - x0) / 4): wline(c, [(px, y), (px, y - h)], seed + int(px), 12, col)
    wline(c, [(x0, y - h), (x1, y - h)], seed + 1, 10, col)
    for k in np.arange(x0, x1, 46):
        wline(c, [(k, y), (min(x1, k + h * 0.5), y - h)], seed + int(k), 3, col, 1, 0.8)
        wline(c, [(k + 46, y), (max(x0, k + 46 - h * 0.5), y - h)], seed + int(k) + 3, 3, col, 1, 0.8)


def label_stack(c, x, y, n=6, s=1.0, seed=611, rot=0.0):
    """bundle of white shipping labels with barcode lines."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for i in range(n):
        ink(c, wrrect(-90, -60 - i * 12, 90, 60 - i * 12, 8, seed + i, 1.2), WHITE, 5)
    for j in range(7): wline(c, [(-60 + j * 18, -40 - (n - 1) * 12), (-60 + j * 18, 20 - (n - 1) * 12)], seed + 20 + j, 4 + (j % 2) * 3, INK, 0.5)
    c.restore()


def clapper(c, x, y, s=1.0, open_=0.0, seed=621):
    """film clapperboard; open_ 0..1 lifts the striped clapstick."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-150, -20, 150, 170, 10, seed, 1.6), (40, 40, 52), 8)
    for j in range(3): wline(c, [(-120, 40 + j * 40), (120, 40 + j * 40)], seed + j, 4, WHITE)
    c.save(); c.translate(-150, -20); c.rotate(-30 * open_)
    ink(c, wrrect(0, -60, 300, 0, 6, seed + 5, 1.2), WHITE, 8)
    for j in range(5): ink(c, wpoly([(10 + j * 60, -58), (40 + j * 60, -58), (20 + j * 60, -2), (-10 + j * 60, -2)], seed + 6 + j, 0.8, True, 30), INK, 0)
    c.restore(); c.restore()


def mailbox(c, x, y, s=1.0, flag=0.0, seed=631, col=BLU):
    """curbside mailbox on a post standing on (x, y); flag 0..1 raises the red flag."""
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, [(0, 0), (0, -200)], seed, 18, BROWN)
    pth = skia.Path(); pth.moveTo(-130, -200); pth.lineTo(-130, -300); pth.cubicTo(-130, -390, 130, -390, 130, -300); pth.lineTo(130, -200); pth.close()
    ink(c, pth, col, 9)
    c.save(); c.translate(120, -300); c.rotate(-90 * flag); wline(c, [(0, 0), (0, -90)], seed + 2, 9, RED); ink(c, wrrect(0, -90, 50, -55, 4, seed + 3, 0.8), RED, 5); c.restore()
    c.restore()


def coffee(c, x, y, s=1.0, seed=641):
    """takeaway coffee cup (generic, no logo), bottom at (x, y)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-80, 0), (80, 0), (100, -260), (-100, -260)], seed, 1.6, True, 40), WHITE, 8)
    ink(c, wrrect(-96, -190, 96, -110, 6, seed + 1, 1), BROWN, 6)
    ink(c, wrrect(-116, -300, 116, -258, 14, seed + 2, 1), (60, 60, 70), 7)
    for j in range(3): wline(c, quad_pts(-40 + j * 40, -330, -30 + j * 40, -420, 20, 6), seed + 5 + j, 5, GREY, 2.5, 0.8)
    c.restore()


def crash_window(c, x, y, s=1.0, t=0.0, seed=651, k=1.0, title_="CHECKOUT"):
    """browser window (generic) with a big red X and smoke puffs = site crashed."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-260, -200, 260, 200, 20, seed, 1.6), WHITE, 9); ink(c, wrrect(-260, -200, 260, -140, 20, seed + 1, 1.2), GREY, 7)
    for j, col in enumerate((RED, YEL, GRN)): c.drawCircle(-220 + j * 36, -170, 11, P(col))
    text(c, title_, 0, -60, 34, GREY, BLK_F)
    wline(c, [(-90, -20), (90, 150)], seed + 3, 22, RED); wline(c, [(90, -20), (-90, 150)], seed + 4, 22, RED)
    for j in range(4):
        u = (t * 0.7 + j * 0.25) % 1.0
        ink(c, wellipse(-120 + j * 80 + 20 * math.sin(t * 2 + j), -230 - 160 * u, 40 + 30 * u, 34 + 26 * u, seed + 10 + j, 2), (150, 150, 160), 0, INK, 0.5 * (1 - u))
    c.restore()


def crowd(c, x, y, n=30, cols=8, k=1.0, seed=661, s=1.0):
    """grid of tiny smiling heads = members / sign-ups; k 0..1 = fraction shown."""
    m = int(n * k)
    for i in range(m):
        cx = x + (i % cols - (cols - 1) / 2) * 92 * s; cy = y - (i // cols) * 96 * s
        ink(c, wellipse(cx, cy, 36 * s, 38 * s, seed + i, 1.2), (PNK, SKY, YEL, GRN, ORG, PUR)[i % 6], 6 * s)
        c.drawCircle(cx - 12 * s, cy - 6 * s, 5 * s, P(INK)); c.drawCircle(cx + 12 * s, cy - 6 * s, 5 * s, P(INK))
        wline(c, quad_pts(cx - 14 * s, cy + 10 * s, cx + 14 * s, cy + 10 * s, 10 * s, 5), seed + i + 50, 4 * s)


def billboard(c, x, y, s=1.0, word="AD $$$", seed=671, col=RED):
    """roadside billboard on two legs standing on (x, y)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for lx in (-120, 120): wline(c, [(lx, 0), (lx, -220)], seed + lx, 14, BROWN)
    ink(c, wrrect(-230, -440, 230, -210, 12, seed, 1.6), col, 9)
    sz = 70
    while sz > 30 and font(BLK_F, sz).measureText(word) > 410: sz -= 4
    f = font(BLK_F, sz); c.drawString(word, -f.measureText(word) / 2, -300, f, P(WHITE)); c.restore()


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
    if sign:
        f = font(BLK_F, 50); tw = f.measureText(sign)
        if tw > w - 20: f = font(BLK_F, 50 * (w - 20) / tw); tw = w - 20
        c.drawString(sign, x - tw / 2, y - h - 18, f, P(WHITE))
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


# ------------------------------------------------------------------ spray bottle + cats + bed (Febreze episode, 16 Nov 2026; black + yellow theme)
def _spray(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, label="SMELL KILLER", flower=False, mist=0.0, body=WHITE, head=YEL, **kw):
    """generic trigger spray bottle character (no brand shape/colours): rounded bottle, black neck, yellow trigger head, tape label.
    flower = perfume flower on the label (after the fix); mist 0..1 = puff from the nozzle."""
    leg = 80 * s; cb = y - leg; ct = cb - 300 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 34)
    bot = wrrect(x - 112 * s, ct, x + 112 * s, cb, 44 * s, seed, 2.2); ink(c, bot, body, 9 * s)
    ink(c, wrrect(x - 44 * s, ct - 56 * s, x + 44 * s, ct + 6 * s, 10 * s, seed + 1, 1.4), INK, 7 * s)           # neck
    hd = wpoly([(x - 70 * s, ct - 56 * s), (x - 70 * s, ct - 150 * s), (x + 90 * s, ct - 150 * s), (x + 150 * s, ct - 120 * s),
                (x + 150 * s, ct - 96 * s), (x + 40 * s, ct - 96 * s), (x + 30 * s, ct - 56 * s)], seed + 2, 1.8, True, 40); ink(c, hd, head, 8 * s)
    wline(c, [(x + 10 * s, ct - 96 * s), (x + 40 * s, ct - 20 * s), (x + 64 * s, ct - 30 * s), (x + 50 * s, ct - 96 * s)], seed + 3, 8 * s)  # trigger
    if mist > 0:
        for j in range(5):
            u = (mist + j * 0.17) % 1.0; r = (14 + 40 * u) * s
            ink(c, wellipse(x + (170 + 160 * u) * s, ct - (110 + 30 * math.sin(j * 2.1)) * s, r, r * 0.8, seed + 10 + j, 1.2), WHITE, 5 * s, INK, 1 - u * 0.8)
    lab = wrrect(x - 92 * s, cb - 132 * s, x + 92 * s, cb - 54 * s, 10 * s, seed + 4, 1.2); ink(c, lab, YEL, 6 * s)
    f = font(BLK_F, 30 * s); tw = f.measureText(label)
    if tw > 170 * s: f = font(BLK_F, 30 * s * 170 * s / tw); tw = 170 * s
    c.drawString(label, x - tw / 2, cb - 82 * s, f, P(INK))
    if flower:
        fx, fy = x + 70 * s, cb - 150 * s
        for j in range(5):
            a = j * math.tau / 5; ink(c, wellipse(fx + math.cos(a) * 26 * s, fy + math.sin(a) * 26 * s, 20 * s, 20 * s, seed + 20 + j, 1), WHITE, 5 * s)
        ink(c, wellipse(fx, fy, 16 * s, 16 * s, seed + 26, 1), YEL, 5 * s)
    _arms(c, x - 108 * s, x + 108 * s, ct + 130 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 70 * s, s, look, blink, 40, 26, mood, seed + 9)
    mouth(c, x, ct + 122 * s, s * 0.8, talk, mood, seed + 5)


def _cat(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=GREY, smug=False, **kw):
    """round doodle cat (no legs needed): body blob, ears, whiskers, curling tail. smug = half-closed eyes + chin up."""
    by = y - 120 * s
    tail = [(x + 110 * s, by + 60 * s), (x + 190 * s, by + 10 * s + 14 * math.sin(t * 4 + seed) * s), (x + 170 * s, by - 80 * s), (x + 210 * s, by - 120 * s)]
    wline(c, tail, seed + 1, 30 * s, INK, 1.2); wline(c, tail, seed + 1, 18 * s, col, 1.2)
    ink(c, wellipse(x, by + 20 * s, 130 * s, 110 * s, seed, 2), col, 9 * s)
    hy = by - 90 * s
    for sx in (-1, 1): ink(c, wpoly([(x + sx * 40 * s, hy - 60 * s), (x + sx * 92 * s, hy - 120 * s), (x + sx * 100 * s, hy - 30 * s)], seed + 2 + sx, 1.4, True, 30), col, 8 * s)
    ink(c, wellipse(x, hy, 100 * s, 78 * s, seed + 5, 1.8), col, 9 * s)
    for sx in (-1, 1):
        for j in (-1, 1): wline(c, [(x + sx * 40 * s, hy + 22 * s), (x + sx * 120 * s, hy + (22 + j * 16) * s)], seed + 6 + j, 4 * s)
    if smug:
        for sx in (-1, 1): wline(c, [(x + sx * 46 * s - 18 * s, hy - 12 * s), (x + sx * 46 * s + 18 * s, hy - 12 * s)], seed + 8 + sx, 7 * s)
        wline(c, [(x - 16 * s, hy + 26 * s), (x, hy + 34 * s), (x + 16 * s, hy + 26 * s)], seed + 9, 5 * s)
    else:
        eyes(c, x, hy - 8 * s, s * 0.62, look, blink, 44, 24, mood, seed + 9); mouth(c, x, hy + 30 * s, s * 0.5, talk, mood, seed + 10)
    ink(c, wellipse(x, hy + 14 * s, 9 * s, 7 * s, seed + 11, 0.5), PNK, 4 * s)


def stink(c, x, y, k=1.0, seed=0, col=(116, 128, 52), n=3, h=160, t=0.0, w=9):
    """wavy rising smell lines; k = opacity / how strong (fade to 0 = nose stops noticing)."""
    if k <= 0: return
    for j in range(n):
        xx = x + (j - (n - 1) / 2) * 46
        pts = [(xx + 18 * math.sin(i * 1.3 + t * 5 + j), y - i * h / 6) for i in range(7)]
        wline(c, pts, seed + j, w, col, 1.2, a=min(1.0, k))


def bed(c, x, y, s=1.0, tuck=1.0, seed=0, sheet=WHITE, cover=YEL):
    """side-view doodle bed: headboard, mattress, comforter that snaps flat as tuck 0..1 (wrinkled -> neat)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-330, -330, -280, 0, 10, seed, 1.6), BROWN, 8); ink(c, wrrect(280, -170, 320, 0, 10, seed + 1, 1.6), BROWN, 8)
    ink(c, wrrect(-300, -170, 300, -100, 14, seed + 2, 1.6), sheet, 8)
    ink(c, wellipse(-210, -200, 70, 36, seed + 3, 1.4), WHITE, 7)
    wob = (1 - tuck) * 26
    cov = wpoly([(-150, -190 + wob), (-40, -200 - wob), (80, -186 + wob), (300, -196), (310, -96), (-150, -96)], seed + 4, 2 + 6 * (1 - tuck), True, 30)
    ink(c, cov, cover, 8)
    for j in range(3): wline(c, [(-120 + j * 140, -170), (-80 + j * 140, -120)], seed + 5 + j, 4, shade(cover, 0.7), a=1 - tuck)
    c.restore()


def house(c, x, y, w=520, h=440, seed=0, wall=WHITE, roof=INK, door=YEL):
    """simple house front; returns the 6 window centres (2 rows x 3) for pop-in heads."""
    ink(c, wrrect(x - w / 2, y - h, x + w / 2, y, 8, seed, 2), wall, 9)
    ink(c, wpoly([(x - w / 2 - 40, y - h + 6), (x, y - h - 200), (x + w / 2 + 40, y - h + 6)], seed + 1, 2, True, 50), roof, 9)
    ink(c, wrrect(x - 50, y - 170, x + 50, y, 8, seed + 2, 1.4), door, 8)
    wins = []
    for r in range(2):
        for q in (-1, 1):
            cx, cy = x + q * 160, y - h + 110 + r * 160; ink(c, wrrect(cx - 62, cy - 52, cx + 62, cy + 52, 6, seed + 3 + r * 2 + q, 1.4), (255, 246, 200), 7); wins.append((cx, cy))
    return wins


def nose_dial(c, x, y, s=1.0, level=1.0, seed=0):
    """big doodle nose + a volume knob beside it turned down to `level` (1 = full, 0 = off)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wpoly([(-40, -200), (10, -200), (90, 40), (60, 90), (-60, 90), (-90, 50)], seed, 2, True, 40), (255, 224, 196), 9)
    for sx in (-1, 1): ink(c, wellipse(sx * 30, 64, 16, 10, seed + sx, 0.6), INK, 0)
    kx, ky = 260, -40; ink(c, wellipse(kx, ky, 90, 90, seed + 3, 1.6), YEL, 9)
    a = math.radians(-220 + 260 * level); wline(c, [(kx, ky), (kx + 70 * math.cos(a), ky + 70 * math.sin(a))], seed + 4, 10)
    f = font(BLK_F, 34); c.drawString("SMELL", kx - f.measureText("SMELL") / 2, ky + 140, f, P(INK))
    c.restore()


def confetti(c, x, y, t, t0, n=18, seed=0, spread=320):
    if t < t0: return
    u = min(1.0, (t - t0) / 0.9)
    for i in range(n):
        a = -math.pi / 2 + (h01(i, seed) - 0.5) * 2.2; r = spread * eout(u) * (0.5 + h01(i + 5, seed) * 0.6)
        px, py = x + math.cos(a) * r, y + math.sin(a) * r + 300 * u * u
        c.save(); c.translate(px, py); c.rotate(t * 300 * (1 if i % 2 else -1)); col = (YEL, INK, RED, WHITE)[i % 4]
        c.drawRect(skia.Rect.MakeLTRB(-12, -6, 12, 6), P(col, 1 - 0.6 * u)); c.restore()


def bars(c, x, y, vals, k=1.0, seed=0, col=YEL, w=110, gap=40, hmax=360, labels=None):
    """simple bar chart on a baseline at y; vals 0..1; k grows the bars."""
    n = len(vals); x0 = x - (n * w + (n - 1) * gap) / 2
    wline(c, [(x0 - 30, y), (x0 + n * (w + gap) + 10, y)], seed, 8)
    for i, v in enumerate(vals):
        hh = max(4, hmax * v * k); bx = x0 + i * (w + gap)
        ink(c, wrrect(bx, y - hh, bx + w, y, 6, seed + i, 1.4), col, 8)
        if labels: text(c, labels[i], bx + w / 2, y + 50, 34, INK, BLK_F)


def cover_by(c, kicker, title, k=1.0, y=700, seed=501):
    """BLACK + YELLOW cover (owner 15 Nov theme): charcoal page with halftone dots, yellow title card, black type, red marker underline."""
    if k <= 0: return
    c.save(); c.drawRect(skia.Rect.MakeWH(W, H), P((30, 30, 34), 0.96 * min(1, k)))
    for yy in range(0, H, 36):
        for xx in range(0 if (yy // 36) % 2 else 18, W, 36): c.drawCircle(xx, yy, 5, P((60, 60, 66), min(1, k)))
    lines = wrap(title, MARK_F, 112, 860)[:3]; f = font(MARK_F, 112); lh = 118
    fk = font(BLK_F, 44); kw = fk.measureText(kicker) if kicker else 0
    w = max([f.measureText(l) for l in lines] + [kw]) + 90; h = lh * len(lines) + (80 if kicker else 0) + 70
    c.translate(540, y); c.rotate(-2); c.scale(k, k)
    c.save(); c.translate(12, 16); c.drawPath(wrrect(-w / 2, -h / 2, w / 2, h / 2, 26, seed, 2.2), P((0, 0, 0), 0.45)); c.restore()
    ink(c, wrrect(-w / 2, -h / 2, w / 2, h / 2, 26, seed, 2.2), (255, 214, 0), 10)
    yy = -h / 2 + 44
    if kicker: c.drawString(kicker, -kw / 2, yy + 34, fk, P(INK)); yy += 80
    for i, l in enumerate(lines): c.drawString(l, -f.measureText(l) / 2, yy + 92 + i * lh, f, P(INK))
    wline(c, [(-w / 2 + 60, h / 2 - 30), (w / 2 - 60, h / 2 - 38)], seed + 3, 12, RED, 1.2)
    c.restore()


# ---------------------------------------------------------------- 17 Nov 2026 (Liquid Death 'ad before the water'): generic tall can, fridge, festival stage,
# social post card, dotted 'render' can, investor door, store shelf, two-continent map. No brand art: the can is plain grey/white with a tape label.
def _tallcan(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, label="WATER", col=(214, 218, 226), loud=False, **kw):
    """plain tall can (tallboy) character: ribbed top, tape label; loud = angry eyebrows + zigzag 'personality' stripes (no real can art)."""
    leg = 80 * s; cb = y - leg; ct = cb - 380 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 34)
    body = wrrect(x - 100 * s, ct, x + 100 * s, cb, 30 * s, seed, 2.0); ink(c, body, col, 9 * s)
    if loud:
        c.save(); c.clipPath(body, doAntiAlias=True)
        for j in range(3):
            yy = ct + (230 + j * 34) * s
            wline(c, [(x - 110 * s + i * 40 * s, yy + (-12 if i % 2 else 12) * s) for i in range(7)], seed + 30 + j, 9 * s, (255, 214, 0) if j % 2 == 0 else RED, 0.8)
        c.restore(); ink(c, body, None, 9 * s)
    ink(c, wrrect(x - 86 * s, ct - 26 * s, x + 86 * s, ct + 8 * s, 12 * s, seed + 1, 1.2), shade(col, 0.82), 7 * s)
    wline(c, [(x - 20 * s, ct - 12 * s), (x + 24 * s, ct - 12 * s)], seed + 2, 6 * s)      # tab
    lab = wrrect(x - 80 * s, cb - 120 * s, x + 80 * s, cb - 50 * s, 8 * s, seed + 4, 1.2); ink(c, lab, WHITE, 6 * s)
    f = font(BLK_F, 34 * s); tw = f.measureText(label)
    if tw > 140 * s: f = font(BLK_F, 34 * s * 140 * s / tw); tw = 140 * s
    c.drawString(label, x - tw / 2, cb - 72 * s, f, P(INK))
    _arms(c, x - 98 * s, x + 98 * s, ct + 190 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 90 * s, s, look, blink, 40, 26, mood, seed + 9)
    if loud:
        for sx in (-1, 1): wline(c, [(x + sx * 70 * s, ct + 44 * s), (x + sx * 14 * s, ct + 64 * s)], seed + 12 + sx, 10 * s)
    mouth(c, x, ct + 150 * s, s * 0.8, talk, mood, seed + 5)


def bottle(c, x, y, s=1.0, seed=0, col=(150, 96, 60), k=1.0, a=1.0):
    """generic glass bottle (no label art)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wpoly([(-34, 0), (-34, -150), (-14, -190), (-14, -250), (14, -250), (14, -190), (34, -150), (34, 0)], seed, 1.4, True, 30), col, 7, INK, a)
    ink(c, wrrect(-26, -120, 26, -60, 6, seed + 1, 0.8), CREAM, 4, INK, a)
    c.restore()


def fridge(c, x, y, w=520, h=860, open_=1.0, seed=0, body=WHITE):
    """drinks fridge seen from the front, door swung open by open_ (0..1). Returns the 3 shelf y values."""
    x0, y0, x1, y1 = x - w / 2, y - h, x + w / 2, y
    ink(c, wrrect(x0, y0, x1, y1, 28, seed, 2), body, 9)
    ink(c, wrrect(x0 + 26, y0 + 26, x1 - 26, y1 - 26, 14, seed + 1, 1.4), (226, 240, 250), 6)
    shelves = [y0 + 300, y0 + 560, y1 - 40]
    for j, sy in enumerate(shelves): wline(c, [(x0 + 30, sy), (x1 - 30, sy)], seed + 2 + j, 7)
    if open_ < 1:   # door panel folding from the right hinge
        dw = w * (1 - ease(open_))
        ink(c, wrrect(x1 - dw, y0, x1, y1, 24, seed + 5, 1.6), body, 9)
        if dw > 40: wline(c, [(x1 - dw + 30, y0 + 360), (x1 - dw + 30, y0 + 520)], seed + 6, 12)
    return shelves


def stage(c, x, y, t, seed=0, lights=True):
    """outdoor festival stage: roof truss, two speaker stacks, coloured lights."""
    w, h = 900, 560
    ink(c, wpoly([(x - w / 2, y - 120), (x + w / 2, y - 120), (x + w / 2, y), (x - w / 2, y)], seed, 2, True, 60), (60, 60, 68), 9)
    for sx in (-1, 1): wline(c, [(x + sx * (w / 2 - 30), y - 120), (x + sx * (w / 2 - 30), y - h)], seed + sx, 12)
    ink(c, wpoly([(x - w / 2 - 20, y - h), (x + w / 2 + 20, y - h), (x + w / 2 - 20, y - h - 70), (x - w / 2 + 20, y - h - 70)], seed + 3, 1.8, True, 60), INK, 0)
    if lights:
        for j in range(6):
            lx = x - 300 + j * 120; on = (int(t * 4) + j) % 3 != 0
            ink(c, wellipse(lx, y - h + 24, 24, 24, seed + 10 + j, 1), [(255, 214, 0), RED, SKY][j % 3] if on else GREY, 5)
    for sx in (-1, 1):
        bx = x + sx * (w / 2 - 110)
        ink(c, wrrect(bx - 70, y - 300, bx + 70, y - 120, 8, seed + 20 + sx, 1.4), (40, 40, 48), 8)
        for q in range(2): ink(c, wellipse(bx, y - 255 + q * 85, 36 + 4 * math.sin(t * 20), 36 + 4 * math.sin(t * 20), seed + 24 + q + sx, 1), GREY, 6)


def drum(c, x, y, s=1.0, seed=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-90, -110, 90, 0, 14, seed, 1.4), RED, 8); ink(c, wellipse(0, -110, 90, 22, seed + 1, 1), WHITE, 7)
    c.restore()


def post_card(c, x, y, s=1.0, seed=0, views=None, k=1.0, t=0.0, img=None, likes=0.0):
    """generic social-media post card (no app logo): avatar dot, two text bars, a picture area (img(c) draws into it), heart + view counter."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-260, -330, 260, 330, 22, seed, 2), WHITE, 8)
    ink(c, wellipse(-210, -280, 26, 26, seed + 1, 0.8), (255, 214, 0), 5)
    wline(c, [(-170, -290), (40, -290)], seed + 2, 10, INK); wline(c, [(-170, -262), (-40, -262)], seed + 3, 7, GREY)
    ink(c, wrrect(-230, -230, 230, 170, 10, seed + 4, 1.2), (40, 40, 52), 6)
    if img: c.save(); c.clipRect(skia.Rect.MakeLTRB(-226, -226, 226, 166)); img(c); c.restore()
    h = skia.Path(); hx, hy = -200, 236; h.moveTo(hx, hy); h.cubicTo(hx - 34, hy - 34, hx - 60, hy + 10, hx, hy + 44); h.cubicTo(hx + 60, hy + 10, hx + 34, hy - 34, hx, hy)
    c.drawPath(h, P(RED if likes > 0 else WHITE)); c.drawPath(h, S(INK, 5))
    if views: f = font(BLK_F, 40); c.drawString(views, 230 - f.measureText(views), 262, f, P(INK))
    c.restore()


def render_can(c, x, y, s=1.0, fill=0.0, seed=0, label="WATER"):
    """a can that exists only as a picture: dashed outline + construction lines; fill 0..1 turns it into a real (solid) can."""
    c.save(); c.translate(x, y); c.scale(s, s)
    body = wrrect(-100, -400, 100, 0, 30, seed, 1.6 if fill > 0.5 else 0.6)
    if fill > 0:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-120, -400 * fill, 120, 10)); c.drawPath(body, P((214, 218, 226))); c.restore()
    pnt = S(SKY if fill < 1 else INK, 7); pnt.setPathEffect(skia.DashPathEffect.Make([20, 14], 0)) if fill < 1 else None; c.drawPath(body, pnt)
    if fill < 1:
        for yy in (-300, -200, -100): wline(c, [(-140, yy), (140, yy)], seed + yy, 3, SKY, 0.6, 0.6)
    f = font(BLK_F, 36); c.drawString(label, -f.measureText(label) / 2, -150, f, P(INK if fill >= 1 else SKY))
    c.restore()


def door(c, x, y, w=170, h=330, shut=1.0, seed=0, col=(150, 96, 60)):
    """office door; shut 0 = open (dark gap), 1 = slammed shut."""
    ink(c, wrrect(x - w / 2 - 14, y - h - 14, x + w / 2 + 14, y, 6, seed, 1.4), (60, 60, 68), 8)
    dw = w * (0.25 + 0.75 * ease(shut))
    ink(c, wrrect(x - w / 2, y - h, x - w / 2 + dw, y, 4, seed + 1, 1.2), col, 7)
    if shut > 0.6: ink(c, wellipse(x + w / 2 - 28, y - h / 2, 10, 10, seed + 2, 0.5), (255, 214, 0), 4)


def shelf(c, x, y, n_full, w=760, seed=0, rows=2, per=6, label="WATER"):
    """store shelf unit; n_full (float) cans appear left to right, row by row."""
    ink(c, wrrect(x - w / 2, y - 250 * rows - 30, x + w / 2, y, 12, seed, 1.8), (236, 236, 228), 9)
    for r in range(rows):
        sy = y - 20 - r * 250; wline(c, [(x - w / 2 + 10, sy), (x + w / 2 - 10, sy)], seed + 1 + r, 9)
        for i in range(per):
            k = min(1.0, max(0.0, n_full - (r * per + i)))
            if k <= 0: continue
            cx = x - w / 2 + 70 + i * (w - 140) / max(1, per - 1)
            c.save(); c.translate(cx, sy); c.scale(back(k) * 0.42, back(k) * 0.42)
            ink(c, wrrect(-100, -400, 100, 0, 30, seed + 9 + i, 1.4), (214, 218, 226), 12)
            ink(c, wrrect(-80, -130, 80, -60, 8, seed + 20 + i, 1), WHITE, 8); c.restore()


def two_lands(c, t, seed=0, k=1.0):
    """simple two-continent map: a left blob tagged later as AMERICA, a right blob (BRITAIN + EUROPE), wavy ocean between."""
    c.drawRect(skia.Rect.MakeLTRB(60, 700, 1020, 1380), P((150, 205, 245), 0.55 * k))
    for j in range(5): wline(c, [(420 + i * 30, 820 + j * 110 + 10 * math.sin(i + t * 2)) for i in range(8)], seed + j, 4, (70, 140, 210), 1, 0.7 * k)
    am = wpoly([(90, 760), (330, 730), (400, 880), (360, 1060), (300, 1200), (220, 1330), (150, 1180), (100, 980)], seed + 10, 3, True, 50)
    eu = wpoly([(760, 760), (840, 740), (860, 820), (990, 830), (1000, 1000), (930, 1120), (800, 1080), (760, 960)], seed + 11, 3, True, 50)
    uk = wpoly([(680, 800), (720, 780), (730, 880), (690, 930), (660, 870)], seed + 12, 2, True, 30)
    for pth in (am, eu, uk): ink(c, pth, (120, 196, 110), 8, INK, k)


# ---------------------------------------------------------------- 18 Nov 2026 (Hoka 'clown shoes'): generic chunky running shoe character, thin barefoot-style
# shoe, mountain with a downhill trail, clown nose, start line + cones, plain stick runner, permit park sign, tower with a plain boot icon.
# No brand marks: no logos, stripes or real colourways — the shoe is a plain sneaker with a puffy white sole and a tape label.
def _chunkyshoe(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, label="SHOE", upper=(120, 200, 255), sole=WHITE, nose=0.0, **kw):
    """chunky running shoe character: oversized puffy sole (two wobbly layers), low upper with laces, eyes on the toe box, stick arms.
    nose 0..1 = a red clown nose pops onto the toe."""
    sy = y - 20 * s
    sl = wpoly([(x - 250 * s, sy - 30 * s), (x - 240 * s, sy - 150 * s), (x + 210 * s, sy - 150 * s), (x + 290 * s, sy - 110 * s), (x + 300 * s, sy - 40 * s), (x + 250 * s, sy)], seed, 2.2, True, 50)
    ink(c, sl, sole, 9 * s)
    wline(c, [(x - 236 * s, sy - 80 * s), (x + 286 * s, sy - 76 * s)], seed + 1, 6 * s, shade(sole, 0.7))
    up = wpoly([(x - 240 * s, sy - 150 * s), (x - 250 * s, sy - 330 * s), (x - 150 * s, sy - 370 * s), (x - 40 * s, sy - 330 * s), (x + 120 * s, sy - 260 * s),
                (x + 250 * s, sy - 200 * s), (x + 270 * s, sy - 150 * s)], seed + 2, 2.2, True, 50)
    ink(c, up, upper, 9 * s)
    for j in range(4):   # laces
        lx = x - 120 * s + j * 50 * s; wline(c, [(lx - 26 * s, sy - 300 * s + j * 22 * s), (lx + 26 * s, sy - 270 * s + j * 22 * s)], seed + 3 + j, 6 * s, WHITE)
    ink(c, wpoly([(x - 250 * s, sy - 330 * s), (x - 262 * s, sy - 380 * s), (x - 200 * s, sy - 392 * s), (x - 150 * s, sy - 370 * s)], seed + 8, 1.4, True, 30), shade(upper, 0.8), 7 * s)
    lab = wrrect(x - 210 * s, sy - 220 * s, x - 60 * s, sy - 170 * s, 8 * s, seed + 9, 1.0); ink(c, lab, ORG, 5 * s)
    f = font(BLK_F, 30 * s); tw = f.measureText(label)
    if tw > 130 * s: f = font(BLK_F, 30 * s * 130 * s / tw); tw = 130 * s
    c.drawString(label, x - 135 * s - tw / 2, sy - 184 * s, f, P(INK))
    eyes(c, x + 110 * s, sy - 236 * s, s * 0.8, look, blink, 40, 26, mood, seed + 11)
    mouth(c, x + 190 * s, sy - 176 * s, s * 0.6, talk, mood, seed + 12)
    if nose > 0: ink(c, wellipse(x + 262 * s, sy - 190 * s, 40 * s * nose, 38 * s * nose, seed + 13, 1.2), RED, 6 * s)
    _arms(c, x - 200 * s, x + 40 * s, sy - 250 * s, arms, t, s * 0.9, seed + 14)
    if walk or kw.get("legs", True): _legs(c, x, sy - 2, y + 6 * s, s * 0.7, t, walk, seed + 16, 120)


def thin_shoe(c, x, y, s=1.0, seed=0, col=(196, 196, 204), rot=0.0, k=1.0):
    """flat barefoot-style shoe (toe-slipper) standing on (x, y)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    ink(c, wpoly([(-170, 0), (-176, -16), (180, -16), (196, -4), (180, 0)], seed, 1.2, True, 40), INK, 0)
    ink(c, wpoly([(-170, -14), (-176, -86), (-110, -100), (-20, -70), (110, -60), (186, -40), (190, -14)], seed + 1, 1.8, True, 40), col, 7)
    for j in range(5): ink(c, wellipse(130 + j * 14 - 30, -44 - (j % 2) * 4, 12, 16, seed + 2 + j, 0.6), shade(col, 0.85), 4)
    c.restore()


def mountain(c, x, y, w=900, h=640, seed=0, snow=True, trail=1.0):
    """big doodle mountain on (x, y) with a dashed downhill trail drawn on (trail 0..1)."""
    ink(c, wpoly([(x - w / 2, y), (x - 60, y - h), (x + 30, y - h + 60), (x + 110, y - h + 10), (x + w / 2, y)], seed, 3, True, 60), (150, 200, 150), 9)
    if snow: ink(c, wpoly([(x - 160, y - h + 220), (x - 60, y - h), (x + 30, y - h + 60), (x + 110, y - h + 10), (x + 200, y - h + 200), (x + 120, y - h + 170), (x + 40, y - h + 230), (x - 50, y - h + 180)], seed + 1, 2, True, 50), WHITE, 7)
    pts = quad_pts(x - 40, y - h + 60, x + w / 2 - 80, y - 20, 160, 22)
    m = int(len(pts) * trail)
    for i in range(0, max(0, m - 1), 2): wline(c, [pts[i], pts[i + 1]], seed + 10 + i, 8, BROWN)


def cone(c, x, y, s=1.0, seed=0, num=None, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-70, -16, 70, 6, 6, seed, 1), ORG, 6)
    ink(c, wpoly([(-50, -14), (-12, -150), (12, -150), (50, -14)], seed + 1, 1.4, True, 40), ORG, 7)
    wline(c, [(-34, -70), (34, -70)], seed + 2, 12, WHITE)
    if num: text(c, num, 0, -170, 54, INK, MARK_F)
    c.restore()


def start_line(c, y=1300, seed=0):
    """chequered start line across the ground."""
    for i in range(27):
        for r in range(2):
            if (i + r) % 2 == 0: c.drawRect(skia.Rect.MakeXYWH(i * 40, y + r * 26, 40, 26), P(INK, 0.85))
    wline(c, [(-10, y), (W + 10, y)], seed, 6); wline(c, [(-10, y + 52), (W + 10, y + 52)], seed + 1, 6)


def runner(c, x, y, t, s=1.0, seed=0, col=BLU, name=None, chunky=True, k=1.0, speed=1.0, mood="happy", bounce=0.0):
    """plain stick runner mid-stride (no likeness); chunky = puffy white soles; bounce = cloud bounce height."""
    if k <= 0: return
    ph = t * 11 * speed + seed
    yy = y - abs(math.sin(ph)) * (14 + bounce) * s
    c.save(); c.translate(x, yy); c.scale(s * k, s * k)
    for j in (0, 1):
        a = math.sin(ph + j * math.pi)
        fx, fy = a * 70, -10 - max(0, -a) * 40
        wline(c, [(0, -150), (a * 30, -80), (fx, fy)], seed + j, 9)
        if chunky: ink(c, wrrect(fx - 34, fy - 6, fx + 44, fy + 22, 10, seed + 3 + j, 1), WHITE, 6)
        else: ink(c, wellipse(fx + 8, fy + 4, 26, 9, seed + 3 + j, 1), INK, 0)
        b = math.sin(ph + j * math.pi + math.pi)
        wline(c, [(0, -270), (b * 50, -220), (b * 70 + 20, -250)], seed + 5 + j, 8)
    ink(c, wpoly([(-30, -300), (30, -300), (26, -150), (-26, -150)], seed + 7, 1.4, True, 30), col, 7)
    ink(c, wellipse(0, -350, 44, 46, seed + 8, 1.2), (255, 224, 196), 7)
    c.drawCircle(10, -358, 6, P(INK)); c.drawCircle(30, -358, 6, P(INK))
    wline(c, quad_pts(4, -332, 32, -332, 8 if mood == "happy" else -6, 5), seed + 9, 4)
    c.restore()
    if name: tape(c, name, x, y + 46, 30, -3, k, seed=seed)


def park_sign(c, x, y, s=1.0, seed=0, word="CITY PARK", k=1.0):
    """generic wooden park sign on two posts standing on (x, y)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    for lx in (-110, 110): ink(c, wrrect(lx - 14, -260, lx + 14, 0, 4, seed + lx, 1), BROWN, 6)
    ink(c, wrrect(-200, -400, 200, -230, 16, seed, 1.6), (90, 160, 90), 9)
    ink(c, wrrect(-180, -382, 180, -248, 10, seed + 1, 1), None, 4, WHITE)
    sz = 62
    while sz > 28 and font(BLK_F, sz).measureText(word) > 330: sz -= 4
    f = font(BLK_F, sz); c.drawString(word, -f.measureText(word) / 2, -295, f, P(WHITE))
    c.restore()


def clipboard(c, x, y, s=1.0, seed=0, head="PERMIT", k=1.0, ticks=0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-150, -200, 150, 200, 14, seed, 1.6), BROWN, 8)
    ink(c, wrrect(-124, -170, 124, 180, 6, seed + 1, 1.2), WHITE, 6)
    ink(c, wrrect(-60, -222, 60, -176, 10, seed + 2, 1), GREY, 6)
    f = font(BLK_F, 44); c.drawString(head, -f.measureText(head) / 2, -110, f, P(INK))
    for j in range(4):
        yy = -50 + j * 56; wline(c, [(-70, yy), (100, yy)], seed + 3 + j, 4, GREY)
        ink(c, wrrect(-110, yy - 18, -84, yy + 8, 4, seed + 9 + j, 0.6), WHITE, 4)
        if j < ticks: wline(c, [(-112, yy - 6), (-100, yy + 8), (-78, yy - 26)], seed + 20 + j, 6, GRN)
    c.restore()


def boot_tower(c, x, y, w=320, h=600, seed=0, label="DECKERS"):
    """office tower with a plain boot outline on its sign (generic, no brand marks)."""
    building(c, x, y, w, h, (210, 214, 224), seed, None, True)
    ink(c, wrrect(x - 130, y - h - 150, x + 130, y - h - 20, 12, seed + 3, 1.4), WHITE, 8)
    ink(c, wpoly([(x - 70, y - h - 50), (x - 66, y - h - 130), (x - 20, y - h - 130), (x - 16, y - h - 80), (x + 60, y - h - 70), (x + 70, y - h - 50)], seed + 4, 1.2, True, 30), TAN, 6)
    tape(c, label, x, y - h - 190, 40, -3, 1.0, seed=seed + 5)


def money_stack(c, x, y, n, s=1.0, seed=0):
    """pile of green bill bricks standing on (x, y); n = number of bricks."""
    for i in range(int(n)):
        yy = y - 30 * s - i * 34 * s; xx = x + (h01(i, seed) - 0.5) * 16 * s
        ink(c, wrrect(xx - 90 * s, yy - 16 * s, xx + 90 * s, yy + 16 * s, 5 * s, seed + i, 1), (140, 214, 140), 5 * s)
        c.drawCircle(xx, yy, 9 * s, P(DGRN))


def speed_lines(c, x, y, n=4, length=160, seed=0, col=RED, k=1.0):
    for i in range(n):
        yy = y + (i - n / 2) * 34; l = length * (0.6 + 0.4 * h01(i, seed)) * k
        wline(c, [(x - l, yy), (x, yy)], seed + i, 7, col)


# ---------------------------------------------------------------- 19 Nov 2026: hot-sauce episode props (generic objects only — no rooster, no green cap, no label art)
def _sauce(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, label="HOT SAUCE", col=(226, 46, 38), cap=WHITE, **kw):
    """generic squeeze-bottle hot sauce character: tapered red body, white flip cap + nozzle, tape label, stick arms + legs."""
    leg = 80 * s; cb = y - leg; ct = cb - 420 * s
    _legs(c, x, cb - 6 * s, y, s, t, walk, seed, 34)
    body = wpoly([(x - 110 * s, cb), (x - 118 * s, cb - 250 * s), (x - 70 * s, ct + 40 * s), (x + 70 * s, ct + 40 * s), (x + 118 * s, cb - 250 * s), (x + 110 * s, cb)], seed, 2.0, True, 40)
    ink(c, body, col, 9 * s)
    wline(c, [(x - 70 * s, cb - 330 * s), (x - 84 * s, cb - 210 * s)], seed + 1, 7 * s, WHITE, a=0.7)   # shine
    ink(c, wrrect(x - 70 * s, ct - 10 * s, x + 70 * s, ct + 46 * s, 12 * s, seed + 2, 1.2), cap, 8 * s)
    ink(c, wpoly([(x - 22 * s, ct - 8 * s), (x - 10 * s, ct - 80 * s), (x + 10 * s, ct - 80 * s), (x + 22 * s, ct - 8 * s)], seed + 3, 1.0, True, 20), cap, 7 * s)
    lab = wrrect(x - 92 * s, cb - 140 * s, x + 92 * s, cb - 62 * s, 8 * s, seed + 4, 1.2); ink(c, lab, WHITE, 6 * s)
    f = font(BLK_F, 32 * s); tw = f.measureText(label)
    if tw > 160 * s: f = font(BLK_F, 32 * s * 160 * s / tw); tw = 160 * s
    c.drawString(label, x - tw / 2, cb - 88 * s, f, P(INK))
    _arms(c, x - 112 * s, x + 112 * s, cb - 230 * s, arms, t, s, seed + 7)
    eyes(c, x, ct + 120 * s, s * 0.9, look, blink, 38, 24, mood, seed + 9)
    mouth(c, x, ct + 186 * s, s * 0.75, talk, mood, seed + 5)


def chili(c, x, y, s=1.0, rot=0.0, seed=0, col=(226, 46, 38), k=1.0):
    """curved chili pepper with a green stem."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    ink(c, wpoly([(-20, -70), (24, -66), (36, -10), (24, 60), (-6, 120), (-30, 150), (-24, 100), (-24, 20)], seed, 1.6, True, 30), col, 7)
    ink(c, wpoly([(-22, -70), (-10, -96), (8, -100), (24, -66)], seed + 1, 1.0, True, 20), DGRN, 6)
    wline(c, [(0, -96), (6, -130), (20, -140)], seed + 2, 7, DGRN)
    c.restore()


def freighter(c, x, y, s=1.0, t=0.0, seed=0, name="HUY FONG", k=1.0):
    """cargo freighter on waves (bobbing), name painted on the hull as plain text."""
    if k <= 0: return
    bob = math.sin(t * 2.2 + seed) * 8
    c.save(); c.translate(x, y + bob); c.rotate(math.sin(t * 1.7) * 1.5); c.scale(s * k, s * k)
    ink(c, wpoly([(-400, -140), (400, -140), (330, 0), (-350, 0)], seed, 2.4, True, 60), (60, 70, 92), 9)
    wline(c, [(-390, -110), (392, -110)], seed + 1, 8, RED)
    for j in range(4): ink(c, wrrect(-300 + j * 120, -230, -200 + j * 120, -140, 6, seed + 2 + j, 1.2), (ORG, BLU, YEL, GRN)[j], 6)
    ink(c, wrrect(190, -330, 330, -140, 10, seed + 7, 1.6), WHITE, 8)
    for j in range(3): ink(c, wrrect(206 + j * 42, -300, 236 + j * 42, -270, 4, seed + 8 + j, 0.8), SKY, 4)
    ink(c, wrrect(270, -400, 310, -330, 6, seed + 12, 1.0), RED, 6)
    text(c, name, -20, -40, 54, WHITE, BLK_F)
    c.restore()
    for j in range(5):   # waves
        wx = x - 520 * s + j * 260 * s + 30 * math.sin(t * 2 + j)
        wline(c, [(wx, y + 30), (wx + 60 * s, y + 6), (wx + 120 * s, y + 30), (wx + 180 * s, y + 6)], seed + 20 + j, 8, BLU)


def van(c, x, y, s=1.0, t=0.0, seed=0, col=BLU, k=1.0, drive=0.0, load=True):
    """boxy delivery van seen from the side, standing on (x, y); drive>0 = bounce + speed lines."""
    if k <= 0: return
    bounce = abs(math.sin(t * 14)) * 6 * drive
    c.save(); c.translate(x, y - bounce); c.scale(s * k, s * k)
    ink(c, wpoly([(-280, -60), (-280, -300), (120, -300), (200, -200), (280, -170), (280, -60)], seed, 2.2, True, 50), col, 9)
    ink(c, wpoly([(130, -280), (190, -205), (130, -205)], seed + 1, 1.0, True, 20), SKY, 6)
    wline(c, [(-30, -290), (-30, -70)], seed + 2, 6)
    if load: text(c, "CHILI SAUCE", -150, -170, 40, WHITE, BLK_F)
    for wx in (-170, 170):
        ink(c, wellipse(wx, -50, 56, 56, seed + 3 + wx, 1.4), INK, 0)
        ink(c, wellipse(wx, -50, 24, 24, seed + 5 + wx, 0.8), GREY, 5)
    c.restore()
    if drive > 0: speed_lines(c, x - 330 * s, y - 220 * s, 4, 150, seed + 9, INK, drive)


def listing(c, x, y, s=1.0, seed=0, price="$70", k=1.0, sold=0.0):
    """generic online-auction listing card (no site branding): photo of a red sauce bottle, '28 OZ', big price, BUY NOW button."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-260, -330, 260, 330, 22, seed, 2), WHITE, 9)
    ink(c, wrrect(-220, -290, 220, 20, 12, seed + 1, 1.4), (236, 240, 246), 6)
    ink(c, wpoly([(-56, 0), (-60, -130), (-36, -200), (36, -200), (60, -130), (56, 0)], seed + 2, 1.4, True, 30), (226, 46, 38), 7)
    ink(c, wrrect(-36, -230, 36, -196, 6, seed + 3, 0.8), WHITE, 5)
    text(c, "HOT SAUCE, 28 OZ", 0, 76, 34, INK, BLK_F)
    text(c, price, -60, 176, 92, RED, ANTON_F)
    ink(c, wrrect(70, 130, 230, 200, 30, seed + 4, 1.2), BLU, 6); text(c, "BUY NOW", 150, 178, 30, WHITE, BLK_F)
    text(c, "ONLINE LISTING, 2023", 0, 282, 28, (120, 120, 128), BLK_F)
    c.restore()


def menu(c, x, y, s=1.0, seed=0, k=1.0, n_hot=0):
    """restaurant menu card: dish lines, the first n_hot get a red chili icon."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-230, -340, 230, 340, 18, seed, 2), CREAM, 9)
    text(c, "MENU", 0, -260, 64, INK, MARK_F)
    for j in range(7):
        yy = -170 + j * 72
        wline(c, [(-170, yy), (90 + (j % 3) * 20, yy)], seed + 1 + j, 9, (120, 110, 100))
        if j < n_hot: chili(c, 160, yy - 6, 0.32, 40, seed + 10 + j)
    c.restore()


def farm(c, x, y, w=700, seed=0, label="PEPPER FARM", k=1.0, rows=4, crop=True, gone=0.0):
    """pepper field: barn on the left, rows of chili plants; gone 0..1 greys the plants out (bad harvest)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    ink(c, wpoly([(-w / 2, -40), (-w / 2, -260), (-w / 2 + 110, -340), (-w / 2 + 220, -260), (-w / 2 + 220, -40)], seed, 2, True, 40), RED, 9)
    ink(c, wrrect(-w / 2 + 70, -150, -w / 2 + 150, -40, 6, seed + 1, 1), WHITE, 6)
    for r in range(rows):
        yy = -40 - r * 50
        wline(c, [(-w / 2 + 250, yy), (w / 2, yy)], seed + 2 + r, 7, BROWN)
        if crop:
            for j in range(6):
                px = -w / 2 + 280 + j * 75 + (r % 2) * 30
                ink(c, wellipse(px, yy - 22, 24, 20, seed + 10 + r * 9 + j, 1), shade(DGRN, 1 - 0.3 * gone) if gone < 0.5 else (170, 160, 120), 5)
                if gone < 0.5: ink(c, wellipse(px + 10, yy - 8, 8, 14, seed + 50 + r * 9 + j, 0.6), (226, 46, 38), 3)
    if label: tape(c, label, 0, 30, 34, 2, 1.0, WHITE, INK, seed + 99)
    c.restore()


def gavel(c, x, y, s=1.0, seed=0, hit=0.0, k=1.0):
    """judge's gavel over a sound block; hit 0..1 swings it down."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-120, -30, 120, 10, 10, seed, 1.4), BROWN, 7)
    c.save(); c.translate(80, -60); c.rotate(-35 * (1 - ease(hit)))
    wline(c, [(0, 0), (-200, -150)], seed + 1, 18, BROWN)
    ink(c, wrrect(-260, -230, -150, -100, 14, seed + 2, 1.2), shade(BROWN, 0.8), 8)
    c.restore()
    if hit > 0.9:
        for a_ in (-50, 0, 50): wline(c, [(math.sin(math.radians(a_)) * 140, -40 - math.cos(math.radians(a_)) * 60), (math.sin(math.radians(a_)) * 200, -60 - math.cos(math.radians(a_)) * 100)], seed + 5 + a_, 7, RED)
    c.restore()


def jury_box(c, x, y, s=1.0, seed=0, t=0.0, k=1.0):
    """jury box: wooden rail with a row of plain doodle heads."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    for j in range(6):
        hx = -250 + j * 100; hy = -230 + (j % 2) * 16
        ink(c, wellipse(hx, hy, 40, 44, seed + j, 1.2), (255, 224, 196), 7)
        eyes(c, hx, hy - 4, 0.36, (0.3, 0), (int(t * 12 + j * 5) % 41) in (0, 1), 40, 22, "neutral", seed + 20 + j)
    ink(c, wrrect(-320, -170, 320, 0, 10, seed + 9, 2), BROWN, 9)
    for j in range(5): wline(c, [(-260 + j * 130, -160), (-260 + j * 130, -10)], seed + 30 + j, 6, shade(BROWN, 0.7))
    text(c, "JURY", 0, -64, 50, WHITE, BLK_F)
    c.restore()


def raincloud(c, x, y, s=1.0, t=0.0, seed=0, k=1.0, storm=True):
    """grey storm cloud with falling rain dashes and a zigzag bolt."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    for j in range(14):
        rx = -150 + (j * 53) % 300; ry = ((t * 600 + j * 97) % 260)
        wline(c, [(rx, 40 + ry), (rx - 12, 80 + ry)], seed + j, 6, BLU)
    for (cx, cy, r) in ((-90, 0, 80), (0, -40, 100), (100, 0, 80), (0, 30, 90)):
        ink(c, wellipse(cx, cy, r * 1.1, r, seed + 40 + cx, 1.6), (150, 156, 170), 9)
    ink(c, wellipse(0, 10, 180, 60, seed + 50, 1.0), (150, 156, 170), 0)
    if storm and int(t * 3) % 3 == 0:
        ink(c, wpoly([(20, 60), (-20, 150), (16, 150), (-26, 250), (60, 130), (20, 130), (50, 60)], seed + 60, 1, True, 20), YEL, 6)
    c.restore()


def stove(c, x, y, s=1.0, seed=0, k=1.0, banned=0.0):
    """home kitchen stove with a pot; banned 0..1 draws a red no-circle over it."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-200, -300, 200, 0, 16, seed, 2), WHITE, 9)
    for j in range(3): ink(c, wellipse(-110 + j * 110, -60, 26, 26, seed + 1 + j, 1), GREY, 6)
    ink(c, wrrect(-130, -300, 130, -290, 4, seed + 5, 1), INK, 0)
    ink(c, wpoly([(-120, -300), (-110, -440), (110, -440), (120, -300)], seed + 6, 1.6, True, 30), (90, 96, 110), 8)
    ink(c, wrrect(-130, -460, 130, -430, 8, seed + 7, 1), (70, 76, 90), 7)
    for j in range(3): wline(c, [(-50 + j * 50, -480), (-40 + j * 50, -530), (-50 + j * 50, -580)], seed + 8 + j, 6, GREY)
    tape(c, "HOME KITCHEN", 0, -170, 34, -2, 1.0, CREAM, INK, seed + 20)
    if banned > 0:
        ink(c, wellipse(0, -270, 300 * ease(banned), 300 * ease(banned), seed + 30, 2.2), None, 22, RED)
        wline(c, [(-210 * ease(banned), -480 * ease(banned) + (-270) * (1 - ease(banned)) + 0), (210 * ease(banned), -60)], seed + 31, 22, RED)
    c.restore()


# ---------------------------------------------------------------- 20 Nov 2026: secondhand-closet episode props (generic objects only — no app logo, no brand colour, no app UI)
def tee(c, x, y, s=1.0, col=BLU, rot=0.0, seed=0, k=1.0, kind="tee"):
    """flat doodle garment centred on (x, y): kind tee | dress | sock | jacket | jeans."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    if kind == "tee":
        ink(c, wpoly([(-60, -80), (-110, -50), (-90, -10), (-62, -24), (-62, 80), (62, 80), (62, -24), (90, -10), (110, -50), (60, -80), (24, -66), (-24, -66)], seed, 1.6, True, 30), col, 7)
    elif kind == "dress":
        ink(c, wpoly([(-36, -90), (36, -90), (44, -30), (100, 90), (-100, 90), (-44, -30)], seed, 1.6, True, 30), col, 7)
        wline(c, [(-44, -30), (44, -30)], seed + 1, 5)
    elif kind == "sock":
        ink(c, wpoly([(-30, -90), (30, -90), (30, 30), (80, 50), (80, 90), (-30, 90)], seed, 1.4, True, 30), col, 7)
        wline(c, [(-30, -60), (30, -60)], seed + 1, 5, WHITE)
    elif kind == "jeans":
        ink(c, wpoly([(-60, -90), (60, -90), (70, 90), (14, 90), (0, -10), (-14, 90), (-70, 90)], seed, 1.6, True, 30), col, 7)
    else:   # jacket: tee shape, longer, zip line
        ink(c, wpoly([(-62, -90), (-116, -54), (-110, 60), (-80, 60), (-66, -20), (-66, 96), (66, 96), (66, -20), (80, 60), (110, 60), (116, -54), (62, -90), (20, -70), (-20, -70)], seed, 1.6, True, 30), col, 7)
        wline(c, [(0, -70), (0, 96)], seed + 1, 5)
    c.restore()


def hanger(c, x, y, s=1.0, seed=0):
    """wire hanger: hook at (x, y), shoulders below."""
    c.save(); c.translate(x, y); c.scale(s, s)
    wline(c, [(0, 0), (10, -18), (0, -34), (-12, -22)], seed, 6, (90, 90, 100))
    wline(c, [(0, 0), (-90, 50), (90, 50), (0, 0)], seed + 1, 6, (90, 90, 100))
    c.restore()


_CLOTH_COLS = [BLU, RED, YEL, GRN, PNK, PUR, ORG, TEAL, (120, 120, 132)]


def closet(c, x, y, w=460, h=760, seed=0, bulge=0.0, open_=0.0, t=0.0, spill=0.0, tags=0.0):
    """wardrobe standing on (x, y). bulge 0..1 = doors strain (wobble + gap), open_ 0..1 = doors swing open showing a jammed rail;
    spill 0..1 = a pile of clothes slides out to the floor; tags 0..1 = little price tags appear on the hanging clothes."""
    x0, x1, y0 = x - w / 2, x + w / 2, y - h
    ink(c, wrrect(x0 - 16, y0 - 30, x1 + 16, y0 + 10, 8, seed, 1.4), shade(BROWN, 0.8), 8)          # crown
    ink(c, wrrect(x0, y0, x1, y, 10, seed + 1, 2.0), shade(BROWN, 1.25), 9)                           # carcass
    ink(c, wrrect(x0 + 18, y0 + 18, x1 - 18, y - 18, 6, seed + 2, 1.2), (60, 46, 40), 6)              # dark inside
    wline(c, [(x0 + 30, y0 + 70), (x1 - 30, y0 + 70)], seed + 3, 8, GREY)                             # rail
    if open_ > 0.05 or spill > 0:
        n = 9
        for i in range(n):
            gx = x0 + 60 + i * (w - 120) / (n - 1) + math.sin(t * 3 + i) * 3
            hanger(c, gx, y0 + 70, 0.5, seed + 10 + i)
            kind = ("tee", "dress", "jacket", "tee", "jeans", "dress", "tee", "jacket", "tee")[i]
            tee(c, gx, y0 + 180, 0.62, _CLOTH_COLS[i % len(_CLOTH_COLS)], (h01(i, seed) - 0.5) * 10, seed + 30 + i, 1.0, kind)
            if tags > 0 and i % 2 == 0:
                kk = min(1.0, max(0.0, tags * 3 - i / 4))
                if kk > 0:
                    c.save(); c.translate(gx + 20, y0 + 250); c.scale(back(kk), back(kk))
                    ink(c, wpoly([(-24, -18), (24, -18), (34, 0), (24, 18), (-24, 18)], seed + 50 + i, 0.8, True, 20), YEL, 5)
                    f = font(BLK_F, 20); c.drawString("$", -6, 7, f, P(INK)); c.restore()
        for j in range(5):   # jammed lower pile
            tee(c, x0 + 80 + j * (w - 160) / 4, y - 120 - (j % 2) * 40, 0.7, _CLOTH_COLS[(j + 3) % len(_CLOTH_COLS)], (j - 2) * 14, seed + 60 + j, 1.0, ("jeans", "tee", "sock", "tee", "jacket")[j])
    # doors
    wob = bulge * math.sin(t * 22) * 6
    for side in (-1, 1):
        hinge = x0 if side < 0 else x1
        dw = (w / 2) * (1 - 0.82 * ease(open_))
        gap = bulge * 14
        if side < 0: dx0, dx1 = hinge - (w / 2 - dw) * 0.6 * ease(open_), hinge + dw - gap
        else: dx0, dx1 = hinge - dw + gap, hinge + (w / 2 - dw) * 0.6 * ease(open_)
        dx0 += side * -wob if side < 0 else wob; dx1 += wob * side
        ink(c, wrrect(min(dx0, dx1), y0 + 4 - bulge * 6, max(dx0, dx1), y - 4 + bulge * 6, 8, seed + 70 + side, 1.6 + bulge), shade(BROWN, 1.45), 9)
        if open_ < 0.4: c.drawCircle((dx1 - 26) if side < 0 else (dx0 + 26), y0 + h / 2, 11, P(YEL))
    if bulge > 0.2 and open_ < 0.3:   # a sleeve + sock poke out of the gap
        tee(c, x + 6, y0 + h * 0.42, 0.5, RED, 80 + wob * 3, seed + 80, 1.0, "sock")
        tee(c, x - 4, y0 + h * 0.7, 0.46, BLU, -70, seed + 81, 1.0, "tee")
    if spill > 0:
        for j in range(8):
            u = min(1.0, max(0.0, spill * 1.6 - j * 0.08))
            if u <= 0: continue
            px = x + (j - 3.5) * 70 + (h01(j, seed + 5) - 0.5) * 40
            py = y0 + h * 0.5 + (y - 30 - (j % 3) * 36 - (y0 + h * 0.5)) * eout(u)
            tee(c, px, py, 0.7, _CLOTH_COLS[(j + 1) % len(_CLOTH_COLS)], (h01(j, seed) - 0.5) * 120 * u, seed + 90 + j, 1.0, ("tee", "sock", "dress", "jeans", "tee", "jacket", "sock", "tee")[j])


def moving_box(c, x, y, s=1.0, seed=0, label="MOVING", stuffed=0.0, k=1.0):
    """cardboard box standing on (x, y); stuffed 0..1 = flaps pushed open by clothes poking out."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-150, -220, 150, 0, 6, seed, 1.6), TAN, 9)
    a = 18 + 40 * stuffed
    for sd in (-1, 1):
        c.save(); c.translate(sd * 150, -220); c.rotate(-sd * a)
        ink(c, wpoly([(0, 0), (-sd * 150, 0), (-sd * 150, -50), (0, -50)], seed + sd + 3, 1.2, True, 30), shade(TAN, 0.92), 8); c.restore()
    if stuffed > 0:
        for j in range(3): tee(c, -70 + j * 70, -240 - 20 * stuffed, 0.55, _CLOTH_COLS[j + 1], (j - 1) * 25, seed + 10 + j, 1.0, ("tee", "sock", "dress")[j])
    ink(c, wrrect(-100, -130, 100, -80, 4, seed + 7, 0.8), (230, 214, 170), 0)
    f = font(MARK_F, 40); c.drawString(label, -f.measureText(label) / 2, -90, f, P(INK))
    c.restore()


def browser(c, x, y, w=620, h=480, seed=0, k=1.0, n_thumbs=0, title_=None, fly=0.0):
    """plain 2008-style web page frame (grey bar, three dots) with clothing thumbnails popping in; fly 0..1 = thumbnails lift off."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    ink(c, wrrect(-w / 2, -h / 2, w / 2, h / 2, 14, seed, 1.6), WHITE, 9)
    ink(c, wrrect(-w / 2, -h / 2, w / 2, -h / 2 + 60, 10, seed + 1, 1.0), (214, 214, 220), 7)
    for j in range(3): c.drawCircle(-w / 2 + 34 + j * 30, -h / 2 + 30, 9, P((RED, YEL, GRN)[j]))
    ink(c, wrrect(-w / 2 + 130, -h / 2 + 16, w / 2 - 30, -h / 2 + 46, 8, seed + 2, 0.8), WHITE, 4)
    if title_:
        f = font(MARK_F, 54); c.drawString(title_, -f.measureText(title_) / 2, -h / 2 + 130, f, P(INK))
    kinds = ("tee", "dress", "jacket", "jeans", "sock", "tee")
    for i in range(min(6, int(n_thumbs + 0.999))):
        kk = min(1.0, n_thumbs - i)
        r_, q = divmod(i, 3); tx = -w / 2 + 110 + q * (w - 220) / 2; ty = -h / 2 + 210 + r_ * 150
        if fly > 0: tx += fly * (q - 1) * 260; ty -= fly * (300 + 80 * r_)
        ink(c, wrrect(tx - 70, ty - 60, tx + 70, ty + 60, 8, seed + 10 + i, 1.0), CREAM, 5)
        tee(c, tx, ty, 0.42 * back(kk), _CLOTH_COLS[i], 0, seed + 20 + i, 1.0, kinds[i])
    c.restore()


_EU_PINS = [(620, 700, "VILNIUS"), (430, 880, "PARIS"), (570, 860, "MUNICH"), (380, 730, "LONDON")]


def euro_map(c, x, y, s=1.0, seed=0, t=0.0, pins=0.0, sf=0.0, gone=0.0, k=1.0):
    """rough doodle map (Europe blob right, US coast left, ocean between). pins 0..4 pop in the European pins, sf 0..1 draws a dotted
    route to a 'SAN FRANCISCO' pin; gone 0..1 = all pins except Vilnius drop away."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k); c.translate(-540, -900)
    c.drawRect(skia.Rect.MakeLTRB(60, 560, 1020, 1240), P((170, 215, 245), 0.6))
    for j in range(4): wline(c, [(140 + i * 26, 680 + j * 150 + 10 * math.sin(i + t * 2)) for i in range(6)], seed + j, 4, (80, 150, 210), 1, 0.7)
    ink(c, wpoly([(330, 640), (470, 600), (640, 640), (700, 760), (660, 900), (560, 980), (430, 960), (340, 880), (360, 760)], seed + 10, 3.0, True, 50), (196, 232, 160), 8)
    ink(c, wpoly([(60, 700), (150, 690), (180, 860), (140, 1000), (60, 1040)], seed + 11, 3.0, True, 50), (232, 214, 160), 8)
    for i, (px, py, nm) in enumerate(_EU_PINS):
        kk = min(1.0, max(0.0, pins - i))
        if i > 0 and gone > 0: py += 400 * ease(min(1.0, max(0.0, gone * 1.5 - (i - 1) * 0.2))); kk *= 1.0 if py < 1200 else 0.0
        if kk <= 0: continue
        c.save(); c.translate(px, py); c.scale(back(kk), back(kk))
        ink(c, wpoly([(0, 0), (-22, -40), (-18, -62), (0, -72), (18, -62), (22, -40)], seed + 20 + i, 1.0, True, 20), RED if i else GRN, 6)
        c.drawCircle(0, -52, 8, P(WHITE)); c.restore()
        f = font(BLK_F, 26); c.drawString(nm, px - f.measureText(nm) / 2, py + 34, f, P(INK, kk))
    if sf > 0:
        n = int(sf * 14)
        for j in range(n):
            u = j / 14; px = 620 - 510 * u; py = 700 - 220 * math.sin(math.pi * u) + 200 * u
            c.drawCircle(px, py, 7, P(RED))
        if sf >= 1:
            fy = 900 + (400 * ease(min(1.0, gone * 1.5)) if gone > 0 else 0)
            if fy < 1200:
                ink(c, wpoly([(110, fy), (88, fy - 40), (92, fy - 62), (110, fy - 72), (128, fy - 62), (132, fy - 40)], seed + 30, 1.0, True, 20), RED, 6)
                f = font(BLK_F, 26); c.drawString("SAN FRANCISCO", 40, fy + 34, f, P(INK))
    c.restore()


def money_fire(c, x, y, s=1.0, t=0.0, seed=0, burn=0.0, k=1.0):
    """bill stack on (x, y) with doodle flames (burn 0..1 grows flames and shrinks the stack)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    money_stack(c, 0, 0, max(1, int(7 - 5 * burn)), 1.0, seed)
    if burn > 0:
        for j in range(5):
            fx = -90 + j * 45; fh = (90 + 60 * h01(j, seed + int(t * 10))) * burn; fy = -30 - 34 * max(1, int(7 - 5 * burn))
            ink(c, wpoly([(fx - 30, fy), (fx - 20, fy - fh * 0.6), (fx, fy - fh), (fx + 18, fy - fh * 0.55), (fx + 30, fy)], seed + 40 + j, 2.0, True, 20), (255, 150, 30), 6)
            ink(c, wpoly([(fx - 14, fy), (fx, fy - fh * 0.5), (fx + 14, fy)], seed + 50 + j, 1.4, True, 20), YEL, 0)
    c.restore()


def fee_tag(c, x, y, s=1.0, seed=0, word="SELLER FEE", k=1.0, rot=-6):
    """big swing price tag with a string hole and a word on it."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    ink(c, wpoly([(-200, -70), (170, -70), (240, 0), (170, 70), (-200, 70)], seed, 1.8, True, 40), YEL, 9)
    c.drawCircle(176, 0, 14, P(WHITE)); wline(c, [(190, 0), (260, -60), (300, -40)], seed + 1, 5)
    sz = 56
    while sz > 26 and font(BLK_F, sz).measureText(word) > 330: sz -= 4
    f = font(BLK_F, sz); c.drawString(word, -20 - f.measureText(word) / 2, sz * 0.36, f, P(INK)); c.restore()


def ledger(c, x, y, s=1.0, seed=0, rows=0.0, k=1.0):
    """spiral notebook with sale rows (item ... price) filling in, each ticked."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    ink(c, wrrect(-200, -260, 200, 260, 14, seed, 1.6), WHITE, 9)
    for j in range(7): c.drawCircle(-200, -220 + j * 70, 12, P(GREY)); 
    f = font(MARK_F, 40); c.drawString("SALES LOG", -f.measureText("SALES LOG") / 2, -190, f, P(INK))
    items = [("JACKET", "$25"), ("JEANS", "$12"), ("DRESS", "$18"), ("BOOTS", "$30"), ("SCARF", "$6")]
    for j in range(min(5, int(rows + 0.999))):
        a = min(1.0, rows - j); yy = -120 + j * 72
        wline(c, [(-170, yy + 14), (170, yy + 14)], seed + 10 + j, 3, GREY)
        f2 = font(HAND_F, 36); c.drawString(items[j][0], -160, yy, f2, P(INK, a)); c.drawString(items[j][1], 70, yy, f2, P(INK, a))
        wline(c, [(140, yy - 10), (152, yy + 4), (176, yy - 26)], seed + 20 + j, 6, GRN, a=a)
    c.restore()


def _hoodie(c, x, y, s, t, talk, look, mood, arms, walk, blink, seed, col=(150, 152, 164), **kw):
    """generic grey hoodie hanging on a wire hanger (no logo): hood ring with a face inside, sleeves = stick-ish arms, a pouch pocket.
    (x, y) = bottom hem; it sways."""
    sw = math.sin(t * 2.4 + seed) * 3
    c.save(); c.translate(x, y - 560 * s); c.rotate(sw); c.translate(-x, -(y - 560 * s))
    top = y - 520 * s
    hanger(c, x, top - 10 * s, 1.5 * s, seed + 1)
    body = wpoly([(x - 150 * s, top + 70 * s), (x + 150 * s, top + 70 * s), (x + 170 * s, y - 40 * s), (x + 150 * s, y), (x - 150 * s, y), (x - 170 * s, y - 40 * s)], seed, 2.0, True, 40)
    ink(c, body, col, 9 * s)
    ink(c, wrrect(x - 100 * s, y - 190 * s, x + 100 * s, y - 70 * s, 20 * s, seed + 2, 1.2), shade(col, 0.88), 7 * s)   # pouch
    for sx in (-1, 1):   # drawstrings
        wline(c, [(x + sx * 30 * s, top + 140 * s), (x + sx * 34 * s, top + 240 * s)], seed + 3 + sx, 5 * s, WHITE)
    ink(c, wellipse(x, top + 40 * s, 120 * s, 110 * s, seed + 5, 2.0), col, 9 * s)          # hood
    ink(c, wellipse(x, top + 50 * s, 82 * s, 76 * s, seed + 6, 1.4), (255, 236, 214), 7 * s)   # face opening
    # sleeves as arms (thick), hands = stick hands from limb()
    pre = ARM_PRESETS.get(arms, ARM_PRESETS["down"]) if isinstance(arms, str) else arms
    for (dx, dy), sx in zip(pre, (-1, 1)):
        sx0 = x + sx * 150 * s; sy0 = top + 110 * s
        ex = sx0 + dx * s * 1.1; ey = sy0 + dy * s * 1.1 + 60 * s
        wline(c, [(sx0, sy0), ((sx0 + ex) / 2 + sx * 20 * s, (sy0 + ey) / 2), (ex, ey)], seed + 8 + sx, 46 * s, INK)
        wline(c, [(sx0, sy0), ((sx0 + ex) / 2 + sx * 20 * s, (sy0 + ey) / 2), (ex, ey)], seed + 8 + sx, 30 * s, col)
    eyes(c, x, top + 36 * s, s * 0.8, look, blink, 36, 20, mood, seed + 9)
    mouth(c, x, top + 84 * s, s * 0.6, talk, mood, seed + 10)
    c.restore()
