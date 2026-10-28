# ================= reusable prop library from ep 15 (chocolate) — materials helpers (mat_shade / mat_put) and the places
# set_chocolatier + marble_front + set_fridge_night live in anim_cine.py. Props: chocolate bar + piece + puddle, wrapped bar, cocoa pod + bean, cocoa-butter block, crystal "brick"
# stacks (cocoa butter forms 1-6) with morphing layouts, temperature gauge, tempering chart, pot + pool of melted chocolate,
# cake, glass jar, mould blob, spatula, sugar crystal =================
SCHEMES["cocoa"] = ((60, 30, 18), (150, 88, 52), (52, 26, 14), (0.35, 0.2, 0.1))
SCHEMES["butter"] = ((250, 214, 120), (255, 240, 190), (240, 200, 100), (0.8, 0.65, 0.3))
SCHEMES["crystal"] = ((22, 18, 60), (70, 60, 150), (18, 14, 50), (0.25, 0.22, 0.55))
SCHEMES["chalk"] = ((150, 146, 140), (214, 208, 198), (140, 134, 126), (0.5, 0.48, 0.44))
SCHEMES["frost"] = ((40, 90, 150), (150, 210, 250), (36, 80, 140), (0.2, 0.45, 0.7))
CHOC = (118, 66, 40); CHOC_D = (46, 22, 12); CHOC_H = (184, 122, 82)
BUT = (250, 222, 140); BUT_D = (196, 150, 60); BUT_H = (255, 246, 210)
BLOOMW = (236, 228, 214)

# ---------------- chocolate bar (segments as pillows), piece, puddle ----------------
def choc_bar_el(kind="gloss", cols=4, rows=2, seg=104, gap=12, bite=False, snap=0):
    """kind: gloss (tempered), matte (untempered / dull), chalky (bloomed). snap = number of columns broken off (right side)."""
    def mk():
        cc = cols - snap
        w = cc * seg + (cc + 1) * gap + 40; h = rows * seg + (rows + 1) * gap + 40; sc = 2
        cv = _Cv(w, h, sc)
        slab = cv.mask(lambda d, S: d.rounded_rectangle(S(20, 20, w - 20, h - 20), 16 * sc, fill=255))
        if bite:
            bm = cv.mask(lambda d, S: [d.ellipse(S(w - 90 + i * 8, 10 + i * 40, w + 30 + i * 8, 120 + i * 40), fill=255) for i in range(2)])
            slab = slab * (1 - bm)
        mat_put(cv, slab, CHOC, CHOC_D, CHOC_H, kind, 5, 0.35, seed=1)
        for r in range(rows):
            for c in range(cc):
                x0 = 20 + gap + c * (seg + gap); y0 = 20 + gap + r * (seg + gap)
                sm = cv.mask(lambda d, S, x0=x0, y0=y0: d.rounded_rectangle(S(x0 + 6, y0 + 6, x0 + seg - 6, y0 + seg - 6), 12 * sc, fill=255))
                sm = sm * (slab > 0.5)
                if sm.sum() < 10: continue
                gr = cv2.dilate(sm, np.ones((7, 7), np.uint8)); cv.fill(CHOC_D, gr * 0.45)
                cv.put(mat_shade(sm, CHOC, CHOC_D, CHOC_H, kind, 0.7, seed=r * 7 + c), sm)
        return cv.done()
    return gcache(("chocbar", kind, cols, rows, seg, gap, bite, snap), mk)


def choc_piece_el(kind="gloss", seg=150):
    def mk():
        w = h = seg + 40; sc = 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.rounded_rectangle(S(20, 20, w - 20, h - 20), 18 * sc, fill=255))
        mat_put(cv, m, CHOC, CHOC_D, CHOC_H, kind, 5, 0.55)
        im = cv.mask(lambda d, S: d.rounded_rectangle(S(38, 38, w - 38, h - 38), 14 * sc, fill=255))
        cv.put(mat_shade(im, CHOC, CHOC_D, CHOC_H, kind, 0.8, seed=3), im * 0.9)
        return cv.done()
    return gcache(("chocpiece", kind, seg), mk)


