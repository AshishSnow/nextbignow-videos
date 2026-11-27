# ================= anim_props_lib71.py (was ep 71 anim_props6.py) (ep 71, 27 Nov): "Does vitamin C stop a cold?" — ACCENT = CITRUS ORANGE (the orange, the juice, the
# tablet, the 1970 book, the 'vitamin C' words). The cold virus keeps its lib44 olive; everything else = the ink palette.
# NEW PLACE: set_shop70(t, blur, dim) + shop70_front(f, top_y) = a 1970 BOOKSHOP: mustard + avocado walls, wooden shelves of 70s book spines left + right,
#   a big shop window onto a pale street with a hanging BOOKS sign, a round paper ceiling lamp (warm pool), a brown carpet, a display table in front
#   (drawn AFTER the people) with a pyramid of the hit book that shrinks as people grab it.
# NEW PROPS (ink): orange_el(mood, look, half, leaf, bite) (a navel orange with dimples + leaf, or a cut half with 9 segments), shield_ink_el(crack)
#   (a heater shield with a C), tab_el (a big vitamin-C tablet), book70_el (the 1970 'VITAMIN C' book), medal_ink_el (a gold prize medal on a ribbon),
#   shoe_el / ski_el / army_helmet_el (the three extreme-stress groups as icons), bib(f, ...) (a race number on Chubby's chest), pile_el (a stack of trial
#   papers), cold_bar(f, ...) (a cold as a row of 7 day blocks; trim = the 'a bit sooner' slice falls off), risk_bars(f, ...) (two bars, the second halves).
ACC = (250, 146, 34); ACC_S = (190, 88, 14); ACC_L = (255, 204, 132); ACC_XL = (255, 234, 204)   # lib71 sets ACC to citrus orange: your anim_props6 overrides it
OJ = (252, 170, 46); OJ_S = (214, 118, 20)
LEAF = (96, 170, 84); LEAF_S = (52, 112, 56)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
STEEL = (206, 212, 220)
SRC_COCH = "Source: Cochrane review (Hemila & Chalker, 2013)"
SRC_NIH = "Source: NIH Office of Dietary Supplements; Cochrane 2013"
SRC_POP = "Source: Popular Science; Pauling, 1970"
SC3 = 3
SHOP_TOP = 1340


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- NEW PLACE: the 1970 BOOKSHOP ----------------
SPINE_COLS = [(214, 160, 60), (150, 160, 70), (196, 96, 40), (120, 76, 48), (236, 206, 140), (90, 120, 110), (176, 70, 56), (230, 180, 90)]


