# ================= anim_props_lib25.py (ep 25, 6 Nov): GHEE + THE TRIAL OF THE HOME TESTS. New craft: TRANSLUCENCY (_tl_fill): a thick glowing centre, thin parts + edges brighter and MORE saturated,
# soft transitions inside, a firm ink silhouette, a saturated warm accent at the shadow edge (Gurney, 'Subsurface scattering II'; SVS forum thread: the object is more saturated or warmer than its background).
# ONE accent: GHEE GOLD. Fake fats read paler + colder. Court wood is the warm neutral. RED only for stamps.
# ghee_jar_el(kind grain|liquid|split|smooth|white, level, mood, look, lid), blob(f, x, y, r, k, t, slide, col) live melting ghee, hand_big_el(), palm_tree(f, x, y, s, k, t, mood), judge_wig(f, x, y, s), gavel_at(f, gx, gy, ang, s),
# block_el, tin_el(fake, mood, look), label_card(f, cx, cy, t, t0s, fake), tube_el(k, level), sesame_el, vanaspati_el(mood, look, tag), essence_el(mood), dye_el, sealer_el(down), foil_el, potato_el(mood), glass_float(f, x, y, s, t, col, label),
# test_icon_el(kind), verdict_board(f, t, t0s, ...), test_pill(f, n, t, t0), peaks(f, x, y, w, h, k, spike), chain_el(n, col), set_court(t) + bench_front(f, top_y), set_store(t, beam).
ACC = (226, 158, 34); ACC_S = (150, 92, 18); ACC_L = (252, 214, 120); ACC_XL = (254, 236, 186)
GHEE = (240, 176, 44); GHEE_D = (206, 128, 22); GHEE_RIM = (255, 206, 70); GHEE_HOT = (255, 240, 170)
FAKE = (232, 214, 130); FAKE_D = (206, 180, 100); PALMO = (232, 120, 40)
RED_V = (190, 52, 40); GOOD = (54, 140, 96); WOOD = (112, 72, 44); WOOD_D = (78, 48, 30); WOOD_L = (150, 104, 66)


def _tl_fill(im, mask_fn, base=GHEE, deep=GHEE_D, rim=GHEE_RIM, hot=GHEE_HOT, light=(-0.35, -0.9), thick=24, hotamt=0.7, sc=SC3):
    """TRANSLUCENCY: fill a shape so it reads as light travelling through it. Thick middle = deep and saturated, edges + thin parts = bright rim, the side toward the light = hot. Soft inside; draw the firm ink outline AFTER this."""
    S = lambda *v: [x * sc for x in v]
    m = Image.new("L", im.size, 0); mask_fn(ImageDraw.Draw(m), S); M_ = np.array(m, np.uint8)
    if M_.max() == 0: return
    dt = cv2.distanceTransform(M_, cv2.DIST_L2, 3).astype(np.float32) / sc
    e = np.exp(-dt / thick)[..., None]                    # 1 at the edge, 0 deep inside
    ys, xs = np.where(M_ > 0); cx, cy = xs.mean(), ys.mean(); ext = max(xs.max() - xs.min(), ys.max() - ys.min(), 1) / 2
    yy, xx = np.mgrid[0:M_.shape[0], 0:M_.shape[1]].astype(np.float32)
    lit = np.clip(((xx - cx) * light[0] + (yy - cy) * light[1]) / ext, 0, 1)[..., None]
    col = np.array(deep, np.float32) * (1 - np.clip(dt / (thick * 2.0), 0, 1))[..., None] * 0 + np.array(base, np.float32)
    col = col * (1 - e) + np.array(rim, np.float32) * e                                             # rim at thin parts
    centre = np.clip(dt / (thick * 3.0), 0, 1)[..., None]
    col = col * (1 - centre * 0.55) + np.array(deep, np.float32) * centre * 0.55                    # thick = deeper
    col = col * (1 - lit * hotamt * (0.35 + 0.65 * e)) + np.array(hot, np.float32) * lit * hotamt * (0.35 + 0.65 * e)
    col = cv2.GaussianBlur(col, (0, 0), 3 * sc)
    out = np.dstack([np.clip(col, 0, 255).astype(np.uint8), M_])
    im.alpha_composite(Image.fromarray(out, "RGBA"))


