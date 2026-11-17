
import os
V = os.environ.get('V', 'ig')

def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def opt(path, **kw):
    return load_rgba(path, **kw) if os.path.exists(path) else None

A = '/home/claude/studio/assets/47/'
WOMAN = opt(A + 'st_woman.png', h=820)
SUGAR = opt(A + 'st_sugar.png', w=560)
COLA = opt(A + 'st_cola.png', h=440)
CHILI = opt(A + 'st_chili.png', w=440)
WATER = opt(A + 'st_water.png', h=440)

def stk(fr, im, x, y, T, k, sc, rot=0, t=None):
    if im is None or sc <= 0.01: return
    if t is None: sticker(fr, im, x, y, T, k, sc, rot)
    else: sticker(fr, im, x, y, T, k, sc, rot, t)

# flowing background: slow rotating rays + drifting rings, so no frame is ever a flat colour
def flow_bg(fr, T, col='FFFFFF', a=.13, cx=CX, cy=980):
    def dr(c):
        c.save(); c.translate(cx, cy); c.rotate(T * .12)
        for k in range(18):
            ang = k * math.pi / 9; c.move_to(0, 0); c.arc(0, 0, 1500, ang, ang + math.pi / 18); c.close_path()
            c.set_source_rgba(*hx(col, a)); c.fill()
        c.restore()
        for k in range(6):
            ph = (T * .18 + k / 6) % 1
            c.arc(cx, cy, 120 + ph * 900, 0, 2 * math.pi); c.set_source_rgba(*hx(col, .12 * (1 - ph))); c.set_line_width(10); c.stroke()
    overlay(fr, cairo_layer(dr))

def hic_burst(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.1)
    n = 12
    c.new_path()
    for k in range(n * 2):
        a = k * math.pi / n; r = 130 if k % 2 == 0 else 90
        c.line_to(r * math.cos(a), r * math.sin(a))
    c.close_path(); c.save(); c.translate(8, 10); c.set_source_rgba(*hx('1C1614')); c.fill_preserve(); c.restore()
    c.set_source_rgba(*hx('FFC93C')); c.fill_preserve(); ink(c, 7); c.stroke(); c.restore()

def torso(c, x, y, s, T, squeeze=0.0, air=0.0, shut=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def body():
        c.new_path(); c.move_to(-230, 420); c.curve_to(-260, 120, -240, -160, -120, -260); c.line_to(-70, -330); c.line_to(-60, -470)
        c.line_to(60, -470); c.line_to(70, -330); c.line_to(120, -260); c.curve_to(240, -160, 260, 120, 230, 420); c.close_path()
    shadowed(c, body, 'F4C7A8')
    c.arc(0, -560, 110, 0, 2 * math.pi); c.set_source_rgba(*hx('F4C7A8')); c.fill_preserve(); ink(c, 8); c.stroke()
    for ex in (-38, 38): c.arc(ex, -575, 12, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, -520, 20 + 14 * shut, 0, 2 * math.pi); c.set_source_rgba(*hx('B33A3A')); c.fill_preserve(); ink(c, 5); c.stroke()
    # windpipe
    c.rectangle(-26, -470, 52, 250); c.set_source_rgba(*hx('F2A3A3')); c.fill_preserve(); ink(c, 5); c.stroke()
    # throat door (vocal cords)
    op = 1 - shut
    for sx in (-1, 1):
        c.save(); c.translate(sx * 26, -400); c.rotate(-sx * (math.pi / 2) * (1 - op) * .95)
        c.rectangle(-4 if sx < 0 else -22, -6, 26, 12); c.restore()
    c.save(); c.translate(0, -400)
    c.move_to(-26, 0); c.line_to(-26 + 26 * shut, 0); c.move_to(26, 0); c.line_to(26 - 26 * shut, 0); ink(c, 9); c.stroke(); c.restore()
    # lungs
    for sx in (-1, 1):
        c.save(); c.scale(sx, 1)
        def lung():
            c.new_path(); c.move_to(30, -220); c.curve_to(150, -230, 200, -60, 190, 80 - 20 * squeeze); c.curve_to(150, 110, 70, 100, 40, 60); c.close_path()
        lung(); c.set_source_rgba(*hx('FF8FA3')); c.fill_preserve(); ink(c, 6); c.stroke(); c.restore()
    # diaphragm dome
    d = 80 * (1 - squeeze)
    c.move_to(-215, 140); c.curve_to(-120, 140 - d - 40, 120, 140 - d - 40, 215, 140)
    c.set_source_rgba(*hx('E63946')); c.set_line_width(26); c.stroke()
    # air arrows
    if air > 0:
        for k in range(3):
            ph = (T * 2.2 + k / 3) % 1
            yy = -470 + ph * 330
            c.move_to(-14, yy); c.line_to(0, yy + 24); c.line_to(14, yy); c.set_source_rgba(*hx('2D6CDF', air)); c.set_line_width(8); c.stroke()
    c.restore()

def badge(c, x, y, r, sc, col='FFC93C'):
    if sc <= 0: return
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.new_path()
    for k in range(32):
        a = k * math.pi / 16; rr = r if k % 2 == 0 else r * .9
        c.line_to(rr * math.cos(a), rr * math.sin(a))
    c.close_path(); c.save(); c.translate(10, 12); c.set_source_rgba(*hx('1C1614')); c.fill_preserve(); c.restore()
    c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 8); c.stroke()
    c.arc(0, 0, r * .72, 0, 2 * math.pi); c.set_source_rgba(*hx('E63946')); c.fill_preserve(); ink(c, 6); c.stroke()
    c.restore()

