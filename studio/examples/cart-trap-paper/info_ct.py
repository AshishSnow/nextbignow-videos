"""MIND TRICKS (purple) N° 07 — the shopping cart trap. PREMIUM DOC look v4:
rich film grade (deep blacks, warm highlights, cool shadows), selective focus blur, 2.5D parallax on archive photos,
dust + light leaks, patent drawing that draws itself, line-art props, kinetic off-white captions, OMB brand."""
import sys, os, math, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/studio')
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
from doc_kit import *

T = Timing(HERE); ph = T.ph; END, DUR = T.END, T.DUR
ACC = (150, 84, 230); ACC_D = (86, 40, 150)
SERIES, NUM = 'MIND TRICKS', 'N° 07'
A = os.path.join(HERE, 'assets')


# ---------------------------------------------------------------- assets
def _load(name, mode='bw', con=1.15, maxw=2200):
    f = os.path.join(A, name + '.bin')
    try: im = Image.open(f); im.load()
    except Exception: return None
    if im.mode in ('I;16', 'I', 'F'): im = ImageOps.autocontrast(im.convert('L'))
    im = im.convert('RGB'); im.thumbnail((maxw, maxw))
    return grade(im, mode, con)


def _pick(*names, mode='bw'):
    for n in names:
        im = _load(n, mode)
        if im is not None: return im
    return None


ARCH = [im for im in (_load(n) for n in ('grandunion', 'bohack', 'winn1', 'winn2', 'calimax')) if im is not None]
MODERN = [im for im in (_load(n, 'warm', 1.08) for n in ('prisma', 'xinyi', 'lone')) if im is not None]
if not ARCH: ARCH = [Image.new('RGB', (1600, 1100), (60, 60, 60))]
if not MODERN: MODERN = [Image.new('RGB', (1600, 1100), (70, 60, 50))]
ARCH_S = [sk(a) for a in ARCH]; ARCH_B = [sk(a.filter(ImageFilter.GaussianBlur(14))) for a in ARCH]
MOD_S = [sk(m) for m in MODERN]; MOD_B = [sk(m.filter(ImageFilter.GaussianBlur(14))) for m in MODERN]


def _patent():
    f = os.path.join(A, 'pat0.bin')
    try: im = Image.open(f).convert('L'); im.thumbnail((1600, 1600))
    except Exception: return None, None
    a = np.asarray(im)
    ink = (a < 150).astype(np.uint8) * 255
    lines = Image.fromarray(ink).filter(ImageFilter.MaxFilter(3))
    bbox = lines.getbbox(); lines = lines.crop(bbox)
    rgba_w = Image.new('RGBA', lines.size, (240, 236, 228, 0)); rgba_w.putalpha(lines)          # cream lines
    rgba_p = Image.new('RGBA', lines.size, (190, 150, 255, 0)); rgba_p.putalpha(lines)          # glow lines
    return sk(rgba_w), sk(rgba_p.filter(ImageFilter.GaussianBlur(6)))


PAT, PAT_GLOW = _patent()


