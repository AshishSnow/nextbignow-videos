# ================= anim_props_lib17.py (ep 17, 31 Oct): the INK PROP TOOLKIT + the teeth / candy / bacteria props of the first Chubby INK
# episode. Draw every new hero prop with _ink_poly / _ink_ell (one wobbly warm-ink outline, flat fill), _shade (shadow side), _hatch_in
# (diagonal hatching), _face (3-stroke face). Palette rule: paper, ink, mint, skin + ONE topic accent (ACC = this episode's violet).
# Props: tooth_el (film/crack/hole/spot/soft + face), teeth_row, bug_el/bug_crowd (bacteria citizens), candy_el (wrap/gummy/caramel/sour/choc/lolly),
# pail_el, acid_drop_el/acid_pool, saliva_wave, minerals, spit_hero_el, brush_el, paste_el, glass_el, plate_el, timer_el, podium/cloth, magnifier_ink_el. =================
ACC = (142, 78, 200); ACC_S = (92, 44, 150); ACC_L = (206, 180, 236); ACC_XL = (232, 220, 246)      # the topic accent (violet) + tints
TOOTHW = (252, 250, 244); TOOTHW_S = (214, 206, 190)
GUM = (236, 170, 160); GUM_S = (206, 128, 120)
CHOC = (92, 56, 36); CHOC_S = (58, 32, 20); CHOC_H = (150, 104, 70)
CARA = (224, 170, 96); CARA_S = (178, 120, 54)
SCHEMES["paper"] = ((247, 241, 228), (252, 248, 238), (240, 232, 214), (0.8, 0.76, 0.68))
SCHEMES["violet"] = ((110, 60, 170), (178, 130, 226), (100, 52, 160), (0.4, 0.25, 0.6))
SCHEMES["dusk_v"] = ((48, 30, 80), (120, 80, 170), (40, 24, 70), (0.3, 0.2, 0.45))
SCHEMES["mintp"] = ((170, 226, 206), (222, 246, 236), (150, 210, 190), (0.5, 0.75, 0.65))
SC3 = 3


def _ink_poly(d, pts, fill=None, seed=0, w=INK_W, sc=SC3, closed=True, amp=1.6, col=INKC):
    """ink polygon: flat fill + ONE wobbly outline (fixed wobble per seed, so it never boils)."""
    P = _wob(list(pts), amp, seed)
    if fill is not None: d.polygon([(x * sc, y * sc) for x, y in P], fill=tuple(fill) + (255,))
    Q = P + [P[0]] if closed else P
    d.line([(x * sc, y * sc) for x, y in Q], fill=tuple(col) + (255,), width=max(1, int(w * sc)), joint="curve")


def _ink_ell(d, cx, cy, rx, ry, fill=None, seed=0, w=INK_W, sc=SC3, n=28, amp=1.4, col=INKC):
    _ink_poly(d, _arcpts(cx, cy, rx, ry, 0, 360, n)[:-1], fill, seed, w, sc, True, amp, col)


def _shade(im, mask_fn, shade_fn, col, alpha=120, sc=SC3):
    """shadow side: shade_fn draws the dark shape, clipped by mask_fn (both get an ImageDraw + S scaler)."""
    S = lambda *v: [x * sc for x in v]
    m = Image.new("L", im.size, 0); mask_fn(ImageDraw.Draw(m), S)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); shade_fn(ImageDraw.Draw(sh), S, tuple(col) + (alpha,))
    im.alpha_composite(Image.composite(sh, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))


def _hatch_in(im, box, mask_fn, ang=-40, gap=9, alpha=34, sc=SC3):
    S = lambda *v: [x * sc for x in v]
    _hatch(im, S, (box[0], box[1], box[2], box[3], lambda q: mask_fn(q, S)), ang, gap, INKC + (alpha,), 1)


def _cv(w, h, sc=SC3):
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); return im, ImageDraw.Draw(im), (lambda *v: [x * sc for x in v])


