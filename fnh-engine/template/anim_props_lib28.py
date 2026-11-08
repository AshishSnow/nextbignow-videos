# ================= anim_props_lib28.py (ep 28, 8 Nov): DO YOU NEED A DETOX AFTER DIWALI? ONE accent: JUICE LIME (= the detox fad: the green drink, the posts, the products).
# Real organs in natural ink colours: liver = warm red-brown, kidneys = rose; fat-soluble junk = a greasy yellow blob; water-soluble = water blue.
# detox_bottle_el(level, mood, look, tilt_label), liver_el(mood, look, arms, hat), kidney_el(mood, look, flip, hat), junk_el(mood, look, packed), beaker_el(kind, level),
# jerrycan_el(), jug_el(level), prod_el(kind bottle|tea|patch|pills|powder, mood), soap_bar_el(), papers_el(n), pill_el(), pillow_el(), blanket_el(w).
ACC = (150, 192, 38); ACC_S = (88, 128, 18); ACC_L = (208, 232, 138); ACC_XL = (236, 246, 206)
LIVER = (178, 76, 64); LIVER_S = (126, 46, 40); LIVER_H = (214, 124, 106)
KID = (214, 112, 112); KID_S = (162, 70, 74)
FATY = (240, 198, 70); FATY_S = (196, 146, 36)
WATER_B = (120, 182, 236); WATER_BS = (70, 130, 196)
HAT = (246, 186, 40); HAT_S = (198, 136, 20)
MILK = (252, 248, 238)
CANB = (70, 132, 206); CANB_S = (40, 90, 160)


def _hat(d, S, cx, cy, s=1.0, seed=1):
    """a little hard hat (the night-shift workers)."""
    _ink_poly(d, _arcpts(cx, cy, 58 * s, 46 * s, 180, 360, 16), HAT, seed, INK_W - 1, amp=0.8)
    _ink_poly(d, [(cx - 78 * s, cy), (cx + 78 * s, cy), (cx + 70 * s, cy + 12 * s), (cx - 70 * s, cy + 12 * s)], HAT_S, seed + 1, INK_W - 2, amp=0.6)
    d.line(S(cx, cy - 46 * s, cx, cy - 4 * s), fill=HAT_S + (255,), width=int(8 * s * SC3))


