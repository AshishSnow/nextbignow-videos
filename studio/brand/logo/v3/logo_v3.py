"""OopsMyBusiness logo v3 — fewer colours (navy + one accent), one clear idea per mark."""
import skia, math, numpy as np, cv2
FD = '/home/claude/studio/fonts/ttf/'
def F(n, s): f = skia.Font(skia.Typeface.MakeFromFile(FD + n), s); f.setEdging(skia.Font.Edging.kAntiAlias); return f
def P(c): p = skia.Paint(AntiAlias=True); p.setColor(skia.Color(*c)); return p
def ST(c, w, cap=True):
    p = P(c); p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(w); p.setStrokeJoin(skia.Paint.kRound_Join)
    p.setStrokeCap(skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap); return p
NAVY = (18, 28, 61); YEL = (255, 190, 0); CORAL = (255, 90, 80); CREAM = (250, 246, 236); WHITE = (255, 255, 255)
OUT = '/home/claude/studio/projects/omb-logo/v3/'
def save(s, n, alpha=True):
    im = np.ascontiguousarray(s.makeImageSnapshot().toarray()[..., :4 if alpha else 3]); cv2.imwrite(OUT + n + '.png', im)

# ---- MARK A: "Chipped O!" — a bold O with a chip knocked out (the oops), the "!" inside the O
def mark_o(c, x, y, s, ring=NAVY, acc=YEL):
    c.save(); c.translate(x, y); c.scale(s, s)
    r = 200; w = 78; rect = skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r)
    p = skia.Path(); p.addArc(rect, 62, 328); c.drawPath(p, ST(ring, w, cap=False))      # gap at ~4 o'clock (34..62 deg)
    mx, my = r * math.cos(math.radians(48)), r * math.sin(math.radians(48))
    c.save(); c.translate(mx + 48, my + 40); c.rotate(26); c.translate(-mx, -my)   # the chip, knocked just out of the O
    ch = skia.Path(); ch.addArc(rect, 37, 22); c.drawPath(ch, ST(ring, w, cap=False)); c.restore()
    for i in range(3): c.drawLine(mx + 120 + i * 4, my - 40 + i * 30, mx + 160 + i * 4, my - 56 + i * 30, ST(acc, 12))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-30, -120, 60, 150), 30, 30), P(acc))
    c.drawCircle(0, 80, 33, P(acc))
    c.restore()


# ---- MARK B: "Loop arrow" — a growth arrow that trips into a loop (the oops) and keeps climbing
def mark_loop(c, x, y, s, line=NAVY, acc=YEL):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = skia.Path(); p.moveTo(-300, 170)
    p.cubicTo(-200, 160, -110, 110, -40, 40)            # rising
    p.cubicTo(30, -40, 150, -60, 150, 40)               # into the loop
    p.cubicTo(150, 150, -10, 160, -30, 60)
    p.cubicTo(-30, -10, 60, -90, 270, -200)             # out of the loop, climbing
    c.drawPath(p, ST(line, 52))
    head = skia.Path(); head.moveTo(300, -225); head.lineTo(175, -215); head.lineTo(260, -120); head.close()
    c.drawPath(head, P(acc)); c.drawPath(head, ST(acc, 18))
    c.restore()

# ---- MARK C: "Slipped S" — OOPS with the S slipping off the baseline
def mark_slip(c, x, y, size, col=NAVY, acc=YEL):
    f = F('Montserrat-Black.ttf', size); s0 = 'OOP'; w0 = f.measureText(s0) - size * 0.04 * 2
    xx = x
    for ch in s0: c.drawString(ch, xx, y, f, P(col)); xx += f.measureText(ch) - size * 0.04
    c.save(); c.translate(xx + size * 0.30, y - size * 0.28); c.rotate(24); c.drawString('S', -size * 0.30, size * 0.28 + size * 0.10, f, P(acc)); c.restore()
    for i in range(3): c.drawLine(xx + size * 0.66 + i * 18, y - size * 0.62 + i * 26, xx + size * 0.80 + i * 18, y - size * 0.58 + i * 26, ST(col, 12))
    return xx + size * 0.8

def wordmark(c, x, y, size, col=NAVY, acc=YEL, light=False):
    f = F('Montserrat-Black.ttf', size)
    a = 'Oops'; b = 'MyBusiness'
    c.drawString(a, x, y, f, P(acc)); c.drawString(b, x + f.measureText(a) + size * 0.02, y, f, P(WHITE if light else col))

