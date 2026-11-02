# ================= props kit 5 (exec'd after anim_props4.py) — HOW TO START EP 3: food truck NYC (R&D run, 2 Nov 2026) =================
# Generic, logo-free assets for the food-truck board (episodes/queue/06-food-truck-nyc):
#   foodtruck_el(w, open_, menu, glow, permit, col)   side view of a step-van food truck: serving window, striped awning (open_), menu board,
#                                                     permit sticker on the door (permit=False = dashed empty outline), roof vent
#   permit_el(w, price, stamped)                      plain city permit card (no seal): title, number line, price corner, optional VALID stamp
#   set "commissary"                                  garage-kitchen base: roll-up door, steel prep tables, wash bay + hose, parked truck rears
def foodtruck_el(w=800, open_=True, menu="TACOS", glow=1.0, permit=True, col=(255, 196, 40)):
    g = round(float(clamp(glow)), 2)
    def mk():
        h = int(w * 0.78); im, d, S = _im4(w, h); o = _O4; sc = 2
        body = tuple(int(v) for v in col); dark = tuple(int(v * 0.72) for v in col)
        bx0, by0, bx1, by1 = w * 0.03, h * 0.10, w * 0.80, h * 0.80          # box body
        cx1 = w * 0.97                                                       # cab front
        # cab (right): sloped windscreen
        d.polygon(S(bx1 - 4, h * 0.30, w * 0.90, h * 0.30, cx1, h * 0.50, cx1, by1, bx1 - 4, by1), fill=body + (255,), outline=o, width=6 * sc)
        d.polygon(S(bx1 + w * 0.02, h * 0.34, w * 0.885, h * 0.34, w * 0.94, h * 0.50, bx1 + w * 0.02, h * 0.50), fill=(150, 210, 240, 255), outline=o, width=4 * sc)
        d.ellipse(S(cx1 - w * 0.045, h * 0.60, cx1 - w * 0.005, h * 0.66), fill=(255, 250, 200, 255), outline=o, width=3 * sc)   # headlight
        # box
        d.rounded_rectangle(S(bx0, by0, bx1, by1), 16 * sc, fill=body + (255,), outline=o, width=6 * sc)
        d.rectangle(S(bx0 + 6, by1 - h * 0.10, bx1 - 6, by1 - 6), fill=dark + (255,))                                         # skirt band
        d.rounded_rectangle(S(w * 0.30, by0 - h * 0.07, w * 0.42, by0 + 4), 6 * sc, fill=(170, 176, 188, 255), outline=o, width=4 * sc)  # roof vent
        # serving window
        wx0, wy0, wx1, wy1 = w * 0.12, h * 0.28, w * 0.62, h * 0.56
        if open_:
            d.rectangle(S(wx0, wy0, wx1, wy1), fill=(60, 44, 40, 255), outline=o, width=5 * sc)
            if g > 0: d.rectangle(S(wx0 + 8, wy0 + 8, wx1 - 8, wy1 - 8), fill=(255, 214, 140, int(150 * g)))                # warm light inside
            d.rectangle(S(wx0 - 10, wy1, wx1 + 10, wy1 + h * 0.04), fill=(200, 204, 212, 255), outline=o, width=4 * sc)         # counter shelf
            # striped awning angled out over the window
            n = 7; ax0, ax1, ay0, ay1 = wx0 - 16, wx1 + 16, wy0 - h * 0.13, wy0
            d.polygon(S(ax0 + 20, ay1, ax1 - 20, ay1, ax1, ay0, ax0, ay0), fill=(255, 255, 255, 255), outline=o, width=4 * sc)
            for i in range(n):
                if i % 2 == 0:
                    xa = ax0 + (ax1 - ax0) * i / n; xb = ax0 + (ax1 - ax0) * (i + 1) / n
                    xa2 = ax0 + 20 + (ax1 - ax0 - 40) * i / n; xb2 = ax0 + 20 + (ax1 - ax0 - 40) * (i + 1) / n
                    d.polygon(S(xa, ay0, xb, ay0, xb2, ay1, xa2, ay1), fill=(230, 60, 60, 255))
            d.line(S(ax0, ay0, ax1, ay0), fill=o, width=4 * sc)
        else:
            d.rectangle(S(wx0, wy0, wx1, wy1), fill=(176, 180, 190, 255), outline=o, width=5 * sc)                             # shutter down
            for k in range(1, 6): d.line(S(wx0 + 6, wy0 + (wy1 - wy0) * k / 6, wx1 - 6, wy0 + (wy1 - wy0) * k / 6), fill=(130, 134, 144, 255), width=3 * sc)
        # menu board right of the window
        mx0, my0, mx1, my1 = w * 0.65, h * 0.26, w * 0.77, h * 0.52
        d.rounded_rectangle(S(mx0, my0, mx1, my1), 6 * sc, fill=(36, 38, 44, 255), outline=o, width=4 * sc)
        for k in range(4): d.line(S(mx0 + 10, my0 + 30 + k * (my1 - my0 - 40) / 4, mx1 - 14 - (k % 2) * 16, my0 + 30 + k * (my1 - my0 - 40) / 4), fill=(236, 236, 230, 255), width=3 * sc)
        # menu word on the box (plain text, no brand)
        if menu:
            fs = font(F_ANTON, int(h * 0.11 * sc)); d.text(S((wx0 + wx1) / 2, h * 0.68), str(menu), font=fs, fill=(30, 26, 36, 255), anchor="mm")
        # permit sticker on the cab door
        px0, py0, px1, py1 = bx1 + w * 0.025, h * 0.54, bx1 + w * 0.10, h * 0.64
        if permit:
            d.rectangle(S(px0, py0, px1, py1), fill=(255, 255, 255, 255), outline=o, width=3 * sc)
            d.rectangle(S(px0 + 4, py0 + 4, px1 - 4, py0 + (py1 - py0) * 0.35), fill=(40, 120, 220, 255))
        else:
            for k in range(8):                                                                                                # dashed empty outline
                t0, t1 = k / 8, (k + 0.5) / 8
                pts = [(px0, py0), (px1, py0), (px1, py1), (px0, py1), (px0, py0)]
                L = 2 * ((px1 - px0) + (py1 - py0))
                def at(u):
                    u *= L
                    for (a, b) in zip(pts, pts[1:]):
                        seg = math.hypot(b[0] - a[0], b[1] - a[1])
                        if u <= seg: return (a[0] + (b[0] - a[0]) * u / seg, a[1] + (b[1] - a[1]) * u / seg)
                        u -= seg
                    return pts[-1]
                p0, p1 = at(t0), at(t1); d.line(S(p0[0], p0[1], p1[0], p1[1]), fill=(240, 50, 50, 255), width=4 * sc)
        # wheels
        for wxc in (w * 0.20, w * 0.84):
            r = h * 0.11
            d.ellipse(S(wxc - r, by1 - r * 0.6, wxc + r, by1 + r * 1.4), fill=(34, 34, 40, 255), outline=o, width=5 * sc)
            d.ellipse(S(wxc - r * 0.45, by1 - r * 0.05, wxc + r * 0.45, by1 + r * 0.85), fill=(180, 184, 192, 255))
        return _el4(im, w, h)
    return gcache(("foodtruck5", int(w), bool(open_), menu, g, bool(permit), tuple(col)), mk)


