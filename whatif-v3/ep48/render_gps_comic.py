"""NextBigNow ep 48 in the new VINTAGE COMIC + EDITORIAL style (same voice, facts and timings as render_gps.py)."""
import sys, os, math
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode
import render_gps as G
from render_gps import ph, END, DURATION

PK.IMG = G.PK.IMG
LX = 90
NAVY = (22, 40, 92)


def credit(c, s, a=1.0, col=(120, 100, 70), y=1480):
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def sticker_pop(k): return eback(cl(k), 1.8)


def map_panel(c, t, jamk, k=1.0):
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 620), paint(NAVY))
        dots(cc, (0, 0, 900, 620), (40, 70, 150), cell=22, rmax=8, grad=(0.0, 1.0))
        for i in range(4):
            ph_ = (t * 0.8 + i / 4) % 1; r = 80 + 420 * ph_
            p = skia.Path(); p.addArc(R.MakeXYWH(730 - r, 40 - r, 2 * r, 2 * r), 95, 70)
            col = CRED if jamk > 0.5 else CCYN
            fl = 1.0 if jamk < 0.5 else (0.3 + 0.7 * (math.sin(t * 40 + i) > 0))
            cc.drawPath(p, stroke(col, 10, (1 - ph_) * fl))
        cc.drawCircle(720, 470, 20, paint(CYEL)); cc.drawCircle(720, 470, 20, stroke(KINK, 5))
        cc.drawString('TARTU', 750, 482, font('LuckiestGuy.ttf', 40), paint(PAPER))
    panel(c, 90, 860, 900, 620, rot=1.5, k=k, draw=dr)


# ================================================================== scenes
def sc_hook(c, t, S):
    tt = ph('turn around'); tj = ph('jamming their gps'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, 'APRIL 2024 . ESTONIA', LX, 318, size=30)
        title(c, 'JAMMED!', 520, 640, 196, CRED, align='c', rot=-3)
        text(c, "2 jets couldn't land.", 540, 760, 'blk', 66, KINK, 'c')
        jamk = pr(t, tj - 0.6, 0.4)
        map_panel(c, t, jamk)
        place(c, 'G1_sat_cut_comic.png', 820, 900 + 8 * math.sin(t * 1.5), 300, rot=-10, shadow=False)
        k_turn = eio(pr(t, tt - 0.2, 1.4))
        px = lerp(380, 560, eo(pr(t, 0.0, 2.2))) - 220 * k_turn
        py = 1250 + 20 * math.sin(t * 2) + 90 * math.sin(math.pi * k_turn)
        place(c, 'G6_plane_cut_comic.png', px, py, 620, rot=-10 + 30 * math.sin(math.pi * k_turn), flip=k_turn > 0.5, shadow=False)
        if t > tj - 0.4: burst(c, 250, 1030, 115, 'ZZZT!', pr(t, tj - 0.4, 0.35), size=50, rot=-8)
        if t > tt: caption(c, 'BOTH TURNED AROUND!', 300, 1400, pr(t, tt, 0.3), col=PAPER, size=30, rot=2)
        credit(c, 'PHOTOS: MARCUSOBAL CC BY-SA 3.0 (ILLUSTRATIVE) . USAF PD')
        return
    bg_flat(c, CRED, (190, 20, 30))
    k = pr(t, tq - 0.1, 0.4)
    caption(c, 'THE REAL QUESTION...', LX, 318, k, col=PAPER, size=30)
    title(c, 'WHAT IF', 90, 560, 150, CYEL, pr(t, tq - 0.05, 0.4))
    title(c, 'GPS GOES', 90, 720, 150, PAPER, pr(t, tq + 0.15, 0.4))
    title(c, 'DOWN?', 90, 880, 190, CYEL, pr(t, tq + 0.35, 0.4))
    kk = pr(t, tq + 0.3, 0.6)
    place(c, 'G1_sat_cut_comic.png', 560, 1230 + 10 * math.sin(t * 1.4), 780 * sticker_pop(kk), rot=-8, a=kk, shadow=False)
    credit(c, 'ARTWORK: U.S. AIR FORCE . PUBLIC DOMAIN', col=(255, 210, 210))