def _face(d, S, cx, cy, s=1.0, mood="n", look=(0, 0), sc=SC3):
    """3-stroke ink face used by the tooth / bugs / spit hero: dot eyes, brow strokes, mouth curve."""
    ex = 16 * s; ey = cy - 6 * s; ox, oy = look[0] * 4 * s, look[1] * 3 * s
    for sgn in (-1, 1):
        x = cx + sgn * ex
        if mood == "love":
            d.polygon(S(x, ey + 7 * s, x - 8 * s, ey - 2 * s, x - 4 * s, ey - 8 * s, x, ey - 4 * s, x + 4 * s, ey - 8 * s, x + 8 * s, ey - 2 * s), fill=(214, 60, 90, 255))
        elif mood == "happy":
            d.line([tuple(q * sc for q in p) for p in _arcpts(x, ey + 3 * s, 7 * s, 6 * s, 200, 340, 8)], fill=INKC + (255,), width=int(4 * s * sc), joint="curve")
        else:
            r = (7 if mood == "wow" else 5) * s
            d.ellipse(S(x + ox - r, ey + oy - r, x + ox + r, ey + oy + r), fill=INKC + (255,))
        by = ey - 14 * s
        if mood in ("sad", "ouch"): bp = [(x - sgn * 8 * s, by + 2 * s), (x + sgn * 8 * s, by - 4 * s)]
        elif mood == "angry": bp = [(x - sgn * 8 * s, by - 4 * s), (x + sgn * 8 * s, by + 3 * s)]
        elif mood == "wow": bp = [(x - 8 * s, by - 6 * s), (x + 8 * s, by - 6 * s)]
        else: bp = [(x - 8 * s, by), (x + 8 * s, by - 1 * s)]
        d.line([tuple(q * sc for q in p) for p in _wob(bp, 0.8, 3 + sgn)], fill=INKC + (255,), width=int(3.5 * s * sc))
    my = cy + 14 * s
    if mood in ("happy", "love"): d.line([tuple(q * sc for q in p) for p in _arcpts(cx, my - 6 * s, 14 * s, 9 * s, 20, 160, 10)], fill=INKC + (255,), width=int(4 * s * sc), joint="curve")
    elif mood in ("sad", "ouch"): d.line([tuple(q * sc for q in p) for p in _arcpts(cx, my + 8 * s, 12 * s, 7 * s, 200, 340, 10)], fill=INKC + (255,), width=int(4 * s * sc), joint="curve")
    elif mood == "wow": d.ellipse(S(cx - 7 * s, my - 6 * s, cx + 7 * s, my + 8 * s), fill=(110, 40, 46, 255), outline=INKC + (255,), width=int(3 * s * sc))
    elif mood == "munch": d.rounded_rectangle(S(cx - 12 * s, my - 6 * s, cx + 12 * s, my + 8 * s), int(5 * s * sc), fill=(110, 40, 46, 255), outline=INKC + (255,), width=int(3 * s * sc))
    elif mood == "hungry":
        d.line(S(cx - 10 * s, my - 2 * s, cx + 10 * s, my - 2 * s), fill=INKC + (255,), width=int(4 * s * sc))
        d.ellipse(S(cx - 1 * s, my - 2 * s, cx + 9 * s, my + 9 * s), fill=(214, 90, 110, 255), outline=INKC + (255,), width=int(2 * s * sc))
    else: d.line([tuple(q * sc for q in p) for p in _wob([(cx - 9 * s, my - 2 * s), (cx + 9 * s, my - 3 * s)], 0.6, 9)], fill=INKC + (255,), width=int(3.5 * s * sc))


# ---------------- the tooth (hero prop): a molar with a face, enamel shell, optional plaque film / crack / hole / white spot ----------------
MOLAR = [(70, 60), (110, 36), (150, 58), (190, 36), (232, 60), (240, 120), (226, 180), (214, 206), (210, 290), (190, 300), (176, 220), (150, 210), (124, 220), (110, 300), (90, 290), (84, 206), (74, 180), (60, 120)]


