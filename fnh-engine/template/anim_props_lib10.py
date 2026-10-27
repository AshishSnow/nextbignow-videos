# ================= reusable prop library from ep 10 (sugar rush myth): candy, lollipop, pumpkin bucket, sugar cube (glucose),
# sweetener packet, test cups, pancreas, stomach, insulin key, cell with a locked door, blood-sugar gauge, wall thermostat,
# rating clipboard, party hat, balloon, witch hat, ghost sheet, wall clock, tooth with a cavity, blindfold, mom, scientist =================
SCHEMES["night"] = ((10, 8, 34), (52, 30, 116), (16, 10, 44), (0.25, 0.18, 0.55))
SCHEMES["lime"] = ((60, 130, 10), (150, 210, 40), (60, 120, 10), (0.25, 0.45, 0.05))
CANDY_COLS = [(255, 70, 110), (60, 160, 255), (255, 190, 30), (120, 210, 80), (190, 90, 255)]
PANC = (255, 196, 92); PANC_D = (214, 130, 40); STOM = (255, 150, 170); STOM_D = (210, 90, 120)
SUGAR_W = (255, 255, 255); KEY_G = (255, 206, 60); KEY_D = (190, 130, 20); CELL = (120, 220, 200); CELL_D = (30, 150, 140)


def candy_el(col=(255, 70, 110)):
    def mk():
        w, h, sc = 300, 150, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        dark = tuple(int(c * 0.65) for c in col)
        def wings(m):
            m.polygon(S(70, 75, 8, 20, 22, 75, 8, 130), fill=255); m.polygon(S(230, 75, 292, 20, 278, 75, 292, 130), fill=255)
        def body(m): m.ellipse(S(62, 28, 238, 122), fill=255)
        _outline(im, lambda m: (wings(m), body(m)), 11)
        shape_grad(im, wings, tuple(min(255, c + 40) for c in col), dark)
        shape_grad(im, body, tuple(min(255, c + 60) for c in col), dark)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        for i in range(4): _masked(im, bm, lambda q, i=i: q.line(S(90 + 40 * i, 20, 60 + 40 * i, 130), fill=(255, 255, 255, 90), width=12 * sc))
        _ov(im, lambda q: q.ellipse(S(92, 40, 150, 62), fill=(255, 255, 255, 170)))
        for x in (64, 236): d.line(S(x, 52, x, 98), fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("candy", col), mk)


def lollipop_el(col=(255, 70, 110)):
    def mk():
        w, h, sc = 220, 420, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(98, 180, 122, 410), 10 * sc, fill=INK + (255,)); d.rounded_rectangle(S(103, 185, 117, 405), 6 * sc, fill=(250, 246, 236, 255))
        d.ellipse(S(10, 10, 210, 210), fill=INK + (255,)); d.ellipse(S(18, 18, 202, 202), fill=(255, 255, 255, 255))
        for i in range(7):
            r0 = 92 - i * 13
            d.arc(S(110 - r0, 110 - r0, 110 + r0, 110 + r0), i * 50, i * 50 + 230, fill=tuple(col) + (255,), width=10 * sc)
        _ov(im, lambda q: q.ellipse(S(44, 38, 100, 80), fill=(255, 255, 255, 150)))
        return _done(im, w, h)
    return gcache(("lolli", col), mk)


