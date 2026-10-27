# ================= Chubby v2 — "3D look" (cel/clay shading) — owner request 27 Oct 23:08 =================
# Same API as fnh_char.py (chub, chub_head_el, chub_body_el, chub_head_only, logo_el) — loaded after it, overrides it.
# Look: natural warm colours, soft volume shading from a top-left key light (pseudo-3D "inflated" normals),
# warm rim light, soft ambient occlusion, warm-brown outlines instead of black, hoodie + jeans + sneakers.
OUT3 = (54, 36, 30)                        # warm dark outline
SKIN3 = (242, 196, 158); SKIN3_D = (196, 132, 100); SKIN3_H = (255, 226, 196)
HOOD3 = (40, 172, 128); HOOD3_D = (16, 98, 78); HOOD3_H = (126, 226, 186)    # FreshNestHub mint, natural
JEAN3 = (52, 70, 112); JEAN3_D = (28, 38, 66); JEAN3_H = (104, 128, 176)
HAIR3 = (74, 48, 34); HAIR3_H = (140, 98, 70)
LIGHT3 = (-0.55, -0.68, 0.50)              # key light from top-left-front
RIM3 = (255, 214, 170)                     # warm rim from behind-right


def _n01(c): return np.array(c, np.float32) / 255.0


def _inflate(mask, base, shadow, hi=None, light=LIGHT3, flat=0.95, spec=0.22, shin=22, rim=RIM3, rim_amt=0.28, wrap=0.35, ao=0.18):
    """pseudo-3D shading of a flat shape: height from the distance field -> normals -> wrapped lambert + spec + rim."""
    m = (mask > 0.5).astype(np.uint8)
    if m.sum() == 0: return np.zeros(mask.shape + (3,), np.float32)
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5).astype(np.float32)
    R = max(1.0, float(d.max())); u = np.clip(d / R, 0, 1)
    hgt = np.sqrt(np.clip(1 - (1 - u) ** 2, 0, 1)) * R * flat
    hgt = cv2.GaussianBlur(hgt, (0, 0), max(1.0, R * 0.04))
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3) / 8.0; gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    n = np.dstack([-gx, -gy, np.ones_like(hgt)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    ndl = n @ L; lam = np.clip((ndl + wrap) / (1 + wrap), 0, 1)
    lam = lam * lam * (3 - 2 * lam)                                            # soft toon-ish ramp
    b, s_ = _n01(base), _n01(shadow)
    col = s_[None, None] + (b - s_)[None, None] * lam[..., None]
    if hi is not None:
        hk = np.clip((lam - 0.78) / 0.22, 0, 1)[..., None]; col += (_n01(hi) - b)[None, None] * hk * 0.55
    Hv = L + np.array([0, 0, 1], np.float32); Hv /= np.linalg.norm(Hv)
    col += (np.clip(n @ Hv, 0, 1) ** shin * spec)[..., None]
    if rim is not None and rim_amt > 0:
        l2 = L[:2] / (np.linalg.norm(L[:2]) + 1e-6)
        back = np.clip(-(n[..., 0] * l2[0] + n[..., 1] * l2[1]) / (np.hypot(n[..., 0], n[..., 1]) + 1e-6), 0, 1)
        rr = (1 - n[..., 2]) ** 2.2 * back
        col += _n01(rim)[None, None] * (rr * rim_amt)[..., None]
    col *= (1 - ao * (1 - np.clip(u * 3, 0, 1)))[..., None]                   # slight darkening at the very edge
    return np.clip(col, 0, 1)


class _Cv:
    """float RGBA canvas for building shaded elements at supersampled size."""
    def __init__(self, w, h, sc):
        self.w, self.h, self.sc = w, h, sc; self.rgb = np.zeros((h * sc, w * sc, 3), np.float32); self.a = np.zeros((h * sc, w * sc), np.float32)

    def S(self, *v): return [x * self.sc for x in v]

    def mask(self, fn):
        im = Image.new("L", (self.w * self.sc, self.h * self.sc), 0); fn(ImageDraw.Draw(im), self.S); return np.asarray(im, np.float32) / 255.0

    def put(self, rgb, a):
        a = a[..., None] if a.ndim == 2 else a
        self.rgb = self.rgb * (1 - a) + rgb * a; self.a = self.a * (1 - a[..., 0]) + a[..., 0]

    def fill(self, col, a): self.put(np.broadcast_to(_n01(col), self.rgb.shape), a)

    def outline(self, m, px, col=OUT3):
        k = max(3, int(px * self.sc) | 1); dil = cv2.dilate((m > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        dil = cv2.GaussianBlur(dil.astype(np.float32), (0, 0), 0.6 * self.sc); self.fill(col, dil)

    def shaded(self, m, base, shadow, hi=None, outline=5, **kw):
        if outline: self.outline(m, outline)
        self.put(_inflate(m, base, shadow, hi, **kw), np.clip(m, 0, 1))

    def pil(self):
        a = np.clip(self.a, 0, 1)[..., None]; rgb = np.clip(self.rgb, 0, 1)
        return Image.fromarray((np.dstack([rgb, a]) * 255).astype(np.uint8), "RGBA")

    def done(self, im=None):
        im = im or self.pil(); return _done(im, self.w, self.h)


# ---------------- head ----------------
def chub_head_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n", tint=0.0, nose=None, cap=False):
    tint = round(clamp(tint) * 10) / 10
    if nose is not None: nose = round(clamp(nose) * 10) / 10
    key = ("chead3", mouth, blink, brow, lx, ly, expr, tint, nose, cap)
    if key in _gc: return _gc[key]
    mixc = lambda a, b, k: tuple(int(x + (y - x) * k) for x, y in zip(a, b))
    skin, skin_d, skin_h = mixc(SKIN3, (255, 150, 52), tint), mixc(SKIN3_D, (206, 96, 30), tint), mixc(SKIN3_H, (255, 196, 120), tint)
    cv = _Cv(230, 236, 3); cx, cy, R0 = 115, 128, 88
    # ears (behind the head)
    for ex in (cx - 86, cx + 86):
        me = cv.mask(lambda d, S, ex=ex: d.ellipse(S(ex - 17, cy - 6, ex + 17, cy + 34), fill=255))
        cv.shaded(me, skin, skin_d, skin_h, outline=5, rim_amt=0.2)
    mh = cv.mask(lambda d, S: d.ellipse(S(cx - R0, cy - R0, cx + R0, cy + R0), fill=255))
    cv.shaded(mh, skin, skin_d, skin_h, outline=6, flat=1.0)
    im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
    # hair: a short swept tuft + the signature curl
    _ov(im, lambda q: q.chord(S(cx - 74, cy - R0 - 2, cx + 70, cy - 10), 196, 330, fill=HAIR3 + (255,)))
    _ov(im, lambda q: q.chord(S(cx - 60, cy - R0 + 6, cx + 30, cy - 30), 200, 300, fill=HAIR3_H + (150,)))
    d.arc(S(98, 6, 132, 40), 150, 420, fill=HAIR3 + (255,), width=8 * 3)
    d.arc(S(108, 16, 124, 32), 200, 470, fill=HAIR3 + (255,), width=6 * 3)
    # cheeks
    for ex in (66, 164): _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 18, 150, ex + 18, 166), fill=(240, 110, 100, 95)))
    # eyes
    ox, oy = lx * 6, ly * 5
    for ex in (86, 144):
        ey = 116
        if blink or expr == "happy":
            d.arc(S(ex - 16, ey - 10, ex + 16, ey + 14), 200, 340, fill=OUT3 + (255,), width=6 * 3); continue
        rx, ry = (19, 24) if expr == "wow" else (15, 19)
        d.ellipse(S(ex - rx, ey - ry, ex + rx, ey + ry), fill=(252, 250, 246, 255), outline=OUT3 + (255,), width=4 * 3)
        pr = 7 if expr == "wow" else 10
        px, py = ex + ox, ey + 3 + oy
        d.ellipse(S(px - pr, py - pr, px + pr, py + pr), fill=(40, 26, 22, 255))
        d.ellipse(S(px - pr + 3, py - pr + 2, px - pr + 9, py - pr + 8), fill=(255, 255, 255, 255))
        _ov(im, lambda q, px=px, py=py: q.ellipse(S(px + 2, py + 3, px + 6, py + 7), fill=(255, 255, 255, 160)))
        if expr == "sus":
            d.rectangle(S(ex - rx - 2, ey - ry - 2, ex + rx + 2, ey - 4), fill=skin + (255,)); d.line(S(ex - rx, ey - 4, ex + rx, ey - 4), fill=OUT3 + (255,), width=5 * 3)
        if expr == "sleepy":   # ep 14 expression, v2 look: heavy drooping lids (shaded) + tired bags
            d.chord(S(ex - rx - 3, ey - ry - 3, ex + rx + 3, ey + ry + 3), 180, 360, fill=skin_d + (255,))
            d.rectangle(S(ex - rx - 3, ey - 2, ex + rx + 3, ey + 3), fill=skin_d + (255,))
            d.arc(S(ex - rx - 1, ey - 8, ex + rx + 1, ey + 10), 180, 360, fill=OUT3 + (255,), width=6 * 3)
            d.arc(S(ex - rx + 2, ey + ry - 6, ex + rx - 2, ey + ry + 8), 20, 160, fill=(150, 110, 160, 255), width=4 * 3)
    # brows (hair coloured)
    for i, ex in enumerate((86, 144)):
        if brow == "up": pts = [(ex - 16, 84), (ex + 14, 80)] if i == 0 else [(ex - 14, 80), (ex + 16, 84)]
        elif brow == "sus": pts = [(ex - 16, 88), (ex + 14, 95)] if i == 0 else [(ex - 14, 95), (ex + 16, 88)]
        elif brow == "sad": pts = [(ex - 16, 95), (ex + 14, 86)] if i == 0 else [(ex - 14, 86), (ex + 16, 95)]
        else: pts = [(ex - 15, 90), (ex + 14, 88)] if i == 0 else [(ex - 14, 88), (ex + 15, 90)]
        d.line([(p[0] * 3, p[1] * 3) for p in pts], fill=HAIR3 + (255,), width=8 * 3)
    if nose is not None:
        nc = mixc(skin, (255, 150, 52), nose)
        d.ellipse(S(101, 128, 129, 150), fill=nc + (255,), outline=OUT3 + (255,), width=4 * 3)
        _ov(im, lambda q: q.ellipse(S(107, 132, 116, 139), fill=(255, 255, 255, 150)))
    if cap:
        d.chord(S(cx - R0 - 4, cy - R0 - 6, cx + R0 + 4, cy + R0 - 10), 180, 360, fill=(120, 72, 40, 255), outline=OUT3 + (255,), width=5 * 3)
        for ex in (84, 146):
            d.ellipse(S(ex - 22, 46, ex + 22, 86), fill=(60, 120, 150, 255), outline=OUT3 + (255,), width=5 * 3)
            _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 12, 54, ex - 2, 66), fill=(200, 240, 255, 200)))
        d.line(S(106, 66, 124, 66), fill=OUT3 + (255,), width=6 * 3)
    # mouth
    mx, my = 115, 166
    if expr == "wow" and mouth == 0: mouth = "o"
    dark = (92, 30, 34)
    if mouth == 0:
        if expr == "sad": d.arc(S(mx - 20, my - 2, mx + 20, my + 20), 200, 340, fill=OUT3 + (255,), width=6 * 3)
        elif expr == "smirk": d.arc(S(mx - 22, my - 16, mx + 20, my + 10), 10, 120, fill=OUT3 + (255,), width=6 * 3)
        elif expr == "happy": d.chord(S(mx - 24, my - 16, mx + 24, my + 20), 0, 180, fill=dark + (255,)); d.chord(S(mx - 14, my + 2, mx + 14, my + 20), 0, 180, fill=(236, 110, 110, 255))
        else: d.arc(S(mx - 22, my - 16, mx + 22, my + 10), 20, 160, fill=OUT3 + (255,), width=6 * 3)
    elif mouth == "o":
        d.ellipse(S(mx - 11, my - 8, mx + 11, my + 16), fill=dark + (255,))
    else:
        hh = {1: 9, 2: 15, 3: 21}[mouth]; ww = {1: 16, 2: 20, 3: 23}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 6, mx + ww, my - 6 + hh * 1.6), int(hh * 0.8) * 3, fill=dark + (255,))
        if mouth >= 2: d.ellipse(S(mx - ww * 0.6, my - 6 + hh * 0.9, mx + ww * 0.6, my - 6 + hh * 1.7), fill=(236, 110, 110, 255))
        d.rectangle(S(mx - ww + 6, my - 6, mx + ww - 6, my - 1), fill=(255, 255, 255, 255))
    el = _done(im, 230, 236)
    if len(_gc) < 900: _gc[key] = el
    return el


