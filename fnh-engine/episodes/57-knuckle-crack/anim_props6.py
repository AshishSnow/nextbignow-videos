# ================= anim_props6.py = lib57 (ep 57, 20 Nov): "Does cracking your knuckles cause arthritis?" — ACCENT = JOINT-FLUID AMBER
# (the fluid in the joint bag, the pop marks, the question words). Everything else stays paper / ink / mint / skin.
# NEW PLACE: set_desk(t, blur, top_y, dim) = a STUDY DESK at night (navy wall, a window with a moon + far windows, a bookshelf, a desk lamp's warm pool,
# a laptop's cool glow, an open doorway with warm hallway light on the right for nani) + desk_front(f, top_y) = the wooden desk edge drawn AFTER Chubby.
# NEW CRAFT (ep 57) = HAND ACTING: big_hand(...) = a close-up ink hand built for acting. Rules used (Animation Mentor, N. Seymour 2025; Animator Island,
# F. Englander 2014; AnimSchool blog, T. Roberts / S. McWhinnie / B. Kirschbaum 2025): no twinning (every finger gets its own angle, length and curl; the
# spacing between knuckles is uneven), group the fingers (two together, one apart) so the hand is not 'one boring shape', an extra bend somewhere (the
# pinky angles out), the thumb sticks out on its own line, relaxed curl lives in the first two joints, tension shows in the third (the knuckle), the
# wrist LEADS and the fingers follow a few frames later (drag), no flat 'spatula hands', and restraint: hands act only when the line is about them.
# Board: joint_board(...) = a finger joint cut-away (two bone ends in a bag of amber fluid) whose bones pull apart while a gas pocket SNAPS open.
# Props: suction_cup(...) on a glass pane, mri_ring(...) + mri_screen(...), xray_hands(...), year_flip(...), old_doc(...) (Dr Unger stand-in: white coat,
# white hair, glasses). =================
ACC = (232, 150, 40); ACC_S = (168, 96, 14); ACC_L = (248, 208, 140); ACC_XL = (252, 236, 204)      # amber = joint fluid / the pop / the question
FLUID = (248, 214, 150); FLUID_S = (214, 160, 70)
GAS = (255, 255, 252)
BONE = (252, 246, 228); BONE_S = (222, 210, 182)
GLASS = (206, 232, 246); GLASS_S = (132, 180, 214)
RED = (176, 40, 44); OKG = (40, 140, 80)
COAT = (246, 248, 250)
SRC_DOC57 = "Source: Cleveland Clinic (2026); Harvard Health; Cedars-Sinai"
SRC_MRI57 = "Source: Kawchuk et al., PLOS ONE 2015 (Univ. of Alberta)"
SRC_20MIN57 = "Source: Cedars-Sinai; Kawchuk et al. 2015"
SRC_UNGER57 = "Source: D. Unger, Arthritis & Rheumatism 1998 (one person)"
SRC_SAFE57 = "Source: Cleveland Clinic; Cedars-Sinai"
SC3 = 3
from gfx import text_el


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def _ln(f, pts, col, w):
    cv2.polylines(f, [np.int32([(int(x), int(y)) for x, y in pts])], False, C(col), max(1, int(w)), cv2.LINE_AA)


def _cap(f, p0, p1, w, fill, ink=INKC, iw=None):
    """an ink capsule (a finger segment): ink outline then flat fill, round ends."""
    iw = iw or max(3, w * 0.16)
    a = (int(p0[0]), int(p0[1])); b = (int(p1[0]), int(p1[1]))
    cv2.line(f, a, b, C(ink), int(w + 2 * iw), cv2.LINE_AA)
    cv2.line(f, a, b, C(fill), int(w), cv2.LINE_AA)


