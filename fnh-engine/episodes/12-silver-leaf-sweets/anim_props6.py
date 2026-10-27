# ================= ep 12 props (silver leaf on sweets): kaju katli + barfi with crinkly silver leaf, plate, diya lamp,
# silver leaf sheet, silver lump, wooden hammer (pivot at the grip for arc swings), beating packet (sheets + silver),
# metal detector, kitchen scale with readout, paper sheet, element tiles (Ag / Al / Pb / Ni), animal-gut layers,
# rule document with a generic seal, food-colour bottle, simple cow icon =================
SCHEMES["festive"] = ((120, 20, 70), (226, 70, 120), (110, 16, 60), (0.55, 0.1, 0.3))
SCHEMES["saffron"] = ((236, 120, 10), (255, 176, 40), (226, 108, 8), (0.8, 0.45, 0.05))
SCHEMES["steel"] = ((60, 70, 92), (150, 162, 186), (70, 80, 104), (0.3, 0.33, 0.42))
SILV = (226, 230, 238); SILV_D = (140, 148, 166); KAJU = (246, 222, 170); KAJU_D = (214, 170, 104)
ALU = (176, 184, 196); ALU_D = (110, 118, 132); GOLDY = (255, 214, 90)


def _silver_tex(im, mask, seed=3, sc=2, dull=False):
    """crinkly metal-leaf texture inside a mask: gradient + wrinkle lines + glints."""
    w_, h_ = im.size
    top, bot = ((205, 210, 220), (150, 158, 172)) if dull else ((250, 252, 255), (176, 184, 200))
    g = grad_img(w_, h_, top, bot); im.paste(g, (0, 0), mask)
    rng = np.random.default_rng(seed)
    def wr(q):
        for i in range(int(w_ * h_ / (9000 * sc * sc)) + 8):
            x0, y0 = rng.uniform(0, w_), rng.uniform(0, h_); L = rng.uniform(20, 70) * sc; a = rng.uniform(0, math.pi)
            pts = [(x0 + L * k / 3 * math.cos(a) + rng.uniform(-6, 6) * sc, y0 + L * k / 3 * math.sin(a) + rng.uniform(-6, 6) * sc) for k in range(4)]
            q.line(pts, fill=(120, 128, 146, 120) if not dull else (110, 116, 128, 120), width=2 * sc)
            q.line([(p[0] + 2 * sc, p[1] + 2 * sc) for p in pts], fill=(255, 255, 255, 150 if not dull else 60), width=2 * sc)
    _masked(im, mask, wr)
    if not dull:
        def gl(q):
            for i in range(4):
                x0, y0 = rng.uniform(0.15, 0.85) * w_, rng.uniform(0.15, 0.6) * h_
                q.ellipse((x0 - 9 * sc, y0 - 9 * sc, x0 + 9 * sc, y0 + 9 * sc), fill=(255, 255, 255, 200))
        _masked(im, mask, gl)


# ---------------- kaju katli (diamond) with silver top ----------------
def kaju_el(silver=True, face=False, mood="n", bite=False, fake=False):
    def mk():
        w, h, sc = 360, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        side = lambda m: m.polygon(S(20, 120, 180, 30, 340, 120, 340, 150, 180, 240, 20, 150), fill=255)
        _outline(im, side, 11)
        shape_grad(im, side, KAJU, KAJU_D)
        top = lambda m: m.polygon(S(20, 120, 180, 30, 340, 120, 180, 210), fill=255)
        tm = Image.new("L", im.size, 0); top(ImageDraw.Draw(tm))
        if silver: _silver_tex(im, tm, 5 if not fake else 9, sc, dull=fake)
        else: shape_grad(im, top, (255, 238, 196), KAJU)
        d.polygon(S(20, 120, 180, 30, 340, 120, 180, 210), outline=INK + (255,), width=4 * sc)
        if bite:
            for bx, by, r in ((300, 110, 34), (330, 140, 30)):
                d.ellipse(S(bx - r, by - r, bx + r, by + r), fill=(0, 0, 0, 0))
        if face:
            _eyes(d, S, sc, [(146, 118), (214, 118)], 15, (0, 0), sly=(mood == "sly"), happy=(mood == "happy"))
            if mood == "sad": d.arc(S(160, 146, 200, 172), 200, 340, fill=INK + (255,), width=5 * sc)
            else: d.arc(S(158, 132, 202, 166), 20, 160, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("kaju", silver, face, mood, bite, fake), mk)


