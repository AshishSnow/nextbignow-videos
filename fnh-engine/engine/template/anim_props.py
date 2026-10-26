# ================= drawn props (supersampled PIL, shaded) =================
def _canvas(w, h, sc=2):
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def _done(im, w, h): return el_from(im.resize((w, h), Image.LANCZOS))


def table_el():
    def mk():
        w, h, sc = 480, 360, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(222, 150, 258, 330), fill=(40, 34, 32, 255))
        d.ellipse(S(150, 318, 330, 352), fill=(40, 34, 32, 255))
        shape_grad(im, lambda m: m.polygon(S(20, 60, 460, 60, 476, 200, 4, 200), fill=255), (250, 250, 252), (214, 220, 232))
        for i in range(7):
            x = 40 + i * 66; d.line(S(x, 70, x - 6 + (i % 2) * 12, 198), fill=(200, 206, 220, 255), width=3 * sc)
        for i in range(12):
            x0 = 4 + i * 39.3; d.pieslice(S(x0, 186, x0 + 39.3, 214), 0, 180, fill=(214, 220, 232, 255))
        shape_grad(im, lambda m: m.ellipse(S(10, 30, 470, 92), fill=255), (255, 255, 255), (232, 236, 244))
        st = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
        for i in range(-3, 9): ds.line(S(30 + i * 56, 30, 90 + i * 56, 94), fill=(236, 80, 70, 90), width=12 * sc)
        em = Image.new("L", im.size, 0); ImageDraw.Draw(em).ellipse(S(12, 32, 468, 90), fill=255)
        im.paste(st, (0, 0), Image.fromarray(np.minimum(np.asarray(em), np.asarray(st.getchannel("A"))), "L"))
        return _done(im, w, h)
    return gcache("table", mk)


def chair_el(col=(232, 60, 40)):
    def mk():
        w, h, sc = 220, 380, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(int(c * 0.7) for c in col)
        d.rounded_rectangle(S(40, 10, 180, 190), 60 * sc, outline=col + (255,), width=16 * sc)
        d.line(S(70, 60, 70, 200), fill=col + (255,), width=10 * sc); d.line(S(150, 60, 150, 200), fill=col + (255,), width=10 * sc)
        d.ellipse(S(20, 186, 200, 236), fill=col + (255,)); d.ellipse(S(20, 180, 200, 226), fill=tuple(min(255, c + 30) for c in col) + (255,))
        for x0, x1 in ((40, 30), (180, 190), (80, 76), (140, 144)): d.line(S(x0, 222, x1, 372), fill=dk + (255,), width=9 * sc)
        return _done(im, w, h)
    return gcache(("chair", col), mk)


def lamp_el(on=1.0):
    def mk():
        w, h, sc = 300, 230, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(110, 120, 190, 200), fill=(255, 250, 210, 255))
        shape_grad(im, lambda m: m.pieslice(S(20, 20, 280, 260), 180, 360, fill=255), (255, 210, 40), (232, 120, 20))
        d.rectangle(S(20, 136, 280, 150), fill=(40, 34, 32, 255))
        d.rounded_rectangle(S(132, 4, 168, 30), 6 * sc, fill=(40, 34, 32, 255))
        d.pieslice(S(60, 50, 160, 150), 200, 260, fill=(255, 255, 255, 110))
        return _done(im, w, h)
    return gcache("lamp", mk)


def glow(f, x, y, r, col, amt):
    if amt <= 0.01: return
    g = np.exp(-((_xx[::8, ::8] - x) ** 2 + (_yy[::8, ::8] - y) ** 2) / (2 * r ** 2)).astype(np.float32)
    f += cv2.resize(g, (W, H))[..., None] * np.array(C(col), np.float32) * amt


