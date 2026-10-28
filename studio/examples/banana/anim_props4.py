# ================= props for "Almost every banana is the same clone" (generic: no real logos, no brand stickers) =================
BAN = (255, 214, 48); BAN_D = (214, 160, 20); BAN_G = (176, 200, 60); BROWNB = (96, 62, 30)
LEAF = (46, 168, 70); LEAF_D = (22, 110, 48); SICK = (176, 150, 54); DEAD = (110, 82, 40)
OCEAN_A = (18, 84, 168); OCEAN_B = (40, 140, 214); LAND = (92, 186, 96); LAND_D = (56, 140, 72)


def _mixc(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def banana_el(w=360, col=BAN, brown=0.0, spots=0.0, label=None, seed=0):
    """generic curved banana (stem on the left, dark tip on the right), lit along the outer curve. brown 0..1 = dying."""
    def mk():
        sc = 2; h = int(w * 0.5); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        c0 = _mixc(col, BROWNB, brown); c_hi = _mixc(c0, (255, 255, 230), 0.35); c_lo = _mixc(c0, (120, 80, 10), 0.35)
        cx, cy = w * 0.5, h * 1.85; Rm = h * 1.5; T = h * 0.6
        a0, a1 = math.radians(226), math.radians(314)
        out, inn, mid = [], [], []
        for i in range(41):
            u = i / 40; a = a0 + (a1 - a0) * u; th = (math.sin(math.pi * (0.06 + 0.88 * u)) ** 0.55) * T / 2
            ca, sa = math.cos(a), math.sin(a)
            out.append((cx + (Rm + th) * ca, cy + (Rm + th) * sa)); inn.append((cx + (Rm - th) * ca, cy + (Rm - th) * sa))
            mid.append((cx + (Rm + th * 0.35) * ca, cy + (Rm + th * 0.35) * sa))
        poly = out + inn[::-1]
        _ov(im, lambda q: q.polygon([(x * sc + 8 * sc, y * sc + 10 * sc) for x, y in poly], fill=(0, 0, 0, 60)))
        d.polygon([(x * sc, y * sc) for x, y in poly], fill=c_lo + (255,))
        hi = out + mid[::-1]; d.polygon([(x * sc, y * sc) for x, y in hi], fill=c0 + (255,))
        d.line([(x * sc, y * sc) for x, y in out[4:-6]], fill=c_hi + (255,), width=int(T * 0.12 * sc))
        d.line([(x * sc, y * sc) for x, y in mid[3:-3]], fill=_mixc(c0, (150, 110, 20), 0.3) + (255,), width=2 * sc)   # ridge
        d.polygon([(x * sc, y * sc) for x, y in poly], outline=INK + (255,), width=4 * sc)
        # stem (left end) and tip (right end)
        sx0, sy0 = out[0]; ix0, iy0 = inn[0]; bx, by = (sx0 + ix0) / 2, (sy0 + iy0) / 2
        stem_c = _mixc((120, 150, 50), BROWNB, brown)
        d.polygon(S(bx - 4, by - 9, bx - 34, by - 30, bx - 44, by - 18, bx - 4, by + 9), fill=stem_c + (255,), outline=INK + (255,))
        d.rounded_rectangle(S(bx - 54, by - 32, bx - 30, by - 12), 4 * sc, fill=_mixc((90, 70, 40), (40, 30, 20), brown) + (255,), outline=INK + (255,), width=2 * sc)
        tx, ty = (out[-1][0] + inn[-1][0]) / 2, (out[-1][1] + inn[-1][1]) / 2
        d.ellipse(S(tx - 9, ty - 9, tx + 9, ty + 9), fill=(50, 36, 22, 255))
        rng = np.random.RandomState(seed + 3)
        nsp = int(spots * 14 + brown * 26)
        for _ in range(nsp):
            j = rng.randint(4, 37); x, y = mid[j]; r = rng.uniform(2, 5 + 6 * brown)
            x += rng.uniform(-T * 0.25, T * 0.25); y += rng.uniform(-T * 0.18, T * 0.18)
            d.ellipse(S(x - r, y - r * 0.8, x + r, y + r * 0.8), fill=(70, 46, 22, int(150 + 100 * brown)))
        if label:
            lx, ly = mid[20]; lx_ = lx; ly_ = ly - T * 0.02
            fn = font(F_BLACK, int(T * 0.24) * sc)
            tw = fn.getlength(label) / sc + 22
            d.rounded_rectangle(S(lx_ - tw / 2, ly_ - T * 0.2, lx_ + tw / 2, ly_ + T * 0.2), int(T * 0.2) * sc, fill=(255, 255, 255, 255), outline=(40, 110, 200, 255), width=3 * sc)
            d.text((lx_ * sc, ly_ * sc), label, font=fn, fill=(40, 90, 180, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("banana", w, col, round(brown, 2), round(spots, 2), label, seed), mk)


def bunch_el(w=420, n=5, col=BAN, brown=0.0, label=None):
    """a hand of bananas fanned from one crown (generic)"""
    def mk():
        h = int(w * 0.9); f = np.zeros((h, w, 3), np.float32); a = np.zeros((h, w), np.float32)
        out = (f, a)
        for i in range(n):
            ang = -38 + 76 * i / max(1, n - 1)
            el = banana_el(int(w * 0.62), col, brown, 0.15, label if i == n // 2 else None, seed=i)
            pm, al = el; hh, ww = al.shape
            D = int(math.hypot(ww, hh)) + 4
            M = cv2.getRotationMatrix2D((ww * 0.12, hh * 0.25), ang - 62, 1.0)
            M[0, 2] += w * 0.5 - ww * 0.12; M[1, 2] += h * 0.24 - hh * 0.25
            pm2 = cv2.warpAffine(pm, M, (w, h)); a2 = cv2.warpAffine(al, M, (w, h))
            f[:] = f * (1 - a2[..., None]) + pm2; a[:] = a + a2 * (1 - a)
        cv2.ellipse(f, (int(w * 0.5), int(h * 0.2)), (int(w * 0.07), int(w * 0.05)), 0, 0, 360, C(_mixc((110, 130, 50), BROWNB, brown)), -1, cv2.LINE_AA)
        cv2.ellipse(a, (int(w * 0.5), int(h * 0.2)), (int(w * 0.07), int(w * 0.05)), 0, 0, 360, 1.0, -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(w * 0.5), int(h * 0.2)), (int(w * 0.07), int(w * 0.05)), 0, 0, 360, C(INK), 3, cv2.LINE_AA)
        return out
    return gcache(("bunch", w, n, col, round(brown, 2), label), mk)


def slice_el(w=300, dots=True):
    """banana cross-section: cream disc, faint 3-part core, tiny dark dots that are not real seeds"""
    def mk():
        sc = 2; im, d = _canvas(w, w); S = lambda *v: [x * sc for x in v]
        c = w / 2
        _ov(im, lambda q: q.ellipse(S(10, 14, w - 2, w + 2), fill=(0, 0, 0, 60)))
        d.ellipse(S(4, 4, w - 8, w - 8), fill=(250, 238, 190, 255), outline=(214, 186, 90, 255), width=8 * sc)
        d.ellipse(S(w * 0.2, w * 0.2, w * 0.8 - 8, w * 0.8 - 8), fill=(252, 246, 212, 255))
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.line(S(c - 4, c - 4, c - 4 + w * 0.17 * math.cos(a), c - 4 + w * 0.17 * math.sin(a)), fill=(226, 206, 140, 255), width=3 * sc)
        if dots:
            for k in range(9):
                a = math.radians(20 + 40 * k); r = w * (0.09 if k % 2 else 0.14)
                x, y = c - 4 + r * math.cos(a), c - 4 + r * math.sin(a)
                rd = max(4, w * 0.016); d.ellipse(S(x - rd, y - rd, x + rd, y + rd), fill=(60, 40, 30, 255))
        return _done(im, w, w)
    return gcache(("slice", w, dots), mk)


def copier_el(w=560, flash=0.0):
    """generic office photocopier with an output tray on the right (no brand)"""
    def mk():
        sc = 2; h = int(w * 0.95); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        bw = w * 0.74
        _ov(im, lambda q: q.rounded_rectangle(S(14, h * 0.22 + 14, bw + 14, h - 2), 24 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(6, h * 0.22, bw, h - 14), 24 * sc, fill=255), (246, 244, 236), (196, 196, 204))
        d.rounded_rectangle(S(6, h * 0.22, bw, h - 14), 24 * sc, outline=INK + (255,), width=5 * sc)
        for k in range(3):   # paper drawers
            y = h * (0.5 + 0.14 * k)
            d.rounded_rectangle(S(28, y, bw - 24, y + h * 0.11), 10 * sc, fill=(226, 226, 232, 255), outline=INK + (255,), width=3 * sc)
            d.rounded_rectangle(S(bw * 0.4, y + h * 0.035, bw * 0.6, y + h * 0.06), 6 * sc, fill=(90, 90, 100, 255))
        # lid + glass
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, h * 0.12, bw + 6, h * 0.24), 14 * sc, fill=255), (120, 124, 136), (70, 72, 84))
        d.rounded_rectangle(S(0, h * 0.12, bw + 6, h * 0.24), 14 * sc, outline=INK + (255,), width=5 * sc)
        # control panel
        d.rounded_rectangle(S(bw * 0.52, h * 0.27, bw - 18, h * 0.42), 10 * sc, fill=(60, 64, 76, 255), outline=INK + (255,), width=3 * sc)
        d.rounded_rectangle(S(bw * 0.56, h * 0.29, bw * 0.82, h * 0.36), 6 * sc, fill=(120, 230, 200, 255))
        d.ellipse(S(bw * 0.86, h * 0.3, bw * 0.95, h * 0.39), fill=(50, 210, 90, 255), outline=INK + (255,), width=2 * sc)
        # output tray
        d.polygon(S(bw - 4, h * 0.44, w - 4, h * 0.40, w - 4, h * 0.45, bw - 4, h * 0.5), fill=(200, 200, 210, 255), outline=INK + (255,))
        return _done(im, w, h)
    return gcache(("copier", w), mk)


