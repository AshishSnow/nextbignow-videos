# ================= shots: FreshNestHub 52 — "Does drinking water standing up hurt your knees?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: warm afternoon home (sunny mint dining corner) for the story; white board + blue ink for the explanation; ONE accent = CLEAR WATER BLUE
# (the water, the question, the joint fluid). Blood = the one red, only on the vessel. The myth's waterfall is drawn in red (wrong), the truth in blue.
# Story: Chubby drinks standing at the dining table, NANI shouts 'sit down!', the bone doctor says myth; the board shows the myth (a waterfall into the
# knees), then the truth: the food pipe is a MUSCLE that squeezes every sip down in a wave (the FOLLOW CAMERA rides one sip down the tall board),
# any posture works (stand / sit / lie down), even astronauts drink with no 'up'; the gut soaks the water into the blood; the knee's slippery joint fluid
# is made from blood -> posture doesn't matter. Knees hurt? a doctor; the glass is NOT GUILTY. Send line = nani's 'sit down!' (loops to frame 0).
END = round(LINES["c2"]["end"] + 1.33, 3)            # 0.1 s air + 0.6 s logo + 0.63 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "really") - 0.12, "punch"),
    ("S1", T("i2", "Your") - 0.12, "whip"), ("S1b", T("i2", "Bone") - 0.1, "cut"),
    ("S2", T("a1", "The") - 0.12, "erase"),
    ("S3", T("a2", "But") - 0.12, "erase"), ("S3b", T("a2", "It's") - 0.1, "cut"),
    ("S4", T("a3", "Standing,") - 0.12, "erase"),
    ("S5", T("a3", "Astronauts") - 0.12, "whip"),
    ("S6", T("b1", "And") - 0.12, "erase"),
    ("S7", T("b2", "Their") - 0.12, "erase"), ("S7b", T("b2", "so") - 0.1, "whip"),
    ("S8", T("c1", "If") - 0.12, "cut"),
    ("S9", T("c2", "Send") - 0.1, "punch"),
    ("S10", LINES["c2"]["end"] + 0.1, "punch"), ("S11", LINES["c2"]["end"] + 0.7, "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
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


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


def hook_band(f, y0=228, y1=700, a=0.7):
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "WATER STANDING UP", 540, 425, t, t0, "pop", 80, col=ACC_S, op=op)
    kw(f, "= BAD KNEES?", 540, 590, t, t0, "shake", 132, col=(176, 40, 44), amp=0.35, op=op)


CX, CY, CS = 400, 1700, 1.55            # Chubby at the dining table (table top 1330)


def drinker(f, t, x=CX, y=CY, s=CS, sip=1.0, level=0.6, expr="happy", brow="n", look=(0.3, -0.3), mouth=None, gulp_t=None, shirt=None, lean=0.0):
    """Chubby (standing) with a steel tumbler: sip 1 = tipped at the mouth (gulping), 0 = held at the chest."""
    ra = (150 - 70 * (1 - sip), -128 + 150 * (1 - sip))
    gl = _rot_el(scale_el(steel_glass_el(level), 0.62), 32 * sip)
    gb = 0.0
    if gulp_t is not None and sip > 0.5: gb = 6 * max(0.0, math.sin((t - gulp_t) * 2 * math.pi / 0.55))       # the throat bobs per gulp
    kw_ = dict(shirt=shirt) if shirt else {}
    chub(f, x, y - gb, s, t=t, la=(26, 14), ra=ra, hold=gl, hold_off=(-38 * sip - 6 * (1 - sip), -18 * sip - 24 * (1 - sip)), hold_front=True, hand_r="grip",
         mouth=(mouth if mouth is not None else (0 if sip > 0.5 else talk(t))), expr=expr, brow=brow, look=look, turn=0.3, lean=lean, squash=0.02 * gb / 6, **kw_)


def gulp_marks(f, t, x=CX, y=CY, s=CS):
    """little 'glug' arcs at the throat while he drinks."""
    k = (t * 1.8) % 1
    for j in range(2):
        r = int((18 + 22 * ((k + j * 0.5) % 1)) * s)
        cv2.ellipse(f, (int(x + 10 * s), int(y - 300 * s)), (r, int(r * 0.6)), 0, 200, 340, C(ACC_S), max(2, int(4 * s)), cv2.LINE_AA)


