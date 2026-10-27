# ================= reusable prop library from ep 13 (onions) (why onions make you cry): onion bulb (+ face), cut onion half with rings, chef knife (sharp /
# dull) + knife_at (pivot at the grip), cutting board, kitchen wall tiles, onion cell with two "rooms" (wall breaks), cell
# grid (onion skin seen under a microscope), sulfur molecule, enzyme pac-men (1 = snipper, 2 = gas maker), wobbly acid blob,
# tear-factor gas ghost, tear drop, tear streams, droplet spray (slow-mo capable), nerve endings, bug, germ, DNA helix with a
# gene, light switch, frying pan with onion rings, slow-motion camera UI, chain icons =================
SCHEMES["kitchen"] = ((255, 200, 110), (255, 236, 186), (236, 176, 96), (0.75, 0.5, 0.2))
SCHEMES["onion"] = ((92, 24, 88), (196, 104, 186), (84, 20, 80), (0.45, 0.12, 0.42))
SCHEMES["gas"] = ((26, 70, 16), (132, 196, 52), (24, 64, 14), (0.15, 0.4, 0.08))
SCHEMES["tear"] = ((12, 92, 150), (80, 196, 236), (12, 84, 140), (0.08, 0.36, 0.6))
ONI = (232, 176, 96); ONI_D = (176, 104, 44); RING = (252, 246, 226); RING_D = (226, 206, 170)
SULF = (255, 218, 40); SULF_D = (214, 160, 10); ENZ1 = (60, 150, 255); ENZ1_D = (24, 86, 200); ENZ2 = (255, 120, 40); ENZ2_D = (210, 70, 14)
ACID = (176, 92, 236); ACID_D = (110, 40, 170); GAS = (150, 230, 90); GAS_D = (70, 160, 40); TEAR = (120, 200, 255); TEAR_D = (40, 130, 220)
CELLW = (150, 190, 70); CELLF = (236, 248, 214)


# ---------------- onion bulb ----------------
def _onion_shape(m, S):
    P = []
    for i in range(61):
        a = math.pi * 2 * i / 60
        r = 1.0 + 0.0 * a
        x = 150 + 128 * math.sin(a) * (1 - 0.25 * max(0, -math.cos(a)) ** 3)
        y = 210 - 118 * math.cos(a) - 70 * max(0, math.cos(a)) ** 6
        P.append((x, y))
    m.polygon([(x * 2, y * 2) for x, y in P], fill=255)


def onion_el(face=False, mood="n", look=(0, 0), red=False):
    def mk():
        w, h, sc = 300, 360, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        top, bot = ((220, 120, 190), (140, 50, 120)) if red else ((246, 196, 120), ONI_D)
        _outline(im, lambda m: _onion_shape(m, S), 11)
        shape_grad(im, lambda m: _onion_shape(m, S), top, bot)
        mk_ = Image.new("L", im.size, 0); _onion_shape(ImageDraw.Draw(mk_), S)
        def stripes(q):
            for k in (-0.75, -0.42, -0.12, 0.18, 0.5, 0.8):
                q.arc(S(150 - 260 * abs(k) * 0.6 + 0, 40, 150 + 260 * abs(k) * 0.6, 340) if k else S(140, 40, 160, 340), 0, 360,
                      fill=(150, 80, 30, 70) if not red else (110, 30, 90, 70), width=3 * sc)
        _masked(im, mk_, stripes)
        _ov(im, lambda q: q.ellipse(S(76, 150, 130, 230), fill=(255, 255, 255, 80)))
        # dry tip + roots
        d.polygon(S(140, 40, 150, 2, 162, 40), fill=(200, 140, 70, 255), outline=INK + (255,))
        for k in range(-3, 4): d.line(S(150 + 9 * k, 326, 150 + 16 * k, 352), fill=(200, 170, 120, 255), width=3 * sc)
        if face:
            _eyes(d, S, sc, [(116, 200), (186, 200)], 18, look, sly=(mood == "sly"), happy=(mood == "happy"))
            if mood == "sly":
                d.arc(S(120, 222, 182, 262), 15, 165, fill=INK + (255,), width=5 * sc)
                d.line(S(94, 168, 136, 182), fill=INK + (255,), width=6 * sc); d.line(S(208, 168, 166, 182), fill=INK + (255,), width=6 * sc)
            elif mood == "sad": d.arc(S(128, 240, 172, 266), 200, 340, fill=INK + (255,), width=5 * sc)
            elif mood == "wow": d.ellipse(S(138, 232, 162, 262), fill=(60, 16, 20, 255))
            else: d.arc(S(124, 226, 176, 258), 20, 160, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("onion", face, mood, look, red), mk)


