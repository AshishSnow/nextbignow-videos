"""Props for 'What if you got stuck in space for a year?' (episode 39, Frank Rubio, Soyuz MS-22, 2022-23)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, thermometer
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from jupprops import astro, no_stamp
from caveprops import dumbbell

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); MINT = (120, 230, 170); ORANGE = (255, 140, 40)
PANEL = (60, 90, 170); PANEL_L = (110, 150, 230); HULL = (232, 234, 240)
SPACE = ((14, 18, 60), (40, 30, 90))


def iss(c, x, y, s, t, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-420, -10, 840, 20), paint((180, 184, 196))); c.drawRect(R.MakeXYWH(-420, -10, 840, 20), stroke(INK, 4))
    for sx in (-1, 1):
        for j in (-1, 1):
            px = sx * 300; py = j * 120
            c.drawRect(R.MakeXYWH(px - 90, py - 80, 180, 160) if j else R.MakeXYWH(0, 0, 0, 0), paint(PANEL))
            c.drawRect(R.MakeXYWH(px - 90, py - 80, 180, 160), stroke(INK, 4))
            for k in range(1, 4):
                c.drawLine(px - 90 + k * 45, py - 80, px - 90 + k * 45, py + 80, stroke(PANEL_L, 3))
            c.drawLine(px, py - 80 * j, px, 0, stroke((180, 184, 196), 8))
    for i, (w, h) in enumerate(((120, 70), (160, 80), (120, 70))):
        cx = -140 + i * 140
        c.drawRoundRect(R.MakeXYWH(cx - w / 2, -h / 2, w, h), 24, 24, paint(HULL)); c.drawRoundRect(R.MakeXYWH(cx - w / 2, -h / 2, w, h), 24, 24, stroke(INK, 5))
    c.restore()


def soyuz(c, x, y, s, t, rot=0.0, leak=0.0, hole=0.0):
    """capsule stack: orbital module (sphere), descent module (bell), service module with panels."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawCircle(0, -150, 60, paint((120, 160, 110))); c.drawCircle(0, -150, 60, stroke(INK, 5))
    bell = skia.Path(); bell.moveTo(-40, -95); bell.lineTo(40, -95); bell.lineTo(75, 10); bell.lineTo(-75, 10); bell.close()
    c.drawPath(bell, paint((140, 120, 90))); c.drawPath(bell, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(-70, 10, 140, 140), 14, 14, paint((200, 205, 215))); c.drawRoundRect(R.MakeXYWH(-70, 10, 140, 140), 14, 14, stroke(INK, 5))
    for sx in (-1, 1):
        c.drawRect(R.MakeXYWH(sx * 70 + (0 if sx > 0 else -190), 50, 190, 60), paint(PANEL)); c.drawRect(R.MakeXYWH(sx * 70 + (0 if sx > 0 else -190), 50, 190, 60), stroke(INK, 4))
    if hole > 0:
        c.drawCircle(40, 80, 10 * hole, paint(INK))
    if leak > 0:
        for i in range(26):
            ph = (t * 1.6 + hsh(i, 2)) % 1
            a = -0.4 + (hsh(i, 3) - 0.5) * 0.8
            d = 40 + ph * 300
            c.drawCircle(40 + math.cos(a) * d, 80 + math.sin(a) * d, 4 + 6 * ph, paint((210, 240, 255), leak * (1 - ph)))
    c.restore()


def rock(c, x, y, s, t, trail=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if trail > 0:
        c.drawPath(poly([(0, -14), (-260, -40), (-260, 40), (0, 14)], True), paint(shader=lin(0, 0, -260, 0, [argb((255, 200, 120), 0.8 * trail), argb((255, 200, 120), 0)])))
    c.drawCircle(0, 0, 18, paint((150, 130, 110))); c.drawCircle(0, 0, 18, stroke(INK, 4))
    c.restore()


def earth_orbit(c, cx, cy, r, t, k=1.0, laps=None):
    draw_planet(c, 'earth', cx, cy, r, rot=t * 0.05, glow=(120, 190, 255))
    rr = r * 1.35
    c.drawOval(R.MakeXYWH(cx - rr, cy - rr * 0.35, rr * 2, rr * 0.7), stroke((255, 255, 255), 4, 0.5))
    a = t * 2.4
    sx, sy = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.35
    c.drawCircle(sx, sy, 14, paint(YEL)); c.drawCircle(sx, sy, 14, stroke(INK, 3))


def sunrise_ticker(c, x, y, s, n, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(16):
        col_ = YEL if i < n else (80, 80, 120)
        xx = -360 + (i % 8) * 103; yy = -50 + (i // 8) * 110
        c.drawCircle(xx, yy, 34, paint(col_)); c.drawCircle(xx, yy, 34, stroke(INK, 4))
        if i < n:
            for j in range(8):
                a = j / 8 * 6.283
                c.drawLine(xx + math.cos(a) * 42, yy + math.sin(a) * 42, xx + math.cos(a) * 52, yy + math.sin(a) * 52, stroke(YEL, 5))
    c.restore()


def module_bg(c, t, tint=(230, 236, 245)):
    """inside the station: curved white walls, handrails, cables, a window with Earth."""
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(tint), argb((190, 200, 220))])))
    for i in range(7):
        c.drawLine(0, 300 + i * 230, W, 300 + i * 230, stroke((205, 212, 228), 6))
    for x in (100, 980):
        c.drawLine(x, 260, x, H, stroke((200, 208, 224), 30))
        for j in range(8):
            c.drawRoundRect(R.MakeXYWH(x - 26, 320 + j * 200, 52, 90), 10, 10, paint([(250, 200, 80), (120, 180, 240), (240, 120, 120)][j % 3], 0.8))
    for j in range(4):
        p = skia.Path(); p.moveTo(140, 900 + j * 40); p.cubicTo(400, 1000 + j * 30, 700, 860 + j * 20, 940, 960 + j * 40)
        c.drawPath(p, stroke([(240, 80, 80), (60, 120, 220), (250, 200, 60), (80, 180, 120)][j], 6, 0.6))


