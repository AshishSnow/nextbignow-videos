
# ================= 72 gas geyser: WINTER DANGER theme (icy blue + red danger, yellow = the point)
# petrol-pump design kept; new: 3D extruded headlines, keyword block with a hard shadow, Kalam handwritten notes,
# danger tape, evidence card with a highlighter + SOURCE tag, newspaper clipping, colour = meaning.
THEME = dict(bg1='9FDCFF', bg2='1C5FB4', hl_main='FFE45C', hl_text_main='1A1A1A', hl_black='FFE45C', hl_text_black='1A1A1A',
             accent='FFE45C', end1='D8F1FF', end2='7CC4F2', end_text='0B3B6E', end_stroke=False)
YL = 'FFE45C'; RED = 'E63946'; GRN = '2E9E4F'; ICE = 'DFF3FF'; NAVY = '0B2A52'
TOTAL = 41.0; BRAND0 = 999.0
KALAM = '/home/claude/studio/fonts/doc/d_kalam.ttf'

# ---------- type: 3D extruded two-tier headline
@functools.lru_cache(maxsize=128)
def tline3(segs, size, mode):
    f = ImageFont.truetype(HI_B, size, layout_engine=ImageFont.Layout.RAQM)
    h = int(size * 1.55); widths = [f.getlength(s) for s, _ in segs]; w = int(sum(widths)) + 60
    return f, w, h, widths

