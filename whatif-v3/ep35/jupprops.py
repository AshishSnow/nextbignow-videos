"""Props for 'What if you fell into Jupiter?' (episode 35, the Galileo probe 1995 + orbiter 2003)."""
import math
import skia
from toon import *
from props import cam, mag_field
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from elevprops import fg_dust
from spinprops import gauge, speed_lines
from fallprops import parachute
from caveprops import dumbbell, sun_icon, stopwatch_count

YEL = (255, 210, 70); RED = (235, 70, 60); CREAM = (250, 232, 200); TAN = (226, 170, 120); RUST = (190, 100, 60)
BANDS = [(250, 236, 210), (228, 176, 124), (246, 220, 186), (196, 120, 76), (240, 210, 170), (214, 150, 100), (252, 240, 220)]


def scale_box(c, x, y, s, val, k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-130, -40, 260, 50), 18, 18, paint((235, 238, 245))); c.drawRoundRect(R.MakeXYWH(-130, -40, 260, 50), 18, 18, stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-80, 20, 160, 70), 12, 12, paint((30, 34, 44))); c.drawRoundRect(R.MakeXYWH(-80, 20, 160, 70), 12, 12, stroke(INK, 5))
    f = font('ant', 54); lab = '%d kg' % val
    c.drawString(lab, -f.measureText(lab) / 2, 74, f, paint((255, 90, 70) if val > 70 else (120, 230, 140)))
    c.restore()


# ------------------------------------------------------------------ characters + craft
def astro(c, x, y, s, pose, face, t, rot=0.0, flip=False, squash=1.0, prop=None):
    """Mascot in a white spacesuit with a bubble helmet and a small backpack."""
    c.save(); c.translate(x, y); c.rotate(rot)
    P = rig_points(pose)
    c.save(); c.scale(-s if flip else s, s * squash)
    nx, ny = P['neck']; hx, hy = P['hip']
    c.drawRoundRect(R.MakeXYWH(nx - 34 - 24, ny - 4, 30, 70), 10, 10, paint((200, 205, 215))); c.drawRoundRect(R.MakeXYWH(nx - 34 - 24, ny - 4, 30, 70), 10, 10, stroke(INK, 4))
    c.restore()
    draw_stick(c, 0, 0, s, pose, face, t=t, scarf=None, flip=flip, helmet=1.0, squash=squash, prop=prop)
    c.save(); c.scale(-s if flip else s, s * squash)
    c.drawLine(nx, ny + 6, hx, hy - 6, stroke((245, 245, 250), 20)); c.drawLine(nx, ny + 6, hx, hy - 6, stroke(INK, 3, 0.3))
    c.drawRoundRect(R.MakeXYWH((nx + hx) / 2 - 10, (ny + hy) / 2 - 8, 20, 14), 3, 3, paint(RED))
    c.restore()
    c.restore()


