"""NextBigNow ep 48: What happens if GPS goes down?
Facts: Finnair (OMAAT, Apr 2024) - two HEL-TAY flights returned to Helsinki after GPS interference; Tartu approach relied on GPS; route
suspended 29 Apr - 31 May 2024. LRT (Mar 2026) - Lithuania pilot GPS-interference reports: 169 Jan + 118 Feb 2026 (302 incl. 5 Mar days);
regulator links to Russia. Eurointegration/Danish data (Aug 2026) - Bornholm station: 30 jamming/spoofing instances in 2026 so far vs 16 in
2025, 11 in 2024; 29 Jul no adequate signal between Gdansk and Gotland. UK gov / London Economics (2021): 7-day GNSS loss = GBP 7.6bn;
emergency services GBP 3.5bn, road 1.7bn, maritime 1.5bn (87.6% together).
Photos (Wikimedia Commons): GPS IIIA artwork - US Air Force PD; GPS III launch - US Space Force (Gwendolyn Kurzen) PD; Tartu approach lights -
Ivo Kruusamagi CC BY-SA 4.0; 707 cockpit - Wilfredor CC0; jet - MarcusObal CC BY-SA 3.0 (illustrative); Bornholm fog - Socket0 CC0."""
import sys, os, math, re
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import *
from edkit import _grain
import photokit as PK
from photokit import img, cover, cutout, photo_card, credit, shade, kicker, place
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('GP_DIR', 'gps'))
PK.IMG = os.path.join(HERE, 'gps', 'img')
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
NAVY = (8, 18, 42); CYAN = (70, 225, 255)


def bg_map(c, t):
    c.drawRect(R.MakeWH(W, H), paint(shader=lin(0, 0, 0, H, [argb((14, 30, 68)), argb(NAVY)])))
    for i in range(0, W, 90): c.drawLine(i, 0, i, H, stroke((60, 90, 150), 1, 0.25))
    for j in range(0, H, 90): c.drawLine(0, j, W, j, stroke((60, 90, 150), 1, 0.25))
    for i in range(160):  # dotted landmass
        x = 60 + hsh(i, 61) * 980; y = 1050 + hsh(i, 62) * 520
        if (x - 300) ** 2 / 4 + (y - 1300) ** 2 < 260 ** 2 or (x - 900) ** 2 / 3 + (y - 1450) ** 2 < 200 ** 2:
            c.drawCircle(x, y, 5, paint((90, 130, 200), 0.6))
    _grain(c, 0.04)


def signal(c, x, y, t, k=1.0, col=CYAN, jam=0.0, down=True):
    for i in range(4):
        ph_ = (t * 0.8 + i / 4) % 1
        r = 60 + 520 * ph_
        p = skia.Path(); p.addArc(R.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 50 if down else 230, 80)
        cc = lerp_col(col, RED, jam)
        fl = 1.0 if jam < 0.5 else (0.3 + 0.7 * (math.sin(t * 40 + i) > 0))
        c.drawPath(p, stroke(cc, 7, (1 - ph_) * 0.8 * k * fl))


def jammer(c, x, y, t, k):
    if k <= 0: return
    for i in range(5):
        ph_ = (t * 1.6 + i / 5) % 1
        r = 40 + 600 * ph_
        c.drawCircle(x, y, r, stroke(RED, 9, (1 - ph_) * 0.7 * k))
    c.drawCircle(x, y, 26, paint(RED, k)); c.drawCircle(x, y, 60, paint(RED, 0.3 * k, blur=20))


def pin(c, x, y, lab, k=1.0, col=YEL):
    if k <= 0: return
    c.drawCircle(x, y, 18 * eback(k, 2), paint(col)); c.drawCircle(x, y, 7, paint(INK))
    c.drawCircle(x, y, 18 + 26 * ((0 * 1) % 1), stroke(col, 3, 0.0))
    mono(c, lab, x + 30, y + 8, 26, PAPER, a=k)


