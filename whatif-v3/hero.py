"""NextBigNow mascot v3 ('Nova'): painted 3D-look character lit by the scene.

Every body part is a closed path shaded by `shade()`: base colour, a soft form shadow on the side away from the
key light (multiply, tinted by the scene's ambient colour), a soft key highlight (screen), a rim light from behind
(additive, scene colour) and a self-coloured outline. Cast shadows (head on body, hair on forehead, jacket on
pants) and ground contact shadows sell the volume. Same pose tuples as toon.POSES, so old scene code still works.
"""
import math
import skia
from toon import *
from gfx import SCREEN, PLUS

MUL = skia.BlendMode.kMultiply
DIFF = skia.PathOp.kDifference_PathOp
UNION = skia.PathOp.kUnion_PathOp
INTER = skia.PathOp.kIntersect_PathOp

HR = 72                     # head radius
TOR = 96                    # hip -> neck
THIGH, SHIN, ANK = 58, 52, 16
UA, FA = 50, 44
SW = 50                     # shoulder half width

SKIN = (246, 196, 158)
HAIR = (70, 42, 30)
EYE = (34, 22, 24)
BROW = (52, 32, 26)


# ------------------------------------------------------------------ lighting
class Light:
    """key/rim are directions pointing FROM the subject TOWARD the light, in screen space (y down)."""
    def __init__(self, key=(-0.55, -0.85), key_col=(255, 242, 220), ka=0.26, tint=(196, 162, 192), sa=0.95,
                 rim=(0.85, -0.35), rim_col=(255, 196, 130), ra=0.55, ground=(0, 0, 0), ga=0.45, amb=None):
        n = math.hypot(*key); self.kx, self.ky = key[0] / n, key[1] / n
        n = math.hypot(*rim); self.rx, self.ry = rim[0] / n, rim[1] / n
        self.key_col, self.ka, self.tint, self.sa = key_col, ka, tint, sa
        self.rim_col, self.ra, self.ground, self.ga = rim_col, ra, ground, ga
        self.amb = amb          # overall exposure/tint multiplier for the character, e.g. (0.85, 0.82, 0.95)

    def flipped(self):
        L = Light.__new__(Light); L.__dict__.update(self.__dict__)
        L.kx, L.rx = -self.kx, -self.rx
        return L

DEFAULT_LIGHT = Light()


def dark(col, k=0.68):
    return mix(col, (26, 14, 18), k)


def _off(path, dx, dy):
    p = skia.Path(path); p.offset(dx, dy); return p


def shade(c, path, col, L, sz=None, ow=3.4, depth=1.0, hi=1.0, rim=1.0, olcol=None, flat=False, gloss=0.0):
    """Paint a closed path as a lit volume."""
    b = path.computeTightBounds()
    if sz is None:
        sz = max(6.0, min(b.width(), b.height()))
    c.drawPath(path, paint(col))
    if not flat:
        c.save(); c.clipPath(path, doAntiAlias=True)
        big = skia.Path(); big.addRect(b.makeOutset(sz * 2 + 20, sz * 2 + 20))
        d = sz * 0.34 * depth
        shp = skia.Op(big, _off(path, L.kx * d, L.ky * d), DIFF)
        if shp is not None:
            c.drawPath(shp, paint(L.tint, L.sa, blur=sz * 0.085 + 0.8, blend=MUL))
        # bounce from the ground keeps the shadow side from going flat
        if hi > 0:
            cx, cy = b.centerX() + L.kx * sz * 0.30, b.centerY() + L.ky * sz * 0.30
            r = sz * 0.75
            c.drawCircle(cx, cy, r, paint(shader=rad(cx, cy, r, [argb(L.key_col, L.ka * hi), argb(L.key_col, L.ka * hi * 0.35), argb(L.key_col, 0)], [0, 0.5, 1]), blend=SCREEN))
        if gloss > 0:
            gx, gy = b.centerX() + L.kx * sz * 0.36, b.centerY() + L.ky * sz * 0.36
            c.drawOval(R.MakeXYWH(gx - sz * 0.16, gy - sz * 0.09, sz * 0.32, sz * 0.18), paint((255, 255, 255), 0.55 * gloss, blur=sz * 0.04 + 0.5, blend=SCREEN))
        if rim > 0 and L.ra > 0:
            dr = max(1.6, sz * 0.085)
            rp = skia.Op(big, _off(path, -L.rx * dr, -L.ry * dr), DIFF)
            if rp is not None:
                c.drawPath(rp, paint(L.rim_col, L.ra * rim, blur=dr * 0.45 + 0.4, blend=PLUS))
        c.restore()
    if ow:
        c.drawPath(path, stroke(olcol or dark(col), ow))


def cast(c, receiver, caster, L, dist, blur, a=0.5, col=None):
    """Soft shadow of `caster` falling on `receiver` (both paths), away from the key light."""
    c.save(); c.clipPath(receiver, doAntiAlias=True)
    c.drawPath(_off(caster, -L.kx * dist, -L.ky * dist + dist * 0.4), paint(col or mix(L.tint, (40, 20, 40), 0.55), a, blur=blur, blend=MUL))
    c.restore()


def fold(c, pts, col, w=3.0, a=0.55, blur=1.2):
    """A soft cloth crease."""
    p = skia.Path(); p.moveTo(*pts[0])
    if len(pts) == 3: p.quadTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1])
    else:
        for q in pts[1:]: p.lineTo(*q)
    pp = stroke(col, w, a); pp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur)); pp.setBlendMode(MUL)
    c.drawPath(p, pp)


# ------------------------------------------------------------------ path builders
def circ(x, y, r):
    p = skia.Path(); p.addCircle(x, y, r); return p


def oval(x, y, w, h):
    p = skia.Path(); p.addOval(R.MakeXYWH(x - w / 2, y - h / 2, w, h)); return p


def rrect(x, y, w, h, r):
    p = skia.Path(); p.addRoundRect(R.MakeXYWH(x, y, w, h), r, r); return p


def union(*ps):
    out = ps[0]
    for q in ps[1:]:
        r = skia.Op(out, q, UNION)
        if r is not None: out = r
    return out


def capsule(a, b, ra, rb):
    dx, dy = b[0] - a[0], b[1] - a[1]; L_ = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / L_, dx / L_
    q = skia.Path(); q.moveTo(a[0] + nx * ra, a[1] + ny * ra); q.lineTo(b[0] + nx * rb, b[1] + ny * rb)
    q.lineTo(b[0] - nx * rb, b[1] - ny * rb); q.lineTo(a[0] - nx * ra, a[1] - ny * ra); q.close()
    return union(circ(a[0], a[1], ra), q, circ(b[0], b[1], rb))


