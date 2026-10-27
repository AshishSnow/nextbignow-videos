# ================= props for "Diamonds: how De Beers sold forever" (generic — no real logos or trade dress) =================
ICE = (196, 236, 255); ICE2 = (120, 190, 240); SEPIA = (112, 74, 40); PAPER = (244, 232, 204); VELVET = (150, 20, 60)
GOLDL = (255, 214, 110); GOLDD = (176, 122, 30)


def gem_el(w=300, col=ICE, cracked=0.0):
    """brilliant-cut diamond, side view: table, crown facets, pavilion to a point. cracked 0..1 draws fracture lines."""
    def mk():
        sc = 2; h = int(w * 0.86); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        top, girdle, tip = h * 0.06, h * 0.34, h * 0.97
        tl, tr = w * 0.27, w * 0.73; gl, gr = w * 0.03, w * 0.97; cx = w / 2
        base = tuple(col)
        lt = lambda c, k: tuple(int(min(255, v + (255 - v) * k)) for v in c)
        dk = lambda c, k: tuple(int(v * (1 - k)) for v in c)
        # crown: table + 4 facets
        d.polygon(S(tl, top, tr, top, gr, girdle, gl, girdle), fill=lt(base, 0.35) + (255,))
        d.polygon(S(tl, top, tr, top, cx + w * 0.12, girdle * 0.72 + top * 0.28, cx - w * 0.12, girdle * 0.72 + top * 0.28), fill=lt(base, 0.7) + (255,))
        d.polygon(S(gl, girdle, tl, top, cx - w * 0.22, girdle), fill=dk(base, 0.08) + (255,))
        d.polygon(S(gr, girdle, tr, top, cx + w * 0.22, girdle), fill=dk(base, 0.18) + (255,))
        # pavilion: 4 long facets to the tip
        d.polygon(S(gl, girdle, cx - w * 0.22, girdle, cx, tip), fill=dk(base, 0.25) + (255,))
        d.polygon(S(cx - w * 0.22, girdle, cx, girdle, cx, tip), fill=lt(base, 0.25) + (255,))
        d.polygon(S(cx, girdle, cx + w * 0.22, girdle, cx, tip), fill=dk(base, 0.05) + (255,))
        d.polygon(S(cx + w * 0.22, girdle, gr, girdle, cx, tip), fill=dk(base, 0.38) + (255,))
        ol = dk(base, 0.62) + (255,); lw = max(2, int(w / 90)) * sc
        for seg in ((tl, top, tr, top), (tr, top, gr, girdle), (gr, girdle, cx, tip), (cx, tip, gl, girdle), (gl, girdle, tl, top),
                    (gl, girdle, gr, girdle), (cx - w * 0.22, girdle, cx, tip), (cx + w * 0.22, girdle, cx, tip), (cx, girdle, cx, tip),
                    (tl, top, cx - w * 0.22, girdle), (tr, top, cx + w * 0.22, girdle)):
            d.line(S(*seg), fill=ol, width=lw)
        d.polygon(S(tl + w * 0.04, top + h * 0.03, tl + w * 0.13, top + h * 0.03, tl + w * 0.02, girdle - h * 0.05), fill=(255, 255, 255, 200))
        if cracked > 0:
            rnd = np.random.default_rng(11)
            for j in range(int(1 + 4 * cracked)):
                x, y = cx + rnd.uniform(-w * 0.15, w * 0.15), girdle + rnd.uniform(-h * 0.1, h * 0.1); pts = [(x, y)]
                for _ in range(5):
                    x += rnd.uniform(-w * 0.12, w * 0.12); y += rnd.uniform(-h * 0.14, h * 0.14); pts.append((x, y))
                d.line([(px * sc, py * sc) for px, py in pts], fill=(30, 30, 40, 255), width=max(3, int(w / 60)) * sc, joint="curve")
        return _done(im, w, h)
    return gcache(("gem", w, col, round(cracked, 2)), mk)


