# ================= props: carrots, beta-carotene, vitamin A machine, skin layers, palm, sole, baby, eyes, WWII plane, radar =================
CARROT = (255, 128, 30); CARROT_D = (214, 84, 10); LEAF = (60, 176, 70); LEAF_D = (24, 110, 40)


def carrot_el(bite=0, leaves=True):
    """vertical carrot, tip down. bite 0..3 = chunks bitten off the top."""
    def mk():
        w, h, sc = 170, 440, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        top = 120 + 34 * bite
        if leaves and bite == 0:
            for ang, L in ((-28, 110), (0, 128), (26, 104), (-12, 90), (14, 96)):
                a = math.radians(ang); x1, y1 = 85 + math.sin(a) * L, 120 - math.cos(a) * L
                shape_grad(im, lambda m, x1=x1, y1=y1: m.polygon(S(78, 124, x1 - 12, y1, x1 + 12, y1, 92, 124), fill=255), LEAF, LEAF_D)
        body = lambda m: m.polygon(S(22, top, 148, top, 104, 410, 85, 436, 66, 410), fill=255)
        shape_grad(im, body, (255, 160, 60), CARROT_D)
        d.rounded_rectangle(S(20, top - 6, 150, top + 30), 18 * sc, fill=(255, 150, 50, 255))
        if bite:
            d.ellipse(S(30, top - 8, 140, top + 22), fill=(255, 196, 110, 255))
            for bx in (44, 80, 116): d.ellipse(S(bx - 18, top - 22, bx + 18, top + 8), fill=(0, 0, 0, 0))
        _ov(im, lambda q: q.line(S(48, top + 30, 74, 380), fill=(255, 220, 160, 150), width=8 * sc))
        for yy in range(top + 50, 400, 46):
            hw = 56 * (1 - (yy - top) / (436 - top)) + 8
            d.line(S(85 - hw * 0.7, yy, 85 - hw * 0.1, yy + 6), fill=CARROT_D + (255,), width=4 * sc)
            d.line(S(85 + hw * 0.2, yy + 22, 85 + hw * 0.75, yy + 18), fill=CARROT_D + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("carrot", bite, leaves), mk)


def dots(f, pts, r=12, col=CARROT, op=1.0):
    for (x, y) in pts:
        cv2.circle(f, (int(x), int(y)), int(r + 3), C(CARROT_D), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), int(r), C(col), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x - r * 0.35), int(y - r * 0.35)), max(1, int(r * 0.3)), (1, 1, 1), -1, cv2.LINE_AA)


def machine_el():
    def mk():
        w, h, sc = 560, 560, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(80, 190, 500, 556), 40 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.polygon(S(150, 0, 410, 0, 330, 150, 230, 150), fill=255), (220, 226, 240), (130, 140, 160))
        shape_grad(im, lambda m: m.rounded_rectangle(S(60, 140, 480, 530), 40 * sc, fill=255), (90, 120, 240), (40, 60, 160))
        d.rounded_rectangle(S(100, 190, 440, 300), 22 * sc, fill=(255, 255, 255, 255))
        d.text((270 * sc, 245 * sc), "BODY", font=font(F_BLACK, 70 * sc), fill=(40, 60, 160, 255), anchor="mm")
        for i in range(3): d.ellipse(S(120 + i * 60, 340, 160 + i * 60, 380), fill=(255, 214, 60, 255) if i == 0 else (140, 160, 240, 255))
        d.rounded_rectangle(S(440, 400, 556, 470), 16 * sc, fill=(60, 70, 120, 255))
        for gx in (130, 250, 370):
            d.ellipse(S(gx - 34, 420, gx + 34, 488), fill=(70, 90, 190, 255), outline=(30, 40, 110, 255), width=5 * sc)
        return _done(im, w, h)
    return gcache("machine", mk)


