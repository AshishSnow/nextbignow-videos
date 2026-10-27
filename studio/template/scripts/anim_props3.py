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