def onion_half_el(w_=340, rings=7):
    """the cut face of an onion half (rings), seen straight on."""
    def mk():
        w, h, sc = w_ + 20, int(w_ * 0.82) + 20, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        cx, cy, rx, ry = w / 2, h / 2 + 8, w_ / 2, w_ * 0.82 / 2 - 4
        d.ellipse(S(cx - rx - 6, cy - ry - 6, cx + rx + 6, cy + ry + 6), fill=INK + (255,))
        d.ellipse(S(cx - rx, cy - ry, cx + rx, cy + ry), fill=ONI_D + (255,))
        for i in range(rings):
            k = 1 - (i + 0.6) / (rings + 0.6); col = RING if i % 2 == 0 else (246, 236, 206)
            d.ellipse(S(cx - rx * k, cy - ry * k + 10 * (1 - k), cx + rx * k, cy + ry * k), fill=col + (255,), outline=RING_D + (255,), width=3 * sc)
        _ov(im, lambda q: q.ellipse(S(cx - rx * 0.6, cy - ry * 0.7, cx - rx * 0.1, cy - ry * 0.35), fill=(255, 255, 255, 90)))
        return _done(im, w, h)
    return gcache(("ohalf", w_, rings), mk)


# ---------------- chef knife (handle left, blade right, edge down); knife_at pivots at the grip ----------------
KN_W, KN_H, KN_GRIP = 560, 120, 70


def knife_el(dull=False):
    def mk():
        w, h, sc = KN_W, KN_H, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        blade = lambda m: m.polygon(S(150, 28, 470, 30, 548, 52, 520, 96, 150, 96), fill=255)
        _outline(im, blade, 9)
        shape_grad(im, blade, (250, 252, 255) if not dull else (196, 200, 208), (170, 178, 196) if not dull else (130, 134, 146))
        if not dull:
            d.line(S(156, 92, 520, 92), fill=(255, 255, 255, 255), width=4 * sc)
            _ov(im, lambda q: q.polygon(S(170, 40, 440, 40, 420, 56, 170, 56), fill=(255, 255, 255, 120)))
        else:
            for x in range(170, 510, 34): d.polygon(S(x, 96, x + 10, 86, x + 20, 96), fill=(110, 112, 120, 255))
            d.line(S(156, 92, 516, 92), fill=(120, 120, 130, 255), width=4 * sc)
        handle = lambda m: m.rounded_rectangle(S(12, 40, 158, 84), 18 * sc, fill=255)
        _outline(im, handle, 9)
        shape_grad(im, handle, (70, 50, 40), (30, 20, 16))
        for x in (50, 100): d.ellipse(S(x - 7, 55, x + 7, 69), fill=(200, 206, 220, 255))
        return _done(im, w, h)
    return gcache(("knife", dull), mk)


def knife_at(f, gx, gy, ang, s=1.0, dull=False, op=1.0):
    """draw the knife so its grip sits at (gx, gy); ang = degrees CCW (0 = blade pointing right, edge down)."""
    dx = (KN_W / 2 - KN_GRIP) * s; dy = (KN_H / 2 - 62) * s; a = math.radians(ang)
    cx = gx + dx * math.cos(a) + dy * math.sin(a); cy = gy - dx * math.sin(a) + dy * math.cos(a)
    rot_comp(f, scale_el(knife_el(dull), s), cx, cy, ang, 1.0, op, 0.25)


def knife_tip(gx, gy, ang, s=1.0):
    a = math.radians(ang); L = (548 - KN_GRIP) * s
    return gx + L * math.cos(a), gy - L * math.sin(a)


def board_el(w_=640):
    def mk():
        w, h, sc = w_, 120, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        top = lambda m: m.rounded_rectangle(S(6, 10, w - 6, 70), 26 * sc, fill=255)
        side = lambda m: m.rounded_rectangle(S(6, 30, w - 6, 110), 26 * sc, fill=255)
        _outline(im, lambda m: (top(m), side(m)), 9)
        shape_grad(im, side, (190, 120, 60), (140, 82, 36)); shape_grad(im, top, (236, 180, 112), (214, 150, 84))
        for k in range(5): d.arc(S(40 + 110 * k, 20, 150 + 110 * k, 64), 200, 340, fill=(190, 130, 70, 160), width=2 * sc)
        return _done(im, w, h)
    return gcache(("board", w_), mk)


def tiles(f, y0=250, y1=1100, col=(255, 255, 255), op=0.18, size=120):
    """kitchen wall tiles (decoration only, faint)."""
    g = f.copy()
    for y in range(y0, y1, size): cv2.line(g, (0, y), (W, y), C(col), 4, cv2.LINE_AA)
    for x in range(0, W, size): cv2.line(g, (x, y0), (x, y1), C(col), 4, cv2.LINE_AA)
    f[:] = f * (1 - op) + g * op


