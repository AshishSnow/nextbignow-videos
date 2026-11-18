"""ep67 'GTA 6 Is About To Make People Rich' - painted neon Vice-City-sunset look, all drawn in code (no game footage, no logos).
Draws in a 1080x1920 design space; SCALE env renders natively larger (YT = 1440x2560).
usage: paint_gta6.py <dir> [still t1 t2 ...]   env PLAT=ig|yt"""
import os, sys, json, math, random, subprocess, re
import numpy as np, skia

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
PLAT = os.environ.get('PLAT', 'ig')
SC = 1440 / 1080 if PLAT == 'yt' else 1.0
OW, OH = int(W * SC), int(H * SC)
T = json.load(open(os.path.join(D, 'times.json')))
S = [t[0] for t in T]; E = [t[1] for t in T]
raw = [[re.sub(r'\(\d\)', '', w), x, y] for w, x, y in json.load(open(os.path.join(D, 'align.json'))) if w not in ('<s>', '</s>', '<sil>')]
WORDS, i = [], 0                                     # merge spelled "g t a" -> GTA, numbers back to digits for subs
NUM = {'six': '6', 'five': '5'}
while i < len(raw):
    w = raw[i]
    if w[0] == 'g' and i + 2 < len(raw) and raw[i + 1][0] == 't' and raw[i + 2][0] == 'a':
        nxt = raw[i + 3][0] if i + 3 < len(raw) else ''
        if nxt in NUM or nxt in ("five's",):
            WORDS.append(['GTA ' + NUM.get(nxt, "5's"), w[1], raw[i + 3][2]]); i += 4; continue
        WORDS.append(['GTA', w[1], raw[i + 2][2]]); i += 3; continue
    WORDS.append(w); i += 1
DUR = E[-1] + 1.8
SUBY = 1500 if PLAT == 'yt' else 1430
FX = os.path.join(HERE, '..', 'fonts'); FD = '/usr/share/fonts/opentype/inter/'


def F(p, s):
    f = skia.Font(skia.Typeface.MakeFromFile(p), s); f.setEdging(skia.Font.Edging.kAntiAlias); return f


ANTON = os.path.join(FX, 'Anton.ttf')
SMALL = F(FD + 'Inter-Bold.otf', 34)
SUBF = F(FD + 'InterDisplay-Bold.otf', 36)
LBL = F(FD + 'InterDisplay-Black.otf', 40)


def col(c, a=1.0): return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(255 * max(0, min(1, a))))
def cl(x): return max(0.0, min(1.0, x))
def ss(a, b, x):
    k = cl((x - a) / (b - a)) if b != a else float(x >= a); return k * k * (3 - 2 * k)
def back(a, b, x):  # ease-out-back for pops (still eased over ~10 frames)
    k = cl((x - a) / (b - a)); s = 1.6; k -= 1; return k * k * ((s + 1) * k + s) + 1
def P(c, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor(col(c, a)); return p
def blur(p, r): p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, r)); return p


PINK, MAG, PURP, DEEP, ORNG, YEL, TEAL, CREAM = (255, 92, 168), (230, 40, 140), (110, 40, 170), (28, 12, 60), (255, 140, 60), (255, 214, 64), (40, 230, 220), (255, 244, 230)
GREEN = (60, 220, 120)

# ---------- grain + watermark ----------
rng = np.random.default_rng(3)
from scipy import ndimage
g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
tex = np.clip(128 + g * 9 + ndimage.gaussian_filter(rng.normal(0, 1, (H // 2, W // 2)), (0.6, 6)) * 20, 0, 255).astype(np.uint8)
tex = np.repeat(np.repeat(tex, 2, 0), 2, 1)
GRAIN = skia.Image.fromarray(np.dstack([tex, tex, tex, np.full_like(tex, 255)]), colorType=skia.kRGBA_8888_ColorType)
WM = skia.Image.open(os.path.join(HERE, 'brand_logo_port.png'))


def grain(c, a=0.16):
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kOverlay); p.setAlphaf(a); c.drawImage(GRAIN, 0, 0, skia.SamplingOptions(), p)


def vgrad(c, cols, stops=None, y0=0, y1=H):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([(0, y0), (0, y1)], [col(x) for x in cols], stops)); c.drawRect(skia.Rect.MakeLTRB(-60, y0, W + 60, y1), p)


def glow(c, x, y, r, cc, a):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((x, y), r, [col(cc, a), col(cc, a * .3), col(cc, 0)], [0, .4, 1])); c.drawCircle(x, y, r, p)


# ---------- scenery ----------
def retro_sun(c, x, y, r, t, a=1.0):
    glow(c, x, y, r * 2.4, (255, 120, 90), .45 * a)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([(0, y - r), (0, y + r)], [col((255, 230, 120), a), col((255, 90, 150), a)]))
    c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, W, y + r * .15))
    c.drawCircle(x, y, r, p)
    for k in range(7):                                                   # stripes drift down (motion, not static)
        yy = y - r * .05 + ((k * 34 + t * 18) % 240)
        c.drawRect(skia.Rect.MakeLTRB(x - r, yy, x + r, yy + 4 + k * 1.6), P((60, 20, 80), a))
    c.restore()