# ---------------- hoodie body ----------------
def chub_body_el(shirt=HOOD3, logo=True):
    if tuple(shirt) == tuple(CH_SHIRT): shirt = HOOD3
    def mk():
        base = tuple(shirt); dark = tuple(int(c * 0.45) for c in base); hi = tuple(min(255, int(c * 1.0 + 70)) for c in base)
        cv = _Cv(300, 270, 2)
        mb = cv.mask(lambda d, S: d.ellipse(S(12, 12, 288, 262), fill=255))
        cv.shaded(mb, base, dark, hi, outline=6, flat=0.85)
        im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
        sh = tuple(int(c * 0.72) for c in base)
        # hood collar folded around the neck
        _ov(im, lambda q: q.chord(S(84, -6, 216, 70), 0, 180, fill=sh + (255,)))
        d.arc(S(84, -6, 216, 70), 0, 180, fill=OUT3 + (255,), width=4 * 2)
        _ov(im, lambda q: q.arc(S(96, 0, 204, 56), 20, 160, fill=hi + (150,), width=5 * 2))
        # drawstrings with aglets
        for x0, x1 in ((134, 128), (166, 172)):
            d.line(S(x0, 50, x1, 118), fill=(246, 244, 236, 255), width=5 * 2)
            d.rounded_rectangle(S(x1 - 4, 114, x1 + 4, 130), 3 * 2, fill=(200, 200, 196, 255))
        # kangaroo pocket + seams
        _ov(im, lambda q: q.rounded_rectangle(S(86, 158, 214, 222), 26 * 2, fill=sh + (190,)))
        d.rounded_rectangle(S(86, 158, 214, 222), 26 * 2, outline=OUT3 + (200,), width=3 * 2)
        _ov(im, lambda q: q.line(S(100, 166, 200, 166), fill=hi + (120,), width=3 * 2))
        # ribbed hem
        hem = Image.new("L", im.size, 0); ImageDraw.Draw(hem).rectangle(S(0, 236, 300, 270), fill=255)
        body = Image.new("L", im.size, 0); ImageDraw.Draw(body).ellipse(S(12, 12, 288, 262), fill=255)
        hm = Image.fromarray(np.minimum(np.asarray(hem), np.asarray(body)), "L")
        im.paste(Image.new("RGBA", im.size, sh + (255,)), (0, 0), hm)
        for i in range(10): d.line(S(70 + i * 16, 238, 72 + i * 16, 256), fill=dark + (140,), width=2 * 2)
        # soft fabric folds
        for (a0, a1, b0, b1) in ((26, 120, 90, 230), (210, 130, 280, 236)):
            _ov(im, lambda q, a0=a0, a1=a1, b0=b0, b1=b1: q.arc(S(a0, a1, b0, b1), 200 if a0 < 100 else 250, 290 if a0 < 100 else 340, fill=dark + (90,), width=4 * 2))
        if logo:  # small FNH badge on the chest
            d.ellipse(S(196, 70, 228, 102), fill=(250, 248, 240, 255), outline=OUT3 + (220,), width=2 * 2)
            d.polygon(S(212, 76, 222, 86, 212, 96, 202, 86), fill=base + (255,))
        return _done(im, 300, 270)
    return gcache(("cbody3", tuple(shirt), logo), mk)


