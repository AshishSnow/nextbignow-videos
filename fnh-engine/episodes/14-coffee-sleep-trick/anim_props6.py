# ================= reusable prop library from ep 14 (coffee): coffee mug, energy battery (with a fake sticker), sleepy key
# (adenosine), fake key (caffeine bean), receptor lock, brain cell with locks on its surface, pile of sleepy keys, smile mask
# on a stick, bed + blanket + nightcap, bee, coffee + lemon flowers, sleep-hours bar, mini sun/moon icons =================
SCHEMES["cafe"] = ((96, 52, 28), (196, 128, 76), (88, 46, 24), (0.4, 0.22, 0.1))
SCHEMES["latte"] = ((236, 200, 160), (255, 236, 210), (226, 186, 142), (0.7, 0.55, 0.38))
SCHEMES["neuro"] = ((14, 30, 70), (40, 110, 170), (12, 28, 64), (0.1, 0.3, 0.5))
SCHEMES["dusk"] = ((40, 20, 80), (230, 110, 120), (60, 24, 90), (0.4, 0.2, 0.45))
SCHEMES["honey"] = ((240, 150, 10), (255, 214, 90), (232, 140, 6), (0.8, 0.5, 0.05))
CAF = (124, 72, 38); CAF_D = (78, 40, 18); CAF_L = (196, 136, 78)
ADE = (156, 110, 236); ADE_D = (92, 52, 176); ADE_L = (214, 196, 255)
LOCK = (40, 196, 180); LOCK_D = (10, 120, 116); NEU = (110, 226, 214); NEU_D = (24, 150, 150)
BEE = (255, 200, 30); BEE_D = (190, 130, 0)


# ---------------- big ceramic mug of coffee ----------------
def mug_el(col=(240, 80, 70), level=0.85, steam_=False):
    def mk():
        w, h, sc = 300, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m): m.rounded_rectangle(S(30, 50, 220, 280), 34 * sc, fill=255)
        def handle(m): m.ellipse(S(180, 100, 290, 230), fill=255)
        _outline(im, lambda m: (body(m), handle(m)), 13)
        d.ellipse(S(206, 128, 262, 202), fill=(0, 0, 0, 0))
        hm = Image.new("L", im.size, 0); hd = ImageDraw.Draw(hm); hd.ellipse(S(184, 104, 286, 226), fill=255); hd.ellipse(S(210, 132, 258, 198), fill=0)
        im.paste(Image.new("RGBA", im.size, tuple(int(c * 0.85) for c in col) + (255,)), (0, 0), hm)
        shape_grad(im, body, tuple(min(255, c + 40) for c in col), tuple(int(c * 0.7) for c in col))
        d.ellipse(S(36, 46, 214, 92), fill=INK + (255,))
        if level > 0: d.ellipse(S(44, 52, 206, 86), fill=CAF + (255,)); _ov(im, lambda q: q.ellipse(S(70, 58, 140, 72), fill=(255, 255, 255, 70)))
        else: d.ellipse(S(44, 52, 206, 86), fill=(250, 246, 240, 255))
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        _masked(im, bm, lambda q: q.rounded_rectangle(S(50, 110, 74, 250), 12 * sc, fill=(255, 255, 255, 110)))
        return _done(im, w, h)
    return gcache(("mug", col, level), mk)


# ---------------- energy battery (level 0..1); fake=True draws a peeling "100%" sticker over an empty battery ----------------
def battery_el(level=1.0, txt=None, col=None):
    level = round(clamp(level) * 20) / 20
    def mk():
        w, h, sc = 420, 210, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(8, 20, 370, 190), 30 * sc, fill=INK + (255,))
        d.rounded_rectangle(S(366, 70, 410, 140), 12 * sc, fill=INK + (255,))
        d.rounded_rectangle(S(24, 36, 354, 174), 20 * sc, fill=(245, 245, 250, 255))
        c = col or ((60, 210, 90) if level > 0.5 else ((255, 190, 30) if level > 0.2 else (240, 50, 50)))
        n_ = int(round(level * 5))
        for i in range(n_):
            x = 38 + i * 63; d.rounded_rectangle(S(x, 50, x + 52, 160), 10 * sc, fill=c + (255,))
            _ov(im, lambda q, x=x: q.rounded_rectangle(S(x + 6, 56, x + 18, 150), 6 * sc, fill=(255, 255, 255, 90)))
        if txt: d.text((189 * sc, 105 * sc), txt, font=font(F_BLACK, 70 * sc), fill=INK + (255,), anchor="mm", stroke_width=6 * sc, stroke_fill=(255, 255, 255, 255))
        return _done(im, w, h)
    return gcache(("batt", level, txt, col), mk)


