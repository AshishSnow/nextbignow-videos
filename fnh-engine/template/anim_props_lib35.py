# ================= anim_props_lib35.py (was ep 35 anim_props6.py) (ep 35, 13 Nov): "Does sesame have more calcium than milk?" — SESAME-GOLD accent, ink props, NEW PLACE
from PIL import ImageFont
# THE BOXING RING (spotlit arena, crowd, ropes that wobble), boxers (a sesame seed vs a glass of milk with ink limbs + gloves), oxalate HANDCUFFS,
# calcium pebbles, the til bowl / spoon / laddoo, and the SECONDARY ACTION helpers (ep 35 craft skill). =================
ACC = (204, 146, 52); ACC_S = (146, 96, 28); ACC_L = (238, 204, 140); ACC_XL = (250, 236, 208)      # sesame gold = sesame / calcium on paper only
SES = (226, 190, 132); SES_S = (178, 136, 76); SES_D = (130, 92, 44)                                 # whole (unhulled) sesame seed tan
MILK = (252, 248, 238); MILK_S = (214, 208, 194)
STEELC = (196, 204, 212); STEEL_S = (128, 138, 150)
CA_C = (250, 250, 246); CA_S = (196, 196, 188)
SRC_US = "Source: USDA nutrient data (NIH ODS)"
SRC_OX = "Source: J Food Comp Anal 2004; Healthline (RD-reviewed)"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def _seed_pts(cx, cy, rx, ry, n=30):
    """a sesame seed outline: rounded bottom, a soft point on top (teardrop)."""
    P = []
    for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
        x, y = math.sin(a), -math.cos(a)                                               # a = 0 at the top
        k = 1 - 0.42 * max(0.0, -y) ** 2                                               # narrower toward the top
        P.append((cx + rx * x * k, cy + ry * y * (1.08 if y < 0 else 1.0)))
    return P


def seed_el(mood="n", look=(0, 0), hulled=False, seed=351):
    """a SESAME SEED buddy (the boxer's body): tan with a seam + hatch (whole) or bright white (hulled), a 3-stroke face."""
    def mk():
        w, h = 220, 300; im, d, S = _cv(w, h); cx, cy = 110, 160
        P = _seed_pts(cx, cy, 86, 128)
        fill = (250, 246, 236) if hulled else SES
        _ink_poly(d, P, fill, seed, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(cx + 10, cy - 120, cx + 200, cy + 160), fill=c),
               (226, 220, 206) if hulled else SES_S, 120)
        if not hulled:
            d.line(_P(_wob([(cx - 4, cy - 118), (cx - 8, cy - 40)], 1.0, seed + 2)), fill=SES_D + (200,), width=3 * SC3)
            _hatch_in(im, (cx, cy - 120, cx + 90, cy + 130), lambda q, S_: q.polygon(_P(P), fill=255))
        if mood: _face(d, S, cx, cy + 34, 1.45, mood, look)
        return _done(im, w, h)
    return gcache(("seed35", mood, tuple(look), hulled, seed), mk)


def milkglass_el(mood="n", look=(0, 0), level=0.86, slosh=0.0, seed=352):
    """a GLASS OF MILK buddy (the other boxer): tumbler, milk with a tilted surface (slosh -1..1), a face on the milk."""
    sl = round(clamp(slosh, -1, 1) * 4) / 4
    def mk():
        w, h = 220, 320; im, d, S = _cv(w, h)
        yl = 290 - 250 * level
        d.polygon(S(36, yl - 18 * sl, 184, yl + 18 * sl, 172, 290, 48, 290), fill=MILK + (255,))
        d.polygon(S(120, yl, 184, yl + 18 * sl, 172, 290, 128, 290), fill=MILK_S + (150,))
        d.line(_P([(38, yl - 18 * sl), (182, yl + 18 * sl)]), fill=INKC + (210,), width=3 * SC3)
        _ink_poly(d, [(24, 20), (196, 20), (178, 300), (42, 300)], None, seed, INK_W, amp=0.9)
        d.line(_P([(52, 50), (62, 260)]), fill=(255, 255, 255, 230), width=8 * SC3)
        if mood: _face(d, S, 110, 190, 1.45, mood, look)
        return _done(im, w, h)
    return gcache(("mglass35", mood, tuple(look), round(level, 2), sl, seed), mk)


