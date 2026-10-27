# ================= props for "Your gas station barely makes money on gas" (generic forecourt props — no brand logos, no trade dress) =================
LED = (255, 70, 40); LED_G = (90, 255, 140); PUMP_R = (226, 40, 46); STEEL = (196, 202, 212); SAUCE = (214, 52, 30); CHEESE = (255, 206, 90)
CRUST = (222, 150, 70); PEPP = (176, 34, 30); ROAD = (60, 62, 72); MINTY = (60, 200, 170)


def price_sign_el(prices=("3.09", "3.29", "3.49"), w=440, h=980, bottom="", lit=1.0):
    """tall generic pylon price sign: GAS header, three LED price rows, optional bottom panel text"""
    key = ("psign", prices, w, h, bottom, round(lit, 2))
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        pw = 34; px = (w / 2 - 110, w / 2 + 110 - pw)
        for x in px:
            shape_grad(im, lambda m, x=x: m.rectangle(S(x, 300, x + pw, h - 4), fill=255), (150, 156, 168), (90, 94, 104))
            d.rectangle(S(x, 300, x + pw, h - 4), outline=INK + (255,), width=4 * sc)
        hb = 700 if bottom else 620
        _ov(im, lambda q: q.rounded_rectangle(S(18, 20, w - 2, hb + 14), 26 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(4, 4, w - 18, hb), 26 * sc, fill=(250, 250, 252, 255), outline=INK + (255,), width=7 * sc)
        d.rounded_rectangle(S(18, 18, w - 32, 140), 18 * sc, fill=PUMP_R + (255,))
        d.text(((w - 14) / 2 * sc, 80 * sc), "GAS", font=font(F_BLACK, 92 * sc), fill=(255, 255, 255, 255), anchor="mm")
        led = tuple(int(c * lit + 60 * (1 - lit)) for c in LED)
        for i, (lab, p) in enumerate(zip(("REG", "PLUS", "PREM"), prices)):
            y = 160 + i * 150
            d.rounded_rectangle(S(18, y, w - 32, y + 136), 14 * sc, fill=(24, 24, 30, 255))
            d.text((36 * sc, (y + 68) * sc), lab, font=font(F_BLACK, 30 * sc), fill=(235, 235, 240, 255), anchor="lm")
            d.text(((w - 92) * sc, (y + 72) * sc), p, font=font(F_BLACK, 92 * sc), fill=led + (255,), anchor="rm")
            d.text(((w - 50) * sc, (y + 40) * sc), "9", font=font(F_BLACK, 34 * sc), fill=led + (255,), anchor="mm")
            d.line(S(w - 62, y + 62, w - 40, y + 62), fill=led + (255,), width=3 * sc)
            d.text(((w - 50) * sc, (y + 86) * sc), "10", font=font(F_BLACK, 26 * sc), fill=led + (255,), anchor="mm")
        if bottom:
            d.rounded_rectangle(S(18, 612, w - 32, hb - 14), 14 * sc, fill=YEL_ + (255,))
            d.text(((w - 14) / 2 * sc, (612 + hb - 14) / 2 * sc), bottom, font=font(F_BLACK, 50 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(key, mk)


def pump_el(w=360, h=660, amt="46.65", gal="15.000", nozzle=True, col=PUMP_R, card=False):
    """generic fuel pump: two-tone body, digital display, buttons, hose + nozzle"""
    key = ("pump", w, h, amt, gal, nozzle, col, card)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        bx0, bx1 = 20, w - 90
        _ov(im, lambda q: q.rounded_rectangle(S(bx0 + 14, 30, bx1 + 14, h - 2), 30 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(bx0, 14, bx1, h - 16), 30 * sc, fill=255), tuple(min(255, c + 30) for c in col), col)
        d.rounded_rectangle(S(bx0, 14, bx1, h - 16), 30 * sc, outline=INK + (255,), width=6 * sc)
        d.rounded_rectangle(S(bx0 + 22, 40, bx1 - 22, 250), 16 * sc, fill=(250, 250, 252, 255), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(bx0 + 36, 56, bx1 - 36, 236), 10 * sc, fill=(20, 26, 24, 255))
        cx = (bx0 + bx1) / 2
        d.text(((bx0 + 46) * sc, 98 * sc), "$", font=font(F_BLACK, 30 * sc), fill=LED_G + (255,), anchor="lm")
        d.text(((bx1 - 46) * sc, 100 * sc), amt, font=font(F_BLACK, 46 * sc), fill=LED_G + (255,), anchor="rm")
        d.text(((bx0 + 46) * sc, 186 * sc), "GAL", font=font(F_BLACK, 20 * sc), fill=LED_G + (255,), anchor="lm")
        d.text(((bx1 - 46) * sc, 188 * sc), gal, font=font(F_BLACK, 36 * sc), fill=LED_G + (255,), anchor="rm")
        for i in range(3):
            x = cx - 70 + i * 70
            d.rounded_rectangle(S(x - 26, 290, x + 26, 330), 8 * sc, fill=(250, 250, 252, 255), outline=INK + (255,), width=3 * sc)
            d.text((x * sc, 310 * sc), ("87", "89", "93")[i], font=font(F_BLACK, 22 * sc), fill=INK + (255,), anchor="mm")
        d.rounded_rectangle(S(cx - 70, 370, cx + 70, 440), 10 * sc, fill=(40, 40, 48, 255), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(cx - 50, 400, cx + 50, 410), fill=(10, 10, 12, 255))
        if card:
            d.rounded_rectangle(S(cx - 46, 336, cx + 46, 404), 8 * sc, fill=(80, 130, 255, 255), outline=INK + (255,), width=3 * sc)
            d.rectangle(S(cx - 30, 352, cx - 6, 370), fill=GOLD + (255,))
        d.rounded_rectangle(S(bx0 + 22, 480, bx1 - 22, h - 40), 14 * sc, fill=(255, 255, 255, 60))
        d.text((cx * sc, (h - 120) * sc), "UNLEADED", font=font(F_BLACK, 28 * sc), fill=(255, 255, 255, 255), anchor="mm")
        # hose + nozzle on the right side
        d.arc(S(bx1 - 70, 250, w - 4, h - 60), 270, 90, fill=INK + (255,), width=16 * sc)
        if nozzle:
            d.rounded_rectangle(S(bx1 - 6, 210, bx1 + 50, 300), 10 * sc, fill=(40, 40, 48, 255), outline=INK + (255,), width=4 * sc)
            d.rectangle(S(bx1 + 30, 190, bx1 + 76, 214), fill=(150, 156, 168, 255), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(key, mk)


def nozzle_el(w=300, h=200):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(40, 60, 190, 50, 210, 120, 120, 130, 90, 180, 40, 180), fill=(40, 40, 48, 255), outline=INK + (255,))
        d.rectangle(S(190, 56, 290, 80), fill=STEEL + (255,), outline=INK + (255,), width=3 * sc)
        d.arc(S(70, 100, 170, 190), 180, 360, fill=INK + (255,), width=8 * sc)
        d.line(S(40, 120, 0, 120), fill=INK + (255,), width=18 * sc)
        return _done(im, w, h)
    return gcache(("nozzle", w, h), mk)


def car_el(col=(60, 140, 255), w=440, h=230):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(30, h - 40, w - 30, h - 6), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 90, w - 10, h - 50), 40 * sc, fill=255), tuple(min(255, c + 40) for c in col), col)
        d.rounded_rectangle(S(10, 90, w - 10, h - 50), 40 * sc, outline=INK + (255,), width=6 * sc)
        d.polygon(S(110, 94, 160, 20, 320, 20, 370, 94), fill=col + (255,), outline=INK + (255,))
        d.line(S(110, 94, 160, 20, 320, 20, 370, 94), fill=INK + (255,), width=6 * sc)
        d.polygon(S(140, 90, 175, 36, 235, 36, 235, 90), fill=(200, 235, 255, 255))
        d.polygon(S(250, 90, 250, 36, 310, 36, 345, 90), fill=(200, 235, 255, 255))
        d.ellipse(S(w - 40, 110, w - 18, 130), fill=(255, 240, 160, 255))
        for x in (110, w - 110):
            d.ellipse(S(x - 46, h - 96, x + 46, h - 4), fill=INK + (255,)); d.ellipse(S(x - 20, h - 70, x + 20, h - 30), fill=STEEL + (255,))
        return _done(im, w, h)
    return gcache(("car", col, w, h), mk)