def tooth_el(mood=None, film=0.0, crack=0.0, hole=False, spot=False, soft=False, look=(0, 0)):
    film = round(clamp(film) * 4) / 4; crack = round(clamp(crack) * 4) / 4
    def mk():
        w, h = 300, 320; im, d, S = _cv(w, h)
        pts = [(x + (6 * math.sin(y / 30.0) if soft else 0), y) for x, y in MOLAR]
        _ink_poly(d, pts, TOOTHW, 11, INK_W, amp=2.2)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts], fill=255),
               lambda q, S_, c: q.polygon(S_(170, 30, 250, 30, 250, 310, 200, 310, 190, 220, 170, 120), fill=c), TOOTHW_S, 150)
        _hatch_in(im, (150, 40, 250, 310), lambda q, S_: q.polygon(S_(176, 40, 246, 60, 236, 180, 212, 300, 190, 300, 178, 220), fill=255), -40, 10, 30)
        d.line(S(96, 70, 150, 100, 204, 70), fill=INKC + (120,), width=3 * SC3, joint="curve")         # fissure line on the crown
        if film > 0:                                                                                      # plaque: a sticky violet film over the crown
            fm = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(fm)
            top = [(x, y) for x, y in pts[:8]] + [(224, 198), (150, 214), (76, 198)]
            q.polygon([(x * SC3, y * SC3) for x, y in top], fill=ACC_L + (int(150 * film),))
            q.line([(x * SC3, y * SC3) for x, y in _wob([(76, 198), (110, 206), (150, 214), (190, 206), (224, 198)], 1.5, 21)], fill=ACC_S + (int(230 * film),), width=4 * SC3, joint="curve")
            im.alpha_composite(fm)
            _hatch_in(im, (60, 30, 250, 220), lambda q2, S_: q2.polygon([(x * SC3, y * SC3) for x, y in top], fill=255), -40, 11, int(40 * film))
        if spot: d.ellipse(S(104, 140, 148, 176), fill=(255, 255, 255, 255), outline=INKC + (120,), width=2 * SC3)
        if crack > 0:
            cp = [(150, 100), (140, 126), (158, 150), (146, 176), (160, 200), (150, 222)]
            n_ = max(2, int(2 + 4 * crack))
            d.line([(x * SC3, y * SC3) for x, y in cp[:n_]], fill=INKC + (255,), width=int((2 + 3 * crack) * SC3), joint="curve")
        if hole:
            _ink_poly(d, _arcpts(150, 150, 34, 30, 0, 360, 14)[:-1], (74, 42, 50), 23, INK_W - 2, amp=4.0)
        if mood: _face(d, S, 150, 128 if not hole else 92, 1.25, mood, look)
        return _done(im, w, h)
    return gcache(("tooth17", mood, film, crack, hole, spot, soft, look), mk)


def teeth_row(f, x, y, n=6, s=0.6, film=0.0, t=0.0):
    """a row of small ink teeth standing in a gum ridge (the inside of the mouth)."""
    ov = f.copy()
    gw = n * 140 * s
    cv2.ellipse(ov, (int(x), int(y + 40 * s)), (int(gw / 2 + 60 * s), int(70 * s)), 0, 0, 360, C(GUM), -1, cv2.LINE_AA)
    cv2.ellipse(ov, (int(x), int(y + 40 * s)), (int(gw / 2 + 60 * s), int(70 * s)), 0, 0, 360, C(INKC), max(2, int(6 * s)), cv2.LINE_AA)
    f[:] = ov
    for i in range(n):
        tx = x - gw / 2 + 70 * s + i * 140 * s
        comp(f, scale_el(tooth_el(None, film), s * 0.78), tx, y - 90 * s + 2 * math.sin(t * 2 + i))


