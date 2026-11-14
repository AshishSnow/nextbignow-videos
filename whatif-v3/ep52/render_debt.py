"""NextBigNow ep 52 (vintage comic + editorial, small subtitles, v5 voice): What happens when a country's debt gets too big?
Facts: Fortune/CBO (28 Oct 2026) - national debt ~$40T; FY2026 interest $1.2T; ~$2.5T/yr by 2036; defense ~$1.1T in 2036. Anadolu/Treasury
(28 Jan 2026) - Q1 FY2026 net interest $270.3B > defense $266.9B; FY2019 interest $375.6B. UK Sept 2022: 23 Sep mini-budget unfunded tax cuts;
gilt yields spiked; sterling record low vs USD (26 Sep); BoE emergency gilt purchases (28 Sep) to stabilise pension (LDI) funds; Truss in
office 49 days (6 Sep - 25 Oct). $1.2T / 365 = ~$3.3B per day.
Photos (Wikimedia Commons): see debt/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('DB_DIR', 'debt'))
PK.IMG = os.path.join(HERE, 'debt', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
SEPIA = (240, 222, 186)
GRN = (80, 200, 120)


def credit(c, key, a=1.0, col=(120, 100, 70), y=1360):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=PAPER, bigsize=54):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.25)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(PAPER if col in (CRED, CBLU) else KINK))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def money_drain(c, t, k):
    """dollar stickers tumbling into a red INTEREST pit."""
    cx, cy = 540, 1260
    c.drawOval(R.MakeXYWH(cx - 330 + 10, cy - 60 + 10, 660, 150), paint(KINK))
    c.drawOval(R.MakeXYWH(cx - 330, cy - 60, 660, 150), paint(CRED))
    dots(c, (cx - 330, cy - 60, 660, 150), (150, 10, 20), cell=16, rmax=5, grad=(0.0, 1.0))
    c.drawOval(R.MakeXYWH(cx - 330, cy - 60, 660, 150), stroke(KINK, 8))
    title(c, 'INTEREST', cx, cy + 34, 70, PAPER, 1.0, 'c', shadow=5)
    for i in range(6):
        ph_ = (t * 0.45 + i / 6) % 1
        x = cx - 260 + 520 * hsh(i, 91) + 40 * math.sin(t * 2 + i)
        y = 840 + 400 * ph_
        a = (1 - cl((ph_ - 0.8) / 0.2)) * k
        place(c, 'D4_dollar_comic.png', x, y, 300 * (1 - 0.4 * ph_), rot=-20 + 40 * hsh(i, 92) + 120 * ph_, a=a, shadow=False)


# ================================================================== scenes
def sc_hook(c, t, S):
    tn = ph('not on schools'); tr = ph('not on roads'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'USA . EVERY SINGLE DAY', LX, 340, 1.0, col=CYEL, size=30)
        title(c, '$3 BILLION+', 70, 560, 158, CRED, 1.0, rot=-2)
        title(c, 'JUST ON INTEREST.', 90, 690, 92, CBLU, 1.0)
        money_drain(c, t, 1.0)
        if t > tn - 0.2: caption(c, 'NOT SCHOOLS', 150, 780, pr(t, tn - 0.2, 0.3), col=PAPER, size=30, rot=-3)
        if t > tr - 0.2: caption(c, 'NOT ROADS', 640, 800, pr(t, tr - 0.2, 0.3), col=PAPER, size=30, rot=3)
        credit(c, 'D4_dollar')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, "WHAT IF A", 90, 540, 130, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, "COUNTRY'S DEBT", 90, 680, 120, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'GETS TOO BIG?', 90, 820, 120, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.6, 0.6)
    place(c, 'D4_dollar_comic.png', 540, 1150 + 10 * math.sin(t * 2), 760 * eback(cl(kk), 1.5), rot=-6, a=kk, shadow=False)


def sc_numbers(c, t, S):
    t40 = ph('forty trillion'); ti = ph('the interest bill'); t19 = ph('back in twenty nineteen'); tm = ph('for a few months')
    paper(c, t)
    caption(c, "HERE'S THE NUMBER", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < ti - 0.3:
        title(c, '$40 TRILLION', 80, 540, 140, CRED, pr(t, t40 - 0.3, 0.4), rot=-2)
        title(c, 'OWED.', 90, 670, 120, CBLU, pr(t, t40, 0.4))
        photo_panel(c, 'D1_clock', 90, 760, 900, 560, 1.2, pr(t, S['t0'] + 0.4, 0.5), t=t - S['t0'])
        caption(c, 'THE NATIONAL DEBT CLOCK, NYC', 160, 1270, pr(t, S['t0'] + 0.8, 0.3), col=CYEL, size=26)
        credit(c, 'D1_clock')
        return
    if t < tm - 0.3:
        title(c, 'INTEREST BILL', 90, 530, 120, CBLU, pr(t, ti - 0.3, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 600), paint(PAPER))
            bars(cc, 140, 120, 620, 340, [('2019', 375.6, '$376B', CCYN), ('2026', 1200, '$1.2T', CRED)], pr(t, ti, 1.6), 1300)
            cc.drawString('US NET INTEREST PER YEAR (TREASURY / CBO)', 30, 580, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 640, 900, 600, rot=1.0, k=pr(t, ti - 0.1, 0.5), draw=dr)
        if t > t19: burst(c, 830, 680, 110, 'x3!', pr(t, t19 + 0.5, 0.35), size=56, rot=8)
        return
    title(c, 'INTEREST', 90, 530, 140, CRED, pr(t, tm - 0.3, 0.4))
    title(c, '> MILITARY', 90, 680, 140, CBLU, pr(t, tm, 0.4))
    mini(c, 90, 780, 430, 360, -2, pr(t, tm + 0.6, 0.4), 'INTEREST (OCT-DEC 2025)', '$270B', CRED, bigsize=66)
    mini(c, 560, 800, 430, 360, 1.5, pr(t, tm + 1.0, 0.4), 'DEFENSE (SAME 3 MONTHS)', '$267B', CBLU, bigsize=66)


def rate_chart(cc, w, h, k):
    x0, y0, cw, ch = 70, 60, w - 120, h - 140
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    pts = [(0, 0.05), (0.2, 0.04), (0.45, 0.03), (0.55, 0.15), (0.7, 0.75), (0.85, 0.85), (1.0, 0.8)]
    p = skia.Path(); first = True
    for fx, v in pts:
        if fx > k: break
        (p.moveTo if first else p.lineTo)(x0 + fx * cw, y0 + ch - v * ch); first = False
    cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(CRED, 9))
    for fx, s in ((0.05, 'NEAR ZERO'), (0.75, 'NOW')):
        cc.drawString(s, x0 + fx * cw, y0 + ch + 44, font('SpecialElite.ttf', 24), paint(KINK))


def sc_why(c, t, S):
    td = ph('debt kept growing'); tr = ph('interest rates went up'); tz = ph('near zero'); to = ph('every old loan'); tb = ph('budget office says'); t36 = ph('two and a half trillion'); tdf = ph('double what america')
    paper(c, t)
    caption(c, 'HOW DID IT GET THIS BAD?', LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tb - 0.3:
        title(c, 'TWO THINGS.', 90, 530, 130, CRED, pr(t, S['t0'] + 0.3, 0.4))
        mini(c, 90, 630, 430, 260, -2, pr(t, td - 0.2, 0.4), 'ONE', 'DEBT UP', CRED, bigsize=60)
        mini(c, 560, 640, 430, 260, 1.5, pr(t, tr - 0.2, 0.4), 'TWO', 'RATES UP', CBLU, bigsize=60)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 380), paint(PAPER)); rate_chart(cc, 900, 380, pr(t, tz - 0.3, 2.5))
            cc.drawString('INTEREST RATES (ILLUSTRATIVE)', 70, 40, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 950, 900, 380, rot=1.0, k=pr(t, tz - 0.4, 0.5), draw=dr)
        if t > to - 0.2: burst(c, 830, 980, 110, 'COSTLY!', pr(t, to, 0.35), size=40, rot=8)
        return
    title(c, 'BY 2036...', 90, 530, 140, CBLU, pr(t, tb - 0.3, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 620), paint(PAPER))
        bars(cc, 70, 120, 760, 360, [('INTEREST 2026', 1.2, '$1.2T', CYEL), ('INTEREST 2036', 2.5, '$2.5T', CRED), ('DEFENSE 2036', 1.1, '$1.1T', CBLU)], pr(t, t36 - 0.6, 1.4), 2.8)
        cc.drawString('CBO PROJECTIONS', 30, 600, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 640, 900, 620, rot=-1.0, k=pr(t, tb, 0.5), draw=dr)
    if t > tdf - 0.3: burst(c, 820, 680, 120, '2x MILITARY', pr(t, tdf - 0.3, 0.35), size=36, rot=8)


def sc_uk(c, t, S):
    tt = ph('big tax cuts'); tp = ph('markets panicked'); tb = ph('government bonds shot up'); tpo = ph('the pound crashed'); tr = ph('emergency rescue'); tm = ph('the prime minister')
    paper(c, t, tint=SEPIA)
    caption(c, 'ASK BRITAIN . SEPTEMBER 2022', LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tp - 0.3:
        title(c, 'TAX CUTS.', 90, 540, 140, CBLU, pr(t, tt - 0.3, 0.4))
        title(c, 'NO PLAN.', 90, 680, 140, CRED, pr(t, ph('no plan') - 0.2, 0.4))
        photo_panel(c, 'D2_boe', 90, 770, 900, 520, 1.2, pr(t, S['t0'] + 0.4, 0.5), fy=0.55, t=t - S['t0'])
        caption(c, 'BANK OF ENGLAND, LONDON', 200, 1240, pr(t, S['t0'] + 0.8, 0.3), col=CYEL, size=26)
        credit(c, 'D2_boe')
        return
    title(c, 'PANIC.', 90, 540, 170, CRED, pr(t, tp - 0.3, 0.4), rot=-3)
    steps = ((tb, 'BOND RATES', 'SHOT UP', CRED), (tpo, 'THE POUND', 'RECORD LOW', CBLU), (tr, 'PENSION FUNDS', 'RESCUED', CYEL), (tm, 'PRIME MINISTER', 'OUT: 49 DAYS', CRED))
    for i, (t0, a, b, col) in enumerate(steps):
        x = 90 + (i % 2) * 470; y = 640 + (i // 2) * 330
        mini(c, x, y, 430, 290, (-2, 1.5, 1.2, -1.5)[i], pr(t, t0 - 0.2, 0.4), a, b, col, txtc=CRED if col == CYEL else PAPER, bigsize=48)


def sc_predict(c, t, S):
    tb = ph('own currency'); tw = ph('world still wants'); tf = ph('fight of the decade'); tt = ph('higher taxes'); ts = ph('spending cuts'); ti = ph('letting inflation'); tl = ph('lose patience'); th = ph('it happens fast')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tf - 0.3:
        title(c, 'NOT BROKE', 90, 540, 150, PAPER, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'TOMORROW.', 90, 690, 150, CYEL, pr(t, S['t0'] + 0.6, 0.4))
        caption(c, 'IT BORROWS IN ITS OWN CURRENCY', 120, 860, pr(t, tb - 0.4, 0.3), col=PAPER, size=30, rot=-2)
        caption(c, 'THE WORLD STILL WANTS DOLLARS', 160, 1000, pr(t, tw - 0.2, 0.3), col=CYEL, size=30, rot=1.5)
        kd = pr(t, tw - 0.1, 0.5)
        place(c, 'D4_dollar_comic.png', 540, 1190 + 8 * math.sin(t * 2), 600 * eback(cl(kd), 1.5), rot=-4, a=kd, shadow=False)
        return
    title(c, 'FIGHT OF', 90, 540, 150, PAPER, pr(t, tf - 0.3, 0.4))
    title(c, 'THE DECADE:', 90, 690, 130, CYEL, pr(t, tf, 0.4))
    for i, (t0, s, col) in enumerate(((tt, 'HIGHER TAXES', CYEL), (ts, 'SPENDING CUTS', PAPER), (ti, 'INFLATION EATS THE DEBT', CCYN))):
        caption(c, s, 130 + (i % 2) * 60, 840 + i * 130, pr(t, t0 - 0.2, 0.3), col=col, size=34, rot=(-2, 1.5, -1)[i])
    if t > th - 0.4: burst(c, 780, 1300, 130, 'FAST!', pr(t, th - 0.4, 0.35), size=60, rot=8)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'DID YOU KNOW', 90, 530, 120, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'THIS?', 90, 670, 160, CRED, pr(t, S['t0'] + 0.3, 0.4))
    photo_panel(c, 'D3_treasury', 120, 740, 840, 420, -1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
    burst(c, 260, 1260, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 820, 1260, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'D3_treasury')
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='numbers', t0=ph("here's the number") - 0.2, fn=with_subs(sc_numbers), tin='whip'),
    dict(k='why', t0=ph('so how did it') - 0.2, fn=with_subs(sc_why), tin='zoom'),
    dict(k='uk', t0=ph('so can a rich') - 0.2, fn=with_subs(sc_uk), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('markets panicked'), 12, 0.35)
EP.shk(ph('the pound crashed'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
