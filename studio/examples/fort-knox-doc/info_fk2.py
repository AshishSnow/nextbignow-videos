"""TRIAL v2 — DOC look after the owner's frame notes: faded matte grade + halation + soft edges, small off-white
tight-tracked captions centred, grey ghost words, 3D card spins with motion trails, triangle split, photo wall push,
red ribbon banners, rolodex year card, red 3D word on pale wall, green-felt investigation board."""
import sys, os, math
sys.path.insert(0, '/home/claude/studio'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageFilter
from doc_kit import *
import info_fk as B

HERE = B.HERE; T = B.T; ph = T.ph; END, DUR = T.END, T.DUR
A = os.path.join(HERE, 'assets')
_v = Image.open(os.path.join(A, 'a5.bin')).convert('RGB').resize((1764, 1148), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 60, 2))
TREES = sk(grade(_v, 'warm', 1.05)); TREES_BW = sk(grade(_v, 'bw', 1.1))
GB_BW = sk(grade(Image.open(os.path.join(A, 'a2.bin')).convert('RGB').resize((1600, 1200)), 'bw', 1.2))
WALL = [B.GB, B.PC_BW, TREES, TREES_BW, B.PC_COL, GB_BW]


def tag_top(c, t): B.tag_top(c, t)


def dim(c, a): c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), a))


# ---------------------------------------------------------------- scenes
def s_hook(c, t):
    ta = ph('america'); tg = ph('guarded')
    z = kb(t, 0, 3, 1.0, 1.1)
    cover(c, B.PC_COL, z, 0.05, -0.2); dim(c, 0.22)
    k = pr(t, ta - 0.08, 0.25)
    if k > 0:
        ghost_word(c, 'AMERICA', 540, 470, 300, k, RED, 1.0, -0.03, 'ArchivoCond-Black')
        cover(c, B.PC_FG, z, 0.05, -0.2); dim(c, 0.22)
    grid_lines(c, 0.28)
    if t < tg - 0.05: kword2(c, T, t, 0.0, tg - 0.05, 540, 1000, 62, spread=True)
    else: kword2(c, T, t, tg - 0.05, ta - 0.05, 540, 1000, 66)


def s_heist(c, t):
    t0 = SCENES[1][0]; th = ph('heist'); tr = ph('real life')
    c.drawRect(skia.Rect.MakeWH(W, H), P((20, 22, 24)))
    u = cl((t - t0) / 0.5)
    if u < 1:   # 3D card spins in with a motion trail, then settles full-frame
        card3d(c, TREES, W / 2, H / 2, 980, 640, ry=-70 * (1 - eo(u)), rz=-14 * (1 - eo(u)), z=900 * (1 - eo(u)), border=0, trail=4, trail_d=(-10, -2, 120))
    else:
        cover(c, TREES, kb(t, t0 + 0.5, t0 + 3.4, 1.05, 1.22), 0.15, 0.0); dim(c, 0.38)
    if t >= th - 0.05:
        amt = 14 * (1 - cl((t - th) / 0.4))
        rgb_split(c, lambda cc: ghost_word(cc, 'HEIST MOVIE', 540, 900, 170, 1.0, OFFW, 0.92), amt)
    if t < th - 0.05: kword2(c, T, t, t0, th - 0.05, 540, 960, 60)
    kword2(c, T, t, tr - 0.1, tr + 0.7, 540, 1080, 60)


def s_called(c, t):
    t0 = SCENES[2][0]; tf = ph('fort knox')
    c.drawRect(skia.Rect.MakeWH(W, H), P((16, 16, 16)))
    card3d(c, B.PC_COL, W / 2, H / 2 + 20, 900, 640, ry=8 * math.sin((t - t0) * 1.2), rz=-3, z=-60 * cl((t - t0) / 1.8), border=12)
    if t >= tf - 0.1: ribbons(c, 'FORT KNOX', t)
    else: kword2(c, T, t, t0, tf - 0.05, 540, 960, 64)


def s_1937(c, t):
    t0 = SCENES[3][0]
    rolodex(c, W / 2, H / 2 - 40, '1937', pr(t, t0 + 0.05, 0.35), t)
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.0))
    kword2(c, T, t, ph('since'), ph('the u s') - 0.05, 540, 1360, 58)


def s_gold(c, t):
    t0 = SCENES[4][0]
    split3(c, [B.PC_BW, TREES_BW, B.GB], t, t0, pr(t, t0, 0.6)); dim(c, 0.3)
    kword2(c, T, t, ph('the u s'), ph('right now') - 0.02, 540, 960, 60, maxw=640)


def s_count(c, t):
    t0 = SCENES[5][0]; tm = ph('million')
    photo_wall(c, WALL, t, t0, pr(t, t0, tm - t0 + 0.8))
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.38))
    ghost_word(c, '{:,}'.format(int(147341858 * eo(pr(t, ph('one hundred') - 0.1, tm - ph('one hundred') + 0.5)))), 540, 900, 150, 1.0, OFFW, 0.95, -0.02, 'ArchivoCond-Black')
    if t > tm: ghost_word(c, 'OUNCES OF GOLD', 540, 1060, 70, pr(t, tm, 0.25), (236, 196, 110), 0.95, -0.02, 'ArchivoCond-Black')


def s_crazy(c, t):
    t0 = SCENES[6][0]; tc = ph('crazy')
    if t < tc - 0.05:
        c.drawRect(skia.Rect.MakeWH(W, H), P((14, 14, 14)))
        kword2(c, T, t, t0, tc - 0.05, 540, 960, 66)
    else: word3d(c, 'CRAZY', t, tc - 0.05)


