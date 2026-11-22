# ------------------------------------------------------------------ props (generic chicken shop: no real logos or trade dress)
def sandwich(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    top = skia.Path(); top.moveTo(-100, -10); top.cubicTo(-100, -100, 100, -100, 100, -10); top.close()
    inked(c, top, LG((0, -95), (0, -10), [(250, 195, 110), (215, 145, 60)]), 6)
    inked(c, path([(-115, -8), (-60, -22), (0, -6), (60, -24), (115, -6), (110, 30), (-110, 30)]), LG((0, -24), (0, 30), [(230, 160, 70), (180, 110, 40)]), 6)
    for i in range(6): c.drawCircle(-80 + i * 32, 8, 5, P((150, 90, 30)))
    c.drawRect(skia.Rect.MakeXYWH(-60, -14, 18, 10), P((120, 200, 90))); c.drawRect(skia.Rect.MakeXYWH(30, -16, 18, 10), P((120, 200, 90)))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-100, 28, 200, 40), 20, 20), P((225, 150, 70)), 6)
    c.restore()


def calendar(c, x, y, s, t, k_closed):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-370 + 10, -150 + 12, 740, 300), P(INK, 0.25, 6))
    inked(c, skia.Rect.MakeXYWH(-370, -150, 740, 300), P((255, 255, 255)), 6)
    inked(c, skia.Rect.MakeXYWH(-370, -150, 740, 70), P((60, 60, 70)), 6)
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    for i, d in enumerate(days):
        x0 = -370 + i * 740 / 7
        ctext(c, d, x0 + 53, -102, 26, (255, 255, 255), 'Anton.ttf')
        if i: c.drawLine(x0, -80, x0, 150, S(INK, 3))
        if i < 6: c.drawCircle(x0 + 53, 40, 30, S((40, 170, 90), 6))
    if k_closed > 0:
        x0 = -370 + 6 * 740 / 7
        c.drawLine(x0 + 10, -70, x0 + 96, 140, S((220, 40, 50), 12 * k_closed)); c.drawLine(x0 + 96, -70, x0 + 10, 140, S((220, 40, 50), 12 * k_closed))
    c.restore()


def shop(c, x, y, w, t, sign, col):
    h = w * 0.7
    c.drawRect(skia.Rect.MakeXYWH(x + 12, y + 12, w, h), P((0, 0, 0), 0.3, 10))
    inked(c, skia.Rect.MakeXYWH(x, y, w, h), LG((0, y), (0, y + h), [(255, 250, 240), (230, 220, 205)]), 6)
    inked(c, path([(x - 20, y + 10), (x + w + 20, y + 10), (x + w, y - h * 0.2), (x, y - h * 0.2)]), P(col), 6)
    inked(c, skia.Rect.MakeXYWH(x + w * 0.1, y + h * 0.3, w * 0.5, h * 0.5), P((255, 210, 120)), 5)
    inked(c, skia.Rect.MakeXYWH(x + w * 0.68, y + h * 0.35, w * 0.22, h * 0.65), P((120, 80, 60)), 5)
    ctext(c, sign, x + w / 2, y - h * 0.03, w * 0.11, (255, 255, 255), 'Anton.ttf')


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    td = ph('almost double')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Closed on Sundays,', False, (34, 32, 30), 98), ('still crushing it,', False, (34, 32, 30), 98), ('explained.', True, (150, 22, 34), 112)), 'in 40 seconds', 'per 2025 sales data')
    calendar(c, 540, 930, 1.15, t, pr(t, ph('every sunday') - 0.1, 0.4))
    if t > td - 0.3: pop(c, pr(t, td - 0.3, 0.4), 540, 1150, lambda: (board(c, 260, 1090, 560, 110, (255, 214, 40)), neon_text(c, '~2x PER STORE', 540, 1168, 64, (34, 32, 30))))
    person(c, 160, 1760, 0.5, (255, 140, 40), (36, 44, 90), mood='shock' if t > td else 'happy', look=(0.6, -0.5), t=t, blink=blinking(t))


