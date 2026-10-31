# ================= story kit 2 (exec'd after anim_story.py) — SPOT THE TRICK store world: sets + props for the flat-pack maze episode =================
# R&D Visuals run, 31 Oct 2026 (episodes/queue/03-ikea-maze BUILD BRIEF). Generic by design: no logos, no blue/yellow trade dress,
# plain cardboard, grey floor arrows, birch-coloured furniture. Everything is lit by the same set_light() as the cast.
# Sets (set_view): maze_store (one-way showroom path, far EXIT sign at the end), market_hall (tall racks + cardboard bins),
#   store_cafe (canteen: windows, counter, menu board, long tables). Floors: 1180 / 1200 / 1200.
# Props: bin_el(item="candles"|"cushions"|"plants"|"mugs") cardboard tub piled with one cheap thing; arrow_floor(f, x, y, s, ang) grey
#   floor arrow decal (draws on the frame, perspective-flattened); flatpack_el(built=0..1) flat box -> wobbly shelf; tray_el() canteen
#   tray (meatballs, mash, jam); shortcut_door_el(open_=0..1) plain grey staff door with a small SHORTCUT sign; exit_sign_el(mirror=)
#   green EXIT sign; list_el("LAMP") paper shopping list; turnstile_el() entrance gate; heart_el() popping heart (d2 row).


def _kraft(k=1.0):   # cardboard browns
    return tuple(int(v * k) for v in (198, 152, 98))


# ---------------- props ----------------
def bin_el(item="candles", w=620, label=None, seed=3):
    """big cardboard tub ('bulla bulla') overflowing with one cheap item; label = optional plain text on the front card"""
    def mk():
        sc = 2; h = int(w * 0.92); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed)
        top, bot = 0.30 * h, h - 10
        # tub body (slightly wider at the top), with a corrugated rim and two side flaps
        shape_grad(im, lambda m: m.polygon(S(30, top, w - 30, top, w - 70, bot, 70, bot), fill=255), _kraft(1.05), _kraft(0.72))
        d.polygon(S(30, top, w - 30, top, w - 70, bot, 70, bot), outline=INK + (255,), width=4 * sc)
        for k in range(3): d.line(S(70 + k * 6, bot - 8, 30 + k * 6, top + 8), fill=(150, 108, 62, 120), width=3 * sc)
        d.rectangle(S(30, top - 14, w - 30, top + 22), fill=_kraft(0.9) + (255,), outline=INK + (255,), width=4 * sc)     # rim
        for x in range(40, w - 40, 14): d.line(S(x, top - 12, x, top + 20), fill=(150, 108, 62, 110), width=2 * sc)      # corrugation
        # front card (plain, no price)
        cw, ch = w * 0.42, h * 0.2; cx0, cy0 = (w - cw) / 2, top + h * 0.22
        d.rounded_rectangle(S(cx0, cy0, cx0 + cw, cy0 + ch), 12 * sc, fill=(252, 250, 244, 255), outline=INK + (255,), width=3 * sc)
        if label:
            fs = int(min(ch * 0.5, cw / max(1, len(label)) * 1.5))
            d.text(((cx0 + cw / 2) * sc, (cy0 + ch / 2) * sc), label, font=font(F_BLACK, fs * sc), fill=INK + (255,), anchor="mm")
        else:
            for k in range(2): d.line(S(cx0 + 24, cy0 + ch * (0.38 + 0.3 * k), cx0 + cw - 24, cy0 + ch * (0.38 + 0.3 * k)), fill=(120, 120, 130, 255), width=4 * sc)
        # the pile: items above the rim, back rows first (drawn behind the rim: paste a layer under the tub? simpler: draw rows then the rim line again)
        L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(L_)
        n_rows = 5
        for r in range(n_rows):
            yc = top - 10 - r * h * 0.075; spread = (w - 120) * (1 - 0.14 * r)
            n = int(10 - r * 1.5)
            for i in range(n):
                x = w / 2 - spread / 2 + spread * (i + 0.5) / n + rng.uniform(-10, 10); y = yc + rng.uniform(-8, 8)
                if item == "candles":
                    cw_, chh = w * 0.075, h * 0.19
                    cc = [(250, 246, 236), (246, 226, 200), (236, 238, 230)][int(rng.integers(0, 3))]
                    q.rounded_rectangle(S(x - cw_ / 2, y - chh, x + cw_ / 2, y), 8 * sc, fill=cc + (255,), outline=INK + (255,), width=2 * sc)
                    q.rounded_rectangle(S(x + cw_ * 0.1, y - chh + 6, x + cw_ / 2 - 3, y - 6), 6 * sc, fill=tuple(int(v * 0.86) for v in cc) + (255,))   # shade
                    q.ellipse(S(x - cw_ / 2, y - chh - 6, x + cw_ / 2, y - chh + 8), fill=(228, 222, 204, 255), outline=INK + (255,), width=2 * sc)
                    q.line(S(x, y - chh, x + 2, y - chh - 18), fill=(40, 30, 24, 255), width=3 * sc)
                elif item == "cushions":
                    c = [(226, 90, 70), (70, 150, 150), (240, 190, 70), (120, 100, 170)][int(rng.integers(0, 4))]
                    q.rounded_rectangle(S(x - w * 0.07, y - h * 0.12, x + w * 0.07, y), 14 * sc, fill=c + (255,), outline=INK + (255,), width=2 * sc)
                elif item == "plants":
                    for a in (-50, -20, 10, 40):
                        q.ellipse(S(x + a * 0.4 - 14, y - h * 0.16 + abs(a) * 0.3, x + a * 0.4 + 14, y - 10), fill=(60, 150, 80, 255), outline=(30, 90, 50, 255), width=2 * sc)
                    q.rounded_rectangle(S(x - w * 0.045, y - h * 0.07, x + w * 0.045, y), 6 * sc, fill=(200, 120, 90, 255), outline=INK + (255,), width=2 * sc)
                else:   # mugs
                    q.rounded_rectangle(S(x - w * 0.05, y - h * 0.11, x + w * 0.05, y), 10 * sc, fill=(240, 240, 236, 255), outline=INK + (255,), width=2 * sc)
                    q.arc(S(x + w * 0.04, y - h * 0.09, x + w * 0.085, y - h * 0.03), 270, 90, fill=INK + (255,), width=3 * sc)
        # keep the pile behind the rim: cut the layer where the tub rim is, then composite
        cut = Image.new("L", L_.size, 255); ImageDraw.Draw(cut).rectangle(S(30, top - 14, w - 30, h), fill=0)
        L_.putalpha(Image.fromarray(np.minimum(np.asarray(L_.getchannel("A")), np.asarray(cut))))
        im.alpha_composite(L_)
        # a few items spilling over the front rim
        for i in range(3):
            x = w * (0.3 + 0.2 * i) + rng.uniform(-14, 14); y = top + 16
            if item == "candles":
                d.rounded_rectangle(S(x - w * 0.09, y - h * 0.035, x + w * 0.09, y + h * 0.035), 8 * sc, fill=(250, 246, 236, 255), outline=INK + (255,), width=2 * sc)
            else:
                d.ellipse(S(x - 18, y - 14, x + 18, y + 14), fill=(220, 200, 170, 255), outline=INK + (255,), width=2 * sc)
        return _done(im, w, h)
    return gcache(("bin", item, w, label, seed), mk)


