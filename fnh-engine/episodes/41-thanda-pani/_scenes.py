
# ---------------------------------------------------------------- cold-water props
def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def snowflake(c, x, y, r, rot=0.0, col='FFFFFF'):
    c.save(); c.translate(x, y); c.rotate(rot)
    for k in range(6):
        c.save(); c.rotate(k * math.pi / 3)
        c.move_to(0, 0); c.line_to(0, -r); c.move_to(0, -r * .55); c.line_to(-r * .25, -r * .78); c.move_to(0, -r * .55); c.line_to(r * .25, -r * .78)
        c.restore()
    ink(c, r * .28); c.stroke_preserve(); c.set_source_rgba(*hx(col)); c.set_line_width(r * .13); c.stroke()
    c.restore()

def bottle(c, x, y, s, T, frost=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def body():
        c.new_path(); c.move_to(-48, -300); c.line_to(48, -300); c.line_to(48, -250); c.curve_to(130, -200, 130, -150, 130, -100)
        c.line_to(130, 280); c.curve_to(130, 320, -130, 320, -130, 280); c.line_to(-130, -100); c.curve_to(-130, -150, -130, -200, -48, -250); c.close_path()
    shadowed(c, body, 'CFEFFF')
    c.save(); body(); c.clip()
    c.rectangle(-140, -40, 280, 330); c.set_source_rgba(*hx('6EC6FF', .55)); c.fill()
    for k in range(4): c.rectangle(-140, -80 + k * 95, 280, 14); c.set_source_rgba(*hx('FFFFFF', .45)); c.fill()
    c.rectangle(-95, -200, 32, 440); c.set_source_rgba(1, 1, 1, .7); c.fill()
    if frost > 0:
        rnd = np.random.default_rng(4)
        for k in range(26):
            dx, dy = rnd.uniform(-115, 115), rnd.uniform(-200, 280); r = rnd.uniform(6, 14)
            c.save(); c.translate(dx, dy + (T * 30 * (k % 3 == 0)) % 40); c.move_to(0, -r * 1.6); c.curve_to(r, 0, r, r, 0, r); c.curve_to(-r, r, -r, 0, 0, -r * 1.6)
            c.set_source_rgba(1, 1, 1, .85 * frost); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', .5 * frost)); c.set_line_width(2); c.stroke(); c.restore()
    c.restore(); body(); ink(c, 8); c.stroke()
    c.rectangle(-60 + 10, -370 + 12, 120, 80); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(-60, -370, 120, 80); c.set_source_rgba(*hx('2D6CDF')); c.fill_preserve(); ink(c, 7); c.stroke()
    for k in range(5): c.move_to(-45 + k * 22, -360); c.line_to(-45 + k * 22, -300); ink(c, 3); c.stroke()
    c.restore()

def belly(c, x, y, s, T, fat=0.0, mood='happy'):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(0, -150); c.curve_to(160, -170, 200 + 40 * fat, 60, 80, 150 + 20 * fat); c.curve_to(0, 200 + 30 * fat, -150, 160, -170 - 30 * fat, 40)
        c.curve_to(-190, -60, -110, -40, -60, -90); c.curve_to(-40, -130, -20, -150, 0, -150); c.close_path()
    shadowed(c, p, 'FF8FA3')
    if fat > 0:
        for k, (fx, fy) in enumerate(((-60, 80), (40, 110), (-10, 140))):
            c.save(); c.translate(fx, fy); c.scale(1, .7); c.arc(0, 0, 34 * fat, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('FFE08A')); c.fill_preserve(); ink(c, 4); c.stroke()
    for ex in (-30, 50):
        if mood == 'shock': c.arc(ex, -20, 16, 0, 2 * math.pi)
        else: c.arc(ex, -20, 12, 0, 2 * math.pi)
        c.set_source_rgba(*hx('1C1614')); c.fill()
    if mood == 'shock': c.save(); c.translate(10, 40); c.scale(1, 1.3); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('B33A3A')); c.fill_preserve(); ink(c, 6); c.stroke()
    else: c.arc(10, 20, 36, .2, math.pi - .2); ink(c, 8); c.stroke()
    c.restore()

