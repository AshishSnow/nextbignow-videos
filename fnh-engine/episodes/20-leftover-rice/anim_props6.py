# ================= anim_props_lib20.py (ep 20, 1 Nov): the LEFTOVER RICE ink props + the NIGHT STOVE place.
# ONE accent per video: WARM ORANGE = the 'warm hours' (the danger zone, the germs, the toxin, the titles, the chips); COLD BLUE = the fridge /
# the fix side; paper = the rice. Props: grains (a heap of ink rice grains), rice_pot_el (cut-away steel pot of rice, steam / warm glow),
# rice_bowl_el (fluffy / hard pebbles / steam / fried / salad), grain_el (one big rice grain character, soft or hard), spore_el (an armoured
# seed with a sleepy face; crack 0..1 = the germ hatching out), germ_el (rod-shaped bacterium with a face, wiggly hairs), germ_crowd,
# toxin_el (a lumpy poison blob, optional fire helmet = 'shrugs off heat'), microwave_el, thermo_ink_el (thermometer with a 'warm zone'),
# starch_rows (the retrogradation diagram: loose swollen chains <-> tight neat rows, water squeezed out), dish_el (wide shallow dish vs a
# deep pot), bin_ink_el, clock_ink_el (night clock with live hands); place set_stove_night (the stove after dinner, lights off, moon window,
# one warm under-cabinet lamp on the pot). =================
ACC = (226, 112, 40); ACC_S = (162, 68, 20); ACC_L = (246, 180, 122); ACC_XL = (252, 228, 204)      # warm orange accent
RICE = (252, 250, 242); RICE_S = (222, 214, 196); RICE_H = (234, 226, 208)
BLUE = (60, 120, 186); BLUE_S = (36, 80, 140); BLUE_L = (206, 228, 248)
MILK = (252, 248, 238)
STEEL = (196, 202, 210); STEEL_S = (140, 148, 160)
SCHEMES["ricep"] = ((240, 230, 210), (252, 248, 236), (232, 220, 196), (0.78, 0.72, 0.6))
SCHEMES["warmp"] = ((246, 196, 150), (252, 232, 206), (240, 184, 132), (0.85, 0.6, 0.4))
SCHEMES["coldp"] = ((188, 214, 238), (232, 242, 252), (172, 202, 230), (0.55, 0.68, 0.82))
SCHEMES["germp"] = ((120, 60, 30), (210, 130, 70), (104, 50, 24), (0.45, 0.25, 0.12))
SCHEMES["mintp"] = ((170, 226, 206), (222, 246, 236), (150, 210, 190), (0.5, 0.75, 0.65))


def _grain(d, S, x, y, ang, L=22, wd=10, fill=RICE, seed=0, hard=False):
    """one small ink rice grain (an elongated oval) at (x, y) rotated by ang (deg)."""
    a = math.radians(ang); pts = []
    for i in range(14):
        th = 2 * math.pi * i / 14; px, py = L / 2 * math.cos(th), wd / 2 * math.sin(th)
        pts.append((x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)))
    _ink_poly(d, pts, fill if not hard else (226, 220, 206), seed, 1.6 if not hard else 2.4, amp=0.3 if not hard else 0.7, col=(120, 100, 84) if not hard else INKC)
    if hard: d.line(S(x - 3, y - 2, x + 3, y + 2), fill=INKC + (160,), width=2 * SC3)


