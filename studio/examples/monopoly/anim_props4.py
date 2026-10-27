# ================= props for "Monopoly was invented to warn against monopolies" (generic: no real game trade dress) =================
# Board: plain cream squares with INVENTED street names, no coloured property bands, no GO arrow, no mascot, no deed cards.
PAPER2 = (246, 236, 208); WOOD = (196, 140, 84); WOOD_D = (140, 92, 50)
BOARD_NAMES = ["LORD LANE", "RENT ROW", "CASH CT", "GREED ST", "TOLL RD", "LAND AVE", "DEBT DR", "MINT ST", "WAGE WAY",
               "PARK PL.", "TAX TER.", "COIN CT", "RICH RD", "LOAN LN", "DUE DR", "FEE FWY", "LEASE LN", "GOLD GR",
               "ACRE AVE", "PLOT PL", "DEED DR", "SHARE ST", "BANK BLVD", "RENT RD", "HOLD HWY", "VAULT VW", "OWN ORCH",
               "LOT LN", "TENANT TR", "YIELD YD", "PROFIT PK", "LEDGER LN", "BOND BLVD", "INCOME IN", "MARKET MW", "PENNY PL"]


def board_el(w=760, corners=("START", "GO TO JAIL", "PUBLIC PARK", "LORD'S\nMANOR"), centre="", hand=0.0, names=None, seed=0, n_side=9,
             paper=PAPER2):
    """square game board, top-down. hand>0 = hand-drawn copy (wobbly lines, pencil names)."""
    key = ("board", w, corners, centre, hand, tuple(names or ()), seed, n_side, paper)
    def mk():
        sc = 2; im, d = _canvas(w, w); S = lambda *v: [x * sc for x in v]
        rng = np.random.default_rng(seed)
        jit = lambda: (rng.uniform(-1, 1) * 3 * hand)
        _ov(im, lambda q: q.rounded_rectangle(S(12, 16, w - 2, w - 2), 18 * sc, fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 12, w - 12), 14 * sc, fill=255), tuple(min(255, c + 6) for c in paper), tuple(max(0, c - 18) for c in paper))
        B_ = w - 14; cw = B_ * 0.15; sw = (B_ - 2 * cw) / n_side; o = 2
        col = (60, 54, 64, 255) if hand else INK + (255,); lw = (3 if hand else 4) * sc
        def L(x0, y0, x1, y1):
            d.line([((x0 + jit()) * sc, (y0 + jit()) * sc), ((x1 + jit()) * sc, (y1 + jit()) * sc)], fill=col, width=lw)
        L(o, o, o + B_, o); L(o, o + B_, o + B_, o + B_); L(o, o, o, o + B_); L(o + B_, o, o + B_, o + B_)
        L(o + cw, o + cw, o + B_ - cw, o + cw); L(o + cw, o + B_ - cw, o + B_ - cw, o + B_ - cw)
        L(o + cw, o + cw, o + cw, o + B_ - cw); L(o + B_ - cw, o + cw, o + B_ - cw, o + B_ - cw)
        for i in range(1, n_side):
            x = o + cw + i * sw
            L(x, o, x, o + cw); L(x, o + B_ - cw, x, o + B_)
            L(o, x, o + cw, x); L(o + B_ - cw, x, o + B_, x)
        nm = names or BOARD_NAMES
        fs = max(9, int(sw * 0.2)); fn = font(F_BOLD, fs * sc)
        k = 0
        for side in range(4):
            for i in range(n_side):
                c = o + cw + (i + 0.5) * sw
                if side == 0: x, y, rot = c, o + B_ - cw / 2, 0
                elif side == 1: x, y, rot = o + cw / 2, o + B_ - c, -90
                elif side == 2: x, y, rot = o + B_ - c, o + cw / 2, 180
                else: x, y, rot = o + B_ - cw / 2, c, 90
                txt = nm[(k + seed * 5) % len(nm)]; k += 1
                ti = Image.new("RGBA", (int(cw * 0.95 * sc), int(sw * 0.95 * sc)), (0, 0, 0, 0)); td = ImageDraw.Draw(ti)
                parts = txt.split(" ")
                for j, p in enumerate(parts[:2]):
                    td.text((ti.size[0] / 2, ti.size[1] * (0.5 + (j - (len(parts[:2]) - 1) / 2) * 0.3)), p, font=fn, fill=col, anchor="mm")
                ti = ti.rotate(90 if side in (0, 2) else 0, expand=True).rotate(rot if side in (1, 3) else (180 if side == 2 else 0), expand=True)
                im.alpha_composite(ti, (int(x * sc - ti.size[0] / 2), int(y * sc - ti.size[1] / 2)))
        fc = font(F_BLACK, int(cw * 0.15) * sc)
        for (cx, cy), lab in zip(((o + B_ - cw / 2, o + B_ - cw / 2), (o + cw / 2, o + B_ - cw / 2), (o + cw / 2, o + cw / 2), (o + B_ - cw / 2, o + cw / 2)), corners):
            for j, p in enumerate(lab.split("\n") if "\n" in lab else lab.split(" ", 1) if len(lab) > 7 else [lab]):
                nl = len(lab.split("\n") if "\n" in lab else lab.split(" ", 1) if len(lab) > 7 else [lab])
                d.text((cx * sc, (cy + (j - (nl - 1) / 2) * cw * 0.2) * sc), p, font=fc, fill=(RED_ if "JAIL" in lab else INK) + (255,), anchor="mm")
        if centre:
            fsz = int(w * 0.075)
            while fsz > 10 and font(F_PF9, fsz * sc).getlength(centre) > (B_ - 2 * cw) * 0.86 * sc: fsz -= 2
            d.text((w / 2 * sc, w / 2 * sc), centre, font=font(F_PF9 if not hand else F_BLACK, fsz * sc),
                   fill=(150, 30, 40, 255) if not hand else col, anchor="mm")
        return _done(im, w, w)
    return gcache(key, mk)