# ---------------- onion cell with two rooms ----------------
def onion_cell(f, x, y, w, h, t=0.0, broken=0.0, wall=True, labels=False, t_lab=0.0):
    """a big cut-away cell: thick cell wall, an inner wall that splits it into ROOM 1 (left) and ROOM 2 (right).
    broken 0..1 cracks the outer wall and dissolves the inner wall."""
    x0, y0, x1, y1 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
    jit = (lambda k: 7 * broken * math.sin(t * 40 + k)) if broken > 0 else (lambda k: 0)
    cv2.rectangle(f, (x0 - 16, y0 - 16), (x1 + 16, y1 + 16), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0 - 8, y0 - 8), (x1 + 8, y1 + 8), C(CELLW), -1, cv2.LINE_AA)
    g = f.copy(); cv2.rectangle(g, (x0, y0), (x1, y1), C(CELLF), -1, cv2.LINE_AA)
    cv2.rectangle(g, (x0, y0), (x1, y0 + 26), C((255, 255, 255)), -1, cv2.LINE_AA); f[:] = g
    if broken > 0:   # cracks + gaps in the outer wall
        for (cx_, cy_, ang) in ((x0, y0 + h * 0.3, 0), (x1, y0 + h * 0.65, 180), (x0 + w * 0.6, y0, 90), (x0 + w * 0.3, y1, 270)):
            L = 70 * clamp(broken * 1.5); a = math.radians(ang)
            P = [(cx_, cy_)]
            for k in range(4): P.append((P[-1][0] + L / 4 * math.cos(a) + 14 * (-1) ** k * math.sin(a), P[-1][1] + L / 4 * math.sin(a) + 14 * (-1) ** k * math.cos(a)))
            cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), 8, cv2.LINE_AA)
    if wall:
        k = clamp(broken * 1.4)
        nseg = 7
        for i in range(nseg):
            if k > 0 and (i % 2 == 1 or k > 0.75): continue
            sy0 = y0 + i * h / nseg; sy1 = y0 + (i + 1) * h / nseg
            cv2.line(f, (int(x + jit(i)), int(sy0 + 4)), (int(x + jit(i + 1)), int(sy1 - 4)), C(INK), 22, cv2.LINE_AA)
            cv2.line(f, (int(x + jit(i)), int(sy0 + 4)), (int(x + jit(i + 1)), int(sy1 - 4)), C((200, 170, 120)), 12, cv2.LINE_AA)
    if labels and t >= t_lab and broken < 0.3:
        comp(f, chip("ROOM 1", INK, WHITE, 26), x - w / 4, y0 + 52, op=clamp((t - t_lab) / 0.25))
        comp(f, chip("ROOM 2", INK, WHITE, 26), x + w / 4, y0 + 52, op=clamp((t - t_lab - 0.2) / 0.25))


def cell_grid(f, x, y, w, h, cw=150, ch=70, t=0.0, hi=None):
    """onion skin under a microscope: long brick-like cells (scale cue)."""
    x0, y0 = x - w / 2, y - h / 2
    g = f.copy(); cv2.rectangle(g, (int(x0), int(y0)), (int(x0 + w), int(y0 + h)), C(CELLF), -1)
    r = 0
    yy = y0
    while yy < y0 + h:
        off = (cw / 2) * (r % 2); xx = x0 - off
        while xx < x0 + w:
            a, b = (int(max(x0, xx + 4)), int(yy + 4)), (int(min(x0 + w, xx + cw - 4)), int(min(y0 + h, yy + ch - 4)))
            if b[0] > a[0] + 6:
                cv2.rectangle(g, a, b, C(CELLW), 6, cv2.LINE_AA)
                cv2.circle(g, (int((a[0] + b[0]) / 2), int((a[1] + b[1]) / 2)), 9, C((170, 200, 120)), -1, cv2.LINE_AA)
            xx += cw
        yy += ch; r += 1
    f[:] = g
    if hi is not None:
        hx, hy = hi; cv2.rectangle(f, (int(hx - cw / 2), int(hy - ch / 2)), (int(hx + cw / 2), int(hy + ch / 2)), C(YEL_), 8, cv2.LINE_AA)


# ---------------- molecule characters ----------------
def sulfur_el(mood="happy", look=(0, 0)):
    def mk():
        w, h, sc = 220, 200, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        balls = ((110, 108, 70), (46, 70, 34), (176, 64, 32), (60, 160, 30))
        allm = lambda m: [m.ellipse(S(bx - r - 4, by - r - 4, bx + r + 4, by + r + 4), fill=255) for bx, by, r in balls]
        _outline(im, allm, 9)
        for i, (bx, by, r) in enumerate(balls):
            top, bot = (SULF, SULF_D) if i == 0 else ((250, 250, 240), (196, 196, 186))
            shape_grad(im, lambda m, bx=bx, by=by, r=r: m.ellipse(S(bx - r, by - r, bx + r, by + r), fill=255), top, bot)
            _ov(im, lambda q, bx=bx, by=by, r=r: q.ellipse(S(bx - r * 0.6, by - r * 0.7, bx - r * 0.05, by - r * 0.25), fill=(255, 255, 255, 120)))
        d.text((110 * sc, 80 * sc), "S", font=font(F_BLACK, 34 * sc), fill=(150, 100, 0, 255), anchor="mm")
        _eyes(d, S, sc, [(90, 112), (130, 112)], 13, look, happy=(mood == "happy"), sly=(mood == "sly"))
        if mood == "sleep":
            for ex in (90, 130): d.line(S(ex - 11, 114, ex + 11, 114), fill=INK + (255,), width=5 * sc)
        d.arc(S(96, 124, 124, 146), 20, 160, fill=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("sulf", mood, look), mk)


