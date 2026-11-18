# ================= anim_props6.py = lib52 (ep 52, 18 Nov): "Does drinking water standing up hurt your knees?" — ACCENT = CLEAR WATER BLUE
# (the water, the question words, the joint fluid, the chips). Blood stays red (the second colour of the story, used only for the vessel).
# NEW PLACE: set_dining(t, blur, top_y, dim) = an Indian home's DINING CORNER on a sunny afternoon (pale mint wall, a wall-mounted water PURIFIER with a
# blue tank + tap, a wall calendar, a window with a sun shaft, a steel matka on a stand) + dining_front(f, top_y) = the dining table edge (wood + a
# plastic checked table cloth) drawn AFTER Chubby.
# NEW INK PROPS: steel_glass_el(level, mood, look, tilt_water) (the steel tumbler), xray_knee_el() (a knee x-ray film in the doctor's hand), water_ball(f, ...)
# (a floating, wobbling ball of water in zero-g), nani(f, ...) (grandma = chub + saree pallu + grey bun + round glasses).
# NEW CRAFT (ep 52) = THE FOLLOW CAMERA (anim_fx.follow_cam): a tilt that FOLLOWS a moving subject down a tall board: starts a few frames after the
# subject, damped (it trails), with look-ahead room in the direction of travel, and a small dead zone so tiny moves don't jiggle the frame. =================
ACC = (64, 156, 226); ACC_S = (26, 96, 170); ACC_L = (178, 220, 248); ACC_XL = (226, 242, 252)      # clear water blue = the water / the question
WAT = (150, 206, 246); WAT_S = (84, 160, 222); WAT_H = (240, 250, 255)
STEEL = (210, 216, 222); STEEL_S = (150, 158, 170); STEEL_H = (246, 248, 252)
BLOOD = (196, 52, 58); BLOOD_L = (240, 170, 170)
BONE = (246, 238, 220); BONE_S = (214, 200, 170)
MINTW = (214, 232, 216)
SRC_MYTH52 = "Source: Medical Dialogues fact check (2024); NewsMeter (2023)"
SRC_PIPE52 = "Source: NIDDK (NIH); Binghamton Univ. / The Conversation (2026)"
SRC_BLOOD52 = "Source: NIDDK (NIH); Cleveland Clinic"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


# ---------------- props (ink language: one warm-ink wobbly outline, flat fill, shade + hatch on the shadow side) ----------------
def steel_glass_el(level=0.75, mood=None, look=(0, 0), seed=521):
    """the Indian STEEL TUMBLER (straight, slightly tapered, a rolled rim, two bright vertical glints), water inside seen at the rim (level 0..1)."""
    lk = round(clamp(level) * 8) / 8
    def mk():
        w, h = 200, 260; im, d, S = _cv(w, h)
        body = [(36, 30), (164, 30), (152, 240), (48, 240)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.7)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(118, 20, 200, 250), fill=c), STEEL_S, 120)
        _hatch_in(im, (122, 34, 166, 238), lambda q, S_: q.polygon(_P(body), fill=255), -40, 9, 34)
        for x0, ww in ((62, 14), (90, 6)):                                                 # glints
            d.polygon(_P([(x0, 40), (x0 + ww, 40), (x0 + ww - 3, 232), (x0 - 3, 232)]), fill=STEEL_H + (230,))
        for y in (64, 210):                                                                # turned rings
            d.line(S(40, y, 160, y), fill=STEEL_S + (200,), width=3 * SC3)
        _ink_ell(d, 100, 30, 64, 14, (196, 204, 212), seed + 1, INK_W - 2, amp=0.5)      # rolled rim
        if lk > 0:
            _ink_ell(d, 100, 32 + 10 * (1 - lk), 56, 10, WAT, seed + 2, 3, amp=0.4)        # the water surface
            d.arc(S(60, 26, 120, 40), 200, 300, fill=WAT_H + (255,), width=3 * SC3)
        _ink_poly(d, body, None, seed, INK_W, amp=0.7)
        if mood: _face(d, S, 100, 140, 1.5, mood, look)
        return _done(im, w, h)
    return gcache(("sglass52", lk, mood, look, seed), mk)


