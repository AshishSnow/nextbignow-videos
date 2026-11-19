# ------------------------------------------------------------------ gift card props
CARDCOLS = [(255, 80, 110), (40, 170, 255), (255, 190, 30), (60, 200, 120), (170, 100, 255), (255, 130, 40)]


def giftcard(c, x, y, w, rot, col, label='', a=1.0, dust=0.0, sparkle_=True, t=0.0):
    h = w * 0.63
    c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.07, w * 0.07)
    c.drawRRect(r.makeOffset(w * 0.03, w * 0.04) if hasattr(r, 'makeOffset') else r, P(INK, 0.3 * a, 6))
    c.drawRRect(r, LG((-w / 2, -h / 2), (w / 2, h / 2), [tuple(min(255, v + 60) for v in col) + (a,), col + (a,), tuple(int(v * 0.75) for v in col) + (a,)]))
    c.save(); c.clipRRect(r, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h * 0.18, w, h * 0.16), P((255, 255, 255), 0.85 * a))
    c.drawRect(skia.Rect.MakeXYWH(w * 0.05, -h / 2, w * 0.1, h), P((255, 255, 255), 0.85 * a))
    c.drawPath(path([(-w / 2, -h / 2), (-w * 0.1, -h / 2), (-w * 0.45, h / 2), (-w / 2, h / 2)]), P((255, 255, 255), 0.18 * a))
    c.restore()
    bw = skia.Path(); bw.addCircle(w * 0.1 - w * 0.07, -h * 0.1, w * 0.07); bw.addCircle(w * 0.1 + w * 0.07, -h * 0.1, w * 0.07)
    c.drawPath(bw, P((255, 255, 255), a)); c.drawPath(bw, S(INK, max(2, w * 0.012), a))
    if label: ctext(c, label, -w * 0.2, h * 0.36, w * 0.17, (255, 255, 255), 'Anton.ttf', a=a)
    c.drawRRect(r, S(INK, max(3, w * 0.018), a))
    if dust > 0:
        c.save(); c.clipRRect(r, doAntiAlias=True); c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), P((150, 140, 120), 0.45 * dust))
        rnd = random.Random(int(w)); [c.drawCircle(rnd.uniform(-w / 2, w / 2), rnd.uniform(-h / 2, h / 2), rnd.uniform(1, 4), P((90, 80, 70), 0.6 * dust)) for _ in range(60)]
        c.restore()
        web = skia.Path(); cx, cy = w / 2, -h / 2
        for k in range(5): a_ = math.radians(90 + k * 22); web.moveTo(cx, cy); web.lineTo(cx + math.cos(a_) * w * 0.35, cy + math.sin(a_) * w * 0.35)
        for rr in (0.12, 0.22, 0.32):
            for k in range(4):
                a1, a2 = math.radians(90 + k * 22), math.radians(90 + (k + 1) * 22)
                web.moveTo(cx + math.cos(a1) * w * rr, cy + math.sin(a1) * w * rr); web.quadTo(cx + math.cos((a1 + a2) / 2) * w * rr * 0.85, cy + math.sin((a1 + a2) / 2) * w * rr * 0.85, cx + math.cos(a2) * w * rr, cy + math.sin(a2) * w * rr)
        c.drawPath(web, S((255, 255, 255), 2.5, 0.9 * dust))
    c.restore()
    if sparkle_ and dust <= 0: sparkle(c, x + w * 0.38, y - h * 0.4, w * 0.08, max(0.0, math.sin(t * 3 + x)) * a)


def cup(c, x, y, s=1.0, steam=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    body = path([(-55, -120), (55, -120), (42, 40), (-42, 40)]); inked(c, body, LG((-55, 0), (55, 0), [(255, 255, 255), (230, 235, 240)]), 6)
    sl = path([(-50, -70), (50, -70), (46, -20), (-46, -20)]); inked(c, sl, P((190, 130, 80)), 5)
    lid = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-64, -146, 128, 30), 10, 10); inked(c, lid, P((250, 250, 252)), 6)
    if steam > 0:
        for k in range(3):
            p = skia.Path(); x0 = -20 + k * 20; p.moveTo(x0, -160)
            for j in range(1, 6): p.lineTo(x0 + 10 * math.sin(t * 4 + j + k), -160 - j * 18)
            c.drawPath(p, S((255, 255, 255), 6, 0.7 * steam))
    c.restore()