def speaker_el():
    def mk():
        w, h, sc = 420, 620, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(20, 20, 400, 600), 150 * sc, fill=255), (255, 90, 170), (150, 30, 160))
        d.rounded_rectangle(S(20, 20, 400, 600), 150 * sc, outline=(255, 220, 120, 255), width=10 * sc)
        d.arc(S(60, 50, 360, 300), 180, 360, fill=(120, 240, 255, 255), width=12 * sc)
        for r, c in ((130, (40, 20, 60)), (110, (70, 40, 100)), (80, (30, 16, 44)), (40, (230, 220, 250)), (16, (40, 20, 60))):
            d.ellipse(S(210 - r, 380 - r, 210 + r, 380 + r), fill=c + (255,))
        d.rounded_rectangle(S(90, 540, 330, 572), 12 * sc, fill=(255, 220, 120, 255))
        return _done(im, w, h)
    return gcache("speaker", mk)


def note_el(col=(255, 230, 120), kind=0):
    def mk():
        w, h, sc = 110, 150, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        if kind == 0:
            d.ellipse(S(10, 100, 56, 136), fill=col + (255,)); d.rectangle(S(46, 14, 56, 118), fill=col + (255,))
            d.polygon(S(56, 14, 96, 44, 92, 62, 56, 38), fill=col + (255,))
        else:
            d.ellipse(S(4, 104, 44, 136), fill=col + (255,)); d.ellipse(S(60, 94, 100, 126), fill=col + (255,))
            d.rectangle(S(36, 24, 44, 120), fill=col + (255,)); d.rectangle(S(92, 14, 100, 110), fill=col + (255,))
            d.polygon(S(36, 24, 100, 14, 100, 32, 36, 42), fill=col + (255,))
        return _done(im, w, h)
    return gcache(("note", col, kind), mk)


def menu_el(items, title="MENU", dollar=True, hi=None, w=600, h=820):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 1, h - 1), 18 * sc, fill=255), (253, 249, 238), (238, 228, 206))
        d.rounded_rectangle(S(18, 18, w - 18, h - 18), 10 * sc, outline=GOLD + (255,), width=4 * sc)
        d.rounded_rectangle(S(30, 30, w - 30, h - 30), 8 * sc, outline=GOLD + (255,), width=2 * sc)
        d.text((w / 2 * sc, 112 * sc), title, font=font(F_PF9, 74 * sc), fill=(40, 30, 22, 255), anchor="mm")
        d.line(S(w / 2 - 120, 168, w / 2 - 20, 168), fill=GOLD + (255,), width=3 * sc); d.line(S(w / 2 + 20, 168, w / 2 + 120, 168), fill=GOLD + (255,), width=3 * sc)
        d.ellipse(S(w / 2 - 7, 161, w / 2 + 7, 175), fill=GOLD + (255,))
        y = 240; fi = font(F_PFI, 40 * sc); fp = font(F_PF, 44 * sc)
        for i, (name, price) in enumerate(items):
            if hi is not None and i == hi:
                d.rounded_rectangle(S(46, y - 36, w - 46, y + 36), 12 * sc, fill=(255, 214, 80, 200))
            d.text((64 * sc, y * sc), name, font=fi, fill=(48, 36, 26, 255), anchor="lm")
            ptxt = (f"${price}" if dollar else f"{price}")
            pw = fp.getlength(ptxt)
            d.text(((w - 64) * sc, y * sc), ptxt, font=fp, fill=(150, 30, 26, 255), anchor="rm")
            nx = 64 * sc + fi.getlength(name) + 14 * sc
            for x in range(int(nx), int((w - 64) * sc - pw - 14 * sc), 12 * sc): d.ellipse([x, y * sc + 8 * sc, x + 4 * sc, y * sc + 12 * sc], fill=(170, 150, 120, 255))
            y += 110
        return _done(im, w, h)
    return gcache(("menu", tuple(items), title, dollar, hi, w, h), mk)


