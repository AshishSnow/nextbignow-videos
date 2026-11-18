"""NEW LOOK sample: 'Painted Story' - painterly 2D, flat shapes + soft gradients + paper grain, drawn entirely in code
(no photos). Layered parallax, motion rules: nothing changes in one frame, exposure dips before impacts,
everything the light/storm touches reacts, particles at 3 depths.
usage: paint_sahara.py <sample_dir>   (reads times.json + align.json, writes sample.mp4 with mix.wav)"""
import os, sys, json, math, random, subprocess
import numpy as np, skia

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
T = json.load(open(os.path.join(D, 'times.json')))          # [[start,end], ...] per voice line
import re
WORDS = [[re.sub(r'\(\d\)', '', w), x, y] for w, x, y in json.load(open(os.path.join(D, 'align.json'))) if w not in ('<s>', '</s>', '<sil>')]
DUR = T[-1][1] + 1.8
PLAT = os.environ.get('PLAT', 'ig')
SUBY = 1500 if PLAT == 'yt' else 1430
FX = os.path.join(HERE, '..', 'fonts'); FD = '/usr/share/fonts/opentype/inter/'


def F(p, s):
    f = skia.Font(skia.Typeface.MakeFromFile(p), s); f.setEdging(skia.Font.Edging.kAntiAlias); return f


SERIF_B = F(os.path.join(FX, 'Cormorant-Bold.ttf'), 190)
SERIF_I = F(os.path.join(FX, 'Cormorant-MediumItalic.ttf'), 64)
SMALL = F(FD + 'Inter-SemiBold.otf', 30)
SUBF = F(FD + 'InterDisplay-Bold.otf', 36)


def C(r, g, b, a=1.0): return skia.Color4f(r / 255, g / 255, b / 255, a)
def col(c, a=1.0): return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(255 * max(0, min(1, a))))
def mix(a, b, k): return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))
def cl(x): return max(0.0, min(1.0, x))
def ss(a, b, x):  # smoothstep: every change eases, never pops
    k = cl((x - a) / (b - a)) if b != a else float(x >= a); return k * k * (3 - 2 * k)
def P(c, a=1.0):
    p = skia.Paint(AntiAlias=True); p.setColor(col(c, a)); return p


# ---------- paper grain (precomputed once) ----------
rng = np.random.default_rng(3)
g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
from scipy import ndimage
fib = ndimage.gaussian_filter(rng.normal(0, 1, (H // 2, W // 2)), (0.6, 6))
tex = np.clip(128 + g * 10 + fib * 26, 0, 255).astype(np.uint8)
tex = np.repeat(np.repeat(tex, 2, 0), 2, 1)
rgba = np.dstack([tex, tex, tex, np.full_like(tex, 255)])
GRAIN = skia.Image.fromarray(rgba, colorType=skia.kRGBA_8888_ColorType)
WM = skia.Image.open(os.path.join(HERE, 'brand_logo_port.png'))


def grain(c, a=0.22):
    p = skia.Paint(); p.setBlendMode(skia.BlendMode.kOverlay); p.setAlphaf(a)
    c.drawImage(GRAIN, 0, 0, skia.SamplingOptions(), p)


def vgrad(c, top, bot, y0=0, y1=H, stops=None, cols=None):
    p = skia.Paint(AntiAlias=True)
    cs = cols or [col(top), col(bot)]
    p.setShader(skia.GradientShader.MakeLinear([(0, y0), (0, y1)], cs, stops))
    c.drawRect(skia.Rect.MakeLTRB(-50, y0, W + 50, y1), p)


def glow(c, x, y, r, cc, a):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((x, y), r, [col(cc, a), col(cc, a * 0.35), col(cc, 0)], [0, 0.35, 1]))
    c.drawCircle(x, y, r, p)


def dune(seed, base, amp, x0):
    """sharp-crested dune silhouette (wind side soft, slip face steep)."""
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(0, 91):
        x = -200 + i * (W + 400) / 90
        u = (x + x0) / (900.0 + 300 * (seed % 3))
        s = (u + ph[0]) % 1.0
        prof = (s / 0.72) ** 1.6 if s < 0.72 else (1 - (s - 0.72) / 0.28) ** 0.7   # long gentle rise, short steep drop
        y = base - amp * prof - amp * 0.35 * math.sin(u * 0.7 + ph[1]) - amp * 0.15 * math.sin(u * 2.3 + ph[2])
        pts.append((x, y))
    return pts


def fill_dune(c, pts, top, bot, rim=None, rim_a=0.0, haze=None, haze_a=0.0):
    path = skia.Path(); path.moveTo(*pts[0])
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        path.quadTo(pts[i][0], pts[i][1], mx, my)
    path.lineTo(W + 200, H + 50); path.lineTo(-200, H + 50); path.close()
    ytop = min(p[1] for p in pts)
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([(0, ytop), (0, ytop + 700)], [col(top), col(bot)]))
    c.drawPath(path, p)
    if haze is not None and haze_a > 0: c.drawPath(path, P(haze, haze_a))
    if rim is not None and rim_a > 0:
        s = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5)
        s.setColor(col(rim, rim_a)); s.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 3))
        top_path = skia.Path(); top_path.moveTo(*pts[0])
        for q in pts[1:]: top_path.lineTo(*q)
        c.drawPath(top_path, s)


