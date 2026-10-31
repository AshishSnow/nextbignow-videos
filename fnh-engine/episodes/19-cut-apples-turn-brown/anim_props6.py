# ================= anim_props6.py — FreshNestHub 19 "why do cut apples turn brown?" ink props (lib17 toolkit: _ink_poly / _ink_ell / _shade /
# _hatch_in / _face). ONE accent per video: APPLE RED = the apple skin, the 3D titles, the chips; the BROWNING itself is a sepia wash in the
# ink family (warm brown, never grey); MINT = the enzyme machine + the fixes; paper = the apple flesh / oxygen / the colourless stage.
# Props: apple_el (whole / cut half, browning 0..1 creeping in from the cut edge, optional face), slice_el (a wedge, browning + face),
# cell_el (one apple cell as a 'room' with a divider wall; broken 0..1 cracks it), ppo_el (the enzyme = a tiny mint machine with a funnel
# mouth; moods n / hungry / munch / sleepy / off), phenol_el (polyphenol bead), o2_el (oxygen twin-circle), melanin_el (blob that goes
# from colourless to brown as k grows), knife_ink_el + knife_ink_at, board_ink_el, lemon_ink_el (whole / half), honey_jar_el, bowl_el,
# lunchbox_el, sun_ink_el, food_el (tea / coffee / cocoa / avocado / banana / potato with browning), tan_patch (Chubby's tan stripe). =================
ACC = (214, 48, 54); ACC_S = (150, 26, 34); ACC_L = (240, 150, 150); ACC_XL = (250, 222, 220)         # apple red accent (overrides lib18 amber)
FLESH = (250, 240, 214); FLESH_S = (226, 210, 176)
BROWN = (150, 96, 54); BROWN_D = (96, 58, 30); BROWN_L = (204, 156, 104)
LEMON = (250, 230, 120); LEMON_S = (214, 184, 60)
MILK = (252, 248, 238); MILK_S = (228, 216, 192)
SCHEMES["applep"] = ((236, 222, 206), (250, 244, 232), (230, 214, 196), (0.78, 0.7, 0.6))
SCHEMES["cream2"] = ((240, 228, 206), (252, 246, 232), (232, 218, 192), (0.78, 0.72, 0.6))
SCHEMES["sepia"] = ((120, 82, 50), (190, 150, 104), (108, 72, 42), (0.45, 0.32, 0.2))
SCHEMES["mintp"] = ((170, 226, 206), (222, 246, 236), (150, 210, 190), (0.5, 0.75, 0.65))
SCHEMES["redp"] = ((190, 60, 64), (236, 130, 130), (176, 50, 56), (0.7, 0.25, 0.25))
SCHEMES["sunny"] = ((250, 206, 90), (255, 236, 170), (240, 190, 70), (0.9, 0.75, 0.3))


def _brown_wash(im, S, mask_fn, k, seed=3, col=BROWN, x0=0, y0=0, x1=300, y1=300, edge=None):
    """the browning: blotchy sepia patches that creep in from the edge (edge = (ex, ey, spread) centre of the spreading) as k grows."""
    if k <= 0: return
    rng = np.random.default_rng(seed)
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(lay)
    ex, ey, spread = edge or ((x0 + x1) / 2, y0, max(x1 - x0, y1 - y0))
    for i in range(60):
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1); r_ = rng.uniform(10, 34)
        dist = math.hypot(px - ex, py - ey) / spread
        a = clamp((k * 1.35 - dist) * 2.2)
        if a <= 0: continue
        c = tuple(int(a_ + (b_ - a_) * min(1, a * 1.2)) for a_, b_ in zip(BROWN_L, col))
        q.ellipse(S(px - r_, py - r_ * 0.8, px + r_, py + r_ * 0.8), fill=c + (int(110 + 120 * a),))
    lay = lay.filter(ImageFilter.GaussianBlur(4 * SC3))
    m = Image.new("L", im.size, 0); mask_fn(ImageDraw.Draw(m), S)
    im.alpha_composite(Image.composite(lay, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))


