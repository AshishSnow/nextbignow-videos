# ================= props for the $1.50 hot dog video =================
def _ov(im, fn):
    """draw translucent shapes on their own layer, then composite (PIL draw replaces alpha otherwise)."""
    L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L_)); im.alpha_composite(L_)

def hotdog_el():
    def mk():
        w, h, sc = 620, 300, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        # back half of the bun
        shape_grad(im, lambda m: m.rounded_rectangle(S(30, 70, 590, 210), 70 * sc, fill=255), (246, 186, 96), (214, 140, 60))
        # sausage
        shape_grad(im, lambda m: m.rounded_rectangle(S(6, 92, 614, 178), 43 * sc, fill=255), (214, 84, 52), (150, 46, 30))
        _ov(im, lambda q: q.rounded_rectangle(S(40, 104, 580, 120), 8 * sc, fill=(255, 170, 140, 150)))
        # mustard zig-zag
        pts = [(60 + i * 40, 112 if i % 2 else 142) for i in range(13)]
        d.line([(x * sc, y * sc) for x, y in pts], fill=(255, 214, 20, 255), width=14 * sc, joint="curve")
        # front half of the bun
        shape_grad(im, lambda m: m.rounded_rectangle(S(24, 150, 596, 292), 70 * sc, fill=255), (252, 196, 104), (206, 128, 50))
        _ov(im, lambda q: q.arc(S(60, 160, 560, 300), 200, 340, fill=(255, 236, 190, 170), width=6 * sc))
        return _done(im, w, h)
    return gcache("hotdog", mk)


def chicken_el(dome=True):
    def mk():
        w, h, sc = 560, 440, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(20, 330, 540, 420), 30 * sc, fill=(26, 26, 32, 255))
        d.rounded_rectangle(S(36, 330, 524, 352), 10 * sc, fill=(60, 60, 70, 255))
        # drumsticks
        for x0, flip in ((120, -1), (440, 1)):
            shape_grad(im, lambda m, x0=x0: m.ellipse(S(x0 - 70, 220, x0 + 70, 330), fill=255), (232, 150, 56), (170, 88, 26))
            d.ellipse(S(x0 + flip * 70 - 26, 238, x0 + flip * 70 + 26, 270), fill=(250, 236, 210, 255))
        # body
        shape_grad(im, lambda m: m.ellipse(S(110, 120, 450, 340), fill=255), (240, 168, 66), (178, 92, 26))
        _ov(im, lambda q: q.arc(S(150, 140, 410, 300), 200, 320, fill=(255, 220, 150, 200), width=10 * sc))
        rng = np.random.default_rng(7)
        for i in range(26):
            x = rng.uniform(150, 410); y = rng.uniform(160, 310); d.ellipse(S(x, y, x + 7, y + 5), fill=(120, 60, 20, 200))
        if dome:
            _ov(im, lambda q: q.chord(S(20, 30, 540, 520), 180, 360, fill=(220, 240, 255, 55), outline=(255, 255, 255, 210), width=4 * sc))
            _ov(im, lambda q: q.arc(S(70, 70, 330, 330), 200, 250, fill=(255, 255, 255, 200), width=12 * sc))
        return _done(im, w, h)
    return gcache(("chicken", dome), mk)


def member_card_el():
    def mk():
        w, h, sc = 620, 390, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(6, 10, w - 2, h - 2), 34 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 10, h - 12), 34 * sc, fill=255), (255, 214, 92), (214, 150, 30))
        _ov(im, lambda q: q.polygon(S(0, 230, w - 10, 120, w - 10, 190, 0, 300), fill=(255, 255, 255, 60)))
        d.rounded_rectangle(S(30, 30, 250, 90), 14 * sc, fill=INK + (255,))
        d.text((140 * sc, 60 * sc), "MEMBER", font=font(F_BLACK, 38 * sc), fill=(255, 214, 92, 255), anchor="mm")
        d.rounded_rectangle(S(440, 40, 560, 110), 12 * sc, fill=(200, 160, 60, 255), outline=(150, 110, 30, 255), width=3 * sc)
        for i in range(3): d.line(S(440, 58 + i * 18, 560, 58 + i * 18), fill=(150, 110, 30, 255), width=2 * sc)
        hel = head_el(2, False, "up", 0, 0, "n"); pm, a = hel
        hp = Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA").resize((150 * sc, 143 * sc), Image.LANCZOS)
        d.rounded_rectangle(S(30, 140, 200, 320), 16 * sc, fill=(255, 255, 255, 255)); im.alpha_composite(hp, (int(38 * sc), int(160 * sc)))
        for i, ln in enumerate((300, 220, 260)): _ov(im, lambda q, i=i, ln=ln: q.rounded_rectangle(S(230, 160 + i * 44, 230 + ln, 184 + i * 44), 10 * sc, fill=(120, 80, 10, 150)))
        x = 230
        rng = np.random.default_rng(11)
        while x < 560:
            bw = int(rng.integers(3, 9)); d.rectangle(S(x, 300, x + bw, 350), fill=INK + (255,)); x += bw + int(rng.integers(3, 8))
        return _done(im, w, h)
    return gcache("mcard", mk)


