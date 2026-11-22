# ------------------------------------------------------------------ props (no real logos or trade dress: plain unbranded bottle, Santa is public domain)
def santa(c, x, y, s, t=0.0, mood='happy', suit=(220, 40, 50), arm_r=None, arm_l=None, look=(0, 0)):
    person(c, x, y, s, (255, 205, 170), suit, pants=(200, 35, 45), mood=mood, look=look, t=t, arm_r=arm_r, arm_l=arm_l, blink=blinking(t))
    hx, hy, r = x, y - 640 * s, 185 * s
    beard = skia.Path(); beard.moveTo(hx - r * 0.95, hy + r * 0.1); beard.cubicTo(hx - r * 0.9, hy + r * 1.5, hx + r * 0.9, hy + r * 1.5, hx + r * 0.95, hy + r * 0.1)
    beard.cubicTo(hx + r * 0.5, hy + r * 0.55, hx - r * 0.5, hy + r * 0.55, hx - r * 0.95, hy + r * 0.1); beard.close()
    inked(c, beard, P((255, 255, 255)), 6 * s / 0.6)
    c.drawCircle(hx, hy + r * 0.42, r * 0.16, P((150, 22, 34)))                                                 # mouth peeking through beard
    hat = skia.Path(); hat.moveTo(hx - r * 0.95, hy - r * 0.5); hat.cubicTo(hx - r * 0.6, hy - r * 1.6, hx + r * 0.9, hy - r * 1.7, hx + r * 1.3, hy - r * 0.9)
    hat.lineTo(hx + r * 0.95, hy - r * 0.5); hat.close(); inked(c, hat, P(suit), 6 * s / 0.6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(hx - r * 1.05, hy - r * 0.62, r * 2.1, r * 0.3), r * 0.14, r * 0.14), P((255, 255, 255)), 5 * s / 0.6)
    c.drawCircle(hx + r * 1.3, hy - r * 0.9, r * 0.2, P((255, 255, 255))); c.drawCircle(hx + r * 1.3, hy - r * 0.9, r * 0.2, S(INK, 4 * s / 0.6))
    c.drawRect(skia.Rect.MakeXYWH(x - 98 * s, y - 272 * s, 196 * s, 26 * s), P((30, 30, 30)))                    # belt
    c.drawRect(skia.Rect.MakeXYWH(x - 22 * s, y - 276 * s, 44 * s, 34 * s), P((255, 214, 40))); c.drawRect(skia.Rect.MakeXYWH(x - 22 * s, y - 276 * s, 44 * s, 34 * s), S(INK, 3))


def bottle(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = skia.Path(); b.moveTo(-22, -200); b.lineTo(22, -200); b.lineTo(24, -120); b.cubicTo(60, -80, 60, -20, 50, 20); b.cubicTo(40, 60, 60, 120, 55, 170)
    b.lineTo(-55, 170); b.cubicTo(-60, 120, -40, 60, -50, 20); b.cubicTo(-60, -20, -60, -80, -24, -120); b.close()
    inked(c, b, LG((-60, 0), (60, 0), [(120, 80, 60), (70, 40, 30), (120, 80, 60)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(-26, -215, 52, 22), P((200, 200, 205))); c.drawRect(skia.Rect.MakeXYWH(-26, -215, 52, 22), S(INK, 4))
    c.drawLine(-30, -60, -32, 120, S((255, 255, 255), 6, 0.5)); c.restore()


def page(c, x, y, w, h, rot, title, draw_inner, k=1.0):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); s_ = 0.85 + 0.15 * eo(k); c.scale(s_, s_)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 10, -h / 2 + 12, w, h), P(INK, 0.25, 6)); inked(c, skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), P((255, 255, 255)), 5)
    ctext(c, title, 0, -h / 2 + 46, 30, (34, 32, 30), 'Anton.ttf'); c.drawLine(-w / 2 + 20, -h / 2 + 62, w / 2 - 20, -h / 2 + 62, S(INK, 3))
    draw_inner(); c.restore()