def apple_el(brown=0.0, cut=False, mood=None, look=(0, 0), seed=1, white=False, flesh=None):
    """an ink apple. cut=True = the cut half seen face-on (cream flesh, seed star); brown 0..1 = browning creeping over the flesh.
    white=True = the Arctic apple (a cut face that stays white, with a little snowflake mark)."""
    brown = round(clamp(brown) * 10) / 10
    def mk():
        w, h = 300, 320; im, d, S = _cv(w, h)
        body = [(150, 70), (196, 52), (240, 70), (268, 120), (266, 190), (236, 262), (190, 288), (150, 280), (110, 288), (64, 262), (34, 190), (32, 120), (60, 70), (104, 52)]
        if not cut:
            _ink_poly(d, body, ACC, seed + 1, INK_W, amp=2.2)
            _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255),
                   lambda q, S_, c: q.polygon(S_(170, 40, 290, 40, 290, 300, 200, 300, 186, 200), fill=c), ACC_S, 120)
            _hatch_in(im, (180, 60, 270, 290), lambda q, S_: q.polygon(S_(190, 60, 262, 90, 262, 200, 230, 270, 196, 284, 186, 200), fill=255), -40, 10, 34)
            d.ellipse(S(78, 92, 118, 136), fill=(255, 255, 255, 150))
            d.line(S(100, 100, 92, 140), fill=(255, 255, 255, 120), width=4 * SC3)
        else:
            _ink_poly(d, body, flesh or FLESH, seed + 1, INK_W, amp=2.2)
            sk = [(x + (6 if x > 150 else -6) * 0 , y) for x, y in body]
            d.line([(x * SC3, y * SC3) for x, y in _wob(body + [body[0]], 1.6, seed + 9)], fill=ACC + (255,), width=9 * SC3, joint="curve")   # thin red skin ring
            d.line([(x * SC3, y * SC3) for x, y in _wob(body + [body[0]], 1.6, seed + 9)], fill=INKC + (255,), width=3 * SC3, joint="curve")
            _hatch_in(im, (190, 70, 262, 280), lambda q, S_: q.polygon(S_(196, 80, 258, 120, 256, 200, 228, 262, 200, 272, 190, 200), fill=255), -40, 12, 22)
            # core + seeds
            d.polygon([(x * SC3, y * SC3) for x, y in _wob([(150, 110), (176, 150), (170, 200), (150, 236), (130, 200), (124, 150)], 1.2, seed + 4)], fill=(236, 222, 188, 255), outline=INKC + (150,), width=2 * SC3)
            for (px, py, a) in ((150, 150, 0), (140, 184, 20), (160, 184, -20)):
                d.ellipse(S(px - 7, py - 12, px + 7, py + 12), fill=BROWN_D + (255,), outline=INKC + (255,), width=2 * SC3)
            if brown > 0:
                _brown_wash(im, S, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), brown, seed + 7, BROWN, 40, 60, 262, 284, (150, 170, 150))
            if white:
                for a in range(0, 180, 60):
                    aa = math.radians(a); d.line(S(226 - 16 * math.cos(aa), 110 - 16 * math.sin(aa), 226 + 16 * math.cos(aa), 110 + 16 * math.sin(aa)), fill=(120, 170, 230, 255), width=3 * SC3)
        # stem + leaf
        d.line([(x * SC3, y * SC3) for x, y in _wob([(150, 64), (156, 30), (166, 14)], 1.0, seed + 5)], fill=INKC + (255,), width=7 * SC3, joint="curve")
        d.line([(x * SC3, y * SC3) for x, y in _wob([(150, 64), (156, 30), (166, 14)], 1.0, seed + 5)], fill=BROWN + (255,), width=3 * SC3, joint="curve")
        leaf = [(160, 36), (186, 18), (220, 18), (214, 40), (186, 52)]
        _ink_poly(d, leaf, INK_MINT, seed + 6, INK_W - 2, amp=1.2)
        d.line(S(166, 36, 212, 24), fill=INKC + (140,), width=2 * SC3)
        if mood: _face(d, S, 150 if not cut else 150, 160 if not cut else 96, 1.3 if not cut else 0.9, mood, look)
        return _done(im, w, h)
    return gcache(("apple19", brown, cut, mood, look, seed, white, flesh), mk)


