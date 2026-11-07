# ================= anim_props_lib27.py (ep 27, 7 Nov): SLEEPY AFTER A BIG MEAL. ONE accent: DUSK LAVENDER (= sleepiness, the dip, the dimmed light).
# Board drawings in blueprint blue (BP_INK); food in warm ink colours; blood = a red drop character (the myth); the wake-up chemical OREXIN = a little lamp-headed buddy.
# thali_el(kind full|small|empty, mood), dimmer_el(k) (k 0 = AWAKE .. 1 = SLEEPY), orexin_el(lit, mood), pizza_el(left), blood_el(mood, look), brain_ink_el(mood, level),
# stomach_ink_el(mood), keys_el(), sofa_el(), envelope_el(), sugar_ink_el(), steth_el().
ACC = (128, 98, 204); ACC_S = (84, 60, 150); ACC_L = (196, 182, 240); ACC_XL = (230, 224, 250)
BLOOD_C = (204, 46, 52); BLOOD_S = (150, 24, 34)
STEEL = (206, 210, 214); STEEL_S = (160, 166, 174); STEEL_L = (236, 238, 240)
DAL = (238, 182, 50); PANEER_C = (222, 98, 48); RAITA = (248, 246, 236); RICE = (252, 250, 242); PURI = (230, 166, 70); PURI_S = (190, 118, 40)
BULB_ON = (255, 230, 120); BULB_OFF = (196, 196, 206)
MILK = (252, 248, 238)


def thali_el(kind="full", mood=None, seed=271):
    """a steel thali seen from a little above: katoris of dal / paneer / raita, a rice mound, puris, a laddoo. full = heaped (plus extra puris), small = a sensible plate, empty = licked clean."""
    def mk():
        w, h = 560, 340; im, d, S = _cv(w, h)
        _ink_ell(d, 280, 190, 262, 132, STEEL, seed, INK_W, n=40, amp=1.0)
        _ink_ell(d, 280, 190, 226, 106, STEEL_L, seed + 1, INK_W - 3, n=40, amp=0.8)
        _shade(im, lambda q, S_: q.ellipse(S_(18, 58, 542, 322), fill=255), lambda q, S_, c: q.ellipse(S_(18, 120, 542, 360), fill=c), STEEL_S, 110)
        if kind != "empty":
            kat = [(150, 150, DAL), (262, 120, PANEER_C), (374, 150, RAITA)] if kind == "full" else [(190, 140, DAL), (330, 140, RAITA)]
            for i, (x, y, c) in enumerate(kat):
                _ink_ell(d, x, y, 58, 34, STEEL, seed + 3 + i, INK_W - 1, amp=0.8); _ink_ell(d, x, y - 4, 46, 24, c, seed + 9 + i, INK_W - 3, amp=0.8)
                if c == PANEER_C:
                    for dx, dy in ((-16, -8), (12, -2), (-2, 8)): _ink_poly(d, [(x + dx - 8, y + dy - 7), (x + dx + 8, y + dy - 7), (x + dx + 8, y + dy + 5), (x + dx - 8, y + dy + 5)], (252, 236, 210), seed + 20 + dx, 2)
            rr = 1.3 if kind == "full" else 0.9
            _ink_ell(d, 300, 236, 84 * rr, 40 * rr, RICE, seed + 30, INK_W - 1, amp=2.2)
            for j in range(10 if kind == "full" else 5): d.ellipse(S(250 + j * 11 % 100, 222 + (j * 7) % 26, 258 + j * 11 % 100, 226 + (j * 7) % 26), fill=(226, 220, 204, 255))
            npuri = 4 if kind == "full" else 1
            for j in range(npuri):
                px, py = 130 + j * 16, 250 - j * 14
                _ink_ell(d, px, py, 58, 34, PURI, seed + 40 + j, INK_W - 1, amp=1.4)
                _shade(im, lambda q, S_, px=px, py=py: q.ellipse(S_(px - 58, py - 34, px + 58, py + 34), fill=255), lambda q, S_, c, px=px, py=py: q.ellipse(S_(px - 40, py - 10, px + 70, py + 50), fill=c), PURI_S, 90)
            nl = 3 if kind == "full" else 1
            for j in range(nl):
                lx, ly = 440 + (j % 2) * 34, 240 - j * 30
                _ink_ell(d, lx, ly, 30, 28, (242, 168, 52), seed + 50 + j, INK_W - 1, amp=1.0)
                for q_ in range(6): d.ellipse(S(lx - 18 + q_ * 7, ly - 10 + (q_ * 5) % 16, lx - 15 + q_ * 7, ly - 7 + (q_ * 5) % 16), fill=(212, 128, 30, 255))
        if mood: _face(d, S, 280, 300 if kind != "empty" else 190, 1.3, mood)
        return _done(im, w, h)
    return gcache(("thali27", kind, mood, seed), mk)


