# ================= props: pineapple (whole / wedge / ring), enzyme critters, protein chain, mouth lining, acid drops,
# grill, generic can, jelly dessert, gelatin net, tingle zaps =================
PINE = (255, 206, 50); PINE_D = (222, 146, 18); PINE_IN = (255, 236, 120); RIND = (186, 120, 30)
CROWN = (70, 180, 80); CROWN_D = (24, 112, 52); ENZ = (236, 64, 160); ENZ_D = (160, 24, 110)
MUCUS = (200, 255, 226); TONGUE = (244, 120, 140); TONGUE_D = (196, 70, 96)
JELLY = (236, 40, 70); JELLY_D = (150, 10, 40)


def _outline(im, allm, k=15, col=INK):
    m = Image.new("L", im.size, 0); allm(ImageDraw.Draw(m))
    im.paste(Image.new("RGBA", im.size, tuple(col) + (255,)), (0, 0), m.filter(ImageFilter.MaxFilter(k)))
    return m


def _masked(im, mask, fn):
    """draw fn on a layer, keep it only inside mask."""
    L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L_))
    a = Image.fromarray(np.minimum(np.asarray(L_.getchannel("A")), np.asarray(mask)), "L"); L_.putalpha(a); im.alpha_composite(L_)


def _face(d, im, S, cx, cy, r, k_open, angry=True, ko=False, sc=2):
    """cartoon eyes + toothy mouth for food characters. k_open 0..1."""
    for ex in (cx - max(r * 0.42, 36), cx + max(r * 0.42, 36)):
        if ko:
            d.line(S(ex - 16, cy - 16, ex + 16, cy + 16), fill=INK + (255,), width=7 * sc)
            d.line(S(ex + 16, cy - 16, ex - 16, cy + 16), fill=INK + (255,), width=7 * sc); continue
        d.ellipse(S(ex - 26, cy - 30, ex + 26, cy + 30), fill=(255, 255, 255, 255), outline=INK + (255,), width=5 * sc)
        d.ellipse(S(ex - 11 + 6, cy - 8, ex + 11 + 6, cy + 16), fill=INK + (255,))
        d.ellipse(S(ex - 1, cy - 6, ex + 7, cy + 2), fill=(255, 255, 255, 255))
        if angry:
            sg = 1 if ex < cx else -1
            d.line(S(ex - 30 * sg, cy - 52, ex + 24 * sg, cy - 34), fill=INK + (255,), width=9 * sc)
    my = cy + r * 0.62; mw = r * 0.62; mh = 12 + 70 * k_open
    if ko:
        d.arc(S(cx - mw * 0.6, my - 6, cx + mw * 0.6, my + 30), 200, 340, fill=INK + (255,), width=7 * sc); return
    d.rounded_rectangle(S(cx - mw, my - mh / 2, cx + mw, my + mh / 2), int(min(mh / 2, 30)) * sc, fill=(70, 14, 24, 255), outline=INK + (255,), width=5 * sc)
    if k_open > 0.15:
        d.ellipse(S(cx - mw * 0.5, my + mh * 0.05, cx + mw * 0.5, my + mh / 2 - 2), fill=(236, 90, 110, 255))
    nt = 6; tw_ = 2 * mw / nt
    for i in range(nt):
        x0 = cx - mw + i * tw_
        d.polygon(S(x0 + 3, my - mh / 2 + 2, x0 + tw_ - 3, my - mh / 2 + 2, x0 + tw_ / 2, my - mh / 2 + 4 + 14 + 6 * k_open), fill=(255, 255, 255, 255))
        if k_open > 0.1:
            d.polygon(S(x0 + 3, my + mh / 2 - 2, x0 + tw_ - 3, my + mh / 2 - 2, x0 + tw_ / 2, my + mh / 2 - 4 - 14 - 6 * k_open), fill=(255, 255, 255, 255))


