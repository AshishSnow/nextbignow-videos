"""TRIAL — DOC look (documentary kinetic edit) — MONEY EXPLAINED: Fort Knox gold is booked at $42.22/oz.
Public-domain / CC0 photos only (assets/credits.jsonl); no people, no logos."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio')
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from doc_kit import *

HERE = os.path.dirname(os.path.abspath(__file__))
T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
A = os.path.join(HERE, 'assets')
GOLD = (232, 180, 60)

# ---------------------------------------------------------------- assets (prepared once)
_pc = Image.open(os.path.join(A, 'img3.bin')).convert('RGB')
_pc = _pc.crop((int(_pc.width * 0.035), int(_pc.height * 0.10), int(_pc.width * 0.965), int(_pc.height * 0.93)))   # drop postcard caption + border
PC_COL = sk(grade(_pc, 'warm', 1.12))
PC_BW = sk(grade(_pc.filter(ImageFilter.GaussianBlur(1.6)), 'bw', 1.12))
# sky mask (for tucking big words behind the building): blue-ish, bright pixels above the roofline
_a = np.asarray(_pc).astype(np.int16)
_roof = np.where(np.arange(_pc.width) < 1150, 540, 468)   # roofline measured by hand on this postcard (img px)
_yy = np.arange(_pc.height)[:, None]
_fgm = (_yy >= _roof[None, :]) | ((_a[..., 0] - _a[..., 2] > 70) & (_yy < _pc.height * 0.45)) | ((_a.sum(-1) < 240) & (_yy < _pc.height * 0.45))
_m = Image.fromarray((_fgm * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
_fg = grade(_pc, 'warm', 1.12).convert('RGBA'); _fg.putalpha(_m); PC_FG = sk(_fg)

_gb = Image.open(os.path.join(A, 'a2.bin')).convert('RGB'); _gb.thumbnail((2400, 2400))
GB = sk(grade(_gb, 'warm', 1.1))
_g = np.asarray(_gb).astype(np.int16); sat = _g.max(-1) - _g.min(-1)
_gm = Image.fromarray(((sat > 38) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
_gc = _gb.convert('RGBA'); _gc.putalpha(_gm); _gc = _gc.crop(_gm.getbbox()); _gc.thumbnail((1400, 1400))
GB_CUT = sk(sticker(_gc, 12))
GB_CUT_RAW = sk(_gc)


def tag_top(c, t, txt='MONEY EXPLAINED — N° 05', dark=True):
    f = capf(26); c.drawString(txt, 80, 230, f, P(WHITE_ if dark else BLACK, 0.85))
    c.drawRect(skia.Rect.MakeXYWH(80, 248, 920 * cl(t / DUR), 3), P(WHITE_ if dark else BLACK, 0.7))


def kb(t, t0, t1, z0=1.0, z1=1.12):
    return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))


# ---------------------------------------------------------------- vault door (procedural, steel)
def vault_door(c, cx, cy, r, rot, light=1.0):
    def rad(rr_, cols, pos):
        return skia.GradientShader.MakeRadial((cx - r * 0.3, cy - r * 0.35), rr_, [skia.Color4f(*[v / 255 for v in col], 1) for col in cols], pos)
    c.drawCircle(cx, cy, r * 1.12, P((30, 30, 32)))
    c.drawCircle(cx, cy, r * 1.06, skia.Paint(AntiAlias=True, Shader=rad(r * 2.2, [(210, 212, 214), (120, 122, 126), (60, 62, 66)], [0, 0.5, 1])))
    for i in range(24):
        a = math.radians(i * 15 + rot * 0.2); bx, by = cx + r * 0.98 * math.cos(a), cy + r * 0.98 * math.sin(a)
        c.drawCircle(bx, by, r * 0.035, P((40, 40, 44))); c.drawCircle(bx - 2, by - 2, r * 0.025, P((190, 190, 196)))
    c.drawCircle(cx, cy, r * 0.86, skia.Paint(AntiAlias=True, Shader=rad(r * 1.8, [(236, 236, 238), (150, 152, 156), (80, 82, 86)], [0, 0.45, 1])))
    c.drawCircle(cx, cy, r * 0.86, S((40, 40, 44), 6))
    for k in range(3): c.drawCircle(cx, cy, r * (0.5 + 0.12 * k), S((90, 92, 96), 3, 0.6))
    c.save(); c.translate(cx, cy); c.rotate(rot)
    for i in range(3):
        c.save(); c.rotate(i * 120)
        c.drawRRect(rr(-r * 0.04, -r * 0.62, r * 0.08, r * 0.62, r * 0.03), P((70, 72, 76))); c.drawCircle(0, -r * 0.64, r * 0.07, P((200, 200, 205))); c.drawCircle(0, -r * 0.64, r * 0.07, S((40, 40, 44), 4))
        c.restore()
    c.drawCircle(0, 0, r * 0.16, P((60, 62, 66))); c.drawCircle(0, 0, r * 0.16, S((210, 210, 214), 5))
    c.restore()
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 1 - light))


# ---------------------------------------------------------------- documents (rendered by us, text from the Treasury report / Pub. L. 93-110)
def ledger(c, x, y, s, t, hk):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-3)
    R = skia.Rect.MakeXYWH(-430, -560, 860, 1120)
    p = P((0, 0, 0), 0.5); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)); c.drawRect(R.makeOffset(14, 24), p)
    c.drawRect(R, P((244, 240, 230)))
    m = mono(24); b = dfont('Archivo-Bold', 30)
    c.drawString('STATUS REPORT OF U.S.', -380, -470, b, P(BLACK)); c.drawString('GOVERNMENT GOLD RESERVE', -380, -430, b, P(BLACK))
    c.drawLine(-380, -400, 380, -400, S(BLACK, 3))
    c.drawString('LOCATION            FINE TROY OZ', -380, -350, m, P(BLACK, 0.75))
    rows = [('Denver, CO', '43,853,707'), ('Fort Knox, KY', '147,341,858'), ('West Point, NY', '54,067,331'), ('NY Fed vault', '418,121')]
    for i, (a_, b_) in enumerate(rows):
        yy = -290 + i * 60; f2 = mono(26)
        c.drawString(a_, -380, yy, f2, P(BLACK, 0.9)); c.drawString(b_, 380 - f2.measureText(b_), yy, f2, P(BLACK, 0.9))
    c.drawLine(-380, -40, 380, -40, S(BLACK, 2, 0.6))
    c.drawString('FORT KNOX BOOK VALUE', -380, 30, m, P(BLACK, 0.75))
    big = mono(46); v = '$6,221,097,412'
    highlight(c, -390, 70, big.measureText(v) + 20, 62, hk)
    c.drawString(v, -380, 118, big, P(BLACK))
    c.drawString('Statutory rate: $42.2222 per fine troy ounce', -380, 220, mono(22), P(BLACK, 0.7))
    c.drawString('Source: Bureau of the Fiscal Service', -380, 480, mono(20), P(BLACK, 0.5))
    c.restore()


def lawpage(c, x, y, s, k1, k2, t):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(2)
    R = skia.Rect.MakeXYWH(-430, -600, 860, 1200)
    p = P((0, 0, 0), 0.5); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 22)); c.drawRect(R.makeOffset(14, 24), p)
    c.drawRect(R, P((238, 232, 214)))
    typewriter(c, 'PUBLIC LAW 93-110', k1, -360, -470, 40, BLACK, cursor=k2 <= 0, t=t)
    typewriter(c, 'SEPTEMBER 21, 1973', cl(k1 * 1.6 - 0.6), -360, -410, 34, BLACK, cursor=False, t=t)
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(-360, -330 + i * 44, 560 + (i * 37 % 160), 14), P(BLACK, 0.12))
    typewriter(c, '$42.22', k2, -360, 40, 150, BLACK, cursor=True, t=t)
    if k2 > 0.95: c.drawString('PER FINE TROY OUNCE', -356, 110, mono(34), P(BLACK, 0.8))
    c.restore()


def price_tag(c, x, y, s, t):
    c.save(); c.translate(x, y); c.rotate(8 * math.sin(t * 2.2)); c.scale(s, s)
    c.drawLine(0, -340, 0, -170, S((90, 80, 60), 4))
    pth = skia.Path(); pth.moveTo(-170, -170); pth.lineTo(170, -170); pth.lineTo(170, 230); pth.lineTo(-170, 230); pth.close()
    pth2 = skia.Path(); pth2.moveTo(-170, -110); pth2.lineTo(0, -230); pth2.lineTo(170, -110); pth2.lineTo(170, 230); pth2.lineTo(-170, 230); pth2.close()
    sh = P((0, 0, 0), 0.5); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16)); c.drawPath(pth2.makeOffset(10, 18) if hasattr(pth2, 'makeOffset') else pth2, sh)
    c.drawPath(pth2, P((240, 226, 190))); c.drawPath(pth2, S((150, 120, 70), 4)); c.drawCircle(0, -150, 16, P((60, 50, 40)))
    f = cond(120); c.drawString('$42.22', -f.measureText('$42.22') / 2, 50, f, P(BLACK))
    g = mono(30); c.drawString('PER OZ · 1973', -g.measureText('PER OZ · 1973') / 2, 130, g, P(BLACK, 0.8))
    c.restore()


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    ta = ph('america')
    z = kb(t, 0, 3, 1.0, 1.08)
    cover(c, PC_COL, z, 0.05, -0.2)
    k = pr(t, ta - 0.08, 0.3)
    if k > 0:   # big word tucked BEHIND the building (sky mask)
        big_word(c, 'AMERICA', 540, 585, 300, k, RED, sh=0.15)
        cover(c, PC_FG, z, 0.05, -0.2)
    kword(c, T, t, 0.0, ta - 0.05, 540, 1330, 84, maxw=820)
    tag_top(c, t)


def s_heist(c, t):
    t0 = SCENES[1][0]; th = ph('heist'); tr = ph('real life')
    c.drawRect(skia.Rect.MakeWH(W, H), P((14, 14, 16)))
    vault_door(c, 540, 1060, 470 * kb(t, t0, t0 + 3.4, 1.0, 1.12), -40 * cl((t - t0) / 3), 0.92)
    g = pr(t, th - 0.06, 0.12); amt = 22 * (1 - cl((t - th) / 0.35)) if t >= th else 0
    if g > 0: rgb_split(c, lambda cc: big_word(cc, 'HEIST MOVIE', 540, 560, 190, 1.0, WHITE_), amt)
    kword(c, T, t, tr - 0.02, tr + 0.6, 540, 1650 - 260, 86)
    if t < th - 0.05: kword(c, T, t, t0, th - 0.05, 540, 560, 76)


def s_called(c, t):
    t0 = SCENES[2][0]; tf = ph('fort knox')
    cover(c, PC_COL, kb(t, t0, t0 + 2, 1.35, 1.5), -0.1, 0.0)
    kword(c, T, t, t0, tf - 0.02, 540, 560, 72)
    name_box(c, 'FORT KNOX, KENTUCKY', 540, 1300, 70, pr(t, tf - 0.05, 0.22))


def s_1937(c, t):
    t0 = SCENES[3][0]
    cover(c, PC_BW, 1.5, 0.2, 0.2, blur=12); c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.55))
    flip_counter(c, 540, 960, 1900, 1937, pr(t, t0 + 0.05, 1.0), 250, 'FIRST GOLD ARRIVED', t)
    kword(c, T, t, ph('the u s'), ph('here', end=True) + 0.1, 540, 1330, 64)


def s_gold(c, t):
    t0 = SCENES[4][0]
    cover(c, GB, kb(t, t0, t0 + 2.5, 1.15, 1.3), 0.1, 0.0)
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.25))
    kword(c, T, t, ph('the u s'), ph('right now') - 0.02, 540, 560, 74)


def s_count(c, t):
    t0 = SCENES[5][0]; tm = ph('million')
    c.drawRect(skia.Rect.MakeWH(W, H), P((12, 11, 10)))
    sh = skia.GradientShader.MakeRadial((540, 1150), 700, [skia.Color4f(0.45, 0.33, 0.1, 0.55), skia.Color4f(0, 0, 0, 0)], [0, 1]); c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))
    k = pr(t, t0 + 0.05, 0.4)
    for e in range(4, 0, -1):   # echo trail (reference: stacked cut-out trail)
        c.save(); c.translate(-60 * e * (1 - eo(k)) - e * 14, 0); cover_img(c, GB_CUT_RAW, 540, 1170, 860, 0.18 * k / e); c.restore()
    cover_img(c, GB_CUT, 540, 1170, 860, k)
    counter_text(c, 147341858, 540, 640, 150, pr(t, ph('one hundred') - 0.1, tm - ph('one hundred') + 0.5))
    if t > tm: big_word(c, 'OUNCES OF GOLD', 540, 760, 80, pr(t, tm, 0.25), GOLD)


def cover_img(c, img, cx, cy, w, a=1.0):
    h = w * img.height() / img.width(); p = skia.Paint(AntiAlias=True, Alphaf=a)
    c.drawImageRect(img, skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), p)


def s_crazy(c, t):
    t0 = SCENES[6][0]; tc = ph('crazy')
    c.drawRect(skia.Rect.MakeWH(W, H), P(BLACK))
    amt = 18 * (1 - cl((t - tc) / 0.4)) if t >= tc else 0
    kword(c, T, t, t0, tc - 0.02, 540, 840, 84)
    if t >= tc - 0.04: rgb_split(c, lambda cc: big_word(cc, 'CRAZY PART.', 540, 1080, 210, 1.0, WHITE_), amt)


def s_books(c, t):
    t0 = SCENES[7][0]; tb = ph('books'); ts = ph('six')
    c.drawRect(skia.Rect.MakeWH(W, H), P((40, 38, 34)))
    ledger(c, 540, 1080, kb(t, t0, ts + 1.2, 1.0, 1.12), t, pr(t, ts - 0.1, 0.6))
    amt = 16 * (1 - cl((t - tb) / 0.5)) if t >= tb else 0
    if tb - 0.05 <= t < ts - 0.3: rgb_split(c, lambda cc: big_word(cc, "GOV'T BOOKS", 540, 470, 150, 1.0, WHITE_), amt)
    if t >= ts - 0.3: kword(c, T, t, ph('all that'), ph('because') - 0.02, 540, 440, 70)


def s_law(c, t):
    t0 = SCENES[8][0]; tl = ph('law'); tf = ph('forty two')
    c.drawRect(skia.Rect.MakeWH(W, H), P((28, 26, 24)))
    lawpage(c, 540, 1040, kb(t, t0, t0 + 5.5, 0.95, 1.08), pr(t, tl - 0.1, 1.0), pr(t, tf - 0.15, 1.1), t)
    if t < tl + 1.2: kword(c, T, t, t0, ph('still') - 0.02, 540, 330, 62)


def s_today(c, t):
    t0 = SCENES[9][0]; th = ph('hundreds')
    c.drawRect(skia.Rect.MakeWH(W, H), P((12, 11, 10)))
    cover_img(c, GB_CUT, 290, 1360, 200)
    big_word(c, 'ON THE BOOKS', 290, 1500, 46, 1.0, WHITE_); big_word(c, '$6.2B', 290, 1220, 80, 1.0, GOLD)
    k = pr(t, th - 0.2, 0.9)
    if k > 0:
        hh = 860 * eo(k); w = 420
        cover_img_rect(c, GB, 560, 1440 - hh, w, hh)
        big_word(c, 'AT TODAY\'S PRICE', 770, 1500, 46, k, WHITE_)
        big_word(c, 'HUNDREDS OF', 770, 1440 - hh - 120, 70, k, GOLD); big_word(c, 'BILLIONS', 770, 1440 - hh - 40, 90, k, GOLD)
    kword(c, T, t, t0, th - 0.05, 540, 520, 70)


def cover_img_rect(c, img, x, y, w, h):
    cover(c, img, 1.0, rect=skia.Rect.MakeXYWH(x, y, w, h))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), S(WHITE_, 6))


def s_same(c, t):
    t0 = SCENES[10][0]; tv = ph('same vault'); tp = ph('same price')
    c.drawRect(skia.Rect.MakeWH(W, H), P((226, 222, 212)))
    card(c, GB, 330, 760, 460, 560, -6, pr(t, t0, 0.25))
    if t >= tv - 0.05: card(c, PC_BW, 760, 1000, 520, 400, 5, pr(t, tv - 0.05, 0.25))
    if t >= tp - 0.05: price_tag(c, 470, 1300, 0.9 * eback(pr(t, tp - 0.05, 0.3)), t)
    ws = ['SAME GOLD.', 'SAME VAULT.', 'SAME PRICE TAG.']
    tag_boxes(c, ws, 120, 400, 64, [pr(t, t0, 0.2), pr(t, tv - 0.05, 0.2), pr(t, tp - 0.05, 0.2)])
    if t > ph('from nineteen', after=33) - 0.05: name_box(c, 'SINCE 1973', 760, 1560 - 160, 64, pr(t, ph('from nineteen', after=33) - 0.05, 0.2))


def s_end(c, t):
    t0 = SCENES[11][0]; tg = ph('government accounting')
    c.drawRect(skia.Rect.MakeWH(W, H), P((242, 240, 236)))
    z = kb(t, t0, END, 1.0, 0.86); c.save(); c.translate(540, 960); c.scale(z, z); c.translate(-540, -960)
    fr = skia.Rect.MakeXYWH(250, 700, 580, 440)
    p = P((0, 0, 0), 0.35); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 20)); c.drawRect(fr.makeOutset(40, 40).makeOffset(8, 16), p)
    c.drawRect(fr.makeOutset(40, 40), P((176, 138, 60))); c.drawRect(fr.makeOutset(40, 40), S((110, 80, 30), 4)); c.drawRect(fr.makeOutset(14, 14), P((236, 230, 214)))
    cover(c, PC_COL, 1.0, rect=fr)
    c.drawCircle(540, 640, 10, P((200, 40, 40))); c.restore()
    kword(c, T, t, t0, tg - 0.05, 540, 470, 60, BLACK)
    if t >= tg - 0.05:
        big_word(c, 'GOVERNMENT', 540, 1400, 130, pr(t, tg - 0.05, 0.2), BLACK, sh=0)
        big_word(c, 'ACCOUNTING.', 540, 1530, 130, pr(t, ph('accounting') - 0.05, 0.2), RED, sh=0)
    if t > END - 0.9:
        g = capf(30); a = cl((t - END + 0.9) / 0.3); s_ = 'FOLLOW FOR DAILY BUSINESS BREAKDOWNS'
        c.drawString(s_, 540 - g.measureText(s_) / 2, 1620, g, P(BLACK, a))


SCENES = [(0.0, s_hook), (ph("and it's") - 0.12, s_heist), (ph("it's called") - 0.12, s_called), (ph('since') - 0.12, s_1937),
          (ph('the u s') + 0.6, s_gold), (ph('right now') - 0.12, s_count), (ph("but here's") - 0.12, s_crazy), (ph('on the') - 0.12, s_books),
          (ph('because a law') - 0.12, s_law), (ph("at today's") - 0.12, s_today), (ph('same gold') - 0.12, s_same), (ph('and at this') - 0.12, s_end)]
LIGHT = {10, 11}


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0); t0 = SCENES[i][0]
    w = whip(t, t0, 0.14) if i > 0 else 0.0
    if w > 0:   # whip cut: new scene slides in with horizontal smear
        c.save(); c.translate(W * 0.18 * w * (1 if i % 2 else -1), 0)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(60 * w, 0.5)); c.saveLayer(None, p); SCENES[i][1](c, t); c.restore(); c.restore()
    else: SCENES[i][1](c, t)
    if i in (2, 6, 9): flash(c, t, t0, 0.07, 0.7)
    film(c, t, 0.06 if i in LIGHT else 0.09, 0.25 if i in LIGHT else 0.6)
    if i not in (0,) and i not in LIGHT: tag_top(c, t)
    return s


def cover_fn(c):
    cover(c, PC_COL, 1.0, 0.05, -0.2)
    big_word(c, 'AMERICA', 540, 585, 300, 1.0, RED, sh=0.15); cover(c, PC_FG, 1.0, 0.05, -0.2)
    f = capf(84); s_ = 'Most guarded building in'; c.drawString(s_, 540 - f.measureText(s_) / 2, 1300, f, shadow_paint(WHITE_))
    name_box(c, 'BOOKED AT $42.22/OZ', 540, 1420, 76, 1.0)
    film(c, 0, 0.08, 0.6)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
