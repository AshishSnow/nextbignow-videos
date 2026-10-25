# ================= props for "Amazon's real money machine is AWS" (generic, no logos) =================
KRAFT = (214, 160, 100); RACK = (44, 48, 60); LED_G = (60, 230, 120); LED_B = (80, 170, 255)


def box_el(w=360, h=280, label=None):
    """plain cardboard parcel (3/4 view), tape strip, no marks"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        top = S(w * 0.08, h * 0.22, w * 0.30, h * 0.04, w * 0.98, h * 0.04, w * 0.76, h * 0.22)
        shape_grad(im, lambda m: m.polygon(top, fill=255), (236, 190, 130), (222, 172, 112))
        shape_grad(im, lambda m: m.rectangle(S(w * 0.08, h * 0.22, w * 0.76, h * 0.98), fill=255), KRAFT, (190, 136, 80))
        shape_grad(im, lambda m: m.polygon(S(w * 0.76, h * 0.22, w * 0.98, h * 0.04, w * 0.98, h * 0.80, w * 0.76, h * 0.98), fill=255),
                   (176, 124, 72), (150, 102, 56))
        d.polygon(S(w * 0.38, h * 0.22, w * 0.60, h * 0.04, w * 0.68, h * 0.04, w * 0.46, h * 0.22), fill=(240, 222, 190, 255))
        d.rectangle(S(w * 0.38, h * 0.22, w * 0.46, h * 0.55), fill=(240, 222, 190, 255))
        d.rectangle(S(w * 0.14, h * 0.66, w * 0.34, h * 0.88), fill=(255, 255, 255, 235))
        for i in range(3): d.line(S(w * 0.17, h * (0.71 + i * 0.05), w * 0.31, h * (0.71 + i * 0.05)), fill=(120, 120, 130, 255), width=2 * sc)
        if label: d.text((w * 0.42 * sc, h * 0.75 * sc), label, font=font(F_BLACK, int(h * 0.16) * sc), fill=(90, 56, 26, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("box", w, h, label), mk)


def rack_el(ph=0, w=230, h=520):
    """server rack with LED rows; ph picks the blink pattern"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(8, 10, w - 1, h - 1), 16 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 10, h - 10), 16 * sc, fill=255), (70, 76, 92), RACK)
        rng = np.random.default_rng(ph)
        for i in range(9):
            y = 24 + i * 54
            d.rounded_rectangle(S(18, y, w - 28, y + 42), 6 * sc, fill=(26, 28, 36, 255))
            for j in range(4):
                d.line(S(30 + j * 10, y + 10, 30 + j * 10, y + 32), fill=(70, 74, 88, 255), width=3 * sc)
            for j in range(3):
                on = rng.random() < 0.6
                col = (LED_G if j < 2 else LED_B) if on else (40, 60, 50)
                cx = w - 60 + j * 14
                d.ellipse(S(cx - 4, y + 17, cx + 4, y + 25), fill=tuple(col) + (255,))
        return _done(im, w, h)
    return gcache(("rack", ph % 4, w, h), mk)


def cloud_el(col=(255, 255, 255), w=520, h=300):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def blob(m):
            m.ellipse(S(w * 0.05, h * 0.42, w * 0.40, h * 0.95), fill=255); m.ellipse(S(w * 0.22, h * 0.12, w * 0.62, h * 0.85), fill=255)
            m.ellipse(S(w * 0.50, h * 0.28, w * 0.84, h * 0.90), fill=255); m.ellipse(S(w * 0.66, h * 0.50, w * 0.96, h * 0.95), fill=255)
            m.rounded_rectangle(S(w * 0.18, h * 0.6, w * 0.86, h * 0.95), int(h * 0.17) * sc, fill=255)
        shape_grad(im, blob, tuple(col), tuple(int(v * 0.86) for v in col))
        return _done(im, w, h)
    return gcache(("cloud", col, w, h), mk)


