"""Toon kit for the What-If series: original stick mascot rig + shaded props + designed sets + two-tier type."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mammoth'))
sys.path.insert(0, os.path.join(HERE, '..', 'qday'))
import numpy as np
import skia
import gfx
from gfx import paint, font, cl, pr, eo, eio, eback, lerp, mix, hsh, argb, lin, rad, poly, partial, WHITE
from ed import img_from, _upnoise

gfx._TF.update({'ant': 'Anton.ttf', 'mbk': 'Montserrat-Black.ttf', 'mxb': 'Montserrat-ExtraBold.ttf', 'mss': 'Montserrat-SemiBold.ttf',
                'msm': 'Montserrat-Medium.ttf', 'lil': 'LilitaOne.ttf'})
LAND = os.environ.get('NBN_ORIENT') == 'land'
W, H = (1920, 1080) if LAND else (1080, 1920)
R = skia.Rect
INK = (22, 22, 28)
SAMP = skia.SamplingOptions(skia.CubicResampler.Mitchell())
LINS = skia.SamplingOptions(skia.FilterMode.kLinear)

def stroke(rgb, w, a=1.0, cap=True):
    p = paint(rgb, a, stroke=w)
    p.setStrokeCap(skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap)
    p.setStrokeJoin(skia.Paint.kRound_Join)
    return p

def ease_io(x):
    return x * x * (3 - 2 * x)

# ================================================================== character rig
LEN = dict(torso=78, uarm=48, farm=44, thigh=54, shin=54, head=46)

POSES = {
    #          lean  head  uaL   faL   uaR   faR   thL  shL  thR  shR
    'stand':  (0,    0,    200,  10,   160,  -10,  186, 0,   174, 0),
    'arms_up': (0,   -6,   230,  40,   130,  -40,  190, 0,   170, 0),
    'shock':  (-4,   -8,   235,  60,   125,  -60,  195, 4,   165, -4),
    'point':  (0,    4,    200,  10,   95,   0,    186, 0,   174, 0),
    'point_up': (0,  -10,  200,  10,   125,  0,    186, 0,   174, 0),
    'shrug':  (0,    8,    235,  -95,  125,  95,   186, 0,   174, 0),
    'crouch': (12,   6,    215,  30,   145,  -30,  140, 80,  130, 70),
    'jump':   (-4,   -10,  240,  20,   120,  -20,  200, -30, 165, -20),
    'hug':    (6,    10,   160,  -110, 200,  110,  184, 0,   176, 0),   # arms crossed (cold)
    'sit':    (-4,   0,    205,  20,   155,  -20,  95,  95,  85,  95),
    'press':  (14,   10,   200,  10,   110,  40,   184, 0,   174, 0),
    'wave':   (0,    4,    200,  10,   130,  -70,  186, 0,   174, 0),
    'hold':   (0,    0,    200,  10,   178,  -80,  186, 0,   174, 0),   # holding something in front
    'float':  (-8,   -6,   240,  -20,  120,  20,   200, 30,  165, 25),
}

def lerp_pose(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))

def walk_pose(ph, amp=1.0, run=False):
    s = math.sin(ph * 2 * math.pi); c = math.cos(ph * 2 * math.pi)
    A = 28 * amp if not run else 42 * amp
    thL = 180 + A * s; thR = 180 - A * s
    shL = max(0, -c) * (45 if run else 30) * amp; shR = max(0, c) * (45 if run else 30) * amp
    uaL = 180 - A * 0.9 * s; uaR = 180 + A * 0.9 * s
    return ((8 if run else 3), 0, uaL, 20 + 10 * amp, uaR, -20 - 10 * amp, thL, shL, thR, shR)

class Face:
    def __init__(self, eyes='open', mouth='smile', brows='none', look=(0, 0), blush=False, beard=0.0):
        self.eyes, self.mouth, self.brows, self.look, self.blush, self.beard = eyes, mouth, brows, look, blush, beard

def _pt(x, y, ang, L):
    a = math.radians(ang)
    return x + math.sin(a) * L, y - math.cos(a) * L   # 0 deg = up, 180 = down

def draw_stick(c, x, y, s, pose, face=None, col=WHITE, outline=INK, scarf=(235, 50, 60), t=0.0, helmet=0.0, flip=False,
               bob=0.0, squash=1.0, blink=False, a=1.0, prop=None, frost=0.0):
    """x,y = feet ground point. pose = tuple(10). s = scale."""
    face = face or Face()
    lean, headt, uaL, faL, uaR, faR, thL, shL, thR, shR = pose
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s * squash)
    if a < 1:
        c.saveLayerAlpha(None, int(255 * a))
    L = LEN
    bob = bob + math.sin(t * 2.6) * 2.2
    # shadow
    c.drawOval(R.MakeXYWH(-46, -8, 92, 16), paint((0, 0, 0), 0.18))
    hip = (0, -(L['thigh'] + L['shin']) + bob)
    # legs (angles relative: thigh angle absolute, shin relative bend)
    def leg(th, sh):
        k = _pt(hip[0], hip[1], th, L['thigh'])
        f = _pt(k[0], k[1], th + sh, L['shin'])
        return k, f
    kL, fL = leg(thL, shL)
    kR, fR = leg(thR, shR)
    neck = _pt(hip[0], hip[1], lean, L['torso'])
    sh_ = _pt(hip[0], hip[1], lean, L['torso'] - 8)
    def arm(ua, fa):
        e = _pt(sh_[0], sh_[1], ua, L['uarm'])
        h = _pt(e[0], e[1], ua + fa, L['farm'])
        return e, h
    eL, hL = arm(uaL, faL)
    eR, hR = arm(uaR, faR)
    W_ = 13
    ink = stroke(outline, W_)
    # back limbs first (left)
    c.drawPath(poly([hip, kL, fL]), ink)
    c.drawPath(poly([sh_, eL, hL]), ink)
    c.drawOval(R.MakeXYWH(fL[0] - 14, fL[1] - 8, 28, 14), paint(outline))
    # torso
    c.drawPath(poly([hip, neck]), stroke(outline, 15))
    # scarf
    if scarf:
        sw = math.sin(t * 7) * 6
        p = skia.Path(); p.moveTo(neck[0] - 18, neck[1] + 4); p.lineTo(neck[0] + 18, neck[1] + 4)
        p.lineTo(neck[0] + 14, neck[1] + 18); p.lineTo(neck[0] - 14, neck[1] + 18); p.close()
        c.drawPath(p, paint(scarf)); c.drawPath(p, stroke(outline, 4))
        tail = skia.Path(); tail.moveTo(neck[0] - 10, neck[1] + 14)
        tail.cubicTo(neck[0] - 26, neck[1] + 30, neck[0] - 30 + sw, neck[1] + 46, neck[0] - 40 + sw, neck[1] + 56)
        tail.lineTo(neck[0] - 24 + sw, neck[1] + 60); tail.cubicTo(neck[0] - 18, neck[1] + 40, neck[0] - 6, neck[1] + 28, neck[0] + 2, neck[1] + 16)
        tail.close()
        c.drawPath(tail, paint(scarf)); c.drawPath(tail, stroke(outline, 4))
    c.drawPath(poly([hip, kR, fR]), ink)
    c.drawOval(R.MakeXYWH(fR[0] - 14, fR[1] - 8, 28, 14), paint(outline))
    if prop:
        prop(c, hR, hL)
    c.drawPath(poly([sh_, eR, hR]), ink)
    for h in (hL, hR):
        c.drawCircle(h[0], h[1], 9, paint(col)); c.drawCircle(h[0], h[1], 9, stroke(outline, 5))
    # head
    hr = L['head']
    hc = _pt(neck[0], neck[1], lean + headt, hr + 6)
    c.save(); c.translate(hc[0], hc[1]); c.rotate(lean + headt)
    c.drawCircle(0, 0, hr, paint(col))
    c.drawCircle(-hr * 0.25, -hr * 0.3, hr * 0.8, paint(shader=rad(-hr * 0.25, -hr * 0.3, hr * 0.8, [argb((255, 255, 255), 0.0), argb((255, 255, 255), 0)])))
    c.drawCircle(4, 6, hr, paint(shader=rad(-10, -12, hr * 1.3, [argb((0, 0, 0), 0), argb((0, 0, 0), 0), argb((40, 50, 90), 0.18)], [0, 0.6, 1])))
    if frost > 0:
        c.drawCircle(0, 0, hr, paint((150, 210, 255), 0.45 * frost))
    c.drawCircle(0, 0, hr, stroke(outline, 7))
    draw_face(c, face, hr, blink, t)
    if helmet > 0:
        c.drawCircle(0, 4, hr + 22, paint((190, 230, 255), 0.18 * helmet))
        c.drawCircle(0, 4, hr + 22, stroke((255, 255, 255), 5, 0.9 * helmet))
        c.drawPath(poly([(-hr * 0.6, -hr * 0.75), (-hr * 0.2, -hr * 0.98)]), stroke((255, 255, 255), 8, 0.8 * helmet))
    c.restore()
    if a < 1: c.restore()
    c.restore()
    return dict(head=hc, hand_r=hR, hand_l=hL, neck=neck)

def draw_face(c, f, hr, blink, t):
    lx, ly = f.look[0] * 6, f.look[1] * 5
    ex = 15
    if f.beard > 0:
        b = f.beard
        p = skia.Path(); p.moveTo(-hr * 0.8, 6); p.cubicTo(-hr * 0.7, 30 + 60 * b, -10, 40 + 140 * b, 0, 46 + 160 * b)
        p.cubicTo(10, 40 + 140 * b, hr * 0.7, 30 + 60 * b, hr * 0.8, 6); p.close()
        c.drawPath(p, paint((235, 235, 240))); c.drawPath(p, stroke(INK, 4))
    if f.eyes == 'skull':
        for sx in (-1, 1):
            c.drawOval(R.MakeXYWH(sx * ex - 10, -16, 20, 22), paint(INK))
        p = skia.Path(); p.moveTo(-4, 10); p.lineTo(4, 10); p.lineTo(0, 2); p.close(); c.drawPath(p, paint(INK))
        for i in range(-2, 3):
            c.drawLine(i * 6, 20, i * 6, 28, stroke(INK, 2.5))
        c.drawLine(-14, 24, 14, 24, stroke(INK, 2.5))
        return
    if f.eyes == 'happy':
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(sx * ex - 9 + lx, -2 + ly); p.quadTo(sx * ex + lx, -14 + ly, sx * ex + 9 + lx, -2 + ly)
            c.drawPath(p, stroke(INK, 5))
    elif blink or f.eyes == 'closed':
        for sx in (-1, 1):
            c.drawLine(sx * ex - 8 + lx, -4 + ly, sx * ex + 8 + lx, -4 + ly, stroke(INK, 5))
    else:
        big = 1.35 if f.eyes == 'wide' else 1.0
        for sx in (-1, 1):
            c.drawOval(R.MakeXYWH(sx * ex - 6 * big + lx, -14 * big + ly - 2, 12 * big, 20 * big), paint(INK))
            c.drawCircle(sx * ex - 2 * big + lx, -8 * big + ly - 2, 3 * big, paint(WHITE))
    if f.brows == 'worried':
        for sx in (-1, 1):
            c.drawLine(sx * ex - 9, -26 - (sx * 4), sx * ex + 9, -26 + (sx * 4), stroke(INK, 4))
    elif f.brows == 'angry':
        for sx in (-1, 1):
            c.drawLine(sx * ex - 9, -28 + (sx * 4), sx * ex + 9, -28 - (sx * 4), stroke(INK, 4))
    elif f.brows == 'up':
        for sx in (-1, 1):
            c.drawLine(sx * ex - 8, -32, sx * ex + 8, -34, stroke(INK, 4))
    my = 16 + ly * 0.5
    m = f.mouth
    if m == 'smile':
        p = skia.Path(); p.moveTo(-12 + lx, my); p.quadTo(lx, my + 12, 12 + lx, my); c.drawPath(p, stroke(INK, 5))
    elif m == 'grin':
        p = skia.Path(); p.moveTo(-15 + lx, my - 2); p.quadTo(lx, my + 22, 15 + lx, my - 2); p.close()
        c.drawPath(p, paint(INK)); c.drawPath(p, stroke(INK, 3))
    elif m == 'o':
        c.drawOval(R.MakeXYWH(-7 + lx, my - 4, 14, 18), paint(INK))
    elif m == 'flat':
        c.drawLine(-9 + lx, my + 4, 9 + lx, my + 4, stroke(INK, 5))
    elif m == 'frown':
        p = skia.Path(); p.moveTo(-11 + lx, my + 8); p.quadTo(lx, my - 2, 11 + lx, my + 8); c.drawPath(p, stroke(INK, 5))
    elif m == 'chatter':
        k = (math.sin(t * 40) > 0)
        c.drawRect(R.MakeXYWH(-12 + lx, my, 24, 10 if k else 6), paint(WHITE)); c.drawRect(R.MakeXYWH(-12 + lx, my, 24, 10 if k else 6), stroke(INK, 3))
    elif m == 'puff':
        c.drawCircle(-hr * 0.55, my - 4, 11, paint((255, 170, 170), 0.8)); c.drawCircle(hr * 0.55, my - 4, 11, paint((255, 170, 170), 0.8))
        c.drawLine(-6 + lx, my + 2, 6 + lx, my + 2, stroke(INK, 5))
    if f.blush:
        c.drawOval(R.MakeXYWH(-hr * 0.75, 4, 16, 8), paint((255, 120, 140), 0.5)); c.drawOval(R.MakeXYWH(hr * 0.75 - 16, 4, 16, 8), paint((255, 120, 140), 0.5))

# tiny crowd person sprite
def make_mini(col=(255, 255, 255), scarf=(235, 50, 60), s=1.0):
    S = skia.Surface(60, 100); c = S.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    c.translate(30, 96)
    k = s
    c.drawPath(poly([(0, -40), (-9, -20), (-12, 0)]), stroke(INK, 5))
    c.drawPath(poly([(0, -40), (9, -20), (12, 0)]), stroke(INK, 5))
    c.drawPath(poly([(0, -40), (0, -68)]), stroke(INK, 6))
    c.drawPath(poly([(0, -64), (-14, -46)]), stroke(INK, 5)); c.drawPath(poly([(0, -64), (14, -46)]), stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-7, -68, 14, 5), paint(scarf))
    c.drawCircle(0, -80, 13, paint(col)); c.drawCircle(0, -80, 13, stroke(INK, 3.5))
    c.drawCircle(-4, -81, 1.8, paint(INK)); c.drawCircle(4, -81, 1.8, paint(INK))
    return S.makeImageSnapshot()

MINIS = None
def minis():
    global MINIS
    if MINIS is None:
        cols = [(255, 255, 255), (255, 236, 210), (215, 235, 255), (255, 225, 235)]
        scs = [(235, 50, 60), (40, 140, 255), (255, 190, 30), (60, 200, 110), (160, 80, 240)]
        MINIS = [make_mini(cols[i % 4], scs[i % 5]) for i in range(10)]
    return MINIS

# ================================================================== planets (procedural, shaded)
_TEX = {}
def planet_tex(kind, seed=3):
    key = (kind, seed)
    if key in _TEX: return _TEX[key]
    rng = np.random.default_rng(seed)
    h, w = 1024, 2048
    n = _upnoise(rng, 8, 16, h, w) * 1.0 + _upnoise(rng, 24, 48, h, w) * 0.5 + _upnoise(rng, 80, 160, h, w) * 0.25 + _upnoise(rng, 200, 400, h, w) * 0.12
    def tile(a):
        m = np.sin(np.pi * (np.arange(w) + 0.5) / w)[None, :] ** 2
        if a.ndim == 3: m = m[..., None]
        return a * m + np.roll(a, w // 2, axis=1) * (1 - m)
    n = tile(n)
    n = (n - n.min()) / (n.max() - n.min())
    lat = np.linspace(90, -90, h)[:, None] * np.ones((1, w))
    if kind == 'moon':
        base = np.array([150, 150, 156]); hi = np.array([222, 222, 228])
        v = n[..., None]
        col = base + (hi - base) * v
        maria = np.clip((tile(_upnoise(rng, 4, 8, h, w) + _upnoise(rng, 12, 24, h, w) * 0.4) + 0.05) * 3.0, 0, 1)
        col = col * (1 - 0.32 * maria[..., None])
        yy, xx = np.mgrid[0:h, 0:w]
        for i in range(160):
            cx, cy, r = rng.uniform(40, w - 40), rng.uniform(80, h - 80), rng.uniform(5, 34) * (1.6 if i < 10 else 1)
            x0, x1, y0, y1 = int(cx - r * 1.4), int(cx + r * 1.4) + 1, int(cy - r * 1.4), int(cy + r * 1.4) + 1
            sub = (slice(max(0, y0), y1), slice(max(0, x0), x1))
            d = np.sqrt((xx[sub] - cx) ** 2 + (yy[sub] - cy) ** 2) / r
            shade = np.where(d < 0.85, -0.14 + 0.08 * d, np.where(d < 1.1, 0.16, 0.0))
            col[sub] = col[sub] * (1 + shade[..., None])
    elif kind == 'mars':
        c0 = np.array([110, 38, 20]); c1 = np.array([196, 82, 42]); c2 = np.array([236, 150, 92])
        v = n[..., None]
        col = np.where(v < 0.5, c0 + (c1 - c0) * (v / 0.5), c1 + (c2 - c1) * ((v - 0.5) / 0.5))
        dark = _upnoise(rng, 6, 12, h, w)
        col = col * (1 - 0.22 * np.clip(dark * 2, 0, 1)[..., None])
        # craters
        yy, xx = np.mgrid[0:h, 0:w]
        for i in range(90):
            cx, cy, r = rng.uniform(40, w - 40), rng.uniform(120, h - 120), rng.uniform(8, 40)
            x0, x1, y0, y1 = int(cx - r * 1.3), int(cx + r * 1.3) + 1, int(cy - r * 1.3), int(cy + r * 1.3) + 1
            sub = (slice(max(0, y0), y1), slice(max(0, x0), x1))
            d = np.sqrt((xx[sub] - cx) ** 2 + (yy[sub] - cy) ** 2) / r
            shade = np.where(d < 0.85, -0.16 + 0.1 * d, np.where(d < 1.08, 0.14, 0.0))
            col[sub] = col[sub] * (1 + shade[..., None])
        # valles marineris-ish canyon
        win = np.clip(np.sin(np.clip((xx - w * 0.33) / (w * 0.32), 0, 1) * np.pi), 0, 1) ** 0.7
        cyn = np.exp(-((yy - h * 0.53 - 36 * np.sin(xx / 120)) / 11) ** 2) * win
        col = col * (1 - 0.35 * cyn[..., None])
        cap = np.clip((np.abs(lat) - 76) / 6, 0, 1)[..., None]
        col = col * (1 - cap) + np.array([245, 240, 235]) * cap
    elif kind == 'mercury':
        base = np.array([118, 108, 102]); hi = np.array([205, 195, 185])
        col = base + (hi - base) * n[..., None]
        yy, xx = np.mgrid[0:h, 0:w]
        for i in range(220):
            cx, cy, r = rng.uniform(40, w - 40), rng.uniform(80, h - 80), rng.uniform(5, 30) * (1.8 if i < 12 else 1)
            x0, x1, y0, y1 = int(cx - r * 1.4), int(cx + r * 1.4) + 1, int(cy - r * 1.4), int(cy + r * 1.4) + 1
            sub = (slice(max(0, y0), y1), slice(max(0, x0), x1))
            d = np.sqrt((xx[sub] - cx) ** 2 + (yy[sub] - cy) ** 2) / r
            shade = np.where(d < 0.85, -0.16 + 0.08 * d, np.where(d < 1.1, 0.16, 0.0))
            col[sub] = col[sub] * (1 + shade[..., None])
    elif kind == 'venus':
        sw = tile(_upnoise(rng, 6, 12, h, w))
        b = np.sin(np.radians(lat) * 6 + sw * 7 + n * 3)
        c0 = np.array([196, 140, 60]); c1 = np.array([250, 222, 160])
        v = (b * 0.5 + 0.5)[..., None] * 0.55 + n[..., None] * 0.45
        col = c0 + (c1 - c0) * v
    elif kind in ('jupiter', 'saturn', 'uranus', 'neptune'):
        turb = tile(_upnoise(rng, 10, 20, h, w) * 1.0 + _upnoise(rng, 30, 60, h, w) * 0.5)
        latr = np.radians(lat)
        P = {'jupiter': (14, 2.4, (150, 92, 58), (242, 224, 196), 0.22),
             'saturn': (18, 1.6, (196, 160, 100), (246, 228, 176), 0.14),
             'uranus': (8, 0.6, (120, 205, 220), (180, 238, 242), 0.05),
             'neptune': (9, 1.0, (30, 70, 200), (90, 150, 245), 0.12)}[kind]
        b = np.sin(latr * P[0] + turb * P[1]) * 0.5 + 0.5
        c0 = np.array(P[2]); c1 = np.array(P[3])
        col = c0 + (c1 - c0) * b[..., None]
        col = col * (1 - P[4] + 2 * P[4] * n[..., None])
        yy, xx = np.mgrid[0:h, 0:w]
        if kind == 'jupiter':
            cx, cy = w * 0.62, h * (0.5 + 22 / 180)
            d = ((xx - cx) / 130) ** 2 + ((yy - cy) / 62) ** 2
            spot = np.clip(1.2 - d, 0, 1)[..., None]
            ring = np.sin(np.sqrt(d) * 9) * 0.08
            col = col * (1 - spot) + (np.array([205, 92, 58]) * (1 + ring[..., None])) * spot
        if kind == 'neptune':
            cx, cy = w * 0.4, h * (0.5 + 20 / 180)
            d = ((xx - cx) / 90) ** 2 + ((yy - cy) / 46) ** 2
            spot = np.clip(1.2 - d, 0, 1)[..., None]
            col = col * (1 - 0.6 * spot)
    else:  # earth
        nl = tile(_upnoise(rng, 5, 10, h, w) * 1.0 + _upnoise(rng, 14, 28, h, w) * 0.45 + _upnoise(rng, 50, 100, h, w) * 0.12)
        n = (nl - nl.min()) / (nl.max() - nl.min())
        landf = np.clip((n - 0.545) / 0.03, 0, 1)
        land = n > 0.56
        ocean = np.array([18, 92, 200]) * (0.8 + 0.4 * n[..., None])
        hgt = np.clip((n - 0.56) / 0.3, 0, 1)[..., None]
        green = np.array([52, 150, 70]); brown = np.array([170, 150, 90]); hi = np.array([110, 120, 70])
        lcol = green * (1 - hgt) + hi * hgt
        desert = (np.abs(lat) < 30)[..., None] * np.clip((_upnoise(rng, 10, 20, h, w) + 0.2) * 3, 0, 1)[..., None]
        lcol = lcol * (1 - desert * 0.7) + brown * desert * 0.7
        col = lcol * landf[..., None] + ocean * (1 - landf[..., None])
        cap = np.clip((np.abs(lat) - 70) / 6, 0, 1)[..., None]
        col = col * (1 - cap) + np.array([240, 248, 255]) * cap
    col = tile(col)
    tex = np.clip(col, 0, 255).astype(np.float32)
    clouds = None
    if kind == 'earth':
        cn = tile(_upnoise(rng, 12, 24, h, w) + _upnoise(rng, 40, 80, h, w) * 0.5)
        cn = (cn - cn.min()) / (cn.max() - cn.min())
        clouds = np.clip((cn - 0.55) / 0.25, 0, 1).astype(np.float32)
    _TEX[key] = (tex, clouds)
    return _TEX[key]

_SPH = {}
def _sphere(size):
    if size not in _SPH:
        y, x = np.mgrid[0:size, 0:size].astype(np.float32)
        x = (x + 0.5) / size * 2 - 1; y = (y + 0.5) / size * 2 - 1
        r2 = x * x + y * y
        m = r2 < 1
        z = np.sqrt(np.clip(1 - r2, 0, 1))
        lat = np.arcsin(np.clip(-y, -1, 1))
        lon = np.arctan2(x, z)
        edge = np.clip((1 - np.sqrt(r2)) * size / 2.0, 0, 1)
        _SPH[size] = (x, y, z, m, lat, lon, edge)
    return _SPH[size]

_PC = {}
def planet_img(kind, size, rot=0.0, light=(-0.55, -0.45, 0.70), glow=None, seed=3, night=0.0):
    key = (kind, size, round(rot / 0.004), light, glow, seed)
    if key in _PC: return _PC[key]
    if len(_PC) > 60: _PC.clear()
    im = _planet_img(kind, size, rot, light, glow, seed)
    _PC[key] = im
    return im

def _planet_img(kind, size, rot=0.0, light=(-0.55, -0.45, 0.70), glow=None, seed=3):
    tex, clouds = planet_tex(kind, seed)
    th, tw = tex.shape[:2]
    x, y, z, m, lat, lon, edge = _sphere(size)
    u = (((lon + rot) / (2 * np.pi) + 0.5) % 1.0) * (tw - 1)
    v = (0.5 - lat / np.pi) * (th - 1)
    u0 = np.floor(u).astype(np.int32); v0 = np.clip(np.floor(v).astype(np.int32), 0, th - 2)
    fu = (u - u0)[..., None]; fv = (v - v0)[..., None]
    u1 = (u0 + 1) % tw
    col = (tex[v0, u0] * (1 - fu) + tex[v0, u1] * fu) * (1 - fv) + (tex[v0 + 1, u0] * (1 - fu) + tex[v0 + 1, u1] * fu) * fv
    ui = u0; vi = v0
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    d = x * L[0] + y * L[1] + z * L[2]
    shade = np.clip(d * 1.15 + 0.12, 0.0, 1.0) ** 0.9
    amb = 0.16
    col = col * (amb + (1 - amb) * shade)[..., None]
    if clouds is not None:
        cu = (((lon + rot * 1.15) / (2 * np.pi) + 0.5) % 1.0) * (tw - 1)
        cl_ = clouds[vi, cu.astype(np.int32)][..., None]
        col = col * (1 - cl_ * 0.85) + 255 * cl_ * 0.85 * (amb + (1 - amb) * shade)[..., None]
    # rim atmosphere
    if glow is not None:
        rim = (1 - z) ** 3
        col = col + np.array(glow, np.float32) * (rim * (0.35 + 0.65 * np.clip(d + 0.3, 0, 1)))[..., None] * 0.9
    out = np.zeros((size, size, 4), np.float32)
    out[..., :3] = np.clip(col, 0, 255)
    out[..., 3] = edge * 255
    out[~m] = 0
    a = out[..., 3:4] / 255.0
    out[..., :3] *= a
    return img_from(out.astype(np.uint8), False)

def draw_planet(c, kind, cx, cy, r, rot=0.0, glow=None, halo=None, light=(-0.55, -0.45, 0.70), a=1.0):
    size = int(min(1400, max(64, r * 2)))
    size -= size % 4
    im = planet_img(kind, size, rot, light, glow)
    if halo:
        c.drawCircle(cx, cy, r * 1.25, paint(shader=rad(cx, cy, r * 1.25, [argb(halo, 0.55 * a), argb(halo, 0.25 * a), argb(halo, 0)], [0.75, 0.83, 1])))
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, R.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), LINS, p)

# ================================================================== rocket
STEEL = [(120, 128, 140), (232, 236, 242), (186, 192, 202), (140, 146, 158), (96, 102, 114)]

def draw_rocket(c, x, y, s, flame=0.0, t=0.0, rot=0.0, windows=True, faces=0):
    """x,y = base centre (bottom of engines). height ~ 520*s"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    w = 88; hgt = 470
    if flame > 0:
        draw_flame(c, 0, 4, flame, t)
    # fins
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(sx * w / 2, -40); p.lineTo(sx * (w / 2 + 34), -6); p.lineTo(sx * (w / 2 + 34), 18); p.lineTo(sx * w / 2, 4); p.close()
        c.drawPath(p, paint((70, 76, 88))); c.drawPath(p, stroke(INK, 4))
    body = skia.Path()
    body.moveTo(-w / 2, 0); body.lineTo(-w / 2, -hgt + 120)
    body.cubicTo(-w / 2, -hgt + 40, -14, -hgt, 0, -hgt)
    body.cubicTo(14, -hgt, w / 2, -hgt + 40, w / 2, -hgt + 120)
    body.lineTo(w / 2, 0); body.close()
    sp = paint(shader=lin(-w / 2, 0, w / 2, 0, [argb(cc) for cc in STEEL], [0, 0.32, 0.55, 0.8, 1]))
    c.drawPath(body, sp)
    c.save(); c.clipPath(body, skia.ClipOp.kIntersect, True)
    for yy in range(-hgt + 160, 0, 46):
        c.drawLine(-w / 2, yy, w / 2, yy, stroke((90, 96, 108), 1.6, 0.5))
    c.drawRect(R.MakeXYWH(-w / 2, -hgt, w * 0.18, hgt), paint((255, 255, 255), 0.18))
    if windows:
        for i in range(6):
            yy = -hgt + 150 + i * 26
            c.drawRoundRect(R.MakeXYWH(-26 + (i % 2) * 2, yy, 52, 12), 5, 5, paint((24, 40, 90)))
            c.drawRoundRect(R.MakeXYWH(-26 + (i % 2) * 2, yy, 20, 4), 2, 2, paint((150, 200, 255), 0.8))
    c.restore()
    # front flaps
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(sx * w / 2, -hgt + 135); p.lineTo(sx * (w / 2 + 20), -hgt + 160); p.lineTo(sx * (w / 2 + 20), -hgt + 200); p.lineTo(sx * w / 2, -hgt + 205); p.close()
        c.drawPath(p, paint((70, 76, 88))); c.drawPath(p, stroke(INK, 4))
    c.drawPath(body, stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-w / 2 + 8, -6, w - 16, 10), paint((50, 54, 62)))
    c.restore()