def smooth_closed(pts):
    """Closed curve through the midpoints of pts (corners become soft points)."""
    n = len(pts)
    mid = lambda i: ((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
    p = skia.Path(); m0 = mid(n - 1); p.moveTo(*m0)
    for i in range(n):
        m = mid(i); p.quadTo(pts[i][0], pts[i][1], m[0], m[1])
    p.close(); return p


def rot_pt(p, ang, o=(0, 0)):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return (o[0] + p[0] * ca - p[1] * sa, o[1] + p[0] * sa + p[1] * ca)


def _pt(x, y, ang, L_):
    a = math.radians(ang)
    return x + math.sin(a) * L_, y - math.cos(a) * L_


# ------------------------------------------------------------------ outfits
OUTFITS = {
    # red utility jacket (open), white tee, backpack, olive cargo joggers, white sneakers with red stripe
    'explorer': dict(style='utility', jacket=(214, 58, 46), trim=(160, 36, 32), tee=(246, 242, 234), pants=(98, 104, 66),
                     pants_style='cargo', shoe=(242, 240, 234), shoe_acc=(214, 58, 46), sole=(70, 70, 78), strap=(46, 48, 58),
                     pack=(232, 168, 46), watch=(40, 42, 50)),
    # navy varsity bomber with cream sleeves + red stripes, black tee, blue jeans, red high-tops
    'varsity': dict(style='varsity', jacket=(36, 52, 112), sleeve=(242, 230, 206), trim=(204, 40, 52), trim2=(242, 230, 206),
                    tee=(34, 34, 40), pants=(62, 98, 160), pants_style='jeans', shoe=(206, 44, 52), shoe_acc=(250, 250, 250),
                    sole=(246, 244, 238), watch=(40, 42, 50)),
    # teal puffer jacket over a grey hoodie, black joggers, white sneakers
    'puffer': dict(style='puffer', jacket=(28, 150, 146), hood=(168, 170, 180), tee=(168, 170, 180), pants=(44, 44, 54),
                   pants_style='jogger', shoe=(246, 246, 246), shoe_acc=(255, 196, 40), sole=(230, 120, 40), watch=None),
}


# ------------------------------------------------------------------ head
def head_path():
    pts = []
    for i in range(64):
        th = i / 64 * 2 * math.pi
        cx, sy = math.cos(th), math.sin(th)
        w = 1.0 + 0.05 * max(0.0, sy)           # fuller cheeks
        pts.append((HR * cx * w, HR * 0.97 * sy + (0.03 * HR * sy * sy if sy > 0 else 0)))
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); return p

_HEAD = None
_HAIR = None


def hair_path():
    u = HR
    outer = [(-0.96, 0.04), (-1.07, -0.36), (-0.97, -0.74), (-0.72, -1.00), (-0.36, -1.13), (-0.04, -1.15), (0.06, -1.38),
             (0.20, -1.14), (0.48, -1.09), (0.78, -0.93), (1.00, -0.62), (1.07, -0.26), (0.97, 0.04)]
    p = skia.Path()
    n = len(outer)
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    p.moveTo(outer[0][0] * u, outer[0][1] * u)
    for i in range(1, n - 1):
        m = mid(outer[i], outer[i + 1])
        p.quadTo(outer[i][0] * u, outer[i][1] * u, m[0] * u, m[1] * u)
    p.lineTo(outer[-1][0] * u, outer[-1][1] * u)
    # fringe: pointed locks sweeping to the right (from the right side back to the left)
    fr = [(0.90, -0.12), (0.84, -0.44), (0.70, -0.14), (0.56, -0.50), (0.38, -0.20), (0.22, -0.54), (0.02, -0.24),
          (-0.14, -0.56), (-0.36, -0.28), (-0.50, -0.58), (-0.72, -0.34), (-0.84, -0.52), (-0.92, -0.08)]
    prev = outer[-1]
    for q in fr:
        cx, cy = (prev[0] + q[0]) / 2 + 0.05, (prev[1] + q[1]) / 2 + 0.02
        p.quadTo(cx * u, cy * u, q[0] * u, q[1] * u)
        prev = q
    p.lineTo(outer[0][0] * u, outer[0][1] * u)
    p.close()
    return p


def draw_face(c, f, L, t, blink=False):
    lx, ly = f.look[0] * 7, f.look[1] * 5
    ex, ey = 26, 6
    # blush
    if f.eyes != 'skull':
        for sx in (-1, 1):
            c.drawOval(R.MakeXYWH(sx * 42 - 15, 26, 30, 15), paint((255, 120, 120), 0.42, blur=5))
    # eyes
    if f.eyes == 'skull':
        for sx in (-1, 1):
            c.drawLine(sx * ex - 9 + lx, ey - 9, sx * ex + 9 + lx, ey + 9, stroke(EYE, 5)); c.drawLine(sx * ex - 9 + lx, ey + 9, sx * ex + 9 + lx, ey - 9, stroke(EYE, 5))
    elif f.eyes == 'happy':
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * ex - 11 + lx, ey + 4 + ly); p.quadTo(sx * ex + lx, ey - 11 + ly, sx * ex + 11 + lx, ey + 4 + ly)
            c.drawPath(p, stroke(EYE, 5.5))
    elif blink or f.eyes == 'closed':
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * ex - 11 + lx, ey + ly); p.quadTo(sx * ex + lx, ey + 7 + ly, sx * ex + 11 + lx, ey + ly)
            c.drawPath(p, stroke(EYE, 5))
    else:
        wide = f.eyes == 'wide'; squint = f.eyes == 'squint'
        w_, h_ = (15, 23) if wide else (13, 19)
        if squint: h_ = 11
        for sx in (-1, 1):
            cx, cy = sx * ex + lx, ey + ly
            if wide:
                c.drawOval(R.MakeXYWH(cx - w_ / 2 - 5, cy - h_ / 2 - 5, w_ + 10, h_ + 10), paint((255, 255, 255), 0.95))
                c.drawOval(R.MakeXYWH(cx - w_ / 2 - 5, cy - h_ / 2 - 5, w_ + 10, h_ + 10), stroke(dark(SKIN, 0.35), 1.6, 0.8))
            c.drawOval(R.MakeXYWH(cx - w_ / 2, cy - h_ / 2, w_, h_), paint(shader=lin(0, cy - h_ / 2, 0, cy + h_ / 2, [argb((14, 8, 10)), argb((70, 44, 40))])))
            c.drawCircle(cx - 2.5, cy - h_ * 0.22, 3.6, paint((255, 255, 255)))
            c.drawCircle(cx + 3, cy + h_ * 0.22, 1.6, paint((255, 255, 255), 0.85))
            if squint:
                c.drawLine(cx - 10, cy - 6, cx + 10, cy - 4, stroke(EYE, 4))
    # brows (tapered, expressive)
    bt = {'worried': 1, 'angry': -1, 'up': 0, 'none': 0, 'sad': 1}.get(f.brows, 0)
    by = -20 - (9 if f.brows == 'up' else 0) - (4 if f.eyes == 'wide' else 0)
    for sx in (-1, 1):
        inner = (sx * 13, by + 8 * bt * 1.0 - (3 if bt < 0 else 0) + (-2 if bt > 0 else 0))
        outer = (sx * 38, by - 6 * bt + 2)
        if bt > 0: inner = (sx * 13, by - 6); outer = (sx * 38, by + 3)
        if bt < 0: inner = (sx * 13, by + 6); outer = (sx * 38, by - 5)
        p = skia.Path()
        nx, ny = 0, -1
        p.moveTo(inner[0], inner[1] - 4.5); p.quadTo((inner[0] + outer[0]) / 2, (inner[1] + outer[1]) / 2 - 7, outer[0], outer[1] - 1.5)
        p.quadTo(outer[0] + sx * 2, outer[1] + 1, outer[0] - sx * 1, outer[1] + 1.5)
        p.quadTo((inner[0] + outer[0]) / 2, (inner[1] + outer[1]) / 2 + 1, inner[0], inner[1] + 4.5); p.close()
        c.drawPath(p, paint(BROW))
    # nose: soft shadow + highlight (no outline)
    c.drawOval(R.MakeXYWH(-7 + lx * 0.6 - L.kx * 3, 20, 14, 8), paint(dark(SKIN, 0.25), 0.6, blur=2.5, blend=MUL))
    c.drawCircle(-2 + lx * 0.6 + L.kx * 2, 19, 2.6, paint((255, 245, 235), 0.6, blur=1))
    # mouth
    my = 38 + ly * 0.4; mx = lx * 0.6; m = f.mouth
    ink = (70, 30, 34)
    if m == 'smile':
        p = skia.Path(); p.moveTo(-12 + mx, my); p.quadTo(mx, my + 10, 12 + mx, my); c.drawPath(p, stroke(ink, 4.2))
    elif m in ('grin', 'open'):
        p = skia.Path()
        if m == 'grin':
            p.moveTo(-17 + mx, my - 3); p.quadTo(mx, my + 24, 17 + mx, my - 3); p.quadTo(mx, my + 1, -17 + mx, my - 3)
        else:
            p.addOval(R.MakeXYWH(-11 + mx, my - 6, 22, 20))
        p.close()
        c.drawPath(p, paint((110, 28, 38)))
        c.save(); c.clipPath(p, doAntiAlias=True)
        c.drawRect(R.MakeXYWH(-20 + mx, my - 8, 40, 7.5), paint((255, 255, 255)))
        c.drawOval(R.MakeXYWH(-9 + mx, my + 7, 18, 12), paint((236, 100, 112)))
        c.restore()
        c.drawPath(p, stroke(ink, 3.2))
    elif m == 'o':
        c.drawOval(R.MakeXYWH(-7 + mx, my - 6, 14, 18), paint((110, 28, 38))); c.drawOval(R.MakeXYWH(-7 + mx, my - 6, 14, 18), stroke(ink, 3.2))
    elif m == 'flat':
        c.drawLine(-9 + mx, my + 2, 9 + mx, my + 2, stroke(ink, 4.2))
    elif m == 'frown':
        p = skia.Path(); p.moveTo(-11 + mx, my + 7); p.quadTo(mx, my - 2, 11 + mx, my + 7); c.drawPath(p, stroke(ink, 4.2))
    elif m == 'wavy':
        p = skia.Path(); p.moveTo(-12 + mx, my + 3); p.quadTo(-6 + mx, my - 3, mx, my + 3); p.quadTo(6 + mx, my + 9, 12 + mx, my + 3)
        c.drawPath(p, stroke(ink, 4))
    elif m == 'teeth':
        p = rrect(-15 + mx, my - 4, 30, 14, 6)
        c.drawPath(p, paint((255, 255, 255))); c.drawLine(-15 + mx, my + 3, 15 + mx, my + 3, stroke((180, 170, 170), 1.8))
        for k in (-7, 0, 7): c.drawLine(k + mx, my - 4, k + mx, my + 10, stroke((180, 170, 170), 1.5))
        c.drawPath(p, stroke(ink, 3))
    elif m == 'chatter':
        k = (math.sin(t * 40) > 0)
        p = rrect(-13 + mx, my - 2, 26, 12 if k else 7, 4)
        c.drawPath(p, paint((255, 255, 255))); c.drawPath(p, stroke(ink, 3))
    elif m == 'puff':
        for sx in (-1, 1): c.drawCircle(sx * 34, my - 8, 13, paint((255, 150, 150), 0.55, blur=2))
        c.drawLine(-6 + mx, my + 2, 6 + mx, my + 2, stroke(ink, 4))


