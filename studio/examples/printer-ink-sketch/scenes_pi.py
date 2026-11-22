def bars2(c, t, kA, kB, labA, labB, valA, valB, hA, hB, colA=(255, 120, 60), colB=(40, 190, 110), cmp_k=0, cmp_txt=''):
    base = 1180
    def col(x, val, h, rgb, lab, k):
        if k <= 0: return
        hh = h * eo(k)
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, base - hh, 300, hh), 18, 18)
        c.drawRRect(r.makeOffset(10, 12), P(INK, 0.25, 6)); inked(c, r, LG((x, base - hh), (x, base), [tuple(min(255, v + 60) for v in rgb), rgb]), 7)
        neon_text(c, val, x + 150, base - hh - 30, 70, rgb, cl(k * 2))
        neon_text(c, lab, x + 150, base + 70, 38, (255, 255, 255))
    inked(c, skia.Rect.MakeXYWH(60, base, 960, 14), P((255, 255, 255)), 5)
    col(140, valA, hA, colA, labA, kA); col(640, valB, hB, colB, labB, kB)
    if cmp_k > 0:
        pop(c, cmp_k, 540, 1610, lambda: (board(c, 250, 1550, 580, 110, (255, 236, 90)), neon_text(c, cmp_txt, 540, 1628, 64, (255, 70, 90))))



# ------------------------------------------------------------------ printer props (generic: no real logos or product designs)
def printer(c, x, y, s=1.0, paper_k=0.0, t=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-230 + 12, -60 + 14, 460, 200), P(INK, 0.25, 8))
    inked(c, path([(-150, -60), (150, -60), (120, -150), (-120, -150)]), P((235, 235, 235)), 6)          # paper tray in
    for i in range(3): c.drawLine(-100 + i * 10, -140 + i * 25, 100 - i * 10, -140 + i * 25, S((190, 190, 190), 3))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-230, -60, 460, 200), 26, 26), LG((0, -60), (0, 140), [(250, 250, 250), (200, 200, 205)]), 7)
    inked(c, skia.Rect.MakeXYWH(-170, 60, 340, 30), P((60, 60, 70)), 5)                                      # paper slot
    c.drawCircle(170, -20, 14, P((60, 200, 120))); c.drawCircle(170, -20, 14, S(INK, 4))
    for i in range(3): c.drawRoundRect(skia.Rect.MakeXYWH(60 + i * 30, -30, 20, 20), 4, 4, P((140, 140, 150)))
    if paper_k > 0:
        hh = 220 * eo(paper_k); inked(c, skia.Rect.MakeXYWH(-140, 75, 280, hh), P((255, 255, 255)), 5)
        for i in range(int(hh / 36)): c.drawLine(-110, 110 + i * 36, 90 - (i % 2) * 50, 110 + i * 36, S((160, 160, 170), 4))
    c.restore()


def cartridge(c, x, y, s=1.0, rot=0, col=(40, 40, 50), lab='INK'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.drawRect(skia.Rect.MakeXYWH(-70 + 10, -110 + 12, 140, 220), P(INK, 0.25, 6))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-70, -110, 140, 220), 14, 14), LG((0, -110), (0, 110), [tuple(min(255, v + 70) for v in col), col]), 6)
    inked(c, skia.Rect.MakeXYWH(-40, 110, 80, 26), P((90, 90, 100)), 5)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-52, -60, 104, 70), 8, 8), P((255, 255, 255)), 4)
    ctext(c, lab, 0, -12, 34, (40, 40, 50), 'Anton.ttf')
    c.restore()


def razor(c, x, y, s=1.0, rot=0, k_blades=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-34, -20, 68, 420), 30, 30), LG((-34, 0), (34, 0), [(220, 220, 230), (150, 150, 165)]), 7)
    for i in range(6): c.drawLine(-22, 80 + i * 40, 22, 80 + i * 40, S((120, 120, 130), 4))
    if k_blades > 0:
        c.save(); c.translate(0, -40); c.scale(k_blades, k_blades)
        inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-150, -60, 300, 70), 14, 14), P((70, 140, 230)), 7)
        for i in range(3): c.drawLine(-135, -45 + i * 18, 135, -45 + i * 18, S((235, 240, 250), 5))
        c.restore()
    c.restore()