def puddle(f, x, y, r, k=1.0, t=0.0):
    """glossy melted-chocolate puddle (top-ish view), radius grows with k."""
    if k <= 0.01: return
    rx, ry = int(r * k), int(r * k * 0.36)
    cv2.ellipse(f, (int(x), int(y)), (rx + 5, ry + 5), 0, 0, 360, C(OUT3), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (rx, ry), 0, 0, 360, C((92, 48, 28)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x - rx * 0.1), int(y - ry * 0.15)), (int(rx * 0.75), int(ry * 0.55)), 0, 0, 360, C((124, 70, 42)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x - rx * 0.35), int(y - ry * 0.35)), (int(rx * 0.22), max(2, int(ry * 0.14))), -8, 0, 360, C((255, 236, 210)), -1, cv2.LINE_AA)


def melting_piece(f, x, y, s, k, kind="gloss", t=0.0):
    """a piece of chocolate that melts into a puddle: k 0 (solid) .. 1 (all liquid). (x, y) = bottom centre."""
    puddle(f, x, y, 120 * s, 0.35 + 0.9 * eo(k), t)
    if k < 0.98:
        el = scale_el(choc_piece_el(kind), s)
        sy = max(0.05, 1 - 0.95 * eio(k)); sx = 1 + 0.35 * eio(k)
        el2 = scale_xy(el, sx, sy)
        comp(f, el2, x, y - el2[1].shape[0] / 2 + 8 * s)
        for i in range(3):                                  # drips running down
            dk = clamp(k * 2.2 - i * 0.25)
            if 0 < dk < 1:
                dx = x + (i - 1) * 50 * s; dy = y - el2[1].shape[0] * 0.4 + 60 * s * dk
                cv2.ellipse(f, (int(dx), int(dy)), (int(14 * s), int(22 * s * (0.6 + dk))), 0, 0, 360, C((92, 48, 28)), -1, cv2.LINE_AA)


# ---------------- wrapped bar (generic: paper sleeve + foil, no brand) ----------------
def wrapped_bar_el(open_=0.45, kind="gloss"):
    def mk():
        bar = choc_bar_el(kind)
        bh, bw = bar[1].shape; w, h, sc = bw + 40, bh + 40, 2
        im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        bimg = _pil_from_el(bar, bw * sc, bh * sc); im.alpha_composite(bimg, (20 * sc, 20 * sc))
        xs = 20 + bw * open_
        _ov(im, lambda q: q.rectangle(S(xs - 30, 14, xs + 10, h - 14), fill=(214, 220, 230, 255)))       # foil edge
        for i in range(6): d.line(S(xs - 30, 22 + i * (h - 44) / 5, xs + 4, 30 + i * (h - 44) / 5), fill=(150, 160, 176, 255), width=3 * sc)
        d.rounded_rectangle(S(xs, 8, w - 8, h - 8), 14 * sc, fill=(200, 40, 50, 255), outline=OUT3 + (255,), width=5 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(xs + 6, 14, w - 14, h - 14), 10 * sc, fill=255), (232, 70, 70), (150, 20, 34))
        d.rectangle(S(xs + 6, h * 0.42, w - 14, h * 0.58), fill=(255, 214, 120, 255))
        _ov(im, lambda q: q.rectangle(S(xs + 16, 20, w - 24, 40), fill=(255, 255, 255, 70)))
        return _done(im, w, h)
    return gcache(("wrapbar", open_, kind), mk)


def _pil_from_el(el, w, h):
    pm, a = el; rgb = np.where(a[..., None] > 1e-4, pm / np.maximum(a[..., None], 1e-4), 0)
    arr = (np.dstack([np.clip(rgb, 0, 1), np.clip(a, 0, 1)[..., None]]) * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA").resize((int(w), int(h)), Image.LANCZOS)


# ---------------- cocoa pod (whole or opened) + bean + cocoa-butter block ----------------
def pod_el(open_=False):
    def mk():
        w, h, sc = 300, 520, 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.ellipse(S(40, 30, 260, 500), fill=255))
        if not open_:
            mat_put(cv, m, (236, 150, 40), (150, 70, 14), (255, 214, 120), "satin", 6, 0.9)
            for i in range(-2, 3):
                rm = cv.mask(lambda d, S, i=i: d.arc(S(150 + i * 38 - 70, 40, 150 + i * 38 + 70, 490), 70 if i < 0 else 250, 110 if i < 0 else 290, fill=255, width=6 * sc) if i else d.line(S(150, 50, 150, 480), fill=255, width=6 * sc))
                cv.fill((170, 84, 20), rm * 0.6)
        else:
            mat_put(cv, m, (236, 150, 40), (150, 70, 14), (255, 214, 120), "satin", 6, 0.9)
            pm_ = cv.mask(lambda d, S: d.ellipse(S(72, 62, 228, 468), fill=255))
            cv.put(mat_shade(pm_, (250, 244, 232), (200, 186, 170), None, "satin", 0.6), pm_)
            for r_ in range(6):
                for c_ in (-1, 1):
                    bx, by = 150 + c_ * 34, 110 + r_ * 58
                    bm = cv.mask(lambda d, S, bx=bx, by=by: d.ellipse(S(bx - 28, by - 22, bx + 28, by + 22), fill=255))
                    cv.put(mat_shade(bm, (150, 86, 70), (80, 40, 34), (210, 150, 130), "satin", 0.8), bm)
        return cv.done()
    return gcache(("pod", open_), mk)