def ghee_jar_el(kind="grain", level=0.78, mood=None, look=(0, 0), lid=False, seed=51):
    """a wide glass jar of ghee. grain = even danedar grains, liquid = clear gold, split = pale solid under clear oil with a hard line (the fridge giving a clue), smooth = waxy, white = buffalo ghee."""
    def mk():
        w, h = 340, 420; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        x0, x1, y0, y1 = 44, 296, 70, 400; top = y1 - (y1 - y0 - 10) * level
        body = lambda q, S_: q.rounded_rectangle(S_(x0 + 7, top, x1 - 7, y1 - 7), 22 * SC3, fill=255)
        if kind == "split":
            ym = top + (y1 - top) * 0.42
            _tl_fill(im, lambda q, S_: q.rounded_rectangle(S_(x0 + 7, top, x1 - 7, ym + 20), 8 * SC3, fill=255), (246, 204, 92), (232, 176, 60), (255, 226, 130), GHEE_HOT, thick=18)
            _tl_fill(im, lambda q, S_: q.rounded_rectangle(S_(x0 + 7, ym, x1 - 7, y1 - 7), 22 * SC3, fill=255), (240, 226, 170), (222, 204, 140), (250, 238, 190), (255, 250, 220), thick=18, hotamt=0.3)
            P = _wob([(x0 + 7 + i * (x1 - x0 - 14) / 8, ym + 6 * math.sin(i * 1.4)) for i in range(9)], 2, seed + 3)
            d.line([(a * SC3, b * SC3) for a, b in P], fill=INKC + (255,), width=4 * SC3)
            for i in range(26):
                a, b = rng.uniform(x0 + 22, x1 - 22), rng.uniform(ym + 18, y1 - 22); r_ = rng.uniform(4, 12); d.ellipse(S(a - r_, b - r_ * 0.7, a + r_, b + r_ * 0.7), fill=(214, 196, 132, 255))
        elif kind == "white":
            _tl_fill(im, body, (250, 244, 224), (232, 222, 192), (255, 252, 240), (255, 255, 250), thick=20, hotamt=0.4)
        elif kind == "smooth":
            _tl_fill(im, body, (246, 196, 84), (224, 158, 50), (255, 222, 120), GHEE_HOT, thick=22)
        else:
            _tl_fill(im, body, GHEE, GHEE_D, GHEE_RIM, GHEE_HOT, thick=22)
        if kind == "grain":
            for i in range(120):
                a, b = rng.uniform(x0 + 16, x1 - 16), rng.uniform(top + 12, y1 - 16); r_ = rng.uniform(2.6, 5.2)
                c = (255, 226, 130, 255) if i % 2 else (196, 122, 22, 255); d.ellipse(S(a - r_, b - r_, a + r_, b + r_), fill=c)
        _ink_poly(d, [(x0 + 7, top), (x1 - 7, top)], None, seed + 6, 4, closed=False, amp=0.8)
        _ink_poly(d, [(x0, y0), (x1, y0), (x1 + 6, y0 + 40), (x1 + 2, y1 - 16), (x1 - 18, y1), (x0 + 18, y1), (x0 - 2, y1 - 16), (x0 - 6, y0 + 40)], None, seed, INK_W, amp=1.2)
        d.line(S(x0 + 18, y0 + 56, x0 + 18, y1 - 60), fill=(255, 255, 255, 170), width=7 * SC3)
        if lid: _ink_poly(d, [(x0 - 8, y0 - 44), (x1 + 8, y0 - 44), (x1 + 6, y0 + 4), (x0 - 6, y0 + 4)], (196, 66, 52), seed + 2, INK_W, amp=1.0)
        else: _ink_ell(d, (x0 + x1) / 2, y0, (x1 - x0) / 2, 15, (248, 244, 232), seed + 4, 5)
        if mood: _face(d, S, (x0 + x1) / 2, (top + y1) / 2 + 8, 1.35, mood, look)
        return _done(im, w, h)
    return gcache(("gjar25", kind, round(level, 2), mood, look, lid, seed), mk)


def _blob_el(r, k, col, seed=7):
    """a dollop of ghee: k 0 = a soft grainy mound, 1 = a thin clear pool. Bright thin edges, deep centre."""
    base, deep, rim, hot = col
    def mk():
        w, h = int(r * 3.1), int(r * 2.3); im, d, S = _cv(w, h); cx, cy = w / 2, h / 2
        rx = r * (0.82 + 0.58 * k); ry = r * (0.72 - 0.34 * k)
        pts = [(cx + rx * math.cos(a) * (1 + 0.06 * math.sin(3 * a + seed) + 0.05 * k * math.sin(5 * a)), cy + ry * math.sin(a) * (1 + 0.07 * math.cos(2 * a + seed))) for a in np.linspace(0, 2 * math.pi, 40)[:-1]]
        _tl_fill(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts], fill=255), base, deep, rim, hot, thick=max(6, ry * 0.34), hotamt=0.85)
        if k < 0.7:
            rng = np.random.default_rng(seed)
            for i in range(int(36 * (1 - k))):
                a, q = rng.uniform(0, 2 * math.pi), rng.uniform(0, 0.8); x, y = cx + rx * q * math.cos(a), cy + ry * q * math.sin(a); r_ = r * 0.05
                d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(255, 226, 130, 200) if i % 2 else tuple(deep) + (200,))
        _ink_poly(d, pts, None, seed, 5, amp=0.8)
        d.ellipse(S(cx - rx * 0.46, cy - ry * 0.58, cx - rx * 0.12, cy - ry * 0.26), fill=(255, 255, 255, 215))
        return _done(im, w, h)
    return gcache(("blob25", r, round(k * 12) / 12, col, seed), mk)


GOLD_C = (GHEE, GHEE_D, GHEE_RIM, GHEE_HOT); PALM_C = ((248, 160, 60), (224, 100, 26), (255, 196, 90), (255, 232, 160)); PALE_C = (FAKE, FAKE_D, (246, 236, 180), (255, 250, 220))


def blob(f, x, y, r=90, k=0.0, t=0.0, slide=0.0, col=GOLD_C, seed=7):
    """live melting ghee: glow behind (it lets light through) + a shiny trail if it slid."""
    if slide > 0:                                                    # the wet shiny trail left behind: tapered, see-through
        ov = f.copy(); y0_ = y - slide
        P = np.array([(x - r * 0.42, y - r * 0.1), (x - r * 0.2, y0_ - r * 0.2), (x + r * 0.2, y0_ - r * 0.2), (x + r * 0.42, y - r * 0.1)], np.int32)
        cv2.fillConvexPoly(ov, P, C(col[2]), cv2.LINE_AA); f[:] = f * 0.52 + ov * 0.48
        cv2.line(f, (int(x - r * 0.18), int(y0_)), (int(x - r * 0.26), int(y - r * 0.2)), C((255, 250, 225)), max(2, int(r * 0.05)), cv2.LINE_AA)
    glow(f, x, y + slide * 0, r * 1.7, col[2], 0.20)
    comp(f, _blob_el(int(r), k, col, seed), x, y)