def detox_bottle_el(level=1.0, mood=None, look=(0, 0), seed=281, label=True):
    """a tall bottle of green 'detox' juice: cream label with hand-lettered DETOX and a leaf, lime juice up to `level` (0..1)."""
    lq = round(clamp(level) * 10) / 10
    def mk():
        w, h = 240, 560; im, d, S = _cv(w, h)
        body = [(60, 150), (78, 112), (90, 70), (150, 70), (162, 112), (180, 150), (188, 210), (188, 520), (176, 540), (64, 540), (52, 520), (52, 210)]
        _ink_poly(d, body, (236, 244, 236), seed, INK_W, amp=1.0)
        if lq > 0:
            top = 530 - 360 * lq
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon([(x * SC3, y * SC3) for x, y in body], fill=255)
            liq = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(liq)
            q.rectangle(S(40, top, 200, 545), fill=ACC + (255,)); q.rectangle(S(140, top, 200, 545), fill=ACC_S + (200,))
            q.line(S(56, top, 184, top), fill=ACC_L + (255,), width=5 * SC3)
            im.alpha_composite(Image.composite(liq, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
            _ink_poly(d, body, None, seed, INK_W, amp=1.0)
        d.line(S(70, 230, 70, 470), fill=(255, 255, 255, 170), width=8 * SC3)                       # glass glint
        _ink_poly(d, [(84, 30), (156, 30), (158, 72), (82, 72)], ACC_S, seed + 1, INK_W - 1, amp=0.6)  # cap
        for x in (96, 112, 128, 144): d.line(S(x, 36, x, 66), fill=INKC + (150,), width=2 * SC3)
        if label:
            _ink_poly(d, [(56, 290), (184, 290), (184, 420), (56, 420)], MILK, seed + 2, INK_W - 2, amp=0.8)
            fn = font(F_HAND if os.path.exists(F_HAND) else F_BOLD, 40 * SC3)
            d.text(S(120, 330), "DETOX", font=fn, fill=ACC_S + (255,), anchor="mm")
            _ink_poly(d, [(120, 352), (146, 372), (120, 404), (94, 372)], ACC, seed + 3, 3, amp=0.5)
            d.line(S(120, 356, 120, 400), fill=ACC_S + (255,), width=3 * SC3)
        if mood: _face(d, S, 120, 470 if label else 360, 1.4, mood, look)
        return _done(im, w, h)
    return gcache(("detoxbottle28", lq, mood, look, seed, label), mk)


LIVER_P = [(40, 120), (70, 70), (140, 46), (240, 40), (330, 48), (392, 74), (420, 118), (404, 170), (350, 214), (270, 250), (210, 262), (160, 246), (110, 208), (60, 170)]


def liver_el(mood="n", look=(0, 0), arms=None, hat=False, seed=282, glow_=False):
    """THE LIVER as a character: a big right lobe + smaller left lobe (wedge), warm red-brown, a gallbladder nub; arms None | 'cross' | 'up' | 'work' | 'shrug'."""
    def mk():
        w, h = 470, 360; im, d, S = _cv(w, h); oy = 50
        P = [(x + 10, y + oy) for x, y in LIVER_P]
        if arms in ("up", "shrug"):
            for sg, (x0, y0) in ((-1, (70, 170)), (1, (400, 150))):
                if arms == "up": pts = [(x0, y0), (x0 + sg * 34, y0 - 60), (x0 + sg * 30, y0 - 110)]
                else: pts = [(x0, y0), (x0 + sg * 50, y0 - 10), (x0 + sg * 66, y0 - 54)]
                d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (255,), width=9 * SC3, joint="curve")
                ex, ey = pts[-1]; _ink_ell(d, ex, ey, 14, 14, INK_SKIN, seed + 20 + sg, 4, amp=0.4)
        _ink_poly(d, P, LIVER, seed, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.polygon(S_(60, 250, 200, 330, 330, 290, 430, 200, 440, 330, 40, 340), fill=c), LIVER_S, 150)
        _hatch_in(im, (40, 220, 440, 320), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), -40, 10, 34)
        d.line([(x * SC3, y * SC3) for x, y in _wob([(176, 100 + oy), (196, 160 + oy), (190, 230 + oy)], 1.2, seed + 5)], fill=LIVER_S + (255,), width=4 * SC3, joint="curve")  # the lobe groove
        d.line([(x * SC3, y * SC3) for x, y in _wob([(130, 92), (210, 80), (300, 84)], 1.0, seed + 6)], fill=LIVER_H + (230,), width=7 * SC3, joint="curve")          # highlight
        _ink_ell(d, 236, 300, 26, 18, (120, 150, 70), seed + 7, INK_W - 2, amp=0.6)                      # gallbladder nub
        if mood: _face(d, S, 300, 178, 2.0, mood, look)
        if arms == "cross":
            for sg in (-1, 1):
                d.line([(x * SC3, y * SC3) for x, y in _wob([(250 + sg * 70, 236), (300, 252), (300 - sg * 70, 244)], 0.8, seed + 9 + sg)], fill=INKC + (255,), width=10 * SC3, joint="curve")
            for sg in (-1, 1): _ink_ell(d, 300 - sg * 72, 244, 14, 13, INK_SKIN, seed + 30 + sg, 4, amp=0.4)
        if arms == "work":
            for sg, x0 in ((-1, 210), (1, 390)):
                pts = [(x0, 250), (x0 + sg * 20, 300), (x0 + sg * 2, 330)]
                d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (255,), width=9 * SC3, joint="curve"); _ink_ell(d, pts[-1][0], pts[-1][1], 14, 14, INK_SKIN, seed + 40 + sg, 4, amp=0.4)
        if hat: _hat(d, S, 300, 108, 1.0, seed + 50)
        return _done(im, w, h)
    return gcache(("liver28", mood, look, arms, hat, seed), mk)


