
# ================= 75 phate honth (chapped lips) — HEALTH = GREEN paper, headline cards, real photos
PUR = '226E44'; _PP.clear(); THEME['end_text'] = PUR
TOTAL = 55.5; BRAND0 = 999.0
A75 = '/home/claude/studio/assets/75/'
def _fc75(name, fx0, fy0, fx1, fy1, w=620):
    im = Image.open(A75 + name); a, b = im.size
    return film_card(A75 + name, (int(fx0 * a), int(fy0 * b), int(fx1 * a), int(fy1 * b)), w)
LIPS = _fc75('chapped.jpg', .08, .02, .92, .98, 660)          # real chapped lips (CC BY-SA 3.0)
LICK = _fc75('licker.jpg', .18, .30, .86, .86, 560)            # lip licker's dermatitis (CC BY-SA 3.0)
@functools.lru_cache(maxsize=1)
def jelly_cut():
    from rembg import remove, new_session
    im = Image.open(A75 + 'pjelly.jpg').convert('RGB'); a, b = im.size
    im = im.crop((int(.22 * a), int(.10 * b), int(.98 * a), int(.92 * b)))
    o = remove(im, session=new_session('u2netp')); o = o.crop(o.getbbox())
    return die_cut(np.array(o.resize((int(o.width * 360 / o.height), 360))))

def tongue(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s * 1.3, s * .78)
    c.move_to(-70, -40); c.curve_to(-80, 60, -40, 120, 0, 120); c.curve_to(40, 120, 80, 60, 70, -40); c.close_path()
    g = cairo.LinearGradient(0, -40, 0, 120); g.add_color_stop_rgba(0, .93, .35, .45, a); g.add_color_stop_rgba(1, .85, .22, .35, a)
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(*hx(INKP, a)); c.set_line_width(6); c.stroke()
    c.move_to(0, -30); c.line_to(0, 70); c.set_source_rgba(.6, .12, .22, a * .8); c.set_line_width(5); c.stroke()
    c.arc(-30, 10, 10, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, .35 * a); c.fill()
    c.restore()

def balm_guy(c, x, y, s, T, mood='smug', a=1.0):
    """cute-evil unbranded lip balm stick"""
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(.06 * math.sin(T * 3))
    rrect(c, -55, -150, 110, 70, 26); c.set_source_rgba(*hx('A8F0D4', a)); c.fill_preserve(); c.set_source_rgba(*hx(INKP, a)); c.set_line_width(6); c.stroke()  # balm tip
    rrect(c, -62, -95, 124, 240, 22); c.set_source_rgba(*hx('E8FFF6', a)); c.fill_preserve(); c.set_source_rgba(*hx(INKP, a)); c.set_line_width(7); c.stroke()
    rrect(c, -62, 5, 124, 70, 0); c.set_source_rgba(*hx('2EC4A0', a)); c.fill()
    for k in range(3):                                                   # mint leaf on label
        c.save(); c.translate(-20 + k * 20, 40); c.rotate(-.6 + k * .6); c.scale(1, .5); c.arc(0, 0, 14, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*hx('E8FFF6', a)); c.fill()
    for sx in (-1, 1):
        c.arc(sx * 24, -45, 15, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a); c.fill_preserve(); c.set_source_rgba(*hx(INKP, a)); c.set_line_width(4); c.stroke()
        c.arc(sx * 24 + 4, -42, 7, 0, 2 * math.pi); c.set_source_rgba(*hx(INKP, a)); c.fill()
        c.move_to(sx * 40, -72); c.line_to(sx * 10, -62); c.set_line_width(6); c.stroke()
    if mood == 'smug': c.arc(0, -18, 22, .1 * math.pi, .9 * math.pi)
    else: c.arc(0, -10, 26, .05 * math.pi, .95 * math.pi)
    c.set_source_rgba(*hx(INKP, a)); c.set_line_width(6); c.stroke()
    c.restore()