def leaf_poly(bx, by, ang, L, Wd, droop, n=16):
    """leaf outline along a curved midrib: angle in degrees (0 = right, -90 = up); droop pulls the tip down"""
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a)
    mid = [(bx + dx * L * u, by + dy * L * u + droop * L * u * u) for u in (i / n for i in range(n + 1))]
    left, right = [], []
    for i, (x, y) in enumerate(mid):
        u = i / n; wd = Wd / 2 * (math.sin(math.pi * min(1, u * 1.05)) ** 0.7)
        if i < n: tx, ty = mid[i + 1][0] - x, mid[i + 1][1] - y
        else: tx, ty = x - mid[i - 1][0], y - mid[i - 1][1]
        nl = math.hypot(tx, ty) + 1e-6; nx, ny = -ty / nl, tx / nl
        left.append((x + nx * wd, y + ny * wd)); right.append((x - nx * wd, y - ny * wd))
    return left + right[::-1], mid


def plant_el(h=900, sick=0.0, fruit=True, seed=0):
    """banana plant: tapered pseudostem, big paddle leaves (droop + yellow-brown with sick), optional hanging bunch"""
    def mk():
        sc = 2; w = int(h * 0.95); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cx, base, top = w * 0.5, h - 6, h * 0.42
        rng = np.random.RandomState(seed)
        stem_hi = _mixc((150, 176, 70), DEAD, sick * 0.8); stem_lo = _mixc((90, 120, 50), DEAD, sick * 0.8)
        shape_grad(im, lambda m: m.polygon(S(cx - w * 0.07, base, cx + w * 0.07, base, cx + w * 0.035, top, cx - w * 0.035, top), fill=255), stem_hi, stem_lo)
        d.polygon(S(cx - w * 0.07, base, cx + w * 0.07, base, cx + w * 0.035, top, cx - w * 0.035, top), outline=INK + (255,), width=3 * sc)
        for k in range(4):
            y = base - (base - top) * (0.2 + 0.2 * k)
            d.line(S(cx - w * 0.05, y, cx + w * 0.04, y - 18), fill=(70, 96, 40, 160), width=2 * sc)
        angs = [-150, -122, -95, -70, -40, -168, -12]
        for i, a in enumerate(angs):
            L = h * (0.52 - 0.05 * abs(a + 90) / 80) * rng.uniform(0.9, 1.05)
            drp = 0.25 + 0.55 * sick + 0.15 * (abs(a + 90) / 80)
            a2 = a + sick * (40 if a > -90 else -40) * 0.8
            col = _mixc(LEAF, SICK, clamp(sick * 1.4 - 0.1 * i)); col = _mixc(col, DEAD, clamp(sick * 1.2 - 0.5))
            poly, mid = leaf_poly(cx, top + 10, a2, L, h * 0.13, drp)
            d.polygon([(x * sc, y * sc) for x, y in poly], fill=col + (255,), outline=_mixc(LEAF_D, DEAD, sick) + (255,))
            d.line([(x * sc, y * sc) for x, y in mid], fill=_mixc((200, 230, 120), (200, 170, 90), sick) + (255,), width=3 * sc)
            for j in range(3, 14, 3):   # side veins / tears
                x, y = mid[j]
                d.line(S(x, y, x + (poly[j][0] - x) * 0.9, y + (poly[j][1] - y) * 0.9), fill=_mixc(LEAF_D, DEAD, sick) + (200,), width=2 * sc)
        if fruit:
            fx, fy = cx + w * 0.07, top + h * 0.06
            d.line(S(cx + 8, top + 20, fx + 30, fy + 20), fill=stem_lo + (255,), width=8 * sc)
            for r in range(4):
                for c in range(3 + (r < 2)):
                    x = fx + 4 + c * 26 - r * 4; y = fy + 30 + r * 34
                    d.rounded_rectangle(S(x, y, x + 20, y + 42), 9 * sc, fill=_mixc(BAN_G, DEAD, sick) + (255,), outline=INK + (255,), width=2 * sc)
            d.ellipse(S(fx + 14, fy + 170, fx + 52, fy + 222), fill=(130, 40, 70, 255), outline=INK + (255,), width=2 * sc)
        return _done(im, w, h)
    return gcache(("plant", h, round(sick, 2), fruit, seed), mk)