def quote_card(c, x, y, w, lines, k, col=(34, 32, 30), src=''):
    if k <= 0: return
    h = 160 + 70 * len(lines)
    c.save(); c.translate(x, y); s_ = 0.9 + 0.1 * eo(k); c.scale(s_, s_)
    board(c, -w / 2, -h / 2, w, h)
    f = serif(140, 700); c.drawString('“', -w / 2 + 30, -h / 2 + 120, f, P((190, 135, 30), cl(k * 2)))
    for i, ln in enumerate(lines):
        f = serif(52, 400, True); tw = f.measureText(ln); c.drawString(ln, -tw / 2, -h / 2 + 110 + i * 70, f, P(col, cl(k * 2)))
    if src:
        f = serif(28, 400); tw = f.measureText(src); c.drawString(src, -tw / 2, h / 2 - 28, f, P((90, 86, 80), cl(k * 2)))
    c.restore()


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    sky_bg(c, t)
    c.save(); c.translate(540, 235); c.rotate(-2); c.drawRect(skia.Rect.MakeXYWH(-190, -42, 380, 76), P((212, 160, 46))); f = serif(44, 400, True); tw = f.measureText('in 40 seconds'); c.drawString('in 40 seconds', -tw / 2, 14, f, P((34, 32, 30))); c.restore()
    for i, (txt, it, col) in enumerate((('Your printer', False, (34, 32, 30)), ('was never the point,', False, (34, 32, 30)), ('explained.', True, (150, 22, 34)))):
        f = serif(100 if i == 0 else 84 if i == 1 else 112, 700 if not it else 500, it); tw = f.measureText(txt)
        c.drawString(txt, 540 - tw / 2, 385 + i * 112, f, P(col, pr(t, i * 0.25, 0.3)))
    f = serif(40, 400); s_ = "per HP's 2025 annual report"; c.drawString(s_, 540 - f.measureText(s_) / 2, 680, f, P((90, 86, 80), pr(t, 0.8, 0.3)))
    printer(c, 420, 1030, 1.1, pr(t, 0.6, 1.2), t)
    tk = ph('your ink')
    if t > tk - 0.3:
        for i in range(3): pop(c, pr(t, tk - 0.3 + i * 0.12, 0.3), 780 + i * 90, 1080, lambda: cartridge(c, 780 + i * 90, 1080 - (i % 2) * 40, 0.6, -8 + i * 8, [(255, 214, 40), (230, 40, 70), (40, 40, 50)][i], '$$$'))
    person(c, 180, 1760, 0.55, (255, 140, 40), (36, 44, 90), mood='happy', look=(0.6, -0.5), t=t, arm_r=(150, -150), arm_l=(-30, 220), blink=blinking(t))


def s_compare(c, t):
    t12 = ph('one point two'); t11 = ph('almost eleven'); t9 = ph('nine times')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 80, 250, 920, 150); neon_text(c, 'HP, FISCAL 2025', 540, 352, 70, (30, 120, 230))
    ctext(c, 'SOURCE: HP 2025 ANNUAL REPORT (10-K)', 540, 445, 24, (255, 255, 255), 'Montserrat-ExtraBold.ttf')
    bars2(c, t, pr(t, t12 - 0.3, 0.8), pr(t, t11 - 0.3, 0.8), 'HOME PRINTERS', 'INK + TONER', '$1.2B', '$10.9B', 1.15 * 58, 10.9 * 58, (150, 150, 160), (255, 190, 30), pr(t, t9 - 0.2, 0.3), 'OVER 9x MORE')
    person(c, 960, 1840, 0.38, (255, 140, 40), (36, 44, 90), mood='shock' if t > t11 else 'neutral', look=(-0.6, -0.7), sweat=2 if t > t9 else 0, t=t, blink=blinking(t))