def doctor(f, x, y, s, t, ok=False, xray=True):
    """the bone doctor: white coat (shirt), stethoscope, a knee X-ray film held up."""
    chub(f, x, y, s, t=t, shirt=(246, 248, 250), la=(24, 12), ra=(150, 170) if xray else (40, 30), hand_r="grip" if xray else "open",
         hold=scale_el(xray_knee_el(), 0.62) if xray else None, hold_off=(-20, -240), hold_front=True,
         mouth=talk(t), expr="smirk" if ok else "n", brow="up", look=(-1, 0), turn=-0.5, lean=-2)
    hx_ = x - 2 * s; cy_ = y - 320 * s
    cv2.ellipse(f, (int(hx_), int(cy_ - 40 * s / 1.5)), (int(70 * s / 1.5), int(60 * s / 1.5)), 0, 0, 180, C((70, 76, 90)), 8, cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 40 * s / 1.5), int(cy_ + 40 * s / 1.5)), int(16 * s / 1.5), C((180, 186, 196)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx_ + 40 * s / 1.5), int(cy_ + 40 * s / 1.5)), int(16 * s / 1.5), C(INKC), 4, cv2.LINE_AA)


# ---- S0: HOOK at frame 0: the dining corner, Chubby GULPING water standing up, nani already pointing 'sit!'; the question as moving words ----
def scene0(f, t, words=True):
    nani(f, 820, 1700, 1.4, t, la=(120, 140), ra=(24, 12), hand_l="point", mouth=2, expr="angry", brow="sus", look=(-1, 0), turn=-0.5, lean=3 * math.sin(t * 9))
    drinker(f, t, sip=1.0, gulp_t=0.0, look=(0.2, -0.5))
    gulp_marks(f, t)
    dining_front(f)
    el_at(f, steel_glass_el(0.9), 640, 1270, 0.55)