# ================================================================== scenes
def sc_hook(c, t, S):
    tt = ph('turn around'); tj = ph('jamming their gps'); tq = ph('so what happens')
    if t < tq - 0.15:
        bg_map(c, t)
        pill(c, 540, 330, 'GPS UNDER ATTACK', 1.0, col=RED, size=40)
        mono(c, 'APRIL 2024 · ESTONIA', LX + 2, 440, 28, (180, 200, 240))
        text(c, 'JAMMED.', 70, 690, 'blk', 185, RED, track=-0.05)
        text(c, "2 jets couldn't land.", LX, 790, 'blk', 74, PAPER)
        # target airport
        pin(c, 820, 1280, 'TARTU', 1.0)
        # satellite + signal
        place(c, 'G1_sat_cut.png', 860, 980, 230, rot=-8 + 3 * math.sin(t))
        jamk = pr(t, tj - 0.6, 0.5)
        signal(c, 860, 1000, t, 1.0, jam=jamk)
        jammer(c, 300, 1430, t, pr(t, tj - 0.4, 0.4))
        # plane: approaches, then turns back
        k_turn = eio(pr(t, tt - 0.2, 1.4))
        px = lerp(340, 600, eo(pr(t, 0.0, 2.2))) - 260 * k_turn
        py = 1220 + 30 * math.sin(t * 2) + 120 * math.sin(math.pi * k_turn)
        rot = -12 + 40 * math.sin(math.pi * k_turn)
        place(c, 'G6_plane_cut.png', px, py, 520, rot=rot, flip=k_turn > 0.5)
        if t > tt:
            pill(c, 540, 1460, 'BOTH TURNED AROUND', pr(t, tt, 0.3), col=PAPER, txt=INK, size=36)
        credit(c, 'PHOTOS: MARCUSOBAL CC BY-SA 3.0 (ILLUSTRATIVE) · USAF PD', col=(150, 170, 210))
        return
    bg_red(c, t)
    kicker(c, 'THE REAL QUESTION', t, tq - 0.1, col=(255, 200, 200))
    headline(c, ['What happens', 'if GPS', 'goes down?'], LX, HY, 136, t, tq - 0.05, col=PAPER, hl=(2, ('', 'goes down?')), hl_col=INK)
    k = pr(t, tq + 0.2, 0.7)
    place(c, 'G1_sat_cut.png', 540, 1280 + 60 * (1 - eo(k)), 760, rot=-6 + 3 * math.sin(t), a=k)
    credit(c, 'ARTWORK: U.S. AIR FORCE · PUBLIC DOMAIN', col=(255, 210, 210), a=k)


def sc_what(c, t, S):
    tb = ph('banks cell towers'); tm = ph('millionth of a second')
    bg_cream(c, t)
    kicker(c, "IT'S NOT JUST MAPS", t, S['t0'] + 0.1)
    if t < tb - 0.6:
        headline(c, ['~30 satellites.', 'One weak signal.'], LX, HY, 112, t, S['t0'] + 0.3, hl=(1, ('One ', 'weak signal.')), hl_col=YEL)
        c.drawCircle(540, 1170, 330, paint(BLUE))
        place(c, 'G1_sat_cut.png', 540, 1150 + 14 * math.sin(t * 1.3), 820, rot=-6, a=pr(t, S['t0'] + 0.3, 0.5))
        pill(c, 540, 1460, 'RUN BY THE U.S. SPACE FORCE', pr(t, ph('space force') - 0.2, 0.3), col=INK, size=34)
        credit(c, 'ARTWORK: U.S. AIR FORCE · PUBLIC DOMAIN')
        return
    headline(c, ['It also tells', 'the time.'], LX, HY, 130, t, tb - 0.6, hl=(1, ('the ', 'time.')), hl_col=YEL)
    for i, (p_, s, col) in enumerate((('banks', 'BANKS', GREEN), ('cell towers', 'CELL TOWERS', BLUE), ('power grids', 'POWER GRIDS', RED))):
        pill(c, 540, 860 + i * 150, s, pr(t, ph(p_) - 0.15, 0.3), col=col, txt=INK if col == GREEN else PAPER, size=54)
    if t > tm - 0.4:
        text(c, '1/1,000,000', 540, 1400, 'blk', 120, INK, 'c', a=pr(t, tm - 0.4, 0.4))
        mono(c, 'OF A SECOND', 540, 1460, 26, GREY, 'c', a=pr(t, tm - 0.2, 0.4))


