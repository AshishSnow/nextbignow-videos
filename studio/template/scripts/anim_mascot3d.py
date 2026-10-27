# ================= 3D-look mascot (exec'd after anim_base.py) =================
# Owner, 27 Oct: "improve our character — not follow exactly, but 3D, better colours". Same identity (rounded-square face, orange
# tie, navy-and-orange palette) with volume: soft-shaded head with hair, a real body (suit jacket, shirt, tie, sleeves, trousers,
# shoes), cel-shaded limbs with highlights and shadows, warm dark outlines, contact shadow. Same API as guy()/head_el(), so all
# shot code keeps working. MASCOT3D=0 restores the stick figure.
import os as _os
MASCOT3D = _os.environ.get("MASCOT3D", "1") != "0"

OUT_ = (40, 26, 32)                                          # warm dark outline
SKIN_HI, SKIN_MID, SKIN_LO = (255, 236, 212), (250, 214, 180), (214, 160, 128)
HAIR_HI, HAIR_LO = (126, 84, 56), (52, 32, 26)
SUIT_HI, SUIT_MID, SUIT_LO = (92, 132, 236), (44, 76, 182), (24, 40, 110)
TIE_HI, TIE_MID, TIE_LO = (255, 170, 90), (255, 96, 36), (196, 54, 18)
PANT_HI, PANT_MID, PANT_LO = (96, 102, 124), (58, 62, 80), (34, 36, 50)
SHOE_HI, SHOE_LO = (130, 84, 56), (58, 34, 24)


def _f(c): return tuple(v / 255.0 for v in c)


def _shade_field(h, w, lx=0.30, ly=0.25):
    """0 (lit, top-left) .. 1 (shadow, bottom-right) — soft key light from upper left"""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot(xx / w - lx, yy / h - ly) / 1.0
    return np.clip(d, 0, 1)


def _ramp(k, hi, mid, lo):
    hi, mid, lo = (np.array(c, np.float32) / 255 for c in (hi, mid, lo))
    k = k[..., None]
    return np.where(k < 0.5, hi + (mid - hi) * (k / 0.5), mid + (lo - mid) * ((k - 0.5) / 0.5))