def drop(c, x, y, r, a=1.0, face=False):
    c.move_to(x, y - r * 1.6); c.curve_to(x + r * .9, y - r * .5, x + r, y + r * .2, x, y + r); c.curve_to(x - r, y + r * .2, x - r * .9, y - r * .5, x, y - r * 1.6)
    c.set_source_rgba(.45, .78, 1, a); c.fill_preserve(); c.set_source_rgba(*hx(INKP, a)); c.set_line_width(4); c.stroke()
    if face:
        for sx in (-1, 1): c.arc(x + sx * r * .3, y - r * .1, r * .13, 0, 2 * math.pi); c.set_source_rgba(*hx(INKP, a)); c.fill()

# ---------------- scenes
def sc_l1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 1.4 if thumb else t
    ebg(fr, 'black', T)
    k = back(clamp(tt / .3))
    _put0(fr, LIPS, CX, 1060, .95 * k, 1.0, -3 + .6 * math.sin(int(CUR[0] * 8) * 2.3))
    sw = clamp((tt - .3) / 1.3)                                          # tongue sweeps across the lips
    def dr(c):
        if 0 < sw < 1 or thumb:
            p = .5 if thumb else sw
            tongue(c, lerp(240, 840, p), 1000 + 30 * math.sin(p * 9), 1.7)
            c.rectangle(240, 990, (lerp(240, 840, p) - 240), 90); c.set_source_rgba(1, 1, 1, .18); c.fill()   # wet shine trail
        if not thumb and 1.9 < tt < 3.2: tick_ring(c, 860, 820, 60, back(clamp((tt - 1.9) / .3)), True)
        if not thumb and tt > 3.3: tick_ring(c, 860, 820, 60, back(clamp((tt - 3.3) / .3)), False)
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('होंठ ', 0), ('चाटते', 1), (' हो?', 0)], 380, tt + 1.0, 124)
    if tt > 4.3: title_line(fr, [('यहीं गलती है', 3)], 560, tt - 4.3, 124)

def sc_l2(fr, T, t, l):
    ebg(fr, 'cream', T)
    def dr(c):
        for i, (x, lab, gl) in enumerate(((290, 'चेहरा', True), (790, 'होंठ', False))):
            k = back(clamp((t - .2 - i * .35) / .35))
            if k <= 0: continue
            c.save(); c.translate(x, 1040); c.scale(k, k); c.translate(-x, -1040)
            chain_card(c, x, 1040, 420, 440, 1.0)
            for j in range(4):                                           # skin layers
                c.rectangle(x - 180, 900 + j * 50, 360, 46); c.set_source_rgba(*hx(['F6C9B0', 'F2B8A0', 'EBA58C', 'E2927A'][j])); c.fill()
            if gl:
                for gx in (-110, 0, 110):
                    c.arc(x + gx, 1060, 30, 0, 2 * math.pi); c.set_source_rgba(*hx('FFD65C')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(4); c.stroke()
                    c.move_to(x + gx, 1030); c.line_to(x + gx, 900); c.set_line_width(5); c.stroke()
            else:
                rng = np.random.default_rng(4)
                for d in range(5):
                    ph = (t * .6 + d * .2) % 1
                    drop(c, x - 120 + d * 60, 890 - ph * 160, 14, (1 - ph) * clamp((t - 3.9) / .4))
            c.restore()
        if t > 1.3: tick_ring(c, 790, 1130, 54, back(clamp((t - 1.3) / .3)), False)
    overlay(fr, cairo_layer(dr))
    for i, (x, lab) in enumerate(((290, 'चेहरा'), (790, 'होंठ'))):
        if t > .4 + i * .35: _put0(fr, htext(lab, 52, INKP, ANEK), x, 1230, 1.0, 1.0, 0)
    title_line(fr, [('तेल ग्रंथि: ', 0), ('ज़ीरो', 1)], 380, t, 124)
    if t > 3.9: title_line(fr, [('जल्दी सूखते हैं', 3)], 560, t - 3.9, 118)

def sc_l3(fr, T, t, l):
    ebg(fr, 'black', T)
    _put0(fr, LIPS, CX, 1080, .9, 1.0, 2 + .6 * math.sin(int(CUR[0] * 8) * 2.3))
    def dr(c):
        rng = np.random.default_rng(6)
        for i in range(12):
            x0 = 300 + rng.random() * 480; y0 = 1040 + rng.random() * 90
            u = t - .8 - i * .12
            if u < 0: drop(c, x0, y0, 16, .9, True); continue
            yy = y0 - 380 * ease(clamp(u / 1.6)); a = 1 - clamp((u - 1.0) / .6)
            if a > 0: drop(c, x0 + 30 * math.sin(u * 4 + i), yy, 16, a, True)
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('थूक सूखा', 0)], 380, t, 124)
    if t > 2.6: title_line(fr, [('नमी भी ले गया', 3)], 560, t - 2.6, 118)
    note(fr, 'नमी उड़ गई', 830, 760, t - 3.2, 50, YL, 6)

