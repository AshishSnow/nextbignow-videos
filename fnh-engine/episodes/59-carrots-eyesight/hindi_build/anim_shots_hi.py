# ================= shots: FreshNestHub 59 — "Do carrots improve your eyesight?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the NIGHT KITCHEN (moonlit, cool) where Chubby crunches a carrot with comic HEADLIGHT EYES while mom cheers him on (the myth);
# then sepia 1940 NEWSPRINT + the NAVY BLITZ NIGHT with cream searchlights (the history = the payoff); the green RADAR glow is the only other
# colour; then the white BOARD (blue ink + carrot orange) for vitamin A; daylight-bright for the safe tip; back to the night kitchen to loop.
# ONE accent = CARROT ORANGE (carrot, vitamin A, the question words). Red only on the stamps / FULL line.
# Story: frame 0 = Chubby mid-crunch, beams from his eyes, mom pointing with a carrot -> the question. Mom says yes, even in the dark. The story
# began as a wartime cover-up (SPINNING NEWSPAPER). 1940: night pilots shooting planes down (blitz sky, searchlights); the papers said 'they eat
# loads of carrots' (SPINNING NEWSPAPER #2 = the craft moment). The real secret: RADAR (reveal in the nose + scope). The carrot in a spy
# disguise = cover story. Carrots -> vitamin A -> the eye in dim light (board). Extra won't give night vision (he eats a pile: beams off); tanks
# with a FULL line: helps only if you're short. Blurry? carrots won't fix it -> eye check. Send line = mom; the tail rebuilds frame 0 (loop).
# CRAFT (ep 59) = THE SPINNING NEWSPAPER (lib59 spin_paper + mix paper_spin).
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "see") - 0.12, "punch"),
    ("S1", T("i2", "Your") - 0.12, "whip"), ("S1b", T("i2", "But") - 0.1, "cut"),
    ("S2", T("a1", "In") - 0.12, "flash"), ("S2b", T("a1q", "And") - 0.1, "cut"),
    ("S3", T("a2", "The") - 0.12, "whip"), ("S3b", T("a2", "The", 1) - 0.1, "punch"),
    ("S4", T("b1", "Carrots") - 0.12, "erase"), ("S4b", T("b1", "and") - 0.1, "cut"),
    ("S5", T("b2", "But") - 0.12, "whip"), ("S5b", T("b2", "They") - 0.1, "erase"),
    ("S6", T("c1", "And") - 0.12, "whip"), ("S6b", T("c1", "time") - 0.1, "cut"),
    ("S7", T("c2", "Send") - 0.1, "whip"),
    ("S8", LINES["c2"]["end"] + 0.05, "punch"), ("S9", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
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


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None, blink=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look,
                   turn=clamp(look[0]) * 0.5, blink=blink)


def hook_band(f, y0=228, y1=700, a=0.72, col=None):
    if a <= 0: return
    m = np.zeros((H, 1), np.float32); m[y0:y1] = a
    m = cv2.GaussianBlur(np.repeat(m, 4, 1), (1, 61), 0)[:, :1, None]
    f[:] = f * (1 - m) + np.array(C(col or PAPER), np.float32) * m


def hook_words(f, t, t0=-1.0, op=1.0):
    kw(f, "DO YOU KNOW IF", 540, 300, t, t0, "pop", 70, col=INKC, op=op)
    kw(f, "CARROTS", 540, 425, t, t0, "pop", 110, col=ACC_S, op=op)
    kw(f, "= BETTER EYESIGHT?", 540, 590, t, t0, "shake", 82, col=BP_INK, amp=0.35, op=op)


def doctor59(f, x, y, s, t, shake=0.0):
    chub(f, x, y, s, t=t, shirt=COAT, la=(26, 14), ra=(60, 40), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0.3 * shake, 0), turn=0.3 * shake)
    hx2, hy2 = x + 0.3 * shake * 14 * s, y - 420 * s
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)
    el_at(f, steth_el(), x - 10 * s, y - 280 * s, 0.6 * s / 1.5)


# ---- the NIGHT KITCHEN (frame 0, send line, tail) ----
CX, CY, CS = 680, 1900, 1.72         # Chubby right of centre (head centre ~ y 1309); beams go up-right into the dark
NX, NY, NS_ = 290, 1900, 1.42        # mom on the left
CAR_ROT, CAR_OFF = 70, (-34, 46)


