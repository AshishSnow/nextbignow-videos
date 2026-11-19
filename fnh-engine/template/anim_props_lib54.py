# ================= anim_props_lib54.py (ep 54) (ep 54, 19 Nov): "Does drinking water while you eat water down your stomach acid?" — ACCENT = ACID LIME
# (the stomach acid, the sensor bells, the acid tap, the question words). Water keeps the clear blue of ep 52 as the story's second colour (only on water).
# NEW PLACE: set_dhaba(t, blur, top_y, dim) = a roadside DHABA at noon (ochre wall, a hand-painted menu board, a big steel WATER DRUM with a tap, a glowing
# tandoor, a string of bulbs, a neem tree past the open side) + dhaba_front(f, top_y) = the long wooden table edge drawn AFTER the people.
# NEW CHARACTER: uncle(f, ...) = THAT UNCLE (chub + cream kurta + a thick moustache + a bald crown with grey sides + a watch).
# CRAFT (ep 54, now in anim_fx.py) = LIQUID FX ANIMATION (2D effects animation of water): splash_crown / pour_stream / fly_drops2 / ripples — the splash curves UP and OUT
# (never straight up and down), every tongue + drop has its own speed (uneven timing: water that all lands together looks 'heavy like mud'), drops that
# break off keep the splash's energy (same velocity at the break), big / medium / small drops, and the splash ends in micro-splashes + ripples that slow
# down instead of stopping. A pour stream NARROWS as it falls (it speeds up, so the same water gets thinner), wobbles in waves that travel down it, and
# lands in a small continuous splash. =================
ACC = (150, 190, 30); ACC_S = (92, 126, 10); ACC_L = (214, 236, 150); ACC_XL = (240, 248, 214)   # acid lime = stomach acid / the question
ACID = (186, 214, 60); ACID_S = (120, 156, 20)
WAT = (150, 206, 246); WAT_S = (84, 160, 222); WAT_H = (240, 250, 255)
RED = (176, 40, 44)
KURTA = (238, 232, 214)
SRC_MAYO54 = "Source: Mayo Clinic (2025); Hackensack Meridian Health"
SRC_PHYS54 = "Source: StatPearls 'Physiology, Stomach' (NCBI / NIH)"
SRC_BLOAT54 = "Source: Mayo Clinic; Dr Manan Vora via India TV (2026)"
SC3 = 3


def _P(pts): return [(x * SC3, y * SC3) for x, y in pts]


def _blend(f, ov, op):
    if op >= 0.999: f[:] = ov
    else: f[:] = f * (1 - op) + ov * op


# ---------------- props (ink language) ----------------
def drum_el(seed=541):
    """the dhaba's big steel WATER DRUM with a brass tap near the bottom and a steel lid."""
    def mk():
        w, h = 300, 420; im, d, S = _cv(w, h)
        body = [(40, 60), (260, 60), (266, 380), (34, 380)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(190, 40, 300, 400), fill=c), STEEL_S, 120)
        _hatch_in(im, (196, 64, 262, 376), lambda q, S_: q.polygon(_P(body), fill=255), -40, 9, 34)
        for y in (120, 250): d.line(S(40, y, 262, y), fill=STEEL_S + (220,), width=4 * SC3)
        d.polygon(_P([(80, 70), (96, 70), (92, 370), (76, 370)]), fill=STEEL_H + (220,))
        _ink_ell(d, 150, 60, 112, 22, (196, 204, 212), seed + 1, INK_W - 1, amp=0.6)
        _ink_ell(d, 150, 46, 30, 10, STEEL_S, seed + 2, INK_W - 2, amp=0.5)
        _ink_poly(d, [(140, 320), (196, 320), (196, 338), (176, 338), (176, 360), (160, 360), (160, 338), (140, 338)], (214, 170, 70), seed + 3, 4, amp=0.4)
        return _done(im, w, h)
    return gcache(("drum54", seed), mk)


def jug54_el(seed=542, mood=None):
    """a steel water JUG (dhaba style: round belly, tall neck, a spout lip and a loop handle) - generic, no brand."""
    def mk():
        w, h = 240, 300; im, d, S = _cv(w, h)
        body = [(70, 60), (150, 60), (150, 110), (196, 170), (196, 250), (160, 286), (60, 286), (24, 250), (24, 170), (70, 110)]
        _ink_poly(d, body, STEEL, seed, INK_W, amp=0.8)
        _shade(im, lambda q, S_: q.polygon(_P(body), fill=255), lambda q, S_, c: q.rectangle(S_(130, 40, 240, 300), fill=c), STEEL_S, 120)
        _ink_poly(d, [(66, 60), (40, 40), (76, 48)], STEEL, seed + 1, 5, amp=0.4)                     # spout lip (left)
        d.arc(S(170, 110, 236, 230), -90, 90, fill=INKC + (255,), width=10 * SC3)                    # handle
        d.arc(S(170, 110, 236, 230), -90, 90, fill=STEEL_S + (255,), width=5 * SC3)
        d.polygon(_P([(56, 170), (66, 170), (62, 270), (52, 270)]), fill=STEEL_H + (220,))
        if mood: _face(d, S, 110, 200, 1.2, mood)
        return _done(im, w, h)
    return gcache(("jug54", seed, mood), mk)


