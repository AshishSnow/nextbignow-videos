# ------------------------------------------------------------------ Yue Yuen: reference-reel layout (explainer centred, small mascot beside the subtitles)
# props: generic sneakers (no logos/stripes/trade dress, brand names as plain tape labels only), factory, conveyor, tag, boxing ring
SNC = {'NIKE': (230, 50, 60), 'ADIDAS': (60, 120, 220), 'NEW BALANCE': (150, 150, 160), 'PUMA': (212, 160, 46)}


def buddy(c, t, mood='happy', look=(0.6, -0.6)):
    """small OMB mascot parked bottom-left, next to the subtitle strip, reacting."""
    person(c, 112, 1500, 0.23, (255, 140, 40), (36, 44, 90), mood=mood, look=look, t=t, blink=blinking(t))


def tape(c, x, y, txt, size=34, col=(212, 160, 46), rot=-3):
    f = serif(size, 600); tw = f.measureText(txt)
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(skia.Rect.MakeXYWH(-tw / 2 - 16, -size * 0.85, tw + 32, size * 1.25), P(col))
    c.drawRect(skia.Rect.MakeXYWH(-tw / 2 - 16, -size * 0.85, tw + 32, size * 1.25), S(INK, 2.5))
    c.drawString(txt, -tw / 2, size * 0.2, f, P((34, 32, 30))); c.restore()


def sneaker(c, x, y, s=1.0, rot=0, col=(230, 50, 60), label=None, face=False, t=0.0, walk=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if walk > 0:   # little legs (reference trick: objects with legs)
        for sx in (-1, 1):
            a = math.sin(t * 12 + sx) * 18 * walk
            c.drawLine(sx * 50, 40, sx * 50 + a, 100, S(INK, 7)); c.drawLine(sx * 50 + a, 100, sx * 50 + a + 22, 100, S(INK, 7))
    sole = skia.Path(); sole.moveTo(-160, 30); sole.lineTo(170, 30); sole.cubicTo(185, 30, 190, 55, 170, 62); sole.lineTo(-150, 62); sole.cubicTo(-175, 62, -178, 30, -160, 30); sole.close()
    inked(c, sole, P((250, 248, 240)), 6)
    up = skia.Path(); up.moveTo(-160, 32); up.cubicTo(-170, -30, -140, -80, -90, -88); up.lineTo(-40, -90); up.cubicTo(-20, -40, 40, -30, 90, -10)
    up.cubicTo(150, 5, 175, 15, 170, 32); up.close()
    inked(c, up, P(col), 6)
    for i in range(4): c.drawLine(-60 + i * 22, -70 + i * 14, -30 + i * 22, -58 + i * 14, S((250, 248, 240), 5))
    c.drawLine(-150, 12, 160, 14, S(INK, 3, 0.6))
    if face:
        for ex in (40, 85):
            c.drawCircle(ex, -8, 13, P((255, 255, 255))); c.drawCircle(ex, -8, 13, S(INK, 3)); c.drawCircle(ex + 3, -6, 6, P(INK))
    c.restore()
    if label: tape(c, x, y + 95 * s + 30, label, 30)


def factory(c, x, y, s=1.0, t=0.0, label='YUE YUEN'):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, cx in enumerate((-150, -40)):   # chimneys + smoke
        inked(c, skia.Rect.MakeXYWH(cx, -330, 50, 170), P((180, 70, 60)), 6)
        for j in range(3):
            u = ((t * 0.6 + j / 3 + i * 0.2) % 1)
            c.drawCircle(cx + 25 + 30 * u, -350 - 120 * u, 18 + 22 * u, P((200, 200, 205), 0.8 * (1 - u)))
    roof = skia.Path(); roof.moveTo(-220, -160)
    for k in range(4): roof.lineTo(-220 + k * 110 + 110, -230); roof.lineTo(-220 + k * 110 + 110, -160)
    roof.close(); inked(c, roof, P((210, 210, 215)), 6)
    inked(c, skia.Rect.MakeXYWH(-220, -160, 440, 160), P((235, 232, 222)), 7)
    for k in range(4): inked(c, skia.Rect.MakeXYWH(-195 + k * 100, -130, 70, 55), P((170, 200, 230)), 4)
    inked(c, skia.Rect.MakeXYWH(-40, -60, 80, 60), P((120, 90, 70)), 5)
    c.restore()
    if label: tape(c, x, y - 250 * s - 120 * s, label, 40, (212, 160, 46), 2)


def arrow(c, x0, y0, x1, y1, k, col=(150, 22, 34)):
    if k <= 0: return
    ex, ey = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    c.drawLine(x0, y0, ex, ey, S(col, 7))
    if k > 0.95:
        a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6): c.drawLine(ex, ey, ex + 34 * math.cos(a + da), ey + 34 * math.sin(a + da), S(col, 7))


