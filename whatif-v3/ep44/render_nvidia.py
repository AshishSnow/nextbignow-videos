"""NextBigNow (editorial look) ep 44: Jensen Huang resigns — what happens to Nvidia now?
Facts: Nvidia 8-K/press release 12 Nov 2026 (resigned as president, CEO and director, effective immediately; Colette Kress
interim CEO; Harvey Jones first chair; no reason given). Al Jazeera 12 Nov 2026 (admitted infidelity; NYT reported relationship
with a direct report; ~90% advanced AI chip share; shares down >14% intraday; Kress CFO since Sep 2013, revenue $4.13bn FY2014 ->
$215.9bn FY2026). TheStreet/Alertsify 13 Nov (closed down ~4.3%; earnings next Tuesday). Apple first US $1T company Aug 2018;
Uber: Kalanick out 2017, first annual operating profit 2023; Microsoft stock flat for a decade+ after 2000."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('NV_DIR', 'nvidia'))
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


def kicker(c, s, t, t0, y=400, col=GREY):
    k = pr(t, t0, 0.3)
    if k > 0:
        c.drawRect(R.MakeXYWH(LX, y - 22, 14, 14), paint(RED, k))
        mono(c, s, LX + 30, y - 8, 26, col, a=k)


# ================================================================== hook
def sc_hook(c, t, S):
    tg = ph('he was gone'); tq = ph('so what happens now')
    if t < tq - 0.15:
        bg_cream(c, t)
        kicker(c, 'NOV 12, 2026 · NVIDIA', t, 0.1)
        k = pr(t, 0.15, 0.5)
        text(c, 'For', LX, 520, 'blk', 90, INK, a=eo(k))
        n = int(33 * eo(pr(t, 0.3, 1.2)))
        text(c, str(n), LX - 10, 900, 'blk', 420, INK, track=-0.06, a=eo(k))
        text(c, 'years,', 600, 700, 'blk', 96, INK, a=eo(pr(t, 0.6, 0.4)))
        text(c, 'one man.', 600, 800, 'blk', 96, INK, a=eo(pr(t, 0.9, 0.4)))
        if t > tg - 0.3:
            kk = pr(t, tg - 0.3, 0.5)
            highlight(c, 590, 830, 380 * 0 + tw('gone.', 'blk', 150) + 30, 140, kk, RED_L)
            text(c, 'gone.', 605, 950, 'blk', 150, INK, a=eo(kk))
        chair(c, 540, 1520, 0.95, light=pr(t, 0.5, 1.0))
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What happens', 'to Nvidia now?'], LX, HY + 60, 136, t, tq - 0.05, col=PAPER, hl=(1, ('to ', 'Nvidia now?')), hl_col=INK)
    chip(c, 540, 1240, 1.0, t, glow=pr(t, tq + 0.4, 0.6))


def sc_catch(c, t, S):
    t90 = ph('ninety percent')
    bg_cream(c, t)
    kicker(c, 'QUICK CATCH-UP', t, S['t0'] + 0.1)
    if t < t90 - 0.6:
        headline(c, ['From graphics', 'cards to AI.'], LX, HY, 132, t, S['t0'] + 0.15, hl=(1, ('cards to ', 'AI.')), hl_col=GREEN)
        timeline(c, 150, 930, 1180, [(0.0, '1993', 'CO-FOUNDED'), (0.35, 'GPUs', 'GAMING'), (0.7, 'AI', 'THE BOOM'), (1.0, '2026', 'RESIGNS')],
                 pr(t, S['t0'] + 0.6, 3.0), t)
        return
    headline(c, ['90% of AI chips.'], LX, HY, 120, t, t90 - 0.6, hl=(0, ('', '90%')), hl_col=GREEN)
    donut(c, 540, 1140, 280, 0.9, pr(t, t90 - 0.5, 1.0), col=GREEN, label='90%')
    mono(c, 'EST. SHARE OF ADVANCED AI CHIPS', 540, 1520, 24, GREY, 'c')


def sc_week(c, t, S):
    t1 = ph("he'd been unfaithful") if True else 0
    t2 = ph('reports linked'); t3 = ph("nvidia didn't give")
    bg_cream(c, t)
    kicker(c, 'A WEEK OF HEADLINES', t, S['t0'] + 0.1)
    headline(c, ['Then came', 'the headlines.'], LX, HY, 130, t, S['t0'] + 0.1)
    items = ((ph('he admitted') - 0.2, 'HE SAID · NOV 8', ['Admitted he was', 'unfaithful.'], -2.5, 820),
             (t2 - 0.2, 'NEWS REPORTS · NOV 11', ['Relationship with an', 'exec who reported to him.'], 2.0, 1080),
             (t3 - 0.2, 'NVIDIA FILING · NOV 12', ['Resigned. Effective', 'immediately.'], -1.5, 1340))
    for t0, lab, lines, rot, y in items:
        def dr(cc, lab=lab, lines=lines):
            mono(cc, lab, 44, 60, 22, RED)
            cc.drawLine(44, 82, 776, 82, stroke(INK, 3))
            for li, ln in enumerate(lines): text(cc, ln, 44, 150 + li * 60, 'blk', 52, INK, maxw=730)
        card(c, 540, y, 820, 230, rot, pr(t, t0, 0.45), dr, rad=20)


def sc_stock(c, t, S):
    t14 = ph('fourteen percent'); t4 = ph('to about four')
    bg_cream(c, t)
    kicker(c, 'THURSDAY · NVDA', t, S['t0'] + 0.1)
    big = '-14%' if t < t4 - 0.1 else '-4%'
    col = RED if t < t4 - 0.1 else INK
    k = pr(t, t14 - 0.3, 0.4)
    text(c, big, LX, 720, 'blk', 300, col, track=-0.05, a=eo(k))
    text(c, 'at the worst point' if t < t4 - 0.1 else 'by the close', LX, 800, 'sb', 50, GREY, a=eo(k))
    def dr(cc):
        mono(cc, 'NVIDIA SHARES · THURSDAY (ILLUSTRATIVE SHAPE)', 50, 70, 20)
        line_chart(cc, 50, 120, 760, 380, [(0, 100), (0.15, 97), (0.35, 86), (0.5, 88), (0.7, 93), (1.0, 95.7)],
                   pr(t, S['t0'] + 0.3, max(1.0, t4 - S['t0'] + 0.5)), col=RED, ymax=102, labels=[(0.05, 'OPEN'), (0.35, 'LOW'), (0.95, 'CLOSE')], fill=True)
    card(c, 540, 1230, 860, 560, 1.5, pr(t, S['t0'] + 0.2, 0.5), dr)
    mono(c, 'NOT FINANCIAL ADVICE', LX, 860, 22, GREY)


def sc_kress(c, t, S):
    tr = ph('revenue went')
    bg_cream(c, t)
    kicker(c, 'WHO IS IN CHARGE NOW', t, S['t0'] + 0.1)
    if t < tr - 0.3:
        def dr(cc):
            mono(cc, 'INTERIM CEO', 56, 80, 26, RED)
            text(cc, 'Colette Kress', 56, 190, 'blk', 96, INK, maxw=700)
            cc.drawLine(56, 236, 760, 236, stroke(INK, 3))
            text(cc, 'Nvidia CFO since 2013.', 56, 310, 'sb', 44, GREY)
            text(cc, 'Also keeps the CFO job.', 56, 370, 'sb', 44, GREY)
        card(c, 540, 1050, 840, 460, -2, pr(t, S['t0'] + 0.2, 0.5), dr)
        return
    headline(c, ['$4B to $216B.'], LX, HY, 132, t, tr - 0.25, hl=(0, ('$4B to ', '$216B.')), hl_col=GREEN)
    def dr(cc):
        mono(cc, 'NVIDIA ANNUAL REVENUE', 50, 70, 22)
        bars(cc, 60, 120, 740, 480, [('FY2014', 4.13, '$4B', INK), ('FY2026', 215.9, '$216B', GREEN)], pr(t, tr, 1.4))
    card(c, 540, 1150, 860, 720, 1.5, pr(t, tr - 0.3, 0.5), dr)


# ================================================================== slow down?
def sc_slow(c, t, S):
    tn = ph('not soon')
    bg_red(c, t)
    kicker(c, 'DOES AI SLOW DOWN?', t, S['t0'] + 0.1, col=(255, 200, 200))
    headline(c, ['Not soon.'], LX, HY + 60, 170, t, tn - 0.15, col=PAPER, hl=(0, ('Not ', 'soon.')), hl_col=INK)
    steps = (('planned years', 'PLANNED', 'Years ahead'), ('already designed', 'DESIGNED', 'Next chips'), ('huge orders', 'ORDERED', 'By big tech'))
    for i, (p_, a, b) in enumerate(steps):
        def dr(cc, a=a, b=b, i=i):
            mono(cc, 'STEP %d' % (i + 1), 44, 64, 22, RED)
            text(cc, a, 44, 150, 'blk', 66, INK)
            text(cc, b, 44, 214, 'sb', 40, GREY)
        card(c, 540, 930 + i * 250, 760, 230, (-2, 1.5, -1)[i], pr(t, ph(p_) - 0.2, 0.45), dr, rad=22)


def sc_risk(c, t, S):
    tw_ = ph('weird bets'); tr = ph('thirty years in a row')
    bg_ink(c, t)
    kicker(c, 'THE REAL RISK', t, S['t0'] + 0.1, col=(170, 170, 176))
    headline(c, ['Founders make', 'the weird bets.'], LX, HY + 60, 128, t, tw_ - 0.6, col=PAPER, hl=(1, ('the ', 'weird bets.')), hl_col=RED)
    chair(c, 540, 1560 - 60, 0.85, light=1.0)
    if t > tr - 0.6:
        pill(c, 540, 1460, 'RIGHT ABOUT THE FUTURE · 30 YEARS', pr(t, tr - 0.6, 0.35), col=PAPER, txt=INK, size=32)


# ================================================================== history
def sc_history(c, t, S):
    bg_cream(c, t)
    kicker(c, 'HISTORY GIVES US CLUES', t, S['t0'] + 0.1)
    headline(c, ['After the', 'founder leaves.'], LX, HY, 128, t, S['t0'] + 0.1, hl=(1, ('', 'founder leaves.')), hl_col=YEL)
    rows = ((ph('steve jobs'), 'APPLE · 2011', 'Jobs steps down', 'First US $1T company, 2018', True, 820),
            (ph("uber's founder"), 'UBER · 2017', 'Founder pushed out', 'First yearly profit, 2023', True, 1080),
            (ph('bill gates'), 'MICROSOFT · 2000', 'Gates hands over', 'Stock flat for 10+ years', False, 1340))
    for i, (t0, lab, a, b, up, y) in enumerate(rows):
        def dr(cc, lab=lab, a=a, b=b, up=up):
            mono(cc, lab, 44, 62, 22, GREY)
            text(cc, a, 44, 132, 'blk', 54, INK, maxw=580)
            text(cc, b, 44, 192, 'sb', 38, GREEN if up else RED, maxw=600)
            arrow(cc, 720, 125, 0.9, up=up, col=GREEN if up else RED)
        card(c, 540, y, 820, 230, (-2, 1.5, -1.5)[i], pr(t, t0 - 0.2, 0.45), dr, rad=22)


# ================================================================== prediction
def sc_predict(c, t, S):
    tn = ph('the next ceo decides'); tu = ph('used to be')
    bg_red(c, t)
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    headline(c, ["Nvidia doesn't", 'collapse.'], LX, HY + 60, 136, t, S['t0'] + 0.2, col=PAPER, hl=(1, ('', 'collapse.')), hl_col=INK)
    if t > tn - 0.2:
        k = pr(t, tn - 0.2, 0.5)
        crown(c, 330, 1250, 1.0 * eback(k, 1.5))
        mono(c, 'KING OF AI', 330, 1390, 26, PAPER, 'c', a=k)
        text(c, 'or', 540, 1270, 'blk', 80, PAPER, 'c', a=eo(k))
        if t > tu - 0.3:
            pill(c, 760, 1250, 'USED TO BE', pr(t, tu - 0.3, 0.3), col=INK, size=44)


def sc_test(c, t, S):
    tw2 = ph('watch that')
    bg_cream(c, t)
    kicker(c, 'THE FIRST BIG TEST', t, S['t0'] + 0.1)
    headline(c, ['Watch the', 'earnings.'], LX, HY, 150, t, S['t0'] + 0.2, hl=(1, ('', 'earnings.')), hl_col=GREEN)
    def dr(cc):
        mono(cc, 'NEXT EARNINGS REPORT', 56, 80, 24, RED)
        text(cc, 'Next week.', 56, 190, 'blk', 96, INK)
        text(cc, 'First one without Jensen.', 56, 260, 'sb', 42, GREY)
    card(c, 540, 1120, 840, 380, -2, pr(t, S['t0'] + 0.4, 0.5), dr)


def sc_ask(c, t, S):
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Is Nvidia bigger', 'than one person?'], LX, HY, 118, t, S['t0'] + 0.1, hl=(1, ('than ', 'one person?')), hl_col=YEL)
    pill(c, 360, 1100, 'YES', pr(t, ph('yes or no') - 0.1, 0.3), col=GREEN, txt=INK, size=80)
    pill(c, 720, 1100, 'NO', pr(t, ph('yes or no') + 0.2, 0.3), col=RED, txt=PAPER, size=80)
    mono(c, 'TELL ME IN THE COMMENTS', 540, 1300, 26, INK, 'c', a=pr(t, ph('comments') - 0.2, 0.3))
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='catch', t0=ph('quick catch up') - 0.2, fn=sc_catch, tin='whip'),
    dict(k='week', t0=ph('then came a week') - 0.2, fn=sc_week, tin='zoom'),
    dict(k='stock', t0=ph('the money reacted') - 0.2, fn=sc_stock, tin='whip'),
    dict(k='kress', t0=ph('for now the finance') - 0.2, fn=sc_kress, tin='zoom'),
    dict(k='slow', t0=ph('so does ai slow') - 0.2, fn=sc_slow, tin='flash'),
    dict(k='risk', t0=ph('the real risk is slower') - 0.2, fn=sc_risk, tin='wipe', col=INK),
    dict(k='history', t0=ph('history gives us') - 0.2, fn=sc_history, tin='wipe', col=CREAM),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='test', t0=ph('the first big test') - 0.2, fn=sc_test, tin='zoom'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=sc_ask, tin='whip'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('he was gone'), 10, 0.3)
EP.shk(ph('fourteen percent'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
