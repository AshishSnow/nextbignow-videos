"""NextBigNow ep 58 (vintage comic + editorial, small subtitles, v5 voice): What happens when air traffic control goes dark?
Facts: FAA statement (13 Nov 2026) - nationwide ground stop, "communication issues impacting multiple Air Route Traffic Control Centers".
Al Jazeera (13 Nov 2026) - ordered 3:54pm ET, lifted 8:15pm ET; all 22 ARTCCs; FlightAware via CBS: >10,000 delays, >=4,000 cancellations;
~1.5M passengers (AP); 4,042 flights airborne heading to US airports (Flightradar24); DHS: no sign of threat; FBI: not believed cyberattack;
Congress approved $12.5B for ATC overhaul last year; administration seeks $30.1B more. NPR (13 Nov 2026) - Duffy: "old switches, old routers",
"1980s little copper lines", system "got overloaded"; second nationwide stop since 9/11, first Jan 2023 (contract workers deleted files).
Jan 11 2023 NOTAM outage: >10,000 delays, ~1,300 cancellations.
Photos (Wikimedia Commons): see atc/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('AT_DIR', 'atc'))
PK.IMG = os.path.join(HERE, 'atc', 'img')
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



def plane(c, x, y, s, rot, col=PAPER, a=1.0):
    """simple comic plane silhouette pointing right."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = poly([(-50, -6), (30, -8), (50, 0), (30, 8), (-50, 6)])
    w = poly([(-5, 0), (10, -45), (22, -45), (14, 0), (22, 45), (10, 45)])
    tl = poly([(-50, 0), (-42, -20), (-34, -20), (-38, 0), (-34, 20), (-42, 20)])
    for pp in (w, tl, p):
        c.save(); c.translate(3, 3); c.drawPath(pp, paint(KINK, a)); c.restore()
        c.drawPath(pp, paint(col, a)); c.drawPath(pp, stroke(KINK, 3, a=a))
    c.restore()


def sc_hook(c, t, S):
    ts = ph('every airport in america'); tn = ph('no takeoffs'); t4 = ph('four thousand planes'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'USA . NOV 13 . 3:54 PM ET', LX, 340, 1.0, col=CYEL, size=30)
        title(c, 'EVERY AIRPORT.', 80, 540, 120, CBLU, 1.0, rot=-2)
        title(c, 'STOPPED.', 90, 690, 160, CRED, pr(t, ts + 0.4, 0.4))
        k = pr(t, 0, 0.6)
        place(c, 'A5_tower_comic.png', 400, 1100, 520 * eback(cl(k), 1.4), rot=-2, a=k, shadow=True)
        frz = pr(t, ts + 0.5, 0.4)
        for i in range(5):
            ang = t * 0.6 * (1 - frz) + i * 1.256
            px, py = 600 + 300 * math.cos(ang), 1050 + 180 * math.sin(ang)
            if t > t4 - 0.2 or i < 2:
                plane(c, px, py, 1.3, math.degrees(ang) + 90, col=CYEL if frz < 1 else PAPER, a=1.0)
        if t > tn - 0.2: burst(c, 840, 820, 115, 'NO TAKEOFFS', pr(t, tn - 0.2, 0.35), size=32, rot=8)
        if t > t4 - 0.2: caption(c, '4,000+ PLANES ALREADY IN THE AIR', 140, 1310, pr(t, t4 - 0.2, 0.3), col=CRED, size=28, rot=-1.5)
        credit(c, 'A5_tower')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF AIR', 90, 540, 140, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, 'TRAFFIC CONTROL', 80, 680, 110, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'GOES DARK?', 90, 820, 140, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.5, 0.5); dk = pr(t, tq + 1.1, 1.0)
    def dr(cc):
        cover(cc, img('A1_controllers_comic.png'), 0, 0, 800, 400, 1.1, 0.3, 0.5)
        cc.drawRect(R.MakeWH(800, 400), paint(KINK, 0.8 * dk))
        if dk > 0.5: title(cc, 'NO SIGNAL', 400, 230, 90, CRED, pr(t, tq + 1.8, 0.3), 'c', shadow=5)
    panel(c, 140, 920, 800, 400, rot=-2, k=kk, draw=dr)


