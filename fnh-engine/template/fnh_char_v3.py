# ================= Chubby v3 — "Pixar kid" (owner, 28 Oct: "the 3D character is not looking good; make him more interesting") =================
# Loaded AFTER fnh_char3d.py; same API (chub, chub_head_el, chub_body_el, chub_head_only, grip_hand, logo_el) so every episode
# and the template keep working. Keeps v2's light model (_inflate / _Cv, key light top-left, warm rim, warm-brown outlines).
# What changed: a FACE with personality (big lidded eyes with a hazel iris and two catchlights, eyebrows shaped per emotion,
# a button nose, blush + freckles, a mouth with teeth and tongue), a messy hair mop with a cowlick, a neck, shoulders, a cream
# chef's APRON over the mint hoodie (signature item) with rolled sleeves, HANDS with fingers that point along the arm, jeans with
# turn-ups, idle life (pass t= for breathing + blinks) and a slight head tilt with `lean`.
APRON3 = (247, 238, 218); APRON3_D = (188, 168, 136); APRON3_H = (255, 252, 244)
IRIS3 = (128, 84, 40); IRIS3_D = (70, 42, 18); PUPIL3 = (28, 20, 18)
LIP3 = (190, 96, 86); MOUTH3 = (96, 30, 36); TONGUE3 = (232, 108, 112); TEETH3 = (252, 250, 246)
FRECK3 = (206, 150, 116); BLUSH3 = (245, 130, 120)


def _mix3(a, b, k): return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