def bean_el():
    def mk():
        w, h, sc = 220, 150, 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.ellipse(S(20, 20, 200, 130), fill=255))
        mat_put(cv, m, (150, 90, 60), (70, 36, 22), (214, 160, 120), "satin", 5, 0.9)
        cm = cv.mask(lambda d, S: d.arc(S(40, 30, 180, 130), 200, 340, fill=255, width=5 * sc))
        cv.fill((80, 44, 28), cm)
        return cv.done()
    return gcache("bean", mk)


def butter_el():
    def mk():
        w, h, sc = 360, 260, 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.polygon(S(40, 90, 230, 40, 330, 90, 330, 200, 140, 240, 40, 200), fill=255))
        mat_put(cv, m, BUT, BUT_D, BUT_H, "satin", 5, 0.5)
        tm = cv.mask(lambda d, S: d.polygon(S(48, 92, 230, 46, 322, 90, 140, 138), fill=255))
        cv.fill((255, 244, 200), tm * 0.55)
        return cv.done()
    return gcache("cbutter", mk)


# ---------------- crystal 'brick' stacks: cocoa butter forms 1..6 = the same bricks built six ways ----------------
FORM_COL = {1: (250, 214, 150), 2: (250, 214, 150), 3: (250, 214, 150), 4: (250, 214, 150), 5: (255, 200, 60), 6: (214, 206, 196)}


def brick_el(col=BUT, w=70, h=34):
    def mk():
        sc = 2; cv = _Cv(w + 16, h + 16, sc)
        m = cv.mask(lambda d, S: d.rounded_rectangle(S(8, 8, w + 8, h + 8), 7 * sc, fill=255))
        mat_put(cv, m, col, tuple(int(c * 0.62) for c in col), tuple(min(255, c + 30) for c in col), "satin", 3, 0.6)
        return cv.done()
    return gcache(("brick", col, w, h), mk)


def brick_layout(form, n=12):
    """list of (dx, dy, rot) for n bricks around (0, 0). 1-4 = loose/messy, 5 = neat running bond, 6 = tightest pack."""
    rng = np.random.default_rng(form * 13 + 5); out = []
    if form == 6:
        for i in range(n):
            r_, c_ = divmod(i, 4); out.append(((c_ - 1.5) * 70 + (35 if r_ % 2 else 0) - 17, (r_ - 1) * 34, 0.0))
        return out
    if form == 5:
        for i in range(n):
            r_, c_ = divmod(i, 3); out.append(((c_ - 1) * 78 + (39 if r_ % 2 else 0) - 19, (r_ - 1.5) * 40, 0.0))
        return out
    jit, rot = {1: (46, 70), 2: (30, 36), 3: (18, 18), 4: (9, 8)}[form]
    for i in range(n):
        r_, c_ = divmod(i, 3)
        out.append(((c_ - 1) * 92 + rng.uniform(-jit, jit), (r_ - 1.5) * 56 + rng.uniform(-jit, jit) * 0.7, rng.uniform(-rot, rot)))
    return out


def lerp_layout(a, b, k):
    k = eio(clamp(k)); return [(x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, r0 + (r1 - r0) * k) for (x0, y0, r0), (x1, y1, r1) in zip(a, b)]


def draw_bricks(f, cx, cy, layout, s=1.0, col=BUT, op=1.0, t=0.0, wob=0.0, melt=0.0, shadow=0.25):
    el = scale_el(brick_el(col), s)
    for i, (dx, dy, r) in enumerate(layout):
        mk = clamp(melt * 1.6 - (i % 5) * 0.12)
        if mk >= 0.99: continue
        x = cx + dx * s + wob * 6 * math.sin(t * 9 + i); y = cy + dy * s + wob * 5 * math.cos(t * 7 + i * 2) + 40 * s * mk
        e2 = scale_xy(el, 1 + 0.4 * mk, max(0.08, 1 - mk)) if mk > 0 else el
        rot_comp(f, e2, x, y, r + wob * 4 * math.sin(t * 6 + i), 1.0, op * (1 - 0.6 * mk), shadow)


