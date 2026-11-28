
# ================= 76 phati ediyan — NEW style for this topic: red-oxide floor (Indian home), footprint-stamp transitions,
# WANTED poster for the villain (chappal), rear X-ray cutaway of the heel fat pad, fuel-gauge for "oil", board-game remedy path
TOTAL = 62.6; BRAND0 = 999.0
A76 = '/home/claude/studio/assets/76/'
PUR = '8A3320'; THEME['end_text'] = PUR; MUST = 'F2B33D'; TERRA = 'C65A3A'
def _floor():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - 1000) / H * 1.1) ** 2); a = np.clip(1 - r * 1.4, 0, 1)[..., None]
    base = np.array(rgb('7A2A18'), np.float32) * (1 - a) + np.array(rgb('D9694A'), np.float32) * a
    g = np.zeros((H, W), np.float32)
    for x in range(0, W, 180): g[:, x:x + 3] = 1
    for y in range(0, H, 180): g[y:y + 3, :] = 1
    rng = np.random.default_rng(3); n = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 1.5)
    base = base * (1 - .12 * g[..., None]) + cv2.resize(n, (W, H))[..., None] * 5
    return np.clip(base, 0, 255).astype(np.uint8)
_PP['p'] = _floor()
NOLEAF = ('h1', 'a1', 'h3', 'a2', 'h7', 'h8', 'h10', 'h11', 'h12', 'e1')    # no leaves here: new topic, new world
def ebg(fr, mode, T=0.0): _ebg0(fr, mode, T)

def _cut(name, h):
    im = Image.open(A76 + name).convert('RGBA'); return die_cut(np.array(im.resize((int(im.width * h / im.height), h))))
CHAPPAL = _cut('chappal_cut.png', 420); PUMICE = _cut('pumice_cut2.png', 300)
SCRUB = film_card(A76 + 'scrub.jpg', (0, 0, 620, 515), 640)