def cash(c, x, y, rot, s=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    r = skia.Rect.MakeXYWH(-90, -45, 180, 90); inked(c, r, LG((0, -45), (0, 45), [(170, 230, 160), (110, 190, 110)]), 5)
    c.drawOval(skia.Rect.MakeXYWH(-30, -30, 60, 60), S((60, 130, 60), 4)); ctext(c, '$', 0, 16, 44, (40, 110, 40), 'Anton.ttf')
    c.restore()


def register(c, rx, ry, k_open=0.0, sticky_txt=None, t=0.0):
    reg = path([(rx - 170, ry), (rx + 170, ry), (rx + 140, ry - 170), (rx - 140, ry - 170)]); inked(c, reg, LG((0, ry - 170), (0, ry), [(120, 210, 255), (40, 140, 220)]), 7)
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(rx - 80, ry - 260, 160, 80), 10, 10); inked(c, scr, P((20, 40, 50)), 6)
    ctext(c, 'PAID', rx, ry - 205, 44, (80, 255, 140), 'Anton.ttf')
    for i in range(3):
        for j in range(4): c.drawRoundRect(skia.Rect.MakeXYWH(rx - 110 + j * 58, ry - 150 + i * 44, 44, 32), 6, 6, P((255, 255, 255), 0.85))
    inked(c, skia.Rect.MakeXYWH(rx - 190, ry + 50 * k_open - 10, 380, 60), P((30, 110, 190)), 7)
    if sticky_txt: sticky(c, rx + 10, ry - 420, 1.15, -6, sticky_txt, size=40)


def kitchen_bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 250, 240), (240, 232, 215)]))
    wr = skia.Rect.MakeXYWH(560, 470, 440, 400); skyline(c, 560, 470, 440, 400, t, 3); c.drawRect(wr, S((255, 255, 255), 18)); c.drawRect(wr.makeOutset(9, 9), S(INK, 6))
    c.drawLine(780, 470, 780, 870, S((255, 255, 255), 12))
    for i in range(3):
        r = skia.Rect.MakeXYWH(60 + i * 160, 470, 150, 300); inked(c, r, LG((0, 470), (0, 770), [(120, 220, 210), (70, 190, 180)]), 6)
        c.drawRoundRect(skia.Rect.MakeXYWH(60 + i * 160 + 110, 600, 14, 50), 7, 7, P(INK))
    inked(c, skia.Rect.MakeXYWH(20, 1040, 1040, 40), LG((0, 1040), (0, 1080), [(255, 255, 255), (220, 225, 235)]), 6)
    c.drawRect(skia.Rect.MakeXYWH(40, 1080, 1000, 840), LG((0, 1080), (0, H), [(120, 220, 210), (60, 170, 165)])); c.drawRect(skia.Rect.MakeXYWH(40, 1080, 1000, 840), S(INK, 6))
    for i in range(1, 3): c.drawLine(40 + i * 333, 1080, 40 + i * 333, 1920, S(INK, 5))
    c.drawRoundRect(skia.Rect.MakeXYWH(140, 1160, 140, 18), 9, 9, P(INK)); c.drawRoundRect(skia.Rect.MakeXYWH(800, 1160, 140, 18), 9, 9, P(INK))


def drawer(c, x, y, w, k_open, cards_k, t, dust=0.0):
    d = 140 * eo(k_open)
    inner = path([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 30, y - d), (x - w / 2 + 30, y - d)]); inked(c, inner, P((150, 90, 50)), 6)
    rnd = random.Random(5)
    for i in range(9):
        kk = pr(cards_k, i * 0.07, 0.5)
        if kk <= 0: continue
        cx = x - w * 0.36 + i * w * 0.09 + rnd.uniform(-10, 10); cy = y - d * 0.5 - 140 * eo(kk) + rnd.uniform(-20, 20)
        giftcard(c, cx, cy, 170, rnd.uniform(-35, 35), CARDCOLS[i % 6], '', 1.0, dust * (1 if i == 4 else 0.6), t=t)
    front = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2 - 10, y, w + 20, 170), 16, 16); inked(c, front, LG((0, y), (0, y + 170), [(130, 230, 220), (70, 190, 180)]), 7)
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 90, y + 70, 180, 24), 12, 12, P(INK))