def glove_el(col=None, seed=353, flip=False):
    """a boxing glove (ink): a fat mitten with a thumb and a white cuff band."""
    col = col or (196, 58, 48)
    def mk():
        w, h = 150, 160; im, d, S = _cv(w, h)
        P = _arcpts(80, 70, 60, 56, 0, 360, 24)[:-1]
        _ink_poly(d, P, col, seed, INK_W, amp=1.0)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(80, 40, 160, 150), fill=c), _mix(col, INKC, 0.35), 120)
        _ink_ell(d, 34, 84, 22, 26, col, seed + 1, INK_W - 1)
        _ink_poly(d, [(40, 116), (120, 116), (116, 150), (44, 150)], (250, 246, 236), seed + 2, INK_W - 1, amp=0.6)
        d.ellipse(S(60, 30, 84, 46), fill=(255, 255, 255, 140))
        im2 = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
        return _done(im2, w, h)
    return gcache(("glove35", col, seed, flip), mk)


GLOVE_SES = (178, 104, 40)          # the seed's gloves: deep sesame brown-gold
GLOVE_MILK = (64, 120, 196)         # the milk's gloves: blue (milk carton blue, generic)


def cuff_el(seed=354, open_=0.0):
    """oxalate HANDCUFFS: two steel rings and a short chain (ink)."""
    def mk():
        w, h = 300, 150; im, d, S = _cv(w, h)
        for cx in (70, 230):
            _ink_ell(d, cx, 75, 52, 52, None, seed + cx, INK_W + 1)
            d.ellipse(S(cx - 52, 23, cx + 52, 127), outline=STEELC + (255,), width=12 * SC3)
            d.arc(S(cx - 52, 23, cx + 52, 127), 200, 300, fill=(255, 255, 255, 220), width=4 * SC3)
            _ink_ell(d, cx, 75, 40, 40, None, seed + cx + 1, 2)
        for i in range(4):
            x = 122 + i * 19
            _ink_ell(d, x, 75, 11, 7, STEELC, seed + 10 + i, 2)
        return _done(im, w, h)
    return gcache(("cuff35", seed), mk)


def ca_el(cuffed=False, free=False, seed=355):
    """a CALCIUM pebble: white chalky round tile with 'Ca'; cuffed = a steel ring snapped round it (oxalate); free = a soft green rim (absorbed)."""
    def mk():
        w, h = 130, 130; im, d, S = _cv(w, h)
        P = _arcpts(65, 65, 44, 42, 0, 360, 20)[:-1]
        _ink_poly(d, P, CA_C, seed, INK_W - 1, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(66, 50, 130, 130), fill=c), CA_S, 110)
        fnt = ImageFont.truetype(F_HAND, 40 * SC3)
        d.text((65 * SC3, 66 * SC3), "Ca", font=fnt, fill=INKC + (255,), anchor="mm")
        if cuffed:
            d.ellipse(S(12, 12, 118, 118), outline=INKC + (255,), width=14 * SC3)
            d.ellipse(S(12, 12, 118, 118), outline=STEELC + (255,), width=8 * SC3)
            d.rectangle(S(100, 56, 128, 74), fill=STEEL_S + (255,), outline=INKC + (255,), width=2 * SC3)
        if free:
            d.ellipse(S(14, 14, 116, 116), outline=INK_MINT + (255,), width=6 * SC3)
        return _done(im, w, h)
    return gcache(("ca35", cuffed, free, seed), mk)