def xray_knee_el(seed=522):
    """a knee X-RAY film: dark blue-black sheet, pale thigh bone + shin bone + kneecap with a clear gap (the joint), a corner clip."""
    def mk():
        w, h = 300, 380; im, d, S = _cv(w, h)
        _ink_poly(d, [(14, 14), (286, 14), (286, 366), (14, 366)], (36, 48, 70), seed, 5, amp=0.5)
        bone = (206, 220, 232)
        _ink_poly(d, [(110, 30), (190, 30), (196, 150), (222, 176), (208, 196), (92, 196), (78, 176), (104, 150)], bone, seed + 1, 3, amp=0.8, col=(150, 170, 190))
        _ink_poly(d, [(84, 214), (216, 214), (204, 238), (186, 250), (182, 350), (118, 350), (114, 250), (96, 238)], bone, seed + 2, 3, amp=0.8, col=(150, 170, 190))
        _ink_ell(d, 214, 168, 22, 30, bone, seed + 3, 3, amp=0.5, col=(150, 170, 190))     # kneecap (side)
        d.rectangle(S(130, 8, 170, 26), fill=(200, 200, 206, 255), outline=INKC + (255,), width=3 * SC3)
        return _done(im, w, h)
    return gcache(("xray52", seed), mk)


def water_ball(f, x, y, r, t, seed=0, mood=None):
    """a floating ball of water in zero-g: a wobbling blob (two slow modes), clear blue fill, white rim highlight, ink outline."""
    P = []
    for i in range(40):
        a = 2 * math.pi * i / 40
        rr = r * (1 + 0.07 * math.sin(2 * a + t * 3.1 + seed) + 0.045 * math.sin(3 * a - t * 4.3 + seed * 2))
        P.append((x + rr * math.cos(a), y + rr * 0.94 * math.sin(a)))
    P = np.int32(np.round(np.array(P)))
    ov = f.copy(); cv2.fillPoly(ov, [P], C(WAT), cv2.LINE_AA); f[:] = f * 0.25 + ov * 0.75
    cv2.ellipse(f, (int(x - r * 0.3), int(y - r * 0.35)), (int(r * 0.32), int(r * 0.16)), -30, 0, 360, C(WAT_H), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(x + r * 0.15), int(y + r * 0.42)), (int(r * 0.5), int(r * 0.2)), 0, 0, 180, C(WAT_S), max(2, int(r * 0.06)), cv2.LINE_AA)
    cv2.polylines(f, [P], True, C(INKC), max(2, int(r * 0.06)), cv2.LINE_AA)


