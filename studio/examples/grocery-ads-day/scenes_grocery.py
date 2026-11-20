# ------------------------------------------------------------------ grocery props
def milk(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, path([(-50, -60), (50, -60), (50, 110), (-50, 110)]), LG((-50, 0), (50, 0), [(255, 255, 255), (225, 235, 245)]), 6)
    inked(c, path([(-50, -60), (0, -110), (50, -60)]), P((80, 160, 255)), 6)
    c.drawRect(skia.Rect.MakeXYWH(-50, -10, 100, 50), P((80, 160, 255))); ctext(c, 'MILK', 0, 28, 30, (255, 255, 255), 'Anton.ttf')
    c.restore()


def bread(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-80, -40, 160, 80), 40, 40)); inked(c, p, LG((0, -40), (0, 40), [(240, 180, 100), (200, 130, 60)]), 6)
    for i in range(3): c.drawLine(-40 + i * 40, -30, -30 + i * 40, 30, S((170, 100, 40), 5))
    c.restore()


def apple(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 38, RG(-12, -12, 50, [(255, 120, 120), (220, 40, 50), (160, 20, 30)])); c.drawCircle(0, 0, 38, S(INK, 5))
    c.drawLine(0, -36, 6, -54, S((110, 70, 30), 6)); c.drawOval(skia.Rect.MakeXYWH(6, -58, 26, 14), P((60, 180, 80))); c.restore()


def cart(c, x, y, s=1.0, full=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if full > 0:
        milk(c, -60, -170, 0.9, -8); bread(c, 40, -150, 0.9, 10); apple(c, 110, -130, 1.0); apple(c, -130, -130, 0.9)
    basket = path([(-180, -140), (180, -140), (150, 20), (-150, 20)])
    c.drawPath(basket, P((200, 220, 240), 0.5)); c.drawPath(basket, S(INK, 7))
    for i in range(1, 6): c.drawLine(-180 + i * 60, -140, -150 + i * 50, 20, S(INK, 3))
    for j in range(1, 3): c.drawLine(-175 + j * 8, -140 + j * 53, 175 - j * 8, -140 + j * 53, S(INK, 3))
    c.drawLine(180, -140, 240, -200, S(INK, 9)); c.drawLine(-150, 20, -120, 60, S(INK, 7)); c.drawLine(150, 20, 130, 60, S(INK, 7))
    c.drawLine(-140, 60, 150, 60, S(INK, 7))
    for wx in (-110, 120): c.drawCircle(wx, 80, 22, P(INK)); c.drawCircle(wx, 80, 9, P((200, 200, 210)))
    c.restore()


def phone(c, x, y, s, rot, draw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-160, -290, 320, 580), 40, 40); c.drawRRect(r.makeOffset(10, 12) if hasattr(r, 'makeOffset') else r, P(INK, 0.3, 6)); inked(c, r, P((30, 30, 40)), 8)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(-140, -260, 280, 520)); c.drawRect(skia.Rect.MakeXYWH(-140, -260, 280, 520), P((255, 255, 255))); c.translate(-140, -260); draw(c); c.restore()
    c.restore()


