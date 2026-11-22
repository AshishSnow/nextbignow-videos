# ------------------------------------------------------------------ Black Friday props
SEPIA = skia.ColorFilters.Matrix([0.393 * 1.05, 0.769 * 1.05, 0.189 * 1.05, 0, 0.02,
                                  0.349, 0.686, 0.168, 0, 0.0,
                                  0.272 * 0.9, 0.534 * 0.9, 0.131 * 0.9, 0, 0.0,
                                  0, 0, 0, 1, 0])


def retro(fn, stamp):
    """flashback scenes (sketch mode): same drawing, plus a red date stamp."""
    def wrapped(c, t):
        fn(c, t)
        c.save(); c.translate(820, 560); c.rotate(-8)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -50, 340, 100), 14, 14); c.drawRRect(r, S((200, 40, 40), 8, 0.9))
        ctext(c, stamp, 0, 18, 50, (230, 40, 50), 'Anton.ttf', 0.9); c.restore()
    return wrapped


def cop(c, x, y, s, mood='worried', look=(0, 0), t=0.0, arm_r=None, arm_l=None, blink=False):
    person(c, x, y, s, (255, 190, 140), (30, 50, 110), mood=mood, look=look, t=t, arm_r=arm_r, arm_l=arm_l, tie=(20, 30, 60), shirt=(200, 220, 255), blink=blink)
    hx, hy, r = x, y - 640 * s, 185 * s
    cap = skia.Path(); cap.moveTo(hx - r * 0.95, hy - r * 0.45); cap.cubicTo(hx - r, hy - r * 1.35, hx + r, hy - r * 1.35, hx + r * 0.95, hy - r * 0.45); cap.close()
    inked(c, cap, P((30, 50, 110)), 7 * s / 0.6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(hx - r * 1.05, hy - r * 0.55, r * 2.1, r * 0.22), r * 0.1, r * 0.1), P((20, 25, 45)), 6 * s / 0.6)
    star = path([(hx + r * 0.2 * math.cos(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.45), hy - r * 0.85 + r * 0.2 * math.sin(math.radians(-90 + i * 36)) * (1 if i % 2 == 0 else 0.45)) for i in range(10)])
    inked(c, star, P((255, 214, 40)), 3)


def football(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, skia.Path().addOval(skia.Rect.MakeXYWH(-110, -65, 220, 130)), LG((0, -65), (0, 65), [(170, 90, 50), (120, 60, 30)]), 7)
    c.drawLine(-50, 0, 50, 0, S((255, 255, 255), 7))
    for i in range(5): c.drawLine(-36 + i * 18, -14, -36 + i * 18, 14, S((255, 255, 255), 6))
    c.restore()


def bag(c, x, y, s=1.0, col=(255, 70, 90), rot=0, lab=''):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    h = skia.Path(); h.moveTo(-40, -90); h.cubicTo(-40, -150, 40, -150, 40, -90); c.drawPath(h, S(INK, 10))
    inked(c, path([(-90, -90), (90, -90), (100, 110), (-100, 110)]), LG((0, -90), (0, 110), [tuple(min(255, v + 50) for v in col), col]), 7)
    if lab: ctext(c, lab, 0, 30, 54, (255, 255, 255), 'Anton.ttf')
    c.restore()


def ledger(c, x, y, s, k_red, k_black, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-360, -230, 720, 460), 20, 20), P((90, 60, 40)), 8)
    for sx in (-1, 1):
        inked(c, skia.Rect.MakeXYWH(-340 if sx < 0 else 0, -210, 340, 420), P((255, 252, 235)), 5)
    for i in range(8):
        c.drawLine(-330, -170 + i * 48, -10, -170 + i * 48, S((180, 200, 230), 3)); c.drawLine(10, -170 + i * 48, 330, -170 + i * 48, S((180, 200, 230), 3))
    if k_red > 0: neon_text(c, '- $', -170, 40, int(150 * min(1, k_red * 1.4)) + 1, (230, 40, 50)); ctext(c, 'LOSS', -170, 150, 50, (230, 40, 50), 'Anton.ttf', cl(k_red * 2))
    if k_black > 0: neon_text(c, '+ $', 170, 40, int(150 * min(1, k_black * 1.4)) + 1, (40, 40, 50)); ctext(c, 'PROFIT', 170, 150, 50, (40, 40, 50), 'Anton.ttf', cl(k_black * 2))
    c.restore()