def folder_el(num, gold=False, label="TOP SECRET"):
    def mk():
        w, h, sc = 300, 250, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        top, bot = ((255, 222, 110), (220, 160, 40)) if gold else ((236, 196, 130), (204, 158, 92))
        d.rounded_rectangle(S(10, 0, 130, 50), 14 * sc, fill=tuple(int(c * 0.9) for c in bot) + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 26, w - 1, h - 1), 22 * sc, fill=255), top, bot)
        d.text((w / 2 * sc, 130 * sc), str(num), font=font(F_BLACK, 120 * sc), fill=(INK if not gold else (120, 70, 0)) + (255,), anchor="mm")
        stamp = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(stamp)
        ds.rounded_rectangle(S(40, 186, 260, 230), 8 * sc, outline=RED_ + (230,), width=5 * sc)
        ds.text((150 * sc, 208 * sc), label, font=font(F_BLACK, 28 * sc), fill=RED_ + (230,), anchor="mm")
        im.alpha_composite(stamp.rotate(6, center=(150 * sc, 208 * sc), resample=Image.BICUBIC))
        return _done(im, w, h)
    return gcache(("folder", num, gold, label), mk)


def shelf_el(seed=0, w=520, h=640):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed)
        cols = [(232, 60, 50), (40, 130, 230), (250, 190, 30), (40, 180, 110), (240, 120, 40), (150, 80, 220), (250, 250, 250)]
        lv = 4; lh = (h - 40) / lv
        for i in range(lv):
            yb = 20 + (i + 1) * lh
            x = 24
            while x < w - 60:
                bw = rng.uniform(50, 110); bh = rng.uniform(lh * 0.45, lh * 0.82); c = cols[int(rng.integers(len(cols)))]
                if x + bw > w - 24: break
                shape_grad(im, lambda m, x=x, bw=bw, bh=bh, yb=yb: m.rectangle(S(x, yb - bh, x + bw - 4, yb - 6), fill=255), tuple(min(255, v + 25) for v in c), tuple(int(v * 0.75) for v in c))
                _ov(im, lambda q, x=x, bw=bw, bh=bh, yb=yb: q.rectangle(S(x + 8, yb - bh * 0.6, x + bw - 12, yb - bh * 0.6 + 10), fill=(255, 255, 255, 150)))
                x += bw + rng.uniform(2, 8)
            d.rectangle(S(0, yb - 8, w, yb + 6), fill=(255, 128, 20, 255))
        d.rectangle(S(0, 0, 16, h), fill=(40, 90, 200, 255)); d.rectangle(S(w - 16, 0, w, h), fill=(40, 90, 200, 255))
        return _done(im, w, h)
    return gcache(("shelf", seed, w, h), mk)


def cash_el(n=1):
    def mk():
        w, h, sc = 360, 200, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        for k_ in range(4):
            y = 120 - k_ * 22
            shape_grad(im, lambda m, y=y: m.rounded_rectangle(S(10, y, 350, y + 76), 10 * sc, fill=255), (120, 210, 120), (60, 150, 70))
            d.rounded_rectangle(S(22, y + 10, 338, y + 66), 8 * sc, outline=(30, 110, 50, 255), width=3 * sc)
            d.ellipse(S(150, y + 14, 210, y + 62), outline=(30, 110, 50, 255), width=3 * sc)
            d.text((180 * sc, (y + 38) * sc), "$", font=font(F_BLACK, 40 * sc), fill=(30, 110, 50, 255), anchor="mm")
        d.rectangle(S(160, 50, 200, 200), fill=(255, 255, 255, 230))
        return _done(im, w, h)
    return gcache(("cash", n), mk)