def slice_el(brown=0.0, mood=None, look=(0, 0), seed=2, tint=None):
    """an apple SLICE for bowls / lunchboxes / close-ups = a cut half at 0.7 scale (the side-view wedge read as a bowl in the ep 19 test
    frames; the cut face with its seed star reads as 'apple' instantly). tint = flesh colour (lemon / honey coat)."""
    return gcache(("slice19", brown, mood, look, seed, tint), lambda: scale_el(apple_el(brown, True, mood, look, seed, False, tint), 0.7))


# ---------------- the apple CELL: one room, a divider wall, two corners ----------------
def cell_el(broken=0.0, divider=True, seed=3, w=640, h=400):
    """one apple cell seen as a ROOM: a thick wobbly ink wall with a pale inside, an inner divider wall splitting it into two corners.
    broken 0..1 cracks the wall and breaks the divider into pieces (the knife went through)."""
    broken = round(clamp(broken) * 6) / 6
    def mk():
        im, d, S = _cv(w, h)
        room = [(40, 60), (w - 40, 40), (w - 30, h - 40), (30, h - 50)]
        _ink_poly(d, room, (244, 236, 212), seed, INK_W + 4, amp=3.0)
        d.polygon([(x * SC3, y * SC3) for x, y in _wob([(58, 76), (w - 58, 58), (w - 48, h - 58), (48, h - 66)], 2.0, seed + 1)], fill=(250, 244, 226, 255))
        _hatch_in(im, (w - 120, 60, w - 40, h - 50), lambda q, S_: q.polygon(S_(w - 110, 60, w - 48, 60, w - 48, h - 58, w - 100, h - 58), fill=255), -40, 12, 20)
        if divider:
            k = broken
            segs = 6
            for i in range(segs):
                if k > 0 and (i % 2 == 1 or k > 0.6): continue
                y0_ = 60 + i * (h - 110) / segs; y1_ = 60 + (i + 1) * (h - 110) / segs
                jit = 14 * k * math.sin(i * 2.1)
                d.line([(x * SC3, y * SC3) for x, y in _wob([(w / 2 + jit, y0_ + 4), (w / 2 + jit, y1_ - 4)], 1.5, seed + 10 + i)], fill=INKC + (255,), width=12 * SC3)
                d.line([(x * SC3, y * SC3) for x, y in _wob([(w / 2 + jit, y0_ + 4), (w / 2 + jit, y1_ - 4)], 1.5, seed + 10 + i)], fill=(226, 206, 160, 255), width=6 * SC3)
        if broken > 0:
            for (cx_, cy_, ang) in ((44, h * 0.35, 0), (w - 36, h * 0.6, 180), (w * 0.62, 50, 90), (w * 0.32, h - 46, 270), (w * 0.5, 50, 100)):
                L = 90 * clamp(broken * 1.4); a = math.radians(ang); P = [(cx_, cy_)]
                for kk in range(5): P.append((P[-1][0] + L / 5 * math.cos(a) + 12 * (-1) ** kk * math.sin(a), P[-1][1] + L / 5 * math.sin(a) + 12 * (-1) ** kk * math.cos(a)))
                d.line([(x * SC3, y * SC3) for x, y in P], fill=INKC + (255,), width=7 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("cell19", broken, divider, seed, w, h), mk)


