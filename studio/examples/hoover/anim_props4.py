# ================= props for "Hoover's free flights" (generic: no real logos, no real product designs) =================
VAC = (214, 40, 52); VAC_D = (150, 22, 34); BAGC = (232, 226, 214); CARTON = (204, 160, 104); CARTON_D = (160, 116, 66)
TICK = (250, 246, 232); TICK_B = (40, 110, 220)


def vacuum_el(w=300, col=VAC, bag=BAGC):
    """generic upright vacuum cleaner (handle, cloth bag, motor base, wheels); facing right"""
    def mk():
        sc = 2; h = int(w * 2.6); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cx = w * 0.5
        # handle + grip
        d.rounded_rectangle(S(cx - 9, 10, cx + 9, h * 0.26), 8 * sc, fill=(60, 60, 70, 255))
        d.rounded_rectangle(S(cx - 46, 4, cx + 46, 46), 20 * sc, fill=(40, 40, 48, 255), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(cx - 30, 14, cx + 30, 36), 10 * sc, fill=(230, 230, 236, 255))
        # cloth bag
        bag_box = S(cx - w * 0.30, h * 0.22, cx + w * 0.30, h * 0.70)
        _ov(im, lambda q: q.rounded_rectangle(S(cx - w * 0.30 + 10, h * 0.22 + 10, cx + w * 0.30 + 10, h * 0.70 + 10), 46 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(bag_box, 46 * sc, fill=255), tuple(min(255, c + 16) for c in bag), tuple(int(c * 0.82) for c in bag))
        d.rounded_rectangle(bag_box, 46 * sc, outline=INK + (255,), width=5 * sc)
        for k in range(1, 5):                                   # stitched seams
            y = h * (0.22 + 0.48 * k / 5)
            d.line(S(cx - w * 0.26, y, cx + w * 0.26, y), fill=(190, 182, 166, 255), width=2 * sc)
        d.rounded_rectangle(S(cx - w * 0.2, h * 0.36, cx + w * 0.2, h * 0.46), 10 * sc, fill=tuple(col) + (255,), outline=INK + (255,), width=3 * sc)
        # neck
        d.rectangle(S(cx - 22, h * 0.69, cx + 22, h * 0.78), fill=(70, 70, 80, 255), outline=INK + (255,), width=3 * sc)
        # motor base
        base = S(w * 0.06, h * 0.76, w * 0.97, h * 0.76, w * 0.97, h * 0.93, w * 0.03, h * 0.93)
        shape_grad(im, lambda m: m.rounded_rectangle(S(w * 0.04, h * 0.76, w * 0.98, h * 0.93), 34 * sc, fill=255),
                   tuple(min(255, c + 40) for c in col), tuple(int(c * 0.7) for c in col))
        d.rounded_rectangle(S(w * 0.04, h * 0.76, w * 0.98, h * 0.93), 34 * sc, outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(w * 0.6, h * 0.79, w * 0.9, h * 0.83), 8 * sc, fill=(255, 236, 160, 255))        # headlight strip
        d.line(S(w * 0.1, h * 0.79, w * 0.45, h * 0.79), fill=(255, 255, 255, 120), width=4 * sc)
        for x in (w * 0.2, w * 0.82):                                                                          # wheels
            d.ellipse(S(x - 26, h * 0.9, x + 26, h * 0.9 + 52), fill=(30, 30, 36, 255)); d.ellipse(S(x - 10, h * 0.9 + 16, x + 10, h * 0.9 + 36), fill=(170, 170, 180, 255))
        return _done(im, w, h)
    return gcache(("vacuum", w, col, bag), mk)


def wing_el(w=380, col=(255, 255, 255)):
    """feathered wing spreading to the left from a root at the right edge (flip for the right wing)"""
    def mk():
        sc = 2; h = int(w * 0.9); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rx, ry = w - 40, h * 0.68
        for k in range(7, -1, -1):                      # primaries (long, lower) -> coverts (short, upper)
            a = math.radians(166 + k * 7.5); L = w * (0.92 - 0.06 * k)
            tx, ty = rx + L * math.cos(a), ry + L * math.sin(a)
            wd = 44 - k * 2
            shade = tuple(int(c * (0.80 + 0.025 * k)) for c in col)
            d.line(S(rx, ry, tx, ty), fill=(150, 160, 186, 255), width=int((wd + 6) * sc))
            d.line(S(rx, ry, tx, ty), fill=shade + (255,), width=int(wd * sc))
            d.ellipse(S(tx - wd / 2 - 3, ty - wd / 2 - 3, tx + wd / 2 + 3, ty + wd / 2 + 3), fill=(150, 160, 186, 255))
            d.ellipse(S(tx - wd / 2, ty - wd / 2, tx + wd / 2, ty + wd / 2), fill=shade + (255,))
        d.ellipse(S(rx - 90, ry - 50, rx + 30, ry + 40), fill=tuple(col) + (255,), outline=(150, 160, 186, 255), width=3 * sc)
        return _done(im, w, h)
    return gcache(("wing3", w, col), mk)


def sky_bg(t):
    """open sky (no ground): deep blue top, bright horizon haze, sun glow, drifting clouds at three depths"""
    def mk():
        f = np.zeros((H, W, 3), np.float32)
        k = (_yy / H)[..., None]
        f[:] = _mix(_c((26, 92, 210)), _c((150, 206, 252)), k ** 0.8)
        _sglow(f, 860, 360, 520, (255, 240, 200), 0.55)
        return f
    f = gcache("skybg", mk).copy()
    for y0, sp, op in ((260, 20, 0.94), (1180, 46, 1.0)):
        clouds(f, t, y0, sp, op)
    return f


def winged_vacuum(f, x, y, s, t, flap=1.0, tilt=0.0):
    """vacuum with two flapping wings (the hook object)"""
    wv = scale_el(vacuum_el(300), s); wg = scale_el(wing_el(380), s)
    a = 18 * math.sin(t * 9) * flap
    wl = wg; wr = (wg[0][:, ::-1].copy(), wg[1][:, ::-1].copy())
    rot_comp(f, wl, x - 190 * s, y - 230 * s, -a + tilt, 1.0, 1.0, 0.2)
    rot_comp(f, wv, x, y, tilt, 1.0, 1.0, 0.35)
    rot_comp(f, wr, x + 190 * s, y - 230 * s, a + tilt, 1.0, 1.0, 0.2)


def ticket_el(dest="NEW YORK", w=420, top="FREE RETURN FLIGHT", col=TICK_B):
    """paper airline ticket with a perforated stub (generic, no airline)"""
    def mk():
        sc = 2; h = int(w * 0.46); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(8, 10, w, h), 18 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 8, h - 10), 18 * sc, fill=255), (255, 252, 240), (238, 230, 206))
        d.rounded_rectangle(S(0, 0, w - 8, h - 10), 18 * sc, outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(0, 0, w - 8, h * 0.3), 18 * sc, fill=tuple(col) + (255,)); d.rectangle(S(0, h * 0.18, w - 8, h * 0.3), fill=tuple(col) + (255,))
        fn = font(F_BLACK, 26 * sc)
        while fn.getlength(top) / sc > w * 0.62: fn = font(F_BLACK, int(fn.size / sc - 2) * sc)
        d.text((w * 0.38 * sc, h * 0.15 * sc), top, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        d.text((w * 0.38 * sc, h * 0.47 * sc), "TO", font=font(F_BOLD, 20 * sc), fill=(120, 110, 96, 255), anchor="mm")
        fd = font(F_BLACK, 46 * sc)
        while fd.getlength(dest) / sc > w * 0.66: fd = font(F_BLACK, int(fd.size / sc - 3) * sc)
        d.text((w * 0.38 * sc, h * 0.66 * sc), dest, font=fd, fill=INK + (255,), anchor="mm")
        for y in range(10, int(h - 16), 14): d.line(S(w * 0.76, y, w * 0.76, y + 7), fill=(120, 110, 96, 255), width=3 * sc)
        # tiny plane on the stub
        px, py = w * 0.87, h * 0.58
        d.polygon(S(px - 34, py, px + 30, py - 4, px + 36, py + 2, px - 30, py + 8), fill=tuple(col) + (255,))
        d.polygon(S(px - 6, py, px + 8, py - 30, px + 16, py - 28, px + 8, py + 2), fill=tuple(col) + (255,))
        d.polygon(S(px - 6, py + 4, px + 8, py + 34, px + 16, py + 32, px + 8, py + 4), fill=tuple(col) + (255,))
        return _done(im, w, h)
    return gcache(("ticket", dest, w, top, col), mk)


def carton_el(w=300, label="VACUUM", col=CARTON):
    """cardboard appliance box with a plain printed label (no brand art)"""
    def mk():
        sc = 2; h = int(w * 1.25); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.polygon(S(4, h * 0.14, w * 0.78, h * 0.14, w * 0.78, h - 4, 4, h - 4), fill=255), tuple(min(255, c + 20) for c in col), col)
        d.polygon(S(4, h * 0.14, w * 0.78, h * 0.14, w * 0.78, h - 4, 4, h - 4), outline=INK + (255,), width=4 * sc)
        d.polygon(S(4, h * 0.14, w * 0.22, 4, w - 4, 4, w * 0.78, h * 0.14), fill=tuple(min(255, c + 34) for c in col) + (255,), outline=INK + (255,), width=4 * sc)
        d.polygon(S(w * 0.78, h * 0.14, w - 4, 4, w - 4, h * 0.86, w * 0.78, h - 4), fill=CARTON_D + (255,), outline=INK + (255,), width=4 * sc)
        d.rectangle(S(w * 0.33, h * 0.14, w * 0.47, h - 4), fill=(190, 150, 96, 160))                  # tape
        d.rounded_rectangle(S(w * 0.1, h * 0.42, w * 0.7, h * 0.62), 8 * sc, fill=(255, 255, 255, 235), outline=INK + (255,), width=3 * sc)
        fn = font(F_BLACK, 34 * sc)
        while fn.getlength(label) / sc > w * 0.54: fn = font(F_BLACK, int(fn.size / sc - 2) * sc)
        d.text((w * 0.4 * sc, h * 0.52 * sc), label, font=fn, fill=VAC_D + (255,), anchor="mm")
        d.text((w * 0.4 * sc, h * 0.75 * sc), "THIS WAY UP", font=font(F_BOLD, 18 * sc), fill=(90, 60, 30, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("carton", w, label, col), mk)


def ad_poster_el(head, big, sub, w=620, h=820, col=(36, 70, 170)):
    """bright 1990s shop-window promo poster (generic)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(10, 12, w, h), fill=(0, 0, 0, 80))
        shape_grad(im, lambda m: m.rectangle(S(0, 0, w - 10, h - 12), fill=255), tuple(min(255, c + 50) for c in col), col)
        d.rectangle(S(0, 0, w - 10, h - 12), outline=(255, 255, 255, 255), width=10 * sc)
        for i in range(16):                                               # starburst
            a = i * math.pi / 8; cx, cy = w * 0.5, h * 0.52
            d.polygon(S(cx, cy, cx + 600 * math.cos(a - 0.08), cy + 600 * math.sin(a - 0.08), cx + 600 * math.cos(a + 0.08), cy + 600 * math.sin(a + 0.08)), fill=(255, 255, 255, 26))
        y = 70
        for text, size, colr in ((head, 58, (255, 255, 255)), (big, 150, YEL_), (sub, 56, (255, 255, 255))):
            fn = font(F_BLACK, size * sc)
            while fn.getlength(text) / sc > w - 90 and size > 20: size -= 4; fn = font(F_BLACK, size * sc)
            d.text((w / 2 * sc, (y + size * 0.6) * sc), text, font=fn, fill=tuple(colr) + (255,), anchor="mm", stroke_width=4 * sc if size > 100 else 0, stroke_fill=INK + (255,))
            y += size * 1.35 + 30
        d.rounded_rectangle(S(w * 0.18, h - 140, w * 0.82, h - 70), 30 * sc, fill=(232, 32, 40, 255))
        d.text((w / 2 * sc, (h - 105) * sc), "*CONDITIONS APPLY", font=font(F_BOLD, 26 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("adposter", head, big, sub, w, h, col), mk)


def form_el(w=380, title="CLAIM FORM", stamp=None):
    """paper form with lines (claims, deadlines)"""
    def mk():
        sc = 2; h = int(w * 1.3); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(8, 10, w, h), fill=(0, 0, 0, 60))
        shape_grad(im, lambda m: m.rectangle(S(0, 0, w - 8, h - 10), fill=255), (255, 255, 252), (234, 232, 224))
        d.rectangle(S(0, 0, w - 8, h - 10), outline=(150, 150, 160, 255), width=2 * sc)
        d.text((w / 2 * sc, 46 * sc), title, font=font(F_BLACK, 34 * sc), fill=INK + (255,), anchor="mm")
        for k in range(9):
            y = 100 + k * (h - 170) / 9
            d.line(S(40, y, w - 50, y), fill=(170, 170, 184, 255), width=2 * sc)
            d.rectangle(S(40, y - 26, 40 + 60 + (k * 37) % 120, y - 12), fill=(200, 200, 210, 255))
        return _done(im, w, h)
    return gcache(("form", w, title, stamp), mk)


def pin_el(label, col=RED_):
    """map pin with a label pill"""
    def mk():
        fn = font(F_BLACK, 40 * 2); tw = fn.getlength(label) / 2
        w = int(max(120, tw + 50)); h = 210; sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, 64), 30 * sc, fill=INK + (240,))
        d.text((w / 2 * sc, 33 * sc), label, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        cx = w / 2; d.ellipse(S(cx - 36, 80, cx + 36, 152), fill=tuple(col) + (255,), outline=INK + (255,), width=4 * sc)
        d.polygon(S(cx - 30, 132, cx + 30, 132, cx, 206), fill=tuple(col) + (255,), outline=INK + (255,))
        d.ellipse(S(cx - 13, 103, cx + 13, 129), fill=(255, 255, 255, 255))
        return _done(im, w, h)
    return gcache(("pin", label, col), mk)


def atlantic(f, k, t, cx=540, cy=1050):
    """stylised ocean map: Britain on the right, America on the left (blob coasts), dotted flight arc drawn by k"""
    sea = np.array(C((40, 120, 200)), np.float32)
    m = np.exp(-(((_xx - cx) / 470) ** 2 + ((_yy - cy) / 420) ** 4))[..., None]
    f[:] = f * (1 - m * 0.92) + sea * m * 0.92
    for i in range(7):                                              # wave lines
        y = cy - 300 + i * 100; ph = t * 1.2 + i
        pts = np.array([[x, y + 8 * math.sin(x / 40 + ph)] for x in range(cx - 360, cx + 360, 12)], np.int32)
        cv2.polylines(f, [pts], False, C((90, 170, 236)), 3, cv2.LINE_AA)
    land = C((96, 186, 96)); edge = C((40, 90, 50))
    us = np.array([[cx - 470, cy - 380], [cx - 300, cy - 360], [cx - 250, cy - 200], [cx - 290, cy - 40], [cx - 250, cy + 120], [cx - 330, cy + 260], [cx - 470, cy + 330]], np.int32)
    uk = np.array([[cx + 300, cy - 300], [cx + 360, cy - 330], [cx + 380, cy - 220], [cx + 350, cy - 120], [cx + 390, cy - 40], [cx + 330, cy - 10], [cx + 290, cy - 120]], np.int32)
    eu = np.array([[cx + 430, cy - 60], [cx + 470, cy - 80], [cx + 470, cy + 260], [cx + 420, cy + 200], [cx + 440, cy + 60]], np.int32)
    for poly in (us, uk, eu):
        cv2.fillPoly(f, [poly], land, cv2.LINE_AA); cv2.polylines(f, [poly], True, edge, 5, cv2.LINE_AA)
    p0, p1 = (cx + 330, cy - 160), (cx - 300, cy - 120)
    n_ = 30
    for i in range(int(n_ * clamp(k))):
        u = i / n_; x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u - 260 * math.sin(math.pi * u)
        cv2.circle(f, (int(x), int(y)), 7, C((255, 255, 255)), -1, cv2.LINE_AA)
    if k > 0:
        u = clamp(k); x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u - 260 * math.sin(math.pi * u)
        ang = math.degrees(math.atan2(-(260 * math.pi * math.cos(math.pi * u)) + (p1[1] - p0[1]), p1[0] - p0[0]))
        el = scale_el(plane_el(420), 0.5); el = (el[0][:, ::-1].copy(), el[1][:, ::-1].copy())
        rot_comp(f, el, x, y, -(ang - 180), 1.0, 1.0, 0.3)


# ---------------- airport departure hall (full-frame set) ----------------
def _airport_base():
    f = np.zeros((H, W, 3), np.float32)
    _srect(f, 0, 0, W, 1180, (150, 196, 240), (230, 236, 246))                 # sky through the glass wall
    m, win = _skyline(17, 60, 170)
    city = _c((150, 176, 210)); mm = (cv2.GaussianBlur(m, (0, 0), 2) * (_yy < 900) * (_yy > 600))[..., None]
    f[:] = _mix(f, city, mm * 0.6)
    _srect(f, 0, 860, W, 980, (120, 124, 134), (96, 100, 110))                   # apron
    for x in range(-40, W, 160): cv2.line(f, (x, 930), (x + 90, 930), _scv((250, 220, 80)), 5, cv2.LINE_AA)
    comp(f, plane_el(980), 560, 760)
    for x in range(0, W + 1, 270): cv2.line(f, (x, 0), (x, 1180), _scv((60, 66, 78)), 16, cv2.LINE_AA)   # mullions
    for y in (300, 620): cv2.line(f, (0, y), (W, y), _scv((60, 66, 78)), 10, cv2.LINE_AA)
    _srect(f, 0, 980, W, 1180, (226, 222, 214), (206, 200, 190), (90, 90, 96), 2)  # check-in desks
    for x0 in (40, 400, 760):
        _srect(f, x0, 1000, x0 + 280, 1180, (64, 92, 150), (44, 66, 116), (30, 30, 40), 3)
        _srect(f, x0 + 30, 1030, x0 + 250, 1070, (250, 250, 246), (230, 230, 224))
    f[1180:] = 0; _sfloor(f, 1180, 540, (236, 236, 240), (176, 180, 190), line_col=(160, 164, 176))
    _sglow(f, 540, 400, 700, (255, 250, 236), 0.2)
    _atmos(f, "airport")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


_set_base_prev = _set_base


def _set_base(name):   # noqa: F811 — adds the airport set, everything else unchanged
    return _airport_base() if name == "airport" else _set_base_prev(name)


_FLOOR["airport"] = 1180; SET_LIGHT["airport"] = "day"


# cheque with a year argument (props3 version prints 2025)
def cheque_el(payer, payee, amount, words, memo, w=860, h=400, year="2025"):
    """big novelty cheque"""
    key = ("chq", payer, payee, amount, words, memo, w, h, year)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 18, w - 2, h - 2), 22 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 16, h - 16), 22 * sc, fill=255), (236, 250, 240), (200, 236, 214))
        d.rounded_rectangle(S(2, 2, w - 16, h - 16), 22 * sc, outline=INK + (255,), width=6 * sc)
        d.text((34 * sc, 46 * sc), payer, font=font(F_BLACK, 32 * sc), fill=INK + (255,), anchor="lm")
        d.text(((w - 50) * sc, 46 * sc), year, font=font(F_BLACK, 28 * sc), fill=(90, 110, 100, 255), anchor="rm")
        d.text((34 * sc, 120 * sc), "PAY TO", font=font(F_BLACK, 24 * sc), fill=(90, 110, 100, 255), anchor="lm")
        d.text((150 * sc, 118 * sc), payee, font=font(F_BLACK, 52 * sc), fill=NAVY_ + (255,), anchor="lm")
        d.line(S(150, 148, w - 300, 148), fill=INK + (255,), width=3 * sc)
        d.rounded_rectangle(S(w - 280, 86, w - 40, 152), 10 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        d.text(((w - 160) * sc, 120 * sc), amount, font=font(F_BLACK, 32 * sc), fill=RED_ + (255,), anchor="mm")
        d.text((34 * sc, 200 * sc), words, font=font(F_BLACK, 30 * sc), fill=INK + (255,), anchor="lm")
        d.line(S(34, 226, w - 40, 226), fill=INK + (255,), width=3 * sc)
        d.text((34 * sc, (h - 70) * sc), "MEMO: " + memo, font=font(F_BLACK, 24 * sc), fill=(90, 110, 100, 255), anchor="lm")
        pts = [(w - 330 + i * 14, h - 74 + 16 * math.sin(i * 1.3)) for i in range(20)]
        d.line([(x * sc, y * sc) for x, y in pts], fill=NAVY_ + (255,), width=4 * sc)
        d.line(S(w - 340, h - 50, w - 50, h - 50), fill=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(key, mk)


