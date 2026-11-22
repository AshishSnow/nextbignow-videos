# ------------------------------------------------------------------ props (generic toy truck + tires: no bricks, logos or minifigures)
def tire(c, x, y, r, rot=0, real=False):
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawCircle(0, 0, r, P((40, 40, 46))); c.drawCircle(0, 0, r, S(INK, max(3, r * 0.08)))
    for i in range(12 if real else 8):
        a = i * math.pi / (6 if real else 4); c.drawLine(r * 0.75 * math.cos(a), r * 0.75 * math.sin(a), r * 0.98 * math.cos(a), r * 0.98 * math.sin(a), S((90, 90, 96), max(2, r * 0.07)))
    c.drawCircle(0, 0, r * 0.5, P((200, 200, 210) if real else (255, 214, 40))); c.drawCircle(0, 0, r * 0.5, S(INK, max(2, r * 0.05)))
    c.drawCircle(0, 0, r * 0.15, P((80, 80, 90))); c.restore()


def toy_truck(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-220, -150, 280, 130), 14, 14), P((60, 140, 230)), 7)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(60, -200, 150, 180), 18, 18), P((230, 50, 60)), 7)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(90, -180, 90, 70), 10, 10), P((180, 220, 255)), 5)
    for wx in (-150, 0, 150): tire(c, wx, -10, 48, t * 120)
    c.restore()


def medal(c, x, y, r, txt):
    for sx in (-1, 1): inked(c, path([(x + sx * 20, y), (x + sx * 70, y + r * 1.6), (x + sx * 20, y + r * 1.3)]), P((150, 22, 34)), 5)
    c.drawCircle(x, y, r, P((212, 160, 46))); c.drawCircle(x, y, r, S(INK, 7)); c.drawCircle(x, y, r * 0.8, S(INK, 3))
    ctext(c, txt, x, y + r * 0.15, r * 0.45, (34, 32, 30), 'Anton.ttf')


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tl = ph("it's lego")
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('The biggest tire maker', False, (34, 32, 30), 88), ('on Earth,', False, (34, 32, 30), 100), ('explained.', True, (150, 22, 34), 112)), 'in 30 seconds', 'per Guinness World Records')
    tire(c, 330, 1010, 170, t * 40, True)
    if t > tl - 0.3: pop(c, pr(t, tl - 0.3, 0.4), 780, 1060, lambda: toy_truck(c, 790, 1120, 0.85, t))
    person(c, 160, 1760, 0.5, (255, 140, 40), (36, 44, 90), mood='shock' if t > tl else 'happy', look=(0.6, -0.5), t=t, blink=blinking(t))


def s_record(c, t):
    t381 = ph('three hundred eighty'); tp = ph('period')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'THE WORLD RECORD', 540, 352, 66, (34, 32, 30))
    k = pr(t, t381 - 0.6, 1.4); n = int(80 * k); rnd = random.Random(2)
    for i in range(n):
        tire(c, 120 + (i * 83) % 840, 1250 - (i // 10) * 62 + rnd.uniform(-8, 8), 30, rnd.uniform(0, 90))
    if t > t381 - 0.2:
        pop(c, pr(t, t381 - 0.2, 0.4), 540, 620, lambda: (board(c, 150, 520, 780, 200, (255, 255, 255)), neon_text(c, '381 MILLION', 540, 630, 100, (190, 135, 30)), ctext(c, 'TIRES IN ONE YEAR (2010), PER GUINNESS', 540, 690, 26, (34, 32, 30))))
    if t > tp - 0.3: medal(c, 860, 470, 70, '#1')


def s_catch(c, t):
    tc = ph("here's the catch"); tt = ph('toy tires')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "THE CATCH", 540, 358, 70, (150, 22, 34))
    tire(c, 330, 860, 230, t * 20, True); ctext(c, 'A REAL TIRE', 330, 1150, 40, (34, 32, 30), 'Anton.ttf')
    if t > tt - 0.3:
        pop(c, pr(t, tt - 0.3, 0.4), 790, 900, lambda: (tire(c, 790, 900, 34, t * 60), ctext(c, 'A LEGO TIRE', 790, 1000, 40, (150, 22, 34), 'Anton.ttf')))
        toy_truck(c, 760, 1200, 0.45 * pr(t, tt, 0.4) + 0.001, t)


def s_cereal(c, t):
    tb = ph('cereal boxes')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'LIKE A WRITER WHO...', 540, 358, 60, (34, 32, 30))
    person(c, 330, 1760, 0.6, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.5, -0.4), t=t, arm_r=(150, -120), arm_l=(-30, 220), blink=blinking(t))
    if t > tb - 0.4:
        def box():
            c.save(); c.translate(760, 900); c.rotate(5)
            inked(c, skia.Rect.MakeXYWH(-150, -230, 300, 460), P((255, 190, 30)), 7)
            board(c, -120, -190, 240, 90, (255, 255, 255)); ctext(c, 'CRUNCHY O’S', 0, -132, 34, (150, 22, 34), 'Anton.ttf')
            for i in range(7): c.drawLine(-110, -40 + i * 34, 110 - (i % 2) * 50, -40 + i * 34, S((34, 32, 30), 4))
            c.restore()
        pop(c, pr(t, tb - 0.4, 0.4), 760, 900, box)


def s_end(c, t):
    td = ph('drive on')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "WORLD'S #1 TIRE MAKER", 540, 358, 58, (34, 32, 30))
    toy_truck(c, 560, 1000, 1.4, t)
    medal(c, 860, 600, 80, '#1')
    if t > td - 0.4: pop(c, pr(t, td - 0.4, 0.35), 540, 1200, lambda: (board(c, 120, 1140, 840, 120, (255, 214, 40)), neon_text(c, 'ZERO YOU CAN DRIVE ON', 540, 1222, 58, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('guinness world records') - 0.15, s_record), (ph("but here's the catch") - 0.15, s_catch), (ph("it's like the most") - 0.15, s_cereal), (ph("so the world's biggest") - 0.15, s_end)]
SHAKES = [(ph("it's lego"), 14, 0.4), (ph('three hundred eighty'), 16, 0.45), (ph('toy tires'), 10, 0.35), (ph('drive on'), 10, 0.35)]
TR = 0.32
