def lerp(a, b, u): return a + (b - a) * u


BOXC = [(214, 160, 100), (200, 145, 85), (226, 175, 115)]


def box(c, x, y, w, h=None, rot=0.0, col=None, tape=True, label=None, open_=0.0):
    h = h or w * 0.75; col = col or BOXC[int(abs(x * 7 + y)) % 3]
    c.save(); c.translate(x, y); c.rotate(rot)
    top = h * 0.22
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 10, w, h), P(INK, 0.25, 5))
    inked(c, skia.Rect.MakeXYWH(-w / 2, -h / 2 + top, w, h - top), LG((0, -h / 2), (0, h / 2), [col, tuple(int(v * 0.85) for v in col)]), max(3, w * 0.025))
    lid = path([(-w / 2, -h / 2 + top), (w / 2, -h / 2 + top), (w / 2 - w * 0.08, -h / 2), (-w / 2 + w * 0.08, -h / 2)])
    if open_ > 0:
        for sx in (-1, 1):
            fl = path([(0, -h / 2 + top), (sx * w / 2, -h / 2 + top), (sx * (w / 2 + w * 0.25 * open_), -h / 2 + top - h * 0.5 * open_), (sx * w * 0.1, -h / 2 + top - h * 0.45 * open_)])
            inked(c, fl, P(tuple(min(255, v + 20) for v in col)), max(3, w * 0.02))
        c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 6, -h / 2 + top, w - 12, h * 0.12), P(INK, 0.5))
    else:
        inked(c, lid, P(tuple(min(255, v + 25) for v in col)), max(3, w * 0.022))
        if tape: c.drawRect(skia.Rect.MakeXYWH(-w * 0.08, -h / 2, w * 0.16, h * 0.55), P((240, 225, 170), 0.9))
    if label: ctext(c, label, 0, h * 0.28, w * 0.2, (60, 40, 20), 'Anton.ttf')
    c.restore()


def pallet(c, x, y, w):
    for i in range(3): inked(c, skia.Rect.MakeXYWH(x - w / 2 + i * (w - 40) / 2, y + 22, 40, 30), P((170, 120, 70)), 4)
    inked(c, skia.Rect.MakeXYWH(x - w / 2, y, w, 24), P((200, 150, 90)), 5)
    inked(c, skia.Rect.MakeXYWH(x - w / 2, y + 50, w, 18), P((190, 140, 80)), 4)


def tv(c, x, y, w, t=0.0, a=1.0):
    h = w * 0.6
    c.save(); c.translate(x, y)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18); inked(c, r, P((30, 30, 40)), 7)
    sc = skia.Rect.MakeXYWH(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32)
    c.drawRect(sc, LG((0, -h / 2), (0, h / 2), [(60, 200, 255), (120, 90, 255), (255, 120, 200)]))
    c.drawPath(path([(-w / 2 + 16, -h / 2 + 16), (-w * 0.05, -h / 2 + 16), (-w * 0.3, h / 2 - 16), (-w / 2 + 16, h / 2 - 16)]), P((255, 255, 255), 0.25))
    c.drawLine(-w * 0.15, h / 2, -w * 0.25, h / 2 + 60, S(INK, 12)); c.drawLine(w * 0.15, h / 2, w * 0.25, h / 2 + 60, S(INK, 12))
    c.restore()


def sky_bg(c, t, ground=(150, 220, 160)):
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(20, 130, 235), (110, 200, 255), (230, 245, 255)], [0, 0.5, 1]))
    c.drawCircle(880, 300, 90, P((255, 255, 230))); c.drawCircle(880, 300, 200, P((255, 255, 220), 0.5, 70))
    cloud(c, 80 + 20 * math.sin(t * 0.3), 560, 0.6); cloud(c, 700 - 15 * math.sin(t * 0.25), 680, 0.5)
    c.drawRect(skia.Rect.MakeXYWH(0, 1350, W, 570), LG((0, 1350), (0, H), [ground, tuple(int(v * 0.8) for v in ground)]))


