# ------------------------------------------------------------------ props (generic theme park + film: no castles, characters, ears or logos)
def ferris(c, x, y, r, t, k=1.0):
    c.save(); c.translate(x, y); c.scale(k, k)
    c.drawLine(-r * 0.6, r * 1.25, 0, 0, S(INK, 10)); c.drawLine(r * 0.6, r * 1.25, 0, 0, S(INK, 10))
    c.drawCircle(0, 0, r, S(INK, 8)); c.drawCircle(0, 0, r * 0.18, P((255, 214, 40))); c.drawCircle(0, 0, r * 0.18, S(INK, 5))
    for i in range(10):
        a = t * 0.6 + i * math.pi / 5; ex, ey = r * math.cos(a), r * math.sin(a)
        c.drawLine(0, 0, ex, ey, S(INK, 3))
        inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(ex - 26, ey, 52, 44), 10, 10), P([(230, 40, 60), (40, 120, 220), (255, 190, 30), (60, 170, 90)][i % 4]), 4)
    c.restore()


def film_reel(c, x, y, r, t):
    c.save(); c.translate(x, y); c.rotate(t * 40)
    c.drawCircle(0, 0, r, P((60, 60, 70))); c.drawCircle(0, 0, r, S(INK, 6))
    for i in range(6):
        a = i * math.pi / 3; c.drawCircle(r * 0.55 * math.cos(a), r * 0.55 * math.sin(a), r * 0.2, P((252, 250, 244)))
    c.drawCircle(0, 0, r * 0.12, P((252, 250, 244))); c.restore()


def ticket_stub(c, x, y, w, rot, txt, col=(255, 214, 40)):
    h = w * 0.45; c.save(); c.translate(x, y); c.rotate(rot)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 10, 10), P(col), 6)
    c.drawLine(w * 0.2, -h / 2 + 8, w * 0.2, h / 2 - 8, S(INK, 3)); ctext(c, txt, -w * 0.12, h * 0.12, w * 0.09, (34, 32, 30), 'Anton.ttf'); c.restore()


def tag_item(c, x, y, lab, k, col=(255, 255, 255)):
    pop(c, k, x, y, lambda: (board(c, x - 120, y - 46, 240, 92, col), neon_text(c, lab, x, y + 16, 44, (34, 32, 30))))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tw = ph('way more')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Parks beat movies,', False, (34, 32, 30), 100), ('by a mile,', False, (34, 32, 30), 100), ('explained.', True, (150, 22, 34), 112)), 'in 35 seconds', "per Disney's 2025 results")
    film_reel(c, 280, 1000, 150, t)
    ferris(c, 760, 960, 210, t, 0.8 + 0.25 * pr(t, tw - 0.3, 0.4))
    person(c, 540, 1760, 0.5, (255, 140, 40), (36, 44, 90), mood='shock' if t > tw else 'happy', look=(0.3, -0.6), t=t, blink=blinking(t))


def s_compare(c, t):
    t10 = ph('almost ten'); t47 = ph('four point seven'); td = ph('more than double')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'DISNEY, FISCAL 2025', 540, 352, 64, (34, 32, 30))
    ctext(c, 'OPERATING INCOME. SOURCE: DISNEY FY2025 EARNINGS RELEASE', 540, 445, 22, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t10 - 0.3, 0.8), pr(t, t47 - 0.3, 0.8), 'PARKS + CRUISES', 'MOVIES + TV', '$10.0B', '$4.7B', 9.995 * 60, 4.674 * 60, (255, 190, 30), (150, 150, 160), pr(t, td - 0.2, 0.3), 'MORE THAN 2x')


def s_why(c, t):
    to = ph('one payment'); items = [('tickets', 'TICKETS'), ('hotels', 'HOTELS'), ('food', 'FOOD'), ('toys', 'TOYS'), ('that photo', 'THE PHOTO')]
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'BUT WHY?', 540, 358, 70, (150, 22, 34))
    if t > to - 0.4:
        c.drawLine(540, 520, 540, 1280, S(INK, 3))
        ctext(c, 'MOVIE', 290, 560, 40, (34, 32, 30), 'Anton.ttf'); ctext(c, 'PARK DAY', 790, 560, 40, (34, 32, 30), 'Anton.ttf')
        ticket_stub(c, 290, 780, 300, -6, '$1 TICKET' if False else 'ONE TICKET')
    for i, (w, lab) in enumerate(items):
        try: tw = ph(w, after=to)
        except KeyError: continue
        tag_item(c, 790, 660 + i * 125, lab, pr(t, tw - 0.2, 0.3), (255, 214, 40) if i % 2 == 0 else (255, 255, 255))


def s_band(c, t):
    ts = ph('the songs'); tb = ph('pay the bills')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE A BAND", 540, 358, 66, (34, 32, 30))
    if t > ts - 0.3:
        for i in range(4):
            v = pr(t, ts - 0.3 + i * 0.1, 0.4)
            if v > 0:
                nx, ny = 200 + i * 120, 760 - 40 * math.sin(t * 3 + i)
                c.drawOval(skia.Rect.MakeXYWH(nx - 30, ny - 18, 56, 40), P((34, 32, 30), v)); c.drawLine(nx + 22, ny, nx + 22, ny - 110, S((34, 32, 30), 8, v)); c.drawLine(nx + 22, ny - 110, nx + 60, ny - 80, S((34, 32, 30), 8, v))
    if t > tb - 0.6:
        def shirt():
            p = path([(560, 700), (640, 660), (760, 660), (840, 700), (900, 780), (850, 820), (830, 790), (830, 1060), (570, 1060), (570, 790), (550, 820), (500, 780)])
            inked(c, p, P((255, 190, 30)), 7); ctext(c, 'TOUR', 700, 900, 54, (34, 32, 30), 'Anton.ttf')
        pop(c, pr(t, tb - 0.6, 0.4), 700, 860, shirt)
    person(c, 360, 1760, 0.6, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.4, -0.6), t=t, arm_r=(140, -220), arm_l=(-30, 220), blink=blinking(t))


def s_end(c, t):
    td = ph('the dream'); tc = ph('cash it in')
    paper_bg(c, t, skyline=False, ground=True)
    film_reel(c, 280, 900, 170, t)
    ferris(c, 770, 870, 230, t, 1.0)
    if t > td - 0.3: pop(c, pr(t, td - 0.3, 0.3), 280, 1170, lambda: (board(c, 60, 1110, 440, 100, (255, 255, 255)), neon_text(c, 'SELLS THE DREAM', 280, 1180, 44, (34, 32, 30))))
    if t > tc - 0.3: pop(c, pr(t, tc - 0.3, 0.3), 770, 1170, lambda: (board(c, 560, 1110, 440, 100, (255, 214, 40)), neon_text(c, 'CASHES IT IN', 770, 1180, 48, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('last year') - 0.15, s_compare), (ph('but why') - 0.15, s_why), (ph("it's like your favorite") - 0.15, s_band), (ph('so the movies') - 0.15, s_end)]
SHAKES = [(ph('almost ten'), 16, 0.45), (ph('more than double'), 12, 0.4), (ph('that photo'), 8, 0.3), (ph('cash it in'), 10, 0.35)]
TR = 0.32