def permit_el(w=420, price="$200", stamped=False):
    def mk():
        h = int(w * 0.62); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rounded_rectangle(S(6, 6, w - 6, h - 6), 14 * sc, fill=(250, 248, 238, 255), outline=o, width=5 * sc)
        d.rectangle(S(6, 6, w - 6, h * 0.24), fill=(40, 90, 170, 255)); d.rounded_rectangle(S(6, 6, w - 6, h - 6), 14 * sc, outline=o, width=5 * sc)
        fs = font(F_ANTON, int(h * 0.10 * sc)); d.text(S(w / 2, h * 0.15), "MOBILE FOOD VENDING", font=fs, fill=(255, 255, 255, 255), anchor="mm")
        fs2 = font(F_ANTON, int(h * 0.13 * sc)); d.text(S(w * 0.08, h * 0.40), "UNIT PERMIT", font=fs2, fill=(30, 26, 36, 255), anchor="lm")
        for k, yy in enumerate((0.58, 0.72)):
            d.line(S(w * 0.08, h * yy, w * (0.62 - 0.12 * k), h * yy), fill=(150, 150, 160, 255), width=3 * sc)
        fs3 = font(F_ANTON, int(h * 0.12 * sc)); d.text(S(w * 0.08, h * 0.86), "No. 0000", font=font(F_ANTON, int(h * 0.08 * sc)), fill=(110, 110, 120, 255), anchor="lm")
        if price:
            d.rounded_rectangle(S(w * 0.66, h * 0.52, w * 0.94, h * 0.84), 10 * sc, fill=(255, 210, 60, 255), outline=o, width=4 * sc)
            d.text(S(w * 0.80, h * 0.68), str(price), font=fs3, fill=(30, 26, 36, 255), anchor="mm")
        if stamped:
            ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(ov)
            q.rounded_rectangle(S(w * 0.30, h * 0.36, w * 0.74, h * 0.66), 8 * sc, outline=(220, 40, 40, 230), width=6 * sc)
            q.text(S(w * 0.52, h * 0.51), "VALID", font=fs2, fill=(220, 40, 40, 230), anchor="mm")
            im.alpha_composite(ov.rotate(-12, center=(w * sc * 0.52, h * sc * 0.51)))
        return _el4(im, w, h)
    return gcache(("permit5", int(w), price, bool(stamped)), mk)


