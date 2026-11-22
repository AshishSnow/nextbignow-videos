# ------------------------------------------------------------------ popcorn props
def kernel_puff(c, x, y, r, seed=0):
    rnd = random.Random(seed)
    for k in range(4):
        dx, dy = rnd.uniform(-0.5, 0.5) * r, rnd.uniform(-0.5, 0.3) * r
        c.drawCircle(x + dx, y + dy, r * rnd.uniform(0.55, 0.75), P((255, 248, 220)))
    for k in range(4):
        dx, dy = rnd.uniform(-0.5, 0.5) * r, rnd.uniform(-0.5, 0.3) * r
        c.drawCircle(x + dx, y + dy, r * 0.6, S(INK, 3))
    c.drawCircle(x - r * 0.15, y - r * 0.2, r * 0.42, P((255, 252, 235)))
    c.drawCircle(x + r * 0.1, y + r * 0.15, r * 0.25, P((255, 215, 90), 0.8))


def bucket(c, x, y, s=1.0, rot=0, t=0.0, label=''):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rnd = random.Random(5)
    for i in range(16):
        px, py = rnd.uniform(-120, 120), rnd.uniform(-200, -130) - (60 - abs(rnd.uniform(-60, 60)))
        kernel_puff(c, px, py + 3 * math.sin(t * 3 + i), rnd.uniform(28, 40), i)
    b = path([(-140, -150), (140, -150), (100, 150), (-100, 150)])
    c.drawPath(b, P((255, 255, 255)))
    c.save(); c.clipPath(b)
    for i in range(-3, 4):
        c.drawPath(path([(i * 80 - 22, -160), (i * 80 + 22, -160), (i * 58 + 16, 160), (i * 58 - 16, 160)]), P((235, 40, 60)))
    c.restore(); c.drawPath(b, S(INK, 8))
    inked(c, skia.Rect.MakeXYWH(-150, -168, 300, 30), P((255, 214, 40)), 6)
    if label:
        board(c, -110, -40, 220, 90, (255, 214, 40)); ctext(c, label, 0, 26, 64 if len(label) < 5 else 46, (235, 40, 60), 'Anton.ttf')
    c.restore()


