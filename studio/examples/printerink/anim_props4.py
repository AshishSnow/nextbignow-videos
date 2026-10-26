# ================= props for "Printer ink costs more than champagne" (generic, no logos / trade dress) =================
CYAN_ = (0, 174, 239); MAG_ = (236, 0, 140); YELI = (255, 222, 0); BLK_ = (40, 40, 48)
GLASSC = (200, 236, 255)


def printer_el(w=620, h=440, paper=0.0, smile=True):
    """generic home inkjet printer: grey body, paper tray, output slot, little screen + buttons; `paper` 0..1 sheet out"""
    paper = round(paper, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        # back paper tray
        d.polygon(S(150, 70, w - 150, 70, w - 120, 150, 120, 150), fill=(210, 214, 222, 255), outline=(70, 74, 86, 255))
        d.rectangle(S(190, 20, w - 190, 120), fill=(255, 255, 255, 255), outline=(170, 174, 184, 255), width=3 * sc)
        _ov(im, lambda q: q.rounded_rectangle(S(24, 132, w - 4, h - 4), 40 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 120, w - 20, h - 20), 40 * sc, fill=255), (246, 247, 250), (190, 196, 208))
        d.rounded_rectangle(S(10, 120, w - 20, h - 20), 40 * sc, outline=(70, 74, 86, 255), width=5 * sc)
        # top lid line + screen
        d.line(S(40, 200, w - 50, 200), fill=(150, 156, 170, 255), width=4 * sc)
        d.rounded_rectangle(S(w - 230, 140, w - 70, 188), 10 * sc, fill=(40, 60, 90, 255))
        d.text(((w - 150) * sc, 164 * sc), ":)" if smile else ":(", font=font(F_BLACK, 30 * sc), fill=(120, 230, 255, 255), anchor="mm")
        for i, col in enumerate((GRN_, (250, 170, 40), RED_)):
            d.ellipse(S(60 + i * 46, 150, 92 + i * 46, 182), fill=col + (255,), outline=(70, 74, 86, 255), width=2 * sc)
        # output slot
        d.rounded_rectangle(S(90, 290, w - 100, 330), 14 * sc, fill=(50, 54, 64, 255))
        if paper > 0:
            ph = 30 + 110 * paper
            d.rectangle(S(150, 300, w - 160, 300 + ph), fill=(255, 255, 255, 255), outline=(170, 174, 184, 255), width=2 * sc)
            for k_ in range(int(4 * paper)):
                d.line(S(180, 330 + k_ * 22, w - 200 - (k_ % 2) * 60, 330 + k_ * 22), fill=(150, 156, 170, 255), width=5 * sc)
        _ov(im, lambda q: q.polygon(S(40, 210, 140, 210, 80, h - 40, 30, h - 40), fill=(255, 255, 255, 60)))
        return _done(im, w, h)
    return gcache(("printer", w, h, paper, smile), mk)


def cartridge_el(col=CYAN_, level=1.0, w=180, h=250, label="INK"):
    """generic ink cartridge with a see-through window showing the level"""
    level = round(level, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(12, 14, w - 2, h - 2), 20 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 6, w - 10, h - 10), 20 * sc, fill=255), (70, 74, 86), (36, 38, 46))
        d.rounded_rectangle(S(24, 40, w - 30, h - 70), 12 * sc, fill=(230, 236, 244, 255))
        top = 40 + (h - 110) * (1 - level)
        if level > 0.01: d.rounded_rectangle(S(24, top, w - 30, h - 70), 12 * sc, fill=tuple(col) + (255,))
        d.rounded_rectangle(S(24, 40, w - 30, h - 70), 12 * sc, outline=(20, 20, 26, 255), width=4 * sc)
        _ov(im, lambda q: q.rectangle(S(34, 48, 48, h - 80), fill=(255, 255, 255, 110)))
        d.text(((w - 6) / 2 * sc, (h - 38) * sc), label, font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("cart", col, level, w, h, label), mk)