def s_compare(c, t):
    t77 = ph('seven point seven'); t41 = ph('four point one'); t7 = ph('open seven days')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'AVERAGE U.S. STORE, 2025', 540, 352, 60, (34, 32, 30))
    ctext(c, 'SOURCE: QSR MAGAZINE (YEAR-END 2025 U.S. STORES)', 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t77 - 0.3, 0.8), pr(t, t41 - 0.3, 0.8), 'CHICK-FIL-A', "McDONALD'S", '$7.7M', '$4.1M', 7.7 * 75, 4.09 * 75, (255, 190, 30), (150, 150, 160), 0, '')
    if t > t7 - 0.3:
        pop(c, pr(t, t7 - 0.3, 0.3), 290, 1340, lambda: (board(c, 130, 1290, 320, 90, (255, 255, 255)), neon_text(c, '6 DAYS', 290, 1352, 50, (150, 22, 34))))
        pop(c, pr(t, t7 - 0.1, 0.3), 790, 1340, lambda: (board(c, 630, 1290, 320, 90, (255, 255, 255)), neon_text(c, '7 DAYS', 790, 1352, 50, (34, 32, 30))))


def s_quote(c, t):
    tq = ph('i never have')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'WHAT DO SUNDAYS COST?', 540, 358, 58, (34, 32, 30))
    k = pr(t, tq - 0.2, 0.5)
    if k > 0:
        c.save(); c.translate(540, 760); s_ = 0.9 + 0.1 * eo(k); c.scale(s_, s_)
        board(c, -440, -190, 880, 380)
        f = serif(140, 700); c.drawString('“', -410, -60, f, P((190, 135, 30)))
        for i, ln in enumerate(('I never have, because it’s', 'never something that', 'we’re entertaining.')):
            f = serif(52, 400, True); tw = f.measureText(ln); c.drawString(ln, -tw / 2, -50 + i * 72, f, P((150, 22, 34) if i == 0 else (34, 32, 30)))
        f = serif(28, 400); s2 = "Chick-fil-A's CEO to Fortune, Oct 2026"; c.drawString(s2, -f.measureText(s2) / 2, 160, f, P((90, 86, 80)))
        c.restore()
    calendar(c, 540, 1240, 0.7, t, 1.0)


def s_kid(c, t):
    tb = ph('best grades')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'SIX DAYS. STILL #1.', 540, 358, 64, (34, 32, 30))
    person(c, 400, 1760, 0.62, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.5, -0.5), t=t, arm_r=(150, -220), arm_l=(-30, 220), blink=blinking(t))
    if t > tb - 0.4:
        def card():
            c.save(); c.translate(760, 860); c.rotate(6)
            board(c, -170, -210, 340, 420, (255, 255, 255)); ctext(c, 'REPORT CARD', 0, -150, 34, (34, 32, 30), 'Anton.ttf')
            f = serif(220, 700); c.drawString('A+', -f.measureText('A+') / 2, 90, f, P((150, 22, 34))); c.restore()
        pop(c, pr(t, tb - 0.4, 0.4), 760, 860, card)


def s_end(c, t):
    ts = ph('six days not seven')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'SUNDAYS OFF...', 540, 358, 70, (34, 32, 30))
    shop(c, 120, 820, 380, t, 'CHICKEN', (255, 190, 30))
    shop(c, 580, 820, 380, t, 'BURGERS', (150, 150, 160))
    sandwich(c, 310, 1240, 1.0, -6)
    if t > ts - 0.4:
        pop(c, pr(t, ts - 0.4, 0.35), 540, 590, lambda: (board(c, 180, 530, 720, 120, (255, 214, 40)), neon_text(c, '...STILL WINS PER STORE', 540, 612, 54, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('the average chick') - 0.15, s_compare), (ph('so has the boss') - 0.15, s_quote), (ph("it's like a kid") - 0.15, s_kid), (ph('so chick fil a takes') - 0.15, s_end)]
SHAKES = [(ph('almost double'), 12, 0.4), (ph('seven point seven'), 16, 0.45), (ph('open seven days'), 8, 0.3), (ph('i never have'), 10, 0.35), (ph('six days not seven'), 10, 0.35)]
TR = 0.32
