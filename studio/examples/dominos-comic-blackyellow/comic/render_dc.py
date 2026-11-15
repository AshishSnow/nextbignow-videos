"""OopsMyBusiness Short — Domino's 'like cardboard' turnaround. Vintage comic, BLACK + YELLOW theme (owner 15 Nov 2026).
Facts: ../SOURCES.md. Photos + licences: dc/img/credits.json. No logos/trade dress; no likeness of Patrick Doyle (name as text only)."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'dc')
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


def dark(c, t=0.0):
    full(c, lambda: _dark(c))


def _dark(c):
    c.drawRect(R.MakeWH(W, H), paint(CHAR))
    dots(c, (0, 0, W, H), CHAR_D, cell=22, rmax=7, grad=(0.45, 1.0), angle=30)
    c.drawRect(R.MakeWH(W, H), paint(shader=skia.GradientShader.MakeRadial((W / 2, H * 0.45), 1250, [argb((0, 0, 0), 0), argb((0, 0, 0), 0.35)])))


def yellow(c, t=0.0): full(c, lambda: bg_flat(c, YEL, (232, 186, 0)))


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


# ------------------------------------------------------------------ scenes
def sc_hook(c, t, S):
    td = ph("domino's did"); tp = ph('on purpose'); tj = ph('sales jumped')
    dark(c, t)
    caption(c, 'WOULD YOU AIR THIS?', LX, 300, 1.0, col=YEL, size=30)
    title(c, 'THE CARDBOARD', 540, 470, 112, CREAM, 1.0, 'c', rot=-2)
    title(c, 'COMEBACK', 540, 610, 150, YEL, 1.0, 'c', rot=-2)
    tv(c, 170, 690, 740, 470, 1.0, t, 'pizza', rot=-2)
    credit(c, 'pizza')
    if t < td - 0.1:
        bubble(c, 600, 1290, 740, 180, '"LIKE CARDBOARD!"', (430, 1160), 1.0, size=56)
    else:
        title(c, "DOMINO'S DID.", 540, 1330, 120, YEL, pr(t, td - 0.1, 0.35), 'c', rot=-3)
    if t > tp - 0.2: burst(c, 880, 720, 125, 'ON PURPOSE', pr(t, tp - 0.2, 0.3), size=30, col=KINK, txt=YEL, rot=8)
    if t > tj - 0.3: burst(c, 470, 920, 160, 'SALES UP!', pr(t, tj - 0.3, 0.35), size=52, col=YEL, txt=CREAM, rot=-6)


def sc_slide(c, t, S):
    t0 = S['t0']; tf = ph('five percent')
    dark(c, t)
    caption(c, 'USA . 2008', LX, 330, pr(t, t0, 0.3), col=YEL, size=32)
    title(c, 'SALES ARE', 80, 540, 130, CREAM, pr(t, t0 + 0.1, 0.4))
    title(c, 'SLIDING.', 90, 700, 150, YEL, pr(t, t0 + 0.5, 0.4), rot=-2)
    def dr(cc):
        cc.drawRect(R.MakeWH(840, 440), paint(CREAM))
        x0, y0, cw, ch = 70, 40, 700, 300
        cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
        k = pr(t, t0 + 0.4, 1.4); p = skia.Path(); pts = [(0, .8), (.25, .74), (.5, .66), (.75, .55), (1, .42)]; first = True
        for fx, v in pts:
            if fx > k: break
            (p.moveTo if first else p.lineTo)(x0 + fx * cw, y0 + ch - v * ch); first = False
        cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(YEL, 9))
        cc.drawString('US SAME-STORE SALES (ILLUSTRATIVE LINE)', 70, 405, font('SpecialElite.ttf', 24), paint(GREY))
    panel(c, 120, 800, 840, 440, rot=1.2, k=pr(t, t0 + 0.3, 0.4), draw=dr)
    if t > tf - 0.3: burst(c, 820, 1210, 125, '-5%', pr(t, tf - 0.3, 0.35), size=70, col=KINK, txt=YEL, rot=-8)
    if t > tf + 0.4: caption(c, 'VS THE YEAR BEFORE', 150, 1290, pr(t, tf + 0.4, 0.3), col=CREAM, size=26, rot=-1.5)


def sc_customers(c, t, S):
    t0 = S['t0']; tc = ph('like cardboard', after=t0); tk = ph('like ketchup'); tb = ph('most companies'); tfx = ph('fixed the pizza')
    dark(c, t)
    if t < tb - 0.3:
        caption(c, 'SO IT ASKED REAL CUSTOMERS', LX, 330, pr(t, t0, 0.3), col=YEL, size=30)
        photo_panel(c, 'office', 120, 440, 840, 480, -1.5, pr(t, t0 + 0.1, 0.5), t=t - t0)
        credit(c, 'office')
        if t > tc - 0.4: bubble(c, 380, 1090, 600, 190, 'CRUST? CARDBOARD.', (300, 900), pr(t, tc - 0.4, 0.35), size=46)
        if t > tk - 0.4: bubble(c, 680, 1290, 600, 190, 'SAUCE? KETCHUP.', (760, 1120), pr(t, tk - 0.4, 0.35), size=48)
        return
    caption(c, 'MOST COMPANIES...', LX, 330, pr(t, tb - 0.3, 0.3), col=CREAM, size=32)
    title(c, 'BURY IT.', 80, 560, 160, CREAM, pr(t, tb - 0.2, 0.4), rot=-2)
    if t > tfx - 0.3:
        k = pr(t, tfx - 0.3, 0.25); c.drawLine(70, 470, 70 + 640 * k, 540 + 30 * k, stroke(YEL, 26))
        title(c, "DOMINO'S:", 80, 790, 120, YEL, pr(t, tfx - 0.2, 0.4))
        title(c, 'FIX THE PIZZA.', 90, 940, 120, CREAM, pr(t, tfx, 0.4), rot=-2)
        photo_panel(c, 'oven', 140, 1010, 800, 330, 1.5, pr(t, tfx, 0.5), t=t - tfx)
        credit(c, 'oven')


def sc_test(c, t, S):
    t0 = S['t0']; ty = ph('two years'); tc = ph('dozens of cheeses'); ts = ph('fifteen sauces'); tcr = ph('nearly fifty')
    dark(c, t)
    caption(c, "DOMINO'S SAYS:", LX, 330, pr(t, t0, 0.3), col=YEL, size=32)
    title(c, '~2 YEARS', 80, 560, 150, YEL, pr(t, t0 + 0.2, 0.4), rot=-2)
    title(c, 'OF TESTING.', 90, 710, 120, CREAM, pr(t, t0 + 0.6, 0.4))
    photo_panel(c, 'cheese', 100, 800, 290, 290, -3, pr(t, tc - 0.3, 0.4), t=t)
    photo_panel(c, 'sauce', 395, 820, 290, 290, 2, pr(t, ts - 0.3, 0.4), t=t)
    mini(c, 690, 800, 290, 290, -2, pr(t, tcr - 0.3, 0.4), 'CRUST SEASONINGS', '~50', YEL, txtc=CREAM, bigsize=120)
    for i, (tt, s) in enumerate(((tc, 'DOZENS OF CHEESES'), (ts, '15 SAUCES'), (tcr, '~50 CRUST SEASONINGS'))):
        if t > tt - 0.2: caption(c, s, 100 + i * 20, 1150 + i * 80, pr(t, tt - 0.2, 0.3), col=(YEL, CREAM, YEL)[i], size=28, rot=(-1.5, 1, -1)[i])
    if t > tc: credit(c, 'cheese' if t < ts else 'sauce')


def sc_ads(c, t, S):
    t0 = S['t0']; td = ph('december'); tc = ph('right on tv'); tdo = ph('patrick doyle'); tq = ph('there comes a time')
    yellow(c, t)
    if t < tdo - 0.4:
        caption(c, 'THE SCARY PART', LX, 330, pr(t, t0, 0.3), col=CREAM, size=32)
        title(c, 'DEC 2009', 80, 540, 140, KINK, pr(t, td - 0.3, 0.4), outline=0.01, shadow=0)
        def scr(cc, sw, sh):
            title(cc, '"LIKE', sw / 2, sh * 0.45, 110, YEL, 1.0, 'c', shadow=6)
            title(cc, 'CARDBOARD"', sw / 2, sh * 0.82, 110, YEL, 1.0, 'c', shadow=6)
        tv(c, 110, 640, 860, 580, pr(t, t0 + 0.2, 0.45), t, None, rot=2, screen=scr)
        if t > tc - 0.4: burst(c, 820, 1300, 120, 'ON TV!', pr(t, tc - 0.4, 0.35), size=44, col=KINK, txt=YEL, rot=8)
        return
    caption(c, 'THE BOSS OF THE US STORES', LX, 330, pr(t, tdo - 0.4, 0.3), col=CREAM, size=30)
    title(c, 'PATRICK DOYLE:', 80, 540, 110, KINK, pr(t, tdo - 0.2, 0.4), outline=0.01, shadow=0)
    quote(c, 110, 650, 860, 400, -1.5, pr(t, tq - 0.3, 0.4),
          ['There comes a time', 'when you know', "you've got to make", 'a change.'], 'PATRICK DOYLE, IN THE DEC 2009 AD (VIA MEDIAPOST)')


def sc_result(c, t, S):
    t0 = S['t0']; tf = ph('fourteen percent'); ty = ph('a year earlier'); to = ph('just one'); tb = ph('doyle credited'); th = ph('the honesty')
    dark(c, t)
    if t < tb - 0.3:
        caption(c, 'JAN-MAR 2010 . US STORES', LX, 330, pr(t, t0, 0.3), col=YEL, size=30)
        title(c, 'DID IT WORK?', 80, 540, 130, CREAM, pr(t, t0 + 0.1, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(840, 560), paint(CREAM))
            bars(cc, 90, 60, 660, 400, [('A YEAR EARLIER', 1.0, '+1%', (120, 120, 130)), ('JAN-MAR 2010', 14.3, '+14.3%', YEL)],
                 pr(t, t0 + 0.5, 1.6), 17)
            cc.drawString('US SAME-STORE SALES (DOMINO\'S, MAY 2010)', 70, 535, font('SpecialElite.ttf', 22), paint(GREY))
        panel(c, 120, 640, 840, 560, rot=-1.2, k=pr(t, t0 + 0.3, 0.4), draw=dr)
        if t > ty - 0.2: caption(c, 'A YEAR EARLIER? +1%', 160, 1290, pr(t, ty - 0.2, 0.3), col=YEL, size=30, rot=-1.5)
        return
    caption(c, 'DOYLE CREDITED...', LX, 330, pr(t, tb - 0.3, 0.3), col=YEL, size=32)
    mini(c, 100, 520, 860, 260, -2, pr(t, tb, 0.4), 'REASON 1', 'A BETTER PIZZA', CREAM, txtc=YEL, bigsize=90)
    mini(c, 120, 830, 860, 260, 1.5, pr(t, th - 0.3, 0.4), 'REASON 2', 'THE HONESTY', CREAM, txtc=YEL, bigsize=96)
    if t > th: burst(c, 820, 1210, 110, '+14%', pr(t, th, 0.35), size=48, col=KINK, txt=YEL, rot=-8)


def sc_move(c, t, S):
    t0 = S['t0']; tr = ph('read your worst'); tf = ph('fix it'); ts = ph('say so out loud')
    dark(c, t)
    caption(c, 'THE MOVE YOU CAN STEAL', LX, 330, pr(t, t0, 0.3), col=YEL, size=30)
    items = [(tr, '1', 'READ YOUR', 'WORST REVIEWS'), (tf, '2', "IF THEY'RE RIGHT,", 'FIX IT'), (ts, '3', 'THEN SAY SO', 'OUT LOUD')]
    for i, (tt, n, a1, a2) in enumerate(items):
        def dr(cc, n=n, a1=a1, a2=a2):
            cc.drawRect(R.MakeWH(860, 230), paint(CREAM))
            cc.drawRect(R.MakeWH(170, 230), paint(YEL)); dots(cc, (0, 0, 170, 230), KINK, cell=14, rmax=3, a=0.2)
            title(cc, n, 85, 160, 150, KINK, 1.0, 'c', shadow=0, outline=0.01)
            cc.drawString(a1, 200, 95, font('SpecialElite.ttf', 44), paint(KINK))
            title(cc, a2, 200, 180, 66, YEL, 1.0, shadow=4)
        panel(c, 110, 480 + i * 280, 860, 230, rot=(-1.5, 1.2, -1)[i], k=pr(t, tt - 0.3, 0.4), draw=dr)


def sc_end(c, t, S):
    t0 = S['t0']; ta = ph('air it'); th = ph('hide it')
    yellow(c, t)
    caption(c, 'YOUR PRODUCT GETS SLAMMED...', LX, 330, pr(t, t0, 0.3), col=CREAM, size=30)
    def scr(cc, sw, sh):
        title(cc, '1 STAR', sw / 2, sh * 0.62, 120, YEL, 1.0, 'c', shadow=6)
    tv(c, 170, 470, 740, 480, pr(t, t0 + 0.1, 0.4), t, None, rot=-2, screen=scr)
    burst(c, 300, 1200, 150, 'AIR IT', pr(t, ta - 0.2, 0.35), col=KINK, txt=YEL, size=52, rot=-6)
    title(c, 'OR', 540, 1225, 90, CREAM, pr(t, ta + 0.2, 0.3), 'c')
    burst(c, 780, 1200, 150, 'HIDE IT?', pr(t, th - 0.2, 0.35), col=CREAM, txt=YEL, size=46, rot=6)
    if t > END:
        full(c, lambda: c.drawCircle(540, 900, 1400 * eio(pr(t, END, 0.8)), paint(CHAR)))


def with_subs(fn):
    def f(c, t, S):
        c.save(); c.concat(LAY); fn(c, t, S); c.restore()
        if 0.35 < t < END + 0.2: subtitle(c, t, SUBS, y=SUB_Y)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook), col=CHAR),
    dict(k='slide', t0=ph('twenty oh eight') - 0.2, fn=with_subs(sc_slide), tin='whip', col=CHAR),
    dict(k='customers', t0=ph('so it asks') - 0.2, fn=with_subs(sc_customers), tin='wipe', col=CHAR),
    dict(k='test', t0=ph("domino's says") - 0.2, fn=with_subs(sc_test), tin='whip', col=CHAR),
    dict(k='ads', t0=ph('then the scary part') - 0.2, fn=with_subs(sc_ads), tin='flash', col=YEL),
    dict(k='result', t0=ph('did it work') - 0.2, fn=with_subs(sc_result), tin='zoom', col=CHAR),
    dict(k='move', t0=ph("so here's the move") - 0.2, fn=with_subs(sc_move), tin='whip', col=CHAR),
    dict(k='end', t0=ph('your product gets') - 0.2, fn=with_subs(sc_end), tin='flash', col=YEL),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('like cardboard'), 8, 0.3)
EP.shk(ph('five percent'), 8, 0.3)
EP.shk(ph('right on tv'), 10, 0.3)
EP.shk(ph('fourteen percent'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