def bucket_el(full=True):
    """jack-o'-lantern candy pail (generic) with candy on top."""
    def mk():
        w, h, sc = 420, 440, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.arc(S(60, 20, 360, 300), 190, 350, fill=INK + (255,), width=12 * sc)
        if full:
            for i, (x, y, c) in enumerate(((140, 120, 0), (230, 108, 1), (300, 126, 2), (190, 104, 3), (100, 136, 4))):
                el = candy_el(CANDY_COLS[c]); pil = _pil_from_el(scale_el(el, 0.45), int(135 * sc), int(68 * sc))
                pil = pil.rotate(25 * (i - 2), expand=True); im.alpha_composite(pil, (int((x - pil.width / sc / 2) * sc), int((y - pil.height / sc / 2) * sc)))
        def body(m):
            m.ellipse(S(30, 120, 390, 430), fill=255)
        _outline(im, body, 13)
        shape_grad(im, body, (255, 170, 60), (220, 90, 10))
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        for x in (120, 210, 300): _masked(im, bm, lambda q, x=x: q.arc(S(x - 70, 120, x + 70, 430), 70, 290, fill=(190, 80, 10, 120), width=5 * sc))
        _ov(im, lambda q: q.ellipse(S(80, 150, 170, 200), fill=(255, 255, 255, 110)))
        d.ellipse(S(60, 132, 360, 176), fill=(150, 60, 10, 255))
        for ex in (150, 270): d.polygon(S(ex - 34, 290, ex + 34, 290, ex, 232), fill=(60, 20, 10, 255))
        d.chord(S(130, 310, 290, 400), 0, 180, fill=(60, 20, 10, 255))
        for tx in (175, 245): d.rectangle(S(tx - 12, 352, tx + 12, 372), fill=(255, 150, 40, 255))
        return _done(im, w, h)
    return gcache(("bucket", full), mk)


def sugar_el(mood="happy", look=(0, 0)):
    """sugar cube = glucose, the fuel (cartoon, not to scale)."""
    def mk():
        w, h, sc = 200, 200, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(14, 14, 186, 186), 30 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(22, 22, 178, 178), 24 * sc, fill=255), (255, 255, 255), (214, 222, 236))
        rng = np.random.default_rng(3)
        for _ in range(26):
            x, y = rng.uniform(34, 166), rng.uniform(34, 166); d.rectangle(S(x, y, x + 6, y + 6), fill=(196, 206, 222, 255))
        _ov(im, lambda q: q.rounded_rectangle(S(34, 30, 110, 54), 10 * sc, fill=(255, 255, 255, 220)))
        if mood:
            _eyes(d, S, sc, [(76, 92), (124, 92)], 15, look, sly=(mood == "sly"), happy=(mood == "happy"))
            if mood in ("happy", "n"): d.chord(S(80, 112, 120, 146), 0, 180, fill=(70, 14, 24, 255))
            elif mood == "o": d.ellipse(S(88, 118, 112, 146), fill=(70, 14, 24, 255))
            else: d.arc(S(80, 112, 122, 140), 10, 150, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("sugar", mood, look), mk)