def board_xy(cx, cy, w, idx, n_side=9):
    """centre of square idx (0 = START corner bottom-right, going anticlockwise like the patent board) for a board drawn at (cx, cy) size w"""
    B_ = w - 14; cw = B_ * 0.15; sw = (B_ - 2 * cw) / n_side; per = n_side + 1
    side, i = divmod(idx % (4 * per), per); x0, y0 = cx - w / 2 + 2, cy - w / 2 + 2
    if side == 0: return (x0 + B_ - cw / 2 - (i * sw + (cw / 2 + sw / 2 - sw if i else 0)), y0 + B_ - cw / 2) if i == 0 else (x0 + B_ - cw - (i - 0.5) * sw, y0 + B_ - cw / 2)
    if side == 1: return (x0 + cw / 2, y0 + B_ - cw / 2) if i == 0 else (x0 + cw / 2, y0 + B_ - cw - (i - 0.5) * sw)
    if side == 2: return (x0 + cw / 2, y0 + cw / 2) if i == 0 else (x0 + cw + (i - 0.5) * sw, y0 + cw / 2)
    return (x0 + B_ - cw / 2, y0 + cw / 2) if i == 0 else (x0 + B_ - cw / 2, y0 + cw + (i - 0.5) * sw)


def pawn_el(w=90, col=(232, 60, 40)):
    def mk():
        h = int(w * 1.5); sc = 3; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.62)) for c in col)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.08, h * 0.78, w * 0.92, h * 0.98), fill=255), col, dk)
        shape_grad(im, lambda m: m.polygon(S(w * 0.3, h * 0.42, w * 0.7, h * 0.42, w * 0.84, h * 0.88, w * 0.16, h * 0.88), fill=255), col, dk)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.2, h * 0.36, w * 0.8, h * 0.48), fill=255), col, dk)
        shape_grad(im, lambda m: m.ellipse(S(w * 0.22, h * 0.02, w * 0.78, h * 0.4), fill=255), tuple(min(255, c + 50) for c in col), col)
        d.ellipse(S(w * 0.34, h * 0.08, w * 0.48, h * 0.17), fill=(255, 255, 255, 150))
        return _done(im, w, h)
    return gcache(("pawn", w, col), mk)


def house_el(w=70, col=WOOD, hotel=False):
    def mk():
        ww = int(w * (1.7 if hotel else 1)); h = int(w * 0.95); sc = 3; im, d = _canvas(ww, h, sc); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.7)) for c in col)
        d.polygon(S(ww * 0.06, h * 0.42, ww * 0.5, h * 0.04, ww * 0.94, h * 0.42), fill=dk + (255,))
        shape_grad(im, lambda m: m.rectangle(S(ww * 0.14, h * 0.4, ww * 0.86, h * 0.98), fill=255), col, dk)
        d.rectangle(S(ww * 0.42, h * 0.62, ww * 0.58, h * 0.98), fill=(70, 46, 30, 255))
        return _done(im, ww, h)
    return gcache(("house", w, col, hotel), mk)


