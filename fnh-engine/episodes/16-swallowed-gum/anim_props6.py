# ================= props for ep 16 (swallowed gum) — gum wad, bubble, toothpaste, corn kernel, birch-tar lump, stomach (3D-shaded),
# broom, bin, birch tree, museum pedestal, stone-age woman, body route. Built on the Chubby v2 light model (mat_shade / _Cv). =================
SCHEMES["flesh"] = ((120, 24, 52), (214, 84, 110), (110, 20, 46), (0.5, 0.1, 0.2))
SCHEMES["gumpink"] = ((255, 150, 190), (255, 214, 230), (246, 132, 176), (0.85, 0.45, 0.6))
SCHEMES["xray"] = ((10, 22, 46), (30, 64, 110), (8, 18, 40), (0.1, 0.25, 0.45))
GUM = (255, 132, 176); GUM_D = (190, 50, 104); GUM_H = (255, 220, 236)
TAR = (92, 52, 34); TAR_D = (34, 18, 12); TAR_H = (170, 118, 84)
CORN = (255, 200, 50); CORN_D = (210, 130, 10); CORN_H = (255, 246, 190)
STOM = (238, 120, 140); STOM_D = (150, 40, 70); STOM_H = (255, 200, 210)


def gum_wad_el(seed=1, w=230, h=170, bites=True, kind="satin", col=None):
    """a chewed lump of gum: blobby, satin-moist, with tooth dents."""
    base, dk, hi = col or (GUM, GUM_D, GUM_H)
    def mk():
        sc = 2; cv = _Cv(w, h, sc); rng = np.random.default_rng(seed)
        blobs = [(w / 2 + rng.uniform(-w * 0.18, w * 0.18), h / 2 + rng.uniform(-h * 0.12, h * 0.12), rng.uniform(0.22, 0.32) * w, rng.uniform(0.24, 0.34) * h) for _ in range(5)]
        m = cv.mask(lambda d, S: [d.ellipse(S(x - rx, y - ry, x + rx, y + ry), fill=255) for x, y, rx, ry in blobs])
        m = cv2.GaussianBlur(m, (0, 0), 4 * sc); m = np.clip((m - 0.5) * 4 + 0.5, 0, 1)
        mat_put(cv, m, base, dk, hi, kind, 5, 0.6, seed=seed)
        if bites:
            for i in range(4):
                x, y = w * (0.3 + 0.13 * i), h * (0.32 + 0.08 * math.sin(i * 2))
                bm = cv.mask(lambda d, S, x=x, y=y: d.arc(S(x - 16, y - 10, x + 16, y + 14), 200, 340, fill=255, width=5 * sc))
                cv.fill(dk, bm * (m > 0.5) * 0.7)
        return cv.done()
    return gcache(("gumwad", seed, w, h, bites, kind, base), mk)


def bubble_el(r=160):
    """big pink bubble-gum bubble: glossy, slightly see-through."""
    r = int(r)
    def mk():
        w = h = 2 * r + 30; sc = 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.ellipse(S(15, 15, w - 15, h - 15), fill=255))
        mat_put(cv, m, GUM, GUM_D, GUM_H, "gloss", 4, 0.3, seed=3)
        cv.a = cv.a * 0.93
        return cv.done()
    return gcache(("bubble", r), mk)


def splat(f, x, y, s, t, t0, seed=2):
    """pink gum splat (popped bubble) stuck on a face."""
    if t < t0: return
    k = pin(t, t0, 0.18); rng = np.random.default_rng(seed)
    for i in range(9):
        a = i / 9 * 2 * math.pi + rng.uniform(-0.2, 0.2); L = rng.uniform(60, 120) * s * k
        cv2.circle(f, (int(x + L * math.cos(a)), int(y + L * math.sin(a) * 0.8)), int(rng.uniform(16, 30) * s * k + 4), C(GUM_D), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x + L * math.cos(a)), int(y + L * math.sin(a) * 0.8)), int(rng.uniform(12, 24) * s * k), C(GUM), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(110 * s * k), int(80 * s * k)), 0, 0, 360, C(GUM), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x - 30 * s), int(y - 24 * s)), (int(30 * s * k), int(12 * s * k)), -20, 0, 360, C(GUM_H), -1, cv2.LINE_AA)