def sc_what(c, t, S):
    tb = ph('banks cell towers'); tm = ph('millionth of a second')
    if t < tb - 0.6:
        paper(c, t)
        caption(c, "IT'S NOT JUST MAPS", LX, 318, pr(t, S['t0'], 0.3), col=CCYN, size=30)
        title(c, '~30 SATELLITES.', 90, 520, 112, KINK if False else CBLU, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'ONE WEAK SIGNAL.', 90, 650, 112, CRED, pr(t, ph('super weak') - 0.2, 0.4))
        c.drawCircle(540 + 12, 1150 + 12, 330, paint(KINK)); c.drawCircle(540, 1150, 330, paint(CYEL))
        dots(c, (210, 820, 660, 660), (235, 170, 20), cell=18, rmax=6, grad=(0.3, 1.0))
        c.drawCircle(540, 1150, 330, stroke(KINK, 9))
        kk = pr(t, S['t0'] + 0.3, 0.6)
        place(c, 'G1_sat_cut_comic.png', 540, 1130 + 14 * math.sin(t * 1.3), 820 * sticker_pop(kk), rot=-6, a=kk, shadow=False)
        if t > ph('space force') - 0.2: caption(c, 'RUN BY THE U.S. SPACE FORCE', 230, 1420, pr(t, ph('space force') - 0.2, 0.3), size=28)
        credit(c, 'ARTWORK: U.S. AIR FORCE . PUBLIC DOMAIN')
        return
    paper(c, t)
    caption(c, 'IT ALSO TELLS THE TIME', LX, 318, size=30)
    title(c, 'TICK. TOCK.', 90, 520, 130, CRED, pr(t, tb - 0.6, 0.4))
    for i, (p_, s, col, tc) in enumerate((('banks', 'BANKS', CYEL, KINK), ('cell towers', 'CELL TOWERS', CCYN, KINK), ('power grids', 'POWER GRIDS', CRED, PAPER))):
        k = pr(t, ph(p_) - 0.15, 0.35)
        def dr(cc, s=s, col=col, tc=tc):
            cc.drawRect(R.MakeWH(700, 130), paint(col))
            title(cc, s, 350, 92, 70, PAPER, 1.0, 'c', shadow=5)
        panel(c, 190, 640 + i * 175, 700, 130, rot=(-2, 1.5, -1)[i], k=k, draw=dr, border=7, shadow=10)
    if t > tm - 0.4:
        burst(c, 540, 1340, 190, '1/1,000,000', pr(t, tm - 0.4, 0.4), col=PAPER, txt=CBLU, size=48, spikes=18)
        caption(c, 'OF A SECOND!', 380, 1470, pr(t, tm, 0.3), size=28)