def skyline(c, base, seed, h0, h1, colr, lit, t, a=1.0, wins=True):
    rnd = random.Random(seed); x = -40
    while x < W + 40:
        w = rnd.uniform(60, 150); h = rnd.uniform(h0, h1)
        c.drawRect(skia.Rect.MakeLTRB(x, base - h, x + w, base + 2), P(colr, a))
        if wins:
            for wy in range(int(base - h + 18), int(base - 10), 26):
                for wx in range(int(x + 10), int(x + w - 12), 22):
                    if rnd.random() < .42:
                        fl = .55 + .45 * math.sin(t * 1.3 + wx * .7 + wy)
                        c.drawRect(skia.Rect.MakeXYWH(wx, wy, 9, 12), P(lit, a * fl * .9))
        x += w + rnd.uniform(2, 14)


def palm(c, x, y, s, t, a=1.0, cc=(30, 8, 40), lean=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    sway = math.sin(t * 1.1 + x) * 3
    trunk = skia.Path(); trunk.moveTo(-14, 0); trunk.cubicTo(-10 + lean * 40, -200, 20 + lean * 90, -380, 30 + lean * 110 + sway, -520)
    trunk.lineTo(44 + lean * 110 + sway, -516); trunk.cubicTo(32 + lean * 90, -380, 6 + lean * 40, -200, 14, 0); trunk.close()
    c.drawPath(trunk, P(cc, a))
    hx, hy = 37 + lean * 110 + sway, -520
    for k in range(7):
        ang = -170 + k * 30 + math.sin(t * 1.5 + k) * 4
        rad = math.radians(ang); L = 210 if k in (0, 6) else 250
        tipx, tipy = hx + math.cos(rad) * L, hy + math.sin(rad) * L * .55 + 70
        f = skia.Path(); f.moveTo(hx, hy)
        f.quadTo(hx + math.cos(rad) * L * .5, hy + math.sin(rad) * L * .5 - 50, tipx, tipy)
        f.quadTo(hx + math.cos(rad) * L * .45, hy + math.sin(rad) * L * .45 - 10, hx, hy + 10); f.close()
        c.drawPath(f, P(cc, a))
    c.restore()


def ocean(c, y, t, a=1.0):
    vgrad(c, [(80, 30, 120), (20, 10, 50)], None, y, H)
    for k in range(14):
        yy = y + 8 + k * k * 4.2; w = 140 + k * 30
        for j in range(5):
            xx = (j * 260 + k * 90 + t * (12 + k * 3)) % (W + 300) - 150
            c.drawRect(skia.Rect.MakeXYWH(xx, yy, w * .5, 2 + k * .35), P((255, 140, 170), a * (.55 - k * .03)))


def money(c, t, seed, n, a=1.0, speed=1.0, y0=H + 80):
    rnd = random.Random(seed)
    for i in range(n):
        z = rnd.random(); x = rnd.uniform(40, W - 40); ph = rnd.uniform(0, 30)
        y = y0 - ((t * (70 + 120 * z) * speed + ph * 60) % (H + 300))
        s = .5 + z * .9; rot = math.sin(t * 2 + i) * 25 + rnd.uniform(-30, 30)
        c.save(); c.translate(x + math.sin(t + i) * 30, y); c.rotate(rot); c.scale(s, s)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-46, -24, 46, 24), 5, 5), P((90, 190, 110), a * (.5 + .5 * z)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-38, -17, 38, 17), 4, 4), P((60, 150, 85), a * (.5 + .5 * z)))
        c.drawCircle(0, 0, 11, P((150, 230, 160), a * (.5 + .5 * z)))
        c.restore()


def neon(c, s, y, size, k, top=CREAM, bot=PINK, glowc=MAG, x=None, sk=0.0):
    if k <= 0: return
    a = ss(0, 1, k); sc = .86 + .14 * back(0, 1, k)
    f = F(ANTON, size); w = f.measureText(s); xx = (W / 2 - w / 2) if x is None else x
    c.save(); c.translate(W / 2 if x is None else x + w / 2, y - size * .35); c.scale(sc, sc); c.skew(sk, 0); c.translate(-(W / 2 if x is None else x + w / 2), -(y - size * .35))
    g = P(glowc, .75 * a); blur(g, 22); c.drawString(s, xx, y, f, g)
    o = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * .07, StrokeJoin=skia.Paint.kRound_Join); o.setColor(col((40, 10, 50), a))
    c.drawString(s, xx, y, f, o)
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([(0, y - size * .75), (0, y)], [col(top, a), col(bot, a)])); c.drawString(s, xx, y, f, p)
    c.restore()