def shot_S0(t, n):
    f = set_dining(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S0b: '...really hurts your knees?' close-up: still gulping, his EYES slide down to his knees (eye lead), a red '?' crack flickers on the knee ----
def shot_S0b(t, n):
    f = set_dining(t, 9); f = dof(f, 3); t0 = st_("S0b")
    look = (0.2, -0.5 + 1.4 * clamp((t - t0 - 0.15) / 0.2))
    drinker(f, t, x=480, y=2160, s=2.3, sip=1.0, gulp_t=t0, expr="wow" if t > t0 + 0.3 else "happy", brow="up", look=look)
    if t > T("i1", "knees?") - 0.15:
        k = ramp(t, T("i1", "knees?") - 0.15, 0.25)
        kw(f, "?", 880, 960, t, T("i1", "knees?") - 0.1, "shake", 170, col=(196, 40, 44), amp=0.5)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S1: 'Your nani swears it does.' NANI close: wagging finger, hand on her heart on 'swears'; YES IT DOES! ----
def shot_S1(t, n):
    f = set_dining(t, 8); f = dof(f, 2); t0 = st_("S1"); ts = T("i2", "swears") - 0.1
    swear = t > ts
    wag = 10 * math.sin(t * 13)
    nani(f, 560, 2000, 2.1, t, la=(120 + wag, 150) if not swear else (60, -120), ra=(24, 12), hand_l="point" if not swear else "open",
         mouth=talk(t), expr="angry", brow="sus", look=(0.3, -0.1), turn=0.2, lean=wag * 0.15)
    kw(f, "NANI SAYS", 540, 340, t, t0 + 0.05, "pop", 90, col=INKC)
    if swear: kw(f, "YES, IT DOES!", 540, 480, t, ts, "shake", 116, col=(176, 40, 44), amp=0.4)
    return finish(f, n, look="golden")


# ---- S1b: 'Bone doctors say it's a myth.' the doctor holds up a knee X-ray; MYTH stamp; nani's jaw drops ----
def shot_S1b(t, n):
    f = set_dining(t); t0 = st_("S1b"); tm = T("i2", "myth.") - 0.1
    nani(f, 240, 1680, 1.35, t, mouth="jaw" if t > tm else 0, expr="wow" if t > tm else "sus", brow="up", look=(1, 0), turn=0.5)
    doctor(f, 640, 1700, 1.5, t, ok=t > tm)
    dining_front(f)
    kw(f, "BONE DOCTORS", 540, 330, t, t0 + 0.05, "pop", 96, col=INKC)
    if t > tm: el_at(f, vstamp_el("MYTH", (176, 40, 44), 120), 540, 520, 1.0, t, tm, rot=-6)
    src(f, SRC_MYTH52, t, t0 + 0.4)
    return finish(f, n, look="golden")


# ---- S2: 'The idea is, water drunk standing falls straight down and slams into your knees.' BOARD: the MYTH as a picture ----
BODY = [(470, 520), (420, 560), (420, 640), (360, 690), (330, 1000), (380, 1010), (400, 790), (420, 1040), (430, 1440), (520, 1440), (540, 1100),
        (560, 1440), (650, 1440), (660, 1040), (680, 790), (700, 1010), (750, 1000), (720, 690), (660, 640), (660, 560), (610, 520)]


def board_body(f, t, t0, k=None):
    kd = ramp(t, t0, 0.5) if k is None else k
    draw_ell_on(f, 540, 440, 86, 96, kd, BP_INK, 7, seed=520)
    draw_on(f, BODY, kd, BP_INK, 7, seed=521, tip=kd < 1)
    if kd > 0.8:
        for x in (475, 605): draw_ell_on(f, x, 1240, 44, 36, clamp((kd - 0.8) / 0.2), BP_INK, 5, seed=522 + x)     # the knees
    return kd


def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tf = T("a1", "falls") - 0.12; tsl = T("a1", "slams") - 0.1
    board_body(f, t, t0)
    write_on(f, "the myth", 540, 300, t, t0 + 0.2, 48, (176, 40, 44))
    if t > tf:
        k = ramp(t, tf, max(0.2, tsl - tf))
        yb = 500 + (1200 - 500) * k
        for j, dx in enumerate((-14, 0, 14)):                                           # the waterfall, wavy lines falling
            pts = [(540 + dx + 6 * math.sin(y * 0.05 + t * 14 + j), y) for y in np.linspace(500, yb, 24)]
            cv2.polylines(f, [np.int32(pts)], False, C((200, 70, 70)), 6, cv2.LINE_AA)
    if t > tsl:
        u = clamp((t - tsl) / 0.6)
        for j in range(10):                                                              # SPLASH on both knees
            a = math.pi + j * math.pi / 9; r = 40 + 120 * u
            for kx in (475, 605):
                cv2.circle(f, (int(kx + r * math.cos(a) * 0.8), int(1220 + r * math.sin(a) * 0.6 - 60 * u * (1 - u) * 4)), 9, C((200, 70, 70)), -1, cv2.LINE_AA)
        kw(f, "SPLASH! CRACK?", 540, 1440, t, tsl, "shake", 96, col=(176, 40, 44), amp=0.5)
    return finish(f, n, look="fresh")


# ---- S3: 'But your food pipe isn't a slide.' BOARD: a playground SLIDE with a drop sliding down it, then a fat red X on 'slide' ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); tx = T("a2", "slide.") - 0.05
    k = ramp(t, t0, 0.5)
    draw_on(f, [(260, 1300), (260, 620), (380, 620)], k, BP_INK, 9, seed=530, tip=False)
    for j in range(6): draw_on(f, [(230, 700 + 100 * j), (300, 700 + 100 * j)], clamp(k * 2 - 0.3 - 0.1 * j), BP_INK, 6, seed=531 + j, tip=False)
    S_ = [(380, 620), (520, 760), (680, 1020), (800, 1220), (900, 1280)]
    draw_on(f, S_, clamp(k * 1.3 - 0.2), BP_INK, 12, seed=540, tip=False)
    u = clamp((t - t0 - 0.35) / 1.1)
    if u > 0:
        P, e = _cut_poly(S_, eio(u) * 0.98)
        el_at(f, wdrop_el("happy", (0.6, 0.4)), e[0], e[1] - 50, 0.55, rot=-30)
    write_on(f, "your food pipe?", 540, 360, t, t0 + 0.1, 50, BP_INK)
    if t > tx:
        kx = ramp(t, tx, 0.18)
        draw_on(f, [(220, 560), (900, 1340)], kx, (196, 40, 44), 22, seed=545, tip=False)
        draw_on(f, [(900, 560), (220, 1340)], kx, (196, 40, 44), 22, seed=546, tip=False)
        kw(f, "NOT A SLIDE", 540, 1440, t, tx + 0.05, "pop", 104, col=(176, 40, 44))
    return finish(f, n, look="fresh")


# ---- S3b: 'It's a muscle, and it squeezes every sip down in a wave.' THE FOLLOW CAMERA on a TALL board ----
TALL = 3600
PIPE_X = 540; PIPE_Y0, PIPE_Y1 = 760, 3020


def tall_board():
    def mk():
        a = board_bg(); b = np.concatenate([a, a, a[: TALL - 2 * H]], 0)
        hd = [(PIPE_X + 140 * math.cos(q), 470 + 170 * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 50)]
        cv2.polylines(b, [np.int32(hd)], True, C(BP_INK), 7, cv2.LINE_AA)
        cv2.ellipse(b, (PIPE_X, 560), (44, 30), 0, 0, 360, C(BP_INK), 6, cv2.LINE_AA)
        for sg in (-1, 1): cv2.circle(b, (PIPE_X + sg * 55, 430), 12, C(BP_INK), -1, cv2.LINE_AA)
        for sg in (-1, 1):
            cv2.polylines(b, [np.int32([(PIPE_X + sg * 80, 630), (PIPE_X + sg * 80, 820), (PIPE_X + sg * 380, 900), (PIPE_X + sg * 420, 3500)])], False, C(BP_GRID2), 5, cv2.LINE_AA)
        st = [(PIPE_X - 30, 3020), (PIPE_X - 210, 3080), (PIPE_X - 250, 3300), (PIPE_X - 60, 3440), (PIPE_X + 200, 3400), (PIPE_X + 240, 3200), (PIPE_X + 30, 3020)]
        cv2.polylines(b, [np.int32(st)], True, C(BP_INK), 8, cv2.LINE_AA)
        return b
    return gcache(("tall52",), mk).copy()


def sip_y(t):
    t0 = st_("S3b") + 0.25; t1 = T("a2", "wave.") + 0.25
    return PIPE_Y0 + (PIPE_Y1 + 140 - PIPE_Y0) * eio(clamp((t - t0) / (t1 - t0)))


def _rad(y, yd):
    sq = math.exp(-((y - (yd - 120)) / 70) ** 2) if yd < PIPE_Y1 + 100 else 0.0
    return 46 * (1 - 0.72 * sq) + 8 * math.exp(-((y - yd) / 60) ** 2), sq


def shot_S3b(t, n):
    t0 = st_("S3b"); b = tall_board()
    yd = sip_y(t)
    ys = np.arange(PIPE_Y0, PIPE_Y1 + 1, 18)
    for sg in (-1, 1):                                                                             # the pipe walls; pinched behind the sip = the squeeze
        for y in ys[:-1]:
            r0, sq = _rad(y, yd); r1, _ = _rad(y + 18, yd)
            cv2.line(b, (int(PIPE_X + sg * r0), int(y)), (int(PIPE_X + sg * r1), int(y + 18)), C(_mix(BP_INK, (200, 70, 70), sq)), 8, cv2.LINE_AA)
    for y in ys[::3]:                                                                              # muscle rings
        r0, sq = _rad(y, yd)
        cv2.ellipse(b, (PIPE_X, int(y)), (int(r0 + 12), 10), 0, 0, 360, C(_mix(BP_GRID2, (220, 110, 110), sq)), 3, cv2.LINE_AA)
    if yd < PIPE_Y1 + 100:
        cv2.ellipse(b, (PIPE_X, int(yd)), (34, 44), 0, 0, 360, C(ACC), -1, cv2.LINE_AA)
        cv2.ellipse(b, (PIPE_X, int(yd)), (34, 44), 0, 0, 360, C(ACC_S), 4, cv2.LINE_AA)
        cv2.ellipse(b, (PIPE_X - 10, int(yd - 14)), (9, 6), 0, 0, 360, C((255, 255, 255)), -1, cv2.LINE_AA)
        for sg in (-1, 1):
            cv2.arrowedLine(b, (int(PIPE_X + sg * 170), int(yd - 190)), (int(PIPE_X + sg * 72), int(yd - 125)), C((200, 70, 70)), 7, cv2.LINE_AA, tipLength=0.35)
    if yd > PIPE_Y1:
        pool = clamp((yd - PIPE_Y1) / 140)
        cv2.ellipse(b, (PIPE_X, 3330), (int(150 * pool) + 1, int(46 * pool) + 1), 0, 0, 360, C(ACC), -1, cv2.LINE_AA)
    cy = follow_cam(t, sip_y, t0, lag=0.25, lead=260, vmax=900, dead=30, delay=3 / 24, lo=H / 2, hi=TALL - H / 2)
    y0 = int(round(cy - H / 2)); f = b[y0:y0 + H].copy()
    tm = T("a2", "muscle,") - 0.12
    if t > tm: kw(f, "IT'S A MUSCLE", 540, 330, t, tm, "pop", 110, col=(176, 40, 44))
    if t > T("a2", "squeezes") - 0.1: kw(f, "SQUEEZE... IN A WAVE", 540, 1420, t, T("a2", "squeezes") - 0.1, "breathe", 80, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S4: 'Standing, sitting, lying down, it works the same.' BOARD: three outline people, each with the pipe + a sip; a tick on each word ----
def mini_pipe(f, pts, t, t0, k):
    draw_on(f, pts, k, ACC_S, 5, seed=int(pts[0][0]), tip=False)
    if k >= 1:
        u = ((t - t0) * 0.9) % 1
        P, e = _cut_poly(pts, u)
        cv2.circle(f, (int(e[0]), int(e[1])), 14, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(e[0]), int(e[1])), 14, C(ACC_S), 3, cv2.LINE_AA)


def tick(f, x, y, k):
    draw_on(f, [(x - 34, y), (x - 8, y + 28), (x + 40, y - 34)], k, (40, 140, 80), 12, seed=int(x), tip=False)


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4")
    ts, tsi, tl, tsame = T("a3", "Standing,") - 0.1, T("a3", "sitting,") - 0.1, T("a3", "lying") - 0.1, T("a3", "same.") - 0.1
    k1 = ramp(t, ts, 0.4)
    draw_ell_on(f, 200, 640, 50, 56, k1, BP_INK, 6, seed=550)
    draw_on(f, [(200, 700), (200, 1000), (160, 1230)], k1, BP_INK, 7, seed=551, tip=False); draw_on(f, [(200, 1000), (240, 1230)], k1, BP_INK, 7, seed=552, tip=False)
    draw_on(f, [(130, 900), (200, 760), (270, 900)], k1, BP_INK, 7, seed=553, tip=False)
    mini_pipe(f, [(200, 670), (206, 760), (206, 880)], t, ts, k1)
    if t > ts + 0.25: tick(f, 200, 1330, ramp(t, ts + 0.25, 0.2))
    k2 = ramp(t, tsi, 0.4)
    draw_ell_on(f, 520, 720, 50, 56, k2, BP_INK, 6, seed=560)
    draw_on(f, [(520, 780), (520, 1020), (650, 1020), (650, 1230)], k2, BP_INK, 7, seed=561, tip=False)
    draw_on(f, [(450, 1040), (690, 1040)], k2, BP_GRID2, 6, seed=562, tip=False); draw_on(f, [(450, 1040), (450, 1230)], k2, BP_GRID2, 6, seed=563, tip=False)
    draw_on(f, [(450, 1040), (450, 780)], k2, BP_GRID2, 6, seed=564, tip=False)
    mini_pipe(f, [(520, 750), (526, 840), (526, 960)], t, tsi, k2)
    if t > tsi + 0.25: tick(f, 540, 1330, ramp(t, tsi + 0.25, 0.2))
    k3 = ramp(t, tl, 0.4)
    draw_ell_on(f, 780, 1130, 50, 46, k3, BP_INK, 6, seed=570)
    draw_on(f, [(830, 1130), (1000, 1130), (1010, 1180)], k3, BP_INK, 7, seed=571, tip=False)
    draw_on(f, [(720, 1190), (1020, 1190)], k3, BP_GRID2, 8, seed=572, tip=False)
    mini_pipe(f, [(800, 1124), (870, 1122), (940, 1124)], t, tl, k3)
    if t > tl + 0.25: tick(f, 880, 1330, ramp(t, tl + 0.25, 0.2))
    kw(f, "STAND  SIT  LIE DOWN", 540, 340, t, t0 + 0.05, "pop", 74, col=INKC)
    if t > tsame: kw(f, "SAME SQUEEZE", 540, 470, t, tsame, "breathe", 110, col=ACC_S)
    src(f, SRC_PIPE52, t, t0 + 0.6)
    return finish(f, n, look="fresh")


# ---- S5: 'Astronauts drink with no up at all.' THE CAPSULE: Chubby floats in a jumpsuit; a wobbling ball of water drifts to his mouth ----
def shot_S5(t, n):
    f = set_capsule(t); t0 = st_("S5"); tn = T("a3", "no") - 0.1
    capsule_front(f)
    u = t - t0
    bx, by = 860 - 260 * eio(clamp(u / 1.6)), 760 + 30 * math.sin(u * 2)
    sip = clamp((u - 1.6) / 0.6)
    fl = 22 * math.sin(u * 1.6)
    chub(f, 470, 1180 + fl, 1.25, t=t, shirt=(214, 218, 226), la=(70 + 20 * math.sin(u * 2), 60), ra=(110, 80), mouth="o" if u < 1.5 else (munch(t) if sip > 0.2 else "o"),
         expr="wow" if u < 1.5 else "happy", brow="up", look=(1, -0.6) if u < 1.6 else (0.6, -0.3), turn=0.4, lean=-10 + 6 * math.sin(u * 1.3), ll=20, rl=-10)
    r = 70 * (1 - 0.75 * sip)
    if r > 8: water_ball(f, bx - 60 * sip, by - 10 * sip, r, t, seed=2)
    for j in range(3):
        water_ball(f, bx + 120 + 30 * j, by - 90 + 50 * math.sin(u * 1.5 + j), 12 - 2 * j, t, seed=5 + j)
    px, py = 200 + 60 * u, 640 - 20 * u
    P = [(px + 70 * math.cos(u), py + 70 * math.sin(u)), (px - 70 * math.cos(u), py - 70 * math.sin(u))]
    cv2.line(f, (int(P[0][0]), int(P[0][1])), (int(P[1][0]), int(P[1][1])), C(INKC), 16, cv2.LINE_AA); cv2.line(f, (int(P[0][0]), int(P[0][1])), (int(P[1][0]), int(P[1][1])), C((60, 110, 200)), 9, cv2.LINE_AA)
    kw(f, "ASTRONAUTS", 540, 330, t, t0 + 0.05, "pop", 100, col=INKC)
    if t > tn: kw(f, "NO UP!", 540, 470, t, tn, "breathe", 130, col=ACC_S)
    return finish(f, n, look="cool")


# ---- S6: 'And the water never goes near your knees. Your gut soaks it into your blood first.' BOARD ----
GUT = [(470, 860), (620, 860), (620, 920), (460, 920), (460, 980), (620, 980), (620, 1040), (470, 1040)]
VESSEL = [(700, 1080), (720, 960), (730, 820), (720, 680), (660, 600)]


def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); tnv = T("b1", "never") - 0.1; tso = T("b1", "soaks") - 0.12; tbl = T("b1", "blood") - 0.12
    board_body(f, t, t0 - 2)
    draw_on(f, [(540, 530), (540, 760)], 1.0, ACC_S, 5, seed=580, tip=False)
    draw_on(f, GUT, ramp(t, t0, 0.5), BP_INK, 6, seed=581, tip=False)
    write_on(f, "gut", 250, 950, t, t0 + 0.3, 40, BP_INK)
    u = clamp((t - t0) / 0.8)
    if u < 1: cv2.circle(f, (540, int(560 + 260 * u)), 16, C(ACC), -1, cv2.LINE_AA)
    if t > tnv:
        k = ramp(t, tnv, 0.4)
        for j in range(6):
            a0 = j / 6; a1 = a0 + 0.08
            if k > a0: draw_on(f, [(540, 1060 + 180 * a0), (540, 1060 + 180 * min(a1, k))], 1.0, BP_GRID2, 6, seed=590 + j, tip=False)
        if t > tnv + 0.45:
            kx = ramp(t, tnv + 0.45, 0.18)
            draw_on(f, [(470, 1150), (610, 1290)], kx, (196, 40, 44), 14, seed=597, tip=False); draw_on(f, [(610, 1150), (470, 1290)], kx, (196, 40, 44), 14, seed=598, tip=False)
    if t > tso:
        draw_on(f, VESSEL, ramp(t, tso, 0.4), BLOOD, 12, seed=600, tip=False)
        for j in range(5):
            v = ((t - tso) * 1.2 + j * 0.2) % 1
            x = 620 + (705 - 620) * min(1, v * 2); y = 900 + 30 * j - (0 if v < 0.5 else (v - 0.5) * 2 * 240)
            cv2.circle(f, (int(x), int(y)), 10, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 10, C(ACC_S), 2, cv2.LINE_AA)
        write_on(f, "blood", 860, 760, t, tbl, 46, BLOOD)
    if t < tso: kw(f, "NEVER NEAR YOUR KNEES", 540, 300, t, tnv, "pop", 70, col=(176, 40, 44))
    else: kw(f, "INTO YOUR BLOOD", 540, 300, t, tso, "pop", 96, col=BLOOD)
    src(f, SRC_BLOOD52, t, t0 + 0.5)
    return finish(f, n, look="fresh")


