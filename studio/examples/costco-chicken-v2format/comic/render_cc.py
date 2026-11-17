"""OopsMyBusiness Short v2 format — Costco's $4.99 rotisserie chicken. CREAM comic paper + black/yellow accents, real cut-outs in
every scene, always moving (owner 17 Nov). Facts: ../SOURCES.md. Photos: cc/img/credits.json. No logos/trade dress; no likenesses."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'cc')
PK.IMG = os.path.join(D, 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))
CRED_J = json.load(open(os.path.join(PK.IMG, 'credits.json')))
YEL = (255, 214, 0); CHAR = (26, 26, 30); CHAR_D = (48, 48, 56); CREAM = (252, 241, 210)


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z0-9']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 1.6
LX = 90


PLAT = os.environ.get('OMB_PLAT', 'ig')   # 'ig' = Instagram Reels, 'yt' = YouTube Shorts
# YouTube Shorts covers more of the frame (owner's screenshot 15 Nov: channel row/title/Promote pill start ~y1380-1530 of 1920,
# right action column from ~y950 at x>900, phones crop ~60 px per side). So the YT cut scales the whole layout into the safe box.
if PLAT == 'yt':
    LAY = skia.Matrix(); LAY.setScaleTranslate(0.85, 0.85, 450 - 450 * 0.85, 250 - 250 * 0.85); SUB_Y = 1320
else:
    LAY = skia.Matrix(); SUB_Y = 1442
LAY_INV = skia.Matrix(); LAY.invert(LAY_INV)


def full(c, fn):
    """draw a background in frame space, cancelling the platform layout scale."""
    c.save(); c.concat(LAY_INV); fn(); c.restore()


def credit(c, key, a=1.0, y=1400):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s . WIKIMEDIA COMMONS' % (cr['author'], cr['license'])).upper()[:78]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, (150, 150, 150), a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0, after=None):
    def dr(cc):
        cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.012 * t, fx, fy)
        if after: after(cc)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=KINK, bigsize=54, headc=KINK):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.18)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(headc))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def tv(c, x, y, w, h, k, t, key=None, rot=-2, screen=None):
    """boxy vintage TV (drawn) with a photo or drawing on its screen."""
    if k <= 0: return
    sc = eback(cl(k), 2.0)
    c.save(); c.translate(x + w / 2, y + h / 2); c.rotate(rot); c.scale(sc, sc); c.translate(-w / 2, -h / 2)
    body = skia.RRect.MakeRectXY(R.MakeXYWH(0, 0, w, h), 40, 40)
    c.save(); c.translate(16, 16); c.drawRRect(body, paint(KINK)); c.restore()
    c.drawRRect(body, paint((70, 58, 48))); dots(c, (0, 0, w, h), KINK, cell=16, rmax=3, a=0.3); c.drawRRect(body, stroke(KINK, 10))
    sw, sh = w - 220, h - 80
    scr = skia.RRect.MakeRectXY(R.MakeXYWH(40, 40, sw, sh), 50, 50)
    c.save(); c.clipRRect(scr, doAntiAlias=True)
    c.drawRect(R.MakeXYWH(40, 40, sw, sh), paint((40, 44, 40)))
    if key: cover(c, img(key + '_comic.png'), 40, 40, sw, sh, 1.08 + 0.01 * t, 0.5, 0.5)
    if screen: c.save(); c.translate(40, 40); screen(c, sw, sh); c.restore()
    for i in range(0, int(sh), 8): c.drawRect(R.MakeXYWH(40, 40 + i, sw, 3), paint((0, 0, 0), 0.12))
    c.restore(); c.drawRRect(scr, stroke(KINK, 10))
    for i, yy in enumerate((h * 0.3, h * 0.55)):
        c.drawCircle(w - 90, yy, 34, paint(YEL)); c.drawCircle(w - 90, yy, 34, stroke(KINK, 7))
        c.drawLine(w - 90, yy, w - 90 + 24 * math.cos(t * 2 + i), yy + 24 * math.sin(t * 2 + i), stroke(KINK, 6))
    for i in range(5): c.drawLine(w - 130, h * 0.72 + i * 16, w - 50, h * 0.72 + i * 16, stroke(KINK, 5))
    c.drawLine(w * 0.25, h, w * 0.18, h + 60, stroke(KINK, 12)); c.drawLine(w * 0.75, h, w * 0.82, h + 60, stroke(KINK, 12))
    c.drawLine(w * 0.35, 0, w * 0.22, -90, stroke(KINK, 7)); c.drawLine(w * 0.45, 0, w * 0.58, -100, stroke(KINK, 7))
    c.restore()


def quote(c, x, y, w, h, rot, k, lines, who):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(CREAM))
        title(cc, '“', 18, 110, 120, YEL, 1.0, shadow=4)
        for i, s in enumerate(lines): cc.drawString(s, 70, 80 + i * 56, font('SpecialElite.ttf', 40), paint(KINK))
        cc.drawString(who, 70, h - 30, font('SpecialElite.ttf', 24), paint((110, 100, 90)))
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def bgp(c, t=0.0):
    full(c, lambda: paper(c, t))


def floaty(t, sp=1.0, amp=10):
    return amp * math.sin(t * 1.6 * sp), 2.0 * math.sin(t * 1.1 * sp + 1)


def stick(c, key, cx, cy, w, k, t, rot=0.0, sp=1.0, amp=10, shadow=True):
    """sticker cut-out that pops in (k) and keeps floating."""
    if k <= 0: return
    dy, dr = floaty(t, sp, amp)
    s = eback(cl(k), 2.2)
    place(c, key + '_cut.png', cx, cy + dy + 60 * (1 - eo(cl(k))), w * s, rot + dr, a=cl(k * 1.6), shadow=shadow)


def tag(c, x, y, s, k, t, rot=-8, col=YEL, txt=KINK, size=110, sub=None, swing=True):
    """swinging yellow price tag with a string."""
    if k <= 0: return
    f = font('LuckiestGuy.ttf', size); w = f.measureText(s) + 110; h = size * 1.5
    sc = eback(cl(k), 2.2)
    c.save(); c.translate(x, y); c.rotate(rot + (4 * math.sin(t * 2.2) if swing else 0)); c.scale(sc, sc)
    p = poly([(0, 0), (60, -h / 2), (w, -h / 2), (w, h / 2), (60, h / 2)])
    c.save(); c.translate(12, 12); c.drawPath(p, paint(KINK)); c.restore()
    c.drawPath(p, paint(col)); dots(c, (0, -h / 2, w, h), KINK, cell=14, rmax=3, a=0.15); c.drawPath(p, stroke(KINK, 8))
    c.drawCircle(42, 0, 13, paint(CREAM)); c.drawCircle(42, 0, 13, stroke(KINK, 6))
    c.drawString(s, 80, size * 0.36, f, paint(txt))
    if sub: c.drawString(sub, 82, h / 2 - 14, font('SpecialElite.ttf', 26), paint(KINK))
    c.restore()


def two(c, a1, a2, y, k1, k2, s1=118, s2=128, rot=-2):
    title(c, a1, 540, y, s1, CHAR, k1, 'c', outline=0.01, shadow=0, rot=rot)
    title(c, a2, 540, y + s2 * 1.1, s2, YEL, k2, 'c', rot=rot)


# ------------------------------------------------------------------ scenes
def sc_hook(c, t, S):
    tm = ph('millions of dollars'); tp = ph('on purpose'); ts = ph('true story')
    bgp(c, t)
    caption(c, 'TRUE STORY', LX, 300, 1.0 if t < 0.3 else pr(t, ts - 0.2, 0.3) if t > ts - 0.2 else 1.0, col=YEL, size=36)
    two(c, 'THE $5 CHICKEN', 'THAT COSTS MILLIONS', 470, 1.0, 1.0, 112, 96)
    c.drawCircle(540, 960, 330 + 8 * math.sin(t * 2), paint(YEL))
    dots(c, (210, 630, 660, 660), (230, 180, 0), cell=18, rmax=5, a=0.5)
    stick(c, 'chicken', 540, 970, 720, 1.0, t, rot=-4)
    tag(c, 640, 1190, '$4.99', 1.0, t, rot=-10, size=96)
    if t > tm - 0.2: burst(c, 850, 700, 175, '-$ MILLIONS', pr(t, tm - 0.2, 0.35), size=40, col=KINK, txt=YEL, rot=10)
    if t > tp - 0.2:
        k = pr(t, tp - 0.2, 0.3); c.save(); c.translate(300, 760); c.rotate(-14); sc = 1.6 - 0.6 * eback(cl(k), 2.0); c.scale(sc, sc)
        f = font('LuckiestGuy.ttf', 74); tw = f.measureText('ON PURPOSE')
        c.drawRect(R.MakeXYWH(-tw / 2 - 20, -70, tw + 40, 100), stroke(CHAR, 10)); c.drawString('ON PURPOSE', -tw / 2, 6, f, paint(CHAR)); c.restore()
    credit(c, 'chicken')


def sc_price(c, t, S):
    t0 = S['t0']; ty = ph('since two thousand nine'); to = ph('other stores'); td = ph("didn't move")
    bgp(c, t)
    caption(c, 'THE PRICE THAT NEVER MOVES', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    # year belt sliding left forever: flowing motion
    yr0 = 2009 + int(cl((t - ty) / 2.4) * 16) if t > ty else 2009
    c.save(); c.translate(0, 470)
    off = (t - t0) * 160
    for i in range(-2, 22):
        x = 120 + i * 230 - off % 230
        yy = 2009 + i + int(off // 230)
        if yy > 2025 or yy < 2009: continue
        c.drawRect(R.MakeXYWH(x, -60, 200, 110), paint(CREAM)); c.drawRect(R.MakeXYWH(x, -60, 200, 110), stroke(KINK, 6))
        c.drawString(str(yy), x + 30, 20, font('LuckiestGuy.ttf', 64), paint(CHAR))
    c.restore()
    stick(c, 'chicken', 360, 900, 520, pr(t, t0 + 0.1, 0.4), t, rot=-6)
    tag(c, 560, 860, '$4.99', pr(t, t0 + 0.3, 0.4), t, rot=-6, size=120, sub='SINCE 2009')
    if t > to - 0.3:
        tag(c, 560, 1130, '$5.99', pr(t, to - 0.3, 0.4), t, rot=8, col=(205, 205, 210), size=90, sub='OTHER STORES')
    if t > td - 0.3:
        title(c, "COSTCO DIDN'T MOVE.", 540, 1350, 74, YEL, pr(t, td - 0.3, 0.35), 'c', rot=-2)
    credit(c, 'chicken')


def sc_cfo(c, t, S):
    t0 = S['t0']; tm = ph('thirty to forty'); tk = ph('keep that price')
    bgp(c, t)
    caption(c, '2015 . COSTCO EARNINGS CALL', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    c.drawCircle(540, 600, 250 + 8 * math.sin(t * 2), paint(YEL, pr(t, t0, 0.3)))
    stick(c, 'chicken', 540, 600, 520, pr(t, t0 + 0.1, 0.4), t, rot=6)
    tag(c, 640, 760, '$4.99', pr(t, t0 + 0.3, 0.4), t, rot=-8, size=80)
    credit(c, 'chicken')
    def dr(cc):
        w, h = 860, 420
        cc.drawRect(R.MakeWH(w, h), paint(CREAM))
        title(cc, '“', 18, 120, 130, YEL, 1.0, shadow=4)
        for i, s_ in enumerate(['...we were willing to eat,', 'if you will, $30 to $40 million', 'a year in gross margin by', 'keeping it at $4.99.']):
            cc.drawString(s_, 80, 90 + i * 64, font('SpecialElite.ttf', 44), paint(KINK))
        cc.drawString('RICHARD GALANTI, COSTCO CFO (2015 CALL)', 80, h - 26, font('SpecialElite.ttf', 24), paint(GREY))
    panel(c, 110, 860, 860, 420, rot=1.2, k=pr(t, t0 + 0.6, 0.45), draw=dr)
    if t > tm - 0.2: burst(c, 840, 1300, 130, '$30-40M', pr(t, tm - 0.2, 0.35), size=44, col=KINK, txt=YEL, rot=-8)


def sc_bet(c, t, S):
    t0 = S['t0']; tb = ph("here's the bet"); tc = ph('cheap chicken'); tf = ph('full cart')
    bgp(c, t)
    caption(c, 'WHY WOULD A STORE DO THAT?', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    two(c, 'THE', 'BET', 470, pr(t, tb - 0.3, 0.35), pr(t, tb - 0.1, 0.35), 100, 150)
    # cart rolls in from the left and keeps rolling a little
    k = pr(t, t0 + 0.2, 0.9); cx = -300 + 840 * eo(cl(k)) + 12 * math.sin(t * 2)
    c.drawCircle(cx + 40, 1250, 300, paint(YEL, 0.0))
    if t > tc - 0.3:
        kk = pr(t, tc - 0.3, 0.5); yy = 500 + 470 * eo(kk)
        stick(c, 'chicken', cx + 30, yy, 260, kk, t, rot=-10 + 30 * (1 - kk), amp=0)
    items = [('COFFEE', -110), ('TIRES', 60), ('A BIG TV', -40), ('PAPER TOWELS', 120), ('SNACKS', -150)]
    if t > tf - 1.2:
        for i, (s_, dx) in enumerate(items):
            kk = pr(t, tf - 1.2 + i * 0.22, 0.4)
            if kk <= 0: continue
            yy = 560 + 400 * eo(kk) - i * 34
            c.save(); c.translate(cx + dx, yy); c.rotate((-12, 8, -4, 14, -9)[i])
            f = font('LuckiestGuy.ttf', 40); w = f.measureText(s_) + 40
            c.drawRect(R.MakeXYWH(-w / 2 + 8, -30 + 8, w, 64), paint(KINK)); c.drawRect(R.MakeXYWH(-w / 2, -30, w, 64), paint(CREAM))
            c.drawRect(R.MakeXYWH(-w / 2, -30, w, 64), stroke(KINK, 6)); c.drawString(s_, -w / 2 + 20, 16, f, paint(CHAR)); c.restore()
    stick(c, 'cart', cx, 1130, 640, k, t, rot=0, amp=4)
    credit(c, 'cart')


def sc_plant(c, t, S):
    t0 = S['t0']; tn = ph('in nebraska'); tm = ph('four hundred fifty'); th = ph('a hatchery'); tf = ph('a feed mill'); tp = ph('a processing plant'); tw = ph('two million birds')
    bgp(c, t)
    caption(c, 'THEN IT GOT EVEN CRAZIER', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    if t < th - 0.3:
        two(c, 'COSTCO BUILT ITS', 'OWN CHICKEN PLANT', 470, pr(t, t0 + 0.1, 0.35), pr(t, t0 + 0.4, 0.35), 90, 92)
        photo_panel(c, 'farm', 110, 650, 860, 520, 1.5, pr(t, t0 + 0.3, 0.45), t=t - t0)
        credit(c, 'farm')
        if t > tn - 0.3: caption(c, 'FREMONT, NEBRASKA . 2019', 130, 1240, pr(t, tn - 0.3, 0.3), col=CREAM, size=30, rot=-1.5)
        if t > tm - 0.3: burst(c, 820, 1170, 170, '$450M', pr(t, tm - 0.3, 0.35), size=74, col=KINK, txt=YEL, rot=-8)
        return
    two(c, 'FARM TO STORE,', 'ALL COSTCO', 470, pr(t, th - 0.3, 0.35), pr(t, th, 0.35), 90, 110)
    steps = [(th, 'HATCHERY'), (tf, 'FEED MILL'), (tp, 'PLANT')]
    for i, (tt, s_) in enumerate(steps):
        kk = pr(t, tt - 0.3, 0.4)
        if kk <= 0: continue
        x = 110 + i * 300
        def dr(cc, s_=s_, i=i):
            cc.drawRect(R.MakeWH(260, 300), paint(CREAM if i != 1 else YEL)); dots(cc, (0, 0, 260, 300), KINK, cell=14, rmax=3, a=0.15)
            title(cc, str(i + 1), 130, 170, 140, CHAR, 1.0, 'c', outline=0.01, shadow=0)
            cc.drawString(s_, 130 - font('LuckiestGuy.ttf', 40).measureText(s_) / 2, 260, font('LuckiestGuy.ttf', 40), paint(CHAR))
        panel(c, x, 650, 260, 300, rot=(-3, 2, -2)[i], k=kk, draw=dr)
        if i < 2: c.drawLine(x + 262, 800, x + 300, 800, stroke(CHAR, 10))
    # conveyor of chickens flowing across under the steps
    if t > tw - 0.6:
        kk = pr(t, tw - 0.6, 0.4)
        for j in range(7):
            xx = (j * 190 + (t - tw) * 260) % 1330 - 140
            place(c, 'chicken_cut.png', xx, 1110, 170, rot=-6 + 4 * math.sin(t * 3 + j), a=kk, shadow=False)
        c.drawRect(R.MakeXYWH(60, 1190, 960, 18), paint(CHAR, kk))
        title(c, '~2,000,000 A WEEK', 540, 1330, 80, YEL, kk, 'c', rot=-2)


def sc_result(c, t, S):
    t0 = S['t0']; tn = ph('fifty-seven million'); ts = ph('still four')
    bgp(c, t)
    caption(c, "AND IT'S WORKING", LX, 300, pr(t, t0, 0.3), col=YEL, size=30)
    # chickens rain in and pile up behind the number
    kr = pr(t, t0 + 0.2, 2.6)
    n = int(26 * kr)
    for j in range(n):
        x = 120 + (j * 223) % 860; y0 = 640 + ((j * 137) % 5) * 150
        kk = pr(t, t0 + 0.2 + j * 0.09, 0.4)
        place(c, 'chicken_cut.png', x, y0 - 300 * (1 - eo(kk)), 220, rot=(j * 37) % 40 - 20, a=kk * 0.95, shadow=False)
    if t > tn - 0.5:
        k = pr(t, tn - 0.5, 0.4)
        c.save(); c.translate(540, 900); c.rotate(-3); sc = eback(cl(k), 2); c.scale(sc, sc)
        c.drawRect(R.MakeXYWH(-430 + 14, -200 + 14, 860, 330), paint(KINK)); c.drawRect(R.MakeXYWH(-430, -200, 860, 330), paint(CREAM)); c.drawRect(R.MakeXYWH(-430, -200, 860, 330), stroke(KINK, 9))
        title(c, '157 MILLION', 0, -40, 130, YEL, 1.0, 'c')
        title(c, 'CHICKENS SOLD IN 2025', 0, 80, 60, CHAR, 1.0, 'c', outline=0.01, shadow=0)
        c.restore()
    if t > ts - 0.3:
        tag(c, 300, 1260, 'STILL $4.99', pr(t, ts - 0.3, 0.35), t, rot=-6, size=100)


def sc_end(c, t, S):
    t0 = S['t0']; tl = ph('lose millions'); tw = ph('the whole cart')
    bgp(c, t)
    caption(c, 'YOUR CALL', LX, 300, pr(t, t0, 0.3), col=YEL, size=36)
    two(c, 'LOSE MILLIONS', 'TO WIN THE CART?', 470, pr(t, tl - 0.3, 0.35), pr(t, tw - 0.3, 0.35), 104, 100)
    c.drawCircle(540, 1000, 300 + 8 * math.sin(t * 2), paint(YEL))
    stick(c, 'cart', 600, 1030, 560, pr(t, t0 + 0.2, 0.4), t, amp=6)
    stick(c, 'chicken', 470, 860, 300, pr(t, t0 + 0.5, 0.4), t, rot=-12, amp=8)
    if t > END:
        full(c, lambda: c.drawCircle(540, 900, 1400 * eio(pr(t, END, 0.8)), paint(CHAR)))


def with_subs(fn):
    def f(c, t, S):
        c.save(); c.concat(LAY); fn(c, t, S); c.restore()
        if 0.35 < t < END + 0.2: subtitle(c, t, SUBS, y=SUB_Y)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook), col=(252, 241, 210)),
    dict(k='price', t0=ph("costco's rotisserie") - 0.2, fn=with_subs(sc_price), tin='whip', col=(252, 241, 210)),
    dict(k='cfo', t0=ph('in twenty fifteen') - 0.2, fn=with_subs(sc_cfo), tin='wipe', col=(252, 241, 210)),
    dict(k='bet', t0=ph('why would a store') - 0.2, fn=with_subs(sc_bet), tin='whip', col=(252, 241, 210)),
    dict(k='plant', t0=ph('then it got even') - 0.2, fn=with_subs(sc_plant), tin='zoom', col=(252, 241, 210)),
    dict(k='result', t0=ph("and it's working") - 0.2, fn=with_subs(sc_result), tin='whip', col=(252, 241, 210)),
    dict(k='end', t0=ph('would you lose') - 0.2, fn=with_subs(sc_end), tin='flash', col=(252, 241, 210)),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('millions of dollars'), 10, 0.3)
EP.shk(ph('thirty to forty'), 8, 0.3)
EP.shk(ph('four hundred fifty'), 10, 0.3)
EP.shk(ph('fifty-seven million'), 12, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
