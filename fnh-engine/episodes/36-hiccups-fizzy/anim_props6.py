# ================= anim_props6.py = lib36 (ep 36, 14 Nov): "Why do fizzy drinks give you hiccups?" — FIZZ-AQUA accent, ink props, NEW PLACE
# THE HOUSE PARTY (warm evening living room, bunting, ink balloons that bob, fairy lights, a striped party table), the fizzy glass + bottle, the board
# torso (lungs, the diaphragm dome that breathes, the stomach that inflates like a balloon, the nerve, the windpipe), the vocal-cord DOORS, the
# ultrasound fan with a hiccupping baby, and the ep 36 craft skill: hic() = an INVOLUNTARY ACTION (no anticipation, 2-frame jolt, stillness, settle,
# every repeat different). =================
ACC = (40, 168, 204); ACC_S = (18, 110, 146); ACC_L = (150, 214, 232); ACC_XL = (222, 242, 248)       # fizz aqua = the drink, the gas, the bubbles
SODA = (196, 232, 236); SODA_S = (120, 190, 204)
CORAL = (226, 120, 104)
NERVE = (206, 52, 52)
SRC_CC = "Source: Cleveland Clinic; NHS"
SRC_WOMB = "Source: Live Science (UCL); The Conversation"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- craft skill (ep 36): INVOLUNTARY ACTION — the hiccup jolt ----------------
def _hic_one(q, a, hold, sgn):
    """q = frames since the hic; returns the jolt 0..1 (can dip a little below 0 on the settle)."""
    if q < 0: return 0.0
    if q < 2: return eo(q / 2)                                                    # 2 frames, NO anticipation: a reflex has no wind-up
    if q < 2 + hold: return 1.0                                                   # stillness: the body 'doesn't know what happened'
    k = (q - 2 - hold) / 9.0
    if k < 1: return (1 - eio(k)) - 0.22 * math.sin(math.pi * k)                  # 9-frame settle with a small sink below rest
    return 0.0


def hic(t, times, amp=1.0, seed=36):
    """INVOLUNTARY ACTION (ep 36): the hiccup jolt at each time in `times`. Unlike a take (anticipation -> snap) a reflex fires with NO wind-up:
    2 frames up (stretch, shoulders hunch, head snaps back), a 2-4 frame STILL hold, then a 9-frame settle that sinks a little below rest.
    Every repeat varies (amplitude 0.8-1.15, hold length, head direction) so a run of hiccups never looks mechanical.
    Returns dict(dy, squash, lean, expr, brow, mouth, arm, hair, k) for chub(); k = the raw jolt (use it to splash the drink)."""
    out = dict(dy=0.0, squash=0.0, lean=0.0, expr=None, brow=None, mouth=None, arm=0.0, hair=(0, 0), k=0.0)
    past = [(i, ti) for i, ti in enumerate(times) if ti <= t < ti + 1.0]
    if not past: return out
    i, ti = past[-1]
    r = np.random.default_rng(seed + 7 * i).random(3)
    a = amp * (0.8 + 0.35 * r[0]); hold = 2 + int(3 * r[1]); sgn = 1 if (i + int(r[2] * 2)) % 2 == 0 else -1
    q = (t - ti) * FPS
    j = _hic_one(q, a, hold, sgn); jl = _hic_one(q - 3, a, hold, sgn)             # the hair lags 3 frames (follow-through)
    out.update(dy=-24 * a * j, squash=-0.38 * a * j, lean=-6 * a * sgn * j, arm=16 * a * max(j, 0), hair=(0, 18 * a * (jl - j)), k=max(0.0, j))
    if q < 2 + hold + 4: out.update(expr="wow", brow="up", mouth="o")
    return out


def hic_word(f, t, times, x, y, size=120, col=None):
    """a small 'hic!' that pops out of the mouth on each hiccup and floats up (no anticipation either)."""
    for i, ti in enumerate(times):
        q = t - ti
        if 0 <= q < 0.9:
            kin_word(f, "hic!", x + (30 if i % 2 else -30) + 40 * q, y - 120 * q, t, ti, "pop", int(size * (1 - 0.2 * q)), col or ACC_S, stroke=2, stroke_col=INKC,
                     stagger=0.02, op=clamp(1.6 - 1.8 * q))


