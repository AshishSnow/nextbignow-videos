# ================= anim_props_lib61.py (ep 61) (ep 61, 24 Nov): "Does sitting too close to the TV ruin your eyes?" — ACCENT = SCREEN BLUE
# (the TV glow, the hot words, the eye rays). Radiation gets a warning yellow ONLY in the 1960s chapter.
# NEW CRAFT (ep 61) = SCREEN LIGHT (practical / interactive light from a TV): screen_light(...) = the screen is the KEY light of a dark room:
#   - a MULTIPLY layer (dark cool ambient everywhere, the screen colour where the light lands), so light shows ONLY where it hits (Toon Boom
#     'interactive lighting'; Clip Studio 'dynamic lights': darken the room edges and around the subject);
#   - falloff by DISTANCE (1 / (1 + (d/r)^2), inverse-square-like): lean in = bright face, sit back = the light on you drops (that IS the story);
#   - the colour follows the PICTURE: stepped 'scene cuts' every 1-3 s at uneven times + a tiny 3-frame flicker (PremiumBeat 'simulating light from a
#     screen': raise / lower the intensity every few seconds to mimic a scene change; Toon Boom forum: a 3-frame cycle; Clip Studio: shift the hue a
#     little between cels);
#   - the subject throws a soft SHADOW on the wall away from the screen (cast_shadow_of: the character drawn into a mask, shifted, scaled, blurred);
#   - an additive spill near the screen so the glass itself glows.
# NEW PROPS (ink): flat_tv (3/4 modern TV on a low cabinet, live picture warped onto the screen), crt60 (a 1960s wooden console TV: legs, round-cornered
#   screen, grille, knobs, rabbit-ear antenna, live colour picture), rad_rays (wavy radiation leaking out), safe_meter (SAFE / DANGER gauge),
#   doorway (warm hallway light for mom). NEW PLACE: set_room60(t, dim) = a 1960s living room (mustard diamond wallpaper, floor lamp, curtains, rug).
ACC = (44, 120, 232); ACC_S = (20, 70, 160); ACC_L = (150, 196, 250); ACC_XL = (220, 236, 252)      # screen blue
RAD = (250, 206, 40); RAD_S = (196, 140, 10)
WOOD6 = (150, 96, 54); WOOD6_S = (104, 62, 32); WOOD6_L = (192, 138, 86)
PINKC = (240, 180, 176); PINKC_S = (214, 130, 128)
RED = (176, 40, 44); OKG = (40, 140, 80); GOLD = (232, 176, 40)
COAT = (246, 248, 250)
SRC_AAO = "Source: American Academy of Ophthalmology"
SRC_SCIAM = "Source: Scientific American; The Star (2026)"
SRC_KIDS = "Source: AAO; Scientific American"
SRC_NEAR = "Source: KSDK Verify (eye doctors); Scientific American"
SC3 = 3

SCENES = [(120, 190, 255), (110, 210, 140), (255, 170, 90), (190, 140, 255), (90, 220, 230), (255, 140, 170)]


def tv_scene(t, seed=0):
    """which picture is on the TV now: stepped scene cuts at uneven times (1.1-2.9 s). Returns (index, time into the scene)."""
    rng = np.random.default_rng(611 + seed); acc = -3.0; i = 0
    while True:
        d = rng.uniform(1.1, 2.9)
        if acc + d > t: return i % len(SCENES), t - acc
        acc += d; i += 1


def tv_col(t, seed=0):
    """the colour the screen throws into the room: the scene colour (blended toward white) x a small 3-frame flicker."""
    i, u = tv_scene(t, seed)
    c = np.array(SCENES[i], np.float32) * 0.6 + 255 * 0.4
    fl = (1.0, 0.93, 0.97)[int(t * FPS) % 3]
    if u < 0.08: fl *= 1.12                                                     # a cut = a tiny flash
    return tuple(float(v) * fl for v in c)