def _plant_base(sick):
    f = np.zeros((H, W, 3), np.float32)
    k = (_yy / H)[..., None]
    f[:] = _mix(_c((70, 150, 236)), _c((200, 230, 250)), np.clip(k / 0.5, 0, 1) ** 0.9)
    _sglow(f, 760, 520, 420, (255, 244, 210), 0.5)
    # hills
    xs = np.arange(W)
    for (yb, amp, col, ph) in ((900, 60, (110, 170, 120), 0.3), (960, 40, (80, 150, 90), 1.7)):
        top = (yb + amp * np.sin(xs / 210 + ph) + 20 * np.sin(xs / 70 + ph * 2)).astype(int)
        for x in range(W): f[top[x]:, x] = C(col)
    # soil with furrows
    soil = np.zeros_like(f); soil[:] = _mix(_c((150, 104, 64)), _c((110, 70, 40)), np.clip((_yy - 1040) / 880, 0, 1)[..., None])
    m = (_yy >= 1040)[..., None]; f = np.where(m, soil, f)
    for i in range(-9, 10):
        x0 = 540 + i * 170
        cv2.line(f, (540 + i * 22, 1040), (x0 * 1, H), C((96, 62, 34)), 6, cv2.LINE_AA)
    # rows of plants, back to front (leave the middle lane open)
    for depth, (y, s, xs_) in enumerate(((1060, 0.22, range(-40, 1140, 95)), (1110, 0.34, range(-60, 1160, 150)),
                                          (1210, 0.55, (-60, 150, 930, 1140)), (1420, 0.95, (-120, 1200)))):
        for j, x in enumerate(xs_):
            if depth >= 2 or abs(x - 540) > 70 * (depth + 1):
                comp(f, scale_el(plant_el(900, sick * (0.6 + 0.4 * ((j * 7 + depth) % 3) / 2), fruit=depth >= 1, seed=j + depth * 5), s),
                     x, y - 450 * s)
        f = f * (0.97) + 0.03 * np.array(C((200, 230, 250)), np.float32) * (depth < 2)
    return f