# ------------------------------------------------------------------ scenes
def s_mountain(c, t):
    th = ph('and a lot')
    sky_bg(c, t)
    board(c, 70, 250, 940, 200)
    neon_text(c, '$850 BILLION', 540, 340, 72, (255, 70, 90))
    neon_text(c, 'OF RETURNS THIS YEAR', 540, 425, 62, (30, 160, 255))
    rows = [(9, 1340), (8, 1250), (7, 1160), (6, 1070), (5, 980), (4, 890), (3, 800)]
    k = pr(t, 0.1, 2.2)
    n = 0
    for ri, (cnt, y) in enumerate(rows):
        for j in range(cnt):
            n += 1; kk = pr(k, n * 0.02, 0.15)
            if kk <= 0: continue
            x = 540 + (j - (cnt - 1) / 2) * 110
            box(c, x, y - 300 * (1 - eo(kk)), 104, 86, rot=((n * 37) % 10 - 5))
    kh = pr(t, 0.6, 1.8)
    person(c, lerp(160, 470, eio(kh)), lerp(1700, 1460, eio(kh)), 0.5, (255, 140, 40), (36, 44, 90), mood='shock', look=(0.6, -0.6), sweat=2, t=t,
           arm_r=(40, -200), arm_l=(-40, -200), blink=blinking(t))
    box(c, lerp(160, 470, eio(kh)), lerp(1700, 1460, eio(kh)) - 500, 120, 96)
    if t > th - 0.3:
        kk = pr(t, th - 0.3, 0.4)
        def shelf():
            board(c, 640, 1430, 380, 260, (255, 255, 255))
            for i in range(3): c.drawRect(skia.Rect.MakeXYWH(660, 1500 + i * 70, 340, 12), P((150, 150, 170)))
            neon_text(c, '?', 830, 1640, 130, (255, 70, 90))
        pop(c, kk, 830, 1560, shelf)


def s_stats(c, t):
    t16 = ph('sixteen percent'); t19 = ph('nineteen percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(230, 245, 255), (200, 228, 252)]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1300, W, 620), LG((0, 1300), (0, H), [(255, 220, 170), (230, 180, 120)]))
    def d(cc):
        ctext(cc, 'NATIONAL RETAIL FEDERATION', 410, 70, 38, (255, 255, 255)); ctext(cc, '2025 RETURNS REPORT', 410, 112, 26, (200, 200, 230), 'Montserrat-ExtraBold.ttf')
        k = pr(t, t16 - 0.3, 0.4)
        if k > 0: neon_text(cc, '16%', 410, 300, 170, (255, 200, 40), cl(k * 2))
        ctext(cc, 'OF EVERYTHING BOUGHT COMES BACK', 410, 370, 30, (255, 255, 255), a=k)
    screen(c, 130, 300, 820, 420, d, (40, 170, 255))
    for i in range(6):
        kk = pr(t, t16 - 0.2 + i * 0.08, 0.3)
        if kk <= 0: continue
        x = 170 + i * 150; y = 1100
        back = (i == 4)
        u = pr(t, t16 + 0.7, 0.9) if back else 0
        bx, by = x + 200 * eio(u) * -1, y - 260 * math.sin(math.pi * min(1, u)) + 0
        pop(c, kk, bx, by, lambda: box(c, bx, by, 120, 100, rot=-30 * u, label='BACK' if back and u > 0.3 else None))
    person(c, 540, 1800, 0.62, (255, 140, 40), (36, 44, 90), mood='shock' if t > t16 + 0.8 else 'happy', look=(-0.4, -0.7), t=t, arm_r=(40, 220), arm_l=(-40, 220), blink=blinking(t))
    if t > t19 - 0.4:
        k = pr(t, t19 - 0.4, 0.4)
        def ph_():
            r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -300, 340, 600), 40, 40)
            c.save(); c.translate(820, 1150); c.rotate(8); inked(c, r, P((30, 30, 40)), 8)
            c.drawRoundRect(skia.Rect.MakeXYWH(-150, -270, 300, 540), 26, 26, LG((0, -270), (0, 270), [(255, 255, 255), (220, 235, 255)]))
            ctext(c, 'ONLINE', 0, -150, 50, (30, 160, 255)); neon_text(c, '19%', 0, 40, 130, (255, 70, 90)); ctext(c, 'RETURNED', 0, 140, 40, (60, 60, 80))
            c.restore()
        pop(c, k, 820, 1150, ph_)