def pineapple_el(face=False, k_open=0.0, angry=True):
    k_open = round(clamp(k_open) * 5) / 5
    def mk():
        w, h, sc = 440, 760, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        leaves = [(-40, 230), (-20, 270), (0, 300), (20, 270), (40, 230), (-62, 170), (62, 170)]
        def crown(m):
            for ang, L in leaves:
                a = math.radians(ang); bx = 220; by = 300; tx = bx + math.sin(a) * L; ty = by - math.cos(a) * L
                m.polygon(S(bx - 26, by, tx, ty, bx + 26, by), fill=255)
        def body(m): m.ellipse(S(40, 250, 400, 750), fill=255)
        def allm(m): crown(m); body(m)
        _outline(im, allm, 15)
        shape_grad(im, crown, CROWN, CROWN_D)
        for ang, L in leaves[:5]:
            a = math.radians(ang); d.line(S(220, 296, 220 + math.sin(a) * L * 0.8, 296 - math.cos(a) * L * 0.8), fill=(150, 230, 140, 200), width=3 * sc)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        shape_grad(im, body, PINE, PINE_D)
        # diamond crosshatch + eyes, clipped to the body
        def hatch(q):
            for i in range(-12, 14):
                x0 = 220 + i * 62
                q.line(S(x0 - 300, 250, x0 + 300, 750 + 50), fill=RIND + (255,), width=5 * sc)
                q.line(S(x0 + 300, 250, x0 - 300, 750 + 50), fill=RIND + (255,), width=5 * sc)
            for i in range(-6, 8):
                for j in range(0, 18):
                    cx_ = 220 + i * 62 + (31 if j % 2 else 0); cy_ = 250 + j * 31
                    q.ellipse(S(cx_ - 6, cy_ - 5 + 15, cx_ + 6, cy_ + 7 + 15), fill=(140, 84, 20, 255))
        _masked(im, bm, hatch)
        _masked(im, bm, lambda q: q.ellipse(S(80, 300, 200, 470), fill=(255, 255, 255, 70)))
        if face: _face(d, im, S, 220, 470, 150, k_open, angry, sc=sc)
        return _done(im, w, h)
    return gcache(("pine", face, k_open, angry), mk)


def pine_wedge_el(face=False, k_open=0.0, bite=False):
    """pineapple wedge (rind at the bottom, core tip up)."""
    k_open = round(clamp(k_open) * 5) / 5
    def mk():
        w, h, sc = 300, 300, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            m.pieslice(S(-10, 40, 310, 360), 200, 340, fill=255)
        rm = lambda m: m.pieslice(S(-10, 40, 310, 360), 200, 340, fill=255)
        _outline(im, body, 13)
        shape_grad(im, body, PINE_IN, PINE)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        # rind arc on top edge of the pie (it is the outer arc)
        _masked(im, bm, lambda q: q.arc(S(-10, 40, 310, 360), 200, 340, fill=(200, 160, 40, 255), width=22 * sc))
        _masked(im, bm, lambda q: q.arc(S(4, 54, 296, 346), 200, 340, fill=(150, 110, 20, 255), width=5 * sc))
        for a in range(212, 340, 16):
            r = math.radians(a)
            _masked(im, bm, lambda q, r=r: q.line(S(150, 200, 150 + 130 * math.cos(r), 200 + 130 * math.sin(r)), fill=(240, 196, 60, 200), width=3 * sc))
        if bite: d.ellipse(S(180, 40, 280, 120), fill=(0, 0, 0, 0))
        if face: _face(d, im, S, 150, 120, 70, k_open, True, sc=sc)
        return _done(im, w, h)
    return gcache(("wedge", face, k_open, bite), mk)