# ---------------- props ----------------
def fizzy_glass_el(level=0.85, tilt=0.0, mood=None, look=(0, 0), seed=361):
    """a tall glass of fizzy drink (generic, no brand): pale aqua soda, bubbles inked, a foam line, a straw-free rim highlight."""
    lv = round(clamp(level) * 10) / 10
    def mk():
        w, h = 200, 330; im, d, S = _cv(w, h)
        yl = 300 - 260 * lv
        d.polygon(S(40, yl, 160, yl, 150, 304, 50, 304), fill=SODA + (255,))
        d.polygon(S(104, yl, 160, yl, 150, 304, 108, 304), fill=SODA_S + (140,))
        if lv > 0.05:
            d.line(_P(_wob([(42, yl), (158, yl)], 1.0, seed)), fill=(255, 255, 255, 255), width=6 * SC3)
            rr = np.random.default_rng(seed)
            for _ in range(14):
                bx, by = rr.uniform(56, 144), rr.uniform(yl + 14, 292); br = rr.uniform(4, 9)
                d.ellipse(S(bx - br, by - br, bx + br, by + br), outline=ACC_S + (230,), width=2 * SC3)
        _ink_poly(d, [(28, 18), (172, 18), (156, 312), (44, 312)], None, seed, INK_W, amp=0.9)
        d.line(_P([(50, 44), (60, 280)]), fill=(255, 255, 255, 220), width=7 * SC3)
        if mood: _face(d, S, 100, 220, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("fglass36", lv, mood, tuple(look), seed), mk)


def soda_bottle_el(seed=362):
    """a generic soda bottle (no label text): aqua glass, a cream band, a cap."""
    def mk():
        w, h = 150, 380; im, d, S = _cv(w, h)
        P = [(58, 30), (92, 30), (92, 90), (124, 150), (124, 350), (26, 350), (26, 150), (58, 90)]
        _ink_poly(d, P, ACC_L, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.rectangle(S_(84, 0, 150, 380), fill=c), ACC_S, 110)
        _ink_poly(d, [(26, 200), (124, 200), (124, 270), (26, 270)], PAPER, seed + 1, INK_W - 2, amp=0.6)
        _ink_poly(d, [(54, 14), (96, 14), (96, 34), (54, 34)], CORAL, seed + 2, INK_W - 2, amp=0.5)
        d.line(_P([(40, 160), (40, 330)]), fill=(255, 255, 255, 200), width=6 * SC3)
        return _done(im, w, h)
    return gcache(("sbottle36", seed), mk)


def balloon36_el(col=None, seed=363):
    """an INK balloon (flat fill + one wobbly outline + a hatch on the shadow side + a knot + string)."""
    col = col or ACC
    def mk():
        w, h = 200, 420; im, d, S = _cv(w, h)
        d.line(_P(_wob([(100, 250), (110, 300), (92, 350), (104, 415)], 1.5, seed)), fill=INKC + (255,), width=3 * SC3, joint="curve")
        P = _arcpts(100, 128, 84, 112, 0, 360, 30)[:-1]
        _ink_poly(d, P, col, seed, INK_W, amp=1.1)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(100, 40, 230, 260), fill=c), _mix(col, INKC, 0.3), 110)
        _hatch_in(im, (100, 20, 190, 240), lambda q, S_: q.polygon(_P(P), fill=255))
        _ink_poly(d, [(90, 238), (110, 238), (100, 254)], col, seed + 1, INK_W - 2, amp=0.4)
        d.ellipse(S(52, 58, 80, 100), fill=(255, 255, 255, 170))
        return _done(im, w, h)
    return gcache(("balloon36", col, seed), mk)


def balloon_bob(f, x, y, t, col=None, s=1.0, seed=0, op=1.0):
    """a balloon that bobs and sways on its string (secondary action in the background)."""
    rot = 4 * math.sin(t * 1.3 + seed); dy = 10 * math.sin(t * 0.9 + seed * 1.7)
    rot_comp(f, scale_el(balloon36_el(col, 363 + seed), s), x, y + dy, rot, 1.0, op, 0.0)


