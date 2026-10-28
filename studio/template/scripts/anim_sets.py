# ================= full-frame story sets + framing (exec'd after anim_cine.py / anim_mascot3d.py) =================
# Owner, 27 Oct: the best story reels use the FULL frame — real rooms and streets edge to edge, big characters, the camera
# changes every shot (wide, medium, close-up, over-the-shoulder). These sets fill 1080x1920 with perspective, texture and light.
#   f = set_view("study", t, zoom=1.0, cx=540, cy=960, blur=0)   -> full-frame background (cached base, camera move, DOF blur)
#   say(f, "YOU TOLD OAK", y=1240)      -> big punchy caption (white, thick black stroke), centred, fits the safe width
#   part_badge(f, "PART 1", "HOW MONOPOLY BEGAN")  -> series badge + title bar (top right, inside the safe zone)
# Sets: street, study, parlor, office, store, dusk, airport (set_view also sets the matching character light).
# FX: smoke(f, t), embers(f, t), glow_eyes(f, x, y). Framing: fg_hand(f, x, y, s) = big blurred foreground hand.
# HUD: hud_clock(f, "DAY 1", "6:14 AM", "ROUTE 2"), hud_rule(f, 1, "NEVER SELL THE PATENT", y), hud_timer(f, secs),
#      hud_choice(f, "MOST OF YOU SAID", "SELL IT", y). Characters: person(...) in anim_mascot3d.py (guy() = the hero).


def _scv(c): return tuple(float(v) / 255 for v in c)


def _sfloor(f, y0, vx, col_a, col_b, tile=True, n_lines=13, n_rows=11, line_col=None, planks=False, seed=3):
    """perspective floor from y0 to the bottom; vanishing point (vx, y0 - 520)"""
    vy = y0 - 520
    k = np.clip((_yy - y0) / (H - y0), 0, 1)[..., None]
    base = _mix(_c(col_a), _c(col_b), k ** 0.9)
    m = (_yy >= y0)[..., None]
    f[:] = np.where(m, base, f)
    lc = _c(line_col) if line_col else _c(col_a) * 0.72
    ov = np.zeros((H, W), np.float32)
    for i in range(-n_lines, n_lines + 1):                              # receding lines
        xb = vx + i * (W / n_lines) * 1.6; xt = vx + (xb - vx) * (y0 - vy) / (H - vy)
        cv2.line(ov, (int(xt), y0), (int(xb), H), 1.0, 2, cv2.LINE_AA)
    if tile:
        for j in range(1, n_rows + 1):                                  # cross lines, closer together near the horizon
            yy_ = int(y0 + (H - y0) * (j / n_rows) ** 1.9); cv2.line(ov, (0, yy_), (W, yy_), 1.0, 2, cv2.LINE_AA)
    if planks:
        r = _rng(seed)
        for j in range(60):
            yy_ = int(y0 + (H - y0) * r.random() ** 1.6); xx_ = int(r.integers(0, W)); ln = int(20 + 120 * (yy_ - y0) / (H - y0))
            cv2.line(ov, (xx_, yy_), (xx_ + 4, yy_ + ln), 1.0, 2, cv2.LINE_AA)
    f[:] = f * (1 - (ov * 0.5)[..., None] * m) + lc * (ov * 0.5)[..., None] * m


def _srect(f, x0, y0, x1, y1, hi, lo, out=None, ow=3):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if X1 <= X0 or Y1 <= Y0: return
    g = np.linspace(0, 1, Y1 - Y0)[:, None, None]
    f[Y0:Y1, X0:X1] = _mix(_c(hi), _c(lo), g)
    if out is not None: cv2.rectangle(f, (x0, y0), (x1, y1), _scv(out), ow, cv2.LINE_AA)