# ---------------- per-frame limbs: shaded tubes, mitten hands, sneakers ----------------
def _limb(f, pts, rs, base, dark, hi, ow=4.0):
    """shaded multi-segment tube (arm / leg): one outline pass for the whole chain, then fill, then per-segment
    shadow + highlight strips on the side away from / toward the key light -> no outline seams at elbows/knees."""
    pts = [(float(a), float(b)) for a, b in pts]
    if not hasattr(rs, "__len__"): rs = [rs] * len(pts)
    P = lambda pt: (int(round(pt[0])), int(round(pt[1])))
    for extra, col in ((ow, OUT3), (0, base)):
        for k in range(len(pts) - 1):
            r = 0.5 * (rs[k] + rs[k + 1]) + extra
            cv2.line(f, P(pts[k]), P(pts[k + 1]), C(col), max(1, int(2 * r)), cv2.LINE_AA)
        for k, pt in enumerate(pts): cv2.circle(f, P(pt), int(rs[k] + extra), C(col), -1, cv2.LINE_AA)
    for k in range(len(pts) - 1):
        p, q = pts[k], pts[k + 1]; r = 0.5 * (rs[k] + rs[k + 1])
        dx, dy = q[0] - p[0], q[1] - p[1]; ln = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / ln, dx / ln
        if nx * LIGHT3[0] + ny * LIGHT3[1] < 0: nx, ny = -nx, -ny             # n points toward the light
        off = lambda pt, kk: (pt[0] + nx * kk, pt[1] + ny * kk)
        cv2.line(f, P(off(p, -0.52 * r)), P(off(q, -0.52 * r)), C(dark), max(1, int(0.85 * r)), cv2.LINE_AA)
        cv2.line(f, P(off(p, 0.42 * r)), P(off(q, 0.42 * r)), C(hi), max(1, int(0.42 * r)), cv2.LINE_AA)