def _commissary():
    f = np.zeros((H, W, 3), np.float32); y0 = 1220
    _srect(f, 0, 0, W, y0, (190, 196, 204), (160, 166, 176))                                    # painted block wall
    for yy in range(80, y0, 70): cv2.line(f, (0, yy), (W, yy), _scv((172, 178, 188)), 2, cv2.LINE_AA)
    _srect(f, 0, 0, W, 240, (60, 64, 72), (46, 50, 58))                                          # ceiling
    _strip_lights(f, 220, n=4, w_=140)
    # roll-up door at the back centre (open half-way, daylight + street outside)
    _srect(f, 300, 420, 780, 1000, (150, 200, 240), (220, 236, 246), (60, 60, 66), 4)            # daylight opening
    _srect(f, 300, 800, 780, 1000, (120, 124, 132), (96, 100, 108))                              # street outside
    _srect(f, 300, 420, 780, 620, (176, 180, 190), (140, 144, 154), (60, 60, 66), 3)             # rolled shutter (top half)
    for yy in range(440, 620, 24): cv2.line(f, (306, yy), (774, yy), _scv((130, 134, 144)), 3, cv2.LINE_AA)
    _srect(f, 280, 400, 800, 424, (90, 94, 104), (70, 74, 84), (40, 40, 46), 2)                  # door header
    # plain sign
    _srect(f, 600, 300, 920, 370, (36, 38, 44), (24, 26, 30), (90, 90, 96), 2)        # right of the cold-open card, left of the UI rail
    fs = font(F_ANTON, 46); im = Image.new("L", (320, 70), 0); ImageDraw.Draw(im).text((160, 35), "COMMISSARY", font=fs, fill=255, anchor="mm")
    m = np.asarray(im, np.float32) / 255; f[300:370, 600:920] = f[300:370, 600:920] * (1 - m[..., None]) + _c((246, 244, 236)) * m[..., None]
    # steel prep tables left, wash bay with hose reel right
    _srect(f, 20, 900, 270, 930, (226, 230, 236), (196, 200, 208), (90, 90, 96), 2)
    _srect(f, 30, 930, 260, 1120, (176, 182, 192), (130, 136, 146), (70, 70, 76), 2)
    for x in (40, 240): _srect(f, x, 1120, x + 14, y0, (150, 156, 166), (110, 116, 126))
    for (x, c) in ((70, (240, 80, 60)), (140, (90, 190, 90)), (200, (250, 200, 60))):              # tubs on the table
        _srect(f, x, 860, x + 50, 900, c, tuple(int(v * 0.75) for v in c), (50, 40, 40), 2)
    cv2.circle(f, (930, 760), 70, _scv((60, 140, 90)), -1, cv2.LINE_AA); cv2.circle(f, (930, 760), 70, _scv((26, 22, 34)), 4, cv2.LINE_AA)   # hose reel
    for r in (52, 36): cv2.circle(f, (930, 760), r, _scv((40, 110, 70)), 6, cv2.LINE_AA)
    cv2.line(f, (930, 830), (900, 1100), _scv((60, 140, 90)), 10, cv2.LINE_AA); cv2.line(f, (900, 1100), (980, 1180), _scv((60, 140, 90)), 10, cv2.LINE_AA)
    # floor: wet sealed concrete with a drain + a yellow bay line
    f[y0:] = 0; _sfloor(f, y0, 540, (150, 156, 164), (96, 102, 110), tile=False, n_lines=9, line_col=(124, 130, 138))
    cv2.ellipse(f, (860, 1500), (60, 16), 0, 0, 360, _scv((60, 64, 70)), -1, cv2.LINE_AA)
    for k in range(-3, 4): cv2.line(f, (860 + k * 14, 1488), (860 + k * 14, 1512), _scv((110, 116, 124)), 2, cv2.LINE_AA)
    cv2.line(f, (130, 1240), (40, 1920), _scv((240, 200, 40)), 12, cv2.LINE_AA); cv2.line(f, (950, 1240), (1040, 1920), _scv((240, 200, 40)), 12, cv2.LINE_AA)
    _sglow(f, 540, 700, 700, (240, 248, 255), 0.18)
    _atmos(f, "commissary")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