def barfi_el(col=(255, 170, 200), silver=True):
    def mk():
        w, h, sc = 260, 220, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: m.rounded_rectangle(S(20, 60, 240, 200), 16 * sc, fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, col, tuple(int(c * 0.8) for c in col))
        top = lambda m: m.polygon(S(20, 76, 60, 30, 240, 30, 240, 76, 200, 116, 20, 116), fill=255)
        tm = Image.new("L", im.size, 0); ImageDraw.Draw(tm).rounded_rectangle(S(26, 56, 234, 110), 14 * sc, fill=255)
        if silver: _silver_tex(im, tm, 11, sc)
        d.rounded_rectangle(S(26, 56, 234, 110), 14 * sc, outline=INK + (255,), width=4 * sc)
        for k in range(3): d.ellipse(S(60 + 60 * k, 150, 74 + 60 * k, 162), fill=(255, 255, 255, 120))
        return _done(im, w, h)
    return gcache(("barfi", col, silver), mk)


def plate_el(w_=560):
    def mk():
        w, h, sc = w_, int(w_ * 0.36), 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(6, 6, w - 6, h - 6), fill=INK + (255,))
        shape_grad(im, lambda m: m.ellipse(S(14, 12, w - 14, h - 14), fill=255), (255, 255, 255), (200, 206, 220))
        _ov(im, lambda q: q.ellipse(S(60, 30, w - 60, h - 40), fill=(225, 230, 240, 200)))
        _ov(im, lambda q: q.arc(S(30, 20, w - 30, h - 20), 190, 260, fill=(255, 255, 255, 220), width=6 * sc))
        return _done(im, w, h)
    return gcache(("plate", w_), mk)


def plate_of_sweets(f, x, y, s, t, hi=None, fake_i=None):
    comp(f, scale_el(plate_el(), s), x, y + 40 * s)
    pos = ((-150, -10, 0), (0, -30, 1), (150, -10, 2), (-75, 30, 3), (75, 30, 4))
    for i, (dx, dy, k) in enumerate(pos):
        el = kaju_el(True, fake=(i == fake_i)) if k % 2 == 0 else barfi_el(((255, 170, 200), (150, 220, 130))[k % 3 == 1])
        sc_ = 0.55 * s * (1.15 if i == hi else 1.0)
        comp(f, scale_el(el, sc_), x + dx * s, y + (dy - (12 if i == hi else 0) + 3 * math.sin(t * 3 + i)) * s)


# ---------------- diya (clay oil lamp) + flickering flame ----------------
def diya_el():
    def mk():
        w, h, sc = 220, 120, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: (m.chord(S(10, -40, 210, 110), 0, 180, fill=255), m.polygon(S(170, 40, 214, 22, 200, 56), fill=255))
        _outline(im, body, 11)
        shape_grad(im, body, (236, 120, 60), (170, 64, 30))
        for k in range(5): d.ellipse(S(40 + 30 * k, 70, 52 + 30 * k, 82), fill=(255, 210, 80, 255))
        d.line(S(20, 42, 200, 42), fill=(120, 40, 20, 255), width=5 * sc)
        return _done(im, w, h)
    return gcache("diya", mk)


