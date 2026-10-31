# ================= anim_props6.py — FreshNestHub 18 "why does milk boil over?" ink props (lib17 toolkit: _ink_poly / _ink_ell / _shade /
# _hatch_in / _face). ONE accent per video: AMBER = heat, the proteins, the 'jacket', the skin (the cause); MINT = the fixes (wide pot,
# stir, soap drop); milk = paper white; water = a pale wash. Props: pot_el (cut-away pot: milk level, foam dome, skin, overflow; kinds steel
# / wide / water / pasta), bubble_el (steam bubble with an optional protein 'jacket' + face), protein_el, fat_el, soap_el / soap_drop_el,
# spoon_el, butter_el, pop_star (a burst bubble), rim_drips. =================
ACC = (232, 148, 40); ACC_S = (176, 100, 18); ACC_L = (250, 206, 120); ACC_XL = (252, 236, 200)      # amber accent (overrides lib17's violet)
MILK = (252, 248, 238); MILK_S = (228, 216, 192)
WATER = (206, 228, 236); WATER_S = (170, 198, 210)
STEEL = (168, 170, 178); STEEL_S = (116, 118, 128); STEEL_H = (226, 228, 232)
SCHEMES["amber"] = ((214, 126, 30), (250, 196, 110), (200, 112, 24), (0.7, 0.42, 0.1))
SCHEMES["cream2"] = ((240, 228, 206), (252, 246, 232), (232, 218, 192), (0.78, 0.72, 0.6))
SCHEMES["steelb"] = ((70, 80, 100), (140, 156, 180), (60, 70, 90), (0.3, 0.35, 0.45))
SCHEMES["mintd"] = ((40, 120, 96), (110, 196, 160), (36, 110, 86), (0.2, 0.5, 0.4))


def _foam_bubbles(d, S, x0, x1, y_top, y_bot, seed=5, rmin=9, rmax=22, col=MILK, alpha=255, edge=None):
    """pack ink bubbles (paper fill + ink ring + a glint) into a box; edge = function(y) -> (xl, xr) allowed span at that y."""
    rng = np.random.default_rng(seed)
    for k in range(130):
        r_ = rng.uniform(rmin, rmax); y = rng.uniform(y_top + r_, y_bot - r_ * 0.3) if y_bot - r_ * 0.3 > y_top + r_ else y_top + r_
        xl, xr = edge(y) if edge else (x0, x1)
        if xr - xl < 2 * r_: continue
        x = rng.uniform(xl + r_, xr - r_)
        d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=tuple(col) + (alpha,), outline=INKC + (255,), width=max(1, int(2.6 * SC3)))
        d.ellipse(S(x - r_ * 0.55, y - r_ * 0.6, x - r_ * 0.2, y - r_ * 0.25), fill=(255, 255, 255, 230))


