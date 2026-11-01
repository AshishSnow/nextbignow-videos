# ================= props kit 4 (exec'd after anim_story2.py) — HOW TO START: drone business (1 Nov 2026) =================
# Generic, logo-free props for "how to start a service business" episodes:
#   home_el(w, col, roof, sign)      suburban house front (optional yard sign: "FOR SALE")
#   aerial_view(t, zoom, cx, cy)     full-frame top-down "seen from the drone" shot: roof, lawn, pool, drive, trees, street
#   viewfinder(f, t, alt, rec)       drone-camera HUD overlay: corner brackets, REC dot, altitude, battery, centre cross
#   route_map(f, t, k, n_red, labels)  step roadmap as a flight route: 5 waypoints, the drone flies along the dotted path (k 0..5)
#   remote_id_el(w)                  "REMOTE ID" licence plate with broadcast waves
#   shield_el(w, text)               insurance shield with a tick
#   airspace_phone_el(ok)            phone with a generic airspace map (red no-fly ring, green zone, status bar)
#   nofly_ring(f, x, y, rx, t)       pulsing red ground ring with hatching (perspective ellipse)
#   photo_el(kind, w, rot)           aerial photo print: "home", "roof", "party"
#   pc_el(w, k, label)               exam monitor with a progress bar (k 0..1)
#   controller_el(w)                 drone remote controller (two sticks, small screen)
#   uk_eu_card_el(side)              outline-only region card (no flags): "UK" / "EU" + steps
_O4 = (26, 22, 34, 255)


def _im4(w, h, sc=2):
    im = Image.new("RGBA", (int(w * sc), int(h * sc)), (0, 0, 0, 0)); return im, ImageDraw.Draw(im), (lambda *v: [x * sc for x in v])


def _el4(im, w, h): return el_from(im.resize((int(w), int(h)), Image.LANCZOS))


