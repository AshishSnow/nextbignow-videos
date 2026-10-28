"""Props for 'What if you lived in a cave for 500 days?' (episode 34, Beatriz Flamini + Michel Siffre)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, blink_at
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from elevprops import fg_dust
from hicprops import speech, brain

ROCK = (78, 62, 96); ROCK_D = (46, 36, 62); ROCK_L = (118, 96, 140)
LAMP = (255, 214, 140); ORANGE = (255, 140, 40); TEAL = (40, 190, 180); YEL = (255, 210, 70); RED = (235, 70, 60)
SKY_N = ((10, 14, 48), (40, 36, 90))


# ------------------------------------------------------------------ characters
def beatriz(c, x, y, s, pose, face, t, flip=False, lamp=1.0, prop=None, squash=1.0, a=1.0):
    """Beatriz: bun, headlamp, orange climbing jacket band, harness."""
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=None, flip=flip, prop=prop, squash=squash, a=a)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s * squash)
    if a < 1: c.saveLayerAlpha(None, int(255 * a))
    nx, ny = P['neck']; hx, hy = P['hip']
    # jacket band + harness
    c.drawLine(nx - 1, ny + 8, hx, hy - 10, stroke(ORANGE, 17))
    c.drawLine(nx - 1, ny + 8, hx, hy - 10, stroke(INK, 3, 0.35))
    c.drawLine(hx - 22, hy - 4, hx + 22, hy - 4, stroke((60, 60, 70), 8))
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    c.drawCircle(-hr * 0.55, -hr * 0.78, 20, paint(INK))                                   # bun
    c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 195, 150, False, stroke(INK, 12))   # hair line
    c.drawRoundRect(R.MakeXYWH(-hr * 0.9, -hr * 0.62, hr * 1.8, 16), 8, 8, paint((60, 60, 70)))                # headband
    c.drawRoundRect(R.MakeXYWH(hr * 0.52, -hr * 0.74, 34, 36), 8, 8, paint((80, 82, 92))); c.drawRoundRect(R.MakeXYWH(hr * 0.52, -hr * 0.74, 34, 36), 8, 8, stroke(INK, 4))
    c.drawCircle(hr * 0.52 + 17, -hr * 0.56, 11, paint(LAMP))
    if lamp > 0:
        beam = poly([(hr * 0.86, -hr * 0.6), (hr * 0.86 + 520, -hr * 0.6 - 190), (hr * 0.86 + 520, -hr * 0.6 + 230)], True)
        c.drawPath(beam, paint(shader=lin(hr * 0.86, 0, hr * 0.86 + 520, 0, [argb(LAMP, 0.45 * lamp), argb(LAMP, 0)])))
    c.restore()
    if a < 1: c.restore()
    c.restore()
    return r


def siffre(c, x, y, s, pose, face, t, flip=False, prop=None):
    """Michel Siffre: 70s beard, round glasses, headlamp."""
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=None, flip=flip, prop=prop)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    bd = skia.Path(); bd.moveTo(-hr * 0.8, hr * 0.1); bd.quadTo(-hr * 0.5, hr * 1.3, 0, hr * 1.35); bd.quadTo(hr * 0.5, hr * 1.3, hr * 0.8, hr * 0.1)
    bd.quadTo(hr * 0.4, hr * 0.55, 0, hr * 0.55); bd.quadTo(-hr * 0.4, hr * 0.55, -hr * 0.8, hr * 0.1); bd.close()
    c.drawPath(bd, paint((90, 60, 40))); c.drawPath(bd, stroke(INK, 4))
    c.drawArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 190, 160, False, stroke((90, 60, 40), 14))
    for sx in (-1, 1):
        c.drawCircle(sx * hr * 0.4, -hr * 0.12, hr * 0.3, stroke(INK, 4))
    c.drawLine(-hr * 0.1, -hr * 0.12, hr * 0.1, -hr * 0.12, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(-hr * 0.9, -hr * 0.62, hr * 1.8, 16), 8, 8, paint((60, 60, 70)))
    c.drawCircle(hr * 0.62, -hr * 0.56, 12, paint(LAMP))
    c.restore(); c.restore()
    return r


def rescuer(c, x, y, s, pose, face, t, flip=False, col=(255, 255, 255)):
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=None, flip=flip)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s)
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    hp = skia.Path(); hp.addArc(R.MakeXYWH(-hr * 1.05, -hr * 1.1, hr * 2.1, hr * 2.0), 180, 180); hp.close()
    c.drawPath(hp, paint(RED)); c.drawPath(hp, stroke(INK, 5))
    c.drawCircle(0, -hr * 0.6, 14, paint(LAMP))
    c.drawCircle(0, -hr * 0.6, 60, paint(LAMP, 0.25, blur=20))
    c.restore(); c.restore()
    return r


# ------------------------------------------------------------------ cave sets
def stalactites(c, y0, n=14, seed=3, hmin=60, hmax=220, col=ROCK_D, x0=-40, x1=W + 40):
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n + (hsh(i, seed) - 0.5) * 60
        h = hmin + (hmax - hmin) * hsh(i, seed + 1); w = 30 + 50 * hsh(i, seed + 2)
        p = poly([(x - w, y0 - 10), (x + w, y0 - 10), (x + w * 0.1, y0 + h)], True)
        c.drawPath(p, paint(col))
        c.drawPath(p, stroke(INK, 4))
        c.drawLine(x - w * 0.5, y0 + 10, x - w * 0.2, y0 + h * 0.55, stroke(ROCK_L, 4, 0.5))


def stalagmites(c, y1, n=9, seed=7, hmin=50, hmax=160, col=ROCK):
    for i in range(n):
        x = W * (i + 0.5) / n + (hsh(i, seed) - 0.5) * 90
        h = hmin + (hmax - hmin) * hsh(i, seed + 1); w = 26 + 40 * hsh(i, seed + 2)
        p = poly([(x - w, y1 + 10), (x + w, y1 + 10), (x + w * 0.1, y1 - h)], True)
        c.drawPath(p, paint(col)); c.drawPath(p, stroke(INK, 4))


def cave_bg(c, t, lamp=(540, 1150), lamp_a=0.55, floor=1420, dark=0.0, teal=0.0):
    """Cave chamber: purple rock walls, a warm lamp glow in the middle, drips and depth-of-field dust."""
    top = mix((44, 32, 70), (6, 4, 16), dark); bot = mix((90, 70, 120), (16, 10, 30), dark)
    top = mix(top, (10, 60, 70), teal); bot = mix(bot, (20, 110, 110), teal)
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(top), argb(bot)])))
    # wall texture blobs
    for i in range(26):
        x = hsh(i, 11) * W; y = hsh(i, 12) * floor
        r = 80 + 220 * hsh(i, 13)
        c.drawOval(R.MakeXYWH(x - r, y - r * 0.6, 2 * r, 1.2 * r), paint(mix(ROCK_L, top, 0.6), 0.18 + 0.1 * hsh(i, 14), blur=r * 0.3))
    if lamp:
        lx, ly = lamp
        c.drawCircle(lx, ly, 760, paint(shader=rad(lx, ly, 760, [argb(LAMP, lamp_a), argb(LAMP, lamp_a * 0.35), argb(LAMP, 0)], [0, 0.4, 1])))
    stalactites(c, 0, n=13, seed=3)
    stalactites(c, -20, n=7, seed=9, hmin=180, hmax=360, col=mix(ROCK_D, (0, 0, 0), 0.3), x0=-100, x1=W + 100)
    # floor
    c.drawRect(R.MakeLTRB(0, floor, W, H), paint(shader=lin(0, floor, 0, H, [argb(mix(ROCK, (0, 0, 0), 0.15)), argb(mix(ROCK_D, (0, 0, 0), 0.35))])))
    c.drawLine(0, floor, W, floor, stroke(INK, 5))
    stalagmites(c, floor + 2, n=8, seed=7, hmin=30, hmax=110, col=mix(ROCK, (0, 0, 0), 0.1))
    for i in range(10):
        x = hsh(i, 21) * W; r = 14 + 30 * hsh(i, 22)
        c.drawOval(R.MakeXYWH(x - r, floor + 40 + hsh(i, 23) * 300 - r * 0.4, 2 * r, r * 0.8), paint(ROCK_L, 0.5)); c.drawOval(R.MakeXYWH(x - r, floor + 40 + hsh(i, 23) * 300 - r * 0.4, 2 * r, r * 0.8), stroke(INK, 3))
    # drips
    for i in range(6):
        x = 120 + i * 170 + hsh(i, 31) * 60
        ph = (t * (0.5 + 0.5 * hsh(i, 32)) + hsh(i, 33)) % 1.0
        y = 180 + ph * (floor - 180)
        c.drawOval(R.MakeXYWH(x - 4, y - 12, 8, 24), paint((170, 210, 255), 0.75 * (1 - ph * 0.5)))
        if ph > 0.97: c.drawOval(R.MakeXYWH(x - 30, floor - 6, 60, 12), stroke((170, 210, 255), 3, 0.7))
    fg_dust(c, t, n=8, seed=5, a=0.25, col=LAMP)


def camp(c, x, y, s, t, lamp_on=True):
    """Beatriz's camp: dome tent, camp lamp, crate of books, mat."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-260, -20, 520, 50), paint((0, 0, 0), 0.25, blur=8))
    tent = skia.Path(); tent.moveTo(-230, 0); tent.quadTo(-200, -230, 0, -240); tent.quadTo(200, -230, 230, 0); tent.close()
    c.drawPath(tent, paint(ORANGE)); c.drawPath(tent, stroke(INK, 7))
    door = skia.Path(); door.moveTo(-70, 0); door.quadTo(-70, -150, 0, -160); door.quadTo(70, -150, 70, 0); door.close()
    c.drawPath(door, paint((120, 60, 20))); c.drawPath(door, stroke(INK, 6))
    c.drawLine(-230, 0, 230, 0, stroke(INK, 7))
    c.drawLine(0, -240, 0, -160, stroke(INK, 4))
    # lamp on a hook
    c.drawLine(250, -30, 250, -210, stroke((90, 90, 100), 10)); c.drawLine(250, -30, 250, -210, stroke(INK, 3, 0.4))
    c.drawRoundRect(R.MakeXYWH(228, -220, 44, 20), 6, 6, paint((80, 80, 90))); c.drawRoundRect(R.MakeXYWH(228, -220, 44, 20), 6, 6, stroke(INK, 4))
    c.drawRoundRect(R.MakeXYWH(222, -200, 56, 70), 14, 14, paint(LAMP if lamp_on else (120, 120, 130))); c.drawRoundRect(R.MakeXYWH(222, -200, 56, 70), 14, 14, stroke(INK, 5))
    if lamp_on:
        c.drawCircle(250, -165, 110, paint(LAMP, 0.35, blur=30))
    # crate of books
    c.drawRoundRect(R.MakeXYWH(-420, -90, 150, 90), 10, 10, paint((150, 105, 60))); c.drawRoundRect(R.MakeXYWH(-420, -90, 150, 90), 10, 10, stroke(INK, 6))
    for i, col in enumerate([(220, 70, 60), (60, 120, 200), (240, 190, 70), (80, 160, 100), (150, 90, 170)]):
        c.drawRect(R.MakeXYWH(-410 + i * 27, -150 + 10 * hsh(i, 4), 22, 70), paint(col)); c.drawRect(R.MakeXYWH(-410 + i * 27, -150 + 10 * hsh(i, 4), 22, 70), stroke(INK, 4))
    c.restore()