def record(c, x, y, r, t):
    c.save(); c.translate(x, y); c.rotate(t * 90)
    c.drawCircle(0, 0, r, P((30, 30, 32))); c.drawCircle(0, 0, r, S(INK, 5))
    for k in range(1, 6): c.drawCircle(0, 0, r * (0.4 + k * 0.1), S((90, 90, 95), 2))
    c.drawCircle(0, 0, r * 0.3, P((220, 40, 50))); c.drawCircle(0, 0, 8, P((252, 250, 244)))
    c.restore()


def headline(c, t, lines, tag, sub):
    c.save(); c.translate(540, 235); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-190, -42, 380, 76), P((212, 160, 46))); f = serif(44, 400, True); tw = f.measureText(tag); c.drawString(tag, -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col, sz) in enumerate(lines):
        f = serif(sz, 700 if not it else 500, it); tw = f.measureText(txt)
        while tw > 940: f = serif(f.getSize() * 0.95, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 112, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); c.drawString(sub, 540 - f.measureText(sub) / 2, 385 + len(lines) * 112 - 40, f, P((90, 86, 80), pr(t, 0.8, 0.3)))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tn = ph('says no')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (("Santa's red suit,", False, (34, 32, 30), 104), ('and the soda myth,', False, (34, 32, 30), 96), ('explained.', True, (150, 22, 34), 112)), 'in 35 seconds', "per Coca-Cola's own website")
    santa(c, 420, 1760, 0.62, t, 'happy', arm_r=(150, -150), arm_l=(-30, 220), look=(0.5, -0.4))
    bottle(c, 800, 1060, 1.1, 8)
    if t > tn - 0.2:
        c.drawLine(690, 860, 910, 1240, S((150, 22, 34), 16)); c.drawLine(910, 860, 690, 1240, S((150, 22, 34), 16))


def s_quote(c, t):
    tb = ph('before sundblom'); ta = ph('the artist'); t31 = ph('thirty one')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, "COKE'S OWN WORDS", 540, 358, 66, (34, 32, 30))
    k = pr(t, ph('its words') - 0.1, 0.5)
    if k > 0:
        c.save(); c.translate(540, 650); s_ = 0.9 + 0.1 * eo(k); c.scale(s_, s_)
        board(c, -440, -170, 880, 340)
        f = serif(140, 700); c.drawString('“', -410, -40, f, P((190, 135, 30)))
        for i, ln in enumerate(('Santa appeared in a red coat', 'before Sundblom painted him.')):
            f = serif(54, 400, True); tw = f.measureText(ln); c.drawString(ln, -tw / 2, -20 + i * 74, f, P((150, 22, 34) if i == 0 else (34, 32, 30)))
        f = serif(28, 400); s2 = 'The Coca-Cola Company, company history page'; c.drawString(s2, -f.measureText(s2) / 2, 140, f, P((90, 86, 80)))
        c.restore()
    if t > ta - 0.3:
        def easel():
            c.drawLine(380, 1340, 470, 960, S(INK, 10)); c.drawLine(700, 1340, 610, 960, S(INK, 10))
            inked(c, skia.Rect.MakeXYWH(390, 940, 300, 260), P((255, 255, 255)), 6)
            santa(c, 540, 1190, 0.3, t, 'happy')
        pop(c, pr(t, ta - 0.3, 0.4), 540, 1100, easel)
    if t > t31 - 0.3:
        c.save(); c.translate(820, 980); c.rotate(-8); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-120, -50, 240, 100), 14, 14); c.drawRRect(r, S((200, 40, 40), 8, 0.9)); ctext(c, '1931', 0, 18, 56, (230, 40, 50), 'Anton.ttf'); c.restore()