def sc_l4(fr, T, t, l):
    ebg(fr, 'cream', T)
    x = lerp(W + 200, CX, ease(clamp(t / .5)))
    overlay(fr, cairo_layer(lambda c: balm_guy(c, x, 1100, 1.6, T, 'smug')))
    def fx(c):
        if t > 2.2:
            for i in range(10):
                ph = (T * .2 + i * .1) % 1; snowflake(c, 200 + (i * 83) % 700, 760 + ph * 560, 14, .9 * clamp((t - 2.2) / .3), T + i)
    overlay(fr, cairo_layer(fx))
    title_line(fr, [('तो बाम लगाया', 0)], 380, t, 124)
    if t > 1.5: title_line(fr, [('पुदीना + ठंडक', 3)], 560, t - 1.5, 118)

def sc_l5(fr, T, t, l):
    ebg(fr, 'black', T)
    _put0(fr, LIPS, CX, 1100, .85, 1.0, -2 + .6 * math.sin(int(CUR[0] * 8) * 2.3))
    red = clamp((t - 3.5) / .3)
    def dr(c):
        balm_guy(c, 880, 880, .9, T, 'evil' if red > 0 else 'smug')
        if t > .4:
            for i in range(8):
                ang = i / 8 * 2 * math.pi + T * 2; r0 = 300
                x0, y0 = CX + r0 * math.cos(ang), 1100 + r0 * .45 * math.sin(ang)
                zap(c, x0, y0, x0 + 40 * math.cos(ang), y0 + 40 * math.sin(ang), T, 6, lerp_col(YL, RED, red) if False else (RED if red > .5 else YL))
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('झनझनाहट = असर?', 0)], 380, t, 118)
    if t > 3.5: title_line(fr, [('नहीं, ये जलन है', 3)], 560, t - 3.5, 118)

def cycle_arrows(c, cx, cy, R, T, k):
    for i in range(3):
        a0 = i * 2 * math.pi / 3 + T * .9; a1 = a0 + 1.6
        c.arc(cx, cy, R * k, a0, a1); c.set_source_rgba(*hx(INKP)); c.set_line_width(14); c.stroke()
        x, y = cx + R * k * math.cos(a1), cy + R * k * math.sin(a1); dx, dy = -math.sin(a1), math.cos(a1)
        c.move_to(x + dx * 26, y + dy * 26); c.line_to(x - dy * 22, y + dx * 22); c.line_to(x + dy * 22, y - dx * 22); c.close_path(); c.fill()
def sc_l6(fr, T, t, l):
    ebg(fr, 'cream', T)
    items = [(0.0, 'मेंथॉल', '2EC4A0'), (.72, 'कपूर', 'FBF7EE'), (1.34, 'खुशबू', 'FFB3C7')]
    cyc = clamp((t - 3.75) / .4)
    def dr(c):
        for i, (ts, lab, col) in enumerate(items):
            k = back(clamp((t - ts) / .3)) * (1 - cyc)
            if k <= 0: continue
            x = 230 + i * 310; y = 1010 + (i % 2) * 70
            c.save(); c.translate(x, y); c.scale(k, k); c.rotate((i - 1) * .08)
            rrect(c, -130, -110, 260, 220, 24); c.set_source_rgba(0, 0, 0, .3); c.fill()
            rrect(c, -140, -120, 260, 220, 24); c.set_source_rgba(*hx(col)); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
            c.restore()
        if cyc > 0: cycle_arrows(c, CX, 1060, 230, T, back(cyc))
    overlay(fr, cairo_layer(dr))
    for i, (ts, lab, col) in enumerate(items):
        k = clamp((t - ts - .1) / .2) * (1 - cyc)
        if k > 0: _put0(fr, htext(lab, 64, INKP, ANEK), 220 + i * 310, 1000 + (i % 2) * 70, 1.0, k, (i - 1) * 4.5)
    if cyc > 0:
        for j, lab in enumerate(('बाम', 'सूखे होंठ', 'फिर बाम')):
            a = j * 2 * math.pi / 3 - math.pi / 2
            _put0(fr, htext(lab, 54, REDP if j == 2 else INKP, ANEK), CX + 330 * math.cos(a), 1060 + 300 * math.sin(a), 1.0, cyc, 0)
    title_line(fr, [('और सुखाते हैं', 1)], 380, t, 124)
    if t > 3.7: title_line(fr, [('फिर बाम, फिर बाम', 3)], 560, t - 3.7, 112)

