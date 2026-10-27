# ================= FreshNestHub mascot "Chubby": round head, big round belly, stick arms + legs =================
CH_SKIN = (255, 222, 192); CH_ORANGE = (255, 150, 52); CH_SHIRT = (16, 190, 130); CH_SHIRT2 = (8, 150, 104)


def _tint(k):
    k = round(clamp(k) * 10) / 10
    return k, tuple(int(a + (b - a) * k) for a, b in zip(CH_SKIN, CH_ORANGE))


def chub_head_el(mouth=0, blink=False, brow="n", lx=0, ly=0, expr="n", tint=0.0, nose=None, cap=False):
    tint, skin = _tint(tint)
    if nose is not None: nose = round(clamp(nose) * 10) / 10
    key = ("chead", mouth, blink, brow, lx, ly, expr, tint, nose, cap)
    if key in _gc: return _gc[key]
    sc = 3; w, h = 230, 236
    im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * sc for x in v]
    cx, cy, R0 = 115, 128, 92
    # hair curl
    d.arc(S(98, 6, 132, 40), 150, 420, fill=INK + (255,), width=7 * sc)
    d.arc(S(108, 16, 124, 32), 200, 470, fill=INK + (255,), width=6 * sc)
    d.ellipse(S(cx - R0, cy - R0, cx + R0, cy + R0), fill=INK + (255,))
    d.ellipse(S(cx - R0 + 7, cy - R0 + 7, cx + R0 - 7, cy + R0 - 7), fill=skin + (255,))
    # soft shading + shine
    sh = Image.new("L", im.size, 0); ImageDraw.Draw(sh).ellipse(S(cx - R0 + 7, cy - R0 + 7, cx + R0 - 7, cy + R0 - 7), fill=255)
    yy, xx = np.mgrid[0:im.size[1], 0:im.size[0]].astype(np.float32) / sc
    grad = np.clip((np.hypot(xx - (cx - 30), yy - (cy - 36)) - 70) * 1.3, 0, 46).astype(np.uint8)
    im.paste(Image.new("RGBA", im.size, (150, 90, 60, 255)), (0, 0), Image.fromarray(np.minimum(np.asarray(sh), grad), "L"))
    _ov(im, lambda q: q.ellipse(S(52, 58, 96, 80), fill=(255, 255, 255, 140)))
    # cheeks
    for ex in (66, 164): _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 18, 148, ex + 18, 166), fill=(255, 110, 110, 110)))
    # eyes: big whites + pupils
    ox, oy = lx * 6, ly * 5
    for ex in (86, 144):
        ey = 116
        if blink or expr == "happy":
            d.arc(S(ex - 16, ey - 10, ex + 16, ey + 14), 200, 340, fill=INK + (255,), width=6 * sc)
            continue
        rx, ry = (19, 24) if expr == "wow" else (16, 20)
        d.ellipse(S(ex - rx, ey - ry, ex + rx, ey + ry), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
        pr = 7 if expr == "wow" else 9
        px, py = ex + ox, ey + 3 + oy
        d.ellipse(S(px - pr, py - pr, px + pr, py + pr), fill=INK + (255,))
        d.ellipse(S(px - 3, py - pr + 2, px + 2, py - pr + 7), fill=(255, 255, 255, 255))
        if expr == "sus": d.rectangle(S(ex - rx - 2, ey - ry - 2, ex + rx + 2, ey - 4), fill=skin + (255,)); d.line(S(ex - rx, ey - 4, ex + rx, ey - 4), fill=INK + (255,), width=5 * sc)
        if expr == "sleepy":   # ep 14: heavy drooping lids + tired bags (character acting: tiredness you can SEE)
            d.chord(S(ex - rx - 3, ey - ry - 3, ex + rx + 3, ey + ry + 3), 180, 360, fill=skin + (255,))
            d.rectangle(S(ex - rx - 3, ey - 2, ex + rx + 3, ey + 3), fill=skin + (255,))
            d.arc(S(ex - rx - 1, ey - 8, ex + rx + 1, ey + 10), 180, 360, fill=INK + (255,), width=6 * sc)
            d.arc(S(ex - rx + 2, ey + ry - 6, ex + rx - 2, ey + ry + 8), 20, 160, fill=(150, 110, 160, 255), width=4 * sc)
    # brows
    for i, ex in enumerate((86, 144)):
        if brow == "up": pts = [(ex - 16, 84), (ex + 14, 80)] if i == 0 else [(ex - 14, 80), (ex + 16, 84)]
        elif brow == "sus": pts = [(ex - 16, 88), (ex + 14, 95)] if i == 0 else [(ex - 14, 95), (ex + 16, 88)]
        elif brow == "sad": pts = [(ex - 16, 95), (ex + 14, 86)] if i == 0 else [(ex - 14, 86), (ex + 16, 95)]
        else: pts = [(ex - 15, 90), (ex + 14, 88)] if i == 0 else [(ex - 14, 88), (ex + 15, 90)]
        d.line([(p[0] * sc, p[1] * sc) for p in pts], fill=INK + (255,), width=7 * sc)
    if nose is not None:
        nc = tuple(int(a + (b - a) * nose) for a, b in zip(skin, CH_ORANGE))
        d.ellipse(S(101, 128, 129, 150), fill=nc + (255,), outline=INK + (255,), width=4 * sc)
        _ov(im, lambda q: q.ellipse(S(107, 132, 116, 139), fill=(255, 255, 255, 150)))
    if cap:  # leather flying cap + goggles pushed up
        d.chord(S(cx - R0 - 4, cy - R0 - 6, cx + R0 + 4, cy + R0 - 10), 180, 360, fill=(120, 72, 40, 255), outline=INK + (255,), width=5 * sc)
        for ex in (84, 146):
            d.ellipse(S(ex - 22, 46, ex + 22, 86), fill=(60, 120, 150, 255), outline=INK + (255,), width=5 * sc)
            _ov(im, lambda q, ex=ex: q.ellipse(S(ex - 12, 54, ex - 2, 66), fill=(200, 240, 255, 200)))
        d.line(S(106, 66, 124, 66), fill=INK + (255,), width=6 * sc)
    # mouth
    mx, my = 115, 166
    if expr == "wow" and mouth == 0: mouth = "o"
    if mouth == 0:
        if expr == "sad": d.arc(S(mx - 20, my - 2, mx + 20, my + 20), 200, 340, fill=INK + (255,), width=6 * sc)
        elif expr == "smirk": d.arc(S(mx - 22, my - 16, mx + 20, my + 10), 10, 120, fill=INK + (255,), width=6 * sc)
        elif expr == "happy": d.chord(S(mx - 24, my - 16, mx + 24, my + 20), 0, 180, fill=(60, 16, 20, 255)); d.chord(S(mx - 14, my + 2, mx + 14, my + 20), 0, 180, fill=(236, 90, 96, 255))
        else: d.arc(S(mx - 22, my - 16, mx + 22, my + 10), 20, 160, fill=INK + (255,), width=6 * sc)
    elif mouth == "o":
        d.ellipse(S(mx - 11, my - 8, mx + 11, my + 16), fill=(60, 16, 20, 255))
    else:
        hh = {1: 9, 2: 15, 3: 21}[mouth]; ww = {1: 16, 2: 20, 3: 23}[mouth]
        d.rounded_rectangle(S(mx - ww, my - 6, mx + ww, my - 6 + hh * 1.6), int(hh * 0.8) * sc, fill=(60, 16, 20, 255))
        if mouth >= 2: d.ellipse(S(mx - ww * 0.6, my - 6 + hh * 0.9, mx + ww * 0.6, my - 6 + hh * 1.7), fill=(236, 90, 96, 255))
        d.rectangle(S(mx - ww + 6, my - 6, mx + ww - 6, my - 1), fill=(255, 255, 255, 255))
    el = el_from(im.resize((w, h), Image.LANCZOS))
    if len(_gc) < 900: _gc[key] = el
    return el


def chub_body_el(shirt=CH_SHIRT, logo=True):
    def mk():
        w, h, sc = 300, 270, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(8, 8, 292, 262), fill=INK + (255,))
        dark = tuple(int(c * 0.72) for c in shirt)
        shape_grad(im, lambda m: m.ellipse(S(15, 15, 285, 255), fill=255), tuple(min(255, c + 30) for c in shirt), dark)
        _ov(im, lambda q: q.ellipse(S(60, 40, 170, 120), fill=(255, 255, 255, 60)))
        # belly + collar
        _ov(im, lambda q: q.ellipse(S(84, 116, 216, 240), fill=(255, 255, 255, 36)))
        d.arc(S(112, 6, 188, 46), 20, 160, fill=INK + (255,), width=6 * sc)
        if logo:
            d.ellipse(S(128, 140, 172, 184), fill=(255, 255, 255, 255))
            d.polygon(S(150, 148, 164, 162, 150, 176, 136, 162), fill=shirt + (255,))
        return _done(im, w, h)
    return gcache(("cbody", shirt, logo), mk)


