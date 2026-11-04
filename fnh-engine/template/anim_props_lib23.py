# ================= anim_props_lib23.py (ep 23, 4 Nov): the MITHAI ink props + the live FUSE + live MOULD + the APARTMENT CORRIDOR + the MITHAI SHOP.
# ONE accent per video: MARIGOLD = fuses' sparks, titles, chips; WATER BLUE (lib22) = water; MOULD grey-green is a story colour (it only appears when something has gone off). Props: kalakand_el, rasgulla_el, rasmalai_el,
# sandesh_el, peda_el, boondi_el, kaju_ink_el, besan_el (each with mood + look), patakha_el (a firecracker), mould_el (a fuzzy character), tray_el, tag_el2 (best-before tag); live: fuse (a burning rope along any path), sweet_fuse (one standing on a sweet),
# coil (a long fuse wound up), poof (mould puff), fuzz (mould that grows, amt 0..1), roots_cut (cut-away sweet: fuzz on top, threads + hidden bacteria inside), gauge (a test tube of water), fuse_chart (a bar chart whose bars are fuses: THE list), scroll (a paper list that unrolls),
# dress (neighbour / boss / cousin accessories drawn over chub). Places: set_corridor(t, camx) (a Diwali apartment corridor, parallax strip; feet at y 1500), set_shop(t) + shop_front(f) (a mithai shop counter).
ACC = (232, 124, 34); ACC_S = (168, 76, 14); ACC_L = (252, 196, 110); ACC_XL = (254, 232, 196)
MOULD = (138, 168, 122); MOULD_S = (84, 118, 88); MOULD_L = (196, 214, 180)
ROPE = (150, 106, 70); ROPE_B = (70, 54, 48); SPARK = (255, 226, 110)
SCHEMES["marig"] = ((250, 222, 170), (254, 242, 214), (246, 208, 150), (0.9, 0.72, 0.5))
SCHEMES["mouldp"] = ((206, 220, 194), (236, 242, 226), (190, 208, 178), (0.62, 0.72, 0.58))
SCHEMES["coldp"] = ((196, 226, 244), (236, 248, 252), (176, 212, 238), (0.56, 0.72, 0.86))


def _block(d, w, h, top, side, seed, dep=44):
    """a sweet cut as a block seen slightly from above; returns the top face box."""
    m = 26
    _ink_poly(d, [(m, 70), (w - m, 70), (w - m, h - 16), (m, h - 16)], side, seed, INK_W - 1)
    _ink_poly(d, [(m + 30, 22), (w - m - 30, 22), (w - m, 70 + dep), (m, 70 + dep)], top, seed + 1, INK_W - 1)
    return (m, 22, w - m, 70 + dep)


def kalakand_el(mood=None, look=(0, 0), seed=31):
    """kalakand: a soft, grainy, creamy block with pistachio + a marigold petal."""
    def mk():
        w, h = 300, 220; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        _block(d, w, h, (254, 244, 214), (236, 216, 170), seed)
        for i in range(90):
            x, y = rng.uniform(62, 238), rng.uniform(32, 108); r_ = rng.uniform(1.5, 4); d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(232, 208, 156, 255))
        for i in range(30):
            x, y = rng.uniform(34, 266), rng.uniform(122, 196); r_ = rng.uniform(1.5, 3.4); d.ellipse(S(x - r_, y - r_, x + r_, y + r_), fill=(210, 184, 130, 255))
        for i in range(8):
            x, y = rng.uniform(70, 230), rng.uniform(36, 100); d.ellipse(S(x - 7, y - 4, x + 7, y + 4), fill=(124, 174, 96, 255), outline=INKC + (255,))
        _hatch_in(im, (190, 118, 274, 200), lambda q, S_: q.rectangle(S_(190, 118, 274, 200), fill=255))
        if mood: _face(d, S, 150, 150, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("kalak23", mood, look, seed), mk)


def rasgulla_el(mood=None, look=(0, 0), seed=32):
    def mk():
        w, h = 240, 230; im, d, S = _cv(w, h)
        _ink_ell(d, 120, 196, 96, 22, (244, 226, 170), seed + 2, INK_W - 2)                # the syrup puddle
        _ink_ell(d, 120, 112, 92, 90, (255, 252, 242), seed, INK_W - 1)
        _shade(im, lambda q, S_: q.ellipse(S_(30, 24, 210, 200), fill=255), lambda q, S_, c: q.ellipse(S_(90, 70, 260, 240), fill=c), (226, 214, 184), 150)
        d.arc(S(58, 44, 118, 104), 190, 270, fill=(255, 255, 255, 255), width=8 * SC3); d.ellipse(S(136, 70, 146, 80), fill=(230, 220, 196, 255)); d.ellipse(S(80, 150, 88, 158), fill=(230, 220, 196, 255))
        if mood: _face(d, S, 120, 118, 1.15, mood, look)
        return _done(im, w, h)
    return gcache(("rasg23", mood, look, seed), mk)