def pine_ring_el(grill=False):
    def mk():
        w, h, sc = 320, 320, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(4, 4, 316, 316), fill=INK + (255,))
        d.ellipse(S(12, 12, 308, 308), fill=(214, 170, 40, 255))
        shape_grad(im, lambda m: m.ellipse(S(26, 26, 294, 294), fill=255), PINE_IN, PINE)
        for a in range(0, 360, 15):
            r = math.radians(a); d.line(S(160 + 62 * math.cos(r), 160 + 62 * math.sin(r), 160 + 130 * math.cos(r), 160 + 130 * math.sin(r)), fill=(240, 196, 60, 255), width=3 * sc)
        d.ellipse(S(98, 98, 222, 222), fill=INK + (255,))
        d.ellipse(S(106, 106, 214, 214), fill=(0, 0, 0, 0))
        if grill:
            gm = Image.new("L", im.size, 0); ImageDraw.Draw(gm).ellipse(S(26, 26, 294, 294), fill=255)
            ImageDraw.Draw(gm).ellipse(S(98, 98, 222, 222), fill=0)
            for i in range(-3, 4):
                _masked(im, gm, lambda q, i=i: q.line(S(20 + i * 60, 0, 300 + i * 60, 320), fill=(110, 56, 16, 235), width=16 * sc))
        _ov(im, lambda q: q.arc(S(36, 36, 284, 284), 200, 250, fill=(255, 255, 255, 140), width=8 * sc))
        return _done(im, w, h)
    return gcache(("ring", grill), mk)


def enzyme_el(k_open=0.5, ko=False, col=ENZ):
    """little pac-man enzyme critter with scissor teeth, facing right."""
    k_open = round(clamp(k_open) * 4) / 4
    def mk():
        w, h, sc = 150, 150, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        a = 4 + 34 * k_open if not ko else 2
        d.pieslice(S(4, 4, 146, 146), a, 360 - a, fill=INK + (255,))
        dark = tuple(int(c * 0.7) for c in col)
        shape_grad(im, lambda m: m.pieslice(S(11, 11, 139, 139), a, 360 - a, fill=255), tuple(min(255, c + 40) for c in col), dark)
        _ov(im, lambda q: q.ellipse(S(30, 26, 70, 54), fill=(255, 255, 255, 110)))
        if not ko and k_open > 0:
            for i in range(3):
                r1 = math.radians(a + 2); x0 = 75 + (20 + i * 18) * math.cos(r1); y0 = 75 + (20 + i * 18) * math.sin(r1)
                d.polygon(S(x0, y0, x0 + 12, y0 - 3, x0 + 4, y0 - 13), fill=(255, 255, 255, 255))
                r2 = math.radians(-a - 2); x0 = 75 + (20 + i * 18) * math.cos(r2); y0 = 75 + (20 + i * 18) * math.sin(r2)
                d.polygon(S(x0, y0, x0 + 12, y0 + 3, x0 + 4, y0 + 13), fill=(255, 255, 255, 255))
        if ko:
            for (p, q2) in (((62, 34), (82, 54)), ((82, 34), (62, 54))): d.line(S(*p, *q2), fill=INK + (255,), width=6 * sc)
        else:
            d.ellipse(S(56, 28, 90, 62), fill=(255, 255, 255, 255), outline=INK + (255,), width=3 * sc)
            d.ellipse(S(70, 38, 84, 54), fill=INK + (255,))
            d.line(S(52, 22, 92, 30), fill=INK + (255,), width=6 * sc)
        return _done(im, w, h)
    return gcache(("enz", k_open, ko, col), mk)


def enzyme(f, x, y, s, t, ko=False, flip=False, rot=0.0, rate=5.0, op=1.0):
    k = 0.5 + 0.5 * math.sin(t * rate * 2 * math.pi / 2)
    el = scale_el(enzyme_el(k, ko), s)
    if flip: el = (np.ascontiguousarray(el[0][:, ::-1]), np.ascontiguousarray(el[1][:, ::-1]))
    rot_comp(f, el, x, y, rot, 1.0, op, 0.25)


AMINO = [(40, 190, 200), (255, 196, 40), (250, 110, 150), (110, 120, 250), (120, 210, 90)]


