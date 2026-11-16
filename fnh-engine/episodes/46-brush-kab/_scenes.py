
import os
V = os.environ.get('V', 'ig')

def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

def opt(path, **kw):
    return load_rgba(path, **kw) if os.path.exists(path) else None

A46 = '/home/claude/studio/assets/46/'
BRUSH = opt(A46 + 'st_brush.png', w=640)
LEMON = opt(A46 + 'st_lemon.png', w=520)
ORANGE = opt(A46 + 'st_orange.png', w=520)
PICKLE = opt(A46 + 'st_pickle.png', h=420)
TAMARIND = opt(A46 + 'st_tamarind.png', w=480)
COLA = opt(A46 + 'st_cola.png', h=460)
TOOTH = opt(A46 + 'st_tooth.png', h=520)

def stk(fr, im, x, y, T, k, sc, rot=0, t=None):
    if im is None: return
    if t is None: sticker(fr, im, x, y, T, k, sc, rot)
    else: sticker(fr, im, x, y, T, k, sc, rot, t)

def tooth_draw(c, x, y, s, T, soft=0.0, worn=0.0, shine=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def body():
        c.new_path(); c.move_to(-150, -120); c.curve_to(-160, -230, -40, -240, 0, -190); c.curve_to(40, -240, 160, -230, 150, -120)
        c.curve_to(150, 0, 120, 60, 100, 220); c.curve_to(90, 270, 40, 270, 30, 210); c.line_to(10, 80); c.line_to(-10, 80); c.line_to(-30, 210)
        c.curve_to(-40, 270, -90, 270, -100, 220); c.curve_to(-120, 60, -150, 0, -150, -120); c.close_path()
    shadowed(c, body, 'FFF6E8')
    # enamel cap
    c.save(); body(); c.clip()
    th = 46 * (1 - worn)
    c.new_path(); c.move_to(-170, -120 + 40); c.curve_to(-170, -260, 170, -260, 170, -120 + 40); c.line_to(170, -120 + 40 + th); c.curve_to(170, -260 + th, -170, -260 + th, -170, -120 + 40 + th)
    col = np.array(hx('BFE8FF')[:3]) * (1 - soft) + np.array(hx('FFD24A')[:3]) * soft
    c.rectangle(-200, -260, 400, 160 * (1 - worn * .7)); c.set_source_rgba(*col, .85); c.fill()
    if shine > 0:
        c.save(); c.translate(-70, -150); c.rotate(-.5); c.scale(1, .35); c.arc(0, 0, 50, 0, 2 * math.pi); c.restore(); c.set_source_rgba(1, 1, 1, .9 * shine); c.fill()
    if soft > .3:
        rnd = np.random.default_rng(3)
        for k in range(14):
            px, py = rnd.uniform(-130, 130), rnd.uniform(-200, -120)
            c.arc(px, py, 6 + 4 * math.sin(T * 5 + k), 0, 2 * math.pi); c.set_source_rgba(*hx('E6A800', .6 * soft)); c.fill()
    c.restore()
    body(); ink(c, 8); c.stroke()
    for ex in (-50, 50): c.arc(ex, -60, 12, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    if worn > .3: c.arc(0, 0, 34, math.pi + .3, -.3); ink(c, 7); c.stroke()
    else: c.arc(0, -20, 34, .3, math.pi - .3); ink(c, 7); c.stroke()
    c.restore()

def brush_draw(c, x, y, s, T, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    def h():
        c.new_path(); c.rectangle(-300, -26, 480, 52)
    shadowed(c, h, '2D6CDF', 8, 10, 6)
    c.rectangle(180, -60, 130, 40); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 5); c.stroke()
    for k in range(7): c.move_to(190 + k * 18, -60); c.line_to(190 + k * 18, -20); ink(c, 3); c.stroke()
    c.restore()

def glass(c, x, y, s, T, col='FFF2A8', level=.75):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path(); c.move_to(-110, -180); c.line_to(110, -180); c.line_to(85, 180); c.line_to(-85, 180); c.close_path()
    c.save(); c.translate(12, 14); p(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    p(); c.set_source_rgba(*hx('E8F7FF')); c.fill()
    top = 180 - 360 * level
    c.save(); p(); c.clip(); c.rectangle(-120, top, 240, 400); c.set_source_rgba(*hx(col, .9)); c.fill(); c.restore()
    p(); ink(c, 8); c.stroke()
    c.rectangle(-70, -160, 22, 300); c.set_source_rgba(1, 1, 1, .5); c.fill()
    c.restore()

def clock(c, x, y, r, T, prog):
    c.arc(x + 10, y + 12, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(x, y); c.arc(x, y, r * .82, -math.pi / 2, -math.pi / 2 + 2 * math.pi * prog); c.close_path(); c.set_source_rgba(*hx('3FAE5A', .55)); c.fill()
    a = -math.pi / 2 + 2 * math.pi * prog
    c.move_to(x, y); c.line_to(x + r * .7 * math.cos(a), y + r * .7 * math.sin(a)); ink(c, 9); c.stroke()

def acid_drops(c, x, y, T, a=1.0, n=6, col='C8E64A'):
    for k in range(n):
        ph = (T * 1.2 + k / n) % 1
        dx = x - 160 + k * 64; dy = y - 220 + ph * 200
        c.save(); c.translate(dx, dy); c.move_to(0, -26); c.curve_to(20, 0, 20, 20, 0, 20); c.curve_to(-20, 20, -20, 0, 0, -26); c.close_path()
        c.set_source_rgba(*hx(col, a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(3); c.stroke(); c.restore()

def scrub_marks(c, x, y, T, a=1.0):
    for k in range(4):
        ox = 40 * math.sin(T * 18 + k)
        c.move_to(x - 120 + ox, y - 40 + k * 26); c.line_to(x + 120 + ox, y - 50 + k * 26); c.set_source_rgba(*hx('E63946', a)); c.set_line_width(6); c.stroke()

SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('FFC93C')
    overlay(fr, cairo_layer(lambda c: glass(c, 360, 1060, .95 * ent(T + .5), T, 'FFF2A8', .72)))
    stk(fr, LEMON, 520, 1240, T, 0, .6 * ent(T + .3), -10)
    if BRUSH is not None: stk(fr, BRUSH, 760, 960, T, 1, .85 * ent(t - 1.9, .35), -35)
    else: overlay(fr, cairo_layer(lambda c: brush_draw(c, 760, 960, .9 * ent(t - 1.9, .35), T, -.6)))
    if V == 'yt': title(fr, 'खाने के बाद तुरंत ब्रश?', 520, T + 1.0, 104, 'E63946', -2.5)
    else: title(fr, 'नींबू पानी के बाद ब्रश?', 520, T + 1.0, 104, 'E63946', -2.5)
    tape(fr, 'वाह, कितने हेल्दी!', CX, 1330, t - 3.6, 'FFFFFF', 50, rot=-3)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .05, .4, 20)
    fr[:] = paper('E63946')
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    if TOOTH is not None: stk(fr, TOOTH, CX + dx, 1040 + dy, T, 2, .95, -4)
    else: overlay(fr, cairo_layer(lambda c: tooth_draw(c, CX + dx, 1040 + dy, 1.1, T, worn=clamp((t - 1.0) / 2.5))))
    overlay(fr, cairo_layer(lambda c: scrub_marks(c, CX + dx, 900 + dy, T, clamp((t - 1.0) / .3))))
    title(fr, 'रुको!', 500, t, 170, 'FFC93C', -4)
    tape(fr, 'दाँत चुपचाप घिस रहे!', CX, 1340, t - 1.6, 'FFFFFF', 50, rot=-2)

def sc_s1(fr, T, t, l):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: tooth_draw(c, 360, 1050, .9, T)))
    if BRUSH is not None: stk(fr, BRUSH, 760, 1000, T, 3, .7, -20, t - .4)
    else: overlay(fr, cairo_layer(lambda c: brush_draw(c, 760, 1000, .8, T, -.4)))
    title(fr, 'बहुत लोग सोचते हैं...', 500, t, 104, 'FFFFFF', -2)
    tape(fr, 'तुरंत ब्रश = साफ़ दाँत?', CX, 700, t - 1.4, 'FFC93C', 50, rot=-2)
    burst(fr, 'ट्विस्ट!', 820, 1320, t - 5.0, 110, 'E63946', HI_B, 48)

def sc_s2(fr, T, t, l):
    fr[:] = paper('8E5CD9')
    items = [(LEMON, 290, 840, .5), (ORANGE, 790, 840, .55), (PICKLE, 290, 1170, .55), (TAMARIND, 540, 1010, .5), (COLA, 790, 1170, .55)]
    times = [.0, .55, 1.15, 1.75, 2.4]
    for i, ((im, x, y, sc), tt) in enumerate(zip(items, times)):
        stk(fr, im, x, y, T, 4 + i, sc * ent(t - tt, .3), (-8, 6, -4, 8, -6)[i])
    title(fr, 'इन सब में एसिड!', 500, t, 116, 'FFFFFF', -2)
    tape(fr, 'नींबू, संतरा, अचार, इमली, कोल्ड ड्रिंक', CX, 1360, t - .2, 'FFC93C', 40, rot=-2)

def sc_s3(fr, T, t, l):
    fr[:] = paper('17A2B8')
    def dr(c):
        tooth_draw(c, CX, 1060, 1.25, T, soft=clamp((t - 2.0) / 3.0))
        acid_drops(c, CX, 860, T, clamp(t / .5) * (1 - clamp((t - 6.0) / .8)))
    overlay(fr, cairo_layer(dr))
    title(fr, 'इनेमल नरम हो जाता है', 500, t, 104, 'FFFFFF', -2)
    tape(fr, 'ऊपरी चमकदार परत = इनेमल', 330, 760, t - 2.4, 'FFC93C', 40, rot=-4)
    tape(fr, 'थोड़ी देर के लिए', 780, 1360, t - 5.6, 'FFFFFF', 44, rot=3)

def sc_s4(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 2.6, .4, 18)
    fr[:] = paper('FF6B5B')
    def dr(c):
        tooth_draw(c, CX + dx, 1070 + dy, 1.2, T, soft=1.0 * (1 - clamp((t - 1.0) / 3.0)) * .8, worn=clamp((t - 1.0) / 3.5), shine=1 - clamp((t - 1.0) / 3.0))
        if 1.0 < t < 5.0:
            brush_draw(c, CX + 60 * math.sin(T * 16), 860, .7, T, .1)
            scrub_marks(c, CX, 900, T)
    overlay(fr, cairo_layer(dr))
    title(fr, 'तुरंत ब्रश = घिसाई!', 500, t, 112, 'FFFFFF', -2)
    burst(fr, 'वापस नहीं उगता!', 800, 1330, t - 6.6, 110, '1C1614', HI_B, 38)

def sc_w1(fr, T, t, l):
    fr[:] = paper('9BDB6A')
    def dr(c):
        glass(c, 280, 1000, .65 * ent(t - .8), T, 'BDE7FF', .7)
        clock(c, 760, 960, 150 * ent(t - 4.6), T, clamp((t - 5.0) / 2.6) * .75)
        tooth_draw(c, 540, 1230, .5 * ent(t - 7.6), T, shine=1.0)
        if t > 8.4: tickmark(c, 680, 1180, 60 * ent(t - 8.4))
    overlay(fr, cairo_layer(dr))
    title(fr, 'डेंटिस्ट का तरीका', 500, t, 112, 'FFFFFF', -2)
    tape(fr, 'पहले पानी से कुल्ला', 280, 760, t - 1.4, 'FFC93C', 42, rot=-4)
    tape(fr, '30-60 मिनट रुको', 760, 760, t - 5.0, 'FFFFFF', 44, rot=4)
    tape(fr, 'थूक = इनेमल मज़बूत', CX, 1400 - 60, t - 7.8, 'E63946', 42, rot=-2, tcol='FFFFFF')

def sc_w2(fr, T, t, l):
    fr[:] = paper('FFF8E7')
    def dr(c):
        num = lambda x, y, n, col, sc: (c.arc(x + 8, y + 10, 60 * sc, 0, 2 * math.pi), c.set_source_rgba(*hx('1C1614')), c.fill(),
                                         c.arc(x, y, 60 * sc, 0, 2 * math.pi), c.set_source_rgba(*hx(col)), c.fill_preserve(), ink(c, 6), c.stroke())
        num(200, 820, 1, '3FAE5A', ent(t - 1.8)); num(200, 1170, 2, 'FFC93C', ent(t - 3.0))
        glass(c, 760, 1180, .55 * ent(t - 3.0), T, 'FFF2A8', .72)
    overlay(fr, cairo_layer(dr))
    if BRUSH is not None: stk(fr, BRUSH, 680, 840, T, 9, .7 * ent(t - 1.8), -15)
    else: overlay(fr, cairo_layer(lambda c: brush_draw(c, 680, 840, .8 * ent(t - 1.8), T, -.3)))
    stk(fr, LEMON, 880, 1300, T, 10, .35 * ent(t - 3.2), 10)
    if t > 1.8: put_rgba(fr, ttext('1', 70, LUCKY, 'FFFFFF', sw=6), 200, 826, ent(t - 1.8), 1.0, -4)
    if t > 3.0: put_rgba(fr, ttext('2', 70, LUCKY, 'FFFFFF', sw=6), 200, 1176, ent(t - 3.0), 1.0, -4)
    title(fr, 'सुबह का आसान तरीका', 500, t, 108, 'E63946', -2)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FF8C1A')
    stk(fr, PICKLE, 330, 1060, T, 11, .6, -6)
    if BRUSH is not None: stk(fr, BRUSH, 760, 1040 + 30 * math.sin(T * 10), T, 12, .7 * ent(t - 1.6), -25)
    else: overlay(fr, cairo_layer(lambda c: brush_draw(c, 760, 1040, .8 * ent(t - 1.6), T, -.4)))
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)
    burst(fr, 'ब्रश लेकर भागा!', CX, 1330, t - 2.4, 110, 'E63946', HI_B, 40)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A')
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, w1=sc_w1, w2=sc_w2, e1=sc_e1)
