"""NextBigNow long-form L02 (16:9, red/cream comic, real photo cut-outs, small subtitles, v5 voice, logo watermark):
Measles is back in America - how we lost a 26-year win.
Facts: PAHO revoked US elimination (review Nov 10-13, 2026). CDC: 5,412 cases 2026 (as of Nov 12), PA 1,500+ (Lancaster County), 10 deaths;
2,289 in 2025 (most since 1992); 285 in 2024. Texas 2025 (Gaines County, from Jan 2025): 762 cases, 2 school-age children died (first US measles
deaths since 2015), 1 adult in New Mexico. Utah/Arizona and South Carolina outbreaks followed. Pre-vaccine (CDC): 3-4 million infected/yr,
~48,000 hospitalized, 400-500 deaths. Vaccine licensed 1963; 2-dose recommendation 1989; eliminated 2000. R0 12-18; airborne up to 2 hours;
up to 9 in 10 unprotected close contacts infected; ~95% immunity threshold; 2 MMR doses ~97% effective. Kindergarten 2-dose MMR: 95.2% (2019-20),
92.4% (2025-26); Idaho ~75%, West Virginia ~99%; 10 states >=95% (KFF/CDC). Canada lost status Nov 2025. NYC 2019: ~60,000 MMR doses, outbreak
declared over Sept 2019 (no new cases after mid-July / chain broken by August). Photos: Wikimedia Commons, see mlong/img/credits.json."""
import sys, os, math, re, json
import skia
from toon import W, H, R, paint, stroke, lin, argb, poly, hsh, eo, eio, eback, pr, cl, lerp
from edkit import text, mono, PAPER, INK, GREY
import photokit as PK
from photokit import img, cover, place
from comickit import *
from engine import Episode, load_words, HERE

D = os.path.join(HERE, os.environ.get('ML_DIR', 'mlong'))
PK.IMG = os.path.join(HERE, 'mlong', 'img')
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
TX = 110
SEPIA = (240, 222, 186)
GRN = (80, 200, 120)
MONO = 'SpecialElite.ttf'


def credit(c, key, a=1.0, col=(120, 100, 70), y=900):
    cr = CRED_J.get(key)
    if not cr: return
    s = ('PHOTO: %s . %s' % (cr['author'], cr['license'])).upper()[:70]
    c.save(); c.translate(70, y); c.rotate(-90); mono(c, s, 0, 0, 17, col, a=a * 0.9); c.restore()


def photo_panel(c, key, x, y, w, h, rot, k, zoom=1.05, fx=0.5, fy=0.5, t=0.0):
    def dr(cc): cover(cc, img(key + '_comic.png'), 0, 0, w, h, zoom + 0.01 * t, fx, fy)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr)


def mini(c, x, y, w, h, rot, k, head, big, col, txtc=PAPER, bigsize=54):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(col)); dots(cc, (0, 0, w, h), KINK, cell=16, rmax=3.2, grad=(0.3, 1.0), a=0.25)
        cc.drawString(head, 22, 44, font(MONO, 26), paint(PAPER if col in (CRED, CBLU, KINK) else KINK))
        title(cc, big, 22, h - 36, bigsize, txtc, 1.0, shadow=4)
    panel(c, x, y, w, h, rot=rot, k=k, draw=dr, border=7, shadow=10)


def head2(c, a, b, t, t0, ca=CBLU, cb=CRED, size=120, y=300):
    title(c, a, TX, y, size, ca, pr(t, t0, 0.4))
    title(c, b, TX, y + size + 20, size, cb, pr(t, t0 + 0.3, 0.4), rot=-1.5)


def row_card(c, x, y, w, h, k, left, right, col, lsize=44, rsize=64):
    def dr(cc):
        cc.drawRect(R.MakeWH(w, h), paint(PAPER))
        cc.drawRect(R.MakeXYWH(0, 0, 18, h), paint(col))
        title(cc, left, 44, h / 2 + lsize * 0.36, lsize, KINK, 1.0, shadow=0, outline=0.01)
        title(cc, right, w - 30, h / 2 + rsize * 0.36, rsize, col, 1.0, 'r', shadow=4)
    panel(c, x, y, w, h, rot=0, k=k, draw=dr, border=6, shadow=8)


def virus(c, x, y, w, t, k=1.0, rot0=0.0):
    if k <= 0: return
    place(c, 'V1_cut_comic.png', x, y, w * eback(cl(k), 1.5), rot=rot0 + 6 * math.sin(t * 1.3), a=cl(k * 2), shadow=True)