def cup_el(xray=0):
    def mk():
        w, h, sc = 380, 640, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        body = S(40, 150, 340, 150, 300, 620, 80, 620)
        if not xray:
            shape_grad(im, lambda m: m.polygon(body, fill=255), (236, 34, 40), (190, 18, 28))
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(body, fill=255)
            st = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
            for i in range(-6, 10):
                x = i * 70; ds.polygon(S(x, 150, x + 34, 150, x + 34 + 120, 620, x + 120, 620), fill=(255, 255, 255, 235))
            im.paste(st, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(st.getchannel("A"))), "L"))
            d.polygon(S(40, 150, 90, 150, 110, 620, 80, 620), fill=(0, 0, 0, 40))
            d.polygon(S(270, 150, 340, 150, 300, 620, 262, 620), fill=(255, 255, 255, 50))
        else:
            d.polygon(body, fill=(200, 230, 255, 90), outline=(120, 170, 220, 255))
            d.line(body + body[:2], fill=(90, 150, 210, 255), width=5 * sc)
            d.polygon(S(76, 560, 304, 560, 300, 618, 80, 618), fill=(110, 50, 20, 235))
            d.polygon(S(52, 260, 328, 260, 304, 560, 76, 560), fill=(150, 210, 255, 150))
            rng = np.random.default_rng(3)
            for i in range(14):
                x = 80 + (i % 4) * 58 + rng.uniform(-8, 8); y = 190 + (i // 4) * 92 + rng.uniform(-10, 10)
                d.rounded_rectangle(S(x, y, x + 62, y + 62), 12 * sc, fill=(230, 248, 255, 230), outline=(140, 200, 240, 255), width=3 * sc)
        d.rounded_rectangle(S(26, 126, 354, 160), 14 * sc, fill=(250, 250, 250, 255))
        d.ellipse(S(70, 92, 310, 150), fill=(240, 240, 244, 255))
        d.polygon(S(200, 0, 228, 6, 214, 120, 190, 118), fill=(255, 255, 255, 255))
        for k_ in range(6): d.polygon(S(203 - k_ * 0.6, 14 + k_ * 20, 226 - k_ * 0.6, 20 + k_ * 20, 224 - k_ * 0.6, 30 + k_ * 20, 201 - k_ * 0.6, 24 + k_ * 20), fill=RED_ + (255,))
        return _done(im, w, h)
    return gcache(("cup", xray), mk)


def steak_el(big=True):
    def mk():
        w, h, sc = (720, 440, 2) if big else (420, 280, 2); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, h * 0.32, w - 10, h - 6), fill=(214, 216, 224, 255))
        shape_grad(im, lambda m: m.ellipse(S(18, h * 0.32 - 8, w - 18, h - 18), fill=255), (255, 255, 255), (228, 230, 238))
        d.ellipse(S(60, h * 0.32 + 14, w - 60, h - 40), outline=(210, 214, 226, 255), width=3 * sc)
        if big:
            d.rounded_rectangle(S(430, 150, 700, 196), 23 * sc, fill=(246, 236, 210, 255)); d.ellipse(S(670, 136, 716, 210), fill=(246, 236, 210, 255))
            pts = [(70, 220), (110, 120), (230, 80), (380, 96), (470, 150), (480, 260), (400, 340), (220, 352), (100, 320)]
        else:
            pts = [(50, 150), (90, 90), (200, 70), (330, 96), (370, 160), (320, 220), (190, 236), (80, 214)]
        shape_grad(im, lambda m: m.polygon([(x * sc, y * sc) for x, y in pts], fill=255), (150, 64, 40), (96, 34, 22))
        d.line([(x * sc, y * sc) for x, y in pts + pts[:1]], fill=(70, 26, 16, 255), width=10 * sc, joint="curve")
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for i in range(5):
            x0 = min(xs) + 60 + i * (max(xs) - min(xs) - 80) / 5
            d.line(S(x0, min(ys) + 30, x0 + 70, max(ys) - 40), fill=(52, 20, 12, 220), width=10 * sc)
        d.arc(S(min(xs) + 40, min(ys) + 30, max(xs) - 40, max(ys) - 20), 200, 300, fill=(250, 220, 200, 200), width=6 * sc)
        return _done(im, w, h)
    return gcache(("steak", big), mk)


def steam(f, x, y, t, s=1.0, op=0.6):
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1.0
        pts = [(x + (i - 1) * 60 * s + 18 * s * math.sin(ph * 8 + k * 0.7 + i), y - k * 26 * s - ph * 90 * s) for k in range(8)]
        ov = f.copy(); cv2.polylines(ov, [np.array(pts, np.int32)], False, (1, 1, 1), int(10 * s), cv2.LINE_AA)
        a = op * math.sin(math.pi * ph); f[:] = f * (1 - a) + ov * a


