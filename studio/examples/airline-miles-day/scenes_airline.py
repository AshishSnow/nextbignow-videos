# ------------------------------------------------------------------ airline props
def plane(c, x, y, s=1.0, rot=0, body=(255, 255, 255), tail=(40, 120, 230), t=0.0, card_wing=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-260, 70, 520, 40), P((0, 0, 0), 0.18, 12))
    inked(c, path([(-40, 10), (60, 10), (-60, 150), (-120, 150)]), P((210, 220, 235)), 6)          # far wing
    inked(c, path([(-230, -20), (-190, -20), (-130, -140), (-180, -140)]), P(tail), 6)              # tail fin
    b = skia.Path(); b.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -40, 520, 90), 45, 45))
    inked(c, b, LG((0, -40), (0, 50), [body, tuple(int(v * 0.85) for v in body)]), 7)
    c.drawPath(path([(200, -30), (262, -5), (262, 10), (200, 10)]), P((60, 80, 120)))                 # cockpit
    for i in range(8): c.drawCircle(-170 + i * 46, -8, 10, P((80, 150, 230))); c.drawCircle(-170 + i * 46, -8, 10, S(INK, 3))
    c.drawRect(skia.Rect.MakeXYWH(-250, 18, 500, 10), P(tail))
    if card_wing:
        c.save(); c.translate(-10, 60); c.rotate(14); credit_card(c, 0, 0, 300, 0, t=t); c.restore()
    else:
        inked(c, path([(-30, 20), (70, 20), (-40, 190), (-110, 190)]), P((235, 240, 250)), 6)       # near wing
        inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-40, 110, 70, 34), 16, 16), P((180, 190, 210)), 5)
    c.restore()


def credit_card(c, x, y, w, rot, col=(40, 90, 200), label='MILES CARD', t=0.0, glow_=0.0):
    h = w * 0.63
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.06, w * 0.06)
    if glow_ > 0: c.drawRRect(r, P((255, 230, 120), 0.7 * glow_, w * 0.12))
    c.drawRRect(r.makeOffset(w * 0.03, w * 0.04), P(INK, 0.3, 6))
    c.drawRRect(r, LG((-w / 2, -h / 2), (w / 2, h / 2), [tuple(min(255, v + 70) for v in col), col, tuple(int(v * 0.7) for v in col)]))
    c.save(); c.clipRRect(r, doAntiAlias=True)
    c.drawPath(path([(-w / 2, -h / 2), (-w * 0.05, -h / 2), (-w * 0.4, h / 2), (-w / 2, h / 2)]), P((255, 255, 255), 0.16))
    c.restore()
    chip = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w * 0.38, -h * 0.18, w * 0.16, w * 0.12), 6, 6)
    c.drawRRect(chip, LG((0, -h * 0.18), (0, 0), [(255, 230, 140), (220, 170, 60)])); c.drawRRect(chip, S(INK, max(2, w * 0.008)))
    for i in range(4): c.drawRoundRect(skia.Rect.MakeXYWH(-w * 0.38 + i * w * 0.15, h * 0.12, w * 0.12, w * 0.04), 4, 4, P((255, 255, 255), 0.8))
    ctext(c, label, -w * 0.38 + w * 0.0 + w * 0.22, -h * 0.3, w * 0.075, (255, 255, 255), 'Anton.ttf')
    pl = path([(w * 0.22, h * 0.32), (w * 0.42, h * 0.22), (w * 0.44, h * 0.26), (w * 0.3, h * 0.36)]); c.drawPath(pl, P((255, 255, 255), 0.9))
    c.drawRRect(r, S(INK, max(3, w * 0.016)))
    c.restore()


def mile_token(c, x, y, r, a=1.0):
    c.drawCircle(x, y, r, P((80, 170, 255), a)); c.drawCircle(x, y, r, S(INK, max(2, r * 0.12), a))
    ctext(c, 'MI', x, y + r * 0.35, r * 0.95, (255, 255, 255), 'Anton.ttf', a)


def wallet(c, x, y, s=1.0, rot=0, open_=0.0, t=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if open_ > 0: credit_card(c, 30, -120 * eo(open_), 260, -8, t=t, glow_=open_)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -80, 340, 200), 30, 30), LG((0, -80), (0, 120), [(170, 110, 70), (120, 70, 40)]), 7)
    c.drawLine(-150, -50, 150, -50, S((230, 190, 140), 4)); c.drawLine(-150, 95, 150, 95, S((230, 190, 140), 4))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(70, -10, 120, 70), 20, 20), P((140, 85, 50)), 6); c.drawCircle(160, 25, 10, P((255, 214, 40)))
    c.restore()