def toothpaste_el(squeeze=0.0):
    """toothpaste tube lying sideways, cap on the right; squeeze 0..1 pinches the back end."""
    q = round(clamp(squeeze) * 8) / 8
    def mk():
        w, h, sc = 520, 200, 2; cv = _Cv(w, h, sc)
        pinch = 30 * q
        m = cv.mask(lambda d, S: d.polygon(S(20, 40 + pinch, 400, 50, 400, 150, 20, 160 - pinch), fill=255))
        m = np.maximum(m, cv.mask(lambda d, S: d.rounded_rectangle(S(14, 30 + pinch, 40, 170 - pinch), 6 * sc, fill=255)))
        mat_put(cv, m, (240, 244, 250), (150, 170, 200), (255, 255, 255), "satin", 5, 0.5)
        st = cv.mask(lambda d, S: d.rectangle(S(150, 70, 330, 128), fill=255)) * (m > 0.5)
        cv.fill((40, 160, 120), st)
        cap = cv.mask(lambda d, S: d.rounded_rectangle(S(398, 64, 470, 136), 10 * sc, fill=255))
        mat_put(cv, cap, (60, 120, 220), (20, 50, 120), (160, 200, 255), "gloss", 5, 0.7)
        return cv.done()
    return gcache(("paste", q), mk)


def paste_ribbon(f, x, y, L, t):
    """white + mint striped paste coming out to the right of (x, y) with length L."""
    if L < 4: return
    pts = [(x + i, y + 10 * math.sin(i / 40 + t * 2) * min(1, i / 60)) for i in range(0, int(L), 6)]
    if len(pts) < 2: return
    a = np.array(pts, np.int32)
    cv2.polylines(f, [a], False, C(OUT3), 40, cv2.LINE_AA); cv2.polylines(f, [a], False, C((250, 252, 255)), 30, cv2.LINE_AA)
    cv2.polylines(f, [a], False, C((80, 200, 160)), 8, cv2.LINE_AA)


def corn_el():
    def mk():
        w, h, sc = 120, 140, 3; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.polygon(S(20, 30, 60, 12, 100, 30, 92, 92, 60, 128, 28, 92), fill=255))
        m = cv2.GaussianBlur(m, (0, 0), 3 * sc); m = np.clip((m - 0.5) * 4 + 0.5, 0, 1)
        mat_put(cv, m, CORN, CORN_D, CORN_H, "gloss", 4, 0.6)
        return cv.done()
    return gcache("corn3", mk)


def seed_el(col=(120, 80, 40)):
    def mk():
        w, h, sc = 70, 100, 3; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: d.ellipse(S(12, 10, 58, 90), fill=255))
        mat_put(cv, m, col, tuple(int(c * 0.5) for c in col), tuple(min(255, c + 80) for c in col), "satin", 4, 0.6)
        return cv.done()
    return gcache(("seed3", col), mk)


def tar_el(w=260, h=180):
    """chewed lump of birch tar (dark brown-black, matte, tooth marks)."""
    def mk():
        sc = 2; cv = _Cv(w, h, sc)
        m = cv.mask(lambda d, S: [d.ellipse(S(20, 30, w - 40, h - 20), fill=255), d.ellipse(S(w * 0.45, 20, w - 15, h - 40), fill=255)])
        m = cv2.GaussianBlur(m, (0, 0), 5 * sc); m = np.clip((m - 0.5) * 4 + 0.5, 0, 1)
        mat_put(cv, m, TAR, TAR_D, TAR_H, "satin", 5, 0.6, seed=7)
        for i in range(5):
            x = w * (0.25 + 0.11 * i); y = h * (0.35 + 0.05 * math.sin(i * 1.7))
            bm = cv.mask(lambda d, S, x=x, y=y: d.arc(S(x - 15, y - 9, x + 15, y + 13), 200, 340, fill=255, width=5 * sc))
            cv.fill((200, 150, 110), bm * (m > 0.5) * 0.55)
        return cv.done()
    return gcache(("tar", w, h), mk)


