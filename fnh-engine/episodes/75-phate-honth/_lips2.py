
# ================= lips v2: 3D leaves growing in from the corners, glow-green set, photo-circle cycle, icon checklist, brush banner, sparkles
def _glow_green():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - CX) / W) ** 2 + ((yy - 1000) / H * 1.1) ** 2)
    a = np.clip(1 - r * 1.5, 0, 1)[..., None]
    c0 = np.array(rgb('0B3A22'), np.float32); c1 = np.array(rgb('2E9A5E'), np.float32)
    base = c0 * (1 - a) + c1 * a
    rng = np.random.default_rng(6); n = cv2.GaussianBlur(rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32), (0, 0), 1.2)
    base = base + cv2.resize(n, (W, H))[..., None] * 4
    return np.clip(base, 0, 255).astype(np.uint8)
_PP['p'] = _glow_green()

def leaf(c, x, y, L, ang, T, seed, k=1.0, dark=False):
    """glossy 3D-ish tropical leaf: gradient body, light rim, midrib + veins, gentle sway"""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang + .05 * math.sin(T * 1.3 + seed)); c.scale(k, k)
    w = L * .36
    c.move_to(0, 0); c.curve_to(w, -L * .15, w * 1.1, -L * .7, 0, -L); c.curve_to(-w * 1.1, -L * .7, -w, -L * .15, 0, 0); c.close_path()
    g = cairo.LinearGradient(-w, -L * .5, w, -L * .5)
    c0, c1 = ((.04, .28, .14), (.18, .55, .28)) if dark else ((.10, .45, .22), (.42, .78, .38))
    g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(.55, *c1); g.add_color_stop_rgb(1, *c0)
    c.set_source(g); c.fill_preserve(); c.set_source_rgba(.02, .16, .08, .9); c.set_line_width(3); c.stroke()
    c.move_to(0, 0); c.curve_to(w * .1, -L * .4, 0, -L * .7, 0, -L * .96); c.set_source_rgba(.85, 1, .8, .55); c.set_line_width(4); c.stroke()
    for i in range(1, 7):
        yy = -L * i / 7.5
        for s in (-1, 1):
            c.move_to(0, yy); c.curve_to(s * w * .3, yy - L * .03, s * w * .6, yy - L * .08, s * w * .8, yy - L * .14)
        c.set_source_rgba(.85, 1, .8, .25); c.set_line_width(2); c.stroke()
    c.move_to(-w * .5, -L * .5); c.curve_to(-w * .4, -L * .7, -w * .15, -L * .85, 0, -L * .9); c.set_source_rgba(1, 1, 1, .18); c.set_line_width(10); c.stroke()
    c.restore()
LEAVES = [(-20, 300, 330, 2.2, 0, True), (30, 250, 260, 1.7, 1, False), (-30, 520, 220, 1.95, 2, False),
          (1100, 1900, 380, -.7, 3, True), (1060, 1960, 300, -1.1, 4, False), (-20, 1920, 300, .7, 5, False)]
def leaves_layer(T, t):
    def dr(c):
        for i, (x, y, L, a, sd, dk) in enumerate(LEAVES):
            k = back(clamp((t - i * .05) / .45))
            leaf(c, x, y, L, a, T, sd, k, dk)
    return cairo_layer(dr)

@functools.lru_cache(maxsize=16)
def circle_photo(name, cx, cy, r, d=260, ring=10):
    im = Image.open(A75 + name).convert('RGB'); a, b = im.size
    x0, y0 = int((cx - r) * a), int((cy - r) * a); s = int(2 * r * a)
    im = im.crop((x0, y0, x0 + s, y0 + s)).resize((d, d), Image.LANCZOS)
    out = Image.new('RGBA', (d + 2 * ring + 16, d + 2 * ring + 16), (0, 0, 0, 0)); dd = ImageDraw.Draw(out)
    dd.ellipse((10, 14, d + 2 * ring + 10, d + 2 * ring + 14), fill=(10, 30, 18, 140))
    dd.ellipse((0, 0, d + 2 * ring, d + 2 * ring), fill=(255, 255, 255, 255))
    m = Image.new('L', (d, d), 0); ImageDraw.Draw(m).ellipse((0, 0, d - 1, d - 1), fill=255)
    out.paste(im, (ring, ring), m); return np.array(out)