def hand_big_el(seed=61):
    """a big open palm, fingers up, in the ink language: rolled mint cuff at the wrist. 620 x 860."""
    def mk():
        w, h = 620, 880; im, d, S = _cv(w, h)
        _ink_poly(d, [(190, 700), (430, 700), (450, 880), (170, 880)], INK_MINT, seed + 7, INK_W + 1, amp=1.4)
        _ink_poly(d, [(170, 680), (450, 680), (458, 742), (162, 742)], INK_MINT_S, seed + 8, INK_W, amp=1.2)
        F_ = [(146, 118, 40, 330), (250, 36, 42, 330), (360, 62, 40, 330), (462, 178, 36, 340)]
        for i, (x, y, r_, yb) in enumerate(F_):
            _ink_poly(d, _arcpts(x, y + r_, r_, r_, 180, 360, 10) + [(x + r_, yb + 40), (x - r_, yb + 40)], INK_SKIN, seed + i, INK_W, amp=0.9)
        _ink_poly(d, [(508, 470), (600, 348), (612, 300), (576, 280), (536, 310), (470, 390)], INK_SKIN, seed + 5, INK_W, amp=1.0)
        pts = [(98, 330), (498, 330), (516, 480), (460, 640), (430, 710), (190, 710), (140, 620), (96, 470)]
        d.polygon([(x * SC3, y * SC3) for x, y in pts], fill=INK_SKIN + (255,))
        _ink_line_pts = _wob(pts + [pts[0]], 1.4, seed + 6); d.line([(x * SC3, y * SC3) for x, y in _ink_line_pts], fill=INKC + (255,), width=INK_W * SC3, joint="curve")
        d.rectangle(S(108, 324, 490, 372), fill=INK_SKIN + (255,))
        for a0, b0, a1, b1 in ((124, 430, 400, 396), (150, 560, 432, 470), (432, 640, 400, 520)):
            d.line(S(a0, b0, (a0 + a1) / 2, (b0 + b1) / 2 - 16, a1, b1), fill=INK_SKIN_S + (255,), width=5 * SC3, joint="curve")
        for x, y, r_, yb in F_:
            d.line(S(x - r_ * 0.5, yb - 14, x + r_ * 0.5, yb - 14), fill=INK_SKIN_S + (255,), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("hand25", seed), mk)


def palm_tree(f, x, y, s=1.0, k=1.0, t=0.0, mood="happy", look=(0, 0)):
    """the gag: a little palm tree that grows from the base point (x, y) with a springy overshoot. Its trunk has a face."""
    if k <= 0.01: return
    def mk():
        w, h = 480, 640; im, d, S = _cv(w, h)
        tr = [(210, 636), (272, 636), (262, 400), (276, 240), (248, 236), (226, 400)]
        _ink_poly(d, tr, (168, 122, 76), 71, INK_W, amp=1.2)
        for i in range(6): d.line(S(214 + i * 2, 590 - i * 66, 270 - i * 1.5, 582 - i * 66), fill=(122, 84, 50, 255), width=4 * SC3)
        for i, (ax, ay, bx, by) in enumerate(((262, 238, 462, 300), (262, 238, 18, 300), (262, 238, 420, 110), (262, 238, 60, 118), (262, 238, 262, 30))):
            mx, my = (ax + bx) / 2, (ay + by) / 2 - 56
            P = _arcpts(0, 0, 1, 1, 0, 1, 2)[:0]; n_ = np.array([by - ay, ax - bx], np.float32); n_ = n_ / (np.linalg.norm(n_) + 1e-6) * 28
            up = [(ax, ay), (mx - n_[0], my - n_[1]), (bx, by), (mx + n_[0] * 0.2, my + n_[1] * 0.2)]
            _ink_poly(d, up, (72, 164, 92) if i % 2 else (56, 142, 80), 72 + i, INK_W - 1, amp=1.4)
        _ink_ell(d, 234, 256, 28, 28, (130, 84, 50), 78, 5); _ink_ell(d, 288, 262, 28, 28, (112, 70, 42), 79, 5)
        if mood: _face(d, S, 244, 440, 1.2, mood, look)
        return _done(im, w, h)
    el = gcache(("palmtree25", mood, look), mk)
    kk = max(0.01, k); yy = y - 320 * s * kk
    rot_comp(f, el, x, yy, 2.5 * math.sin(t * 2.6), s * kk)


