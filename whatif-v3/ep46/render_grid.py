"""NextBigNow (editorial look, real photos) ep 46: AI is eating the power grid. What happens next?
Facts: DCD (NERC report) - 10 Jul 2024 ~7pm, Fairfax County VA, 60 data centers / 1,500 MW dropped to backup after a lightning-arrester
failure on a 230 kV line; PJM + Dominion cut generation output to control voltage. BloombergNEF via Bloomberg Law 21 Jul 2026: data
centers 5.9% of US power now, ~20% by 2035. Shipley Energy/WFTV 9 Nov 2026: PJM capacity price $28.92 -> $269.92/MW-day (2024/25 ->
2025/26); market monitor ~46% of capacity costs over last four auctions attributed to data centers; ERCOT >474 GW of requests, >5x
record peak, ~90% data centers. Microsoft-Constellation 20-yr deal (Sep 2024) to restart TMI Unit 1 (Crane Clean Energy Center).
Photos (Wikimedia Commons): Ashburn aerial - Theodore Christopher CC0; pylon - Mozzihh CC BY-SA 4.0; servers - BalticServers.com
CC BY-SA 3.0; meter - RobbieIanMorrison CC BY 4.0; TMI - US DOE public domain; map - DOE/NREL public domain; Lower Manhattan
night - VynedJ CC BY 4.0."""
import sys, os, math, re
import numpy as np
import skia
from PIL import Image
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from edkit import _grain
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('GR_DIR', 'grid'))
IMG = os.path.join(HERE, 'grid', 'img')
WT = load_words(D)
TOK = [(w.lower().strip("'"), a, b) for w, a, b in WT]


def ph(text_, after=0.0, end=False):
    q = [x.strip("'") for x in re.findall(r"[a-zA-Z']+", text_.lower())]
    for i in range(len(TOK) - len(q) + 1):
        if TOK[i][1] + 1e-6 < after: continue
        if all(TOK[i + j][0] == q[j].strip("'") or TOK[i + j][0] == q[j] for j in range(len(q))):
            return TOK[i + len(q) - 1][2] if end else TOK[i][1]
    raise KeyError(text_)


END = WT[-1][2] + 0.45
DURATION = END + 2.3
LX = 90
HY = 540

# ------------------------------------------------------------------ photos
_IM = {}
def img(name, maxw=2000):
    if name not in _IM:
        im = Image.open(os.path.join(IMG, name)).convert('RGBA')
        im.thumbnail((maxw, maxw * 2))
        _IM[name] = skia.Image.fromarray(np.ascontiguousarray(np.array(im)), colorType=skia.kRGBA_8888_ColorType)
    return _IM[name]


SAMP = skia.SamplingOptions(skia.FilterMode.kLinear)


def cover(c, im, x, y, w, h, zoom=1.0, fx=0.5, fy=0.5, a=1.0):
    """draw image to fill rect (x,y,w,h), cropped; zoom>1 pushes in around focus (fx,fy)."""
    iw, ih = im.width(), im.height()
    s = max(w / iw, h / ih) * zoom
    sw, sh = w / s, h / s
    sx = cl(fx * iw - sw / 2, 0, iw - sw) if iw > sw else 0
    sy = cl(fy * ih - sh / 2, 0, ih - sh) if ih > sh else 0
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, R.MakeXYWH(sx, sy, sw, sh), R.MakeXYWH(x, y, w, h), SAMP, p)


def cutout(c, name, cx, by, h, k=1.0, shadow=True, bw=False, a=1.0):
    """cut-out PNG standing with its bottom at by, height h, centred on cx; rises in with k."""
    if k <= 0: return
    im = img(name, 1600)
    w = h * im.width() / im.height()
    yy = by - h + 80 * (1 - eo(cl(k)))
    p = skia.Paint(); p.setAlphaf(cl(k * 1.5) * a)
    if bw: p.setColorFilter(skia.ColorFilters.Matrix([0.3, 0.59, 0.11, 0, 0, 0.3, 0.59, 0.11, 0, 0, 0.3, 0.59, 0.11, 0, 0, 0, 0, 0, 1, 0]))
    if shadow:
        sp = skia.Paint(); sp.setImageFilter(skia.ImageFilters.DropShadowOnly(0, 24, 26, 26, skia.ColorSetARGB(int(255 * 0.35 * cl(k)), 0, 0, 0)))
        c.saveLayer(None, sp); c.drawImageRect(im, R.MakeXYWH(cx - w / 2, yy, w, h), SAMP); c.restore()
    c.drawImageRect(im, R.MakeXYWH(cx - w / 2, yy, w, h), SAMP, p)
    return (cx - w / 2, yy, w, h)


