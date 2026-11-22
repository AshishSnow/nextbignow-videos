# ================= anim_props6.py = lib59 (ep 59, 22 Nov): "Do carrots improve your eyesight?" — ACCENT = CARROT ORANGE
# (the carrot, the vitamin A, the question words). Everything else stays paper / ink / mint / skin; the 1940 night is navy + searchlight cream.
# NEW CRAFT (ep 59) = THE SPINNING NEWSPAPER (a 1930s-60s film transition: a paper spins in from small and stops dead on the headline that tells
# the off-screen story). spin_paper(...) = scale ~0.12 -> 1 and N full turns that END at 0 degrees, both on the SAME ease-out over ~0.9 s (MacMost:
# scale + rotate stacked, same duration, ease out; DV Info: ~20 % -> 100 %, ~5 spins ending at 0 degrees, spin blur keyed to 0 as it stops),
# a SPIN BLUR made of rotated copies whose spread follows the angular speed (so it fades to sharp exactly when it stops), then a HOLD so the
# headline can be read; sound twin = mix.py paper_spin (a rising whirr that stops with a thump + a rustle).
# NEW PLACE: set_blitz(t) = a 1940 city at NIGHT (blacked-out rooftops + chimneys, barrage balloons, a moon, SEARCHLIGHT beams that sweep).
# Props: carrot_ink_el (ink carrot with a face, bite, DISGUISE = dark glasses + moustache + hat), newspaper_el (1940 front page), plane_ink_el
# (a generic propeller fighter, side view, no insignia; radar box in the nose shows in cut-away), radar_scope (green scope with a sweep + blips),
# vit_a_el (the vitamin A buddy), vit_tank (a glass tank of vitamin A with a FULL line), eye_beams (comic headlight eyes), pilot() (Chubby in a
# leather cap + goggles + scarf). Reused: lib58 eye_board / eye_chart_el / mom58, lib57 doctor via ep 58 doctor58 (copied in anim_shots). =================
ACC = (238, 122, 30); ACC_S = (176, 74, 8); ACC_L = (250, 186, 120); ACC_XL = (253, 228, 200)      # carrot orange
LEAF = (96, 170, 84); LEAF_S = (58, 120, 56)
NAVY = (26, 32, 58); NAVY2 = (44, 54, 92); BEAM = (252, 244, 214)
NEWS = (240, 232, 208); NEWS_S = (206, 194, 164)
SCOPE = (12, 46, 26); SCOPE_L = (90, 240, 140)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
MOM_TOP = (196, 70, 110); MOM_HAIR2 = (58, 38, 32)
LEATHER = (124, 78, 44); LEATHER_S = (86, 50, 26)
SRC_WAR = "Source: Smithsonian Magazine; Scientific American"
SRC_RADAR = "Source: Smithsonian; Scientific American; Live Science"
SRC_VITA = "Source: Scientific American; UT Austin; Smithsonian"
SRC_SHORT = "Source: Live Science; Smithsonian; UT Austin"
SRC_CHECK = "Source: Scientific American"
SC3 = 3