# ---------------- HAND ACTING: the close-up ink hand ----------------
# per finger (index, middle, ring, pinky): base offset along the knuckle line, length, rest angle (deg from 'up', + = toward the pinky side), width
_FING = [(-64, 158, -9, 40), (-20, 172, -1, 42), (24, 160, 7, 40), (62, 124, 19, 34)]     # uneven spacing + lengths + an angled pinky (no twinning)


def big_hand(f, x, y, s=1.0, rot=0.0, side=1, ang=(0, 0, 0, 0), curl=(0.15, 0.1, 0.2, 0.3), stretch=(0, 0, 0, 0), thumb=35.0, swell=0.0,
             swell_f=1, red=0.0, op=1.0, sleeve=INK_MINT):
    """a big ink HAND seen from the back, wrist at (x, y), pointing up (rot deg, + = clockwise on screen). side +1 = a right hand (thumb on screen-left),
    -1 = a left hand (mirrored). ang = extra angle per finger, curl 0..1 per finger (foreshortens the first two joints = relaxed curl), stretch = extra
    length (a finger being pulled), thumb = thumb angle out from the palm, swell / red on finger swell_f's knuckle. Returns the four fingertips + knuckles."""
    g = f if op >= 0.999 else f.copy()
    ra = math.radians(rot)
    def P(dx, dy):                       # hand space (dx right, dy up) -> screen
        dx = dx * side
        return (x + (dx * math.cos(ra) + dy * math.sin(ra)) * s, y + (dx * math.sin(ra) - dy * math.cos(ra)) * s)
    tips = [None] * 4; knuck = [None] * 4
    # sleeve cuff first (the wrist comes out of it)
    cuff = [P(-62, -10), P(62, -10), P(70, -110), P(-70, -110)]
    cv2.fillPoly(g, [np.int32(cuff)], C(sleeve), cv2.LINE_AA); cv2.polylines(g, [np.int32(cuff)], True, C(INKC), max(3, int(6 * s)), cv2.LINE_AA)
    # fingers: pinky first so the index overlaps it (overlap = depth); each finger = 3 segments
    order = [3, 2, 1, 0]
    segs = {}
    for i in order:
        bx, L, a0, w = _FING[i]
        L = L * (1 + stretch[i]); a = math.radians(a0 + ang[i]); c = clamp(curl[i])
        k0 = (bx, 150)
        lens = (L * 0.42 * (1 - 0.45 * c), L * 0.33 * (1 - 0.55 * c), L * 0.25 * (1 - 0.35 * c))
        pts = [k0]; cur = k0; aa = a
        for j, ln_ in enumerate(lens):
            aa = aa + (0.10 * c if j else 0.0) * (1 if a0 >= 0 else -1)
            cur = (cur[0] + math.sin(aa) * ln_, cur[1] + math.cos(aa) * ln_); pts.append(cur)
        segs[i] = (pts, w)
        SP = [P(*p) for p in pts]
        ww = w * s
        for j in range(3):
            fw = ww * (1 - 0.06 * j)
            if j == 0 and i == swell_f and swell > 0: fw *= 1 + 0.35 * swell
            _cap(g, SP[j], SP[j + 1], fw, _mix(INK_SKIN, (236, 120, 110), red * (1.0 if j == 0 else 0.25) if i == swell_f else 0))
        # knuckle creases + a nail on the last segment
        for j in (1, 2):
            px, py = SP[j]; dx_, dy_ = SP[j + 1][0] - SP[j - 1][0], SP[j + 1][1] - SP[j - 1][1]; nn = math.hypot(dx_, dy_) + 1e-6
            nx, ny = -dy_ / nn, dx_ / nn
            cv2.line(g, (int(px - nx * ww * 0.28), int(py - ny * ww * 0.28)), (int(px + nx * ww * 0.18), int(py + ny * ww * 0.18)), C(INK_SKIN_S), max(2, int(3 * s)), cv2.LINE_AA)
        tx_, ty_ = SP[3]; ux, uy = SP[3][0] - SP[2][0], SP[3][1] - SP[2][1]; nn = math.hypot(ux, uy) + 1e-6
        nc = (tx_ - ux / nn * ww * 0.32, ty_ - uy / nn * ww * 0.32)
        cv2.ellipse(g, (int(nc[0]), int(nc[1])), (max(2, int(ww * 0.26)), max(2, int(ww * 0.34))), math.degrees(math.atan2(uy, ux)) + 90, 0, 360, C((252, 236, 226)), -1, cv2.LINE_AA)
        cv2.ellipse(g, (int(nc[0]), int(nc[1])), (max(2, int(ww * 0.26)), max(2, int(ww * 0.34))), math.degrees(math.atan2(uy, ux)) + 90, 0, 360, C(INK_SKIN_S), max(2, int(2.5 * s)), cv2.LINE_AA)
        tips[i] = SP[3]; knuck[i] = SP[1]
    # thumb (its own line: from the lower palm side, out at `thumb` degrees)
    th_ = math.radians(40 + (thumb - 35) * 0.6); th2 = th_ - math.radians(18)
    t0 = (-72, 50); t1 = (t0[0] - math.sin(th_) * 58, t0[1] + math.cos(th_) * 58); t2 = (t1[0] - math.sin(th2) * 46, t1[1] + math.cos(th2) * 46)
    TP = [P(*t0), P(*t1), P(*t2)]
    _cap(g, TP[0], TP[1], 46 * s, INK_SKIN); _cap(g, TP[1], TP[2], 40 * s, INK_SKIN)
    # palm over the finger roots (no top outline, so the fingers grow out of it)
    palm = [P(-80, 0), P(-86, 70), P(-80, 150), P(-40, 166), P(0, 170), P(42, 164), P(80, 150), P(88, 70), P(80, 0)]
    cv2.fillPoly(g, [np.int32(palm)], C(INK_SKIN), cv2.LINE_AA)
    sh = [P(30, 4), P(80, 0), P(88, 70), P(80, 140), P(44, 120)]                       # shadow side (away from the lamp)
    cv2.fillPoly(g, [np.int32(sh)], C(_mix(INK_SKIN, INK_SKIN_S, 0.35)), cv2.LINE_AA)
    _ln(g, [P(-80, 150), P(-86, 70), P(-80, 0)], INKC, 6 * s); _ln(g, [P(80, 150), P(88, 70), P(80, 0)], INKC, 6 * s)
    _ln(g, [P(-80, 150), P(-74, 160)], INKC, 6 * s); _ln(g, [P(80, 150), P(74, 160)], INKC, 6 * s)
    # knuckle bumps (the joints this video is about): small arcs, the tense one darker
    for i in range(4):
        bx = _FING[i][0]
        cv2.ellipse(g, (int(P(bx, 152)[0]), int(P(bx, 152)[1])), (int(16 * s), int(9 * s)), math.degrees(ra), 180, 360, C(INK_SKIN_S), max(2, int(4 * s)), cv2.LINE_AA)
        if i == swell_f and red > 0:
            glow(g, P(bx, 160)[0], P(bx, 160)[1], 70 * s, (240, 90, 80), 0.25 * red)
    for j in range(3):                                                                  # tendons / back-of-hand lines
        _ln(g, [P(-46 + 30 * j, 30), P(-50 + 34 * j, 120)], INK_SKIN_S, 3 * s)
    if op < 0.999: f[:] = f * (1 - op) + g * op
    return dict(tips=tips, knuck=knuck, wrist=P(0, 0))


