# ================= props for "Closed every Sunday, still winning" (generic, no logos / trade dress) =================
AWN1 = (20, 150, 140); AWN2 = (250, 246, 236); BRICK = (196, 104, 70); BUN = (232, 162, 70); FRY = (214, 140, 52)
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def store_el(sign=None, w=560, h=520, sepia=False):
    """generic little restaurant: striped teal awning, big windows, door; optional hanging door sign (OPEN/CLOSED)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(18, 70, w - 4, h - 2), 18 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 60, w - 14, h - 12), 18 * sc, fill=255), (250, 240, 222), (226, 210, 186))
        d.rectangle(S(10, h - 70, w - 14, h - 12), fill=BRICK + (255,))
        for i in range(8): d.line(S(10 + i * 70, h - 70, 10 + i * 70, h - 12), fill=(170, 84, 56, 255), width=3 * sc)
        d.line(S(10, h - 41, w - 14, h - 41), fill=(170, 84, 56, 255), width=3 * sc)
        d.rounded_rectangle(S(0, 0, w - 4, 70), 14 * sc, fill=(60, 64, 76, 255))
        for i in range(9):
            x0 = i * (w - 4) / 9
            col = AWN1 if i % 2 == 0 else AWN2
            d.polygon(S(x0, 70, x0 + (w - 4) / 9, 70, x0 + (w - 4) / 9, 150, x0 + (w - 4) / 18, 168, x0, 150), fill=col + (255,))
        for x0 in (40, w - 214):
            shape_grad(im, lambda m, x0=x0: m.rounded_rectangle(S(x0, 200, x0 + 170, 380), 12 * sc, fill=255), (170, 220, 255), (90, 160, 230))
            d.rounded_rectangle(S(x0, 200, x0 + 170, 380), 12 * sc, outline=(60, 64, 76, 255), width=6 * sc)
            d.line(S(x0 + 85, 200, x0 + 85, 380), fill=(60, 64, 76, 255), width=5 * sc)
            _ov(im, lambda q, x0=x0: q.polygon(S(x0 + 20, 370, x0 + 70, 210, x0 + 100, 210, x0 + 50, 370), fill=(255, 255, 255, 70)))
        dx = w / 2 - 70
        d.rounded_rectangle(S(dx, 220, dx + 140, h - 70), 10 * sc, fill=(120, 72, 40, 255), outline=(60, 40, 24, 255), width=5 * sc)
        d.rounded_rectangle(S(dx + 22, 240, dx + 118, 330), 8 * sc, fill=(170, 220, 255, 255))
        d.ellipse(S(dx + 110, 350, dx + 126, 366), fill=GOLD + (255,))
        if sign:
            col = RED_ if sign == "CLOSED" else GRN_
            d.line(S(w / 2 - 40, 236, w / 2, 214), fill=(60, 60, 60, 255), width=3 * sc); d.line(S(w / 2 + 40, 236, w / 2, 214), fill=(60, 60, 60, 255), width=3 * sc)
            d.rounded_rectangle(S(w / 2 - 66, 234, w / 2 + 66, 296), 10 * sc, fill=col + (255,), outline=(255, 255, 255, 255), width=4 * sc)
            d.text((w / 2 * sc, 265 * sc), sign, font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
        if sepia:
            a = im.getchannel("A"); g = im.convert("L")
            im = Image.merge("RGB", [g.point(lambda v: min(255, int(v * 1.08 + 20))), g.point(lambda v: int(v * 0.92 + 10)), g.point(lambda v: int(v * 0.7))]).convert("RGBA")
            im.putalpha(a)
        return _done(im, w, h)
    return gcache(("store", sign, w, h, sepia), mk)


def mini_store_el(col=AWN1, w=96, h=90):
    """tiny store icon for unit grids"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(6, 26, w - 6, h - 4), 8 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        d.polygon(S(0, 30, w / 2, 2, w, 30), fill=tuple(col) + (255,), outline=INK + (255,))
        d.rounded_rectangle(S(w / 2 - 12, h - 36, w / 2 + 12, h - 6), 4 * sc, fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("mstore", col, w, h), mk)