def footprint(c, x, y, s, a=1.0, col='1E102C', rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.scale(.62, 1); c.arc(0, 40, 120, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx(col, a)); c.fill()
    for tx, ty, tr in ((-44, -110, 26), (-6, -128, 21), (26, -124, 18), (52, -110, 15), (72, -90, 12)):
        c.arc(tx, ty, tr, 0, 2 * math.pi); c.fill()
    c.restore()

# ---- shared drawing: rear cut-away of the heel
def heel_rear(c, cx, cy, s, bulge, walls, crack, weight, T):
    c.save(); c.translate(cx, cy); c.scale(s, s)
    sq = 1 - .18 * weight                                           # vertical squash on each step
    pw = 170 * (1 + .55 * bulge); ph = 120 * sq
    c.rectangle(-420, 250, 840, 60); c.set_source_rgba(*hx('5A2214')); c.fill()          # floor
    if walls > 0:                                                   # closed shoe heel-cup
        for sgn in (-1, 1):
            rrect(c, sgn * 250 - 35 if sgn > 0 else -285, 40 - 220 * walls, 70, 220 * walls + 210, 20); c.set_source_rgba(*hx('6B3A1E')); c.fill()
        rrect(c, -285, 215, 570, 40, 14); c.set_source_rgba(*hx('6B3A1E')); c.fill()
    else:
        rrect(c, -330, 220, 660, 34, 14); c.set_source_rgba(*hx('6CCB5F')); c.fill()      # flat chappal sole
    # skin (thick dry outer layer) + inner soft tissue
    c.save(); c.translate(0, 60)
    sk = pw + 60
    c.move_to(-sk, -260); c.curve_to(-sk, 40, -sk * .9, 190 * sq, 0, 190 * sq); c.curve_to(sk * .9, 190 * sq, sk, 40, sk, -260); c.close_path()
    c.set_source_rgba(*hx('C98A62')); c.fill()
    c.move_to(-sk + 34, -260); c.curve_to(-sk + 34, 30, -sk * .85, 160 * sq, 0, 160 * sq); c.curve_to(sk * .85, 160 * sq, sk - 34, 30, sk - 34, -260); c.close_path()
    c.set_source_rgba(*hx('F2B79A')); c.fill()
    c.save(); c.scale(1, 1); c.arc(0, 60 * sq, 1, 0, 2 * math.pi); c.restore()
    c.save(); c.translate(0, 60 + 20 * (1 - sq)); c.scale(pw / 100, ph / 100)                    # fat pad
    c.arc(0, 0, 100, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*hx('FFD25A')); c.fill()
    rng = np.random.default_rng(2)
    for i in range(14):
        bx = (rng.random() - .5) * pw * 1.5; by = 60 + (rng.random() - .5) * ph * 1.2
        c.arc(bx, by, 14, 0, 2 * math.pi); c.set_source_rgba(1, .93, .6, .9); c.fill()
    rrect(c, -110, -260, 220, 230, 60); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()   # heel bone
    if crack > 0:                                                   # splits at the stretched sides
        for sgn in (-1, 1):
            for k in range(3):
                y0 = -40 + k * 60; L = 70 * clamp(crack * 1.3 - k * .2)
                if L <= 0: continue
                c.move_to(sgn * sk, y0); c.line_to(sgn * (sk - L * .6), y0 + 14); c.line_to(sgn * (sk - L), y0 - 6)
                c.set_source_rgba(*hx('7A1E14')); c.set_line_width(9); c.stroke()
    c.restore()
    if weight > 0:                                                  # body weight arrow
        c.move_to(0, -330); c.line_to(0, -240); c.set_source_rgba(*hx(REDP)); c.set_line_width(30); c.stroke()
        c.move_to(-50, -250); c.line_to(0, -190); c.line_to(50, -250); c.close_path(); c.fill()
    c.restore()

def fuel_gauge(c, x, y, r, v):
    c.save(); c.translate(x, y)
    c.arc(0, 0, r, math.pi, 2 * math.pi); c.close_path(); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(8); c.stroke()
    for i in range(9):
        a = math.pi + i / 8 * math.pi; c.move_to(r * .78 * math.cos(a), r * .78 * math.sin(a)); c.line_to(r * .92 * math.cos(a), r * .92 * math.sin(a))
    c.set_line_width(6); c.stroke()
    c.arc(0, 0, r * .85, math.pi, math.pi * 1.2); c.set_source_rgba(*hx(REDP)); c.set_line_width(18); c.stroke()
    a = math.pi + v * math.pi; c.move_to(0, 0); c.line_to(r * .8 * math.cos(a), r * .8 * math.sin(a)); c.set_source_rgba(*hx(REDP)); c.set_line_width(10); c.stroke()
    c.arc(0, 0, 16, 0, 2 * math.pi); c.set_source_rgba(*hx(INKP)); c.fill(); c.restore()

def foot_side(c, x, y, s, lift, T):
    """flat cartoon side-view foot in a chappal"""
    c.save(); c.translate(x, y - 60 * lift); c.rotate(-.15 * lift); c.scale(s, s)
    c.move_to(-160, -40); c.curve_to(-180, 40, -150, 70, -80, 70); c.line_to(170, 70); c.curve_to(230, 70, 240, 30, 200, 10)
    c.curve_to(120, -10, 40, -40, -10, -140); c.line_to(-90, -150); c.curve_to(-120, -100, -150, -80, -160, -40); c.close_path()
    c.set_source_rgba(*hx('E9A57F')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
    rrect(c, -190, 70, 450, 24, 10); c.set_source_rgba(*hx('6CCB5F')); c.fill()
    c.move_to(140, 20); c.curve_to(110, 40, 60, 50, 30, 70); c.set_source_rgba(*hx('2F9E58')); c.set_line_width(12); c.stroke()
    c.restore()

# ---------------- scenes
def sc_h1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 1.6 if thumb else t
    ebg(fr, 'black', T)
    rub = 14 * math.sin(T * 14) * (1 - clamp((t - 2.2) / .3))
    _put0(fr, SCRUB, CX + rub, 1080, back(clamp(tt / .3)) * 1.05, 1.0, -3)
    def dr(c):
        sparks(c, 200, 800, tt - .3)
        for i in range(5):                                         # rough scratch marks = "खुरदरी"
            if tt > 1.4 + i * .08:
                x = 640 + i * 26; c.move_to(x, 1160); c.line_to(x + 16, 1220); c.set_source_rgba(*hx(REDP)); c.set_line_width(6); c.stroke()
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('एड़ी फटी?', 3)], 380, tt + 1.0, 136)
    title_line(fr, [('चप्पल देखो', 0)], 575, tt + .7, 118)