def pricetag(c, x, y, txt, rot=-10, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, path([(-30, -60), (190, -60), (190, 60), (-30, 60), (-80, 0)]), P((255, 214, 40)), 6)
    c.drawCircle(-38, 0, 12, P((252, 250, 244))); c.drawCircle(-38, 0, 12, S(INK, 3))
    f = serif(72, 700); c.drawString(txt, 80 - f.measureText(txt) / 2, 25, f, P((150, 22, 34))); c.restore()


def ring(c, k=1.0):
    for i, y in enumerate((640, 720, 800)):
        c.drawLine(110, y, 110 + 860 * k, y, S((200, 40, 40), 8))
    for px in (110, 970):
        if px == 110 or k > 0.98: inked(c, skia.Rect.MakeXYWH(px - 16, 590, 32, 500), P((200, 40, 40)), 5)
    c.drawRect(skia.Rect.MakeXYWH(90, 1090, 900, 24), P((190, 170, 140)))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t + 2.0, (('The sneaker maker', False, (34, 32, 30), 104), ("you've never heard of,", False, (34, 32, 30), 88), ('explained.', True, (150, 22, 34), 112)), 'in 30 seconds', 'per its 2025 results')
    names = ['NIKE', 'ADIDAS', 'NEW BALANCE', 'PUMA']; keys = ['nike', 'adidas', 'new balance', 'puma']
    pos = [(290, 900), (790, 900), (290, 1130), (790, 1130)]
    th = ph('yue yuen'); te = ph('every one')
    for i, (n, kk, (x, y)) in enumerate(zip(names, keys, pos)):
        k = pr(t, ph(kk) - 0.15, 0.35) if t > 0.05 else 0
        if i == 0: k = 1.0   # frame 0 already has a sneaker on it
        sh = 0 if t < th else -40 * eo(pr(t, th, 0.4)) * (1 if x < 540 else -1)
        if k > 0: pop(c, k, x, y, lambda x=x, y=y, n=n, sh=sh: sneaker(c, x, y, 0.95, sh * 0.15, SNC[n], n, face=True, t=t))
    if t > th - 0.2:
        pop(c, pr(t, th - 0.2, 0.45), 540, 1010, lambda: (c.drawCircle(540, 1010, 95, P((252, 250, 244))), c.drawCircle(540, 1010, 95, S(INK, 6)), ctext(c, '?', 540, 1050, 120, (150, 22, 34), 'Anton.ttf')))
    if t > te - 0.3:
        for i, (x, y) in enumerate(pos): arrow(c, 540, 1010, x + (60 if x < 540 else -60), y - 20, pr(t, te - 0.2 + i * 0.1, 0.3))
    buddy(c, t, 'shock' if t > th else 'happy')


def s_who(c, t):
    tq = ph('who really'); tl = ph('listed in')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'WHO MAKES YOUR SNEAKERS?', 540, 358, 54, (34, 32, 30))
    sneaker(c, 540, 700, 1.4, -4, (230, 50, 60), None, face=True, t=t)
    if t > ph('yue yuen', tq) - 0.3: pop(c, pr(t, ph('yue yuen', tq) - 0.3, 0.45), 540, 1100, lambda: factory(c, 540, 1235, 1.0, t))
    if t > tl - 0.3:
        c.save(); c.translate(540, 1300); c.rotate(-4); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -44, 400, 88), 12, 12); c.drawRRect(r, S((200, 40, 40), 7, 0.9)); ctext(c, 'LISTED IN HONG KONG', 0, 14, 38, (230, 40, 50), 'Anton.ttf'); c.restore()
    buddy(c, t, 'happy', (0.7, -0.8))


def s_volume(c, t):
    tn = ph('two hundred'); te = ph('eight pairs')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'SHIPPED IN 2025', 540, 358, 66, (34, 32, 30))
    # conveyor with sneakers rolling off the line
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(80, 860, 920, 60), 30, 30), P((120, 120, 130)), 6)
    for i in range(9): c.drawCircle(120 + i * 105, 890, 18, P((200, 200, 210))); c.drawCircle(120 + i * 105, 890, 18, S(INK, 3))
    sp = 1.6 if t > te else 0.8
    for i in range(5):
        u = ((t * sp * 0.25 + i / 5) % 1); x = 80 + 920 * u
        sneaker(c, x, 820, 0.5, 0, [(230, 50, 60), (60, 120, 220), (150, 150, 160), (212, 160, 46), (60, 160, 90)][i])
    if t > tn - 0.3:
        def big():
            board(c, 120, 1000, 840, 220, (255, 214, 40))
            f = serif(104, 700); s_ = '252,000,000'; c.drawString(s_, 540 - f.measureText(s_) / 2, 1110, f, P((150, 22, 34)))
            ctext(c, 'PAIRS OF SHOES', 540, 1180, 44, (34, 32, 30), 'Anton.ttf')
        pop(c, pr(t, tn - 0.3, 0.45), 540, 1110, big)
    if t > te - 0.3:
        def clock():
            c.drawCircle(540, 560, 100, P((252, 250, 244))); c.drawCircle(540, 560, 100, S(INK, 7))
            a = t * 6.28; c.drawLine(540, 560, 540 + 75 * math.sin(a), 560 - 75 * math.cos(a), S((150, 22, 34), 6))
            tape(c, 540, 715, '8 PAIRS EVERY SECOND', 34, (212, 160, 46), -2)
        pop(c, pr(t, te - 0.3, 0.4), 540, 580, clock)
    buddy(c, t, 'shock' if t > tn else 'happy', (0.6, -0.9))