def photo_card(c, name, cx, cy, w, h, rot, k, zoom=1.0, fx=0.5, fy=0.5, pad=18, after=None):
    def dr(cc):
        cover(cc, img(name), pad, pad, w - 2 * pad, h - 2 * pad, zoom, fx, fy)
        if after: after(cc)
    card(c, cx, cy, w, h, rot, k, dr, rad=10)


def credit(c, s, a=1.0, col=GREY, y=1480):
    c.save(); c.translate(80, y); c.rotate(-90)
    mono(c, s, 0, 0, 17, col, a=a * 0.9)
    c.restore()


def shade(c, a, col=(0, 0, 0)):
    c.drawRect(R.MakeWH(W, H), paint(col, a))


def kicker(c, s, t, t0, y=400, col=GREY):
    k = pr(t, t0, 0.3)
    if k > 0:
        c.drawRect(R.MakeXYWH(LX, y - 22, 14, 14), paint(RED, k))
        mono(c, s, LX + 30, y - 8, 26, col, a=k)


def bolt(c, x, y, s, k):
    if k <= 0 or k >= 1: return
    a = 1 - k
    c.drawPath(poly([(x, y), (x - 60 * s, y + 220 * s), (x + 10 * s, y + 220 * s), (x - 50 * s, y + 470 * s), (x + 110 * s, y + 160 * s), (x + 30 * s, y + 160 * s), (x + 90 * s, y)], True), paint(YEL, a))
    c.drawCircle(x, y + 230 * s, 300 * s, paint((255, 255, 200), 0.35 * a, blur=40))


DOTS = [(0.18 + 0.66 * hsh(i, 41), 0.30 + 0.22 * hsh(i, 42)) for i in range(60)]


# ================================================================== hook
def sc_hook(c, t, S):
    tv = ph('vanished'); tq = ph('so what happens')
    if t < tq - 0.15:
        z = 1.0 + 0.05 * t
        cover(c, img('R1_ashburn.jpg'), 0, 0, W, H, z, 0.52, 0.55)
        shade(c, 0.42 + 0.2 * pr(t, tv, 0.8), (6, 10, 30))
        c.drawRect(R.MakeWH(W, 700), paint(shader=lin(0, 0, 0, 700, [argb((6, 10, 30), 0.85), argb((6, 10, 30), 0.0)])))
        ko = pr(t, tv - 0.05, 1.2)
        for i, (fx, fy) in enumerate(DOTS):
            on = cl(pr(t, 0.3 + i * 0.02, 0.2)) * (1 - cl(ko * 60 - i))
            if on <= 0: continue
            x = 80 + fx * 920; y = 820 + fy * 1000
            fl = 0.8 + 0.2 * math.sin(t * 7 + i)
            c.drawCircle(x, y, 26, paint(CYAN_G, 0.35 * on * fl, blur=10)); c.drawCircle(x, y, 8, paint((230, 255, 255), on))
        kicker(c, 'JULY 10, 2024 · 7 PM · VIRGINIA', t, 0.15, col=(200, 215, 255))
        n = int(60 * eo(pr(t, 0.3, 1.2)))
        headline(c, ['%d data centers.' % max(n, 1)], LX, HY + 20, 118, t, 0.2, col=PAPER)
        if t > tv - 0.2:
            headline(c, ['Gone.'], LX, HY + 190, 190, t, tv - 0.2, col=PAPER, hl=(0, ('', 'Gone.')), hl_col=RED)
        credit(c, 'PHOTO: THEODORE CHRISTOPHER · CC0 · WIKIMEDIA', col=(200, 210, 230))
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What happens when', 'AI eats the', 'power grid?'], LX, HY, 118, t, tq - 0.05, col=PAPER, hl=(2, ('', 'power grid?')), hl_col=INK)
    k = pr(t, tq + 0.2, 0.7)
    cutout(c, 'R5_tower_cut.png', 540, 1490, 660, k)
    credit(c, 'PHOTO: MOZZIHH · CC BY-SA 4.0', col=(255, 210, 210), a=k)


