"""Props for 'What if you were trapped 700 m underground?' (episode 42, San José mine, Chile, 5 Aug - 13 Oct 2010)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, thermometer
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from meteorprops import speech

YEL = (255, 210, 70); RED = (235, 70, 60); TEAL = (40, 190, 180); MINT = (120, 230, 170); ORANGE = (255, 140, 40)
ROCK = (150, 105, 75); ROCK_D = (105, 70, 50); ROCK_L = (190, 140, 100); DESERT = (240, 180, 110); SKY_T = (90, 170, 250)
VEST = (255, 120, 30)


def miner(c, x, y, s, pose, face, t, flip=False, lamp=1.0, shades=0.0, beard=0.0, rot=0.0, dirt=0.0):
    """Original miner: yellow hard hat with headlamp, orange hi-vis vest."""
    c.save(); c.translate(x, y); c.rotate(rot)
    P = rig_points(pose)
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip)
    c.save(); c.scale(-s if flip else s, s)
    nx, ny = P['neck']; hx, hy = P['hip']
    c.drawLine(nx, ny + 6, hx, hy - 6, stroke(VEST, 24)); c.drawLine(nx, ny + 22, hx, ny + 22, stroke((230, 230, 230), 5))
    c.drawLine(nx - 12, ny + 40, nx + 12, ny + 40, stroke((230, 230, 230), 5))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    if dirt > 0:
        for i in range(6): c.drawCircle((hsh(i, 2) - 0.5) * hr * 1.4, (hsh(i, 3) - 0.2) * hr, 5, paint((80, 60, 40), 0.5 * dirt))
    if beard > 0:
        bd = skia.Path(); bd.moveTo(-hr * 0.75, hr * 0.15); bd.quadTo(0, hr * (0.9 + 0.4 * beard), hr * 0.75, hr * 0.15); bd.quadTo(0, hr * 0.55, -hr * 0.75, hr * 0.15); bd.close()
        c.drawPath(bd, paint((60, 50, 45), beard)); c.drawPath(bd, stroke(INK, 3, beard))
    hat = skia.Path(); hat.moveTo(-hr * 1.1, -hr * 0.35); hat.quadTo(-hr * 1.0, -hr * 1.55, 0, -hr * 1.55); hat.quadTo(hr * 1.0, -hr * 1.55, hr * 1.1, -hr * 0.35); hat.close()
    c.drawPath(hat, paint(YEL)); c.drawPath(hat, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(-hr * 1.3, -hr * 0.45, hr * 2.6, hr * 0.22), 6, 6, paint(YEL)); c.drawRoundRect(R.MakeXYWH(-hr * 1.3, -hr * 0.45, hr * 2.6, hr * 0.22), 6, 6, stroke(INK, 4))
    c.drawCircle(0, -hr * 0.95, hr * 0.28, paint((240, 240, 240))); c.drawCircle(0, -hr * 0.95, hr * 0.28, stroke(INK, 4))
    if lamp > 0:
        c.drawCircle(0, -hr * 0.95, hr * 0.5, paint((255, 250, 200), 0.6 * lamp, blur=8))
    if shades > 0:
        for sx in (-1, 1):
            c.drawRoundRect(R.MakeXYWH(sx * 18 - 15, -22, 30, 22), 8, 8, paint(INK, shades))
        c.drawLine(-3, -14, 3, -14, stroke(INK, 4, shades))
    c.restore()
    c.restore()
    c.restore()


def ground_section(c, t, surf=560, mood=0.0):
    """mountain cross-section: sky, desert surface, layered rock, cracks."""
    c.drawRect(R.MakeLTRB(0, 0, W, surf), paint(shader=lin(0, 0, 0, surf, [argb(SKY_T), argb((200, 230, 255))])))

    hill = skia.Path(); hill.moveTo(0, surf)
    for i in range(0, W + 1, 60): hill.lineTo(i, surf - 60 * math.sin(i * 0.006) - 30 * math.sin(i * 0.017))
    hill.lineTo(W, H); hill.lineTo(0, H); hill.close()
    c.drawPath(hill, paint(shader=lin(0, surf, 0, H, [argb(DESERT), argb(ROCK), argb(ROCK_D)])))
    for i in range(7):
        yy = surf + 120 + i * 190
        p = skia.Path(); p.moveTo(0, yy)
        for x in range(0, W + 1, 80): p.lineTo(x, yy + 20 * math.sin(x * 0.01 + i))
        c.drawPath(p, stroke((90, 60, 40), 4, 0.35))
    for i in range(16):
        c.drawCircle(hsh(i, 2) * W, surf + 200 + hsh(i, 3) * 1300, 10 + 20 * hsh(i, 4), paint(ROCK_L, 0.5))
    if mood > 0: c.drawRect(R.MakeWH(W, H), paint((0, 0, 0), mood))


def cave_room(c, t, lamp=1.0, warm=0.0):
    """inside the dark refuge: rock walls lit by helmet lamps."""
    c.drawRect(R.MakeWH(W, H), paint((40, 30, 26)))
    c.drawCircle(540, 1200, 700, paint(shader=skia.GradientShader.MakeRadial((540, 1200), 700, [argb((160, 110, 70), 0.9 * lamp), argb((40, 30, 26), 0)])))
    for i in range(14):
        a = i / 14 * 6.283
        x = 540 + math.cos(a) * 620; y = 1150 + math.sin(a) * 560
        c.drawCircle(x, y, 120 + 40 * hsh(i, 2), paint((70, 50, 40)))
    c.drawRect(R.MakeLTRB(0, 1500, W, H), paint((60, 45, 35)))
    if warm > 0: c.drawRect(R.MakeWH(W, H), paint((255, 120, 40), 0.12 * warm))


def tuna_can(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-90, -40, 180, 80), 20, 20, paint((200, 205, 215))); c.drawRoundRect(R.MakeXYWH(-90, -40, 180, 80), 20, 20, stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-90, -20, 180, 40), paint((60, 130, 220)))
    f = font('ant', 34); c.drawString('TUNA', -f.measureText('TUNA') / 2, 12, f, paint((255, 255, 255)))
    c.restore()


def spoon(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-30, -90, 60, 80), paint((210, 215, 225))); c.drawOval(R.MakeXYWH(-30, -90, 60, 80), stroke(INK, 4))
    c.drawOval(R.MakeXYWH(-18, -70, 36, 40), paint((240, 170, 140)))
    c.drawRoundRect(R.MakeXYWH(-8, -12, 16, 110), 8, 8, paint((210, 215, 225))); c.drawRoundRect(R.MakeXYWH(-8, -12, 16, 110), 8, 8, stroke(INK, 4))
    c.restore()


def milk_cup(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(poly([(-50, -70), (50, -70), (40, 70), (-40, 70)], True), paint((255, 255, 255))); c.drawPath(poly([(-50, -70), (50, -70), (40, 70), (-40, 70)], True), stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-38, 40, 76, 26), paint((245, 245, 235)))
    c.restore()


def cracker(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.addRoundRect(R.MakeXYWH(-70, -50, 140, 100), 10, 10)
    c.drawPath(p, paint((230, 190, 120))); c.drawPath(p, stroke(INK, 5))
    for i in range(3):
        for j in range(2): c.drawCircle(-40 + i * 40, -20 + j * 40, 5, paint((180, 140, 80)))
    c.drawPath(poly([(70, -50), (40, -50), (55, -20), (70, -10)], True), paint((255, 255, 255)))
    c.restore()


def drill_rig(c, x, y, s, t, run=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(poly([(-60, 0), (60, 0), (20, -260), (-20, -260)], True), stroke((80, 80, 90), 10))
    c.drawLine(-60, 0, 20, -260, stroke((80, 80, 90), 6)); c.drawLine(60, 0, -20, -260, stroke((80, 80, 90), 6))
    c.drawRoundRect(R.MakeXYWH(-90, -40, 180, 50), 10, 10, paint((240, 200, 60))); c.drawRoundRect(R.MakeXYWH(-90, -40, 180, 50), 10, 10, stroke(INK, 5))
    if run > 0:
        for i in range(4):
            ph = (t * 1.5 + i / 4) % 1
            c.drawCircle(-60 + 30 * i, -60 - ph * 80, 10 + 10 * ph, paint((200, 190, 170), 0.6 * (1 - ph)))
    c.restore()


def note_paper(c, x, y, s, k=1.0, rot=-5):
    if k <= 0: return
    kk = eback(min(1, k), 1.6)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * kk, s * kk)
    c.drawRect(R.MakeXYWH(-250, -150, 500, 300), paint((0, 0, 0), 0.25, blur=8))
    c.drawRect(R.MakeXYWH(-250, -150, 500, 300), paint((255, 252, 235))); c.drawRect(R.MakeXYWH(-250, -150, 500, 300), stroke(INK, 5))
    for i in range(5): c.drawLine(-230, -90 + i * 50, 230, -90 + i * 50, stroke((170, 200, 240), 3))
    f = font('mbk', 40)
    for i, ln in enumerate(('ESTAMOS BIEN', 'EN EL REFUGIO', 'LOS 33')):
        c.drawString(ln, -f.measureText(ln) / 2, -60 + i * 70, f, paint(RED))
    c.restore()


def capsule(c, x, y, s, t, face=None, shades=0.0):
    """tall narrow rescue capsule with a miner visible through the grille."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-60, -260, 120, 520), 50, 50, paint((240, 245, 250))); c.drawRoundRect(R.MakeXYWH(-60, -260, 120, 520), 50, 50, stroke(INK, 6))
    for yy in (-200, 200):
        c.drawRect(R.MakeXYWH(-60, yy - 12, 120, 24), paint((220, 50, 50)))
    c.drawRoundRect(R.MakeXYWH(-40, -170, 80, 330), 30, 30, paint((60, 70, 90)))
    c.save(); c.clipRect(R.MakeXYWH(-40, -170, 80, 330))
    miner(c, 0, 150, 0.85, POSES['stand'], face or Face('happy', 'grin'), t, shades=shades, beard=0.5)
    c.restore()
    for i in range(5): c.drawLine(-40, -150 + i * 70, 40, -150 + i * 70, stroke((180, 185, 200), 6))
    c.drawLine(0, -260, 0, -2000, stroke((90, 90, 100), 6))
    for sx in (-1, 1): c.drawCircle(sx * 62, -100, 12, paint(INK)); c.drawCircle(sx * 62, 100, 12, paint(INK))
    c.restore()