def sc_a1(fr, T, t, l):
    a = T
    ebg(fr, 'black', T)
    zoom = 1.0 if a < 5.2 else math.exp(lerp(0, math.log(1.45), ease(clamp((a - 5.2) / .9))))
    def dr(c):
        step = (a * 1.6) % 1; lift = math.sin(step * math.pi) if a < 5.2 else 0
        fx = lerp(-200, CX, clamp((a - 2.7) / 1.6))
        c.save(); c.translate(CX, 1150); c.scale(zoom, zoom); c.translate(-CX + (CX - fx) * 0, -1150)
        foot_side(c, fx, 1150, 1.5, lift, T)
        if lift < .08 and a < 5.2:
            for k in range(6): c.arc(fx - 260 + k * 30, 1290 - (k % 2) * 12, 14, 0, 2 * math.pi)
            c.set_source_rgba(1, .85, .7, .5); c.fill()
        if a > 6.0:                                                # dry flakes drift off the heel
            rng = np.random.default_rng(5)
            for i in range(18):
                u = (a - 6.0) * .6 + rng.random(); u %= 1
                c.rectangle(fx - 250 + rng.random() * 100, 1180 + u * 240, 10, 6); c.set_source_rgba(1, .95, .85, 1 - u); c.fill()
        c.restore()
        if a > 7.9: fuel_gauge(c, CX, 1060, 190 * back(clamp((a - 7.9) / .3)), lerp(.6, 0.0, ease(clamp((a - 8.5) / .9))))
    overlay(fr, cairo_layer(dr))
    if 3.2 < a < 6.2:
        k = back(clamp((a - 3.25) / .3)) * (1 - clamp((a - 5.9) / .3))
        _put0(fr, circle_photo('chapped.jpg', .5, .5, .16, 210, 9), 250, 800, k, 1.0, -6)
        _put0(fr, card_line_img((('पिछली बार: होंठ', 0),), 40, 'cream', 0), 250, 950, k, 1.0, -4)
    if a > 5.1: title_line(fr, [('आज: ', 0), ('एड़ियाँ', 1)], 380, a - 5.1, 124)
    if a > 9.0: title_line(fr, [('तेल ग्रंथि: खाली', 3)], 575, a - 9.0, 110)
    if a > 8.1: _put0(fr, htext('तेल', 46, INKP, ANEK), CX, 1130, back(clamp((a - 8.1) / .3)), 1.0, 0)

@functools.lru_cache(maxsize=1)
def wanted_poster():
    w, h = 760, 980
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((18, 22, w + 18, h + 22), fill=(40, 12, 6, 120))
    rng = np.random.default_rng(1); pts = [(rng.random() * 8, 0)]
    d.rectangle((0, 0, w, h), fill=(236, 214, 170, 255))
    a = np.array(im).astype(np.float32); n = rng.normal(0, 1, (h + 30, w + 30)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), 6) * 9; a[..., :3] = np.clip(a[..., :3] - n[..., None] * (a[..., 3:] > 0), 0, 255)
    yy, xx = np.mgrid[0:h + 30, 0:w + 30]; v = np.clip(np.hypot((xx - w / 2) / w, (yy - h / 2) / h) * 1.6 - .5, 0, 1)
    a[..., :3] = a[..., :3] * (1 - .35 * v[..., None]); im = Image.fromarray(a.astype(np.uint8)); d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(ANEK, 150, layout_engine=ImageFont.Layout.RAQM); f2 = ImageFont.truetype(ANEK, 54, layout_engine=ImageFont.Layout.RAQM)
    for txt, f, y in (('गुनहगार', f1, 20), ('जुर्म  एड़ियाँ फाड़ना', f2, 840)):
        tw = f.getlength(txt); d.text(((w - tw) / 2, y), txt, font=f, fill=(70, 24, 12, 255))
    d.rectangle((90, 230, w - 90, 820), outline=(70, 24, 12, 255), width=6)
    return np.array(im)