def grains(d, S, cx, cy, rx, ry, n=60, seed=1, hard=False, tint=None, top_only=False):
    """a heap / mound of rice grains filling an ellipse (cx, cy, rx, ry); hard = tighter, greyer, cracked (fridge rice)."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        r_ = math.sqrt(rng.uniform(0, 1)); th = rng.uniform(0, 2 * math.pi)
        x = cx + r_ * rx * math.cos(th); y = cy + r_ * ry * math.sin(th)
        if top_only and y > cy + ry * 0.3: continue
        col = tint[i % len(tint)] if (tint and rng.uniform() < 0.18) else RICE
        _grain(d, S, x, y, rng.uniform(-35, 35) + (90 if rng.uniform() < 0.3 else 0) if not hard else rng.uniform(-12, 12), 30 if not hard else 24, 14 if not hard else 11, col, seed * 100 + i, hard)


def rice_pot_el(level=0.75, warm=0.0, lid=False, seed=1, mood=None):
    """a CUT-AWAY steel pot of cooked rice from the front: steel walls with handles, the rice mound inside; warm 0..1 = an orange warmth
    wash over the rice (the danger hours); lid = a domed lid on top; mood = a face on the pot."""
    warm = round(clamp(warm) * 5) / 5
    def mk():
        w, h = 420, 340; im, d, S = _cv(w, h)
        body = [(50, 90), (370, 90), (356, 300), (64, 300)]
        for sx in (1, -1):                                                                                      # handles
            hx = 30 if sx > 0 else 390
            _ink_poly(d, [(hx - 22, 110), (hx + 22, 110), (hx + 22, 132), (hx - 22, 132)], STEEL_S, seed + 3 + sx, INK_W - 2, amp=0.8)
        _ink_poly(d, body, STEEL, seed + 1, INK_W, amp=1.6)
        # cut-away: the rice mound inside the open front
        top = 300 - 200 * level
        inner = [(70, top + 10), (350, top + 10), (342, 290), (78, 290)]
        d.polygon([(x * SC3, y * SC3) for x, y in inner], fill=RICE_H + (255,))
        grains(d, S, 210, top + 70, 130, 60 * level + 20, int(45 * level) + 14, seed + 5)
        grains(d, S, 210, top + 4, 140, 26, 26, seed + 6)
        if warm > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(lay)
            q.ellipse(S(60, top - 40, 360, 300), fill=ACC + (int(90 * warm),)); lay = lay.filter(ImageFilter.GaussianBlur(14 * SC3))
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon([(x * SC3, y * SC3) for x, y in inner], fill=255)
            im.alpha_composite(Image.composite(lay, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
        d.line([(x * SC3, y * SC3) for x, y in _wob([(70, top + 10), (350, top + 10)], 1.2, seed + 7)], fill=INKC + (200,), width=3 * SC3)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.polygon(S_(330, 80, 380, 80, 380, 310, 330, 310), fill=c), STEEL_S, 140)
        _hatch_in(im, (300, 90, 370, 300), lambda q, S_: q.polygon(S_(336, 90, 370, 90, 356, 300, 330, 300), fill=255), -40, 9, 40)
        d.line(S(80, 120, 76, 270), fill=(255, 255, 255, 170), width=5 * SC3)                                   # steel glint
        _ink_poly(d, [(40, 80), (380, 80), (380, 96), (40, 96)], STEEL, seed + 9, INK_W - 2, amp=0.8)          # rim
        if lid:
            dome = _arcpts(210, 82, 176, 60, 180, 360, 20)
            _ink_poly(d, dome, STEEL, seed + 11, INK_W - 1, amp=1.2)
            _ink_ell(d, 210, 20, 22, 12, STEEL_S, seed + 12, INK_W - 2, n=14, amp=0.8)
        if mood: _face(d, S, 210, 200 if not lid else 200, 1.4, mood)
        return _done(im, w, h)
    return gcache(("ricepot20", level, warm, lid, seed, mood), mk)


def rice_bowl_el(state="fluffy", seed=1, mood=None, look=(0, 0)):
    """an ink bowl of rice. state: fluffy (loose soft grains), hard (tight greyish pebbles with cracks), fried (yellow rice with peas +
    carrot bits), salad (rice + tomato + peas + herbs). mood = a face on the bowl."""
    def mk():
        w, h = 360, 260; im, d, S = _cv(w, h)
        hard = state == "hard"
        tint = {"fried": [(240, 200, 90), (110, 170, 80), (236, 120, 60)], "salad": [(220, 70, 60), (110, 170, 80), (90, 150, 90)]}.get(state)
        base = {"fried": (246, 222, 150)}.get(state, RICE_H if not hard else (214, 208, 196))
        d.ellipse(S(40, 50, 320, 150), fill=base + (255,))
        if state == "fried":
            grains(d, S, 180, 96, 128, 54, 60, seed + 2, False, [(244, 204, 100), (110, 170, 80), (236, 120, 60)])
        else:
            grains(d, S, 180, 96, 128, 54, 60 if not hard else 80, seed + 2, hard, tint)
        bowl = [(24, 120), (336, 120), (300, 216), (240, 240), (120, 240), (60, 216)]
        _ink_poly(d, bowl, (236, 240, 244) if state != "fried" else (70, 72, 80), seed + 3, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in bowl], fill=255), lambda q, S_, c: q.polygon(S_(220, 110, 340, 110, 340, 250, 210, 250), fill=c), (180, 190, 200) if state != "fried" else (40, 40, 46), 140)
        _hatch_in(im, (230, 120, 330, 240), lambda q, S_: q.polygon(S_(236, 124, 330, 124, 296, 214, 240, 236), fill=255), -40, 9, 36)
        d.line(S(70, 140, 100, 200), fill=(255, 255, 255, 170), width=5 * SC3)
        if state != "fried": d.line([(x * SC3, y * SC3) for x, y in _wob([(30, 124), (330, 124)], 1.0, seed + 4)], fill=(120, 170, 220, 255) if state != "salad" else ACC + (255,), width=5 * SC3)
        if hard:
            for (x0, y0) in ((110, 70), (230, 80), (170, 110)):
                d.line(S(x0, y0, x0 + 14, y0 + 10, x0 + 6, y0 + 22), fill=INKC + (220,), width=3 * SC3)
        if mood: _face(d, S, 180, 186, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("ricebowl20", state, seed, mood, look), mk)


def grain_el(mood="n", hard=False, look=(0, 0), seed=1):
    """ONE big rice grain character (for close-ups): soft = plump cream with a shine; hard = greyer, tighter, with crack lines."""
    def mk():
        w, h = 200, 300; im, d, S = _cv(w, h)
        body = _arcpts(100, 150, 70 if not hard else 62, 128 if not hard else 120, 0, 360, 30)[:-1]
        _ink_poly(d, body, RICE if not hard else (222, 216, 202), seed + 1, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.ellipse(S_(110, 30, 220, 290), fill=c), RICE_S if not hard else (180, 174, 160), 130)
        _hatch_in(im, (120, 40, 180, 270), lambda q, S_: q.ellipse(S_(124, 40, 190, 270), fill=255), -40, 10, 30)
        if not hard: d.ellipse(S(62, 70, 82, 120), fill=(255, 255, 255, 220))
        else:
            for (x0, y0) in ((60, 90), (120, 200), (80, 230)):
                d.line(S(x0, y0, x0 + 16, y0 + 12, x0 + 6, y0 + 28), fill=INKC + (230,), width=4 * SC3)
        _face(d, S, 100, 150, 1.6, mood, look)
        return _done(im, w, h)
    return gcache(("grain20", mood, hard, look, seed), mk)


def spore_el(mood="sleepy", crack=0.0, seed=1):
    """the SPORE = 'a seed wearing armour': an oval seed in overlapping ink armour plates (warm brown-orange), a sleepy face; crack 0..1
    splits the shell along the middle and the germ peeks out."""
    crack = round(clamp(crack) * 4) / 4
    def mk():
        w, h = 220, 220; im, d, S = _cv(w, h)
        shell = _arcpts(110, 116, 78, 90, 0, 360, 26)[:-1]
        if crack > 0:                                                                                             # the germ peeking out (behind)
            _ink_ell(d, 110, 60 - 30 * crack, 30, 40, ACC_L, seed + 9, INK_W - 2, n=18, amp=1.2)
            _face(d, S, 110, 60 - 30 * crack, 0.8, "wow" if crack < 1 else "happy")
        _ink_poly(d, shell, (232, 170, 104), seed + 1, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in shell], fill=255), lambda q, S_, c: q.ellipse(S_(120, 30, 230, 220), fill=c), ACC_S, 120)
        for r_ in range(4):                                                                                       # armour plates
            y = 60 + r_ * 34
            d.line([(x * SC3, yy * SC3) for x, yy in _wob(_arcpts(110, y - 30, 70 - 6 * abs(r_ - 1.5), 34, 30, 150, 10), 0.8, seed + 20 + r_)], fill=INKC + (210,), width=3 * SC3)
        for (x0, y0) in ((70, 80), (150, 90), (90, 150), (140, 160)):
            d.ellipse(S(x0 - 4, y0 - 4, x0 + 4, y0 + 4), fill=INKC + (200,))                                     # rivets
        if crack > 0:
            zz = [(36, 110), (60, 98), (80, 116), (104, 96), (128, 118), (150, 98), (176, 114), (186, 106)]
            d.line([(x * SC3, y * SC3) for x, y in zz], fill=INKC + (255,), width=5 * SC3, joint="curve")
        if crack < 1:
            if mood == "sleepy":
                for sgn in (-1, 1):
                    x = 110 + sgn * 22
                    d.line([(q * SC3) for q in (x - 11, 136, x + 11, 136)], fill=INKC + (255,), width=5 * SC3)
                d.line([(x * SC3, y * SC3) for x, y in _arcpts(110, 160, 10, 6, 20, 160, 8)], fill=INKC + (255,), width=4 * SC3, joint="curve")
                d.text((190 * SC3, 40 * SC3), "z", font=font(F_BLACK, 30 * SC3), fill=INKC + (255,), anchor="mm"); d.text((206 * SC3, 14 * SC3), "z", font=font(F_BLACK, 20 * SC3), fill=INKC + (255,), anchor="mm")
            else:
                _face(d, S, 110, 146, 1.2, mood)
        return _done(im, w, h)
    return gcache(("spore20", mood, crack, seed), mk)


def germ_el(mood="n", look=(0, 0), seed=1, ph=0):
    """Bacillus = a ROD: an orange capsule with a face and wiggly hairs (ph 0..3 = hair wiggle frame)."""
    def mk():
        w, h = 240, 140; im, d, S = _cv(w, h)
        for i in range(9):                                                                                         # hairs
            a = -150 + i * 38; x0 = 120 + 92 * math.cos(math.radians(a)); y0 = 70 + 44 * math.sin(math.radians(a))
            x1 = x0 + 18 * math.cos(math.radians(a)) + 6 * math.sin(ph * 1.6 + i); y1 = y0 + 18 * math.sin(math.radians(a)) + 6 * math.cos(ph * 1.6 + i)
            d.line(S(x0, y0, (x0 + x1) / 2 + 4, (y0 + y1) / 2 - 4, x1, y1), fill=INKC + (255,), width=3 * SC3)
        body = [(40, 34), (200, 34), (226, 70), (200, 106), (40, 106), (14, 70)]
        body = _arcpts(70, 70, 46, 38, 90, 270, 10) + _arcpts(170, 70, 46, 38, -90, 90, 10)
        _ink_poly(d, body, ACC, seed + 1, INK_W - 1, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.rectangle(S_(20, 76, 230, 120), fill=c), ACC_S, 120)
        _hatch_in(im, (30, 80, 220, 110), lambda q, S_: q.rectangle(S_(30, 82, 220, 110), fill=255), -40, 9, 34)
        d.ellipse(S(52, 44, 80, 56), fill=(255, 255, 255, 150))
        _face(d, S, 120, 72, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("germ20", mood, look, seed, ph), mk)


def germ_crowd(f, cx, cy, t, n=8, s=0.5, rad=160, mood="happy", seed=4, op=1.0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi); r_ = rad * math.sqrt(rng.uniform(0.05, 1))
        x = cx + r_ * math.cos(a) * 1.3 + 8 * math.sin(t * 3 + i); y = cy + r_ * math.sin(a) * 0.8 + 6 * math.cos(t * 2.6 + i)
        comp(f, _rot_el(scale_el(germ_el(mood, (math.sin(t + i), 0), 1 + i % 3, int(t * 8 + i) % 4), s), rng.uniform(-30, 30)), x, y, op=op)


def toxin_el(mood="angry", helmet=False, seed=1):
    """the TOXIN: a lumpy dark-orange poison blob with drips and a mean face; helmet = a little fire helmet (it 'shrugs off heat')."""
    def mk():
        w, h = 260, 260; im, d, S = _cv(w, h)
        rng = np.random.default_rng(seed); P = []
        for i in range(22):
            a = 2 * math.pi * i / 22; r_ = 86 + 12 * math.sin(i * 2.7) + rng.uniform(-5, 5)
            P.append((130 + r_ * math.cos(a), 150 + r_ * 0.86 * math.sin(a)))
        _ink_poly(d, P, (200, 90, 34), seed + 1, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in P], fill=255), lambda q, S_, c: q.ellipse(S_(130, 70, 260, 260), fill=c), (130, 50, 18), 140)
        _hatch_in(im, (140, 80, 230, 230), lambda q, S_: q.ellipse(S_(140, 80, 240, 240), fill=255), -40, 9, 40)
        for (x0, L) in ((80, 34), (150, 46), (190, 26)):                                                            # drips
            _ink_poly(d, [(x0 - 9, 218), (x0 + 9, 218), (x0 + 6, 218 + L), (x0, 226 + L), (x0 - 6, 218 + L)], (200, 90, 34), seed + x0, INK_W - 2, amp=0.8)
        d.ellipse(S(80, 98, 104, 116), fill=(255, 255, 255, 140))
        _face(d, S, 130, 160, 1.6, mood)
        if helmet:
            hel = _arcpts(130, 82, 82, 50, 180, 360, 16) + [(222, 86), (38, 86)]
            _ink_poly(d, hel, (214, 50, 40), seed + 30, INK_W - 1, amp=1.0)
            _ink_poly(d, [(30, 80), (230, 80), (236, 94), (24, 94)], (176, 34, 30), seed + 31, INK_W - 2, amp=0.8)
            _ink_poly(d, [(116, 40), (144, 40), (146, 70), (114, 70)], (250, 210, 90), seed + 32, INK_W - 3, amp=0.6)
        return _done(im, w, h)
    return gcache(("toxin20", mood, helmet, seed), mk)


def microwave_el(on=False, timer="0:30", seed=1, inside=None):
    """an ink microwave from the front: body, a dark window (glows warm when on), a keypad + a little display."""
    def mk():
        w, h = 520, 320; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 30), (500, 30), (500, 300), (20, 300)], (236, 232, 222), seed + 1, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.rectangle(S_(20, 30, 500, 300), fill=255), lambda q, S_, c: q.rectangle(S_(20, 250, 500, 300), fill=c), (200, 192, 176), 140)
        win = [(50, 60), (360, 60), (360, 270), (50, 270)]
        _ink_poly(d, win, (255, 190, 110) if on else (60, 62, 70), seed + 2, INK_W - 1, amp=1.0)
        if on:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse(S(90, 90, 320, 250), fill=(255, 240, 200, 200))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(20 * SC3)))
        d.line(S(70, 80, 120, 80), fill=(255, 255, 255, 140), width=4 * SC3)
        _ink_poly(d, [(380, 70), (480, 70), (480, 120), (380, 120)], (40, 46, 40), seed + 3, 3, amp=0.5)
        d.text((430 * SC3, 96 * SC3), timer, font=font(F_BLACK, 32 * SC3), fill=(120, 250, 140, 255) if on else (90, 160, 100, 255), anchor="mm")
        for r_ in range(3):
            for c in range(3): _ink_ell(d, 400 + c * 32, 150 + r_ * 34, 11, 11, (214, 208, 196), seed + 10 + r_ * 3 + c, 3, n=12, amp=0.5)
        _ink_poly(d, [(392, 254), (472, 254), (472, 282), (392, 282)], ACC, seed + 30, 3, amp=0.5)
        return _done(im, w, h)
    return gcache(("micro20", on, timer, seed), mk)


def thermo_ink_el(k=0.5, zone=True, seed=1, label=None):
    """a vertical ink thermometer; k 0..1 = the red-orange column height; zone = a shaded 'WARM = GERMS GROW' band (10-50 C)."""
    k = round(clamp(k) * 20) / 20
    def mk():
        w, h = 160, 520; im, d, S = _cv(w, h)
        _ink_poly(d, [(56, 40), (104, 40), (104, 420), (56, 420)], (250, 250, 248), seed + 1, INK_W - 1, amp=0.8)
        _ink_ell(d, 80, 450, 46, 46, ACC, seed + 2, INK_W - 1, n=20, amp=0.8)
        top = 410 - 360 * k
        d.rectangle(S(68, top, 92, 420), fill=ACC + (255,))
        if zone:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle(S(20, 160, 140, 360), fill=ACC_L + (110,))
            im.alpha_composite(lay); d.line(S(20, 160, 140, 160), fill=ACC_S + (255,), width=3 * SC3); d.line(S(20, 360, 140, 360), fill=ACC_S + (255,), width=3 * SC3)
        for i in range(9): d.line(S(104, 60 + i * 42, 120, 60 + i * 42), fill=INKC + (255,), width=3 * SC3)
        d.ellipse(S(62, 432, 76, 450), fill=(255, 255, 255, 180))
        return _done(im, w, h)
    return gcache(("thermo20", k, zone, seed), mk)


def starch_rows(f, cx, cy, k, t, w=560, h=420, n=6, water=True):
    """the RETROGRADATION diagram drawn live: k = 0 -> loose, swollen, wiggly starch chains with water drops between them (fluffy rice);
    k = 1 -> the same chains pulled into neat, tight, straight rows (a crystal-ish block), water squeezed out to the sides."""
    k = clamp(k)
    for i in range(n):
        y_loose = cy - h / 2 + (i + 0.5) * h / n; y_tight = cy - (n - 1) * 26 / 2 + i * 26
        y0 = y_loose + (y_tight - y_loose) * eio(k)
        amp = 34 * (1 - k) + 2; ph = i * 1.3 + t * 2.2 * (1 - k)
        P = [(cx - w / 2 + j * w / 24, y0 + amp * math.sin(j * 0.9 + ph)) for j in range(25)]
        A = np.array(P, np.int32)
        cv2.polylines(f, [A], False, C(INKC), 13, cv2.LINE_AA)
        cv2.polylines(f, [A], False, C((246, 236, 214) if k < 0.6 else (226, 218, 200)), 7, cv2.LINE_AA)
    if water:
        rng = np.random.default_rng(3)
        for i in range(14):
            xi = cx + rng.uniform(-w / 2.3, w / 2.3); yi = cy + rng.uniform(-h / 2.2, h / 2.2)
            side = -1 if xi < cx else 1
            xo = cx + side * (w / 2 + 50 + rng.uniform(0, 60)); yo = cy + rng.uniform(-h / 3, h / 3)
            x = xi + (xo - xi) * eio(k); y = yi + (yo - yi) * eio(k)
            r_ = 13
            cv2.circle(f, (int(x), int(y)), r_ + 3, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), r_, C((120, 180, 236)), -1, cv2.LINE_AA)
            cv2.circle(f, (int(x - 4), int(y - 4)), 4, C((240, 250, 255)), -1, cv2.LINE_AA)


def dish_el(seed=1):
    """a WIDE, shallow ink dish with a thin layer of rice spread out (cools fast)."""
    def mk():
        w, h = 520, 170; im, d, S = _cv(w, h)
        d.ellipse(S(30, 30, 490, 110), fill=RICE_H + (255,))
        grains(d, S, 260, 70, 210, 30, 55, seed + 3)
        dish = [(10, 80), (510, 80), (470, 150), (50, 150)]
        _ink_poly(d, dish, BLUE_L, seed + 4, INK_W - 1, amp=1.4)
        _hatch_in(im, (380, 80, 510, 150), lambda q, S_: q.polygon(S_(400, 84, 506, 84, 470, 148, 420, 148), fill=255), -40, 9, 36)
        d.line([(x * SC3, y * SC3) for x, y in _wob([(14, 82), (506, 82)], 1.0, seed + 5)], fill=BLUE + (255,), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("dish20", seed), mk)


def bin_ink_el(open_=0.0, seed=1):
    """a kitchen pedal bin in ink; open_ 0..1 lifts the lid."""
    open_ = round(clamp(open_) * 4) / 4
    def mk():
        w, h = 260, 340; im, d, S = _cv(w, h)
        body = [(40, 110), (220, 110), (206, 320), (54, 320)]
        _ink_poly(d, body, (150, 160, 170), seed + 1, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.rectangle(S_(160, 100, 230, 330), fill=c), (100, 108, 120), 140)
        for x0 in (90, 130, 170): d.line(S(x0, 140, x0 - 2, 290), fill=INKC + (120,), width=3 * SC3)
        a = math.radians(-70 * open_)
        lid = [(40, 110), (220, 110), (220, 92), (40, 92)]
        lid = [(40 + (x - 40) * math.cos(a) - (y - 110) * math.sin(a), 110 + (x - 40) * math.sin(a) + (y - 110) * math.cos(a)) for x, y in lid]
        _ink_poly(d, lid, (120, 130, 140), seed + 2, INK_W - 1, amp=0.8)
        _ink_poly(d, [(100, 320), (160, 320), (160, 332), (100, 332)], (90, 96, 104), seed + 3, 3, amp=0.4)
        return _done(im, w, h)
    return gcache(("bin20", open_, seed), mk)


def clock_ink_el(r=110, seed=1):
    """a round ink wall clock face (hands are drawn live with clock_hands)."""
    def mk():
        w = h = 2 * r + 30; im, d, S = _cv(w, h); c = w / 2
        _ink_ell(d, c, c, r, r, (250, 246, 236), seed + 1, INK_W, n=30, amp=1.2)
        for i in range(12):
            a = math.radians(i * 30); L = 16 if i % 3 == 0 else 8
            d.line(S(c + (r - 12) * math.cos(a), c + (r - 12) * math.sin(a), c + (r - 12 - L) * math.cos(a), c + (r - 12 - L) * math.sin(a)), fill=INKC + (255,), width=(5 if i % 3 == 0 else 3) * SC3)
        return _done(im, w, h)
    return gcache(("clock20", r, seed), mk)


def clock_hands(f, x, y, hours, r=110, s=1.0):
    """live hands on clock_ink_el at (x, y): hours as a float (23.5 = 11:30 pm)."""
    for frac, L, th in ((hours / 12.0, 0.5, 9), ((hours % 1.0), 0.78, 6)):
        a = math.radians(-90 + 360 * frac)
        cv2.line(f, (int(x), int(y)), (int(x + r * s * L * math.cos(a)), int(y + r * s * L * math.sin(a))), C(INKC), int(th * s), cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(8 * s), C(ACC), -1, cv2.LINE_AA)


def set_stove_night(t=0.0, lamp=1.0, hob_y=1300):
    """NEW PLACE (ep 20): the stove after dinner — flames off, kitchen lights off, a cold moonlit window, ONE warm under-cabinet lamp
    pooling on the pot (the 'warm hours' lighting beat). Pot goes at (540, hob_y - 10) like set_stove."""
    f = set_stove(t, blur=4, hob_y=hob_y, on=0.0)
    f *= np.array([0.42, 0.46, 0.62], np.float32)                                                           # night: dark + cool
    f[450:880, 720:1020] = f[450:880, 720:1020] * 0.35 + np.array(C((60, 80, 130)), np.float32) * 0.65      # moonlit window
    cv2.circle(f, (930, 540), 34, C((236, 240, 250)), -1, cv2.LINE_AA); glow(f, 930, 540, 120, (190, 210, 255), 0.35)
    cv2.rectangle(f, (300, 560), (780, 600), C((60, 44, 34)), -1, cv2.LINE_AA)                              # cabinet with the lamp
    cv2.rectangle(f, (380, 598), (700, 610), C((255, 220, 160)), -1, cv2.LINE_AA)
    if lamp > 0:
        glow(f, 540, 1080, 520, (255, 190, 110), 0.55 * lamp)
        god_rays(f, 540, 610, t, (255, 206, 140), 0.18 * lamp, 7, 900, 0.5, math.pi / 2, 4)
    return f