def _tube(f, p, q, r, base, dark, hi, ow=4.0):
    _limb(f, (p, q), r, base, dark, hi, ow)


_AO = {}


def _chin_ao(s):
    k = round(s, 2)
    if k not in _AO:
        w, h = int(170 * s), int(70 * s); a = np.zeros((h, w), np.float32)
        cv2.ellipse(a, (w // 2, h // 2), (int(w * 0.36), int(h * 0.26)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        a = cv2.GaussianBlur(a, (0, 0), 7 * s + 1) * 0.42
        _AO[k] = (np.zeros((h, w, 3), np.float32), a)
    return _AO[k]


def _mitt_el(tint=0.0):
    tint = round(clamp(tint) * 10) / 10
    def mk():
        mixc = lambda a, b, k: tuple(int(x + (y - x) * k) for x, y in zip(a, b))
        skin, skin_d, skin_h = mixc(SKIN3, (255, 150, 52), tint), mixc(SKIN3_D, (206, 96, 30), tint), mixc(SKIN3_H, (255, 196, 120), tint)
        cv = _Cv(70, 70, 3)
        m1 = cv.mask(lambda d, S: d.ellipse(S(12, 14, 54, 58), fill=255))
        m2 = cv.mask(lambda d, S: d.ellipse(S(40, 10, 60, 32), fill=255))
        cv.shaded(np.maximum(m1, m2), skin, skin_d, skin_h, outline=4, flat=0.8)
        return cv.done()
    return gcache(("mitt3", tint), mk)


def _sneaker_el(side=1):
    def mk():
        cv = _Cv(110, 60, 3)
        mu = cv.mask(lambda d, S: d.rounded_rectangle(S(12, 8, 100, 46), 20 * 3, fill=255))
        cv.shaded(mu, (246, 244, 238), (176, 172, 168), (255, 255, 255), outline=4, flat=0.6, rim_amt=0.1)
        im = cv.pil(); d = ImageDraw.Draw(im); S = cv.S
        d.rounded_rectangle(S(8, 38, 104, 54), 8 * 3, fill=(210, 206, 200, 255), outline=OUT3 + (255,), width=3 * 3)
        d.line(S(40, 30, 74, 24), fill=HOOD3 + (255,), width=5 * 3)
        for i in range(3): d.line(S(30 + i * 9, 14, 34 + i * 9, 24), fill=(150, 146, 140, 255), width=2 * 3)
        el = _done(im, 110, 60)
        if side < 0: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
        return el
    return gcache(("sneak3", side), mk)


def chub(f, x, y, s=1.0, la=(20, 10), ra=(20, 10), ll=6, rl=6, mouth=0, blink=False, brow="n", look=(0, 0), expr="n", tint=0.0,
         hold=None, hold_off=(0, 0), hold_l=None, bob=0.0, op=1.0, shirt=HOOD3, shadow=True, lean=0.0, squash=0.0, sit=False, nose=None, cap=False, hold_front=False):
    """Chubby v2 (3D look). (x, y) = feet baseline. arm angles (upper, fore) from straight down, positive = outward."""
    g = f if op >= 0.999 else f.copy()
    if tuple(shirt) == tuple(CH_SHIRT): shirt = HOOD3
    sq = 1 + 0.12 * squash
    if shadow:
        contact(g, x, y + 6 * s, 300 * s, 0.42); contact(g, x, y + 2 * s, 170 * s, 0.30)
    hipy = y - 120 * s * (1 / sq)
    for side, ang in ((-1, ll), (1, rl)):
        hx_ = x + side * 54 * s
        if sit:
            kn = (hx_ + side * 30 * s, hipy + 20 * s); ft = (hx_ + side * 40 * s, y)
            _limb(g, ((hx_, hipy), kn, ft), (21 * s, 21 * s, 20 * s), JEAN3, JEAN3_D, JEAN3_H)
        else:
            ft = (hx_ + side * math.sin(math.radians(ang)) * 112 * s, hipy + math.cos(math.radians(ang)) * 112 * s)
            _tube(g, (hx_, hipy), ft, 21 * s, JEAN3, JEAN3_D, JEAN3_H)
        comp(g, scale_el(_sneaker_el(side), s), ft[0] + side * 14 * s, ft[1] + 2 * s)
    lr = math.radians(lean)
    bcx = x + 40 * s * math.sin(lr); bcy = y - 215 * s / sq + bob * s * 0.5
    el = scale_el(chub_body_el(shirt), s)
    if abs(sq - 1) > 1e-3:
        el = (cv2.resize(el[0], (int(el[0].shape[1] * (1 + 0.1 * squash)), int(el[0].shape[0] / sq))),
              cv2.resize(el[1], (int(el[1].shape[1] * (1 + 0.1 * squash)), int(el[1].shape[0] / sq))))
    comp(g, el, bcx, bcy)
    base = tuple(shirt); dark = tuple(int(c * 0.55) for c in base); hi = tuple(min(255, int(c + 60)) for c in base)
    hands = {}
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sh_ = (bcx + side * 118 * s, bcy - 46 * s)   # same shoulder as v1 -> arm_ik helpers keep working
        e = (sh_[0] + side * math.sin(math.radians(a1)) * 76 * s, sh_[1] + math.cos(math.radians(a1)) * 76 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 70 * s, e[1] + math.cos(math.radians(a2)) * 70 * s)
        _limb(g, (sh_, e, hd), (19 * s, 18 * s, 16 * s), base, dark, hi)
        cuff = (e[0] + (hd[0] - e[0]) * 0.86, e[1] + (hd[1] - e[1]) * 0.86)
        cv2.circle(g, (int(cuff[0]), int(cuff[1])), int(15 * s), C(tuple(int(c * 0.8) for c in base)), -1, cv2.LINE_AA)
        hands[side] = hd
    mitt = scale_el(_mitt_el(tint), s)
    if hold is not None and not hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    if hold_l is not None:
        hx, hy = hands[-1]; comp(g, hold_l, hx - hold_off[0] * s, hy + hold_off[1] * s)
    for side in (-1, 1):
        hx, hy = hands[side]; comp(g, mitt if side > 0 else (np.ascontiguousarray(mitt[0][:, ::-1]), np.ascontiguousarray(mitt[1][:, ::-1])), hx, hy)
    hel = chub_head_el(mouth, blink, brow, look[0], look[1], expr, tint, nose, cap)
    hxc, hyc = bcx + 10 * s * math.sin(lr), bcy - 205 * s / sq + bob * s
    comp(g, _chin_ao(s), hxc, hyc + 84 * s)   # soft ambient occlusion under the chin
    comp(g, scale_el(hel, s), hxc, hyc)
    if hold is not None and hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s); comp(g, mitt, hx, hy)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


def chub_head_only(f, x, y, s, t=0.0, mouth=None, expr="n", brow="n", look=(0, 0), tint=0.0, blink=None, nose=None, cap=False, op=1.0):
    m = talk(t) if mouth is None else mouth
    b = blink_at(t, 1) if blink is None else blink
    comp(f, scale_el(chub_head_el(m, b, brow, look[0], look[1], expr, tint, nose, cap), s), x, y, op=op)


def logo_el():
    def mk():
        w, h, sc = 940, 380, 2; im, d = _canvas(w, h)
        hp = _pil_from_el(chub_head_el(2, False, "up", 0, 0, "happy"), 190 * sc, 195 * sc); im.alpha_composite(hp, (int(10 * sc), int(30 * sc)))
        fo = font(F_BLACK, 150 * sc); x = 215 * sc
        for ch in "FRESH": d.text((x, 128 * sc), ch, font=fo, fill=HOOD3 + (255,), anchor="lm"); x += fo.getlength(ch) - 4 * sc
        d.text((219 * sc, 272 * sc), "NEST HUB", font=font(F_BLACK, 112 * sc), fill=INK + (255,), anchor="lm")
        return _done(im, w, h)
    return gcache("logo_fnh3", mk)


def grip_hand(f, x, y, s=1.0, tint=0.0):
    """a shaded hand drawn OVER a held object's handle (knife, spoon...) -> the fingers wrap the grip."""
    comp(f, scale_el(_mitt_el(tint), s * 0.92), x, y)


CH_SKIN = SKIN3      # close-up props (eye2_el, hands) pick up the v2 skin tone