def sc_tartu(c, t, S):
    tn = ph('needed gps'); tc = ph("simply couldn't come in"); tf = ph('flew back to helsinki'); tr = ph('shut the whole route')
    bg_cream(c, t)
    kicker(c, 'CASE STUDY · TARTU, ESTONIA · APRIL 2024', t, S['t0'] + 0.1)
    if t < tf - 0.4:
        headline(c, ['No GPS.', 'No landing.'], LX, HY, 150, t, tn - 0.4, hl=(1, ('No ', 'landing.')), hl_col=RED_L)
        def after(cc):
            if t > tc - 0.2:
                kk = pr(t, tc - 0.2, 0.3)
                cc.drawRect(R.MakeWH(900, 700), paint((0, 0, 0), 0.35 * kk))
                text(cc, 'APPROACH BLOCKED', 432, 330, 'blk', 64, PAPER, 'c', a=kk)
        photo_card(c, 'G3_tartu.jpg', 540, 1120, 880, 620, -1.5, pr(t, S['t0'] + 0.3, 0.5), zoom=1.05 + 0.02 * (t - S['t0']), fx=0.6, fy=0.5, after=after)
        mono(c, "TARTU AIRPORT'S APPROACH LIGHTS", 540, 1465, 20, GREY, 'c')
        credit(c, 'PHOTO: IVO KRUUSAMÄGI · CC BY-SA 4.0')
        return
    headline(c, ['Route shut', 'for a month.'], LX, HY, 140, t, tf - 0.4, hl=(1, ('for a ', 'month.')), hl_col=YEL)
    timeline(c, 250, 830, 1000, [(0.0, 'Apr 2024', 'TURNED BACK'), (0.5, 'Apr 29', 'PAUSED'), (1.0, 'May 31', 'RESUMED')], pr(t, tf - 0.2, 2.2), t)
    if t > tr: pill(c, 540, 1300, 'FINNAIR · HELSINKI TO TARTU', pr(t, tr, 0.3), col=INK, size=34)


def sc_worse(c, t, S):
    tl = ph('pilots in lithuania'); tb = ph('bornholm'); tj = ph('one day in july'); tr = ph('blame russia')
    cover(c, img('G7_bornholm.jpg'), 0, 0, W, H, 1.7 + 0.02 * (t - S['t0']), 0.5, 0.5)
    shade(c, 0.72, NAVY)
    kicker(c, "AND IT'S GETTING WORSE", t, S['t0'] + 0.1, col=(180, 200, 240))
    if t < tb - 0.4:
        headline(c, ['~300 incidents.', 'In 2 months.'], LX, HY, 112, t, tl - 0.3, col=PAPER, hl=(0, ('', '~300')), hl_col=RED)
        def dr(cc):
            mono(cc, 'LITHUANIA · PILOT GPS-INTERFERENCE REPORTS, 2026', 44, 64, 19, GREY)
            bars(cc, 60, 110, 740, 400, [('JAN', 169, '169', RED), ('FEB', 118, '118', RED_D)], pr(t, tl, 1.2), ymax=190)
        card(c, 540, 1160, 860, 580, -1.5, pr(t, tl - 0.2, 0.5), dr)
        return
    if t < tj - 0.4:
        headline(c, ['Bornholm:', 'a new record.'], LX, HY, 120, t, tb - 0.4, col=PAPER, hl=(1, ('a new ', 'record.')), hl_col=RED)
        def dr(cc):
            mono(cc, 'JAMMING & SPOOFING, BORNHOLM STATION (DENMARK)', 44, 64, 19, GREY)
            bars(cc, 60, 110, 740, 400, [('2024', 11, '11', LIGHT), ('2025', 16, '16', INK), ('2026*', 30, '30', RED)], pr(t, tb, 1.4), ymax=34)
            mono(cc, '*SO FAR', 60, 560, 18, GREY)
        card(c, 540, 1160, 860, 600, 1.5, pr(t, tb - 0.2, 0.5), dr)
        credit(c, 'PHOTO: SOCKET0 · CC0', col=(150, 170, 210))
        return
    headline(c, ['July 29:', 'no signal.'], LX, HY, 140, t, tj - 0.4, col=PAPER, hl=(1, ('', 'no signal.')), hl_col=RED)
    def dr(cc):
        mono(cc, 'BALTIC SEA · ALL DAY', 44, 64, 20, RED)
        for i, (x, lab) in enumerate(((150, 'GDAŃSK'), (690, 'GOTLAND'))):
            cc.drawCircle(x, 200, 16, paint(INK)); mono(cc, lab, x, 250, 22, INK, 'c')
        for j in range(12):
            x = 180 + j * 42
            cc.drawLine(x, 200, x + 22, 200, stroke(RED, 6, 0.5 + 0.5 * (math.sin(t * 20 + j) > 0)))
        text(cc, 'No usable GPS', 420, 330, 'blk', 54, INK, 'c')
    card(c, 540, 1080, 840, 400, -1.5, pr(t, tj - 0.2, 0.5), dr)
    if t > tr - 0.3:
        pill(c, 540, 1400, 'EUROPEAN OFFICIALS BLAME RUSSIA', pr(t, tr - 0.3, 0.3), col=PAPER, txt=INK, size=34)
    credit(c, 'PHOTO: SOCKET0 · CC0', col=(150, 170, 210))


