# ================= shots: FreshNestHub 57 — "Does cracking your knuckles cause arthritis?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: a STUDY DESK at night (navy wall, warm lamp, cool laptop, warm hallway light where nani stands) for the story; white board + blue ink for
# the explanation; ONE accent = JOINT-FLUID AMBER (the fluid in the joint bag, the pop marks, the suction cup, the question words). The MRI + X-ray are the
# 'proof' look. Red only on the safe-tip swelling.
# Story: frame 0 = Chubby mid-crack at his desk, nani already in the doorway yelling -> the question. Nani says yes, doctors say no (MYTH). The pop: every
# knuckle sits in a bag of fluid; pull the bones apart and a gas pocket SNAPS open (like a suction cup coming off glass); filmed in an MRI (2015); that's why
# the same knuckle needs ~20 minutes. Proof: one doctor cracked ONE hand for fifty years, never the other: arthritis in neither. Safe tip: pain or swelling
# -> a doctor. Send line = the desk friend; the tail rebuilds frame 0 (loop).
# CRAFT (ep 57) = HAND ACTING: every close-up hand is anim_props6.big_hand with asymmetric fingers, grouped spacing, an angled pinky, a thumb on its own
# line, curl in the first two joints, tension only in the pulled knuckle, the wrist LEADING and the fingers following 3 frames later (drag).
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail = 50.0 s
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "knuckles") - 0.1, "punch"),
    ("S1", T("i2", "Your") - 0.12, "whip"), ("S1b", T("i2", "Doctors") - 0.1, "cut"),
    ("S2", T("a1", "So") - 0.12, "erase"), ("S2b", T("a1", "Every") - 0.1, "cut"),
    ("S3", T("a2", "Pull") - 0.12, "punch"),
    ("S3b", T("a2", "like") - 0.1, "whip"),
    ("S4", T("a3", "Scientists") - 0.12, "erase"),
    ("S5", T("b1", "That's") - 0.12, "whip"),
    ("S6", T("b2", "One") - 0.12, "whip"), ("S6b", T("b2", "He") - 0.1, "cut"),
    ("S7", T("b3", "And") - 0.12, "punch"),
    ("S8", T("c1", "But") - 0.12, "whip"),
    ("S9", T("c2", "Send") - 0.1, "whip"),
    ("S10", LINES["c2"]["end"] + 0.05, "punch"), ("S11", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
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


def hook_band(f, y0=228, y1=700, a=0.72):
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "CRACKING KNUCKLES", 540, 425, t, t0, "pop", 84, col=BP_INK, op=op)
    kw(f, "= ARTHRITIS?", 540, 590, t, t0, "shake", 132, col=ACC_S, amp=0.35, op=op)


def pops(f, x, y, t, times, r=46, col=None):
    """the visible POP: an ink star + 3 short crack ticks at each time."""
    for tp in times:
        if tp <= t < tp + 0.32:
            pop_star(f, x, y, t, tp, r=r, col=col or ACC_S)
            u = (t - tp) / 0.32
            for j in range(3):
                a = math.radians(-150 + 60 * j); r0 = r * (0.9 + 0.8 * u); r1 = r0 + r * 0.5
                cv2.line(f, (int(x + r0 * math.cos(a)), int(y + r0 * math.sin(a))), (int(x + r1 * math.cos(a)), int(y + r1 * math.sin(a))), C(INKC), 5, cv2.LINE_AA)


def drag3(t, fn, frames=3):
    """HAND ACTING: the fingers follow the wrist 3 frames later (drag)."""
    return fn(t - frames / FPS)


CX, CY, CS = 440, 2080, 2.0            # Chubby at the desk (desk top 1560): big enough to act, hands above the desk
NX, NY, NS_ = 850, 1900, 1.5          # nani in the doorway
CRACK0 = [-0.05, 0.62, 1.2]           # the cracks of the opening (t < 0 = it started before frame 0)
CRARM = (-80, -158)                    # forearms up + in = hands pressed together at the chest