def ppo_el(mood="n", look=(0, 0), seed=1, s_=1.0):
    """PPO, the enzyme: a tiny MINT machine — a rounded body with a funnel mouth on the right, two rivets, a little chimney, and a face.
    moods: n, hungry (tongue out), munch, happy, sleepy (sluggish: heavy lids + zz), off (switched off: X eyes, grey)."""
    def mk():
        w, h = 200, 170; im, d, S = _cv(w, h)
        col = INK_MINT if mood != "off" else (190, 196, 196); cols = INK_MINT_S if mood != "off" else (150, 156, 156)
        body = [(30, 60), (130, 50), (150, 70), (150, 130), (130, 150), (30, 146), (16, 120), (16, 80)]
        _ink_poly(d, body, col, seed + 20, INK_W - 1, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.polygon(S_(100, 40, 160, 40, 160, 160, 110, 160, 96, 100), fill=c), cols, 110)
        _hatch_in(im, (100, 50, 150, 150), lambda q, S_: q.polygon(S_(104, 54, 148, 70, 148, 130, 126, 148, 108, 148, 98, 100), fill=255), -40, 8, 34)
        # funnel mouth on the right
        _ink_poly(d, [(148, 78), (190, 62), (190, 128), (148, 112)], (232, 240, 236) if mood != "off" else (210, 214, 214), seed + 21, INK_W - 2, amp=1.4)
        d.line(S(156, 84, 184, 72), fill=INKC + (120,), width=2 * SC3); d.line(S(156, 106, 184, 118), fill=INKC + (120,), width=2 * SC3)
        # chimney + rivets
        _ink_poly(d, [(50, 54), (74, 54), (72, 26), (52, 26)], cols, seed + 22, INK_W - 2, amp=1.0)
        for (rx, ry) in ((30, 72), (30, 134), (128, 140)): d.ellipse(S(rx - 5, ry - 5, rx + 5, ry + 5), fill=INKC + (200,))
        if mood == "off":
            for sgn in (-1, 1):
                x = 82 + sgn * 20
                d.line(S(x - 9, 88, x + 9, 106), fill=INKC + (255,), width=4 * SC3); d.line(S(x + 9, 88, x - 9, 106), fill=INKC + (255,), width=4 * SC3)
            d.line([(x * SC3, y * SC3) for x, y in _arcpts(82, 126, 14, 8, 200, 340, 10)], fill=INKC + (255,), width=4 * SC3, joint="curve")
        else:
            _face(d, S, 82, 100, 1.0, "hungry" if mood == "hungry" else mood, look)
            if mood == "sleepy":
                for sgn in (-1, 1):
                    x = 82 + sgn * 16; d.rectangle(S(x - 9, 80, x + 9, 96), fill=col + (255,)); d.line(S(x - 8, 96, x + 8, 96), fill=INKC + (255,), width=3 * SC3)
                d.text((150 * SC3, 30 * SC3), "z", font=font(F_BLACK, 22 * SC3), fill=INKC + (255,), anchor="mm"); d.text((170 * SC3, 14 * SC3), "z", font=font(F_BLACK, 16 * SC3), fill=INKC + (255,), anchor="mm")
        return _done(im, w, h)
    el = gcache(("ppo19", mood, look, seed), mk)
    return el if s_ == 1.0 else scale_el(el, s_)


def phenol_el(mood="n", look=(0, 0), seed=1):
    """a polyphenol bead: paper-pink round bead with a face (the apple's flavour chemical)."""
    def mk():
        w, h = 100, 100; im, d, S = _cv(w, h)
        _ink_ell(d, 50, 52, 36, 34, ACC_XL, seed + 30, INK_W - 2, n=22, amp=2.0)
        _shade(im, lambda q, S_: q.ellipse(S_(14, 18, 86, 86), fill=255), lambda q, S_, c: q.ellipse(S_(44, 28, 100, 100), fill=c), ACC_L, 80)
        d.ellipse(S(28, 28, 40, 38), fill=(255, 255, 255, 220))
        _face(d, S, 50, 54, 0.8, mood, look)
        return _done(im, w, h)
    return gcache(("phenol19", mood, look, seed), mk)


def o2_el(seed=1, mood=None):
    """oxygen: two joined paper circles with an ink outline and 'O2'."""
    def mk():
        w, h = 130, 80; im, d, S = _cv(w, h)
        for cx_ in (42, 88): _ink_ell(d, cx_, 40, 30, 30, (240, 246, 250), seed + 40 + cx_, INK_W - 2, n=20, amp=1.4)
        d.ellipse(S(28, 24, 40, 34), fill=(255, 255, 255, 230))
        d.text((65 * SC3, 40 * SC3), "O2", font=font(F_BLACK, 24 * SC3), fill=INKC + (255,), anchor="mm")
        if mood: _face(d, S, 88, 42, 0.6, mood)
        return _done(im, w, h)
    return gcache(("o2_19", seed, mood), mk)