def s_everywhere(c, t):
    tm = ph('magazines'); tbb = ph('billboards'); ts = ph('store displays'); t64 = ph('sixty four')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'WHY THE MYTH STUCK', 540, 358, 64, (34, 32, 30))
    if t < tm - 0.3:
        f = serif(420, 700); c.drawString('?', 540 - f.measureText('?') / 2, 1000, f, P((150, 22, 34)))
        people(c, 170, 1300, 5, 1.1, 0, pr(t, ph('so why does'), 1.0), t, hold=False)
    page(c, 280, 760, 300, 400, -6, 'MAGAZINE', lambda: santa(c, 0, 170, 0.32, t, 'happy'), pr(t, tm - 0.3, 0.4))
    if t > tbb - 0.3:
        def bb():
            inked(c, skia.Rect.MakeXYWH(560, 560, 420, 260), P((255, 255, 255)), 7); c.drawLine(680, 820, 680, 960, S(INK, 10)); c.drawLine(860, 820, 860, 960, S(INK, 10))
            ctext(c, 'BILLBOARD', 770, 610, 30, (34, 32, 30), 'Anton.ttf'); santa(c, 700, 800, 0.24, t, 'happy'); bottle(c, 880, 740, 0.45, 6)
        pop(c, pr(t, tbb - 0.3, 0.4), 770, 700, bb)
    if t > ts - 0.3:
        def disp():
            inked(c, skia.Rect.MakeXYWH(380, 1020, 320, 200), P((255, 255, 255)), 6); ctext(c, 'STORE DISPLAY', 540, 1060, 28, (34, 32, 30), 'Anton.ttf')
            for i in range(5): bottle(c, 420 + i * 60, 1180, 0.28, 0)
        pop(c, pr(t, ts - 0.3, 0.4), 540, 1120, disp)
    if t > ph('so why does'):
        k = pr(t, ph('thirty years') - 0.3, 0.5)
        if k > 0: pop(c, k, 540, 1330, lambda: (board(c, 190, 1270, 700, 110, (255, 214, 40)), neon_text(c, '1931 TO 1964', 540, 1348, 66, (34, 32, 30))))
    if t > t64 - 0.2:
        pop(c, pr(t, t64 - 0.2, 0.3), 540, 1330, lambda: (board(c, 190, 1270, 700, 110, (255, 214, 40)), neon_text(c, 'EVERY CHRISTMAS', 540, 1348, 66, (150, 22, 34))))


def s_cover(c, t):
    tw = ph("didn't write it"); te = ph('everywhere')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE A COVER SONG", 540, 358, 60, (34, 32, 30))
    record(c, 540, 850, 260, t)
    if t > tw - 0.2: pop(c, pr(t, tw - 0.2, 0.3), 540, 1220, lambda: (board(c, 220, 1160, 640, 100, (255, 255, 255)), neon_text(c, "DIDN'T WRITE IT", 540, 1232, 56, (34, 32, 30))))
    if t > te - 0.3:
        for i in range(6):
            a = i * math.pi / 3 + t; r = 330 + 20 * math.sin(t * 3 + i)
            pop(c, pr(t, te - 0.3 + i * 0.06, 0.3), 540 + r * math.cos(a), 850 + r * math.sin(a), lambda: (c.drawCircle(540 + r * math.cos(a), 850 + r * math.sin(a), 30, P((150, 22, 34))), c.drawCircle(540 + r * math.cos(a), 850 + r * math.sin(a), 30, S(INK, 4))))


def s_end(c, t):
    tf = ph('made him famous')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "COKE DIDN'T MAKE HIM RED", 540, 358, 56, (34, 32, 30))
    santa(c, 540, 1760, 0.72, t, 'happy' if t < tf else 'happy', arm_r=(120, -220), arm_l=(-120, -220), look=(0, -0.5))
    if t > tf - 0.3:
        pop(c, pr(t, tf - 0.3, 0.35), 540, 560, lambda: (board(c, 220, 500, 640, 120, (255, 214, 40)), neon_text(c, 'IT MADE HIM FAMOUS', 540, 585, 58, (150, 22, 34))))
        for i in range(8):
            a = i * math.pi / 4; c.drawLine(540 + 300 * math.cos(a), 1000 + 300 * math.sin(a), 540 + 380 * math.cos(a), 1000 + 380 * math.sin(a), S((190, 135, 30), 10, pr(t, tf, 0.3)))


SCENES = [(0.0, s_hook), (ph('its words') - 0.15, s_quote), (ph('so why does') - 0.15, s_everywhere), (ph("it's like a song") - 0.15, s_cover), (ph("so coke didn't") - 0.15, s_end)]
SHAKES = [(ph('says no'), 10, 0.35), (ph('red coat'), 8, 0.3), (ph('sixty four'), 12, 0.4), (ph('made him famous'), 10, 0.35)]
TR = 0.32