def form_stack(f, form, cx, cy, s=1.0, t=0.0, op=1.0, num=True, wob=None, melt=0.0, glow_=False, lab=None):
    if glow_: glow(f, cx, cy, 170 * s, (255, 210, 90), 0.55)
    draw_bricks(f, cx, cy, brick_layout(form), s, FORM_COL[form], op, t, (1.0 if form <= 4 else 0.0) if wob is None else wob, melt)
    if num: comp(f, chip(lab or f"SHAPE {form}", INK if form != 5 else (150, 90, 0), WHITE, int(26 * max(0.8, s))), cx, cy + 165 * s, op=op)


# ---------------- temperature gauge with marks (34 = melts, 37 = your mouth) ----------------
def temp_gauge(f, x, yb, h_, val, lo=20.0, hi=40.0, marks=(), col=(240, 70, 50), w_=46):
    """vertical thermometer, bulb at (x, yb), scale lo..hi C over h_ px; marks = [(deg, text, chip_col)] drawn to the right."""
    def Y(v): return yb - 60 - (h_ - 80) * clamp((v - lo) / (hi - lo))
    cv2.rectangle(f, (int(x - w_), int(yb - h_)), (int(x + w_), int(yb)), C(OUT3), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(yb)), int(w_ * 1.9), C(OUT3), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w_ + 10), int(yb - h_ + 12)), (int(x + w_ - 10), int(yb)), C((250, 248, 244)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(yb)), int(w_ * 1.9 - 10), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w_ * 0.45), int(Y(val))), (int(x + w_ * 0.45), int(yb)), C(col), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x - w_ * 0.6), int(yb - w_ * 0.6)), int(w_ * 0.35), C((255, 200, 190)), -1, cv2.LINE_AA)
    for v in range(int(lo), int(hi) + 1, 2):
        L = 26 if v % 10 == 0 else 14
        cv2.line(f, (int(x - w_ + 10), int(Y(v))), (int(x - w_ + 10 + L), int(Y(v))), C(OUT3), 3, cv2.LINE_AA)
    for v, txt, cc in marks:
        y = Y(v); cv2.line(f, (int(x + w_), int(y)), (int(x + w_ + 50), int(y)), C(cc), 8, cv2.LINE_AA)
        ch_ = chip(txt, cc, WHITE, 32); comp(f, ch_, x + w_ + 56 + ch_[1].shape[1] / 2, y)
    return Y


# ---------------- tempering chart: MELT (hot) -> COOL (down) -> WARM A LITTLE (small rise) ----------------
def temper_chart(f, t, ts, x0=150, x1=930, y0=700, y1=1270):
    """ts = (t_melt, t_cool, t_warm). The line draws itself segment by segment in sync with the voice."""
    cv2.rectangle(f, (x0 - 30, y0 - 40), (x1 + 30, y1 + 70), C((255, 250, 242)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0 - 30, y0 - 40), (x1 + 30, y1 + 70), C(OUT3), 6, cv2.LINE_AA)
    cv2.line(f, (x0, y0), (x0, y1), C(OUT3), 6, cv2.LINE_AA); cv2.line(f, (x0, y1), (x1, y1), C(OUT3), 6, cv2.LINE_AA)
    comp(f, chip("HOT", (220, 70, 40), WHITE, 24), x0 - 2, y0 - 40); comp(f, chip("COOL", (60, 130, 220), WHITE, 24), x0 + 56, y1 - 30)
    comp(f, chip("TIME", OUT3, WHITE, 22), x1 - 50, y1 + 38)
    P = [(x0 + 10, y0 + 70), (x0 + 250, y0 + 70), (x0 + 520, y1 - 110), (x0 + 600, y1 - 110), (x1 - 20, y1 - 250)]
    segs = [(P[0], P[1], ts[0], (220, 70, 40)), (P[1], P[2], ts[1], (60, 130, 220)), (P[2], P[3], ts[1] + 0.6, (60, 130, 220)), (P[3], P[4], ts[2], (240, 150, 40))]
    head = None
    for (a, b, tsg, col) in segs:
        if t < tsg: break
        k = eio(clamp((t - tsg) / 0.7)); e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        cv2.line(f, (int(a[0]), int(a[1])), (int(e[0]), int(e[1])), C(OUT3), 20, cv2.LINE_AA)
        cv2.line(f, (int(a[0]), int(a[1])), (int(e[0]), int(e[1])), C(col), 12, cv2.LINE_AA); head = e
    if head is not None: cv2.circle(f, (int(head[0]), int(head[1])), 16, C(WHITE), -1, cv2.LINE_AA); cv2.circle(f, (int(head[0]), int(head[1])), 16, C(OUT3), 5, cv2.LINE_AA)
    labs = [("1  MELT", (P[0][0] + P[1][0]) / 2 + 60, P[0][1] - 50, ts[0], (220, 70, 40)), ("2  COOL", (P[1][0] + P[2][0]) / 2 - 110, (P[1][1] + P[2][1]) / 2 + 40, ts[1], (60, 130, 220)),
            ("3  WARM A LITTLE", (P[3][0] + P[4][0]) / 2 - 60, P[3][1] + 70, ts[2], (230, 130, 20))]
    for txt, lx, ly, tl, col in labs:
        if t >= tl + 0.2: comp(f, chip(txt, col, WHITE, 30), lx, ly, scale=pin(t, tl + 0.2, 0.25))
    return head