def sc_tartu(c, t, S):
    tn = ph('needed gps'); tc = ph("simply couldn't come in"); tf = ph('flew back to helsinki'); tr = ph('shut the whole route')
    paper(c, t)
    caption(c, 'MEANWHILE, IN TARTU...', LX, 318, pr(t, S['t0'], 0.3), size=32)
    if t < tf - 0.4:
        title(c, 'NO GPS.', 90, 520, 140, CBLU, pr(t, tn - 0.4, 0.4))
        title(c, 'NO LANDING.', 90, 670, 140, CRED, pr(t, tn, 0.4))
        def dr(cc):
            cover(cc, img('G3_tartu_comic.png'), 0, 0, 900, 640, 1.0 + 0.015 * (t - S['t0']), 0.65, 0.5)
        panel(c, 90, 760, 900, 640, rot=-1.5, k=pr(t, S['t0'] + 0.3, 0.5), draw=dr)
        if t > tc - 0.3: bubble(c, 700, 860, 380, 170, 'NO SIGNAL!', (610, 1010), pr(t, tc - 0.3, 0.35), size=48)
        credit(c, 'PHOTO: IVO KRUUSAMAGI . CC BY-SA 4.0')
        return
    title(c, 'ROUTE SHUT', 90, 520, 130, KINK if False else CRED, pr(t, tf - 0.4, 0.4))
    title(c, 'FOR A MONTH!', 90, 660, 130, CBLU, pr(t, tf - 0.2, 0.4))
    steps = ((tf - 0.2, 'APR 2024', 'TURNED BACK', CRED), (tr - 0.4, 'APR 29', 'ROUTE PAUSED', CYEL), (tr + 0.6, 'MAY 31', 'RESUMED', CCYN))
    for i, (t0, a, b, col) in enumerate(steps):
        def dr(cc, a=a, b=b, col=col):
            cc.drawRect(R.MakeWH(260, 300), paint(col))
            title(cc, a, 130, 120, 46, PAPER, 1.0, 'c', shadow=4)
            cc.drawString(b, 130 - width(b, 'SpecialElite.ttf', 26) / 2, 220, font('SpecialElite.ttf', 26), paint(KINK))
        panel(c, 90 + i * 300, 820, 260, 300, rot=(-2, 1, -1)[i], k=pr(t, t0, 0.4), draw=dr, border=7, shadow=10)
    if t > tr: caption(c, 'FINNAIR . HELSINKI TO TARTU', 220, 1240, pr(t, tr, 0.3), col=PAPER, size=28)


def sc_worse(c, t, S):
    tl = ph('pilots in lithuania'); tb = ph('bornholm'); tj = ph('one day in july'); tr = ph('blame russia')
    paper(c, t)
    caption(c, "AND IT'S GETTING WORSE...", LX, 318, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tb - 0.4:
        title(c, '~300 INCIDENTS!', 90, 520, 110, CRED, pr(t, tl - 0.3, 0.4))
        text(c, 'In just 2 months. Lithuania, 2026.', 92, 610, 'sb', 44, KINK)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 620), paint(PAPER))
            bars(cc, 120, 130, 660, 360, [('JAN', 169, '169', CRED), ('FEB', 118, '118', CYEL)], pr(t, tl, 1.2), 190)
        panel(c, 90, 720, 900, 620, rot=1.2, k=pr(t, tl - 0.2, 0.5), draw=dr)
        return
    if t < tj - 0.4:
        title(c, 'BORNHOLM:', 90, 520, 120, CBLU, pr(t, tb - 0.4, 0.4))
        title(c, 'A NEW RECORD!', 90, 650, 120, CRED, pr(t, tb - 0.2, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 620), paint(PAPER))
            bars(cc, 90, 130, 720, 360, [('2024', 11, '11', CCYN), ('2025', 16, '16', CYEL), ('2026*', 30, '30', CRED)], pr(t, tb, 1.4), 34)
            cc.drawString('*SO FAR', 40, 590, font('SpecialElite.ttf', 24), paint(KINK))
        panel(c, 90, 740, 900, 620, rot=-1.2, k=pr(t, tb - 0.2, 0.5), draw=dr)
        return
    title(c, 'JULY 29:', 90, 520, 130, CBLU, pr(t, tj - 0.4, 0.4))
    title(c, 'NO SIGNAL!', 90, 660, 130, CRED, pr(t, tj - 0.2, 0.4))
    def dr(cc):
        cover(cc, img('G7_bornholm_comic.png'), 0, 0, 900, 520, 1.1, 0.5, 0.5)
        for i, (x, lab) in enumerate(((150, 'GDANSK'), (750, 'GOTLAND'))):
            cc.drawCircle(x, 260, 20, paint(CYEL)); cc.drawCircle(x, 260, 20, stroke(KINK, 5))
            title(cc, lab, x, 320, 40, PAPER, 1.0, 'c', shadow=4)
        for j in range(12):
            x = 190 + j * 46
            cc.drawLine(x, 260, x + 26, 260, stroke(CRED, 9, 0.5 + 0.5 * (math.sin(t * 20 + j) > 0)))
    panel(c, 90, 760, 900, 520, rot=1.5, k=pr(t, tj - 0.2, 0.5), draw=dr)
    if t > tj + 0.6: burst(c, 820, 790, 110, 'ZZZT!', pr(t, tj + 0.6, 0.35), size=46, rot=10)
    if t > tr - 0.3: caption(c, 'EUROPEAN OFFICIALS BLAME RUSSIA', 160, 1340, pr(t, tr - 0.3, 0.3), col=PAPER, size=28)
    credit(c, 'PHOTO: SOCKET0 . CC0')


