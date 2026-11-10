# ================= anim_props_lib31.py (ep 31, 10 Nov): WHY DO SALTY SNACKS MAKE YOU THIRSTY? ONE accent: SALT ORANGE (= salt only: the crystals' shadow
# side, the chips' seasoning, the SALT words, the salt checker's alarm). Water keeps its natural blue, cells a soft pink, kidneys their own colour.
# chip_el(seed, bite), chips_bowl_el(level), salt_el(mood, look), shaker_el(mood, look), cell_buddy_el(mood, look, k), checker_el(mood, look, needle, ring),
# courier_el(mood, look) (vasopressin), urea_el(mood, look, pull), magnet_el(), wdrop_el(mood, look) (a water drop), tv_glow / set_tvroom(t, flick) + sofa_front,
# set_capsule(t, dim) + capsule_front(f, top_y) (inside a mock spaceship module, Mars in the porthole), tray_el(salty), crew(...) helper lives in anim_shots.
ACC = (236, 128, 52); ACC_S = (176, 80, 28); ACC_L = (250, 196, 150); ACC_XL = (254, 232, 212)
ACC_SALT = ACC
WAT = (98, 168, 228); WAT_S = (52, 116, 188); WAT_L = (200, 228, 250)
CHIP = (244, 202, 104); CHIP_S = (206, 150, 58); CHIP_D = (176, 112, 40)
CELLP = (246, 190, 196); CELLP_S = (214, 138, 150); CELLP_N = (196, 110, 140)
SALTW = (252, 252, 248); SALT_S = (226, 222, 214)
MILK = (252, 248, 238)
UREA = (196, 210, 96); UREA_S = (140, 156, 48)
MAG = (210, 52, 48); MAG_S = (150, 28, 30); STEEL = (206, 212, 220)
MARS = (214, 104, 62); MARS_S = (160, 64, 40)


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def chip_el(seed=310, bite=0.0, mood=None, look=(0, 0)):
    """one potato chip: a wavy golden oval with ridges, toasty edge spots and orange seasoning specks; bite 0..1 takes a scalloped bite out of the top right."""
    bt = round(clamp(bite) * 3) / 3
    def mk():
        w, h = 240, 200; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        P = []
        for i in range(30):
            a = 2 * math.pi * i / 30; r = 1 + 0.06 * math.sin(3 * a + seed) + 0.04 * math.sin(7 * a)
            x, y = 120 + 100 * r * math.cos(a), 100 + 78 * r * math.sin(a)
            if bt > 0:
                dx, dy = x - 205, y - 40; dd = math.hypot(dx, dy); R = 70 * bt
                if dd < R: x, y = 205 + dx / max(dd, 1e-3) * R, 40 + dy / max(dd, 1e-3) * R
            P.append((x, y))
        _ink_poly(d, P, CHIP, seed, INK_W - 1, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.polygon(S_(0, 120, 240, 90, 240, 200, 0, 200), fill=c), CHIP_S, 120)
        for k in range(4):                                                                 # ridges
            y0 = 52 + k * 30
            d.line(_P(_wob([(46 + 6 * k, y0 + 6), (90, y0 - 4), (140, y0 + 8), (190 - 4 * k, y0)], 1.0, seed + k)), fill=CHIP_D + (150,), width=3 * SC3, joint="curve")
        for k in range(14):                                                                # seasoning specks (the accent)
            x, y = 50 + rng.random() * 140, 40 + rng.random() * 120
            d.ellipse(S(x - 3, y - 3, x + 3, y + 3), fill=(ACC if k % 2 else ACC_S) + (230,))
        for k in range(3):
            x, y = 60 + rng.random() * 120, 50 + rng.random() * 100
            d.ellipse(S(x - 8, y - 5, x + 8, y + 5), fill=CHIP_D + (110,))
        if mood: _face(d, S, 110, 104, 1.4, mood, look)
        return _done(im, w, h)
    return gcache(("chip31", seed, bt, mood, look), mk)