def soda(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawLine(20, -170, 50, -260, S(INK, 16)); c.drawLine(20, -170, 50, -260, S((255, 90, 120), 9))
    inked(c, path([(-80, -170), (80, -170), (60, 150), (-60, 150)]), LG((-80, 0), (80, 0), [(40, 170, 255), (30, 110, 230)]), 7)
    inked(c, skia.Rect.MakeXYWH(-92, -190, 184, 30), P((255, 255, 255)), 6)
    c.drawCircle(0, -20, 50, P((255, 255, 255))); c.drawCircle(0, -20, 50, S(INK, 5)); ctext(c, 'XL', 0, 2, 54, (30, 110, 230), 'Anton.ttf')
    c.restore()


def ticket(c, x, y, w, rot, part='both', text='ADMIT ONE', price='$12'):
    """horizontal cinema ticket; part = both | left | right (torn halves)."""
    h = w * 0.45
    c.save(); c.translate(x, y); c.rotate(rot)
    halves = {'left': (-w / 2, 0), 'right': (0, w / 2), 'both': (-w / 2, w / 2)}[part]
    r = skia.Rect.MakeLTRB(halves[0], -h / 2, halves[1], h / 2)
    c.drawRect(r.makeOffset(10, 12), P(INK, 0.3, 6))
    shape = skia.Path(); shape.addRect(r)
    for sy in (-h / 2, h / 2):
        for k in range(1, 7):
            cx_ = -w / 2 + k * w / 7
            if halves[0] < cx_ < halves[1]: shape.addCircle(cx_, sy, 12)
    shape.setFillType(skia.PathFillType.kEvenOdd)
    inked(c, shape, LG((0, -h / 2), (0, h / 2), [(255, 230, 90), (255, 190, 30)]), 7)
    c.save(); c.clipRect(r)
    c.drawLine(0, -h / 2 + 10, 0, h / 2 - 10, S((200, 120, 20), 5))
    ctext(c, text, -w / 4, 16, w * 0.075, (200, 40, 50), 'Anton.ttf')
    ctext(c, price, w / 4, 30, w * 0.16, (200, 40, 50), 'Anton.ttf')
    c.restore()
    if part != 'both':
        z = halves[1] if part == 'left' else halves[0]
        p = skia.Path(); p.moveTo(z, -h / 2)
        for k in range(1, 9): p.lineTo(z + (10 if k % 2 else -10), -h / 2 + k * h / 8)
        c.drawPath(p, S(INK, 6))
    c.restore()


def studio(c, x, y, w, h, t):
    """generic film studio lot: hangar with a clapperboard sign."""
    p = skia.Path(); p.moveTo(x, y + h); p.lineTo(x, y + h * 0.35); p.quadTo(x + w / 2, y - h * 0.15, x + w, y + h * 0.35); p.lineTo(x + w, y + h); p.close()
    c.save(); c.translate(14, 14); c.drawPath(p, P((0, 0, 0), 0.3, 10)); c.restore()
    inked(c, p, LG((0, y), (0, y + h), [(250, 250, 255), (205, 210, 230)]), 7)
    inked(c, skia.Rect.MakeXYWH(x + w * 0.35, y + h * 0.55, w * 0.3, h * 0.45), P((120, 130, 160)), 5)
    cx_, cy_ = x + w / 2, y + h * 0.3
    inked(c, skia.Rect.MakeXYWH(cx_ - 90, cy_ - 30, 180, 90), P((30, 30, 40)), 5)
    c.save(); c.translate(cx_ - 90, cy_ - 30); c.rotate(-14 - 6 * abs(math.sin(t * 2)))
    inked(c, skia.Rect.MakeXYWH(0, -30, 180, 30), P((255, 255, 255)), 5)
    for i in range(4): c.drawPath(path([(10 + i * 45, -30), (35 + i * 45, -30), (20 + i * 45, 0), (-5 + i * 45, 0)]), P((30, 30, 40)))
    c.restore()
    neon_text(c, 'STUDIOS', cx_, y + h * 0.5, 56, (255, 214, 40))


def curtains(c, t, k_open=1.0):
    for sx in (-1, 1):
        x0 = 0 if sx < 0 else W
        wdt = 160 + 300 * (1 - k_open)
        for i in range(5):
            xx = x0 - sx * (i * wdt / 5)
            c.drawRect(skia.Rect.MakeXYWH(min(xx, xx - sx * wdt / 5), 0, wdt / 5, H), LG((xx, 0), (xx - sx * wdt / 5, 0), [(150, 10, 30), (220, 40, 60), (150, 10, 30)]))
        c.drawLine(x0 - sx * wdt, 0, x0 - sx * wdt, H, S(INK, 8))


def cinema_inside(c, t, glow_=(120, 200, 255), draw=None):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(60, 40, 110), (120, 50, 120), (200, 70, 90)]))
    sr = skia.Rect.MakeXYWH(110, 380, 860, 480)
    c.drawRect(sr.makeOutset(40, 40), P(glow_, 0.45, 60))
    inked(c, sr.makeOutset(14, 14), P((30, 24, 40)), 7)
    c.drawRect(sr, LG((0, 380), (0, 860), [(230, 245, 255), (160, 210, 255)]))
    if draw:
        c.save(); c.clipRect(sr); c.translate(sr.left(), sr.top()); draw(c); c.restore()
    light_cone(c, 540, 300, 30, 860, 560, (255, 255, 230), 0.12)
    curtains(c, t)
    for row in range(3):
        y = 1180 + row * 200; n = 6 + row
        for i in range(n):
            x = 540 + (i - (n - 1) / 2) * (900 / (n - 0.5))
            seat = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 62, y, 124, 170), 34, 34)
            inked(c, seat, LG((0, y), (0, y + 170), [(240, 60, 80), (170, 20, 45)]), 6)
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 46, y + 18, 92, 22), 10, 10, P((255, 255, 255), 0.25))