def board_row(c, y0, label, desc, icon_fn, lockup_fn):
    c.drawString(label, 80, y0, F('Montserrat-Black.ttf', 54), P(NAVY))
    c.drawString(desc, 80, y0 + 58, F('Montserrat-Medium.ttf', 34), P((70, 76, 96)))
    # light tile
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(80, y0 + 100, 1500, 520), 30, 30), P(WHITE))
    lockup_fn(c, 80, y0 + 100, False)
    # dark avatar tile
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1620, y0 + 100, 520, 520), 30, 30), P(NAVY))
    c.drawCircle(1880, y0 + 360, 210, P(CREAM)); icon_fn(c, 1880, y0 + 365, 0.62)
    c.drawString('profile picture', 1760, y0 + 600, F('Montserrat-SemiBold.ttf', 28), P(CREAM))

def lockA(c, x, y, dark):
    mark_o(c, x + 300, y + 260, 0.95, ring=CREAM if dark else NAVY); wordmark(c, x + 620, y + 300, 88, light=dark)
    c.drawString('BUSINESS STORIES . CASE STUDIES', x + 626, y + 360, F('Montserrat-SemiBold.ttf', 30), P((120, 126, 146)))
def lockB(c, x, y, dark):
    mark_loop(c, x + 300, y + 280, 0.8, line=CREAM if dark else NAVY); wordmark(c, x + 600, y + 300, 88, light=dark)
    c.drawString('BUSINESS STORIES . CASE STUDIES', x + 606, y + 360, F('Montserrat-SemiBold.ttf', 30), P((120, 126, 146)))
def lockC(c, x, y, dark):
    mark_slip(c, x + 120, y + 330, 250, col=CREAM if dark else NAVY)
    c.drawString('MY BUSINESS', x + 130, y + 420, F('Montserrat-Black.ttf', 70), P(CREAM if dark else NAVY))
def iconC(c, x, y, s):  # icon for C = the slipping S alone
    f = F('Montserrat-Black.ttf', 420 * s); c.save(); c.translate(x, y); c.rotate(24); w = f.measureText('S'); c.drawString('S', -w / 2, 150 * s, f, P(YEL)); c.restore()
    for i in range(3): c.drawLine(x + (120 + i * 26) * s, y - (190 - i * 34) * s, x + (190 + i * 26) * s, y - (170 - i * 34) * s, ST(NAVY, 14 * s))

B = skia.Surface(2240, 2300); c = B.getCanvas(); c.clear(skia.Color(*CREAM, 255))
c.drawString('OOPS MY BUSINESS . LOGO DIRECTIONS (2 colours: navy + yellow)', 80, 110, F('Montserrat-Black.ttf', 46), P(NAVY))
board_row(c, 230, 'A  "CHIPPED O!"', 'An O with a chip knocked out = the oops. The "!" inside = the surprise. Works tiny as a favicon.', lambda c, x, y, s: mark_o(c, x, y, s), lockA)
board_row(c, 950, 'B  "LOOP ARROW"', 'A growth arrow that trips into a loop, then keeps climbing. Every oops is part of the growth story.', lambda c, x, y, s: mark_loop(c, x, y, s), lockB)
board_row(c, 1670, 'C  "SLIPPED S"', 'Pure type: OOPS, with the S slipping off the line. The mistake is built into the name.', iconC, lockC)
save(B, '0_logo_board_v3', alpha=False)

for name, icon, lock in (('A_chipped_O', lambda c, x, y, s: mark_o(c, x, y, s), lockA), ('B_loop_arrow', lambda c, x, y, s: mark_loop(c, x, y, s), lockB), ('C_slipped_S', iconC, lockC)):
    s = skia.Surface(1024, 1024); cc = s.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0)); icon(cc, 512, 530, 1.5); save(s, name + '_icon')
    s = skia.Surface(1024, 1024); cc = s.getCanvas(); cc.clear(skia.Color(0, 0, 0, 0)); cc.drawCircle(512, 512, 512, P(CREAM)); icon(cc, 512, 530, 1.25); save(s, name + '_avatar')
    for dark in (False, True):
        s = skia.Surface(1700, 620); cc = s.getCanvas(); cc.clear(skia.Color(*(NAVY if dark else WHITE), 255)); lock(cc, 0, 50, dark); save(s, name + ('_lockup_dark' if dark else '_lockup'), alpha=False)
print('ok')