def bank(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x + 14, y + 14, w, h), P((0, 0, 0), 0.3, 10))
    inked(c, path([(x - 20, y + h * 0.28), (x + w / 2, y), (x + w + 20, y + h * 0.28)]), P((250, 250, 255)), 7)
    inked(c, skia.Rect.MakeXYWH(x, y + h * 0.28, w, h * 0.72), LG((0, y), (0, y + h), [(245, 248, 255), (205, 215, 235)]), 7)
    for i in range(4): inked(c, skia.Rect.MakeXYWH(x + 30 + i * (w - 60) / 4 + 10, y + h * 0.4, 24, h * 0.5), P((225, 230, 245)), 4)
    neon_text(c, 'CARD BANK', x + w / 2, y + h * 0.24, 40, (40, 90, 200))


def sky_air(c, t, ground=None):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(0, 120, 235), (90, 190, 255), (220, 245, 255)], [0, 0.55, 1]))
    c.drawCircle(880, 300, 90, P((255, 255, 230))); c.drawCircle(880, 300, 200, P((255, 255, 220), 0.5, 70))
    for i, (cx, cy, s) in enumerate(((80, 600, 0.6), (700, 760, 0.5), (300, 1050, 0.7), (850, 1250, 0.55))):
        cloud(c, (cx + t * (30 + 10 * i)) % 1300 - 150, cy, s)
    if ground: c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 420), LG((0, 1500), (0, H), [ground, tuple(int(v * 0.8) for v in ground)]))


def bill(c, x, y, k, t, rot, s):
    if k <= 0: return
    sc = min(1, k * 1.5); c.save(); c.translate(x, y); c.rotate(rot + 4 * math.sin(t * 3 + x)); c.scale(sc, sc)
    c.drawRect(skia.Rect.MakeXYWH(-90 + 8, -110 + 8, 180, 220), P(INK, 0.3)); inked(c, skia.Rect.MakeXYWH(-90, -110, 180, 220), P((255, 252, 240)), 6)
    ctext(c, s, 0, -50, 34 if len(s) > 6 else 40, (220, 40, 60), 'Anton.ttf')
    for i in range(4): c.drawLine(-70, -10 + i * 30, 60 - (i % 2) * 40, -10 + i * 30, S((170, 170, 190), 5))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tw = ph('a card in your wallet'); tp = ph('own numbers prove')
    sky_air(c, t, (150, 210, 150))
    board(c, 70, 250, 940, 200)
    neon_text(c, 'YOUR AIRLINE BARELY', 540, 340, 64, (30, 120, 230))
    neon_text(c, 'PROFITS ON FLYING YOU', 540, 425, 58, (255, 70, 90))
    kx = pr(t, 0.0, 2.8)
    plane(c, lerp(-300, 760, eo(kx)), 820 - 120 * eo(kx), 1.1, -6, t=t)
    person(c, 300, 1760, 0.62, (255, 140, 40), (36, 44, 90), mood='happy' if t < tw else 'shock', look=(0.5, -0.8), t=t, arm_r=(150, -150), arm_l=(-30, 220), blink=blinking(t))
    if t > tw - 0.4:
        pop(c, pr(t, tw - 0.4, 0.4), 760, 1300, lambda: wallet(c, 760, 1350, 1.2, 6, pr(t, tw, 0.6), t))
    if t > tp - 0.3:
        pop(c, pr(t, tp - 0.3, 0.3), 760, 1640, lambda: (board(c, 560, 1580, 400, 110, (255, 236, 90)), neon_text(c, "DELTA'S OWN DATA", 760, 1658, 44, (30, 120, 230))))


def bars(c, t, show82, show5, show9, cmp_k):
    base = 1180; sc = 75
    def col(x, val, h, rgb, lab, k, ghost=False):
        if k <= 0: return
        hh = h * eo(k)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, base - hh, 230, hh), 18, 18)
        if ghost:
            c.drawRRect(r, P(rgb, 0.35)); c.drawRRect(r, S(INK, 5))
        else:
            c.drawRRect(r.makeOffset(10, 12), P(INK, 0.25, 6)); inked(c, r, LG((x, base - hh), (x, base), [tuple(min(255, v + 60) for v in rgb), rgb]), 7)
        neon_text(c, val, x + 115, base - hh - 30, 62, rgb, cl(k * 2))
        ctext(c, lab, x + 115, base + 70, 40, (255, 255, 255), 'Anton.ttf')
    inked(c, skia.Rect.MakeXYWH(60, base, 960, 14), P((255, 255, 255)), 5)
    col(90, '$5.0B', 5.0 * sc, (255, 120, 60), 'AIRLINE PROFIT', show5)
    col(425, '$8.2B', 8.2 * sc, (40, 190, 110), 'CARD DEAL', show82)
    col(760, '~$9B', 9.0 * sc, (40, 190, 110), '2026 EXPECTED', show9, True)
    if cmp_k > 0:
        pop(c, cmp_k, 420, 1610, lambda: (board(c, 160, 1550, 520, 110, (255, 236, 90)), neon_text(c, 'CARD > PROFIT', 420, 1628, 64, (255, 70, 90))))