def week_el(lit=6, label="CLOSED", w=900, h=200):
    """7 day tiles MON..SUN; tile `lit` gets a red label"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        tw = (w - 6 * 12) / 7
        for i, dn in enumerate(DAYS):
            x0 = i * (tw + 12)
            _ov(im, lambda q, x0=x0: q.rounded_rectangle(S(x0 + 5, 12, x0 + tw + 5, h - 2), 16 * sc, fill=(0, 0, 0, 60)))
            off = i == lit
            d.rounded_rectangle(S(x0, 4, x0 + tw, h - 10), 16 * sc, fill=(255, 255, 255, 255) if not off else (40, 40, 48, 255))
            d.rounded_rectangle(S(x0, 4, x0 + tw, 60), 16 * sc, fill=(RED_ if off else NAVY_) + (255,)); d.rectangle(S(x0, 40, x0 + tw, 60), fill=(RED_ if off else NAVY_) + (255,))
            d.text(((x0 + tw / 2) * sc, 32 * sc), dn, font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
            if off:
                d.text(((x0 + tw / 2) * sc, 125 * sc), "X", font=font(F_BLACK, 80 * sc), fill=RED_ + (255,), anchor="mm")
            else:
                d.ellipse(S(x0 + tw / 2 - 26, 99, x0 + tw / 2 + 26, 151), fill=GRN_ + (255,))
                d.line(S(x0 + tw / 2 - 13, 125, x0 + tw / 2 - 3, 137, x0 + tw / 2 + 14, 112), fill=(255, 255, 255, 255), width=7 * sc)
        return _done(im, w, h)
    return gcache(("week", lit, label, w, h), mk)


def padlock_el(w=200, h=250):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.arc(S(40, 10, w - 40, 170), 180, 360, fill=(170, 176, 190, 255), width=26 * sc)
        d.line(S(53, 90, 53, 130), fill=(170, 176, 190, 255), width=26 * sc); d.line(S(w - 53, 90, w - 53, 130), fill=(170, 176, 190, 255), width=26 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(14, 110, w - 14, h - 6), 26 * sc, fill=255), (255, 214, 80), (214, 150, 20))
        d.ellipse(S(w / 2 - 20, 150, w / 2 + 20, 190), fill=INK + (255,)); d.rectangle(S(w / 2 - 8, 180, w / 2 + 8, 216), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("lock", w, h), mk)


def sandwich_el(w=380, h=280):
    """generic chicken sandwich: bun, crispy fillet, two pickles"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(30, h - 46, w - 30, h - 6), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(30, 190, w - 30, h - 24), 30 * sc, fill=255), BUN, (196, 120, 40))
        pts = []
        for i in range(25):
            x = 10 + i * (w - 20) / 24; pts += [x, 150 + (10 if i % 2 else 0)]
        shape_grad(im, lambda m: m.polygon(S(*pts) + S(w - 10, 210, 10, 210), fill=255), (240, 176, 80), FRY)
        for x in (110, 230):
            d.ellipse(S(x, 128, x + 70, 156), fill=(110, 170, 60, 255), outline=(70, 120, 30, 255), width=3 * sc)
        shape_grad(im, lambda m: m.chord(S(26, 10, w - 26, 280), 180, 360, fill=255), (250, 190, 90), (214, 130, 40))
        for i in range(9):
            x = 80 + (i * 37) % 220; y = 50 + (i * 23) % 60
            d.ellipse(S(x, y, x + 14, y + 7), fill=(255, 246, 220, 255))
        return _done(im, w, h)
    return gcache(("sand", w, h), mk)


def podium_el(labels=("2", "1", "3"), w=760, h=420, hi=2):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        hs = (260, 360, 200); cw = (w - 20) / 3
        cols = [(200, 206, 220), (255, 206, 60), (214, 140, 80)]
        for i in range(3):
            x0 = 10 + i * cw; y0 = h - hs[i]
            shape_grad(im, lambda m, x0=x0, y0=y0: m.rectangle(S(x0, y0, x0 + cw - 6, h), fill=255),
                       tuple(min(255, c + 30) for c in cols[i]), cols[i])
            d.rectangle(S(x0, y0, x0 + cw - 6, h), outline=INK + (255,), width=5 * sc)
            d.text(((x0 + cw / 2) * sc, (y0 + 70) * sc), labels[i], font=font(F_BLACK, 90 * sc), fill=(INK if i != hi else RED_) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("podium", labels, w, h, hi), mk)