def set_shop70(t=0.0, blur=4, dim=0.0, top_y=SHOP_TOP):
    def mk():
        f = _vgrad((232, 204, 140), (210, 176, 110), 0, top_y)
        rng = np.random.default_rng(710)
        # wallpaper: 70s rounded stripes
        for x in range(0, W, 120):
            cv2.rectangle(f, (x + 40, 0), (x + 80, top_y), C((222, 190, 122)), -1)
        # the shop window (middle, top) onto a pale street
        x0, y0, x1, y1 = 300, 330, 780, 900
        out = _vgrad((196, 220, 230), (232, 236, 228), y0, y1)
        f[y0:y1, x0:x1] = out[y0:y1, x0:x1]
        for (bx, bw, bh, c) in ((320, 140, 300, (214, 196, 170)), (480, 120, 380, (200, 180, 150)), (620, 150, 260, (220, 204, 176))):
            cv2.rectangle(f, (bx, y1 - bh), (bx + bw, y1), C(c), -1)
            for wy in range(y1 - bh + 30, y1 - 40, 70):
                for wx in range(bx + 16, bx + bw - 24, 40): cv2.rectangle(f, (wx, wy), (wx + 20, wy + 34), C((180, 200, 214)), -1)
        cv2.rectangle(f, (x0, y0), (x1, y1), C((120, 76, 40)), 22, cv2.LINE_AA)
        cv2.line(f, ((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1), C((120, 76, 40)), 14, cv2.LINE_AA)
        cv2.rectangle(f, (x0 - 14, y0 - 14), (x1 + 14, y1 + 14), C(INKC), 5, cv2.LINE_AA)
        # shelves left + right, full of 70s spines
        for (sx0, sx1) in ((0, 250), (830, W)):
            cv2.rectangle(f, (sx0, 240), (sx1, top_y), C((140, 92, 52)), -1)
            for sy in range(300, top_y - 60, 190):
                cv2.rectangle(f, (sx0, sy + 150), (sx1, sy + 170), C((104, 66, 36)), -1)
                xx = sx0 + 12
                while xx < sx1 - 30:
                    bw = int(rng.uniform(20, 38)); bh = int(rng.uniform(110, 148)); c = SPINE_COLS[int(rng.integers(0, len(SPINE_COLS)))]
                    tilt = 0 if rng.uniform() > 0.12 else 1
                    cv2.rectangle(f, (xx, sy + 150 - bh), (xx + bw, sy + 150), C(c), -1)
                    cv2.rectangle(f, (xx, sy + 150 - bh), (xx + bw, sy + 150), C(INKC), 2, cv2.LINE_AA)
                    cv2.line(f, (xx + 4, sy + 150 - bh + 20), (xx + bw - 4, sy + 150 - bh + 20), C((250, 240, 214)), 3)
                    xx += bw + 3 + 10 * tilt
            cv2.rectangle(f, (sx0, 240), (sx1, top_y), C(INKC), 5, cv2.LINE_AA)
        # floor carpet
        cv2.rectangle(f, (0, top_y), (W, H), C((150, 96, 60)), -1)
        for yy in range(top_y + 20, H, 36): cv2.line(f, (0, yy), (W, yy), C((138, 88, 54)), 4)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("shop70", blur, top_y), mk).copy()
    # hanging BOOKS sign + the round paper lamp (live sway)
    sw = 6 * math.sin(t * 1.3)
    cv2.line(f, (540, 0), (int(540 + sw), 180), C(INKC), 4, cv2.LINE_AA)
    cv2.ellipse(f, (int(540 + sw), 210), (90, 56), 0, 0, 360, C((252, 238, 206)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(540 + sw), 210), (90, 56), 0, 0, 360, C(INKC), 4, cv2.LINE_AA)
    for k_ in (-40, 0, 40): cv2.ellipse(f, (int(540 + sw), 210), (90, 56 - abs(k_) // 2), 0, 0, 360, C((230, 210, 170)), 2, cv2.LINE_AA)
    glow(f, 540 + sw, 260, 600, (255, 220, 150), 0.14)
    if dim > 0: f *= (1 - 0.6 * dim)
    return inkify(f)


def shop70_front(f, top_y=SHOP_TOP, left=1.0, x=540, w=760, px=None, ps=0.5):
    """the display table drawn AFTER the people (they stand behind it); left 0..1 = how much of the book pyramid is left."""
    cv2.rectangle(f, (int(x - w / 2), top_y), (int(x + w / 2), H), C((168, 110, 62)), -1)
    cv2.rectangle(f, (int(x - w / 2), top_y), (int(x + w / 2), top_y + 34), C((196, 136, 80)), -1)
    cv2.rectangle(f, (int(x - w / 2), top_y), (int(x + w / 2), H + 10), C(INKC), 5, cv2.LINE_AA)
    for xx in range(int(x - w / 2) + 60, int(x + w / 2), 120): cv2.line(f, (xx, top_y + 60), (xx, H), C((150, 96, 52)), 3)
    book_pyramid(f, x if px is None else px, top_y + 6, left, ps)


def book_pyramid(f, x, base_y, left=1.0, s=0.5):
    """rows 4-3-2-1 of the book standing on the table; left < 1 removes books from the top down."""
    el = scale_el(book70_el(), s); bw = 172 * s; bh = 236 * s
    slots = [(r, i) for r in range(4) for i in range(4 - r)]
    keep = int(round(len(slots) * clamp(left)))
    for r, i in slots[:keep]:
        n = 4 - r
        bx = x - (n - 1) * bw / 2 + i * bw
        by = base_y - bh / 2 - r * (bh - 8)
        comp(f, el, bx, by)


# ---------------- INK PROPS ----------------
def orange_el(mood=None, look=(0, 0), half=False, leaf=True, bite=0.0, seed=711):
    def mk():
        w, h = 260, 270; im, d, S = _cv(w, h); cx, cy, R = 130, 150, 100
        if half:
            _ink_ell(d, cx, cy, R, R * 0.9, ACC, seed, INK_W, n=30, amp=1.6)
            _ink_ell(d, cx, cy, R - 12, R * 0.9 - 12, (255, 248, 230), seed + 1, INK_W - 3, n=28, amp=1.0)
            _ink_ell(d, cx, cy, R - 22, R * 0.9 - 22, ACC_L, seed + 2, INK_W - 3, n=28, amp=1.0)
            for a in range(0, 360, 40):
                aa = math.radians(a + 10)
                d.line(S(cx, cy, cx + (R - 22) * math.cos(aa), cy + (R * 0.9 - 22) * math.sin(aa)), fill=(255, 248, 230, 255), width=4 * SC3)
            d.ellipse(S(cx - 9, cy - 8, cx + 9, cy + 8), fill=(255, 248, 230, 255))
            for a in range(20, 360, 40):
                aa = math.radians(a + 10); rr = (R - 50)
                d.ellipse(S(cx + rr * math.cos(aa) - 5, cy + rr * 0.9 * math.sin(aa) - 3, cx + rr * math.cos(aa) + 5, cy + rr * 0.9 * math.sin(aa) + 3), fill=(255, 236, 190, 255))
        else:
            _ink_ell(d, cx, cy, R, R * 0.96, ACC, seed, INK_W, n=30, amp=1.8)
            _shade(im, lambda q, S_: q.ellipse(S_(cx - R, cy - R, cx + R, cy + R), fill=255),
                   lambda q, S_, c: q.ellipse(S_(cx - 20, cy - 40, cx + R + 60, cy + R + 40), fill=c), ACC_S, 110)
            _hatch_in(im, (cx + 20, cy - 30, cx + R, cy + R), lambda q, S_: q.ellipse(S_(cx - 10, cy - 50, cx + R, cy + R), fill=255), -40, 10, 26)
            rng = np.random.default_rng(seed)
            for _ in range(26):                                                   # peel dimples
                a = rng.uniform(0, 2 * math.pi); r = R * math.sqrt(rng.uniform(0.05, 0.8))
                px, py = cx + r * math.cos(a), cy + r * math.sin(a)
                d.ellipse(S(px - 2.5, py - 2, px + 2.5, py + 2), fill=ACC_S + (150,))
            d.ellipse(S(cx - 62, cy - 70, cx - 22, cy - 46), fill=(255, 240, 210, 170))
            if bite > 0:
                for (bx, by) in ((cx + R * 0.8, cy - 30), (cx + R * 0.9, cy + 10), (cx + R * 0.78, cy + 46)):
                    d.ellipse(S(bx - 30 * bite, by - 26 * bite, bx + 30 * bite, by + 26 * bite), fill=(0, 0, 0, 0))
            if mood: _face(d, S, cx - 4, cy + 4, 1.15, mood, look)
        if leaf and not half:
            d.line(S(cx, cy - R + 4, cx + 6, cy - R - 16), fill=INKC + (255,), width=5 * SC3)
            _ink_poly(d, [(cx + 6, cy - R - 14), (cx + 40, cy - R - 44), (cx + 74, cy - R - 30), (cx + 40, cy - R - 8)], LEAF, seed + 5, INK_W - 2, amp=1.0)
            d.line(S(cx + 10, cy - R - 16, cx + 64, cy - R - 30), fill=LEAF_S + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("orange71", mood, look, half, leaf, round(bite, 2), seed), mk)


def shield_ink_el(crack=0.0, seed=712):
    def mk():
        w, h = 220, 260; im, d, S = _cv(w, h)
        P = [(20, 24), (110, 10), (200, 24), (196, 120), (164, 196), (110, 248), (56, 196), (24, 120)]
        _ink_poly(d, P, (230, 234, 240), seed, INK_W, amp=1.2)
        _ink_poly(d, [(44, 44), (110, 34), (176, 44), (172, 118), (146, 178), (110, 218), (74, 178), (48, 118)], ACC_XL, seed + 1, INK_W - 3, amp=1.0)
        _hatch_in(im, (110, 20, 200, 250), lambda q, S_: q.polygon(S_(*sum(P[1:7], ())), fill=255), -40, 10, 30)
        fn = font(F_BLACK, 120 * SC3)
        d.text((110 * SC3, 128 * SC3), "C", font=fn, fill=ACC + (255,), anchor="mm", stroke_width=3 * SC3, stroke_fill=INKC + (255,))
        if crack > 0:
            pts = [(110, 14), (96, 70), (126, 110), (100, 160), (120, 210)]
            n = max(2, int(len(pts) * crack + 0.5))
            d.line(_P(pts[:n]), fill=INKC + (255,), width=6 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("shield71", round(crack, 2), seed), mk)


def tab_el(seed=713):
    def mk():
        w, h = 180, 180; im, d, S = _cv(w, h)
        _ink_ell(d, 90, 90, 74, 74, ACC_L, seed, INK_W, n=26, amp=1.0)
        _ink_ell(d, 90, 90, 56, 56, ACC_XL, seed + 1, INK_W - 3, n=24, amp=0.8)
        fn = font(F_BLACK, 70 * SC3)
        d.text((90 * SC3, 92 * SC3), "C", font=fn, fill=ACC_S + (255,), anchor="mm")
        for a in range(0, 360, 60):
            aa = math.radians(a); d.ellipse(S(90 + 64 * math.cos(aa) - 3, 90 + 64 * math.sin(aa) - 3, 90 + 64 * math.cos(aa) + 3, 90 + 64 * math.sin(aa) + 3), fill=ACC_S + (200,))
        return _done(im, w, h)
    return gcache(("tab71", seed), mk)


def book70_el(seed=714):
    """the 1970 hit book (generic cover: a big orange sun + VITAMIN C)."""
    def mk():
        w, h = 180, 244; im, d, S = _cv(w, h)
        _ink_poly(d, [(12, 10), (170, 8), (172, 236), (10, 238)], (246, 236, 206), seed, INK_W - 1, amp=0.8)
        d.rectangle(S(12, 10, 26, 236), fill=ACC_S + (255,))
        _ink_ell(d, 98, 104, 46, 46, ACC, seed + 1, INK_W - 3, n=22, amp=0.8)
        for a in range(0, 360, 30):
            aa = math.radians(a); d.line(S(98 + 54 * math.cos(aa), 104 + 54 * math.sin(aa), 98 + 66 * math.cos(aa), 104 + 66 * math.sin(aa)), fill=ACC_S + (255,), width=4 * SC3)
        fn = font(F_BLACK, 30 * SC3); fs = font(F_BLACK, 18 * SC3)
        d.text((98 * SC3, 186 * SC3), "VITAMIN C", font=fn, fill=INKC + (255,), anchor="mm")
        d.text((98 * SC3, 214 * SC3), "AND THE COLD", font=fs, fill=ACC_S + (255,), anchor="mm")
        d.text((98 * SC3, 30 * SC3), "1970", font=fs, fill=INKC + (200,), anchor="mm")
        return _done(im, w, h)
    return gcache(("book70", seed), mk)


def medal_ink_el(seed=715):
    def mk():
        w, h = 120, 190; im, d, S = _cv(w, h)
        _ink_poly(d, [(30, 4), (54, 4), (70, 90), (50, 96)], (190, 60, 60), seed, INK_W - 3, amp=0.6)
        _ink_poly(d, [(90, 4), (66, 4), (50, 90), (70, 96)], (60, 90, 170), seed + 1, INK_W - 3, amp=0.6)
        _ink_ell(d, 60, 132, 46, 46, (240, 196, 70), seed + 2, INK_W - 1, n=24, amp=0.8)
        _ink_ell(d, 60, 132, 32, 32, (252, 220, 110), seed + 3, INK_W - 4, n=20, amp=0.6)
        d.ellipse(S(42, 112, 56, 124), fill=(255, 250, 220, 220))
        return _done(im, w, h)
    return gcache(("medal71", seed), mk)


def shoe_el(seed=716):
    def mk():
        w, h = 240, 150; im, d, S = _cv(w, h)
        _ink_poly(d, [(20, 60), (90, 40), (130, 70), (210, 86), (226, 118), (20, 120)], ACC, seed, INK_W, amp=1.2)
        _ink_poly(d, [(14, 118), (230, 118), (226, 138), (18, 138)], (246, 246, 246), seed + 1, INK_W - 2, amp=0.8)
        for k_ in range(3): d.line(S(70 + 18 * k_, 52 + 6 * k_, 96 + 18 * k_, 70 + 6 * k_), fill=(255, 255, 255, 255), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("shoe71", seed), mk)


def ski_el(seed=717):
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h)
        for sg in (-1, 1):
            P = [(120 + sg * 100, 30), (120 + sg * 84, 22), (120 - sg * 92, 214), (120 - sg * 104, 222)]
            _ink_poly(d, P, (70, 130, 200) if sg < 0 else ACC, seed + sg, INK_W - 1, amp=0.8)
        for sg in (-1, 1): d.line(S(120 + sg * 40, 20, 120 + sg * 70, 220), fill=INKC + (255,), width=6 * SC3)
        return _done(im, w, h)
    return gcache(("ski71", seed), mk)


def army_helmet_el(seed=718):
    def mk():
        w, h = 240, 180; im, d, S = _cv(w, h)
        P = _arcpts(120, 130, 100, 100, 180, 360, 24) + [(226, 132), (14, 132)]
        _ink_poly(d, P, (110, 128, 82), seed, INK_W, amp=1.2)
        _ink_poly(d, [(6, 128), (234, 128), (230, 150), (10, 150)], (90, 106, 66), seed + 1, INK_W - 2, amp=0.8)
        _hatch_in(im, (120, 30, 220, 130), lambda q, S_: q.ellipse(S_(20, 30, 220, 230), fill=255), -40, 10, 30)
        for k_ in range(4): d.ellipse(S(60 + 36 * k_, 80 - 10 * (k_ % 2), 72 + 36 * k_, 92 - 10 * (k_ % 2)), fill=(240, 246, 250, 230))   # snow dots
        return _done(im, w, h)
    return gcache(("helmet71", seed), mk)


def pile_el(n=6, seed=719):
    """a stack of n trial papers (study reports)."""
    def mk():
        w, h = 260, 80 + 26 * n; im, d, S = _cv(w, h)
        for i in range(n):
            y = h - 50 - i * 26; dx = 6 * math.sin(i * 1.7)
            _ink_poly(d, [(20 + dx, y), (240 + dx, y - 4), (236 + dx, y + 30), (24 + dx, y + 34)], (250, 248, 240), seed + i, INK_W - 3, amp=0.6)
            d.line(S(40 + dx, y + 14, 200 + dx, y + 12), fill=(150, 160, 180, 255), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("pile71", n, seed), mk)


# ---------------- LIVE pieces ----------------
def bib(f, x, y, s, num="71", lean=0.0):
    """a race number pinned on Chubby's chest (chub feet at x, y)."""
    bx = x + 30 * s * math.sin(math.radians(lean)); by = y - 250 * s
    w, h = 96 * s, 70 * s
    P = np.int32([(bx - w / 2, by - h / 2), (bx + w / 2, by - h / 2 - 3 * s), (bx + w / 2, by + h / 2), (bx - w / 2, by + h / 2 + 2 * s)])
    cv2.fillPoly(f, [P], C((252, 252, 248)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    comp(f, scale_el(ed_el(num, "", lead_col=ACC_S, lead_size=46), s), bx, by + 2 * s)


def cold_bar(f, x0, y, t, k=1.0, trim=0.0, n=7, bw=110, gap=8, col=None, label=True):
    """a cold as a row of n day blocks (drawn in with k); trim 0..1 = the 'bit sooner' slice (~8 %) at the end drops off and falls."""
    col = col or (214, 222, 160)
    tot = n * bw + (n - 1) * gap; cut = x0 + tot * (1 - 0.08)
    for i in range(n):
        if k * n < i + 0.2: break
        a = x0 + i * (bw + gap); b = a + bw
        cv2.rectangle(f, (int(a), int(y - 50)), (int(min(b, cut if trim > 0 else b)), int(y + 50)), C(col), -1)
        cv2.rectangle(f, (int(a), int(y - 50)), (int(min(b, cut if trim > 0 else b)), int(y + 50)), C(BP_INK), 5, cv2.LINE_AA)
        if b > cut and trim > 0:                                             # the falling slice
            dy = 900 * trim * trim; rot = 40 * trim
            sl = np.zeros((H, W), np.uint8)
            P = cv2.boxPoints(((float((cut + b) / 2), float(y + dy)), (float(b - cut), 100.0), rot)).astype(np.int32)
            cv2.fillPoly(f, [P], C(ACC_L), cv2.LINE_AA); cv2.polylines(f, [P], True, C(ACC_S), 5, cv2.LINE_AA)
    return cut


def risk_bars(f, t, x0, y0, k1, k2, h=560, bw=230, gap=150, labels=("NO VITAMIN C", "VITAMIN C"), cols=None):
    """two vertical risk bars that grow from the base; the second stops at half."""
    cols = cols or ((214, 200, 120), ACC)
    for i, (kk, frac) in enumerate(((k1, 1.0), (k2, 0.5))):
        x = x0 + i * (bw + gap); hh = h * frac * kk
        if kk > 0:
            cv2.rectangle(f, (int(x), int(y0 - hh)), (int(x + bw), int(y0)), C(cols[i]), -1)
            cv2.rectangle(f, (int(x), int(y0 - hh)), (int(x + bw), int(y0)), C(BP_INK), 6, cv2.LINE_AA)
        write_on(f, labels[i], x + bw / 2, y0 + 60, t, 0, 30, BP_INK, cps=400)
    cv2.line(f, (int(x0 - 40), int(y0)), (int(x0 + 2 * bw + gap + 40), int(y0)), C(BP_INK), 6, cv2.LINE_AA)
