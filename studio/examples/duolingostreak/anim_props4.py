# ================= props for "Duolingo's streak" (generic app / habit props — no owl, no app branding, no trade dress) =================
FLAME_O = (255, 120, 20); FLAME_Y = (255, 214, 60); FLAME_R = (232, 50, 30); SCREEN = (250, 250, 255); PURP = (120, 70, 230)
APPBLUE = (40, 140, 255)


def flame_el(w=300, h=380, num=None, lit=1.0, num_col=WHITE):
    """streak flame: layered teardrop flame; lit 0 = grey, burnt-out; optional number inside"""
    key = ("flame", w, h, num, round(lit, 2), num_col)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        def tear(cx, by, rw, rh):
            pts = []
            for i in range(41):
                a = math.pi * i / 40
                pts += [cx + rw * math.cos(a + math.pi), by - rh * 0.42 * math.sin(a)]
            pts += [cx + rw * 0.9, by - rh * 0.55, cx + rw * 0.35, by - rh * 0.8, cx + rw * 0.1, by - rh,
                    cx - rw * 0.25, by - rh * 0.78, cx - rw * 0.55, by - rh * 0.88, cx - rw * 0.85, by - rh * 0.58]
            return [p * sc for p in pts]
        mix = lambda c: tuple(int(v * lit + 170 * (1 - lit)) for v in c)
        _ov(im, lambda q: q.polygon(tear(w / 2 + 10, h - 6, w * 0.44, h * 0.92), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.polygon(tear(w / 2, h - 16, w * 0.44, h * 0.92), fill=255), mix(FLAME_Y), mix(FLAME_R))
        d.polygon(tear(w / 2, h - 16, w * 0.44, h * 0.92), outline=INK + (255,), width=max(2, int(6 * min(1.0, w / 240))) * sc)
        shape_grad(im, lambda m: m.polygon(tear(w / 2, h - 30, w * 0.26, h * 0.52), fill=255), (255, 250, 210), mix(FLAME_Y))
        if num is not None:
            fs = int(h * (0.26 if len(num) > 2 else 0.32))
            d.text((w / 2 * sc, (h - 16 - h * 0.25) * sc), num, font=font(F_BLACK, fs * sc), fill=INK + (255,), anchor="mm",
                   stroke_width=0)
        return _done(im, w, h)
    return gcache(key, mk)


def app_phone(screen="streak", w=440, h=820, num="365", ad_k=0.0, label=None, lit=1.0):
    """generic phone; screens: 'streak' (flame + day count), 'lesson' (lesson complete), 'ad' (ad with skip), 'notif'"""
    key = ("aphone", screen, w, h, num, round(ad_k, 1), label, round(lit, 2))
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(18, 20, w - 2, h - 2), 58 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, w - 18, h - 20), 58 * sc, fill=INK + (255,))
        sx0, sy0, sx1, sy1 = 22, 60, w - 40, h - 64
        if screen == "ad":
            shape_grad(im, lambda m: m.rounded_rectangle(S(sx0, sy0, sx1, sy1), 30 * sc, fill=255), (255, 220, 90), (255, 120, 60))
        else:
            d.rounded_rectangle(S(sx0, sy0, sx1, sy1), 30 * sc, fill=SCREEN + (255,))
        d.rounded_rectangle(S(w / 2 - 70, 24, w / 2 + 50, 40), 8 * sc, fill=(60, 60, 70, 255))
        cx = (sx0 + sx1) / 2
        if screen == "streak":
            fl = flame_el(int((sx1 - sx0) * 0.62), int((sx1 - sx0) * 0.8), None, lit)
            fim = Image.fromarray((np.dstack([fl[0] / np.maximum(fl[1][..., None], 1e-4), fl[1]]) * 255).clip(0, 255).astype(np.uint8), "RGBA")
            fim = fim.resize((fim.size[0] * sc, fim.size[1] * sc), Image.LANCZOS)
            im.alpha_composite(fim, (int((cx - fl[1].shape[1] / 2) * sc), int((sy0 + 70) * sc)))
            d.text((cx * sc, (sy0 + 70 + fl[1].shape[0] + 70) * sc), num, font=font(F_BLACK, 110 * sc), fill=INK + (255,), anchor="mm")
            d.text((cx * sc, (sy0 + 70 + fl[1].shape[0] + 150) * sc), label or "DAY STREAK", font=font(F_BLACK, 40 * sc), fill=(255, 120, 20, 255), anchor="mm")
        elif screen == "lesson":
            d.text((cx * sc, (sy0 + 120) * sc), "LESSON", font=font(F_BLACK, 56 * sc), fill=INK + (255,), anchor="mm")
            d.text((cx * sc, (sy0 + 185) * sc), "COMPLETE!", font=font(F_BLACK, 56 * sc), fill=APPBLUE + (255,), anchor="mm")
            for i in range(3):
                x = cx - 110 + i * 110
                star = []
                for j in range(10):
                    rr = 48 if j % 2 == 0 else 20; aa = -math.pi / 2 + j * math.pi / 5
                    star += [(x + rr * math.cos(aa)) * sc, (sy0 + 330 + rr * math.sin(aa)) * sc]
                d.polygon(star, fill=YEL_ + (255,), outline=INK + (255,), width=3 * sc)
            d.rounded_rectangle(S(sx0 + 40, sy1 - 140, sx1 - 40, sy1 - 50), 24 * sc, fill=APPBLUE + (255,), outline=INK + (255,), width=4 * sc)
            d.text((cx * sc, (sy1 - 95) * sc), label or "CONTINUE", font=font(F_BLACK, 42 * sc), fill=(255, 255, 255, 255), anchor="mm")
        elif screen == "ad":
            d.text((cx * sc, (sy0 + 110) * sc), "AD", font=font(F_BLACK, 150 * sc), fill=(255, 255, 255, 255), anchor="mm",
                   stroke_width=5 * sc, stroke_fill=INK + (255,))
            d.rounded_rectangle(S(sx0 + 40, sy0 + 230, sx1 - 40, sy0 + 470), 24 * sc, fill=(255, 255, 255, 235), outline=INK + (255,), width=4 * sc)
            d.text((cx * sc, (sy0 + 300) * sc), "BUY", font=font(F_BLACK, 70 * sc), fill=INK + (255,), anchor="mm")
            d.text((cx * sc, (sy0 + 400) * sc), "STUFF!", font=font(F_BLACK, 70 * sc), fill=RED_ + (255,), anchor="mm")
            d.rounded_rectangle(S(sx1 - 190, sy1 - 110, sx1 - 30, sy1 - 40), 18 * sc, fill=INK + (230,))
            d.text(((sx1 - 110) * sc, (sy1 - 75) * sc), f"SKIP {max(0, 5 - int(ad_k * 5))}", font=font(F_BOLD, 34 * sc), fill=(255, 255, 255, 255), anchor="mm")
        elif screen == "notif":
            d.text((cx * sc, (sy0 + 70) * sc), "9:41", font=font(F_BLACK, 60 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(key, mk)


def notif_el(text="Time for today's lesson!", sub="Don't lose your streak", w=620, h=150):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 12, w - 2, h - 2), 34 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, w - 10, h - 12), 34 * sc, fill=(255, 255, 255, 250), outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(22, 26, 112, 116), 22 * sc, fill=FLAME_O + (255,), outline=INK + (255,), width=3 * sc)
        d.text((67 * sc, 71 * sc), "!", font=font(F_BLACK, 64 * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text((136 * sc, 52 * sc), text, font=font(F_BLACK, 34 * sc), fill=INK + (255,), anchor="lm")
        d.text((136 * sc, 98 * sc), sub, font=font(F_SEMI, 30 * sc), fill=(90, 90, 100, 255), anchor="lm")
        return _done(im, w, h)
    return gcache(("notif", text, sub, w, h), mk)


def course_el(word, col, w=300, h=200):
    """generic language course card with a greeting word (no flags, no app branding)"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 12, w - 2, h - 2), 26 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(0, 0, w - 10, h - 12), 26 * sc, fill=255), col, tuple(int(v * 0.78) for v in col))
        d.rounded_rectangle(S(0, 0, w - 10, h - 12), 26 * sc, outline=INK + (255,), width=5 * sc)
        d.text(((w - 10) / 2 * sc, (h - 12) / 2 * sc), word, font=font(F_BLACK, 58 * sc), fill=(255, 255, 255, 255), anchor="mm",
               stroke_width=3 * sc, stroke_fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("course", word, col, w, h), mk)


def envelope_el(w=620, h=420, open_k=0.0, label="THE NUMBER"):
    def mk():
        sc = 2; im, d = _canvas(w, h + 200); S = lambda *v: [x * sc for x in v]
        top = 200
        _ov(im, lambda q: q.rectangle(S(14, top + 14, w - 2, top + h - 2), fill=(0, 0, 0, 70)))
        d.rectangle(S(0, top, w - 14, top + h - 14), fill=(250, 236, 205, 255), outline=INK + (255,), width=5 * sc)
        if open_k > 0.5:
            d.rectangle(S(40, top - 150 * (open_k - 0.5) * 2 + 30, w - 54, top + h - 60), fill=(255, 255, 255, 255), outline=INK + (255,), width=4 * sc)
            d.text(((w - 14) / 2 * sc, (top - 150 * (open_k - 0.5) * 2 + 110) * sc), "???", font=font(F_BLACK, 80 * sc), fill=RED_ + (255,), anchor="mm")
        d.polygon(S(0, top + h - 14, (w - 14) / 2, top + h * 0.45, w - 14, top + h - 14), fill=(240, 222, 186, 255), outline=INK + (255,), width=4 * sc)
        fy = top + (h * 0.5) * (1 - 2 * min(open_k, 0.5) * 2) if open_k < 0.5 else top - h * 0.45 * (open_k - 0.5) * 2
        d.polygon(S(0, top, (w - 14) / 2, fy, w - 14, top), fill=(244, 228, 194, 255), outline=INK + (255,), width=4 * sc)
        if open_k < 0.3:
            d.ellipse(S((w - 14) / 2 - 50, top + h * 0.38 - 50, (w - 14) / 2 + 50, top + h * 0.38 + 50), fill=RED_ + (255,), outline=INK + (255,), width=4 * sc)
        d.text(((w - 14) / 2 * sc, (top + h - 60) * sc), label, font=font(F_BLACK, 44 * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w, h + 200)
    return gcache(("env", w, h, round(open_k, 2), label), mk)


def heatmap(f, cx, cy, k, cols=26, rows=14, cell=26, gap=5, col=FLAME_O, dim=(255, 255, 255)):
    """year grid (364 days) filling column by column as k goes 0..1"""
    n = cols * rows; on = int(round(n * clamp(k))); s = cell + gap
    x0 = int(cx - cols * s / 2); y0 = int(cy - rows * s / 2)
    cv2.rectangle(f, (x0 - 22, y0 - 22), (x0 + cols * s + 16, y0 + rows * s + 16), C(INK), -1, cv2.LINE_AA)
    for i in range(n):
        c_, r_ = divmod(i, rows); x = x0 + c_ * s; y = y0 + r_ * s
        shade = 0.75 + 0.25 * ((i * 37) % 7) / 6
        colr = tuple(min(255, int(v * shade)) for v in col) if i < on else (70, 70, 84)
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(colr), -1, cv2.LINE_AA)


def week_strip(f, cx, cy, done, miss=-1, cell=110, gap=14, t=0.0, labels="MTWTFSS", x_k=1.0):
    """7 day boxes: first `done` get a flame check; box `miss` gets a red X (scaled by x_k)"""
    s = cell + gap; x0 = cx - 7 * s / 2 + gap / 2
    for i in range(7):
        x = int(x0 + i * s); y = int(cy - cell / 2)
        cv2.rectangle(f, (x + 6, y + 8), (x + cell + 6, y + cell + 8), (0, 0, 0), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C((255, 255, 255)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(INK), 5, cv2.LINE_AA)
        comp(f, ed_el("", labels[i], "", big_col=INK, big_size=34, maxw=80), x + cell / 2, y - 34)
        if i < done: comp(f, flame_el(int(cell * 0.7), int(cell * 0.86)), x + cell / 2, y + cell / 2 + 4)
        if i == miss and x_k > 0:
            L = int(cell * 0.38 * clamp(x_k)); c0 = (x + cell // 2, y + cell // 2)
            for sg in (1, -1):
                cv2.line(f, (c0[0] - L, c0[1] - sg * L), (c0[0] + L, c0[1] + sg * L), C(RED_), 16, cv2.LINE_AA)


def heart_line(f, x0, x1, y, t, k, col=(60, 230, 120), amp=90):
    """ECG line drawn up to fraction k with a moving beat"""
    pts = []
    n = 160
    for i in range(int(n * clamp(k)) + 1):
        q = i / n; x = x0 + (x1 - x0) * q; ph = (q * 3 + 0.2) % 1.0
        yy = y - amp * (math.exp(-((ph - 0.5) / 0.03) ** 2) - 0.45 * math.exp(-((ph - 0.56) / 0.03) ** 2) + 0.15 * math.exp(-((ph - 0.3) / 0.06) ** 2))
        pts.append([x, yy])
    if len(pts) > 1:
        p = np.array(pts, np.int32)
        cv2.polylines(f, [p], False, C(INK), 16, cv2.LINE_AA); cv2.polylines(f, [p], False, C(col), 9, cv2.LINE_AA)
        cv2.circle(f, tuple(p[-1]), 14, C(WHITE), -1, cv2.LINE_AA)


def loop_diagram(f, cx, cy, r, steps, k, t, cols):
    """circular habit loop: arrow ring + step bubbles appearing in order as k goes 0..1"""
    n = len(steps)
    ang_end = -90 + 360 * clamp(k)
    cv2.ellipse(f, (int(cx), int(cy)), (int(r), int(r)), 0, -90, ang_end, C(INK), 30, cv2.LINE_AA)
    cv2.ellipse(f, (int(cx), int(cy)), (int(r), int(r)), 0, -90, ang_end, C(WHITE), 18, cv2.LINE_AA)
    a = math.radians(ang_end); hx, hy = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    tri = np.array([[hx + tx * 40, hy + ty * 40], [hx - tx * 6 + math.cos(a) * 34, hy - ty * 6 + math.sin(a) * 34],
                    [hx - tx * 6 - math.cos(a) * 34, hy - ty * 6 - math.sin(a) * 34]], np.int32)
    if k > 0.03: cv2.fillPoly(f, [tri], C(INK), cv2.LINE_AA)
    for i, s in enumerate(steps):
        q = i / n
        if k < q + 0.02: continue
        a = math.radians(-90 + 360 * q); x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        comp(f, chip(s, cols[i % len(cols)], WHITE if cols[i % len(cols)] != YEL_ else INK, 40), x, y, scale=pin(t, 0, 0.01) * (1.0 + 0.15 * math.exp(-(k - q) * 30)))


def bars(f, x, base, w, hgt, col, k=1.0, label="", val=""):
    h_ = int(hgt * eo(clamp(k)))
    cv2.rectangle(f, (int(x - w / 2) + 8, base - h_ + 8), (int(x + w / 2) + 8, base), (0, 0, 0), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), base - h_), (int(x + w / 2), base), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - w / 2), base - h_), (int(x + w / 2), base), C(INK), 6, cv2.LINE_AA)
    if label: comp(f, ed_el("", label, "", big_col=INK, big_size=40, maxw=300), x, base + 50)
    if val and k > 0.6: comp(f, ed_el("", val, "", big_col=INK, big_size=74, maxw=300), x, base - h_ - 60, op=clamp((k - 0.6) / 0.3))


def swag_el(w=320, h=340, label="THE TRICK"):
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(30, 80, w - 2, h - 2), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.ellipse(S(16, 70, w - 16, h - 16), fill=255), (150, 150, 160), (90, 90, 104))
        d.ellipse(S(16, 70, w - 16, h - 16), outline=INK + (255,), width=6 * sc)
        d.polygon(S(w / 2 - 50, 80, w / 2 + 50, 80, w / 2 + 30, 20, w / 2 - 30, 20), fill=(110, 110, 124, 255), outline=INK + (255,), width=5 * sc)
        d.rectangle(S(w / 2 - 56, 70, w / 2 + 56, 92), fill=FLAME_O + (255,), outline=INK + (255,), width=4 * sc)
        d.text((w / 2 * sc, 210 * sc), label, font=font(F_BLACK, 48 * sc), fill=(255, 255, 255, 255), anchor="mm", stroke_width=3 * sc, stroke_fill=INK + (255,))
        return _done(im, w, h)
    return gcache(("swag", w, h, label), mk)


def cap_el(w=260, h=180):
    """graduation cap"""
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.polygon(S(w / 2, 10, w - 6, 60, w / 2, 110, 6, 60), fill=INK + (255,))
        d.rectangle(S(w / 2 - 70, 80, w / 2 + 70, 150), fill=INK + (255,))
        d.line(S(w / 2, 60, w - 40, 90, w - 40, 150), fill=YEL_ + (255,), width=6 * sc)
        d.ellipse(S(w - 54, 140, w - 26, 172), fill=YEL_ + (255,))
        return _done(im, w, h)
    return gcache(("cap", w, h), mk)


def cents_grid(f, cx, cy, lit, col, cell=44, gap=8, k=1.0, dim=(255, 255, 255)):
    """10x10 grid = one dollar in cents; the first `lit` cells glow in col (k animates fill 0..1)"""
    n_on = int(round(lit * clamp(k)))
    s = cell + gap; x0 = cx - 5 * s + gap / 2; y0 = cy - 5 * s + gap / 2
    cv2.rectangle(f, (int(x0 - 24), int(y0 - 24)), (int(x0 + 10 * s + 16), int(y0 + 10 * s + 16)), C(INK), -1, cv2.LINE_AA)
    for i in range(100):
        r_, c_ = divmod(i, 10); x = int(x0 + c_ * s); y = int(y0 + (9 - r_) * s)
        on = i < n_on
        cv2.rectangle(f, (x, y), (x + cell, y + cell), C(col if on else dim), -1, cv2.LINE_AA)


def people_grid(f, cx, cy, k, lit_idx, t, r=34, cols=10, rows=10, step=78, crown_k=0.0):
    """100 mini heads; heads in lit_idx get an orange halo + gold coin once crown_k > 0"""
    x0 = cx - (cols - 1) * step / 2; y0 = cy - (rows - 1) * step / 2
    shown = int(round(cols * rows * clamp(k)))
    dim = mini_head(r, False); hi = mini_head(r, True)
    for j in range(shown):
        rr, cc = divmod(j, cols); x = x0 + cc * step; y = y0 + rr * step
        if j in lit_idx and crown_k > 0:
            cv2.circle(f, (int(x), int(y)), int(r * 1.25 * clamp(crown_k * 2)), C(FLAME_O), -1, cv2.LINE_AA)
            comp(f, hi, x, y - 6 * math.sin(t * 8 + j) * clamp(crown_k))
            comp(f, coin_el(16, abs(math.cos(t * 4 + j))), x + r * 0.9, y - r * 0.9, scale=pin(t, 0, 0.01))
        else:
            comp(f, dim, x, y, op=1.0 if crown_k <= 0 else 1.0 - 0.6 * clamp(crown_k))


def odometer(f, cx, cy, text, k=1.0, cell=(96, 150), col=YEL_, seed=0):
    """rolling digit counter drawn straight on the frame; digits settle left-to-right as k goes 0..1"""
    n_ = len(text); cw, ch = cell; gap = 10; x0 = cx - (n_ * cw + (n_ - 1) * gap) / 2
    cv2.rectangle(f, (int(x0 - 26), int(cy - ch / 2 - 26)), (int(x0 + n_ * (cw + gap) - gap + 26), int(cy + ch / 2 + 26)), C(INK), -1, cv2.LINE_AA)
    rng = np.random.default_rng(seed)
    for i, c in enumerate(text):
        x = x0 + i * (cw + gap)
        if c in ",.":
            el = ed_el("", c, "", big_col=col, big_size=110, fp_big=F_BLACK, maxw=200)
            comp(f, el, x + cw / 2, cy + 8); continue
        cv2.rectangle(f, (int(x), int(cy - ch / 2)), (int(x + cw), int(cy + ch / 2)), C((250, 248, 240)), -1, cv2.LINE_AA)
        done = k >= (i + 1) / (n_ + 1)
        d_ = c if done or not c.isdigit() else str(int(rng.integers(0, 10) + k * 97 + i * 3) % 10)
        el = ed_el("", d_, "", big_col=INK, big_size=118, fp_big=F_BLACK, maxw=200)
        comp(f, el, x + cw / 2, cy + 2)
        cv2.line(f, (int(x), int(cy)), (int(x + cw), int(cy)), C((200, 200, 205)), 2)


def smoke(f, x, y, t, t0, n=7):
    q = t - t0
    if q <= 0 or q > 1.6: return
    op = 0.55 * (1 - q / 1.6)
    for i in range(n):
        r = 14 + 30 * q + 4 * i; yy = y - 220 * q - 26 * i; xx = x + 26 * math.sin(i * 1.7 + q * 3)
        y0, y1, x0, x1 = int(yy - r), int(yy + r), int(xx - r), int(xx + r)
        if y0 < 0 or x0 < 0: continue
        m = np.zeros((y1 - y0, x1 - x0), np.float32); cv2.circle(m, (int(r), int(r)), int(r), 1.0, -1, cv2.LINE_AA)
        reg = f[y0:y1, x0:x1]; reg[:] = reg * (1 - op * m[..., None]) + np.array(C((225, 225, 232)), np.float32) * op * m[..., None]