def walker(c, x, y, s, t, a=1.0, col_=(40, 22, 18)):
    """tiny silhouette runner, legs swing (generic figure, not a real person)."""
    ph = math.sin(t * 7.5)
    c.save(); c.translate(x, y); c.scale(s, s)
    p = P(col_, a); st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap); st.setColor(col(col_, a))
    c.drawCircle(0, -78, 10, p)
    c.drawLine(0, -66, 2, -30, st)
    c.drawLine(2, -30, 2 + 14 * ph, 0, st); c.drawLine(2, -30, 2 - 14 * ph, 0, st)
    c.drawLine(0, -60, 12 * -ph, -38, st); c.drawLine(0, -60, -12 * -ph, -38, st)
    c.drawRect(skia.Rect.MakeXYWH(-14, -64, 12, 22), p)  # backpack
    c.restore()


def bat(c, x, y, s, flap, a=1.0, cc=(25, 18, 30)):
    w = math.sin(flap)
    path = skia.Path(); path.moveTo(0, 0)
    path.quadTo(-18, -14 * w - 6, -36, -6 * w); path.quadTo(-24, 2, -14, 0); path.quadTo(-8, 6, 0, 4)
    path.quadTo(8, 6, 14, 0); path.quadTo(24, 2, 36, -6 * w); path.quadTo(18, -14 * w - 6, 0, 0)
    c.save(); c.translate(x, y); c.scale(s, s); c.drawPath(path, P(cc, a)); c.restore()