def plantation_view(t=0.0, zoom=1.0, cx=W / 2, cy=H / 2, blur=0.0, sick=0.0, drift=4.0):
    """full-frame banana plantation (healthy -> sick blend)"""
    if "set_light" in globals(): set_light("day")
    a = gcache(("plantset", 0), lambda: _plant_base(0.0))
    if sick > 0.02:
        b = gcache(("plantset", 1), lambda: _plant_base(1.0)); base = a * (1 - sick) + b * sick
    else: base = a
    s = zoom * (1.0 + 0.004 * math.sin(t * 0.5))
    M = cv2.getRotationMatrix2D((cx, cy), 0, s); M[0, 2] += W / 2 - cx + drift * math.sin(t * 0.35); M[1, 2] += H / 2 - cy
    f = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return cv2.GaussianBlur(f, (0, 0), blur) if blur > 0.3 else f


def soil_view(t=0.0):
    """underground cross-section: grass line + small plant on top, dark soil layers, stones, roots"""
    def mk():
        f = np.zeros((H, W, 3), np.float32); k = (_yy / H)[..., None]
        f[:] = _mix(_c((120, 190, 245)), _c((210, 236, 250)), np.clip(k / 0.3, 0, 1))
        soil = _mix(_c((126, 84, 50)), _c((52, 32, 20)), np.clip((_yy - 640) / 1280, 0, 1)[..., None])
        f = np.where((_yy >= 640)[..., None], soil, f)
        rng = np.random.RandomState(4)
        for _ in range(70):
            x, y = rng.randint(0, W), rng.randint(700, H); r = rng.randint(6, 26)
            cv2.ellipse(f, (x, y), (r, int(r * 0.7)), rng.randint(0, 180), 0, 360, C((150, 130, 110) if rng.rand() < 0.5 else (90, 64, 44)), -1, cv2.LINE_AA)
        for i in range(5):   # strata lines
            y = 900 + i * 220
            cv2.polylines(f, [np.array([(x, int(y + 18 * math.sin(x / 90 + i))) for x in range(0, W + 40, 40)], np.int32)], False, C((70, 46, 28)), 3, cv2.LINE_AA)
        cv2.rectangle(f, (0, 620), (W, 650), C((60, 160, 60)), -1)
        # roots under the centre plant
        for j in range(9):
            a = math.radians(30 + 120 * j / 8); pts = []
            for u in np.linspace(0, 1, 12):
                pts.append((int(540 + 330 * u * math.cos(a) + 20 * math.sin(u * 9 + j)), int(650 + 420 * u * math.sin(a))))
            cv2.polylines(f, [np.array(pts, np.int32)], False, C((220, 196, 150)), max(2, 12 - j % 4 * 2), cv2.LINE_AA)
        return f
    return gcache("soil", mk).copy()


