# ================= props for "One company behind your glasses" (generic: no real logos, no frame trade dress, no Wayfarer shapes) =================
# Brand names appear only as plain text on signs/chips (commentary). Glasses are generic shapes: round, oval, cat, sport shield, thin rect.
FR_COLS = [(22, 22, 28), (150, 40, 40), (200, 150, 60), (40, 90, 170), (230, 230, 236), (120, 70, 150), (30, 130, 90), (232, 110, 40)]
LENS_COLS = [(40, 60, 90), (90, 60, 40), (40, 90, 70), (120, 60, 110), (200, 220, 240), (60, 80, 140)]


def glasses_el(w=360, style="round", frame=(22, 22, 28), lens=(40, 60, 90), clear=False, smart=False, led=0.0):
    """generic glasses seen from the front. style: round | oval | cat | sport | rect. clear=True = optical (pale lens).
    smart=True adds a tiny camera dot + LED on the corners (AI glasses)."""
    key = ("gls", w, style, frame, lens, clear, smart, round(led, 1))
    def mk():
        sc = 2; h = int(w * 0.42); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        th = max(5, int(w * 0.035)); lw = w * 0.36; lh = h * 0.72; cy = h * 0.52
        lc = (lens + (90,)) if clear else (lens + (238,))
        hi = (255, 255, 255, 120 if clear else 150)
        def lens_shape(dd, cx, fill=None, outline=None, wd=0):
            x0, x1, y0, y1 = cx - lw / 2, cx + lw / 2, cy - lh / 2, cy + lh / 2
            if style == "round":
                r = min(lw, lh) / 2; dd.ellipse(S(cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=wd)
            elif style == "oval":
                dd.ellipse(S(x0, y0 + lh * 0.08, x1, y1 - lh * 0.04), fill=fill, outline=outline, width=wd)
            elif style == "cat":
                s = 1 if cx > w / 2 else -1
                pts = [(cx - s * lw * 0.5, cy - lh * 0.18), (cx + s * lw * 0.55, cy - lh * 0.5), (cx + s * lw * 0.45, cy + lh * 0.18),
                       (cx + s * lw * 0.1, cy + lh * 0.45), (cx - s * lw * 0.4, cy + lh * 0.3)]
                dd.polygon([v * sc for p in pts for v in p], fill=fill, outline=outline, width=wd)
            else:   # rect (thin)
                dd.rounded_rectangle(S(x0, y0 + lh * 0.12, x1, y1 - lh * 0.12), int(lh * 0.22) * sc, fill=fill, outline=outline, width=wd)
        cxs = (w * 0.27, w * 0.73)
        _ov(im, lambda q: [lens_shape(q, cx + 6, (0, 0, 0, 50)) for cx in cxs])
        if style == "sport":
            pts = [(w * 0.04, h * 0.30), (w * 0.5, h * 0.18), (w * 0.96, h * 0.30), (w * 0.92, h * 0.70), (w * 0.62, h * 0.86),
                   (w * 0.5, h * 0.62), (w * 0.38, h * 0.86), (w * 0.08, h * 0.70)]
            d.polygon([v * sc for p in pts for v in p], fill=lc)
            _ov(im, lambda q: q.polygon(S(w * 0.12, h * 0.30, w * 0.4, h * 0.24, w * 0.2, h * 0.62), fill=hi))
            d.line([v * sc for p in pts + [pts[0]] for v in p], fill=frame + (255,), width=th * sc, joint="curve")
            d.line(S(w * 0.04, h * 0.30, w * 0.5, h * 0.18, w * 0.96, h * 0.30), fill=frame + (255,), width=int(th * 1.8) * sc, joint="curve")
        else:
            for cx in cxs:
                lens_shape(d, cx, lc)
                _ov(im, lambda q, cx=cx: q.polygon(S(cx - lw * 0.3, cy - lh * 0.2, cx - lw * 0.05, cy - lh * 0.32, cx - lw * 0.22, cy + lh * 0.12), fill=hi))
                lens_shape(d, cx, None, frame + (255,), th * sc)
            d.arc(S(w * 0.43, cy - lh * 0.32, w * 0.57, cy + lh * 0.1), 200, 340, fill=frame + (255,), width=th * sc)   # bridge
            for x0, x1 in ((0, cxs[0] - lw / 2), (cxs[1] + lw / 2, w)):                                                  # temples (stubs)
                d.line(S(x0, cy - lh * 0.3, x1, cy - lh * 0.3), fill=frame + (255,), width=th * sc)
        if smart:
            for x in (w * 0.08, w * 0.92):
                d.ellipse(S(x - 7, cy - lh * 0.36 - 7, x + 7, cy - lh * 0.36 + 7), fill=(60, 64, 80, 255), outline=(200, 210, 230, 255), width=2 * sc)
            if led > 0:
                _ov(im, lambda q: q.ellipse(S(w * 0.08 - 16, cy - lh * 0.36 - 16, w * 0.08 + 16, cy - lh * 0.36 + 16), fill=(255, 255, 255, int(160 * led))))
        return _done(im, w, h)
    return gcache(key, mk)


def gl_style(i):
    sty = ["round", "oval", "cat", "sport", "rect"]
    return dict(style=sty[i % 5], frame=FR_COLS[(i * 3) % len(FR_COLS)], lens=LENS_COLS[(i * 5) % len(LENS_COLS)])


def glasses_tree(f, cx, base_y, t, k=1.0, n=13, scale=1.0, labels=None):
    """one tree trunk whose branches end in many different pairs of glasses (all from the same root). k grows it in."""
    s = scale
    trunk = (110, 70, 40); trunk_d = (80, 48, 26)
    top = base_y - 560 * s
    pts = np.array([[cx - 70 * s, base_y], [cx - 38 * s, top + 140 * s], [cx + 38 * s, top + 140 * s], [cx + 70 * s, base_y]], np.int32)
    cv2.fillPoly(f, [pts], C(trunk), cv2.LINE_AA)
    cv2.line(f, (int(cx + 14 * s), int(base_y - 20 * s)), (int(cx + 8 * s), int(top + 160 * s)), C(trunk_d), int(10 * s), cv2.LINE_AA)
    for dx in (-90, -40, 40, 90):                                                    # roots
        cv2.line(f, (int(cx), int(base_y - 10 * s)), (int(cx + dx * 1.6 * s), int(base_y + 22 * s)), C(trunk), int(22 * s), cv2.LINE_AA)
    rng = np.random.RandomState(4)
    for i in range(n):
        a = math.radians(-160 + 140 * (i / max(1, n - 1))) + rng.uniform(-0.08, 0.08)
        L = (190 + 120 * ((i * 7) % 3) / 2) * s
        kk = clamp(k * 1.6 - i * 0.05)
        if kk <= 0: continue
        x0, y0 = cx, top + 170 * s
        x1, y1 = x0 + math.cos(a) * L * kk, y0 + math.sin(a) * L * kk * 0.9
        cv2.line(f, (int(x0), int(y0)), (int(x1), int(y1)), C(trunk), int(max(6, 20 * s * (1 - 0.4 * kk))), cv2.LINE_AA)
        if kk >= 0.98:
            sw = math.sin(t * 2.2 + i * 1.3) * 7
            el = glasses_el(int(175 * s), **gl_style(i))
            cv2.line(f, (int(x1), int(y1)), (int(x1 + sw * 0.4), int(y1 + 40 * s)), C((60, 60, 60)), 2, cv2.LINE_AA)
            rot_comp(f, el, x1 + sw * 0.4, y1 + 40 * s + 28 * s, sw, pin(t, -1, 0.1) if k >= 1 else 1.0, 1.0, 0.25)
            if labels and i < len(labels) and labels[i]:
                comp(f, chip(labels[i], WHITE, INK, int(22 * s + 2)), x1, y1 + 40 * s + 80 * s)
    # leaves blobs behind (drawn after branches but light alpha)
    return f


def door_el(w=220, h=420, num=1, label="FRAME", col=(40, 110, 220), open_=0.0, glow=0.0):
    """a numbered door; open_ 0..1 swings it open revealing warm light"""
    key = ("door", w, h, num, label, col, round(open_, 2), round(glow, 2))
    def mk():
        sc = 2; im, d = _canvas(w + 40, h + 60); S = lambda *v: [x * sc for x in v]
        ox, oy = 20, 40
        d.rectangle(S(ox - 14, oy - 14, ox + w + 14, oy + h), fill=(70, 50, 40, 255))           # frame
        d.rectangle(S(ox, oy, ox + w, oy + h), fill=(255, 230, 150, 255))                          # light behind
        if glow > 0:
            _ov(im, lambda q: q.rectangle(S(ox, oy, ox + w, oy + h), fill=(255, 255, 255, int(150 * glow))))
        ww = w * (1 - 0.82 * open_)
        lo = tuple(int(v * 0.72) for v in col)
        d.polygon(S(ox, oy, ox + ww, oy + h * 0.04 * open_, ox + ww, oy + h * (1 - 0.04 * open_), ox, oy + h), fill=col + (255,), outline=INK + (255,))
        if ww > 60:
            for (a, b) in ((0.1, 0.45), (0.55, 0.92)):
                d.rectangle(S(ox + ww * 0.16, oy + h * a, ox + ww * 0.84, oy + h * b), outline=lo + (255,), width=5 * sc)
            d.ellipse(S(ox + ww * 0.82 - 10, oy + h * 0.52 - 10, ox + ww * 0.82 + 10, oy + h * 0.52 + 10), fill=GOLD + (255,), outline=INK + (255,), width=2 * sc)
            d.text(((ox + ww / 2) * sc, (oy + h * 0.27) * sc), str(num), font=font(F_BLACK, int(w * 0.38) * sc), fill=(255, 255, 255, 255), anchor="mm",
                   stroke_width=3 * sc, stroke_fill=INK + (255,))
        d.rounded_rectangle(S(ox + 6, 0, ox + w - 6, 34), 10 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=3 * sc)
        fs = int(min(26, (w - 30) / max(1, len(label)) * 1.7))
        d.text(((ox + w / 2) * sc, 17 * sc), label, font=font(F_BLACK, fs * sc), fill=INK + (255,), anchor="mm")
        return _done(im, w + 40, h + 60)
    return gcache(key, mk)


def shopfront_el(name, col=(40, 110, 220), w=330, h=520, sun=True):
    """generic mall shopfront with a plain-text name sign and a window of glasses on stands"""
    key = ("shopf", name, col, w, h, sun)
    def mk():
        sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(0, 0, w, h), fill=(236, 232, 226, 255), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(0, 0, w, h * 0.2), fill=col + (255,), outline=INK + (255,), width=3 * sc)
        fs = int(min(h * 0.09, (w - 24) / max(1, len(name)) * 1.4))
        d.text((w / 2 * sc, h * 0.1 * sc), name, font=font(F_BLACK, fs * sc), fill=(255, 255, 255, 255), anchor="mm")
        shape_grad(im, lambda m: m.rectangle(S(16, h * 0.25, w - 16, h * 0.95), fill=255), (190, 220, 240), (140, 170, 200))
        d.rectangle(S(16, h * 0.25, w - 16, h * 0.95), outline=(60, 60, 70, 255), width=4 * sc)
        for r in range(2):
            y = h * (0.45 + 0.27 * r)
            d.rectangle(S(26, y + 26, w - 26, y + 34), fill=(250, 250, 250, 255))
        return _done(im, w, h)
    el = gcache(key, mk)
    return el


