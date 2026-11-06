"""Props for 'What if you couldn't stop sneezing?' (episode 36: Donna Griffiths 1981-83, Dundee windpipe case 2023, sneeze science)."""
import math
import skia
from toon import *
from props import cam, check_icon, cross_icon, tree
from volcanoprops import calendar
from whaleprops import card3d, comment_bubble
from spinprops import gauge, speed_lines, car
from meteorprops import speech, bed, blanket, medal
from hicprops import brain
from caveprops import sun_icon

YEL = (255, 210, 70); RED = (235, 70, 60); PURP = (150, 80, 220); TEAL = (40, 190, 180); PINK = (255, 120, 170)
SKY = (120, 200, 255); MINT = (120, 230, 170); ORANGE = (255, 140, 40); BLUE = (60, 120, 230)
SNOT = (170, 225, 255)

# extra poses (lean head uaL faL uaR faR thL shL thR shR)
P_PRE = (-12, -18, 225, 30, 135, -30, 188, 0, 172, 0)        # head back: ah... ah...
P_BLAST = (16, 16, 205, 30, 155, -30, 184, 0, 176, 0)        # choo! folded forward
P_PINCH = (0, 0, 200, 10, 60, -126, 186, 0, 174, 0)          # right hand up at nose
P_SIT_PINCH = (-4, 0, 150, -40, 60, -126, 95, 95, 85, 95)
P_SIT_DRIVE = (-4, 0, 150, -40, 140, -50, 95, 95, 85, 95)
P_ELBOW = (6, 10, 200, 10, 70, -150, 186, 0, 174, 0)         # sneeze into elbow


def donna(c, x, y, s, pose, face, t, flip=False, prop=None, squash=1.0, a=1.0):
    """Original girl character: high ponytail with a purple band, purple scarf."""
    r = draw_stick(c, x, y, s, pose, face, t=t, scarf=PURP, flip=flip, prop=prop, squash=squash, a=a)
    P = rig_points(pose)
    c.save(); c.translate(x, y); c.scale(-s if flip else s, s * squash)
    hdx, hdy = P['head']; lean = pose[0] + pose[1]
    c.save(); c.translate(hdx, hdy); c.rotate(lean)
    hr = LEN['head']
    sw = 10 * math.sin(t * 3)
    tail = skia.Path(); tail.moveTo(-hr * 0.55, -hr * 0.8)
    tail.cubicTo(-hr * 1.6, -hr * 1.1 + sw, -hr * 1.9, hr * 0.2, -hr * 1.35 + sw * 0.5, hr * 0.9)
    tail.cubicTo(-hr * 1.2, hr * 0.1, -hr * 1.0, -hr * 0.5, -hr * 0.45, -hr * 0.62); tail.close()
    c.drawPath(tail, paint((70, 46, 30))); c.drawPath(tail, stroke(INK, 4))
    c.drawCircle(-hr * 0.62, -hr * 0.78, 12, paint(PURP)); c.drawCircle(-hr * 0.62, -hr * 0.78, 12, stroke(INK, 3))
    fr = skia.Path(); fr.addArc(R.MakeXYWH(-hr * 1.02, -hr * 1.02, hr * 2.04, hr * 2.04), 200, 140)
    c.drawPath(fr, stroke((70, 46, 30), 13))
    c.restore()
    c.restore()
    return r


def face_pt(x, y, s, pose, flip=False):
    """screen point of the mouth for a figure drawn at x,y,s."""
    P = rig_points(pose)
    hx, hy = P['head']; lean = math.radians(pose[0] + pose[1])
    mx, my = hx - math.sin(lean) * -16, hy + math.cos(lean) * 16
    return x + (-mx if flip else mx) * s, y + my * s