def sc_l7(fr, T, t, l):
    ebg(fr, 'black', T)
    _put0(fr, LICK, CX, 1090, .95, 1.0, 3 + .6 * math.sin(int(CUR[0] * 8) * 2.3))
    def dr(c):
        if t > 2.9: tongue(c, 260, 1300, .8 * back(clamp((t - 2.9) / .3)))
        if t > 4.35: balm_guy(c, 830, 1270, .75 * back(clamp((t - 4.35) / .3)), T, 'evil')
        k = clamp(t / .3) * (1 - clamp((t - 1.4) / .3))
        if k > 0: snowflake(c, CX, 760, 60 * k, 1.0, T)
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('ठंड बस शुरुआत', 0)], 380, t, 120)
    if t > 2.8: title_line(fr, [('विलेन: जीभ + बाम', 3)], 560, t - 2.8, 116, sel=True)

def sc_l8(fr, T, t, l):
    ebg(fr, 'cream', T)
    rows = [(.9, 'जीभ फेरना बंद'), (2.8, 'बिना खुशबू पेट्रोलियम जेली'), (4.45, 'दिन में कई बार और रात को')]
    def dr(c):
        for i, (ts, _) in enumerate(rows):
            k = back(clamp((t - ts) / .3))
            if k <= 0: continue
            y = 790 + i * 170
            c.save(); c.translate(CX, y); c.scale(k, k); c.translate(-CX, -y)
            chain_card(c, CX, y, 860, 130, 1.0); tick_ring(c, 170, y, 40, 1.0, True); c.restore()
    overlay(fr, cairo_layer(dr))
    for i, (ts, txt) in enumerate(rows):
        k = clamp((t - ts - .1) / .2)
        if k > 0: _put0(fr, htext(txt, 50, INKP, ANEK), CX + 50, 790 + i * 170, 1.0, k, 0)
    if t > 2.9: _put0(fr, jelly_cut(), 850, 1330, .7 * back(clamp((t - 2.9) / .3)), 1.0, 6)
    title_line(fr, [('इलाज सीधा', 3)], 380, t, 124)

def sc_l9(fr, T, t, l):
    ebg(fr, 'black', T)
    def dr(c):
        k = back(clamp(t / .35))
        c.save(); c.translate(CX, 1020); c.scale(k, k)
        rrect(c, -300 + 12, -230 + 14, 600, 460, 30); c.set_source_rgba(0, 0, 0, .35); c.fill()
        rrect(c, -300, -230, 600, 460, 30); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
        rrect(c, -300, -230, 600, 90, 30); c.set_source_rgba(*hx(REDP)); c.fill()
        n = int(clamp((t - .5) / 2.4) * 21)
        for d in range(21):
            r_, q = divmod(d, 7); x = -240 + q * 80; y = -100 + r_ * 100
            c.rectangle(x - 30, y - 30, 60, 60); c.set_source_rgba(*hx(INKP, .15)); c.fill()
            if d < n: tick_ring(c, x, y, 26, 1.0, True)
        c.restore()
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('2-3 हफ़्ते में', 0)], 380, t, 124)
    if t > 1.6: title_line(fr, [('होंठ ठीक', 3)], 560, t - 1.6, 124)
    source_tag(fr, 'American Academy of Dermatology', 100, 1330, t - .8)