# ---------------------------------------------------------------- premium finish helpers
def focus_photo(c, img, img_b, t, t0, t1, z0=1.06, z1=1.18, ox=0.0, oy=0.0, fx=540, fy=900, fr=520, drift=(0, 0)):
    """2.5D: blurred copy drifts slower behind; sharp copy masked by a soft focus ellipse drifts faster (depth + 'blur some place')"""
    u = cl((t - t0) / max(0.01, t1 - t0)); z = z0 + (z1 - z0) * eio(u)
    cover(c, img_b, z * 1.04, ox * 0.6 + drift[0] * u * 0.5, oy * 0.6 + drift[1] * u * 0.5)
    c.saveLayer(None, None)
    cover(c, img, z, ox + drift[0] * u, oy + drift[1] * u)
    m = skia.Paint(BlendMode=skia.BlendMode.kDstIn)
    m.setShader(skia.GradientShader.MakeRadial((fx, fy), fr * 1.5, [skia.Color4f(0, 0, 0, 1), skia.Color4f(0, 0, 0, 1), skia.Color4f(0, 0, 0, 0)], [0, 0.45, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), m); c.restore()


_DUST = np.random.default_rng(11).uniform(0, 1, (70, 5))


def dust(c, t, a=0.5):
    for (x, y, s, sp, ph_) in _DUST:
        xx = (x * W + 30 * math.sin(t * 0.4 + ph_ * 6)) % W; yy = (y * H - t * 25 * (0.4 + sp)) % H
        c.drawCircle(xx, yy, 1.2 + 2.8 * s, P((255, 240, 220), a * (0.25 + 0.5 * s) * (0.6 + 0.4 * math.sin(t * 2 + ph_ * 9))))


def light_leak(c, t, t0, d=0.7, col=(255, 150, 80)):
    u = (t - t0) / d
    if not 0 <= u <= 1: return
    a = math.sin(u * math.pi) * 0.55; x = -300 + u * (W + 600)
    sh = skia.GradientShader.MakeRadial((x, H * 0.35), 700, [skia.Color4f(col[0] / 255, col[1] / 255, col[2] / 255, a), skia.Color4f(0, 0, 0, 0)], [0, 1])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kScreen))


def spotlight(c, cx, cy, r, a=0.65):
    sh = skia.GradientShader.MakeRadial((cx, cy), r, [skia.Color4f(0, 0, 0, 0), skia.Color4f(0, 0, 0, a)], [0.35, 1])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))


def bg_dark(c, col=(16, 14, 20)):
    c.drawRect(skia.Rect.MakeWH(W, H), P(col))
    sh = skia.GradientShader.MakeRadial((W / 2, H * 0.48), H * 0.6, [skia.Color4f(ACC_D[0] / 255, ACC_D[1] / 255, ACC_D[2] / 255, 0.55), skia.Color4f(0, 0, 0, 0)], [0, 1])
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=sh))


# ---------------------------------------------------------------- line-art props (same ink style as the patent)
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


def cart_line(c, cx, cy, s, col=OFFW, a=1.0, fill=0.0):
    """modern cart in the same ink style; fill 0..1 stacks goods inside"""
    c.save(); c.translate(cx, cy); c.scale(s, s)
    st = S(col, 7, a); thin = S(col, 3, a * 0.55)
    p = skia.Path(); p.moveTo(-300, -200); p.lineTo(260, -200); p.lineTo(200, 80); p.lineTo(-250, 80); p.close()
    if fill > 0:
        cols = [(200, 70, 60), (236, 196, 110), (90, 150, 210), (120, 190, 120), (230, 150, 70), (190, 120, 200), (230, 220, 200), (160, 60, 60)]
        n = int(24 * fill)
        c.save(); c.clipPath(p, doAntiAlias=True)
        for i in range(n):
            bx = -280 + (i % 6) * 92; by = 70 - (i // 6) * 75 - 70
            c.drawRRect(rr(bx, by, 84, 70, 8), P(cols[(i * 5) % 8], a)); c.drawRRect(rr(bx, by, 84, 70, 8), S((20, 20, 20), 2, a))
        c.restore()
        for i in range(max(0, n - 24)): pass
    for i in range(1, 11):
        x0 = -300 + i * 560 / 11; x1 = -250 + i * 450 / 11; c.drawLine(x0, -200, x1, 80, thin)
    for j in range(1, 4):
        y = -200 + j * 70; c.drawLine(-300 + 50 * j * 70 / 280, y, 260 - 60 * j * 70 / 280, y, thin)
    c.drawPath(p, st)
    c.drawLine(260, -200, 330, -290, st); c.drawLine(330, -290, 400, -290, S(col, 10, a))
    c.drawLine(-230, 80, -200, 210, st); c.drawLine(180, 80, 150, 210, st); c.drawLine(-230, 150, 170, 150, st)
    for wx in (-190, 140): c.drawCircle(wx, 235, 26, st)
    c.restore()


def draw_on(c, img, glow, cx, cy, w, k, t):
    """patent drawing reveals with a glowing scan line"""
    if img is None: return
    h = w * img.height() / img.width(); x0, y0 = cx - w / 2, cy - h / 2; yc = y0 + h * eo(k)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x0 - 20, y0 - 20, w + 40, yc - y0 + 20))
    if glow is not None: c.drawImageRect(glow, skia.Rect.MakeXYWH(x0, y0, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(Alphaf=0.9))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x0, y0, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True))
    c.restore()
    if k < 1:
        g = skia.GradientShader.MakeLinear([(0, yc - 40), (0, yc + 6)], [skia.Color4f(0.6, 0.4, 1, 0), skia.Color4f(0.85, 0.75, 1, 0.9)], [0, 1])
        c.drawRect(skia.Rect.MakeXYWH(x0 - 40, yc - 40, w + 80, 46), skia.Paint(Shader=g, BlendMode=skia.BlendMode.kScreen))


