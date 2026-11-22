# ------------------------------------------------------------------ props (generic coffee cup + phone wallet: no siren logo, green trade dress)
def coffee(c, x, y, s=1.0, rot=0, t=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, path([(-80, -120), (80, -120), (62, 130), (-62, 130)]), P((255, 255, 255)), 6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-92, -150, 184, 36), 12, 12), P((90, 70, 60)), 6)
    inked(c, path([(-76, -40), (76, -40), (70, 40), (-70, 40)]), P((180, 130, 90)), 5)
    for k in range(3):
        p = skia.Path(); x0 = -30 + k * 30; p.moveTo(x0, -160)
        for j in range(1, 5): p.lineTo(x0 + 8 * math.sin(t * 4 + j + k), -160 - j * 20)
        c.drawPath(p, S((150, 150, 160), 4, 0.7))
    c.restore()


def app_phone(c, x, y, s, t, bal_k=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-140, -260, 280, 520), 36, 36), P((30, 30, 36)), 7)
    c.drawRoundRect(skia.Rect.MakeXYWH(-122, -230, 244, 460), 20, 20, P((252, 250, 244)))
    ctext(c, 'BALANCE', 0, -150, 34, (90, 86, 80), 'Anton.ttf')
    f = serif(80, 700); s_ = '$%d' % int(25 * bal_k); c.drawString(s_, -f.measureText(s_) / 2, -60, f, P((34, 32, 30)))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-90, 60, 180, 70), 20, 20), P((255, 190, 30)), 4); ctext(c, 'RELOAD', 0, 108, 34, (34, 32, 30), 'Anton.ttf')
    c.restore()


def vault(c, x, y, s, k_open, t):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.Rect.MakeXYWH(-260, -220, 520, 440), P((150, 150, 160)), 8)
    c.drawCircle(0, 0, 150, P((190, 190, 200))); c.drawCircle(0, 0, 150, S(INK, 7))
    for i in range(6): a = i * math.pi / 3 + t; c.drawLine(0, 0, 110 * math.cos(a), 110 * math.sin(a), S(INK, 8))
    c.restore()


def pizza(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 170, P((230, 170, 90))); c.drawCircle(0, 0, 170, S(INK, 6)); c.drawCircle(0, 0, 140, P((240, 200, 110)))
    for a in range(6): c.drawLine(0, 0, 170 * math.cos(a * math.pi / 3), 170 * math.sin(a * math.pi / 3), S(INK, 3))
    rnd = random.Random(3)
    for i in range(10): c.drawCircle(rnd.uniform(-110, 110), rnd.uniform(-110, 110), 18, P((200, 50, 50)))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tb = ph('billion dollars')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Your coffee app', False, (34, 32, 30), 104), ('is holding your cash,', False, (34, 32, 30), 92), ('explained.', True, (150, 22, 34), 112)), 'in 30 seconds', "per Starbucks' 2025 annual report")
    coffee(c, 300, 1020, 1.0, -4, t)
    app_phone(c, 760, 1010, 0.75, t)
    if t > tb - 0.3: pop(c, pr(t, tb - 0.3, 0.4), 540, 1310, lambda: (board(c, 220, 1250, 640, 110, (255, 214, 40)), neon_text(c, '~$1.75 BILLION', 540, 1328, 66, (150, 22, 34))))


