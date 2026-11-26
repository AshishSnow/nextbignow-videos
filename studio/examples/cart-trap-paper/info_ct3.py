"""MIND TRICKS N° 07 — the shopping cart trap, PAPER look v2:
real public-domain photos as die-cut stickers (1940s store interiors, Goldman's 1940 patent sheets, carts),
a word-by-word typographic hook (ref 4), hand-drawn boiling hero words, italic serif captions, OMB brand."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from paper_kit import *

T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
PURPLE = (88, 40, 146); PURPLE_D = (40, 18, 70); PAPER_C = (240, 232, 216); YEL = (255, 214, 92); RED_ = (232, 70, 60)
INK = (30, 16, 44); ACC = (150, 84, 230); SERIES, NUM = 'MIND TRICKS', 'N° 07'
A = os.path.join(HERE, 'assets')


def _img(name, mode='warm', crop=None):
    try:
        im = Image.open(os.path.join(A, name + '.bin')); im.load(); im = im.convert('RGB')
    except Exception: return None
    if crop: w, h = im.size; im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if mode == 'sepia':
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1); a = np.asarray(g, np.float32)[..., None] / 255
        im = Image.fromarray((np.concatenate([a * 245 + 8, a * 228 + 12, a * 200 + 18], -1)).clip(0, 255).astype(np.uint8))
        im = ImageEnhance.Contrast(im).enhance(1.12)
    else:
        im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Contrast(im).enhance(1.06)
    return sk(im)


def _patent(name):
    try: im = Image.open(os.path.join(A, name + '.bin')).convert('L')
    except Exception: return None
    a = np.asarray(ImageOps.autocontrast(im, cutoff=1), np.float32) / 255
    paper_c = np.array([236, 228, 208], np.float32); ink = np.array([30, 22, 40], np.float32)
    rgb = paper_c * a[..., None] + ink * (1 - a[..., None])
    return sk(Image.fromarray(rgb.clip(0, 255).astype(np.uint8)))


CANNED = _img('canned', 'sepia', (0.0, 0.0, 1.0, 0.95)); STORE = _img('storeint', 'sepia', (0.0, 0.0, 1.0, 0.95))
CART = _img('prisma', 'warm'); ROWS = _img('xinyi', 'warm'); TOY = _img('toycart', 'warm'); LONE = _img('lone', 'warm')
AISLE = _img('aisle', 'warm'); PAT1 = _patent('pat1'); PAT2 = _patent('pat2')


def kb(t, t0, t1, z0=1.0, z1=1.1): return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))


def label(c, txt, x, y, k, rot=-3, size=64, bg=(250, 246, 236), fg=INK):
    f = cond(size); w = f.measureText(txt)
    sticker_draw(c, lambda cc: cc.drawString(txt, -w / 2, size * 0.36, f, P(fg)), x, y, w + 70, size * 1.5, k, rot, radius=14, bg=bg)


def guides(c, y0, y1, col=(30, 16, 44), a=0.35):
    """dashed type guides (ref 4 word frames)"""
    pe = skia.DashPathEffect.Make([18, 12], 0)
    for y in (y0, y1):
        p = S(col, 2, a); p.setPathEffect(pe); c.drawLine(0, y, W, y, p)


def sel_box(c, x, y, w, h, col=INK):
    pe = skia.DashPathEffect.Make([10, 8], 0); p = S(col, 3, 0.8); p.setPathEffect(pe)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    for (hx, hy) in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)): c.drawRect(skia.Rect.MakeXYWH(hx - 9, hy - 9, 18, 18), P(col))


def hand_arrow(c, x0, y0, x1, y1, t, col=YEL, w=10):
    seed = int(t * 12); p = skia.Path(); p.moveTo(x0, y0); p.quadTo((x0 + x1) / 2 + 80, (y0 + y1) / 2 - 120, x1, y1)
    pen = S(col, w); pen.setStrokeCap(skia.Paint.kRound_Cap); pen.setPathEffect(skia.DiscretePathEffect.Make(12, 2.5, seed)); c.drawPath(p, pen)
    a = math.atan2(y1 - ((y0 + y1) / 2 - 120), x1 - ((x0 + x1) / 2 + 80))
    for da in (2.6, -2.6): c.drawLine(x1, y1, x1 + 60 * math.cos(a + da), y1 + 60 * math.sin(a + da), pen)


def big_type(c, txt, y, size, font, col, x=W / 2):
    f = font(size); w = f.measureText(txt); c.drawString(txt, x - w / 2, y, f, P(col)); return w


# ---------------------------------------------------------------- the hook: one designed frame per word (ref 4)
def s_hook(c, t):
    tp, tt, tev, tit, tbuy, tand, tfake = ph('push'), ph('this'), ph('every'), ph('it was'), ph('buy'), ph('and it only'), ph('fake')
    if t < tp - 0.03:
        paper(c, PAPER_C, t); guides(c, 760, 1150)
        w = big_type(c, 'YOU', 1110, 380, cond, INK); sel_box(c, W / 2 - w / 2 - 30, 760, w + 60, 390)
    elif t < tt - 0.03:
        paper(c, PURPLE, t); guides(c, 800, 1120, CREAM)
        big_type(c, 'push', 1090, 360, serif, CREAM)
    elif t < tit - 0.03:
        paper(c, PURPLE, t)
        sticker_img(c, CART, 540, 1080, 720, drop_k(t, tt - 0.03, 0.3), -4)
        hand_arrow(c, 250, 560, 420, 820, t)
        if t >= tev - 0.05: boil_text(c, 'EVERY WEEK.', 600, 560, 120, t, tev - 0.05, YEL, scribble=0.12)
    elif t < tbuy - 0.03:
        paper(c, PAPER_C, t)
        sticker_img(c, PAT1, 540, 1040, 560, drop_k(t, tit - 0.03, 0.3), 3)
        scap(c, T, t, tit - 0.03, tbuy - 0.03, 520, 66, INK)
    elif t < tand - 0.03:
        paper(c, PURPLE, t)
        sticker_img(c, CART, 540, 1180, 560, 1.0, 6 * math.sin((t - tbuy) * 18) * (1 - cl((t - tbuy) / 0.5)))
        boil_text(c, 'BUY MORE.', 540, 720, 210, t, tbuy - 0.03, YEL, scribble=0.15)
    elif t < tfake - 0.03:
        paper(c, PURPLE_D, t)
        sticker_img(c, STORE, 540, 1080, 760, drop_k(t, tand - 0.03, 0.3), -3)
        scap(c, T, t, tand - 0.03, tfake - 0.03, 560, 64)
    else:
        paper(c, PURPLE_D, t)
        sticker_img(c, STORE, 360, 1130, 520, 1.0, -8); sticker_img(c, CANNED, 740, 1180, 520, drop_k(t, tfake - 0.03, 0.25), 7)
        boil_text(c, 'FAKE', 540, 620, 240, t, tfake - 0.03, YEL, scribble=0.12); boil_text(c, 'SHOPPERS', 540, 830, 200, t, tfake + 0.1, YEL, scribble=0.12)


def s_1937(c, t):
    t0 = SC[1][0]; to = ph('oklahoma'); tg = ph('goldman'); tpb = ph('problem')
    paper(c, PURPLE, t)
    sticker_img(c, CANNED, 560, 1230, 620, drop_k(t, to - 0.1), 4)
    def card(cc):
        f = cond(230); cc.drawString('1937', -f.measureText('1937') / 2, 80, f, P(INK))
    sticker_draw(c, card, 540, 640, 560, 330, drop_k(t, t0 + 0.02), -3)
    if t >= to - 0.1 and t < tg - 0.3: boil_text(c, 'OKLAHOMA CITY', 540, 930, 100, t, to - 0.1, YEL)
    if t >= tg - 0.3: label(c, 'SYLVAN GOLDMAN, GROCER', 540, 900, drop_k(t, tg - 0.3), 3, 54)
    if t >= tpb - 0.05: boil_text(c, 'PROBLEM.', 540, 1500 - 60, 110, t, tpb - 0.05, RED_)


def s_heavy(c, t):
    t0 = SC[2][0]; th = ph('heavy')
    paper(c, PURPLE, t)
    sag = eo(pr(t, th - 0.2, 0.4))
    sticker_draw(c, lambda cc: B_basket(cc, 1.05, pr(t, t0 + 0.2, th - t0), sag), 540, 1040 + 30 * sag, 640, 560, drop_k(t, t0), 2)
    scap(c, T, t, t0, th + 0.3, 520, 60)
    if t >= th - 0.05: boil_text(c, 'STOP.', 540, 1440, 160, t, th - 0.05, RED_)


def basket(c, cx, cy, s, k_items, sag=0.0, col=OFFW, a=1.0):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    st = S(col, 6, a)
    top = -120; bot = 110 + 30 * sag
    p = skia.Path(); p.moveTo(-230, top); p.lineTo(230, top); p.lineTo(185, bot); p.lineTo(-185, bot); p.close()
    for i in range(1, 9):
        x0 = -230 + i * 460 / 9; x1 = -185 + i * 370 / 9; c.drawLine(x0, top, x1, bot, S(col, 3, a * 0.6))
    for j in range(1, 4):
        y = top + j * (bot - top) / 4; w = 230 - 45 * j / 4; c.drawLine(-w, y, w, y, S(col, 3, a * 0.6))
    c.drawPath(p, st)
    h = skia.Path(); h.moveTo(-150, top); h.cubicTo(-150, top - 190 - 30 * sag, 150, top - 190 - 30 * sag, 150, top); c.drawPath(h, S(col, 8, a))
    cols = [(200, 70, 60), (236, 196, 110), (90, 150, 210), (120, 190, 120), (230, 150, 70), (190, 120, 200)]
    for i in range(6):
        kk = cl(k_items * 6 - i)
        if kk <= 0: continue
        bx = -165 + (i % 3) * 110 + (i // 3) * 40; by = bot - 120 - (i // 3) * 85 - 320 * (1 - eo(kk))
        c.drawRRect(rr(bx, by, 90, 110, 10), P(cols[i], a)); c.drawRRect(rr(bx, by, 90, 110, 10), S((20, 20, 20), 3, a))
    c.restore()



def B_basket(c, s, k, sag):
    basket(c, 0, 40, s, k, sag, INK)


def s_built(c, t):
    t0 = SC[3][0]; tb = ph('two baskets'); tf = ph('folding'); tw = ph('wheels')
    paper(c, PURPLE_D, t)
    sticker_img(c, PAT2, 360, 1150, 430, drop_k(t, t0 + 0.05), -5)
    sticker_img(c, PAT1, 730, 1090, 430, drop_k(t, tb - 0.1), 5)
    scap(c, T, t, t0, tb - 0.05, 520, 62)
    for (txt, tt, x, y, r) in (('TWO BASKETS.', tb, 540, 470, -3), ('A FOLDING FRAME.', tf, 540, 580, 2), ('WHEELS.', tw, 540, 690, -2)):
        if t >= tt - 0.1: label(c, txt, x, y, drop_k(t, tt - 0.1), r, 60, YEL)


def s_flop(c, t):
    t0 = SC[4][0]; tm = ph('men said'); tw = ph('women said')
    paper(c, PURPLE, t)
    if t < tm - 0.08:
        sticker_img(c, LONE, 540, 1080, 820, drop_k(t, t0), -2)
        boil_text(c, 'NOBODY TOUCHED IT.', 540, 620, 110, t, t0 + 0.05); return
    sticker_img(c, LONE, 540, 1120, 820, 1.0, -2)
    def note(txt, sub):
        def d(cc):
            f = serif(70); g = capf(28)
            cc.drawString(txt, -f.measureText(txt) / 2, 10, f, P(INK)); cc.drawString(sub, -g.measureText(sub) / 2, 80, g, P((120, 90, 150)))
        return d
    sticker_draw(c, note('"It looks weak."', 'MEN'), 400, 620, 640, 240, drop_k(t, tm - 0.05), -5, bg=(255, 236, 140), radius=6)
    if t >= tw - 0.08: sticker_draw(c, note('"Another stroller?"', 'WOMEN'), 660, 860, 680, 240, drop_k(t, tw - 0.08), 4, bg=(255, 200, 210), radius=6)


def s_models(c, t):
    t0 = SC[5][0]; tm = ph('models'); ta = ph('actors'); tp = ph('pretending')
    paper(c, PURPLE_D, t)
    boil_text(c, 'FAKE SHOPPERS.', 540, 560, 130, t, t0 + 0.05, YEL)
    sticker_img(c, STORE, 380, 1090, 560, drop_k(t, tm - 0.1), -6); sticker_img(c, CANNED, 720, 1170, 560, drop_k(t, ta - 0.1), 6)
    for (w, tt, x, y, r) in (('MODELS.', tm, 300, 760, -6), ('ACTORS.', ta, 770, 780, 5), ('PRETENDING TO SHOP.', tp, 540, 1440, -2)):
        if t >= tt - 0.1: label(c, w, x, y, drop_k(t, tt - 0.1), r, 62)


def s_copied(c, t):
    t0 = SC[6][0]; tw = ph('within weeks'); tm = ph('multimillionaire')
    paper(c, PURPLE, t)
    if t < tw - 0.1:
        sticker_img(c, STORE, 540, 1040, 800, drop_k(t, t0), -3); scap(c, T, t, t0, tw - 0.1, 520, 60)
    else:
        sticker_img(c, ROWS, 540, 1060, 860, drop_k(t, tw - 0.1), 3)
        if t >= tm - 0.1: boil_text(c, 'MULTIMILLIONAIRE', 540, 1440, 120, t, tm - 0.1, YEL)
        else: scap(c, T, t, tw - 0.1, tm - 0.1, 560, 58)


def s_twist(c, t):
    t0 = SC[7][0]
    paper(c, (24, 12, 40), t)
    boil_text(c, "BUT HERE'S THE PART", 540, 880, 110, t, t0 + 0.05)
    boil_text(c, 'NOBODY TELLS YOU.', 540, 1030, 110, t, ph('nobody tells') - 0.05, YEL)


def s_bigger(c, t):
    t0 = SC[8][0]; t3 = ph('three')
    paper(c, PURPLE, t); k = pr(t, t3 - 0.2, 0.6)
    sticker_img(c, TOY, 300, 1200, 300, drop_k(t, t0), -5); label(c, 'THEN', 300, 1420, drop_k(t, t0 + 0.2), -4, 44)
    sticker_img(c, CART, 720, 1120 - 40 * eo(k), 300 + 340 * eo(k), drop_k(t, t0 + 0.15), 4)
    if t >= t3 - 0.1: boil_text(c, '~3x BIGGER', 540, 620, 170, t, t3 - 0.1, YEL)
    else: scap(c, T, t, t0, t3 - 0.1, 600, 60)


def s_forty(c, t):
    t0 = SC[9][0]; tf = ph('forty'); td = ph('doubling')
    paper(c, PURPLE_D, t)
    sticker_img(c, AISLE, 540, 1220, 520, drop_k(t, t0), -3)
    if t >= tf - 0.1:
        boil_text(c, '+40%', 540, 700, 300, t, tf - 0.1, YEL)
        g = serif(34); s_ = 'more bought — marketing experiment (M. Lindstrom)'; c.drawString(s_, 540 - g.measureText(s_) / 2, 790, g, P(CREAM, pr(t, tf, 0.4)))
    else: scap(c, T, t, t0, tf - 0.1, 600, 58)


def s_mirror(c, t):
    t0 = SC[10][0]; tc = ph('a cart never')
    paper(c, PURPLE, t)
    sticker_draw(c, lambda cc: basket(cc, 0, 40, 0.62, 1.0, 0.0, INK), 330, 720, 400, 360, drop_k(t, t0), -6)
    boil_text(c, 'A BASKET', 790, 640, 88, t, t0 + 0.1); boil_text(c, 'SAYS STOP.', 790, 750, 88, t, ph('stop') - 0.1, RED_)
    if t >= tc - 0.08:
        sticker_img(c, CART, 740, 1180, 460, drop_k(t, tc - 0.08), 5)
        boil_text(c, 'A CART', 270, 1100, 92, t, tc - 0.08); boil_text(c, 'NEVER', 270, 1220, 104, t, ph('never') - 0.08, YEL); boil_text(c, 'DOES.', 270, 1340, 92, t, ph('does') - 0.08)


def s_send(c, t):
    t0 = SC[11][0]
    paper(c, PAPER_C, t)
    sticker_img(c, CART, 540, 800, 560, drop_k(t, t0), -3)
    scap(c, T, t, t0, END, 1180, 64, (40, 20, 60))
    k = pr(t, ph('milk') + 0.2, 0.4)
    if k > 0:
        wordmark(c, 540, 1365, 400, False, k)
        g = capf(24); s_ = 'FOLLOW FOR DAILY BUSINESS BREAKDOWNS'; c.drawString(s_, 540 - g.measureText(s_) / 2, 1470, g, P((30, 30, 30), k))


SC = [(0.0, s_hook), (ph('nineteen thirty') - 0.1, s_1937), (ph('his shoppers') - 0.1, s_heavy), (ph('so he built') - 0.1, s_built),
      (ph('and nobody would') - 0.1, s_flop), (ph('so he hired') - 0.1, s_models), (ph('real shoppers') - 0.1, s_copied), (ph("but here's") - 0.1, s_twist),
      (ph('carts today') - 0.1, s_bigger), (ph('and in one') - 0.1, s_forty), (ph('a basket') - 0.1, s_mirror), (ph('send this') - 0.1, s_send)]
SCENES = SC
LIGHT = {11}
WARM = grade_filter(desat=0.05, lift=0.02, gain=0.98, cool=-0.01)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    i = max(j for j, (t0, _) in enumerate(SC) if t >= t0); t0 = SC[i][0]
    gp = skia.Paint(); gp.setColorFilter(WARM); c.saveLayer(None, gp)
    w = whip(t, t0, 0.1) if i > 0 else 0.0
    if w > 0:
        c.save(); c.translate(0, -H * 0.12 * w)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(0.5, 50 * w)); c.saveLayer(None, p); SC[i][1](c, t); c.restore(); c.restore()
    else: SC[i][1](c, t)
    c.restore()
    halation(s, 0.14, 22)
    film(c, t, 0.06, 0.3 if i in LIGHT else 0.5)
    brand_badge(c)
    if i not in LIGHT and t > 0.8: series_tag(c, SERIES, NUM, ACC, t, DUR, dark=True)
    return s


def cover_fn(c):
    s = frame(ph('fake') + 0.8); c.drawImage(s.makeImageSnapshot(), 0, 0)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