# ---------------- head ----------------
def chub_head_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n", tint=0.0, nose=None, cap=False):
    tint = round(clamp(tint) * 10) / 10
    if nose is not None: nose = round(clamp(nose) * 10) / 10
    key = ("chead4", mouth, blink, brow, lx, ly, expr, tint, nose, cap)
    if key in _gc: return _gc[key]
    skin, skin_d, skin_h = _mix3(SKIN3, (255, 150, 52), tint), _mix3(SKIN3_D, (206, 96, 30), tint), _mix3(SKIN3_H, (255, 196, 120), tint)
    W_, H_ = 250, 270; cv = _Cv(W_, H_, 3); cx, cy = 125, 140
    # ears (behind the head), with an inner curve
    for sgn in (-1, 1):
        ex = cx + sgn * 92
        me = cv.mask(lambda d, S, ex=ex: d.ellipse(S(ex - 18, cy - 10, ex + 18, cy + 34), fill=255))
        cv.shaded(me, skin, skin_d, skin_h, outline=5, rim_amt=0.2)
    # head: wide round cranium + softer rounded jaw -> a kid's face, slightly taller than wide
    mh = cv.mask(lambda d, S: [d.ellipse(S(cx - 94, cy - 104, cx + 94, cy + 76), fill=255), d.ellipse(S(cx - 80, cy - 30, cx + 80, cy + 110), fill=255)])
    mh = cv2.GaussianBlur(mh, (0, 0), 6); mh = np.clip((mh - 0.5) * 6 + 0.5, 0, 1)
    cv.shaded(mh, skin, skin_d, skin_h, outline=6, flat=1.0, spec=0.16, shin=30)
    # hair: a messy mop of overlapping tufts with volume + a cowlick, drawn OVER the forehead
    tufts = [(26, 48, 140, 122), (84, 30, 190, 110), (140, 44, 226, 120), (14, 76, 76, 134), (192, 80, 238, 138), (118, 22, 166, 70), (62, 36, 120, 84), (168, 34, 214, 80)]
    mhair = cv.mask(lambda d, S: [d.ellipse(S(*t_), fill=255) for t_ in tufts])
    mhair = mhair * (1 - cv.mask(lambda d, S: d.ellipse(S(cx - 74, 86, cx + 74, 220), fill=255)))       # keep the face clear
    mhair = cv2.GaussianBlur(mhair, (0, 0), 5); mhair = np.clip((mhair - 0.5) * 4 + 0.5, 0, 1)
    cv.shaded(mhair, HAIR3, (40, 24, 16), (118, 82, 58), outline=5, flat=0.6, spec=0.08, shin=8, rim_amt=0.3, wrap=0.45)
    im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
    for (x0, y0, x1, y1, a0, a1) in ((40, 70, 110, 130, 200, 260), (96, 44, 170, 110, 210, 280), (150, 54, 222, 126, 220, 290)):   # soft strand curves
        d.arc(S(x0, y0, x1, y1), a0, a1, fill=(126, 88, 62, 70), width=2 * 3)
    for (a, b, c_, e_) in ((36, 110, 48, 100), (214, 112, 224, 100)):                                                       # sideburn wisps
        d.line(S(a, b, c_, e_), fill=HAIR3 + (255,), width=3 * 3)
    # cheeks: blush + 3 freckles each
    for sgn in (-1, 1):
        bx = cx + sgn * 56
        _ov(im, lambda q, bx=bx: q.ellipse(S(bx - 22, 168, bx + 22, 188), fill=BLUSH3 + (80,)))
        for (fx, fy) in ((bx - 8, 170), (bx + 4, 176), (bx - 2, 184)): d.ellipse(S(fx - 2, fy - 2, fx + 2, fy + 2), fill=FRECK3 + (200,))
    # ---- eyes: big, lidded, hazel iris, two catchlights ----
    ox, oy = lx * 7, ly * 6
    ey = 142
    for i, sgn in enumerate((-1, 1)):
        ex = cx + sgn * 40
        big = expr == "wow"
        rx, ry = (28, 33) if big else (24, 29)
        closed = blink or (expr == "happy" and mouth == 3)
        if closed:   # laughing / blinking: curved closed lids with lashes
            d.arc(S(ex - rx, ey - 12, ex + rx, ey + 16), 200, 340, fill=OUT3 + (255,), width=7 * 3)
            d.line(S(ex + sgn * (rx - 4), ey - 2, ex + sgn * (rx + 4), ey + 4), fill=OUT3 + (255,), width=4 * 3)
            continue
        # eye white with a soft top shadow
        d.ellipse(S(ex - rx, ey - ry, ex + rx, ey + ry), fill=(252, 250, 246, 255))
        _ov(im, lambda q, ex=ex, rx=rx, ry=ry: q.chord(S(ex - rx, ey - ry, ex + rx, ey + ry), 190, 350, fill=(150, 120, 110, 60)))
        ir = 16 if not big else 13; pr = 8 if not big else 6
        px, py = ex + ox * 0.9, ey + 4 + oy * 0.9
        d.ellipse(S(px - ir, py - ir, px + ir, py + ir), fill=IRIS3_D + (255,))
        d.ellipse(S(px - ir + 3, py - ir + 3, px + ir - 3, py + ir - 3), fill=IRIS3 + (255,))
        _ov(im, lambda q, px=px, py=py, ir=ir: q.chord(S(px - ir + 3, py - ir + 3, px + ir - 3, py + ir - 3), 0, 180, fill=(190, 140, 70, 110)))
        d.ellipse(S(px - pr, py - pr, px + pr, py + pr), fill=PUPIL3 + (255,))
        d.ellipse(S(px - ir * 0.55 - 2, py - ir * 0.6 - 2, px - ir * 0.55 + 6, py - ir * 0.6 + 6), fill=(255, 255, 255, 255))
        _ov(im, lambda q, px=px, py=py, ir=ir: q.ellipse(S(px + ir * 0.35, py + ir * 0.35, px + ir * 0.35 + 5, py + ir * 0.35 + 5), fill=(255, 255, 255, 190)))
        # lids: how much the upper lid covers (per expression), drawn as skin over the eye + a lash line
        cover = {"n": 0.14, "wow": 0.0, "sus": 0.50, "sleepy": 0.66, "sad": 0.22, "smirk": 0.42 if i == 0 else 0.14, "happy": 0.08}.get(expr, 0.14)
        if cover > 0:
            top = ey - ry; yl = top + 2 * ry * cover
            if expr == "sad":    # outer corner droops
                yo = yl + 12; yi = yl - 6
                pts = [(ex - rx - 3, top - 3), (ex + rx + 3, top - 3), (ex + rx + 3, yo if sgn > 0 else yi), (ex - rx - 3, yi if sgn > 0 else yo)]
                d.polygon([(p[0] * 3, p[1] * 3) for p in pts], fill=skin + (255,))
                d.line(S(ex - rx, yi if sgn > 0 else yo, ex + rx, yo if sgn > 0 else yi), fill=OUT3 + (255,), width=6 * 3)
            else:
                d.rectangle(S(ex - rx - 3, top - 3, ex + rx + 3, yl), fill=skin + (255,))
                d.line(S(ex - rx, yl, ex + rx, yl), fill=OUT3 + (255,), width=6 * 3)
                if expr == "sleepy": d.arc(S(ex - rx + 2, ey + ry - 6, ex + rx - 2, ey + ry + 8), 20, 160, fill=(150, 110, 160, 255), width=4 * 3)
        # upper lash line follows the eye's top edge (thicker toward the outer corner) + lower lid
        d.arc(S(ex - rx, ey - ry, ex + rx, ey + ry), 190, 350, fill=OUT3 + (255,), width=5 * 3)
        d.line(S(ex + sgn * (rx - 2), ey - ry * 0.55, ex + sgn * (rx + 6), ey - ry * 0.75), fill=OUT3 + (255,), width=4 * 3)
        d.arc(S(ex - rx, ey - ry, ex + rx, ey + ry), 30, 150, fill=skin_d + (200,), width=3 * 3)
        if expr == "happy":      # cheeks push the lower lid up (the Pixar smile-eye)
            d.chord(S(ex - rx - 3, ey - ry + 2 * ry * 0.55, ex + rx + 3, ey + ry + 3), 0, 180, fill=skin + (255,))
            d.arc(S(ex - rx, ey - ry * 0.1, ex + rx, ey + ry + 2), 10, 170, fill=OUT3 + (255,), width=5 * 3)
    # ---- eyebrows: thick, tapered, shaped per emotion (asymmetric for sus / smirk) ----
    by = 98
    for i, sgn in enumerate((-1, 1)):
        ex = cx + sgn * 40
        inn, out = ex - sgn * 20, ex + sgn * 22           # inner / outer end
        if brow == "up": yi, yo, th = by - 10, by - 4, 9
        elif brow == "sus": yi, yo, th = by + 6, by - 2, 10
        elif brow == "sad": yi, yo, th = by - 8, by + 6, 9
        else: yi, yo, th = by, by - 2, 9
        if expr == "smirk": yi, yo = (by - 12, by - 6) if i == 1 else (by + 4, by)
        if expr == "wow": yi, yo = yi - 8, yo - 8
        if expr == "sus" and brow == "n": yi, yo = by + 6, by - 2
        mid = ((inn + out) / 2, (yi + yo) / 2 - 3)
        pts = [(inn, yi - th * 0.35), (mid[0], mid[1] - th * 0.7), (out, yo - th * 0.5), (out, yo + th * 0.5), (mid[0], mid[1] + th * 0.6), (inn, yi + th * 0.35)]
        d.polygon([(p[0] * 3, p[1] * 3) for p in pts], fill=HAIR3 + (255,))
    # ---- nose: small button nose with a highlight ----
    nc = skin if nose is None else _mix3(skin, (255, 150, 52), nose)
    d.ellipse(S(cx - 11, 160, cx + 11, 178), fill=_mix3(nc, skin_d, 0.25) + (255,))
    _ov(im, lambda q: q.ellipse(S(cx - 7, 162, cx + 1, 169), fill=(255, 255, 255, 140)))
    d.arc(S(cx - 12, 158, cx + 12, 180), 20, 160, fill=skin_d + (230,), width=3 * 3)
    if cap:
        d.chord(S(cx - 98, 34, cx + 98, 150), 180, 360, fill=(120, 72, 40, 255), outline=OUT3 + (255,), width=5 * 3)
        for ex in (cx - 40, cx + 40):
            d.ellipse(S(ex - 24, 64, ex + 24, 108), fill=(60, 120, 150, 255), outline=OUT3 + (255,), width=5 * 3)
            _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 14, 72, ex - 2, 86), fill=(200, 240, 255, 200)))
        d.line(S(cx - 16, 86, cx + 16, 86), fill=OUT3 + (255,), width=6 * 3)
    # ---- mouth: lips, teeth, tongue ----
    mx, my = cx, 204
    if expr == "wow" and mouth == 0: mouth = "o"
    def lips(x0, y0, x1, y1, a0, a1, w=6):
        d.arc(S(x0, y0, x1, y1), a0, a1, fill=OUT3 + (255,), width=w * 3)
    if mouth == 0:
        if expr == "sad":
            lips(mx - 22, my, mx + 22, my + 22, 200, 340)
            d.ellipse(S(mx - 26, my + 14, mx - 20, my + 20), fill=OUT3 + (255,)); d.ellipse(S(mx + 20, my + 14, mx + 26, my + 20), fill=OUT3 + (255,))
        elif expr == "smirk":
            lips(mx - 26, my - 20, mx + 22, my + 10, 20, 110, 6)
            d.ellipse(S(mx + 18, my - 8, mx + 26, my), fill=OUT3 + (255,))
        elif expr == "happy":
            d.chord(S(mx - 32, my - 22, mx + 32, my + 22), 0, 180, fill=MOUTH3 + (255,))
            d.rectangle(S(mx - 24, my - 2, mx + 24, my + 7), fill=TEETH3 + (255,))
            for k in range(-2, 3): d.line(S(mx + k * 10, my - 1, mx + k * 10, my + 7), fill=(200, 196, 190, 255), width=1 * 3)
            d.chord(S(mx - 16, my + 4, mx + 16, my + 22), 0, 180, fill=TONGUE3 + (255,))
            lips(mx - 32, my - 22, mx + 32, my + 22, 0, 180, 5)
            for sgn in (-1, 1): d.ellipse(S(mx + sgn * 34 - 4, my - 6, mx + sgn * 34 + 4, my + 2), fill=skin_d + (160,))   # dimples
        else:
            lips(mx - 20, my - 14, mx + 20, my + 8, 20, 160, 6)
            for sgn in (-1, 1): d.ellipse(S(mx + sgn * 21 - 3, my - 2, mx + sgn * 21 + 3, my + 4), fill=OUT3 + (255,))
    elif mouth == "o":
        d.ellipse(S(mx - 14, my - 12, mx + 14, my + 18), fill=MOUTH3 + (255,), outline=OUT3 + (255,), width=4 * 3)
        d.chord(S(mx - 9, my + 4, mx + 9, my + 18), 0, 180, fill=TONGUE3 + (255,))
        _ov(im, lambda q: q.arc(S(mx - 14, my - 12, mx + 14, my + 18), 200, 340, fill=LIP3 + (120,), width=3 * 3))
    else:
        hh = {1: 10, 2: 17, 3: 24}[mouth]; ww = {1: 18, 2: 23, 3: 27}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 7, mx + ww, my - 7 + hh * 1.5), int(hh * 0.7) * 3, fill=MOUTH3 + (255,), outline=OUT3 + (255,), width=4 * 3)
        d.rounded_rectangle(S(mx - ww + 5, my - 6, mx + ww - 5, my + 1), 2 * 3, fill=TEETH3 + (255,))
        if mouth >= 2: d.chord(S(mx - ww * 0.6, my - 7 + hh * 0.75, mx + ww * 0.6, my - 7 + hh * 1.5), 0, 180, fill=TONGUE3 + (255,))
    # chin crease
    d.arc(S(cx - 10, 226, cx + 10, 238), 20, 160, fill=skin_d + (150,), width=3 * 3)
    el = _done(im, W_, H_)
    if len(_gc) < 900: _gc[key] = el
    return el