def bill(c, x, y, k, t, rot, s):
    if k <= 0: return
    sc = min(1, k * 1.5); c.save(); c.translate(x, y); c.rotate(rot + 4 * math.sin(t * 3 + x)); c.scale(sc, sc)
    c.drawRect(skia.Rect.MakeXYWH(-90 + 8, -110 + 8, 180, 220), P(INK, 0.3)); inked(c, skia.Rect.MakeXYWH(-90, -110, 180, 220), P((255, 252, 240)), 6)
    ctext(c, s, 0, -50, 34 if len(s) > 6 else 40, (220, 40, 60), 'Anton.ttf')
    for i in range(4): c.drawLine(-70, -10 + i * 30, 60 - (i % 2) * 40, -10 + i * 30, S((170, 170, 190), 5))
    c.restore()


def counter_bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 120, 90), (255, 190, 120), (255, 230, 170)]))
    for i in range(14):                                   # marquee bulbs
        on = ((int(t * 6) + i) % 3) != 0
        c.drawCircle(60 + i * 74, 210, 16, P((255, 240, 160) if on else (200, 140, 80)))
        if on: c.drawCircle(60 + i * 74, 210, 30, P((255, 240, 160), 0.4, 12))
    inked(c, skia.Rect.MakeXYWH(-20, 1220, W + 40, 60), P((255, 255, 255)), 7)
    c.drawRect(skia.Rect.MakeXYWH(0, 1280, W, 640), LG((0, 1280), (0, H), [(235, 40, 60), (160, 15, 40)]))
    for i in range(8): c.drawRect(skia.Rect.MakeXYWH(i * 140, 1280, 60, 640), P((255, 255, 255), 0.12))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    th = ph('the real money')
    sky_bg(c, t, (170, 180, 195))
    building(c, 110, 760, 860, 560, (120, 60, 150), 'CINEMA', (255, 214, 40), t, False)
    for i in range(12):                                   # marquee bulbs around the sign
        on = ((int(t * 6) + i) % 3) != 0
        c.drawCircle(150 + i * 71, 790, 12, P((255, 240, 160) if on else (150, 110, 80)))
    board(c, 70, 250, 940, 200)
    neon_text(c, 'YOUR MOVIE THEATER', 540, 340, 66, (120, 60, 200))
    neon_text(c, 'BARELY PROFITS ON TICKETS', 540, 425, 54, (255, 70, 90))
    kx = pr(t, 0.0, 1.6)
    person(c, lerp(-300, 330, eo(kx)), 1720, 0.62, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.7, -0.2), t=t,
           arm_r=(170, -150), arm_l=(-30, 220), blink=blinking(t), prop=(1, lambda cc, ex, ey: ticket(cc, ex + 60, ey - 40, 220, -12)))
    if t > th - 0.3:
        k = pr(t, th - 0.3, 0.4)
        pop(c, k, 790, 1250, lambda: (bucket(c, 790, 1300, 1.2, 8, t), sparkle(c, 640, 1030, 40), sparkle(c, 950, 1080, 30)))
        if t > th + 0.6: pop(c, pr(t, th + 0.6, 0.3), 800, 1640, lambda: (board(c, 640, 1580, 320, 110, (255, 236, 90)), neon_text(c, '$$$', 800, 1665, 80, (40, 170, 90))))


def s_ticket(c, t):
    th = ph('about half'); ts = ph('to the studios'); t12 = ph('twelve dollar'); tr = ph('the rent')
    sky_bg(c, t, (150, 220, 160))
    studio(c, 560, 1000, 460, 380, t)
    board(c, 90, 250, 900, 150); neon_text(c, 'WHERE YOUR TICKET GOES', 540, 350, 60, (120, 60, 200))
    split = pr(t, th - 0.1, 0.5)
    if split <= 0:
        ticket(c, 540, 760, 640, -4 + 2 * math.sin(t * 2))
    else:
        u = pr(t, ts - 0.2, 0.9)
        ticket(c, 540 - 40 * eo(split), 760, 640, -4 - 6 * split, 'left')
        rx = lerp(540 + 40 * eo(split), 790, eio(u)); ry = lerp(760, 1330, eio(u)) - 160 * math.sin(math.pi * u)
        c.save(); c.translate(rx, ry); c.scale(1 - 0.6 * u, 1 - 0.6 * u); c.translate(-rx, -ry)
        ticket(c, rx, ry, 640, -4 + 30 * u, 'right'); c.restore()
        if u > 0.6:
            pop(c, pr(t, ts + 0.3, 0.3), 790, 940, lambda: (board(c, 640, 880, 300, 110, (255, 255, 255)), neon_text(c, '~51%', 790, 965, 72, (255, 70, 90))))
    ctext(c, "SOURCE: AMC 10-K, 2025, U.S. MARKETS", 540, 445, 26, (40, 60, 110), 'Montserrat-ExtraBold.ttf')
    if t > t12 - 0.2 and t < tr - 0.3:
        pop(c, pr(t, t12 - 0.2, 0.35), 280, 1180, lambda: sticky(c, 280, 1180, 1.0, -6, '$12 = $6 GONE', size=46))
    for i, lab in enumerate(('RENT', 'STAFF', 'SCREENS')):
        kb = pr(t, tr - 0.3 + i * 0.35, 0.35)
        if kb > 0: bill(c, 150 + i * 150, 1180 - 30 * i, kb, t, -10 + i * 10, lab)
    person(c, 260, 1800, 0.5, (255, 140, 40), (36, 44, 90), mood='worried' if t > th else 'neutral', look=(0.6, -0.6), t=t, blink=blinking(t))