def draw_head(c, f, L, t, blink=False, frost=0.0, sweat=0.0, acc=None):
    global _HEAD, _HAIR
    if _HEAD is None: _HEAD = head_path(); _HAIR = hair_path()
    # ears
    for sx in (-1, 1):
        ep = oval(sx * HR * 0.97, 10, 24, 32)
        shade(c, ep, SKIN, L, sz=24, ow=3.2)
        c.drawArc(R.MakeXYWH(sx * HR * 0.97 - 6, 2, 12, 16), 90 if sx > 0 else -90, 180, False, stroke(dark(SKIN, 0.3), 2.6, 0.7))
    shade(c, _HEAD, SKIN, L, sz=HR * 2, ow=3.6, depth=1.05, hi=1.0)
    # hair shadow on forehead
    cast(c, _HEAD, _HAIR, L, 6, 6, 0.55)
    if frost > 0:
        c.drawPath(_HEAD, paint((150, 210, 255), 0.45 * frost))
    draw_face(c, f, L, t, blink)
    if acc: draw_acc(c, acc, L, t)
    # hair
    shade(c, _HAIR, HAIR, L, sz=HR * 1.2, ow=3.4, depth=0.75, hi=0.7, rim=0.8)
    c.save(); c.clipPath(_HAIR, doAntiAlias=True)
    hl = mix(HAIR, (255, 226, 190), 0.45)
    # soft sheen band across the crown
    p = skia.Path(); p.addArc(R.MakeXYWH(-HR * 0.78, -HR * 1.02, HR * 1.56, HR * 1.0), 200, 110)
    pp = stroke(hl, HR * 0.13, 0.42); pp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, HR * 0.05)); pp.setBlendMode(SCREEN)
    c.drawPath(_off(p, L.kx * HR * 0.08, L.ky * HR * 0.05), pp)
    # lock separations rising from the fringe valleys
    for (x0, y0, x1, y1) in [(0.56, -0.50, 0.46, -0.78), (0.22, -0.54, 0.14, -0.86), (-0.14, -0.56, -0.20, -0.86), (-0.50, -0.58, -0.52, -0.82)]:
        p = skia.Path(); p.moveTo(x0 * HR, y0 * HR); p.quadTo((x0 + x1) / 2 * HR + 4, (y0 + y1) / 2 * HR, x1 * HR, y1 * HR)
        pp = stroke(dark(HAIR, 0.55), 3.0, 0.45); pp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.4))
        c.drawPath(p, pp)
    # darker underside of the fringe (ambient occlusion)
    c.drawPath(_off(_HAIR, 0, -HR * 0.16), paint(dark(HAIR, 0.5), 0.0))
    c.restore()
    if sweat > 0:
        sx_, sy_ = HR * 0.78, -HR * 0.45
        p = skia.Path(); p.moveTo(sx_, sy_ - 16); p.cubicTo(sx_ + 9, sy_ - 2, sx_ + 10, sy_ + 10, sx_, sy_ + 10); p.cubicTo(sx_ - 10, sy_ + 10, sx_ - 9, sy_ - 2, sx_, sy_ - 16); p.close()
        c.saveLayerAlpha(None, int(255 * sweat))
        c.drawPath(p, paint(shader=lin(0, sy_ - 16, 0, sy_ + 10, [argb((170, 225, 255)), argb((70, 160, 235))])))
        c.drawPath(p, stroke((40, 90, 150), 2.4)); c.drawCircle(sx_ - 3, sy_ + 2, 2.5, paint((255, 255, 255)))
        c.restore()


