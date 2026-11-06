"""Props for 'What if a war ended and nobody told you?' (episode 41, Hiroo Onoda, Lubang 1944-1974)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, tree
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from islandprops import jungle
from meteorprops import speech
from jupprops import no_stamp
from trenchprops import jet

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); MINT = (120, 230, 170); ORANGE = (255, 140, 40)
KHAKI = (150, 140, 90); KHAKI_D = (110, 100, 60)


def soldier(c, x, y, s, pose, face, t, flip=False, beard=0.0, worn=0.0, rot=0.0):
    """Original jungle soldier: khaki shirt, field cap with neck flap; worn = patched/tattered."""
    c.save(); c.translate(x, y); c.rotate(rot)
    P = rig_points(pose)
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip)
    c.save(); c.scale(-s if flip else s, s)
    nx, ny = P['neck']; hx, hy = P['hip']
    c.drawLine(nx, ny + 6, hx, hy - 6, stroke(KHAKI, 22)); c.drawLine(nx, ny + 6, hx, hy - 6, stroke(INK, 3, 0.3))
    if worn > 0:
        c.drawRect(R.MakeXYWH(nx - 8, ny + 24, 14, 14), paint((120, 90, 60), worn))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    cap = skia.Path(); cap.moveTo(-hr * 1.02, -hr * 0.35); cap.quadTo(0, -hr * 1.7, hr * 1.02, -hr * 0.35); cap.close()
    c.drawPath(cap, paint(KHAKI)); c.drawPath(cap, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(hr * 0.5, -hr * 0.5, hr * 0.8, 12), 6, 6, paint(KHAKI_D))
    flap = poly([(-hr * 1.0, -hr * 0.4), (-hr * 1.25, hr * 0.5), (-hr * 0.7, hr * 0.3)], True)
    c.drawPath(flap, paint(KHAKI)); c.drawPath(flap, stroke(INK, 3))
    c.drawCircle(0, -hr * 0.9, 7, paint(YEL))
    if beard > 0:
        bd = skia.Path(); bd.moveTo(-hr * 0.75, hr * 0.15); bd.quadTo(0, hr * (0.9 + 0.5 * beard), hr * 0.75, hr * 0.15); bd.quadTo(0, hr * 0.55, -hr * 0.75, hr * 0.15); bd.close()
        c.drawPath(bd, paint((70, 60, 50), beard)); c.drawPath(bd, stroke(INK, 3, beard))
    c.restore()
    c.restore()
    c.restore()


def leaflets(c, t, k, n=26, seed=3):
    for i in range(n):
        ph = (t * (0.18 + 0.1 * hsh(i, seed)) + hsh(i, seed + 1)) % 1
        x = hsh(i, seed + 2) * W + 40 * math.sin(t * 2 + i)
        y = 900 + ph * 700
        c.save(); c.translate(x, y); c.rotate(30 * math.sin(t * 3 + i)); c.scale(k, k)
        c.drawRect(R.MakeXYWH(-34, -24, 68, 48), paint((255, 252, 235))); c.drawRect(R.MakeXYWH(-34, -24, 68, 48), stroke(INK, 3))
        for j in range(3): c.drawLine(-24, -10 + j * 10, 24, -10 + j * 10, stroke((150, 150, 160), 3))
        c.restore()


def big_leaflet(c, x, y, s, k=1.0, fake=0.0):
    if k <= 0: return
    kk = eback(min(1, k), 1.6)
    c.save(); c.translate(x, y); c.rotate(-6); c.scale(s * kk, s * kk)
    c.drawRect(R.MakeXYWH(-200, -140, 400, 280), paint((255, 252, 235))); c.drawRect(R.MakeXYWH(-200, -140, 400, 280), stroke(INK, 6))
    f = font('ant', 60); s_ = 'THE WAR IS OVER'
    c.drawString(s_, -f.measureText(s_) / 2, -40, f, paint(INK))
    for j in range(3): c.drawLine(-150, 30 + j * 30, 150, 30 + j * 30, stroke((160, 160, 170), 6))
    if fake > 0:
        c.save(); c.rotate(-18); c.scale(eback(min(1, fake), 1.8), eback(min(1, fake), 1.8))
        c.drawRoundRect(R.MakeXYWH(-150, -50, 300, 100), 14, 14, stroke(RED, 10)); fs = font('ant', 80)
        c.drawString('FAKE?', -fs.measureText('FAKE?') / 2, 28, fs, paint(RED)); c.restore()
    c.restore()


def year_flip(c, x, y, s, year, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-220, -130, 440, 260), 30, 30, paint(INK)); c.drawRoundRect(R.MakeXYWH(-205, -115, 410, 230), 22, 22, paint((40, 40, 52)))
    c.drawLine(-205, 0, 205, 0, stroke(INK, 6))
    f = font('ant', 190); s_ = str(year)
    c.drawString(s_, -f.measureText(s_) / 2, 68, f, paint(YEL))
    c.restore()


def panda(c, x, y, s, t):
    c.save(); c.translate(x, y + 4 * math.sin(t * 2)); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-80, -150, 160, 150), paint((255, 255, 255))); c.drawOval(R.MakeXYWH(-80, -150, 160, 150), stroke(INK, 5))
    c.drawCircle(0, -200, 70, paint((255, 255, 255))); c.drawCircle(0, -200, 70, stroke(INK, 5))
    for sx in (-1, 1):
        c.drawCircle(sx * 52, -255, 24, paint(INK))
        c.drawOval(R.MakeXYWH(sx * 26 - 16, -222, 32, 40), paint(INK)); c.drawCircle(sx * 26, -205, 6, paint((255, 255, 255)))
        c.drawOval(R.MakeXYWH(sx * 70 - 22, -110, 44, 80), paint(INK))
    c.drawOval(R.MakeXYWH(-10, -178, 20, 12), paint(INK))
    c.restore()


def snow_beast(c, x, y, s, t):
    """original shaggy white mountain creature."""
    c.save(); c.translate(x, y + 4 * math.sin(t * 2 + 1)); c.scale(s, s)
    body = skia.Path()
    for i in range(24):
        a = i / 24 * 6.283; r = 110 + 16 * (i % 2)
        (body.moveTo if i == 0 else body.lineTo)(math.cos(a) * r * 0.8, -150 + math.sin(a) * r * 1.3)
    body.close()
    c.drawPath(body, paint((235, 240, 250))); c.drawPath(body, stroke(INK, 5))
    c.drawOval(R.MakeXYWH(-50, -260, 100, 70), paint((150, 170, 210))); c.drawOval(R.MakeXYWH(-50, -260, 100, 70), stroke(INK, 4))
    for sx in (-1, 1): c.drawCircle(sx * 20, -232, 8, paint(INK))
    c.drawPath(poly([(-14, -205), (14, -205), (0, -196)], True), paint(INK))
    c.restore()


def explorer(c, x, y, s, pose, face, t, flip=False):
    draw_stick(c, x, y, s, pose, face, t=t, scarf=ORANGE, flip=flip)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    nx, ny = P['neck']; hx, hy = P['hip']
    c.drawRoundRect(R.MakeXYWH(nx - 52, ny + 4, 40, 70), 10, 10, paint((60, 120, 200))); c.drawRoundRect(R.MakeXYWH(nx - 52, ny + 4, 40, 70), 10, 10, stroke(INK, 4))
    hdx, hdy = P['head']
    c.save(); c.translate(hdx, hdy)
    hr = LEN['head']
    c.drawOval(R.MakeXYWH(-hr * 1.4, -hr * 0.75, hr * 2.8, hr * 0.4), paint((200, 170, 110))); c.drawOval(R.MakeXYWH(-hr * 1.4, -hr * 0.75, hr * 2.8, hr * 0.4), stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(-hr * 0.8, -hr * 1.35, hr * 1.6, hr * 0.75), 16, 16, paint((200, 170, 110))); c.drawRoundRect(R.MakeXYWH(-hr * 0.8, -hr * 1.35, hr * 1.6, hr * 0.75), 16, 16, stroke(INK, 4))
    c.restore()
    c.restore()


def commander(c, x, y, s, pose, face, t, flip=False):
    """older officer-turned-bookseller: grey hair, round glasses, cardigan."""
    draw_stick(c, x, y, s, pose, face, t=t, scarf=None, flip=flip)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    nx, ny = P['neck']; hx, hy = P['hip']
    c.drawLine(nx, ny + 6, hx, hy - 6, stroke((140, 60, 70), 22))
    hdx, hdy = P['head']
    c.save(); c.translate(hdx, hdy)
    hr = LEN['head']
    c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 200, 140, False, stroke((200, 200, 205), 12))
    for sx in (-1, 1): c.drawCircle(sx * 15, -8, 14, stroke(INK, 3))
    c.restore()
    c.restore()


def bookshelf(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-260, -560, 520, 560), paint((140, 90, 50))); c.drawRect(R.MakeXYWH(-260, -560, 520, 560), stroke(INK, 6))
    cols = [(220, 80, 80), (80, 140, 220), (240, 200, 70), (90, 180, 120), (180, 110, 200)]
    for r in range(4):
        yy = -540 + r * 135
        c.drawLine(-260, yy + 120, 260, yy + 120, stroke((100, 60, 30), 10))
        xx = -240
        for i in range(12):
            w = 26 + 12 * hsh(r * 12 + i, 2); h = 80 + 30 * hsh(r * 12 + i, 3)
            if xx + w > 240: break
            c.drawRect(R.MakeXYWH(xx, yy + 120 - h, w, h), paint(cols[(r + i) % 5])); c.drawRect(R.MakeXYWH(xx, yy + 120 - h, w, h), stroke(INK, 2))
            xx += w + 4
    c.restore()


def missed_icon(c, kind, s=1.0, t=0.0):
    c.save(); c.scale(s, s)
    if kind == 'moon':
        c.drawCircle(0, 0, 80, paint((230, 230, 225))); c.drawCircle(0, 0, 80, stroke(INK, 5))
        for (dx, dy, r) in ((-25, -20, 14), (20, 15, 18), (30, -30, 8)): c.drawCircle(dx, dy, r, paint((200, 200, 195)))
        c.drawLine(10, -60, 10, -120, stroke(INK, 4)); c.drawRect(R.MakeXYWH(10, -120, 50, 30), paint((60, 120, 220)))
    elif kind == 'tv':
        c.drawRoundRect(R.MakeXYWH(-90, -70, 180, 130), 20, 20, paint((120, 80, 50))); c.drawRoundRect(R.MakeXYWH(-90, -70, 180, 130), 20, 20, stroke(INK, 5))
        cols = [(255, 80, 80), (255, 200, 60), (80, 200, 120), (80, 160, 255), (200, 100, 255)]
        for i, col in enumerate(cols): c.drawRect(R.MakeXYWH(-70 + i * 24, -52, 24, 90), paint(col))
        c.drawLine(-30, -70, -60, -110, stroke(INK, 4)); c.drawLine(30, -70, 60, -110, stroke(INK, 4))
    elif kind == 'record':
        c.drawCircle(0, 0, 85, paint(INK)); c.drawCircle(0, 0, 30, paint((240, 90, 90))); c.drawCircle(0, 0, 6, paint((255, 255, 255)))
        for r in (45, 60, 75): c.drawCircle(0, 0, r, stroke((60, 60, 70), 2))
    c.restore()


def cow(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    for lx in (-60, -30, 40, 70): c.drawLine(lx, -60, lx, 0, stroke(INK, 14)); c.drawLine(lx, -60, lx, 0, stroke((255, 255, 255), 8))
    c.drawRoundRect(R.MakeXYWH(-100, -150, 210, 100), 40, 40, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-100, -150, 210, 100), 40, 40, stroke(INK, 5))
    for (dx, dy, r) in ((-40, -110, 22), (30, -120, 18), (60, -85, 14)): c.drawCircle(dx, dy, r, paint(INK))
    c.drawOval(R.MakeXYWH(90, -190, 80, 70), paint((255, 255, 255))); c.drawOval(R.MakeXYWH(90, -190, 80, 70), stroke(INK, 5))
    c.drawOval(R.MakeXYWH(120, -150, 56, 34), paint((255, 180, 190))); c.drawCircle(120, -170, 5, paint(INK))
    c.restore()
