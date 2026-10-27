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


# ================= travel / money-flow props (from the airline-miles video, 27 Oct 2026) =================
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


# ---- money-flow helpers: drifting clouds, curved animated arrows, gauge ----
def clouds(f, t, y0=760, sp=40, op=0.8):
    for i, (x, y, s) in enumerate(((180, y0, 1.0), (760, y0 + 260, 0.8), (420, y0 + 640, 1.2), (900, y0 + 760, 0.7))):
        xx = (x - sp * t * s) % 1400 - 180
        for dx, dy, r in ((0, 0, 60), (55, -22, 70), (115, 0, 55)):
            cv2.circle(f, (int(xx + dx * s), int(y + dy * s)), int(r * s), (op, op, op), -1, cv2.LINE_AA)


def _bez(p0, p1, u, bend):
    mx, my = (p0[0] + p1[0]) / 2 - bend * (p1[1] - p0[1]), (p0[1] + p1[1]) / 2 + bend * (p1[0] - p0[0])
    return (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1]


def along(p0, p1, u, bend=0.0): return _bez(p0, p1, u, bend)


def arrow(f, p0, p1, k, col=INK, th=12, bend=0.0):
    """animated curved arrow drawn k = 0..1"""
    if k <= 0.01: return
    n_ = 40; pts = [_bez(p0, p1, i / n_, bend) for i in range(int(n_ * k) + 1)]
    cv2.polylines(f, [np.array(pts, np.int32)], False, C(col), th, cv2.LINE_AA)
    if k > 0.95 and len(pts) > 2:
        (x0, y0), (x1, y1) = pts[-3], pts[-1]; a = math.atan2(y1 - y0, x1 - x0)
        tri = np.array([[x1 + 30 * math.cos(a), y1 + 30 * math.sin(a)], [x1 + 26 * math.cos(a + 2.3), y1 + 26 * math.sin(a + 2.3)],
                        [x1 + 26 * math.cos(a - 2.3), y1 + 26 * math.sin(a - 2.3)]], np.int32)
        cv2.fillPoly(f, [tri], C(col), cv2.LINE_AA)


def dial(f, cx, cy, r, v, lab="VALUE"):
    """semicircle gauge; v = 0..1 needle position (1 = high)"""
    cv2.ellipse(f, (cx, cy), (r + 16, r + 16), 0, 180, 360, C(INK), -1, cv2.LINE_AA)
    for i, col in enumerate(((232, 28, 36), (255, 199, 30), (22, 170, 76))):
        cv2.ellipse(f, (cx, cy), (r, r), 0, 180 + 60 * i, 240 + 60 * i, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy), (int(r * 0.55), int(r * 0.55)), 0, 180, 360, C(INK), -1, cv2.LINE_AA)
    a = math.pi * (1 - v)
    cv2.line(f, (cx, cy), (int(cx + r * 0.92 * math.cos(a)), int(cy - r * 0.92 * math.sin(a))), C(WHITE), 14, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), 26, C(WHITE), -1, cv2.LINE_AA)
    comp(f, chip(lab, INK, WHITE, 34), cx, cy + 60)


# ---- generic props added 27 Oct (De Beers video, render-tested): gem, ring, velvet pillow, hanging price tag, person icon (bride), sparkle,
# ---- vault drawer wall, hourglass, mine cart, vintage print-ad poster, typewriter, award medal, animated line chart, lab bell jar, hanging sign
ICE = (196, 236, 255); ICE2 = (120, 190, 240); SEPIA = (112, 74, 40); PAPER = (244, 232, 204); VELVET = (150, 20, 60)
GOLDL = (255, 214, 110); GOLDD = (176, 122, 30)


def gem_el(w=300, col=ICE, cracked=0.0):
    """brilliant-cut diamond, side view: table, crown facets, pavilion to a point. cracked 0..1 draws fracture lines."""
    def mk():
        sc = 2; h = int(w * 0.86); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        top, girdle, tip = h * 0.06, h * 0.34, h * 0.97
        tl, tr = w * 0.27, w * 0.73; gl, gr = w * 0.03, w * 0.97; cx = w / 2
        base = tuple(col)
        lt = lambda c, k: tuple(int(min(255, v + (255 - v) * k)) for v in c)
        dk = lambda c, k: tuple(int(v * (1 - k)) for v in c)
        # crown: table + 4 facets
        d.polygon(S(tl, top, tr, top, gr, girdle, gl, girdle), fill=lt(base, 0.35) + (255,))
        d.polygon(S(tl, top, tr, top, cx + w * 0.12, girdle * 0.72 + top * 0.28, cx - w * 0.12, girdle * 0.72 + top * 0.28), fill=lt(base, 0.7) + (255,))
        d.polygon(S(gl, girdle, tl, top, cx - w * 0.22, girdle), fill=dk(base, 0.08) + (255,))
        d.polygon(S(gr, girdle, tr, top, cx + w * 0.22, girdle), fill=dk(base, 0.18) + (255,))
        # pavilion: 4 long facets to the tip
        d.polygon(S(gl, girdle, cx - w * 0.22, girdle, cx, tip), fill=dk(base, 0.25) + (255,))
        d.polygon(S(cx - w * 0.22, girdle, cx, girdle, cx, tip), fill=lt(base, 0.25) + (255,))
        d.polygon(S(cx, girdle, cx + w * 0.22, girdle, cx, tip), fill=dk(base, 0.05) + (255,))
        d.polygon(S(cx + w * 0.22, girdle, gr, girdle, cx, tip), fill=dk(base, 0.38) + (255,))
        ol = dk(base, 0.62) + (255,); lw = max(2, int(w / 90)) * sc
        for seg in ((tl, top, tr, top), (tr, top, gr, girdle), (gr, girdle, cx, tip), (cx, tip, gl, girdle), (gl, girdle, tl, top),
                    (gl, girdle, gr, girdle), (cx - w * 0.22, girdle, cx, tip), (cx + w * 0.22, girdle, cx, tip), (cx, girdle, cx, tip),
                    (tl, top, cx - w * 0.22, girdle), (tr, top, cx + w * 0.22, girdle)):
            d.line(S(*seg), fill=ol, width=lw)
        d.polygon(S(tl + w * 0.04, top + h * 0.03, tl + w * 0.13, top + h * 0.03, tl + w * 0.02, girdle - h * 0.05), fill=(255, 255, 255, 200))
        if cracked > 0:
            rnd = np.random.default_rng(11)
            for j in range(int(1 + 4 * cracked)):
                x, y = cx + rnd.uniform(-w * 0.15, w * 0.15), girdle + rnd.uniform(-h * 0.1, h * 0.1); pts = [(x, y)]
                for _ in range(5):
                    x += rnd.uniform(-w * 0.12, w * 0.12); y += rnd.uniform(-h * 0.14, h * 0.14); pts.append((x, y))
                d.line([(px * sc, py * sc) for px, py in pts], fill=(30, 30, 40, 255), width=max(3, int(w / 60)) * sc, joint="curve")
        return _done(im, w, h)
    return gcache(("gem", w, col, round(cracked, 2)), mk)