def fist_at(f, x, y, s=1.0, rot=0.0):
    """the OTHER hand as a fist gripping a fingertip at (x, y) (pulling it)."""
    grip_hand(f, x, y, s * 2.6, kind="grip", rot=rot)


# ---------------- BOARD: the finger joint cut-away ----------------
def joint_board(f, cx, cy, t, k=1.0, gap=0.0, cav=0.0, fluid=1.0, sc=1.0, seed=570, labels=None):
    """the KNUCKLE on the board: an upper bone with a ROUND head that sits in the CUP of the lower bone, inside a bag (capsule) filled with amber joint
    fluid. gap = how far the bones are pulled apart (px), cav 0..1 = the gas pocket that snaps open in the fluid (white with an amber rim)."""
    hg = gap / 2
    def S(px, py): return (cx + px * sc, cy + py * sc)
    bag_ry = 130 + hg * 0.9
    if fluid > 0 and k > 0.6:                                                            # the fluid inside the bag
        ov = f.copy()
        cv2.ellipse(ov, (int(cx), int(cy + 10 * sc)), (int(205 * sc), int(bag_ry * sc)), 0, 0, 360, C(FLUID), -1, cv2.LINE_AA)
        a = clamp((k - 0.6) / 0.4) * 0.9 * fluid; f[:] = f * (1 - a) + ov * a
    head = [(100 * math.cos(math.radians(a_)), -30 - hg + 70 * math.sin(math.radians(a_))) for a_ in range(0, 181, 12)]
    up = [S(100, -330)] + [S(*p) for p in head] + [S(-100, -330)]
    cup = [(x_, 50 + hg - 55 * (x_ / 118) ** 2) for x_ in range(-118, 119, 16)]
    lo = [S(-118, 350)] + [S(*p) for p in cup] + [S(118, 350)]
    for poly in (up, lo):
        if k > 0.5:
            ov = f.copy(); cv2.fillPoly(ov, [np.int32(poly)], C(BONE), cv2.LINE_AA)
            a = clamp((k - 0.5) / 0.4); f[:] = f * (1 - a) + ov * a
            if a > 0.9: hatch_on(f, poly, 1.0, BONE_S, gap=22, ang=45, w=3, op=0.5)
    draw_on(f, up, k, BP_INK, 8, seed=seed, tip=k < 1)
    draw_on(f, lo, k, BP_INK, 8, seed=seed + 1, tip=k < 1)
    if cav > 0.01:                                                                       # the gas pocket between the head and the cup
        r = 78 * sc * cav; ccy = cy + 45 * sc
        ry = max(5, min(r * 0.6, (hg + 20) * sc))
        cv2.ellipse(f, (int(cx), int(ccy)), (int(r), int(ry)), 0, 0, 360, C(GAS), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(cx), int(ccy)), (int(r), int(ry)), 0, 0, 360, C(ACC_S), 5, cv2.LINE_AA)
    draw_ell_on(f, cx, cy + 10 * sc, 205 * sc, bag_ry * sc, k, BP_INK, 7, seed=seed + 2)
    return dict(bag=(cx, cy, 205 * sc, bag_ry * sc))