# ---------------- NEW PLACE: THE HOUSE PARTY ----------------
def _party_table_el(top_y=1330):
    """the party table front: aqua + cream stripes, an ink edge, a paper-cream fringe."""
    def mk():
        h = H - top_y; rgb = np.zeros((h, W, 3), np.float32); rgb[:] = np.array(C(PAPER), np.float32)
        for x in range(-40, W + 80, 140): cv2.rectangle(rgb, (x, 0), (x + 70, h), C(_mix(ACC, PAPER, 0.62)), -1)
        for x in range(0, W, 36):                                                     # scalloped fringe
            cv2.ellipse(rgb, (x + 18, 34), (18, 16), 0, 0, 180, C(_mix(ACC, INKC, 0.25)), -1, cv2.LINE_AA)
        cv2.rectangle(rgb, (0, 0), (W, 34), C(_mix(ACC, INKC, 0.25)), -1)
        g = np.clip(np.arange(h, dtype=np.float32) / h, 0, 1)[:, None, None]; rgb = rgb * (1 - 0.2 * g)
        cv2.line(rgb, (0, 2), (W, 2), C(INKC), 5, cv2.LINE_AA)
        return rgb.astype(np.float32), np.ones((h, W), np.float32)
    return gcache(("ptable36", top_y), mk)


def party_front(f, top_y=1330):
    """draw the party table IN FRONT of Chubby (he stands behind it; props on it at y ~ top_y - 10)."""
    comp(f, _party_table_el(top_y), W / 2, top_y + (H - top_y) / 2)


