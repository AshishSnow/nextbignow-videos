# ================= anim_props_lib24.py (ep 24, 5 Nov): PANEER + IODINE ink props, the live STAIN + the STARCH SPRING, the DOOR GUARD metaphor, the DINER place.
# ONE accent per video: STARCH BLUE (blue-black) = the reaction, titles, chips. AMBER = iodine itself / oil (the story's other colour: it means 'nothing happened').
# paneer_el(mood, look, blue, oil, stache), tikka_el, packet_el(s), menu_el, buffalo_el, bottle_el(mood, cap=guard), oil_bottle_el, oil_drop_el(mood, ghost), iod_drop_el, dropper_el + dropper_at, milk_can_el,
# flask_el, microscope_el, article_el, door_el(open_), hearts. Live: stain(f, x, y, rx, ry, k, col, seed), net_catch(f, cx, cy, w, h, k, t), helix(f, cx, cy, L, coil, t, lit, beads) (a chain that coils into a spring; iodine lines up inside it),
# light_in_out(f, ...), phone_frame(f, cx, cy, w, h) -> screen box, guard_post(f, t, ...), waiter(...) bow tie. Places: set_diner(t) + diner_front(f, top_y).
ACC = (66, 74, 186); ACC_S = (38, 42, 118); ACC_L = (176, 186, 244); ACC_XL = (226, 230, 252)
IOD = (164, 96, 30); IOD_S = (110, 60, 18); IOD_L = (222, 160, 80)
PAN = (254, 248, 230); PAN_S = (232, 218, 182); OILC = (244, 204, 72); OIL_S = (190, 140, 30)
GOOD = (54, 140, 96)


def paneer_el(mood=None, look=(0, 0), blue=0.0, oil=False, stache=False, seed=41):
    """a block of paneer in 3/4 view: a front face, a top face and a side face, crumbly + a little spongy. blue 0..1 = a stain baked on the top face. stache = the lookalike's disguise. oil = an amber sheen + drops."""
    def mk():
        w, h = 300, 240; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        fr, tp, sd = ((252, 236, 180), (255, 246, 206), (232, 208, 150)) if oil else (PAN, (255, 253, 244), PAN_S)
        A, B_, C_, D_ = (24, 96), (66, 30), (276, 30), (234, 96)
        _ink_poly(d, [D_, C_, (276, 166), (234, 226)], sd, seed + 2, INK_W - 1, amp=1.0)
        _ink_poly(d, [A, B_, C_, D_], tp, seed + 1, INK_W - 1, amp=1.0)
        _ink_poly(d, [A, D_, (234, 226), (24, 226)], fr, seed, INK_W - 1, amp=1.2)
        for i in range(70):
            x, y = rng.uniform(36, 222), rng.uniform(106, 216); r_ = rng.uniform(1.2, 3.6); d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(232, 216, 176, 255))
        for i in range(34):
            k_ = rng.uniform(0.1, 0.9); x, y = rng.uniform(70, 240) + (1 - k_) * 0, 40 + 48 * k_; r_ = rng.uniform(1.2, 2.8); d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(240, 228, 196, 255))
        _hatch_in(im, (234, 40, 276, 226), lambda q, S_: q.polygon(S_(234, 96, 276, 30, 276, 166, 234, 226), fill=255))
        if oil:
            for (x, y, r_) in ((50, 130, 11), (214, 200, 9), (110, 60, 8), (210, 54, 7)):
                _ink_ell(d, x, y, r_, r_ * 1.15, OILC, seed + int(x), 3, n=12, amp=0.6); d.ellipse(S(x - r_ * 0.4, y - r_ * 0.5, x, y - r_ * 0.1), fill=(255, 255, 255, 230))
        if blue > 0:
            pts = _arcpts(150, 63, 74 * blue, 25 * blue, 0, 360, 24)[:-1]
            _ink_poly(d, pts, ACC_S, seed + 3, 0, amp=3.0, col=ACC_S)
        if mood: _face(d, S, 128, 152, 1.05, mood, look)
        if stache:
            cx, cy = 128, 180
            for sg in (-1, 1): _ink_poly(d, [(cx, cy - 6), (cx + sg * 30, cy - 14), (cx + sg * 52, cy - 2), (cx + sg * 34, cy + 8), (cx, cy + 4)], (70, 46, 34), seed + 5 + sg, 3, amp=0.8)
        return _done(im, w, h)
    return gcache(("paneer24b", mood, look, round(blue, 2), oil, stache, seed), mk)


def top_of(x, y, s):
    """centre + half-axes of a paneer_el's top face when it is drawn at (x, y) with scale s."""
    return x, y - 57 * s, 86 * s, 30 * s