def rasmalai_el(mood=None, look=(0, 0), seed=33):
    def mk():
        w, h = 280, 190; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        _ink_ell(d, 140, 136, 130, 44, (250, 222, 140), seed + 1, INK_W - 1)
        _ink_ell(d, 140, 96, 92, 56, (254, 248, 230), seed, INK_W - 1)
        for i in range(9):
            x, y = 140 + rng.uniform(-70, 70), 90 + rng.uniform(-30, 30); d.ellipse(S(x - 5, y - 3, x + 5, y + 3), fill=((124, 174, 96, 255) if i % 2 else (232, 124, 34, 255)))
        if mood: _face(d, S, 140, 100, 0.95, mood, look)
        return _done(im, w, h)
    return gcache(("rasm23", mood, look, seed), mk)


def sandesh_el(mood=None, look=(0, 0), seed=34):
    def mk():
        w, h = 240, 190; im, d, S = _cv(w, h)
        P = [(120 + 100 * math.cos(a / 16 * 3.14 + 3.14) * (1 + 0.05 * math.sin(a * 2.2)), 150 + 118 * math.sin(a / 16 * 3.14 + 3.14)) for a in range(17)]
        _ink_poly(d, P + [(150, 172), (90, 172)], (252, 240, 214), seed, INK_W - 1)
        for a in (-50, -25, 0, 25, 50):
            aa = math.radians(a - 90); d.line(S(120 + 34 * math.cos(aa), 150 + 34 * math.sin(aa), 120 + 96 * math.cos(aa), 150 + 106 * math.sin(aa)), fill=(216, 196, 150, 255), width=3 * SC3)
        d.ellipse(S(110, 136, 130, 156), fill=(124, 174, 96, 255), outline=INKC + (255,))
        if mood: _face(d, S, 120, 110, 0.85, mood, look)
        return _done(im, w, h)
    return gcache(("sand23", mood, look, seed), mk)


def peda_el(mood=None, look=(0, 0), seed=35):
    def mk():
        w, h = 220, 180; im, d, S = _cv(w, h)
        _ink_ell(d, 110, 96, 92, 72, (230, 196, 146), seed, INK_W - 1)
        _shade(im, lambda q, S_: q.ellipse(S_(20, 26, 200, 166), fill=255), lambda q, S_, c: q.ellipse(S_(80, 70, 240, 200), fill=c), (196, 156, 104), 130)
        d.ellipse(S(92, 54, 128, 76), fill=(206, 168, 116, 255)); d.ellipse(S(102, 58, 118, 70), fill=(124, 174, 96, 255), outline=INKC + (255,))
        if mood: _face(d, S, 110, 108, 0.95, mood, look)
        return _done(im, w, h)
    return gcache(("peda23", mood, look, seed), mk)


def boondi_el(mood=None, look=(0, 0), seed=36):
    def mk():
        w, h = 230, 230; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        _ink_ell(d, 115, 115, 96, 94, (246, 150, 44), seed, INK_W)
        for i in range(120):
            a, r_ = rng.uniform(0, 6.28), 94 * math.sqrt(rng.uniform(0, 0.96)); x, y = 115 + r_ * math.cos(a), 115 + r_ * math.sin(a); c = (250, 178, 66, 255) if rng.uniform() < 0.55 else (224, 124, 30, 255)
            d.ellipse(S(x - 8, y - 8, x + 8, y + 8), fill=c, outline=(176, 88, 24, 255))
        if mood:
            d.ellipse(S(70, 74, 160, 160), fill=(250, 178, 66, 255)); _face(d, S, 115, 118, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("boondi23", mood, look, seed), mk)


def kaju_ink_el(mood=None, look=(0, 0), seed=37):
    """kaju katli: a thin diamond of cashew fudge with a patch of silver."""
    def mk():
        w, h = 300, 190; im, d, S = _cv(w, h)
        _ink_poly(d, [(16, 80), (150, 164), (284, 80), (284, 104), (150, 186), (16, 104)], (226, 200, 156), seed + 1, INK_W - 1)
        _ink_poly(d, [(150, 8), (284, 80), (150, 164), (16, 80)], (244, 228, 192), seed, INK_W - 1)
        _ink_poly(d, [(150, 30), (248, 82), (150, 140), (52, 82)], (232, 234, 234), seed + 2, 2, amp=2.2)
        d.line(S(110, 60, 170, 90), fill=(255, 255, 255, 255), width=3 * SC3); d.line(S(130, 106, 190, 76), fill=(205, 208, 208, 255), width=2 * SC3)
        if mood: _face(d, S, 150, 84, 0.9, mood, look)
        return _done(im, w, h)
    return gcache(("kaju23", mood, look, seed), mk)