def mic_el(seed=356):
    """an announcer's microphone: a mesh ball head + a dark handle."""
    def mk():
        w, h = 90, 230; im, d, S = _cv(w, h)
        _ink_poly(d, [(32, 70), (58, 70), (52, 220), (38, 220)], (60, 56, 60), seed, INK_W - 1, amp=0.6)
        _ink_ell(d, 45, 46, 36, 38, STEELC, seed + 1, INK_W)
        for k in range(-2, 3):
            d.line(_P([(45 + k * 12, 14), (45 + k * 12, 80)]), fill=STEEL_S + (200,), width=2 * SC3)
        d.ellipse(S(26, 22, 44, 38), fill=(255, 255, 255, 180))
        return _done(im, w, h)
    return gcache(("mic35", seed), mk)


def _seed_dots(d, S, box, n, seed, r=7, hulled=False):
    rng = np.random.default_rng(seed); x0, y0, x1, y1 = box
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1); a = rng.uniform(0, 180)
        c = (250, 244, 228) if hulled else (SES if rng.random() > 0.3 else SES_S)
        dx, dy = math.cos(math.radians(a)) * r, math.sin(math.radians(a)) * r
        d.ellipse(S(x - r, y - r * 0.6, x + r, y + r * 0.6), fill=c + (255,), outline=SES_D + (255,), width=1 * SC3)


def til_bowl_el(seed=357, label="100 g"):
    """a BIG steel bowl heaped with sesame seeds (100 g = a heap you'd never eat in one go)."""
    def mk():
        w, h = 460, 340; im, d, S = _cv(w, h)
        heap = _arcpts(230, 170, 190, 130, 180, 360, 30)
        _ink_poly(d, heap + [(420, 170), (40, 170)], SES, seed, INK_W, amp=1.4)
        _seed_dots(d, S, (70, 60, 390, 170), 260, seed, 8)
        B_ = [(20, 160), (440, 160)] + _arcpts(230, 160, 200, 150, 0, 180, 20)
        _ink_poly(d, B_, STEELC, seed + 1, INK_W)
        _shade(im, lambda q, S_: q.polygon(_P(B_), fill=255), lambda q, S_, c: q.rectangle(S_(250, 150, 460, 340), fill=c), STEEL_S, 120)
        d.line(_P([(70, 190), (380, 190)]), fill=(255, 255, 255, 160), width=5 * SC3)
        if label:
            fnt = ImageFont.truetype(F_HAND, 54 * SC3)
            d.text((230 * SC3, 248 * SC3), label, font=fnt, fill=INKC + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("tilbowl35", seed, label), mk)


def spoon_til_el(seed=358):
    """a steel spoon with a small heap of sesame (the real serving)."""
    def mk():
        w, h = 360, 140; im, d, S = _cv(w, h)
        _ink_poly(d, [(150, 62), (350, 52), (352, 74), (150, 82)], STEELC, seed, INK_W - 1, amp=0.6)
        B_ = _arcpts(90, 70, 78, 46, 0, 360, 24)[:-1]
        _ink_poly(d, B_, STEELC, seed + 1, INK_W)
        _ink_poly(d, _arcpts(90, 66, 62, 34, 180, 360, 16) + [(152, 70), (28, 70)], SES, seed + 2, INK_W - 1, amp=1.0)
        _seed_dots(d, S, (40, 38, 140, 70), 44, seed, 6)
        d.ellipse(S(52, 80, 92, 96), fill=(255, 255, 255, 150))
        return _done(im, w, h)
    return gcache(("spoontil35", seed), mk)