def stain(f, x, y, rx, ry, k, col=None, seed=3, op=0.96, core=None):
    """a LIVE stain spreading through a surface (k 0..1): a wobbly blob with fingers + a dark core. Use on any 'it spreads' moment."""
    if k <= 0: return
    col = col or ACC_S; rng = np.random.default_rng(seed); ph = rng.uniform(0, 6, 5); n = 56
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    w = 1 + 0.16 * np.sin(3 * a + ph[0]) + 0.1 * np.sin(5 * a + ph[1]) + 0.07 * np.sin(9 * a + ph[2]) * k
    kk = k ** 0.7
    P = np.stack([x + rx * kk * w * np.cos(a), y + ry * kk * w * np.sin(a)], 1).astype(np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [P], C(col), cv2.LINE_AA)
    Q = np.stack([x + 0.55 * rx * kk * w * np.cos(a + 0.4), y + 0.55 * ry * kk * w * np.sin(a + 0.4)], 1).astype(np.int32)
    cv2.fillPoly(ov, [Q], C(core or _mix(col, (10, 10, 30), 0.35)), cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op


def iod_drop_el(mood=None, s=1.0, seed=2, col=None):
    def mk():
        w, h = 90, 130; im, d, S = _cv(w, h); c = col or IOD
        P = [(45, 8)] + _arcpts(45, 82, 34, 36, -35, 215, 18)
        _ink_poly(d, P, c, seed, INK_W - 2, amp=0.8)
        d.arc(S(24, 62, 56, 104), 110, 200, fill=(255, 240, 210, 220), width=5 * SC3)
        if mood: _face(d, S, 45, 84, 0.72, mood, (0, 0))
        return _done(im, w, h)
    return gcache(("iod24", mood, seed, col), mk)


def dropper_el(squeeze=0.0, fill=0.7):
    def mk():
        w, h = 130, 360; im, d, S = _cv(w, h)
        _ink_poly(d, [(58, 342), (72, 342), (82, 130), (48, 130)], (232, 240, 240), 3, INK_W - 2, amp=0.5)
        yl = 340 - 210 * fill
        d.polygon(S(60, 338, 70, 338, 79, 134 + (340 - yl) * 0 + 0, 51, 134) if False else S(60, 338, 70, 338, 72 + 8 * fill, yl, 58 - 8 * fill, yl), fill=IOD + (255,))
        rx = 44 - 9 * squeeze
        _ink_ell(d, 65, 74, rx, 58 + 6 * squeeze, (82, 56, 50), 4, INK_W - 1, n=20, amp=1.0)
        d.rectangle(S(38, 118, 92, 136), fill=(60, 42, 38, 255), outline=INKC + (255,), width=3 * SC3)
        d.arc(S(38, 34, 70, 90), 150, 240, fill=(170, 130, 120, 255), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("dropper24", round(squeeze, 1), round(fill, 1)), mk)


def dropper_at(f, x, y, s=1.0, squeeze=0.0, fill=0.7, rot=0.0):
    """(x, y) = the tip."""
    el = scale_el(dropper_el(squeeze, fill), s); a = math.radians(rot)
    rot_comp(f, el, x + 170 * s * math.sin(a), y - 170 * s * math.cos(a), rot, 1.0, 1.0, 0.0)


def bottle_el(mood=None, look=(0, 0), cap=False, seed=6, salute=False):
    """the brown iodine bottle; cap=True = the door guard (peaked cap + face on the label)."""
    def mk():
        w, h = 300, 470; im, d, S = _cv(w, h)
        _ink_poly(d, [(110, 96), (190, 96), (190, 140), (244, 186), (244, 430), (56, 430), (56, 186), (110, 140)], (136, 80, 30), seed, INK_W)
        _shade(im, lambda q, S_: q.rectangle(S_(56, 96, 244, 430), fill=255), lambda q, S_, c: q.rectangle(S_(180, 90, 260, 440), fill=c), (70, 36, 10), 110)
        d.arc(S(70, 190, 150, 400), 120, 230, fill=(226, 170, 110, 255), width=6 * SC3)
        _ink_poly(d, [(72, 236), (228, 236), (228, 382), (72, 382)], (252, 244, 220), seed + 1, INK_W - 2, amp=1.0)
        if cap:
            _ink_poly(d, [(58, 60), (242, 60), (216, 98), (84, 98)], (50, 60, 110), seed + 2, INK_W)
            _ink_ell(d, 150, 52, 100, 34, (62, 74, 134), seed + 3, INK_W, n=24)
            d.polygon(S(70, 92, 230, 92, 262, 118, 38, 118), fill=(30, 30, 50, 255), outline=INKC + (255,))
            d.rectangle(S(136, 28, 164, 58), fill=(240, 200, 80, 255), outline=INKC + (255,), width=3 * SC3)
        else:
            _ink_poly(d, [(112, 40), (188, 40), (188, 98), (112, 98)], (62, 44, 40), seed + 2, INK_W)
        if mood: _face(d, S, 150, 306, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("bottle24", mood, look, cap, seed), mk)


def oil_bottle_el(seed=7):
    def mk():
        w, h = 260, 480; im, d, S = _cv(w, h)
        _ink_poly(d, [(100, 66), (160, 66), (160, 120), (214, 190), (214, 450), (46, 450), (46, 190), (100, 120)], OILC, seed, INK_W)
        d.arc(S(60, 200, 130, 420), 120, 230, fill=(255, 250, 210, 255), width=7 * SC3)
        _hatch_in(im, (150, 200, 214, 440), lambda q, S_: q.rectangle(S_(150, 200, 214, 440), fill=255))
        _ink_poly(d, [(96, 22), (164, 22), (164, 66), (96, 66)], (200, 60, 40), seed + 1, INK_W)
        _ink_poly(d, [(58, 262), (202, 262), (202, 380), (58, 380)], (254, 248, 226), seed + 2, INK_W - 2, amp=1.0)
        return _done(im, w, h)
    return gcache(("oilb24", seed), mk)


def oil_drop_el(mood="happy", look=(0, 0), ghost=False, seed=8):
    def mk():
        w, h = 150, 190; im, d, S = _cv(w, h)
        P = [(75, 8)] + _arcpts(75, 118, 56, 60, -35, 215, 20)
        if ghost:
            _ink_poly(d, P, None, seed, 4, amp=1.0, col=(150, 120, 60))
            if mood: _face(d, S, 75, 122, 1.05, mood, look)
        else:
            _ink_poly(d, P, OILC, seed, INK_W - 1, amp=1.0)
            d.arc(S(38, 84, 96, 154), 120, 210, fill=(255, 255, 230, 255), width=7 * SC3)
            if mood: _face(d, S, 75, 122, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("oild24", mood, look, ghost, seed), mk)


def milk_can_el(mood=None, seed=9):
    def mk():
        w, h = 260, 400; im, d, S = _cv(w, h)
        _ink_poly(d, [(92, 58), (168, 58), (172, 118), (216, 166), (216, 378), (44, 378), (44, 166), (88, 118)], (222, 230, 234), seed, INK_W)
        _shade(im, lambda q, S_: q.rectangle(S_(44, 58, 216, 378), fill=255), lambda q, S_, c: q.rectangle(S_(160, 50, 230, 390), fill=c), (150, 164, 176), 150)
        _ink_ell(d, 130, 52, 50, 18, (246, 248, 248), seed + 1, INK_W, n=20)
        d.line([tuple(q * SC3 for q in p) for p in ((44, 176), (216, 176))], fill=INKC + (255,), width=4 * SC3)
        d.line([tuple(q * SC3 for q in p) for p in ((44, 350), (216, 350))], fill=INKC + (255,), width=4 * SC3)
        if mood: _face(d, S, 130, 262, 1.5, mood, (0, 0))
        return _done(im, w, h)
    return gcache(("milkc24", mood, seed), mk)


def tikka_el(mood=None, seed=10, q=False):
    """a plate of paneer tikka on two skewers (no label anywhere)."""
    def mk():
        w, h = 520, 320; im, d, S = _cv(w, h)
        _ink_ell(d, 260, 212, 240, 88, (250, 248, 238), seed, INK_W, n=36)
        _ink_ell(d, 260, 208, 188, 62, (240, 236, 222), seed + 1, 3, n=30, amp=0.8)
        cols = [(246, 196, 120), (222, 90, 40), (246, 200, 130), (100, 150, 70), (244, 190, 110)]
        for sk, (yy, off) in enumerate(((128, 0), (196, 22))):
            d.line([tuple(q_ * SC3 for q_ in p) for p in ((66 + off, yy + 26), (456 + off, yy - 6))], fill=(120, 84, 50, 255), width=6 * SC3)
            for j, c in enumerate(cols):
                x = 110 + off + j * 68; y = yy + 20 - j * 6
                _ink_poly(d, [(x - 28, y - 30), (x + 28, y - 30), (x + 30, y + 26), (x - 30, y + 26)], c, seed + 3 + j + sk * 7, INK_W - 2, amp=1.4)
                for (dx, dy) in ((-12, -14), (10, 8), (2, -20)): d.ellipse(S(x + dx - 4, y + dy - 3, x + dx + 4, y + dy + 3), fill=(90, 50, 30, 255))
        if mood: _face(d, S, 260, 260, 1.1, mood, (0, 0))
        return _done(im, w, h)
    return gcache(("tikka24", mood, seed), mk)


def packet_el(seed=11, tint=None):
    """a sealed plastic pouch (write on it with chips in the shot: word at y - 60, small line at y + 90)."""
    def mk():
        w, h = 420, 540; im, d, S = _cv(w, h)
        _ink_poly(d, [(36, 50), (384, 50), (396, 500), (24, 500)], tint or (232, 244, 244), seed, INK_W)
        _ink_poly(d, [(30, 22), (390, 22), (388, 72), (32, 72)], (200, 214, 216), seed + 1, INK_W - 1, amp=0.8)
        d.line([tuple(q * SC3 for q in p) for p in ((60, 96), (100, 460))], fill=(255, 255, 255, 230), width=9 * SC3)
        _hatch_in(im, (300, 90, 390, 490), lambda q, S_: q.rectangle(S_(300, 90, 390, 490), fill=255))
        return _done(im, w, h)
    return gcache(("packet24", seed, tint), mk)


def menu_el(seed=12):
    def mk():
        w, h = 560, 720; im, d, S = _cv(w, h)
        _ink_poly(d, [(26, 22), (534, 14), (540, 702), (20, 706)], (254, 246, 224), seed, INK_W, amp=2.2)
        d.rectangle(S(52, 48, 508, 676), outline=(180, 90, 60, 255), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("menu24", seed), mk)


def article_el(seed=13):
    """a news article (the shot writes the headline with chips)."""
    def mk():
        w, h = 440, 560; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 18), (420, 12), (426, 544), (14, 548)], (250, 246, 234), seed, INK_W, amp=2.0)
        rng = np.random.default_rng(seed)
        for yy in range(300, 520, 30):
            x1 = rng.uniform(320, 396); d.line([tuple(q * SC3 for q in p) for p in ((50, yy), (x1, yy))], fill=(170, 160, 146, 255), width=5 * SC3)
        d.rectangle(S(50, 60, 390, 96), fill=(170, 160, 146, 255))
        return _done(im, w, h)
    return gcache(("article24", seed), mk)