def dimmer_el(k=0.0, seed=272, labels=True):
    """a wall dimmer: a cream plate, a scale from AWAKE (warm yellow) to SLEEPY (lavender), a round knob whose pointer turns with k (0..1)."""
    kq = round(clamp(k), 2)
    def mk():
        w, h = 420, 470; im, d, S = _cv(w, h); cx, cy, R_ = 210, 250, 150
        _ink_poly(d, [(30, 40), (390, 40), (390, 440), (30, 440)], (250, 244, 228), seed, INK_W, amp=1.2)
        for i in range(40):
            a0 = 135 + 270 * i / 40; a1 = 135 + 270 * (i + 1) / 40; u = i / 39
            col = tuple(int(BULB_ON[c] * (1 - u) + ACC[c] * u) for c in range(3))
            d.arc(S(cx - R_, cy - R_, cx + R_, cy + R_), a0, a1 + 1, fill=col + (255,), width=26 * SC3)
        d.arc(S(cx - R_ - 14, cy - R_ - 14, cx + R_ + 14, cy + R_ + 14), 135, 405, fill=INKC + (255,), width=4 * SC3)
        _ink_ell(d, cx, cy, 92, 92, (236, 230, 216), seed + 2, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.ellipse(S_(cx - 92, cy - 92, cx + 92, cy + 92), fill=255), lambda q, S_, c: q.ellipse(S_(cx - 70, cy - 40, cx + 130, cy + 140), fill=c), (190, 180, 160), 120)
        a = math.radians(135 + 270 * kq)
        d.line(S(cx + 20 * math.cos(a), cy + 20 * math.sin(a), cx + 80 * math.cos(a), cy + 80 * math.sin(a)), fill=INKC + (255,), width=14 * SC3)
        if labels:
            fn = font(F_BOLD, 30 * SC3)
            d.text(S(96, 410), "AWAKE", font=fn, fill=INKC + (255,), anchor="mm"); d.text(S(324, 410), "SLEEPY", font=fn, fill=ACC_S + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("dimmer27", kq, seed, labels), mk)


def orexin_el(lit=1.0, mood="happy", look=(0, 0), seed=273):
    """OREXIN, the wake-up chemical, as a little buddy with a light-bulb head: lit = bright yellow + rays, 0 = grey and sleepy."""
    lq = round(clamp(lit), 1)
    def mk():
        w, h = 260, 330; im, d, S = _cv(w, h)
        col = tuple(int(BULB_OFF[c] + (BULB_ON[c] - BULB_OFF[c]) * lq) for c in range(3))
        if lq > 0.3:
            for i in range(8):
                a = math.radians(-90 + (i - 3.5) * 24); L = 26 * lq
                d.line(S(130 + 112 * math.cos(a), 118 + 112 * math.sin(a), 130 + (112 + L) * math.cos(a), 118 + (112 + L) * math.sin(a)), fill=(240, 190, 60, int(255 * lq)), width=6 * SC3)
        _ink_ell(d, 130, 118, 92, 96, col, seed, INK_W, amp=1.2)
        d.ellipse(S(82, 62, 108, 100), fill=(255, 255, 255, int(120 + 100 * lq)))
        _ink_poly(d, [(92, 206), (168, 206), (160, 252), (100, 252)], (170, 172, 184), seed + 1, INK_W - 1, amp=0.8)
        for y in (220, 236): d.line(S(96, y, 164, y), fill=INKC + (255,), width=3 * SC3)
        _ink_poly(d, [(110, 252), (150, 252), (162, 312), (98, 312)], ACC, seed + 2, INK_W - 1, amp=1.0)
        _face(d, S, 130, 130, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("orexin27", lq, mood, look, seed), mk)


