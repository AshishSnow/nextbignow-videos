# ================= anim_props_lib22.py (ep 22, 3 Nov): the DIWALI NAMKEEN ink props + the PARALLAX DIWALI LANE + the DIWALI ROOM.
# ONE accent per video: RANI PINK = gift box, titles, chips; WATER BLUE = the water (story role); namkeen = its natural fried gold. Props: chakli_el (spiral, soft = droops + goes pale), sev_el, mathri_el,
# cracker_el, barfi_ink_el (dry = cracked), cookie_el, drop_el (a water drop with a face), cloud_el (humid air), straw_el, giftbox (front view, lid lifts), gift_top (top view with compartments), jar_ink_el
# (airtight clip jar), oven_ink_el, kadai_el, paint_el, crayon_el; live: fly_drops, strand (ink noodle), thirst_meter (the 0-1 water-activity plank he can WALK on), glass_rubber (starch: stiff rows <-> loose + wet),
# tank_pair (water levels evening out), stink. Places: set_lane(t, camx) + lane_front (a Diwali lane at dusk in 4 parallax layers), set_droom + table_front.
ACC = (214, 54, 112); ACC_S = (150, 26, 78); ACC_L = (248, 170, 198); ACC_XL = (252, 224, 234)
N_G = (228, 170, 84); N_S = (176, 116, 44); N_SOFT = (216, 196, 152); N_SOFT_S = (172, 150, 110); WATER = (110, 176, 236); WATER_S = (54, 116, 190)
SCHEMES["rosep"] = ((248, 216, 222), (254, 240, 240), (244, 204, 214), (0.9, 0.68, 0.74))
SCHEMES["wetp"] = ((186, 220, 244), (232, 246, 252), (170, 208, 238), (0.56, 0.72, 0.86))
SCHEMES["dryp"] = ((246, 220, 170), (254, 240, 206), (240, 208, 150), (0.9, 0.76, 0.5))
SCHEMES["plum"] = ((70, 40, 84), (150, 86, 130), (60, 34, 76), (0.34, 0.2, 0.36))


def _mix22(a, b, k): return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


def chakli_el(mood=None, soft=0.0, look=(0, 0), seed=1):
    """a chakli / murukku: a ridged fried spiral. soft 0..1: paler + the whole disc droops at its edges like a wet cloth."""
    soft = round(clamp(soft) * 5) / 5
    def mk():
        w, h = 340, 360; im, d, S = _cv(w, h); cx, cy = 170, 165
        col = _mix22(N_G, N_SOFT, soft); dark = _mix22(N_S, N_SOFT_S, soft)
        wr = lambda x, y: (x, y + soft * 0.0042 * (x - cx) ** 2 + soft * 10)
        P = []
        for i in range(120):
            a = i * 0.145; r = 36 + i * 1.02 + 3 * math.sin(i * 0.9)
            P.append(wr(cx + r * math.cos(a), cy + r * math.sin(a)))
        Q = [(x * SC3, y * SC3) for x, y in _wob(P, 0.9, seed)]
        d.line(Q, fill=INKC + (255,), width=44 * SC3 // 1, joint="curve")
        d.line(Q, fill=dark + (255,), width=30 * SC3, joint="curve")
        d.line(Q, fill=col + (255,), width=22 * SC3, joint="curve")
        for i in range(2, 118, 3):                                                       # the ridges
            x, y = P[i]; x2, y2 = P[i + 1]; a = math.atan2(y2 - y, x2 - x) + 1.5
            d.line(S(x - 9 * math.cos(a), y - 9 * math.sin(a), x + 9 * math.cos(a), y + 9 * math.sin(a)), fill=dark + (255,), width=3 * SC3)
        if mood:
            _ink_ell(d, *wr(cx, cy), 52, 50, _mix22(col, (255, 244, 220), 0.45), seed + 3, INK_W - 2)
            fx, fy = wr(cx, cy); _face(d, S, fx, fy, 1.15, mood, look)
        return _done(im, w, h)
    return gcache(("chakli22", mood, soft, look, seed), mk)


def sev_el(soft=0.0, seed=2):
    soft = round(clamp(soft) * 3) / 3
    def mk():
        w, h = 240, 150; im, d, S = _cv(w, h); rng = np.random.default_rng(seed); col = _mix22(N_G, N_SOFT, soft)
        for i in range(46):
            x0, y0 = rng.uniform(26, 214), rng.uniform(36, 130); a = rng.uniform(-0.8, 0.8); L = rng.uniform(40, 90)
            pts = [(x0 + j / 5 * L * math.cos(a), y0 + j / 5 * L * math.sin(a) + 6 * math.sin(j * 1.6 + i)) for j in range(6)]
            Q = [(x * SC3, y * SC3) for x, y in pts]
            d.line(Q, fill=INKC + (255,), width=9 * SC3, joint="curve"); d.line(Q, fill=col + (255,), width=5 * SC3, joint="curve")
        return _done(im, w, h)
    return gcache(("sev22", soft, seed), mk)


def mathri_el(soft=0.0, mood=None, seed=3):
    soft = round(clamp(soft) * 3) / 3
    def mk():
        w, h = 200, 200; im, d, S = _cv(w, h); col = _mix22((238, 196, 120), N_SOFT, soft)
        _ink_ell(d, 100, 100, 82, 78, col, seed, INK_W - 1)
        _shade(im, lambda q, S_: q.ellipse(S_(18, 22, 182, 178), fill=255), lambda q, S_, c: q.ellipse(S_(60, 60, 200, 200), fill=c), _mix22(N_S, N_SOFT_S, soft), 90)
        rng = np.random.default_rng(seed)
        for i in range(12):
            a, r = rng.uniform(0, 6.28), rng.uniform(10, 60); d.ellipse(S(100 + r * math.cos(a) - 4, 100 + r * math.sin(a) - 4, 100 + r * math.cos(a) + 4, 100 + r * math.sin(a) + 4), fill=INKC + (200,))
        if mood: _face(d, S, 100, 100, 1.2, mood)
        return _done(im, w, h)
    return gcache(("mathri22", soft, mood, seed), mk)


def cracker_el(mood=None, soft=0.0, seed=4):
    soft = round(clamp(soft) * 3) / 3
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h); col = _mix22((240, 208, 146), N_SOFT, soft)
        P = [(26 + j * 30.5, 26 + 5 * ((j + 1) % 2)) for j in range(7)] + [(214 - 5 * (j % 2), 26 + j * 31) for j in range(1, 7)] + [(214 - j * 31, 214 - 5 * (j % 2)) for j in range(1, 7)] + [(26 + 5 * (j % 2), 214 - j * 31) for j in range(1, 6)]
        _ink_poly(d, P, col, seed, INK_W - 1, amp=1.0)
        for x in range(60, 200, 40):
            for y in range(60, 200, 40): d.ellipse(S(x - 5, y - 5, x + 5, y + 5), fill=N_S + (255,))
        if mood:
            d.ellipse(S(70, 70, 170, 170), fill=col + (255,)); _face(d, S, 120, 120, 1.3, mood)
        return _done(im, w, h)
    return gcache(("cracker22", mood, soft, seed), mk)