def melanin_el(k=1.0, seed=1, r=60):
    """the browning product: a lumpy blob. k 0..0.35 = colourless (paper, dotted outline), then it darkens to sepia brown and grows."""
    k = round(clamp(k) * 10) / 10
    def mk():
        R = r * (0.6 + 0.6 * k); w = h = int(2 * R + 60); im, d, S = _cv(w, h); cx = cy = w / 2
        rng = np.random.default_rng(seed)
        pts = [(cx + R * (1 + 0.16 * math.sin(i * 1.7 + rng.uniform(0, 1))) * math.cos(i * 2 * math.pi / 14), cy + R * (1 + 0.16 * math.cos(i * 2.3)) * math.sin(i * 2 * math.pi / 14)) for i in range(14)]
        c = clamp((k - 0.3) / 0.7)
        fill = tuple(int(a + (b - a) * c) for a, b in zip((250, 246, 236), BROWN))
        _ink_poly(d, pts, fill, seed + 50, INK_W - 2 if c > 0.2 else INK_W - 4, amp=2.4, col=INKC if c > 0.2 else (120, 110, 100))
        if c > 0.3:
            _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts], fill=255), lambda q, S_, c_: q.ellipse(S_(cx - R * 0.2, cy - R * 0.1, cx + R * 1.3, cy + R * 1.3), fill=c_), BROWN_D, int(120 * c))
            _hatch_in(im, (cx, cy, cx + R * 1.3, cy + R * 1.3), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts], fill=255), -40, 9, int(40 * c))
        d.ellipse(S(cx - R * 0.5, cy - R * 0.55, cx - R * 0.2, cy - R * 0.3), fill=(255, 255, 255, 120 + int(80 * c)))
        return _done(im, w, h)
    return gcache(("melanin19", k, seed, r), mk)


# ---------------- kitchen things in ink ----------------
KN19_W, KN19_H, KN19_GRIP = 520, 110, 70


def knife_ink_el():
    def mk():
        w, h = KN19_W, KN19_H; im, d, S = _cv(w, h)
        _ink_poly(d, [(150, 30), (470, 32), (514, 56), (490, 92), (150, 92)], (232, 234, 238), 61, INK_W - 1, amp=1.4)
        _hatch_in(im, (160, 60, 490, 92), lambda q, S_: q.polygon(S_(160, 66, 486, 66, 480, 90, 160, 90), fill=255), -40, 8, 26)
        d.line(S(160, 40, 450, 42), fill=(255, 255, 255, 200), width=4 * SC3)
        _ink_poly(d, [(14, 40), (156, 40), (156, 84), (14, 84)], BROWN_D, 62, INK_W - 1, amp=1.2)
        for x in (50, 100): d.ellipse(S(x - 6, 56, x + 6, 68), fill=(220, 222, 230, 255), outline=INKC + (255,), width=2 * SC3)
        return _done(im, w, h)
    return gcache("knife19", mk)


def knife_ink_at(f, gx, gy, ang, s=1.0, op=1.0):
    """draw the ink knife so its grip sits at (gx, gy); ang = degrees CCW (0 = blade pointing right, edge down)."""
    dx = (KN19_W / 2 - KN19_GRIP) * s; dy = (KN19_H / 2 - 62) * s; a = math.radians(ang)
    cx = gx + dx * math.cos(a) + dy * math.sin(a); cy = gy - dx * math.sin(a) + dy * math.cos(a)
    rot_comp(f, scale_el(knife_ink_el(), s), cx, cy, ang, 1.0, op, 0.25)


def board_ink_el(w_=640):
    def mk():
        w, h = w_, 110; im, d, S = _cv(w, h)
        _ink_poly(d, [(10, 44), (w - 10, 44), (w - 10, 100), (10, 100)], (190, 130, 70), 71, INK_W - 1, amp=1.6)
        _ink_poly(d, [(10, 12), (w - 10, 12), (w - 10, 56), (10, 56)], (226, 176, 110), 72, INK_W - 1, amp=1.6)
        for k in range(5): d.line([(x * SC3, y * SC3) for x, y in _arcpts(80 + 110 * k, 30, 46, 16, 200, 340, 8)], fill=INKC + (90,), width=2 * SC3, joint="curve")
        _hatch_in(im, (10, 60, w - 10, 100), lambda q, S_: q.rectangle(S_(14, 62, w - 14, 98), fill=255), -40, 10, 24)
        return _done(im, w, h)
    return gcache(("board19", w_), mk)