def packet_el():
    def mk():
        w, h, sc = 300, 200, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(6, 6, 294, 194), 14 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(14, 14, 286, 186), 10 * sc, fill=255), (255, 170, 210), (230, 110, 170))
        for x in range(20, 290, 14): d.line(S(x, 16, x + 6, 30), fill=(255, 255, 255, 160), width=2 * sc)
        d.text((150 * sc, 100 * sc), "SWEETENER", font=font(F_BLACK, 36 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text((150 * sc, 146 * sc), "no sugar", font=font(F_BOLD, 24 * sc), fill=(120, 20, 70, 255), anchor="mm")
        return _done(im, w, h)
    return gcache("packet", mk)


def cup2_el(label="", col=(255, 120, 60), level=0.75):
    """plain party cup with juice (label = big letter on the side)."""
    level = round(level * 10) / 10
    def mk():
        w, h, sc = 240, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: m.polygon(S(20, 20, 220, 20, 190, 290, 50, 290), fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, (250, 250, 255), (210, 214, 230))
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        top = 290 - 260 * level
        _masked(im, bm, lambda q: q.rectangle(S(0, top, w, 290), fill=tuple(col) + (200,)))
        _masked(im, bm, lambda q: q.line(S(46, 30, 66, 280), fill=(255, 255, 255, 170), width=12 * sc))
        d.rectangle(S(14, 14, 226, 34), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        if label: d.text((122 * sc, 180 * sc), label, font=font(F_BLACK, 96 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("cup2", label, col, level), mk)


def pancreas_el(awake=False):
    """pancreas: long lobed organ, head on the right, tail tapering left (cartoon)."""
    def mk():
        w, h, sc = 520, 240, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def shp(m):
            m.ellipse(S(330, 40, 500, 210), fill=255)
            m.polygon(S(40, 90, 120, 60, 240, 70, 360, 60, 380, 190, 260, 170, 140, 160, 50, 150), fill=255)
            m.ellipse(S(20, 86, 90, 156), fill=255)
            for x in range(70, 360, 46): m.ellipse(S(x, 52, x + 56, 104), fill=255); m.ellipse(S(x, 128, x + 56, 178), fill=255)
        _outline(im, shp, 13)
        shape_grad(im, shp, (255, 226, 140), PANC_D)
        bm = Image.new("L", im.size, 0); shp(ImageDraw.Draw(bm))
        rng = np.random.default_rng(7)
        for _ in range(40):
            x, y = rng.uniform(40, 480), rng.uniform(70, 190); r_ = rng.uniform(5, 11)
            _masked(im, bm, lambda q, x=x, y=y, r_=r_: q.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(200, 120, 40, 90)))
        _masked(im, bm, lambda q: q.ellipse(S(350, 56, 430, 92), fill=(255, 255, 255, 130)))
        if awake:
            _eyes(d, S, sc, [(390, 120), (446, 120)], 18, (-0.4, 0), happy=False)
            d.chord(S(392, 150, 446, 186), 0, 180, fill=(70, 14, 24, 255))
        else:
            for ex in (390, 446): d.arc(S(ex - 18, 110, ex + 18, 134), 20, 160, fill=INK + (255,), width=5 * sc)
            d.arc(S(400, 152, 436, 172), 200, 340, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("pancreas", awake), mk)


def stomach_el():
    def mk():
        w, h, sc = 360, 380, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def shp(m):
            m.ellipse(S(40, 60, 330, 330), fill=255)
            m.rounded_rectangle(S(70, 10, 130, 140), 26 * sc, fill=255)
            m.polygon(S(250, 270, 330, 300, 340, 370, 290, 360), fill=255)
        _outline(im, shp, 13)
        shape_grad(im, shp, (255, 190, 200), STOM_D)
        bm = Image.new("L", im.size, 0); shp(ImageDraw.Draw(bm))
        for i in range(4): _masked(im, bm, lambda q, i=i: q.arc(S(80 + i * 30, 100 + i * 24, 300 - i * 10, 320 - i * 10), 200, 320, fill=(200, 80, 110, 120), width=6 * sc))
        _masked(im, bm, lambda q: q.ellipse(S(80, 90, 150, 140), fill=(255, 255, 255, 120)))
        return _done(im, w, h)
    return gcache("stomach", mk)


def ikey_el(face=True):
    """insulin key (cartoon): gold key with a small happy face on the bow."""
    def mk():
        w, h, sc = 380, 180, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def shp(m):
            m.ellipse(S(10, 10, 170, 170), fill=255)
            m.rounded_rectangle(S(150, 70, 370, 110), 12 * sc, fill=255)
            m.rectangle(S(290, 104, 316, 150), fill=255); m.rectangle(S(330, 104, 356, 136), fill=255)
        _outline(im, shp, 11)
        shape_grad(im, shp, (255, 236, 140), KEY_D)
        _ov(im, lambda q: q.ellipse(S(36, 26, 100, 60), fill=(255, 255, 255, 170)))
        if face:
            _eyes(d, S, sc, [(66, 88), (114, 88)], 14, (0.3, 0), happy=True)
            d.chord(S(68, 104, 112, 138), 0, 180, fill=(70, 14, 24, 255))
        else: d.ellipse(S(60, 60, 120, 120), fill=(0, 0, 0, 0))
        return _done(im, w, h)
    return gcache(("ikey", face), mk)


def cell_el(open_k=0.0, sugar_in=0):
    """body cell: membrane circle, nucleus, a door with a keyhole on the left (opens with open_k 0..1)."""
    open_k = round(clamp(open_k) * 8) / 8
    def mk():
        w, h, sc = 520, 520, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 10, 510, 510), fill=INK + (255,))
        d.ellipse(S(22, 22, 498, 498), fill=CELL_D + (255,))
        shape_grad(im, lambda m: m.ellipse(S(44, 44, 476, 476), fill=255), (200, 250, 236), (120, 214, 196))
        d.ellipse(S(270, 180, 420, 330), fill=(120, 90, 200, 255), outline=INK + (255,), width=5 * sc)
        d.ellipse(S(310, 220, 360, 262), fill=(170, 140, 240, 255))
        for i in range(sugar_in):
            x, y = 200 + (i % 3) * 60, 340 + (i // 3) * 56
            d.rounded_rectangle(S(x - 22, y - 22, x + 22, y + 22), 8 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=3 * sc)
        _ov(im, lambda q: q.ellipse(S(90, 70, 220, 130), fill=(255, 255, 255, 120)))
        # door in the membrane (left side)
        d.rounded_rectangle(S(0, 170, 100, 350), 16 * sc, fill=INK + (255,))
        d.rounded_rectangle(S(8, 178, 92, 342), 12 * sc, fill=(30, 20, 40, 255))
        dw = 92 * (1 - open_k)
        if dw > 8:
            d.rounded_rectangle(S(8, 178, max(14, dw), 342), 12 * sc, fill=(200, 120, 60, 255), outline=INK + (255,), width=5 * sc)
            if dw > 40:
                d.rounded_rectangle(S(20, 194, dw - 12, 250), 6 * sc, outline=(150, 80, 30, 255), width=4 * sc)
                kx = dw * 0.55; d.ellipse(S(kx - 12, 270, kx + 12, 294), fill=INK + (255,)); d.polygon(S(kx - 7, 288, kx + 7, 288, kx + 11, 326, kx - 11, 326), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("cell", open_k, sugar_in), mk)


def sugar_gauge(f, x, y, r, v, band=(0.4, 0.6), label="BLOOD SUGAR", t=0.0):
    """semicircle dial (0..1): green 'tight range' band; needle at v. Drawn directly (crisp at any size)."""
    cv2.ellipse(f, (int(x), int(y)), (int(r + 26), int(r + 26)), 0, 180, 360, C(INK), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(r + 14), int(r + 14)), 0, 180, 360, C((250, 248, 240)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - r - 26), int(y)), (int(x + r + 26), int(y + 40)), C(INK), -1, cv2.LINE_AA)
    for a0, a1, col in ((180, 180 + 180 * band[0], (120, 180, 255)), (180 + 180 * band[0], 180 + 180 * band[1], (40, 200, 100)),
                        (180 + 180 * band[1], 360, (255, 110, 80))):
        cv2.ellipse(f, (int(x), int(y)), (int(r - 10), int(r - 10)), 0, a0, a1, C(col), int(r * 0.22), cv2.LINE_AA)
    for i in range(11):
        a = math.radians(180 + 18 * i)
        cv2.line(f, (int(x + (r - 46) * math.cos(a)), int(y + (r - 46) * math.sin(a))), (int(x + (r - 26 - (10 if i % 5 else 24)) * math.cos(a) - 0), int(y + (r - 26 - (10 if i % 5 else 24)) * math.sin(a))), C(INK), 4, cv2.LINE_AA)
    a = math.radians(180 + 180 * clamp(v))
    cv2.line(f, (int(x), int(y)), (int(x + (r - 30) * math.cos(a)), int(y + (r - 30) * math.sin(a))), C(RED_), 14, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 26, C(INK), -1, cv2.LINE_AA)
    comp(f, chip(label, INK, WHITE, 26), x, y + 20)