def chain(f, pts, r=26, link=True, seed=0):
    for i in range(len(pts) - 1):
        if link and pts[i] is not None and pts[i + 1] is not None:
            cv2.line(f, (int(pts[i][0]), int(pts[i][1])), (int(pts[i + 1][0]), int(pts[i + 1][1])), C(INK), 9, cv2.LINE_AA)
    for i, p in enumerate(pts):
        if p is None: continue
        col = AMINO[(i + seed) % len(AMINO)]
        cv2.circle(f, (int(p[0]), int(p[1])), int(r + 5), C(INK), -1, cv2.LINE_AA)
        cv2.circle(f, (int(p[0]), int(p[1])), int(r), C(col), -1, cv2.LINE_AA)
        cv2.circle(f, (int(p[0] - r * 0.35), int(p[1] - r * 0.35)), max(2, int(r * 0.28)), (1, 1, 1), -1, cv2.LINE_AA)


HOLES = [(0.14, 0.9), (0.33, 1.1), (0.52, 0.8), (0.70, 1.0), (0.88, 0.85)]


def tissue(f, x, y, w, t, holes=0.0, sore=0.0, heal=0.0, mh=70, th=300):
    """mouth lining cross-section: mint mucus shield (top, thickness mh) over pink tongue tissue with papillae.
    holes 0..1 = chewed gaps in the mucus; sore 0..1 = red glow in gaps; heal 0..1 closes the gaps."""
    x0, x1 = int(x - w / 2), int(x + w / 2); ty = y + mh
    f[ty + 16:ty + th + 16, x0 + 16:x1 + 16] *= 0.7
    # tongue tissue
    g = np.linspace(0, 1, th)[:, None, None]
    f[ty:ty + th, x0:x1] = np.array(C(TONGUE), np.float32) * (1 - g) + np.array(C(TONGUE_D), np.float32) * g
    rng = np.random.default_rng(7)
    for i in range(16):
        cx = rng.uniform(x0 + 30, x1 - 30); cy = ty + rng.uniform(70, th - 30)
        cv2.circle(f, (int(cx), int(cy)), int(rng.uniform(10, 22)), C((230, 96, 120)), -1, cv2.LINE_AA)
    # papillae bumps along the top
    for i in range(int(w / 48) + 1):
        px = x0 + 24 + i * 48
        if px > x1 - 10: break
        cv2.ellipse(f, (int(px), int(ty + 4)), (20, 22), 0, 180, 360, C((250, 150, 166)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(px), int(ty + 4)), (20, 22), 0, 180, 360, C(TONGUE_D), 3, cv2.LINE_AA)
    # mucus layer (translucent) with gaps
    k = clamp(holes) * (1 - clamp(heal))
    gaps = []
    for (hx, hs) in HOLES:
        gw = 90 * hs * k
        if gw > 3:
            cx = x0 + hx * w; gaps.append((cx, gw))
    mask = np.zeros((H, W), np.float32); cv2.rectangle(mask, (x0, int(y)), (x1, int(ty)), 1.0, -1)
    for cx, gw in gaps: cv2.ellipse(mask, (int(cx), int(y - 4)), (int(gw), int(mh + 6)), 0, 0, 180, 0.0, -1, cv2.LINE_AA)
    f[:] = f * (1 - 0.82 * mask[..., None]) + np.array(C(MUCUS), np.float32) * 0.82 * mask[..., None]
    for i in range(14):  # slime bubbles
        bx = x0 + 30 + ((i * 97 + t * 30) % (w - 60)); by = y + 18 + (i * 13) % max(1, mh - 30)
        if mask[int(by), int(bx)] > 0.5: cv2.circle(f, (int(bx), int(by)), 6 + i % 3 * 2, C((255, 255, 255)), 2, cv2.LINE_AA)
    cv2.line(f, (x0, int(y)), (x1, int(y)), C((120, 200, 160)), 4, cv2.LINE_AA)
    if sore > 0.02:
        for cx, gw in gaps:
            glow(f, cx, ty + 6, gw * 1.8, (255, 30, 30), 0.9 * sore * (0.75 + 0.25 * math.sin(t * 14)))
            ov = f.copy(); cv2.ellipse(ov, (int(cx), int(ty + 2)), (int(gw * 0.8), 18), 0, 0, 360, C((220, 20, 40)), -1, cv2.LINE_AA); f[:] = f * (1 - 0.8 * sore) + ov * 0.8 * sore
    cv2.rectangle(f, (x0, int(y)), (x1, int(ty + th)), C(INK), 6, cv2.LINE_AA)
    return gaps


