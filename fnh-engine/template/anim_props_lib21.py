# ================= anim_props_lib21.py (ep 21, 2 Nov): the BREAD ink props + the MORNING WORKTOP place + the INSIDE-THE-CRUMB place.
# ONE accent per video: CRUST GOLD = bread, starch, titles, chips; COLD BLUE = fridge / freezer (from lib20). Props: bread_slice_el (fresh / stale /
# frozen / toasted / mould, optional face), loaf_el (side view with an end face, stale state, nightcap), fridge_ink_el (top freezer + main door, each can open;
# shelves, eggs, milk, loaf inside), toaster_el (slices pop up), bread_bin_el, freezer_bag_el, nail_el + board_ink2_el, starch_guy_el (the culprit: a
# wiggly starch chain with a face), wanted_el (a WANTED poster), tomb_el (R.I.P. tombstone), egg_el, drop_lock_el; live drawings: starch_lock (rows with
# water locked between them, reverse of ep 20's squeeze-out), temp_strip (a thermometer ruler with the fast zone), race_lanes (three loaves race to STALE);
# places: set_worktop + worktop_front (morning kitchen, drawers, towel = no more empty foreground), set_crumb (inside a slice of bread).
ACC = (204, 132, 44); ACC_S = (140, 82, 22); ACC_L = (242, 200, 124); ACC_XL = (250, 232, 196)      # crust gold accent
CRUST = (198, 130, 58); CRUST_S = (146, 88, 34); CRUMB = (252, 238, 204); CRUMB_S = (232, 208, 164); STALE_C = (214, 202, 176); STALE_S = (176, 162, 136)
TOAST_C = (214, 150, 74); FROST = (214, 236, 252); MOULD = (92, 142, 112); MOULD_D = (54, 96, 84)
SCHEMES["breadp"] = ((244, 226, 186), (252, 244, 222), (238, 216, 170), (0.8, 0.68, 0.48))
SCHEMES["coldb"] = ((176, 208, 236), (230, 242, 252), (160, 196, 228), (0.52, 0.68, 0.84))
SCHEMES["freeze"] = ((130, 176, 220), (214, 234, 250), (112, 160, 208), (0.42, 0.62, 0.82))
SCHEMES["moss"] = ((176, 196, 150), (232, 238, 208), (160, 184, 136), (0.56, 0.66, 0.46))
SCHEMES["toastp"] = ((246, 190, 120), (254, 232, 190), (240, 176, 100), (0.88, 0.6, 0.32))


def _mix(a, b, k): return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


SLICE = [(52, 118), (34, 86), (40, 48), (76, 22), (150, 12), (224, 22), (260, 48), (266, 86), (248, 118), (246, 290), (150, 300), (54, 290)]