def thermostat_el(temp="21"):
    def mk():
        w, h, sc = 360, 360, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 10, 350, 350), fill=INK + (255,))
        shape_grad(im, lambda m: m.ellipse(S(22, 22, 338, 338), fill=255), (250, 250, 252), (196, 200, 214))
        d.ellipse(S(70, 70, 290, 290), fill=(34, 40, 56, 255))
        for i in range(24):
            a = math.radians(140 + i * 260 / 23); r0, r1 = 124, 140
            d.line(S(180 + r0 * math.cos(a), 180 + r0 * math.sin(a), 180 + r1 * math.cos(a), 180 + r1 * math.sin(a)), fill=(120, 126, 140, 255), width=3 * sc)
        d.text((180 * sc, 176 * sc), temp, font=font(F_BLACK, 96 * sc), fill=(120, 230, 160, 255), anchor="mm")
        d.text((180 * sc, 250 * sc), "STEADY", font=font(F_BOLD, 22 * sc), fill=(160, 170, 190, 255), anchor="mm")
        _ov(im, lambda q: q.ellipse(S(60, 34, 170, 80), fill=(255, 255, 255, 150)))
        return _done(im, w, h)
    return gcache(("tstat", temp), mk)


def rating_board(f, x, y, s, lvl, title="HOW HYPER?", t=0.0):
    """clipboard with a 1..5 'hyper' scale; lvl 0..1 fills the bars (mom's rating)."""
    el = gcache("clipb", lambda: _clip_el())
    comp(f, scale_el(el, s), x, y)
    comp(f, chip(title, INK, WHITE, int(24 * s + 2)), x, y - 150 * s)
    for i in range(5):
        bx = x - 120 * s + i * 60 * s; hh = (30 + 22 * i) * s; on = lvl * 5 > i + 0.05
        col = (40, 200, 100) if i < 2 else ((255, 190, 30) if i < 4 else (240, 60, 50))
        cv2.rectangle(f, (int(bx - 20 * s), int(y + 120 * s - hh)), (int(bx + 20 * s), int(y + 120 * s)), C(col if on else (220, 222, 230)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(bx - 20 * s), int(y + 120 * s - hh)), (int(bx + 20 * s), int(y + 120 * s)), C(INK), max(2, int(4 * s)), cv2.LINE_AA)


