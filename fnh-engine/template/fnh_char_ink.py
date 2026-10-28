# ================= Chubby "INK" — hand-drawn line-art character (owner reference 28 Oct: round-head ink cartoon people) =================
# Original design in that language: a round head drawn with one wobbly ink line, scribble hair, dot eyes + brow strokes + a mouth
# curve that do all the acting, an outlined hoodie + chef's apron, thin ink limbs with small hands, big sneakers. Lines are warm
# ink (not pure black) with a hand-drawn wobble that is FIXED per element (no boiling between frames).
# Colour: INK_MODE = "mono" (ink on paper + the mint accent only), "flat" (ink + flat fills), "wash" (ink + flat fills + a soft
# shadow side + hatching + paper texture). Same chub() API as v2/v3; loaded after them, overrides them.
INK_MODE = "wash"
INKC = (46, 32, 26)                                  # warm ink
PAPER = (247, 241, 228)
INK_SKIN = (250, 222, 196); INK_SKIN_S = (226, 184, 152)
INK_MINT = (72, 190, 150); INK_MINT_S = (38, 142, 108)
INK_APRON = (252, 247, 236); INK_APRON_S = (214, 202, 180)
INK_JEAN = (92, 118, 160); INK_JEAN_S = (60, 82, 122)
INK_HAIR = (58, 40, 30)
INK_W = 7                                            # ink line width at s = 1 (px)


def _wob(pts, amp=1.6, seed=0, n=1):
    """add a fixed hand-drawn wobble to a polyline (deterministic per seed)."""
    rng = np.random.default_rng(seed); out = []
    for k, (x, y) in enumerate(pts):
        out.append((x + rng.uniform(-amp, amp), y + rng.uniform(-amp, amp)))
    return out


def _arcpts(cx, cy, rx, ry, a0, a1, n=24):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _ink_line(f, pts, w, col=INKC, seed=0, amp=1.4):
    P = _wob(pts, amp, seed)
    cv2.polylines(f, [np.array(P, np.int32)], False, C(col), max(1, int(w)), cv2.LINE_AA)


def _hatch(im, S, box, ang=-35, gap=7, col=(0, 0, 0, 60), w=2):
    """diagonal hatching inside a PIL box (x0, y0, x1, y1) through a mask drawn by box[4] (a function)."""
    x0, y0, x1, y1, fn = box
    m = Image.new("L", im.size, 0); fn(ImageDraw.Draw(m))
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(-60, 60):
        xa = x0 + k * gap; d.line(S(xa, y1, xa + (y1 - y0) * math.tan(math.radians(-ang)), y0), fill=col, width=w * 3)
    im.alpha_composite(Image.composite(lay, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))


def _fillcol(c): return c if INK_MODE != "mono" else PAPER