def anchor_el():
    def mk():
        w, h, sc = 420, 560, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        m = Image.new("L", im.size, 0); dm = ImageDraw.Draw(m)
        dm.ellipse(S(160, 10, 260, 110), outline=255, width=26 * sc)
        dm.rounded_rectangle(S(190, 90, 230, 500), 18 * sc, fill=255)
        dm.rounded_rectangle(S(90, 140, 330, 180), 18 * sc, fill=255)
        dm.arc(S(30, 250, 390, 530), 20, 160, fill=255, width=36 * sc)
        dm.polygon(S(10, 360, 90, 330, 80, 420), fill=255); dm.polygon(S(410, 360, 330, 330, 340, 420), fill=255)
        g = grad_img(im.size[0], im.size[1], (150, 164, 190), (46, 54, 76)); im.paste(g, (0, 0), m)
        hl = Image.new("L", im.size, 0); ImageDraw.Draw(hl).rectangle(S(196, 100, 206, 480), fill=110)
        im.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), Image.fromarray(np.minimum(np.asarray(hl), np.asarray(m)), "L"))
        return _done(im, w, h)
    return gcache("anchor", mk)


def glass_el(kind=0):
    def mk():
        w, h, sc = 160, 260, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        if kind == 0:
            d.polygon(S(10, 20, 150, 20, 80, 120), fill=(220, 240, 255, 140)); d.polygon(S(26, 32, 134, 32, 80, 108), fill=(255, 80, 150, 255))
            d.rectangle(S(76, 116, 84, 220), fill=(220, 240, 255, 220)); d.ellipse(S(36, 214, 124, 236), fill=(220, 240, 255, 230))
            d.ellipse(S(108, 10, 136, 38), fill=(120, 220, 80, 255))
        elif kind == 1:
            d.ellipse(S(20, 10, 140, 150), fill=(220, 240, 255, 140)); d.chord(S(28, 18, 132, 142), 10, 170, fill=(150, 20, 40, 255))
            d.rectangle(S(76, 146, 84, 226), fill=(220, 240, 255, 220)); d.ellipse(S(36, 220, 124, 242), fill=(220, 240, 255, 230))
        else:
            d.rounded_rectangle(S(20, 40, 120, 240), 14 * sc, fill=(255, 196, 40, 255)); d.rounded_rectangle(S(14, 20, 126, 64), 20 * sc, fill=(255, 255, 255, 255))
            d.arc(S(100, 90, 156, 190), 270, 90, fill=(220, 240, 255, 255), width=12 * sc)
            d.rounded_rectangle(S(20, 40, 120, 240), 14 * sc, outline=(255, 255, 255, 120), width=4 * sc)
        d.line(S(30, 30, 30, 90) if kind != 2 else S(34, 70, 34, 220), fill=(255, 255, 255, 160), width=5 * sc)
        return _done(im, w, h)
    return gcache(("glass", kind), mk)


def burger_el():
    def mk():
        w, h, sc = 420, 340, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(40, 250, 380, 320), 30 * sc, fill=255), (232, 160, 70), (196, 120, 46))
        shape_grad(im, lambda m: m.rounded_rectangle(S(30, 196, 390, 262), 30 * sc, fill=255), (110, 52, 28), (70, 30, 16))
        d.polygon(S(30, 196, 390, 196, 330, 236, 270, 204, 210, 240, 150, 204, 90, 236), fill=(255, 196, 30, 255))
        for i in range(9): d.ellipse(S(24 + i * 42, 168, 72 + i * 42, 206), fill=(90, 190, 60, 255))
        d.rectangle(S(60, 150, 360, 176), fill=(236, 60, 40, 255))
        shape_grad(im, lambda m: m.chord(S(30, 10, 390, 270), 180, 360, fill=255), (250, 180, 80), (214, 130, 50))
        rng = np.random.default_rng(2)
        for i in range(16):
            x = rng.uniform(80, 340); y = rng.uniform(40, 120); d.ellipse(S(x, y, x + 12, y + 7), fill=(255, 244, 210, 255))
        d.pieslice(S(80, 30, 220, 140), 200, 250, fill=(255, 255, 255, 80))
        return _done(im, w, h)
    return gcache("burger", mk)