def pot_el(kind="steel", level=0.55, foam=0.0, skin=0.0, spill=None, seed=5):
    """CUT-AWAY pot seen from the front (we see the liquid): kind = steel (tall milk pot) | wide (big wide pan) | water | pasta.
    level = liquid height 0..1; foam = height of the bubble dome 0..1 (1 = well over the rim); skin = amber skin on the surface 0..1;
    spill (None = auto from foam) = foam running down the outside 0..1. Returns an element whose centre is the pot's middle."""
    level = round(clamp(level) * 20) / 20; foam = round(clamp(foam) * 20) / 20; skin = round(clamp(skin) * 4) / 4
    spill = clamp((foam - 0.72) / 0.28) if spill is None else round(clamp(spill) * 4) / 4
    spill = round(spill * 4) / 4
    def mk():
        wide = kind == "wide"
        w, h = (720, 330) if wide else (470, 450); im, d, S = _cv(w, h)
        x0, x1, yr, yb = (70, 650, 86, 290) if wide else (96, 374, 118, 408)                    # interior box (rim y, bottom y)
        flare = 10 if wide else 16
        liq = WATER if kind in ("water", "pasta") else MILK; liq_s = WATER_S if kind in ("water", "pasta") else MILK_S
        # pot body (steel, cut-away: the inside is drawn as a lighter panel)
        body = [(x0 - 26 - flare, yr - 8), (x1 + 26 + flare, yr - 8), (x1 + 26, yb + 16), (x0 - 26, yb + 16)]
        _ink_poly(d, body, STEEL, seed + 1, INK_W, amp=1.8)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255),
               lambda q, S_, c: q.polygon(S_(x1 - 40, yr - 20, x1 + 60, yr - 20, x1 + 60, yb + 30, x1 - 60, yb + 30), fill=c), STEEL_S, 120)
        _hatch_in(im, (x1 - 60, yr, x1 + 40, yb + 16), lambda q, S_: q.polygon(S_(x1 - 30, yr, x1 + 24, yr, x1 + 20, yb + 12, x1 - 36, yb + 12), fill=255), -40, 10, 34)
        inner = [(x0 - flare, yr), (x1 + flare, yr), (x1, yb), (x0, yb)]
        d.polygon([(x * SC3, y * SC3) for x, y in inner], fill=(196, 198, 206, 255))
        d.polygon([(x * SC3, y * SC3) for x, y in [(x0 - flare, yr), (x0 + 30, yr), (x0 + 34, yb), (x0, yb)]], fill=(176, 178, 188, 255))
        # liquid
        ym = yb - (yb - yr - 10) * level
        def span(y):
            k = clamp((y - yr) / max(1, yb - yr)); return x0 - flare * (1 - k), x1 + flare * (1 - k)
        xl, xr = span(ym)
        d.polygon([(x * SC3, y * SC3) for x, y in [(xl, ym), (xr, ym), (x1, yb), (x0, yb)]], fill=tuple(liq) + (255,))
        _hatch_in(im, (x1 - 90, ym, x1, yb), lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in [(xr - 70, ym), (xr, ym), (x1, yb), (x1 - 70, yb)]], fill=255), -40, 9, 26)
        if kind == "pasta":
            for k in range(7):
                xa = x0 + 30 + k * 40; d.line([(xa * SC3, (ym + 10) * SC3), ((xa + 18) * SC3, (ym + 60) * SC3), ((xa - 8) * SC3, (yb - 10) * SC3)], fill=CARA + (255,), width=5 * SC3, joint="curve")
                d.line([(xa * SC3, (ym + 10) * SC3), ((xa + 18) * SC3, (ym + 60) * SC3), ((xa - 8) * SC3, (yb - 10) * SC3)], fill=INKC + (160,), width=2 * SC3, joint="curve")
        # small steam bubbles forming at the bottom
        rng = np.random.default_rng(seed + 7)
        for k in range(6):
            bx = rng.uniform(x0 + 20, x1 - 20); by = yb - rng.uniform(12, 40); r_ = rng.uniform(5, 9)
            d.ellipse(S(bx - r_, by - r_, bx + r_, by + r_), fill=(255, 255, 255, 230), outline=INKC + (200,), width=2 * SC3)
        d.line([(x * SC3, y * SC3) for x, y in _wob([(xl, ym), (xr, ym)], 1.2, seed + 3)], fill=INKC + (255,), width=4 * SC3)
        # rim lip (under the foam), then the foam dome: bubbles from the surface up to y_top; above the rim they widen and spill
        _ink_poly(d, [(x0 - 30 - flare, yr - 14), (x1 + 30 + flare, yr - 14), (x1 + 30 + flare, yr - 2), (x0 - 30 - flare, yr - 2)], STEEL_H, seed + 2, INK_W - 1, amp=1.2)
        if foam > 0:
            y_top = ym - foam * (ym - (10 if not wide else 6))
            def edge(y):
                if y >= yr: return span(y)
                over = clamp((yr - y) / 60) * (40 if not wide else 30)
                return x0 - flare - over, x1 + flare + over
            fcol = ACC_XL if kind == "pasta" else MILK
            _foam_bubbles(d, S, x0, x1, y_top, ym + 6, seed + 11, 12 if wide else 13, 26 if wide else 32, fcol, 255, edge)
            if spill > 0:                                                                            # foam running down the outside
                for sgn, xs in ((-1, x0 - 26), (1, x1 + 26)):
                    L_ = spill * (yb - yr) * 0.9
                    pts = [(xs + sgn * (6 + 8 * math.sin(k * 1.3)), yr - 8 + L_ * k / 6) for k in range(7)]
                    d.line([(x * SC3, y * SC3) for x, y in pts], fill=MILK + (255,), width=22 * SC3, joint="curve")
                    d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (255,), width=3 * SC3, joint="curve")
                    d.ellipse(S(pts[-1][0] - 14, pts[-1][1] - 10, pts[-1][0] + 14, pts[-1][1] + 14), fill=MILK + (255,), outline=INKC + (255,), width=3 * SC3)
        # skin: an amber wrinkly layer on the surface (or on top of the foam)
        if skin > 0:
            ys = ym if foam <= 0 else ym - foam * (ym - (10 if not wide else 6))
            xa, xb = (span(ys) if ys >= yr else (x0 - flare - 30, x1 + flare + 30))
            pts = [(xa + (xb - xa) * k / 26, ys - 6 - 7 * skin * math.sin(k * 1.7) - 3 * math.sin(k * 0.7)) for k in range(27)]
            d.polygon([(x * SC3, y * SC3) for x, y in pts + [(xb, ys + 14), (xa, ys + 14)]], fill=ACC_L + (int(120 + 120 * skin),))
            d.line([(x * SC3, y * SC3) for x, y in pts], fill=ACC_S + (255,), width=int((3 + 3 * skin) * SC3), joint="curve")
            for k in range(2, 26, 4): d.line(S(pts[k][0], pts[k][1] + 3, pts[k][0] + 6, pts[k][1] + 10), fill=ACC_S + (170,), width=2 * SC3)
        # handles
        for sgn, xs in ((-1, x0 - 30 - flare), (1, x1 + 30 + flare)):
            hp = [(xs, yr + 20), (xs + sgn * 44, yr + 10), (xs + sgn * 44, yr + 54), (xs, yr + 64)]
            d.line([(x * SC3, y * SC3) for x, y in _wob(hp, 1.2, seed + 20 + sgn)], fill=INKC + (255,), width=12 * SC3, joint="curve")
            d.line([(x * SC3, y * SC3) for x, y in _wob(hp, 1.2, seed + 20 + sgn)], fill=STEEL_S + (255,), width=6 * SC3, joint="curve")
        d.line(S(x0 - 10, yr + 30, x0 - 4, yb - 30), fill=(255, 255, 255, 170), width=5 * SC3)       # steel glint on the cut edge
        return _done(im, w, h)
    return gcache(("pot18", kind, level, foam, skin, spill, seed), mk)