def drop_el(col=(200, 240, 60)):
    def mk():
        w, h, sc = 120, 170, 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m): m.ellipse(S(14, 60, 106, 156), fill=255); m.polygon(S(60, 4, 18, 92, 102, 92), fill=255)
        _outline(im, body, 13)
        shape_grad(im, body, tuple(min(255, c + 40) for c in col), tuple(int(c * 0.75) for c in col))
        _ov(im, lambda q: q.ellipse(S(32, 84, 54, 120), fill=(255, 255, 255, 170)))
        return _done(im, w, h)
    return gcache(("drop", col), mk)


def zaps(f, x, y, r, t, n=7, col=(255, 240, 80), amt=1.0, seed=0, upper=False):
    if amt <= 0.02: return
    rng = np.random.default_rng(seed + int(t * 12))
    ov = f.copy()
    for i in range(n):
        a = (math.pi * (1.08 + 0.84 * i / max(1, n - 1)) if upper else i * 2 * math.pi / n) + rng.uniform(-0.15, 0.15); r0 = r * 0.75; r1 = r * (1.15 + 0.25 * rng.random())
        pts = []
        for j in range(5):
            q = j / 4; rr = r0 + (r1 - r0) * q; jit = (rng.uniform(-9, 9) if 0 < j < 4 else 0)
            pts.append((x + rr * math.cos(a) - jit * math.sin(a), y + rr * math.sin(a) + jit * math.cos(a)))
        P = np.array(pts, np.int32)
        cv2.polylines(ov, [P], False, C(INK), 13, cv2.LINE_AA); cv2.polylines(ov, [P], False, C(col), 7, cv2.LINE_AA)
    f[:] = f * (1 - amt) + ov * amt


def flames(f, x, y, w, t, h_=150, op=1.0):
    ov = f.copy()
    for layer, (col, sc_) in enumerate((((255, 90, 20), 1.0), ((255, 170, 30), 0.72), ((255, 236, 120), 0.42))):
        for i in range(9):
            fx = x - w / 2 + (i + 0.5) * w / 9; hh = h_ * sc_ * (0.75 + 0.25 * math.sin(t * 13 + i * 1.7 + layer))
            bw = w / 9 * 0.75 * (0.6 + 0.4 * sc_)
            P = np.array([[fx - bw, y], [fx - bw * 0.5, y - hh * 0.5], [fx + 8 * math.sin(t * 9 + i), y - hh], [fx + bw * 0.5, y - hh * 0.5], [fx + bw, y]], np.int32)
            cv2.fillPoly(ov, [P], C(col), cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op


def grill(f, x, y, w, t):
    """grill: flames under a dark grate; y = grate top."""
    cv2.rectangle(f, (int(x - w / 2 - 30), int(y + 60)), (int(x + w / 2 + 30), int(y + 250)), C((50, 50, 58)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2 - 30), int(y + 60)), (int(x + w / 2 + 30), int(y + 250)), C(INK), 6, cv2.LINE_AA)
    glow(f, x, y + 40, w * 0.6, (255, 120, 30), 0.35)
    flames(f, x, y + 66, w, t, 120)
    for i in range(10):
        gx = x - w / 2 + i * w / 9
        cv2.line(f, (int(gx), int(y + 20)), (int(gx), int(y + 66)), C((30, 30, 34)), 10, cv2.LINE_AA)
    cv2.line(f, (int(x - w / 2 - 20), int(y + 30)), (int(x + w / 2 + 20), int(y + 30)), C((30, 30, 34)), 12, cv2.LINE_AA)
    cv2.line(f, (int(x - w / 2 - 20), int(y + 62)), (int(x + w / 2 + 20), int(y + 62)), C((30, 30, 34)), 12, cv2.LINE_AA)


