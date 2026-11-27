
# ================= v3: REAL photos (Wikimedia Commons, CC0 / CC BY / CC BY-SA) + thermal-camera reveal
A73 = '/home/claude/studio/assets/73/'
def _rgba(p):
    im = Image.open(p).convert('RGBA'); return np.array(im)
BOXR = _rgba(A73 + 'box_cut.png')                                   # real clip-lid plastic box (CC0)
STEEL = _rgba(A73 + 'steel2.png')                                   # real steel bowl cutout (CC BY 4.0)

def photo_card(path, crop, w, rad=34, border=10):
    im = Image.open(path).convert('RGB').crop(crop); h = int(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new('RGBA', (w + 2 * border, h + 2 * border), (0, 0, 0, 0)); d = ImageDraw.Draw(out)
    d.rounded_rectangle((0, 0, w + 2 * border - 1, h + 2 * border - 1), rad + border, fill=(255, 255, 255, 255))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), rad, fill=255)
    out.paste(im, (border, border), m); return np.array(out)

# ---- hook plate: real microwave cavity + real box on the turntable; and its thermal twin
MWC = (140, 130, 1180, 900); MWW = 1000
@functools.lru_cache(maxsize=1)
def mw_plates():
    im = Image.open(A73 + 'mw_in.jpg').convert('RGB').crop(MWC); h = int(im.height * MWW / im.width)
    base = np.array(im.resize((MWW, h), Image.LANCZOS)).astype(np.float32)
    # warm "oven on" light
    yy, xx = np.mgrid[0:h, 0:MWW]; g = np.exp(-(((xx - 520) / 520) ** 2 + ((yy - 330) / 380) ** 2))
    warm = base * (0.55 + 0.6 * g[..., None]) * np.array([1.12, .9, .62]); warm = np.clip(warm, 0, 255)
    bx = cv2.resize(BOXR, (390, int(390 * BOXR.shape[0] / BOXR.shape[1])), interpolation=cv2.INTER_AREA)
    return warm.astype(np.uint8), bx, h
BOXPOS = (515, 485)     # box centre on the turntable inside the plate
def plate_frame(T, scan, hot):
    warm, bx, h = mw_plates(); p = warm.copy()
    sq = .9 + .1 * math.cos(T * 2.3)                                # turntable: the box turns (x squash)
    b = cv2.resize(bx, (max(8, int(bx.shape[1] * sq)), bx.shape[0]))
    sh = np.zeros((h, MWW), np.float32); cv2.ellipse(sh, (BOXPOS[0], BOXPOS[1] + 150), (int(200 * sq), 40), 0, 0, 360, .55, -1)
    sh = cv2.GaussianBlur(sh, (0, 0), 18); p = (p * (1 - sh[..., None])).astype(np.uint8)
    _put_on(p, b, BOXPOS[0], BOXPOS[1])
    if scan <= 0: return p
    gray = cv2.cvtColor(p, cv2.COLOR_RGB2GRAY).astype(np.float32) * .45
    yy, xx = np.mgrid[0:h, 0:MWW]
    blob = np.exp(-(((xx - BOXPOS[0]) / 230) ** 2 + ((yy - BOXPOS[1]) / 150) ** 2)) * 255 * hot
    th = cv2.applyColorMap(np.clip(gray + blob, 0, 255).astype(np.uint8), cv2.COLORMAP_INFERNO)[..., ::-1]
    xs = int(MWW * scan); p[:, :xs] = th[:, :xs]
    if scan < 1:
        p[:, max(0, xs - 4):xs + 4] = (170, 255, 230)
    return p
def _put_on(dst, rgba, cx, cy):
    h, w = rgba.shape[:2]; x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(dst.shape[1], x0 + w), min(dst.shape[0], y0 + h)
    s = rgba[ya - y0:yb - y0, xa - x0:xb - x0].astype(np.float32); a = s[..., 3:] / 255
    dst[ya:yb, xa:xb] = (dst[ya:yb, xa:xb] * (1 - a) + s[..., :3] * a).astype(np.uint8)

@functools.lru_cache(maxsize=1)
def photo_bg():
    """full-bleed blurred real photo + purple grade (premium documentary backdrop)"""
    im = Image.open(A73 + 'mw_in.jpg').convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 2, int(im.height * s) + 2), Image.LANCZOS)
    x0 = (im.width - W) // 2; a = np.array(im)[:H, x0:x0 + W].astype(np.float32)
    a = cv2.GaussianBlur(a, (0, 0), 26)
    tint = np.array(hx('3A1677')[:3]) * 255
    a = a * .38 + tint * .62
    yy = np.linspace(0, 1, H)[:, None, None]; a = a * (0.65 + .35 * np.sin(yy * math.pi))
    return np.clip(a, 0, 255).astype(np.uint8)