def head3d_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n"):
    key = ("head3d", mouth, blink, brow, lx, ly, expr)
    if key in _gc: return _gc[key]
    sc = 3; w, h = 230, 236; S = lambda *v: [x * sc for x in v]; W3, H3 = w * sc, h * sc
    # face mask (rounded square), shaded in 3 tones with a soft gradient + rim light + chin occlusion
    m = Image.new("L", (W3, H3), 0); ImageDraw.Draw(m).rounded_rectangle(S(30, 52, 200, 222), 44 * sc, fill=255)
    m = np.asarray(m, np.float32) / 255
    k = _shade_field(H3, W3, 0.32, 0.30) * 1.25
    k = np.clip(k + 0.35 * np.clip((np.mgrid[0:H3, 0:W3][0] / H3 - 0.80) * 4, 0, 1), 0, 1)   # chin occlusion
    rgb = _ramp(k, SKIN_HI, SKIN_MID, SKIN_LO)
    rim = np.clip(m - cv2.erode(m, np.ones((5, 5), np.uint8), iterations=4), 0, 1) * (np.mgrid[0:H3, 0:W3][1] / W3 > 0.62)
    rgb = rgb + rim[..., None] * np.array([0.10, 0.12, 0.18], np.float32)
    # outline
    ol = np.clip(cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=6) - m, 0, 1)
    out = np.zeros((H3, W3, 4), np.float32)
    out[..., :3] = rgb * m[..., None] + np.array(_f(OUT_), np.float32) * ol[..., None]
    out[..., 3] = np.clip(m + ol, 0, 1)
    im = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA"); d = ImageDraw.Draw(im)
    # hair cap: side-swept, with a highlight band
    hair = [(34, 104), (40, 60), (70, 34), (118, 24), (166, 30), (196, 56), (202, 100), (178, 76), (150, 70), (120, 82), (92, 72), (62, 88)]
    d.polygon([(x * sc, y * sc) for x, y in hair], fill=HAIR_LO + (255,), outline=OUT_ + (255,), width=5 * sc)
    d.line([(x * sc, y * sc) for x, y in [(66, 52), (106, 36), (150, 38)]], fill=HAIR_HI + (255,), width=9 * sc, joint="curve")
    # ears
    for ex in (24, 206):
        d.ellipse(S(ex - 14, 128, ex + 14, 162), fill=SKIN_MID + (255,), outline=OUT_ + (255,), width=4 * sc)
    d.rounded_rectangle(S(30, 52, 200, 222), 44 * sc, outline=OUT_ + (255,), width=5 * sc)
    # cheeks
    bl = Image.new("RGBA", im.size, (0, 0, 0, 0)); db = ImageDraw.Draw(bl)   # blush composited (a plain draw would punch holes in alpha)
    for cx in (70, 160):
        db.ellipse(S(cx - 18, 168, cx + 18, 184), fill=(255, 120, 120, 120))
    im = Image.alpha_composite(im, bl.filter(ImageFilter.GaussianBlur(3 * sc))); d = ImageDraw.Draw(im)
    # eyes: white + iris + 2 speculars (look direction), or blink/sus lids
    ox, oy = lx * 8, ly * 5
    for cx in (86, 144):
        x = cx + ox; y = 132 + oy
        if blink: d.rounded_rectangle(S(x - 14, y - 2, x + 14, y + 4), 3 * sc, fill=OUT_ + (255,)); continue
        rr = 17 if expr == "wow" else 14
        d.ellipse(S(cx - rr, 132 - rr * 1.1, cx + rr, 132 + rr * 1.1), fill=(255, 255, 255, 255), outline=OUT_ + (255,), width=3 * sc)
        ir = rr * 0.66
        d.ellipse(S(x - ir, y - ir * 1.05, x + ir, y + ir * 1.05), fill=(54, 34, 26, 255))
        d.ellipse(S(x - ir * 0.45, y - ir * 0.5, x + ir * 0.45, y + ir * 0.5), fill=(16, 10, 10, 255))
        d.ellipse(S(x - ir * 0.62, y - ir * 0.85, x - ir * 0.05, y - ir * 0.28), fill=(255, 255, 255, 255))
        d.ellipse(S(x + ir * 0.25, y + ir * 0.25, x + ir * 0.55, y + ir * 0.55), fill=(255, 255, 255, 200))
        if expr == "sus":   # heavy upper lids
            d.rectangle(S(cx - rr - 2, 132 - rr * 1.2, cx + rr + 2, 132 - rr * 0.15), fill=SKIN_MID + (255,))
            d.line(S(cx - rr, 132 - rr * 0.15, cx + rr, 132 - rr * 0.15), fill=OUT_ + (255,), width=4 * sc)
    for i, cx in enumerate((86, 144)):
        if brow == "up": pts = [(cx - 16, 100), (cx + 14, 94)] if i == 0 else [(cx - 14, 94), (cx + 16, 100)]
        elif brow == "sus": pts = [(cx - 16, 104), (cx + 14, 112)] if i == 0 else [(cx - 14, 112), (cx + 16, 104)]
        elif brow == "sad": pts = [(cx - 16, 112), (cx + 14, 104)] if i == 0 else [(cx - 14, 104), (cx + 16, 112)]
        else: pts = [(cx - 16, 108), (cx + 14, 105)] if i == 0 else [(cx - 14, 105), (cx + 16, 108)]
        d.line([(p[0] * sc, p[1] * sc) for p in pts], fill=HAIR_LO + (255,), width=8 * sc)
    mx, my = 115, 186
    if expr == "wow" and mouth == 0: mouth = "o"
    if mouth == 0:
        if expr == "sad": d.arc(S(mx - 20, my - 2, mx + 20, my + 18), 200, 340, fill=OUT_ + (255,), width=5 * sc)
        elif expr == "smirk": d.arc(S(mx - 22, my - 14, mx + 20, my + 8), 10, 120, fill=OUT_ + (255,), width=5 * sc)
        elif expr == "sus": d.line(S(mx - 14, my + 2, mx + 14, my - 2), fill=OUT_ + (255,), width=5 * sc)
        else: d.arc(S(mx - 22, my - 16, mx + 22, my + 10), 20, 160, fill=OUT_ + (255,), width=5 * sc)
    elif mouth == "o":
        d.ellipse(S(mx - 11, my - 8, mx + 11, my + 15), fill=(70, 20, 26, 255), outline=OUT_ + (255,), width=3 * sc)
    else:
        hh = {1: 9, 2: 15, 3: 21}[mouth]; ww = {1: 16, 2: 20, 3: 23}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 6, mx + ww, my - 6 + hh * 1.6), int(hh * 0.8) * sc, fill=(80, 22, 28, 255), outline=OUT_ + (255,), width=3 * sc)
        if mouth >= 2: d.ellipse(S(mx - ww * 0.55, my - 6 + hh * 0.9, mx + ww * 0.55, my - 6 + hh * 1.65), fill=(240, 100, 106, 255))
        d.rectangle(S(mx - ww + 6, my - 4, mx + ww - 6, my + 1), fill=(255, 255, 255, 255))
    # soft glossy highlight on the forehead
    gl = Image.new("L", im.size, 0); ImageDraw.Draw(gl).ellipse(S(52, 72, 98, 92), fill=90); gl = gl.filter(ImageFilter.GaussianBlur(6 * sc))
    im.paste(Image.new("RGBA", im.size, (255, 255, 255, 255)), (0, 0), gl)
    el = el_from(im.resize((w, h), Image.LANCZOS))
    _gc[key] = el; return el