def pizza_el(left=1.0, seed=274):
    """a round pizza from above (veg: tomato, capsicum, olive); left = fraction of slices still there (eaten slices leave the board)."""
    nl = int(round(8 * clamp(left)))
    def mk():
        w = h = 300; im, d, S = _cv(w, h); c = 150
        _ink_ell(d, c, c, 136, 136, (226, 236, 240), seed + 9, 3, amp=0.6)
        for i in range(nl):
            a0, a1 = -90 + i * 45, -90 + (i + 1) * 45
            P = [(c, c)] + _arcpts(c, c, 124, 124, a0 + 1.5, a1 - 1.5, 6)
            _ink_poly(d, P, (236, 176, 80), seed + i, INK_W - 2, amp=0.8)
            P2 = [(c, c)] + _arcpts(c, c, 108, 108, a0 + 3, a1 - 3, 6)
            d.polygon([(x * SC3, y * SC3) for x, y in P2], fill=(250, 214, 110, 255))
            am = math.radians((a0 + a1) / 2)
            for rr, col in ((70, (214, 60, 40)), (40, (90, 160, 70)), (94, (60, 50, 40))):
                x, y = c + rr * math.cos(am), c + rr * math.sin(am); d.ellipse(S(x - 9, y - 9, x + 9, y + 9), fill=col + (255,))
        return _done(im, w, h)
    return gcache(("pizza27", nl, seed), mk)


def blood_el(mood="happy", look=(0, 0), seed=275):
    def mk():
        w, h = 160, 200; im, d, S = _cv(w, h)
        P = [(80, 14)] + _arcpts(80, 120, 60, 62, -30, 210, 18)
        _ink_poly(d, P, BLOOD_C, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(60, 90, 170, 200), fill=c), BLOOD_S, 120)
        d.ellipse(S(48, 92, 62, 116), fill=(255, 255, 255, 170))
        if mood: _face(d, S, 84, 130, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("blood27", mood, look, seed), mk)


def brain_ink_el(mood="happy", look=(0, 0), level=1.0, seed=276):
    """a pink ink brain with a face; level < 1 drains its colour toward grey (the 'runs dry' myth picture)."""
    lq = round(clamp(level), 1)
    def mk():
        w, h = 300, 240; im, d, S = _cv(w, h)
        base = tuple(int(200 + (244 - 200) * lq) if c == 0 else int(200 + ((168, 176)[c - 1] - 200) * lq) for c in range(3))
        P = []
        for i in range(11):                                  # scalloped top: a row of bumps = folds seen from the side
            a0 = 180 + 180 * i / 11; a1 = 180 + 180 * (i + 1) / 11; am = math.radians((a0 + a1) / 2)
            cx_, cy_ = 150 + 112 * math.cos(am), 150 + 104 * math.sin(am)
            P += _arcpts(cx_, cy_, 22, 22, math.degrees(am) - 90, math.degrees(am) + 90, 6)
        P += [(262, 160), (254, 196), (210, 214), (150, 208), (92, 214), (46, 196), (38, 160)]
        _ink_poly(d, P, base, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(40, 150, 300, 280), fill=c), (200, 110, 130), 70)
        d.line([(x * SC3, y * SC3) for x, y in _wob([(150, 50), (142, 90), (156, 126), (148, 160)], 1.0, seed + 7)], fill=INKC + (230,), width=5 * SC3, joint="curve")
        for j, (x0, y0, sg) in enumerate(((84, 82, 1), (108, 130, -1), (200, 84, -1), (196, 132, 1))):
            d.line([(x * SC3, y * SC3) for x, y in _arcpts(x0, y0, 24, 14, 200 if sg > 0 else -20, 340 if sg > 0 else 160, 8)], fill=INKC + (200,), width=4 * SC3, joint="curve")
        if mood: _face(d, S, 150, 172, 1.2, mood, look)
        return _done(im, w, h)
    return gcache(("brain27", mood, look, lq, seed), mk)


def stomach_ink_el(mood="happy", look=(0, 0), grab=0.0, seed=277):
    """a J-shaped stomach character (pink), arms out when grab > 0 (the greedy-stomach myth)."""
    gq = round(clamp(grab), 1)
    def mk():
        w, h = 340, 300; im, d, S = _cv(w, h)
        if gq > 0:
            for sgn in (-1, 1):
                x0 = 170 + sgn * 92; d.line([(x * SC3, y * SC3) for x, y in _wob([(x0, 130), (x0 + sgn * 40, 100 - 30 * gq), (x0 + sgn * 56, 60 - 30 * gq)], 1.0, seed + sgn)], fill=INKC + (255,), width=7 * SC3, joint="curve")
                for k_ in range(3): d.line(S(x0 + sgn * 56, 60 - 30 * gq, x0 + sgn * (56 + 14 * math.cos(k_ - 1)), 60 - 30 * gq - 16 + 8 * k_), fill=INKC + (255,), width=5 * SC3)
        P = [(110, 40), (150, 40), (160, 90), (240, 110), (290, 170), (270, 240), (180, 270), (100, 250), (80, 190), (110, 130)]
        _ink_poly(d, P, (240, 156, 170), seed, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(140, 170, 330, 320), fill=c), (200, 100, 120), 110)
        if mood: _face(d, S, 190, 180, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("stom27", mood, look, gq, seed), mk)