def arrow_floor(f, x, y, s=1.0, ang=90.0, col=(118, 120, 128), op=0.9, squash=0.42):
    """grey floor arrow decal in perspective; (x, y) = centre on the floor, ang 90 = pointing down (towards the camera), -90 = away"""
    pts = np.array([(-40, -110), (40, -110), (40, 20), (90, 20), (0, 120), (-90, 20), (-40, 20)], np.float32)
    ca, sa = math.cos(math.radians(ang - 90)), math.sin(math.radians(ang - 90))
    P = np.stack([pts[:, 0] * ca - pts[:, 1] * sa, pts[:, 0] * sa + pts[:, 1] * ca], 1) * s
    P[:, 1] *= squash; P[:, 0] += x; P[:, 1] += y
    ov = np.zeros((H, W), np.float32); cv2.fillPoly(ov, [np.round(P * 4).astype(np.int32)], 1.0, cv2.LINE_AA, shift=2)
    ov = cv2.GaussianBlur(ov, (0, 0), 0.8) * op
    f[:] = f * (1 - ov[..., None]) + _c(col) * ov[..., None]


def flatpack_el(built=0.0, w=520, wobble=6.0):
    """flat cardboard box (built=0) -> a slightly wobbly birch shelf (built=1); in between the box sinks away and the shelf rises plank by plank"""
    k = round(float(clamp(built)), 2)
    def mk():
        sc = 2; h = int(w * 1.1); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        # the box: lying flat, label on top, sinks + fades as k grows
        if k < 1.0:
            bk = 1 - k; by = h - 120 + 60 * k; bw = w * 0.92; dp = 56
            L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(L_)
            q.polygon(S(w / 2 - bw / 2 + 40, by - dp, w / 2 + bw / 2 + 40, by - dp, w / 2 + bw / 2, by, w / 2 - bw / 2, by), fill=_kraft(1.08) + (255,), outline=INK + (255,))   # top face
            q.rectangle(S(w / 2 - bw / 2, by, w / 2 + bw / 2, by + 70), fill=_kraft(0.82) + (255,), outline=INK + (255,), width=3 * sc)             # front face
            q.polygon(S(w / 2 + bw / 2, by, w / 2 + bw / 2 + 40, by - dp, w / 2 + bw / 2 + 40, by + 14, w / 2 + bw / 2, by + 70), fill=_kraft(0.66) + (255,), outline=INK + (255,))   # side
            q.rounded_rectangle(S(w / 2 - 110, by + 14, w / 2 + 110, by + 56), 6 * sc, fill=(250, 248, 240, 255), outline=INK + (255,), width=2 * sc)
            q.text((w / 2 * sc, (by + 35) * sc), "SHELF · 1 BOX", font=font(F_BLACK, 18 * sc), fill=INK + (255,), anchor="mm")
            for xx in (w / 2 - bw / 2 + 60, w / 2 + bw / 2 - 60): q.line(S(xx, by + 2, xx, by + 68), fill=(150, 108, 62, 200), width=3 * sc)   # tape lines
            L_.putalpha(Image.fromarray((np.asarray(L_.getchannel("A")) * bk).astype(np.uint8)))
            im.alpha_composite(L_)
        if k > 0.0:
            # the shelf: two uprights + 3 planks, tilted by wobble*k degrees, drawn on its own layer then rotated
            sh_w, sh_h = w * 0.7, h * 0.78 * (0.6 + 0.4 * eo(k))
            L_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(L_)
            x0, x1 = w / 2 - sh_w / 2, w / 2 + sh_w / 2; yb = h - 70; yt = yb - sh_h
            birch, edge = (226, 200, 150), (176, 146, 96)
            for xx in (x0, x1 - 28): q.rectangle(S(xx, yt, xx + 28, yb), fill=birch + (255,), outline=INK + (255,), width=3 * sc)
            n_pl = 3; shown = int(round(k * n_pl + 0.49)) if k < 1 else n_pl
            for i in range(n_pl):
                if i >= shown: break
                yy = yt + 10 + (sh_h - 20) * i / (n_pl - 1) - (14 if i == n_pl - 1 else 0)
                q.rectangle(S(x0 + 6, yy, x1 - 6, yy + 22), fill=birch + (255,), outline=INK + (255,), width=3 * sc)
                q.line(S(x0 + 6, yy + 22, x1 - 6, yy + 22), fill=edge + (255,), width=5 * sc)
            # a plain lamp + a book on the shelf once it is built
            if k >= 0.99:
                q.rounded_rectangle(S(x0 + 60, yt - 46, x0 + 130, yt + 12), 8 * sc, fill=(240, 120, 80, 255), outline=INK + (255,), width=2 * sc)
                q.rectangle(S(x1 - 120, yt + 40, x1 - 60, yt + 10 + (sh_h - 20) * 0.5 - 2), fill=(70, 110, 170, 255), outline=INK + (255,), width=2 * sc)
            # a lonely leftover screw (the universal flat-pack truth)
            q.ellipse(S(x1 + 20, yb - 6, x1 + 34, yb + 8), fill=(130, 130, 140, 255), outline=INK + (255,), width=2 * sc)
            L_ = L_.rotate(-wobble * eo(k), resample=Image.BICUBIC, center=(w / 2 * sc, yb * sc))
            im.alpha_composite(L_)
        return _done(im, w, h)
    return gcache(("flatpack", k, w, wobble), mk)