def judge_wig(f, x, y, s=1.0, lean=0.0):
    """a court wig + white bands over a chub in a black robe (feet at x, y)."""
    hx, hy = x + lean * 2 * s, y - 420 * s
    for j, (dx, dy, r_) in enumerate(((-108, -30, 40), (-92, 34, 38), (-110, 92, 34), (108, -30, 40), (92, 34, 38), (110, 92, 34), (-70, -86, 44), (0, -112, 48), (70, -86, 44))):
        cv2.circle(f, (int(hx + dx * s), int(hy + dy * s)), int((r_ + 5) * s), C(INKC), -1, cv2.LINE_AA)
    for j, (dx, dy, r_) in enumerate(((-108, -30, 40), (-92, 34, 38), (-110, 92, 34), (108, -30, 40), (92, 34, 38), (110, 92, 34), (-70, -86, 44), (0, -112, 48), (70, -86, 44))):
        cv2.circle(f, (int(hx + dx * s), int(hy + dy * s)), int(r_ * s), C((250, 246, 232)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(hx + dx * s), int(hy + dy * s)), (int(r_ * 0.55 * s), int(r_ * 0.5 * s)), 20, 200, 340, C((206, 196, 172)), max(2, int(4 * s)), cv2.LINE_AA)
    by = y - 300 * s
    for sg in (-1, 1):
        P = np.array([(x + lean * s, by), (x + sg * 40 * s + lean * s, by), (x + sg * 44 * s + lean * s, by + 74 * s), (x + sg * 8 * s + lean * s, by + 74 * s)], np.int32)
        cv2.fillPoly(f, [P], C((252, 250, 244)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


ROBE = (46, 42, 54)


def _gavel_el():
    def mk():
        w, h = 300, 150; im, d, S = _cv(w, h)
        _ink_poly(d, [(10, 64), (190, 58), (190, 88), (10, 84)], (164, 112, 66), 81, 5, amp=0.8)
        _ink_poly(d, [(178, 22), (270, 22), (270, 128), (178, 128)], (128, 80, 44), 82, INK_W, amp=1.0)
        for x in (196, 252): d.line(S(x, 24, x, 126), fill=(244, 214, 110, 255), width=7 * SC3)
        return _done(im, w, h)
    return gcache(("gavel25",), mk)


def gavel_at(f, gx, gy, ang, s=1.0):
    """gx, gy = the grip (handle end); ang = 0 points right, + counter-clockwise."""
    el = _gavel_el(); L = 120 * s; a = math.radians(ang)
    rot_comp(f, el, gx + L * math.cos(a), gy - L * math.sin(a), ang, s)


def block_el():
    def mk():
        w, h = 240, 80; im, d, S = _cv(w, h)
        _ink_ell(d, 120, 26, 100, 18, (160, 110, 66), 83, 5); _ink_poly(d, [(20, 26), (220, 26), (220, 58), (20, 58)], (128, 80, 44), 84, 5, amp=0.7); _ink_ell(d, 120, 26, 100, 18, (172, 122, 76), 85, 5)
        return _done(im, w, h)
    return gcache(("block25",), mk)


def tin_el(fake=False, mood=None, look=(0, 0), seed=91, tag_text="PURE GHEE"):
    def mk():
        w, h = 300, 400; im, d, S = _cv(w, h)
        base = (222, 226, 226) if not fake else (214, 214, 200)
        _ink_poly(d, [(36, 52), (264, 52), (270, 388), (30, 388)], base, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.rectangle(S_(30, 52, 270, 388), fill=255), lambda q, S_, c: q.rectangle(S_(210, 40, 280, 396), fill=c), (120, 120, 118), 70)
        _ink_ell(d, 150, 52, 114, 22, (240, 240, 238), seed + 1, INK_W, n=26); _ink_ell(d, 150, 52, 60, 10, (200, 200, 198), seed + 2, 3, n=20)
        _ink_poly(d, [(44, 130), (256, 130), (256, 340), (44, 340)], (250, 230, 160) if not fake else (250, 240, 200), seed + 3, 4, amp=0.8)
        fn = font(F_BLACK, 40 * SC3); d.text((150 * SC3, 164 * SC3), tag_text, font=fn, fill=(160, 90, 20, 255), anchor="mm")
        if mood: _face(d, S, 150, 262, 1.25, mood, look)
        return _done(im, w, h)
    return gcache(("tin25", fake, mood, look, seed, tag_text), mk)


def label_card(f, cx, cy, t, t0s, fake=False, s=1.0, names=("LICENCE NO.", "MAKER", "BATCH NO.", "EXPIRY"), miss=(2, 3)):
    """a tin's label close up. Rows tick in on word times; fake=True leaves the rows in `miss` empty with a red X."""
    def mk():
        w, h = 760, 560; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 14), (746, 14), (746, 546), (14, 546)], (252, 246, 226), 95, INK_W, amp=1.2)
        return _done(im, w, h)
    comp(f, scale_el(gcache(("lblcard25",), mk), s), cx, cy)
    for i, nm in enumerate(names):
        y = cy - 190 * s + i * 126 * s
        comp(f, ed_el(nm, "", lead_col=INKC, lead_size=int(50 * s)), cx - 330 * s, y, anchor="l", op=1.0)
        if t >= t0s[i]:
            k = pin(t, t0s[i], 0.2); x_ = cx + 290 * s
            if fake and i in miss:
                cv2.line(f, (int(cx + 40 * s), int(y)), (int(cx + 190 * s), int(y)), C((170, 160, 140)), max(2, int(6 * s)), cv2.LINE_AA)
                comp(f, scale_el(_mark_el(False), s), x_, y, scale=k)
            else:
                comp(f, scale_el(_mark_el(True), s), x_, y, scale=k)


def _mark_el(ok=True):
    def mk():
        w, h = 110, 110; im, d, S = _cv(w, h)
        _ink_ell(d, 55, 55, 44, 44, GOOD if ok else RED_V, 97 if ok else 98, 5)
        if ok: d.line(S(34, 56, 50, 72, 78, 38), fill=(255, 255, 255, 255), width=10 * SC3, joint="curve")
        else:
            d.line(S(38, 38, 72, 72), fill=(255, 255, 255, 255), width=10 * SC3); d.line(S(72, 38, 38, 72), fill=(255, 255, 255, 255), width=10 * SC3)
        return _done(im, w, h)
    return gcache(("mark25", ok), mk)


