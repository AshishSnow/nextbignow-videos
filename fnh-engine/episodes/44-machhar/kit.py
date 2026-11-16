"""Retro 90s-anime drawing kit (cairo): palette, cel-shaded shapes, the heroine Riya, props,
backgrounds, effects, Hindi text (PIL + raqm) and the VHS/film grade."""
import math, random, functools
import numpy as np, cairo, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
INK = (0.17, 0.11, 0.19)
FONT = '/home/claude/studio/fonts/hi/baloo-2-800.ttf'
FONT2 = '/home/claude/studio/fonts/hi/mukta-700.ttf'


def hx(h, a=1.0):
    h = h.lstrip('#'); return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


P = dict(
    skin=hx('F6CDB0'), skin_sh=hx('E0A08A'), blush=hx('F08A8A', .55),
    hair=hx('2B2F5E'), hair_sh=hx('1B1C3E'), hair_hi=hx('6F78C8'),
    top=hx('F2A33A'), top_sh=hx('C8742A'), jeans=hx('3E64A8'), jeans_sh=hx('2C4680'),
    shoe=hx('F4F1EA'), shoe_sh=hx('C9C2B6'), eye=hx('5A3A2A'), eye2=hx('B9734A'), white=hx('FFFDF7'),
    pj=hx('9BC6E8'), pj_sh=hx('6E9CC6'),
)


# ---------------------------------------------------------------- easing
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def lerp(a, b, t): return a + (b - a) * t


# ---------------------------------------------------------------- primitives
def setc(c, col): c.set_source_rgba(*col)


def fill_stroke(c, col, lw=5, ink=INK):
    setc(c, col); c.fill_preserve()
    if lw: c.set_line_width(lw); setc(c, ink); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    else: c.new_path()