def stomach3_el(w=420, h=440, cut=True):
    """3D-shaded stomach (J shape); cut=True shows a darker inside opening for things to sit in."""
    def mk():
        sc = 2; cv = _Cv(w, h, sc)
        def shp(d, S):
            d.ellipse(S(40, 90, w - 40, h - 60), fill=255)
            d.rounded_rectangle(S(90, 10, 160, 170), 30 * sc, fill=255)
            d.polygon(S(w - 110, h - 150, w - 10, h - 110, w - 30, h - 20, w - 120, h - 60), fill=255)
        m = cv.mask(shp); m = cv2.GaussianBlur(m, (0, 0), 3 * sc); m = np.clip((m - 0.5) * 4 + 0.5, 0, 1)
        mat_put(cv, m, STOM, STOM_D, STOM_H, "satin", 6, 0.45, seed=4)
        if cut:
            im_ = cv.mask(lambda d, S: d.ellipse(S(90, 150, w - 90, h - 110), fill=255))
            cv.fill((110, 20, 48), im_ * 0.92)
            for k in range(4):
                fm = cv.mask(lambda d, S, k=k: d.arc(S(110 + 10 * k, 170 + 22 * k, w - 110 - 10 * k, h - 120 - 4 * k), 20, 160, fill=255, width=6 * sc))
                cv.fill((170, 50, 84), fm * im_ * 0.8)
        return cv.done()
    return gcache(("stom3", w, h, cut), mk)


def broom_el():
    def mk():
        w, h, sc = 160, 520, 2; cv = _Cv(w, h, sc)
        st = cv.mask(lambda d, S: d.rounded_rectangle(S(70, 10, 90, 380), 8 * sc, fill=255))
        mat_put(cv, st, (190, 130, 80), (110, 70, 40), (240, 200, 150), "satin", 4, 0.5)
        br = cv.mask(lambda d, S: d.polygon(S(52, 370, 108, 370, 150, 510, 10, 510), fill=255))
        mat_put(cv, br, (240, 200, 90), (170, 120, 40), (255, 240, 180), "matte", 4, 0.5)
        for i in range(9):
            ln = cv.mask(lambda d, S, i=i: d.line(S(60 + i * 5, 380, 20 + i * 15, 505), fill=255, width=2 * sc)) * (br > 0.5)
            cv.fill((170, 120, 40), ln * 0.8)
        return cv.done()
    return gcache("broom", mk)


def bin_el(open_=0.0):
    q = round(clamp(open_) * 6) / 6
    def mk():
        w, h, sc = 300, 380, 2; cv = _Cv(w, h, sc)
        body = cv.mask(lambda d, S: d.polygon(S(40, 110, 260, 110, 240, 370, 60, 370), fill=255))
        mat_put(cv, body, (90, 170, 150), (30, 90, 80), (170, 230, 210), "satin", 5, 0.5)
        ang = -60 * q
        cx, cy = 40, 100
        pts = [(40, 80), (262, 80), (262, 112), (40, 112)]
        rp = [(cx + (x - cx) * math.cos(math.radians(ang)) - (y - cy) * math.sin(math.radians(ang)), cy + (x - cx) * math.sin(math.radians(ang)) + (y - cy) * math.cos(math.radians(ang))) for x, y in pts]
        lid = cv.mask(lambda d, S: d.polygon([v * sc for p in rp for v in p], fill=255))
        mat_put(cv, lid, (110, 190, 170), (40, 110, 100), (200, 250, 230), "gloss", 5, 0.6)
        return cv.done()
    return gcache(("bin", q), mk)