def bubble_el(r=60, jacket=0.0, mood=None, look=(0, 0), seed=1, col=MILK):
    """a steam bubble (paper fill, ink ring, glint). jacket 0..1 = amber protein beads wrapped around it (the 'jacket')."""
    jacket = round(clamp(jacket) * 4) / 4
    def mk():
        w = h = int(2 * r + 60); im, d, S = _cv(w, h); cx = cy = w / 2
        _ink_ell(d, cx, cy, r, r, col, seed, INK_W - 1, n=32, amp=1.4)
        d.ellipse(S(cx - r * 0.6, cy - r * 0.65, cx - r * 0.2, cy - r * 0.25), fill=(255, 255, 255, 240))
        d.arc(S(cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8), 20, 110, fill=INKC + (90,), width=int(2 * SC3))
        if jacket > 0:
            n_ = int(14 * jacket) + 2; rng = np.random.default_rng(seed)
            for k in range(n_):
                a = k * 2 * math.pi / max(1, n_) + rng.uniform(-0.1, 0.1); br = 9 + rng.uniform(-1, 2)
                px, py = cx + (r + 2) * math.cos(a), cy + (r + 2) * math.sin(a)
                d.ellipse(S(px - br, py - br, px + br, py + br), fill=ACC + (255,), outline=INKC + (255,), width=int(2.4 * SC3))
                d.ellipse(S(px - br * 0.45, py - br * 0.5, px - br * 0.1, py - br * 0.15), fill=(255, 255, 255, 200))
        if mood: _face(d, S, cx, cy + 4, max(0.6, r / 60), mood, look)
        return _done(im, w, h)
    return gcache(("bubble18", r, jacket, mood, look, seed, col), mk)


def protein_el(mood="n", look=(0, 0), seed=1):
    """a protein bead (amber) with a face: 'loves sitting on the edge of a bubble'."""
    def mk():
        w, h = 110, 110; im, d, S = _cv(w, h)
        _ink_ell(d, 55, 56, 40, 38, ACC, seed + 30, INK_W - 1, n=24, amp=2.0)
        _shade(im, lambda q, S_: q.ellipse(S_(15, 18, 95, 94), fill=255), lambda q, S_, c: q.ellipse(S_(50, 30, 110, 110), fill=c), ACC_S, 90)
        _hatch_in(im, (60, 40, 95, 94), lambda q, S_: q.ellipse(S_(50, 30, 96, 96), fill=255), -40, 7, 30)
        d.ellipse(S(30, 30, 44, 42), fill=(255, 255, 255, 210))
        _face(d, S, 55, 58, 0.85, mood, look)
        return _done(im, w, h)
    return gcache(("protein18", mood, look, seed), mk)


def fat_el(seed=2):
    """a fat droplet (pale amber, round) — the other thing that thickens the skin."""
    def mk():
        w, h = 90, 90; im, d, S = _cv(w, h)
        _ink_ell(d, 45, 46, 30, 28, ACC_L, seed + 40, INK_W - 2, n=20, amp=1.6)
        d.ellipse(S(28, 26, 40, 36), fill=(255, 255, 255, 220))
        return _done(im, w, h)
    return gcache(("fat18", seed), mk)