def sc_h1(fr, T, t, l):
    thumb = V == 'thumb'; tt = 2.6 if thumb else t
    fr[:] = photo_bg()
    scan = clamp((tt - 1.35) / .9); hot = clamp((tt - 1.3) / 1.0)
    pl = plate_frame(T, scan, hot)
    k = ease(clamp((tt - .1) / 1.1)); s = lerp(2.05, 1.0, k)
    card = np.zeros((pl.shape[0] + 20, MWW + 20, 4), np.uint8); card[..., :3] = 255; card[..., 3] = 255
    card[10:-10, 10:-10, :3] = pl
    cy = lerp(1060 + (pl.shape[0] / 2 - BOXPOS[1]) * 2.05, 1080, k)    # start centred on the box
    cx = lerp(CX + (MWW / 2 - BOXPOS[0]) * 2.05, CX, k)
    put_rgba(fr, card, cx, cy, s, 1.0, lerp(0, -1.5, k))
    if scan > 0:
        def parts(c):
            ox, oy = cx - MWW / 2 * s, cy - pl.shape[0] / 2 * s
            rng = np.random.default_rng(9); xs = ox + MWW * scan * s
            for kk in range(160):
                ang = rng.random() * 2 * math.pi; ph = (rng.random() + T * (.3 + .4 * rng.random())) % 1
                r = (60 + 300 * ph) * s; x = ox + BOXPOS[0] * s + math.cos(ang) * r; y = oy + BOXPOS[1] * s + math.sin(ang) * r * .7
                if x > xs: continue
                c.arc(x, y, (2 + 4 * rng.random()) * s, 0, 2 * math.pi); c.set_source_rgba(1, 1, .7, .95 * (1 - ph)); c.fill()
        overlay(fr, cairo_layer(parts))
    if k > .9: timer_txt(fr, 905, 790, 180 - tt * 30 if not thumb else 180, '7DFF9B', 64)
    title_line(fr, [('प्लास्टिक डिब्बा', 0)], 380, tt + 1.0, 108)
    title_line(fr, [('माइक्रोवेव में?', 3)], 548, tt + 1.0, 120)

def sc_h2(fr, T, t, l):
    ebg(fr, 'black', T)
    p = back(clamp(t / .35)); b = clamp((t - 1.9) / .25)
    def glow(c):
        if b > 0:
            g = cairo.RadialGradient(CX, 1060, 30, CX, 1060, 600); g.add_color_stop_rgba(0, .9, .22, .27, .5 * b); g.add_color_stop_rgba(1, .9, .22, .27, 0)
            c.arc(CX, 1060, 600, 0, 2 * math.pi); c.set_source(g); c.fill()
    overlay(fr, cairo_layer(glow))
    put_rgba(fr, BOXR, CX, 1060, 1.25 * p, 1.0, -3 + 2.5 * math.sin(T * 11) * b)
    if b > 0:
        def dr(c):
            rng = np.random.default_rng(21); u = t - 1.9
            for k in range(260):
                ang = rng.random() * 2 * math.pi; spd = .5 + rng.random(); d0 = rng.random() * .9
                z = 1.0 / (1 + max(0, (u * spd * .9 + d0 * (u > .4)) % 1.6) * 3.2)
                r = (1 / z - 1) * 120; x = CX + math.cos(ang) * r; y = 1060 + math.sin(ang) * r
                if not (-50 < x < W + 50 and 820 < y < H): continue
                sz = 2 + 5 / z * (.4 + rng.random() * .6)
                c.arc(x, y, min(sz, 34), 0, 2 * math.pi); c.set_source_rgba(*hx(RED if k % 3 else 'FFFFFF', min(1, .35 + .25 / z))); c.fill()
        overlay(fr, cairo_layer(dr))
    title_line(fr, [('3 मिनट में', 0)], 400, t, 124)
    title_line(fr, [('अरबों कण', 3)], 580, t - 1.95, 136)
    timer_txt(fr, CX, 820, 180 - clamp(t / 1.9) * 180, YL, 90)
    note(fr, 'आँख से दिखते नहीं', CX, 1340, t - 2.9, 50, YL, -3)