# ---------------- the carrot (hero prop, ink) ----------------
def carrot_ink_el(bite=0, mood=None, look=(0, 0), disguise=False, s=1.0):
    """an ink carrot standing up (tip down), leafy top; bite 0..2 = bites out of the tip end; mood = a 3-stroke face; disguise = spy look."""
    def mk():
        w, h = 200, 470; im, d, S = _cv(w, h)
        for i, (dx, ang) in enumerate(((-34, -30), (0, -4), (34, 26))):              # leaves first (behind)
            cx, cy = 100 + dx * 0.4, 120
            tipx, tipy = cx + 150 * math.sin(math.radians(ang)), cy - 112 * math.cos(math.radians(ang))
            pts = [(cx - 10, cy), (cx + (tipx - cx) * 0.5 - 22, cy + (tipy - cy) * 0.5), (tipx, tipy), (cx + (tipx - cx) * 0.5 + 22, cy + (tipy - cy) * 0.5), (cx + 10, cy)]
            _ink_poly(d, pts, LEAF if i != 1 else LEAF_S, 5901 + i, INK_W - 1, amp=1.2)
        tip_y = 455 - [0, 70, 140][min(2, bite)]
        body = [(46, 118), (154, 118), (150, 200), (128, 330), (108, tip_y - 6), (100, tip_y), (92, tip_y - 6), (72, 330), (50, 200)]
        _ink_poly(d, body, ACC, 5905, INK_W, amp=1.4)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(body, ())), fill=255), lambda q, S_, c: q.polygon(S_(110, 118, 160, 118, 150, 210, 110, tip_y), fill=c), ACC_S, 120)
        if bite:
            _ink_ell(d, 100, tip_y + 4, 26, 12, ACC_L, 5906, INK_W - 1, amp=0.8)
        for j, yy in enumerate((170, 230, 290, 350)):                                    # rings
            if yy < tip_y - 20:
                d.line(S(62 + j * 4, yy, 88 + j * 3, yy + 6), fill=ACC_S + (255,), width=4 * SC3)
                d.line(S(118 - j * 2, yy + 20, 138 - j * 4, yy + 14), fill=ACC_S + (255,), width=4 * SC3)
        if mood: _face(d, S, 100, 196, 1.5, mood, look)
        if disguise:
            for sgn in (-1, 1):                                                         # dark round glasses
                d.ellipse(S(100 + sgn * 24 - 19, 172, 100 + sgn * 24 + 19, 208), fill=(30, 26, 30, 255), outline=INKC + (255,), width=4 * SC3)
                d.ellipse(S(100 + sgn * 24 - 8, 178, 100 + sgn * 24 - 1, 186), fill=(200, 200, 220, 200))
            d.line(S(86, 190, 114, 190), fill=INKC + (255,), width=4 * SC3)
            _ink_poly(d, [(70, 232), (100, 220), (130, 232), (118, 242), (100, 234), (82, 242)], (60, 40, 30), 5907, 3, amp=0.6)   # moustache
            _ink_poly(d, [(30, 128), (170, 128), (160, 112), (130, 108), (124, 60), (76, 60), (70, 108), (40, 112)], (70, 62, 66), 5908, INK_W, amp=1.0)  # hat
            d.rectangle(S(74, 96, 126, 108), fill=RED + (255,))
        return _done(im, w, h)
    return gcache(("carrot59", bite, mood, look, disguise), mk)


# ---------------- the 1940 newspaper ----------------
def newspaper_el(head1, head2="", stamp=None, pic=None, year="1940"):
    """a 1940 front page: masthead, date line, a 2-line headline in heavy caps, a picture box (pic: 'pilot' | 'carrot' | None), columns of grey lines."""
    def mk():
        w, h = 760, 960; im, d, S = _cv(w, h)
        _ink_poly(d, [(16, 20), (744, 12), (748, 944), (12, 950)], NEWS, 5910, INK_W, amp=1.2)
        fM = font(F_BLACK, 74 * SC3); t_ = "THE EVENING PAPER"
        d.text((380 * SC3 - d.textlength(t_, font=fM) / 2, 34 * SC3), t_, font=fM, fill=INKC + (255,))
        d.line(S(40, 130, 720, 130), fill=INKC + (255,), width=5 * SC3); d.line(S(40, 172, 720, 172), fill=INKC + (255,), width=3 * SC3)
        fD = font(F_BLACK, 28 * SC3); dl = f"LONDON  -  {year}  -  ONE PENNY"
        d.text((380 * SC3 - d.textlength(dl, font=fD) / 2, 136 * SC3), dl, font=fD, fill=INKC + (230,))
        yy = 190
        for line in (head1, head2):
            if not line: continue
            sz = 104
            while sz > 40 and d.textlength(line, font=font(F_BLACK, sz * SC3)) > 680 * SC3: sz -= 4
            fH = font(F_BLACK, sz * SC3)
            d.text((380 * SC3 - d.textlength(line, font=fH) / 2, yy * SC3), line, font=fH, fill=INKC + (255,))
            yy += sz + 14
        py = max(yy + 20, 430)
        d.rectangle(S(60, py, 400, py + 330), fill=(214, 206, 184, 255), outline=INKC + (255,), width=4 * SC3)
        if pic == "carrot":
            _ink_poly(d, [(200, py + 300), (170, py + 90), (230, py + 90)], ACC_S, 5911, 4, amp=0.8)
            _ink_poly(d, [(200, py + 90), (180, py + 40), (200, py + 60), (220, py + 36)], LEAF_S, 5912, 4, amp=0.8)
        elif pic == "pilot":
            d.ellipse(S(150, py + 70, 310, py + 230), fill=(232, 210, 186, 255), outline=INKC + (255,), width=4 * SC3)
            d.chord(S(146, py + 64, 314, py + 170), 180, 360, fill=LEATHER + (255,), outline=INKC + (255,), width=4 * SC3)
            for sgn in (-1, 1): d.ellipse(S(230 + sgn * 34 - 24, py + 92, 230 + sgn * 34 + 24, py + 132), fill=(170, 210, 230, 255), outline=INKC + (255,), width=4 * SC3)
            d.arc(S(196, py + 150, 264, py + 200), 20, 160, fill=INKC + (255,), width=5 * SC3)
            _ink_poly(d, [(300, py + 300), (282, py + 170), (320, py + 170)], ACC_S, 5913, 4, amp=0.8)
            d.rectangle(S(110, py + 250, 350, py + 330), fill=(120, 110, 96, 255))
        rng = np.random.default_rng(5914)
        for c0, c1, y0 in ((430, 710, py), (60, 710, py + 350)):
            for j in range(9 if c0 == 430 else 5):
                ly = y0 + 10 + j * 34
                if ly > 920: break
                d.line(S(c0, ly, c1 - rng.uniform(0, 60), ly), fill=(120, 110, 96, 200), width=8 * SC3)
        return _done(im, w, h)
    return gcache(("news59", head1, head2, pic, year), mk)