def sc_cost(c, t, S):
    t7 = ph('seven and a half billion'); td = ph('billion pounds a day'); te = ph('emergency services')
    paper(c, t)
    caption(c, 'UK GOVERNMENT STUDY', LX, 318, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < te - 0.6:
        text(c, 'One week without GPS:', 92, 500, 'blk', 72, KINK)
        burst(c, 540, 960, 330, '7.6 BILLION', pr(t, t7 - 0.2, 0.45), col=CYEL, txt=CRED, size=100, spikes=20, rot=-4)
        caption(c, 'POUNDS (£), GONE', 330, 1180, pr(t, t7 + 0.4, 0.3), col=PAPER, size=30)
        if t > td - 0.3: caption(c, 'OVER £1 BILLION A DAY!', 260, 1360, pr(t, td - 0.3, 0.3), col=PAPER, size=32)
        return
    title(c, 'BIGGEST HIT:', 90, 520, 110, KINK if False else CBLU, pr(t, te - 0.6, 0.4))
    title(c, 'EMERGENCY SERVICES', 90, 640, 84, CRED, pr(t, te - 0.4, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(900, 600), paint(PAPER))
        bars(cc, 70, 130, 760, 340, [('EMERGENCY', 3.5, '3.5BN', CRED), ('ROAD', 1.7, '1.7BN', CYEL), ('SHIPS', 1.5, '1.5BN', CBLU)], pr(t, te, 1.3), 3.9)
    panel(c, 90, 740, 900, 600, rot=1.2, k=pr(t, te - 0.3, 0.5), draw=dr)
    burst(c, 860, 760, 120, 'OUCH!', pr(t, te + 0.8, 0.35), size=52, rot=-10)


def sc_backup(c, t, S):
    tp = ph('planes have older'); ts = ph('ships have radar'); te = ph('eloran'); ty = ph('your phone your car')
    paper(c, t)
    caption(c, 'IS THERE A BACKUP?', LX, 318, pr(t, S['t0'], 0.3), size=30)
    title(c, 'KIND OF...', 90, 530, 160, CRED, pr(t, S['t0'] + 0.3, 0.4))
    rows = ((tp, 'PLANES', 'Old radio beacons', True), (ts, 'SHIPS', 'Radar & compasses', True), (ty, 'YOUR PHONE & CAR', 'Nothing else', False))
    for i, (t0, a, b, ok) in enumerate(rows):
        def dr(cc, a=a, b=b, ok=ok):
            cc.drawRect(R.MakeWH(820, 190), paint(PAPER if ok else (255, 225, 220)))
            cc.drawString(a, 30, 56, font('SpecialElite.ttf', 30), paint(KINK))
            title(cc, b.upper(), 30, 140, 58, KINK if ok else CRED, 1.0, shadow=4, outline=0.01)
            if ok: cc.drawPath(poly([(690, 95), (725, 135), (790, 55)], False), stroke((30, 170, 90), 16))
            else:
                cc.drawLine(700, 60, 780, 140, stroke(CRED, 16)); cc.drawLine(780, 60, 700, 140, stroke(CRED, 16))
        panel(c, 130, 640 + i * 230, 820, 190, rot=(-2, 1.5, -1)[i], k=pr(t, t0 - 0.2, 0.4), draw=dr, border=7, shadow=10)
    if te - 0.3 < t < ty - 0.2: caption(c, 'BACKUP IDEA: eLORAN (GROUND RADIO)', 150, 1380, pr(t, te - 0.3, 0.3), col=CCYN, size=26)


def sc_predict(c, t, S):
    tj = ph('jamming becomes normal'); tc = ph('more cancelled flights'); tn = ph('the next big business')
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 318, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tn - 0.4:
        title(c, "GPS DOESN'T", 90, 540, 130, PAPER, pr(t, S['t0'] + 0.2, 0.4))
        title(c, 'SWITCH OFF.', 90, 680, 130, CYEL, pr(t, S['t0'] + 0.4, 0.4))
        for i, (t0, s, col) in enumerate(((tj, 'JAMMING BECOMES NORMAL', CYEL), (tc, 'MORE CANCELLED FLIGHTS', PAPER), (ph('wrong place'), 'SHIPS IN THE WRONG PLACE', CCYN))):
            caption(c, s, 140 + (i % 2) * 60, 860 + i * 170, pr(t, t0 - 0.2, 0.3), col=col, size=36, rot=(-2, 1.5, -1)[i])
    else:
        title(c, 'NEXT BIG', 90, 540, 140, PAPER, pr(t, tn - 0.4, 0.4))
        title(c, 'BUSINESS:', 90, 690, 140, CYEL, pr(t, tn - 0.2, 0.4))
        burst(c, 540, 1100, 300, 'NAVIGATION', pr(t, ph('navigation that') - 0.2, 0.4), col=CYEL, txt=CBLU, size=88, spikes=20, rot=-3)
        caption(c, "THAT DOESN'T NEED SPACE", 270, 1360, pr(t, ph("doesn't need space") - 0.2, 0.3), col=PAPER, size=30)
    place(c, 'G1_sat_cut_comic.png', 850, 1500, 260, rot=12, a=0.0)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 318, pr(t, S['t0'], 0.3), size=30)
    title(c, 'COULD YOU GET', 90, 520, 100, KINK if False else CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'HOME WITHOUT GPS?', 90, 640, 86, CRED, pr(t, S['t0'] + 0.3, 0.4))
    c.drawCircle(552, 1072, 260, paint(KINK)); c.drawCircle(540, 1060, 260, paint(CYEL)); c.drawCircle(540, 1060, 260, stroke(KINK, 9))
    kk = pr(t, S['t0'] + 0.3, 0.6)
    place(c, 'G6_plane_cut_comic.png', 540 + 40 * math.sin(t), 1060, 640 * sticker_pop(kk), rot=-10, a=kk, shadow=False)
    burst(c, 300, 1400, 110, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=(80, 210, 120), txt=PAPER, size=60)
    burst(c, 780, 1400, 110, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=64)
    credit(c, 'PHOTO: MARCUSOBAL . CC BY-SA 3.0', a=kk)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(k2), paint(CRED))


FN = dict(hook=sc_hook, what=sc_what, tartu=sc_tartu, worse=sc_worse, cost=sc_cost, backup=sc_backup, predict=sc_predict, ask=sc_ask)
SCENES = []
for S in G.SCENES:
    d = dict(S); d['fn'] = FN[S['k']]
    if 'col' in d: d['col'] = CRED if S['k'] in ('predict',) else NEWS
    SCENES.append(d)
EP = Episode(G.D, SCENES, DURATION, END)
EP.shk(ph('jamming their gps'), 12, 0.35)
EP.shk(ph("simply couldn't come in"), 8, 0.3)
EP.shk(ph('seven and a half billion'), 10, 0.35)

if __name__ == '__main__':
    EP.main(sys.argv)