def _tube(g, p, q, th, hi, mid, lo, out=OUT_):
    """cel-shaded limb: outline, base, shadow side, highlight stripe, round caps"""
    p = np.array(p, np.float32); q = np.array(q, np.float32); v = q - p; L = float(np.hypot(*v)) or 1.0
    n = np.array([-v[1], v[0]]) / L
    if n[0] + n[1] > 0: n = -n                                   # point the normal toward the upper-left light
    P = lambda a: (int(round(a[0])), int(round(a[1])))
    cv2.line(g, P(p), P(q), _f(out), int(th + 6), cv2.LINE_AA)
    for c in (p, q): cv2.circle(g, P(c), int((th + 6) / 2), _f(out), -1, cv2.LINE_AA)
    cv2.line(g, P(p), P(q), _f(mid), int(th), cv2.LINE_AA)
    for c in (p, q): cv2.circle(g, P(c), int(th / 2), _f(mid), -1, cv2.LINE_AA)
    cv2.line(g, P(p - n * th * 0.2), P(q - n * th * 0.2), _f(lo), max(1, int(th * 0.5)), cv2.LINE_AA)
    cv2.line(g, P(p + n * th * 0.24), P(q + n * th * 0.24), _f(hi), max(1, int(th * 0.22)), cv2.LINE_AA)


