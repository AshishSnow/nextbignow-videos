# ------------------------------------------------------------------ landlord props (generic burger place: no real logos or trade dress)
def burger(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    top = skia.Path(); top.moveTo(-90, -10); top.cubicTo(-90, -95, 90, -95, 90, -10); top.close()
    inked(c, top, LG((0, -90), (0, -10), [(250, 190, 100), (215, 140, 60)]), 6)
    for sx, sy in ((-40, -50), (0, -65), (35, -45), (-10, -35), (55, -30)): c.drawOval(skia.Rect.MakeXYWH(sx, sy, 12, 7), P((255, 245, 210)))
    inked(c, path([(-100, -8), (-60, 8), (-20, -4), (20, 10), (60, -4), (100, 8), (95, 18), (-95, 18)]), P((90, 200, 90)), 5)
    inked(c, path([(-95, 15), (95, 15), (95, 30), (-95, 30)]), P((255, 200, 40)), 5)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-92, 26, 184, 34), 16, 16), P((120, 60, 30)), 6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-88, 58, 176, 36), 18, 18), P((225, 150, 70)), 6)
    c.restore()


def fries(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for i in range(7):
        fx = -60 + i * 20; inked(c, skia.Rect.MakeXYWH(fx, -150 + (i % 3) * 18, 18, 120), P((255, 210, 70)), 4)
    inked(c, path([(-80, -40), (80, -40), (60, 100), (-60, 100)]), LG((0, -40), (0, 100), [(40, 190, 200), (20, 140, 160)]), 6)
    c.drawCircle(0, 30, 26, P((255, 255, 255))); c.restore()


def report(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-140 + 10, -180 + 12, 280, 360), P(INK, 0.3, 6))
    inked(c, skia.Rect.MakeXYWH(-140, -180, 280, 360), P((255, 255, 255)), 7)
    inked(c, skia.Rect.MakeXYWH(-140, -180, 280, 80), P((40, 90, 200)), 7)
    ctext(c, 'ANNUAL', 0, -145, 34, (255, 255, 255), 'Anton.ttf'); ctext(c, 'REPORT 2025', 0, -110, 30, (255, 255, 255), 'Anton.ttf')
    for i in range(6): c.drawLine(-110, -60 + i * 34, 110 - (i % 2) * 60, -60 + i * 34, S((170, 170, 190), 6))
    for i, h in enumerate((40, 70, 55, 100)): c.drawRect(skia.Rect.MakeXYWH(-100 + i * 50, 160 - h, 34, h), P((40, 190, 110)))
    c.restore()


def restaurant(c, x, y, w, t, sign='BURGERS', col=(40, 180, 190), lit=True):
    h = w * 0.62
    c.drawRect(skia.Rect.MakeXYWH(x + 12, y + 12, w, h), P((0, 0, 0), 0.3, 10))
    inked(c, skia.Rect.MakeXYWH(x, y, w, h), LG((x, y), (x, y + h), [(255, 250, 240), (235, 225, 210)]), 6)
    inked(c, path([(x - 20, y + 10), (x + w + 20, y + 10), (x + w, y - h * 0.18), (x, y - h * 0.18)]), P(col), 6)
    r = skia.Rect.MakeXYWH(x + w * 0.08, y + h * 0.3, w * 0.55, h * 0.55); inked(c, r, P((255, 210, 120) if lit else (150, 170, 200)), 5)
    if lit: c.drawRect(r, P((255, 200, 90), 0.3, 20))
    inked(c, skia.Rect.MakeXYWH(x + w * 0.7, y + h * 0.35, w * 0.22, h * 0.65), P((120, 80, 60)), 5)
    ctext(c, sign, x + w / 2, y - h * 0.02, w * 0.12, (255, 255, 255), 'Anton.ttf')


def land(c, x, y, w, t, k=1.0):
    h = w * 0.35
    inked(c, path([(x, y), (x + w, y), (x + w * 0.85, y + h), (x - w * 0.15, y + h)]), LG((0, y), (0, y + h), [(140, 210, 110), (90, 170, 80)]), 6)
    for i in range(5): c.drawLine(x + 20 + i * w / 5, y + 10, x - 10 + i * w / 5, y + h - 10, S((120, 190, 100), 3))
    if k > 0:
        c.save(); c.translate(x + w * 0.8, y + h * 0.4); c.scale(k, k)
        c.drawLine(0, 0, 0, -140, S(INK, 8)); inked(c, skia.Rect.MakeXYWH(0, -140, 130, 70), P((255, 255, 255)), 5); ctext(c, 'OWNED', 65, -95, 34, (40, 90, 200), 'Anton.ttf')
        c.restore()