def _clip_el():
    w, h, sc = 380, 480, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
    d.rounded_rectangle(S(10, 30, 370, 470), 26 * sc, fill=INK + (255,)); d.rounded_rectangle(S(20, 40, 360, 460), 20 * sc, fill=(190, 130, 70, 255))
    d.rectangle(S(46, 70, 334, 436), fill=(255, 255, 255, 255))
    for yy in range(120, 260, 34): d.line(S(70, yy, 310, yy), fill=(200, 206, 220, 255), width=4 * sc)
    d.rounded_rectangle(S(120, 10, 260, 70), 14 * sc, fill=(150, 156, 172, 255), outline=INK + (255,), width=4 * sc)
    return _done(im, w, h)


def party_hat_el(col=(255, 70, 110)):
    def mk():
        w, h, sc = 180, 220, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        shp = lambda m: m.polygon(S(90, 20, 160, 200, 20, 200), fill=255)
        _outline(im, shp, 9); shape_grad(im, shp, tuple(min(255, c + 50) for c in col), tuple(int(c * 0.7) for c in col))
        bm = Image.new("L", im.size, 0); shp(ImageDraw.Draw(bm))
        for i in range(4): _masked(im, bm, lambda q, i=i: q.line(S(10, 200 - i * 45, 170, 140 - i * 45), fill=(255, 255, 255, 150), width=10 * sc))
        d.ellipse(S(70, 0, 110, 40), fill=(255, 230, 80, 255), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("phat", col), mk)