def spores(f, t, n=40, k=1.0, seed=2, y0=700, y1=1850, col=(255, 70, 90)):
    """glowing fungus spores drifting in the soil"""
    rng = np.random.RandomState(seed)
    for i in range(int(n * k)):
        x = rng.uniform(140, 940) + 14 * math.sin(t * 0.8 + i); y = rng.uniform(y0, y1) + 10 * math.cos(t * 0.7 + i * 1.3)
        r = rng.uniform(5, 11) * (0.9 + 0.2 * math.sin(t * 3 + i))
        _sglow(f, int(x), int(y), int(r * 4), col, 0.35)
        cv2.circle(f, (int(x), int(y)), int(r), C(col), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y)), int(r), C((90, 10, 30)), 2, cv2.LINE_AA)


def hyphae(f, cx, cy, k, t, seed=5, reach=380, col=(255, 236, 240)):
    """fungus threads growing out from a point (k = 0..1 growth)"""
    rng = np.random.RandomState(seed)
    for j in range(14):
        a = rng.uniform(0, 2 * math.pi); L = reach * rng.uniform(0.5, 1.0) * k
        pts = [(cx, cy)]
        x, y = cx, cy
        for s_ in range(10):
            a += rng.uniform(-0.5, 0.5); x += math.cos(a) * L / 10; y += math.sin(a) * L / 10
            pts.append((x, y))
        cv2.polylines(f, [np.array(pts, np.int32)], False, C(col), 3, cv2.LINE_AA)