def people(c, x0, y, n, s, hl, k, t, grey=None, hold=True):
    for i in range(n):
        kk = pr(k, i * 0.05, 0.3)
        if kk <= 0: continue
        x = x0 + i * 170 * s
        g = (grey is not None and i == grey)
        hc = (170, 170, 180) if g else [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][i % 5]
        jc = (150, 150, 160) if g else [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][i % 5]
        pop(c, kk, x, y, lambda: person(c, x, y, 0.28 * s, hc, jc, mood='neutral' if g else 'happy', t=t, blink=blinking(t, i)))
        if hold and i < hl:
            giftcard(c, x + 50 * s, y - 120 * s, 70 * s, -15, CARDCOLS[i % 6], '', kk, (0.8 if g else 0), sparkle_=False)


# ------------------------------------------------------------------ scenes
def s_kitchen(c, t):
    tz = ph('and the one')
    kitchen_bg(c, t)
    board(c, 70, 250, 940, 200)
    neon_text(c, 'STORES MAKE MILLIONS', 540, 335, 60, (255, 70, 90))
    neon_text(c, 'FROM UNUSED GIFT CARDS', 540, 420, 60, (30, 160, 255))
    person(c, 230, 1520, 0.7, (255, 140, 40), (36, 44, 90), mood='shock', look=(0.6, 0.6), t=t, arm_r=(120, 120), arm_l=(-60, 220), blink=blinking(t))
    drawer(c, 700, 1240, 540, pr(t, 0.2, 0.5), pr(t, 0.4, 1.4), t, dust=pr(t, tz - 0.2, 0.8))
    if t > tz - 0.2: sparkle(c, 700, 1060, 40, pr(t, tz, 0.4))


def s_survey(c, t):
    t43 = ph('forty three percent'); t244 = ph('two hundred forty four')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(230, 245, 255), (200, 228, 252)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        ctext(cc, 'BANKRATE SURVEY', 410, 70, 44, (255, 255, 255)); ctext(cc, 'US ADULTS, SEP 2024', 410, 112, 26, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
        k = pr(t, t43 - 0.3, 0.4)
        if k > 0: neon_text(cc, '43%', 410, 300, 170, (255, 200, 40), cl(k * 2))
        ctext(cc, "HAVE AN UNUSED GIFT CARD", 410, 370, 34, (255, 255, 255), a=k)
    screen(c, 130, 300, 820, 420, d, (40, 170, 255))
    c.drawLine(400, 720, 360, 800, S(INK, 12)); c.drawLine(680, 720, 720, 800, S(INK, 12))
    for row in range(2):
        for i in range(5):
            idx = row * 5 + i; x = 160 + i * 190; y = 1150 + row * 330
            kk = pr(t, t43 - 0.2 + idx * 0.05, 0.3)
            if kk <= 0: continue
            pop(c, kk, x, y, lambda: person(c, x, y, 0.32, [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][idx % 5], [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][idx % 5], mood='happy', t=t, blink=blinking(t, idx)))
            if idx in (0, 3, 6, 8): giftcard(c, x + 60, y - 150, 80, -15, CARDCOLS[idx % 6], '', kk, sparkle_=False)
    if t > t244 - 0.3:
        k = pr(t, t244 - 0.3, 0.4)
        c.drawRect(skia.Rect.MakeWH(W, H), P((255, 255, 255), 0.45 * k))
        pop(c, k, 540, 1150, lambda: giftcard(c, 540, 1150, 720, -6, (255, 80, 110), '$244', 1.0, t=t))
        if k > 0.5: neon_text(c, 'AVERAGE UNUSED', 540, 870, 60, (30, 160, 255), cl(k * 2 - 1))


def s_store(c, t):
    tb = ph('the store already'); tn = ph("can't count it")
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 245, 230), (255, 225, 200)]))
    board(c, 140, 260, 800, 140); neon_text(c, 'GIFT CARDS', 540, 360, 84, (255, 70, 90))
    for row in range(3):
        for i in range(6):
            giftcard(c, 150 + i * 156, 500 + row * 120, 120, (i * 7 + row * 11) % 14 - 7, CARDCOLS[(i + row) % 6], '', 1.0, t=t, sparkle_=(i + row) % 3 == 0)
    person(c, 900, 1480, 0.62, (70, 140, 255), (255, 255, 255), mood='happy', look=(-0.6, 0.1), t=t, arm_r=(-100, 160), arm_l=(-60, 220), tie=(255, 80, 110), shirt=(250, 250, 255), blink=blinking(t, 2))
    inked(c, skia.Rect.MakeXYWH(20, 1300, 1040, 50), LG((0, 1300), (0, 1350), [(255, 255, 255), (220, 225, 235)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1350, 1000, 600), LG((0, 1350), (0, H), [(255, 120, 140), (220, 70, 100)])); c.drawRect(skia.Rect.MakeXYWH(40, 1350, 1000, 600), S(INK, 7))
    k = pr(t, tb - 0.4, 0.6)
    register(c, 600, 1290, eo(pr(t, tb, 0.3)) * (1 - pr(t, tb + 1.0, 0.4)), "NOT A\nSALE YET" if t > tn - 0.2 else None, t)
    cash(c, lerp(260, 560, eio(k)), lerp(1180, 1240, eio(k)) - 60 * math.sin(math.pi * k), -10 + 20 * k, 1.0) if k < 1 else None
    person(c, 220, 1800, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.7, -0.2), t=t, arm_r=(140, -40) if k < 1 else (60, 200), arm_l=(-30, 230), blink=blinking(t))
    if k >= 1: giftcard(c, 330, 1420, 160, -12, (40, 170, 255), '', 1.0, t=t)