def ring_el(w=420, gem=True):
    """gold band (seen at an angle) with a solitaire on top"""
    def mk():
        sc = 2; h = int(w * 1.15); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cy = h * 0.66; rx, ry = w * 0.44, h * 0.3
        shape_grad(im, lambda m: (m.ellipse(S(w / 2 - rx, cy - ry, w / 2 + rx, cy + ry), fill=255),
                                  m.ellipse(S(w / 2 - rx * 0.8, cy - ry * 0.74, w / 2 + rx * 0.8, cy + ry * 0.86), fill=0)), GOLDL, GOLDD)
        d.arc(S(w / 2 - rx + 6, cy - ry + 6, w / 2 + rx - 6, cy + ry - 6), 200, 300, fill=(255, 248, 220, 220), width=5 * sc)
        d.polygon(S(w / 2 - w * 0.12, cy - ry - 2, w / 2 + w * 0.12, cy - ry - 2, w / 2 + w * 0.07, cy - ry + h * 0.05, w / 2 - w * 0.07, cy - ry + h * 0.05), fill=GOLDD + (255,))
        if gem:
            g = gem_el(int(w * 0.5)); gi = Image.fromarray((np.dstack([g[0] / np.maximum(g[1][..., None], 1e-4), g[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
            gi = gi.resize((gi.size[0] * sc, gi.size[1] * sc), Image.LANCZOS)
            im.alpha_composite(gi, (int((w / 2) * sc - gi.size[0] / 2), int((cy - ry - h * 0.36) * sc)))
        return _done(im, w, h)
    return gcache(("ring", w, gem), mk)


def pillow_el(w=560):
    def mk():
        sc = 2; h = int(w * 0.42); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, h * 0.15, w, h), int(h * 0.4) * sc, fill=255), (200, 40, 90), (110, 10, 44))
        d.ellipse(S(w * 0.3, h * 0.2, w * 0.7, h * 0.48), fill=(90, 6, 36, 120))
        for x in (w * 0.08, w * 0.92):
            d.ellipse(S(x - 18, h * 0.82, x + 18, h + 0), fill=GOLDL + (255,))
        return _done(im, w, h)
    return gcache(("pillow", w), mk)


def hangtag_el(text, sub="", w=360, col=(255, 248, 230), fg=INK):
    """upright paper price tag, pointed top with a string hole at (w/2, 0.14 h); text horizontal"""
    def mk():
        sc = 2; h = int(w * 0.78); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w / 2, 3, w - 3, h * 0.26, w - 3, h - 3, 3, h - 3, 3, h * 0.26), fill=tuple(col) + (255,), outline=INK + (255,), width=5 * sc)
        d.ellipse(S(w / 2 - 13, h * 0.14 - 13, w / 2 + 13, h * 0.14 + 13), fill=(0, 0, 0, 0), outline=INK + (255,), width=4 * sc)
        fs = 66; fn = font(F_BLACK, fs * sc)
        while fn.getlength(text) / sc > w - 50 and fs > 20: fs -= 3; fn = font(F_BLACK, fs * sc)
        ty = h * 0.58 - (16 if sub else 0)
        d.text((w / 2 * sc, ty * sc), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        if sub: d.text((w / 2 * sc, (ty + fs * 0.62 + 18) * sc), sub, font=font(F_BOLD, 28 * sc), fill=(120, 110, 100, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("htag", text, sub, w, col, fg), mk)


def swing_tag(f, el, x, y, t, amp=6.0, L=80, ph=0.0):
    """hang an upright tag from pin (x, y) on a string, swinging gently"""
    a = amp * math.sin(t * 2.4 + ph); ra = math.radians(a)
    hx, hy = x + L * math.sin(ra), y + L * math.cos(ra)
    cv2.line(f, (int(x), int(y)), (int(hx), int(hy)), C(INK), 4, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 9, C(INK), -1, cv2.LINE_AA)
    h = el[1].shape[0]; dist = h * 0.36
    rot_comp(f, el, hx + dist * math.sin(ra), hy + dist * math.cos(ra), a, 1.0, 1.0, 0.3)


def bride_icon(f, x, y, s=1.0, lit=False, t=0.0):
    """bride icon: veil, head, dress. lit = white dress, warm glow, a sparkling diamond ring; unlit = faded"""
    ink = C(INK); lw = max(2, int(3 * s))
    if lit:
        cv2.circle(f, (int(x), int(y + 10 * s)), int(62 * s), C((255, 236, 150)), -1, cv2.LINE_AA)
    dress = C((255, 255, 255)) if lit else C((200, 192, 182)); veil = C((236, 244, 255)) if lit else C((214, 208, 200))
    cv2.fillPoly(f, [np.array([[x, y - 50 * s], [x - 32 * s, y + 24 * s], [x + 32 * s, y + 24 * s]], np.int32)], veil, cv2.LINE_AA)
    body = np.array([[x - 36 * s, y + 72 * s], [x + 36 * s, y + 72 * s], [x + 12 * s, y - 8 * s], [x - 12 * s, y - 8 * s]], np.int32)
    cv2.fillPoly(f, [body], dress, cv2.LINE_AA); cv2.polylines(f, [body], True, ink, lw, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y - 30 * s)), int(17 * s), C(SKIN) if lit else C((222, 214, 204)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y - 30 * s)), int(17 * s), ink, lw, cv2.LINE_AA)
    if lit:
        gx, gy = x + 26 * s, y + 20 * s; r = 12 * s * (1 + 0.12 * math.sin(t * 8))
        pts = np.array([[gx, gy - r], [gx + r * 0.8, gy], [gx, gy + r], [gx - r * 0.8, gy]], np.int32)
        cv2.fillPoly(f, [pts], C(ICE), cv2.LINE_AA); cv2.polylines(f, [pts], True, C((40, 110, 180)), lw, cv2.LINE_AA)
        sparkle(f, gx + 1.6 * r, gy - 1.6 * r, 1.4 * r, t, x * 0.01)