def lemon_ink_el(half=False, seed=1):
    def mk():
        w, h = 220, 170; im, d, S = _cv(w, h)
        body = _arcpts(110, 85, 84, 62, 0, 360, 26)[:-1]
        body = [(x + (14 if i in (0, 25, 1) else (-14 if 12 <= i <= 14 else 0)) * (1 if x > 110 else -1) * 0, y) for i, (x, y) in enumerate(body)]
        _ink_poly(d, body, LEMON, seed + 80, INK_W - 1, amp=2.0)
        _ink_ell(d, 24, 85, 12, 9, LEMON, seed + 81, INK_W - 3, n=12); _ink_ell(d, 196, 85, 12, 9, LEMON, seed + 82, INK_W - 3, n=12)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.ellipse(S_(110, 40, 210, 160), fill=c), LEMON_S, 100)
        _hatch_in(im, (130, 50, 194, 140), lambda q, S_: q.ellipse(S_(120, 46, 196, 146), fill=255), -40, 9, 26)
        if half:
            _ink_ell(d, 110, 85, 62, 48, (252, 244, 190), seed + 83, INK_W - 2, n=24)
            for a in range(0, 360, 45):
                aa = math.radians(a); d.line(S(110, 85, 110 + 56 * math.cos(aa), 85 + 42 * math.sin(aa)), fill=INKC + (150,), width=2 * SC3)
            d.ellipse(S(102, 79, 118, 91), fill=(252, 244, 190, 255), outline=INKC + (200,), width=2 * SC3)
        else:
            d.ellipse(S(60, 46, 96, 66), fill=(255, 255, 255, 150))
        return _done(im, w, h)
    return gcache(("lemon19", half, seed), mk)


def honey_jar_el():
    def mk():
        w, h = 180, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(50, 40), (130, 40), (130, 64), (150, 80), (150, 196), (30, 196), (30, 80), (50, 64)], (240, 176, 60), 91, INK_W - 1, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(S_(50, 40, 130, 40, 130, 64, 150, 80, 150, 196, 30, 196, 30, 80, 50, 64), fill=255), lambda q, S_, c: q.rectangle(S_(110, 30, 160, 210), fill=c), (196, 130, 30), 110)
        _hatch_in(im, (116, 80, 150, 196), lambda q, S_: q.rectangle(S_(118, 82, 148, 194), fill=255), -40, 8, 30)
        _ink_poly(d, [(44, 20), (136, 20), (136, 44), (44, 44)], BROWN_D, 92, INK_W - 2, amp=1.0)
        d.rounded_rectangle(S(52, 100, 128, 150), 6 * SC3, fill=MILK + (255,), outline=INKC + (255,), width=3 * SC3)
        d.text((90 * SC3, 125 * SC3), "HONEY", font=font(F_BLACK, 18 * SC3), fill=INKC + (255,), anchor="mm")
        d.line(S(42, 86, 40, 186), fill=(255, 255, 255, 170), width=5 * SC3)
        return _done(im, w, h)
    return gcache("honey19", mk)


def bowl_el(level=0.6, tint=None, seed=1):
    """a glass bowl of water (optionally tinted: lemon water / honey water) seen from the front, cut-away."""
    level = round(clamp(level) * 4) / 4
    def mk():
        w, h = 360, 220; im, d, S = _cv(w, h)
        bowl = [(20, 40), (340, 40), (300, 190), (60, 190)]
        d.polygon([(x * SC3, y * SC3) for x, y in bowl], fill=(236, 244, 250, 255))
        if level > 0:
            ym = 190 - 140 * level; k = (190 - ym) / 150
            xl = 60 - 40 * k; xr = 300 + 40 * k
            d.polygon([(x * SC3, y * SC3) for x, y in [(xl, ym), (xr, ym), (300, 190), (60, 190)]], fill=(tint or (206, 228, 236)) + (230,))
            d.line([(x * SC3, y * SC3) for x, y in _wob([(xl, ym), (xr, ym)], 1.2, seed + 3)], fill=INKC + (200,), width=3 * SC3)
        _ink_poly(d, bowl, None, seed + 100, INK_W - 1, amp=1.6)
        d.line(S(80, 60, 70, 170), fill=(255, 255, 255, 200), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("bowl19", level, tint, seed), mk)