def diya(f, x, y, s, t, seed=0):
    comp(f, scale_el(diya_el(), s), x, y)
    fx, fy = x + 88 * s, y - 34 * s; fl = 1 + 0.12 * math.sin(t * 17 + seed) + 0.06 * math.sin(t * 29 + seed * 2)
    glow(f, fx, fy - 20 * s, 90 * s, (255, 190, 80), 0.55)
    for r, col in ((1.0, (255, 150, 30)), (0.62, (255, 230, 120)), (0.3, (255, 255, 230))):
        P = np.array([[fx - 16 * s * r, fy], [fx, fy - 62 * s * r * fl], [fx + 16 * s * r, fy], [fx, fy + 12 * s * r]], np.int32)
        cv2.fillPoly(f, [P], C(col), cv2.LINE_AA)


# ---------------- silver leaf sheet / silver lump ----------------
def leaf_el(w_=420, h_=420, seed=2, fake=False, label=None):
    def mk():
        w, h, sc = w_ + 30, h_ + 30, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed)
        P = []
        for i in range(24):
            k = i / 24; side = int(k * 4); u = k * 4 - side
            x, y = [(15 + u * w_, 15), (15 + w_, 15 + u * h_), (15 + w_ - u * w_, 15 + h_), (15, 15 + h_ - u * h_)][side]
            P.append(((x + rng.uniform(-7, 7)) * sc, (y + rng.uniform(-7, 7)) * sc))
        m_ = Image.new("L", im.size, 0); ImageDraw.Draw(m_).polygon(P, fill=255)
        _silver_tex(im, m_, seed, sc, dull=fake)
        d.polygon(P, outline=(90, 96, 110, 255), width=3 * sc)
        if label: d.text((w / 2 * sc, h / 2 * sc), label, font=font(F_BLACK, 90 * sc), fill=(80, 86, 100, 230), anchor="mm")
        return _done(im, w, h)
    return gcache(("leaf", w_, h_, seed, fake, label), mk)


def lump_el():
    def mk():
        w, h, sc = 240, 170, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: m.polygon(S(20, 120, 50, 40, 120, 18, 200, 46, 224, 118, 160, 156, 70, 154), fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, (250, 252, 255), SILV_D)
        _ov(im, lambda q: q.polygon(S(60, 50, 120, 30, 150, 50, 90, 80), fill=(255, 255, 255, 190)))
        _ov(im, lambda q: q.line(S(70, 130, 180, 120), fill=(110, 118, 136, 160), width=6 * sc))
        return _done(im, w, h)
    return gcache("lump", mk)


# ---------------- wooden hammer: element centre = the grip (rotate with rot_comp to swing on an arc) ----------------
def hammer_el():
    def mk():
        w, h, sc = 560, 240, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        # grip at the canvas centre (280, 120); handle goes right to the head at x 420-520
        hd = lambda m: m.rounded_rectangle(S(250, 108, 450, 132), 10 * sc, fill=255)
        _outline(im, hd, 9); shape_grad(im, hd, (214, 160, 100), (150, 96, 50))
        head = lambda m: m.rounded_rectangle(S(430, 40, 540, 200), 18 * sc, fill=255)
        _outline(im, head, 11); shape_grad(im, head, (190, 120, 60), (120, 70, 30))
        for k in range(3): d.line(S(446, 70 + 40 * k, 524, 66 + 40 * k), fill=(110, 64, 28, 255), width=3 * sc)
        _ov(im, lambda q: q.rounded_rectangle(S(442, 52, 470, 186), 8 * sc, fill=(255, 255, 255, 60)))
        return _done(im, w, h)
    return gcache("hammer", mk)


def hammer_swing(t, t0, period=0.5, up=-70, down=8):
    """angle for a hammer beating on an arc: anticipation lift (up) then a fast strike (down); returns (ang, hit_now)."""
    if t < t0: return up * 0.4, False
    ph = ((t - t0) % period) / period
    if ph < 0.65: return down + (up - down) * eio(ph / 0.65), False          # slow lift (anticipation)
    k = (ph - 0.65) / 0.35; return up + (down - up) * (k * k), k > 0.85       # fast fall (accelerating)