def enz_el(kind=1, open_=0.5, mood="n", look=(0, 0)):
    """enzyme pac-man: kind 1 = the snipper (blue, scissor teeth), kind 2 = the gas maker (orange)."""
    open_ = round(clamp(open_) * 8) / 8
    def mk():
        w, h, sc = 240, 220, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        col, dk = (ENZ1, ENZ1_D) if kind == 1 else (ENZ2, ENZ2_D)
        a = 8 + 38 * open_
        body = lambda m: m.pieslice(S(20, 16, 220, 216), a, 360 - a, fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, tuple(min(255, c + 40) for c in col), dk)
        _ov(im, lambda q: q.ellipse(S(52, 40, 120, 90), fill=(255, 255, 255, 90)))
        # teeth along the mouth
        for k in range(3):
            for sg in (-1, 1):
                ang = math.radians(sg * a); r0 = 50 + 26 * k
                px, py = 120 + r0 * math.cos(ang), 116 + r0 * math.sin(ang)
                d.polygon(S(px - 7, py, px + 7, py, px, py - sg * 14), fill=(255, 255, 255, 255))
        if mood == "sleep":
            d.line(S(96, 74, 124, 74), fill=INK + (255,), width=6 * sc)
        elif mood == "dizzy":
            for k in (-1, 1): d.line(S(100 + 10 * k, 64, 120 - 10 * k, 84), fill=INK + (255,), width=6 * sc)
        else:
            _eyes(d, S, sc, [(112, 74)], 17, look, sly=(mood == "sly"), happy=(mood == "happy"))
        if mood in ("n", "sly", "happy"): d.line(S(92, 46, 132, 54) if mood != "sly" else S(92, 52, 134, 60), fill=INK + (255,), width=6 * sc)
        d.ellipse(S(30, 150, 76, 196), fill=WHITE + (255,), outline=INK + (255,), width=4 * sc)
        d.text((53 * sc, 173 * sc), str(kind), font=font(F_BLACK, 32 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("enz", kind, open_, mood, look), mk)


def chomp(t, rate=0.28): return 0.5 + 0.5 * math.cos(2 * math.pi * t / rate)


def acid(f, x, y, s, t, wob=1.0, mood="wow", op=1.0):
    """the unstable acid: a purple jelly blob that wobbles (wob 0..1+) - drawn live."""
    g = f if op >= 0.999 else f.copy()
    P = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        r = 92 * s * (1 + 0.08 * wob * math.sin(3 * a + t * 13) + 0.05 * wob * math.sin(5 * a - t * 17))
        P.append((x + r * math.cos(a) * 1.08, y + r * math.sin(a) * 0.92))
    P = np.array(P, np.int32)
    cv2.fillPoly(g, [P], C(INK), cv2.LINE_AA)
    P2 = (np.array(P, np.float32) - [x, y]) * 0.9 + [x, y]
    cv2.fillPoly(g, [P2.astype(np.int32)], C(ACID), cv2.LINE_AA)
    cv2.ellipse(g, (int(x - 30 * s), int(y - 40 * s)), (int(26 * s), int(14 * s)), -20, 0, 360, C((236, 200, 255)), -1, cv2.LINE_AA)
    jx = 3 * wob * math.sin(t * 31)
    for ex in (-26, 26):
        cv2.circle(g, (int(x + ex * s + jx), int(y - 4 * s)), int(15 * s), C(WHITE), -1, cv2.LINE_AA)
        cv2.circle(g, (int(x + ex * s + jx), int(y - 4 * s)), int(15 * s), C(INK), max(1, int(4 * s)), cv2.LINE_AA)
        cv2.circle(g, (int(x + ex * s + jx + 3 * math.sin(t * 9)), int(y - 2 * s)), int(6 * s), C(INK), -1, cv2.LINE_AA)
    cv2.ellipse(g, (int(x + jx), int(y + 34 * s)), (int(14 * s), int(10 * s)), 0, 0, 360, C((60, 16, 20)), -1, cv2.LINE_AA)
    if op < 0.999: f[:] = f * (1 - op) + g * op


def gas_el(mood="sly", look=(0, 0)):
    """the tear factor: a green gas ghost with a wavy tail."""
    def mk():
        w, h, sc = 260, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            m.ellipse(S(30, 20, 230, 220), fill=255)
            P = [(30, 120), (230, 120)]
            for i in range(9):
                xx = 230 - i * 25; P.append((xx, 250 + (24 if i % 2 else 0) - (10 if i in (0, 8) else 0)))
            m.polygon(S(*[v for p in P for v in p]), fill=255)
            for bx, by, r in ((40, 110, 40), (220, 100, 44), (130, 30, 46)): m.ellipse(S(bx - r, by - r, bx + r, by + r), fill=255)
        _outline(im, body, 11)
        shape_grad(im, body, (200, 255, 150), GAS_D)
        _ov(im, lambda q: q.ellipse(S(70, 50, 140, 100), fill=(255, 255, 255, 110)))
        _eyes(d, S, sc, [(100, 128), (162, 128)], 19, look, sly=(mood == "sly"), happy=(mood == "happy"))
        if mood == "sly":
            d.line(S(76, 98, 118, 110), fill=INK + (255,), width=7 * sc); d.line(S(186, 98, 144, 110), fill=INK + (255,), width=7 * sc)
            d.arc(S(102, 150, 162, 194), 15, 165, fill=INK + (255,), width=6 * sc)
        elif mood == "sad": d.arc(S(110, 172, 154, 196), 200, 340, fill=INK + (255,), width=6 * sc)
        else: d.ellipse(S(120, 160, 144, 190), fill=(60, 16, 20, 255))
        return _done(im, w, h)
    return gcache(("gas", mood, look), mk)


def gas(f, x, y, s, t, mood="sly", op=1.0, look=(0, 0)):
    rot_comp(f, scale_el(gas_el(mood, look), s), x + 6 * math.sin(t * 3.1), y + 10 * math.sin(t * 2.3), 5 * math.sin(t * 2.7), 1.0, op, 0.0)


def wisps(f, x, y, t, t0=0.0, n=4, h_=420, s=1.0, op=0.75, seed=2):
    """thin green gas wisps rising from a cut (continuous)."""
    if t < t0: return
    rng = np.random.default_rng(seed)
    g = f.copy()
    for i in range(n):
        ph = ((t - t0) * 0.6 + i / n) % 1.0; xo = rng.uniform(-60, 60) * s
        P = [(x + xo + 30 * s * math.sin(ph * 9 + i + k * 0.7 + t * 2), y - h_ * ph * s - k * 22 * s) for k in range(8)]
        cv2.polylines(g, [np.array(P, np.int32)], False, C(GAS), max(2, int(16 * s * (1 - ph))), cv2.LINE_AA)
    a = op * clamp((t - t0) / 0.4); f[:] = f * (1 - a) + g * a


def drop_el(col=TEAR):
    def mk():
        w, h, sc = 120, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: (m.ellipse(S(16, 50, 104, 142), fill=255), m.polygon(S(22, 82, 60, 6, 98, 82), fill=255))
        _outline(im, body, 9)
        shape_grad(im, body, tuple(min(255, c + 60) for c in col), tuple(int(c * 0.7) for c in col))
        _ov(im, lambda q: q.ellipse(S(36, 74, 58, 110), fill=(255, 255, 255, 170)))
        return _done(im, w, h)
    return gcache(("drop", col), mk)


def tears(f, x, y, t, t0, amt=1.0, side=1, power=1.0, n=14, s=1.0):
    """cartoon tear fountain: drops arc out of an eye corner at (x, y). side = -1 left, +1 right."""
    if t < t0 or amt <= 0: return
    for i in range(n):
        ph = ((t - t0) * 1.6 + i / n) % 1.0
        if (t - t0) * 1.6 < i / n: continue
        vx = side * (260 + 60 * math.sin(i * 1.7)) * power; vy = -(320 + 50 * math.cos(i)) * power
        tt = ph * 0.9
        px, py = x + vx * tt * s, y + (vy * tt + 900 * tt * tt) * s
        r = (13 + 5 * math.sin(i)) * s * amt
        cv2.circle(f, (int(px), int(py)), int(r + 3), C(TEAR_D), -1, cv2.LINE_AA)
        cv2.circle(f, (int(px), int(py)), int(r), C(TEAR), -1, cv2.LINE_AA)
        cv2.circle(f, (int(px - r * 0.3), int(py - r * 0.3)), max(1, int(r * 0.3)), C(WHITE), -1, cv2.LINE_AA)


def tear_streams(f, hx, hy, s, t, t0, amt=1.0, power=1.0):
    """both eyes of Chubby (head centre hx, hy, scale s) gush tears."""
    for side in (-1, 1):
        ex, ey = hx + side * 46 * s, hy + 4 * s
        cv2.ellipse(f, (int(ex), int(ey + 40 * s)), (int(10 * s), int(44 * s * amt)), 0, 0, 360, C(TEAR), -1, cv2.LINE_AA)
        tears(f, ex, ey, t, t0, amt, side, power, 12, s)


def droplets(f, x, y, t, t0, n=40, spd=900.0, spread=70.0, up=90.0, slow=1.0, seed=5, col=(230, 250, 200), g_=1600.0, r0=9):
    """juice droplet spray from a cut at (x, y): each drop launched at t0 with a random speed/angle, falls with gravity.
    slow < 1 = slow motion (the high-speed-camera look). Returns the highest drop's y (for 'how high' cues)."""
    if t < t0: return None
    rng = np.random.default_rng(seed); q = (t - t0) * slow; top = None
    for i in range(n):
        a = math.radians(up + rng.uniform(-spread, spread)); v = spd * rng.uniform(0.35, 1.0); dl = rng.uniform(0, 0.12)
        qq = q - dl
        if qq < 0: continue
        px = x + v * math.cos(a) * qq; py = y - v * math.sin(a) * qq + 0.5 * g_ * qq * qq
        if py > y + 60: continue
        r = r0 * rng.uniform(0.5, 1.3)
        vx_, vy_ = v * math.cos(a), -v * math.sin(a) + g_ * qq; sp = math.hypot(vx_, vy_) + 1e-6
        tl = min(40, sp * 0.02 / max(0.05, slow) * 0.15)
        cv2.line(f, (int(px - vx_ / sp * tl), int(py - vy_ / sp * tl)), (int(px), int(py)), C(col), max(1, int(r * 1.3)), cv2.LINE_AA)
        cv2.circle(f, (int(px), int(py)), int(r), C(col), -1, cv2.LINE_AA)
        cv2.circle(f, (int(px - r * 0.3), int(py - r * 0.3)), max(1, int(r * 0.35)), C(WHITE), -1, cv2.LINE_AA)
        top = py if top is None else min(top, py)
    return top


def nerve_endings(f, cx, cy, r, t, lit=0.0, seed=4):
    """little branching nerve endings (yellow) inside a circle; lit 0..1 makes them glow + spark."""
    rng = np.random.default_rng(seed)
    col = tuple(int(a + (b - a) * clamp(lit)) for a, b in zip((230, 190, 90), (255, 250, 150)))
    for i in range(7):
        x0 = cx - r * 0.75 + i * r * 0.25; y0 = cy + r * 0.85
        P = [(x0, y0)]
        for k in range(4): P.append((P[-1][0] + rng.uniform(-30, 30), P[-1][1] - r * 0.33))
        cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), 14, cv2.LINE_AA)
        cv2.polylines(f, [np.array(P, np.int32)], False, C(col), 8, cv2.LINE_AA)
        ex, ey = P[-1]
        for b in (-1, 1): cv2.line(f, (int(ex), int(ey)), (int(ex + b * 24), int(ey - 22)), C(col), 6, cv2.LINE_AA)
        if lit > 0.2:
            glow(f, ex, ey, 30, (255, 240, 120), 0.4 * lit * (0.6 + 0.4 * math.sin(t * 20 + i)))
            sparkles(f, ex, ey - 10, t, t - ((t * 3 + i * 0.3) % 1.0) * 0.6, 4, 40, (255, 250, 170), i, 0.6)