def chips_bowl_el(level=1.0, seed=311):
    """a wide cream ceramic bowl heaped with chips; level 0..1 = how full (0 = crumbs at the bottom)."""
    lv = round(clamp(level) * 4) / 4
    def mk():
        w, h = 520, 380; im, d, S = _cv(w, h)
        if lv > 0:                                                                         # the heap (drawn first, the bowl's front covers its base)
            rng = np.random.default_rng(seed)
            n = int(4 + 12 * lv)
            for i in range(n):
                cx = 110 + rng.random() * 300; cy = 210 - lv * (60 + rng.random() * 120) + 40
                ch = chip_el(seed + 20 + i % 5)
                pil = Image.fromarray((np.dstack([ch[0] / np.maximum(ch[1][..., None], 1e-4), ch[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
                pil = pil.resize((int(pil.width * 0.62 * SC3), int(pil.height * 0.62 * SC3))).rotate(rng.uniform(-50, 50), expand=True)
                im.alpha_composite(pil, (int(cx * SC3 - pil.width / 2), int(cy * SC3 - pil.height / 2)))
        bowl = [(30, 200), (490, 200), (470, 270), (420, 330), (330, 360), (190, 360), (100, 330), (50, 270)]
        _ink_poly(d, bowl, (246, 238, 222), seed, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.polygon(_P(bowl), fill=255), lambda q, S_, c: q.polygon(S_(300, 200, 520, 200, 520, 380, 280, 380), fill=c), (214, 196, 170), 140)
        _hatch_in(im, (300, 210, 480, 360), lambda q, S_: q.polygon(_P(bowl), fill=255), -40, 10, 30)
        d.line(_P(_wob([(60, 236), (460, 236)], 1.0, seed + 3)), fill=ACC + (200,), width=8 * SC3)   # a stripe on the bowl (the accent)
        if lv == 0:
            for k in range(8): d.ellipse(S(150 + k * 28, 196 + (k % 3) * 3, 160 + k * 28, 204 + (k % 3) * 3), fill=CHIP + (255,))
        return _done(im, w, h)
    return gcache(("bowl31", lv, seed), mk)


def salt_el(mood="n", look=(0, 0), seed=312):
    """a SALT CRYSTAL buddy: a white cube in 3/4 view (bright top, cream left face, ACCENT-hatched shadow face), dot face on the front."""
    def mk():
        w, h = 210, 220; im, d, S = _cv(w, h)
        top = [(40, 64), (120, 30), (182, 56), (104, 92)]
        left = [(40, 64), (104, 92), (104, 196), (40, 166)]
        right = [(104, 92), (182, 56), (182, 160), (104, 196)]
        _ink_poly(d, right, ACC_L, seed + 2, INK_W - 1, amp=1.0)
        _hatch_in(im, (104, 56, 182, 196), lambda q, S_: q.polygon(_P(right), fill=255), -40, 9, 60)
        _ink_poly(d, left, SALTW, seed + 1, INK_W - 1, amp=1.0)
        _ink_poly(d, top, (255, 255, 255), seed, INK_W - 1, amp=1.0)
        d.line(_P([(60, 70), (110, 48)]), fill=(255, 255, 255, 255), width=5 * SC3)
        if mood: _face(d, S, 72, 136, 1.15, mood, look)
        return _done(im, w, h)
    return gcache(("salt31", mood, look, seed), mk)


def shaker_el(mood=None, look=(0, 0), seed=313):
    """a glass salt shaker: a ribbed glass body full of white salt, a steel cap with holes."""
    def mk():
        w, h = 200, 300; im, d, S = _cv(w, h)
        body = [(48, 90), (152, 90), (164, 270), (36, 270)]
        _ink_poly(d, body, (232, 240, 246), seed, INK_W, amp=1.2)
        sal = [(44, 150), (156, 150), (163, 266), (37, 266)]
        d.polygon(_P(sal), fill=SALTW + (255,))
        for k in range(16): d.ellipse(S(50 + (k * 37) % 100, 156 + (k * 23) % 100, 56 + (k * 37) % 100, 162 + (k * 23) % 100), fill=SALT_S + (255,))
        _ink_poly(d, body, None, seed, INK_W, amp=1.2)
        for x in (70, 100, 130): d.line(_P([(x, 100), (x + 2, 262)]), fill=(200, 214, 226, 160), width=4 * SC3)
        cap = [(44, 50), (156, 50), (160, 92), (40, 92)]
        _ink_poly(d, cap, STEEL, seed + 1, INK_W, amp=1.0)
        _ink_ell(d, 100, 50, 56, 16, (226, 232, 238), seed + 2, INK_W - 2, amp=0.8)
        for (x, y) in ((84, 48), (100, 44), (116, 48), (92, 54), (108, 54)): d.ellipse(S(x - 3, y - 2, x + 3, y + 2), fill=INKC + (255,))
        if mood: _face(d, S, 100, 210, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("shaker31", mood, look, seed), mk)


def cell_buddy_el(mood="happy", look=(0, 0), k=0.0, seed=314):
    """a body CELL as a round pink buddy with a nucleus; k 0..1 = how much water it has lost (shrinks, the outline goes wrinkly, it sags)."""
    kk = round(clamp(k) * 5) / 5
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h)
        r = 96 * (1 - 0.32 * kk)
        P = []
        for i in range(36):
            a = 2 * math.pi * i / 36; rr = r * (1 + kk * 0.09 * math.sin(9 * a + seed) + kk * 0.05 * math.sin(14 * a))
            P.append((120 + rr * math.cos(a), 124 + rr * 0.94 * math.sin(a) + kk * 10))
        _ink_poly(d, P, CELLP, seed, INK_W - 1, amp=1.2 + 1.5 * kk)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(120 - r * 0.2, 124 - r * 0.1, 120 + r * 1.9, 124 + r * 1.9), fill=c), CELLP_S, 120)
        _hatch_in(im, (120, 120, 230, 230), lambda q, S_: q.polygon(_P(P), fill=255), -40, 9, 28)
        nx, ny = 120 + r * 0.42, 124 + r * 0.38 + kk * 8
        _ink_ell(d, nx, ny, r * 0.2, r * 0.18, CELLP_N, seed + 1, INK_W - 3, amp=0.8)
        d.line(_P([(120 - r * 0.6, 124 - r * 0.45), (120 - r * 0.3, 124 - r * 0.7)]), fill=(255, 255, 255, 200), width=6 * SC3)
        _face(d, S, 112, 116 + kk * 8, 1.3 * (1 - 0.2 * kk), mood, look)
        return _done(im, w, h)
    return gcache(("cellb31", mood, look, kk, seed), mk)


def checker_el(mood="n", look=(0, 0), needle=0.2, ring=False, seed=315):
    """THE SALT CHECKER (the subfornical organ): a small brain-pink buddy in a lab cap with a round DIAL on its belly (needle 0..1 = how salty);
    ring=True: the little alarm bell on its cap is ringing (accent glow + motion strokes)."""
    nd = round(clamp(needle) * 10) / 10
    def mk():
        w, h = 260, 300; im, d, S = _cv(w, h)
        body = _arcpts(130, 180, 96, 100, 0, 360, 30)[:-1]
        _ink_poly(d, body, (244, 176, 196), seed, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.ellipse(S_(150, 120, 300, 320), fill=c), (210, 130, 160), 120)
        for k in range(3):                                                                   # brain folds
            d.line(_P(_wob([(70 + k * 10, 110 + k * 20), (100, 100 + k * 18), (130, 116 + k * 16)], 1.2, seed + 10 + k)), fill=(196, 110, 140, 200), width=4 * SC3, joint="curve")
        cap = [(64, 98), (196, 98), (186, 64), (74, 64)]
        _ink_poly(d, cap, (250, 250, 248), seed + 1, INK_W - 1, amp=1.0)
        _ink_ell(d, 130, 46, 20, 18, ACC if ring else (226, 206, 120), seed + 2, INK_W - 2, amp=0.8)     # the bell
        d.line(S(130, 24, 130, 30), fill=INKC + (255,), width=4 * SC3)
        if ring:
            for sg in (-1, 1):
                for j in (0, 1): d.arc(S(130 - 40 - j * 16, 46 - 30 - j * 14, 130 + 40 + j * 16, 46 + 30 + j * 14), 200 if sg < 0 else -20, 240 if sg < 0 else 20, fill=ACC_S + (255,), width=4 * SC3)
        _ink_ell(d, 130, 206, 46, 44, (255, 252, 244), seed + 3, INK_W - 2, amp=0.8)             # the dial
        for j in range(5):
            a = math.radians(200 + 140 * j / 4); d.line(S(130 + 34 * math.cos(a), 210 + 34 * math.sin(a), 130 + 40 * math.cos(a), 210 + 40 * math.sin(a)), fill=INKC + (255,), width=3 * SC3)
        d.arc(S(96, 176, 164, 244), 305, 340, fill=ACC + (255,), width=7 * SC3)               # the 'too salty' zone
        a = math.radians(200 + 140 * nd); d.line(S(130, 210, 130 + 32 * math.cos(a), 210 + 32 * math.sin(a)), fill=(ACC_S if nd > 0.7 else INKC) + (255,), width=5 * SC3)
        d.ellipse(S(125, 205, 135, 215), fill=INKC + (255,))
        _face(d, S, 130, 140, 1.25, mood, look)
        return _done(im, w, h)
    return gcache(("checker31", mood, look, nd, ring, seed), mk)


def courier_el(mood="happy", look=(0, 0), seed=316):
    """VASOPRESSIN as a courier: a small blue drop-shaped buddy with a peaked courier cap and a satchel strap."""
    def mk():
        w, h = 200, 240; im, d, S = _cv(w, h)
        P = [(100, 30)] + _arcpts(100, 150, 70, 72, -40, 220, 26)
        _ink_poly(d, P, (150, 196, 240), seed, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(110, 90, 240, 260), fill=c), WAT_S, 110)
        d.line(_P([(50, 120), (150, 196)]), fill=(150, 104, 60, 255), width=7 * SC3)                  # satchel strap
        cap = [(58, 92), (142, 92), (136, 70), (64, 70)]
        _ink_poly(d, cap, (40, 70, 130), seed + 1, INK_W - 2, amp=0.8)
        d.line(S(56, 94, 170, 98), fill=INKC + (255,), width=6 * SC3)
        _face(d, S, 98, 140, 1.25, mood, look)
        return _done(im, w, h)
    return gcache(("courier31", mood, look, seed), mk)


def urea_el(mood="happy", look=(0, 0), seed=317):
    """UREA: a small olive-lime buddy with stubby arms up (it holds a rope in the shots), little 'U' on its belly."""
    def mk():
        w, h = 200, 220; im, d, S = _cv(w, h)
        _ink_ell(d, 100, 130, 66, 62, UREA, seed, INK_W - 1, amp=1.2)
        _shade(im, lambda q, S_: q.ellipse(S_(34, 68, 166, 192), fill=255), lambda q, S_, c: q.ellipse(S_(100, 100, 220, 230), fill=c), UREA_S, 120)
        for sg in (-1, 1): d.line(_P(_wob([(100 + sg * 58, 110), (100 + sg * 84, 70)], 1.0, seed + sg)), fill=INKC + (255,), width=6 * SC3)
        d.arc(S(84, 150, 116, 182), 0, 180, fill=UREA_S + (255,), width=5 * SC3)
        _face(d, S, 100, 118, 1.2, mood, look)
        return _done(im, w, h)
    return gcache(("urea31", mood, look, seed), mk)


def magnet_el(seed=318):
    """a red horseshoe magnet with steel tips (opening down)."""
    def mk():
        w, h = 240, 260; im, d, S = _cv(w, h)
        outer = _arcpts(120, 110, 100, 90, 180, 360, 20); inner = _arcpts(120, 110, 50, 44, 360, 180, 20)
        P = outer + [(220, 200), (170, 200)] + inner + [(70, 200), (20, 200)]
        _ink_poly(d, P, MAG, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(130, 0, 240, 260), fill=c), MAG_S, 120)
        for x0 in (20, 170):
            _ink_poly(d, [(x0, 200), (x0 + 50, 200), (x0 + 50, 244), (x0, 244)], STEEL, seed + x0, INK_W - 1, amp=0.8)
        d.line(_P([(54, 90), (80, 50)]), fill=(255, 255, 255, 190), width=7 * SC3)
        return _done(im, w, h)
    return gcache(("magnet31", seed), mk)