def kidney_el(mood="n", look=(0, 0), flip=False, hat=False, seed=283):
    """a KIDNEY as a character: a rose bean with a little ureter tube from the inner curve."""
    def mk():
        w, h = 240, 330; im, d, S = _cv(w, h)
        P = []
        for a in range(0, 360, 12):
            r = math.radians(a); rx, ry = 92, 128
            x = 120 + rx * math.cos(r); y = 160 + ry * math.sin(r)
            if math.cos(r) > 0.55: x -= 46 * (math.cos(r) - 0.55) / 0.45 * (1 - abs(math.sin(r)))   # the bean's dent on the inner side
            P.append((x, y))
        if flip: P = [(240 - x, y) for x, y in P]
        ix = 196 if not flip else 44
        d.line(S(ix - (6 if not flip else -6), 170, ix + (24 if not flip else -24), 230, ix + (20 if not flip else -20), 320), fill=KID_S + (255,), width=12 * SC3, joint="curve")
        _ink_poly(d, P, KID, seed, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.ellipse(S_(60 if not flip else -40, 140, 300 if not flip else 180, 360), fill=c), KID_S, 140)
        _hatch_in(im, (30, 200, 210, 300), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), -40, 10, 30)
        hx = 82 if not flip else 158
        d.line(S(hx, 70, hx - (10 if not flip else -10), 110), fill=(246, 180, 176, 255), width=8 * SC3)
        if mood: _face(d, S, 110 if not flip else 130, 170, 1.5, mood, look)
        if hat: _hat(d, S, 110 if not flip else 130, 58, 0.75, seed + 50)
        return _done(im, w, h)
    return gcache(("kidney28", mood, look, flip, hat, seed), mk)


def junk_el(mood="n", look=(0, 0), packed=False, seed=284):
    """the stuff your body wants gone: a greasy yellow blob (dissolves in FAT). packed = the liver's new packaging: a water-blue box with a bow (dissolves in WATER)."""
    def mk():
        w, h = 260, 260; im, d, S = _cv(w, h)
        if packed:
            _ink_poly(d, [(40, 96), (220, 96), (220, 236), (40, 236)], WATER_B, seed, INK_W, amp=1.0)
            _ink_poly(d, [(28, 70), (232, 70), (232, 106), (28, 106)], (160, 206, 244), seed + 1, INK_W - 1, amp=0.8)
            _shade(im, lambda q, S_: q.rectangle(S_(40, 96, 220, 236), fill=255), lambda q, S_, c: q.rectangle(S_(150, 96, 230, 240), fill=c), WATER_BS, 130)
            d.rectangle(S(118, 70, 142, 236), fill=(250, 250, 255, 255)); d.line(S(118, 70, 118, 236), fill=INKC + (255,), width=3 * SC3); d.line(S(142, 70, 142, 236), fill=INKC + (255,), width=3 * SC3)
            for sg in (-1, 1): _ink_ell(d, 130 + sg * 34, 52, 32, 20, (250, 250, 255), seed + 3 + sg, INK_W - 2, amp=0.6)
            for j in range(3): d.ellipse(S(54 + j * 22, 200 - j * 26, 66 + j * 22, 214 - j * 26), fill=(230, 244, 255, 255))
            if mood: _face(d, S, 80, 168, 1.3, mood, look)
        else:
            P = [(130 + (96 + 12 * math.sin(a * 0.11 * 5 + seed)) * math.cos(math.radians(a)), 140 + (84 + 10 * math.cos(a * 0.07 * 5)) * math.sin(math.radians(a))) for a in range(0, 360, 15)]
            _ink_poly(d, P, FATY, seed, INK_W, amp=1.4)
            _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.ellipse(S_(80, 120, 260, 260), fill=c), FATY_S, 140)
            d.ellipse(S(70, 84, 112, 110), fill=(255, 250, 220, 230)); d.ellipse(S(120, 70, 136, 80), fill=(255, 250, 220, 200))   # greasy shine
            _ink_ell(d, 200, 218, 12, 16, FATY, seed + 4, 3, amp=0.4)                                                                # a drip
            if mood: _face(d, S, 130, 146, 1.6, mood, look)
        return _done(im, w, h)
    return gcache(("junk28", mood, look, packed, seed), mk)