def tube_el(k=0.0, level=0.62, acid_only=False, fat_col=(246, 200, 92), seed=101):
    """a test tube: fat on top, acid at the bottom. k 0..1 = the acid layer turns crimson."""
    k = round(clamp(k) * 8) / 8
    def mk():
        w, h = 170, 560; im, d, S = _cv(w, h); x0, x1, y0, y1 = 42, 128, 60, 500; ym = y0 + (y1 - y0) * (1 - level * 0.46)
        ty = y0 + (y1 - y0) * (1 - level)
        ac = _mix((236, 240, 236), (182, 22, 62), k)
        _tl_fill(im, lambda q, S_: q.rounded_rectangle(S_(x0 + 5, ty, x1 - 5, ym + 6), 4 * SC3, fill=255), fat_col, _mix(fat_col, (190, 120, 30), 0.4), _mix(fat_col, (255, 255, 200), 0.5), (255, 250, 220), thick=10)
        _tl_fill(im, lambda q, S_: (q.rectangle(S_(x0 + 5, ym, x1 - 5, y1 - 40), fill=255), q.ellipse(S_(x0 + 5, y1 - 80, x1 - 5, y1 - 2), fill=255)), ac, _mix(ac, (100, 0, 30), 0.5 * k), _mix(ac, (255, 255, 255), 0.25), (255, 255, 255), thick=10, hotamt=0.3)
        d.line(S(x0 + 5, ym, x1 - 5, ym), fill=INKC + (255,), width=3 * SC3)
        _ink_poly(d, [(x0, y0), (x1, y0), (x1, y1 - 40)] + _arcpts((x0 + x1) / 2, y1 - 40, (x1 - x0) / 2, 42, 0, 180, 10) + [(x0, y1 - 40)], None, seed, INK_W - 1, amp=0.6)
        _ink_poly(d, [(x0 - 12, y0 - 8), (x1 + 12, y0 - 8), (x1 + 12, y0 + 8), (x0 - 12, y0 + 8)], (246, 244, 236), seed + 1, 4, amp=0.5)
        d.line(S(x0 + 14, y0 + 30, x0 + 14, y1 - 60), fill=(255, 255, 255, 150), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("tube25", k, level, fat_col, seed), mk)


def vanaspati_el(mood=None, look=(0, 0), tag=False, seed=111):
    """a pale block of vanaspati (hydrogenated fat); tag=True hangs the sesame tag off it."""
    def mk():
        w, h = 380, 300; im, d, S = _cv(w, h)
        A, B_, C_, D_ = (24, 100), (66, 36), (316, 36), (272, 100)
        _ink_poly(d, [D_, C_, (316, 196), (272, 262)], (222, 214, 170), seed + 2, 5, amp=1.0); _ink_poly(d, [A, B_, C_, D_], (250, 244, 210), seed + 1, 5, amp=1.0); _ink_poly(d, [A, D_, (272, 262), (24, 262)], (240, 232, 190), seed, 6, amp=1.2)
        if mood: _face(d, S, 148, 180, 1.2, mood, look)
        if tag:
            d.line(S(268, 120, 322, 170), fill=INKC + (255,), width=4 * SC3)
            _ink_poly(d, [(296, 170), (366, 170), (366, 270), (296, 270)], (176, 66, 52), seed + 3, 4, amp=0.8)
            for (a, b) in ((316, 196), (344, 204), (322, 228), (348, 240), (318, 254)):
                d.ellipse(S(a - 7, b - 4, a + 7, b + 4), fill=(250, 232, 180, 255))
        return _done(im, w, h)
    return gcache(("vana25", mood, look, tag, seed), mk)


def sesame_el(n=30, seed=112):
    def mk():
        w, h = 220, 150; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        for i in range(n):
            x, y = rng.uniform(20, 200), rng.uniform(20, 130); r_ = 9; a = rng.uniform(0, 3.14)
            pts = [(x + r_ * math.cos(q + a) * (1.0 if math.sin(q) > 0 else 0.62), y + r_ * 0.55 * math.sin(q + a)) for q in np.linspace(0, 6.28, 12)]
            _ink_poly(d, pts, (246, 226, 176), seed + i, 2, amp=0.3)
        return _done(im, w, h)
    return gcache(("sesame25", n, seed), mk)


def essence_el(mood="smirk", look=(0, 0), seed=121, label="ESSENCE"):
    """a little bottle of artificial essence with a dropper top."""
    def mk():
        w, h = 220, 320; im, d, S = _cv(w, h)
        _ink_poly(d, [(84, 60), (136, 60), (136, 104), (184, 150), (184, 300), (36, 300), (36, 150), (84, 104)], (240, 200, 210), seed, INK_W - 1)
        _tl_fill(im, lambda q, S_: q.rounded_rectangle(S_(43, 170, 177, 294), 6 * SC3, fill=255), (232, 120, 150), (190, 60, 100), (252, 170, 190), (255, 230, 236), thick=14)
        _ink_poly(d, [(84, 60), (136, 60), (136, 104), (184, 150), (184, 300), (36, 300), (36, 150), (84, 104)], None, seed, INK_W - 1)
        _ink_poly(d, [(92, 14), (128, 14), (128, 60), (92, 60)], (70, 50, 60), seed + 1, 5, amp=0.6)
        _ink_poly(d, [(50, 196), (170, 196), (170, 240), (50, 240)], (252, 248, 236), seed + 2, 3, amp=0.5)
        fn = font(F_BLACK, 24 * SC3); d.text((110 * SC3, 218 * SC3), label, font=fn, fill=INKC + (255,), anchor="mm")
        if mood: _face(d, S, 110, 268, 0.75, mood, look)
        return _done(im, w, h)
    return gcache(("essence25", mood, look, seed, label), mk)