# ---------------- bacteria 'citizens' of the plaque city ----------------
def bug_el(mood="n", look=(0, 0), seed=1, col=ACC_L):
    def mk():
        w, h = 130, 110; im, d, S = _cv(w, h)
        rng = np.random.default_rng(seed)
        body = _arcpts(65, 54, 46 + rng.uniform(-4, 4), 36 + rng.uniform(-3, 3), 0, 360, 22)[:-1]
        for sgn in (-1, 1):                                                                   # 3 little leg strokes per side
            for k in range(3):
                y0 = 46 + k * 12; x0 = 65 + sgn * 44
                d.line(S(x0, y0, x0 + sgn * 14, y0 + 8 + 3 * k), fill=INKC + (255,), width=3 * SC3)
        _ink_poly(d, body, col, seed + 40, INK_W - 2, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255),
               lambda q, S_, c: q.ellipse(S_(70, 40, 125, 100), fill=c), ACC_S, 70)
        for k in range(3): d.line(S(40 + k * 22, 20 - 4 * (k % 2), 44 + k * 22, 6 - 4 * (k % 2)), fill=INKC + (255,), width=3 * SC3)   # tiny hairs
        _face(d, S, 65, 56, 0.9, mood, look)
        return _done(im, w, h)
    return gcache(("bug17", mood, look, seed, col), mk)


def bug_crowd(f, cx, cy, t, n=7, s=0.6, mood="n", rad=120, seed=4, look=(0, 0)):
    rng = np.random.default_rng(seed)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi); r_ = rad * rng.uniform(0.2, 1.0)
        x = cx + r_ * math.cos(a); y = cy + r_ * math.sin(a) * 0.6 + 4 * math.sin(t * 5 + i)
        comp(f, scale_el(bug_el(mood, look, 1 + i % 4), s * rng.uniform(0.8, 1.15)), x, y)


