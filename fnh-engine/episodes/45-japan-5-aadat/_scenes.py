
import os
V = os.environ.get('V', 'ig')

def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def person(c, x, y, s, col, T, mood='happy', skin='E8B48F', belly=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    w = 130 + 90 * belly
    c.move_to(-w, 170); c.curve_to(-w, -20, w, -20, w, 170); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, -110, 90, 0, 2 * math.pi); c.set_source_rgba(*hx(skin)); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex in (-30, 30): c.arc(ex, -115, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    if mood == 'full':
        c.arc(0, -70, 22, 0, 2 * math.pi); c.set_source_rgba(*hx('B33A3A')); c.fill_preserve(); ink(c, 6); c.stroke()
    else:
        c.arc(0, -90, 30, .2, math.pi - .2); ink(c, 7); c.stroke()
    c.restore()

def num_badge(c, x, y, r, n, col='E63946', sc=1.0):
    if sc <= 0: return
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.arc(10, 12, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, r * .08); c.stroke()
    c.restore()

def num_text(fr, x, y, n, t, size=150):
    put_rgba(fr, ttext(str(n), size, LUCKY, 'FFFFFF', sw=10), x, y + 8, back(t / .3), clamp(t / .1), -6)

def meter(c, x, y, h, fill_frac, T):
    w = 150
    c.rectangle(x - w / 2 + 12, y - h / 2 + 14, w, h); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 8); c.stroke()
    fh = (h - 20) * fill_frac
    c.rectangle(x - w / 2 + 10, y + h / 2 - 10 - fh, w - 20, fh); c.set_source_rgba(*hx('3FAE5A' if fill_frac <= .82 else 'E63946')); c.fill()
    ly = y + h / 2 - 10 - (h - 20) * .8
    c.set_dash([18, 10]); c.move_to(x - w / 2 - 30, ly); c.line_to(x + w / 2 + 30, ly); ink(c, 6); c.stroke(); c.set_dash([])

def bowl(c, x, y, r, col, food):
    c.save(); c.translate(x, y)
    c.save(); c.scale(1, .3); c.arc(0, 0, r, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx(food)); c.fill_preserve(); ink(c, 5); c.stroke()
    c.move_to(-r, 0); c.curve_to(-r, r * .9, r, r * .9, r, 0); c.curve_to(r * .6, r * .25, -r * .6, r * .25, -r, 0); c.close_path()
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def brain(c, x, y, s, T, lit=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-120, 20)
        c.curve_to(-160, -80, -60, -150, 0, -110); c.curve_to(60, -150, 170, -90, 130, 10); c.curve_to(160, 90, 40, 120, 0, 90); c.curve_to(-60, 130, -170, 90, -120, 20); c.close_path()
    shadowed(c, p, 'FF9FB4' if lit < .5 else 'FFC93C')
    for a, b in (((-80, -60), (-20, 0)), ((20, -80), (70, -10)), ((-60, 50), (10, 40)), ((60, 40), (100, 0))):
        c.move_to(*a); c.curve_to(a[0] + 20, a[1] + 30, b[0] - 20, b[1] - 30, *b); ink(c, 5); c.stroke()
    c.restore()

def signal_path(c, x0, y0, x1, y1, prog, T):
    n = 14
    for i in range(n):
        u = i / (n - 1)
        if u > prog: break
        px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u + 18 * math.sin(u * 12 + T * 6)
        c.arc(px, py, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 3); c.stroke()

def clock(c, x, y, r, T, prog):
    c.arc(x + 10, y + 12, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(x, y); c.arc(x, y, r * .82, -math.pi / 2, -math.pi / 2 + 2 * math.pi * prog); c.close_path(); c.set_source_rgba(*hx('3FAE5A', .55)); c.fill()
    a = -math.pi / 2 + 2 * math.pi * prog
    c.move_to(x, y); c.line_to(x + r * .7 * math.cos(a), y + r * .7 * math.sin(a)); ink(c, 9); c.stroke()

def stairs(c, x, y, s, T, step):
    c.save(); c.translate(x, y); c.scale(s, s)
    for k in range(5):
        c.rectangle(-300 + k * 120 + 8, 100 - k * 70 + 10, 120, 70 * (k + 1)); c.set_source_rgba(*hx('1C1614')); c.fill()
    for k in range(5):
        c.rectangle(-300 + k * 120, 100 - k * 70, 120, 70 * (k + 1)); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 6); c.stroke()
    k = min(4, int(step)); f = step - int(step)
    px = -240 + (k + f) * 120; py = 100 - (k + f) * 70 - 60
    person(c, px, py - 140, .5, '2D6CDF', T)
    c.restore()