def draw_flame(c, x, y, k, t, scale=1.0):
    fl = 1 + 0.08 * math.sin(t * 50) + 0.05 * math.sin(t * 31)
    L = 260 * k * fl * scale
    for (wid, col, a, lmul) in [(70, (255, 120, 30), 0.55, 1.0), (52, (255, 190, 60), 0.85, 0.82), (30, (255, 250, 220), 1.0, 0.55)]:
        p = skia.Path(); p.moveTo(x - wid / 2 * scale, y)
        p.cubicTo(x - wid / 2 * scale, y + L * lmul * 0.5, x - 6, y + L * lmul * 0.85, x, y + L * lmul)
        p.cubicTo(x + 6, y + L * lmul * 0.85, x + wid / 2 * scale, y + L * lmul * 0.5, x + wid / 2 * scale, y); p.close()
        c.drawPath(p, paint(col, a * min(1, k * 3)))
    c.drawCircle(x, y + L * 0.3, 120 * k * scale, paint((255, 160, 60), 0.25 * min(1, k * 2), blur=40, blend=skia.BlendMode.kPlus))

def smoke(c, x, y, t, t0, n=14, spread=320, seed=1, col=(245, 240, 235), a=1.0, rise=0.0):
    d = t - t0
    if d < 0: return
    for i in range(n):
        ang = (hsh(i, seed) - 0.5) * 3.0
        v = spread * (0.4 + 0.6 * hsh(i, seed + 1))
        xx = x + math.sin(ang) * v * (1 - math.exp(-d * 2.2))
        yy = y - abs(math.cos(ang)) * 60 * (1 - math.exp(-d * 2)) - rise * d
        r = (40 + 60 * hsh(i, seed + 2)) * (0.4 + 0.6 * (1 - math.exp(-d * 2.5)))
        al = a * (1 - pr(d, 1.6, 1.6))
        c.drawCircle(xx, yy, r, paint(shader=rad(xx - r * 0.3, yy - r * 0.3, r * 1.2, [argb(col, al), argb(mix(col, (150, 140, 135), 0.4), al)])))