def small(c, s, y, k, cc=CREAM, f=None):
    if k <= 0: return
    f = f or SMALL; a = ss(0, 1, k); x = W / 2 - f.measureText(s) / 2
    sh = P((0, 0, 0), .5 * a); blur(sh, 6); c.drawString(s, x + 2, y + 4 + 12 * (1 - a), f, sh)
    c.drawString(s, x, y + 12 * (1 - a), f, P(cc, a))


def card(c, cx, cy, w, h, k, rot=0.0, fill=(255, 255, 255), r=34, tilt=0.0):
    """floating card with soft shadow + subtle 3D tilt (perspective)."""
    if k <= 0: return False
    a = ss(0, 1, k); sc = .7 + .3 * back(0, 1, k)
    c.save(); c.translate(cx, cy + 60 * (1 - a)); c.rotate(rot); c.scale(sc, sc)
    m = skia.Matrix(); m.setAll(1, 0, 0, 0, 1, 0, tilt * 0.000008, 0, 1); c.concat(m)
    sh = P((10, 0, 30), .45 * a); blur(sh, 30); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2 + 10, -h / 2 + 30, w / 2 + 10, h / 2 + 40), r, r), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), r, r), P(fill, a))
    return True


def chip(c, s, x, y, bg, fg=(255, 255, 255), a=1.0, f=None):
    f = f or SMALL; w = f.measureText(s) + 40
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - 34, w, 50), 25, 25), P(bg, a)); c.drawString(s, x - w / 2 + 20, y + 1, f, P(fg, a))


def person(c, x, y, s, cc, kind, t, a=1.0):
    """generic silhouettes: cop / robber / driver / streamer (no real people)."""
    c.save(); c.translate(x, y); c.scale(s, s); p = P(cc, a)
    bob = math.sin(t * 3 + x) * 3
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-60, -170 + bob, 60, 0), 40, 40), p)           # body
    c.drawCircle(0, -215 + bob, 46, p)                                                                     # head
    if kind == 'cop':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-54, -272 + bob, 54, -238 + bob), 10, 10), P((30, 60, 160), a))
        c.drawRect(skia.Rect.MakeLTRB(-62, -246 + bob, 62, -236 + bob), P((20, 40, 120), a))
        c.drawCircle(-28, -120 + bob, 13, P(YEL, a))
    elif kind == 'robber':
        c.drawRect(skia.Rect.MakeLTRB(-46, -232 + bob, 46, -206 + bob), P((20, 10, 25), a))
        c.drawCircle(-17, -219 + bob, 7, P(CREAM, a)); c.drawCircle(17, -219 + bob, 7, P(CREAM, a))
        c.drawCircle(78, -60 + bob, 44, P((90, 70, 50), a)); c.drawString('$', 62, -42 + bob, F(ANTON, 50), P(GREEN, a))
    elif kind == 'driver':
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-52, -268 + bob, 52, -236 + bob), 12, 12), P(YEL, a))
    elif kind == 'streamer':
        c.drawArc(skia.Rect.MakeLTRB(-58, -275 + bob, 58, -160 + bob), 180, 180, False, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=12, Color=col((20, 20, 30), a)))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-70, -232 + bob, -48, -190 + bob), 8, 8), P((20, 20, 30), a))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(48, -232 + bob, 70, -190 + bob), 8, 8), P((20, 20, 30), a))
    c.restore()


def taxi(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -70, 150, 0), 26, 26), P(YEL, a))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-90, -125, 80, -60), 26, 26), P(YEL, a))
    c.drawRect(skia.Rect.MakeLTRB(-70, -112, -10, -70), P((60, 120, 170), a)); c.drawRect(skia.Rect.MakeLTRB(2, -112, 62, -70), P((60, 120, 170), a))
    c.drawRect(skia.Rect.MakeLTRB(-30, -150, 20, -128), P(CREAM, a))
    for wx in (-90, 90): c.drawCircle(wx, 0, 32, P((25, 15, 30), a)); c.drawCircle(wx, 0, 13, P((120, 120, 130), a))
    c.restore()