def besan_el(mood=None, look=(0, 0), seed=38):
    """besan laddoo: a roasted-flour ball with an almond on top. The dry, smug survivor."""
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        _ink_ell(d, 120, 128, 100, 98, (226, 172, 88), seed, INK_W)
        _shade(im, lambda q, S_: q.ellipse(S_(20, 30, 220, 226), fill=255), lambda q, S_, c: q.ellipse(S_(90, 90, 280, 280), fill=c), (182, 122, 52), 130)
        for i in range(70):
            a, r_ = rng.uniform(0, 6.28), 90 * math.sqrt(rng.uniform()); x, y = 120 + r_ * math.cos(a), 128 + r_ * math.sin(a); e = rng.uniform(1.5, 3.2)
            d.ellipse(S(x - e, y - e, x + e, y + e), fill=(194, 136, 62, 255) if i % 2 else (242, 200, 124, 255))
        _ink_ell(d, 120, 32, 15, 25, (190, 134, 80), seed + 3, 3, amp=0.6)
        if mood:
            d.ellipse(S(76, 92, 164, 174), fill=(232, 182, 100, 255)); _face(d, S, 120, 128, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("besan23", mood, look, seed), mk)


def patakha_el(seed=39):
    """a Diwali firecracker: red paper tube, gold bands."""
    def mk():
        w, h = 170, 280; im, d, S = _cv(w, h)
        _ink_poly(d, [(36, 30), (134, 30), (134, 262), (36, 262)], (214, 52, 44), seed, INK_W)
        _ink_ell(d, 85, 30, 49, 14, (240, 110, 80), seed + 1, INK_W - 1)
        for y in (70, 222): d.rectangle(S(38, y, 132, y + 16), fill=(250, 206, 96, 255))
        d.polygon(S(85, 106, 112, 146, 85, 186, 58, 146), fill=(250, 206, 96, 255), outline=INKC + (255,))
        _hatch_in(im, (100, 44, 134, 262), lambda q, S_: q.rectangle(S_(100, 44, 134, 262), fill=255))
        return _done(im, w, h)
    return gcache(("patakha23", seed), mk)


def mould_el(mood="happy", look=(0, 0), seed=40):
    """the mould, as a fuzzy character: a tuft of soft spikes."""
    def mk():
        w, h = 240, 220; im, d, S = _cv(w, h); rng = np.random.default_rng(seed)
        for i in range(70):
            a = rng.uniform(0, 6.28); r0, r1 = 66, rng.uniform(88, 108); x0, y0, x1, y1 = 120 + r0 * math.cos(a), 116 + r0 * 0.86 * math.sin(a), 120 + r1 * math.cos(a), 116 + r1 * 0.86 * math.sin(a)
            d.line(S(x0, y0, x1, y1), fill=INKC + (255,), width=5 * SC3); d.line(S(x0, y0, x1 - 2 * math.cos(a), y1 - 2 * math.sin(a)), fill=MOULD + (255,), width=2 * SC3)
        _ink_ell(d, 120, 116, 80, 70, MOULD, seed, 3, amp=2.5)
        for i in range(26):
            a, r_ = rng.uniform(0, 6.28), 70 * math.sqrt(rng.uniform()); x, y = 120 + r_ * math.cos(a), 116 + r_ * 0.86 * math.sin(a); d.ellipse(S(x - 3, y - 3, x + 3, y + 3), fill=(MOULD_S if i % 2 else MOULD_L) + (255,))
        d.ellipse(S(82, 88, 158, 150), fill=MOULD_L + (255,))
        _face(d, S, 120, 118, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("mould23", mood, look, seed), mk)


def tag_el2(top="BEST BEFORE", day="6 NOV", s=1.0):
    def mk():
        w, h = 340, 210; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 20), (320, 20), (320, 190), (40, 190), (8, 105)], (254, 248, 230), 41, INK_W - 1)
        d.ellipse(S(34, 94, 54, 114), fill=INKC + (255,))
        return _done(im, w, h)
    return gcache(("tag23",), mk)


def tray_el(kind="barfi", seed=42):
    """a steel shop tray piled with sweets, seen from the front."""
    def mk():
        w, h = 460, 150; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 70), (446, 70), (420, 136), (40, 136)], (206, 212, 214), seed, INK_W - 1)
        d.line(S(40, 90, 420, 90), fill=(238, 242, 244, 255), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("tray23", kind, seed), mk)