# ---------------- body: shoulders + hoodie + chef's apron ----------------
def chub_body_el(shirt=HOOD3, logo=True):
    if tuple(shirt) == tuple(CH_SHIRT): shirt = HOOD3
    def mk():
        base = tuple(shirt); dark = tuple(int(c * 0.45) for c in base); hi = tuple(min(255, int(c + 70)) for c in base)
        W_, H_ = 320, 300; cv = _Cv(W_, H_, 2); cx = 160
        # torso: rounded shoulders + a chubby belly (two shapes blended)
        mb = cv.mask(lambda d, S: [d.rounded_rectangle(S(30, 36, 290, 200), 58 * 2, fill=255), d.ellipse(S(38, 80, 282, 292), fill=255)])
        mb = cv2.GaussianBlur(mb, (0, 0), 5); mb = np.clip((mb - 0.5) * 6 + 0.5, 0, 1)
        cv.shaded(mb, base, dark, hi, outline=6, flat=0.8, spec=0.1)
        # hood collar folded behind the neck
        mcol = cv.mask(lambda d, S: d.chord(S(84, 8, 236, 84), 180, 360, fill=255)) * (1 - cv.mask(lambda d, S: d.ellipse(S(112, 20, 208, 76), fill=255)))
        cv.shaded(mcol, tuple(int(c * 0.78) for c in base), dark, hi, outline=4, flat=0.6)
        # apron: bib + skirt, cream, matte
        mbib = cv.mask(lambda d, S: d.polygon(S(112, 66, 208, 66, 224, 150, 96, 150), fill=255))
        mskirt = cv.mask(lambda d, S: d.rounded_rectangle(S(52, 142, 268, 300), 34 * 2, fill=255)) * mb
        mapron = np.clip(np.maximum(mbib, mskirt), 0, 1)
        cv.outline(mapron, 4)
        cv.put(_inflate(mapron, APRON3, APRON3_D, APRON3_H, flat=0.5, spec=0.03, shin=6, wrap=0.6, rim_amt=0.12, ao=0.1), mapron)
        im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
        # neck strap + waist ties
        for x0 in (118, 202): d.line(S(x0, 68, 160 + (x0 - 160) * 0.55, 34), fill=APRON3_D + (255,), width=5 * 2)
        d.rectangle(S(52, 146, 268, 162), fill=tuple(int(c * 0.9) for c in APRON3_D) + (255,))
        d.line(S(52, 146, 268, 146), fill=OUT3 + (200,), width=2 * 2); d.line(S(52, 162, 268, 162), fill=OUT3 + (200,), width=2 * 2)
        for (x0, y0, x1, y1) in ((252, 154, 290, 136), (252, 154, 294, 170)):      # bow at the hip
            d.line(S(x0, y0, x1, y1), fill=APRON3_D + (255,), width=10 * 2); d.line(S(x0, y0, x1, y1), fill=OUT3 + (200,), width=2 * 2)
        d.ellipse(S(246, 148, 262, 164), fill=APRON3 + (255,), outline=OUT3 + (220,), width=2 * 2)
        # apron seams + pocket + folds
        _ov(im, lambda q: q.line(S(118, 72, 112, 148), fill=APRON3_D + (120,), width=3 * 2))
        _ov(im, lambda q: q.line(S(202, 72, 208, 148), fill=APRON3_D + (120,), width=3 * 2))
        d.rounded_rectangle(S(110, 186, 210, 250), 14 * 2, fill=_mix3(APRON3, APRON3_D, 0.18) + (255,), outline=OUT3 + (200,), width=3 * 2)
        _ov(im, lambda q: q.line(S(118, 192, 202, 192), fill=APRON3_H + (200,), width=3 * 2))
        for (a0, a1, b0, b1, s0, s1) in ((60, 170, 130, 300, 230, 300), (190, 170, 262, 300, 240, 310), (90, 200, 240, 310, 250, 290)):
            _ov(im, lambda q, a0=a0, a1=a1, b0=b0, b1=b1, s0=s0, s1=s1: q.arc(S(a0, a1, b0, b1), s0, s1, fill=APRON3_D + (110,), width=4 * 2))
        # hoodie folds at the armpits + sleeve seams
        for (a0, a1, b0, b1, s0, s1) in ((34, 70, 96, 160, 200, 290), (224, 70, 286, 160, 250, 340)):
            _ov(im, lambda q, a0=a0, a1=a1, b0=b0, b1=b1, s0=s0, s1=s1: q.arc(S(a0, a1, b0, b1), s0, s1, fill=dark + (100,), width=4 * 2))
        if logo:   # FNH leaf badge on the pocket
            d.ellipse(S(146, 204, 174, 232), fill=(250, 248, 240, 255), outline=OUT3 + (220,), width=2 * 2)
            d.polygon(S(160, 208, 170, 218, 160, 228, 150, 218), fill=base + (255,))
            d.line(S(160, 212, 160, 226), fill=dark + (255,), width=1 * 2)
        return _done(im, W_, H_)
    return gcache(("cbody4", tuple(shirt), logo), mk)