def _swindow(f, x0, y0, x1, y1, frame=(250, 246, 240), glass_top=(120, 170, 220), glass_bot=(60, 90, 140), mull=True):
    _srect(f, x0 - 14, y0 - 14, x1 + 14, y1 + 14, frame, tuple(int(v * 0.8) for v in frame), (60, 44, 40), 3)
    _srect(f, x0, y0, x1, y1, glass_top, glass_bot)
    # diagonal reflection streak
    pts = np.array([[x0 + (x1 - x0) * 0.15, y0], [x0 + (x1 - x0) * 0.42, y0], [x0 + (x1 - x0) * 0.05, y1], [x0 - (x1 - x0) * 0.22, y1]], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [pts], (1, 1, 1), cv2.LINE_AA)
    sub = (slice(max(0, y0), min(H, y1)), slice(max(0, x0), min(W, x1))); f[sub] = f[sub] * 0.86 + ov[sub] * 0.14
    if mull:
        cv2.line(f, ((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1), _scv(frame), 10, cv2.LINE_AA)
        cv2.line(f, (x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2), _scv(frame), 10, cv2.LINE_AA)


def _sbush(f, x, y, r, seed=1):
    rr = _rng(seed)
    for i in range(7):
        cx, cy, ri = x + rr.integers(-r // 2, r // 2), y + rr.integers(-r // 3, r // 4), int(r * (0.45 + 0.25 * rr.random()))
        cv2.circle(f, (int(cx), int(cy)), ri + 3, _scv((24, 60, 30)), -1, cv2.LINE_AA)
        cv2.circle(f, (int(cx), int(cy)), ri, _scv((46, 130, 60)), -1, cv2.LINE_AA)
        cv2.circle(f, (int(cx - ri * 0.3), int(cy - ri * 0.3)), int(ri * 0.5), _scv((92, 182, 84)), -1, cv2.LINE_AA)


def _sbooks(f, x0, x1, ybase, hmax, seed):
    r = _rng(seed); x = x0
    pal = [(150, 34, 40), (34, 70, 140), (40, 110, 70), (210, 160, 60), (90, 50, 120), (230, 230, 220), (180, 90, 40), (30, 30, 40)]
    while x < x1 - 14:
        w = int(r.integers(16, 34)); h = int(hmax * (0.62 + 0.38 * r.random())); c = pal[int(r.integers(0, len(pal)))]
        if x + w > x1: break
        _srect(f, x, ybase - h, x + w, ybase, tuple(min(255, int(v * 1.15)) for v in c), tuple(int(v * 0.7) for v in c), (30, 20, 20), 2)
        cv2.line(f, (x + 3, ybase - h + 2), (x + 3, ybase - 2), _scv(tuple(min(255, int(v * 1.35)) for v in c)), 2, cv2.LINE_AA)
        if r.random() < 0.4: cv2.rectangle(f, (x + 3, ybase - int(h * 0.75)), (x + w - 3, ybase - int(h * 0.68)), _scv((240, 210, 120)), -1, cv2.LINE_AA)
        x += w + int(r.integers(0, 3))


def _sglow(f, x, y, rad, col, amt):
    g = np.exp(-(((_xx - x) / rad) ** 2 + ((_yy - y) / rad) ** 2))[..., None]
    f[:] = 1 - (1 - f) * (1 - _c(col) * g * amt)


def _set_base(name):
    f = np.zeros((H, W, 3), np.float32)
    if name == "street":
        _srect(f, 0, 0, W, 1150, (238, 214, 190), (214, 182, 156))
        for (a, b) in ((0, 250), (600, 900)):                         # windows upstairs
            _swindow(f, a + 40, 30, b - 40, 230)
        _srect(f, 0, 300, W, 330, (250, 240, 228), (220, 204, 188), (90, 70, 60), 2)   # ledge
        for (a, b) in ((-40, 260), (760, 1120)):                      # shop windows
            _swindow(f, a, 420, b, 900, frame=(236, 226, 214), glass_top=(150, 140, 150), glass_bot=(90, 84, 100), mull=False)
        _srect(f, 340, 440, 740, 1000, (222, 40, 40), (170, 24, 30), (60, 20, 20), 3)  # door frame
        _srect(f, 380, 480, 700, 1000, (250, 236, 236), (226, 200, 204), (60, 30, 30), 2)
        _srect(f, 410, 600, 670, 700, (250, 200, 200), (236, 170, 176))                # door sign panel
        for k, y in enumerate((1000, 1050, 1100)):                     # steps
            _srect(f, 0, y, W, y + 50, (232, 200, 180), (200, 160, 140), (110, 80, 70), 2)
        _sbush(f, 130, 920, 120, 1); _sbush(f, 960, 920, 120, 2)
        _srect(f, 40, 960, 230, 1000, (230, 210, 190), (200, 170, 150), (90, 70, 60), 2)
        _srect(f, 860, 960, 1060, 1000, (230, 210, 190), (200, 170, 150), (90, 70, 60), 2)
        f[1150:] = 0; _sfloor(f, 1150, 540, (226, 168, 140), (190, 118, 96), line_col=(160, 100, 84))
        _sglow(f, 540, 600, 700, (255, 220, 170), 0.18)
    elif name == "study":
        _srect(f, 0, 0, W, 1280, (122, 74, 48), (92, 52, 34))     # wooden wall
        for sx0, sx1 in ((-30, 520), (560, 1110)):                    # two bookcases
            _srect(f, sx0, 40, sx1, 1300, (110, 64, 38), (82, 44, 26), (40, 22, 14), 4)
            for k, yb in enumerate(range(260, 1300, 250)):
                _srect(f, sx0 + 16, yb - 230, sx1 - 16, yb, (70, 40, 24), (54, 30, 18))
                _sbooks(f, sx0 + 24, sx1 - 24, yb - 4, 200, seed=k * 7 + sx0 + 100)
                _srect(f, sx0 + 8, yb, sx1 - 8, yb + 22, (160, 104, 64), (118, 72, 44), (40, 22, 14), 2)
        f[1280:] = 0; _sfloor(f, 1280, 540, (150, 92, 56), (100, 58, 34), tile=False, planks=True, line_col=(76, 44, 28))
        _sglow(f, 820, 300, 520, (255, 210, 140), 0.25)
    elif name == "parlor":
        _srect(f, 0, 0, W, 260, (150, 90, 50), (120, 70, 40))     # ceiling beams
        for x in range(-40, W + 40, 220): _srect(f, x, 0, x + 70, 260, (120, 72, 40), (90, 52, 30), (50, 30, 20), 2)
        _srect(f, 0, 260, W, 900, (246, 196, 96), (232, 168, 74))     # warm wallpaper
        for x in range(0, W, 60): cv2.line(f, (x, 260), (x, 900), _scv((226, 160, 70)), 6, cv2.LINE_AA)
        _srect(f, 0, 900, W, 1240, (200, 60, 40), (160, 40, 28))     # brick wainscot
        for y in range(900, 1240, 34):
            off = 0 if ((y - 900) // 34) % 2 == 0 else 40
            cv2.line(f, (0, y), (W, y), _scv((120, 30, 20)), 2, cv2.LINE_AA)
            for x in range(off, W, 80): cv2.line(f, (x, y), (x, y + 34), _scv((120, 30, 20)), 2, cv2.LINE_AA)
        for (a, b) in ((80, 300), (400, 640), (740, 960)):            # picture frames
            _srect(f, a, 420, b, 700, (120, 80, 50), (80, 50, 30), (40, 24, 14), 3)
            _srect(f, a + 16, 436, b - 16, 684, (110, 110, 100), (70, 70, 64))
        cv2.line(f, (150, 260), (150, 330), _scv((40, 30, 30)), 4, cv2.LINE_AA); cv2.circle(f, (150, 350), 26, _scv((255, 250, 230)), -1, cv2.LINE_AA)
        _sglow(f, 150, 350, 260, (255, 230, 170), 0.55)
        f[1240:] = 0; _sfloor(f, 1240, 540, (200, 110, 60), (150, 74, 40), tile=False, planks=True, line_col=(110, 56, 30))
    elif name == "office":
        _srect(f, 0, 0, W, 1250, (226, 232, 240), (200, 208, 220))
        _swindow(f, 80, 140, 1000, 1000, frame=(60, 66, 80), glass_top=(120, 180, 240), glass_bot=(200, 220, 240), mull=False)
        m, win = _skyline(9, 200, 520)
        sky = f.copy(); city = _mix(_c((70, 100, 160)), _c((140, 170, 210)), 0.4)
        mm = (cv2.GaussianBlur(m, (0, 0), 2) * ((_xx > 80) & (_xx < 1000) & (_yy > 140) & (_yy < 1000)))[..., None]
        f[:] = _mix(f, city, mm * 0.9)
        cv2.line(f, (540, 140), (540, 1000), _scv((60, 66, 80)), 14, cv2.LINE_AA)
        f[1250:] = 0; _sfloor(f, 1250, 540, (180, 186, 200), (130, 136, 150), line_col=(110, 116, 130))
        _sglow(f, 540, 500, 700, (255, 245, 230), 0.15)
    elif name == "store":
        _srect(f, 0, 0, W, 1200, (248, 248, 244), (226, 228, 222))
        for sx0, sx1 in ((-60, 380), (700, 1140)):                    # shelves in perspective (simplified)
            for k, yb in enumerate(range(380, 1200, 200)):
                _srect(f, sx0, yb - 180, sx1, yb, (240, 240, 236), (220, 220, 214))
                r = _rng(k + sx0 + 100)
                for x in range(sx0 + 10, sx1 - 40, 44):
                    c = [(230, 60, 50), (40, 120, 220), (250, 190, 40), (60, 170, 90), (240, 120, 30)][int(r.integers(0, 5))]
                    _srect(f, x, yb - 120, x + 36, yb - 4, tuple(min(255, int(v * 1.1)) for v in c), tuple(int(v * 0.75) for v in c), (40, 40, 40), 2)
                _srect(f, sx0, yb, sx1, yb + 16, (200, 200, 196), (170, 170, 166), (80, 80, 80), 2)
        f[1200:] = 0; _sfloor(f, 1200, 540, (236, 236, 230), (200, 200, 194), line_col=(170, 170, 164))
        _sglow(f, 540, 200, 600, (255, 255, 240), 0.2)
    elif name == "dusk":
        _dusk(f)
        return np.clip(f, 0, 1).astype(np.float32)
    elif name == "airport":
        return _airport_base()
    _atmos(f, name)
    # soft room light falloff + corner occlusion
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


_FLOOR = dict(street=1150, study=1280, parlor=1240, office=1250, store=1200, dusk=1250, airport=1180)
SET_LIGHT = dict(street="day", study="warm", parlor="warm", office="cool", store="day", dusk="dusk", airport="day")
SETS = tuple(_FLOOR)


def _atmos(f, name):
    """turn flat vector rooms into lit spaces: plaster/wood texture, occlusion where wall meets floor, a soft light pool"""
    y0 = _FLOOR[name]
    n = _noise(H, W, 180, 11 + len(name)); n2 = _noise(H, W, 26, 3 + len(name), octaves=2)
    tex = 0.95 + 0.07 * n + 0.03 * n2
    f *= tex[..., None]
    f *= (1 - 0.30 * np.exp(-((_yy - y0) / 46) ** 2) * (_yy < y0 + 30) - 0.12 * np.clip((y0 - _yy) / 500, 0, 1) * (_yy < y0))[..., None]
    floor = (_yy >= y0)[..., None]
    sheen = np.exp(-(((_xx - 540) / 520) ** 2 + ((_yy - (y0 + 180)) / 160) ** 2))[..., None] * floor
    f[:] = f + sheen * 0.10
    top = np.clip(1 - _yy / 500, 0, 1)[..., None]
    f *= 1 - 0.18 * top


def _ridge(seed, base, amp, tree_w, n_trees, rough=10):
    """y of a tree line per x column (conifers = triangles), smaller y = taller"""
    r = _rng(seed); x = np.arange(W, dtype=np.float32); top = np.full(W, base, np.float32)
    for _ in range(n_trees):
        xi = r.uniform(-60, W + 60); hi = amp * (0.55 + 0.45 * r.random()); wi = tree_w * (0.7 + 0.6 * r.random())
        top = np.minimum(top, base - hi * np.clip(1 - np.abs(x - xi) / wi, 0, 1) ** 0.9)
    top += (r.random(W).astype(np.float32) - 0.5) * rough
    return cv2.GaussianBlur(top[None], (0, 0), 1.2)[0]


def _dusk(f):
    """open field at dusk: violet-to-amber sky, low sun on the right, layered hazy tree lines, warm-lit grass, ground fog"""
    y0 = _FLOOR["dusk"]
    k = np.clip(_yy / y0, 0, 1)[..., None]
    top, mid, low = _c((40, 38, 96)), _c((150, 70, 120)), _c((255, 156, 84))
    f[:] = np.where(k < 0.5, _mix(top, mid, k / 0.5), _mix(mid, low, np.clip((k - 0.5) / 0.5, 0, 1) ** 0.8))
    n = _noise(H, W, 300, 5); cl = np.clip((n - 0.5) * 3.2, 0, 1) * np.exp(-((_yy - 560) / 300) ** 2)
    f[:] = _mix(f, _c((248, 140, 120)), (cl * 0.5)[..., None])
    _sglow(f, 790, 1040, 560, (255, 170, 90), 0.75); _sglow(f, 790, 1090, 170, (255, 236, 190), 0.95)
    sky_low = _c((240, 150, 110))
    for seed, base, amp, tw, nt, col, haze in ((21, 1150, 120, 90, 26, (110, 60, 96), 0.55), (22, 1210, 200, 70, 34, (66, 34, 64), 0.32),
                                               (23, 1262, 300, 60, 30, (34, 20, 40), 0.12)):
        rg = _ridge(seed, base, amp, tw, nt)
        m = (_yy >= rg[None, :]).astype(np.float32)
        m = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
        c = _mix(_c(col), sky_low, haze)
        rim = np.exp(-np.clip(_yy - rg[None, :], 0, None) / 6)[..., None] * np.exp(-((_xx - 790) / 380) ** 2)[..., None]
        layer = c + rim * _c((255, 170, 90)) * 0.55
        f[:] = f * (1 - m) + layer * m
    g = (_yy >= y0)[..., None]
    gk = np.clip((_yy - y0) / (H - y0), 0, 1)[..., None]
    grass = _mix(_c((176, 120, 62)), _c((30, 46, 34)), gk ** 0.7)
    grass = grass + np.exp(-(((_xx - 790) / 360) ** 2 + ((_yy - y0) / 120) ** 2))[..., None] * _c((255, 160, 80)) * 0.35
    f[:] = np.where(g, grass, f)
    r = _rng(31)
    for _ in range(2600):
        y = y0 + (H - y0) * r.random() ** 1.5; x = r.uniform(0, W); d = (y - y0) / (H - y0)
        ln = 6 + 46 * d; lean = r.uniform(-0.5, 0.5) * ln
        sh = 0.55 + 0.6 * r.random()
        c = _mix(_c((150, 104, 56)), _c((40, 60, 40)), d ** 0.6) * sh
        cv2.line(f, (int(x), int(y)), (int(x + lean), int(y - ln)), tuple(float(v) for v in np.clip(c, 0, 1)), max(1, int(1 + 3 * d)), cv2.LINE_AA)
    fog = np.exp(-((_yy - (y0 + 10)) / 70) ** 2)[..., None] * (0.7 + 0.3 * _noise(H, W, 220, 8)[..., None])
    f[:] = _mix(f, _c((236, 170, 150)), fog * 0.45)
    f *= (1 - 0.35 * np.clip(1 - _yy / 420, 0, 1))[..., None]


_SMOKE = {}


def smoke(f, t, y0=900, y1=1500, col=(30, 22, 34), op=0.55, speed=18.0, seed=4):
    """drifting dark smoke / mist band (horror, mystery, 'something is coming')"""
    if seed not in _SMOKE: _SMOKE[seed] = _noise(H, W * 2, 200, seed, octaves=4)
    n = _SMOKE[seed]; off = int(t * speed) % W
    m = n[:, off:off + W]
    band = np.clip((_yy - y0) / 160, 0, 1) * np.clip((y1 - _yy) / 260, 0, 1)
    a = (np.clip((m - 0.38) * 2.2, 0, 1) * band * op)[..., None]
    f[:] = f * (1 - a) + _c(col) * a


def embers(f, t, n=40, seed=7, col=(255, 190, 110), y0=300, y1=1700, size=4.0, op=0.8):
    """floating glowing particles (fireflies / embers / dust in light)"""
    r = _rng(seed)
    ov = np.zeros((H, W), np.float32)
    for i in range(n):
        x0, ys, sp, ph = r.uniform(0, W), r.uniform(y0, y1), r.uniform(10, 40), r.uniform(0, 6.3)
        x = x0 + 30 * math.sin(t * 0.7 + ph); y = y1 - ((y1 - ys + sp * t) % (y1 - y0))
        fl = 0.55 + 0.45 * math.sin(t * 3.1 + ph * 2)
        cv2.circle(ov, (int(x), int(y)), int(size * (0.6 + 0.8 * r.random())), fl, -1, cv2.LINE_AA)
    g = cv2.GaussianBlur(ov, (0, 0), size * 1.6) * 2.2 + ov
    f[:] = 1 - (1 - f) * (1 - (np.clip(g * op, 0, 1)[..., None] * _c(col)))


def glow_eyes(f, x, y, s=1.0, col=(255, 40, 30), op=1.0):
    """two glowing eyes in the dark (the 'someone is watching' beat)"""
    ov = np.zeros((H, W), np.float32)
    for dx in (-30, 30): cv2.ellipse(ov, (int(x + dx * s), int(y)), (int(14 * s), int(7 * s)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
    g = np.clip(cv2.GaussianBlur(ov, (0, 0), 14 * s) * 2.5 + ov, 0, 1) * op
    f[:] = 1 - (1 - f) * (1 - g[..., None] * _c(col))
    f[:] = f * (1 - ov[..., None] * op) + ov[..., None] * op * _c((255, 230, 200))


def set_view(name, t=0.0, zoom=1.0, cx=W / 2, cy=H / 2, blur=0.0, drift=4.0):
    """full-frame set with a camera: zoom/centre for wide→close framing, slow drift, optional depth blur (close-ups)"""
    if "set_light" in globals(): set_light(SET_LIGHT.get(name, "day"))
    base = gcache(("set", name), lambda: _set_base(name))
    s = zoom * (1.0 + 0.004 * math.sin(t * 0.5))
    M = cv2.getRotationMatrix2D((cx, cy), 0, s); M[0, 2] += W / 2 - cx + drift * math.sin(t * 0.35); M[1, 2] += H / 2 - cy
    f = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return cv2.GaussianBlur(f, (0, 0), blur) if blur > 0.3 else f


def say(f, text, y=1240, size=150, col=(255, 255, 255), t=None, t0=None, max_w=800):
    """big punchy caption (condensed, white, thick black stroke + soft shadow) centred at x=540"""
    def mk():
        fn = font(F_ANTON, size); tw = fn.getlength(text); sw = max(6, size // 13)
        wpx, hpx = int(tw + 4 * sw + 40), int(size * 1.5)
        im = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((wpx // 2 + 6, hpx // 2 + 10), text, font=fn, fill=(0, 0, 0, 150), anchor="mm",
                                                                            stroke_width=sw, stroke_fill=(0, 0, 0, 150))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8)))
        ImageDraw.Draw(im).text((wpx // 2, hpx // 2), text, font=fn, fill=tuple(col) + (255,), anchor="mm", stroke_width=sw, stroke_fill=(12, 12, 16, 255))
        return el_from(im)
    el = gcache(("say", text, size, col), mk)
    s = min(1.0, max_w / el[1].shape[1])
    if t is not None and t0 is not None:
        k = clamp((t - t0) / 0.18)
        if k <= 0: return
        s *= 1.25 - 0.25 * eo(k)
    x_, y = safe_xy(el, 540, y, min(1.0, max_w / el[1].shape[1]))
    comp(f, el, x_, y, scale=s)


def part_badge(f, part="PART 1", title=None, x=760, y=330):
    """series badge (red pill) + optional dark title bar under it; stays inside the right safe margin"""
    comp(f, gcache(("badge", part), lambda: _badge_el(part)), x, y)
    if title: comp(f, gcache(("btitle", title), lambda: _title_el(title)), 540 + 100, y + 70)


def _badge_el(part):
    fn = font(F_ANTON, 64); tw = fn.getlength(part); w, h = int(tw + 60), 92
    im = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, w + 5, h + 5], h // 2, fill=(255, 255, 255, 255))
    d.rounded_rectangle([10, 10, w + 1, h + 1], h // 2, fill=(226, 36, 44, 255))
    d.text(((w + 12) // 2, (h + 12) // 2), part, font=fn, fill=(255, 255, 255, 255), anchor="mm")
    return el_from(im)


def _title_el(title):
    fn = font(F_ANTON, 40); tw = fn.getlength(title); w, h = int(min(600, tw + 50)), 64   # centred at x 640: stays left of the UI (x < 940)
    while tw + 50 > w and fn.size > 24: fn = font(F_ANTON, fn.size - 2); tw = fn.getlength(title)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 14, fill=(18, 18, 24, 230), outline=(90, 90, 100, 255), width=2)
    d.text((w // 2, h // 2), title, font=fn, fill=(255, 255, 255, 255), anchor="mm")
    return el_from(im)


# ---------------- framing: big foreground hand (depth + 'you are there') ----------------
def fg_hand(f, x, y, s=2.2, ang=0.0, who="hero", blur=5.0, op=1.0):
    """open hand reaching up into frame from the bottom edge; (x, y) = palm centre, ang = tilt in degrees"""
    L = _look(who); ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    T = lambda u, v: (x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
    fg = _Fig(x - 330 * s, y - 330 * s, x + 330 * s, y + 360 * s, s)
    sleeve = L["top"]
    fg.capsule(T(0, 330), T(0, 150), 150 * s, sleeve, r0=60 * s)
    fg.ellipse(T(0, 140), (88 * s, 30 * s), _mtone(sleeve, 0.85), ang=ang, r0=20 * s)
    fg.capsule(T(-6, 150), T(0, 60), 120 * s, L["skin"], r0=55 * s, gloss=0.05)
    fg.ellipse(T(0, 0), (96 * s, 104 * s), L["skin"], ang=ang, r0=80 * s, gloss=0.06, soft=0.2)
    for (bu, bv), (tu, tv) in (((-64, -56), (-92, -190)), ((-22, -76), (-30, -244)), ((22, -76), (28, -240)), ((62, -56), (84, -188))):
        fg.capsule(T(bu, bv), T(tu, tv), 46 * s, L["skin"], gloss=0.06)
        nu, nv = tu + (bu - tu) * 0.08, tv + (bv - tv) * 0.08
        fg.ellipse(T(nu, nv + 6), (11 * s, 9 * s), _mtone(L["skin"], 1.12), ang=ang, ow=1, ao=0, r0=4 * s)
    fg.capsule(T(84, 30), T(160, -54), 50 * s, L["skin"], gloss=0.06)
    fg.line(T(-50, 10), T(40, -30), 4 * s, _mtone(L["skin"], 0.6), op=0.4)
    fg.line(T(-40, 50), T(50, 10), 4 * s, _mtone(L["skin"], 0.6), op=0.35)
    fg.comp(f, op, blur=blur)


# ---------------- HUD pieces (story-reel overlays) ----------------
def _stxt_el(text, size, col=(255, 255, 255), fpath=None, stroke=0, scol=(10, 10, 14)):
    fn = font(fpath or F_ANTON, size); tw = int(fn.getlength(text)) + 4 * stroke + 8
    im = Image.new("RGBA", (tw, int(size * 1.35) + 2 * stroke), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((tw // 2, im.size[1] // 2), text, font=fn, fill=tuple(col) + (255,), anchor="mm", stroke_width=stroke, stroke_fill=tuple(scol) + (255,))
    return im


def hud_clock(f, top="DAY 1", mid="6:14 AM", sub=None, x=72, y=272, op=1.0):
    """top-left story clock panel (inside the safe zone)"""
    def mk():
        a = _stxt_el(top, 46, (255, 206, 60)); b = _stxt_el(mid, 86); c = _stxt_el(sub, 40, (210, 214, 224)) if sub else None
        w = max(a.size[0], b.size[0], c.size[0] if c else 0) + 56; h = 30 + a.size[1] + b.size[1] - 18 + (c.size[1] - 10 if c else 0) + 14
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 22, fill=(14, 14, 20, 196), outline=(255, 255, 255, 70), width=2)
        d.ellipse([w - 34, 18, w - 18, 34], fill=(240, 40, 40, 255))
        yy = 14; im.alpha_composite(a, (28, yy)); yy += a.size[1] - 12; im.alpha_composite(b, (24, yy)); yy += b.size[1] - 14
        if c: im.alpha_composite(c, (28, yy))
        return el_from(im)
    el = gcache(("hclock", top, mid, sub), mk)
    comp(f, el, x, y + el[1].shape[0] / 2, op=op, anchor="l")


def hud_rule(f, n, text, y=430, op=1.0, t=None, t0=None):
    """red 'RULE #n' chip + white pill with the rule, centred at x=540"""
    def mk():
        a = _stxt_el(f"RULE #{n}", 50); b = _stxt_el(text, 50, (20, 20, 26))
        h = max(a.size[1], b.size[1]) + 8; wa = a.size[0] + 34; wb = min(b.size[0] + 40, 860 - wa)
        im = Image.new("RGBA", (wa + wb + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([4, 4, wa + wb + 4, h + 4], h // 2, fill=(255, 255, 255, 250))
        d.rounded_rectangle([4, 4, wa + 4, h + 4], h // 2, fill=(228, 34, 42, 255))
        im.alpha_composite(a, (4 + (wa - a.size[0]) // 2, 4 + (h - a.size[1]) // 2))
        bb = b if b.size[0] <= wb - 20 else b.resize((wb - 20, int(b.size[1] * (wb - 20) / b.size[0])), Image.LANCZOS)
        im.alpha_composite(bb, (4 + wa + (wb - bb.size[0]) // 2, 4 + (h - bb.size[1]) // 2))
        return el_from(im)
    el = gcache(("hrule", n, text), mk); s = 1.0
    if t is not None and t0 is not None:
        k = clamp((t - t0) / 0.2)
        if k <= 0: return
        s = 0.85 + 0.15 * eback(k)
    x_, y = safe_xy(el, 540, y, 1.0)
    comp(f, el, x_, y, scale=s, op=op)


def hud_timer(f, secs, x=540, y=330, col=(255, 44, 44), op=1.0):
    """red digital countdown (glowing), e.g. the 'you have 30 seconds' beat"""
    secs = max(0, int(secs)); txt = f"{secs // 60:02d}:{secs % 60:02d}"
    def mk():
        im = _stxt_el(txt, 130, col)
        pad = 40; big = Image.new("RGBA", (im.size[0] + 2 * pad, im.size[1] + 2 * pad), (0, 0, 0, 0))
        d = ImageDraw.Draw(big); d.rounded_rectangle([pad - 26, pad - 6, big.size[0] - pad + 26, big.size[1] - pad + 6], 24, fill=(10, 8, 10, 205),
                                                     outline=(col[0], col[1], col[2], 120), width=3)
        gl = Image.new("RGBA", big.size, (0, 0, 0, 0)); gl.alpha_composite(im, (pad, pad)); gl = gl.filter(ImageFilter.GaussianBlur(10))
        big = Image.alpha_composite(big, gl); big.alpha_composite(im, (pad, pad))
        return el_from(big)
    comp(f, gcache(("htimer", txt, col), mk), x, y, op=op)


def hud_choice(f, label="MOST OF YOU SAID", choice="SELL IT", y=1420, col=(36, 186, 88), op=1.0, t=None, t0=None):
    """audience-choice callback: small caps label + coloured pill (series / comments loop)"""
    def mk():
        a = _stxt_el(label, 54, stroke=5); b = _stxt_el(choice, 76)
        wb = b.size[0] + 70; hb = b.size[1] + 6
        w = max(a.size[0], wb) + 10; h = a.size[1] + hb + 6
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        im.alpha_composite(a, ((w - a.size[0]) // 2, 0))
        x0 = (w - wb) // 2; d.rounded_rectangle([x0, a.size[1], x0 + wb, a.size[1] + hb], hb // 2, fill=tuple(col) + (255,), outline=(255, 255, 255, 255), width=4)
        im.alpha_composite(b, (x0 + 35, a.size[1] + 3))
        return el_from(im)
    el = gcache(("hchoice", label, choice, col), mk); s = min(1.0, 800 / el[1].shape[1]); x_, y = safe_xy(el, 540, y, s)
    if t is not None and t0 is not None:
        k = clamp((t - t0) / 0.22)
        if k <= 0: return
        s *= 0.8 + 0.2 * eback(k)
    comp(f, el, x_, y, scale=s, op=op)


# ---------------- airport departure hall (Hoover video, 28 Oct 2026): glass wall + parked jet, apron, check-in desks ----------------
def _airport_base():
    f = np.zeros((H, W, 3), np.float32)
    _srect(f, 0, 0, W, 1180, (150, 196, 240), (230, 236, 246))                 # sky through the glass wall
    m, win = _skyline(17, 60, 170)
    city = _c((150, 176, 210)); mm = (cv2.GaussianBlur(m, (0, 0), 2) * (_yy < 900) * (_yy > 600))[..., None]
    f[:] = _mix(f, city, mm * 0.6)
    _srect(f, 0, 860, W, 980, (120, 124, 134), (96, 100, 110))                   # apron
    for x in range(-40, W, 160): cv2.line(f, (x, 930), (x + 90, 930), _scv((250, 220, 80)), 5, cv2.LINE_AA)
    comp(f, plane_el(980), 560, 760)
    for x in range(0, W + 1, 270): cv2.line(f, (x, 0), (x, 1180), _scv((60, 66, 78)), 16, cv2.LINE_AA)   # mullions
    for y in (300, 620): cv2.line(f, (0, y), (W, y), _scv((60, 66, 78)), 10, cv2.LINE_AA)
    _srect(f, 0, 980, W, 1180, (226, 222, 214), (206, 200, 190), (90, 90, 96), 2)  # check-in desks
    for x0 in (40, 400, 760):
        _srect(f, x0, 1000, x0 + 280, 1180, (64, 92, 150), (44, 66, 116), (30, 30, 40), 3)
        _srect(f, x0 + 30, 1030, x0 + 250, 1070, (250, 250, 246), (230, 230, 224))
    f[1180:] = 0; _sfloor(f, 1180, 540, (236, 236, 240), (176, 180, 190), line_col=(160, 164, 176))
    _sglow(f, 540, 400, 700, (255, 250, 236), 0.2)
    _atmos(f, "airport")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)