def bread_slice_el(stale=0.0, mood=None, look=(0, 0), frozen=0.0, toast=0.0, mould=0.0, seed=1):
    """a sandwich slice face-on. stale 0..1 = paler dull crumb, cracks, the corners curl; frozen 0..1 = blue + frost; toast 0..1 = brown from the middle;
    mould 0..1 = green-blue fuzzy blobs spreading."""
    stale, frozen, toast, mould = [round(clamp(v) * 6) / 6 for v in (stale, frozen, toast, mould)]
    def mk():
        w, h = 300, 320; im, d, S = _cv(w, h)
        cur = 10 * stale
        P = [(x + (x - 150) * 0.02 * stale, y + (cur if y > 250 and abs(x - 150) > 60 else 0) * -1) for x, y in SLICE]
        cr = _mix(_mix(CRUST, STALE_S, stale * 0.7), (150, 186, 220), frozen * 0.55)
        _ink_poly(d, P, cr, seed, INK_W, amp=1.6)
        Q = [(150 + (x - 150) * 0.86, 156 + (y - 156) * 0.9) for x, y in P]
        cc = _mix(_mix(CRUMB, STALE_C, stale), FROST, frozen * 0.8)
        d.polygon([(x * SC3, y * SC3) for x, y in _wob(Q, 1.2, seed + 1)], fill=cc + (255,))
        if toast > 0:
            lay = Image.new("RGBA", im.size, (0, 0, 0, 0)); q = ImageDraw.Draw(lay)
            q.polygon([(150 * SC3 + (x - 150) * SC3 * 0.74, 156 * SC3 + (y - 156) * SC3 * 0.8) for x, y in Q], fill=TOAST_C + (int(230 * toast),))
            lay = lay.filter(ImageFilter.GaussianBlur(9 * SC3)); im.alpha_composite(lay)
        rng = np.random.default_rng(seed + 5)
        for i in range(30):                                                                  # the crumb's little holes
            px, py = rng.uniform(70, 230), rng.uniform(46, 276); rx = rng.uniform(3, 8); ry = rx * rng.uniform(0.6, 1.0)
            d.ellipse(S(px - rx, py - ry, px + rx, py + ry), fill=_mix(cc, (150, 118, 80), 0.32 + 0.1 * toast) + (255,))
        _hatch_in(im, (180, 30, 250, 290), lambda q, S_: q.polygon(S_(196, 40, 244, 56, 234, 280, 196, 286), fill=255), -40, 11, 22)
        if stale > 0.3:
            for (x0, y0, a) in ((64, 196, 80), (238, 186, 100), (104, 278, -70), (196, 276, -110), (150, 30, 90)):
                L = 56 * stale; aa = math.radians(a); pts = [(x0, y0)]
                for k in range(4): pts.append((pts[-1][0] + L / 4 * math.cos(aa) + 6 * (-1) ** k * math.sin(aa), pts[-1][1] + L / 4 * math.sin(aa) + 6 * (-1) ** k * math.cos(aa)))
                d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (190,), width=3 * SC3, joint="curve")
        if frozen > 0:
            for i in range(26):
                px, py = rng.uniform(46, 254), rng.uniform(24, 290); r_ = rng.uniform(1.5, 4)
                d.ellipse(S(px - r_, py - r_, px + r_, py + r_), fill=(255, 255, 255, int(220 * frozen)))
        if mould > 0:
            for (px, py, r_) in ((96, 90, 42), (206, 214, 52), (116, 236, 30), (214, 70, 26), (160, 150, 20)):
                r2 = r_ * mould
                for k in range(11):
                    a_ = k * 0.57; dd = r2 * (0.3 + 0.7 * (k % 3) / 2)
                    xx, yy = px + dd * math.cos(a_ * 2.4), py + dd * math.sin(a_ * 2.4); rr = r2 * 0.42
                    d.ellipse(S(xx - rr, yy - rr, xx + rr, yy + rr), fill=(MOULD if k % 2 else MOULD_D) + (255,))
        if mood: _face(d, S, 150, 150, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("bslice21", stale, mood, look, frozen, toast, mould, seed), mk)


def loaf_el(stale=0.0, mood=None, look=(0, 0), cap=False, frost=0.0, seed=2):
    """a tin loaf from the side with a cut end face on the left; stale = dull + cracked, cap = a little nightcap (the loaf 'tucked in')."""
    stale, frost = round(clamp(stale) * 6) / 6, round(clamp(frost) * 4) / 4
    def mk():
        w, h = 520, 340; im, d, S = _cv(w, h)
        top = [(120, 96), (170, 56), (300, 40), (420, 54), (482, 100), (484, 150), (472, 300), (120, 300)]
        cr = _mix(_mix(CRUST, STALE_S, stale * 0.8), (160, 196, 228), frost * 0.6)
        _ink_poly(d, top, cr, seed, INK_W, amp=2.0)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in top], fill=255),
               lambda q, S_, c: q.polygon(S_(120, 210, 490, 200, 490, 310, 120, 310), fill=c), CRUST_S, 110)
        _hatch_in(im, (300, 200, 480, 300), lambda q, S_: q.polygon(S_(300, 210, 478, 200, 470, 298, 300, 298), fill=255), -40, 11, 30)
        for x0 in (210, 300, 390):                                                            # the score marks on top
            d.line([(a * SC3, b * SC3) for a, b in _wob([(x0 - 20, 66 + (x0 - 300) ** 2 * 0.0006), (x0 + 26, 96)], 1.0, x0)], fill=_mix(cr, (255, 240, 200), 0.5) + (255,), width=7 * SC3)
        face = [(52, 118), (36, 88), (42, 52), (76, 28), (130, 22), (182, 30), (214, 54), (218, 90), (200, 118), (198, 300), (54, 300)]
        _ink_poly(d, face, cr, seed + 1, INK_W, amp=1.4)
        Q = [(126 + (x - 126) * 0.84, 160 + (y - 160) * 0.9) for x, y in face]
        cc = _mix(_mix(CRUMB, STALE_C, stale), FROST, frost * 0.8)
        d.polygon([(x * SC3, y * SC3) for x, y in _wob(Q, 1.2, seed + 2)], fill=cc + (255,))
        rng = np.random.default_rng(seed)
        for i in range(16):
            px, py = rng.uniform(70, 182), rng.uniform(52, 282); rx = rng.uniform(3, 7)
            d.ellipse(S(px - rx, py - rx * 0.8, px + rx, py + rx * 0.8), fill=_mix(cc, (150, 118, 80), 0.32) + (255,))
        if stale > 0.3:
            for (x0, y0, a) in ((250, 90, 70), (360, 60, 110), (440, 130, 100), (74, 250, -80), (170, 268, -100)):
                L = 70 * stale; aa = math.radians(a); pts = [(x0, y0)]
                for k in range(4): pts.append((pts[-1][0] + L / 4 * math.cos(aa) + 6 * (-1) ** k * math.sin(aa), pts[-1][1] + L / 4 * math.sin(aa) + 6 * (-1) ** k * math.cos(aa)))
                d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (200,), width=3 * SC3, joint="curve")
        if frost > 0:
            for i in range(40):
                px, py = rng.uniform(50, 470), rng.uniform(40, 296); r_ = rng.uniform(1.5, 4)
                d.ellipse(S(px - r_, py - r_, px + r_, py + r_), fill=(255, 255, 255, int(230 * frost)))
        if cap:
            _ink_poly(d, [(44, 66), (96, 8), (176, 2), (214, 56), (130, 34)], (86, 130, 190), seed + 3, INK_W - 1, amp=1.0)
            d.ellipse(S(30, 56, 62, 88), fill=(250, 248, 238, 255), outline=INKC + (255,), width=4 * SC3)
        if mood: _face(d, S, 126, 160, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("loaf21", stale, mood, look, cap, frost, seed), mk)