def title_line(fr, segs, y, t, size=112, mode=None, x=LX, wipe=True):
    if t <= 0: return
    mode = mode or MODE[0]; segs = tuple(segs)
    f, w, h, widths = tline3(segs, size, mode)
    k = ease(clamp(t / .28)); dy = 30 * (1 - k)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ext = max(5, size // 16)                               # extrusion depth
    xx = 8; ty = int(size * .1)
    for (s, hi), sw in zip(segs, widths):                  # keyword blocks with a hard offset shadow
        if hi:
            p = ease(clamp((t - .12) / .3)) if wipe else 1
            x0, y0, x1, y1 = xx - 12, int(size * .2), xx + sw + 8, int(size * 1.32)
            if p > 0:
                xe = x0 + (x1 - x0) * p
                d.rectangle((x0 + ext + 2, y0 + ext + 2, xe + ext + 2, y1 + ext + 2), fill=rgb('0E1A2B') + (255,))
                blk = RED if hi == 3 else (INK if hi == 2 else THEME['hl_main'])
                d.rectangle((x0, y0, xe, y1), fill=rgb(blk) + (255,))
        xx += sw
    xx = 8
    for (s, hi), sw in zip(segs, widths):
        if hi:
            col = 'FFFFFF' if hi == 3 else (YEL if hi == 2 else THEME['hl_text_main'])
            d.text((xx, ty), s, font=f, fill=rgb(col) + (255,))
        else:
            fgc = 'FFFFFF' if mode != 'end' else THEME['end_text']
            if mode != 'end':
                for i in range(ext, 0, -1):                 # stacked extrusion = 3D depth
                    d.text((xx + i, ty + i), s, font=f, fill=rgb('0E1A2B') + (255,), stroke_width=max(4, size // 14), stroke_fill=rgb('0E1A2B') + (255,))
            d.text((xx, ty), s, font=f, fill=rgb(fgc) + (255,), stroke_width=max(4, size // 14) if mode != 'end' else 0, stroke_fill=rgb('0E1A2B') + (255,))
        xx += sw
    put_rgba(fr, np.array(im), x + w / 2, y + dy + h / 2, 1.0, k, 0)

@functools.lru_cache(maxsize=64)
def note_img(txt, size, col):
    f = ImageFont.truetype(KALAM, size, layout_engine=ImageFont.Layout.RAQM); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] + 20, bb[3] + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((6, 8), txt, font=f, fill=(0, 0, 0, 150)); d.text((2, 4), txt, font=f, fill=rgb(col) + (255,))
    return np.array(im)
def note(fr, txt, x, y, t, size=54, col=YL, rot=-4, ax=None, ay=None):
    """handwritten yellow note, optional hand-drawn arrow to (ax, ay)"""
    if t <= 0: return
    k = back(clamp(t / .3)); put_rgba(fr, note_img(txt, size, col), x, y, k, 1.0, rot)
    if ax is not None:
        p = ease(clamp((t - .15) / .4))
        def dr(c):
            sx, sy = x, y + size * .7; mx, my = (sx + ax) / 2 + 60, (sy + ay) / 2
            n = 30; pts = []
            for i in range(int(n * p) + 1):
                u = i / n; pts.append(((1 - u) ** 2 * sx + 2 * (1 - u) * u * mx + u * u * ax, (1 - u) ** 2 * sy + 2 * (1 - u) * u * my + u * u * ay))
            if len(pts) > 1:
                c.move_to(*pts[0])
                for q in pts[1:]: c.line_to(*q)
                c.set_source_rgba(*hx(col)); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
            if p >= 1:
                ang = math.atan2(ay - my, ax - mx)
                for s in (-.5, .5):
                    c.move_to(ax, ay); c.line_to(ax - 30 * math.cos(ang + s), ay - 30 * math.sin(ang + s))
                c.set_source_rgba(*hx(col)); c.set_line_width(7); c.stroke()
        overlay(fr, cairo_layer(dr))

def danger_tape(fr, T, t, y=1610, txt='खतरा   ·   खतरा   ·   खतरा   ·   खतरा   ·   खतरा', rot=-6):
    if t <= 0: return
    k = ease(clamp(t / .35))
    def dr(c):
        c.save(); c.translate(CX, y); c.rotate(math.radians(rot)); x0 = -900 + 1800 * (1 - k) * -1
        c.rectangle(-900, -48, 1800 * k, 96); c.clip()
        c.rectangle(-900, -48, 1800, 96); c.set_source_rgba(*hx(YL)); c.fill()
        off = (T * 90) % 80
        for i in range(-14, 26):
            xx = -900 + i * 80 + off; c.move_to(xx, -48); c.line_to(xx + 40, -48); c.line_to(xx - 10, 48); c.line_to(xx - 50, 48); c.close_path()
        c.set_source_rgba(*hx('1A1A1A')); c.fill(); c.restore()
    overlay(fr, cairo_layer(dr))
    if k > .6: put_rgba(fr, htext('घर का ये ख़तरा दिखता नहीं', 44, 'FFFFFF', HI_B), CX, y - 2, 1.0, 0, rot)

# ---------- drawn props
def geyser(c, x, y, s, T, on=True, glow=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    # pipes: gas (yellow) from the side, hot (red) + cold (blue) below
    for (px, col) in ((-50, '3E8FE0'), (50, RED)):
        c.move_to(px, 170); c.line_to(px, 300); c.set_source_rgba(*hx('1C1614')); c.set_line_width(26); c.stroke()
        c.move_to(px, 170); c.line_to(px, 300); c.set_source_rgba(*hx(col)); c.set_line_width(16); c.stroke()
    c.move_to(-130, 120); c.line_to(-260, 120); c.line_to(-260, 330); c.set_source_rgba(*hx('1C1614')); c.set_line_width(22); c.stroke()
    c.move_to(-130, 120); c.line_to(-260, 120); c.line_to(-260, 330); c.set_source_rgba(*hx(YL)); c.set_line_width(12); c.stroke()
    # body
    rrect(c, -130, -190, 260, 370, 34); c.set_source_rgba(*hx('F4F7FA')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke()
    rrect(c, -130, -190, 40, 370, 20); c.set_source_rgba(0, 0, 0, .06); c.fill()
    for i in range(5):                                          # top vents
        rrect(c, -80 + i * 34, -165, 18, 46, 8); c.set_source_rgba(*hx('9AA7B4')); c.fill()
    # flame window
    rrect(c, -78, -60, 156, 120, 22); c.set_source_rgba(*hx('10223A')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(6); c.stroke()
    if on:
        for k in range(5):
            fx = -52 + k * 26; hgt = 34 + 10 * math.sin(T * 14 + k * 1.7)
            c.move_to(fx - 10, 38); c.curve_to(fx - 12, 20, fx - 2, 38 - hgt * .6, fx, 38 - hgt); c.curve_to(fx + 2, 38 - hgt * .6, fx + 12, 20, fx + 10, 38); c.close_path()
            c.set_source_rgba(*hx('4FB6FF')); c.fill()
            c.move_to(fx - 5, 38); c.curve_to(fx - 5, 28, fx, 38 - hgt * .4, fx, 38 - hgt * .55); c.curve_to(fx, 38 - hgt * .4, fx + 5, 28, fx + 5, 38); c.close_path()
            c.set_source_rgba(*hx('DFF6FF')); c.fill()
    for i, kx in enumerate((-45, 45)):                          # knobs
        c.arc(kx, 115, 24, 0, 2 * math.pi); c.set_source_rgba(*hx('D5DDE5')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(5); c.stroke()
        c.move_to(kx, 115); c.line_to(kx + 16 * math.cos(-1 + i), 115 + 16 * math.sin(-1 + i)); c.set_line_width(5); c.stroke()
    c.restore()

def steam(c, x, y, T, n=4, a=.55, s=1.0):
    for k in range(n):
        ph = (T * .45 + k / n) % 1.0
        xx = x + (k - n / 2) * 34 * s + 26 * math.sin(T * 2 + k); yy = y - ph * 260 * s
        c.arc(xx, yy, (22 + 40 * ph) * s, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, a * (1 - ph)); c.fill()

def door(c, x, y, s=1.0, closed=1.0, lock=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -110, -230, 220, 460, 10); c.set_source_rgba(*hx('3A2618')); c.fill()
    w = 200 * closed
    rrect(c, -100, -220, max(8, w), 440, 8); c.set_source_rgba(*hx('B07945')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(6); c.stroke()
    if closed > .9:
        for yy in (-170, 20): rrect(c, -70, yy, 140, 150, 8); c.set_source_rgba(0, 0, 0, .12); c.fill()
        c.arc(70, 10, 13, 0, 2 * math.pi); c.set_source_rgba(*hx('FFD34D')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(4); c.stroke()
        if lock:
            rrect(c, 48, 40, 44, 34, 6); c.set_source_rgba(*hx('C9CED6')); c.fill_preserve(); c.stroke()
    c.restore()

def window(c, x, y, s=1.0, open_=0.0, T=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -120, -100, 240, 200, 12); c.set_source_rgba(*hx('CFEFFF')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke()
    if open_ > 0:   # fresh air swirls coming in
        for k in range(3):
            ph = (T * .7 + k / 3) % 1
            c.move_to(-60 + k * 50, -40 + k * 30); c.curve_to(-20 + k * 50, -80 + k * 30, 40 + k * 50 - 200 * ph, 0, -40 + k * 50 - 260 * ph, -20 + k * 30)
            c.set_source_rgba(*hx('FFFFFF', .9 * open_ * (1 - ph))); c.set_line_width(7); c.stroke()
    lw = 116 * (1 - open_)
    for sgn in (-1, 1):                                          # shutters slide open
        c.rectangle(sgn * 2 if sgn > 0 else -2 - lw, -96, lw, 192); c.set_source_rgba(*hx('7BA7C9')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(5); c.stroke()
    c.restore()

def molecule(c, x, y, kind='CO', r=20, a=1.0):
    if kind == 'O2':
        for dx in (-r * .7, r * .7):
            c.arc(x + dx, y, r, 0, 2 * math.pi); c.set_source_rgba(*hx('5AB8FF', a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(3); c.stroke()
    else:
        c.arc(x - r * .75, y, r * 1.05, 0, 2 * math.pi); c.set_source_rgba(*hx('3B3B3B', a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(3); c.stroke()
        c.arc(x + r * .75, y, r, 0, 2 * math.pi); c.set_source_rgba(*hx(RED, a)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614', a)); c.set_line_width(3); c.stroke()

def fog(c, x0, x1, y0, y1, T, amt, col=(0.55, 0.58, 0.62)):
    rng = np.random.default_rng(5)
    for k in range(28):
        bx = x0 + rng.random() * (x1 - x0); by = y1 - rng.random() * (y1 - y0) * amt
        r = 70 + 60 * rng.random(); bx += 30 * math.sin(T * .8 + k)
        c.arc(bx, by, r, 0, 2 * math.pi); c.set_source_rgba(*col, .16 * amt); c.fill()

def person_icon(c, x, y, s, col):
    c.arc(x, y - 26 * s, 13 * s, 0, 2 * math.pi); c.set_source_rgba(*hx(col)); c.fill()
    rrect(c, x - 15 * s, y - 10 * s, 30 * s, 40 * s, 12 * s); c.fill()

def room_card(c, x, y, w, h, T):
    rrect(c, x, y, w, h, 34); c.set_source_rgba(*hx('E8F4FB')); c.fill()
    c.save(); rrect(c, x, y, w, h, 34); c.clip()
    for i in range(0, int(w), 70):
        c.move_to(x + i, y); c.line_to(x + i, y + h)
    for j in range(0, int(h), 70):
        c.move_to(x, y + j); c.line_to(x + w, y + j)
    c.set_source_rgba(*hx('B9D7EA')); c.set_line_width(3); c.stroke(); c.restore()
    rrect(c, x, y, w, h, 34); c.set_source_rgba(*hx('1C1614')); c.set_line_width(8); c.stroke()

@functools.lru_cache(maxsize=8)
def doc_card(hl):
    """evidence card: the study, as a clean page (no logos), hl = highlighter progress bucket"""
    w, h = 820, 520
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 22, w + 18, h + 22), 18, fill=(0, 0, 0, 90))
    d.rounded_rectangle((0, 0, w, h), 18, fill=(255, 253, 246, 255), outline=(28, 22, 20, 255), width=5)
    fb = ImageFont.truetype(HI_B, 46, layout_engine=ImageFont.Layout.RAQM); fm = ImageFont.truetype(HI_M, 36, layout_engine=ImageFont.Layout.RAQM)
    d.text((40, 30), 'सर गंगा राम अस्पताल, दिल्ली', font=fb, fill=(28, 22, 20, 255))
    d.text((40, 96), 'न्यूरोलॉजी विभाग · 2008 से 2010', font=fm, fill=(120, 110, 100, 255))
    d.line((40, 156, w - 40, 156), fill=(28, 22, 20, 255), width=3)
    rows = [('नहाते वक़्त बेहोश हुए मरीज़', '26'), ('कार्बन मोनोऑक्साइड का असर', '13'), ('दिल लगभग रुकने वाले', '4')]
    for i, (a, b) in enumerate(rows):
        yy = 190 + i * 100
        if i == 1 and hl > 0:
            d.rectangle((30, yy - 6, 30 + (w - 60) * hl / 4, yy + 66), fill=(255, 228, 92, 255))
        d.text((40, yy), a, font=fm, fill=(28, 22, 20, 255)); d.text((w - 110, yy - 8), b, font=fb, fill=(230, 57, 70, 255) if i else (28, 22, 20, 255))
    return np.array(im)
def source_tag(fr, txt, x, y, t):
    if t <= 0: return
    k = ease(clamp(t / .25)); f = ImageFont.truetype(HI_B, 30, layout_engine=ImageFont.Layout.RAQM)
    tw = int(f.getlength(txt)); im = Image.new('RGBA', (tw + 190, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 150, 63), fill=rgb(RED) + (255,)); d.text((18, 14), 'SOURCE', font=f, fill=(255, 255, 255, 255))
    d.rectangle((150, 0, tw + 190, 63), fill=(20, 20, 20, 255)); d.text((168, 14), txt, font=f, fill=(255, 255, 255, 255))
    put_rgba(fr, np.array(im), x + (tw + 190) / 2, y, 1.0, k, 0)

@functools.lru_cache(maxsize=2)
def clipping():
    w, h = 800, 560
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(4); pts = []
    for x in np.linspace(0, w, 30): pts.append((x, rng.uniform(0, 10)))
    for y in np.linspace(0, h, 14): pts.append((w - rng.uniform(0, 8), y))
    for x in np.linspace(w, 0, 30): pts.append((x, h - rng.uniform(0, 10)))
    for y in np.linspace(h, 0, 14): pts.append((rng.uniform(0, 8), y))
    sh = [(x + 16, y + 20) for x, y in pts]; d.polygon(sh, fill=(0, 0, 0, 90)); d.polygon(pts, fill=(240, 234, 218, 255))
    fh = ImageFont.truetype('/home/claude/studio/fonts/doc/nserif-700.ttf', 62, layout_engine=ImageFont.Layout.RAQM)
    fs = ImageFont.truetype(HI_M, 32, layout_engine=ImageFont.Layout.RAQM)
    d.text((40, 30), 'बेंगलुरु · जून 2023', font=fs, fill=(150, 30, 30, 255))
    d.text((40, 80), 'बाथरूम में कपल', font=fh, fill=(28, 22, 20, 255)); d.text((40, 160), 'मृत मिला', font=fh, fill=(28, 22, 20, 255))
    d.line((40, 258, w - 40, 258), fill=(28, 22, 20, 255), width=3)
    d.text((40, 278), 'पुलिस: गैस गीज़र से कार्बन मोनोऑक्साइड', font=fs, fill=(28, 22, 20, 255))
    d.text((40, 324), 'का शक, दरवाज़ा और खिड़की बंद थे', font=fs, fill=(28, 22, 20, 255))
    for i in range(4):
        y = 390 + i * 36; d.rectangle((40, y, w - 40 - (i % 2) * 140, y + 14), fill=(185, 178, 160, 255))
    return np.array(im)

# ---------------- scenes (t = time inside the scene)
def bath_scene(fr, T, t, fogamt=0.0, on=True, door_c=1.0, win_o=0.0, cx=CX, cy=1180):
    def dr(c):
        room_card(c, 110, 820, 860, 700, T)
        door(c, 830, 1200, .95, door_c)
        window(c, 300, 960, .9, win_o, T)
        geyser(c, 470, 1190, .9, T, on)
        if on: steam(c, 470, 1010, T, 4, .5)
        if fogamt > 0: fog(c, 130, 950, 840, 1500, T, fogamt)
    overlay(fr, cairo_layer(dr))

def sc_h1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 3.0 if thumb else t
    ebg(fr, 'cream', T)
    title_line(fr, [('गैस गीज़र =', 0)], 380, tt + 1.0, 116)
    title_line(fr, [('गैस चैंबर?', 3)], 560, tt + 1.0, 136)
    k = 1.0 if thumb else ease(clamp((t - 2.2) / .8))
    bath_scene(fr, T, tt, 0.0, True, k)
    def snow(c):
        for i in range(16):
            ph = (T * .12 + i * .071) % 1
            snowflake(c, 140 + (i * 61) % 820, 760 + ph * 820, 10 + (i % 3) * 5, .8, T * .5 + i)
    overlay(fr, cairo_layer(snow))
    note(fr, 'सर्दी + बंद दरवाज़ा', 700, 760, 1.0 if thumb else t - 3.2, 46, YL, -5, 830, 980)

def sc_h2(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('ये आदत', 0)], 400, t, 124)
    title_line(fr, [('जान ले सकती है', 3)], 580, t - .9, 116)
    p = back(clamp(t / .35))
    def dr(c):
        c.save(); c.translate(CX, 1040); c.scale(p, p); c.translate(-CX, -1040)
        geyser(c, CX, 1040, .75, T, True); c.restore()
        r = 270 + 26 * math.sin(T * 6)
        c.arc(CX, 1040, r, 0, 2 * math.pi); c.set_source_rgba(*hx(RED, .55)); c.set_line_width(14); c.stroke()
    overlay(fr, cairo_layer(dr))
    danger_tape(fr, T, t - .3, 1340, rot=-5)

def sc_s1(fr, T, t, l):
    ebg(fr, 'cream', T)
    if t < 3.3:
        title_line(fr, [('गीज़र जलाता है', 0)], 380, t, 112)
        title_line(fr, [('बाथरूम की हवा', 1)], 560, t - .4, 112)
    else:
        title_line(fr, [('बनती है', 0)], 380, t - 3.3, 112)
        title_line(fr, [('कार्बन मोनोऑक्साइड', 3)], 560, t - 3.3, 96)
    fogamt = clamp((t - 2.4) / 2.5)
    bath_scene(fr, T, t, fogamt, True, 1.0)
    def mols(c):
        for k in range(10):                     # O2 drawn into the geyser, CO pushed out
            ph = (T * .5 + k / 10) % 1
            if t < 3.3:
                x = lerp(160 + (k * 83) % 780, 470, ph); y = lerp(860 + (k * 47) % 560, 1190, ph)
                molecule(c, x, y, 'O2', 16, 1 - ph * .6)
            else:
                ang = k * .63; x = 470 + math.cos(ang) * 340 * ph; y = 1100 + math.sin(ang) * 220 * ph - 80 * ph
                molecule(c, x, y, 'CO', 18, clamp(1.2 - ph))
    overlay(fr, cairo_layer(mols))
    if t > 3.6:
        note(fr, 'न रंग', 260, 1350, t - 3.6, 56, YL, -4)
        note(fr, 'न बदबू', 760, 1350, t - 4.3, 56, YL, 4)
        overlay(fr, cairo_layer(lambda c: (tick_ring(c, 400, 1340, 34, back(clamp((t - 3.8) / .3)), False), tick_ring(c, 930, 1340, 34, back(clamp((t - 4.5) / .3)), False))))

def sc_p1(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('26 लोग ', 1), ('बेहोश', 0)], 380, t, 120)
    if t > 4.6: title_line(fr, [('आधे में: ', 0), ('यही गैस', 3)], 560, t - 4.6, 112)
    k = back(clamp((t - .2) / .4)); hl = int(clamp((t - 4.9) / .8) * 4)
    put_rgba(fr, doc_card(hl), CX, 990, .82 * k, 1.0, -3)
    if t > 1.5:
        def grid(c):
            n = int(clamp((t - 1.5) / 1.4) * 26)
            for i in range(26):
                r, q = divmod(i, 13); x = 156 + q * 64; y = 1330 + r * 66
                col = (RED if (t > 4.9 and i < 13) else 'FFFFFF') if i < n else '444444'
                person_icon(c, x, y, 1.0, col)
        overlay(fr, cairo_layer(grid))
    source_tag(fr, 'Annals of Indian Academy of Neurology, 2013', 100, 1238, t - 1.0)

def sc_p2(fr, T, t, l):
    ebg(fr, 'cream', T)
    if t < 4.9:
        title_line(fr, [('2023, ', 1), ('बेंगलुरु', 0)], 380, t, 120)
        k = back(clamp((t - .3) / .4)); put_rgba(fr, clipping(), CX, 1080, .98 * k, 1.0, 2.5)
        def tapes(c):
            for (x, y, r) in ((180, 800, -.5), (900, 800, .5)):
                c.save(); c.translate(x, y); c.rotate(r); c.rectangle(-70, -20, 140, 40); c.set_source_rgba(1, 1, 1, .75 * k); c.fill(); c.restore()
        overlay(fr, cairo_layer(tapes))
        note(fr, 'नहाने गए… बाहर नहीं आए', CX, 1500, t - 2.6, 50, YL, -3)
    else:
        u = t - 4.9
        title_line(fr, [('दरवाज़ा + खिड़की', 0)], 380, u, 108)
        title_line(fr, [('दोनों बंद', 3)], 560, u - .5, 130)
        bath_scene(fr, T, t, .7, True, 1.0, 0.0)
        def xs(c):
            tick_ring(c, 830, 900, 56, back(clamp((u - .6) / .3)), False)
            tick_ring(c, 300, 820, 56, back(clamp((u - .9) / .3)), False)
        overlay(fr, cairo_layer(xs))

def sc_w1(fr, T, t, l):
    ebg(fr, 'cream', T)
    if t < 3.3:
        title_line(fr, [('गीज़र ', 0), ('बाहर', 1), (' लगवाओ', 0)], 380, t, 104)
        title_line(fr, [('या खिड़की ', 0), ('खुली', 1)], 560, t - 2.1, 110)
        win = ease(clamp((t - 2.2) / .8))
        bath_scene(fr, T, t, .6 * (1 - win), True, 1.0, win)
        note(fr, 'हवा आने दो', 330, 1560, t - 2.6, 50, YL, -4, 300, 1060)
    else:
        u = t - 3.3
        title_line(fr, [('नहाने से ', 0), ('पहले', 1)], 380, u, 112)
        steps = [('1', 'पानी गर्म करो', 0.0), ('2', 'गीज़र बंद करो', .8), ('3', 'फिर नहाओ', 1.7)]
        for i, (n, txt, d0) in enumerate(steps):
            tt = u - d0
            if tt <= 0: continue
            k = back(clamp(tt / .3)); y = 760 + i * 230
            def chip(c, y=y, k=k, i=i, tt=tt):
                rrect(c, 150, y, 780, 170, 40); c.set_source_rgba(*hx('0E1A2B', .35)); c.fill()
                rrect(c, 140, y - 10, 780, 170, 40); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke()
                c.arc(230, y + 75, 52, 0, 2 * math.pi); c.set_source_rgba(*hx(YL)); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(6); c.stroke()
                if tt > .5: tick_ring(c, 840, y + 75, 44, back(clamp((tt - .5) / .3)), True)
            overlay(fr, cairo_layer(chip))
            put_rgba(fr, htext(n, 70, '1A1A1A', HI_B), 230, 760 + i * 230 + 72, k, 1.0, 0)
            put_rgba(fr, htext(txt, 64, '1A1A1A', HI_B), 520, 760 + i * 230 + 70, k, 1.0, 0)

def sc_w2(fr, T, t, l):
    ebg(fr, 'black', T)
    title_line(fr, [('चक्कर आए?', 0)], 380, t, 124)
    title_line(fr, [('तुरंत बाहर', 3)], 560, t - .9, 130)
    def dr(c):
        c.arc(400, 1150, 120, 0, 2 * math.pi); c.set_source_rgba(*hx('F8B996')); c.fill_preserve(); c.set_source_rgba(*hx('1C1614')); c.set_line_width(7); c.stroke()
        for k in range(5):                      # dizzy stars
            ang = T * 3 + k * 1.256
            sparkle(c, 400 + 170 * math.cos(ang), 1010 + 50 * math.sin(ang), 22, YL, 1.0)
        for sx in (360, 440):                   # spiral eyes
            for i in range(14):
                a0 = i * .6 + T * 4; r = 3 + i * 1.6
                c.line_to(sx + r * math.cos(a0), 1130 + r * math.sin(a0))
            c.set_source_rgba(*hx('1C1614')); c.set_line_width(4); c.stroke(); c.new_path()
        p = ease(clamp((t - .9) / .6))           # exit arrow
        c.move_to(560, 1150); c.line_to(560 + 330 * p, 1150); c.set_source_rgba(*hx(GRN)); c.set_line_width(40); c.stroke()
        if p >= 1:
            c.move_to(950, 1150); c.line_to(870, 1080); c.line_to(870, 1220); c.close_path(); c.set_source_rgba(*hx(GRN)); c.fill()
    overlay(fr, cairo_layer(dr))

def sc_e1(fr, T, t, l):
    ebg(fr, 'end', T)
    title_line(fr, [('ऐसे ही रोज़ के सच', 0)], 380, t + .1, 104)
    title_line(fr, [('FreshNestHub', 2)], 560, t - 1.2, 120)
    k = back(clamp((t - .4) / .4))
    def dr(c): logo(c, CX, 1030, 170 * k)
    overlay(fr, cairo_layer(dr))
    if t > 2.0: put_rgba(fr, htext('फ़ॉलो करो', 84, THEME['end_text'], HI_B), CX, 1290, back(clamp((t - 2.0) / .3)), 1.0, 0)

SCENES = dict(h1=sc_h1, h2=sc_h2, s1=sc_s1, p1=sc_p1, p2=sc_p2, w1=sc_w1, w2=sc_w2, e1=sc_e1)