def keys_el(seed=278):
    def mk():
        w, h = 200, 200; im, d, S = _cv(w, h)
        _ink_ell(d, 70, 60, 34, 34, None, seed, INK_W - 1, amp=0.6)
        _ink_poly(d, [(84, 84), (110, 70), (178, 150), (164, 168), (150, 158), (140, 170), (128, 160), (100, 110)], (214, 190, 110), seed + 1, INK_W - 2, amp=0.6)
        _ink_poly(d, [(50, 86), (78, 96), (60, 186), (34, 180)], (90, 96, 110), seed + 2, INK_W - 2, amp=0.6)
        return _done(im, w, h)
    return gcache(("keys27", seed), mk)


def envelope_el(seed=279):
    def mk():
        w, h = 120, 90; im, d, S = _cv(w, h)
        _ink_poly(d, [(8, 12), (112, 12), (112, 80), (8, 80)], (252, 248, 236), seed, 4, amp=0.6)
        d.line([(x * SC3, y * SC3) for x, y in [(10, 14), (60, 52), (110, 14)]], fill=INKC + (255,), width=4 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("env27", seed), mk)


def sugar_ink_el(seed=280):
    def mk():
        w, h = 120, 120; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 40), (70, 20), (104, 44), (104, 96), (54, 112), (20, 90)], (252, 252, 250), seed, 5, amp=0.6)
        d.line(S(20, 40, 54, 62, 104, 44), fill=INKC + (255,), width=4 * SC3); d.line(S(54, 62, 54, 112), fill=INKC + (255,), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("sug27", seed), mk)


def sofa_el(seed=281):
    """a low Diwali-room sofa (ink, lavender cushions) for the nap gag."""
    def mk():
        w, h = 760, 360; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 60), (720, 60), (720, 250), (40, 250)], (176, 112, 84), seed, INK_W, amp=1.4)
        _ink_poly(d, [(10, 140), (90, 130), (96, 320), (16, 320)], (150, 92, 66), seed + 1, INK_W, amp=1.2)
        _ink_poly(d, [(670, 130), (750, 140), (744, 320), (664, 320)], (150, 92, 66), seed + 2, INK_W, amp=1.2)
        _ink_poly(d, [(80, 220), (680, 220), (690, 300), (70, 300)], (196, 132, 100), seed + 3, INK_W, amp=1.4)
        for j, x in enumerate((150, 610)): _ink_ell(d, x, 170, 70, 52, ACC_L, seed + 5 + j, INK_W - 1, amp=1.2)
        _hatch_in(im, (40, 60, 720, 320), lambda q, S_: q.rectangle(S_(40, 230, 720, 320), fill=255))
        return _done(im, w, h)
    return gcache(("sofa27", seed), mk)


def steth_el(seed=282):
    def mk():
        w, h = 220, 240; im, d, S = _cv(w, h)
        P = _arcpts(110, 70, 70, 80, 180, 360, 16)
        d.line([(x * SC3, y * SC3) for x, y in _wob(P, 1.0, seed)], fill=INKC + (255,), width=8 * SC3, joint="curve")
        d.line([(x * SC3, y * SC3) for x, y in _wob([(110, 150), (110, 190), (150, 200)], 1.0, seed + 1)], fill=INKC + (255,), width=8 * SC3, joint="curve")
        d.line([(x * SC3, y * SC3) for x, y in _wob([(40, 70), (60, 130), (110, 150), (160, 130), (180, 70)], 1.0, seed + 2)], fill=INKC + (255,), width=8 * SC3, joint="curve")
        _ink_ell(d, 160, 204, 26, 26, STEEL, seed + 3, INK_W - 1, amp=0.6)
        return _done(im, w, h)
    return gcache(("steth27", seed), mk)
