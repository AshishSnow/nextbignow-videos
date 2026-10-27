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


# ---- generic data-viz props (from the Duolingo episode, 27 Oct 2026) ----

def odometer(f, cx, cy, text, k=1.0, cell=(96, 150), col=YEL_, seed=0):
    """rolling digit counter drawn straight on the frame; digits settle left-to-right as k goes 0..1"""
    n_ = len(text); cw, ch = cell; gap = 10; x0 = cx - (n_ * cw + (n_ - 1) * gap) / 2
    cv2.rectangle(f, (int(x0 - 26), int(cy - ch / 2 - 26)), (int(x0 + n_ * (cw + gap) - gap + 26), int(cy + ch / 2 + 26)), C(INK), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed)
    for i, c in enumerate(text):
        x = x0 + i * (cw + gap)
        if c in ",.":
            el = ed_el("", c, "", big_col=col, big_size=110, fp_big=F_BLACK, maxw=200)
            comp(f, el, x + cw / 2, cy + 8); continue
        cv2.rectangle(f, (int(x), int(cy - ch / 2)), (int(x + cw), int(cy + ch / 2)), C((250, 248, 240)), -1, cv2.LINE_AA)
        done = k >= (i + 1) / (n_ + 1)
        d_ = c if done or not c.isdigit() else str(int(rng.integers(0, 10) + k * 97 + i * 3) % 10)
        el = ed_el("", d_, "", big_col=INK, big_size=118, fp_big=F_BLACK, maxw=200)
        comp(f, el, x + cw / 2, cy + 2)
        cv2.line(f, (int(x), int(cy)), (int(x + cw), int(cy)), C((200, 200, 205)), 2)


def cents_grid(f, cx, cy, lit, col, cell=44, gap=8, k=1.0, dim=(255, 255, 255)):
    """10x10 grid = one dollar in cents; the first `lit` cells glow in col (k animates fill 0..1)"""
    n_on = int(round(lit * clamp(k)))
    s = cell + gap; x0 = cx - 5 * s + gap / 2; y0 = cy - 5 * s + gap / 2
    cv2.rectangle(f, (int(x0 - 24), int(y0 - 24)), (int(x0 + 10 * s + 16), int(y0 + 10 * s + 16)), C(INK), -1, cv2.LINE_AA)
    for i in range(100):
        r_, c_ = divmod(i, 10); x = int(x0 + c_ * s); y = int(y0 + (9 - r_) * s)
        on = i < n_on
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(col if on else dim), -1, cv2.LINE_AA)


def bars(f, x, base, w, hgt, col, k=1.0, label="", val=""):
    h_ = int(hgt * eo(clamp(k)))
    cv2.rectangle(f, (int(x - w / 2) + 8, base - h_ + 8), (int(x + w / 2) + 8, base), (0, 0, 0), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), base - h_), (int(x + w / 2), base), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), base - h_), (int(x + w / 2), base), C(INK), 6, cv2.LINE_AA)
    if label: comp(f, ed_el("", label, "", big_col=INK, big_size=40, maxw=300), x, base + 50)
    if val and k > 0.6: comp(f, ed_el("", val, "", big_col=INK, big_size=74, maxw=300), x, base - h_ - 60, op=clamp((k - 0.6) / 0.3))


def loop_diagram(f, cx, cy, r, steps, k, t, cols):
    """circular habit loop: arrow ring + step bubbles appearing in order as k goes 0..1"""
    n = len(steps)
    ang_end = -90 + 360 * clamp(k)
    cv2.ellipse(f, (int(cx), int(cy)), (int(r), int(r)), 0, -90, ang_end, C(INK), 30, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy)), (int(r), int(r)), 0, -90, ang_end, C(WHITE), 18, cv2.LINE_AA)
    a = math.radians(ang_end); hx, hy = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    tri = np.array([[hx + tx * 40, hy + ty * 40], [hx - tx * 6 + math.cos(a) * 34, hy - ty * 6 + math.sin(a) * 34],
                    [hx - tx * 6 - math.cos(a) * 34, hy - ty * 6 - math.sin(a) * 34]], np.int32)
    if k > 0.03: cv2.fillPoly(f, [tri], C(INK), cv2.LINE_AA)
    for i, s in enumerate(steps):
        q = i / n
        if k < q + 0.02: continue
        a = math.radians(-90 + 360 * q); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        comp(f, chip(s, cols[i % len(cols)], WHITE if cols[i % len(cols)] != YEL_ else INK, 40), x, y, scale=pin(t, 0, 0.01) * (1.0 + 0.15 * math.exp(-(k - q) * 30)))