def tv_picture(w, h, t, seed=0, era=0):
    """the cartoon picture on the screen (a sky + a hill + a bouncing ball / a sun), w x h float image. era 1 = 1960s: softer + scanlines."""
    i, u = tv_scene(t, seed)
    top = np.array(SCENES[i], np.float32) / 255; bot = np.array(SCENES[(i + 2) % len(SCENES)], np.float32) / 255
    g = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    img = np.ones((h, w, 3), np.float32) * (top * (1 - g) + bot * g)
    cv2.ellipse(img, (int(w * 0.5), int(h * 1.05)), (int(w * 0.8), int(h * 0.42)), 0, 180, 360, tuple(float(v) for v in bot * 0.7), -1, cv2.LINE_AA)
    bx = w * (0.2 + 0.6 * ((u * 0.45) % 1.0)); by = h * (0.62 - 0.32 * abs(math.sin(u * 4.2)))
    cv2.circle(img, (int(bx), int(by)), max(3, int(h * 0.1)), (1.0, 0.95, 0.8), -1, cv2.LINE_AA)
    cv2.circle(img, (int(w * 0.8), int(h * 0.22)), max(3, int(h * 0.09)), (1.0, 0.98, 0.7), -1, cv2.LINE_AA)
    img = img * 0.82 + 0.18
    if era:
        img = cv2.GaussianBlur(img, (0, 0), 1.6) * 0.9 + 0.08
        img[::4] *= 0.78
    return np.clip(img, 0, 1).astype(np.float32)


def _quad_paste(f, img, quad):
    """warp img onto the 4-point quad (tl, tr, br, bl) of the frame."""
    h, w = img.shape[:2]
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), np.float32(quad))
    warped = cv2.warpPerspective(img, M, (W, H))
    m = cv2.warpPerspective(np.ones((h, w), np.float32), M, (W, H))[..., None]
    f[:] = f * (1 - m) + warped * m


def _ipoly(f, pts, fill, w=6):
    P = np.array([(int(x), int(y)) for x, y in pts], np.int32)
    if fill is not None: cv2.fillPoly(f, [P], C(fill), cv2.LINE_AA)
    cv2.polylines(f, [P], True, C(INKC), max(2, int(w)), cv2.LINE_AA)