def barfi_ink_el(mood=None, dry=0.0, look=(0, 0), seed=5):
    """a diamond of barfi: pale milk fudge + pistachio dust; dry = cracks + duller."""
    dry = round(clamp(dry) * 4) / 4
    def mk():
        w, h = 260, 220; im, d, S = _cv(w, h); col = _mix22((255, 246, 226), (226, 214, 188), dry)
        _ink_poly(d, [(130, 186), (246, 110), (246, 134), (130, 208), (14, 134), (14, 110)], _mix22(col, (214, 190, 150), 0.5), seed, INK_W - 1)
        _ink_poly(d, [(130, 24), (246, 110), (130, 186), (14, 110)], col, seed + 1, INK_W - 1)
        rng = np.random.default_rng(seed)
        for i in range(16):
            a, r = rng.uniform(0, 6.28), rng.uniform(4, 54); x, y = 130 + r * 1.4 * math.cos(a), 104 + r * 0.8 * math.sin(a)
            d.ellipse(S(x - 3, y - 3, x + 3, y + 3), fill=(120, 170, 92, 255))
        if dry > 0.2:
            for (x0, y0, a) in ((60, 92, 30), (200, 94, 150), (130, 170, -90), (128, 34, 90)):
                pts = [(x0, y0)]; L = 60 * dry; aa = math.radians(a)
                for k in range(4): pts.append((pts[-1][0] + L / 4 * math.cos(aa) + 5 * (-1) ** k * math.sin(aa), pts[-1][1] + L / 4 * math.sin(aa) + 5 * (-1) ** k * math.cos(aa)))
                d.line([(x * SC3, y * SC3) for x, y in pts], fill=INKC + (200,), width=3 * SC3, joint="curve")
        if mood: _face(d, S, 130, 104, 1.05, mood, look)
        return _done(im, w, h)
    return gcache(("barfi22", mood, dry, look, seed), mk)


def cookie_el(kind="crisp", mood=None, change=0.0, seed=6):
    """kind 'crisp' (flat, cracked gingersnap), 'soft' (fat + chips). change 0..1: crisp -> droopy, soft -> dry + cracked."""
    change = round(clamp(change) * 4) / 4
    def mk():
        w, h = 240, 240; im, d, S = _cv(w, h)
        col = (204, 134, 70) if kind == "crisp" else (236, 196, 136)
        col = _mix22(col, (214, 180, 130), change) if kind == "crisp" else _mix22(col, (208, 186, 150), change)
        yy = (10 * change) if kind == "crisp" else 0
        _ink_ell(d, 120, 120 + yy, 96, 92 - yy * 2, col, seed, INK_W - 1)
        rng = np.random.default_rng(seed)
        if kind == "crisp":
            if change < 0.5:
                for (x0, y0, x1, y1) in ((60, 92, 92, 110), (150, 70, 178, 96), (80, 170, 116, 150)): d.line(S(x0, y0, x1, y1), fill=INKC + (200,), width=3 * SC3)
        else:
            for i in range(9):
                a, r = rng.uniform(0, 6.28), rng.uniform(24, 72); x, y = 120 + r * math.cos(a), 120 + r * math.sin(a)
                d.ellipse(S(x - 8, y - 7, x + 8, y + 7), fill=(92, 56, 36, 255))
            if change > 0.4:
                for (x0, y0, x1, y1) in ((50, 110, 96, 130), (170, 70, 140, 116), (116, 200, 130, 150)): d.line(S(x0, y0, x1, y1), fill=INKC + (220,), width=3 * SC3)
        if mood:
            d.ellipse(S(76, 76, 164, 164), fill=col + (255,)); _face(d, S, 120, 120, 1.05, mood)
        return _done(im, w, h)
    return gcache(("cookie22", kind, mood, change, seed), mk)