def capsule_el():
    def mk():
        w, h, sc = 150, 74, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(2, 2, 148, 72), 35 * sc, fill=INK + (255,))
        d.rounded_rectangle(S(7, 7, 75, 67), 30 * sc, fill=(255, 214, 40, 255)); d.rectangle(S(40, 7, 75, 67), fill=(255, 214, 40, 255))
        d.rounded_rectangle(S(75, 7, 143, 67), 30 * sc, fill=(255, 255, 255, 255)); d.rectangle(S(75, 7, 110, 67), fill=(255, 255, 255, 255))
        d.text((42 * sc, 38 * sc), "A", font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        _ov(im, lambda q: q.line(S(20, 18, 130, 18), fill=(255, 255, 255, 160), width=5 * sc))
        return _done(im, w, h)
    return gcache("capsule", mk)


def gauge_tube(f, x, y0, y1, k, limit=0.8, w=70, col=(255, 214, 40), label="LIMIT"):
    cv2.rectangle(f, (int(x - w / 2 - 8), int(y0 - 8)), (int(x + w / 2 + 8), int(y1 + 8)), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), int(y0)), (int(x + w / 2), int(y1)), C((240, 244, 250)), -1, cv2.LINE_AA)
    lv = y1 - (y1 - y0) * clamp(k)
    cv2.rectangle(f, (int(x - w / 2), int(lv)), (int(x + w / 2), int(y1)), C(col), -1, cv2.LINE_AA)
    ly = y1 - (y1 - y0) * limit
    cv2.line(f, (int(x - w / 2 - 26), int(ly)), (int(x + w / 2 + 26), int(ly)), C(RED2), 8, cv2.LINE_AA)
    comp(f, chip(label, RED2, WHITE, 26), x, ly - 34)


def vessel(f, x0, x1, yc, r, t, flow=300, n_cells=9, n_dots=0, seed=3, dots_out=0.0):
    """horizontal blood vessel cut-away with red cells + orange beta-carotene dots flowing right."""
    cv2.rectangle(f, (int(x0), int(yc - r - 22)), (int(x1), int(yc + r + 22)), C((200, 60, 80)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x0), int(yc - r)), (int(x1), int(yc + r)), C((255, 200, 196)), -1, cv2.LINE_AA)
    cv2.line(f, (int(x0), int(yc - r - 22)), (int(x1), int(yc - r - 22)), C(INK), 5, cv2.LINE_AA)
    cv2.line(f, (int(x0), int(yc + r + 22)), (int(x1), int(yc + r + 22)), C(INK), 5, cv2.LINE_AA)
    rng = np.random.default_rng(seed); L = x1 - x0
    for i in range(n_cells):
        ox = rng.uniform(0, L); oy = rng.uniform(-r * 0.6, r * 0.6)
        x = x0 + (ox + flow * t) % L; y = yc + oy + 6 * math.sin(t * 3 + i)
        cv2.ellipse(f, (int(x), int(y)), (30, 22), 15 * math.sin(t + i), 0, 360, C((200, 30, 40)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), int(y)), (14, 9), 15 * math.sin(t + i), 0, 360, C((150, 16, 26)), -1, cv2.LINE_AA)
    pts = []
    for i in range(n_dots):
        ox = rng.uniform(0, L); oy = rng.uniform(-r * 0.7, r * 0.7)
        x = x0 + (ox + flow * 1.1 * t) % L; y = yc + oy + 8 * math.sin(t * 4 + i * 2)
        pts.append((x, y))
    dots(f, pts, 11)