def wdrop_el(mood="happy", look=(0, 0), seed=319):
    """a WATER DROP buddy (clear blue, white glint)."""
    def mk():
        w, h = 160, 200; im, d, S = _cv(w, h)
        P = [(80, 16)] + _arcpts(80, 128, 58, 58, -42, 222, 24)
        _ink_poly(d, P, WAT_L, seed, INK_W - 2, amp=1.0, col=WAT_S)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(80, 90, 200, 220), fill=c), WAT, 140)
        d.line(_P([(54, 100), (60, 76)]), fill=(255, 255, 255, 255), width=7 * SC3)
        if mood: _face(d, S, 84, 134, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("wdrop31", mood, look, seed), mk)


def tray_el(salty=False, seed=320):
    """a space-food tray: 3 compartments (rice, veg, a bread roll) + a salt shaker sign when salty."""
    def mk():
        w, h = 360, 170; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 40), (346, 40), (330, 156), (30, 156)], (214, 220, 228), seed, INK_W - 1, amp=1.0)
        for i, (x0, col) in enumerate(((36, (250, 246, 232)), (140, (120, 180, 90)), (244, (226, 176, 110)))):
            _ink_poly(d, [(x0, 56), (x0 + 88, 56), (x0 + 84, 140), (x0 + 4, 140)], (236, 238, 242), seed + i + 1, INK_W - 3, amp=0.8)
            _ink_ell(d, x0 + 44, 98, 32, 24, col, seed + 10 + i, INK_W - 3, amp=0.8)
        if salty:
            for k in range(18): d.ellipse(S(40 + (k * 53) % 290, 70 + (k * 31) % 60, 46 + (k * 53) % 290, 76 + (k * 31) % 60), fill=SALTW + (255,), outline=ACC_S + (255,), width=SC3)
        return _done(im, w, h)
    return gcache(("tray31", salty, seed), mk)