def bottle_el(w=230, h=640):
    """generic dark-green sparkling-wine bottle with gold foil, blank cream label (no brand)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]; cx = w / 2
        body = lambda m: (m.rounded_rectangle(S(cx - 100, 300, cx + 100, h - 6), 40 * sc, fill=255),
                          m.polygon(S(cx - 34, 120, cx + 34, 120, cx + 100, 330, cx - 100, 330), fill=255),
                          m.rectangle(S(cx - 34, 40, cx + 34, 140), fill=255))
        shape_grad(im, body, (30, 110, 70), (8, 46, 28))
        shape_grad(im, lambda m: m.polygon(S(cx - 38, 20, cx + 38, 20, cx + 46, 200, cx - 46, 200), fill=255), (255, 226, 130), (196, 146, 40))
        d.rounded_rectangle(S(cx - 30, 0, cx + 30, 36), 10 * sc, fill=(230, 190, 80, 255))
        d.rounded_rectangle(S(cx - 84, 400, cx + 84, 560), 14 * sc, fill=(250, 240, 214, 255), outline=(196, 156, 60, 255), width=5 * sc)
        d.line(S(cx - 54, 450, cx + 54, 450), fill=(196, 156, 60, 255), width=5 * sc)
        d.line(S(cx - 40, 490, cx + 40, 490), fill=(196, 156, 60, 255), width=4 * sc)
        d.line(S(cx - 54, 520, cx + 54, 520), fill=(196, 156, 60, 255), width=3 * sc)
        _ov(im, lambda q: q.rounded_rectangle(S(cx - 80, 320, cx - 56, h - 40), 12 * sc, fill=(255, 255, 255, 60)))
        return _done(im, w, h)
    return gcache(("bottle", w, h), mk)


def flute_el(w=200, h=420, fill=0.8):
    """champagne flute with bubbles"""
    fill = round(fill, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]; cx = w / 2
        lvl = 30 + 230 * (1 - fill)
        shape_grad(im, lambda m: m.polygon(S(cx - 54, lvl, cx + 54, lvl, cx + 40, 250, cx + 10, 280, cx - 10, 280, cx - 40, 250), fill=255),
                   (255, 236, 150), (238, 190, 60))
        for (bx, by) in ((cx - 18, 220), (cx + 10, 180), (cx - 6, 140), (cx + 20, 110), (cx - 24, 90)):
            if by > lvl: d.ellipse(S(bx - 6, by - 6, bx + 6, by + 6), outline=(255, 255, 255, 230), width=2 * sc)
        d.line(S(cx - 58, 20, cx - 40, 250, cx - 10, 285, cx + 10, 285, cx + 40, 250, cx + 58, 20), fill=(120, 150, 170, 255), width=5 * sc, joint="curve")
        d.line(S(cx, 285, cx, h - 30), fill=(150, 180, 200, 255), width=8 * sc)
        d.ellipse(S(cx - 64, h - 44, cx + 64, h - 16), fill=(200, 226, 240, 255), outline=(120, 150, 170, 255), width=4 * sc)
        _ov(im, lambda q: q.polygon(S(cx - 46, 40, cx - 34, 40, cx - 22, 240, cx - 30, 240), fill=(255, 255, 255, 110)))
        return _done(im, w, h)
    return gcache(("flute", w, h, fill), mk)


def drop_el(col=BLK_, r=120, label=""):
    """single liquid drop"""
    def mk():
        w, h = int(r * 2 + 20), int(r * 2.9 + 20); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]; cx = w / 2; cy = h - r - 10
        hi = tuple(min(255, int(c * 0.6 + 120)) for c in col); lo = tuple(int(c * 0.55) for c in col)
        shape_grad(im, lambda m: (m.ellipse(S(cx - r, cy - r, cx + r, cy + r), fill=255),
                                  m.polygon(S(cx, 10, cx + r * 0.86, cy - r * 0.5, cx - r * 0.86, cy - r * 0.5), fill=255)), hi, lo)
        _ov(im, lambda q: q.ellipse(S(cx - r * 0.6, cy - r * 0.5, cx - r * 0.25, cy + r * 0.05), fill=(255, 255, 255, 120)))
        if label: d.text((cx * sc, (cy + r * 0.15) * sc), label, font=font(F_BLACK, int(r * 0.8) * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("drop", col, r, label), mk)


def mousetrap_el(w=760, h=200):
    """wooden snap trap base (the printer sits on it as bait)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 70, w - 2, h - 2), 16 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 60, w - 12, h - 12), 16 * sc, fill=255), (236, 186, 120), (190, 130, 70))
        for k_ in range(6): d.line(S(30, 84 + k_ * 16, w - 40, 88 + k_ * 16), fill=(200, 146, 86, 255), width=2 * sc)
        d.rounded_rectangle(S(4, 60, w - 12, h - 12), 16 * sc, outline=(120, 76, 36, 255), width=4 * sc)
        d.line(S(40, 70, 40, 20, w - 52, 20, w - 52, 70), fill=(150, 156, 170, 255), width=10 * sc, joint="curve")
        d.ellipse(S(w / 2 - 30, 70, w / 2 + 30, 100), fill=(150, 156, 170, 255))
        return _done(im, w, h)
    return gcache(("trap", w, h), mk)