def s_snack(c, t):
    tc = ph('the snack counter'); td = ph('every dollar'); t18 = ph('eighteen cents'); t82 = ph('eighty two')
    counter_bg(c, t)
    if t < tc - 0.2:
        board(c, 120, 300, 840, 150); neon_text(c, "WHERE'S THE MONEY?", 540, 400, 64, (30, 160, 255))
    else:
        board(c, 120, 300, 840, 150); neon_text(c, 'THE SNACK COUNTER', 540, 400, 68, (235, 40, 60))
    pop(c, pr(t, tc - 0.3, 0.4), 300, 1080, lambda: bucket(c, 300, 1080, 0.85, -6, t))
    pop(c, pr(t, tc - 0.1, 0.4), 760, 1080, lambda: soda(c, 760, 1080, 0.85, 6))
    person(c, 540, 1240, 0.5, (90, 200, 120), (235, 40, 60), mood='happy', look=(0, 0.2), t=t, arm_r=(120, 140), arm_l=(-120, 140), shirt=(255, 255, 255), blink=blinking(t, 3))
    if t > td - 0.3:                                      # $1 split bar: 18c food vs 82c left
        k = pr(t, td - 0.3, 0.4)
        def dollar():
            board(c, 90, 470, 900, 350, (255, 255, 255))
            ctext(c, 'EVERY $1 OF SNACKS', 540, 545, 46, (40, 40, 60), 'Anton.ttf')
            x0, y0, w, h = 140, 580, 800, 120
            f = pr(t, t18 - 0.2, 0.5); g = pr(t, t82 - 0.3, 0.6)
            c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), P((235, 235, 240)))
            if f > 0: c.drawRect(skia.Rect.MakeXYWH(x0, y0, w * 0.18 * eo(f), h), P((255, 90, 110)))
            if g > 0: c.drawRect(skia.Rect.MakeXYWH(x0 + w * 0.18, y0, w * 0.82 * eo(g), h), P((60, 200, 120)))
            c.drawRect(skia.Rect.MakeXYWH(x0, y0, w, h), S(INK, 7))
            if f > 0.5: ctext(c, '18¢', x0 + w * 0.09, y0 + 82, 52, (255, 255, 255), 'Anton.ttf'); ctext(c, 'FOOD', x0 + w * 0.09, y0 + 170, 34, (220, 40, 60), 'Anton.ttf')
            if g > 0.5: ctext(c, '82¢', x0 + w * 0.59, y0 + 88, 76, (255, 255, 255), 'Anton.ttf'); ctext(c, 'LEFT, BEFORE STAFF + RENT', x0 + w * 0.59, y0 + 170, 32, (30, 140, 80), 'Anton.ttf')
        pop(c, k, 540, 650, dollar)