def people_grid(c, x, y, T, prog):
    for i in range(20):
        r, k = divmod(i, 5)
        px, py = x - 300 + k * 150, y - 210 + r * 140
        on = prog * 20 > i
        good = i != 13
        col = ('3FAE5A' if good else 'E63946') if on else 'BFB6A0'
        c.arc(px, py - 32, 24, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 4); c.stroke()
        c.move_to(px - 34, py + 40); c.curve_to(px - 34, py - 6, px + 34, py - 6, px + 34, py + 40); c.close_path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 4); c.stroke()

def granny_bubble(c, x, y, w, h):
    bubble(c, x, y, w, h, (-1, 1))

SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('5EC8F2'); flow_bg(fr, T)
    k = 1 + .03 * math.sin(T * 9) * (1 if (T % 1.2) < .25 else 0)
    stk(fr, WOMAN, CX, 1060, T, 0, .95 * ent(T + .6) * k, -2)
    overlay(fr, cairo_layer(lambda c: (hic_burst(c, 820, 840, .9 * ent(t - .35, .25), T), granny_bubble(c, 300, 760, 380, 190) if t > 1.4 else None)))
    put_rgba(fr, ttext('हिच!', 66, HI_B, 'E63946', sw=6), 820, 846, ent(t - .35, .25), 1.0, -8)
    if t > 1.4: put_rgba(fr, ttext('कोई याद कर रहा है!', 34, HI_B, '1C1614', sw=0, shadow=False), 300, 752, ent(t - 1.5), 1.0, -2)
    if V == 'yt': title(fr, 'हिचकी क्यों आती है?', 520, T + 1.0, 112, 'FFFFFF', -2.5)
    else: title(fr, 'हिचकी = कोई याद कर रहा?', 520, T + 1.0, 100, 'FFFFFF', -2.5)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 3.1, .4, 18)
    fr[:] = paper('E63946'); flow_bg(fr, T, 'FFFFFF', .1)
    stk(fr, WOMAN, CX + dx, 1080 + dy, T, 1, .8, 3)
    overlay(fr, cairo_layer(lambda c: xmark(c, CX + dx, 1000 + dy, 260 * ent(t - 3.1, .25)) if t > 3.1 else None))
    title(fr, 'बहुत लोग यही मानते हैं', 500, t, 100, 'FFFFFF', -2)
    tape(fr, 'याद से कोई लेना-देना नहीं!', CX, 1340, t - 3.3, 'FFC93C', 48, rot=-2)