# ---------------- the SUCTION CUP on a glass pane ----------------
def glass_pane(f, x0, y0, x1, y1):
    ov = f.copy(); cv2.rectangle(ov, (x0, y0), (x1, y1), C(GLASS), -1); f[:] = f * 0.35 + ov * 0.65
    for j, (a, b) in enumerate(((60, 160), (120, 190))):
        cv2.line(f, (x0 + a, y0 + 40), (x0 + a - 60, y0 + b + 120), C((250, 254, 255)), 10 - 3 * j, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C(GLASS_S), 8, cv2.LINE_AA)


def suction_cup(f, x, y, s=1.0, pull=0.0, off=0.0, rot=0.0):
    """a rubber suction cup stuck to a pane at x (its flat rim), dome facing right; pull 0..1 stretches the dome into a cone while the rim holds;
    off = how far the whole cup has flown off after the pop (px). Returns the knob point (for the fist)."""
    rx = x + off; d = (55 + 95 * pull) * s; Ry = 120 * s * (1 - 0.15 * pull)
    dome = [(rx + d * math.cos(math.radians(a_)) ** (1 + 0.6 * pull), y + Ry * math.sin(math.radians(a_))) for a_ in range(-90, 91, 8)]
    if off > 0:
        ccx, ccy = rx + d / 2, y; r_ = math.radians(rot)
        dome = [(ccx + (px - ccx) * math.cos(r_) - (py - ccy) * math.sin(r_), ccy + (px - ccx) * math.sin(r_) + (py - ccy) * math.cos(r_)) for px, py in dome]
    cv2.fillPoly(f, [np.int32(dome)], C(ACC), cv2.LINE_AA)
    cv2.polylines(f, [np.int32(dome)], True, C(INKC), max(3, int(6 * s)), cv2.LINE_AA)
    mid = dome[len(dome) // 2]
    if off <= 0 and pull > 0.05:                                                         # the low-pressure pocket under the dome
        cv2.ellipse(f, (int(rx + d * 0.32), int(y)), (int(d * 0.24), int(Ry * 0.55 * pull)), 0, 0, 360, C(GAS), -1, cv2.LINE_AA)
    kx, ky = mid
    cv2.line(f, (int(kx), int(ky)), (int(kx + 44 * s), int(ky)), C(INKC), int(30 * s), cv2.LINE_AA)
    cv2.line(f, (int(kx), int(ky)), (int(kx + 44 * s), int(ky)), C(ACC_S), int(20 * s), cv2.LINE_AA)
    return (kx + 54 * s, ky)


# ---------------- the MRI scanner + its screen ----------------
def mri_ring(f, cx, cy, R=330, t=0.0, scan=0.0):
    cv2.ellipse(f, (cx, cy + R - 30), (int(R * 1.05), 40), 0, 0, 360, C((60, 60, 70)), -1, cv2.LINE_AA)     # floor shadow
    cv2.circle(f, (cx, cy), R, C((236, 238, 242)), -1, cv2.LINE_AA); cv2.circle(f, (cx, cy), R, C(INKC), 8, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), int(R * 0.86), C(ACC), 22, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), int(R * 0.5), C((40, 46, 60)), -1, cv2.LINE_AA); cv2.circle(f, (cx, cy), int(R * 0.5), C(INKC), 7, cv2.LINE_AA)
    if scan > 0:
        a = (t * 360) % 360
        cv2.ellipse(f, (cx, cy), (int(R * 0.68), int(R * 0.68)), 0, a, a + 50, C((120, 210, 255)), 12, cv2.LINE_AA)
    cv2.rectangle(f, (cx - R - 120, cy + 60), (cx + R + 120, cy + 110), C((210, 214, 222)), -1)              # the bed
    cv2.rectangle(f, (cx - R - 120, cy + 60), (cx + R + 120, cy + 110), C(INKC), 6, cv2.LINE_AA)