def ellipse(c, x, y, rx, ry):
    c.save(); c.translate(x, y); c.scale(max(rx, .01), max(ry, .01)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()


def rrect(c, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


def poly(c, pts, close=True):
    c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    if close: c.close_path()


def smooth(c, pts, close=True):
    """Catmull-Rom through points."""
    n = len(pts)
    if n < 3: return poly(c, pts, close)
    P_ = pts + pts[:3] if close else [pts[0]] + pts + [pts[-1]]
    c.move_to(*P_[1] if close else pts[0])
    rng = range(1, n + 1) if close else range(1, n)
    for i in rng:
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        c.curve_to(*c1, *c2, *p2)
    if close: c.close_path()


def limb(c, a, b, ra, rb, col, sh=None, lw=5):
    """Tapered capsule from a to b with radii ra, rb; cel shadow on one side."""
    ax, ay = a; bx, by = b
    ang = math.atan2(by - ay, bx - ax); nx, ny = -math.sin(ang), math.cos(ang)
    c.new_path()
    c.arc(ax, ay, ra, ang + math.pi / 2, ang + 3 * math.pi / 2)
    c.arc(bx, by, rb, ang - math.pi / 2, ang + math.pi / 2)
    c.close_path()
    setc(c, col); c.fill_preserve()
    if sh:
        c.save(); c.clip()
        c.new_path(); c.move_to(ax + nx * ra * .2, ay + ny * ra * .2); c.line_to(bx + nx * rb * .2, by + ny * rb * .2)
        c.line_to(bx + nx * rb * 1.5, by + ny * rb * 1.5); c.line_to(ax + nx * ra * 1.5, ay + ny * ra * 1.5); c.close_path()
        setc(c, sh); c.fill(); c.restore()
        c.new_path(); c.arc(ax, ay, ra, ang + math.pi / 2, ang + 3 * math.pi / 2); c.arc(bx, by, rb, ang - math.pi / 2, ang + math.pi / 2); c.close_path()
    c.set_line_width(lw); setc(c, INK); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def polar(o, ang_deg, L):
    a = math.radians(ang_deg); return (o[0] + math.sin(a) * L, o[1] + math.cos(a) * L)


# ---------------------------------------------------------------- Riya
DEFAULT_POSE = dict(
    lsh=12, lel=-6, rsh=-12, rel=6,   # arm angles (deg from straight down; +ve = towards her left/viewer right)
    lhip=4, lkn=0, rhip=-4, rkn=0,    # leg angles
    tilt=0, lean=0, crouch=0,          # head tilt, body lean, hip drop (px)
    eyes=1.0, look=(0, 0), mouth='smile', blush=0, brow=0, sweat=0, outfit='casual', hair_wind=0,
    hand_l=None, hand_r=None, blink=0, thigh=1.0,
)


def riya(c, x, y, s=1.0, **kw):
    """Riya, front view. (x, y) = point between her feet on the floor. ~900 px tall at s=1."""
    p = dict(DEFAULT_POSE); p.update(kw)
    c.save(); c.translate(x, y); c.scale(s, s)
    out = p['outfit']
    topc, topsh = (P['pj'], P['pj_sh']) if out == 'pj' else (P['top'], P['top_sh'])
    legc, legsh = (P['pj'], P['pj_sh']) if out == 'pj' else (P['jeans'], P['jeans_sh'])
    cr = p['crouch']
    hip = (0, -430 + cr)
    if cr > 0 and p.get('squat', True) and p['lkn'] == 0 and p['rkn'] == 0 and p['thigh'] == 1.0:
        th = math.degrees(math.acos(clamp((405 - cr) / 405, -1, 1)))
        p['lhip'], p['lkn'], p['rhip'], p['rkn'] = th, -2 * th, -th, 2 * th
    c.rotate(math.radians(p['lean']) * 0.3)
    # legs
    lh, rh = (hip[0] + 38, hip[1]), (hip[0] - 38, hip[1])
    lk = polar(lh, p['lhip'], 205 * p['thigh']); la = polar(lk, p['lhip'] + p['lkn'], 200)
    rk = polar(rh, p['rhip'], 205 * p['thigh']); ra = polar(rk, p['rhip'] + p['rkn'], 200)
    for h_, k_, a_ in ((rh, rk, ra), (lh, lk, la)):
        limb(c, h_, k_, 36, 29, legc, legsh); limb(c, k_, a_, 29, 22, legc, legsh)
        # shoe
        ellipse(c, a_[0] + (8 if a_ is la else -8), a_[1] + 14, 44, 24); fill_stroke(c, P['shoe'])
    # torso
    sh_y = hip[1] - 300
    c.new_path()
    smooth(c, [(-92, sh_y + 10), (-60, sh_y - 8), (60, sh_y - 8), (92, sh_y + 10), (84, sh_y + 160), (96, hip[1] + 20),
               (0, hip[1] + 40), (-96, hip[1] + 20), (-84, sh_y + 160)])
    setc(c, topc); c.fill_preserve(); c.save(); c.clip()
    c.rectangle(10, sh_y - 30, 120, 400); setc(c, topsh); c.fill()
    c.restore(); c.set_line_width(5); setc(c, INK); c.stroke()
    if out != 'pj':  # collar + hem line
        c.move_to(-40, sh_y - 4); c.curve_to(-20, sh_y + 40, 20, sh_y + 40, 40, sh_y - 4); c.set_line_width(4); setc(c, INK); c.stroke()
        c.move_to(-90, hip[1] + 4); c.curve_to(-30, hip[1] + 26, 30, hip[1] + 26, 90, hip[1] + 4); c.stroke()
    # arms
    ls, rs = (78, sh_y + 22), (-78, sh_y + 22)
    le = polar(ls, p['lsh'], 145); lw_ = polar(le, p['lsh'] + p['lel'], 135)
    re = polar(rs, p['rsh'], 145); rw_ = polar(re, p['rsh'] + p['rel'], 135)
    hands = []
    for s_, e_, w_ in ((rs, re, rw_), (ls, le, lw_)):
        limb(c, s_, e_, 31, 27, topc, topsh); limb(c, e_, w_, 23, 19, P['skin'], P['skin_sh'])
        hands.append(w_)
    for w_ in hands:
        ellipse(c, w_[0], w_[1] + 6, 24, 26); fill_stroke(c, P['skin'])
    p['_hands'] = {'r': hands[0], 'l': hands[1]}
    # neck + head
    c.save(); c.translate(0, sh_y - 10); c.rotate(math.radians(p['tilt']))
    limb(c, (0, 10), (0, -40), 26, 24, P['skin'], P['skin_sh'])
    head(c, 0, -150, p)
    c.restore()
    c.restore()
    # world-space hand positions (for props)
    sx = s
    def world(pt):
        a = math.radians(p['lean']) * 0.3
        X = pt[0] * math.cos(a) - pt[1] * math.sin(a); Y = pt[0] * math.sin(a) + pt[1] * math.cos(a)
        return (x + X * sx, y + Y * sx)
    return {'r': world(hands[0]), 'l': world(hands[1]), 'head': world((0, sh_y - 160))}


def head(c, x, y, p):
    c.save(); c.translate(x, y)
    wind = p['hair_wind']
    # back hair
    c.new_path(); smooth(c, [(-118, -20), (-128, 70), (-112, 140), (-60, 150), (60, 150), (112 + wind * 30, 140), (128 + wind * 40, 70), (118, -20), (0, -150)])
    setc(c, P['hair_sh']); c.fill_preserve(); c.set_line_width(5); setc(c, INK); c.stroke()
    # face
    c.new_path(); smooth(c, [(-96, -40), (-94, 40), (-60, 110), (0, 142), (60, 110), (94, 40), (96, -40), (60, -110), (-60, -110)])
    setc(c, P['skin']); c.fill_preserve(); c.save(); c.clip()
    ellipse(c, 90, 40, 50, 110); setc(c, P['skin_sh']); c.fill(); c.restore()
    c.set_line_width(5); setc(c, INK); c.stroke()
    # ears
    for sx in (-1, 1):
        ellipse(c, sx * 98, 20, 14, 24); fill_stroke(c, P['skin'], 4)
    # blush
    if p['blush'] > 0:
        for sx in (-1, 1):
            ellipse(c, sx * 56, 62, 26, 11); setc(c, (*P['blush'][:3], P['blush'][3] * p['blush'])); c.fill()
            c.set_line_width(2.5); setc(c, hx('D86A6A', .7 * p['blush']))
            for k in range(3): c.move_to(sx * 56 - 14 + k * 11, 68); c.line_to(sx * 56 - 8 + k * 11, 56); c.stroke()
    # eyes
    lx, ly = p['look']; op = clamp(p['eyes'] * (1 - p['blink']))
    for sx in (-1, 1):
        ex, ey = sx * 44, 18
        if op < 0.15:  # closed: curve
            c.new_path(); c.move_to(ex - 26, ey + 4); c.curve_to(ex - 10, ey + 16, ex + 10, ey + 16, ex + 26, ey + 4)
            c.set_line_width(6); setc(c, INK); c.stroke()
            continue
        hgt = 36 * op
        c.new_path(); ellipse(c, ex, ey, 26, hgt); setc(c, P['white']); c.fill_preserve(); c.save(); c.clip()
        ellipse(c, ex + lx * 8, ey + ly * 6 + 4, 20, 30); grad = cairo.LinearGradient(0, ey - 30, 0, ey + 30)
        grad.add_color_stop_rgba(0, *P['eye'][:3], 1); grad.add_color_stop_rgba(1, *P['eye2'][:3], 1); c.set_source(grad); c.fill()
        ellipse(c, ex + lx * 8, ey + ly * 6 + 6, 10, 15); setc(c, hx('24130F')); c.fill()
        ellipse(c, ex + lx * 8 - 8, ey + ly * 6 - 8, 8, 10); setc(c, P['white']); c.fill()
        ellipse(c, ex + lx * 8 + 9, ey + ly * 6 + 16, 4, 4); setc(c, P['white']); c.fill()
        c.restore()
        # upper lid
        c.new_path(); c.move_to(ex - 30, ey - hgt * .55); c.curve_to(ex - 12, ey - hgt * 1.15, ex + 14, ey - hgt * 1.15, ex + 31, ey - hgt * .45)
        c.set_line_width(8); setc(c, INK); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        # lashes
        c.move_to(ex + sx * 26, ey - hgt * .6); c.line_to(ex + sx * 38, ey - hgt * .9); c.set_line_width(5); c.stroke()
    # brows
    b = p['brow']
    for sx in (-1, 1):
        c.new_path(); c.move_to(sx * 22, -36 - b * 10 * (1 if sx < 0 else 1)); c.curve_to(sx * 40, -46 - b * 6, sx * 56, -46, sx * 70, -38 + b * 8)
        c.set_line_width(5); setc(c, P['hair_sh']); c.stroke()
    # nose
    c.move_to(4, 58); c.line_to(-2, 66); c.set_line_width(3.5); setc(c, hx('B0705A')); c.stroke()
    # mouth
    m = p['mouth']; setc(c, INK); c.set_line_width(4.5)
    if m == 'smile':
        c.move_to(-18, 92); c.curve_to(-8, 102, 8, 102, 18, 92); c.stroke()
    elif m == 'open':
        c.new_path(); smooth(c, [(-20, 90), (0, 88), (20, 90), (12, 112), (-12, 112)]); fill_stroke(c, hx('B2414A'), 4)
        c.new_path(); ellipse(c, 0, 106, 9, 5); setc(c, hx('F08A8A')); c.fill()
    elif m == 'big':
        c.new_path(); smooth(c, [(-28, 86), (28, 86), (18, 122), (0, 128), (-18, 122)]); fill_stroke(c, hx('B2414A'), 4)
        c.new_path(); c.rectangle(-22, 86, 44, 8); setc(c, P['white']); c.fill()
    elif m == 'flat':
        c.move_to(-14, 98); c.line_to(14, 98); c.stroke()
    elif m == 'frown':
        c.move_to(-16, 102); c.curve_to(-6, 94, 6, 94, 16, 102); c.stroke()
    elif m == 'yawn':
        c.new_path(); ellipse(c, 0, 104, 15, 20); fill_stroke(c, hx('7A2630'), 4)
    elif m == 'o':
        c.new_path(); ellipse(c, 0, 102, 9, 11); fill_stroke(c, hx('7A2630'), 4)
    # bangs + side hair
    c.new_path()
    smooth(c, [(-112, -10), (-104, -90), (-40, -140), (40, -140), (104, -90), (112 + wind * 20, -10), (96, -20), (82, -60), (62, -28),
               (40, -70), (16, -30), (-8, -74), (-30, -30), (-56, -66), (-78, -24), (-96, -40)])
    setc(c, P['hair']); c.fill_preserve(); c.save(); c.clip()
    c.new_path(); smooth(c, [(-70, -118), (-20, -132), (30, -128), (10, -110), (-50, -104)]); setc(c, P['hair_hi']); c.fill()
    c.restore(); c.set_line_width(5); setc(c, INK); c.stroke()
    for sx in (-1, 1):
        c.new_path(); smooth(c, [(sx * 96, -40), (sx * 120, 40), (sx * 116, 128), (sx * 98, 118), (sx * 92, 30)])
        setc(c, P['hair']); c.fill_preserve(); c.set_line_width(5); setc(c, INK); c.stroke()
    # hair clip
    c.new_path(); rrect(c, 52, -96, 34, 12, 6); fill_stroke(c, hx('FF6B6B'), 3)
    # sweat
    if p['sweat'] > 0:
        c.new_path(); c.move_to(108, -60); c.curve_to(128, -30, 128, -10, 112, -6); c.curve_to(96, -10, 96, -30, 108, -60)
        fill_stroke(c, hx('BFE6FF', p['sweat']), 3)
    c.restore()


# ---------------------------------------------------------------- props
def phone(c, x, y, s=1.0, glow=0.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(math.radians(ang)); c.scale(s, s)
    if glow > 0:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 260); g.add_color_stop_rgba(0, .55, .8, 1, .55 * glow); g.add_color_stop_rgba(1, .55, .8, 1, 0)
        c.set_source(g); c.arc(0, 0, 260, 0, 2 * math.pi); c.fill()
    rrect(c, -34, -62, 68, 124, 12); fill_stroke(c, hx('2A2D3A'), 4)
    rrect(c, -27, -52, 54, 100, 6); setc(c, hx('7EC8FF') if glow > 0 else hx('3A4256')); c.fill()
    c.restore()


def alarm_clock(c, x, y, s=1.0, ring=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if ring > 0: c.rotate(math.sin(t * 50) * 0.12 * ring)
    for sx in (-1, 1):
        ellipse(c, sx * 46, -66, 26, 20); fill_stroke(c, hx('F2C14E'), 4)
    for sx in (-1, 1):
        c.move_to(sx * 40, 60); c.line_to(sx * 58, 86); c.set_line_width(8); setc(c, INK); c.stroke()
    ellipse(c, 0, 0, 78, 78); fill_stroke(c, hx('E8524A'), 5)
    ellipse(c, 0, 0, 62, 62); fill_stroke(c, hx('FFF8E6'), 3)
    c.move_to(0, 0); c.line_to(0, -40); c.set_line_width(6); setc(c, INK); c.stroke()
    c.move_to(0, 0); c.line_to(28, 10); c.stroke()
    c.restore()
    if ring > 0:  # ring marks
        c.save(); c.set_line_width(6); setc(c, INK)
        for sx in (-1, 1):
            for k in range(3):
                a = math.radians(-60 + k * 30); r0, r1 = 110 * s, 140 * s
                c.move_to(x + sx * math.cos(a) * r0, y + math.sin(a) * r0); c.line_to(x + sx * math.cos(a) * r1, y + math.sin(a) * r1); c.stroke()
        c.restore()


def big_clock(c, x, y, r, h_from=8, h_to=None, prog=0.0, night=0.0, label=True):
    """Kitchen wall clock with an arc showing an eating window from h_from for 12 h * prog."""
    c.save(); c.translate(x, y)
    ellipse(c, 6, 10, r * 1.08, r * 1.08); setc(c, (0, 0, 0, .18)); c.fill()
    ellipse(c, 0, 0, r * 1.08, r * 1.08); fill_stroke(c, hx('7C4A2D'), 6)
    ellipse(c, 0, 0, r, r); fill_stroke(c, hx('FFF6E2'), 4)
    if prog > 0:
        a0 = (h_from % 12) / 12 * 2 * math.pi - math.pi / 2
        c.move_to(0, 0); c.arc(0, 0, r * .92, a0, a0 + prog * 2 * math.pi * 0.999); c.close_path()
        setc(c, hx('7ED957', .55)); c.fill()
    for k in range(12):
        a = k / 12 * 2 * math.pi
        c.move_to(math.sin(a) * r * .8, -math.cos(a) * r * .8); c.line_to(math.sin(a) * r * .92, -math.cos(a) * r * .92)
        c.set_line_width(6 if k % 3 == 0 else 3); setc(c, INK); c.stroke()
    hrs = h_from + 12 * prog
    ah = (hrs % 12) / 12 * 2 * math.pi; am = (hrs % 1) * 2 * math.pi
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(0, 0); c.line_to(math.sin(ah) * r * .5, -math.cos(ah) * r * .5); c.set_line_width(12); setc(c, INK); c.stroke()
    c.move_to(0, 0); c.line_to(math.sin(am) * r * .75, -math.cos(am) * r * .75); c.set_line_width(7); c.stroke()
    ellipse(c, 0, 0, 10, 10); setc(c, hx('E8524A')); c.fill()
    c.restore()


def bowl(c, x, y, s=1.0, steam=0.0, t=0.0, col='FFFFFF', food='noodle'):
    c.save(); c.translate(x, y); c.scale(s, s)
    if steam > 0:
        c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(3):
            xo = -30 + k * 30; ph = t * 3 + k
            c.move_to(xo, -40)
            for j in range(1, 6): c.line_to(xo + math.sin(ph + j) * 10, -40 - j * 22)
            setc(c, (1, 1, 1, .6 * steam)); c.stroke()
    c.move_to(-80, -20); c.curve_to(-70, 60, 70, 60, 80, -20); c.close_path(); fill_stroke(c, hx(col))
    ellipse(c, 0, -20, 80, 16); fill_stroke(c, hx('F4D27A') if food == 'noodle' else hx('E46A4A'), 4)
    if food == 'noodle':
        c.set_line_width(3); setc(c, hx('C99B3A'))
        for k in range(6): c.move_to(-60 + k * 22, -26); c.curve_to(-50 + k * 22, -12, -40 + k * 22, -30, -30 + k * 22, -16); c.stroke()
    c.restore()


def plant(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k, (a, L) in enumerate(((-35, 120), (-10, 160), (15, 140), (40, 110), (-60, 90))):
        sw = math.sin(t * 1.5 + k) * 3
        c.save(); c.rotate(math.radians(a + sw))
        c.new_path(); smooth(c, [(0, 0), (-22, -L * .5), (0, -L), (22, -L * .5)]); fill_stroke(c, hx('5DBB63'), 4)
        c.move_to(0, 0); c.line_to(0, -L * .9); c.set_line_width(2.5); setc(c, hx('2E7D32')); c.stroke()
        c.restore()
    c.move_to(-60, 0); c.line_to(60, 0); c.line_to(46, 90); c.line_to(-46, 90); c.close_path(); fill_stroke(c, hx('D9774A'))
    c.rectangle(-66, -6, 132, 22); fill_stroke(c, hx('E88A5A'), 4)
    c.restore()


def mug(c, x, y, s=1.0, t=0.0, steam=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if steam:
        c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(2):
            c.move_to(-10 + k * 20, -50)
            for j in range(1, 5): c.line_to(-10 + k * 20 + math.sin(t * 3 + j + k) * 7, -50 - j * 16)
            setc(c, (1, 1, 1, .7 * steam)); c.stroke()
    c.arc(42, 2, 20, -math.pi / 2, math.pi / 2); c.set_line_width(9); setc(c, INK); c.stroke()
    c.arc(42, 2, 20, -math.pi / 2, math.pi / 2); c.set_line_width(4); setc(c, hx('F6E7C1')); c.stroke()
    rrect(c, -40, -44, 80, 90, 14); fill_stroke(c, hx('F6E7C1'))
    ellipse(c, 0, -42, 38, 8); fill_stroke(c, hx('B8743A'), 3)
    c.restore()


# ---------------------------------------------------------------- backgrounds
def sky(c, top, mid, bot, y0=0, y1=H):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, *hx(top)); g.add_color_stop_rgba(.55, *hx(mid)); g.add_color_stop_rgba(1, *hx(bot))
    c.set_source(g); c.rectangle(0, y0, W, y1 - y0); c.fill()


def cloud(c, x, y, s=1.0, col='FFFFFF', sh='E6D3F0', alpha=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    puffs = [(-150, 20, 80), (-70, -30, 105), (40, -50, 120), (150, -10, 95), (220, 30, 70), (60, 30, 110), (-60, 40, 90)]
    for (px, py, r) in puffs: ellipse(c, px, py, r, r * .85)
    setc(c, hx(sh, alpha)); c.fill()
    for (px, py, r) in puffs: ellipse(c, px - 10, py - 16, r * .9, r * .75)
    setc(c, hx(col, alpha)); c.fill()
    c.restore()


def sun(c, x, y, r, t=0.0, col='FFE08A'):
    g = cairo.RadialGradient(x, y, r * .5, x, y, r * 4); g.add_color_stop_rgba(0, *hx(col, .7)); g.add_color_stop_rgba(1, *hx(col, 0))
    c.set_source(g); c.arc(x, y, r * 4, 0, 2 * math.pi); c.fill()
    ellipse(c, x, y, r, r); setc(c, hx('FFF4C4')); c.fill()


def sunburst(c, cx, cy, n, c1, c2, rot=0.0):
    setc(c, hx(c1)); c.paint()
    setc(c, hx(c2))
    for i in range(n):
        a = rot + i * 2 * math.pi / n
        c.move_to(cx, cy); c.arc(cx, cy, 3000, a, a + math.pi / n); c.close_path(); c.fill()


def speedlines(c, cx, cy, t, col=(1, 1, 1, .5), n=60, r0=380):
    rnd = random.Random(int(t * 12))
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        a = rnd.random() * 2 * math.pi; r = r0 + rnd.random() * 200; L = 300 + rnd.random() * 900
        c.move_to(cx + math.cos(a) * r, cy + math.sin(a) * r); c.line_to(cx + math.cos(a) * (r + L), cy + math.sin(a) * (r + L))
        c.set_line_width(2 + rnd.random() * 7); setc(c, col); c.stroke()


def sparkle(c, x, y, r, col='FFFFFF', a=1.0):
    c.save(); c.translate(x, y); c.new_path()
    for k in range(4):
        ang = k * math.pi / 2
        c.line_to(math.cos(ang) * r, math.sin(ang) * r); c.line_to(math.cos(ang + math.pi / 4) * r * .22, math.sin(ang + math.pi / 4) * r * .22)
    c.close_path(); setc(c, hx(col, a)); c.fill(); c.restore()


def window_frame(c, x, y, w, h, inner_cb=None):
    c.save(); rrect(c, x, y, w, h, 10); c.clip()
    if inner_cb: inner_cb()
    c.restore()
    rrect(c, x, y, w, h, 10); c.set_line_width(22); setc(c, hx('F3E3C7')); c.stroke_preserve(); c.set_line_width(5); setc(c, INK); c.stroke()
    c.move_to(x + w / 2, y); c.line_to(x + w / 2, y + h); c.move_to(x, y + h / 2); c.line_to(x + w, y + h / 2)
    c.set_line_width(14); setc(c, hx('F3E3C7')); c.stroke()


def room(c, wall='F7D9B5', wall2='EBC39A', floor='C98B5A', floor2='B57745', horizon=760):
    setc(c, hx(wall)); c.rectangle(0, 0, W, horizon); c.fill()
    for i in range(0, W, 120):  # wallpaper stripes
        c.rectangle(i, 0, 40, horizon); setc(c, hx(wall2, .35)); c.fill()
    setc(c, hx(floor)); c.rectangle(0, horizon, W, H - horizon); c.fill()
    for i in range(-10, 30):
        c.move_to(i * 140, horizon); c.line_to(i * 140 - 500, H); c.set_line_width(4); setc(c, hx(floor2)); c.stroke()
    c.rectangle(0, horizon - 18, W, 22); setc(c, hx('8A5A3A')); c.fill()


def city(c, t, night=0.0, y0=640):
    rnd = random.Random(4)
    x = -40
    while x < W + 100:
        w = rnd.randint(110, 220); h = rnd.randint(160, 420)
        col = hx('6F6AA8') if night < .5 else hx('2D2B57')
        c.rectangle(x, y0 - h, w, h + 500); setc(c, col); c.fill_preserve(); c.set_line_width(4); setc(c, INK); c.stroke()
        for wy in range(int(y0 - h + 20), y0 + 200, 44):
            for wx in range(x + 16, x + w - 24, 34):
                lit = rnd.random() < (0.25 + night * .5)
                c.rectangle(wx, wy, 18, 24); setc(c, hx('FFE08A') if lit else hx('9B97CC', .7)); c.fill()
        x += w + rnd.randint(-10, 20)


def tree(c, x, y, s=1.0, t=0.0, col='4FA65A', sh='2F7A44'):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-22, 0); c.line_to(-14, -200); c.line_to(14, -200); c.line_to(22, 0); c.close_path(); fill_stroke(c, hx('8A5A3A'))
    sw = math.sin(t * 1.2) * 6
    for (px, py, r, cl) in ((-90, -230, 110, sh), (90, -240, 110, sh), (0, -330, 140, sh), (-70, -260, 100, col), (70, -270, 100, col), (sw, -350, 120, col)):
        ellipse(c, px + sw * .5, py, r, r * .85); setc(c, hx(cl)); c.fill_preserve(); c.set_line_width(5); setc(c, INK); c.stroke()
    c.restore()


# ---------------------------------------------------------------- text (PIL, shaped Hindi)
@functools.lru_cache(maxsize=256)
def text_img(txt, size, fill='FFFFFF', stroke='2B1D30', sw=10, font=FONT, shadow=True):
    f = ImageFont.truetype(font, size, layout_engine=ImageFont.Layout.RAQM)
    bb = f.getbbox(txt, stroke_width=sw)
    w, h = bb[2] - bb[0] + 40, bb[3] - bb[1] + 40
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow:
        d.text((20 - bb[0] + 8, 20 - bb[1] + 10), txt, font=f, fill=(20, 10, 30, 150), stroke_width=sw, stroke_fill=(20, 10, 30, 150))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill='#' + fill, stroke_width=sw, stroke_fill='#' + stroke)
    return np.array(im)


def put_rgba(frame, rgba, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    """Composite an RGBA numpy image centred at (cx, cy) on an RGB uint8 frame."""
    if alpha <= 0 or scale <= 0.01: return
    im = rgba
    if scale != 1.0 or rot:
        h, w = im.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
        nw, nh = int(w * scale * 1.2 + 4), int(h * scale * 1.5 + 4)
        M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
        im = cv2.warpAffine(im, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    h, w = im.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return
    sub = im[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32)
    a = sub[..., 3:4] / 255 * alpha
    frame[ya:yb, xa:xb] = (frame[ya:yb, xa:xb] * (1 - a) + sub[..., :3] * a).astype(np.uint8)


def caption(frame, txt, cx=W // 2, cy=900, size=84, t=0.0, fill='FFFFFF', stroke='2B1D30', pop=True, alpha=1.0, font=FONT, rot=0.0):
    sc = back(t / 0.28) if pop else 1.0
    put_rgba(frame, text_img(txt, size, fill, stroke, max(6, size // 9), font), cx, cy, sc, alpha * clamp(t / 0.12), rot)


# ---------------------------------------------------------------- frame helpers + grade
def new_surface():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
    return s, c


def surf_to_rgb(s):
    buf = np.ndarray((H, W, 4), np.uint8, s.get_data())
    return buf[..., 2::-1].copy()  # BGRA -> RGB


_GRAIN = None
def grade(img, fi, warm=1.0, vign=0.35, grain=1.0, bloom=0.25):
    """Retro anime film/VHS finish: bloom, warm cel colour, slight chroma offset, grain, scanlines, vignette."""
    global _GRAIN
    f = img.astype(np.float32) / 255
    if bloom > 0:
        small = cv2.resize(f, (W // 8, H // 8), interpolation=cv2.INTER_AREA)
        hi = np.clip(small - 0.62, 0, 1) * 2.2
        hi = cv2.GaussianBlur(hi, (0, 0), 6)
        f = f + cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR) * bloom
    # warm, slightly lifted blacks (old cel/film)
    f = f * np.array([1.0 + .03 * warm, 1.0, 1.0 - .05 * warm], np.float32) + np.array([.035, .02, .045], np.float32)
    # chroma offset (red right, blue left) by 2px
    f[..., 0] = np.roll(f[..., 0], 2, axis=1); f[..., 2] = np.roll(f[..., 2], -2, axis=1)
    if _GRAIN is None:
        rng = np.random.default_rng(3)
        _GRAIN = [cv2.resize(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (W, H)) for _ in range(6)]
        yy = np.arange(H, dtype=np.float32)
        globals()['_SCAN'] = (1 - 0.035 * (np.sin(yy * math.pi / 2) ** 2))[:, None, None]
        X, Y = np.meshgrid(np.linspace(-1, 1, W, dtype=np.float32), np.linspace(-1, 1, H, dtype=np.float32))
        globals()['_VIG'] = (1 - vign * np.clip((X ** 2 * .8 + Y ** 2) - .25, 0, 1.5))[..., None]
    f = f + _GRAIN[(fi // 2) % 6][..., None] * 0.022 * grain
    f = f * _SCAN * _VIG
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)
