# ================= shots: FreshNestHub 38 — "Why does your mouth water when you just look at food?" (Chubby INK; 35-50 s rule; ONE takeaway) ===
# COLOUR SCRIPT: SAFFRON (ACC) = the food, the order, the sugar. Saliva = clear water-blue (SPIT). Story = THE SWEET SHOP (the jalebi tray), the morning
# worktop (the roti test), the lunch table (setting the table); every explanation = the white BOARD. METAPHOR: a restaurant KITCHEN inside you: the brain
# is the head chef who gets the ORDER the moment you see / smell / think of food; the spit glands are taps; amylase is the prep cook with scissors; the
# stomach is the stove that lights before the food arrives.
# Visual upgrade (ep 38): Chubby's MOUTH-WATERING acting: the aroma ribbon hooks his nose and pulls him in nose-first, a saliva drool with anticipation,
# a lip lick, a gulp with a throat bob. Sound skill (ep 38): SOUND PERSPECTIVE (distance by filtering, Doppler fly-bys) in mix.py.
END = round(LINES["c2"]["end"] + 1.33, 3)            # 35-50 s rule: 0.1 s air + 0.6 s logo + 0.63 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "just") - 0.12, "punch"),
    ("S1", T("i2", "You") - 0.12, "cut"), ("S1b", T("i2", "But") - 0.12, "erase"),
    ("S2", T("a1", "The") - 0.1, "cut"), ("S2b", T("a1", "and") - 0.1, "cut"),
    ("S3", T("a2", "And") - 0.1, "erase"), ("S3b", T("a2", "It") - 0.1, "morph"),
    ("S4", T("a3", "Try") - 0.12, "erase"), ("S4b", T("a3", "and") - 0.1, "punch"),
    ("S5", T("b1", "Your") - 0.12, "erase"), ("S5b", T("b2", "In") - 0.1, "cut"),
    ("S6", T("c1", "So") - 0.12, "erase"),
    ("S7", T("c2", "Send") - 0.1, "whip"),
    ("S8", LINES["c2"]["end"] + 0.1, "punch"), ("S9", LINES["c2"]["end"] + 0.7, "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {"S3b": ((560, 1240, 150), (540, 900, 640))}         # the drool drop in S3 -> the big spit drop on the board
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, PAPER, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def flip_el(el): return (el[0][:, ::-1].copy(), el[1][:, ::-1].copy())


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


# ---- the shop cast ----
CX, CY, CS = 390, 1730, 1.6          # Chubby at the sweet-shop counter (counter top 1300)
TOP = 1300
JX, JY = 800, 1236                     # the jalebi tray on the counter
LICK1 = T("i1", "look") - 0.05
GULP1 = T("i1", "food") + 0.35


def jalebi_tray(f, x=JX, y=JY, s=1.0, n=5):
    el_at(f, tray38_el(), x, y + 44 * s, 0.8 * s)
    spots = [(-110, 0), (0, -8), (110, 0), (-55, -62), (55, -66)][:n]
    for j, (dx, dy) in enumerate(spots): el_at(f, jalebi_el(381 + j), x + dx * s, y + dy * s, 0.52 * s, rot=12 * j)


def shop_props(f, t):
    el_at(f, tray_el(), 160, 1250, 0.7)
    for j in range(3): el_at(f, (kalakand_el(), barfi_ink_el(), kaju_ink_el())[j], 70 + j * 90, 1196, 0.32)
    jalebi_tray(f)


def customer(f, t, x=CX, y=CY, s=CS, drool_t0=-0.9, licks=(), gulps=(), expr="love", talking=False, look=(0.8, 0.45), pull=1.0, shirt=None, smell=None):
    """Chubby (or the friend) staring at the jalebi: the aroma pull (lean in nose-first), a drool, lip licks, gulps. Returns his nose tip."""
    g = dict(dy=0.0, squash=0.0, k=-1.0)
    for tg in gulps:
        gg = gulp(t, tg)
        if gg["k"] >= 0 or abs(gg["dy"]) > 0: g = gg
    lean = 9 * pull + 2 * math.sin(t * 1.7)
    kw_ = dict(shirt=shirt) if shirt else {}
    chub(f, x, y + g["dy"], s, t=t, la=(20, 10), ra=(36, 60), mouth=talk(t) if talking else 0, expr=expr, brow="up", look=look, lean=lean, squash=g["squash"],
         hand_r="open", turn=0.45, hair=(-6 * pull, 0), **kw_)
    gulp_mark(f, x, y + g["dy"], s, g["k"])
    if smell is not None:                                                        # the aroma ribbon ends ON his nose tip (drawn over the face)
        nx_, ny_ = nose_xy(x, y + g["dy"], s, t, lean, g["squash"]); scent(f, smell, (nx_ + 4, ny_ - 2), t, -1.0, 1.0, n=3, amp=22)
    mx, my = mouth_xy(x, y + g["dy"], s, t, lean, g["squash"])
    for tl in licks: lick(f, mx, my, s, t, tl)
    if not talking and not any(0 <= t - tl < 0.6 for tl in licks): drool(f, mx, my, s, t, drool_t0, 1.9, 1.0)
    return nose_xy(x, y + g["dy"], s, t, lean, g["squash"])


def hook_band(f, y0=228, y1=690, a=0.62):
    """a soft paper band behind the hook words so they read over the busy shop shelves (feathered edges)."""
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0): WATERS? breathes and drips."""
    kw(f, "DO YOU KNOW WHY", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "YOUR MOUTH", 540, 425, t, t0, "pop", 120, col=INKC, op=op)
    kw(f, "WATERS?", 540, 575, t, t0, "breathe", 150, col=SPIT_S, op=op)
    for j, (dx, ph) in enumerate(((-150, 0.0), (-20, 0.45), (120, 0.8))):       # three drops fall off the letters
        u = ((t + ph) / 1.3) % 1
        if u < 0.75:
            y0 = 640 + 40 * u + 1560 * max(0, u - 0.35) ** 2
            r = 9 + 5 * min(1, u / 0.35)
            cv2.ellipse(f, (int(540 + dx), int(y0)), (int(r * 0.8), int(r * 1.2)), 0, 0, 360, C(SPIT), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(540 + dx), int(y0)), (int(r * 0.8), int(r * 1.2)), 0, 0, 360, C(SPIT_S), 3, cv2.LINE_AA)


# ---- S0: HOOK at frame 0: the sweet shop; a jalebi's aroma has already hooked Chubby's nose, he leans in nose-first, a drool already swelling ----
def shot_S0(t, n):
    f = set_shop(t); f = dof(f, 3)
    customer(f, t, gulps=[GULP1], licks=[LICK1], smell=(JX - 60, JY - 70))
    shop_front(f, TOP, t); shop_props(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S0b: '...when you just look at food?' close-up on his face: eyes locked on the jalebi, a lip lick, the drool lets go, a GULP ----
def shot_S0b(t, n):
    f = set_shop(t); f = dof(f, 6)
    hx, hy, s = 430, 1120, 2.6
    gg = gulp(t, GULP1)
    chub_head_only(f, hx, hy + gg["dy"] * 2, s, t, mouth=0, expr="love", brow="up", look=(0.9, 0.5), turn=0.5)
    mx, my = hx + 78, hy + 192 + gg["dy"] * 2                                     # the right corner of his mouth
    lick(f, mx - 20, my + 4, s * 0.8, t, LICK1, 0.6)
    if not (0 <= t - LICK1 < 0.62): drool(f, mx + 14, my + 6, s * 0.8, t, LICK1 + 0.2, 1.7, 1.0)
    el_at(f, jalebi_el(), 850, 1420, 1.25, rot=8)
    scent(f, (800, 1330), (hx + 62, hy + 108), t, -1, 1.0, n=2, amp=20)
    if gg["k"] >= 0: kw(f, "gulp!", 840, 1060 + 60 * gg["k"], t, GULP1, "pop", 90, col=INKC, stagger=0.03)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S1: 'You haven't taken a single bite.' the counter: his hand stops an inch from the jalebi; 0 BITES ----
def shot_S1(t, n):
    f = set_shop(t); t0 = st_("S1"); tb = T("i2", "bite") - 0.15
    customer(f, t, drool_t0=t0 - 0.4, expr="sus" if t > tb else "love", look=(0.9, 0.5))
    shop_front(f, TOP, t); shop_props(f, t)
    reach = ramp(t, t0 + 0.1, 0.5)
    hx = 520 + 140 * reach - 6 * math.sin(t * 9) * (t > tb)                     # the hand hovers, trembling, and stops short
    grip_hand(f, hx, 1190, 1.3, kind="open")
    if t > tb:
        kw(f, "0 BITES", 540, 430, t, tb, "pop", 150, col=INKC)
        write_on(f, "not one", 540, 560, t, tb + 0.15, 40, ACC_S)
    return finish(f, n, look="golden")


# ---- S1b: '...But your brain's already placed the order.' BOARD: the brain in a chef's toque; an ORDER! ticket slams in ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); tb = T("i2", "brain's") - 0.15; to = T("i2", "order") - 0.1
    if t > tb: brain_chef(f, 540, 1000, 1.7 * max(0.05, snap(t, tb, 4)), t, "happy" if t < to else "wow", (0, -0.4))
    if t > tb: write_on(f, "your brain", 540, 1300, t, tb + 0.15, 48, BP_INK)
    if t > to:
        y = 600 - 260 * (1 - eo(clamp((t - to) / 0.12)))
        el_at(f, ticket_el("ORDER!"), 540, y, 1.35, rot=-6)
        for j in range(6):
            a = math.pi + j * math.pi / 5; r0 = 170 + 60 * ramp(t, to, 0.2)
            cv2.line(f, (int(540 + r0 * math.cos(a)), int(620 + 0.6 * r0 * math.sin(a))), (int(540 + (r0 + 36) * math.cos(a)), int(620 + 0.6 * (r0 + 36) * math.sin(a))), C(ACC_S), 5, cv2.LINE_AA)
    peek(f, t, 860, 1440, 0.42, expr="happy", look=(-0.6, -0.5))
    return finish(f, n, look="fresh")


# ---- S2: 'The sight, the smell, even the thought of food,' BOARD: three triggers draw on in a column, each on its word, arrows into the brain ----
def eye_ico(f, x, y, k):
    draw_on(f, [(x - 70, y), (x, y - 40), (x + 70, y), (x, y + 40), (x - 70, y)], k, BP_INK, 8, seed=21, tip=False)
    if k > 0.8: cv2.circle(f, (x, y), 18, C(BP_INK), -1, cv2.LINE_AA)


def nose_ico(f, x, y, k):
    draw_on(f, [(x - 8, y - 60), (x - 20, y + 10), (x - 46, y + 34), (x - 10, y + 48), (x + 30, y + 40)], k, BP_INK, 8, seed=22, tip=False)
    if k > 0.8:
        for j in range(3): draw_on(f, [(x + 70 + 20 * j + 8 * math.sin(u * 6), y + 50 - 90 * u) for u in np.linspace(0, 1, 8)], 1.0, ACC, 5, seed=30 + j, tip=False)


def think_ico(f, x, y, k):
    draw_ell_on(f, x, y - 10, 70, 46, k, BP_INK, 7, seed=23)
    if k > 0.9:
        for dx, dy, r in ((-60, 52, 12), (-84, 76, 7)): cv2.circle(f, (x + dx, y + dy), r, C(BP_INK), 4, cv2.LINE_AA)
        el_at(f, jalebi_el(), x, y - 10, 0.3)


def shot_S2(t, n):
    f = board_bg(); ts = T("a1", "sight") - 0.12; tm = T("a1", "smell") - 0.12; tt = T("a1", "thought") - 0.12
    brain_chef(f, 760, 900, 1.05, t, "happy", (-0.6, 0))
    rows = [(ts, eye_ico, "sight", 520), (tm, nose_ico, "smell", 860), (tt, think_ico, "thought", 1200)]
    for t1, ico, lab, y in rows:
        if t > t1:
            k = ramp(t, t1, 0.35); ico(f, 230, y, k)
            write_on(f, lab, 230, y + 100, t, t1 + 0.1, 40, BP_INK)
            draw_arrow_on(f, (330, y), (600, 900 + (y - 860) * 0.25), ramp(t, t1 + 0.15, 0.3), ACC_S, 7, 26, bend=0.15)
    return finish(f, n, look="fresh")


# ---- S2b: '...and your brain tells your spit glands, open up.' BOARD: brain -> two nerve lines -> two TAPS (the glands) that turn on and run ----
def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tg = T("a1", "glands") - 0.15; to = T("a1", "open") - 0.08
    brain_chef(f, 540, 520, 1.0, t, "happy", (0, 0.6))
    for sg in (-1, 1):
        x = 540 + sg * 260
        draw_on(f, [(540 + sg * 60, 640), (540 + sg * 140, 760), (x, 860)], ramp(t, t0 + 0.1, 0.5), BP_INK, 6, seed=40 + sg, tip=False)
        ok = ramp(t, to, 0.25)
        tap = tap_el(ok)
        if sg < 0: tap = flip_el(tap)
        el_at(f, tap, x, 960, 1.0, t, tg if sg < 0 else tg + 0.1)
        if t > to:                                                                # saliva runs from the spout
            sx = x + sg * 92; L = 360 * ramp(t, to, 0.4)
            cv2.line(f, (int(sx), 1010), (int(sx), int(1010 + L)), C(SPIT), 26, cv2.LINE_AA)
            cv2.line(f, (int(sx - 13), 1010), (int(sx - 13), int(1010 + L)), C(SPIT_S), 4, cv2.LINE_AA)
            cv2.line(f, (int(sx + 13), 1010), (int(sx + 13), int(1010 + L)), C(SPIT_S), 4, cv2.LINE_AA)
            for j in range(4):
                u = ((t - to) * 1.6 + j / 4) % 1
                cv2.ellipse(f, (int(sx), int(1010 + L * u)), (6, 10), 0, 0, 360, C(SPIT_H), -1, cv2.LINE_AA)
    if t > tg: write_on(f, "spit glands", 540, 1180, t, tg, 50, BP_INK)
    if t > to: kw(f, "OPEN UP!", 540, 1330, t, to, "shake", 110, col=SPIT_S, amp=0.4)
    src(f, SRC_CC, t, t0 + 0.3, 1462)
    return finish(f, n, look="fresh")


# ---- S3: 'And that spit isn't just water.' the shop close-up: the drool hangs from his lip as a long strand with a big drop ----
def shot_S3(t, n):
    f = set_shop(t, 0.05); f = dof(f, 5); t0 = st_("S3"); tw = T("a2", "water") - 0.15
    hx, hy, s = 470, 900, 2.3
    chub_head_only(f, hx, hy, s, t, mouth=0, expr="sus" if t > tw else "love", brow="up", look=(0.2, 0.9), turn=0.2)
    mx, my = hx + 69, hy + 170                                                       # the right corner of his mouth
    sway = 8 * math.sin(t * 2.2)
    L = 180 + 60 * ramp(t, t0, 0.8)
    cv2.line(f, (int(mx), int(my)), (int(mx + sway), int(my + L)), C(SPIT), 14, cv2.LINE_AA)
    cv2.line(f, (int(mx - 7), int(my)), (int(mx + sway - 7), int(my + L)), C(SPIT_S), 3, cv2.LINE_AA)
    dx, dy = mx + sway, my + L + 48
    cv2.ellipse(f, (int(dx), int(dy)), (40, 54), 0, 0, 360, C(SPIT), -1, cv2.LINE_AA); cv2.ellipse(f, (int(dx), int(dy)), (40, 54), 0, 0, 360, C(SPIT_S), 5, cv2.LINE_AA)
    cv2.ellipse(f, (int(dx - 12), int(dy - 18)), (9, 13), 0, 0, 360, C(SPIT_H), -1, cv2.LINE_AA)
    if t > tw:
        kw(f, "JUST WATER?", 540, 380, t, tw, "pop", 110, col=INKC)
        stamp_k = snap(t, tw + 0.6, 3) if t > tw + 0.6 else 0
        if stamp_k > 0:
            for sg in (-1, 1): cv2.line(f, (int(540 - 300 * stamp_k), int(380 - sg * 70 * stamp_k)), (int(540 + 300 * stamp_k), int(380 + sg * 70 * stamp_k)), C((176, 40, 44)), 16, cv2.LINE_AA)
    return finish(f, n, look="golden")


# ---- S3b: 'It carries an enzyme, amylase, that cuts starch into sugar.' BOARD inside a big spit drop: the prep cook snips the starch chain into sugar pairs ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); te = T("a2", "enzyme") - 0.12; ta = T("a2", "amylase") - 0.12; tc = T("a2", "cuts") - 0.1; ts = T("a2", "starch") - 0.12
    tg = T("a2", "sugar") - 0.12
    P = [(540, 380)] + _arcpts(540, 960, 400, 420, -60, 240, 40)                     # the drop outline
    draw_on(f, [(int(x), int(y)) for x, y in P] + [P[0]], ramp(t, t0, 0.45), SPIT_S, 9, seed=50, tip=False)
    if t > te:
        el_at(f, amylase_el("happy" if t < tc else "wow"), 360, 760, 1.5, t, te)
        write_on(f, "amylase", 360, 990, t, ta, 46, SPIT_S)
    if t > ts - 0.2:
        cut = ramp(t, tc, max(0.4, tg + 0.5 - tc))
        sx = starch_chain(f, 200, 1110, 10, t, ts, cut, 60, 22, ramp(t, ts - 0.2, 0.35))
        if t > tc:
            op_ = 0.5 + 0.5 * math.cos(t * 26)
            el_at(f, scissors_el(op_), min(880, sx + 40), 1040, 1.1, rot=-90)
        write_on(f, "starch", 330, 1240, t, ts, 44, STARCH_S)
    if t > tg:
        write_on(f, "= sugar", 740, 1240, t, tg, 52, ACC_S)
    src(f, SRC_CC, t, t0 + 0.6, 1462)
    return finish(f, n, look="fresh")


# ---- S4: 'Try it. Chew a plain bit of roti for a while,' the morning worktop: Chubby tears a bit of roti and chews; a timer ticks ----
WX, WY, WS = 430, 1720, 1.5


def shot_S4(t, n):
    f = set_worktop(t); t0 = st_("S4"); tc = T("a3", "Chew") - 0.1
    chewing = t > tc + 0.3
    rr = scale_el(roti_el(1 if t > tc else 0), 0.95); rr = (cv2.resize(rr[0], (rr[0].shape[1], int(rr[0].shape[0] * 0.42))), cv2.resize(rr[1], (rr[1].shape[1], int(rr[1].shape[0] * 0.42))))
    rot_comp(f, rr, 810, 1300, 0, 1.0, 1.0, 0.0)
    hand_up = ramp(t, tc - 0.05, 0.3) * (1 - ramp(t, tc + 0.4, 0.3))
    chub(f, WX, WY, WS, t=t, la=(24, 12), ra=(70 + 80 * hand_up, 40 + 100 * hand_up), mouth=munch(t) if chewing else talk(t), expr="n" if not chewing else "sus",
         brow="up" if not chewing else "sus", look=(0.6, 0.3) if not chewing else (0, -0.2), hand_r="pinch", turn=0.3, lean=2 + 2 * math.sin(t * 5) * chewing,
         hold=scale_el(roti_el(0), 0.22) if tc < t < tc + 0.5 else None, hold_front=True)
    worktop_front(f, 1330)
    if t < tc: kw(f, "TRY IT", 540, 380, t, t0 + 0.05, "pop", 130, col=INKC)
    if t > tc:
        kw(f, "CHEW...", 540, 380, t, tc, "breathe", 120, col=INKC)
        comp(f, timer_el(clamp((t - tc) / 3.0), "1 MIN"), 830, 760)
    return finish(f, n, look="warm")


# ---- S4b: '...and it starts tasting a little sweet.' face close-up: the chew slows, the eyes go wide, sugar sparkles pop out; SWEET ----
def shot_S4b(t, n):
    f = set_worktop(t, blur=8); f = dof(f, 3); t0 = st_("S4b"); tsw = T("a3", "sweet") - 0.15
    tk = take(t, tsw, 0.8, 7)
    chub_head_only(f, 520, 1060 + tk["dy"], 2.5, t, mouth=munch(t, 0.42) if t < tsw else "o", expr="happy" if t > tsw + 0.5 else (tk["expr"] or "sus"), brow=tk["brow"] or "sus",
                   look=(0, -0.3), turn=0.1)
    if t > tsw:
        r = np.random.default_rng(38)
        for j in range(10):
            a = r.uniform(0, 2 * math.pi); u = clamp((t - tsw) * 1.6 - j * 0.04)
            x = 540 + math.cos(a) * (220 + 260 * u); y = 1020 + math.sin(a) * (180 + 220 * u)
            if 0 < u < 1:
                s_ = 18 * (1 - u) + 6
                cv2.line(f, (int(x - s_), int(y)), (int(x + s_), int(y)), C(ACC), 5, cv2.LINE_AA); cv2.line(f, (int(x), int(y - s_)), (int(x), int(y + s_)), C(ACC), 5, cv2.LINE_AA)
        kw(f, "SWEET!", 540, 420, t, tsw, "pop", 170, col=ACC_S)
        write_on(f, "starch -> sugar", 540, 1390, t, tsw + 0.3, 44, INKC)
    src(f, SRC_SWEET, t, t0 + 0.2, 1462)
    return finish(f, n, look="warm")


# ---- S5: 'Your stomach gets the memo too, and starts making acid before the food even arrives.' BOARD: a memo flies to the stomach, the stove
#      under it lights, acid drops start; the food is still far away at the top of the food pipe ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tm = T("b1", "memo") - 0.15; ta = T("b1", "acid") - 0.12; tf = T("b1", "food") - 0.12
    el_at(f, stomach_ink_el("sus" if t < tm + 0.5 else "happy", (0.4, -0.6)), 560, 1000, 1.55, t, t0 + 0.05)
    draw_on(f, [(470, 260), (470, 600), (500, 760)], ramp(t, t0, 0.4), BP_INK, 7, seed=61, tip=False)
    draw_on(f, [(540, 260), (540, 600), (560, 740)], ramp(t, t0, 0.4), BP_INK, 7, seed=62, tip=False)
    write_on(f, "stomach", 560, 1300, t, t0 + 0.2, 48, BP_INK)
    if t > tm:                                                                       # the memo flies in on an arc
        u = clamp((t - tm) / 0.45); ex = 120 + (700 - 120) * u; ey = 420 + (820 - 420) * u - 200 * math.sin(math.pi * u)
        el_at(f, envelope_el(), ex, ey, 1.1 * (1 - 0.3 * u), rot=-30 * (1 - u))
    if t > ta:
        flames(f, 560, 1240, t, 260, 9, ramp(t, ta, 0.3))
        for j in range(5):
            u = ((t - ta) * 0.9 + j / 5) % 1
            x = 470 + 40 * j; y = 900 + 160 * u
            cv2.ellipse(f, (x, int(y)), (9, 14), 0, 0, 360, C(INK_MINT), -1, cv2.LINE_AA); cv2.ellipse(f, (x, int(y)), (9, 14), 0, 0, 360, C(INKC), 3, cv2.LINE_AA)
        kw(f, "ACID ON", 820, 760, t, ta, "pop", 80, col=INKC)
    if t > tf:                                                                       # the food is still at the top, far away
        el_at(f, jalebi_el(), 505, 300, 0.32, t, tf)
        write_on(f, "food: not here yet", 540, 1400, t, tf + 0.1, 40, ACC_S)
    return finish(f, n, look="fresh")


# ---- S5b: 'In one study, just talking about tasty food for half an hour... more than tripled it.' BOARD: two bars: 4 -> 13 (count up) ----
def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); tt = T("b2", "talking") - 0.15; th = T("b2", "half") - 0.15; tr = T("b2", "tripled") - 0.1
    base_y = 1240; px = 40
    write_on(f, "stomach acid", 540, 300, t, t0 + 0.05, 52, BP_INK)
    draw_on(f, [(170, base_y), (910, base_y)], ramp(t, t0, 0.35), BP_INK, 7, seed=70, tip=False)
    h1 = 4 * px * ramp(t, t0 + 0.3, 0.4)
    cv2.rectangle(f, (250, int(base_y - h1)), (450, base_y), C(BP_GRID2), -1); cv2.rectangle(f, (250, int(base_y - h1)), (450, base_y), C(BP_INK), 6, cv2.LINE_AA)
    write_on(f, "before", 350, base_y + 70, t, t0 + 0.35, 40, BP_INK)
    if t > t0 + 0.6: write_on(f, "4", 350, int(base_y - h1 - 50), t, t0 + 0.6, 56, BP_INK)
    if t > tt:
        peek(f, t, 860, 520, 0.36, expr="happy", look=(-0.4, 0.3))
        write_on(f, "just talking about food", 540, 1400, t, tt, 38, ACC_S)
    if t > th:
        v = count_up(t, th + 0.1, 13, max(0.6, tr - th))
        h2 = v * px
        cv2.rectangle(f, (630, int(base_y - h2)), (830, base_y), C(ACC_L), -1); cv2.rectangle(f, (630, int(base_y - h2)), (830, base_y), C(ACC_S), 6, cv2.LINE_AA)
        write_on(f, "30 min", 730, base_y + 70, t, th, 40, ACC_S)
        kin_word(f, f"{int(round(v))}", 730, int(base_y - h2 - 56), t, th, "pop", 84, ACC_S, stroke=2, stroke_col=INKC)
    if t > tr: kw(f, "x3+", 540, 470, t, tr, "shake", 150, col=ACC_S, amp=0.4)
    src(f, SRC_ACID, t, t0 + 0.3, 1462)
    return finish(f, n, look="fresh")


# ---- S6: 'So a watering mouth isn't greed. It's your body setting the table.' the lunch table: plate, glass, spoon pop on; a napkin tucks in ----
LX, LY, LS = 540, 1730, 1.45


def shot_S6(t, n):
    f = set_lunch(t); tg = T("c1", "greed") - 0.15; ts = T("c1", "setting") - 0.1
    mh = moving_hold(t, 3, 0.8)
    chub(f, LX, LY, LS, t=t, la=(30, 20), ra=(110, 150) if t < ts else (30, 20), mouth=talk(t), expr="smirk" if t < ts else "happy", brow="up", look=(0, 0.2),
         lean=mh["lean"], turn=0.0)
    cloth_front(f, 1330)
    items = [(plate_el(), 540, 1310, 0.95, ts), (glass_el(0.8), 820, 1250, 0.7, ts + 0.22), (spoon_el(), 280, 1320, 0.5, ts + 0.42)]
    for el, x, y, s, ti in items: el_at(f, el, x, y, s, t, ti)
    if tg < t < ts: kw(f, "NOT GREED", 540, 420, t, tg, "pop", 120, col=INKC)
    if t > ts: ui_word(f, "your body is", "[SETTING THE TABLE]", 430, t, ts, col=INKC, acc=ACC_S, size=84, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S7: 'Send this to the friend staring into a sweet shop window right now.' the shop: the FRIEND drooling at the jalebi; Chubby points ----
FRIEND = (236, 150, 110)


def shot_S7(t, n):
    f = set_shop(t)
    customer(f, t, x=660, y=1590, s=1.2, drool_t0=st_("S7") - 0.6, licks=[T("c2", "staring") - 0.05], gulps=[T("c2", "now") - 0.1], look=(0.6, 0.6), shirt=FRIEND)
    dress(f, 660, 1590, 1.2, "cousin")
    chub(f, 230, 1640, 1.05, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="happy", brow="up", look=(1, 0), turn=0.5)
    shop_front(f, TOP, t); jalebi_tray(f, 900, JY, 0.9, 4)
    ui_word(f, "send this to the friend at the", "[SWEET SHOP]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S8: the logo beat (0.6 s) ----
def shot_S8(t, n):
    t0 = st_("S8"); f = set_shop(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.25) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.12) / 0.2))
    return finish(f, n, look="golden")


# ---- S9: the LOOP TAIL: back at the shop exactly like frame 0 (no caption); loop_seam blends into frame 0 ----
def shot_S9(t, n):
    f = set_shop(t); f = dof(f, 3)
    customer(f, t, smell=(JX - 60, JY - 70))
    shop_front(f, TOP, t); shop_props(f, t)
    hook_band(f)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(GULP1, 0.25, 8), (T("i2", "bite") - 0.15, 0.25, 8), (T("i2", "order") - 0.1, 0.4, 16), (T("a1", "open") - 0.08, 0.3, 10),
           (T("a2", "water") + 0.2, 0.3, 10), (T("a2", "cuts") - 0.1, 0.3, 10), (T("a2", "sugar") - 0.12, 0.35, 12), (T("a3", "sweet") - 0.15, 0.4, 16),
           (T("b1", "acid") - 0.12, 0.3, 10), (T("b2", "tripled") - 0.1, 0.45, 18), (T("c1", "greed") - 0.15, 0.25, 8), (T("c1", "table") - 0.1, 0.25, 8)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


_FIRST = {}


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "erase" and dt < 0.42:
            f = erase_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42)
        elif k == "morph" and dt < 0.42:
            a, b = MORPH[sh["id"]]; f = morph_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, a, b)
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    if i == len(SHOTS) - 1:                                                     # the LOOP SEAM: the tail melts into frame 0
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