def sc_h3(fr, T, t, l):
    ebg(fr, 'black', T)
    k = ease(clamp(t / .35)); y = lerp(-700, 1030, k) + 10 * math.sin(T * 3) * (1 - k)
    _put0(fr, wanted_poster(), CX, y, .95, 1.0, -4 + 4 * (1 - k))
    def pin(c):
        if k >= 1: c.arc(CX - 20, y - 470, 18, 0, 2 * math.pi); c.set_source_rgba(*hx(REDP)); c.fill()
    overlay(fr, cairo_layer(pin))
    if t > 3.5: _put0(fr, CHAPPAL, CX, 1050, back(clamp((t - 3.5) / .25)) * .95, 1.0, 8)
    if t > 3.9: stamp(fr, 'पकड़ा गया', CX + 150, 1250, t - 3.9, REDP, -14)

def sc_a2(fr, T, t, l):
    a = T
    ebg(fr, 'cream' if a < 20.7 else 'black', T)
    stepping = a > 17.2
    ph = (a * 1.25) % 1; wgt = (math.sin(ph * math.pi) ** 2) if stepping else 0.0
    walls = clamp((a - 20.7) / .35) * (1 - clamp((a - 23.4) / .35))
    open_ = clamp((a - 23.5) / .3)
    bulge = wgt * open_ + .25 * clamp((a - 28.0) / 1.0)
    crack = clamp((a - 29.0) / 2.6)
    def dr(c):
        k = back(clamp((a - 15.1) / .4))
        heel_rear(c, CX, 1040, 1.1 * k, bulge, walls, crack, wgt, T)
        if open_ > 0 and wgt > .3:
            for sgn in (-1, 1):
                x = CX + sgn * (330 + 60 * wgt); c.move_to(x - sgn * 60, 1080); c.line_to(x + sgn * 30, 1080)
                c.set_source_rgba(*hx(REDP)); c.set_line_width(14); c.stroke()
                c.move_to(x + sgn * 60, 1080); c.line_to(x + sgn * 20, 1050); c.line_to(x + sgn * 20, 1110); c.close_path(); c.fill()
        if 20.8 < a < 23.4: badge(c, 880, 760, 44, True, back(clamp((a - 21.0) / .25)))
        if a > 31.5: badge(c, 880, 760, 44, False, back(clamp((a - 31.5) / .25)))
    overlay(fr, cairo_layer(dr))
    if a > 16.4: _put0(fr, card_line_img((('चर्बी की गद्दी', 0),), 44, 'cream', 0), CX, 1120, back(clamp((a - 16.4) / .3)) * .9 * (1 - clamp((a - 20.4) / .3)), 1.0, 0)
    if a < 20.7: title_line(fr, [('हर कदम पर ', 0), ('वज़न', 1)], 380, a - 17.2, 118)
    elif a < 23.5: title_line(fr, [('बंद जूता: ', 0), ('गद्दी टिकी', 1)], 380, a - 20.7, 112)
    elif a < 28.0: title_line(fr, [('खुली चप्पल: ', 0), ('फैलाव', 3)], 380, a - 23.5, 112)
    else:
        title_line(fr, [('सूखी त्वचा खिंची', 0)], 380, a - 28.0, 112)
        if a > 31.4: title_line(fr, [('और फट गई', 3)], 560, a - 31.4, 120)

