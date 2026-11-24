# ================= shots: FreshNestHub 61 — "Does sitting too close to the TV ruin your eyes?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the dark TV ROOM at night lit ONLY by the screen (cool ambient + the picture's changing colour = the new SCREEN LIGHT craft) + mom's
# warm hallway doorway = the myth; the white BOARD (blue ink + screen blue) for 'no damage', kids' eyes and the nearsighted sign; a warm mustard 1960s
# ROOM with a sepia tint for the origin story (yellow radiation is the only other colour); back to the TV room for the send line + the loop.
# ONE accent = SCREEN BLUE.
# Story: frame 0 = Chubby nose-close to the TV, face lit by the screen, his shadow huge on the wall, mom yelling from the doorway -> the question.
# Every mom yells 'sit back!' -> he scoots back and the light on his face DROPS (falloff = distance). Eye doctors: won't damage them (board eye,
# focus lands on the retina). Where did the fear come from? A silhouette -> the 1960s console TV; some leaked radiation (rays + a meter in the red),
# recalled + fixed, the calendar flips to 1968 -> modern TV = no problem. Today: tired, dry eyes, you forget to blink. Kids focus up close better.
# But ALWAYS sitting close can be a SIGN of nearsightedness (the eye grows long) -> get eyes checked. Send line = mom; the tail rebuilds frame 0.
END = round(LINES["c1"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "can") - 0.12, "punch"),
    ("S1", T("i2", "Every") - 0.12, "whip"), ("S1b", T("i2", "Sit") - 0.12, "cut"),
    ("S2", T("i3", "But") - 0.1, "erase"),
    ("S3", T("a1q", "So") - 0.12, "cut"), ("S4", T("a1", "The") - 0.05, "flash"), ("S4b", T("a1", "Some") - 0.1, "cut"),
    ("S5", T("a2", "They") - 0.12, "punch"), ("S5b", T("a2", "and", 1) - 0.1, "whip"),
    ("S6", T("b1", "Sitting") - 0.12, "flash"), ("S6b", T("b1", "because") - 0.1, "punch"),
    ("S7", T("b2", "And") - 0.1, "erase"),
    ("S8", T("b3", "But") - 0.1, "cut"), ("S8b", T("b3", "Get") - 0.1, "whip"),
    ("S9", T("c1", "Send") - 0.1, "whip"),
    ("S10", LINES["c1"]["end"] + 0.05, "punch"), ("S11", round(LINES["c1"]["end"] + 0.45, 3), "cut"),
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
    kw(f, "TOO CLOSE TO THE TV", 540, 425, t, t0, "shake", 80, col=ACC_S, amp=0.25, op=op)
    kw(f, "= RUINED EYES?", 540, 580, t, t0, "pop", 96, col=RED, op=op)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


def hand_xy(x, y, s, arm, side, lean=0.0):
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