# ---- S7: 'Their slippery joint fluid is made from that blood,' BOARD: the KNEE close-up ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tf = T("b2", "fluid") - 0.12; tm = T("b2", "made") - 0.1
    k = ramp(t, t0, 0.5)
    femur = [(400, 300), (400, 760), (360, 830), (380, 900), (540, 910), (700, 900), (720, 830), (680, 760), (680, 300)]
    tibia = [(370, 1500), (390, 1060), (360, 1010), (380, 980), (700, 980), (720, 1010), (690, 1060), (700, 1500)]
    draw_on(f, femur, k, BP_INK, 8, seed=610, tip=k < 1); draw_on(f, tibia, k, BP_INK, 8, seed=611, tip=k < 1)
    write_on(f, "thigh bone", 540, 560, t, t0 + 0.4, 40, BP_INK); write_on(f, "shin bone", 540, 1250, t, t0 + 0.6, 40, BP_INK)
    cap = [(330, 780), (300, 940), (330, 1100), (750, 1100), (780, 940), (750, 780)]
    draw_on(f, cap, ramp(t, t0 + 0.3, 0.5), BP_GRID2, 6, seed=612, tip=False, closed=True)
    if t > tf:
        hatch_on(f, [(360, 905), (720, 905), (720, 985), (360, 985)], ramp(t, tf, 0.35), ACC, gap=12, w=5)
        draw_arrow_on(f, (880, 820), (735, 930), ramp(t, tf + 0.2, 0.3), ACC_S, 7, 26)
        write_on(f, "joint fluid", 820, 740, t, tf + 0.25, 44, ACC_S)
        kw(f, "SLIPPERY JOINT FLUID", 540, 300, t, tf, "pop", 74, col=ACC_S)
    if t > tm:
        draw_on(f, [(120, 1500), (180, 1200), (230, 1000), (300, 950)], ramp(t, tm, 0.35), BLOOD, 12, seed=613, tip=False)
        for j in range(4):
            v = ((t - tm) * 1.3 + j * 0.25) % 1
            P, e = _cut_poly([(140, 1420), (200, 1150), (250, 1000), (330, 950), (450, 945)], v)
            cv2.circle(f, (int(e[0]), int(e[1])), 11, C(ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(e[0]), int(e[1])), 11, C(ACC_S), 2, cv2.LINE_AA)
        write_on(f, "from your blood", 330, 1400, t, tm + 0.2, 40, BLOOD)
    peek(f, t, 900, 1330, 0.4, expr="wow" if t > tm else "sus", look=(-0.7, -0.3))
    return finish(f, n, look="fresh")