def shopfront(f, name, x, y, col, w=330, h=520, t=0.0, seed=0):
    comp(f, shopfront_el(name, col, w, h), x, y)
    for r in range(2):
        for j in range(3):
            gy = y - h / 2 + h * (0.45 + 0.27 * r) + 4
            gx = x - w / 2 + w * (0.24 + 0.26 * j)
            comp(f, glasses_el(int(w * 0.22), **gl_style(seed + r * 3 + j)), gx, gy)


def lens_el(w=520, tint=(170, 210, 255), label=None):
    """big optical lens disc, side bevel, rainbow coating reflections"""
    key = ("lens", w, tint, label)
    def mk():
        sc = 2; im, d = _canvas(w, w); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.ellipse(S(18, 26, w - 2, w - 2), fill=(0, 0, 0, 60)))
        shape_grad(im, lambda m: m.ellipse(S(6, 6, w - 14, w - 14), fill=255), tuple(min(255, v + 50) for v in tint), tint)
        _ov(im, lambda q: q.ellipse(S(6, 6, w - 14, w - 14), fill=(255, 255, 255, 40)))
        d.ellipse(S(6, 6, w - 14, w - 14), outline=(90, 120, 160, 255), width=max(3, int(w * 0.02)) * sc)
        d.ellipse(S(w * 0.05, w * 0.05, w * 0.935, w * 0.935), outline=(255, 255, 255, 200), width=3 * sc)
        _ov(im, lambda q: q.arc(S(w * 0.115, w * 0.115, w * 0.865, w * 0.865), 200, 260, fill=(120, 255, 160, 150), width=max(2, int(w * 0.027)) * sc))
        _ov(im, lambda q: q.arc(S(w * 0.155, w * 0.155, w * 0.83, w * 0.83), 205, 250, fill=(200, 120, 255, 140), width=max(2, int(w * 0.02)) * sc))
        _ov(im, lambda q: q.ellipse(S(w * 0.22, w * 0.18, w * 0.4, w * 0.3), fill=(255, 255, 255, 170)))
        if label:
            d.text((w / 2 * sc, w * 0.56 * sc), label, font=font(F_BLACK, int(w * 0.09) * sc), fill=(30, 50, 90, 220), anchor="mm")
        return _done(im, w, w)
    return gcache(key, mk)