def laddoo_el(mood=None, look=(0, 0), seed=359):
    """a TIL LADDOO: a round brown jaggery ball studded with sesame."""
    def mk():
        w, h = 200, 200; im, d, S = _cv(w, h)
        P = _arcpts(100, 100, 82, 80, 0, 360, 26)[:-1]
        _ink_poly(d, P, (164, 104, 52), seed, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon(_P(P), fill=255), lambda q, S_, c: q.ellipse(S_(100, 80, 200, 200), fill=c), (120, 72, 34), 120)
        rng = np.random.default_rng(seed)
        for _ in range(70):
            a = rng.uniform(0, 2 * math.pi); r_ = 74 * math.sqrt(rng.uniform(0, 1)); x, y = 100 + r_ * math.cos(a), 100 + r_ * math.sin(a)
            d.ellipse(S(x - 6, y - 3.5, x + 6, y + 3.5), fill=(240, 220, 170, 255), outline=SES_D + (255,), width=1 * SC3)
        if mood: _face(d, S, 100, 104, 1.3, mood, look)
        return _done(im, w, h)
    return gcache(("laddoo35", mood, tuple(look), seed), mk)


def belt_el(seed=360):
    """a champion's belt (gold plate on a dark strap), no words."""
    def mk():
        w, h = 420, 150; im, d, S = _cv(w, h)
        _ink_poly(d, [(10, 50), (410, 50), (410, 100), (10, 100)], (70, 52, 44), seed, INK_W - 1, amp=0.6)
        P = _arcpts(210, 75, 80, 64, 0, 360, 22)[:-1]
        _ink_poly(d, P, ACC, seed + 1, INK_W)
        _ink_ell(d, 210, 75, 44, 34, ACC_L, seed + 2, 3)
        return _done(im, w, h)
    return gcache(("belt35", seed), mk)


# (SECONDARY ACTION helpers sec_bounce / sec_tap / sec_wobble live in anim_fx.py since ep 35)