def spin_paper(f, el, t, t0, cx=540, cy=980, dur=0.9, turns=4, s0=0.12, s1=1.0, blur=7):
    """THE SPINNING NEWSPAPER (ep 59 craft): the paper grows from s0 to s1 while it turns `turns` full times, ending at 0 degrees, both on ONE
    ease-out (cubic) over dur; a spin blur of rotated copies follows the angular speed and is 0 when it stops; then it holds still to be read.
    Returns k 0..1 (1 = landed)."""
    if t < t0: return 0.0
    u = clamp((t - t0) / dur); e = 1 - (1 - u) ** 3
    ang = -360.0 * turns * (1 - e)                                                   # ends at exactly 0
    sc = s0 + (s1 - s0) * e
    w = 3 * (1 - u) ** 2                                                              # d(e)/du: angular speed
    spread = min(28.0, 360.0 * turns * w / dur / 24.0 * 0.5) if u < 1 else 0.0        # degrees swept in half a frame
    if spread > 0.6 and blur > 1:
        for j in range(blur):
            a = ang + spread * (j / (blur - 1) - 0.5)
            rot_comp(f, scale_el(el, sc), cx, cy, a, 1.0, 1.0 / blur * 1.6 if j != blur // 2 else 0.6, 0.0)
    else:
        rot_comp(f, scale_el(el, sc), cx, cy, ang, 1.0, 1.0, 0.25)
    return e


# ---------------- NEW PLACE: the 1940 city at NIGHT (blackout + searchlights) ----------------
BLITZ_ROOF = 1500


def set_blitz(t=0.0, blur=3, beams=1.0, moon_x=840, moon_y=560):
    """a 1940 city at night: deep navy sky softened toward paper, stars, a big moon, barrage balloons, blacked-out rooftops with chimneys along
    the bottom (roof line ~BLITZ_ROOF), 3 SEARCHLIGHT beams that sweep slowly (live)."""
    def mk():
        f = _vgrad(NAVY, NAVY2, 0, H)
        rng = np.random.default_rng(5920)
        for i in range(90):
            x, y = rng.uniform(0, W), rng.uniform(0, 1300)
            cv2.circle(f, (int(x), int(y)), int(rng.uniform(1, 3)), C((230, 230, 250)), -1, cv2.LINE_AA)
        for bx, by, s_ in ((180, 820, 0.8), (980, 700, 0.6), (620, 980, 0.5)):          # barrage balloons (soft silhouettes)
            cv2.ellipse(f, (bx, by), (int(90 * s_), int(46 * s_)), 0, 0, 360, C((70, 78, 110)), -1, cv2.LINE_AA)
            for sgn in (-1, 1): cv2.ellipse(f, (int(bx - 80 * s_), int(by + sgn * 22 * s_)), (int(30 * s_), int(14 * s_)), sgn * 30, 0, 360, C((70, 78, 110)), -1, cv2.LINE_AA)
            cv2.line(f, (bx, int(by + 46 * s_)), (bx + 20, BLITZ_ROOF), C((60, 66, 96)), 1, cv2.LINE_AA)
        f = _soft(f, blur)
        x = -20                                                                         # rooftops: two rows, back row lighter
        for row, col, base in ((0, (40, 44, 70), BLITZ_ROOF - 80), (1, (18, 20, 34), BLITZ_ROOF)):
            x = -40 + row * 60
            while x < W + 60:
                bw = int(rng.uniform(140, 230)); bh = int(rng.uniform(40, 160))
                cv2.rectangle(f, (x, base - bh), (x + bw, H), C(col), -1)
                if rng.uniform() < 0.6: cv2.rectangle(f, (x + 20, base - bh - 50), (x + 46, base - bh), C(col), -1)   # chimney
                if rng.uniform() < 0.5:
                    P = np.int32([(x, base - bh), (x + bw // 2, base - bh - 60), (x + bw, base - bh)]); cv2.fillPoly(f, [P], C(col), cv2.LINE_AA)
                x += bw
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("blitz59", blur), mk).copy()
    glow(f, moon_x, moon_y, 220, (210, 220, 255), 0.35)
    cv2.circle(f, (moon_x, moon_y), 64, C((240, 240, 226)), -1, cv2.LINE_AA); cv2.circle(f, (moon_x, moon_y), 64, C(INKC), 4, cv2.LINE_AA)
    cv2.circle(f, (moon_x - 18, moon_y - 10), 12, C((214, 214, 200)), -1, cv2.LINE_AA)
    if beams > 0:
        for i, (bx, ph, sp) in enumerate(((140, 0.0, 0.33), (560, 2.1, 0.27), (960, 4.0, 0.3))):
            a = math.radians(-90 + 32 * math.sin(t * sp + ph))
            L = 2000; wd = 0.07
            P = np.int32([(bx, BLITZ_ROOF - 60), (bx + L * math.cos(a - wd), BLITZ_ROOF - 60 + L * math.sin(a - wd)),
                          (bx + L * math.cos(a + wd), BLITZ_ROOF - 60 + L * math.sin(a + wd))])
            ov = f.copy(); cv2.fillPoly(ov, [P], C(BEAM), cv2.LINE_AA)
            ov = cv2.GaussianBlur(ov, (0, 0), 6)
            f[:] = f * (1 - 0.22 * beams) + ov * 0.22 * beams
    return inkify(f, 0.08)


# ---------------- the plane ----------------
def plane_ink_el(cut=False, lit=0.0, smoke=False, dark=False):
    """a generic 1940 propeller fighter in side view, nose to the RIGHT (ink; no insignia). cut = a cut-away hatch in the nose showing the radar box,
    lit 0..1 = the radar box lights up. Cockpit centre at (+60, -70) from the element centre at s 1 (for the pilot's head); prop hub at (+300, 0)."""
    def mk():
        w, h = 660, 300; im, d, S = _cv(w, h)
        body_c = (118, 132, 110) if not dark else (60, 56, 70)
        _ink_poly(d, [(40, 110), (90, 40), (130, 44), (150, 130)], body_c, 5930, INK_W, amp=1.0)                  # tail fin
        _ink_poly(d, [(30, 150), (160, 140), (160, 168), (40, 172)], body_c, 5931, INK_W, amp=1.0)                 # tail plane
        hull = [(40, 140), (200, 118), (430, 110), (590, 120), (626, 150), (590, 184), (430, 194), (200, 186), (40, 162)]
        _ink_poly(d, hull, body_c, 5932, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(hull, ())), fill=255), lambda q, S_, c: q.rectangle(S_(0, 160, 660, 200), fill=c), (40, 50, 40), 90)
        _ink_poly(d, [(250, 170), (470, 168), (440, 236), (300, 240)], body_c, 5933, INK_W, amp=1.0)              # wing
        _ink_poly(d, [(330, 112), (360, 66), (440, 62), (470, 110)], (190, 226, 244), 5934, INK_W, amp=1.0)       # canopy
        d.line(S(400, 64, 400, 110), fill=INKC + (255,), width=4 * SC3)
        _ink_ell(d, 614, 150, 16, 22, (60, 60, 66), 5935, INK_W - 1)                                                # spinner
        if cut:
            _ink_poly(d, [(500, 126), (586, 128), (586, 176), (500, 180)], (40, 40, 46), 5936, 4, amp=0.6)
            col = (int(70 + 120 * lit), int(90 + 150 * lit), int(70 + 60 * lit))
            _ink_poly(d, [(510, 134), (578, 136), (578, 170), (510, 172)], col, 5937, 3, amp=0.5)
            for j in range(3): d.ellipse(S(520 + 18 * j, 146, 530 + 18 * j, 156), fill=(255, 240, 160, int(80 + 175 * lit)))
        if smoke:
            for j in range(5): d.ellipse(S(10 + j * 10 - 30, 120 - j * 18, 50 + j * 14, 160 - j * 12), fill=(90, 90, 96, 150))
        return _done(im, w, h)
    return gcache(("plane59", cut, round(lit, 2), smoke, dark), mk)


def prop_spin(f, x, y, r, t, s=1.0):
    """a spinning propeller disc at the nose (x, y) (thin ellipse blur + 2 blades)."""
    ov = f.copy(); cv2.ellipse(ov, (int(x), int(y)), (int(r * 0.18), int(r)), 0, 0, 360, C((220, 224, 236)), -1, cv2.LINE_AA)
    f[:] = f * 0.7 + ov * 0.3
    a = t * 37
    for k in range(2):
        yy = y + r * math.sin(a + k * math.pi)
        cv2.line(f, (int(x), int(y)), (int(x + 5 * math.cos(a)), int(yy)), C((40, 40, 46)), max(3, int(8 * s)), cv2.LINE_AA)


def radar_scope(f, x, y, r, t, blips=((0.55, -0.8), (0.75, 2.2), (0.35, 1.0)), lit=1.0):
    """a green 1940 radar scope in an ink bezel: range rings, a sweeping line with a fading trail, blips that flare as the sweep passes."""
    cv2.circle(f, (int(x), int(y)), int(r + 22), C((70, 70, 78)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x), int(y)), int(r + 22), C(INKC), 6, cv2.LINE_AA)
    base = np.array(C(SCOPE), np.float32) * (0.4 + 0.6 * lit)
    cv2.circle(f, (int(x), int(y)), int(r), tuple(float(c) for c in base), -1, cv2.LINE_AA)
    if lit <= 0.05: return
    gl = tuple(float(c) * lit for c in C((50, 150, 80)))
    for k in (0.33, 0.66, 1.0): cv2.circle(f, (int(x), int(y)), int(r * k), gl, 2, cv2.LINE_AA)
    cv2.line(f, (int(x - r), int(y)), (int(x + r), int(y)), gl, 2, cv2.LINE_AA); cv2.line(f, (int(x), int(y - r)), (int(x), int(y + r)), gl, 2, cv2.LINE_AA)
    a = t * 3.0
    for j in range(16):
        aa = a - j * 0.045; c = np.array(C(SCOPE_L), np.float32) * (1 - j / 16) * lit
        cv2.line(f, (int(x), int(y)), (int(x + r * math.cos(aa)), int(y + r * math.sin(aa))), tuple(float(v) for v in c), 4, cv2.LINE_AA)
    for rr, ang in blips:
        bx, by = x + r * rr * math.cos(ang), y + r * rr * math.sin(ang)
        ph = (a - ang) % (2 * math.pi); br = math.exp(-ph * 0.9)
        cv2.circle(f, (int(bx), int(by)), int(8 + 10 * br), tuple(float(v) * lit for v in C((170, 255, 190))), -1, cv2.LINE_AA)
    glow(f, x, y, r * 1.1, (90, 240, 140), 0.18 * lit)