CYAN_G = (90, 220, 255)


def sc_alley(c, t, S):
    bg_cream(c, t)
    kicker(c, 'ASHBURN, VIRGINIA', t, S['t0'] + 0.1)
    headline(c, ['Data Center', 'Alley.'], LX, HY, 150, t, ph('people call it') - 0.2, hl=(1, ('', 'Alley.')), hl_col=YEL)
    k = pr(t, S['t0'] + 0.2, 0.5)
    def after(cc):
        for i in range(9):
            kk = pr(t, ph('biggest clusters') - 0.3 + i * 0.12, 0.3)
            if kk <= 0: continue
            x = 120 + 640 * hsh(i, 51); y = 200 + 260 * hsh(i, 52)
            cc.drawCircle(x, y, 22 * eback(kk, 2), paint(RED)); cc.drawCircle(x, y, 9 * eback(kk, 2), paint(PAPER))
    photo_card(c, 'R1_ashburn.jpg', 540, 1120, 900, 640, -1.5, k, zoom=1.15 + 0.03 * (t - S['t0']), fx=0.55, fy=0.55, after=after)
    if t > ph('internet you use') - 0.3:
        pill(c, 540, 1470, 'RUNS A HUGE CHUNK OF THE INTERNET', pr(t, ph('internet you use') - 0.3, 0.3), col=INK, size=34)
    credit(c, 'PHOTO: THEODORE CHRISTOPHER · CC0', a=k)


def sc_night(c, t, S):
    tf = ph('one small part failed'); tfl = ph('flickered'); tb = ph('backup power'); tm = ph('fifteen hundred megawatts'); th = ph('hundreds of thousands')
    bg_ink(c, t)
    kicker(c, 'THAT NIGHT', t, S['t0'] + 0.1, col=(170, 170, 176))
    if t < tm - 0.3:
        headline(c, ['One part failed.'], LX, HY, 120, t, tf - 0.1, col=PAPER, hl=(0, ('One part ', 'failed.')), hl_col=RED)
        if t > tb - 0.4:
            headline(c, ['60 switched to', 'backup power.'], LX, HY + 150, 92, t, tb - 0.4, col=(200, 200, 206))
        flick = 1.0
        if tfl - 0.1 < t < tfl + 0.5: flick = 0.35 + 0.65 * (math.sin(t * 60) > 0)
        cutout(c, 'R5_tower_cut.png', 540, 1490, 680, pr(t, S['t0'] + 0.1, 0.6), a=flick)
        bolt(c, 640, 760, 1.1, pr(t, tf + 0.4, 0.45))
        credit(c, 'PHOTO: MOZZIHH · CC BY-SA 4.0', col=(150, 150, 160))
        return
    k = pr(t, tm - 0.3, 0.5)
    n = int(1500 * eo(pr(t, tm - 0.3, 1.0)))
    text(c, '{:,}'.format(n), 540, 1000, 'blk', 290, RED, 'c', track=-0.05, a=eo(k))
    cutout(c, 'R5_tower_cut.png', 540, 1490, 540, 1.0, bw=True)
    headline(c, ['Megawatts.', 'Gone.'], LX, HY, 140, t, tm - 0.2, col=PAPER, hl=(1, ('', 'Gone.')), hl_col=RED)
    if t > th - 0.3:
        pill(c, 540, 1440, 'ENOUGH FOR HUNDREDS OF THOUSANDS OF HOMES', pr(t, th - 0.3, 0.3), col=PAPER, txt=INK, size=30)
    credit(c, 'PHOTO: MOZZIHH · CC BY-SA 4.0', col=(150, 150, 160))