def drop_el(mood="happy", look=(0, 0), seed=7):
    def mk():
        w, h = 160, 200; im, d, S = _cv(w, h)
        P = [(80, 12)] + [(80 + 60 * math.sin(a * 3.14 / 12), 118 - 60 * math.cos(a * 3.14 / 12) + (0 if a > 3 else (12 - a * 4))) for a in range(1, 24)]
        _ink_poly(d, P, WATER, seed, INK_W - 1, amp=1.0)
        d.line(S(52, 104, 46, 134), fill=(235, 248, 255, 255), width=6 * SC3)
        if mood: _face(d, S, 84, 124, 1.0, mood, look)
        return _done(im, w, h)
    return gcache(("drop22", mood, look, seed), mk)


def cloud_el(mood="n", n=7, seed=8):
    def mk():
        w, h = 420, 280; im, d, S = _cv(w, h); col = (226, 240, 250)
        for (x, y, r) in ((110, 150, 78), (200, 110, 92), (300, 140, 84), (210, 180, 84)): d.ellipse(S(x - r - 3, y - r - 3, x + r + 3, y + r + 3), fill=INKC + (255,))
        for (x, y, r) in ((110, 150, 73), (200, 110, 87), (300, 140, 79), (210, 180, 79)): d.ellipse(S(x - r + 2, y - r + 2, x + r - 2, y + r - 2), fill=col + (255,))
        rng = np.random.default_rng(seed)
        for i in range(n):
            a, r = rng.uniform(0, 6.28), rng.uniform(70, 110); x, y = 205 + r * 1.3 * math.cos(a), 145 + r * 0.7 * math.sin(a)
            d.ellipse(S(x - 8, y - 11, x + 8, y + 11), fill=WATER + (255,), outline=INKC + (255,), width=2 * SC3)
        if mood: _face(d, S, 205, 138, 1.5, mood)
        return _done(im, w, h)
    return gcache(("cloud22", mood, n, seed), mk)


def straw_el():
    def mk():
        w, h = 90, 340; im, d, S = _cv(w, h)
        _ink_poly(d, [(30, 110), (56, 110), (56, 330), (30, 330)], (255, 250, 244), 3, INK_W - 3, amp=0.6)
        for y in range(120, 330, 34): d.polygon(S(31, y, 55, y + 12, 55, y + 26, 31, y + 14), fill=ACC + (255,))
        _ink_poly(d, [(30, 110), (56, 110), (84, 40), (84, 10), (62, 10), (62, 36)], (255, 250, 244), 4, INK_W - 3, amp=0.6)
        return _done(im, w, h)
    return gcache(("straw22",), mk)


def _box_front_el(soft=0.0):
    soft = round(clamp(soft) * 3) / 3
    def mk():
        w, h = 520, 420; im, d, S = _cv(w, h)
        _ink_poly(d, [(50, 110), (470, 110), (450, 150), (70, 150)], (96, 40, 66), 11, INK_W - 1)
        for el, x_, y_ in ((chakli_el(None, soft, seed=2), 150, 74), (mathri_el(soft), 262, 96), (sev_el(soft), 372, 96), (chakli_el(None, soft, seed=5), 300, 62)):
            pm, a = el; ss = 0.46 if el[1].shape[0] > 300 else 0.62
            arr = np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-3), 0, 1), a]); pil = Image.fromarray((arr * 255).astype(np.uint8), "RGBA")
            pil = pil.resize((int(pil.width * ss * SC3), int(pil.height * ss * SC3)), Image.LANCZOS); im.alpha_composite(pil, (int((x_ - pil.width / SC3 / 2) * SC3), int((y_ - 0) * SC3 - pil.height / 3)))
        _ink_poly(d, [(36, 150), (484, 150), (466, 404), (54, 404)], ACC, 12, INK_W)
        _shade(im, lambda q, S_: q.polygon(S_(36, 150, 484, 150, 466, 404, 54, 404), fill=255), lambda q, S_, c: q.polygon(S_(300, 150, 500, 150, 500, 420, 260, 420), fill=c), ACC_S, 130)
        for x in range(90, 460, 90):
            for y in (210, 300):
                d.polygon(S(x, y - 26, x + 20, y, x, y + 26, x - 20, y), fill=(248, 206, 110, 255), outline=INKC + (255,))
        d.rectangle(S(46, 348, 474, 366), fill=(248, 206, 110, 255))
        return _done(im, w, h)
    return gcache(("boxfront22", soft), mk)


def _box_lid_el():
    def mk():
        w, h = 560, 120; im, d, S = _cv(w, h)
        _ink_poly(d, [(16, 24), (544, 24), (536, 100), (24, 100)], ACC, 13, INK_W)
        d.rectangle(S(250, 26, 310, 98), fill=(248, 206, 110, 255))
        _ink_poly(d, [(280, 26), (220, 2), (232, 40)], (248, 206, 110), 14, INK_W - 2, amp=0.6); _ink_poly(d, [(280, 26), (340, 2), (328, 40)], (248, 206, 110), 15, INK_W - 2, amp=0.6)
        return _done(im, w, h)
    return gcache(("boxlid22",), mk)


