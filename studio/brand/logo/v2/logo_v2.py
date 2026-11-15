"""OopsMyBusiness logo v2 — three thought-through marks, each 6 colours, with icon + horizontal lockup."""
import skia, math, numpy as np, cv2
FD = '/home/claude/studio/fonts/ttf/'
def tf(n): return skia.Typeface.MakeFromFile(FD + n)
def F(n, s): f = skia.Font(tf(n), s); f.setEdging(skia.Font.Edging.kAntiAlias); return f
def P(c, a=1.0): p = skia.Paint(AntiAlias=True); p.setColor(skia.Color(*c, int(255 * a))); return p
def ST(c, w): p = P(c); p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeJoin(skia.Paint.kRound_Join); p.setStrokeCap(skia.Paint.kRound_Cap); return p
INK = (24, 22, 30); CREAM = (255, 247, 230)
BLUE, TEAL, GRN, YEL, ORG, PINK, PURP = (37, 99, 235), (13, 160, 150), (34, 177, 92), (255, 200, 20), (255, 122, 26), (244, 84, 150), (124, 72, 214)
SIX = (BLUE, TEAL, GRN, YEL, ORG, PINK)
OUT = '/home/claude/studio/projects/omb-logo/v2/'

def save(s, n): cv2.imwrite(OUT + n + '.png', np.ascontiguousarray(s.makeImageSnapshot().toarray()[..., :4]))

def text(c, s, x, y, f, col, outline=0, sh=0):
    if sh: c.drawString(s, x + sh, y + sh, f, P(INK))
    if outline: c.drawString(s, x, y, f, ST(INK, outline))
    c.drawString(s, x, y, f, P(col))

def multiword(c, s, x, y, f, cols, outline=0, sh=0, gap=0):
    for i, ch in enumerate(s):
        text(c, ch, x, y, f, cols[i % len(cols)], outline, sh); x += f.measureText(ch) + gap
    return x

# ---------------- MARK 1: the "Oops Shop" — striped awning (6 colours), one scallop falling; the door is an "!"
def mark_shop(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    # shop body
    body = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-230, -40, 460, 300), 34, 34)
    c.save(); c.translate(14, 14); c.drawRRect(body, P(INK)); c.restore(); c.drawRRect(body, P(CREAM)); c.drawRRect(body, ST(INK, 16))
    # door = exclamation mark
    door = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-46, 40, 92, 150), 46, 46); c.drawRRect(door, P(INK))
    c.drawCircle(0, 228, 24, P(INK))
    # windows
    for wx in (-170, 100):
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx, 40, 70, 90), 16, 16); c.drawRRect(r, P((200, 230, 255))); c.drawRRect(r, ST(INK, 10))
    # awning: 6 stripes with scallops
    top, bot = -200, -60; n = 6; w = 520 / n
    c.save(); c.translate(10, 10)
    pth = skia.Path(); pth.moveTo(-260, top); pth.lineTo(260, top); pth.lineTo(260, bot); pth.lineTo(-260, bot); pth.close(); c.drawPath(pth, P(INK)); c.restore()
    for i, col in enumerate(SIX):
        x0 = -260 + i * w
        c.drawRect(skia.Rect.MakeXYWH(x0, top, w + 1, bot - top), P(col))
        if i != 4:  # scallop
            c.drawOval(skia.Rect.MakeXYWH(x0, bot - 40, w, 80), P(col))
    for i in range(n + 1): c.drawLine(-260 + i * w, top, -260 + i * w, bot, ST(INK, 8))
    rr = skia.Path(); rr.moveTo(-260, top); rr.lineTo(260, top); rr.lineTo(260, bot); rr.lineTo(-260, bot); rr.close(); c.drawPath(rr, ST(INK, 16))
    for i in range(n):
        if i != 4: c.drawArc(skia.Rect.MakeXYWH(-260 + i * w, bot - 40, w, 80), 0, 180, False, ST(INK, 12))
    # the falling scallop ("oops")
    c.save(); c.translate(330, bot + 120); c.rotate(38)
    c.drawOval(skia.Rect.MakeXYWH(-w / 2, -40, w, 80), P(ORG)); c.drawOval(skia.Rect.MakeXYWH(-w / 2, -40, w, 80), ST(INK, 12)); c.restore()
    for i in range(3): c.drawLine(262 + i * 26, bot + 10 + i * 6, 288 + i * 26, bot + 50 + i * 6, ST(INK, 9))
    c.restore()

# ---------------- MARK 2: "Tumble chart" — 6 rising bars, the top block tumbling off with a spark
def mark_bars(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    base = 230; bw = 66; gap = 14
    heights = (80, 130, 180, 230, 290, 330)
    for i, (h, col) in enumerate(zip(heights, SIX)):
        bx = -250 + i * (bw + gap); hh = h if i < 5 else h - 90
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bx, base - hh, bw, hh), 14, 14)
        c.save(); c.translate(10, 10); c.drawRRect(r, P(INK)); c.restore(); c.drawRRect(r, P(col)); c.drawRRect(r, ST(INK, 12))
    # tumbling top block of the last bar
    c.save(); c.translate(-250 + 5 * (bw + gap) + bw / 2 + 50, base - 330 - 50); c.rotate(32)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-bw / 2, -45, bw, 90), 14, 14); c.save(); c.translate(10, 10); c.drawRRect(r, P(INK)); c.restore(); c.drawRRect(r, P(PINK)); c.drawRRect(r, ST(INK, 12)); c.restore()
    for a in (-60, -20, 20):  # spark lines
        ax = -250 + 5 * (bw + gap) + 10; ay = base - 240
        c.drawLine(ax + 40 * math.cos(math.radians(a - 90)), ay + 40 * math.sin(math.radians(a - 90)), ax + 80 * math.cos(math.radians(a - 90)), ay + 80 * math.sin(math.radians(a - 90)), ST(INK, 10))
    c.drawLine(-280, base + 6, 260, base + 6, ST(INK, 16))
    c.restore()

