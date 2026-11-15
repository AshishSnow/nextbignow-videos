"""OopsMyBusiness LONG-FORM 16:9 — The Economics of Owning a Bus Business (US + Europe). Vintage comic + current editorial.
Run with NBN_ORIENT=land. Facts: ../scripts/vo_lines.py header + ../SOURCES.md. Photos: be/img/credits.json (Wikimedia Commons, comic-filtered)."""
import os
os.environ['NBN_ORIENT'] = 'land'
import sys, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

assert (W, H) == (1920, 1080)
D = os.path.join(HERE, 'be')
PK.IMG = os.path.join(D, 'img')
WT = load_words(D)
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT), maxc=34)
LN = json.load(open(os.path.join(D, 'lines.json')))          # id -> [start, end] (seconds, after tempo)
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))


def L(i): return LN[i][0]
def LE(i): return LN[i][1]


END = WT[-1][2] + 0.4
DURATION = END + 2.2
SEPIA = (240, 222, 186)
GRN = (60, 190, 110)
NAVY = (22, 36, 84)
LX = 110
SUBY = 968


def credit(c, key, a=1.0, col=(120, 100, 70)):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s . WIKIMEDIA COMMONS' % (cr['author'], cr['license'])).upper()[:80]
    c.save(); c.translate(46, 900); c.rotate(-90); mono(c, s, 0, 0, 15, col, a=a * 0.9); c.restore()


def photo(c, key, x, y, w, h, rot, k, t=0.0, zoom=1.06, fx=0.5, fy=0.5, cred=True, after=None):
    def dr(cc):
        cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * max(0, t), fx, fy)
        if after: after(cc)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)
    if cred and k > 0.2: credit(c, key, min(1, k))


def stat(c, x, y, w, h, rot, k, head, big, col, txtc=PAPER, bigsize=80, foot=None):
    """mini stat card: small typewriter label + one big number."""
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.22)
        cc.drawString(head, 24, 46, font('SpecialElite.ttf', 28), paint(PAPER if col in (CRED, CBLU, NAVY, GRN) else KINK))
        title(cc, big, 24, h - (54 if foot else 34), bigsize, txtc, 1.0, shadow=5)
        if foot: cc.drawString(foot, 24, h - 18, font('SpecialElite.ttf', 22), paint(PAPER if col in (CRED, CBLU, NAVY, GRN) else KINK))
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def tag(c, s, x, y, k, col=CYEL, size=30, rot=-2): caption(c, s, x, y, k, col=col, size=size, rot=rot)