def rope(c, x, y0, y1, sway=0.0, t=0.0):
    p = skia.Path(); p.moveTo(x, y0)
    p.quadTo(x + 30 * math.sin(t * 1.5) * sway, (y0 + y1) / 2, x + 14 * math.sin(t * 1.5) * sway, y1)
    c.drawPath(p, stroke((200, 170, 110), 10)); c.drawPath(p, stroke(INK, 3, 0.35))
    for k in range(int(abs(y1 - y0) / 34)):
        yy = y0 + k * 34 + 10
        c.drawLine(x - 6, yy, x + 6, yy + 8, stroke(INK, 2.5, 0.5))


def bucket(c, x, y, s, t, kind='food'):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = poly([(-70, -60), (70, -60), (56, 70), (-56, 70)], True)
    c.drawPath(p, paint((110, 120, 140))); c.drawPath(p, stroke(INK, 6))
    c.drawArc(R.MakeXYWH(-74, -120, 148, 120), 200, 140, False, stroke(INK, 6))
    if kind == 'food':
        c.drawOval(R.MakeXYWH(-50, -110, 50, 70), paint((90, 150, 60))); c.drawOval(R.MakeXYWH(-50, -110, 50, 70), stroke(INK, 4))     # avocado
        c.drawOval(R.MakeXYWH(5, -100, 36, 46), paint((250, 240, 220))); c.drawOval(R.MakeXYWH(5, -100, 36, 46), stroke(INK, 4))         # egg
        c.drawOval(R.MakeXYWH(30, -96, 36, 46), paint((250, 240, 220))); c.drawOval(R.MakeXYWH(30, -96, 36, 46), stroke(INK, 4))
    else:
        c.drawRoundRect(R.MakeXYWH(-54, -96, 108, 50), 14, 14, paint((70, 60, 70))); c.drawRoundRect(R.MakeXYWH(-54, -96, 108, 50), 14, 14, stroke(INK, 4))
        for i in range(3):
            yy = -100 - 20 * ((t * 0.8 + i * 0.33) % 1); c.drawPath(_wave(i * 30 - 30, yy), stroke((160, 160, 170), 4, 0.7))
    c.restore()