def fuse(f, pts, k, t, w=12, spark=True, burnt=True):
    """a burning rope along pts: pts[0] = the sweet, pts[-1] = the free end. k 0..1 = how much has burnt away from the free end (1 = the spark reached the sweet). Returns the spark point."""
    P = np.array(pts, np.float32); seg = np.hypot(*(P[1:] - P[:-1]).T); cum = np.r_[0, np.cumsum(seg)]; L = cum[-1]
    kk = 1 - clamp(k); ln = L * kk; idx = int(np.searchsorted(cum, ln)); idx = max(1, min(idx, len(P) - 1))
    a_ = clamp((ln - cum[idx - 1]) / max(seg[idx - 1], 1e-3)); sp = P[idx - 1] + (P[idx] - P[idx - 1]) * a_
    Q = np.vstack([P[:idx], sp[None]]) if kk > 0 else P[:1]
    Qi = Q.astype(np.int32)
    if len(Qi) > 1:
        cv2.polylines(f, [Qi], False, C(INKC), w + 7, cv2.LINE_AA); cv2.polylines(f, [Qi], False, C(ROPE), w, cv2.LINE_AA)
        dist = 0.0
        for i in range(len(Q) - 1):                                                   # the twist of the rope
            a = Q[i]; b = Q[i + 1]; s_ = float(np.hypot(*(b - a)))
            for q in np.arange(0, s_, 16.0):
                c = a + (b - a) * (q / max(s_, 1e-3)); nx, ny = (b - a)[1] / max(s_, 1e-3), -(b - a)[0] / max(s_, 1e-3)
                cv2.line(f, (int(c[0] - nx * w * 0.4), int(c[1] - ny * w * 0.4)), (int(c[0] + nx * w * 0.4 + (b - a)[0] / max(s_, 1) * 6), int(c[1] + ny * w * 0.4 + (b - a)[1] / max(s_, 1) * 6)), C(ROPE_B), 2, cv2.LINE_AA)
    if spark and k < 1:
        rng = np.random.default_rng(int(t * 24) + 7); sx, sy = float(sp[0]), float(sp[1])
        glow(f, sx, sy, 60, (255, 190, 90), 0.5)
        for i in range(9):
            a = rng.uniform(0, 6.28); r_ = rng.uniform(10, 42); cv2.line(f, (int(sx), int(sy)), (int(sx + r_ * math.cos(a)), int(sy + r_ * math.sin(a))), C(SPARK if i % 2 else (255, 150, 60)), 3, cv2.LINE_AA)
        cv2.circle(f, (int(sx), int(sy)), 9, C((255, 250, 220)), -1, cv2.LINE_AA)
    return float(sp[0]), float(sp[1])


def sweet_fuse(f, x, y, L, k, t, curl=26, w=12, seed=1):
    """a fuse standing up on a sweet; (x, y) = where it enters the sweet."""
    pts = [(x + curl * math.sin(q * 3.6 + seed) * q, y - L * q) for q in np.linspace(0, 1, 18)]
    return fuse(f, pts, k, t, w)


def coil(f, cx, cy, r, turns=3.5, k=0.0, t=0.0, w=10, start=None):
    """a long fuse wound up on the floor: the month-long one. start = where the line comes in from. Spark at the outer free end."""
    pts = [] if start is None else [start]
    for q in np.linspace(0, 1, int(46 * turns / 3)):
        a = -1.57 + q * turns * 6.283; rr = 8 + r * (1 - q); pts.append((cx + rr * math.cos(a), cy + rr * 0.62 * math.sin(a)))
    pts = pts + pts[-1:]
    return fuse(f, pts[::-1], k, t, w)


def poof(f, x, y, t, t0, r=170, seed=5):
    """the fuse reached the sweet: a soft grey-green puff, no flame."""
    d = t - t0
    if d < 0 or d > 0.8: return
    k = eo(clamp(d / 0.45)); op = 1 - clamp((d - 0.3) / 0.5); rng = np.random.default_rng(seed); g = f.copy()
    for i in range(11):
        a = rng.uniform(0, 6.28); rr = r * k * rng.uniform(0.3, 1.0); R_ = int(rng.uniform(40, 86) * (0.5 + k)); xx, yy = int(x + rr * math.cos(a)), int(y + rr * 0.8 * math.sin(a) - 30 * k)
        cv2.circle(g, (xx, yy), R_ + 5, C(INKC), -1, cv2.LINE_AA)
    for i in range(11):
        rng2 = np.random.default_rng(seed);
    rng = np.random.default_rng(seed)
    for i in range(11):
        a = rng.uniform(0, 6.28); rr = r * k * rng.uniform(0.3, 1.0); R_ = int(rng.uniform(40, 86) * (0.5 + k)); xx, yy = int(x + rr * math.cos(a)), int(y + rr * 0.8 * math.sin(a) - 30 * k)
        cv2.circle(g, (xx, yy), R_, C(MOULD_L if i % 3 else MOULD), -1, cv2.LINE_AA)
    f[:] = f * (1 - op) + g * op


