# ================= props for "Starbucks is secretly a bank" (generic, no logos) =================
COFFEE = (120, 70, 40); SLEEVE = (176, 118, 64); MINT = (40, 190, 140)


def coffee_el(w=380, h=560):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        body = S(w * 0.12, h * 0.2, w * 0.88, h * 0.2, w * 0.76, h * 0.98, w * 0.24, h * 0.98)
        shape_grad(im, lambda m: m.polygon(body, fill=255), (255, 255, 255), (226, 228, 236))
        _ov(im, lambda q: q.polygon(S(w * 0.66, h * 0.2, w * 0.86, h * 0.2, w * 0.75, h * 0.98, w * 0.62, h * 0.98), fill=(0, 0, 0, 22)))
        _ov(im, lambda q: q.polygon(S(w * 0.18, h * 0.2, w * 0.28, h * 0.2, w * 0.33, h * 0.98, w * 0.26, h * 0.98), fill=(255, 255, 255, 160)))
        shape_grad(im, lambda m: m.polygon(S(w * 0.15, h * 0.45, w * 0.85, h * 0.45, w * 0.81, h * 0.72, w * 0.19, h * 0.72), fill=255), (196, 136, 78), (150, 96, 50))
        cx, cy = w * 0.5, h * 0.585
        d.ellipse(S(cx - 30, cy - 42, cx + 30, cy + 42), fill=(90, 50, 24, 255)); d.arc(S(cx - 16, cy - 40, cx + 16, cy + 40), 250, 110, fill=(196, 136, 78, 255), width=6 * sc)
        d.rounded_rectangle(S(w * 0.06, h * 0.12, w * 0.94, h * 0.22), 18 * sc, fill=(248, 248, 250, 255), outline=(200, 204, 214, 255), width=3 * sc)
        d.chord(S(w * 0.14, h * 0.02, w * 0.86, h * 0.24), 180, 360, fill=(255, 255, 255, 255), outline=(206, 210, 220, 255), width=3 * sc)
        d.ellipse(S(w * 0.42, h * 0.05, w * 0.58, h * 0.1), fill=(190, 196, 206, 255))
        return _done(im, w, h)
    return gcache(("coffee", w, h), mk)


def vault_door_el(r=150):
    def mk():
        sc = 2; s = 2 * r + 20; im, d = _canvas(s, s); S = lambda *v: [x * sc for x in v]; c = s / 2
        _ov(im, lambda q: q.ellipse(S(c - r + 8, c - r + 10, c + r + 8, c + r + 10), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.ellipse(S(c - r, c - r, c + r, c + r), fill=255), (214, 220, 230), (130, 140, 156))
        d.ellipse(S(c - r * 0.82, c - r * 0.82, c + r * 0.82, c + r * 0.82), outline=(100, 108, 122, 255), width=6 * sc)
        for i in range(12):
            a = i * math.pi / 6; x, y = c + r * 0.91 * math.cos(a), c + r * 0.91 * math.sin(a)
            d.ellipse(S(x - 7, y - 7, x + 7, y + 7), fill=(90, 98, 112, 255))
        for i in range(3):
            a = i * math.pi / 3
            d.line(S(c - r * 0.6 * math.cos(a), c - r * 0.6 * math.sin(a), c + r * 0.6 * math.cos(a), c + r * 0.6 * math.sin(a)), fill=(60, 66, 80, 255), width=14 * sc)
        d.ellipse(S(c - r * 0.2, c - r * 0.2, c + r * 0.2, c + r * 0.2), fill=(250, 200, 40, 255), outline=(60, 66, 80, 255), width=6 * sc)
        return _done(im, s, s)
    return gcache(("vault", r), mk)


def bank_el(label="BANK", w=600, h=540, col=(250, 246, 236)):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(int(v * 0.8) for v in col)
        shape_grad(im, lambda m: m.polygon(S(w * 0.5, 6, w - 20, h * 0.26, 20, h * 0.26), fill=255), col, dk)
        d.rectangle(S(30, h * 0.26, w - 30, h * 0.34), fill=dk + (255,))
        d.text((w / 2 * sc, h * 0.19 * sc), label, font=font(F_BLACK, int(h * 0.09) * sc), fill=INK + (255,), anchor="mm")
        for i in range(5):
            x = 70 + i * (w - 140) / 4
            shape_grad(im, lambda m, x=x: m.rectangle(S(x - 26, h * 0.34, x + 26, h * 0.84), fill=255), (255, 255, 255), dk)
            d.rectangle(S(x - 34, h * 0.34, x + 34, h * 0.37), fill=dk + (255,)); d.rectangle(S(x - 34, h * 0.81, x + 34, h * 0.84), fill=dk + (255,))
        for k_ in range(3):
            d.rectangle(S(20 - k_ * 10, h * 0.84 + k_ * 18, w - 20 + k_ * 10, h * 0.84 + (k_ + 1) * 18), fill=tuple(int(v * (0.9 - 0.06 * k_)) for v in col) + (255,))
        return _done(im, w, h)
    return gcache(("bank", label, w, h, col), mk)


def app_phone_el(balance="$0.00", hl=None):
    def mk():
        w, h, sc = 420, 760, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, h - 1), 60 * sc, fill=(24, 24, 30, 255))
        shape_grad(im, lambda m: m.rounded_rectangle(S(18, 18, w - 18, h - 18), 46 * sc, fill=255), (250, 246, 236), (236, 230, 216))
        d.rounded_rectangle(S(150, 30, 270, 54), 12 * sc, fill=(24, 24, 30, 255))
        d.rounded_rectangle(S(40, 90, 380, 330), 30 * sc, fill=MINT + (255,))
        d.text((210 * sc, 140 * sc), "MY BALANCE", font=font(F_BOLD, 28 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text((210 * sc, 225 * sc), balance, font=font(F_BLACK, 84 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.rounded_rectangle(S(110, 270, 310, 314), 22 * sc, fill=(255, 255, 255, 255))
        d.text((210 * sc, 292 * sc), "RELOAD", font=font(F_BLACK, 26 * sc), fill=MINT + (255,), anchor="mm")
        for i, (a, b) in enumerate((("Latte", "-$5.45"), ("Reload", "+$25.00"), ("Cold brew", "-$4.95"))):
            y = 380 + i * 80
            d.rounded_rectangle(S(40, y, 380, y + 64), 18 * sc, fill=(255, 255, 255, 255))
            d.text((64 * sc, (y + 32) * sc), a, font=font(F_SEMI, 26 * sc), fill=INK + (255,), anchor="lm")
            d.text((356 * sc, (y + 32) * sc), b, font=font(F_BOLD, 26 * sc), fill=((22, 150, 70) if b[0] == "+" else INK) + (255,), anchor="rm")
        return _done(im, w, h)
    return gcache(("appphone", balance, hl), mk)


def loan_doc_el():
    def mk():
        w, h, sc = 420, 540, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(14, 16, w - 2, h - 2), fill=(0, 0, 0, 60)))
        d.rectangle(S(0, 0, w - 14, h - 16), fill=(255, 255, 255, 255))
        d.text(((w - 14) / 2 * sc, 70 * sc), "LOAN", font=font(F_BLACK, 70 * sc), fill=INK + (255,), anchor="mm")
        for i in range(7):
            y = 140 + i * 40; d.rounded_rectangle(S(40, y, w - 60 - (i % 3) * 40, y + 14), 6 * sc, fill=(210, 214, 224, 255))
        d.line(S(200, 450, 360, 450), fill=INK + (255,), width=3 * sc)
        d.line(S(210, 440, 240, 420, 260, 445, 300, 418, 330, 440), fill=(40, 60, 160, 255), width=4 * sc, joint="curve")
        return _done(im, w, h)
    return gcache("loan", mk)


def stamp_el(text, col=RED_, size=70):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 60), int(size * 1.6); sc = 2
        im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(4, 4, w - 4, h - 4), 12 * sc, outline=tuple(col) + (240,), width=8 * sc)
        d.text((w / 2 * sc, h / 2 * sc), text, font=fn, fill=tuple(col) + (240,), anchor="mm")
        return _done(im, w, h)
    return gcache(("stamp", text, col, size), mk)