def sticker_el(txt="100%"):
    def mk():
        w, h, sc = 300, 150, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(12, 14, 296, 146), 22 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(4, 4, 288, 136), 22 * sc, fill=(60, 210, 90, 255), outline=INK + (255,), width=6 * sc)
        d.text((146 * sc, 70 * sc), txt, font=font(F_BLACK, 72 * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("sticker", txt), mk)


# ---------------- keys: sleepy key (adenosine, purple, droopy face) and fake key (caffeine bean, brown, sly face) ----------------
def _key_blade(m, S):
    m.rounded_rectangle(S(120, 70, 330, 104), 12 * sc_k, fill=255)
    for x in (230, 270, 306): m.rectangle(S(x, 98, x + 20, 132), fill=255)


sc_k = 2


def _key_face(d, S, sc, mood, cx=78, cy=86):
    if mood == "sleep":
        for ex in (cx - 22, cx + 22): d.arc(S(ex - 13, cy - 12, ex + 13, cy + 6), 20, 160, fill=INK + (255,), width=5 * sc)
        d.ellipse(S(cx - 7, cy + 16, cx + 7, cy + 28), fill=(60, 16, 20, 255))
        return
    if mood == "sleepy":
        for ex in (cx - 22, cx + 22):
            d.ellipse(S(ex - 12, cy - 14, ex + 12, cy + 14), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
            d.ellipse(S(ex - 6, cy, ex + 6, cy + 12), fill=INK + (255,))
            d.chord(S(ex - 14, cy - 16, ex + 14, cy + 16), 180, 360, fill=ADE_L + (255,)); d.line(S(ex - 13, cy, ex + 13, cy), fill=INK + (255,), width=4 * sc)
        d.arc(S(cx - 14, cy + 18, cx + 14, cy + 32), 200, 340, fill=INK + (255,), width=4 * sc)
        return
    lk = 3 if mood == "sly" else 0
    for ex in (cx - 22, cx + 22):
        d.ellipse(S(ex - 12, cy - 14, ex + 12, cy + 14), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        d.ellipse(S(ex - 6 + lk, cy - 6, ex + 6 + lk, cy + 6), fill=INK + (255,))
        if mood == "sly": d.rectangle(S(ex - 14, cy - 16, ex + 14, cy - 4), fill=(0, 0, 0, 0)); d.line(S(ex - 13, cy - 4, ex + 13, cy - 4), fill=INK + (255,), width=4 * sc)
    if mood == "sly": d.arc(S(cx - 18, cy + 8, cx + 16, cy + 32), 15, 150, fill=INK + (255,), width=5 * sc)
    elif mood == "wow": d.ellipse(S(cx - 8, cy + 16, cx + 8, cy + 34), fill=(60, 16, 20, 255))
    elif mood == "sweat": d.arc(S(cx - 14, cy + 18, cx + 14, cy + 34), 200, 340, fill=INK + (255,), width=4 * sc); d.ellipse(S(cx + 34, cy - 30, cx + 46, cy - 12), fill=(140, 210, 255, 255))
    else: d.arc(S(cx - 16, cy + 10, cx + 16, cy + 30), 20, 160, fill=INK + (255,), width=5 * sc)


def skey_el(mood="sleepy"):
    """adenosine = the SLEEPY key (purple, droopy)."""
    def mk():
        w, h, sc = 340, 170, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        head = lambda m: m.ellipse(S(10, 14, 146, 158), fill=255)
        _outline(im, lambda m: (head(m), _key_blade(m, S)), 11)
        shape_grad(im, lambda m: _key_blade(m, S), ADE_L, ADE)
        shape_grad(im, head, ADE_L, ADE_D)
        _ov(im, lambda q: q.ellipse(S(36, 30, 86, 62), fill=(255, 255, 255, 110)))
        _key_face(d, S, sc, mood)
        return _done(im, w, h)
    return gcache(("skey", mood), mk)


def ckey_el(mood="sly"):
    """caffeine = the FAKE key (same blade, coffee-bean head)."""
    def mk():
        w, h, sc = 340, 170, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        head = lambda m: m.ellipse(S(4, 20, 152, 152), fill=255)
        _outline(im, lambda m: (head(m), _key_blade(m, S)), 11)
        shape_grad(im, lambda m: _key_blade(m, S), CAF_L, CAF)
        shape_grad(im, head, CAF_L, CAF_D)
        d.arc(S(30, 22, 126, 150), 250, 290, fill=CAF_D + (255,), width=6 * sc)
        _ov(im, lambda q: q.ellipse(S(30, 34, 80, 64), fill=(255, 255, 255, 90)))
        _key_face(d, S, sc, mood)
        return _done(im, w, h)
    return gcache(("ckey", mood), mk)


# ---------------- receptor lock (sits on the cell surface; keyhole faces up) ----------------
def lock_el(lit=0.0):
    lit = round(clamp(lit) * 4) / 4
    def mk():
        w, h, sc = 170, 190, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: (m.rounded_rectangle(S(10, 40, 160, 182), 26 * sc, fill=255), m.chord(S(10, 6, 160, 90), 180, 360, fill=255))
        _outline(im, body, 11)
        top = tuple(int(a + (b - a) * lit) for a, b in zip((120, 240, 226), (255, 236, 120)))
        bot = tuple(int(a + (b - a) * lit) for a, b in zip(LOCK_D, (230, 150, 20)))
        shape_grad(im, body, top, bot)
        d.ellipse(S(66, 30, 104, 68), fill=INK + (255,)); d.polygon(S(72, 56, 98, 56, 92, 118, 78, 118), fill=INK + (255,))
        _ov(im, lambda q: q.rounded_rectangle(S(24, 52, 44, 160), 10 * sc, fill=(255, 255, 255, 80)))
        return _done(im, w, h)
    return gcache(("lock", lit), mk)


def brain_cell(f, cx, cy, w, t, locks=(), dim=0.0, hgt=360, seed=4, sleepy=False):
    """a brain cell seen from the side as a big soft blob with branches; locks = [(dx, key, rot, lit)] sitting on its TOP edge
    (key: None | 'skey' | 'ckey' | el). Returns the list of lock keyhole points."""
    rng = np.random.default_rng(seed); top = cy - hgt / 2
    for i in range(7):
        a = -math.pi * (0.1 + 0.8 * i / 6); L = rng.uniform(140, 230)
        x0, y0 = cx + 0.5 * w * math.cos(a), cy + 0.5 * hgt * math.sin(a) * -1 + 40
        x1, y1 = cx + (0.5 * w + L) * math.cos(a), cy + (0.5 * hgt + L) * -math.sin(a) * -1 + 60 + 40 * math.sin(t + i)
        if y1 > top + 40:
            cv2.line(f, (int(x0), int(y0)), (int(x1), int(y1)), C(INK), 30, cv2.LINE_AA); cv2.line(f, (int(x0), int(y0)), (int(x1), int(y1)), C(NEU_D), 20, cv2.LINE_AA)
    col = tuple(int(a * (1 - 0.45 * dim)) for a in NEU); col_d = tuple(int(a * (1 - 0.45 * dim)) for a in NEU_D)
    cv2.ellipse(f, (int(cx), int(cy)), (int(w / 2) + 10, int(hgt / 2) + 10), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
    g = np.clip((_yy - top) / hgt, 0, 1)[..., None]
    m = np.zeros((H, W), np.float32); cv2.ellipse(m, (int(cx), int(cy)), (int(w / 2), int(hgt / 2)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    shade = np.array(C(col), np.float32) * (1 - g) + np.array(C(col_d), np.float32) * g
    f[:] = f * (1 - m[..., None]) + shade * m[..., None]
    cv2.ellipse(f, (int(cx - w * 0.22), int(cy - hgt * 0.22)), (int(w * 0.12), int(hgt * 0.07)), -10, 0, 360, C(tuple(min(255, c + 60) for c in col)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy + hgt * 0.12)), int(hgt * 0.16), C(INK), -1, cv2.LINE_AA)
    cv2.circle(f, (int(cx), int(cy + hgt * 0.12)), int(hgt * 0.16) - 7, C(tuple(int(c * 0.8) for c in ADE_D) if sleepy else (60, 90, 200)), -1, cv2.LINE_AA)
    pts = []
    for dx, key, rot, lit in locks:
        lx = cx + dx; ly = cy - (hgt / 2) * math.sqrt(max(0.0, 1 - (2 * dx / w) ** 2)) - 10
        if key is not None:
            el = skey_el("sleepy") if key == "skey" else (ckey_el("sly") if key == "ckey" else key)
            rot_comp(f, scale_el(el, 0.6), lx + 4, ly - 72, 90 + rot, 1.0)
        comp(f, scale_el(lock_el(lit), 0.68), lx, ly)
        pts.append((lx, ly - 40))
    return pts


def key_pile(f, x, y, n, t, w=520, s=0.42, wob=1.0, seed=7, mood="sleepy"):
    """a heap of sleepy keys growing upward from baseline y (n keys)."""
    rng = np.random.default_rng(seed); el = scale_el(skey_el(mood), s)
    row, i = 0, 0
    while i < n:
        per = max(1, int((w - row * 70) / (330 * s * 0.75)))
        for j in range(per):
            if i >= n: break
            xx = x - (per - 1) * (330 * s * 0.75) / 2 + j * (330 * s * 0.75) + rng.uniform(-12, 12)
            yy = y - row * 150 * s * 0.8 + 3 * wob * math.sin(t * 3 + i)
            rot_comp(f, el, xx, yy, rng.uniform(-35, 35), 1.0)
            i += 1
        row += 1


# ---------------- smile mask on a stick (hiding tiredness) ----------------
def mask_el():
    def mk():
        w, h, sc = 300, 420, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(140, 220, 160, 416), 8 * sc, fill=INK + (255,)); d.rounded_rectangle(S(144, 224, 156, 412), 6 * sc, fill=CAF_L + (255,))
        d.ellipse(S(10, 10, 290, 270), fill=INK + (255,)); shape_grad(im, lambda m: m.ellipse(S(18, 18, 282, 262), fill=255), (255, 252, 230), (255, 214, 120))
        for ex in (100, 200): d.arc(S(ex - 30, 90, ex + 30, 140), 200, 340, fill=INK + (255,), width=9 * sc)
        d.chord(S(80, 150, 220, 230), 0, 180, fill=(60, 16, 20, 255)); d.chord(S(110, 186, 190, 230), 0, 180, fill=(236, 90, 96, 255))
        for ex in (70, 230): _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 22, 150, ex + 22, 176), fill=(255, 120, 120, 120)))
        return _done(im, w, h)
    return gcache("mask", mk)


# ---------------- bed with blanket (Chubby sits behind it) + nightcap ----------------
def bed_el(w_=620):
    def mk():
        w, h, sc = w_, 360, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(6, 120, w - 6, 300), 30 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(16, 130, w - 16, 290), 24 * sc, fill=255), (120, 170, 255), (60, 100, 210))
        for k in range(1, 5): d.line(S(40 + k * (w - 80) / 5, 140, 30 + k * (w - 80) / 5, 284), fill=(255, 255, 255, 90), width=5 * sc)
        d.rectangle(S(20, 296, 60, 356), fill=INK + (255,)); d.rectangle(S(w - 60, 296, w - 20, 356), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("bed", w_), mk)


