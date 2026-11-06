"""Props for 'What if you went over Niagara Falls in a barrel?' (episode 37, Annie Edson Taylor, 24 Oct 1901)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, tree
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from spinprops import gauge, speed_lines
from meteorprops import speech, medal
from jupprops import no_stamp

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); PINK = (255, 120, 170); MINT = (120, 230, 170)
WATER = (60, 150, 230); WATER_D = (30, 90, 180); FOAM = (240, 250, 255); OAK = (176, 112, 60); OAK_D = (120, 72, 36); IRON = (70, 74, 86)
GOWN = (60, 50, 120)


def annie(c, x, y, s, pose, face, t, flip=False, prop=None, squash=1.0, a=1.0, rot=0.0):
    """Original 1900s lady: wide hat with a pink flower, long dark skirt."""
    c.save(); c.translate(x, y); c.rotate(rot)
    P = rig_points(pose)
    c.save(); c.scale(-s if flip else s, s * squash)
    hx, hy = P['hip']; nx, ny = P['neck']
    sk = skia.Path(); sk.moveTo(hx - 18, hy - 10); sk.lineTo(hx + 18, hy - 10); sk.lineTo(hx + 52, -6); sk.lineTo(hx - 52, -6); sk.close()
    c.drawPath(sk, paint(GOWN)); c.drawPath(sk, stroke(INK, 5))
    c.restore()
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip, prop=prop, squash=squash, a=a)
    c.save(); c.scale(-s if flip else s, s * squash)
    c.drawLine(nx, ny + 6, hx, hy - 8, stroke(GOWN, 20)); c.drawLine(nx, ny + 6, hx, hy - 8, stroke(INK, 3, 0.3))
    c.drawPath(sk, paint(GOWN)); c.drawPath(sk, stroke(INK, 5))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 190, 160, False, stroke((150, 150, 160), 12))
    c.drawOval(R.MakeXYWH(-hr * 1.6, -hr * 1.0, hr * 3.2, hr * 0.5), paint((40, 34, 60))); c.drawOval(R.MakeXYWH(-hr * 1.6, -hr * 1.0, hr * 3.2, hr * 0.5), stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(-hr * 0.8, -hr * 1.55, hr * 1.6, hr * 0.7), 14, 14, paint((40, 34, 60))); c.drawRoundRect(R.MakeXYWH(-hr * 0.8, -hr * 1.55, hr * 1.6, hr * 0.7), 14, 14, stroke(INK, 4))
    for i in range(5):
        a_ = i / 5 * 6.283
        c.drawCircle(hr * 0.6 + math.cos(a_) * 11, -hr * 1.1 + math.sin(a_) * 11, 9, paint(PINK))
    c.drawCircle(hr * 0.6, -hr * 1.1, 7, paint(YEL))
    c.restore()
    c.restore()
    c.restore()


def cat(c, x, y, s, t, face='happy', bandage=0.0, flip=False):
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    orange = (255, 160, 60)
    tail = skia.Path(); tail.moveTo(-60, -30); tail.cubicTo(-130, -40 + 20 * math.sin(t * 3), -120, -150, -80, -150)
    c.drawPath(tail, stroke(INK, 22)); c.drawPath(tail, stroke(orange, 14))
    c.drawOval(R.MakeXYWH(-80, -90, 140, 90), paint(orange)); c.drawOval(R.MakeXYWH(-80, -90, 140, 90), stroke(INK, 6))
    for lx in (-50, -10, 20):
        c.drawLine(lx, -10, lx, 0, stroke(INK, 18)); c.drawLine(lx, -10, lx, 0, stroke(orange, 10))
    c.drawCircle(50, -110, 55, paint(orange)); c.drawCircle(50, -110, 55, stroke(INK, 6))
    for sx in (-1, 1):
        ear = poly([(50 + sx * 20, -155), (50 + sx * 48, -185), (50 + sx * 50, -130)], True)
        c.drawPath(ear, paint(orange)); c.drawPath(ear, stroke(INK, 5))
    if face == 'happy':
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(50 + sx * 20 - 8, -112); p.quadTo(50 + sx * 20, -122, 50 + sx * 20 + 8, -112); c.drawPath(p, stroke(INK, 5))
    else:
        for sx in (-1, 1):
            c.drawCircle(50 + sx * 20, -115, 9, paint(INK)); c.drawCircle(50 + sx * 20 - 3, -118, 3, paint(WHITE))
    c.drawCircle(50, -98, 5, paint((255, 120, 140)))
    for sx in (-1, 1):
        c.drawLine(50 + sx * 25, -95, 50 + sx * 70, -100, stroke(INK, 3)); c.drawLine(50 + sx * 25, -90, 50 + sx * 68, -82, stroke(INK, 3))
    if bandage > 0:
        c.save(); c.translate(50, -150); c.rotate(-20)
        c.drawRoundRect(R.MakeXYWH(-40, -12, 80, 24), 8, 8, paint((255, 235, 220), bandage)); c.drawRoundRect(R.MakeXYWH(-40, -12, 80, 24), 8, 8, stroke(INK, 3, bandage))
        c.drawLine(-6, -6, 6, 6, stroke(RED, 3, bandage)); c.drawLine(-6, 6, 6, -6, stroke(RED, 3, bandage))
        c.restore()
    c.restore()


def barrel(c, x, y, s, rot=0.0, cut=0.0, mattress=0.0, harness=0.0, anvil=0.0, name=True, lid=1.0):
    """upright oak barrel (local height 300, width 200); cut = cutaway reveal of the inside."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    body = skia.Path(); body.moveTo(-90, -150); body.quadTo(-120, 0, -90, 150); body.lineTo(90, 150); body.quadTo(120, 0, 90, -150); body.close()
    c.drawPath(body, paint((0, 0, 0), 0.25, blur=8))
    c.drawPath(body, paint(OAK))
    for i in range(-3, 4):
        p = skia.Path(); p.moveTo(i * 26, -150); p.quadTo(i * 34, 0, i * 26, 150); c.drawPath(p, stroke(OAK_D, 3))
    for yy in (-110, -40, 40, 110):
        w = 98 + 14 * (1 - abs(yy) / 150)
        c.drawLine(-w, yy, w, yy, stroke(IRON, 14, cap=False))
    if cut > 0:
        k = eo(cut)
        inner = skia.Path(); inner.addRoundRect(R.MakeXYWH(-80 * k, -135, 160 * k, 270), 20, 20)
        c.drawPath(inner, paint((60, 36, 20)))
        if mattress > 0:
            c.drawRoundRect(R.MakeXYWH(-72 * k, -125, 144 * k, 250), 24, 24, paint((235, 225, 255), mattress))
            for i in range(5):
                c.drawCircle(-40 * k + (i % 2) * 80 * k, -90 + i * 45, 5, paint((150, 130, 200), mattress))
        if harness > 0:
            c.drawLine(-60 * k, -60, 60 * k, 30, stroke((140, 80, 40), 12, harness)); c.drawLine(60 * k, -60, -60 * k, 30, stroke((140, 80, 40), 12, harness))
        if anvil > 0:
            av = poly([(-50, 135), (50, 135), (40, 105), (65, 85), (-65, 85), (-40, 105)], True)
            c.save(); c.translate(0, -60 * (1 - eo(anvil)))
            c.drawPath(av, paint((80, 84, 96), anvil)); c.drawPath(av, stroke(INK, 5, anvil)); c.restore()
    c.drawPath(body, stroke(INK, 7))
    if lid > 0:
        c.drawOval(R.MakeXYWH(-90, -165, 180, 30), paint(OAK_D)); c.drawOval(R.MakeXYWH(-90, -165, 180, 30), stroke(INK, 5))
    if name and cut <= 0:
        f = font('ant', 30); s_ = 'ANNIE'
        c.drawRoundRect(R.MakeXYWH(-60, -18, 120, 40), 8, 8, paint((255, 245, 220))); c.drawString(s_, -f.measureText(s_) / 2, 12, f, paint(RED))
    c.restore()