def skin_block(f, x, y, w, k_orange, thick=1.0, label=True, t=0.0):
    """skin cross-section centred at x, top at y. outer layer thickness scales with `thick`; k_orange tints the outer layer."""
    ho = int(40 + 70 * thick); he = 110; hd = 190
    x0, x1 = int(x - w / 2), int(x + w / 2)
    f[y + 14:y + ho + he + hd + 14, x0 + 14:x1 + 14] *= 0.7
    base = np.array(C((246, 214, 180)), np.float32); org = np.array(C((255, 150, 50)), np.float32)
    f[y:y + ho, x0:x1] = base * (1 - k_orange) + org * k_orange
    for i in range(int(ho / 14)):
        cv2.line(f, (x0, y + 8 + i * 14), (x1, y + 8 + i * 14), C((200, 150, 110)), 2, cv2.LINE_AA)
    f[y + ho:y + ho + he, x0:x1] = np.array(C((255, 190, 170)), np.float32)
    f[y + ho + he:y + ho + he + hd, x0:x1] = np.array(C((240, 120, 130)), np.float32)
    rng = np.random.default_rng(5)
    for i in range(10):
        cx = rng.uniform(x0 + 20, x1 - 20); cy = y + ho + he + rng.uniform(30, hd - 30)
        cv2.circle(f, (int(cx), int(cy)), int(rng.uniform(14, 26)), C((255, 220, 130)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y), (x1, y + ho + he + hd), C(INK), 6, cv2.LINE_AA)
    cv2.line(f, (x0, y + ho), (x1, y + ho), C(INK), 4, cv2.LINE_AA)
    if k_orange > 0.05:
        rng2 = np.random.default_rng(9); pts = [(rng2.uniform(x0 + 16, x1 - 16), y + rng2.uniform(10, ho - 10)) for _ in range(int(14 * thick * k_orange) + 2)]
        dots(f, pts, 8)
    return y + ho


def palm_el(tint=0.0):
    tint, skin = _tint(tint)
    def mk():
        w, h, sc = 520, 640, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        fills = []
        for (x0, y0, x1, y1) in ((92, 110, 170, 360), (182, 40, 260, 340), (272, 50, 350, 340), (362, 110, 440, 360)):
            fills.append(lambda m, b=(x0, y0, x1, y1): m.rounded_rectangle(S(*b), 39 * sc, fill=255))
        fills.append(lambda m: m.polygon(S(70, 380, 20, 250, 60, 230, 140, 330), fill=255))
        fills.append(lambda m: m.ellipse(S(40, 220, 40 + 50, 290), fill=255))
        fills.append(lambda m: m.rounded_rectangle(S(80, 280, 450, 620), 150 * sc, fill=255))
        def allm(m):
            for fn in fills: fn(m)
        ol = Image.new("L", im.size, 0); allm(ImageDraw.Draw(ol))
        olb = ol.filter(ImageFilter.MaxFilter(17))
        im.paste(Image.new("RGBA", im.size, INK + (255,)), (0, 0), olb)
        hi = tuple(min(255, c + 16) for c in skin); lo = tuple(int(c * 0.86) for c in skin)
        shape_grad(im, allm, hi, lo)
        for (a, b, c_, e) in ((140, 430, 330, 380), (150, 480, 400, 450), (200, 560, 300, 400)):
            d.arc(S(a, c_ - 60, b, e + 40), 200, 330, fill=tuple(int(v * 0.7) for v in skin) + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("palm", tint), mk)


def sole_el(tint=0.0):
    tint, skin = _tint(tint)
    def mk():
        w, h, sc = 360, 640, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def allm(m):
            m.ellipse(S(40, 120, 330, 420), fill=255); m.ellipse(S(80, 330, 280, 630), fill=255); m.rectangle(S(70, 300, 300, 480), fill=255)
            for i, (tx, ty, r) in enumerate(((90, 90, 46), (170, 60, 36), (232, 64, 32), (282, 88, 28), (318, 124, 24))):
                m.ellipse(S(tx - r, ty - r, tx + r, ty + r), fill=255)
        ol = Image.new("L", im.size, 0); allm(ImageDraw.Draw(ol))
        im.paste(Image.new("RGBA", im.size, INK + (255,)), (0, 0), ol.filter(ImageFilter.MaxFilter(15)))
        shape_grad(im, allm, tuple(min(255, c + 16) for c in skin), tuple(int(c * 0.84) for c in skin))
        _ov(im, lambda q: q.ellipse(S(90, 170, 200, 300), fill=(255, 255, 255, 50)))
        return _done(im, w, h)
    return gcache(("sole", tint), mk)