def probe(c, x, y, s, t, rot=0.0, heat=0.0, chute=0.0, signal=1.0):
    """Galileo atmospheric probe: blunt cone heat shield, aft cover, antenna; heat = plasma glow."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if chute > 0:
        c.save(); c.translate(0, -260); c.scale(0.5 * chute, 0.5 * chute)
        parachute(c, 0, 0, 1.0, t, col1=(255, 150, 40), col2=(255, 255, 255))
        c.restore()
        for sx in (-1, 1): c.drawLine(sx * 60, -40, sx * 120 * chute, -260 + 160 * chute * 0.5, stroke(INK, 2.5))
    if heat > 0:
        trail = poly([(-90, -20), (90, -20), (30, -520), (-30, -520)], True)
        c.drawPath(trail, paint(shader=lin(0, -20, 0, -520, [argb((255, 240, 200), 0.9 * heat), argb((255, 140, 40), 0.6 * heat), argb((255, 80, 20), 0)])))
        c.drawCircle(0, 40, 170, paint((255, 170, 60), 0.5 * heat, blur=40))
    body = skia.Path(); body.moveTo(-110, 10); body.lineTo(-60, -70); body.lineTo(60, -70); body.lineTo(110, 10); body.close()
    c.drawPath(body, paint((210, 214, 224))); c.drawPath(body, stroke(INK, 6))
    shield = skia.Path(); shield.moveTo(-120, 10); shield.quadTo(0, 120, 120, 10); shield.close()
    c.drawPath(shield, paint(mix((150, 90, 60), (255, 230, 170), heat))); c.drawPath(shield, stroke(INK, 6))
    c.drawLine(0, -70, 0, -120, stroke(INK, 5)); c.drawCircle(0, -124, 9, paint(YEL)); c.drawCircle(0, -124, 9, stroke(INK, 3))
    if signal > 0:
        for i in range(3):
            ph = (t * 1.2 + i / 3) % 1
            c.drawArc(R.MakeXYWH(-40 - ph * 120, -164 - ph * 120, 80 + ph * 240, 80 + ph * 240), 225, 90, False, stroke((120, 220, 255), 6, signal * (1 - ph)))
    c.restore()


def orbiter(c, x, y, s, t, rot=0.0, fire=0.0):
    """Galileo orbiter: big dish antenna, body, two boom arms."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for sx in (-1, 1):
        c.drawLine(0, 30, sx * 230, 90, stroke((150, 150, 160), 10)); c.drawLine(0, 30, sx * 230, 90, stroke(INK, 3, 0.4))
        c.drawRoundRect(R.MakeXYWH(sx * 230 - 26, 66, 52, 52), 10, 10, paint((90, 90, 100))); c.drawRoundRect(R.MakeXYWH(sx * 230 - 26, 66, 52, 52), 10, 10, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(-60, -10, 120, 120), 14, 14, paint((230, 190, 90))); c.drawRoundRect(R.MakeXYWH(-60, -10, 120, 120), 14, 14, stroke(INK, 6))
    dish = skia.Path(); dish.moveTo(-170, -20); dish.quadTo(0, -170, 170, -20); dish.quadTo(0, -60, -170, -20); dish.close()
    c.drawPath(dish, paint((245, 245, 250))); c.drawPath(dish, stroke(INK, 6))
    for k in (-100, -40, 40, 100): c.drawLine(k * 0.2, -60, k, -40 - (170 - abs(k)) * 0.5, stroke((180, 180, 190), 3))
    c.drawLine(0, -60, 0, -150, stroke(INK, 5)); c.drawCircle(0, -152, 10, paint(RED))
    if fire > 0:
        c.drawCircle(0, 60, 220, paint((255, 150, 60), 0.5 * fire, blur=50))
    c.restore()


# ------------------------------------------------------------------ backdrops
def jupiter_space(c, t, cx=540, cy=2300, r=1500, rot=0.0, glow=True):
    space_bg(c, t, (14, 16, 50), (36, 24, 60), seed=6, glow=(255, 170, 90) if glow else None, gx=cx, gy=cy - r)
    draw_planet(c, 'jupiter', cx, cy, r, rot=rot + t * 0.02, glow=(255, 210, 160), halo=(255, 190, 130), light=(-0.45, -0.6, 0.66))