def falls_bg(c, t, edge_y=900, top=(120, 200, 255), bot=(200, 235, 255), mist=1.0, cliff=(90, 80, 70)):
    """front-on Horseshoe Falls: river on top, white curtain of water, mist at the bottom."""
    set_bg(c, top, bot, spot=False, t=t)
    if edge_y >= 1000:
        for i in range(5):
            tree(c, 60 + i * 230, edge_y - 120, 0.9, seed=i + 2, col=(60, 170, 90))
    c.drawRect(R.MakeLTRB(0, edge_y - 140, W, edge_y), paint(WATER))
    for i in range(10):
        x = (i * 130 + t * 160) % (W + 200) - 100
        c.drawLine(x, edge_y - 100 + (i % 3) * 30, x + 70, edge_y - 100 + (i % 3) * 30, stroke((200, 230, 255), 6, 0.7))
    c.drawRect(R.MakeLTRB(0, edge_y, W, H), paint((220, 240, 255)))
    for i in range(36):
        x = i * 32 + 6 * math.sin(i)
        ph = (t * 1.6 + hsh(i, 2)) % 1
        c.drawLine(x, edge_y, x + 4, H, stroke((150, 200, 245) if i % 2 else (190, 225, 255), 10, 0.8))
        c.drawLine(x, edge_y + ph * 900, x, edge_y + ph * 900 + 120, stroke((255, 255, 255), 6, 0.8))
    c.drawLine(0, edge_y, W, edge_y, stroke((255, 255, 255), 12))
    if mist > 0:
        for i in range(14):
            mx = (i * 97 + t * 30) % (W + 300) - 150; my = H - 260 + 60 * math.sin(i + t * 0.8)
            c.drawCircle(mx, my, 160 + 40 * hsh(i, 3), paint((255, 255, 255), 0.35 * mist, blur=30))


