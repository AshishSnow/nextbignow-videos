# ------------------------------------------------------------------ props (generic furniture store: no real logos, colors or trade dress)
def plate(c, x, y, s=1.0, n=6, t=0.0, steam=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-200 + 10, -60 + 14, 400, 130), P(INK, 0.25, 8))
    inked(c, skia.Path().addOval(skia.Rect.MakeXYWH(-200, -60, 400, 130)), P((255, 255, 255)), 6)
    c.drawOval(skia.Rect.MakeXYWH(-150, -38, 300, 86), S((200, 200, 205), 3))
    for i in range(n):
        a = i / max(1, n) * 2 * math.pi; mx, my = 60 * math.cos(a), -6 + 22 * math.sin(a)
        c.drawCircle(mx, my, 34, RG(mx - 10, my - 12, 44, [(200, 120, 70), (150, 80, 40), (100, 50, 25)])); c.drawCircle(mx, my, 34, S(INK, 4))
    c.drawCircle(-120, 10, 22, P((230, 40, 60))); c.drawCircle(-120, 10, 22, S(INK, 3))       # berry jam
    if steam > 0:
        for k in range(3):
            p = skia.Path(); x0 = -50 + k * 50; p.moveTo(x0, -60)
            for j in range(1, 5): p.lineTo(x0 + 10 * math.sin(t * 4 + j + k), -60 - j * 22)
            c.drawPath(p, S((150, 150, 160), 4, 0.7 * steam))
    c.restore()


def sofa(c, x, y, s=1.0, rot=0, col=(90, 140, 200)):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawOval(skia.Rect.MakeXYWH(-260, 90, 520, 40), P((0, 0, 0), 0.25, 10))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-220, -120, 440, 140), 40, 40), LG((0, -120), (0, 20), [tuple(min(255, v + 50) for v in col), col]), 6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-230, 0, 460, 90), 24, 24), P(tuple(int(v * 0.85) for v in col)), 6)
    for sx in (-1, 1): inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx * 230 - 40, -40, 80, 140), 30, 30), P(col), 6)
    c.drawLine(0, 5, 0, 85, S(INK, 3))
    for sx in (-1, 1): c.drawLine(sx * 200, 100, sx * 210, 125, S(INK, 8))
    c.restore()


def warehouse(c, x, y, w, h, t, sign='FURNITURE'):
    c.drawRect(skia.Rect.MakeXYWH(x + 14, y + 14, w, h), P((0, 0, 0), 0.3, 10))
    inked(c, skia.Rect.MakeXYWH(x, y, w, h), LG((0, y), (0, y + h), [(220, 225, 235), (180, 190, 205)]), 7)
    for i in range(1, 8): c.drawLine(x + i * w / 8, y + 10, x + i * w / 8, y + h - 10, S((150, 160, 175), 3))
    inked(c, skia.Rect.MakeXYWH(x + w * 0.38, y + h * 0.55, w * 0.24, h * 0.45), P((120, 130, 150)), 5)
    board(c, x + w * 0.2, y + h * 0.12, w * 0.6, h * 0.24); neon_text(c, sign, x + w / 2, y + h * 0.29, 60, (34, 32, 30))


def clock(c, x, y, r, t, spin=1.0):
    c.drawCircle(x, y, r, P((255, 255, 255))); c.drawCircle(x, y, r, S(INK, 8))
    for i in range(12): a = i * math.pi / 6; c.drawLine(x + 0.8 * r * math.cos(a), y + 0.8 * r * math.sin(a), x + 0.9 * r * math.cos(a), y + 0.9 * r * math.sin(a), S(INK, 4))
    a = t * 5 * spin - math.pi / 2; c.drawLine(x, y, x + 0.7 * r * math.cos(a), y + 0.7 * r * math.sin(a), S(INK, 7))
    a2 = t * 0.4 * spin - math.pi / 2; c.drawLine(x, y, x + 0.45 * r * math.cos(a2), y + 0.45 * r * math.sin(a2), S(INK, 10))


def headline(c, t, lines, tag, sub):
    c.save(); c.translate(540, 235); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-190, -42, 380, 76), P((212, 160, 46))); f = serif(44, 400, True); tw = f.measureText(tag); c.drawString(tag, -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col, sz) in enumerate(lines):
        f = serif(sz, 700 if not it else 500, it); tw = f.measureText(txt)
        while tw > 940: f = serif(f.getSize() * 0.95, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 112, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); c.drawString(sub, 540 - f.measureText(sub) / 2, 385 + len(lines) * 112 - 40, f, P((90, 86, 80), pr(t, 0.8, 0.3)))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    ts = ph('buy the sofa')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Cheap meatballs,', False, (34, 32, 30), 104), ('expensive sofa,', False, (34, 32, 30), 104), ('explained.', True, (150, 22, 34), 112)), 'in 35 seconds', 'per IKEA’s own history')
    plate(c, 330, 1060, 1.05, 6, t)
    if t > ts - 0.3: pop(c, pr(t, ts - 0.3, 0.4), 780, 1060, lambda: sofa(c, 780, 1060, 0.75, -4))
    person(c, 540, 1760, 0.5, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, arm_r=(120, -160), arm_l=(-120, -160), blink=blinking(t))