def sc_scramble(c, t, S):
    tn = ph('no blackout')
    bg_cream(c, t)
    kicker(c, 'THE GRID PANICS', t, S['t0'] + 0.1)
    headline(c, ['Too much power.', 'Nowhere to go.'], LX, HY, 118, t, S['t0'] + 0.2, hl=(1, ('Nowhere ', 'to go.')), hl_col=RED_L)
    def dr(cc):
        mono(cc, 'POWER ON THE GRID vs. DEMAND (ILLUSTRATIVE)', 50, 66, 20)
        line_chart(cc, 50, 110, 760, 330, [(0, 50), (0.3, 50), (0.36, 92), (0.5, 80), (0.7, 62), (1.0, 52)],
                   pr(t, S['t0'] + 0.5, 3.0), col=RED, ymax=100, labels=[(0.05, '7:00 PM'), (0.36, 'DATA CENTERS DROP'), (0.95, 'FIXED')], fill=True)
    card(c, 540, 1060, 860, 500, 1.5, pr(t, S['t0'] + 0.3, 0.5), dr)
    if t > tn - 0.3:
        def d2(cc):
            mono(cc, 'RESULT', 44, 64, 22, RED)
            text(cc, 'No blackout.', 44, 150, 'blk', 70, INK)
            text(cc, 'But it was close.', 44, 220, 'sb', 46, GREY)
        card(c, 540, 1420, 760, 250, -2, pr(t, tn - 0.3, 0.45), d2, rad=22)


def sc_share(c, t, S):
    t6 = ph('six percent'); t20 = ph('twenty percent'); t5 = ph('one in every five')
    z = 1.05 + 0.02 * (t - S['t0'])
    cover(c, img('R6_servers.jpg'), 0, 0, W, H, z, 0.5, 0.5)
    shade(c, 0.62, (4, 8, 30))
    kicker(c, 'HOW MUCH POWER AI EATS', t, S['t0'] + 0.1, col=(190, 210, 255))
    headline(c, ['6% of US power', 'today.'], LX, HY, 120, t, t6 - 0.4, col=PAPER, hl=(0, ('', '6%')), hl_col=BLUE)
    def dr(cc):
        mono(cc, 'DATA CENTERS · SHARE OF US ELECTRICITY (BNEF)', 50, 66, 20)
        bars(cc, 60, 120, 740, 400, [('NOW', 5.9, '6%', INK), ('2030', 12, '12%', BLUE), ('2035', 20, '20%', RED)],
             pr(t, t6, max(1.2, t20 - t6 + 0.6)), ymax=22)
    card(c, 540, 1180, 860, 620, -1.5, pr(t, t6 - 0.2, 0.5), dr)
    if t > t5 - 0.3:
        pill(c, 540, 1440, '1 IN EVERY 5 UNITS OF POWER', pr(t, t5 - 0.3, 0.3), col=YEL, txt=INK, size=38)
    credit(c, 'PHOTO: BALTICSERVERS.COM · CC BY-SA 3.0', col=(170, 180, 210))


def sc_map(c, t, S):
    td = ph('every yellow dot'); tp = ph('same power lines')
    bg_cream(c, t)
    kicker(c, 'US GOVERNMENT MAP · DOE / NREL', t, S['t0'] + 0.1)
    headline(c, ['Every yellow dot', 'is a data center.'], LX, HY, 112, t, td - 0.3, hl=(0, ('Every ', 'yellow dot')), hl_col=YEL)
    zk = eio(pr(t, tp - 0.6, 1.6))
    photo_card(c, 'R13_dcmap.jpg', 540, 1110, 920, 620, 1.2, pr(t, S['t0'] + 0.2, 0.5), zoom=1.05 + 1.3 * zk, fx=0.45 + 0.33 * zk, fy=0.48 - 0.08 * zk, pad=14)
    if t > tp - 0.2:
        pill(c, 540, 1470, 'SAME POWER LINES AS YOUR HOUSE', pr(t, tp - 0.2, 0.3), col=RED, size=34)
    credit(c, 'MAP: DOE / NREL · PUBLIC DOMAIN')