def draw_acc(c, acc, L, t):
    """Face accessories: 'shades', 'sleepmask', 'snorkel'."""
    if acc == 'shades':
        for sx in (-1, 1):
            c.drawLine(sx * 44, 0, sx * HR * 0.98, -2, stroke((30, 30, 36), 4))
        lens = union(rrect(-50, -8, 40, 30, 11), rrect(10, -8, 40, 30, 11))
        c.drawPath(lens, paint(shader=lin(0, -8, 0, 22, [argb((40, 44, 70)), argb((10, 10, 18))])))
        c.save(); c.clipPath(lens, doAntiAlias=True)
        for x0 in (-46, 14):
            p = skia.Path(); p.moveTo(x0, 18); p.lineTo(x0 + 14, -10); p.lineTo(x0 + 22, -10); p.lineTo(x0 + 8, 18); p.close()
            c.drawPath(p, paint((255, 255, 255), 0.35))
        c.restore()
        c.drawPath(lens, stroke((198, 40, 50), 4))
        c.drawLine(-10, 0, 10, 0, stroke((198, 40, 50), 4))
    elif acc == 'sleepmask':
        for sx in (-1, 1):
            c.drawLine(sx * 46, 2, sx * HR * 0.99, -4, stroke((60, 70, 140), 6))
        m = smooth_closed([(-52, -10), (0, -14), (52, -10), (54, 14), (14, 22), (0, 14), (-14, 22), (-54, 14)])
        shade(c, m, (70, 84, 170), L, sz=30, ow=3)
        c.drawPath(m, paint((255, 255, 255), 0.0))
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * 36, 6); p.quadTo(sx * 26, 14, sx * 16, 6)
            c.drawPath(p, stroke((255, 255, 255), 3, 0.85))
    elif acc == 'snorkel':
        for sx in (-1, 1):
            c.drawLine(sx * 48, 0, sx * HR * 0.99, -6, stroke((30, 30, 36), 7))
        fr = rrect(-52, -20, 104, 52, 20)
        c.drawPath(fr, paint((150, 225, 255), 0.35))
        c.save(); c.clipPath(fr, doAntiAlias=True)
        p = skia.Path(); p.moveTo(-40, 30); p.lineTo(-20, -20); p.lineTo(-6, -20); p.lineTo(-26, 30); p.close()
        c.drawPath(p, paint((255, 255, 255), 0.35))
        c.restore()
        c.drawPath(fr, stroke((255, 200, 40), 7)); c.drawPath(fr, stroke(dark((255, 200, 40)), 2))
        tube = skia.Path(); tube.moveTo(HR * 0.86, 30); tube.quadTo(HR * 1.18, 10, HR * 1.12, -HR * 1.25)
        c.drawPath(tube, stroke(dark((255, 200, 40), 0.5), 15)); c.drawPath(tube, stroke((255, 140, 30), 10))
        c.drawRoundRect(R.MakeXYWH(HR * 1.02, -HR * 1.36, 18, 16), 4, 4, paint((255, 200, 40)))


# ------------------------------------------------------------------ hands
def hand_shape(kind, thumb_up):
    """Local frame: wrist at origin, fingers along +x, thumb on -y if thumb_up else +y."""
    s = -1 if thumb_up else 1
    if kind == 'fist':
        p = union(rrect(-2, -13, 28, 26, 11), capsule((8, 11 * s), (20, 6 * s), 5.5, 5))
    elif kind == 'point':
        # index finger along the thumb edge, other fingers curled: reads clearly as pointing
        e = -s          # the edge the index runs along
        iy = -12 if e < 0 else 4.5
        parts = [rrect(-2, -12, 24, 24, 10), rrect(16, iy, 30, 7.5, 3.75)]
        for k, yy in enumerate((-5, 1, 7) if e < 0 else (-7, -1, 5)):
            parts.append(oval(23, yy, 11, 7.5))
        parts.append(capsule((4, e * 9), (10, e * 24), 5.2, 4.6))     # thumb sticks out clearly (finger-gun)
        p = union(*parts)
    elif kind == 'open':
        parts = [rrect(-2, -12, 24, 24, 9)]
        for i, (yy, ln, ang) in enumerate([(-8.5, 19, -10), (-3, 22, -3), (2.5, 21, 3), (8, 17, 10)]):
            a0 = (18, yy); a1 = rot_pt((ln, 0), ang, a0)
            parts.append(capsule(a0, a1, 3.4, 3.1))
        parts.append(capsule((6, 9 * s), (14, 21 * s), 4.6, 4.0))
        p = union(*parts)
    else:  # relaxed: fingers curled forward
        p = union(rrect(-2, -12, 26, 24, 10), oval(24, 0, 12, 20), capsule((7, 9 * s), (17, 14 * s), 4.8, 4.2))
    return p