def moneybag(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b = skia.Path(); b.moveTo(-30, -70); b.cubicTo(-110, -40, -110, 80, 0, 80); b.cubicTo(110, 80, 110, -40, 30, -70); b.close()
    inked(c, b, LG((0, -70), (0, 80), [(150, 220, 140), (80, 170, 90)]), 6)
    inked(c, path([(-34, -70), (34, -70), (20, -95), (-20, -95)]), P((120, 200, 120)), 5)
    ctext(c, '$', 0, 30, 70, (30, 100, 40), 'Anton.ttf'); c.restore()


def store_inside(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(240, 250, 255), (215, 238, 252)]))
    for row in range(3):
        y = 520 + row * 170
        inked(c, skia.Rect.MakeXYWH(40, y + 120, 1000, 18), P((200, 210, 225)), 4)
        rnd = random.Random(row)
        for i in range(12):
            x = 70 + i * 82; col = [(255, 90, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120), (170, 100, 255)][rnd.randint(0, 4)]
            hh = rnd.randint(70, 110); inked(c, skia.Rect.MakeXYWH(x, y + 120 - hh, 60, hh), P(col), 3)
            c.drawRect(skia.Rect.MakeXYWH(x + 8, y + 120 - hh + 15, 44, 14), P((255, 255, 255), 0.85))
    c.drawRect(skia.Rect.MakeXYWH(0, 1100, W, 820), LG((0, 1100), (0, H), [(230, 235, 245), (190, 200, 215)]))
    for i in range(-6, 7): c.drawLine(540 + i * 60, 1100, 540 + i * 300, H, S((255, 255, 255), 3, 0.6))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    th = ph('the real money')
    sky_bg(c, t, (170, 180, 195))
    building(c, 110, 760, 860, 560, (255, 245, 230), 'GROCERY', (40, 170, 90), t, True)
    board(c, 70, 250, 940, 200)
    neon_text(c, 'YOUR GROCERY STORE', 540, 340, 66, (40, 170, 90))
    neon_text(c, 'BARELY PROFITS ON FOOD', 540, 425, 60, (255, 70, 90))
    kx = pr(t, 0.0, 1.6)
    cart(c, lerp(-150, 700, eo(kx)), 1600, 1.0, 1.0, t)
    person(c, lerp(-420, 300, eo(kx)), 1700, 0.62, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.7, -0.2), t=t, arm_r=(200, -120), arm_l=(160, -80), blink=blinking(t))
    if t > th - 0.3:
        k = pr(t, th - 0.3, 0.4)
        burst_k = k
        pop(c, k, 760, 1000, lambda: (board(c, 600, 930, 320, 140, (255, 236, 90)), neon_text(c, '???', 760, 1030, 90, (255, 70, 90))))


