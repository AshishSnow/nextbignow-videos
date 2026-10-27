# ================= props for "Your airline's real money machine is your credit card" =================
# Generic props only: no airline liveries, no card-network logos, no real card designs (brand names appear only as plain caption text).
SKYB = (60, 140, 240); JET = (246, 248, 252); JET_S = (196, 204, 220); MILEB = (40, 110, 230); CARD_P = (70, 40, 160)
STEEL = (196, 202, 212); WOOD = (150, 92, 44); WOOD_D = (104, 60, 28); CHAIN = (120, 126, 140)


def plane_el(w=820, tail=(232, 60, 40), stripe=None, grey=0.0, gear=False):
    """generic side-view airliner facing right (no livery, no logo)"""
    key = ("plane", w, tail, stripe, round(grey, 2), gear)
    def mk():
        sc = 2; h = int(w * 0.42); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        g = lambda c: tuple(int(v * (1 - grey) + 150 * grey) for v in c)
        body = g(JET); sh = g(JET_S); tl = g(tail); st = g(stripe or tail)
        fy0, fy1 = h * 0.42, h * 0.70; cy = (fy0 + fy1) / 2; fh = fy1 - fy0
        # tail fin
        d.polygon(S(w * 0.04, fy0 + 4, w * 0.10, h * 0.04, w * 0.20, h * 0.04, w * 0.24, fy0 + 4), fill=tl + (255,), outline=INK + (255,))
        d.line(S(w * 0.04, fy0 + 4, w * 0.10, h * 0.04, w * 0.20, h * 0.04, w * 0.24, fy0 + 4), fill=INK + (255,), width=5 * sc)
        # far wing
        d.polygon(S(w * 0.50, fy0 + fh * 0.3, w * 0.40, h * 0.18, w * 0.46, h * 0.18, w * 0.62, fy0 + fh * 0.3), fill=sh + (255,), outline=INK + (255,))
        # fuselage
        shape_grad(im, lambda m: m.rounded_rectangle(S(w * 0.03, fy0, w * 0.93, fy1), int(fh / 2) * sc, fill=255), body, sh)
        d.rounded_rectangle(S(w * 0.03, fy0, w * 0.93, fy1), int(fh / 2) * sc, outline=INK + (255,), width=6 * sc)
        d.rectangle(S(w * 0.08, cy + fh * 0.12, w * 0.86, cy + fh * 0.24), fill=st + (255,))
        # cockpit windows
        d.polygon(S(w * 0.865, fy0 + fh * 0.22, w * 0.905, fy0 + fh * 0.22, w * 0.92, fy0 + fh * 0.40, w * 0.86, fy0 + fh * 0.40), fill=(40, 60, 90, 255))
        # cabin windows
        for i in range(14):
            x = w * 0.22 + i * w * 0.042
            d.rounded_rectangle(S(x, cy - fh * 0.22, x + w * 0.022, cy - fh * 0.02), 5 * sc, fill=(60, 90, 140, 255))
        # door
        d.rounded_rectangle(S(w * 0.80, cy - fh * 0.32, w * 0.83, cy + fh * 0.30), 6 * sc, outline=g((150, 156, 170)) + (255,), width=3 * sc)
        # near wing + engine
        d.polygon(S(w * 0.42, cy + fh * 0.1, w * 0.60, cy + fh * 0.1, w * 0.44, h * 0.98, w * 0.37, h * 0.98), fill=g((226, 230, 238)) + (255,), outline=INK + (255,))
        d.line(S(w * 0.42, cy + fh * 0.1, w * 0.37, h * 0.98, w * 0.44, h * 0.98, w * 0.60, cy + fh * 0.1), fill=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(w * 0.47, cy + fh * 0.42, w * 0.63, cy + fh * 0.95), 18 * sc, fill=g((214, 220, 232)) + (255,), outline=INK + (255,), width=5 * sc)
        d.ellipse(S(w * 0.60, cy + fh * 0.46, w * 0.645, cy + fh * 0.91), fill=(50, 54, 64, 255))
        if gear:
            for x in (w * 0.24, w * 0.52, w * 0.84):
                d.line(S(x, fy1 - 4, x, h * 0.9), fill=INK + (255,), width=6 * sc)
                d.ellipse(S(x - 16, h * 0.86, x + 16, h * 0.99), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(key, mk)


def card_el(w=560, col=CARD_P, col2=(150, 80, 255), label="MILES CARD", num="2026", foil=0.0):
    """generic rewards credit card: gradient, gold chip, contactless waves, a small plane icon (no network logo)"""
    key = ("card", w, col, col2, label, num, round(foil, 2))
    def mk():
        sc = 2; h = int(w * 0.63); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 14, w - 2, h - 2), 34 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 12, h - 12), 34 * sc, fill=255), col2, col)
        d.rounded_rectangle(S(2, 2, w - 12, h - 12), 34 * sc, outline=INK + (255,), width=6 * sc)
        if foil > 0:
            x0 = (w + 200) * foil - 200
            _ov(im, lambda q: q.polygon(S(x0, 4, x0 + 90, 4, x0 - 40, h - 14, x0 - 130, h - 14), fill=(255, 255, 255, 70)))
        d.rounded_rectangle(S(52, h * 0.34, 52 + w * 0.15, h * 0.34 + w * 0.115), 10 * sc, fill=GOLD + (255,), outline=(150, 110, 30, 255), width=3 * sc)
        for i in range(3):
            r = 18 + i * 14; cx, cy = w * 0.34, h * 0.42
            d.arc(S(cx - r, cy - r, cx + r, cy + r), -40, 40, fill=(255, 255, 255, 230), width=4 * sc)
        d.text((44 * sc, 52 * sc), label, font=font(F_BLACK, int(w * 0.075) * sc), fill=(255, 255, 255, 255), anchor="lm")
        d.text((44 * sc, h * 0.74 * sc), "••••  ••••  ••••  " + num, font=font(F_BLACK, int(w * 0.06) * sc), fill=(255, 255, 255, 235), anchor="lm")
        # little plane glyph top-right
        px, py = w - 90, 56
        d.polygon(S(px - 40, py, px + 34, py - 6, px + 44, py, px + 34, py + 6), fill=(255, 255, 255, 255))
        d.polygon(S(px - 4, py, px - 20, py - 30, px - 8, py - 30, px + 14, py), fill=(255, 255, 255, 255))
        d.polygon(S(px - 4, py, px - 20, py + 30, px - 8, py + 30, px + 14, py), fill=(255, 255, 255, 255))
        return _done(im, w, h)
    return gcache(key, mk)