def menu_board_el(seed=543):
    """a hand-painted dhaba menu board (green with yellow letters): DAL / ROTI / CHAI / LASSI with prices as squiggles."""
    def mk():
        w, h = 300, 220; im, d, S = _cv(w, h)
        _ink_poly(d, [(12, 12), (288, 12), (288, 208), (12, 208)], (46, 110, 76), seed, 6, amp=0.6)
        fnt = font(F_HAND, 30 * SC3)
        for j, tx in enumerate(("DAL", "ROTI", "CHAI", "LASSI")):
            if fnt: d.text((30 * SC3, (24 + 44 * j) * SC3), tx, font=fnt, fill=(250, 214, 90, 255))
            d.line(S(170, 46 + 44 * j, 260, 46 + 44 * j), fill=(250, 214, 90, 255), width=4 * SC3)
        return _done(im, w, h)
    return gcache(("menu54", seed), mk)


def acid_tap_el(open_k=0.0, seed=544):
    """the ACID TAP on the board: an ink tap (handle turns with open_k), lime drip ready at the nozzle."""
    ok = round(clamp(open_k) * 6) / 6
    def mk():
        w, h = 240, 200; im, d, S = _cv(w, h)
        _ink_poly(d, [(0, 70), (120, 70), (150, 92), (170, 150), (140, 150), (126, 106), (0, 106)], (212, 216, 224), seed, INK_W, amp=0.6)
        _shade(im, lambda q, S_: q.polygon(_P([(0, 92), (120, 92), (150, 150), (0, 106)]), fill=255), lambda q, S_, c: q.rectangle(S_(0, 92, 240, 200), fill=c), STEEL_S, 120)
        a = math.radians(-90 + 80 * ok)
        cx, cy = 96, 60
        d.line(S(cx, cy, cx + 70 * math.cos(a), cy + 70 * math.sin(a)), fill=INKC + (255,), width=16 * SC3)
        d.line(S(cx, cy, cx + 70 * math.cos(a), cy + 70 * math.sin(a)), fill=ACC + (255,), width=9 * SC3)
        _ink_ell(d, cx, cy, 16, 16, (212, 216, 224), seed + 1, 5, amp=0.3)
        return _done(im, w, h)
    return gcache(("acidtap54", ok, seed), mk)


# ---------------- other people: THAT UNCLE ----------------
def uncle(f, x, y, s, t, la=(24, 12), ra=(24, 12), hand_l="open", hand_r="open", mouth=0, expr="n", brow="sus", look=(0, 0), turn=0.0, lean=0.0,
          hold=None, hold_off=(0, 0), hold_front=False, sit=False):
    """THAT UNCLE: chub with a cream kurta (shirt), a bald crown with grey side hair, a thick black moustache, a steel watch."""
    kw_ = dict(hold=hold, hold_off=hold_off, hold_front=hold_front) if hold is not None else {}
    chub(f, x, y, s, t=t, shirt=KURTA, la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=mouth, expr=expr, brow=brow, look=look, turn=turn, lean=lean, sit=sit, **kw_)
    hx, hy = x + lean * 2 * s + turn * 14 * s, y - 420 * s
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INK_SKIN), -1, cv2.LINE_AA)  # bald crown
    cv2.ellipse(f, (int(hx), int(hy - 70 * s)), (int(84 * s), int(46 * s)), 0, 180, 360, C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    for sg in (-1, 1):                                                                                                 # grey side tufts
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(22 * s), int(36 * s)), 0, 0, 360, C((200, 200, 204)), -1, cv2.LINE_AA)
        cv2.ellipse(f, (int(hx + sg * 86 * s), int(hy - 40 * s)), (int(22 * s), int(36 * s)), 0, 0, 360, C(INKC), max(2, int(3 * s)), cv2.LINE_AA)
    mx = hx + turn * 18 * s + look[0] * 4 * s; my = hy + 40 * s                                                       # the moustache
    M = np.int32([(mx - 58 * s, my + 12 * s), (mx - 30 * s, my - 10 * s), (mx, my - 4 * s), (mx + 30 * s, my - 10 * s), (mx + 58 * s, my + 12 * s), (mx + 30 * s, my + 6 * s), (mx, my + 10 * s), (mx - 30 * s, my + 6 * s)])
    cv2.fillPoly(f, [M], C((52, 40, 34)), cv2.LINE_AA)