# ---- S0: HOOK at frame 0 = MID-CRACK: Chubby's hands pressed together at his chest, a POP already flying, nani in the doorway mid-yell ----
def scene0(f, t, words=True):
    push = 0.5 + 0.5 * math.sin(t * 9)
    jolt = max((math.exp(-(t - tp) * 14) for tp in CRACK0 if t >= tp), default=0.0)
    nani(f, NX, NY, NS_, t, la=(30, 20), ra=(120 + 10 * math.sin(t * 12), 150), hand_r="point", mouth="jaw" if t % 1.2 < 0.8 else 2,
         expr="angry", brow="sus", look=(-1, 0.1), turn=-0.5, lean=-4)
    hd = chub(f, CX, CY - 8 * jolt, CS, t=t, la=(CRARM[0], CRARM[1] + 6 * push), ra=(CRARM[0], CRARM[1] + 6 * push), hand_l="grip", hand_r="grip",
         mouth="o" if jolt > 0.3 else 1, expr="happy" if jolt < 0.3 else "wow", brow="up", look=(0.2, 0.4), turn=0.1, squash=0.06 * jolt)
    desk_front(f, DESK_TOP, t)
    hx_ = (hd[-1][0] + hd[1][0]) / 2; hy_ = min(hd[-1][1], hd[1][1])
    pops(f, hx_, hy_ - 40, t, CRACK0, r=56)


def shot_S0(t, n):
    f = set_desk(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...knuckles can actually give you arthritis?' THE HANDS close-up: the right fist pulls the left middle finger; the wrist leads, POP ----
def hands_cu(f, t, t_pull, t_pop, pop=True, x=560, y=1880, s=2.6):
    """left hand (fingers up) + the right hand's fist pulling the middle finger. HAND ACTING: the wrist leads the pull, the fingers drag 3 frames behind;
    tension only in the pulled finger (stretch + its knuckle), the others curl a little more (they 'brace'), the pinky angles out."""
    def pullk(tt): return ramp(tt, t_pull, max(0.2, t_pop - t_pull)) if tt < t_pop else max(0.0, 1 - (tt - t_pop) / 0.12) * 0.25
    pk = pullk(t); pf = drag3(t, pullk)
    brace = 0.25 * pf
    h = big_hand(f, x, y + 30 * pk, s, rot=-4 + 3 * pk, side=-1, ang=(-4 - 6 * pf, 0, 5 + 4 * pf, 12 + 6 * pf),
                 curl=(0.3 + brace, 0.0, 0.35 + brace, 0.45 + brace), stretch=(0, 0.12 * pk, 0, 0), thumb=30 + 10 * pf)
    tip = h["tips"][1]
    fist_at(f, tip[0] + 6, tip[1] - 10 - 40 * pk, s * 0.62, rot=-8)
    if pop and t >= t_pop:
        kn = h["knuck"][1]
        pops(f, kn[0], kn[1] - 30, t, [t_pop], r=70)
        kw(f, "POP!", 540, 820, t, t_pop, "pop", 150, col=ACC_S)
    return h


def shot_S0b(t, n):
    f = set_desk(t, 9); f = dof(f, 3); t0 = st_("S0b")
    hands_cu(f, t, t0 + 0.15, T("i1", "give") - 0.05)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Your naanee says yes.' NANI close in the doorway: finger wag, YES! ----
def shot_S1(t, n):
    f = set_desk(t, 9); f = dof(f, 2); ty = T("i2", "yes.") - 0.1
    wag = 12 * math.sin(t * 13)
    nani(f, 620, 2080, 2.2, t, la=(30, 20), ra=(120 + wag, 150), hand_r="point", mouth=talk(t) if t < ty else "jaw", expr="angry", brow="sus",
         look=(-0.5, 0), turn=-0.2, lean=wag * 0.1)
    hook_band(f, 250, 640)
    kw(f, "NANI SAYS:", 540, 330, t, T("i2", "naanee") - 0.2, "pop", 96, col=INKC)
    if t > ty: kw(f, "YES!", 540, 520, t, ty, "shake", 170, col=RED, amp=0.4)
    return finish(f, n, look="night")


# ---- S1b: 'Doctors at Harvard say... no.' a doctor on the clinic board, a calm head shake, NO. + MYTH stamp ----
def doctor57(f, x, y, s, t, shake=0.0):
    chub(f, x, y, s, t=t, shirt=COAT, la=(26, 14), ra=(60, 40), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0.3 * shake, 0), turn=0.3 * shake)
    hx2, hy2 = x + 0.3 * shake * 14 * s, y - 420 * s                                         # head mirror = 'doctor' at a glance
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)
    el_at(f, steth_el(), x - 10 * s, y - 280 * s, 0.6 * s / 1.5)