def s_margin(c, t):
    t2 = ph('two cents'); tc = ph('hundred dollar'); tl = ph('the lights')
    store_inside(c, t)
    inked(c, skia.Rect.MakeXYWH(20, 1250, 1040, 50), LG((0, 1250), (0, 1300), [(255, 255, 255), (220, 225, 235)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1300, 1000, 650), LG((0, 1300), (0, H), [(60, 200, 120), (40, 160, 95)])); c.drawRect(skia.Rect.MakeXYWH(40, 1300, 1000, 650), S(INK, 7))
    register(c, 300, 1240, 0.0, None, t)
    cart(c, 760, 1690, 0.75, 1.0, t)
    rk = pr(t, tc - 0.4, 1.0)
    if rk > 0:
        rl = 500 * eo(rk); r = skia.Rect.MakeXYWH(440, 1240 - rl, 170, rl); inked(c, r, P((255, 255, 255)), 4)
        for i in range(int(rl / 40)): c.drawLine(460, 1220 - i * 40, 590 - (i % 3) * 30, 1220 - i * 40, S((170, 170, 190), 5))
        if rk > 0.6: ctext(c, '$100', 525, 1240 - rl + 60, 46, (40, 40, 60), 'Anton.ttf')
    if t > t2 - 0.3:
        k = pr(t, t2 - 0.3, 0.4)
        def big():
            coin(c, 800, 900, 140)
            neon_text(c, '2¢', 800, 935, 110, (255, 255, 255))
        pop(c, k, 800, 900, big)
        if t > t2 + 0.5: neon_text(c, 'OF EVERY $1', 800, 1100, 48, (40, 170, 90), pr(t, t2 + 0.5, 0.3))
    if t > tc: sticky(c, 800, 1180, 1.0, 6, '= ~$2', size=60) if t < tl - 0.3 else None
    for i, lab in enumerate(('LIGHTS', 'STAFF', 'FREEZERS')):
        kb = pr(t, tl - 0.3 + i * 0.35, 0.35)
        if kb > 0: bill(c, 650 + i * 140, 1150 - 40 * i, kb, t, -10 + i * 10, lab)


def bill(c, x, y, k, t, rot, s):
    if k <= 0: return
    sc = min(1, k * 1.5); c.save(); c.translate(x, y); c.rotate(rot + 4 * math.sin(t * 3 + x)); c.scale(sc, sc)
    c.drawRect(skia.Rect.MakeXYWH(-90 + 8, -110 + 8, 180, 220), P(INK, 0.3)); inked(c, skia.Rect.MakeXYWH(-90, -110, 180, 220), P((255, 252, 240)), 6)
    ctext(c, s, 0, -50, 34 if len(s) > 6 else 40, (220, 40, 60), 'Anton.ttf')
    for i in range(4): c.drawLine(-70, -10 + i * 30, 60 - (i % 2) * 40, -10 + i * 30, S((170, 170, 190), 5))
    c.restore()


def s_ads(c, t):
    ts = ph('screen at checkout'); tco = ph('the coupon'); tsp = ph('the sponsored'); ta = ph('those are ads'); tp = ph('brands pay')
    store_inside(c, t)
    if t < ta - 0.2:
        board(c, 120, 260, 840, 150); neon_text(c, "WHERE'S THE MONEY?", 540, 360, 64, (30, 160, 255))
        pop(c, pr(t, ts - 0.3, 0.35), 250, 820, lambda: (tv(c, 250, 820, 360, t), neon_text(c, 'AD', 250, 860, 110, (255, 255, 255))))
        pop(c, pr(t, tco - 0.3, 0.35), 760, 900, lambda: phone(c, 760, 900, 0.75, 6, lambda cc: (cc.drawRect(skia.Rect.MakeXYWH(20, 120, 240, 200), P((255, 236, 90))), ctext(cc, 'COUPON', 140, 200, 44, (220, 40, 60), 'Anton.ttf'), ctext(cc, '$1 OFF', 140, 270, 50, (40, 40, 60), 'Anton.ttf'))))
        def search(cc):
            for i in range(4):
                y = 40 + i * 120; cc.drawRect(skia.Rect.MakeXYWH(20, y, 240, 100), P((240, 245, 250))); cc.drawRect(skia.Rect.MakeXYWH(20, y, 70, 100), P([(255, 90, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120)][i]))
                if i == 0: cc.drawRect(skia.Rect.MakeXYWH(100, y + 10, 150, 30), P((255, 214, 40))); ctext(cc, 'SPONSORED', 175, y + 34, 22, (40, 40, 60))
        pop(c, pr(t, tsp - 0.3, 0.35), 520, 1230, lambda: phone(c, 520, 1230, 0.6, -5, search))
    else:
        board(c, 120, 260, 840, 150); neon_text(c, 'THOSE ARE ADS', 540, 360, 74, (255, 70, 90))
        person(c, 780, 1700, 0.62, (70, 140, 255), (40, 170, 90), mood='happy', look=(-0.7, 0), t=t, arm_r=(-160, 120), arm_l=(-60, 220), tie=(255, 214, 40), shirt=(250, 250, 255), blink=blinking(t, 2))
        for i in range(3):
            kk = pr(t, tp - 0.2 + i * 0.25, 0.4)
            x = 200 + i * 40; y = 1700 - i * 10
            if kk > 0:
                person(c, 200 + i * 160 - 120 * (1 - eo(kk)), 1760, 0.42, [(170, 110, 255), (255, 90, 120), (60, 200, 120)][i], [(90, 60, 140), (200, 60, 70), (40, 120, 90)][i], mood='happy', t=t, arm_r=(120, -40), arm_l=(-30, 230), blink=blinking(t, i + 3))
                u = pr(t, tp + 0.3 + i * 0.25, 0.6)
                moneybag(c, lerp(260 + i * 160, 660, eio(u)), lerp(1480, 1300, eio(u)) - 80 * math.sin(math.pi * u), 0.8, -10 + 20 * u)


def s_big(c, t):
    th = ph('how big'); t64 = ph('six point four'); tm = ph('membership fees')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        k = pr(t, t64 - 0.4, 0.4)
        ctext(cc, "WALMART'S AD BUSINESS", 410, 70, 40, (255, 255, 255))
        if k > 0: neon_text(cc, '~$6.4 BILLION', 410, 250, 104, (80, 230, 140), cl(k * 2))
        ctext(cc, 'FISCAL 2026, PER WALMART RESULTS', 410, 330, 24, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
    screen(c, 130, 300, 820, 380, d, (80, 230, 140))
    dim = pr(t, th - 0.1, 0.4) * (1 - pr(t, t64 - 0.2, 0.25))
    if t > tm - 0.3:
        k = pr(t, tm - 0.3, 0.4)
        def card_():
            giftcard(c, 540, 1010, 560, -5, (40, 120, 220), '', 1.0, sparkle_=True, t=t)
            neon_text(c, 'MEMBERSHIP', 540, 960, 56, (255, 255, 255)); neon_text(c, '$4.3B+', 540, 1090, 100, (255, 214, 40))
        pop(c, k, 540, 1010, card_)
    else:
        rnd = random.Random(2)
        for i in range(int(16 * pr(t, t64, 1.2))):
            moneybag(c, 140 + (i * 197) % 820, 1150 - (i // 5) * 90 + rnd.uniform(-20, 20), 0.75, rnd.uniform(-20, 20))
    person(c, 900, 1800, 0.56, (255, 140, 40), (36, 44, 90), mood='shock', look=(-0.6, -0.7), sweat=2, t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.4 * dim))


def s_customer(c, t):
    tn = ph("it's not you"); tb = ph("it's the brands")
    store_inside(c, t)
    c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.25))
    board(c, 100, 260, 880, 150); neon_text(c, 'WHO IS THE REAL CUSTOMER?', 540, 352, 50, (30, 160, 255))
    sp = 1.0 if t < tb - 0.2 else 0.0
    light_cone(c, 280, 420, 60, 420, 1400, (255, 255, 220), 0.35 * sp + 0.05)
    light_cone(c, 780, 420, 60, 460, 1400, (255, 255, 220), 0.05 + 0.4 * (1 - sp))
    cart(c, 300, 1600, 0.7, 1.0, t)
    person(c, 260, 1800, 0.6, (255, 140, 40), (36, 44, 90), mood='happy' if t < tn else 'shock', look=(0.6, -0.4), t=t, arm_r=(100, -40), arm_l=(-30, 230), blink=blinking(t))
    for i in range(3):
        person(c, 660 + i * 150, 1780, 0.42, [(170, 110, 255), (255, 90, 120), (60, 200, 120)][i], [(90, 60, 140), (200, 60, 70), (40, 120, 90)][i], mood='happy', t=t, arm_r=(40, -200), arm_l=(-30, 230), blink=blinking(t, i))
        moneybag(c, 690 + i * 150, 1360, 0.7, 10)
    if t > tn - 0.2: pop(c, pr(t, tn - 0.2, 0.3), 260, 980, lambda: (board(c, 120, 920, 280, 110, (255, 255, 255)), neon_text(c, 'NOT YOU?', 260, 1000, 54, (255, 70, 90))))
    if t > tb - 0.2: pop(c, pr(t, tb - 0.2, 0.3), 810, 980, lambda: (board(c, 620, 920, 380, 110, (255, 236, 90)), neon_text(c, 'THE BRANDS', 810, 1000, 54, (40, 170, 90))))


def s_end(c, t):
    tm = ph('you came in'); ta = ph('your attention'); tq = ph('do you ever')
    sky_bg(c, t)
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOU CAME FOR MILK', 540, 355, 70, (30, 160, 255)); neon_text(c, 'THEY CAME FOR YOU', 540, 440, 70, (255, 70, 90), pr(t, ta - 0.6, 0.3))
        pop(c, pr(t, tm, 0.4), 330, 1100, lambda: milk(c, 330, 1100, 2.2, -8))
        if t > ta - 0.4:
            def eye():
                c.drawOval(skia.Rect.MakeXYWH(620, 950, 300, 170), P((255, 255, 255))); c.drawOval(skia.Rect.MakeXYWH(620, 950, 300, 170), S(INK, 8))
                c.drawCircle(770 + 20 * math.sin(t * 2), 1035, 60, P((40, 120, 220))); c.drawCircle(770 + 20 * math.sin(t * 2), 1035, 28, P(INK)); c.drawCircle(755, 1020, 10, P((255, 255, 255)))
            pop(c, pr(t, ta - 0.4, 0.4), 770, 1035, eye)
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'DO YOU TAP THE', 540, 355, 70, (30, 160, 255)); neon_text(c, 'SPONSORED STUFF?', 540, 440, 70, (255, 190, 30))
        for x, lab, col in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 130, 590, 260, 120, col), neon_text(c, lab, x, 680, 80, (255, 255, 255))))
    person(c, 540, 1660, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_hook), (ph('the food industry') - 0.15, s_margin), (ph("so where's the") - 0.15, s_ads), (ph('how big') - 0.15, s_big),
    (ph("so who's the") - 0.15, s_customer), (ph('you came in') - 0.15, s_end)]
SHAKES = [(ph('two cents'), 10, 0.35), (ph('six point four'), 18, 0.45), (ph('four point three'), 10, 0.35), (ph("it's the brands"), 8, 0.3)]
TR = 0.32
