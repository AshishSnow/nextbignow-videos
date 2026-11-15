"""NextBigNow long-form (16:9, vintage comic + editorial, small subtitles, v5 voice): Social Security 2027 raise - how much your check really goes up.
Facts: SSA (14 Oct 2026) - 3.6% COLA for 2027; ~76M people (nearly 72M SS beneficiaries + ~7.3M SSI); SSI increase from 31 Dec 2026, SS from Jan 2027;
average retirement benefit +~$75/month; taxable max $184,500 -> $192,300; COLA notices online in my Social Security Message Center from late Nov
(paperless enrolment by 18 Nov), mailed early Dec. Yahoo Finance: average benefit ~$2,088; +$75/month ~ $900/yr; 2026 COLA 2.8%.
COLA history: 2023 8.7%, 2024 3.2%, 2025 2.5%, 2026 2.8%. CPI-W Q3 vs Q3. Payment days: 2nd/3rd/4th Wednesday by birth date (Jan 2027: 13/20/27).
Medicare Part B 2026 standard premium $202.90; 2027 Trustees projection ~$209.50 (CMS final usually mid-Nov). Hold-harmless provision.
2026 Trustees report (SSA, 9 Jun 2026): combined OASDI reserves through 2034, then 83% payable. Medicare open enrollment ends 7 Dec.
Photos (Wikimedia Commons): see cola/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CO_DIR', 'cola'))
PK.IMG = os.path.join(HERE, 'cola', 'img')
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


def credit(c, key, a=1.0, col=(120, 100, 70), y=900):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(70, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


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



TX = 110  # left text column


def head2(c, a, b, t, t0, ca=CBLU, cb=CRED, size=120, y=300):
    title(c, a, TX, y, size, ca, pr(t, t0, 0.4))
    title(c, b, TX, y + size + 20, size, cb, pr(t, t0 + 0.3, 0.4), rot=-1.5)


def row_card(c, x, y, w, h, k, left, right, col, lsize=44, rsize=64):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(PAPER))
        cc.drawRect(R.MakeXYWH(0, 0, 18, h), paint(col))
        title(cc, left, 44, h / 2 + lsize * 0.36, lsize, KINK, 1.0, shadow=0, outline=0.01)
        title(cc, right, w - 30, h / 2 + rsize * 0.36, rsize, col, 1.0, 'r', shadow=4)
    panel(c, x, y, w, h, rot=0, k=k, draw=dr, border=6, shadow=8)


def check_card(c, x, y, w, h, k, amt, t):
    """a comic benefit check (no real logos)"""
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint((225, 238, 222)))
        dots(cc, (0, 0, w, h), (120, 160, 120), cell=14, rmax=2.5, grad=(0.0, 1.0), a=0.35)
        cc.drawString('MONTHLY BENEFIT', 36, 60, font('SpecialElite.ttf', 30), paint(KINK))
        cc.drawString('PAY TO THE ORDER OF: YOU', 36, 120, font('SpecialElite.ttf', 26), paint(KINK))
        cc.drawLine(36, h - 70, w * 0.55, h - 70, stroke(KINK, 3))
        cc.drawString('JANUARY 2027', 36, h - 34, font('SpecialElite.ttf', 24), paint(KINK))
        cc.drawRect(R.MakeXYWH(w - 360, 70, 320, 110), paint(PAPER)); cc.drawRect(R.MakeXYWH(w - 360, 70, 320, 110), stroke(KINK, 4))
        title(cc, amt, w - 200, 152, 70, CRED, 1.0, 'c', shadow=0)
    panel(c, x, y, w, h, rot=-2, k=k, draw=dr, border=7, shadow=12)


def sc_hook(c, t, S):
    t76 = ph('seventy six million'); t36 = ph('three point six percent'); tg = ph('sounds great'); ts = ph('smaller than that'); th = ph('exactly how much'); tw = ph('when it hits'); tc = ph('the one thing')
    paper(c, t)
    caption(c, 'SOCIAL SECURITY . 2027 RAISE', TX, 120, 1.0, col=CYEL, size=30)
    title(c, '+3.6%', TX, 400, 260, GRN, 1.0, rot=-3)
    title(c, 'FOR ~76 MILLION', TX, 520, 70, CBLU, pr(t, t76 - 0.2, 0.4))
    title(c, 'AMERICANS', TX, 600, 70, CBLU, pr(t, t76 + 0.2, 0.4))
    k = pr(t, 0, 0.6)
    check_card(c, 1000, 200, 800, 380, k, '+$75' if t < ts - 0.4 else '+$68?', t)
    place(c, 'D4_dollar_comic.png', 1400, 760 + 8 * math.sin(t * 2), 620 * eback(cl(pr(t, 0.3, 0.6)), 1.4), rot=-8, a=pr(t, 0.3, 0.6), shadow=True)
    if t > ts - 0.4: burst(c, 900, 190, 110, 'SMALLER!', pr(t, ts - 0.4, 0.35), size=40, rot=8)
    for i, (t0, s_, col) in enumerate(((th, '1. HOW MUCH', CBLU), (tw, '2. WHEN IT HITS', GRN), (tc, '3. THE CATCH', CRED))):
        caption(c, s_, TX + 10, 700 + i * 70, pr(t, t0 - 0.2, 0.3), col=col if col != GRN else CYEL, size=30, rot=(-1.5, 1, -1)[i])
    credit(c, 'D4_dollar')


def sc_how(c, t, S):
    tc = ph('called cpi w'); tf = ph('food gas rent'); tj = ph('july august and september'); tl = ph('same three months'); tp = ph('prices were up'); tco = ph('cost of living adjustment'); tm = ph('call it the cola')
    paper(c, t)
    caption(c, 'WHERE DOES 3.6% COME FROM?', TX, 120, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    head2(c, 'IT FOLLOWS', 'PRICES.', t, S['t0'] + 0.3)
    if t > tc - 0.3: caption(c, 'THE INFLATION NUMBER: CPI-W', TX, 520, pr(t, tc - 0.3, 0.3), col=CYEL, size=32, rot=-1.5)
    photo_panel(c, 'L3_grocery', 1000, 170, 800, 460, 1.5, pr(t, tf - 0.5, 0.5), t=t - tf)
    if t > tf - 0.5: credit(c, 'L3_grocery')
    if t > tj - 0.3:
        for i, m in enumerate(('JUL', 'AUG', 'SEP')):
            mini(c, TX + i * 270, 620, 240, 170, (-2, 1, -1)[i], pr(t, tj - 0.2 + 0.3 * i, 0.35), '2026', m, (CBLU, CRED, CBLU)[i], bigsize=64)
    if t > tl - 0.2: caption(c, 'VS. THE SAME 3 MONTHS LAST YEAR', TX + 20, 860, pr(t, tl - 0.2, 0.3), col=PAPER, size=28, rot=-1)
    if t > tp - 0.2: burst(c, 1560, 760, 150, '+3.6%', pr(t, tp, 0.35), size=70, rot=8)
    if t > tm - 0.2: caption(c, 'COLA = COST-OF-LIVING ADJUSTMENT', 1020, 720, pr(t, tm - 0.2, 0.3), col=CYEL, size=26, rot=2)


def sc_dollars(c, t, S):
    ta = ph('average retired worker'); t75 = ph('about seventy five dollars'); t63 = ph('one hundred and sixty three'); t9 = ph('nine hundred extra'); tq = ph('quick way'); t1k = ph('one thousand dollars a month')
    t15 = ph('fifteen hundred'); t2k = ph('two thousand about'); t3k = ph('three thousand about'); tx = ph('multiply it by')
    paper(c, t)
    caption(c, 'IN REAL DOLLARS', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tq - 0.3:
        title(c, 'AVERAGE CHECK', TX, 290, 90, CBLU, pr(t, ta - 0.2, 0.4))
        title(c, '$2,088', TX, 470, 190, KINK if False else CBLU, pr(t, ta + 0.6, 0.4), rot=-2)
        if t > t63 - 0.3:
            title(c, '-> $2,163', TX + 40, 680, 150, GRN, pr(t, t63 - 0.3, 0.4), rot=-2)
        mini(c, 1060, 220, 700, 260, 2, pr(t, t75 - 0.2, 0.4), 'RAISE PER MONTH', '+$75', GRN, bigsize=130)
        mini(c, 1100, 540, 640, 240, -1.5, pr(t, t9 - 0.2, 0.4), 'RAISE PER YEAR', '+$900', CBLU, bigsize=120)
        return
    title(c, 'DO YOUR', TX, 300, 120, CBLU, pr(t, tq - 0.3, 0.4))
    title(c, 'OWN MATH:', TX, 440, 120, CRED, pr(t, tq, 0.4), rot=-1.5)
    if t > tx - 0.4:
        def dr(cc):
            cc.drawRect(R.MakeWH(720, 200), paint(CYEL))
            title(cc, 'CHECK x 0.036', 360, 125, 80, CRED, 1.0, 'c', shadow=4)
        panel(c, TX, 560, 720, 200, rot=-2, k=pr(t, tx - 0.4, 0.5), draw=dr)
    rows = ((t1k, '$1,000 / MONTH', '+$36'), (t15, '$1,500', '+$54'), (t2k, '$2,000', '+$72'), (t3k, '$3,000', '+$108'))
    for i, (t0, l, r_) in enumerate(rows):
        row_card(c, 1000, 190 + i * 165, 800, 130, pr(t, t0 - 0.3, 0.35), l, r_, (CBLU, GRN, CRED, CYEL)[i])


def calendar(c, x, y, w, h, k, t, hl):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(PAPER))
        cc.drawRect(R.MakeWH(w, 90), paint(CRED))
        title(cc, 'JANUARY 2027', w / 2, 66, 54, PAPER, 1.0, 'c', shadow=3)
        cw_, ch_ = w / 7, (h - 140) / 5
        for i, d in enumerate('SMTWTFS'):
            cc.drawString(d, i * cw_ + cw_ / 2 - 8, 126, font('SpecialElite.ttf', 26), paint(KINK))
        day = 1
        for r_ in range(5):
            for col in range(7):
                if r_ == 0 and col < 5: continue
                if day > 31: break
                cx_, cy_ = col * cw_, 140 + r_ * ch_
                on = day in hl and hl[day] <= t
                if on:
                    kk = pr(t, hl[day], 0.3)
                    cc.drawCircle(cx_ + cw_ / 2, cy_ + ch_ / 2, 36 * eback(kk, 1.6), paint(CYEL)); cc.drawCircle(cx_ + cw_ / 2, cy_ + ch_ / 2, 36 * eback(kk, 1.6), stroke(CRED, 5))
                s_ = str(day)
                cc.drawString(s_, cx_ + cw_ / 2 - width(s_, 'SpecialElite.ttf', 30) / 2, cy_ + ch_ / 2 + 10, font('SpecialElite.ttf', 30), paint(KINK))
                day += 1
    panel(c, x, y, w, h, rot=1.5, k=k, draw=dr, border=7, shadow=12)


def sc_when(c, t, S):
    tssi = ph('if you get ssi'); td31 = ph('december thirty first'); tj = ph('it starts in january'); tb = ph('depends on your birthday')
    t13 = ph('january thirteenth'); t20 = ph('january twentieth'); t27 = ph('january twenty seventh'); tl = ph('get a letter'); to = ph('shows up online'); tm = ph('in the mail')
    paper(c, t)
    caption(c, 'WHEN DOES IT HIT?', TX, 120, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tl - 0.3:
        head2(c, 'IT DEPENDS ON', 'YOUR BIRTHDAY.', t, tb - 0.4, size=96)
        if t > tssi - 0.2: caption(c, 'SSI: STARTS DEC 31', TX, 560, pr(t, tssi - 0.2, 0.3), col=CYEL, size=32, rot=-1.5)
        for i, (t0, a, b) in enumerate(((t13, 'BORN 1ST-10TH', 'JAN 13'), (t20, 'BORN 11TH-20TH', 'JAN 20'), (t27, 'BORN 21ST-31ST', 'JAN 27'))):
            row_card(c, TX, 630 + i * 110, 760, 92, pr(t, t0 - 0.6, 0.35), a, b, (CBLU, GRN, CRED)[i], lsize=36, rsize=52)
        calendar(c, 1060, 160, 720, 640, pr(t, tj - 0.4, 0.5), t, {13: t13, 20: t20, 27: t27})
        return
    head2(c, 'WATCH FOR', 'YOUR LETTER.', t, tl - 0.3, size=104)
    row_card(c, TX, 600, 780, 110, pr(t, to - 0.3, 0.35), 'ONLINE (MY SOCIAL SECURITY)', 'LATE NOV', CBLU, lsize=30, rsize=52)
    row_card(c, TX, 740, 780, 110, pr(t, tm - 0.3, 0.35), 'BY MAIL', 'EARLY DEC', CRED, lsize=36, rsize=52)
    photo_panel(c, 'L2_poster', 1180, 150, 520, 720, 2, pr(t, tl, 0.5), fy=0.4, t=t - tl)
    credit(c, 'L2_poster')


def sc_catch(c, t, S):
    tme = ph("if you're on medicare"); tst = ph('straight out of'); t202 = ph('two hundred and two dollars'); tup = ph('go up again'); t209 = ph('two hundred and nine fifty'); tmid = ph('mid november')
    tr = ph('real math'); t75 = ph('seventy five dollar raise'); t66 = ph('six sixty'); t68 = ph('sixty eight dollars'); tsr = ph('still a raise'); thh = ph('hold harmless')
    paper(c, t)
    caption(c, 'THE CATCH', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tr - 0.3:
        head2(c, 'MEDICARE', 'TAKES A BITE.', t, tme - 0.3, ca=CRED, cb=CBLU, size=110)
        photo_panel(c, 'L4_pharmacy', 1000, 160, 800, 420, -1.5, pr(t, tst - 0.4, 0.5), t=t - tst)
        if t > tst - 0.4: credit(c, 'L4_pharmacy')
        row_card(c, TX, 600, 820, 110, pr(t, t202 - 0.3, 0.35), 'PART B PREMIUM 2026', '$202.90', CBLU, lsize=34, rsize=56)
        row_card(c, TX, 740, 820, 110, pr(t, t209 - 0.4, 0.35), '2027 (PROJECTED)', '~$209.50', CRED, lsize=34, rsize=56)
        if t > tmid - 0.3: caption(c, 'OFFICIAL NUMBER: USUALLY MID-NOVEMBER', 1020, 680, pr(t, tmid - 0.3, 0.3), col=CYEL, size=24, rot=1.5)
        return
    if t < thh - 0.4:
        head2(c, 'THE REAL', 'MATH:', t, tr - 0.3, size=120)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
            lines = ((t75, 'RAISE', '+$75.00', GRN), (t66, 'PREMIUM JUMP', '-$6.60', CRED), (t68, 'REAL RAISE', '~$68', CBLU))
            for i, (t0, a, b, col) in enumerate(lines):
                kk = pr(t, t0 - 0.2, 0.35)
                if kk <= 0: continue
                y_ = 130 + i * 160
                if i == 2: cc.drawLine(40, y_ - 70, 860, y_ - 70, stroke(KINK, 6))
                title(cc, a, 50, y_, 56, KINK, kk, shadow=0, outline=0.01)
                title(cc, b, 860, y_, 90 if i == 2 else 74, col, kk, 'r', shadow=4)
        panel(c, 960, 200, 900, 560, rot=1.5, k=pr(t, tr, 0.5), draw=dr)
        if t > tsr - 0.2: caption(c, 'STILL A RAISE. JUST NOT THE HEADLINE.', TX, 640, pr(t, tsr - 0.2, 0.3), col=CYEL, size=28, rot=-1.5)
        return
    head2(c, 'GOOD NEWS:', '"HOLD HARMLESS"', t, thh - 0.4, ca=GRN, cb=CBLU, size=86)
    caption(c, 'A HIGHER PREMIUM CAN\'T SHRINK YOUR CHECK', TX, 600, pr(t, thh + 0.8, 0.3), col=CYEL, size=30, rot=-1.5)
    caption(c, '(FOR MOST PEOPLE)', TX + 40, 680, pr(t, thh + 1.6, 0.3), col=PAPER, size=26, rot=1)
    k = pr(t, thh, 0.5)
    c.save(); c.translate(1500, 470); s_ = eback(cl(k), 1.5); c.scale(s_, s_)
    sh = poly([(-200, -230), (200, -230), (200, 20), (0, 240), (-200, 20)], True)
    c.save(); c.translate(12, 12); c.drawPath(sh, paint(KINK)); c.restore()
    c.drawPath(sh, paint(GRN)); dots(c, (-200, -230, 400, 470), KINK, cell=16, rmax=3, grad=(0.3, 1.0), a=0.25); c.drawPath(sh, stroke(KINK, 9))
    title(c, 'YOUR', 0, -60, 70, PAPER, 1.0, 'c', shadow=4); title(c, 'CHECK', 0, 30, 80, PAPER, 1.0, 'c', shadow=4)
    c.restore()


def sc_history(c, t, S):
    t87 = ph('eight point seven'); t32 = ph('three point two'); t25 = ph('two point five'); t28 = ph('then two point eight'); tb = ph('biggest raise since')
    tp = ph('the problem a lot'); tw = ph('working people'); th = ph('housing and health care'); tf = ph('rise faster'); ts = ph('feel smaller')
    paper(c, t)
    caption(c, 'IS 3.6% A LOT?', TX, 120, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tp - 0.3:
        head2(c, 'COLA', 'BY YEAR', t, S['t0'] + 0.2, size=120)
        def dr(cc):
            cc.drawRect(R.MakeWH(1100, 700), paint(PAPER))
            items = [('2023', 8.7, '8.7%', CRED), ('2024', 3.2, '3.2%', CBLU), ('2025', 2.5, '2.5%', CBLU), ('2026', 2.8, '2.8%', CBLU), ('2027', 3.6, '3.6%', GRN)]
            bars(cc, 60, 120, 980, 440, items, pr(t, t87 - 0.4, (tb + 0.4) - (t87 - 0.4)), 10)
            cc.drawString('SOCIAL SECURITY COST-OF-LIVING ADJUSTMENTS', 40, 680, font('SpecialElite.ttf', 24), paint(KINK))
        panel(c, 720, 150, 1100, 700, rot=1.0, k=pr(t, t87 - 0.6, 0.5), draw=dr)
        if t > t87: burst(c, 380, 690, 160, 'BIGGEST IN 40 YEARS', pr(t, t87 + 0.6, 0.35), size=30, rot=-6)
        if t > tb - 0.2: caption(c, 'BIGGEST SINCE 2023', TX, 860, pr(t, tb - 0.2, 0.3), col=CYEL, size=30, rot=-1)
        return
    head2(c, 'BUT RETIREES', 'SPEND DIFFERENT.', t, tp - 0.3, size=96)
    mini(c, TX, 560, 420, 250, -2, pr(t, tw - 0.3, 0.4), 'CPI-W TRACKS', 'WORKERS', CBLU, bigsize=60)
    mini(c, TX + 460, 580, 420, 250, 1.5, pr(t, th - 0.4, 0.4), 'RETIREES SPEND ON', 'HOUSING + HEALTH', CRED, bigsize=40)
    photo_panel(c, 'L4_pharmacy', 1080, 170, 720, 440, 1.5, pr(t, th, 0.5), zoom=1.3, t=t - th)
    if t > ts - 0.3: burst(c, 1450, 760, 130, 'FEELS SMALLER', pr(t, ts - 0.3, 0.35), size=34, rot=6)


def sc_workers(c, t, S):
    tw = ph('this one is for workers'); tl = ph('up to a limit'); t184 = ph('one hundred eighty four thousand'); t192 = ph('one hundred ninety two thousand'); tm = ph('earn more than that')
    paper(c, t)
    caption(c, 'IF YOU STILL WORK', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    head2(c, 'THE TAX CAP', 'GOES UP.', t, tw - 0.3, size=120)
    caption(c, 'SOCIAL SECURITY TAX APPLIES UP TO A LIMIT', TX, 600, pr(t, tl - 0.2, 0.3), col=CYEL, size=28, rot=-1.5)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 620), paint(PAPER))
        bars(cc, 150, 140, 600, 360, [('2026', 184.5, '$184,500', CBLU), ('2027', 192.3, '$192,300', CRED)], pr(t, t184 - 0.4, (t192 + 0.8) - (t184 - 0.4)), 230)
        cc.drawString('TAXABLE MAXIMUM (SSA)', 40, 600, font('SpecialElite.ttf', 24), paint(KINK))
    panel(c, 920, 170, 900, 620, rot=1.0, k=pr(t, tl, 0.5), draw=dr)


def sc_fund(c, t, S):
    tj = ph('in june'); t34 = ph('twenty thirty four'); t83 = ph('eighty three percent'); ty = ph('years away'); t83y = ph('back in nineteen eighty three'); tm = ph('months before'); tr = ph('every raise matters')
    paper(c, t, tint=SEPIA)
    caption(c, 'THE BIG ONE', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < t83y - 0.3:
        head2(c, 'TRUST FUNDS', 'RUN DRY: 2034', t, tj - 0.2, size=104)
        mini(c, TX, 580, 460, 260, -2, pr(t, t83 - 0.3, 0.4), 'THEN PAYABLE (IF NO FIX)', '83%', CRED, bigsize=110)
        k = pr(t, S['t0'] + 0.3, 0.6)
        place(c, 'S6_dome_cut.png', 1400, 520 + 6 * math.sin(t * 2), 760 * eback(cl(k), 1.3), rot=-2, a=k, shadow=True)
        if t > ty - 0.3: caption(c, 'STILL YEARS AWAY', 1180, 880, pr(t, ty - 0.3, 0.3), col=CYEL, size=28, rot=-2)
        credit(c, 'S6_dome')
        return
    head2(c, '1983:', 'FIXED IN TIME.', t, t83y - 0.3, size=120)
    caption(c, 'A DEAL, MONTHS BEFORE THE MONEY RAN SHORT', TX, 600, pr(t, tm - 0.3, 0.3), col=CYEL, size=28, rot=-1.5)
    photo_panel(c, 'L1_ssa', 1000, 170, 820, 520, 1.5, pr(t, t83y, 0.5), t=t - t83y)
    if t > tr - 0.3: burst(c, 1500, 800, 140, 'EVERY $ MATTERS', pr(t, tr - 0.3, 0.35), size=32, rot=6)
    credit(c, 'L1_ssa')


def sc_todo(c, t, S):
    tf = ph('first look for'); ts = ph('second when you budget'); tt = ph('and third'); tdec = ph('december seventh')
    paper(c, t)
    caption(c, 'WHAT TO DO NOW', TX, 120, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    head2(c, 'YOUR 3-STEP', 'CHECKLIST', t, S['t0'] + 0.2, size=92)
    items = ((tf, '1', 'CHECK YOUR COLA LETTER', 'LATE NOV / EARLY DEC', CBLU), (ts, '2', 'BUDGET THE REAL RAISE', 'AFTER MEDICARE', GRN), (tt, '3', 'COMPARE MEDICARE PLANS', 'BY DEC 7', CRED))
    for i, (t0, n, a, b, col) in enumerate(items):
        kk = pr(t, t0 - 0.2, 0.4)
        if kk <= 0: continue
        def dr(cc, a=a, b=b, col=col, n=n):
            cc.drawRect(R.MakeWH(1080, 170), paint(PAPER))
            cc.drawRect(R.MakeWH(170, 170), paint(col)); title(cc, n, 85, 120, 120, PAPER, 1.0, 'c', shadow=4)
            title(cc, a, 200, 80, 56, KINK, 1.0, shadow=0, outline=0.01)
            cc.drawString(b, 204, 138, font('SpecialElite.ttf', 30), paint(col))
        panel(c, 760, 300 + i * 200, 1060, 170, rot=(-1, 1, -0.5)[i], k=kk, draw=dr, border=7, shadow=10)
        # tick
        if t > t0 + 1.2:
            kt = pr(t, t0 + 1.2, 0.3)
            p = skia.Path(); p.moveTo(1720, 385 + i * 200); p.lineTo(1745, 410 + i * 200); p.lineTo(1790, 345 + i * 200)
            c.drawPath(p, stroke(GRN, 14 * kt))


def sc_end(c, t, S):
    t36 = ph('about three point six percent'); t75 = ph('about seventy five dollars or'); t68 = ph('closer to sixty eight'); tw = ph("not a windfall"); ta = ph('and tell me'); ty = ph('yes or no'); tv = ph('whole video')
    if t < ta - 0.2:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'THE BOTTOM LINE', TX, 120, pr(t, S['t0'], 0.3), col=PAPER, size=30)
        title(c, '+3.6%', TX, 380, 220, CYEL, pr(t, t36 - 0.3, 0.4), rot=-3)
        mini(c, 1000, 180, 380, 240, -2, pr(t, t75 - 0.3, 0.4), 'HEADLINE', '+$75', CBLU, bigsize=100)
        mini(c, 1420, 200, 380, 240, 1.5, pr(t, t68 - 0.3, 0.4), 'AFTER MEDICARE', '~$68', GRN, bigsize=100)
        caption(c, 'REAL MONEY. BIGGEST SINCE 2023.', TX, 560, pr(t, t68 + 1.2, 0.3), col=PAPER, size=34, rot=-1.5)
        if t > tw - 0.4: burst(c, 1400, 700, 160, 'NOT A WINDFALL', pr(t, tw - 0.4, 0.35), size=36, col=CYEL, txt=CRED, rot=6)
        return
    paper(c, t)
    caption(c, 'YOUR TURN!', TX, 120, pr(t, ta, 0.3), size=30)
    head2(c, 'IS 3.6%', 'ENOUGH?', t, ta + 0.1, size=150)
    check_card(c, 1000, 200, 800, 380, pr(t, ta + 0.2, 0.5), '+3.6%', t)
    burst(c, 1150, 760, 110, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=60)
    burst(c, 1650, 760, 110, 'NO', pr(t, ty + 0.2, 0.35), col=CRED, txt=CYEL, size=64)
    if t > tv - 0.6: caption(c, 'WATCH NEXT: WHAT IF SOCIAL SECURITY RUNS DRY?', TX, 640, pr(t, tv - 0.6, 0.3), col=CYEL, size=28, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(W / 2, H / 2, 1300 * eio(k2), paint(CRED))


SUBY = 975


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY, size=34)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='how', t0=ph('first where does') - 0.2, fn=with_subs(sc_how), tin='whip'),
    dict(k='dollars', t0=ph('now what does that mean') - 0.2, fn=with_subs(sc_dollars), tin='zoom'),
    dict(k='when', t0=ph('so when does the money') - 0.2, fn=with_subs(sc_when), tin='whip'),
    dict(k='catch', t0=ph("but now here's the catch") - 0.2, fn=with_subs(sc_catch), tin='flash'),
    dict(k='history', t0=ph('so is three point six percent a lot') - 0.2, fn=with_subs(sc_history), tin='zoom'),
    dict(k='workers', t0=ph("there's one more number") - 0.2, fn=with_subs(sc_workers), tin='whip'),
    dict(k='fund', t0=ph("and we can't talk") - 0.2, fn=with_subs(sc_fund), tin='wipe', col=SEPIA),
    dict(k='todo', t0=ph('so what should you actually') - 0.2, fn=with_subs(sc_todo), tin='zoom'),
    dict(k='end', t0=ph("so here's the bottom line") - 0.2, fn=with_subs(sc_end), tin='flash'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('sixty eight dollars'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