def tape_measure(c, x, y, w, T, prog):
    c.save(); c.translate(x, y)
    L = w * prog
    c.rectangle(-w / 2 + 8, -40 + 10, L, 80); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-w / 2, -40, L, 80); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 6); c.stroke()
    for k in range(int(L / 30)):
        hh = 34 if k % 5 == 0 else 18
        c.move_to(-w / 2 + k * 30, -40); c.line_to(-w / 2 + k * 30, -40 + hh); ink(c, 4); c.stroke()
    c.arc(-w / 2 - 60, 0, 90, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(-w / 2 - 60, 0, 30, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def opt(path, **kw):
    return load_rgba(path, **kw) if os.path.exists(path) else None

A45 = '/home/claude/studio/assets/45/'
BENTO = opt(A45 + 'card_bowls.png', w=840)
TRAIN = opt(A45 + 'card_train.png', w=840)
CHOP = opt(A45 + 'card_chop.png', w=420)
THALI = load_rgba('/home/claude/studio/assets/41/st_thali.png', w=760)
GIRL = load_rgba(A45 + 'st_girl.png', h=760)

SC = {l['id']: l for l in TL}

def habit_head(fr, n, t, label, col):
    overlay(fr, cairo_layer(lambda c: num_badge(c, 230, 520, 105, n, col, back(t / .3))))
    num_text(fr, 230, 520, n, t, 150)
    put_rgba(fr, ttext(label, 84, HI_B, 'FFFFFF'), 640, 520, back((t - .3) / .3) * min(1.0, 560 / ttext(label, 84, HI_B, 'FFFFFF').shape[1]), clamp((t - .3) / .1), -2)

def sc_h1(fr, T, t, l):
    fr[:] = paper('5EC8F2')
    def dr(c):
        for k in range(5):
            num_badge(c, 200 + k * 170, 690 + 40 * math.sin(T * 3 + k), 70, k + 1, ['FFC93C', '3FAE5A', '2D6CDF', '8E5CD9', 'FF8C1A'][k], back((t - .5 - .15 * k) / .3))
    overlay(fr, cairo_layer(dr))
    for k in range(5):
        if t > .5 + .15 * k: put_rgba(fr, ttext(str(k + 1), 80, LUCKY, 'FFFFFF', sw=7), 200 + k * 170, 698 + 40 * math.sin(T * 3 + k), back((t - .5 - .15 * k) / .3), 1.0, -4)
    sticker(fr, GIRL, CX, 1090, T, 9, .95 * ent(T + .6), -2)
    if V == 'yt': title(fr, 'बिना जिम पतले कैसे?', 520, T + 1.0, 112, 'FFC93C', -2.5)
    else: title(fr, '5 जापानी आदतें', 520, T + 1.0, 130, 'FFFFFF', -2.5)
    tape(fr, 'बिना जिम के पतले!', 760, 1330, t - 2.0, 'FFC93C', 48, rot=-3)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 3.1, .35, 16)
    fr[:] = paper('FFF8E7')
    def dr(c):
        for i, (lab, v, col) in enumerate((('JP', .045, 'E63946'), ('US', .42, '2D6CDF'))):
            y = 820 + i * 260
            w = 700 * v / .42 * clamp((t - .3 - 2.6 * i) / 1.0)
            c.rectangle(250 + 10 + dx, y - 70 + 12 + dy, max(20, w), 140); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.rectangle(250 + dx, y - 70 + dy, max(20, w), 140); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 7); c.stroke()
        person(c, 860, 1250, .55, '2D6CDF', T, belly=clamp((t - 3.1) / .6))
        person(c, 230, 1250, .55, 'E63946', T)
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('जापान', 50, HI_B, '1C1614', sw=0, shadow=False), 160, 820, ent(t - .2), 1.0, 0)
    put_rgba(fr, ttext('अमेरिका', 46, HI_B, '1C1614', sw=0, shadow=False), 160, 1080, ent(t - 2.8), 1.0, 0)
    burst(fr, '4-5%', 520, 700, t - 1.0, 90, 'FFC93C', LUCKY, 52)
    burst(fr, '40%+', 860, 960, t - 3.2, 100, 'E63946', LUCKY, 56)
    title(fr, 'मोटापा कितना?', 500, t, 120, 'E63946', -2)
    tape(fr, 'तो राज़ क्या है?', CX, 1340, t - 5.6, 'FFC93C', 52, rot=-2)

def sc_a1(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    habit_head(fr, 1, t, 'हारा हाची बू', 'FFC93C')
    def dr(c):
        person(c, 380, 1120, .95, 'FF6B5B', T, belly=.15 * clamp((t - 1.5) / 2.0))
        meter(c, 820, 1030, 520, .8 * clamp((t - 1.5) / 2.2), T)
        if t > 3.8: tickmark(c, 820, 700, 70 * ent(t - 3.8))
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('80%', 64, LUCKY, '1C1614', sw=0, shadow=False), 650, 1030 - 210 + 20, ent(t - 2.0), 1.0, 0)
    tape(fr, 'पेट 80% भरा = बस!', CX, 1360, t - 3.5, 'FFC93C', 50, rot=-2)