# ---------------- candy ----------------
def candy_el(kind="wrap", col=None):
    def mk():
        w, h = 200, 150; im, d, S = _cv(w, h)
        if kind == "wrap":                                                                   # twisted wrapper
            c = col or ACC
            _ink_poly(d, [(30, 48), (60, 62), (60, 88), (30, 102), (44, 75)], c, 1, INK_W - 2)
            _ink_poly(d, [(170, 48), (140, 62), (140, 88), (170, 102), (156, 75)], c, 2, INK_W - 2)
            _ink_ell(d, 100, 75, 44, 34, c, 3, INK_W - 1)
            _hatch_in(im, (100, 40, 150, 110), lambda q, S_: q.ellipse(S_(56, 41, 144, 109), fill=255), -40, 8, 40)
            for k in range(3): d.line(S(76 + k * 18, 48, 70 + k * 18, 100), fill=INKC + (90,), width=2 * SC3)
            d.ellipse(S(78, 52, 94, 64), fill=(255, 255, 255, 200))
        elif kind == "gummy":                                                                # gummy bear
            c = col or ACC_L
            _ink_ell(d, 100, 92, 44, 40, c, 4, INK_W - 2)
            _ink_ell(d, 100, 48, 30, 28, c, 5, INK_W - 2)
            for sgn in (-1, 1):
                _ink_ell(d, 100 + sgn * 26, 30, 11, 11, c, 6, INK_W - 3); _ink_ell(d, 100 + sgn * 44, 80, 14, 12, c, 7, INK_W - 3); _ink_ell(d, 100 + sgn * 24, 126, 15, 11, c, 8, INK_W - 3)
            _face(d, S, 100, 46, 0.6, "n")
            _hatch_in(im, (100, 50, 150, 136), lambda q, S_: q.ellipse(S_(56, 52, 144, 132), fill=255), -40, 8, 34)
        elif kind == "caramel":                                                              # caramel cube
            _ink_poly(d, [(50, 60), (130, 60), (150, 40), (150, 110), (130, 130), (50, 130)], CARA, 9, INK_W - 2)
            d.line(S(130, 60, 130, 130), fill=INKC + (255,), width=3 * SC3); d.line(S(130, 60, 150, 40), fill=INKC + (255,), width=3 * SC3)
            _shade(im, lambda q, S_: q.polygon(S_(130, 60, 150, 40, 150, 110, 130, 130), fill=255), lambda q, S_, c: q.rectangle(S_(120, 30, 160, 140), fill=c), CARA_S, 150)
            _hatch_in(im, (90, 60, 132, 132), lambda q, S_: q.rectangle(S_(92, 62, 130, 130), fill=255), -40, 8, 30)
        elif kind == "sour":                                                                 # sour drop with sugar grains + spikes
            pts = _arcpts(100, 80, 48, 44, 0, 360, 16)[:-1]
            pts = [(x + (10 * math.cos(i * 2 * math.pi / 16) if i % 2 else 0), y + (10 * math.sin(i * 2 * math.pi / 16) if i % 2 else 0)) for i, (x, y) in enumerate(pts)]
            _ink_poly(d, pts, ACC, 12, INK_W - 2, amp=1.0)
            rng = np.random.default_rng(5)
            for k in range(26):
                a = rng.uniform(0, 2 * math.pi); r_ = rng.uniform(0, 38); d.ellipse(S(100 + r_ * math.cos(a) - 3, 80 + r_ * math.sin(a) - 3, 100 + r_ * math.cos(a) + 3, 80 + r_ * math.sin(a) + 3), fill=(255, 255, 255, 230))
            _face(d, S, 100, 78, 0.8, "angry")
        elif kind == "choc":                                                                 # chocolate square
            _ink_poly(d, [(40, 50), (160, 50), (160, 120), (40, 120)], CHOC, 14, INK_W - 2)
            d.line(S(100, 50, 100, 120), fill=INKC + (255,), width=3 * SC3); d.line(S(40, 85, 160, 85), fill=INKC + (255,), width=3 * SC3)
            for (x0, y0) in ((48, 58), (108, 58), (48, 93), (108, 93)): d.rounded_rectangle(S(x0, y0, x0 + 44, y0 + 20), 4 * SC3, fill=CHOC_H + (160,))
            _hatch_in(im, (100, 50, 160, 120), lambda q, S_: q.rectangle(S_(118, 52, 158, 118), fill=255), -40, 8, 46)
        elif kind == "lolly":
            d.line(S(100, 86, 100, 146), fill=TOOTHW + (255,), width=8 * SC3); d.line(S(100, 86, 100, 146), fill=INKC + (255,), width=2 * SC3)
            _ink_ell(d, 100, 56, 38, 38, ACC_L, 15, INK_W - 2)
            for k in range(3): d.arc(S(100 - 30 + k * 10, 56 - 30 + k * 10, 100 + 30 - k * 10, 56 + 30 - k * 10), 0, 300, fill=ACC_S + (200,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("candy17", kind, col), mk)


def pail_el(open_=True):
    """Halloween candy pail (violet) with a jack-o-lantern ink face; candies peeking out."""
    def mk():
        w, h = 300, 300; im, d, S = _cv(w, h)
        d.line([(x * SC3, y * SC3) for x, y in _wob(_arcpts(150, 120, 100, 100, 200, 340, 14), 1.5, 31)], fill=INKC + (255,), width=5 * SC3, joint="curve")   # handle
        _ink_poly(d, [(60, 110), (240, 110), (222, 280), (78, 280)], ACC, 32, INK_W)
        _shade(im, lambda q, S_: q.polygon(S_(60, 110, 240, 110, 222, 280, 78, 280), fill=255), lambda q, S_, c: q.polygon(S_(160, 100, 250, 100, 250, 290, 180, 290), fill=c), ACC_S, 130)
        _hatch_in(im, (160, 110, 240, 280), lambda q, S_: q.polygon(S_(170, 112, 238, 112, 222, 278, 178, 278), fill=255), -40, 10, 36)
        if open_:
            for i, (k, x, y, r_) in enumerate((("wrap", 110, 92, -20), ("lolly", 180, 70, 15), ("gummy", 148, 96, 6))):
                el = candy_el(k); pm, a = el
                pil = Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA").resize((int(pm.shape[1] * 0.55 * SC3), int(pm.shape[0] * 0.55 * SC3)), Image.LANCZOS).rotate(r_, expand=True)
                im.alpha_composite(pil, (int(x * SC3 - pil.width / 2), int(y * SC3 - pil.height / 2)))
        _ink_ell(d, 150, 112, 92, 22, ACC_L, 33, INK_W - 1)                                   # rim
        # jack-o-lantern face
        d.polygon(S(100, 160, 124, 160, 112, 184), fill=INKC + (255,)); d.polygon(S(176, 160, 200, 160, 188, 184), fill=INKC + (255,))
        d.polygon(S(96, 210, 204, 210, 190, 240, 170, 226, 150, 244, 130, 226, 110, 240), fill=INKC + (255,))
        return _done(im, w, h)
    return gcache(("pail17", open_), mk)


# ---------------- acid, saliva, minerals ----------------
def acid_drop_el(s=1.0, mood=None):
    def mk():
        w, h = 90, 120; im, d, S = _cv(w, h)
        pts = [(45, 10), (70, 56), (76, 80), (62, 106), (45, 112), (28, 106), (14, 80), (20, 56)]
        _ink_poly(d, pts, ACC, 41, INK_W - 2, amp=1.2)
        _hatch_in(im, (45, 30, 80, 110), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts[:5]] + [(45 * SC3, 112 * SC3), (45 * SC3, 30 * SC3)], fill=255), -40, 7, 50)
        d.ellipse(S(28, 54, 38, 66), fill=(255, 255, 255, 190))
        if mood: _face(d, S, 45, 74, 0.6, mood)
        return _done(im, w, h)
    return gcache(("acid17", mood), mk)