def bottlecap_el(text="MAX"):
    def mk():
        w, h, sc = 420, 260, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        pts = []
        for i in range(37):
            x = 20 + i * 10; pts.append((x, 200 if i % 2 else 214))
        shape_grad(im, lambda m: m.polygon(S(20, 60, 400, 60) + [v * sc for p in pts[::-1] for v in p], fill=255), (240, 50, 50), (170, 16, 24))
        shape_grad(im, lambda m: m.ellipse(S(16, 20, 404, 110), fill=255), (255, 90, 80), (210, 30, 34))
        _ov(im, lambda q: q.ellipse(S(60, 34, 360, 96), outline=(255, 200, 190, 160), width=4 * sc))
        d.text((210 * sc, 148 * sc), text, font=font(F_BLACK, 70 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("cap", text), mk)


def calendar_el(top="YEAR", big="1985"):
    def mk():
        w, h, sc = 420, 460, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 30, 410, 450), 30 * sc, fill=(0, 0, 0, 60)))
        d.rounded_rectangle(S(0, 20, 400, 440), 30 * sc, fill=(255, 255, 255, 255))
        d.rounded_rectangle(S(0, 20, 400, 140), 30 * sc, fill=RED_ + (255,)); d.rectangle(S(0, 100, 400, 140), fill=RED_ + (255,))
        for x in (100, 300): d.rounded_rectangle(S(x - 12, 0, x + 12, 56), 10 * sc, fill=(60, 60, 70, 255))
        d.text((200 * sc, 88 * sc), top, font=font(F_BLACK, 52 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text((200 * sc, 292 * sc), big, font=font(F_BLACK, 150 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("cal", top, big), mk)


def sign_el(text, bg=YEL_, fg=INK, size=90, pole=True):
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w = int(tw + 70); hh = int(size * 1.5); h = hh + (170 if pole else 0); sc = 2
        im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        if pole: d.rectangle(S(w / 2 - 9, hh - 10, w / 2 + 9, h), fill=(120, 80, 40, 255))
        d.rounded_rectangle(S(0, 0, w - 1, hh), 16 * sc, fill=tuple(bg) + (255,), outline=INK + (255,), width=6 * sc)
        d.text((w / 2 * sc, hh / 2 * sc + 4 * sc), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("sign", text, bg, fg, size, pole), mk)


def phone2_el(msg1, msg2, pressed=False):
    def mk():
        w, h, sc = 420, 760, 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w - 1, h - 1), 60 * sc, fill=(24, 24, 30, 255))
        shape_grad(im, lambda m: m.rounded_rectangle(S(18, 18, w - 18, h - 18), 46 * sc, fill=255), (250, 246, 236), (236, 230, 216))
        d.rounded_rectangle(S(150, 30, 270, 54), 12 * sc, fill=(24, 24, 30, 255))
        f1 = font(F_SEMI, 24 * sc)
        d.rounded_rectangle(S(40, 110, 60 + f1.getlength(msg1) / sc + 30, 190), 26 * sc, fill=(226, 226, 232, 255))
        d.text((62 * sc, 150 * sc), msg1, font=f1, fill=INK + (255,), anchor="lm")
        x0 = 380 - f1.getlength(msg2) / sc - 50
        d.rounded_rectangle(S(x0, 220, 380, 300), 26 * sc, fill=(60, 140, 255, 255))
        d.text(((x0 + 24) * sc, 260 * sc), msg2, font=f1, fill=(255, 255, 255, 255), anchor="lm")
        col = (34, 190, 94) if pressed else YEL_
        d.rounded_rectangle(S(60, 600, 360, 690), 45 * sc, fill=col + (255,))
        d.text((210 * sc, 645 * sc), "SEND THIS", font=font(F_BLACK, 40 * sc), fill=(INK if not pressed else (255, 255, 255)) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("phone2", msg1, msg2, pressed), mk)


def check_el(r=40, ok=True):
    def mk():
        sc = 2; s = 2 * r + 8; im, d = _canvas(s, s); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(4, 4, s - 4, s - 4), fill=((34, 190, 94) if ok else RED_) + (255,))
        if ok: d.line(S(s * 0.28, s * 0.52, s * 0.44, s * 0.68, s * 0.74, s * 0.34), fill=(255, 255, 255, 255), width=int(r * 0.28) * sc, joint="curve")
        else:
            d.line(S(s * 0.32, s * 0.32, s * 0.68, s * 0.68), fill=(255, 255, 255, 255), width=int(r * 0.26) * sc)
            d.line(S(s * 0.68, s * 0.32, s * 0.32, s * 0.68), fill=(255, 255, 255, 255), width=int(r * 0.26) * sc)
        return _done(im, s, s)
    return gcache(("check", r, ok), mk)


def mini_head(r=60, lit=True):
    def mk():
        hel = head_el(2 if lit else 0, False, "up" if lit else "n", 0, 0, "n" if lit else "sad")
        return scale_el(hel, r / 100.0)
    return gcache(("mhead", r, lit), mk)