def _wave(x, y):
    p = skia.Path(); p.moveTo(x - 10, y + 10); p.quadTo(x - 5, y, x, y + 5); p.quadTo(x + 5, y + 10, x + 10, y); return p


def cave_mouth(c, t, k_down=0.0):
    """Night hillside with the cave entrance; Beatriz descends a ladder as k_down goes 0->1."""
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, 1200, [argb(SKY_N[0]), argb(SKY_N[1])])))
    for i in range(120):
        x = hsh(i, 1) * W; y = hsh(i, 2) * 900
        c.drawCircle(x, y, 1 + 2 * hsh(i, 3) ** 3, paint((255, 255, 255), 0.5 + 0.5 * math.sin(t * 2 + i)))
    c.drawCircle(860, 300, 90, paint((255, 245, 210))); c.drawCircle(860, 300, 90, stroke(INK, 5)); c.drawCircle(860, 300, 220, paint((255, 245, 210), 0.15, blur=40))
    # hills
    for (yb, col, amp, sd) in ((980, (34, 70, 60), 80, 4), (1080, (26, 54, 48), 60, 8)):
        p = skia.Path(); p.moveTo(-50, H)
        for i in range(0, 46):
            x = -50 + i * 26; p.lineTo(x, yb - amp * (0.5 + 0.5 * math.sin(x * 0.006 + sd)) - 20 * math.sin(x * 0.02 + sd))
        p.lineTo(W + 50, H); p.close(); c.drawPath(p, paint(col)); c.drawPath(p, stroke(INK, 5))
    # trees
    for i in range(7):
        x = 60 + i * 170 + hsh(i, 5) * 50; y = 1010 - 20 * math.sin(x * 0.006 + 4)
        for j in range(3):
            w = 60 - j * 14; yy = y - j * 50
            p = poly([(x - w, yy), (x + w, yy), (x, yy - 80)], True); c.drawPath(p, paint((30, 90, 70))); c.drawPath(p, stroke(INK, 4))
    # ground + hole
    c.drawRect(R.MakeLTRB(0, 1120, W, H), paint(shader=lin(0, 1120, 0, H, [argb((96, 80, 70)), argb((60, 46, 44))])))
    c.drawLine(0, 1120, W, 1120, stroke(INK, 5))
    hole = skia.Path(); hole.addOval(R.MakeXYWH(300, 1090, 480, 120))
    c.drawPath(hole, paint((8, 6, 14))); c.drawPath(hole, stroke(INK, 7))
    c.drawOval(R.MakeXYWH(330, 1105, 420, 90), paint(shader=rad(540, 1150, 220, [argb(LAMP, 0.35), argb(LAMP, 0)])))
    for sx in (-1, 1):
        c.drawLine(540 + sx * 70, 1100, 540 + sx * 70, 1190, stroke((200, 170, 110), 10))
    for k in range(3):
        c.drawLine(470, 1110 + k * 28, 610, 1110 + k * 28, stroke((200, 170, 110), 8))
    # depth label
    f = font('ant', 50); s_ = '70 M DOWN'
    c.drawString(s_, 820 - f.measureText(s_) / 2, 1290, f, paint(YEL))
    c.drawLine(760, 1230, 760, 1300, stroke(YEL, 6)); c.drawPath(poly([(760, 1320), (745, 1296), (775, 1296)], True), paint(YEL))


