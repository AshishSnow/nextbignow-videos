
import os
V = os.environ.get('V', 'ig')

def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def mosquito(c, x, y, s, T, rot=0.0, buzz=True):
    c.save(); c.translate(x + (6 * math.sin(T * 23) if buzz else 0), y + (5 * math.cos(T * 19) if buzz else 0)); c.rotate(rot); c.scale(s, s)
    for sx in (-1, 1):  # wings
        c.save(); c.scale(sx, 1); c.rotate(-.5 + .25 * math.sin(T * 60)); c.save(); c.scale(1, .38); c.arc(70, 0, 70, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(1, 1, 1, .7); c.fill_preserve(); ink(c, 4); c.stroke(); c.restore()
    for k in range(3):  # legs
        for sx in (-1, 1):
            c.move_to(sx * 10, 10 + k * 14); c.curve_to(sx * 60, 30 + k * 20, sx * 90, 70 + k * 30, sx * 110, 140 + k * 20); ink(c, 4); c.stroke()
    c.save(); c.scale(.6, 1); c.arc(0, 60, 40, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('3B3F4A')); c.fill_preserve(); ink(c, 5); c.stroke()
    for k in range(3): c.move_to(-22, 40 + k * 18); c.line_to(22, 40 + k * 18); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(5); c.stroke()
    c.arc(0, 0, 26, 0, 2 * math.pi); c.set_source_rgba(*hx('3B3F4A')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.arc(0, -30, 18, 0, 2 * math.pi); c.set_source_rgba(*hx('3B3F4A')); c.fill_preserve(); ink(c, 5); c.stroke()
    for ex in (-8, 8): c.arc(ex, -34, 6, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill()
    c.move_to(0, -46); c.line_to(0, -110); ink(c, 5); c.stroke()
    c.restore()

def person(c, x, y, s, col, T, mood='happy', skin='C68A5E', bites=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-130, 170); c.curve_to(-130, -20, 130, -20, 130, 170); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, -110, 90, 0, 2 * math.pi); c.set_source_rgba(*hx(skin)); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex in (-30, 30): c.arc(ex, -115, 10, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    if mood == 'angry':
        for ex in (-30, 30): c.move_to(ex - 22, -150 + (8 if ex < 0 else -8) * 0); c.line_to(ex + 22, -140 if ex < 0 else -150); ink(c, 7); c.stroke()
        c.arc(0, -55, 28, math.pi + .3, -.3); ink(c, 7); c.stroke()
    else:
        c.arc(0, -90, 30, .2, math.pi - .2); ink(c, 7); c.stroke()
    rnd = np.random.default_rng(4)
    for k in range(bites):
        bx, by = rnd.uniform(-70, 70), rnd.uniform(-170, -40)
        c.arc(bx, by, 11, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c, 3); c.stroke()
    c.restore()

def smell_waves(c, x, y, T, col='9B7FE0', n=3, a=1.0, up=True):
    for k in range(n):
        ph = (T * .8 + k / n) % 1
        yy = y - ph * 260
        c.move_to(x - 60, yy)
        for i in range(1, 7): c.line_to(x - 60 + i * 20, yy + 14 * math.sin(i * 1.6 + T * 4))
        c.set_source_rgba(*hx(col, a * (1 - ph))); c.set_line_width(10); c.stroke()

def stocking(c, x, y, s, col='E8C6A0', rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-60, -220); c.line_to(60, -220); c.line_to(60, 100); c.curve_to(60, 170, 0, 200, -80, 200); c.curve_to(-160, 200, -170, 120, -100, 110); c.line_to(-60, 100); c.close_path()
    shadowed(c, p, col)
    for k in range(9): c.move_to(-60, -200 + k * 34); c.line_to(60, -200 + k * 34); c.set_source_rgba(*hx('1C1614', .18)); c.set_line_width(3); c.stroke()
    c.rectangle(-62, -232, 124, 30); c.set_source_rgba(*hx('C9A27E')); c.fill_preserve(); ink(c, 5); c.stroke()
    c.restore()

def tshirt(c, x, y, s, col):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-60, -150); c.curve_to(-30, -120, 30, -120, 60, -150); c.line_to(160, -100); c.line_to(120, -20); c.line_to(90, -40)
        c.line_to(90, 150); c.line_to(-90, 150); c.line_to(-90, -40); c.line_to(-120, -20); c.line_to(-160, -100); c.close_path()
    shadowed(c, p, col, 10, 12, 7)
    c.restore()

def bar_cmp(c, x, y, T, prog):
    w = 760
    c.rectangle(x - w / 2 + 12, y - 150 + 14, w, 300); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - 150, w, 300); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 8); c.stroke()
    for i, (lab_w, col) in enumerate(((.01, '9FD8FF'), (1.0, 'E63946'))):
        by = y - 80 + i * 110
        c.rectangle(x - w / 2 + 40, by, (w - 80) * max(.012, lab_w * prog), 70); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()

