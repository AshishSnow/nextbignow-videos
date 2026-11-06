"""Props for 'What if you were left alone on an island?' (episode 40, Alexander Selkirk, 1704-1709)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, tree
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from seaprops import ocean, wave_front, island
from dinoprops import palm
from niagaraprops import cat
from meteorprops import speech
from jupprops import no_stamp

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); MINT = (120, 230, 170); ORANGE = (255, 140, 40)
SAND = (245, 220, 160); GRASS = (90, 180, 90); GOAT = (235, 225, 205); SKIN = (190, 150, 100)


def selkirk(c, x, y, s, pose, face, t, flip=False, goat=0.0, beard=0.0, rot=0.0):
    """Original 1700s sailor: blue bandana, striped shirt; goat = goat-skin outfit amount; beard grows."""
    c.save(); c.translate(x, y); c.rotate(rot)
    P = rig_points(pose)
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip)
    c.save(); c.scale(-s if flip else s, s)
    nx, ny = P['neck']; hx, hy = P['hip']
    if goat > 0:
        body = skia.Path(); body.moveTo(nx - 26, ny + 2); body.lineTo(nx + 26, ny + 2); body.lineTo(hx + 34, hy + 26); body.lineTo(hx - 34, hy + 26); body.close()
        c.drawPath(body, paint(SKIN, goat)); c.drawPath(body, stroke(INK, 4, goat))
        for i in range(8):
            c.drawLine(hx - 30 + i * 8, hy + 20, hx - 32 + i * 8, hy + 34, stroke((150, 110, 70), 4, goat))
    else:
        c.drawLine(nx, ny + 6, hx, hy - 6, stroke((250, 250, 255), 20))
        for i in range(4):
            yy = ny + 14 + i * 16
            c.drawLine(nx - 9, yy, nx + 9, yy, stroke((60, 100, 200), 5))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    if goat > 0.5:
        hat = skia.Path(); hat.moveTo(-hr * 1.05, -hr * 0.45); hat.quadTo(0, -hr * 1.9, hr * 1.05, -hr * 0.45); hat.close()
        c.drawPath(hat, paint(SKIN)); c.drawPath(hat, stroke(INK, 4))
    else:
        band = skia.Path(); band.moveTo(-hr * 1.02, -hr * 0.3); band.quadTo(0, -hr * 1.6, hr * 1.02, -hr * 0.3); band.close()
        c.drawPath(band, paint((50, 90, 200))); c.drawPath(band, stroke(INK, 4))
        c.drawCircle(-hr * 1.05, -hr * 0.2, 9, paint((50, 90, 200)))
    if beard > 0:
        bd = skia.Path(); bd.moveTo(-hr * 0.8, hr * 0.15); bd.quadTo(-hr * 0.4, hr * (0.8 + 0.8 * beard), 0, hr * (0.9 + 0.9 * beard)); bd.quadTo(hr * 0.4, hr * (0.8 + 0.8 * beard), hr * 0.8, hr * 0.15)
        bd.quadTo(hr * 0.3, hr * 0.55, 0, hr * 0.55); bd.quadTo(-hr * 0.3, hr * 0.55, -hr * 0.8, hr * 0.15); bd.close()
        c.drawPath(bd, paint((110, 70, 40))); c.drawPath(bd, stroke(INK, 3))
    c.restore()
    c.restore()
    c.restore()


def tall_ship(c, x, y, s, t, rot=0.0, flag=(200, 40, 40), damaged=0.0, sink=0.0):
    c.save(); c.translate(x, y + 6 * math.sin(t * 1.6) + 200 * sink); c.rotate(rot + 2.5 * math.sin(t * 1.2) + 25 * sink); c.scale(s, s)
    hull = skia.Path(); hull.moveTo(-260, -40); hull.lineTo(260, -60); hull.lineTo(200, 60); hull.lineTo(-220, 60); hull.close()
    c.drawPath(hull, paint((130, 80, 40))); c.drawPath(hull, stroke(INK, 7))
    for i in range(5): c.drawCircle(-150 + i * 70, 0, 12, paint((60, 40, 20)))
    for mx, h in ((-90, 380), (60, 440), (190, 320)):
        c.drawLine(mx, -50, mx, -50 - h, stroke((90, 60, 30), 12))
        for j in range(2):
            sy = -50 - h + 60 + j * (h * 0.42)
            sail = skia.Path(); sail.moveTo(mx - 90, sy); sail.quadTo(mx, sy + 40 + 10 * math.sin(t * 2 + mx), mx + 90, sy)
            sail.lineTo(mx + 80, sy + h * 0.34); sail.quadTo(mx, sy + h * 0.34 + 30, mx - 80, sy + h * 0.34); sail.close()
            c.drawPath(sail, paint((250, 245, 230))); c.drawPath(sail, stroke(INK, 5))
            if damaged > 0:
                c.drawCircle(mx - 30 + 40 * j, sy + 60, 18 * damaged, paint(INK))
    c.drawPath(poly([(60, -490), (150, -470), (60, -450)], True), paint(flag)); c.drawPath(poly([(60, -490), (150, -470), (60, -450)], True), stroke(INK, 3))
    if damaged > 0:
        for i in range(3):
            c.drawLine(-200 + i * 140, -30, -170 + i * 140, 30, stroke(INK, 5, damaged))
    c.restore()


def beach(c, t, sea_y=1350, sky=((120, 200, 255), (230, 245, 255))):
    ocean(c, t, hy=1000, sky=sky, sun=False)
    c.drawRect(R.MakeLTRB(0, sea_y, W, H), paint(SAND))
    wv = skia.Path(); wv.moveTo(0, sea_y)
    for i in range(0, W + 41, 40): wv.lineTo(i, sea_y + 10 * math.sin(i * 0.02 + t * 2))
    c.drawPath(wv, stroke((255, 255, 255), 10))
    palm(c, 120, sea_y + 20, 1.2, t, seed=1)
    palm(c, 960, sea_y + 40, 1.0, t, seed=3)


def jungle(c, t):
    set_bg(c, (90, 190, 120), (170, 230, 150), spot=False, t=t)
    for i in range(7):
        tree(c, -40 + i * 190, 1250 + 30 * (i % 2), 1.4, seed=i + 4, col=(50, 150, 80))
    c.drawRect(R.MakeLTRB(0, 1450, W, H), paint((120, 170, 80)))
    c.drawLine(0, 1450, W, 1450, stroke(INK, 6, 0.5))


def sea_lion(c, x, y, s, t, roar=0.0, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    body = skia.Path(); body.moveTo(-120, 0); body.quadTo(-60, -70, 40, -60); body.quadTo(80, -150, 110, -150); body.quadTo(140, -140, 130, -100)
    body.quadTo(110, -50, 120, 0); body.close()
    c.drawPath(body, paint((120, 100, 90))); c.drawPath(body, stroke(INK, 5))
    c.drawPath(poly([(-120, 0), (-170, -30), (-160, 10)], True), paint((100, 84, 76))); c.drawPath(poly([(-120, 0), (-170, -30), (-160, 10)], True), stroke(INK, 4))
    c.drawCircle(118, -125, 6, paint(INK))
    if roar > 0:
        c.drawOval(R.MakeXYWH(124, -112, 22, 14 + 10 * roar), paint(INK))
        for i in range(3):
            c.drawArc(R.MakeXYWH(140 + i * 22, -150 - i * 10, 40 + i * 20, 60 + i * 20), -40, 80, False, stroke((255, 255, 255), 5, roar))
    c.restore()


def goat(c, x, y, s, t, run=0.0, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    ph = t * 10 * run
    for i, lx in enumerate((-60, -30, 40, 70)):
        sw = 18 * math.sin(ph + i * 1.6) * run
        c.drawLine(lx, -60, lx + sw, 0, stroke(INK, 14)); c.drawLine(lx, -60, lx + sw, 0, stroke(GOAT, 8))
    c.drawOval(R.MakeXYWH(-90, -130, 190, 90), paint(GOAT)); c.drawOval(R.MakeXYWH(-90, -130, 190, 90), stroke(INK, 5))
    c.drawOval(R.MakeXYWH(80, -180, 70, 60), paint(GOAT)); c.drawOval(R.MakeXYWH(80, -180, 70, 60), stroke(INK, 5))
    for hx in (92, 110):
        h = skia.Path(); h.moveTo(hx, -175); h.quadTo(hx - 30, -230, hx - 50, -200); c.drawPath(h, stroke((120, 100, 80), 8))
    c.drawCircle(128, -160, 5, paint(INK))
    c.drawPath(poly([(120, -125), (130, -95), (140, -125)], True), paint((200, 190, 170)))
    c.restore()


def rat(c, x, y, s, t, flip=False):
    c.save(); c.translate(x + 6 * math.sin(t * 12), y); c.scale(-s if flip else s, s)
    tail = skia.Path(); tail.moveTo(-40, -10); tail.cubicTo(-90, 0, -110, -40, -140, -20 + 8 * math.sin(t * 8))
    c.drawPath(tail, stroke((230, 150, 150), 5))
    c.drawOval(R.MakeXYWH(-50, -40, 100, 45), paint((120, 110, 120))); c.drawOval(R.MakeXYWH(-50, -40, 100, 45), stroke(INK, 4))
    c.drawPath(poly([(40, -35), (75, -15), (40, -5)], True), paint((120, 110, 120))); c.drawCircle(52, -26, 4, paint(INK))
    c.drawCircle(30, -42, 12, paint((230, 150, 150))); c.drawCircle(30, -42, 12, stroke(INK, 3))
    c.restore()


def item_icon(c, kind, s=1.0):
    c.save(); c.scale(s, s)
    if kind == 'hatchet':
        c.drawLine(0, 80, 0, -70, stroke((140, 90, 50), 18)); c.drawPath(poly([(0, -70), (70, -90), (70, -20), (0, -30)], True), paint((180, 185, 200)))
        c.drawPath(poly([(0, -70), (70, -90), (70, -20), (0, -30)], True), stroke(INK, 5))
    elif kind == 'pot':
        c.drawRoundRect(R.MakeXYWH(-70, -40, 140, 100), 30, 30, paint((70, 70, 80))); c.drawRoundRect(R.MakeXYWH(-70, -40, 140, 100), 30, 30, stroke(INK, 5))
        c.drawLine(-90, -40, 90, -40, stroke(INK, 10))
    elif kind == 'book':
        c.drawRect(R.MakeXYWH(-60, -80, 120, 160), paint((120, 50, 40))); c.drawRect(R.MakeXYWH(-60, -80, 120, 160), stroke(INK, 5))
        c.drawLine(-10, -40, -10, 20, stroke(YEL, 6)); c.drawLine(-30, -20, 10, -20, stroke(YEL, 6))
    elif kind == 'knife':
        c.drawPath(poly([(-10, -80), (12, -80), (12, 10), (-10, 30)], True), paint((200, 205, 215))); c.drawPath(poly([(-10, -80), (12, -80), (12, 10), (-10, 30)], True), stroke(INK, 4))
        c.drawRoundRect(R.MakeXYWH(-12, 20, 26, 60), 8, 8, paint((120, 80, 40)))
    c.restore()


def book_cover(c, x, y, s, k=1.0):
    if k <= 0: return
    kk = eback(min(1, k), 1.6)
    c.save(); c.translate(x, y); c.scale(s * kk, s * kk)
    c.drawRect(R.MakeXYWH(-180, -250, 360, 500), paint((0, 0, 0), 0.3, blur=10))
    c.drawRect(R.MakeXYWH(-190, -260, 360, 500), paint((150, 50, 40))); c.drawRect(R.MakeXYWH(-190, -260, 360, 500), stroke(INK, 7))
    c.drawRect(R.MakeXYWH(-160, -230, 300, 440), stroke((240, 200, 100), 4))
    f = font('ant', 60); f2 = font('mss', 34)
    for i, ln in enumerate(('ROBINSON', 'CRUSOE')):
        c.drawString(ln, -10 - f.measureText(ln) / 2, -110 + i * 70, f, paint((250, 220, 130)))
    c.drawString('1719', -10 - f2.measureText('1719') / 2, 140, f2, paint((250, 220, 130)))
    c.restore()