def coach(c, x, y, s, k=1.0, col=CBLU, t=0.0, label='', lights=False, rot=0.0):
    """drawn comic motorcoach (no brand), front-left at (x, y=ground)."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); sc = s * (0.85 + 0.15 * eback(cl(k), 1.6)); c.scale(sc, sc)
    body = skia.Path(); body.moveTo(0, -40); body.lineTo(0, -300); body.quadTo(0, -330, 40, -335); body.lineTo(640, -335)
    body.quadTo(690, -330, 700, -280); body.lineTo(712, -40); body.close()
    c.save(); c.translate(12, 12); c.drawPath(body, paint(KINK)); c.restore()
    c.drawPath(body, paint(col)); dots(c, (0, -335, 712, 295), KINK, cell=14, rmax=3, grad=(0.5, 1.0), a=0.2)
    c.drawRect(R.MakeXYWH(0, -150, 712, 26), paint(PAPER))
    for i in range(6):
        wx = 40 + i * 100
        c.drawRect(R.MakeXYWH(wx, -300, 86, 110), paint((150, 200, 230) if not lights else (255, 226, 130)))
        c.drawRect(R.MakeXYWH(wx, -300, 86, 110), stroke(KINK, 5))
    c.drawRect(R.MakeXYWH(640, -300, 56, 180), paint((150, 200, 230))); c.drawRect(R.MakeXYWH(640, -300, 56, 180), stroke(KINK, 5))
    c.drawPath(body, stroke(KINK, 8))
    for wx in (130, 560):
        c.drawCircle(wx, -40, 58, paint(KINK)); c.drawCircle(wx, -40, 26, paint((190, 190, 190))); c.drawCircle(wx, -40, 26, stroke(KINK, 5))
    c.drawCircle(690, -80, 14, paint(CYEL if lights else PAPER)); c.drawCircle(690, -80, 14, stroke(KINK, 4))
    if label: c.drawString(label, 40, -88, font('SpecialElite.ttf', 40), paint(PAPER))
    c.restore()


def seats(c, x, y, n, filled, k, cols=10, cell=46, t=0.0):
    """seat map: n seats, `filled` coloured in."""
    if k <= 0: return
    for i in range(n):
        cx = x + (i % cols) * cell + (12 if (i % cols) >= cols // 2 else 0); cy = y + (i // cols) * cell
        kk = cl(k * 1.4 - i / n * 0.4)
        if kk <= 0: continue
        on = i < filled
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(cx, cy, cell - 8, cell - 8), 7, 7), paint(CRED if on else PAPER, kk))
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(cx, cy, cell - 8, cell - 8), 7, 7), stroke(KINK, 4, kk))


def meter(c, x, y, w, frac, k, col=CRED, label=''):
    if k <= 0: return
    c.drawRect(R.MakeXYWH(x + 8, y + 8, w, 54), paint(KINK, k)); c.drawRect(R.MakeXYWH(x, y, w, 54), paint(PAPER, k))
    c.drawRect(R.MakeXYWH(x, y, w * cl(frac) * eo(cl(k)), 54), paint(col, k)); c.drawRect(R.MakeXYWH(x, y, w, 54), stroke(KINK, 6, k))
    if label: c.drawString(label, x, y - 14, font('SpecialElite.ttf', 28), paint(KINK, k))


def waterfall(c, x, y, k_list, items, t):
    """P&L waterfall: items = [(label, value, col)], first is the total; bars drop down."""
    top = items[0][1]; sc = 360 / top; bw = 150; cur = top
    c.drawLine(x - 20, y + 380, x + len(items) * 190, y + 380, stroke(KINK, 5))
    for i, ((lab, v, col), k) in enumerate(zip(items, k_list)):
        if k <= 0: continue
        bx = x + i * 190
        if i == 0: y0, y1 = y + 380 - top * sc, y + 380
        elif lab.startswith('='): y0, y1 = y + 380 - v * sc, y + 380
        else: y0, y1 = y + 380 - cur * sc, y + 380 - (cur - v) * sc
        hh = (y1 - y0) * eo(cl(k))
        c.drawRect(R.MakeXYWH(bx + 8, y0 + 8, bw, hh), paint(KINK)); c.drawRect(R.MakeXYWH(bx, y0, bw, hh), paint(col)); c.drawRect(R.MakeXYWH(bx, y0, bw, hh), stroke(KINK, 5))
        c.drawString(lab.lstrip('='), bx, y + 420, font('SpecialElite.ttf', 24), paint(KINK))
        val = ('$%d' % v) if (i == 0 or lab.startswith('=')) else ('-$%d' % v)
        title(c, val, bx + bw / 2, y0 - 16, 40, KINK if i else CBLU, cl(k * 2), 'c', shadow=3)
        if i and not lab.startswith('='): cur -= v


def clock(c, x, y, r, k, t, hours=None, col=CYEL):
    if k <= 0: return
    sc = eback(cl(k), 2); c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawCircle(8, 8, r, paint(KINK)); c.drawCircle(0, 0, r, paint(col)); c.drawCircle(0, 0, r, stroke(KINK, 7))
    for i in range(12):
        a = i / 12 * math.tau; c.drawLine(math.sin(a) * r * 0.8, -math.cos(a) * r * 0.8, math.sin(a) * r * 0.92, -math.cos(a) * r * 0.92, stroke(KINK, 5))
    a = t * 2.2; c.drawLine(0, 0, math.sin(a) * r * 0.75, -math.cos(a) * r * 0.75, stroke(KINK, 7)); c.drawLine(0, 0, math.sin(a / 12) * r * 0.5, -math.cos(a / 12) * r * 0.5, stroke(KINK, 9))
    c.restore()


def doc(c, x, y, w, h, rot, k, head, lines_, stamp_=None, ks=0.0):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint((250, 246, 232)))
        cc.drawString(head, 30, 60, font('SpecialElite.ttf', 34), paint(KINK)); cc.drawLine(30, 76, w - 30, 76, stroke(KINK, 4))
        for i, s in enumerate(lines_): cc.drawString(s, 30, 130 + i * 48, font('SpecialElite.ttf', 26), paint(KINK))
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)
    if stamp_ and ks > 0:
        title(c, stamp_, x + w * 0.70, y + h * 1.02, 64, CRED, ks, 'c', shadow=4, rot=-12)


# ================================================================== scenes
def sc_hook(c, t, S):
    bg_flat(c, NAVY, (40, 60, 130))
    # frame 0 = thumbnail-ready: title + night coach
    photo(c, 'night', 900, 120, 920, 560, 1.5, 1.0, t, cred=t > 1)
    title(c, 'THE ECONOMICS OF', LX, 250, 84, PAPER, 1.0, rot=-1.5)
    title(c, 'OWNING A BUS', LX, 380, 120, CYEL, 1.0, rot=-2)
    title(c, 'BUSINESS', LX, 510, 120, CRED, 1.0, rot=-1)
    tag(c, 'USA + EUROPE . CASE STUDY', LX, 580, 1.0, col=PAPER, size=30)
    if t > L('h2') - 0.2:
        for i in range(3): title(c, 'Z', 1500 + i * 60, 760 - i * 60 - 20 * math.sin(t * 2 + i), 60 + i * 14, PAPER, pr(t, L('h2') + i * 0.25, 0.3))
    if t > L('h3') - 0.1: burst(c, 1300, 820, 150, 'THE OWNER?', pr(t, L('h3'), 0.35), size=40, rot=-6)
    if t > L('h4'): stat(c, LX, 680, 560, 230, -2, pr(t, L('h4'), 0.4), 'ONE COACH CAN COST', 'MORE THAN A HOUSE', CRED, bigsize=48)


def sc_question(c, t, S):
    bg_flat(c, CRED, (190, 20, 30))
    tag(c, 'THE QUESTION', LX, 120, pr(t, S['t0'], 0.3), col=PAPER)
    title(c, 'IS OWNING BUSES', LX, 330, 120, PAPER, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'A GOOD BUSINESS?', LX, 480, 130, CYEL, pr(t, S['t0'] + 0.4, 0.4), rot=-2)
    items = [('h6b', 'WHAT IT COSTS', CBLU), ('h6b', 'HOW IT EARNS', GRN), ('h6b', 'WHERE MONEY LEAKS', NAVY)]
    for i, (lid, s, col) in enumerate(items):
        stat(c, LX + i * 560, 600, 520, 200, (-2, 1.5, -1)[i], pr(t, L('h6b') + i * 0.7, 0.4), 'PART %d' % (i + 1), s, col, bigsize=46)
    if t > L('h7') - 0.2: burst(c, 1640, 300, 190, 'OWNS ~NO BUSES?!', pr(t, L('h7') + 0.6, 0.4), size=34, rot=8)


def sc_machine(c, t, S):
    paper(c, t)
    tag(c, 'PART 1 . THE MACHINE', LX, 110, pr(t, S['t0'], 0.3), col=CCYN)
    if t < L('a8') - 0.3:
        photo(c, 'interior', 980, 150, 830, 520, 1.5, pr(t, S['t0'] + 0.2, 0.5), t - S['t0'])
        title(c, 'A 50-SEAT COACH', LX, 300, 92, CBLU, pr(t, L('a2'), 0.4))
        stat(c, LX, 360, 520, 240, -2, pr(t, L('a3'), 0.4), 'BRAND NEW', '$500,000+', CRED, bigsize=96)
        if t > L('a4'): tag(c, 'ONE US OPERATOR: ~$600,000 PER BUS', LX + 20, 640, pr(t, L('a4'), 0.3), size=28)
        if t > L('a5') - 0.2:
            meter(c, 980, 760, 830, pr(t, L('a5'), 2.0), pr(t, L('a5') - 0.2, 0.3), CBLU, 'LOAN: OFTEN 5-7 YEARS')
        if t > L('a6'):
            for i in range(12):
                kk = pr(t, L('a6') + i * 0.12, 0.2)
                if kk > 0: title(c, '$', 990 + i * 68, 900, 54, CRED, kk, 'c', shadow=3)
            tag(c, 'A PAYMENT EVERY MONTH', 1200, 925, pr(t, L('a6') + 0.8, 0.3), col=CRED, size=26)
        if t > L('a7'): burst(c, 760, 860, 120, 'USED = CHEAPER', pr(t, L('a7'), 0.35), size=28, col=CCYN, txt=KINK, rot=-6)
        return
    title(c, 'NEARLY 50,000', LX, 330, 110, CBLU, pr(t, L('a8b') - 0.2, 0.4))
    title(c, 'MOTORCOACHES (US)', LX, 450, 76, CRED, pr(t, L('a8b') + 0.3, 0.4))
    stat(c, LX, 520, 560, 220, -2, pr(t, L('a9') - 0.1, 0.4), 'RUN BY FEWER THAN', '2,000 FIRMS', CRED, bigsize=72, foot='ABA FOUNDATION CENSUS, 2025')
    for i in range(18):
        kk = pr(t, L('a8') + i * 0.08, 0.3)
        coach(c, 1060 + (i % 6) * 125, 330 + (i // 6) * 170, 0.16, kk, (CBLU, CRED, GRN, CYEL)[i % 4])
    if t > L('a10'): tag(c, "MOST FIRMS RUN UNDER 10 COACHES", 1020, 860, pr(t, L('a10') + 0.8, 0.3), size=30)


def sc_earn(c, t, S):
    paper(c, t)
    tag(c, 'PART 2 . HOW A BUS MAKES MONEY', LX, 110, pr(t, S['t0'], 0.3), col=GRN)
    ways = [('b3', '1', 'CHARTER', CRED), ('b9', '2', 'OWN ROUTE', CBLU), ('b13', '3', 'CONTRACTS', GRN)]
    cur = max([i for i, (l, _, _, _) in enumerate(ways) if t >= L(l) - 0.2], default=-1)
    if cur < 0:
        title(c, 'HOW DOES A BUS', LX, 330, 110, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'MAKE MONEY?', LX, 470, 130, CRED, pr(t, S['t0'] + 0.6, 0.4), rot=-2)
        coach(c, 1050, 700, 0.95, pr(t, S['t0'] + 0.3, 0.5), CBLU, t)
        if t > L('b2'): burst(c, 1600, 300, 120, '3 WAYS', pr(t, L('b2'), 0.35), size=44, rot=8)
        return
    for i, (l, n, s, col) in enumerate(ways):      # tab rail (evolving)
        if i <= cur:
            on = i == cur
            stat(c, LX + i * 380, 170, 340, 120, (-1.5, 1, -1)[i], pr(t, L(l) - 0.2, 0.35), 'WAY ' + n, s, col if on else (200, 190, 170), txtc=PAPER if on else KINK, bigsize=46)
    if cur == 0:
        coach(c, 980, 820, 1.0, 1.0, CRED, t, 'CHARTER')
        for i, (s, lid) in enumerate((('SCHOOL TRIP', 'b4'), ('WEDDING', 'b4'), ('COMPANY RETREAT', 'b4'))):
            tag(c, s, 1150 + (i % 2) * 260, 360 + i * 70, pr(t, L(lid) + 0.6 * i, 0.3), col=(CYEL, CCYN, PAPER)[i], size=28, rot=(-3, 2, -1)[i])
        stat(c, LX, 360, 500, 220, -2, pr(t, L('b5'), 0.4), 'PRICING GUIDES', '$100+ / HOUR', CBLU, bigsize=64)
        stat(c, LX, 610, 500, 220, 1.5, pr(t, L('b6'), 0.4), 'A FULL DAY', '$1,000+', CRED, bigsize=80)
        if t > L('b7') - 0.1: burst(c, 760, 880, 110, 'UPSIDE', pr(t, L('b7'), 0.35), size=34, col=GRN, txt=PAPER)
        if t > L('b8') - 0.1: tag(c, 'CATCH: FIND THE NEXT CUSTOMER', 980, 900, pr(t, L('b8'), 0.3), col=CRED, size=30)
    elif cur == 1:
        title(c, 'CITY A  ----  CITY B', LX, 400, 64, KINK, pr(t, L('b10') - 0.2, 0.4))
        tag(c, 'TIMETABLE + SELL SEAT BY SEAT', LX, 440, pr(t, L('b10') + 0.6, 0.3), size=28)
        half = t >= L('b12') - 0.2
        seats(c, 1000, 380, 50, 25 if half else int(50 * pr(t, L('b11') - 0.3, 1.0)), 1.0, cell=74)
        title(c, 'HALF EMPTY...' if half else 'FULL = GREAT MONEY', 1000, 360, 54, CRED if half else GRN, pr(t, L('b11') - 0.3, 0.4))
        if half: stat(c, LX, 560, 640, 240, -2, pr(t, L('b12'), 0.4), 'YOU STILL PAY FOR', 'THE WHOLE TRIP', CRED, bigsize=56)
        if t > L('b12b'): burst(c, 560, 900, 110, 'FUEL!', pr(t, L('b12b'), 0.35), size=40, rot=-6)
    else:
        for i, s in enumerate(('UNIVERSITY SHUTTLE', 'AIRPORT RUN', 'WORKER COMMUTE')):
            tag(c, s, LX + i * 40, 380 + i * 80, pr(t, L('b14') + 0.7 * i, 0.3), col=(CYEL, CCYN, PAPER)[i], size=30, rot=(-2, 1.5, -1)[i])
        clock(c, 1240, 560, 170, pr(t, L('b15') - 0.2, 0.4), t)
        if t > L('b15'): title(c, 'PAID BY HOUR OR MILE', 1240, 830, 52, KINK, pr(t, L('b15') + 0.4, 0.4), 'c')
        if t > L('b16'): stat(c, LX, 640, 600, 220, -2, pr(t, L('b16'), 0.4), 'LESS UPSIDE, LESS RISK', 'STEADY MONEY', GRN, bigsize=60)


def sc_germany(c, t, S):
    paper(c, t, tint=SEPIA)
    tag(c, 'PART 3 . THE FOURTH WAY', LX, 110, pr(t, S['t0'], 0.3), col=CYEL)
    if t < L('c2') - 0.2:
        title(c, 'LET SOMEONE ELSE', LX, 380, 110, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'SELL YOUR SEATS', LX, 520, 120, CRED, pr(t, S['t0'] + 0.7, 0.4), rot=-2)
        return
    if t < L('c5') - 0.3:
        photo(c, 'berlin', 960, 150, 860, 500, 1.5, pr(t, L('c2') - 0.2, 0.5), t - L('c2'))
        title(c, 'GERMANY, 2013', LX, 300, 100, CBLU, pr(t, L('c2'), 0.4))
        if t > L('c3') - 0.2: doc(c, LX, 360, 640, 300, -2, pr(t, L('c3'), 0.4), 'LONG-DISTANCE BUSES', ['LIMITED, TO PROTECT', 'THE RAILWAY', '...UNTIL 2013'], 'CHANGED!', pr(t, L('c4'), 0.3))
        if t > L('c4b') - 0.2:
            def dr(cc):
                cc.drawRect(R.MakeWH(860, 300), paint(PAPER))
                bars(cc, 70, 30, 680, 200, [('BEFORE', 1, '', CBLU), ('1 YEAR LATER', 2.9, 'X3', CRED)], pr(t, L('c4b'), 1.0), 3.9)
            panel(c, 960, 690, 860, 300, rot=1.2, k=pr(t, L('c4b') - 0.2, 0.4), draw=dr)
            tag(c, 'INTERCITY BUS ROUTES', 1000, 690, pr(t, L('c4b') + 0.4, 0.3), size=24)
        if t > L('c4c') - 0.2: burst(c, 760, 860, 130, '~HALF THE TRAIN FARE', pr(t, L('c4c'), 0.35), size=24, rot=-6)
        if t > L('c4d') - 0.2:
            title(c, 'MERGED.', 1300, 420, 100, CRED, pr(t, L('c4d') + 0.3, 0.35), 'c', rot=-10)
            title(c, 'BOUGHT.', 1560, 520, 100, CBLU, pr(t, L('c4d') + 0.9, 0.35), 'c', rot=8)
        return
    if t < L('c10') - 0.3:
        title(c, 'FLIXBUS', LX, 300, 150, GRN, pr(t, L('c5'), 0.4), rot=-2)
        if t > L('c5b') - 0.2: burst(c, 820, 230, 130, 'BUSES OWNED: ~0', pr(t, L('c5b'), 0.35), size=28, rot=6)
        # split diagram
        def left(cc):
            cc.drawRect(R.MakeWH(760, 480), paint(PAPER)); title(cc, 'LOCAL BUS COMPANY', 30, 70, 46, CBLU, 1.0, shadow=3)
            for i, s in enumerate(('OWNS THE COACHES', 'EMPLOYS THE DRIVERS', 'DRIVES THE ROUTE')): cc.drawString('+ ' + s, 30, 150 + i * 60, font('SpecialElite.ttf', 32), paint(KINK))
            coach(cc, 200, 450, 0.5, 1.0, CBLU, t)
        def right(cc):
            cc.drawRect(R.MakeWH(760, 480), paint(PAPER)); title(cc, 'FLIX', 30, 70, 46, GRN, 1.0, shadow=3)
            for i, s in enumerate(('PLANS THE ROUTES', 'SETS THE PRICES', 'RUNS THE APP', 'SELLS THE TICKETS')):
                if t > L('c7') + i * 0.6 - 0.2: cc.drawString('+ ' + s, 30, 150 + i * 60, font('SpecialElite.ttf', 32), paint(KINK))
        panel(c, LX, 380, 760, 480, rot=-1.2, k=pr(t, L('c6') - 0.2, 0.4), draw=left)
        panel(c, 1000, 380, 760, 480, rot=1.2, k=pr(t, L('c7') - 0.2, 0.4), draw=right)
        if t > L('c8') - 0.2: burst(c, 1660, 260, 140, '~25% CUT', pr(t, L('c8'), 0.35), size=36, rot=-8, col=CRED, txt=CYEL)
        if t > L('c9') - 0.2: tag(c, 'LIKE UBER, BUT FOR INTERCITY BUSES', 520, 900, pr(t, L('c9'), 0.3), size=32)
        return
    if t < L('c12') - 0.3:
        title(c, 'WIN-WIN?', LX, 300, 130, CBLU, pr(t, L('c10') - 0.3, 0.4))
        stat(c, LX, 400, 760, 240, -2, pr(t, L('c10'), 0.4), 'BUS OWNER GETS', 'SEATS SOLD FOR THEM', CBLU, bigsize=56, foot='NO MARKETING OF THEIR OWN')
        stat(c, 1000, 420, 760, 240, 1.5, pr(t, L('c11'), 0.4), 'FLIX GETS', 'FAST GROWTH', GRN, bigsize=80, foot='WITHOUT BUYING WHOLE FLEETS')
        return
    tag(c, 'THE GIANT TODAY', LX, 180, pr(t, L('c12') - 0.3, 0.3), col=CCYN)
    stat(c, LX, 260, 520, 230, -2, pr(t, L('c12'), 0.4), '2021: FLIX BUYS', 'GREYHOUND', CBLU, bigsize=64, foot='~1,300 VEHICLES')
    stat(c, 680, 260, 520, 230, 1.5, pr(t, L('c13'), 0.4), 'PASSENGERS, 2023', '81 MILLION', CRED, bigsize=64)
    stat(c, 1250, 260, 560, 230, -1.5, pr(t, L('c14'), 0.4), 'REVENUE, 2023', 'EUR 2BN+', GRN, bigsize=72)
    if t > L('c15') - 0.2:
        meter(c, LX, 720, 1700, 0.052, pr(t, L('c15'), 0.4), CRED, 'ADJUSTED PROFIT MARGIN (EBITDA): ~5%')
        title(c, '~5 CENTS PER EURO', LX, 630, 52, CRED, pr(t, L('c15') + 0.8, 0.4))
    if t > L('c16') - 0.2: tag(c, 'BEFORE INTEREST, TAXES, WEAR AND TEAR', LX, 820, pr(t, L('c16'), 0.3), size=28)
    if t > L('c17') - 0.2: burst(c, 1620, 820, 120, 'THIN!', pr(t, L('c17'), 0.35), size=44, rot=8)


def sc_money(c, t, S):
    paper(c, t)
    tag(c, 'PART 4 . WHERE THE MONEY GOES', LX, 110, pr(t, S['t0'], 0.3), col=CRED)
    if t < L('d2') - 0.3:
        title(c, 'FOLLOW THE MONEY', LX, 420, 120, CBLU, pr(t, S['t0'] + 0.1, 0.4)); coach(c, 1100, 860, 0.9, pr(t, S['t0'] + 0.3, 0.4), CRED, t, lights=True)
        for i in range(5): title(c, '$', 1000 + i * 120, 470 - 40 * ((t * 1.5 + i * 0.3) % 1), 70, GRN, pr(t, S['t0'] + 0.5 + i * 0.15, 0.3), 'c')
        return
    if t < L('d7') - 0.3:
        title(c, 'BILL #1: FUEL', LX, 290, 110, CRED, pr(t, L('d2') - 0.2, 0.4))
        photo(c, 'diesel', 1060, 130, 760, 470, 1.5, pr(t, S['t0'] + 0.3, 0.5), t - S['t0'])
        lines_ = [('d3', 'SAY ~6 MILES PER GALLON'), ('d4', '500-MILE RUN: 80+ GALLONS'), ('d5', 'US DIESEL: $6+/GALLON (EIA, NOV 2026)')]
        for i, (lid, s) in enumerate(lines_): tag(c, s, LX, 360 + i * 90, pr(t, L(lid), 0.3), col=(CYEL, CCYN, PAPER)[i], size=30, rot=(-1.5, 1, -1)[i])
        if t > L('d6') - 0.2: stat(c, LX, 660, 620, 250, -2, pr(t, L('d6'), 0.4), 'FUEL, ONE WAY', '~$500', CRED, bigsize=110)
        return
    if t < L('d14') - 0.3:
        title(c, 'BILL #2: THE DRIVER', LX, 290, 92, CBLU, pr(t, L('d7') - 0.2, 0.4))
        photo(c, 'driver', 1060, 130, 760, 470, -1.5, pr(t, L('d7'), 0.5), t - L('d7'))
        stat(c, LX, 340, 620, 240, -2, pr(t, L('d8'), 0.4), 'MEDIAN BUS DRIVER PAY (US)', '~$59,050/YR', CBLU, bigsize=70, foot='BLS, MAY 2025')
        if t > L('d10') - 0.2: burst(c, 900, 520, 130, '1 IN 5 MISSING', pr(t, L('d10'), 0.35), size=28, rot=6)
        if t > L('d11') - 0.2:
            title(c, 'BILL #3: INSURANCE', LX, 720, 80, NAVY, pr(t, L('d11'), 0.4))
            stat(c, 1060, 660, 760, 250, 1.5, pr(t, L('d13') - 0.1, 0.4), 'FEDERAL MINIMUM, 16+ SEATS', '$5,000,000', CRED, bigsize=96)
        return
    if t < L('m1') - 0.3:
        title(c, 'AND THEN...', LX, 290, 110, KINK, pr(t, L('d14') - 0.2, 0.4))
        for i, s in enumerate(('TIRES', 'BRAKES', 'REPAIRS', 'PARKING', 'LOAN')):
            burst(c, 260 + i * 330, 600 + (i % 2) * 120, 120, s, pr(t, L('d14') + 0.45 * i, 0.3), size=30, col=(CYEL, CCYN, PAPER, CYEL, CRED)[i], txt=KINK if i < 4 else CYEL, rot=(-6, 4, -3, 7, -5)[i])
        return
    if t < L('d15') - 0.3:     # worked example
        title(c, 'A ROUGH, MADE-UP EXAMPLE', LX, 270, 70, CBLU, pr(t, L('m1'), 0.4))
        tag(c, '50 SEATS x $40, ONE TRIP', LX, 300, pr(t, L('m2'), 0.3), size=28)
        half = t >= L('m7') + 0.6
        tot = 1000 if half else 2000
        items = [('TICKETS', tot, CBLU), ('PLATFORM 25%', tot // 4, CYEL), ('FUEL', 500, CRED), ('DRIVER', 300, CCYN), ('=LEFT', max(0, tot - tot // 4 - 800), GRN)]
        ks = [pr(t, L('m3'), 0.5), pr(t, L('m4'), 0.5), pr(t, L('m5'), 0.5), pr(t, L('m5') + 1.2, 0.5), pr(t, L('m6'), 0.5)]
        if half: ks = [pr(t, L('m7') + 0.6 + 0.3 * i, 0.4) for i in range(5)]
        waterfall(c, 260, 400, ks, items, t)
        seats(c, 1300, 460, 50, 25 if half else 50, pr(t, L('m2'), 0.8), cols=10, cell=50)
        tag(c, 'HALF FULL' if half else 'EVERY SEAT SOLD', 1300, 400, pr(t, L('m2'), 0.3), col=CRED if half else GRN, size=28)
        if t > L('m6'): tag(c, '...BEFORE LOAN, INSURANCE, REPAIRS', 1240, 800, pr(t, L('m6') + 0.5, 0.3), size=26)
        if half and t > L('m8'): burst(c, 1480, 880, 110, 'GONE.', pr(t, L('m8') + 1.2, 0.35), size=44, rot=-6)
        if t > L('m9') - 0.2: title(c, 'EMPTY SEATS = LOST MONEY', W / 2, 890, 56, CRED, pr(t, L('m9'), 0.4), 'c')
        return
    photo(c, 'depot', 960, 130, 860, 520, 1.5, pr(t, L('d15') - 0.2, 0.5), t - L('d15'), zoom=1.35, fy=0.85)
    title(c, 'THE SCARY PART', LX, 300, 100, CRED, pr(t, L('d15'), 0.4))
    tag(c, 'A PARKED BUS STILL COSTS MONEY', LX, 340, pr(t, L('d15') + 1.0, 0.3), size=30)
    for i, s in enumerate(('LOAN', 'INSURANCE', 'PARKING')):
        meter(c, LX, 500 + i * 110, 700, (t - L('d16')) * 0.12 + 0.1 * i, pr(t, L('d16') + 0.4 * i, 0.3), (CRED, CBLU, NAVY)[i], s + ' . STILL RUNNING')
    if t > L('d17') - 0.2: stat(c, 960, 700, 860, 210, 1.5, pr(t, L('d17'), 0.4), 'RULE #1 OF THE BUSINESS', 'KEEP IT MOVING', GRN, bigsize=76)


def sc_rules(c, t, S):
    paper(c, t)
    tag(c, 'PART 5 . THE PAPERWORK', LX, 110, pr(t, S['t0'], 0.3), col=CYEL)
    if t < L('e5') - 0.3:
        title(c, "YOU CAN'T JUST DRIVE.", LX, 290, 92, CRED, pr(t, S['t0'] + 0.2, 0.4))
        doc(c, LX, 360, 560, 300, -2, pr(t, L('e2'), 0.4), 'USA', ['FEDERAL OPERATING', 'AUTHORITY TO CROSS', 'STATE LINES'], 'REQUIRED', pr(t, L('e2') + 1.2, 0.3))
        doc(c, 720, 380, 560, 300, 1.5, pr(t, L('e3'), 0.4), 'DRIVER', ['COMMERCIAL LICENSE', '+ PASSENGER (P)', 'ENDORSEMENT'], None)
        photo(c, 'interior', 1330, 360, 500, 330, -1.5, pr(t, L('e4'), 0.4), t - L('e4'))
        if t > L('e4'): tag(c, 'NEW COACHES: SEAT BELTS SINCE LATE 2016', 980, 760, pr(t, L('e4') + 0.6, 0.3), size=28)
        return
    title(c, 'EUROPE: OWN RULEBOOK', LX, 290, 92, CBLU, pr(t, L('e5') - 0.2, 0.4))
    clock(c, 330, 600, 170, pr(t, L('e6') - 0.1, 0.4), t)
    stat(c, 560, 420, 520, 230, -2, pr(t, L('e6'), 0.4), 'DRIVING, USUALLY', '9 HRS/DAY', CBLU, bigsize=80)
    stat(c, 560, 680, 520, 230, 1.5, pr(t, L('e7'), 0.4), 'AFTER 4.5 HOURS', '45-MIN BREAK', CRED, bigsize=64)
    photo(c, 'tacho', 1150, 420, 680, 420, 1.5, pr(t, L('e8') - 0.2, 0.4), t - L('e8'))
    if t > L('e8'): tag(c, 'TACHOGRAPH = THE RECORDER', 1180, 870, pr(t, L('e8') + 0.4, 0.3), size=28)
    if t > L('e9') - 0.2: burst(c, 300, 880, 110, 'SAFE', pr(t, L('e9') + 1.0, 0.35), size=40, col=GRN, txt=PAPER)


def sc_verdict(c, t, S):
    bg_flat(c, CYEL, (230, 170, 20))
    tag(c, 'PART 6 . THE VERDICT', LX, 110, pr(t, S['t0'], 0.3), col=PAPER)
    title(c, 'GOOD BUSINESS?', W / 2, 290, 120, CRED, pr(t, S['t0'] + 0.1, 0.4), 'c')
    def up(cc):
        cc.drawRect(R.MakeWH(760, 500), paint(PAPER)); title(cc, 'THE UPSIDE', 30, 80, 60, GRN, 1.0, shadow=3)
        for i, (lid, s) in enumerate((('f2', 'PEOPLE ALWAYS TRAVEL'), ('f2', 'ONE BUS MOVES MANY'), ('f3', 'OFTEN CHEAPER THAN FLYING'))):
            if t > L(lid) + i * 0.8 - 0.2: cc.drawString('+ ' + s, 30, 170 + i * 80, font('SpecialElite.ttf', 36), paint(KINK))
    def dn(cc):
        cc.drawRect(R.MakeWH(760, 500), paint(PAPER)); title(cc, 'THE CATCH', 30, 80, 60, CRED, 1.0, shadow=3)
        for i, (lid, s) in enumerate((('f4', 'BIG MONEY UP FRONT'), ('f4', 'THIN MARGINS'), ('f4', 'EMPTY MONTHS HURT'), ('f5', 'PRICE WARS'))):
            if t > L(lid) + i * 0.8 - 0.2: cc.drawString('- ' + s, 30, 170 + i * 80, font('SpecialElite.ttf', 36), paint(KINK))
    panel(c, LX, 360, 760, 500, rot=-1.5, k=pr(t, L('f2') - 0.2, 0.4), draw=up)
    panel(c, 1040, 360, 760, 500, rot=1.5, k=pr(t, L('f4') - 0.2, 0.4), draw=dn)
    if t > L('f6') - 0.2:
        c.drawRect(R.MakeWH(W, H), paint(KINK, 0.55 * pr(t, L('f6') - 0.2, 0.3)))
        title(c, 'WINNERS KEEP', W / 2, 470, 130, PAPER, pr(t, L('f6') + 0.6, 0.4), 'c')
        title(c, 'EVERY BUS BUSY.', W / 2, 640, 140, CYEL, pr(t, L('f7'), 0.4), 'c', rot=-2)


def sc_start(c, t, S):
    paper(c, t)
    tag(c, 'PART 7 . HOW YOU WOULD START', LX, 110, pr(t, S['t0'], 0.3), col=CCYN)
    if t < L('g2') - 0.3:
        title(c, 'HOW WOULD YOU', W / 2, 430, 120, CBLU, pr(t, S['t0'] + 0.1, 0.4), 'c'); title(c, 'START?', W / 2, 600, 160, CRED, pr(t, S['t0'] + 0.5, 0.4), 'c', rot=-2)
        burst(c, 1550, 760, 120, '3 MOVES', pr(t, S['t0'] + 1.5, 0.35), size=40, rot=8); return
    items = [('g2', '1', 'ONE GOOD USED COACH', 'NOT A SHINY NEW FLEET', CRED), ('g3', '2', 'LOCK IN CONTRACTS FIRST', 'STEADY HOURS PAY THE LOAN', CBLU),
             ('g4', '3', 'PLUG INTO A NETWORK', "DON'T BUILD YOUR OWN APP", GRN)]
    for i, (lid, n, a1, a2, col) in enumerate(items):
        def dr(cc, n=n, a1=a1, a2=a2, col=col):
            cc.drawRect(R.MakeWH(1500, 180), paint(PAPER)); cc.drawRect(R.MakeWH(180, 180), paint(col)); dots(cc, (0, 0, 180, 180), KINK, cell=14, rmax=3, a=0.3)
            title(cc, n, 90, 130, 130, PAPER, 1.0, 'c', shadow=6); title(cc, a1, 220, 85, 64, KINK, 1.0, shadow=0, outline=0.01); title(cc, a2, 220, 155, 50, col, 1.0, shadow=4)
        panel(c, 210, 200 + i * 220, 1500, 180, rot=(-1, 0.8, -0.6)[i], k=pr(t, L(lid) - 0.2, 0.4), draw=dr)
    if t > L('g5') - 0.2: burst(c, 1700, 880, 120, '$ PER MILE?', pr(t, L('g5'), 0.35), size=32, rot=8)
    if t > L('g5') - 0.2: tag(c, 'KNOW YOUR COST PER MILE FIRST', 520, 880, pr(t, L('g5') + 0.3, 0.3), col=CYEL, size=30)


def sc_end(c, t, S):
    if t < L('z3') - 0.3:
        bg_flat(c, NAVY, (40, 60, 130))
        photo(c, 'night', 900, 140, 920, 560, -1.5, pr(t, S['t0'], 0.5), t - S['t0'])
        title(c, 'WHILE YOU DREAM,', LX, 360, 90, PAPER, pr(t, L('z2') - 0.3, 0.4))
        title(c, 'THEY DO MATH.', LX, 500, 120, CYEL, pr(t, L('z2') + 0.5, 0.4), rot=-2)
        for i in range(3): title(c, 'Z', 1560 + i * 60, 780 - i * 60 - 20 * math.sin(t * 2 + i), 60 + i * 14, PAPER, pr(t, S['t0'] + 0.5 + i * 0.25, 0.3))
        return
    bg_flat(c, CRED, (190, 20, 30))
    tag(c, 'YOUR TURN', LX, 120, pr(t, L('z3') - 0.3, 0.3), col=PAPER)
    title(c, 'WOULD YOU RATHER OWN...', W / 2, 330, 96, PAPER, pr(t, L('z4') - 0.2, 0.4), 'c')
    burst(c, 620, 640, 220, 'THE BUSES', pr(t, L('z4') + 1.4, 0.35), size=56, col=CYEL, txt=CBLU, rot=-6)
    title(c, 'OR', W / 2, 670, 90, PAPER, pr(t, L('z4') + 1.8, 0.3), 'c')
    burst(c, 1300, 640, 220, 'THE APP?', pr(t, L('z4') + 2.1, 0.35), size=60, col=PAPER, txt=GRN, rot=6)
    tag(c, 'TELL ME IN THE COMMENTS', W / 2 - 230, 880, pr(t, L('z4') + 2.6, 0.3), col=CYEL, size=32)
    if t > END: c.drawCircle(W / 2, H / 2, 2200 * eio(pr(t, END, 0.9)), paint(KINK))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY, size=36)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='question', t0=L('h5') - 0.2, fn=with_subs(sc_question), tin='flash'),
    dict(k='machine', t0=L('a1') - 0.2, fn=with_subs(sc_machine), tin='whip'),
    dict(k='earn', t0=L('b1') - 0.2, fn=with_subs(sc_earn), tin='wipe'),
    dict(k='germany', t0=L('c1') - 0.2, fn=with_subs(sc_germany), tin='zoom', col=SEPIA),
    dict(k='money', t0=L('d1') - 0.2, fn=with_subs(sc_money), tin='whip'),
    dict(k='rules', t0=L('e1') - 0.2, fn=with_subs(sc_rules), tin='wipe'),
    dict(k='verdict', t0=L('f1') - 0.2, fn=with_subs(sc_verdict), tin='flash'),
    dict(k='start', t0=L('g1') - 0.2, fn=with_subs(sc_start), tin='whip'),
    dict(k='end', t0=L('z1') - 0.2, fn=with_subs(sc_end), tin='zoom'),
]
CHAPTERS = [('Intro', 'hook'), ('What a coach really costs', 'machine'), ('3 ways a bus makes money', 'earn'), ('The FlixBus model', 'germany'),
            ('Where the money goes', 'money'), ('The rules (US + Europe)', 'rules'), ('The verdict', 'verdict'), ('How you would start', 'start')]
EP = Episode(D, SCENES, DURATION, END)
for lid, a in (('h4', 6), ('a3', 8), ('c5b', 8), ('d6', 8), ('d13', 8), ('m8', 10), ('f7', 8)): EP.shk(L(lid) + 0.4, a, 0.3)
EP.flash(L('c4d') + 0.3, 0.3)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'chapters':
        T = {S['k']: S['t0'] for S in SCENES}
        for name, k in CHAPTERS:
            s = int(max(0, T[k])); print('%d:%02d %s' % (s // 60, s % 60, name))
    else:
        EP.main(sys.argv)