# ---------------- beating packet: stack of sheets with silver squares between (side view, opens by k) ----------------
def packet(f, x, y, s, k_open=0.0, n=6, t=0.0, gut=False, squash=0.0):
    w_ = 380 * s; th = 16 * s * (1 - 0.35 * squash)
    for i in range(n):
        yy = y - i * (th * 2 + 10 * s * k_open)
        col = ((240, 120, 140) if gut else (120, 90, 60)); col2 = ((200, 100, 110) if gut else (80, 56, 34))
        if gut:
            P = [(x - w_ / 2 + j * w_ / 12, yy + 4 * s * math.sin(j * 1.3 + i)) for j in range(13)]
            cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), int(th + 8 * s), cv2.LINE_AA)
            cv2.polylines(f, [np.array(P, np.int32)], False, C(col), int(th), cv2.LINE_AA)
            cv2.polylines(f, [np.array([(p[0], p[1] - th * 0.2) for p in P], np.int32)], False, C((255, 200, 200)), max(2, int(th * 0.25)), cv2.LINE_AA)
        else:
            cv2.rectangle(f, (int(x - w_ / 2), int(yy - th / 2)), (int(x + w_ / 2), int(yy + th / 2)), C(INK), -1, cv2.LINE_AA)
            cv2.rectangle(f, (int(x - w_ / 2 + 4), int(yy - th / 2 + 4)), (int(x + w_ / 2 - 4), int(yy + th / 2 - 4)), C(col), -1, cv2.LINE_AA)
        if i < n - 1:
            sw = w_ * (0.25 + 0.5 * squash)
            sy = yy - th - 5 * s * k_open
            cv2.rectangle(f, (int(x - sw / 2 - 3), int(sy - 6 * s - 3)), (int(x + sw / 2 + 3), int(sy + 6 * s + 3)), C(INK), -1, cv2.LINE_AA)
            cv2.rectangle(f, (int(x - sw / 2), int(sy - 6 * s)), (int(x + sw / 2), int(sy + 6 * s)), C(SILV), -1, cv2.LINE_AA)
            cv2.line(f, (int(x - sw / 2), int(sy - 4 * s)), (int(x + sw / 2), int(sy - 4 * s)), C(WHITE), max(1, int(3 * s)), cv2.LINE_AA)


# ---------------- metal detector held by Chubby: pole from (hx, hy) to a coil at angle ----------------
def detector(f, hx, hy, L, ang, t, beep=0.0):
    a = math.radians(ang); ex, ey = hx + L * math.sin(a), hy + L * math.cos(a)
    cv2.line(f, (int(hx), int(hy)), (int(ex), int(ey)), C(INK), 18, cv2.LINE_AA)
    cv2.line(f, (int(hx), int(hy)), (int(ex), int(ey)), C((170, 176, 190)), 10, cv2.LINE_AA)
    bx, by = hx + 0.25 * L * math.sin(a), hy + 0.25 * L * math.cos(a)
    cv2.rectangle(f, (int(bx - 34), int(by - 22)), (int(bx + 34), int(by + 22)), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(bx - 28), int(by - 16)), (int(bx + 28), int(by + 16)), C((255, 200, 40)), -1, cv2.LINE_AA)
    lit = beep > 0.3 and (t * 8) % 1 < 0.5
    cv2.circle(f, (int(bx), int(by)), 9, C((255, 40, 40) if lit else (90, 30, 30)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(ex), int(ey)), (78, 26), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(ex), int(ey)), (68, 18), 0, 0, 360, C((60, 64, 80)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(ex), int(ey)), (44, 10), 0, 0, 360, C((40, 40, 50)), -1, cv2.LINE_AA)
    if beep > 0.05:
        for j in range(3):
            ph = (t * 2.4 + j / 3) % 1.0; r_ = 60 + 140 * ph
            ov = f.copy(); cv2.ellipse(ov, (int(ex), int(ey)), (int(r_), int(r_ * 0.45)), 0, 0, 360, C((255, 230, 90)), 7, cv2.LINE_AA)
            op = (1 - ph) * beep; f[:] = f * (1 - op) + ov * op
    return ex, ey