def glasses(f, x, y, s, lean=0.0, turn=0.0):
    hx = x + lean * 2 * s + turn * 14 * s; hy = y - 420 * s - 6 * s
    for sg in (-1, 1):
        cv2.circle(f, (int(hx + sg * 34 * s), int(hy)), int(26 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.line(f, (int(hx - 8 * s), int(hy)), (int(hx + 8 * s), int(hy)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def doc_mirror(f, x, y, s, t, **k):
    chub(f, x, y, s, t=t, shirt=COAT, **k)
    hx2, hy2 = x + k.get("turn", 0.0) * 14 * s, y - 420 * s
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)


# ---- the TV ROOM (frame 0, sit back, today, the send line, the tail): TV on the LEFT facing right, mom's doorway on the RIGHT ----
TVX, TVY, TVS = 190, 1720, 1.5          # flat TV on its cabinet (floor point)
DOOR = (760, 600, 1040, 1330)
MX, MY, MS = 930, 1520, 1.25             # mom in the doorway
CX, CY, CS = 500, 1900, 1.8              # Chubby, nose-close


def tv_room(f, t, cx=CX, cy=CY, cs=CS, mom=True, chub_kw=None, mom_kw=None, light_amt=1.0, r=380, seed=0):
    """the whole TV-room composition with the SCREEN LIGHT: doorway + mom, Chubby's shadow on the wall, Chubby, TV, then the multiply light,
    then the screen + the doorway glow re-lit on top."""
    doorway(f, *DOOR)
    mk = dict(la=(110, 80), ra=(24, 12), hand_l="point", mouth=(2 if t % 0.8 < 0.5 else "o"), expr="angry", brow="sus", look=(-1, 0), turn=-0.5)
    if mom_kw: mk.update(mom_kw)
    if mom: mom58(f, MX, MY, MS, t, **mk)
    ck = dict(la=(24, 12), ra=(24, 12), mouth=0, expr="wow", brow="up", look=(-1, 0), turn=-0.6, lean=-6)
    if chub_kw: ck.update(chub_kw)
    src_xy = (TVX + 60, TVY - 270 * TVS - 165 * TVS)
    cast_shadow_of(f, lambda g: chub(g, cx, cy, cs, t=t, **ck), dx=int(160 * (1 - (cx - TVX) / 900)) + 60, dy=-30, sc=1.18, amt=0.62,
                   blur=14, ymax=1300, ox=src_xy[0], oy=src_xy[1])
    chub(f, cx, cy, cs, t=t, **ck)
    flat_tv(f, TVX, TVY, TVS, t, face=1, seed=seed)
    col = screen_light(f, src_xy[0], src_xy[1], t, amt=light_amt, r=r, amb=0.45, seed=seed)
    flat_tv(f, TVX, TVY, TVS, t, face=1, seed=seed)                    # the glass stays bright
    glow(f, (DOOR[0] + DOOR[2]) / 2, 1000, 340, (255, 196, 130), 0.30)
    return col


def scene0(f, t):
    tv_room(f, t)


def shot_S0(t, n):
    f = set_tvroom(t, flick=0.4)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S0b: '...can ruin your eyes?' close-up: his face a hand's width from the glass, the picture's colours wash over him ----
def shot_S0b(t, n):
    f = set_tvroom(t, flick=0.3); f = dof(f, 4)
    chub_head_only(f, 640, 1220, 2.7, t, mouth="o", expr="wow", brow="up", look=(-1, 0.1), turn=-0.6)
    pic = tv_picture(300, 900, t)
    f[620:1520, 0:300] = pic
    screen_light(f, 150, 1070, t, r=520, amb=0.45, spill=0.15)
    f[620:1520, 0:300] = f[620:1520, 0:300] * 0.3 + pic * 0.7
    cv2.rectangle(f, (0, 600), (310, 1540), C(INKC), 14, cv2.LINE_AA)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="night")


# ---- S1: 'Every mom has yelled it at least once.' mom close in the doorway, finger up ----
def shot_S1(t, n):
    f = set_tvroom(t, flick=0.3); f = dof(f, 4); t0 = st_("S1")
    doorway(f, 200, 600, 900, 1500)
    mom58(f, 560, 2150, 2.3, t, la=(24, 12), ra=(150 + 12 * math.sin(t * 9), 160), hand_r="point", mouth=talk(t), expr="angry", brow="sus", look=(0, 0.1))
    hook_band(f, 250, 560, 0.75)
    kw(f, "EVERY MOM", 540, 320, t, t0 + 0.05, "pop", 110, col=INKC)
    if t > T("i2", "yelled") - 0.1: kw(f, "HAS YELLED IT", 540, 460, t, T("i2", "yelled") - 0.1, "shake", 80, col=RED, amp=0.3)
    return finish(f, n, look="warm")


# ---- S1b: 'Sit back, you'll ruin your eyes!' he scoots back toward the door: the light on his face DROPS with distance ----
def shot_S1b(t, n):
    f = set_tvroom(t, flick=0.4); t0 = st_("S1b"); ts = T("i2", "Sit") - 0.1; ty = T("i2", "you'll") - 0.1
    k = snap(t, ts + 0.25, 6) if t > ts + 0.25 else 0.0
    tk = take(t, ts, 0.8) if t > ts else None
    cx = CX + 110 * k
    tv_room(f, t, cx=cx, cy=CY + 40 * k, cs=CS - 0.15 * k,
            chub_kw=dict(expr="wow" if t > ts else "n", brow="up", mouth="jaw" if ts < t < ts + 0.6 else 0, look=(-0.6, -0.2), lean=(tk["lean"] if tk else -6),
                         squash=(tk["squash"] if tk else 0.0), hair=(-18 * k, 0)),
            mom_kw=dict(la=(140, 150), mouth=2 if t % 0.5 < 0.3 else 3))
    hook_band(f, 250, 600, 0.72)
    if t > ts: kw(f, "SIT BACK!", 540, 340, t, ts, "shake", 150, col=RED, amp=0.5)
    if t > ty: kw(f, "YOU'LL RUIN YOUR EYES!", 540, 500, t, ty, "pop", 66, col=INKC)
    return finish(f, n, look="night")


# ---- S2: 'But eye doctors say... it won't damage them.' board eye: light rays focus right on the retina; NO DAMAGE stamp ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tw = T("i3", "won't") - 0.1
    eye_board(f, 560, 1010, t, k=ramp(t, t0, 0.6), R=300, pupil=0.5, rays=ramp(t, t0 + 0.5, 1.0))
    peek(f, t, 190, 1350, 0.85, expr="happy", look=(0.5, -0.3))
    kw(f, "EYE DOCTORS SAY:", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > tw:
        kw(f, "NO DAMAGE", 540, 460, t, tw, "pop", 130, col=OKG)
        el_at(f, vstamp_el("JUST A MYTH", OKG, 60), 760, 1330, 1.0, t, tw + 0.3, rot=-8)
    src(f, SRC_AAO, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S3: 'So where did that fear come from?' the dark room: a big boxy SILHOUETTE with a '?' ----
def shot_S3(t, n):
    f = set_room60(t, dim=0.85); t0 = st_("S3")
    lamp_pool(f, 540, 1000, 300, 0.25, (220, 210, 255))
    silhouette_reveal(f, crt60_el(), 540, 1060, 0.0, 1.25, dark=(30, 28, 38), rim=(210, 220, 255))
    q = snap(t, t0 + 0.3, 4) if t > t0 + 0.3 else 0
    if q > 0: kw(f, "?", 540, 980, t, t0 + 0.3, "shake", 260, col=PAPER, amp=0.4)
    hook_band(f, 250, 560, 0.75)
    kw(f, "SO WHERE DID", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > T("a1q", "fear") - 0.1: kw(f, "THAT FEAR COME FROM?", 540, 450, t, T("a1q", "fear") - 0.1, "pop", 72, col=ACC_S)
    return finish(f, n, look="night")


# ---- S4: 'The nineteen sixties.' the light clicks on: a 1960s console TV in a mustard living room ----
def shot_S4(t, n):
    t0 = st_("S4"); tr = T("a1", "nineteen") - 0.1
    k = clamp((t - tr) / 0.14)
    f = set_room60(t, dim=0.85 * (1 - k))
    if k > 0: lamp_pool(f, 540, 1000, 340, 0.3 * k)
    silhouette_reveal(f, crt60_el(), 540, 1060, k, 1.25, dark=(30, 28, 38), rim=(210, 220, 255))
    if k >= 1: crt60(f, 540, 1060, 1.25, t)
    sepia(f, 0.35 * k)
    hook_band(f, 250, 560, 0.75)
    if k < 0.5: kw(f, "?", 540, 980, t, -1, "pop", 260, col=PAPER)
    if t > tr: kw(f, "THE 1960s", 540, 380, t, tr, "pop", 150, col=WOOD6_S)
    return finish(f, n, look="warm")


# ---- S4b: 'Some new colour TVs leaked radiation, way above the safe level.' rays leak out; a 1960s kid (Chubby) does a take; the meter goes red ----
def shot_S4b(t, n):
    f = set_room60(t); t0 = st_("S4b"); tl = T("a1", "leaked") - 0.1; tw = T("a1", "way") - 0.1
    sx, sy = crt60(f, 680, 1060, 1.05, t)
    rad_rays(f, sx, sy, t, k=ramp(t, tl, 0.4), n=12, s=1.1, spread=1.25, down=False)
    rad_rays(f, sx, sy, t, k=ramp(t, tl, 0.4), n=5, s=1.0, spread=1.25, down=True)
    tk = take(t, tl + 0.2, 0.9) if t > tl + 0.2 else None
    chub(f, 250, 1930, 1.25, t=t, la=(24, 12) if not tk else (60, 100), ra=(24, 12) if not tk else (60, 100), mouth="jaw" if tk else 0,
         expr=(tk["expr"] if tk else "happy"), brow=(tk["brow"] if tk else "n"), look=(1, -0.2), turn=0.6, squash=(tk["squash"] if tk else 0.0))
    if t > tw: safe_meter(f, 250, 860, 0.55, 0.2 + 0.7 * ramp(t, tw, 0.8), t)
    sepia(f, 0.35)
    hook_band(f, 250, 600, 0.75)
    kw(f, "SOME NEW COLOUR TVs", 540, 320, t, t0 + 0.05, "pop", 74, col=WOOD6_S)
    if t > tl: kw(f, "LEAKED RADIATION", 540, 450, t, tl, "shake", 92, col=RAD_S, amp=0.4)
    if t > tw: kw(f, "WAY ABOVE SAFE", 540, 560, t, tw, "pop", 66, col=RED)
    src(f, SRC_SCIAM, t, t0 + 0.4, y=1462)
    return finish(f, n, look="warm")


# ---- S5: 'They got recalled and fixed,' RECALLED stamp, a spanner taps, the rays switch off, the needle drops to SAFE ----
def shot_S5(t, n):
    f = set_room60(t); t0 = st_("S5"); tr = T("a2", "recalled") - 0.1; tf = T("a2", "fixed,") - 0.1
    sx, sy = crt60(f, 540, 1080, 1.05, t)
    rad_rays(f, sx, sy, t, k=1 - ramp(t, tf, 0.25), n=12, s=1.1, spread=1.25)
    safe_meter(f, 860, 1290, 0.55, 0.9 - 0.75 * ramp(t, tf, 0.5), t)
    if t > tr: el_at(f, vstamp_el("RECALLED", RED, 80), 540, 760, 1.0, t, tr, rot=-10)
    if t > tf:
        el_at(f, vstamp_el("FIXED", OKG, 80), 560, 900, 1.0, t, tf, rot=6)
    sepia(f, 0.35)
    hook_band(f, 250, 560, 0.75)
    kw(f, "RECALLED", 540, 330, t, tr, "pop", 110, col=RED)
    if t > tf: kw(f, "+ FIXED", 540, 470, t, tf, "pop", 110, col=OKG)
    return finish(f, n, look="warm")


# ---- S5b: '...and TVs made after nineteen sixty-eight don't have that problem.' the calendar flips to 1968 -> today's TV, a green tick ----
def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); te = T("a2", "sixty-eight") - 0.1; td = T("a2", "don't") - 0.1
    year_flip(f, 300, 1000, t, t0 + 0.1, te + 0.2, 1960, 1968, s=1.1)
    if t > td:
        k = snap(t, td, 5)
        flat_tv(f, 780, 1300, 1.0 * k + 0.01, t, face=-1)
        el_at(f, check_el(70, True) if "check_el" in globals() else vstamp_el("OK", OKG, 70), 620, 820, 1.0, t, td + 0.2)
    kw(f, "TVs MADE AFTER", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > te: kw(f, "1968", 540, 460, t, te, "pop", 130, col=ACC_S)
    if t > td: kw(f, "NO PROBLEM", 540, 1460 - 40, t, td, "pop", 90, col=OKG)
    return finish(f, n, look="fresh")


# ---- S6: 'Sitting close today just gives you tired, dry eyes,' back in the TV room: he's close again, lids heavy, rubs an eye ----
def shot_S6(t, n):
    f = set_tvroom(t, flick=0.4); t0 = st_("S6"); tt = T("b1", "tired,") - 0.1
    rub = t > tt + 0.5
    tv_room(f, t, mom=False, chub_kw=dict(expr="sleepy" if t > tt else "n", brow="sad" if t > tt else "n", mouth=0,
                                          la=(150, -150) if rub else (24, 12), hand_l="grip" if rub else "open", look=(-1, 0.2)))
    hook_band(f, 250, 560, 0.75)
    kw(f, "SITTING CLOSE TODAY?", 540, 320, t, t0 + 0.05, "pop", 74, col=INKC)
    if t > tt: kw(f, "TIRED, DRY EYES", 540, 460, t, tt, "pop", 96, col=ACC_S)
    src(f, SRC_AAO, t, t0 + 0.4, y=1462)
    return finish(f, n, look="night")


# ---- S6b: 'because you forget to blink.' a face close-up staring without blinking (a blink counter slows) -> on 'blink' a big slow blink ----
def shot_S6b(t, n):
    f = set_tvroom(t, flick=0.4); f = dof(f, 4); t0 = st_("S6b"); tb = T("b1", "blink.") - 0.05
    bl = (tb < t < tb + 0.25)
    chub_head_only(f, 560, 1200, 2.7, t, mouth=0, expr="wow" if not bl else "n", brow="up", look=(-1, 0), turn=-0.5, blink=bl)
    pic = tv_picture(260, 900, t)
    f[620:1520, 0:260] = pic
    screen_light(f, 130, 1070, t, r=620, amb=0.45, spill=0.12)
    f[620:1520, 0:260] = f[620:1520, 0:260] * 0.3 + pic * 0.7
    cv2.rectangle(f, (0, 600), (270, 1540), C(INKC), 14, cv2.LINE_AA)
    hook_band(f, 250, 560, 0.75)
    kw(f, "YOU FORGET TO", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > tb - 0.1: kw(f, "BLINK", 540, 440, t, tb - 0.1, "drop", 130, col=ACC_S, t1=tb + 0.25)
    return finish(f, n, look="night")


# ---- S7: 'And kids can actually focus up close better than grown-ups.' board: a kid with a book at his nose (happy) vs a grown-up at arm's length ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tb = T("b2", "better") - 0.1
    kid58(f, 280, 1500, 1.25, t, ra=(150, -120), hand_r="grip", mouth=0, expr="happy", brow="up", look=(0.5, 0.3))
    hx, hy = hand_xy(280, 1500, 1.25, (150, -120), 1)
    el_at(f, book_el(), hx + 30, hy - 30, 0.5)
    chub(f, 620, 1500, 1.25, t=t, ra=(95, 70), la=(24, 12), hand_r="grip", mouth=0, expr="sus", brow="sus", look=(1, 0.3), turn=0.3, lean=-6)
    glasses(f, 620, 1500, 1.25, -6, 0.3)
    hx2, hy2 = hand_xy(620, 1500, 1.25, (95, 70), 1)
    el_at(f, book_el(), hx2 - 10, hy2 - 30, 0.42)
    write_on(f, "kid", 280, 1400, t, t0 + 0.3, 36, BP_INK, cps=30)
    write_on(f, "grown-up", 640, 1400, t, t0 + 0.5, 36, BP_INK, cps=30)
    kw(f, "KIDS FOCUS UP CLOSE", 540, 320, t, t0 + 0.05, "pop", 76, col=BP_INK)
    if t > tb: kw(f, "BETTER", 540, 460, t, tb, "pop", 130, col=ACC_S)
    src(f, SRC_KIDS, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S8: 'But if your kid always sits close, that could be a sign they're nearsighted.' board: the eyeball grows long, the focus lands short ----
def shot_S8(t, n):
    f = board_bg(); t0 = st_("S8"); ts = T("b3", "sign") - 0.1; tn = T("b3", "nearsighted.") - 0.1
    r = eye_board(f, 560, 1050, t, k=1.0, R=280, pupil=0.5, rays=1.0, length=ramp(t, tn - 0.2, 0.6))
    if t > tn + 0.4: label_at(f, "BLURRY FAR AWAY", 560, 1400, t, tn + 0.4, size=34)
    kw(f, "ALWAYS SITS CLOSE?", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > ts: kw(f, "COULD BE A SIGN", 540, 450, t, ts, "pop", 84, col=ACC_S)
    if t > tn: kw(f, "NEARSIGHTED", 540, 570, t, tn, "shake", 96, col=RED, amp=0.3)
    src(f, SRC_NEAR, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S8b: 'Get their eyes checked.' the eye doctor points at a chart; the kid reads it ----
def shot_S8b(t, n):
    f = board_bg(); t0 = st_("S8b")
    el_at(f, eye_chart_el(), 820, 980, 1.0)
    kid58(f, 230, 1560, 1.3, t, mouth=talk(t), expr="happy", brow="up", look=(1, -0.4), turn=0.5)
    doc_mirror(f, 620, 1600, 1.2, t, la=(26, 14), ra=(120, 80), hand_r="point", mouth=0, expr="happy", brow="up", look=(1, -0.4), turn=0.4)
    kw(f, "GET THEIR EYES", 540, 320, t, t0 + 0.05, "pop", 96, col=BP_INK)
    kw(f, "CHECKED", 540, 460, t, T("b3", "checked.") - 0.1, "pop", 120, col=OKG)
    return finish(f, n, look="fresh")


# ---- S9: send line: Chubby (sitting back now) points at us; mom still mid-yell in the doorway ----
def shot_S9(t, n):
    f = set_tvroom(t, flick=0.4); t0 = st_("S9")
    tv_room(f, t, cx=620, cy=1880, cs=1.6, chub_kw=dict(ra=(24, 12), la=(110, 110), hand_l="point", mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2), turn=0, lean=0),
            mom_kw=dict(mouth=2 if t > T("c1", "sit") - 0.1 and t % 0.5 < 0.3 else 0))
    hook_band(f, 250, 600, 0.78)
    ui_word(f, "send this to the mom who still yells", "[SIT BACK!]", 420, t, t0 + 0.05, col=INKC, acc=RED, size=110, lead_col=INKC)
    return finish(f, n, look="night")


# ---- S10: the logo beat ----
def shot_S10(t, n):
    t0 = st_("S10"); f = set_tvroom(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food + health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S11: the LOOP TAIL ----
def shot_S11(t, n):
    f = set_tvroom(t - END, flick=0.4)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="night")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "TV") - 0.1, 0.3, 12), (T("i2", "Sit") - 0.1, 0.35, 14), (T("i3", "won't") - 0.1, 0.3, 12),
           (T("a1", "nineteen") - 0.1, 0.3, 10), (T("a1", "leaked") - 0.1, 0.35, 14), (T("a2", "recalled") - 0.1, 0.3, 12),
           (T("a2", "fixed,") - 0.1, 0.3, 10), (T("b1", "tired,") - 0.1, 0.25, 8), (T("b3", "nearsighted.") - 0.1, 0.3, 12),
           (T("c1", "back") - 0.1, 0.3, 10)]


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