def plan_card_el(w=600, name="EyeMed", col=(30, 120, 170), col2=(60, 190, 200)):
    """generic vision-plan member card: plain-text plan name (no logo), eye glyph, member id"""
    key = ("plan", w, name, col, col2)
    def mk():
        sc = 2; h = int(w * 0.62); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(10, 14, w - 2, h - 2), 30 * sc, fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 12, h - 12), 30 * sc, fill=255), col2, col)
        d.rounded_rectangle(S(2, 2, w - 12, h - 12), 30 * sc, outline=INK + (255,), width=6 * sc)
        d.rectangle(S(2, h * 0.62, w - 12, h * 0.64), fill=(255, 255, 255, 120))
        d.text((40 * w / 600 * sc, 56 * w / 600 * sc), "VISION PLAN", font=font(F_BLACK, int(w * 0.05) * sc), fill=(255, 255, 255, 220), anchor="lm")
        d.text((40 * w / 600 * sc, h * 0.36 * sc), name, font=font(F_BLACK, int(w * (0.11 if len(name) < 8 else 0.075)) * sc), fill=(255, 255, 255, 255), anchor="lm")
        d.text((40 * w / 600 * sc, h * 0.78 * sc), "MEMBER ID  0042 7781", font=font(F_BLACK, int(w * 0.045) * sc), fill=(255, 255, 255, 230), anchor="lm")
        u = w / 600; ex, ey = w - 110 * u, h * 0.34                                        # eye glyph (scales with the card)
        d.ellipse(S(ex - 58 * u, ey - 30 * u, ex + 58 * u, ey + 30 * u), fill=(255, 255, 255, 255), outline=INK + (255,), width=max(2, int(4 * u)) * sc)
        d.ellipse(S(ex - 22 * u, ey - 22 * u, ex + 22 * u, ey + 22 * u), fill=(40, 110, 200, 255)); d.ellipse(S(ex - 9 * u, ey - 9 * u, ex + 9 * u, ey + 9 * u), fill=INK + (255,))
        return _done(im, w, h)
    return gcache(key, mk)