def acid_pool(f, x, y, w, h, t, k=1.0, op=0.9):
    """wobbly violet acid pool (fill + ink crest + a few rising bubbles)."""
    if k <= 0.02: return
    pts = [(x - w / 2 * k + i * w * k / 24, y - h * k * (0.5 + 0.5 * math.sin(i * 0.9 + t * 3)) * 0.4) for i in range(25)]
    poly = np.array(pts + [(x + w / 2 * k, y + h * k), (x - w / 2 * k, y + h * k)], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [poly], C(ACC), cv2.LINE_AA); f[:] = f * (1 - op) + ov * op
    cv2.polylines(f, [np.array(pts, np.int32)], False, C(INKC), 5, cv2.LINE_AA)
    for i in range(4):
        bx = x - w * 0.3 * k + i * w * 0.2 * k; by = y + h * k * 0.6 - ((t * 60 + i * 30) % (h * k * 0.6))
        cv2.circle(f, (int(bx), int(by)), 6, C(ACC_XL), 2, cv2.LINE_AA)


def saliva_wave(f, x, y, w, t, k=1.0, h=90, op=0.75):
    """mint saliva wash: a translucent wave with an ink crest, rolling left -> right as k grows."""
    if k <= 0.02: return
    x0 = x - w / 2; x1 = x0 + w * k
    pts = [(x0 + i * (x1 - x0) / 30, y - h * (0.5 + 0.5 * math.sin(i * 0.8 - t * 6)) * 0.5) for i in range(31)]
    poly = np.array(pts + [(x1, y + h), (x0, y + h)], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [poly], C(INK_MINT), cv2.LINE_AA); f[:] = f * (1 - op) + ov * op
    cv2.polylines(f, [np.array(pts, np.int32)], False, C(INKC), 5, cv2.LINE_AA)
    cv2.polylines(f, [np.array([(px, py + 10) for px, py in pts], np.int32)], False, C((255, 255, 255)), 3, cv2.LINE_AA)
    cv2.circle(f, (int(x1), int(pts[-1][1] - 10)), 14, C(INK_MINT), -1, cv2.LINE_AA); cv2.circle(f, (int(x1), int(pts[-1][1] - 10)), 14, C(INKC), 4, cv2.LINE_AA)


def minerals(f, pts, r=9, col=TOOTHW):
    for (x, y) in pts:
        cv2.circle(f, (int(x), int(y)), int(r), C(col), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), int(r), C(INKC), 3, cv2.LINE_AA)


def spit_hero_el(mood="happy"):
    """a mint saliva drop with a tiny cape — the 'rescue team' (small joke prop)."""
    def mk():
        w, h = 200, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(60, 120), (150, 92), (176, 170), (120, 150), (90, 190)], ACC, 51, INK_W - 2)                   # cape
        pts = [(100, 20), (140, 84), (150, 130), (130, 180), (100, 196), (70, 180), (50, 130), (60, 84)]
        _ink_poly(d, pts, INK_MINT, 52, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in pts], fill=255), lambda q, S_, c: q.ellipse(S_(100, 60, 170, 200), fill=c), INK_MINT_S, 110)
        _hatch_in(im, (100, 80, 160, 196), lambda q, S_: q.ellipse(S_(104, 84, 156, 194), fill=255), -40, 8, 34)
        d.ellipse(S(72, 78, 88, 98), fill=(255, 255, 255, 210))
        _face(d, S, 100, 124, 1.0, mood)
        return _done(im, w, h)
    return gcache(("spithero17", mood), mk)