def co2_bubbles(c, x, y, T, a=1.0):
    for k in range(5):
        ph = (T * .6 + k / 5) % 1
        bx = x + 40 * math.sin(T * 2 + k * 1.3) + (k - 2) * 30; by = y - ph * 300
        c.arc(bx, by, 26 + 12 * ph, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .8 * a * (1 - ph)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', .6 * a * (1 - ph))); c.set_line_width(3); c.stroke()

def crown(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-90, 40); c.line_to(-100, -50); c.line_to(-45, -5); c.line_to(0, -70); c.line_to(45, -5); c.line_to(100, -50); c.line_to(90, 40); c.close_path()
    shadowed(c, p, 'FFC93C', 8, 10, 6)
    c.restore()

def heat(c, x, y, T, a=1.0):
    for k in range(3):
        c.move_to(x - 50 + k * 50, y)
        for i in range(1, 9): c.line_to(x - 50 + k * 50 + 12 * math.sin(i + T * 6 + k), y - i * 22)
        c.set_source_rgba(*hx('FF8C1A', a)); c.set_line_width(9); c.stroke()

SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('17A2B8')
    def dr(c):
        if t < 2.0: return
        cols = ['8E5CD9', '3FAE5A', 'FFC93C', '2D6CDF']
        xs = [200, 400, 680, 880]
        for i, x in enumerate(xs): person(c, x, 1180, .55, cols[i], T)
        person(c, CX, 1060, .95, 'E63946', T, 'angry', bites=min(6, int(t * 2)))
        mosquito(c, CX + 160 * math.cos(T * 2.2), 820 + 60 * math.sin(T * 3.1), .55, T)
    overlay(fr, cairo_layer(dr))
    if t < 2.2: sticker(fr, BITE, CX, 1000, T, 0, .9 * (1 - clamp((t - 1.9) / .3)), -3)
    if V == 'yt': title(fr, 'मच्छर सिर्फ़ आपको क्यों?', 520, T + 1.0, 104, 'FFC93C', -2.5)
    else: title(fr, 'सिर्फ़ आपको ही काटता है?', 520, T + 1.0, 104, 'FFFFFF', -2.5)

def sc_h2(fr, T, t, l):
    fr[:] = paper('E63946')
    def dr(c):
        person(c, 330, 1080, .9, '2D6CDF', T, 'happy', bites=4)
        bubble(c, 740, 820, 440, 220, (-1, 1))
        if t > 3.6:
            sc = ent(t - 3.6)
            c.save(); c.translate(760, 1180); c.scale(sc, sc)
            c.move_to(0, -110); c.curve_to(90, 0, 90, 90, 0, 90); c.curve_to(-90, 90, -90, 0, 0, -110); c.close_path(); c.set_source_rgba(*hx('B3122E')); c.fill_preserve(); ink(c, 8); c.stroke()
            c.restore()
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('मेरा खून मीठा है!', 52, HI_B, 'E63946', sw=5), 740, 812, ent(t - .2), 1.0, -2)
    title(fr, 'बहुत लोग कहते हैं...', 500, t - 2.4, 104, 'FFFFFF', -2)
    tape(fr, 'मीठा खून?', 640, 1330, t - 4.4, 'FFC93C', 50, rot=-4)
    tape(fr, 'ब्लड ग्रुप?', 860, 1060, t - 5.4, 'FFFFFF', 46, rot=5)