def draw_hand(c, wrist, ang, kind, side, L, cuff=None, watch=None):
    """ang = direction of the forearm in degrees (0 = +x)."""
    c.save(); c.translate(*wrist); c.rotate(ang)
    hp = hand_shape(kind, thumb_up=(side < 0))
    # local light (rotate light into the hand frame)
    a = math.radians(-ang); ca, sa = math.cos(a), math.sin(a)
    LL = Light.__new__(Light); LL.__dict__.update(L.__dict__)
    LL.kx, LL.ky = L.kx * ca - L.ky * sa, L.kx * sa + L.ky * ca
    LL.rx, LL.ry = L.rx * ca - L.ry * sa, L.rx * sa + L.ry * ca
    shade(c, hp, SKIN, LL, sz=24, ow=3.0, depth=0.8)
    if kind in ('fist', 'relaxed'):
        for yy in (-6, 0, 6):
            c.drawLine(18, yy, 23, yy, stroke(dark(SKIN, 0.4), 1.8, 0.7))
    if kind == 'open':
        c.drawArc(R.MakeXYWH(2, -6, 14, 12), -60, 120, False, stroke(dark(SKIN, 0.35), 1.6, 0.6))
    if watch:
        wp = rrect(-6, -12.5, 9, 25, 3)
        shade(c, wp, watch, LL, sz=9, ow=2.2, hi=0.6)
        c.drawRect(R.MakeXYWH(-4.5, -5, 6, 10), paint((120, 210, 255), 0.85))
    c.restore()


# ------------------------------------------------------------------ shoes
def draw_shoe(c, f, d, O, L, ang=0.0):
    """f = ankle point, d = +1 toe points to +x, -1 to -x."""
    c.save(); c.translate(f[0], f[1] + 2); c.rotate(ang); c.scale(d, 1)
    LL = Light.__new__(Light); LL.__dict__.update(L.__dict__)
    if d < 0: LL.kx, LL.rx = -L.kx, -L.rx
    hi_top = O.get('pants_style') == 'jeans'
    upper = union(rrect(-20, -16 - (8 if hi_top else 0), 44, 28 + (8 if hi_top else 0), 13), oval(22, 2, 46, 24))
    sole = union(rrect(-22, 8, 70, 11, 5.5))
    shade(c, sole, O['sole'], LL, sz=11, ow=2.8, hi=0.5)
    shade(c, upper, O['shoe'], LL, sz=26, ow=3.0, depth=0.8)
    c.save(); c.clipPath(upper, doAntiAlias=True)
    # toe cap + accent stripe
    c.drawArc(R.MakeXYWH(20, -12, 34, 30), -70, 160, False, stroke(dark(O['shoe'], 0.18), 2.2, 0.8))
    p = skia.Path(); p.moveTo(-18, 4); p.cubicTo(-4, 4, 10, -2, 22, -10); p.lineTo(26, -5); p.cubicTo(12, 4, 0, 9, -18, 10); p.close()
    c.drawPath(p, paint(O['shoe_acc'])); c.drawPath(p, stroke(dark(O['shoe_acc']), 1.4))
    c.restore()
    # laces
    for i in range(2):
        x = 6 + i * 8
        c.drawLine(x - 3, -13 + i * 3, x + 4, -10 + i * 3, stroke(dark(O['shoe'], 0.3), 2.2, 0.8))
    c.drawLine(-20, 13, 46, 13, stroke(dark(O['sole'], 0.3), 1.4, 0.6))
    c.restore()


# ------------------------------------------------------------------ torso / outfits
def torso_path():
    p = skia.Path()
    p.moveTo(-16, -98); p.quadTo(-34, -97, -45, -89); p.quadTo(-56, -80, -53, -62)
    p.cubicTo(-50, -42, -44, -22, -46, -2); p.lineTo(-48, 14); p.quadTo(0, 21, 48, 14); p.lineTo(46, -2)
    p.cubicTo(44, -22, 50, -42, 53, -62); p.quadTo(56, -80, 45, -89); p.quadTo(34, -97, 16, -98); p.quadTo(0, -92, -16, -98)
    p.close(); return p

_TORSO = None