def sc_h7(fr, T, t, l):
    ebg(fr, 'cream', T)
    def dr(c):
        k1 = back(clamp(t / .3))
        if k1 > 0:
            for i in range(4):
                y = 820 + i * 60; ph = (T * .8 + i * .2) % 1; x0 = 120 + ph * 300
                c.move_to(x0, y); c.curve_to(x0 + 60, y - 20, x0 + 120, y + 20, x0 + 180, y); c.set_source_rgba(.4, .7, .95, .9 * k1); c.set_line_width(8); c.stroke()
            snowflake(c, 250, 760, 30 * k1, 1.0, T)
        k2 = back(clamp((t - 1.5) / .3))
        if k2 > 0:
            c.arc(790, 880, 120 * k2, 0, 2 * math.pi); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(8); c.stroke()
            for ang, L in ((T * 6, 90), (T * .5, 60)):
                c.move_to(790, 880); c.line_to(790 + L * k2 * math.cos(ang), 880 + L * k2 * math.sin(ang)); c.set_line_width(10); c.stroke()
        k3 = clamp((t - 2.6) / .3)
        if k3 > 0:
            boost = 1 + 1.3 * ease(clamp((t - 3.3) / .4))
            flame(c, CX, 1330, 90 * k3 * boost, T)
            if 2.8 < t < 3.4:
                y = lerp(1000, 1260, (t - 2.8) / .6); drop_col = (1, .8, .25)
                c.arc(CX, y, 22, 0, 2 * math.pi); c.set_source_rgb(*drop_col); c.fill()
    overlay(fr, cairo_layer(dr))
    if t > .2: _put0(fr, card_line_img((('सूखी हवा', 0),), 44, 'cream', 0), 280, 1040, back(clamp((t - .2) / .3)), 1.0, -3)
    if t > 1.6: _put0(fr, card_line_img((('घंटों खड़े', 0),), 44, 'cream', 0), 790, 1060, back(clamp((t - 1.6) / .3)), 1.0, 3)
    title_line(fr, [('और ऊपर से', 0)], 380, t, 116)
    if t > 2.7: title_line(fr, [('आग में घी', 3)], 560, t - 2.7, 124)