def giftbox(f, x, y, s=1.0, lid=0.0, soft=0.0, t=0.0):
    """front view of a Diwali gift box; (x, y) = bottom centre. lid 0 = closed, 1 = lifted + tilted away."""
    comp(f, scale_el(_box_front_el(soft), s), x, y - 210 * s)
    lk = clamp(lid); ly = y - 390 * s - 200 * s * lk; lx = x + 170 * s * lk
    rot_comp(f, scale_el(_box_lid_el(), s), lx, ly, -24 * lk, 1.0, 1.0, 0.0)


def gift_top(f, cx, cy, w=820, h=460, soft=0.0, dry=0.0, t=0.0, wall=True, moods=(None, None), wall_k=1.0):
    """top view of the Diwali box: namkeen compartment on the left, barfi on the right; soft / dry = what the water has done."""
    x0, y0, x1, y1 = int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)
    cv2.rectangle(f, (x0 + 10, y0 + 14), (x1 + 10, y1 + 14), C((110, 70, 70)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(ACC), -1, cv2.LINE_AA); cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 8, cv2.LINE_AA)
    m = 26; cv2.rectangle(f, (x0 + m, y0 + m), (x1 - m, y1 - m), C((252, 240, 214)), -1, cv2.LINE_AA); cv2.rectangle(f, (x0 + m, y0 + m), (x1 - m, y1 - m), C(INKC), 5, cv2.LINE_AA)
    xm = int(cx)
    if wall: cv2.line(f, (xm, y0 + m), (xm, y1 - m), C(INKC), 10, cv2.LINE_AA); cv2.line(f, (xm, y0 + m), (xm, y1 - m), C(ACC_L), 5, cv2.LINE_AA)
    lx = cx - w / 4; rx = cx + w / 4; sc_ = h / 460
    comp(f, scale_el(chakli_el(moods[0], soft, seed=1), 0.56 * sc_), lx - 68 * sc_, cy - 52 * sc_); comp(f, scale_el(mathri_el(soft), 0.62 * sc_), lx + 92 * sc_, cy - 76 * sc_); comp(f, scale_el(sev_el(soft), 0.86 * sc_), lx + 30 * sc_, cy + 110 * sc_)
    for (dx, dy, md) in ((-90, -96, None), (90, -96, None), (-90, 96, None), (90, 96, moods[1])):
        comp(f, scale_el(barfi_ink_el(md, dry), 0.66 * sc_), rx + dx * sc_, cy + dy * sc_)
    return (lx, cy), (rx, cy)


def jar_ink_el(lid=1.0, kind="namkeen", soft=0.0):
    """an airtight glass jar with a clip lid; lid 1 = shut + clipped."""
    lid = round(clamp(lid) * 4) / 4; soft = round(clamp(soft) * 3) / 3
    def mk():
        w, h = 400, 560; im, d, S = _cv(w, h)
        yl = 96 - 70 * (1 - lid); xl = 22 * (1 - lid)
        d.rounded_rectangle(S(50, 130, 350, 530), 34 * SC3, fill=(232, 244, 250, 150))
        if kind == "namkeen":
            for el, x_, y_, ss in ((chakli_el(None, soft, seed=1), 140, 400, 0.5), (mathri_el(soft), 262, 420, 0.62), (chakli_el(None, soft, seed=2), 230, 300, 0.5), (sev_el(soft), 120, 262, 0.7)):
                pm, a = el; arr = np.dstack([np.clip(pm / np.maximum(a[..., None], 1e-3), 0, 1), a]); pil = Image.fromarray((arr * 255).astype(np.uint8), "RGBA")
                pil = pil.resize((int(pil.width * ss * SC3), int(pil.height * ss * SC3)), Image.LANCZOS); im.alpha_composite(pil, (int(x_ * SC3 - pil.width / 2), int(y_ * SC3 - pil.height / 2)))
        d.rounded_rectangle(S(50, 130, 350, 530), 34 * SC3, outline=INKC + (255,), width=INK_W * SC3)
        d.line(S(84, 170, 76, 400), fill=(255, 255, 255, 230), width=9 * SC3)
        _ink_poly(d, [(66 + xl, yl), (334 + xl, yl), (340 + xl, yl + 40), (60 + xl, yl + 40)], (240, 236, 226), 7, INK_W - 1, amp=0.8)
        d.line(S(36 + xl * 0.3, yl + 56, 362 + xl * 0.3, yl + 56), fill=INKC + (255,), width=(4 if lid > 0.9 else 1) * SC3)
        if lid > 0.9:
            d.rounded_rectangle(S(170, yl + 28, 230, yl + 84), 8 * SC3, fill=(190, 200, 208, 255), outline=INKC + (255,), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("jar22", lid, kind, soft), mk)


def oven_ink_el(on=0.0):
    on = round(clamp(on) * 3) / 3
    def mk():
        w, h = 600, 440; im, d, S = _cv(w, h)
        _ink_poly(d, [(16, 24), (584, 24), (584, 410), (16, 410)], (206, 208, 206), 3, INK_W, amp=1.0)
        _ink_poly(d, [(46, 60), (460, 60), (460, 380), (46, 380)], (46, 34, 30), 4, INK_W - 1, amp=0.8)
        d.rectangle(S(60, 72, 446, 368), fill=_mix22((70, 54, 46), (250, 148, 64), on) + (255,))
        for y in (160, 280): d.line(S(62, y, 444, y), fill=INKC + (220,), width=3 * SC3)
        for (y, c) in ((110, (240, 90, 60)), (210, (90, 90, 90)), (310, (90, 90, 90))):
            d.ellipse(S(490, y - 30, 550, y + 30), fill=c + (255,) if on or y != 110 else (150, 150, 150, 255), outline=INKC + (255,), width=5 * SC3); d.line(S(520, y - 22, 520, y), fill=INKC + (255,), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("oven22", on), mk)