# ---------------- MARK 3: "Oops bubble" — speech bubble "O" with a shocked face; 6-colour ring of confetti
def mark_bubble(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for i, col in enumerate(SIX):
        a = math.radians(-150 + i * 40); rx, ry = 300 * math.cos(a), 270 * math.sin(a)
        c.save(); c.translate(rx, ry - 20); c.rotate(i * 37); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -14, 60, 28), 8, 8)
        c.drawRRect(r, P(col)); c.drawRRect(r, ST(INK, 7)); c.restore()
    b = skia.Path(); b.addOval(skia.Rect.MakeXYWH(-210, -220, 420, 400))
    tail = skia.Path(); tail.moveTo(-90, 140); tail.lineTo(-170, 250); tail.lineTo(10, 168); tail.close()
    bb = skia.Op(b, tail, skia.PathOp.kUnion_PathOp)
    c.save(); c.translate(14, 14); c.drawPath(bb, P(INK)); c.restore(); c.drawPath(bb, P(YEL)); c.drawPath(bb, ST(INK, 16))
    for ex in (-80, 80):
        c.drawCircle(ex, -50, 46, P(CREAM)); c.drawCircle(ex, -50, 46, ST(INK, 10)); c.drawCircle(ex + 6, -44, 20, P(INK))
    c.drawOval(skia.Rect.MakeXYWH(-40, 30, 80, 96), P(INK)); c.drawOval(skia.Rect.MakeXYWH(-22, 70, 44, 40), P(PINK))
    c.restore()

def wordmark(c, x, y, size, cols, sub_col=INK, stacked=False):
    f = F('LuckiestGuy.ttf', size); fs = F('Montserrat-Black.ttf', size * 0.34)
    end = multiword(c, 'OOPS', x, y, f, cols, outline=size * 0.11, sh=size * 0.07)
    text(c, '!', end + 4, y, f, cols[-1], outline=size * 0.11, sh=size * 0.07)
    sub = 'MY BUSINESS'; sp = size * 0.06
    xx = x + 6
    for ch in sub: c.drawString(ch, xx, y + size * 0.55, fs, P(sub_col)); xx += fs.measureText(ch) + sp
    return end

MARKS = (('1_oops_shop', mark_shop, (BLUE, ORG, GRN, PINK, TEAL)), ('2_tumble_chart', mark_bars, (TEAL, BLUE, ORG, PINK, GRN)), ('3_oops_bubble', mark_bubble, (PURP, ORG, BLUE, PINK, GRN)))
for name, fn, cols in MARKS:
    # icon (square, transparent)
    s = skia.Surface(1024, 1024); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0)); fn(c, 512, 540, 1.35); save(s, name + '_icon')
    # icon on round avatar
    s = skia.Surface(1024, 1024); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0)); c.drawCircle(512, 512, 500, P(CREAM)); c.drawCircle(512, 512, 494, ST(INK, 12)); fn(c, 512, 540, 1.05); save(s, name + '_avatar')
    # horizontal lockup
    s = skia.Surface(2400, 900); c = s.getCanvas(); c.clear(skia.Color(0, 0, 0, 0)); fn(c, 430, 470, 1.15); wordmark(c, 1010, 470, 260, cols); save(s, name + '_lockup')

# presentation board
board = skia.Surface(2400, 3000); c = board.getCanvas(); c.clear(skia.Color(*CREAM, 255))
for i, (name, fn, cols) in enumerate(MARKS):
    y0 = 80 + i * 980
    c.drawString(('1  THE OOPS SHOP: a 6-colour storefront awning, one scallop falls off, the door is an "!"',
                  '2  TUMBLE CHART: 6 bars of growth, the top block tumbles (the "oops"), business keeps climbing',
                  '3  OOPS BUBBLE: a shocked speech-bubble face, 6 confetti pieces of colour')[i], 60, y0, F('Montserrat-ExtraBold.ttf', 40), P(INK))
    c.save(); c.translate(0, y0 + 40); c.scale(0.95, 0.95); fn(c, 420, 450, 1.05); wordmark(c, 960, 450, 240, cols); c.restore()
    # small avatar preview
    c.drawCircle(2180, y0 + 330, 150, P((255, 255, 255))); c.drawCircle(2180, y0 + 330, 150, ST(INK, 8)); fn(c, 2180, y0 + 345, 0.32)
    c.drawString('profile pic', 2100, y0 + 520, F('Montserrat-SemiBold.ttf', 30), P(INK))
im = board.makeImageSnapshot().toarray()[..., :3]
cv2.imwrite(OUT + '0_logo_board.png', np.ascontiguousarray(im)); print('ok')