def ring_el(w=420, gem=True):
    """gold band (seen at an angle) with a solitaire on top"""
    def mk():
        sc = 2; h = int(w * 1.15); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        cy = h * 0.66; rx, ry = w * 0.44, h * 0.3
        shape_grad(im, lambda m: (m.ellipse(S(w / 2 - rx, cy - ry, w / 2 + rx, cy + ry), fill=255),
                                  m.ellipse(S(w / 2 - rx * 0.8, cy - ry * 0.74, w / 2 + rx * 0.8, cy + ry * 0.86), fill=0)), GOLDL, GOLDD)
        d.arc(S(w / 2 - rx + 6, cy - ry + 6, w / 2 + rx - 6, cy + ry - 6), 200, 300, fill=(255, 248, 220, 220), width=5 * sc)
        d.polygon(S(w / 2 - w * 0.12, cy - ry - 2, w / 2 + w * 0.12, cy - ry - 2, w / 2 + w * 0.07, cy - ry + h * 0.05, w / 2 - w * 0.07, cy - ry + h * 0.05), fill=GOLDD + (255,))
        if gem:
            g = gem_el(int(w * 0.5)); gi = Image.fromarray((np.dstack([g[0] / np.maximum(g[1][..., None], 1e-4), g[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
            gi = gi.resize((gi.size[0] * sc, gi.size[1] * sc), Image.LANCZOS)
            im.alpha_composite(gi, (int((w / 2) * sc - gi.size[0] / 2), int((cy - ry - h * 0.36) * sc)))
        return _done(im, w, h)
    return gcache(("ring", w, gem), mk)


def pillow_el(w=560):
    def mk():
        sc = 2; h = int(w * 0.42); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, h * 0.15, w, h), int(h * 0.4) * sc, fill=255), (200, 40, 90), (110, 10, 44))
        d.ellipse(S(w * 0.3, h * 0.2, w * 0.7, h * 0.48), fill=(90, 6, 36, 120))
        for x in (w * 0.08, w * 0.92):
            d.ellipse(S(x - 18, h * 0.82, x + 18, h + 0), fill=GOLDL + (255,))
        return _done(im, w, h)
    return gcache(("pillow", w), mk)


def hangtag_el(text, sub="", w=360, col=(255, 248, 230), fg=INK):
    """upright paper price tag, pointed top with a string hole at (w/2, 0.14 h); text horizontal"""
    def mk():
        sc = 2; h = int(w * 0.78); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w / 2, 3, w - 3, h * 0.26, w - 3, h - 3, 3, h - 3, 3, h * 0.26), fill=tuple(col) + (255,), outline=INK + (255,), width=5 * sc)
        d.ellipse(S(w / 2 - 13, h * 0.14 - 13, w / 2 + 13, h * 0.14 + 13), fill=(0, 0, 0, 0), outline=INK + (255,), width=4 * sc)
        fs = 66; fn = font(F_BLACK, fs * sc)
        while fn.getlength(text) / sc > w - 50 and fs > 20: fs -= 3; fn = font(F_BLACK, fs * sc)
        ty = h * 0.58 - (16 if sub else 0)
        d.text((w / 2 * sc, ty * sc), text, font=fn, fill=tuple(fg) + (255,), anchor="mm")
        if sub: d.text((w / 2 * sc, (ty + fs * 0.62 + 18) * sc), sub, font=font(F_BOLD, 28 * sc), fill=(120, 110, 100, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("htag", text, sub, w, col, fg), mk)


def swing_tag(f, el, x, y, t, amp=6.0, L=80, ph=0.0):
    """hang an upright tag from pin (x, y) on a string, swinging gently"""
    a = amp * math.sin(t * 2.4 + ph); ra = math.radians(a)
    hx, hy = x + L * math.sin(ra), y + L * math.cos(ra)
    cv2.line(f, (int(x), int(y)), (int(hx), int(hy)), C(INK), 4, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), 9, C(INK), -1, cv2.LINE_AA)
    h = el[1].shape[0]; dist = h * 0.36
    rot_comp(f, el, hx + dist * math.sin(ra), hy + dist * math.cos(ra), a, 1.0, 1.0, 0.3)


