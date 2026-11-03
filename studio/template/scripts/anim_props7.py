# ================= props kit 7 (exec'd after anim_props6.py) — HOW TO START EP 4: Christmas-light install (episode run, 3 Nov 2026) =================
# Clean, flat, logo-free. house_flat_el + roof_pts = big flat house and its roofline; bulb_string = glowing bulbs that switch on in a wave along any polyline;
# ladder = fibreglass ladder drawn foot → top; tape_run = tape measure along a line; snow = sparse flat snowfall; spool_el = reel of lights; year_strip_el = 12 month tiles;
# dim_arrow = double-headed measure arrow; power_line = pole + two wires.
_BULB_COLS = [(255, 70, 70), (255, 205, 60), (70, 220, 120), (70, 170, 255), (255, 130, 220)]


def _glow_sprite(col, r):
    def mk():
        R_ = int(r * 3.2); yy, xx = np.mgrid[-R_:R_ + 1, -R_:R_ + 1]; d2 = (xx ** 2 + yy ** 2) / float(R_ * R_)
        a = np.clip(1 - d2, 0, 1) ** 2.2 * 0.75
        return a[..., None] * (np.array(col, np.float32) / 255 * 0.9 + 0.1), R_
    return gcache(("glowsp", col, r), mk)


def _add_glow(f, x, y, col, r, k=1.0):
    sp, R_ = _glow_sprite(col, r); x = int(x); y = int(y)
    x0, y0 = max(0, x - R_), max(0, y - R_); x1, y1 = min(W, x + R_ + 1), min(H, y + R_ + 1)
    if x1 <= x0 or y1 <= y0: return
    f[y0:y1, x0:x1] = np.minimum(1.0, f[y0:y1, x0:x1] + k * sp[y0 - (y - R_):y1 - (y - R_), x0 - (x - R_):x1 - (x - R_)])


def poly_points(pts, step):
    out = []; carry = 0.0; s = 0.0
    for (a, b) in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); q = carry
        while q <= L:
            out.append((a[0] + (b[0] - a[0]) * q / max(L, 1e-6), a[1] + (b[1] - a[1]) * q / max(L, 1e-6), s + q)); q += step
        carry = q - L; s += L
    return out, s


def bulb_string(f, pts, t, t_on=0.0, speed=1400.0, step=44, r=12, cols=None, on=1.0, wire=True, dead=None):
    """wire + bulbs along a polyline; bulbs switch on in a wave from the first point at t_on (speed px/s); on = master level 0..1; dead(i) -> True keeps a bulb dark"""
    cols = cols or _BULB_COLS
    if wire:
        cv2.polylines(f, [np.array(pts, np.int32)], False, (0.05, 0.05, 0.07), 5, cv2.LINE_AA)
    P, _ = poly_points(pts, step)
    for i, (x, y, s) in enumerate(P):
        c = cols[i % len(cols)]; lit = clamp((t - t_on - s / speed) / 0.12) * on
        if dead is not None and dead(i): lit = 0.0
        tw = 0.9 + 0.1 * math.sin(t * 3.1 + i * 1.7)
        base = tuple(float(v) / 255 * (0.32 + 0.68 * lit) for v in c)
        cv2.circle(f, (int(x), int(y + r * 0.7)), r, base, -1, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y + r * 0.7)), r, (0.05, 0.05, 0.07), 2, cv2.LINE_AA)
        if lit > 0.02: _add_glow(f, x, y + r * 0.7, c, r, 0.9 * lit * tw)


def house_flat_el(w=760, wall=(40, 56, 130), roof=(24, 30, 72), win=1.0, door=(170, 50, 60), snow_=True):
    wn = round(float(clamp(win)), 2)
    def mk():
        h = int(w * 0.86); im, d, S = _im4(w, h); o = _O4; sc = 2
        d.rectangle(S(w * 0.70, h * 0.10, w * 0.80, h * 0.34), fill=tuple(roof) + (255,), outline=o, width=5 * sc)
        d.rectangle(S(w * 0.10, h * 0.42, w * 0.90, h * 0.98), fill=tuple(wall) + (255,), outline=o, width=6 * sc)
        d.polygon(S(w * 0.02, h * 0.44, w * 0.5, h * 0.06, w * 0.98, h * 0.44), fill=tuple(roof) + (255,), outline=o, width=6 * sc)
        if snow_: d.polygon(S(w * 0.33, h * 0.195, w * 0.5, h * 0.06, w * 0.67, h * 0.195, w * 0.58, h * 0.17, w * 0.5, h * 0.20, w * 0.42, h * 0.17), fill=(236, 242, 252, 255), outline=o, width=3 * sc)
        wc = tuple(int(a + (b - a) * wn) for a, b in zip((30, 36, 70), (255, 226, 130)))
        for xx in (w * 0.18, w * 0.64):
            d.rectangle(S(xx, h * 0.54, xx + w * 0.18, h * 0.76), fill=wc + (255,), outline=o, width=5 * sc)
            d.line(S(xx + w * 0.09, h * 0.54, xx + w * 0.09, h * 0.76), fill=o, width=4 * sc); d.line(S(xx, h * 0.65, xx + w * 0.18, h * 0.65), fill=o, width=4 * sc)
        d.rounded_rectangle(S(w * 0.43, h * 0.60, w * 0.57, h * 0.98), 8 * sc, fill=tuple(door) + (255,), outline=o, width=5 * sc)
        return _el4(im, w, h)
    return gcache(("hflat", w, wall, roof, wn, door, snow_), mk)