def sugar_cube_el():
    def mk():
        w, h = 90, 90; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 34), (60, 34), (74, 22), (74, 62), (60, 74), (20, 74)], MILK, 44, INK_W - 2)
        d.line(S(60, 34, 60, 74), fill=INKC + (255,), width=3 * SC3); d.line(S(60, 34, 74, 22), fill=INKC + (255,), width=3 * SC3)
        for k in range(8): d.ellipse(S(26 + (k * 13) % 30, 40 + (k * 9) % 28, 29 + (k * 13) % 30, 43 + (k * 9) % 28), fill=INKC + (70,))
        return _done(im, w, h)
    return gcache("sugar18", mk)


def soap_el():
    """a dish-soap bottle (mint) with a pump top."""
    def mk():
        w, h = 160, 300; im, d, S = _cv(w, h)
        d.line(S(80, 60, 80, 20), fill=INKC + (255,), width=10 * SC3); d.line(S(80, 24, 118, 24), fill=INKC + (255,), width=10 * SC3)
        d.line(S(80, 60, 80, 20), fill=INK_MINT_S + (255,), width=5 * SC3); d.line(S(80, 24, 118, 24), fill=INK_MINT_S + (255,), width=5 * SC3)
        _ink_poly(d, [(56, 60), (104, 60), (104, 90), (124, 110), (124, 276), (36, 276), (36, 110), (56, 90)], INK_MINT, 51, INK_W - 1)
        _shade(im, lambda q, S_: q.polygon(S_(56, 60, 104, 60, 104, 90, 124, 110, 124, 276, 36, 276, 36, 110, 56, 90), fill=255),
               lambda q, S_, c: q.rectangle(S_(92, 60, 130, 280), fill=c), INK_MINT_S, 110)
        _hatch_in(im, (96, 110, 124, 276), lambda q, S_: q.rectangle(S_(100, 112, 122, 274), fill=255), -40, 8, 34)
        d.rounded_rectangle(S(50, 150, 110, 210), 6 * SC3, fill=MILK + (255,), outline=INKC + (255,), width=3 * SC3)
        d.text((80 * SC3, 180 * SC3), "SOAP", font=font(F_BLACK, 20 * SC3), fill=INKC + (255,), anchor="mm")
        d.line(S(46, 120, 44, 260), fill=(255, 255, 255, 200), width=5 * SC3)
        return _done(im, w, h)
    return gcache("soap18", mk)


def soap_drop_el():
    def mk():
        w, h = 70, 90; im, d, S = _cv(w, h)
        pts = [(35, 8), (54, 44), (58, 62), (46, 82), (35, 86), (24, 82), (12, 62), (16, 44)]
        _ink_poly(d, pts, INK_MINT, 52, INK_W - 2, amp=1.0)
        d.ellipse(S(22, 46, 30, 56), fill=(255, 255, 255, 210))
        return _done(im, w, h)
    return gcache("soapdrop18", mk)


def spoon_el():
    """a long wooden spoon (ink): handle along +x, bowl at the right end; element centre = middle of the handle."""
    def mk():
        w, h = 460, 110; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 44), (330, 40), (330, 70), (14, 66)], CARA, 61, INK_W - 1)
        _ink_ell(d, 390, 55, 64, 40, CARA, 62, INK_W - 1, n=24, amp=1.4)
        _ink_ell(d, 396, 55, 44, 24, CARA_S, 63, INK_W - 3, n=20, amp=1.0)
        _hatch_in(im, (330, 30, 460, 90), lambda q, S_: q.ellipse(S_(360, 60, 456, 96), fill=255), -40, 8, 30)
        d.line(S(30, 50, 300, 48), fill=(255, 255, 255, 120), width=3 * SC3)
        return _done(im, w, h)
    return gcache("spoon18", mk)