# ---------------- pot of melted chocolate (side) + pool (top-down) ----------------
def pot_el():
    def mk():
        w, h, sc = 460, 330, 2; cv = _Cv(w, h, sc)
        body = cv.mask(lambda d, S: d.rounded_rectangle(S(50, 90, 410, 300), 40 * sc, fill=255))
        mat_put(cv, body, (214, 120, 70), (120, 56, 30), (255, 200, 150), "gloss", 6, 0.8)
        hm = cv.mask(lambda d, S: [d.rounded_rectangle(S(4, 130, 70, 160), 14 * sc, fill=255), d.rounded_rectangle(S(390, 130, 456, 160), 14 * sc, fill=255)])
        mat_put(cv, hm, (90, 60, 50), (40, 26, 22), None, "satin", 4, 0.5)
        rim = cv.mask(lambda d, S: d.ellipse(S(44, 66, 416, 124), fill=255))
        mat_put(cv, rim, (230, 140, 90), (140, 70, 40), None, "satin", 5, 0.4)
        surf = cv.mask(lambda d, S: d.ellipse(S(62, 74, 398, 116), fill=255))
        cv.put(mat_shade(surf, CHOC, CHOC_D, CHOC_H, "gloss", 0.3), surf)
        return cv.done()
    return gcache("pot", mk)


def pool(f, cx, cy, r, t, op=1.0):
    """top-down disc of melted chocolate with slow swirling highlights."""
    g = f if op >= 0.999 else f.copy()
    cv2.circle(g, (int(cx), int(cy)), int(r + 14), C(OUT3), -1, cv2.LINE_AA)
    cv2.circle(g, (int(cx), int(cy)), int(r), C((96, 52, 30)), -1, cv2.LINE_AA)
    for i in range(5):
        a = t * 0.4 + i * 1.25; rr = r * (0.25 + 0.13 * i)
        cv2.ellipse(g, (int(cx), int(cy)), (int(rr), int(rr)), math.degrees(a), 0, 70, C((140, 84, 52)), 10, cv2.LINE_AA)
    cv2.ellipse(g, (int(cx - r * 0.4), int(cy - r * 0.45)), (int(r * 0.3), int(r * 0.09)), -30, 0, 360, C((255, 236, 214)), -1, cv2.LINE_AA)
    if op < 0.999: f[:] = f * (1 - op) + g * op


# ---------------- cake (chocolate drip cake), glass jar, mould blob, spatula ----------------
def cake_el():
    def mk():
        w, h, sc = 460, 420, 2; cv = _Cv(w, h, sc)
        pl = cv.mask(lambda d, S: d.ellipse(S(10, 330, 450, 410), fill=255))
        mat_put(cv, pl, (240, 240, 246), (170, 170, 186), None, "gloss", 4, 0.3)
        body = cv.mask(lambda d, S: [d.rectangle(S(50, 120, 410, 360), fill=255), d.ellipse(S(50, 320, 410, 400), fill=255)])
        mat_put(cv, body, (140, 82, 52), (70, 36, 22), (190, 128, 90), "matte", 5, 0.5)
        for yy in (190, 270):
            lm = cv.mask(lambda d, S, yy=yy: d.rectangle(S(52, yy, 408, yy + 14), fill=255)); cv.fill((250, 230, 200), lm * 0.85)
        top = cv.mask(lambda d, S: [d.ellipse(S(46, 80, 414, 160), fill=255)] + [d.ellipse(S(60 + i * 48, 120, 96 + i * 48, 170 + (i * 37 % 60)), fill=255) for i in range(7)])
        mat_put(cv, top, CHOC, CHOC_D, CHOC_H, "gloss", 5, 0.4)
        for i in range(3):
            bm = cv.mask(lambda d, S, i=i: d.ellipse(S(150 + i * 60, 60, 190 + i * 60, 100), fill=255))
            mat_put(cv, bm, (220, 40, 60), (120, 10, 30), (255, 140, 150), "gloss", 4, 0.9)
        return cv.done()
    return gcache("cake", mk)


