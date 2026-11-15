"""OopsMyBusiness — the Pet Rock (vintage comic + current editorial, 15 Nov 2026 brief). Real Commons photos (comic-filtered), no music.
Facts: see ../scripts/vo_lines.py header + ../SOURCES.md. Photos + licences: pr/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, 'pr')
PK.IMG = os.path.join(D, 'img')
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
DURATION = END + 2.0
LX = 90
SEPIA = (240, 222, 186)
GRN = (60, 190, 110)
STONE = 'stone_cut.png'


def credit(c, key, a=1.0, col=(120, 100, 70), y=1400):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s . WIKIMEDIA COMMONS' % (cr['author'], cr['license'])).upper()[:78]
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0, after=None):
    def dr(cc):
        cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.012 * t, fx, fy)
        if after: after(cc)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=PAPER, bigsize=54):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.25)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(PAPER if col in (CRED, CBLU) else KINK))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def rock(c, x, y, w, t, rot=0.0, a=1.0, bob=1.0, face=True, eyes_look=0.0):
    """the star: a comic-filtered stone sticker that bobs; optional googly eyes (drawn, not photo)."""
    yy = y + 10 * bob * math.sin(t * 3.1)
    place(c, STONE, x, yy, w, rot=rot + 2 * bob * math.sin(t * 2.3), a=a, shadow=True)
    if face and a > 0.5:
        for sx in (-1, 1):
            ex, ey = x + sx * w * 0.13, yy - w * 0.08
            c.drawCircle(ex, ey, w * 0.07, paint(PAPER)); c.drawCircle(ex, ey, w * 0.07, stroke(KINK, 5))
            c.drawCircle(ex + w * 0.025 * eyes_look, ey + w * 0.01, w * 0.03, paint(KINK))


def box(c, x, y, s, k, t, lid=0.0, label='PET CARRIER'):
    """cardboard pet carrier with air holes (drawn comic prop)."""
    if k <= 0: return
    c.save(); c.translate(x, y); sc = s * (0.85 + 0.15 * eback(cl(k), 1.6)); c.scale(sc, sc)
    tan = (214, 168, 110); dk = (170, 122, 70)
    front = poly([(-200, -40), (200, -40), (200, 180), (-200, 180)])
    side = poly([(200, -40), (270, -90), (270, 130), (200, 180)])
    top = poly([(-200, -40), (-130, -90), (270, -90), (200, -40)])
    for pp, col in ((front, tan), (side, dk), (top, (232, 194, 140))):
        c.save(); c.translate(10, 10); c.drawPath(pp, paint(KINK)); c.restore()
        c.drawPath(pp, paint(col)); c.drawPath(pp, stroke(KINK, 7))
    dots(c, (-200, -40, 400, 220), KINK, cell=14, rmax=2.6, grad=(0.5, 1.0), a=0.25)
    for i in range(4):
        c.drawCircle(-120 + i * 80, 20, 14, paint(KINK))
    c.drawString(label, -170, 130, font('SpecialElite.ttf', 40), paint(KINK))
    if lid > 0:
        c.save(); c.translate(-130, -90); c.rotate(-60 * lid)
        lp = poly([(0, 0), (400, 0), (330, 50), (-70, 50)]); c.drawPath(lp, paint((232, 194, 140))); c.drawPath(lp, stroke(KINK, 7)); c.restore()
    c.restore()


def manual(c, x, y, k, rot, t, page=0):
    if k <= 0: return
    def dr(cc):
        cc.drawRect(R.MakeWH(420, 540), paint((250, 244, 226)))
        dots(cc, (0, 0, 420, 540), CRED, cell=18, rmax=4, grad=(0.6, 1.0), a=0.25)
        cc.drawString('THE CARE AND', 30, 70, font('SpecialElite.ttf', 30), paint(KINK))
        cc.drawString('TRAINING OF YOUR', 30, 110, font('SpecialElite.ttf', 30), paint(KINK))
        title(cc, 'PET ROCK', 30, 200, 66, CRED, 1.0, shadow=5)
        cc.drawLine(30, 230, 390, 230, stroke(KINK, 4))
        for i, s in enumerate(('LESSON 1: OBEDIENCE', 'LESSON 2: PLAY DEAD')):
            if page >= i + 1: cc.drawString(s, 30, 300 + i * 60, font('SpecialElite.ttf', 28), paint(KINK))
            if page >= i + 1: cc.drawLine(30, 312 + i * 60, 30 + 330 * min(1, page - i), 312 + i * 60, stroke(CYEL, 6))
    panel(c, x, y, 420, 540, rot=rot, k=k, draw=dr, border=8, shadow=12)


def coin(c, x, y, r, k, t, txt='1c'):
    if k <= 0: return
    sc = eback(cl(k), 2.0); c.save(); c.translate(x, y); c.rotate(10 * math.sin(t * 2)); c.scale(sc, sc)
    c.drawCircle(8, 8, r, paint(KINK)); c.drawCircle(0, 0, r, paint((206, 128, 70))); c.drawCircle(0, 0, r, stroke(KINK, 7))
    c.drawCircle(0, 0, r * 0.78, stroke((150, 80, 40), 4))
    title(c, txt, 0, r * 0.25, r * 0.7, PAPER, 1.0, 'c', shadow=3)
    c.restore()


# ------------------------------------------------------------------ scenes
def sc_hook(c, t, S):
    t4 = ph('four bucks'); tl = ph('people loved them')
    paper(c, t)
    caption(c, 'CALIFORNIA . 1975', LX, 340, 1.0, col=CYEL, size=30)
    title(c, '1.5 MILLION', 80, 560, 132, CBLU, 1.0, rot=-2)
    title(c, 'ROCKS. SOLD.', 90, 720, 124, CRED, 1.0, rot=-1)
    # pile of pebbles (photo panel) with the hero rock bobbing in front
    photo_panel(c, 'pebbles', 120, 840, 840, 440, 1.5, 1.0, 1.08, t=t)
    rock(c, 560, 1130, 420, t, -6, eyes_look=math.sin(t * 1.3))
    if t > t4 - 0.2: burst(c, 840, 900, 120, '$3.95', pr(t, t4 - 0.2, 0.35), size=44, rot=8)
    if t > tl - 0.2: caption(c, 'PLAIN. ROCKS.', 170, 1300, pr(t, tl - 0.2, 0.3), col=CRED, size=30, rot=-2)
    credit(c, 'pebbles')


def sc_question(c, t, S):
    tq = S['t0']; ts = ph('three moves')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq, 0.3), col=PAPER, size=30)
    title(c, 'HOW DO YOU SELL', 80, 540, 108, PAPER, pr(t, tq + 0.1, 0.4))
    title(c, 'SOMETHING', 90, 680, 130, CYEL, pr(t, tq + 0.4, 0.4))
    title(c, 'FREE?', 90, 830, 170, PAPER, pr(t, tq + 0.8, 0.4), rot=-3)
    rock(c, 760, 1060, 360, t, 8, a=pr(t, tq + 0.5, 0.4))
    if t > ts - 0.3: burst(c, 330, 1220, 130, '+3 MOVES', pr(t, ts - 0.3, 0.35), size=40, rot=-8)


def sc_dahl(c, t, S):
    tb = ph('one night at a bar'); tf = ph('ruined furniture'); tw = ph('walks feeding'); tfe = ph('feeding')
    tj = ph('so dahl joked'); tn = ph('no food'); tla = ph('everybody laughed'); tm = ph('could be more')
    paper(c, t, tint=SEPIA)
    if t < tb - 0.3:
        caption(c, 'MEET GARY DAHL', LX, 340, pr(t, S['t0'], 0.3), size=30)
        title(c, 'AD COPYWRITER.', 80, 560, 112, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        photo_panel(c, 'typewriter', 120, 680, 840, 560, -1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        caption(c, 'WORDS FOR A LIVING', 200, 1260, pr(t, S['t0'] + 1.0, 0.3), col=CYEL, size=26, rot=-1)
        credit(c, 'typewriter')
        return
    if t < tj - 0.3:
        caption(c, 'ONE NIGHT, AT A BAR...', LX, 340, pr(t, tb - 0.3, 0.3), size=30)
        title(c, 'PET PROBLEMS:', 80, 540, 116, CRED, pr(t, tb, 0.4))
        photo_panel(c, 'bar', 120, 610, 840, 420, 1.2, pr(t, tb - 0.2, 0.5), t=t - tb)
        mini(c, 90, 1060, 300, 200, -3, pr(t, tf - 0.1, 0.35), 'PROBLEM 1', 'FURNITURE', CRED, bigsize=40)
        mini(c, 400, 1080, 280, 200, 2, pr(t, tw - 0.1, 0.35), 'PROBLEM 2', 'WALKS', CBLU, bigsize=56)
        mini(c, 690, 1060, 300, 200, -2, pr(t, tfe - 0.1, 0.35), 'PROBLEM 3', 'FEEDING', CYEL, txtc=CRED, bigsize=48)
        credit(c, 'bar')
        return
    caption(c, 'THE JOKE', LX, 340, pr(t, tj - 0.3, 0.3), size=30)
    bubble(c, 540, 620, 820, 260, 'MY PET IS A ROCK!', (420, 900), pr(t, tj, 0.4), size=62)
    rock(c, 540, 1090, 440, t, -4, a=pr(t, tj + 0.4, 0.4), eyes_look=math.sin(t * 2))
    if t > tn - 0.2: burst(c, 230, 1000, 105, 'NO FOOD', pr(t, tn - 0.2, 0.3), size=30, col=CYEL, rot=-8)
    if t > tn + 0.4: burst(c, 860, 1020, 105, 'NO WALKS', pr(t, tn + 0.4, 0.3), size=28, col=CCYN, rot=8)
    if t > tla - 0.2: caption(c, 'HA HA HA', 140, 1300, pr(t, tla - 0.2, 0.3), col=CYEL, size=34, rot=-3)
    if t > tm - 0.2: caption(c, '...WAIT. THAT COULD SELL.', 380, 1380 - 60, pr(t, tm - 0.2, 0.3), col=CRED, size=28, rot=2)


def sc_product(c, t, S):
    tm = ph('mexico'); tp = ph('about a penny'); tpk = ph('the packaging'); tc = ph('cardboard pet carrier'); ta = ph('air holes')
    tsn = ph('straw nest'); tman = ph('funny manual'); tob = ph('obedience'); tpd = ph('play dead')
    paper(c, t)
    if t < tpk - 0.4:
        caption(c, 'STEP 1: THE "PETS"', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
        title(c, 'BEACH STONES', 80, 540, 120, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'FROM MEXICO.', 90, 690, 120, CRED, pr(t, tm - 0.2, 0.4), rot=-2)
        photo_panel(c, 'beach', 120, 780, 840, 480, 1.2, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        coin(c, 800, 1230, 110, pr(t, tp - 0.2, 0.35), t)
        if t > tp: caption(c, 'COST: ABOUT A PENNY EACH', 140, 1320, pr(t, tp, 0.3), col=CYEL, size=28, rot=-1.5)
        credit(c, 'beach')
        return
    caption(c, 'STEP 2: THE REAL WORK', LX, 340, pr(t, tpk - 0.4, 0.3), col=CYEL, size=30)
    title(c, 'THE PACKAGING.', 80, 540, 104, CRED, pr(t, tpk - 0.2, 0.4), rot=-2)
    if t < tman - 0.3:
        photo_panel(c, 'hay', 150, 1010, 780, 300, 1.5, pr(t, tsn - 0.3, 0.4), t=t - tsn)
        box(c, 500, 960, 1.0, pr(t, tc - 0.3, 0.4), t, lid=0.55 * pr(t, tsn - 0.2, 0.5))
        if t > tsn - 0.1: rock(c, 520, 930, 280, t, 4, a=pr(t, tsn, 0.3), bob=0.4)
        if t > ta - 0.2: burst(c, 860, 700, 105, 'AIR HOLES!', pr(t, ta - 0.2, 0.3), size=28, rot=8)
        if t > tsn - 0.2: caption(c, 'A STRAW NEST', 200, 1340, pr(t, tsn - 0.2, 0.3), col=CYEL, size=28, rot=-1.5)
        if t > tsn - 0.3: credit(c, 'hay')
        return
    manual(c, 120, 680, pr(t, tman - 0.3, 0.45), -3, t, page=pr(t, tob - 0.2, 0.4) + pr(t, tpd - 0.2, 0.4))
    rock(c, 780, 1120, 340, t, -8 if t < tpd else 85, eyes_look=0)
    if t > tpd: burst(c, 780, 820, 110, 'PLAY DEAD', pr(t, tpd, 0.3), size=30, rot=6)


def sc_launch(c, t, S):
    tg = ph('gift show'); tn = ph('neiman marcus'); tw = ph('did it work'); th = ph('hundred thousand a day'); tp = ph('three ninety five')
    tk = ph('kept about'); thon = ph('honestly'); tg2 = ph("that's genius"); tmil = ph('a millionaire')
    paper(c, t)
    if t < tw - 0.3:
        caption(c, 'AUGUST 1975', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
        title(c, 'GIFT SHOW', 80, 560, 140, CBLU, pr(t, tg - 0.3, 0.4))
        title(c, 'DEBUT.', 90, 720, 150, CRED, pr(t, tg + 0.2, 0.4), rot=-2)
        def booth(cc):
            cc.drawRect(R.MakeWH(840, 440), paint((250, 236, 200))); dots(cc, (0, 0, 840, 440), CRED, cell=18, rmax=4, grad=(0.5, 1.0), a=0.3)
            cc.drawRect(R.MakeXYWH(0, 0, 840, 70), paint(CRED)); cc.drawRect(R.MakeXYWH(0, 0, 840, 70), stroke(KINK, 6))
            for i in range(8): cc.drawRect(R.MakeXYWH(i * 105, 0, 52, 70), paint(PAPER))
            cc.drawString('SAN FRANCISCO GIFT SHOW', 150, 130, font('SpecialElite.ttf', 38), paint(KINK))
            cc.drawRect(R.MakeXYWH(40, 330, 760, 30), paint((150, 100, 60))); cc.drawRect(R.MakeXYWH(40, 330, 760, 30), stroke(KINK, 6))
            for i in range(3): box(cc, 190 + i * 230, 250, 0.42, 1.0, t, label='')
        panel(c, 120, 820, 840, 440, rot=1.2, k=pr(t, S['t0'] + 0.2, 0.5), draw=booth)
        if t > tn - 0.3: mini(c, 520, 1150, 450, 200, 3, pr(t, tn - 0.3, 0.4), 'NEIMAN MARCUS', 'ORDERS!', CYEL, txtc=CRED, bigsize=60)
        return
    if t < tp - 0.3:
        bg_flat(c, CBLU, (20, 80, 170))
        caption(c, 'SO... DID IT WORK?', LX, 340, pr(t, tw - 0.3, 0.3), col=CYEL, size=30)
        if t < th - 0.5: title(c, 'DID IT WORK?', 80, 700, 130, CYEL, pr(t, tw - 0.2, 0.4), rot=-2); return
        title(c, 'UP TO', 90, 540, 120, PAPER, pr(t, th - 0.4, 0.4))
        title(c, '100,000', 80, 700, 170, CYEL, pr(t, th - 0.2, 0.4), rot=-2)
        title(c, 'A DAY.', 90, 850, 140, PAPER, pr(t, th + 0.3, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(840, 360), paint(PAPER))
            bars(cc, 80, 40, 680, 240, [('AUG', 1, '', CBLU), ('OCT', 3, '', CBLU), ('DEC', 10, '!!!', CRED)], pr(t, th - 0.3, 1.2), 10)
        panel(c, 120, 930, 840, 360, rot=1.5, k=pr(t, th - 0.4, 0.4), draw=dr)
        caption(c, "HIS ESTIMATE, HOLIDAY 1975", 160, 1320, pr(t, th + 0.6, 0.3), col=CRED, size=24, rot=-1)
        return
    if t < tmil - 0.4:
        caption(c, 'DO THE MATH', LX, 340, pr(t, tp - 0.3, 0.3), col=CCYN, size=30)
        mini(c, 80, 520, 400, 280, -2, pr(t, tp - 0.2, 0.4), 'PRICE', '$3.95', CBLU, bigsize=96)
        mini(c, 520, 540, 400, 280, 2, pr(t, tk - 0.2, 0.4), 'HE KEPT ABOUT', '95 CENTS', CRED, bigsize=60)
        coin(c, 320, 1060, 120, pr(t, thon - 0.2, 0.35), t)
        if t > thon: title(c, 'TO', 470, 1090, 80, KINK, pr(t, thon, 0.3))
        if t > thon + 0.4: burst(c, 740, 1060, 160, '~$1 PROFIT', pr(t, thon + 0.4, 0.35), size=30, rot=6)
        if t > tg2 - 0.2: caption(c, "THAT'S GENIUS.", 300, 1300, pr(t, tg2 - 0.2, 0.3), col=CYEL, size=40, rot=-3)
        return
    bg_flat(c, CYEL, (230, 170, 20))
    caption(c, 'THE RESULT', LX, 340, pr(t, tmil - 0.4, 0.3), col=PAPER, size=30)
    title(c, 'GARY DAHL,', 80, 560, 130, CBLU, pr(t, tmil - 0.3, 0.4))
    title(c, 'MILLIONAIRE.', 80, 720, 130, CRED, pr(t, tmil, 0.4), rot=-2)
    rock(c, 540, 1080, 460, t, -4, eyes_look=math.sin(t * 3))
    for i in range(7):
        coin(c, 180 + i * 120, 900 + ((t * 300 + i * 160) % 600), 46, 1.0, t + i, '$')


def sc_catch(c, t, S):
    tf = ph('fast as it started'); tx = ph('right after christmas'); tcl = ph('off a cliff'); ti = ph('inventors kept calling'); tv = ph('his verdict')
    paper(c, t)
    caption(c, 'THE CATCH?', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < ti - 0.3:
        title(c, 'GONE AS FAST', 80, 540, 116, CRED, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'AS IT CAME.', 90, 690, 120, CBLU, pr(t, tf - 0.3, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(840, 480), paint(PAPER))
            x0, y0, cw, ch = 70, 40, 720, 330
            pts = [(0.0, 0.1), (0.25, 0.35), (0.5, 0.75), (0.62, 1.0), (0.72, 0.3), (0.85, 0.08), (1.0, 0.03)]
            k = pr(t, tx - 0.3, 1.4)
            cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
            p = skia.Path(); first = True
            for fx, v in pts:
                if fx > k: break
                (p.moveTo if first else p.lineTo)(x0 + fx * cw, y0 + ch - v * ch); first = False
            cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(CRED, 9))
            for fx, s in ((0.05, 'AUG'), (0.55, 'DEC'), (0.85, 'JAN')):
                cc.drawString(s, x0 + fx * cw - 20, y0 + ch + 50, font('SpecialElite.ttf', 30), paint(KINK))
            cc.drawString('SALES (ILLUSTRATIVE)', 470, 30, font('SpecialElite.ttf', 22), paint(GREY))
        panel(c, 120, 800, 840, 480, rot=-1.2, k=pr(t, tf - 0.2, 0.4), draw=dr)
        if t > tcl - 0.3: burst(c, 820, 1100, 115, 'CRASH!', pr(t, tcl - 0.3, 0.35), size=44, rot=8)
        return
    title(c, 'INVENTORS', 80, 540, 130, CBLU, pr(t, ti - 0.3, 0.4))
    title(c, 'KEPT CALLING.', 90, 690, 112, CRED, pr(t, ti + 0.3, 0.4), rot=-2)
    for i in range(3):
        k = pr(t, ti + 0.3 * i, 0.3)
        bubble(c, 260 + i * 280, 900 + (i % 2) * 70, 230, 130, ('IDEA!', 'NEW IDEA!', 'HEAR ME OUT!')[i], (300 + i * 260, 1100), k, size=30)
    def dr(cc):
        cc.drawRect(R.MakeWH(760, 230), paint(PAPER))
        title(cc, '"THEY\'RE ALL BAD."', 40, 130, 70, CRED, 1.0, shadow=5)
        cc.drawString('GARY DAHL, TO CNN (VIA OBITUARY, 2015)', 40, 200, font('SpecialElite.ttf', 24), paint(KINK))
    panel(c, 160, 1080, 760, 230, rot=1.5, k=pr(t, tv, 0.4), draw=dr)


def sc_korea(c, t, S):
    tk = ph('south koreans'); tn = ph('name them'); td = ph('dress them'); tt = ph('talk to them'); te = ph('eleven dollars')
    paper(c, t)
    caption(c, 'NOW THE TWIST', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    if t < tn - 0.3:
        title(c, 'PET ROCKS', 80, 560, 140, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'ARE BACK.', 90, 720, 150, CRED, pr(t, S['t0'] + 0.8, 0.4), rot=-2)
        photo_panel(c, 'seoul', 120, 820, 840, 460, 1.4, pr(t, tk - 0.3, 0.5), t=t - tk)
        if t > tk - 0.2: caption(c, 'SOUTH KOREA . 2024', 160, 1300, pr(t, tk - 0.2, 0.3), col=CYEL, size=28, rot=-1.5)
        credit(c, 'seoul')
        return
    title(c, 'OWNERS...', 80, 540, 130, CBLU, pr(t, tn - 0.3, 0.4))
    mini(c, 90, 620, 290, 200, -3, pr(t, tn - 0.1, 0.35), 'THEY', 'NAME', CRED, bigsize=60)
    mini(c, 395, 640, 290, 200, 2, pr(t, td - 0.1, 0.35), 'THEY', 'DRESS', CBLU, bigsize=60)
    mini(c, 700, 620, 290, 200, -2, pr(t, tt - 0.1, 0.35), 'THEY', 'TALK TO', CYEL, txtc=CRED, bigsize=52)
    rock(c, 540, 1080, 360, t, 3, eyes_look=math.sin(t * 2))
    # tiny drawn bow tie (dress) + name tag
    if t > td:
        c.save(); c.translate(540, 1200); bw = poly([(-50, -25), (0, 0), (-50, 25)]); bw2 = poly([(50, -25), (0, 0), (50, 25)])
        for pp in (bw, bw2): c.drawPath(pp, paint(CRED)); c.drawPath(pp, stroke(KINK, 5))
        c.restore()
    if t > tn: caption(c, 'HELLO, MY NAME IS: ROCK', 620, 940, pr(t, tn, 0.3), col=PAPER, size=24, rot=5)
    if t > te - 0.3: mini(c, 140, 1180 + 20, 380, 180, -2, pr(t, te - 0.3, 0.4), 'ONLINE PRICE', 'UP TO $11', GRN, bigsize=54)


def sc_moves(c, t, S):
    t1 = ph('one sell the joke'); ts = ph('story was the product'); t2 = ph('two let the packaging'); t3 = ph('three launch before'); tf = ph('fads fade')
    paper(c, t)
    caption(c, '3 MOVES YOU CAN STEAL', LX, 340, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    items = [(t1, '1', 'SELL THE JOKE,', 'NOT THE OBJECT', CRED), (t2, '2', 'LET THE PACKAGING', 'DO THE TALKING', CBLU), (t3, '3', 'LAUNCH BEFORE', 'THE GIFT RUSH', GRN)]
    for i, (tt, n, a1, a2, col) in enumerate(items):
        k = pr(t, tt - 0.2, 0.4)
        y = 520 + i * 270
        def dr(cc, n=n, a1=a1, a2=a2, col=col):
            cc.drawRect(R.MakeWH(860, 230), paint(PAPER))
            cc.drawRect(R.MakeWH(170, 230), paint(col)); dots(cc, (0, 0, 170, 230), KINK, cell=14, rmax=3, a=0.3)
            title(cc, n, 85, 160, 150, PAPER, 1.0, 'c', shadow=6)
            title(cc, a1, 200, 100, 56, KINK, 1.0, shadow=0, outline=0.01)
            title(cc, a2, 200, 175, 56, col, 1.0, shadow=4)
        panel(c, 110, y, 860, 230, rot=(-1.5, 1.2, -1)[i], k=k, draw=dr)
    if t > ts - 0.2 and t < t2: burst(c, 860, 1330, 100, 'STORY!', pr(t, ts - 0.2, 0.3), size=34, rot=8)
    if t > tf - 0.3: burst(c, 860, 1330, 100, 'GO FAST', pr(t, tf - 0.3, 0.3), size=32, col=CRED, txt=CYEL, rot=8)


def sc_end(c, t, S):
    tl = ph('laugh first'); tz = ph('send this'); ty = ph('yes or no')
    if t < tz - 0.3:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'SO, HOW DO YOU SELL A FREE ROCK?', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=28)
        title(c, 'MAKE PEOPLE', 80, 560, 130, PAPER, pr(t, tl - 0.6, 0.4))
        title(c, 'LAUGH FIRST.', 80, 720, 136, CYEL, pr(t, tl - 0.1, 0.4), rot=-2)
        rock(c, 540, 1090, 440, t, -5, eyes_look=math.sin(t * 2.5))
        return
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, tz - 0.3, 0.3), size=30)
    title(c, 'WOULD YOU BUY', 80, 540, 112, CBLU, pr(t, tz - 0.2, 0.4))
    title(c, 'A PET ROCK?', 90, 690, 130, CRED, pr(t, tz + 0.2, 0.4), rot=-2)
    rock(c, 540, 1000, 380, t, 4, eyes_look=math.sin(t * 2))
    burst(c, 260, 1260, 105, 'YES', pr(t, ty - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 820, 1260, 105, 'NO', pr(t, ty + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    if t > END:
        c.drawCircle(540, 1000, 1400 * eio(pr(t, END, 0.9)), paint(CRED))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='question', t0=ph('so how do you sell') - 0.2, fn=with_subs(sc_question), tin='flash'),
    dict(k='dahl', t0=ph('meet gary dahl') - 0.2, fn=with_subs(sc_dahl), tin='wipe', col=SEPIA),
    dict(k='product', t0=ph('he bought smooth') - 0.2, fn=with_subs(sc_product), tin='whip'),
    dict(k='launch', t0=ph('in august') - 0.2, fn=with_subs(sc_launch), tin='zoom'),
    dict(k='catch', t0=ph('the catch') - 0.2, fn=with_subs(sc_catch), tin='whip'),
    dict(k='korea', t0=ph('now the twist') - 0.2, fn=with_subs(sc_korea), tin='flash'),
    dict(k='moves', t0=ph('okay here are three') - 0.2, fn=with_subs(sc_moves), tin='whip'),
    dict(k='end', t0=ph('so how do you sell something free') - 0.2, fn=with_subs(sc_end), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('one and a half million'), 8, 0.3)
EP.shk(ph('a millionaire'), 10, 0.3)
EP.shk(ph('off a cliff'), 10, 0.3)
EP.flash(ph('play dead'), 0.4)

if __name__ == '__main__':
    EP.main(sys.argv)