def nightcap(f, hx, hy, s):
    P = np.array([[hx - 95 * s, hy - 40 * s], [hx + 90 * s, hy - 55 * s], [hx + 150 * s, hy - 150 * s], [hx + 10 * s, hy - 160 * s]], np.int32)
    cv2.fillPoly(f, [P], C(INK), cv2.LINE_AA)
    P2 = np.array([[hx - 82 * s, hy - 48 * s], [hx + 82 * s, hy - 60 * s], [hx + 140 * s, hy - 146 * s], [hx + 8 * s, hy - 150 * s]], np.int32)
    cv2.fillPoly(f, [P2], C((80, 120, 230)), cv2.LINE_AA)
    cv2.circle(f, (int(hx + 150 * s), int(hy - 150 * s)), int(26 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(hx + 150 * s), int(hy - 150 * s)), int(20 * s), C(WHITE), -1, cv2.LINE_AA)


# ---------------- bee + flowers ----------------
def bee_el(flap=0, mood="happy"):
    def mk():
        w, h, sc = 300, 240, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        wy = 30 if flap else 50
        for wx in (110, 170):
            _ov(im, lambda q, wx=wx: q.ellipse(S(wx - 50, wy - 30, wx + 40, wy + 50), fill=(220, 240, 255, 200)))
            d.ellipse(S(wx - 50, wy - 30, wx + 40, wy + 50), outline=INK + (255,), width=5 * sc)
        body = lambda m: m.ellipse(S(40, 80, 250, 210), fill=255)
        _outline(im, body, 11); shape_grad(im, body, (255, 230, 90), BEE_D)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        _masked(im, bm, lambda q: [q.rectangle(S(x, 70, x + 26, 220), fill=INK + (255,)) for x in (120, 170, 216)])
        d.polygon(S(246, 138, 290, 145, 246, 156), fill=INK + (255,))
        _eyes(d, S, sc, [(76, 130), (106, 130)], 14, (-0.6, 0), happy=(mood == "happy"))
        if mood == "wow": d.ellipse(S(82, 160, 98, 180), fill=(60, 16, 20, 255))
        else: d.arc(S(74, 150, 104, 176), 20, 160, fill=INK + (255,), width=5 * sc)
        d.line(S(80, 90, 60, 40), fill=INK + (255,), width=5 * sc); d.ellipse(S(50, 28, 70, 48), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("bee", flap, mood), mk)