# ---------------- vitamin A ----------------
def vit_a_el(mood="happy", s=1.0):
    """the VITAMIN A buddy: an orange drop with an 'A' on its belly and a face."""
    def mk():
        w, h = 200, 250; im, d, S = _cv(w, h)
        P = [(100, 14), (140, 90), (164, 150), (150, 206), (100, 236), (50, 206), (36, 150), (60, 90)]
        _ink_poly(d, P, ACC, 5940, INK_W, amp=1.2)
        _shade(im, lambda q, S_: q.polygon(S_(*sum(P, ())), fill=255), lambda q, S_, c: q.ellipse(S_(100, 80, 200, 250), fill=c), ACC_S, 110)
        d.ellipse(S(62, 58, 84, 96), fill=(255, 255, 255, 160))
        fA = font(F_BLACK, 70 * SC3); d.text((100 * SC3 - d.textlength("A", font=fA) / 2, 150 * SC3), "A", font=fA, fill=(255, 250, 240, 255))
        _face(d, S, 100, 120, 1.3, mood)
        return _done(im, w, h)
    return gcache(("vita59", mood), mk)


def vit_tank(f, x, y, w, h, level, t, full=0.8, label=None, col=None):
    """a glass tank of vitamin A (orange liquid with a wavy top) with a FULL line at `full`; level 0..1. (x, y) = bottom centre."""
    x0, x1, y0, y1 = int(x - w / 2), int(x + w / 2), int(y - h), int(y)
    f[y0:y1, x0:x1] = f[y0:y1, x0:x1] * 0.82 + np.array(C((230, 240, 246)), np.float32) * 0.18
    lv = clamp(level)
    if lv > 0.01:
        top = y1 - lv * h
        pts = [(x0 + 6, y1 - 6)] + [(x0 + 6 + i * (w - 12) / 20, top + 6 * math.sin(t * 5 + i * 0.8)) for i in range(21)] + [(x1 - 6, y1 - 6)]
        cv2.fillPoly(f, [np.int32(pts)], C(col or ACC), cv2.LINE_AA)
        cv2.polylines(f, [np.int32(pts[1:-1])], False, C(ACC_S), 4, cv2.LINE_AA)
    fy = int(y1 - full * h)
    for xx in range(x0 - 20, x1 + 20, 26): cv2.line(f, (xx, fy), (min(xx + 14, x1 + 20), fy), C(RED), 5, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 7, cv2.LINE_AA)
    cv2.line(f, (x0 + 18, y0 + 20), (x0 + 18, y1 - 30), C((255, 255, 255)), 5, cv2.LINE_AA)
    return fy