def draw_torso(c, O, L, t):
    """Local torso frame: hip at origin, neck at (0, -TOR)."""
    global _TORSO
    if _TORSO is None: _TORSO = torso_path()
    T = _TORSO
    st = O['style']
    jcol = O['jacket']
    if st == 'utility':
        shade(c, T, jcol, L, sz=96, ow=3.6, depth=0.55)
        # open front: tee panel
        tee = skia.Path(); tee.moveTo(-15, -97); tee.quadTo(0, -86, 15, -97); tee.lineTo(21, 15); tee.quadTo(0, 19, -21, 15); tee.close()
        tee = skia.Op(tee, T, INTER) or tee
        shade(c, tee, O['tee'], L, sz=40, ow=0, depth=0.6, hi=0.7)
        c.drawPath(tee, stroke(dark(O['tee'], 0.4), 2.2))
        # tee graphic: tiny planet-ring logo
        c.drawCircle(1, -28, 7, paint((32, 46, 96))); c.drawOval(R.MakeXYWH(-11, -31, 24, 6), stroke((214, 58, 46), 2.2))
        # zipper edges
        for sx in (-1, 1):
            e = skia.Path(); e.moveTo(sx * 15, -97); e.lineTo(sx * 21, 15)
            c.drawPath(e, stroke(O['trim'], 5)); c.drawPath(e, stroke(dark(jcol), 1.6))
        c.save(); c.clipPath(T, doAntiAlias=True)
        # hem band
        c.drawRect(R.MakeLTRB(-60, 4, -21, 30), paint(O['trim'])); c.drawRect(R.MakeLTRB(21, 4, 60, 30), paint(O['trim']))
        c.drawLine(-60, 4, -21, 4, stroke(dark(jcol), 1.8)); c.drawLine(21, 4, 60, 4, stroke(dark(jcol), 1.8))
        c.restore()
        # chest pockets with flaps
        for sx in (-1, 1):
            px = sx * 33
            pk = rrect(px - 11, -66, 22, 22, 4)
            shade(c, pk, jcol, L, sz=22, ow=2.2, hi=0.5)
            fl = rrect(px - 12.5, -70, 25, 9, 3)
            shade(c, fl, mix(jcol, (0, 0, 0), 0.08), L, sz=9, ow=2.2, hi=0.5)
            c.drawCircle(px, -64, 2, paint((40, 40, 46)))
        # folds at the waist
        for sx in (-1, 1):
            fold(c, [(sx * 46, -24), (sx * 36, -18), (sx * 28, -8)], dark(jcol, 0.3), 2.6)
            fold(c, [(sx * 48, -46), (sx * 40, -40), (sx * 34, -30)], dark(jcol, 0.3), 2.2, 0.4)
        # backpack straps + chest strap
        sc = O['strap']
        for sx in (-1, 1):
            sp = skia.Path(); sp.moveTo(sx * 27, -97); sp.quadTo(sx * 33, -60, sx * 36, -12)
            spp = stroke(sc, 11, cap=False)
            fp = skia.Path(); spp.getFillPath(sp, fp)
            shade(c, fp, sc, L, sz=11, ow=2.2, hi=0.7)
            c.drawRect(R.MakeXYWH(sx * 33 - 7, -34, 14, 7), paint((200, 202, 210))); c.drawRect(R.MakeXYWH(sx * 33 - 7, -34, 14, 7), stroke((60, 60, 70), 1.4))
        cs = rrect(-32, -58, 64, 7, 3)
        shade(c, cs, sc, L, sz=7, ow=2, hi=0.6)
        c.drawRoundRect(R.MakeXYWH(-7, -60, 14, 11), 3, 3, paint((232, 168, 46))); c.drawRoundRect(R.MakeXYWH(-7, -60, 14, 11), 3, 3, stroke((90, 60, 20), 1.4))
        # collar flaps
        for sx in (-1, 1):
            cp = skia.Path(); cp.moveTo(sx * 12, -101); cp.quadTo(sx * 26, -104, sx * 38, -96); cp.lineTo(sx * 24, -76); cp.quadTo(sx * 18, -86, sx * 12, -101); cp.close()
            shade(c, cp, mix(jcol, (255, 255, 255), 0.06), L, sz=16, ow=2.6, hi=0.8)
    elif st == 'varsity':
        shade(c, T, jcol, L, sz=96, ow=3.6, depth=0.55)
        c.save(); c.clipPath(T, doAntiAlias=True)
        # ribbed hem with stripes
        c.drawRect(R.MakeLTRB(-60, 2, 60, 30), paint(jcol))
        for yy, col in ((6, O['trim']), (10.5, O['trim2']), (15, O['trim'])):
            c.drawRect(R.MakeLTRB(-60, yy, 60, yy + 3), paint(col))
        for x in range(-56, 60, 5): c.drawLine(x, 2, x, 30, stroke(dark(jcol, 0.3), 1, 0.5))
        c.drawLine(-60, 2, 60, 2, stroke(dark(jcol), 1.8))
        c.restore()
        # placket + snaps
        c.drawLine(0, -88, 0, 4, stroke(dark(jcol, 0.45), 2.2))
        for yy in (-74, -52, -30, -8):
            c.drawCircle(0, yy, 3.6, paint((210, 212, 220))); c.drawCircle(0, yy, 3.6, stroke((60, 60, 70), 1.2)); c.drawCircle(-1, yy - 1, 1.2, paint((255, 255, 255)))
        # ribbed collar
        col_p = skia.Path(); col_p.moveTo(-20, -100); col_p.quadTo(0, -86, 20, -100); col_p.lineTo(26, -94); col_p.quadTo(0, -74, -26, -94); col_p.close()
        shade(c, col_p, jcol, L, sz=12, ow=2.4, hi=0.6)
        c.save(); c.clipPath(col_p, doAntiAlias=True)
        for k, col in ((0, O['trim']), (1, O['trim2']), (2, O['trim'])):
            p = skia.Path(); p.moveTo(-26, -96 + k * 3.5); p.quadTo(0, -80 + k * 3.5, 26, -96 + k * 3.5)
            c.drawPath(p, stroke(col, 2.2))
        c.restore()
        # tee peeking
        tp = skia.Path(); tp.moveTo(-15, -99); tp.quadTo(0, -90, 15, -99); tp.quadTo(0, -93, -15, -99); tp.close()
        c.drawPath(tp, paint(O['tee']))
        # chest letter patch
        # chenille letter patch: cream felt base, red letter, stitched edge
        f = font('ant', 34); s_ = 'N'
        w_ = f.measureText(s_)
        tb = skia.TextBlob(s_, f)
        c.drawTextBlob(tb, 27 - w_ / 2, -44, stroke(dark(O['trim2'], 0.45), 11))
        c.drawTextBlob(tb, 27 - w_ / 2, -44, stroke(O['trim2'], 8))
        c.drawTextBlob(tb, 27 - w_ / 2, -44, paint(O['trim']))
        c.save()
        c.drawTextBlob(tb, 27 - w_ / 2 - 1, -45, paint((255, 255, 255), 0.18, blend=SCREEN))
        c.restore()
        c.drawTextBlob(tb, 27 - w_ / 2, -44, stroke(dark(O['trim'], 0.5), 1.0))
        for sx in (-1, 1):
            fold(c, [(sx * 46, -24), (sx * 36, -18), (sx * 26, -8)], dark(jcol, 0.3), 2.6)
            c.drawLine(sx * 22, -20, sx * 34, -20, stroke(dark(jcol, 0.4), 2))   # welt pockets
    elif st == 'puffer':
        # hood of the hoodie lying over the back of the collar
        hood = smooth_closed([(-40, -100), (-30, -118), (0, -124), (30, -118), (40, -100), (0, -92)])
        shade(c, hood, O['hood'], L, sz=26, ow=3, hi=0.6)
        shade(c, T, jcol, L, sz=96, ow=3.6, depth=0.5)
        c.save(); c.clipPath(T, doAntiAlias=True)
        seams = [-78, -54, -30, -6, 18]
        for i in range(len(seams) - 1):
            y0, y1 = seams[i], seams[i + 1]
            ym = (y0 + y1) / 2
            c.drawRect(R.MakeLTRB(-70, ym - 5, 70, ym + 5), paint(L.key_col, 0.22, blur=5, blend=SCREEN))
        for yy in seams:
            p = skia.Path(); p.moveTo(-60, yy - 3); p.quadTo(0, yy + 5, 60, yy - 3)
            pp = stroke(dark(jcol, 0.45), 6, 0.5); pp.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3)); pp.setBlendMode(MUL)
            c.drawPath(p, pp); c.drawPath(p, stroke(dark(jcol, 0.55), 1.8))
        c.restore()
        # zipper
        c.drawLine(0, -96, 0, 16, stroke(dark(jcol, 0.5), 3)); c.drawLine(0, -96, 0, 16, stroke((200, 204, 210), 1.2, 0.8))
        c.drawRoundRect(R.MakeXYWH(-3.5, -70, 7, 14), 2, 2, paint((210, 212, 220))); c.drawRoundRect(R.MakeXYWH(-3.5, -70, 7, 14), 2, 2, stroke((60, 60, 70), 1.2))
        # funnel collar
        fc = rrect(-27, -112, 54, 24, 10)
        shade(c, fc, mix(jcol, (255, 255, 255), 0.05), L, sz=24, ow=3, hi=0.8)
        c.drawLine(0, -112, 0, -88, stroke(dark(jcol, 0.5), 2))
        # hoodie drawstrings out of the collar
        for sx in (-1, 1):
            c.drawLine(sx * 9, -88, sx * 10, -64 - 4 * sx, stroke((236, 236, 240), 3.2)); c.drawCircle(sx * 10, -64 - 4 * sx, 2.4, paint((200, 200, 205)))


