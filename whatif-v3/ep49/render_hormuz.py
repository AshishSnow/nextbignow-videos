"""NextBigNow ep 49 (vintage comic + editorial, small creative subtitles): What happens when the world's oil highway closes?
Facts: EIA (Nov 2023) - Hormuz 21 mi wide at narrowest; ~21 mb/d in 2022 = ~21% of global petroleum liquids; ~82% to Asia.
Wikipedia '2026 Iran war fuel crisis' - closure began late Feb 2026; Brent peak ~$118 late March; QatarEnergy force majeure 3 Mar;
IEA 400m bbl collective release; Philippines national energy emergency 24 Mar + 4-day week for govt offices; Slovenia first EU country to
ration fuel (50 L/day private); CA gas > $6 in seven counties by 30 Mar; US SPR lowest since Nov 1982 (Sep 2026). OPB/NPR (2 May 2026) -
Spirit ceased operations, jet fuel spike from the Iran war a factor. Straits.live / IMF PortWatch - 3 transits on 8 Nov vs ~85/day baseline.
gCaptain (13 Nov 2026) - European diesel ~77% above pre-war; tanker attacks continue. 1973: OAPEC embargo, ~4x price, gas lines, odd-even
rationing in some states; SPR created 1975, CAFE fuel-economy rules 1975.
Photos (Wikimedia Commons): Hormuz MODIS - NASA GSFC PD; tanker - ITookSomePhotos CC BY-SA 4.0; SPR - energy.gov PD; 2026 gas sign - Rick Obst
CC BY 4.0; 1973 Portland 'Sorry no gasoline' + 'Closed due to gasoline shortage' - David Falconer / NARA PD."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('HZ_DIR', 'hormuz'))
PK.IMG = os.path.join(HERE, 'hormuz', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]
SUBS = sub_chunks(sub_tokens(os.path.join(D, 'script.txt'), WT))


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
SEPIA = (240, 222, 186)


def credit(c, s, a=1.0, col=(120, 100, 70), y=1360):
    c.save(); c.translate(76, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def k0(t, t0, d=0.4):
    """pop-in that is already complete on frame 0 (so the first frame works as the cover)."""
    return 1.0 if t0 <= 0.05 else pr(t, t0, d)


def strait_panel(c, t, x, y, w, h, rot, k, zoom=1.0, block=0.0, tankers=True, labels=None):
    def dr(cc):
        cover(cc, img('H1_strait_comic.png'), 0, 0, w, h, zoom, 0.62, 0.42)
        if block > 0:  # red barrier across the narrows
            bx, by = w * 0.66, h * 0.36
            cc.drawLine(bx - 120, by + 70, bx + 110, by - 80, stroke(CRED, 16 * eo(block)))
            for i in range(5):
                xx = bx - 120 + i * 57; yy = by + 70 - i * 37.5
                cc.drawCircle(xx, yy, 13 * eo(block), paint(CYEL)); cc.drawCircle(xx, yy, 13 * eo(block), stroke(KINK, 4))
        if labels:
            for (fx, fy, s, kk) in labels:
                if kk > 0:
                    caption(cc, s, fx * w, fy * h, kk, col=PAPER, size=22, rot=0)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)
    if tankers:
        for i in range(3):
            stop = block > 0.5
            dx = (0 if stop else (t * 40 + i * 120) % 360)
            place(c, 'H2_tanker_comic.png', x + 150 + i * 120 + dx * 0.25, y + h * 0.47 + i * 34, 230, rot=-4, shadow=False)


# ================================================================== scenes
def sc_hook(c, t, S):
    ts = ph('almost shut'); tq = ph('so what happens')
    if t < tq - 0.15:
        paper(c, t)
        caption(c, "THE WORLD'S OIL HIGHWAY", LX, 340, k0(t, 0), size=30)
        title(c, '21 MILES.', 90, 560, 170, CRED, k0(t, 0), rot=-2)
        text(c, '1 in 5 barrels of oil on Earth', 92, 650, 'blk', 50, KINK)
        text(c, 'went through this gap.', 92, 712, 'blk', 50, KINK)
        strait_panel(c, t, 90, 790, 900, 560, 1.2, 1.0, zoom=1.15 + 0.01 * t, block=pr(t, ts - 0.2, 0.5))
        if t > ts - 0.2: burst(c, 830, 820, 120, 'SHUT!', pr(t, ts - 0.2, 0.35), size=56, rot=8)
        credit(c, 'NASA MODIS (PD) . TANKER: ITOOKSOMEPHOTOS CC BY-SA 4.0')
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'THE REAL QUESTION...', LX, 340, pr(t, tq - 0.1, 0.3), col=PAPER, size=30)
    title(c, 'WHAT IF THE', 90, 540, 128, PAPER, pr(t, tq - 0.05, 0.4))
    title(c, "WORLD'S OIL", 90, 680, 128, CYEL, pr(t, tq + 0.2, 0.4))
    title(c, 'HIGHWAY CLOSES?', 90, 820, 112, PAPER, pr(t, tq + 0.45, 0.4))
    kk = pr(t, tq + 0.4, 0.5)
    place(c, 'H2_tanker_comic.png', 540 + 30 * math.sin(t), 1120 + 8 * math.sin(t * 2), 920 * eback(cl(kk), 1.5), rot=-4, a=kk, shadow=False)
    burst(c, 820, 1250, 100, '?!', pr(t, tq + 0.9, 0.3), size=70, rot=10)


def sc_what(c, t, S):
    t20 = ph('twenty million'); ta = ph('headed to asia')
    paper(c, t)
    caption(c, "IT'S CALLED...", LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    title(c, 'THE STRAIT', 90, 520, 130, CBLU, pr(t, S['t0'] + 0.2, 0.4))
    title(c, 'OF HORMUZ', 90, 655, 130, CRED, pr(t, S['t0'] + 0.4, 0.4))
    names = (('saudi arabia', 0.03, 0.05, 'SAUDI ARABIA'), ('iraq', 0.03, 0.15, 'IRAQ'), ('kuwait', 0.03, 0.25, 'KUWAIT'), ('qatar', 0.03, 0.35, 'QATAR'), ('uae', 0.03, 0.45, 'UAE'))
    labels = [(fx, fy, s, pr(t, ph(p_) - 0.1, 0.3)) for p_, fx, fy, s in names] + [(0.62, 0.08, 'IRAN', pr(t, S['t0'] + 0.6, 0.3))]
    strait_panel(c, t, 90, 740, 900, 560, -1.2, pr(t, S['t0'] + 0.3, 0.5), zoom=1.0, labels=labels, tankers=t < t20 - 0.3)
    if t > t20 - 0.3:
        burst(c, 540, 1040, 250, '20M BARRELS', pr(t, t20 - 0.3, 0.4), col=CYEL, txt=CRED, size=70, spikes=18, rot=-3)
        caption(c, 'EVERY SINGLE DAY', 330, 1180, pr(t, t20 + 0.5, 0.3), col=PAPER, size=30)
    if t > ta - 0.3: caption(c, 'MOST OF IT -> ASIA', 560, 1290, pr(t, ta - 0.3, 0.3), col=CCYN, size=30, rot=3)
    credit(c, 'NASA MODIS . PUBLIC DOMAIN')


def price_chart(cc, w, h, k, t):
    pts = [(0, 72), (0.12, 74), (0.22, 82), (0.4, 118), (0.6, 96), (0.75, 108), (1.0, 100)]
    x0, y0, cw, ch = 70, 60, w - 120, h - 150
    yv = lambda v: y0 + ch - (v - 60) / 70 * ch
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    p = skia.Path(); n = 0
    for i, (fx, v) in enumerate(pts):
        if fx > k: break
        X, Y = x0 + fx * cw, yv(v)
        (p.moveTo if i == 0 else p.lineTo)(X, Y); n += 1
    cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(CRED, 9))
    if k > 0.4:
        X, Y = x0 + 0.4 * cw, yv(118)
        cc.drawCircle(X, Y, 16, paint(CYEL)); cc.drawCircle(X, Y, 16, stroke(KINK, 5))
    for fx, s in ((0.0, 'FEB'), (0.4, 'MAR'), (1.0, 'NOW')):
        cc.drawString(s, x0 + fx * cw - 20, y0 + ch + 44, font('SpecialElite.ttf', 26), paint(KINK))


def sc_war(c, t, S):
    tw = ph('within weeks'); tq = ph('qatar one'); t4 = ph('four hundred million'); te = ph('it still wasn', ) if False else ph('still wasn') if False else None
    bg_flat(c, (250, 236, 200), (236, 214, 160))
    caption(c, 'LATE FEBRUARY 2026', LX, 340, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tq - 0.3:
        title(c, 'SHIPS GET HIT.', 90, 520, 116, KINK if False else CBLU, pr(t, ph('started getting hit') - 0.3, 0.4))
        title(c, 'OIL: $118!', 90, 660, 150, CRED, pr(t, tw - 0.1, 0.4), rot=-2)
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 520), paint(PAPER))
            price_chart(cc, 900, 520, pr(t, tw, 1.8), t)
            cc.drawString('BRENT CRUDE, $ PER BARREL', 70, 40, font('SpecialElite.ttf', 24), paint(KINK))
        panel(c, 90, 770, 900, 520, rot=1.0, k=pr(t, tw - 0.3, 0.5), draw=dr)
        return
    if t < t4 - 0.3:
        title(c, 'QATAR', 90, 540, 150, CBLU, pr(t, tq - 0.3, 0.4))
        title(c, 'STOPS SHIPPING', 90, 680, 110, CRED, pr(t, tq + 0.2, 0.4))
        burst(c, 540, 1050, 260, 'GAS: PAUSED', pr(t, ph('stopped shipping') - 0.2, 0.4), col=CYEL, txt=CBLU, size=72, spikes=18, rot=3)
        caption(c, 'ONE OF THE BIGGEST GAS EXPORTERS', 180, 1300, pr(t, tq + 0.4, 0.3), col=PAPER, size=26)
        return
    title(c, '400 MILLION', 90, 540, 140, CRED, pr(t, t4 - 0.3, 0.4))
    title(c, 'BARRELS RELEASED', 90, 670, 100, CBLU, pr(t, t4, 0.4))
    for i in range(10):
        kk = pr(t, t4 + 0.3 + i * 0.08, 0.3)
        if kk <= 0: continue
        x = 140 + (i % 5) * 170; y = 820 + (i // 5) * 220
        c.save(); c.translate(x, y); s_ = eback(cl(kk), 2); c.scale(s_, s_)
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(6, 6, 110, 160), 14, 14), paint(KINK))
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(0, 0, 110, 160), 14, 14), paint(CBLU))
        for j in (40, 120): c.drawLine(0, j, 110, j, stroke(KINK, 5))
        c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(0, 0, 110, 160), 14, 14), stroke(KINK, 5))
        c.restore()
    if t > ph('still wasn') - 0.2 if False else t > ph('enough') - 0.4:
        burst(c, 540, 1300, 150, 'NOT ENOUGH!', pr(t, ph('enough') - 0.4, 0.35), size=48, rot=-6)


def mini(c, x, y, w, h, rot, k, head, big, col, photo=None, txtc=PAPER):
    def dr(cc):
        if photo:
            cover(cc, img(photo), 0, 0, w, h, 1.05, 0.5, 0.5)
            cc.drawRect(R.MakeXYWH(0, h - 120, w, 120), paint(KINK, 0.55))
        else:
            cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.25)
        cc.drawString(head, 22, 44, font('SpecialElite.ttf', 26), paint(PAPER if photo or col in (CRED, CBLU) else KINK))
        title(cc, big, 22, h - 36, 54, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def sc_people(c, t, S):
    tp = ph('the philippines'); tsl = ph('slovenia became'); tc = ph('in parts of california'); tsp = ph('and spirit airlines')
    paper(c, t)
    caption(c, 'MEANWHILE, FOR REGULAR PEOPLE...', LX, 340, pr(t, S['t0'], 0.3), size=28)
    title(c, 'REAL LIFE HITS.', 90, 500, 104, CRED, pr(t, S['t0'] + 0.2, 0.4))
    mini(c, 90, 580, 430, 360, -2, pr(t, tp - 0.2, 0.4), 'PHILIPPINES', '4-DAY WEEK', CBLU)
    mini(c, 560, 600, 430, 360, 1.5, pr(t, tsl - 0.2, 0.4), 'SLOVENIA', '50 L / DAY', CYEL, txtc=CRED)
    mini(c, 90, 990, 430, 360, 1.2, pr(t, tc - 0.2, 0.4), 'GAS PRICES, 2026', '$6+ IN CA', None, photo='H4_gas2026_comic.png', txtc=CYEL)
    mini(c, 560, 1000, 430, 360, -1.5, pr(t, tsp - 0.2, 0.4), 'SPIRIT AIRLINES', 'SHUT DOWN', CRED)
    if t > ph('fuel rationing') if False else t > ph('ration fuel') - 0.1:
        burst(c, 900, 600, 80, 'RATIONED!', pr(t, ph('ration fuel'), 0.3), size=30, rot=12)
    credit(c, 'PHOTO: RICK OBST . CC BY 4.0')


def sc_now(c, t, S):
    th = ph('only a handful'); te = ph('about eighty five'); ta = ph('tankers are still'); td = ph('and diesel in europe')
    paper(c, t)
    caption(c, 'SO WHERE ARE WE NOW?', LX, 340, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < td - 0.3:
        title(c, 'SHIPS PER DAY', 90, 520, 120, CBLU, pr(t, th - 0.4, 0.4))
        def dr(cc):
            cc.drawRect(R.MakeWH(900, 600), paint(PAPER))
            k = pr(t, th, 0.8) if t < te else 1.0
            bars(cc, 120, 120, 660, 340, [('BEFORE', 85, '85', CCYN), ('NOV 8', 3, '3', CRED)], pr(t, te - 0.3, 1.0) if t > te - 0.3 else 0.5 * k, 95)
            cc.drawString('IMF PORTWATCH', 40, 580, font('SpecialElite.ttf', 22), paint(KINK))
        panel(c, 90, 620, 900, 600, rot=1.0, k=pr(t, th - 0.3, 0.5), draw=dr)
        if t > ta - 0.2: burst(c, 840, 640, 110, 'BOOM!', pr(t, ta - 0.2, 0.3), size=46, rot=-8)
        if t > ta: caption(c, 'TANKERS STILL BEING ATTACKED', 180, 1290, pr(t, ta, 0.3), col=PAPER, size=28)
        return
    title(c, 'EUROPE DIESEL', 90, 520, 116, CBLU, pr(t, td - 0.3, 0.4))
    burst(c, 540, 960, 300, '+77%', pr(t, ph('seventy seven') - 0.2, 0.4), col=CYEL, txt=CRED, size=170, spikes=20, rot=-4)
    caption(c, 'VS. BEFORE THE WAR', 340, 1240, pr(t, ph('before the war', after=td) - 0.1, 0.3), col=PAPER, size=30)


def plate(c, x, y, s, k, lab, num, col):
    if k <= 0: return
    c.save(); c.translate(x, y); sc = eback(cl(k), 2); c.scale(sc, sc)
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-190 + 8, -80 + 8, 380, 160), 18, 18), paint(KINK))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-190, -80, 380, 160), 18, 18), paint(PAPER))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-190, -80, 380, 160), 18, 18), stroke(KINK, 6))
    title(c, num, 0, 40, 82, col, 1.0, 'c', shadow=4)
    c.drawString(lab, -width(lab, 'SpecialElite.ttf', 26) / 2, -46, font('SpecialElite.ttf', 26), paint(KINK))
    c.restore()


def sc_1973(c, t, S):
    tq = ph('prices quadrupled'); to = ph('odd or even'); tc = ph('that shock changed'); tr = ph('emergency oil reserve'); tf = ph('more fuel efficient')
    paper(c, t, tint=SEPIA)
    caption(c, "WE'VE SEEN THIS BEFORE...", LX, 340, pr(t, S['t0'], 0.3), size=30)
    if t < to - 0.4:
        title(c, '1973', 90, 560, 200, CRED, pr(t, S['t0'] + 0.3, 0.4), rot=-3)
        def dr(cc):
            cover(cc, img('H5_outofgas_crop_comic.png'), 0, 0, 640, 560, 1.0, 0.5, 0.45)
        panel(c, 320, 660, 640, 560, rot=2, k=pr(t, S['t0'] + 0.5, 0.5), draw=dr)
        if t > tq - 0.2: burst(c, 220, 820, 140, 'PRICES x4', pr(t, tq - 0.2, 0.35), size=40, rot=-8)
        credit(c, 'PHOTO: DAVID FALCONER / NARA . PUBLIC DOMAIN')
        return
    if t < tc - 0.3:
        title(c, 'GAS ON ODD', 90, 520, 116, CBLU, pr(t, to - 0.4, 0.4))
        title(c, 'OR EVEN DAYS', 90, 650, 116, CRED, pr(t, to - 0.1, 0.4))
        plate(c, 300, 870, 1, pr(t, to + 0.2, 0.35), 'PLATE ENDS IN 3', 'ODD', CRED)
        plate(c, 780, 1060, 1, pr(t, to + 0.6, 0.35), 'PLATE ENDS IN 8', 'EVEN', CBLU)
        def dr(cc):
            cover(cc, img('H6_shortage_comic.png'), 0, 0, 420, 300, 1.2, 0.45, 0.6)
        panel(c, 120, 1020, 420, 300, rot=-2, k=pr(t, to + 1.0, 0.4), draw=dr, border=7, shadow=10)
        credit(c, 'PHOTO: DAVID FALCONER / NARA . PUBLIC DOMAIN')
        return
    title(c, 'IT CHANGED', 90, 520, 130, CBLU, pr(t, tc - 0.3, 0.4))
    title(c, 'EVERYTHING.', 90, 660, 130, CRED, pr(t, tc, 0.4))
    def dr(cc):
        cover(cc, img('H3_spr_comic.png'), 0, 0, 900, 440, 1.1, 0.5, 0.5)
    panel(c, 90, 760, 900, 440, rot=-1, k=pr(t, tr - 0.4, 0.5), draw=dr)
    if t > tr: caption(c, "AMERICA'S EMERGENCY OIL RESERVE", 130, 800, pr(t, tr, 0.3), size=26)
    if t > tf - 0.3: caption(c, 'CARS GOT WAY MORE EFFICIENT', 230, 1260, pr(t, tf - 0.3, 0.3), col=CCYN, size=28, rot=2)
    credit(c, 'PHOTO: ENERGY.GOV . PUBLIC DOMAIN')


def sc_predict(c, t, S):
    ti = ph('tanker insurance'); tl = ph('lowest level since'); tb = ph('but the bigger change'); tp = ph('build pipelines'); ts = ph('store more oil'); te = ph('electric cars'); to = ph("won't stay the only")
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NEXTBIGNOW PREDICTION', LX, 340, pr(t, S['t0'], 0.3), col=PAPER, size=30)
    if t < tb - 0.3:
        title(c, "PRICES WON'T", 90, 540, 130, PAPER, pr(t, S['t0'] + 0.3, 0.4))
        title(c, 'SNAP BACK.', 90, 680, 130, CYEL, pr(t, S['t0'] + 0.6, 0.4))
        caption(c, 'TANKER INSURANCE STAYS EXPENSIVE', 120, 860, pr(t, ti - 0.2, 0.3), col=PAPER, size=30, rot=-2)
        caption(c, 'US RESERVE: LOWEST SINCE 1982', 150, 1010, pr(t, tl - 0.4, 0.3), col=CYEL, size=30, rot=1.5)
        if t > tl + 1.2: burst(c, 540, 1250, 150, 'REFILL!', pr(t, tl + 1.2, 0.35), col=PAPER, txt=CRED, size=56, rot=-6)
        return
    title(c, 'THE BIG', 90, 540, 140, PAPER, pr(t, tb - 0.3, 0.4))
    title(c, 'CHANGE:', 90, 690, 140, CYEL, pr(t, tb, 0.4))
    for i, (t0, s, col) in enumerate(((tp, 'PIPELINES AROUND HORMUZ', CYEL), (ts, 'MORE OIL STORED AT HOME', PAPER), (te, 'ELECTRIC CARS + SOLAR', CCYN))):
        caption(c, s, 130 + (i % 2) * 50, 840 + i * 140, pr(t, t0 - 0.2, 0.3), col=col, size=34, rot=(-2, 1.5, -1)[i])
    if t > to - 0.2: burst(c, 820, 1300, 120, 'NEW ROADS', pr(t, to - 0.2, 0.35), size=36, rot=8)


def sc_ask(c, t, S):
    paper(c, t)
    caption(c, 'YOUR TURN!', LX, 340, pr(t, S['t0'], 0.3), size=30)
    title(c, 'HAVE FUEL PRICES', 90, 520, 96, CBLU, pr(t, S['t0'] + 0.1, 0.4))
    title(c, 'HIT YOU?', 90, 640, 130, CRED, pr(t, S['t0'] + 0.3, 0.4))
    def dr(cc):
        cover(cc, img('H4_gas2026_comic.png'), 0, 0, 840, 330, 1.0, 0.5, 0.5)
    panel(c, 120, 740, 840, 330, rot=-1.5, k=pr(t, S['t0'] + 0.3, 0.5), draw=dr)
    burst(c, 300, 1220, 110, 'YES', pr(t, ph('yes or no') - 0.1, 0.35), col=(80, 210, 120), txt=PAPER, size=60)
    burst(c, 780, 1220, 110, 'NO', pr(t, ph('yes or no') + 0.2, 0.35), col=CRED, txt=CYEL, size=64)
    credit(c, 'PHOTO: RICK OBST . CC BY 4.0')
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
    dict(k='what', t0=ph("it's called the") - 0.2, fn=with_subs(sc_what), tin='whip'),
    dict(k='war', t0=ph('then in late') - 0.2, fn=with_subs(sc_war), tin='flash'),
    dict(k='people', t0=ph("here's what that") - 0.2, fn=with_subs(sc_people), tin='whip'),
    dict(k='now', t0=ph('so where are we') - 0.2, fn=with_subs(sc_now), tin='zoom'),
    dict(k='y1973', t0=ph("and we've actually") - 0.2, fn=with_subs(sc_1973), tin='wipe', col=SEPIA),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=with_subs(sc_predict), tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=with_subs(sc_ask), tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('almost shut'), 10, 0.3)
EP.shk(ph('started getting hit'), 12, 0.35)
EP.shk(ph('seventy seven'), 8, 0.3)
EP.shk(ph('prices quadrupled'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