def kadai_el():
    def mk():
        w, h = 620, 300; im, d, S = _cv(w, h)
        P = _arcpts(310, 40, 270, 240, 0, 180, 30)
        _ink_poly(d, P, (60, 54, 54), 6, INK_W + 1, amp=1.0)
        _ink_poly(d, _arcpts(310, 60, 240, 200, 0, 180, 24), (240, 170, 60), 7, INK_W - 3, amp=0.6)
        d.rectangle(S(60, 30, 560, 60), fill=(0, 0, 0, 0))
        _ink_poly(d, [(14, 34), (48, 24), (56, 48), (20, 60)], (60, 54, 54), 8, INK_W - 2, amp=0.5); _ink_poly(d, [(606, 34), (572, 24), (564, 48), (600, 60)], (60, 54, 54), 9, INK_W - 2, amp=0.5)
        return _done(im, w, h)
    return gcache(("kadai22",), mk)


def paint_el():
    def mk():
        w, h = 240, 280; im, d, S = _cv(w, h)
        _ink_poly(d, [(34, 60), (206, 60), (196, 260), (44, 260)], (196, 200, 206), 3, INK_W - 1, amp=0.8)
        _ink_ell(d, 120, 60, 86, 22, (120, 170, 110), 4, INK_W - 1)
        d.line(S(70, 60, 62, 150), fill=(120, 170, 110, 255), width=16 * SC3); d.ellipse(S(52, 144, 72, 168), fill=(120, 170, 110, 255))
        d.arc(S(30, 10, 210, 150), 180, 360, fill=INKC + (255,), width=5 * SC3)
        return _done(im, w, h)
    return gcache(("paint22",), mk)


def crayon_el(col=(236, 120, 60)):
    def mk():
        w, h = 80, 260; im, d, S = _cv(w, h)
        _ink_poly(d, [(40, 8), (64, 52), (64, 250), (16, 250), (16, 52)], col, 5, INK_W - 2, amp=0.6)
        d.rectangle(S(18, 84, 62, 212), fill=_mix22(col, (255, 255, 255), 0.5) + (255,)); d.line(S(16, 84, 64, 84), fill=INKC + (255,), width=4 * SC3); d.line(S(16, 212, 64, 212), fill=INKC + (255,), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("crayon22", tuple(col)), mk)


def stink(f, x, y, t, n=3, h=220, col=(120, 150, 70)):
    for i in range(n):
        xx = x + (i - (n - 1) / 2) * 62; pts = []
        for j in range(12):
            k = j / 11; yy = y - h * k; pts.append((xx + 22 * math.sin(k * 7 + t * 4 + i * 2), yy))
        A = np.array(pts, np.int32)
        cv2.polylines(f, [A], False, C(INKC), 14, cv2.LINE_AA); cv2.polylines(f, [A], False, C(col), 8, cv2.LINE_AA)


def strand(f, pts, w=14, col=(244, 214, 120), ink=INKC):
    A = np.array(pts, np.int32)
    cv2.polylines(f, [A], False, C(ink), int(w + 8), cv2.LINE_AA); cv2.polylines(f, [A], False, C(col), int(w), cv2.LINE_AA)


def fly_drops(f, src, dst, t, n=9, rate=0.7, seed=3, s=0.26, arc=-120, mood=None, op=1.0, end_shrink=True):
    """a stream of little water drops travelling src -> dst on an arc (ARCS, ep 22)."""
    rng = np.random.default_rng(seed)
    el = scale_el(drop_el(mood), s)
    for i in range(n):
        p = (t * rate + i / n + rng.uniform(0, 0.03)) % 1.0
        sp = rng.uniform(-60, 60)
        x = src[0] + (dst[0] - src[0]) * p + sp * math.sin(p * 3.14)
        y = src[1] + (dst[1] - src[1]) * p + arc * 4 * p * (1 - p)
        sc_ = (0.5 + 0.5 * math.sin(min(1, p * 5) * 1.57)) * (1 - 0.5 * p if end_shrink else 1)
        comp(f, el, x, y, scale=sc_, op=op)


def thirst_meter(f, t, y=1270, x0=100, x1=980, h=62, band=0.0, title=True, labels=True):
    """the water-activity scale as a plank Chubby can WALK on: sandy = thirsty (0), blue = wet (1). Returns X(v). y = the plank top = his feet."""
    X = lambda v: x0 + (x1 - x0) * v
    n = 60
    for i in range(n):
        k = i / n; c = _mix22((240, 198, 120), WATER, k)
        cv2.rectangle(f, (int(x0 + (x1 - x0) * k), y), (int(x0 + (x1 - x0) * (k + 1 / n)) + 1, y + h), C(c), -1)
    if band > 0:
        ov = f.copy(); cv2.rectangle(ov, (int(X(0.35)), y - 8), (int(X(0.35 + 0.15 * clamp(band))), y + h + 8), C((206, 50, 60)), -1, cv2.LINE_AA); f[:] = f * 0.25 + ov * 0.75
    cv2.rectangle(f, (x0, y), (x1, y + h), C(INKC), 7, cv2.LINE_AA)
    for j in range(11):
        xx = int(X(j / 10)); cv2.line(f, (xx, y + h), (xx, y + h + (26 if j % 5 == 0 else 14)), C(INKC), 5, cv2.LINE_AA)
    if labels:
        comp(f, chip("0", INKC, MILK, 30), x0 + 2, y + h + 58); comp(f, chip("1", INKC, MILK, 30), x1 - 2, y + h + 58)
        comp(f, chip("THIRSTY", N_S, MILK, 24), x0 + 100, y + h + 58); comp(f, chip("WET", WATER_S, MILK, 24), x1 - 76, y + h + 58)
    return X


