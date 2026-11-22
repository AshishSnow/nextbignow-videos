# ------------------------------------------------------------------ props (generic warehouse club: no logos, colors or trade dress)
def member_card(c, x, y, w, rot, t=0.0, glow_=0.0):
    h = w * 0.63; c.save(); c.translate(x, y); c.rotate(rot)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), w * 0.06, w * 0.06)
    if glow_ > 0: c.drawRRect(r, P((255, 230, 120), 0.7 * glow_, w * 0.12))
    c.drawRRect(r.makeOffset(w * 0.03, w * 0.04), P(INK, 0.3, 6)); inked(c, r, P((255, 255, 255)), max(3, w * 0.014))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2 + h * 0.1, w, h * 0.2), P((255, 190, 30)))
    ctext(c, 'MEMBER', 0, -h / 2 + h * 0.26, w * 0.1, (34, 32, 30), 'Anton.ttf')
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w * 0.42, -h * 0.05, w * 0.26, h * 0.42), 8, 8), P((210, 210, 215)), 3)
    for i in range(3): c.drawLine(-w * 0.08, h * 0.02 + i * h * 0.12, w * 0.4, h * 0.02 + i * h * 0.12, S((150, 150, 160), max(2, w * 0.012)))
    c.restore()


def hotdog(c, x, y, s=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -30, 300, 70), 35, 35), P((230, 180, 110)), 6)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -40, 340, 40), 20, 20), P((200, 90, 70)), 6)
    p = skia.Path(); p.moveTo(-130, -22)
    for i in range(1, 12): p.lineTo(-130 + i * 24, -22 + (8 if i % 2 else -8))
    c.drawPath(p, S((255, 214, 40), 7)); c.restore()


def cart_big(c, x, y, s, t):
    cart(c, x, y, s, 1.0, t)


def warehouse2(c, x, y, w, h, t):
    c.drawRect(skia.Rect.MakeXYWH(x + 14, y + 14, w, h), P((0, 0, 0), 0.3, 10))
    inked(c, skia.Rect.MakeXYWH(x, y, w, h), LG((0, y), (0, y + h), [(220, 225, 235), (180, 190, 205)]), 7)
    for i in range(1, 9): c.drawLine(x + i * w / 9, y + 10, x + i * w / 9, y + h - 10, S((150, 160, 175), 3))
    inked(c, skia.Rect.MakeXYWH(x + w * 0.38, y + h * 0.55, w * 0.24, h * 0.45), P((120, 130, 150)), 5)
    board(c, x + w * 0.15, y + h * 0.1, w * 0.7, h * 0.24); neon_text(c, 'WAREHOUSE CLUB', x + w / 2, y + h * 0.27, 50, (34, 32, 30))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    tc = ph('membership card')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Costco sells cheap,', False, (34, 32, 30), 100), ('profits on the card,', False, (34, 32, 30), 96), ('explained.', True, (150, 22, 34), 112)), 'in 40 seconds', "per Costco's 2025 results")
    cart(c, 320, 1200, 0.75, 1.0, t)
    if t > tc - 0.4: pop(c, pr(t, tc - 0.4, 0.4), 780, 1000, lambda: member_card(c, 780, 1000, 380, -8, t, 0.8))
    person(c, 600, 1780, 0.48, (255, 140, 40), (36, 44, 90), mood='shock' if t > tc else 'happy', look=(0.4, -0.6), t=t, blink=blinking(t))


def s_profit(c, t):
    t81 = ph('eight point one'); t53 = ph('five point three'); tt = ph('two thirds')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'COSTCO, FISCAL 2025', 540, 352, 64, (34, 32, 30))
    ctext(c, 'SOURCE: COSTCO FY2025 OPERATING RESULTS', 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t81 - 0.3, 0.8), pr(t, t53 - 0.3, 0.8), 'NET PROFIT', 'MEMBER FEES', '$8.1B', '$5.3B', 8.1 * 70, 5.32 * 70, (150, 150, 160), (255, 190, 30), pr(t, tt - 0.2, 0.3), '= ~2/3 OF PROFIT')


def s_sales(c, t):
    ts = ph('two hundred seventy'); tp = ph('on purpose')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'ALL THAT SELLING...', 540, 358, 66, (34, 32, 30))
    warehouse2(c, 140, 600, 800, 520, t)
    if t > ts - 0.3: pop(c, pr(t, ts - 0.3, 0.4), 540, 1250, lambda: (board(c, 170, 1190, 740, 120, (255, 255, 255)), neon_text(c, '$270B OF SALES', 540, 1275, 70, (34, 32, 30))))
    if t > tp - 0.3:
        c.save(); c.translate(720, 560); c.rotate(-6); r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-170, -50, 340, 100), 14, 14); c.drawRRect(r, S((200, 40, 40), 8, 0.9)); ctext(c, 'LOW ON PURPOSE', 0, 18, 44, (230, 40, 50), 'Anton.ttf'); c.restore()


def s_gym(c, t):
    tb = ph('protein bars'); tm = ph('the membership pays')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE A GYM", 540, 358, 66, (34, 32, 30))
    c.drawLine(200, 760, 520, 760, S(INK, 16)); c.drawRoundRect(skia.Rect.MakeXYWH(160, 690, 60, 140), 12, 12, P((60, 60, 70))); c.drawRoundRect(skia.Rect.MakeXYWH(500, 690, 60, 140), 12, 12, P((60, 60, 70)))
    if t > tb - 0.3:
        def bars_():
            for i in range(3):
                inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(640, 640 + i * 90, 300, 70), 16, 16), P((200, 130, 70)), 5); ctext(c, '$1', 790, 690 + i * 90, 40, (255, 255, 255), 'Anton.ttf')
        pop(c, pr(t, tb - 0.3, 0.4), 790, 740, bars_)
    if t > tm - 0.3: pop(c, pr(t, tm - 0.3, 0.4), 540, 1080, lambda: (member_card(c, 540, 1060, 420, 4, t, 0.8)))
    person(c, 300, 1780, 0.5, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.5, -0.5), t=t, arm_r=(150, -200), blink=blinking(t))


def s_end(c, t):
    th = ph('hot dogs')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'NOT REALLY A STORE...', 540, 358, 60, (34, 32, 30))
    member_card(c, 540, 760, 560, -4, t, 0.6)
    if t > th - 0.5:
        pop(c, pr(t, th - 0.5, 0.4), 540, 1130, lambda: hotdog(c, 540, 1130, 1.1, -4))
        pop(c, pr(t, th - 0.2, 0.3), 540, 1300, lambda: (board(c, 170, 1240, 740, 110, (255, 214, 40)), neon_text(c, 'A CLUB THAT SELLS HOT DOGS', 540, 1318, 46, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('last fiscal year') - 0.15, s_profit), (ph('but to make') - 0.15, s_sales), (ph("it's like a gym") - 0.15, s_gym), (ph("so costco isn't") - 0.15, s_end)]
SHAKES = [(ph('membership card'), 10, 0.35), (ph('five point three'), 16, 0.45), (ph('two hundred seventy'), 12, 0.4), (ph('hot dogs'), 10, 0.35)]
TR = 0.32