def s_big(c, t):
    t82 = ph('eight point two'); t5 = ph('about five billion'); tb = ph('deal beat')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    board(c, 80, 250, 920, 150); neon_text(c, 'DELTA, 2025', 540, 352, 70, (30, 120, 230))
    ctext(c, 'SOURCE: DELTA FULL-YEAR 2025 RESULTS (ADJUSTED PRE-TAX PROFIT)', 540, 445, 22, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars(c, t, pr(t, t82 - 0.3, 0.8), pr(t, t5 - 0.3, 0.8), 0, pr(t, tb - 0.2, 0.3))
    person(c, 930, 1840, 0.42, (255, 140, 40), (36, 44, 90), mood='shock' if t > t82 else 'neutral', look=(-0.6, -0.7), sweat=2 if t > tb else 0, t=t, blink=blinking(t))


def s_card(c, t):
    tm = ph('miles are money'); ta = ph('american express pays'); tsw = ph('every time you swipe'); tco = ph('coffee'); tg = ph('groceries'); tgs = ph('gas'); tn = ph('still gets paid')
    sky_air(c, t, (150, 210, 150))
    if t < ta - 0.3:
        board(c, 120, 260, 840, 150); neon_text(c, 'WHY PAY THAT MUCH?', 540, 358, 64, (30, 120, 230))
        credit_card(c, 540, 900, 700, -6 + 2 * math.sin(t * 2), t=t, glow_=0.6)
        if t > tm - 0.3: pop(c, pr(t, tm - 0.3, 0.3), 540, 1200, lambda: (board(c, 230, 1140, 620, 110, (255, 236, 90)), neon_text(c, 'MILES = MONEY', 540, 1218, 60, (40, 170, 90))))
        return
    if t < tco - 0.3:
        board(c, 120, 260, 840, 150); neon_text(c, 'HOW THE MONEY FLOWS', 540, 358, 62, (30, 120, 230))
        bank(c, 90, 700, 360, 330, t)
        plane(c, 790, 860, 0.62, -4, t=t)
        u = pr(t, ta + 0.3, 1.0)
        for i in range(3):
            v = cl(u * 1.4 - i * 0.2)
            if 0 < v < 1: moneybag(c, lerp(380, 740, eio(v)), 820 - 90 * math.sin(math.pi * v), 0.6, -10 + 20 * v)
        if u > 0.7: neon_text(c, '$$$ FOR MILES', 600, 1120, 46, (40, 170, 90))
        v2 = pr(t, tsw - 0.6, 1.0)
        for i in range(4):
            v = cl(v2 * 1.5 - i * 0.15)
            if v > 0: mile_token(c, lerp(760, 320, eio(v)) + i * 18, lerp(980, 1350, eio(v)) - 120 * math.sin(math.pi * v), 34)
        person(c, 280, 1780, 0.55, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.6, -0.6), t=t, arm_r=(120, -120), arm_l=(-30, 220), blink=blinking(t),
               prop=(1, lambda cc, ex, ey: credit_card(cc, ex + 30, ey - 30, 160, -14, t=t)))
        return
    sky_air(c, t, (150, 210, 150))
    board(c, 120, 260, 840, 150); neon_text(c, 'EVERY SWIPE PAYS DELTA', 540, 358, 56, (30, 120, 230))
    items = ((tco, lambda: cup(c, 250, 1000, 1.4, 1.0, t), 'COFFEE'), (tg, lambda: cart(c, 540, 1080, 0.75, 1.0, t), 'GROCERIES'), (tgs, lambda: (inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(760, 820, 160, 260), 20, 20), P((255, 80, 90)), 7), c.drawRect(skia.Rect.MakeXYWH(785, 850, 110, 70), P((230, 250, 255)))), 'GAS'))
    for i, (ti, fn, lab) in enumerate(items):
        k = pr(t, ti - 0.2, 0.3)
        if k > 0:
            x = (250, 540, 840)[i]
            pop(c, k, x, 1000, fn); ctext(c, lab, x, 1210, 40, (40, 60, 110), 'Anton.ttf')
            for j in range(3):
                v = pr(t, ti + 0.1 + j * 0.15, 0.9)
                if 0 < v < 1: mile_token(c, lerp(x, 540, eio(v)), lerp(920, 560, eio(v)), 26, 1 - max(0, v - 0.8) * 5)
    plane(c, 540, 600, 0.45, -4, t=t)
    person(c, 540, 1780, 0.5, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(120, -160), arm_l=(-30, 220), blink=blinking(t),
           prop=(1, lambda cc, ex, ey: credit_card(cc, ex + 30, ey - 30, 160, -14, t=t)))
    if t > tn - 0.3: pop(c, pr(t, tn - 0.3, 0.3), 540, 1340, lambda: (board(c, 250, 1280, 580, 110, (255, 236, 90)), neon_text(c, 'NO PLANE NEEDED', 540, 1358, 54, (255, 70, 90))))