def achoo(c, x, y, s, k, t, dirx=1.0, diry=0.25, word='ACHOO!', col=YEL, seed=3):
    """sneeze blast: droplet cone + spiky burst word. k: 0..1 progress (0.0-0.15 pop, then droplets fly)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s)
    ang = math.atan2(diry, dirx)
    # droplets
    for i in range(40):
        a = ang + (hsh(i, seed) - 0.5) * 0.9
        d = (80 + 620 * hsh(i, seed + 1)) * eo(cl(k * 1.4 - 0.05 * hsh(i, 5)))
        r = 4 + 11 * hsh(i, seed + 2)
        al = 0.9 * (1 - cl((k - 0.6) / 0.4))
        c.drawCircle(math.cos(a) * d, math.sin(a) * d + 40 * k * k * hsh(i, 9), r, paint(SNOT, al))
    # mist cone
    cone = poly([(0, 0), (math.cos(ang - 0.38) * 520, math.sin(ang - 0.38) * 520), (math.cos(ang + 0.38) * 520, math.sin(ang + 0.38) * 520)], True)
    c.drawPath(cone, paint(shader=lin(0, 0, math.cos(ang) * 520, math.sin(ang) * 520, [argb((255, 255, 255), 0.3 * (1 - k)), argb((255, 255, 255), 0)])))
    # burst + word
    kk = eback(cl(k / 0.18), 1.8) * (1 - cl((k - 0.75) / 0.25))
    if kk > 0 and word:
        bs = min(1.0, s) * 0.62
        gx = x + math.copysign(1, dirx) * (150 + 220 * min(1.0, s)); gy = y - 250 * min(1.0, s)
        gx = min(max(gx, 80 + 215 * bs * 1.3), 960 - 215 * bs * 1.3)
        c.restore(); c.save(); c.translate(gx, gy); c.rotate(-8); c.scale(kk * bs, kk * bs)
        pts = []
        for i in range(24):
            rr = 210 if i % 2 == 0 else 150
            a = i / 24 * 6.283
            pts.append((math.cos(a) * rr * 1.3, math.sin(a) * rr * 0.8))
        st = poly(pts, True)
        c.drawPath(st, paint((0, 0, 0), 0.25, blur=8)); c.drawPath(st, paint(col)); c.drawPath(st, stroke(INK, 7))
        f = font('ant', 110 if len(word) < 8 else 84)
        c.drawString(word, -f.measureText(word) / 2, 38, f, stroke(INK, 14)); c.drawString(word, -f.measureText(word) / 2, 38, f, paint((255, 255, 255)))
        c.restore(); c.save()
    c.restore()


def sneezer(c, x, y, s, t, t0, who='donna', flip=False, base=None, face_base=None, word='ACHOO!', period=None):
    """character that does ah..ah..CHOO starting at t0. returns blast progress."""
    who_fn = donna if who == 'donna' else (lambda c_, x_, y_, s_, p, f, t_, flip=False: draw_stick(c_, x_, y_, s_, p, f, t=t_, flip=flip))
    base = base or POSES['stand']; face_base = face_base or Face('open', 'smile')
    u = t - t0
    if period: u = u % period if u > 0 else u
    if u < 0:
        who_fn(c, x, y, s, base, face_base, t, flip=flip); return 0.0
    if u < 0.55:
        k = eio(cl(u / 0.45))
        pose = lerp_pose(base, P_PRE, k)
        who_fn(c, x, y, s, pose, Face('closed', 'o', 'up'), t, flip=flip); return 0.0
    kb = cl((u - 0.55) / 0.9)
    pose = lerp_pose(P_BLAST, base, eio(cl((u - 0.85) / 0.6)))
    who_fn(c, x + (-1 if flip else 1) * 10 * math.sin(u * 60) * (1 - kb), y, s, pose, Face('closed', 'grin', 'angry') if kb < 0.5 else Face('wide', 'flat', 'worried'), t, flip=flip)
    mx, my = face_pt(x, y, s, P_BLAST, flip)
    achoo(c, mx, my, s / 1.4, kb, t, dirx=-1 if flip else 1, word=word)
    return kb


def counter(c, x, y, s, n, t, col=RED, digits=7, label=None):
    """odometer counter box with comma groups."""
    txt = f'{int(n):,}'
    c.save(); c.translate(x, y); c.scale(s, s)
    f = font('ant', 150)
    w = max(f.measureText('0,000,000'), f.measureText(txt)) + 80
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 6, -110 + 12, w, 200), 34, 34, paint((0, 0, 0), 0.3, blur=8))
    c.drawRoundRect(R.MakeXYWH(-w / 2, -110, w, 200), 34, 34, paint(INK))
    c.drawRoundRect(R.MakeXYWH(-w / 2 + 16, -94, w - 32, 168), 24, 24, paint((40, 40, 52)))
    c.drawString(txt, -f.measureText(txt) / 2, 46, f, paint(col))
    if label:
        f2 = font('mbk', 44); c.drawString(label, -f2.measureText(label) / 2, 150, f2, paint((255, 255, 255)))
    c.restore()


def tissue_box(c, x, y, s, t, k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRoundRect(R.MakeXYWH(-120, -110, 240, 120), 14, 14, paint((90, 160, 240))); c.drawRoundRect(R.MakeXYWH(-120, -110, 240, 120), 14, 14, stroke(INK, 6))
    for i in range(4):
        c.drawCircle(-80 + i * 54, -50, 12, paint((255, 255, 255), 0.6))
    tp = skia.Path(); sw = 8 * math.sin(t * 4)
    tp.moveTo(-40, -108); tp.cubicTo(-60, -170, -10 + sw, -220, 10 + sw, -230); tp.cubicTo(30, -200, 50, -160, 40, -108); tp.close()
    c.drawPath(tp, paint((255, 255, 255))); c.drawPath(tp, stroke(INK, 5))
    c.restore()


def tissue_pile(c, x, y, n, seed=4):
    for i in range(n):
        dx = (hsh(i, seed) - 0.5) * 60 * math.sqrt(n); dy = -hsh(i, seed + 1) * 12 * math.sqrt(n)
        r = 34 + 12 * hsh(i, seed + 2)
        p = skia.Path()
        for j in range(9):
            a = j / 9 * 6.283
            rr = r * (0.8 + 0.3 * hsh(i * 9 + j, 7))
            (p.moveTo if j == 0 else p.lineTo)(x + dx + math.cos(a) * rr, y + dy + math.sin(a) * rr * 0.75)
        p.close(); c.drawPath(p, paint((255, 255, 255))); c.drawPath(p, stroke(INK, 4))


def soup(c, x, y, s, t, splash=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-150, -30, 300, 70), paint((255, 150, 60)))
    bowl = skia.Path(); bowl.moveTo(-160, 0); bowl.quadTo(-150, 150, 0, 150); bowl.quadTo(150, 150, 160, 0); bowl.close()
    c.drawPath(bowl, paint((255, 255, 255))); c.drawPath(bowl, stroke(INK, 6))
    c.drawOval(R.MakeXYWH(-160, -30, 320, 60), stroke(INK, 6))
    if splash > 0:
        for i in range(14):
            a = -math.pi / 2 + (hsh(i, 2) - 0.5) * 2.2
            d = 260 * eo(splash) * (0.5 + 0.5 * hsh(i, 3))
            c.drawCircle(math.cos(a) * d, -10 + math.sin(a) * d + 300 * splash * splash * 0.4, 10 + 8 * hsh(i, 4), paint((255, 150, 60), 1 - cl((splash - 0.7) / 0.3)))
    c.restore()


def homework(c, x, y, s, rot, k_fly=0.0):
    c.save(); c.translate(x + 300 * k_fly, y - 200 * k_fly); c.rotate(rot + 160 * k_fly); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-110, -140, 220, 280), paint((255, 255, 255))); c.drawRect(R.MakeXYWH(-110, -140, 220, 280), stroke(INK, 5))
    for i in range(6):
        c.drawLine(-80, -90 + i * 40, 60 - 30 * (i % 2), -90 + i * 40, stroke((120, 150, 220), 6))
    c.drawString('2+2=', -80, -100, font('mbk', 40), paint(RED))
    c.restore()


def sofa(c, x, y, s, col=(230, 90, 110)):
    c.save(); c.translate(x, y); c.scale(s, s)
    dk = tuple(int(v * 0.75) for v in col)
    c.drawRoundRect(R.MakeXYWH(-260, -240, 520, 170), 40, 40, paint(dk)); c.drawRoundRect(R.MakeXYWH(-260, -240, 520, 170), 40, 40, stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-300, -110, 600, 90), 30, 30, paint(col)); c.drawRoundRect(R.MakeXYWH(-300, -110, 600, 90), 30, 30, stroke(INK, 6))
    for sx in (-1, 1):
        c.drawRoundRect(R.MakeXYWH(sx * 300 - 50, -170, 100, 160), 40, 40, paint(col)); c.drawRoundRect(R.MakeXYWH(sx * 300 - 50, -170, 100, 160), 40, 40, stroke(INK, 6))
    c.drawRect(R.MakeXYWH(-250, -20, 30, 30), paint(INK)); c.drawRect(R.MakeXYWH(220, -20, 30, 30), paint(INK))
    c.restore()


def head_section(c, x, y, s, t, tickle=0.0, signal=0.0, alarm=0.0):
    """side-profile head (facing right): nose cavity, tickle speck, nerve line to the brain."""
    c.save(); c.translate(x, y); c.scale(s, s)
    skin = (255, 214, 180)
    hd = skia.Path()
    hd.moveTo(-60, 330); hd.lineTo(-40, 180); hd.cubicTo(-200, 150, -240, -60, -170, -200); hd.cubicTo(-90, -330, 150, -330, 210, -180)
    hd.cubicTo(240, -100, 230, -40, 250, 0)                          # forehead -> nose bridge
    hd.lineTo(330, 90); hd.quadTo(340, 115, 300, 120)                 # nose
    hd.lineTo(250, 125); hd.quadTo(270, 150, 255, 175); hd.quadTo(270, 200, 245, 225)  # lips
    hd.cubicTo(230, 270, 160, 290, 100, 270); hd.lineTo(90, 330); hd.close()
    c.drawPath(hd, paint(skin)); c.drawPath(hd, stroke(INK, 8))
    c.drawCircle(150, -40, 14, paint(INK))
    # nasal cavity
    cav = skia.Path(); cav.moveTo(160, 40); cav.cubicTo(220, 20, 280, 60, 300, 105); cav.lineTo(250, 110); cav.cubicTo(220, 80, 190, 75, 150, 80); cav.close()
    c.drawPath(cav, paint((240, 130, 140))); c.drawPath(cav, stroke(INK, 4))
    # brain
    c.save(); c.translate(-10, -150); c.scale(0.55, 0.5)
    c.drawOval(R.MakeXYWH(-220, -150, 440, 290), paint((255, 175, 190))); c.drawOval(R.MakeXYWH(-220, -150, 440, 290), stroke(INK, 9))
    for i in range(6):
        q = skia.Path(); q.moveTo(-160 + i * 60, -110); q.cubicTo(-130 + i * 60, -30, -180 + i * 60, 30, -150 + i * 60, 100)
        c.drawPath(q, stroke((220, 120, 140), 8))
    if alarm > 0:
        c.drawOval(R.MakeXYWH(-240, -170, 480, 330), paint((255, 60, 60), 0.35 * alarm * (0.6 + 0.4 * math.sin(t * 18)), blur=20))
    c.restore()
    # tickle speck (pollen) + feather
    if tickle > 0:
        for i in range(5):
            px = 330 - 120 * eo(tickle) + 10 * math.sin(t * 6 + i); py = 100 + (hsh(i, 3) - 0.5) * 40
            c.drawCircle(px + i * 14, py, 7, paint(YEL)); c.drawCircle(px + i * 14, py, 7, stroke(INK, 2))
    # nerve
    nv = skia.Path(); nv.moveTo(190, 70); nv.cubicTo(140, 0, 80, -60, 30, -120)
    c.drawPath(nv, stroke((255, 230, 120), 9, 0.9))
    if signal > 0:
        for i in range(3):
            ph_ = (signal * 1.4 - i * 0.18)
            if 0 < ph_ < 1:
                meas = skia.PathMeasure(nv, False); pos, _ = meas.getPosTan(meas.getLength() * ph_)
                c.drawCircle(pos.x(), pos.y(), 18, paint((255, 255, 160), 0.5, blur=8)); c.drawCircle(pos.x(), pos.y(), 9, paint((255, 250, 200)))
    c.restore()


def jogger(c, x, y, s, t, col=MINT):
    draw_stick(c, x, y, s, walk_pose(t * 1.6, 1.0, run=True), Face('happy', 'grin'), t=t, scarf=col)


def race_car(c, x, y, s, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = poly([(-200, -10), (-190, -60), (-60, -70), (-20, -110), (60, -110), (100, -70), (200, -50), (210, -10)], True)
    c.drawPath(body, paint(RED)); c.drawPath(body, stroke(INK, 7))
    c.drawPath(poly([(-10, -100), (50, -100), (80, -70), (-30, -70)], True), paint((190, 230, 255)))
    c.drawRect(R.MakeXYWH(-215, -110, 40, 60), paint(INK))
    c.drawCircle(-30, -50, 30, paint((255, 255, 255))); f = font('ant', 40); c.drawString('1', -40, -36, f, paint(INK))
    for wx in (-120, 130):
        c.drawCircle(wx, -8, 38, paint(INK)); c.drawCircle(wx, -8, 16, paint((200, 200, 210)))
    c.restore()


def droplet_cloud(c, cx, cy, k, t, spread=1.0, seed=6, a=1.0):
    for i in range(60):
        dx = (hsh(i, seed) - 0.5) * 520 * spread * (0.3 + 0.7 * k) + 260 * k * spread
        dy = (hsh(i, seed + 1) - 0.5) * 260 * (0.4 + 0.6 * k) + 12 * math.sin(t * 1.3 + i)
        r = 5 + 9 * hsh(i, seed + 2)
        c.drawCircle(cx + dx, cy + dy, r, paint(SNOT, a * (0.6 + 0.4 * hsh(i, 4))))
        c.drawCircle(cx + dx, cy + dy, r, stroke((60, 120, 200), 2, a * 0.6))
    c.drawOval(R.MakeXYWH(cx - 300 * spread + 260 * k * spread, cy - 140, 600 * spread, 280), paint(SNOT, 0.3 * a, blur=30))


def car_side(c, x, y, s, t, inner=None):
    """big side view of a small car with an open window; inner(c) draws the driver in local coords."""
    c.save(); c.translate(x, y); c.scale(s, s)
    win = skia.Path(); win.moveTo(-200, -200); win.lineTo(-130, -330); win.lineTo(150, -330); win.lineTo(230, -200); win.close()
    body = skia.Path(); body.addRoundRect(R.MakeXYWH(-380, -210, 760, 190), 60, 60)
    roof = skia.Path(); roof.moveTo(-240, -195); roof.lineTo(-150, -360); roof.lineTo(170, -360); roof.lineTo(270, -195); roof.close()
    c.drawPath(roof, paint((60, 140, 230))); c.drawPath(roof, stroke(INK, 7))
    c.drawPath(win, paint((200, 235, 255)))
    if inner:
        c.save(); c.clipPath(win, doAntiAlias=True); inner(c); c.restore()
    c.drawPath(win, stroke(INK, 6))
    c.drawLine(0, -330, 0, -200, stroke(INK, 10))
    c.drawPath(body, paint((60, 140, 230))); c.drawPath(body, stroke(INK, 7))
    c.drawRect(R.MakeXYWH(330, -170, 40, 30), paint(YEL)); c.drawRect(R.MakeXYWH(-370, -170, 30, 30), paint(RED))
    for wx in (-230, 230):
        c.drawCircle(wx, -20, 78, paint(INK)); c.drawCircle(wx, -20, 34, paint((200, 200, 210)))
        for i in range(4):
            a = t * 12 + i * 1.57
            c.drawLine(wx, -20, wx + math.cos(a) * 30, -20 + math.sin(a) * 30, stroke((90, 90, 100), 5))
    c.restore()


def windpipe(c, x, y, s, t, pressure=0.0, tear=0.0, swell=0.0, heal=0.0):
    """neck cut-out: the windpipe tube with rings; pressure arrows; a tiny tear with leaking air."""
    c.save(); c.translate(x, y); c.scale(s, s)
    sw = 1 + 0.18 * swell
    neck = skia.Path(); neck.addRoundRect(R.MakeXYWH(-230 * sw, -330, 460 * sw, 660), 120, 120)
    c.drawPath(neck, paint((255, 214, 180))); c.drawPath(neck, stroke(INK, 8))
    if swell > 0:
        for sx in (-1, 1):
            c.drawOval(R.MakeXYWH(sx * 200 * sw - 70, -120, 140, 240), paint((255, 150, 140), 0.5 * swell, blur=14))
    tube = R.MakeXYWH(-80, -360, 160, 720)
    c.drawRect(tube, paint((255, 170, 175)))
    for i in range(12):
        yy = -340 + i * 60
        c.drawRoundRect(R.MakeXYWH(-92, yy, 184, 30), 15, 15, paint((250, 250, 240))); c.drawRoundRect(R.MakeXYWH(-92, yy, 184, 30), 15, 15, stroke(INK, 4))
    c.drawLine(-80, -360, -80, 360, stroke(INK, 6)); c.drawLine(80, -360, 80, 360, stroke(INK, 6))
    if pressure > 0:
        for i in range(6):
            ph_ = (t * 2.2 + i / 6) % 1
            yy = 300 - ph_ * 560
            c.drawCircle(-30 + (i % 2) * 60, yy, 14 + 10 * pressure, paint((255, 255, 255), 0.75 * pressure))
        for sx in (-1, 1):
            for j in range(3):
                yy = -140 + j * 110
                ax = sx * (110 + 14 * math.sin(t * 20) * pressure)
                c.drawPath(poly([(ax, yy - 22), (ax + sx * 60, yy), (ax, yy + 22)], True), paint(RED, pressure))
    if tear > 0:
        hx, hy = 80, -40
        kk = eback(cl(tear * 2), 1.8) * (1 - heal)
        c.drawCircle(hx, hy, 30 * kk, paint((255, 60, 60), 0.5 * kk, blur=10)); c.drawCircle(hx, hy, 22 * kk, paint(INK))
        if heal < 1:
            for i in range(8):
                ph_ = (t * 1.5 + i / 8) % 1
                c.drawCircle(hx + 30 + ph_ * 150, hy + (hsh(i, 2) - 0.5) * 120 * ph_, 8 + 10 * ph_, stroke((255, 255, 255), 4, (1 - ph_) * cl(tear * 2) * (1 - heal)))
        if heal > 0:
            c.drawCircle(hx, hy, 34, paint((60, 210, 110), heal * 0.9)); check_icon(c, hx, hy, 0.5 * heal, (255, 255, 255))
    c.restore()


def tweezers(c, x, y, s, t, pluck=0.0):
    c.save(); c.translate(x, y); c.rotate(-30 + 6 * math.sin(pluck * 12)); c.scale(s, s)
    for sx in (-1, 1):
        c.drawPath(poly([(0, 0), (sx * 24, 200), (sx * 10, 200), (sx * 2, 20)], True), paint((200, 205, 215)))
        c.drawPath(poly([(0, 0), (sx * 24, 200), (sx * 10, 200), (sx * 2, 20)], True), stroke(INK, 4))
    c.restore()


def plate_big(c, x, y, s, k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(R.MakeXYWH(-210, -40, 420, 80), paint((255, 255, 255))); c.drawOval(R.MakeXYWH(-210, -40, 420, 80), stroke(INK, 6))
    for i in range(6):
        c.drawCircle(-100 + i * 40, -40 - 30 * math.sin(i * 0.9) * k, 40, paint([(255, 200, 80), (240, 120, 70), (120, 200, 90)][i % 3]))
        c.drawCircle(-100 + i * 40, -40 - 30 * math.sin(i * 0.9) * k, 40, stroke(INK, 4))
    c.restore()


def zzz(c, x, y, t, a=1.0):
    for i in range(3):
        ph_ = (t * 0.6 + i / 3) % 1
        f = font('ant', 50 + 30 * i)
        c.drawString('Z', x + i * 50 + 20 * ph_, y - i * 70 - 60 * ph_, f, paint((255, 255, 255), a * (1 - ph_)))


def trophy(c, x, y, s, k, label='976 DAYS'):
    if k <= 0: return
    kk = eback(min(1, k), 1.6)
    c.save(); c.translate(x, y); c.scale(s * kk, s * kk)
    gold = (255, 200, 50); dk = (220, 150, 30)
    cup = skia.Path(); cup.moveTo(-150, -300); cup.lineTo(150, -300); cup.cubicTo(150, -120, 80, -60, 0, -60); cup.cubicTo(-80, -60, -150, -120, -150, -300); cup.close()
    for sx in (-1, 1):
        c.drawArc(R.MakeXYWH(sx * 150 - 60, -280, 120, 140), 0, 360, False, stroke(INK, 26)); c.drawArc(R.MakeXYWH(sx * 150 - 60, -280, 120, 140), 0, 360, False, stroke(gold, 14))
    c.drawPath(cup, paint(gold)); c.drawPath(cup, stroke(INK, 8))
    c.drawRect(R.MakeXYWH(-24, -64, 48, 80), paint(dk)); c.drawRect(R.MakeXYWH(-24, -64, 48, 80), stroke(INK, 6))
    c.drawRoundRect(R.MakeXYWH(-130, 10, 260, 70), 12, 12, paint((70, 50, 40))); c.drawRoundRect(R.MakeXYWH(-130, 10, 260, 70), 12, 12, stroke(INK, 6))
    f = font('ant', 46); c.drawString(label, -f.measureText(label) / 2, 62, f, paint(gold))
    c.drawCircle(-60, -230, 18, paint((255, 255, 255), 0.6))
    c.restore()


def doorway(c, x, y, s, t, k_sun=1.0):
    """bright open door from a dark room."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(R.MakeXYWH(-160, -520, 320, 520), paint(shader=lin(0, -520, 0, 0, [argb((255, 245, 180), k_sun), argb((255, 210, 110), k_sun)])))
    c.drawRect(R.MakeXYWH(-160, -520, 320, 520), stroke(INK, 10))
    for i in range(7):
        a = math.radians(-60 + i * 20)
        c.drawPath(poly([(0, -260), (math.sin(a) * 900, -260 + math.cos(a) * 900 - 200), (math.sin(a + 0.12) * 900, -260 + math.cos(a + 0.12) * 900 - 200)], True),
                   paint((255, 240, 160), 0.18 * k_sun))
    c.restore()