def buffalo_el(mood="happy", seed=14):
    def mk():
        w, h = 460, 400; im, d, S = _cv(w, h)
        for sg in (-1, 1):
            P = [(230 + sg * 80, 130), (230 + sg * 170, 110), (230 + sg * 210, 50), (230 + sg * 222, 110), (230 + sg * 180, 170), (230 + sg * 90, 180)]
            _ink_poly(d, P, (210, 200, 180), seed + sg, INK_W - 1, amp=1.0)
            _ink_ell(d, 230 + sg * 138, 196, 36, 18, (70, 70, 76), seed + 2 + sg, INK_W - 1, n=14)
        _ink_ell(d, 230, 208, 112, 136, (74, 74, 82), seed, INK_W, n=30, amp=1.8)
        _ink_ell(d, 230, 296, 78, 54, (150, 136, 130), seed + 3, INK_W - 1, n=20)
        for sg in (-1, 1): d.ellipse(S(230 + sg * 30 - 9, 288, 230 + sg * 30 + 9, 306), fill=INKC + (255,))
        # eyes + brows on the dark face in cream
        for sg in (-1, 1):
            d.ellipse(S(230 + sg * 46 - 16, 168, 230 + sg * 46 + 16, 200), fill=(250, 246, 234, 255)); d.ellipse(S(230 + sg * 46 - 7, 178, 230 + sg * 46 + 7, 194), fill=INKC + (255,))
        d.arc(S(190, 300, 270, 336), 20, 160, fill=INKC + (255,), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("buff24", mood, seed), mk)