def flat_tv(f, x, y, s, t, on=1.0, face=-1, seed=0):
    """a modern flat TV on a low cabinet, seen in 3/4 with its screen facing screen-LEFT (face=-1) or RIGHT (+1). (x, y) = the floor under the
    cabinet's centre. Returns the screen's centre (the light source)."""
    sw, sh, d = 150 * s, 330 * s, 26 * s                                         # foreshortened screen width, height, depth
    cx, cy = x, y - 270 * s - sh / 2
    _ipoly(f, [(x - 170 * s, y - 230 * s), (x + 170 * s, y - 230 * s), (x + 170 * s, y), (x - 170 * s, y)], WOOD6, 5 * s)
    _ipoly(f, [(x - 170 * s, y - 230 * s), (x + 170 * s, y - 230 * s), (x + 150 * s, y - 262 * s), (x - 150 * s, y - 262 * s)], WOOD6_L, 4 * s)
    cv2.line(f, (int(x), int(y - 220 * s)), (int(x), int(y - 10 * s)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    _ipoly(f, [(cx - 30 * s, y - 262 * s), (cx + 30 * s, y - 262 * s), (cx + 12 * s, cy + sh / 2 - 6 * s), (cx - 12 * s, cy + sh / 2 - 6 * s)], (60, 60, 70), 4 * s)
    fx = cx + face * sw / 2; bxx = cx - face * sw / 2
    near = [(bxx, cy - sh / 2 - 12 * s), (fx, cy - sh / 2 + 16 * s), (fx, cy + sh / 2 - 16 * s), (bxx, cy + sh / 2 + 12 * s)]
    back = [(p[0] - face * d, p[1]) for p in near]
    _ipoly(f, [back[0], near[0], near[3], back[3]], (40, 40, 48), 5 * s)
    _ipoly(f, near, (30, 30, 36), 6 * s)
    ins = [(near[0][0] + face * 10 * s, near[0][1] + 14 * s), (near[1][0] - face * 8 * s, near[1][1] + 10 * s),
           (near[2][0] - face * 8 * s, near[2][1] - 10 * s), (near[3][0] + face * 10 * s, near[3][1] - 14 * s)]
    quad = [ins[0], ins[1], ins[2], ins[3]] if face > 0 else [ins[1], ins[0], ins[3], ins[2]]
    if on > 0.02:
        pic = tv_picture(240, 300, t, seed) * on + (1 - on) * 0.1
        _quad_paste(f, pic, quad)
    cv2.polylines(f, [np.array([(int(a), int(b)) for a, b in ins], np.int32)], True, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    return (cx + face * sw * 0.3, cy)


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def crt60_el(seed=612):
    """a 1960s wooden CONSOLE TV (front view), no picture: legs, cabinet, a dark round-cornered screen hole, speaker grille, two knobs, rabbit ears.
    500 x 620, centre (250, 310); the screen hole box = (70, 140)-(330, 370) in el coords."""
    def mk():
        w, h = 500, 620; im, d, S = _cv(w, h)
        for lx, a in ((80, -1), (420, 1)):                                          # splayed legs
            d.line(S(lx, 500, lx + a * 30, 606), fill=INKC + (255,), width=18 * SC3)
            d.line(S(lx, 500, lx + a * 30, 606), fill=WOOD6_S + (255,), width=10 * SC3)
        d.line(S(250, 40, 150, 4), fill=INKC + (255,), width=6 * SC3)                       # rabbit ears
        d.line(S(250, 40, 360, 6), fill=INKC + (255,), width=6 * SC3)
        _ink_ell(d, 250, 50, 34, 18, (60, 60, 66), seed + 5, INK_W - 2, amp=0.6)
        _ink_poly(d, [(30, 70), (470, 70), (470, 510), (30, 510)], WOOD6, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P([(30, 70), (470, 70), (470, 510), (30, 510)]), fill=255),
               lambda q, S_, c: q.polygon(_P([(390, 70), (470, 70), (470, 510), (390, 510)]), fill=c), WOOD6_S, 110)
        d.rounded_rectangle(S(58, 128, 342, 382), radius=40 * SC3, fill=(70, 60, 50, 255), outline=INKC + (255,), width=5 * SC3)
        d.rounded_rectangle(S(70, 140, 330, 370), radius=34 * SC3, fill=(36, 40, 44, 255), outline=INKC + (255,), width=4 * SC3)
        _ink_poly(d, [(366, 140), (446, 140), (446, 300), (366, 300)], (214, 196, 160), seed + 1, INK_W - 2, amp=0.6)       # grille
        for k in range(7): d.line(S(374, 156 + 20 * k, 438, 156 + 20 * k), fill=INKC + (150,), width=3 * SC3)
        for k, ky in enumerate((340, 410)):
            _ink_ell(d, 406, ky, 22, 22, (220, 210, 190), seed + 2 + k, INK_W - 2, amp=0.5)
            d.line(S(406, ky, 420, ky - 14), fill=INKC + (255,), width=4 * SC3)
        d.line(S(60, 440, 340, 440), fill=WOOD6_L + (255,), width=6 * SC3)
        return _done(im, w, h)
    return gcache(("crt60", seed), mk)


def crt60(f, x, y, s, t, on=1.0, seed=3):
    """the console TV at (x, y) = its centre; draws the cabinet + a live 1960s colour picture in the screen. Returns the screen centre."""
    comp(f, scale_el(crt60_el(), s), x, y)
    x0, y0 = int(x + (74 - 250) * s), int(y + (144 - 310) * s); x1, y1 = int(x + (326 - 250) * s), int(y + (366 - 310) * s)
    if on > 0.02 and x1 > x0 + 8 and y1 > y0 + 8:
        pic = tv_picture(x1 - x0, y1 - y0, t, seed, era=1)
        m = np.zeros(pic.shape[:2], np.float32)
        r = max(2, int(30 * s))
        cv2.rectangle(m, (r, 0), (x1 - x0 - r, y1 - y0), 1.0, -1); cv2.rectangle(m, (0, r), (x1 - x0, y1 - y0 - r), 1.0, -1)
        for cx_, cy_ in ((r, r), (x1 - x0 - r, r), (r, y1 - y0 - r), (x1 - x0 - r, y1 - y0 - r)): cv2.circle(m, (cx_, cy_), r, 1.0, -1)
        m = cv2.GaussianBlur(m, (0, 0), 2.0)[..., None] * on
        reg = f[y0:y1, x0:x1]; hh, ww = reg.shape[:2]
        reg[:] = reg * (1 - m[:hh, :ww]) + pic[:hh, :ww] * m[:hh, :ww]
    return ((x0 + x1) / 2, (y0 + y1) / 2)


def rad_rays(f, x, y, t, k=1.0, n=7, s=1.0, spread=1.0, down=False):
    """wavy RADIATION rays leaking out of (x, y) in a fan (yellow with an ink edge), travelling outward; k 0..1 = how strong (0 = stopped)."""
    if k <= 0.01: return
    glow(f, x, y, 180 * s, (255, 230, 120), 0.22 * k)
    for i in range(n):
        a = math.radians((90 if down else -90) + (i - (n - 1) / 2) * 24 * spread)
        L = (200 + 60 * math.sin(t * 3 + i)) * s * (0.4 + 0.6 * k)
        pts = []
        for j in range(22):
            v = j / 21; r = 40 * s + L * v
            wv = 6 * s * math.sin(v * 12 - t * 12 + i)
            px = x + r * math.cos(a) - wv * math.sin(a); py = y + r * math.sin(a) + wv * math.cos(a)
            pts.append((int(px), int(py)))
        P = np.array(pts, np.int32)
        cv2.polylines(f, [P], False, C(INKC), max(3, int(11 * s * k)), cv2.LINE_AA)
        cv2.polylines(f, [P], False, C(RAD), max(2, int(6 * s * k)), cv2.LINE_AA)


def safe_meter(f, x, y, s, val, t=0.0):
    """a semicircle gauge: green SAFE zone (left 45 %), red DANGER, ink needle at val 0..1 (jitters when in the red)."""
    R = 170 * s
    cv2.ellipse(f, (int(x), int(y)), (int(R + 40 * s), int(R + 40 * s)), 0, 180, 360, C(PAPER), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(R), int(R)), 0, 180, 180 + 81, C(OKG), int(30 * s), cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(R), int(R)), 0, 180 + 81, 360, C(RED), int(30 * s), cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(R + 40 * s), int(R + 40 * s)), 0, 180, 360, C(INKC), max(3, int(6 * s)), cv2.LINE_AA)
    cv2.line(f, (int(x - R - 40 * s), int(y)), (int(x + R + 40 * s), int(y)), C(INKC), max(3, int(6 * s)), cv2.LINE_AA)
    v = clamp(val) + (0.02 * math.sin(t * 40) if val > 0.5 else 0)
    a = math.radians(180 + 180 * v)
    cv2.line(f, (int(x), int(y)), (int(x + R * 0.92 * math.cos(a)), int(y + R * 0.92 * math.sin(a))), C(INKC), max(3, int(10 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(16 * s), C(INKC), -1, cv2.LINE_AA)


def doorway(f, x0=40, y0=640, x1=330, y1=1330, amt=1.0):
    """a doorway with a warm lit hallway behind it (mom stands in it)."""
    cv2.rectangle(f, (x0 - 18, y0 - 18), (x1 + 18, y1), C((70, 54, 48)), -1, cv2.LINE_AA)
    g = _vgrad((255, 214, 150), (232, 176, 110), y0, y1)
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * (1 - amt) + g[y0:y1, x0:x1] * amt
    cv2.rectangle(f, (x0 - 18, y0 - 18), (x1 + 18, y1), C(INKC), 5, cv2.LINE_AA)


# ---------------- CRAFT: SCREEN LIGHT ----------------
_GX6 = np.arange(0, W, 8, dtype=np.float32)[None, :]; _GY6 = np.arange(0, H, 8, dtype=np.float32)[:, None]


def screen_light(f, x, y, t, amt=1.0, r=420, amb=0.42, seed=0, spill=0.22, col=None):
    """the TV as the KEY light of a dark room, applied as a MULTIPLY layer over everything drawn so far: cool dark ambient (amb) everywhere,
    the screen's current colour where the light lands, falling off with distance as 1 / (1 + (d / r)^2). Draw the TV picture AFTER this if the
    glass must stay bright. Returns the light colour (0..255)."""
    c = np.array(col if col is not None else tv_col(t, seed), np.float32) / 255
    d2 = ((_GX6 - x) ** 2 + (_GY6 - y) ** 2) / (r * r)
    g = cv2.resize((1.0 / (1.0 + d2)).astype(np.float32), (W, H))[..., None]
    cool = np.array([0.52, 0.58, 0.86], np.float32)
    m = amb * cool + (1 - amb) * g * amt * c * 1.25
    f[:] = f * np.clip(m, 0, 1.25)
    if spill > 0: glow(f, x, y, r * 0.55, tuple(float(v) * 255 for v in c), spill * amt)
    return tuple(float(v) * 255 for v in c)


def cast_shadow_of(f, draw_fn, dx=-140, dy=-10, sc=1.12, amt=0.45, blur=14, ymax=1330, ox=540, oy=1330):
    """a soft shadow of whatever draw_fn(g) draws, thrown on the WALL away from the light: draw into a mask, scale about (ox, oy), shift, blur,
    darken the frame there (only above ymax = the wall). Call BEFORE drawing the character itself."""
    g = np.zeros_like(f); draw_fn(g)
    m = (g.max(axis=2) > 0.02).astype(np.float32)
    M = np.float32([[sc, 0, ox - sc * ox + dx], [0, sc, oy - sc * oy + dy]])
    m = cv2.warpAffine(m, M, (W, H)); m = cv2.GaussianBlur(m, (0, 0), blur)
    m[int(ymax):] = 0
    f[:] = f * (1 - amt * m[..., None])


# ---------------- NEW PLACE: a 1960s LIVING ROOM ----------------
def set_room60(t=0.0, blur=4, top_y=1330, dim=0.0):
    def mk():
        f = _vgrad((236, 206, 130), (214, 176, 100), 0, top_y)                                 # mustard wallpaper
        for yy in range(0, top_y, 120):
            for xx in range(0 if (yy // 120) % 2 == 0 else 60, W, 120):
                P = np.array([(xx, yy - 30), (xx + 24, yy), (xx, yy + 30), (xx - 24, yy)], np.int32)
                cv2.polylines(f, [P], True, C((196, 150, 80)), 3, cv2.LINE_AA)
        for x0 in (20, 880):                                                                      # curtains
            cv2.rectangle(f, (x0, 260), (x0 + 180, top_y - 40), C((160, 90, 60)), -1, cv2.LINE_AA)
            for k in range(4): cv2.line(f, (x0 + 20 + 45 * k, 280), (x0 + 20 + 45 * k, top_y - 60), C((128, 70, 46)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (0, top_y), (W, H), C((150, 100, 60)), -1)                               # floor
        for yy in range(top_y + 40, H, 70): cv2.line(f, (0, yy), (W, yy), C((126, 82, 48)), 3, cv2.LINE_AA)
        cv2.ellipse(f, (540, top_y + 190), (420, 110), 0, 0, 360, C((180, 70, 60)), -1, cv2.LINE_AA)   # rug
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("room60", blur, top_y), mk).copy()
    if dim > 0: f *= (1 - 0.7 * dim)
    return inkify(f)


def sepia(f, amt=0.5):
    """a gentle 1960s photo tint (warm, lower contrast)."""
    g = f.mean(axis=2, keepdims=True)
    tone = g * np.array([1.08, 0.94, 0.74], np.float32) * 0.92 + 0.05
    f[:] = f * (1 - amt) + tone * amt