_STORY_SETS.update(commissary=_commissary)
_FLOOR.update(commissary=1220)
SET_LIGHT.update(commissary="cool")
SETS = tuple(_FLOOR)


# ---- staging helpers (3 Nov, HOW TO START EP 3): rope = velvet rope that clicks shut (a cap, a queue); steam = rising vent puffs ----
def steam(f, x, y, t, n=4, s=1.0):
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1.0; r = int((14 + 40 * ph) * s)
        ov = f.copy(); cv2.circle(ov, (int(x + 30 * math.sin(ph * 5 + i)), int(y - 240 * ph * s)), r, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
        a = 0.28 * clamp(ph * 6) * clamp(2.2 * (1 - ph)); f[:] = f * (1 - a) + ov * a


def rope(f, x0, x1, y, t, t_close=None, h=170):
    """velvet rope between two brass posts; t_close = the hook clicks across the gap at that moment"""
    k = 1.0 if t_close is None else eback(clamp((t - t_close) / 0.25))
    xm = x0 + (x1 - x0) * k
    for x in (x0, x1):
        cv2.rectangle(f, (int(x - 9), int(y - h)), (int(x + 9), int(y)), (0.72, 0.56, 0.18), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x - 9), int(y - h)), (int(x + 9), int(y)), (0.1, 0.08, 0.1), 3, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y - h)), 17, (0.9, 0.72, 0.25), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y - h)), 17, (0.1, 0.08, 0.1), 3, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), int(y)), (46, 13), 0, 0, 360, (0.72, 0.56, 0.18), -1, cv2.LINE_AA)
    pts = np.array([[x0 + (xm - x0) * q, y - h + 8 + 70 * math.sin(q * math.pi) * (0.6 + 0.4 * k)] for q in np.linspace(0, 1, 24)], np.int32)
    cv2.polylines(f, [pts], False, (0.1, 0.06, 0.08), 22, cv2.LINE_AA); cv2.polylines(f, [pts], False, (0.72, 0.1, 0.16), 15, cv2.LINE_AA)