def flask_el(col=None, seed=15):
    def mk():
        w, h = 240, 320; im, d, S = _cv(w, h); c = col or ACC_L
        _ink_poly(d, [(96, 26), (144, 26), (144, 112), (220, 290), (20, 290), (96, 112)], (236, 246, 248), seed, INK_W)
        d.polygon(S(66, 196, 174, 196, 212, 286, 28, 286), fill=c + (255,))
        d.line([tuple(q * SC3 for q in p) for p in ((66, 196), (174, 196))], fill=INKC + (255,), width=4 * SC3)
        d.ellipse(S(110, 230, 126, 246), fill=(255, 255, 255, 220)); d.ellipse(S(90, 256, 100, 266), fill=(255, 255, 255, 200))
        return _done(im, w, h)
    return gcache(("flask24", col, seed), mk)


def microscope_el(seed=16):
    def mk():
        w, h = 340, 460; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 410), (300, 410), (300, 440), (40, 440)], (70, 76, 92), seed, INK_W)
        _ink_poly(d, [(220, 410), (260, 410), (250, 200), (214, 170), (190, 196), (222, 226)], (92, 100, 120), seed + 1, INK_W)
        _ink_poly(d, [(84, 300), (250, 300), (250, 322), (84, 322)], (60, 64, 80), seed + 2, INK_W - 1)
        P = [(130, 40), (176, 26), (232, 196), (186, 212)]
        _ink_poly(d, P, (226, 230, 236), seed + 3, INK_W)
        _ink_poly(d, [(176, 212), (222, 198), (232, 232), (190, 246)], (70, 76, 92), seed + 4, INK_W - 1)
        return _done(im, w, h)
    return gcache(("micro24", seed), mk)