def rx_el(w=460, title="PRESCRIPTION"):
    """eyeglass prescription slip (generic numbers), 'FREE COPY' line"""
    key = ("rx", w, title)
    def mk():
        sc = 2; h = int(w * 1.25); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(12, 16, w - 2, h - 2), fill=(0, 0, 0, 70)))
        d.rectangle(S(2, 2, w - 12, h - 12), fill=(252, 252, 248, 255), outline=INK + (255,), width=4 * sc)
        d.rectangle(S(2, 2, w - 12, 80), fill=(40, 110, 200, 255))
        d.text((w / 2 * sc, 42 * sc), title, font=font(F_BLACK, int(w * 0.075) * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.text((40 * sc, 140 * sc), "Rx", font=font(F_BLACK, int(w * 0.14) * sc), fill=INK + (255,), anchor="lm")
        rows = (("", "SPH", "CYL", "AXIS"), ("R", "-1.25", "-0.50", "180"), ("L", "-1.00", "-0.25", "175"))
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                x = 50 + c * (w - 90) / 4 + 20; y = 230 + r * 70
                d.text((x * sc, y * sc), cell, font=font(F_BLACK if r == 0 or c == 0 else F_BOLD, int(w * 0.055) * sc), fill=INK + (255,), anchor="lm")
            d.line(S(36, 230 + r * 70 + 34, w - 46, 230 + r * 70 + 34), fill=(190, 190, 200, 255), width=2 * sc)
        d.text((40 * sc, (h - 120) * sc), "PD 63", font=font(F_BOLD, int(w * 0.05) * sc), fill=INK + (255,), anchor="lm")
        d.line(S(w * 0.45, h - 90, w - 50, h - 90), fill=INK + (255,), width=2 * sc)
        d.text(((w * 0.45) * sc, (h - 70) * sc), "signature", font=font(F_BOLD, int(w * 0.035) * sc), fill=(120, 120, 130, 255), anchor="lm")
        return _done(im, w, h)
    return gcache(key, mk)


def eyechart_el(w=420):
    key = ("eyech", w)
    def mk():
        sc = 2; h = int(w * 1.35); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rectangle(S(2, 2, w - 4, h - 4), fill=(255, 255, 255, 255), outline=(60, 60, 70, 255), width=6 * sc)
        rows = ("E", "F P", "T O Z", "L P E D", "P E C F D", "E D F C Z P")
        y = 40
        for i, r in enumerate(rows):
            s = int(w * (0.28 / (1 + i * 0.7)))
            d.text((w / 2 * sc, (y + s / 2) * sc), r, font=font(F_BLACK, s * sc), fill=INK + (255,), anchor="mm")
            y += s + 22
        d.line(S(30, y + 10, w - 30, y + 10), fill=(220, 40, 40, 255), width=3 * sc)
        return _done(im, w, h)
    return gcache(key, mk)


def hub_map(f, cx, cy, k, t, center="ONE COMPANY", spokes=(), r=330, col=YEL_):
    """network: one centre node, spokes to labelled satellites (frame/lens/shop/plan), grows with k (0..1 per spoke)"""
    n_ = len(spokes)
    for i, (lab, ic) in enumerate(spokes):
        kk = clamp(k * n_ - i)
        if kk <= 0: continue
        a = math.radians(-90 + 360 * i / n_ + 45)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        arrow(f, (cx, cy), (cx + (x1 - cx) * 0.78, cy + (y1 - cy) * 0.78), clamp(kk * 1.5), col=WHITE, th=10)
        if kk > 0.5:
            sc_ = pin(kk, 0.5, 0.4)
            cv2.circle(f, (int(x1), int(y1)), int(108 * sc_), C(WHITE), -1, cv2.LINE_AA)
            cv2.circle(f, (int(x1), int(y1)), int(108 * sc_), C(INK), 6, cv2.LINE_AA)
            if ic is not None: comp(f, ic, x1, y1 - 14, scale=0.9 * sc_)
            comp(f, chip(lab, INK, WHITE, 28), x1, y1 + 78, scale=sc_)
    cv2.circle(f, (int(cx), int(cy)), 150, C(col), -1, cv2.LINE_AA); cv2.circle(f, (int(cx), int(cy)), 150, C(INK), 8, cv2.LINE_AA)
    sparkle(f, cx + 120, cy - 120, 26, t)
    lines = center.split("\n")
    for j, ln in enumerate(lines):
        comp(f, ed_el(ln, "", lead_col=INK, lead_size=40), cx, cy + (j - (len(lines) - 1) / 2) * 50)


# ---------- full-frame sets: mall corridor + optician's exam room ----------
_old_set_base = _set_base


def _set_base(name):
    if name == "mall":
        f = np.zeros((H, W, 3), np.float32)
        _srect(f, 0, 0, W, 300, (250, 248, 244), (230, 226, 220))                       # ceiling
        for x in range(60, W, 240): _sglow(f, x, 150, 90, (255, 250, 230), 0.8)
        _srect(f, 0, 300, W, 1260, (236, 226, 214), (214, 202, 190))                     # back wall
        _srect(f, 0, 1180, W, 1260, (200, 190, 180), (170, 160, 150), (90, 80, 70), 2)
        f[1260:] = 0; _sfloor(f, 1260, 540, (246, 242, 236), (210, 204, 196), line_col=(190, 184, 176))
        _sglow(f, 540, 700, 800, (255, 240, 220), 0.15)
        _atmos(f, "store")
        return np.clip(f, 0, 1).astype(np.float32)
    if name == "optician":
        f = np.zeros((H, W, 3), np.float32)
        _srect(f, 0, 0, W, 1250, (214, 236, 240), (186, 214, 222))                       # mint clinic wall
        for y in range(80, 1250, 120): cv2.line(f, (0, y), (W, y), _scv((200, 226, 230)), 3, cv2.LINE_AA)
        _srect(f, 640, 220, 1000, 760, (255, 255, 255), (240, 240, 240), (60, 60, 70), 4)   # eye chart frame
        comp(f, eyechart_el(330), 820, 490)
        _srect(f, 60, 300, 420, 1000, (250, 250, 252), (226, 228, 232), (80, 80, 90), 3)    # display wall of frames
        for j in range(5):
            _srect(f, 80, 380 + j * 125, 400, 392 + j * 125, (210, 210, 214), (180, 180, 186))
        f[1250:] = 0; _sfloor(f, 1250, 540, (222, 226, 232), (186, 190, 200), line_col=(170, 174, 184))
        _sglow(f, 540, 300, 700, (240, 250, 255), 0.25)
        _atmos(f, "office")
        return np.clip(f, 0, 1).astype(np.float32)
    return _old_set_base(name)


SET_LIGHT.update(mall="day", optician="cool")


def optician_dressing(f, t):
    """frames on the display wall of the optician set (drawn per frame so they stay crisp)"""
    for j in range(5):
        for q in range(2):
            comp(f, glasses_el(130, **gl_style(j * 2 + q), clear=True), 160 + q * 160, 350 + j * 125)


def mall_dressing(f, t, names=(("SUNGLASS HUT", (232, 60, 40)), ("LENSCRAFTERS", (40, 110, 220)), ("TARGET OPTICAL", (200, 30, 50))),
                  y=860, w=320, h=500, cam_x=0.0):
    for i, (nm, col) in enumerate(names):
        shopfront(f, nm, 190 + 350 * i + cam_x, y, col, w, h, t, seed=i * 5)


def stock_crash(f, x0, y0, x1, y1, k, t):
    pts = [(0.0, 0.62), (0.1, 0.6), (0.2, 0.66), (0.3, 0.63), (0.42, 0.68), (0.5, 0.66), (0.6, 0.7), (0.7, 0.68), (0.74, 0.69), (0.78, 0.25), (0.88, 0.27), (1.0, 0.24)]
    line_chart(f, x0, y0, x1, y1, pts, k, col=RED_, th=12)
