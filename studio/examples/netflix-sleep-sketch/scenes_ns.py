# ------------------------------------------------------------------ props (generic TV, bed, moon: no streaming logos or UI)
def tv_set(c, x, y, w, t, glow_=1.0, txt=''):
    h = w * 0.6
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2 - 30, y - h / 2 - 30, w + 60, h + 60), P((160, 200, 255), 0.3 * glow_, 40))
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 18, 18), P((30, 30, 36)), 7)
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 18, y - h / 2 + 18, w - 36, h - 36), LG((0, y - h / 2), (0, y + h / 2), [(150, 200, 255), (90, 120, 220)]))
    c.drawLine(x - w * 0.15, y + h / 2, x - w * 0.25, y + h / 2 + 50, S(INK, 10)); c.drawLine(x + w * 0.15, y + h / 2, x + w * 0.25, y + h / 2 + 50, S(INK, 10))
    if txt: ctext(c, txt, x, y + 18, w * 0.09, (255, 255, 255), 'Anton.ttf')


def bed(c, x, y, s, t, sleeper=True, eyes_open=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-300, -60, 600, 120), 20, 20), P((150, 110, 80)), 7)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-310, -200, 60, 260), 20, 20), P((150, 110, 80)), 7)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-250, -110, 120, 60), 25, 25), P((255, 255, 255)), 5)
    inked(c, skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-160, -100, 440, 70), 30, 30), P((90, 140, 220)), 6)
    c.restore()
    if sleeper: head(c, x - 170 * s, y - 120 * s, 70 * s, (255, 140, 40), 'shock' if eyes_open else 'neutral', (0.8, -0.2), 0, t, not eyes_open)


def moon(c, x, y, r):
    m = skia.Path(); m.addCircle(x, y, r); cut = skia.Path(); cut.addCircle(x + r * 0.45, y - r * 0.2, r * 0.85)
    m = skia.Op(m, cut, skia.PathOp.kDifference_PathOp); inked(c, m, P((255, 214, 40)), 6)


def clock_face(c, x, y, r, hh, mm):
    c.drawCircle(x, y, r, P((255, 255, 255))); c.drawCircle(x, y, r, S(INK, 8))
    a = (mm / 60) * 2 * math.pi - math.pi / 2; c.drawLine(x, y, x + r * 0.75 * math.cos(a), y + r * 0.75 * math.sin(a), S(INK, 6))
    a = ((hh % 12) / 12 + mm / 720) * 2 * math.pi - math.pi / 2; c.drawLine(x, y, x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a), S(INK, 9))


# ------------------------------------------------------------------ scenes
def s_hook(c, t):
    ts = ph('your sleep')
    paper_bg(c, t, skyline=False, ground=True)
    headline(c, t, (('Streaming vs. sleep,', False, (34, 32, 30), 100), ('who wins?', False, (34, 32, 30), 100), ('explained.', True, (150, 22, 34), 112)), 'in 35 seconds', "per Netflix's own CEO")
    tv_set(c, 760, 970, 360, t, 1.0, 'PLAY')
    bed(c, 360, 1150, 0.8, t, True, True)
    if t > ts - 0.3: pop(c, pr(t, ts - 0.3, 0.3), 330, 880, lambda: moon(c, 330, 880, 70))


def s_quote(c, t):
    tl = ph('staying up late'); tw = ph("we're winning")
    paper_bg(c, t, skyline=False, ground=False)
    board(c, 120, 260, 840, 150); neon_text(c, 'HIS EXACT WORDS', 540, 358, 66, (34, 32, 30))
    k = pr(t, ph('his words') - 0.1, 0.5)
    if k > 0:
        c.save(); c.translate(540, 720); s_ = 0.9 + 0.1 * eo(k); c.scale(s_, s_)
        board(c, -440, -200, 880, 400)
        f = serif(140, 700); c.drawString('“', -410, -70, f, P((190, 135, 30)))
        lines = ('You get a show or a movie', 'you’re really dying to watch,', 'and you end up staying', 'up late at night.')
        for i, ln in enumerate(lines):
            f = serif(48, 400, True); tw_ = f.measureText(ln); c.drawString(ln, -tw_ / 2, -90 + i * 64, f, P((34, 32, 30)))
        f = serif(28, 400); s2 = 'Netflix CEO Reed Hastings, via Fast Company (Nov 2017)'; c.drawString(s2, -f.measureText(s2) / 2, 175, f, P((90, 86, 80)))
        c.restore()
    if t > ph('compete with sleep') - 0.3:
        pop(c, pr(t, ph('compete with sleep') - 0.3, 0.3), 540, 1080, lambda: (board(c, 100, 1020, 880, 110, (255, 255, 255)), neon_text(c, 'WE COMPETE WITH SLEEP', 540, 1098, 54, (34, 32, 30))))
    if t > tw - 0.2:
        pop(c, pr(t, tw - 0.2, 0.3), 540, 1230, lambda: (board(c, 140, 1170, 800, 110, (255, 214, 40)), neon_text(c, "AND WE'RE WINNING!", 540, 1248, 56, (150, 22, 34))))