def witch_hat_el():
    def mk():
        w, h, sc = 300, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(4, 190, 296, 250), fill=INK + (255,)); d.ellipse(S(12, 196, 288, 242), fill=(60, 30, 100, 255))
        d.polygon(S(150, 6, 214, 210, 86, 210), fill=INK + (255,)); d.polygon(S(150, 20, 204, 206, 96, 206), fill=(80, 40, 130, 255))
        d.rectangle(S(92, 178, 208, 204), fill=(255, 150, 40, 255))
        return _done(im, w, h)
    return gcache("witchhat", mk)


def balloon_el(col=(255, 70, 110)):
    def mk():
        w, h, sc = 200, 420, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.line(S(100, 250, 110, 300, 92, 350, 104, 415), fill=INK + (255,), width=3 * sc, joint="curve")
        shp = lambda m: (m.ellipse(S(14, 10, 186, 240), fill=255), m.polygon(S(88, 236, 112, 236, 100, 256), fill=255))
        _outline(im, shp, 9); shape_grad(im, shp, tuple(min(255, c + 60) for c in col), tuple(int(c * 0.7) for c in col))
        _ov(im, lambda q: q.ellipse(S(46, 40, 90, 100), fill=(255, 255, 255, 160)))
        return _done(im, w, h)
    return gcache(("balloon", col), mk)


def ghost_el():
    def mk():
        w, h, sc = 300, 340, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        shp = lambda m: (m.ellipse(S(30, 10, 270, 240), fill=255), m.rectangle(S(30, 120, 270, 300), fill=255),
                         [m.ellipse(S(30 + i * 60, 270, 90 + i * 60, 330), fill=255) for i in range(4)])
        _outline(im, shp, 11); shape_grad(im, shp, (255, 255, 255), (210, 214, 236))
        for ex in (115, 185): d.ellipse(S(ex - 20, 100, ex + 20, 150), fill=INK + (255,))
        d.ellipse(S(130, 170, 170, 220), fill=INK + (255,))
        return _done(im, w, h)
    return gcache("ghost", mk)


def clock_el(hh=11, mm=0):
    def mk():
        w, h, sc = 300, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(6, 6, 294, 294), fill=INK + (255,)); shape_grad(im, lambda m: m.ellipse(S(20, 20, 280, 280), fill=255), (255, 255, 255), (220, 224, 236))
        for i in range(12):
            a = math.radians(i * 30 - 90); d.line(S(150 + 104 * math.cos(a), 150 + 104 * math.sin(a), 150 + 120 * math.cos(a), 150 + 120 * math.sin(a)), fill=INK + (255,), width=6 * sc)
        a1 = math.radians((hh % 12 + mm / 60) * 30 - 90); a2 = math.radians(mm * 6 - 90)
        d.line(S(150, 150, 150 + 66 * math.cos(a1), 150 + 66 * math.sin(a1)), fill=INK + (255,), width=12 * sc)
        d.line(S(150, 150, 150 + 100 * math.cos(a2), 150 + 100 * math.sin(a2)), fill=INK + (255,), width=8 * sc)
        d.ellipse(S(138, 138, 162, 162), fill=RED_ + (255,))
        return _done(im, w, h)
    return gcache(("clock", hh, mm), mk)


def tooth(f, x, y, s, t, mood="sad", cavity=1.0):
    comp(f, scale_el(molar_el(), s), x, y)
    if cavity > 0: cv2.ellipse(f, (int(x + 50 * s), int(y - 120 * s)), (int(34 * s * cavity), int(24 * s * cavity)), 20, 0, 360, C((90, 60, 40)), -1, cv2.LINE_AA)
    for ex in (-40, 40):
        cv2.circle(f, (int(x + ex * s), int(y - 40 * s)), int(14 * s), C(INK), -1, cv2.LINE_AA)
    if mood == "sad": cv2.ellipse(f, (int(x), int(y + 10 * s)), (int(30 * s), int(16 * s)), 0, 200, 340, C(INK), max(2, int(6 * s)), cv2.LINE_AA)
    else: cv2.ellipse(f, (int(x), int(y - 4 * s)), (int(30 * s), int(18 * s)), 0, 20, 160, C(INK), max(2, int(6 * s)), cv2.LINE_AA)