# ---- Latin America map (lon/lat polygons, hand-simplified coastlines; equirectangular) ----
MAP_LON0, MAP_LAT0, MAP_S = -98.0, 24.0, 16.0
MAP_X0, MAP_Y0 = 140, 640
SA = [(-77.4, 8.6), (-76.0, 9.6), (-75.5, 10.8), (-74.2, 11.2), (-72.2, 11.9), (-71.3, 11.0), (-70.0, 12.2), (-68.2, 10.5), (-66.0, 10.6),
      (-63.0, 10.7), (-61.6, 9.8), (-60.0, 8.4), (-58.0, 6.8), (-55.0, 5.9), (-52.0, 4.8), (-50.5, 2.0), (-49.8, 0.0), (-47.5, -0.8),
      (-44.0, -2.4), (-40.0, -2.9), (-37.5, -4.6), (-35.2, -5.6), (-34.9, -8.0), (-36.5, -10.5), (-38.6, -13.2), (-39.1, -17.5),
      (-40.5, -20.5), (-42.0, -22.9), (-44.5, -23.4), (-48.5, -26.0), (-49.5, -29.0), (-53.0, -33.8), (-58.0, -34.5), (-57.5, -38.0),
      (-62.0, -39.0), (-65.0, -42.0), (-67.5, -46.5), (-68.5, -50.5), (-68.5, -53.0), (-71.0, -54.0), (-74.5, -52.0), (-75.5, -47.0),
      (-73.6, -42.0), (-73.5, -37.0), (-71.6, -33.0), (-71.4, -28.0), (-70.3, -18.5), (-75.0, -15.5), (-77.5, -12.0), (-79.5, -7.5),
      (-81.3, -5.0), (-80.4, -3.4), (-80.9, -1.0), (-80.0, 0.8), (-78.8, 1.8), (-77.4, 4.0), (-77.4, 7.0)]
CA = [(-77.4, 8.6), (-79.5, 9.5), (-81.5, 9.0), (-83.6, 10.9), (-83.4, 13.0), (-83.2, 15.0), (-85.0, 16.0), (-88.2, 15.8), (-88.3, 17.5),
      (-87.6, 19.7), (-87.1, 21.5), (-90.4, 21.2), (-91.0, 18.6), (-94.5, 18.3), (-96.5, 19.6), (-97.6, 22.0), (-98.2, 25.0), (-100, 25.0),
      (-100, 16.6), (-96.5, 15.7), (-94.0, 16.1), (-92.2, 14.5), (-89.6, 13.5), (-87.6, 13.1), (-86.6, 12.0), (-85.7, 11.0),
      (-85.6, 9.9), (-84.0, 9.0), (-82.8, 8.2), (-80.4, 7.4), (-79.0, 8.4), (-78.0, 8.0)]
CUBA = [(-84.9, 21.9), (-82.0, 23.1), (-79.5, 22.6), (-77.2, 21.6), (-74.2, 20.2), (-77.7, 19.9), (-80.0, 21.7), (-82.0, 22.0)]
HISP = [(-74.4, 19.8), (-71.0, 19.9), (-68.4, 18.6), (-70.0, 18.2), (-72.5, 18.2), (-74.4, 18.4)]
JAM = [(-78.3, 18.4), (-76.3, 18.2), (-76.8, 17.9), (-78.2, 18.2)]


def map_xy(lon, lat): return MAP_X0 + (lon - MAP_LON0) * MAP_S, MAP_Y0 + (MAP_LAT0 - lat) * MAP_S


def _map_base(sepia):
    f = np.zeros((H, W, 3), np.float32); k = (_yy / H)[..., None]
    f[:] = _mix(_c(OCEAN_A), _c(OCEAN_B), np.clip(1 - abs(k - 0.5) * 1.6, 0, 1))
    for lat in range(-60, 40, 10):   # graticule
        y = int(map_xy(-80, lat)[1]); cv2.line(f, (0, y), (W, y), C((80, 160, 230)), 1, cv2.LINE_AA)
    for lon in range(-130, 0, 10):
        x = int(map_xy(lon, 0)[0]); cv2.line(f, (x, 0), (x, H), C((80, 160, 230)), 1, cv2.LINE_AA)
    for poly in (SA, CA, CUBA, HISP, JAM):
        p = np.array([map_xy(*q) for q in poly], np.float32)
        sh = p + np.float32([10, 14]); cv2.fillPoly(f, [sh.astype(np.int32)], C((10, 50, 110)), cv2.LINE_AA)
        cv2.fillPoly(f, [p.astype(np.int32)], C(LAND), cv2.LINE_AA)
    lm = np.zeros((H, W), np.float32)
    for poly in (SA, CA, CUBA, HISP, JAM):
        cv2.fillPoly(lm, [np.array([map_xy(*q) for q in poly], np.int32)], 1.0, cv2.LINE_AA)
    shade = cv2.GaussianBlur(lm, (0, 0), 30)
    f = f * (1 - lm[..., None]) + lm[..., None] * (f * (0.82 + 0.25 * shade[..., None]))
    for poly in (SA, CA, CUBA, HISP, JAM):
        cv2.polylines(f, [np.array([map_xy(*q) for q in poly], np.int32)], True, C((20, 60, 40)), 4, cv2.LINE_AA)
    if sepia: f = sepia_tone(f, 1.0)
    return f