# ---------------- hands with fingers (fingers point UP in the element; rotated along the forearm per frame) ----------------
def _hand_el(tint=0.0, side=1):
    tint = round(clamp(tint) * 10) / 10
    def mk():
        skin, skin_d, skin_h = _mix3(SKIN3, (255, 150, 52), tint), _mix3(SKIN3_D, (206, 96, 30), tint), _mix3(SKIN3_H, (255, 196, 120), tint)
        cv = _Cv(104, 112, 3)
        def shp(d, S):
            d.rounded_rectangle(S(24, 42, 82, 100), 22 * 3, fill=255)                   # palm
            for k, (fx, fy, fh) in enumerate(((31, 20, 46), (46, 10, 58), (61, 12, 56), (75, 24, 44))):   # four fingers
                d.rounded_rectangle(S(fx - 7, fy, fx + 7, fy + fh), 7 * 3, fill=255)
            d.rounded_rectangle(S(4, 52, 34, 70), 9 * 3, fill=255)                      # thumb (left side)
        m = cv.mask(shp); m = cv2.GaussianBlur(m, (0, 0), 1.8); m = np.clip((m - 0.5) * 6 + 0.5, 0, 1)
        cv.shaded(m, skin, skin_d, skin_h, outline=4, flat=0.6, spec=0.1, wrap=0.45)
        im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
        for fx in (38, 53, 68): d.line(S(fx, 44, fx, 74), fill=skin_d + (150,), width=2 * 3)        # finger gaps
        d.arc(S(30, 66, 76, 96), 200, 340, fill=skin_d + (110,), width=2 * 3)                       # palm crease
        el = _done(im, 104, 112)
        if side < 0: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
        return el
    return gcache(("hand4", tint, side), mk)