def sealer_el(down=0.0, seed=131):
    """a small tin-sealing press: the head comes down on a tin. down 0..1."""
    down = round(clamp(down) * 6) / 6
    def mk():
        w, h = 460, 620; im, d, S = _cv(w, h)
        _ink_poly(d, [(60, 560), (400, 560), (400, 606), (60, 606)], (88, 92, 104), seed, INK_W, amp=1.0)
        _ink_poly(d, [(336, 60), (390, 60), (390, 560), (336, 560)], (120, 124, 136), seed + 1, INK_W, amp=1.0)
        _ink_poly(d, [(120, 40), (390, 40), (390, 110), (120, 110)], (120, 124, 136), seed + 2, INK_W, amp=1.0)
        hy = 110 + 150 * down
        _ink_poly(d, [(176, 110), (216, 110), (216, hy), (176, hy)], (198, 200, 206), seed + 3, 5, amp=0.5)
        _ink_poly(d, [(120, hy), (272, hy), (272, hy + 44), (120, hy + 44)], (214, 64, 50), seed + 4, 6, amp=0.8)
        d.line(S(390, 90, 430, 26), fill=INKC + (255,), width=10 * SC3); _ink_ell(d, 434, 22, 18, 18, (214, 64, 50), seed + 5, 4, n=12)
        return _done(im, w, h)
    return gcache(("sealer25", down, seed), mk)


def potato_el(mood="sus", look=(0, 0), seed=141):
    def mk():
        w, h = 240, 200; im, d, S = _cv(w, h)
        _ink_ell(d, 120, 100, 100, 78, (206, 168, 110), seed, INK_W, amp=3)
        for x, y in ((60, 60), (170, 60), (190, 126), (70, 146)): d.ellipse(S(x - 5, y - 3, x + 5, y + 3), fill=(150, 110, 68, 255))
        if mood: _face(d, S, 120, 104, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("potato25", mood, look, seed), mk)


def glass_float(f, x, y, s=1.0, t=0.0, col=GOLD_C, label=None, kk=1.0, mood=None):
    """a glass of water with a blob of fat floating on top (bobbing)."""
    def mk():
        w, h = 230, 360; im, d, S = _cv(w, h)
        _tl_fill(im, lambda q, S_: q.polygon(S_(28, 92, 202, 92, 188, 338, 42, 338), fill=255), (176, 214, 236), (130, 184, 220), (214, 236, 248), (250, 254, 255), thick=20, hotamt=0.4)
        _ink_poly(d, [(14, 26), (216, 26), (192, 346), (38, 346)], None, 151, INK_W - 1, amp=0.9)
        d.line(S(36, 66, 50, 300), fill=(255, 255, 255, 170), width=6 * SC3)
        return _done(im, w, h)
    comp(f, scale_el(gcache(("gfl25",), mk), s), x, y)
    wy = y - 86 * s + 5 * s * math.sin(t * 2.2 + x)
    comp(f, scale_el(_blob_el(46, 0.25, col, int(x) % 5 + 1), s * kk), x + 4 * s * math.sin(t * 1.6 + x), wy)
    if label:
        comp(f, chip(label, INKC, MILK, int(26 * max(0.8, s))), x, y + 210 * s)


MILK = (252, 248, 238)


def _pill_el(n):
    def mk():
        w, h = 300, 76; im, d, S = _cv(w, h)
        _ink_poly(d, _arcpts(40, 38, 32, 32, 90, 270, 10) + _arcpts(260, 38, 32, 32, -90, 90, 10), ACC_L, 161, 5, amp=0.5)
        fn = font(F_BLACK, 40 * SC3); d.text((150 * SC3, 38 * SC3), n, font=fn, fill=INKC + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("pill25", n), mk)


def test_pill(f, n, t, t0, y=270):
    if t >= t0: comp(f, _pill_el(f"TEST {n}"), 540, y, scale=pin(t, t0, 0.2))


def chain_el(n=4, col=ACC, r=22, seed=171, mood=None):
    """a fat molecule drawn as a chain of beads: n = 4 is butyric (tiny), 16-18 is a long fat."""
    def mk():
        w = int(60 + (n - 1) * r * 1.5 + r); h = 120 if not mood else 150; im, d, S = _cv(w, h); pts = [(30 + r / 2 + i * r * 1.5, 56 + (10 if i % 2 else -10)) for i in range(n)]
        d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (255,), width=6 * SC3)
        for i, (x, y) in enumerate(pts): _ink_ell(d, x, y, r * 0.72, r * 0.72, col, seed + i, 4, n=14, amp=0.5)
        if mood: _face(d, S, w / 2, 112, 0.7, mood)
        return _done(im, w, h)
    return gcache(("chain25", n, col, r, seed, mood), mk)


def peaks(f, x0, y0, w, h, k, spike=1.0, seed=3, col=None, hi=None):
    """a chromatogram that draws itself: the machine's readout. spike = the height of the first (butyric) peak."""
    col = col or ACC_S; hi = hi or RED_V
    cv2.rectangle(f, (x0, y0), (x0 + w, y0 + h), C((252, 248, 236)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x0 + w, y0 + h), C(INKC), 5, cv2.LINE_AA)
    rng = np.random.default_rng(seed); P = [(0.14, spike * 0.62, 0.012)] + [(0.28 + i * 0.09, rng.uniform(0.25, 0.9), 0.012) for i in range(7)]
    X = np.linspace(0, 1, 260); Y = np.zeros_like(X)
    for c_, a, s_ in P: Y += a * np.exp(-((X - c_) / s_) ** 2)
    n_ = int(clamp(k) * 259) + 1
    pts = np.array([(x0 + 18 + X[i] * (w - 36), y0 + h - 18 - Y[i] * (h - 60)) for i in range(n_)], np.int32)
    if n_ > 1: cv2.polylines(f, [pts], False, C(col), 5, cv2.LINE_AA)
    return x0 + 18 + 0.14 * (w - 36), y0 + h - 18 - spike * 0.62 * (h - 60)