def crumbs(f, x, y, t, t0, n=9, seed=0):
    """carrot crumbs that fly off each crunch (gravity), orange flecks."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        vx, vy = rng.uniform(-260, 260), rng.uniform(-420, -160); r = int(rng.uniform(5, 10))
        dt = (t - t0 + i * 0.08) % 0.72
        px, py = x + vx * dt, y + vy * dt + 900 * dt * dt
        cv2.circle(f, (int(px), int(py)), r, C(ACC), -1, cv2.LINE_AA)
        cv2.circle(f, (int(px), int(py)), r, C(ACC_S), 2, cv2.LINE_AA)


def cruncher(f, t, x=CX, y=CY, s=CS, beams=1.0, mouth=None, expr="happy", look=(0.6, -0.3), ang=-0.38):
    """Chubby crunching a carrot held to his mouth (screen-right hand), comic headlight beams from his eyes into the dark."""
    hx, hy = x, y - 420 * s
    car = _rot_el(scale_el(carrot_ink_el(bite=1), 0.34 * s), CAR_ROT)
    chub(f, x, y, s, t=t, la=(22, 12), ra=(148, -130), hand_r="grip", hold=car, hold_off=CAR_OFF, hold_front=True,
         mouth=munch(t) if mouth is None else mouth, expr=expr, brow="up", look=look, lean=-3)
    crumbs(f, hx + 40 * s, hy + 70 * s, t, 0.0, seed=1)
    eye_beams(f, hx + 10 * s, hy - 8 * s, 70 * s, ang=ang, L=1100, amt=beams * (0.9 + 0.1 * math.sin(t * 7)))


def mom_cheer(f, t, x=NX, y=NY, s=NS_, mouth=None, expr="happy"):
    """mom holds a carrot up (screen-left hand) and points at it with the other."""
    car = scale_el(carrot_ink_el(mood="happy"), 0.32 * s)
    hd = mom58(f, x, y, s, t, la=(30, 20), ra=(150, 165), hand_l="open", hand_r="grip", mouth=talk(t) if mouth is None else mouth, expr=expr, brow="up",
               look=(0.6, -0.2), turn=0.3, lean=2)
    lx, ly = hd[1]
    wag = 8 * math.sin(t * 9)
    rot_comp(f, car, lx, ly - 70 * s, wag, 1.0, 1.0, 0.0)
    grip_hand(f, lx, ly, s, kind="grip")


def night_kitchen(t):
    f = set_stove_night(t, lamp=0.5)
    return f * 0.85


def scene0(f, t):
    mom_cheer(f, t, mouth=2 if t % 1.1 < 0.7 else 0)
    cruncher(f, t)


def shot_S0(t, n):
    f = night_kitchen(t)
    scene0(f, t)
    hook_band(f, a=0.66); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...see better?' face close-up: chomp, the beams snap brighter ----
def shot_S0b(t, n):
    f = night_kitchen(t); f = dof(f, 4); t0 = st_("S0b")
    hx, hy = 520, 1180
    peek(f, t, hx, hy, 1.25, expr="happy", look=(0.6, -0.3), mouth=munch(t))
    rot_comp(f, scale_el(carrot_ink_el(bite=2), 1.1), hx + 200, hy + 150, -72, 1.0, 1.0, 0.0)
    crumbs(f, hx + 200, hy + 160, t, 0.0, 12, seed=2)
    eye_beams(f, hx + 20, hy - 30, 150, ang=-0.3, L=1000, amt=0.6 + 0.4 * ramp(t, t0, 0.2))
    hook_band(f, a=0.66); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Your mom says yes, even in the dark.' MOM close, carrot raised; YES! + EVEN IN THE DARK ----
def shot_S1(t, n):
    f = night_kitchen(t); f = dof(f, 3); ty = T("i2", "yes,") - 0.1; td = T("i2", "dark.") - 0.15
    mom_cheer(f, t, 600, 2120, 2.2, mouth=talk(t))
    hook_band(f, 250, 680, 0.72)
    kw(f, "MOM SAYS:", 540, 330, t, T("i2", "mom") - 0.2, "pop", 96, col=INKC)
    if t > ty: kw(f, "YES!", 540, 480, t, ty, "shake", 150, col=OKG, amp=0.4)
    if t > td: kw(f, "EVEN IN THE DARK", 540, 620, t, td, "pop", 70, col=INKC)
    return finish(f, n, look="night")


# ---- S1b: '...that story started as a wartime cover-up.' SPINNING NEWSPAPER #1 + COVER-UP? stamp ----
def sepia_bg(t):
    f = np.ones((H, W, 3), np.float32) * np.array(C((96, 78, 56)), np.float32)
    g = cv2.GaussianBlur(np.random.default_rng(5950).uniform(0, 1, (H // 8, W // 8)).astype(np.float32), (0, 0), 3)
    f *= (0.88 + 0.12 * cv2.resize(g, (W, H)))[..., None]
    glow(f, 540, 980, 700, (255, 220, 160), 0.25 + 0.05 * math.sin(t * 2))
    return f


def shot_S1b(t, n):
    f = sepia_bg(t); t0 = st_("S1b"); tc = T("i2", "cover-up.") - 0.1
    spin_paper(f, newspaper_el("CARROTS GIVE", "PILOTS CAT'S EYES!", pic="carrot"), t, t0 + 0.02, 540, 1010, 0.85, 4, 0.1, 1.0)
    kw(f, "WARTIME", 540, 300, t, T("i2", "wartime") - 0.12, "pop", 96, col=(250, 240, 220))
    if t > tc: el_at(f, vstamp_el("COVER-UP?", RED, 84), 720, 1230, 1.0, t, tc, rot=-12)
    return finish(f, n, look="warm")


# ---- S2: 'In nineteen-forty, British pilots kept shooting down planes at night.' THE BLITZ NIGHT ----
def shot_S2(t, n):
    f = set_blitz(t); t0 = st_("S2"); u = t - t0
    hit = T("a1", "shooting") - 0.05
    ex_, ey_ = 900 - 60 * u, 760 + 12 * math.sin(u * 3)                          # the enemy bomber, high on the right, caught in a beam
    if t > hit:
        v = t - hit; ex_, ey_ = 900 - 60 * u + 90 * v, 760 + 260 * v * v + 60 * v
        for j in range(7):
            cv2.circle(f, (int(ex_ + 40 - j * 30), int(ey_ - 30 - j * 30 + 6 * math.sin(t * 5 + j))), 16 + 5 * j, C((120, 118, 126)), -1, cv2.LINE_AA)
        flash_k = math.exp(-v * 6)
        if flash_k > 0.05: glow(f, ex_, ey_, 160, (255, 200, 120), 0.8 * flash_k)
        rot_comp(f, scale_el(plane_ink_el(dark=True), 0.75), ex_, ey_, 180 - 70 * v, 1.0, 1.0, 0.0)
    else:
        lamp_pool(f, ex_, ey_, 170, 0.25)
        rot_comp(f, scale_el(plane_ink_el(dark=True), 0.75), ex_, ey_, 180, 1.0, 1.0, 0.0)
    px = 150 + 200 * u; py = 1180 + 24 * math.sin(u * 2.2)                         # our plane with Chubby in the cockpit
    PS = 1.25
    comp(f, scale_el(plane_ink_el(), PS), px, py)
    pilot_head(f, px + (400 - 330) * PS, py - 95 * PS, 0.5, t, mouth=3 if t > hit else 0, expr="happy" if t > hit else "sus", turn=0.5, look=(0.6, -0.6))
    prop_spin(f, px + (614 - 330) * PS, py, 80, t)
    kw(f, "1940", 540, 330, t, t0 + 0.05, "pop", 150, col=BEAM)
    kw(f, "NIGHT PILOTS", 540, 480, t, T("a1", "pilots") - 0.1, "pop", 90, col=ACC)
    src(f, SRC_WAR, t, t0 + 0.4, y=1560)
    return finish(f, n, look="night")


# ---- S2b: 'And the papers said, they eat loads of carrots!' SPINNING NEWSPAPER #2 (the craft moment) ----
def shot_S2b(t, n):
    f = sepia_bg(t); t0 = st_("S2b")
    spin_paper(f, newspaper_el("NIGHT PILOTS EAT", "LOADS OF CARROTS!", pic="pilot"), t, t0 + 0.02, 540, 1010, 0.9, 5, 0.1, 1.05)
    kw(f, "THE PAPERS SAID:", 540, 300, t, T("a1q", "papers") - 0.12, "pop", 84, col=(250, 240, 220))
    return finish(f, n, look="warm")


# ---- S3: 'The real secret was a brand-new radar in the plane.' the plane's nose cut-away lights up = RADAR + the scope ----
def shot_S3(t, n):
    f = set_blitz(t, beams=0.6, moon_x=930, moon_y=760); t0 = st_("S3"); tr = T("a2", "radar") - 0.1
    k = clamp((t - tr) / 0.12) if t > tr else 0.0
    f *= (0.55 + 0.45 * k)
    comp(f, scale_el(plane_ink_el(cut=True, lit=k), 1.45), 470, 1000)
    prop_spin(f, 470 + 284 * 1.45, 1000, 92, t)
    nx_, ny_ = 470 + (544 - 330) * 1.45, 1000 + (152 - 150) * 1.45
    if k < 1:
        draw_ell_on(f, nx_, ny_, 80, 60, ramp(t, t0 + 0.2, 0.4), BEAM, 6, seed=595)
        kw(f, "?", nx_, ny_ - 150, t, t0 + 0.4, "shake", 120, col=BEAM, amp=0.4)
    else:
        glow(f, nx_, ny_, 140, (140, 255, 170), 0.5)
        radar_scope(f, 540, 1320, 150, t, lit=ramp(t, tr, 0.3))
        draw_arrow_on(f, (nx_, ny_ + 60), (600, 1160), ramp(t, tr, 0.25), SCOPE_L, 6, 22)
    kw(f, "THE REAL SECRET:", 540, 320, t, T("a2", "real") - 0.12, "pop", 84, col=BEAM)
    if t > tr: kw(f, "RADAR", 540, 480, t, tr, "pop", 170, col=SCOPE_L)
    if t > tr: src(f, SRC_RADAR, t, tr + 0.3, y=1560)
    return finish(f, n, look="night")


# ---- S3b: 'The carrots? Just a cover story.' the carrot in a spy disguise sneaks across a searchlit roof; COVER STORY stamp ----
def shot_S3b(t, n):
    f = set_blitz(t, beams=1.0); t0 = st_("S3b"); tc = T("a2", "cover") - 0.1
    x = 300 + 240 * ramp(t, t0, 1.2)
    bob = abs(math.sin((t - t0) * 7)) * 18
    lamp_pool(f, x, 1300, 300, 0.35)
    comp(f, scale_el(carrot_ink_el(mood="n", disguise=True, look=(0.6, 0)), 1.7), x, 1150 - bob)
    kw(f, "THE CARROTS?", 540, 320, t, t0 + 0.02, "sneak", 100, col=ACC)
    if t > tc: el_at(f, vstamp_el("COVER STORY", RED, 96), 600, 560, 1.0, t, tc, rot=-8)
    return finish(f, n, look="night")


# ---- S4: 'Carrots do help a bit. Your body turns them into vitamin A,' the BOARD: carrot -> arrow -> vitamin A ----
def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tb = T("b1", "body") - 0.1; tv = T("b1", "vitamin") - 0.1
    el_at(f, carrot_ink_el(mood="happy"), 250, 1020, 1.25, t, t0 + 0.05, rot=-8)
    kw(f, "CARROTS DO HELP", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    kw(f, "A BIT", 540, 440, t, T("b1", "bit.") - 0.1, "pop", 80, col=ACC_S)
    if t > tb:
        draw_arrow_on(f, (380, 1020), (680, 1020), ramp(t, tb, 0.3), BP_INK, 8, 30)
        write_on(f, "your body", 530, 930, t, tb, 36, BP_INK, cps=40)
    if t > tv:
        el_at(f, vit_a_el("happy"), 830, 1010, 1.35, t, tv)
        kw(f, "VITAMIN A", 540, 1360, t, tv, "pop", 130, col=ACC_S)
    peek(f, t, 900, 640, 0.42, expr="happy", look=(-0.6, 0.6))
    src(f, SRC_VITA, t, t0 + 0.4, y=1560)
    return finish(f, n, look="fresh")


# ---- S4b: '...and your eyes need it to see in dim light.' the board eye: vitamin A drops ride to the back of the eye, it lights up ----
EX, EY = 600, 1000


def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b"); td = T("b1", "dim") - 0.1
    eye_board(f, EX, EY, t, k=ramp(t, t0, 0.5), R=280, pupil=0.75, rays=ramp(t, td, 0.5), light_amt=0.35)
    for i in range(4):
        u = clamp((t - t0 - 0.2 - i * 0.18) / 0.9)
        if 0 < u < 1:
            x = 130 + (EX + 230 - 130) * eio(u); y = 1420 - (1420 - EY - 40 + 30 * i) * eio(u)
            comp(f, scale_el(vit_a_el("happy"), 0.35), x, y)
    lit = ramp(t, td + 0.2, 0.4)
    if lit > 0:
        glow(f, EX + 250, EY, 150, (255, 190, 120), 0.45 * lit)
        draw_arrow_on(f, (EX + 380, EY + 330), (EX + 270, EY + 120), lit, ACC_S, 7, 24)
        write_on(f, "the back of your eye", 600, EY + 400, t, td + 0.2, 34, ACC_S, cps=40)
    kw(f, "YOUR EYES NEED IT", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > td: kw(f, "IN DIM LIGHT", 540, 450, t, td, "pop", 104, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S5: 'But extra carrots won't give you night vision.' night kitchen, carrot stubs everywhere, the beams DON'T come on ----
def shot_S5(t, n):
    f = night_kitchen(t) * 0.75; tn = T("b2", "night") - 0.1
    tk = take(t, tn, 0.8) if t > tn else None
    chub(f, 660, 2050 + (tk["dy"] if tk else 0), 1.85, t=t, la=(30, 20), ra=(30, 20), mouth=munch(t) if tk is None else "o",
         expr=tk["expr"] if tk else "happy", brow=tk["brow"] if tk else "up", squash=tk["squash"] if tk else 0.0, look=(0.4, -0.3))
    comp(f, scale_el(plate_el(), 1.0), 200, 1480)
    for i in range(7):
        rot_comp(f, scale_el(carrot_ink_el(bite=2), 0.36), 110 + 30 * i, 1430 - 18 * (i % 3), 60 + 16 * i, 1.0, 1.0, 0.0)
    hook_band(f, 250, 660, 0.72)
    kw(f, "EXTRA CARROTS", 540, 330, t, T("b2", "extra") - 0.1, "pop", 96, col=ACC_S)
    if t > tn: kw(f, "NIGHT VISION", 540, 500, t, tn, "drop", 104, col=BP_INK, t1=tn + 0.6)
    return finish(f, n, look="night")


# ---- S5b: 'They only help if you're short on vitamin A.' two TANKS with a FULL line ----
def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); ts = T("b2", "short") - 0.1
    k1 = ramp(t, t0 + 0.3, 0.9)
    vit_tank(f, 300, 1300, 260, 520, 0.18 + 0.62 * k1, t)
    vit_tank(f, 780, 1300, 260, 520, 0.8, t)
    for x in (300, 780):
        if k1 < 0.95: comp(f, scale_el(carrot_ink_el(), 0.55), x, 640 + 160 * k1)
    write_on(f, "short on A", 300, 1400, t, t0 + 0.1, 36, BP_INK, cps=40)
    write_on(f, "already enough", 780, 1400, t, t0 + 0.3, 36, BP_INK, cps=40)
    if k1 > 0.95:
        kw(f, "HELPS!", 300, 700, t, t0 + 1.2, "pop", 84, col=OKG)
        kw(f, "NO CHANGE", 780, 700, t, t0 + 1.35, "drop", 70, col=RED, t1=t0 + 2.2)
    kw(f, "ONLY IF YOU'RE", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > ts: kw(f, "SHORT ON IT", 540, 440, t, ts, "pop", 100, col=ACC_S)
    src(f, SRC_SHORT, t, t0 + 0.4, y=1490)
    return finish(f, n, look="fresh")


# ---- S6: 'And if things still look blurry, carrots won't fix that.' Chubby crunches, squints at a chart that goes blurry ----
def shot_S6(t, n):
    f = board_bg(); tb = T("c1", "blurry,") - 0.1; tf = T("c1", "fix") - 0.1
    el_at(f, eye_chart_el(), 760, 980, 1.25)
    if t > tb: f[:] = cv2.GaussianBlur(f, (0, 0), 2 + 7 * ramp(t, tb, 0.4))
    s = 1.8
    chub(f, 330, 2080, s, t=t, la=(22, 12), ra=(150, -150), hand_r="grip", mouth=munch(t), expr="sus", brow="sus", look=(0.8, -0.3), lean=4)
    rot_comp(f, scale_el(carrot_ink_el(bite=1), 0.9), 330 + 120 * s, 2080 - 420 * s + 60 * s, -70, 1.0, 1.0, 0.0)
    if t > tb: kw(f, "STILL BLURRY?", 540, 330, t, tb, "shake", 104, col=RED, amp=0.3)
    if t > tf: kw(f, "CARROTS WON'T FIX IT", 540, 470, t, tf, "pop", 70, col=INKC)
    return finish(f, n, look="fresh")


# ---- S6b: '...it's time to get your eyes checked.' the eye doctor points at a sharp chart ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); tc = T("c1", "checked.") - 0.1
    el_at(f, eye_chart_el(), 780, 1060, 1.15)
    doctor59(f, 360, 1700, 1.5, t)
    kw(f, "GET YOUR EYES", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tc: kw(f, "CHECKED", 540, 470, t, tc, "pop", 140, col=ACC_S)
    src(f, SRC_CHECK, t, t0 + 0.3, y=1560)
    return finish(f, n, look="fresh")


# ---- S7: send line: the night kitchen, mom raises the carrot, Chubby points at us ----
def shot_S7(t, n):
    f = night_kitchen(t); tm = T("c2", "eat") - 0.1
    mom_cheer(f, t, mouth="jaw" if t > tm else 0)
    chub(f, CX + 40, CY, CS, t=t, la=(26, 14), ra=(110, 110), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2))
    hook_band(f, 250, 600, 0.78)
    ui_word(f, "send this to the mom who still says", "[EAT YOUR CARROTS!]", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=92, lead_col=INKC)
    return finish(f, n, look="night")


# ---- S8: the logo beat ----
def shot_S8(t, n):
    t0 = st_("S8"); f = night_kitchen(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S9: the LOOP TAIL ----
def shot_S9(t, n):
    f = night_kitchen(t - END)
    scene0(f, t - END)
    hook_band(f, a=0.66)
    return finish(f, n, look="night")


def newspaper_hi(h1, h2, pic):
    """the 1940 front page with the headline in Hindi (masthead + date stay as printed)."""
    def mk():
        pm, a = newspaper_el(" ", "", pic=pic); pm = pm.copy(); a = a.copy()
        for txt, yy, sz in ((h1, 230, 66), (h2, 320, 66)):
            if not txt: continue
            e = hi_el(txt, sz, INKC, NEWS)
            ep, ea = e
            if ea.shape[1] > 690: ep, ea = scale_el(e, 690 / ea.shape[1])
            h_, w_ = ea.shape; x0 = (a.shape[1] - w_) // 2; y0 = yy - h_ // 2
            reg = slice(y0, y0 + h_), slice(x0, x0 + w_)
            pm[reg] = ep + pm[reg] * (1 - ea[..., None]); a[reg] = ea + a[reg] * (1 - ea)
        return pm, a
    return gcache(("newshi59", h1, h2, pic), mk)


def shot_S1b(t, n):
    f = sepia_bg(t); t0 = st_("S1b"); tc = T("i2", "cover-up.") - 0.1
    spin_paper(f, newspaper_hi("गाजर से पायलटों को", "बिल्ली जैसी आँखें!", "carrot"), t, t0 + 0.02, 540, 1010, 0.85, 4, 0.1, 1.0)
    kw(f, "WARTIME", 540, 300, t, T("i2", "wartime") - 0.12, "pop", 96, col=(250, 240, 220))
    if t > tc: el_at(f, vstamp_el("COVER-UP?", RED, 84), 720, 1230, 1.0, t, tc, rot=-12)
    return finish(f, n, look="warm")


def shot_S2b(t, n):
    f = sepia_bg(t); t0 = st_("S2b")
    spin_paper(f, newspaper_hi("रात के पायलट खाते हैं", "ढेर सारी गाजर!", "pilot"), t, t0 + 0.02, 540, 1010, 0.9, 5, 0.1, 1.05)
    kw(f, "THE PAPERS SAID:", 540, 300, t, T("a1q", "papers") - 0.12, "pop", 84, col=(250, 240, 220))
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "see") - 0.12, 0.3, 12), (T("i2", "yes,") - 0.1, 0.3, 10), (T("i2", "cover-up.") - 0.1, 0.35, 12),
           (T("a1", "shooting") - 0.05, 0.3, 12), (T("a2", "radar") - 0.1, 0.4, 16), (T("a2", "cover") - 0.1, 0.3, 12),
           (T("b1", "vitamin") - 0.1, 0.3, 10), (T("b2", "night") - 0.1, 0.3, 10), (T("c1", "blurry,") - 0.1, 0.3, 10)]


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


# ================= HINDI VERSION (59h, Bunty voice): every on-screen word in Hindi (Devanagari via PIL + raqm, Baloo 2 ExtraBold / Mukta Bold) =================
from PIL import ImageFont
HI_B = "/home/claude/studio/fonts/hi/Baloo2.ttf"; HI_M = "/home/claude/studio/fonts/hi/Mukta-Bold.ttf"
HI = {"DO YOU KNOW IF": "क्या", "CARROTS": "गाजर खाने से", "= BETTER EYESIGHT?": "आँखें तेज़ होती हैं?",
      "MOM SAYS:": "मम्मी:", "YES!": "हाँ!", "EVEN IN THE DARK": "अंधेरे में भी दिखेगा!", "WARTIME": "जंग का झूठ?",
      "1940": "1940", "NIGHT PILOTS": "रात के पायलट", "THE PAPERS SAID:": "अखबारों में छपा:", "THE REAL SECRET:": "असली राज़:",
      "RADAR": "रडार!", "?": "?", "THE CARROTS?": "और गाजर?", "CARROTS DO HELP": "गाजर थोड़ी", "A BIT": "काम की है",
      "VITAMIN A": "विटामिन A", "YOUR EYES NEED IT": "आँखों को चाहिए", "IN DIM LIGHT": "कम रोशनी में",
      "EXTRA CARROTS": "ज़्यादा गाजर?", "NIGHT VISION": "नाइट विज़न नहीं!", "ONLY IF YOU'RE": "फ़ायदा तभी,", "SHORT ON IT": "जब कमी हो",
      "HELPS!": "फ़ायदा!", "NO CHANGE": "कोई फ़र्क नहीं", "STILL BLURRY?": "धुंधला दिखे?", "CARROTS WON'T FIX IT": "गाजर से ठीक नहीं होगा",
      "GET YOUR EYES": "आँखों की", "CHECKED": "जाँच करवाओ!",
      "your body": "शरीर", "the back of your eye": "आँख का पिछला हिस्सा", "short on A": "विटामिन A कम", "already enough": "पहले से पूरा",
      "COVER-UP?": "झूठ?", "COVER STORY": "बस बहाना!"}
_HIF = {}


def _hifont(path, size):
    k = (path, size)
    if k not in _HIF:
        fnt = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
        try: fnt.set_variation_by_axes([800])
        except Exception: pass
        _HIF[k] = fnt
    return _HIF[k]


def hi_el(text, size=100, col=INKC, stroke=None, path=None, sw=None):
    """a Hindi word/phrase element: fill + an outline (stroke) for legibility on any background; cached."""
    def mk():
        fnt = _hifont(path or HI_B, int(size * 2)); s_ = sw if sw is not None else max(3, int(size * 0.07)) * 2
        d0 = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
        x0, y0, x1, y1 = d0.textbbox((0, 0), text, font=fnt, stroke_width=s_)
        w, h = x1 - x0 + 20, y1 - y0 + 20
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.text((10 - x0, 10 - y0), text, font=fnt, fill=tuple(col) + (255,), stroke_width=s_, stroke_fill=tuple(stroke or PAPER) + (255,))
        return _done(im, w // 2, h // 2)
    return gcache(("hi59", text, size, tuple(col), tuple(stroke or PAPER), path, sw), mk)


def hi_word(f, text, x, y, t, t0, mode="pop", size=100, col=INKC, stroke=None, op=1.0, amp=0.3, t1=None, **k):
    if t < t0 - 1e-6 and t0 > -0.5: return
    el = hi_el(text, size, col, stroke)
    pm, a = el
    maxw = 900
    sc = min(1.0, maxw / max(1, a.shape[1]))
    u = (t - t0) if t0 > -0.5 else 9.0
    k_ = min(1.0, max(0.0, u / 0.22)); s_ = sc * (1 + 0.12 * math.sin(math.pi * k_) * (1 - k_) * 3) * (0.6 + 0.4 * k_) if k_ < 1 else sc
    rot = 0.0; dx = dy = 0.0
    if mode == "shake" and u > 0.2: rot = 3.0 * amp * math.sin(t * 31); dx = 5 * amp * math.sin(t * 47)
    if mode == "drop" and t1 is not None and t > t1:
        v = min(1.0, (t - t1) / 0.35); rot = -9 * v; dy = 26 * v
    if mode == "breathe": s_ *= 1 + 0.05 * math.sin(t * 3)
    if mode == "sneak" and u < 0.5: dx = -160 * (1 - u / 0.5) ** 2
    rot_comp(f, scale_el(el, s_), x + dx, y + dy, rot, 1.0, op * min(1.0, k_ * 3 + 0.01), 0.0)


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    hi = HI.get(text, text)
    hi_word(f, hi, x, y, t, t0, mode, int(size * 0.95), col or ACC_S, stroke=PAPER if sum(col or ACC_S) < 600 else INKC, **{q: v for q, v in k.items() if q in ("op", "amp", "t1")})


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    hi_word(f, HI.get(text, text), x, y, t, t0, "pop", int(size * 1.5), col, PAPER, op)


def hook_words(f, t, t0=-1.0, op=1.0):
    hi_word(f, "क्या", 540, 300, t, t0, "pop", 80, INKC, PAPER, op)
    hi_word(f, "गाजर खाने से", 540, 425, t, t0, "pop", 120, ACC_S, PAPER, op)
    hi_word(f, "आँखें तेज़ होती हैं?", 540, 580, t, t0, "shake", 104, BP_INK, PAPER, op, amp=0.35)


_vstamp0 = vstamp_el


def vstamp_el(text, col=None, size=70):
    text = HI.get(text, text)
    col = col or RED
    def mk():
        fn = _hifont(HI_B, size * 2); tw = fn.getlength(text) / 2; w, h = int(tw + 70), int(size * 1.8); sc = 2
        im = Image.new("RGBA", (w * sc, h * sc), (0, 0, 0, 0)); d = ImageDraw.Draw(im); S = lambda *v: [x * sc for x in v]
        d.rounded_rectangle(S(4, 4, w - 4, h - 4), 12 * sc, fill=(252, 247, 232, 240), outline=tuple(col) + (255,), width=8 * sc)
        d.text((w / 2 * sc, h / 2 * sc), text, font=fn, fill=tuple(col) + (255,), anchor="mm")
        return _done(im, w, h)
    return gcache(("vstamp59h", text, col, size), mk)


def shot_S7(t, n):
    f = night_kitchen(t); tm = T("c2", "eat") - 0.1
    mom_cheer(f, t, mouth="jaw" if t > tm else 0)
    chub(f, CX + 40, CY, CS, t=t, la=(26, 14), ra=(110, 110), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2))
    hook_band(f, 250, 640, 0.78)
    t0 = T("c2", "Send") - 0.05
    hi_word(f, "ये उस मम्मी को भेजो जो कहती हैं:", 540, 340, t, t0, "pop", 62, INKC, PAPER)
    if t > tm: hi_word(f, "गाजर खाओ, अंधेरे में दिखेगा!", 540, 480, t, tm, "shake", 84, ACC_S, PAPER, amp=0.25)
    return finish(f, n, look="night")


def shot_S8(t, n):
    t0 = st_("S8"); f = night_kitchen(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    hi_word(f, "ऐसे और फ़ैक्ट्स के लिए फ़ॉलो करो", 540, 980, t, t0 + 0.1, "pop", 48, INKC, PAPER)
    return finish(f, n, look="warm")


def newspaper_hi(h1, h2, pic):
    """the 1940 front page with the headline in Hindi (masthead + date stay as printed)."""
    def mk():
        pm, a = newspaper_el(" ", "", pic=pic); pm = pm.copy(); a = a.copy()
        for txt, yy, sz in ((h1, 230, 66), (h2, 320, 66)):
            if not txt: continue
            e = hi_el(txt, sz, INKC, NEWS)
            ep, ea = e
            if ea.shape[1] > 690: ep, ea = scale_el(e, 690 / ea.shape[1])
            h_, w_ = ea.shape; x0 = (a.shape[1] - w_) // 2; y0 = yy - h_ // 2
            reg = slice(y0, y0 + h_), slice(x0, x0 + w_)
            pm[reg] = ep + pm[reg] * (1 - ea[..., None]); a[reg] = ea + a[reg] * (1 - ea)
        return pm, a
    return gcache(("newshi59", h1, h2, pic), mk)


def shot_S1b(t, n):
    f = sepia_bg(t); t0 = st_("S1b"); tc = T("i2", "cover-up.") - 0.1
    spin_paper(f, newspaper_hi("गाजर से पायलटों को", "बिल्ली जैसी आँखें!", "carrot"), t, t0 + 0.02, 540, 1010, 0.85, 4, 0.1, 1.0)
    kw(f, "WARTIME", 540, 300, t, T("i2", "wartime") - 0.12, "pop", 96, col=(250, 240, 220))
    if t > tc: el_at(f, vstamp_el("COVER-UP?", RED, 84), 720, 1230, 1.0, t, tc, rot=-12)
    return finish(f, n, look="warm")


def shot_S2b(t, n):
    f = sepia_bg(t); t0 = st_("S2b")
    spin_paper(f, newspaper_hi("रात के पायलट खाते हैं", "ढेर सारी गाजर!", "pilot"), t, t0 + 0.02, 540, 1010, 0.9, 5, 0.1, 1.05)
    kw(f, "THE PAPERS SAID:", 540, 300, t, T("a1q", "papers") - 0.12, "pop", 84, col=(250, 240, 220))
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}