def cloud_fall(c, t, depth=0.0, speed=1.0, dark=0.0, ammonia=0.0):
    """Falling through Jupiter's sky: horizontal coloured bands scrolling up, puffy clouds rushing past."""
    top = mix((255, 214, 160), (12, 10, 26), dark); bot = mix((214, 130, 80), (4, 4, 12), dark)
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(top), argb(bot)])))
    off = (t * 420 * speed) % 300
    for i in range(-1, 9):
        y = i * 300 - off + 150
        col = mix(BANDS[(i + int(t * 420 * speed // 300)) % len(BANDS)], (10, 8, 20), dark)
        c.drawRect(R.MakeXYWH(-20, y - 40, W + 40, 80), paint(col, 0.35 * (1 - dark * 0.7), blur=30))
    for i in range(14):
        ph = (t * 0.35 * speed * (0.6 + hsh(i, 3)) + hsh(i, 4)) % 1
        x = hsh(i, 5) * W; y = H + 300 - ph * (H + 600)
        r = 90 + 160 * hsh(i, 6)
        col = mix(mix(CREAM, (255, 255, 255), ammonia), (20, 16, 30), dark)
        a = 0.8 * (1 - dark * 0.6)
        for j in range(4):
            c.drawCircle(x + (j - 1.5) * r * 0.55, y + math.sin(j * 1.7) * r * 0.2, r * (0.6 + 0.2 * math.sin(j)), paint(col, a, blur=r * 0.25))
    speed_lines(c, t, a=0.8 * (1 - dark), n=20, speed=-2200 * speed, col=(255, 255, 255)) if False else None
    for i in range(18):
        ph = (t * 1.8 * speed + hsh(i, 11)) % 1
        x = hsh(i, 12) * W; y = H - ph * (H + 300)
        c.drawLine(x, y, x, y + 160 + 100 * hsh(i, 13), stroke((255, 255, 255), 5, 0.35 * (1 - dark)))


def metal_ocean(c, t, k=1.0, top=900):
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb((8, 8, 20)), argb((20, 22, 40))])))
    if k <= 0: return
    p = skia.Path(); p.moveTo(-20, H + 20)
    for i in range(0, 46):
        x = -20 + i * 26
        p.lineTo(x, top + 18 * math.sin(x * 0.012 + t * 1.5) + 8 * math.sin(x * 0.04 - t * 2.2))
    p.lineTo(W + 20, H + 20); p.close()
    c.saveLayerAlpha(None, int(255 * k))
    c.drawPath(p, paint(shader=lin(0, top, 0, H, [argb((230, 236, 250)), argb((140, 150, 175)), argb((60, 66, 88))], [0, 0.3, 1])))
    c.save(); c.clipPath(p, doAntiAlias=True)
    for i in range(16):
        y = top + 40 + i * 60; ph = t * 1.2 + i
        c.drawLine(-20, y + 10 * math.sin(ph), W + 20, y + 10 * math.sin(ph + 1.5), stroke((255, 255, 255), 4, 0.25 - i * 0.012))
    for i in range(5):
        x = 150 + i * 200 + 30 * math.sin(t + i)
        c.drawOval(R.MakeXYWH(x - 60, top + 120 + i * 40, 120, 20), paint((255, 255, 255), 0.5, blur=6))
    c.restore()
    c.drawPath(p, stroke(INK, 6))
    c.restore()