def building_el(col=(90, 120, 230), w=150, h=240):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rectangle(S(0, 0, w, h), fill=255), tuple(min(255, v + 30) for v in col), tuple(int(v * 0.72) for v in col))
        for r_ in range(int((h - 50) / 40)):
            for c_ in range(3):
                x = 18 + c_ * (w - 36) / 3; y = 20 + r_ * 40
                d.rectangle(S(x, y, x + (w - 36) / 3 - 12, y + 24), fill=(255, 244, 190, 255) if (r_ + c_) % 3 else (210, 230, 255, 255))
        d.rectangle(S(w / 2 - 18, h - 46, w / 2 + 18, h), fill=(40, 40, 50, 255))
        return _done(im, w, h)
    return gcache(("bld", col, w, h), mk)


def search_phone_el(k=3):
    """phone with a search bar and k results, first two marked SPONSORED"""
    def mk():
        w, h, sc = 440, 800, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, h - 1), 60 * sc, fill=(24, 24, 30, 255))
        shape_grad(im, lambda m: m.rounded_rectangle(S(18, 18, w - 18, h - 18), 46 * sc, fill=255), (252, 250, 246), (238, 234, 226))
        d.rounded_rectangle(S(160, 30, 280, 54), 12 * sc, fill=(24, 24, 30, 255))
        d.rounded_rectangle(S(40, 84, 400, 150), 33 * sc, fill=(255, 255, 255, 255), outline=(200, 204, 214, 255), width=3 * sc)
        d.ellipse(S(62, 102, 92, 132), outline=(120, 124, 136, 255), width=4 * sc); d.line(S(88, 128, 100, 140), fill=(120, 124, 136, 255), width=4 * sc)
        d.text((116 * sc, 117 * sc), "headphones", font=font(F_SEMI, 28 * sc), fill=INK + (255,), anchor="lm")
        cols = [(255, 120, 80), (90, 150, 255), (60, 200, 140)]
        for i in range(k):
            y = 180 + i * 190
            d.rounded_rectangle(S(40, y, 400, y + 170), 22 * sc, fill=(255, 255, 255, 255), outline=(222, 224, 232, 255), width=2 * sc)
            d.rounded_rectangle(S(58, y + 18, 178, y + 152), 16 * sc, fill=tuple(cols[i]) + (255,))
            d.arc(S(84, y + 40, 152, y + 120), 180, 360, fill=(255, 255, 255, 255), width=10 * sc)
            d.rounded_rectangle(S(76, y + 82, 98, y + 124), 8 * sc, fill=(255, 255, 255, 255)); d.rounded_rectangle(S(138, y + 82, 160, y + 124), 8 * sc, fill=(255, 255, 255, 255))
            for j, ww in enumerate((190, 150, 110)): d.rounded_rectangle(S(198, y + 30 + j * 30, 198 + ww, y + 46 + j * 30), 8 * sc, fill=(214, 216, 224, 255))
            if i < 2:
                d.rounded_rectangle(S(198, y + 118, 360, y + 150), 10 * sc, fill=(255, 210, 60, 255))
                d.text((279 * sc, 134 * sc + y * sc), "SPONSORED", font=font(F_BLACK, 20 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("sphone", k), mk)


def cents_grid(f, cx, cy, lit, col, cell=44, gap=8, k=1.0, dim=(255, 255, 255)):
    """10x10 grid = one dollar in cents; the first `lit` cells glow in col (k animates fill 0..1)"""
    n_on = int(round(lit * clamp(k)))
    s = cell + gap; x0 = cx - 5 * s + gap / 2; y0 = cy - 5 * s + gap / 2
    for i in range(100):
        r_, c_ = divmod(i, 10); x = int(x0 + c_ * s); y = int(y0 + (9 - r_) * s)
        on = i < n_on
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(col if on else dim), -1, cv2.LINE_AA)
        if on: cv2.rectangle(f, (x, y), (x + cell, y + cell), C(INK), 3, cv2.LINE_AA)