# ================================================================== sets & type
def set_bg(c, top, bot, circle=None, cx=540, cy=900, r=430, floor=None, spot=True, t=0.0, circ_k=1.0):
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(top), argb(bot)])))
    if spot:
        sr = max(W, H) * 0.52
        c.drawCircle(W / 2, H * 0.4, sr, paint(shader=rad(W / 2, H * 0.4, sr, [argb((255, 255, 255), 0.35), argb((255, 255, 255), 0)])))
    if floor is not None:
        fy = floor
        c.drawRect(R.MakeLTRB(0, fy, W, H), paint(shader=lin(0, fy, 0, H, [argb(mix(bot, (0, 0, 0), 0.05)), argb(mix(bot, (0, 0, 0), 0.18))])))
        c.drawRect(R.MakeLTRB(0, fy - 2, W, fy + 30), paint(shader=lin(0, fy - 2, 0, fy + 30, [argb((0, 0, 0), 0.12), argb((0, 0, 0), 0)])))
    if circle is not None and circ_k > 0:
        rr = r * eback(circ_k, 1.4) if circ_k < 1 else r
        c.drawCircle(cx, cy, rr, paint(circle))
        c.drawCircle(cx, cy, rr, paint(shader=rad(cx - rr * 0.3, cy - rr * 0.35, rr * 1.4, [argb((255, 255, 255), 0.22), argb((255, 255, 255), 0), argb((0, 0, 0), 0.12)], [0, 0.55, 1])))