# ---------------- bug, germ ----------------
def bug_el(bite=False, scared=False):
    def mk():
        w, h, sc = 260, 200, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        for k in range(3):
            for sg in (-1, 1): d.line(S(100 + 30 * k, 110, 90 + 36 * k, 110 + sg * 70), fill=INK + (255,), width=6 * sc)
        body = lambda m: (m.ellipse(S(60, 50, 210, 170), fill=255), m.ellipse(S(180, 70, 250, 140), fill=255))
        _outline(im, body, 9)
        shape_grad(im, lambda m: m.ellipse(S(60, 50, 210, 170), fill=255), (110, 200, 90), (40, 120, 40))
        shape_grad(im, lambda m: m.ellipse(S(180, 70, 250, 140), fill=255), (90, 90, 100), (40, 40, 48))
        d.line(S(135, 54, 135, 166), fill=INK + (255,), width=4 * sc)
        for bx, by in ((100, 90), (160, 130), (110, 140)): d.ellipse(S(bx - 10, by - 10, bx + 10, by + 10), fill=(30, 90, 30, 255))
        _eyes(d, S, sc, [(214, 96), (236, 96)], 9, (0.6, 0), happy=False)
        if bite: d.pieslice(S(222, 104, 256, 138), 300, 60, fill=(60, 16, 20, 255))
        if scared:
            for k in range(3): d.line(S(40, 70 + 30 * k, 10, 66 + 30 * k), fill=INK + (255,), width=4 * sc)
        for sg in (-1, 1): d.line(S(236, 80, 250 + 10, 50 + sg * 10), fill=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("bug", bite, scared), mk)