def bride_icon(f, x, y, s=1.0, lit=False, t=0.0):
    """bride icon: veil, head, dress. lit = white dress, warm glow, a sparkling diamond ring; unlit = faded"""
    ink = C(INK); lw = max(2, int(3 * s))
    if lit:
        cv2.circle(f, (int(x), int(y + 10 * s)), int(62 * s), C((255, 236, 150)), -1, cv2.LINE_AA)
    dress = C((255, 255, 255)) if lit else C((200, 192, 182)); veil = C((236, 244, 255)) if lit else C((214, 208, 200))
    cv2.fillPoly(f, [np.array([[x, y - 50 * s], [x - 32 * s, y + 24 * s], [x + 32 * s, y + 24 * s]], np.int32)], veil, cv2.LINE_AA)
    body = np.array([[x - 36 * s, y + 72 * s], [x + 36 * s, y + 72 * s], [x + 12 * s, y - 8 * s], [x - 12 * s, y - 8 * s]], np.int32)
    cv2.fillPoly(f, [body], dress, cv2.LINE_AA); cv2.polylines(f, [body], True, ink, lw, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y - 30 * s)), int(17 * s), C(SKIN) if lit else C((222, 214, 204)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y - 30 * s)), int(17 * s), ink, lw, cv2.LINE_AA)
    if lit:
        gx, gy = x + 26 * s, y + 20 * s; r = 12 * s * (1 + 0.12 * math.sin(t * 8))
        pts = np.array([[gx, gy - r], [gx + r * 0.8, gy], [gx, gy + r], [gx - r * 0.8, gy]], np.int32)
        cv2.fillPoly(f, [pts], C(ICE), cv2.LINE_AA); cv2.polylines(f, [pts], True, C((40, 110, 180)), lw, cv2.LINE_AA)
        sparkle(f, gx + 1.6 * r, gy - 1.6 * r, 1.4 * r, t, x * 0.01)


def sparkle(f, x, y, r, t, ph=0.0, col=(255, 255, 255)):
    k = 0.5 + 0.5 * math.sin(t * 6 + ph)
    if k < 0.15: return
    rr = r * k
    pts = np.array([[x, y - rr], [x + rr * 0.18, y - rr * 0.18], [x + rr, y], [x + rr * 0.18, y + rr * 0.18], [x, y + rr],
                    [x - rr * 0.18, y + rr * 0.18], [x - rr, y], [x - rr * 0.18, y - rr * 0.18]], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA)


def vault_wall(f, cx, cy, cols, rows, cell, k_open, t, locked=1.0):
    """wall of safe-deposit drawers; each holds gems; k_open = fraction of drawers lit/open"""
    x0 = cx - cols * cell / 2; y0 = cy - rows * cell / 2
    cv2.rectangle(f, (int(x0 - 18), int(y0 - 18)), (int(x0 + cols * cell + 18), int(y0 + rows * cell + 18)), C((70, 74, 86)), -1, cv2.LINE_AA)
    n = cols * rows
    for i in range(n):
        r, c = divmod(i, cols); x = x0 + c * cell; y = y0 + r * cell
        cv2.rectangle(f, (int(x + 6), int(y + 6)), (int(x + cell - 6), int(y + cell - 6)), C((160, 166, 180)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x + 6), int(y + 6)), (int(x + cell - 6), int(y + cell - 6)), C((60, 62, 72)), 3, cv2.LINE_AA)
        if (i * 7 % n) / n < k_open:
            comp(f, gem_el(int(cell * 0.5)), x + cell / 2, y + cell / 2)
            sparkle(f, x + cell * 0.7, y + cell * 0.3, cell * 0.12, t, i)
        else:
            cv2.circle(f, (int(x + cell / 2), int(y + cell / 2)), int(cell * 0.1), C((60, 62, 72)), -1, cv2.LINE_AA)
            if locked > 0.5: cv2.rectangle(f, (int(x + cell / 2 - 3), int(y + cell / 2)), (int(x + cell / 2 + 3), int(y + cell / 2 + cell * 0.18)), C((60, 62, 72)), -1)