def can_el():
    """generic food can, no brand: yellow label with a pineapple ring drawing."""
    def mk():
        w, h, sc = 300, 380, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(10, 30, 290, 370), 24 * sc, fill=INK + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(18, 36, 282, 362), 20 * sc, fill=255), (225, 228, 236), (150, 156, 170))
        shape_grad(im, lambda m: m.rectangle(S(18, 80, 282, 320), fill=255), (255, 216, 70), (240, 170, 20))
        d.rectangle(S(18, 80, 282, 104), fill=(40, 150, 80, 255)); d.rectangle(S(18, 296, 282, 320), fill=(40, 150, 80, 255))
        ring = _pil_from_el(pine_ring_el(), 130 * sc, 130 * sc); im.alpha_composite(ring, (int(85 * sc), int(118 * sc)))
        d.text((150 * sc, 274 * sc), "PINEAPPLE", font=font(F_BLACK, 30 * sc), fill=(150, 60, 20, 255), anchor="mm")
        d.ellipse(S(18, 14, 282, 58), fill=INK + (255,)); d.ellipse(S(24, 18, 276, 52), fill=(210, 214, 224, 255))
        d.ellipse(S(50, 24, 250, 46), outline=(160, 166, 180, 255), width=3 * sc)
        _ov(im, lambda q: q.rectangle(S(40, 110, 60, 300), fill=(255, 255, 255, 70)))
        return _done(im, w, h)
    return gcache("can", mk)


def plate_el():
    def mk():
        w, h, sc = 560, 140, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(4, 10, 556, 136), fill=INK + (255,))
        shape_grad(im, lambda m: m.ellipse(S(12, 14, 548, 128), fill=255), (255, 255, 255), (214, 218, 230))
        d.ellipse(S(90, 34, 470, 108), outline=(200, 204, 218, 255), width=4 * sc)
        return _done(im, w, h)
    return gcache("plate", mk)


def jelly_el(rings=False):
    """moulded jelly dessert (bundt shape with ridges), translucent red; rings=True shows pineapple rings set inside."""
    def mk():
        w, h, sc = 440, 360, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        def body(m):
            m.polygon(S(30, 350, 70, 110, 370, 110, 410, 350), fill=255)
            m.ellipse(S(70, 60, 370, 160), fill=255)
        _outline(im, body, 13)
        shape_grad(im, body, (255, 90, 110), JELLY_D)
        bm = Image.new("L", im.size, 0); body(ImageDraw.Draw(bm))
        if rings:
            for (rx, ry) in ((140, 250), (300, 250), (220, 170)):
                r_ = _pil_from_el(pine_ring_el(), 110 * sc, 110 * sc); a = r_.getchannel("A").point(lambda v: int(v * 0.65)); r_.putalpha(a)
                im.alpha_composite(r_, (int((rx - 55) * sc), int((ry - 55) * sc)))
        for i in range(7):
            xb = 70 + i * 50
            _masked(im, bm, lambda q, xb=xb: q.line(S(xb, 120, xb - (220 - xb) * 0.18, 350), fill=(120, 0, 30, 110), width=6 * sc))
        _masked(im, bm, lambda q: q.ellipse(S(100, 74, 210, 110), fill=(255, 255, 255, 150)))
        _masked(im, bm, lambda q: q.line(S(90, 150, 70, 320), fill=(255, 220, 230, 140), width=14 * sc))
        return _done(im, w, h)
    return gcache(("jelly", rings), mk)