def sc_s1(fr, T, t, l):
    fr[:] = paper('17A2B8'); flow_bg(fr, T)
    sq = .5 + .5 * math.sin(T * 2.4)
    overlay(fr, cairo_layer(lambda c: torso(c, CX, 1200, .8 * ent(t, .4), T, squeeze=sq * .6)))
    title(fr, 'असली वजह अंदर है', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'डायफ्राम = साँस वाली मसल', CX, 700, t - 3.6, 'FFC93C', 46, rot=-2)
    overlay(fr, cairo_layer(lambda c: (c.move_to(820, 1300), c.line_to(700, 1250), ink(c, 8), c.stroke()) if t > 3.8 else None))

def sc_s2(fr, T, t, l):
    jolt = t > .6 and ((t - .6) % 2.4) < .35
    dx, dy = (0, -18) if jolt else (0, 0)
    fr[:] = paper('8E5CD9'); flow_bg(fr, T)
    shut = clamp((t - 4.6) / .2)
    overlay(fr, cairo_layer(lambda c: (torso(c, CX + dx, 1210 + dy, .8, T, squeeze=1.0 if jolt or t > 1.0 else 0.0, air=clamp((t - 2.6) / .4) * (1 - shut), shut=shut),
                                        hic_burst(c, 820, 760, 1.0 * ent(t - 6.6, .25), T))))
    if t > 6.6: put_rgba(fr, ttext('हिच!', 80, HI_B, 'E63946', sw=6), 820, 768, ent(t - 6.6, .25), 1.0, -8)
    title(fr, 'झटका → हवा → बंद!', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'गले का दरवाज़ा फ़टाक से बंद', 380, 1360, t - 4.6, 'FFC93C', 42, rot=-3)

