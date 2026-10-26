# ================= props for "Why movie theaters make money on popcorn" (generic cinema props, no logos / trade dress) =================
STEEL = (150, 158, 172); POP = (255, 236, 170); POPD = (240, 196, 90)

def report_el(lines=(), hi=-1, k_hi=1.0, w=640, h=760, title="ANNUAL REPORT", year="2025"):
    """generic annual report page: title band, quote lines; line `hi` gets a highlighter swipe (k_hi 0..1)"""
    k_hi = round(k_hi, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(18, 20, w - 2, h - 2), fill=(0, 0, 0, 60)))
        d.rectangle(S(0, 0, w - 18, h - 20), fill=(255, 255, 255, 255))
        d.rectangle(S(0, 0, w - 18, 130), fill=(28, 52, 140, 255))
        d.text(((w - 18) / 2 * sc, 52 * sc), title, font=font(F_BLACK, 50 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text(((w - 18) / 2 * sc, 104 * sc), year, font=font(F_BOLD, 32 * sc), fill=(255, 214, 92, 255), anchor="mm")
        y = 180
        for i in range(3):
            d.rounded_rectangle(S(50, y + i * 34, w - 70 - (i % 2) * 90, y + i * 34 + 14), 6 * sc, fill=(214, 218, 228, 255))
        y = 310; fn = font(F_BLACK, 40 * sc)
        for i, ln in enumerate(lines):
            if i == hi and k_hi > 0:
                tw = fn.getlength(ln) / sc
                _ov(im, lambda q, y=y, tw=tw: q.rectangle(S((w - 18) / 2 - tw / 2 - 12, y - 26, (w - 18) / 2 - tw / 2 - 12 + (tw + 24) * k_hi, y + 26), fill=(255, 226, 40, 200)))
            d.text(((w - 18) / 2 * sc, y * sc), ln, font=fn, fill=INK + (255,), anchor="mm"); y += 62
        for i in range(3):
            yy = h - 150 + i * 34
            d.rounded_rectangle(S(50, yy, w - 70 - (i % 2) * 120, yy + 14), 6 * sc, fill=(214, 218, 228, 255))
        return _done(im, w, h)
    return gcache(("report", tuple(lines), hi, k_hi, w, h, title, year), mk)


def ticket_el(top="DAY PASS", big="$10", col=(255, 199, 30), w=520, h=260):
    """admission-ticket style pass with notches and perforation"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(14, 16, w - 2, h - 2), 22 * sc, fill=(0, 0, 0, 60)))
        d.rounded_rectangle(S(0, 0, w - 14, h - 16), 22 * sc, fill=tuple(col) + (255,), outline=INK + (255,), width=5 * sc)
        for cy in (0, h - 16):
            d.ellipse(S(w * 0.68 - 22, cy - 22, w * 0.68 + 22, cy + 22), fill=(0, 0, 0, 0))
        for y in range(30, h - 40, 22): d.line(S(w * 0.68, y, w * 0.68, y + 10), fill=INK + (255,), width=4 * sc)
        d.text((w * 0.34 * sc, 70 * sc), top, font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        d.text((w * 0.34 * sc, 160 * sc), big, font=font(F_BLACK, 96 * sc), fill=INK + (255,), anchor="mm")
        d.text((w * 0.84 * sc, 120 * sc), "1x", font=font(F_BLACK, 60 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("ticket", top, big, col, w, h), mk)


def popcorn_el(w=440, h=620, split=0.0, heap=1.0):
    """generic striped popcorn bucket with a puffy heap; split 0..1 shows an x-ray band: bottom 20% = FOOD COST, rest = KEPT"""
    split = round(split, 2); heap = round(heap, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        top_y = 210; bx0, bx1, tx0, tx1 = 70, w - 70, 20, w - 20
        body = S(tx0, top_y, tx1, top_y, bx1, h - 10, bx0, h - 10)
        _ov(im, lambda q: q.polygon(S(tx0 + 16, top_y + 16, tx1 + 16, top_y + 16, bx1 + 16, h - 2, bx0 + 16, h - 2), fill=(0, 0, 0, 60)))
        # heap of popcorn (drawn first, the bucket rim overlaps it)
        rng = np.random.default_rng(7)
        nh = int(46 * heap)
        for i in range(nh):
            a = rng.uniform(0, math.pi); rr = rng.uniform(0, 1) ** 0.6
            x = w / 2 + math.cos(a) * (w / 2 - 50) * rr * 1.05; y = top_y + 10 - math.sin(a) * 170 * heap * (1 - 0.5 * rr) - rng.uniform(0, 30)
            r = rng.uniform(26, 40)
            for k_ in range(3):
                ox, oy = rng.uniform(-r * 0.5, r * 0.5), rng.uniform(-r * 0.5, r * 0.5)
                d.ellipse(S(x + ox - r * 0.7, y + oy - r * 0.7, x + ox + r * 0.7, y + oy + r * 0.7), fill=POP + (255,), outline=POPD + (255,), width=2 * sc)
            d.ellipse(S(x - r * 0.3, y - r * 0.4, x, y - r * 0.1), fill=(255, 252, 236, 255))
            if i % 4 == 0: d.ellipse(S(x + 4, y + 2, x + 12, y + 10), fill=(214, 150, 50, 255))
        if split <= 0:
            shape_grad(im, lambda m: m.polygon(body, fill=255), (255, 255, 255), (232, 232, 238))
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon(body, fill=255)
            st = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(st)
            for i in range(-1, 9):
                x0 = tx0 + i * (tx1 - tx0) / 7; x1 = x0 + (tx1 - tx0) / 14
                xb0 = bx0 + i * (bx1 - bx0) / 7; xb1 = xb0 + (bx1 - bx0) / 14
                ds.polygon(S(x0, top_y, x1, top_y, xb1, h - 10, xb0, h - 10), fill=RED_ + (255,))
            im.paste(st, (0, 0), Image.fromarray(np.minimum(np.asarray(m), np.asarray(st.getchannel("A"))), "L"))
            _ov(im, lambda q: q.polygon(S(tx1 - 70, top_y, tx1, top_y, bx1, h - 10, bx1 - 50, h - 10), fill=(0, 0, 0, 40)))
            _ov(im, lambda q: q.polygon(S(tx0 + 30, top_y, tx0 + 60, top_y, bx0 + 42, h - 10, bx0 + 22, h - 10), fill=(255, 255, 255, 90)))
        else:
            # x-ray: glassy outline, popcorn inside, bottom band = cost
            d.polygon(body, fill=(255, 246, 214, 255))
            yc = h - 10 - (h - 10 - top_y) * 0.2
            fx = lambda y: (tx0 + (bx0 - tx0) * (y - top_y) / (h - 10 - top_y), tx1 + (bx1 - tx1) * (y - top_y) / (h - 10 - top_y))
            a0, a1 = fx(yc)
            d.polygon(S(a0, yc, a1, yc, bx1, h - 10, bx0, h - 10), fill=RED_ + (int(255 * split),))
            for i in range(30):
                x = rng.uniform(tx0 + 50, tx1 - 50); y = rng.uniform(top_y + 30, yc - 30)
                d.ellipse(S(x - 20, y - 20, x + 20, y + 20), fill=POP + (255,), outline=POPD + (255,), width=2 * sc)
            d.line(S(a0, yc, a1, yc), fill=INK + (255,), width=4 * sc)
        d.polygon(body, outline=INK + (255,))
        d.line(body + body[:2], fill=INK + (255,), width=6 * sc, joint="curve")
        d.rounded_rectangle(S(tx0 - 8, top_y - 12, tx1 + 8, top_y + 16), 12 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("popcorn", w, h, split, heap), mk)


def kernel_el(r=34, seed=0):
    def mk():
        sc = 2; s = int(r * 2.6); im, d = _canvas(s, s); rng = np.random.default_rng(seed); S = lambda *v: [x * sc for x in v]
        for k_ in range(4):
            ox, oy = rng.uniform(-r * 0.45, r * 0.45), rng.uniform(-r * 0.45, r * 0.45)
            d.ellipse(S(s / 2 + ox - r * 0.65, s / 2 + oy - r * 0.65, s / 2 + ox + r * 0.65, s / 2 + oy + r * 0.65), fill=POP + (255,), outline=POPD + (255,), width=2 * sc)
        d.ellipse(S(s / 2 - 6, s / 2 - 2, s / 2 + 4, s / 2 + 8), fill=(214, 150, 50, 255))
        return _done(im, s, s)
    return gcache(("kernel", r, seed), mk)


def cinema_el(w=900, h=640, glow=1.0, label=""):
    """generic auditorium: red drapes, glowing screen (optional label), rows of seat backs"""
    glow = round(glow, 2)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(16, 16, w - 2, h - 2), 30 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, w - 16, h - 16), 30 * sc, fill=(30, 20, 40, 255), outline=INK + (255,), width=6 * sc)
        g = int(170 + 85 * glow)
        shape_grad(im, lambda m: m.rounded_rectangle(S(120, 60, w - 136, 380), 12 * sc, fill=255), (g, g, min(255, g + 10)), (int(g * 0.75), int(g * 0.82), g))
        if label: d.text(((w - 16) / 2 * sc, 220 * sc), label, font=font(F_BLACK, 72 * sc), fill=INK + (255,), anchor="mm")
        for side in (0, 1):
            x0 = 20 if side == 0 else w - 146; x1 = x0 + 110
            shape_grad(im, lambda m, x0=x0, x1=x1: m.rectangle(S(x0, 20, x1, 470), fill=255), (210, 20, 40), (130, 8, 24))
            for k_ in range(4):
                xx = x0 + 14 + k_ * 26
                _ov(im, lambda q, xx=xx: q.rectangle(S(xx, 20, xx + 8, 470), fill=(0, 0, 0, 60)))
        d.rectangle(S(20, 14, w - 36, 56), fill=(170, 12, 30, 255))
        for row in range(2):
            y = 470 + row * 70
            for i in range(9):
                x = 50 + i * ((w - 116) / 9) + (row * 22)
                d.rounded_rectangle(S(x, y, x + 74, y + 90), 22 * sc, fill=(150, 20, 40, 255) if row else (180, 28, 50, 255), outline=INK + (255,), width=3 * sc)
        return _done(im, w, h)
    return gcache(("cinema", w, h, glow, label), mk)


def reel_el(r=170):
    """generic film reel with a trailing strip"""
    def mk():
        sc = 2; s = int(r * 2 + 20); im, d = _canvas(s + 200, s); S = lambda *v: [x * sc for x in v]
        c = s / 2
        d.polygon(S(c, c + r * 0.6, s + 190, c + r * 0.4, s + 190, c + r * 0.85, c, c + r), fill=(40, 40, 46, 255))
        for k_ in range(9):
            x = c + 40 + k_ * 34; d.rectangle(S(x, c + r * 0.62, x + 14, c + r * 0.68), fill=(230, 230, 230, 255))
        shape_grad(im, lambda m: m.ellipse(S(c - r, c - r, c + r, c + r), fill=255), (200, 206, 218), (120, 126, 140))
        d.ellipse(S(c - r, c - r, c + r, c + r), outline=INK + (255,), width=6 * sc)
        for k_ in range(5):
            a = k_ * 2 * math.pi / 5 - math.pi / 2; x = c + 0.55 * r * math.cos(a); y = c + 0.55 * r * math.sin(a)
            d.ellipse(S(x - r * 0.24, y - r * 0.24, x + r * 0.24, y + r * 0.24), fill=(40, 40, 50, 255))
        d.ellipse(S(c - r * 0.12, c - r * 0.12, c + r * 0.12, c + r * 0.12), fill=(40, 40, 50, 255))
        return _done(im, s + 200, s)
    return gcache(("reel", r), mk)


def pie(f, cx, cy, r, frac, col_a, col_b, k=1.0, explode=0.0, start=-90):
    """pie chart drawn straight to the frame: slice a = frac (animated by k), pushed out by `explode` px"""
    a1 = start + 360 * frac * clamp(k)
    mid = math.radians((start + a1) / 2)
    ex, ey = explode * math.cos(mid), explode * math.sin(mid)
    m_ = np.zeros((H, W), np.float32); cv2.ellipse(m_, (int(cx + 12), int(cy + 16)), (r, r), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    f *= (1 - 0.3 * m_)[..., None]
    cv2.ellipse(f, (int(cx), int(cy)), (r, r), 0, a1, start + 360, C(col_b), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy)), (r, r), 0, a1, start + 360, C(INK), 6, cv2.LINE_AA)
    if a1 > start + 0.5:
        cv2.ellipse(f, (int(cx + ex), int(cy + ey)), (r, r), 0, start, a1, C(col_a), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(cx + ex), int(cy + ey)), (r, r), 0, start, a1, C(INK), 6, cv2.LINE_AA)
        for a in (start, a1):
            cv2.line(f, (int(cx + ex), int(cy + ey)), (int(cx + ex + r * math.cos(math.radians(a))), int(cy + ey + r * math.sin(math.radians(a)))), C(INK), 6, cv2.LINE_AA)
    return mid


def balance(f, cx, cy, ang, left_el, right_el, arm=330):
    """balance scale: post + beam tilted by ang degrees (+ = right side down); pans hang from the beam ends"""
    ink = C(INK)
    cv2.rectangle(f, (int(cx - 18), int(cy)), (int(cx + 18), int(cy + 470)), C((90, 70, 50)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - 18), int(cy)), (int(cx + 18), int(cy + 470)), ink, 5, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy + 480)), (150, 34), 0, 0, 360, C(GOLD), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy + 480)), (150, 34), 0, 0, 360, ink, 5, cv2.LINE_AA)
    a = math.radians(ang); ends = []
    for s_ in (-1, 1):
        ends.append((cx + s_ * arm * math.cos(a), cy + s_ * arm * math.sin(a)))
    cv2.line(f, tuple(int(v) for v in ends[0]), tuple(int(v) for v in ends[1]), C(GOLD), 22, cv2.LINE_AA)
    cv2.line(f, tuple(int(v) for v in ends[0]), tuple(int(v) for v in ends[1]), ink, 4, cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy)), 26, C(GOLD), -1, cv2.LINE_AA); cv2.circle(f, (int(cx), int(cy)), 26, ink, 5, cv2.LINE_AA)
    for (ex, ey), el in zip(ends, (left_el, right_el)):
        py = ey + 230
        for dx in (-110, 110): cv2.line(f, (int(ex), int(ey)), (int(ex + dx), int(py)), ink, 4, cv2.LINE_AA)
        cv2.ellipse(f, (int(ex), int(py)), (130, 30), 0, 0, 180, C(GOLD), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(ex), int(py)), (130, 30), 0, 0, 180, ink, 5, cv2.LINE_AA)
        cv2.line(f, (int(ex - 130), int(py)), (int(ex + 130), int(py)), ink, 5, cv2.LINE_AA)
        if el is not None:
            hh = el[1].shape[0]
            comp(f, el, ex, py - hh / 2 + 4)
    return ends


def door_el(w=360, h=560, sign="ENTER"):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(18, 18, w - 2, h - 2), 18 * sc, fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 18, h - 18), 18 * sc, fill=255), (120, 70, 40), (80, 44, 24))
        d.rounded_rectangle(S(0, 0, w - 18, h - 18), 18 * sc, outline=INK + (255,), width=6 * sc)
        for y0 in (40, 290): d.rounded_rectangle(S(40, y0, w - 58, y0 + 200), 12 * sc, outline=(60, 30, 14, 255), width=5 * sc)
        d.ellipse(S(w - 90, h / 2 - 20, w - 54, h / 2 + 16), fill=GOLD + (255,), outline=INK + (255,), width=3 * sc)
        d.rounded_rectangle(S(60, 110, w - 78, 180), 14 * sc, fill=(255, 220, 90, 255), outline=INK + (255,), width=4 * sc)
        d.text(((w - 18) / 2 * sc, 146 * sc), sign, font=font(F_BLACK, 40 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("door", w, h, sign), mk)


def bill_el(text="BILLS", w=420, h=200, col=(250, 250, 250)):
    """a generic paper bill / invoice slip"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(12, 12, w - 2, h - 2), 14 * sc, fill=(0, 0, 0, 60)))
        d.rounded_rectangle(S(0, 0, w - 12, h - 12), 14 * sc, fill=tuple(col) + (255,), outline=INK + (255,), width=4 * sc)
        d.text(((w - 12) / 2 * sc, 60 * sc), text, font=font(F_BLACK, 52 * sc), fill=RED_ + (255,), anchor="mm")
        for k_ in range(3): d.rounded_rectangle(S(36, 110 + k_ * 22, w - 60 - k_ * 50, 122 + k_ * 22), 6 * sc, fill=(214, 218, 228, 255))
        return _done(im, w, h)
    return gcache(("bill", text, w, h, col), mk)