def s_books(c, t):
    t0 = SCENES[7][0]; tb = ph('books'); ts = ph('six')
    c.drawRect(skia.Rect.MakeWH(W, H), P((44, 36, 28)))
    B.ledger(c, 540, 1080, kb(t, t0, ts + 1.2, 1.02, 1.16), t, pr(t, ts - 0.1, 0.6))
    if tb - 0.05 <= t < ts - 0.3:
        amt = 14 * (1 - cl((t - tb) / 0.5)); rgb_split(c, lambda cc: ghost_word(cc, "GOV'T BOOKS", 540, 960, 150, 1.0, OFFW, 0.95), amt)
    elif t < tb - 0.05: kword2(c, T, t, t0, tb - 0.05, 540, 960, 64)
    else: kword2(c, T, t, ph('all that'), ph('because') - 0.02, 540, 400, 60)


def s_law(c, t):
    t0 = SCENES[8][0]; tl = ph('law'); tf = ph('forty two')
    c.drawRect(skia.Rect.MakeWH(W, H), P((30, 28, 26)))
    B.lawpage(c, 540, 1040, kb(t, t0, t0 + 5.5, 0.96, 1.1), pr(t, tl - 0.1, 1.0), pr(t, tf - 0.15, 1.1), t)
    if t < tl + 1.2: kword2(c, T, t, t0, ph('still') - 0.02, 540, 330, 58)


def s_today(c, t):
    B.s_today(c, t)


def s_same(c, t):
    t0 = SCENES[10][0]; tv = ph('same vault'); tp = ph('same price')
    felt(c)
    z = kb(t, t0, t0 + 4.5, 1.0, 1.08); c.save(); c.translate(540, 960); c.scale(z, z); c.translate(-540, -960)
    string(c, [(180, 520), (330, 760), (760, 900), (470, 1280), (900, 1450)])
    sticky(c, 860, 380, 'who\nprices it?', (236, 150, 160), 7, 40)
    sticky(c, 190, 1560, '1973', (240, 214, 90), -6, 70)
    for (img, x, y, rot, tt) in ((B.GB, 330, 760, -5, t0), (TREES, 760, 980, 4, tv - 0.05)):
        k = pr(t, tt, 0.22)
        if k > 0: card(c, img, x, y, 440, 330, rot, k); pin(c, x, y - 175)
    if t >= tp - 0.05: B.price_tag(c, 470, 1320, 0.85 * eback(pr(t, tp - 0.05, 0.3)), t); pin(c, 470, 1320 - 300)
    c.restore()
    for i, (w, tt) in enumerate((('Same gold.', t0), ('Same vault.', tv - 0.05), ('Same price tag.', tp - 0.05))):
        k = pr(t, tt, 0.18)
        if k > 0 and t < tt + (tv - t0 if i < 2 else 3): ghost_word(c, w, 540, 520, 84, k, OFFW, 0.98, -0.03, 'Archivo-SemiBold')


def s_end(c, t):
    B.s_end(c, t)


def kb(t, t0, t1, z0=1.0, z1=1.12): return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))


SCENES = [(0.0, s_hook), (ph("and it's") - 0.12, s_heist), (ph("it's called") - 0.12, s_called), (ph('since') - 0.12, s_1937),
          (ph('the u s') - 0.05, s_gold), (ph('right now') - 0.12, s_count), (ph("but here's") - 0.12, s_crazy), (ph('on the') - 0.12, s_books),
          (ph('because a law') - 0.12, s_law), (ph("at today's") - 0.12, s_today), (ph('same gold') - 0.12, s_same), (ph('and at this') - 0.12, s_end)]
B.SCENES[:] = SCENES   # B.s_today / B.s_end read their start time from SCENES
LIGHT = {11}


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    i = max(j for j, (t0, _) in enumerate(SCENES) if t >= t0); t0 = SCENES[i][0]
    gp = skia.Paint(); gp.setColorFilter(GRADE); c.saveLayer(None, gp)
    w = whip(t, t0, 0.12) if i > 0 else 0.0
    if w > 0:
        c.save(); c.translate(W * 0.2 * w * (1 if i % 2 else -1), 0)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(70 * w, 0.5)); c.saveLayer(None, p); SCENES[i][1](c, t); c.restore(); c.restore()
    else: SCENES[i][1](c, t)
    if i in (2, 6, 9): flash(c, t, t0, 0.06, 0.6)
    c.restore()
    halation(s, 0.2, 24)
    soft_edges(s, 8.0)
    film(c, t, 0.07, 0.35 if i in LIGHT else 0.7)
    if i not in (0, 2, 3) and i not in LIGHT: tag_top(c, t)
    return s


def cover_fn(c):
    s = skia.Surface(W, H); cc = s.getCanvas(); gp = skia.Paint(); gp.setColorFilter(GRADE); cc.saveLayer(None, gp)
    cover(cc, B.PC_COL, 1.0, 0.05, -0.2); dim(cc, 0.22); ghost_word(cc, 'AMERICA', 540, 470, 300, 1.0, RED, 1.0, -0.03, 'ArchivoCond-Black'); cover(cc, B.PC_FG, 1.0, 0.05, -0.2); dim(cc, 0.22)
    f = cap2(84); s_ = 'The most guarded building in'; draw_tight(cc, s_, 540 - tight_w(s_, f) / 2, 1000, f, glow_paint())
    name_box(cc, 'BOOKED AT $42.22/OZ', 540, 1180, 76, 1.0); cc.restore()
    halation(s, 0.2, 24); film(cc, 0, 0.07, 0.7)
    c.drawImage(s.makeImageSnapshot(), 0, 0)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
