# ================= props for "Visa never lends you a dollar" (generic payments props, no logos / trade dress) =================
ASPH = (58, 60, 72); LANE = (255, 222, 90); BOOTH = (255, 120, 60)


def card_el(top=(120, 60, 230), bot=(40, 190, 200), label="MY BANK", w=560, h=350, num="4821"):
    """generic payment card: gradient, chip, contactless waves, masked number — no network logo"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 16, w - 2, h - 2), 30 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 14, h - 16), 30 * sc, fill=255), top, bot)
        _ov(im, lambda q: q.polygon(S(w * 0.45, 0, w * 0.75, 0, w * 0.35, h - 16, w * 0.05, h - 16), fill=(255, 255, 255, 34)))
        d.rounded_rectangle(S(0, 0, w - 14, h - 16), 30 * sc, outline=INK + (255,), width=5 * sc)
        d.text((40 * sc, 54 * sc), label, font=font(F_BLACK, 40 * sc), fill=(255, 255, 255, 255), anchor="lm")
        d.rounded_rectangle(S(46, 110, 136, 176), 12 * sc, fill=(240, 200, 90, 255), outline=(150, 110, 30, 255), width=3 * sc)
        for yy in (132, 154): d.line(S(46, yy, 136, yy), fill=(150, 110, 30, 255), width=2 * sc)
        d.line(S(91, 110, 91, 176), fill=(150, 110, 30, 255), width=2 * sc)
        for i, r in enumerate((22, 38, 54)):
            d.arc(S(170 - r, 143 - r, 170 + r, 143 + r), -50, 50, fill=(255, 255, 255, 230), width=5 * sc)
        d.text((40 * sc, 236 * sc), "••••  ••••  ••••  " + num, font=font(F_BOLD, 34 * sc), fill=(255, 255, 255, 255), anchor="lm")
        d.text((40 * sc, 292 * sc), "YOU", font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 235), anchor="lm")
        return _done(im, w, h)
    return gcache(("card", top, bot, label, w, h, num), mk)


def tollbooth_el(w=330, h=500, sign="TOLL"):
    """generic toll booth: roof + sign, window, striped base"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(46, 130, w - 2, h - 2), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rectangle(S(30, 120, w - 46, h - 16), fill=255), (255, 255, 255), (220, 222, 232))
        d.rectangle(S(30, 120, w - 46, h - 16), outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(60, 170, w - 76, 300), 10 * sc, fill=(150, 210, 255, 255), outline=INK + (255,), width=5 * sc)
        _ov(im, lambda q: q.polygon(S(80, 170, 130, 170, 90, 300, 60, 300), fill=(255, 255, 255, 120)))
        for i in range(6):
            x0 = 30 + i * (w - 76) / 6
            if i % 2 == 0: d.rectangle(S(x0, h - 90, x0 + (w - 76) / 6, h - 16), fill=RED_ + (255,))
        d.rectangle(S(30, h - 90, w - 46, h - 16), outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(6, 40, w - 22, 128), 16 * sc, fill=BOOTH + (255,), outline=INK + (255,), width=5 * sc)
        d.text(((w - 16) / 2 * sc, 86 * sc), sign, font=font(F_BLACK, 62 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("booth", w, h, sign), mk)


def barrier(f, x, y, ang, L=360):
    """striped boom barrier pivoting at (x, y); ang 0 = horizontal pointing right, 80 = raised"""
    a = math.radians(-ang); ex, ey = x + L * math.cos(a), y + L * math.sin(a)
    cv2.line(f, (int(x), int(y)), (int(ex), int(ey)), C(INK), 34, cv2.LINE_AA)
    cv2.line(f, (int(x), int(y)), (int(ex), int(ey)), C(WHITE), 24, cv2.LINE_AA)
    for k_ in range(0, 6, 2):
        p0 = (x + L * (k_ / 6) * math.cos(a), y + L * (k_ / 6) * math.sin(a)); p1 = (x + L * ((k_ + 1) / 6) * math.cos(a), y + L * ((k_ + 1) / 6) * math.sin(a))
        cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(RED_), 24, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 30, C(GOLD), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 30, C(INK), 5, cv2.LINE_AA)


def road(f, y0, y1, t, speed=600.0, vertical=False):
    """asphalt band with moving dashed centre line"""
    if not vertical:
        f[int(y0):int(y1)] = np.array(C(ASPH), np.float32)
        cv2.line(f, (0, int(y0)), (W, int(y0)), C(INK), 8); cv2.line(f, (0, int(y1)), (W, int(y1)), C(INK), 8)
        yc = int((y0 + y1) / 2); off = (t * speed) % 160
        for x in np.arange(-160, W + 160, 160):
            cv2.line(f, (int(x + off), yc), (int(x + off + 80), yc), C(LANE), 12, cv2.LINE_AA)