def s_drop(c, t):
    t0 = ph('you print'); te = ph("that's where")
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 245, 230), (255, 225, 200)]))
    board(c, 220, 260, 640, 150); neon_text(c, 'RETURNS', 540, 365, 96, (255, 70, 90))
    person(c, 560, 1330, 0.6, (70, 140, 255), (255, 255, 255), mood='happy', look=(-0.6, 0.2), t=t, arm_r=(-60, 200), arm_l=(-60, 220), tie=(40, 170, 255), shirt=(250, 250, 255), blink=blinking(t, 2))
    door = skia.Rect.MakeXYWH(700, 560, 300, 620); inked(c, door, LG((0, 560), (0, 1180), [(120, 130, 150), (80, 90, 110)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(720, 580, 260, 160), P((180, 220, 255))); c.drawRect(skia.Rect.MakeXYWH(720, 580, 260, 160), S(INK, 5))
    inked(c, skia.Rect.MakeXYWH(20, 1180, 1040, 50), LG((0, 1180), (0, 1230), [(255, 255, 255), (220, 225, 235)]), 7)
    c.drawRect(skia.Rect.MakeXYWH(40, 1230, 1000, 700), LG((0, 1230), (0, H), [(40, 170, 255), (30, 120, 210)])); c.drawRect(skia.Rect.MakeXYWH(40, 1230, 1000, 700), S(INK, 7))
    kd = pr(t, t0 + 0.3, 0.6); ks = pr(t, te - 0.3, 1.4)
    bx = lerp(300, 460, eio(kd)) + 400 * eio(ks); by = 1110 - 30 * math.sin(math.pi * kd)
    box(c, bx, by, 170, 140, rot=-8 + 16 * kd, label='RETURN')
    if t > te: sticky(c, 520, 900, 0.9, -6, '$$$', size=70, col=(255, 236, 90), tc=(220, 30, 40))
    kw = pr(t, te + 1.0, 1.4)
    person(c, lerp(260, -200, eio(kw)), 1800, 0.74, (255, 140, 40), (36, 44, 90), mood='happy', look=(-0.6, -0.2), t=t, arm_r=(80, 150) if kd < 1 else (40, 220), arm_l=(-30, 230), blink=blinking(t))


def s_warehouse(c, t):
    ts = ph('ship it back'); to = ph('open it'); tc = ph('check it'); tr = ph('repack it'); t66 = ph('sixty six percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(225, 240, 255), (190, 220, 245)]))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(i * 190, 260, 100, 700), P((255, 255, 255), 0.35))
    for k_, (lab, tt, x, col) in enumerate((('SHIP', ts, 200, (255, 70, 90)), ('OPEN', to, 420, (30, 160, 255)), ('CHECK', tc, 650, (40, 190, 110)), ('REPACK', tr, 880, (255, 160, 30)))):
        kk = pr(t, tt - 0.2, 0.3)
        pop(c, kk, x, 620, lambda: (board(c, x - 105, 560, 210, 100), neon_text(c, lab, x, 635, 48, col)))
    belt = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(30, 1060, 1020, 70), 35, 35); inked(c, belt, P((70, 75, 90)), 7)
    for i in range(14): c.drawCircle(70 + i * 72, 1095, 22, P((150, 155, 170))); c.drawCircle(70 + i * 72, 1095, 22, S(INK, 4))
    for i in range(6):
        x = (i * 210 + t * 160) % 1260 - 110
        box(c, x, 990, 150, 120, open_=1.0 if 320 < x < 760 else 0.0)
    for i, x in enumerate((200, 650)):
        person(c, x, 1600 if i == 0 else 1600, 0.5, (70, 140, 255) if i == 0 else (60, 200, 120), (255, 160, 30), mood='worried', sweat=1, t=t, arm_r=(20, -160), arm_l=(-20, -160), blink=blinking(t, i))
    if t > t66 - 0.5:
        k = pr(t, t66 - 0.5, 0.4); kb = pr(t, t66 - 0.1, 0.3)
        c.drawRect(skia.Rect.MakeWH(W, H), P((255, 255, 255), 0.5 * k))
        def tagd():
            c.save(); c.translate(520, 1100); c.rotate(-6); c.scale(0.85, 0.85)
            tg = path([(-330, -60), (-260, -200), (330, -200), (330, 200), (-260, 200), (-330, 60)]); inked(c, tg, LG((0, -200), (0, 200), [(255, 255, 255), (230, 230, 240)]), 8)
            c.drawCircle(-250, 0, 24, P((200, 200, 210))); c.drawCircle(-250, 0, 24, S(INK, 5))
            ctext(c, "ITEM'S PRICE", 20, -90, 52, (60, 60, 80))
            if kb > 0:
                c.drawLine(-200, -150, lerp(-200, 300, eo(kb)), lerp(-150, 170, eo(kb)), S((255, 70, 90), 14, 0.85))
            neon_text(c, 'UP TO 66%', 20, 90, 110, (255, 70, 90), cl(kb * 2))
            c.restore()
        pop(c, k, 540, 1100, tagd)
        if kb > 0.5: ctext(c, 'TO PROCESS A RETURN (OPTORO, VIA CNBC)', 540, 1360, 26, (40, 40, 60), 'Montserrat-ExtraBold.ttf')


def s_pallet(c, t):
    t0 = ph('so lots of'); tl = ph('liquidators'); tb = ph('bargain stores')
    sky_bg(c, t, (180, 190, 205))
    kp = pr(t, t0 - 0.1, 1.2)
    if t < tb - 0.4:
        pallet(c, 540, 1320, 700)
        n = 0
        for row in range(4):
            for j in range(4 - (row // 2)):
                n += 1; kk = pr(kp, n * 0.06, 0.25)
                if kk <= 0: continue
                x = 540 + (j - (3 - row // 2) / 2) * 165; y = 1240 - row * 120
                box(c, x, y - 400 * (1 - eo(kk)), 160, 118)
        if kp >= 1: c.drawRoundRect(skia.Rect.MakeXYWH(190, 800, 700, 520), 30, 30, P((220, 240, 255), 0.35)); c.drawRoundRect(skia.Rect.MakeXYWH(190, 800, 700, 520), 30, 30, S((255, 255, 255), 5, 0.9))
        if t > tl - 0.2:
            kg = pr(t, tl - 0.2, 0.3)
            c.save(); c.translate(860, 600); c.rotate(-40 + 40 * eo(kg))
            inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-40, -110, 220, 90), 20, 20), LG((0, -110), (0, -20), [(200, 130, 70), (150, 90, 40)]), 6)
            c.drawLine(70, -30, 70, 200, S(INK, 22)); c.drawLine(70, -30, 70, 200, S((180, 110, 60), 12)); c.restore()
            pop(c, pr(t, tl + 0.1, 0.3), 330, 620, lambda: (board(c, 160, 550, 340, 130, (255, 236, 90)), neon_text(c, 'SOLD!', 330, 645, 80, (255, 70, 90))))
    else:
        building(c, 150, 760, 780, 600, (255, 150, 120), 'BARGAIN STORE', (255, 200, 40), t, False)
        for i in range(6):
            x = 120 + i * 160; kk = pr(t, tb - 0.4 + i * 0.07, 0.3)
            if kk <= 0: continue
            pop(c, kk, x, 1700, lambda: person(c, x, 1700, 0.3, [(255, 140, 40), (70, 140, 255), (60, 200, 120), (255, 90, 120), (170, 110, 255)][i % 5], [(36, 44, 90), (200, 60, 70), (40, 120, 90), (90, 60, 140), (230, 160, 40)][i % 5], mood='happy', t=t, blink=blinking(t, i)))


def s_reveal(c, t):
    tw = ph('the wild part'); t90 = ph('ninety percent')
    c.drawRect(skia.Rect.MakeWH(W, H), LG((0, 0), (0, H), [(255, 240, 220), (245, 215, 180)]))
    pallet(c, 540, 1380, 760)
    for j in range(4): box(c, 260 + j * 185, 1300, 170, 130) if j != 1 else None
    ko = pr(t, t90 - 0.5, 0.5)
    box(c, 445, 1300, 170, 130, open_=ko)
    dim = pr(t, tw - 0.1, 0.4) * (1 - pr(t, t90 - 0.2, 0.25))
    if dim > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 30, 60), 0.4 * dim))
    if t > t90 - 0.2:
        k = pr(t, t90 - 0.2, 0.5)
        c.drawCircle(540, 1000, 420, P((255, 255, 220), 0.6 * k, 90))
        pop(c, k, 540, 1000, lambda: tv(c, 540, 1050 - 120 * eo(k), 520, t))
        for i in range(6): sparkle(c, 540 + 300 * math.cos(i + t), 1000 + 220 * math.sin(i * 2 + t), 30, k * abs(math.sin(t * 3 + i)))
        def q():
            board(c, 80, 270, 920, 300)
            neon_text(c, '"90% OF THE TIME,', 540, 370, 62, (30, 160, 255))
            neon_text(c, "THERE'S NOTHING", 540, 445, 62, (255, 70, 90)); neon_text(c, 'WRONG WITH IT."', 540, 520, 62, (255, 70, 90))
            ctext(c, 'TONY SCIARROTTA, REVERSE LOGISTICS ASSN., TO CNBC', 540, 600, 22, (40, 40, 60), 'Montserrat-ExtraBold.ttf')
        pop(c, pr(t, t90 + 0.1, 0.4), 540, 420, q)


