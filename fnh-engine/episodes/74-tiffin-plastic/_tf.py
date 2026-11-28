
# ================= 74 tiffin v4 script: participation hook, villain particles, cause chain, bite punchline, share, part-2 tease
TOTAL = 51.0; BRAND0 = 999.0

def kan(c, x, y, r, T, col='E63946', seed=0, look=(0, 0), q=0.0, a=1.0):
    """cute-evil plastic particle character"""
    bob = 4 * math.sin(T * 6 + seed)
    y = y + bob
    for s in (-1, 1):                                                 # feet
        c.move_to(x + s * r * .35, y + r * .8); c.line_to(x + s * r * .45, y + r * 1.15)
        c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(max(2, r * .12)); c.stroke()
    g = cairo.RadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r)
    cc = hx(col); g.add_color_stop_rgba(0, min(1, cc[0] + .35), min(1, cc[1] + .35), min(1, cc[2] + .35), a); g.add_color_stop_rgba(1, cc[0] * .75, cc[1] * .75, cc[2] * .75, a)
    for i in range(17):                                               # jagged plastic-shard body
        an = i / 16 * 2 * math.pi; rr = r * (1 + .1 * math.sin(an * 5 + seed))
        (c.move_to if i == 0 else c.line_to)(x + rr * math.cos(an), y + rr * math.sin(an))
    c.close_path(); c.set_source(g); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(max(2, r * .1)); c.stroke()
    for s in (-1, 1):
        ex, ey = x + s * r * .33, y - r * .12
        c.arc(ex, ey, r * .25, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a); c.fill()
        c.arc(ex + look[0] * r * .1, ey + look[1] * r * .1, r * .12, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.fill()
        c.move_to(ex - s * r * .25, ey - r * .38); c.line_to(ex + s * r * .2, ey - r * .25)      # evil brows
        c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(max(2, r * .1)); c.stroke()
    c.arc(x, y + r * .3, r * .3, .15 * math.pi, .85 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(max(2, r * .09)); c.stroke()
    if q > 0:
        put = None
        c.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(r * 1.1)
        c.move_to(x + r * .5, y - r * 1.1); c.set_source_rgba(*hx('FFE45C', q * a)); c.show_text('?')

def magnifier(c, x, y, R, a=1.0):
    c.save(); c.translate(x, y); c.rotate(.8)
    rrect(c, R - 10, -26, R * .9, 52, 22); c.set_source_rgba(*hx('2A1A4A', a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(6); c.stroke()
    c.restore()
    c.arc(x, y, R + 14, 0, 2 * math.pi); c.set_source_rgba(*hx('C9C4D6', a)); c.set_line_width(26); c.stroke()
    c.arc(x, y, R + 28, 0, 2 * math.pi); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(6); c.stroke()

@functools.lru_cache(maxsize=1)
def macro_wall():
    """zoomed real plastic wall + fine scratches + cloudy film"""
    b = BOXR; h, w = b.shape[:2]; crop = b[int(h * .45):int(h * .85), int(w * .25):int(w * .7), :3].astype(np.float32)
    D = 680; im = cv2.resize(crop, (D, D), interpolation=cv2.INTER_CUBIC)
    rng = np.random.default_rng(4); sc = np.zeros((D, D), np.float32)
    for _ in range(140):
        x0, y0 = rng.random(2) * D; ang = rng.normal(.3, .5); L = 30 + rng.random() * 160
        cv2.line(sc, (int(x0), int(y0)), (int(x0 + L * math.cos(ang)), int(y0 + L * math.sin(ang))), float(.35 + .5 * rng.random()), 1, cv2.LINE_AA)
    fog = cv2.GaussianBlur(rng.random((D, D)).astype(np.float32), (0, 0), 22); fog = (fog - fog.min()) / (fog.max() - fog.min())
    return im, sc, fog

def sc_s1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 1.0 if thumb else t
    fr[:] = photo_bg()
    up = ease(clamp(tt / .45)); dive = ease(clamp((tt - 2.1) / 1.2))
    s = lerp(1.25, 1.45, up) * lerp(1, 2.0, dive)
    put_rgba(fr, BOXR, CX + 30 * dive, lerp(1250, 1060, up) + 120 * dive, s, 1.0, lerp(-18, -4, up) + 2 * math.sin(T * 2))
    if dive > .3:
        def mg(c): magnifier(c, CX, 1060, 300 * back(clamp((tt - 2.4) / .4)), clamp((tt - 2.4) / .2))
        overlay(fr, cairo_layer(mg))
    title_line(fr, [('अपना टिफ़िन', 0)], 380, tt + 1.0, 112)
    title_line(fr, [('अंदर से देखो', 3)], 552, tt + 1.0, 124)
    note(fr, 'अभी उठाओ', 820, 1290, 1.0 if thumb else tt - .5, 56, YL, 5)

def sc_s2(fr, T, t, l):
    ebg(fr, 'black', T)
    im, sc, fog = macro_wall(); D = im.shape[0]
    z = 1 + .12 * t / l['dur']; M = np.float32([[z, 0, (1 - z) * D / 2], [0, z, (1 - z) * D / 2]])
    k = clamp((t - .3) / 1.2)                                         # scratches + film fade in as the words come
    img = im * (1 - .45 * fog[..., None] * k) + 255 * .45 * fog[..., None] * k
    img = img + sc[..., None] * 255 * k
    img = cv2.warpAffine(np.clip(img, 0, 255), M, (D, D), borderMode=cv2.BORDER_REFLECT)
    R = 300; yy, xx = np.mgrid[0:D, 0:D]; rr = np.sqrt((xx - D / 2) ** 2 + (yy - D / 2) ** 2) / (D / 2)
    al = np.clip((1 - rr) * 40, 0, 1)
    rgba = np.dstack([img, al * 255]).astype(np.uint8)
    put_rgba(fr, rgba, CX, 1060, 2 * R / D, 1.0, 0)
    overlay(fr, cairo_layer(lambda c: magnifier(c, CX, 1060, R)))
    title_line(fr, [('धुंधली, ', 0), ('खुरदरी', 1), (' परत?', 0)], 400, t, 108)
    if t > 2.3: title_line(fr, [('गंदगी नहीं है', 3)], 580, t - 2.3, 124)
    note(fr, 'ये परत', 250, 1390, t - 1.0, 54, YL, -6, 420, 1150)

def sc_s3(fr, T, t, l):
    ebg(fr, 'black', T)
    put_rgba(fr, BOXR, CX, 880, 1.0, 1.0, -2)
    put_rgba(fr, GLASSC, CX, 1285, .9, 1.0, 0)
    jump = 3.9
    def dr(c):
        rng = np.random.default_rng(3)
        for i in range(7):
            x0 = CX - 210 + i * 70 + rng.random() * 20; y0 = 1010 + rng.random() * 20
            born = .3 + i * .18; u = t - born
            if u < 0: continue
            pop = back(clamp(u / .3))
            if t < jump:
                look = (math.sin(T * 3 + i), 0) if t > 2.2 else (0, 1)
                kan(c, x0 + 6 * math.sin(T * 4 + i), y0 + 30 * pop, 38 * pop, T, RED if i % 3 else '9B5DE5', i, look, clamp((t - 2.3) / .3) * (i % 2))
            else:
                v = t - jump - i * .04
                if v < 0: kan(c, x0, y0 + 30, 38, T, RED if i % 3 else '9B5DE5', i); continue
                fx = lerp(x0, CX - 120 + i * 40, clamp(v / .5)); fy = y0 + 30 - 160 * math.sin(math.pi * clamp(v / .5)) + 250 * clamp(v / .5) ** 2
                if v < .55: kan(c, fx, fy, 38, T, RED if i % 3 else '9B5DE5', i, (0, 1))
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('प्लास्टिक ', 0), ('घिस रहा है', 1)], 400, t, 112)
    if t > 3.85: title_line(fr, [('तुम्हारे खाने में', 3)], 580, t - 3.85, 120)

def sc_s4(fr, T, t, l):
    fr[:] = photo_bg()
    scan = clamp((t - 3.3) / .9); hot = clamp((t - 3.2) / 1.0)
    pl = plate_frame(T, scan, hot)
    card = np.zeros((pl.shape[0] + 20, MWW + 20, 4), np.uint8); card[..., :3] = 255; card[..., 3] = 255; card[10:-10, 10:-10, :3] = pl
    k = back(clamp(t / .45))
    put_rgba(fr, card, CX, 1068, lerp(.6, .9, k), clamp(t / .2), lerp(6, -1.5, k))
    if t > 1.2: timer_txt(fr, 905, 790, 180 - (t - 1.2) * 20, '7DFF9B', 64)
    title_line(fr, [('सबसे ज़्यादा कब?', 0)], 380, t, 112)
    if t > 3.3: title_line(fr, [('माइक्रोवेव में', 3)], 552, t - 3.3, 124)

def sc_s5(fr, T, t, l):
    fr[:] = photo_bg()
    title_line(fr, [('अमेरिका, ', 0), ('2023', 1)], 380, t, 120)
    if t > 2.8: title_line(fr, [('सिर्फ़ 3 मिनट', 3)], 560, t - 2.8, 120)
    k = ease(clamp((t - .15) / .55)); hl = 1 if t > 1.2 else 0
    if t > 2.9: hl = 2
    put_rgba(fr, mw_card(hl), CX + 700 * (1 - k), 990 + 60 * (1 - k), .82 * lerp(.7, 1, k), 1.0, lerp(18, -3, k) + .8 * math.sin(T * 1.3))
    source_tag(fr, 'Environmental Science & Technology, 2023', 100, 1238, t - 1.0)

def sc_s6(fr, T, t, l):
    ebg(fr, 'black', T)
    _p2body(fr, T, t)
    title_line(fr, [('हर ', 0), ('1 सेंटीमीटर', 1), (' से', 0)], 400, t, 112)
    if t > 1.4: title_line(fr, [('200 करोड़+ कण', 3)], 580, t - 1.4, 124, sel=True)

def chain_card(c, x, y, w, h, k):
    rrect(c, x - w / 2 + 10, y - h / 2 + 12, w, h, 26); c.set_source_rgba(0, 0, 0, .35 * k); c.fill()
    rrect(c, x - w / 2, y - h / 2, w, h, 26); c.set_source_rgba(1, 1, 1, k); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', k)); c.set_line_width(6); c.stroke()
def sc_s7(fr, T, t, l):
    ebg(fr, 'cream', T)
    steps = [(0.1, 'गर्मी'), (1.05, 'परतें टूटीं'), (2.55, 'कण खाने में')]
    ys = [830, 1030, 1230]
    def dr(c):
        for i, (ts, _) in enumerate(steps):
            k = back(clamp((t - ts) / .35))
            if k <= 0: continue
            c.save(); c.translate(CX, ys[i]); c.scale(k, k); c.translate(-CX, -ys[i])
            chain_card(c, CX, ys[i], 760, 150, 1.0)
            ix = CX - 290
            if i == 0: flame(c, ix, ys[i] + 30, 52, T)
            elif i == 1:
                for j in range(3):
                    rrect(c, ix - 60, ys[i] - 45 + j * 32, 120, 24, 8); c.set_source_rgba(*hx(['9B5DE5', 'B892F5', 'D9C6FF'][j])); c.fill()
                zap(c, ix - 10, ys[i] - 55, ix + 15, ys[i] + 55, T, 6, RED)
            else:
                kan(c, ix, ys[i] - 5, 34, T, RED, 2, (0, 1))
            c.restore()
            if i < 2 and t > steps[i + 1][0] - .2:
                a = clamp((t - steps[i + 1][0] + .2) / .2)
                c.move_to(CX, ys[i] + 80); c.line_to(CX, ys[i + 1] - 80); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(8); c.stroke()
                c.move_to(CX - 18, ys[i + 1] - 98); c.line_to(CX, ys[i + 1] - 78); c.line_to(CX + 18, ys[i + 1] - 98); c.stroke()
    overlay(fr, cairo_layer(dr))
    for i, (ts, txt) in enumerate(steps):
        k = clamp((t - ts - .1) / .25)
        if k > 0: put_rgba(fr, htext(txt, 64, 'E63946' if i == 2 else '1C1614', HI_B), CX + 70, ys[i], 1.0, k, 0)
    title_line(fr, [('ऐसे ', 0), ('निकलते', 1), (' हैं', 0)], 380, t, 116)

def sc_s8(fr, T, t, l):
    ebg(fr, 'black', T)
    bite = clamp((t - 3.0) / .08)
    b = BOXR.copy()
    if bite > 0:
        h, w = b.shape[:2]; m = np.zeros((h, w), np.uint8)
        for j in range(6): cv2.circle(m, (int(w * .82 + 60 * math.cos(j)), int(h * .22 + 50 * math.sin(j * 1.3))), int(80 - j * 6), 255, -1)
        b[..., 3] = np.where(m > 0, 0, b[..., 3])
    put_rgba(fr, b, CX, 1080, 1.3, 1.0, -4 + 3 * math.sin(T * 1.3))
    if bite > 0:
        def cr(c):
            rng = np.random.default_rng(8); u = t - 3.0
            for i in range(26):
                ang = -math.pi / 2 + (rng.random() - .5) * 2.4; sp = 300 + 500 * rng.random()
                x = CX + 220 + math.cos(ang) * sp * u; y = 900 + math.sin(ang) * sp * u + 900 * u * u
                if y < H: rrect(c, x, y, 10 + 12 * rng.random(), 8 + 10 * rng.random(), 3); c.set_source_rgba(.85, .9, 1, .9); c.fill()
        overlay(fr, cairo_layer(cr))
    title_line(fr, [('टिफ़िन गर्म करके', 0)], 400, t, 112)
    if t > 2.95: title_line(fr, [('डिब्बा भी खा रहे हो', 3)], 580, t - 2.95, 112, sel=True)

def sc_s10(fr, T, t, l):
    fr[:] = photo_bg()
    k = back(clamp(t / .4))
    def phone(c):
        c.save(); c.translate(CX, 1040); c.rotate(-.05); c.scale(k * .92, k * .92)
        rrect(c, -230, -330, 460, 660, 56); c.set_source_rgba(*hx('111111')); c.fill()
        rrect(c, -210, -300, 420, 600, 40); c.set_source_rgba(*hx('2B1B55')); c.fill()
        c.restore()
    overlay(fr, cairo_layer(phone))
    put_rgba(fr, BOXR, CX, 960, .5 * k, 1.0, -6)
    tap = clamp((t - 1.0) / .25)
    def btn(c):
        if k < 1: return
        s = 1 + .12 * math.sin(math.pi * tap)
        rrect(c, CX - 150 * s, 1160 - 44 * s, 300 * s, 88 * s, 44 * s); c.set_source_rgba(*hx(GRN)); c.fill()
        if 1.2 < t < 2.6:                                             # chat bubble lands
            a = clamp((t - 1.2) / .2)
            rrect(c, CX - 40, 770, 330, 90, 30); c.set_source_rgba(1, 1, 1, a); c.fill()
    overlay(fr, cairo_layer(btn))
    if k >= 1: put_rgba(fr, htext('भेजो', 52, 'FFFFFF', HI_B), CX, 1160, 1.0, 1.0, 0)
    if 1.2 < t < 2.6: put_rgba(fr, htext('भाई, ये देख!', 44, '1C1614', HI_B), CX + 125, 815, 1.0, clamp((t - 1.2) / .2), 0)
    title_line(fr, [('उस दोस्त को ', 0), ('भेजो', 1)], 380, t, 116)
    if t > 1.6: title_line(fr, [('जो रोज़ ऐसा करता है', 0)], 552, t - 1.6, 96)
    note(fr, 'टैग करो', 860, 1300, t - 2.2, 56, YL, 6)

def recycle(c, x, y, R, T, a=1.0):
    if R < 4: return
    for i in range(3):
        an = i * 2 * math.pi / 3 - math.pi / 2 + T * .4
        x1, y1 = x + R * math.cos(an), y + R * math.sin(an); an2 = an + 2 * math.pi / 3 * .72
        x2, y2 = x + R * math.cos(an2), y + R * math.sin(an2)
        c.move_to(x1, y1); c.line_to(x2, y2); c.set_source_rgba(1, 1, 1, a); c.set_line_width(22); c.stroke()
        ux, uy = (x2 - x1), (y2 - y1); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        c.move_to(x2 + ux * 30, y2 + uy * 30); c.line_to(x2 - uy * 28, y2 + ux * 28); c.line_to(x2 + uy * 28, y2 - ux * 28); c.close_path(); c.fill()
def sc_s11(fr, T, t, l):
    ebg(fr, 'black', T)
    k = back(clamp(t / .4))
    overlay(fr, cairo_layer(lambda c: recycle(c, CX, 1010, 190 * k, T)))
    num = str(1 + int(T * 8) % 7) if t < 3.6 else '?'
    put_rgba(fr, htext(num, 150, 'FFE45C', HI_B), CX, 1030, k, 1.0, 0)
    if t > 3.6:
        for i in range(7):
            kk = back(clamp((t - 3.6 - i * .07) / .25))
            def chip(c, i=i, kk=kk):
                x = 165 + i * 125
                c.arc(x, 1330, 46 * kk, 0, 2 * math.pi); c.set_source_rgba(*hx('3A3A3A')); c.fill_preserve(); c.set_source_rgba(*hx(YL)); c.set_line_width(3); c.stroke()
            overlay(fr, cairo_layer(chip))
            if kk > .5: put_rgba(fr, htext(str(i + 1), 50, 'FFFFFF', HI_B), 165 + i * 125, 1330, kk, 1.0, 0)
    title_line(fr, [('कौन सा प्लास्टिक', 0)], 380, t, 112)
    title_line(fr, [('सबसे ख़तरनाक?', 3)], 552, t - .9, 124)
    if t > 4.85: tape(fr, 'पार्ट 2 जल्द', 780, 790, t - 4.85, 'FFE45C', 50, HI_B, 8)

def sc_e1(fr, T, t, l):
    ebg(fr, 'end', T)
    title_line(fr, [('पार्ट 2 के लिए', 0)], 380, t + .3, 104)
    title_line(fr, [('FreshNestHub', 2)], 560, t + .1, 120)
    def dr(c): logo(c, CX, 1030, 170 * back(clamp(t / .4)))
    overlay(fr, cairo_layer(dr))
    put_rgba(fr, htext('फ़ॉलो करो', 84, THEME['end_text'], HI_B), CX, 1290, back(clamp((t - .6) / .3)), 1.0, 0)

SCENES = dict(s1=sc_s1, s2=sc_s2, s3=sc_s3, s4=sc_s4, s5=sc_s5, s6=sc_s6, s7=sc_s7, s8=sc_s8, s9=sc_w1, s10=sc_s10, s11=sc_s11, e1=sc_e1)
SHAKES = [(1.2, 10), (6.08, 18), (11.38, 24), (16.06, 14), (20.5, 12), (23.44, 28), (29.02, 14), (33.92, 32), (47.3, 20)]
FOCUS = dict(s2=1060, s3=1000, s4=1080, s5=990, s6=1030, s7=1030, s8=1080, s9=1080, s10=1090, s11=1010)