def patent_el(w=620):
    """1904-style patent sheet with the board drawing (public record: US 748,626, 5 Jan 1904)"""
    def mk():
        h = int(w * 1.3); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(12, 16, w - 2, h - 2), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rectangle(S(2, 2, w - 12, h - 12), fill=255), (250, 244, 226), (232, 220, 190))
        d.rectangle(S(18, 18, w - 28, h - 28), outline=(90, 70, 50, 255), width=3 * sc)
        d.text((w / 2 * sc, 60 * sc), "No. 748,626.", font=font(F_PF9, 36 * sc), fill=(60, 44, 30, 255), anchor="mm")
        d.text((w / 2 * sc, 104 * sc), "PATENTED JAN. 5, 1904.", font=font(F_PF, 26 * sc), fill=(60, 44, 30, 255), anchor="mm")
        d.text((w / 2 * sc, 142 * sc), "L. J. MAGIE.  GAME BOARD.", font=font(F_PF, 24 * sc), fill=(60, 44, 30, 255), anchor="mm")
        bw = int(w * 0.72)
        b_ = board_el(bw, corners=("", "GO TO JAIL", "PUBLIC PARK", ""), hand=0.6, paper=(250, 244, 226), seed=3)
        pm, a = b_
        bim = Image.fromarray((np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-4), 0, 1), a]) * 255).astype(np.uint8), "RGBA").resize((bw * sc, bw * sc))
        im.alpha_composite(bim, (int((w - bw) / 2 * sc), int(180 * sc)))
        y0 = 180 + bw + 30
        d.text((90 * sc, y0 * sc), "Fig. 1.", font=font(F_PFI, 24 * sc), fill=(60, 44, 30, 255), anchor="lm")
        pts = [(w - 300 + i * 12, y0 + 10 + 12 * math.sin(i * 1.1)) for i in range(18)]
        d.line([(x * sc, y * sc) for x, y in pts], fill=(40, 40, 90, 255), width=3 * sc)
        d.text(((w - 190) * sc, (y0 + 44) * sc), "Inventor", font=font(F_PFI, 20 * sc), fill=(60, 44, 30, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("patent", w), mk)


def book_el(title, sub, col, icon="fist", w=330):
    """a rulebook cover: title + simple icon (fist = crush, hands = share)"""
    def mk():
        h = int(w * 1.32); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.65)) for c in col)
        _ov(im, lambda q: q.rounded_rectangle(S(14, 18, w - 2, h - 2), 14 * sc, fill=(0, 0, 0, 80)))
        d.rounded_rectangle(S(w - 34, 12, w - 10, h - 20), 6 * sc, fill=(248, 244, 232, 255), outline=INK + (255,), width=3 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 22, h - 16), 14 * sc, fill=255), col, dk)
        d.rounded_rectangle(S(2, 2, w - 22, h - 16), 14 * sc, outline=INK + (255,), width=5 * sc)
        d.rectangle(S(20, 2, 34, h - 16), fill=dk + (255,))
        d.text(((w - 10) / 2 * sc, 64 * sc), "RULES", font=font(F_BLACK, 30 * sc), fill=(255, 255, 255, 230), anchor="mm")
        _ts = 46
        while _ts > 14 and font(F_BLACK, _ts * sc).getlength(title) > (w - 80) * sc: _ts -= 2
        d.text(((w - 10) / 2 * sc, 112 * sc), title, font=font(F_BLACK, _ts * sc), fill=(255, 255, 255, 255), anchor="mm")
        cx, cy = (w - 10) / 2, h * 0.58
        if icon == "fist":
            d.rounded_rectangle(S(cx - 62, cy - 50, cx + 62, cy + 40), 26 * sc, fill=(255, 236, 210, 255), outline=INK + (255,), width=5 * sc)
            for k in range(3): d.line(S(cx - 30 + 30 * k, cy - 50, cx - 30 + 30 * k, cy - 14), fill=INK + (255,), width=4 * sc)
            d.rounded_rectangle(S(cx - 40, cy + 30, cx + 40, cy + 90), 10 * sc, fill=(255, 236, 210, 255), outline=INK + (255,), width=5 * sc)
        else:
            for sx in (-1, 1):
                d.rounded_rectangle(S(cx + sx * 20 - 50 + (25 if sx > 0 else -25) * 0, cy - 26, cx + sx * 20 + 50, cy + 26), 24 * sc,
                                    fill=(255, 236, 210, 255) if sx < 0 else (226, 186, 150, 255), outline=INK + (255,), width=5 * sc)
            for k in range(-1, 2): d.text(((cx + 70 * k) * sc, (cy - 74) * sc), "$", font=font(F_BLACK, 40 * sc), fill=(255, 230, 120, 255), anchor="mm")
        d.text(((w - 10) / 2 * sc, (h - 70) * sc), sub, font=font(F_BOLD, 22 * sc), fill=(255, 255, 255, 235), anchor="mm")
        return _done(im, w, h)
    return gcache(("book", title, sub, col, icon, w), mk)