def mri_screen(f, x, y, w, h, gap=0.0, cav=0.0, t=0.0):
    """a grey MRI image of the joint: the bone ends bright, the joint fluid mid grey; the cavity appears as a DARK spot (cav 0..1)."""
    cv2.rectangle(f, (x - 16, y - 16), (x + w + 16, y + h + 16), C((52, 54, 62)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x, y), (x + w, y + h), C((26, 26, 30)), -1)
    cx, cy = x + w // 2, y + h // 2; hg = gap / 2
    cv2.ellipse(f, (cx, cy), (int(w * 0.36), int(h * 0.2 + hg)), 0, 0, 360, C((118, 118, 124)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (cx - int(w * 0.16), y + 10), (cx + int(w * 0.16), int(cy - 14 - hg)), C((206, 206, 210)), -1)
    cv2.ellipse(f, (cx, int(cy - 14 - hg)), (int(w * 0.16), 22), 0, 0, 180, C((206, 206, 210)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (cx - int(w * 0.18), int(cy + 18 + hg)), (cx + int(w * 0.18), y + h - 10), C((206, 206, 210)), -1)
    if cav > 0.01:
        cv2.ellipse(f, (cx, cy + 2), (int(w * 0.14 * cav), int((10 + hg * 0.8) * cav)), 0, 0, 360, C((6, 6, 8)), -1, cv2.LINE_AA)
    n = np.random.default_rng(int(t * 24) % 5).random((h // 6, w // 6)).astype(np.float32)
    n = cv2.resize(n, (w, h))[..., None] * 0.08
    f[y:y + h, x:x + w] = np.clip(f[y:y + h, x:x + w] + n - 0.04, 0, 1)
    cv2.rectangle(f, (x, y), (x + w, y + h), C((150, 156, 170)), 4, cv2.LINE_AA)


# ---------------- the X-ray lightbox with two hands ----------------
def _bones(f, x, y, s, side, col, glowc=None):
    def P(dx, dy): return (x + dx * side * s, y - dy * s)
    for i, (bx, L, a0, w) in enumerate(_FING):
        a = math.radians(a0); cur = (bx * 0.9, 150)
        for j, fr in enumerate((0.42, 0.33, 0.25)):
            nx_ = (cur[0] + math.sin(a) * L * fr, cur[1] + math.cos(a) * L * fr)
            p0, p1 = P(*cur), P(*nx_)
            cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(col), max(3, int(16 * s)), cv2.LINE_AA)
            cv2.circle(f, (int(p1[0]), int(p1[1])), max(2, int(10 * s)), C(col), -1, cv2.LINE_AA)
            cur = (nx_[0] + math.sin(a) * 10, nx_[1] + math.cos(a) * 10)
        b0 = P(bx * 0.6, 10); b1 = P(bx * 0.9, 140)
        cv2.line(f, (int(b0[0]), int(b0[1])), (int(b1[0]), int(b1[1])), C(col), max(3, int(18 * s)), cv2.LINE_AA)
    t0 = P(-60, 30); t1 = P(-120, 100); t2 = P(-150, 150)
    cv2.line(f, (int(t0[0]), int(t0[1])), (int(t1[0]), int(t1[1])), C(col), max(3, int(18 * s)), cv2.LINE_AA)
    cv2.line(f, (int(t1[0]), int(t1[1])), (int(t2[0]), int(t2[1])), C(col), max(3, int(15 * s)), cv2.LINE_AA)


def xray_hands(f, cx, cy, t, s=1.0):
    """two X-ray films side by side on a lightbox (left hand = cracked, right hand = never cracked)."""
    for j, side in enumerate((-1, 1)):
        x0 = int(cx - 420 * s + j * 430 * s); y0 = int(cy - 300 * s)
        cv2.rectangle(f, (x0, y0), (int(x0 + 410 * s), int(y0 + 600 * s)), C((30, 48, 74)), -1)
        cv2.rectangle(f, (x0, y0), (int(x0 + 410 * s), int(y0 + 600 * s)), C(INKC), 7, cv2.LINE_AA)
        _bones(f, x0 + 205 * s, y0 + 520 * s, 1.15 * s, -side, (214, 232, 246))


# ---------------- the doctor who tested it on himself (a generic stand-in, not a likeness) ----------------
def old_doc(f, x, y, s, t, la=(26, 14), ra=(26, 14), hand_l="open", hand_r="open", mouth=0, expr="n", brow="n", look=(0, 0), turn=0.0, lean=0.0):
    hands = chub(f, x, y, s, t=t, shirt=COAT, la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=mouth, expr=expr, brow=brow, look=look, turn=turn, lean=lean)
    hx, hy = x + lean * 2 * s + turn * 14 * s, y - 420 * s
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INK_SKIN), -1, cv2.LINE_AA)             # bald crown
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    for sg in (-1, 1):                                                                                                       # white side tufts
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(24 * s), int(38 * s)), 0, 0, 360, C((240, 240, 244)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(24 * s), int(38 * s)), 0, 0, 360, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    for sg in (-1, 1):                                                                                                       # square glasses
        gx = hx + sg * 34 * s + turn * 10 * s
        cv2.rectangle(f, (int(gx - 24 * s), int(hy - 26 * s)), (int(gx + 24 * s), int(hy + 10 * s)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.line(f, (int(hx - 10 * s), int(hy - 10 * s)), (int(hx + 10 * s), int(hy - 10 * s)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    for sg in (-1, 1):                                                                                                       # coat lapels
        P_ = np.int32([(x + sg * 20 * s, y - 330 * s), (x + sg * 70 * s, y - 330 * s), (x + sg * 30 * s, y - 220 * s)])
        cv2.fillPoly(f, [P_], C((222, 226, 232)), cv2.LINE_AA); cv2.polylines(f, [P_], True, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    return hands


def year_flip(f, x, y, t, t0, t1, y0=1, y1=50, s=1.0):
    """a desk calendar whose pages flip from YEAR y0 to YEAR y1 between t0 and t1 (ease-in: slow, then a blur of pages)."""
    v = clamp((t - t0) / max(1e-3, t1 - t0)); v = v * v
    yr = int(round(y0 + (y1 - y0) * v))
    w, h = int(300 * s), int(260 * s)
    cv2.rectangle(f, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), C(PAPER), -1)
    cv2.rectangle(f, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y - h / 2 + 60 * s)), C(ACC), -1)
    cv2.rectangle(f, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), C(INKC), 7, cv2.LINE_AA)
    for j in range(5): cv2.circle(f, (int(x - w / 2 + 40 * s + j * 55 * s), int(y - h / 2)), int(9 * s), C(INKC), -1, cv2.LINE_AA)
    comp(f, text_el([([("YEAR", PAPER, 1.0)], F_BLACK, int(34 * s), 2)], shadow=0, pad=6), x, y - h / 2 + 30 * s)
    comp(f, text_el([([(str(yr), INKC, 1.0)], F_BLACK, int(110 * s), 0)], shadow=0, pad=6), x, y + 30 * s)
    if 0 < v < 1 and int(t * 24) % 2 == 0:                                              # a page flying off
        P_ = np.int32([(x - w / 2, y - h / 2 + 60 * s), (x + w / 2, y - h / 2 + 60 * s), (x + w / 2 + 40 * s, y - h / 2 - 80 * s), (x - w / 2 + 60 * s, y - h / 2 - 40 * s)])
        cv2.fillPoly(f, [P_], C((250, 248, 240)), cv2.LINE_AA); cv2.polylines(f, [P_], True, C(INKC), 4, cv2.LINE_AA)
    return yr


# ---------------- NEW PLACE: the STUDY DESK at night ----------------
DESK_TOP = 1560


def set_desk(t=0.0, blur=5, top_y=DESK_TOP, dim=0.0, door=1.0):
    """THE STUDY DESK at night: a navy-grey wall, a window (left) with a moon and far lit windows, a bookshelf (centre-left), a desk LAMP (left) with a
    warm pool, an OPEN DOORWAY (right) with warm hallway light (where nani appears), a laptop's cool glow from the desk. Paper-softened."""
    def mk():
        f = _vgrad((92, 104, 132), (70, 80, 106), 0, top_y)
        cv2.rectangle(f, (60, 300), (360, 760), C((34, 44, 74)), -1)                                                # night window
        cv2.circle(f, (270, 400), 46, C((250, 244, 214)), -1, cv2.LINE_AA)
        for j in range(9):
            bx = 80 + 32 * j; bh = 140 + (j * 53) % 160
            cv2.rectangle(f, (bx, 760 - bh), (bx + 28, 760), C((52, 62, 92)), -1)
            for k in range(3):
                if (j + k) % 3: cv2.rectangle(f, (bx + 8, 770 - bh + 30 * k + 20), (bx + 16, 770 - bh + 30 * k + 30), C((250, 214, 130)), -1)
        cv2.rectangle(f, (60, 300), (360, 760), C((50, 40, 34)), 16, cv2.LINE_AA); cv2.line(f, (210, 300), (210, 760), C((50, 40, 34)), 10)
        cv2.rectangle(f, (400, 420), (640, 900), C((120, 86, 60)), -1)                                               # bookshelf
        for r_, yy in enumerate((520, 680, 840)):
            cv2.rectangle(f, (400, yy), (640, yy + 14), C((90, 62, 42)), -1)
            for j in range(7):
                bw = 22 + (j * 7 + r_ * 5) % 12; bh = 70 + (j * 13 + r_ * 11) % 40
                col = [(176, 70, 60), (60, 120, 150), (220, 180, 90), (90, 150, 110), (150, 110, 170)][(j + r_) % 5]
                bx = 412 + j * 32
                cv2.rectangle(f, (bx, yy - bh), (bx + bw, yy), C(col), -1)
        cv2.rectangle(f, (800, 320), (1040, top_y), C((54, 40, 30)), -1)                                             # the doorway (dark frame)
        cv2.rectangle(f, (824, 344), (1040, top_y), C((250, 214, 150)), -1)                                          # warm hallway light
        cv2.rectangle(f, (824, top_y - 160), (1040, top_y), C((226, 180, 120)), -1)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("desk57", blur, top_y), mk).copy()
    lamp_glow(f, 930, 760, 360, (255, 200, 130), 0.22 * door)
    lamp_glow(f, 150, top_y - 330, 300, (255, 206, 140), 0.30)                                                     # desk lamp pool
    lamp_glow(f, 760, top_y - 120, 260, (150, 200, 255), 0.12 + 0.02 * math.sin(t * 5))                           # laptop glow
    dust_motes(f, t, 60, 600, 360, 1300, n=14, amt=0.4)
    if dim > 0: f = f * (1 - 0.5 * dim)
    return inkify(f)