def nani(f, x, y, s, t, la=(24, 12), ra=(24, 12), hand_l="open", hand_r="open", mouth=0, expr="n", brow="n", look=(0, 0), turn=0.0, lean=0.0, hold=None, hold_off=(0, 0)):
    """GRANDMA (nani): chub with a maroon-and-cream saree look (shirt), a grey bun, round glasses, a pallu over one shoulder."""
    kw_ = dict(hold=hold, hold_off=hold_off) if hold is not None else {}
    chub(f, x, y, s, t=t, shirt=(150, 64, 84), la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=mouth, expr=expr, brow=brow, look=look, turn=turn, lean=lean, **kw_)
    hx, hy = x + lean * 2 * s + turn * 14 * s, y - 420 * s
    cv2.circle(f, (int(hx + 4 * s), int(hy - 112 * s)), int(38 * s), C(INKC), -1, cv2.LINE_AA)                      # grey bun
    cv2.circle(f, (int(hx + 4 * s), int(hy - 112 * s)), int(30 * s), C((196, 196, 200)), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(92 * s), int(40 * s)), 0, 180, 360, C((206, 206, 210)), int(14 * s), cv2.LINE_AA)   # grey hair line
    for sg in (-1, 1):                                                                                                 # round glasses
        cv2.circle(f, (int(hx + sg * 34 * s + turn * 10 * s), int(hy - 6 * s)), int(24 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.line(f, (int(hx - 10 * s + turn * 10 * s), int(hy - 6 * s)), (int(hx + 10 * s + turn * 10 * s), int(hy - 6 * s)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    P = np.array([(hx - 110 * s, y - 330 * s), (hx - 40 * s, y - 330 * s), (hx + 90 * s, y - 120 * s), (hx + 30 * s, y - 100 * s)], np.int32)  # the pallu
    cv2.fillPoly(f, [P], C((236, 196, 120)), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    for k in range(3):
        u = 0.25 + 0.25 * k
        a = (P[0] + (P[3] - P[0]) * u); b = (P[1] + (P[2] - P[1]) * u)
        cv2.line(f, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), C((176, 52, 70)), max(2, int(5 * s)), cv2.LINE_AA)


# ---------------- NEW PLACE: the DINING CORNER (afternoon) ----------------
DIN_TOP = 1330


def set_dining(t=0.0, blur=5, top_y=DIN_TOP, dim=0.0):
    """THE DINING CORNER: pale mint wall, a wall-mounted water PURIFIER (white box, blue see-through tank, a tap) on the right, a wall calendar, a window
    with a warm afternoon sun shaft on the left, a steel matka on a stand. Paper-softened for Chubby INK. dim 0..1 = lights down."""
    def mk():
        f = _vgrad((226, 240, 228), (200, 222, 206), 0, top_y)
        cv2.rectangle(f, (0, top_y - 120), (W, top_y), C((186, 206, 192)), -1)                                   # dado band
        cv2.line(f, (0, top_y - 120), (W, top_y - 120), C((150, 170, 156)), 6, cv2.LINE_AA)
        cv2.rectangle(f, (60, 380), (360, 860), C((120, 92, 66)), -1, cv2.LINE_AA)                                 # window frame
        cv2.rectangle(f, (80, 400), (340, 840), C((252, 236, 196)), -1, cv2.LINE_AA)
        cv2.line(f, (210, 400), (210, 840), C((120, 92, 66)), 10); cv2.line(f, (80, 620), (340, 620), C((120, 92, 66)), 10)
        for j in range(4): cv2.ellipse(f, (150 + 60 * j, 720), (40, 70), 0, 180, 360, C((150, 196, 140)), -1, cv2.LINE_AA)  # a tree outside
        x0, y0 = 760, 430                                                                                           # the water purifier
        cv2.rectangle(f, (x0 - 130, y0), (x0 + 130, y0 + 420), C((250, 250, 248)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x0 - 130, y0), (x0 + 130, y0 + 420), C((150, 160, 168)), 5, cv2.LINE_AA)
        cv2.rectangle(f, (x0 - 90, y0 + 60), (x0 + 90, y0 + 280), C((150, 206, 240)), -1, cv2.LINE_AA)            # see-through tank
        cv2.rectangle(f, (x0 - 90, y0 + 60), (x0 - 90 + 180, y0 + 120), C((214, 236, 250)), -1, cv2.LINE_AA)
        for k in range(3): cv2.circle(f, (x0 + 100, y0 + 330 + 26 * k), 7, C((120, 200, 140) if k == 0 else (200, 206, 210)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x0 - 20, y0 + 420), (x0 + 20, y0 + 470), C((200, 206, 212)), -1, cv2.LINE_AA)            # tap
        cv2.rectangle(f, (x0 - 40, y0 + 440), (x0 + 40, y0 + 460), C((170, 176, 184)), -1, cv2.LINE_AA)
        cv2.rectangle(f, (450, 300), (590, 470), C((252, 250, 244)), -1, cv2.LINE_AA)                              # wall calendar
        cv2.rectangle(f, (450, 300), (590, 340), C((210, 70, 60)), -1)
        for r_ in range(4):
            for c_ in range(5): cv2.rectangle(f, (462 + c_ * 25, 356 + r_ * 26), (478 + c_ * 25, 372 + r_ * 26), C((214, 214, 210)), -1)
        cv2.ellipse(f, (180, top_y - 130), (70, 80), 0, 0, 360, C((178, 186, 196)), -1, cv2.LINE_AA)            # steel matka on a stand
        cv2.ellipse(f, (180, top_y - 214), (34, 12), 0, 0, 360, C((150, 158, 170)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("dining52", blur, top_y), mk).copy()
    god_rays(f, 210, 420, t, amt=0.22, ang0=1.0)
    lamp_glow(f, 210, 600, 520, (255, 226, 170), 0.28)
    dust_motes(f, t, 80, 400, 520, 1200, amt=0.5)
    if dim > 0: f = f * (1 - 0.5 * dim)
    return inkify(f)


def dining_front(f, top_y=DIN_TOP):
    """the dining-table edge (drawn AFTER Chubby): a red-and-white checked plastic table cloth with a scalloped hem, wooden legs below."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 120), C((252, 244, 236)), -1)
    for x in range(0, W, 60):
        for y in range(top_y, top_y + 120, 60):
            if ((x // 60) + (y - top_y) // 60) % 2 == 0: cv2.rectangle(f, (x, y), (x + 60, y + 60), C((220, 96, 92)), -1)
    for x in range(0, W + 60, 60):
        cv2.ellipse(f, (x + 30, top_y + 120), (30, 18), 0, 0, 180, C((252, 244, 236)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (x + 30, top_y + 120), (30, 18), 0, 0, 180, C(INKC), 4, cv2.LINE_AA)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 138), (W, H), C((150, 104, 70)), -1)
    _hatch_band(f, top_y + 140, H)