def set_party(t=0.0, blur=4, top_y=1330, dim=0.0, balloons=True):
    """NEW PLACE (ep 36) THE HOUSE PARTY: a warm evening living room — peach wall, a night window with fairy lights, bunting across the top,
    a shelf with gifts, the party table from top_y; warm lamp key light from the left; ink balloons bob in front of the wall (secondary action);
    paper-softened for Chubby INK. dim 0..1 = lights down."""
    def mk():
        f = _vgrad((246, 214, 190), (230, 188, 166), 0, top_y)
        cv2.rectangle(f, (600, 380), (1010, 1040), C((112, 84, 70)), -1, cv2.LINE_AA)                     # window frame
        f[404:1016, 624:986] = _vgrad((40, 46, 86), (74, 64, 104), 404, 1016)[404:1016, 624:986]          # night sky
        cv2.line(f, (805, 404), (805, 1016), C((112, 84, 70)), 14, cv2.LINE_AA); cv2.line(f, (624, 710), (986, 710), C((112, 84, 70)), 14, cv2.LINE_AA)
        for i in range(9): cv2.circle(f, (650 + 40 * i, 470 + int(20 * math.sin(i))), 3, C((255, 240, 200)), -1, cv2.LINE_AA)   # far city lights
        cv2.rectangle(f, (40, 820), (460, 846), C((150, 112, 78)), -1, cv2.LINE_AA)                       # shelf + gifts
        for (x, w_, h_, c) in ((80, 110, 90, _mix(ACC, PAPER, 0.3)), (210, 90, 120, (240, 228, 200)), (320, 110, 70, _mix(CORAL, PAPER, 0.3))):
            cv2.rectangle(f, (x, 820 - h_), (x + w_, 820), C(c), -1, cv2.LINE_AA)
            cv2.line(f, (x + w_ // 2, 820 - h_), (x + w_ // 2, 820), C((200, 70, 80)), 6, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_party", blur, top_y), mk).copy()
    for i in range(14):                                                               # fairy lights along the window top (twinkle)
        x = 610 + 30 * i; y = 400 + 14 * math.sin(i * 0.8); a = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7)
        glow(f, x, y, 26, (255, 214, 140), 0.10 + 0.08 * a)
        cv2.circle(f, (int(x), int(y)), 5, C(_mix((255, 214, 140), (255, 255, 255), a)), -1, cv2.LINE_AA)
    pts = [(20, 170), (270, 230), (540, 190), (810, 230), (1060, 170)]                 # bunting (decoration only, above the hook words)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cv2.line(f, (x0, y0), (x1, y1), C(INKC), 3, cv2.LINE_AA)
        for j in range(4):
            u = (j + 0.5) / 4; x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u + 6 * math.sin(t * 1.5 + j + x0)
            col = (ACC, PAPER, INK_MINT, CORAL)[(j + x0 // 270) % 4]
            tri = np.array([(x - 26, y), (x + 26, y), (x, y + 52)], np.int32)
            cv2.fillPoly(f, [tri], C(_mix(col, PAPER, 0.25)), cv2.LINE_AA); cv2.polylines(f, [tri], True, C(INKC), 2, cv2.LINE_AA)
    if balloons:
        balloon_bob(f, 110, 930, t, ACC, 1.0, 1); balloon_bob(f, 215, 1010, t, PAPER, 0.85, 2); balloon_bob(f, 975, 1130, t, INK_MINT, 0.8, 3)
    lamp_glow(f, 60, 700, 520, (255, 210, 150), 0.35)
    if dim > 0: f = f * (1 - 0.55 * dim)
    return inkify(f)


# ---------------- BOARD: the torso (lungs, diaphragm dome, stomach balloon, nerve, windpipe) ----------------
TX = 540
def dome_pts(drop=0.0, bulge=0.0, y0=1010):
    """the diaphragm dome: peak at y0 - 120 when relaxed; drop 0..1 flattens it down (breathing in / the jerk); bulge = pushed up on the right."""
    P = []
    for i in range(41):
        u = i / 40; x = 200 + 680 * u
        h = 120 * (1 - drop * 0.75) * math.sin(math.pi * u) ** 0.8
        h += bulge * 60 * math.exp(-((u - 0.68) / 0.16) ** 2)
        P.append((x, y0 - h))
    return P


def lung_pts(side, k=0.0):
    """a lung outline (side -1 = viewer left), k 0..1 = breath (taller down to the dome)."""
    cx = TX + side * 175; s = 1 + 0.08 * k
    P = []
    for a in np.linspace(-math.pi / 2, 3 * math.pi / 2, 30):
        rx = 130 * s; ry = 200 * s
        x = cx + rx * math.cos(a) * (0.85 if (math.cos(a) * side) < 0 else 1.0); y = 760 + 30 * k + ry * math.sin(a) * (0.9 if math.sin(a) < 0 else 1.0)
        P.append((x, y))
    return P


def board_torso(f, t, t0, k=None, lung_k=0.0, drop=0.0, bulge=0.0, st_r=0.0, st_t=None, nerve_k=0.0, nerve_t=None, show_lungs=True, show_body=True, pipe=True):
    """the board body: outline, windpipe, lungs, the dome (thick, the hero), the stomach as an inflating aqua balloon right under it."""
    kd = ramp36(t, t0, 0.5) if k is None else k
    if show_body:
        body = [(330, 330), (330, 440), (150, 520), (120, 1380), (960, 1380), (930, 520), (750, 440), (750, 330)]
        draw_on(f, body, kd, BP_INK, 5, seed=361, tip=kd < 1)
    if pipe and kd > 0.2:
        draw_on(f, [(TX - 22, 340), (TX - 22, 560)], clamp((kd - 0.2) / 0.5), BP_INK, 5, seed=362, tip=False)
        draw_on(f, [(TX + 22, 340), (TX + 22, 560)], clamp((kd - 0.2) / 0.5), BP_INK, 5, seed=363, tip=False)
    if show_lungs and kd > 0.3:
        for sd in (-1, 1):
            P = lung_pts(sd, lung_k)
            cv2.fillPoly(f, [np.array(P, np.int32)], C((250, 232, 228)), cv2.LINE_AA)
            draw_on(f, P, clamp((kd - 0.3) / 0.6), BP_INK, 6, seed=364 + sd, tip=False, closed=True)
    if st_r > 1:
        cx, cy = 660, 1012 + st_r
        P = _arcpts(cx, cy, st_r * 1.15, st_r, 0, 360, 40)[:-1]
        cv2.fillPoly(f, [np.array(P, np.int32)], C(ACC_XL), cv2.LINE_AA)
        hatch_on(f, P, 1.0 if st_t is None else ramp36(t, st_t, 0.4), ACC, gap=16)
        draw_on(f, P, 1.0, ACC_S, 7, seed=367, tip=False, closed=True)
        rr = np.random.default_rng(3)
        for j in range(int(st_r / 12)):                                              # gas bubbles inside
            a = rr.uniform(0, 2 * math.pi); r_ = rr.uniform(0.1, 0.75) * st_r; bb = rr.uniform(6, 12)
            y_ = cy + r_ * math.sin(a) - ((t * 60 + j * 37) % (st_r * 0.6))
            cv2.circle(f, (int(cx + r_ * 1.1 * math.cos(a)), int(max(cy - st_r + 14, y_))), int(bb), C(ACC_S), 2, cv2.LINE_AA)
    D = dome_pts(drop, bulge)
    if kd > 0.5:
        draw_on(f, D, clamp((kd - 0.5) / 0.5), (190, 60, 70) if nerve_k > 0.5 else BP_INK, 13, seed=368, tip=kd < 1)
    if nerve_k > 0:                                                                   # the nerve: from the dome up the neck, zigzag + red when irritated
        N = [(250, 960), (215, 760), (240, 560), (380, 470), (500, 340)]
        draw_on(f, N, nerve_k, NERVE, 5, seed=369, tip=nerve_k < 1)
        if nerve_t is not None and t > nerve_t:
            for j in range(3):
                pulse_path(f, N, t, nerve_t + 0.25 * j, 0.6, (255, 120, 90), 14)
    return D


def ramp36(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


# ---------------- BOARD: the vocal cords as two doors in the windpipe (close-up) ----------------
def cord_doors(f, t, cx, cy, shut, w=420, h=560):
    """a cut-away windpipe (two walls) with the vocal cords as two swing DOORS; shut 0 = open (a gap for air), 1 = slammed shut."""
    draw_on(f, [(cx - w / 2, cy - h / 2), (cx - w / 2, cy + h / 2)], 1.0, BP_INK, 9, seed=371, tip=False)
    draw_on(f, [(cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2)], 1.0, BP_INK, 9, seed=372, tip=False)
    gap = (1 - clamp(shut)) * 0.42
    for sd in (-1, 1):
        x0 = cx + sd * w / 2; L = w / 2
        ang = math.radians(130 * gap + 2)                                            # hinge at the wall: doors swing up (~55 deg) when open
        x1 = x0 - sd * (L - 6) * math.cos(ang); y1 = cy - (L - 6) * math.sin(ang)
        nx, ny = -math.sin(ang) * 22, -math.cos(ang) * 22
        P = [(x0, cy - 22), (x1, y1 - 22), (x1, y1 + 22), (x0, cy + 22)]
        cv2.fillPoly(f, [np.array(P, np.int32)], C(_mix(CORAL, (255, 255, 255), 0.35)), cv2.LINE_AA)
        draw_on(f, P, 1.0, BP_INK, 6, seed=373 + sd, tip=False, closed=True)
        kx = x0 + (x1 - x0) * 0.8; ky = cy + (y1 - cy) * 0.8
        cv2.circle(f, (int(kx), int(ky)), 8, C(BP_INK), -1, cv2.LINE_AA)               # the door knob


# ---------------- BOARD: the ultrasound fan + the hiccupping baby ----------------
def ultrasound(f, t, cx, cy, k, hics=(), r=430):
    """a dark ultrasound fan on the board; inside, a curled baby silhouette that jolts on each time in `hics`."""
    P = [(cx, cy - 560)] + [(cx + (r * 1.15) * math.cos(math.radians(a)) * k, cy - 560 + (r * 1.6) * math.sin(math.radians(a)) * k) for a in np.linspace(40, 140, 30)]
    cv2.fillPoly(f, [np.array(P, np.int32)], C((34, 36, 44)), cv2.LINE_AA)
    rr = np.random.default_rng(int(t * 8))
    if k > 0.6:
        for _ in range(60):                                                           # speckle
            x = cx + rr.uniform(-300, 300); y = cy - 200 + rr.uniform(-160, 220)
            cv2.circle(f, (int(x), int(y)), 2, C((90, 92, 100)), -1)
        j = 0.0
        for ti in hics:
            q = (t - ti) * FPS
            if 0 <= q < 14: j = max(j, _hic_one(q, 1, 2, 1))
        bx, by = cx, cy - 120 - 22 * j
        g = (196, 200, 206)
        cv2.ellipse(f, (int(bx - 20), int(by + 30)), (110, 80), -20, 0, 360, C(g), -1, cv2.LINE_AA)       # curled body
        cv2.circle(f, (int(bx + 80), int(by - 80)), 92, C(g), -1, cv2.LINE_AA)                            # big baby head
        cv2.circle(f, (int(bx + 120), int(by - 90)), 9, C((60, 62, 70)), -1, cv2.LINE_AA)                 # closed-eye dot
        cv2.ellipse(f, (int(bx + 160), int(by - 60)), (14, 10), 0, 0, 360, C((150, 154, 162)), -1, cv2.LINE_AA)   # nose bump
        cv2.ellipse(f, (int(bx + 40), int(by + 30)), (50, 18), 30, 0, 360, C((150, 154, 162)), -1, cv2.LINE_AA)  # tucked arm
        cv2.ellipse(f, (int(bx - 110), int(by + 70)), (40, 22), -30, 0, 360, C((150, 154, 162)), -1, cv2.LINE_AA)  # tucked leg
    draw_on(f, P, 1.0, BP_INK, 5, seed=381, tip=False, closed=True)