def space_bg(c, t, top=(22, 36, 110), bot=(8, 10, 40), seed=4, glow=None, gx=540, gy=800):
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(top), argb(bot)])))
    if glow:
        c.drawCircle(gx, gy, 900, paint(shader=rad(gx, gy, 900, [argb(glow, 0.45), argb(glow, 0)])))
    for i in range(170):
        x = hsh(i, seed) * W; y = hsh(i, seed + 1) * H
        r = 1 + 2.4 * hsh(i, seed + 2) ** 3
        tw = 0.55 + 0.45 * math.sin(t * (1 + 2 * hsh(i, seed + 3)) + i)
        c.drawCircle(x, y, r, paint((255, 255, 255), tw))
        if r > 2.6:
            c.drawCircle(x, y, r * 4, paint((180, 200, 255), 0.15 * tw, blur=4))

def two_tier(c, t, t0, small, big, x=None, y=430, big_size=230, small_size=50, big_col=INK, small_col=INK, t1=None,
             key='ant', align='c', track=0, shadow=False, t_big=None, maxw=None):
    """small line on top + one big word that rises into view (clipped)."""
    if t < t0 or (t1 is not None and t > t1 + 0.25): return
    o = 1.0 if t1 is None else 1 - pr(t, t1, 0.25)
    k1 = eo(pr(t, t0, 0.35)); k2 = eo(pr(t, (t0 + 0.12) if t_big is None else t_big, 0.45))
    fs = font('mss', small_size)
    fb = font(key, big_size)
    wb = fb.measureText(big)
    if x is None: x = W / 2
    mw = maxw or W * 0.76
    if wb > mw:
        big_size *= mw / wb; fb = font(key, big_size); wb = fb.measureText(big)
    ws_ = fs.measureText(small)
    xs = x - ws_ / 2 if align == 'c' else x
    xb = x - wb / 2 if align == 'c' else x
    if small:
        sb = y - big_size * 0.86 - small_size * 0.38   # small baseline sits clear of the big word's cap line
        c.save(); c.clipRect(R.MakeLTRB(0, sb - small_size * 1.3, W, sb + small_size * 0.3))
        c.drawString(small, xs, sb + (1 - k1) * small_size * 1.4, fs, paint(small_col, o))
        c.restore()
    c.save(); c.clipRect(R.MakeLTRB(0, y - big_size * 0.95, W, y + big_size * 0.12))
    yy = y + (1 - k2) * big_size * 1.05
    if shadow:
        c.drawString(big, xb + 5, yy + 8, fb, paint((0, 0, 0), 0.25 * o, blur=4))
    c.drawString(big, xb, yy, fb, paint(big_col, o))
    c.restore()