def sleep_bag(c, x, y, s, t, face=None):
    c.save(); c.translate(x, y + 6 * math.sin(t * 1.2)); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-90, -60, 180, 380), 80, 80, paint((60, 120, 220))); c.drawRoundRect(R.MakeXYWH(-90, -60, 180, 380), 80, 80, stroke(INK, 6))
    for yy in (40, 140, 240): c.drawLine(-90, yy, 90, yy, stroke((40, 90, 180), 6))
    for yy in (0, 300):
        c.drawRect(R.MakeXYWH(-120, yy - 8, 240, 16), paint((240, 200, 60))); c.drawRect(R.MakeXYWH(-120, yy - 8, 240, 16), stroke(INK, 3))
    c.drawCircle(0, -70, 56, paint((255, 255, 255))); c.drawCircle(0, -70, 56, stroke(INK, 6))
    c.save(); c.translate(0, -70); draw_face(c, face or Face('closed', 'smile'), 46, False, t); c.restore()
    c.restore()


def water_loop(c, x, y, s, t, k=1.0):
    """recycler: sweat/pee in -> machine -> clean water out into a pouch."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-160, -150, 320, 300), 30, 30, paint((210, 215, 228))); c.drawRoundRect(R.MakeXYWH(-160, -150, 320, 300), 30, 30, stroke(INK, 6))
    for i in range(3):
        a = t * 3 + i * 2.09
        c.drawCircle(math.cos(a) * 60, math.sin(a) * 60, 20, paint((80, 190, 250))); c.drawCircle(math.cos(a) * 60, math.sin(a) * 60, 20, stroke(INK, 3))
    c.drawCircle(0, 0, 100, stroke((150, 160, 180), 6))
    for sgn, col in ((-1, (240, 210, 80)), (1, (90, 200, 255))):
        for i in range(5):
            ph = (t * 1.2 + i / 5) % 1
            xx = sgn * (180 + 120 * (ph if sgn > 0 else 1 - ph))
            c.drawCircle(xx, 0, 12, paint(col, 0.9 * k))
    c.restore()


def pouch(c, x, y, s, label='COFFEE'):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-70, -110, 140, 220), 30, 30, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-70, -110, 140, 220), 30, 30, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(-60, -20, 120, 120), 24, 24, paint((120, 70, 40)))
    c.drawRect(R.MakeXYWH(-10, -150, 20, 44), paint((60, 60, 70)))
    f = font('ant', 30); c.drawString(label, -f.measureText(label) / 2, -50, f, paint(INK))
    c.restore()


def ruler(c, x, y, h, k=1.0, label=None):
    c.drawRoundRect(R.MakeXYWH(x - 26, y - h, 52, h), 8, 8, paint((255, 220, 90))); c.drawRoundRect(R.MakeXYWH(x - 26, y - h, 52, h), 8, 8, stroke(INK, 4))
    for i in range(int(h / 20)):
        c.drawLine(x - 26, y - i * 20, x - 26 + (22 if i % 5 == 0 else 12), y - i * 20, stroke(INK, 3))


def bone(c, x, y, s, frac=1.0, rot=0.0):
    """leg bone; frac = density (holes appear as it drops)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path()
    p.addRoundRect(R.MakeXYWH(-30, -160, 60, 320), 30, 30)
    for sy in (-1, 1):
        for sx in (-1, 1):
            p.addCircle(sx * 34, sy * 160, 40)
    c.drawPath(p, paint((250, 245, 230))); c.drawPath(p, stroke(INK, 6))
    for i in range(int((1 - frac) * 30)):
        c.drawCircle((hsh(i, 2) - 0.5) * 40, (hsh(i, 3) - 0.5) * 280, 5 + 5 * hsh(i, 4), paint((200, 180, 160)))
    c.restore()


def treadmill(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-260, -30, 520, 60), 20, 20, paint((60, 64, 76))); c.drawRoundRect(R.MakeXYWH(-260, -30, 520, 60), 20, 20, stroke(INK, 6))
    for i in range(10):
        xx = ((i * 60 - t * 300) % 520) - 260
        c.drawLine(xx, -28, xx, 28, stroke((100, 104, 116), 4))
    c.restore()


def bungee(c, x0, y0, x1, y1):
    c.drawLine(x0, y0, x1, y1, stroke((240, 90, 60), 8))