def stamp(c, s, x, y, size, col, k, rot=-8, fill=None):
    if k <= 0: return
    sc = 1.0 + 0.6 * (1 - eo(cl(k)))
    tw_ = width(s, MONO, size)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    a = cl(k * 2)
    r_ = R.MakeXYWH(-tw_ / 2 - 34, -size * 0.95, tw_ + 68, size * 1.45)
    if fill: c.drawRect(r_, paint(fill, a))
    c.drawRect(r_, stroke(col, 9, a=a))
    c.drawString(s, -tw_ / 2, size * 0.18, font(MONO, size), paint(col, a))
    c.restore()


def people(c, x, y, n_sick, k, t0_list=None, t=0.0, cols=5, sz=70):
    """10 simple person icons; the first n_sick turn red."""
    for i in range(10):
        cx = x + (i % cols) * sz * 1.25; cy = y + (i // cols) * sz * 1.7
        sick = i < n_sick and k > 0.2 + 0.07 * i
        col = CRED if sick else CBLU
        c.drawCircle(cx + 4, cy + 4, sz * 0.28, paint(KINK)); c.drawCircle(cx, cy, sz * 0.28, paint(col)); c.drawCircle(cx, cy, sz * 0.28, stroke(KINK, 5))
        rr = skia.RRect.MakeRectXY(R.MakeXYWH(cx - sz * 0.42, cy + sz * 0.34, sz * 0.84, sz * 0.7), sz * 0.3, sz * 0.3)
        c.drawRRect(rr, paint(col)); c.drawRRect(rr, stroke(KINK, 5))


def line_chart(cc, w, h, k, pts, ymin, ymax, col=CRED, labels=(), target=None):
    x0, y0, cw, ch = 70, 50, w - 130, h - 140
    yv = lambda v: y0 + ch - (v - ymin) / (ymax - ymin) * ch
    cc.drawLine(x0, y0 + ch, x0 + cw, y0 + ch, stroke(KINK, 5)); cc.drawLine(x0, y0, x0, y0 + ch, stroke(KINK, 5))
    if target is not None:
        p = stroke(GRN, 6); p.setPathEffect(skia.DashPathEffect.Make([20, 12], 0))
        cc.drawLine(x0, yv(target), x0 + cw, yv(target), p)
        cc.drawString('%g%% TARGET' % target, x0 + cw - 210, yv(target) - 14, font(MONO, 24), paint((40, 140, 70)))
    p = skia.Path(); first = True
    for fx, v in pts:
        if fx > k + 1e-6: break
        (p.moveTo if first else p.lineTo)(x0 + fx * cw, yv(v)); first = False
    cc.drawPath(p, stroke(KINK, 16)); cc.drawPath(p, stroke(col, 9))
    for fx, s in labels:
        cc.drawString(s, x0 + fx * cw - 40, y0 + ch + 44, font(MONO, 24), paint(KINK))


def timeline(c, x, y, w, items, t):
    """items: (t_on, year, label, col)"""
    c.drawLine(x, y, x + w, y, stroke(KINK, 10))
    n = len(items)
    for i, (t0, yr, lab, col) in enumerate(items):
        k = pr(t, t0 - 0.2, 0.35)
        if k <= 0: continue
        X = x + w * (i + 0.5) / n
        c.drawCircle(X, y, 26 * eback(k, 1.6), paint(col)); c.drawCircle(X, y, 26 * eback(k, 1.6), stroke(KINK, 6))
        title(c, yr, X, y - 50, 64, col, k, 'c', shadow=4)
        s_ = lab
        c.drawString(s_, X - width(s_, MONO, 26) / 2, y + 74, font(MONO, 26), paint(KINK, k))


def sc_hook(c, t, S):
    tk = ph('a few kids in west texas'); tf = ph('fever cough'); t22 = ph('twenty two months later'); t26 = ph('twenty six years')
    tw = ph('this week the pan american'); tn = ph('no longer eliminated'); th = ph('so how did a disease'); tm = ph('what does it actually mean')
    if t < tw - 0.2:
        paper(c, t, tint=SEPIA)
        caption(c, 'JANUARY 2025 . WEST TEXAS', TX, 120, 1.0, col=CYEL, size=30)
        photo_panel(c, 'L1_texas', TX, 200, 860, 450, -1.5, pr(t, 0.0, 0.45), t=t)
        credit(c, 'L1_texas')
        caption(c, 'GAINES COUNTY COURTHOUSE, SEMINOLE', TX + 30, 690, pr(t, 0.6, 0.3), size=24, rot=1)
        virus(c, 1420, 520, 640, t, pr(t, 0.4, 0.5), rot0=-8)
        if t > tf: caption(c, 'FEVER. COUGH. RASH.', 1180, 900, pr(t, tf, 0.3), col=CRED, size=34, rot=-2)
        if t > t22 - 0.2: title(c, '22 MONTHS LATER...', TX, 830, 80, CBLU, pr(t, t22 - 0.2, 0.4), rot=-1.5)
        if t > t26 - 0.3: burst(c, 1700, 230, 130, '26 YEARS', pr(t, t26 - 0.3, 0.35), size=44, rot=8)
        return
    bg_flat(c, CRED, (190, 20, 30))
    caption(c, 'NOVEMBER 2026', TX, 120, pr(t, tw - 0.2, 0.3), col=PAPER, size=30)
    head2(c, 'MEASLES IS', 'BACK.', t, tw, ca=PAPER, cb=CYEL, size=150, y=330)
    photo_panel(c, 'L5_paho', 1000, 170, 800, 400, 1.5, pr(t, tw + 0.3, 0.5), t=t - tw)
    credit(c, 'L5_paho', col=PAPER)
    caption(c, 'PAN AMERICAN HEALTH ORGANIZATION', 1040, 610, pr(t, tw + 0.8, 0.3), col=CYEL, size=26, rot=-1)
    stamp(c, 'ELIMINATION: REVOKED', 1400, 760, 46, PAPER, pr(t, tn - 0.3, 0.35), rot=-5, fill=(150, 15, 25))
    for i, (t0, s_) in enumerate(((th, '1. HOW DID IT COME BACK?'), (tm, '2. WHAT DOES IT MEAN FOR YOU?'))):
        caption(c, s_, TX + 10, 700 + i * 75, pr(t, t0 - 0.2, 0.3), col=(CYEL, PAPER)[i], size=32, rot=(-1.5, 1)[i])


def sc_before(c, t, S):
    t63 = ph('nineteen sixty three'); te = ph('almost every american kid'); t34 = ph('three to four million'); t48 = ph('forty eight thousand'); t45 = ph('four to five hundred'); tev = ph('every single year')
    paper(c, t, tint=SEPIA)
    caption(c, 'BEFORE THE VACCINE', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    head2(c, 'ALMOST EVERY', 'KID GOT IT.', t, te - 0.3, size=96)
    if t > t63 - 0.3: burst(c, 700, 560, 110, 'PRE-1963', pr(t, t63 - 0.3, 0.35), size=40, rot=8)
    cards = ((t34, 'CASES PER YEAR', '3-4 MILLION', CBLU), (t48, 'HOSPITALIZED', '48,000', CRED), (t45, 'DEATHS', '400-500', KINK))
    for i, (t0, hd, big, col) in enumerate(cards):
        mini(c, 1040 + (i % 2) * 20, 170 + i * 240, 760, 210, (-1.5, 1.5, -1)[i], pr(t, t0 - 0.3, 0.4), hd, big, col, bigsize=100)
    if t > tev - 0.2: title(c, 'EVERY. SINGLE. YEAR.', TX, 720, 70, CRED, pr(t, tev - 0.2, 0.4), rot=-1.5)
    caption(c, 'SOURCE: CDC', TX, 800, pr(t, t34, 0.3), size=22)


def sc_elim(c, t, S):
    ts = ph('then the shots came'); t89 = ph('nineteen eighty nine'); t2d = ph('two doses'); t2k = ph('in the year two thousand'); tz = ph('that never meant zero'); tt = ph('travelers still brought'); tc = ph('no chain of spread lasted')
    paper(c, t)
    caption(c, 'HOW AMERICA WON', TX, 120, pr(t, S['t0'], 0.3), col=GRN if False else CBLU, size=30)
    title(c, 'THE SHOTS CAME.', TX, 280, 110, CBLU, pr(t, ts, 0.4))
    timeline(c, 200, 520, 1520, [(ts + 0.3, '1963', 'FIRST VACCINE', CBLU), (t89, '1989', 'SECOND DOSE ADDED', CCYN), (t2k, '2000', 'ELIMINATED!', GRN)], t)
    place(c, 'V6_cut_comic.png', 1450, 250, 300 * eback(cl(pr(t, ts + 0.2, 0.5)), 1.4), rot=-6, a=pr(t, ts + 0.2, 0.5), shadow=True)
    if t > tz - 0.3:
        def dr(cc):
            cc.drawRect(R.MakeWH(1100, 190), paint(CYEL))
            title(cc, 'ELIMINATED =', 30, 80, 54, CRED, 1.0, shadow=3)
            cc.drawString('NOT ZERO CASES. NO CHAIN OF SPREAD LASTING 12 MONTHS.', 30, 150, font(MONO, 30), paint(KINK))
        panel(c, 410, 690, 1100, 190, rot=-1.5, k=pr(t, tz - 0.3, 0.5), draw=dr)
    if t > tt - 0.2: burst(c, 1640, 760, 100, 'TRAVELERS', pr(t, tt - 0.2, 0.35), size=34, col=CBLU, txt=PAPER, rot=8)


def sc_contagious(c, t, S):
    tm = ph('most contagious'); t12 = ph('twelve to eighteen'); t2 = ph('up to two hours'); t9 = ph('nine out of ten'); tw = ph('so the only real wall'); t95 = ph('ninety five percent of a community'); t97 = ph('ninety seven percent effective')
    paper(c, t)
    caption(c, 'WHY IS IT SO HARD TO STOP?', TX, 120, pr(t, S['t0'], 0.3), col=CCYN, size=30)
    if t < tw - 0.3:
        head2(c, 'THE MOST', 'CONTAGIOUS.', t, tm - 0.4, size=120)
        if t > t12 - 0.3:
            mini(c, TX, 580, 380, 200, -1.5, pr(t, t12 - 0.3, 0.4), '1 SICK PERSON', '-> 12-18', CRED, bigsize=80)
        if t > t2 - 0.3:
            mini(c, TX + 420, 580, 380, 200, 1.5, pr(t, t2 - 0.3, 0.4), 'HANGS IN THE AIR', '2 HOURS', CBLU, bigsize=90)
        photo_panel(c, 'V2_room', 1000, 160, 820, 440, 1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        credit(c, 'V2_room')
        kk = pr(t, t2 - 0.3, 1.2)
        for i in range(10):
            if kk <= 0: break
            px = 1060 + (i * 97) % 720 + 25 * math.sin(t * 1.1 + i); py = 220 + (i * 61) % 340 + 18 * math.cos(t * 0.9 + i * 2)
            place(c, 'V1_cut_comic.png', px, py, 64 * kk, rot=t * 30 + i * 40, a=kk * 0.95, shadow=False)
        if t > t9 - 0.4:
            people(c, 1120, 690, 9, pr(t, t9 - 0.4, 1.5), sz=62, cols=10)
            caption(c, 'UP TO 9 IN 10 UNPROTECTED PEOPLE CATCH IT', 1080, 920 - 20, pr(t, t9, 0.3), col=CYEL, size=24, rot=-1)
        return
    head2(c, 'THE ONLY WALL:', 'IMMUNITY.', t, tw - 0.2, ca=CBLU, cb=GRN, size=120)
    mini(c, 1040, 190, 760, 260, -1.5, pr(t, t95 - 0.3, 0.4), 'IMMUNE TO STOP SPREAD', '~95%', CBLU, bigsize=150)
    mini(c, 1060, 500, 740, 260, 1.5, pr(t, t97 - 0.3, 0.4), '2 DOSES OF MMR WORK', '~97%', GRN, bigsize=150)
    people(c, TX + 20, 640, 0, 1.0, sz=60, cols=10)


def sc_cracks(c, t, S):
    tc = ph('had been cracking'); t952 = ph('ninety five point two'); t924 = ph('ninety two point four'); ta = ph("that's an average"); ti = ph('idaho'); twv = ph('west virginia'); t10 = ph('only ten states'); tp = ph('find the pockets')
    paper(c, t)
    caption(c, 'KINDERGARTEN, BOTH MMR DOSES', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    head2(c, 'THE WALL', 'CRACKED.', t, tc - 0.3, size=130)
    if t < ta - 0.3:
        def dr(cc):
            cc.drawRect(R.MakeWH(820, 560), paint(PAPER))
            k = pr(t, t952 - 0.3, (t924 - t952) + 0.6)
            pts = [(0.0, 95.2), (0.2, 94.9), (0.4, 93.9), (0.6, 93.1), (0.8, 92.7), (1.0, 92.4)]
            line_chart(cc, 820, 560, k, pts, 90, 97, labels=((0.0, '2019'), (0.5, '2022'), (1.0, '2025')), target=95)
        panel(c, 1000, 160, 820, 560, rot=1.2, k=pr(t, tc, 0.5), draw=dr)
        if t > t952 - 0.2: row_card(c, TX, 620, 700, 100, pr(t, t952 - 0.2, 0.35), '2019-20', '95.2%', GRN, lsize=40, rsize=60)
        if t > t924 - 0.2: row_card(c, TX, 740, 700, 100, pr(t, t924 - 0.2, 0.35), '2025-26', '92.4%', CRED, lsize=40, rsize=60)
        return
    if t > ti - 0.3: row_card(c, 1000, 200, 800, 120, pr(t, ti - 0.3, 0.35), 'IDAHO', '~75%', CRED, rsize=72)
    if t > twv - 0.3: row_card(c, 1000, 350, 800, 120, pr(t, twv - 0.3, 0.35), 'WEST VIRGINIA', '~99%', GRN, rsize=72)
    if t > t10 - 0.3: row_card(c, 1000, 500, 800, 120, pr(t, t10 - 0.3, 0.35), 'STATES AT 95%+', 'ONLY 10', CBLU, rsize=72)
    photo_panel(c, 'V3_class', TX, 600, 560, 300, -1.5, pr(t, ta - 0.3, 0.5), t=t - ta)
    credit(c, 'V3_class')
    if t > ta - 0.3: caption(c, 'AN AVERAGE HIDES THE GAPS', TX + 600, 680, pr(t, ta - 0.3, 0.3), col=CYEL, size=28, rot=-2)
    if t > tp - 0.3: burst(c, 1500, 760, 130, 'IT FINDS THE POCKETS', pr(t, tp - 0.3, 0.35), size=26, col=CRED, txt=CYEL, rot=-5)


def sc_chain(c, t, S):
    tg = ph('gaines county texas'); t7 = ph('more than seven hundred'); td = ph('two school age children died'); tdec = ph('first us measles deaths'); tnm = ph('an adult in new mexico')
    tk = ph('then it kept moving'); tu = ph('utah and arizona'); ts = ph('then south carolina'); t2289 = ph('two thousand two hundred eighty nine'); t30 = ph('most in over thirty years')
    paper(c, t)
    caption(c, 'THE CHAIN, 2025', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tk - 0.3:
        head2(c, 'TEXAS:', '700+ CASES', t, tg - 0.3, size=130)
        photo_panel(c, 'L1_texas', 1000, 160, 820, 430, 1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        credit(c, 'L1_texas')
        if t > td - 0.3: mini(c, TX, 620, 520, 230, -1.5, pr(t, td - 0.3, 0.4), 'CHILDREN DIED', '2', CRED, bigsize=130)
        if t > tdec - 0.2: caption(c, 'FIRST US MEASLES DEATHS SINCE 2015', 690, 700, pr(t, tdec - 0.2, 0.3), col=CYEL, size=26, rot=1.5)
        if t > tnm - 0.3: mini(c, 1060, 640, 700, 200, 1.5, pr(t, tnm - 0.3, 0.4), 'NEW MEXICO', '+1 ADULT', KINK, bigsize=80)
        return
    title(c, 'THEN IT KEPT', TX, 290, 110, CBLU, pr(t, tk - 0.3, 0.4))
    title(c, 'MOVING.', TX, 410, 110, CRED, pr(t, tk, 0.4), rot=-1.5)
    stops = ((tg, 'TEXAS', 'L1_texas'), (tu, 'UTAH / ARIZONA', 'L6_utah'), (ts, 'SOUTH CAROLINA', 'L7_sc'))
    for i, (t0, lab, key) in enumerate(stops):
        X = 160 + i * 590
        k = pr(t, max(t0, tk) - 0.2 if i == 0 else t0 - 0.3, 0.45)
        photo_panel(c, key, X, 500, 480, 280, (-2, 1.5, -1)[i], k, t=t - tk)
        if k > 0: caption(c, lab, X + 30, 820, k, col=(CRED, CBLU, CRED)[i], size=28)
        if i and k > 0:
            p = stroke(KINK, 10); p.setPathEffect(skia.DashPathEffect.Make([24, 14], 0))
            c.drawLine(X - 110, 640, lerp(X - 110, X - 20, eo(k)), 640, p)
    if i: credit(c, 'L7_sc')
    if t > t2289 - 0.3:
        mini(c, 1060, 170, 740, 260, 2, pr(t, t2289 - 0.3, 0.4), 'US CASES IN 2025', '2,289', CRED, bigsize=140)
    if t > t30 - 0.2: burst(c, 1700, 420, 120, 'MOST SINCE 1992', pr(t, t30 - 0.2, 0.35), size=30, rot=8)


def sc_2026(c, t, S):
    tl = ph('lancaster county'); t15 = ph('more than fifteen hundred'); tn = ph('as of november twelfth'); t5 = ph('five thousand four hundred twelve'); t10 = ph('and ten deaths'); tb = ph('too young for the shot')
    paper(c, t)
    caption(c, '2026 GOT WORSE', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < tn - 0.3:
        head2(c, 'PENNSYLVANIA:', '1,500+ CASES', t, tl - 0.4, size=110)
        photo_panel(c, 'L2_lancaster', 1000, 160, 820, 420, 1.5, pr(t, S['t0'] + 0.3, 0.5), t=t - S['t0'])
        credit(c, 'L2_lancaster')
        caption(c, 'LANCASTER COUNTY, FROM ABOVE', 1040, 620, pr(t, tl, 0.3), col=CYEL, size=26, rot=-1)
        photo_panel(c, 'V7_philly', TX, 620, 700, 260, -1.5, pr(t, t15, 0.5), t=t - t15)
        if t > t15: caption(c, 'BIGGEST US OUTBREAK IN DECADES', 900, 760, pr(t, t15 + 0.3, 0.3), col=PAPER, size=28, rot=1.5)
        return
    title(c, 'US CASES', TX, 290, 110, CBLU, pr(t, tn - 0.3, 0.4))
    def dr(cc):
        cc.drawRect(R.MakeWH(820, 600), paint(PAPER))
        k = pr(t, tn, 0.6) * 0.67 + 0.33 * pr(t, t5 - 0.2, 0.8)
        bars(cc, 90, 110, 660, 360, [('2024', 285, '285', CCYN), ('2025', 2289, '2,289', CYEL), ('2026', 5412, '5,412', CRED)], k, 5800)
        cc.drawString('CONFIRMED CASES . CDC (2026 AS OF NOV 12)', 30, 580, font(MONO, 22), paint(KINK))
    panel(c, 1000, 150, 820, 600, rot=1.0, k=pr(t, tn - 0.2, 0.5), draw=dr)
    if t > t10 - 0.3: mini(c, TX, 470, 560, 230, -1.5, pr(t, t10 - 0.3, 0.4), 'DEATHS IN 2026', '10', CRED, bigsize=140)
    if t > tb - 0.3: caption(c, 'SEVERAL WERE BABIES TOO YOUNG FOR THE SHOT', TX, 780, pr(t, tb - 0.3, 0.3), col=CYEL, size=30, rot=-1)


def sc_verdict(c, t, S):
    tr = ph('the rule is twelve months'); tw = ph('put the us on watch'); tca = ph('canada lost its status'); t4 = ph('four day review'); tl = ph('the us lost it too')
    bg_flat(c, CBLU, (25, 90, 180))
    caption(c, 'THE VERDICT', TX, 120, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    title(c, 'ONE CHAIN.', TX, 300, 130, PAPER, pr(t, tr - 0.2, 0.4))
    title(c, '12 MONTHS.', TX, 440, 130, CYEL, pr(t, tr + 0.4, 0.4), rot=-1.5)
    gap = 1700 / 12
    for i in range(12):
        kk = pr(t, tr + 0.4 + 0.12 * i, 0.25)
        cx = 110 + gap * (i + 0.5); r = gap * 0.38
        rr = skia.RRect.MakeRectXY(R.MakeXYWH(cx - r, 560 - r * 0.6, 2 * r, 1.2 * r), r * 0.6, r * 0.6)
        c.drawRRect(rr, stroke(KINK, 14))
        if kk > 0: c.drawRRect(rr, stroke(CYEL, 8 * kk))
    row_card(c, TX, 690, 760, 100, pr(t, tw - 0.3, 0.35), 'LATE 2025', 'US ON WATCH', CCYN, lsize=36, rsize=50)
    row_card(c, TX + 800, 690, 760, 100, pr(t, tca - 0.3, 0.35), 'NOV 2025', 'CANADA: LOST', CRED, lsize=36, rsize=50)
    if t > t4 - 0.3: stamp(c, 'NOV 2026: U.S. LOST IT', 1350, 330, 54, PAPER, pr(t, tl - 0.3, 0.35), rot=-6, fill=(190, 20, 30))
    if t > t4 - 0.3 and t < tl - 0.3: caption(c, 'A 4-DAY REVIEW...', 1250, 330, pr(t, t4 - 0.3, 0.3), col=PAPER, size=34)


def sc_means(c, t, S):
    tn = ph('nothing flips overnight'); tf = ph('no fine'); tb = ph('no travel ban'); tl = ph("it's a label"); to = ph('spreads here on its own')
    tmo = ph('more outbreaks'); ts = ph('school and daycare closures'); th = ph('strain on hospitals'); tr = ph('most at risk are babies'); tp = ph('pregnant women'); tw = ph('weak immune systems')
    paper(c, t)
    caption(c, 'WHAT IT MEANS FOR YOU', TX, 120, pr(t, S['t0'], 0.3), col=CRED, size=30)
    if t < to - 0.3:
        head2(c, 'NOTHING FLIPS', 'OVERNIGHT.', t, tn - 0.3, size=120)
        for i, (t0, s_) in enumerate(((tf, 'NO FINE'), (tb, 'NO TRAVEL BAN'))):
            k = pr(t, t0 - 0.2, 0.35)
            if k > 0: stamp(c, s_, 1300 + (i * 140), 300 + i * 220, 60, CBLU, k, rot=(-6, 4)[i])
        if t > tl - 0.3: burst(c, 1450, 760, 150, "IT'S A LABEL", pr(t, tl - 0.3, 0.35), size=30, rot=6)
        return
    if t < tr - 0.4:
        head2(c, 'IT SPREADS', 'HERE NOW.', t, to - 0.3, size=120)
        photo_panel(c, 'L3_hosp', 1000, 150, 420, 620, -1.5, pr(t, th - 0.4, 0.5), t=t - th)
        if t > th - 0.4: credit(c, 'L3_hosp')
        for i, (t0, s_, col) in enumerate(((tmo, 'MORE OUTBREAKS', CRED), (ts, 'SCHOOL & DAYCARE CLOSURES', CBLU), (th, 'STRAIN ON HOSPITALS', KINK))):
            row_card(c, TX, 600 + i * 110 if False else 590 + i * 105, 800, 90, pr(t, t0 - 0.3, 0.35), s_, '', col, lsize=40, rsize=10)
        return
    head2(c, 'MOST AT', 'RISK:', t, tr - 0.4, ca=CBLU, cb=CRED, size=130)
    for i, (t0, hd, big, col) in enumerate(((tr, 'TOO YOUNG FOR THE SHOT', 'BABIES <1', CRED), (tp, 'CAN\'T GET MMR WHILE PREGNANT', 'PREGNANT', CBLU), (tw, 'CANCER CARE, TRANSPLANTS...', 'WEAK IMMUNITY', KINK))):
        mini(c, 1000 + (i % 2) * 30, 160 + i * 240, 800, 210, (-1.5, 1.5, -1)[i], pr(t, t0 - 0.3, 0.4), hd, big, col, bigsize=84)


def sc_comeback(c, t, S):
    tn = ph('new york city faced'); t60 = ph('sixty thousand'); ta = ph('broken by august'); tb = ph('break every chain'); ty = ph('at least a year')
    bg_flat(c, CBLU, (25, 90, 180))
    caption(c, 'CAN AMERICA WIN IT BACK?', TX, 120, pr(t, S['t0'], 0.3), col=CYEL, size=30)
    title(c, 'YES. IT\'S BEEN DONE.', TX, 280, 76, PAPER, pr(t, S['t0'] + 0.6, 0.4))
    photo_panel(c, 'V4_brooklyn', 1000, 170, 820, 400, 1.5, pr(t, tn - 0.3, 0.5), fy=0.55, t=t - tn)
    credit(c, 'V4_brooklyn', col=PAPER)
    caption(c, 'NEW YORK CITY, 2019', 1040, 610, pr(t, tn, 0.3), col=CYEL, size=28, rot=-1)
    if t > t60 - 0.4:
        title(c, '60,000', TX, 500, 150, CYEL, pr(t, t60 - 0.4, 0.4), rot=-2)
        caption(c, 'MMR DOSES IN A FEW MONTHS', TX + 10, 580, pr(t, t60 + 0.2, 0.3), col=PAPER, size=30, rot=1.5)
        for i in range(3):
            kk = pr(t, t60 + 0.15 * i, 0.4)
            if kk > 0: place(c, 'V6_cut_comic.png', 800 + 40 * i, 470 - 50 * i, 160 * eback(cl(kk), 1.5), rot=-5 + 10 * i, a=kk, shadow=True)
    if t > ta - 0.3: burst(c, 1700, 640, 120, 'CHAIN BROKEN', pr(t, ta - 0.3, 0.35), size=32, col=GRN, txt=PAPER, rot=-6)
    if t > tb - 0.3:
        def dr(cc):
            cc.drawRect(R.MakeWH(1100, 150), paint(CYEL))
            title(cc, 'TO WIN IT BACK: 12 MONTHS, NO CHAIN', 550, 98, 54, CRED, 1.0, 'c', shadow=3)
        panel(c, TX, 700, 1100, 150, rot=-1.5, k=pr(t, tb - 0.3, 0.5), draw=dr)


def sc_end(c, t, S):
    tn = ph("we didn't lose to a new virus"); to = ph('an old one'); t12 = ph('next twelve months'); tq = ph('by twenty twenty eight'); tc = ph('tell me in the comments')
    if t < tq - 1.5:
        bg_flat(c, CRED, (190, 20, 30))
        caption(c, 'THE HONEST PICTURE', TX, 120, pr(t, S['t0'], 0.3), col=PAPER, size=30)
        title(c, 'NOT A NEW VIRUS.', TX, 330, 110, PAPER, pr(t, tn - 0.2, 0.4))
        title(c, 'AN OLD ONE WE', TX, 470, 110, CYEL, pr(t, to - 0.2, 0.4), rot=-1.5)
        title(c, 'KNEW HOW TO STOP.', TX, 600, 110, CYEL, pr(t, to + 0.4, 0.4), rot=-1.5)
        virus(c, 1500, 480, 560, t, pr(t, S['t0'] + 0.3, 0.5), rot0=8)
        if t > t12 - 0.3: burst(c, 1600, 820, 120, 'NEXT 12 MONTHS', pr(t, t12 - 0.3, 0.35), size=32, col=CYEL, txt=CRED, rot=6)
        return
    paper(c, t)
    caption(c, 'YOUR TURN!', TX, 120, pr(t, tq - 1.5, 0.3), size=30)
    head2(c, 'BACK BY', '2028?', t, tq - 1.4, size=170)
    virus(c, 1400, 430, 520, t, pr(t, tq - 1.2, 0.5))
    burst(c, 1150, 800, 100, 'YES', pr(t, tc - 0.2, 0.35), col=GRN, txt=PAPER, size=56)
    burst(c, 1650, 800, 100, 'NO', pr(t, tc + 0.1, 0.35), col=CRED, txt=CYEL, size=60)
    caption(c, 'SUBSCRIBE FOR MORE REAL STORIES', TX, 700, pr(t, tc + 0.8, 0.3), col=CYEL, size=30, rot=-1.5)
    if t > END:
        k2 = pr(t, END, 0.9)
        c.drawCircle(W / 2, H / 2, 1300 * eio(k2), paint(CRED))


SUBY = 975


def with_subs(fn):
    def f(c, t, S):
        fn(c, t, S)
        if t < END + 0.2: subtitle(c, t, SUBS, y=SUBY, size=34)
    return f


SCENES = [
    dict(k='hook', t0=0.0, fn=with_subs(sc_hook)),
    dict(k='before', t0=ph('first how bad') - 0.2, fn=with_subs(sc_before), tin='whip'),
    dict(k='elim', t0=ph('then the shots came') - 0.2, fn=with_subs(sc_elim), tin='zoom'),
    dict(k='contagious', t0=ph('so why is measles') - 0.2, fn=with_subs(sc_contagious), tin='whip'),
    dict(k='cracks', t0=ph('but that wall had') - 0.2, fn=with_subs(sc_cracks), tin='zoom'),
    dict(k='chain', t0=ph("that's exactly what happened") - 0.2, fn=with_subs(sc_chain), tin='flash'),
    dict(k='y2026', t0=ph('and twenty twenty six got') - 0.2, fn=with_subs(sc_2026), tin='whip'),
    dict(k='verdict', t0=ph('now the verdict') - 0.2, fn=with_subs(sc_verdict), tin='flash'),
    dict(k='means', t0=ph('so what does it mean') - 0.2, fn=with_subs(sc_means), tin='zoom'),
    dict(k='comeback', t0=ph('so can america win') - 0.2, fn=with_subs(sc_comeback), tin='whip'),
    dict(k='end', t0=ph("so here's the honest") - 0.2, fn=with_subs(sc_end), tin='flash'),
]
EP = Episode(D, SCENES, DURATION, END)
EP.shk(ph('no longer eliminated'), 8, 0.3)
EP.shk(ph('the us lost it too'), 9, 0.3)

if __name__ == '__main__':
    EP.main(sys.argv)