# ---------------- live: a BOXER (body element + ink limbs + gloves) ----------------
def boxer(f, x, y, s, t, kind="seed", mood="n", look=(0, 0), punch=0.0, cuff=0.0, ko=0.0, bounce=True, ph=0.0, struggle=0.0, slosh=0.0, raise_=0.0):
    """x, y = feet; kind 'seed' faces right, 'milk' faces left. punch 0..1 = the lead glove shoots out; cuff 0..1 = handcuffs snap on (gloves pulled
    together); ko 0..1 = knocked back (lean + lift); struggle = the cuffed gloves shake; raise_ = both gloves up (victory)."""
    dirn = 1 if kind == "seed" else -1
    dy, sq = sec_bounce(t, 150, 9 * s, ph) if bounce and ko < 0.3 else (0.0, 0.0)
    lean = -dirn * 26 * ko
    bh = 300 * s
    hip = (x, y - 120 * s + dy)
    by = hip[1] - bh * 0.5                                                           # body centre
    bx = x - dirn * 40 * s * ko
    # legs
    for sg in (-1, 1):
        fx = x + sg * 46 * s - dirn * 10 * s * ko
        kx = (hip[0] + fx) / 2 + sg * 10 * s
        P = [(hip[0] + sg * 22 * s, hip[1]), (kx, (hip[1] + y) / 2 - 4 * s), (fx, y - 10 * s)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C(INKC), max(3, int(16 * s)), cv2.LINE_AA)
        cv2.polylines(f, [np.array(P, np.int32)], False, C(SES_D if kind == "seed" else (120, 150, 200)), max(2, int(9 * s)), cv2.LINE_AA)
        cv2.ellipse(f, (int(fx + dirn * 10 * s), int(y - 6 * s)), (int(26 * s), int(13 * s)), 0, 0, 360, C(INKC), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(fx + dirn * 10 * s), int(y - 8 * s)), (int(21 * s), int(9 * s)), 0, 0, 360, C((250, 246, 236)), -1, cv2.LINE_AA)
    body = seed_el(mood, look) if kind == "seed" else milkglass_el(mood, look, 0.86, slosh)
    rot_comp(f, scale_el(body, s * (1 - 0.5 * sq)), bx, by, lean, 1.0, 1.0, 0.0)
    # arms + gloves
    gcol = GLOVE_SES if kind == "seed" else GLOVE_MILK
    sh_y = by - 40 * s
    tap = sec_tap(t, 1.3, ph) if (punch < 0.05 and cuff < 0.05 and ko < 0.2 and raise_ < 0.05) else 0.0
    for i, sg in enumerate((dirn, -dirn)):                                           # lead hand first (toward the opponent)
        shx = bx + sg * 70 * s
        if raise_ > 0:
            gx = bx + sg * (120 * s); gy = by - (170 + 60 * raise_) * s
        elif cuff > 0:
            gx = bx + dirn * (70 * s) + sg * 34 * s * (1 - cuff) + struggle * 10 * s * math.sin(t * 40 + i)
            gy = by + 30 * s + struggle * 6 * s * math.cos(t * 37 + i)
        else:
            reach = (105 + 160 * punch) * s if i == 0 else 80 * s
            gx = bx + dirn * reach - (0 if i == 0 else dirn * 40 * s) + dirn * 14 * s * tap * (i == 0)
            gy = by - 70 * s + (i * 30 * s) - 10 * s * tap
            if ko > 0: gx -= dirn * 160 * s * ko; gy -= 120 * s * ko
        ex = (shx + gx) / 2; ey = max(sh_y, gy) + 30 * s
        cv2.polylines(f, [np.array([(shx, sh_y), (ex, ey), (gx, gy)], np.int32)], False, C(INKC), max(3, int(14 * s)), cv2.LINE_AA)
        cv2.polylines(f, [np.array([(shx, sh_y), (ex, ey), (gx, gy)], np.int32)], False, C(SES_D if kind == "seed" else (120, 150, 200)), max(2, int(7 * s)), cv2.LINE_AA)
        el_g = glove_el(gcol, flip=(dirn < 0))
        rot_comp(f, scale_el(el_g, 0.8 * s), gx, gy, -dirn * 10, 1.0, 1.0, 0.0)
    if cuff > 0.05:
        cx_ = bx + dirn * 70 * s + struggle * 10 * s * math.sin(t * 40)
        rot_comp(f, scale_el(cuff_el(), 0.55 * s), cx_, by + 52 * s, 0, min(1.0, 0.4 + 0.6 * cuff), 1.0, 0.0)
    return bx, by


# ---------------- NEW PLACE: THE BOXING RING (a spotlit ring in a dark arena; crowd in the dark; ropes in front wobble on hits) ----------------
RING_FLOOR = 1300