def store_el(w=760, h=560, awning="SNACKS", door_open=0.0):
    """generic convenience store facade: striped awning, windows with stocked shelves, OPEN door"""
    key = ("store", w, h, awning, round(door_open, 1))
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(24, 70, w - 2, h - 2), fill=(0, 0, 0, 70)))
        d.rectangle(S(10, 60, w - 16, h - 14), fill=(250, 242, 226, 255), outline=INK + (255,), width=6 * sc)
        d.rounded_rectangle(S(40, 10, w - 46, 110), 16 * sc, fill=GRN_ + (255,), outline=INK + (255,), width=6 * sc)
        d.text(((w - 6) / 2 * sc, 62 * sc), awning, font=font(F_BLACK, 66 * sc), fill=(255, 255, 255, 255), anchor="mm")
        n_ = 9; sw = (w - 26) / n_
        for i in range(n_):
            d.polygon(S(10 + i * sw, 130, 10 + (i + 1) * sw, 130, 10 + (i + 1) * sw - 6, 196, 10 + i * sw + 6, 196),
                      fill=(RED_ if i % 2 == 0 else (255, 255, 255)) + (255,), outline=INK + (255,))
        d.line(S(10, 130, w - 16, 130), fill=INK + (255,), width=5 * sc)
        dx0, dx1 = w / 2 - 80, w / 2 + 80
        for (x0, x1) in ((40, dx0 - 30), (dx1 + 30, w - 46)):
            d.rectangle(S(x0, 230, x1, h - 60), fill=(180, 225, 255, 255), outline=INK + (255,), width=5 * sc)
            for r in range(3):
                y = 280 + r * 70
                d.line(S(x0 + 10, y + 36, x1 - 10, y + 36), fill=(120, 120, 130, 255), width=4 * sc)
                for j in range(int((x1 - x0 - 20) / 34)):
                    cc = ((255, 120, 40), (255, 200, 40), (60, 170, 255), (240, 60, 90), (90, 200, 110))[(j + r * 2) % 5]
                    d.rounded_rectangle(S(x0 + 14 + j * 34, y, x0 + 40 + j * 34, y + 34), 4 * sc, fill=cc + (255,))
        d.rectangle(S(dx0, 230, dx1, h - 14), fill=(60, 64, 76, 255) if door_open > 0.5 else (200, 235, 255, 255), outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(dx0 + 30, 270, dx1 - 30, 316), 10 * sc, fill=RED_ + (255,))
        d.text((w / 2 * sc, 293 * sc), "OPEN", font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
        if door_open > 0.5: d.rectangle(S(dx0 - 2, 220, dx0 + 30, h - 14), fill=(250, 250, 252, 255), outline=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(key, mk)


def pizza_el(r=220, missing=0):
    def mk():
        sc = 2; w = h = 2 * r + 30; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cx = cy = r + 12; a0 = 360 / 8 * missing
        _ov(im, lambda q: q.pieslice(S(cx - r + 10, cy - r + 16, cx + r + 10, cy + r + 16), -90 + a0, 270, fill=(0, 0, 0, 70)))
        d.pieslice(S(cx - r, cy - r, cx + r, cy + r), -90 + a0, 270, fill=CRUST + (255,), outline=INK + (255,), width=6 * sc)
        r2 = r * 0.84
        d.pieslice(S(cx - r2, cy - r2, cx + r2, cy + r2), -90 + a0, 270, fill=SAUCE + (255,))
        r3 = r * 0.8
        d.pieslice(S(cx - r3, cy - r3, cx + r3, cy + r3), -90 + a0, 270, fill=CHEESE + (255,))
        rng_ = np.random.default_rng(7)
        for i in range(14):
            a = rng_.uniform(0, 2 * math.pi); rr = rng_.uniform(0.15, 0.65) * r
            ang = (math.degrees(a) + 90) % 360
            if ang < a0: continue
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a); pr = r * 0.1
            d.ellipse(S(x - pr, y - pr, x + pr, y + pr), fill=PEPP + (255,), outline=(120, 20, 18, 255), width=2 * sc)
        for k_ in range(8):
            ang = -90 + k_ * 45
            if k_ * 45 < a0: continue
            d.line(S(cx, cy, cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))), fill=(190, 120, 50, 255), width=3 * sc)
        return _done(im, w, h)
    return gcache(("pizza", r, missing), mk)