def roof_pts(cx, cy, w):
    """roofline polyline of a house_flat_el(w) composited at centre (cx, cy): left eave → peak → right eave"""
    h = int(w * 0.86); x0 = cx - w / 2; y0 = cy - h / 2
    return [(x0 + w * 0.02, y0 + h * 0.44), (x0 + w * 0.5, y0 + h * 0.06), (x0 + w * 0.98, y0 + h * 0.44)]


def eave_pts(cx, cy, w):
    h = int(w * 0.86); x0 = cx - w / 2; y0 = cy - h / 2
    return [(x0 + w * 0.02, y0 + h * 0.445), (x0 + w * 0.98, y0 + h * 0.445)]


def ladder(f, x0, y0, x1, y1, width=70, col=(250, 186, 40), rungs=None):
    """fibreglass ladder from foot (x0, y0) to top (x1, y1)"""
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    c = tuple(float(v) / 255 for v in col); o = (0.09, 0.08, 0.13)
    n = rungs or max(4, int(L / 62))
    for i in range(1, n):
        q = i / n; a = (x0 + (x1 - x0) * q - nx * width / 2, y0 + (y1 - y0) * q - ny * width / 2); b = (a[0] + nx * width, a[1] + ny * width)
        cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), o, 13, cv2.LINE_AA); cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), (0.92, 0.92, 0.94), 7, cv2.LINE_AA)
    for sgn in (-1, 1):
        a = (int(x0 + sgn * nx * width / 2), int(y0 + sgn * ny * width / 2)); b = (int(x1 + sgn * nx * width / 2), int(y1 + sgn * ny * width / 2))
        cv2.line(f, a, b, o, 19, cv2.LINE_AA); cv2.line(f, a, b, c, 12, cv2.LINE_AA)


def tape_run(f, x0, y0, x1, y1, k=1.0):
    """tape measure pulled from (x0, y0) towards (x1, y1), k = 0..1; ticks on the blade, case at the moving end"""
    k = clamp(k); xe = x0 + (x1 - x0) * k; ye = y0 + (y1 - y0) * k; L = math.hypot(xe - x0, ye - y0)
    cv2.line(f, (int(x0), int(y0)), (int(xe), int(ye)), (0.09, 0.08, 0.13), 26, cv2.LINE_AA); cv2.line(f, (int(x0), int(y0)), (int(xe), int(ye)), (1.0, 0.82, 0.16), 18, cv2.LINE_AA)
    if L > 1:
        ux, uy = (xe - x0) / L, (ye - y0) / L
        for q in range(0, int(L), 28):
            a = (int(x0 + ux * q), int(y0 + uy * q)); cv2.line(f, a, (int(a[0] - uy * 9), int(a[1] + ux * 9)), (0.09, 0.08, 0.13), 2, cv2.LINE_AA)
    cv2.rectangle(f, (int(xe - 34), int(ye - 34)), (int(xe + 34), int(ye + 34)), (0.09, 0.08, 0.13), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(xe - 28), int(ye - 28)), (int(xe + 28), int(ye + 28)), (0.93, 0.25, 0.22), -1, cv2.LINE_AA)


def snow(f, t, n=46, seed=3, y1=1900, op=0.8):
    r = np.random.default_rng(seed)
    xs = r.uniform(0, W, n); sp = r.uniform(45, 110, n); ph = r.uniform(0, 1, n); sz = r.integers(3, 8, n)
    for i in range(n):
        y = (ph[i] * y1 + sp[i] * t) % y1; x = xs[i] + 24 * math.sin(t * 0.8 + i)
        cv2.circle(f, (int(x), int(y)), int(sz[i]), (op, op, op) if False else (0.96, 0.97, 1.0), -1, cv2.LINE_AA)