def sc_what(c, t, S):
    tr = ph('radar and radio'); t22 = ph('twenty two'); tf = ph('froze the whole'); t4 = ph('more than four hours'); tc = ph('thousands of flights'); tp = ph('one and a half million')
    paper(c, t)
    caption(c, "HERE'S WHAT HAPPENED", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tf - 0.3:
        title(c, 'RADAR + RADIO', 80, 540, 116, CBLU, pr(t, tr - 0.3, 0.4))
        title(c, 'FAILING.', 90, 690, 160, CRED, pr(t, tr + 0.4, 0.4), rot=-2)
        photo_panel(c, 'A1_controllers', 90, 780, 900, 540, 1.2, pr(t, S['t0'] + 0.3, 0.5), fx=0.3, t=t - S['t0'])
        if t > t22 - 0.2: burst(c, 820, 830, 125, 'ALL 22 CENTERS', pr(t, t22 - 0.2, 0.35), size=30, rot=8)
        caption(c, 'AN FAA RADAR ROOM', 200, 1270, pr(t, S['t0'] + 0.8, 0.3), col=CYEL, size=24)
        credit(c, 'A1_controllers')
        return
    title(c, 'AMERICA,', 90, 540, 150, CBLU, pr(t, tf - 0.3, 0.4))
    title(c, 'FROZEN.', 90, 690, 160, CRED, pr(t, tf + 0.2, 0.4), rot=-2)
    mini(c, 90, 790, 430, 260, -2, pr(t, t4 - 0.2, 0.4), 'GROUND STOP', '4+ HOURS', CBLU, bigsize=66)
    mini(c, 560, 810, 430, 260, 1.5, pr(t, tc - 0.2, 0.4), 'FLIGHTS CANCELED', 'THOUSANDS', CRED, bigsize=54)
    mini(c, 200, 1090, 680, 250, -1, pr(t, tp - 0.3, 0.4), 'PASSENGERS STUCK (AP)', '~1.5 MILLION', CYEL, txtc=CRED, bigsize=66)


def sc_cause(c, t, S):
    tn = ph('not a cyberattack'); to = ph('old equipment'); tsw = ph('old switches'); trt = ph('old routers'); tcu = ph('copper lines'); tov = ph('overloaded with data'); tst = ph('still being investigated')
    paper(c, t)
    caption(c, 'AND THE CAUSE?', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tsw - 0.4:
        title(c, 'NOT A HACK.', 90, 560, 150, GRN, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'OLD GEAR.', 90, 720, 160, CRED, pr(t, to - 0.2, 0.4), rot=-2)
        photo_panel(c, 'A4_radar', 140, 820, 800, 460, 1.5, pr(t, to, 0.5), t=t - to)
        credit(c, 'A4_radar')
        return
    title(c, 'BLAMED ON:', 90, 540, 140, CBLU, pr(t, tsw - 0.4, 0.4))
    mini(c, 90, 640, 430, 250, -2, pr(t, tsw - 0.2, 0.4), 'OLD', 'SWITCHES', CRED, bigsize=60)
    mini(c, 560, 660, 430, 250, 1.5, pr(t, trt - 0.2, 0.4), 'OLD', 'ROUTERS', CBLU, bigsize=60)
    mini(c, 200, 950, 680, 260, -1, pr(t, tcu - 0.3, 0.4), 'COPPER LINES FROM THE', '1980s', CYEL, txtc=CRED, bigsize=90)
    if t > tov - 0.3: burst(c, 800, 1260, 120, 'OVERLOAD!', pr(t, tov - 0.3, 0.35), size=40, rot=8)
    if t > tst - 0.4: caption(c, 'EXACT CAUSE: UNDER INVESTIGATION', 110, 1300, pr(t, tst - 0.4, 0.3), col=PAPER, size=24, rot=-1)


def sc_2023(c, t, S):
    tj = ph('in january twenty twenty three'); tcr = ph('crashed overnight'); tg = ph('whole country was grounded'); tc = ph('contract workers'); td = ph('deleted files'); t10 = ph('ten thousand flights')
    paper(c, t, tint=SEPIA)
    caption(c, 'THIS HAS HAPPENED BEFORE', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'JAN 2023:', 90, 540, 150, CBLU, pr(t, tj - 0.2, 0.4))
    title(c, 'GROUNDED AGAIN.', 80, 690, 112, CRED, pr(t, tj + 1.0, 0.4), rot=-2)
    if t < tc - 0.3:
        photo_panel(c, 'A3_board', 90, 780, 900, 520, 1.2, pr(t, S['t0'] + 0.4, 0.5), t=t - S['t0'])
        credit(c, 'A3_board')
        return
    mini(c, 90, 790, 430, 280, -2, pr(t, tc - 0.2, 0.4), 'THE CAUSE', 'DELETED FILES', CRED, bigsize=42)
    mini(c, 560, 810, 430, 280, 1.5, pr(t, td + 0.4, 0.4), 'WHO', 'CONTRACTORS', CBLU, bigsize=46)
    mini(c, 200, 1110, 680, 240, -1, pr(t, t10 - 0.3, 0.4), 'FLIGHTS DELAYED', '10,000+', CYEL, txtc=CRED, bigsize=80)


def sc_fragile(c, t, S):
    tl = ph('fixing a plane while'); tw = ph('every single second'); ts = ph('switch it off'); t12 = ph('twelve and a half billion'); t30 = ph('thirty billion more')
    paper(c, t)
    caption(c, 'WHY IS IT SO FRAGILE?', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < t12 - 0.4:
        title(c, 'FIXING A PLANE', 80, 540, 110, CBLU, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'MID-FLIGHT.', 90, 690, 150, CRED, pr(t, tl, 0.4), rot=-2)
        for i in range(3):
            plane(c, 300 + 240 * i, 950 + 40 * math.sin(t * 2 + i), 2.0, -8 + 6 * math.sin(t + i), col=(CYEL, PAPER, CCYN)[i])
        if t > tw - 0.2: caption(c, 'IT MUST WORK EVERY SECOND', 130, 1150, pr(t, tw - 0.2, 0.3), col=CRED, size=32, rot=-2)
        if t > ts - 0.2: burst(c, 780, 1260, 115, 'NO OFF SWITCH', pr(t, ts - 0.2, 0.35), size=28, rot=8)
        return
    title(c, 'THE FIX:', 90, 540, 150, CBLU, pr(t, t12 - 0.4, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 560), paint(PAPER))
        bars(cc, 140, 120, 620, 320, [('APPROVED', 12.5, '$12.5B', GRN), ('REQUESTED', 30.1, '$30B', CRED)], pr(t, t12, (t30 + 0.6) - t12), 34)
        cc.drawString('AIR TRAFFIC CONTROL OVERHAUL', 30, 540, font('SpecialElite.ttf', 22), paint(KINK))
    panel(c, 90, 700, 900, 560, rot=1.0, k=pr(t, t12 - 0.2, 0.5), draw=dr)


def sc_predict(c, t, S):
    tl = ph("won't be the last"); ty = ph('take years'); t80 = ph('technology from the'); ts = ph('incredibly safe'); tg = ph('planes stay on the ground'); te = ph('more days like'); tb = ph('book early flights'); tp = ph('plan b')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < ts - 0.3:
        title(c, 'NOT THE', 90, 540, 150, PAPER, pr(t, tl - 0.3, 0.4))
        title(c, 'LAST ONE.', 90, 690, 150, CYEL, pr(t, tl + 0.2, 0.4))
        caption(c, 'NEW SYSTEM: YEARS AWAY', 120, 860, pr(t, ty - 0.2, 0.3), col=PAPER, size=32, rot=-2)
        if t > t80 - 0.2: caption(c, 'UNTIL THEN: 1980s TECH', 160, 980, pr(t, t80 - 0.2, 0.3), col=CYEL, size=32, rot=1.5)
        return
    title(c, 'STILL', 90, 540, 150, PAPER, pr(t, ts - 0.3, 0.4))
    title(c, 'SAFE.', 90, 690, 160, CYEL, pr(t, ts, 0.4), rot=-2)
    caption(c, 'WHEN IT BREAKS, PLANES STAY DOWN', 110, 850, pr(t, tg - 0.3, 0.3), col=PAPER, size=30, rot=-2)
    if t > te - 0.2: caption(c, 'BUT EXPECT MORE DAYS LIKE FRIDAY', 140, 970, pr(t, te - 0.2, 0.3), col=CYEL, size=30, rot=1.5)
    if t > tb - 0.3: burst(c, 330, 1220, 120, 'FLY EARLY', pr(t, tb - 0.3, 0.35), size=38, col=CYEL, txt=CRED, rot=-6)
    if t > tp - 0.3: burst(c, 780, 1240, 115, 'PLAN B!', pr(t, tp - 0.3, 0.35), size=44, rot=8)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'WOULD YOU FLY', 80, 530, 116, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'NEXT WEEK?', 90, 670, 140, CRED, pr(t, S['t0'] + 0.3, 0.4))
    kc = pr(t, S['t0'] + 0.3, 0.5)
    place(c, 'A5_tower_comic.png', 540, 1000, 400 * eback(cl(kc), 1.4), rot=-2, a=kc, shadow=True)
    plane(c, 300 + 100 * math.sin(t), 860, 1.1, -10, col=CYEL, a=kc)
    burst(c, 230, 1250, 100, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 850, 1250, 100, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=60)
    credit(c, 'A5_tower')
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
    dict(k='cause', t0=ph('and the cause') - 0.2, fn=with_subs(sc_cause), tin='zoom'),
    dict(k='y2023', t0=ph('and this has happened') - 0.2, fn=with_subs(sc_2023), tin='wipe', col=SEPIA),
    dict(k='fragile', t0=ph('so why is it') - 0.2, fn=with_subs(sc_fragile), tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('every airport in america'), 10, 0.3)
EP.shk(ph('froze the whole'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