def ground_shadow(c, x, y, w, a=0.22):
    c.drawOval(R.MakeXYWH(x - w / 2, y - w * 0.08, w, w * 0.16), paint((0, 0, 0), a, blur=6))


def rig_points(pose, bob=0.0):
    lean, headt, uaL, faL, uaR, faR, thL, shL, thR, shR = pose
    L = LEN
    hip = (0, -(L['thigh'] + L['shin']) + bob)
    def leg(th, sh):
        k = _pt(hip[0], hip[1], th, L['thigh']); f = _pt(k[0], k[1], th + sh, L['shin']); return k, f
    kL, fL = leg(thL, shL); kR, fR = leg(thR, shR)
    neck = _pt(hip[0], hip[1], lean, L['torso']); sh_ = _pt(hip[0], hip[1], lean, L['torso'] - 8)
    def arm(ua, fa):
        e = _pt(sh_[0], sh_[1], ua, L['uarm']); h = _pt(e[0], e[1], ua + fa, L['farm']); return e, h
    eL, hL = arm(uaL, faL); eR, hR = arm(uaR, faR)
    hc = _pt(neck[0], neck[1], lean + headt, L['head'] + 6)
    return dict(hip=hip, kL=kL, fL=fL, kR=kR, fR=fR, neck=neck, sh=sh_, eL=eL, hL=hL, eR=eR, hR=hR, head=hc)