def oil_pan(c, x, y, s, T, solid=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(170, -10); c.line_to(380, -60); c.set_source_rgba(*hx('1C1614')); c.set_line_width(46); c.stroke()
    c.move_to(170, -10); c.line_to(370, -58); c.set_source_rgba(*hx('5B4636')); c.set_line_width(28); c.stroke()
    def pan():
        c.new_path(); c.move_to(-240, -20); c.curve_to(-230, 150, 230, 150, 240, -20); c.close_path()
    shadowed(c, pan, '3B3F4A')
    c.save(); c.scale(1, .26); c.arc(0, -80, 228, 0, 2 * math.pi); c.restore()
    col = np.array(hx('F2B627')[:3]) * (1 - solid) + np.array(hx('FFF6DC')[:3]) * solid
    c.set_source_rgba(*col, 1); c.fill_preserve(); ink(c, 6); c.stroke()
    if solid < .5:
        for k in range(4):
            ph = (T * .9 + k / 4) % 1; c.arc(-120 + k * 80, -22, 6 + 8 * ph, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .7 * (1 - ph)); c.fill()
    else:
        for k in range(3): snowflake(c, -110 + k * 110, -22, 22 * solid, k)
    c.restore()

def thermo(c, x, y, s, T, level=.75, col='E63946'):
    c.save(); c.translate(x, y); c.scale(s, s)
    def tube():
        c.new_path(); c.arc(0, 200, 70, -math.pi * .3, math.pi * 1.3); c.line_to(-38, -260); c.arc(0, -260, 38, math.pi, 0); c.close_path()
    shadowed(c, tube, 'FFFFFF')
    c.arc(0, 200, 50, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
    top = 170 - 420 * level; c.rectangle(-18, top, 36, 200 - top); c.fill()
    for k in range(8): c.move_to(38, 140 - k * 50); c.line_to(62, 140 - k * 50); ink(c, 5); c.stroke()
    c.restore()

def temp_graph(c, x, y, w, h, prog, T):
    c.rectangle(x - w / 2 + 14, y - h / 2 + 16, w, h); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - h / 2, w, h); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 9); c.stroke()
    base = y - h / 2 + h * .3
    c.set_dash([24, 16]); c.move_to(x - w / 2 + 30, base); c.line_to(x + w / 2 - 30, base); c.set_source_rgba(*hx('3FAE5A')); c.set_line_width(7); c.stroke(); c.set_dash([])
    n = int(120 * prog)
    pts = []
    for i in range(n + 1):
        u = i / 120; px = x - w / 2 + 40 + u * (w - 80)
        dip = math.exp(-((u - .25) / .1) ** 2) if u < .25 else math.exp(-(u - .25) * 4.5)
        pts.append((px, base + h * .5 * (dip if u > .12 else math.exp(-((u - .25) / .1) ** 2))))
    if len(pts) > 1:
        c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.set_source_rgba(*hx('2D6CDF')); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        c.arc(*pts[-1], 18, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c, 5); c.stroke()