def spool_el(w=360, col=(40, 200, 120)):
    def mk():
        h = w; im, d, S = _im4(w, h); o = _O4; sc = 2
        d.ellipse(S(w * 0.04, h * 0.04, w * 0.96, h * 0.96), fill=tuple(col) + (255,), outline=o, width=7 * sc)
        d.ellipse(S(w * 0.2, h * 0.2, w * 0.8, h * 0.8), fill=(30, 34, 46, 255), outline=o, width=5 * sc)
        for i in range(14):
            a = i / 14 * 2 * math.pi; x = w / 2 + w * 0.3 * math.cos(a); y = h / 2 + h * 0.3 * math.sin(a); c = _BULB_COLS[i % 5]
            d.ellipse(S(x - w * 0.035, y - w * 0.035, x + w * 0.035, y + w * 0.035), fill=tuple(c) + (255,), outline=o, width=2 * sc)
        d.ellipse(S(w * 0.42, h * 0.42, w * 0.58, h * 0.58), fill=(240, 240, 244, 255), outline=o, width=5 * sc)
        return _el4(im, w, h)
    return gcache(("spool", w, col), mk)


def year_strip_el(w=820, lit=(10, 11)):
    def mk():
        cols = 6; gap = 12; tw = (w - gap * (cols - 1)) / cols; th = tw * 0.92; h = int(th * 2 + gap)
        im, d, S = _im4(w, h); o = _O4; sc = 2; fn = font(F_ANTON, int(tw * 0.5 * sc))
        for i, m_ in enumerate("JFMAMJJASOND"):
            x = (i % cols) * (tw + gap); y = (i // cols) * (th + gap); on = i in lit
            d.rounded_rectangle(S(x + 2, y + 2, x + tw - 2, y + th - 2), 14 * sc, fill=(255, 205, 50, 255) if on else (44, 50, 78, 255), outline=o, width=5 * sc)
            d.text(S(x + tw / 2, y + th / 2), m_, font=fn, fill=(26, 22, 34, 255) if on else (120, 128, 160, 255), anchor="mm")
        return _el4(im, w, h)
    return gcache(("ystrip", w, lit), mk)


def dim_arrow(f, x0, y0, x1, y1, col=(1.0, 1.0, 1.0), th=7):
    cv2.arrowedLine(f, (int(x0), int(y0)), (int(x1), int(y1)), col, th, cv2.LINE_AA, tipLength=0.14)
    cv2.arrowedLine(f, (int(x1), int(y1)), (int(x0), int(y0)), col, th, cv2.LINE_AA, tipLength=0.14)


def power_line(f, y=760, x_pole=880, y_ground=1400, sag=26):
    o = (0.08, 0.07, 0.11)
    cv2.rectangle(f, (x_pole - 13, y - 50), (x_pole + 13, y_ground), (0.20, 0.14, 0.14), -1, cv2.LINE_AA); cv2.rectangle(f, (x_pole - 13, y - 50), (x_pole + 13, y_ground), o, 3, cv2.LINE_AA)
    cv2.rectangle(f, (x_pole - 90, y - 34), (x_pole + 90, y - 12), (0.20, 0.14, 0.14), -1, cv2.LINE_AA); cv2.rectangle(f, (x_pole - 90, y - 34), (x_pole + 90, y - 12), o, 3, cv2.LINE_AA)
    for dy, x_ in ((-40, x_pole - 80), (-40, x_pole + 80)):
        P = np.array([[xx, y + dy + (sag * (1 - ((xx - x_pole) / 900.0) ** 2) if xx < x_pole else 0)] for xx in range(-40, W + 40, 40)], np.int32)
        cv2.polylines(f, [P], False, o, 5, cv2.LINE_AA)
        y += 18


def mini_card(f, top, mid, x=72, y=262, op=1.0):
    """compact step/cold-open tag (owner 3 Nov: keep cards small and tidy): small yellow line + one title line, top-left, ends above y≈400"""
    def mk():
        a = _stxt_el(top, 38, (255, 206, 60)); b = _stxt_el(mid, 66)
        w = max(a.size[0], b.size[0]) + 40; h = a.size[1] + b.size[1] + 6
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(14, 14, 20, 190))
        im.alpha_composite(a, (20, 8)); im.alpha_composite(b, (18, 2 + a.size[1] - 6))
        return el_from(im)
    el = gcache(("minicard", top, mid), mk)
    comp(f, el, x, y + el[1].shape[0] / 2, op=op, anchor="l")