def _p2body(fr, T, t):
    S = 420; x0, y0 = CX - S / 2, 820
    if t < .75:                                             # dive into the real plastic wall
        z = ease(clamp(t / .75)); s = lerp(1.2, 9.0, z)
        put_rgba(fr, BOXR, CX - 40 * s, 1040 - 90 * s, s, 1.0, 0)
        def dv(c):
            q = S * s / 9; c.rectangle(CX - q / 2, 1040 - q / 2, q, q); c.set_source_rgba(*hx(YL)); c.set_line_width(6); c.stroke()
            c.rectangle(0, 0, W, H); c.set_source_rgba(.086, .086, .086, clamp((t - .45) / .3)); c.fill()
        overlay(fr, cairo_layer(dv)); return
    p = ease(clamp((t - .75) / .3))
    def dr(c):
        c.rectangle(x0, y0, S * p, S * p); c.set_source_rgba(*hx('F3F6FA', .14)); c.fill_preserve(); c.set_source_rgba(*hx(YL)); c.set_line_width(6); c.stroke()
        if p >= 1:
            n = int(clamp((t - 1.0) / 2.0) ** 1.6 * 900); rng = np.random.default_rng(11); pts = rng.random((900, 3))
            for i in range(n):
                px, py, s_ = pts[i]; jx = 2 * math.sin(T * 7 + i); jy = 2 * math.cos(T * 6 + i * 1.3)
                c.arc(x0 + 8 + px * (S - 16) + jx, y0 + 8 + py * (S - 16) + jy, 2 + s_ * 4, 0, 2 * math.pi)
                c.set_source_rgba(*hx(RED if i % 4 else 'FFFFFF', .9)); c.fill()
            for i in range(11):
                c.move_to(x0 + i * S / 10, y0 - 14 - (10 if i % 5 == 0 else 0)); c.line_to(x0 + i * S / 10, y0 - 4)
                c.move_to(x0 - 14 - (10 if i % 5 == 0 else 0), y0 + i * S / 10); c.line_to(x0 - 4, y0 + i * S / 10)
            c.set_source_rgba(1, 1, 1, .9); c.set_line_width(3); c.stroke()
    overlay(fr, cairo_layer(dr))
    if p >= 1:
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), CX, y0 - 58, 1.0, 1.0, 0)
        put_rgba(fr, htext('1 cm', 40, 'FFFFFF', HI_B), x0 - 80, y0 + S / 2, 1.0, 1.0, 90)
    note(fr, 'बस इतनी सी जगह', 760, 1330, t - 1.4, 48, YL, -4, 720, 1200)

def sc_a1(fr, T, t, l):
    fr[:] = photo_bg()
    put_rgba(fr, BOXR, CX, 1080, 1.45, 1.0, -4 + math.sin(T * 1.5))
    title_line(fr, [('और ये प्लास्टिक', 0)], 380, t, 116)
    title_line(fr, [('सरकार से मंज़ूर', 1)], 560, t - .6, 116)
    stamp(fr, 'मंज़ूर', CX + 40, 1080, t - 1.35, GRN, -14)
    note(fr, 'फिर भी?', 820, 1360, t - 1.9, 60, YL, 6)

# ---- real kidney cells (HEK 293 = human embryonic kidney) in the eyepiece; 75% die = patches go grey and dim
@functools.lru_cache(maxsize=1)
def hek_disc():
    im = Image.open(A73 + 'hek.jpg').convert('RGB'); s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    D = 2 * MR; a = np.array(im.resize((D, D), Image.LANCZOS)).astype(np.float32)
    rng = np.random.default_rng(7); seeds = rng.random((40, 2)) * D
    yy, xx = np.mgrid[0:D, 0:D]; d = np.stack([(xx - sx) ** 2 + (yy - sy) ** 2 for sx, sy in seeds]); lab = d.argmin(0)
    order = rng.permutation(40)
    return a, lab, order