def fuzz(f, x, y, w, h, amt, t=0.0, seed=7, n=None):
    """mould that GROWS: tufts spread from a few spots across an ellipse (w, h) around (x, y) as amt goes 0 -> 1, and the hairs lengthen. It breathes a little."""
    amt = clamp(amt)
    if amt <= 0: return
    rng = np.random.default_rng(seed); n = n or max(26, int(w * 0.26))
    spots = [(rng.uniform(-0.6, 0.6), rng.uniform(-0.6, 0.6)) for _ in range(4)]
    for i in range(n):
        sp_ = spots[i % 4]; a, r_ = rng.uniform(0, 6.28), math.sqrt(rng.uniform()); px, py = r_ * math.cos(a), r_ * math.sin(a)
        dist = math.hypot(px - sp_[0], py - sp_[1]); born = dist / 1.8; vis = clamp((amt - born) / 0.35)
        L_ = rng.uniform(16, 38); hh = rng.integers(5, 9); xx, yy = x + px * w / 2, y + py * h / 2
        if vis <= 0: continue
        cv2.circle(f, (int(xx), int(yy)), int(12 * vis) + 3, C(MOULD_S), -1, cv2.LINE_AA); cv2.circle(f, (int(xx), int(yy)), int(10 * vis) + 1, C(MOULD), -1, cv2.LINE_AA)
        for j in range(hh):
            aa = -1.57 + rng.uniform(-1.1, 1.1) + 0.05 * math.sin(t * 3 + i); ll = L_ * vis * rng.uniform(0.6, 1.1); x1, y1 = xx + ll * math.cos(aa), yy + ll * math.sin(aa)
            cv2.line(f, (int(xx), int(yy)), (int(x1), int(y1)), C(MOULD_S if j % 2 else MOULD_L), 2, cv2.LINE_AA)
            cv2.circle(f, (int(x1), int(y1)), 3, C(MOULD_L if j % 2 else (232, 240, 222)), -1, cv2.LINE_AA)


def roots_cut(f, cx, cy, w, h, k, t, top=1.0, seed=9, bugs=True, bk=1.0):
    """a cut-away piece of a soft sweet: fuzz on top (top 0..1), root threads growing down inside (k 0..1), hidden bacteria (bk)."""
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)
    cv2.rectangle(f, (x0 + 10, y0 + 14), (x1 + 10, y1 + 14), C((130, 104, 84)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((252, 240, 214)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed)
    for i in range(220):
        xx, yy = rng.uniform(x0 + 8, x1 - 8), rng.uniform(y0 + 8, y1 - 8); cv2.circle(f, (int(xx), int(yy)), int(rng.uniform(1, 3)), C((226, 204, 160)), -1, cv2.LINE_AA)
    for i in range(14):                                                                   # the roots: branching threads from the top surface
        xx = x0 + 34 + (w - 68) * (i + 0.5) / 14 + rng.uniform(-10, 10); yy = float(y0); ang = 1.57 + rng.uniform(-0.25, 0.25); L_ = rng.uniform(0.55, 0.95) * h * clamp(k * 1.15); st_ = 22.0; dn = 0.0; P = [(xx, yy)]
        while dn < L_:
            ang += rng.uniform(-0.45, 0.45); ang = max(0.7, min(2.4, ang)); xx += st_ * math.cos(ang); yy += st_ * math.sin(ang); dn += st_; P.append((xx, yy))
            if rng.uniform() < 0.22:
                bb = ang + rng.choice([-0.9, 0.9]); B_ = [(xx, yy), (xx + 30 * math.cos(bb), yy + 30 * math.sin(bb)), (xx + 54 * math.cos(bb + 0.3), yy + 54 * math.sin(bb + 0.3))]
                cv2.polylines(f, [np.array(B_, np.int32)], False, C(MOULD_S), 3, cv2.LINE_AA)
        if len(P) > 1: cv2.polylines(f, [np.array(P, np.int32)], False, C(MOULD_S), 5, cv2.LINE_AA); cv2.polylines(f, [np.array(P, np.int32)], False, C(MOULD), 2, cv2.LINE_AA)
    if bugs and bk > 0:
        for i, (dx, dy) in enumerate(((-0.28, 0.2), (0.25, 0.32), (0.05, 0.1), (-0.1, 0.38), (0.34, 0.05))):
            comp(f, scale_el(germ_el("happy" if i % 2 else "n", seed=i + 2, ph=int(t * 6) % 4), 0.26), cx + dx * w, cy + dy * h, scale=bk)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 8, cv2.LINE_AA)
    if top > 0: fuzz(f, cx, y0 - 2, w, 34, top, t, seed + 1, n=int(w * 0.14))


def gauge(f, x, y, h, level, t, w=92, label=None, col=None):
    """a test tube of water; (x, y) = bottom centre. Level 0..1 sloshes a little."""
    x0, x1, y0 = int(x - w / 2), int(x + w / 2), int(y - h); col = col or WATER
    cv2.rectangle(f, (x0 + 7, y0 + 8), (x1 + 7, y + 8), C((150, 128, 110)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y), C((248, 250, 250)), -1, cv2.LINE_AA)
    if level > 0:
        yy = int(y - h * clamp(level) + 3 * math.sin(t * 3)); cv2.rectangle(f, (x0, yy), (x1, y), C(col), -1, cv2.LINE_AA); cv2.line(f, (x0, yy), (x1, yy), C(WATER_S), 4, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y), C(INKC), 7, cv2.LINE_AA)
    for q in (0.25, 0.5, 0.75): cv2.line(f, (x1 - 24, int(y - h * q)), (x1, int(y - h * q)), C(INKC), 4, cv2.LINE_AA)


