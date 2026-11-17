
import os
V = os.environ.get('V', 'ig')

def shadowed(c, path, col, dx=14, dy=16, lw=8):
    c.save(); c.translate(dx, dy); path(); c.set_source_rgba(*hx('1C1614')); c.fill(); c.restore()
    path(); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, lw); c.stroke()

A = '/home/claude/studio/assets/48/'
def opt(n, **kw):
    p = A + n
    return load_rgba(p, **kw) if os.path.exists(p) else None
CHAI = opt('st_chai.png', h=620)
CUP = opt('st_cup.png', w=640)
DAL = opt('st_dal.png', w=560)
ROTI = opt('st_roti.png', w=520)
PALAK = opt('st_palak.png', w=560)
THALI = opt('st_thali.png', w=760)
AMLA = opt('card_amla.png', w=520)
WOMAN = opt('st_woman.png', h=760)

def stk(fr, im, x, y, T, k, sc, rot=0, t=None):
    if im is None or sc <= 0.01: return
    if t is None: sticker(fr, im, x, y, T, k, sc, rot)
    else: sticker(fr, im, x, y, T, k, sc, rot, t)

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

def fe(c, x, y, r, a=1.0):
    c.arc(x + 4, y + 5, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(*hx('B3122E', a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(4); c.stroke()

def fe_label(fr, x, y, sc):
    if sc > .05: put_rgba(fr, ttext('Fe', 34, LUCKY, 'FFFFFF', sw=3, shadow=False), x, y + 2, sc, 1.0, 0)

def iron_stream(c, x0, y0, x1, y1, T, n=8, a=1.0):
    pts = []
    for k in range(n):
        ph = (T * .5 + k / n) % 1
        x = x0 + (x1 - x0) * ph; y = y0 + (y1 - y0) * ph - 180 * math.sin(ph * math.pi)
        fe(c, x, y, 28, a * (1 - .3 * ph)); pts.append((x, y))
    return pts

def tannin(c, x, y, s, T, grab=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    def p():
        c.new_path()
        for k in range(10):
            a = k * math.pi / 5 + T * .6; r = 70 if k % 2 == 0 else 52
            c.line_to(r * math.cos(a), r * math.sin(a))
        c.close_path()
    shadowed(c, p, '8B4513', 6, 8, 5)
    for ex in (-18, 18): c.arc(ex, -8, 9, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill(); c.arc(ex + 2, -6, 4, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 18, 18, .2, math.pi - .2); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(5); c.stroke()
    for k in range(4):
        a = k * math.pi / 2 + .4
        L = 80 + 40 * grab
        c.move_to(60 * math.cos(a), 60 * math.sin(a)); c.line_to(L * math.cos(a), L * math.sin(a)); ink(c, 7); c.stroke()
    c.restore()

def bars(c, x, y, T, p1, p2):
    w = 760
    c.rectangle(x - w / 2 + 12, y - 170 + 14, w, 340); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.rectangle(x - w / 2, y - 170, w, 340); c.set_source_rgba(*hx('FFF8E7')); c.fill_preserve(); ink(c, 8); c.stroke()
    for i, (v, col, p) in enumerate(((1.0, '3FAE5A', p1), (.38, 'E63946', p2))):
        by = y - 110 + i * 130
        L = (w - 300) * v * p
        c.rectangle(x - w / 2 + 250, by, max(4, L), 90); c.set_source_rgba(*hx(col)); c.fill_preserve(); ink(c, 5); c.stroke()

def clock(c, x, y, r, T, prog):
    c.arc(x + 10, y + 12, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(x, y, r, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); ink(c, 8); c.stroke()
    c.move_to(x, y); c.arc(x, y, r * .82, -math.pi / 2, -math.pi / 2 + 2 * math.pi * prog); c.close_path(); c.set_source_rgba(*hx('3FAE5A', .55)); c.fill()
    a = -math.pi / 2 + 2 * math.pi * prog
    c.move_to(x, y); c.line_to(x + r * .7 * math.cos(a), y + r * .7 * math.sin(a)); ink(c, 9); c.stroke()

def lemon(c, x, y, r, sc):
    if sc <= 0: return
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.arc(8, 10, r, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614')); c.fill()
    c.arc(0, 0, r, 0, 2 * math.pi); c.set_source_rgba(*hx('FFE14A')); c.fill_preserve(); ink(c, 7); c.stroke()
    c.arc(0, 0, r * .82, 0, 2 * math.pi); c.set_source_rgba(*hx('FFF6B0')); c.fill()
    for k in range(8):
        a = k * math.pi / 4; c.move_to(0, 0); c.line_to(r * .8 * math.cos(a), r * .8 * math.sin(a)); c.set_source_rgba(*hx('F2C200')); c.set_line_width(5); c.stroke()
    c.restore()

SC = {l['id']: l for l in TL}

def sc_h1(fr, T, t, l):
    fr[:] = paper('FF8C1A'); flow_bg(fr, T)
    stk(fr, THALI, 380, 1080, T, 0, .78 * ent(T + .6), -6)
    stk(fr, CHAI, 800, 1020, T, 1, .82 * ent(t - 1.4, .35), 6)
    if V == 'yt': title(fr, 'खाने के बाद चाय = गलती?', 520, T + 1.0, 104, 'FFFFFF', -2.5)
    else: title(fr, 'खाना खाते ही चाय?', 520, T + 1.0, 116, 'FFFFFF', -2.5)
    tape(fr, 'भारत का रिवाज़!', CX, 1360, t - 3.8, 'FFC93C', 50, rot=-3)

def sc_h2(fr, T, t, l):
    dx, dy = shake(T, l['start'] + .05, .4, 20)
    fr[:] = paper('E63946'); flow_bg(fr, T)
    if t < .12: fr[:] = (fr * .3 + 255 * .7).astype(np.uint8)
    stk(fr, THALI, 330 + dx, 1120 + dy, T, 2, .6, -4)
    stk(fr, CHAI, 800 + dx, 960 + dy, T, 3, .7, 8)
    pts = []
    overlay(fr, cairo_layer(lambda c: pts.extend(iron_stream(c, 360, 1060, 780, 880, T, 7, clamp((t - .8) / .5)))))
    for (x, y) in pts: fe_label(fr, x, y, clamp((t - .8) / .5))
    title(fr, 'पर रुको!', 500, t, 160, 'FFC93C', -4)
    tape(fr, 'कप आयरन चुरा रहा है!', CX, 1360, t - 1.4, 'FFFFFF', 48, rot=-2)

def sc_s1(fr, T, t, l):
    fr[:] = paper('8E5CD9'); flow_bg(fr, T)
    stk(fr, CUP, 300, 820, T, 4, .5 * ent(t), -6)
    grab = clamp((t - 4.4) / 1.2)
    pos = []
    def dr(c):
        for i, (tx, ty) in enumerate(((330, 1100), (720, 1050), (540, 1230))):
            fx, fy = tx + 220 - 150 * grab, ty - 30 + 20 * grab
            tannin(c, tx, ty, 1.0 * ent(t - 1.0 - .3 * i), T, grab)
            fe(c, fx + 10 * math.sin(T * 3 + i), fy, 34); pos.append((fx + 10 * math.sin(T * 3 + i), fy))
    overlay(fr, cairo_layer(dr))
    for (x, y) in pos: fe_label(fr, x, y, 1.0)
    title(fr, 'चाय का टैनिन', 500, t, 120, 'FFFFFF', -2)
    tape(fr, 'कड़क रंग वाला', 760, 820, t - 1.8, 'FFC93C', 44, rot=4)
    tape(fr, 'आयरन से चिपक गया!', CX, 1340, t - 4.4, 'E63946', 46, rot=-2, tcol='FFFFFF')

def sc_s2(fr, T, t, l):
    fr[:] = paper('17A2B8'); flow_bg(fr, T)
    stk(fr, DAL, 260, 760, T, 5, .38 * ent(t - 3.2), -8)
    stk(fr, PALAK, 540, 740, T, 6, .34 * ent(t - 4.0), 4)
    stk(fr, ROTI, 820, 760, T, 7, .36 * ent(t - 4.6), 8)
    overlay(fr, cairo_layer(lambda c: bars(c, CX, 1130, T, clamp((t - 1.0) / .8), clamp((t - 5.6) / 1.4))))
    put_rgba(fr, ttext('बिना चाय', 40, HI_B, '1C1614', sw=0, shadow=False), 280, 1085, ent(t - 1.0), 1.0, 0)
    put_rgba(fr, ttext('चाय के साथ', 40, HI_B, '1C1614', sw=0, shadow=False), 280, 1215, ent(t - 5.6), 1.0, 0)
    title(fr, 'रिसर्च में देखा गया', 500, t, 108, 'FFFFFF', -2)
    burst(fr, 'आधे से भी कम!', 800, 1380 - 30, t - 6.4, 110, 'E63946', HI_B, 38)

def sc_s3(fr, T, t, l):
    dx, dy = shake(T, l['start'] + 2.0, .35, 14)
    fr[:] = paper('1C1614'); flow_bg(fr, T, 'E63946', .12)
    stk(fr, WOMAN, CX + dx, 1080 + dy, T, 8, .82, -2)
    title(fr, 'छोटी बात नहीं!', 500, t, 124, 'FFC93C', -2)
    burst(fr, 'आधी से ज़्यादा महिलाएँ', CX, 700, t - 2.0, 140, 'E63946', HI_B, 34)
    tape(fr, 'थकान', 260, 1300, t - 4.8, 'FFC93C', 46, rot=-5)
    tape(fr, 'चक्कर', CX, 1330, t - 5.6, 'FFFFFF', 46, rot=2)
    tape(fr, 'बाल झड़ना', 820, 1300, t - 6.3, 'FFC93C', 46, rot=5)

def sc_w1(fr, T, t, l):
    fr[:] = paper('3FAE5A'); flow_bg(fr, T)
    if t < 6.6:
        stk(fr, THALI, 300, 980, T, 9, .5 * ent(t - 2.0), -4)
        stk(fr, CHAI, 800, 980, T, 10, .55 * ent(t - 4.4), 6)
        overlay(fr, cairo_layer(lambda c: clock(c, CX, 1000, 120 * ent(t - 3.4), T, clamp((t - 3.6) / 2.4))))
        tape(fr, '1 घंटा रुको, फिर चाय', CX, 1330, t - 3.8, 'FFC93C', 48, rot=-2)
    else:
        stk(fr, THALI, 320, 1060, T, 11, .55 * ent(t - 6.6), -4)
        stk(fr, AMLA, 790, 960, T, 12, .58 * ent(t - 7.6), 6)
        overlay(fr, cairo_layer(lambda c: lemon(c, 790, 1260, 90, ent(t - 7.0))))
        tape(fr, 'नींबू या आंवला', 790, 760, t - 7.0, 'FFC93C', 44, rot=4)
        burst(fr, 'विटामिन C', 320, 760, t - 9.4, 100, 'FF8C1A', HI_B, 40)
    title(fr, 'बस टाइमिंग बदलो', 500, t, 116, 'FFFFFF', -2)

def sc_e1(fr, T, t, l):
    fr[:] = paper('FF6B5B'); flow_bg(fr, T)
    stk(fr, THALI, 380, 1080, T, 13, .66, -5)
    stk(fr, CHAI, 760 - 300 * (1 - ent(t - .6, .5)), 1000, T, 14, .7, 8)
    title(fr, 'भेजो उस दोस्त को', 500, t, 108, 'FFFFFF', -2)
    burst(fr, 'चाय पहले आ गई!', CX, 1360, t - 2.6, 110, '2D6CDF', HI_B, 38)

def sc_brand(fr, T, t):
    fr[:] = paper('3FAE5A'); flow_bg(fr, T)
    overlay(fr, cairo_layer(lambda c: logo(c, CX, 860, 200 * ent(t, .4))))
    title(fr, 'FreshNestHub', 1150, t - .3, 110, 'FFFFFF', -2, LUCKY)
    tape(fr, '@fnhtruths  |  @FreshnestHub', CX, 1300, t - .7, 'FFC93C', 40, ELITE, -1)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, s2=sc_s2, s3=sc_s3, w1=sc_w1, e1=sc_e1)