def xray_figure(c, x, y, s, pose, wk, t):
    P = rig_points(pose, math.sin(t * 2.6) * 2.2)
    c.save(); c.translate(x, y); c.scale(s, s)
    segs = [('hip', 'kL'), ('kL', 'fL'), ('hip', 'kR'), ('kR', 'fR'), ('sh', 'eL'), ('eL', 'hL'), ('sh', 'eR'), ('eR', 'hR'), ('hip', 'neck')]
    flesh = 46 * (1 - 0.35 * wk)
    for a_, b_ in segs:
        c.drawPath(poly([P[a_], P[b_]]), stroke((90, 200, 255), flesh, 0.16))
    c.drawCircle(P['head'][0], P['head'][1], 54, paint((90, 200, 255), 0.14))
    bw = 12 * (1 - 0.5 * wk)
    for a_, b_ in segs:
        c.drawPath(poly([P[a_], P[b_]]), stroke((255, 255, 255), bw, 0.95))
    for j in ('kL', 'kR', 'eL', 'eR', 'hip', 'sh', 'fL', 'fR', 'hL', 'hR'):
        c.drawCircle(P[j][0], P[j][1], bw * 0.85, paint((255, 255, 255), 0.95))
    # ribs
    nx, ny = P['neck']; hx, hy = P['hip']
    for i in range(4):
        yy = ny + 14 + i * 13
        c.drawArc(R.MakeXYWH(nx - 26, yy - 8, 52, 20), 200, 140, False, stroke((255, 255, 255), 5 * (1 - 0.4 * wk), 0.9))
    hc = P['head']
    c.drawCircle(hc[0], hc[1], 40, stroke((255, 255, 255), 8, 0.95))
    for sx in (-1, 1):
        c.drawOval(R.MakeXYWH(hc[0] + sx * 15 - 9, hc[1] - 14, 18, 20), paint((255, 255, 255), 0.9))
    if wk > 0.4:
        a = pr(wk, 0.4, 0.4)
        for (a_, b_) in [('hip', 'kL'), ('sh', 'eR'), ('kR', 'fR')]:
            mx_, my_ = (P[a_][0] + P[b_][0]) / 2, (P[a_][1] + P[b_][1]) / 2
            c.drawPath(poly([(mx_ - 8, my_ - 6), (mx_ + 2, my_), (mx_ - 4, my_ + 4), (mx_ + 8, my_ + 8)]), stroke((255, 80, 80), 3.5, a))
    c.restore()