# ---------------- Chubby as a 1940 pilot + comic 'headlight eyes' ----------------
def pilot_head(f, x, y, s, t, mouth=0, expr="happy", brow="up", look=(0.3, 0), goggles_up=True, scarf=True, turn=0.2):
    """Chubby's head as a pilot (leather cap + goggles pushed up + a white scarf); (x, y) = head centre like chub_head_only."""
    chub_head_only(f, x, y, s, t, mouth=mouth, expr=expr, brow=brow, look=look, cap=True, turn=turn)
    gy = y - 62 * s * 1.0
    for sgn in (-1, 1):
        cx = x + sgn * 40 * s + turn * 12 * s
        cv2.circle(f, (int(cx), int(gy)), int(26 * s), C((170, 210, 230)), -1, cv2.LINE_AA)
        cv2.circle(f, (int(cx), int(gy)), int(26 * s), C(INKC), max(2, int(6 * s)), cv2.LINE_AA)
        cv2.circle(f, (int(cx - 8 * s), int(gy - 8 * s)), max(1, int(6 * s)), C((255, 255, 255)), -1, cv2.LINE_AA)
    cv2.line(f, (int(x - 14 * s + turn * 12 * s), int(gy)), (int(x + 14 * s + turn * 12 * s), int(gy)), C(INKC), max(2, int(6 * s)), cv2.LINE_AA)
    if scarf:
        sy = y + 100 * s; fl = 18 * math.sin(t * 9)
        P = np.int32([(x - 70 * s, sy), (x + 70 * s, sy), (x + 60 * s, sy + 30 * s), (x - 60 * s, sy + 30 * s)])
        cv2.fillPoly(f, [P], C((250, 250, 244)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
        T_ = np.int32([(x - 60 * s, sy + 10 * s), (x - 170 * s, sy + 20 * s + fl * s), (x - 190 * s, sy + 50 * s + fl * s), (x - 70 * s, sy + 30 * s)])
        cv2.fillPoly(f, [T_], C((250, 250, 244)), cv2.LINE_AA); cv2.polylines(f, [T_], True, C(INKC), max(2, int(5 * s)), cv2.LINE_AA)


def eye_beams(f, ex, ey, sep, ang=0.0, L=900, amt=1.0, spread=0.16):
    """two comic 'headlight' beams from the eyes at (ex +- sep/2, ey) toward angle ang (radians, 0 = right, pi/2 = down)."""
    if amt <= 0: return
    ov = f.copy()
    for sgn in (-1, 1):
        x0 = ex + sgn * sep / 2
        P = np.int32([(x0, ey), (x0 + L * math.cos(ang - spread), ey + L * math.sin(ang - spread)), (x0 + L * math.cos(ang + spread), ey + L * math.sin(ang + spread))])
        cv2.fillPoly(ov, [P], C((255, 246, 200)), cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 4)
    f[:] = f * (1 - 0.62 * amt) + ov * 0.62 * amt
    for sgn in (-1, 1): glow(f, ex + sgn * sep / 2, ey, 26, (255, 246, 200), 0.35 * amt)