def _mitt_el(tint=0.0):      # kept for callers that composite a bare hand (grip_hand etc.)
    return _hand_el(tint, 1)


def _sneaker_el(side=1):
    def mk():
        cv = _Cv(116, 64, 3)
        mu = cv.mask(lambda d, S: [d.rounded_rectangle(S(12, 10, 104, 50), 20 * 3, fill=255), d.ellipse(S(60, 4, 108, 46), fill=255)])
        cv.shaded(mu, (248, 246, 240), (178, 172, 166), (255, 255, 255), outline=4, flat=0.6, rim_amt=0.1)
        im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
        d.rounded_rectangle(S(8, 42, 108, 58), 8 * 3, fill=(214, 208, 200, 255), outline=OUT3 + (255,), width=3 * 3)
        d.polygon(S(14, 44, 50, 36, 50, 44), fill=HOOD3 + (255,))                                   # mint swoosh-free side panel
        d.line(S(74, 14, 100, 30), fill=OUT3 + (120,), width=2 * 3)
        for i in range(3): d.line(S(30 + i * 10, 14, 36 + i * 10, 26), fill=(150, 146, 140, 255), width=2 * 3)
        d.ellipse(S(24, 12, 34, 22), fill=(236, 232, 226, 255), outline=OUT3 + (200,), width=2 * 3)   # eyelet/tongue tab
        el = _done(im, 116, 64)
        if side < 0: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
        return el
    return gcache(("sneak4", side), mk)