def cheque_el(payer, payee, amount, words, memo, w=860, h=400):
    """big novelty cheque"""
    key = ("chq", payer, payee, amount, words, memo, w, h)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 18, w - 2, h - 2), 22 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 16, h - 16), 22 * sc, fill=255), (236, 250, 240), (200, 236, 214))
        d.rounded_rectangle(S(2, 2, w - 16, h - 16), 22 * sc, outline=INK + (255,), width=6 * sc)
        d.text((34 * sc, 46 * sc), payer, font=font(F_BLACK, 32 * sc), fill=INK + (255,), anchor="lm")
        d.text(((w - 50) * sc, 46 * sc), "2025", font=font(F_BLACK, 28 * sc), fill=(90, 110, 100, 255), anchor="rm")
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


def balance(f, cx, cy, tilt, left_el, right_el, t=0.0, arm=330):
    """balance scale: tilt in degrees (+ = left side down); pans hang from the beam ends"""
    a = math.radians(tilt)
    lx, ly = cx - arm * math.cos(a), cy + arm * math.sin(a); rx, ry = cx + arm * math.cos(a), cy - arm * math.sin(a)
    cv2.line(f, (cx, cy), (cx, cy + 560), C(INK), 18, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy + 570), (150, 34), 0, 0, 360, C((90, 60, 40)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy + 570), (150, 34), 0, 0, 360, C(INK), 6, cv2.LINE_AA)
    cv2.line(f, (int(lx), int(ly)), (int(rx), int(ry)), C(INK), 20, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), 26, C(GOLD), -1, cv2.LINE_AA); cv2.circle(f, (cx, cy), 26, C(INK), 6, cv2.LINE_AA)
    for (px, py, el) in ((lx, ly, left_el), (rx, ry, right_el)):
        py2 = py + 230
        for dx in (-110, 110): cv2.line(f, (int(px), int(py)), (int(px + dx), int(py2)), C(INK), 5, cv2.LINE_AA)
        if el is not None: comp(f, el, px, py2 - el[1].shape[0] / 2 + 6)
        cv2.ellipse(f, (int(px), int(py2)), (150, 30), 0, 0, 180, C(STEEL), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(px), int(py2)), (150, 30), 0, 0, 180, C(INK), 6, cv2.LINE_AA)
        cv2.line(f, (int(px - 150), int(py2)), (int(px + 150), int(py2)), C(INK), 6, cv2.LINE_AA)


_FLAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def flapboard(f, cx, cy, text, t, t0, cell=(92, 136), gap=10, stagger=0.07, spin=0.6, col=(255, 214, 60)):
    """airport split-flap board: each cell flips through letters, then settles on its character (left to right)"""
    n_ = len(text); cw, ch = cell; x0 = cx - (n_ * cw + (n_ - 1) * gap) / 2
    cv2.rectangle(f, (int(x0 - 28), int(cy - ch / 2 - 28)), (int(x0 + n_ * (cw + gap) - gap + 28), int(cy + ch / 2 + 28)), C((30, 30, 36)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x0 - 28), int(cy - ch / 2 - 28)), (int(x0 + n_ * (cw + gap) - gap + 28), int(cy + ch / 2 + 28)), C(INK), 8, cv2.LINE_AA)
    fn = int(ch * 0.78)
    for i, c in enumerate(text):
        x = x0 + i * (cw + gap)
        cv2.rectangle(f, (int(x), int(cy - ch / 2)), (int(x + cw), int(cy + ch / 2)), C((14, 14, 18)), -1, cv2.LINE_AA)
        ts = t0 + i * stagger + spin
        if c == " ": ch_ = " "
        elif t < ts: ch_ = ((_FLAP[26:] if c.isdigit() else _FLAP[:26])[int((t * 30 + i * 7)) % (10 if c.isdigit() else 26)]) if t >= t0 else " "
        else: ch_ = c
        if ch_ != " ":
            comp(f, gcache(("flapc", ch_, fn, col), lambda: ed_el("", ch_, "", big_col=col, big_size=fn, maxw=cw * 2)), x + cw / 2, cy + 2)
        cv2.line(f, (int(x), int(cy)), (int(x + cw), int(cy)), C((0, 0, 0)), 3, cv2.LINE_AA)