def head_pos(x, y, s, bob=0.0, lean=0.0):
    """centre of Chubby's head element for chub(f, x, y, s, bob=, lean=) (squash 0)."""
    lr = math.radians(lean)
    return x + 40 * s * math.sin(lr) + 10 * s * math.sin(lr), y - 420 * s + 1.5 * bob * s


def blindfold(f, x, y, s, bob=0.0, lean=0.0, col=(30, 30, 40)):
    hx, hy = head_pos(x, y, s, bob, lean); ey = hy - 2 * s
    cv2.rectangle(f, (int(hx - 96 * s), int(ey - 26 * s)), (int(hx + 96 * s), int(ey + 24 * s)), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx - 92 * s), int(ey - 21 * s)), (int(hx + 92 * s), int(ey + 19 * s)), C(col), -1, cv2.LINE_AA)
    cv2.line(f, (int(hx + 92 * s), int(ey)), (int(hx + 130 * s), int(ey + 30 * s)), C(col), max(2, int(10 * s)), cv2.LINE_AA)


MOM_SHIRT = (236, 72, 140); MOM_HAIR = (110, 60, 40); LAB = (240, 244, 252)


def mom(f, x, y, s=1.0, bob=0.0, lean=0.0, **kw):
    """Chubby-style mom: long hair + bun drawn behind the head, pink shirt."""
    hx, hy = head_pos(x, y, s, bob, lean)
    cv2.ellipse(f, (int(hx), int(hy + 30 * s)), (int(112 * s), int(122 * s)), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy + 30 * s)), (int(104 * s), int(114 * s)), 0, 0, 360, C(MOM_HAIR), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx), int(hy - 104 * s)), int(42 * s), C(INK), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx), int(hy - 104 * s)), int(35 * s), C(MOM_HAIR), -1, cv2.LINE_AA)
    return chub(f, x, y, s, bob=bob, lean=lean, shirt=MOM_SHIRT, **kw)


def scientist(f, x, y, s=1.0, bob=0.0, lean=0.0, goggles=True, **kw):
    """Chubby in a white lab coat + goggles pushed up on the forehead."""
    h = chub(f, x, y, s, bob=bob, lean=lean, shirt=LAB, **kw)
    if goggles:
        hx, hy = head_pos(x, y, s, bob, lean)
        cv2.line(f, (int(hx - 88 * s), int(hy - 52 * s)), (int(hx + 88 * s), int(hy - 52 * s)), C(INK), max(2, int(10 * s)), cv2.LINE_AA)
        for ex in (-30, 30):
            cv2.circle(f, (int(hx + ex * s), int(hy - 56 * s)), int(24 * s), C(INK), -1, cv2.LINE_AA)
            cv2.circle(f, (int(hx + ex * s), int(hy - 56 * s)), int(17 * s), C((150, 220, 255)), -1, cv2.LINE_AA)
    return h


def test_card_el():
    """one 'blind test' paper (for the pile of 23)."""
    def mk():
        w, h, sc = 200, 240, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(6, 6, 194, 234), 14 * sc, fill=INK + (255,)); d.rounded_rectangle(S(14, 14, 186, 226), 10 * sc, fill=(255, 255, 255, 255))
        d.rectangle(S(30, 34, 170, 58), fill=(60, 140, 240, 255))
        for yy in (84, 112, 140): d.line(S(30, yy, 170, yy), fill=(190, 196, 210, 255), width=5 * sc)
        d.rectangle(S(40, 168, 80, 206), fill=(255, 190, 30, 255)); d.rectangle(S(110, 168, 150, 206), fill=(255, 190, 30, 255))
        d.line(S(30, 208, 170, 208), fill=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache("testcard", mk)