def jar_el(filled=True):
    """glass storage jar with a lid (glass = Fresnel: clear middle, bright rim + edges) holding chocolate pieces."""
    def mk():
        w, h, sc = 300, 400, 2; cv = _Cv(w, h, sc)
        if filled:
            for i, (px, py) in enumerate(((100, 300), (180, 290), (140, 230), (100, 180), (190, 210))):
                pm = cv.mask(lambda d, S, px=px, py=py: d.rounded_rectangle(S(px - 46, py - 40, px + 46, py + 40), 12 * sc, fill=255))
                mat_put(cv, pm, CHOC, CHOC_D, CHOC_H, "gloss", 3, 0.6, seed=i)
        gm = cv.mask(lambda d, S: d.rounded_rectangle(S(30, 80, 270, 380), 40 * sc, fill=255))
        e = cv2.erode((gm > 0.5).astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
        edge = np.clip(gm - cv2.GaussianBlur(e, (0, 0), 10) * 0.85, 0, 1)
        cv.fill((220, 236, 250), edge * 0.75)
        rf = cv.mask(lambda d, S: d.rounded_rectangle(S(60, 110, 84, 340), 12 * sc, fill=255)); cv.fill((255, 255, 255), rf * 0.6)
        cv.outline(gm - cv2.erode(gm, np.ones((5, 5), np.uint8)), 2, (120, 140, 160))
        lid = cv.mask(lambda d, S: d.rounded_rectangle(S(40, 40, 260, 92), 14 * sc, fill=255))
        mat_put(cv, lid, (60, 170, 130), (20, 96, 74), (140, 230, 190), "satin", 5, 0.6)
        return cv.done()
    return gcache(("jar", filled), mk)


def mould_el():
    def mk():
        w, h, sc = 260, 200, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(4)
        for i in range(90):
            x, y = rng.uniform(40, 220), rng.uniform(40, 170); r = rng.uniform(10, 26)
            c = [(120, 160, 90), (90, 130, 80), (170, 190, 120), (200, 210, 190)][i % 4]
            d.ellipse(S(x - r, y - r, x + r, y + r), fill=c + (230,))
        for i in range(60):
            x, y = rng.uniform(40, 220), rng.uniform(30, 170); a = rng.uniform(0, 6.28)
            d.line(S(x, y, x + 18 * math.cos(a), y + 18 * math.sin(a)), fill=(230, 240, 220, 200), width=2 * sc)
        return _done(im.filter(ImageFilter.GaussianBlur(1.5 * sc)), w, h)
    return gcache("mould", mk)


def spatula_el():
    def mk():
        w, h, sc = 120, 420, 2; cv = _Cv(w, h, sc)
        hm = cv.mask(lambda d, S: d.rounded_rectangle(S(46, 10, 74, 220), 12 * sc, fill=255))
        mat_put(cv, hm, (150, 100, 60), (80, 50, 30), None, "satin", 4, 0.6)
        bm = cv.mask(lambda d, S: d.rounded_rectangle(S(20, 200, 100, 410), 18 * sc, fill=255))
        mat_put(cv, bm, (200, 206, 216), (110, 116, 130), (255, 255, 255), "gloss", 4, 0.4)
        return cv.done()
    return gcache("spatula", mk)


def sugar_xtal(f, x, y, s, t, op=1.0):
    """tiny white cube-ish sugar crystal that sparkles."""
    r = int(14 * s)
    pts = np.array([[x, y - r], [x + r, y], [x, y + r], [x - r, y]], np.int32)
    cv2.fillPoly(f, [pts], C((250, 250, 255)), cv2.LINE_AA); cv2.polylines(f, [pts], True, C((150, 170, 200)), 2, cv2.LINE_AA)
    if (t * 3 + x * 0.01) % 1 < 0.2: cv2.line(f, (int(x - r * 1.6), int(y)), (int(x + r * 1.6), int(y)), C(WHITE), 2, cv2.LINE_AA)