def mile_el(r=60):
    """generic 'mile' token: blue coin with a plane glyph and M"""
    def mk():
        sc = 2; R = r * sc; w = h = 2 * R + 8 * sc; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = w / 2
        d.ellipse([c - R, c - R, c + R, c + R], fill=(20, 60, 160, 255))
        d.ellipse([c - R * 0.88, c - R * 0.88, c + R * 0.88, c + R * 0.88], fill=MILEB + (255,))
        d.ellipse([c - R * 0.88, c - R * 0.88, c + R * 0.88, c + R * 0.88], outline=(170, 210, 255, 255), width=max(2, int(R * 0.05)))
        d.text((c, c + R * 0.05), "M", font=font(F_BLACK, int(R * 1.05)), fill=(255, 255, 255, 255), anchor="mm")
        return el_from(im.resize((w // sc, h // sc), Image.LANCZOS))
    return gcache(("mile", r), mk)


def chest_el(w=520, open_=0.0, chained=0.0):
    """treasure chest full of mile tokens; chained = 0..1 wraps chains + padlock"""
    key = ("chest", w, round(open_, 2), round(chained, 2))
    def mk():
        sc = 2; h = int(w * 0.9); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        by0 = h * 0.45
        _ov(im, lambda q: q.rounded_rectangle(S(18, by0 + 16, w - 2, h - 2), 20 * sc, fill=(0, 0, 0, 80)))
        if open_ > 0.05:   # lid open: show tokens
            for i in range(9):
                x = w * 0.18 + (i % 5) * w * 0.16; y = by0 - 10 - (i // 5) * 40 - 30 * open_
                d.ellipse(S(x - 44, y - 44, x + 44, y + 44), fill=(20, 60, 160, 255)); d.ellipse(S(x - 38, y - 38, x + 38, y + 38), fill=MILEB + (255,))
                d.text((x * sc, y * sc), "M", font=font(F_BLACK, 44 * sc), fill=(255, 255, 255, 255), anchor="mm")
            ly = by0 - h * 0.38 * open_
            d.rounded_rectangle(S(10, ly - 30, w - 22, ly + 8), 14 * sc, fill=WOOD_D + (255,), outline=INK + (255,), width=6 * sc)
        else:
            d.chord(S(10, by0 - h * 0.34, w - 22, by0 + h * 0.34), 180, 360, fill=WOOD + (255,), outline=INK + (255,), width=6 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, by0, w - 22, h - 16), 18 * sc, fill=255), WOOD, WOOD_D)
        d.rounded_rectangle(S(10, by0, w - 22, h - 16), 18 * sc, outline=INK + (255,), width=6 * sc)
        for x in (w * 0.2, w * 0.76): d.rectangle(S(x - 16, by0, x + 16, h - 16), fill=GOLD + (255,), outline=INK + (255,), width=4 * sc)
        d.rectangle(S(10, by0, w - 22, by0 + 30), fill=GOLD + (255,), outline=INK + (255,), width=4 * sc)
        if chained > 0:
            n_ = int(14 * chained)
            for j in range(2):
                for i in range(n_):
                    x0 = 20 + i * (w - 40) / 14; y0 = by0 + 70 + j * 120 + (i % 2) * 6
                    d.ellipse(S(x0, y0 - 14, x0 + 44, y0 + 14), outline=CHAIN + (255,), width=8 * sc)
            if chained >= 0.99:
                cx, cy = w / 2 - 6, by0 + 190
                d.arc(S(cx - 40, cy - 110, cx + 40, cy - 10), 180, 360, fill=STEEL + (255,), width=14 * sc)
                d.line(S(cx - 40, cy - 60, cx - 40, cy - 10), fill=STEEL + (255,), width=14 * sc); d.line(S(cx + 40, cy - 60, cx + 40, cy - 10), fill=STEEL + (255,), width=14 * sc)
                d.rounded_rectangle(S(cx - 70, cy - 20, cx + 70, cy + 90), 16 * sc, fill=YEL_ + (255,), outline=INK + (255,), width=6 * sc)
                d.ellipse(S(cx - 12, cy + 18, cx + 12, cy + 42), fill=INK + (255,)); d.rectangle(S(cx - 5, cy + 36, cx + 5, cy + 66), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(key, mk)


def suitcase_el(w=360, col=(240, 120, 40)):
    def mk():
        sc = 2; h = int(w * 0.95); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(w * 0.33, 8, w * 0.67, 70), 16 * sc, outline=INK + (255,), width=12 * sc)
        _ov(im, lambda q: q.rounded_rectangle(S(18, 70, w - 2, h - 2), 30 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 54, w - 16, h - 18), 30 * sc, fill=255), tuple(min(255, c + 30) for c in col), col)
        d.rounded_rectangle(S(4, 54, w - 16, h - 18), 30 * sc, outline=INK + (255,), width=6 * sc)
        for x in (w * 0.28, w * 0.68): d.rectangle(S(x - 10, 54, x + 10, h - 18), fill=(110, 60, 30, 255))
        d.rounded_rectangle(S(w * 0.4, h * 0.45, w * 0.58, h * 0.6), 8 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("suitcase", w, col), mk)


def rulebook_el(w=520, page=0.0, lines_col=(150, 150, 160)):
    """open program rulebook; page = 0..1 page-flip progress"""
    key = ("rules", w, round(page, 2))
    def mk():
        sc = 2; h = int(w * 0.72); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(16, 22, w - 2, h - 2), 16 * sc, fill=(0, 0, 0, 80)))
        d.rounded_rectangle(S(2, 8, w - 14, h - 14), 16 * sc, fill=(160, 30, 40, 255), outline=INK + (255,), width=6 * sc)
        for side in (0, 1):
            x0 = 24 + side * (w / 2 - 12); x1 = x0 + w / 2 - 36
            d.rectangle(S(x0, 26, x1, h - 34), fill=(252, 250, 244, 255), outline=INK + (255,), width=3 * sc)
            for i in range(9):
                y = 60 + i * (h - 110) / 9
                d.line(S(x0 + 20, y, x1 - 20 - (i * 37 % 60), y), fill=lines_col + (255,), width=5 * sc)
        d.text((w / 4 * sc + 6 * sc, 44 * sc), "RULES", font=font(F_BLACK, 28 * sc), fill=INK + (255,), anchor="mm")
        if 0 < page < 1:
            xm = w / 2 - 6; xe = xm + (w / 2 - 36) * math.cos(math.pi * page)
            d.polygon(S(xm, 26, xe, 26 - 20 * math.sin(math.pi * page), xe, h - 34 - 20 * math.sin(math.pi * page), xm, h - 34), fill=(236, 232, 222, 255), outline=INK + (255,))
        d.line(S(w / 2 - 6, 20, w / 2 - 6, h - 28), fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(key, mk)


def terminal_el(w=300, screen="TAP CARD", ok=False):
    """generic card reader"""
    def mk():
        sc = 2; h = int(w * 1.5); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 18, w - 2, h - 2), 34 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 14, h - 14), 34 * sc, fill=255), (70, 74, 88), (36, 38, 46))
        d.rounded_rectangle(S(2, 2, w - 14, h - 14), 34 * sc, outline=INK + (255,), width=6 * sc)
        d.rounded_rectangle(S(26, 30, w - 38, h * 0.42), 14 * sc, fill=((40, 200, 110) if ok else (210, 236, 255)) + (255,), outline=INK + (255,), width=4 * sc)
        d.text(((w - 12) / 2 * sc, h * 0.23 * sc), screen, font=font(F_BLACK, int(w * 0.1) * sc), fill=((255, 255, 255) if ok else INK) + (255,), anchor="mm")
        for r_ in range(3):
            for c_ in range(3):
                x = 60 + c_ * (w - 120) / 2.6; y = h * 0.52 + r_ * h * 0.13
                d.rounded_rectangle(S(x - 30, y - 22, x + 30, y + 22), 10 * sc, fill=(230, 232, 240, 255), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("term", w, screen, ok), mk)


def runway(f, y, col=(70, 72, 84)):
    f[y:] = f[y:] * 0.3 + np.array(C(col), np.float32) * 0.7
    cv2.line(f, (0, y), (W, y), C(INK), 6, cv2.LINE_AA)
    for i in range(6):
        x = 60 + i * 190; cv2.rectangle(f, (x, y + 90), (x + 110, y + 106), C((250, 250, 250)), -1, cv2.LINE_AA)