def chat(c, t, t0, x0, n, a=1.0, seed=4):
    rnd = random.Random(seed); msgs = ['W', 'LMAO', 'no way', 'clip it', 'GG', 'insane', '+1', 'LOL', 'ICONIC', 'run!!']
    cols = [PINK, TEAL, YEL, GREEN, ORNG, (170, 140, 255)]
    for i in range(n):
        st = t0 + i * .33
        if t < st: break
        k = t - st; y = 1240 - k * 120
        if y < 380: continue
        m = msgs[rnd.randrange(len(msgs))]; cc = cols[i % len(cols)]; f = SMALL
        w = f.measureText(m) + 40; x = x0 + rnd.uniform(-40, 40)
        al = a * ss(0, .25, k) * (1 - ss(5.5, 7, k))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - 36, w, 52), 24, 24), P((25, 10, 45), .78 * al))
        c.drawString(m, x + 20, y, f, P(cc, al))


def phone(c, cx, cy, s, a, t, screen='live', rot=0.0):
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    sh = P((10, 0, 30), .45 * a); blur(sh, 26); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-150, -280, 170, 320), 46, 46), sh)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-160, -300, 160, 300), 46, 46), P((22, 14, 34), a))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-146, -286, 146, 286), 36, 36))
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([(0, -286), (0, 286)], [col((255, 120, 90), a), col((120, 40, 170), a)])); c.drawRect(skia.Rect.MakeLTRB(-146, -286, 146, 286), p)
    if screen == 'live':
        person(c, 0, 280, .9, (30, 10, 45), 'streamer', t, a)
        chip(c, 'LIVE', -80, -220, (230, 30, 60), a=a)
    elif screen == 'video':
        c.drawCircle(0, -10, 70, P((255, 255, 255), .92 * a))
        tri = skia.Path(); tri.moveTo(-22, -45); tri.lineTo(38, -10); tri.lineTo(-22, 25); tri.close(); c.drawPath(tri, P((230, 40, 80), a))
        c.drawRect(skia.Rect.MakeLTRB(-130, 230, -130 + 260 * ((t * .3) % 1), 238), P((230, 40, 80), a))
    elif screen == 'clip':
        for k in range(3): c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-120 + k * 84, -60, 72, 120), 12, 12), P(CREAM, (.5 + .2 * k) * a))
        c.drawString('0:15', -40, 140, F(ANTON, 60), P(CREAM, a))
    c.restore(); c.restore()


def bars(c, k, kb, a=1.0):
    """GTA 5 record vs GTA 6 forecast, day one copies."""
    base, x1, x2, bw = 1260, 300, 640, 220
    h1 = 220 * ss(0, 1, k); h2 = 760 * ss(0, 1, kb)
    c.drawRect(skia.Rect.MakeLTRB(120, base, W - 120, base + 6), P(CREAM, .6 * a))
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([(0, base - 220), (0, base)], [col((180, 170, 220), a), col((110, 90, 170), a)]))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x1 - bw / 2, base - h1, x1 + bw / 2, base), 14, 14), p)
    if kb > 0:
        g = P(PINK, .6 * a); blur(g, 30); c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x2 - bw / 2, base - h2, x2 + bw / 2, base), 14, 14), g)
        p2 = skia.Paint(AntiAlias=True); p2.setShader(skia.GradientShader.MakeLinear([(0, base - 760), (0, base)], [col(YEL, a), col(MAG, a)]))
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x2 - bw / 2, base - h2, x2 + bw / 2, base), 14, 14), p2)
    f = F(ANTON, 64)
    if k > .3:
        s = '11M'; c.drawString(s, x1 - f.measureText(s) / 2, base - h1 - 24, f, P(CREAM, a * ss(.3, .8, k)))
    if kb > .2:
        s = '%dM' % round(45 * ss(0, 1, kb)); c.drawString(s, x2 - f.measureText(s) / 2, base - h2 - 24, f, P(YEL, a))
    for s, x in (('GTA 5 RECORD', x1), ('GTA 6 FORECAST', x2)):
        c.drawString(s, x - SMALL.measureText(s) / 2, base + 60, SMALL, P(CREAM, a))