def _eggs(d, S, x, y, n=3, r_=19):
    for i in range(n):
        _ink_ell(d, x + i * (r_ * 2 + 6), y, r_, r_ * 1.28, (250, 240, 222), 30 + i, INK_W - 3, amp=0.8)


def fridge_ink_el(open_=False, top=False, loaf=False, loaf_state=0.0, eggs=True, milk=True, frozen_bag=False, seed=4):
    """an ink fridge from the front (470 x 930): top freezer + main door. open_ / top = that door swung to the right with the lit cold inside.
    loaf=True puts a loaf on the middle shelf next to the eggs."""
    loaf_state = round(clamp(loaf_state) * 6) / 6
    def mk():
        w, h = 560, 960; im, d, S = _cv(w, h)
        B_ = (232, 238, 240); BS_ = (196, 206, 212)
        _ink_poly(d, [(30, 20), (470, 20), (476, 930), (24, 930)], B_, seed, INK_W + 1, amp=1.6)
        _ink_poly(d, [(40, 26), (460, 26), (462, 250), (38, 250)], B_, seed + 1, INK_W - 1, amp=1.2)
        _ink_poly(d, [(38, 262), (462, 262), (466, 900), (34, 900)], B_, seed + 2, INK_W - 1, amp=1.2)
        for (x0, y0, x1, y1) in ((44, 214, 456, 246), (44, 800, 456, 894)):
            d.rectangle(S(x0, y0, x1, y1), fill=BS_ + (120,))
        _hatch_in(im, (360, 40, 460, 890), lambda q, S_: q.polygon(S_(380, 30, 458, 30, 460, 895, 380, 895), fill=255), -40, 12, 22)
        if top:
            d.rectangle(S(52, 36, 448, 240), fill=(190, 222, 248, 255), outline=INKC + (255,), width=6 * SC3)
            for yy in (120, 196): d.line(S(56, yy, 444, yy), fill=(120, 170, 214, 255), width=5 * SC3)
            rng = np.random.default_rng(9)
            for i in range(26):
                px, py = rng.uniform(60, 440), rng.uniform(44, 234); r_ = rng.uniform(1.5, 4)
                d.ellipse(S(px - r_, py - r_, px + r_, py + r_), fill=(255, 255, 255, 230))
            _ink_poly(d, [(462, 26), (556, 8), (556, 266), (462, 250)], B_, seed + 3, INK_W - 1, amp=1.0)
        else:
            d.rounded_rectangle(S(70, 180, 90, 240), 6 * SC3, fill=(150, 160, 170, 255), outline=INKC + (255,), width=3 * SC3)
        if open_:
            d.rectangle(S(52, 274, 448, 890), fill=(218, 240, 255, 255), outline=INKC + (255,), width=6 * SC3)
            for yy in (430, 600, 760): d.rectangle(S(56, yy, 444, yy + 10), fill=(160, 196, 226, 255), outline=INKC + (120,), width=2 * SC3)
            if milk:
                _ink_poly(d, [(92, 350), (106, 330), (106, 308), (138, 308), (138, 330), (152, 350), (152, 428), (92, 428)], (252, 250, 244), 41, INK_W - 3, amp=0.8)
                _ink_poly(d, [(190, 366), (262, 366), (262, 428), (190, 428)], (240, 170, 110), 42, INK_W - 3, amp=0.8)
                _ink_ell(d, 340, 400, 42, 28, (150, 200, 120), 43, INK_W - 3, amp=0.8)
            if eggs: _eggs(d, S, 300, 572, 3)
            _ink_poly(d, [(84, 700), (200, 700), (200, 758), (84, 758)], (232, 110, 90), 44, INK_W - 3, amp=0.8)
            _ink_poly(d, [(240, 690), (400, 690), (400, 758), (240, 758)], (250, 220, 120), 45, INK_W - 3, amp=0.8)
            _ink_poly(d, [(462, 262), (556, 240), (556, 926), (466, 900)], B_, seed + 4, INK_W - 1, amp=1.0)
            for yy in (390, 560, 730): d.rectangle(S(476, yy, 546, yy + 14), fill=BS_ + (255,), outline=INKC + (160,), width=2 * SC3)
        else:
            d.rounded_rectangle(S(70, 290, 90, 420), 6 * SC3, fill=(150, 160, 170, 255), outline=INKC + (255,), width=3 * SC3)
        el = _done(im, w, h)
        return el
    return gcache(("fridge21", open_, top, loaf, loaf_state, eggs, milk, frozen_bag, seed), mk)