def lerp(a, b, u): return a + (b - a) * u


def s_drawer(c, t):
    t0 = ph('some cards never'); tf = ph('forgotten')
    kitchen_bg(c, t)
    months = ['JAN', 'MAR', 'JUN', 'SEP', 'DEC', 'JAN']
    m = months[min(len(months) - 1, int(max(0, t - t0) * 2.2))]
    cal = skia.Rect.MakeXYWH(120, 300, 300, 330); inked(c, cal, P((255, 255, 255)), 6); c.drawRect(skia.Rect.MakeXYWH(120, 300, 300, 80), P((255, 80, 110))); c.drawRect(skia.Rect.MakeXYWH(120, 300, 300, 80), S(INK, 6))
    ctext(c, m, 270, 540, 120, (30, 30, 50), 'Anton.ttf')
    flip = ((t - t0) * 2.2) % 1.0
    if t > t0 and flip < 0.4:
        c.save(); c.translate(270, 380); c.rotate(-40 * flip / 0.4); c.drawRect(skia.Rect.MakeXYWH(-150, 0, 300, 250 * (1 - flip / 0.4)), P((245, 245, 250))); c.restore()
    drawer(c, 540, 1240, 700, 1.0, 9.0, t, dust=pr(t, tf - 0.3, 1.0))
    person(c, 860, 1640, 0.62, (255, 140, 40), (36, 44, 90), mood='neutral', look=(-0.8, 0.5), t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))