def germ_el(mood="sly"):
    def mk():
        w, h, sc = 220, 220, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        for k in range(10):
            a = 2 * math.pi * k / 10; d.line(S(110, 110, 110 + 98 * math.cos(a), 110 + 98 * math.sin(a)), fill=INK + (255,), width=6 * sc)
            d.ellipse(S(110 + 98 * math.cos(a) - 9, 110 + 98 * math.sin(a) - 9, 110 + 98 * math.cos(a) + 9, 110 + 98 * math.sin(a) + 9), fill=(180, 90, 200, 255), outline=INK + (255,))
        body = lambda m: m.ellipse(S(40, 40, 180, 180), fill=255)
        _outline(im, body, 9)
        shape_grad(im, body, (210, 140, 230), (130, 60, 160))
        _eyes(d, S, sc, [(90, 104), (132, 104)], 14, (0, 0), sly=(mood == "sly"))
        if mood == "sad": d.arc(S(96, 134, 126, 152), 200, 340, fill=INK + (255,), width=5 * sc)
        else: d.arc(S(92, 122, 130, 148), 20, 160, fill=INK + (255,), width=5 * sc)
        return _done(im, w, h)
    return gcache(("germ", mood), mk)


# ---------------- DNA helix with a gene + light switch ----------------
def helix(f, x, y, h_, t, gene=(0.4, 0.62), gene_col=ENZ2, off=0.0, w_=150):
    """vertical DNA ladder centred on (x, y); the 'gene' span (0..1) is coloured; off 0..1 greys it out."""
    y0 = y - h_ / 2; nn = 60
    P1, P2 = [], []
    for i in range(nn + 1):
        k = i / nn; yy = y0 + k * h_; ph = k * 4 * math.pi + t * 1.2
        P1.append((x + w_ / 2 * math.sin(ph), yy)); P2.append((x - w_ / 2 * math.sin(ph), yy))
    for i in range(0, nn + 1, 3):
        k = i / nn; ing = gene[0] <= k <= gene[1]
        col = gene_col if ing else (120, 200, 255)
        if ing and off > 0: col = tuple(int(c + (150 - c) * clamp(off)) for c in gene_col)
        cv2.line(f, (int(P1[i][0]), int(P1[i][1])), (int(P2[i][0]), int(P2[i][1])), C(INK), 14, cv2.LINE_AA)
        cv2.line(f, (int(P1[i][0]), int(P1[i][1])), (int(P2[i][0]), int(P2[i][1])), C(col), 8, cv2.LINE_AA)
    for P, col in ((P1, (60, 120, 230)), (P2, (236, 72, 140))):
        cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), 20, cv2.LINE_AA)
        cv2.polylines(f, [np.array(P, np.int32)], False, C(col), 12, cv2.LINE_AA)