# ---------------- bathroom + kitchen props ----------------
def brush_el():
    def mk():
        w, h = 420, 120; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 50), (300, 44), (330, 36), (400, 36), (404, 60), (330, 64), (300, 70), (20, 70)], TOOTHW, 61, INK_W - 1)
        d.line(S(40, 60, 290, 58), fill=INK_MINT + (255,), width=6 * SC3)
        for k in range(12): d.line(S(336 + k * 5.4, 36, 336 + k * 5.4, 8), fill=INKC + (255,), width=3 * SC3)
        d.line(S(334, 8, 400, 8), fill=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache("brush17", mk)


def paste_el():
    def mk():
        w, h = 260, 120; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 40), (200, 44), (200, 76), (20, 86)], TOOTHW, 62, INK_W - 1)
        _ink_poly(d, [(200, 50), (236, 50), (236, 70), (200, 70)], INK_MINT, 63, INK_W - 2)
        d.rectangle(S(60, 52, 170, 74), fill=INK_MINT + (255,))
        d.text((115 * SC3, 63 * SC3), "FLUORIDE", font=font(F_BLACK, 15 * SC3), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache("paste17", mk)


def glass_el(level=1.0):
    level = round(clamp(level) * 4) / 4
    def mk():
        w, h = 160, 240; im, d, S = _cv(w, h)
        if level > 0:
            y0 = 220 - 180 * level
            d.polygon(S(42 + (y0 - 40) * 0.08, y0, 118 - (y0 - 40) * 0.08, y0, 128, 220, 32, 220), fill=INK_MINT + (150,))
            d.line(S(42 + (y0 - 40) * 0.08, y0, 118 - (y0 - 40) * 0.08, y0), fill=INKC + (200,), width=3 * SC3)
        _ink_poly(d, [(38, 30), (122, 30), (130, 224), (30, 224)], None, 64, INK_W - 1)
        d.line(S(52, 50, 48, 200), fill=(255, 255, 255, 220), width=6 * SC3)
        return _done(im, w, h)
    return gcache(("glass17", level), mk)


def plate_el():
    """a plate with a meal (ink food shapes: rice mound, two rotis, a veg heap) — 'eat sweets with a meal'."""
    def mk():
        w, h = 420, 220; im, d, S = _cv(w, h)
        _ink_ell(d, 210, 150, 196, 56, TOOTHW, 71, INK_W - 1)
        _ink_ell(d, 210, 150, 150, 36, None, 72, INK_W - 3)
        _ink_ell(d, 150, 130, 70, 40, (250, 244, 222), 73, INK_W - 2)                       # rice
        for k in range(14): d.ellipse(S(100 + (k * 37) % 100, 108 + (k * 23) % 40, 106 + (k * 37) % 100, 112 + (k * 23) % 40), fill=INKC + (90,))
        _ink_ell(d, 290, 118, 54, 24, CARA, 74, INK_W - 2); _ink_ell(d, 300, 134, 54, 24, CARA, 75, INK_W - 2)   # rotis
        for k in range(5): _ink_ell(d, 230 + k * 18, 160 + 6 * (k % 2), 12, 9, INK_MINT, 76 + k, INK_W - 3)      # veg
        return _done(im, w, h)
    return gcache("plate17", mk)


def timer_el(k=0.0, label=None, R=130):
    """ink timer dial: paper face, ticks, a violet 'acid' arc from 12 o'clock to k * 360 deg, hand at the arc end."""
    k = round(clamp(k) * 60) / 60
    def mk():
        w = h = 2 * R + 40; im, d, S = _cv(w, h); cx = cy = w / 2
        d.rectangle(S(cx - 16, 14, cx + 16, 30), fill=INKC + (255,)); d.line(S(cx, 30, cx, 46), fill=INKC + (255,), width=5 * SC3)    # stop button
        _ink_ell(d, cx, cy + 10, R, R, TOOTHW, 81, INK_W, n=40, amp=1.8)
        _hatch_in(im, (cx, cy - R + 10, cx + R, cy + R + 10), lambda q, S_: q.pieslice(S_(cx - R, cy - R + 10, cx + R, cy + R + 10), -30, 120, fill=255), -40, 11, 26)
        if k > 0:
            d.pieslice(S(cx - R + 14, cy - R + 24, cx + R - 14, cy + R - 4), -90, -90 + 360 * k, fill=ACC + (200,))
        for i in range(12):
            a = math.radians(i * 30 - 90); r0 = R - 10 if i % 3 else R - 22
            d.line(S(cx + r0 * math.cos(a), cy + 10 + r0 * math.sin(a), cx + (R - 4) * math.cos(a), cy + 10 + (R - 4) * math.sin(a)), fill=INKC + (255,), width=(4 if i % 3 else 6) * SC3)
        a = math.radians(360 * k - 90)
        d.line(S(cx, cy + 10, cx + (R - 30) * math.cos(a), cy + 10 + (R - 30) * math.sin(a)), fill=INKC + (255,), width=7 * SC3)
        d.ellipse(S(cx - 10, cy, cx + 10, cy + 20), fill=INKC + (255,))
        if label: d.text((cx * SC3, (cy + 10 + R * 0.5) * SC3), label, font=font(F_BLACK, 26 * SC3), fill=ACC_S + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("timer17", k, label, R), mk)


def podium(f, x, y, w=560, h=120, t=0.0):
    pts = np.array([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 20, y + h), (x - w / 2 + 20, y + h)], np.int32)
    cv2.fillPoly(f, [pts], C(TOOTHW), cv2.LINE_AA); cv2.polylines(f, [pts], True, C(INKC), 6, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(w / 2), 22), 0, 0, 360, C(TOOTHW), -1, cv2.LINE_AA); cv2.ellipse(f, (int(x), int(y)), (int(w / 2), 22), 0, 0, 360, C(INKC), 6, cv2.LINE_AA)


