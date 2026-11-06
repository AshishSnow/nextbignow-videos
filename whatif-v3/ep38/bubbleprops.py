"""Props for 'What if you were trapped at the bottom of the sea?' (episode 38, Harrison Okene, Jascon-4, May 2013)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, thermometer
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble, diver
from seaprops import ocean, wave_front
from trenchprops import deep_bg, depth_meter
from meteorprops import speech

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); MINT = (120, 230, 170); ORANGE = (255, 140, 40)
SEA_C = (30, 110, 190); SEA_DK = (8, 30, 70); AIR = (200, 235, 255)


def harrison(c, x, y, s, pose, face, t, flip=False, rot=0.0, a=1.0, prop=None):
    """Original cook character: blue shorts, no scarf, short beard stubble."""
    c.save(); c.translate(x, y); c.rotate(rot)
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip, a=a, prop=prop)
    P = rig_points(pose)
    c.save(); c.scale(-s if flip else s, s)
    hx, hy = P['hip']
    c.drawRoundRect(R.MakeXYWH(hx - 26, hy - 10, 52, 40), 10, 10, paint((60, 120, 230), a)); c.drawRoundRect(R.MakeXYWH(hx - 26, hy - 10, 52, 40), 10, 10, stroke(INK, 4, a))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 200, 140, False, stroke(INK, 10, a))
    c.restore()
    c.restore()
    c.restore()


def tug(c, x, y, s, t, rot=0.0, flipped=0.0, lights=True):
    """tugboat; rot in degrees (180 = upside down)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-260, -40); hull.lineTo(240, -40); hull.lineTo(200, 60); hull.lineTo(-230, 60); hull.close()
    c.drawPath(hull, paint((230, 70, 50))); c.drawPath(hull, stroke(INK, 7))
    c.drawRect(R.MakeXYWH(-260, -40, 500, 16), paint((255, 255, 255)))
    c.drawRect(R.MakeXYWH(-230, 40, 430, 20), paint((40, 40, 50)))
    cab = R.MakeXYWH(-90, -190, 210, 150)
    c.drawRoundRect(cab, 14, 14, paint((250, 250, 245))); c.drawRoundRect(cab, 14, 14, stroke(INK, 6))
    for i in range(3):
        c.drawRect(R.MakeXYWH(-70 + i * 64, -165, 44, 40), paint((255, 230, 140) if lights else (60, 80, 110))); c.drawRect(R.MakeXYWH(-70 + i * 64, -165, 44, 40), stroke(INK, 4))
    c.drawRect(R.MakeXYWH(-10, -270, 40, 80), paint((240, 200, 60))); c.drawRect(R.MakeXYWH(-10, -270, 40, 80), stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-10, -270, 40, 16), paint(INK))
    for i in range(4):
        c.drawCircle(-220 + i * 30, 10, 16, paint((60, 60, 70))); c.drawCircle(-220 + i * 30, 10, 16, stroke(INK, 3))
    c.restore()


def big_wave(c, t, k, x0=-200):
    """a giant curling wave sweeping in from the left; k 0..1."""
    xx = lerp(x0, 900, eo(k))
    p = skia.Path(); p.moveTo(-200, H); p.lineTo(-200, 700)
    p.cubicTo(xx - 300, 500, xx, 450, xx + 80, 620); p.cubicTo(xx + 40, 560, xx - 80, 600, xx - 60, 760)
    p.cubicTo(xx - 20, 900, xx + 80, 1000, xx + 160, H); p.close()
    c.drawPath(p, paint(shader=lin(0, 450, 0, H, [argb((60, 160, 230)), argb((20, 70, 150))]))); c.drawPath(p, stroke(INK, 6))
    for i in range(8):
        c.drawCircle(xx + 40 + 30 * math.cos(i + t * 4), 600 + 25 * math.sin(i * 1.7 + t * 5), 16 + 8 * hsh(i, 2), paint((255, 255, 255), 0.9))