def giftcard_el(col=MINT, label="GIFT CARD"):
    def mk():
        w, h, sc = 340, 214, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(6, 8, w - 1, h - 1), 22 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 8, h - 10), 22 * sc, fill=255), tuple(min(255, v + 30) for v in col), tuple(int(v * 0.75) for v in col))
        cx, cy = 70, 100
        d.ellipse(S(cx - 30, cy - 40, cx + 30, cy + 40), fill=(255, 255, 255, 230)); d.arc(S(cx - 14, cy - 38, cx + 14, cy + 38), 250, 110, fill=tuple(col) + (255,), width=6 * sc)
        d.text((210 * sc, 82 * sc), label, font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.rounded_rectangle(S(130, 120, 300, 136), 6 * sc, fill=(255, 255, 255, 140))
        return _done(im, w, h)
    return gcache(("gcard", col, label), mk)


def drawer_el():
    def mk():
        w, h, sc = 700, 420, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.polygon(S(60, 40, 640, 40, 700, 200, 0, 200), fill=255), (150, 96, 56), (120, 72, 40))
        for i, (x, col) in enumerate(((120, MINT), (230, (230, 70, 60)), (340, (250, 180, 40)), (450, (90, 120, 230)), (540, MINT))):
            d.rounded_rectangle(S(x, 70 + (i % 2) * 14, x + 120, 190), 14 * sc, fill=tuple(col) + (255,))
        shape_grad(im, lambda m: m.rectangle(S(0, 200, 700, 400), fill=255), (176, 116, 70), (130, 80, 44))
        d.rounded_rectangle(S(280, 280, 420, 314), 16 * sc, fill=(230, 200, 140, 255))
        for i in range(6):
            a = math.pi * (0.55 + i * 0.09)
            d.line(S(700, 40, 700 + 260 * math.cos(a), 40 + 260 * math.sin(a)), fill=(255, 255, 255, 230), width=2 * sc)
        for r in (70, 130, 190):
            pts = [(700 + r * math.cos(math.pi * (0.55 + i * 0.09)), 40 + r * math.sin(math.pi * (0.55 + i * 0.09))) for i in range(6)]
            d.line([(x * sc, y * sc) for x, y in pts], fill=(255, 255, 255, 230), width=2 * sc)
        return _done(im, w, h)
    return gcache("drawer", mk)


def counter_el(label, col, w=420, h=300):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rectangle(S(0, 110, w, h), fill=255), col, tuple(int(v * 0.7) for v in col))
        d.rectangle(S(0, 96, w, 118), fill=(250, 250, 252, 255))
        d.rounded_rectangle(S(w / 2 - 120, 10, w / 2 + 120, 80), 16 * sc, fill=INK + (255,))
        d.text((w / 2 * sc, 45 * sc), label, font=font(F_BLACK, 40 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("counter", label, col, w, h), mk)