def heatmap(f, cx, cy, k, cols=26, rows=14, cell=26, gap=5, col=(255, 120, 20), dim=(255, 255, 255)):
    """year grid (364 days) filling column by column as k goes 0..1"""
    n = cols * rows; on = int(round(n * clamp(k))); s = cell + gap
    x0 = int(cx - cols * s / 2); y0 = int(cy - rows * s / 2)
    cv2.rectangle(f, (x0 - 22, y0 - 22), (x0 + cols * s + 16, y0 + rows * s + 16), C(INK), -1, cv2.LINE_AA)
    for i in range(n):
        c_, r_ = divmod(i, rows); x = x0 + c_ * s; y = y0 + r_ * s
        shade = 0.75 + 0.25 * ((i * 37) % 7) / 6
        colr = tuple(min(255, int(v * shade)) for v in col) if i < on else (70, 70, 84)
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(colr), -1, cv2.LINE_AA)


def heart_line(f, x0, x1, y, t, k, col=(60, 230, 120), amp=90):
    """ECG line drawn up to fraction k with a moving beat"""
    pts = []
    n = 160
    for i in range(int(n * clamp(k)) + 1):
        q = i / n; x = x0 + (x1 - x0) * q; ph = (q * 3 + 0.2) % 1.0
        yy = y - amp * (math.exp(-((ph - 0.5) / 0.03) ** 2) - 0.45 * math.exp(-((ph - 0.56) / 0.03) ** 2) + 0.15 * math.exp(-((ph - 0.3) / 0.06) ** 2))
        pts.append([x, yy])
    if len(pts) > 1:
        p = np.array(pts, np.int32)
        cv2.polylines(f, [p], False, C(INK), 16, cv2.LINE_AA); cv2.polylines(f, [p], False, C(col), 9, cv2.LINE_AA)
        cv2.circle(f, tuple(p[-1]), 14, C(WHITE), -1, cv2.LINE_AA)


# ---- generic props from the gas-station video (27 Oct): receipt, coin pie, 100% stacked bar, cash pile, stage curtains ----
def receipt_el(rows, w=470, h=600, stamp=None, title="RECEIPT"):
    """paper receipt with zig-zag bottom; rows = [(left, right, bold)]"""
    key = ("rcpt", tuple(rows), w, h, stamp, title)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        zz = [(0, 0), (w, 0), (w, h - 20)]
        for i in range(int(w / 30), -1, -1): zz += [(i * 30 + 15, h), (i * 30, h - 20)]
        _ov(im, lambda q: q.polygon([(x * sc + 12 * sc, y * sc + 14 * sc) for x, y in zz], fill=(0, 0, 0, 60)))
        d.polygon([(x * sc, y * sc) for x, y in zz], fill=(255, 255, 252, 255), outline=(170, 170, 170, 255))
        d.text((w / 2 * sc, 50 * sc), title, font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.line(S(30, 90, w - 30, 90), fill=(150, 150, 150, 255), width=2 * sc)
        for i, (l, r, b) in enumerate(rows):
            y = 130 + i * 62; fn = font(F_BLACK if b else F_SEMI, (40 if b else 34) * sc)
            d.text((36 * sc, y * sc), l, font=fn, fill=INK + (255,), anchor="lm")
            d.text(((w - 36) * sc, y * sc), r, font=fn, fill=(GRN_ if b else INK) + (255,), anchor="rm")
        return _done(im, w, h)
    return gcache(key, mk)

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

def cash_pile(f, x, base, n_, k, s=0.7):
    """pile of cash bundles that builds up as k goes 0 -> 1"""
    m = int(round(n_ * clamp(k)))
    for i in range(m):
        r_, c_ = divmod(i, 3)
        xx = x + (c_ - 1) * 110 * s + (55 * s if r_ % 2 else 0); yy = base - r_ * 52 * s
        comp(f, scale_el(cash_el(1), s * 0.62), xx, yy)