def sc_s1(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.4, .35, 16)
    fr[:] = paper('9B7FE0')
    def dr(c):
        person(c, CX + dx, 1150 + dy, 1.1, '3FAE5A', T)
        smell_waves(c, CX - 160, 1000, T, 'FFC93C', 3, ent(t - .8)); smell_waves(c, CX + 160, 1000, T + .3, 'FFC93C', 3, ent(t - .8))
        mosquito(c, 300 + 40 * math.sin(T * 3), 760, .5, T, .3); mosquito(c, 800, 790 + 30 * math.sin(T * 2), .45, T, -.3)
    overlay(fr, cairo_layer(dr))
    title(fr, 'असली वजह?', 500, t, 130, 'FFFFFF', -2)
    burst(fr, 'स्किन की खुशबू!', CX, 720, t - 1.4, 140, 'E63946', HI_B, 44)

def sc_s2(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    def dr(c):
        if t < 5.2:
            for k in range(3): mosquito(c, 300 + k * 260 + 50 * math.sin(T * 3 + k), 720 + 30 * math.cos(T * 2 + k), .4, T)
        else:
            bar_cmp(c, CX, 1000, T, clamp((t - 5.4) / 1.6))
            for k in range(6): mosquito(c, 760 + 60 * math.sin(T * 2 + k), 900 + 70 * math.cos(T * 3 + k) + (k % 2) * 60, .3, T)
    overlay(fr, cairo_layer(dr))
    if t < 5.2: sticker(fr, STOCK, CX, 1040, T, 1, .85 * ent(t - .3), 4)
    title(fr, 'मोज़ा टेस्ट!', 500, t, 130, 'FFFFFF', -2)
    tape(fr, 'हाथ पर नायलॉन का मोज़ा', CX, 700, t - .3, 'FFC93C', 48, rot=-2)
    if t > 5.2:
        tape(fr, 'सबसे कम', 290, 960, t - 5.4, 'FFFFFF', 38, rot=-3)
        burst(fr, '100x', 820, 1220, t - 6.6, 110, 'FFC93C', LUCKY, 66)

def sc_s3(fr, T, t, l):
    fr[:] = paper('2D6CDF')
    def dr(c):
        person(c, CX, 1130, 1.05, 'E63946', T, 'angry', bites=5)
        crown(c, CX, 860, .9 * ent(t - 2.4))
        for k in range(4): mosquito(c, CX + 260 * math.cos(T * 1.6 + k * 1.6), 1000 + 140 * math.sin(T * 1.6 + k * 1.6), .38, T)
    overlay(fr, cairo_layer(dr))
    sticker(fr, MAGNET, 860, 760, T, 2, .6 * ent(t - 3.0), 18)
    title(fr, 'सालों बाद भी...', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'नंबर 1 मच्छर-मैग्नेट!', CX, 1330, t - 2.6, 'FFC93C', 52, rot=-2)

def sc_s4(fr, T, t, l):
    fr[:] = paper('FF8C1A')
    def dr(c):
        person(c, CX, 1150, 1.0, '17A2B8', T)
        smell_waves(c, CX - 200, 1040, T, '9B7FE0', 3, ent(t - .6))
        co2_bubbles(c, CX, 900, T, clamp((t - 6.3) / .5))
        heat(c, CX + 220, 1120, T, clamp((t - 7.6) / .5))
        mosquito(c, 220, 700, .5, T, .4); mosquito(c, 880, 720, .45, T, -.4)
    overlay(fr, cairo_layer(dr))
    title(fr, 'मच्छर का रडार', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'स्किन तेल के एसिड', 300, 960, t - .8, 'FFFFFF', 42, rot=-4)
    tape(fr, 'साँस की CO2', 780, 820, t - 6.3, 'FFC93C', 44, rot=3)
    tape(fr, 'शरीर की गर्मी', 800, 1330, t - 7.6, 'E63946', 44, rot=-2, tcol='FFFFFF')

def sc_s5(fr, T, t, l):
    fr[:] = paper('FFF8E7')
    def dr(c):
        for i, col in enumerate(('E63946', 'FF8C1A', '1C1614')):
            tshirt(c, 230 + i * 300, 860, .9 * ent(t - .8 - .4 * i), col)
        for i, col in enumerate(('3FAE5A', '2D6CDF', 'FFFFFF')):
            tshirt(c, 230 + i * 300, 1220, .7 * ent(t - 6.6 - .3 * i), col)
        for k in range(5): mosquito(c, 230 + (k % 3) * 300 + 70 * math.sin(T * 3 + k), 720 + 40 * math.cos(T * 4 + k), .32, T)
        if t > 8.4:
            c.move_to(140, 1110); c.line_to(940, 1330); c.set_source_rgba(*hx('E63946')); c.set_line_width(16); c.stroke()
    overlay(fr, cairo_layer(dr))
    title(fr, 'मच्छर के फ़ेवरेट रंग!', 500, t, 104, 'E63946', -2)
    tape(fr, 'कम पसंद', CX, 1050, t - 8.4, 'FFC93C', 46, rot=2)

def sc_w1(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    def dr(c):
        tshirt(c, 270, 960, .75 * ent(t - 1.2), 'CFEFFF')
        c.save(); c.translate(560, 980); c.scale(ent(t - 4.2), ent(t - 4.2))
        c.arc(0, 0, 90, 0, 2 * math.pi); c.set_source_rgba(*hx('5EC8F2')); c.fill_preserve(); ink(c, 7); c.stroke()
        for k in range(5): c.move_to(-40 + k * 20, -120); c.line_to(-50 + k * 20, -170); ink(c, 6); c.stroke()
        c.restore()
        c.save(); c.translate(840, 990); c.scale(ent(t - 5.8), ent(t - 5.8))
        c.move_to(-120, 120); c.line_to(-100, -120); c.curve_to(-40, -170, 40, -170, 100, -120); c.line_to(120, 120); c.close_path()
        c.set_source_rgba(1, 1, 1, .55); c.fill_preserve(); ink(c, 6); c.stroke()
        for k in range(7): c.move_to(-110 + k * 36, -140); c.line_to(-110 + k * 36, 120); c.set_source_rgba(*hx('1C1614', .3)); c.set_line_width(2); c.stroke()
        c.restore()
        if t > 5.8:
            mosquito(c, 840 + 160 * math.cos(T * 2), 820, .32, T)
            xmark(c, 840 + 160 * math.cos(T * 2), 820, 50)
    overlay(fr, cairo_layer(dr))
    title(fr, 'तो करना क्या है?', 500, t, 116, 'FFFFFF', -2)
    tape(fr, 'हल्के रंग, पूरी बाँह', 270, 1200, t - 1.4, 'FFC93C', 40, rot=-4)
    tape(fr, 'पसीना? नहा लो', 560, 1330, t - 4.4, 'FFFFFF', 42, rot=2)
    tape(fr, 'मच्छरदानी', 840, 1200, t - 5.9, 'E63946', 40, rot=4, tcol='FFFFFF')

def sc_e1(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 6.6, .35, 16)
    fr[:] = paper('FF6B5B')
    def dr(c):
        person(c, CX + dx, 1150 + dy, 1.05, 'FFC93C', T, 'angry', bites=6)
        for k in range(6): mosquito(c, CX + 300 * math.cos(T * 1.8 + k), 1000 + 200 * math.sin(T * 1.8 + k), .34, T)
    overlay(fr, cairo_layer(dr))
    if t > 6.4: sticker(fr, MAGNET, CX, 800, T, 3, .55 * ent(t - 6.4), 180)
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'मीठा नहीं...', 330, 1320, t - 5.6, 'FFF8E7', 46, rot=-3)
    burst(fr, 'मच्छर-मैग्नेट!', 760, 1330, t - 6.6, 120, '2D6CDF', HI_B, 40)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, s5=sc_s5, w1=sc_w1, e1=sc_e1)