def eye2_el(sclera=(255, 255, 255), skin=None):
    skin = skin or CH_SKIN
    def mk():
        w, h, sc = 560, 380, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def almond(m, pad=0):
            top = [(20 + i * 5.2, 190 - math.sin(math.pi * i / 100) * (150 + pad)) for i in range(101)]
            bot = [(540 - i * 5.2, 190 + math.sin(math.pi * i / 100) * (130 + pad)) for i in range(101)]
            m.polygon([(px * sc, py * sc) for px, py in top + bot], fill=255)
        shape_grad(im, lambda m: m.ellipse(S(0, 0, 560, 380), fill=255), tuple(min(255, c + 10) for c in skin), tuple(int(c * 0.86) for c in skin))
        shape_grad(im, lambda m: almond(m, 8), (120, 70, 60), (90, 50, 44))
        shape_grad(im, almond, tuple(sclera), tuple(int(c * 0.9) for c in sclera))
        shape_grad(im, lambda m: m.ellipse(S(190, 100, 370, 280), fill=255), (110, 80, 50), (60, 40, 24))
        d.ellipse(S(240, 150, 320, 230), fill=(12, 12, 16, 255))
        d.ellipse(S(300, 128, 330, 158), fill=(255, 255, 255, 240))
        top = [(20 + i * 5.2, 190 - math.sin(math.pi * i / 100) * 150) for i in range(101)]
        d.line([(px * sc, py * sc) for px, py in top], fill=INK + (255,), width=10 * sc, joint="curve")
        for i in range(14, 90, 10):
            px, py = top[i]; a = math.atan2(py - 190, px - 280)
            d.line(S(px, py, px + 26 * math.cos(a), py + 22 * math.sin(a) - 4), fill=INK + (255,), width=6 * sc)
        return _done(im, w, h)
    return gcache(("eye2", tuple(sclera), tuple(skin)), mk)


def baby(f, x, y, s, t, tint=0.0, mouth=0, expr="happy"):
    """baby in a high chair, (x, y) = chair floor centre."""
    ink = C(INK)
    for side in (-1, 1): cv2.line(f, (int(x + side * 90 * s), int(y - 260 * s)), (int(x + side * 120 * s), int(y)), C((200, 120, 60)), int(16 * s), cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 150 * s), int(y - 290 * s)), (int(x + 150 * s), int(y - 250 * s)), C((230, 150, 80)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 150 * s), int(y - 290 * s)), (int(x + 150 * s), int(y - 250 * s)), ink, 5, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y - 360 * s)), (int(95 * s), int(85 * s)), 0, 0, 360, ink, -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y - 360 * s)), (int(88 * s), int(78 * s)), 0, 0, 360, C((250, 250, 255)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y - 400 * s)), (int(60 * s), int(36 * s)), 0, 0, 180, C((255, 120, 150)), -1, cv2.LINE_AA)
    _, sk = _tint(tint)
    for side in (-1, 1):
        cv2.line(f, (int(x + side * 80 * s), int(y - 380 * s)), (int(x + side * 120 * s), int(y - 320 * s)), ink, int(10 * s), cv2.LINE_AA)
        cv2.circle(f, (int(x + side * 120 * s), int(y - 318 * s)), int(15 * s), ink, -1, cv2.LINE_AA)
        cv2.circle(f, (int(x + side * 120 * s), int(y - 318 * s)), int(11 * s), C(sk), -1, cv2.LINE_AA)
    comp(f, scale_el(chub_head_el(mouth, False, "up", 0, 0, expr, tint), 0.9 * s), x, y - 520 * s)