def toaster_el(hot=0.0, seed=6):
    """an ink toaster (slices are drawn BEFORE it by the shot, so they rise out of the slot)."""
    hot = round(clamp(hot) * 4) / 4
    def mk():
        w, h = 420, 300; im, d, S = _cv(w, h)
        body = [(42, 70), (78, 34), (342, 34), (378, 70), (382, 240), (360, 270), (60, 270), (38, 240)]
        _ink_poly(d, body, (204, 210, 218), seed, INK_W, amp=1.6)
        _shade(im, lambda q, S_: q.polygon([(x * SC3, y * SC3) for x, y in body], fill=255), lambda q, S_, c: q.polygon(S_(250, 30, 390, 30, 390, 280, 250, 280), fill=c), (140, 148, 160), 130)
        d.rounded_rectangle(S(80, 42, 340, 62), 8 * SC3, fill=_mix((40, 34, 32), (255, 110, 40), hot) + (255,), outline=INKC + (255,), width=3 * SC3)
        d.rectangle(S(60, 90, 90, 104), fill=(255, 255, 255, 170))
        d.rounded_rectangle(S(378, 120, 406, 150), 6 * SC3, fill=(70, 60, 56, 255), outline=INKC + (255,), width=3 * SC3)
        for sx in (70, 340): d.rounded_rectangle(S(sx, 262, sx + 30, 286), 6 * SC3, fill=INKC + (255,))
        d.ellipse(S(180, 200, 240, 248), fill=(120, 126, 134, 255), outline=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("toaster21", hot, seed), mk)


def bread_bin_el(open_=0.0, seed=7):
    """a wooden bread bin on the counter (roll top; open_ lifts the lid)."""
    open_ = round(clamp(open_) * 2) / 2
    def mk():
        w, h = 460, 330; im, d, S = _cv(w, h)
        _ink_poly(d, [(30, 150), (430, 150), (440, 310), (20, 310)], (178, 126, 78), seed, INK_W, amp=1.6)
        _hatch_in(im, (260, 160, 430, 300), lambda q, S_: q.polygon(S_(260, 156, 428, 156, 436, 306, 260, 306), fill=255), -40, 11, 32)
        if open_ < 0.5:
            _ink_poly(d, [(30, 150), (60, 70), (230, 40), (400, 70), (430, 150)], (198, 146, 92), seed + 1, INK_W, amp=1.4)
            d.rounded_rectangle(S(190, 112, 270, 130), 6 * SC3, fill=INKC + (255,))
        else:
            _ink_poly(d, [(40, 150), (42, 60), (230, 26), (418, 60), (420, 150)], (120, 80, 50), seed + 1, INK_W, amp=1.4)
        return _done(im, w, h)
    return gcache(("bin21", open_, seed), mk)


def freezer_bag_el(n=4, frost=0.0, seed=8):
    """a clear freezer bag with n slices standing inside, a twist tie on the top."""
    frost = round(clamp(frost) * 2) / 2
    def mk():
        w, h = 400, 420; im, d, S = _cv(w, h)
        _ink_poly(d, [(60, 110), (340, 110), (368, 390), (32, 390)], (214, 234, 248), seed, INK_W - 2, amp=2.2)
        for i in range(n):
            x0 = 64 + i * 58
            _ink_poly(d, [(x0, 190), (x0 + 8, 150), (x0 + 70, 150), (x0 + 80, 190), (x0 + 76, 370), (x0 + 4, 370)], _mix(CRUMB, FROST, frost * 0.7), seed + i + 1, INK_W - 3, amp=1.0, col=CRUST_S)
        d.line(S(90, 140, 76, 360), fill=(255, 255, 255, 170), width=7 * SC3)
        _ink_poly(d, [(150, 110), (120, 40), (280, 40), (250, 110)], (226, 240, 250), seed + 8, INK_W - 3, amp=1.2)
        d.rectangle(S(142, 94, 258, 112), fill=ACC + (255,), outline=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("fbag21", n, frost, seed), mk)


