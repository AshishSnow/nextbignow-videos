# ================= anim_props_lib29.py (ep 29, 9 Nov): WHY DOES GARLIC BREATH LAST SO LONG? ONE accent: GARLIC MAUVE (= the smell: the gases, AMS, the stink).
# Real things keep natural ink colours: garlic = cream with mauve streaks (the accent's home), lungs = coral pink, blood = red, apple = red, lettuce / mint = greens, milk = white.
# garlic_bulb_el(mood, look), clove_el(mood, look, crush), alliin_el(mood, look), enzyme_el(mood, look, bite), allicin_el(mood), gas_el2(mood, look, seed),
# ams_el(mood, look), lungs_el(mood, look, k), lettuce_el(mood, look), mint_sprig_el(mood, look), naan_el(), red_apple(mood, look, cut),
# breath_meter_el(level), tongue_teeth_el(bits), sweat_drop_el(mood), set_office(t, dim) + office_front(f, top_y), (kinetic type = anim_fx.kin_word).
ACC = (150, 96, 168); ACC_S = (104, 58, 124); ACC_L = (214, 186, 226); ACC_XL = (238, 226, 244)
GAR = (248, 242, 226); GAR_S = (214, 202, 178); GAR_ST = (176, 128, 186)
LUNG = (238, 140, 136); LUNG_S = (196, 92, 96); LUNG_H = (250, 190, 182)
BLOOD = (196, 44, 52); BLOOD_S = (140, 24, 34)
LET = (150, 204, 92); LET_S = (96, 156, 56); LET_L = (204, 236, 160)
MNT = (64, 170, 112); MNT_S = (34, 120, 76)
APR = (214, 58, 52); APR_S = (156, 30, 30)
MILK = (252, 248, 238)
NAAN = (238, 200, 136); NAAN_S = (196, 140, 76); CHAR = (120, 76, 40)


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def clove_el(mood=None, look=(0, 0), crush=0.0, seed=291):
    """one garlic clove: a fat teardrop with a pointed tip, papery cream skin with mauve streaks at the base; crush 0..1 flattens it and cracks it open."""
    cr = round(clamp(crush) * 5) / 5
    def mk():
        w, h = 260, 320; im, d, S = _cv(w, h)
        sq = 1 - 0.55 * cr; sx = 1 + 0.45 * cr; cx, by = 130, 290
        def pt(x, y): return (cx + (x - 130) * sx, by - (by - y) * sq)
        body = [pt(*p) for p in ((130, 30), (150, 70), (190, 140), (214, 210), (206, 262), (170, 288), (90, 288), (54, 262), (46, 210), (70, 140), (110, 70))]
        _ink_poly(d, body, GAR, seed, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.polygon(S_(150, 0, 260, 0, 260, 320, 160, 320, 176, 160), fill=c), GAR_S, 130)
        _hatch_in(im, (150, 60, 230, 300), lambda q, S_: q.polygon(_P(body), fill=255), -40, 10, 30)
        for i, x0 in enumerate((96, 124, 152)):                                                # mauve streaks up from the base
            d.line(_P(_wob([pt(x0, 284), pt(x0 + 4, 230), pt(x0 + 2, 190)], 1.0, seed + i)), fill=GAR_ST + (200,), width=5 * SC3, joint="curve")
        d.line(_P([pt(84, 150), pt(78, 210)]), fill=(255, 255, 255, 180), width=7 * SC3)
        if cr > 0:
            for (x0, y0, a) in ((130, 180, -60), (110, 230, 200), (170, 220, 20)):
                P = [pt(x0, y0)]
                for k in range(4): P.append((P[-1][0] + 16 * math.cos(math.radians(a)) + 6 * (-1) ** k, P[-1][1] + 16 * math.sin(math.radians(a)) * sq))
                d.line(_P(P), fill=INKC + (255,), width=4 * SC3, joint="curve")
        if mood: _face(d, S, 130, pt(130, 205)[1], 1.5 * (1 - 0.3 * cr), mood, look)
        return _done(im, w, h)
    return gcache(("clove29", mood, look, cr, seed), mk)