def door_el(open_=0.0, seed=17):
    def mk():
        w, h = 400, 900; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 14), (386, 14), (386, 890), (14, 890)], (120, 78, 50), seed, INK_W + 1, amp=1.2)
        _ink_poly(d, [(40, 40), (360, 40), (360, 890), (40, 890)], (40, 34, 44) if open_ > 0.5 else (170, 112, 70), seed + 1, INK_W - 1, amp=1.0)
        if open_ > 0.5:
            _ink_poly(d, [(40, 40), (130, 90), (130, 890), (40, 890)], (170, 112, 70), seed + 2, INK_W - 1, amp=0.8)
        else:
            for (a, b, c_, e) in ((80, 90, 320, 380), (80, 450, 320, 840)): d.rectangle(S(a, b, c_, e), outline=(110, 70, 44, 255), width=5 * SC3)
            d.ellipse(S(316, 470, 346, 500), fill=(240, 200, 80, 255), outline=INKC + (255,))
        return _done(im, w, h)
    return gcache(("door24", open_ > 0.5, seed), mk)


def heart_el(col=None):
    def mk():
        w, h = 80, 76; im, d, S = _cv(w, h)
        P = [(40, 68)] + _arcpts(22, 26, 18, 18, 140, 340, 8) + _arcpts(58, 26, 18, 18, 200, 400, 8)
        _ink_poly(d, P, col or (232, 70, 90), 3, 4, amp=0.3)
        return _done(im, w, h)
    return gcache(("heart24", col), mk)


def net_catch(f, cx, cy, w, h, k, t, seed=4, fish=False, nfat=9):
    """heat + acid: protein bits (loose wiggles, k=0) snap into a NET (k=1) and the fat balls get caught in it. Paper panel behind; whey = the pale green liquid."""
    x0, y0 = cx - w / 2, cy - h / 2
    cv2.rectangle(f, (int(x0), int(y0)), (int(x0 + w), int(y0 + h)), C((238, 240, 214)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed); nx, ny = 7, 6
    home = np.stack(np.meshgrid(np.linspace(x0 + 70, x0 + w - 70, nx), np.linspace(y0 + 70, y0 + h - 70, ny)), -1).reshape(-1, 2)
    scat = np.stack([rng.uniform(x0 + 30, x0 + w - 30, nx * ny), rng.uniform(y0 + 30, y0 + h - 30, nx * ny)], 1)
    wob = np.stack([np.sin(t * 2.3 + np.arange(nx * ny)), np.cos(t * 1.9 + np.arange(nx * ny) * 1.7)], 1) * (10 + 18 * (1 - k))
    e = k * k * (3 - 2 * k); P = scat * (1 - e) + home * e + wob
    # fat balls drift freely, then sit in the net cells
    cells = np.stack(np.meshgrid(np.linspace(x0 + 70 + (w - 140) / (nx - 1) / 2, x0 + w - 70 - (w - 140) / (nx - 1) / 2, nx - 1), np.linspace(y0 + 70 + (h - 140) / (ny - 1) / 2, y0 + h - 70 - (h - 140) / (ny - 1) / 2, ny - 1)), -1).reshape(-1, 2)
    idx = rng.permutation(len(cells))[:nfat]
    for j, i_ in enumerate(idx):
        fx = cx + (w * 0.42) * math.sin(t * 1.3 + j * 2.1) * (1 - e) * 0.9 + (cells[i_][0] - cx) * e
        fy = cy + (h * 0.42) * math.cos(t * 1.1 + j * 1.3) * (1 - e) * 0.9 + (cells[i_][1] - cy) * e
        if fish:
            cv2.ellipse(f, (int(fx), int(fy)), (34, 22), 0, 0, 360, C(INKC), -1, cv2.LINE_AA); cv2.ellipse(f, (int(fx), int(fy)), (28, 17), 0, 0, 360, C(OILC), -1, cv2.LINE_AA)
            T_ = np.array([(fx - 26, fy), (fx - 52, fy - 18), (fx - 52, fy + 18)], np.int32); cv2.fillPoly(f, [T_], C(OILC), cv2.LINE_AA); cv2.polylines(f, [T_], True, C(INKC), 4, cv2.LINE_AA)
            cv2.circle(f, (int(fx + 14), int(fy - 4)), 4, C(INKC), -1, cv2.LINE_AA)
        else:
            cv2.circle(f, (int(fx), int(fy)), 28, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(fx), int(fy)), 23, C(OILC), -1, cv2.LINE_AA); cv2.circle(f, (int(fx - 8), int(fy - 8)), 6, C((255, 250, 220)), -1, cv2.LINE_AA)
    if k > 0.25:
        al = clamp((k - 0.25) / 0.5); ov = f.copy()
        for j in range(ny):
            for i in range(nx):
                a = P[j * nx + i]
                if i + 1 < nx: b = P[j * nx + i + 1]; cv2.line(ov, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C(INKC), 11, cv2.LINE_AA); cv2.line(ov, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C((255, 252, 240)), 6, cv2.LINE_AA)
                if j + 1 < ny: b = P[(j + 1) * nx + i]; cv2.line(ov, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C(INKC), 11, cv2.LINE_AA); cv2.line(ov, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C((255, 252, 240)), 6, cv2.LINE_AA)
        f[:] = f * (1 - al) + ov * al
    for j in range(nx * ny):
        a = P[j]; cv2.circle(f, (int(a[0]), int(a[1])), 13, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(a[0]), int(a[1])), 9, C((255, 252, 240)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x0), int(y0)), (int(x0 + w), int(y0 + h)), C(INKC), 7, cv2.LINE_AA)


