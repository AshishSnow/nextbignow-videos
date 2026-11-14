"""NextBigNow ep 50 (vintage comic + editorial, small subtitles, v5 voice): What happens when a generation can't afford a home? (Spain)
Facts: NPR via WUNC (11 Nov 2026) - first general strike in 14 years, mainly over housing; unions CCOO/UGT: stoppages 90% auto & ports;
Madrid regional govt: 9% of its public employees joined; average rent nearly doubled over the past decade; 87-year-old Madrid woman
evicted, her death made her a symbol; snap election 29 Nov. Al Jazeera (11 Nov 2026) - youth council: 98.7% of a young person's salary to
rent alone; her EUR 500 rent faced a fivefold increase; evicted in September; Bank of Spain: 750,000 homes needed, 92,000 built in 2025.
Olive Press / CJE (May 2026): avg rent EUR 1,176 vs avg young salary EUR 1,190; 75% of 16-34 live with parents; leave home at 30 vs EU 26
(Eurostat). Photos (Wikimedia Commons): 26S housing march - CC BY-SA 4.0; Barcelona balconies - CC0; laundry windows - CC BY 3.0;
Madrid building - CC BY-SA 3.0 (credits in credits.json)."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('SP_DIR', 'spain'))
PK.IMG = os.path.join(HERE, 'spain', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
SEPIA = (240, 222, 186)


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


def paycheck(c, x, y, w, k_rent, t):
    """paycheck strip that rent eats almost entirely."""
    h = 230
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint((236, 244, 232)))
        for i in range(8): cc.drawLine(20, 30 + i * 26, w - 20, 30 + i * 26, stroke((210, 228, 205), 2))
        cc.drawRect(R.MakeWH(w, 56), paint((30, 110, 70)))
        cc.drawString('MONTHLY PAYCHECK . YOUNG WORKER', 20, 38, font('SpecialElite.ttf', 24), paint(PAPER))
        fw = (w - 40) * 0.99 * eo(cl(k_rent))
        cc.drawRect(R.MakeXYWH(20, 80, fw, 110), paint(CRED))
        dots(cc, (20, 80, fw, 110), KINK, cell=14, rmax=3.2, grad=(0.0, 1.0), a=0.3)
        cc.drawRect(R.MakeXYWH(20, 80, w - 40, 110), stroke(KINK, 5))
        if k_rent > 0.3: title(cc, 'RENT', 40 + fw / 2 - 60, 160, 62, PAPER, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=-1.5, k=1.0, draw=dr)
    if k_rent > 0.95:
        caption(c, '1% LEFT', x + w - 120, y + h + 10, pr(k_rent, 0.95, 0.05), col=CYEL, size=26, rot=4)


def house(c, x, y, s, col, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    pts = [(-50, 0), (0, -46), (50, 0), (50, 60), (-50, 60)]
    c.save(); c.translate(6, 6); c.drawPath(poly(pts, True), paint(KINK, a)); c.restore()
    c.drawPath(poly(pts, True), paint(col, a)); c.drawPath(poly(pts, True), stroke(KINK, 6, a))
    c.drawRect(R.MakeXYWH(-12, 26, 24, 34), paint(KINK, a))
    c.restore()


# ================================================================== scenes
def sc_hook(c, t, S):
    tg = ph('whole generation'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'SPAIN, RIGHT NOW', LX, 340, 1.0, size=30)
        title(c, '99%', 80, 640, 240, CRED, 1.0, rot=-3)
        text(c, 'of a young paycheck,', 92, 730, 'blk', 54, KINK)
        text(c, 'just to rent alone.', 92, 795, 'blk', 54, KINK)
        paycheck(c, 120, 870, 840, pr(t, 0.3, 2.2), t)
        if t > ph('ninety nine percent', after=2.0) - 0.2:
            burst(c, 830, 1200, 110, '99%!', pr(t, ph('ninety nine percent', after=2.0) - 0.2, 0.35), size=60, rot=10)
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF A WHOLE', 90, 540, 104, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'GENERATION', 90, 670, 128, CYEL, pr(t, tq + 0.25, 0.4))
    title(c, "CAN'T AFFORD", 90, 800, 104, PAPER, pr(t, tq + 0.5, 0.4))
    title(c, 'A HOME?', 90, 940, 128, CYEL, pr(t, tq + 0.75, 0.4))
    for i in range(5):
        kk = pr(t, tq + 0.9 + i * 0.1, 0.3)
        if kk > 0: house(c, 190 + i * 175, 1180, 1.2 * eback(cl(kk), 2), PAPER if i else CYEL)
    burst(c, 540, 1180, 90, 'X', pr(t, tq + 1.6, 0.3), size=70, rot=8) if False else None


def sc_strike(c, t, S):
    tg = ph('first general strike'); tr = ph('it was about rent'); tu = ph('unions say'); tm = ph("madrid's regional government"); te = ph('either way')
    paper(c, t)
    caption(c, 'NOVEMBER 11, 2026', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tu - 0.3:
        title(c, 'SPAIN STOPS.', 90, 530, 140, CBLU, pr(t, S['t0'] + 0.3, 0.4))
        photo_panel(c, 'E2_protest', 90, 620, 900, 600, 1.2, pr(t, S['t0'] + 0.4, 0.5), fx=0.55, fy=0.5, t=t - S['t0'])
        if t > tg - 0.2: caption(c, 'FIRST GENERAL STRIKE IN 14 YEARS', 140, 1180, pr(t, tg - 0.2, 0.3), col=CYEL, size=28)
        if t > tr - 0.2: burst(c, 830, 650, 120, 'RENT!', pr(t, tr, 0.35), size=56, rot=8)
        credit(c, 'E2_protest')
        return
    title(c, 'WHO JOINED?', 90, 530, 140, CRED, pr(t, tu - 0.3, 0.4))
    mini(c, 90, 640, 430, 420, -2, pr(t, tu - 0.1, 0.4), 'UNIONS SAY', 'PORTS: ~90%', CBLU, bigsize=50)
    mini(c, 560, 660, 430, 420, 1.5, pr(t, tm - 0.1, 0.4), 'MADRID GOV. SAYS', '9% OF STAFF', CYEL, txtc=CRED, bigsize=50)
    if t > te - 0.2: caption(c, 'EITHER WAY: THE MESSAGE WAS LOUD', 140, 1180, pr(t, te - 0.2, 0.3), col=PAPER, size=28)


def sc_numbers(c, t, S):
    td = ph('nearly doubled'); ts = ph('a young worker makes'); ta = ph('the average apartment'); tp = ph('three out of four'); to = ph('they move out at')
    paper(c, t)
    caption(c, "HERE'S HOW BAD IT GOT", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < ts - 0.3:
        title(c, 'RENT: x2', 90, 560, 180, CRED, pr(t, td - 0.3, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
            bars(cc, 140, 100, 620, 330, [('10 YEARS AGO', 1.0, 'x1', CCYN), ('NOW', 1.95, 'x2', CRED)], pr(t, td, 1.0), 2.2)
            cc.drawString('AVERAGE RENT IN SPAIN (APPROX.)', 30, 540, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 680, 900, 560, rot=1.0, k=pr(t, td - 0.2, 0.5), draw=dr)
        return
    if t < tp - 0.3:
        title(c, 'PAY vs RENT', 90, 530, 140, CBLU, pr(t, ts - 0.3, 0.4))
        mini(c, 90, 640, 430, 440, -2, pr(t, ts, 0.4), 'YOUNG SALARY', 'EUR 1,190', (80, 200, 120), txtc=PAPER, bigsize=58)
        mini(c, 560, 660, 430, 440, 1.5, pr(t, ta, 0.4), 'AVERAGE RENT', 'EUR 1,176', CRED, bigsize=58)
        if t > ta + 1.2: burst(c, 540, 1180, 130, '= EUR 14 LEFT', pr(t, ta + 1.2, 0.35), size=38, rot=-6)
        return
    if t < to - 0.3:
        title(c, '3 IN 4', 90, 560, 200, CRED, pr(t, tp - 0.3, 0.4), rot=-2)
        text(c, 'aged 16 to 34 live with parents.', 92, 650, 'blk', 48, KINK)
        for i in range(4):
            kk = pr(t, tp + 0.3 + i * 0.15, 0.3)
            if kk > 0: house(c, 210 + i * 220, 900, 1.6 * eback(cl(kk), 2), CRED if i < 3 else PAPER)
        caption(c, 'SPANISH YOUTH COUNCIL', 330, 1100, pr(t, tp + 1.0, 0.3), col=PAPER, size=26)
        return
    title(c, 'MOVING OUT AT...', 90, 530, 116, CBLU, pr(t, to - 0.3, 0.4))
    burst(c, 320, 900, 210, '30', pr(t, ph('thirty', after=to) - 0.2, 0.35), col=CYEL, txt=CRED, size=150, spikes=18)
    caption(c, 'SPAIN', 250, 1110, pr(t, ph('thirty', after=to), 0.3), size=30)
    burst(c, 770, 960, 150, '26', pr(t, ph('twenty six') - 0.2, 0.35), col=PAPER, txt=CBLU, size=110, spikes=16)
    caption(c, 'EUROPE AVG.', 680, 1130, pr(t, ph('twenty six'), 0.3), size=26)


def sc_why(c, t, S):
    tb = ph('bank of spain'); t9 = ph('ninety two thousand'); tm = ph('more people not enough')
    paper(c, t)
    caption(c, 'SO WHY?', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'NOT ENOUGH', 90, 530, 140, CRED, pr(t, tb - 0.3, 0.4))
    title(c, 'HOMES.', 90, 670, 140, CBLU, pr(t, tb, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
        bars(cc, 140, 100, 620, 330, [('NEEDED', 750, '750K', CRED), ('BUILT 2025', 92, '92K', CCYN)], pr(t, tb + 0.6, 1.0) if t < t9 else 1.0, 820)
        cc.drawString('BANK OF SPAIN', 30, 540, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 760, 900, 560, rot=-1.0, k=pr(t, tb, 0.5), draw=dr)
    if t > tm - 0.2: burst(c, 820, 790, 120, 'PRICES UP!', pr(t, ph('prices only') - 0.2, 0.35), size=34, rot=8)


def sc_story(c, t, S):
    tm = ph('in madrid an'); tf = ph('five times higher'); te = ph('she was evicted'); tw = ph('weeks later')
    paper(c, t, tint=SEPIA)
    caption(c, 'THE STORY THAT BROKE PEOPLE', LX, 340, pr(t, S['t0'], 0.3), size=28)
    title(c, 'MADRID, AGE 87.', 90, 530, 116, KINK if False else CBLU, pr(t, tm - 0.2, 0.4))
    photo_panel(c, 'E5_madrid', 300, 620, 660, 640, 2, pr(t, tm, 0.5), fy=0.5, t=t - S['t0'])
    if t > tf - 0.3:
        mini(c, 80, 760, 380, 300, -3, pr(t, tf - 0.3, 0.4), 'HER RENT', 'EUR 500 x5', CYEL, txtc=CRED, bigsize=50)
    if t > te - 0.2:
        title(c, 'EVICTED.', 540, 1220, 130, CRED, pr(t, te, 0.35), 'c', rot=-6)
    if t > tw: caption(c, 'SHE BECAME THE FACE OF THE CRISIS', 150, 1300, pr(t, ph('the face of'), 0.3), col=PAPER, size=26)
    credit(c, 'E5_madrid')


def sc_politics(c, t, S):
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NOW IT HITS POLITICS', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    title(c, 'SNAP ELECTION', 90, 540, 126, PAPER, pr(t, S['t0'] + 0.3, 0.4))
    title(c, 'NOV 29', 90, 700, 170, CYEL, pr(t, ph('november twenty ninth') - 0.3, 0.4), rot=-2)
    k = pr(t, ph('november twenty ninth'), 0.5)
    if k > 0:
        c.save(); c.translate(540, 1050); s_ = eback(cl(k), 1.8); c.scale(s_, s_)
        c.drawRect(R.MakeXYWH(-200 + 10, -120 + 10, 400, 280), paint(KINK)); c.drawRect(R.MakeXYWH(-200, -120, 400, 280), paint(PAPER))
        c.drawRect(R.MakeXYWH(-200, -120, 400, 280), stroke(KINK, 8)); c.drawRect(R.MakeXYWH(-90, -128, 180, 18), paint(KINK))
        title(c, 'VOTE', 0, 60, 90, CRED, 1.0, 'c', shadow=5)
        c.save(); c.translate(0, -150 - 30 * math.sin(t * 3)); c.rotate(-8)
        c.drawRect(R.MakeXYWH(-70, -90, 140, 100), paint(CYEL)); c.drawRect(R.MakeXYWH(-70, -90, 140, 100), stroke(KINK, 6)); c.restore()
        c.restore()
    if t > ph('center of it') - 0.3: caption(c, 'HOUSING AT THE CENTER', 300, 1280, pr(t, ph('center of it') - 0.3, 0.3), col=CYEL, size=30)


def sc_predict(c, t, S):
    tr = ph('rent caps'); tt = ph('tourist rentals'); tb = ph('build fast'); tc = ph("here's the catch"); th = ph('help renters today'); tl = ph('build less tomorrow'); tf = ph('only real fix')
    if t < tc - 0.3:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
        title(c, 'HOUSING DECIDES', 90, 540, 108, PAPER, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'ELECTIONS.', 90, 680, 140, CYEL, pr(t, S['t0'] + 0.6, 0.4))
        for i, (t0, s, col) in enumerate(((tr, 'MORE RENT CAPS', CYEL), (tt, 'LIMITS ON TOURIST RENTALS', PAPER), (tb, 'PROMISES TO BUILD FAST', CCYN))):
            caption(c, s, 130 + (i % 2) * 50, 860 + i * 140, pr(t, t0 - 0.2, 0.3), col=col, size=34, rot=(-2, 1.5, -1)[i])
        return
    paper(c, t)
    caption(c, 'BUT HERE IS THE CATCH...', LX, 340, pr(t, tc - 0.2, 0.3), size=30)
    title(c, 'RENT CAPS:', 90, 530, 140, CBLU, pr(t, tc, 0.4))
    mini(c, 90, 640, 430, 380, -2, pr(t, th - 0.2, 0.4), 'TODAY', 'HELP RENTERS', (80, 200, 120), bigsize=46)
    mini(c, 560, 660, 430, 380, 1.5, pr(t, tl - 0.2, 0.4), 'TOMORROW', 'LESS BUILDING', CRED, bigsize=46)
    if t > tf - 0.3: burst(c, 540, 1180, 170, 'MORE HOMES', pr(t, tf - 0.3, 0.35), col=CYEL, txt=CRED, size=56, spikes=18, rot=-4)
    if t > ph('homes take years') - 0.2: caption(c, '...AND HOMES TAKE YEARS', 300, 1330, pr(t, ph('homes take years') - 0.2, 0.3), col=PAPER, size=28)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'HOW OLD WERE YOU', 90, 520, 96, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'WHEN YOU MOVED OUT?', 90, 630, 84, CRED, pr(t, S['t0'] + 0.3, 0.4))
    photo_panel(c, 'E4_laundry', 120, 720, 840, 400, -1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
    for i, s in enumerate(('18', '22', '26', '30+')):
        burst(c, 200 + i * 230, 1240, 80, s, pr(t, ph('still at home') - 0.3 + i * 0.12, 0.3), col=(CYEL, PAPER, CCYN, CRED)[i], txt=(CRED, CBLU, PAPER, CYEL)[i], size=50, rot=(-8, 6, -4, 8)[i])
    credit(c, 'E4_laundry')
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
    dict(k='strike', t0=ph('this week spain') - 0.2, fn=with_subs(sc_strike), tin='whip'),
    dict(k='numbers', t0=ph("here's how bad") - 0.2, fn=with_subs(sc_numbers), tin='zoom'),
    dict(k='why', t0=ph('so why is this') - 0.2, fn=with_subs(sc_why), tin='whip'),
    dict(k='story', t0=ph('and then came') - 0.2, fn=with_subs(sc_story), tin='wipe', col=SEPIA),
    dict(k='politics', t0=ph("now it's shaking") - 0.2, fn=with_subs(sc_politics), tin='flash'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='zoom'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('walked off the job'), 10, 0.3)
EP.shk(ph('she was evicted'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