def tray_el(w=560):
    """canteen tray: plate of meatballs with mash and a red jam blob, a glass, a fork — no brand, no price"""
    def mk():
        sc = 2; h = int(w * 0.62); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        shape_grad(im, lambda m: m.rounded_rectangle(S(6, h * 0.3, w - 6, h - 6), 22 * sc, fill=255), (126, 64, 54), (84, 40, 34))
        d.rounded_rectangle(S(6, h * 0.3, w - 6, h - 6), 22 * sc, outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(26, h * 0.36, w - 26, h - 24), 16 * sc, outline=(160, 90, 76, 255), width=3 * sc)
        # plate
        px, py, pr = w * 0.42, h * 0.62, w * 0.25
        d.ellipse(S(px - pr, py - pr * 0.5, px + pr, py + pr * 0.5), fill=(250, 250, 246, 255), outline=(190, 190, 186, 255), width=3 * sc)
        d.ellipse(S(px - pr * 0.84, py - pr * 0.4, px + pr * 0.84, py + pr * 0.4), outline=(220, 220, 216, 255), width=2 * sc)
        # mash (cream blob) + jam (red blob)
        d.ellipse(S(px - pr * 0.75, py - pr * 0.24, px - pr * 0.1, py + pr * 0.22), fill=(246, 230, 190, 255), outline=(200, 180, 140, 255), width=2 * sc)
        d.ellipse(S(px + pr * 0.35, py + pr * 0.02, px + pr * 0.72, py + pr * 0.3), fill=(176, 28, 60, 255), outline=(120, 20, 40, 255), width=2 * sc)
        # meatballs
        rng = np.random.default_rng(5)
        for (mx, my) in ((px - 0.02 * pr, py - 0.2 * pr), (px + 0.3 * pr, py - 0.22 * pr), (px + 0.1 * pr, py + 0.05 * pr), (px + 0.42 * pr, py - 0.02 * pr), (px - 0.25 * pr, py + 0.12 * pr)):
            r = pr * 0.13 * rng.uniform(0.9, 1.1)
            shape_grad(im, lambda m, mx=mx, my=my, r=r: m.ellipse(S(mx - r, my - r, mx + r, my + r), fill=255), (150, 92, 60), (92, 48, 30))
            d.ellipse(S(mx - r * 0.45, my - r * 0.55, mx - r * 0.1, my - r * 0.2), fill=(210, 160, 120, 200))
        # glass + fork
        gx = w * 0.84
        d.rounded_rectangle(S(gx - 36, h * 0.12, gx + 36, h * 0.6), 8 * sc, fill=(220, 236, 246, 200), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(gx - 30, h * 0.3, gx + 30, h * 0.58), fill=(180, 60, 60, 160))
        fx = w * 0.12
        d.rectangle(S(fx - 5, h * 0.4, fx + 5, h * 0.92), fill=(200, 204, 210, 255), outline=INK + (255,), width=2 * sc)
        for a in (-16, -5, 6, 17): d.line(S(fx + a, h * 0.42, fx + a, h * 0.3), fill=(200, 204, 210, 255), width=5 * sc)
        d.line(S(fx - 18, h * 0.42, fx + 20, h * 0.42), fill=(200, 204, 210, 255), width=6 * sc)
        return _done(im, w, h)
    return gcache(("tray", w), mk)