def butter_el():
    def mk():
        w, h = 160, 110; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 40), (110, 40), (140, 22), (140, 80), (110, 96), (20, 96)], ACC_L, 71, INK_W - 1)
        d.line(S(110, 40, 110, 96), fill=INKC + (255,), width=3 * SC3); d.line(S(110, 40, 140, 22), fill=INKC + (255,), width=3 * SC3)
        _shade(im, lambda q, S_: q.polygon(S_(110, 40, 140, 22, 140, 80, 110, 96), fill=255), lambda q, S_, c: q.rectangle(S_(100, 10, 160, 110), fill=c), ACC_S, 90)
        d.text((65 * SC3, 68 * SC3), "BUTTER", font=font(F_BLACK, 16 * SC3), fill=INKC + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache("butter18", mk)


def pop_star(f, x, y, t, t0, r=40, col=INKC, dur=0.3):
    """a burst bubble: 6 short ink dashes flying out + a fading ring (the 'pop')."""
    q = t - t0
    if q < 0 or q > dur: return
    k = q / dur
    for i in range(6):
        a = i * math.pi / 3 + 0.3; r0 = r * (0.5 + 0.9 * eo(k)); r1 = r0 + 14 * (1 - k)
        cv2.line(f, (int(x + r0 * math.cos(a)), int(y + r0 * math.sin(a))), (int(x + r1 * math.cos(a)), int(y + r1 * math.sin(a))), C(col), 5, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(r * 0.4 * (1 + k)), C(col), max(1, int(4 * (1 - k))), cv2.LINE_AA)


def rising_bubbles(f, x, y_bot, y_top, t, w=200, n=7, r=14, speed=160, seed=3, pop_at=None, jacket=0.0, col=MILK):
    """steam bubbles rising from y_bot to y_top; pop_at = y where they burst (water) or None (they stack). Returns the list of (x, y, alive)."""
    rng = np.random.default_rng(seed); out = []
    for i in range(n):
        ph = (t * speed / max(1, (y_bot - y_top)) + rng.uniform(0, 1)) % 1.0
        bx = x + rng.uniform(-w / 2, w / 2) + 8 * math.sin(t * 4 + i); by = y_bot - (y_bot - y_top) * ph
        rr = r * rng.uniform(0.7, 1.3)
        if pop_at is not None and by < pop_at:
            k = clamp((pop_at - by) / 30)
            if k < 1: pop_star(f, bx, pop_at, t, t - k * 0.3 + 0.0, rr * 1.4, INKC, 0.3)
            continue
        comp(f, scale_el(bubble_el(40, jacket, None, (0, 0), 1 + i % 3, col), rr / 40), bx, by)
        out.append((bx, by))
    return out


def pot_geom(cx, cy, s, kind="steel", level=0.55):
    """interior box of pot_el drawn at (cx, cy, scale s): returns dict(xl, xr, y_rim, y_bot, y_surf, w, h)."""
    wide = kind == "wide"
    w, h = (720, 330) if wide else (470, 450)
    x0, x1, yr, yb = (70, 650, 86, 290) if wide else (96, 374, 118, 408)
    ym = yb - (yb - yr - 10) * clamp(level)
    X = lambda x: cx + (x - w / 2) * s; Y = lambda y: cy + (y - h / 2) * s
    return dict(xl=X(x0), xr=X(x1), y_rim=Y(yr), y_bot=Y(yb), y_surf=Y(ym), w=w * s, h=h * s, top=Y(0), bottom=Y(h))


def side_flames(f, x, y, t, pot_w, on=1.0, n=4, w=90):
    """flames licking up BOTH sides of a pot that sits on the burner (draw AFTER the pot)."""
    flames(f, x - pot_w / 2 - 20, y, t, w, n, on); flames(f, x + pot_w / 2 + 20, y, t, w, n, on)


def steam_wisps(f, x, y, t, n=4, h=160, w=120, col=(255, 255, 255), op=0.8, seed=2):
    """soft steam curls rising from (x, y) (evaporation off the top)."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        ph = (t * 0.45 + rng.uniform(0, 1)) % 1.0
        px = x + rng.uniform(-w / 2, w / 2) + 18 * math.sin(t * 2 + i * 2); py = y - h * ph
        r_ = 10 + 16 * ph; a_ = op * (1 - ph) * 0.8
        ov = f.copy(); cv2.circle(ov, (int(px), int(py)), int(r_), C(col), -1, cv2.LINE_AA); f[:] = f * (1 - a_) + ov * a_
        cv2.circle(f, (int(px), int(py)), int(r_), C(INKC), 2, cv2.LINE_AA) if ph < 0.6 else None


def spoon_at(f, gx, gy, ang, s=1.0, op=1.0):
    """draw the spoon so the END of its handle sits at (gx, gy); ang = degrees CCW (0 = bowl pointing right). Draw the grip hand after it."""
    dx = (230 - 34) * s; dy = 0.0; a = math.radians(ang)
    cx = gx + dx * math.cos(a) + dy * math.sin(a); cy = gy - dx * math.sin(a) + dy * math.cos(a)
    rot_comp(f, scale_el(spoon_el(), s), cx, cy, ang, 1.0, op, 0.25)