def shrine(c, x, y, s, door_glow):
    """marabout: white cube + dome, warm doorway."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-90, -120, 180, 120), P((232, 220, 200)))
    c.drawRect(skia.Rect.MakeXYWH(-90, -120, 60, 120), P((200, 185, 165)))
    path = skia.Path(); path.moveTo(-70, -120); path.cubicTo(-70, -210, 70, -210, 70, -120); path.close()
    c.drawPath(path, P((240, 230, 212)))
    c.drawRect(skia.Rect.MakeXYWH(-4, -232, 8, 30), P((240, 230, 212)))
    door = skia.Path(); door.moveTo(-22, 0); door.lineTo(-22, -60); door.cubicTo(-22, -84, 22, -84, 22, -60); door.lineTo(22, 0); door.close()
    c.drawPath(door, P(mix((40, 30, 30), (255, 170, 70), door_glow)))
    c.restore()
    glow(c, x, y - 40 * s, 260 * s, (255, 160, 60), 0.35 * door_glow)


def stars(c, a, seed=5):
    rnd = random.Random(seed)
    for i in range(180):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H * 0.55); r = rnd.choice((1.2, 1.6, 2.4))
        c.drawCircle(x, y, r, P((255, 245, 225), a * rnd.uniform(0.4, 1)))


def sand(c, t, k, warm=(232, 160, 90)):
    """storm sand at 3 depths: far fine haze-specks, mid streaks, near thick fast blurred streaks."""
    if k <= 0: return
    rnd = random.Random(9)
    for i in range(520):
        z = rnd.random(); spd = 300 + 2600 * z * z
        x = (rnd.uniform(0, W + 600) + t * spd) % (W + 600) - 300
        y = rnd.uniform(0, H) + math.sin(t * 2 + i) * 20 * z
        L = 6 + 110 * z * z; th = 1 + 6 * z * z
        p = skia.Paint(AntiAlias=True, StrokeWidth=th, StrokeCap=skia.Paint.kRound_Cap)
        p.setColor(col(mix(warm, (255, 225, 170), z), k * (0.25 + 0.5 * z)))
        if z > 0.8: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 2.5))
        c.drawLine(x, y, x + L, y + L * 0.12, p)


def storm_wall(c, t, front, a):
    """billowing haboob wall rolling in from the left; front = x of leading edge."""
    if a <= 0: return
    rnd = random.Random(4)
    for layer in range(3):
        cc = [(150, 75, 35), (190, 105, 50), (225, 145, 80)][layer]
        for i in range(26):
            y = 200 + i * 62 + layer * 18
            r = 160 + 90 * math.sin(i * 1.7 + layer) + 40 * math.sin(t * 0.8 + i)
            x = front - 120 * layer - rnd.uniform(0, 220) + 30 * math.sin(t * 0.6 + i * 0.5)
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial((x, y), r, [col(cc, a), col(cc, a * 0.85), col(cc, 0)], [0, 0.6, 1]))
            c.drawCircle(x, y, r, p)
        top = 260 + 120 * layer
        c.drawRect(skia.Rect.MakeLTRB(-50, top, front - 160 - 120 * layer, H), P(cc, a))
        for j in range(12):  # billowing crown
            bx = -50 + j * (front - 160 - 120 * layer + 50) / 11; br = 120 + 50 * math.sin(j * 2.1 + layer + t * 0.7)
            pp = skia.Paint(AntiAlias=True)
            pp.setShader(skia.GradientShader.MakeRadial((bx, top), br, [col(cc, a), col(cc, a * 0.8), col(cc, 0)], [0, 0.65, 1]))
            c.drawCircle(bx, top, br, pp)


def title(c, small, big, k, y=760, bigcol=(255, 236, 200)):
    if k <= 0: return
    a = ss(0, 1, k); dy = 24 * (1 - a)
    if small:
        x = W / 2 - SMALL.measureText(small) / 2
        c.drawString(small, x, y - 200 + dy, SMALL, P((255, 240, 220), a * 0.9))
    x = W / 2 - SERIF_B.measureText(big) / 2
    sh = P((0, 0, 0), 0.35 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    c.drawString(big, x, y + 8 + dy, SERIF_B, sh); c.drawString(big, x, y + dy, SERIF_B, P(bigcol, a))


def line_i(c, text, k, y, cc=(255, 236, 200)):
    if k <= 0: return
    a = ss(0, 1, k); x = W / 2 - SERIF_I.measureText(text) / 2
    sh = P((0, 0, 0), 0.4 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 8))
    c.drawString(text, x, y + 4, SERIF_I, sh); c.drawString(text, x, y + (1 - a) * 16, SERIF_I, P(cc, a))


def subs(c, t):
    cur = [w for w in WORDS if w[1] - 0.05 <= t]
    if not cur: return
    # group words into chunks of <=5 by line starts
    chunks, chunk = [], []
    for w in WORDS:
        if chunk and any(chunk[-1][1] < ln[0] - 0.05 <= w[1] for ln in T): chunks.append(chunk); chunk = []
        chunk.append(w)
        if len(chunk) >= 5: chunks.append(chunk); chunk = []
    if chunk: chunks.append(chunk)
    show = None
    for i, ch in enumerate(chunks):
        nb = chunks[i + 1][0][1] if i + 1 < len(chunks) else ch[-1][2] + 0.6
        if ch[0][1] - 0.05 <= t < min(nb, ch[-1][2] + 0.6): show = ch
    if not show: return
    words = [w[0].upper().strip('.,?') for w in show]; sp = SUBF.measureText(' ')
    tw = sum(SUBF.measureText(w) for w in words) + sp * (len(words) - 1); x = W / 2 - tw / 2; y = SUBY
    pill = P((20, 10, 8), 0.38); pill.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 18))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x - 40, y - 62, x + tw + 40, y + 28), 40, 40), pill)
    for (wd, a, b), wu in zip(show, words):
        on = a - 0.03 <= t < b + 0.05
        sh = P((0, 0, 0), 0.7); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 4))
        c.drawString(wu, x, y + 3, SUBF, sh)
        c.drawString(wu, x, y, SUBF, P((255, 214, 64) if on else (255, 255, 255), 1 if t >= a - 0.03 else 0.5))
        x += SUBF.measureText(wu) + sp


def frame(c, t):
    L = T
    s2, s3, s4 = L[1][0], L[2][0] - 0.25, L[3][0] - 0.25     # shot boundaries
    hit = L[3][0] + 0.9                                        # "sandstorm HITS"
    calm = L[4][0]                                             # "when it ends"
    # ---------------- shot 1+2: golden dusk dunes, lone runner (hook) ----------------
    if t < s3:
        u = t
        cam = 40 * u
        vgrad(c, None, None, 0, 1300, [0, .45, .8, 1], [col((38, 30, 70)), col((140, 60, 70)), col((240, 130, 60)), col((255, 200, 120))])
        sx, sy = 640 - cam * 0.05, 900 + 6 * u
        glow(c, sx, sy, 520, (255, 190, 110), 0.55); c.drawCircle(sx, sy, 120, P((255, 226, 170)))
        fill_dune(c, dune(1, 1080, 120, cam * 0.25), (210, 120, 80), (170, 80, 70), haze=(240, 160, 110), haze_a=0.35)
        fill_dune(c, dune(2, 1250, 180, cam * 0.55 + 300), (205, 105, 55), (120, 50, 40), rim=(255, 210, 150), rim_a=0.8)
        nd = dune(3, 1360, 200, cam * 1.0 + 120)
        fill_dune(c, nd, (150, 62, 38), (60, 22, 25), rim=(255, 190, 120), rim_a=0.9)
        # runner on the near crest + footprint trail
        wx = 360 + 12 * u
        cy = min(nd, key=lambda q: abs(q[0] - wx))[1]
        for i in range(1, 9):
            fx = wx - i * 26; fy = min(nd, key=lambda q: abs(q[0] - fx))[1] + 4
            c.drawOval(skia.Rect.MakeXYWH(fx - 5, fy - 2, 10, 4), P((90, 35, 25), 0.6 * (1 - i / 9)))
        walker(c, wx, cy + 2, 1.15, u)
        # shimmer
        for i in range(6):
            y = 1050 + i * 22; a = 0.05 + 0.03 * math.sin(u * 3 + i)
            c.drawLine(0, y + 4 * math.sin(u * 4 + i), W, y, skia.Paint(AntiAlias=True, StrokeWidth=3, Color=col((255, 220, 160), a)))
        # bats cross the sun on "survived on bats"
        kb = ss(s2 - 0.1, s2 + 0.4, t)
        for i in range(7):
            bx = sx - 520 + (t - s2) * (180 + 40 * i) + i * 40; by = sy - 160 - i * 30 + 20 * math.sin(t * 2 + i)
            bat(c, bx, by, 0.8 + 0.15 * (i % 3), t * 14 + i, kb)
        title(c, 'LOST IN THE SAHARA', '9 Days', ss(0.0, 0.6, t), y=640)
        line_i(c, '...and he survived on bats.', ss(s2 - 0.05, s2 + 0.5, t), 740)
        out_k = ss(s3 - 0.35, s3, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((20, 14, 30), out_k))
        return
    # ---------------- shot 3: night shrine, bats (main point) ----------------
    if t < s4:
        u = t - s3
        vgrad(c, None, None, 0, 1400, [0, .6, 1], [col((12, 14, 40)), col((40, 40, 90)), col((110, 80, 110))])
        stars(c, 0.9)
        glow(c, 230, 420, 200, (220, 225, 255), 0.25); c.drawCircle(230, 420, 54, P((240, 238, 225)))
        fill_dune(c, dune(5, 1180, 140, u * 10), (70, 60, 100), (40, 34, 66))
        nd = dune(6, 1380, 200, u * 30 + 80)
        sx = 540 + 8 * u
        shrine(c, sx, min(nd, key=lambda q: abs(q[0] - sx))[1] + 30, 1.25, ss(0.2, 1.2, u))
        fill_dune(c, nd, (95, 70, 95), (30, 22, 40), rim=(190, 190, 255), rim_a=0.35)
        for i in range(9):  # bats spiral out of the dome
            ang = u * 1.6 + i * 0.7; rr = 120 + 60 * i * ss(0, 2, u)
            bat(c, sx + math.cos(ang) * rr, 900 - 120 - math.sin(ang) * rr * 0.5 - i * 8, 0.7 + 0.1 * (i % 3), t * 16 + i, ss(0.3, 1.0, u))
        w_ = WORDS
        def at(word, after):
            for w in w_:
                if w[1] >= after - 0.01 and w[0].lower().strip('.,?') == word: return w[1]
            return 99
        for j, (word, lab) in enumerate((('shrine', 'SHADE'), ('bats', 'FOOD'), ('urine', 'WATER'))):
            k = ss(at(word, s3) - 0.1, at(word, s3) + 0.35, t)
            if k > 0:
                x = 240 + j * 300
                c.drawString(lab, x - SMALL.measureText(lab) / 2, 700 + (1 - k) * 16, F(FD + 'Inter-Bold.otf', 40), P((255, 214, 64), k))
                c.drawLine(x - 50, 720, x + 50, 720, skia.Paint(AntiAlias=True, StrokeWidth=3, Color=col((255, 214, 64), k * 0.8)))
        title(c, None, 'How?', ss(s3, s3 + 0.5, t), y=600, bigcol=(255, 240, 220))
        out_k = ss(s4 - 0.3, s4, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((240, 200, 150), out_k * 0.9))
        return
    # ---------------- shot 4: the sandstorm ----------------
    if len(L) > 5 and t >= L[5][0] - 0.3:
        return frame2(c, t)
    u = t - s4
    dip = 1 - 0.3 * ss(hit - 0.5, hit - 0.15, t) * (1 - ss(hit, hit + 0.3, t))      # exposure dips ~30% before impact
    clear = ss(calm + 0.2, calm + 1.6, t)                                           # slow recovery after "when it ends"
    vgrad(c, None, None, 0, 1300, [0, .7, 1], [col((120, 150, 190)), col((230, 190, 140)), col((250, 210, 160))])
    c.drawCircle(300, 380, 70, P((255, 245, 220))); glow(c, 300, 380, 300, (255, 230, 180), 0.5)
    fill_dune(c, dune(7, 1150, 130, u * 15), (230, 160, 100), (200, 120, 80), haze=(250, 210, 160), haze_a=0.3)
    nd = dune(8, 1360, 200, u * 40 + 200)
    reach = ss(hit - 0.3, hit + 0.12, t)                                             # light/storm touches the ground -> warm reaction
    fill_dune(c, nd, mix((215, 130, 70), (180, 80, 40), reach), (110, 50, 35), rim=(255, 230, 180), rim_a=0.8 * (1 - reach))
    wx = 640
    cy = min(nd, key=lambda q: abs(q[0] - wx))[1]
    if clear < 0.5:
        for i in range(1, 9):
            fx = wx - i * 26; fy = min(nd, key=lambda q: abs(q[0] - fx))[1] + 4
            c.drawOval(skia.Rect.MakeXYWH(fx - 5, fy - 2, 10, 4), P((90, 35, 25), 0.6 * (1 - i / 9)))
        walker(c, wx, cy + 2, 1.2, u, a=1 - ss(hit, hit + 0.4, t))
    front = -500 + 2000 * ss(L[3][0] - 0.1, hit + 0.25, t)
    engulf = ss(hit - 0.1, hit + 0.35, t) * (1 - clear)
    storm_wall(c, u, front, 1 - clear)
    c.drawRect(skia.Rect.MakeWH(W, H), P((200, 115, 55), 0.62 * engulf))
    glow(c, 300, 380, 260, (255, 230, 170), 0.35 * engulf); c.drawCircle(300, 380, 60, P((255, 225, 170), 0.55 * engulf))
    sand(c, u, max(engulf, 0.35 * ss(hit - 0.6, hit, t) * (1 - clear)))
    if dip < 1: c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), 1 - dip))
    title(c, 'THEN A SANDSTORM HITS', '8 Hours', ss(L[3][0] + 0.9, L[3][0] + 1.5, t) * (1 - ss(calm - 0.3, calm, t)), y=640)
    line_i(c, '...and the trail is gone.', ss(calm + 0.9, calm + 1.6, t), 700, cc=(80, 40, 30))
    out_k = ss(L[5][0] - 0.6, L[5][0] - 0.3, t)
    if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 236, 200), out_k))



# ======================= second half of the story =======================
def wat(word, after=0.0):
    for w in WORDS:
        if w[1] >= after - 0.01 and w[0].lower().strip(".,?'") == word: return w[1]
    return 1e9


def goat(c, x, y, s, t, a=1.0, cc=(45, 25, 30)):
    ph = math.sin(t * 6 + x * 0.01)
    c.save(); c.translate(x, y); c.scale(s, s); p = P(cc, a)
    c.drawOval(skia.Rect.MakeXYWH(-26, -40, 52, 24), p)
    c.drawOval(skia.Rect.MakeXYWH(18, -54, 18, 14), p)
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, StrokeCap=skia.Paint.kRound_Cap); st.setColor(col(cc, a))
    c.drawLine(28, -54, 22, -66, st); c.drawLine(-24, -32, -30, -40, st)
    for lx, sgn in ((-16, 1), (-8, -1), (10, 1), (18, -1)):
        c.drawLine(lx, -18, lx + 4 * ph * sgn, 0, st)
    c.restore()


def girl(c, x, y, s, t, walking, a=1.0, cc=(45, 25, 30)):
    ph = math.sin(t * 6) * walking
    c.save(); c.translate(x, y); c.scale(s, s); p = P(cc, a)
    st = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap); st.setColor(col(cc, a))
    c.drawCircle(0, -70, 9, p)
    d = skia.Path(); d.moveTo(-4, -60); d.lineTo(4, -60); d.lineTo(14, -22); d.lineTo(-14, -22); d.close(); c.drawPath(d, p)
    c.drawLine(-5, -22, -5 + 8 * ph, 0, st); c.drawLine(5, -22, 5 - 8 * ph, 0, st)
    c.drawLine(4, -54, 26, -78 + 10 * (1 - walking), st)  # stick / pointing arm
    c.restore()


def plane_top(c, x, y, s, rot, a):
    """top-down plane SHADOW passing over the sand."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    p = P((60, 30, 20), a); p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    b = skia.Path(); b.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-14, -110, 28, 220), 14, 14)); c.drawPath(b, p)
    w = skia.Path(); w.moveTo(0, -20); w.lineTo(150, 30); w.lineTo(150, 50); w.lineTo(0, 20); w.lineTo(-150, 50); w.lineTo(-150, 30); w.close(); c.drawPath(w, p)
    tl = skia.Path(); tl.moveTo(0, 80); tl.lineTo(50, 110); tl.lineTo(50, 120); tl.lineTo(0, 105); tl.lineTo(-50, 120); tl.lineTo(-50, 110); tl.close(); c.drawPath(tl, p)
    c.restore()