def bars2(c, t, kA, kB, labA, labB, valA, valB, hA, hB, colA=(255, 120, 60), colB=(40, 190, 110), cmp_k=0, cmp_txt=''):
    base = 1180
    def col(x, val, h, rgb, lab, k):
        if k <= 0: return
        hh = h * eo(k)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, base - hh, 300, hh), 18, 18)
        c.drawRRect(r.makeOffset(10, 12), P(INK, 0.25, 6)); inked(c, r, LG((x, base - hh), (x, base), [tuple(min(255, v + 60) for v in rgb), rgb]), 7)
        neon_text(c, val, x + 150, base - hh - 30, 70, rgb, cl(k * 2))
        neon_text(c, lab, x + 150, base + 70, 38, (255, 255, 255))
    inked(c, skia.Rect.MakeXYWH(60, base, 960, 14), P((255, 255, 255)), 5)
    col(140, valA, hA, colA, labA, kA); col(640, valB, hB, colB, labB, kB)
    if cmp_k > 0:
        pop(c, cmp_k, 540, 1610, lambda: (board(c, 250, 1550, 580, 110, (255, 236, 90)), neon_text(c, cmp_txt, 540, 1628, 64, (255, 70, 90))))


def street(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (230, 245, 255)], [0, 0.5, 1]))
    c.drawCircle(880, 300, 90, P((255, 255, 230))); c.drawCircle(880, 300, 200, P((255, 255, 220), 0.5, 70))
    cloud(c, 80 + 20 * math.sin(t * 0.3), 560, 0.6); cloud(c, 700 - 15 * math.sin(t * 0.25), 660, 0.5)
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(150, 160, 175), (110, 120, 135)]))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(-60 + i * 220 - (t * 120) % 220, 1590, 120, 16), P((255, 255, 255), 0.8))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tp = ph('annual report'); td = 1e9
    street(c, t)
    k0 = pr(t, 0.0, 0.5)
    c.save(); c.translate(540, 235); c.rotate(-2); r = skia.Rect.MakeXYWH(-190, -42, 380, 76); c.drawRect(r, P((212, 160, 46))); c.restore()
    c.save(); c.translate(540, 235); c.rotate(-2); f = serif(44, 400, True); tw = f.measureText('in 60 seconds'); c.drawString('in 60 seconds', -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col) in enumerate((("McDonald's is", False, (34, 32, 30)), ('a landlord,', False, (34, 32, 30)), ('explained.', True, (150, 22, 34)))):
        f = serif(108 if i < 2 else 112, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 118, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); s_ = 'per its 2025 annual report'; c.drawString(s_, 540 - f.measureText(s_) / 2, 695, f, P((90, 86, 80), pr(t, 0.8, 0.3)))
    restaurant(c, 250, 960, 580, t)
    kx = pr(t, 0.0, 1.4)
    person(c, lerp(-200, 170, eo(kx)), 1760, 0.6, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.6, -0.4), t=t, arm_r=(150, -120), arm_l=(-30, 220), blink=blinking(t),
           prop=(1, lambda cc, ex, ey: burger(cc, ex + 40, ey - 40, 0.6)))
    if t > tp - 0.4: pop(c, pr(t, tp - 0.4, 0.4), 800, 1330, lambda: report(c, 800, 1360, 0.95, 6))
    if t > td - 0.5:
        u = pr(t, td - 0.5, 1.6); car(c, lerp(1300, 600, eo(u)), 1720, 420, (255, 80, 90), t)


def s_big(c, t):
    t10 = ph('ten billion'); t97 = ph('nine point seven'); tr = ph('rent wins')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    board(c, 80, 250, 920, 150); neon_text(c, "McDONALD'S, 2025", 540, 352, 70, (40, 90, 200))
    ctext(c, "SOURCE: McDONALD'S 2025 ANNUAL REPORT (10-K)", 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t10 - 0.3, 0.8), pr(t, t97 - 0.3, 0.8), 'RENT', 'OWN-RESTAURANT SALES', '$10.4B', '$9.7B', 10.44 * 55, 9.69 * 55, (40, 190, 110), (255, 120, 60), pr(t, tr - 0.2, 0.3), 'RENT > BURGERS')
    if t > t97: burger(c, 790, 1380 - 60 * pr(t, t97, 0.5), 0.0001 + 0.7 * pr(t, t97, 0.4))
    person(c, 960, 1840, 0.38, (255, 140, 40), (36, 44, 90), mood='shock' if t > t10 else 'neutral', look=(-0.6, -0.7), sweat=2 if t > tr else 0, t=t, blink=blinking(t))