def glass_rubber(f, cx, cy, k, t, w=680, h=440, n=7, drops=True, shake=0.0):
    """starch at molecule scale. k = 0: stiff straight rows packed tight (glassy: it breaks). k = 1: water drops between them, the same rows wavy + loose (rubbery: it bends)."""
    k = clamp(k); px0, px1, py0, py1 = int(cx - w / 2 - 36), int(cx + w / 2 + 36), int(cy - h / 2 - 30), int(cy + h / 2 + 30)
    ov = f.copy(); cv2.rectangle(ov, (px0, py0), (px1, py1), C((254, 248, 232)), -1, cv2.LINE_AA); f[:] = f * 0.1 + ov * 0.9
    cv2.rectangle(f, (px0, py0), (px1, py1), C(INKC), 7, cv2.LINE_AA)
    gap0, gap1 = 46, h / n
    for i in range(n):
        y0 = cy + (i - (n - 1) / 2) * (gap0 + (gap1 - gap0) * eio(k)); amp = 22 * k + 0.0; ph = i * 1.4 + t * 2.4 * k
        P = [(cx - w / 2 + j * w / 24 + shake * math.sin(t * 50 + i), y0 + amp * math.sin(j * 0.8 + ph)) for j in range(25)]
        strand(f, P, 14, _mix22((232, 182, 96), (240, 214, 150), k))
    if drops and k > 0:
        rng = np.random.default_rng(5); m = int(16 * k)
        for i in range(m):
            rr = i % (n - 1); xt = cx - w / 2 + 40 + ((i * 5.3) % 13) * (w - 80) / 13; yt = cy + (rr - (n - 2) / 2) * (gap0 + (gap1 - gap0) * eio(k))
            yy = yt + 5 * math.sin(t * 2 + i); r_ = 13
            cv2.circle(f, (int(xt), int(yy)), r_ + 3, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(xt), int(yy)), r_, C(WATER), -1, cv2.LINE_AA); cv2.circle(f, (int(xt - 4), int(yy - 4)), 3, C((240, 250, 255)), -1, cv2.LINE_AA)


def tank_pair(f, t, k, cx=540, cy=1040, gap=420, w=330, hh=420, lab=("MORE", "LESS"), even=False):
    """two tanks joined by a pipe. k 0..1: the water levels even out, drops cross the pipe (moisture flows from more to less)."""
    k = clamp(k); xa, xb = cx - gap / 2, cx + gap / 2; lv_a = 0.86 + (0.5 - 0.86) * eio(k); lv_b = 0.14 + (0.5 - 0.14) * eio(k); y1 = cy + hh / 2; y0 = cy - hh / 2
    for (xx, lv) in ((xa, lv_a), (xb, lv_b)):
        cv2.rectangle(f, (int(xx - w / 2), int(y0)), (int(xx + w / 2), int(y1)), C((246, 250, 252)), -1, cv2.LINE_AA)
        ty = y1 - hh * lv; xs = np.arange(int(xx - w / 2), int(xx + w / 2)); yw = ty + 7 * np.sin(xs * 0.05 + t * 5)
        pts = np.vstack([np.stack([xs, yw], 1), [[xs[-1], y1], [xs[0], y1]]]).astype(np.int32)
        cv2.fillPoly(f, [pts], C(WATER), cv2.LINE_AA)
    pipe_y = int(y1 - 56)
    cv2.rectangle(f, (int(xa + w / 2 - 8), pipe_y - 26), (int(xb - w / 2 + 8), pipe_y + 26), C(WATER), -1, cv2.LINE_AA)
    cv2.line(f, (int(xa + w / 2), pipe_y - 30), (int(xb - w / 2), pipe_y - 30), C(INKC), 7, cv2.LINE_AA); cv2.line(f, (int(xa + w / 2), pipe_y + 30), (int(xb - w / 2), pipe_y + 30), C(INKC), 7, cv2.LINE_AA)
    for xx in (xa, xb): cv2.rectangle(f, (int(xx - w / 2), int(y0)), (int(xx + w / 2), int(y1)), C(INKC), 8, cv2.LINE_AA)
    if 0.02 < k < 0.98:
        for j in range(4):
            p = (t * 1.3 + j / 4) % 1; xx = xa + w / 2 - 20 + (gap - w + 40) * p
            draw_arrow(f, xx - 14, pipe_y, xx + 14, pipe_y, 1.0, (250, 252, 255), 6, 18)
    return xa, xb, y0


# ================= the DIWALI LANE: 4 parallax layers (skyline 0.18, houses 0.55, ground 1.0, garlands 1.7 x the camera). Depth + the walk cycle: ep 22. =================
_LW = 2160