def map_view(t=0.0, zoom=1.0, cx=W / 2, cy=H / 2, sepia=False):
    base = gcache(("mapbase", sepia), lambda: _map_base(sepia))
    s = zoom * (1.0 + 0.004 * math.sin(t * 0.5))
    M = cv2.getRotationMatrix2D((cx, cy), 0, s); M[0, 2] += W / 2 - cx; M[1, 2] += H / 2 - cy
    return cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), (s, cx, cy)


def map_pt(lon, lat, cam):
    s, cx, cy = cam; x, y = map_xy(lon, lat)
    return (x - cx) * s + W / 2, (y - cy) * s + H / 2


def blight(f, x, y, r, k, t, col=(220, 30, 40)):
    """red infection blob that pulses and spreads"""
    if k <= 0: return
    rr = r * eo(clamp(k))
    if rr < 2: return
    _sglow(f, int(x), int(y), int(rr * 1.8), col, 0.45)
    ov = f.copy(); cv2.circle(ov, (int(x), int(y)), int(rr), C(col), -1, cv2.LINE_AA)
    f[:] = f * 0.45 + ov * 0.55
    cv2.circle(f, (int(x), int(y)), int(rr * (1 + 0.15 * (t * 2 % 1))), C((255, 120, 120)), 3, cv2.LINE_AA)


def map_pin(f, x, y, label, sub, t, t0, col=RED_, big=False):
    if t < t0: return
    k = pin(t, t0, 0.3)
    el = pin_el(label, col)
    comp(f, el, x, y - 70 * k, scale=(1.25 if big else 0.95) * k)
    if sub:
        comp(f, chip(sub, INK, WHITE, 30 if big else 26), x, y + 46, op=clamp((t - t0) / 0.25))


def sepia_tone(f, k=1.0):
    g = (f @ LUMA)[..., None]
    sep = np.concatenate([g * 1.07 + 0.06, g * 0.94 + 0.03, g * 0.72], -1)
    out = f * (1 - k) + np.clip(sep, 0, 1) * k
    return out * (1 - 0.25 * k * np.clip(_rr - 0.35, 0, 1)[..., None])


def spray_el(w=260):
    """generic trigger spray bottle"""
    def mk():
        sc = 2; h = int(w * 1.7); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(w * 0.16, h * 0.36, w * 0.84, h - 6), 40 * sc, fill=255), (120, 220, 250), (40, 150, 210))
        d.rounded_rectangle(S(w * 0.16, h * 0.36, w * 0.84, h - 6), 40 * sc, outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(w * 0.28, h * 0.55, w * 0.72, h * 0.78), 10 * sc, fill=(255, 255, 255, 230), outline=INK + (255,), width=2 * sc)
        d.text((w * 0.5 * sc, h * 0.665 * sc), "FUNGICIDE", font=font(F_BLACK, int(w * 0.075) * sc), fill=(30, 110, 60, 255), anchor="mm")
        d.rectangle(S(w * 0.36, h * 0.26, w * 0.64, h * 0.37), fill=(240, 240, 246, 255), outline=INK + (255,), width=3 * sc)
        d.polygon(S(w * 0.24, h * 0.14, w * 0.72, h * 0.14, w * 0.72, h * 0.27, w * 0.24, h * 0.27), fill=(250, 250, 250, 255), outline=INK + (255,))
        d.polygon(S(w * 0.24, h * 0.16, w * 0.02, h * 0.16, w * 0.02, h * 0.21, w * 0.24, h * 0.23), fill=(230, 60, 50, 255), outline=INK + (255,))
        d.polygon(S(w * 0.5, h * 0.27, w * 0.42, h * 0.42, w * 0.48, h * 0.43, w * 0.58, h * 0.27), fill=(230, 60, 50, 255), outline=INK + (255,))
        return _done(im, w, h)
    return gcache(("spray", w), mk)