def beaker_el(kind="fat", level=0.6, label=True, seed=285):
    """a lab beaker of cooking oil (kind fat, yellow) or water (kind water, blue)."""
    def mk():
        w, h = 260, 320; im, d, S = _cv(w, h)
        P = [(40, 40), (220, 40), (212, 60), (212, 290), (196, 304), (64, 304), (48, 290), (48, 60)]
        _ink_poly(d, P, (240, 246, 248), seed, INK_W, amp=0.8)
        col, cs = (FATY, FATY_S) if kind == "fat" else (WATER_B, WATER_BS)
        top = 300 - 230 * level
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon([(x * SC3, y * SC3) for x, y in P], fill=255)
        liq = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(liq); q.rectangle(S(40, top, 230, 310), fill=col + (220,)); q.rectangle(S(150, top, 230, 310), fill=cs + (160,))
        im.alpha_composite(Image.composite(liq, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
        _ink_poly(d, P, None, seed, INK_W, amp=0.8)
        for j in range(4): d.line(S(56, 110 + j * 44, 84, 110 + j * 44), fill=INKC + (200,), width=3 * SC3)
        d.line(S(70, 80, 70, 280), fill=(255, 255, 255, 180), width=6 * SC3)
        if label:
            fn = font(F_BOLD, 34 * SC3); d.text(S(140, 20), "FAT" if kind == "fat" else "WATER", font=fn, fill=INKC + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("beaker28", kind, round(level, 2), label, seed), mk)


def jerrycan_el(seed=286):
    """a big 20-litre water can (blue, handle on top)."""
    def mk():
        w, h = 240, 300; im, d, S = _cv(w, h)
        P = [(30, 70), (210, 70), (220, 90), (220, 280), (206, 292), (34, 292), (20, 280), (20, 90)]
        _ink_poly(d, P, CANB, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.rectangle(S_(150, 60, 240, 300), fill=c), CANB_S, 150)
        _ink_poly(d, [(70, 24), (170, 24), (184, 72), (150, 72), (142, 46), (98, 46), (90, 72), (56, 72)], CANB_S, seed + 1, INK_W - 1, amp=0.6)
        _ink_poly(d, [(176, 40), (204, 40), (204, 72), (176, 72)], (240, 240, 244), seed + 2, INK_W - 2, amp=0.4)
        for y in (130, 190, 250): d.line(S(36, y, 204, y), fill=CANB_S + (255,), width=4 * SC3)
        fn = font(F_BOLD, 44 * SC3); d.text(S(120, 168), "20 L", font=fn, fill=(250, 250, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("can28", seed), mk)


def jug_el(level=0.5, seed=287):
    """a small measuring jug (pale yellow liquid) with litre marks."""
    def mk():
        w, h = 220, 260; im, d, S = _cv(w, h)
        P = [(40, 40), (170, 40), (176, 230), (166, 244), (48, 244), (36, 230)]
        _ink_poly(d, P, (242, 246, 248), seed, INK_W, amp=0.8)
        top = 240 - 190 * level
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon([(x * SC3, y * SC3) for x, y in P], fill=255)
        liq = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(liq).rectangle(S(30, top, 180, 250), fill=(246, 226, 120, 230))
        im.alpha_composite(Image.composite(liq, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
        _ink_poly(d, P, None, seed, INK_W, amp=0.8)
        d.line(S(172, 80, 206, 92, 206, 170, 174, 186), fill=INKC + (255,), width=8 * SC3, joint="curve")
        for j in range(4): d.line(S(48, 90 + j * 40, 72, 90 + j * 40), fill=INKC + (200,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("jug28", round(level, 2), seed), mk)


def prod_el(kind="bottle", mood=None, look=(0, 0), seed=288):
    """a generic 'detox' product (no brands): bottle | tea (box with a leaf) | patch (foot pad) | pills (tub) | powder (pouch). All carry the lime leaf."""
    def mk():
        w, h = 200, 240; im, d, S = _cv(w, h)
        if kind == "bottle":
            _ink_poly(d, [(70, 40), (130, 40), (132, 70), (150, 90), (150, 220), (50, 220), (50, 90), (68, 70)], ACC_L, seed, INK_W - 1, amp=0.8); _ink_poly(d, [(76, 20), (124, 20), (124, 42), (76, 42)], ACC_S, seed + 1, 4, amp=0.4)
        elif kind == "tea":
            _ink_poly(d, [(36, 70), (164, 70), (164, 220), (36, 220)], (238, 226, 196), seed, INK_W - 1, amp=0.8); _ink_poly(d, [(36, 70), (60, 40), (188, 40), (164, 70)], (250, 240, 214), seed + 1, 4, amp=0.6)
        elif kind == "patch":
            _ink_poly(d, [(40, 60), (160, 60), (160, 200), (40, 200)], (250, 246, 236), seed, INK_W - 1, amp=1.2); _ink_poly(d, [(62, 82), (138, 82), (138, 178), (62, 178)], (150, 130, 110), seed + 1, 3, amp=0.8)
        elif kind == "pills":
            _ink_poly(d, [(50, 70), (150, 70), (150, 220), (50, 220)], (250, 250, 250), seed, INK_W - 1, amp=0.6); _ink_poly(d, [(44, 44), (156, 44), (156, 74), (44, 74)], ACC_S, seed + 1, 4, amp=0.4)
        else:
            _ink_poly(d, [(46, 60), (154, 60), (164, 220), (36, 220)], (246, 236, 220), seed, INK_W - 1, amp=1.0); d.line(S(50, 84, 150, 84), fill=INKC + (200,), width=3 * SC3)
        _ink_poly(d, [(100, 112), (124, 132), (100, 164), (76, 132)], ACC, seed + 3, 3, amp=0.5); d.line(S(100, 116, 100, 160), fill=ACC_S + (255,), width=3 * SC3)
        if mood: _face(d, S, 100, 190, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("prod28", kind, mood, look, seed), mk)


def soap_bar_el(seed=289):
    def mk():
        w, h = 300, 220; im, d, S = _cv(w, h)
        P = [(40, 110), (60, 80), (240, 80), (262, 110), (262, 170), (240, 194), (60, 194), (40, 170)]
        _ink_poly(d, P, (250, 238, 212), seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.rectangle(S_(40, 150, 270, 200), fill=c), (214, 192, 150), 150)
        for (x, y, r) in ((90, 66, 26), (130, 46, 18), (210, 60, 30), (250, 40, 14), (170, 30, 12)):
            _ink_ell(d, x, y, r, r, (240, 248, 255), seed + x, 3, amp=0.4); d.ellipse(S(x - r * 0.5, y - r * 0.6, x - r * 0.1, y - r * 0.2), fill=(255, 255, 255, 255))
        return _done(im, w, h)
    return gcache(("soap28", seed), mk)


def papers_el(n=5, seed=290):
    """a stack of research papers (the studies)."""
    def mk():
        w, h = 340, 300; im, d, S = _cv(w, h)
        for j in range(n):
            dx, dy = (j % 2) * 10 - 5, -j * 16
            _ink_poly(d, [(50 + dx, 120 + dy), (290 + dx, 120 + dy), (290 + dx, 270 + dy), (50 + dx, 270 + dy)], (252, 250, 244), seed + j, 4, amp=0.8)
        for k in range(5): d.line(S(80, 80 - 16 * (n - 5) + k * 24 - 16 * 4 + 64, 250 - 30 * (k % 2), 80 - 16 * (n - 5) + k * 24 - 16 * 4 + 64), fill=INKC + (150,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("papers28", n, seed), mk)


def pill_el(seed=291):
    def mk():
        w, h = 160, 90; im, d, S = _cv(w, h)
        _ink_poly(d, _arcpts(50, 45, 34, 30, 90, 270, 12) + [(80, 15), (80, 75)], (250, 250, 250), seed, 5, amp=0.4)
        _ink_poly(d, [(80, 15)] + _arcpts(110, 45, 34, 30, -90, 90, 12) + [(80, 75)], ACC, seed + 1, 5, amp=0.4)
        return _done(im, w, h)
    return gcache(("pill28", seed), mk)


def pillow_el(seed=292):
    def mk():
        w, h = 480, 200; im, d, S = _cv(w, h)
        P = [(40, 100), (70, 40), (240, 30), (410, 40), (440, 100), (410, 166), (240, 174), (70, 166)]
        _ink_poly(d, P, (250, 248, 240), seed, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.rectangle(S_(30, 120, 450, 190), fill=c), (214, 206, 196), 140)
        return _done(im, w, h)
    return gcache(("pillow28", seed), mk)


def blanket_el(w_=880, seed=293):
    def mk():
        w, h = w_, 420; im, d, S = _cv(w, h)
        P = [(20, 60), (w * 0.3, 30), (w * 0.6, 50), (w - 20, 30), (w - 10, 400), (10, 400)]
        _ink_poly(d, P, (196, 214, 236), seed, INK_W, amp=2.0)
        for k in range(1, 5): d.line(S(w * k / 5, 50, w * k / 5 + 10, 400), fill=(160, 186, 220, 255), width=6 * SC3)
        _hatch_in(im, (0, 240, w, 410), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), -40, 12, 30)
        return _done(im, w, h)
    return gcache(("blanket28", w_, seed), mk)


# ================= NEW PLACE (ep 28): INSIDE THE LIVER FACTORY — a cosy red-brown works hall: arched windows of warm light, pipes (blood vessels) along the wall,
# hanging lamps, and a sharp CONVEYOR belt in front (y ~ 1230). Draw props on the belt AFTER set_factory, then conveyor_front(f, t) for the belt's front lip.
def set_factory(t=0.0, blur=4, belt_y=1230, dim=0.0):
    def mk():
        f = _vgrad((236, 196, 176), (206, 150, 132), 0, belt_y)
        for i, x in enumerate((180, 540, 900)):
            cv2.ellipse(f, (x, 560), (130, 130), 0, 180, 360, C((150, 92, 78)), -1, cv2.LINE_AA)
            cv2.rectangle(f, (x - 130, 560), (x + 130, 900), C((150, 92, 78)), -1, cv2.LINE_AA)
            sub = _vgrad((255, 236, 196), (250, 206, 160), 440, 890)
            m = np.zeros((H, W), np.uint8); cv2.ellipse(m, (x, 570), (110, 110), 0, 180, 360, 255, -1); cv2.rectangle(m, (x - 110, 570), (x + 110, 890), 255, -1)
            f[m > 0] = sub[m > 0]
            cv2.line(f, (x, 460), (x, 890), C((150, 92, 78)), 10, cv2.LINE_AA); cv2.line(f, (x - 110, 700), (x + 110, 700), C((150, 92, 78)), 10, cv2.LINE_AA)
        for y, col in ((1000, (196, 70, 66)), (1060, (90, 110, 170))):                     # two pipes: red in (blood), blue out
            cv2.line(f, (0, y), (W, y), C(tuple(int(c * 0.7) for c in col)), 34, cv2.LINE_AA); cv2.line(f, (0, y - 6), (W, y - 6), C(col), 22, cv2.LINE_AA)
            for x in range(60, W, 240): cv2.rectangle(f, (x - 14, y - 22), (x + 14, y + 22), C((120, 84, 70)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (0, belt_y - 20), (W, H), C((120, 80, 66)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("factory28", blur, belt_y), mk).copy()
    for x in (300, 780):
        cv2.line(f, (x, 0), (x, 300), C((70, 50, 44)), 4, cv2.LINE_AA)
        cv2.ellipse(f, (x, 320), (60, 34), 0, 180, 360, C((60, 46, 40)), -1, cv2.LINE_AA)
        glow(f, x, 360, 260, (255, 226, 170), 0.30 * (1 - dim))
    if dim > 0: f *= (1 - 0.55 * dim)
    dust_motes(f, t, 100, 400, 980, 1100, 12, 8, 0.35)
    return inkify(f)


def conveyor(f, t, y=1230, speed=160.0, x0=-20, x1=1100):
    """the belt: a dark rubber top with moving cleats + rollers turning underneath. Props ride at y - (their half height)."""
    cv2.rectangle(f, (x0, y - 16), (x1, y + 20), C((70, 62, 60)), -1, cv2.LINE_AA)
    off = (t * speed) % 80
    for x in np.arange(x0 - 80 + off, x1, 80): cv2.line(f, (int(x), y - 14), (int(x), y + 18), C((110, 100, 96)), 4, cv2.LINE_AA)
    cv2.line(f, (x0, y - 16), (x1, y - 16), C(INKC), 6, cv2.LINE_AA)
    for x in range(40, 1080, 120):
        cv2.circle(f, (x, y + 52), 30, C((150, 140, 136)), -1, cv2.LINE_AA); cv2.circle(f, (x, y + 52), 30, C(INKC), 5, cv2.LINE_AA)
        a = t * speed / 30 + x
        cv2.line(f, (x, y + 52), (int(x + 26 * math.cos(a)), int(y + 52 + 26 * math.sin(a))), C(INKC), 4, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y + 86), (x1, y + 104), C((96, 66, 54)), -1); cv2.line(f, (x0, y + 86), (x1, y + 86), C(INKC), 6, cv2.LINE_AA)


def machine_el(lit=0, seed=294):
    """the liver's sorting machine: a hopper on top, a body with step lamps 1 and 2, an outlet chute on the right."""
    lq = int(lit)
    def mk():
        w, h = 420, 520; im, d, S = _cv(w, h)
        _ink_poly(d, [(70, 40), (350, 40), (290, 150), (130, 150)], (196, 120, 100), seed, INK_W, amp=1.0)
        _ink_poly(d, [(60, 150), (360, 150), (360, 470), (60, 470)], (226, 170, 140), seed + 1, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.rectangle(S_(60, 150, 360, 470), fill=255), lambda q, S_, c: q.rectangle(S_(260, 150, 370, 480), fill=c), (170, 106, 84), 150)
        _ink_poly(d, [(360, 360), (414, 380), (414, 470), (360, 470)], (196, 120, 100), seed + 2, INK_W - 1, amp=0.8)
        fn = font(F_BOLD, 40 * SC3)
        for i, x in enumerate((140, 280)):
            on = lq > i
            _ink_ell(d, x, 250, 46, 46, (255, 222, 120) if on else (150, 120, 110), seed + 3 + i, INK_W - 1, amp=0.6)
            d.text(S(x, 250), str(i + 1), font=fn, fill=INKC + (255,), anchor="mm")
        for k in range(3): d.line(S(100, 360 + k * 30, 320, 360 + k * 30), fill=INKC + (90,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("machine28", lq, seed), mk)