def _lane_far():
    f = _vgrad((46, 34, 86), (246, 150, 110), 0, 1250); f = np.ascontiguousarray(f[:, :W]); f = np.tile(f, (1, 2, 1))
    rng = np.random.default_rng(7); x = 0
    while x < _LW:
        bw = int(rng.uniform(120, 230)); top = int(rng.uniform(640, 980)); c = _mix22((70, 44, 90), (120, 70, 110), rng.uniform(0, 1))
        cv2.rectangle(f, (x, top), (x + bw, 1300), C(c), -1)
        for wx in range(x + 22, x + bw - 26, 46):
            for wy in range(top + 26, 1250, 60):
                if rng.uniform(0, 1) < 0.55: cv2.rectangle(f, (wx, wy), (wx + 22, wy + 30), C((255, 214, 130)), -1)
        x += bw
    for x0 in range(0, _LW, 360):                                                       # string lights between roofs
        for j in range(19):
            k = j / 18; xx = x0 + 360 * k; yy = 650 + 60 * math.sin(3.14 * k) + 16 * math.sin(x0)
            cv2.circle(f, (int(xx), int(yy)), 7, C(((255, 214, 110), (248, 120, 170), (120, 220, 200))[j % 3]), -1, cv2.LINE_AA)
    return np.clip(_soft(f, 5), 0, 1).astype(np.float32)


def _lane_mid():
    im, d, S = _cv(_LW, H, 1); rng = np.random.default_rng(11); x = 40; pal = [(244, 196, 180), (170, 214, 200), (246, 214, 150), (226, 186, 214)]; i = 0
    while x < _LW - 300:
        bw = int(rng.uniform(320, 440)); top = int(rng.uniform(800, 900)); c = pal[i % 4]; i += 1; yb = 1450
        _ink_poly(d, [(x, top), (x + bw, top), (x + bw, yb), (x, yb)], c, i, 6, 1, amp=1.2)
        d.rectangle([x - 12, top - 22, x + bw + 12, top + 4], fill=(150, 96, 80, 255), outline=INKC + (255,), width=5)
        dx = x + bw // 2 - 62
        d.rectangle([dx, yb - 280, dx + 124, yb], fill=(120, 74, 56, 255), outline=INKC + (255,), width=6)
        d.ellipse([dx + 96, yb - 150, dx + 112, yb - 134], fill=(240, 210, 130, 255))
        for k in range(9):                                                               # toran over the door
            tx = dx - 20 + k * 20; d.polygon([tx, yb - 296, tx + 18, yb - 296, tx + 9, yb - 268], fill=(246, 150, 50, 255) if k % 2 else (120, 180, 90, 255), outline=INKC + (255,))
        for wx in (x + 26, x + bw - 96):
            if wx + 70 < dx or wx > dx + 124:
                d.rectangle([wx, top + 60, wx + 70, top + 180], fill=(255, 226, 150, 255), outline=INKC + (255,), width=5); d.line([wx + 35, top + 60, wx + 35, top + 180], fill=INKC + (255,), width=4)
        x += bw + int(rng.uniform(10, 120))
    a = np.asarray(im, np.float32) / 255
    rgb = cv2.GaussianBlur(a[..., :3], (0, 0), 1.8); al = cv2.GaussianBlur(a[..., 3], (0, 0), 1.8)
    return rgb.astype(np.float32), al.astype(np.float32)


def _lane_ground():
    f = np.ones((H - 1420, _LW, 3), np.float32) * np.array(C((176, 150, 130)), np.float32)
    for x in range(0, _LW, 180): cv2.line(f, (x, 0), (x - 60, H - 1420), C((150, 124, 106)), 3, cv2.LINE_AA)
    cv2.line(f, (0, 62), (_LW, 62), C((150, 124, 106)), 3, cv2.LINE_AA); cv2.line(f, (0, 0), (_LW, 0), C(INKC), 6, cv2.LINE_AA)
    for x0, cc in ((280, (214, 54, 112)), (1040, (246, 150, 50)), (1790, (60, 170, 150))):      # rangoli on the path
        for r_, c in ((110, cc), (84, (252, 240, 214)), (58, (246, 190, 60)), (30, cc)):
            cv2.ellipse(f, (x0, 104), (r_ * 2, int(r_ * 0.62)), 0, 0, 360, C(c), -1, cv2.LINE_AA); cv2.ellipse(f, (x0, 104), (r_ * 2, int(r_ * 0.62)), 0, 0, 360, C(INKC), 3, cv2.LINE_AA)
    return f.astype(np.float32)