def fries_el():
    def mk():
        w, h, sc = 240, 320, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        for i in range(9):
            x = 36 + i * 20; d.rounded_rectangle(S(x, 20 + (i % 3) * 18, x + 18, 200), 5 * sc, fill=(255, 210, 70, 255), outline=(230, 170, 30, 255), width=2 * sc)
        shape_grad(im, lambda m: m.polygon(S(20, 120, 220, 120, 196, 312, 44, 312), fill=255), (236, 34, 40), (190, 18, 28))
        d.arc(S(20, 70, 220, 170), 0, 180, fill=(190, 18, 28, 255), width=4 * sc)
        return _done(im, w, h)
    return gcache("fries", mk)


def magnifier_el():
    def mk():
        w, h, sc = 380, 520, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(168, 300, 212, 510), 20 * sc, fill=(70, 40, 24, 255))
        d.ellipse(S(30, 20, 350, 340), fill=(30, 30, 36, 255)); d.ellipse(S(52, 42, 328, 318), fill=(200, 235, 255, 70))
        d.pieslice(S(70, 60, 250, 240), 200, 250, fill=(255, 255, 255, 120))
        return _done(im, w, h)
    return gcache("magnifier", mk)


def wallet_el(mood="ouch"):
    def mk():
        w, h, sc = 460, 340, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(20, 40, 440, 320), 40 * sc, fill=255), (170, 100, 56), (120, 66, 34))
        d.rounded_rectangle(S(36, 56, 424, 304), 30 * sc, outline=(240, 200, 150, 200), width=3 * sc)
        d.rounded_rectangle(S(300, 120, 460, 230), 30 * sc, fill=(140, 80, 44, 255)); d.ellipse(S(400, 160, 428, 188), fill=GOLD + (255,))
        d.rectangle(S(80, 10, 260, 60), fill=(60, 170, 90, 255)); d.rectangle(S(96, 0, 276, 50), fill=(90, 200, 110, 255))
        ex = (130, 210); ey = 160
        if mood == "ouch":
            for x in ex: d.line(S(x - 16, ey - 12, x + 16, ey + 4), fill=INK + (255,), width=7 * sc); d.line(S(x - 16, ey + 4, x + 16, ey - 12), fill=INK + (255,), width=7 * sc)
            d.ellipse(S(146, 212, 194, 260), fill=(60, 16, 20, 255)); d.ellipse(S(96, 176, 116, 206), fill=(120, 200, 255, 230))
        else:
            for x in ex: d.arc(S(x - 18, ey - 14, x + 18, ey + 14), 200, 340, fill=INK + (255,), width=7 * sc)
            d.arc(S(130, 196, 210, 250), 20, 160, fill=INK + (255,), width=7 * sc)
        return _done(im, w, h)
    return gcache(("wallet", mood), mk)


def tag_el(text, col=RED_, fg=WHITE, size=84):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 150), int(size * 1.7); sc = 2
        im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(0, h / 2, 46, 0, w, 0, w, h, 46, h), fill=tuple(col) + (255,))
        d.ellipse(S(30, h / 2 - 11, 52, h / 2 + 11), fill=(255, 255, 255, 255))
        d.text(((w + 46) / 2 * sc, h / 2 * sc), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("tag", text, col, fg, size), mk)


def card_num_el(num, kind):
    def mk():
        w, h, sc = 230, 320, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, h - 1), 26 * sc, fill=(255, 255, 255, 255))
        col = [ORANGE, (120, 60, 220), RED_, (14, 120, 86)][num - 1]
        d.rounded_rectangle(S(12, 12, w - 12, h - 12), 20 * sc, outline=col + (255,), width=6 * sc)
        d.text((w / 2 * sc, 92 * sc), str(num), font=font(F_BLACK, 120 * sc), fill=col + (255,), anchor="mm")
        if kind == "?": d.text((w / 2 * sc, 236 * sc), "?", font=font(F_BLACK, 110 * sc), fill=INK + (255,), anchor="mm")
        else:
            src = {"steak": steak_el(False), "note": note_el(col, 1), "cup": cup_el()}[kind]
            pm, a = src; hh = 120 if kind != "steak" else 90; s = hh / a.shape[0]
            sm = Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA")
            sm = sm.resize((int(a.shape[1] * s * sc), int(a.shape[0] * s * sc)), Image.LANCZOS)
            im.alpha_composite(sm, (int((w * sc - sm.width) / 2), int(236 * sc - sm.height / 2)))
        return _done(im, w, h)
    return gcache(("cardn", num, kind), mk)