def counter_big(c, val, x, y, size, k, suffix='', prefix='', col=OFFW):
    v = int(round(val * eo(k))); s = prefix + str(v) + suffix; f = cond(size); w = f.measureText(s)
    c.drawString(s, x - w / 2, y, f, glow_paint(col))


def kb(t, t0, t1, z0=1.0, z1=1.12): return z0 + (z1 - z0) * cl((t - t0) / max(0.01, t1 - t0))


# ---------------------------------------------------------------- beats
def s_hook(c, t):                       # context lean: the thing everyone knows
    i = 0
    focus_photo(c, MOD_S[i], MOD_B[i], t, 0, 3, 1.05, 1.18, 0.0, 0.1, fx=540, fy=980, fr=560, drift=(0.15, 0))
    spotlight(c, 540, 980, 1100, 0.55)
    kword2(c, T, t, 0.0, ph('but when') - 0.05, 540, 1360, 64)


def s_nobody(c, t):                     # snapback: nobody would touch it
    t0 = SC[1][0]; tn = ph('nobody')
    focus_photo(c, ARCH_S[0], ARCH_B[0], t, t0, t0 + 3, 1.1, 1.2, -0.1, 0.0, fx=540, fy=960, fr=500, drift=(-0.2, 0))
    spotlight(c, 540, 960, 1000, 0.6)
    if t >= tn - 0.05: rgb_split(c, lambda cc: ghost_word(cc, 'NOBODY', 540, 760, 230, 1.0, OFFW, 0.95, -0.03, 'ArchivoCond-Black'), 14 * (1 - cl((t - tn) / 0.4)))
    kword2(c, T, t, t0, ph('so the inventor') - 0.05, 540, 1360, 60)


def s_fake(c, t):                       # the wow, inside 5 s
    t0 = SC[2][0]; tf = ph('fake')
    focus_photo(c, ARCH_S[1 % len(ARCH_S)], ARCH_B[1 % len(ARCH_B)], t, t0, t0 + 2.5, 1.2, 1.32, 0.2, 0.1, fx=540, fy=980, fr=420, drift=(0.25, 0))
    c.drawRect(skia.Rect.MakeWH(W, H), P((30, 10, 50), 0.35))
    kword2(c, T, t, t0, tf - 0.05, 540, 760, 62)
    if t >= tf - 0.05:
        k = pr(t, tf - 0.05, 0.18); stamp_box(c, 'FAKE SHOPPERS', 540, 980, 130, k)


def stamp_box(c, txt, x, y, size, k, col=None):
    col = col or ACC
    if k <= 0: return
    f = cond(size); w = f.measureText(txt); s = 1.6 - 0.6 * eo(k)
    c.save(); c.translate(x, y); c.rotate(-6); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 - 30, -size * 0.95, w + 60, size * 1.2), P(col, 0.92 * eo(k)))
    c.drawString(txt, -w / 2, 0, f, P((244, 238, 228), eo(k))); c.restore()