def hourglass(f, cx, cy, h, top_k, t, drip=True):
    """hourglass of diamonds: top_k = how full the top bulb is (falls slowly), one gem drips through at a time"""
    w = h * 0.55
    frame = C(GOLDD)
    for yy in (cy - h / 2 - 16, cy + h / 2 + 16):
        cv2.rectangle(f, (int(cx - w / 2 - 40), int(yy - 14)), (int(cx + w / 2 + 40), int(yy + 14)), frame, -1, cv2.LINE_AA)
    glass = np.array([[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + 18, cy], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2], [cx - 18, cy]], np.int32)
    ov = f.copy(); cv2.fillPoly(ov, [glass], C((235, 245, 255)), cv2.LINE_AA); f[:] = f * 0.6 + ov * 0.4
    rnd = np.random.default_rng(4)
    # top bulb gems (stacked in a triangle that empties from the bottom)
    gs = 52
    for row in range(6):                       # top bulb: inverted triangle of gems, rows near the neck empty first
        n_ = 6 - row; y = cy - h / 2 + 46 + row * 44
        if row >= int(round(6 * top_k)): continue
        for c in range(n_): comp(f, gem_el(gs), cx + (c - (n_ - 1) / 2) * 50, y)
    for row in range(2):                       # bottom pile
        n_ = 3 - row; y = cy + h / 2 - 34 - row * 40
        for c in range(n_): comp(f, gem_el(gs), cx + (c - (n_ - 1) / 2) * 50, y)
    if drip:
        u = (t * 0.7) % 1.0; comp(f, gem_el(gs), cx, cy - 20 + u * (h / 2 - 90), op=clamp(u / 0.1) * clamp((1 - u) / 0.15))
    cv2.polylines(f, [glass], True, C((60, 90, 130)), 6, cv2.LINE_AA)