CHART = [("SAME DAY", 1), ("2 DAYS", 2), ("4 DAYS", 4), ("7 DAYS", 7), ("30 DAYS", 30)]
CHART_L = {1: 60, 2: 130, 4: 230, 7: 340, 30: 430}
CHART_N = ["KALAKAND", "RASGULLA, RASMALAI, SANDESH", "MILK BARFI, PEDA, BOONDI LADDOO", "KAJU KATLI", "BESAN LADDOO"]


def _chart_icons(i):
    return {0: [(kalakand_el("sad"), 0.5, 0, 0)], 1: [(rasgulla_el(), 0.4, -60, 8), (rasmalai_el(), 0.36, 12, 24), (sandesh_el(), 0.36, 62, -20)],
            2: [(barfi_ink_el(), 0.42, -62, 16), (peda_el(), 0.42, 22, 24), (boondi_el(), 0.38, 62, -24)], 3: [(kaju_ink_el(), 0.6, 0, 6)], 4: [(besan_el("happy"), 0.58, 0, -4)]}[i]


def fuse_chart(f, t, t0s, y0=640, gap=166, x_ic=190, x_f=330, k=0.0, cur=None, chips=True, s_chip=38, fridge_tag=True):
    """THE LIST as a bar chart whose bars are fuses. t0s[i] = when row i pins in. The month row runs into a coil. cur = the row to highlight."""
    for i, (txt, dd) in enumerate(CHART):
        if t < t0s[i]: continue
        kk = pin(t, t0s[i]); y = y0 + i * gap; L = CHART_L[dd]
        if cur == i:
            cv2.rectangle(f, (70, int(y - gap * 0.47)), (1000, int(y + gap * 0.47)), C(ACC_XL), -1, cv2.LINE_AA); cv2.rectangle(f, (70, int(y - gap * 0.47)), (1000, int(y + gap * 0.47)), C(ACC_S), 5, cv2.LINE_AA)
        if dd < 30: fuse(f, [(x_f, y), (x_f + L * kk, y + 3 * math.sin(i + 1))], k, t + i, 11)
        else:
            cx_, cy_ = x_f + L + 90, y + 6
            fuse(f, [(x_f, y), (x_f + L * kk, y + 3)], 0, t + i, 11, spark=False)
            if kk > 0.5: coil(f, cx_, cy_, 80, 3.2, k, t + i, 9, (x_f + L, y + 3))
        for el, s_, dx, dy in _chart_icons(i): comp(f, scale_el(el, s_), x_ic + dx, y + dy, scale=kk)
        el_n = chip(CHART_N[i], INKC, MILK, 24); comp(f, el_n, x_f + el_n[1].shape[1] / 2 - 6, y - 50, scale=kk)
        if chips and dd < 30: comp(f, chip(txt, ACC_S if i else (176, 52, 44), MILK, s_chip), min(860, x_f + L + 150), y, scale=kk)
        elif chips: comp(f, chip(txt, ACC_S, MILK, s_chip), x_f + 200, y + 46, scale=kk)
        if i == 1 and fridge_tag: comp(f, chip("FRIDGE", WATER_S, MILK, 22), x_f + L + 300, y, scale=kk)