def flower_el(kind="coffee", glow_=0.0):
    glow_ = round(clamp(glow_) * 4) / 4
    def mk():
        w, h, sc = 340, 340, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        cx, cy = 170, 170; n_ = 5
        pc, pd = ((255, 255, 255), (220, 224, 236)) if kind == "coffee" else ((255, 252, 240), (240, 220, 200))
        def petals(m):
            for i in range(n_):
                a = 2 * math.pi * i / n_ - math.pi / 2; px, py = cx + 90 * math.cos(a), cy + 90 * math.sin(a)
                if kind == "coffee": m.polygon(S(cx + 30 * math.cos(a + 1.2), cy + 30 * math.sin(a + 1.2), px + 60 * math.cos(a), py + 60 * math.sin(a), cx + 30 * math.cos(a - 1.2), cy + 30 * math.sin(a - 1.2)), fill=255)
                else: m.ellipse(S(px - 58, py - 58, px + 58, py + 58), fill=255)
        _outline(im, petals, 11); shape_grad(im, petals, pc, pd)
        cc = tuple(int(a + (b - a) * glow_) for a, b in zip((255, 214, 60), CAF_L))
        d.ellipse(S(cx - 46, cy - 46, cx + 46, cy + 46), fill=INK + (255,)); d.ellipse(S(cx - 38, cy - 38, cx + 38, cy + 38), fill=cc + (255,))
        for i in range(8):
            a = 2 * math.pi * i / 8; d.line(S(cx, cy, cx + 30 * math.cos(a), cy + 30 * math.sin(a)), fill=(240, 150, 20, 255), width=4 * sc)
        return _done(im, w, h)
    return gcache(("flower", kind, glow_), mk)