def nail_el(sink=0.0, seed=9):
    """a nail in a wood block: sink 0..1 drives it in."""
    sink = round(clamp(sink) * 6) / 6
    def mk():
        w, h = 360, 280; im, d, S = _cv(w, h)
        ny = 30 + 86 * sink
        d.rectangle(S(172, ny + 10, 188, 170), fill=(150, 158, 168, 255), outline=INKC + (255,), width=4 * SC3)
        _ink_poly(d, [(146, ny), (214, ny), (214, ny + 14), (146, ny + 14)], (176, 184, 192), seed + 1, INK_W - 3, amp=0.6)
        _ink_poly(d, [(22, 150), (338, 150), (344, 262), (16, 262)], (170, 118, 72), seed, INK_W, amp=1.6)
        for yy in (176, 200, 228): d.line([(x * SC3, y * SC3) for x, y in _wob([(36, yy), (120, yy + 3), (230, yy - 3), (326, yy)], 1.2, yy)], fill=(130, 84, 46, 255), width=3 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("nail21", sink, seed), mk)


def starch_guy_el(mood="sus", look=(0, 0), tight=False, frozen=False, seed=10):
    """the culprit: a wiggly starch chain with a face; tight = straight stiff rod (crystal mood)."""
    def mk():
        w, h = 320, 460; im, d, S = _cv(w, h)
        P = []
        for j in range(24):
            y = 64 + j * 15.5; a_ = 0 if (tight or j < 6) else 56 * math.sin((j - 6) * 0.55)
            P.append((160 + a_, y))
        col_ = _mix(CRUMB, FROST, 0.7) if frozen else ACC_XL
        for (x, y) in P:
            d.ellipse(S(x - 49, y - 49, x + 49, y + 49), fill=INKC + (255,))
        for (x, y) in P:
            d.ellipse(S(x - 42, y - 42, x + 42, y + 42), fill=col_ + (255,))
        for (x, y) in P[8::3]: d.ellipse(S(x - 8, y - 8, x + 8, y + 8), fill=CRUMB_S + (255,))
        _face(d, S, 160, 92, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("starchguy21", mood, look, tight, frozen, seed), mk)


def wanted_el(seed=11):
    """a WANTED poster (paper); the shot draws the suspect on top."""
    def mk():
        w, h = 520, 680; im, d, S = _cv(w, h)
        _ink_poly(d, [(24, 24), (496, 14), (506, 660), (14, 668)], (240, 222, 178), seed, INK_W, amp=2.4)
        d.rectangle(S(70, 150, 450, 560), fill=(250, 240, 214, 255), outline=INKC + (255,), width=5 * SC3)
        for (x, y) in ((40, 40), (480, 34), (484, 640), (34, 644)): d.ellipse(S(x - 8, y - 8, x + 8, y + 8), fill=INKC + (255,))
        return _done(im, w, h)
    return gcache(("wanted21", seed), mk)


def tomb_el(seed=12):
    """a little ink tombstone with a slice engraved on it."""
    def mk():
        w, h = 400, 460; im, d, S = _cv(w, h)
        P = [(70, 440), (66, 150), (110, 66), (200, 36), (290, 66), (334, 150), (330, 440)]
        _ink_poly(d, P, (196, 196, 190), seed, INK_W, amp=2.2)
        _hatch_in(im, (230, 70, 330, 430), lambda q, S_: q.polygon(S_(240, 60, 330, 120, 328, 438, 240, 438), fill=255), -40, 11, 40)
        return _done(im, w, h)
    return gcache(("tomb21", seed), mk)


def egg_el(seed=13):
    def mk():
        w, h = 90, 120; im, d, S = _cv(w, h)
        _ink_poly(d, _arcpts(45, 62, 32, 46, 0, 360, 22)[:-1], (250, 240, 222), seed, INK_W - 2, amp=0.8)
        return _done(im, w, h)
    return gcache(("egg21", seed), mk)


def crystal_el(s=60, col=None, seed=14):
    """a small ink crystal (starch crystal icon)."""
    def mk():
        w, h = int(s * 2.4), int(s * 2.4); im, d, S = _cv(w, h); c = w / 2
        P = [(c, c - s), (c + s * 0.72, c - s * 0.3), (c + s * 0.5, c + s * 0.8), (c - s * 0.5, c + s * 0.8), (c - s * 0.72, c - s * 0.3)]
        _ink_poly(d, P, col or ACC_XL, seed, INK_W - 3, amp=0.8)
        d.line(S(c, c - s, c, c + s * 0.8), fill=INKC + (160,), width=2 * SC3)
        d.line(S(c - s * 0.72, c - s * 0.3, c, c + s * 0.05, c + s * 0.72, c - s * 0.3), fill=INKC + (160,), width=2 * SC3)
        return _done(im, w, h)
    return gcache(("crystal21", s, col, seed), mk)