def sparkle(f, x, y, r, t, ph=0.0, col=(255, 255, 255)):
    k = 0.5 + 0.5 * math.sin(t * 6 + ph)
    if k < 0.15: return
    rr = r * k
    pts = np.array([[x, y - rr], [x + rr * 0.18, y - rr * 0.18], [x + rr, y], [x + rr * 0.18, y + rr * 0.18], [x, y + rr],
                    [x - rr * 0.18, y + rr * 0.18], [x - rr, y], [x - rr * 0.18, y - rr * 0.18]], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA)


def vault_wall(f, cx, cy, cols, rows, cell, k_open, t, locked=1.0):
    """wall of safe-deposit drawers; each holds gems; k_open = fraction of drawers lit/open"""
    x0 = cx - cols * cell / 2; y0 = cy - rows * cell / 2
    cv2.rectangle(f, (int(x0 - 18), int(y0 - 18)), (int(x0 + cols * cell + 18), int(y0 + rows * cell + 18)), C((70, 74, 86)), -1, cv2.LINE_AA)
    n = cols * rows
    for i in range(n):
        r, c = divmod(i, cols); x = x0 + c * cell; y = y0 + r * cell
        cv2.rectangle(f, (int(x + 6), int(y + 6)), (int(x + cell - 6), int(y + cell - 6)), C((160, 166, 180)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x + 6), int(y + 6)), (int(x + cell - 6), int(y + cell - 6)), C((60, 62, 72)), 3, cv2.LINE_AA)
        if (i * 7 % n) / n < k_open:
            comp(f, gem_el(int(cell * 0.5)), x + cell / 2, y + cell / 2)
            sparkle(f, x + cell * 0.7, y + cell * 0.3, cell * 0.12, t, i)
        else:
            cv2.circle(f, (int(x + cell / 2), int(y + cell / 2)), int(cell * 0.1), C((60, 62, 72)), -1, cv2.LINE_AA)
            if locked > 0.5: cv2.rectangle(f, (int(x + cell / 2 - 3), int(y + cell / 2)), (int(x + cell / 2 + 3), int(y + cell / 2 + cell * 0.18)), C((60, 62, 72)), -1)


def hourglass(f, cx, cy, h, top_k, t, drip=True):
    """hourglass of diamonds: top_k = how full the top bulb is (falls slowly), one gem drips through at a time"""
    w = h * 0.55
    frame = C(GOLDD)
    for yy in (cy - h / 2 - 16, cy + h / 2 + 16):
        cv2.rectangle(f, (int(cx - w / 2 - 40), int(yy - 14)), (int(cx + w / 2 + 40), int(yy + 14)), frame, -1, cv2.LINE_AA)
    glass = np.array([[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + 18, cy], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2], [cx - 18, cy]], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [glass], C((235, 245, 255)), cv2.LINE_AA); f[:] = f * 0.6 + ov * 0.4
    rnd = np.random.default_rng(4)
    # top bulb gems (stacked in a triangle that empties from the bottom)
    gs = 52
    for row in range(6):                       # top bulb: inverted triangle of gems, rows near the neck empty first
        n_ = 6 - row; y = cy - h / 2 + 46 + row * 44
        if row >= int(round(6 * top_k)): continue
        for c in range(n_): comp(f, gem_el(gs), cx + (c - (n_ - 1) / 2) * 50, y)
    for row in range(2):                       # bottom pile
        n_ = 3 - row; y = cy + h / 2 - 34 - row * 40
        for c in range(n_): comp(f, gem_el(gs), cx + (c - (n_ - 1) / 2) * 50, y)
    if drip:
        u = (t * 0.7) % 1.0; comp(f, gem_el(gs), cx, cy - 20 + u * (h / 2 - 90), op=clamp(u / 0.1) * clamp((1 - u) / 0.15))
    cv2.polylines(f, [glass], True, C((60, 90, 130)), 6, cv2.LINE_AA)