def sc_s3(fr, T, t, l):
    fr[:] = paper('FF8C1A'); flow_bg(fr, T)
    title(fr, 'झटका आता क्यों है?', 500, t, 112, 'FFFFFF', -2)
    def dr(c):
        if t > 2.0:
            sc = ent(t - 2.0)
            c.save(); c.translate(290, 860); c.scale(sc, sc)
            c.arc(10, 12, 110, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.arc(0, 0, 110, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 7); c.stroke()
            a = T * 8; c.move_to(0, 0); c.line_to(80 * math.cos(a), 80 * math.sin(a)); ink(c, 8); c.stroke()
            c.restore()
        if t > 6.3:
            sc = ent(t - 6.3); c.save(); c.translate(540, 1200); c.scale(sc, sc)
            for k in range(3): c.arc(-120 + k * 120, 0, 70, 0, 2 * math.pi); c.set_source_rgba(*hx(('5EC8F2', 'FFFFFF', 'FF6B5B')[k])); c.fill_preserve(); ink(c, 6); c.stroke()
            c.restore()
    overlay(fr, cairo_layer(dr))
    stk(fr, COLA, 790, 860, T, 2, .7 * ent(t - 3.4), 6)
    stk(fr, CHILI, 300, 1190, T, 3, .75 * ent(t - 4.6), -10)
    tape(fr, 'जल्दी-जल्दी खाना', 290, 1010, t - 2.0, 'FFFFFF', 38, rot=-4)
    tape(fr, 'कोल्ड ड्रिंक गैस', 790, 1080, t - 3.4, 'FFC93C', 40, rot=4)
    tape(fr, 'तीखा', 300, 1360, t - 4.6, 'E63946', 44, rot=-3, tcol='FFFFFF')
    tape(fr, 'ठंडा-गरम', 760, 1360, t - 6.3, '5EC8F2', 44, rot=3)

def sc_s4(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 4.0, .4, 18)
    fr[:] = paper('1C1614'); flow_bg(fr, T, 'FFC93C', .1)
    overlay(fr, cairo_layer(lambda c: badge(c, CX + dx, 1000 + dy, 300, back((t - 3.8) / .4))))
    if t > 3.8:
        put_rgba(fr, ttext('68', 210, LUCKY, 'FFFFFF', sw=10), CX + dx, 960 + dy, back((t - 3.8) / .4), 1.0, -4)
        put_rgba(fr, ttext('साल', 70, HI_B, 'FFFFFF', sw=6), CX + dx, 1110 + dy, back((t - 4.0) / .4), 1.0, -4)
    title(fr, 'हैरान करने वाली कहानी', 500, t, 100, 'FFC93C', -2)
    tape(fr, 'अमेरिका का एक आदमी', CX, 690, t - 2.4, 'FFFFFF', 46, rot=-2)
    burst(fr, '43 करोड़ हिचकियाँ!', CX, 1380 - 40, t - 8.4, 130, 'E63946', HI_B, 40)

def sc_s5(fr, T, t, l):
    fr[:] = paper('3FAE5A'); flow_bg(fr, T)
    if t < 6.2:
        stk(fr, SUGAR, CX, 960, T, 4, .85 * ent(t - .3), -4)
        def sp(c):
            sc = ent(t - 1.2); c.save(); c.translate(CX + 40, 1180); c.rotate(-.25); c.scale(sc, sc)
            c.save(); c.translate(8, 10); c.scale(1, .55); c.arc(-160, 0, 110, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('1C1614')); c.fill()
            c.save(); c.scale(1, .55); c.arc(-160, 0, 110, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('DDE3EA')); c.fill_preserve(); ink(c, 7); c.stroke()
            c.save(); c.scale(1, .4); c.arc(-160, -10, 80, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, 1); c.fill()
            c.rectangle(-55, -16, 300, 32); c.set_source_rgba(*hx('DDE3EA')); c.fill_preserve(); ink(c, 6); c.stroke()
            c.restore()
        overlay(fr, cairo_layer(sp))
        tape(fr, 'एक चम्मच सूखी चीनी', CX, 1340, t - 3.0, 'FFC93C', 46, rot=-2)
        tape(fr, 'बिना पानी', 300, 760, t - 4.6, 'FFFFFF', 42, rot=-5)
    else:
        overlay(fr, cairo_layer(lambda c: people_grid(c, CX, 1040, T, clamp((t - 6.3) / 2.0))))
        burst(fr, '19 / 20', 820, 760, t - 8.4, 110, 'FFC93C', LUCKY, 56)
        tape(fr, 'हिचकी रुक गई!', CX, 1360, t - 8.6, 'FFFFFF', 50, rot=-2)
    title(fr, 'रिसर्च वाला नुस्खा', 500, t, 112, 'FFFFFF', -2)

def sc_w1(fr, T, t, l):
    fr[:] = paper('9BDB6A'); flow_bg(fr, T)
    stk(fr, SUGAR, 320, 1030, T, 5, .55 * ent(t - .8), -6)
    stk(fr, WATER, 780, 1030, T, 6, .75 * ent(t - 2.6), 5)
    overlay(fr, cairo_layer(lambda c: (c.arc(CX, 1030, 50, 0, 2 * math.pi), c.set_source_rgba(1, 1, 1, 1), c.fill_preserve(), ink(c, 6), c.stroke()) if t > 2.2 else None))
    if t > 2.2: put_rgba(fr, ttext('या', 40, HI_B, '1C1614', sw=0, shadow=False), CX, 1030, ent(t - 2.2), 1.0, 0)
    title(fr, 'अगली बार ट्राई करो', 500, t, 108, 'FFFFFF', -2)
    tape(fr, 'साँस रोको + छोटे घूँट', 760, 1330, t - 3.0, 'FFC93C', 42, rot=3)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FF6B5B'); flow_bg(fr, T)
    stk(fr, WOMAN, 380, 1090, T, 7, .72, -3)
    overlay(fr, cairo_layer(lambda c: (granny_bubble(c, 760, 800, 420, 200), hic_burst(c, 820, 1180, .7, T))))
    put_rgba(fr, ttext('कौन याद कर रहा है?', 40, HI_B, '1C1614', sw=0, shadow=False), 760, 792, ent(t - 3.4), 1.0, -2)
    put_rgba(fr, ttext('हिच!', 56, HI_B, 'E63946', sw=5), 820, 1186, 1.0, 1.0, -8)
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A'); flow_bg(fr, T)
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, s5=sc_s5, w1=sc_w1, e1=sc_e1)