def seafloor(c, y, t):
    p = skia.Path(); p.moveTo(-20, H + 20); p.lineTo(-20, y)
    for i in range(14):
        p.lineTo(i * 90, y + 20 * math.sin(i * 1.3))
    p.lineTo(W + 20, y); p.lineTo(W + 20, H + 20); p.close()
    c.drawPath(p, paint((150, 130, 90))); c.drawPath(p, stroke(INK, 5, 0.6))
    for i in range(6):
        sx = 80 + i * 180; h = 80 + 40 * hsh(i, 4)
        wd = skia.Path(); wd.moveTo(sx, y + 10)
        for j in range(6):
            wd.lineTo(sx + 14 * math.sin(t * 1.5 + j + i), y + 10 - h * j / 5)
        c.drawPath(wd, stroke((60, 160, 90), 9))


def pocket_room(c, t, water_y=1200, air_top=700, dark=0.0, flash=0.0, fx=540, fy=900):
    """inside the upside-down cabin: dark walls, air pocket on top, water below with ripples."""
    c.drawRect(R.MakeWH(W, H), paint((50, 44, 60)))
    for i in range(6):
        c.drawLine(i * 200 + 40, air_top - 300, i * 200 + 40, H, stroke((70, 62, 84), 10))
    c.drawRect(R.MakeLTRB(0, air_top - 400, W, air_top), paint((80, 70, 90)))
    c.drawLine(0, air_top, W, air_top, stroke(INK, 10))
    c.drawRect(R.MakeLTRB(0, air_top, W, water_y), paint(AIR, 0.08))
    wp = skia.Path(); wp.moveTo(-20, H + 20); wp.lineTo(-20, water_y)
    for i in range(0, W + 41, 30):
        wp.lineTo(i, water_y + 10 * math.sin(i * 0.02 + t * 2))
    wp.lineTo(W + 20, H + 20); wp.close()
    c.drawPath(wp, paint(shader=lin(0, water_y, 0, H, [argb((40, 110, 170), 0.92), argb((10, 30, 70), 0.98)])))
    c.drawPath(wp, stroke((140, 200, 255), 4, 0.7))
    if flash > 0:
        beam = poly([(fx, fy), (fx + 420, fy - 260), (fx + 420, fy + 200)], True)
        c.drawPath(beam, paint(shader=lin(fx, 0, fx + 420, 0, [argb((255, 245, 190), 0.5 * flash), argb((255, 245, 190), 0)])))
    if dark > 0:
        c.drawRect(R.MakeWH(W, H), paint((0, 0, 10), dark))


def mattress_raft(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-200, -30, 400, 60), 26, 26, paint((235, 225, 255))); c.drawRoundRect(R.MakeXYWH(-200, -30, 400, 60), 26, 26, stroke(INK, 6))
    for i in range(6): c.drawCircle(-150 + i * 60, 0, 6, paint((150, 130, 200)))
    c.restore()