def cutaway(c, x, y, r, t, k=1.0, marker=None, labels=True, glow_core=1.0):
    """Jupiter cut open: clouds, hydrogen gas, liquid metallic hydrogen, fuzzy core. marker = depth 0..1 for the 'you are here' pin."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    draw_planet(c, 'jupiter', 0, 0, r, rot=t * 0.03, glow=(255, 210, 160), light=(-0.5, -0.4, 0.75))
    wedge = skia.Path(); wedge.moveTo(0, 0); wedge.arcTo(R.MakeXYWH(-r - 2, -r - 2, 2 * r + 4, 2 * r + 4), -60, 80, False); wedge.close()
    c.drawPath(wedge, paint((14, 10, 24)))
    layers = [(1.0, (235, 190, 140)), (0.93, (196, 130, 90)), (0.78, (150, 160, 190)), (0.45, (255, 140, 60))]
    for frac, col in layers:
        p = skia.Path(); p.moveTo(0, 0); p.arcTo(R.MakeXYWH(-r * frac, -r * frac, 2 * r * frac, 2 * r * frac), -60, 80, False); p.close()
        c.drawPath(p, paint(col))
    c.drawCircle(0, 0, r * 0.45 * 0.7, paint((255, 220, 120), 0.6 * glow_core, blur=r * 0.08))
    c.drawPath(wedge, stroke(INK, 6))
    for frac in (0.93, 0.78, 0.45):
        c.drawArc(R.MakeXYWH(-r * frac, -r * frac, 2 * r * frac, 2 * r * frac), -60, 80, False, stroke(INK, 3, 0.6))
    if labels:
        f = font('ant', 40)
        for i, (frac, lab) in enumerate(((0.965, 'CLOUDS'), (0.86, 'HYDROGEN GAS'), (0.62, 'LIQUID METAL'), (0.22, 'CORE'))):
            a = math.radians(-20); rr = r * frac
            px, py = math.cos(a) * rr, math.sin(a) * rr
            ly = -r * 0.62 + i * r * 0.36
            lx = r * 1.12
            c.drawLine(px, py, lx - 10, ly, stroke((255, 255, 255), 3, 0.8))
            c.drawCircle(px, py, 6, paint((255, 255, 255)))
            c.drawString(lab, lx, ly + 14, f, paint((255, 255, 255)))
    if marker is not None:
        a = math.radians(-20); rr = r * (1 - marker)
        px, py = math.cos(a) * rr, math.sin(a) * rr
        c.drawCircle(px, py, r * 0.06 + 6 * math.sin(t * 6), paint(RED, 0.5, blur=8))
        c.drawCircle(px, py, r * 0.035, paint(RED)); c.drawCircle(px, py, r * 0.035, stroke((255, 255, 255), 4))
    c.restore()


def europa(c, x, y, r, t, cut=0.0, life=0.0):
    c.save(); c.translate(x, y)
    c.drawCircle(0, 0, r * 1.15, paint((200, 230, 255), 0.25, blur=r * 0.2))
    c.drawCircle(0, 0, r, paint(shader=rad(-r * 0.3, -r * 0.3, r * 1.4, [argb((255, 250, 240)), argb((225, 210, 190)), argb((150, 130, 120))])))
    c.save(); p = skia.Path(); p.addCircle(0, 0, r); c.clipPath(p, doAntiAlias=True)
    for i in range(12):
        a0 = hsh(i, 3) * 6.28; q = skia.Path(); px, py = math.cos(a0) * r * 1.2, math.sin(a0) * r * 1.2; q.moveTo(px, py)
        for j in range(5):
            a0 += (hsh(i * 7 + j, 4) - 0.5) * 0.8; px -= math.cos(a0) * r * 0.45; py -= math.sin(a0) * r * 0.45; q.lineTo(px, py)
        c.drawPath(q, stroke((170, 90, 60), 5, 0.7))
    if cut > 0:
        cw = skia.Path(); cw.moveTo(0, 0); cw.arcTo(R.MakeXYWH(-r, -r, 2 * r, 2 * r), -30, 90 * cut, False); cw.close()
        c.drawPath(cw, paint((250, 250, 255)))
        oc = skia.Path(); oc.moveTo(0, 0); oc.arcTo(R.MakeXYWH(-r * 0.9, -r * 0.9, 1.8 * r, 1.8 * r), -30, 90 * cut, False); oc.close()
        c.drawPath(oc, paint((40, 120, 220)))
        rk = skia.Path(); rk.moveTo(0, 0); rk.arcTo(R.MakeXYWH(-r * 0.62, -r * 0.62, 1.24 * r, 1.24 * r), -30, 90 * cut, False); rk.close()
        c.drawPath(rk, paint((120, 100, 90)))
        c.drawPath(cw, stroke(INK, 5))
    c.restore()
    c.drawCircle(0, 0, r, stroke(INK, 6))
    if life > 0:
        a = math.radians(15); px, py = math.cos(a) * r * 0.76, math.sin(a) * r * 0.76
        microbe(c, px, py, 0.5 * eback(min(1, life), 1.6), t)
    c.restore()


def microbe(c, x, y, s, t, col=(120, 220, 120), angry=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(8):
        a = i * 0.785 + math.sin(t * 4 + i) * 0.1
        c.drawLine(math.cos(a) * 50, math.sin(a) * 40, math.cos(a) * 72, math.sin(a) * 60, stroke(INK, 4))
    c.drawOval(R.MakeXYWH(-56, -44, 112, 88), paint(col)); c.drawOval(R.MakeXYWH(-56, -44, 112, 88), stroke(INK, 5))
    for sx in (-1, 1):
        c.drawCircle(sx * 18, -8, 10, paint((255, 255, 255))); c.drawCircle(sx * 18 + 2, -6, 5, paint(INK))
        if angry: c.drawLine(sx * 8, -24, sx * 30, -18 - 8, stroke(INK, 4))
    p = skia.Path(); p.moveTo(-14, 16); p.quadTo(0, 28 if not angry else 8, 14, 16); c.drawPath(p, stroke(INK, 4))
    c.restore()


def no_stamp(c, x, y, s, k):
    if k <= 0: return
    kk = eback(min(1, k), 1.8)
    c.save(); c.translate(x, y); c.rotate(-12); c.scale(s * kk, s * kk)
    c.drawCircle(0, 0, 110, stroke(RED, 18)); c.drawLine(-78, 78, 78, -78, stroke(RED, 18))
    c.restore()


def spray_bottle(c, x, y, s, t, spray=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-50, -40, 100, 170), 24, 24, paint((120, 200, 255))); c.drawRoundRect(R.MakeXYWH(-50, -40, 100, 170), 24, 24, stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-36, 10, 72, 70), 10, 10, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-36, 10, 72, 70), 10, 10, stroke(INK, 4))
    f = font('ant', 22); s_ = 'NH3'; c.drawString(s_, -f.measureText(s_) / 2, 54, f, paint(INK))
    c.drawRoundRect(R.MakeXYWH(-30, -100, 60, 64), 10, 10, paint((240, 240, 245))); c.drawRoundRect(R.MakeXYWH(-30, -100, 60, 64), 10, 10, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(26, -96, 50, 22), 6, 6, paint((240, 240, 245))); c.drawRoundRect(R.MakeXYWH(26, -96, 50, 22), 6, 6, stroke(INK, 4))
    if spray > 0:
        for i in range(10):
            ph = (t * 2 + i / 10) % 1
            c.drawCircle(80 + ph * 200, -86 + (hsh(i, 3) - 0.5) * 120 * ph, 6 + 14 * ph, paint((220, 240, 255), 0.6 * (1 - ph) * spray))
    c.restore()


def car_seat(c, x, y, s, t, squash=0.0):
    """Mascot in a car seat being flattened by a seatbelt (230 g gag)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-120, -300, 90, 300), 30, 30, paint((60, 60, 72))); c.drawRoundRect(R.MakeXYWH(-120, -300, 90, 300), 30, 30, stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-130, -40, 260, 70), 24, 24, paint((60, 60, 72))); c.drawRoundRect(R.MakeXYWH(-130, -40, 260, 70), 24, 24, stroke(INK, 6))
    c.restore()
    sq = 1 - 0.55 * squash
    draw_stick(c, x, y - 30 * s, s * 1.1, POSES['sit'], Face('wide', 'chatter' if squash > 0.3 else 'o', 'worried'), t=t, squash=sq)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(-80, -260 * sq, 60, -40, stroke((200, 40, 50), 18)); c.drawLine(-80, -260 * sq, 60, -40, stroke(INK, 3, 0.4))
    c.restore()