def draw_sleeve(c, o, e, h, O, L, front=True):
    st = O['style']
    col = O.get('sleeve', O['jacket'])
    path = union(capsule(o, e, 16, 14.5), capsule(e, h, 14.5, 12.5))
    shade(c, path, col, L, sz=28, ow=3.2, depth=0.8, gloss=0.6 if st == 'varsity' else 0.0)
    dx, dy = h[0] - e[0], h[1] - e[1]; Ln = math.hypot(dx, dy) + 1e-6; ux, uy = dx / Ln, dy / Ln
    # elbow crease
    fold(c, [(e[0] - uy * 10 - ux * 4, e[1] + ux * 10 - uy * 4), (e[0] - ux * 1, e[1] - uy * 1), (e[0] + uy * 9 - ux * 6, e[1] - ux * 9 - uy * 6)], dark(col, 0.3), 2.4, 0.5)
    if st == 'puffer':
        for k in (0.35, 0.7):
            for (a_, b_) in ((o, e), (e, h)):
                px, py = lerp(a_[0], b_[0], k), lerp(a_[1], b_[1], k)
                ddx, ddy = b_[0] - a_[0], b_[1] - a_[1]; LL = math.hypot(ddx, ddy) + 1e-6
                nx, ny = -ddy / LL * 14, ddx / LL * 14
                c.drawLine(px - nx, py - ny, px + nx, py + ny, stroke(dark(col, 0.5), 1.8, 0.8))
    # cuff
    cx, cy = h[0] - ux * 7, h[1] - uy * 7
    cuff_col = O.get('trim', dark(col, 0.15)) if st != 'puffer' else dark(col, 0.12)
    cp = capsule((cx - ux * 5, cy - uy * 5), (cx + ux * 3, cy + uy * 3), 13, 13)
    shade(c, cp, cuff_col if st != 'utility' else mix(col, (0, 0, 0), 0.1), L, sz=16, ow=2.6, hi=0.5)
    if st == 'varsity':
        for k in (-2.5, 1.5):
            c.drawLine(cx + ux * k - uy * 12, cy + uy * k + ux * 12, cx + ux * k + uy * 12, cy + uy * k - ux * 12, stroke(O['trim2'], 1.8))


def draw_leg(c, hp, k, f, O, L, side):
    col = O['pants']
    path = union(capsule(hp, k, 18, 15.5), capsule(k, f, 15.5, 13.5))
    shade(c, path, col, L, sz=32, ow=3.2, depth=0.8)
    dx, dy = k[0] - hp[0], k[1] - hp[1]; Ln = math.hypot(dx, dy) + 1e-6; ux, uy = dx / Ln, dy / Ln
    nx, ny = -uy, ux
    if O['pants_style'] == 'cargo':
        # side pocket on the outer thigh
        mx, my = lerp(hp[0], k[0], 0.55), lerp(hp[1], k[1], 0.55)
        ox = side * 7
        c.save(); c.translate(mx + ox, my); c.rotate(math.degrees(math.atan2(dy, dx)) - 90)
        pk = rrect(-8, -11, 16, 22, 3)
        shade(c, pk, col, L, sz=16, ow=2, hi=0.5)
        c.drawLine(-8, -6, 8, -6, stroke(dark(col), 1.6))
        c.restore()
    if O['pants_style'] == 'jeans':
        c.drawLine(hp[0] + side * 12, hp[1], f[0] + side * 9, f[1] - 4, stroke(dark(col, 0.25), 1.4, 0.7))
        mx, my = lerp(hp[0], k[0], 0.5), lerp(hp[1], k[1], 0.5)
        c.save(); c.clipPath(path, doAntiAlias=True)
        c.drawOval(R.MakeXYWH(mx - 9, my - 18, 18, 36), paint((200, 225, 255), 0.25, blur=6, blend=SCREEN))
        c.restore()
    # knee crease
    fold(c, [(k[0] - 9, k[1] - 2), (k[0], k[1] + 3), (k[0] + 9, k[1] - 1)], dark(col, 0.3), 2.2, 0.45)
    # ankle cuff
    fdx, fdy = f[0] - k[0], f[1] - k[1]; Lf = math.hypot(fdx, fdy) + 1e-6
    if O['pants_style'] in ('cargo', 'jogger'):
        cp = capsule((f[0] - fdx / Lf * 9, f[1] - fdy / Lf * 9), (f[0] - fdx / Lf * 2, f[1] - fdy / Lf * 2), 13.5, 13.5)
        shade(c, cp, dark(col, 0.12), L, sz=14, ow=2.4, hi=0.4)
    else:
        cp = capsule((f[0] - fdx / Lf * 10, f[1] - fdy / Lf * 10), (f[0] - fdx / Lf * 3, f[1] - fdy / Lf * 3), 15, 15)
        shade(c, cp, mix(col, (255, 255, 255), 0.15), L, sz=14, ow=2.4, hi=0.5)