def sc_bills(c, t, S):
    t29 = ph('twenty nine dollars'); t270 = ph('two hundred seventy'); th = ph('close to half'); tr = ph("regular people's")
    bg_cream(c, t)
    kicker(c, 'WHO PAYS?', t, S['t0'] + 0.1)
    if t < th - 0.3:
        headline(c, ['Somebody has', 'to pay.'], LX, HY, 130, t, S['t0'] + 0.2, hl=(1, ('to ', 'pay.')), hl_col=RED_L)
        big = '$29' if t < t270 - 0.1 else '$270'
        k = pr(t, t29 - 0.2, 0.4)
        text(c, big, LX - 10, 1130, 'blk', 300 if big == '$29' else 225, RED if big == '$270' else INK, 'l', track=-0.05, a=eo(k))
        box = cutout(c, 'R7_meter_cut.png', 790, 1470, 540, pr(t, S['t0'] + 0.3, 0.6))
        if box:
            x, y, w, h = box
            pill(c, x + w * 0.24, y + h * 0.25, 'YOUR BILL', 1.0, col=RED, size=30)
            pill(c, x + w * 0.42, y + h * 0.485, '$ / kWh', 1.0, col=INK, size=26)
        if t > t29:
            mono(c, '$ PER MW-DAY · PJM', LX, 1200, 20, GREY, 'l', a=pr(t, t29, 0.4))
        credit(c, 'PHOTO: ROBBIEIANMORRISON · CC BY 4.0')
        return
    headline(c, ['~Half of it:', 'data centers.'], LX, HY, 130, t, th - 0.3, hl=(0, ('', '~Half')), hl_col=YEL)
    def dr(cc):
        mono(cc, 'PJM CAPACITY COSTS, LAST 4 AUCTIONS (MARKET MONITOR)', 40, 66, 19, GREY)
        donut(cc, 430, 300, 165, 0.46, pr(t, th, 1.0), col=RED, width=56)
        text(cc, '~46%', 430, 330, 'blk', 92, INK, 'c')
    card(c, 540, 1100, 860, 520, 1.5, pr(t, th - 0.2, 0.5), dr)
    if t > tr - 0.4:
        pill(c, 540, 1450, 'LANDS ON YOUR POWER BILL', pr(t, tr - 0.4, 0.3), col=INK, size=38)


def sc_race(c, t, S):
    tt = ph('in texas'); tm = ph('microsoft signed'); ty = ph('yes that three')
    bg_cream(c, t)
    kicker(c, 'THE RACE FOR POWER', t, S['t0'] + 0.1)
    if t < tm - 0.3:
        headline(c, ['Hunting for', 'power.'], LX, HY, 150, t, S['t0'] + 0.2, hl=(1, ('', 'power.')), hl_col=GREEN)
        def dr(cc):
            mono(cc, 'TEXAS · GRID CONNECTION REQUESTS', 50, 66, 20, RED)
            bars(cc, 60, 120, 740, 400, [('RECORD PEAK', 1, '1x', INK), ('REQUESTED', 5, '5x', RED)], pr(t, tt + 0.3, 1.2), ymax=5.6)
        card(c, 540, 1180, 860, 620, -1.5, pr(t, tt - 0.2, 0.5), dr)
        return
    headline(c, ['Three Mile Island.', 'Back on.'], LX, HY, 112, t, tm - 0.2, hl=(1, ('', 'Back on.')), hl_col=GREEN)
    photo_card(c, 'R3_tmi.jpg', 540, 1110, 860, 640, -1.2, pr(t, tm - 0.1, 0.5), zoom=1.05 + 0.02 * (t - tm), fx=0.4, fy=0.35)
    pill(c, 540, 1460, 'MICROSOFT · 20-YEAR DEAL', pr(t, tm + 0.4, 0.3), col=INK, size=36)
    if t > ty - 0.2:
        def d2(cc):
            mono(cc, '1979', 36, 56, 22, RED)
            text(cc, "America's worst", 36, 120, 'blk', 46, INK)
            text(cc, 'nuclear accident', 36, 170, 'blk', 46, INK)
        card(c, 700, 830, 450, 210, 3, pr(t, ty + 0.6, 0.4), d2, rad=18)
    credit(c, 'PHOTO: US DEPT. OF ENERGY · PUBLIC DOMAIN')