def city_bg(c, t, modern=True):
    if modern:
        c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (230, 245, 255)], [0, 0.5, 1]))
        c.drawCircle(880, 300, 90, P((255, 255, 230))); c.drawCircle(880, 300, 200, P((255, 255, 220), 0.5, 70))
    else:
        c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(150, 190, 230), (220, 230, 240)]))
    rnd = random.Random(7)
    x = -20
    while x < W:
        w = rnd.randint(120, 200); h = rnd.randint(380, 640); col = rnd.choice([(230, 120, 90), (240, 200, 120), (150, 190, 230), (200, 150, 220), (120, 200, 170)])
        inked(c, skia.Rect.MakeXYWH(x, 1250 - h, w, h + 50), P(col), 5)
        for wy in range(1250 - h + 30, 1200, 70):
            for wx in range(x + 20, x + w - 30, 50): c.drawRect(skia.Rect.MakeXYWH(wx, wy, 26, 36), P((255, 250, 220) if (wx + wy) % 3 else (80, 100, 140)))
        x += w + 6
    c.drawRect(skia.Rect.MakeXYWH(0, 1250, W, 670), LG((0, 1250), (0, H), [(150, 160, 175), (110, 120, 135)]))


def store_front(c, t):
    city_bg(c, t)
    inked(c, skia.Rect.MakeXYWH(100, 830, 880, 420), P((255, 250, 240)), 7)
    inked(c, skia.Rect.MakeXYWH(80, 770, 920, 100), P((30, 30, 40)), 7)
    neon_text(c, 'MEGA SALE', 540, 845, 64, (255, 214, 40), 1.0 if (t % 1.3) > 0.1 else 0.5)
    for i in range(3):
        r = skia.Rect.MakeXYWH(140 + i * 280, 900, 240, 330); inked(c, r, LG((0, 850), (0, 1230), [(150, 220, 255), (90, 160, 230)]), 5)
        sticky(c, 260 + i * 280, 1010, 0.9, -8 + i * 8, ['-50%', '-70%', '-40%'][i], size=56)


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tl = ph('finally profit'); tp = ph('angry cops')
    store_front(c, t)
    c.save(); c.translate(540, 235); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-190, -42, 380, 76), P((212, 160, 46))); f = serif(44, 400, True); tw = f.measureText('in 45 seconds'); c.drawString('in 45 seconds', -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col) in enumerate((("Black Friday's", False, (34, 32, 30)), ('real name,', False, (34, 32, 30)), ('explained.', True, (150, 22, 34)))):
        f = serif(108 if i < 2 else 112, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 118, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); s_ = "it's not about profit"; c.drawString(s_, 540 - f.measureText(s_) / 2, 695, f, P((90, 86, 80), pr(t, tl - 0.5, 0.3)))
    people(c, 130, 1760, 5, 1.25, 0, pr(t, 0.0, 2.0), t, hold=False)
    for i in range(4):
        if pr(t, 0.3 + i * 0.3, 0.3) > 0: bag(c, 230 + i * 220, 1640, 0.55, [(255, 70, 90), (40, 170, 255), (255, 190, 30), (60, 200, 120)][i], -8 + i * 6)
    if t > tp - 0.3:
        def siren():
            board(c, 300, 1080, 480, 120, (30, 50, 110)); neon_text(c, 'POLICE', 540, 1168, 80, (255, 255, 255))
            for sx, col in ((-1, (255, 40, 60)), (1, (40, 120, 255))):
                c.drawCircle(540 + sx * 300, 1140, 40, P(col)); c.drawCircle(540 + sx * 300, 1140, 40, S(INK, 6))
        pop(c, pr(t, tp - 0.3, 0.35), 540, 1140, siren)