def s_hour(c, t):
    th = ph('every hour')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'WHY IS SLEEP THE ENEMY?', 540, 358, 56, (34, 32, 30))
    hh = 22 + 6 * pr(t, th - 0.5, 3.0); clock_face(c, 540, 760, 180, int(hh) % 24, (hh % 1) * 60)
    if t > th - 0.2:
        pop(c, pr(t, th - 0.2, 0.3), 290, 1130, lambda: (board(c, 70, 1070, 440, 110, (255, 255, 255)), neon_text(c, '1 HOUR ASLEEP', 290, 1148, 46, (34, 32, 30))))
        pop(c, pr(t, th + 0.5, 0.3), 790, 1130, lambda: (board(c, 570, 1070, 440, 110, (255, 214, 40)), neon_text(c, '= 0 WATCHING', 790, 1148, 46, (150, 22, 34))))


def s_buffet(c, t):
    ty = ph('is you')
    paper_bg(c, t, skyline=False, ground=True)
    board(c, 120, 260, 840, 150); neon_text(c, 'AN ENDLESS BUFFET', 540, 358, 62, (34, 32, 30))
    inked(c, skia.Rect.MakeXYWH(120, 900, 840, 60), P((255, 255, 255)), 6)
    for i in range(5):
        c.drawOval(skia.Rect.MakeXYWH(150 + i * 165, 850, 140, 60), P([(230, 120, 60), (120, 200, 90), (255, 214, 40), (200, 80, 80), (150, 110, 80)][i])); c.drawOval(skia.Rect.MakeXYWH(150 + i * 165, 850, 140, 60), S(INK, 4))
    sign_on = (t % 1.0) > 0.15
    board(c, 360, 560, 360, 110, (255, 214, 40) if sign_on else (255, 255, 255)); neon_text(c, 'OPEN 24/7', 540, 640, 60, (150, 22, 34))
    person(c, 540, 1760, 0.6, (255, 140, 40), (36, 44, 90), mood='happy' if t < ty else 'shock', look=(0, -0.6), t=t, blink=blinking(t))


def s_end(c, t):
    tt = ph("that's not a timer"); tc = ph("that's the competition")
    paper_bg(c, t, skyline=False, ground=True)
    tv_set(c, 540, 820, 700, t, 1.0, '')
    n = max(1, 5 - int(pr(t, ph('five seconds') - 0.2, 2.5) * 4))
    ctext(c, 'NEXT EPISODE IN', 540, 760, 50, (255, 255, 255), 'Anton.ttf')
    f = serif(150, 700); s_ = str(n); c.drawString(s_, 540 - f.measureText(s_) / 2, 920, f, P((255, 255, 255)))
    if t > tt - 0.3: pop(c, pr(t, tt - 0.3, 0.3), 540, 1160, lambda: (board(c, 220, 1100, 640, 100, (255, 255, 255)), neon_text(c, 'NOT A TIMER...', 540, 1172, 56, (34, 32, 30))))
    if t > tc - 0.3: pop(c, pr(t, tc - 0.3, 0.3), 540, 1280, lambda: (board(c, 140, 1220, 800, 100, (255, 214, 40)), neon_text(c, "IT'S THE COMPETITION", 540, 1292, 52, (150, 22, 34))))


SCENES = [(0.0, s_hook), (ph('his words') - 0.15, s_quote), (ph('but why would') - 0.15, s_hour), (ph("it's like an all") - 0.15, s_buffet), (ph('so when the next') - 0.15, s_end)]
SHAKES = [(ph('your sleep'), 10, 0.35), (ph("we're winning"), 14, 0.4), (ph('every hour'), 8, 0.3), (ph("that's the competition"), 10, 0.35)]
TR = 0.32