def test_icon_el(kind, seed=181):
    """the seven defendants as mini ink icons (size ~ 120)."""
    def mk():
        w, h = 140, 140; im, d, S = _cv(w, h)
        if kind == "water":
            _tl_fill(im, lambda q, S_: q.polygon(S_(36, 50, 104, 50, 98, 124, 42, 124), fill=255), (176, 214, 236), (130, 184, 220), (214, 236, 248), (250, 254, 255), thick=10, hotamt=0.4)
            _ink_poly(d, [(30, 18), (110, 18), (100, 128), (40, 128)], None, seed, 5, amp=0.5); _ink_ell(d, 70, 48, 22, 11, GHEE, seed + 1, 3, n=14)
        elif kind == "palm":
            _ink_poly(d, [(40, 66), (102, 66), (98, 118), (46, 118)], INK_SKIN, seed, 5, amp=0.5)
            for i, x in enumerate((46, 62, 79, 95)): _ink_poly(d, [(x - 7, 70), (x - 7, 22 + abs(i - 1.5) * 8), (x + 7, 22 + abs(i - 1.5) * 8), (x + 7, 70)], INK_SKIN, seed + i, 4, amp=0.4)
            d.rectangle(S(43, 60, 100, 76), fill=INK_SKIN + (255,)); _ink_ell(d, 70, 92, 16, 9, GHEE, seed + 7, 3, n=12)
        elif kind == "smell":
            _ink_poly(d, [(62, 34), (84, 90), (100, 106), (78, 118), (52, 112), (50, 100)], INK_SKIN, seed, 5, amp=0.6)
            for x in (22, 36): d.arc(S(x, 30, x + 22, 72), 110, 250, fill=INKC + (255,), width=4 * SC3); d.arc(S(x, 72, x + 22, 112), 110, 250, fill=INKC + (255,), width=4 * SC3)
        elif kind == "colour":
            _ink_ell(d, 52, 72, 34, 38, GHEE, seed, 5, n=18); _ink_ell(d, 92, 72, 34, 38, (250, 246, 232), seed + 1, 5, n=18)
        elif kind == "iodine":
            _ink_poly(d, [(58, 28), (82, 28), (82, 46), (104, 62), (104, 124), (36, 124), (36, 62), (58, 46)], (136, 80, 30), seed, 5, amp=0.5); _ink_poly(d, [(46, 76), (94, 76), (94, 108), (46, 108)], (252, 244, 220), seed + 1, 3, amp=0.3)
        elif kind == "acid":
            _ink_poly(d, [(54, 16), (86, 16), (86, 100)] + _arcpts(70, 100, 16, 18, 0, 180, 8) + [(54, 100)], (250, 248, 240), seed, 5, amp=0.4); d.ellipse(S(57, 86, 83, 116), fill=(182, 22, 62, 255)); d.rectangle(S(57, 72, 83, 100), fill=(182, 22, 62, 255))
        elif kind == "fridge":
            _ink_poly(d, [(38, 12), (102, 12), (104, 128), (36, 128)], (232, 238, 240), seed, 5, amp=0.5); d.line(S(38, 48, 102, 48), fill=INKC + (255,), width=4 * SC3); d.line(S(48, 56, 48, 84), fill=INKC + (255,), width=5 * SC3); d.line(S(48, 24, 48, 38), fill=INKC + (255,), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("ticon25", kind, seed), mk)


BOARD = (("water", "WATER", "USELESS", RED_V), ("palm", "PALM", "USELESS", RED_V), ("smell", "SMELL", "FOOLED", RED_V), ("colour", "COLOUR", "FOOLED", RED_V),
         ("iodine", "IODINE", "ONLY STARCH", ACC_S), ("acid", "ACID", "ONLY SESAME", ACC_S), ("fridge", "FRIDGE", "A CLUE", GOOD))


def verdict_board(f, t, t0s, y0=500, gap=132, x_ic=170, x_n=262, x_v=600, cur=None, title=None, tv=None):
    """the verdicts as a list you can screenshot. A row appears at t0s[i], its stamp (optional) at tv[i]."""
    for i, (kind, nm, vd, col) in enumerate(BOARD):
        if i >= len(t0s) or t < t0s[i]: continue
        y = y0 + i * gap; k = pin(t, t0s[i], 0.18)
        if cur == i: cv2.rectangle(f, (92, int(y - gap * 0.46)), (988, int(y + gap * 0.46)), C((255, 240, 190)), -1, cv2.LINE_AA)
        comp(f, test_icon_el(kind), x_ic, y, scale=k * 0.86)
        comp(f, ed_el(nm, "", lead_col=INKC, lead_size=56), x_n, y, anchor="l", op=k)
        tv_ = (tv[i] if tv else t0s[i] + 0.12)
        if t >= tv_:
            q = 1.5 - 0.5 * eo(clamp((t - tv_) / 0.14)); rot_comp(f, stamp_el(vd, col, 44), x_v + 170, y, -3 + (i % 3) * 2, q, clamp((t - tv_) / 0.08), 0.0)