def s_landfill(c, t):
    t58 = ph('five point eight')
    sky_bg(c, t, (150, 200, 120))
    hill = skia.Path(); hill.moveTo(0, 1400); hill.cubicTo(200, 1000, 800, 980, 1080, 1380); hill.lineTo(1080, 1920); hill.lineTo(0, 1920); hill.close()
    c.drawPath(hill, LG((0, 1000), (0, 1500), [(170, 150, 120), (130, 110, 90)])); c.drawPath(hill, S(INK, 7))
    rnd = random.Random(3)
    for i in range(26): box(c, rnd.uniform(120, 960), rnd.uniform(1120, 1400), rnd.uniform(60, 110), rot=rnd.uniform(-40, 40))
    tx = lerp(1300, 760, eo(pr(t, ph("what doesn't") - 0.1, 1.0)))
    c.save(); c.translate(tx, 1180)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(0, -60, 200, 160), 20, 20), P((255, 190, 30)), 7)
    c.drawRect(skia.Rect.MakeXYWH(30, -40, 120, 60), P((180, 220, 255))); c.drawRect(skia.Rect.MakeXYWH(30, -40, 120, 60), S(INK, 5))
    tilt = 25 * pr(t, t58 - 0.6, 0.6)
    c.save(); c.translate(-20, 60); c.rotate(-tilt)
    bed = path([(-320, -140), (0, -140), (0, 40), (-300, 40)]); inked(c, bed, P((40, 170, 255)), 7)
    for j in range(3): box(c, -250 + j * 90, -170, 80)
    c.restore()
    for x in (-220, 60): c.drawCircle(x + 40, 110, 46, P(INK)); c.drawCircle(x + 40, 110, 20, P((200, 200, 210)))
    c.restore()
    if t > t58 - 0.4:
        def sg():
            board(c, 90, 280, 900, 260)
            neon_text(c, 'UP TO 5.8 BILLION LBS', 540, 380, 64, (255, 70, 90)); neon_text(c, 'TO LANDFILL A YEAR', 540, 460, 58, (40, 160, 90))
            ctext(c, 'OPTORO ESTIMATE, VIA CNBC', 540, 520, 24, (40, 40, 60), 'Montserrat-ExtraBold.ttf')
        pop(c, pr(t, t58 - 0.4, 0.4), 540, 410, sg)