def bucket(c, x, y, s, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-90, -60); c.line_to(90, -60); c.line_to(70, 80); c.line_to(-70, 80); c.close_path(); c.set_source_rgba(*hx('3A7BD5')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
    c.restore(); steam(c, x, y - 80 * s, T, 3, .5, .9)
def cream_tube(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(-.3)
    rrect(c, -50, -110, 100, 200, 20); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
    rrect(c, -22, 90, 44, 40, 6); c.set_source_rgba(*hx('3A7BD5')); c.fill(); rrect(c, -50, -40, 100, 40, 0); c.set_source_rgba(*hx('3A7BD5')); c.fill()
    c.restore()
def socks(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-30, -100); c.line_to(30, -100); c.line_to(30, 30); c.curve_to(30, 70, 90, 60, 100, 80); c.curve_to(110, 110, 60, 120, 0, 110); c.curve_to(-40, 105, -30, 60, -30, 40); c.close_path()
    c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
    for k in range(3): c.move_to(-30, -90 + k * 14); c.line_to(30, -90 + k * 14)
    c.set_source_rgba(*hx(REDP)); c.set_line_width(4); c.stroke(); c.restore()
STEPS = [(39.0, 'कुछ मिनट गुनगुना पानी', 260, 820), (41.5, 'प्यूमिक से हल्का', 800, 900), (43.7, 'यूरिया क्रीम', 260, 1060), (45.5, 'पेट्रोलियम जेली', 800, 1140), (46.8, 'सूती मोज़े, सो जाओ', 300, 1300)]
def sc_h8(fr, T, t, l):
    a = T
    ebg(fr, 'black', T)
    jl = jelly_cut()
    def dr(c):
        for i in range(len(STEPS) - 1):                                   # board-game path
            if a > STEPS[i + 1][0] - .3:
                (_, _, x0, y0), (_, _, x1, y1) = STEPS[i][:4], STEPS[i + 1][:4]
                c.move_to(x0, y0); c.line_to(x1, y1); c.set_dash([18, 14]); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(8); c.stroke(); c.set_dash([])
        for i, (ts, txt, x, y) in enumerate(STEPS):
            k = back(clamp((a - ts) / .3))
            if k <= 0: continue
            c.arc(x, y, 95 * k, 0, 2 * math.pi); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
            c.arc(x - 70 * k, y - 70 * k, 26 * k, 0, 2 * math.pi); c.set_source_rgba(*hx(MUST)); c.fill()
            if i == 0: bucket(c, x, y + 10, .75 * k, T)
            elif i == 2: cream_tube(c, x, y, .6 * k)
            elif i == 4: socks(c, x, y, .7 * k)
        cur = [s_ for s_ in STEPS if a > s_[0]]                           # footprint token hops along
        if cur:
            _, _, x, y = cur[-1][:4]; hop = clamp((a - cur[-1][0]) / .35)
            footprint(c, x + 60, y - 90 - 60 * math.sin(math.pi * hop), .28, 1.0, REDP, .3)
        c.arc(900, 700, 50, 0, 2 * math.pi); c.set_source_rgba(1, .9, .5, 1); c.fill(); c.arc(925, 685, 44, 0, 2 * math.pi); c.set_source_rgba(*hx('7A2A18')); c.fill()
    overlay(fr, cairo_layer(dr))
    for i, (ts, txt, x, y) in enumerate(STEPS):
        k = back(clamp((a - ts) / .3))
        if k <= 0: continue
        if i == 1: _put0(fr, PUMICE, x + 10 * math.sin(T * 12), y, .45 * k, 1.0, 20)
        if i == 3: _put0(fr, jl, x, y, .42 * k, 1.0, 0)
        _put0(fr, card_line_img(((txt, 0),), 42, 'cream', 0), x + (230 if x < CX else -230), y, k, 1.0, 0)
        _put0(fr, htext(str(i + 1), 40, INKP, ANEK), x - 70, y - 72, k, 1.0, 0)
    title_line(fr, [('रात का ', 0), ('इलाज', 3)], 380, a - 37.6, 124)

def sc_h10(fr, T, t, l):
    ebg(fr, 'cream', T)
    heal = clamp((t - .4) / 2.0)
    def dr(c):
        heel_rear(c, 300, 1110, .5, .25 * (1 - heal), 0, 1 - heal, 0, T)
        c.save(); c.translate(780, 1080)
        rrect(c, -230, -200, 460, 400, 26); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
        rrect(c, -230, -200, 460, 70, 26); c.set_source_rgba(*hx(REDP)); c.fill()
        n = int(heal * 14)
        for d in range(14):
            r_, q = divmod(d, 7); x = -180 + q * 60; y = -80 + r_ * 110
            c.rectangle(x - 24, y - 24, 48, 48); c.set_source_rgba(*hx(INKP, .12)); c.fill()
            if d < n: tick_ring(c, x, y, 22, 1.0, True)
        c.restore()
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('करीब ', 0), ('2 हफ़्ते', 3)], 380, t, 124)