def birch(f, x, y, s=1.0, t=0.0):
    """birch tree: white trunk with dark marks + soft leaf clumps (drawn live, lit from the low sun)."""
    tw = int(34 * s); top = int(y - 760 * s)
    cv2.rectangle(f, (int(x - tw / 2 - 4), top), (int(x + tw / 2 + 4), int(y)), C(OUT3), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - tw / 2), top), (int(x + tw / 2), int(y)), C((240, 236, 226)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x + tw * 0.1), top), (int(x + tw / 2), int(y)), C((200, 190, 180)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(int(x))
    for i in range(14):
        yy = rng.uniform(top + 40, y - 20); cv2.line(f, (int(x - tw / 2), int(yy)), (int(x - tw / 2 + rng.uniform(8, tw)), int(yy)), C((40, 34, 30)), max(2, int(5 * s)), cv2.LINE_AA)
    for i in range(7):
        lx = x + rng.uniform(-170, 170) * s + 6 * math.sin(t * 1.3 + i); ly = top + rng.uniform(-60, 220) * s
        cv2.circle(f, (int(lx), int(ly)), int(rng.uniform(70, 110) * s), C((150, 170, 70) if i % 2 else (190, 190, 80)), -1, cv2.LINE_AA)


def pedestal(f, x, y, t=0.0):
    """museum pedestal + glass case (top at y)."""
    cv2.rectangle(f, (int(x - 150), int(y)), (int(x + 150), int(y + 420)), C(OUT3), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 142), int(y + 6)), (int(x + 142), int(y + 420)), C((70, 60, 70)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 142), int(y + 6)), (int(x - 60), int(y + 420)), C((96, 84, 96)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 170), int(y - 14)), (int(x + 170), int(y + 10)), C((150, 30, 50)), -1, cv2.LINE_AA)


def glass_case(f, x, y, w=320, h=300):
    ov = f.copy()
    cv2.rectangle(ov, (int(x - w / 2), int(y - h)), (int(x + w / 2), int(y)), C((200, 230, 255)), -1, cv2.LINE_AA)
    f[:] = f * 0.9 + ov * 0.1
    cv2.rectangle(f, (int(x - w / 2), int(y - h)), (int(x + w / 2), int(y)), C((230, 245, 255)), 4, cv2.LINE_AA)
    cv2.line(f, (int(x - w / 2 + 30), int(y - h + 20)), (int(x - w / 2 + 80), int(y - 30)), C((255, 255, 255)), 6, cv2.LINE_AA)


def stone_woman(f, x, y, s=1.0, **kw):
    """Chubby-style stone-age woman: long dark hair, fur-brown top (drawn like mom(), own colours)."""
    hx, hy = head_pos(x, y, s, kw.get("bob", 0.0), kw.get("lean", 0.0))
    cv2.ellipse(f, (int(hx), int(hy + 40 * s)), (int(116 * s), int(150 * s)), 0, 0, 360, C(OUT3), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy + 40 * s)), (int(108 * s), int(142 * s)), 0, 0, 360, C((60, 36, 26)), -1, cv2.LINE_AA)
    return chub(f, x, y, s, shirt=(150, 104, 66), **kw)


def body_route_pts(cx=540, top=600, s=1.0):
    """stops of the gut route inside a big see-through Chubby: mouth -> food pipe -> stomach -> small intestine -> large intestine -> out."""
    P = [(cx, top), (cx, top + 210 * s), (cx + 90 * s, top + 360 * s), (cx - 80 * s, top + 470 * s), (cx + 60 * s, top + 560 * s),
         (cx - 60 * s, top + 640 * s), (cx + 120 * s, top + 700 * s), (cx + 120 * s, top + 790 * s), (cx, top + 840 * s)]
    return P


ROUTE_NAMES = ["MOUTH", "FOOD PIPE", "STOMACH", "SMALL INTESTINE", "", "", "LARGE INTESTINE", "", "OUT"]


def gum_stick_el():
    return gum_el()
