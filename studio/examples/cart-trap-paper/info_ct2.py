"""MIND TRICKS N° 07 — the shopping cart trap, PAPER look (signature purple paper, die-cut stickers dropped by hand,
hand-drawn boiling hero words, italic serif captions) + OMB brand."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, HERE)
from paper_kit import *
import info_ct as B

T = B.T; ph = T.ph; END, DUR = T.END, T.DUR
PURPLE = (88, 40, 146); PURPLE_D = (40, 18, 70); YEL = (255, 214, 92); RED_ = (232, 70, 60)
ACC = (150, 84, 230); SERIES, NUM = 'MIND TRICKS', 'N° 07'
HAS_ARCH = len(B.ARCH) > 0 and B.ARCH[0].size != (1600, 1100)
HAS_MOD = len(B.MODERN) > 0 and B.MODERN[0].size != (1600, 1100)


def ink_cart(c, s=1.0, fill=0.0, col=(36, 20, 56)): B.cart_line(c, 0, 0, s, col, 1.0, fill)
def ink_basket(c, s=1.0, k=1.0, sag=0.0, col=(36, 20, 56)): B.basket(c, 0, 40, s, k, sag, col)


def cart_sticker(c, cx, cy, w, k, rot=0.0, fill=0.0, photo=None):
    if photo is not None: sticker_img(c, photo, cx, cy, w, k, rot); return
    sticker_draw(c, lambda cc: ink_cart(cc, w / 820, fill), cx, cy, w, w * 0.78, k, rot)


def label(c, txt, x, y, k, rot=-3, size=64, bg=(250, 246, 236), fg=(30, 16, 44)):
    f = cond(size); w = f.measureText(txt)
    sticker_draw(c, lambda cc: cc.drawString(txt, -w / 2, size * 0.36, f, P(fg)), x, y, w + 70, size * 1.5, k, rot, radius=14, bg=bg)


def kb(t, t0, t1, z0=1.0, z1=1.1): return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))


# ---------------------------------------------------------------- beats
def s_hook(c, t):
    paper(c, PURPLE, t)
    boil_text(c, 'EVERY STORE.', 540, 560, 150, t, 0.0, YEL, scribble=0.15)
    cart_sticker(c, 540, 1010, 760, drop_k(t, 0.05), -4, 0.0, B.MOD_S[0] if HAS_MOD else None)
    scap(c, T, t, 0.0, ph('but when') - 0.05, 1440, 62)


def s_nobody(c, t):
    t0 = SC[1][0]; tn = ph('nobody')
    paper(c, PURPLE, t)
    cart_sticker(c, 540 + 80 * eo(cl((t - tn) / 0.4)), 1000, 700, 1.0, -4 + 14 * eo(cl((t - tn) / 0.4)), 0.0, B.MOD_S[0] if HAS_MOD else None)
    boil_text(c, 'NOBODY', 540, 640, 250, t, tn - 0.05)
    scap(c, T, t, t0, ph('so the inventor') - 0.05, 1420, 60)


def s_fake(c, t):
    t0 = SC[2][0]; tf = ph('fake')
    paper(c, PURPLE_D, t)
    if HAS_ARCH:
        for i, (x, y, r) in enumerate(((330, 1080, -8), (760, 1020, 6), (540, 1200, -2))):
            sticker_img(c, B.ARCH_S[i % len(B.ARCH_S)], x, y, 460, drop_k(t, t0 + 0.1 + i * 0.12), r)
    else:
        for i, (x, y, r) in enumerate(((300, 1080, -8), (780, 1060, 7), (540, 1200, -2))):
            cart_sticker(c, x, y, 380, drop_k(t, t0 + 0.1 + i * 0.12), r)
    scap(c, T, t, t0, tf - 0.05, 560, 64)
    boil_text(c, 'FAKE', 540, 620, 230, t, tf - 0.05, YEL); boil_text(c, 'SHOPPERS', 540, 820, 200, t, tf + 0.1, YEL)


def s_1937(c, t):
    t0 = SC[3][0]; to = ph('oklahoma'); tg = ph('goldman')
    paper(c, PURPLE, t)
    def card(cc):
        f = cond(260); cc.drawString('1937', -f.measureText('1937') / 2, 90, f, P((30, 16, 44)))
    sticker_draw(c, card, 540, 760 if t > to - 0.1 else 900, 640, 380, drop_k(t, t0 + 0.02), -3)
    if t >= to - 0.1: boil_text(c, 'OKLAHOMA CITY', 540, 1130, 120, t, to - 0.1)
    if t >= tg - 0.3: label(c, 'SYLVAN GOLDMAN, GROCER', 540, 1300, drop_k(t, tg - 0.3), 3, 54)
    elif t >= to: scap(c, T, t, ph('a grocer'), tg - 0.3, 1330, 56)


def s_heavy(c, t):
    t0 = SC[4][0]; th = ph('heavy')
    paper(c, PURPLE, t)
    sag = eo(pr(t, th - 0.2, 0.4))
    sticker_draw(c, lambda cc: ink_basket(cc, 1.05, pr(t, t0 + 0.2, th - t0), sag), 540, 1020 + 30 * sag, 640, 560, drop_k(t, t0), 2)
    scap(c, T, t, t0, th + 0.3, 520, 60)
    if t >= th - 0.05: boil_text(c, 'STOP.', 540, 1420, 170, t, th - 0.05, RED_)


def s_wheels(c, t):
    t0 = SC[5][0]; tw = ph('wheels')
    paper(c, PURPLE_D, t)
    if B.PAT is not None:
        def pat(cc):
            w = 560; h = w * B.PAT.height() / B.PAT.width()
            cc.save(); cc.clipRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h * eo(pr(t, t0 + 0.2, 1.4))))
            p = skia.Paint(); p.setColorFilter(skia.ColorFilters.Blend(skia.Color(30, 16, 44), skia.BlendMode.kSrcIn))
            cc.drawImageRect(B.PAT, skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), p); cc.restore()
        sticker_draw(c, pat, 540, 1000, 640, 820, drop_k(t, t0), -2, bg=(236, 230, 214))
    else:
        cart_sticker(c, 540, 1000, 760, drop_k(t, t0), -2)
    scap(c, T, t, t0, tw + 0.4, 470, 62)
    if t >= tw - 0.1: label(c, 'U.S. PATENT 2,196,914', 540, 1470, drop_k(t, tw - 0.1), -2, 44)


def s_flop(c, t):
    t0 = SC[6][0]; tm = ph('men said'); tw = ph('women said')
    paper(c, PURPLE, t)
    if t < tm - 0.08: boil_text(c, 'NOBODY WANTED IT.', 540, 960, 120, t, t0); return
    def note(txt, sub):
        def d(cc):
            f = serif(70); g = capf(28)
            cc.drawString(txt, -f.measureText(txt) / 2, 10, f, P((30, 16, 44))); cc.drawString(sub, -g.measureText(sub) / 2, 80, g, P((120, 90, 150)))
        return d
    sticker_draw(c, note('"It looks weak."', 'MEN'), 400, 800, 640, 260, drop_k(t, tm - 0.05), -5, bg=(255, 236, 140), radius=6)
    if t >= tw - 0.08: sticker_draw(c, note('"Another stroller?"', 'WOMEN'), 660, 1200, 680, 260, drop_k(t, tw - 0.08), 4, bg=(255, 200, 210), radius=6)


def s_models(c, t):
    t0 = SC[7][0]; ta = ph('actors'); tp = ph('pretending'); tm = ph('models')
    paper(c, PURPLE_D, t)
    if HAS_ARCH: sticker_img(c, B.ARCH_S[0], 540, 1120, 760, drop_k(t, t0), -3)
    else: cart_sticker(c, 540, 1140, 640, drop_k(t, t0), -3)
    for i, (w, tt, x, y, r) in enumerate((('MODELS.', tm, 330, 560, -6), ('ACTORS.', ta, 740, 660, 5), ('PRETENDING TO SHOP.', tp, 540, 800, -2))):
        if t >= tt - 0.1: label(c, w, x, y, drop_k(t, tt - 0.1), r, 66, (250, 246, 236))


def s_copied(c, t):
    t0 = SC[8][0]; tw = ph('within weeks'); tm = ph('multimillionaire')
    paper(c, PURPLE, t)
    n = 1 + int(8 * eo(pr(t, t0 + 0.2, tw - t0 + 1.2)))
    for i in range(n):
        x = 200 + (i % 3) * 340; y = 640 + (i // 3) * 300
        cart_sticker(c, x, y, 280, drop_k(t, t0 + 0.2 + i * 0.25), (-6, 4, -2, 7, -4, 3, -7, 5, -1)[i])
    if t >= tm - 0.1: boil_text(c, 'MULTIMILLIONAIRE', 540, 1500 - 70, 120, t, tm - 0.1, YEL)
    else: scap(c, T, t, t0, tm - 0.1, 1450, 56)


def s_twist(c, t):
    t0 = SC[9][0]
    paper(c, (24, 12, 40), t)
    boil_text(c, "BUT HERE'S THE PART", 540, 880, 110, t, t0 + 0.05)
    boil_text(c, 'NOBODY TELLS YOU.', 540, 1030, 110, t, ph('nobody tells') - 0.05, YEL)


def s_bigger(c, t):
    t0 = SC[10][0]; t3 = ph('three')
    paper(c, PURPLE, t)
    k = pr(t, t3 - 0.2, 0.6)
    cart_sticker(c, 300, 1200, 300, drop_k(t, t0), -5); label(c, '1937', 300, 1420, drop_k(t, t0 + 0.2), -4, 44)
    cart_sticker(c, 700, 1100 - 60 * eo(k), 300 + 360 * eo(k), drop_k(t, t0 + 0.15), 4)
    if t >= t3 - 0.1: boil_text(c, '~3x BIGGER', 540, 620, 170, t, t3 - 0.1, YEL)
    else: scap(c, T, t, t0, t3 - 0.1, 600, 60)


def s_forty(c, t):
    t0 = SC[11][0]; tf = ph('forty'); td = ph('doubled')
    paper(c, PURPLE_D, t)
    fill = 0.4 * eo(pr(t, td, 0.8)) + 0.6 * eo(pr(t, tf, 1.0))
    cart_sticker(c, 540, 1180, 720, drop_k(t, t0), -2, fill)
    if t >= tf - 0.1:
        boil_text(c, '+40%', 540, 760, 300, t, tf - 0.1, YEL)
        g = serif(34); s_ = 'more bought — marketing experiment (M. Lindstrom)'; c.drawString(s_, 540 - g.measureText(s_) / 2, 840, g, P(CREAM, pr(t, tf, 0.4)))
    else: scap(c, T, t, t0, tf - 0.1, 600, 58)


def s_mirror(c, t):
    t0 = SC[12][0]; tc = ph('a cart never')
    paper(c, PURPLE, t)
    sticker_draw(c, lambda cc: ink_basket(cc, 0.62, 1.0), 360, 720, 400, 360, drop_k(t, t0), -6)
    boil_text(c, 'A BASKET', 790, 640, 88, t, t0 + 0.1); boil_text(c, 'SAYS STOP.', 790, 750, 88, t, ph('stop') - 0.1, RED_)
    if t >= tc - 0.08:
        cart_sticker(c, 740, 1180, 480, drop_k(t, tc - 0.08), 5, 1.0)
        boil_text(c, 'A CART', 270, 1100, 92, t, tc - 0.08); boil_text(c, 'NEVER', 270, 1220, 104, t, ph('never') - 0.08, YEL); boil_text(c, 'DOES.', 270, 1340, 92, t, ph('does') - 0.08)


def s_send(c, t):
    t0 = SC[13][0]
    paper(c, (238, 230, 214), t)
    cart_sticker(c, 540, 820, 520, drop_k(t, t0), -3, 0.15)
    scap(c, T, t, t0, END, 1180, 64, (40, 20, 60))
    k = pr(t, ph('milk') + 0.2, 0.4)
    if k > 0:
        wordmark(c, 540, 1365, 400, False, k)
        g = capf(24); s_ = 'FOLLOW FOR DAILY BUSINESS BREAKDOWNS'; c.drawString(s_, 540 - g.measureText(s_) / 2, 1470, g, P((30, 30, 30), k))


SC = [(0.0, s_hook), (ph('but when') - 0.1, s_nobody), (ph('so the inventor') - 0.1, s_fake), (ph('nineteen thirty') - 0.1, s_1937),
      (ph('his shoppers') - 0.1, s_heavy), (ph('so he put') - 0.1, s_wheels), (ph('and nobody wanted') - 0.1, s_flop), (ph('so he hired') - 0.1, s_models),
      (ph('real shoppers') - 0.1, s_copied), (ph("but here's") - 0.1, s_twist), (ph('carts today') - 0.1, s_bigger), (ph('and one marketing') - 0.1, s_forty),
      (ph('a basket') - 0.1, s_mirror), (ph('send this') - 0.1, s_send)]
SCENES = SC
LIGHT = {13}
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
    halation(s, 0.16, 22)
    film(c, t, 0.06, 0.3 if i in LIGHT else 0.5)
    brand_badge(c)
    if i not in LIGHT and t > 0.8: series_tag(c, SERIES, NUM, ACC, t, DUR, dark=True)
    return s


def cover_fn(c):
    s = frame(ph('fake') + 0.9); c.drawImage(s.makeImageSnapshot(), 0, 0)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