def river(c, t, y0=1100, col=WATER):
    c.drawRect(R.MakeLTRB(0, y0, W, H), paint(col))
    for i in range(18):
        x = (i * 110 + t * 220) % (W + 200) - 100; yy = y0 + 40 + (i % 6) * 70
        c.drawLine(x, yy, x + 80, yy, stroke((200, 230, 255), 6, 0.7))


def splash(c, x, y, k, s=1.0):
    if k <= 0 or k >= 1: return
    for i in range(22):
        a = -math.pi / 2 + (hsh(i, 5) - 0.5) * 2.4
        d = 320 * s * eo(k) * (0.4 + 0.6 * hsh(i, 6))
        c.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d + 400 * k * k * s, (14 + 16 * hsh(i, 7)) * s, paint((255, 255, 255), 1 - k))


def anvil_icon(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    av = poly([(-60, 40), (60, 40), (40, 10), (90, -10), (-90, -10), (-50, 10)], True)
    c.drawPath(av, paint((80, 84, 96))); c.drawPath(av, stroke(INK, 6)); c.restore()


def pump(c, x, y, s, k):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-30, -180, 60, 180), 12, 12, paint((220, 60, 60))); c.drawRoundRect(R.MakeXYWH(-30, -180, 60, 180), 12, 12, stroke(INK, 5))
    hy = -180 - 60 * (0.5 + 0.5 * math.sin(k * 12))
    c.drawLine(0, hy, 0, -180, stroke(INK, 8)); c.drawLine(-60, hy, 60, hy, stroke(INK, 14))
    c.drawRect(R.MakeXYWH(-70, -6, 140, 16), paint(INK))
    c.restore()