def sc_cost(c, t, S):
    t7 = ph('seven and a half billion'); td = ph('billion pounds a day'); te = ph('emergency services')
    bg_cream(c, t)
    kicker(c, 'A FULL OUTAGE · UK GOVERNMENT STUDY', t, S['t0'] + 0.1)
    if t < te - 0.6:
        headline(c, ['One week', 'without GPS:'], LX, HY, 130, t, S['t0'] + 0.2)
        n = 7.6 * eo(pr(t, t7 - 0.2, 1.2))
        text(c, '£%.1fbn' % n, 540, 1130, 'blk', 230, RED, 'c', track=-0.04, a=pr(t, t7 - 0.2, 0.3))
        if t > td - 0.3:
            pill(c, 540, 1300, 'OVER £1 BILLION A DAY', pr(t, td - 0.3, 0.3), col=INK, size=44)
        return
    headline(c, ['Biggest hit:', 'emergency services.'], LX, HY, 108, t, te - 0.6, hl=(1, ('', 'emergency services.')), hl_col=YEL)
    def dr(cc):
        mono(cc, 'WHERE THE £7.6BN LOSS HITS (7 DAYS)', 44, 64, 20, GREY)
        bars(cc, 60, 110, 740, 400, [('EMERGENCY', 3.5, '£3.5bn', RED), ('ROAD', 1.7, '£1.7bn', INK), ('SHIPPING', 1.5, '£1.5bn', BLUE)], pr(t, te, 1.3), ymax=3.9)
    card(c, 540, 1160, 860, 600, -1.5, pr(t, te - 0.3, 0.5), dr)


def sc_backup(c, t, S):
    tp = ph('planes have older'); ts = ph('ships have radar'); te = ph('eloran'); ty = ph('your phone your car')
    cover(c, img('G4_cockpit.jpg'), 0, 0, W, H, 1.75 + 0.02 * (t - S['t0']), 0.5, 0.45)
    shade(c, 0.66, (6, 10, 24))
    kicker(c, 'IS THERE A BACKUP?', t, S['t0'] + 0.1, col=(200, 210, 240))
    headline(c, ['Kind of.'], LX, HY, 160, t, S['t0'] + 0.3, col=PAPER, hl=(0, ('Kind ', 'of.')), hl_col=YEL)
    rows = ((tp, 'PLANES', 'Old radio beacons', True), (ts, 'SHIPS', 'Radar & compasses', True), (ty, 'YOUR PHONE & CAR', 'Nothing else', False))
    for i, (t0, a, b, ok) in enumerate(rows):
        def dr(cc, a=a, b=b, ok=ok):
            mono(cc, a, 40, 60, 22, GREEN if ok else RED)
            text(cc, b, 40, 140, 'blk', 56, INK)
            if ok:
                cc.drawPath(poly([(700, 100), (725, 130), (775, 70)], False), stroke(GREEN, 12))
            else:
                cc.drawLine(705, 75, 765, 135, stroke(RED, 12)); cc.drawLine(765, 75, 705, 135, stroke(RED, 12))
        card(c, 540, 820 + i * 220, 820, 190, (-2, 1.5, -1)[i], pr(t, t0 - 0.2, 0.4), dr, rad=20)
    if t > te - 0.3 and t < ty - 0.2:
        pill(c, 540, 1470, 'BACKUP IDEA: eLORAN (GROUND RADIO)', pr(t, te - 0.3, 0.3), col=YEL, txt=INK, size=30)
    credit(c, 'PHOTO: WILFREDOR · CC0', col=(170, 180, 210))