def _rot_el(el, ang):
    """rotate an element by ang degrees (CCW on screen) around its centre; returns a new (premult, alpha)."""
    pm, a = el; h, w = a.shape; D = int(math.hypot(w, h)) + 8
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0); M[0, 2] += D / 2 - w / 2; M[1, 2] += D / 2 - h / 2
    return cv2.warpAffine(pm, M, (D, D), flags=cv2.INTER_LINEAR), cv2.warpAffine(a, M, (D, D), flags=cv2.INTER_LINEAR)


# ---------------- the character ----------------
def chub(f, x, y, s=1.0, la=(20, 10), ra=(20, 10), ll=6, rl=6, mouth=0, blink=False, brow="n", look=(0, 0), expr="n", tint=0.0,
         hold=None, hold_off=(0, 0), hold_l=None, bob=0.0, op=1.0, shirt=HOOD3, shadow=True, lean=0.0, squash=0.0, sit=False, nose=None, cap=False,
         hold_front=False, t=None):
    """Chubby v3. (x, y) = feet baseline; height ~ 480*s; head centre ~ (x, y - 420*s). Pass t= for idle life (breathing, blinks).
    Arms (upper, fore) in degrees from straight down, + = outward. Returns {-1: left hand, 1: right hand} positions."""
    g = f if op >= 0.999 else f.copy()
    if tuple(shirt) == tuple(CH_SHIRT): shirt = HOOD3
    if t is not None:
        bob = bob + 3.0 * math.sin(t * 2.4)
        if not blink: blink = blink_at(t, int(x) % 7)
    sq = 1 + 0.12 * squash
    if shadow:
        contact(g, x, y + 6 * s, 300 * s, 0.42); contact(g, x, y + 2 * s, 170 * s, 0.30)
    hipy = y - 112 * s * (1 / sq)
    # legs: jeans with turn-ups, chunkier
    for side, ang in ((-1, ll), (1, rl)):
        hx_ = x + side * 52 * s
        if sit:
            kn = (hx_ + side * 30 * s, hipy + 20 * s); ft = (hx_ + side * 40 * s, y)
            _limb(g, ((hx_, hipy), kn, ft), (23 * s, 23 * s, 21 * s), JEAN3, JEAN3_D, JEAN3_H)
        else:
            ft = (hx_ + side * math.sin(math.radians(ang)) * 104 * s, hipy + math.cos(math.radians(ang)) * 104 * s)
            _tube(g, (hx_, hipy), ft, 23 * s, JEAN3, JEAN3_D, JEAN3_H)
            cuff = (hx_ + (ft[0] - hx_) * 0.86, hipy + (ft[1] - hipy) * 0.86)
            cv2.circle(g, (int(cuff[0]), int(cuff[1])), int(25 * s), C(OUT3), -1, cv2.LINE_AA)
            cv2.circle(g, (int(cuff[0]), int(cuff[1])), int(22 * s), C(JEAN3_H), -1, cv2.LINE_AA)
        comp(g, scale_el(_sneaker_el(side), s), ft[0] + side * 14 * s, ft[1] + 2 * s)
    lr = math.radians(lean)
    bcx = x + 40 * s * math.sin(lr); bcy = y - 222 * s / sq + bob * s * 0.5
    el = scale_el(chub_body_el(shirt), s)
    if t is not None or abs(sq - 1) > 1e-3:
        br = 1 + (0.012 * math.sin(t * 2.4) if t is not None else 0.0)
        el = scale_xy(el, (1 + 0.1 * squash) * br, (1 / sq) / br)
    comp(g, el, bcx, bcy)
    base = tuple(shirt); dark = tuple(int(c * 0.58) for c in base); hi = tuple(min(255, int(c + 34)) for c in base)
    cuffc = tuple(int(c * 0.8) for c in base)
    hands = {}; fore = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sh_ = (bcx + side * 118 * s, bcy - 46 * s)      # same shoulder as v1/v2 -> arm_ik helpers keep working
        e = (sh_[0] + side * math.sin(math.radians(a1)) * 76 * s, sh_[1] + math.cos(math.radians(a1)) * 76 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 70 * s, e[1] + math.cos(math.radians(a2)) * 70 * s)
        _limb(g, (sh_, e, hd), (21 * s, 19 * s, 17 * s), base, dark, hi)
        # rolled sleeve cuff: a thick band two-thirds down the forearm
        c0 = (e[0] + (hd[0] - e[0]) * 0.55, e[1] + (hd[1] - e[1]) * 0.55); c1 = (e[0] + (hd[0] - e[0]) * 0.8, e[1] + (hd[1] - e[1]) * 0.8)
        _tube(g, c0, c1, 21 * s, cuffc, dark, hi, ow=3.5)
        hands[side] = hd; fore[side] = math.degrees(math.atan2(hd[1] - e[1], hd[0] - e[0]))
    def hand_at(side):
        ang = -(fore[side] + 90)                       # the element's fingers point up; turn them along the forearm
        hel = scale_el(_hand_el(tint, side), s)
        comp(g, _rot_el(hel, ang), hands[side][0], hands[side][1])
    if hold is not None and not hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    if hold_l is not None:
        hx, hy = hands[-1]; comp(g, hold_l, hx - hold_off[0] * s, hy + hold_off[1] * s)
    hand_at(-1); hand_at(1)
    # neck + head (the head tilts a little with lean)
    hxc, hyc = bcx + 14 * s * math.sin(lr), bcy - 214 * s / sq + bob * s
    _tube(g, (bcx, bcy - 100 * s), (hxc, hyc + 60 * s), 26 * s, SKIN3, SKIN3_D, SKIN3_H, ow=3.0)
    comp(g, _chin_ao(s), hxc, hyc + 92 * s)
    hel = scale_el(chub_head_el(mouth, blink, brow, look[0], look[1], expr, tint, nose, cap), s)
    if abs(lean) > 0.5: hel = _rot_el(hel, -lean * 0.6)
    comp(g, hel, hxc, hyc)
    if hold is not None and hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s); hand_at(1)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