# ---------------- kitchen scale with a digital readout ----------------
def kscale_el(text="0 g", col=(120, 230, 160)):
    def mk():
        w, h, sc = 440, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: m.rounded_rectangle(S(20, 60, 420, 240), 28 * sc, fill=255)
        _outline(im, body, 11); shape_grad(im, body, (250, 250, 252), (196, 200, 212))
        pan = lambda m: m.rounded_rectangle(S(40, 20, 400, 64), 14 * sc, fill=255)
        _outline(im, pan, 9); shape_grad(im, pan, (226, 232, 242), (160, 168, 184))
        d.rounded_rectangle(S(110, 110, 330, 200), 14 * sc, fill=(26, 34, 30, 255), outline=INK + (255,), width=4 * sc)
        d.text((220 * sc, 156 * sc), text, font=font(F_BLACK, 52 * sc), fill=tuple(col) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("kscale", text, col), mk)


def paper_el(label="1 m²", w_=300, h_=360):
    def mk():
        w, h, sc = w_ + 20, h_ + 20, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(10, 10, w - 10, h - 10), fill=INK + (255,))
        d.rectangle(S(16, 16, w - 16, h - 16), fill=(255, 255, 255, 255))
        d.polygon(S(w - 16 - 50, 16, w - 16, 16 + 50, w - 16 - 50, 16 + 50), fill=(220, 222, 230, 255), outline=INK + (255,))
        for k in range(6): d.line(S(40, 80 + 40 * k, w - 50, 80 + 40 * k), fill=(200, 210, 230, 255), width=3 * sc)
        if label: d.text((w / 2 * sc, (h - 50) * sc), label, font=font(F_BLACK, 44 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("paper", label, w_, h_), mk)


# ---------------- periodic-table style element tile (define-on-sight for metals) ----------------
def elem_el(sym="Ag", num=47, name="SILVER", col=(214, 220, 232), bad=False):
    def mk():
        w, h, sc = 220, 250, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        box = lambda m: m.rounded_rectangle(S(10, 10, 210, 240), 22 * sc, fill=255)
        _outline(im, box, 11); shape_grad(im, box, tuple(min(255, c + 25) for c in col), tuple(int(c * 0.78) for c in col))
        d.text((30 * sc, 46 * sc), str(num), font=font(F_BOLD, 30 * sc), fill=INK + (255,), anchor="lm")
        d.text((110 * sc, 128 * sc), sym, font=font(F_BLACK, 104 * sc), fill=(RED_ if bad else INK) + (255,), anchor="mm")
        d.text((110 * sc, 206 * sc), name, font=font(F_BLACK, 30 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("elem", sym, num, name, col, bad), mk)


# ---------------- rule document with a generic round seal (no real logos) ----------------
def rule_doc_el(title="FOOD RULE", year="2016", lines_=("silver leaf:", "99.9% pure", "no animal parts")):
    def mk():
        w, h, sc = 420, 540, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        pg = lambda m: m.rectangle(S(20, 20, 400, 520), fill=255)
        _outline(im, pg, 11); shape_grad(im, pg, (255, 252, 240), (236, 226, 200))
        d.text((210 * sc, 76 * sc), title, font=font(F_BLACK, 46 * sc), fill=INK + (255,), anchor="mm")
        d.text((210 * sc, 126 * sc), year, font=font(F_BOLD, 36 * sc), fill=(150, 30, 30, 255), anchor="mm")
        for i, tx in enumerate(lines_): d.text((210 * sc, (200 + 56 * i) * sc), tx, font=font(F_BOLD, 34 * sc), fill=(50, 50, 60, 255), anchor="mm")
        d.ellipse(S(270, 390, 380, 500), fill=(200, 40, 40, 255), outline=INK + (255,), width=4 * sc)
        d.ellipse(S(288, 408, 362, 482), outline=(255, 220, 200, 255), width=4 * sc)
        for k in range(8):
            a = k * math.pi / 4; d.line(S(325 + 14 * math.cos(a), 445 + 14 * math.sin(a), 325 + 28 * math.cos(a), 445 + 28 * math.sin(a)), fill=(255, 220, 200, 255), width=3 * sc)
        return _done(im, w, h)
    return gcache(("ruledoc", title, year, lines_), mk)


def colour_bottle_el(label="E174", col=(200, 206, 220)):
    def mk():
        w, h, sc = 200, 320, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        b = lambda m: (m.rounded_rectangle(S(30, 90, 170, 300), 30 * sc, fill=255), m.rectangle(S(72, 40, 128, 100), fill=255))
        _outline(im, b, 11); shape_grad(im, b, (240, 246, 255), (180, 196, 220))
        d.rounded_rectangle(S(64, 20, 136, 52), 8 * sc, fill=(40, 40, 50, 255))
        tm = Image.new("L", im.size, 0); ImageDraw.Draw(tm).rounded_rectangle(S(36, 160, 164, 294), 26 * sc, fill=255)
        _silver_tex(im, tm, 4, sc)
        d.rounded_rectangle(S(44, 110, 156, 156), 10 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=3 * sc)
        d.text((100 * sc, 133 * sc), label, font=font(F_BLACK, 34 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("cbottle", label), mk)


def cow_el():
    """very simple friendly cow head icon (for 'animal' in the gut story — never gory)."""
    def mk():
        w, h, sc = 260, 240, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        hd = lambda m: (m.ellipse(S(50, 30, 210, 200), fill=255), m.ellipse(S(10, 50, 80, 90), fill=255), m.ellipse(S(180, 50, 250, 90), fill=255))
        _outline(im, hd, 11); shape_grad(im, hd, (255, 255, 255), (220, 220, 226))
        d.ellipse(S(70, 50, 120, 100), fill=(60, 50, 50, 255))
        d.ellipse(S(70, 130, 190, 210), fill=(255, 180, 190, 255), outline=INK + (255,), width=4 * sc)
        for nx in (105, 155): d.ellipse(S(nx - 9, 160, nx + 9, 180), fill=(120, 60, 70, 255))
        for ex in (100, 160): d.ellipse(S(ex - 10, 92, ex + 10, 114), fill=INK + (255,))
        for hx_, s_ in ((80, -1), (180, 1)): d.line(S(hx_, 44, hx_ + 18 * s_, 10), fill=(230, 210, 160, 255), width=10 * sc)
        return _done(im, w, h)
    return gcache("cow", mk)


def hair_cross(f, x, y, r, t, leaf_w=520):
    """magnified close-up: a hair seen end-on (big circle) next to a silver leaf seen edge-on (a hairline)."""
    if r < 12: return
    cv2.circle(f, (int(x - 120), int(y)), int(r), C(INK), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x - 120), int(y)), int(r - 8), C((110, 70, 40)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x - 120 - r * 0.3), int(y - r * 0.3)), int(r * 0.25), C((160, 110, 70)), -1, cv2.LINE_AA)
    yy = y + r + 70
    cv2.line(f, (int(x - leaf_w / 2), int(yy)), (int(x + leaf_w / 2), int(yy)), C(SILV_D), 3, cv2.LINE_AA)
    cv2.line(f, (int(x - leaf_w / 2), int(yy - 1)), (int(x + leaf_w / 2), int(yy - 1)), C(WHITE), 1, cv2.LINE_AA)