# ---------- NEW PLACE 1: the TV ROOM at night (movie night: one cool flickering TV glow from the camera side + a warm lamp in the corner) ----------
def set_tvroom(t=0.0, blur=4, top_y=1330, flick=1.0):
    def mk():
        f = _vgrad((92, 98, 132), (60, 62, 92), 0, top_y)                                     # night wall
        cv2.rectangle(f, (640, 380), (1000, 900), C((52, 46, 60)), -1, cv2.LINE_AA)            # window frame
        f[400:880, 660:980] = _vgrad((24, 28, 64), (60, 50, 90), 400, 880)[400:880, 660:980]
        for (x, y) in ((700, 450), (760, 520), (900, 470), (940, 600), (820, 430)): cv2.circle(f, (x, y), 3, C((240, 240, 255)), -1, cv2.LINE_AA)
        cv2.circle(f, (880, 540), 38, C((236, 232, 214)), -1, cv2.LINE_AA)                       # moon
        cv2.line(f, (820, 400), (820, 880), C((52, 46, 60)), 10, cv2.LINE_AA)
        cv2.rectangle(f, (80, 520), (300, 760), C((150, 120, 100)), -1, cv2.LINE_AA)            # a framed picture
        f[540:740, 100:280] = _vgrad((210, 170, 120), (130, 150, 120), 540, 740)[540:740, 100:280]
        cv2.rectangle(f, (110, 960), (200, 1240), C((120, 90, 70)), -1, cv2.LINE_AA)            # lamp stand
        cv2.ellipse(f, (155, 940), (90, 70), 0, 180, 360, C((250, 214, 150)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (0, 1240), (W, top_y), C((70, 60, 70)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("tvroom31", blur, top_y), mk).copy()
    glow(f, 155, 930, 330, (255, 200, 130), 0.22)
    fl = flick * (0.75 + 0.18 * math.sin(t * 13.0) + 0.07 * math.sin(t * 37.0 + 1.0))     # the TV flicker (cool blue key light from the viewer's side)
    glow(f, 540, 1300, 900, (140, 180, 255), 0.16 * fl)
    return inkify(f)


def sofa_front(f, top_y=1360):
    """the front of a sofa cushion row (Chubby sits behind it): muted teal with ink seams, a cushion, lit blue by the TV."""
    cv2.rectangle(f, (0, top_y), (W, H), C((70, 120, 130)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y), (W, top_y + 60), C((96, 150, 156)), -1, cv2.LINE_AA)
    for x in (360, 720): cv2.line(f, (x, top_y + 10), (x, top_y + 160), C(INKC), 4, cv2.LINE_AA)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 60), (W, top_y + 60), C(INKC), 4, cv2.LINE_AA)
    _hatch_band(f, top_y + 64, H)