def s_end(c, t):
    t0 = ph('so that box'); tm = ph('would you buy')
    sky_bg(c, t)
    pallet(c, 540, 1320, 700)
    for row in range(3):
        for j in range(4 - row):
            box(c, 540 + (j - (3 - row) / 2) * 165, 1240 - row * 120, 160, 118, label='RETURN' if (row == 2 and j == 0) else None)
    if t < tm - 0.3:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'YOUR RETURN IS', 540, 355, 70, (30, 160, 255)); neon_text(c, 'ON A PALLET NOW', 540, 440, 70, (255, 190, 30), pr(t, t0 + 0.6, 0.3))
        pop(c, pr(t, t0 + 1.2, 0.3), 840, 820, lambda: sticky(c, 840, 820, 1.0, 8, 'SOLD', size=60))
    else:
        board(c, 90, 270, 900, 200)
        neon_text(c, 'WOULD YOU BUY A', 540, 355, 70, (30, 160, 255)); neon_text(c, 'MYSTERY PALLET?', 540, 440, 70, (255, 190, 30))
        for x, lab, col in ((300, 'YES', (40, 190, 110)), (780, 'NO', (255, 70, 90))):
            pop(c, pr(t, tm + 0.3, 0.3), x, 620, lambda: (board(c, x - 130, 560, 260, 120, col), neon_text(c, lab, x, 650, 80, (255, 255, 255))))
    person(c, 180, 1800, 0.66, (255, 140, 40), (36, 44, 90), mood='shock' if t < tm else 'happy', look=(0.8, -0.4), t=t, arm_r=(120, -60), arm_l=(-30, 230), blink=blinking(t))


SCENES = [
    (0.0, s_mountain), (ph('the national retail') - 0.15, s_stats), (ph('you print') - 0.15, s_drop), (ph('someone has to') - 0.15, s_warehouse),
    (ph('so lots of') - 0.15, s_pallet), (ph("and here's the") - 0.15, s_reveal), (ph("and what doesn't") - 0.15, s_landfill), (ph('so that box') - 0.15, s_end)]
SHAKES = [(ph('sixteen percent'), 8, 0.3), (ph('nineteen percent'), 8, 0.3), (ph('sixty six percent'), 12, 0.35), (ph('ninety percent'), 16, 0.45), (ph('five point eight'), 10, 0.35)]
TR = 0.32
