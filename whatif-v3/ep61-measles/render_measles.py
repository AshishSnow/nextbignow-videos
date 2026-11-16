"""NextBigNow ep 61 (classic red/cream comic, real photo cut-outs, small subtitles, v5 voice, logo watermark): What if measles moved back into America?
Facts: PAHO revoked US measles elimination status (review Nov 10-13, 2026; reported Nov 13-14). Elimination = no continuous chain for 12 months.
CDC: 5,412 cases in 2026 as of Nov 12 (PA 1,529); 2,289 in 2025; 285 in 2024; 10 deaths in 2026 (National Desk / Healio; infants in WI, NY, PA).
KFF/CDC: kindergarten 2-dose MMR 92.4% (2025-26), 95% target, only 10 states at/above 95%; US declared eliminated in 2000;
NYC 2019: ~60,000 MMR doses, transmission interrupted. PAHO: Canada lost status Nov 2025. Measles virus stays airborne up to 2 hours (CDC).
Photos (Wikimedia Commons): see measles/img/credits.json. No brand logos shown."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('MS_DIR', 'measles'))
PK.IMG = os.path.join(HERE, 'measles', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))
PLAT = os.environ.get('PLAT', 'ig')
SUBY = 1530 if PLAT == 'yt' else 1442


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


def virus(c, x, y, w, t, k=1.0, rot0=0.0):
    """the real (TEM) measles particle as a comic sticker, slowly turning."""
    if k <= 0: return
    place(c, 'V1_cut_comic.png', x, y, w * eback(cl(k), 1.5), rot=rot0 + 6 * math.sin(t * 1.3), a=cl(k * 2), shadow=True)


def stamp(c, s, x, y, size, col, k, rot=-8):
    """rubber stamp: ink box + letters, slams in."""
    if k <= 0: return
    sc = 1.0 + 0.6 * (1 - eo(cl(k)))
    tw_ = width(s, 'SpecialElite.ttf', size)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    a = cl(k * 2)
    c.drawRect(R.MakeXYWH(-tw_ * 0.6 - 30, -size * 0.95, tw_ * 1.2 + 60, size * 1.45), stroke(col, 9, a=a))
    c.drawString(s, -tw_ * 0.55, size * 0.18, font('SpecialElite.ttf', size), paint(col, a))
    c.restore()


def strike(c, x0, y0, x1, y1, k, col=CRED, wdt=16):
    if k <= 0: return
    kk = eo(cl(k))
    c.drawLine(x0, y0, lerp(x0, x1, kk), lerp(y0, y1, kk), stroke(KINK, wdt + 8))
    c.drawLine(x0, y0, lerp(x0, x1, kk), lerp(y0, y1, kk), stroke(col, wdt))


def chain(c, x, y, w, t, t0, dur, n=12):
    """12 months, one chain: links light up one by one."""
    gap = w / n
    for i in range(n):
        kk = pr(t, t0 + dur * i / n, 0.25)
        cx = x + gap * (i + 0.5)
        r = gap * 0.42
        rr = skia.RRect.MakeRectXY(R.MakeXYWH(cx - r, y - r * 0.62, 2 * r, 1.24 * r), r * 0.6, r * 0.6)
        c.drawRRect(rr, stroke(KINK, 14))
        if kk > 0: c.drawRRect(rr, stroke(CRED, 8 * kk))
        lab = str(i + 1)
        if kk > 0.5: c.drawString(lab, cx - width(lab, 'SpecialElite.ttf', 24) / 2, y + r + 34, font('SpecialElite.ttf', 24), paint(KINK))


def gauge(cc, w, h, k, t, t92, t95):
    """horizontal fill bar: 92.4% now vs 95% line."""
    x0, y0, bw, bh = 50, 150, w - 100, 120
    cc.drawRect(R.MakeXYWH(x0 + 10, y0 + 10, bw, bh), paint(KINK))
    cc.drawRect(R.MakeXYWH(x0, y0, bw, bh), paint(PAPER))
    # scale 80..100 so the gap is visible
    fx = lambda v: x0 + (v - 80) / 20 * bw
    kk = pr(t, t92 - 0.3, 1.0)
    cc.drawRect(R.MakeLTRB(x0, y0, lerp(x0, fx(92.4), eo(kk)), y0 + bh), paint(CBLU))
    dots(cc, (x0, y0, lerp(0, fx(92.4) - x0, eo(kk)), bh), KINK, cell=14, rmax=3.2, grad=(0.0, 1.0), a=0.3)
    cc.drawRect(R.MakeXYWH(x0, y0, bw, bh), stroke(KINK, 7))
    k5 = pr(t, t95 - 0.3, 0.4)
    if k5 > 0:
        X = fx(95)
        cc.drawLine(X, y0 - 40, X, y0 + bh + 40, stroke(CRED, 12 * k5))
        title(cc, '95% NEEDED', X, y0 - 56, 44, CRED, k5, 'c', shadow=4)
    if kk > 0.7: title(cc, '92.4%', fx(92.4) - 110, y0 + bh + 92, 64, CBLU, 1.0, 'c', shadow=5)
    for v in (80, 90, 100):
        s = '%d%%' % v
        cc.drawString(s, fx(v) - width(s, 'SpecialElite.ttf', 22) / 2 if v > 80 else fx(v), y0 + bh + 150 if v != 90 else y0 + bh + 150, font('SpecialElite.ttf', 22), paint(KINK))


def sc_hook(c, t, S):
    t26 = ph('twenty six years ago'); tm = ph('moved back in'); tw = ph('this week it did')
    paper(c, t)
    # visual first: the real particle crashes in
    virus(c, 540, 950, 700, t, pr(t, 0.0, 0.5), rot0=-8)
    caption(c, 'MEASLES VIRUS . UNDER A MICROSCOPE', 240, 1335, pr(t, 0.4, 0.3), col=CYEL, size=24, rot=1.5)
    stamp(c, 'ELIMINATED 2000', 540, 520, 64, CBLU, pr(t, t26 - 0.6, 0.35), rot=-6)
    strike(c, 220, 560, 860, 440, pr(t, tm - 0.4, 0.3))
    if t > tm - 0.1: burst(c, 760, 690, 150, "IT'S BACK!", pr(t, tm - 0.1, 0.35), size=44, rot=8)
    credit(c, 'V1_virus')


def sc_status(c, t, S):
    tp = ph('pan american'); tl = ph('lost its measles'); tr = ph('the rule is simple'); t12 = ph('twelve straight months'); tn = ph('not eliminated anymore')
    if t < tr - 0.3:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'NOVEMBER 2026', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
        title(c, 'U.S. MEASLES', 90, 540, 120, PAPER, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'STATUS:', 90, 680, 130, CYEL, pr(t, tl - 0.4, 0.4))
        title(c, 'LOST.', 90, 840, 190, PAPER, pr(t, tl, 0.4), rot=-3)
        caption(c, 'PAN AMERICAN HEALTH ORGANIZATION', 140, 960, pr(t, tp, 0.3), col=CYEL, size=28, rot=-1.5)
        virus(c, 540 + 220 * pr(t, tl, 0.6), 1150 + 30 * pr(t, tl, 0.6), 520 - 180 * pr(t, tl, 0.6), t, pr(t, S['t0'] + 0.3, 0.5), rot0=12)
        return
    paper(c, t)
    caption(c, 'THE RULE', LX, 340, pr(t, tr - 0.2, 0.3), col=CCYN, size=30)
    title(c, 'ONE CHAIN.', 90, 540, 150, CBLU, pr(t, tr, 0.4))
    title(c, '12 MONTHS.', 90, 700, 150, CRED, pr(t, t12 - 0.3, 0.4), rot=-2)
    if t > tr - 0.1: chain(c, 90, 960, 900, t, t12 - 0.3, 1.4)
    if t > tn - 0.3: burst(c, 540, 1220, 160, 'NOT ELIMINATED', pr(t, tn - 0.3, 0.35), size=36, col=CYEL, txt=CRED, rot=-5)


def sc_jump(c, t, S):
    t24 = ph('twenty twenty four'); t25 = ph('twenty twenty five'); ty = ph('this year more than'); tpa = ph('pennsylvania alone'); td = ph('ten people have died'); tb = ph('too young for the shot')
    paper(c, t)
    caption(c, 'LOOK AT THE JUMP', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tpa - 0.3:
        title(c, 'U.S. CASES', 90, 540, 150, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 640), paint(PAPER))
            k = 0.0
            if t > t24 - 0.3: k = 0.34 * pr(t, t24 - 0.3, 0.6)
            if t > t25 - 0.3: k = 0.34 + 0.33 * pr(t, t25 - 0.3, 0.6)
            if t > ty - 0.1: k = 0.67 + 0.33 * pr(t, ty - 0.1, 0.8)
            bars(cc, 90, 130, 720, 380, [('2024', 285, '285', CCYN), ('2025', 2289, '2,289', CYEL), ('2026', 5412, '5,400+', CRED)], k, 5800)
            cc.drawString('CONFIRMED MEASLES CASES . CDC (2026 AS OF NOV 12)', 30, 620, font('SpecialElite.ttf', 21), paint(KINK))
        panel(c, 90, 640, 900, 640, rot=1.0, k=pr(t, S['t0'] + 0.3, 0.5), draw=dr)
        if t > ty + 0.6: burst(c, 330, 820, 100, 'x19!', pr(t, ty + 0.6, 0.35), size=58, rot=8)
        return
    title(c, 'PENNSYLVANIA:', 80, 540, 116, CBLU, pr(t, tpa - 0.3, 0.4))
    title(c, '1,500+ CASES', 80, 690, 130, CRED, pr(t, tpa + 0.3, 0.4), rot=-2)
    photo_panel(c, 'V7_philly', 90, 780, 900, 420, 1.2, pr(t, tpa - 0.1, 0.5), t=t - tpa)
    caption(c, 'PHILADELPHIA', 150, 1170, pr(t, tpa + 0.4, 0.3), col=CYEL, size=26)
    credit(c, 'V7_philly')
    if t > td - 0.3:
        mini(c, 520, 1060, 440, 240, 2.5, pr(t, td - 0.3, 0.4), 'DEATHS IN 2026', '10', CRED, bigsize=110)
    if t > tb - 0.3: caption(c, 'INCLUDING BABIES TOO YOUNG FOR THE SHOT', 110, 1320, pr(t, tb - 0.3, 0.3), col=PAPER, size=26, rot=-1)


def sc_why(c, t, S):
    tc = ph('most contagious'); ta = ph('hang in the air'); t2 = ph('up to two hours'); t95 = ph('ninety five percent'); t92 = ph('ninety two point four'); t10 = ph('only ten states')
    paper(c, t)
    caption(c, 'WHY SO HARD TO STOP?', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < t95 - 0.4:
        title(c, 'IT STAYS IN', 90, 540, 140, CBLU, pr(t, tc - 0.3, 0.4))
        title(c, 'THE AIR.', 90, 690, 150, CRED, pr(t, ta - 0.3, 0.4), rot=-2)
        photo_panel(c, 'V2_room', 90, 780, 900, 540, 1.2, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        # drifting particles filling the room
        kk = pr(t, ta - 0.2, 1.2)
        for i in range(9):
            if kk <= 0: break
            px = 200 + (i * 97) % 700 + 25 * math.sin(t * 1.1 + i)
            py = 900 + (i * 61) % 360 + 18 * math.cos(t * 0.9 + i * 2)
            place(c, 'V1_cut_comic.png', px, py, 70 * kk, rot=t * 30 + i * 40, a=kk * 0.95, shadow=False)
        if t > t2 - 0.3: burst(c, 820, 840, 130, 'UP TO 2 HOURS', pr(t, t2 - 0.3, 0.35), size=32, rot=8)
        credit(c, 'V2_room')
        return
    title(c, 'KINDERGARTEN', 80, 530, 120, CBLU, pr(t, t95 - 0.4, 0.4))
    title(c, 'SHOT RATE', 90, 670, 130, CRED, pr(t, t95 - 0.1, 0.4), rot=-2)
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 470), paint(PAPER))
        gauge(cc, 900, 470, 1.0, t, t92, t95)
        cc.drawString('2-DOSE MMR, KINDERGARTEN 2025-26 . CDC', 30, 450, font('SpecialElite.ttf', 21), paint(KINK))
    panel(c, 90, 760, 900, 470, rot=-1.0, k=pr(t, t95 - 0.2, 0.5), draw=dr)
    if t > t10 - 0.3: caption(c, 'ONLY 10 STATES HIT 95%', 220, 1330, pr(t, t10 - 0.3, 0.3), col=CYEL, size=36, rot=-1.5)


def sc_canada(c, t, S):
    tc = ph('canada lost')
    paper(c, t, tint=SEPIA)
    caption(c, 'MEANWHILE, NEXT DOOR', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'CANADA LOST', 80, 540, 130, CRED, pr(t, tc - 0.2, 0.4))
    title(c, 'IT TOO.', 90, 690, 150, CBLU, pr(t, tc + 0.3, 0.4), rot=-2)
    photo_panel(c, 'V5_toronto', 90, 780, 900, 500, -1.2, pr(t, S['t0'] + 0.2, 0.5), t=t - S['t0'])
    burst(c, 820, 830, 120, 'NOV 2025', pr(t, tc + 0.6, 0.35), size=40, rot=8)
    caption(c, 'TORONTO', 150, 1240, pr(t, tc + 0.4, 0.3), col=CYEL, size=26)
    credit(c, 'V5_toronto')


def sc_comeback(c, t, S):
    t19 = ph('in twenty nineteen'); t60 = ph('sixty thousand'); ts = ph('stopped its outbreak')
    bg_flat(c, CBLU, (25, 90, 180))
    caption(c, 'THE COMEBACK STORY', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    title(c, 'NEW YORK, 2019', 80, 540, 120, PAPER, pr(t, t19 - 0.2, 0.4))
    photo_panel(c, 'V4_brooklyn', 90, 600, 900, 380, 1.0, pr(t, t19, 0.5), fy=0.55, t=t - t19)
    credit(c, 'V4_brooklyn', col=PAPER)
    if t > t60 - 0.4:
        title(c, '60,000', 90, 1150, 180, CYEL, pr(t, t60 - 0.4, 0.4), rot=-2)
        caption(c, 'MMR SHOTS IN A FEW MONTHS', 110, 1250, pr(t, t60 + 0.2, 0.3), col=PAPER, size=30, rot=1.5)
        for i in range(3):
            kk = pr(t, t60 + 0.15 * i, 0.4)
            if kk > 0: place(c, 'V6_cut_comic.png', 840 + 40 * i, 1180 - 60 * i, 220 * eback(cl(kk), 1.5), rot=-5 + 10 * i, a=kk, shadow=True)
    if t > ts - 0.3: burst(c, 760, 760, 140, 'OUTBREAK STOPPED', pr(t, ts - 0.3, 0.35), size=32, col=GRN, txt=PAPER, rot=-6)


def sc_ask(c, t, S):
    ty = ph('yes or no')
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'CAN AMERICA', 90, 530, 130, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'WIN IT BACK?', 80, 670, 130, CRED, pr(t, S['t0'] + 0.3, 0.4))
    virus(c, 540, 1010, 360, t, pr(t, S['t0'] + 0.3, 0.5))
    burst(c, 230, 1250, 100, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ty + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    cta = 'SUBSCRIBE FOR DAILY WHAT IFS' if PLAT == 'yt' else 'SEND THIS TO SOMEONE WHO NEEDS TO SEE IT'
    caption(c, cta, 170, 1375, pr(t, ty + 0.6, 0.3), col=CYEL, size=28, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='status', t0=ph('this week it did') - 0.15, fn=with_subs(sc_status), tin='flash'),
    dict(k='jump', t0=ph('look at the jump') - 0.2, fn=with_subs(sc_jump), tin='whip'),
    dict(k='why', t0=ph('why is it so hard') - 0.2, fn=with_subs(sc_why), tin='zoom'),
    dict(k='canada', t0=ph('canada lost') - 0.2, fn=with_subs(sc_canada), tin='whip'),
    dict(k='comeback', t0=ph('but there is a comeback') - 0.2, fn=with_subs(sc_comeback), tin='flash'),
    dict(k='ask', t0=ph('so what if america') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(0.15, 10, 0.3)
EP.shk(ph('moved back in'), 8, 0.25)

if __name__ == '__main__':
    EP.main(sys.argv)