# ---------------- NEW PLACE: the DHABA at noon ----------------
DHA_TOP = 1330


def set_dhaba(t=0.0, blur=5, top_y=DHA_TOP, dim=0.0):
    """THE DHABA: warm ochre wall with a lighter plaster band, a hand-painted menu board, a big steel water drum with a tap on a stand (right),
    an open side with a neem tree in noon sun (left), a glowing tandoor mouth (far right, low), a sagging string of bulbs. Paper-softened."""
    def mk():
        f = _vgrad((244, 214, 160), (224, 182, 124), 0, top_y)
        cv2.rectangle(f, (0, 0), (W, 200), C((196, 150, 100)), -1)                                                    # roof beam shadow
        for x in range(0, W, 140): cv2.rectangle(f, (x, 150), (x + 26, 230), C((150, 104, 70)), -1)                 # rafters
        cv2.rectangle(f, (0, top_y - 140), (W, top_y), C((214, 168, 114)), -1)                                       # dado
        cv2.rectangle(f, (40, 330), (330, 900), C((252, 238, 196)), -1, cv2.LINE_AA)                                 # the open side: bright noon
        for j, (cx, cy, rr) in enumerate(((120, 560, 120), (250, 500, 140), (200, 650, 110), (300, 640, 90))):
            cv2.circle(f, (cx, cy), rr, C((150, 196, 120) if j % 2 else (130, 180, 104)), -1, cv2.LINE_AA)          # neem crown
        cv2.rectangle(f, (180, 680), (210, 900), C((140, 104, 76)), -1)
        cv2.rectangle(f, (40, 820), (330, 900), C((226, 206, 160)), -1)                                              # road
        cv2.rectangle(f, (40, 330), (330, 900), C((150, 104, 70)), 14, cv2.LINE_AA)
        ex = menu_board_el(); comp(f, ex, 560, 520)
        cv2.rectangle(f, (760, 860), (1000, top_y - 140), C((150, 104, 70)), -1)                                     # drum stand
        comp(f, scale_el(drum_el(), 0.95), 880, 680)
        cv2.circle(f, (1010, top_y - 60), 120, C((150, 90, 60)), -1, cv2.LINE_AA)                                    # tandoor (clay)
        cv2.ellipse(f, (1010, top_y - 150), (70, 26), 0, 0, 360, C((60, 30, 20)), -1, cv2.LINE_AA)
        f = _soft(f, blur)
        return np.clip(f, 0, 1).astype(np.float32)
    f = gcache(("dhaba54", blur, top_y), mk).copy()
    for j in range(9):                                                                                               # string of bulbs (sway)
        u = j / 8; bx = 380 + 640 * u; by = 250 + 70 * math.sin(math.pi * u) + 4 * math.sin(t * 2 + j)
        cv2.circle(f, (int(bx), int(by)), 9, C((255, 236, 170)), -1, cv2.LINE_AA)
        glow(f, bx, by, 40, (255, 220, 150), 0.10)
    lamp_glow(f, 1010, top_y - 150, 260, (255, 150, 80), 0.18 + 0.03 * math.sin(t * 7))
    god_rays(f, 180, 360, t, amt=0.18, ang0=0.9)
    dust_motes(f, t, 80, 380, 600, 1200, amt=0.5)
    if dim > 0: f = f * (1 - 0.5 * dim)
    return inkify(f)


def dhaba_front(f, top_y=DHA_TOP):
    """the long dhaba TABLE edge (drawn AFTER the people): a thick wooden plank top with grain, a steel strip, a bench below."""
    cv2.rectangle(f, (0, top_y), (W, top_y + 70), C((176, 120, 72)), -1)
    for y in (top_y + 22, top_y + 46): cv2.line(f, (0, y), (W, y), C((150, 100, 60)), 3, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 70), (W, top_y + 84), C((206, 212, 220)), -1)
    cv2.line(f, (0, top_y), (W, top_y), C(INKC), 6, cv2.LINE_AA); cv2.line(f, (0, top_y + 84), (W, top_y + 84), C(INKC), 5, cv2.LINE_AA)
    cv2.rectangle(f, (0, top_y + 84), (W, H), C((120, 84, 56)), -1)
    _hatch_band(f, top_y + 90, H)