def floor(f, y0=DIN_TOP):
    """the dining-room floor (terracotta tiles) for full-body shots without the table."""
    cv2.rectangle(f, (0, y0), (W, H), C((214, 160, 128)), -1)
    for x in range(-200, W + 200, 160): cv2.line(f, (x, y0), (int(540 + (x - 540) * 2.2), H), C((186, 130, 100)), 4, cv2.LINE_AA)
    for y in (y0 + 60, y0 + 150, y0 + 280, y0 + 460): cv2.line(f, (0, y), (W, y), C((186, 130, 100)), 4, cv2.LINE_AA)
    cv2.line(f, (0, y0), (W, y0), C(INKC), 6, cv2.LINE_AA)


def chair_back(f, x, y, s):
    """a wooden dining chair seen from the front: back posts + top rail (drawn BEFORE the sitter)."""
    sy = y - 112 * s
    for sg in (-1, 1):
        cv2.line(f, (int(x + sg * 120 * s), int(sy - 330 * s)), (int(x + sg * 120 * s), int(y)), C(INKC), int(26 * s), cv2.LINE_AA)
        cv2.line(f, (int(x + sg * 120 * s), int(sy - 330 * s)), (int(x + sg * 120 * s), int(y)), C((150, 100, 60)), int(16 * s), cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 130 * s), int(sy - 350 * s)), (int(x + 130 * s), int(sy - 290 * s)), C((150, 100, 60)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 130 * s), int(sy - 350 * s)), (int(x + 130 * s), int(sy - 290 * s)), C(INKC), max(2, int(5 * s)), cv2.LINE_AA)