def s_1937(c, t):                       # setting + character
    t0 = SC[3][0]; to = ph('oklahoma'); tg = ph('goldman')
    if t < to - 0.08:
        rolodex(c, W / 2, H / 2 - 40, '1937', pr(t, t0 + 0.05, 0.3), t)
    else:
        focus_photo(c, ARCH_S[2 % len(ARCH_S)], ARCH_B[2 % len(ARCH_B)], t, to, to + 3.5, 1.15, 1.3, 0.0, 0.0, fx=540, fy=940, fr=480, drift=(0.2, 0.05))
        spotlight(c, 540, 940, 1000, 0.6)
        ghost_word(c, 'OKLAHOMA CITY', 540, 700, 110, pr(t, to - 0.05, 0.25), OFFW, 0.95, -0.02, 'ArchivoCond-Black')
        if t >= tg - 0.3: name_box(c, 'SYLVAN GOLDMAN · GROCER', 540, 1240, 56, pr(t, tg - 0.3, 0.22), ACC)
        else: kword2(c, T, t, ph('a grocer'), tg - 0.3, 540, 1240, 58)


def s_heavy(c, t):                      # the problem, made physical
    t0 = SC[4][0]; th = ph('heavy')
    bg_dark(c)
    k = pr(t, t0 + 0.1, th - t0)
    basket(c, 540, 1160 + 40 * eo(pr(t, th - 0.2, 0.4)), 1.3, k, sag=eo(pr(t, th - 0.2, 0.4)))
    dust(c, t, 0.4)
    kword2(c, T, t, t0, th + 0.3, 540, 470, 60, maxw=820)
    if t >= th - 0.05: stamp_box(c, 'STOP.', 540, 1430, 110, pr(t, th - 0.05, 0.2), (200, 50, 50))


def s_wheels(c, t):                     # the invention: patent draws itself
    t0 = SC[5][0]; tw = ph('wheels')
    bg_dark(c, (12, 12, 24))
    for i in range(0, W, 60): c.drawLine(i, 0, i, H, S((120, 100, 200), 1, 0.12))
    for j in range(0, H, 60): c.drawLine(0, j, W, j, S((120, 100, 200), 1, 0.12))
    draw_on(c, PAT, PAT_GLOW, 540, 1000, 780, pr(t, t0 + 0.05, max(0.8, tw - t0 + 0.2)), t)
    if PAT is None: cart_line(c, 540, 1000, 1.2)
    g = mono(30); s_ = 'U.S. PATENT 2,196,914 · S. N. GOLDMAN'
    c.drawString(s_, 540 - g.measureText(s_) / 2, 1500, g, P((200, 180, 255), 0.85 * pr(t, t0 + 0.4, 0.4)))
    kword2(c, T, t, t0, tw + 0.4, 540, 470, 64)


def s_flop(c, t):                       # rejection: two halves
    t0 = SC[6][0]; tm = ph('men said'); tw = ph('women said')
    if t < tm - 0.08:
        bg_dark(c, (8, 8, 10)); ghost_word(c, 'NOBODY WANTED IT.', 540, 960, 120, pr(t, t0, 0.2), OFFW, 0.95, -0.02, 'ArchivoCond-Black'); return
    top = skia.Rect.MakeXYWH(0, 0, W, H / 2); bot = skia.Rect.MakeXYWH(0, H / 2, W, H / 2)
    cover(c, ARCH_S[3 % len(ARCH_S)], kb(t, tm, tm + 3, 1.15, 1.25), -0.2, 0.0, rect=top)
    if t >= tw - 0.08: cover(c, ARCH_S[4 % len(ARCH_S)], kb(t, tw, tw + 3, 1.15, 1.25), 0.2, 0.0, rect=bot)
    else: c.drawRect(bot, P((10, 10, 12)))
    c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.4)); c.drawLine(0, H / 2, W, H / 2, S((0, 0, 0), 10))
    ghost_word(c, '"LOOKS WEAK."', 540, 760, 110, pr(t, ph('weak') - 0.1, 0.2), OFFW, 0.97, -0.02, 'ArchivoCond-Black')
    if t >= tw - 0.08: ghost_word(c, '"ANOTHER STROLLER."', 540, 1250, 100, pr(t, ph('strollers') - 0.1, 0.2), OFFW, 0.97, -0.02, 'ArchivoCond-Black')