def sc_h11(fr, T, t, l):
    ebg(fr, 'black', T)
    k = back(clamp(t / .4))
    def phone(c):
        c.save(); c.translate(CX, 1040); c.rotate(-.05); c.scale(k * .92, k * .92)
        rrect(c, -230, -330, 460, 660, 56); c.set_source_rgba(*hx('111111')); c.fill()
        rrect(c, -210, -300, 420, 600, 40); c.set_source_rgba(*hx('3A1A10')); c.fill(); c.restore()
        if k >= 1:
            tap = clamp((t - 1.0) / .25); s = 1 + .12 * math.sin(math.pi * tap)
            rrect(c, CX - 150 * s, 1160 - 44 * s, 300 * s, 88 * s, 44 * s); c.set_source_rgba(*hx(GRN)); c.fill()
            if t > 1.3: a_ = clamp((t - 1.3) / .2); rrect(c, CX - 60, 760, 380, 90, 30); c.set_source_rgba(1, 1, 1, a_); c.fill()
    overlay(fr, cairo_layer(phone))
    _put0(fr, CHAPPAL, CX, 970, .42 * k, 1.0, 10)
    if k >= 1: _put0(fr, htext('भेजो', 52, 'FFFFFF', ANEK), CX, 1160, 1.0, 1.0, 0)
    if t > 1.3: _put0(fr, htext('भाई चप्पल बदल', 42, INKP, ANEK), CX + 130, 805, 1.0, clamp((t - 1.3) / .2), 0)
    title_line(fr, [('उसे भेजो', 0)], 380, t, 120)
    if t > 1.8: title_line(fr, [('जो दिन भर चप्पल पहनता', 0)], 552, t - 1.8, 96)

def red_hand(c, x, y, s, T, swell):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -110, -40, 220, 200, 60); c.set_source_rgba(*hx('E9A57F')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(6); c.stroke()
    for i, (fx, L) in enumerate(((-80, 150), (-27, 175), (27, 170), (80, 140))):
        w = 46 * (1 + .35 * swell); rrect(c, fx - w / 2, -40 - L, w, L + 20, w / 2)
        c.set_source_rgba(lerp(.91, .9, swell), lerp(.65, .3, swell), lerp(.5, .32, swell), 1); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
    c.restore()
def sc_h12(fr, T, t, l):
    ebg(fr, 'black', T)
    sw = clamp((t - .9) / 1.2)
    def dr(c):
        red_hand(c, CX, 1220, 1.4 * back(clamp(t / .35)), T, sw)
        for i in range(10):
            ph = (T * .15 + i * .1) % 1; snowflake(c, 140 + (i * 87) % 800, 700 + ph * 700, 14, .9, T + i)
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('सर्दी में उँगलियाँ', 0)], 380, t, 116)
    title_line(fr, [('लाल और सूजी?', 3)], 560, t - .9, 120)
    if t > 2.6: tape(fr, 'पार्ट 3 जल्द', 820, 1420 - 120, t - 2.6, 'FFE45C', 50, HI_B, 8)

def sc_he(fr, T, t, l):
    ebg(fr, 'end', T)
    title_line(fr, [('रोज़ के सच के लिए', 0)], 380, t + .3, 104)
    title_line(fr, [('FreshNestHub', 2)], 560, t + .1, 120)
    def dr(c): logo(c, CX, 1030, 170 * back(clamp(t / .4)))
    overlay(fr, cairo_layer(dr))
    _put0(fr, htext('फ़ॉलो करो', 84, PUR, ANEK), CX, 1290, back(clamp((t - .6) / .3)), 1.0, 0)

SCENES = dict(h1=sc_h1, a1=sc_a1, h3=sc_h3, a2=sc_a2, h7=sc_h7, h8=sc_h8, h10=sc_h10, h11=sc_h11, h12=sc_h12, e1=sc_he)
SHAKES = [(5.2, 10), (9.3, 14), (13.94, 30), (19.44, 14), (24.4, 16), (31.58, 30), (35.9, 22), (54.6, 12)]
FOCUS = dict(h3=1030, h7=1000, h8=1000, h10=1080, h11=1040, h12=1200)

TR = .18
def transition(fr, T):                                                    # footprint stamp
    for i, x in enumerate(TL[1:]):
        u = T - x['start']
        if -TR < u < TR:
            p = (u + TR) / (2 * TR); s = lerp(3.2, 2.4, p); a_ = math.sin(p * math.pi)
            def dr(c): footprint(c, CX + (60 if i % 2 else -60), 1000, s, .96 * a_, '2A1208', (-.25 if i % 2 else .25))
            overlay(fr, cairo_layer(dr)); return