def badge(c, x, y, r, good, k=1.0):
    if k <= 0: return
    c.arc(x, y, r * k, 0, 2 * math.pi); c.set_source_rgba(*hx(GRN if good else RED)); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(4); c.stroke()
    c.set_line_width(max(2, 6 * k)); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if good: c.move_to(x - r * .45 * k, y); c.line_to(x - r * .1 * k, y + r * .35 * k); c.line_to(x + r * .5 * k, y - r * .35 * k)
    else: c.move_to(x - r * .4 * k, y - r * .4 * k); c.line_to(x + r * .4 * k, y + r * .4 * k); c.move_to(x + r * .4 * k, y - r * .4 * k); c.line_to(x - r * .4 * k, y + r * .4 * k)
    c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
def sparks(c, x, y, t, a0=-2.4):
    if t <= 0: return
    k = back(clamp(t / .25))
    for i in range(3):
        an = a0 + i * .45; r0, r1 = 26 * k, 70 * k
        c.move_to(x + r0 * math.cos(an), y + r0 * math.sin(an)); c.line_to(x + r1 * math.cos(an), y + r1 * math.sin(an))
    c.set_source_rgba(*hx(YLP)); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)

@functools.lru_cache(maxsize=16)
def brush_banner(txt, size=56):
    f = ImageFont.truetype(ANEK, size, layout_engine=ImageFont.Layout.RAQM); tw = int(f.getlength(txt))
    w, h = tw + 110, int(size * 1.9)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(len(txt)); pts = []
    for i in range(24):                                              # ragged brush outline
        x = 20 + (w - 40) * i / 23; pts.append((x, 12 + rng.random() * 10))
    for i in range(24):
        x = w - 20 - (w - 40) * i / 23; pts.append((x, h - 14 - rng.random() * 10))
    d.polygon(pts, fill=rgb(YLP) + (255,)); d.ellipse((0, 10, 50, h - 10), fill=rgb(YLP) + (255,)); d.ellipse((w - 50, 10, w, h - 10), fill=rgb(YLP) + (255,))
    d.text((55, int(size * .28)), txt, font=f, fill=rgb(INKP) + (255,))
    a = np.array(im); M = np.float32([[1, -.18, 14], [0, 1, 0]])
    return cv2.warpAffine(a, M, (w + 30, h), borderValue=(0, 0, 0, 0))

# ---- upgraded scenes
_l1_old = sc_l1
def sc_l1(fr, T, t, l):
    _l1_old(fr, T, t, l)
    tt = 1.4 if V == 'thumb' else t
    overlay(fr, cairo_layer(lambda c: sparks(c, 230, 830, tt - .25)))
    if V != 'thumb' and 1.9 < t < 3.4:
        _put0(fr, brush_banner('अच्छा लगा', 60), CX, 1300, back(clamp((t - 1.9) / .25)), 1.0, -3)

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
            badge(c, x + 100, y - 100, 30, False, back(clamp((t - ts - .25) / .25)) * (1 - cyc))
        if cyc > 0:
            for j in range(4):                                       # arrows between the 4 photo circles
                a0 = j * math.pi / 2 - math.pi / 2 + .45; a1 = a0 + math.pi / 2 - .9
                c.arc(CX, 1000, 230, a0, a1); c.set_source_rgba(*hx('1F7A45', cyc)); c.set_line_width(12); c.stroke()
                x, y = CX + 230 * math.cos(a1), 1000 + 230 * math.sin(a1); dx, dy = -math.sin(a1), math.cos(a1)
                c.move_to(x + dx * 26, y + dy * 26); c.line_to(x - dy * 20, y + dx * 20); c.line_to(x + dy * 20, y - dx * 20); c.close_path(); c.fill()
            c.save(); c.translate(CX, 1000); c.rotate(T * 2)
            for j in range(2):
                c.arc(0, 0, 60, j * math.pi + .3, j * math.pi + 2.6); c.set_source_rgba(*hx(REDP, cyc)); c.set_line_width(10); c.stroke()
            c.restore()
    overlay(fr, cairo_layer(dr))
    for i, (ts, lab, col) in enumerate(items):
        k = clamp((t - ts - .1) / .2) * (1 - cyc)
        if k > 0: _put0(fr, htext(lab, 64, INKP, ANEK), 220 + i * 310, 1000 + (i % 2) * 70, 1.0, k, (i - 1) * 4.5)
    if cyc > 0:
        spots = [('chapped.jpg', .5, .33, .16, 'बाम लगाया'), ('licker.jpg', .5, .62, .14, 'होंठ सूखे'), ('chapped.jpg', .3, .45, .15, 'फिर फटे'), ('licker.jpg', .52, .78, .12, 'फिर बाम')]
        for j, (nm, cx_, cy_, r_, lab) in enumerate(spots):
            a = j * math.pi / 2 - math.pi / 2; x, y = CX + 230 * math.cos(a), 1000 + 230 * math.sin(a)
            kk = back(clamp((cyc - j * .1) / .6)) if cyc < 1 else 1.0
            _put0(fr, circle_photo(nm, cx_, cy_, r_, 160, 8), x, y, kk, 1.0, 0)
            _put0(fr, card_line_img(((lab, 1 if j == 3 else 0),), 38, 'cream', 0), x, y + 105, kk * .85, 1.0, 0)
    title_line(fr, [('और सुखाते हैं', 1)], 380, t, 124)
    if t > 3.7: title_line(fr, [('फिर बाम, फिर बाम', 3)], 560, t - 3.7, 112)