def slice_el(w=220, h=260):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w / 2, h - 10, 10, 50, w - 10, 50), fill=CHEESE + (255,), outline=INK + (255,))
        d.rounded_rectangle(S(4, 20, w - 4, 70), 24 * sc, fill=CRUST + (255,), outline=INK + (255,), width=5 * sc)
        for (x, y) in ((w / 2 - 40, 110), (w / 2 + 34, 120), (w / 2, 180)):
            d.ellipse(S(x - 20, y - 20, x + 20, y + 20), fill=PEPP + (255,))
        d.line(S(w / 2, h - 10, 10, 50), fill=INK + (255,), width=5 * sc); d.line(S(w / 2, h - 10, w - 10, 50), fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("slice", w, h), mk)


def fountain_cup_el(w=220, h=360, col=(40, 150, 255)):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.line(S(w / 2 + 20, 0, w / 2 + 6, 90), fill=RED_ + (255,), width=14 * sc)
        d.rounded_rectangle(S(10, 70, w - 10, 104), 12 * sc, fill=(250, 250, 252, 255), outline=INK + (255,), width=5 * sc)
        shape_grad(im, lambda m: m.polygon(S(22, 104, w - 22, 104, w - 44, h - 8, 44, h - 8), fill=255), tuple(min(255, c + 50) for c in col), col)
        d.polygon(S(22, 104, w - 22, 104, w - 44, h - 8, 44, h - 8), outline=INK + (255,))
        d.line(S(22, 104, 44, h - 8, w - 44, h - 8, w - 22, 104), fill=INK + (255,), width=5 * sc)
        d.rectangle(S(36, 170, w - 36, 220), fill=(255, 255, 255, 230))
        d.text((w / 2 * sc, 196 * sc), "XL", font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("fcup", w, h, col), mk)