def lemon_el():
    def mk():
        w, h, sc = 220, 170, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        body = lambda m: (m.ellipse(S(20, 20, 200, 150), fill=255), m.ellipse(S(4, 70, 40, 100), fill=255), m.ellipse(S(180, 70, 216, 100), fill=255))
        _outline(im, body, 11); shape_grad(im, body, (255, 246, 120), (240, 196, 10))
        _ov(im, lambda q: q.ellipse(S(54, 40, 110, 70), fill=(255, 255, 255, 120)))
        return _done(im, w, h)
    return gcache("lemon", mk)


def sun_icon(f, x, y, r, t=0.0):
    for i in range(10):
        a = t * 0.6 + i * math.pi / 5
        cv2.line(f, (int(x + r * 1.25 * math.cos(a)), int(y + r * 1.25 * math.sin(a))), (int(x + r * 1.65 * math.cos(a)), int(y + r * 1.65 * math.sin(a))), C((255, 200, 30)), max(3, int(r * 0.18)), cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(r) + 5, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), int(r), C((255, 214, 40)), -1, cv2.LINE_AA)


def moon_icon(f, x, y, r, bg):
    cv2.circle(f, (int(x), int(y)), int(r) + 5, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), int(r), C((255, 244, 190)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x + r * 0.45), int(y - r * 0.3)), int(r * 0.85), C(bg), -1, cv2.LINE_AA)


def zzs(f, x, y, t, n=3, col=WHITE, s=1.0):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1.0
        comp(f, ed_el("", "Z", "", big_col=col, big_size=int((40 + 30 * ph) * s)), x + 40 * ph * s + 10 * i, y - 160 * ph * s, op=math.sin(math.pi * ph))


def caf_dot(f, x, y, r=14):
    cv2.circle(f, (int(x), int(y)), int(r) + 4, C(INK), -1, cv2.LINE_AA); cv2.ellipse(f, (int(x), int(y)), (int(r), int(r * 0.8)), 30, 0, 360, C(CAF), -1, cv2.LINE_AA)
    cv2.line(f, (int(x - r * 0.5), int(y - r * 0.4)), (int(x + r * 0.5), int(y + r * 0.4)), C(CAF_D), 3, cv2.LINE_AA)