def _s_1950(c, t):
    tf = ph('football game'); tj = ph('traffic jams'); tsw = ph('packed sidewalks'); ts = ph('extra long shifts')
    city_bg(c, t, False)
    board(c, 90, 250, 900, 150); neon_text(c, "THEY CALLED IT 'BLACK FRIDAY'", 540, 348, 46, (30, 30, 40))
    if t > tj - 0.3:
        for i in range(3):
            kk = pr(t, tj - 0.3 + i * 0.15, 0.4)
            if kk > 0: car(c, lerp(1400, 200 + i * 340, eo(kk)), 1290, 300, [(232, 38, 60), (40, 120, 220), (60, 170, 90)][i], 0)
    k = pr(t, ph('why huge crowds'), 1.6) if t > ph('why huge crowds') - 0.1 else 0
    people(c, 70, 1560, 6, 1.1, 0, k, t, hold=False)
    if t > tf - 0.3: pop(c, pr(t, tf - 0.3, 0.35), 300, 800, lambda: (football(c, 300, 780, 1.3, -20), ctext(c, 'ARMY-NAVY GAME', 300, 910, 44, (30, 30, 40), 'Anton.ttf')))
    cop(c, 540, 1880, 0.6, 'worried' if t < ts else 'shock', (0, -0.6), t, arm_r=(140, -200), arm_l=(-30, 220), blink=blinking(t))
    if t > ts - 0.3:
        def clock():
            c.drawCircle(860, 1100, 110, P((255, 255, 255))); c.drawCircle(860, 1100, 110, S(INK, 8))
            a = t * 6; c.drawLine(860, 1100, 860 + 70 * math.cos(a), 1100 + 70 * math.sin(a), S(INK, 9)); c.drawLine(860, 1100, 860 + 45 * math.cos(a / 12), 1100 + 45 * math.sin(a / 12), S(INK, 11))
            ctext(c, 'EXTRA SHIFTS', 860, 1260, 40, (200, 40, 40), 'Anton.ttf')
        pop(c, pr(t, ts - 0.3, 0.35), 860, 1100, clock)


def _s_rebrand(c, t):
    tb = ph('big friday'); tf = ph('it flopped')
    city_bg(c, t, False)
    board(c, 90, 250, 900, 150); neon_text(c, 'STORES HATED THE NAME', 540, 350, 60, (30, 30, 40))
    if t > tb - 0.4:
        def banner():
            inked(c, path([(120, 760), (960, 760), (930, 1020), (150, 1020)]), P((255, 236, 90)), 8)
            neon_text(c, "IT'S 'BIG FRIDAY'!", 540, 920, 78, (40, 120, 220))
        pop(c, pr(t, tb - 0.4, 0.4), 540, 890, banner)
    person(c, 320, 1780, 0.55, (255, 190, 140), (120, 60, 40), mood='happy' if t < tf else 'worried', look=(0.5, -0.6), t=t, arm_r=(160, -260), arm_l=(-30, 220), tie=(200, 40, 40), shirt=(255, 255, 255), blink=blinking(t))
    if t > tf - 0.2:
        k = pr(t, tf - 0.2, 0.3)
        def nope():
            c.drawLine(160, 780, 920, 1000, S((220, 30, 40), 30)); c.drawLine(920, 780, 160, 1000, S((220, 30, 40), 30))
            c.save(); c.translate(760, 1250); c.rotate(-10); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-200, -70, 400, 140), 16, 16); c.drawRRect(r, S((220, 30, 40), 12)); ctext(c, 'FLOPPED', 0, 32, 90, (220, 30, 40), 'Anton.ttf'); c.restore()
        pop(c, k, 540, 900, nope)


s_1950 = retro(_s_1950, 'PHILLY, 1950s')
s_rebrand = retro(_s_rebrand, 'EARLY 1960s')