def chips_el(col=(255, 170, 30), w=170, h=230, label="CHIPS"):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.polygon(S(10, 14, w - 10, 14, w - 18, h / 2, w - 10, h - 14, 10, h - 14, 18, h / 2), fill=255), tuple(min(255, c + 50) for c in col), col)
        d.line(S(10, 14, w - 10, 14, w - 18, h / 2, w - 10, h - 14, 10, h - 14, 18, h / 2, 10, 14), fill=INK + (255,), width=5 * sc)
        for x in range(16, w - 14, 12): d.line(S(x, 14, x + 6, 26), fill=INK + (200,), width=2 * sc)
        d.ellipse(S(w / 2 - 50, h / 2 - 34, w / 2 + 50, h / 2 + 34), fill=(255, 255, 255, 235))
        d.text((w / 2 * sc, h / 2 * sc), label, font=font(F_BLACK, 24 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("chips", col, w, h, label), mk)


def receipt_el(rows, w=470, h=600, stamp=None):
    """paper receipt with zig-zag bottom; rows = [(left, right, bold)]"""
    key = ("rcpt", tuple(rows), w, h, stamp)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        zz = [(0, 0), (w, 0), (w, h - 20)]
        for i in range(int(w / 30), -1, -1): zz += [(i * 30 + 15, h), (i * 30, h - 20)]
        _ov(im, lambda q: q.polygon([(x * sc + 12 * sc, y * sc + 14 * sc) for x, y in zz], fill=(0, 0, 0, 60)))
        d.polygon([(x * sc, y * sc) for x, y in zz], fill=(255, 255, 252, 255), outline=(170, 170, 170, 255))
        d.text((w / 2 * sc, 50 * sc), "FUEL RECEIPT", font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.line(S(30, 90, w - 30, 90), fill=(150, 150, 150, 255), width=2 * sc)
        for i, (l, r, b) in enumerate(rows):
            y = 130 + i * 62; fn = font(F_BLACK if b else F_SEMI, (40 if b else 34) * sc)
            d.text((36 * sc, y * sc), l, font=fn, fill=INK + (255,), anchor="lm")
            d.text(((w - 36) * sc, y * sc), r, font=fn, fill=(GRN_ if b else INK) + (255,), anchor="rm")
        return _done(im, w, h)
    return gcache(key, mk)


def gas_can_el(w=260, h=300, label="1 GAL"):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(26, 70, w - 2, h - 2), 26 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(14, 60, w - 14, h - 12), 26 * sc, fill=255), (255, 80, 70), (200, 24, 30))
        d.rounded_rectangle(S(14, 60, w - 14, h - 12), 26 * sc, outline=INK + (255,), width=6 * sc)
        d.rounded_rectangle(S(40, 20, 140, 70), 14 * sc, outline=INK + (255,), width=12 * sc)
        d.polygon(S(170, 64, 210, 6, 236, 14, 206, 70), fill=(250, 210, 40, 255), outline=INK + (255,))
        d.text((w / 2 * sc, (h / 2 + 40) * sc), label, font=font(F_BLACK, 54 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("gascan", w, h, label), mk)


def pay_card_el(w=300, h=190, col=(80, 130, 255)):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 4, w - 4, h - 4), 22 * sc, fill=255), tuple(min(255, c + 60) for c in col), col)
        d.rounded_rectangle(S(4, 4, w - 4, h - 4), 22 * sc, outline=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(34, 60, 94, 106), 8 * sc, fill=GOLD + (255,), outline=INK + (255,), width=2 * sc)
        d.text((34 * sc, 146 * sc), "•••• 4242", font=font(F_BLACK, 26 * sc), fill=(255, 255, 255, 255), anchor="lm")
        return _done(im, w, h)
    return gcache(("pcard", w, h, col), mk)