def wave(c, t, k, a=1.0):
    """big neon wave + a surfer riding it."""
    crest = 1000 - 220 * ss(0, 1, k)
    path = skia.Path(); path.moveTo(-50, H)
    pts = []
    for i in range(0, 61):
        x = -50 + i * (W + 100) / 60
        y = crest + 140 * math.sin(i / 60 * math.pi * 1.2 + t * .8) * (1 - i / 80) + (i / 60) ** 2 * 260
        pts.append((x, y)); path.lineTo(x, y)
    path.lineTo(W + 50, H); path.close()
    p = skia.Paint(AntiAlias=True); p.setShader(skia.GradientShader.MakeLinear([(0, crest - 150), (0, H)], [col(TEAL, a), col((40, 60, 160), a), col(DEEP, a)], [0, .4, 1])); c.drawPath(path, p)
    foam = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=14, StrokeCap=skia.Paint.kRound_Cap); foam.setColor(col(CREAM, .9 * a))
    fp = skia.Path(); fp.moveTo(*pts[0])
    for q in pts[1:]: fp.lineTo(*q)
    c.drawPath(fp, foam)
    gx = 540 + math.sin(t * 1.2) * 40; gy = min(q[1] for q in pts[25:35]) - 10
    c.save(); c.translate(gx, gy); c.rotate(-12 + math.sin(t * 1.6) * 5)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-120, -12, 120, 12), 12, 12), P(PINK, a))
    person(c, 0, -10, .55, (30, 10, 45), 'none', t, a)
    c.restore()


def screens(c, t, k, a=1.0):
    """city of glowing phone screens lighting up = viewers."""
    rnd = random.Random(8)
    for i in range(140):
        x = rnd.uniform(60, W - 60); y = rnd.uniform(420, 1300); on = ss(i / 140 * .8, i / 140 * .8 + .2, k)
        if on <= 0: continue
        s = .25 + rnd.random() * .25
        cc = [PINK, TEAL, YEL, ORNG][i % 4]
        glow(c, x, y, 70 * s * 2, cc, .35 * on * a)
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 40 * s, y - 70 * s, 80 * s, 140 * s), 12 * s, 12 * s), P(cc, on * a * .95))


def subs(c, t):
    chunks, chunk = [], []
    for w in WORDS:
        if chunk and any(chunk[-1][1] < s0 - .05 <= w[1] for s0 in S): chunks.append(chunk); chunk = []
        chunk.append(w)
        if len(chunk) >= 5: chunks.append(chunk); chunk = []
    if chunk: chunks.append(chunk)
    show = None
    for i, ch in enumerate(chunks):
        nb = chunks[i + 1][0][1] if i + 1 < len(chunks) else ch[-1][2] + .6
        if ch[0][1] - .05 <= t < min(nb, ch[-1][2] + .6): show = ch
    if not show: return
    words = [w[0].upper().strip('.,?') for w in show]; sp = SUBF.measureText(' ')
    tw = sum(SUBF.measureText(w) for w in words) + sp * (len(words) - 1); x = W / 2 - tw / 2; y = SUBY
    pill = P((20, 6, 30), .45); blur(pill, 18)
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 40, y - 62, x + tw + 40, y + 28), 40, 40), pill)
    for (wd, a0, b0), wu in zip(show, words):
        on = a0 - .03 <= t < b0 + .05
        sh = P((0, 0, 0), .7); blur(sh, 4); c.drawString(wu, x, y + 3, SUBF, sh)
        c.drawString(wu, x, y, SUBF, P(YEL if on else (255, 255, 255), 1 if t >= a0 - .03 else .5))
        x += SUBF.measureText(wu) + sp


def wat(word, li, after=0.0):
    """time a word is spoken inside line li (fallback: line start)."""
    for w, a0, b0 in WORDS:
        if S[li] - .1 <= a0 <= E[li] + .1 and w.lower().startswith(word): return a0 + after
    return S[li] + after


def sunset_bg(c, t, sun_y=820, a=1.0):
    vgrad(c, [(40, 14, 90), (150, 40, 150), (255, 100, 120), (255, 170, 110)], [0, .38, .62, .78], 0, 1200)
    retro_sun(c, W / 2, sun_y, 250, t, a)
    skyline(c, 1150, 2, 120, 380, (60, 20, 90), (255, 200, 120), t, .9, wins=False)
    skyline(c, 1200, 5, 80, 300, (35, 12, 60), (255, 220, 150), t)
    ocean(c, 1200, t)