def _poly_shaded(g, pts, hi, mid, lo, out=OUT_, ow=4):
    """fill a polygon with a key-light gradient (upper-left lit) and outline it — done in a local box"""
    pts = np.array(pts, np.float32); x0, y0 = np.floor(pts.min(0)).astype(int) - ow - 2; x1, y1 = np.ceil(pts.max(0)).astype(int) + ow + 2
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if X1 <= X0 or Y1 <= Y0: return
    hh, ww = Y1 - Y0, X1 - X0
    m = np.zeros((hh, ww), np.float32); cv2.fillPoly(m, [np.round(pts - [X0, Y0]).astype(np.int32)], 1.0, cv2.LINE_AA)
    ol = np.clip(cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=max(1, ow // 2)) - m, 0, 1)
    k = _shade_field(hh, ww, 0.25, 0.15)
    rgb = _ramp(k, hi, mid, lo)
    sub = g[Y0:Y1, X0:X1]
    sub[:] = sub * (1 - m[..., None]) + rgb * m[..., None]
    sub[:] = sub * (1 - ol[..., None]) + np.array(_f(out), np.float32) * ol[..., None]


def guy3d(f, x, y, s=1.0, la=(18, 8), ra=(18, 8), ll=7, rl=7, lean=0.0, sit=False, mouth=0, blink=False, brow="n", look=(0, 0),
          expr="n", bob=0.0, hold=None, hold_off=(0, 0), face_dir=1, op=1.0, shadow=True):
    """3D-look mascot, same API as guy(): (x, y) = feet baseline (or seat point when sit=True). Returns {side: hand point}."""
    g = f if op >= 0.999 else f.copy()
    lr = math.radians(lean)
    if not sit:
        hip = (x, y - 178 * s)
        if shadow: contact(g, x, y + 6 * s, 230 * s, 0.42)
        for side, ang in ((-1, ll), (1, rl)):
            hp = (hip[0] + side * 24 * s, hip[1] - 6 * s)
            ft = (hp[0] + side * math.sin(math.radians(ang)) * 158 * s, hp[1] + math.cos(math.radians(ang)) * 158 * s)
            _tube(g, hp, ft, 38 * s, PANT_HI, PANT_MID, PANT_LO)
            _poly_shaded(g, [(ft[0] - 22 * s, ft[1] - 8 * s), (ft[0] + 6 * s + side * 22 * s, ft[1] - 10 * s),
                             (ft[0] + 14 * s + side * 30 * s, ft[1] + 10 * s), (ft[0] - 24 * s, ft[1] + 12 * s)], SHOE_HI, SHOE_LO, SHOE_LO)
    else:
        hip = (x, y)
        for side in (-1, 1):
            hp = (hip[0] + side * 22 * s, hip[1]); kn = (hip[0] + side * 44 * s, hip[1] + 30 * s); ft = (hip[0] + side * 46 * s, hip[1] + 136 * s)
            _tube(g, hp, kn, 30 * s, PANT_HI, PANT_MID, PANT_LO); _tube(g, kn, ft, 28 * s, PANT_HI, PANT_MID, PANT_LO)
            _poly_shaded(g, [(ft[0] - 20 * s, ft[1] - 8 * s), (ft[0] + 20 * s + side * 10 * s, ft[1] - 8 * s),
                             (ft[0] + 24 * s + side * 16 * s, ft[1] + 12 * s), (ft[0] - 22 * s, ft[1] + 12 * s)], SHOE_HI, SHOE_LO, SHOE_LO)
    neck = (hip[0] + 168 * s * math.sin(lr), hip[1] - 168 * s * math.cos(lr))
    ux, uy = math.sin(lr), -math.cos(lr); px, py = -uy, ux        # up and side vectors along the lean
    P = lambda a, b: (hip[0] + ux * a + px * b, hip[1] + uy * a + py * b)
    sh_ = (neck[0] - ux * 24 * s, neck[1] - uy * 24 * s)
    hands = {}
    arms = []
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sp = (sh_[0] + side * 62 * s, sh_[1] + 6 * s)
        e = (sp[0] + side * math.sin(math.radians(a1)) * 86 * s, sp[1] + math.cos(math.radians(a1)) * 86 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 78 * s, e[1] + math.cos(math.radians(a2)) * 78 * s)
        arms.append((side, sp, e, hd)); hands[side] = hd
    # torso: tapered jacket (shoulders -> hips), shirt V, tie, lapels
    torso = [P(188 * s, -74 * s), P(196 * s, 0), P(188 * s, 74 * s), P(40 * s, 66 * s), P(-6 * s, 60 * s), P(-18 * s, 0), P(-6 * s, -60 * s), P(40 * s, -66 * s)]
    _poly_shaded(g, torso, SUIT_HI, SUIT_MID, SUIT_LO)
    _poly_shaded(g, [P(184 * s, -26 * s), P(184 * s, 26 * s), P(118 * s, 0)], (255, 255, 255), (238, 238, 244), (200, 204, 220), ow=2)
    tie = [P(178 * s, -8 * s), P(178 * s, 8 * s), P(164 * s, 6 * s), P(96 * s, 14 * s), P(80 * s, 0), P(96 * s, -14 * s), P(164 * s, -6 * s)]
    _poly_shaded(g, tie, TIE_HI, TIE_MID, TIE_LO, ow=2)
    for side in (-1, 1):
        _poly_shaded(g, [P(186 * s, side * 26 * s), P(186 * s, side * 44 * s), P(110 * s, side * 6 * s), P(120 * s, side * 2 * s)],
                     SUIT_MID, SUIT_LO, SUIT_LO, ow=2)
    for yb in (70, 38):
        cv2.circle(g, (int(P(yb * s, 0)[0]), int(P(yb * s, 0)[1])), max(2, int(5 * s)), _f((240, 200, 90)), -1, cv2.LINE_AA)   # buttons
    _poly_shaded(g, [P(150 * s, 30 * s), P(150 * s, 56 * s), P(138 * s, 56 * s), P(138 * s, 30 * s)], TIE_HI, TIE_MID, TIE_LO, ow=2)   # pocket square
    # arms (sleeves + cuffs + hands)
    for side, sp, e, hd in arms:
        _tube(g, sp, e, 36 * s, SUIT_HI, SUIT_MID, SUIT_LO); _tube(g, e, hd, 33 * s, SUIT_HI, SUIT_MID, SUIT_LO)
        v = np.array(hd) - np.array(e); v = v / (np.hypot(*v) or 1)
        cf = (hd[0] - v[0] * 10 * s, hd[1] - v[1] * 10 * s)
        cv2.circle(g, (int(cf[0]), int(cf[1])), int(16 * s), _f(OUT_), -1, cv2.LINE_AA)
        cv2.circle(g, (int(cf[0]), int(cf[1])), int(13 * s), _f((250, 250, 252)), -1, cv2.LINE_AA)
    if hold is not None:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    for side, sp, e, hd in arms:
        hx, hy = hd
        cv2.circle(g, (int(hx), int(hy + 4 * s)), int(23 * s), _f(OUT_), -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx), int(hy + 4 * s)), int(20 * s), _f(SKIN_MID), -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx - 4 * s), int(hy)), int(9 * s), _f(SKIN_HI), -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx + side * 17 * s), int(hy - 3 * s)), int(9 * s), _f(OUT_), -1, cv2.LINE_AA)   # thumb
        cv2.circle(g, (int(hx + side * 17 * s), int(hy - 3 * s)), int(6 * s), _f(SKIN_MID), -1, cv2.LINE_AA)
    hel = head3d_el(mouth, blink, brow, look[0], look[1], expr)
    comp(g, scale_el(hel, s * 1.0), neck[0], neck[1] - 92 * s + bob * s)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


_guy_flat, _head_flat = guy, head_el
if MASCOT3D:
    guy = guy3d            # noqa: F811 — every existing shot gets the new character
    head_el = head3d_el    # noqa: F811