def s_ledger(c, t):
    tr = ph('red ink'); tb = ph('black ink'); tl = ph('late eighties'); tc = 1e9
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 150, 90), (255, 205, 140), (255, 235, 190)]))
    board(c, 90, 250, 900, 150); neon_text(c, "THE 'IN THE BLACK' STORY", 540, 350, 58, (30, 30, 40))
    if t > tl - 0.3:
        c.save(); c.translate(820, 520); c.rotate(-8); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -50, 340, 100), 14, 14); c.drawRRect(r, P((255, 255, 255))); c.drawRRect(r, S((30, 30, 40), 8)); ctext(c, 'LATE 1980s', 0, 18, 50, (30, 30, 40), 'Anton.ttf'); c.restore()
    if t < tc - 0.3:
        ledger(c, 540, 960, 1.15, pr(t, tr - 0.3, 0.4), pr(t, tb - 0.3, 0.4), t)
    else:
        k = pr(t, tc - 0.3, 0.8)
        cop(c, 260, 1560, 0.45, 'worried', (0.6, -0.4), t, blink=blinking(t))
        board(c, 380, 820, 300, 130, (255, 255, 255)); ctext(c, 'UGH!', 530, 910, 70, (220, 40, 50), 'Anton.ttf')
        for i in range(5):
            v = cl(k * 1.6 - i * 0.12)
            if v > 0: bag(c, lerp(530, 560 + (i - 2) * 130, eo(v)), lerp(900, 1200 + (i % 2) * 90, eo(v)), 0.6 * eo(v) + 0.01, [(255, 70, 90), (40, 170, 255), (255, 190, 30), (60, 200, 120), (170, 110, 255)][i], -10 + i * 5)
        if k > 0.7: pop(c, pr(t, tc + 0.5, 0.3), 700, 1560, lambda: (board(c, 440, 1500, 520, 110, (255, 236, 90)), neon_text(c, 'BIGGEST WEEKEND', 700, 1578, 54, (255, 70, 90))))


def s_big(c, t):
    tr = ph('a record'); tm = ph('three million')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    def d(cc):
        k = pr(t, tm - 0.5, 0.4)
        ctext(cc, 'THANKSGIVING WEEKEND 2025', 410, 70, 36, (255, 255, 255))
        if k > 0: neon_text(cc, '203 MILLION', 410, 250, 110, (255, 214, 40), cl(k * 2))
        ctext(cc, 'SHOPPERS, PER NRF (A RECORD)', 410, 330, 24, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
    screen(c, 130, 300, 820, 380, d, (255, 214, 40))
    k = pr(t, tr - 0.2, 1.6)
    for row in range(3):
        people(c, 90 + row * 60, 1150 + row * 170, 6, 1.0, 0, cl(k * 1.3 - row * 0.15), t + row, hold=False)


def s_end(c, t):
    tc = ph('congrats'); tq = 1e9
    city_bg(c, t)
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'STUCK IN TRAFFIC?', 540, 355, 70, (30, 30, 40)); neon_text(c, "THAT'S THE ORIGINAL", 540, 440, 60, (255, 70, 90), pr(t, tc - 0.3, 0.3))
        for i in range(4): car(c, 150 + i * 270 + 6 * math.sin(t * 8 + i), 1380 + (i % 2) * 140, 300, [(232, 38, 60), (40, 120, 220), (60, 170, 90), (255, 190, 30)][i], 0)
        if t > tc - 0.2:
            pop(c, pr(t, tc - 0.2, 0.3), 540, 900, lambda: (board(c, 300, 840, 480, 120, (255, 255, 255)), neon_text(c, 'HONK HONK', 540, 925, 66, (255, 70, 90))))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'SHOPPING BLACK', 540, 355, 70, (30, 30, 40)); neon_text(c, 'FRIDAY THIS YEAR?', 540, 440, 66, (255, 190, 30))
        for x, lab, col_ in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 130, 590, 260, 120, col_), neon_text(c, lab, x, 680, 80, (255, 255, 255))))
        person(c, 540, 1680, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t),
               prop=(1, lambda cc, ex, ey: bag(cc, ex + 20, ey + 40, 0.5)))


SCENES = [
    (0.0, s_hook), (ph('back in the') - 0.15, s_1950), (ph('stores hated') - 0.15, s_rebrand), (ph('so in the late') - 0.15, s_ledger),
    (ph('last thanksgiving') - 0.15, s_big), (ph("so if you're") - 0.15, s_end)]
SHAKES = [(ph('angry cops'), 10, 0.35), (ph('traffic jams'), 8, 0.3), (ph('it flopped'), 14, 0.4), (ph('black ink'), 8, 0.3), (ph('three million'), 18, 0.45)]
TR = 0.32
