"""TRIAL v3 — DOC look + OMB brand + reference script structure. MONEY EXPLAINED (blue) N° 05: Fort Knox gold booked at $42.22/oz."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, os.path.join(HERE, '..', 'fort-knox'))
import numpy as np
from PIL import Image, ImageFilter
from doc_kit import *
import info_fk as B      # postcard + sky mask, gold photo/cut-out, ledger, law page, price tag (asset prep only)
import info_fk2 as B2    # TREES photos, WALL list

T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC = (36, 98, 214); ACC_L = (120, 160, 240)
SERIES, NUM = 'MONEY EXPLAINED', 'N° 05'
TREES, TREES_BW, WALL, GB_BW = B2.TREES, B2.TREES_BW, B2.WALL, B2.GB_BW


def dim(c, a): c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), a))
def kb(t, t0, t1, z0=1.0, z1=1.12): return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))
def cap(t, a, b, y=960, size=60, **kw): kword2(c_[0], T, t, a, b, 540, y, size, **kw)


c_ = [None]


# ---------------------------------------------------------------- scenes (one beat of the script each)
def s_hook(c, t):            # POINT AT IT
    ta = ph('america'); tg = ph('guarded'); z = kb(t, 0, 3, 1.0, 1.1)
    cover(c, B.PC_COL, z, 0.05, -0.2); dim(c, 0.2)
    k = pr(t, ta - 0.08, 0.25)
    if k > 0:
        ghost_word(c, 'AMERICA', 540, 470, 300, k, ACC, 1.0, -0.03, 'ArchivoCond-Black')
        cover(c, B.PC_FG, z, 0.05, -0.2); dim(c, 0.2)
    grid_lines(c, 0.26)
    if t < tg - 0.05: kword2(c, T, t, 0.0, tg - 0.05, 540, 1000, 62, spread=True)
    else: kword2(c, T, t, tg - 0.05, ta - 0.05, 540, 1000, 66)


def s_heist(c, t):           # POP-CULTURE ANCHOR
    t0 = SC[1][0]; th = ph('heist'); tr = ph('real life')
    c.drawRect(skia.Rect.MakeWH(W, H), P((20, 22, 24))); u = cl((t - t0) / 0.5)
    if u < 1: card3d(c, TREES, W / 2, H / 2, 980, 640, ry=-70 * (1 - eo(u)), rz=-14 * (1 - eo(u)), z=900 * (1 - eo(u)), border=0, trail=4, trail_d=(-10, -2, 120))
    else: cover(c, TREES, kb(t, t0 + 0.5, t0 + 3.2, 1.05, 1.2), 0.15, 0.0); dim(c, 0.38)
    if t >= th - 0.05: rgb_split(c, lambda cc: ghost_word(cc, 'HEIST MOVIE', 540, 900, 170, 1.0, OFFW, 0.92), 14 * (1 - cl((t - th) / 0.4)))
    else: kword2(c, T, t, t0, th - 0.05, 540, 960, 60)
    kword2(c, T, t, tr - 0.1, tr + 0.7, 540, 1080, 60)


def s_name(c, t):            # NAME LATE
    t0 = SC[2][0]; tf = ph('fort knox')
    c.drawRect(skia.Rect.MakeWH(W, H), P((16, 16, 16)))
    card3d(c, B.PC_COL, W / 2, H / 2 + 20, 900, 640, ry=8 * math.sin((t - t0) * 1.2), rz=-3, z=-60 * cl((t - t0) / 1.8), border=12)
    if t >= tf - 0.1: ribbons(c, 'FORT KNOX', t, ACC)
    else: kword2(c, T, t, t0, tf - 0.05, 540, 960, 64)


def s_thesis(c, t):          # PARADOX THESIS
    t0 = SC[3][0]; ts = ph('same thing'); tr = ph('refuse')
    c.drawRect(skia.Rect.MakeWH(W, H), P((14, 13, 12)))
    card3d(c, B.GB, W / 2, H / 2 + 40, 820, 600, ry=-18 + 10 * cl((t - t0) / 3), rx=8, rz=-4, z=200 - 260 * cl((t - t0) / 3), border=10)
    dim(c, 0.35)
    if t < ts - 0.05: kword2(c, T, t, t0, ts - 0.05, 540, 960, 60, maxw=700)
    elif t < tr - 0.05: kword2(c, T, t, ts - 0.05, tr - 0.05, 540, 960, 60, maxw=700)
    else: rgb_split(c, lambda cc: ghost_word(cc, 'REFUSE TO COUNT', 540, 960, 120, 1.0, OFFW, 0.95), 16 * (1 - cl((t - tr) / 0.4)))


def s_stack(c, t):           # VIVID PROOF 1 — year, then the pile
    t0 = SC[4][0]; ta = ph('america has'); tm = ph('million')
    if t < ta - 0.1:
        rolodex(c, W / 2, H / 2 - 40, '1937', pr(t, t0 + 0.05, 0.35), t)
        kword2(c, T, t, t0, ta - 0.1, 540, 1360, 58)
    else:
        photo_wall(c, WALL, t, ta, pr(t, ta - 0.1, tm - ta + 1.0)); dim(c, 0.4)
        n = int(147341858 * eo(pr(t, ph('one hundred') - 0.1, tm - ph('one hundred') + 0.5)))
        ghost_word(c, '{:,}'.format(n), 540, 900, 150, 1.0, OFFW, 0.95, -0.02, 'ArchivoCond-Black')
        if t > tm: ghost_word(c, 'OUNCES OF GOLD', 540, 1060, 70, pr(t, tm, 0.25), (236, 196, 110), 0.95, -0.02, 'ArchivoCond-Black')


def s_trio(c, t):            # VIVID PROOF 2 — list of three, each its own cut
    t0 = SC[5][0]; tp = ph('its own'); tv = ph('no visitors')
    if t < tp - 0.08:
        cover(c, GB_BW, kb(t, t0, tp, 1.25, 1.4), -0.3, 0.2); dim(c, 0.35)
    elif t < tv - 0.08:
        split3(c, [TREES_BW, B.PC_BW, TREES], t, tp - 0.08, pr(t, tp - 0.08, 0.35)); dim(c, 0.35)
    else:
        cover(c, B.PC_BW, kb(t, tv, tv + 1.5, 1.3, 1.4), 0.4, 0.3); dim(c, 0.3)
    tag_boxes(c, ['Tons of steel.', 'Its own police force.', 'No visitors.'], 140, 860, 62,
              [pr(t, t0 - 0.05, 0.18), pr(t, tp - 0.08, 0.18), pr(t, tv - 0.08, 0.18)])


def s_books(c, t):           # PIVOT — "But on the books"
    t0 = SC[6][0]; tb = ph('books', after=t0); ts = ph('six', after=t0)
    c.drawRect(skia.Rect.MakeWH(W, H), P((44, 36, 28)))
    B.ledger(c, 540, 1130, kb(t, t0, ts + 1.2, 0.95, 1.06), t, pr(t, ts - 0.1, 0.6))
    if tb - 0.05 <= t < ts - 0.3: rgb_split(c, lambda cc: ghost_word(cc, "GOV'T BOOKS", 540, 560, 140, 1.0, OFFW, 0.95), 14 * (1 - cl((t - tb) / 0.5)))
    elif t < tb - 0.05: kword2(c, T, t, t0, tb - 0.05, 540, 560, 62)
    else: kword2(c, T, t, ph('all of that'), ph('because') - 0.02, 540, 470, 58)


def s_law(c, t):             # WHY
    t0 = SC[7][0]; tl = ph('law', after=t0); tf = ph('forty two'); tn = ph('nobody')
    if t < tn - 0.1:
        c.drawRect(skia.Rect.MakeWH(W, H), P((30, 28, 26)))
        B.lawpage(c, 540, 1040, kb(t, t0, tn, 0.96, 1.1), pr(t, tl - 0.1, 1.0), pr(t, tf - 0.15, 1.1), t)
        if t < tl + 1.2: kword2(c, T, t, t0, ph('locked') - 0.02, 540, 470, 58)
    else:
        word3d(c, 'NOBODY', t, tn - 0.1, ACC)
        kword2(c, T, t, ph('ever changed'), ph("at today's") - 0.1, 540, 1250, 72, col=(20, 20, 20))


def s_today(c, t):           # CONTRAST
    t0 = SC[8][0]; th = ph('hundreds')
    c.drawRect(skia.Rect.MakeWH(W, H), P((12, 11, 10)))
    B.cover_img(c, B.GB_CUT, 290, 1360, 200)
    big_word(c, 'ON THE BOOKS', 290, 1500, 46, 1.0, OFFW); big_word(c, '$6.2B', 290, 1220, 80, 1.0, (236, 196, 110))
    k = pr(t, th - 0.2, 0.9)
    if k > 0:
        hh = 860 * eo(k); B.cover_img_rect(c, B.GB, 560, 1440 - hh, 420, hh)
        big_word(c, "AT TODAY'S PRICE", 770, 1500, 46, k, OFFW)
        big_word(c, 'HUNDREDS OF', 770, 1440 - hh - 120, 70, k, (236, 196, 110)); big_word(c, 'BILLIONS', 770, 1440 - hh - 40, 90, k, (236, 196, 110))
    kword2(c, T, t, t0, th - 0.05, 540, 520, 62)


def s_mirror(c, t):          # MIRROR IRONY — two halves, same sentence shape
    t0 = SC[9][0]; tv = ph('too valuable'); tc = ph('too cheap')
    top = skia.Rect.MakeXYWH(0, 0, W, H / 2); bot = skia.Rect.MakeXYWH(0, H / 2, W, H / 2)
    cover(c, B.PC_BW, kb(t, t0, t0 + 4, 1.0, 1.08), rect=top)
    if t >= tc - 0.1: cover(c, B.GB, kb(t, tc, tc + 3, 1.0, 1.08), rect=bot)
    else: c.drawRect(bot, P((14, 14, 14)))
    dim(c, 0.3); c.drawLine(0, H / 2, W, H / 2, S((10, 10, 10), 10))
    if t >= tv - 0.1: ghost_word(c, 'TOO VALUABLE TO VISIT', 540, 760, 86, pr(t, tv - 0.1, 0.2), OFFW, 0.98, -0.02, 'ArchivoCond-Black')
    if t >= tc - 0.1: ghost_word(c, 'TOO CHEAP TO COUNT', 540, 1240, 86, pr(t, tc - 0.1, 0.2), (236, 196, 110), 0.98, -0.02, 'ArchivoCond-Black')
    if t < tv - 0.1: kword2(c, T, t, t0, tv - 0.1, 540, 960, 60)


def s_same(c, t):            # ECHO
    t0 = SC[10][0]; tv = ph('same vault'); tp = ph('same price')
    felt(c)
    z = kb(t, t0, t0 + 4.5, 1.0, 1.08); c.save(); c.translate(540, 960); c.scale(z, z); c.translate(-540, -960)
    string(c, [(180, 560), (330, 800), (760, 1000), (470, 1300), (900, 1450)])
    sticky(c, 190, 1500, '1973', (240, 214, 90), -6, 70)
    for (img, x, y, rot, tt) in ((B.GB, 330, 800, -5, t0), (TREES, 760, 1010, 4, tv - 0.05)):
        k = pr(t, tt, 0.22)
        if k > 0: card(c, img, x, y, 440, 330, rot, k); pin(c, x, y - 175)
    if t >= tp - 0.05: B.price_tag(c, 500, 1300, 0.8 * eback(pr(t, tp - 0.05, 0.3)), t); pin(c, 500, 1300 - 290)
    c.restore()
    for i, (w, tt) in enumerate((('Same gold.', t0), ('Same vault.', tv - 0.05), ('Same price tag.', tp - 0.05))):
        nxt = (tv - 0.05, tp - 0.05, END)[i]
        if tt <= t < nxt: ghost_word(c, w, 540, 520, 84, pr(t, tt, 0.18), OFFW, 0.98, -0.03, 'Archivo-SemiBold')


def s_end(c, t):             # ZOOM-OUT CLOSER + brand lockup
    t0 = SC[11][0]; tg = ph('government accounting')
    c.drawRect(skia.Rect.MakeWH(W, H), P((236, 230, 218)))
    z = kb(t, t0, END, 1.0, 0.92); c.save(); c.translate(540, 800); c.scale(z, z); c.translate(-540, -800)
    fr = skia.Rect.MakeXYWH(270, 580, 540, 400)
    p = P((0, 0, 0), 0.35); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20)); c.drawRect(fr.makeOutset(40, 40).makeOffset(8, 16), p)
    c.drawRect(fr.makeOutset(40, 40), P((176, 138, 60))); c.drawRect(fr.makeOutset(40, 40), S((110, 80, 30), 4)); c.drawRect(fr.makeOutset(14, 14), P((236, 230, 214)))
    cover(c, B.PC_COL, 1.0, rect=fr); c.drawCircle(540, 520, 10, P(ACC)); c.restore()
    kword2(c, T, t, t0, tg - 0.05, 540, 420, 58, col=(30, 30, 30))
    if t >= tg - 0.05:
        big_word(c, 'GOVERNMENT', 540, 1150, 110, pr(t, tg - 0.05, 0.2), (20, 20, 20), sh=0)
        big_word(c, 'ACCOUNTING.', 540, 1260, 110, pr(t, ph('accounting') - 0.05, 0.2), ACC, sh=0)
    k = pr(t, ph('accounting') + 0.3, 0.4)
    if k > 0:
        wordmark(c, 540, 1365, 400, False, k)
        g = capf(24); s_ = 'FOLLOW FOR DAILY BUSINESS BREAKDOWNS'; c.drawString(s_, 540 - g.measureText(s_) / 2, 1470, g, P((30, 30, 30), k))


SC = [(0.0, s_hook), (ph("and it's") - 0.12, s_heist), (ph("it's called") - 0.12, s_name), (ph('and the thing') - 0.12, s_thesis),
      (ph('since') - 0.12, s_stack), (ph('tons of') - 0.12, s_trio), (ph('but on the') - 0.12, s_books), (ph('because a law') - 0.12, s_law),
      (ph("at today's") - 0.12, s_today), (ph('so the building') - 0.12, s_mirror), (ph('same gold') - 0.12, s_same), (ph('and at this') - 0.12, s_end)]
SCENES = SC
LIGHT = {11}


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas(); c_[0] = c
    i = max(j for j, (t0, _) in enumerate(SC) if t >= t0); t0 = SC[i][0]
    gp = skia.Paint(); gp.setColorFilter(GRADE); c.saveLayer(None, gp)
    w = whip(t, t0, 0.12) if i > 0 else 0.0
    if w > 0:
        c.save(); c.translate(W * 0.2 * w * (1 if i % 2 else -1), 0)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(70 * w, 0.5)); c.saveLayer(None, p); SC[i][1](c, t); c.restore(); c.restore()
    else: SC[i][1](c, t)
    if i in (2, 6, 9): flash(c, t, t0, 0.06, 0.6)
    c.restore()
    halation(s, 0.2, 24); soft_edges(s, 8.0); film(c, t, 0.07, 0.35 if i in LIGHT else 0.7)
    # brand: badge always; series tag on every beat except the hook's first second and the end card
    brand_badge(c, a=1.0)
    if i not in LIGHT and t > 1.0: series_tag(c, SERIES, NUM, ACC, t, DUR, dark=True)
    return s


def cover_fn(c):
    s = skia.Surface(W, H); cc = s.getCanvas(); gp = skia.Paint(); gp.setColorFilter(GRADE); cc.saveLayer(None, gp)
    cover(cc, B.PC_COL, 1.0, 0.05, -0.2); dim(cc, 0.2); ghost_word(cc, 'AMERICA', 540, 470, 300, 1.0, ACC, 1.0, -0.03, 'ArchivoCond-Black'); cover(cc, B.PC_FG, 1.0, 0.05, -0.2); dim(cc, 0.2)
    f = cap2(84); s_ = 'The most guarded building in'; draw_tight(cc, s_, 540 - tight_w(s_, f) / 2, 1000, f, glow_paint())
    name_box(cc, 'BOOKED AT $42.22/OZ', 540, 1180, 76, 1.0, ACC); cc.restore()
    halation(s, 0.2, 24); film(cc, 0, 0.07, 0.7)
    brand_badge(cc); series_tag(cc, SERIES, NUM, ACC, 0, 1)
    c.drawImage(s.makeImageSnapshot(), 0, 0)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