def bowl_el(label="MASHED CARROT"):
    def mk():
        w, h, sc = 420, 220, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(40, 20, 380, 80), fill=(255, 140, 40, 255))
        _ov(im, lambda q: q.ellipse(S(90, 30, 200, 56), fill=(255, 200, 120, 200)))
        shape_grad(im, lambda m: m.chord(S(20, -110, 400, 210), 0, 180, fill=255), (120, 200, 255), (40, 120, 220))
        d.text((210 * sc, 140 * sc), label, font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("bowl", label), mk)


def spoon_el():
    def mk():
        w, h, sc = 320, 90, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(100, 36, 316, 54), 9 * sc, fill=(200, 206, 220, 255))
        d.ellipse(S(4, 14, 120, 76), fill=(200, 206, 220, 255)); d.ellipse(S(16, 22, 104, 62), fill=(255, 140, 40, 255))
        return _done(im, w, h)
    return gcache("spoon", mk)


def carrot_side(bite=0, sc_=0.5):
    def mk():
        pm, a = scale_el(carrot_el(0, True), sc_)
        return np.ascontiguousarray(np.rot90(pm, -1)), np.ascontiguousarray(np.rot90(a, -1))
    return gcache(("cside", bite, sc_), mk)


def plane_el_old():
    def mk():
        w, h, sc = 760, 300, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        g0, g1 = (110, 130, 90), (54, 70, 44)
        shape_grad(im, lambda m: m.polygon(S(40, 110, 120, 70, 160, 130, 60, 150), fill=255), g0, g1)  # tail fin
        shape_grad(im, lambda m: m.polygon(S(30, 130, 120, 120, 120, 150, 30, 150), fill=255), g0, g1)
        shape_grad(im, lambda m: m.rounded_rectangle(S(60, 110, 690, 190), 40 * sc, fill=255), g0, g1)
        shape_grad(im, lambda m: m.polygon(S(250, 170, 480, 170, 520, 240, 230, 240), fill=255), (90, 110, 74), (44, 58, 36))
        d.ellipse(S(640, 116, 712, 184), fill=(60, 60, 66, 255))
        _ov(im, lambda q: q.chord(S(300, 50, 470, 170), 180, 360, fill=(180, 230, 255, 200)))
        d.arc(S(300, 50, 470, 170), 180, 360, fill=INK + (255,), width=5 * sc)
        _ov(im, lambda q: q.line(S(120, 128, 620, 128), fill=(255, 255, 255, 50), width=6 * sc))
        return _done(im, w, h)
    return gcache("plane", mk)


def radar_screen(f, x, y, r, t, blip=True):
    cv2.circle(f, (int(x), int(y)), int(r + 14), C(INK), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(r), C((8, 40, 20)), -1, cv2.LINE_AA)
    for k in (0.33, 0.66, 1.0): cv2.circle(f, (int(x), int(y)), int(r * k), C((40, 160, 80)), 2, cv2.LINE_AA)
    cv2.line(f, (int(x - r), int(y)), (int(x + r), int(y)), C((40, 160, 80)), 2, cv2.LINE_AA)
    cv2.line(f, (int(x), int(y - r)), (int(x), int(y + r)), C((40, 160, 80)), 2, cv2.LINE_AA)
    a = t * 3.2
    for j in range(14):
        aa = a - j * 0.05; col = np.array(C((80, 255, 140)), np.float32) * (1 - j / 14)
        cv2.line(f, (int(x), int(y)), (int(x + r * math.cos(aa)), int(y + r * math.sin(aa))), tuple(float(c) for c in col), 4, cv2.LINE_AA)
    if blip:
        bx, by = x + r * 0.55 * math.cos(-0.8), y + r * 0.55 * math.sin(-0.8)
        ph = (a - (-0.8)) % (2 * math.pi); br = math.exp(-ph * 1.2)
        cv2.circle(f, (int(bx), int(by)), int(10 + 8 * br), C((160, 255, 180)), -1, cv2.LINE_AA)