# ---------------- live drawings ----------------
def starch_lock(f, cx, cy, k, t, w=600, h=420, n=6, locks=0.0, swell=0.0):
    """k = 0: loose swollen chains with free water drops between them (soft bread); k = 1: the same chains in tight rows with the water LOCKED between the rows,
    nothing leaves (locks 0..1 pops little padlocks onto the block). The reverse of the ep 20 squeeze-out picture: here the water stays."""
    k = clamp(k); hh = h * (1 + 0.12 * swell)
    gap = hh / n; rows = []
    px0, px1, py0, py1 = int(cx - w / 2 - 44), int(cx + w / 2 + 44), int(cy - h / 2 - 46), int(cy + h / 2 + 46)
    ov = f.copy(); cv2.rectangle(ov, (px0, py0), (px1, py1), C((254, 248, 232)), -1, cv2.LINE_AA); f[:] = f * 0.14 + ov * 0.86
    cv2.rectangle(f, (px0, py0), (px1, py1), C(INKC), 7, cv2.LINE_AA)
    for i in range(n):
        y_loose = cy - hh / 2 + (i + 0.5) * gap; y_tight = cy - (n - 1) * 62 / 2 + i * 62
        y0 = y_loose + (y_tight - y_loose) * eio(k)
        amp = 30 * (1 - k) + 1.5; ph = i * 1.3 + t * 2.0 * (1 - k)
        P = [(cx - w / 2 + j * w / 24, y0 + amp * math.sin(j * 0.9 + ph)) for j in range(25)]
        rows.append(y0)
        A = np.array(P, np.int32)
        cv2.polylines(f, [A], False, C(INKC), 22, cv2.LINE_AA)
        cv2.polylines(f, [A], False, C(_mix(ACC_L, STALE_C, k)), 14, cv2.LINE_AA)
    rng = np.random.default_rng(5)
    for i in range(15):
        xf = cx + rng.uniform(-w / 2.2, w / 2.2); yf = cy + rng.uniform(-hh / 2.2, hh / 2.2)
        rr = i % (n - 1); xt = cx - w / 2 + 40 + ((i * 4.7) % 12) * (w - 80) / 12; yt = cy - (n - 1) * 62 / 2 + rr * 62 + 31
        x = xf + (xt - xf) * eio(k) + 7 * (1 - k) * math.sin(t * 2.2 + i); y = yf + (yt - yf) * eio(k) + 7 * (1 - k) * math.cos(t * 1.9 + i)
        r_ = 16 - 4 * k
        cv2.circle(f, (int(x), int(y)), int(r_ + 3), C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), int(r_), C((110, 176, 236)), -1, cv2.LINE_AA)
        cv2.circle(f, (int(x - r_ * 0.3), int(y - r_ * 0.3)), max(1, int(r_ * 0.28)), C((240, 250, 255)), -1, cv2.LINE_AA)
    if locks > 0:
        for j, (dx, dy) in enumerate(((-w * 0.32, -h * 0.28), (w * 0.34, -h * 0.05), (-w * 0.12, h * 0.26))):
            kk = clamp(locks * 3 - j)
            if kk > 0: comp(f, scale_el(padlock_el(), 0.42 * eo(kk)), cx + dx, cy + dy)


def temp_strip(f, t, x0=110, x1=970, y=1010, zone=1.0, marker=None, labels=True, mode="fast"):
    """a horizontal thermometer ruler: FREEZER (-20) .. FRIDGE .. KITCHEN; zone lights the 0-10 C fast band; marker = C value of a moving pointer."""
    T0, T1 = -24.0, 34.0
    X = lambda c: x0 + (x1 - x0) * (c - T0) / (T1 - T0)
    cv2.rectangle(f, (x0, y - 34), (x1, y + 34), C((252, 248, 238)), -1, cv2.LINE_AA)
    col = np.zeros((1, x1 - x0, 3), np.float32)
    for i in range(x1 - x0):
        c = T0 + (T1 - T0) * i / (x1 - x0); k = clamp((c + 24) / 58)
        col[0, i] = np.array(_mix((96, 156, 226), (244, 184, 110), k), np.float32) / 255
    f[y - 30:y + 30, x0:x1] = cv2.resize(col, (x1 - x0, 60))
    cv2.rectangle(f, (x0, y - 34), (x1, y + 34), C(INKC), 7, cv2.LINE_AA)
    if zone > 0:
        a, b = int(X(0)), int(X(10)); ov = f.copy(); cv2.rectangle(ov, (a, y - 92), (b, y + 92), C(ACC), -1, cv2.LINE_AA)
        f[:] = f * (1 - 0.72 * zone) + ov * 0.72 * zone
        cv2.rectangle(f, (a, y - 92), (b, y + 92), C(INKC), 6, cv2.LINE_AA)
    if labels:
        for c, tx in ((-20, "-20"), (0, "0"), (10, "10"), (25, "25")):
            xx = int(X(c)); cv2.line(f, (xx, y + 34), (xx, y + 50 if zone <= 0 or c not in (0, 10) else y + 92), C(INKC), 5, cv2.LINE_AA)
            comp(f, chip(f"{tx} C", INKC, MILK, 26), xx, y + 128)
    if marker is not None:
        xx = int(X(marker)); cv2.drawMarker(f, (xx, y - 62), C(INKC), cv2.MARKER_TRIANGLE_DOWN, 44, 12, cv2.LINE_AA)
    return X