def minecart_el(w=520, load=1.0):
    def mk():
        sc = 2; h = int(w * 0.8); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rnd = np.random.default_rng(2)
        body_top = h * 0.36
        if load > 0:
            for i in range(int(40 * load)):
                gx = rnd.uniform(w * 0.14, w * 0.86); gy = body_top - rnd.uniform(0, h * 0.26) * (1 - abs(gx - w / 2) / (w * 0.45)) + 10
                g = gem_el(int(rnd.choice([54, 64, 74]))); gi = Image.fromarray((np.dstack([g[0] / np.maximum(g[1][..., None], 1e-4), g[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
                gi = gi.resize((gi.size[0] * sc, gi.size[1] * sc), Image.LANCZOS)
                im.alpha_composite(gi, (int(gx * sc - gi.size[0] / 2), int(gy * sc - gi.size[1] / 2)))
        shape_grad(im, lambda m: m.polygon(S(w * 0.04, body_top, w * 0.96, body_top, w * 0.86, h * 0.8, w * 0.14, h * 0.8), fill=255), (110, 116, 130), (60, 62, 74))
        d.rectangle(S(w * 0.02, body_top - 10, w * 0.98, body_top + 10), fill=(50, 52, 62, 255))
        for x in (w * 0.28, w * 0.72):
            d.ellipse(S(x - h * 0.12, h * 0.74, x + h * 0.12, h * 0.98), fill=(36, 36, 44, 255)); d.ellipse(S(x - h * 0.05, h * 0.81, x + h * 0.05, h * 0.91), fill=(160, 160, 170, 255))
        return _done(im, w, h)
    return gcache(("cart", w, round(load, 2)), mk)


def poster_el(lines, w=640, h=860, accent=(170, 30, 40), ring=True):
    """vintage 1940s print ad (sepia paper, serif type); lines = [(text, size, italic)]; ring=False drops the ring drawing"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(8, 10, w, h), fill=(0, 0, 0, 70))
        shape_grad(im, lambda m: m.rectangle(S(0, 0, w - 8, h - 10), fill=255), (248, 238, 212), (228, 210, 172))
        d.rectangle(S(22, 22, w - 30, h - 32), outline=SEPIA + (255,), width=4 * sc)
        d.rectangle(S(34, 34, w - 42, h - 44), outline=SEPIA + (180,), width=2 * sc)
        y = 90
        for text, size, ital in lines:
            fn = font(F_PFI if ital else F_PF9, size * sc)
            while fn.getlength(text) / sc > w - 110 and size > 18: size -= 2; fn = font(F_PFI if ital else F_PF9, size * sc)
            d.text((w / 2 * sc - 4 * sc, y * sc), text, font=fn, fill=(accent if ital else SEPIA) + (255,), anchor="mt"); y += size * 1.35
        # ring line drawing in the middle
        if not ring: return _done(im, w, h)
        cy = h * 0.62; d.ellipse(S(w / 2 - 110, cy - 50, w / 2 + 110, cy + 60), outline=SEPIA + (255,), width=8 * sc)
        d.polygon(S(w / 2 - 50, cy - 70, w / 2 + 50, cy - 70, w / 2, cy - 10), outline=SEPIA + (255,), fill=(255, 250, 235, 255), width=5 * sc)
        d.polygon(S(w / 2 - 50, cy - 70, w / 2 - 30, cy - 100, w / 2 + 30, cy - 100, w / 2 + 50, cy - 70), outline=SEPIA + (255,), fill=(255, 250, 235, 255), width=5 * sc)
        for k in range(6):
            a = -math.pi / 2 + (k - 2.5) * 0.45
            d.line(S(w / 2 + 120 * math.cos(a), cy - 80 + 90 * math.sin(a) - 40, w / 2 + 165 * math.cos(a), cy - 80 + 130 * math.sin(a) - 40), fill=SEPIA + (200,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("poster", tuple(lines), w, h, ring), mk)


def typewriter(f, cx, cy, text, k, t, w=640):
    """typewriter with a sheet of paper; k = fraction of text typed"""
    pw, ph = w * 0.72, w * 0.62
    cv2.rectangle(f, (int(cx - pw / 2), int(cy - ph - 40)), (int(cx + pw / 2), int(cy - 40)), C(PAPER), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - pw / 2), int(cy - ph - 40)), (int(cx + pw / 2), int(cy - 40)), C((190, 170, 130)), 3, cv2.LINE_AA)
    n = int(len(text) * k); shown = text[:n]
    lines = shown.split("\n")
    for i, ln in enumerate(lines):
        if ln: comp(f, ed_el(ln, "", "", lead_col=INK, lead_size=50), cx, cy - ph + 40 + i * 70)
    if k < 1 and int(t * 4) % 2 == 0:
        cv2.rectangle(f, (int(cx - 6), int(cy - ph + 50 + (len(lines) - 1) * 70 + 20)), (int(cx + 18), int(cy - ph + 50 + (len(lines) - 1) * 70 + 26)), C(INK), -1)
    body = np.array([[cx - w / 2, cy + 200], [cx + w / 2, cy + 200], [cx + w / 2 - 40, cy - 30], [cx - w / 2 + 40, cy - 30]], np.int32)
    cv2.fillPoly(f, [body], C((40, 44, 52)), cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - w / 2 - 30), int(cy - 60)), (int(cx + w / 2 + 30), int(cy - 20)), C((24, 26, 30)), -1, cv2.LINE_AA)
    for r in range(3):
        for c in range(9):
            kx = cx - w / 2 + 90 + c * (w - 180) / 8 + (r % 2) * 18; ky = cy + 30 + r * 52
            press = (int(t * 14) + c * 3 + r) % 11 == 0 and k < 1
            cv2.circle(f, (int(kx), int(ky + (5 if press else 0))), 20, C((235, 230, 215)), -1, cv2.LINE_AA)
            cv2.circle(f, (int(kx), int(ky + (5 if press else 0))), 20, C((24, 26, 30)), 3, cv2.LINE_AA)


def medal_el(text="SLOGAN OF THE CENTURY", w=360):
    def mk():
        sc = 2; h = int(w * 1.35); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w * 0.3, h * 0.55, w * 0.18, h, w * 0.33, h * 0.92, w * 0.45, h), fill=(210, 30, 50, 255))
        d.polygon(S(w * 0.7, h * 0.55, w * 0.82, h, w * 0.67, h * 0.92, w * 0.55, h), fill=(210, 30, 50, 255))
        shape_grad(im, lambda m: m.ellipse(S(w * 0.04, w * 0.04, w * 0.96, w * 0.96), fill=255), GOLDL, GOLDD)
        d.ellipse(S(w * 0.13, w * 0.13, w * 0.87, w * 0.87), outline=(255, 245, 200, 255), width=5 * sc)
        words = text.split(" "); ls = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [text]
        for i, ln in enumerate(ls):
            fn = font(F_BLACK, 40 * sc)
            while fn.getlength(ln) / sc > w * 0.66: fn = font(F_BLACK, int(fn.size / sc - 2) * sc)
            d.text((w / 2 * sc, (w * 0.5 + (i - (len(ls) - 1) / 2) * 50) * sc), ln, font=fn, fill=(90, 50, 10, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("medal", text, w), mk)


def line_chart(f, x0, y0, x1, y1, pts, k, col=RED_, th=12, labels=None, grid=True):
    """animated line chart in a box; pts = [(u, v)] with u,v in 0..1 (v=1 top); k = draw progress"""
    cv2.rectangle(f, (x0, y0), (x1, y1), C((255, 255, 255)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INK), 5, cv2.LINE_AA)
    if grid:
        for g in range(1, 4):
            yy = int(y0 + (y1 - y0) * g / 4); cv2.line(f, (x0 + 10, yy), (x1 - 10, yy), C((225, 225, 232)), 2, cv2.LINE_AA)
    P = [(x0 + 40 + u * (x1 - x0 - 80), y1 - 40 - v * (y1 - y0 - 80)) for u, v in pts]
    n = len(P) - 1; seg = k * n; out = [P[0]]
    for i in range(n):
        if seg >= i + 1: out.append(P[i + 1])
        elif seg > i:
            q = seg - i; out.append((P[i][0] + (P[i + 1][0] - P[i][0]) * q, P[i][1] + (P[i + 1][1] - P[i][1]) * q)); break
    if len(out) > 1: cv2.polylines(f, [np.array(out, np.int32)], False, C(col), th, cv2.LINE_AA)
    cv2.circle(f, (int(out[-1][0]), int(out[-1][1])), th + 6, C(col), -1, cv2.LINE_AA)
    if labels:
        for (u, txt) in labels: comp(f, ed_el(txt, "", "", lead_col=INK, lead_size=30), x0 + 40 + u * (x1 - x0 - 80), y1 + 34)
    return out[-1]


def flask_el(w=360, fill=0.6):
    """lab reactor / bell jar (generic)"""
    def mk():
        sc = 2; h = int(w * 1.35); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(w * 0.08, h * 0.86, w * 0.92, h), 14 * sc, fill=(60, 64, 76, 255))
        d.rounded_rectangle(S(w * 0.14, h * 0.12, w * 0.86, h * 0.87), int(w * 0.36) * sc, fill=(220, 240, 255, 110), outline=(80, 120, 170, 255), width=6 * sc)
        d.rectangle(S(w * 0.18, h * 0.87 - (h * 0.72) * fill * 0.25, w * 0.82, h * 0.86), fill=(150, 90, 255, 90))
        d.rounded_rectangle(S(w * 0.38, h * 0.02, w * 0.62, h * 0.14), 10 * sc, fill=(60, 64, 76, 255))
        d.arc(S(w * 0.2, h * 0.16, w * 0.5, h * 0.5), 190, 260, fill=(255, 255, 255, 200), width=8 * sc)
        return _done(im, w, h)
    return gcache(("flask", w, round(fill, 2)), mk)


def closed_sign_el(text="CLOSED", w=420):
    def mk():
        sc = 2; h = int(w * 0.62); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.line(S(w * 0.2, 0, w * 0.5, h * 0.22), fill=INK + (255,), width=5 * sc); d.line(S(w * 0.8, 0, w * 0.5, h * 0.22), fill=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(0, h * 0.22, w - 1, h - 1), 18 * sc, fill=RED_ + (255,), outline=INK + (255,), width=6 * sc)
        fn = font(F_BLACK, 90 * sc)
        while fn.getlength(text) / sc > w * 0.82: fn = font(F_BLACK, int(fn.size / sc - 4) * sc)
        d.text((w / 2 * sc, h * 0.61 * sc), text, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("closed", text, w), mk)


# ---- generic props added 27 Oct (Monopoly origin video): game board with invented street names (no real trade dress), board_xy,
# pawn_el, house_el, book_el (rulebook cover), gamebox_el, census_el, gavel_el, a woman character (lizzie/woman = guy + dress + bun), hat (fedora) ----
# Board: plain cream squares with INVENTED street names, no coloured property bands, no GO arrow, no mascot, no deed cards.
PAPER2 = (246, 236, 208); WOOD = (196, 140, 84); WOOD_D = (140, 92, 50)
BOARD_NAMES = ["LORD LANE", "RENT ROW", "CASH CT", "GREED ST", "TOLL RD", "LAND AVE", "DEBT DR", "MINT ST", "WAGE WAY",
               "PARK PL.", "TAX TER.", "COIN CT", "RICH RD", "LOAN LN", "DUE DR", "FEE FWY", "LEASE LN", "GOLD GR",
               "ACRE AVE", "PLOT PL", "DEED DR", "SHARE ST", "BANK BLVD", "RENT RD", "HOLD HWY", "VAULT VW", "OWN ORCH",
               "LOT LN", "TENANT TR", "YIELD YD", "PROFIT PK", "LEDGER LN", "BOND BLVD", "INCOME IN", "MARKET MW", "PENNY PL"]


def board_el(w=760, corners=("START", "GO TO JAIL", "PUBLIC PARK", "LORD'S\nMANOR"), centre="", hand=0.0, names=None, seed=0, n_side=9,
             paper=PAPER2):
    """square game board, top-down. hand>0 = hand-drawn copy (wobbly lines, pencil names)."""
    key = ("board", w, corners, centre, hand, tuple(names or ()), seed, n_side, paper)
    def mk():
        sc = 2; im, d = _canvas(w, w); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed)
        jit = lambda: (rng.uniform(-1, 1) * 3 * hand)
        _ov(im, lambda q: q.rounded_rectangle(S(12, 16, w - 2, w - 2), 18 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 12, w - 12), 14 * sc, fill=255), tuple(min(255, c + 6) for c in paper), tuple(max(0, c - 18) for c in paper))
        B_ = w - 14; cw = B_ * 0.15; sw = (B_ - 2 * cw) / n_side; o = 2
        col = (60, 54, 64, 255) if hand else INK + (255,); lw = (3 if hand else 4) * sc
        def L(x0, y0, x1, y1):
            d.line([((x0 + jit()) * sc, (y0 + jit()) * sc), ((x1 + jit()) * sc, (y1 + jit()) * sc)], fill=col, width=lw)
        L(o, o, o + B_, o); L(o, o + B_, o + B_, o + B_); L(o, o, o, o + B_); L(o + B_, o, o + B_, o + B_)
        L(o + cw, o + cw, o + B_ - cw, o + cw); L(o + cw, o + B_ - cw, o + B_ - cw, o + B_ - cw)
        L(o + cw, o + cw, o + cw, o + B_ - cw); L(o + B_ - cw, o + cw, o + B_ - cw, o + B_ - cw)
        for i in range(1, n_side):
            x = o + cw + i * sw
            L(x, o, x, o + cw); L(x, o + B_ - cw, x, o + B_)
            L(o, x, o + cw, x); L(o + B_ - cw, x, o + B_, x)
        nm = names or BOARD_NAMES
        fs = max(9, int(sw * 0.2)); fn = font(F_BOLD, fs * sc)
        k = 0
        for side in range(4):
            for i in range(n_side):
                c = o + cw + (i + 0.5) * sw
                if side == 0: x, y, rot = c, o + B_ - cw / 2, 0
                elif side == 1: x, y, rot = o + cw / 2, o + B_ - c, -90
                elif side == 2: x, y, rot = o + B_ - c, o + cw / 2, 180
                else: x, y, rot = o + B_ - cw / 2, c, 90
                txt = nm[(k + seed * 5) % len(nm)]; k += 1
                ti = Image.new("RGBA", (int(cw * 0.95 * sc), int(sw * 0.95 * sc)), (0, 0, 0, 0)); td = ImageDraw.Draw(ti)
                parts = txt.split(" ")
                for j, p in enumerate(parts[:2]):
                    td.text((ti.size[0] / 2, ti.size[1] * (0.5 + (j - (len(parts[:2]) - 1) / 2) * 0.3)), p, font=fn, fill=col, anchor="mm")
                ti = ti.rotate(90 if side in (0, 2) else 0, expand=True).rotate(rot if side in (1, 3) else (180 if side == 2 else 0), expand=True)
                im.alpha_composite(ti, (int(x * sc - ti.size[0] / 2), int(y * sc - ti.size[1] / 2)))
        fc = font(F_BLACK, int(cw * 0.15) * sc)
        for (cx, cy), lab in zip(((o + B_ - cw / 2, o + B_ - cw / 2), (o + cw / 2, o + B_ - cw / 2), (o + cw / 2, o + cw / 2), (o + B_ - cw / 2, o + cw / 2)), corners):
            for j, p in enumerate(lab.split("\n") if "\n" in lab else lab.split(" ", 1) if len(lab) > 7 else [lab]):
                nl = len(lab.split("\n") if "\n" in lab else lab.split(" ", 1) if len(lab) > 7 else [lab])
                d.text((cx * sc, (cy + (j - (nl - 1) / 2) * cw * 0.2) * sc), p, font=fc, fill=(RED_ if "JAIL" in lab else INK) + (255,), anchor="mm")
        if centre:
            fsz = int(w * 0.075)
            while fsz > 10 and font(F_PF9, fsz * sc).getlength(centre) > (B_ - 2 * cw) * 0.86 * sc: fsz -= 2
            d.text((w / 2 * sc, w / 2 * sc), centre, font=font(F_PF9 if not hand else F_BLACK, fsz * sc),
                   fill=(150, 30, 40, 255) if not hand else col, anchor="mm")
        return _done(im, w, w)
    return gcache(key, mk)


def board_xy(cx, cy, w, idx, n_side=9):
    """centre of square idx (0 = START corner bottom-right, going anticlockwise like the patent board) for a board drawn at (cx, cy) size w"""
    B_ = w - 14; cw = B_ * 0.15; sw = (B_ - 2 * cw) / n_side; per = n_side + 1
    side, i = divmod(idx % (4 * per), per); x0, y0 = cx - w / 2 + 2, cy - w / 2 + 2
    if side == 0: return (x0 + B_ - cw / 2 - (i * sw + (cw / 2 + sw / 2 - sw if i else 0)), y0 + B_ - cw / 2) if i == 0 else (x0 + B_ - cw - (i - 0.5) * sw, y0 + B_ - cw / 2)
    if side == 1: return (x0 + cw / 2, y0 + B_ - cw / 2) if i == 0 else (x0 + cw / 2, y0 + B_ - cw - (i - 0.5) * sw)
    if side == 2: return (x0 + cw / 2, y0 + cw / 2) if i == 0 else (x0 + cw + (i - 0.5) * sw, y0 + cw / 2)
    return (x0 + B_ - cw / 2, y0 + cw / 2) if i == 0 else (x0 + B_ - cw / 2, y0 + cw + (i - 0.5) * sw)


def pawn_el(w=90, col=(232, 60, 40)):
    def mk():
        h = int(w * 1.5); sc = 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.62)) for c in col)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.08, h * 0.78, w * 0.92, h * 0.98), fill=255), col, dk)
        shape_grad(im, lambda m: m.polygon(S(w * 0.3, h * 0.42, w * 0.7, h * 0.42, w * 0.84, h * 0.88, w * 0.16, h * 0.88), fill=255), col, dk)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.2, h * 0.36, w * 0.8, h * 0.48), fill=255), col, dk)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.22, h * 0.02, w * 0.78, h * 0.4), fill=255), tuple(min(255, c + 50) for c in col), col)
        d.ellipse(S(w * 0.34, h * 0.08, w * 0.48, h * 0.17), fill=(255, 255, 255, 150))
        return _done(im, w, h)
    return gcache(("pawn", w, col), mk)


def house_el(w=70, col=WOOD, hotel=False):
    def mk():
        ww = int(w * (1.7 if hotel else 1)); h = int(w * 0.95); sc = 3; im, d = _canvas(ww, h, sc); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.7)) for c in col)
        d.polygon(S(ww * 0.06, h * 0.42, ww * 0.5, h * 0.04, ww * 0.94, h * 0.42), fill=dk + (255,))
        shape_grad(im, lambda m: m.rectangle(S(ww * 0.14, h * 0.4, ww * 0.86, h * 0.98), fill=255), col, dk)
        d.rectangle(S(ww * 0.42, h * 0.62, ww * 0.58, h * 0.98), fill=(70, 46, 30, 255))
        return _done(im, ww, h)
    return gcache(("house", w, col, hotel), mk)


def book_el(title, sub, col, icon="fist", w=330):
    """a rulebook cover: title + simple icon (fist = crush, hands = share)"""
    def mk():
        h = int(w * 1.32); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.65)) for c in col)
        _ov(im, lambda q: q.rounded_rectangle(S(14, 18, w - 2, h - 2), 14 * sc, fill=(0, 0, 0, 80)))
        d.rounded_rectangle(S(w - 34, 12, w - 10, h - 20), 6 * sc, fill=(248, 244, 232, 255), outline=INK + (255,), width=3 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 22, h - 16), 14 * sc, fill=255), col, dk)
        d.rounded_rectangle(S(2, 2, w - 22, h - 16), 14 * sc, outline=INK + (255,), width=5 * sc)
        d.rectangle(S(20, 2, 34, h - 16), fill=dk + (255,))
        d.text(((w - 10) / 2 * sc, 64 * sc), "RULES", font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 230), anchor="mm")
        _ts = 46
        while _ts > 14 and font(F_BLACK, _ts * sc).getlength(title) > (w - 80) * sc: _ts -= 2
        d.text(((w - 10) / 2 * sc, 112 * sc), title, font=font(F_BLACK, _ts * sc), fill=(255, 255, 255, 255), anchor="mm")
        cx, cy = (w - 10) / 2, h * 0.58
        if icon == "fist":
            d.rounded_rectangle(S(cx - 62, cy - 50, cx + 62, cy + 40), 26 * sc, fill=(255, 236, 210, 255), outline=INK + (255,), width=5 * sc)
            for k in range(3): d.line(S(cx - 30 + 30 * k, cy - 50, cx - 30 + 30 * k, cy - 14), fill=INK + (255,), width=4 * sc)
            d.rounded_rectangle(S(cx - 40, cy + 30, cx + 40, cy + 90), 10 * sc, fill=(255, 236, 210, 255), outline=INK + (255,), width=5 * sc)
        else:
            for sx in (-1, 1):
                d.rounded_rectangle(S(cx + sx * 20 - 50 + (25 if sx > 0 else -25) * 0, cy - 26, cx + sx * 20 + 50, cy + 26), 24 * sc,
                                    fill=(255, 236, 210, 255) if sx < 0 else (226, 186, 150, 255), outline=INK + (255,), width=5 * sc)
            for k in range(-1, 2): d.text(((cx + 70 * k) * sc, (cy - 74) * sc), "$", font=font(F_BLACK, 40 * sc), fill=(255, 230, 120, 255), anchor="mm")
        d.text(((w - 10) / 2 * sc, (h - 70) * sc), sub, font=font(F_BOLD, 22 * sc), fill=(255, 255, 255, 235), anchor="mm")
        return _done(im, w, h)
    return gcache(("book", title, sub, col, icon, w), mk)


def gamebox_el(w=300, col=NAVY_, label="BOARD GAME"):
    """plain generic game box (no real packaging)"""
    def mk():
        h = int(w * 0.62); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.6)) for c in col)
        d.rectangle(S(6, h * 0.72, w - 6, h - 4), fill=dk + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 2, h * 0.8), 10 * sc, fill=255), tuple(min(255, c + 40) for c in col), col)
        d.rounded_rectangle(S(2, 2, w - 2, h * 0.8), 10 * sc, outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(w * 0.12, h * 0.18, w * 0.88, h * 0.6), 8 * sc, outline=(255, 255, 255, 200), width=3 * sc)
        d.text((w / 2 * sc, h * 0.39 * sc), label, font=font(F_BLACK, int(w * 0.085) * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("gbox", w, col, label), mk)


def census_el(w=640, rows=(("NAME", "ELIZABETH M. PHILLIPS"),), title="1940 CENSUS"):
    """census form card; rows are drawn by the shot (so they can be typed in)"""
    def mk():
        h = int(w * 0.82); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(12, 16, w - 2, h - 2), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rectangle(S(2, 2, w - 12, h - 12), fill=255), (246, 240, 222), (226, 216, 186))
        d.rectangle(S(2, 2, w - 12, h - 12), outline=(70, 60, 50, 255), width=4 * sc)
        d.rectangle(S(2, 2, w - 12, 76), fill=(70, 60, 50, 255))
        d.text((w / 2 * sc, 40 * sc), title, font=font(F_PF9, 38 * sc), fill=(246, 240, 222, 255), anchor="mm")
        for i in range(4):
            y = 150 + i * 110
            d.line(S(40, y + 34, w - 52, y + 34), fill=(120, 110, 96, 255), width=2 * sc)
        return _done(im, w, h)
    return gcache(("census", w, title), mk)


def gavel_el(w=360):
    def mk():
        h = int(w * 0.7); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(w * 0.42, h * 0.3, w * 0.98, h * 0.42), 10 * sc, fill=WOOD_D + (255,), outline=INK + (255,), width=4 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(w * 0.04, h * 0.06, w * 0.46, h * 0.66), 20 * sc, fill=255), WOOD, WOOD_D)
        d.rounded_rectangle(S(w * 0.04, h * 0.06, w * 0.46, h * 0.66), 20 * sc, outline=INK + (255,), width=5 * sc)
        for x in (0.12, 0.38): d.line(S(w * x, h * 0.06, w * x, h * 0.66), fill=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("gavel", w), mk)


def bun_hair(f, x, y, s=1.0, col=(92, 52, 30)):
    """Lizzie: hair bun + side hair drawn on top of guy() at feet (x, y), same s"""
    hx, hy = x, y - 178 * s - 168 * s - 76 * s
    cv2.ellipse(f, (int(hx), int(hy - 80 * s)), (int(44 * s), int(34 * s)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy - 58 * s)), (int(86 * s), int(30 * s)), 0, 180, 360, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy - 80 * s)), (int(44 * s), int(34 * s)), 0, 0, 360, C(INK), max(1, int(5 * s)), cv2.LINE_AA)


def dress(f, x, y, s=1.0, col=(120, 60, 170)):
    """long dress over the stick body (covers the tie), feet baseline y"""
    hip = (x, y - 178 * s); neck = (x, hip[1] - 168 * s)
    pts = np.array([[neck[0] - 26 * s, neck[1] + 8 * s], [neck[0] + 26 * s, neck[1] + 8 * s], [x + 30 * s, hip[1]], [x + 90 * s, y - 20 * s],
                    [x - 90 * s, y - 20 * s], [x - 30 * s, hip[1]]], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA); cv2.polylines(f, [pts], True, C(INK), max(1, int(6 * s)), cv2.LINE_AA)
    cv2.line(f, (int(x - 30 * s), int(hip[1])), (int(x + 30 * s), int(hip[1])), C(INK), max(1, int(5 * s)), cv2.LINE_AA)


def lizzie(f, x, y, s=1.0, **kw):
    """guy() dressed as Lizzie: draw the stick figure, then dress + bun (face stays the mascot style)"""
    hands = guy(f, x, y, s, **kw)
    dress(f, x, y, s)
    hel = head_el(kw.get("mouth", 0), kw.get("blink", False), kw.get("brow", "n"), kw.get("look", (0, 0))[0], kw.get("look", (0, 0))[1], kw.get("expr", "n"))
    bun_hair(f, x, y, s)
    comp(f, scale_el(hel, s), x, y - 178 * s - 168 * s - 76 * s + kw.get("bob", 0.0) * s)
    for side in (-1, 1):
        hx, hy = hands[side]
        cv2.circle(f, (int(hx), int(hy)), int(15 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(hx), int(hy)), int(10 * s), (1, 1, 1), -1, cv2.LINE_AA)
    return hands


def hat(f, x, y, s=1.0, col=(70, 66, 74)):
    """fedora on a standing guy at feet (x, y)"""
    hx, hy = x, y - 178 * s - 168 * s - 76 * s - 92 * s
    cv2.ellipse(f, (int(hx), int(hy + 22 * s)), (int(112 * s), int(18 * s)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx - 66 * s), int(hy - 40 * s)), (int(hx + 66 * s), int(hy + 20 * s)), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx - 66 * s), int(hy + 2 * s)), (int(hx + 66 * s), int(hy + 14 * s)), C((30, 28, 32)), -1, cv2.LINE_AA)


woman = lizzie