def s_big(c, t):
    th = ph('how big'); t8 = ph('eight dollars'); tb = ph('one point three')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        if t < tb - 0.3:
            k = pr(t, t8 - 0.3, 0.4)
            ctext(cc, 'SNACKS PER AMC MOVIEGOER', 410, 70, 36, (255, 255, 255))
            if k > 0: neon_text(cc, '$8.57', 410, 250, 130, (255, 214, 40), cl(k * 2))
            ctext(cc, 'U.S., 2025, PER AMC 10-K', 410, 330, 24, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
        else:
            k = pr(t, tb - 0.3, 0.4)
            ctext(cc, 'AMC U.S. SNACK SALES, 2025', 410, 70, 36, (255, 255, 255))
            neon_text(cc, '$1.3 BILLION+', 410, 250, 100, (80, 230, 140), cl(k * 2))
            ctext(cc, 'IN ONE YEAR', 410, 330, 24, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
    screen(c, 130, 300, 820, 380, d, (255, 214, 40))
    dim = pr(t, th - 0.1, 0.4) * (1 - pr(t, t8 - 0.2, 0.25))
    rnd = random.Random(3)
    n = int(14 * pr(t, tb, 1.2))
    for i in range(n):
        bucket(c, 150 + (i * 197) % 780, 1180 - (i // 5) * 120 + rnd.uniform(-20, 20), 0.42, rnd.uniform(-20, 20), t)
    person(c, 900, 1800, 0.56, (255, 140, 40), (36, 44, 90), mood='shock', look=(-0.6, -0.7), sweat=2, t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.4 * dim))


def s_reveal(c, t):
    ts = ph('a snack bar'); tbs = ph('really big screen')
    def film(cc):
        cc.drawRect(skia.Rect.MakeWH(860, 480), LG((0, 0), (860, 480), [(120, 200, 255), (255, 170, 210)]))
        bucket(cc, 430, 330, 1.05 + 0.03 * math.sin(t * 4), 0, t)
    cinema_inside(c, t, (255, 200, 120), film if t > ts - 0.3 else None)
    if t < ts - 0.3:
        board(c, 120, 140, 840, 150); neon_text(c, 'WHAT IS A THEATER?', 540, 240, 64, (120, 60, 200))
    else:
        pop(c, pr(t, ts - 0.3, 0.35), 540, 215, lambda: (board(c, 120, 140, 840, 150, (255, 236, 90)), neon_text(c, 'A SNACK BAR...', 540, 240, 74, (235, 40, 60))))
        if t > tbs - 0.3:
            pop(c, pr(t, tbs - 0.3, 0.35), 540, 960, lambda: (board(c, 170, 900, 740, 110, (255, 255, 255)), neon_text(c, 'WITH A REALLY BIG SCREEN', 540, 978, 48, (30, 160, 255))))
    person(c, 540, 1900, 0.62, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.8), t=t, arm_r=(60, -40), arm_l=(-60, -40), blink=blinking(t),
           prop=(1, lambda cc, ex, ey: bucket(cc, ex - 40, ey - 60, 0.5, 0, t)))


def s_end(c, t):
    tm = ph('you came for'); tp = ph('came for your popcorn'); tq = ph('do you buy')
    sky_bg(c, t)
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOU CAME FOR THE MOVIE', 540, 355, 56, (30, 160, 255)); neon_text(c, 'THEY CAME FOR THE POPCORN', 540, 440, 50, (255, 70, 90), pr(t, tp - 0.4, 0.3))
        pop(c, pr(t, tm, 0.4), 300, 1000, lambda: ticket(c, 300, 1000, 380, -10))
        if t > tp - 0.2: pop(c, pr(t, tp - 0.2, 0.4), 800, 1000, lambda: bucket(c, 800, 1060, 1.0, 8, t, '$$$'))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'DO YOU BUY THE', 540, 355, 70, (30, 160, 255)); neon_text(c, 'POPCORN EVERY TIME?', 540, 440, 64, (255, 190, 30))
        for x, lab, col in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 130, 590, 260, 120, col), neon_text(c, lab, x, 680, 80, (255, 255, 255))))
    person(c, 540, 1680, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_hook), (ph("amc's annual") - 0.15, s_ticket), (ph("so where's the") - 0.15, s_snack), (ph('how big') - 0.15, s_big),
    (ph('so what is') - 0.15, s_reveal), (ph('you came for') - 0.15, s_end)]
SHAKES = [(ph('about half'), 10, 0.35), (ph('eighteen cents'), 8, 0.3), (ph('eight dollars'), 12, 0.35), (ph('one point three'), 18, 0.45), (ph('a snack bar'), 10, 0.35)]
TR = 0.32
