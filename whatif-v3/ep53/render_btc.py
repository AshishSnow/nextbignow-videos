"""NextBigNow ep 53 (vintage comic + editorial, small subtitles, v5 voice): What if Bitcoin keeps falling?
Facts: Forbes (14 Nov 2026) - BTC ~ $66,000; ATH ~$126,000 Oct 2025; ~$2T wiped from crypto market since late Sept; Fear & Greed 'extreme fear'.
Rio Times (13 Nov 2026) - 10-yr Treasury yield 5.14%; traders price another Fed hike; dollar index up. Pluang / CryptoTimes (13 Nov 2026) -
$1.31B-$1.41B liquidations. History: Nov 2021 high ~$69K -> ~$15.5K Nov 2022 (-77%); FTX collapsed Nov 2022, founder convicted of fraud (2023).
Past drawdowns (approx.): 2011 -93%, 2013-15 -85%, 2017-18 -84%, 2021-22 -77%.
Photos (Wikimedia Commons): see btc/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('BT_DIR', 'btc'))
PK.IMG = os.path.join(HERE, 'btc', 'img')
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
GOLD = (245, 180, 40)


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


def down_chart(cc, w, h, k, pts, color=CRED, labels=()):
    x0, y0, cw, ch = 60, 50, w - 110, h - 130
    vmax = max(v for _, v in pts); vmin = 0
    yv = lambda v: y0 + ch - (v - vmin) / (vmax - vmin) * ch
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    p = skia.Path(); first = True
    for fx, v in pts:
        if fx > k: break
        (p.moveTo if first else p.lineTo)(x0 + fx * cw, yv(v)); first = False
    cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(color, 9))
    for fx, s in labels:
        cc.drawString(s, x0 + fx * cw - 30, y0 + ch + 44, font('SpecialElite.ttf', 24), paint(KINK))


def coin(c, x, y, w, rot=0.0, a=1.0, crack=0.0, split=0.0):
    """the gold coin sticker; crack draws a zig-zag ink line, split pulls the halves apart."""
    if split <= 0:
        place(c, 'K1_coin_comic.png', x, y, w, rot=rot, a=a, shadow=True)
    else:
        for sgn in (-1, 1):
            c.save()
            c.clipRect(R.MakeLTRB(x - w if sgn < 0 else x, y - w, x if sgn < 0 else x + w, y + w))
            place(c, 'K1_coin_comic.png', x + sgn * 60 * split, y + 30 * split * sgn, w, rot=rot + sgn * 10 * split, a=a, shadow=True)
            c.restore()
    if crack > 0 and split <= 0:
        pts = [(0, -0.5), (-0.06, -0.3), (0.05, -0.12), (-0.04, 0.05), (0.06, 0.22), (-0.03, 0.38), (0.02, 0.5)]
        n = max(2, int(len(pts) * crack + 0.999))
        p = skia.Path()
        for i, (fx, fy) in enumerate(pts[:n]):
            (p.moveTo if i == 0 else p.lineTo)(x + fx * w, y + fy * w)
        c.drawPath(p, stroke(KINK, 14 * a)); c.drawPath(p, stroke(PAPER, 4 * a))


# ================================================================== scenes
def sc_hook(c, t, S):
    tw = ph('this week'); tsx = ph('sixty six thousand'); th = ph('almost half'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'BITCOIN . OCTOBER 2025', LX, 340, 1.0, col=CYEL, size=30)
        title(c, '$126,000', 80, 540, 150, GRN, 1.0, rot=-2)
        if t > tw:
            k = pr(t, tw, 0.35)
            c.drawLine(70, 495, 70 + 760 * eo(k), 470, stroke(CRED, 22))
        title(c, '$66,000', 90, 700, 150, CRED, pr(t, tsx - 0.2, 0.4), rot=1.5)
        if t > tw - 0.2: caption(c, 'THIS WEEK', 640, 720, pr(t, tw - 0.2, 0.3), col=PAPER, size=30, rot=4)
        bob = 10 * math.sin(t * 2.2)
        coin(c, 540, 1110 + bob, 520 + 20 * pr(t, 0, 2), rot=-6 + 3 * math.sin(t), crack=pr(t, th - 0.1, 0.6))
        if t > th: burst(c, 850, 1010, 120, 'HALF GONE!', pr(t, th + 0.2, 0.35), size=40, rot=8)
        credit(c, 'K1_coin')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF', 90, 540, 150, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'BITCOIN KEEPS', 90, 690, 120, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'FALLING?', 90, 830, 140, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.5, 0.6)
    fall = pr(t, tq + 0.9, 1.2)
    coin(c, 540, 1130 + 60 * eio(fall), 460 * eback(cl(kk), 1.5), rot=-8 + 20 * fall, a=kk, split=eo(fall))


def sc_what(c, t, S):
    tt = ph('two trillion'); tm = ph('money got more'); ty = ph('ten year treasury'); tr = ph('another rate hike'); td = ph('dollar got stronger'); ts = ph('when safe bonds')
    paper(c, t)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tm - 0.3:
        title(c, '$2 TRILLION', 80, 540, 150, CRED, pr(t, tt - 0.4, 0.4), rot=-2)
        title(c, 'WIPED OUT.', 90, 690, 130, CBLU, pr(t, tt, 0.4))
        caption(c, 'WHOLE CRYPTO MARKET . SINCE LATE SEPTEMBER', 120, 790, pr(t, tt + 0.4, 0.3), col=CYEL, size=24, rot=-1.5)
        photo_panel(c, 'K2_farm', 90, 860, 900, 460, 1.2, pr(t, S['t0'] + 0.4, 0.5), t=t - S['t0'])
        caption(c, 'A BITCOIN MINING FARM', 200, 1270, pr(t, S['t0'] + 0.8, 0.3), col=CYEL, size=26)
        credit(c, 'K2_farm')
        return
    if t < ts - 0.3:
        title(c, 'MONEY GOT', 90, 530, 130, CBLU, pr(t, tm - 0.3, 0.4))
        title(c, 'EXPENSIVE.', 90, 670, 140, CRED, pr(t, tm, 0.4))
        mini(c, 90, 760, 430, 290, -2, pr(t, ty - 0.2, 0.4), '10-YEAR TREASURY', '> 5%', CRED, bigsize=80)
        mini(c, 560, 780, 430, 290, 1.5, pr(t, tr - 0.2, 0.4), 'TRADERS BET ON', 'RATE HIKE', CBLU, bigsize=56)
        mini(c, 300, 1090, 480, 250, -1, pr(t, td - 0.2, 0.4), 'THE DOLLAR', 'STRONGER', CYEL, txtc=CRED, bigsize=60)
        return
    title(c, 'WHO PAYS', 90, 530, 140, CBLU, pr(t, ts - 0.3, 0.4))
    title(c, 'YOU MORE?', 90, 670, 140, CRED, pr(t, ts, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 600), paint(PAPER))
        bars(cc, 140, 120, 620, 340, [('SAFE BONDS', 5, '5%', GRN), ('BITCOIN', 0.12, '0%', GOLD)], pr(t, ts + 0.5, 1.4), 6.5)
        cc.drawString('WHAT EACH ONE PAYS YOU, PER YEAR', 30, 580, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 760, 900, 600, rot=1.0, k=pr(t, ts + 0.1, 0.5), draw=dr)


def loop_arrows(c, cx, cy, r, k, t, steps):
    """4 caption boxes on a circle joined by arrows: the forced-selling spiral."""
    n = len(steps)
    for i in range(n):
        a0 = -math.pi / 2 + i * 2 * math.pi / n
        a1 = a0 + 2 * math.pi / n
        ki = cl(k * n - i)
        if ki <= 0: continue
        p = skia.Path(); m = 24
        for j in range(m + 1):
            a = lerp(a0 + 0.35, a1 - 0.35, j / m * ki)
            (p.moveTo if j == 0 else p.lineTo)(cx + r * math.cos(a), cy + r * math.sin(a))
        c.drawPath(p, stroke(KINK, 14)); c.drawPath(p, stroke(CRED, 7))
        ae = lerp(a0 + 0.35, a1 - 0.35, ki); ex, ey = cx + r * math.cos(ae), cy + r * math.sin(ae)
        tang = ae + math.pi / 2
        hp = poly([(ex + 26 * math.cos(tang), ey + 26 * math.sin(tang)), (ex + 18 * math.cos(tang + 2.4), ey + 18 * math.sin(tang + 2.4)), (ex + 18 * math.cos(tang - 2.4), ey + 18 * math.sin(tang - 2.4))])
        c.drawPath(hp, paint(KINK))
    for i, (s, col, t0) in enumerate(steps):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        kk = pr(t, t0 - 0.2, 0.35)
        if kk <= 0: continue
        wdt = width(s, 'LuckiestGuy.ttf', 40) + 40
        c.save(); c.translate(x, y); c.rotate((-3, 2, -2, 3)[i % 4]); c.scale(eback(kk, 1.6), eback(kk, 1.6))
        c.drawRect(R.MakeXYWH(-wdt / 2 + 8, -34 + 8, wdt, 68), paint(KINK))
        c.drawRect(R.MakeXYWH(-wdt / 2, -34, wdt, 68), paint(col)); c.drawRect(R.MakeXYWH(-wdt / 2, -34, wdt, 68), stroke(KINK, 6))
        title(c, s, 0, 16, 40, PAPER if col != CYEL else KINK, 1.0, 'c', shadow=0)
        c.restore()


def sc_lever(c, t, S):
    tb = ph('borrow money'); tp = ph('when the price drops'); tf = ph('force closed'); tpu = ph('pushes the price'); tfr = ph('on friday alone')
    paper(c, t)
    caption(c, 'WHY IT FALLS EVEN FASTER', LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tfr - 0.3:
        title(c, 'THE DEATH', 90, 530, 140, CRED, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'SPIRAL.', 90, 680, 150, CBLU, pr(t, S['t0'] + 0.6, 0.4))
        steps = [('BORROW TO BET', CBLU, tb), ('PRICE DROPS', CRED, tp), ('FORCE-CLOSED', KINK, tf), ('MORE SELLING', CRED, tpu)]
        k = pr(t, tb, (tpu + 1.0) - tb)
        loop_arrows(c, 540, 1060, 250, k, t, steps)
        place(c, 'K1_coin_comic.png', 540, 1060, 170 * pr(t, tb - 0.2, 0.4), rot=t * 40, shadow=False)
        return
    title(c, 'IN ONE DAY:', 90, 540, 130, CBLU, pr(t, tfr - 0.3, 0.4))
    title(c, '$1 BILLION+', 70, 700, 150, CRED, pr(t, tfr + 0.2, 0.4), rot=-2)
    caption(c, 'OF CRYPTO BETS WIPED OUT . FRIDAY, NOV 13', 110, 800, pr(t, tfr + 0.5, 0.3), col=CYEL, size=24, rot=-1.5)
    photo_panel(c, 'K3_laptop', 120, 870, 840, 460, -1.5, pr(t, tfr, 0.5), t=t - tfr)
    credit(c, 'K3_laptop')


def sc_2022(c, t, S):
    t69 = ph('sixty nine thousand'); t15 = ph('fifteen and a half'); t75 = ph('more than seventy five percent'); tftx = ph('then ftx'); tb = ph('billions of dollars'); tfo = ph('its founder')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS MOVIE...", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < tftx - 0.3:
        title(c, 'NOV 2021:', 90, 530, 130, CBLU, pr(t, S['t0'] + 0.3, 0.4))
        title(c, '$69,000', 90, 680, 150, GRN, pr(t, t69 - 0.3, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 520), paint(PAPER))
            down_chart(cc, 900, 520, pr(t, t15 - 1.2, 1.8), [(0, 69), (0.15, 60), (0.3, 38), (0.45, 45), (0.6, 30), (0.75, 20), (0.9, 19), (1.0, 15.5)],
                       labels=((0.0, 'NOV 2021'), (0.9, 'NOV 2022')))
            cc.drawString('BITCOIN PRICE, $ THOUSANDS (APPROX.)', 30, 500, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 760, 900, 520, rot=1.0, k=pr(t, t69, 0.5), draw=dr)
        if t > t15: burst(c, 800, 830, 120, '$15.5K', pr(t, t15, 0.35), size=44, rot=8)
        if t > t75 - 0.2: burst(c, 560, 1150, 110, '-77%', pr(t, t75, 0.35), size=56, rot=-8)
        return
    title(c, 'THEN FTX', 90, 540, 150, CRED, pr(t, tftx - 0.3, 0.4), rot=-2)
    title(c, 'COLLAPSED.', 90, 690, 140, CBLU, pr(t, tftx + 0.3, 0.4))
    mini(c, 90, 790, 430, 260, -2, pr(t, ph('matter of days') - 0.3, 0.4), 'HOW LONG IT TOOK', 'DAYS', CRED, bigsize=70)
    mini(c, 560, 810, 430, 260, 1.5, pr(t, tb - 0.2, 0.4), 'CUSTOMER MONEY', 'MISSING', CBLU, bigsize=56)
    mini(c, 300, 1100, 480, 230, -1, pr(t, tfo - 0.2, 0.4), 'ITS FOUNDER', 'CONVICTED', CYEL, txtc=CRED, bigsize=56)


def sc_back(c, t, S):
    tr = ph('brand new record'); tw = ph('the wild thing'); tc = ph('crashed more than'); tb = ph('come back every')
    paper(c, t)
    caption(c, 'BUT HERE IS THE TWIST', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tc - 0.3:
        title(c, "IT DIDN'T DIE.", 80, 540, 130, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'NEW RECORD!', 90, 690, 140, GRN, pr(t, tr - 0.2, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 480), paint(PAPER))
            down_chart(cc, 900, 480, pr(t, S['t0'] + 0.3, 2.6), [(0, 15.5), (0.25, 30), (0.45, 42), (0.6, 70), (0.75, 95), (0.9, 110), (1.0, 126)],
                       color=GRN, labels=((0.0, '2022'), (0.9, 'OCT 2025')))
        panel(c, 90, 770, 900, 480, rot=-1.0, k=pr(t, S['t0'] + 0.2, 0.5), draw=dr)
        if t > tr: burst(c, 820, 800, 120, '$126K', pr(t, tr, 0.35), size=48, rot=8)
        return
    title(c, 'CRASH. COMEBACK.', 70, 540, 104, CRED, pr(t, tc - 0.3, 0.4))
    title(c, 'REPEAT.', 90, 680, 150, CBLU, pr(t, tc, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
        bars(cc, 50, 110, 800, 320, [('2011', 93, '-93%', CRED), ('2014', 85, '-85%', CRED), ('2018', 84, '-84%', CRED), ('2022', 77, '-77%', CRED)], pr(t, tc + 0.3, 1.8), 110)
        cc.drawString('BIG BITCOIN CRASHES FROM PEAK (APPROX.)', 30, 540, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 760, 900, 560, rot=1.0, k=pr(t, tc, 0.5), draw=dr)
    if t > tb - 0.3: caption(c, 'SO FAR, IT CAME BACK EVERY TIME', 160, 1290, pr(t, tb - 0.3, 0.3), col=CYEL, size=28, rot=-2)


def sc_predict(c, t, S):
    tz = ph('not going to zero'); tf = ph('too many big funds'); tn = ph('a new risk'); tco = ph('companies that borrowed'); tw = ph('watch them'); tu = ph('things get ugly')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tn - 0.3:
        title(c, 'NOT ZERO.', 90, 540, 160, PAPER, pr(t, tz - 0.3, 0.4))
        title(c, 'NOT THIS WEEK.', 90, 690, 120, CYEL, pr(t, tz + 0.3, 0.4))
        caption(c, 'TOO MANY BIG FUNDS + COMPANIES HOLD IT', 110, 850, pr(t, tf - 0.2, 0.3), col=PAPER, size=28, rot=-2)
        k = pr(t, tf, 0.5)
        place(c, 'K4_hand_comic.png', 540, 1150 + 8 * math.sin(t * 2), 700 * eback(cl(k), 1.4), rot=-3, a=k, shadow=True)
        credit(c, 'K4_hand', col=PAPER)
        return
    title(c, 'THE NEW', 90, 540, 150, PAPER, pr(t, tn - 0.3, 0.4))
    title(c, 'RISK:', 90, 690, 150, CYEL, pr(t, tn, 0.4))
    caption(c, 'COMPANIES THAT BORROWED TO BUY BITCOIN', 110, 850, pr(t, tco - 0.2, 0.3), col=PAPER, size=28, rot=-2)
    caption(c, 'IF ONE IS FORCED TO SELL...', 160, 990, pr(t, ph('forced to sell') - 0.2, 0.3), col=CYEL, size=32, rot=1.5)
    if t > tw - 0.2: caption(c, 'WATCH THEM.', 150, 1170, pr(t, tw - 0.2, 0.3), col=CYEL, size=44, rot=-4)
    if t > tu - 0.3: burst(c, 780, 1240, 130, 'UGLY!', pr(t, tu - 0.3, 0.35), size=60, rot=8)
    if t > ph('financial advice') - 0.6: caption(c, 'NOT FINANCIAL ADVICE', 330, 1360, pr(t, ph('financial advice') - 0.6, 0.3), col=PAPER, size=24)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'WOULD YOU BUY', 80, 530, 112, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'RIGHT NOW?', 90, 670, 140, CRED, pr(t, S['t0'] + 0.3, 0.4))
    kc = pr(t, S['t0'] + 0.3, 0.5)
    coin(c, 540, 1010 + 10 * math.sin(t * 2), 420 * eback(cl(kc), 1.5), rot=4 * math.sin(t), a=kc)
    burst(c, 230, 1250, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
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
    dict(k='what', t0=ph("here's what happened") - 0.2, fn=with_subs(sc_what), tin='whip'),
    dict(k='lever', t0=ph("and here's what makes") - 0.2, fn=with_subs(sc_lever), tin='zoom'),
    dict(k='y2022', t0=ph("but we've seen") - 0.2, fn=with_subs(sc_2022), tin='wipe', col=SEPIA),
    dict(k='back', t0=ph('and yet bitcoin') - 0.2, fn=with_subs(sc_back), tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('almost half'), 10, 0.3)
EP.shk(ph('collapsed in a matter'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