def race_lanes(f, t, pos, y0=720, gap=210, x0=170, x1=900, moods=("n", "n", "n"), stale=(0, 0, 0), names=("COUNTER", "FREEZER", "FRIDGE"), cols=None, frost=(0, 0, 0)):
    """three loaves race to the STALE line. pos = 0..1 per lane. Positions are proportional to staling speed."""
    for i in range(3):
        y = y0 + i * gap
        cv2.rectangle(f, (70, y - 6), (x1 + 80, y + 104), C((250, 242, 224)), -1, cv2.LINE_AA); cv2.rectangle(f, (70, y - 6), (x1 + 80, y + 104), C(INKC), 5, cv2.LINE_AA)
        for xd in range(120, x1, 90): cv2.line(f, (xd, y + 92), (xd + 40, y + 92), C((200, 186, 160)), 4, cv2.LINE_AA)
    xf = x1 + 16; cc = 22
    for r_ in range(int((gap * 2 + 110) / cc)):
        for c_ in range(2):
            col = INKC if (r_ + c_) % 2 else (252, 248, 238)
            cv2.rectangle(f, (xf + c_ * cc, y0 - 6 + r_ * cc), (xf + (c_ + 1) * cc, y0 - 6 + (r_ + 1) * cc), C(col), -1)
    for i in range(3):
        y = y0 + i * gap; x = x0 + (x1 - 90 - x0) * clamp(pos[i])
        run = pos[i] > 0.002
        el = scale_el(loaf_el(stale[i], moods[i], (1, 0), False, frost[i]), 0.34)
        hop = abs(math.sin(t * 13 + i)) * 14 if (run and pos[i] < 0.999) else 0
        comp(f, el, x, y + 44 - hop)
        comp(f, chip(names[i], (cols or (ACC_S, BLUE_S, BLUE))[i], MILK, 28), 200, y - 30)