def draw_backpack(c, O, L):
    """Local torso frame. Pack sits behind the torso; we see its top and sides."""
    p = smooth_closed([(-44, -104), (-30, -120), (0, -124), (30, -120), (44, -104), (40, -60), (-40, -60)])
    shade(c, p, O['pack'], L, sz=50, ow=3.2, depth=0.6)
    h = skia.Path(); h.moveTo(-10, -122); h.quadTo(0, -134, 10, -122)
    c.drawPath(h, stroke(O['strap'], 5)); c.drawPath(h, stroke(dark(O['strap']), 1.4))


# ------------------------------------------------------------------ the character
def draw_hero(c, x, y, s, pose, face=None, outfit='explorer', L=None, t=0.0, flip=False, bob=0.0, squash=1.0, blink=False,
              a=1.0, prop=None, frost=0.0, hands=('relaxed', 'relaxed'), sweat=0.0, shadow=1.0, breathe=True, arm_over=False, acc=None):
    """x, y = ground point between the feet. s = scale (1.0 = ~400 px tall)."""
    face = face or Face()
    O = OUTFITS[outfit] if isinstance(outfit, str) else outfit
    L = L or DEFAULT_LIGHT
    LL = L.flipped() if flip else L
    lean, headt, uaL, faL, uaR, faR, thL, shL, thR, shR = pose
    c.save(); c.translate(x, y)
    # ground shadows (unflipped space, so they fall away from the screen-space light)
    if shadow > 0:
        c.drawOval(R.MakeXYWH(-70 * s, -10 * s, 140 * s, 22 * s), paint(L.ground, L.ga * shadow, blur=6 * s))
        c.drawOval(R.MakeXYWH(-46 * s, -6 * s, 92 * s, 12 * s), paint(L.ground, L.ga * shadow * 0.9, blur=2.5 * s))
        c.save(); c.skew(-L.kx * 1.6, 0); c.drawOval(R.MakeXYWH(-50 * s, -30 * s * abs(L.ky), 100 * s, 30 * s * abs(L.ky) + 6 * s), paint(L.ground, L.ga * shadow * 0.35, blur=12 * s)); c.restore()
    c.scale(-s if flip else s, s * squash)
    layered = a < 1 or L.amb is not None
    if layered:
        lp = skia.Paint(); lp.setAlphaf(a)
        if L.amb is not None:
            r_, g_, b_ = L.amb
            lp.setColorFilter(skia.ColorFilters.Matrix([r_, 0, 0, 0, 0, 0, g_, 0, 0, 0, 0, 0, b_, 0, 0, 0, 0, 0, 1, 0]))
        c.saveLayer(None, lp)
    br = math.sin(t * 2.4) * 1.6 if breathe else 0.0
    hip = (0, -(THIGH + SHIN + ANK) + bob + br * 0.3)

    def leg(th, sh_, side):
        hp = (hip[0] + side * 15, hip[1])
        k = _pt(hp[0], hp[1], th, THIGH)
        f = _pt(k[0], k[1], th + sh_, SHIN)
        return hp, k, f
    hpL, kL, fL = leg(thL, shL, -1); hpR, kR, fR = leg(thR, shR, 1)
    neck = _pt(hip[0], hip[1], lean, TOR + br)

    def torso_pt(px, py):
        return rot_pt((px, py), lean, hip)

    def arm(ua, fa, side):
        o = torso_pt(side * (SW - 14), -TOR + 16 + br)
        e = _pt(o[0], o[1], ua, UA)
        h = _pt(e[0], e[1], ua + fa, FA)
        return o, e, h
    oL, eL, hL = arm(uaL, faL, -1); oR, eR, hR = arm(uaR, faR, 1)

    # backpack behind everything
    c.save(); c.translate(*hip); c.rotate(lean); c.translate(0, br)
    if O.get('pack'): draw_backpack(c, O, LL)
    c.restore()
    # legs + shoes
    draw_leg(c, hpL, kL, fL, O, LL, -1); draw_leg(c, hpR, kR, fR, O, LL, 1)
    draw_shoe(c, fL, -1, O, LL, ang=-(thL + shL - 180) * 0.5); draw_shoe(c, fR, 1, O, LL, ang=-(thR + shR - 180) * 0.5)
    # neck
    hc = _pt(neck[0], neck[1], lean + headt, 72)
    nk = capsule(neck, _pt(neck[0], neck[1], lean + headt, 30), 15, 14)
    shade(c, nk, SKIN, LL, sz=28, ow=3)
    # torso
    c.save(); c.translate(*hip); c.rotate(lean); c.translate(0, br)
    draw_torso(c, O, LL, t)
    # head shadow on chest + jacket shadow on the pants
    tp = _TORSO
    c.save(); c.clipPath(tp, doAntiAlias=True)
    c.drawOval(R.MakeXYWH(-46 - LL.kx * -6, -112, 92, 34), paint(mix(LL.tint, (40, 20, 40), 0.5), 0.55, blur=9, blend=MUL))
    c.restore()
    c.restore()
    # arms (back one first)
    def arm_draw(o, e, h, side, kind):
        draw_sleeve(c, o, e, h, O, LL)
        ang = math.degrees(math.atan2(h[1] - e[1], h[0] - e[0]))
        draw_hand(c, h, ang, kind, side, LL, watch=(O.get('watch') if side < 0 else None))
    over_L = arm_over in ('L', 'both'); over_R = arm_over in (True, 'R', 'both')
    if not over_L: arm_draw(oL, eL, hL, -1, hands[0])
    if prop: prop(c, hR, hL)
    if not over_R: arm_draw(oR, eR, hR, 1, hands[1])
    # head
    c.save(); c.translate(*hc); c.rotate(lean + headt)
    HL = Light.__new__(Light); HL.__dict__.update(LL.__dict__)
    draw_head(c, face, HL, t, blink, frost, sweat, acc)
    c.restore()
    if over_L: arm_draw(oL, eL, hL, -1, hands[0])
    if over_R: arm_draw(oR, eR, hR, 1, hands[1])
    if layered: c.restore()
    c.restore()
    sx = -s if flip else s
    return dict(head=(x + hc[0] * sx, y + hc[1] * s * squash), hand_r=(x + hR[0] * sx, y + hR[1] * s * squash),
                hand_l=(x + hL[0] * sx, y + hL[1] * s * squash), neck=(x + neck[0] * sx, y + neck[1] * s * squash))