def garlic_bulb_el(mood=None, look=(0, 0), seed=292):
    """a whole bulb: 5 fat lobes, papery cream with mauve streaks, a dry neck on top, root whiskers below."""
    def mk():
        w, h = 400, 440; im, d, S = _cv(w, h)
        for i, (x, r) in enumerate(((110, 92), (290, 92), (150, 104), (250, 104), (200, 116))):
            lobe = _arcpts(x, 270, r, 132, 0, 360, 26)
            _ink_poly(d, lobe, GAR, seed + i, INK_W, amp=1.6)
            _shade(im, lambda q, S_, lobe=lobe: q.polygon(_P(lobe), fill=255), lambda q, S_, c, x=x: q.polygon(S_(x + 20, 120, x + 140, 120, x + 140, 420, x + 30, 420), fill=c), GAR_S, 110)
            for j in (-1, 1): d.line(_P(_wob([(x + j * r * 0.3, 380), (x + j * r * 0.45, 300), (x + j * r * 0.3, 210)], 1.0, seed + 10 + i + j)), fill=GAR_ST + (170,), width=4 * SC3, joint="curve")
        _ink_poly(d, [(176, 160), (186, 70), (172, 36), (200, 50), (228, 36), (214, 70), (224, 160)], GAR, seed + 20, INK_W - 1, amp=1.2)   # the neck
        for j in range(7):
            x0 = 160 + j * 13; d.line(_P(_wob([(x0, 398), (x0 - 20 + j * 7, 432)], 1.0, seed + 30 + j)), fill=(170, 140, 100, 255), width=3 * SC3)
        _hatch_in(im, (230, 160, 370, 400), lambda q, S_: q.ellipse(S_(150, 140, 390, 410), fill=255), -40, 10, 26)
        if mood: _face(d, S, 200, 270, 2.0, mood, look)
        return _done(im, w, h)
    return gcache(("bulb29", mood, look, seed), mk)


def alliin_el(mood="n", look=(0, 0), seed=293):
    """ALLIIN: a calm pale-cream round buddy with a tiny sulfur-yellow dot on top (harmless on its own)."""
    def mk():
        w, h = 200, 210; im, d, S = _cv(w, h)
        _ink_ell(d, 100, 120, 76, 72, (250, 240, 200), seed, INK_W - 1, amp=1.4)
        _shade(im, lambda q, S_: q.ellipse(S_(24, 48, 176, 192), fill=255), lambda q, S_, c: q.ellipse(S_(70, 70, 230, 240), fill=c), (226, 208, 150), 120)
        _ink_ell(d, 100, 40, 18, 18, (244, 214, 90), seed + 1, INK_W - 2, amp=0.8)
        d.line(S(100, 58, 100, 50), fill=INKC + (255,), width=4 * SC3)
        _face(d, S, 100, 120, 1.6, mood, look)
        return _done(im, w, h)
    return gcache(("alliin29", mood, look, seed), mk)


def enzyme_el(mood="n", look=(0, 0), bite=0.5, seed=294):
    """THE ENZYME (alliinase): a mint pac-man buddy with a little hard hat stripe; bite 0..1 opens the jaw."""
    bt = round(clamp(bite) * 4) / 4
    def mk():
        w, h = 220, 210; im, d, S = _cv(w, h)
        a = 8 + 34 * bt
        P = [(110, 110)] + _arcpts(110, 110, 84, 84, a, 360 - a, 30)
        _ink_poly(d, P, INK_MINT, seed, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(0, 130, 220, 210), fill=c), INK_MINT_S, 130)
        _hatch_in(im, (30, 140, 190, 200), lambda q, S_: q.polygon(_P(P), fill=255), -40, 9, 30)
        for i in range(3): d.polygon(S(150 + i * 14, 110 - a * 0.9 + 2, 158 + i * 14, 110 - a * 0.9 + 14, 166 + i * 14, 110 - a * 0.9 + 2), fill=(255, 255, 255, 255))
        _face(d, S, 84, 74, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("enz29", mood, look, bt, seed), mk)