def s_report(c, t):
    tl = ph('loaded onto'); tr = ph('annual report'); ts = ph('september twenty')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'LOADED, NOT SPENT', 540, 358, 66, (34, 32, 30))
    app_phone(c, 300, 820, 0.8, t, pr(t, tl, 1.0))
    for i in range(3):
        k = pr(t, tl + 0.2 + i * 0.2, 0.4)
        if k > 0: giftcard(c, 760, 680 + i * 140, 280, -6 + i * 6, (255, 190, 30), '', 1.0, 0.0, False, t)
    if t > tr - 0.3:
        def doc():
            board(c, 140, 1130, 800, 200, (255, 255, 255))
            f = serif(36, 600); s1 = 'Stored value cards and loyalty program'; c.drawString(s1, 540 - f.measureText(s1) / 2, 1200, f, P((34, 32, 30)))
            f = serif(64, 700); s2 = '$1,751.7 million'; c.drawString(s2, 540 - f.measureText(s2) / 2, 1285, f, P((150, 22, 34)))
        pop(c, pr(t, tr - 0.3, 0.4), 540, 1230, doc)
    if t > ts - 0.3:
        c.save(); c.translate(740, 1110); c.rotate(-6); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -40, 300, 80), 12, 12); c.drawRRect(r, S((200, 40, 40), 7, 0.9)); ctext(c, 'SEP 28, 2025', 0, 16, 40, (230, 40, 50), 'Anton.ttf'); c.restore()


def s_twist(c, t):
    tp = ph('pay first'); tl = ph('coffee later'); th = ph('in between')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'PAY FIRST. COFFEE LATER.', 540, 358, 56, (34, 32, 30))
    c.drawLine(140, 900, 940, 900, S(INK, 6))
    if t > tp - 0.3: pop(c, pr(t, tp - 0.3, 0.3), 220, 760, lambda: (app_phone(c, 220, 700, 0.42, t), ctext(c, 'YOU PAY', 220, 980, 40, (34, 32, 30), 'Anton.ttf')))
    if t > tl - 0.3: pop(c, pr(t, tl - 0.3, 0.3), 860, 760, lambda: (coffee(c, 860, 740, 0.7, 0, t), ctext(c, 'COFFEE', 860, 980, 40, (34, 32, 30), 'Anton.ttf')))
    if t > th - 0.4:
        pop(c, pr(t, th - 0.4, 0.4), 540, 760, lambda: vault(c, 540, 740, 0.45, 0, t))
        pop(c, pr(t, th - 0.2, 0.3), 540, 1150, lambda: (board(c, 160, 1090, 760, 110, (255, 214, 40)), neon_text(c, 'STARBUCKS HOLDS IT', 540, 1168, 58, (150, 22, 34))))


def s_pizza(c, t):
    tw = ph('a week before')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE PIZZA...", 540, 358, 66, (34, 32, 30))
    pizza(c, 540, 800, 1.1)
    if t > tw - 0.3:
        def cal():
            board(c, 220, 1080, 640, 130, (255, 255, 255)); neon_text(c, 'PAID: MONDAY', 540, 1135, 46, (34, 32, 30)); ctext(c, 'BAKED: NEXT MONDAY', 540, 1190, 34, (150, 22, 34), 'Anton.ttf')
        pop(c, pr(t, tw - 0.3, 0.4), 540, 1140, cal)


def s_end(c, t):
    tf = ph('for free')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'EVERY TOP-UP...', 540, 358, 66, (34, 32, 30))
    app_phone(c, 540, 820, 1.0, t)
    if t > ph('kind of lending') - 0.3:
        for i in range(4):
            v = pr(t, ph('kind of lending') - 0.2 + i * 0.15, 0.7)
            if 0 < v < 1: coin(c, 540 + 300 * eio(v), 700 - 150 * math.sin(math.pi * v), 30)
    if t > tf - 0.3: pop(c, pr(t, tf - 0.3, 0.3), 540, 1220, lambda: (board(c, 140, 1160, 800, 110, (255, 214, 40)), neon_text(c, 'A FREE LOAN TO STARBUCKS', 540, 1238, 52, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph("it's money people") - 0.15, s_report), (ph("but here's the twist") - 0.15, s_twist), (ph("it's like paying") - 0.15, s_pizza), (ph('so every time') - 0.15, s_end)]
SHAKES = [(ph('billion dollars'), 14, 0.4), (ph('annual report'), 8, 0.3), (ph('in between'), 10, 0.35), (ph('for free'), 10, 0.35)]
TR = 0.32