def shortcut_door_el(open_=0.0, w=260, h=460, sign="SHORTCUT"):
    """plain grey staff door in a dark frame with a small white SHORTCUT sign; open_ 0..1 swings it open onto warm light"""
    key = ("scdoor", round(open_, 2), w, h, sign)
    def mk():
        sc = 2; im, d = _canvas(w + 40, h + 70); S = lambda *v: [x * sc for x in v]
        ox, oy = 20, 50
        d.rectangle(S(ox - 14, oy - 14, ox + w + 14, oy + h), fill=(64, 66, 72, 255))
        d.rectangle(S(ox, oy, ox + w, oy + h), fill=(255, 232, 170, 255))
        if open_ > 0: _ov(im, lambda q: q.rectangle(S(ox, oy, ox + w, oy + h), fill=(255, 255, 255, int(120 * open_))))
        ww = w * (1 - 0.82 * open_); grey, dark = (176, 178, 184), (120, 122, 130)
        d.polygon(S(ox, oy, ox + ww, oy + h * 0.04 * open_, ox + ww, oy + h * (1 - 0.04 * open_), ox, oy + h), fill=grey + (255,), outline=INK + (255,))
        if ww > 60:
            d.rectangle(S(ox + ww * 0.12, oy + h * 0.1, ox + ww * 0.88, oy + h * 0.42), outline=dark + (255,), width=4 * sc)      # panel
            d.rounded_rectangle(S(ox + ww * 0.1, oy + h * 0.55, ox + ww * 0.9, oy + h * 0.6), 6 * sc, fill=(210, 212, 216, 255), outline=INK + (255,), width=2 * sc)  # push bar
            d.rectangle(S(ox + ww * 0.3, oy + h * 0.68, ox + ww * 0.7, oy + h * 0.74), fill=(230, 230, 232, 255), outline=INK + (255,), width=2 * sc)  # kick plate line
            d.text(((ox + ww / 2) * sc, (oy + h * 0.25) * sc), "STAFF", font=font(F_BLACK, int(min(30, ww * 0.16)) * sc), fill=(90, 92, 98, 255), anchor="mm")
        d.rounded_rectangle(S(ox + 10, 0, ox + w - 10, 40), 8 * sc, fill=(255, 255, 255, 255), outline=INK + (255,), width=3 * sc)
        fs = int(min(26, (w - 60) / max(1, len(sign)) * 1.7))
        d.text(((ox + w / 2 - 12) * sc, 20 * sc), sign, font=font(F_BLACK, fs * sc), fill=INK + (255,), anchor="mm")
        d.polygon(S(ox + w - 42, 12, ox + w - 22, 20, ox + w - 42, 28), fill=(36, 150, 80, 255))
        return _done(im, w + 40, h + 70)
    return gcache(key, mk)