def gamebox_el(w=300, col=NAVY_, label="BOARD GAME"):
    """plain generic game box (no real packaging)"""
    def mk():
        h = int(w * 0.62); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        dk = tuple(max(0, int(c * 0.6)) for c in col)
        d.rectangle(S(6, h * 0.72, w - 6, h - 4), fill=dk + (255,))
        shape_grad(im, lambda m: m.rounded_rectangle(S(2, 2, w - 2, h * 0.8), 10 * sc, fill=255), tuple(min(255, c + 40) for c in col), col)
        d.rounded_rectangle(S(2, 2, w - 2, h * 0.8), 10 * sc, outline=INK + (255,), width=4 * sc)
        d.rounded_rectangle(S(w * 0.12, h * 0.18, w * 0.88, h * 0.6), 8 * sc, outline=(255, 255, 255, 200), width=3 * sc)
        d.text((w / 2 * sc, h * 0.39 * sc), label, font=font(F_BLACK, int(w * 0.085) * sc), fill=(255, 255, 255, 255), anchor="mm")
        return _done(im, w, h)
    return gcache(("gbox", w, col, label), mk)


def census_el(w=640, rows=(("NAME", "ELIZABETH M. PHILLIPS"),), title="1940 CENSUS"):
    """census form card; rows are drawn by the shot (so they can be typed in)"""
    def mk():
        h = int(w * 0.82); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(12, 16, w - 2, h - 2), fill=(0, 0, 0, 70)))
        shape_grad(im, lambda m: m.rectangle(S(2, 2, w - 12, h - 12), fill=255), (246, 240, 222), (226, 216, 186))
        d.rectangle(S(2, 2, w - 12, h - 12), outline=(70, 60, 50, 255), width=4 * sc)
        d.rectangle(S(2, 2, w - 12, 76), fill=(70, 60, 50, 255))
        d.text((w / 2 * sc, 40 * sc), title, font=font(F_PF9, 38 * sc), fill=(246, 240, 222, 255), anchor="mm")
        for i in range(4):
            y = 150 + i * 110
            d.line(S(40, y + 34, w - 52, y + 34), fill=(120, 110, 96, 255), width=2 * sc)
        return _done(im, w, h)
    return gcache(("census", w, title), mk)


def oldcheque_el(amount="$500", w=700):
    def mk():
        h = int(w * 0.42); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        _ov(im, lambda q: q.rectangle(S(12, 16, w - 2, h - 2), fill=(0, 0, 0, 80)))
        shape_grad(im, lambda m: m.rectangle(S(2, 2, w - 12, h - 12), fill=255), (232, 240, 222), (206, 220, 196))
        d.rectangle(S(2, 2, w - 12, h - 12), outline=(60, 80, 60, 255), width=4 * sc)
        d.rectangle(S(14, 14, w - 24, h - 24), outline=(120, 150, 120, 255), width=2 * sc)
        d.text((36 * sc, 50 * sc), "PARKER BROTHERS", font=font(F_PF9, 28 * sc), fill=(40, 60, 40, 255), anchor="lm")
        d.text(((w - 50) * sc, 50 * sc), "1935", font=font(F_PF, 26 * sc), fill=(40, 60, 40, 255), anchor="rm")
        d.text((36 * sc, 112 * sc), "PAY TO  Lizzie Magie", font=font(F_PFI, 30 * sc), fill=(30, 40, 90, 255), anchor="lm")
        d.line(S(150, 134, w - 60, 134), fill=(60, 80, 60, 255), width=2 * sc)
        d.rectangle(S(w - 230, h - 104, w - 40, h - 44), fill=(255, 255, 255, 255), outline=(60, 80, 60, 255), width=3 * sc)
        d.text(((w - 135) * sc, (h - 74) * sc), amount, font=font(F_BLACK, 40 * sc), fill=RED_ + (255,), anchor="mm")
        d.text((36 * sc, (h - 60) * sc), "FOR: one patent", font=font(F_PFI, 22 * sc), fill=(40, 60, 40, 255), anchor="lm")
        return _done(im, w, h)
    return gcache(("ocheque", amount, w), mk)


