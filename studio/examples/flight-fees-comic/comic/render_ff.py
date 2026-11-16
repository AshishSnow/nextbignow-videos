"""OopsMyBusiness Short — budget-airline fee traps ($19 flight, $99 bag). Vintage comic, BLACK + YELLOW theme (owner 15 Nov 2026).
Facts: ../SOURCES.md. Photos + licences: ff/img/credits.json. No airline logos/liveries; airline names as text only."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'ff')
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
def boarding_pass(c, x, y, w, h, rot, k, price, t=0.0, stamp=None, sk=0.0):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(CREAM)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=2.6, a=0.12)
        cc.drawRect(R.MakeWH(w, 90), paint(CHAR))
        cc.drawString('BOARDING PASS', 30, 62, font('LuckiestGuy.ttf', 50), paint(YEL))
        cc.drawString('ECONOMY . BASIC FARE', 30, 140, font('SpecialElite.ttf', 30), paint(KINK))
        title(cc, 'NYC', 30, 255, 80, KINK, 1.0, shadow=0, outline=0.01)
        cc.drawLine(215, 225, 330, 225, stroke(KINK, 6)); cc.drawPath(poly([(330, 207), (362, 225), (330, 243)]), paint(KINK))
        title(cc, 'MIA', 380, 255, 80, KINK, 1.0, shadow=0, outline=0.01)
        cc.drawLine(w - 250, 100, w - 250, h - 20, stroke(KINK, 4))
        title(cc, price, w - 225, 250, 120, YEL, 1.0, shadow=6)
        for i in range(26): cc.drawRect(R.MakeXYWH(30 + i * 22, h - 90, 8 + (i * 7) % 11, 60), paint(KINK))
        if stamp and sk > 0:
            cc.save(); cc.translate(w * 0.55, h * 0.55); cc.rotate(-12); sc = 1.6 - 0.6 * eback(cl(sk), 2.0); cc.scale(sc, sc)
            f = font('LuckiestGuy.ttf', 130); tw = f.measureText(stamp)
            cc.drawRect(R.MakeXYWH(-tw / 2 - 30, -120, tw + 60, 160), stroke((210, 30, 40), 12))
            cc.drawString(stamp, -tw / 2, 10, f, paint((210, 30, 40))); cc.restore()
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def suitcase(c, x, y, k, t, rot=-8):
    """drawn carry-on roller bag (comic sticker)."""
    if k <= 0: return
    sc = eback(cl(k), 2.0)
    c.save(); c.translate(x, y); c.rotate(rot + 2 * math.sin(t * 3)); c.scale(sc, sc)
    c.drawLine(-60, -260, -60, -150, stroke(KINK, 22)); c.drawLine(60, -260, 60, -150, stroke(KINK, 22)); c.drawLine(-60, -260, 60, -260, stroke(KINK, 22))
    c.drawLine(-60, -260, -60, -150, stroke((150, 150, 160), 10)); c.drawLine(60, -260, 60, -150, stroke((150, 150, 160), 10)); c.drawLine(-60, -260, 60, -260, stroke((150, 150, 160), 10))
    body = skia.RRect.MakeRectXY(R.MakeXYWH(-130, -160, 260, 330), 34, 34)
    c.save(); c.translate(14, 14); c.drawRRect(body, paint(KINK)); c.restore()
    c.drawRRect(body, paint(YEL)); dots(c, (-130, -160, 260, 330), (200, 150, 0), cell=14, rmax=4, a=0.5)
    for xx in (-60, 0, 60): c.drawLine(xx, -140, xx, 150, stroke((200, 150, 0), 8))
    c.drawRRect(body, stroke(KINK, 10))
    for xx in (-80, 80): c.drawCircle(xx, 190, 26, paint(KINK)); c.drawCircle(xx, 190, 10, paint((150, 150, 160)))
    c.save(); c.rotate(14); c.drawRect(R.MakeXYWH(30, -40, 140, 70), paint(CREAM)); c.drawRect(R.MakeXYWH(30, -40, 140, 70), stroke(KINK, 6))
    c.drawString('+$99', 44, 14, font('LuckiestGuy.ttf', 44), paint((210, 30, 40))); c.restore()
    c.restore()


def sc_hook(c, t, S):
    tn = ph('ninety-nine dollars more'); tb = ph('for one bag')
    dark(c, t)
    caption(c, 'WOULD YOU PAY THIS?', LX, 300, 1.0, col=YEL, size=30)
    title(c, 'THE $19', 540, 470, 120, CREAM, 1.0, 'c', rot=-2)
    title(c, 'FLIGHT TRAP', 540, 620, 140, YEL, 1.0, 'c', rot=-2)
    boarding_pass(c, 100, 700, 880, 440, 2, 1.0, '$19', t, stamp='+$99', sk=pr(t, tn - 0.15, 0.35))
    if t > tb - 0.3:
        suitcase(c, 760, 1180, pr(t, tb - 0.3, 0.35), t)
        caption(c, 'FOR ONE BAG.', 160, 1290, pr(t, tb - 0.2, 0.3), col=YEL, size=34, rot=-2)


def sc_bag(c, t, S):
    t0 = S['t0']; tb = ph('twenty-nine dollars'); tg = ph('wait until the gate'); tn = ph('ninety-nine to'); ts = ph('same bag')
    dark(c, t)
    caption(c, 'TRAP 1: THE BAG', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    photo_panel(c, 'gate', 110, 380, 860, 420, -1.2, pr(t, t0 + 0.1, 0.45), t=t - t0)
    credit(c, 'gate')
    mini(c, 100, 860, 420, 300, -2.5, pr(t, tb - 0.3, 0.4), 'ADD IT WHEN YOU BOOK', '$29', CREAM, txtc=YEL, bigsize=130)
    if t > tg - 0.3:
        mini(c, 550, 880, 430, 300, 2.5, pr(t, tg - 0.2, 0.4), 'PAY AT THE GATE', '$99+', YEL, txtc=CREAM, bigsize=130)
    if t > tn: caption(c, 'UP TO $115', 640, 1230, pr(t, tn, 0.3), col=CREAM, size=30, rot=2)
    if t > ts - 0.2: title(c, 'SAME BAG. SAME PLANE.', 540, 1350, 70, YEL, pr(t, ts - 0.2, 0.35), 'c', rot=-2)


def sc_senate(c, t, S):
    t0 = S['t0']; tr = ph('senate report'); tt = ph('ten dollars'); te = ph('every bag')
    yellow(c, t)
    caption(c, 'WHO IS AT THE GATE?', LX, 300, pr(t, t0, 0.3), col=CREAM, size=32)
    def dr(cc):
        w, h = 860, 560
        cc.drawRect(R.MakeWH(w, h), paint(CREAM))
        cc.drawString('US SENATE . STAFF REPORT', 40, 80, font('SpecialElite.ttf', 38), paint(KINK))
        cc.drawString('NOVEMBER 2024', 40, 130, font('SpecialElite.ttf', 30), paint(GREY))
        cc.drawString('"THE SKY\'S THE LIMIT: THE RISE', 40, 210, font('SpecialElite.ttf', 32), paint(KINK))
        cc.drawString('OF JUNK FEES IN AMERICAN TRAVEL"', 40, 255, font('SpecialElite.ttf', 32), paint(KINK))
        for i in range(4): cc.drawRect(R.MakeXYWH(40, 310 + i * 40, (760, 700, 740, 520)[i], 14), paint((190, 182, 160)))
    panel(c, 110, 400, 860, 560, rot=-1.5, k=pr(t, tr - 0.3, 0.45), draw=dr)
    if t > tt - 0.3: burst(c, 740, 1020, 175, 'UP TO $10', pr(t, tt - 0.3, 0.35), size=50, col=KINK, txt=YEL, rot=-8)
    if t > te - 0.2: caption(c, 'PER BAG CHECKED AT THE GATE', 110, 1180, pr(t, te - 0.2, 0.3), col=CREAM, size=30, rot=-1.5)
    if t > te + 0.4: caption(c, 'FRONTIER STAFF . 2022-2023', 140, 1260, pr(t, te + 0.4, 0.3), col=CREAM, size=26, rot=1)


def sc_seat(c, t, S):
    t0 = S['t0']; t1 = ph('fifty dollars'); t2 = ph('forty-one')
    dark(c, t)
    caption(c, 'TRAP 2: THE SEAT', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    photo_panel(c, 'cabin', 110, 380, 860, 400, 1.2, pr(t, t0 + 0.1, 0.45), zoom=1.0, fy=0.45, t=t - t0)
    credit(c, 'cabin')
    def dr(cc):
        cc.drawRect(R.MakeWH(860, 480), paint(CREAM))
        bars(cc, 120, 50, 620, 340, [('2018', 50, '$50', (120, 120, 130)), ('2023', 141, '$141', YEL)], pr(t, t0 + 0.6, 1.8), 165)
        cc.drawString("FRONTIER'S PRICIEST LEGROOM SEAT (SENATE REPORT)", 40, 455, font('SpecialElite.ttf', 22), paint(GREY))
    panel(c, 110, 830, 860, 480, rot=-1, k=pr(t, t0 + 0.4, 0.4), draw=dr)
    if t > t2: burst(c, 860, 840, 110, 'X2.8', pr(t, t2, 0.3), size=48, col=KINK, txt=YEL, rot=10)


def sc_europe(c, t, S):
    t0 = S['t0']; to = ph('check in online'); tf = ph('fifty-five pounds')
    dark(c, t)
    caption(c, 'TRAP 3: EUROPE', LX, 300, pr(t, t0, 0.3), col=YEL, size=34)
    title(c, 'FORGOT TO', 80, 480, 120, CREAM, pr(t, to - 0.4, 0.4))
    title(c, 'CHECK IN ONLINE?', 90, 610, 104, YEL, pr(t, to - 0.1, 0.4), rot=-2)
    photo_panel(c, 'checkin', 110, 680, 860, 520, -1.5, pr(t, t0 + 0.2, 0.45), zoom=1.9, fx=0.55, fy=0.15, t=t - t0)
    credit(c, 'checkin')
    if t > tf - 0.3: burst(c, 760, 1180, 170, '£55', pr(t, tf - 0.3, 0.35), size=96, col=YEL, txt=CREAM, rot=-8)
    if t > tf + 0.2: caption(c, 'RYANAIR AIRPORT CHECK-IN', 120, 1290, pr(t, tf + 0.2, 0.3), col=CREAM, size=28, rot=-1.5)


def sc_money(c, t, S):
    t0 = S['t0']; tf = ph('fifty-one euros'); tx = ph('twenty-four euros'); tb = ph('five billion'); tt = ph('the ticket gets you')
    dark(c, t)
    if t < tt - 0.3:
        caption(c, 'HOW DOES A CHEAP TICKET MAKE MONEY?', LX, 300, pr(t, t0, 0.3), col=YEL, size=28)
        k = pr(t, t0 + 0.2, 0.45)
        def dr(cc):
            w = 700; cc.drawRect(R.MakeWH(w, 900), paint(CREAM))
            cc.drawString('RYANAIR . YEAR TO MARCH 2026', 40, 70, font('SpecialElite.ttf', 30), paint(KINK))
            cc.drawLine(40, 95, w - 40, 95, stroke(KINK, 3))
            rows = [(min(tf, t0 + 1.0), 'AVERAGE FARE', '€51', KINK), (tx, '+ EXTRAS / PERSON', '€24', (190, 140, 0))]
            for i, (tt_, a, b, col) in enumerate(rows):
                if t > tt_ - 0.3:
                    kk = pr(t, tt_ - 0.3, 0.3); yy = 200 + i * 130
                    cc.drawString(a, 40, yy, font('SpecialElite.ttf', 40), paint(KINK, kk))
                    title(cc, b, w - 220, yy + 10, 90, col if col != KINK else CHAR, kk, shadow=0, outline=0.01)
            if t > tb - 0.3:
                kk = pr(t, tb - 0.3, 0.3); cc.drawLine(40, 470, w - 40, 470, stroke(KINK, 4))
                cc.drawString('EXTRAS, ALL YEAR:', 40, 560, font('SpecialElite.ttf', 40), paint(KINK, kk))
                title(cc, '€4.99 BILLION', 40, 700, 104, YEL, kk, shadow=6)
            for i in range(0, w, 40): cc.drawPath(poly([(i, 900), (i + 20, 880), (i + 40, 900)]), paint(CHAR))
        panel(c, 190, 380, 700, 900, rot=-1.5, k=k, draw=dr)
        return
    title(c, 'THE TICKET', 540, 640, 130, CREAM, pr(t, tt - 0.2, 0.4), 'c', rot=-2)
    title(c, 'GETS YOU ON.', 540, 780, 110, CREAM, pr(t, tt, 0.4), 'c', rot=-2)
    te = ph('the extras pay')
    title(c, 'THE EXTRAS', 540, 1000, 130, YEL, pr(t, te - 0.2, 0.4), 'c', rot=2)
    title(c, 'PAY THE BILLS.', 540, 1140, 110, YEL, pr(t, te, 0.4), 'c', rot=2)


def sc_move(c, t, S):
    t0 = S['t0']; tr = ph('add your bag'); tf = ph('check in online', after=t0); ts = ph('measure your bag')
    dark(c, t)
    caption(c, 'BEAT THE TRAP', LX, 300, pr(t, t0, 0.3), col=YEL, size=32)
    items = [(tr, '1', 'ADD YOUR BAG', 'WHEN YOU BOOK'), (tf, '2', 'CHECK IN', 'ONLINE'), (ts, '3', 'MEASURE YOUR', 'BAG AT HOME')]
    for i, (tt, n, a1, a2) in enumerate(items):
        def dr(cc, n=n, a1=a1, a2=a2):
            cc.drawRect(R.MakeWH(860, 230), paint(CREAM))
            cc.drawRect(R.MakeWH(170, 230), paint(YEL)); dots(cc, (0, 0, 170, 230), KINK, cell=14, rmax=3, a=0.2)
            title(cc, n, 85, 160, 150, KINK, 1.0, 'c', shadow=0, outline=0.01)
            cc.drawString(a1, 200, 95, font('SpecialElite.ttf', 44), paint(KINK))
            title(cc, a2, 200, 180, 66, YEL, 1.0, shadow=4)
        panel(c, 110, 420 + i * 280, 860, 230, rot=(-1.5, 1.2, -1)[i], k=pr(t, tt - 0.3, 0.4), draw=dr)


def sc_end(c, t, S):
    t0 = S['t0']; tw = ph('worst fee')
    yellow(c, t)
    caption(c, 'YOUR TURN', LX, 300, pr(t, t0, 0.3), col=CREAM, size=32)
    title(c, "WHAT'S THE WORST", 540, 560, 100, KINK, pr(t, t0 + 0.1, 0.4), 'c', outline=0.01, shadow=0)
    title(c, 'FEE YOU PAID?', 540, 700, 120, CREAM, pr(t, tw - 0.2, 0.4), 'c', rot=-2)
    boarding_pass(c, 140, 790, 800, 400, -3, pr(t, t0 + 0.3, 0.4), '$19', t, stamp='+FEES', sk=pr(t, tw, 0.35))
    if t > END:
        full(c, lambda: c.drawCircle(540, 900, 1400 * eio(pr(t, END, 0.8)), paint(CHAR)))


def with_subs(fn):
    def f(c, t, S):
        c.save(); c.concat(LAY); fn(c, t, S); c.restore()
        if 0.35 < t < END + 0.2: subtitle(c, t, SUBS, y=SUB_Y)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook), col=CHAR),
    dict(k='bag', t0=ph("here's the trap") - 0.2, fn=with_subs(sc_bag), tin='whip', col=CHAR),
    dict(k='senate', t0=ph('and the person') - 0.2, fn=with_subs(sc_senate), tin='flash', col=YEL),
    dict(k='seat', t0=ph('trap two') - 0.2, fn=with_subs(sc_seat), tin='wipe', col=CHAR),
    dict(k='europe', t0=ph('trap three') - 0.2, fn=with_subs(sc_europe), tin='whip', col=CHAR),
    dict(k='money', t0=ph('so how does') - 0.2, fn=with_subs(sc_money), tin='zoom', col=CHAR),
    dict(k='move', t0=ph('so add your bag') - 0.2, fn=with_subs(sc_move), tin='whip', col=CHAR),
    dict(k='end', t0=ph("what's the worst") - 0.2, fn=with_subs(sc_end), tin='flash', col=YEL),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('ninety-nine dollars more'), 10, 0.3)
EP.shk(ph('ten dollars'), 8, 0.3)
EP.shk(ph('fifty-five pounds'), 8, 0.3)
EP.shk(ph('five billion'), 10, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