def chub(f, x, y, s=1.0, la=(20, 10), ra=(20, 10), ll=6, rl=6, mouth=0, blink=False, brow="n", look=(0, 0), expr="n", tint=0.0,
         hold=None, hold_off=(0, 0), hold_l=None, bob=0.0, op=1.0, shirt=CH_SHIRT, shadow=True, lean=0.0, squash=0.0, sit=False, nose=None, cap=False, hold_front=False):
    """chubby stick mascot. (x, y) = feet baseline. arm angles (upper, fore) in degrees from straight down, positive = outward."""
    g = f if op >= 0.999 else f.copy()
    tint_k, skin = _tint(tint)
    ink = C(INK); th = max(2, 12 * s)
    sq = 1 + 0.12 * squash
    if shadow: contact(g, x, y + 4 * s, 260 * s, 0.32)
    # legs (short) — drawn first, body covers the hips
    hipy = y - 120 * s * (1 / sq)
    feet = {}
    for side, ang in ((-1, ll), (1, rl)):
        hx_ = x + side * 54 * s
        if sit:
            kn = (hx_ + side * 30 * s, hipy + 20 * s); ft = (hx_ + side * 40 * s, y)
            _seg(g, (hx_, hipy), kn, th, ink); _seg(g, kn, ft, th, ink)
        else:
            ft = (hx_ + side * math.sin(math.radians(ang)) * 120 * s, hipy + math.cos(math.radians(ang)) * 120 * s)
            _seg(g, (hx_, hipy), ft, th, ink)
        feet[side] = ft
        cv2.ellipse(g, (int(ft[0] + side * 12 * s), int(ft[1] - 2 * s)), (int(30 * s), int(15 * s)), 0, 0, 360, ink, -1, cv2.LINE_AA)
        cv2.ellipse(g, (int(ft[0] + side * 12 * s), int(ft[1] - 3 * s)), (int(25 * s), int(10 * s)), 0, 0, 360, C(skin), -1, cv2.LINE_AA)
    # body
    lr = math.radians(lean)
    bcx = x + 40 * s * math.sin(lr); bcy = y - 215 * s / sq + bob * s * 0.5
    bs = s
    pm, a = chub_body_el(shirt)
    el = scale_el((pm, a), bs)
    if abs(sq - 1) > 1e-3:
        el = (cv2.resize(el[0], (int(el[0].shape[1] * (1 + 0.1 * squash)), int(el[0].shape[0] / sq))),
              cv2.resize(el[1], (int(el[1].shape[1] * (1 + 0.1 * squash)), int(el[1].shape[0] / sq))))
    hands = {}
    # arms behind? no — arms in front of the body
    comp(g, el, bcx, bcy)
    for side, (a1, a2) in ((-1, la), (1, ra)):
        sh_ = (bcx + side * 118 * s, bcy - 46 * s)
        e = (sh_[0] + side * math.sin(math.radians(a1)) * 76 * s, sh_[1] + math.cos(math.radians(a1)) * 76 * s)
        hd = (e[0] + side * math.sin(math.radians(a2)) * 70 * s, e[1] + math.cos(math.radians(a2)) * 70 * s)
        _seg(g, sh_, e, th, ink); _seg(g, e, hd, th, ink)
        hands[side] = hd
    if hold is not None and not hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
    if hold_l is not None:
        hx, hy = hands[-1]; comp(g, hold_l, hx - hold_off[0] * s, hy + hold_off[1] * s)
    for side in (-1, 1):
        hx, hy = hands[side]
        cv2.circle(g, (int(hx), int(hy)), int(19 * s), ink, -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx), int(hy)), int(14 * s), C(skin), -1, cv2.LINE_AA)
    hel = chub_head_el(mouth, blink, brow, look[0], look[1], expr, tint, nose, cap)
    comp(g, scale_el(hel, s), bcx + 10 * s * math.sin(lr), bcy - 205 * s / sq + bob * s)
    if hold is not None and hold_front:
        hx, hy = hands[1]; comp(g, hold, hx + hold_off[0] * s, hy + hold_off[1] * s)
        cv2.circle(g, (int(hx), int(hy)), int(19 * s), ink, -1, cv2.LINE_AA)
        cv2.circle(g, (int(hx), int(hy)), int(14 * s), C(skin), -1, cv2.LINE_AA)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return hands