def gavel_el(w=360):
    def mk():
        h = int(w * 0.7); sc = 2; im, d = _canvas(w, h); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(w * 0.42, h * 0.3, w * 0.98, h * 0.42), 10 * sc, fill=WOOD_D + (255,), outline=INK + (255,), width=4 * sc)
        shape_grad(im, lambda m: m.rounded_rectangle(S(w * 0.04, h * 0.06, w * 0.46, h * 0.66), 20 * sc, fill=255), WOOD, WOOD_D)
        d.rounded_rectangle(S(w * 0.04, h * 0.06, w * 0.46, h * 0.66), 20 * sc, outline=INK + (255,), width=5 * sc)
        for x in (0.12, 0.38): d.line(S(w * x, h * 0.06, w * x, h * 0.66), fill=INK + (255,), width=4 * sc)
        return _done(im, w, h)
    return gcache(("gavel", w), mk)


def bun_hair(f, x, y, s=1.0, col=(92, 52, 30)):
    """Lizzie: hair bun + side hair drawn on top of guy() at feet (x, y), same s"""
    hx, hy = x, y - 178 * s - 168 * s - 76 * s
    cv2.ellipse(f, (int(hx), int(hy - 80 * s)), (int(44 * s), int(34 * s)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy - 58 * s)), (int(86 * s), int(30 * s)), 0, 180, 360, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy - 80 * s)), (int(44 * s), int(34 * s)), 0, 0, 360, C(INK), max(1, int(5 * s)), cv2.LINE_AA)


def dress(f, x, y, s=1.0, col=(120, 60, 170)):
    """long dress over the stick body (covers the tie), feet baseline y"""
    hip = (x, y - 178 * s); neck = (x, hip[1] - 168 * s)
    pts = np.array([[neck[0] - 26 * s, neck[1] + 8 * s], [neck[0] + 26 * s, neck[1] + 8 * s], [x + 30 * s, hip[1]], [x + 90 * s, y - 20 * s],
                    [x - 90 * s, y - 20 * s], [x - 30 * s, hip[1]]], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA); cv2.polylines(f, [pts], True, C(INK), max(1, int(6 * s)), cv2.LINE_AA)
    cv2.line(f, (int(x - 30 * s), int(hip[1])), (int(x + 30 * s), int(hip[1])), C(INK), max(1, int(5 * s)), cv2.LINE_AA)


def lizzie(f, x, y, s=1.0, **kw):
    """guy() dressed as Lizzie: draw the stick figure, then dress + bun (face stays the mascot style)"""
    hands = guy(f, x, y, s, **kw)
    dress(f, x, y, s)
    hel = head_el(kw.get("mouth", 0), kw.get("blink", False), kw.get("brow", "n"), kw.get("look", (0, 0))[0], kw.get("look", (0, 0))[1], kw.get("expr", "n"))
    bun_hair(f, x, y, s)
    comp(f, scale_el(hel, s), x, y - 178 * s - 168 * s - 76 * s + kw.get("bob", 0.0) * s)
    for side in (-1, 1):
        hx, hy = hands[side]
        cv2.circle(f, (int(hx), int(hy)), int(15 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(hx), int(hy)), int(10 * s), (1, 1, 1), -1, cv2.LINE_AA)
    return hands


def hat(f, x, y, s=1.0, col=(70, 66, 74)):
    """fedora on a standing guy at feet (x, y)"""
    hx, hy = x, y - 178 * s - 168 * s - 76 * s - 92 * s
    cv2.ellipse(f, (int(hx), int(hy + 22 * s)), (int(112 * s), int(18 * s)), 0, 0, 360, C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx - 66 * s), int(hy - 40 * s)), (int(hx + 66 * s), int(hy + 20 * s)), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(hx - 66 * s), int(hy + 2 * s)), (int(hx + 66 * s), int(hy + 14 * s)), C((30, 28, 32)), -1, cv2.LINE_AA)