def exit_sign_el(w=240, mirror=False, col=(32, 150, 78)):
    """green EXIT sign with a running-man-free arrow; mirror=True = seen from behind (reversed letters)"""
    def mk():
        sc = 2; h = int(w * 0.42); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(0, 0, w, h), 10 * sc, fill=col + (255,), outline=(255, 255, 255, 255), width=4 * sc)
        d.text((w * 0.42 * sc, h / 2 * sc), "EXIT", font=font(F_ANTON, int(h * 0.72) * sc), fill=(255, 255, 255, 255), anchor="mm")
        d.polygon(S(w * 0.72, h * 0.32, w * 0.9, h * 0.5, w * 0.72, h * 0.68), fill=(255, 255, 255, 255))
        if mirror: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        return _done(im, w, h)
    return gcache(("exit", w, mirror, col), mk)


def list_el(text="LAMP", w=220, ticked=False, extra=0):
    """a small paper shopping list: one item written, the rest empty lines (extra = items added later, drawn as scribbles)"""
    def mk():
        sc = 2; h = int(w * 1.25); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rounded_rectangle(S(8, 10, w, h), 6 * sc, fill=(0, 0, 0, 70)))
        d.rounded_rectangle(S(0, 0, w - 8, h - 10), 6 * sc, fill=(252, 250, 242, 255), outline=INK + (255,), width=3 * sc)
        d.rectangle(S(0, 0, w - 8, 36), fill=(236, 226, 196, 255))
        d.text(((w - 8) / 2 * sc, 18 * sc), "LIST", font=font(F_BLACK, 20 * sc), fill=INK + (255,), anchor="mm")
        for i in range(5):
            y = 70 + i * 40
            d.line(S(18, y + 14, w - 26, y + 14), fill=(200, 196, 186, 255), width=2 * sc)
            if i == 0:
                d.rectangle(S(18, y - 8, 38, y + 12), outline=INK + (255,), width=3 * sc)
                if ticked: d.line(S(21, y + 2, 27, y + 10, 37, y - 6), fill=(36, 150, 80, 255), width=4 * sc, joint="curve")
                d.text((46 * sc, y * sc), text, font=font(F_SEMI, 24 * sc), fill=INK + (255,), anchor="lm")
            elif i <= extra:
                d.line(S(46, y + 2, w - 40, y + 2), fill=(200, 60, 60, 255), width=4 * sc)
        return _done(im, w, h)
    return gcache(("list", text, w, ticked, extra), mk)


def turnstile_el(w=420):
    """entrance turnstile: two steel posts, a three-arm tripod, a small green arrow light"""
    def mk():
        sc = 2; h = int(w * 0.9); im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        steel, dark = (190, 196, 204), (110, 116, 126)
        for x in (30, w - 90):
            shape_grad(im, lambda m, x=x: m.rounded_rectangle(S(x, h * 0.25, x + 60, h - 10), 14 * sc, fill=255), steel, dark)
            d.rounded_rectangle(S(x, h * 0.25, x + 60, h - 10), 14 * sc, outline=INK + (255,), width=3 * sc)
        cx, cy = w / 2, h * 0.5
        for a in (0, 120, 240):
            ex, ey = cx + math.cos(math.radians(a)) * w * 0.3, cy + math.sin(math.radians(a)) * w * 0.12
            d.line(S(cx, cy, ex, ey), fill=steel + (255,), width=14 * sc); d.line(S(cx, cy, ex, ey), fill=INK + (255,), width=3 * sc)
            d.ellipse(S(ex - 12, ey - 12, ex + 12, ey + 12), fill=steel + (255,), outline=INK + (255,), width=2 * sc)
        d.ellipse(S(cx - 26, cy - 26, cx + 26, cy + 26), fill=dark + (255,), outline=INK + (255,), width=3 * sc)
        d.rounded_rectangle(S(w - 84, h * 0.3, w - 36, h * 0.38), 6 * sc, fill=(30, 36, 40, 255))
        d.polygon(S(w - 72, h * 0.315, w - 48, h * 0.34, w - 72, h * 0.365), fill=(60, 230, 120, 255))
        return _done(im, w, h)
    return gcache(("turnstile", w), mk)


def heart_el(w=160, col=(236, 60, 90), cracked=False):
    """popping heart (the 'you still love it' beat); cracked=True draws a zig-zag split"""
    def mk():
        sc = 2; h = w; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        r = w * 0.27
        d.ellipse(S(w * 0.5 - r * 1.85, h * 0.12, w * 0.5 - r * 1.85 + 2 * r, h * 0.12 + 2 * r), fill=col + (255,))
        d.ellipse(S(w * 0.5 - r * 0.15, h * 0.12, w * 0.5 - r * 0.15 + 2 * r, h * 0.12 + 2 * r), fill=col + (255,))
        d.polygon(S(w * 0.5 - r * 1.85 + r * 0.12, h * 0.12 + r * 1.3, w * 0.5 + r * 1.85 - r * 0.12, h * 0.12 + r * 1.3, w * 0.5, h * 0.92), fill=col + (255,))
        d.ellipse(S(w * 0.3, h * 0.2, w * 0.42, h * 0.3), fill=(255, 255, 255, 170))
        if cracked:
            d.line([(x * sc, y * sc) for x, y in ((w * 0.5, h * 0.14), (w * 0.44, h * 0.34), (w * 0.56, h * 0.5), (w * 0.46, h * 0.68), (w * 0.52, h * 0.9))], fill=(40, 10, 20, 255), width=5 * sc, joint="curve")
        return _done(im, w, h)
    return gcache(("heart", w, col, cracked), mk)