def chub_head_only(f, x, y, s, t=0.0, mouth=None, expr="n", brow="n", look=(0, 0), tint=0.0, blink=None, nose=None, cap=False, op=1.0):
    m = talk(t) if mouth is None else mouth
    b = blink_at(t, 1) if blink is None else blink
    comp(f, scale_el(chub_head_el(m, b, brow, look[0], look[1], expr, tint, nose, cap), s), x, y, op=op)


# ---------------- FreshNestHub logo with Chubby's head ----------------
def logo_el():
    def mk():
        w, h, sc = 940, 380, 2; im, d = _canvas(w, h)
        hp = _pil_from_el(chub_head_el(2, False, "up", 0, 0, "happy"), 190 * sc, 195 * sc); im.alpha_composite(hp, (int(10 * sc), int(30 * sc)))
        fo = font(F_BLACK, 150 * sc); x = 215 * sc
        for ch in "FRESH": d.text((x, 128 * sc), ch, font=fo, fill=CH_SHIRT + (255,), anchor="lm"); x += fo.getlength(ch) - 4 * sc
        d.text((219 * sc, 272 * sc), "NEST HUB", font=font(F_BLACK, 112 * sc), fill=INK + (255,), anchor="lm")
        return _done(im, w, h)
    return gcache("logo_fnh2", mk)