def zzz_moon(f, t):
    rng = np.random.default_rng(3)
    for i in range(40):
        x, y = rng.uniform(40, 1040), rng.uniform(260, 1300); tw = 0.5 + 0.5 * math.sin(t * 3 + i)
        cv2.circle(f, (int(x), int(y)), int(2 + 2 * tw), (1, 1, 1), -1, cv2.LINE_AA)


def mirror_el():
    def mk():
        w, h, sc = 300, 520, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(126, 300, 174, 510), 24 * sc, fill=(236, 80, 140, 255))
        d.ellipse(S(10, 10, 290, 330), fill=(236, 80, 140, 255))
        shape_grad(im, lambda m: m.ellipse(S(30, 30, 270, 310), fill=255), (220, 244, 255), (140, 190, 230))
        _ov(im, lambda q: q.line(S(80, 90, 140, 60), fill=(255, 255, 255, 220), width=14 * sc))
        _ov(im, lambda q: q.line(S(70, 140, 100, 120), fill=(255, 255, 255, 180), width=10 * sc))
        return _done(im, w, h)
    return gcache("mirror", mk)


def plane_el():
    def mk():
        w, h, sc = 820, 360, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        g0, g1 = (120, 142, 96), (52, 68, 42)
        shape_grad(im, lambda m: m.polygon(S(30, 80, 110, 60, 150, 170, 70, 180), fill=255), g0, g1)
        shape_grad(im, lambda m: m.polygon(S(20, 176, 170, 166, 170, 196, 40, 200), fill=255), g0, g1)
        shape_grad(im, lambda m: m.polygon(S(40, 160, 300, 120, 700, 128, 740, 170, 700, 226, 300, 230, 40, 196), fill=255), g0, g1)
        d.polygon(S(40, 160, 300, 120, 700, 128, 740, 170, 700, 226, 300, 230, 40, 196), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(680, 124, 760, 228), 30 * sc, fill=(60, 62, 70, 255), outline=INK + (255,), width=4 * sc)
        d.rectangle(S(250, 180, 268, 230), fill=(255, 214, 60, 255))
        shape_grad(im, lambda m: m.ellipse(S(260, 200, 640, 290), fill=255), (100, 122, 80), (44, 58, 36))
        d.ellipse(S(260, 200, 640, 290), outline=INK + (255,), width=4 * sc)
        _ov(im, lambda q: q.chord(S(400, 40, 610, 200), 180, 360, fill=(180, 230, 255, 150)))
        d.arc(S(400, 40, 610, 200), 180, 360, fill=INK + (255,), width=5 * sc)
        _ov(im, lambda q: q.line(S(90, 150, 660, 136), fill=(255, 255, 255, 60), width=6 * sc))
        return _done(im, w, h)
    return gcache("plane2", mk)


def prop_disc(f, x, y, r, t):
    ov = f.copy(); cv2.ellipse(ov, (int(x), int(y)), (int(r * 0.22), int(r)), 0, 0, 360, C((220, 224, 236)), -1, cv2.LINE_AA)
    f[:] = f * 0.75 + ov * 0.25
    a = t * 40
    for k in range(3):
        yy = y + r * math.sin(a + k * 2.094); cv2.line(f, (int(x), int(y)), (int(x + 6 * math.cos(a + k * 2.094)), int(yy)), C((40, 40, 46)), 8, cv2.LINE_AA)


def moon(f, x, y, r):
    glow(f, x, y, r * 1.6, (200, 210, 255), 0.25)
    cv2.circle(f, (int(x), int(y)), int(r), C((250, 248, 228)), -1, cv2.LINE_AA)
    for (dx, dy, rr) in ((-0.3, -0.2, 0.18), (0.25, 0.15, 0.12), (-0.05, 0.35, 0.1)):
        cv2.circle(f, (int(x + dx * r), int(y + dy * r)), int(rr * r), C((222, 220, 200)), -1, cv2.LINE_AA)
