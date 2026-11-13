"""NextBigNow (editorial look) ep 43: Microsoft 365 / Outlook outage, 12-13 Nov 2026 — what happens next time.
Facts: reports from ~12:00 PM ET Nov 12; Downdetector peak >130,000 (Outlook); UK schools, banks, hospitals, a parliamentary
network hit; 48h email queue; Microsoft: servers 'unexpectedly unavailable', no malicious activity (Tom's Guide / Windows Central
live blogs, 12-13 Nov 2026). CrowdStrike 19 Jul 2024 ~8.5M Windows devices; AWS us-east-1 20 Oct 2025 ~15 h; EU DORA in force
17 Jan 2025; UK critical third parties regime."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('OU_DIR', 'outage'))
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90                     # left text margin
HY = 540                    # first headline baseline


def kicker(c, s, t, t0, y=400, col=GREY):
    k = pr(t, t0, 0.3)
    if k > 0:
        c.drawRect(R.MakeXYWH(LX, y - 22, 14, 14), paint(RED, k))
        mono(c, s, LX + 30, y - 8, 26, col, a=k)


# ================================================================== 1. hook
def sc_hook(c, t, S):
    ts = ph('stopped'); td = ph('down for more'); tq = ph("here's the real question")
    if t < tq - 0.15:
        bg_cream(c, t)
        kicker(c, 'NOV 12, 2026 · GLOBAL OUTAGE', t, 0.1)
        headline(c, ["The world's", 'inbox stopped.'], LX, HY, 132, t, 0.15, hl=(1, ('inbox ', 'stopped.')), hl_col=RED_L)
        broken = pr(t, ts - 0.1, 0.5)
        inbox(c, 540, 1110, 880, 740, -2.5 + 1.5 * math.sin(t * 0.6), pr(t, 0.2, 0.6), t, broken=broken)
        for i, s in enumerate(('Outlook', 'Teams', 'Microsoft 365')):
            pill(c, 260 + i * 270 + (40 if i == 2 else 0), 1440, s, pr(t, ph('outlook') - 0.1 + i * 0.35, 0.3), col=INK, size=34)
        if t > td - 0.2:
            pill(c, 540, 760, '24+ HOURS DOWN', pr(t, td - 0.2, 0.3), col=RED, size=46)
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What happens', 'next time?'], LX, HY + 120, 140, t, tq - 0.05, col=PAPER, hl=(1, ('', 'next time?')), hl_col=INK)
    k = pr(t, ph('break everything') - 0.4, 0.5)
    if k > 0:
        for i in range(9):
            ang = cl((t - ph('break everything')) * 1.6 - i * 0.12) * 75
            domino(c, 170 + i * 92, 1500, 1.0, ang, PAPER)
        text(c, "Why one company's bad day", LX, 1000, 'xb', 62, PAPER, a=eo(k))
        text(c, 'breaks everything.', LX, 1072, 'xb', 62, PAPER, a=eo(k))


# ================================================================== 2. the numbers
def sc_numbers(c, t, S):
    tp = ph('at the peak'); tb = ph('just the people who')
    bg_cream(c, t)
    kicker(c, 'NOV 12 · FROM 12:00 PM ET', t, S['t0'] + 0.1)
    n = int(130000 * eo(pr(t, tp, 1.4)))
    text(c, '{:,}+'.format(n) if t > tp else '0', LX, 560, 'blk', 190, INK, maxw=900)
    text(c, 'outage reports at the peak', LX, 640, 'sb', 50, GREY)
    def dr(cc):
        mono(cc, 'DOWNDETECTOR · OUTLOOK REPORTS', 50, 70, 22)
        line_chart(cc, 50, 120, 760, 430, [(0, 2), (0.12, 3), (0.22, 60), (0.32, 130), (0.45, 90), (0.6, 60), (0.75, 37), (0.88, 30), (1.0, 12)],
                   pr(t, S['t0'] + 0.4, max(1.0, tb - S['t0'])), labels=[(0.05, '11 AM'), (0.32, 'PEAK'), (0.6, '4 PM'), (0.95, 'NEXT DAY')], ymax=150)
    card(c, 540, 1160, 860, 660, 1.5, pr(t, S['t0'] + 0.2, 0.5), dr)
    if t > tb - 0.2:
        pill(c, 540, 1500, '...and only people who bothered to report', pr(t, tb - 0.2, 0.3), col=INK, size=32)


def sc_who(c, t, S):
    tq = ph('in a queue')
    bg_cream(c, t)
    kicker(c, 'WHO GOT HIT · UK', t, S['t0'] + 0.1)
    headline(c, ['Schools. Banks.', 'Hospitals.'], LX, HY, 132, t, S['t0'] + 0.1, hl=(1, ('', 'Hospitals.')), hl_col=YEL)
    labels = (('schools', 'SCHOOLS'), ('banks', 'BANKS'), ('hospitals', 'HOSPITALS'), ('parliament', 'PARLIAMENT NETWORK'))
    for i, (p_, lbl) in enumerate(labels):
        k = pr(t, ph(p_) - 0.15, 0.4)
        def dr(cc, lbl=lbl, i=i):
            cc.drawCircle(60, 66, 14, paint(RED))
            text(cc, lbl, 96, 82, 'xb', 50, INK, maxw=640)
            mono(cc, 'SERVICE DISRUPTED', 96, 130, 20)
        card(c, 540 + (-30 if i % 2 else 30), 820 + i * 150, 760, 170, (-2.5 if i % 2 else 2), k, dr, rad=20) if t < tq - 0.3 else None
    if t > tq - 0.3:
        k = pr(t, tq - 0.3, 0.5)
        for i in range(6):
            def dr(cc):
                cc.drawLine(0, 0, 160, 100, stroke(LIGHT, 4)); cc.drawLine(320, 0, 160, 100, stroke(LIGHT, 4))
            card(c, 540 + (i - 2.5) * 14, 1180 - i * 26, 340, 220, (i - 2.5) * 3, cl(k * 1.5 - i * 0.1), dr, rad=14, drop=20)
        pill(c, 540, 1500, 'EMAILS HELD UP TO 48 HOURS', k, col=INK, size=40)


def sc_cause(c, t, S):
    th = ph('not hackers'); ts = ph('unexpectedly went offline'); tc = ph('got crushed')
    bg_cream(c, t)
    kicker(c, 'THE CAUSE', t, S['t0'] + 0.1)
    headline(c, ['Not hackers.'], LX, HY, 140, t, th - 0.1, hl=(0, ('Not ', 'hackers.')), hl_col=GREEN)
    if t < ts - 0.3:
        source_card(c, 540, 1100, 860, 560, -2, pr(t, S['t0'] + 0.2, 0.5), 'Microsoft 365 Status', 'NOV 13, 2026',
                    ['"No indication of', 'malicious activity."'], t, body_rows=3, head_size=62, label='COMPANY STATEMENT')
        return
    for i in range(5):
        down = pr(t, ts + i * 0.18, 0.2) if i in (1, 3) else (pr(t, tc - 0.2 + i * 0.1, 0.3) if t > tc - 0.2 else 0)
        server(c, 150 + i * 195, 1280 + 10 * math.sin(t * 2 + i), 0.85, t, down=down)
    if t > tc - 0.3:
        text(c, 'one part fails...', LX, 820, 'xb', 66, INK, a=eo(pr(t, tc - 0.3, 0.3)))
        text(c, 'everything on top falls.', LX, 900, 'xb', 66, RED, a=eo(pr(t, ph('everything piled') - 0.1, 0.3)))


# ================================================================== 3. concentration
def sc_three(c, t, S):
    tp = ph('sixty percent')
    bg_cream(c, t)
    kicker(c, 'WHO RUNS THE CLOUD', t, S['t0'] + 0.1)
    headline(c, ['3 companies.', '60%+ of the cloud.'], LX, HY, 118, t, S['t0'] + 0.2, hl=(1, ('', '60%+')), hl_col=YEL)
    k = pr(t, ph('amazon') - 0.2, max(1.2, tp - ph('amazon') + 0.4))
    def dr(cc):
        mono(cc, 'SHARE OF CLOUD INFRASTRUCTURE · 2025', 50, 70, 22)
        bar_split(cc, 50, 140, 760, 120, [('Amazon', 0.30, INK), ('Microsoft', 0.20, RED), ('Google', 0.13, (90, 90, 96)), ('Everyone else', 0.37, LIGHT)], k, t)
        mono(cc, 'APPROX. · SYNERGY RESEARCH GROUP', 50, 400, 20)
    card(c, 540, 1180, 860, 460, -1.5, pr(t, ph('amazon') - 0.4, 0.5), dr)


def sc_rent(c, t, S):
    tr = ph('they rent it')
    bg_cream(c, t)
    kicker(c, 'ONE SNEEZE, EVERYONE CATCHES A COLD', t, S['t0'] + 0.1)
    node_graph(c, t, pr(t, S['t0'] + 0.6, 2.0), cy=1180)
    for i, (p_, lbl, x, y) in enumerate((('your bank', 'BANK', 230, 1450), ('your school', 'SCHOOL', 540, 1490), ('your airline', 'AIRLINE', 850, 1450))):
        pill(c, x, y, lbl, pr(t, ph(p_) - 0.1, 0.3), col=RED, size=34)
    if t < tr - 0.3:
        headline(c, ["They don't", 'own it.'], LX, HY, 132, t, ph("they don't own") - 0.1)
    else:
        headline(c, ['They rent it.'], LX, HY, 132, t, tr - 0.2, hl=(0, ('They ', 'rent it.')), hl_col=GREEN)


# ================================================================== 4. pattern
def sc_pattern(c, t, S):
    t25 = ph('october twenty twenty'); tb = ph('yes beds')
    bg_cream(c, t)
    kicker(c, 'THIS KEEPS HAPPENING', t, S['t0'] + 0.1)
    headline(c, ['It keeps', 'happening.'], LX, HY, 132, t, S['t0'] + 0.1)
    events = ((ph('july twenty'), 'JUL 19, 2024', 'CrowdStrike update', '~8.5M Windows PCs crashed', -2.5, 830),
              (t25, 'OCT 20, 2025', 'Amazon cloud (AWS)', 'Down for about 15 hours', 2.0, 1090),
              (ph('yes beds') + 0.8, 'NOV 12, 2026', 'Microsoft 365', 'Down for 24+ hours', -1.5, 1350))
    for i, (t0, date, who, what, rot, y) in enumerate(events):
        def dr(cc, date=date, who=who, what=what, i=i):
            mono(cc, date, 44, 64, 24, RED if i == 2 else GREY)
            text(cc, who, 44, 138, 'blk', 60, INK, maxw=720)
            text(cc, what, 44, 200, 'sb', 40, GREY, maxw=720)
        card(c, 540, y, 820, 250, rot, pr(t, t0 - 0.2, 0.45), dr, rad=22)
    if t > tb - 0.2 and t < tb + 1.0:
        pill(c, 760, 1250, 'Yes, smart beds.', pr(t, tb - 0.2, 0.25), col=YEL, txt=INK, size=38)


# ================================================================== 5. prediction
def sc_predict(c, t, S):
    ta = ph('now including ai')
    bg_red(c, t)
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    headline(c, ['Outages get', 'bigger.'], LX, HY + 40, 150, t, ph('going to get bigger') - 0.2, col=PAPER, hl=(1, ('', 'bigger.')), hl_col=INK)
    k = pr(t, ph('we\'re putting more') - 0.2, 1.6)
    for i in range(9):
        x = 150 + (i % 3) * 390 / 1.0 if False else 170 + (i % 3) * 370
        y = 1050 + (i // 3) * 200
        kk = cl(k * 9 - i)
        if kk <= 0: continue
        def dr(cc, i=i):
            cc.drawRect(R.MakeXYWH(0, 0, 300, 160), paint((34, 34, 40)))
            for j in range(3): cc.drawLine(24, 40 + j * 40, 200, 40 + j * 40, stroke((80, 80, 90), 6))
            cc.drawCircle(256, 80, 12, paint(GREEN if (int(t * 3) + i) % 3 else RED))
        card(c, x, y, 300, 160, 0, kk, dr, col=(34, 34, 40), rad=14, drop=30)
    if t > ta - 0.2:
        pill(c, 540, 1470, '+ AI, IN THE SAME FEW DATA CENTERS', pr(t, ta - 0.2, 0.3), col=INK, size=34)


def sc_gov(c, t, S):
    tu = ph('the uk is moving')
    bg_cream(c, t)
    kicker(c, 'GOVERNMENTS ARE WORRIED', t, S['t0'] + 0.1)
    headline(c, ['Prove you can', 'survive it.'], LX, HY, 128, t, S['t0'] + 0.2, hl=(1, ('', 'survive it.')), hl_col=YEL)
    def d1(cc):
        mono(cc, 'EU · IN FORCE SINCE JAN 2025', 50, 70, 22)
        text(cc, 'DORA', 50, 160, 'blk', 90, INK)
        text(cc, 'Banks must manage the risk of', 50, 230, 'sb', 38, GREY)
        text(cc, 'their tech suppliers failing.', 50, 280, 'sb', 38, GREY)
    def d2(cc):
        mono(cc, 'UK · FINANCIAL REGULATORS', 50, 70, 22)
        text(cc, 'Critical third parties', 50, 150, 'blk', 60, INK, maxw=740)
        text(cc, 'Big cloud suppliers can be', 50, 220, 'sb', 38, GREY)
        text(cc, 'overseen directly.', 50, 270, 'sb', 38, GREY)
    card(c, 540, 960, 840, 340, -2, pr(t, ph('in europe') - 0.2, 0.45), d1)
    card(c, 540, 1360, 840, 320, 2, pr(t, tu - 0.2, 0.45), d2)


def sc_planb(c, t, S):
    bg_cream(c, t)
    kicker(c, 'WHAT COMPANIES DO NEXT', t, S['t0'] + 0.1)
    headline(c, ['Everyone buys', 'a plan B.'], LX, HY, 132, t, S['t0'] + 0.1, hl=(1, ('a ', 'plan B.')), hl_col=GREEN)
    for i, (p_, lbl) in enumerate((('a backup cloud', 'Backup cloud'), ('backup way to talk', 'Backup chat'), ('plain old paper', 'Plain old paper'))):
        def dr(cc, lbl=lbl):
            cc.drawCircle(70, 90, 34, paint(GREEN)); cc.drawLine(54, 92, 66, 104, stroke(PAPER, 8)); cc.drawLine(66, 104, 88, 76, stroke(PAPER, 8))
            text(cc, lbl, 130, 110, 'blk', 64, INK, maxw=620)
        card(c, 540, 900 + i * 230, 800, 180, (-2, 1.5, -1)[i], pr(t, ph(p_) - 0.2, 0.45), dr, rad=22)


def sc_fear(c, t, S):
    tu = ph('until the day')
    bg_ink(c, t)
    kicker(c, 'WHY WE FEAR IT', t, S['t0'] + 0.1, col=(170, 170, 176))
    headline(c, ["You don't", 'notice it...'], LX, HY + 120, 140, t, ph("you don't notice") - 0.1, col=PAPER)
    if t > tu - 0.2:
        headline(c, ['until it\'s gone.'], LX, HY + 440, 140, t, tu - 0.2, col=PAPER, hl=(0, ('until ', "it's gone.")), hl_col=RED)
    on = t < tu + 0.2
    c.drawCircle(540, 1350, 120 if on else 110, paint(YEL if on else (60, 60, 64)))
    if on: c.drawCircle(540, 1350, 220, paint(YEL, 0.15, blur=30))


def sc_ask(c, t, S):
    tq = ph("what's the first thing")
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Cloud down', 'for a week.'], LX, HY, 140, t, S['t0'] + 0.1, hl=(1, ('', 'for a week.')), hl_col=RED_L)
    def dr(cc):
        text(cc, 'What breaks first', 50, 120, 'blk', 64, INK)
        text(cc, 'in your life?', 50, 196, 'blk', 64, INK)
        mono(cc, 'TELL ME IN THE COMMENTS', 50, 270, 24, RED)
    card(c, 540, 1150, 800, 340, -2, pr(t, tq - 0.3, 0.45), dr)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='numbers', t0=ph('it started around') - 0.2, fn=sc_numbers, tin='whip'),
    dict(k='who', t0=ph('in the uk') - 0.2, fn=sc_who, tin='zoom'),
    dict(k='cause', t0=ph('and the cause') - 0.2, fn=sc_cause, tin='whip'),
    dict(k='three', t0=ph("here's why that's scary") - 0.2, fn=sc_three, tin='wipe', col=RED),
    dict(k='rent', t0=ph('so when one of them') - 0.2, fn=sc_rent, tin='zoom'),
    dict(k='pattern', t0=ph('and this keeps happening') - 0.2, fn=sc_pattern, tin='whip'),
    dict(k='predict', t0=ph("so what's next") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='gov', t0=ph('governments are already') - 0.2, fn=sc_gov, tin='wipe', col=CREAM),
    dict(k='planb', t0=ph('and companies will start') - 0.2, fn=sc_planb, tin='zoom'),
    dict(k='fear', t0=ph("that's why people fear") - 0.2, fn=sc_fear, tin='wipe', col=INK),
    dict(k='ask', t0=ph('so tell me') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('stopped'), 10, 0.3)
EP.shk(ph('got crushed'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