TONGUE_IMG = None
def sc_l8(fr, T, t, l):
    ebg(fr, 'cream', T)
    rows = [(.9, 'जीभ फेरना बंद', False), (2.8, 'बिना खुशबू पेट्रोलियम जेली', True), (4.45, 'दिन में कई बार और रात को', True)]
    def dr(c):
        for i, (ts, _, good) in enumerate(rows):
            k = back(clamp((ts and (t - ts) or t) / .3)) if True else 0
            k = back(clamp((t - ts) / .3))
            if k <= 0: continue
            y = 790 + i * 190
            c.save(); c.translate(CX, y); c.scale(k, k); c.translate(-CX, -y)
            rrect(c, 230 + 10, y - 70 + 12, 760, 140, 70); c.set_source_rgba(0, 0, 0, .3); c.fill()
            rrect(c, 230, y - 70, 760, 140, 70); c.set_source_rgba(*hx('FBF7EE')); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
            c.arc(210, y, 95, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill_preserve(); c.set_source_rgba(*hx(INKP)); c.set_line_width(5); c.stroke()
            if i == 0: tongue(c, 210, y - 20, .75)
            elif i == 2:
                c.arc(200, y, 52, 0, 2 * math.pi); c.set_source_rgba(*hx('FFD65C')); c.fill(); c.arc(228, y - 18, 46, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 1); c.fill()
            c.restore()
    overlay(fr, cairo_layer(dr))
    if t > 2.8: _put0(fr, jelly_cut(), 210, 980, .42 * back(clamp((t - 2.8) / .3)), 1.0, 0)
    def bd(c):
        for i, (ts, _, good) in enumerate(rows): badge(c, 285, 790 + i * 190 - 70, 30, good, back(clamp((t - ts - .3) / .25)))
    overlay(fr, cairo_layer(bd))
    for i, (ts, txt, good) in enumerate(rows):
        k = clamp((t - ts - .1) / .2)
        if k > 0: _put0(fr, htext(txt, 50, INKP, ANEK), 640, 790 + i * 190, 1.0, k, 0)
    title_line(fr, [('इलाज सीधा', 3)], 380, t, 124)

SCENES.update(s1=sc_l1, s6=sc_l6, s8=sc_l8)

_frame_prev = frame
NOLEAF = ('e1',)
LT = [0.0, 's1']
_ebg0 = ebg
def ebg(fr, mode, T=0.0):
    _ebg0(fr, mode, T)
    if LT[1] not in NOLEAF: overlay(fr, leaves_layer(T, LT[0] if V != 'thumb' else 1.0))
def frame(T):
    CUR[0] = T
    fr = np.zeros((H, W, 3), np.uint8)
    l = TL[0]
    for x in TL:
        if x['start'] <= T: l = x
    t = T - l['start']; LT[0] = t; LT[1] = l['id']
    SCENES[l['id']](fr, T, t, l)
    camera(fr, l, t, T)
    if V != 'thumb': transition(fr, T)
    if V != 'thumb': subtitle(fr, T)
    overlay(fr, BADGE)
    g = cv2.resize(_GR[int(T * 12) % 6], (W, H))[..., None]
    return np.clip(fr.astype(np.float32) + g, 0, 255).astype(np.uint8)
