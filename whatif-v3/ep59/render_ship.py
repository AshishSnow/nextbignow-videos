"""NextBigNow ep 59 (vintage comic, SPACE palette: navy + orange + cyan; small subtitles; v5 voice; new logo watermark): What if rockets become as reusable as airplanes?
Facts: Space.com (14 Nov 2026) - Starship Flight 15 launched Fri 13 Nov from Starbase, Texas; Ship 42 caught by tower "chopsticks" ~22.5 h after liftoff,
first catch of a vehicle returning from orbit ("missing link"); 26 Starlink V3 deployed; Super Heavy booster diverted to Gulf of Mexico after low-fuel
alarm. Space Shuttle avg cost ~$1.5B per flight (program ~$209B / 135 flights). Falcon 9 first booster landing 21 Dec 2015 (LZ-1); some boosters 25+ flights.
Photos (Wikimedia Commons): see ship/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('SH_DIR', 'ship'))
PK.IMG = os.path.join(HERE, 'ship', 'img')
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



NAVY = (22, 34, 84); NAVY_D = (14, 22, 58); ORNG = (255, 138, 36); SKY = (215, 228, 245)


def space_bg(c, t):
    bg_flat(c, NAVY, NAVY_D)
    for i in range(70):
        x = hsh(i, 3) * W; y = hsh(i, 4) * H; r = 1.5 + 3 * hsh(i, 5)
        tw = 0.5 + 0.5 * math.sin(t * 2 + i)
        c.drawCircle(x, y, r, paint(PAPER, 0.35 + 0.5 * tw))


def rocket(c, x, y, s, rot, a=1.0, flame=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    body = poly([(-22, -150), (22, -150), (22, 110), (-22, 110)])
    nose = poly([(-22, -150), (0, -200), (22, -150)])
    fins = [poly([(-22, 60), (-50, 120), (-22, 110)]), poly([(22, 60), (50, 120), (22, 110)])]
    if flame > 0:
        fl = poly([(-16, 110), (0, 110 + 120 * flame * (0.85 + 0.15 * math.sin(x))), (16, 110)])
        c.drawPath(fl, paint(ORNG, a)); c.drawPath(fl, stroke(KINK, 4, a=a))
    for p in fins + [body, nose]:
        c.save(); c.translate(5, 5); c.drawPath(p, paint(KINK, a)); c.restore()
    for p in fins: c.drawPath(p, paint(ORNG, a)); c.drawPath(p, stroke(KINK, 5, a=a))
    c.drawPath(body, paint(SKY, a)); c.drawPath(body, stroke(KINK, 6, a=a))
    c.drawPath(nose, paint(SKY, a)); c.drawPath(nose, stroke(KINK, 6, a=a))
    c.drawCircle(0, -80, 12, paint(CCYN, a)); c.drawCircle(0, -80, 12, stroke(KINK, 4, a=a))
    c.restore()


def sc_hook(c, t, S):
    tt = ph('a giant tower caught it'); ta = ph('two metal arms'); ts = ph('right out of the sky'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t, tint=SKY)
        caption(c, 'TEXAS . NOV 14, 2026', LX, 340, 1.0, col=ORNG, size=30)
        title(c, 'CAUGHT', 80, 540, 170, CBLU, 1.0, rot=-2)
        title(c, 'FROM SPACE.', 90, 690, 130, ORNG, pr(t, tt - 0.2, 0.4))
        photo_panel(c, 'K5_superheavy', 120, 770, 840, 580, 1.5, 1.0, zoom=1.15, fy=0.3, t=t)
        if t > ta - 0.2: burst(c, 820, 830, 120, 'TWO ARMS!', pr(t, ta - 0.2, 0.35), size=38, col=ORNG, txt=PAPER, rot=8)
        if t > ts - 0.2: caption(c, 'THE TOWER GRABS THE ROCKET MIDAIR', 150, 1300, pr(t, ts - 0.2, 0.3), col=CCYN, size=26, rot=-1.5)
        credit(c, 'K5_superheavy')
        return
    space_bg(c, t)
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=ORNG, size=30)
    title(c, 'WHAT IF ROCKETS', 80, 540, 116, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'WORK LIKE', 90, 680, 130, CCYN, pr(t, tq + 0.2, 0.4))
    title(c, 'AIRPLANES?', 90, 820, 140, ORNG, pr(t, tq + 0.45, 0.4))
    k = pr(t, tq + 0.5, 0.6)
    yy = 1250 - 160 * eio(pr(t, tq + 0.8, 2.0))
    rocket(c, 540, yy, 1.6 * eback(cl(k), 1.4), -4 + 2 * math.sin(t * 3), a=k, flame=k)


def sc_what(c, t, S):
    tf = ph('friday evening'); t22 = ph('twenty two hours'); t26 = ph('twenty six satellites'); tb = ph('back through the atmosphere'); tg = ph('grabbed it in midair'); tfi = ph('first time anyone'); tm = ph('the missing link')
    paper(c, t, tint=SKY)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tb - 0.3:
        title(c, 'STARSHIP', 90, 540, 160, CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'FLIGHT 15', 90, 690, 130, ORNG, pr(t, tf - 0.2, 0.4), rot=-2)
        mini(c, 90, 790, 430, 280, -2, pr(t, t22 - 0.3, 0.4), 'TIME IN SPACE', '~22 HRS', NAVY, bigsize=74)
        mini(c, 560, 810, 430, 280, 1.5, pr(t, t26 - 0.3, 0.4), 'SATELLITES DROPPED', '26', ORNG, bigsize=110)
        photo_panel(c, 'K1_tower', 200, 1120, 680, 220, -1, pr(t, tf, 0.5), t=t - tf)
        credit(c, 'K1_tower')
        return
    title(c, 'CAUGHT', 90, 540, 160, CBLU, pr(t, tg - 0.3, 0.4))
    title(c, 'MIDAIR.', 90, 690, 160, ORNG, pr(t, tg, 0.4), rot=-2)
    photo_panel(c, 'K5_superheavy', 140, 780, 800, 520, 1.5, pr(t, tb - 0.2, 0.5), zoom=1.3, fy=0.35, t=t - tb)
    if t > tfi - 0.2: burst(c, 800, 830, 125, 'FIRST EVER', pr(t, tfi - 0.2, 0.35), size=36, col=CCYN, txt=NAVY, rot=8)
    if t > tm - 0.3: caption(c, '"THE MISSING LINK" . SPACEX', 220, 1260, pr(t, tm - 0.3, 0.3), col=ORNG, size=28, rot=-2)
    credit(c, 'K5_superheavy')


def sc_why(c, t, S):
    tw = ph('rockets were thrown away'); ti = ph('imagine flying'); tth = ph('throwing the plane'); te = ph('every launch meant')
    paper(c, t, tint=SKY)
    caption(c, 'WHY DOES THAT MATTER?', LX, 340, pr(t, S['t0'], 0.3), col=ORNG, size=30)
    title(c, 'ROCKETS WERE', 80, 540, 120, CBLU, pr(t, tw - 0.3, 0.4))
    title(c, 'TRASH.', 90, 700, 170, ORNG, pr(t, tw + 0.3, 0.4), rot=-3)
    if t > ti - 0.3:
        caption(c, 'NEW YORK -> LONDON...', 120, 840, pr(t, ti - 0.3, 0.3), col=CCYN, size=34, rot=-2)
        k = pr(t, ti, (tth + 0.6) - ti)
        px = 200 + 600 * eio(cl(k / 0.7)); py = 1050 + (300 * eio(cl((k - 0.7) / 0.3)) if k > 0.7 else 0)
        rocket(c, px, py, 0.9, 90 + 60 * cl((k - 0.7) / 0.3), flame=0.6 if k < 0.7 else 0)
        c.drawRect(R.MakeXYWH(60, 1290, 960, 60), paint(CBLU)); dots(c, (60, 1290, 960, 60), KINK, cell=14, rmax=3, grad=(0, 1), a=0.25)
        if t > tth: burst(c, 820, 1180, 110, 'SPLASH!', pr(t, tth + 0.2, 0.35), size=40, col=CCYN, txt=NAVY, rot=8)
    if t > te - 0.2: caption(c, 'EVERY LAUNCH = A BRAND-NEW ROCKET', 110, 960, pr(t, te - 0.2, 0.3), col=ORNG, size=28, rot=1.5)


def sc_reuse(c, t, S):
    ts = ph('space shuttle'); t15 = ph('one and a half billion'); tm = ph('months of repairs'); td = ph('december twenty fifteen'); tl = ph('landed a falcon'); ti = ph('it was impossible'); t25 = ph('more than twenty five times')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN WHAT REUSE CAN DO", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < td - 0.3:
        title(c, 'THE SHUTTLE:', 80, 540, 130, CBLU, pr(t, ts - 0.2, 0.4))
        title(c, '~$1.5B A FLIGHT', 80, 690, 110, ORNG, pr(t, t15 - 0.3, 0.4), rot=-2)
        photo_panel(c, 'K4_shuttle', 90, 770, 900, 560, 1.2, pr(t, ts, 0.5), t=t - ts)
        if t > tm - 0.2: burst(c, 800, 830, 120, 'MONTHS OF REPAIRS', pr(t, tm - 0.2, 0.35), size=26, rot=8)
        credit(c, 'K4_shuttle')
        return
    title(c, 'DEC 2015:', 90, 540, 150, CBLU, pr(t, td - 0.3, 0.4))
    title(c, 'IT LANDED.', 90, 690, 150, ORNG, pr(t, tl, 0.4), rot=-2)
    photo_panel(c, 'K2_boosterland', 90, 770, 900, 560, 1.2, pr(t, tl - 0.2, 0.5), fy=0.45, t=t - tl)
    if t > ti - 0.3: caption(c, '"IMPOSSIBLE," THEY SAID', 150, 860, pr(t, ti - 0.3, 0.3), col=PAPER, size=32, rot=-3)
    if t > t25 - 0.3: burst(c, 780, 1220, 125, '25+ FLIGHTS', pr(t, t25 - 0.3, 0.35), size=38, col=ORNG, txt=PAPER, rot=8)
    credit(c, 'K2_boosterland')


def sc_both(c, t, S):
    tb = ph('reuse both halves'); tl = ph('land refuel inspect'); tc = ph('launches get cheap'); tm = ph('more satellites'); tf = ph('faster internet'); tmo = ph('moon and mars')
    space_bg(c, t)
    caption(c, 'NEXT: REUSE BOTH HALVES', LX, 340, pr(t, S['t0'], 0.3), col=ORNG, size=30)
    if t < tc - 0.3:
        title(c, 'LIKE AN', 90, 540, 150, PAPER, pr(t, tb - 0.2, 0.4))
        title(c, 'AIRLINE.', 90, 690, 160, CCYN, pr(t, tb + 0.4, 0.4), rot=-2)
        for i, (s_, col) in enumerate((('LAND', ORNG), ('REFUEL', CCYN), ('INSPECT', PAPER), ('FLY AGAIN', CYEL))):
            kk = pr(t, tl - 0.2 + 0.45 * i, 0.35)
            if kk <= 0: continue
            caption(c, '%d. %s' % (i + 1, s_), 140 + (i % 2) * 300, 860 + i * 110, kk, col=col, size=40, rot=(-2, 1.5, -1, 2)[i])
        return
    title(c, 'CHEAP LAUNCH =', 80, 540, 110, PAPER, pr(t, tc - 0.3, 0.4))
    title(c, 'NEW WORLD.', 90, 690, 150, ORNG, pr(t, tc + 0.3, 0.4), rot=-2)
    for i, (t0, s_, col) in enumerate(((tm, 'MORE SATELLITES', CCYN), (tf, 'FASTER INTERNET FROM SPACE', PAPER), (tmo, 'CARGO TO THE MOON + MARS', CYEL))):
        caption(c, s_, 120 + (i % 2) * 50, 860 + i * 120, pr(t, t0 - 0.2, 0.3), col=col, size=32, rot=(-2, 1.5, -1)[i])
    k = pr(t, tc, 0.6)
    rocket(c, 870, 1260 - 120 * eio(pr(t, tc + 0.4, 3.0)), 0.9 * eback(cl(k), 1.4), 4, a=k, flame=k)


def sc_notyet(c, t, S):
    tb = ph('the booster got'); tlf = ph('low fuel alarm'); tg = ph('gulf of mexico'); tn = ph('the next big test')
    paper(c, t, tint=SKY)
    caption(c, "BUT IT'S NOT DONE YET", LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    title(c, 'BOOSTER:', 90, 540, 150, CBLU, pr(t, tb - 0.2, 0.4))
    title(c, 'SPLASHDOWN.', 80, 690, 130, CRED, pr(t, tg - 0.3, 0.4), rot=-2)
    photo_panel(c, 'K3_droneship', 90, 770, 900, 520, 1.2, pr(t, tb, 0.5), t=t - tb)
    if t > tlf - 0.2: burst(c, 800, 830, 120, 'LOW FUEL!', pr(t, tlf - 0.2, 0.35), size=38, rot=8)
    if t > tn - 0.3: caption(c, 'NEXT TEST: CATCH BOTH HALVES', 140, 1250, pr(t, tn - 0.3, 0.3), col=ORNG, size=30, rot=-2)
    credit(c, 'K3_droneship')


def sc_predict(c, t, S):
    tf = ph('feel normal'); tr = ph('turnaround time'); th = ph('hours instead of months'); tc = ph('a lot cheaper')
    space_bg(c, t)
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=ORNG, size=30)
    title(c, 'CATCHING ROCKETS', 80, 540, 104, PAPER, pr(t, S['t0'] + 0.3, 0.4))
    title(c, '= NORMAL.', 90, 680, 150, CCYN, pr(t, tf - 0.2, 0.4), rot=-2)
    if t > tr - 0.3: caption(c, 'THE REAL RACE: TURNAROUND TIME', 110, 850, pr(t, tr - 0.3, 0.3), col=ORNG, size=30, rot=-2)
    if t > th - 0.3:
        mini(c, 90, 950, 430, 260, -2, pr(t, th - 0.3, 0.4), 'TODAY', 'MONTHS', CRED, bigsize=70)
        mini(c, 560, 970, 430, 260, 1.5, pr(t, th + 0.4, 0.4), 'THE GOAL', 'HOURS', GRN, bigsize=80)
    if t > tc - 0.3: burst(c, 800, 1300, 100, 'CHEAPER!', pr(t, tc - 0.3, 0.35), size=34, col=CYEL, txt=NAVY, rot=8)


def sc_ask(c, t, S):
    space_bg(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), col=ORNG, size=30)
    title(c, 'SPACE FOR THE', 80, 530, 112, PAPER, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'PRICE OF A', 90, 660, 130, CCYN, pr(t, S['t0'] + 0.3, 0.4))
    title(c, 'PLANE TICKET?', 80, 800, 120, ORNG, pr(t, S['t0'] + 0.5, 0.4))
    k = pr(t, S['t0'] + 0.6, 0.6)
    rocket(c, 540, 1120 - 30 * math.sin(t * 2), 1.0 * eback(cl(k), 1.4), 0, a=k, flame=k)
    burst(c, 230, 1250, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(ORNG))


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='what', t0=ph("here's what happened") - 0.2, fn=with_subs(sc_what), tin='whip'),
    dict(k='why', t0=ph('why does that matter') - 0.2, fn=with_subs(sc_why), tin='zoom'),
    dict(k='reuse', t0=ph("we've seen what reuse") - 0.2, fn=with_subs(sc_reuse), tin='wipe', col=SEPIA),
    dict(k='both', t0=ph('now starship wants') - 0.2, fn=with_subs(sc_both), tin='flash'),
    dict(k='notyet', t0=ph("but it's not done") - 0.2, fn=with_subs(sc_notyet), tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('grabbed it in midair'), 10, 0.3)
EP.shk(ph('throwing the plane'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