def curtain(f, k, col=(190, 20, 40)):
    """stage curtains; k = 0 closed .. 1 fully open"""
    half = int((W / 2) * (1 - eo(clamp(k))))
    if half <= 2: return
    for side in (0, 1):
        x0, x1 = (0, half) if side == 0 else (W - half, W)
        f[:, x0:x1] = np.array(C(col), np.float32)
        for xx in range(x0, x1, 70):
            cv2.line(f, (xx, 0), (xx, H), C((120, 8, 24)), 18, cv2.LINE_AA)
        cv2.line(f, ((x1 if side == 0 else x0), 0), ((x1 if side == 0 else x0), H), C(GOLD), 10, cv2.LINE_AA)


def pie_coin(f, cx, cy, r, frac, col, label, k=1.0, sub=""):
    """gold coin with a coloured wedge = share of each dollar kept; label in the middle"""
    if k <= 0.01: return
    s = pin(k, 0.0, 1.0) if k < 1 else 1.0
    rr = int(r * max(0.05, s))
    cv2.circle(f, (cx + 8, cy + 14), rr, (0, 0, 0), -1, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), rr, C((250, 222, 140)), -1, cv2.LINE_AA)
    ang = 360 * frac * eo(clamp(k * 1.4))
    if ang > 0.5: cv2.ellipse(f, (cx, cy), (rr, rr), -90, 0, ang, C(col), -1, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), rr, C(INK), max(2, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (cx, cy), int(rr * 0.62), C((255, 248, 225)), -1, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), int(rr * 0.62), C(INK), max(2, int(5 * s)), cv2.LINE_AA)
    if s > 0.6:
        comp(f, ed_el("", label, "", big_col=INK, big_size=int(r * 0.5), maxw=int(r * 1.1)), cx, cy - 4, op=clamp((s - 0.6) / 0.3))
        if sub: comp(f, ed_el(sub, "", lead_col=WHITE, lead_size=34), cx, cy + rr + 46, op=clamp((s - 0.6) / 0.3))