# ------------------------------------------------------------------ explainer props
def body_clock(c, x, y, s, t, k_drift=0.0, hours=24, hand_speed=1.0, glow=False):
    """A clock face with 24 ticks; k_drift smears the hand (the body clock drifting)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 230, paint(RED)); c.drawCircle(0, 0, 230, stroke(INK, 8))
    c.drawCircle(0, 0, 196, paint((255, 250, 240))); c.drawCircle(0, 0, 196, stroke(INK, 6))
    f = font('ant', 36)
    for i in range(hours):
        a = math.radians(-90 + 360 * i / hours)
        c.drawLine(math.cos(a) * 168, math.sin(a) * 168, math.cos(a) * 186, math.sin(a) * 186, stroke(INK, 5 if i % 6 else 9))
        if i % 6 == 0:
            lab = str(hours if i == 0 else i)
            c.drawString(lab, math.cos(a) * 140 - f.measureText(lab) / 2, math.sin(a) * 140 + 13, f, paint(INK))
    a = math.radians(-90 + t * 60 * hand_speed)
    if k_drift > 0:
        for j in range(6):
            aa = a - j * 0.12 * k_drift
            c.drawLine(0, 0, math.cos(aa) * 150, math.sin(aa) * 150, stroke(RED, 14, 0.35 * (1 - j / 6)))
    c.drawLine(0, 0, math.cos(a) * 150, math.sin(a) * 150, stroke(INK, 14))
    c.drawCircle(0, 0, 16, paint(INK))
    if glow: c.drawCircle(0, 0, 300, paint(YEL, 0.25, blur=50))
    c.restore()


def sun_icon(c, x, y, r, t, a=1.0):
    c.drawCircle(x, y, r * 1.8, paint(YEL, 0.3 * a, blur=r * 0.6))
    for i in range(12):
        ang = math.radians(i * 30 + t * 20)
        c.drawLine(x + math.cos(ang) * r * 1.2, y + math.sin(ang) * r * 1.2, x + math.cos(ang) * r * 1.6, y + math.sin(ang) * r * 1.6, stroke(YEL, 9, a))
    c.drawCircle(x, y, r, paint(YEL, a)); c.drawCircle(x, y, r, stroke(INK, 6, a))


def head_with_clock(c, x, y, s, t, drift=0.0, hand_speed=1.0):
    """Big mascot head in profile with a clock inside the brain."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 230, paint((255, 255, 255))); c.drawCircle(0, 0, 230, stroke(INK, 9))
    c.drawCircle(190, 20, 18, paint(INK))
    p = skia.Path(); p.moveTo(170, 90); p.quadTo(200, 110, 230, 95); c.drawPath(p, stroke(INK, 7))
    brain(c, -20, -40, 0.42, t)
    body_clock(c, -20, -40, 0.34, t, k_drift=drift, hand_speed=hand_speed)
    c.restore()