def allicin_el(mood="wow", seed=295):
    """ALLICIN: the short-lived product, a jittery cream-yellow star buddy about to fall apart (crack lines)."""
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h)
        P = []
        for i in range(16):
            r = 104 if i % 2 == 0 else 70; a = math.radians(i * 22.5 - 90); P.append((120 + r * math.cos(a), 124 + r * math.sin(a)))
        _ink_poly(d, P, (250, 226, 120), seed, INK_W - 1, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(0, 150, 240, 240), fill=c), (220, 180, 70), 120)
        for (x0, y0, x1, y1) in ((60, 70, 90, 110), (180, 160, 150, 140)): d.line(S(x0, y0, x1, y1), fill=INKC + (255,), width=4 * SC3)
        _face(d, S, 120, 124, 1.6, mood)
        return _done(im, w, h)
    return gcache(("allicin29", mood, seed), mk)


def gas_el2(mood="n", look=(0, 0), seed=296, scale=1.0):
    """a SMELLY SULFUR GAS: a mauve puff cloud with a wavy stink line on top and a face."""
    def mk():
        w, h = 300, 260; im, d, S = _cv(w, h)
        balls = ((90, 150, 62), (150, 116, 74), (214, 146, 64), (150, 172, 66))
        for (x, y, r) in balls: d.ellipse(S(x - r - 3, y - r - 3, x + r + 3, y + r + 3), fill=INKC + (255,))
        for (x, y, r) in balls: d.ellipse(S(x - r + 2, y - r + 2, x + r - 2, y + r - 2), fill=ACC_L + (255,))
        _shade(im, lambda q, S_: [q.ellipse(S_(x - r + 2, y - r + 2, x + r - 2, y + r - 2), fill=255) for (x, y, r) in balls], lambda q, S_, c: q.rectangle(S_(0, 176, 300, 260), fill=c), ACC, 150)
        for j in (-1, 1):
            d.line(_P([(150 + j * 34 + 10 * math.sin(k * 1.4), 50 - k * 8) for k in range(6)]), fill=ACC_S + (255,), width=5 * SC3, joint="curve")
        _face(d, S, 150, 148, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("gas29", mood, look, seed), mk)


def ams_el(mood="sly", look=(0, 0), seed=297):
    """AMS (allyl methyl sulfide): the SNEAKY gas — a darker mauve puff wearing a black bandit mask, a little trail behind it."""
    def mk():
        w, h = 320, 280; im, d, S = _cv(w, h)
        balls = ((100, 160, 66), (166, 120, 80), (232, 156, 62), (166, 184, 70), (60, 196, 30))
        for (x, y, r) in balls: d.ellipse(S(x - r - 3, y - r - 3, x + r + 3, y + r + 3), fill=INKC + (255,))
        for (x, y, r) in balls: d.ellipse(S(x - r + 2, y - r + 2, x + r - 2, y + r - 2), fill=ACC + (255,))
        _shade(im, lambda q, S_: [q.ellipse(S_(x - r + 2, y - r + 2, x + r - 2, y + r - 2), fill=255) for (x, y, r) in balls], lambda q, S_, c: q.rectangle(S_(0, 190, 320, 280), fill=c), ACC_S, 160)
        d.rounded_rectangle(S(108, 120, 230, 156), 16 * SC3, fill=(40, 28, 34, 255))                          # the bandit mask
        for sgn in (-1, 1): d.polygon(S(169 + sgn * 62, 132, 169 + sgn * 90, 118, 169 + sgn * 88, 150), fill=(40, 28, 34, 255))
        ox, oy = look[0] * 5, look[1] * 3
        for sgn in (-1, 1):
            x = 169 + sgn * 28
            if mood == "sly": d.line(S(x - 12, 138 + oy, x + 12, 136 + oy), fill=(255, 255, 255, 255), width=5 * SC3)
            else: d.ellipse(S(x - 8 + ox, 130 + oy, x + 8 + ox, 146 + oy), fill=(255, 255, 255, 255))
        if mood == "sly": d.line(_P(_arcpts(176, 172, 20, 10, 20, 150, 10)), fill=INKC + (255,), width=4 * SC3, joint="curve")
        elif mood == "wow": d.ellipse(S(160, 168, 180, 190), fill=(110, 40, 46, 255), outline=INKC + (255,), width=3 * SC3)
        else: d.line(_P(_arcpts(170, 166, 18, 9, 20, 160, 10)), fill=INKC + (255,), width=4 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("ams29", mood, look, seed), mk)