def enzyme(c, x, y, r, T, col='3FAE5A', ph=0.0):
    c.save(); c.translate(x, y + 8 * math.sin(T * 5 + ph))
    m = .25 + .2 * abs(math.sin(T * 7 + ph))
    def p():
        c.new_path(); c.move_to(0, 0); c.arc(0, 0, r, m, 2 * math.pi - m); c.close_path()
    shadowed(c, p, col, 8, 10, 6)
    c.arc(r * .2, -r * .45, r * .14, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def fat_drop(c, x, y, r):
    c.save(); c.translate(x, y); c.move_to(0, -r * 1.4); c.curve_to(r, -r * .2, r, r, 0, r); c.curve_to(-r, r, -r, -r * .2, 0, -r * 1.4); c.close_path()
    c.set_source_rgba(*hx('FFD24A')); c.fill_preserve(); ink(c, 5); c.stroke(); c.restore()

def fridge(c, x, y, s, T, door=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p(): c.new_path(); c.rectangle(-150, -260, 300, 520)
    shadowed(c, p, 'E6EEF5')
    c.move_to(-150, -90); c.line_to(150, -90); ink(c, 7); c.stroke()
    for yy in (-200, -20): c.rectangle(100, yy, 20, 70); c.set_source_rgba(*hx('8A94A3')); c.fill_preserve(); ink(c, 4); c.stroke()
    snowflake(c, -40, -180, 40, T * .5, '9FD8FF')
    c.restore()

def balance(c, x, y, s, T, tilt=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-90, 300); c.line_to(90, 300); c.line_to(0, 40); c.close_path(); c.set_source_rgba(*hx('8E5CD9')); c.fill_preserve(); ink(c, 8); c.stroke()
    c.save(); c.translate(0, 40); c.rotate(tilt)
    c.rectangle(-360, -14, 720, 28); c.set_source_rgba(*hx('5B3FA8')); c.fill_preserve(); ink(c, 7); c.stroke()
    for sx in (-1, 1):
        c.save(); c.translate(sx * 330, 0); c.rotate(-tilt)
        c.move_to(-90, 140); c.line_to(0, 0); c.line_to(90, 140); ink(c, 5); c.stroke()
        c.move_to(-130, 140); c.curve_to(-110, 200, 110, 200, 130, 140); c.close_path(); c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 7); c.stroke()
        c.restore()
    c.restore(); c.arc(0, 40, 20, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.restore()

def pan_pos(tilt, sx, s, x, y):
    return (x + s * (sx * 330 * math.cos(tilt)), y + s * (40 + sx * 330 * math.sin(tilt)))

# ---------------------------------------------------------------- scenes
SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('7FD8B0')
    sticker(fr, THALI, 360, 1010, T, 0, .78, -6)
    overlay(fr, cairo_layer(lambda c: (bottle(c, 820, 1010 - 60 * (1 - ent(t - .9, .4)), .95 * ent(t - .9, .4), T, rot=.12),
                                        snowflake(c, 940, 700, 40, T), snowflake(c, 700, 760, 26, -T))))
    title(fr, 'खाने के बाद ठंडा पानी?', 520, T + 1.0, 98, 'FFFFFF', -2.5)
    tape(fr, 'खाना खाया...', 360, 1330, T + 1.0, 'FFFFFF', 48, rot=-4)
    tape(fr, '...फ्रिज वाली बोतल!', 800, 1330, t - 2.0, '2D6CDF', 48, rot=4, tcol='FFFFFF')

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .1, .4, 22)
    fr[:] = paper('FF6B5B')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    overlay(fr, cairo_layer(lambda c: (belly(c, CX + dx, 1040 + dy, 1.45, T, fat=clamp((t - 2.6) / 1.2), mood='shock' if t > 2.6 else 'happy'),
                                        bottle(c, 250, 1080, .55, T, rot=-.2))))
    title(fr, 'रुको!', 470, t, 170, 'FFFFFF', -4)
    tape(fr, 'ठंडा पानी = पेट की चर्बी?', CX, 690, t - 1.9, 'FFC93C', 56, rot=-2)
    burst(fr, '?!', 860, 860, t - 3.0, 95, '8E5CD9', LUCKY, 90)

def sc_s1(fr, T, t, l):
    fr[:] = paper('9B7FE0')
    solid = clamp((t - 2.4) / 1.4)
    def dr(c):
        oil_pan(c, 360, 960, 1.0, T, solid)
        c.move_to(560, 1000); c.line_to(660, 1000); ink(c, 14); c.stroke()
        c.move_to(640, 975); c.line_to(680, 1000); c.line_to(640, 1025); ink(c, 14); c.stroke()
        belly(c, 830, 1010, .9 * ent(t - 4.0), T, fat=clamp((t - 4.3) / 1.0))
    overlay(fr, cairo_layer(dr))
    title(fr, 'बहुत लोग कहते हैं...', 500, t, 104, 'FFFFFF', -2)
    tape(fr, 'तेल + ठंडा पानी = जम गया!', 360, 1290, t - 2.4, 'FFFFFF', 46, rot=-3)
    tape(fr, '= पेट की चर्बी?', 830, 1290, t - 4.4, 'FFC93C', 46, rot=3)

def sc_s2(fr, T, t, l):
    fr[:] = paper('FF8C1A')
    overlay(fr, cairo_layer(lambda c: (belly(c, 380, 1020, 1.25, T), thermo(c, 820, 1000, .95 * ent(t - .6), T, .78 * clamp((t - .8) / 1.4)))))
    title(fr, 'अब सच सुनो', 500, t, 124, 'FFFFFF', -2)
    burst(fr, '37°C', 820, 700, t - 2.2, 120, 'E63946', LUCKY, 72)
    tape(fr, 'पेट अंदर से गरम है', CX, 1340, t - 2.6, 'FFF8E7', 52, rot=-2)

def sc_s3(fr, T, t, l):
    fr[:] = paper('5EC8F2')
    def dr(c):
        wglass(c, 230, 860, .6, T, .8, '9FD8FF', ice=True)
        temp_graph(c, 620, 1060, 720, 420, clamp((t - 1.0) / 4.8), T)
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('37°C', 44, LUCKY, '3FAE5A', sw=5, shadow=False), 340, 936, ent(t - .8), 1.0, 0)
    title(fr, 'ठंडा? थोड़ी देर में गरम!', 500, t, 92, 'FFFFFF', -2)
    tape(fr, 'पेट का तापमान वापस नॉर्मल', 620, 1340, t - 4.4, 'FFC93C', 48, rot=-2)