# ---------------- places ----------------
def _worktop_el(top_y=1330):
    def mk():
        h = H - top_y + 80; im = Image.new("RGBA", (W * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * 2 for x in v]
        d.rectangle(S(0, 0, W, 70), fill=(214, 168, 112, 255))
        d.line([(x * 2, y * 2) for x, y in _wob([(0, 2), (360, 6), (720, 0), (W, 4)], 1.5, 3)], fill=INKC + (255,), width=12)
        for x0, x1, yy in ((60, 300, 26), (420, 780, 44), (820, 1040, 22)):
            d.line(S(x0, yy, x1, yy + 3), fill=(190, 142, 90, 255), width=6)
        d.rectangle(S(0, 70, W, h), fill=(142, 170, 158, 255))
        d.line(S(0, 72, W, 72), fill=INKC + (255,), width=12)
        for x0 in (40, 400, 760):
            d.rounded_rectangle(S(x0, 106, x0 + 300, 380), 16, fill=(158, 186, 172, 255), outline=INKC + (255,), width=10)
            d.rounded_rectangle(S(x0 + 110, 150, x0 + 190, 168), 8, fill=(226, 208, 170, 255), outline=INKC + (255,), width=6)
        # a checked towel hanging on the middle drawer
        d.polygon(S(470, 106, 610, 106, 620, 300, 462, 300), fill=(240, 230, 208, 255), outline=INKC + (255,))
        for yy in (150, 200, 250): d.line(S(466, yy, 616, yy), fill=ACC + (255,), width=10)
        return np.asarray(im.resize((W, h), Image.LANCZOS)).astype(np.float32) / 255
    a = gcache(("worktop21", top_y), mk)
    return a[..., :3], a[..., 3:]


def worktop_front(f, top_y=1330):
    """the worktop edge + drawer fronts, drawn AFTER Chubby so he stands behind it."""
    rgb, al = _worktop_el(top_y); h = rgb.shape[0]; y1 = min(H, top_y + h)
    f[top_y:y1] = f[top_y:y1] * (1 - al[:y1 - top_y]) + rgb[:y1 - top_y] * al[:y1 - top_y]


def set_worktop(t=0.0, blur=4, top_y=1330):
    """the MORNING WORKTOP: pale tiled wall, a window with morning sun on the left, a shelf with jars, utensils on a rail; paper-softened."""
    def mk():
        f = _vgrad((236, 228, 206), (226, 212, 184), 0, top_y)
        for r_ in range(0, 26):
            y = 880 + r_ * 56
            if y > top_y: break
            cv2.line(f, (0, y), (W, y), C((206, 192, 166)), 3, cv2.LINE_AA)
            off = 0 if r_ % 2 else 70
            for x in range(-off, W, 140): cv2.line(f, (x, y), (x, y + 56), C((206, 192, 166)), 3, cv2.LINE_AA)
        cv2.rectangle(f, (70, 300), (500, 820), C((134, 100, 68)), -1, cv2.LINE_AA)
        f[330:790, 100:470] = _vgrad((206, 232, 250), (252, 240, 210), 330, 790)[330:790, 100:470]
        cv2.line(f, (285, 330), (285, 790), C((134, 100, 68)), 12, cv2.LINE_AA); cv2.line(f, (100, 560), (470, 560), C((134, 100, 68)), 12, cv2.LINE_AA)
        cv2.circle(f, (190, 440), 46, C((255, 244, 196)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (600, 620), (1010, 644), C((150, 112, 78)), -1, cv2.LINE_AA)
        for (x, hh, c) in ((650, 110, (214, 150, 74)), (750, 80, (232, 214, 170)), (850, 130, (120, 170, 120)), (950, 90, (214, 96, 80))):
            cv2.rectangle(f, (x - 34, 620 - hh), (x + 34, 620), C(c), -1, cv2.LINE_AA); cv2.rectangle(f, (x - 38, 620 - hh - 16), (x + 38, 620 - hh), C((130, 96, 66)), -1, cv2.LINE_AA)
        cv2.line(f, (600, 790), (1010, 790), C((120, 110, 100)), 8, cv2.LINE_AA)
        for x, l_ in ((660, 90), (770, 120), (880, 80), (970, 110)): cv2.line(f, (x, 790), (x, 790 + l_), C((110, 96, 84)), 10, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_worktop21", blur, top_y), mk).copy()
    god_rays(f, 190, 440, t, (255, 238, 196), 0.15, 7, 1400, 0.8, 0.9, 5)
    glow(f, 190, 440, 300, (255, 240, 204), 0.28)
    dust_motes(f, t, 200, 400, 900, 1200, 16, 8, 0.4)
    return inkify(f)


def set_crumb(t=0.0, stale=0.0, zoom=1.0, tint=None):
    """INSIDE A SLICE OF BREAD: a sponge-world of cream walls and dark pores, blurred far layer + sharp near pores, slow drift; stale = paler, duller."""
    stale = round(clamp(stale) * 4) / 4
    def mk():
        f = _vgrad(_mix((250, 232, 190), STALE_C, stale), _mix((236, 208, 158), STALE_S, stale), 0, H)
        rng = np.random.default_rng(3)
        for i in range(46):
            x, y = rng.uniform(0, W), rng.uniform(0, H); rx = rng.uniform(26, 90); ry = rx * rng.uniform(0.55, 1.0); a = rng.uniform(0, 180)
            cv2.ellipse(f, (int(x), int(y)), (int(rx), int(ry)), a, 0, 360, C(_mix((236, 208, 160), STALE_C, stale)), -1, cv2.LINE_AA)
        f = _soft(f, 9)
        for i in range(16):
            x, y = rng.uniform(0, W), rng.uniform(0, H); rx = rng.uniform(40, 120); ry = rx * rng.uniform(0.6, 1.0); a = rng.uniform(0, 180)
            if y < 1400 and 60 < x < 1020: continue
            cv2.ellipse(f, (int(x), int(y)), (int(rx + 6), int(ry + 6)), a, 0, 360, C(INKC), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(x), int(y)), (int(rx), int(ry)), a, 0, 360, C(_mix((176, 130, 82), STALE_S, stale * 0.7)), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(x), int(y + ry * 0.2)), (int(rx * 0.72), int(ry * 0.66)), a, 0, 360, C(_mix((120, 84, 50), (120, 108, 88), stale)), -1, cv2.LINE_AA)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("set_crumb21", stale), mk).copy()
    f = cam(f, zoom + 0.02 * math.sin(t * 0.5), 540, 960, 8 * math.sin(t * 0.4), 6 * math.cos(t * 0.3))
    return inkify(f, 0.1)