def s_acct(c, t):
    tc = ph('once a company'); tr = ph('as revenue'); tbk = ph('breakage', after=ph("there's even"))
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(235, 255, 240), (200, 240, 215)]))
    wr = skia.Rect.MakeXYWH(620, 300, 380, 360); skyline(c, 620, 300, 380, 360, t, 7); c.drawRect(wr, S((255, 255, 255), 18)); c.drawRect(wr.makeOutset(9, 9), S(INK, 6))
    person(c, 500, 1520, 0.66, (60, 200, 120), (40, 40, 60), pants=(30, 30, 46), mood='happy', look=(-0.6, 0.6), t=t,
           arm_r=(-120, 120 - 60 * abs(math.sin(t * 5))), arm_l=(-60, 230), tie=(255, 200, 40), shirt=(250, 250, 255), blink=blinking(t, 3))
    inked(c, skia.Rect.MakeXYWH(30, 1400, 1020, 50), LG((0, 1400), (0, 1450), [(240, 180, 110), (205, 140, 80)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(60, 1450, 960, 500), P((210, 140, 80))); c.drawRect(skia.Rect.MakeXYWH(60, 1450, 960, 500), S(INK, 7))
    jar = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(800, 1150, 200, 250), 30, 30); c.drawRRect(jar, P((220, 245, 255), 0.6)); c.drawRRect(jar, S(INK, 6)); inked(c, skia.Rect.MakeXYWH(790, 1130, 220, 34), P((255, 200, 40)), 5)
    sticky(c, 900, 1330, 0.8, 4, 'REVENUE', size=34, col=(255, 255, 255), tc=(40, 160, 90))
    for i in range(5):
        u = ((t - tc) * 0.3 - i * 0.16)
        if u < 0 or u > 1: continue
        x = lerp(120, 760, u); y = 1360
        if u < 0.55: giftcard(c, x, y, 150, -8, CARDCOLS[i % 6], '', 1.0, dust=0.6, sparkle_=False)
        else:
            for j in range(4): coin(c, x - 30 + j * 20, y + 30 - j * 14, 26)
    if t > tr - 0.3:
        for j in range(int(10 * pr(t, tr - 0.3, 0.8))): coin(c, 870 + (j % 3) * 30, 1380 - j * 14, 30)
    if t > tbk - 0.4:
        k = pr(t, tbk - 0.4, 0.35)
        def sign():
            board(c, 120, 330, 840, 230, (255, 240, 120))
            neon_text(c, 'BREAKAGE', 540, 495, 128, (255, 70, 90))
            cr = skia.Path(); cr.moveTo(560, 330); cr.lineTo(530, 400); cr.lineTo(575, 440); cr.lineTo(540, 520); cr.lineTo(560, 560)
            c.drawPath(cr, S(INK, 6, cl(k * 2 - 0.6)))
        pop(c, k, 540, 445, sign)


def s_cafe(c, t):
    td = ph('how big'); t222 = ph('two hundred twenty two'); tn = ph('for coffee nobody')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 240, 220), (245, 215, 180)]))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(i * 190, 0, 90, 1300), P((255, 255, 255), 0.25))
    def d(cc):
        k = pr(t, t222 - 0.4, 0.4)
        ctext(cc, 'STARBUCKS GIFT CARD BREAKAGE', 410, 70, 34, (255, 255, 255))
        if k > 0: neon_text(cc, '$222 MILLION', 410, 250, 112, (80, 230, 140), cl(k * 2))
        ctext(cc, 'FISCAL 2025, PER ITS 10-K', 410, 330, 26, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
    screen(c, 130, 300, 820, 380, d, (80, 230, 140))
    inked(c, skia.Rect.MakeXYWH(20, 1200, 1040, 50), LG((0, 1200), (0, 1250), [(240, 180, 110), (205, 140, 80)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1250, 1000, 700), P((200, 125, 70))); c.drawRect(skia.Rect.MakeXYWH(40, 1250, 1000, 700), S(INK, 7))
    nk = pr(t, ph('how big') - 0.1, 0.9)
    for i in range(9):
        kk = pr(nk, i * 0.06, 0.4)
        if kk <= 0: continue
        cup(c, 120 + i * 105 + 300 * (1 - eo(kk)), 1190, 0.75, steam=1.0, t=t + i)
    dim = pr(t, td - 0.1, 0.4) * (1 - pr(t, t222 - 0.1, 0.25))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.35 * dim))
    if t > t222:
        rnd = random.Random(4); tt = t - t222
        for k in range(30):
            d0 = rnd.random() * 0.6; ang = rnd.uniform(-1.2, 1.2); v = rnd.uniform(500, 900); u = tt - d0
            if 0 < u < 1.6: coin(c, 540 + math.sin(ang) * v * u, 760 - math.cos(ang) * v * u * 1.2 + 900 * u * u, rnd.uniform(16, 26))