def texas_sign(c, x, y, s, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * eback(k, 1.6), s * eback(k, 1.6))
    c.drawLine(0, 0, 0, 120, stroke((120, 90, 50), 12)); c.drawLine(0, 0, 0, 120, stroke(INK, 3, 0.4))
    c.drawRoundRect(R.MakeXYWH(-150, -70, 300, 90), 14, 14, paint((240, 200, 100))); c.drawRoundRect(R.MakeXYWH(-150, -70, 300, 90), 14, 14, stroke(INK, 6))
    f = font('ant', 50); s_ = 'TEXAS 1972'; c.drawString(s_, -f.measureText(s_) / 2, -8, f, paint(INK))
    c.restore()


def tally_wall(c, x, y, s, n, k=1.0, col=(250, 240, 220)):
    """Chalk tally marks on the rock wall, up to n."""
    c.save(); c.translate(x, y); c.scale(s, s)
    for i in range(min(n, 100)):
        g = i // 5; j = i % 5
        gx = (g % 7) * 90; gy = (g // 7) * 90
        if j < 4:
            c.drawLine(gx + j * 16, gy, gx + j * 16 + 4, gy + 60, stroke(col, 6, k))
        else:
            c.drawLine(gx - 8, gy + 48, gx + 60, gy + 10, stroke(col, 6, k))
    c.restore()


def chalk_text(c, x, y, s, size=90, k=1.0, col=(250, 240, 220)):
    f = font('ant', size); c.drawString(s, x - f.measureText(s) / 2, y, f, paint(col, k))


def stopwatch_count(c, x, y, s, number, t, col=RED):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-30, -300, 60, 50), 10, 10, paint((90, 90, 100))); c.drawRoundRect(R.MakeXYWH(-30, -300, 60, 50), 10, 10, stroke(INK, 5))
    c.drawCircle(0, 0, 250, paint(col)); c.drawCircle(0, 0, 250, stroke(INK, 8))
    c.drawCircle(0, 0, 205, paint((255, 255, 255))); c.drawCircle(0, 0, 205, stroke(INK, 6))
    for i in range(12):
        a = math.radians(i * 30 - 90); c.drawLine(math.cos(a) * 180, math.sin(a) * 180, math.cos(a) * 196, math.sin(a) * 196, stroke(INK, 5))
    a = math.radians(-90 + t * 6 * 60 / 60 * 6)
    c.drawLine(0, 0, math.cos(a) * 170, math.sin(a) * 170, stroke(col, 8))
    f = font('ant', 120); s_ = str(number); c.drawString(s_, -f.measureText(s_) / 2, 45, f, paint(INK))
    c.restore()