def chub_head_only(f, x, y, s, t=0.0, mouth=None, expr="n", brow="n", look=(0, 0), tint=0.0, blink=None, nose=None, cap=False, op=1.0):
    m = talk(t) if mouth is None else mouth
    b = blink_at(t, 1) if blink is None else blink
    comp(f, scale_el(chub_head_el(m, b, brow, look[0], look[1], expr, tint, nose, cap), s), x, y, op=op)


def grip_hand(f, x, y, s=1.0, tint=0.0):
    comp(f, scale_el(_hand_el(tint, 1), s * 0.95), x, y)


def logo_el():
    def mk():
        w, h, sc = 940, 380, 2; im, d = _canvas(w, h)
        hp = _pil_from_el(chub_head_el(0, False, "up", 0, 0, "happy"), 196 * sc, 212 * sc); im.alpha_composite(hp, (int(8 * sc), int(22 * sc)))
        fo = font(F_BLACK, 150 * sc); x = 215 * sc
        for ch in "FRESH": d.text((x, 128 * sc), ch, font=fo, fill=HOOD3 + (255,), anchor="lm"); x += fo.getlength(ch) - 4 * sc
        d.text((219 * sc, 272 * sc), "NEST HUB", font=font(F_BLACK, 112 * sc), fill=INK + (255,), anchor="lm")
        return _done(im, w, h)
    return gcache("logo_fnh4", mk)