def sc_predict(c, t, S):
    tc = ph('more close calls'); tb = ph('bills keep climbing'); ty = ph('bring your own power')
    k_dark = pr(t, tc - 0.2, 1.2)
    cover(c, img('R10_skyline.jpg'), 0, 0, W, H, 1.6 + 0.02 * (t - S['t0']), 0.55, 0.62)
    # right half flickers dark
    for i in range(8):
        kk = cl(k_dark * 8 - i)
        if kk <= 0: continue
        fl = 1.0 if kk >= 1 else (0.5 + 0.5 * (math.sin(t * 50 + i) > 0))
        c.drawRect(R.MakeXYWH(540 + i * 68, 0, 70, H), paint((0, 0, 0), 0.82 * fl * eo(kk)))
    c.drawRect(R.MakeWH(W, 900), paint(shader=lin(0, 0, 0, 900, [argb((0, 0, 0), 0.75), argb((0, 0, 0), 0.0)])))
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    headline(c, ["The grid doesn't", 'collapse.'], LX, HY, 118, t, S['t0'] + 0.3, col=PAPER, hl=(1, ('', 'collapse.')), hl_col=RED)
    if t > tc - 0.3:
        headline(c, ['More close calls.'], LX, HY + 260, 88, t, tc - 0.3, col=(230, 230, 236))
    items = ((tb, 'BILLS KEEP CLIMBING'), (ty, 'BRING YOUR OWN POWER'))
    for i, (t0, s) in enumerate(items):
        pill(c, 540, 1180 + i * 130, s, pr(t, t0 - 0.2, 0.3), col=(PAPER, RED)[i], txt=(INK, PAPER)[i], size=42)
    if t > ty + 0.6:
        pill(c, 540, 1440, 'OR WAIT IN LINE', pr(t, ph('wait in line') - 0.2, 0.3), col=INK, size=36)
    credit(c, 'PHOTO: VYNEDJ · CC BY 4.0', col=(190, 190, 200))


def sc_ask(c, t, S):
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Would you pay more', 'so AI can run?'], LX, HY, 112, t, S['t0'] + 0.1, hl=(1, ('so ', 'AI can run?')), hl_col=YEL)
    pill(c, 360, 1100, 'YES', pr(t, ph('yes or no') - 0.1, 0.3), col=GREEN, txt=INK, size=80)
    pill(c, 720, 1100, 'NO', pr(t, ph('yes or no') + 0.2, 0.3), col=RED, txt=PAPER, size=80)
    mono(c, 'TELL ME IN THE COMMENTS', 540, 1300, 26, INK, 'c', a=pr(t, ph('comments') - 0.2, 0.3))
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='alley', t0=ph('this is ashburn') - 0.2, fn=sc_alley, tin='whip'),
    dict(k='night', t0=ph('that night') - 0.2, fn=sc_night, tin='wipe', col=INK),
    dict(k='scramble', t0=ph('suddenly the grid') - 0.2, fn=sc_scramble, tin='flash'),
    dict(k='share', t0=ph("here's why that's") - 0.2, fn=sc_share, tin='zoom'),
    dict(k='map', t0=ph('look at this government') - 0.2, fn=sc_map, tin='whip'),
    dict(k='bills', t0=ph('and somebody has') - 0.2, fn=sc_bills, tin='zoom'),
    dict(k='race', t0=ph('so tech companies') - 0.2, fn=sc_race, tin='whip'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('vanished'), 12, 0.35)
EP.shk(ph('one small part failed') + 0.4, 10, 0.3)
EP.shk(ph('two hundred seventy'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