def s_museum(c, t):
    tf = ph('fifties'); tfs = ph('full stomachs'); tl = ph('stay longer'); tb = ph('buy more')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "THE FOUNDER'S DISCOVERY", 540, 358, 58, (34, 32, 30))
    if t > tf - 0.3:
        c.save(); c.translate(820, 520); c.rotate(-8); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -50, 300, 100), 14, 14); c.drawRRect(r, S((200, 40, 40), 8, 0.9)); ctext(c, 'SWEDEN, 1950s', 0, 18, 46, (230, 40, 50), 'Anton.ttf'); c.restore()
    warehouse(c, 140, 640, 800, 480, t)
    if t > tfs - 0.3: pop(c, pr(t, tfs - 0.3, 0.35), 300, 1000, lambda: plate(c, 300, 1000, 0.7, 6, t))
    if t > tl - 0.3: pop(c, pr(t, tl - 0.3, 0.35), 540, 1000, lambda: clock(c, 540, 1000, 100, t, 3.0))
    if t > tb - 0.3: pop(c, pr(t, tb - 0.3, 0.35), 790, 1000, lambda: sofa(c, 790, 1000, 0.5, 6))
    if t > tb: pop(c, pr(t, tb, 0.3), 540, 1290, lambda: (board(c, 150, 1230, 780, 110, (255, 214, 40)), neon_text(c, 'FULL = STAY + BUY MORE', 540, 1308, 54, (34, 32, 30))))
    person(c, 540, 1800, 0.45, (255, 140, 40), (36, 44, 90), mood='happy' if t > tfs else 'neutral', look=(0, -0.6), t=t, blink=blinking(t))


def s_billion(c, t):
    tb = ph('a billion meatballs'); ti = ph('so ikea put')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'FOOD INSIDE THE STORE', 540, 358, 60, (34, 32, 30))
    rnd = random.Random(5); k = pr(t, tb - 0.6, 1.4)
    n = int(60 * k)
    for i in range(n):
        x = 130 + (i * 97) % 820; y = 1180 - (i // 9) * 70 + rnd.uniform(-10, 10)
        c.drawCircle(x, y, 32, RG(x - 10, y - 12, 44, [(200, 120, 70), (150, 80, 40), (100, 50, 25)])); c.drawCircle(x, y, 32, S(INK, 4))
    plate(c, 540, 1300, 0.9, 6, t)
    if t > tb - 0.2:
        pop(c, pr(t, tb - 0.2, 0.4), 540, 610, lambda: (board(c, 170, 520, 740, 170, (255, 255, 255)), neon_text(c, '~1 BILLION', 540, 610, 96, (190, 135, 30)), ctext(c, 'MEATBALLS A YEAR, PER IKEA (2020)', 540, 668, 28, (34, 32, 30))))


def s_twist(c, t):
    tw = ph("here's the twist"); t5 = ph('five percent')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'THE TWIST', 540, 358, 70, (150, 22, 34))
    plate(c, 330, 860, 0.9, 6, t)
    sofa(c, 760, 880, 0.6, 4)
    if t > t5 - 0.3:
        def pct():
            c.drawCircle(540, 1180, 150, P((212, 160, 46))); c.drawCircle(540, 1180, 150, S(INK, 8))
            f = serif(110, 700); s_ = '~5%'; c.drawString(s_, 540 - f.measureText(s_) / 2, 1220, f, P((34, 32, 30)))
        pop(c, pr(t, t5 - 0.3, 0.4), 540, 1180, pct)
        ctext(c, 'TARGET PROFIT ON FOOD (IKEA MUSEUM)', 540, 1380, 28, (34, 32, 30))


def s_end(c, t):
    tbz = ph("aren't the business"); ts = ph('for the sofa')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "NOT THE BUSINESS...", 540, 358, 64, (34, 32, 30))
    plate(c, 540, 700, 1.2, 6, t, 1.0)
    if t > tbz - 0.3:
        c.drawLine(300, 620, 780, 790, S((150, 22, 34), 14)); c.drawLine(780, 620, 300, 790, S((150, 22, 34), 14))
    if t > ts - 0.4:
        pop(c, pr(t, ts - 0.4, 0.4), 540, 1050, lambda: sofa(c, 540, 1050, 1.0, 0))
        pop(c, pr(t, ts - 0.2, 0.3), 540, 1300, lambda: (board(c, 170, 1240, 740, 110, (255, 214, 40)), neon_text(c, "THEY'RE WHY YOU STAY", 540, 1318, 56, (34, 32, 30))))
        person(c, 540, 1170, 0.4, (255, 140, 40), (36, 44, 90), mood='happy', look=(0, -0.6), t=t, blink=blinking(t))


SCENES = [(0.0, s_hook), (ph("ikea's own museum") - 0.15, s_museum), (ph('so ikea put') - 0.15, s_billion), (ph("but here's the twist") - 0.15, s_twist), (ph("so the meatballs aren't") - 0.15, s_end)]
SHAKES = [(ph('full stomachs'), 8, 0.3), (ph('a billion meatballs'), 16, 0.45), (ph('five percent'), 12, 0.4), (ph('for the sofa'), 10, 0.35)]
TR = 0.32
