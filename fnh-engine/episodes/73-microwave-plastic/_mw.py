
# ================= 73 microwave plastic: PURPLE theme (interesting/science), yellow = the point, red = danger, green = safe
THEME = dict(bg1='C9A7FF', bg2='5B2DB8', hl_main='FFE45C', hl_text_main='1A1A1A', hl_black='FFE45C', hl_text_black='1A1A1A',
             accent='FFE45C', end1='EFE4FF', end2='B892F5', end_text='3A1677', end_stroke=False)
TOTAL = 40.6; BRAND0 = 999.0
LID = '7B4DE0'; BOX = 'F3F6FA'

# ---------- drawn props
def tiffin(c, x, y, s=1.0, rot=0.0, a=1.0, frost=0.0):
    """generic translucent plastic food box with a clip lid (no brand)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -150, -40, 300, 150, 26); c.set_source_rgba(*hx(BOX, .92 * a)); c.fill_preserve()
    c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(7); c.stroke()
    rrect(c, -132, -10, 264, 105, 18); c.set_source_rgba(*hx('F4B25A', .85 * a)); c.fill()       # food (dal/rice colour)
    for i in range(6):
        c.arc(-100 + i * 40, 20 + (i % 2) * 22, 9, 0, 2 * math.pi); c.set_source_rgba(*hx('FFFFFF', .6 * a)); c.fill()
    rrect(c, -150, -40, 300, 150, 26); c.set_source_rgba(1, 1, 1, .22 * a); c.fill()            # plastic sheen
    c.move_to(-120, 0); c.line_to(-120, 80); c.set_source_rgba(1, 1, 1, .7 * a); c.set_line_width(8); c.stroke()
    rrect(c, -164, -78, 328, 46, 18); c.set_source_rgba(*hx(LID, a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(7); c.stroke()
    for sx in (-110, 110):                                                                      # clips
        rrect(c, sx - 24, -50, 48, 52, 10); c.set_source_rgba(*hx('5A33B0', a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(5); c.stroke()
    if frost > 0:
        rrect(c, -164, -78, 328, 188, 26); c.set_source_rgba(*hx('DFF3FF', .45 * frost)); c.fill()
    c.restore()

def microwave(c, x, y, s, T, on=True, inner=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -330 + 14, -200 + 18, 660, 400, 40); c.set_source_rgba(0, 0, 0, .28); c.fill()
    rrect(c, -330, -200, 660, 400, 40); c.set_source_rgba(*hx('EDEAF4')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(9); c.stroke()
    # window
    rrect(c, -290, -160, 420, 320, 26); c.set_source_rgba(*hx('20123A')); c.fill()
    if on:
        g = cairo.RadialGradient(-80, 20, 20, -80, 20, 260); g.add_color_stop_rgba(0, 1, .86, .45, .85); g.add_color_stop_rgba(1, 1, .6, .2, .05)
        rrect(c, -290, -160, 420, 320, 26); c.set_source(g); c.fill()
    c.save(); rrect(c, -290, -160, 420, 320, 26); c.clip()
    c.save(); c.translate(-80, 110); c.scale(1, .22); c.arc(0, 0, 170, 0, 2 * math.pi); c.restore()   # turning plate
    c.set_source_rgba(1, 1, 1, .25); c.fill()
    if inner: inner(c)
    for i in range(0, 420, 22):                                                                 # mesh dots
        for j in range(0, 320, 22): c.rectangle(-290 + i, -160 + j, 3, 3)
    c.set_source_rgba(0, 0, 0, .18); c.fill()
    c.restore()
    rrect(c, -290, -160, 420, 320, 26); c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke()
    # control panel
    rrect(c, 160, -160, 140, 90, 14); c.set_source_rgba(*hx('10223A')); c.fill()
    for k in range(3):
        c.arc(230, -10 + k * 62, 22, 0, 2 * math.pi); c.set_source_rgba(*hx('C9C4D6')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(5); c.stroke()
    c.restore()

def timer_txt(fr, x, y, secs, col=None, size=58):
    m, sec = divmod(max(0, int(math.ceil(secs))), 60)
    put_rgba(fr, htext(f'{m}:{sec:02d}', size, col or '7DFF9B', HI_B), x, y, 1.0, 1.0, 0)

def particles(c, x, y, T, t, n=60, spread=380, col=RED, seed=1, a=1.0):
    rng = np.random.default_rng(seed)
    for k in range(n):
        ang = rng.random() * 2 * math.pi; sp = .4 + rng.random(); d0 = rng.random()
        ph = (d0 + t * .35 * sp) % 1.0
        r = spread * ph; xx = x + math.cos(ang) * r; yy = y + math.sin(ang) * r * .8 - 40 * ph
        sz = 3 + rng.random() * 7
        c.arc(xx, yy, sz, 0, 2 * math.pi); c.set_source_rgba(*hx(col if k % 3 else 'FFFFFF', a * (1 - ph * .7))); c.fill()

def cell(c, x, y, r, dead=0.0, T=0.0):
    w = 1 - dead
    c.save(); c.translate(x, y); c.scale(1 + .04 * math.sin(T * 3 + x), 1)
    c.arc(0, 0, r, 0, 2 * math.pi)
    c.set_source_rgba(lerp(.55, 1.0, w) * 1, lerp(.55, .62, w), lerp(.55, .72, w), 1); c.fill_preserve()
    c.set_source_rgba(*hx('1C1614')); c.set_line_width(4); c.stroke()
    c.arc(r * .1, -r * .05, r * .38, 0, 2 * math.pi); c.set_source_rgba(lerp(.35, .78, w), lerp(.35, .28, w), lerp(.35, .55, w), 1); c.fill()
    if dead > .5:
        for s in (-1, 1):
            c.move_to(-r * .5, -r * .5 * s); c.line_to(r * .5, r * .5 * s)
        c.set_source_rgba(*hx('1C1614', .8)); c.set_line_width(6); c.stroke()
    c.restore()

def bowl(c, x, y, s, kind, T):
    c.save(); c.translate(x, y); c.scale(s, s)
    if kind == 'glass':
        c.move_to(-150, -60); c.curve_to(-150, 90, 150, 90, 150, -60); c.close_path()
        c.set_source_rgba(.75, .92, 1, .55); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke()
        c.move_to(-120, -30); c.curve_to(-115, 30, -80, 55, -50, 62); c.set_source_rgba(1, 1, 1, .8); c.set_line_width(9); c.stroke()
    else:
        g = cairo.LinearGradient(-150, 0, 150, 0)
        for p_, v in ((0, .55), (.3, .95), (.55, .62), (.8, .9), (1, .5)): g.add_color_stop_rgb(p_, v, v, v * 1.03)
        c.move_to(-150, -60); c.curve_to(-150, 90, 150, 90, 150, -60); c.close_path()
        c.set_source(g); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke()
    c.save(); c.scale(1, .2); c.arc(0, -300, 150, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hx('F4B25A')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(5); c.stroke()
    c.restore()
    steam(c, x, y - 90 * s, T, 3, .45, .8)

def stamp(fr, txt, x, y, t, col=GRN, rot=-12):
    if t <= 0: return
    k = clamp(t / .18); sc = lerp(2.2, 1.0, ease(k))
    f = ImageFont.truetype(HI_B, 78, layout_engine=ImageFont.Layout.RAQM); tw = int(f.getlength(txt))
    im = Image.new('RGBA', (tw + 90, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, tw + 84, 144), 22, outline=rgb(col) + (255,), width=10)
    d.text((45, 18), txt, font=f, fill=rgb(col) + (255,))
    put_rgba(fr, np.array(im), x, y, sc, k, rot)

@functools.lru_cache(maxsize=8)
def mw_card(hl):
    w, h = 820, 520
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 22, w + 18, h + 22), 18, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, h), 18, fill=(255, 253, 246, 255), outline=(28, 22, 20, 255), width=5)
    fb = ImageFont.truetype(HI_B, 46, layout_engine=ImageFont.Layout.RAQM); fm = ImageFont.truetype(HI_M, 36, layout_engine=ImageFont.Layout.RAQM)
    d.text((40, 30), 'नेब्रास्का यूनिवर्सिटी, अमेरिका', font=fb, fill=(28, 22, 20, 255))
    d.text((40, 96), 'लैब टेस्ट · 2023', font=fm, fill=(120, 110, 100, 255))
    d.line((40, 156, w - 40, 156), fill=(28, 22, 20, 255), width=3)
    rows = [('बच्चों के खाने के डिब्बे', 'प्लास्टिक'), ('माइक्रोवेव में गर्म', '3 मिनट'), ('निकले प्लास्टिक कण', 'अरबों')]
    for i, (a, b) in enumerate(rows):
        yy = 190 + i * 100
        if hl > i:
            d.rectangle((30, yy - 6, w - 30, yy + 66), fill=(255, 228, 92, 255))
        d.text((40, yy), a, font=fm, fill=(28, 22, 20, 255))
        bw = fb.getlength(b); d.text((w - 40 - bw, yy - 8), b, font=fb, fill=(230, 57, 70, 255) if i == 2 else (28, 22, 20, 255))
    return np.array(im)

# ---------------- scenes
def box_in_mw(T, t, burst=0.0):
    def inner(c):
        sw = 22 * math.sin(T * 2.2)
        tiffin(c, -80 + sw, 40, .72, .0)
        if burst > 0: particles(c, -80 + sw, 30, T, t, int(40 * burst), 200 * burst + 40, YL, 3, .9)
    return inner

def sc_h1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 3.0 if thumb else t
    ebg(fr, 'cream', T)
    title_line(fr, [('प्लास्टिक डिब्बा', 0)], 380, tt + 1.0, 116)
    title_line(fr, [('माइक्रोवेव में?', 3)], 560, tt + 1.0, 128)
    overlay(fr, cairo_layer(lambda c: microwave(c, CX, 1090, 1.15, T, True, box_in_mw(T, tt, clamp((tt - 1.6) / 1.2)))))
    timer_txt(fr, CX + 1.15 * 230, 1090 - 1.15 * 115, 180 - tt * 30 if not thumb else 180)
    note(fr, 'टिफ़िन वाला', 230, 830, 1.0 if thumb else t - 1.0, 50, YL, -6, 400, 1090)

def sc_h2(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('3 मिनट में', 0)], 400, t, 124)
    title_line(fr, [('अरबों कण', 3)], 580, t - 1.95, 136)
    p = back(clamp(t / .35)); b = clamp((t - 1.9) / 1.5)
    def dr(c):
        if b > 0:
            g = cairo.RadialGradient(CX, 1060, 30, CX, 1060, 520); g.add_color_stop_rgba(0, .9, .22, .27, .45 * b); g.add_color_stop_rgba(1, .9, .22, .27, 0)
            c.arc(CX, 1060, 520, 0, 2 * math.pi); c.set_source(g); c.fill()
            particles(c, CX, 1040, T, t, int(160 * b), 470, RED, 7)
        tiffin(c, CX, 1060, 1.5 * p, -.05 + .03 * math.sin(T * 9) * b)
    overlay(fr, cairo_layer(dr))
    timer_txt(fr, CX, 820, 180 - clamp(t / 3.0) * 180, YL, 90)
    note(fr, 'आँख से दिखते नहीं', CX, 1340, t - 2.9, 50, YL, -3)

def sc_p1(fr, T, t, l):
    ebg(fr, 'cream', T)
    title_line(fr, [('2023, ', 1), ('अमेरिका', 0)], 380, t, 120)
    if t > 3.3: title_line(fr, [('बच्चों के ', 0), ('खाने के डिब्बे', 1)], 560, t - 3.3, 100)
    k = back(clamp((t - .2) / .4)); hl = 1 if t > 3.6 else 0
    if t > 5.5: hl = 2
    put_rgba(fr, mw_card(hl), CX, 990, .82 * k, 1.0, -3)
    source_tag(fr, 'Environmental Science & Technology, 2023', 100, 1238, t - 1.2)

def sc_p2(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('हर ', 0), ('1 सेंटीमीटर', 1), (' से', 0)], 400, t, 112)
    if t > 2.8: title_line(fr, [('200 करोड़+ कण', 3)], 580, t - 2.8, 124)
    S = 420; x0, y0 = CX - S / 2, 820; p = ease(clamp((t - .3) / .5))
    def dr(c):
        c.rectangle(x0, y0, S * p, S * p); c.set_source_rgba(*hx('F3F6FA', .14)); c.fill_preserve(); c.set_source_rgba(*hx(YL)); c.set_line_width(6); c.stroke()
        if p >= 1:
            n = int(clamp((t - 1.0) / 2.4) ** 1.6 * 900); rng = np.random.default_rng(11)
            pts = rng.random((900, 3))
            for i in range(n):
                px, py, s_ = pts[i]
                c.arc(x0 + 8 + px * (S - 16), y0 + 8 + py * (S - 16), 2 + s_ * 4, 0, 2 * math.pi)
                c.set_source_rgba(*hx(RED if i % 4 else 'FFFFFF', .9)); c.fill()
            for i in range(11):                                       # rulers
                c.move_to(x0 + i * S / 10, y0 - 14 - (10 if i % 5 == 0 else 0)); c.line_to(x0 + i * S / 10, y0 - 4)
                c.move_to(x0 - 14 - (10 if i % 5 == 0 else 0), y0 + i * S / 10); c.line_to(x0 - 4, y0 + i * S / 10)
            c.set_source_rgba(1, 1, 1, .9); c.set_line_width(3); c.stroke()
    overlay(fr, cairo_layer(dr))
    if p >= 1:
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), CX, y0 - 58, 1.0, 1.0, 0)
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), x0 - 80, y0 + S / 2, 1.0, 1.0, 90)
    note(fr, 'बस इतनी सी जगह', 760, 1330, t - 1.4, 48, YL, -4, 720, 1200)

def sc_a1(fr, T, t, l):
    ebg(fr, 'cream', T)
    title_line(fr, [('और ये प्लास्टिक', 0)], 380, t, 116)
    title_line(fr, [('सरकार से मंज़ूर', 1)], 560, t - .6, 116)
    overlay(fr, cairo_layer(lambda c: tiffin(c, CX, 1080, 1.6, -.04)))
    stamp(fr, 'मंज़ूर', CX + 40, 1060, t - 1.35, GRN, -14)
    note(fr, 'फिर भी?', 820, 1330, t - 1.9, 60, YL, 6)

def sc_k1(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('लैब: ', 0), ('किडनी', 1), (' कोशिकाएँ', 0)], 400, t, 108)
    if t > 5.6: title_line(fr, [('75% मर गईं', 3)], 580, t - 5.6, 132)
    cols, rows, r = 8, 4, 50; gx0, gy0 = CX - (cols - 1) * 115 / 2, 820
    dead_n = int(clamp((t - 5.7) / .9) * 24)
    order = np.random.default_rng(2).permutation(32)
    def dr(c):
        for i in range(32):
            rr_, q = divmod(i, cols); x = gx0 + q * 115; y = gy0 + rr_ * 112
            k = back(clamp((t - .1 - i * .015) / .3))
            if k <= 0: continue
            dead = 1.0 if (list(order).index(i) < dead_n) else 0.0
            c.save(); c.translate(x, y); c.scale(k, k); cell(c, 0, 0, r, dead, T); c.restore()
        if 1.0 < t < 5.8:                                             # particles raining onto cells
            rng = np.random.default_rng(5)
            for j in range(90):
                ph = (rng.random() + (t - 1.0) * .5) % 1
                c.arc(gx0 - 60 + rng.random() * 920, 720 + ph * 480, 3 + rng.random() * 4, 0, 2 * math.pi)
                c.set_source_rgba(*hx(YL, .85 * (1 - ph * .5))); c.fill()
    overlay(fr, cairo_layer(dr))
    note(fr, 'सबसे ज़्यादा मात्रा पर', 330, 1330, t - 3.0, 44, YL, -4)
    note(fr, '2 दिन में', 820, 1330, t - 4.7, 50, YL, 5)

def sc_w1(fr, T, t, l):
    ebg(fr, 'cream', T)
    title_line(fr, [('खाना गर्म करो', 0)], 380, t, 112)
    title_line(fr, [('काँच', 1), (' या ', 0), ('स्टील', 1), (' में', 0)], 560, t - .7, 116)
    k1 = back(clamp((t - .7) / .35)); k2 = back(clamp((t - 1.4) / .35))
    def dr(c):
        if k1 > 0: bowl(c, 300, 1080, 1.05 * k1, 'glass', T)
        if k2 > 0: bowl(c, 780, 1080, 1.05 * k2, 'steel', T)
        tick_ring(c, 300, 1250, 46, back(clamp((t - 1.0) / .3)), True)
        tick_ring(c, 780, 1250, 46, back(clamp((t - 1.7) / .3)), True)
    overlay(fr, cairo_layer(dr))

def sc_w2(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('प्लास्टिक डिब्बा?', 0)], 400, t, 120)
    title_line(fr, [('सिर्फ़ ठंडा खाना', 1)], 580, t - 1.0, 120)
    fz = clamp((t - 1.1) / .8)
    def dr(c):
        tiffin(c, CX, 1080, 1.45, 0, 1.0, fz)
        for i in range(14):
            ph = (T * .12 + i * .071) % 1
            snowflake(c, 140 + (i * 61) % 820, 760 + ph * 620, 10 + (i % 3) * 5, .8 * fz, T * .5 + i)
    overlay(fr, cairo_layer(dr))
    note(fr, 'गर्म करने के लिए नहीं', CX, 1340, t - 1.9, 48, YL, -3)

def sc_e1(fr, T, t, l):
    ebg(fr, 'end', T)
    title_line(fr, [('ऐसे ही रोज़ के सच', 0)], 380, t + .1, 104)
    title_line(fr, [('FreshNestHub', 2)], 560, t - 1.4, 120)
    k = back(clamp((t - .4) / .4))
    def dr(c): logo(c, CX, 1030, 170 * k)
    overlay(fr, cairo_layer(dr))
    if t > 2.6: put_rgba(fr, htext('फ़ॉलो करो', 84, THEME['end_text'], HI_B), CX, 1290, back(clamp((t - 2.6) / .3)), 1.0, 0)

SCENES = dict(h1=sc_h1, h2=sc_h2, p1=sc_p1, p2=sc_p2, a1=sc_a1, k1=sc_k1, w1=sc_w1, w2=sc_w2, e1=sc_e1)
