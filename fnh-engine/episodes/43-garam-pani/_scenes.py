
import os
V = os.environ.get('V', 'ig')

# ---------------------------------------------------------------- winter-bath props
def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def steam_puffs(c, x, y, s, T, n=4, a=1.0):
    for k in range(n):
        ph = (T * .55 + k / n) % 1
        px = x + (k - (n - 1) / 2) * 70 * s + 30 * s * math.sin(T * 2 + k)
        py = y - ph * 340 * s
        r = (30 + 50 * ph) * s
        c.arc(px, py, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a * .85 * (1 - ph)); c.fill()

def bucket(c, x, y, s, T, col='2D6CDF', hot=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def body():
        c.new_path(); c.move_to(-230, -170); c.line_to(230, -170); c.line_to(180, 230); c.curve_to(120, 260, -120, 260, -180, 230); c.close_path()
    shadowed(c, body, col)
    for k in range(3): c.move_to(-215 + k * 8, -110 + k * 90); c.line_to(215 - k * 8, -110 + k * 90); c.set_source_rgba(1, 1, 1, .25); c.set_line_width(10); c.stroke()
    c.save(); c.scale(1, .22); c.arc(0, -170 / .22, 232, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.save(); c.scale(1, .2); c.arc(0, -160 / .2, 205, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hx('FF8A5B' if hot > .5 else '9FD8FF')); c.fill()
    c.arc(0, -150, 300, math.pi * 1.1, math.pi * 1.9); ink(c, 14); c.stroke()
    c.restore()
    if hot > 0: steam_puffs(c, x, y - 190 * s, s, T, 4, hot)

def mug(c, x, y, s, T, col='FF6B5B'):
    c.save(); c.translate(x, y); c.scale(s, s)
    def body():
        c.new_path(); c.move_to(-90, -100); c.line_to(90, -100); c.line_to(80, 100); c.line_to(-80, 100); c.close_path()
    shadowed(c, body, col)
    c.move_to(-90, -60); c.curve_to(-200, -60, -200, 60, -82, 60); ink(c, 34); c.stroke()
    c.move_to(-90, -60); c.curve_to(-200, -60, -200, 60, -82, 60); c.set_source_rgba(*hx(col)); c.set_line_width(18); c.stroke()
    c.restore()

def skin_section(c, x, y, T, oil=1.0, escape=0.0, hotwash=0.0):
    w, h = 820, 420
    c.rectangle(x - w / 2 + 14, y - h / 2 + 16, w, h); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(*hx('F4C7A8')); c.fill_preserve(); ink(c, 9); c.stroke()
    for k in range(9):  # skin cells (bricks)
        for r in range(2):
            bx = x - w / 2 + 20 + k * 90 + (45 if r else 0); by = y - h / 2 + 110 + r * 70
            if bx + 80 < x + w / 2: c.rectangle(bx, by, 80, 60); c.set_source_rgba(*hx('E8A988')); c.fill_preserve(); ink(c, 4); c.stroke()
    # moisture drops inside
    rnd = np.random.default_rng(5)
    for k in range(10):
        dx = rnd.uniform(-w / 2 + 50, w / 2 - 50); dy = y + 110 + rnd.uniform(-20, 40)
        up = escape * (300 + 200 * (k % 3)) if escape > 0 and k % 2 == 0 else 0
        c.save(); c.translate(x + dx, dy - up); c.move_to(0, -24); c.curve_to(18, 0, 18, 18, 0, 18); c.curve_to(-18, 18, -18, 0, 0, -24); c.close_path()
        c.set_source_rgba(*hx('5EC8F2', 1 - .6 * min(1, escape) * (k % 2 == 0))); c.fill_preserve(); ink(c, 3); c.stroke(); c.restore()
    # oil layer on top
    if oil > 0:
        top = y - h / 2
        c.rectangle(x - w / 2, top - 34 * oil, w * oil, 34 * oil + 4); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 5); c.stroke()
        for k in range(int(9 * oil)): c.arc(x - w / 2 + 45 + k * 90, top - 17 * oil, 7, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .8); c.fill()
    if hotwash > 0:
        for k in range(7):
            ph = (T * 1.4 + k / 7) % 1
            dx = x - w / 2 + 60 + k * 115; dy = y - h / 2 - 260 + ph * 220
            c.save(); c.translate(dx, dy); c.move_to(0, -26); c.curve_to(20, 0, 20, 20, 0, 20); c.curve_to(-20, 20, -20, 0, 0, -26); c.close_path()
            c.set_source_rgba(*hx('FF6B5B', hotwash)); c.fill_preserve(); ink(c, 3); c.stroke(); c.restore()

def lips(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-160, 0); c.curve_to(-100, -80, -30, -70, 0, -40); c.curve_to(30, -70, 100, -80, 160, 0); c.curve_to(90, 90, -90, 90, -160, 0); c.close_path()
    shadowed(c, p, 'E05A6A')
    c.move_to(-160, 0); c.curve_to(-60, 20, 60, 20, 160, 0); ink(c, 6); c.stroke()
    for k in range(6): c.move_to(-110 + k * 44, -30 + (k % 2) * 60); c.line_to(-100 + k * 44, -5 + (k % 2) * 40); ink(c, 4); c.stroke()
    c.restore()

def heel(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-60, -200); c.curve_to(-140, -60, -150, 120, -40, 200); c.curve_to(60, 240, 150, 150, 120, 20); c.curve_to(100, -80, 80, -160, 60, -200); c.close_path()
    shadowed(c, p, 'E8B48F')
    for (a, b) in (((-60, 140), (-20, 60)), ((10, 190), (40, 100)), ((70, 150), (60, 80)), ((-90, 60), (-50, 20))):
        c.move_to(*a); c.line_to(*b); ink(c, 6); c.stroke()
    c.restore()

def head_hair(c, x, y, s, T, frizz=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.arc(0, 0, 150, 0, 2 * math.pi); c.set_source_rgba(*hx('E8B48F')); c.fill_preserve(); ink(c, 8); c.stroke()
    rnd = np.random.default_rng(2)
    for k in range(26):
        a = math.pi + k / 25 * math.pi
        bx, by = 150 * math.cos(a), 150 * math.sin(a) - 10
        L = 70 + 60 * frizz * rnd.uniform(.4, 1.2)
        wob = frizz * rnd.uniform(-40, 40)
        c.move_to(bx, by); c.curve_to(bx * 1.15 + wob, by * 1.15 - 20, bx * 1.3 - wob, by * 1.3, bx + (L + 20) * math.cos(a) + wob, by + (L + 20) * math.sin(a))
        ink(c, 16); c.stroke_preserve(); c.set_source_rgba(*hx('3B2A20')); c.set_line_width(9); c.stroke()
    for ex in (-50, 50): c.arc(ex, 10, 14, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 70, 40, math.pi + .3, -.3); ink(c, 7); c.stroke()
    c.restore()

def clock(c, x, y, r, T, prog):
    c.arc(x + 10, y + 12, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(x, y); c.arc(x, y, r * .82, -math.pi / 2, -math.pi / 2 + 2 * math.pi * prog / 6); c.close_path(); c.set_source_rgba(*hx('3FAE5A', .55)); c.fill()
    a = -math.pi / 2 + 2 * math.pi * prog / 6
    c.move_to(x, y); c.line_to(x + r * .7 * math.cos(a), y + r * .7 * math.sin(a)); ink(c, 9); c.stroke()

def thermo(c, x, y, s, T, level=.5, col='FFA43A'):
    c.save(); c.translate(x, y); c.scale(s, s)
    def tube():
        c.new_path(); c.arc(0, 200, 70, -math.pi * .3, math.pi * 1.3); c.line_to(-38, -260); c.arc(0, -260, 38, math.pi, 0); c.close_path()
    shadowed(c, tube, 'FFFFFF')
    c.arc(0, 200, 50, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
    top = 170 - 420 * level; c.rectangle(-18, top, 36, 200 - top); c.fill()
    c.restore()

# ---------------------------------------------------------------- scenes
SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('2D6CDF')
    sticker(fr, BUCKET, CX - 30, 1060, T, 0, .95 * ent(T + .5), -3)
    overlay(fr, cairo_layer(lambda c: steam_puffs(c, CX - 30, 780, 1.5, T, 5, 1.0)))
    if t > 1.2: sticker(fr, TAP, 860, 900, T, 1, .42 * ent(t - 1.2), 8)
    if V == 'yt':
        title(fr, 'गरम पानी से नहाना = गलती?', 520, T + 1.0, 100, 'FFC93C', -2.5)
    else:
        title(fr, 'सर्दी में खौलता पानी?', 520, T + 1.0, 110, 'FFFFFF', -2.5)
    tape(fr, 'भाप देखकर ही मज़ा!', CX, 1310, t - 3.5, 'FFC93C', 50, rot=-3)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .05, .4, 20)
    fr[:] = paper('E63946')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    sticker(fr, CARD, CX + dx, 960 + dy, T, 2, .95, -3)
    overlay(fr, cairo_layer(lambda c: steam_puffs(c, CX + 200, 820, 1.2, T, 4, .9)))
    title(fr, 'पर रुको!', 500, t, 160, 'FFC93C', -4)
    tape(fr, 'स्किन खिंची-खिंची?', 330, 1250, t - 1.0, 'FFFFFF', 46, rot=-4)
    tape(fr, 'सफ़ेद पपड़ी, खुजली?', 760, 1330, t - 3.6, 'FFC93C', 46, rot=3)
    burst(fr, '?!', 880, 720, t - 5.6, 80, '2D6CDF', LUCKY, 80)

def sc_s1(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: skin_section(c, CX, 1040, T, oil=clamp((t - 1.2) / 1.6))))
    title(fr, 'स्किन का कवच', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'कुदरती तेल की परत', CX, 760, t - 2.4, 'FFC93C', 52, rot=-2)
    tape(fr, 'नमी अंदर लॉक!', CX, 1330, t - 4.8, 'FFFFFF', 52, rot=2)

def sc_s2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.0, .35, 14)
    fr[:] = paper('FF6B5B')
    oil = 1 - clamp((t - .8) / 2.0)
    overlay(fr, cairo_layer(lambda c: skin_section(c, CX + dx, 1110 + dy, T, oil=oil, escape=clamp((t - 3.4) / 2.4), hotwash=clamp(t / .5) * (1 - clamp((t - 3.0) / .8)))))
    sticker(fr, TAP, 860, 760, T, 3, .34, -12, t)
    title(fr, 'गरम पानी = तेल साफ़!', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'परत कमज़ोर', 330, 1340, t - 3.2, 'FFC93C', 50, rot=-3)
    tape(fr, 'नमी उड़ गई!', 760, 1340, t - 4.8, 'FFFFFF', 50, rot=3)

def sc_s3(fr, T, t, l):
    fr[:] = paper('8E5CD9')
    def dr(c):
        lips(c, CX, 820, .8 * ent(t - 3.6), T)
        heel(c, 780, 1130, .75 * ent(t - 5.4), T)
        c.save(); c.translate(320, 1130); c.scale(ent(t - 3.0), ent(t - 3.0))
        c.rectangle(-150 + 10, -110 + 12, 300, 220); c.set_source_rgba(*hx('1C1614')); c.fill()
        c.rectangle(-150, -110, 300, 220); c.set_source_rgba(*hx('E8B48F')); c.fill_preserve(); ink(c, 7); c.stroke()
        rnd = np.random.default_rng(1)
        for k in range(14):
            px, py = rnd.uniform(-130, 110), rnd.uniform(-90, 80)
            c.move_to(px, py); c.line_to(px + 26, py - 8); c.line_to(px + 34, py + 8); c.close_path(); c.set_source_rgba(1, 1, 1, .9); c.fill()
        c.restore()
    overlay(fr, cairo_layer(dr))
    title(fr, 'सूखी हवा + गरम पानी', 500, t, 100, 'FFFFFF', -2)
    burst(fr, 'डबल अटैक!', CX, 660, t - 2.4, 120, 'E63946', HI_B, 46)
    tape(fr, 'रूखी स्किन', 320, 1300, t - 3.6, 'FFC93C', 44, rot=-3)
    tape(fr, 'फटी एड़ियाँ', 780, 1390, t - 6.2, 'FFFFFF', 44, rot=3)

def sc_s4(fr, T, t, l):
    fr[:] = paper('17A2B8')
    sticker(fr, CARD, CX, 980, T, 4, .9, 3, t)
    overlay(fr, cairo_layer(lambda c: steam_puffs(c, 640, 800, 1.1, T, 4, .9)))
    title(fr, 'बालों के साथ भी!', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'सिर पर तेज़ गरम पानी', 380, 1230, t - 1.4, 'FFC93C', 44, rot=-3)
    tape(fr, 'रूखे, बेजान, उलझे', 720, 1330, t - 3.4, 'FFFFFF', 48, rot=2)

def sc_w1(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    sticker(fr, BUCKET, 330, 960, T, 5, .42, -3, t)
    overlay(fr, cairo_layer(lambda c: (steam_puffs(c, 330, 840, .7, T, 3, .35), thermo(c, 600, 930, .5 * ent(t - 1.2), T, .45),
                                        clock(c, 820, 920, 110 * ent(t - 3.8), T, clamp((t - 4.0) / 1.6)))))
    if t > 6.0: sticker(fr, COCO, 560, 1200, T, 6, .42 * ent(t - 6.0), -4)
    title(fr, 'तो करना क्या है?', 500, t, 116, 'FFFFFF', -2)
    tape(fr, 'गुनगुना पानी', 330, 1170, t - 1.3, 'FFC93C', 46, rot=-4)
    tape(fr, '5-10 मिनट', 820, 1100, t - 4.4, 'FFFFFF', 46, rot=4)
    tape(fr, 'गीली स्किन पर तेल!', 800, 1340, t - 8.6, 'E63946', 42, rot=-2, tcol='FFFFFF')

def sc_e1(fr, T, t, l):
    fr[:] = paper('FF8A5B')
    sticker(fr, TAP, CX + 60, 1000, T, 7, .7, -4)
    sticker(fr, BUCKET, 330, 1150, T, 8, .4, 4)
    def dr(c):
        for k in range(10):
            ph = (T * .35 + k / 10) % 1
            c.arc(180 + (k * 83) % 720, 1320 - ph * 650, 70 + 60 * ph, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .6 * clamp((t - 1.0) / 1.5)); c.fill()
    overlay(fr, cairo_layer(dr))
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)
    burst(fr, 'बाथरूम = सौना!', CX, 1000, t - 3.6, 140, 'E63946', HI_B, 46)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, w1=sc_w1, e1=sc_e1)