def sc_predict(c, t, S):
    tj = ph('jamming becomes normal'); tc = ph('more cancelled flights'); tn = ph('the next big business')
    cover(c, img('G2_launch.jpg'), 0, 0, W, H, 1.9 + 0.02 * (t - S['t0']), 0.5, 0.5)
    shade(c, 0.55, (10, 6, 20))
    kicker(c, 'NEXTBIGNOW PREDICTION', t, S['t0'] + 0.1, col=(255, 200, 200))
    if t < tn - 0.4:
        headline(c, ["GPS doesn't", 'switch off.'], LX, HY, 132, t, S['t0'] + 0.2, col=PAPER, hl=(1, ('', 'switch off.')), hl_col=RED)
        for i, (t0, s) in enumerate(((tj, 'JAMMING BECOMES NORMAL'), (tc, 'MORE CANCELLED FLIGHTS'), (ph('wrong place'), 'SHIPS IN THE WRONG PLACE'))):
            pill(c, 540, 1000 + i * 140, s, pr(t, t0 - 0.2, 0.3), col=(RED, PAPER, PAPER)[i], txt=(PAPER, INK, INK)[i], size=42)
    else:
        headline(c, ['Next big business:', 'navigation', 'without space.'], LX, HY, 108, t, tn - 0.4, col=PAPER, hl=(2, ('without ', 'space.')), hl_col=GREEN)
    credit(c, 'PHOTO: U.S. SPACE FORCE (G. KURZEN) · PUBLIC DOMAIN', col=(200, 190, 210))


def sc_ask(c, t, S):
    bg_cream(c, t)
    kicker(c, 'YOUR TURN', t, S['t0'] + 0.1)
    headline(c, ['Could you get home', 'without GPS?'], LX, HY, 108, t, S['t0'] + 0.1, hl=(1, ('without ', 'GPS?')), hl_col=YEL)
    k = pr(t, S['t0'] + 0.3, 0.6)
    c.drawCircle(540, 1060, 260, paint(BLUE))
    place(c, 'G6_plane_cut.png', 540 + 40 * math.sin(t), 1060, 620, rot=-10, a=k)
    pill(c, 330, 1400, 'YES', pr(t, ph('yes or no') - 0.1, 0.3), col=GREEN, txt=INK, size=70)
    pill(c, 750, 1400, 'NO', pr(t, ph('yes or no') + 0.2, 0.3), col=RED, txt=PAPER, size=70)
    credit(c, 'PHOTO: MARCUSOBAL · CC BY-SA 3.0', a=k)
    if t > END:
        kk = pr(t, END, 0.9)
        c.drawCircle(540, 1000, 1400 * eio(kk), paint(RED_D))


SCENES = [
    dict(k='hook', t0=0.0, fn=sc_hook),
    dict(k='what', t0=ph("here's the thing") - 0.2, fn=sc_what, tin='whip'),
    dict(k='tartu', t0=ph('back to estonia') - 0.2, fn=sc_tartu, tin='zoom'),
    dict(k='worse', t0=ph("and it's getting worse") - 0.2, fn=sc_worse, tin='wipe', col=NAVY),
    dict(k='cost', t0=ph('now imagine a full') - 0.2, fn=sc_cost, tin='whip'),
    dict(k='backup', t0=ph('so is there a backup') - 0.2, fn=sc_backup, tin='zoom'),
    dict(k='predict', t0=ph("so here's my prediction") - 0.2, fn=sc_predict, tin='flash'),
    dict(k='ask', t0=ph('and tell me') - 0.2, fn=sc_ask, tin='zoom'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('jamming their gps'), 10, 0.3)
EP.shk(ph("simply couldn't come in"), 8, 0.3)
EP.shk(ph('seven and a half billion'), 8, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