def frame(c, t):
    s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11 = S[2] - .2, S[3] - .2, S[4] - .25, S[5] - .2, S[6] - .25, S[7] - .25, S[8] - .25, S[10] - .2, S[11] - .25, S[12] - .25, DUR
    cam = 1 + .03 * math.sin(t * .35)
    c.save(); c.translate(W / 2, H / 2); c.scale(cam, cam); c.translate(-W / 2, -H / 2)
    if t < s1:                                            # 0: neon title over Vice-City sunset, cash rising
        sunset_bg(c, t)
        palm(c, 120, 1420, 1.25, t, lean=.15); palm(c, 1000, 1460, 1.1, t + 2, lean=-.35)
        money(c, t, 1, 26, ss(.6, 2.0, t))
        neon(c, 'GTA 6', 640, 250, ss(.1, .7, t) * 1.0, sk=-.08)
        small(c, 'IS ABOUT TO MAKE PEOPLE', 760, ss(.6, 1.2, t))
        neon(c, 'RICH', 930, 170, ss(wat('rich', 0) - .25, wat('rich', 0) + .2, t), top=YEL, bot=GREEN, glowc=GREEN)
        k = ss(S[1] - .2, S[1] + .3, t)                   # calendar card: tomorrow
        if card(c, W / 2, 1160, 380, 280, k, rot=-4, fill=CREAM, tilt=40):
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-210, -150, 210, -60), 34, 34), P((230, 40, 90)))
            c.drawRect(skia.Rect.MakeLTRB(-210, -95, 210, -60), P((230, 40, 90)))
            f = F(ANTON, 52); c.drawString('NOV', -f.measureText('NOV') / 2, -82, f, P(CREAM))
            f = F(ANTON, 170); c.drawString('19', -f.measureText('19') / 2, 120, f, P(DEEP))
            c.restore()
        chipk = ss(wat('tomorrow', 1) - .1, wat('tomorrow', 1) + .25, t)
        if chipk > 0: chip(c, 'TOMORROW', W / 2, 1360, (230, 40, 90), a=chipk, f=LBL)
    elif t < s2:                                          # 1: who gets rich - three phones
        k0 = t - s1
        vgrad(c, [(30, 10, 70), (120, 30, 140), (255, 110, 120)], [0, .6, 1])
        glow(c, W / 2, 900, 700, PINK, .35)
        money(c, t, 3, 14, .55, .6)
        small(c, 'NOT JUST THE GAME STUDIO', 420, ss(0, .4, k0), f=LBL)
        for i, (scr, lab, kw) in enumerate([('live', 'STREAMERS', 'streamers'), ('video', 'YOUTUBERS', 'youtubers'), ('clip', 'CLIPPERS', 'clip')]):
            tk = ss(wat(kw, 2) - .35, wat(kw, 2) + .1, t)
            if tk <= 0: continue
            x = [250, 540, 830][i]; y = 860 + [30, -20, 30][i] + 50 * (1 - tk)
            phone(c, x, y, .78, tk, t, scr, rot=[-7, 0, 7][i])
            chip(c, lab, x, y + 300, [(230, 40, 90), (120, 60, 220), (20, 160, 150)][i], a=tk)
    elif t < s3:                                          # 2: rewind to 2013
        k = cl((t - s2) / (s3 - s2))
        vgrad(c, [(20, 8, 50), (70, 20, 110)])
        for i in range(18):                               # rewind streaks
            y = (i * 113 + k * 2200) % H; c.drawRect(skia.Rect.MakeLTRB(0, y, W, y + 3 + i % 4), P(PINK, .25))
        neon(c, '2013', 960, 300, ss(.05, .5, k), top=CREAM, bot=TEAL, glowc=TEAL)
        small(c, "HERE'S HOW WE KNOW", 1100, ss(0, .35, k), f=LBL)
    elif t < s4:                                          # 3: GTA 5, $1B in 3 days
        k0 = t - s3
        vgrad(c, [(15, 10, 45), (60, 20, 100), (200, 70, 120)], [0, .6, 1], 0, 1300)
        skyline(c, 1300, 11, 200, 520, (25, 10, 50), (255, 210, 140), t)
        vgrad(c, [(25, 10, 50), (10, 5, 25)], None, 1300, H)
        small(c, 'GTA 5 . 2013', 420, ss(0, .4, k0), cc=TEAL, f=LBL)
        kb = ss(wat('billion', 4) - .4, wat('billion', 4) + .5, t)
        n = int(1_000_000_000 * ss(0, 1, kb)); s = '$' + format(n, ',')
        neon(c, s, 720, 112 if n >= 1e9 else 112, min(1, kb * 3), top=YEL, bot=GREEN, glowc=GREEN)
        kd = ss(wat('three', 4) - .2, wat('three', 4) + .3, t)
        for i in range(3):                                # three day cards flip in
            dk = ss(.0 + i * .18, .3 + i * .18, kd)
            if card(c, 290 + i * 250, 1000, 200, 220, dk, rot=[-5, 0, 5][i], fill=CREAM, tilt=30, r=26):
                f = F(ANTON, 40); c.drawString('DAY', -f.measureText('DAY') / 2, -40, f, P((230, 40, 90)))
                f = F(ANTON, 120); c.drawString(str(i + 1), -f.measureText(str(i + 1)) / 2, 80, f, P(DEEP)); c.restore()
        money(c, t, 5, 30, ss(0, .6, kb), 1.4)
    elif t < s5:                                          # 4: 230M copies - stack of game cases
        k0 = t - s4
        vgrad(c, [(40, 14, 90), (180, 50, 140), (255, 140, 100)], [0, .55, 1])
        glow(c, W / 2, 1000, 600, YEL, .25)
        n = int(26 * ss(.2, (E[5] - s4) * .85, k0))
        rnd = random.Random(2)
        for i in range(n):
            x = W / 2 + rnd.uniform(-260, 260) * (1 - i / 34); y = 1330 - (i // 3) * 64 - (i % 3) * 6
            c.save(); c.translate(x, y); c.rotate(rnd.uniform(-8, 8))
            c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-110, -30, 110, 30), 8, 8), P([PINK, TEAL, YEL, ORNG][i % 4]))
            c.drawRect(skia.Rect.MakeLTRB(-110, -30, -86, 30), P((40, 15, 60), .5)); c.restore()
        kc = ss(wat('two', 5) - .2, wat('copies', 5) + .2, t)
        neon(c, '%dM' % round(230 * ss(0, 1, kc)), 640, 260, min(1, kc * 4), top=CREAM, bot=PINK)
        small(c, 'COPIES SOLD', 760, kc, f=LBL)
    elif t < s6:                                          # 5: #1 on Twitch-style streaming, 2.1B hours
        k0 = t - s5
        vgrad(c, [(30, 12, 70), (90, 50, 180), (150, 90, 230)], [0, .6, 1])
        if card(c, W / 2, 900, 820, 520, ss(0, .4, k0), rot=-2, fill=(24, 14, 40), tilt=30):
            c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-390, -240, 390, 240), 24, 24))
            gp = skia.Paint(AntiAlias=True); gp.setShader(skia.GradientShader.MakeLinear([(0, -240), (0, 240)], [col((255, 120, 90)), col((120, 40, 170))])); c.drawRect(skia.Rect.MakeLTRB(-390, -240, 390, 240), gp)
            for i in range(3): person(c, -220 + i * 220, 240, .8, (35, 12, 50), ['cop', 'driver', 'robber'][i], t)
            c.restore(); chip(c, 'LIVE', -300, -170, (230, 30, 60)); c.restore()
        small(c, '2021 . MOST-WATCHED GAME', 520, ss(.2, .6, k0), cc=TEAL, f=LBL)
        kh = ss(wat('two', 6) - .3, wat('hours', 6) + .2, t)
        neon(c, '2.1 BILLION', 1330, 150, kh, top=CREAM, bot=(190, 150, 255), glowc=(150, 90, 255))
        small(c, 'HOURS WATCHED', 1420, kh, f=LBL)
        chat(c, t, s5 + .6, 760, 18, .9)
    elif t < s7:                                          # 6: roleplay - cop, robber, taxi
        k0 = t - s6
        sunset_bg(c, t, 760)
        kr = ss(wat('roleplay', 7) - .3, wat('roleplay', 7) + .2, t)
        neon(c, 'ROLEPLAY', 560, 180, kr, top=CREAM, bot=TEAL, glowc=TEAL)
        for i, (kind, kw) in enumerate([('cop', 'cops'), ('robber', 'robbers'), ('driver', 'taxi')]):
            pk = ss(wat(kw, 7) - .3, wat(kw, 7) + .15, t)
            if pk <= 0: continue
            x = [230, 540, 850][i]; y = 1230 + 40 * (1 - back(0, 1, pk))
            cc = [(70, 110, 255), (255, 80, 120), (255, 200, 60)][i]
            glow(c, x, y - 150, 300, cc, .55 * pk)
            if kind == 'driver': taxi(c, x, y + 20, .9, pk)
            person(c, x, y - (40 if kind == 'driver' else 0), 1.0, (25, 8, 35), kind, t, pk)
            chip(c, ['COP', 'ROBBER', 'TAXI DRIVER'][i], x, y + 80, [(40, 80, 200), (200, 40, 80), (220, 160, 20)][i], a=pk)
        lk = ss(wat('live', 7) - .2, wat('live', 7) + .2, t)
        if lk > 0: chip(c, 'LIVE  24/7', W / 2, 700, (230, 30, 60), a=lk, f=LBL)
        chat(c, t, wat('live', 7), 700, 10, .9, 9)
    elif t < s8:                                          # 7: forecast chart + 4X
        k0 = t - s7
        vgrad(c, [(12, 8, 40), (40, 20, 90), (120, 40, 140)], [0, .6, 1])
        for i in range(10): c.drawRect(skia.Rect.MakeLTRB(120, 360 + i * 90, W - 120, 362 + i * 90), P(CREAM, .06))
        small(c, 'BANK FORECAST: DAY ONE', 330, ss(0, .4, k0), cc=TEAL, f=LBL)
        bars(c, ss(.2, 1.0, k0), ss(wat('forty', 8) - .3, wat('copies', 8) + .3, t))
        k4 = ss(S[9] - .1, S[9] + .35, t)
        if k4 > 0:
            c.save(); c.translate(560, 700); c.rotate(-12); sc = 1.6 - .6 * back(0, 1, k4); c.scale(sc, sc)
            g = P(YEL, .6 * k4); blur(g, 26); c.drawCircle(0, 0, 130, g); c.drawCircle(0, 0, 120, P((230, 40, 90), k4))
            f = F(ANTON, 130); c.drawString('4X', -f.measureText('4X') / 2, 46, f, P(YEL, k4)); c.restore()
    elif t < s9:                                          # 8: every player wants to watch -> city of screens
        k0 = t - s8
        vgrad(c, [(10, 6, 30), (40, 14, 80), (110, 30, 120)], [0, .6, 1])
        screens(c, t, ss(0, (s9 - s8) * .9, k0))
        skyline(c, 1500, 21, 100, 300, (15, 6, 30), (255, 200, 140), t)
        neon(c, '45M PLAYERS', 1250, 120, ss(.2, .7, k0), top=CREAM, bot=TEAL, glowc=TEAL)
        small(c, '= 45 MILLION VIEWERS', 1330, ss(wat('watch', 10) - .2, wat('watch', 10) + .3, t), f=LBL)
    elif t < s10:                                         # 9: week one = the biggest wave
        k0 = t - s9
        vgrad(c, [(40, 14, 90), (200, 60, 140), (255, 160, 110)], [0, .5, 1], 0, 1100)
        retro_sun(c, W / 2, 700, 230, t)
        wave(c, t, ss(0, 1.6, k0))
        small(c, 'POST IN', 370, ss(.1, .5, k0), f=LBL)
        neon(c, 'WEEK ONE', 580, 190, ss(wat('week', 11) - .3, wat('week', 11) + .2, t), top=YEL, bot=ORNG, glowc=ORNG)
        bw = ss(wat('biggest', 11) - .2, wat('wave', 11) + .2, t)
        if bw > 0: chip(c, 'CATCH THE BIGGEST WAVE', W / 2, 1360, (230, 40, 90), a=bw, f=LBL)
    else:                                                 # 10: question + CTA
        k0 = t - s10
        sunset_bg(c, t, 900)
        palm(c, 110, 1460, 1.2, t, lean=.2); palm(c, 990, 1480, 1.05, t + 1, lean=-.3)
        small(c, 'WOULD YOU START A', 560, ss(0, .4, k0), f=LBL)
        neon(c, 'GTA 6', 760, 220, ss(.2, .7, k0), sk=-.08)
        neon(c, 'CHANNEL?', 930, 150, ss(.4, .9, k0), top=YEL, bot=ORNG, glowc=ORNG)
        cta = 'SUBSCRIBE FOR WHAT HAPPENS NEXT' if PLAT == 'yt' else 'SEND THIS TO YOUR GTA FRIEND'
        small(c, cta, 1040, ss(E[12] - .2, E[12] + .4, t), cc=YEL)
        fade = ss(DUR - .7, DUR, t)
        if fade > 0: c.drawRect(skia.Rect.MakeLTRB(-100, -100, W + 100, H + 100), P((0, 0, 0), fade))
    c.restore()
    for bt in (s1, s2, s3, s4, s5, s6, s7, s8, s9, s10):   # soft cross-dissolve flash at cuts (eased over ~8 frames)
        d = abs(t - bt)
        if d < .14: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 220, 240), .22 * (1 - d / .14)))


def render_frame(c, t):
    c.save(); c.scale(SC, SC); c.clear(skia.ColorBLACK); frame(c, t); grain(c); subs(c, t); c.drawImage(WM, 0, 0); c.restore()


def main():
    out = os.path.join(D, 'v_%s.mp4' % PLAT); n = int(DUR * FPS)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '%dx%d' % (OW, OH), '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    surf = skia.Surface(OW, OH)
    for f in range(n):
        render_frame(surf.getCanvas(), f / FPS)
        ff.stdin.write(surf.makeImageSnapshot().tobytes())
        if f % 150 == 0: print('frame', f, n, flush=True)
    ff.stdin.close(); ff.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-i', os.path.join(D, 'mix_fx.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', os.path.join(D, 'GTA6_Make_People_Rich_%s.mp4' % PLAT)], check=True)
    print('done')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'still':
        for ts in sys.argv[3:]:
            s = skia.Surface(OW, OH); t = float(ts); render_frame(s.getCanvas(), t)
            s.makeImageSnapshot().save(os.path.join(D, 'still_%05.2f.png' % t), skia.kPNG)
    else:
        main()
