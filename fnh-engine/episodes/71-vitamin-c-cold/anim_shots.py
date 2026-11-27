# ================= shots: FreshNestHub 71 — "Does vitamin C stop a cold?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the sunny MORNING WORKTOP (warm, oranges everywhere = the belief) for the story; the white BOARD (blue ink + citrus orange) for every
# explanation (the orange shield the virus hops over, the week of tablets, the 29-trial pile, two equal icon rows, the cold bar that loses one slice, the
# risk bars that halve); the 1970 BOOKSHOP (mustard + brown + a paper lamp) for the origin; the noon PARK as a marathon course for the twist.
# ONE accent = CITRUS ORANGE. Virus = olive.
# NEW CRAFT = MATCH ON ACTION: the glass lift at frame 0 starts in the wide shot and finishes in the close-up (cut a third into the move, one shared
# action clock, a 1-frame smear along the move, the whoosh + gulp running across the cut); the friend's chug at the end does the same.
LIFT_T0, LIFT_D = 1.56, 0.78                 # Chubby's glass lift (S0 -> S0b), cut a third of the way in
LIFT2_T0, LIFT2_D = 42.12, 0.8               # the friend's chug (S8 -> S8b)
END = round(LINES["c2"]["end"] + 0.9, 3)     # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", round(LIFT_T0 + LIFT_D / 3, 3), "action"),
    ("S1", T("i2", "For") - 0.12, "whip"), ("S1b", T("i2", "Taking") - 0.1, "cut"),
    ("S2", T("a1", "Across") - 0.1, "erase"), ("S2b", T("a1", "the") - 0.1, "cut"),
    ("S3", T("a2", "So") - 0.1, "punch"),
    ("S4", T("a3", "In") - 0.1, "flash"), ("S4b", T("a3", "and") - 0.1, "cut"),
    ("S5", T("a4", "What") - 0.1, "erase"),
    ("S6", T("a5", "Except") - 0.12, "whip"), ("S6b", T("a5", "skiers,") - 0.1, "erase"), ("S6c", T("a5", "Their") - 0.1, "cut"),
    ("S7", T("c1", "So") - 0.1, "punch"), ("S7b", T("c1", "not") - 0.1, "erase"),
    ("S8", T("c2", "Send") - 0.1, "whip"), ("S8b", round(LIFT2_T0 + LIFT2_D / 3, 3), "action"),
    ("S9", LINES["c2"]["end"] + 0.05, "punch"), ("S10", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
CLOCK = {}
CLOCK_D = 0.6
ACTION = {"S0b": (0, -34), "S8b": (0, -34)}    # the move's direction + travel per frame on the cut (for the smear)
_write_on0 = write_on


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def hand_xy(x, y, s, arm, side, lean=0.0):
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


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
    kw(f, "VITAMIN C", 540, 430, t, t0, "pop", 130, col=ACC_S, op=op)
    kw(f, "STOPS A COLD?", 540, 590, t, t0, "shake", 110, col=RED, amp=0.25, op=op)


def red_nose(f, x, y, s, t, lean=0.0, k=1.0):
    nx, ny = nose_xy(x, y, s, t, lean)
    glow(f, nx, ny, 30 * s, (240, 70, 60), 0.35 * k)
    cv2.circle(f, (int(nx), int(ny + 2 * s)), int(13 * s), C((226, 84, 74)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(nx - 4 * s), int(ny - 3 * s)), max(1, int(4 * s)), C((255, 200, 190)), -1, cv2.LINE_AA)


def drinker(f, t, x, y, s, sip, level=0.8, shirt=None, gulp_t=None, nose=True, dy=0.0, **k):
    """a person holding a tall glass of orange juice; sip 0..1 = the glass travels from the chest to the mouth and tips (the shared action)."""
    gb = 0.0
    if gulp_t is not None and sip > 0.95 and t > gulp_t: gb = 6 * max(0.0, math.sin((t - gulp_t) * 2 * math.pi / 0.5))
    rr = (150 - 110 * (1 - sip), -128 + 18 * (1 - sip))
    gl = _rot_el(scale_el(glass2_el(OJ, level), 0.62), 34 * sip)
    kk = dict(la=(26, 14), mouth=0 if sip > 0.6 else talk(t), expr="n", brow="n", look=(0.3, -0.3 * sip), turn=0.2)
    kk.update(k)
    if shirt is not None: kk["shirt"] = shirt
    chub(f, x, y - gb + dy, s, t=t, ra=rr, hold=gl, hold_off=(-26 * sip - 6 * (1 - sip), 44 * sip - 24 * (1 - sip)), hold_front=True, hand_r="grip",
         squash=0.02 * gb / 6, **kk)
    if nose: red_nose(f, x, y - gb + dy, s, t, kk.get("lean", 0.0))


# ---- the cast at the WORKTOP ----
CX, CY, CS = 540, 1700, 1.6
TOP = 1440


def worktop_props(f, t, oranges=True):
    if oranges:
        for (ox, oy, sc) in ((150, 1406, 0.62), (230, 1410, 0.58), (190, 1346, 0.6), (900, 1410, 0.6)):
            el_at(f, orange_el(), ox, oy, sc)
        el_at(f, orange_el(half=True), 820, 1430, 0.5)
    el_at(f, tissue_box_el(), 960, 1360, 0.62)
    for j, (tx, ty) in enumerate(((300, 1428), (340, 1432))): el_at(f, tab_el(), tx, ty, 0.26)


def scene0(f, t):
    """frame 0: Chubby with a red nose, a glass of orange juice in his hand, oranges + tablets everywhere; a sneeze at 0.55 s, then the lift."""
    tz = 0.55
    tk = take(t, tz, 0.7) if t > tz - 0.15 else dict(dy=0, squash=0, lean=0)
    inhale = ramp(t, 0.0, 0.5) * (1 - ramp(t, tz, 0.08))
    sip = action_k(t, LIFT_T0, LIFT_D)
    lean = -10 * inhale + (tk.get("lean", 0) if t > tz else 0)
    drinker(f, t, CX, CY, CS, sip, dy=tk.get("dy", 0), expr="ouch" if t < tz + 0.3 else "sad", brow="sad", lean=lean,
            mouth="o" if inhale > 0.3 else 0, look=(0.2, -0.4 * inhale))
    worktop_front(f, TOP)
    worktop_props(f, t)
    if t > tz:
        nx, ny = nose_xy(CX, CY, CS, t, lean)
        sneeze_spray(f, nx + 10, ny + 10, t, tz, dirx=1, n=24, spd=820, seed=7)


def shot_S0(t, n):
    f = set_worktop(t, top_y=TOP)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S0b: MATCH ON ACTION — the same lift, now close: the glass reaches his mouth and he gulps ----
def shot_S0b(t, n):
    f = set_worktop(t, top_y=TOP); f = dof(f, 6)
    sip = action_k(t, LIFT_T0, LIFT_D)
    drinker(f, t, 560, 2330, 2.7, sip, level=0.8 - 0.4 * ramp(t, LIFT_T0 + LIFT_D, 0.8), gulp_t=LIFT_T0 + LIFT_D, expr="n", brow="sad",
            lean=-4 * sip, look=(0.2, -0.3))
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S1: 'For most people? Nope.' board: the orange holds up a C-shield; the virus walks up and hops right over it; NOPE ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tn = T("i2", "Nope.") - 0.1
    peek(f, t, 210, 1300, 0.8, expr="sus", look=(0.8, -0.2))
    el_at(f, orange_el("n" if t < tn else "wow", (1, 0)), 400, 1040, 1.5, t, t0 + 0.05)
    crack = ramp(t, tn + 0.25, 0.3)
    el_at(f, shield_ink_el(crack), 600, 1030, 1.1, t, t0 + 0.2, rot=-4)
    hop = ramp(t, tn - 0.05, 0.55)
    vx = 950 - 230 * ramp(t, t0 + 0.2, max(0.3, tn - t0 - 0.25)) - 520 * hop
    vy = 1060 - 330 * math.sin(math.pi * hop)
    el_at(f, virus_el("sly", (-1, 0), int(t * 8) % 4), vx, vy, 0.78, rot=-200 * hop)
    kw(f, "FOR MOST PEOPLE?", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tn: kw(f, "NOPE.", 540, 470, t, tn, "shake", 150, col=RED, amp=0.3)
    return finish(f, n, look="fresh")


# ---- S1b: '...every day won't stop you catching one.' a week of tablets, and the cold still shows up on Saturday ----
def week_tabs(f, t, t0s, sick_t, y=1000, x0=150, gap=130, size=112):
    for i, dch in enumerate("MTWTFSS"):
        x = x0 + i * gap
        cv2.rectangle(f, (int(x - size / 2), int(y - size / 2)), (int(x + size / 2), int(y + size / 2)), C(BP_INK), 6, cv2.LINE_AA)
        comp(f, ed_el(dch, "", lead_col=BP_INK, lead_size=44), x, y - size / 2 - 42)
        if t > t0s[i]: el_at(f, tab_el(), x, y, 0.52, t, t0s[i])
    if t > sick_t:
        x = x0 + 5 * gap
        el_at(f, virus_el("sly", (0, 0), int(t * 8) % 4), x, y + 190, 0.62, t, sick_t)
        write_on(f, "a cold!", x, y + 330, t, sick_t + 0.1, 40, RED, cps=30)
        draw_arrow_on(f, (x, y + 120), (x, y + 70), ramp(t, sick_t, 0.2), RED, 7, 22)


def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b")
    ts = [t0 + 0.1 + 0.2 * i for i in range(7)]
    week_tabs(f, t, ts, T("i2", "catching") - 0.1)
    kw(f, "EVERY DAY", 540, 320, t, t0 + 0.05, "pop", 100, col=ACC_S)
    if t > T("i2", "won't") - 0.1: kw(f, "STILL CATCH ONE", 540, 460, t, T("i2", "won't") - 0.1, "pop", 96, col=RED)
    peek(f, t, 190, 1400, 0.62, expr="ouch", look=(0.6, -0.4), mouth=talk(t))
    return finish(f, n, look="fresh")


# ---- S2: 'Across twenty-nine trials and eleven thousand people,' the pile of trials + the crowd ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); t29 = T("a1", "twenty-nine") - 0.1; t11 = T("a1", "eleven") - 0.1
    k = ramp(t, t29, 0.7)
    if t > t29 - 0.1:
        nn = max(1, int(round(1 + 7 * k)))
        el_at(f, pile_el(nn), 290, 1180 - 13 * nn, 1.3)
        write_on(f, "trials", 290, 1330, t, t29 + 0.3, 44, BP_INK, cps=30)
    if t > t11:
        for r in range(5):
            for c in range(4):
                i = r * 4 + c
                if t > t11 + 0.03 * i: person_icon(f, 650 + c * 92, 820 + r * 100, 1.2, 0.0, t)
        write_on(f, "11,306 people", 790, 1360, t, t11 + 0.3, 40, BP_INK, cps=40)
    kw(f, "ACROSS", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > t29: kw(f, f"{count_up(t, t29, 29, 0.7)} TRIALS", 540, 450, t, t29, "pop", 110, col=ACC_S)
    src(f, SRC_COCH, t, t0 + 0.4, y=1470)
    return finish(f, n, look="fresh")


# ---- S2b: '...the colds came just as often.' two icon rows (took it / didn't) with the same number sick = ----
GAP = 82; X0 = 540 - 4.5 * GAP


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tc = T("a1", "colds") - 0.1; tj = T("a1", "just") - 0.1
    write_on(f, "TOOK VITAMIN C", 540, 720, t, t0 + 0.05, 44, ACC_S, cps=40)
    icon_row(f, X0, 850, 10, [2, 5, 8], t, [tc + 0.12 * j for j in range(3)], gap=GAP, s=1.45)
    write_on(f, "NO VITAMIN C", 540, 1030, t, t0 + 0.2, 44, BP_INK, cps=40)
    icon_row(f, X0, 1160, 10, [1, 4, 7], t, [tc + 0.3 + 0.12 * j for j in range(3)], gap=GAP, s=1.45)
    if t > tj:
        for dy in (-14, 14): draw_on(f, [(470, 1310 + dy), (610, 1310 + dy)], ramp(t, tj, 0.25), RED, 12, seed=21 + dy, tip=False)
    kw(f, "THE COLDS CAME", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tj: kw(f, "JUST AS OFTEN", 540, 450, t, tj, "shake", 100, col=RED, amp=0.25)
    src(f, SRC_COCH, t, t0 + 0.3, y=1420)
    return finish(f, n, look="fresh")


# ---- S3: 'So why does everyone believe it?' worktop: Chubby with an orange, a double take, then the think pose; question marks ----
def shot_S3(t, n):
    f = set_worktop(t, top_y=TOP); t0 = st_("S3"); te = T("a2", "everyone") - 0.1
    lk, ln, ex, br = double_take(t, t0 + 0.05)
    th = ramp(t, te, 0.25)
    la = (26 + (-186) * th, 14 + (-129) * th)
    chub(f, CX, CY, CS, t=t, la=la, ra=(150, -60), hand_r="grip", hold=scale_el(orange_el(), 0.55), hold_off=(-10, -20), hold_front=True,
         mouth=talk(t), expr="sus" if t > te else ex, brow="sus" if t > te else br, look=lk if t < te else (0.6, -0.4), lean=ln - 4 * th)
    worktop_front(f, TOP); worktop_props(f, t)
    for j in range(3):
        tq = te + 0.15 * j
        if t > tq: kw(f, "?", 800 + 70 * j, 900 - 60 * j, t, tq, "pop", 110 - 15 * j, col=ACC_S)
    hook_band(f, 250, 600, 0.75)
    kw(f, "SO WHY DOES", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > te: kw(f, "EVERYONE BELIEVE IT?", 540, 460, t, te, "pop", 84, col=ACC_S)
    return finish(f, n, look="warm")


# ---- S4: 'In 1970, a two-time Nobel winner wrote a book saying it works,' the 1970 BOOKSHOP: the scientist holds up the book; two medals ----
SX, SY, SS = 700, 1730, 1.45


def shot_S4(t, n):
    f = set_shop70(t); t0 = st_("S4"); t2 = T("a3", "two-time") - 0.1; tb = T("a3", "book") - 0.1; tw = T("a3", "works,") - 0.1
    up = ramp(t, tb - 0.1, 0.3)
    ra = (40 + 125 * up, 30 + 160 * up)
    old_doc(f, SX, SY, SS, t, la=(26, 14), ra=ra, hand_r="grip", mouth=talk(t), expr="happy" if t > tw else "n", brow="up", look=(-0.2, -0.1))
    hx, hy = hand_xy(SX, SY, SS, ra, 1)
    if up > 0.05:
        el_at(f, book70_el(), hx - 10, hy - 110 * up, 0.9 * (0.6 + 0.4 * up)); grip_hand(f, hx, hy, SS * 0.9)
    for j in range(2):                                         # two medals pop onto his coat on 'two-time Nobel'
        tm = t2 + 0.28 * j
        if t > tm: el_at(f, medal_ink_el(), SX - 70 + 60 * j, SY - 330 * SS, 0.62, t, tm)
    shop70_front(f, SHOP_TOP, 1.0, px=330, ps=0.44)
    hook_band(f, 250, 600, 0.72)
    kw(f, "1970", 540, 320, t, t0 + 0.05, "pop", 120, col=ACC_S)
    if t > t2: kw(f, "2 NOBEL PRIZES", 540, 460, t, t2, "pop", 100, col=INKC)
    src(f, SRC_POP, t, t0 + 0.4, y=1462)
    return finish(f, n, look="warm")


# ---- S4b: '...and people went crazy for it.' shoppers rush the table; the pyramid empties; SOLD OUT ----
def shot_S4b(t, n):
    f = set_shop70(t); t0 = st_("S4b"); tc = T("a3", "crazy") - 0.1
    left = 1.0 - 0.9 * ramp(t, t0 + 0.3, 1.3)
    for j, (x0, dir_, sh, kind, stop) in enumerate(((-120, 1, (120, 140, 200), "aunty", 260), (1200, -1, (200, 120, 90), "boss", 820),
                                                    (-300, 1, (150, 110, 170), "cousin", 520))):
        tt = t - t0 - 0.12 * j
        xx = x0 + dir_ * 900 * max(0.0, tt)
        arrived = (dir_ > 0 and xx >= stop) or (dir_ < 0 and xx <= stop)
        if arrived: xx = stop
        w = walk(t, xx, 1700 - 20 * j, 1.2, speed=900, dir=dir_, period=0.5, t0=t0, amt=0.0 if arrived else 1.0, track=True, lift=46)
        if arrived: w["la"] = (150, 170); w["ra"] = (150, 170)
        chub(f, s=1.2, t=t, shirt=sh, mouth="o" if t > tc else 3, expr="wow" if t > tc else "happy", brow="up", **w)
        dress(f, w["x"], w["y"], 1.2, kind, w["lean"])
    shop70_front(f, SHOP_TOP, left)
    if t > tc: el_at(f, vstamp_el("SOLD OUT", RED, 70), 540, 880, 1.0, t, tc, rot=-10)
    hook_band(f, 250, 600, 0.72)
    kw(f, "PEOPLE WENT", 540, 320, t, t0 + 0.05, "pop", 90, col=INKC)
    if t > tc: kw(f, "CRAZY FOR IT", 540, 460, t, tc, "shake", 110, col=ACC_S, amp=0.3)
    return finish(f, n, look="warm")


# ---- S5: 'What it really does is small: taken daily, your colds end a bit sooner.' a cold = 7 day blocks; the last slice drops off ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tsm = T("a4", "small:") - 0.1; tso = T("a4", "sooner.") - 0.15
    k = ramp(t, t0 + 0.1, 0.8)
    write_on(f, "your cold", 540, 820, t, t0 + 0.1, 46, BP_INK, cps=30)
    cut = cold_bar(f, 120, 1000, t, k, trim=ramp(t, tso, 0.9))
    if t > tsm:
        draw_ell_on(f, cut + 34, 1000, 90, 90, ramp(t, tsm, 0.35), RED, 7, seed=51)
    if t > tso: write_on(f, "about 8% shorter", 540, 1210, t, tso + 0.15, 44, ACC_S, cps=40)
    peek(f, t, 200, 1370, 0.62, expr="sus", look=(0.8, -0.4), mouth=talk(t))
    kw(f, "WHAT IT REALLY DOES:", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > tsm: kw(f, "SMALL", 540, 450, t, tsm, "drop", 110, col=ACC_S, t1=tsm + 0.7)
    src(f, SRC_NIH, t, t0 + 0.4, y=1470)
    return finish(f, n, look="fresh")


def bunting(f, t, y=760):
    """race-day bunting: a sagging string of triangle flags across the park (flutters)."""
    cols = [ACC, (70, 130, 200), (200, 60, 60), (250, 220, 90), (72, 190, 150)]
    pts = [(x, y + 60 * math.sin(math.pi * x / W)) for x in range(-40, W + 80, 70)]
    cv2.polylines(f, [np.int32(pts)], False, C(INKC), 4, cv2.LINE_AA)
    for i, (x, yy) in enumerate(pts[:-1]):
        fl = 6 * math.sin(t * 7 + i)
        P = np.int32([(x + 6, yy), (x + 58, yy + 3), (x + 32 + fl, yy + 60)])
        cv2.fillPoly(f, [P], C(cols[i % len(cols)]), cv2.LINE_AA); cv2.polylines(f, [P], True, C(INKC), 3, cv2.LINE_AA)


def blue_snow(f, t, k=1.0, n=36, seed=71, y0=650, y1=1450):
    rng = np.random.default_rng(seed)
    for i in range(int(n * k)):
        x = rng.uniform(80, 1000) + 20 * math.sin(t * 1.5 + i); sp = rng.uniform(90, 160); ph = rng.uniform(0, 1)
        y = y0 + ((t * sp + ph * (y1 - y0)) % (y1 - y0)); r = rng.uniform(9, 16)
        for a in range(3):
            aa = math.radians(60 * a + t * 40)
            cv2.line(f, (int(x - r * math.cos(aa)), int(y - r * math.sin(aa))), (int(x + r * math.cos(aa)), int(y + r * math.sin(aa))), C((90, 150, 220)), 3, cv2.LINE_AA)


# ---- S6: 'Except for one group: marathon runners,' the PARK as a marathon course: Chubby + a rival run past, bibs on ----
def shot_S6(t, n):
    f = set_park(t); t0 = st_("S6"); tm = T("a5", "marathon") - 0.1
    bunting(f, t, 760)
    for j, (x0, sh, num, s_) in enumerate(((90, (150, 110, 170), "12", 1.05), (250, None, "71", 1.2))):
        w = walk(t, x0 + 220 * (t - t0), 1640 + 30 * j, s_, speed=220, dir=1, period=0.52, t0=t0, lift=60, bob=14, arm=46, track=True)
        w["lean"] = w["lean"] + 8
        kk = dict(mouth=3, expr="happy" if j else "n", brow="up")
        if sh is not None: kk["shirt"] = sh
        chub(f, s=s_, t=t, **kk, **w)
        bib(f, w["x"], w["y"], s_, num, w["lean"])
    park_front(f, 1700)
    hook_band(f, 250, 600, 0.72)
    kw(f, "EXCEPT ONE GROUP:", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > tm: kw(f, "MARATHON RUNNERS", 540, 460, t, tm, "pop", 96, col=ACC_S)
    return finish(f, n, look="golden")


# ---- S6b: '...skiers, and soldiers training in the freezing cold.' the three groups as icons; snow starts ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); ts = T("a5", "skiers,") - 0.1; tsl = T("a5", "soldiers") - 0.1; tf = T("a5", "freezing") - 0.1
    items = ((shoe_el(), "runners", t0 + 0.02, 250), (ski_el(), "skiers", ts + 0.05, 540), (helmet_el(), "soldiers", tsl, 830))
    for el, lab, tt, x in items:
        if t > tt:
            el_at(f, el, x, 980, 1.05, t, tt)
            write_on(f, lab, x, 1150, t, tt + 0.1, 42, BP_INK, cps=40)
    if t > tf:
        blue_snow(f, t, ramp(t, tf, 0.4))
        kw(f, "FREEZING COLD", 540, 460, t, tf, "shiver", 100, col=(70, 130, 200))
    kw(f, "SKIERS + SOLDIERS", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    src(f, SRC_COCH, t, t0 + 0.3, y=1470)
    return finish(f, n, look="fresh")


# ---- S6c: 'Their colds dropped by half.' risk bars: no vitamin C full, vitamin C stops at half ----
def shot_S6c(t, n):
    f = board_bg(); t0 = st_("S6c"); td = T("a5", "dropped") - 0.1; th = T("a5", "half.") - 0.05
    risk_bars(f, t, 225, 1280, ramp(t, t0 + 0.05, 0.4), ramp(t, td, 0.6), labels=("no vitamin C", "vitamin C"))
    if t > th:
        draw_arrow_on(f, (760, 640), (760, 960), ramp(t, th, 0.25), RED, 8, 26)
    peek(f, t, 900, 1390, 0.6, expr="wow" if t > th else "sus", look=(-0.6, -0.4), mouth=talk(t))
    kw(f, "THEIR COLDS:", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > th: kw(f, "HALF!", 540, 460, t, th, "drop", 140, col=ACC_S, t1=th + 0.8)
    src(f, SRC_COCH, t, t0 + 0.3, y=1470)
    return finish(f, n, look="fresh")


# ---- S7: 'So eat oranges because they're good food,' worktop in golden light: Chubby munches a juicy orange half ----
def shot_S7(t, n):
    f = set_worktop(t, top_y=TOP); t0 = st_("S7"); tg = T("c1", "good") - 0.1
    chub(f, CX, CY, CS, t=t, la=(26, 14), ra=(150, -112), hand_r="grip", hold=scale_el(orange_el(half=True), 0.62), hold_off=(-30, 20), hold_front=True,
         mouth=munch(t) if t < tg else talk(t), expr="happy", brow="up", look=(0.3, -0.2), lean=-3)
    worktop_front(f, TOP); worktop_props(f, t)
    fly_drops2(f, CX + 120, CY - 620, 300, -500, t, t0 + 0.2, n=6, r=8, col=OJ, rim=OJ_S, floor=TOP)
    hook_band(f, 250, 600, 0.75)
    kw(f, "EAT ORANGES", 540, 320, t, t0 + 0.05, "pop", 96, col=ACC_S)
    if t > tg: kw(f, "THEY'RE GOOD FOOD", 540, 460, t, tg, "pop", 90, col=OKG)
    return finish(f, n, look="golden")


# ---- S7b: '...not a cold shield.' board: the orange keeps its tick, the shield gets a red X ----
def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b"); ts = T("c1", "shield.") - 0.1
    el_at(f, orange_el("happy", (0, 0)), 330, 980, 1.5, t, t0 + 0.02)
    el_at(f, shield_ink_el(0.0), 760, 980, 1.25, t, t0 + 0.1)
    write_on(f, "good food", 330, 1210, t, t0 + 0.2, 44, OKG, cps=40)
    draw_on(f, [(250, 1290), (300, 1340), (410, 1250)], ramp(t, t0 + 0.4, 0.3), OKG, 14, seed=81, tip=False)
    if t > ts:
        draw_on(f, [(620, 830), (900, 1130)], ramp(t, ts, 0.25), RED, 20, seed=82, tip=False)
        draw_on(f, [(900, 830), (620, 1130)], ramp(t, ts + 0.12, 0.25), RED, 20, seed=83, tip=False)
        write_on(f, "cold shield", 760, 1210, t, ts + 0.1, 44, RED, cps=40)
    kw(f, "NOT A", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > ts - 0.1: kw(f, "COLD SHIELD", 540, 450, t, ts - 0.1, "shake", 110, col=RED, amp=0.25)
    return finish(f, n, look="fresh")


# ---- S8: 'Send this to the friend who downs orange juice...' the friend sneezes and reaches for the juice; Chubby points + laughs ----
FX_, FY_, FS_ = 700, 1720, 1.5
FRIEND = (150, 110, 170)


def friend(f, t, x=FX_, y=FY_, s=FS_, sip=0.0, **k):
    drinker(f, t, x, y, s, sip, shirt=FRIEND, **k)
    dress(f, x, y, s, "boss", k.get("lean", 0.0))


def shot_S8(t, n):
    f = set_worktop(t, top_y=TOP); t0 = st_("S8"); tz = t0 + 0.35
    chub(f, 250, 1730, 1.35, t=t, **nolean(POSE["point"]), mouth=3 if t > tz + 0.4 else talk(t), expr="happy", brow="up", look=(1, 0), lean=4, turn=0.5)
    tk = take(t, tz, 0.6) if t > tz - 0.1 else dict(dy=0, lean=0)
    sip = action_k(t, LIFT2_T0, LIFT2_D)
    pre = -8 * ramp(t, t0, 0.3) if t < tz else 0.0
    friend(f, t, sip=sip, expr="ouch" if t < tz + 0.4 else "n", brow="sad", lean=tk.get("lean", 0) + pre,
           mouth="o" if t < tz else (0 if sip > 0.6 else 3), look=(-0.4, -0.2))
    worktop_front(f, TOP); worktop_props(f, t)
    if t > tz:
        nx, ny = nose_xy(FX_, FY_, FS_, t, tk.get("lean", 0))
        sneeze_spray(f, nx - 10, ny + 10, t, tz, dirx=-1, n=20, spd=700, seed=9)
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to the friend who", "[DOWNS JUICE]", 430, t, t0 + 0.05, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S8b: MATCH ON ACTION — the chug finishes in close-up: the juice drains; on 'sneeze!' he sneezes again (the gag) ----
def shot_S8b(t, n):
    f = set_worktop(t, top_y=TOP); f = dof(f, 6); tz = T("c2", "sneeze!") - 0.05
    sip = action_k(t, LIFT2_T0, LIFT2_D) * (1 - ramp(t, tz - 0.25, 0.15))
    lvl = 0.85 - 0.75 * ramp(t, LIFT2_T0 + LIFT2_D, 1.3)
    friend(f, t, x=560, y=2330, s=2.6, sip=sip, level=lvl, gulp_t=LIFT2_T0 + LIFT2_D, expr="n" if t < tz else "ouch", brow="sad",
           mouth=0 if sip > 0.6 else ("o" if t > tz else 3), look=(0.1, -0.3), lean=-4 * sip)
    if t > tz:
        nx, ny = nose_xy(560, 2330, 2.6, t, 0)
        sneeze_spray(f, nx, ny + 10, t, tz, dirx=1, n=26, spd=900, seed=11)
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to the friend who", "[DOWNS JUICE]", 430, t, -1, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    if t > tz: kw(f, "THE SECOND THEY SNEEZE!", 540, 610, t, tz, "shake", 64, col=RED, amp=0.2)
    return finish(f, n, look="warm")


# ---- S9: the logo beat ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_worktop(t, top_y=TOP); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food + health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S10: the LOOP TAIL ----
def shot_S10(t, n):
    f = set_worktop(t - END, top_y=TOP)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "cold?") - 0.1, 0.3, 10), (0.55, 0.3, 12), (T("i2", "Nope.") - 0.1, 0.35, 14), (T("i2", "catching") - 0.1, 0.25, 8),
           (T("a1", "just") - 0.1, 0.3, 10), (T("a3", "two-time") - 0.1, 0.25, 8), (T("a3", "crazy") - 0.1, 0.35, 14), (T("a4", "sooner.") - 0.1, 0.25, 8),
           (T("a5", "freezing") - 0.1, 0.25, 8), (T("a5", "half.") - 0.05, 0.35, 14), (T("c1", "shield.") - 0.1, 0.3, 12), (T("c2", "Send") + 0.25, 0.3, 10),
           (T("c2", "sneeze!") - 0.05, 0.3, 12)]


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
        elif k == "action" and dt < 2 / FPS:                 # MATCH ON ACTION: hard cut + a smear along the move on the first 2 frames
            f = action_smear(f, ACTION[sh["id"]], 1.0 - dt * FPS / 2)
        elif k == "clock" and dt < CLOCK_D:
            cx, cy = CLOCK.get(sh["id"], (540, 960)); f = clock_wipe(rs(SHOTS[i - 1]["id"], t, n), f, dt / CLOCK_D, cx, cy)
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
    if nx is not None and nx["trans"] == "action" and sh["end"] - t < 1 / FPS:   # the last outgoing frame smears too (half strength)
        f = action_smear(f, ACTION[nx["id"]], 0.5)
    if i == len(SHOTS) - 1:
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