def stack_bar(f, x, top, w, h, frac_a, k, col_a, col_b, lab_a, lab_b, title):
    """100% stacked vertical bar: bottom part col_a (frac_a), top part col_b"""
    kk = eo(clamp(k)); hh = int(h * kk)
    cv2.rectangle(f, (x - w // 2 + 10, top + h - hh + 10), (x + w // 2 + 10, top + h + 10), (0, 0, 0), -1, cv2.LINE_AA)
    ha = int(hh * frac_a)
    cv2.rectangle(f, (x - w // 2, top + h - ha), (x + w // 2, top + h), C(col_a), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x - w // 2, top + h - hh), (x + w // 2, top + h - ha), C(col_b), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x - w // 2, top + h - hh), (x + w // 2, top + h), C(INK), 6, cv2.LINE_AA)
    cv2.line(f, (x - w // 2, top + h - ha), (x + w // 2, top + h - ha), C(INK), 6, cv2.LINE_AA)
    if kk > 0.7:
        op = clamp((kk - 0.7) / 0.3)
        comp(f, ed_el("", lab_a, "", big_col=WHITE, big_size=60, maxw=w - 20), x, top + h - ha / 2, op=op)
        comp(f, ed_el("", lab_b, "", big_col=INK, big_size=60, maxw=w - 20), x, top + h - ha - (hh - ha) / 2, op=op)
    comp(f, ed_el("", title, "", big_col=INK, big_size=46, maxw=w + 80), x, top + h + 52)


def store_map(f, cx, cy, k, t):
    """top-down store floor plan: door at the bottom, coffee + restroom at the back, a dotted path that snakes past every shelf"""
    x0, y0, x1, y1 = cx - 380, cy - 420, cx + 380, cy + 420
    cv2.rectangle(f, (x0 + 12, y0 + 14), (x1 + 12, y1 + 14), (0, 0, 0), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((250, 246, 236)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INK), 10, cv2.LINE_AA)
    cv2.rectangle(f, (cx - 70, y1 - 6), (cx + 70, y1 + 6), C((250, 246, 236)), -1)
    shelves = [(x0 + 90, y0 + 260, x0 + 330, y0 + 300), (x1 - 330, y0 + 260, x1 - 90, y0 + 300),
               (x0 + 90, y0 + 450, x0 + 330, y0 + 490), (x1 - 330, y0 + 450, x1 - 90, y0 + 490)]
    cols = ((255, 120, 40), (60, 170, 255), (240, 60, 90), (90, 200, 110))
    for (a, b, c, d_), cc in zip(shelves, cols):
        cv2.rectangle(f, (a, b), (c, d_), C(cc), -1, cv2.LINE_AA); cv2.rectangle(f, (a, b), (c, d_), C(INK), 5, cv2.LINE_AA)
    cv2.rectangle(f, (x0 + 30, y0 + 30), (x0 + 270, y0 + 130), C((120, 70, 40)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0 + 30, y0 + 30), (x0 + 270, y0 + 130), C(INK), 5, cv2.LINE_AA)
    cv2.rectangle(f, (x1 - 270, y0 + 30), (x1 - 30, y0 + 130), C((60, 200, 220)), -1, cv2.LINE_AA); cv2.rectangle(f, (x1 - 270, y0 + 30), (x1 - 30, y0 + 130), C(INK), 5, cv2.LINE_AA)
    cv2.rectangle(f, (x0 + 260, y1 - 150), (x1 - 260, y1 - 90), C((255, 199, 30)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0 + 260, y1 - 150), (x1 - 260, y1 - 90), C(INK), 5, cv2.LINE_AA)
    comp(f, ed_el("", "COFFEE", "", big_col=WHITE, big_size=40, maxw=220), x0 + 150, y0 + 80)
    comp(f, ed_el("", "RESTROOM", "", big_col=INK, big_size=36, maxw=220), x1 - 150, y0 + 80)
    comp(f, ed_el("", "CANDY + CASH", "", big_col=INK, big_size=30, maxw=230), cx, y1 - 120)
    comp(f, ed_el("", "DOOR", "", big_col=INK, big_size=30, maxw=200), cx, y1 + 40)
    path = [(cx, y1 - 10), (cx, y1 - 200), (x0 + 60, y1 - 250), (x0 + 60, y0 + 380), (x1 - 60, y0 + 380), (x1 - 60, y0 + 180),
            (x0 + 150, y0 + 180), (x0 + 150, y0 + 140)]
    seg = [math.hypot(path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]) for i in range(len(path) - 1)]
    tot = sum(seg); L = tot * eio(clamp(k)); acc = 0.0; head = path[0]
    for i, s_ in enumerate(seg):
        if acc >= L: break
        q = min(1.0, (L - acc) / s_); a, b = path[i], path[i + 1]
        e = (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)
        nd = int(s_ * q / 34)
        for j in range(nd + 1):
            p = (a[0] + (b[0] - a[0]) * j * 34 / s_, a[1] + (b[1] - a[1]) * j * 34 / s_)
            cv2.circle(f, (int(p[0]), int(p[1])), 9, C(RED_), -1, cv2.LINE_AA)
        head = e; acc += s_
    if k > 0.02: cv2.circle(f, (int(head[0]), int(head[1])), 22, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(head[0]), int(head[1])), 14, C(YEL_), -1, cv2.LINE_AA)


def cash_pile(f, x, base, n_, k, s=0.7):
    """pile of cash bundles that builds up as k goes 0 -> 1"""
    m = int(round(n_ * clamp(k)))
    for i in range(m):
        r_, c_ = divmod(i, 3)
        xx = x + (c_ - 1) * 110 * s + (55 * s if r_ % 2 else 0); yy = base - r_ * 52 * s
        comp(f, scale_el(cash_el(1), s * 0.62), xx, yy)


def mini_store(x, y, f, s=1.0):
    comp(f, scale_el(store_el(), 0.16 * s), x, y)