def lunchbox_el(open_=True, brown=0.0, n=3):
    """a lunchbox (mint, ink) with apple slices inside; brown 0..1 browns them."""
    brown = round(clamp(brown) * 4) / 4
    def mk():
        w, h = 420, 300; im, d, S = _cv(w, h)
        _ink_poly(d, [(30, 150), (390, 150), (390, 280), (30, 280)], INK_MINT, 111, INK_W, amp=1.8)
        _shade(im, lambda q, S_: q.rectangle(S_(30, 150, 390, 280), fill=255), lambda q, S_, c: q.rectangle(S_(300, 140, 400, 290), fill=c), INK_MINT_S, 110)
        _hatch_in(im, (300, 150, 390, 280), lambda q, S_: q.rectangle(S_(304, 154, 386, 276), fill=255), -40, 10, 30)
        d.rectangle(S(40, 160, 380, 200), fill=(250, 246, 234, 255))
        if open_:
            _ink_poly(d, [(30, 150), (390, 150), (380, 30), (40, 30)], INK_MINT_S, 112, INK_W, amp=1.8)
            d.rectangle(S(60, 50, 360, 130), fill=(226, 240, 234, 255), outline=INKC + (180,), width=2 * SC3)
        return _done(im, w, h)
    el = gcache(("lunchbox19", open_), mk)
    return el


def lunchbox(f, x, y, t, brown=0.0, n=3, s=1.0, open_=True):
    comp(f, scale_el(lunchbox_el(open_), s), x, y)
    for i in range(n):
        comp(f, scale_el(slice_el(brown, None, (0, 0), 2 + i), 0.55 * s), x + (i - (n - 1) / 2) * 100 * s, y + 40 * s + 2 * math.sin(t * 3 + i))


def sun_ink_el(mood=None):
    def mk():
        w = h = 240; im, d, S = _cv(w, h)
        for i in range(12):
            a = i * math.pi / 6; d.line([(x * SC3, y * SC3) for x, y in _wob([(120 + 84 * math.cos(a), 120 + 84 * math.sin(a)), (120 + 112 * math.cos(a), 120 + 112 * math.sin(a))], 1.5, 120 + i)], fill=INKC + (255,), width=5 * SC3)
        _ink_ell(d, 120, 120, 70, 70, LEMON, 121, INK_W, n=30, amp=2.0)
        _hatch_in(im, (140, 90, 190, 190), lambda q, S_: q.pieslice(S_(50, 50, 190, 190), -40, 110, fill=255), -40, 10, 24)
        if mood: _face(d, S, 120, 122, 1.2, mood)
        return _done(im, w, h)
    return gcache(("sun19", mood), mk)