def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); tno = T("i2", "no.") - 0.12
    sh = math.sin((t - tno) * 14) * math.exp(-(t - tno) * 3) if t > tno else 0.0
    doctor57(f, 540, 1660, 1.5, t, shake=sh)
    kw(f, "DOCTORS:", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    write_on(f, "Harvard Health, Cleveland Clinic", 540, 430, t, T("i2", "Harvard") - 0.1, 30, BP_INK, cps=40)
    if t > tno:
        kw(f, "NO.", 540, 600, t, tno, "pop", 190, col=ACC_S)
        el_at(f, vstamp_el("MYTH", RED, 90), 860, 820, 1.0, t, tno + 0.25, rot=8)
    src(f, SRC_DOC57, t, t0 + 0.4, y=1560)
    return finish(f, n, look="fresh")


# ---- S2: 'So what's that pop?' board: a finger draws itself, the knuckle gets a ring ----
FINGER = [(420, 1500), (420, 980), (430, 820), (440, 640), (470, 520), (540, 490), (610, 520), (640, 640), (650, 820), (660, 980), (660, 1500)]


def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tp = T("a1", "pop?") - 0.1
    k = ramp(t, t0, 0.7)
    draw_on(f, FINGER, k, BP_INK, 9, seed=571, tip=k < 1)
    for y_ in (700, 900):
        draw_on(f, [(450, y_), (500, y_ + 14), (580, y_ + 14), (630, y_)], ramp(t, t0 + 0.4, 0.3), BP_INK, 6, seed=y_, tip=False)
    draw_on(f, [(470, 560), (480, 520), (540, 506), (600, 520), (610, 560), (540, 580)], ramp(t, t0 + 0.6, 0.3), BP_INK, 5, seed=575, tip=False, closed=True)
    kw(f, "WHAT'S THAT", 540, 330, t, t0 + 0.1, "pop", 92, col=BP_INK)
    if t > tp:
        draw_ell_on(f, 540, 900, 150, 110, ramp(t, tp, 0.3), ACC_S, 9, seed=576)
        kw(f, "POP?", 540, 1300, t, tp, "shake", 170, col=ACC_S, amp=0.4)
    peek(f, t, 880, 1150, 0.45, expr="sus", look=(-0.8, -0.3))
    return finish(f, n, look="fresh")


# ---- S2b: 'Every knuckle sits in a tiny bag of slippery fluid.' the JOINT draws itself: bones -> bag -> amber fluid fills ----
JX, JY = 540, 930


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tb = T("a1", "bag") - 0.1; tfl = T("a1", "slippery") - 0.1
    k = ramp(t, t0, 0.8)
    fluid = ramp(t, tfl, 0.6)
    joint_board(f, JX, JY, t, k=k, fluid=fluid, sc=1.3)
    if t > t0 + 0.4: write_on(f, "bone", 800, 600, t, t0 + 0.4, 40, BP_INK)
    if t > tb: draw_arrow_on(f, (900, 1200), (790, 1090), ramp(t, tb, 0.25), BP_INK, 7, 24); write_on(f, "bag", 900, 1250, t, tb, 40, BP_INK)
    if t > tfl:
        kw(f, "JOINT FLUID", 540, 1440, t, tfl, "breathe", 100, col=ACC_S)
    kw(f, "INSIDE YOUR KNUCKLE", 540, 300, t, t0 + 0.1, "pop", 76, col=BP_INK)
    return finish(f, n, look="fresh")


# ---- S3: 'Pull the bones apart, and a tiny gas pocket snaps open,' the bones slide apart (arrows), the GAS POCKET SNAPS (2 frames) ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); ts = T("a2", "snaps") - 0.06
    gap = 70 * ramp(t, t0 + 0.1, max(0.3, ts - t0 - 0.1))
    if t > ts: gap = 70 + 14 * math.exp(-(t - ts) * 10) * math.cos((t - ts) * 40)      # the snap jolt + settle
    cav = 0.0 if t < ts else min(1.0, (t - ts) / (2 / FPS))                              # involuntary: no anticipation, 2 frames
    joint_board(f, JX, JY, t, k=1.0, gap=gap, cav=cav, sc=1.3)
    ka = ramp(t, t0 + 0.05, 0.3)
    draw_arrow_on(f, (JX + 330, JY - 260), (JX + 330, JY - 420), ka, RED, 10, 32); draw_arrow_on(f, (JX + 330, JY + 300), (JX + 330, JY + 460), ka, RED, 10, 32)
    kw(f, "PULL", 540, 300, t, t0, "pop", 110, col=RED)
    if t > ts:
        pops(f, JX, JY + 60, t, [ts], r=110)
        kw(f, "GAS POCKET", 540, 1440, t, ts, "pop", 104, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S3b: '...like a suction cup coming off glass.' the analogy you can feel: a fist pulls a cup, the dome stretches, the rim holds... POP ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); tpop = T("a2", "coming") + 0.05
    glass_pane(f, 60, 600, 330, 1380)
    pull = ramp(t, t0 + 0.1, max(0.2, tpop - t0 - 0.1)) if t < tpop else 1.0
    off = 0.0 if t < tpop else 260 * (1 - math.exp(-(t - tpop) * 7))
    rot = 0.0 if t < tpop else 25 * (1 - math.exp(-(t - tpop) * 5))
    knob = suction_cup(f, 330, 980, 1.6, pull=pull, off=off, rot=rot)
    fx = knob[0] + 30; fy = knob[1]
    cv2.line(f, (int(fx + 60), int(fy + 20)), (W + 40, int(fy + 120)), C(INKC), 74, cv2.LINE_AA); cv2.line(f, (int(fx + 60), int(fy + 20)), (W + 40, int(fy + 120)), C(INK_MINT), 60, cv2.LINE_AA)
    grip_hand(f, fx, fy, 2.3, kind="grip", rot=-90)
    if t > tpop:
        pops(f, 360, 980, t, [tpop], r=80)
        kw(f, "POP!", 540, 1300, t, tpop, "pop", 150, col=ACC_S)
    kw(f, "LIKE A SUCTION CUP", 540, 330, t, T("a2", "suction") - 0.15, "pop", 84, col=BP_INK)
    if 0.2 < pull and t < tpop: write_on(f, "low pressure", 560, 1180, t, t0 + 0.3, 32, BP_INK)
    return finish(f, n, look="fresh")


# ---- S4: 'Scientists actually filmed it happening inside an MRI scanner.' the scanner + the real-time image: the dark pocket appears ----
def shot_S4(t, n):
    f = ink_set("paper"); t0 = st_("S4"); tf = T("a3", "filmed") - 0.1; th = T("a3", "happening") - 0.05
    mri_ring(f, 290, 1080, 230, t, scan=1.0)
    cv2.line(f, (290, 1080), (60, 1080), C(INKC), 14, cv2.LINE_AA); cv2.line(f, (290, 1080), (60, 1080), C(ACC), 6, cv2.LINE_AA)
    gap = 40 * ramp(t, tf - 0.4, 0.8); cav = 0.0 if t < th else min(1.0, (t - th) / (2 / FPS))
    mri_screen(f, 560, 760, 380, 520, gap=gap, cav=cav, t=t)
    if t > th: draw_ell_on(f, 750, 1022, 110, 70, ramp(t, th, 0.25), ACC, 8, seed=577); write_on(f, "the gas pocket", 750, 1360, t, th + 0.1, 34, ACC_S)
    kw(f, "FILMED IN AN MRI", 540, 340, t, tf, "pop", 92, col=INKC)
    write_on(f, "2015", 540, 470, t, tf + 0.3, 46, ACC_S)
    src(f, SRC_MRI57, t, t0 + 0.6)
    return finish(f, n, look="cool")


# ---- S5: 'That's also why the same knuckle won't pop again for about twenty minutes.' Chubby tries again: pull... nothing. The 20-min timer ----
def shot_S5(t, n):
    f = set_desk(t, 9); f = dof(f, 3); t0 = st_("S5"); tw = T("b1", "won't") - 0.1; tt = T("b1", "twenty") - 0.1
    hands_cu(f, t, t0 + 0.2, tw + 0.6, pop=False, x=560, y=2000, s=2.3)
    if t > tw + 0.5:
        hook_band(f, 890, 1040, 0.7)
        kw(f, "...NOPE", 540, 960, t, tw + 0.5, "drop", 110, col=INKC, t1=tw + 1.6)
    peek(f, t, 170, 1250, 0.5, expr="sad" if t > tw + 0.5 else "sus", look=(0.7, 0.4))
    tk = ramp(t, tt, 1.0)
    el_at(f, timer_el(tk, "20 MIN"), 540, 560, 1.25, t, tt - 0.2)
    if t > tt:
        hook_band(f, 250, 360, 0.7)
        kw(f, "WAIT ~20 MIN", 540, 300, t, tt, "pop", 80, col=ACC_S)
    src(f, SRC_20MIN57, t, tt + 0.3, y=1560)
    return finish(f, n, look="night")


# ---- S6: 'One doctor even tested it on himself.' the old doctor at his desk, LEFT hand cracking, right hand still ----
def shot_S6(t, n):
    f = set_desk(t, 6, door=0.0); t0 = st_("S6"); th = T("b2", "tested") - 0.1
    times = [t0 + 0.4 + 0.7 * j for j in range(5)]
    jol = max((math.exp(-(t - tp) * 14) for tp in times if t >= tp), default=0.0)
    hd = old_doc(f, 540, 2080, 2.0, t, la=(CRARM[0], CRARM[1] + 8 * jol), ra=(30, 60), hand_l="grip", hand_r="open", mouth=0, expr="smirk", brow="up", look=(-0.6, 0.4), turn=-0.2)
    desk_front(f, DESK_TOP, t, laptop=False)
    for tp in times: pops(f, hd[-1][0], hd[-1][1] - 40, t, [tp], r=46)
    if t > th: hook_band(f, 250, 420, 0.7)
    kw(f, "TESTED ON HIMSELF", 540, 330, t, th, "pop", 84, col=INKC)
    return finish(f, n, look="warm")


# ---- S6b: 'He cracked just one hand for fifty years, never the other.' SPLIT: LEFT hand cracking | the calendar flips to 50 | RIGHT hand still ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); tf = T("b2", "fifty") - 0.1; tn = T("b2", "never") - 0.1
    times = [t0 + 0.2 + 0.45 * j for j in range(9)]
    jol = max((math.exp(-(t - tp) * 14) for tp in times if t >= tp), default=0.0)
    big_hand(f, 270, 1360 - 20 * jol, 1.4, rot=-6, side=-1, ang=(-5, 0, 6, 14), curl=(0.2 + 0.2 * jol, 0.1 + 0.3 * jol, 0.3, 0.4), sleeve=COAT)
    big_hand(f, 810, 1360, 1.4, rot=6, side=1, ang=(-3, 1, 5, 10), curl=(0.1, 0.05, 0.15, 0.25), sleeve=COAT)
    for tp in times: pops(f, 270, 990, t, [tp], r=36)
    write_on(f, "CRACKED", 270, 1440, t, t0 + 0.2, 36, ACC_S)
    if t > tn - 0.3: write_on(f, "NEVER", 810, 1440, t, tn - 0.3, 36, BP_INK)
    year_flip(f, 540, 640, t, t0 + 0.2, tf + 0.4, 1, 50, 1.1)
    if t > tf: kw(f, "50 YEARS", 540, 330, t, tf, "pop", 110, col=INKC)
    return finish(f, n, look="fresh")


# ---- S7: 'And his result? Not a trace of arthritis in either hand.' the X-ray lightbox: both films clean, two green ticks ----
def shot_S7(t, n):
    f = ink_set("paper"); t0 = st_("S7"); tn = T("b3", "Not") - 0.1; te = T("b3", "either") - 0.1
    lit = ramp(t, t0 + 0.05, 0.25)
    cv2.rectangle(f, (90, 600), (990, 1330), C(_mix((60, 66, 80), (236, 244, 252), lit)), -1); cv2.rectangle(f, (90, 600), (990, 1330), C(INKC), 9, cv2.LINE_AA)
    xray_hands(f, 540, 965, t, 0.95)
    write_on(f, "cracked", 330, 1400, t, t0 + 0.3, 36, ACC_S)
    write_on(f, "never", 760, 1400, t, t0 + 0.3, 36, BP_INK)
    kw(f, "HIS RESULT?", 540, 320, t, t0 + 0.05, "pop", 96, col=INKC)
    if t > tn:
        for j, x_ in enumerate((330, 760)):
            k = ramp(t, tn + 0.15 + 0.25 * j, 0.2)
            draw_on(f, [(x_ - 70, 1120), (x_ - 20, 1170), (x_ + 80, 1040)], k, OKG, 18, seed=580 + j, tip=False)
        kw(f, "NO ARTHRITIS", 540, 470, t, tn, "pop", 100, col=OKG)
    if t > te: kw(f, "IN EITHER HAND", 540, 1500, t, te, "shake", 90, col=ACC_S, amp=0.3)
    src(f, SRC_UNGER57, t, t0 + 0.6, y=1590)
    return finish(f, n, look="fresh")


# ---- S8: 'But if a knuckle ever hurts or swells up, show it to a doctor.' Chubby looks at a red swollen knuckle; then the doctor card ----
def shot_S8(t, n):
    f = set_desk(t, 9); f = dof(f, 3); t0 = st_("S8"); th = T("c1", "hurts") - 0.1; tsw = T("c1", "swells") - 0.1; td = T("c1", "show") - 0.1
    sw = ramp(t, tsw, 0.6); rd = ramp(t, th, 0.4)
    peek(f, t, 250, 1050, 0.62, expr="sad" if t > th else "sus", look=(0.8, 0.5), mouth=talk(t) if t < th else "o")
    big_hand(f, 700, 1900, 2.1, rot=-8, side=-1, ang=(-4, 0, 6, 14), curl=(0.3, 0.2, 0.35, 0.45), swell=sw, swell_f=1, red=rd)
    if t > th:
        hook_band(f, 250, 640 if t > td else 420, 0.8)
        kw(f, "HURTS? SWELLS?", 540, 330, t, th, "shake", 92, col=RED, amp=0.3)
    if t > td:
        kw(f, "SEE A DOCTOR", 540, 530, t, td, "pop", 110, col=BP_INK)
    src(f, SRC_SAFE57, t, td + 0.2, y=1560)
    return finish(f, n, look="night")


# ---- S9: 'Send this to the friend who cracks his knuckles all day.' the desk wide: Chubby points at us, cracks once more; nani arms crossed in the door ----
def shot_S9(t, n):
    f = set_desk(t); tk = T("c2", "knuckles") - 0.1
    nani(f, NX, NY, NS_, t, la=(-80, -150), ra=(-80, -150), mouth=0, expr="smirk", brow="sus", look=(-1, 0), turn=-0.5)
    pt = t < tk
    hd = chub(f, CX, CY, CS, t=t, la=(26, 14) if pt else CRARM, ra=(110, 110) if pt else CRARM, hand_r="point" if pt else "grip", hand_l="open" if pt else "grip",
         mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2), turn=0.0)
    desk_front(f, DESK_TOP, t)
    if not pt: pops(f, (hd[-1][0] + hd[1][0]) / 2, min(hd[-1][1], hd[1][1]) - 40, t, [tk + 0.1], r=56)
    hook_band(f, 250, 560)
    ui_word(f, "send this to the friend who cracks his", "[KNUCKLES]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=120, lead_col=INKC)
    return finish(f, n, look="night")


# ---- S10: the logo beat (0.4 s) ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_desk(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S11: the LOOP TAIL: replays the run-up to frame 0 so the seam lands on the same pose ----
def shot_S11(t, n):
    f = set_desk(t - END)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="night")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "give") - 0.05, 0.3, 12), (T("i2", "yes.") - 0.1, 0.3, 10), (T("i2", "no.") - 0.12, 0.35, 12),
           (T("a1", "pop?") - 0.1, 0.3, 10), (T("a2", "snaps") - 0.06, 0.35, 16), (T("a2", "coming") + 0.05, 0.3, 12),
           (T("a3", "happening") - 0.05, 0.3, 10), (T("b2", "fifty") - 0.1, 0.3, 10), (T("b3", "Not") - 0.1, 0.35, 14),
           (T("c1", "swells") - 0.1, 0.3, 10)]


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