def cloth(f, x, y, w, h, t=0.0, lift=0.0):
    """a violet cloth covering something on the podium; lift 0..1 pulls it up and away."""
    if lift >= 0.99: return
    yy = y - h * lift * 1.4; sx = 1 - 0.5 * lift
    pts = [(x - w / 2 * sx + i * w * sx / 20, yy - h + 8 * math.sin(i * 1.1 + t * 2)) for i in range(21)]
    poly = np.array(pts + [(x + w / 2 * sx + 20 * (1 - lift), y + 8 - 12 * lift), (x - w / 2 * sx - 20 * (1 - lift), y + 8 - 12 * lift)], np.int32)
    cv2.fillPoly(f, [poly], C(ACC), cv2.LINE_AA); cv2.polylines(f, [poly], True, C(INKC), 6, cv2.LINE_AA)
    for k in range(4): cv2.line(f, (int(x - w * 0.3 * sx + k * w * 0.2 * sx), int(yy - h + 30)), (int(x - w * 0.3 * sx + k * w * 0.2 * sx + 10), int(y - 10)), C(INKC), 2, cv2.LINE_AA)


def magnifier_ink_el():
    def mk():
        w, h = 260, 260; im, d, S = _cv(w, h)
        d.line(S(170, 170, 236, 236), fill=INKC + (255,), width=16 * SC3); d.line(S(170, 170, 236, 236), fill=CARA + (255,), width=9 * SC3)
        _ink_ell(d, 110, 110, 86, 86, (236, 244, 250), 91, INK_W + 2, n=36, amp=1.5)
        d.arc(S(50, 50, 170, 170), 200, 260, fill=(255, 255, 255, 230), width=6 * SC3)
        return _done(im, w, h)
    return gcache("magnifier17", mk)