def _lane_fg():
    im = Image.new("RGBA", (_LW, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for x0 in (150, 1240):                                                              # marigold garlands hanging close to the lens
        for j in range(22):
            k = j / 21; xx = x0 + 300 * k; yy = 90 + 170 * math.sin(3.14 * k)
            d.ellipse([xx - 30, yy - 30, xx + 30, yy + 30], fill=(246, 160, 40, 255) if j % 2 else (250, 196, 60, 255))
    a = np.asarray(im, np.float32) / 255
    return cv2.GaussianBlur(a[..., :3], (0, 0), 9).astype(np.float32), cv2.GaussianBlur(a[..., 3], (0, 0), 9).astype(np.float32)


def _roll(a, px):
    px = int(px) % a.shape[1]; return np.concatenate([a[:, px:px + W], a[:, : max(0, px + W - a.shape[1])]], 1)[:, :W]


def set_lane(t=0.0, camx=0.0):
    """a Diwali lane at dusk. camx = camera position in ground px; each layer scrolls at its own speed (parallax). Ground plane from y 1420; his feet belong at y ~ 1500."""
    far = gcache(("lane_far",), _lane_far); mid_rgb, mid_a = gcache(("lane_mid",), _lane_mid); gr = gcache(("lane_gr",), _lane_ground)
    f = _roll(far, camx * 0.18).copy()
    a = _roll(mid_a, camx * 0.55)[..., None]; f = f * (1 - a) + _roll(mid_rgb, camx * 0.55) * a
    f[1420:] = _roll(gr, camx)
    for j in range(12):                                                                 # diyas on the kerb, in the ground plane, alive
        xx = ((j * 180 + 90) - camx) % _LW
        if xx < W + 60:
            cv2.ellipse(f, (int(xx), 1440), (24, 12), 0, 0, 180, C((170, 90, 50)), -1, cv2.LINE_AA); cv2.ellipse(f, (int(xx), 1440), (24, 12), 0, 0, 180, C(INKC), 3, cv2.LINE_AA)
            h_ = 22 + 4 * math.sin(t * 13 + j * 2); cv2.ellipse(f, (int(xx), int(1434 - h_ / 2)), (7, int(h_ / 2)), 0, 0, 360, C((255, 214, 90)), -1, cv2.LINE_AA)
            glow(f, xx, 1424, 80, (255, 190, 90), 0.14)
    return inkify(f, 0.08)


def lane_front(f, camx=0.0):
    rgb, al = gcache(("lane_fg",), _lane_fg)
    r2 = _roll(rgb, camx * 1.7); a2 = _roll(al, camx * 1.7)[..., None]
    f[: H // 2] = f[: H // 2] * (1 - a2) + r2 * a2


def _table_el(top_y=1330):
    def mk():
        h = H - top_y + 80; im = Image.new("RGBA", (W * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * 2 for x in v]
        d.rectangle(S(0, 0, W, 60), fill=(150, 96, 66, 255)); d.line([(x * 2, y * 2) for x, y in _wob([(0, 2), (360, 6), (720, 0), (W, 4)], 1.5, 3)], fill=INKC + (255,), width=12)
        d.rectangle(S(0, 60, W, h), fill=(120, 76, 54, 255)); d.line(S(0, 62, W, 62), fill=INKC + (255,), width=12)
        d.polygon(S(150, 0, 930, 0, 950, 210, 840, 170, 720, 210, 600, 170, 480, 210, 360, 170, 240, 210, 130, 170), fill=ACC + (255,), outline=INKC + (255,))        # a pink runner
        for x in range(190, 900, 90): d.polygon(S(x, 80, x + 18, 106, x, 132, x - 18, 106), fill=(248, 206, 110, 255))
        return np.asarray(im.resize((W, h), Image.LANCZOS)).astype(np.float32) / 255
    a = gcache(("table22", top_y), mk)
    return a[..., :3], a[..., 3:]


def table_front(f, top_y=1330):
    rgb, al = _table_el(top_y); h = rgb.shape[0]; y1 = min(H, top_y + h)
    f[top_y:y1] = f[top_y:y1] * (1 - al[:y1 - top_y]) + rgb[:y1 - top_y] * al[:y1 - top_y]


def set_droom(t=0.0, blur=4, top_y=1330, dim=0.0):
    """the DIWALI ROOM at night: warm wall, a window on the dark street + lights, a shelf of live diyas, a marigold garland; one warm lamp."""
    def mk():
        f = _vgrad((244, 214, 190), (222, 170, 150), 0, top_y)
        cv2.rectangle(f, (70, 560), (470, 1030), C((120, 84, 66)), -1, cv2.LINE_AA)
        f[586:1004, 96:444] = _vgrad((40, 30, 80), (170, 96, 110), 586, 1004)[586:1004, 96:444]
        cv2.line(f, (270, 586), (270, 1004), C((120, 84, 66)), 12, cv2.LINE_AA); cv2.line(f, (96, 790), (444, 790), C((120, 84, 66)), 12, cv2.LINE_AA)
        for j in range(16):
            k = j / 15; xx = 96 + 348 * k; yy = 640 + 50 * math.sin(3.14 * k); cv2.circle(f, (int(xx), int(yy)), 8, C(((255, 214, 110), (248, 120, 170), (120, 220, 200))[j % 3]), -1, cv2.LINE_AA)
        cv2.rectangle(f, (590, 700), (1020, 726), C((130, 90, 66)), -1, cv2.LINE_AA)
        for j in range(22):
            k = j / 21; xx = 40 + 1000 * k; yy = 270 + 44 * math.sin(3.14 * k * 4) ** 2
            cv2.circle(f, (int(xx), int(yy)), 22, C((246, 160, 40) if j % 2 else (250, 196, 60)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("droom22", blur, top_y), mk).copy()
    for j, x in enumerate((650, 760, 870, 980)):
        cv2.ellipse(f, (x, 696), (32, 18), 0, 0, 180, C((170, 90, 50)), -1, cv2.LINE_AA); cv2.ellipse(f, (x, 696), (32, 18), 0, 0, 180, C(INKC), 3, cv2.LINE_AA)
        h_ = 30 + 5 * math.sin(t * 12 + j * 2); cv2.ellipse(f, (x, int(688 - h_ / 2)), (9, int(h_ / 2)), 0, 0, 360, C((255, 214, 90)), -1, cv2.LINE_AA); glow(f, x, 670, 90, (255, 190, 90), 0.1)
    if dim > 0: f = f * (1 - dim)
    return inkify(f)