def sc_k1(fr, T, t, l):
    ebg(fr, 'black', T)
    a, lab, order = hek_disc(); D = 2 * MR
    dead_n = int(clamp((t - 5.7) / .9) * 30)                       # 30 of 40 patches = 75%
    img = a.copy()
    if dead_n:
        m = np.isin(lab, order[:dead_n])[..., None]
        g = img.mean(2, keepdims=True); grey = np.concatenate([g, g, g], 2) * .55
        img = np.where(m, grey, img)
    zoom = 1.0 + .06 * t / l['dur']
    M = np.float32([[zoom, 0, (1 - zoom) * MR], [0, zoom, (1 - zoom) * MR]])
    img = cv2.warpAffine(img, M, (D, D), borderMode=cv2.BORDER_REFLECT)
    open_ = ease(clamp(t / .45)); R = MR * open_
    yy, xx = np.mgrid[0:D, 0:D]; rr = np.sqrt((xx - MR) ** 2 + (yy - MR) ** 2)
    alpha = np.clip(R - rr, 0, 1) * np.clip(1.25 - (rr / MR) ** 4 * .45, 0, 1)
    rgba = np.dstack([np.clip(img, 0, 255), alpha * 255]).astype(np.uint8)
    put_rgba(fr, rgba, MC[0], MC[1], 1.0, 1.0, 0)
    def dr(c):
        if R < 2: return
        if 1.0 < t < 6.2:
            c.save(); c.arc(*MC, R, 0, 2 * math.pi); c.clip(); rng = np.random.default_rng(5)
            for j in range(140):
                x0 = MC[0] + (rng.random() - .5) * 520; y0 = MC[1] + (rng.random() - .5) * 520; ang = rng.random() * 2 * math.pi
                ph = clamp((t - 1.0 - rng.random() * 2.5) / 1.6); d = lerp(320, 0, ease(ph))
                c.arc(x0 + d * math.cos(ang), y0 + d * math.sin(ang), 3 + 3 * rng.random(), 0, 2 * math.pi)
                c.set_source_rgba(*hx('FFE45C', .95 * (ph > 0))); c.fill()
            c.restore()
        c.arc(*MC, R + 10, 0, 2 * math.pi); c.set_source_rgba(.75, .75, .8, 1); c.set_line_width(20); c.stroke()
        c.arc(*MC, R + 22, 0, 2 * math.pi); c.set_source_rgba(.2, .2, .24, 1); c.set_line_width(8); c.stroke()
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('लैब: ', 0), ('किडनी', 1), (' कोशिकाएँ', 0)], 400, t, 108)
    if t > 5.6: title_line(fr, [('75% मर गईं', 3)], 580, t - 5.6, 132)
    note(fr, 'सबसे ज़्यादा मात्रा पर', 215, 1365, t - 3.0, 36, YL, -5)
    note(fr, '2 दिन में', 885, 1365, t - 4.7, 44, YL, 5)

_gw, _gh = Image.open(A73 + 'glass.jpg').size
GLASSC = photo_card(A73 + 'glass.jpg', (int(.1 * _gw), 0, int(.92 * _gw), _gh), 400)
@functools.lru_cache(maxsize=1)
def steel_card():
    w = 400; s = cv2.resize(STEEL, (w, w), interpolation=cv2.INTER_AREA)
    out = np.zeros((w + 20, w + 20, 4), np.uint8); out[..., :3] = 255; out[..., 3] = 255
    inner = np.zeros((w, w, 3), np.float32) + np.array([232, 228, 220], np.float32)
    a = s[..., 3:] / 255; out[10:-10, 10:-10, :3] = (inner * (1 - a) + s[..., :3] * a).astype(np.uint8)
    return out
def sc_w1(fr, T, t, l):
    fr[:] = photo_bg()
    title_line(fr, [('खाना गर्म करो', 0)], 380, t, 112)
    title_line(fr, [('काँच', 1), (' या ', 0), ('स्टील', 1), (' में', 0)], 560, t - .7, 116)
    k1 = ease(clamp((t - .6) / .4)); k2 = ease(clamp((t - 1.3) / .4))
    if k1 > 0: put_rgba(fr, GLASSC, lerp(-260, 290, k1), 1060, 1.0, 1.0, -5)
    if k2 > 0: put_rgba(fr, steel_card(), lerp(W + 260, 790, k2), 1080, 1.0, 1.0, 5)
    def dr(c):
        tick_ring(c, 300, 1310, 46, back(clamp((t - 1.0) / .3)), True)
        tick_ring(c, 790, 1330, 46, back(clamp((t - 1.7) / .3)), True)
    overlay(fr, cairo_layer(dr))

def sc_w2(fr, T, t, l):
    ebg(fr, 'black', T)
    fz = clamp((t - 1.1) / .8)
    b = BOXR.copy().astype(np.float32)
    b[..., :3] = b[..., :3] * (1 - .45 * fz) + np.array([200, 235, 255]) * .45 * fz
    put_rgba(fr, b.astype(np.uint8), CX, 1080, 1.3, 1.0, 2)
    def dr(c):
        for i in range(14):
            ph = (T * .12 + i * .071) % 1
            snowflake(c, 140 + (i * 61) % 820, 760 + ph * 620, 10 + (i % 3) * 5, .8 * fz, T * .5 + i)
    overlay(fr, cairo_layer(dr))
    title_line(fr, [('प्लास्टिक डिब्बा?', 0)], 400, t, 120)
    title_line(fr, [('सिर्फ़ ठंडा खाना', 1)], 580, t - 1.0, 120)
    note(fr, 'गर्म करने के लिए नहीं', CX, 1340, t - 1.9, 48, YL, -3)

SCENES = dict(h1=sc_h1, h2=sc_h2, p1=sc_p1, p2=sc_p2, a1=sc_a1, k1=sc_k1, w1=sc_w1, w2=sc_w2, e1=sc_e1)