def s_price(c, t):
    ta = ph('twenty one') if True else 0
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'WHAT IT GETS PER PAIR', 540, 358, 58, (34, 32, 30))
    factory(c, 300, 1170, 0.8, t, 'YUE YUEN')
    sneaker(c, 700, 860, 1.2, -6, (60, 120, 220), None, face=True, t=t)
    arrow(c, 430, 1000, 600, 930, pr(t, ph('per pair') - 0.2, 0.3))
    if t > ta - 0.3: pop(c, pr(t, ta - 0.3, 0.4), 760, 1080, lambda: pricetag(c, 700, 1080, '$21', -8, 1.1))
    if t > ph('on average') - 0.2: tape(c, 760, 1210, 'ON AVERAGE, 2025', 30, (252, 250, 244), 2)
    buddy(c, t, 'happy', (0.7, -0.6))


def s_split(c, t):
    tb = ph('does the building')
    paper_bg(c, t, skyline=False, ground=True)
    c.drawLine(540, 450, 540, 1230, S(INK, 3, 0.6))
    tape(c, 300, 520, 'THE BRAND', 40, (252, 250, 244), -2); tape(c, 780, 520, 'YUE YUEN', 40, (212, 160, 46), 2)
    # left: billboard + pencil
    kd = pr(t, ph('the design') - 0.2, 0.4)
    if kd > 0:
        def bb():
            inked(c, skia.Rect.MakeXYWH(120, 640, 360, 240), P((252, 250, 244)), 7)
            sneaker(c, 300, 760, 0.7, -10, (230, 50, 60))
            c.drawLine(300, 880, 300, 1180, S(INK, 8)); ctext(c, 'DESIGN + ADS', 300, 960, 42, (150, 22, 34), 'Anton.ttf')
        pop(c, kd, 300, 760, bb)
    kb = pr(t, tb - 0.3, 0.4)
    if kb > 0: pop(c, kb, 780, 1000, lambda: (factory(c, 780, 1180, 0.75, t, None), ctext(c, 'BUILDS IT', 780, 700, 52, (150, 22, 34), 'Anton.ttf')))
    buddy(c, t, 'happy', (0.8, -0.5))


def s_war(c, t):
    ts = ph('same maker'); tw = ph('sneaker war'); tb = ph('both sides')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'RIVALS ON THE SHELF', 540, 358, 60, (34, 32, 30))
    ring(c, pr(t, SCENES[-1][0], 0.5))
    rk = pr(t, ts - 0.2, 0.6)
    if rk > 0:   # the factory rises behind both fighters
        c.save(); c.translate(0, 300 * (1 - eo(rk))); factory(c, 540, 1050, 0.9, t, 'SAME MAKER'); c.restore()
    bump = math.sin(t * 9) * 10 if t > tw else 0
    sneaker(c, 300 + bump, 960, 1.0, 4, (230, 50, 60), 'NIKE', face=True, t=t, walk=1.0 if t > tw else 0.0)
    c.save(); c.translate(780 - bump, 0); c.scale(-1, 1); sneaker(c, 0, 960, 1.0, 4, (60, 120, 220), None, face=True, t=t, walk=1.0 if t > tw else 0.0); c.restore()
    tape(c, 780 - bump, 1085, 'ADIDAS', 30)
    if t > tb - 0.2:
        pop(c, pr(t, tb - 0.2, 0.35), 540, 1250, lambda: (board(c, 150, 1180, 780, 110, (255, 214, 40)), neon_text(c, 'BOTH BUY FROM ONE MAKER', 540, 1258, 50, (150, 22, 34))))
    buddy(c, t, 'shock' if t > ts else 'happy', (0.7, -0.7))


SCENES = [(0.0, s_hook), (ph('so who really') - 0.15, s_who), (ph('last year') - 0.15, s_volume), (ph('how much') - 0.15, s_price),
          (ph('the brands do') - 0.15, s_split), (ph('rivals on') - 0.15, s_war)]
SHAKES = [(ph('yue yuen'), 10, 0.3), (ph('two hundred'), 14, 0.4), (ph('twenty one'), 8, 0.3), (ph('same maker'), 12, 0.4), (ph('both sides'), 10, 0.35)]
TR = 0.3