def molecule(c, x, y, s, kind='co2', a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if kind == 'co2':
        for dx, col in ((-46, (240, 70, 60)), (46, (240, 70, 60)), (0, (60, 60, 70))):
            c.drawCircle(dx, 0, 30 if dx else 34, paint(col, a)); c.drawCircle(dx, 0, 30 if dx else 34, stroke(INK, 4, a))
    else:
        for dx in (-24, 24):
            c.drawCircle(dx, 0, 30, paint((70, 160, 250), a)); c.drawCircle(dx, 0, 30, stroke(INK, 4, a))
    c.restore()


def soda_bottle(c, x, y, s, rot=0.0):
    """plain unbranded cola bottle."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = skia.Path(); b.moveTo(-18, -160); b.lineTo(18, -160); b.lineTo(20, -110); b.cubicTo(50, -80, 50, -40, 40, 0); b.cubicTo(50, 40, 50, 90, 40, 110)
    b.lineTo(-40, 110); b.cubicTo(-50, 90, -50, 40, -40, 0); b.cubicTo(-50, -40, -50, -80, -20, -110); b.close()
    c.drawPath(b, paint((90, 40, 30))); c.drawPath(b, stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-42, -20, 84, 50), paint((235, 235, 240))); c.drawRect(R.MakeXYWH(-42, -20, 84, 50), stroke(INK, 3))
    f = font('ant', 30); c.drawString('COLA', -f.measureText('COLA') / 2, 16, f, paint(INK))
    c.drawRect(R.MakeXYWH(-20, -176, 40, 18), paint(RED)); c.drawRect(R.MakeXYWH(-20, -176, 40, 18), stroke(INK, 3))
    c.restore()


def life_vest(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-1, 1):
        p = skia.Path(); p.moveTo(sx * 20, -120); p.lineTo(sx * 90, -100); p.lineTo(sx * 100, 110); p.lineTo(sx * 20, 110); p.close()
        c.drawPath(p, paint(ORANGE)); c.drawPath(p, stroke(INK, 5))
    for yy in (-40, 40): c.drawLine(-100, yy, 100, yy, stroke((255, 255, 255), 10))
    c.restore()


def flashlight(c, x, y, s, rot=0.0, on=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if on > 0:
        beam = poly([(60, 0), (420, -140), (420, 140)], True)
        c.drawPath(beam, paint(shader=lin(60, 0, 420, 0, [argb((255, 245, 190), 0.5 * on), argb((255, 245, 190), 0)])))
    c.drawRoundRect(R.MakeXYWH(-60, -18, 100, 36), 10, 10, paint((60, 60, 70))); c.drawRoundRect(R.MakeXYWH(-60, -18, 100, 36), 10, 10, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(30, -28, 34, 56), 8, 8, paint((90, 90, 100))); c.drawRoundRect(R.MakeXYWH(30, -28, 34, 56), 8, 8, stroke(INK, 4))
    c.restore()


def chamber(c, x, y, s, t, inside=None):
    """decompression chamber: big white tube with round window and gauges."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-380, -170, 760, 340), 170, 170, paint((235, 238, 245))); c.drawRoundRect(R.MakeXYWH(-380, -170, 760, 340), 170, 170, stroke(INK, 8))
    for xx in (-250, 250): c.drawLine(xx, -165, xx, 165, stroke((180, 185, 200), 8))
    win = skia.Path(); win.addCircle(0, 0, 110)
    c.drawPath(win, paint((150, 210, 250)))
    if inside:
        c.save(); c.clipPath(win, doAntiAlias=True); inside(c); c.restore()
    c.drawCircle(0, 0, 110, stroke(INK, 12)); c.drawCircle(0, 0, 124, stroke((150, 155, 170), 8))
    c.drawCircle(-300, -60, 36, paint((255, 255, 255))); c.drawCircle(-300, -60, 36, stroke(INK, 5))
    a = math.radians(-120 + 60 * math.sin(t))
    c.drawLine(-300, -60, -300 + math.cos(a) * 26, -60 + math.sin(a) * 26, stroke(RED, 5))
    c.drawRect(R.MakeXYWH(-120, 170, 60, 40), paint((120, 125, 140))); c.drawRect(R.MakeXYWH(60, 170, 60, 40), paint((120, 125, 140)))
    c.restore()


def hand(c, x, y, s, rot=0.0, col=(255, 255, 255)):
    """open hand (palm, four fingers + thumb; no single pointing finger)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-40, -40, 80, 80), 24, 24, paint(col)); c.drawRoundRect(R.MakeXYWH(-40, -40, 80, 80), 24, 24, stroke(INK, 5))
    for i in range(4):
        r = R.MakeXYWH(-36 + i * 20, -90, 16, 56)
        c.drawRoundRect(r, 8, 8, paint(col)); c.drawRoundRect(r, 8, 8, stroke(INK, 4))
    th = R.MakeXYWH(34, -20, 46, 18); c.drawRoundRect(th, 9, 9, paint(col)); c.drawRoundRect(th, 9, 9, stroke(INK, 4))
    c.restore()