def tower(c, x, y, s, floors=17, k=1.0, col=(240, 200, 150)):
    c.save(); c.translate(x, y); c.scale(s, s)
    n = int(floors * k + 0.999)
    for i in range(n):
        yy = -(i + 1) * 40
        c.drawRect(R.MakeXYWH(-80, yy, 160, 40), paint(col)); c.drawRect(R.MakeXYWH(-80, yy, 160, 40), stroke(INK, 4))
        for wx in (-50, -10, 30):
            c.drawRect(R.MakeXYWH(wx, yy + 10, 22, 20), paint((120, 190, 240)))
    c.restore()


def pool_icon(c, x, y, s, fill=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-200, -80, 400, 160), 20, 20, paint((240, 240, 245))); c.drawRoundRect(R.MakeXYWH(-200, -80, 400, 160), 20, 20, stroke(INK, 6))
    h = 140 * fill
    c.drawRect(R.MakeXYWH(-190, 70 - h, 380, h), paint((80, 190, 250)))
    for i in range(1, 6):
        c.drawLine(-190, 70 - h + i * 0 , 190, 70 - h, stroke((255, 255, 255), 0))
    for i in range(1, 6):
        c.drawLine(-200 + i * 66, 70 - h, -200 + i * 66, 70, stroke((255, 255, 255), 4, 0.7))
    c.restore()


def cannon(c, x, y, s, t, fire=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(-15)
    c.drawRoundRect(R.MakeXYWH(-160, -50, 300, 100), 50, 50, paint((60, 64, 76))); c.drawRoundRect(R.MakeXYWH(-160, -50, 300, 100), 50, 50, stroke(INK, 6))
    c.drawCircle(140, 0, 40, paint(INK))
    c.restore()
    c.drawCircle(-20, 60, 70, paint(OAK)); c.drawCircle(-20, 60, 70, stroke(INK, 6)); c.drawCircle(-20, 60, 14, paint(INK))
    c.restore()


def camera_flash(c, x, y, s, t, k=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-90, -60, 180, 120), 16, 16, paint((60, 60, 70))); c.drawRoundRect(R.MakeXYWH(-90, -60, 180, 120), 16, 16, stroke(INK, 6))
    c.drawCircle(0, 0, 40, paint((150, 200, 240))); c.drawCircle(0, 0, 40, stroke(INK, 6))
    c.drawRect(R.MakeXYWH(40, -80, 40, 20), paint((60, 60, 70)))
    if k > 0:
        c.drawCircle(60, -80, 120 * k, paint((255, 255, 220), (1 - k) * 0.9, blur=10))
    c.restore()


def booklet(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-80, -110, 160, 220), paint((250, 235, 200))); c.drawRect(R.MakeXYWH(-80, -110, 160, 220), stroke(INK, 5))
    f = font('ant', 34); c.drawString('MY RIDE', -f.measureText('MY RIDE') / 2, -50, f, paint(RED))
    for i in range(4): c.drawLine(-55, -10 + i * 30, 55, -10 + i * 30, stroke((180, 160, 120), 5))
    c.drawString('10¢', -30, 100, font('ant', 40), paint(INK))
    c.restore()


def cake(c, x, y, s, t, candles=6):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-150, -120, 300, 120), 20, 20, paint((255, 200, 220))); c.drawRoundRect(R.MakeXYWH(-150, -120, 300, 120), 20, 20, stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-150, -80, 300, 18), paint((255, 255, 255)))
    f = font('ant', 60); c.drawString('63', -f.measureText('63') / 2, -20, f, paint(RED))
    for i in range(candles):
        cx = -110 + i * 44
        c.drawRect(R.MakeXYWH(cx - 7, -180, 14, 60), paint([(120, 200, 255), YEL, MINT][i % 3])); c.drawRect(R.MakeXYWH(cx - 7, -180, 14, 60), stroke(INK, 3))
        c.drawOval(R.MakeXYWH(cx - 8, -212 + 3 * math.sin(t * 10 + i), 16, 26), paint((255, 170, 40)))
    c.restore()