def chair_seat(f, x, y, s):
    """the seat edge + front legs (drawn AFTER the sitter, under his thighs)."""
    sy = y - 112 * s
    cv2.rectangle(f, (int(x - 150 * s), int(sy)), (int(x + 150 * s), int(sy + 30 * s)), C((170, 116, 72)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - 150 * s), int(sy)), (int(x + 150 * s), int(sy + 30 * s)), C(INKC), max(2, int(5 * s)), cv2.LINE_AA)
    for sg in (-1, 1):
        cv2.line(f, (int(x + sg * 135 * s), int(sy + 30 * s)), (int(x + sg * 135 * s), int(y + 4)), C(INKC), int(22 * s), cv2.LINE_AA)
        cv2.line(f, (int(x + sg * 135 * s), int(sy + 30 * s)), (int(x + sg * 135 * s), int(y + 4)), C((150, 100, 60)), int(12 * s), cv2.LINE_AA)


# ---- S7b: '...so posture doesn't matter.' TWO Chubbies drinking: standing (left) and sitting (right, behind the table): ticks ----
def shot_S7b(t, n):
    f = set_dining(t); floor(f); t0 = st_("S7b"); tmat = T("b2", "matter.") - 0.12
    drinker(f, t, x=290, y=1480, s=1.15, sip=1.0, gulp_t=t0)
    chair_back(f, 790, 1480, 1.15)
    chub(f, 790, 1480, 1.15, t=t, sit=True, la=(26, 14), ra=(150, -128), hold=_rot_el(scale_el(steel_glass_el(0.6), 0.55), 32), hold_off=(-38, -18), hold_front=True,
         hand_r="grip", mouth=0, expr="happy", look=(-0.2, -0.4), turn=-0.3)
    chair_seat(f, 790, 1480, 1.15)
    kw(f, "STANDING", 290, 330, t, t0 + 0.05, "pop", 80, col=INKC); kw(f, "SITTING", 790, 330, t, t0 + 0.15, "pop", 80, col=INKC)
    kw(f, "=", 540, 900, t, t0 + 0.25, "pop", 160, col=ACC_S)
    if t > tmat:
        tick(f, 290, 450, ramp(t, tmat, 0.2)); tick(f, 790, 450, ramp(t, tmat + 0.1, 0.2))
        kw(f, "DOESN'T MATTER", 540, 600, t, tmat, "pop", 104, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S8: 'If your knees really hurt, ask a doctor. Just don't blame the glass.' ----
def shot_S8(t, n):
    f = set_dining(t); floor(f); t0 = st_("S8"); td = T("c1", "doctor.") - 0.12; tg = T("c1", "glass.") - 0.12
    hurt = t < td
    X8, Y8, S8 = 380, 1480, 1.3
    chub(f, X8, Y8, S8, t=t, la=(30, 60) if hurt else (24, 12), ra=(20, -40) if hurt else (72, 42), hand_r="open" if hurt else "point", mouth=talk(t),
         expr="ouch" if hurt else "n", brow="sad" if hurt else "up", look=(0.3, 0.9) if hurt else (1, 0), turn=0.3, lean=8 if hurt else 0, rl=14 if hurt else 6)
    if hurt:
        kx, ky = X8 + 60 * S8, Y8 - 66 * S8                                                    # the right knee
        glow(f, kx, ky, 70, (255, 90, 80), 0.35 + 0.15 * math.sin(t * 12))
        for j in range(5):
            a = -2.4 + 0.75 * j; ph = (t * 3 + j * 0.3) % 1
            r1, r2 = 55 + 20 * ph, 105 + 20 * ph
            cv2.line(f, (int(kx + r1 * math.cos(a)), int(ky + r1 * math.sin(a))), (int(kx + r2 * math.cos(a)), int(ky + r2 * math.sin(a))), C((200, 50, 50)), 8, cv2.LINE_AA)
        kw(f, "KNEES REALLY HURT?", 540, 340, t, t0 + 0.05, "pop", 90, col=(176, 40, 44))
    else:
        ui_word(f, "ask a", "[DOCTOR]", 360, t, td, col=INKC, acc=ACC_S, size=120, lead_col=INKC)
    cv2.rectangle(f, (650, 1180), (870, 1480), C((150, 100, 60)), -1, cv2.LINE_AA); cv2.rectangle(f, (650, 1180), (870, 1480), C(INKC), 6, cv2.LINE_AA)   # a side stool
    cv2.rectangle(f, (630, 1160), (890, 1200), C((176, 120, 76)), -1, cv2.LINE_AA); cv2.rectangle(f, (630, 1160), (890, 1200), C(INKC), 6, cv2.LINE_AA)
    el_at(f, steel_glass_el(0.7, mood="happy" if t > tg + 0.2 else ("ouch" if t > tg else "n"), look=(-0.6, -0.2)), 760, 1040, 1.1)
    if t > tg: el_at(f, vstamp_el("NOT GUILTY", (40, 130, 90), 70), 760, 800, 1.0, t, tg + 0.15, rot=-6)
    return finish(f, n, look="golden")


# ---- S9: 'Send this to whoever yells sit down every time you grab a glass.' ----
def shot_S9(t, n):
    f = set_dining(t); tsd = T("c2", "sit") - 0.1
    yell = t > tsd
    nani(f, 790, 1700, 1.5, t, la=(130, 150) if yell else (40, 30), hand_l="point", mouth=3 if yell else 0, expr="angry", brow="sus", look=(-1, 0), turn=-0.5, lean=4 * math.sin(t * 11) if yell else 0)
    drinker(f, t, x=320, y=1700, s=1.5, sip=0.0, expr="smirk" if yell else "happy", brow="up", look=(1, 0))
    dining_front(f)
    ui_word(f, "send this to whoever yells", "[SIT DOWN!]", 400, t, T("c2", "Send") - 0.05, col=INKC, acc=(176, 40, 44), size=120, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S10: the logo beat (0.6 s) ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_dining(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.25) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.12) / 0.2))
    return finish(f, n, look="warm")


# ---- S11: the LOOP TAIL ----
def shot_S11(t, n):
    f = set_dining(t)
    scene0(f, t)
    hook_band(f)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "swears") - 0.1, 0.3, 10), (T("i2", "myth.") - 0.1, 0.35, 14), (T("a1", "slams") - 0.1, 0.4, 16),
           (T("a2", "slide.") - 0.05, 0.3, 12), (T("a2", "muscle,") - 0.12, 0.3, 10), (T("a3", "no") - 0.1, 0.25, 8),
           (T("b1", "never") - 0.1 + 0.45, 0.3, 10), (T("b2", "matter.") - 0.12, 0.3, 10), (T("c1", "glass.") - 0.12 + 0.15, 0.3, 10), (T("c2", "sit") - 0.1, 0.3, 12)]


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
    if i == len(SHOTS) - 1:
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