def s_models(c, t):                     # the move
    t0 = SC[7][0]; ta = ph('actors'); tp = ph('pretending')
    imgs = MOD_S[1 % len(MOD_S)] if t < ta else ARCH_S[0]
    focus_photo(c, ARCH_S[0], ARCH_B[0], t, t0, t0 + 4.5, 1.25, 1.45, 0.0, 0.0, fx=540, fy=980, fr=460, drift=(0.35, 0.0))
    spotlight(c, 540, 980, 900, 0.6); light_leak(c, t, t0, 0.8)
    tag_boxes(c, ['Models.', 'Actors.', 'Pretending to shop.'], 140, 760, 70,
              [pr(t, ph('models') - 0.1, 0.18), pr(t, ta - 0.1, 0.18), pr(t, tp - 0.1, 0.18)])


def s_copied(c, t):                     # proof + payoff
    t0 = SC[8][0]; tc = ph('copied'); tw = ph('within weeks'); tm = ph('multimillionaire')
    if t < tw - 0.08:
        photo_wall(c, ARCH_S + MOD_S[:1], t, t0, pr(t, t0, tw - t0 + 0.6)); c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 0.4))
        kword2(c, T, t, t0, tw - 0.08, 540, 960, 66)
    else:
        bg_dark(c)
        n = 1 + int(5 * eo(pr(t, tw, 1.0)))
        for i in range(n):
            cart_line(c, 180 + (i % 3) * 360, 820 + (i // 3) * 420, 0.42, OFFW, 0.85)
        if t >= tm - 0.1: stamp_box(c, 'MULTIMILLIONAIRE', 540, 1500 - 120, 96, pr(t, tm - 0.1, 0.2), (200, 160, 60))
        else: kword2(c, T, t, tw - 0.08, tm - 0.1, 540, 560, 62)


def s_twist(c, t):                      # re-hook
    t0 = SC[9][0]
    c.drawRect(skia.Rect.MakeWH(W, H), P((6, 6, 8))); dust(c, t, 0.35)
    kword2(c, T, t, t0, ph('carts today') - 0.05, 540, 960, 78)


def s_bigger(c, t):                     # scale
    t0 = SC[10][0]; t3 = ph('three')
    bg_dark(c, (14, 12, 18))
    k = pr(t, t3 - 0.2, 0.7)
    cart_line(c, 300, 1150, 0.45, (200, 180, 255), 0.9)
    body(c, '1937', 250, 1330, 40, (200, 180, 255), 'Bold')
    cart_line(c, 700, 1150 - 100 * eo(k), 0.45 + 0.75 * eo(k), OFFW, 1.0)
    body(c, 'TODAY', 640, 1430, 40, OFFW, 'Bold', a=k)
    if t >= t3 - 0.1: ghost_word(c, '~3x BIGGER', 540, 560, 130, pr(t, t3 - 0.1, 0.2), OFFW, 0.97, -0.02, 'ArchivoCond-Black')
    else: kword2(c, T, t, t0, t3 - 0.1, 540, 560, 64)


def s_forty(c, t):                      # the number that makes it about YOU
    t0 = SC[11][0]; td = ph('doubled'); tf = ph('forty')
    bg_dark(c)
    cart_line(c, 540, 1180, 1.05, OFFW, 1.0, fill=0.45 + 0.55 * eo(pr(t, tf - 0.1, 1.0)) if t >= tf - 0.1 else 0.45 * eo(pr(t, td, 0.8)))
    if t >= tf - 0.1:
        counter_big(c, 40, 540, 720, 260, pr(t, tf - 0.1, 0.8), '%', '+', OFFW)
        body(c, 'MORE BOUGHT (MARKETING EXPERIMENT, M. LINDSTROM)', 150, 790, 26, (190, 180, 210), 'SemiBold', a=pr(t, tf, 0.4))
    else: kword2(c, T, t, t0, tf - 0.1, 540, 640, 62, maxw=800)


def s_mirror(c, t):                     # the line they'll remember
    t0 = SC[12][0]; tc = ph('a cart never')
    top = skia.Rect.MakeXYWH(0, 0, W, H / 2); bot = skia.Rect.MakeXYWH(0, H / 2, W, H / 2)
    c.drawRect(top, P((18, 16, 22))); c.drawRect(bot, P((30, 16, 48)))
    basket(c, 540, 600, 0.8, 1.0, 0.0, OFFW, pr(t, t0, 0.2))
    ghost_word(c, 'A BASKET SAYS STOP.', 540, 860, 84, pr(t, t0 + 0.1, 0.2), OFFW, 0.98, -0.02, 'ArchivoCond-Black')
    if t >= tc - 0.08:
        cart_line(c, 540, 1350, 0.62, OFFW, pr(t, tc - 0.08, 0.2), fill=1.0)
        ghost_word(c, 'A CART NEVER DOES.', 540, 1080, 84, pr(t, tc - 0.08, 0.2), (210, 180, 255), 0.98, -0.02, 'ArchivoCond-Black')
    c.drawLine(0, H / 2, W, H / 2, S((0, 0, 0), 8))


def s_send(c, t):                       # share trigger + brand lockup
    t0 = SC[13][0]
    c.drawRect(skia.Rect.MakeWH(W, H), P((236, 230, 218)))
    cart_line(c, 540, 860, 0.8, (30, 30, 30), 1.0, fill=0.25)
    kword2(c, T, t, t0, END, 540, 1180, 60, col=(30, 30, 30), maxw=860)
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
FLASH = {2, 6, 9, 12}

# richer grade than the faded v2: keep deep blacks, warm highs, cool shadows, 22% desat
GRADE4 = grade_filter(desat=0.22, lift=0.03, gain=0.95, cool=0.025)


def frame(t):
    s = skia.Surface(W, H); c = s.getCanvas()
    i = max(j for j, (t0, _) in enumerate(SC) if t >= t0); t0 = SC[i][0]
    gp = skia.Paint(); gp.setColorFilter(GRADE4); c.saveLayer(None, gp)
    w = whip(t, t0, 0.12) if i > 0 else 0.0
    if w > 0:
        c.save(); c.translate(W * 0.18 * w * (1 if i % 2 else -1), 0)
        p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(70 * w, 0.5)); c.saveLayer(None, p); SC[i][1](c, t); c.restore(); c.restore()
    else: SC[i][1](c, t)
    if i in FLASH: flash(c, t, t0, 0.06, 0.55)
    if i not in LIGHT: light_leak(c, t, t0, 0.6, (255, 160, 90) if i % 2 else (180, 120, 255))
    c.restore()
    halation(s, 0.24, 26); soft_edges(s, 7.0)
    if i not in LIGHT: dust(c, t, 0.3)
    film(c, t, 0.065, 0.35 if i in LIGHT else 0.72)
    brand_badge(c)
    if i not in LIGHT and t > 0.8: series_tag(c, SERIES, NUM, ACC, t, DUR, dark=True)
    return s


def cover_fn(c):
    s = skia.Surface(W, H); cc = s.getCanvas(); gp = skia.Paint(); gp.setColorFilter(GRADE4); cc.saveLayer(None, gp)
    focus_photo(cc, ARCH_S[0], ARCH_B[0], 0, 0, 1, 1.2, 1.2, 0, 0, fx=540, fy=980, fr=460)
    spotlight(cc, 540, 980, 900, 0.6)
    f = cap2(76); s_ = 'Nobody wanted this. So he'; draw_tight(cc, s_, 540 - tight_w(s_, f) / 2, 720, f, glow_paint())
    stamp_box(cc, 'HIRED FAKE SHOPPERS', 540, 920, 110, 1.0); cc.restore()
    halation(s, 0.24, 26); film(cc, 0, 0.065, 0.72); brand_badge(cc); series_tag(cc, SERIES, NUM, ACC, 0, 1)
    c.drawImage(s.makeImageSnapshot(), 0, 0)


if __name__ == '__main__': main(HERE, frame, cover_fn, DUR)