def s_who(c, t):
    tf = ph('franchise owners'); t95 = ph('ninety five'); tl = ph('the land'); trt = ph('rents it to them'); tc = ph('a cut of')
    street(c, t)
    if t < tl - 0.4:
        board(c, 120, 260, 840, 150); neon_text(c, "WHO'S PAYING THE RENT?", 540, 358, 58, (40, 90, 200))
        n = 20
        for i in range(n):
            k = pr(t, tf - 0.3 + i * 0.05, 0.3)
            x, y = 95 + (i % 5) * 190, 620 + (i // 5) * 160
            franch = i != 7
            col = (40, 180, 190) if franch else (255, 120, 60)
            pop(c, k, x + 70, y + 50, lambda: restaurant(c, x, y, 140, t, '', col))
        if t > t95 - 0.2:
            pop(c, pr(t, t95 - 0.2, 0.3), 540, 1300, lambda: (board(c, 220, 1240, 640, 120, (255, 236, 90)), neon_text(c, '~95% FRANCHISED', 540, 1325, 64, (40, 140, 160))))
        return
    board(c, 120, 260, 840, 150); neon_text(c, 'HOW IT WORKS', 540, 358, 70, (40, 90, 200))
    land(c, 160, 1040, 760, t, pr(t, tl - 0.2, 0.4))
    kb = pr(t, tl + 0.2, 0.5)
    if kb > 0:
        c.save(); c.translate(0, -200 * (1 - eo(kb))); restaurant(c, 300, 760, 480, t); c.restore()
    person(c, 190, 1760, 0.5, (90, 200, 120), (40, 180, 190), mood='happy', look=(0.6, -0.4), t=t, arm_r=(120, -60), arm_l=(-30, 220), shirt=(255, 255, 255), blink=blinking(t, 2))
    ctext(c, 'FRANCHISEE', 250, 1290, 30, (255, 255, 255), 'Anton.ttf')
    person(c, 890, 1760, 0.5, (255, 140, 40), (40, 90, 200), mood='happy', look=(-0.6, -0.4), t=t, arm_r=(40, 220), arm_l=(-120, -60), tie=(255, 214, 40), shirt=(255, 255, 255), blink=blinking(t))
    ctext(c, "McDONALD'S", 830, 1290, 30, (255, 255, 255), 'Anton.ttf')
    u = pr(t, trt - 0.2, 1.0)
    if u > 0:
        for i in range(3):
            v = cl(u * 1.4 - i * 0.2)
            if 0 < v < 1: moneybag(c, lerp(290, 780, eio(v)), 1330 - 80 * math.sin(math.pi * v), 0.6, -10 + 20 * v)
        neon_text(c, 'RENT', 540, 1280, 54, (40, 170, 90), cl(u * 2))
    if t > tc - 0.2:
        for i in range(5):
            v = pr(t, tc - 0.2 + i * 0.12, 0.7)
            if 0 < v < 1: coin(c, lerp(290, 780, eio(v)), 1460 - 60 * math.sin(math.pi * v), 26)
        pop(c, pr(t, tc - 0.2, 0.3), 540, 1530, lambda: (board(c, 300, 1490, 480, 90, (255, 236, 90)), neon_text(c, '+ A CUT OF SALES', 540, 1555, 44, (255, 70, 90))))


def s_genius(c, t):
    t15 = ph('fifteen cents'); t84 = ph('eighty four')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 150, 90), (255, 205, 140), (255, 235, 190)]))
    board(c, 120, 260, 840, 150); neon_text(c, "WHY IT'S GENIUS", 540, 358, 70, (40, 90, 200))
    def row(y, lab, frac, k, colk, txt):
        if k <= 0: return
        board(c, 90, y, 900, 260, (255, 255, 255))
        ctext(c, lab, 540, y + 70, 44, (40, 40, 60), 'Anton.ttf')
        x0, w, h = 140, 800, 110
        c.drawRect(skia.Rect.MakeXYWH(x0, y + 100, w, h), P((235, 235, 240)))
        c.drawRect(skia.Rect.MakeXYWH(x0, y + 100, w * frac * eo(k), h), P(colk))
        c.drawRect(skia.Rect.MakeXYWH(x0, y + 100, w, h), S(INK, 7))
        if k > 0.5: ctext(c, txt, x0 + max(70, w * frac / 2), y + 180, 70, (255, 255, 255), 'Anton.ttf')
    row(480, 'ITS OWN RESTAURANTS KEEP', 0.15, pr(t, t15 - 0.3, 0.6), (255, 120, 60), '15¢')
    row(800, 'FRANCHISE MONEY KEEPS', 0.84, pr(t, t84 - 0.3, 0.6), (40, 190, 110), '84¢')
    ctext(c, 'MARGINS, OUR MATH FROM THE 2025 10-K', 540, 1110, 26, (90, 60, 40), 'Montserrat-ExtraBold.ttf')
    person(c, 540, 1800, 0.5, (255, 140, 40), (36, 44, 90), mood='shock' if t > t84 else 'happy', look=(0, -0.7), t=t, blink=blinking(t))