def minecart_el(w=520, load=1.0):
    def mk():
        sc = 2; h = int(w * 0.8); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rnd = np.random.default_rng(2)
        body_top = h * 0.36
        if load > 0:
            for i in range(int(40 * load)):
                gx = rnd.uniform(w * 0.14, w * 0.86); gy = body_top - rnd.uniform(0, h * 0.26) * (1 - abs(gx - w / 2) / (w * 0.45)) + 10
                g = gem_el(int(rnd.choice([54, 64, 74]))); gi = Image.fromarray((np.dstack([g[0] / np.maximum(g[1][..., None], 1e-4), g[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
                gi = gi.resize((gi.size[0] * sc, gi.size[1] * sc), Image.LANCZOS)
                im.alpha_composite(gi, (int(gx * sc - gi.size[0] / 2), int(gy * sc - gi.size[1] / 2)))
        shape_grad(im, lambda m: m.polygon(S(w * 0.04, body_top, w * 0.96, body_top, w * 0.86, h * 0.8, w * 0.14, h * 0.8), fill=255), (110, 116, 130), (60, 62, 74))
        d.rectangle(S(w * 0.02, body_top - 10, w * 0.98, body_top + 10), fill=(50, 52, 62, 255))
        for x in (w * 0.28, w * 0.72):
            d.ellipse(S(x - h * 0.12, h * 0.74, x + h * 0.12, h * 0.98), fill=(36, 36, 44, 255)); d.ellipse(S(x - h * 0.05, h * 0.81, x + h * 0.05, h * 0.91), fill=(160, 160, 170, 255))
        return _done(im, w, h)
    return gcache(("cart", w, round(load, 2)), mk)


def poster_el(lines, w=640, h=860, accent=(170, 30, 40)):
    """vintage 1940s print ad (sepia paper, serif type); lines = [(text, size, italic)]"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(8, 10, w, h), fill=(0, 0, 0, 70))
        shape_grad(im, lambda m: m.rectangle(S(0, 0, w - 8, h - 10), fill=255), (248, 238, 212), (228, 210, 172))
        d.rectangle(S(22, 22, w - 30, h - 32), outline=SEPIA + (255,), width=4 * sc)
        d.rectangle(S(34, 34, w - 42, h - 44), outline=SEPIA + (180,), width=2 * sc)
        y = 90
        for text, size, ital in lines:
            fn = font(F_PFI if ital else F_PF9, size * sc)
            while fn.getlength(text) / sc > w - 110 and size > 18: size -= 2; fn = font(F_PFI if ital else F_PF9, size * sc)
            d.text((w / 2 * sc - 4 * sc, y * sc), text, font=fn, fill=(accent if ital else SEPIA) + (255,), anchor="mt"); y += size * 1.35
        # ring line drawing in the middle
        cy = h * 0.62; d.ellipse(S(w / 2 - 110, cy - 50, w / 2 + 110, cy + 60), outline=SEPIA + (255,), width=8 * sc)
        d.polygon(S(w / 2 - 50, cy - 70, w / 2 + 50, cy - 70, w / 2, cy - 10), outline=SEPIA + (255,), fill=(255, 250, 235, 255), width=5 * sc)
        d.polygon(S(w / 2 - 50, cy - 70, w / 2 - 30, cy - 100, w / 2 + 30, cy - 100, w / 2 + 50, cy - 70), outline=SEPIA + (255,), fill=(255, 250, 235, 255), width=5 * sc)
        for k in range(6):
            a = -math.pi / 2 + (k - 2.5) * 0.45
            d.line(S(w / 2 + 120 * math.cos(a), cy - 80 + 90 * math.sin(a) - 40, w / 2 + 165 * math.cos(a), cy - 80 + 130 * math.sin(a) - 40), fill=SEPIA + (200,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("poster", tuple(lines), w, h), mk)


def typewriter(f, cx, cy, text, k, t, w=640):
    """typewriter with a sheet of paper; k = fraction of text typed"""
    pw, ph = w * 0.72, w * 0.62
    cv2.rectangle(f, (int(cx - pw / 2), int(cy - ph - 40)), (int(cx + pw / 2), int(cy - 40)), C(PAPER), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - pw / 2), int(cy - ph - 40)), (int(cx + pw / 2), int(cy - 40)), C((190, 170, 130)), 3, cv2.LINE_AA)
    n = int(len(text) * k); shown = text[:n]
    lines = shown.split("\n")
    for i, ln in enumerate(lines):
        if ln: comp(f, ed_el(ln, "", "", lead_col=INK, lead_size=50), cx, cy - ph + 40 + i * 70)
    if k < 1 and int(t * 4) % 2 == 0:
        cv2.rectangle(f, (int(cx - 6), int(cy - ph + 50 + (len(lines) - 1) * 70 + 20)), (int(cx + 18), int(cy - ph + 50 + (len(lines) - 1) * 70 + 26)), C(INK), -1)
    body = np.array([[cx - w / 2, cy + 200], [cx + w / 2, cy + 200], [cx + w / 2 - 40, cy - 30], [cx - w / 2 + 40, cy - 30]], np.int32)
    cv2.fillPoly(f, [body], C((40, 44, 52)), cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - w / 2 - 30), int(cy - 60)), (int(cx + w / 2 + 30), int(cy - 20)), C((24, 26, 30)), -1, cv2.LINE_AA)
    for r in range(3):
        for c in range(9):
            kx = cx - w / 2 + 90 + c * (w - 180) / 8 + (r % 2) * 18; ky = cy + 30 + r * 52
            press = (int(t * 14) + c * 3 + r) % 11 == 0 and k < 1
            cv2.circle(f, (int(kx), int(ky + (5 if press else 0))), 20, C((235, 230, 215)), -1, cv2.LINE_AA)
            cv2.circle(f, (int(kx), int(ky + (5 if press else 0))), 20, C((24, 26, 30)), 3, cv2.LINE_AA)


def medal_el(text="SLOGAN OF THE CENTURY", w=360):
    def mk():
        sc = 2; h = int(w * 1.35); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w * 0.3, h * 0.55, w * 0.18, h, w * 0.33, h * 0.92, w * 0.45, h), fill=(210, 30, 50, 255))
        d.polygon(S(w * 0.7, h * 0.55, w * 0.82, h, w * 0.67, h * 0.92, w * 0.55, h), fill=(210, 30, 50, 255))
        shape_grad(im, lambda m: m.ellipse(S(w * 0.04, w * 0.04, w * 0.96, w * 0.96), fill=255), GOLDL, GOLDD)
        d.ellipse(S(w * 0.13, w * 0.13, w * 0.87, w * 0.87), outline=(255, 245, 200, 255), width=5 * sc)
        words = text.split(" "); ls = [" ".join(words[:2]), " ".join(words[2:])] if len(words) > 2 else [text]
        for i, ln in enumerate(ls):
            fn = font(F_BLACK, 40 * sc)
            while fn.getlength(ln) / sc > w * 0.66: fn = font(F_BLACK, int(fn.size / sc - 2) * sc)
            d.text((w / 2 * sc, (w * 0.5 + (i - (len(ls) - 1) / 2) * 50) * sc), ln, font=fn, fill=(90, 50, 10, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("medal", text, w), mk)


def line_chart(f, x0, y0, x1, y1, pts, k, col=RED_, th=12, labels=None, grid=True):
    """animated line chart in a box; pts = [(u, v)] with u,v in 0..1 (v=1 top); k = draw progress"""
    cv2.rectangle(f, (x0, y0), (x1, y1), C((255, 255, 255)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INK), 5, cv2.LINE_AA)
    if grid:
        for g in range(1, 4):
            yy = int(y0 + (y1 - y0) * g / 4); cv2.line(f, (x0 + 10, yy), (x1 - 10, yy), C((225, 225, 232)), 2, cv2.LINE_AA)
    P = [(x0 + 40 + u * (x1 - x0 - 80), y1 - 40 - v * (y1 - y0 - 80)) for u, v in pts]
    n = len(P) - 1; seg = k * n; out = [P[0]]
    for i in range(n):
        if seg >= i + 1: out.append(P[i + 1])
        elif seg > i:
            q = seg - i; out.append((P[i][0] + (P[i + 1][0] - P[i][0]) * q, P[i][1] + (P[i + 1][1] - P[i][1]) * q)); break
    if len(out) > 1: cv2.polylines(f, [np.array(out, np.int32)], False, C(col), th, cv2.LINE_AA)
    cv2.circle(f, (int(out[-1][0]), int(out[-1][1])), th + 6, C(col), -1, cv2.LINE_AA)
    if labels:
        for (u, txt) in labels: comp(f, ed_el(txt, "", "", lead_col=INK, lead_size=30), x0 + 40 + u * (x1 - x0 - 80), y1 + 34)
    return out[-1]


def flask_el(w=360, fill=0.6):
    """lab reactor / bell jar (generic)"""
    def mk():
        sc = 2; h = int(w * 1.35); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(w * 0.08, h * 0.86, w * 0.92, h), 14 * sc, fill=(60, 64, 76, 255))
        d.rounded_rectangle(S(w * 0.14, h * 0.12, w * 0.86, h * 0.87), int(w * 0.36) * sc, fill=(220, 240, 255, 110), outline=(80, 120, 170, 255), width=6 * sc)
        d.rectangle(S(w * 0.18, h * 0.87 - (h * 0.72) * fill * 0.25, w * 0.82, h * 0.86), fill=(150, 90, 255, 90))
        d.rounded_rectangle(S(w * 0.38, h * 0.02, w * 0.62, h * 0.14), 10 * sc, fill=(60, 64, 76, 255))
        d.arc(S(w * 0.2, h * 0.16, w * 0.5, h * 0.5), 190, 260, fill=(255, 255, 255, 200), width=8 * sc)
        return _done(im, w, h)
    return gcache(("flask", w, round(fill, 2)), mk)


def closed_sign_el(text="CLOSED", w=420):
    def mk():
        sc = 2; h = int(w * 0.62); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.line(S(w * 0.2, 0, w * 0.5, h * 0.22), fill=INK + (255,), width=5 * sc); d.line(S(w * 0.8, 0, w * 0.5, h * 0.22), fill=INK + (255,), width=5 * sc)
        d.rounded_rectangle(S(0, h * 0.22, w - 1, h - 1), 18 * sc, fill=RED_ + (255,), outline=INK + (255,), width=6 * sc)
        fn = font(F_BLACK, 90 * sc)
        while fn.getlength(text) / sc > w * 0.82: fn = font(F_BLACK, int(fn.size / sc - 4) * sc)
        d.text((w / 2 * sc, h * 0.61 * sc), text, font=fn, fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("closed", text, w), mk)