def sc_l10(fr, T, t, l):
    ebg(fr, 'cream', T)
    k = back(clamp(t / .4))
    def phone(c):
        c.save(); c.translate(CX, 1040); c.rotate(-.05); c.scale(k * .92, k * .92)
        rrect(c, -230, -330, 460, 660, 56); c.set_source_rgba(*hx('111111')); c.fill()
        rrect(c, -210, -300, 420, 600, 40); c.set_source_rgba(*hx('0C2C1A')); c.fill(); c.restore()
        if k >= 1:
            tap = clamp((t - 1.0) / .25); s = 1 + .12 * math.sin(math.pi * tap)
            rrect(c, CX - 150 * s, 1160 - 44 * s, 300 * s, 88 * s, 44 * s); c.set_source_rgba(*hx(GRN)); c.fill()
            if t > 1.3:
                a = clamp((t - 1.3) / .2); rrect(c, CX - 60, 760, 360, 90, 30); c.set_source_rgba(1, 1, 1, a); c.fill()
    overlay(fr, cairo_layer(phone))
    _put0(fr, LIPS, CX, 960, .45 * k, 1.0, -4)
    if k >= 1: _put0(fr, htext('भेजो', 52, 'FFFFFF', ANEK), CX, 1160, 1.0, 1.0, 0)
    if t > 1.3: _put0(fr, htext('होंठ मत चाट', 44, INKP, ANEK), CX + 120, 805, 1.0, clamp((t - 1.3) / .2), 0)
    title_line(fr, [('उस दोस्त को ', 0), ('भेजो', 1)], 380, t, 116)
    if t > 1.7: title_line(fr, [('जो होंठ चाटता है', 0)], 552, t - 1.7, 104)

def heel(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(.62, 1); c.arc(0, 40, 170, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hx('F2B8A0')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(7); c.stroke()
    for i, (tx, ty, tr) in enumerate(((-62, -150, 30), (-18, -172, 24), (20, -170, 21), (54, -158, 18), (82, -136, 15))):
        c.arc(tx, ty, tr, 0, 2 * math.pi); c.set_source_rgba(*hx('F2B8A0')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
    for i in range(6):
        x0 = -60 + i * 24; c.move_to(x0, 205); c.line_to(x0 + 8 * math.sin(i * 2), 150); c.line_to(x0 - 6, 110)
    c.set_source_rgba(.62, .2, .16, 1); c.set_line_width(5); c.stroke(); c.restore()
def sc_l11(fr, T, t, l):
    ebg(fr, 'black', T)
    overlay(fr, cairo_layer(lambda c: heel(c, CX, 1060, 1.5 * back(clamp((t - .9) / .35)), T)))
    title_line(fr, [('और सर्दी में', 0)], 380, t, 120)
    title_line(fr, [('फटी एड़ियाँ?', 3)], 560, t - .9, 124)
    if t > 2.3: tape(fr, 'पार्ट 2 जल्द', 800, 1330, t - 2.3, 'FFE45C', 50, HI_B, 8)

def sc_le(fr, T, t, l):
    ebg(fr, 'end', T)
    title_line(fr, [('रोज़ के सच के लिए', 0)], 380, t + .3, 104)
    title_line(fr, [('FreshNestHub', 2)], 560, t + .1, 120)
    def dr(c): logo(c, CX, 1030, 170 * back(clamp(t / .4)))
    overlay(fr, cairo_layer(dr))
    _put0(fr, htext('फ़ॉलो करो', 84, PUR, ANEK), CX, 1290, back(clamp((t - .6) / .3)), 1.0, 0)

SCENES = dict(s1=sc_l1, s2=sc_l2, s3=sc_l3, s4=sc_l4, s5=sc_l5, s6=sc_l6, s7=sc_l7, s8=sc_l8, s9=sc_l9, s10=sc_l10, s11=sc_l11, e1=sc_le)
SHAKES = [(3.3, 22), (7.0, 12), (13.5, 12), (22.6, 26), (27.4, 14), (31.9, 18), (33.4, 26), (43.3, 12), (50.7, 18)]
FOCUS = dict(s2=1040, s3=1080, s4=1100, s5=1100, s6=1060, s7=1090, s8=1000, s9=1020, s10=1040, s11=1060)