def helix(f, cx, y0, y1, t, ca=(255, 214, 48), cb=(120, 220, 120), amp=110, k=1.0, tag=None):
    """rotating DNA double helix (vertical)"""
    n = 26
    for i in range(n):
        if i / n > k: break
        y = y0 + (y1 - y0) * i / (n - 1); ph = i * 0.55 + t * 2.2
        xa, xb = cx + amp * math.sin(ph), cx - amp * math.sin(ph)
        front = math.cos(ph) > 0
        cv2.line(f, (int(xa), int(y)), (int(xb), int(y)), C((240, 240, 250)), 5, cv2.LINE_AA)
        for (x, c, fr) in ((xa, ca, front), (xb, cb, not front)):
            r = 17 if fr else 12
            cv2.circle(f, (int(x), int(y)), r, C(c if fr else _mixc(c, (40, 40, 60), 0.4)), -1, cv2.LINE_AA)
            cv2.circle(f, (int(x), int(y)), r, C(INK), 2, cv2.LINE_AA)


def basket_el(w=520):
    """woven basket (generic)"""
    def mk():
        sc = 2; h = int(w * 0.55); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.polygon(S(16, h * 0.14 + 10, w - 2, h * 0.14 + 10, w * 0.86, h, w * 0.18, h), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.polygon(S(6, h * 0.12, w - 12, h * 0.12, w * 0.84, h - 8, w * 0.16, h - 8), fill=255), (226, 170, 96), (160, 104, 48))
        for r in range(1, 6):
            y = h * (0.12 + 0.17 * r); xo = w * 0.03 * r
            d.line(S(6 + xo, y, w - 12 - xo, y), fill=(130, 84, 36, 255), width=4 * sc)
        for c in range(1, 12):
            x = w * c / 12; d.line(S(x, h * 0.12, w * 0.5 + (x - w * 0.5) * 0.72, h - 8), fill=(130, 84, 36, 200), width=3 * sc)
        d.polygon(S(6, h * 0.12, w - 12, h * 0.12, w * 0.84, h - 8, w * 0.16, h - 8), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(0, h * 0.06, w - 6, h * 0.17), 14 * sc, fill=(200, 140, 70, 255), outline=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("basket", w), mk)


def numcard_el(num, text, col=(40, 110, 220), w=250, down=False):
    """roadmap card: big number + one word; down=True shows a '?' back"""
    def mk():
        sc = 2; h = int(w * 1.4); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 14, w, h), 26 * sc, fill=(0, 0, 0, 70)))
        if down:
            shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 10, h - 14), 26 * sc, fill=255), (60, 40, 120), (30, 20, 70))
            d.rounded_rectangle(S(0, 0, w - 10, h - 14), 26 * sc, outline=(255, 214, 60, 255), width=6 * sc)
            d.text(((w - 10) / 2 * sc, (h - 14) / 2 * sc), "?", font=font(F_ANTON, int(w * 0.62) * sc), fill=(255, 214, 60, 255), anchor="mm")
        else:
            shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 10, h - 14), 26 * sc, fill=255), (255, 255, 255), (232, 232, 240))
            d.rounded_rectangle(S(0, 0, w - 10, h - 14), 26 * sc, outline=INK + (255,), width=5 * sc)
            d.text(((w - 10) / 2 * sc, h * 0.36 * sc), str(num), font=font(F_ANTON, int(w * 0.5) * sc), fill=tuple(col) + (255,), anchor="mm")
            fn = font(F_BLACK, int(w * 0.13) * sc)
            while fn.getlength(text) / sc > w * 0.8: fn = font(F_BLACK, int(fn.size / sc - 2) * sc)
            d.text(((w - 10) / 2 * sc, h * 0.72 * sc), text, font=fn, fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("numcard", num, text, col, w, down), mk)


def stand_el(w=700):
    """market fruit stand: wooden crate table with a striped awning edge (generic)"""
    def mk():
        sc = 2; h = int(w * 0.5); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rectangle(S(10, h * 0.25, w - 10, h - 6), fill=255), (196, 140, 80), (130, 86, 44))
        for k in range(1, 4): d.line(S(10, h * (0.25 + 0.18 * k), w - 10, h * (0.25 + 0.18 * k)), fill=(110, 70, 34, 255), width=4 * sc)
        d.rectangle(S(10, h * 0.25, w - 10, h - 6), outline=INK + (255,), width=4 * sc)
        d.polygon(S(0, h * 0.25, w, h * 0.25, w - 30, h * 0.1, 30, h * 0.1), fill=(150, 100, 56, 255), outline=INK + (255,))
        return _done(im, w, h)
    return gcache(("stand", w), mk)