def big_number_bar(c, x, y, w, k, label, col, text_col=INK, h=110):
    """Horizontal bar growing to k of w with a label at the end."""
    c.drawRoundRect(R.MakeXYWH(x, y - h / 2, w, h), h / 2, h / 2, paint((255, 255, 255), 0.25))
    c.drawRoundRect(R.MakeXYWH(x, y - h / 2, w, h), h / 2, h / 2, stroke(INK, 5))
    ww = max(h, w * k)
    c.drawRoundRect(R.MakeXYWH(x, y - h / 2, ww, h), h / 2, h / 2, paint(col)); c.drawRoundRect(R.MakeXYWH(x, y - h / 2, ww, h), h / 2, h / 2, stroke(INK, 5))
    f = font('ant', int(h * 0.62)); c.drawString(label, x + ww - f.measureText(label) - 28, y + h * 0.22, f, paint(text_col))


def book(c, x, y, s, rot=0.0, col=(60, 120, 200), open_=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if open_:
        for sx in (-1, 1):
            p = skia.Path(); p.moveTo(0, -40); p.quadTo(sx * 60, -56, sx * 120, -40); p.lineTo(sx * 120, 50); p.quadTo(sx * 60, 36, 0, 50); p.close()
            c.drawPath(p, paint((255, 250, 240))); c.drawPath(p, stroke(INK, 5))
            for j in range(4): c.drawLine(sx * 20, -20 + j * 16, sx * 100, -24 + j * 16, stroke((150, 150, 160), 3))
    else:
        c.drawRoundRect(R.MakeXYWH(-50, -70, 100, 140), 6, 6, paint(col)); c.drawRoundRect(R.MakeXYWH(-50, -70, 100, 140), 6, 6, stroke(INK, 5))
        c.drawRect(R.MakeXYWH(-50, -70, 16, 140), paint(mix(col, (0, 0, 0), 0.3))); c.drawLine(-34, -70, -34, 70, stroke(INK, 3))
    c.restore()


def knit_hat(c, x, y, s, col=(230, 80, 90)):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.addArc(R.MakeXYWH(-70, -70, 140, 140), 180, 180); p.close()
    c.drawPath(p, paint(col)); c.drawPath(p, stroke(INK, 5))
    c.drawRoundRect(R.MakeXYWH(-76, -10, 152, 34), 10, 10, paint(mix(col, (255, 255, 255), 0.3))); c.drawRoundRect(R.MakeXYWH(-76, -10, 152, 34), 10, 10, stroke(INK, 5))
    c.drawCircle(0, -74, 18, paint((255, 255, 255))); c.drawCircle(0, -74, 18, stroke(INK, 4))
    for i in range(4): c.drawLine(-50 + i * 32, -50, -40 + i * 32, -12, stroke(INK, 2.5, 0.4))
    c.restore()


def dumbbell(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawLine(-70, 0, 70, 0, stroke((90, 90, 100), 14)); c.drawLine(-70, 0, 70, 0, stroke(INK, 3, 0.4))
    for sx in (-1, 1):
        c.drawRoundRect(R.MakeXYWH(sx * 90 - 22, -40, 44, 80), 8, 8, paint((60, 60, 70))); c.drawRoundRect(R.MakeXYWH(sx * 90 - 22, -40, 44, 80), 8, 8, stroke(INK, 5))
    c.restore()


def flies(c, t, n, cx, cy, spread, k=1.0, seed=9):
    """Swarm of flies around (cx, cy)."""
    if k <= 0: return
    for i in range(n):
        ph = hsh(i, seed) * 6.283; r = spread * (0.2 + 0.8 * hsh(i, seed + 1)) * k
        x = cx + math.cos(t * (3 + 4 * hsh(i, seed + 2)) + ph) * r + math.sin(t * 7 + i) * 12
        y = cy + math.sin(t * (2.5 + 3 * hsh(i, seed + 3)) + ph * 2) * r * 0.8
        c.drawOval(R.MakeXYWH(x - 7, y - 4, 14, 9), paint(INK))
        w = math.sin(t * 60 + i) * 6
        c.drawOval(R.MakeXYWH(x - 10, y - 10 + w, 9, 7), paint((200, 220, 255), 0.7)); c.drawOval(R.MakeXYWH(x + 1, y - 10 - w, 9, 7), paint((200, 220, 255), 0.7))


def phone(c, x, y, s, t, k_scroll=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-110, -200, 220, 400), 30, 30, paint((30, 30, 40))); c.drawRoundRect(R.MakeXYWH(-110, -200, 220, 400), 30, 30, stroke(INK, 7))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-96, -184, 192, 368), 20, 20), skia.ClipOp.kIntersect, True)
    c.drawRect(R.MakeXYWH(-96, -184, 192, 368), paint((245, 245, 250)))
    off = (t * 180 * k_scroll) % 140
    for i in range(5):
        yy = -184 + i * 140 - off
        c.drawRoundRect(R.MakeXYWH(-80, yy + 10, 160, 90), 12, 12, paint([(255, 120, 120), (120, 180, 255), (255, 200, 90), (140, 220, 140), (200, 150, 255)][i]))
        c.drawRoundRect(R.MakeXYWH(-80, yy + 108, 110, 14), 7, 7, paint((200, 200, 210)))
    c.restore()
    c.restore()


def astronaut_window(c, x, y, s, t):
    """Space station window with Earth outside and an astronaut stick floating."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-240, -240, 480, 480), 80, 80, paint((200, 205, 215))); c.drawRoundRect(R.MakeXYWH(-240, -240, 480, 480), 80, 80, stroke(INK, 8))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-200, -200, 400, 400), 60, 60), skia.ClipOp.kIntersect, True)
    c.drawRect(R.MakeXYWH(-200, -200, 400, 400), paint((8, 10, 30)))
    for i in range(40): c.drawCircle(-200 + hsh(i, 3) * 400, -200 + hsh(i, 4) * 400, 1.5 + hsh(i, 5) * 2, paint((255, 255, 255), 0.8))
    draw_planet(c, 'earth', 60, 260, 260, rot=t * 0.05, glow=(120, 180, 255))
    c.restore()
    c.drawRoundRect(R.MakeXYWH(-200, -200, 400, 400), 60, 60, stroke(INK, 6))
    c.restore()