def jelly(f, x, y, s, t, wob=0.0, melt=0.0, rings=False):
    """jelly sitting on a plate; (x, y) = plate centre. wob = wobble amplitude, melt 0..1 collapses into a puddle."""
    comp(f, scale_el(plate_el(), s), x, y)
    sx = 1 + 0.08 * wob * math.sin(t * 22) + 0.6 * melt; sy = 1 - 0.08 * wob * math.sin(t * 22) - 0.82 * melt
    if melt < 0.98:
        pm, a = jelly_el(rings); hh, ww = a.shape
        nw, nh = max(2, int(ww * s * sx)), max(2, int(hh * s * sy))
        el = (cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_AREA), cv2.resize(a, (nw, nh), interpolation=cv2.INTER_AREA))
        comp(f, el, x, y - nh / 2 + 14 * s, op=1 - clamp((melt - 0.7) / 0.3))
    if melt > 0.3:
        k = clamp((melt - 0.3) / 0.5); ov = f.copy()
        cv2.ellipse(ov, (int(x), int(y - 6 * s)), (int(250 * s * (0.6 + 0.4 * k)), int(46 * s)), 0, 0, 360, C(JELLY_D), -1, cv2.LINE_AA)
        cv2.ellipse(ov, (int(x), int(y - 12 * s)), (int(236 * s * (0.6 + 0.4 * k)), int(36 * s)), 0, 0, 360, C(JELLY), -1, cv2.LINE_AA)
        cv2.ellipse(ov, (int(x - 80 * s), int(y - 22 * s)), (int(60 * s), int(9 * s)), 0, 0, 360, C((255, 170, 180)), -1, cv2.LINE_AA)
        f[:] = f * (1 - k) + ov * k


def gel_net(f, x, y, w, h, t, cut=0.0, seed=2):
    """gelatin = a net of protein strands (wavy). cut 0..1 removes strands, pieces fall."""
    rng = np.random.default_rng(seed)
    nx, ny = 7, 6
    segs = []
    for j in range(ny):
        for i in range(nx - 1): segs.append(((i, j), (i + 1, j)))
    for i in range(nx):
        for j in range(ny - 1): segs.append(((i, j), (i, j + 1)))
    order = rng.permutation(len(segs))
    P = lambda i, j: (x - w / 2 + i * w / (nx - 1) + 10 * math.sin(t * 2 + j + i * 0.7), y - h / 2 + j * h / (ny - 1) + 10 * math.cos(t * 2.3 + i))
    ncut = int(len(segs) * clamp(cut))
    cutset = set(order[:ncut].tolist())
    for si, ((i0, j0), (i1, j1)) in enumerate(segs):
        a = P(i0, j0); b = P(i1, j1)
        if si in cutset:
            rank = int(np.where(order == si)[0][0]); q = clamp((cut * len(segs) - rank) / 6)
            dy = 260 * q * q; op = 1 - q
            if op <= 0.02: continue
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            a = (a[0] + (mid[0] - a[0]) * 0.25, a[1] + dy); b = (b[0] + (mid[0] - b[0]) * 0.25, b[1] + dy)
        pts = []
        for k in range(9):
            q2 = k / 8; px = a[0] + (b[0] - a[0]) * q2; py = a[1] + (b[1] - a[1]) * q2
            nxv, nyv = -(b[1] - a[1]), (b[0] - a[0]); L = math.hypot(nxv, nyv) + 1e-6
            wv = 10 * math.sin(q2 * math.pi * 2 + si)
            pts.append((px + nxv / L * wv, py + nyv / L * wv))
        A = np.array(pts, np.int32)
        cv2.polylines(f, [A], False, C(INK), 15, cv2.LINE_AA); cv2.polylines(f, [A], False, C((255, 120, 140)), 9, cv2.LINE_AA)
    for i in range(nx):
        for j in range(ny):
            p = P(i, j); cv2.circle(f, (int(p[0]), int(p[1])), 13, C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(p[0]), int(p[1])), 9, C((255, 200, 60)), -1, cv2.LINE_AA)


def sparkles(f, pts, t, s=1.0, col=(255, 255, 255)):
    for i, (x, y) in enumerate(pts):
        k = 0.5 + 0.5 * math.sin(t * 8 + i * 1.3); r = (10 + 16 * k) * s
        P = np.array([[x, y - r], [x + r * 0.25, y - r * 0.25], [x + r, y], [x + r * 0.25, y + r * 0.25], [x, y + r], [x - r * 0.25, y + r * 0.25], [x - r, y], [x - r * 0.25, y - r * 0.25]], np.int32)
        cv2.fillPoly(f, [P], C(col), cv2.LINE_AA)