def s_grow(c, t):
    t9 = ph('nine billion')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(30, 150, 240), (150, 215, 255)]))
    board(c, 80, 250, 920, 150); neon_text(c, 'AND STILL GROWING', 540, 352, 70, (40, 170, 90))
    ctext(c, "SOURCE: DELTA CEO VIA PAYMENTS DIVE, JUL 2026", 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars(c, t, 1.0, 1.0, pr(t, t9 - 0.3, 0.8), 0)
    person(c, 930, 1840, 0.42, (255, 140, 40), (36, 44, 90), mood='shock' if t > t9 else 'happy', look=(-0.6, -0.7), t=t, blink=blinking(t))


def s_reveal(c, t):
    ts = ph('sure'); tr = ph('a rewards program'); tp = ph('planes attached')
    sky_air(c, t)
    if t < tr - 0.3:
        board(c, 120, 260, 840, 150); neon_text(c, 'IS DELTA AN AIRLINE?', 540, 358, 64, (30, 120, 230))
        plane(c, 540, 1000, 1.3, -4 + 2 * math.sin(t * 2), t=t)
        if t > ts - 0.2: pop(c, pr(t, ts - 0.2, 0.3), 540, 1340, lambda: (board(c, 380, 1280, 320, 110, (255, 255, 255)), neon_text(c, 'SURE...', 540, 1358, 60, (40, 170, 90))))
    else:
        pop(c, pr(t, tr - 0.3, 0.35), 540, 330, lambda: (board(c, 100, 260, 880, 150, (255, 236, 90)), neon_text(c, 'A REWARDS PROGRAM...', 540, 358, 64, (255, 70, 90))))
        credit_card(c, 540, 900, 760, -5 + 2 * math.sin(t * 2), t=t, glow_=0.5)
        if t > tp - 0.4:
            pop(c, pr(t, tp - 0.4, 0.5), 540, 1220, lambda: (plane(c, 300, 1230, 0.5, -10, t=t), plane(c, 780, 1210, 0.5, 8, t=t)))
            pop(c, pr(t, tp, 0.3), 540, 1580, lambda: (board(c, 160, 1520, 760, 110, (255, 255, 255)), neon_text(c, 'WITH PLANES ATTACHED', 540, 1598, 56, (30, 120, 230))))


def s_end(c, t):
    tc = ph('cashing in'); tq = ph('do you have')
    sky_air(c, t, (150, 210, 150))
    if t < tq - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'PICKING A CARD FOR POINTS?', 540, 355, 54, (30, 160, 255)); neon_text(c, "WHO'S REALLY CASHING IN?", 540, 440, 56, (255, 70, 90), pr(t, tc - 0.6, 0.3))
        credit_card(c, 330, 950, 360, -10, t=t)
        if t > tc - 0.5:
            for i in range(5):
                v = pr(t, tc - 0.5 + i * 0.12, 0.4)
                pop(c, v, 700 + (i % 3) * 110, 900 + (i // 3) * 120, lambda: mile_token(c, 700 + (i % 3) * 110, 900 + (i // 3) * 120, 52))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'GOT AN AIRLINE', 540, 355, 70, (30, 160, 255)); neon_text(c, 'CREDIT CARD?', 540, 440, 70, (255, 190, 30))
        for x, lab, col_ in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tq + 0.3, 0.3), x, 650, lambda: (board(c, x - 130, 590, 260, 120, col_), neon_text(c, lab, x, 680, 80, (255, 255, 255))))
    person(c, 540, 1680, 0.66, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(80, -220), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_hook), (ph("here's the wild") - 0.15, s_big), (ph('but why would') - 0.15, s_card), (ph("and it's still growing") - 0.15, s_grow),
    (ph('so is delta') - 0.15, s_reveal), (ph('next time you pick') - 0.15, s_end)]
SHAKES = [(ph('eight point two'), 18, 0.45), (ph('deal beat'), 10, 0.35), (ph('miles are money'), 8, 0.3), (ph('nine billion'), 12, 0.4), (ph('a rewards program'), 10, 0.35)]
TR = 0.32