def switch_el(on=True):
    def mk():
        w, h, sc = 220, 320, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        plate = lambda m: m.rounded_rectangle(S(10, 10, 210, 310), 30 * sc, fill=255)
        _outline(im, plate, 9); shape_grad(im, plate, (255, 255, 255), (214, 218, 228))
        d.rounded_rectangle(S(66, 70, 154, 250), 16 * sc, fill=(60, 60, 70, 255))
        if on: d.rounded_rectangle(S(74, 78, 146, 160), 12 * sc, fill=(120, 230, 120, 255), outline=INK + (255,), width=4 * sc)
        else: d.rounded_rectangle(S(74, 160, 146, 242), 12 * sc, fill=(240, 90, 80, 255), outline=INK + (255,), width=4 * sc)
        d.text((110 * sc, 40 * sc), "ON", font=font(F_BLACK, 26 * sc), fill=(60, 60, 70, 255), anchor="mm")
        d.text((110 * sc, 280 * sc), "OFF", font=font(F_BLACK, 26 * sc), fill=(60, 60, 70, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("switch", on), mk)


# ---------------- frying pan with onion rings ----------------
def pan_el():
    def mk():
        w, h, sc = 700, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(470, 96, 690, 132), 16 * sc, fill=INK + (255,)); d.rounded_rectangle(S(480, 102, 684, 126), 12 * sc, fill=(60, 40, 30, 255))
        body = lambda m: m.ellipse(S(10, 40, 500, 230), fill=255)
        _outline(im, body, 11); shape_grad(im, body, (90, 96, 110), (40, 42, 50))
        d.ellipse(S(40, 56, 470, 200), fill=(56, 58, 66, 255))
        rng = np.random.default_rng(3)
        for i in range(9):
            cx, cy = 90 + i * 42 + rng.uniform(-10, 10), 128 + rng.uniform(-36, 36)
            d.ellipse(S(cx - 34, cy - 20, cx + 34, cy + 20), outline=(150, 90, 30, 255), width=12 * sc)
            d.ellipse(S(cx - 34, cy - 20, cx + 34, cy + 20), outline=(236, 176, 80, 255), width=7 * sc)
        return _done(im, w, h)
    return gcache("pan", mk)