def lungs_el(mood="happy", look=(0, 0), k=0.5, seed=298):
    """the LUNGS as a pair of characters on one windpipe: coral pink, bronchi branches inked inside, one face; k 0..1 = breath (they swell)."""
    kk = round(clamp(k) * 4) / 4
    def mk():
        w, h = 520, 520; im, d, S = _cv(w, h); sw = 1 + 0.07 * kk
        d.line(S(260, 30, 260, 210), fill=INKC + (255,), width=40 * SC3); d.line(S(260, 30, 260, 210), fill=(246, 214, 206, 255), width=28 * SC3)
        for y in range(50, 200, 26): d.line(S(248, y, 272, y), fill=INKC + (160,), width=3 * SC3)
        for sgn in (-1, 1):
            cx = 260 + sgn * 120 * sw
            L = [(cx - sgn * 70 * sw, 150), (cx + sgn * 40 * sw, 140), (cx + sgn * 104 * sw, 260), (cx + sgn * 112 * sw, 400), (cx + sgn * 70 * sw, 480), (cx - sgn * 40 * sw, 488), (cx - sgn * 92 * sw, 440), (cx - sgn * 80 * sw, 300)]
            _ink_poly(d, L, LUNG, seed + sgn, INK_W, amp=2.0)
            _shade(im, lambda q, S_, L=L: q.polygon(_P(L), fill=255), lambda q, S_, c: q.rectangle(S_(0, 380, 520, 520), fill=c), LUNG_S, 140)
            _hatch_in(im, (int(cx - 110), 390, int(cx + 110), 490), lambda q, S_, L=L: q.polygon(_P(L), fill=255), -40, 10, 30)
            br = [(260, 210), (260 + sgn * 60, 250), (cx, 320)]
            d.line(_P(br), fill=LUNG_S + (255,), width=10 * SC3, joint="curve")
            for (dx, dy) in ((-30, 60), (30, 50), (0, 100)): d.line(S(cx, 320, cx + sgn * dx, 320 + dy), fill=LUNG_S + (255,), width=6 * SC3)
            d.line(_P(_wob([(cx - sgn * 30 * sw, 180), (cx + sgn * 20 * sw, 176)], 1.0, seed + 5 + sgn)), fill=LUNG_H + (255,), width=8 * SC3)
        if mood: _face(d, S, 260, 330, 2.2, mood, look)
        return _done(im, w, h)
    return gcache(("lungs29", mood, look, kk, seed), mk)


