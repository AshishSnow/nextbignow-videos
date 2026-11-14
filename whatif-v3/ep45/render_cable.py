"""NextBigNow (editorial look) ep 45: What happens if the undersea internet cables get cut?
Facts: UN Geneva Feb 2026 (~99% of international internet traffic via submarine cables; 150-200 incidents/yr; ~80% human activity).
APNIC (G. Huston, 14 Oct 2026): 607 in-service systems, ~200 faults/yr, 86% fishing/anchoring, ~60 repair ships, repair times more
than doubled in a decade, Baltic 11 disruptions since 2023, Bab al-Mandab Sep 2025 ~25% Asia-Europe-ME capacity, Perth Aug 2026
Indigo West/Central damaged, tanker under AFP investigation. AP Sep 2025 (likely anchor drag; 4 cables; at least 10 nations incl.
India, Pakistan, UAE). AP Feb 2022 (Tonga: ~90 km of cable replaced; restored after 5+ weeks; Starlink helped)."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from edkit import _grain
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('CB_DIR', 'cable'))
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
SEA_T = (18, 120, 190); SEA_B = (4, 22, 52); CYAN = (60, 220, 255); SAND = (40, 52, 70)


def kicker(c, s, t, t0, y=400, col=GREY):
    k = pr(t, t0, 0.3)
    if k > 0:
        c.drawRect(R.MakeXYWH(LX, y - 22, 14, 14), paint(RED, k))
        mono(c, s, LX + 30, y - 8, 26, col, a=k)


# ------------------------------------------------------------------ props
def bg_sea(c, t, floor=1500):
    """deep ocean: vivid blue gradient, god rays, drifting particles, seabed."""
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb(SEA_T), argb((8, 60, 120)), argb(SEA_B)])))
    for i in range(5):
        x = 120 + i * 220 + 40 * math.sin(t * 0.4 + i)
        c.drawPath(poly([(x - 30, 0), (x + 50, 0), (x + 260, floor), (x + 60, floor)], True),
                   paint(shader=lin(0, 0, 0, floor, [argb((180, 240, 255), 0.13), argb((180, 240, 255), 0.0)])))
    for i in range(70):
        px = (hsh(i, 1) * W + t * 8 * (hsh(i, 2) - 0.5)) % W
        py = (hsh(i, 3) * H - t * (10 + 25 * hsh(i, 4))) % H
        c.drawCircle(px, py, 1.5 + 2.5 * hsh(i, 5), paint((200, 240, 255), 0.25 + 0.3 * hsh(i, 6)))
    p = skia.Path(); p.moveTo(0, floor)
    for i in range(13): p.lineTo(i * 90, floor + 18 * math.sin(i * 1.3) + 10 * math.cos(i * 2.7))
    p.lineTo(W, H); p.lineTo(0, H); p.close()
    c.drawPath(p, paint(shader=lin(0, floor, 0, H, [argb((30, 46, 70)), argb((8, 14, 26))])))
    for i in range(30):
        c.drawCircle(hsh(i, 9) * W, floor + 40 + hsh(i, 8) * 300, 4 + 10 * hsh(i, 7), paint((60, 80, 110), 0.5))
    _grain(c, 0.04)


def cable_line(c, pts, k=1.0, cut=None, t=0.0, col=(20, 20, 24), w=16, glow=True):
    """seabed cable along pts; data pulses travel along it; cut = (x, k_cut) breaks it at x."""
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    meas = skia.PathMeasure(p, False); L = meas.getLength()
    seg = skia.Path(); meas.getSegment(0, L * eo(cl(k)), seg, True)
    c.drawPath(seg, stroke((0, 0, 0), w + 6, 0.35))
    c.drawPath(seg, stroke(col, w))
    c.drawPath(seg, stroke((90, 90, 100), 3, 0.6))
    if glow and k >= 1:
        for j in range(6):
            d = ((t * 0.35 + j / 6) % 1) * L
            if cut and cut[1] > 0:
                pos = meas.getPosTan(d)[0]
                if pos.x() > cut[0]: continue
            pos = meas.getPosTan(d)[0]
            c.drawCircle(pos.x(), pos.y(), 14, paint(CYAN, 0.35, blur=8)); c.drawCircle(pos.x(), pos.y(), 6, paint((220, 255, 255)))
    if cut and cut[1] > 0:
        x, kc = cut
        y = pts[0][1] + (pts[-1][1] - pts[0][1]) * (x - pts[0][0]) / max(1, pts[-1][0] - pts[0][0])
        gap = 40 * eo(cl(kc))
        c.drawRect(R.MakeXYWH(x - gap, y - 30, gap * 2, 60), paint(shader=lin(0, y - 30, 0, y + 30, [argb((10, 40, 80), 0), argb((10, 40, 80)), argb((10, 40, 80), 0)])))
        sparks(c, x, y, kc)


def sparks(c, x, y, k):
    if k <= 0 or k >= 1: return
    for i in range(16):
        a = hsh(i, 11) * math.tau; d = 30 + 140 * eo(k) * (0.5 + hsh(i, 12))
        c.drawCircle(x + math.cos(a) * d, y + math.sin(a) * d * 0.7, 6 * (1 - k) + 1, paint(YEL, 1 - k))
    c.drawCircle(x, y, 60 + 120 * k, paint((255, 240, 200), 0.6 * (1 - k), blur=20))


def cross_section(c, x, y, s, k=1.0, label=True):
    """cut-away cable: rings of polyethylene, copper, steel wires, fibres."""
    c.save(); c.translate(x, y); c.scale(s * eback(cl(k), 1.4), s * eback(cl(k), 1.4))
    c.drawCircle(8, 16, 200, paint((0, 0, 0), 0.25, blur=26))
    c.drawCircle(0, 0, 200, paint(shader=skia.GradientShader.MakeRadial((-60, -60), 280, [argb((70, 70, 80)), argb((14, 14, 18))])))
    c.drawCircle(0, 0, 150, paint(shader=skia.GradientShader.MakeRadial((-40, -40), 200, [argb((255, 190, 120)), argb((170, 90, 40))])))
    for i in range(18):
        a = i / 18 * math.tau
        c.drawCircle(math.cos(a) * 112, math.sin(a) * 112, 22, paint(shader=skia.GradientShader.MakeRadial((math.cos(a) * 112 - 8, math.sin(a) * 112 - 8), 30, [argb((235, 235, 245)), argb((120, 120, 135))])))
    c.drawCircle(0, 0, 80, paint((240, 200, 60)))
    c.drawCircle(0, 0, 60, paint((30, 30, 36)))
    for i in range(8):
        a = i / 8 * math.tau; col = [(255, 80, 80), (60, 200, 255), (60, 220, 120), (255, 214, 60)][i % 4]
        c.drawCircle(math.cos(a) * 32, math.sin(a) * 32, 11, paint(col)); c.drawCircle(math.cos(a) * 32, math.sin(a) * 32, 18, paint(col, 0.25, blur=6))
    c.drawCircle(0, 0, 11, paint((230, 255, 255)))
    c.restore()


def ship(c, x, y, s, col=(26, 26, 30), acc=RED):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(poly([(-200, -30), (200, -30), (160, 40), (-170, 40)], True), paint(col))
    c.drawRect(R.MakeXYWH(-200, -30, 400, 14), paint(acc))
    c.drawRect(R.MakeXYWH(60, -110, 110, 80), paint((240, 240, 240)))
    for i in range(3): c.drawRect(R.MakeXYWH(74 + i * 32, -95, 20, 18), paint((40, 60, 90)))
    for i in range(4): c.drawRect(R.MakeXYWH(-170 + i * 52, -78, 46, 48), paint([(222, 32, 44), (40, 110, 240), (30, 205, 120), (255, 214, 60)][i]))
    c.drawRect(R.MakeXYWH(120, -170, 16, 60), paint((60, 60, 66)))
    c.restore()


def anchor(c, x, y, s, col=(30, 30, 34)):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, -90, 18, stroke(col, 9))
    c.drawRect(R.MakeXYWH(-7, -72, 14, 130), paint(col))
    c.drawRect(R.MakeXYWH(-40, -60, 80, 12), paint(col))
    p = skia.Path(); p.addArc(R.MakeXYWH(-60, -10, 120, 80), 0, 180)
    c.drawPath(p, stroke(col, 13))
    c.drawPath(poly([(-60, 30), (-80, 10), (-52, 6)], True), paint(col)); c.drawPath(poly([(60, 30), (80, 10), (52, 6)], True), paint(col))
    c.restore()


def mini_ship(c, x, y, s, old=0.0):
    col = lerp_col((26, 26, 30), (190, 184, 176), old)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawPath(poly([(-30, -6), (30, -6), (24, 8), (-26, 8)], True), paint(col))
    c.drawRect(R.MakeXYWH(6, -20, 16, 14), paint(col))
    c.drawRect(R.MakeXYWH(-30, -6, 60, 3), paint(lerp_col(RED, (200, 190, 180), old)))
    c.restore()


def volcano(c, x, y, k, t):
    c.drawPath(poly([(x - 330, y), (x - 60, y - 260), (x + 60, y - 260), (x + 330, y)], True),
               paint(shader=lin(0, y - 260, 0, y, [argb((60, 50, 56)), argb((24, 22, 28))])))
    if k > 0:
        for i in range(24):
            kk = cl(k * 1.4 - hsh(i, 21) * 0.4)
            if kk <= 0: continue
            dx = (hsh(i, 22) - 0.5) * 360 * kk; dy = -260 - 700 * eo(kk) * (0.5 + hsh(i, 23))
            r = 50 + 90 * kk * hsh(i, 24)
            c.drawCircle(x + dx, y + dy, r, paint((70, 66, 72), 0.6 * (1 - kk * 0.6)))
        c.drawCircle(x, y - 270, 70 + 50 * math.sin(t * 20), paint((255, 120, 40), 0.7 * cl(k * 3), blur=20))
        ring = 900 * eo(cl(k * 1.2))
        c.drawCircle(x, y - 260, ring, stroke((255, 255, 255), 6, 0.5 * (1 - cl(k * 1.2))))


def satellite(c, x, y, s, t):
    c.save(); c.translate(x, y); c.rotate(-20 + 6 * math.sin(t)); c.scale(s, s)
    for sx in (-1, 1):
        c.drawRect(R.MakeXYWH(sx * 70 - (110 if sx < 0 else 0), -30, 110, 60), paint((40, 80, 170)))
        for j in range(4): c.drawLine(sx * 70 - (110 if sx < 0 else 0) + j * 27, -30, sx * 70 - (110 if sx < 0 else 0) + j * 27, 30, stroke((140, 180, 255), 2))
    c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(-60, -45, 120, 90), 14, 14), paint((220, 220, 228)))
    c.drawCircle(0, 0, 18, paint(RED))
    c.restore()


def xmark(c, x, y, s, k, col=RED):
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(s * eback(cl(k), 2), s * eback(cl(k), 2))
    c.drawLine(-20, -20, 20, 20, stroke(col, 10)); c.drawLine(20, -20, -20, 20, stroke(col, 10))
    c.restore()


# ================================================================== hook
def sc_hook(c, t, S):
    tb = ph('blew up'); tf = ph('fell off'); tg = ph('gone'); tq = ph('so what happens')
    if t < tq - 0.15:
        bg_sea(c, t, floor=1330)
        kicker(c, 'JAN 15, 2022 · SOUTH PACIFIC', t, 0.2, col=(190, 230, 255))
        volcano(c, 330, 1330, pr(t, tb - 0.1, 2.2), t)
        cable_line(c, [(-20, 1380), (420, 1360), (760, 1395), (1100, 1370)], 1.0, cut=(600, pr(t, tf, 0.7)), t=t, w=18)
        if t < tf - 0.1:
            headline(c, ['A volcano.', 'Under the sea.'], LX, HY + 40, 120, t, 0.25, col=PAPER, hl=(1, ('Under the ', 'sea.')), hl_col=BLUE)
        else:
            headline(c, ['A whole country.'], LX, HY + 40, 120, t, tf - 0.1, col=PAPER)
        if t > tg - 0.3:
            headline(c, ['Offline.'], LX, HY + 180, 170, t, tg - 0.3, col=PAPER, hl=(0, ('', 'Offline.')), hl_col=RED)
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What if the', 'ocean cables', 'get cut?'], LX, HY + 20, 132, t, tq - 0.05, col=PAPER, hl=(2, ('get ', 'cut?')), hl_col=INK)
    cross_section(c, 540, 1240, 0.95, pr(t, tq + 0.3, 0.6))


def sc_catch(c, t, S):
    th = ph('garden hose'); t99 = ph('ninety nine percent')
    bg_cream(c, t)
    kicker(c, 'HOW THE INTERNET CROSSES OCEANS', t, S['t0'] + 0.1)
    if t < th - 1.6:
        headline(c, ['99% goes', 'under the sea.'], LX, HY, 132, t, t99 - 0.3, hl=(0, ('', '99%')), hl_col=CYAN)
        donut(c, 540, 1180, 270, 0.99, pr(t, t99 - 0.2, 1.4), col=BLUE, label='99%')
        mono(c, 'OF INTERNET TRAFFIC BETWEEN COUNTRIES', 540, 1540, 23, GREY, 'c', a=pr(t, t99, 0.4))
        satellite(c, 820, 860, 0.55 * pr(t, ph('through space') - 0.1, 0.3), t)
        xmark(c, 820, 860, 2.2, pr(t, ph('through space') + 0.2, 0.3))
        return
    headline(c, ['As thick as a', 'garden hose.'], LX, HY, 128, t, th - 1.6, hl=(1, ('', 'garden hose.')), hl_col=YEL)
    cross_section(c, 540, 1180, 1.05, pr(t, th - 1.4, 0.7))
    mono(c, 'DEEP-SEA CABLE · CROSS-SECTION', 540, 1480, 23, GREY, 'c', a=pr(t, th - 1.0, 0.4))


def sc_tonga(c, t, S):
    t90 = ph('ninety kilometers'); tc = ph('calls abroad'); tw5 = ph('more than five weeks')
    bg_cream(c, t)
    kicker(c, 'CASE STUDY · TONGA, 2022', t, S['t0'] + 0.1)
    if t < tc - 0.3:
        k = pr(t, t90 - 0.4, 0.5)
        text(c, '%d km' % int(90 * eo(pr(t, t90 - 0.4, 1.0))), LX, 760, 'blk', 260, RED, track=-0.05, a=eo(k))
        text(c, 'of cable ripped up', LX, 850, 'sb', 54, GREY, a=eo(k))
        def dr(cc):
            cc.drawRect(R.MakeWH(860, 520), paint(shader=lin(0, 0, 0, 520, [argb((20, 110, 180)), argb((6, 30, 66))])))
            cable_line(cc, [(-10, 330), (300, 310), (560, 345), (870, 320)], 1.0, cut=(430, pr(t, t90, 0.8)), t=t, w=14)
            mono(cc, 'MAIN INTERNATIONAL CABLE', 40, 60, 22, (190, 230, 255))
        card(c, 540, 1240, 860, 520, -1.5, pr(t, S['t0'] + 0.3, 0.5), dr)
        return
    if t < tw5 - 0.4:
        headline(c, ['All cut.'], LX, HY, 170, t, tc - 0.3, hl=(0, ('All ', 'cut.')), hl_col=RED_L)
        for i, (p_, lab) in enumerate((('calls abroad', 'Calls abroad'), ('card payments', 'Card payments'), ('news from family', 'News from family'))):
            def dr(cc, lab=lab, p_=p_):
                text(cc, lab, 44, 120, 'blk', 64, INK, maxw=560)
                xmark(cc, 700, 98, 1.6, pr(t, ph(p_) + 0.3, 0.3))
            card(c, 540, 860 + i * 230, 820, 190, (-2, 1.5, -1)[i], pr(t, ph(p_) - 0.15, 0.4), dr, rad=22)
        return
    headline(c, ['5+ weeks', 'to fix it.'], LX, HY, 150, t, tw5 - 0.4, hl=(0, ('', '5+ weeks')), hl_col=YEL)
    timeline(c, 200, 820, 1150, [(0.0, 'Jan 15', 'ERUPTION'), (0.5, '+3 wks', 'STILL DOWN'), (1.0, 'Feb 22', 'BACK ONLINE')], pr(t, tw5 - 0.2, 2.2), t)


def sc_redsea(c, t, S):
    ta = ph('dragged its anchor'); t10 = ph('at least ten countries'); tq_ = ph('about a quarter')
    bg_sea(c, t, floor=1290)
    kicker(c, 'SEPT 2025 · RED SEA', t, S['t0'] + 0.1, col=(190, 230, 255))
    if t < t10 - 0.3:
        headline(c, ['One anchor.', 'Four cables.'], LX, HY, 130, t, ta - 0.6, col=PAPER, hl=(1, ('', 'Four cables.')), hl_col=RED)
        ka = pr(t, ta - 0.3, 3.2)
        sx = 140 + 700 * eio(ka)
        ship(c, sx + 60, 860, 0.8)
        ax = sx; ay = 960 + 340 * eo(cl(ka * 3))
        c.drawLine(sx + 60, 880, ax, ay, stroke((30, 30, 34), 5))
        for i in range(4):
            y = 1080 + i * 60
            cx_ = 220 + i * 150
            hit = cl((sx - cx_ + 40) / 80) if ay > 1060 else 0
            cable_line(c, [(-20, y), (1100, y + 10)], 1.0, cut=(cx_, hit), t=t + i * 0.3, w=12)
        anchor(c, ax, min(ay, 1300), 0.7)
        return
    headline(c, ['Felt in 10+', 'countries.'], LX, HY, 130, t, t10 - 0.3, col=PAPER, hl=(0, ('Felt in ', '10+')), hl_col=RED)
    for i, (p_, lab) in enumerate((('india', 'INDIA'), ('pakistan', 'PAKISTAN'), ('uae', 'UAE'))):
        pill(c, 230 + i * 300, 960, lab, pr(t, ph(p_) - 0.1, 0.3), col=PAPER, txt=INK, size=44)
    if t > tq_ - 0.3:
        def dr(cc):
            mono(cc, 'ASIA · EUROPE · MIDDLE EAST TRAFFIC HIT (EST.)', 40, 66, 20, GREY)
            donut(cc, 430, 290, 160, 0.25, pr(t, tq_, 1.0), col=RED, width=56)
            text(cc, '~25%', 430, 320, 'blk', 96, INK, 'c')
        card(c, 540, 1230, 860, 500, 1.5, pr(t, tq_ - 0.3, 0.5), dr)


def sc_faults(c, t, S):
    t200 = ph('two hundred'); t4 = ph('four a week'); ts = ph("aren't spies"); tfb = ph('fishing boats')
    bg_cream(c, t)
    kicker(c, 'HOW OFTEN CABLES BREAK', t, S['t0'] + 0.1)
    if t < ts - 0.3:
        headline(c, ['~200 breaks', 'a year.'], LX, HY, 140, t, t200 - 0.4, hl=(0, ('', '~200')), hl_col=RED_L)
        k = pr(t, t200 - 0.2, 2.6)
        n = int(208 * eo(k))
        for i in range(208):
            col_, row = i % 16, i // 16
            x = 210 + col_ * 44; y = 830 + row * 44
            on = i < n
            c.drawCircle(x, y, 14 if on else 5, paint(RED if on else LIGHT))
        if t > t4 - 0.3:
            pill(c, 540, 1440, '≈ 4 EVERY WEEK', pr(t, t4 - 0.3, 0.3), col=INK, size=46)
        return
    headline(c, ['Not spies.'], LX, HY, 160, t, ts - 0.3)
    def d1(cc):
        mono(cc, 'MAIN CAUSE', 44, 64, 22, RED)
        text(cc, 'Fishing boats', 44, 150, 'blk', 70, INK)
        text(cc, '& anchors', 44, 230, 'blk', 70, INK)
        anchor(cc, 690, 160, 0.9)
    card(c, 540, 980, 820, 300, -2, pr(t, tfb - 0.2, 0.45), d1, rad=24)
    def d2(cc):
        mono(cc, 'SHARE OF FAULTS (APNIC)', 44, 64, 22, GREY)
        bar_split(cc, 44, 110, 730, 70, [('fishing & anchors', 0.86, INK), ('', 0.14, LIGHT)], pr(t, tfb + 0.4, 1.0), t)
    card(c, 540, 1330, 820, 280, 1.5, pr(t, tfb + 0.2, 0.45), d2, rad=24)


def sc_repair(c, t, S):
    t60 = ph('only about sixty'); told = ph('getting old'); td = ph('more than doubled')
    bg_red(c, t)
    kicker(c, 'THE SCARY PART', t, S['t0'] + 0.1, col=(255, 200, 200))
    if t < td - 0.4:
        headline(c, ['Only ~60', 'repair ships.'], LX, HY, 140, t, t60 - 0.3, col=PAPER, hl=(0, ('Only ', '~60')), hl_col=INK)
        k = pr(t, t60, 1.6)
        for i in range(60):
            col_, row = i % 10, i // 10
            kk = cl(k * 60 - i)
            if kk <= 0: continue
            old = pr(t, told - 0.1 + (i % 7) * 0.05, 0.4) if (i * 37) % 10 < 6 else 0
            c.save(); c.translate(0, 0)
            c.drawRRect(skia.RRect.MakeRectXY(R.MakeXYWH(130 + col_ * 82, 820 + row * 84, 72, 70), 12, 12), paint(PAPER, 0.95 * eo(kk)))
            mini_ship(c, 166 + col_ * 82, 862 + row * 84, 0.95 * eback(kk, 1.5), old)
            c.restore()
        if t > told - 0.2:
            mono(c, 'GREY = NEARING END OF LIFE (BY 2040)', 540, 1400, 22, (255, 220, 220), 'c', a=pr(t, told, 0.4))
        return
    headline(c, ['Repairs take', '2x longer.'], LX, HY, 140, t, td - 0.4, col=PAPER, hl=(1, ('', '2x')), hl_col=INK)
    def dr(cc):
        mono(cc, 'TIME TO REPAIR A CABLE FAULT', 50, 70, 22)
        bars(cc, 60, 120, 740, 440, [('10 YEARS AGO', 1.0, '1x', INK), ('NOW', 2.1, '2x+', RED)], pr(t, td, 1.3))
    card(c, 540, 1230, 860, 700, -1.5, pr(t, td - 0.3, 0.5), dr)


def sc_hot(c, t, S):
    bg_ink(c, t)
    kicker(c, 'WHY PEOPLE ARE WORRIED', t, S['t0'] + 0.1, col=(170, 170, 176))
    headline(c, ['Same hot', 'spots.'], LX, HY, 150, t, S['t0'] + 0.3, col=PAPER, hl=(1, ('', 'spots.')), hl_col=RED)
    rows = ((ph('baltic sea'), 'BALTIC SEA', '11 disruptions', 'since 2023', 840),
            (ph('perth'), 'PERTH, AUSTRALIA · AUG 2026', '2 cables damaged', 'Police looking into a tanker', 1110),)
    for i, (t0, lab, a, b, y) in enumerate(rows):
        def dr(cc, lab=lab, a=a, b=b):
            c2 = cc
            c2.drawCircle(70, 120, 26, paint(RED)); c2.drawCircle(70, 120, 10, paint(PAPER))
            c2.drawCircle(70, 120, 26 + 20 * ((t * 1.2) % 1), stroke(RED, 4, 1 - ((t * 1.2) % 1)))
            mono(c2, lab, 120, 70, 21, RED)
            text(c2, a, 120, 150, 'blk', 62, INK, maxw=640)
            text(c2, b, 120, 205, 'sb', 38, GREY, maxw=640)
        card(c, 540, y, 840, 240, (-1.5, 1.5)[i], pr(t, t0 - 0.25, 0.45), dr, rad=22)
    def d3(cc):
        mono(cc, 'RED SEA · SEPT 2025', 120, 70, 21, RED)
        cc.drawCircle(70, 120, 26, paint(RED)); cc.drawCircle(70, 120, 10, paint(PAPER))
        text(cc, '4 cables at once', 120, 150, 'blk', 62, INK, maxw=640)
        text(cc, 'Anchor drag (likely)', 120, 205, 'sb', 38, GREY)
    card(c, 540, 1380, 840, 240, -1, pr(t, ph('police') + 0.3, 0.45), d3, rad=22)


def sc_sat(c, t, S):
    tn = ph('not really'); tt = ph('starlink helped'); tm = ph('way more data')
    bg_sea(c, t, floor=1700)
    kicker(c, 'PLAN B?', t, S['t0'] + 0.1, col=(190, 230, 255))
    headline(c, ['Satellites?', 'Not enough.'], LX, HY, 140, t, S['t0'] + 0.2, col=PAPER, hl=(1, ('Not ', 'enough.')), hl_col=RED)
    satellite(c, 760, 860, 0.9, t)
    if t > tt - 0.3:
        pill(c, 330, 880, 'HELPED TONGA', pr(t, tt - 0.2, 0.3), col=PAPER, txt=INK, size=38)
    def dr(cc):
        mono(cc, 'DATA CAPACITY (ILLUSTRATIVE)', 50, 70, 22)
        kk = pr(t, tm - 0.3, 1.2)
        for i, (lab, fr, col) in enumerate((('ONE BIG CABLE', 1.0, BLUE), ('SATELLITE BACKUP', 0.06, RED))):
            y = 140 + i * 170
            mono(cc, lab, 50, y, 24, INK)
            cc.drawRect(R.MakeXYWH(50, y + 24, 740 * fr * eo(cl(kk * 2 - i)), 80), paint(col))
    card(c, 540, 1210, 860, 440, 1.5, pr(t, tm - 0.5, 0.5), dr)


def sc_predict(c, t, S):
    tr = ph('finds another path'); tg = ph('hit hard'); td = ph('go dark')
    bg_red(c, t)
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    if t < tg - 0.4:
        headline(c, ["The internet", "doesn't collapse."], LX, HY + 40, 126, t, S['t0'] + 0.2, col=PAPER, hl=(1, ("doesn't ", 'collapse.')), hl_col=INK)
        node_graph(c, t, 0.0, cx=540, cy=1100, seed=7, n=24)
        if t > tr - 0.3: pill(c, 540, 1450, 'TRAFFIC REROUTES', pr(t, tr - 0.3, 0.3), col=PAPER, txt=INK, size=40)
        return
    headline(c, ['But one region', 'goes dark.'], LX, HY + 40, 130, t, tg - 0.4, col=PAPER, hl=(1, ('', 'goes dark.')), hl_col=INK)
    def dr(cc):
        mono(cc, 'MOST AT RISK', 50, 70, 22, RED)
        text(cc, 'Places with only', 50, 160, 'blk', 64, INK)
        text(cc, '1 or 2 cables.', 50, 236, 'blk', 64, RED)
        for i in range(2):
            cable_line(cc, [(50, 320 + i * 50), (790, 320 + i * 50)], 1.0, cut=(420 + i * 120, pr(t, td - 0.2 + i * 0.2, 0.7)), t=t, w=12, glow=True)
    card(c, 540, 1250, 860, 440, -1.5, pr(t, ph('the places') - 0.3, 0.5), dr)


def sc_watch(c, t, S):
    bg_cream(c, t)
    kicker(c, 'WHAT TO WATCH', t, S['t0'] + 0.1)
    headline(c, ['Watch for', 'three things.'], LX, HY, 132, t, S['t0'] + 0.1, hl=(1, ('', 'three things.')), hl_col=GREEN)
    items = ((ph('more repair ships'), 'ONE', 'More repair ships'), (ph('navies guarding'), 'TWO', 'Navies guarding cables'), (ph('big tech companies'), 'THREE', 'Big tech laying its own'))
    for i, (t0, n, a) in enumerate(items):
        def dr(cc, n=n, a=a, i=i):
            mono(cc, n, 44, 64, 22, RED)
            text(cc, a, 44, 150, 'blk', 62, INK, maxw=560)
            if i == 0: mini_ship(cc, 700, 120, 2.0)
            elif i == 1: anchor(cc, 700, 120, 0.7, col=BLUE)
            else: cross_section(cc, 700, 115, 0.35)
        card(c, 540, 860 + i * 250, 820, 220, (-2, 1.5, -1)[i], pr(t, t0 - 0.2, 0.45), dr, rad=22)


def sc_ask(c, t, S):
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Could you live', '5 weeks offline?'], LX, HY, 118, t, S['t0'] + 0.1, hl=(1, ('', '5 weeks')), hl_col=YEL)
    pill(c, 360, 1100, 'YES', pr(t, ph('yes or no') - 0.1, 0.3), col=GREEN, txt=INK, size=80)
    pill(c, 720, 1100, 'NO', pr(t, ph('yes or no') + 0.2, 0.3), col=RED, txt=PAPER, size=80)
    mono(c, 'TELL ME IN THE COMMENTS', 540, 1300, 26, INK, 'c', a=pr(t, ph('comments') - 0.2, 0.3))
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='catch', t0=ph("here's what most") - 0.2, fn=sc_catch, tin='whip'),
    dict(k='tonga', t0=ph('that country was tonga') - 0.2, fn=sc_tonga, tin='zoom'),
    dict(k='redsea', t0=ph("and it's not just") - 0.2, fn=sc_redsea, tin='wipe', col=SEA_B),
    dict(k='faults', t0=ph('this happens way more') - 0.2, fn=sc_faults, tin='whip'),
    dict(k='repair', t0=ph("now here's the scary") - 0.2, fn=sc_repair, tin='flash'),
    dict(k='hot', t0=ph('so why are people') - 0.2, fn=sc_hot, tin='wipe', col=INK),
    dict(k='sat', t0=ph("so can't satellites") - 0.2, fn=sc_sat, tin='zoom'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='watch', t0=ph('watch for three') - 0.2, fn=sc_watch, tin='whip'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('fell off'), 12, 0.35)
EP.shk(ph('dragged its anchor', end=True), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