def dove_tube(c, x, y, s, t, item=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-40, -200, 80, 400), 36, 36, paint((60, 130, 230))); c.drawRoundRect(R.MakeXYWH(-40, -200, 80, 400), 36, 36, stroke(INK, 5))
    c.drawLine(0, -200, 0, -1800, stroke((90, 90, 100), 4))
    c.restore()


def projector(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-70, -40, 140, 80), 14, 14, paint((60, 60, 70))); c.drawRoundRect(R.MakeXYWH(-70, -40, 140, 80), 14, 14, stroke(INK, 5))
    c.drawCircle(70, 0, 26, paint((180, 220, 255))); c.drawCircle(70, 0, 26, stroke(INK, 4))
    c.restore()


def letter(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-80, -55, 160, 110), paint((255, 250, 230))); c.drawRect(R.MakeXYWH(-80, -55, 160, 110), stroke(INK, 5))
    c.drawLine(-80, -55, 0, 10, stroke(INK, 3)); c.drawLine(80, -55, 0, 10, stroke(INK, 3))
    c.drawPath(poly([(0, 20), (-12, 6), (0, 0), (12, 6)], True), paint(RED))
    c.restore()


def water_bottle(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-35, -90, 70, 180), 20, 20, paint((150, 210, 255))); c.drawRoundRect(R.MakeXYWH(-35, -90, 70, 180), 20, 20, stroke(INK, 5))
    c.drawRect(R.MakeXYWH(-18, -115, 36, 26), paint((60, 120, 220)))
    c.restore()


def pills(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, col in enumerate(((240, 90, 90), (90, 160, 240), (250, 210, 70))):
        c.save(); c.translate(-50 + i * 50, 0); c.rotate(30 * (i - 1))
        c.drawRoundRect(R.MakeXYWH(-18, -40, 36, 80), 18, 18, paint(col)); c.drawRoundRect(R.MakeXYWH(-18, -40, 36, 80), 18, 18, stroke(INK, 4))
        c.restore()
    c.restore()
