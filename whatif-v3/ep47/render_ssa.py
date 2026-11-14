"""NextBigNow ep 47: What happens if Social Security runs dry?
Facts: 2026 Trustees Report (9 Jun 2026) via Fortune/CRFB - OASI fund depleted Q4 2032, then 78% payable (22% cut); combined OASDI 2034
(17% cut); 75-yr shortfall 4.42% of payroll; fix now = +4.25 pts payroll tax (~34%) or 25% across-the-board benefit cut; CRFB: typical
couple retiring 2033 loses ~$18,400/yr. SSA 2025 TR: 5.1 workers per beneficiary in 1960, 2.7 in 2025, 2.3 by 2035. SSA history:
OASI fund could have run out as early as Aug 1983; 1983 Amendments signed 20 Apr 1983 (retirement age 65->67 phased, benefit taxation,
payroll tax schedule accelerated).
Photos (Wikimedia Commons): US Capitol dome - Diliff CC BY 2.5; Capitol at dusk - Martin Falbisoner CC BY-SA 3.0; NARA poster - public
domain; 1930s Treasury check machine - Harris & Ewing, public domain (Library of Congress)."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from edkit import _grain
import photokit as PK
from photokit import img, cover, cutout, photo_card, credit, shade, kicker
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('SS_DIR', 'ssa'))
PK.IMG = os.path.join(HERE, 'ssa', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j].strip("'") or TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
HY = 540
PAPERG = (236, 244, 232)


def check(c, cx, cy, s, k_cut=0.0, rot=-3, amount='$2,000', t=0.0):
    """illustrative monthly benefit check; k_cut snips off the right 22% and drops it."""
    w, h = 860, 400
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    cut_x = -w / 2 + w * 0.78
    def body(cc, x0, x1):
        cc.save(); cc.clipRect(R.MakeLTRB(x0, -h / 2 - 40, x1, h / 2 + 40))
        cc.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2 + 6, -h / 2 + 18, w, h), 18, 18), paint((0, 0, 0), 0.22, blur=18))
        cc.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-w / 2, -h / 2, w, h), 18, 18), paint(PAPERG))
        for i in range(14): cc.drawLine(-w / 2 + 20, -h / 2 + 30 + i * 26, w / 2 - 20, -h / 2 + 30 + i * 26, stroke((210, 228, 205), 2))
        cc.drawRect(R.MakeXYWH(-w / 2, -h / 2, w, 70), paint((30, 110, 70)))
        mono(cc, 'MONTHLY BENEFIT', -w / 2 + 30, -h / 2 + 46, 26, PAPER)
        mono(cc, 'ILLUSTRATIVE', w / 2 - 230, -h / 2 + 46, 22, (190, 230, 200))
        mono(cc, 'PAY TO THE ORDER OF', -w / 2 + 30, -h / 2 + 130, 20, (60, 90, 70))
        text(cc, 'A U.S. Retiree', -w / 2 + 30, -h / 2 + 195, 'sb', 48, INK)
        cc.drawLine(-w / 2 + 30, -h / 2 + 215, w / 2 - 260, -h / 2 + 215, stroke(INK, 2))
        cc.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(w / 2 - 300, -h / 2 + 110, 260, 100), 10, 10), stroke(INK, 3))
        text(cc, amount, w / 2 - 170, -h / 2 + 180, 'blk', 58, INK, 'c')
        mono(cc, 'SOCIAL SECURITY · RETIREMENT', -w / 2 + 30, h / 2 - 40, 22, (60, 90, 70))
        cc.restore()
    body(c, -w / 2 - 40, cut_x)
    k = cl(k_cut)
    c.save(); c.translate(cut_x, 0)
    if k > 0:
        c.translate(30 * eo(k), 900 * k * k); c.rotate(25 * eo(k))
    c.translate(-cut_x, 0)
    body(c, cut_x, w / 2 + 40)
    c.restore()
    if k_cut > 0:
        for i in range(12):
            y = -h / 2 + i * (h / 12)
            c.drawLine(cut_x, y + 6, cut_x, y + 20, stroke(RED, 6, cl(1 - k * 2)))
    else:
        for i in range(12):
            y = -h / 2 + i * (h / 12)
            c.drawLine(cut_x, y + 6, cut_x, y + 20, stroke(RED, 5))
    c.restore()


def person(c, x, y, s, col, a=1.0):
    c.drawCircle(x, y - 70 * s, 22 * s, paint(col, a))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(x - 28 * s, y - 42 * s, 56 * s, 80 * s), 22 * s, 22 * s), paint(col, a))


def tank(c, x, y, w, h, level, col=GREEN):
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(x, y, w, h), 24, 24), paint((255, 255, 255)))
    lh = (h - 16) * cl(level)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(R.MakeXYWH(x + 8, y + 8, w - 16, h - 16), 18, 18))
    c.drawRect(R.MakeXYWH(x + 8, y + h - 8 - lh, w - 16, lh), paint(col))
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(x, y, w, h), 24, 24), stroke(INK, 5))


# ================================================================== scenes
def sc_hook(c, t, S):
    tp = ph('pay cut'); tr = ph('runs out of money'); tq = ph('so what happens')
    if t < tq - 0.15:
        bg_cream(c, t)
        c.drawCircle(540, 1370, 370, paint(RED))
        pill(c, 540, 330, 'SOCIAL SECURITY', 1.0, col=INK, size=40)
        mono(c, 'LATE 2032 · USA', LX + 2, 440, 28, GREY)
        n = 22 if t > 0.05 else 22
        text(c, '-22%', 60, 800, 'blk', 330, INK, track=-0.06)
        text(c, 'for every retiree.', LX, 900, 'blk', 74, INK)
        if t > ph('automatically') - 0.2:
            text(c, 'Automatically.', LX, 985, 'blk', 74, RED, a=pr(t, ph('automatically') - 0.2, 0.2))
        check(c, 540, 1330, 0.95 + 0.02 * math.sin(t * 2), pr(t, tp, 1.0), t=t)
        if t > tr - 0.3:
            pill(c, 540, 1470, 'BECAUSE A FUND RUNS OUT OF MONEY', pr(t, tr - 0.3, 0.3), col=INK, size=32)
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What if Social', 'Security', 'runs dry?'], LX, HY, 132, t, tq - 0.05, col=PAPER, hl=(2, ('', 'runs dry?')), hl_col=INK)
    k = pr(t, tq + 0.2, 0.7)
    cutout(c, 'S6_dome_cut.png', 540, 1520, 600, k)
    credit(c, 'PHOTO: DILIFF · CC BY 2.5', col=(255, 210, 210), a=k)


def sc_how(c, t, S):
    tl = ph("whatever's left over"); tg = ph('kept growing'); ts = ph("now it's shrinking")
    bg_cream(c, t)
    kicker(c, 'HOW IT WORKS', t, S['t0'] + 0.1)
    headline(c, ['Your paycheck', "pays today's", 'retirees.'], LX, HY, 112, t, S['t0'] + 0.2, hl=(2, ('', 'retirees.')), hl_col=YEL)
    k = pr(t, S['t0'] + 0.5, 0.5)
    def dr(cc):
        cover(cc, img('S4_archive.jpg'), 14, 14, 392, 452, 1.15, 0.55, 0.5)
    card(c, 290, 1150, 420, 480, -3, k, dr, rad=8)
    mono(c, 'CHECKS GOING OUT, 1930s', 290, 1430, 20, GREY, 'c', a=k)
    if t > tl - 0.3:
        kk = pr(t, tl - 0.3, 0.4)
        mono(c, 'TRUST FUND', 790, 900, 24, INK, 'c', a=kk)
        lv = 0.25 + 0.6 * eo(pr(t, tg - 0.3, 1.0)) - 0.62 * eio(pr(t, ts, 1.4))
        tank(c, 680, 930, 220, 440, lv, GREEN if t < ts else RED)
        if t > ts:
            pill(c, 790, 1430, 'SHRINKING', pr(t, ts, 0.3), col=RED, size=34)
    credit(c, 'PHOTO: HARRIS & EWING · LIBRARY OF CONGRESS · PUBLIC DOMAIN')


def sc_report(c, t, S):
    td = ph('runs dry in late'); ts = ph('one year sooner'); t78 = ph('seventy eight cents'); tc = ph('typical couple')
    bg_cream(c, t)
    kicker(c, "TRUSTEES' REPORT · JUNE 2026", t, S['t0'] + 0.1)
    if t < t78 - 0.4:
        headline(c, ['Runs dry:', 'late 2032.'], LX, HY, 150, t, td - 0.3, hl=(1, ('late ', '2032.')), hl_col=RED_L)
        def dr(cc):
            mono(cc, 'RETIREMENT FUND · PROJECTED EMPTY', 44, 64, 20, GREY)
            for i, (yr, lab, col) in enumerate((('2033', 'LAST YEAR SAID', LIGHT), ('2032', 'NOW SAYS', RED))):
                kk = pr(t, (td if i == 0 else ts) - 0.1, 0.4)
                x = 60 + i * 400
                text(cc, yr, x, 220, 'blk', 150, col if i else GREY, a=eo(kk))
                mono(cc, lab, x + 4, 270, 22, INK, a=kk)
        card(c, 540, 1130, 860, 380, -1.5, pr(t, td, 0.5), dr)
        return
    if t < tc - 0.4:
        headline(c, ['78¢ on', 'every $1.'], LX, HY, 150, t, t78 - 0.4, hl=(0, ('', '78¢')), hl_col=YEL)
        k = pr(t, t78, 1.2)
        for i in range(100):
            col_, row = i % 10, i // 10
            x = 220 + col_ * 72; y = 900 + row * 60
            paid = i < 78
            on = cl(k * 100 - i)
            c.drawCircle(x, y, 24, paint((GREEN if paid else RED) if on > 0 else LIGHT, 1.0 if paid or on <= 0 else 0.9))
        mono(c, 'GREEN = PAID   RED = CUT', 540, 1480, 22, GREY, 'c', a=pr(t, t78 + 0.6, 0.4))
        return
    headline(c, ['A typical', 'couple loses:'], LX, HY, 130, t, tc - 0.4)
    n = int(18400 * eo(pr(t, tc + 0.6, 1.2)))
    text(c, '$' + '{:,}'.format(n), 540, 1150, 'blk', 200, RED, 'c', track=-0.04, a=pr(t, tc, 0.4))
    text(c, 'a year', 540, 1250, 'sb', 64, INK, 'c', a=pr(t, tc + 0.3, 0.4))
    mono(c, 'RETIRING IN 2033 · ESTIMATE: CRFB', 540, 1340, 22, GREY, 'c', a=pr(t, tc + 0.5, 0.4))


def sc_why(c, t, S):
    t60 = ph('in nineteen sixty'); tt = ph("today it's under three"); tf = ph('fewer babies')
    bg_cream(c, t)
    kicker(c, 'WHY IT HAPPENS', t, S['t0'] + 0.1)
    if t < tf - 0.4:
        headline(c, ['Fewer workers', 'per retiree.'], LX, HY, 120, t, S['t0'] + 0.2, hl=(0, ('', 'Fewer')), hl_col=YEL)
        rows = ((t60, '1960', 5.1), (tt, 'TODAY', 2.7), (ph('keeps falling'), '2035', 2.3))
        for i, (t0, lab, n) in enumerate(rows):
            k = pr(t, t0 - 0.1, 0.6)
            if k <= 0: continue
            y = 900 + i * 210
            mono(c, lab, LX, y - 40, 26, RED if i else INK, a=k)
            for j in range(6):
                fr = cl(n - j)
                if fr <= 0: break
                kk = cl(k * 6 - j)
                c.save(); c.clipRect(R.MakeXYWH(LX + 40 + j * 100 - 40, y - 140, 80 * fr, 200))
                person(c, LX + 40 + j * 100, y + 60, 1.1, INK, eo(kk))
                c.restore()
            text(c, '%.1f' % n, 820, y + 40, 'blk', 96, RED if i else INK, a=k)
        mono(c, 'WORKERS PER BENEFICIARY · SSA', 540, 1480, 20, GREY, 'c', a=pr(t, t60, 0.4))
        return
    headline(c, ['Three reasons.'], LX, HY, 130, t, tf - 0.4)
    for i, (p_, s) in enumerate((('fewer babies', 'FEWER BABIES'), ('living longer', 'PEOPLE LIVING LONGER'), ('giant wave', 'A GIANT WAVE OF RETIREES'))):
        pill(c, 540, 900 + i * 170, s, pr(t, ph(p_) - 0.15, 0.3), col=(INK, BLUE, RED)[i], size=48)


def sc_1983(c, t, S):
    tm = ph('months from running'); td = ph('made a deal'); ts = ph('signed in april')
    bg_ink(c, t)
    kicker(c, 'THIS HAPPENED BEFORE', t, S['t0'] + 0.1, col=(170, 170, 176))
    if t < td - 0.4:
        k = pr(t, S['t0'] + 0.2, 0.6)
        text(c, '1983', 540, 1080, 'blk', 360, RED, 'c', track=-0.05, a=eo(k))
        cutout(c, 'S6_dome_cut.png', 540, 1500, 540, pr(t, S['t0'] + 0.4, 0.6), bw=True)
        headline(c, ['Months from', 'empty.'], LX, HY, 130, t, tm - 0.3, col=PAPER, hl=(1, ('', 'empty.')), hl_col=RED)
        credit(c, 'PHOTO: DILIFF · CC BY 2.5', col=(150, 150, 160))
        return
    headline(c, ['The deal.'], LX, HY, 150, t, td - 0.4, col=PAPER, hl=(0, ('The ', 'deal.')), hl_col=RED)
    items = ((ph('retirement age'), 'Retirement age', '65 → 67, slowly'), (ph('taxing some'), 'Some benefits', 'now taxed'), (ph('payroll taxes sooner'), 'Payroll taxes', 'raised sooner'))
    for i, (t0, a, b) in enumerate(items):
        def dr(cc, a=a, b=b, i=i):
            mono(cc, '0%d' % (i + 1), 40, 60, 22, RED)
            text(cc, a, 40, 140, 'blk', 58, INK)
            text(cc, b, 40, 200, 'sb', 40, GREY)
        card(c, 540, 830 + i * 240, 820, 220, (-2, 1.5, -1)[i], pr(t, t0 - 0.2, 0.4), dr, rad=20)
    if t > ts - 0.3:
        pill(c, 540, 1500, 'SIGNED APRIL 1983 · JUST IN TIME', pr(t, ts - 0.3, 0.3), col=GREEN, txt=INK, size=34)


def sc_options(c, t, S):
    tt = ph('about a third'); tq = ph('about a quarter'); tw = ph('every year congress')
    cover(c, img('S1_capitol.jpg'), 0, 0, W, H, 1.9 + 0.02 * (t - S['t0']), 0.5, 0.42)
    shade(c, 0.6, (4, 8, 30))
    kicker(c, 'THE OPTIONS', t, S['t0'] + 0.1, col=(200, 210, 240))
    headline(c, ['Pick one.', 'Or both.'], LX, HY, 150, t, S['t0'] + 0.2, col=PAPER, hl=(1, ('Or ', 'both.')), hl_col=RED)
    for i, (t0, big, lab, col) in enumerate(((tt, '+34%', 'PAYROLL TAX', BLUE), (tq, '-25%', 'BENEFITS', RED))):
        def dr(cc, big=big, lab=lab, col=col):
            mono(cc, lab, 30, 56, 22, GREY)
            text(cc, big, 30, 190, 'blk', 120, col)
        card(c, 300 + i * 460, 1060, 400, 250, (-2, 2)[i], pr(t, t0 - 0.2, 0.45), dr, rad=20)
    if t > tw - 0.3:
        pill(c, 540, 1300, 'EVERY YEAR OF WAITING = A BIGGER FIX', pr(t, tw - 0.3, 0.3), col=YEL, txt=INK, size=32)
    mono(c, 'TO FIX 75 YEARS, IF DONE NOW · TRUSTEES / CRFB', 540, 1420, 20, (190, 200, 220), 'c', a=pr(t, tt, 0.4))
    credit(c, 'PHOTO: MARTIN FALBISONER · CC BY-SA 3.0', col=(180, 190, 210))


def sc_predict(c, t, S):
    tc = ph("the checks don't stop"); tl = ph('very last minute'); tm = ph('expect it to be a mix')
    bg_red(c, t)
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    if t < tl - 0.4:
        headline(c, ["Social Security", "doesn't vanish."], LX, HY, 118, t, S['t0'] + 0.2, col=PAPER, hl=(1, ("doesn't ", 'vanish.')), hl_col=INK)
        check(c, 540, 1180, 0.9, 0.0, rot=2, t=t)
        if t > tc - 0.2: pill(c, 540, 1460, "CHECKS DON'T STOP", pr(t, tc - 0.2, 0.3), col=PAPER, txt=INK, size=40)
        return
    headline(c, ['A last-minute', 'deal.'], LX, HY, 130, t, tl - 0.4, col=PAPER, hl=(1, ('', 'deal.')), hl_col=INK)
    timeline(c, 160, 900, 1080, [(0.0, '2026', 'WARNINGS'), (0.6, '2030', 'STILL WAITING'), (1.0, '2032', 'DEAL')], pr(t, tl - 0.2, 1.6), t)
    if t > tm - 0.2:
        pill(c, 540, 1300, 'MORE MONEY IN', pr(t, ph('more money coming') - 0.2, 0.3), col=PAPER, txt=INK, size=40)
        pill(c, 540, 1420, 'SMALLER PROMISES FOR YOUNGER WORKERS', pr(t, ph('smaller promises') - 0.2, 0.3), col=INK, size=32)


def sc_ask(c, t, S):
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Will it be there', 'when you retire?'], LX, HY, 112, t, S['t0'] + 0.1, hl=(1, ('when you ', 'retire?')), hl_col=YEL)
    k = pr(t, S['t0'] + 0.3, 0.5)
    def dr(cc):
        cover(cc, img('S2_poster.jpg'), 12, 12, 336, 456, 1.0, 0.5, 0.35)
    card(c, 540, 1060, 360, 480, 3, k, dr, rad=8)
    pill(c, 330, 1400, 'YES', pr(t, ph('yes or no') - 0.1, 0.3), col=GREEN, txt=INK, size=70)
    pill(c, 750, 1400, 'NO', pr(t, ph('yes or no') + 0.2, 0.3), col=RED, txt=PAPER, size=70)
    credit(c, 'POSTER: NARA · PUBLIC DOMAIN', a=k)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='how', t0=ph("here's how it works") - 0.2, fn=sc_how, tin='whip'),
    dict(k='report', t0=ph('in june') - 0.2, fn=sc_report, tin='zoom'),
    dict(k='why', t0=ph('so why is this') - 0.2, fn=sc_why, tin='whip'),
    dict(k='y1983', t0=ph("and here's the wild") - 0.2, fn=sc_1983, tin='wipe', col=INK),
    dict(k='options', t0=ph('so what are the options') - 0.2, fn=sc_options, tin='zoom'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('pay cut'), 10, 0.3)
EP.shk(ph('runs dry in late'), 8, 0.3)
EP.shk(ph('panicked'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