def car_el(col=(240, 80, 70), w=200, h=120):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 44, w - 4, h - 26), 22 * sc, fill=255), tuple(min(255, c + 30) for c in col), tuple(int(c * 0.75) for c in col))
        shape_grad(im, lambda m: m.rounded_rectangle(S(44, 8, w - 50, 60), 20 * sc, fill=255), tuple(min(255, c + 30) for c in col), col)
        d.rounded_rectangle(S(58, 18, w / 2 - 4, 50), 8 * sc, fill=(190, 230, 255, 255)); d.rounded_rectangle(S(w / 2 + 4, 18, w - 64, 50), 8 * sc, fill=(190, 230, 255, 255))
        for x in (46, w - 46):
            d.ellipse(S(x - 24, h - 50, x + 24, h - 2), fill=INK + (255,)); d.ellipse(S(x - 10, h - 36, x + 10, h - 16), fill=(180, 184, 196, 255))
        d.ellipse(S(w - 18, 60, w - 4, 74), fill=(255, 240, 150, 255))
        return _done(im, w, h)
    return gcache(("car", col, w, h), mk)


def bundle_el(w=300, h=64):
    """one flat cash bundle (side view) for stacks"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 4, w, h - 4), 8 * sc, fill=255), (130, 216, 130), (60, 150, 70))
        for i in range(5): d.line(S(8, 14 + i * 9, w - 8, 14 + i * 9), fill=(40, 120, 56, 255), width=2 * sc)
        d.rectangle(S(w / 2 - 34, 4, w / 2 + 34, h - 4), fill=(255, 236, 160, 255))
        d.text((w / 2 * sc, h / 2 * sc), "$1M", font=font(F_BLACK, 26 * sc), fill=(60, 90, 40, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("bundle", w, h), mk)


def key_el(w=320, h=140):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: (m.ellipse(S(4, 10, 124, 130), fill=255), m.rectangle(S(110, 56, w - 10, 84), fill=255),
                                  m.rectangle(S(w - 70, 84, w - 50, 116), fill=255), m.rectangle(S(w - 34, 84, w - 12, 108), fill=255)),
                   (255, 220, 100), (206, 146, 20))
        d.ellipse(S(40, 46, 88, 94), fill=(0, 0, 0, 0))
        return _done(im, w, h)
    return gcache(("key", w, h), mk)


def hammock_scene(f, x, y, t, s=1.0):
    """two posts + hammock curve with the mascot lying in it (eyes closed)"""
    ink = C(INK)
    for px in (x - 300 * s, x + 300 * s):
        cv2.line(f, (int(px), int(y - 260 * s)), (int(px), int(y + 60 * s)), C((120, 80, 50)), int(22 * s), cv2.LINE_AA)
    sw = 14 * math.sin(t * 2.2)
    pts = [(x - 300 * s + i * 600 * s / 30, y - 230 * s + 150 * s * math.sin(math.pi * i / 30) + sw * math.sin(math.pi * i / 30)) for i in range(31)]
    for a, b in zip(pts[:-1], pts[1:]): cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C((255, 120, 60)), int(26 * s), cv2.LINE_AA)
    mid = pts[15]
    # lying body
    cv2.line(f, (int(mid[0] - 140 * s), int(mid[1] - 30 * s)), (int(mid[0] + 150 * s), int(mid[1] - 40 * s)), ink, int(12 * s), cv2.LINE_AA)
    cv2.line(f, (int(mid[0] - 40 * s), int(mid[1] - 34 * s)), (int(mid[0] - 100 * s), int(mid[1] - 120 * s)), ink, int(12 * s), cv2.LINE_AA)
    comp(f, scale_el(head_el(0, True, "n", 0, 0, "smirk"), 0.8 * s), mid[0] - 190 * s, mid[1] - 80 * s)
    for i in range(3):
        q = (t * 0.8 + i / 3) % 1
        comp(f, ed_el("", "z", big_col=WHITE, big_size=int(50 + 30 * q), shadow=0.3), mid[0] - 150 * s + 90 * q * s, mid[1] - 200 * s - 160 * q * s, op=math.sin(math.pi * q))