def helix(f, cx, cy, L, coil, t, lit=0.0, beads=0.0, R=120, turns=4.0, nb=7, sway=True):
    """a bead CHAIN that coils into a SPRING (coil 0..1) along x; iodine beads (beads 0..1) fly in from the right and sit in a straight line on its axis; lit 0..1 = the whole thing goes blue-black."""
    us = np.linspace(0, 1, 110); col = tuple(int(a + (b - a) * lit) for a, b in zip(PAN, ACC))
    dark = tuple(int(a + (b - a) * lit) for a, b in zip((214, 196, 150), ACC_S))
    pts = []
    for u in us:
        ph = 2 * math.pi * turns * u + t * 0.5
        wig = 16 * math.sin(u * 22 + t * 2) * (1 - coil)
        x = cx - L / 2 + L * u + coil * R * 0.5 * math.sin(ph)
        y = cy + wig + coil * R * math.cos(ph)
        pts.append((x, y, math.sin(ph) * coil))
    back = [p for p in pts if p[2] < 0]; front = [p for p in pts if p[2] >= 0]
    for (x, y, z) in back:
        cv2.circle(f, (int(x), int(y)), 21, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 16, C(dark), -1, cv2.LINE_AA)
    # iodine line
    for j in range(nb):
        k = clamp(beads * 1.6 - 0.6 * (nb - 1 - j) / (nb - 1) if False else beads * 1.6 - 0.6 * j / (nb - 1))
        tx = cx - L * 0.36 + L * 0.72 * j / (nb - 1)
        e = k * k * (3 - 2 * k); x = W + 80 + (tx - W - 80) * e; y = cy - 260 * (1 - e) * math.sin(math.pi * clamp(e)) + 6 * math.sin(t * 2 + j)
        if k > 0:
            cv2.circle(f, (int(x), int(y)), 26, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 20, C(IOD if lit < 0.5 else ACC_S), -1, cv2.LINE_AA); cv2.circle(f, (int(x - 6), int(y - 7)), 5, C((255, 240, 210)), -1, cv2.LINE_AA)
    for (x, y, z) in front:
        cv2.circle(f, (int(x), int(y)), 21, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 16, C(col), -1, cv2.LINE_AA)