def chub_head_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n", tint=0.0, nose=None, cap=False):
    tint = round(clamp(tint) * 10) / 10
    key = ("chead_ink", INK_MODE, mouth, blink, brow, lx, ly, expr, tint, nose, cap)
    if key in _gc: return _gc[key]
    W_, H_, sc = 240, 250, 3
    im = Image.new("RGBA", (W_ * sc, H_ * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
    cx, cy, R = 120, 132, 92
    skin = _mix3(INK_SKIN, (255, 160, 70), tint) if INK_MODE != "mono" else PAPER
    skin_s = _mix3(INK_SKIN_S, (220, 120, 40), tint)
    wob = lambda pts, amp=1.6, seed=0: [(x * sc, y * sc) for x, y in _wob(pts, amp, seed)]
    # head: fill, soft shadow side, then one wobbly ink outline
    d.ellipse(S(cx - R, cy - R + 4, cx + R, cy + R - 4), fill=skin + (255,))
    if INK_MODE == "wash":
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse(S(cx - R + 26, cy - R + 30, cx + R + 6, cy + R + 2), fill=skin_s + (120,))
        m = Image.new("L", im.size, 0); ImageDraw.Draw(m).ellipse(S(cx - R, cy - R + 4, cx + R, cy + R - 4), fill=255)
        im.alpha_composite(Image.composite(sh, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
        _hatch(im, S, (cx + 30, cy - 20, cx + R, cy + R, lambda q: q.pieslice(S(cx - R, cy - R + 4, cx + R, cy + R - 4), -40, 110, fill=255)), -40, 9, INKC + (34,), 1)
    d.line(wob(_arcpts(cx, cy, R, R - 4, -90, 270, 40), 2.0, 1), fill=INKC + (255,), width=INK_W * sc, joint="curve")
    # ears
    for sgn in (-1, 1):
        ex = cx + sgn * (R + 4)
        d.ellipse(S(ex - 13, cy - 12, ex + 13, cy + 18), fill=skin + (255,), outline=INKC + (255,), width=INK_W * sc - 3)
    # hair: a scribble of loops along the top (fixed seed), drawn as thick ink
    rng = np.random.default_rng(3)
    for k in range(26):
        a = -160 + k * 5.4; r0 = R - 6 + rng.uniform(-4, 8); lp = rng.uniform(12, 24)
        px, py = cx + r0 * math.cos(math.radians(a)), cy - 8 + r0 * math.sin(math.radians(a))
        d.ellipse(S(px - lp / 2, py - lp / 2 - 8, px + lp / 2, py + lp / 2 - 8), outline=INK_HAIR + (255,), width=4 * sc)
    for k in range(10):
        a = -150 + k * 13; r0 = R - 20 + rng.uniform(-6, 6)
        px, py = cx + r0 * math.cos(math.radians(a)), cy - 10 + r0 * math.sin(math.radians(a))
        d.line(S(px, py, px + rng.uniform(-10, 10), py - rng.uniform(10, 24)), fill=INK_HAIR + (255,), width=4 * sc)
    d.chord(S(cx - R + 8, cy - R + 2, cx + R - 8, cy + 6), 190, 350, fill=INK_HAIR + (255,))         # solid cap under the scribble
    for k in range(3): d.line(S(cx + 12 + k * 10, cy - R - 4, cx + 20 + k * 12, cy - R - 22 + k * 4), fill=INK_HAIR + (255,), width=4 * sc)   # cowlick
    # eyes: ink dots with a little white glint; expression changes shape
    ox, oy = lx * 6, ly * 5; ey = 134
    for i, sgn in enumerate((-1, 1)):
        ex = cx + sgn * 36
        if blink or (expr == "happy" and mouth == 3):
            d.line(wob(_arcpts(ex, ey + 2, 16, 10, 200, 340, 10), 1.0, 7 + i), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve"); continue
        if expr == "wow":
            d.ellipse(S(ex - 17, ey - 19, ex + 17, ey + 19), fill=(255, 255, 255, 255), outline=INKC + (255,), width=5 * sc)
            d.ellipse(S(ex + ox - 7, ey + oy - 7, ex + ox + 7, ey + oy + 7), fill=INKC + (255,))
        elif expr == "happy":
            d.line(wob(_arcpts(ex, ey + 6, 15, 12, 200, 340, 10), 1.0, 9 + i), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
        else:
            r_ = 11
            d.ellipse(S(ex + ox - r_, ey + oy - r_, ex + ox + r_, ey + oy + r_), fill=INKC + (255,))
            d.ellipse(S(ex + ox - r_ + 3, ey + oy - r_ + 3, ex + ox - r_ + 8, ey + oy - r_ + 8), fill=(255, 255, 255, 255))
            if expr in ("sus", "sleepy", "smirk") and not (expr == "smirk" and i == 1):
                cov = {"sus": 0.45, "sleepy": 0.65, "smirk": 0.4}[expr]
                d.rectangle(S(ex - 16, ey - 16, ex + 16, ey - 16 + 32 * cov), fill=skin + (255,))
                d.line(S(ex - 15, ey - 16 + 32 * cov, ex + 15, ey - 16 + 32 * cov), fill=INKC + (255,), width=5 * sc)
            if expr == "sad":
                d.polygon(S(ex - 16, ey - 18, ex + 16, ey - 18, ex + 16, ey - 18 + (14 if sgn > 0 else 2), ex - 16, ey - 18 + (2 if sgn > 0 else 14)), fill=skin + (255,))
                d.line(S(ex - 15, ey - 18 + (2 if sgn > 0 else 14), ex + 15, ey - 18 + (14 if sgn > 0 else 2)), fill=INKC + (255,), width=5 * sc)
    # brows: single ink strokes, the angle is the emotion
    by = 104
    for i, sgn in enumerate((-1, 1)):
        ex = cx + sgn * 36; inn, out = ex - sgn * 18, ex + sgn * 18
        if brow == "up": yi, yo = by - 10, by - 2
        elif brow == "sus": yi, yo = by + 4, by - 6
        elif brow == "sad": yi, yo = by - 8, by + 4
        else: yi, yo = by, by - 2
        if expr == "smirk": yi, yo = (by - 12, by - 6) if i == 1 else (by + 3, by)
        if expr == "wow": yi, yo = yi - 10, yo - 10
        d.line(wob([(inn, yi), ((inn + out) / 2, (yi + yo) / 2 - 3), (out, yo)], 1.2, 20 + i), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
    # nose: one small hook stroke
    d.line(wob([(cx + 2, 150), (cx + 8, 166), (cx - 2, 170)], 0.8, 31), fill=INKC + (255,), width=(INK_W - 2) * sc, joint="curve")
    # cheeks (colour modes only)
    if INK_MODE != "mono":
        for sgn in (-1, 1): d.ellipse(S(cx + sgn * 56 - 14, 160, cx + sgn * 56 + 14, 176), fill=(240, 130, 120, 70))
    if cap:
        d.chord(S(cx - R - 2, cy - R - 2, cx + R + 2, cy + 8), 180, 360, fill=_fillcol((130, 80, 46)) + (255,), outline=INKC + (255,), width=5 * sc)
    # mouth
    mx, my = cx, 196
    if expr == "wow" and mouth == 0: mouth = "o"
    dark = _fillcol((110, 40, 46))
    if mouth == 0:
        if expr == "sad": d.line(wob(_arcpts(mx, my + 12, 20, 12, 200, 340, 12), 1.0, 40), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
        elif expr == "smirk": d.line(wob(_arcpts(mx - 4, my - 6, 22, 12, 10, 110, 10), 1.0, 41), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
        elif expr == "happy":
            d.chord(S(mx - 30, my - 20, mx + 30, my + 18), 0, 180, fill=dark + (255,), outline=INKC + (255,), width=5 * sc)
            d.rectangle(S(mx - 22, my - 1, mx + 22, my + 6), fill=(255, 255, 255, 255))
        else: d.line(wob(_arcpts(mx, my - 8, 20, 12, 20, 160, 12), 1.0, 42), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
    elif mouth == "o":
        d.ellipse(S(mx - 12, my - 10, mx + 12, my + 16), fill=dark + (255,), outline=INKC + (255,), width=5 * sc)
    else:
        hh = {1: 9, 2: 16, 3: 23}[mouth]; ww = {1: 17, 2: 22, 3: 26}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 7, mx + ww, my - 7 + hh * 1.5), int(hh * 0.7) * sc, fill=dark + (255,), outline=INKC + (255,), width=5 * sc)
        d.rectangle(S(mx - ww + 5, my - 6, mx + ww - 5, my), fill=(255, 255, 255, 255))
    el = _done(im, W_, H_)
    if len(_gc) < 900: _gc[key] = el
    return el


def chub_body_el(shirt=HOOD3, logo=True):
    def mk():
        W_, H_, sc = 300, 290, 3
        im = Image.new("RGBA", (W_ * sc, H_ * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
        wob = lambda pts, amp=1.6, seed=0: [(x * sc, y * sc) for x, y in _wob(pts, amp, seed)]
        mint = _fillcol(INK_MINT); apron = _fillcol(INK_APRON)
        # hoodie: rounded torso with shoulders
        torso = [(60, 40), (240, 40), (272, 100), (268, 250), (230, 286), (70, 286), (32, 250), (28, 100)]
        tp = _arcpts(150, 160, 122, 128, 0, 360, 36)
        d.polygon([(x * sc, y * sc) for x, y in tp], fill=mint + (255,))
        if INK_MODE == "wash":
            m = Image.new("L", im.size, 0); ImageDraw.Draw(m).polygon([(x * sc, y * sc) for x, y in tp], fill=255)
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse(S(150, 60, 290, 300), fill=INK_MINT_S + (150,))
            im.alpha_composite(Image.composite(sh, Image.new("RGBA", im.size, (0, 0, 0, 0)), m))
        d.line(wob(tp, 2.0, 5), fill=INKC + (255,), width=INK_W * sc, joint="curve")
        # hood collar: two strokes
        d.line(wob(_arcpts(150, 44, 54, 30, 180, 360, 14), 1.4, 6), fill=INKC + (255,), width=(INK_W - 1) * sc, joint="curve")
        # apron: bib + skirt, outlined, with strap strokes and a pocket
        ap = [(106, 62), (194, 62), (210, 150), (232, 150), (252, 282), (236, 290), (150, 286), (64, 290), (48, 282), (68, 150), (90, 150)]
        d.polygon([(x * sc, y * sc) for x, y in ap], fill=apron + (255,))
        if INK_MODE == "wash":
            _hatch(im, S, (170, 150, 236, 288, lambda q: q.polygon([(x * sc, y * sc) for x, y in [(180, 150), (236, 150), (232, 288), (176, 288)]], fill=255)), -40, 10, INKC + (26,), 1)
        d.line(wob(ap + [ap[0]], 1.8, 7), fill=INKC + (255,), width=INK_W * sc, joint="curve")
        for x0 in (110, 190): d.line(wob([(x0, 64), (150 + (x0 - 150) * 0.5, 36)], 1.0, 8), fill=INKC + (255,), width=(INK_W - 2) * sc)
        d.line(wob([(68, 152), (232, 152)], 1.0, 9), fill=INKC + (255,), width=(INK_W - 2) * sc)
        d.line(wob([(232, 152), (268, 134)], 1.0, 10), fill=INKC + (255,), width=(INK_W - 2) * sc); d.line(wob([(232, 152), (272, 168)], 1.0, 11), fill=INKC + (255,), width=(INK_W - 2) * sc)
        d.line(wob([(104, 196), (196, 196), (200, 250), (100, 250), (104, 196)], 1.4, 14), fill=INKC + (255,), width=(INK_W - 2) * sc, joint="curve")
        if logo:
            d.ellipse(S(136, 204, 164, 232), fill=mint + (255,), outline=INKC + (255,), width=3 * sc)
            d.polygon(S(150, 208, 160, 218, 150, 228, 140, 218), fill=apron + (255,))
        # a couple of fold strokes
        for (x0, x1, sd) in ((82, 70, 12), (218, 230, 13), (120, 112, 15), (180, 188, 16)):
            d.line(wob([(x0, 170), (x1, 276)], 1.2, sd), fill=INKC + (110,), width=3 * sc)
        return _done(im, W_, H_)
    return gcache(("cbody_ink", INK_MODE, tuple(shirt), logo), mk)


def _hand_ink_el(tint=0.0, side=1):
    def mk():
        W_, H_, sc = 100, 110, 3
        im = Image.new("RGBA", (W_ * sc, H_ * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
        skin = _mix3(INK_SKIN, (255, 160, 70), round(clamp(tint) * 10) / 10) if INK_MODE != "mono" else PAPER
        for fx, fy, fh in ((34, 18, 40), (48, 10, 48), (62, 14, 44), (74, 26, 36)):
            d.rounded_rectangle(S(fx - 7, fy, fx + 7, fy + fh), 7 * sc, fill=skin + (255,), outline=INKC + (255,), width=(INK_W - 3) * sc)
        d.rounded_rectangle(S(24, 42, 84, 100), 20 * sc, fill=skin + (255,), outline=INKC + (255,), width=(INK_W - 2) * sc)
        d.rounded_rectangle(S(4, 54, 36, 72), 8 * sc, fill=skin + (255,), outline=INKC + (255,), width=(INK_W - 3) * sc)
        d.line(S(26, 58, 36, 62), fill=skin + (255,), width=10 * sc)
        for fx in (41, 55, 69): d.line(S(fx, 44, fx, 52), fill=INKC + (255,), width=2 * sc)
        el = _done(im, W_, H_)
        if side < 0: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
        return el
    return gcache(("hand_ink", INK_MODE, round(clamp(tint) * 10) / 10, side), mk)


def _mitt_el(tint=0.0): return _hand_ink_el(tint, 1)


def _sneaker_ink_el(side=1):
    def mk():
        W_, H_, sc = 110, 56, 3
        im = Image.new("RGBA", (W_ * sc, H_ * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(8, 8, 102, 48), 18 * sc, fill=_fillcol((250, 248, 242)) + (255,), outline=INKC + (255,), width=(INK_W - 2) * sc)
        d.line(S(10, 36, 100, 36), fill=INKC + (255,), width=3 * sc)
        d.line(S(30, 30, 62, 24), fill=_fillcol(INK_MINT) + (255,) if INK_MODE != "mono" else INKC + (255,), width=5 * sc)
        for i in range(3): d.line(S(28 + i * 9, 14, 32 + i * 9, 24), fill=INKC + (200,), width=2 * sc)
        el = _done(im, W_, H_)
        if side < 0: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
        return el
    return gcache(("sneak_ink", INK_MODE, side), mk)


def _ink_limb(f, pts, w, fill, shade, s, seed):
    """ink limb: a coloured stroke with a thinner ink outline (two passes) and a fixed wobble."""
    P = _wob(pts, 1.2 * s, seed)
    A = np.array(P, np.int32)
    cv2.polylines(f, [A], False, C(INKC), max(2, int(w + 2 * INK_W * 0.45 * s)), cv2.LINE_AA)
    cv2.polylines(f, [A], False, C(_fillcol(fill)), max(1, int(w)), cv2.LINE_AA)
    if INK_MODE == "wash":
        Q = [(x + 0.28 * w, y + 0.1 * w) for x, y in P]
        cv2.polylines(f, [np.array(Q, np.int32)], False, C(shade), max(1, int(w * 0.35)), cv2.LINE_AA)


def chub(f, x, y, s=1.0, la=(20, 10), ra=(20, 10), ll=6, rl=6, mouth=0, blink=False, brow="n", look=(0, 0), expr="n", tint=0.0,
         hold=None, hold_off=(0, 0), hold_l=None, bob=0.0, op=1.0, shirt=HOOD3, shadow=True, lean=0.0, squash=0.0, sit=False, nose=None, cap=False,
         hold_front=False, t=None):
    g = f if op >= 0.999 else f.copy()
    if t is not None:
        bob = bob + 3.0 * math.sin(t * 2.4)
        if not blink: blink = blink_at(t, int(x) % 7)
    sq = 1 + 0.12 * squash
    if shadow:
        contact(g, x, y + 6 * s, 300 * s, 0.30)
    hipy = y - 112 * s / sq
    for side, ang in ((-1, ll), (1, rl)):
        hx_ = x + side * 46 * s
        if sit:
            kn = (hx_ + side * 30 * s, hipy + 20 * s); ft = (hx_ + side * 40 * s, y)
            _ink_limb(g, ((hx_, hipy), kn, ft), 26 * s, INK_JEAN, INK_JEAN_S, s, 50 + side)
        else:
            ft = (hx_ + side * math.sin(math.radians(ang)) * 104 * s, hipy + math.cos(math.radians(ang)) * 104 * s)
            _ink_limb(g, ((hx_, hipy), ft), 26 * s, INK_JEAN, INK_JEAN_S, s, 50 + side)
        comp(g, scale_el(_sneaker_ink_el(side), s), ft[0] + side * 14 * s, ft[1] + 2 * s)
    lr = math.radians(lean)
    bcx = x + 40 * s * math.sin(lr); bcy = y - 222 * s / sq + bob * s * 0.5
    el = scale_el(chub_body_el(shirt), s)
    if t is not None or abs(sq - 1) > 1e-3:
        br = 1 + (0.012 * math.sin(t * 2.4) if t is not None else 0.0)
        el = scale_xy(el, (1 + 0.1 * squash) * br, (1 / sq) / br)
    comp(g, el, bcx, bcy)
    hands = {}; fore = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sh_ = (bcx + side * 118 * s, bcy - 46 * s)
        e = (sh_[0] + side * math.sin(math.radians(a1)) * 76 * s, sh_[1] + math.cos(math.radians(a1)) * 76 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 70 * s, e[1] + math.cos(math.radians(a2)) * 70 * s)
        _ink_limb(g, (sh_, e, hd), 24 * s, INK_MINT, INK_MINT_S, s, 60 + side)
        c0 = (e[0] + (hd[0] - e[0]) * 0.6, e[1] + (hd[1] - e[1]) * 0.6)      # rolled cuff: a short ink band
        cv2.circle(g, (int(c0[0]), int(c0[1])), int(15 * s), C(INKC), -1, cv2.LINE_AA); cv2.circle(g, (int(c0[0]), int(c0[1])), int(12 * s), C(_fillcol(INK_MINT_S)), -1, cv2.LINE_AA)
        hands[side] = hd; fore[side] = math.degrees(math.atan2(hd[1] - e[1], hd[0] - e[0]))
    def hand_at(side):
        comp(g, _rot_el(scale_el(_hand_ink_el(tint, side), s), -(fore[side] + 90)), hands[side][0], hands[side][1])
    if hold is not None and not hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    if hold_l is not None:
        hx, hy = hands[-1]; comp(g, hold_l, hx - hold_off[0] * s, hy + hold_off[1] * s)
    hand_at(-1); hand_at(1)
    hxc, hyc = bcx + 14 * s * math.sin(lr), bcy - 214 * s / sq + bob * s
    _ink_limb(g, ((bcx, bcy - 100 * s), (hxc, hyc + 70 * s)), 30 * s, INK_SKIN, INK_SKIN_S, s, 70)       # neck
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
    comp(f, scale_el(_hand_ink_el(tint, 1), s * 0.95), x, y)


_PAPER = {}


def paper(f, amt=0.08, seed=1):
    """paper-grain texture multiplied over the frame (cached)."""
    if seed not in _PAPER:
        rng = np.random.default_rng(seed); n = rng.random((H // 3, W // 3)).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), 0.8); n = cv2.resize(n, (W, H)); _PAPER[seed] = (n - 0.5)
    f *= (1 + _PAPER[seed][..., None] * amt * 2)
    return f