# ---------------- slow-motion camera UI ----------------
def slowmo_ui(f, t, label="SLOW MOTION", y0=300, y1=1440, x0=90, x1=990, rate="x 0.01"):
    L = 70
    for (cx, cy, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        cv2.line(f, (cx, cy), (cx + sx * L, cy), C(WHITE), 8, cv2.LINE_AA); cv2.line(f, (cx, cy), (cx, cy + sy * L), C(WHITE), 8, cv2.LINE_AA)
    if int(t * 2) % 2 == 0: cv2.circle(f, (x0 + 50, y0 + 50), 16, C((255, 40, 40)), -1, cv2.LINE_AA)
    comp(f, chip("REC", (0, 0, 0), WHITE, 22), x0 + 120, y0 + 50)
    comp(f, chip(label, YEL_, INK, 26), (x0 + x1) / 2 + 150, y0 + 50)
    ms = int((t * 1000 * 0.05) % 100000)
    comp(f, chip(f"00:00:{ms // 1000:02d}.{ms % 1000:03d}", (0, 0, 0), WHITE, 22), (x0 + x1) / 2, y1 - 40)


def mix_icon_el():
    """two little blobs (yellow + blue) touching = MIX (chain icon)."""
    def mk():
        w, h, sc = 200, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        for (bx, col, dk) in ((70, SULF, SULF_D), (130, ENZ1, ENZ1_D)):
            m = lambda q, bx=bx: q.ellipse(S(bx - 54, 26, bx + 54, 134), fill=255)
            _outline(im, m, 9); shape_grad(im, m, col, dk)
        d.text((100 * sc, 80 * sc), "+", font=font(F_BLACK, 60 * sc), fill=WHITE + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache("mixicon", mk)


def acid_icon_el():
    def mk():
        w, h, sc = 200, 180, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: m.ellipse(S(16, 20, 184, 166), fill=255)
        _outline(im, body, 9); shape_grad(im, body, (210, 150, 255), ACID_D)
        _eyes(d, S, sc, [(74, 86), (126, 86)], 15, (0, 0))
        d.ellipse(S(88, 112, 112, 134), fill=(60, 16, 20, 255))
        return _done(im, w, h)
    return gcache("acidicon", mk)


def sting_eye_el():
    """an eye with a little red spark = 'nerves feel the sting' (chain icon)."""
    def mk():
        w, h, sc = 220, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        alm = lambda m: m.polygon(S(*[v for i in range(41) for v in (14 + i * 4.8, 80 - 60 * math.sin(math.pi * i / 40))] +
                                    [v for i in range(41) for v in (206 - i * 4.8, 80 + 52 * math.sin(math.pi * i / 40))]), fill=255)
        _outline(im, alm, 9); shape_grad(im, alm, (255, 255, 255), (220, 222, 230))
        d.ellipse(S(80, 44, 140, 116), fill=(60, 130, 200, 255)); d.ellipse(S(98, 62, 122, 98), fill=INK + (255,))
        for k in range(6):
            a = k * math.pi / 3; d.line(S(186 + 10 * math.cos(a), 30 + 10 * math.sin(a), 186 + 26 * math.cos(a), 30 + 26 * math.sin(a)), fill=(255, 60, 40, 255), width=5 * sc)
        return _done(im, w, h)
    return gcache("stingeye", mk)


# ---------------- ep 13 scene helpers (Chubby chopping with IK, board + onion, Zzz, shield, tear gland, onion ring) ----------------
def chop_pose(t, t0, period=0.5, up=1140, down=1250, gx=560):
    """grip point for a vertical chop (fast down, slower up). returns (gx, gy, hit 0..1)."""
    if t < t0: return gx, up, 0.0
    ph = ((t - t0) % period) / period
    gy = up + (down - up) * (eo(ph / 0.35) if ph < 0.35 else 1 - eio((ph - 0.35) / 0.65))
    hit = math.exp(-((ph - 0.35) % 1.0) * 14) if ph >= 0.33 else 0.0
    return gx, gy, hit


def chopper(f, t, x=330, y=1470, s=1.0, period=0.5, t0=0.0, dull=False, ang=-6, gx=560, up=1140, down=1250, expr="happy", mouth=None,
            brow="up", look=(1, 0.4), la=(20, 10)):
    """Chubby holding a knife in his right hand (2-bone IK) and chopping. returns the hit strength (for squash/SFX)."""
    gx, gy, hit = chop_pose(t, t0, period, up, down, gx)
    sh = (x + 118 * s, y - 215 * s - 46 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, la=la, ra=(a1, a2), mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look)
    knife_at(f, gx, gy, ang, 0.7 * s, dull)
    if "grip_hand" in globals(): grip_hand(f, gx, gy, s)
    else: cv2.circle(f, (int(gx), int(gy)), int(19 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(gx), int(gy)), int(14 * s), C(CH_SKIN), -1, cv2.LINE_AA)
    return hit


def board_onion(f, t, x=760, y=1395, s=0.75, os_=0.7, face=False, mood="n", look=(0, 0)):
    comp(f, scale_el(board_el(), s), x - 40, y)
    oy = y - 30 - 126 * os_ / 0.7
    comp(f, scale_el(onion_el(face, mood, look), os_), x, oy)
    return x, oy


def zz(f, x, y, t, n=3, col=WHITE):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1.0
        comp(f, ed_el("", "Z", "", big_col=col, big_size=int(40 + 30 * ph)), x + 40 * ph + 10 * i, y - 160 * ph, op=math.sin(math.pi * ph))


def shield_el():
    def mk():
        w, h, sc = 220, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        sh = lambda m: m.polygon(S(20, 30, 110, 10, 200, 30, 196, 140, 110, 246, 24, 140), fill=255)
        _outline(im, sh, 11); shape_grad(im, sh, (120, 180, 255), (40, 90, 200))
        d.polygon(S(110, 40, 172, 56, 168, 140, 110, 214, 52, 140, 48, 56), outline=(255, 255, 255, 255), width=6 * sc)
        d.line(S(110, 60, 110, 190), fill=(255, 255, 255, 255), width=8 * sc); d.line(S(66, 110, 154, 110), fill=(255, 255, 255, 255), width=8 * sc)
        return _done(im, w, h)
    return gcache("shield", mk)


def gland(f, x, y, s, lit=0.0):
    cv2.ellipse(f, (int(x), int(y)), (int(46 * s), int(24 * s)), -18, 0, 360, C(INK), -1, cv2.LINE_AA)
    col = tuple(int(a + (b - a) * clamp(lit)) for a, b in zip((255, 160, 180), (120, 210, 255)))
    cv2.ellipse(f, (int(x), int(y)), (int(40 * s), int(18 * s)), -18, 0, 360, C(col), -1, cv2.LINE_AA)


def ring_el():
    def mk():
        w, h, sc = 200, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 10, 190, 150), outline=INK + (255,), width=34 * sc)
        d.ellipse(S(16, 16, 184, 144), outline=(236, 176, 80, 255), width=22 * sc)
        return _done(im, w, h)
    return gcache("oring", mk)