def light_in_out(f, cx, cy, t, k=1.0, kout=1.0):
    """white light (a fan of colours) comes in from the left, the blue leaves on the right: 'soaks up light differently'."""
    cols = ((226, 70, 60), (240, 150, 50), (240, 210, 70), (80, 170, 90), (70, 90, 210))
    for i, c in enumerate(cols):
        y = cy - 120 + 60 * i
        x1 = cx - 240 + 0; xs = int(40 + (x1 - 40) * clamp(k * 1.2 - i * 0.05))
        cv2.line(f, (40, y), (xs, y), C(INKC), 22, cv2.LINE_AA); cv2.line(f, (40, y), (xs, y), C(c), 14, cv2.LINE_AA)
    if kout > 0:
        xe = int(cx + 240 + (1020 - cx - 240) * clamp(kout)); yb = cy
        cv2.line(f, (cx + 240, yb), (xe, yb), C(INKC), 34, cv2.LINE_AA); cv2.line(f, (cx + 240, yb), (xe, yb), C((70, 90, 210)), 24, cv2.LINE_AA)


def phone_frame(f, cx, cy, w=520, h=860, bg=(250, 244, 226)):
    """an ink phone; returns the screen box (x0, y0, x1, y1). Draw the 'video' inside it."""
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)
    cv2.rectangle(f, (x0 + 10, y0 + 12), (x1 + 10, y1 + 12), C((96, 74, 60)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((48, 44, 50)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 8, cv2.LINE_AA)
    sx0, sy0, sx1, sy1 = x0 + 22, y0 + 44, x1 - 22, y1 - 44
    cv2.rectangle(f, (sx0, sy0), (sx1, sy1), C(bg), -1, cv2.LINE_AA)
    cv2.circle(f, (int(cx), y0 + 22), 7, C((110, 104, 110)), -1, cv2.LINE_AA)
    return sx0, sy0, sx1, sy1


def waiter(f, x, y, s=1.0, t=0.0, **kw):
    """another person on mute: white shirt + a red bow tie + a towel on the arm."""
    hs = chub(f, x, y, s, t=t, shirt=(248, 248, 244), **kw)
    bx, by = x, y - 332 * s
    for sg in (-1, 1):
        P = np.array([(bx, by), (bx + sg * 36 * s, by - 20 * s), (bx + sg * 36 * s, by + 20 * s)], np.int32); cv2.fillPoly(f, [P], C((196, 44, 44)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(bx), int(by)), int(9 * s), C(INKC), -1, cv2.LINE_AA)
    return hs


def guard_post(f, t, guard_mood="n", look=(0.8, 0), photo=True, door_open=0.0, gx=640, gy=1190, gs=1.0):
    """the guard metaphor: a door at the right, the iodine guard at his post, ONE photo on the wall (the wanted poster shows the starch chain)."""
    comp(f, scale_el(door_el(door_open), 0.92), 880, 1000)
    if photo:
        comp(f, scale_el(wanted_el(), 0.66), 290, 830); comp(f, scale_el(starch_guy_el("sus"), 0.56), 290, 860)
    comp(f, scale_el(bottle_el(guard_mood, look, cap=True), gs), gx, gy)


def _diner_bg(top_y=1330):
    f = _vgrad((232, 150, 96), (196, 110, 76), 0, top_y)
    # brick wall
    for r_, yy in enumerate(range(240, top_y, 62)):
        for x in range(-60 + (r_ % 2) * 70, W, 140):
            c_ = (206 + (x * 7 + yy) % 24, 118 + (x * 3 + yy) % 18, 84)
            cv2.rectangle(f, (x, yy), (x + 132, yy + 54), C(c_), -1, cv2.LINE_AA); cv2.rectangle(f, (x, yy), (x + 132, yy + 54), C((160, 96, 72)), 3, cv2.LINE_AA)
    # night window with lights
    cv2.rectangle(f, (70, 480), (430, 960), C((30, 36, 70)), -1, cv2.LINE_AA)
    for j in range(16):
        xx = 80 + j * 22; yy = 560 + 46 * math.sin(j * 0.6)
        cv2.circle(f, (xx, int(yy)), 7, C((255, 210, 110)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (70, 480), (430, 960), C(INKC), 9, cv2.LINE_AA); cv2.line(f, (250, 480), (250, 960), C(INKC), 7, cv2.LINE_AA)
    # chalk menu board
    cv2.rectangle(f, (640, 470), (1010, 900), C((44, 50, 48)), -1, cv2.LINE_AA); cv2.rectangle(f, (640, 470), (1010, 900), C((130, 84, 50)), 16, cv2.LINE_AA)
    for yy, x1 in ((550, 930), (620, 880), (690, 950), (760, 860), (830, 910)):
        cv2.line(f, (690, yy), (x1, yy), C((220, 224, 210)), 7, cv2.LINE_AA)
    # booth back
    cv2.rectangle(f, (0, 1110), (W, top_y), C((150, 46, 46)), -1, cv2.LINE_AA); cv2.line(f, (0, 1110), (W, 1110), C(INKC), 8, cv2.LINE_AA)
    for x in range(90, W, 180): cv2.line(f, (x, 1116), (x, top_y), C((110, 30, 34)), 5, cv2.LINE_AA)
    return _soft(f, 4).astype(np.float32)


def set_diner(t=0.0, dim=0.0, top_y=1330):
    """a warm restaurant at night: brick, a window on the street, a chalk menu, a red booth, two hanging lamps."""
    f = gcache(("diner24", top_y), lambda: _diner_bg(top_y)).copy()
    for lx in (250, 830):
        cv2.line(f, (lx, 0), (lx, 300), C(INKC), 6, cv2.LINE_AA)
        P = np.array([(lx - 70, 360), (lx + 70, 360), (lx + 36, 296), (lx - 36, 296)], np.int32); cv2.fillPoly(f, [P], C((230, 150, 60)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 6, cv2.LINE_AA)
        glow(f, lx, 400, 340, (255, 226, 160), 0.14 + 0.008 * math.sin(t * 3 + lx))
    if dim: f = f * (1 - dim)
    return inkify(f, 0.08)


def diner_front(f, top_y=1330):
    cv2.rectangle(f, (0, top_y), (W, H), C((128, 84, 54)), -1); cv2.line(f, (0, top_y), (W, top_y), C(INKC), 8, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 8), (W, top_y + 30), C((170, 118, 76)), -1)
    for x in (150, 420, 700, 950): cv2.line(f, (x, top_y + 40), (x + 30, H), C((104, 66, 42)), 4, cv2.LINE_AA)


SCHEMES["bluep"] = ((206, 212, 244), (238, 240, 252), (190, 198, 238), (0.6, 0.62, 0.86))
SCHEMES["amberp"] = ((246, 222, 176), (254, 242, 214), (238, 206, 150), (0.86, 0.68, 0.44))


def milkfat_el(seed=18):
    """a milk-fat globule (cream)."""
    def mk():
        w, h = 90, 90; im, d, S = _cv(w, h)
        _ink_ell(d, 45, 46, 30, 28, (255, 240, 190), seed, INK_W - 2, n=20, amp=1.6)
        d.ellipse(S(28, 26, 40, 36), fill=(255, 255, 255, 230))
        return _done(im, w, h)
    return gcache(("mfat24", seed), mk)


def glass2_el(col=(250, 248, 240), level=0.8, seed=19):
    """a tumbler with any liquid (milk by default; lib17 glass_el is water-mint)."""
    def mk():
        w, h = 200, 300; im, d, S = _cv(w, h)
        yl = 270 - 230 * level
        d.polygon(S(34, yl, 166, yl, 158, 270, 42, 270), fill=tuple(col) + (255,))
        d.line([tuple(q * SC3 for q in p) for p in ((36, yl), (164, yl))], fill=INKC + (200,), width=3 * SC3)
        _ink_poly(d, [(24, 20), (176, 20), (160, 280), (40, 280)], None, seed, INK_W, amp=0.9)
        d.line([tuple(q * SC3 for q in p) for p in ((50, 50), (58, 240))], fill=(255, 255, 255, 220), width=7 * SC3)
        return _done(im, w, h)
    return gcache(("glass24", col, round(level, 1), seed), mk)


def muslin_el(seed=20, drip=True):
    """a muslin cloth bundle tied at the top, holding the curds."""
    def mk():
        w, h = 340, 380; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        P = [(150, 70), (190, 70)] + _arcpts(170, 230, 136, 130, -55, 235, 26)
        _ink_poly(d, P, (246, 240, 222), seed, INK_W, amp=2.0)
        for i in range(90):
            a_ = rng.uniform(0, 6.28); r_ = rng.uniform(0, 1) ** 0.5; x, y = 170 + 118 * r_ * math.cos(a_), 240 + 110 * r_ * math.sin(a_); d.ellipse(S(x - 2, y - 2, x + 2, y + 2), fill=(226, 216, 186, 255))
        for dx in (-40, 0, 40): d.line([tuple(q * SC3 for q in p) for p in ((170 + dx * 0.3, 80), (170 + dx * 1.6, 200))], fill=INKC + (120,), width=3 * SC3)
        _ink_poly(d, [(140, 58), (200, 58), (204, 82), (136, 82)], (200, 150, 100), seed + 1, INK_W - 1, amp=0.8)
        _hatch_in(im, (220, 160, 306, 340), lambda q, S_: q.ellipse(S_(34, 100, 306, 360), fill=255))
        return _done(im, w, h)
    return gcache(("muslin24", seed), mk)