def s_quote(c, t):
    tc = ph('told cnbc'); tb = ph('bad investment')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, "WHY CARE WHAT YOU PRINT?", 540, 358, 56, (30, 120, 230))
    quote_card(c, 540, 820, 900, ['Every time a customer', 'buys a printer, it’s', 'an investment for us.'], pr(t, tc, 0.5), src="HP's CEO to CNBC, Jan 2024 (via The Register)")
    if t > tb - 1.4:
        quote_card(c, 540, 1240, 760, ['...it’s a bad', 'investment.'], pr(t, tb - 0.3, 0.4), (150, 22, 34), 'if you print too little or skip their ink')
    printer(c, 200, 1640, 0.45, 0.0, t)
    person(c, 900, 1840, 0.42, (255, 140, 40), (36, 44, 90), mood='shock' if t > tb else 'worried', look=(-0.6, -0.6), t=t, blink=blinking(t))


def s_razor(c, t):
    th = ph('the handle'); tbl = ph('the blades')
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, "IT'S LIKE A RAZOR", 540, 358, 66, (30, 120, 230))
    razor(c, 300, 760, 1.0, -12, pr(t, tbl - 0.2, 0.3))
    if t > th - 0.2:
        pop(c, pr(t, th - 0.2, 0.3), 330, 1280, lambda: (board(c, 140, 1220, 380, 100, (255, 255, 255)), neon_text(c, 'HANDLE: CHEAP', 330, 1290, 44, (34, 32, 30))))
        printer(c, 780, 800, 0.55 * pr(t, th, 0.3) + 0.001, 0, t)
    if t > tbl - 0.2:
        pop(c, pr(t, tbl - 0.2, 0.3), 760, 1280, lambda: (board(c, 570, 1220, 380, 100, (255, 214, 40)), neon_text(c, 'BLADES: $$$', 760, 1290, 44, (34, 32, 30))))
        for i in range(3): cartridge(c, 680 + i * 90, 1060, 0.5 * pr(t, tbl + i * 0.1, 0.3) + 0.001, -6 + i * 6, [(255, 214, 40), (230, 40, 70), (40, 40, 50)][i], '$$$')


def s_end(c, t):
    tb = ph('the bait'); ti = ph('the ink is')
    paper_bg(c, t, skyline=False, ground=False)
    c.drawLine(540, 0, 540 + 20 * math.sin(t * 2), 640, S(INK_D, 4))
    hk = skia.Path(); hk.moveTo(540, 640); hk.cubicTo(540, 740, 640, 740, 640, 670); c.drawPath(hk, S(INK_D, 8))
    printer(c, 540 + 20 * math.sin(t * 2), 850, 0.9, 0.0, t)
    if t > tb - 0.2: pop(c, pr(t, tb - 0.2, 0.3), 540, 1135, lambda: (board(c, 190, 1080, 700, 110, (255, 255, 255)), neon_text(c, 'THE PRINTER = BAIT', 540, 1158, 60, (34, 32, 30))))
    if t > ti - 0.2:
        pop(c, pr(t, ti - 0.2, 0.3), 540, 1265, lambda: (board(c, 160, 1210, 760, 110, (255, 214, 40)), neon_text(c, 'THE INK = BUSINESS', 540, 1288, 60, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('last year') - 0.15, s_compare), (ph('so why would') - 0.15, s_quote), (ph("it's like a razor") - 0.15, s_razor), (ph('so the printer') - 0.15, s_end)]
SHAKES = [(ph('almost eleven'), 18, 0.45), (ph('nine times'), 10, 0.35), (ph('bad investment'), 12, 0.4), (ph('the ink is'), 10, 0.35)]
TR = 0.32