def scroll(f, x, y0, w, h, k, t=0.0):
    """a paper list that unrolls downwards from a rod at (x, y0). k 0..1."""
    hh = int(h * eo(clamp(k))); x0, x1 = int(x - w / 2), int(x + w / 2)
    if hh > 6:
        cv2.rectangle(f, (x0 + 8, y0 + 8), (x1 + 8, y0 + hh + 8), C((140, 118, 96)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x1, y0 + hh), C((254, 248, 232)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x1, y0 + hh), C(INKC), 6, cv2.LINE_AA)
        rng = np.random.default_rng(3)
        for j in range(int((hh - 30) / 44)):
            yy = y0 + 34 + j * 44; cv2.line(f, (x0 + 30, yy), (int(x0 + 30 + (w - 60) * rng.uniform(0.5, 1.0)), yy), C((150, 128, 110)), 7, cv2.LINE_AA)
    cv2.rectangle(f, (x0 - 16, y0 + hh - 13), (x1 + 16, y0 + hh + 13), C((226, 200, 150)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0 - 16, y0 + hh - 13), (x1 + 16, y0 + hh + 13), C(INKC), 6, cv2.LINE_AA)


def dress(f, x, y, s, kind, lean=0.0):
    """accessories over a chub (feet at x, y) so the neighbours read as other people on mute."""
    hx, hy = x + lean * 2 * s, y - 420 * s
    if kind == "aunty":
        cv2.circle(f, (int(hx + 6 * s), int(hy - 112 * s)), int(36 * s), C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(hx + 6 * s), int(hy - 112 * s)), int(27 * s), C((70, 50, 44)), -1, cv2.LINE_AA)
        cv2.circle(f, (int(hx), int(hy - 40 * s)), int(9 * s), C((200, 40, 60)), -1, cv2.LINE_AA)
    if kind == "cousin":
        cv2.ellipse(f, (int(hx), int(hy - 58 * s)), (int(96 * s), int(52 * s)), 0, 180, 360, C(INKC), -1, cv2.LINE_AA); cv2.ellipse(f, (int(hx), int(hy - 60 * s)), (int(86 * s), int(44 * s)), 0, 180, 360, C((70, 130, 190)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(hx + 40 * s), int(hy - 66 * s)), (int(hx + 140 * s), int(hy - 52 * s)), C((54, 104, 160)), -1, cv2.LINE_AA)
    if kind == "boss":
        for sg in (-1, 1): cv2.circle(f, (int(hx + sg * 36 * s), int(hy - 2 * s)), int(25 * s), C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
        cv2.line(f, (int(hx - 11 * s), int(hy - 2 * s)), (int(hx + 11 * s), int(hy - 2 * s)), C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
        cv2.ellipse(f, (int(hx), int(hy + 36 * s)), (int(42 * s), int(11 * s)), 0, 0, 360, C(INKC), -1, cv2.LINE_AA)
        P = np.array([(hx - 18 * s, y - 318 * s), (hx + 18 * s, y - 318 * s), (hx + 26 * s, y - 180 * s), (hx, y - 150 * s), (hx - 26 * s, y - 180 * s)], np.int32)
        cv2.fillPoly(f, [P], C((176, 52, 44)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def _corr_strip():
    """the apartment corridor, _LW wide: cream wall, doors with torans + nameplates, rangoli on the floor, tube lights."""
    cols = ((116, 150, 136), (176, 96, 76), (92, 120, 160), (150, 116, 80))
    a = np.zeros((H, _LW, 3), np.float32); a[:] = _vgrad((248, 232, 204), (236, 210, 170), 0, H)[0, 0]
    for y in range(H): a[y, :] = np.array(C(tuple(int(u + (v - u) * min(1.0, y / 1420)) for u, v in zip((250, 236, 208), (232, 204, 164)))), np.float32)
    n = _LW // 420
    for i in range(n):
        x = i * 420 + 210; c = cols[i % 4]
        cv2.rectangle(a, (x - 136, 640), (x + 136, 1424), C((96, 70, 54)), -1, cv2.LINE_AA)
        cv2.rectangle(a, (x - 116, 660), (x + 116, 1424), C(c), -1, cv2.LINE_AA)
        for yy, hh_ in ((700, 280), (1020, 340)): cv2.rectangle(a, (x - 86, yy), (x + 86, yy + hh_), C(tuple(int(u * 0.85) for u in c)), 5, cv2.LINE_AA)
        cv2.circle(a, (x + 90, 1060), 14, C((230, 190, 90)), -1, cv2.LINE_AA); cv2.circle(a, (x + 90, 1060), 14, C(INKC), 3, cv2.LINE_AA)
        for j in range(15):                                                      # toran of marigolds
            k = j / 14; xx = x - 140 + 280 * k; yy = 632 + 34 * math.sin(3.14 * k); cv2.circle(a, (int(xx), int(yy)), 16, C((246, 160, 40) if j % 2 else (250, 196, 60)), -1, cv2.LINE_AA)
        cv2.rectangle(a, (x + 170, 900), (x + 240, 960), C((250, 244, 228)), -1, cv2.LINE_AA); cv2.rectangle(a, (x + 170, 900), (x + 240, 960), C(INKC), 4, cv2.LINE_AA)
        cv2.circle(a, (x + 205, 880), 12, C((240, 200, 90)), -1, cv2.LINE_AA)
    a = cv2.GaussianBlur(a, (0, 0), 3.5)
    cv2.rectangle(a, (0, 1424), (_LW, H), C((206, 178, 140)), -1)
    for x in range(0, _LW, 150): cv2.line(a, (x, 1424), (x + 40, H), C((180, 150, 112)), 3, cv2.LINE_AA)
    cv2.line(a, (0, 1424), (_LW, 1424), C(INKC), 7, cv2.LINE_AA)
    for i in range(n):
        x = i * 420 + 210; yy = 1490
        for r_, c in ((62, (214, 54, 112)), (46, (250, 196, 60)), (30, (250, 244, 228)), (15, (60, 150, 130))): cv2.ellipse(a, (x, yy), (r_ * 2, int(r_ * 0.6)), 0, 0, 360, C(c), -1, cv2.LINE_AA)
    return a


def set_corridor(t=0.0, camx=0.0):
    s_ = gcache(("corr23",), _corr_strip); f = _roll(s_, camx).copy()
    for j in range(10):
        xx = ((j * 420 + 40) - camx) % _LW
        if xx < W + 60:
            h_ = 24 + 4 * math.sin(t * 12 + j * 2); cv2.ellipse(f, (int(xx), 1420), (22, 11), 0, 0, 180, C((170, 90, 50)), -1, cv2.LINE_AA); cv2.ellipse(f, (int(xx), int(1414 - h_ / 2)), (7, int(h_ / 2)), 0, 0, 360, C((255, 214, 90)), -1, cv2.LINE_AA); glow(f, xx, 1404, 80, (255, 190, 90), 0.12)
    return inkify(f, 0.06)


def _shop_bg():
    f = _vgrad((250, 226, 176), (238, 196, 136), 0, 1330)
    for yy in (610, 830):
        cv2.rectangle(f, (30, yy), (1050, yy + 24), C((130, 88, 58)), -1, cv2.LINE_AA)
        for j, x in enumerate(range(70, 1010, 150)):
            c = ((232, 124, 34), (214, 54, 112), (250, 196, 60), (92, 150, 130))[(j + yy // 10) % 4]; cv2.rectangle(f, (x, yy - 130), (x + 118, yy), C(c), -1, cv2.LINE_AA); cv2.rectangle(f, (x, yy - 130), (x + 118, yy), C(INKC), 5, cv2.LINE_AA); cv2.rectangle(f, (x + 48, yy - 130), (x + 70, yy), C((252, 226, 150)), -1)
    for j in range(22):
        k = j / 21; xx = 40 + 1000 * k; yy = 300 + 36 * math.sin(3.14 * k * 3) ** 2; cv2.circle(f, (int(xx), int(yy)), 20, C((246, 160, 40) if j % 2 else (250, 196, 60)), -1, cv2.LINE_AA)
    return _soft(f, 4).astype(np.float32)


def set_shop(t=0.0, dim=0.0):
    f = gcache(("shop23",), _shop_bg).copy()
    glow(f, 540, 420, 620, (255, 236, 190), 0.16 + 0.01 * math.sin(t * 2))
    if dim: f = f * (1 - dim)
    return inkify(f, 0.08)


def shop_front(f, y0=1130, t=0.0):
    """the glass counter: a steel top, a lit glass case, the floor panel."""
    ov = f.copy(); cv2.rectangle(ov, (0, y0), (W, 1500), C((226, 240, 240)), -1); f[:] = f * 0.45 + ov * 0.55
    cv2.rectangle(f, (0, y0 - 16), (W, y0 + 8), C((200, 208, 210)), -1, cv2.LINE_AA); cv2.line(f, (0, y0 - 16), (W, y0 - 16), C(INKC), 7, cv2.LINE_AA); cv2.line(f, (0, y0 + 8), (W, y0 + 8), C(INKC), 5, cv2.LINE_AA)
    cv2.rectangle(f, (0, 1500), (W, H), C((130, 86, 58)), -1); cv2.line(f, (0, 1500), (W, 1500), C(INKC), 8, cv2.LINE_AA)
    for x in (120, 960):
        cv2.line(f, (x, y0 + 40), (x - 40, 1460), C((255, 255, 255)), 5, cv2.LINE_AA)