def _court_bg(top_y=1330):
    f = _vgrad((150, 108, 74), (118, 80, 52), 0, top_y)
    for x in range(-40, W + 200, 240):                                # wood panels
        cv2.rectangle(f, (x + 14, 860), (x + 226, 1280), C((132, 92, 60)), -1, cv2.LINE_AA); cv2.rectangle(f, (x + 14, 860), (x + 226, 1280), C((88, 58, 36)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (x + 34, 880), (x + 206, 1260), C((146, 104, 70)), 3, cv2.LINE_AA)
    cv2.rectangle(f, (0, 830), (W, 860), C((88, 58, 36)), -1, cv2.LINE_AA)
    for x in (130, 790):                                              # two tall windows with warm light
        cv2.rectangle(f, (x - 14, 256), (x + 174, 820), C((88, 58, 36)), -1, cv2.LINE_AA)
        f[270:806, x:x + 160] = _vgrad((252, 236, 196), (252, 214, 150), 270, 806)[270:806, x:x + 160]
        cv2.line(f, (x + 80, 270), (x + 80, 806), C((88, 58, 36)), 9, cv2.LINE_AA)
        for y in (400, 540, 680): cv2.line(f, (x, y), (x + 160, y), C((88, 58, 36)), 9, cv2.LINE_AA)
    cv2.circle(f, (540, 560), 150, C((88, 58, 36)), -1, cv2.LINE_AA); cv2.circle(f, (540, 560), 134, C((206, 170, 100)), -1, cv2.LINE_AA)   # a plain round plaque
    cv2.line(f, (540, 470), (540, 650), C((88, 58, 36)), 10, cv2.LINE_AA); cv2.line(f, (450, 505), (630, 505), C((88, 58, 36)), 10, cv2.LINE_AA)
    for sg in (-1, 1):
        cv2.ellipse(f, (540 + sg * 90, 575), (46, 26), 0, 0, 180, C((88, 58, 36)), -1, cv2.LINE_AA)
        cv2.line(f, (540 + sg * 90, 505), (540 + sg * 90 - 42, 575), C((88, 58, 36)), 4, cv2.LINE_AA); cv2.line(f, (540 + sg * 90, 505), (540 + sg * 90 + 42, 575), C((88, 58, 36)), 4, cv2.LINE_AA)
    return f


def set_court(t=0.0, blur=4, top_y=1330, dim=0.0):
    """THE COURTROOM: wood panels, two tall windows with warm sun, a plain round scales plaque behind the judge. bench_front AFTER Chubby: he sits behind the bench."""
    f = gcache(("set_court25", blur, top_y), lambda: np.clip(_soft(_court_bg(top_y), blur), 0, 1).astype(np.float32)).copy()
    for x in (210, 870): god_rays(f, x, 400, t, (255, 232, 180), 0.12, 6, 1300, 0.6, 1.35, 5)
    glow(f, 210, 520, 320, (255, 232, 180), 0.16); glow(f, 870, 520, 320, (255, 232, 180), 0.16)
    dust_motes(f, t, 120, 500, 980, 1200, 14, 9, 0.4)
    if dim > 0: f = f * (1 - dim) + f * np.array((0.35, 0.3, 0.42), np.float32) * dim
    return inkify(f, 0.1)


def bench_front(f, top_y=1250, plate=True):
    """the judge's bench: heavy dark wood with panels and a nameplate; fills the foreground down past the safe line."""
    def mk():
        g = np.zeros((H - top_y, W, 3), np.float32); g[:] = C(WOOD_D); h_ = H - top_y
        g[0:34] = C((150, 104, 66)); g[32:40] = C(INKC)
        for x in range(-30, W, 280):
            cv2.rectangle(g, (x + 16, 62), (x + 262, h_ - 10), C(WOOD), -1, cv2.LINE_AA); cv2.rectangle(g, (x + 16, 62), (x + 262, h_ - 10), C((54, 34, 22)), 5, cv2.LINE_AA)
            cv2.rectangle(g, (x + 34, 82), (x + 244, h_ - 30), C((96, 62, 38)), 3, cv2.LINE_AA)
        return g
    g = gcache(("bench25", top_y), mk)
    f[top_y:H] = g
    if plate:
        comp(f, chip("JUDGE CHUBBY", (246, 232, 190), INKC, 34), 540, top_y + 100)


def _store_bg():
    f = _vgrad((30, 30, 46), (20, 20, 32), 0, H)
    for y in (560, 880, 1200):
        cv2.rectangle(f, (40, y), (W - 40, y + 26), C((60, 52, 56)), -1, cv2.LINE_AA)
    return np.clip(_soft(f, 3), 0, 1).astype(np.float32)


def set_store(t=0.0):
    """a dark storeroom with empty shelves: a torch beam does the lighting (use spotlight or torch_beam)."""
    return gcache(("store25",), _store_bg).copy()


def torch_beam(f, x0, y0, x1, y1, r=240, amt=0.8, col=(255, 240, 200)):
    """a cone of torch light from (x0, y0) to a pool at (x1, y1): everything in it brightens."""
    m = np.zeros((H // 4, W // 4), np.float32); P = np.array([(x0 / 4, y0 / 4), ((x1 - r * 0.9) / 4, y1 / 4), ((x1 + r * 0.9) / 4, y1 / 4)], np.int32)
    cv2.fillConvexPoly(m, P, 0.5, cv2.LINE_AA); cv2.ellipse(m, (int(x1 / 4), int(y1 / 4)), (int(r / 4), int(r * 0.8 / 4)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    m = cv2.resize(cv2.GaussianBlur(m, (0, 0), 7), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
    f += m * amt * np.array(C(col), np.float32) * (0.35 + f)
    return m


def vstamp_el(text, col=None, size=70):
    """a verdict stamp on a cream slip, so it reads on any background (wood, dark store, pink room)."""
    col = col or RED_V
    def mk():
        fn = font(F_BLACK, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 64), int(size * 1.62); sc = 2
        im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(4, 4, w - 4, h - 4), 12 * sc, fill=(252, 247, 232, 240), outline=tuple(col) + (255,), width=8 * sc)
        d.text((w / 2 * sc, h / 2 * sc), text, font=fn, fill=tuple(col) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("vstamp25", text, col, size), mk)