def beaker_el(level=0.0, col=BLK_, w=300, h=420, ticks=True):
    """measuring beaker filling with liquid"""
    level = round(level, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(30, 40, w - 30, h - 10), 24 * sc, fill=(255, 255, 255, 90)))
        if level > 0.01:
            top = 60 + (h - 90) * (1 - level)
            hi = tuple(min(255, int(c * 0.7 + 90)) for c in col)
            shape_grad(im, lambda m: m.rounded_rectangle(S(36, top, w - 36, h - 16), 20 * sc, fill=255), hi, tuple(int(c * 0.7) for c in col))
        d.rounded_rectangle(S(30, 40, w - 30, h - 10), 24 * sc, outline=(70, 90, 110, 255), width=6 * sc)
        d.line(S(20, 40, w - 20, 40), fill=(70, 90, 110, 255), width=6 * sc)
        if ticks:
            for k_ in range(1, 6):
                y = h - 16 - k_ * (h - 90) / 5
                d.line(S(w - 90, y, w - 36, y), fill=(255, 255, 255, 230), width=4 * sc)
        _ov(im, lambda q: q.rectangle(S(46, 60, 62, h - 30), fill=(255, 255, 255, 120)))
        return _done(im, w, h)
    return gcache(("beaker", level, col, w, h, ticks), mk)


def tv_el(lines, w=820, h=600, sub="LIVE INTERVIEW"):
    """generic TV set with a quote card on screen (no faces, no channel logos)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.line(S(w / 2 - 120, 0, w / 2, 60), fill=INK + (255,), width=8 * sc); d.line(S(w / 2 + 120, 0, w / 2, 60), fill=INK + (255,), width=8 * sc)
        _ov(im, lambda q: q.rounded_rectangle(S(16, 70, w - 4, h - 34), 40 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(4, 56, w - 16, h - 46), 40 * sc, fill=255), (70, 74, 90), (30, 32, 42))
        shape_grad(im, lambda m: m.rounded_rectangle(S(40, 92, w - 52, h - 120), 22 * sc, fill=255), (40, 70, 140), (16, 30, 80))
        d.text((80 * sc, 150 * sc), "“", font=font(F_BLACK, 130 * sc), fill=YEL_ + (255,), anchor="lm")
        y = 200; fn = font(F_BLACK, 46 * sc)
        for ln in lines:
            d.text(((w - 12) / 2 * sc, y * sc), ln, font=fn, fill=(255, 255, 255, 255), anchor="mm"); y += 64
        d.rounded_rectangle(S(40, h - 170, 330, h - 124), 8 * sc, fill=RED_ + (255,))
        d.text((185 * sc, (h - 147) * sc), sub, font=font(F_BLACK, 24 * sc), fill=(255, 255, 255, 255), anchor="mm")
        for x in (w * 0.25, w * 0.7): d.rounded_rectangle(S(x - 40, h - 50, x + 40, h - 4), 8 * sc, fill=(40, 42, 52, 255))
        return _done(im, w, h)
    return gcache(("tv", tuple(lines), w, h, sub), mk)


def receipt_el(n, w=380, row=58):
    """receipt that grows: n rows of 'INK REFILL'"""
    def mk():
        h = 120 + row * n + 60; sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        pts = [(0, 0), (w, 0), (w, h - 20)] + [(w - i * 20, h - (0 if i % 2 else 20)) for i in range(int(w / 20) + 1)] + [(0, h - 20)]
        _ov(im, lambda q: q.polygon([(x * sc + 8 * sc, y * sc + 10 * sc) for x, y in pts], fill=(0, 0, 0, 60)))
        d.polygon([(x * sc, y * sc) for x, y in pts], fill=(255, 255, 255, 255))
        d.text((w / 2 * sc, 50 * sc), "RECEIPT", font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.line(S(30, 90, w - 30, 90), fill=(170, 170, 180, 255), width=3 * sc)
        for i in range(n):
            y = 120 + i * row
            d.text((34 * sc, y * sc), "INK REFILL", font=font(F_BOLD, 28 * sc), fill=INK + (255,), anchor="lm")
            d.text(((w - 34) * sc, y * sc), "$$$", font=font(F_BLACK, 28 * sc), fill=RED_ + (255,), anchor="rm")
        return _done(im, w, h)
    return gcache(("receipt", n, w, row), mk)


def bar(f, x, base, w, hgt, col, k=1.0):
    """vertical bar from baseline, animated by k"""
    hh = max(2, int(hgt * clamp(k)))
    y0 = int(base - hh + 12); xs0, xs1 = int(x - w / 2 + 12), int(x + w / 2 + 12)
    f[y0:int(base), xs0:xs1] *= 0.7
    f[int(base - hh):int(base), int(x - w / 2):int(x + w / 2)] = np.array(C(col), np.float32)
    cv2.rectangle(f, (int(x - w / 2), int(base - hh)), (int(x + w / 2), int(base)), C(INK), 6, cv2.LINE_AA)
    return base - hh