def s_reveal(c, t):
    ts = ph('sells burgers'); tb = ph('on the building')
    street(c, t)
    if t < tb - 0.4:
        board(c, 120, 260, 840, 150); neon_text(c, 'IT SELLS BURGERS...', 540, 358, 66, (40, 90, 200))
        burger(c, 540, 900, 2.4 + 0.05 * math.sin(t * 3))
        if t > ts - 0.2: pop(c, pr(t, ts - 0.2, 0.3), 540, 1260, lambda: (board(c, 380, 1200, 320, 110, (255, 255, 255)), neon_text(c, 'BUT...', 540, 1278, 60, (40, 170, 90))))
        return
    pop(c, pr(t, tb - 0.4, 0.35), 540, 330, lambda: (board(c, 100, 260, 880, 150, (255, 236, 90)), neon_text(c, 'THE REAL BUSINESS:', 540, 358, 66, (255, 70, 90))))
    land(c, 160, 1080, 760, t, 1.0)
    u = pr(t, tb, 0.8)
    c.save(); c.translate(0, -260 * eo(u)); restaurant(c, 300, 800, 480, t); c.restore()
    if u > 0.5:
        pop(c, pr(t, tb + 0.4, 0.3), 540, 1530, lambda: (board(c, 190, 1470, 700, 110, (255, 255, 255)), neon_text(c, 'THE BUILDING + LAND', 540, 1548, 58, (40, 90, 200))))
        for i in range(6):
            sparkle(c, 250 + i * 110, 1120 + 30 * math.sin(t * 4 + i), 26)


def s_end(c, t):
    tr = ph('paid rent'); tq = ph('would you rather')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(40, 180, 190), (150, 230, 225), (240, 250, 245)]))
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'GRABBING FRIES?', 540, 355, 70, (40, 90, 200)); neon_text(c, 'SOMEONE PAID RENT', 540, 440, 66, (255, 70, 90), pr(t, tr - 0.5, 0.3))
        inked(c, skia.Rect.MakeXYWH(60, 1120, 960, 70), P((255, 255, 255)), 7)
        c.drawRect(skia.Rect.MakeXYWH(60, 1190, 960, 400), LG((0, 1190), (0, 1590), [(40, 180, 190), (20, 130, 140)]))
        fries(c, 330, 1060, 1.3, -6); burger(c, 700, 1060, 1.1)
        if t > tr - 0.3: pop(c, pr(t, tr - 0.3, 0.3), 540, 1320, lambda: sticky(c, 540, 1330, 1.2, -5, 'RENT: PAID', size=54))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'OWN THE RESTAURANT', 540, 355, 62, (40, 90, 200)); neon_text(c, 'OR THE LAND?', 540, 440, 70, (255, 120, 40))
        for x, lab, col_ in ((290, 'RESTAURANT', (255, 120, 60)), (790, 'LAND', (40, 190, 110))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 200, 590, 400, 120, col_), neon_text(c, lab, x, 675, 50, (255, 255, 255))))
        person(c, 540, 1680, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_hook), (ph('its own annual') - 0.15, s_big), (ph('so who pays') - 0.15, s_who), (ph("but here's the best") - 0.15, s_genius),
    (ph("so mcdonald's sells") - 0.15, s_reveal)]
SHAKES = [(ph('ten billion'), 18, 0.45), (ph('rent wins'), 12, 0.4), (ph('ninety five'), 8, 0.3), (ph('eighty four'), 14, 0.4), (ph('on the building'), 10, 0.35)]
TR = 0.32