def lettuce_el(mood=None, look=(0, 0), seed=299):
    """a round head of lettuce: wavy layered leaves, light green inside, a pale stem base."""
    def mk():
        w, h = 320, 300; im, d, S = _cv(w, h)
        for i, (x, y, r, c) in enumerate(((100, 170, 92, LET_S), (220, 170, 92, LET_S), (160, 150, 110, LET), (160, 190, 90, LET_L))):
            P = [(x + (r + 8 * math.sin(a * 7)) * math.cos(a), y + (r * 0.86 + 8 * math.sin(a * 7)) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
            _ink_poly(d, P, c, seed + i, INK_W - 1, amp=1.2)
        for j in (-1, 0, 1): d.line(_P(_wob([(160 + j * 20, 260), (160 + j * 50, 160), (160 + j * 70, 110)], 1.0, seed + 9 + j)), fill=(240, 250, 220, 255), width=5 * SC3, joint="curve")
        _hatch_in(im, (190, 150, 310, 280), lambda q, S_: q.ellipse(S_(40, 40, 310, 280), fill=255), -40, 10, 26)
        if mood: _face(d, S, 160, 186, 1.6, mood, look)
        return _done(im, w, h)
    return gcache(("lettuce29", mood, look, seed), mk)


def mint_sprig_el(mood=None, look=(0, 0), seed=300):
    """a fresh mint sprig: a stem with 3 pairs of serrated leaves, deep green, veins inked."""
    def mk():
        w, h = 260, 340; im, d, S = _cv(w, h)
        d.line(_P(_wob([(130, 330), (128, 200), (132, 40)], 1.0, seed)), fill=MNT_S + (255,), width=9 * SC3, joint="curve")
        for i, (y, L) in enumerate(((260, 100), (170, 86), (90, 66))):
            for sgn in (-1, 1):
                a = math.radians(-90 + sgn * 62); cx, cy = 130 + sgn * L * 0.55, y - 16
                P = []
                for q in np.linspace(0, 2 * math.pi, 26, endpoint=False):
                    rr = 1 + 0.08 * (1 if int(q * 4) % 2 else -1)
                    P.append((cx + L * 0.52 * rr * math.cos(q) * math.cos(a + 1.57) - L * 0.3 * rr * math.sin(q) * math.sin(a + 1.57), cy + L * 0.52 * rr * math.cos(q) * math.sin(a + 1.57) + L * 0.3 * rr * math.sin(q) * math.cos(a + 1.57)))
                _ink_poly(d, P, MNT if i % 2 == 0 else (88, 190, 130), seed + i * 2 + sgn, INK_W - 2, amp=1.0)
                d.line(S(130, y - 6, cx + sgn * L * 0.3, cy - 8), fill=MNT_S + (255,), width=3 * SC3)
        if mood: _face(d, S, 130, 200, 1.2, mood, look)
        return _done(im, w, h)
    return gcache(("mint29", mood, look, seed), mk)


def naan_el(seed=301, bite=False):
    """a teardrop garlic naan: golden, charred blisters, green herb flecks + cream garlic bits."""
    def mk():
        w, h = 360, 260; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        P = [(40, 140), (90, 60), (200, 40), (320, 80), (340, 150), (290, 220), (160, 236), (60, 210)]
        if bite: P = P[:3] + [(300, 70), (290, 100), (320, 120), (330, 150)] + P[5:]
        _ink_poly(d, P, NAAN, seed, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(0, 170, 360, 260), fill=c), NAAN_S, 120)
        for i in range(14):
            x, y = rng.uniform(90, 290), rng.uniform(80, 200); r = rng.uniform(6, 14)
            d.ellipse(S(x - r, y - r * 0.7, x + r, y + r * 0.7), fill=CHAR + (200,))
        for i in range(18):
            x, y = rng.uniform(80, 300), rng.uniform(80, 200)
            d.ellipse(S(x - 4, y - 3, x + 4, y + 3), fill=(MNT if i % 2 else GAR) + (255,), outline=INKC + (200,), width=SC3)
        return _done(im, w, h)
    return gcache(("naan29", seed, bite), mk)


def red_apple(mood=None, look=(0, 0), cut=False):
    """lib19 apple_el follows the global accent: draw it once in apple red (seed 91 keeps its own cache slot)."""
    global ACC, ACC_S
    a0, s0 = ACC, ACC_S; ACC, ACC_S = APR, APR_S
    try: return apple_el(mood=mood, look=look, cut=cut, seed=91)
    finally: ACC, ACC_S = a0, s0


def breath_meter_el(level=0.0, seed=302):
    """the lab BREATH METER: a cream box with a mouthpiece hose, a dial window and a bar that shows how smelly the breath is (mauve)."""
    lv = round(clamp(level) * 20) / 20
    def mk():
        w, h = 420, 360; im, d, S = _cv(w, h)
        _ink_poly(d, [(60, 80), (380, 80), (390, 330), (50, 330)], (236, 230, 214), seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(S_(60, 80, 380, 80, 390, 330, 50, 330), fill=255), lambda q, S_, c: q.rectangle(S_(300, 60, 420, 360), fill=c), (200, 190, 168), 120)
        _ink_poly(d, [(100, 120), (340, 120), (340, 200), (100, 200)], (250, 250, 244), seed + 1, INK_W - 2, amp=0.8)
        bw = 220 * lv
        if bw > 4: d.rectangle(S(110, 134, 110 + bw, 186), fill=ACC + (255,))
        for x in range(110, 340, 44): d.line(S(x, 194, x, 186), fill=INKC + (200,), width=2 * SC3)
        for i, x in enumerate((130, 200, 270)): _ink_ell(d, x, 262, 22, 22, ((214, 80, 70), (240, 200, 80), (110, 190, 120))[i], seed + 5 + i, INK_W - 3, amp=0.6)
        d.line(_P(_wob([(60, 150), (20, 140), (16, 60), (60, 30)], 1.0, seed + 9)), fill=INKC + (255,), width=16 * SC3, joint="curve")
        d.line(_P(_wob([(60, 150), (20, 140), (16, 60), (60, 30)], 1.0, seed + 9)), fill=(180, 200, 210, 255), width=9 * SC3, joint="curve")
        _ink_poly(d, [(56, 14), (96, 20), (92, 46), (54, 42)], (90, 90, 96), seed + 11, INK_W - 3, amp=0.5)
        return _done(im, w, h)
    return gcache(("meter29", lv, seed), mk)


def tongue_teeth_el(bits=1.0, seed=303):
    """an open-mouth close-up (front): pink gum arch, a row of teeth, a tongue; cream garlic bits stuck between teeth and on the tongue."""
    b = round(clamp(bits) * 4) / 4
    def mk():
        w, h = 640, 520; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        mouth = _arcpts(320, 220, 290, 230, 0, 360, 40)
        _ink_poly(d, mouth, (120, 36, 48), seed, INK_W + 2, amp=1.6)
        _ink_poly(d, _arcpts(320, 390, 200, 120, 180, 360, 20) + [(520, 400), (120, 400)], (232, 120, 130), seed + 1, INK_W, amp=1.4)   # tongue
        d.line(S(320, 300, 320, 380), fill=(200, 90, 100, 255), width=4 * SC3)
        for i in range(8):
            x = 70 + i * 64; _ink_poly(d, [(x, 40), (x + 60, 40), (x + 56, 120), (x + 4, 120)], (252, 250, 240), seed + 10 + i, INK_W - 2, amp=0.8)
        if b > 0:
            for i in range(int(10 * b)):
                if i < 5: x, y = 130 + i * 64, 122 + rng.uniform(-4, 4)
                else: x, y = rng.uniform(200, 440), rng.uniform(320, 380)
                r = rng.uniform(9, 14); _ink_poly(d, [(x - r, y), (x, y - r * 0.8), (x + r, y), (x + 2, y + r * 0.7)], GAR, seed + 30 + i, 3, amp=0.5)
        return _done(im, w, h)
    return gcache(("tteeth29", b, seed), mk)


def sweat_drop_el(mood="n", seed=304):
    def mk():
        w, h = 150, 200; im, d, S = _cv(w, h)
        P = [(75, 20)] + _arcpts(75, 128, 52, 54, -20, 200, 20)
        _ink_poly(d, P, (196, 228, 246), seed, INK_W - 1, amp=1.0)
        d.line(S(56, 110, 52, 140), fill=(255, 255, 255, 220), width=6 * SC3)
        if mood: _face(d, S, 80, 132, 1.0, mood)
        return _done(im, w, h)
    return gcache(("sweat29", mood, seed), mk)


# ---------------- NEW PLACE: the MEETING ROOM (an office the morning after): big window with a city skyline, a glass wall, a whiteboard with a chart, a plant; table front ----------------
def set_office(t=0.0, blur=4, top_y=1330, dim=0.0):
    def mk():
        f = _vgrad((232, 226, 214), (214, 204, 186), 0, top_y)
        cv2.rectangle(f, (40, 260), (640, 940), C((96, 92, 96)), -1, cv2.LINE_AA)                          # window frame
        f[280:920, 60:620] = _vgrad((178, 214, 244), (238, 232, 214), 280, 920)[280:920, 60:620]
        for (x, w_, h_) in ((80, 90, 300), (180, 70, 420), (260, 110, 250), (380, 80, 380), (470, 120, 300), (560, 60, 200)):  # skyline
            cv2.rectangle(f, (x, 920 - h_), (x + w_, 920), C((150, 168, 190)), -1, cv2.LINE_AA)
            for yy in range(940 - h_, 900, 40):
                for xx in range(x + 12, x + w_ - 12, 24): cv2.rectangle(f, (xx, yy), (xx + 10, yy + 16), C((214, 226, 236)), -1)
        cv2.line(f, (340, 280), (340, 920), C((96, 92, 96)), 10, cv2.LINE_AA)
        cv2.rectangle(f, (700, 330), (1040, 640), C((250, 250, 246)), -1, cv2.LINE_AA); cv2.rectangle(f, (700, 330), (1040, 640), C((120, 116, 112)), 8, cv2.LINE_AA)   # whiteboard
        P = np.array([(740, 590), (810, 540), (880, 560), (950, 450), (1000, 420)], np.int32); cv2.polylines(f, [P], False, C((80, 120, 190)), 8, cv2.LINE_AA)
        for i, hh in enumerate((60, 110, 80)): cv2.rectangle(f, (750 + i * 60, 600 - hh - 120), (790 + i * 60, 600 - 120), C((236, 180, 90)), -1)
        cv2.rectangle(f, (900, 1000), (980, 1180), C((150, 104, 72)), -1, cv2.LINE_AA)                      # plant pot
        for a in range(-60, 61, 20):
            x1 = int(940 + 150 * math.sin(math.radians(a))); y1 = int(1000 - 200 * math.cos(math.radians(a)))
            cv2.line(f, (940, 1000), (x1, y1), C((90, 150, 90)), 14, cv2.LINE_AA)
        cv2.rectangle(f, (0, 1180), (W, top_y), C((196, 184, 168)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_office29", blur, top_y), mk).copy()
    god_rays(f, 340, 420, t, (255, 244, 220), 0.12, 6, 1200, 0.7, 0.9, 3)
    glow(f, 340, 560, 380, (255, 246, 222), 0.2)
    if dim > 0: f *= (1 - 0.45 * dim)
    return inkify(f)


def office_front(f, top_y=1330):
    """the meeting table edge: warm wood top + a darker front with a soft highlight; a mug and a notepad on it."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 40), C((178, 128, 88)), -1, cv2.LINE_AA)
    cv2.line(f, (0, top_y + 4), (W, top_y + 4), C((214, 170, 120)), 6, cv2.LINE_AA)
    f[top_y + 40:, :] = f[top_y + 40:, :] * 0 + np.array(C((132, 92, 62)), np.float32)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 40), (W, top_y + 40), C(INKC), 5, cv2.LINE_AA)
    _hatch_band(f, top_y + 44, H)


def _hatch_band(f, y0, y1, gap=22):
    for x in range(-400, W, gap): cv2.line(f, (x, y1), (x + (y1 - y0), y0), C((110, 74, 50)), 2, cv2.LINE_AA)