def s_expire(c, t):
    t5 = ph('one in five')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(225, 240, 255), (255, 235, 220)]))
    board(c, 120, 300, 840, 200); neon_text(c, '1 IN 5', 540, 390, 90, (255, 70, 90)); neon_text(c, 'LET A CARD EXPIRE', 540, 470, 56, (30, 160, 255))
    c.drawRect(skia.Rect.MakeXYWH(0, 1500, W, 420), LG((0, 1500), (0, H), [(150, 220, 160), (100, 190, 120)]))
    k = pr(t, t5 - 0.6, 1.0)
    for i in range(5):
        x = 150 + i * 195; kk = pr(k, i * 0.1, 0.4)
        if kk <= 0: continue
        g = i == 2
        hc = (175, 175, 185) if g else [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][i]
        jc = (150, 150, 160) if g else [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][i]
        pop(c, kk, x, 1560, lambda: person(c, x, 1560, 0.42, hc, jc, mood='worried' if g else 'happy', sweat=2 if g else 0, t=t, blink=blinking(t, i)))
    if t > t5 + 0.3:
        ke = pr(t, t5 + 0.3, 0.35)
        giftcard(c, 540, 860, 360, -8, (175, 175, 185), '', 1.0, dust=0.8)
        pop(c, ke, 540, 860, lambda: (c.save(), c.translate(540, 860), c.rotate(-14), board(c, -210, -60, 420, 110, (255, 255, 255)), c.restore(), neon_text(c, 'EXPIRED', 540, 900, 84, (255, 60, 70), 1.0, rot=-14)))


def s_end(c, t):
    tc = ph('your coffee'); tp = ph('their profit'); th = ph('how much is')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (230, 245, 255)], [0, 0.5, 1]))
    for i in range(16):
        a = math.radians(i * 22.5); p = path([(540, 1100), (540 + 1800 * math.cos(a - 0.07), 1100 + 1800 * math.sin(a - 0.07)), (540 + 1800 * math.cos(a + 0.07), 1100 + 1800 * math.sin(a + 0.07))])
        c.drawPath(p, P((255, 255, 255), 0.12))
    cloud(c, 80, 760, 0.6); cloud(c, 740, 820, 0.5)
    c.drawOval(skia.Rect.MakeXYWH(-100, 1500, 1280, 700), P((120, 210, 240)))
    if t < th - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOUR COFFEE...', 540, 355, 70, (190, 120, 60), pr(t, tc - 0.3, 0.3))
        neon_text(c, '...OR THEIR PROFIT?', 540, 440, 70, (40, 190, 110), pr(t, tp - 0.3, 0.3))
        pop(c, pr(t, tc - 0.3, 0.4), 220, 1150, lambda: cup(c, 220, 1150, 1.3, 1.0, t))
        if t > tp - 0.3:
            for j in range(int(12 * pr(t, tp - 0.3, 0.6))): coin(c, 860 + (j % 3) * 34 - 34, 1180 - (j // 3) * 22, 34)
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, "HOW MUCH IS IN", 540, 355, 70, (30, 160, 255)); neon_text(c, 'YOUR DRAWER?', 540, 440, 70, (255, 190, 30))
        def bub():
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(640, 620, 340, 200), 50, 50); inked(c, r, P((255, 255, 255)), 7)
            c.drawPath(path([(700, 815), (680, 900), (760, 815)]), P((255, 255, 255))); ctext(c, '$___?', 810, 750, 80, (255, 70, 90), 'Anton.ttf')
        pop(c, pr(t, th, 0.4), 810, 720, bub)
    person(c, 540, 1780, 0.82, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.0, -0.6), t=t, arm_r=(40, -260), arm_l=(-30, 230), blink=blinking(t),
           prop=(1, lambda cc, x, y: giftcard(cc, x, y - 80, 240, 8, (255, 80, 110), '', 1.0, t=t)))


SCENES = [
    (0.0, s_kitchen), (ph('bankrate asked') - 0.15, s_survey), (ph("so where's that") - 0.15, s_store), (ph('some cards never') - 0.15, s_drawer),
    (ph('once a company') - 0.15, s_acct), (ph('how big') - 0.15, s_cafe), (ph('and one in five') - 0.15, s_expire), (ph('so that card') - 0.15, s_end)]
SHAKES = [(ph('forty three percent'), 8, 0.3), (ph('two hundred forty four'), 10, 0.35), (ph('breakage', after=ph("there's even")), 12, 0.35),
          (ph('two hundred twenty two'), 18, 0.45), (ph('one in five'), 8, 0.3)]
TR = 0.32