# ---------------- sets ----------------
def _strip_lights(f, y, n=5, w_=140, col=(255, 252, 240)):
    for i in range(n):
        x = int(W * (i + 0.5) / n)
        cv2.rectangle(f, (x - w_ // 2, y - 8), (x + w_ // 2, y + 8), _scv(col), -1, cv2.LINE_AA)
        _sglow(f, x, y + 10, 160, col, 0.22)


def _alcove(f, x0, x1, y0, y1, wall, floorc):
    """a room-set alcove: back wall panel + a low floor strip, inside the showroom path"""
    _srect(f, x0, y0, x1, y1, wall, tuple(int(v * 0.86) for v in wall), (120, 116, 110), 2)
    _srect(f, x0, y1 - 40, x1, y1, floorc, tuple(int(v * 0.8) for v in floorc))


def _maze_store():
    f = np.zeros((H, W, 3), np.float32); y0 = 1180
    _srect(f, 0, 0, W, y0, (244, 242, 236), (226, 224, 216))                                  # pale walls
    _srect(f, 0, 0, W, 240, (96, 98, 104), (72, 74, 80))                                      # open ceiling (dark, with lights)
    _strip_lights(f, 150, n=4)
    # the far end of the one-way path: a narrowing corridor, lighter, with the EXIT sign small at its end
    _srect(f, 300, 560, 780, y0, (236, 234, 228), (220, 218, 210))
    _srect(f, 380, 700, 700, y0, (228, 226, 220), (214, 212, 204))
    _srect(f, 440, 800, 640, y0, (238, 236, 230), (224, 222, 214))
    comp(f, exit_sign_el(120), 540, 720)
    # left alcove: living room set (teal sofa, rug, framed picture, floor lamp)
    _alcove(f, 0, 300, 420, y0, (228, 214, 196), (186, 150, 110))
    _srect(f, 50, 470, 230, 650, (246, 240, 230), (226, 220, 206), (100, 90, 80), 2)           # picture frame
    cv2.circle(f, (140, 560), 46, _scv((110, 160, 150)), -1, cv2.LINE_AA)
    _srect(f, 20, 900, 290, 1080, (66, 140, 140), (42, 100, 104), (30, 60, 60), 3)               # sofa body
    _srect(f, 20, 840, 290, 910, (76, 156, 154), (56, 120, 120), (30, 60, 60), 2)               # sofa back
    for x in (40, 150): _srect(f, x, 920, x + 110, 1000, (90, 170, 166), (66, 140, 140), (30, 60, 60), 2)   # cushions
    _srect(f, 20, 1080, 290, y0, (196, 110, 80), (160, 86, 60))                                 # rug
    cv2.line(f, (262, 760), (262, 900), _scv((60, 60, 66)), 6, cv2.LINE_AA); cv2.ellipse(f, (262, 740), (46, 30), 0, 0, 360, _scv((246, 236, 200)), -1, cv2.LINE_AA)   # floor lamp
    _sglow(f, 262, 760, 160, (255, 230, 170), 0.3)
    # right alcove: kitchen set (birch cabinets, counter, plant, hanging pans)
    _alcove(f, 780, W, 420, y0, (230, 226, 216), (210, 206, 196))
    for x in range(800, W, 100): _srect(f, x, 470, x + 90, 640, (226, 200, 150), (196, 166, 116), (120, 96, 60), 2)   # wall cabinets
    _srect(f, 790, 820, W, 860, (236, 236, 232), (206, 206, 200), (110, 110, 110), 2)             # counter top
    for x in range(800, W, 100): _srect(f, x, 860, x + 90, 1080, (226, 200, 150), (196, 166, 116), (120, 96, 60), 2)   # base cabinets
    cv2.circle(f, (900, 790), 30, _scv((60, 150, 80)), -1, cv2.LINE_AA); cv2.circle(f, (930, 780), 24, _scv((80, 170, 96)), -1, cv2.LINE_AA)
    _srect(f, 880, 800, 950, 822, (200, 120, 90), (160, 90, 70), (80, 40, 30), 2)                # plant pot
    for x in (990, 1050): cv2.circle(f, (x, 720), 26, _scv((140, 144, 150)), 6, cv2.LINE_AA); cv2.line(f, (x, 694), (x, 660), _scv((120, 122, 128)), 4, cv2.LINE_AA)   # pans
    # low half-walls that make the alcoves read as room sets
    _srect(f, 0, 1080, 320, 1110, (238, 236, 230), (214, 212, 206), (120, 118, 112), 2)
    _srect(f, 760, 1080, W, 1110, (238, 236, 230), (214, 212, 206), (120, 118, 112), 2)
    # floor: pale grey, no tiles, with the one-way arrows coming towards the camera
    f[y0:] = 0; _sfloor(f, y0, 540, (222, 222, 218), (176, 176, 172), tile=False, n_lines=9, line_col=(190, 190, 186))
    # the one-way path: a dashed grey line that snakes left and right through the showroom, arrows on it coming towards the camera
    path = [(540, 1185), (300, 1240), (760, 1330), (320, 1470), (560, 1600), (540, 1900)]
    for (a, b) in zip(path, path[1:]):
        n = 7
        for i in range(n):
            k0, k1 = i / n, (i + 0.55) / n
            p0 = (int(a[0] + (b[0] - a[0]) * k0), int(a[1] + (b[1] - a[1]) * k0)); p1 = (int(a[0] + (b[0] - a[0]) * k1), int(a[1] + (b[1] - a[1]) * k1))
            cv2.line(f, p0, p1, _scv((176, 178, 184)), int(6 + 10 * (p0[1] - 1180) / 740), cv2.LINE_AA)
    for (x, y, s, ang) in ((420, 1215, 0.45, 160), (530, 1290, 0.6, 20), (540, 1400, 0.85, 160), (440, 1540, 1.1, 30), (550, 1760, 1.6, 90)):
        arrow_floor(f, x, y, s, ang, (118, 120, 128), 0.9)
    _sglow(f, 540, 600, 700, (255, 250, 236), 0.16)
    _atmos(f, "maze_store")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


def _market_hall():
    f = np.zeros((H, W, 3), np.float32); y0 = 1200
    _srect(f, 0, 0, W, y0, (204, 206, 210), (180, 182, 188))                                    # concrete back wall
    _srect(f, 0, 0, W, 330, (58, 60, 66), (44, 46, 52))                                          # high dark ceiling
    for x in range(-40, W + 40, 220): cv2.line(f, (x, 0), (x + 60, 330), _scv((70, 72, 80)), 10, cv2.LINE_AA)    # roof trusses
    _strip_lights(f, 300, n=5, w_=120)
    # plain sign on the back wall
    _srect(f, 300, 400, 780, 480, (36, 38, 44), (24, 26, 30), (90, 90, 96), 2)
    fs = font(F_ANTON, 50); im = Image.new("L", (480, 80), 0); ImageDraw.Draw(im).text((240, 40), "SELF-SERVE", font=fs, fill=255, anchor="mm")
    m = np.asarray(im, np.float32) / 255; f[400:480, 300:780] = f[400:480, 300:780] * (1 - m[..., None]) + _c((246, 244, 236)) * m[..., None]
    # tall racks left and right: steel uprights + 4 levels of cardboard boxes
    r = _rng(11)
    for (sx0, sx1) in ((-60, 330), (750, 1140)):
        for x in (sx0 + 10, sx1 - 24): _srect(f, x, 340, x + 16, y0, (96, 102, 118), (60, 64, 76), (30, 30, 36), 2)
        for k, yb in enumerate(range(560, y0 + 1, 210)):
            _srect(f, sx0, yb, sx1, yb + 18, (120, 126, 140), (80, 84, 96), (30, 30, 36), 2)             # beam
            x = sx0 + 30
            while x < sx1 - 60:
                bw = int(r.integers(70, 150)); bh = int(r.integers(90, 170))
                if x + bw > sx1 - 30: break
                kk = 0.9 + 0.2 * r.random()
                _srect(f, x, yb - bh, x + bw, yb, _kraft(kk * 1.05), _kraft(kk * 0.78), (70, 50, 30), 2)
                cv2.rectangle(f, (x + 10, yb - bh + 10), (x + min(bw - 10, 60), yb - bh + 28), _scv((248, 246, 240)), -1, cv2.LINE_AA)   # white label
                x += bw + int(r.integers(4, 16))
    # a pallet of boxes at the back centre
    _srect(f, 400, 1040, 680, 1080, (170, 130, 80), (120, 90, 54), (60, 40, 20), 2)
    for (x, bw) in ((410, 120), (545, 125)): _srect(f, x, 950, x + bw, 1040, _kraft(1.0), _kraft(0.76), (70, 50, 30), 2)
    # floor: polished concrete with faint lines
    f[y0:] = 0; _sfloor(f, y0, 540, (170, 172, 178), (112, 114, 122), tile=False, n_lines=9, line_col=(140, 142, 150))
    _sglow(f, 540, 700, 720, (255, 252, 240), 0.14)
    _atmos(f, "market_hall")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


def _store_cafe():
    f = np.zeros((H, W, 3), np.float32); y0 = 1200
    _srect(f, 0, 0, W, y0, (238, 236, 228), (222, 218, 208))                                    # pale wall
    for x0 in (40, 400, 760):                                                                     # three tall windows, daylight
        _swindow(f, x0, 120, x0 + 280, 640, frame=(236, 232, 224), glass_top=(150, 196, 240), glass_bot=(220, 236, 246))
    _srect(f, 0, 640, W, 668, (226, 222, 212), (200, 196, 186), (120, 116, 108), 2)             # sill
    # menu board (plain: lines only) above the counter
    _srect(f, 260, 700, 820, 830, (36, 38, 44), (26, 28, 32), (90, 90, 96), 2)
    fs = font(F_ANTON, 40); im = Image.new("L", (560, 50), 0); ImageDraw.Draw(im).text((280, 25), "MENU", font=fs, fill=255, anchor="mm")
    m = np.asarray(im, np.float32) / 255; f[705:755, 260:820] = f[705:755, 260:820] * (1 - m[..., None]) + _c((246, 244, 236)) * m[..., None]
    for k in range(3): cv2.line(f, (300, 770 + k * 18), (560 + k * 40, 770 + k * 18), _scv((200, 200, 196)), 4, cv2.LINE_AA)
    # serving counter (stainless front, warm food lamps)
    _srect(f, 150, 860, 930, 900, (236, 236, 232), (206, 206, 200), (110, 110, 110), 2)           # top
    _srect(f, 160, 900, 920, 1060, (186, 190, 198), (130, 134, 142), (70, 70, 76), 3)             # front
    for x in range(200, 900, 120): cv2.rectangle(f, (x, 930), (x + 80, 1030), _scv((150, 154, 162)), 2, cv2.LINE_AA)
    for x in (300, 540, 780):
        _srect(f, x - 60, 830, x + 60, 858, (190, 60, 50), (140, 40, 34), (60, 20, 16), 2)           # heat lamps (red hoods)
        _sglow(f, x, 880, 120, (255, 200, 120), 0.3)
    for (x, c) in ((300, (246, 230, 190)), (540, (150, 92, 60)), (780, (176, 28, 60))):           # food wells: mash / meatballs / jam
        cv2.ellipse(f, (x, 870), (54, 14), 0, 0, 360, _scv(c), -1, cv2.LINE_AA)
    # long tables with benches, two rows, in perspective (closer = lower + wider)
    f[y0:] = 0; _sfloor(f, y0, 540, (214, 206, 190), (160, 150, 130), tile=False, n_lines=9, line_col=(176, 168, 150))
    birch, edge, bench = (226, 200, 150), (176, 146, 96), (120, 126, 134)
    for (yt, hgt, x0, x1) in ((1240, 60, 60, 420), (1240, 60, 660, 1020), (1400, 110, -40, 460), (1400, 110, 620, 1120)):
        _srect(f, x0 - 20, yt + hgt + 70, x1 + 20, yt + hgt + 100, bench, tuple(int(v * 0.7) for v in bench), (50, 50, 56), 2)   # bench
        _srect(f, x0, yt, x1, yt + hgt, birch, edge, (90, 70, 40), 3)                                                   # table top
        for x in (x0 + 30, x1 - 50): _srect(f, x, yt + hgt, x + 20, yt + hgt + 120, edge, tuple(int(v * 0.8) for v in edge), (90, 70, 40), 2)   # legs
        for tx in range(x0 + 40, x1 - 60, 150):                                                                        # trays on the tables
            cv2.rectangle(f, (tx, yt + 8), (tx + 90, yt + hgt - 8), _scv((126, 64, 54)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (tx + 45, yt + hgt // 2), (26, 10), 0, 0, 360, _scv((250, 250, 246)), -1, cv2.LINE_AA)
    _sglow(f, 540, 400, 700, (255, 250, 236), 0.2)
    _atmos(f, "store_cafe")
    f *= (0.9 + 0.16 * np.exp(-(((_xx - W / 2) / 700) ** 2 + ((_yy - 800) / 900) ** 2)))[..., None]
    return np.clip(f, 0, 1).astype(np.float32)


_STORY_SETS.update(maze_store=_maze_store, market_hall=_market_hall, store_cafe=_store_cafe)
_FLOOR.update(maze_store=1180, market_hall=1200, store_cafe=1200)
SET_LIGHT.update(maze_store="day", market_hall="cool", store_cafe="day")
SETS = tuple(_FLOOR)
