# ------------------------------------------------------------------ props (generic boxes, cloud, servers: no logos or smile arrow)
def parcel(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, skia.Rect.MakeXYWH(-110, -80, 220, 160), P((205, 160, 110)), 6)
    c.drawRect(skia.Rect.MakeXYWH(-20, -80, 40, 160), P((230, 200, 150))); c.drawRect(skia.Rect.MakeXYWH(-20, -80, 40, 160), S(INK, 3))
    c.drawLine(-110, -40, 110, -40, S(INK, 3)); c.restore()


def cloud_icon(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path()
    for cx, cy, r in ((-90, 20, 80), (0, -30, 110), (100, 10, 90), (40, 50, 80), (-40, 60, 70)): p.addCircle(cx, cy, r)
    p.setFillType(skia.PathFillType.kWinding)
    c.drawPath(p, P((255, 255, 255))); c.drawPath(p, S(INK, 7))
    c.drawPath(p, P((255, 255, 255)))
    c.restore()


def server(c, x, y, s=1.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.Rect.MakeXYWH(-90, -220, 180, 440), P((60, 64, 74)), 7)
    for i in range(6):
        inked(c, skia.Rect.MakeXYWH(-75, -200 + i * 70, 150, 54), P((90, 96, 110)), 3)
        on = int(t * 4 + i) % 3 != 0
        c.drawCircle(50, -173 + i * 70, 7, P((80, 230, 140) if on else (40, 80, 60)))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tc = ph('the cloud')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (("Amazon's real store", False, (34, 32, 30), 98), ('is in the cloud,', False, (34, 32, 30), 98), ('explained.', True, (150, 22, 34), 112)), 'in 35 seconds', "per Amazon's 2025 results")
    for i in range(4): parcel(c, 230 + (i % 2) * 120, 1150 - (i // 2) * 140, 0.8, -6 + i * 5)
    if t > tc - 0.4:
        pop(c, pr(t, tc - 0.4, 0.4), 760, 860, lambda: cloud_icon(c, 760, 860, 1.0))
        server(c, 760, 1120, 0.55 * pr(t, tc, 0.4) + 0.001, t)
    person(c, 540, 1760, 0.5, (255, 140, 40), (36, 44, 90), mood='shock' if t > tc else 'happy', look=(0.3, -0.6), t=t, blink=blinking(t))


def s_profit(c, t):
    t80 = ph('eighty billion'); t45 = ph('forty five'); th = ph('more than half')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'AMAZON, 2025 PROFIT', 540, 352, 62, (34, 32, 30))
    ctext(c, 'OPERATING INCOME. SOURCE: AMAZON Q4 2025 RELEASE', 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t80 - 0.3, 0.8), pr(t, t45 - 0.3, 0.8), 'ALL OF AMAZON', 'JUST AWS', '$80.0B', '$45.6B', 80.0 * 7.5, 45.6 * 7.5, (150, 150, 160), (255, 190, 30), pr(t, th - 0.2, 0.3), 'MORE THAN HALF')


def s_split(c, t):
    tf = ph('a fifth'); tb = ph('the boxes'); ts = ph('the servers')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'SALES vs PROFIT', 540, 358, 70, (34, 32, 30))
    def pie(cx, cy, r, frac, lab, k):
        if k <= 0: return
        c.drawCircle(cx, cy, r, P((225, 225, 230))); c.drawCircle(cx, cy, r, S(INK, 6))
        p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), -90, 360 * frac * eo(k), False); p.close()
        c.drawPath(p, P((255, 190, 30))); c.drawPath(p, S(INK, 5))
        ctext(c, lab, cx, cy + r + 60, 40, (34, 32, 30), 'Anton.ttf')
    pie(300, 760, 190, 0.18, 'AWS: 18% OF SALES', pr(t, tf - 0.4, 0.6))
    pie(780, 760, 190, 0.57, 'AWS: 57% OF PROFIT', pr(t, tf + 0.6, 0.6))
    if t > tb - 0.3: pop(c, pr(t, tb - 0.3, 0.3), 300, 1180, lambda: (parcel(c, 300, 1180, 0.8), ctext(c, 'BRING THE CROWDS', 300, 1290, 34, (34, 32, 30), 'Anton.ttf')))
    if t > ts - 0.3: pop(c, pr(t, ts - 0.3, 0.3), 780, 1180, lambda: (server(c, 780, 1150, 0.35, t), ctext(c, 'BRING THE MONEY', 780, 1290, 34, (150, 22, 34), 'Anton.ttf')))


def s_mall(c, t):
    tp = ph('parking garage')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE A MALL...", 540, 358, 66, (34, 32, 30))
    inked(c, skia.Rect.MakeXYWH(140, 640, 520, 600), P((240, 235, 225)), 7); ctext(c, 'MALL', 400, 720, 60, (34, 32, 30), 'Anton.ttf')
    for i in range(3):
        for j in range(2): inked(c, skia.Rect.MakeXYWH(180 + i * 160, 780 + j * 200, 120, 150), P((180, 210, 240)), 4)
    if t > tp - 0.4:
        def garage():
            inked(c, skia.Rect.MakeXYWH(680, 800, 300, 440), P((200, 200, 205)), 7); ctext(c, 'P', 830, 960, 130, (34, 32, 30), 'Anton.ttf')
            for k in range(3): c.drawLine(700, 1020 + k * 60, 960, 1020 + k * 60, S(INK, 4))
            board(c, 690, 1100, 280, 90, (255, 214, 40)); neon_text(c, '$$$', 830, 1162, 56, (150, 22, 34))
        pop(c, pr(t, tp - 0.4, 0.4), 830, 1020, garage)


def s_end(c, t):
    tw = ph('with a store')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'NOT A STORE WITH A CLOUD...', 540, 358, 52, (34, 32, 30))
    cloud_icon(c, 540, 800, 1.6)
    if t > tw - 0.5:
        pop(c, pr(t, tw - 0.5, 0.4), 540, 900, lambda: (parcel(c, 540, 930, 0.7), None))
        pop(c, pr(t, tw - 0.3, 0.3), 540, 1230, lambda: (board(c, 160, 1170, 760, 110, (255, 214, 40)), neon_text(c, 'A CLOUD WITH A STORE', 540, 1248, 58, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('in twenty twenty five') - 0.15, s_profit), (ph('but aws was') - 0.15, s_split), (ph("it's like a mall") - 0.15, s_mall), (ph("so amazon isn't") - 0.15, s_end)]
SHAKES = [(ph('the cloud'), 10, 0.35), (ph('forty five'), 16, 0.45), (ph('the servers'), 10, 0.35), (ph('with a store'), 10, 0.35)]
TR = 0.32