def food_el(kind="tea", brown=1.0, seed=1):
    """little ink foods for the 'on purpose' + 'same trick' lists: tea (cup of black tea + leaf), coffee (bean), cocoa (pod), avocado (half),
    banana, potato (cut). brown 0..1 = how browned the cut face is (avocado / banana / potato)."""
    brown = round(clamp(brown) * 4) / 4
    def mk():
        w, h = 240, 200; im, d, S = _cv(w, h)
        if kind == "tea":
            _ink_poly(d, [(50, 70), (190, 70), (176, 170), (64, 170)], MILK, seed + 130, INK_W - 1, amp=1.6)
            d.polygon([(x * SC3, y * SC3) for x, y in [(60, 86), (180, 86), (170, 164), (70, 164)]], fill=BROWN + (255,))
            d.ellipse(S(60, 76, 180, 96), fill=BROWN_L + (255,), outline=INKC + (200,), width=2 * SC3)
            d.line([(x * SC3, y * SC3) for x, y in _arcpts(206, 110, 28, 36, -90, 90, 10)], fill=INKC + (255,), width=6 * SC3, joint="curve")
            _ink_poly(d, [(30, 40), (60, 20), (90, 36), (62, 60)], INK_MINT, seed + 131, INK_W - 3, amp=1.0)
        elif kind == "coffee":
            body = _arcpts(120, 100, 60, 84, 0, 360, 24)[:-1]
            _ink_poly(d, body, BROWN_D, seed + 132, INK_W - 1, amp=2.0)
            d.line([(x * SC3, y * SC3) for x, y in _wob([(120, 26), (108, 60), (126, 100), (112, 140), (120, 176)], 1.2, seed + 133)], fill=INKC + (255,), width=5 * SC3, joint="curve")
            d.ellipse(S(88, 50, 104, 70), fill=(255, 255, 255, 110))
        elif kind == "cocoa":
            body = [(70, 30), (160, 26), (200, 60), (204, 140), (170, 180), (90, 182), (40, 140), (36, 70)]
            _ink_poly(d, body, (214, 130, 40), seed + 134, INK_W - 1, amp=2.0)
            for k in range(4): d.line([(x * SC3, y * SC3) for x, y in _wob([(60 + k * 36, 40), (56 + k * 38, 176)], 1.0, seed + 140 + k)], fill=INKC + (140,), width=3 * SC3, joint="curve")
            _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.rectangle(S_(140, 20, 220, 200), fill=c), (160, 90, 24), 100)
        elif kind == "avocado":
            body = [(120, 20), (160, 40), (200, 100), (196, 160), (150, 188), (90, 188), (44, 160), (40, 100), (80, 40)]
            _ink_poly(d, body, (90, 130, 60), seed + 135, INK_W - 1, amp=2.0)
            inner = [(120, 40), (150, 56), (182, 104), (178, 154), (148, 174), (92, 174), (62, 154), (58, 104), (90, 56)]
            d.polygon([(x * SC3, y * SC3) for x, y in _wob(inner, 1.4, seed + 136)], fill=(200, 216, 120, 255))
            _brown_wash(im, S, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in inner], fill=255), brown, seed + 137, (124, 100, 60), 58, 40, 182, 174, (120, 40, 170))
            _ink_ell(d, 120, 124, 34, 36, BROWN, seed + 138, INK_W - 2, n=18)
        elif kind == "banana":
            body = [(30, 60), (70, 40), (130, 44), (190, 70), (214, 110), (200, 126), (150, 120), (90, 110), (50, 100)]
            _ink_poly(d, body, LEMON, seed + 139, INK_W - 1, amp=2.0)
            _brown_wash(im, S, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), brown, seed + 141, (110, 76, 40), 30, 40, 214, 126, (40, 60, 220))
            d.line([(x * SC3, y * SC3) for x, y in _wob([(40, 70), (120, 66), (196, 92)], 1.0, seed + 142)], fill=INKC + (120,), width=3 * SC3, joint="curve")
        else:                                                                                    # potato, cut
            body = _arcpts(120, 100, 86, 64, 0, 360, 22)[:-1]
            _ink_poly(d, body, (214, 180, 120), seed + 143, INK_W - 1, amp=2.6)
            d.polygon([(x * SC3, y * SC3) for x, y in _arcpts(120, 100, 66, 46, 0, 360, 22)], fill=(250, 240, 200, 255))
            _brown_wash(im, S, lambda q, S_: q.ellipse(S_(54, 54, 186, 146), fill=255), brown, seed + 144, (140, 110, 70), 54, 54, 186, 146, (120, 54, 160))
            for k in range(5): d.ellipse(S(50 + (k * 47) % 140, 40 + (k * 31) % 120, 56 + (k * 47) % 140, 46 + (k * 31) % 120), fill=INKC + (90,))
        return _done(im, w, h)
    return gcache(("food19", kind, brown, seed), mk)


def tan_patch(f, x, y, w, h, k, seed=1):
    """a tan stripe on Chubby (k 0..1 = how dark) drawn as a soft sepia wash over his skin (use on the face / arm area)."""
    if k <= 0.01: return
    m = np.zeros((H, W), np.float32)
    cv2.ellipse(m, (int(x), int(y)), (int(w / 2), int(h / 2)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    m = cv2.GaussianBlur(m, (0, 0), 12) * 0.45 * k
    f[:] = f * (1 - m[..., None]) + f * np.array(C((196, 120, 70)), np.float32) * m[..., None] * 1.1


def spread_edge(f, x0, y0, x1, y1, k, t, col=BROWN):
    """the browning front creeping across a flesh area in the FRAME (live, not cached): blotches that fade in with k (0..1)."""
    if k <= 0: return
    rng = np.random.default_rng(7); ov = f.copy()
    for i in range(40):
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1); r_ = rng.uniform(14, 40)
        a = clamp((k * 1.3 - abs(px - (x0 + x1) / 2) / (x1 - x0) * 1.6) * 2)
        if a <= 0: continue
        cv2.ellipse(ov, (int(px), int(py)), (int(r_), int(r_ * 0.7)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6)
    f[:] = f * (1 - 0.6 * k) + ov * 0.6 * k