def hurricane_icon(c, x, y, s, t):
    c.save(); c.translate(x, y); c.rotate(-t * 200); c.scale(s, s)
    for i in range(3):
        p = skia.Path(); p.moveTo(0, 0)
        for j in range(30):
            a = i * 2.094 + j * 0.15; rr = j * 4
            p.lineTo(math.cos(a) * rr, math.sin(a) * rr)
        c.drawPath(p, stroke((120, 170, 230), 14)); c.drawPath(p, stroke(INK, 3, 0.4))
    c.drawCircle(0, 0, 16, paint((240, 245, 255))); c.drawCircle(0, 0, 16, stroke(INK, 4))
    c.restore()


def thermometer(c, x, y, s, frac, label, col=RED):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-30, -260, 60, 300), 30, 30, paint((255, 255, 255))); c.drawRoundRect(R.MakeXYWH(-30, -260, 60, 300), 30, 30, stroke(INK, 6))
    h = 240 * frac
    c.drawRoundRect(R.MakeXYWH(-16, 30 - h, 32, h), 16, 16, paint(col))
    c.drawCircle(0, 60, 54, paint(col)); c.drawCircle(0, 60, 54, stroke(INK, 6))
    f = font('ant', 70); c.drawString(label, -f.measureText(label) / 2, 190, f, paint((255, 255, 255)))
    c.restore()


def india_bar(c, x, y, w, t, k):
    """3,000 km bar labelled INDIA with the probe zipping across."""
    c.drawRoundRect(R.MakeXYWH(x, y - 50, w, 100), 50, 50, paint((255, 150, 60))); c.drawRoundRect(R.MakeXYWH(x, y - 50, w, 100), 50, 50, stroke(INK, 7))
    for i in range(3):
        c.drawRect(R.MakeXYWH(x + 40 + i * (w - 80) / 3, y - 50, (w - 80) / 3, 33), paint([(255, 153, 51), (255, 255, 255), (19, 136, 8)][i], 0.0))
    f = font('ant', 64); s_ = 'INDIA  ~3,000 KM'; c.drawString(s_, x + w / 2 - f.measureText(s_) / 2, y + 22, f, paint((255, 255, 255)))
    px = x + w * k
    c.save(); c.translate(px, y - 120); c.rotate(-90); probe(c, 0, 0, 0.45, t, heat=1.0, signal=0.0); c.restore()