def phone_el(pressed=False):
    def mk():
        w, h, sc = 420, 760, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, h - 1), 60 * sc, fill=(24, 24, 30, 255))
        shape_grad(im, lambda m: m.rounded_rectangle(S(18, 18, w - 18, h - 18), 46 * sc, fill=255), (250, 246, 236), (236, 230, 216))
        d.rounded_rectangle(S(150, 30, 270, 54), 12 * sc, fill=(24, 24, 30, 255))
        d.rounded_rectangle(S(40, 110, 300, 190), 26 * sc, fill=(226, 226, 232, 255))
        d.text((60 * sc, 150 * sc), "who orders the steak?", font=font(F_SEMI, 22 * sc), fill=INK + (255,), anchor="lm")
        d.rounded_rectangle(S(130, 220, 380, 300), 26 * sc, fill=(60, 140, 255, 255))
        d.text((150 * sc, 260 * sc), "always me lol", font=font(F_SEMI, 22 * sc), fill=(255, 255, 255, 255), anchor="lm")
        col = (34, 190, 94) if pressed else YEL_
        d.rounded_rectangle(S(60, 600, 360, 690), 45 * sc, fill=col + (255,))
        d.text((210 * sc, 645 * sc), "SEND THIS", font=font(F_BLACK, 40 * sc), fill=(INK if not pressed else (255, 255, 255)) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("phone", pressed), mk)


def bubble_el(text, size=46):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 90), int(size * 2.4); sc = 2
        im, d = _canvas(w + 60, h + 70); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(0, 0, w, h), fill=(255, 255, 255, 255))
        d.ellipse(S(w * 0.18, h - 6, w * 0.18 + 34, h + 28), fill=(255, 255, 255, 255)); d.ellipse(S(w * 0.1, h + 34, w * 0.1 + 20, h + 54), fill=(255, 255, 255, 255))
        d.text((w / 2 * sc, h / 2 * sc), text, font=fn, fill=INK + (255,), anchor="mm")
        return _done(im, w + 60, h + 70)
    return gcache(("bubble", text, size), mk)


def coin_el(r=50, sx=1.0):
    sx = round(max(0.08, abs(sx)), 2)
    def mk():
        sc = 2; R = r * sc; w = int(2 * R * sx) + 6 * sc; h = 2 * R + 6 * sc
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cx, cy = w / 2, h / 2
        d.ellipse([cx - R * sx, cy - R, cx + R * sx, cy + R], fill=(196, 132, 10, 255))
        d.ellipse([cx - R * sx * 0.9, cy - R * 0.9, cx + R * sx * 0.9, cy + R * 0.9], fill=(255, 200, 40, 255))
        if sx > 0.45: d.text((cx, cy + R * 0.04), "¢", font=font(F_BLACK, int(R * 0.95 * sx)), fill=(214, 150, 20, 255), anchor="mm")
        return el_from(im.resize((w // sc, h // sc), Image.LANCZOS))
    return gcache(("coin", r, sx), mk)


def logo_el():
    def mk():
        w, h, sc = 900, 360, 2; im, d = _canvas(w, h)
        fo = font(F_BLACK, 190 * sc); x = 70 * sc
        hel = head_el(2, False, "up", 0, 0, "n"); pm, a = hel
        hp = Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA").resize((168 * sc, 160 * sc), Image.LANCZOS)
        im.alpha_composite(hp, (x, int(36 * sc)))
        x += 172 * sc
        for ch in "OPS": d.text((x, 116 * sc), ch, font=fo, fill=ORANGE + (255,), anchor="lm"); x += fo.getlength(ch) - 6 * sc
        d.text((w / 2 * sc + 30 * sc, 282 * sc), "MY BUSINESS", font=font(F_BLACK, 86 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache("logo", mk)