def home_el(w=520, col=(120, 200, 255), roof=(230, 70, 60), sign=None):
    def mk():
        h = int(w * 0.95); im, d, S = _im4(w, h); o = _O4; sc = 2
        bx0, bx1, by0, by1 = w * 0.12, w * 0.88, h * 0.40, h * 0.86
        d.rectangle(S(w * 0.66, h * 0.10, w * 0.76, h * 0.34), fill=(170, 80, 60, 255), outline=o, width=5 * sc)
        d.polygon(S(w * 0.04, by0 + 6, w * 0.5, h * 0.08, w * 0.96, by0 + 6), fill=tuple(roof) + (255,), outline=o, width=6 * sc)
        for i in range(1, 5):
            yy = h * 0.08 + (by0 - h * 0.08) * i / 5; xl = w * 0.5 - (w * 0.46) * i / 5; xr = w * 0.5 + (w * 0.46) * i / 5
            d.line(S(xl + 8, yy, xr - 8, yy), fill=tuple(_darker(roof, 0.8)) + (255,), width=3 * sc)
        d.rectangle(S(bx0, by0, bx1, by1), fill=tuple(col) + (255,), outline=o, width=6 * sc)
        for xx in (bx0 + (bx1 - bx0) * 0.12, bx0 + (bx1 - bx0) * 0.62):
            d.rectangle(S(xx, by0 + h * 0.08, xx + w * 0.2, by0 + h * 0.24), fill=(255, 236, 150, 255), outline=o, width=5 * sc)
            d.line(S(xx + w * 0.1, by0 + h * 0.08, xx + w * 0.1, by0 + h * 0.24), fill=o, width=4 * sc)
        dx = w * 0.43; d.rounded_rectangle(S(dx, by0 + h * 0.16, dx + w * 0.14, by1), int(8 * sc), fill=(150, 60, 40, 255), outline=o, width=5 * sc)
        d.ellipse(S(dx + w * 0.10, by0 + h * 0.31, dx + w * 0.12, by0 + h * 0.33), fill=(255, 220, 80, 255))
        d.rectangle(S(0, by1, w, h), fill=(80, 190, 70, 255))
        d.line(S(0, by1, w, by1), fill=o, width=4 * sc)
        for bx in (bx0 + 10, bx1 - 70): d.ellipse(S(bx, by1 - 40, bx + 64, by1 + 14), fill=(50, 160, 60, 255), outline=o, width=4 * sc)
        if sign:
            sx = w * 0.84; d.line(S(sx, by1 - 60, sx, h - 4), fill=o, width=8 * sc)
            d.rounded_rectangle(S(sx - 70, by1 - 100, sx + 70, by1 - 40), int(8 * sc), fill=(255, 255, 255, 255), outline=(220, 40, 40, 255), width=6 * sc)
            fn = font(F_ANTON, int(30 * sc)); d.text(S(sx, by1 - 70), sign, font=fn, fill=(220, 40, 40, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("home4", w, col, roof, sign), mk)


def _aerial_base():
    f = np.zeros((H, W, 3), np.float32); f[:] = C((92, 178, 74))
    rng = np.random.default_rng(5)
    nz = cv2.GaussianBlur(rng.random((H // 8, W // 8)).astype(np.float32), (0, 0), 2)
    nz = cv2.resize(nz, (W, H)); f *= (0.9 + 0.2 * nz)[..., None]
    for x in range(0, W, 46): cv2.line(f, (x, 0), (x, H), C((104, 192, 84)), 18)   # mowing stripes
    cv2.rectangle(f, (0, 1520), (W, 1760), C((70, 72, 82)), -1)                     # street
    for x in range(0, W, 160): cv2.rectangle(f, (x, 1636), (x + 80, 1646), C((250, 240, 200)), -1)
    cv2.rectangle(f, (0, 1500), (W, 1522), C((200, 200, 196)), -1)
    cv2.rectangle(f, (660, 1180), (840, 1520), C((190, 186, 180)), -1)               # driveway
    # roof (top-down hip roof)
    x0, y0, x1, y1 = 230, 560, 860, 1160
    cv2.rectangle(f, (x0 + 18, y0 + 22), (x1 + 18, y1 + 22), C((40, 70, 40)), -1)    # shadow
    rc = [C((214, 74, 62)), C((190, 58, 50)), C((236, 96, 78)), C((176, 50, 44))]
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2; ridge = 150
    polys = [[(x0, y0), (x1, y0), (cx + ridge, cy), (cx - ridge, cy)], [(x1, y0), (x1, y1), (cx + ridge, cy)],
             [(x1, y1), (x0, y1), (cx - ridge, cy), (cx + ridge, cy)], [(x0, y1), (x0, y0), (cx - ridge, cy)]]
    for p, c_ in zip(polys, (rc[2], rc[1], rc[3], rc[0])):
        cv2.fillPoly(f, [np.array(p, np.int32)], c_, cv2.LINE_AA)
    for p in polys: cv2.polylines(f, [np.array(p, np.int32)], True, C((60, 24, 24)), 4, cv2.LINE_AA)
    for i in range(1, 9):   # shingle rows on the front face
        k = i / 9; cv2.line(f, (int(x0 + (cx - ridge - x0) * k), int(y1 + (cy - y1) * k)), (int(x1 + (cx + ridge - x1) * k), int(y1 + (cy - y1) * k)), C((160, 48, 40)), 2, cv2.LINE_AA)
    cv2.rectangle(f, (680, 640), (740, 700), C((120, 60, 50)), -1)                   # chimney
    cv2.rectangle(f, (680, 640), (740, 700), C((40, 20, 20)), 3)
    # pool + patio
    cv2.rectangle(f, (110, 220), (520, 470), C((226, 222, 210)), -1)
    cv2.rectangle(f, (150, 250), (480, 440), C((40, 180, 230)), -1)
    cv2.rectangle(f, (150, 250), (480, 440), C((255, 255, 255)), 6)
    for i in range(6): cv2.ellipse(f, (200 + i * 50, 340 + (i % 2) * 30), (26, 8), 0, 0, 360, C((150, 230, 255)), 2, cv2.LINE_AA)
    # trees
    for (tx, ty, r) in ((900, 300, 120), (130, 1300, 110), (960, 1300, 95), (620, 250, 80)):
        cv2.circle(f, (tx + 20, ty + 24), r, C((40, 80, 40)), -1, cv2.LINE_AA)
        cv2.circle(f, (tx, ty), r, C((44, 140, 56)), -1, cv2.LINE_AA)
        cv2.circle(f, (tx - r // 3, ty - r // 3), r // 2, C((80, 176, 76)), -1, cv2.LINE_AA)
    # car on the drive
    cv2.rectangle(f, (690, 1300), (810, 1480), C((30, 120, 230)), -1); cv2.rectangle(f, (705, 1340), (795, 1400), C((150, 210, 255)), -1)
    cv2.rectangle(f, (690, 1300), (810, 1480), C((20, 30, 60)), 4)
    return f


def aerial_view(t=0.0, zoom=1.0, cx=W / 2, cy=H / 2, rot=0.0):
    base = gcache(("aerial4",), _aerial_base)
    return cam(base.copy(), zoom, cx, cy, 0, 0, rot)


def viewfinder(f, t, alt="ALT 200 FT", rec=True, col=(255, 255, 255)):
    c = C(col); L = 90; m = (120, 300, W - 160, H - 470)
    for (x, y, sx, sy) in ((m[0], m[1], 1, 1), (m[2], m[1], -1, 1), (m[0], m[3], 1, -1), (m[2], m[3], -1, -1)):
        cv2.line(f, (x, y), (x + sx * L, y), c, 7, cv2.LINE_AA); cv2.line(f, (x, y), (x, y + sy * L), c, 7, cv2.LINE_AA)
    cv2.line(f, (520, 960), (560, 960), c, 3, cv2.LINE_AA); cv2.line(f, (540, 940), (540, 980), c, 3, cv2.LINE_AA)
    if rec and (t % 1.0) < 0.6: cv2.circle(f, (m[0] + 40, m[1] + 60), 14, C((240, 40, 40)), -1, cv2.LINE_AA)
    comp(f, gcache(("vf_txt", alt), lambda: el_from(_stxt_el(alt, 34, stroke=3))), 540, m[3] - 40)
    comp(f, gcache(("vf_rec",), lambda: el_from(_stxt_el("REC", 34, stroke=3))), m[0] + 110, m[1] + 60)


def route_map(f, t, k, n_red=5, labels=("LICENSE", "REGISTER", "GEAR", "CLIENTS", "MISTAKE"), y0=760, y1=1500, t_pop=None):
    """5 waypoints on a zig-zag dotted flight path; drone sits at position k (0..5 float; 0 = before step 1)."""
    pts = [(240, y1), (800, y1 - (y1 - y0) * 0.25), (300, y1 - (y1 - y0) * 0.5), (790, y1 - (y1 - y0) * 0.75), (330, y0)]
    for i in range(4):
        p, q = pts[i], pts[i + 1]; n_ = 14
        for j in range(n_):
            if j % 2: continue
            a = j / n_; b = (j + 1) / n_
            cv2.line(f, (int(p[0] + (q[0] - p[0]) * a), int(p[1] + (q[1] - p[1]) * a)), (int(p[0] + (q[0] - p[0]) * b), int(p[1] + (q[1] - p[1]) * b)),
                     C((255, 255, 255)), 8, cv2.LINE_AA)
    for i, (x, y) in enumerate(pts):
        if t_pop is not None and t < t_pop + 0.25 * i: continue
        red = (i + 1) == n_red
        el = gcache(("wp", i, red, labels[i]), lambda: numcard_el(str(i + 1), labels[i], col=(226, 40, 50) if red else (40, 110, 220), w=230))
        sc = pin(t, t_pop + 0.25 * i, 0.25) if t_pop is not None else 1.0
        comp(f, el, x, y, scale=sc)
    if k > 0:
        kk = min(k, 5.0); i = min(int(kk) - 1, 3) if kk >= 1 else -1
        if kk < 1: p = (540, y1 + 200); q = pts[0]; a = kk
        else: p = pts[max(0, int(kk) - 1)]; q = pts[min(4, int(kk))]; a = kk - int(kk)
        x = p[0] + (q[0] - p[0]) * a; y = p[1] + (q[1] - p[1]) * a - 140
        comp(f, drone_el(220, t), x, y + 8 * math.sin(t * 6))


def remote_id_el(w=520):
    def mk():
        h = int(w * 0.42); im, d, S = _im4(w, h); sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h - 6), int(26 * sc), fill=(245, 248, 255, 255), outline=_O4, width=7 * sc)
        d.rounded_rectangle(S(20, 20, w - 20, 62), int(12 * sc), fill=(30, 110, 230, 255))
        d.text(S(w / 2, 41), "BROADCASTING", font=font(F_BOLD, int(26 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        d.text(S(w / 2, h * 0.64), "REMOTE ID", font=font(F_ANTON, int(h * 0.42 * sc)), fill=(22, 22, 28, 255), anchor="mm")
        for x in (30, w - 30): d.ellipse(S(x - 8, h - 38, x + 8, h - 22), fill=(150, 150, 160, 255))
        return _el4(im, w, h)
    return gcache(("rid", w), mk)


def waves(f, x, y, t, col=(90, 200, 255), n=3, r0=60, sp=180, op=0.8):
    for i in range(n):
        ph = ((t * 0.9 + i / n) % 1.0); r = int(r0 + ph * sp)
        cv2.circle(f, (int(x), int(y)), r, C(col), max(2, int(10 * (1 - ph))), cv2.LINE_AA)


def shield_el(w=420, text="INSURED", col=(30, 120, 240)):
    def mk():
        h = int(w * 1.15); im, d, S = _im4(w, h); sc = 2
        pts = [(w * 0.5, 8), (w - 10, h * 0.16), (w - 24, h * 0.58), (w * 0.5, h - 10), (24, h * 0.58), (10, h * 0.16)]
        d.polygon(S(*[v for p in pts for v in p]), fill=tuple(col) + (235,), outline=(255, 255, 255, 255), width=10 * sc)
        d.line(S(w * 0.3, h * 0.42, w * 0.45, h * 0.56, w * 0.72, h * 0.30), fill=(255, 255, 255, 255), width=24 * sc, joint="curve")
        d.text(S(w / 2, h * 0.76), text, font=font(F_ANTON, int(56 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("shield4", w, text, col), mk)


def airspace_phone_el(ok=True, w=420):
    def mk():
        h = int(w * 1.9); im, d, S = _im4(w, h); sc = 2
        d.rounded_rectangle(S(4, 4, w - 4, h - 4), int(54 * sc), fill=(24, 24, 30, 255), outline=_O4, width=6 * sc)
        x0, y0, x1, y1 = 24, 70, w - 24, h - 150
        d.rectangle(S(x0, y0, x1, y1), fill=(232, 236, 226, 255))
        for i in range(6):
            yy = y0 + (y1 - y0) * (i + 0.5) / 6; d.line(S(x0, yy, x1, yy + 30), fill=(255, 255, 255, 255), width=10 * sc)
        for i in range(4):
            xx = x0 + (x1 - x0) * (i + 0.5) / 4; d.line(S(xx, y0, xx - 20, y1), fill=(255, 255, 255, 255), width=10 * sc)
        rx, ry, rr = x0 + (x1 - x0) * 0.68, y0 + (y1 - y0) * 0.3, w * 0.24
        d.ellipse(S(rx - rr, ry - rr, rx + rr, ry + rr), fill=(240, 60, 60, 110), outline=(220, 30, 30, 255), width=5 * sc)
        d.text(S(rx, ry), "NO FLY", font=font(F_ANTON, int(30 * sc)), fill=(170, 20, 20, 255), anchor="mm")
        gx, gy, gr = x0 + (x1 - x0) * 0.32, y0 + (y1 - y0) * 0.72, w * 0.2
        d.ellipse(S(gx - gr, gy - gr, gx + gr, gy + gr), fill=(60, 200, 90, 110), outline=(30, 150, 60, 255), width=5 * sc)
        d.ellipse(S(gx - 12, gy - 12, gx + 12, gy + 12), fill=(255, 120, 20, 255), outline=_O4, width=3 * sc)
        bc = (40, 170, 80) if ok else (220, 40, 40); bt = "CLEAR TO FLY" if ok else "RESTRICTED"
        d.rounded_rectangle(S(x0, y1 + 20, x1, y1 + 100), int(22 * sc), fill=bc + (255,))
        d.text(S(w / 2, y1 + 60), bt, font=font(F_ANTON, int(44 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        d.text(S(w / 2, 40), "AIRSPACE CHECK", font=font(F_BOLD, int(24 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("airphone", ok, w), mk)


def nofly_ring(f, x, y, rx, t, ry=None, op=1.0):
    ry = ry or rx * 0.36; pul = 0.5 + 0.5 * math.sin(t * 7)
    ov = f.copy()
    cv2.ellipse(ov, (int(x), int(y)), (int(rx), int(ry)), 0, 0, 360, C((240, 40, 40)), -1, cv2.LINE_AA)
    f[:] = f * (1 - 0.32 * op) + ov * 0.32 * op
    for i in range(-8, 9):
        xx = x + i * rx / 8
        cv2.line(f, (int(xx - 30), int(y + ry * 0.6)), (int(xx + 30), int(y - ry * 0.6)), C((255, 90, 90)), 3, cv2.LINE_AA)
    cv2.ellipse(f, (int(x), int(y)), (int(rx), int(ry)), 0, 0, 360, C((255, 40 + 120 * pul, 40)), int(8 + 4 * pul), cv2.LINE_AA)


def photo_el(kind="home", w=300):
    if w != 300: return scale_el(photo_el(kind, 300), w / 300)
    def mk():
        h = int(w * 1.12); im, d, S = _im4(w, h); sc = 2
        d.rectangle(S(0, 0, w, h), fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2 * sc)
        x0, y0, x1, y1 = 16, 16, w - 16, w - 16
        if kind == "home":
            d.rectangle(S(x0, y0, x1, y1), fill=(92, 178, 74, 255))
            d.rectangle(S(x0 + 50, y0 + 60, x1 - 50, y1 - 70), fill=(214, 74, 62, 255), outline=(60, 24, 24, 255), width=3 * sc)
            d.line(S(x0 + 50, y0 + 60, (x0 + x1) / 2, (y0 + y1) / 2 - 5, x1 - 50, y0 + 60), fill=(60, 24, 24, 255), width=3 * sc)
            d.rectangle(S(x0 + 10, y0 + 10, x0 + 70, y0 + 46), fill=(40, 180, 230, 255))
        elif kind == "roof":
            d.rectangle(S(x0, y0, x1, y1), fill=(120, 120, 130, 255))
            for i in range(9): d.line(S(x0, y0 + i * (y1 - y0) / 9, x1, y0 + i * (y1 - y0) / 9), fill=(90, 90, 100, 255), width=3 * sc)
            d.ellipse(S((x0 + x1) / 2 - 30, (y0 + y1) / 2 - 30, (x0 + x1) / 2 + 30, (y0 + y1) / 2 + 30), outline=(240, 40, 40, 255), width=6 * sc)
        else:
            d.rectangle(S(x0, y0, x1, y1), fill=(60, 170, 90, 255))
            for i in range(14):
                cx_ = x0 + 30 + (i * 53) % (x1 - x0 - 60); cy_ = y0 + 30 + (i * 37) % (y1 - y0 - 60)
                d.ellipse(S(cx_ - 9, cy_ - 9, cx_ + 9, cy_ + 9), fill=((255, 90, 160), (255, 200, 0), (40, 150, 255))[i % 3] + (255,))
            d.rectangle(S(x0 + 60, y0 + 40, x1 - 60, y0 + 90), fill=(255, 255, 255, 255))
        lab = {"home": "HOME", "roof": "ROOF", "party": "EVENT"}[kind]
        d.text(S(w / 2, (y1 + h) / 2), lab, font=font(F_ANTON, int(34 * sc)), fill=(40, 40, 48, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("photo4", kind, w), mk)


def pc_el(w=560, k=0.0, label="QUESTION 1 / 60"):
    kq = round(k, 2)
    def mk():
        h = int(w * 0.8); im, d, S = _im4(w, h); sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h * 0.78), int(22 * sc), fill=(36, 38, 48, 255), outline=_O4, width=6 * sc)
        d.rectangle(S(28, 28, w - 28, h * 0.72), fill=(236, 244, 255, 255))
        d.text(S(w / 2, h * 0.17), label, font=font(F_BOLD, int(30 * sc)), fill=(30, 40, 70, 255), anchor="mm")
        for i, opt in enumerate(("A", "B", "C")):
            yy = h * 0.29 + i * h * 0.105
            d.rounded_rectangle(S(70, yy, w - 70, yy + h * 0.08), int(10 * sc), fill=(255, 255, 255, 255), outline=(150, 170, 210, 255), width=3 * sc)
            d.text(S(100, yy + h * 0.04), opt, font=font(F_BOLD, int(26 * sc)), fill=(30, 40, 70, 255), anchor="mm")
        d.rounded_rectangle(S(60, h * 0.63, w - 60, h * 0.67), int(8 * sc), fill=(200, 210, 230, 255))
        d.rounded_rectangle(S(60, h * 0.63, 60 + (w - 120) * max(0.03, kq), h * 0.67), int(8 * sc), fill=(40, 180, 90, 255))
        d.polygon(S(w * 0.42, h * 0.78, w * 0.58, h * 0.78, w * 0.64, h * 0.95, w * 0.36, h * 0.95), fill=(60, 62, 74, 255), outline=_O4, width=4 * sc)
        return _el4(im, w, h)
    return gcache(("pc4", w, kq, label), mk)


def controller_el(w=200):
    def mk():
        h = int(w * 0.6); im, d, S = _im4(w, h); sc = 2
        d.rounded_rectangle(S(4, 18, w - 4, h - 4), int(30 * sc), fill=(50, 52, 62, 255), outline=_O4, width=4 * sc)
        d.rounded_rectangle(S(w * 0.32, 4, w * 0.68, h * 0.48), int(8 * sc), fill=(90, 190, 255, 255), outline=_O4, width=3 * sc)
        for x in (w * 0.2, w * 0.8):
            d.ellipse(S(x - 18, h * 0.55, x + 18, h * 0.55 + 36), fill=(30, 30, 36, 255)); d.ellipse(S(x - 8, h * 0.55 + 10, x + 8, h * 0.55 + 26), fill=(200, 200, 210, 255))
        return _el4(im, w, h)
    return gcache(("ctrl4", w), mk)


def uk_eu_card_el(side="UK", lines=("OPERATOR ID", "+ ONLINE TEST"), col=(30, 90, 200), w=440):
    def mk():
        h = int(w * 1.05); im, d, S = _im4(w, h); sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h - 6), int(34 * sc), fill=tuple(col) + (240,), outline=(255, 255, 255, 255), width=7 * sc)
        d.text(S(w / 2, h * 0.24), side, font=font(F_ANTON, int(h * 0.26 * sc)), fill=(255, 255, 255, 255), anchor="mm")
        for i, ln in enumerate(lines):
            d.text(S(w / 2, h * 0.56 + i * h * 0.15), ln, font=font(F_ANTON, int(h * 0.105 * sc)), fill=(255, 236, 120, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("ukeu", side, lines, col, w), mk)


# ---- vending kit (R&D run 1 Nov 2026: BUILD BRIEF of episodes/queue/05-vending-machines AND 04-nickel-coke) ----
#   vending_el(w, fill, glow, broken, era)  generic glass-front snack machine: 5 coil rows of plain coloured packs (no brands), keypad,
#   coin slot + bill reader + cooler vent on the right panel, pickup flap. fill 0..1 empties the coils from the top; glow = glass light;
#   broken = "coins" | "bills" | "cooler" greys that part and adds a red warning dot; era="1950" = a rounded red-free cream soda cooler
#   with bottle caps behind a small window and a coin slot only (for the nickel-Coke board; no Coke red, no script lettering).
def vending_el(w=600, fill=1.0, glow=1.0, broken=None, era=None):
    if w < 400 and era is None: return scale_el(vending_el(400, fill, glow, broken, era), w / 400)   # keypad maths breaks below ~260 px (2 Nov)
    k = round(float(clamp(fill)), 2); g = round(float(clamp(glow)), 2)
    def mk():
        h = int(w * 1.72); im, d, S = _im4(w, h); sc = 2
        rng = np.random.default_rng(11)
        if era == "1950":
            body, trim = (238, 228, 204), (120, 126, 136)
            d.rounded_rectangle(S(10, 30, w - 10, h - 10), 60 * sc, fill=body + (255,), outline=_O4, width=6 * sc)
            d.rounded_rectangle(S(10, 30, w - 10, h * 0.16), 60 * sc, fill=trim + (255,), outline=_O4, width=6 * sc)
            gx0, gy0, gx1, gy1 = w * 0.16, h * 0.24, w * 0.84, h * 0.62
            d.rounded_rectangle(S(gx0, gy0, gx1, gy1), 24 * sc, fill=(40, 48, 62, 255), outline=_O4, width=5 * sc)
            n = int(round(9 * k))
            for i in range(9):
                r, c = divmod(i, 3); cx = gx0 + (gx1 - gx0) * (c + 0.5) / 3; cy = gy0 + (gy1 - gy0) * (r + 0.5) / 3
                if i < n:
                    d.ellipse(S(cx - w * 0.07, cy - w * 0.07, cx + w * 0.07, cy + w * 0.07), fill=(196, 200, 206, 255), outline=_O4, width=3 * sc)
                    d.ellipse(S(cx - w * 0.035, cy - w * 0.035, cx + w * 0.035, cy + w * 0.035), fill=(160, 166, 174, 255))
            d.rounded_rectangle(S(w * 0.42, h * 0.68, w * 0.58, h * 0.74), 10 * sc, fill=(70, 74, 82, 255), outline=_O4, width=3 * sc)   # coin slot plate
            d.line(S(w * 0.5, h * 0.695, w * 0.5, h * 0.725), fill=(20, 20, 24, 255), width=5 * sc)
            d.rounded_rectangle(S(w * 0.2, h * 0.82, w * 0.8, h * 0.92), 16 * sc, fill=(60, 62, 70, 255), outline=_O4, width=4 * sc)     # door
            if g > 0: d.rounded_rectangle(S(gx0 + 10, gy0 + 10, gx0 + 40, gy1 - 30), 12 * sc, fill=(255, 255, 255, int(70 * g)))
            return _el4(im, w, h)
        body = (52, 58, 72)
        shape_grad(im, lambda m: m.rounded_rectangle(S(10, 10, w - 10, h - 10), 30 * sc, fill=255), (78, 86, 104), (40, 44, 56))
        d.rounded_rectangle(S(10, 10, w - 10, h - 10), 30 * sc, outline=_O4, width=6 * sc)
        gx0, gy0, gx1, gy1 = 36, 50, w * 0.70, h * 0.74            # glass window
        d.rounded_rectangle(S(gx0, gy0, gx1, gy1), 16 * sc, fill=(22, 30, 44, 255), outline=_O4, width=5 * sc)
        rows, cols = 5, 4; rh = (gy1 - gy0 - 24) / rows; cw = (gx1 - gx0 - 24) / cols
        cols_pal = [(240, 80, 70), (255, 190, 50), (70, 170, 255), (90, 200, 120), (200, 110, 230), (255, 140, 40)]
        empty_rows = int(round((1 - k) * rows))
        for r in range(rows):
            y1 = gy0 + 12 + (r + 1) * rh
            d.line(S(gx0 + 10, y1 - 4, gx1 - 10, y1 - 4), fill=(150, 156, 170, 255), width=4 * sc)                      # shelf
            for c in range(cols):
                x0 = gx0 + 12 + c * cw
                for j in range(3):                                                                                       # coil turns
                    d.arc(S(x0 + cw * (0.15 + 0.25 * j), y1 - 22, x0 + cw * (0.35 + 0.25 * j), y1 - 2), 0, 360, fill=(180, 186, 198, 255), width=2 * sc)
                if r >= empty_rows:
                    col = cols_pal[int(rng.integers(0, len(cols_pal)))]
                    if r % 2 == 0:   # chip bags
                        d.rounded_rectangle(S(x0 + cw * 0.14, y1 - rh * 0.82, x0 + cw * 0.86, y1 - 12), 10 * sc, fill=col + (255,), outline=_O4, width=3 * sc)
                        d.ellipse(S(x0 + cw * 0.36, y1 - rh * 0.6, x0 + cw * 0.64, y1 - rh * 0.34), fill=(255, 255, 255, 200))
                    else:            # bars
                        d.rounded_rectangle(S(x0 + cw * 0.1, y1 - rh * 0.5, x0 + cw * 0.9, y1 - 12), 6 * sc, fill=col + (255,), outline=_O4, width=3 * sc)
                        d.line(S(x0 + cw * 0.25, y1 - rh * 0.32, x0 + cw * 0.75, y1 - rh * 0.32), fill=(255, 255, 255, 190), width=4 * sc)
        if g > 0:   # glass light + reflection
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(ov)
            q.rounded_rectangle(S(gx0 + 6, gy0 + 6, gx1 - 6, gy0 + 22), 8 * sc, fill=(230, 245, 255, int(200 * g)))
            q.polygon(S(gx0 + 40, gy1 - 10, gx0 + 120, gy0 + 10, gx0 + 170, gy0 + 10, gx0 + 90, gy1 - 10), fill=(255, 255, 255, int(38 * g)))
            im.alpha_composite(ov)
        px0, px1 = w * 0.74, w - 30                                   # right panel
        d.rounded_rectangle(S(px0, 50, px1, h * 0.74), 14 * sc, fill=(34, 38, 48, 255), outline=_O4, width=4 * sc)
        d.rounded_rectangle(S(px0 + 14, 74, px1 - 14, 140), 8 * sc, fill=(30, 200, 140, 255) if g > 0 else (40, 60, 50, 255))   # display
        for i in range(12):                                           # keypad
            r, c = divmod(i, 3); bx = px0 + 20 + c * (px1 - px0 - 40) / 3; by = 170 + r * 46
            d.rounded_rectangle(S(bx, by, bx + (px1 - px0 - 40) / 3 - 8, by + 36), 6 * sc, fill=(210, 214, 222, 255), outline=_O4, width=2 * sc)
        parts = {"coins": (h * 0.47, "COINS"), "bills": (h * 0.55, "BILLS"), "cooler": (h * 0.66, "COOL")}
        for name, (py, _) in parts.items():
            bad = broken == name; colp = (110, 110, 116) if bad else (200, 204, 212)
            if name == "coins":
                d.rounded_rectangle(S(px0 + 30, py, px1 - 30, py + 40), 8 * sc, fill=colp + (255,), outline=_O4, width=3 * sc)
                d.line(S((px0 + px1) / 2, py + 8, (px0 + px1) / 2, py + 32), fill=(20, 20, 24, 255), width=5 * sc)
            elif name == "bills":
                d.rounded_rectangle(S(px0 + 20, py, px1 - 20, py + 50), 8 * sc, fill=colp + (255,), outline=_O4, width=3 * sc)
                d.rectangle(S(px0 + 34, py + 20, px1 - 34, py + 28), fill=(20, 20, 24, 255))
                d.ellipse(S(px1 - 40, py + 6, px1 - 28, py + 18), fill=((90, 220, 120) if not bad else (90, 90, 90)) + (255,))
            else:
                for j in range(4): d.line(S(px0 + 24, py + j * 14, px1 - 24, py + j * 14), fill=colp + (255,), width=5 * sc)
            if bad:
                d.ellipse(S(px1 - 30, py - 12, px1 - 6, py + 12), fill=(235, 50, 50, 255), outline=(255, 255, 255, 255), width=3 * sc)
        d.rounded_rectangle(S(40, h * 0.79, w * 0.70, h * 0.92), 14 * sc, fill=(20, 24, 32, 255), outline=_O4, width=4 * sc)   # pickup flap
        d.line(S(60, h * 0.83, w * 0.68, h * 0.83), fill=(70, 76, 90, 255), width=4 * sc)
        return _el4(im, w, h)
    return gcache(("vending4", w, k, g, broken, era), mk)


# ---- small staging helpers (2 Nov, HOW TO START EP 2 vending): thought bubble, floating music notes, coin rain, split-screen wipe ----
def thought(f, x, y, w, inner, op=1.0):
    """white thought cloud (circle + 3 trailing dots towards the lower left) with an element inside — 'you dream of X'"""
    if op <= 0: return
    ov = f.copy()
    cv2.ellipse(ov, (int(x), int(y)), (int(w * 0.62), int(w * 0.62)), 0, 0, 360, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
    for i, r in enumerate((34, 22, 14)):
        cv2.circle(ov, (int(x - w * 0.3 - i * 40), int(y + w * 0.62 + 30 + i * 46)), r, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op
    comp(f, inner, x, y, op=op)


def notes(f, x, y, t, n=3, op=1.0):
    """music notes rising and fading from (x, y) — a 'singer', a jingle, a radio"""
    for i in range(n):
        ph = (t * 0.9 + i / n) % 1.0
        comp(f, note_el(kind=i % 2), x + 60 * math.sin(ph * 6 + i), y - 220 * ph, scale=0.8, op=op * clamp(3 * (1 - ph)) * clamp(ph * 6))


def coin_rain(f, t, t0, x, y, n=7):
    """coins tumbling down from (x, y) after t0 — money draining away"""
    for i in range(n):
        q = t - t0 - i * 0.09
        if q <= 0: continue
        rot_comp(f, coin_el(42), x + (i - n / 2) * 40 + 30 * math.sin(i * 2.1), y + 900 * q * q, 40 * q * (i % 3 - 1), 1.0, clamp(2.0 - q), 0.2)


def split_wipe(f, g, t, t0, d=0.3):
    """split screen: frame g wipes in from the right to fill the right half (white divider) — 'meanwhile' / cause and effect"""
    if t < t0: return
    xs = int(W - (W // 2) * eo(clamp((t - t0) / d)))
    f[:, xs:] = g[:, xs:]
    cv2.line(f, (xs, 0), (xs, H), (1, 1, 1), 8)