def big_center(c, small, bigt, k, y, cc=(255, 236, 200), size=190):
    if k <= 0: return
    a = ss(0, 1, k); dy = 24 * (1 - a)
    f = F(os.path.join(FX, 'Cormorant-Bold.ttf'), size)
    if small:
        x = W / 2 - SMALL.measureText(small) / 2; c.drawString(small, x, y - size * 0.95 + dy, SMALL, P(cc, a * 0.9))
    x = W / 2 - f.measureText(bigt) / 2
    sh = P((0, 0, 0), 0.35 * a); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 10))
    c.drawString(bigt, x, y + 8 + dy, f, sh); c.drawString(bigt, x, y + dy, f, P(cc, a))


def frame2(c, t):
    L = T
    s5, s6, s7, s8, s9, s10 = (L[5][0] - 0.3, L[8][0] - 0.3, L[10][0] - 0.3, L[11][0] - 0.3, L[13][0] - 0.3, L[14][0] - 0.25)
    fin = ss(s5, s5 + 0.35, t)          # every cut fades in from the previous shot's colour, never pops
    # ---------- shot 5: noon shrine, then inside with the bats ----------
    if t < s6:
        u = t - s5; inside = ss(L[6][0] - 0.35, L[6][0] + 0.15, t)
        vgrad(c, None, None, 0, 1400, [0, .6, 1], [col((250, 225, 180)), col((250, 200, 140)), col((240, 170, 110))])
        glow(c, 540, 300, 520, (255, 250, 220), 0.7); c.drawCircle(540, 300, 90, P((255, 252, 235)))
        fill_dune(c, dune(9, 1150, 110, u * 12), (240, 175, 110), (215, 140, 90), haze=(255, 230, 190), haze_a=0.35)
        nd = dune(10, 1400, 150, u * 30 + 400)
        sx = 520; sy = min(nd, key=lambda q: abs(q[0] - sx))[1] + 40
        sh = skia.Path(); sh.moveTo(sx + 112, sy); sh.lineTo(sx + 112, sy - 150); sh.lineTo(sx + 420, sy + 10); sh.lineTo(sx + 300, sy + 30); sh.close()
        fill_dune(c, nd, (225, 145, 85), (150, 70, 45), rim=(255, 240, 200), rim_a=0.8)
        c.drawPath(sh, P((120, 50, 40), 0.35))
        shrine(c, sx, sy, 1.6, 0.0)
        walker(c, sx + 150, sy + 4, 1.0, 0, a=1.0)          # resting in the shade (still)
        for i in range(6):
            y = 1000 + i * 26; a = 0.05 + 0.03 * math.sin(u * 3 + i)
            c.drawLine(0, y + 5 * math.sin(u * 4 + i), W, y, skia.Paint(AntiAlias=True, StrokeWidth=3, Color=col((255, 240, 200), a)))
        big_center(c, 'DAY 3', 'Shade.', ss(L[5][0] + 0.6, L[5][0] + 1.2, t) * (1 - inside), 700, cc=(110, 40, 30))
        if inside > 0:   # inside the dome: dark, a shaft of light, bats hanging
            c.save(); c.drawRect(skia.Rect.MakeWH(W, H), P((28, 18, 22), inside))
            shaft = skia.Path(); shaft.moveTo(380, 1700); shaft.lineTo(700, 1700); shaft.lineTo(620, 1100); shaft.lineTo(460, 1100); shaft.close()
            sp = skia.Paint(AntiAlias=True)
            sp.setShader(skia.GradientShader.MakeLinear([(0, 1100), (0, 1700)], [col((255, 200, 120), 0.0), col((255, 200, 120), 0.45 * inside)]))
            c.drawPath(shaft, sp)
            arc = skia.Path(); arc.moveTo(60, 900); arc.cubicTo(60, 200, 1020, 200, 1020, 900)
            ap = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10); ap.setColor(col((80, 55, 50), inside)); c.drawPath(arc, ap)
            rnd = random.Random(12)
            for i in range(14):
                bx = 180 + i * 52 + rnd.uniform(-10, 10); by = 420 + abs(bx - 540) * 0.55 + rnd.uniform(-8, 8)
                sw = 3 * math.sin(t * 2 + i)
                c.save(); c.translate(bx, by); c.rotate(sw)
                c.drawLine(0, -18, 0, 0, skia.Paint(AntiAlias=True, StrokeWidth=2, Color=col((60, 40, 40), inside)))
                c.scale(2.0, 2.0)
                body = skia.Path(); body.moveTo(0, 0); body.cubicTo(-14, 6, -12, 44, 0, 50); body.cubicTo(12, 44, 14, 6, 0, 0)
                c.drawPath(body, P((15, 10, 14), inside)); c.drawCircle(-4, 42, 1.6, P((255, 200, 120), inside)); c.drawCircle(4, 42, 1.6, P((255, 200, 120), inside))
                c.restore()
            glow(c, 540, 1400, 500, (255, 170, 80), 0.25 * inside)
            c.restore()
            line_i(c, 'Bats live in the roof.', ss(L[6][0], L[6][0] + 0.5, t) * (1 - ss(L[7][0] - 0.3, L[7][0], t)), 1100, cc=(255, 220, 170))
            big_center(c, 'SO HE EATS THEM', 'Raw.', ss(wat('raw', L[7][0]) - 0.15, wat('raw', L[7][0]) + 0.3, t), 1150, cc=(255, 214, 120), size=220)
        out_k = ss(s6 - 0.3, s6, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((235, 190, 135), out_k))
        if fin < 1: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 236, 200), 1 - fin))
        return
    # ---------- shot 6: SOS in the sand from above, plane shadows miss him ----------
    if t < s7:
        u = t - s6
        z = 1.0 + 0.04 * u
        c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        vgrad(c, None, None, 0, H, [0, 1], [col((238, 186, 128)), col((214, 150, 95))])
        for i in range(40):   # wind ripples
            y = i * 52 + 10 * math.sin(i)
            path = skia.Path(); path.moveTo(-50, y)
            for xx in range(0, W + 100, 60): path.lineTo(xx, y + 10 * math.sin(xx * 0.012 + i * 0.7))
            rp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3); rp.setColor(col((190, 120, 70), 0.35)); c.drawPath(path, rp)
        sos_k = ss(L[8][0] + 0.2, L[8][1] + 0.2, t)
        fs = F(os.path.join(FX, 'Anton.ttf'), 420); tw = fs.measureText('SOS'); x0 = W / 2 - tw / 2
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x0 - 20, 0, (tw + 40) * sos_k, H))
        dp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, StrokeJoin=skia.Paint.kRound_Join); dp.setColor(col((150, 80, 45)))
        c.drawString('SOS', x0, 1050, fs, dp)
        hp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=8); hp.setColor(col((255, 225, 170), 0.8))
        c.drawString('SOS', x0 - 6, 1044, fs, hp)
        c.restore()
        walker(c, W / 2 + 330, 1150, 0.9, 0)
        tp = wat('planes', L[9][0])
        for j in range(2):
            k = cl((t - tp - j * 0.9) / 1.6)
            if 0 < k < 1: plane_top(c, lerp_ := (-300 + 1700 * k), 300 + 1200 * k + j * 200, 1.4 - j * 0.3, 145, 0.5 * math.sin(math.pi * k))
        c.restore()
        line_i(c, '...and miss him.', ss(wat('miss', L[9][0]) - 0.1, wat('miss', L[9][0]) + 0.4, t), 560, cc=(90, 35, 25))
        out_k = ss(s7 - 0.3, s7, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((250, 190, 170), out_k))
        return
    # ---------- shot 7: dawn, a girl with goats spots him ----------
    if t < s8:
        u = t - s7
        vgrad(c, None, None, 0, 1400, [0, .5, 1], [col((90, 90, 160)), col((240, 150, 150)), col((255, 205, 160))])
        glow(c, 760, 1060, 600, (255, 210, 160), 0.6); c.drawCircle(760, 1060, 110, P((255, 230, 190)))
        fill_dune(c, dune(11, 1150, 120, u * 10), (220, 140, 130), (180, 100, 100), haze=(255, 200, 180), haze_a=0.3)
        nd = dune(12, 1380, 170, u * 25 + 600)
        fill_dune(c, nd, (170, 85, 80), (70, 35, 45), rim=(255, 210, 180), rim_a=0.9)
        def gy(x): return min(nd, key=lambda q: abs(q[0] - x))[1] + 3
        spot = ss(wat('spots', L[10][0]) - 0.2, wat('spots', L[10][0]) + 0.3, t)
        for i in range(5):
            gx = 60 + i * 110 + 40 * u * (1 - spot * 0.7); goat(c, gx, gy(gx), 1.5 + 0.15 * (i % 2), t)
        gx = 640 + 40 * u * (1 - spot); girl(c, gx, gy(gx), 1.6, t, 1 - spot)
        rx = 930; c.save(); c.translate(rx, gy(rx)); c.rotate(-80)  # him, lying exhausted on the far crest
        walker(c, 0, 0, 1.3, 0); c.restore()
        if spot > 0: glow(c, rx - 10, gy(rx) - 30, 120, (255, 230, 170), 0.5 * spot)
        big_center(c, 'DAY 9', 'Found.', ss(wat('spots', L[10][0]), wat('spots', L[10][0]) + 0.5, t), 700, cc=(255, 240, 220))
        out_k = ss(s8 - 0.3, s8, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((236, 214, 175), out_k))
        return
    # ---------- shot 8: painted map, 180 miles into Algeria, -33 lb ----------
    if t < s9:
        u = t - s8
        vgrad(c, None, None, 0, H, [0, 1], [col((240, 222, 186)), col((225, 200, 160))])
        mor = skia.Path(); mor.moveTo(-50, -50); mor.lineTo(500, -50); mor.lineTo(520, 380); mor.lineTo(600, 760); mor.lineTo(480, 1350); mor.lineTo(420, H + 50); mor.lineTo(-50, H + 50); mor.close()
        alg = skia.Path(); alg.moveTo(500, -50); alg.lineTo(1150, -50); alg.lineTo(1150, H + 50); alg.lineTo(420, H + 50); alg.lineTo(480, 1350); alg.lineTo(600, 760); alg.lineTo(520, 380); alg.close()
        c.drawPath(mor, P((228, 170, 120))); c.drawPath(alg, P((214, 150, 105)))
        bp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5); bp.setColor(col((120, 70, 50), 0.7)); bp.setPathEffect(skia.DashPathEffect.Make([18, 12], 0))
        b = skia.Path(); b.moveTo(500, -50); b.lineTo(520, 380); b.lineTo(600, 760); b.lineTo(480, 1350); b.lineTo(420, H + 50); c.drawPath(b, bp)
        lf = F(FD + 'Inter-Bold.otf', 34)
        c.drawString('MOROCCO', 120, 980, lf, P((120, 60, 40), 0.8)); c.drawString('ALGERIA', 760, 1180, lf, P((110, 55, 40), 0.8))
        pts = [(260, 880), (360, 820), (430, 900), (560, 880), (650, 960), (720, 900), (820, 1000)]
        k = ss(L[11][0], L[11][1] - 0.2, t); n = min(len(pts) - 1.001, 1 + k * (len(pts) - 2))
        rp = skia.Path(); rp.moveTo(*pts[0])
        for i in range(1, int(n) + 1): rp.lineTo(*pts[i])
        if n % 1 > 0 and int(n) + 1 < len(pts):
            a_, b_ = pts[int(n)], pts[int(n) + 1]; f_ = n % 1; rp.lineTo(a_[0] + (b_[0] - a_[0]) * f_, a_[1] + (b_[1] - a_[1]) * f_)
        rr = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9, StrokeCap=skia.Paint.kRound_Cap); rr.setColor(col(CRED_ if False else (200, 40, 50)))
        rr.setPathEffect(skia.DashPathEffect.Make([4, 18], 0)); c.drawPath(rp, rr)
        c.drawCircle(*pts[0], 14, P((40, 30, 30)))
        c.drawString('RACE', pts[0][0] - 40, pts[0][1] + 50, SMALL, P((60, 30, 25)))
        big_center(c, 'HE WANDERED', '180 Miles', ss(wat('hundred', L[11][0]) - 0.1, wat('hundred', L[11][0]) + 0.4, t) * (1 - ss(L[12][0] - 0.3, L[12][0], t)), 620, cc=(110, 40, 30))
        big_center(c, 'HE LOST', '33 lbs', ss(L[12][0], L[12][0] + 0.4, t), 620, cc=(170, 35, 40))
        out_k = ss(s9 - 0.3, s9, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((255, 225, 170), out_k))
        return
    # ---------- shot 9: he ran that race again ----------
    if t < s10:
        u = t - s9
        vgrad(c, None, None, 0, 1400, [0, .65, 1], [col((110, 170, 230)), col((240, 210, 170)), col((255, 220, 170))])
        glow(c, 820, 420, 300, (255, 250, 220), 0.6); c.drawCircle(820, 420, 70, P((255, 250, 230)))
        fill_dune(c, dune(13, 1150, 120, u * 20), (240, 180, 120), (215, 150, 100), haze=(255, 230, 190), haze_a=0.3)
        nd = dune(14, 1370, 160, u * 60 + 900)
        fill_dune(c, nd, (225, 140, 80), (140, 60, 40), rim=(255, 240, 200), rim_a=0.9)
        for i in range(7):
            x = (100 + i * 150 + u * 70) % 1180 - 50
            walker(c, x, min(nd, key=lambda q: abs(q[0] - x))[1] + 2, 1.0, t + i * 0.37, a=1.0 if i == 3 else 0.75)
        big_center(c, 'HE RAN IT AGAIN', '6 More Times', ss(wat('six', L[13][0]) - 0.15, wat('six', L[13][0]) + 0.4, t), 700, cc=(110, 40, 30), size=170)
        out_k = ss(s10 - 0.3, s10, t)
        if out_k > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((60, 30, 50), out_k))
        return
    # ---------- shot 10: the question ----------
    u = t - s10
    vgrad(c, None, None, 0, 1400, [0, .5, .85, 1], [col((30, 24, 60)), col((130, 55, 75)), col((235, 120, 70)), col((255, 180, 110))])
    stars(c, 0.5)
    glow(c, 540, 1080, 460, (255, 170, 100), 0.5); c.drawCircle(540, 1080, 95, P((255, 205, 150)))
    fill_dune(c, dune(15, 1200, 130, u * 15), (180, 85, 70), (120, 50, 55), haze=(240, 140, 110), haze_a=0.3)
    nd = dune(16, 1390, 180, u * 30 + 100)
    fill_dune(c, nd, (110, 45, 40), (40, 18, 25), rim=(255, 170, 110), rim_a=0.9)
    wx = 540 + 10 * u; walker(c, wx, min(nd, key=lambda q: abs(q[0] - wx))[1] + 2, 1.1, t)
    big_center(c, 'SO...', 'Would you', ss(s10 + 0.3, s10 + 0.8, t), 560, cc=(255, 236, 200), size=170)
    big_center(c, None, 'have survived?', ss(s10 + 0.6, s10 + 1.1, t), 730, cc=(255, 214, 120), size=150)
    cta = 'SUBSCRIBE FOR MORE TRUE STORIES' if PLAT == 'yt' else "SEND THIS TO SOMEONE WHO'D MAKE IT"
    k = ss(T[-1][1] - 0.2, T[-1][1] + 0.4, t)
    if k > 0:
        cf = F(FD + 'Inter-Bold.otf', 32); c.drawString(cta, W / 2 - cf.measureText(cta) / 2, 840, cf, P((255, 255, 255), k))
    fade = ss(DUR - 0.6, DUR, t)
    if fade > 0: c.drawRect(skia.Rect.MakeWH(W, H), P((0, 0, 0), fade))


def main():
    out = os.path.join(D, 'v_%s.mp4' % PLAT); n = int(DUR * FPS)
    ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    for f in range(n):
        t = f / FPS; c = surf.getCanvas(); c.clear(skia.ColorBLACK)
        frame(c, t); grain(c); subs(c, t)
        c.drawImage(WM, 0, 0)
        ff.stdin.write(surf.makeImageSnapshot().tobytes())
        if f % 60 == 0: print('frame', f, n, flush=True)
    ff.stdin.close(); ff.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-i', os.path.join(D, 'mix_fx.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', os.path.join(D, 'Lost_In_The_Sahara_%s.mp4' % PLAT)], check=True)
    print('done')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'still':
        for ts in sys.argv[3:]:
            s = skia.Surface(W, H); c = s.getCanvas(); t = float(ts); frame(c, t); grain(c); subs(c, t); c.drawImage(WM, 0, 0)
            s.makeImageSnapshot().save(os.path.join(D, 'still_%05.2f.png' % t), skia.kPNG)
    else:
        main()