def desk_front(f, top_y=DESK_TOP, t=0.0, laptop=False, lamp=True):
    """the wooden DESK edge (drawn AFTER Chubby): plank top with grain, a lamp on the left, a laptop seen from behind on the right, a mug + pencil."""
    if lamp:                                                                                                     # desk lamp (arm + shade)
        cv2.line(f, (60, top_y), (70, top_y - 200), C(INKC), 16, cv2.LINE_AA); cv2.line(f, (70, top_y - 200), (120, top_y - 290), C(INKC), 16, cv2.LINE_AA)
        P_ = np.int32([(60, top_y - 330), (170, top_y - 300), (140, top_y - 236), (40, top_y - 270)])
        cv2.fillPoly(f, [P_], C(ACC), cv2.LINE_AA); cv2.polylines(f, [P_], True, C(INKC), 6, cv2.LINE_AA)
        cv2.ellipse(f, (60, top_y), (50, 14), 0, 0, 360, C(INKC), -1, cv2.LINE_AA)
    if laptop:
        P_ = np.int32([(700, top_y), (980, top_y), (960, top_y - 190), (720, top_y - 190)])                         # laptop lid from behind
        cv2.fillPoly(f, [P_], C((176, 184, 196)), cv2.LINE_AA); cv2.polylines(f, [P_], True, C(INKC), 6, cv2.LINE_AA)
        cv2.circle(f, (840, top_y - 100), 16, C((214, 220, 230)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y), (W, top_y + 60), C((176, 124, 80)), -1)
    for y in (top_y + 20, top_y + 40): cv2.line(f, (0, y), (W, y), C((150, 102, 62)), 3, cv2.LINE_AA)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 60), (W, top_y + 60), C(INKC), 5, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 60), (W, H), C((132, 92, 60)), -1)
    _hatch_band(f, top_y + 66, H)