# ---------- NEW PLACE 2: THE CAPSULE (inside a mock spaceship module on the ground: curved white panels, a porthole with a painted Mars, a console with lamps) ----------
def set_capsule(t=0.0, blur=4, top_y=1330, dim=0.0):
    def mk():
        f = _vgrad((226, 230, 234), (196, 202, 210), 0, top_y)
        for x in range(0, W + 1, 180):                                                        # panel seams + rivets
            cv2.line(f, (x, 0), (x, top_y), C((170, 176, 186)), 4, cv2.LINE_AA)
            for y in range(120, top_y, 160): cv2.circle(f, (x + 14, y), 5, C((150, 156, 166)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (540, 0), (700, 260), 0, 0, 180, C((206, 212, 220)), -1, cv2.LINE_AA)    # curved ceiling
        cv2.ellipse(f, (540, 0), (700, 260), 0, 0, 180, C((160, 166, 176)), 6, cv2.LINE_AA)
        cv2.circle(f, (760, 640), 210, C((120, 126, 138)), -1, cv2.LINE_AA)                     # porthole frame
        cv2.circle(f, (760, 640), 180, C((14, 16, 34)), -1, cv2.LINE_AA)
        for k in range(26):
            x, y = 760 + int(170 * math.cos(k * 2.3)), 640 + int(160 * math.sin(k * 1.7)) * ((k % 3) / 2)
            cv2.circle(f, (x, int(y)), 2, C((240, 240, 255)), -1, cv2.LINE_AA)
        cv2.circle(f, (700, 700), 92, C(MARS), -1, cv2.LINE_AA)                                  # Mars (a painted one: it's a pretend trip)
        cv2.circle(f, (730, 724), 70, C(MARS_S), -1, cv2.LINE_AA); cv2.circle(f, (690, 690), 70, C(MARS), -1, cv2.LINE_AA)
        for (x, y, r) in ((670, 670, 12), (720, 730, 9)): cv2.circle(f, (x, y), r, C(MARS_S), -1, cv2.LINE_AA)
        for k in range(12): cv2.circle(f, (int(760 + 196 * math.cos(k * math.pi / 6)), int(640 + 196 * math.sin(k * math.pi / 6))), 7, C((90, 96, 108)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (80, 420), (380, 900), C((170, 176, 186)), -1, cv2.LINE_AA)           # a wall locker with a calendar
        cv2.rectangle(f, (110, 450), (350, 640), C((250, 250, 246)), -1, cv2.LINE_AA)
        for r_ in range(4):
            for c_ in range(6): cv2.rectangle(f, (124 + c_ * 36, 500 + r_ * 32), (148 + c_ * 36, 522 + r_ * 32), C((214, 218, 224)), -1)
        cv2.rectangle(f, (110, 450), (350, 486), C((200, 84, 60)), -1)
        cv2.rectangle(f, (0, 1180), (W, top_y), C((150, 156, 166)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("capsule31", blur, top_y), mk).copy()
    glow(f, 540, 120, 520, (255, 252, 236), 0.18)                                                # ceiling strip light
    for i, x in enumerate(range(140, 1000, 70)):                                                  # blinking status lamps on the ceiling rim
        on = (math.sin(t * 3 + i * 1.7) > 0.2)
        cv2.circle(f, (x, 300 + int(30 * math.sin(i))), 7, C((120, 220, 140) if on else (90, 110, 100)), -1, cv2.LINE_AA)
    if dim > 0: f *= (1 - 0.45 * dim)
    return inkify(f)


def capsule_front(f, top_y=1330):
    """the crew's console / table edge: grey metal top with a lit strip of buttons, darker front panel with hatching."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 46), C((176, 182, 192)), -1, cv2.LINE_AA)
    for i, x in enumerate(range(60, W, 90)):
        cv2.rectangle(f, (x, top_y + 14), (x + 40, top_y + 32), C(((236, 128, 52), (120, 210, 150), (250, 220, 120))[i % 3]), -1, cv2.LINE_AA)
    f[top_y + 46:, :] = f[top_y + 46:, :] * 0 + np.array(C((96, 102, 114)), np.float32)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 46), (W, top_y + 46), C(INKC), 5, cv2.LINE_AA)
    _hatch_band(f, top_y + 50, H)