def car_el(col=(60, 170, 255), w=300, h=170, cargo="$"):
    """side-view cartoon car carrying a money sign on its door"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(20, h - 30, w - 20, h - 4), fill=(0, 0, 0, 70)))
        dk = tuple(int(v * 0.75) for v in col)
        d.rounded_rectangle(S(70, 14, w - 80, 80), 24 * sc, fill=tuple(col) + (255,), outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(90, 26, w / 2 - 6, 70), 10 * sc, fill=(190, 230, 255, 255), outline=INK + (255,), width=3 * sc)
        d.rounded_rectangle(S(w / 2 + 6, 26, w - 100, 70), 10 * sc, fill=(190, 230, 255, 255), outline=INK + (255,), width=3 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 66, w - 10, 134), 26 * sc, fill=255), col, dk)
        d.rounded_rectangle(S(10, 66, w - 10, 134), 26 * sc, outline=INK + (255,), width=5 * sc)
        d.ellipse(S(w - 36, 82, w - 18, 100), fill=(255, 240, 160, 255))
        if cargo: d.text((w / 2 * sc, 100 * sc), cargo, font=font(F_BLACK, 50 * sc), fill=(255, 255, 255, 255), anchor="mm")
        for cx in (70, w - 70):
            d.ellipse(S(cx - 30, h - 66, cx + 30, h - 6), fill=INK + (255,)); d.ellipse(S(cx - 13, h - 49, cx + 13, h - 23), fill=(200, 200, 210, 255))
        return _done(im, w, h)
    return gcache(("car", col, w, h, cargo), mk)


def shop_el(col=(255, 90, 120), w=150, h=150):
    """tiny generic storefront with a striped awning"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(w * 0.08, h * 0.33, w - w * 0.08, h - 6), fill=(255, 250, 240, 255), outline=INK + (255,), width=4 * sc)
        for i in range(5):
            x0 = 6 + i * (w - 12) / 5
            d.rectangle(S(x0, h * 0.17, x0 + (w - 12) / 5, h * 0.4), fill=(tuple(col) if i % 2 == 0 else (255, 255, 255)) + (255,))
        d.rectangle(S(6, h * 0.17, w - 6, h * 0.4), outline=INK + (255,), width=4 * sc)
        d.rectangle(S(w / 2 - w * 0.12, h * 0.55, w / 2 + w * 0.12, h - 6), fill=(110, 70, 40, 255), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(w * 0.14, h * 0.5, w * 0.34, h * 0.72), fill=(160, 220, 255, 255), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(w * 0.66, h * 0.5, w * 0.86, h * 0.72), fill=(160, 220, 255, 255), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("shop", col, w, h), mk)


def terminal_el(w=300, h=480, screen="TAP", lit=False):
    """generic handheld card terminal with screen + keypad"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 16, w - 2, h - 2), 36 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 14, h - 16), 36 * sc, fill=255), (70, 74, 90), (34, 36, 46))
        d.rounded_rectangle(S(0, 0, w - 14, h - 16), 36 * sc, outline=INK + (255,), width=5 * sc)
        sc_col = (120, 255, 160) if lit else (190, 230, 255)
        d.rounded_rectangle(S(30, 34, w - 44, 200), 16 * sc, fill=sc_col + (255,), outline=INK + (255,), width=4 * sc)
        d.text(((w - 14) / 2 * sc, 117 * sc), screen, font=font(F_BLACK, 52 * sc), fill=INK + (255,), anchor="mm")
        for r in range(4):
            for c in range(3):
                x = 50 + c * (w - 114) / 2; y = 236 + r * 52
                d.rounded_rectangle(S(x - 26, y - 18, x + 26, y + 18), 9 * sc, fill=(230, 232, 240, 255) if (r, c) != (3, 2) else (60, 200, 100, 255))
        return _done(im, w, h)
    return gcache(("term", w, h, screen, lit), mk)


def odometer(f, cx, cy, text, k=1.0, cell=(96, 150), col=YEL_, seed=0):
    """rolling digit counter drawn straight on the frame; digits settle left-to-right as k goes 0..1"""
    n_ = len(text); cw, ch = cell; gap = 10; x0 = cx - (n_ * cw + (n_ - 1) * gap) / 2
    cv2.rectangle(f, (int(x0 - 26), int(cy - ch / 2 - 26)), (int(x0 + n_ * (cw + gap) - gap + 26), int(cy + ch / 2 + 26)), C(INK), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed)
    for i, c in enumerate(text):
        x = x0 + i * (cw + gap)
        if c in ",.":
            el = ed_el("", c, "", big_col=col, big_size=110, fp_big=F_BLACK, maxw=200)
            comp(f, el, x + cw / 2, cy + 8); continue
        cv2.rectangle(f, (int(x), int(cy - ch / 2)), (int(x + cw), int(cy + ch / 2)), C((250, 248, 240)), -1, cv2.LINE_AA)
        done = k >= (i + 1) / (n_ + 1)
        d_ = c if done or not c.isdigit() else str(int(rng.integers(0, 10) + k * 97 + i * 3) % 10)
        el = ed_el("", d_, "", big_col=INK, big_size=118, fp_big=F_BLACK, maxw=200)
        comp(f, el, x + cw / 2, cy + 2)
        cv2.line(f, (int(x), int(cy)), (int(x + cw), int(cy)), C((200, 200, 205)), 2)


def pie(f, cx, cy, r, frac, col_a, col_b, k=1.0, explode=0.0, start=-90):
    """pie chart drawn straight to the frame: slice a = frac (animated by k), pushed out by `explode` px"""
    a1 = start + 360 * frac * clamp(k)
    mid = math.radians((start + a1) / 2)
    ex, ey = explode * math.cos(mid), explode * math.sin(mid)
    m_ = np.zeros((H, W), np.float32); cv2.ellipse(m_, (int(cx + 12), int(cy + 16)), (r, r), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    f *= (1 - 0.3 * m_)[..., None]
    cv2.ellipse(f, (int(cx), int(cy)), (r, r), 0, a1, start + 360, C(col_b), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy)), (r, r), 0, a1, start + 360, C(INK), 6, cv2.LINE_AA)
    if a1 > start + 0.5:
        cv2.ellipse(f, (int(cx + ex), int(cy + ey)), (r, r), 0, start, a1, C(col_a), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(cx + ex), int(cy + ey)), (r, r), 0, start, a1, C(INK), 6, cv2.LINE_AA)
        for a in (start, a1):
            cv2.line(f, (int(cx + ex), int(cy + ey)), (int(cx + ex + r * math.cos(math.radians(a))), int(cy + ey + r * math.sin(math.radians(a)))), C(INK), 6, cv2.LINE_AA)
    return mid