def sc_s4(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    def dr(c):
        for k in range(7):
            gone = t > 1.6 + k * .45
            if not gone: fat_drop(c, 260 + (k % 4) * 180, 900 + (k // 4) * 200 + 10 * math.sin(T * 3 + k), 34)
        enzyme(c, 330 + 520 * clamp((t - 1.2) / 3.2), 950, 90 * ent(t - .6), T, 'FFC93C')
        enzyme(c, 820 - 420 * clamp((t - 1.6) / 3.2), 1120, 80 * ent(t - .9), T, 'FF7AA8', 1.3)
    overlay(fr, cairo_layer(dr))
    title(fr, 'चर्बी को कौन पचाता है?', 500, t, 96, 'FFFFFF', -2)
    tape(fr, 'पित्त + एंज़ाइम', 330, 700, t - 1.2, 'FFC93C', 54, rot=-4)
    tape(fr, 'शरीर की गर्मी में काम', CX, 1330, t - 3.4, 'FFFFFF', 50, rot=2)

def sc_s5(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 2.2, .4, 18)
    fr[:] = paper('FF7AA8')
    def dr(c):
        oil_pan(c, 330, 940, .75, T, 1.0)
        fridge(c, 800, 1000 + dy, .85, T)
        if t > 2.2: xmark(c, 800 + dx, 1000 + dy, 170 * ent(t - 2.2, .25))
    overlay(fr, cairo_layer(dr))
    title(fr, 'पेट कोई फ्रिज नहीं!', 500, t, 112, 'FFFFFF', -2)
    tape(fr, 'बर्तन का तेल जमता है', 330, 1240, t - .3, 'FFF8E7', 46, rot=-4)

def sc_s6(fr, T, t, l):
    fr[:] = paper('1FB5A8')
    tilt = -.28 * clamp((t - .8) / 1.0)
    def dr(c):
        balance(c, CX, 1000, 1.0, T, tilt)
        px, py = pan_pos(tilt, 1, 1.0, CX, 1000); wglass(c, px, py + 40, .32, T, .7)
    overlay(fr, cairo_layer(dr))
    lx, ly = pan_pos(tilt, -1, 1.0, CX, 1000)
    sticker(fr, THALI, int(lx), int(ly + 40), T, 1, .32, 0, t)
    title(fr, 'चर्बी किससे बढ़ती है?', 500, t, 100, 'FFFFFF', -2)
    tape(fr, 'ज़्यादा कैलोरी', int(lx), 1330, t - .6, 'FFC93C', 50, rot=-4)
    tape(fr, 'पानी का तापमान नहीं', 800, 760, t - 2.9, 'FFFFFF', 46, rot=4)

def sc_s7(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    def dr(c):
        doctor(c, 330, 1010, 1.1 * ent(t - 1.4), T)
        bubble(c, 790, 820, 420, 200, (-1, 1))
        wglass(c, 900, 1150, .5, T, .8)
        if t > 4.6: tickmark(c, 900, 1150, 90 * ent(t - 4.6))
    overlay(fr, cairo_layer(dr))
    sticker(fr, THALI, 670, 1180, T, 2, .36, 0, t - .2)
    put_rgba(fr, ttext('पाचन में मदद!', 44, HI_B, '3FAE5A', sw=6), 790, 815, ent(t - 2.8), 1.0, -2)
    title(fr, 'खाने के साथ पानी?', 500, t, 112, 'FFFFFF', -2)

def sc_w1(fr, T, t, l):
    fr[:] = paper('B79CF2')
    def dr(c):
        belly(c, CX, 860, .75, T, mood='shock' if t < 3.2 else 'happy')
        wglass(c, 330, 1170, .62, T, .75, '9FD8FF')
        wglass(c, 790, 1170, .62 * ent(t - 4.0), T, .75, 'FFE3B0')
        if t > 4.0: steam(c, 790, 990, .9, T)
    overlay(fr, cairo_layer(dr))
    title(fr, 'पेट भारी लगे तो?', 490, t, 112, 'FFFFFF', -2)
    tape(fr, 'सादा', 330, 1380, t - 3.6, 'FFF8E7', 52, rot=-4)
    tape(fr, 'हल्का गुनगुना', 790, 1380, t - 4.4, 'FFC93C', 52, rot=4)
    burst(fr, 'घूँट-घूँट', 860, 690, t - 6.8, 120, '2D6CDF', HI_B, 46)

def sc_e1(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 1.1, .35, 16)
    fr[:] = paper('3EC1D3')
    overlay(fr, cairo_layer(lambda c: (bottle(c, CX + dx, 1020 + dy, 1.25 * ent(t - .9, .35), T, .3, rot=-.08),
                                        snowflake(c, 300, 820, 34, T), snowflake(c, 820, 900, 28, -T))))
    title(fr, 'डरना छोड़ो!', 500, t, 140, 'FFFFFF', -3)
    burst(fr, 'बोतल उठाओ!', 820, 1300, t - 1.1, 140, 'E63946', HI_B, 50)

def sc_e2(fr, T, t, l):
    fr[:] = paper('FF8A5B')
    def dr(c):
        granny(c, 330, 1040, 1.0, T)
        bubble(c, 740, 780, 460, 220, (-1, 1))
        phone_s(c, 810, 1190, .55, T)
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, ttext('ठंडा पानी मत पियो!', 42, HI_B, 'E63946', sw=5), 740, 775, ent(t - .6), 1.0, -2)
    title(fr, 'भेजो उस दोस्त को', 490, t, 108, 'FFFFFF', -2)
    tape(fr, 'जो लेक्चर शुरू कर देता है!', CX, 1340, t - 2.6, 'FFC93C', 48, rot=-2)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, s5=sc_s5, s6=sc_s6, s7=sc_s7, w1=sc_w1, e1=sc_e1, e2=sc_e2)