def set_ring(t=0.0, blur=5, dim=0.0, flash=True):
    """BOXING RING: a dark navy arena, a cone of warm light from above, a dotted crowd in the dark with camera flashes, the canvas floor from y
    RING_FLOOR with the back ropes + corner posts. Draw boxers / Chubby, then ring_front() for the front apron + front ropes."""
    def mk():
        f = _vgrad((26, 28, 46), (44, 40, 58), 0, 1100)
        f[1100:] = _vgrad((44, 40, 58), (30, 28, 40), 1100, H)[1100:]
        rng = np.random.default_rng(5)
        for row in range(6):                                                           # the crowd: rows of heads in the dark
            yb = 760 + row * 62
            for i in range(26):
                xx = -20 + i * 44 + (row % 2) * 22 + rng.uniform(-6, 6)
                col = _mix((70, 64, 84), (130, 110, 120), rng.uniform(0, 1) * (0.4 + row * 0.1))
                cv2.circle(f, (int(xx), int(yb)), int(17 + row * 2), C(col), -1, cv2.LINE_AA)
                cv2.ellipse(f, (int(xx), int(yb + 40 + row * 2)), (int(26 + row * 2), int(26)), 0, 180, 360, C(col), -1, cv2.LINE_AA)
        f = _soft(f, blur + 3)
        # canvas floor (a trapezoid seen from the front)
        poly = np.array([(-200, H), (W + 200, H), (W - 40, RING_FLOOR), (40, RING_FLOOR)], np.int32)
        cv2.fillPoly(f, [poly], C((232, 222, 204)), cv2.LINE_AA)
        cv2.ellipse(f, (540, 1560), (520, 120), 0, 0, 360, C((214, 200, 178)), 6, cv2.LINE_AA)
        # corner posts + back ropes
        for px in (70, 1010):
            cv2.rectangle(f, (px - 14, 980), (px + 14, RING_FLOOR + 4), C((70, 66, 74)), -1, cv2.LINE_AA)
            cv2.rectangle(f, (px - 20, 970), (px + 20, 1000), C(ACC), -1, cv2.LINE_AA)
        for k, yy in enumerate((1030, 1110, 1190)):
            cv2.line(f, (70, yy), (1010, yy), C(INKC), 9, cv2.LINE_AA); cv2.line(f, (70, yy), (1010, yy), C((236, 230, 220)), 5, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("ring35", blur), mk).copy()
    # the overhead light cone (warm), the arena around it stays dark
    cone = np.zeros((H, W), np.float32)
    pts = np.array([(430, 0), (650, 0), (1000, RING_FLOOR + 300), (80, RING_FLOOR + 300)], np.int32)
    cv2.fillPoly(cone, [pts], 1.0); cone = cv2.GaussianBlur(cone, (0, 0), 60)
    f = f + cone[..., None] * np.array(C((255, 214, 150)), np.float32) * 0.16 * (1 - dim)
    glow(f, 540, 1450, 520, (255, 226, 170), 0.20 * (1 - dim))
    if flash:                                                                          # camera flashes in the crowd
        for i in range(5):
            u = (t * 0.9 + i * 0.37) % 1.0
            if u < 0.06:
                rng = np.random.default_rng(int(t * 0.9 + i * 0.37) * 13 + i)
                glow(f, rng.uniform(60, 1020), rng.uniform(780, 1080), 46, (255, 255, 240), 0.55 * (1 - u / 0.06))
    if dim > 0: f *= (1 - 0.45 * dim)
    return inkify(f)


def ring_front(f, t=0.0, hits=(), wob_amp=26.0):
    """the front ropes (sag + wobble after each hit: SECONDARY ACTION of the ring) + the apron below the canvas edge."""
    cv2.rectangle(f, (0, 1640), (W, H), C((60, 56, 92)), -1, cv2.LINE_AA)
    cv2.line(f, (0, 1640), (W, 1640), C(INKC), 6, cv2.LINE_AA)
    _hatch_band(f, 1648, H)
    wv = sec_wobble(t, list(hits), wob_amp)
    for k, yy in enumerate((1360, 1450)):
        P = [(x, yy + 18 * math.sin(math.pi * x / W) + wv * (1 - k * 0.3) * math.sin(math.pi * x / W)) for x in range(0, W + 1, 40)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C(INKC), 15, cv2.LINE_AA)
        cv2.polylines(f, [np.array(P, np.int32)], False, C((196, 58, 48) if k == 0 else (236, 230, 220)), 9, cv2.LINE_AA)


def bowtie(f, x, y, s, t=0.0, lean=0.0):
    """a bow tie under Chubby INK's chin (announcer)."""
    hx = x + 30 * s * math.sin(math.radians(lean)); ny = y - 300 * s + 3 * s * math.sin(t * 2.4)
    for sg in (-1, 1):
        P = np.array([(hx, ny), (hx + sg * 42 * s, ny - 22 * s), (hx + sg * 42 * s, ny + 22 * s)], np.int32)
        cv2.fillPoly(f, [P], C((196, 58, 48)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx), int(ny)), int(11 * s), C((160, 40, 36)), -1, cv2.LINE_AA); cv2.circle(f, (int(hx), int(ny)), int(11 * s), C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