def sc_a2(fr, T, t, l):
    fr[:] = paper('2D6CDF')
    habit_head(fr, 2, t, 'छोटी कटोरियाँ', '3FAE5A')
    if t < 4.6:
        sticker(fr, THALI, CX, 1040, T, 0, .8 * ent(t - .8), -4)
        overlay(fr, cairo_layer(lambda c: xmark(c, CX, 1040, 220 * ent(t - 3.4, .25)) if t > 3.4 else None))
    else:
        if BENTO is not None: sticker(fr, BENTO, CX, 1030, T, 1, .9 * ent(t - 4.6), 3)
        else:
            def dr(c):
                for i, (bx, by, col, food) in enumerate(((330, 930, 'E63946', '3FAE5A'), (720, 930, '1C1614', 'FFF8E7'), (330, 1180, '8E5CD9', 'FF8C1A'), (720, 1180, 'FF6B5B', 'C68A5E'))):
                    sc = ent(t - 4.6 - .3 * i)
                    c.save(); c.translate(bx, by); c.scale(sc, sc); bowl(c, 0, 0, 140, col, food); c.restore()
            overlay(fr, cairo_layer(dr))
    tape(fr, 'सब्ज़ी, मछली, सूप, चावल', CX, 1360, t - 6.6, 'FFC93C', 46, rot=-2)

def sc_a3(fr, T, t, l):
    fr[:] = paper('8E5CD9')
    habit_head(fr, 3, t, 'धीरे-धीरे खाना', '2D6CDF')
    def dr(c):
        if t < 7.4: return
        person(c, 300, 1180, .8, 'FFC93C', T)
        brain(c, 800, 800, .9, T, lit=1.0 if t > 9.8 else 0.0)
        signal_path(c, 330, 1100, 760, 860, clamp((t - 8.0) / 2.0), T)
        clock(c, 820, 1170, 120 * ent(t - 7.6), T, clamp((t - 8.0) / 3.0) * .33)
    overlay(fr, cairo_layer(dr))
    if CHOP is not None and t < 7.4: sticker(fr, CHOP, CX, 1000, T, 2, 1.6 * ent(t - .8) * (1 - clamp((t - 7.1) / .3)), -4)
    tape(fr, 'धीरे खाने वालों में मोटापा कम', CX, 700, t - 3.0, 'FFC93C', 42, rot=-2)
    tape(fr, '"पेट भर गया" सिग्नल', 760, 1360, t - 8.6, 'FFFFFF', 44, rot=3)

def sc_a4(fr, T, t, l):
    fr[:] = paper('17A2B8')
    habit_head(fr, 4, t, 'पैदल चलना', '8E5CD9')
    if TRAIN is not None and t < 4.6:
        sticker(fr, TRAIN, CX, 1000, T, 3, .95 * ent(t - .8), -2)
    else:
        overlay(fr, cairo_layer(lambda c: stairs(c, CX, 1060, 1.0, T, clamp((t - 4.6) / 3.0) * 4.0)))
    tape(fr, 'ट्रेन + स्टेशन तक पैदल', CX, 1360, t - 2.0, 'FFC93C', 46, rot=-2)
    if t > 6.4: burst(fr, 'हज़ारों कदम!', 820, 760, t - 6.6, 110, 'E63946', HI_B, 40)

def sc_a5(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.8, .35, 18)
    fr[:] = paper('FF8C1A')
    habit_head(fr, 5, t, 'कमर नापो!', 'E63946')
    def dr(c):
        person(c, CX + dx, 1150 + dy, 1.15, '2D6CDF', T, belly=.25)
        tape_measure(c, CX + 60 + dx, 1290 + dy, 420, T, clamp((t - 3.6) / 1.4))
    overlay(fr, cairo_layer(dr))
    burst(fr, 'सबसे बड़ा ट्विस्ट!', 820, 760, t - 1.8, 110, 'E63946', HI_B, 38)
    tape(fr, 'सरकार हर साल नापती है', CX, 1360, t - 5.8, 'FFC93C', 46, rot=-2)

def sc_w1(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    def dr(c):
        person(c, 380, 1150, .95, 'FF6B5B', T)
        meter(c, 820, 1050, 480, .78 * clamp((t - 1.5) / 1.8), T)
        if t > 4.0: tickmark(c, 820, 740, 70 * ent(t - 4.0))
    overlay(fr, cairo_layer(dr))
    title(fr, 'आज से ट्राई करो', 500, t, 116, 'FFFFFF', -2)
    tape(fr, '"थोड़ी जगह बाकी है" = बस!', CX, 1360, t - 3.8, 'FFC93C', 46, rot=-2)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FF6B5B')
    def dr(c):
        person(c, CX, 1160, 1.1, 'FFC93C', T, mood='full', belly=.5)
        bubble(c, 720, 790, 440, 210, (-1, 1))
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('बस एक रोटी और!', 50, HI_B, 'E63946', sw=5), 720, 782, ent(t - 3.0), 1.0, -2)
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, a1=sc_a1, a2=sc_a2, a3=sc_a3, a4=sc_a4, a5=sc_a5, w1=sc_w1, e1=sc_e1)
