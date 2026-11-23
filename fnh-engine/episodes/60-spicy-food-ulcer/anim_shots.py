# ================= shots: FreshNestHub 60 — "Does spicy food give you stomach ulcers?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the noon DHABA (warm ochre, steam glowing off a red curry) = the myth + the uncle; the white BOARD (blue ink + chilli red +
# the olive germ) for the two real causes and the 'sting vs make' split; the cool green 1982 LAB at night for the proof story (one warm spotlight
# for the prize); back to the dhaba for the tip, the send line and the loop.
# ONE accent = CHILLI RED (chilli, curry, sores, the hot words). Olive only on the germ.
# Story: frame 0 = Chubby mid-bite of a red chilli, flushed + sweating over a steaming curry, the uncle wagging a finger -> the question. Uncle says
# yes. The real culprit? Not the chilli (the chilli walks free). Board: a germ (H. pylori) swims in + drills a sore; painkillers taken a lot = a
# second sore. Split: spicy food stings a sore that's there / can't make one. 1982 lab: doctors blamed STRESS; two doctors found the germ (scope).
# So how do you prove it? He drank the germs. On purpose. Days later: inflamed. 2005: the prize. Tip: upper belly keeps hurting -> a doctor;
# don't blame the chilli. Send line = the uncle; the tail rebuilds frame 0 (loop).
# CRAFT (ep 60) = STEAM FROM HOT FOOD (food_steam: travelling-wave ribbons that widen, slow, break up, fade; lighten blend).
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "stomach") - 0.12, "punch"),
    ("S1", T("i2", "Every") - 0.12, "whip"), ("S1b", T("i2", "But") - 0.1, "cut"),
    ("S2", T("a1", "Most") - 0.12, "erase"), ("S2b", T("a1", "or") - 0.1, "cut"),
    ("S3", T("a2", "Spicy") - 0.12, "erase"), ("S3b", T("a2", "It") - 0.1, "cut"),
    ("S4", T("b1", "Back") - 0.12, "flash"), ("S4b", T("b1", "Then") - 0.1, "cut"),
    ("S5", T("b2q", "So") - 0.12, "punch"), ("S5b", T("b2", "One") - 0.1, "cut"),
    ("S6", T("b3", "Days") - 0.12, "whip"), ("S6b", T("b3", "In") - 0.1, "flash"),
    ("S7", T("c1", "If") - 0.12, "erase"), ("S7b", T("c1", "Just") - 0.1, "whip"),
    ("S8", T("c2", "Send") - 0.1, "whip"),
    ("S9", LINES["c2"]["end"] + 0.05, "punch"), ("S10", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
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
    kw(f, "SPICY FOOD", 540, 425, t, t0, "shake", 110, col=ACC_S, amp=0.25, op=op)
    kw(f, "= STOMACH ULCERS?", 540, 590, t, t0, "pop", 82, col=BP_INK, op=op)


def nolean(d): return {k: v for k, v in d.items() if k != "lean"}


def hand_xy(x, y, s, arm, side, lean=0.0):
    a1, a2 = arm; bcx = x + 40 * s * math.sin(math.radians(lean)); bcy = y - 222 * s
    sx, sy = bcx + side * 118 * s, bcy - 46 * s
    ex, ey = sx + side * math.sin(math.radians(a1)) * 76 * s, sy + math.cos(math.radians(a1)) * 76 * s
    return ex + side * math.sin(math.radians(a2)) * 70 * s, ey + math.cos(math.radians(a2)) * 70 * s


# ---- the DHABA (frame 0, the tip, the send line, the tail) ----
CX, CY, CS = 330, 1790, 1.75            # Chubby at the dhaba table (table top 1330)
UX, UY, US = 790, 1780, 1.68            # the uncle on the right
BOWL = (560, 1290, 0.85)                # the curry katori on the table


def bowl_steam(f, t, x=None, y=None, s=None, amt=1.6, n=4, seed=1):
    bx, by, bs = BOWL
    x = bx if x is None else x; y = by if y is None else y; s = bs if s is None else s
    el_at(f, curry_el(), x, y, s)
    food_steam(f, x, y - 22 * s, t, w=150 * s, h=520 * s, n=n, s=s * 1.1, seed=seed, amt=amt)


def sweat(f, x, y, s, t, n=3, seed=0):
    """sweat beads that slide down his face (spicy)."""
    hx, hy = x, y - 420 * s
    for j in range(n):
        u = ((t * 0.6 + j * 0.37 + seed * 0.1) % 1.0)
        sx = hx + (-70 + 70 * j) * s + 6 * s * math.sin(j * 3); sy = hy - 60 * s + 120 * s * u
        el_at(f, sweat_drop_el(), sx, sy, 0.22 * s, op=min(1.0, (1 - u) * 3))


def chilli_bite(f, t, x=CX, y=CY, s=CS, mouth=None, expr="happy", look=(0.6, -0.3), heat=1.0, lean=-3):
    """Chubby biting a red chilli: the screen-right hand holds it, its TIP in his mouth (drawn from hand_xy -> mouth_xy); flush, heat, sweat."""
    arm = (150, -112)
    chub(f, x, y, s, t=t, la=(22, 12), ra=arm, hand_r="grip", mouth=munch(t) if mouth is None else mouth, expr=expr, brow="up", look=look, lean=lean)
    mx, my = mouth_xy(x, y, s, t, lean)
    hx, hy = hand_xy(x, y, s, arm, 1, lean)
    ang = math.degrees(math.atan2(-(my - hy), mx - hx))          # direction hand -> mouth (CCW degrees, screen y down)
    L = math.hypot(mx - hx, my - hy) + 60 * s
    k = L / 290.0
    cxm, cym = hx + (mx - hx) * 0.42, hy + (my - hy) * 0.42
    rot_comp(f, scale_el(red_chilli_el(), k), cxm, cym, ang, 1.0, 1.0, 0.0)
    grip_hand(f, hx, hy, s, kind="grip")
    flush(f, x, y, s, heat, t, lean)
    sweat(f, x, y, s, t)


def uncle_wag(f, t, x=UX, y=UY, s=US, mouth=None, expr="angry"):
    wag = 18 * math.sin(t * 9)
    uncle(f, x, y, s, t, la=(120 + wag, 150), ra=(26, 14), hand_l="point", mouth=(2 if t % 0.9 < 0.55 else 0) if mouth is None else mouth,
          expr=expr, brow="sus", look=(-1, 0), turn=-0.5)


def scene0(f, t):
    uncle_wag(f, t)
    chilli_bite(f, t)
    dhaba_front(f)
    bowl_steam(f, t)


def shot_S0(t, n):
    f = set_dhaba(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S0b: '...a stomach ulcer?' close-up: he chews, sweats, the steam rolls past his face ----
def shot_S0b(t, n):
    f = set_dhaba(t, 9); f = dof(f, 3)
    chilli_bite(f, t, 520, 2350, 2.5, expr="sus", look=(0.2, 0.5), heat=1.0)
    bowl_steam(f, t, 300, 1560, 1.4, n=5, seed=4)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S1: 'Every uncle says yes.' the uncle close, finger wagging; EVERY UNCLE SAYS: YES! ----
def shot_S1(t, n):
    f = set_dhaba(t, 9); f = dof(f, 3); ty = T("i2", "yes.") - 0.1
    uncle(f, 560, 2150, 2.3, t, la=(120 + 18 * math.sin(t * 9), 150), ra=(26, 14), hand_l="point", mouth=talk(t), expr="angry", brow="sus", look=(0, 0.1))
    hook_band(f, 250, 640, 0.72)
    kw(f, "EVERY UNCLE SAYS:", 540, 330, t, T("i2", "Every") - 0.1, "pop", 84, col=INKC)
    if t > ty: kw(f, "YES!", 540, 500, t, ty, "shake", 160, col=ACC_S, amp=0.4)
    return finish(f, n, look="golden")


# ---- S1b: 'But the real culprit? It isn't the chilli.' the chilli in a lamp pool on the table: sad -> NOT GUILTY stamp, it smiles ----
def shot_S1b(t, n):
    f = set_dhaba(t, 9, dim=0.6); t0 = st_("S1b"); tc = T("i2", "culprit?") - 0.1; tn = T("i2", "isn't") - 0.1
    dhaba_front(f)
    lamp_pool(f, 540, 1200, 360, 0.5)
    mood_ = "happy" if t > tn else "sad"
    bob = 10 * abs(math.sin((t - t0) * 6)) if t > tn else 0
    el_at(f, red_chilli_el(mood_, look=(0, -0.3) if t > tn else (0, 0.5)), 540, 1180 - bob, 1.9)
    if t > tc: kw(f, "THE REAL CULPRIT?", 540, 330, t, tc, "pop", 90, col=INKC)
    if t > tn:
        kw(f, "ISN'T THE CHILLI", 540, 480, t, tn, "pop", 96, col=ACC_S)
        el_at(f, vstamp_el("NOT GUILTY", OKG, 90), 560, 900, 1.0, t, T("i2", "chilli.") - 0.05, rot=-8)
    return finish(f, n, look="golden")


# ---- S2: 'Most ulcers come from a germ called H. pylori,' the BOARD stomach; the germ swims in and drills a sore in the lining ----
SORE1 = (420, 980)


def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tg = T("a1", "germ") - 0.1; tp = T("a1", "aitch") - 0.1
    board_stomach(f, t, ramp(t, t0, 0.5), dx=40, dy=120)
    write_on(f, "your stomach", 820, 1350, t, t0 + 0.4, 34, BP_INK, cps=40)
    if t > tg:
        u = ramp(t, tg, 1.1)
        gx = 120 + (SORE1[0] + 60 - 120) * u; gy = 700 + (SORE1[1] - 40 - 700) * u + 20 * math.sin(t * 4)
        drill = clamp((t - tg - 1.1) / 0.6)
        sore(f, SORE1[0], SORE1[1] + 60, 50, drill, t)
        pylori(f, gx, gy + 40, 1.0, t, rot=-35 * u + 6 * math.sin(t * 30) * drill, mood="sly", look=(0.6, 0.6))
    kw(f, "MOST ULCERS?", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tg: kw(f, "A GERM", 540, 450, t, tg, "pop", 120, col=GERM_S)
    if t > tp: label_at(f, "H. PYLORI", 250, 760, t, tp, size=36)
    return finish(f, n, look="fresh")


# ---- S2b: '...or from taking painkillers like aspirin a lot.' pills arc in; a second sore opens ----
SORE2 = (760, 1060)


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tpk = T("a1", "painkillers") - 0.1; tl = T("a1", "lot.") - 0.1
    board_stomach(f, t, 1.0, dx=40, dy=120)
    sore(f, SORE1[0], SORE1[1] + 60, 50, 1.0, t)
    pylori(f, SORE1[0] + 60, SORE1[1] - 10, 0.6, t, rot=-35, mood="sly", look=(0.5, 0.6))
    for j in range(5):
        u = clamp((t - tpk - 0.12 * j) / 0.9)
        if u <= 0: continue
        px = 1000 - (1000 - SORE2[0] - 40 * (j - 2)) * eio(u); py = 560 + (SORE2[1] + 80 - 560) * eio(u) - 160 * math.sin(math.pi * u)
        rot_comp(f, scale_el(pill_el(), 0.55), px, py, 360 * u + 30 * j, 1.0, 1.0, 0.0)
    sore(f, SORE2[0], SORE2[1] + 90, 46, clamp((t - tpk - 1.0) / 0.5), t)
    kw(f, "OR...", 540, 320, t, t0 + 0.05, "pop", 80, col=BP_INK)
    if t > tpk: kw(f, "PAINKILLERS", 540, 450, t, tpk, "pop", 110, col=ACC_S)
    if t > tl: write_on(f, "taken a lot", 540, 560, t, tl, 40, BP_INK, cps=30)
    src(f, SRC_HARV, t, t0 + 0.3, y=1462)
    return finish(f, n, look="fresh")


# ---- S3: 'Spicy food can sting an ulcer that's already there.' split board: left lining WITH a sore, chilli bits land, the sore flares ----
def lining_panel(f, x0, x1, y0, y1, seed):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    cv2.rectangle(f, (x0, y0), (x1, y1), C(PINKC), -1)
    draw_on(f, pts, 1.0, BP_INK, 7, seed=seed, tip=False, closed=True)
    for j in range(5):
        xx = x0 + 30 + j * (x1 - x0 - 60) / 4
        cv2.ellipse(f, (int(xx), int(y0 + 40)), (34, 20), 0, 180, 360, C(PINKC_S), 4, cv2.LINE_AA)


def chilli_drops(f, x, y_top, y_hit, t, t0, n=4, bounce=False):
    for j in range(n):
        u = clamp((t - t0 - 0.18 * j) / 0.45)
        if u <= 0: continue
        px = x + (j - (n - 1) / 2) * 50
        if u < 1: py = y_top + (y_hit - y_top) * u * u
        else:
            v = t - t0 - 0.18 * j - 0.45
            py = y_hit
            if bounce:
                py = y_hit - max(0.0, 520 * v - 1100 * v * v); px += 90 * v * (1 if j % 2 else -1)
        el_at(f, red_chilli_el(), px, py, 0.32, rot=40 * j)


def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); ts = T("a2", "sting") - 0.1
    lining_panel(f, 80, 500, 1000, 1300, 601); lining_panel(f, 580, 1000, 1000, 1300, 602)
    sting = ramp(t, ts + 0.2, 0.2) * (0.7 + 0.3 * math.sin(t * 18)) if t > ts else 0
    sore(f, 290, 1150, 64, 1.0, t, sting)
    chilli_drops(f, 290, 640, 1080, t, t0 + 0.35)
    write_on(f, "already sore", 290, 1380, t, t0 + 0.2, 36, BP_INK, cps=40)
    write_on(f, "healthy", 790, 1380, t, t0 + 0.4, 36, BP_INK, cps=40)
    kw(f, "SPICY FOOD", 540, 320, t, t0 + 0.05, "pop", 90, col=ACC_S)
    if t > ts:
        kw(f, "CAN STING A SORE", 540, 450, t, ts, "shake", 80, col=ACC_S, amp=0.35)
        el_at(f, vstamp_el("OUCH", RED, 64), 300, 860, 1.0, t, ts + 0.3, rot=-10)
    src(f, SRC_STING, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S3b: 'It just can't make one.' right panel: chilli bits bounce off a healthy lining; CAN'T MAKE ONE ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); tm = T("a2", "make") - 0.1
    lining_panel(f, 80, 500, 1000, 1300, 601); lining_panel(f, 580, 1000, 1000, 1300, 602)
    sore(f, 290, 1150, 64, 1.0, t, 0.2)
    chilli_drops(f, 790, 640, 1080, t, t0 + 0.05, bounce=True)
    write_on(f, "already sore", 290, 1380, t, -9, 36, BP_INK, cps=40)
    write_on(f, "healthy", 790, 1380, t, -9, 36, BP_INK, cps=40)
    kw(f, "SPICY FOOD", 540, 320, t, -9, "pop", 90, col=ACC_S)
    if t > tm:
        kw(f, "CAN'T MAKE ONE", 540, 450, t, tm, "pop", 96, col=OKG)
        el_at(f, vstamp_el("NO ULCER", OKG, 64), 800, 860, 1.0, t, tm + 0.2, rot=8)
    return finish(f, n, look="fresh")


SCRUB = (186, 212, 236)


# ---- the LAB: Chubby as the doctor (lab coat + glasses) and a colleague ----
def glasses(f, x, y, s, lean=0.0, turn=0.0):
    hx = x + lean * 2 * s + turn * 14 * s; hy = y - 420 * s - 6 * s
    for sg in (-1, 1):
        cv2.circle(f, (int(hx + sg * 34 * s), int(hy)), int(26 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.line(f, (int(hx - 8 * s), int(hy)), (int(hx + 8 * s), int(hy)), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)


def labdoc(f, x, y, s, t, specs=True, **k):
    k.setdefault("mouth", talk(t))
    chub(f, x, y, s, t=t, shirt=COAT, **k)
    if specs: glasses(f, x, y, s, k.get("lean", 0.0), k.get("turn", 0.0))


def colleague(f, x, y, s, t, **k):
    """the second doctor: light-blue scrubs (generic cartoon, not a likeness)."""
    k.setdefault("mouth", 0)
    chub(f, x, y, s, t=t, shirt=SCRUB, **k)


def shot_S4(t, n):
    f = set_lab(t); t0 = st_("S4"); ts = T("b1", "stress.") - 0.1; tdo = T("b1", "doctors") - 0.1
    labdoc(f, 330, 1960, 2.0, t, la=(30, 20), ra=(150, -150), hand_r="open", expr="sus", brow="sus", look=(0.5, -0.4), turn=0.3)
    colleague(f, 850, 1940, 1.8, t, la=(30, 20), ra=(30, 20), expr="sus", brow="sus", look=(-0.8, 0), turn=-0.4)
    lab_front(f)
    el_at(f, flask_el(col=GERM_L), 660, 1260, 0.7)
    hook_band(f, 250, 640, 0.72)
    kw(f, "1982:", 540, 320, t, t0 + 0.05, "pop", 110, col=INKC)
    if t > tdo: kw(f, "DOCTORS BLAMED", 540, 450, t, tdo, "pop", 74, col=INKC)
    if t > ts: kw(f, "STRESS", 540, 580, t, ts, "shake", 130, col=RED, amp=0.5)
    src(f, SRC_NOBEL, t, t0 + 0.5, y=1462)
    return finish(f, n, look="cool")


# ---- S4b: 'Then two Australian doctors found the germ.' microscope + the round view of spiral germs ----
def shot_S4b(t, n):
    f = set_lab(t, dim=0.25); t0 = st_("S4b"); tf = T("b1", "found") - 0.1
    labdoc(f, 290, 1960, 1.9, t, la=(30, 20), ra=(70, 60), hand_r="grip", mouth=0 if t < tf else "o", expr="wow" if t > tf else "sus", brow="up",
           look=(0.6, 0.6), turn=0.4, lean=6)
    colleague(f, 900, 1940, 1.65, t, la=(80, 60), ra=(30, 20), hand_l="point", mouth=2 if t > tf else 0, expr="wow" if t > tf else "n", brow="up",
              look=(-0.6, 0.3), turn=-0.4)
    lab_front(f)
    el_at(f, microscope_el(), 560, 1220, 0.95)
    scope_view(f, 700, 820, 230, t, ramp(t, t0 + 0.15, 0.35))
    if t > tf: label_at(f, "THE GERM", 700, 1090, t, tf, size=36)
    kw(f, "TWO DOCTORS", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > tf: kw(f, "FOUND THE GERM", 540, 450, t, tf, "pop", 84, col=GERM_S)
    return finish(f, n, look="cool")


# ---- S5: 'So how do you prove it?' he lifts a glass of murky germ broth into the light; the colleague side-eyes ----
def shot_S5(t, n):
    f = set_lab(t, dim=0.2); t0 = st_("S5"); tp = T("b2q", "prove") - 0.1
    tk = take(t, tp, 0.7) if t > tp else None
    colleague(f, 920, 1930, 1.65, t, la=(30, 20), ra=(30, 20), mouth=0, expr="sus", brow="sus", look=(-1, -0.3), turn=-0.5)
    labdoc(f, 340, 2000 + (tk["dy"] if tk else 0), 2.0, t, la=(26, 14), ra=(150, 175), hand_r="grip", hold=scale_el(broth_glass(), 0.6), hold_off=(0, -40),
           hold_front=True, expr="smirk", brow="up", look=(0.4, -0.9), turn=0.3, squash=tk["squash"] if tk else 0.0)
    lab_front(f, 1400)
    gx, gy = hand_xy(340, 2000, 2.0, (150, 175), 1)
    glow(f, gx, gy - 90, 160, (220, 255, 200), 0.25)
    hook_band(f, 250, 640, 0.72)
    kw(f, "SO HOW DO YOU", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > tp: kw(f, "PROVE IT?", 540, 470, t, tp, "shake", 124, col=GERM_S, amp=0.3)
    return finish(f, n, look="cool")


# ---- S5b: 'One of them drank the germs. On purpose.' he gulps it down; the colleague's jaw drops; ON PURPOSE stamp ----
def shot_S5b(t, n):
    f = set_lab(t, dim=0.2); t0 = st_("S5b"); td = T("b2", "drank") - 0.1; tp = T("b2", "purpose.") - 0.1
    sip = ramp(t, td - 0.1, 0.3) * (1 - ramp(t, td + 1.3, 0.3))
    g = gulp(t, td + 0.5)
    colleague(f, 920, 1930, 1.65, t, la=(60, 100), ra=(60, 100), mouth="jaw" if t > td + 0.2 else 0, expr="wow" if t > td + 0.2 else "sus", brow="up",
              look=(-1, -0.2), turn=-0.5)
    ra = (150 - 70 * (1 - sip), -128 + 150 * (1 - sip))
    gl = _rot_el(scale_el(broth_glass(0.75 - 0.6 * ramp(t, td, 1.2)), 0.6), 32 * sip)
    labdoc(f, 360, 2000 + g["dy"], 2.0, t, la=(26, 14), ra=ra, hand_r="grip", hold=gl, hold_off=(-38 * sip - 6 * (1 - sip), -18 * sip - 24 * (1 - sip)),
           hold_front=True, mouth=0 if sip > 0.5 else talk(t), expr="happy" if t < tp else "smirk", brow="up", look=(0.3, -0.3), turn=0.3, squash=g["squash"])
    gulp_mark(f, 360, 2000, 2.0, g["k"])
    lab_front(f, 1400)
    hook_band(f, 250, 640, 0.72)
    if t > td: kw(f, "HE DRANK THE GERMS", 540, 330, t, td, "pop", 80, col=GERM_S)
    if t > tp: el_at(f, vstamp_el("ON PURPOSE!", RED, 84), 560, 520, 1.0, t, tp, rot=-8)
    src(f, SRC_BMJ, t, t0 + 0.4, y=1462)
    return finish(f, n, look="cool")


# ---- S6: 'Days later, his stomach was inflamed.' he clutches his belly (queasy); an x-ray window: red swollen lining with germs inside ----
def shot_S6(t, n):
    f = set_lab(t, dim=0.35); t0 = st_("S6"); ti = T("b3", "inflamed.") - 0.1
    labdoc(f, 540, 2000, 2.0, t, la=(25, -95), ra=(25, -95), hand_l="open", hand_r="open", mouth=0, expr="gross", brow="sad", look=(0, 0.6), lean=-4)
    mood(f, (255, 80, 60), 0.25 * ramp(t, ti, 0.3))
    bx, by = 540, 1480
    m = np.zeros((H, W), np.float32); cv2.circle(m, (bx, by), 150, 1.0, -1, cv2.LINE_AA)
    lay = np.ones_like(f) * np.array(C(PAPER), np.float32)
    red = ramp(t, ti, 0.4)
    cv2.circle(lay, (bx, by), 120, C(_mix(PINKC, ACC, 0.55 * red)), -1, cv2.LINE_AA)
    if red > 0: glow(lay, bx, by, 160, (255, 80, 60), 0.5 * red * (0.8 + 0.2 * math.sin(t * 8)))
    for j in range(3): pylori(lay, bx - 60 + 60 * j, by - 30 + 30 * math.sin(t * 2 + j), 0.3, t, rot=40 * j, mood="sly")
    f[:] = f * (1 - m[..., None]) + lay * m[..., None]
    cv2.circle(f, (bx, by), 150, C(BP_INK), 7, cv2.LINE_AA)
    hook_band(f, 250, 640, 0.72)
    kw(f, "DAYS LATER:", 540, 330, t, t0 + 0.05, "pop", 90, col=INKC)
    if t > ti: kw(f, "INFLAMED", 540, 480, t, ti, "shake", 130, col=ACC_S, amp=0.45)
    return finish(f, n, look="cool")


# ---- S6b: 'In 2005, a Nobel Prize.' spotlight; a gold medal drops onto his coat; he beams; the colleague cheers ----
def shot_S6b(t, n):
    f = set_lab(t, dim=0.7); t0 = st_("S6b"); tn = T("b3", "Nobel") - 0.1
    lamp_pool(f, 540, 1100, 520, 0.6)
    tk = take(t, tn, 0.8) if t > tn else None
    colleague(f, 880, 1780, 1.4, t, **nolean(POSE["cheer"]), mouth=3 if t > tn else 0, expr="happy", brow="up", look=(-0.8, -0.3))
    labdoc(f, 470, 1820 + (tk["dy"] if tk else 0), 1.8, t, **nolean(POSE["tada"]), mouth=3 if t > tn else talk(t), expr="happy", brow="up", look=(0, -0.2),
           squash=tk["squash"] if tk else 0.0)
    k = ramp(t, tn - 0.25, 0.25)
    if k > 0:
        my = 300 + (1290 - 300) * k + (8 * math.sin((t - tn) * 6) if k >= 1 else 0)
        el_at(f, medal_el("2005"), 480, my, 0.75)
    if t > tn:
        for j in range(14):
            u = ((t - tn) * 0.7 + j * 0.071) % 1.0
            cv2.circle(f, (int(120 + 64 * j + 30 * math.sin(t * 3 + j)), int(260 + 1100 * u)), 9, C((GOLD, ACC, OKG, GERM)[j % 4]), -1, cv2.LINE_AA)
    hook_band(f, 250, 560, 0.6)
    kw(f, "2005", 540, 320, t, T("b3", "In") - 0.05, "pop", 110, col=GOLD)
    if t > tn: kw(f, "NOBEL PRIZE", 540, 460, t, tn, "pop", 120, col=GOLD)
    src(f, SRC_NOBEL, t, t0 + 0.4, y=1462)
    return finish(f, n, look="warm")


# ---- S7: 'If your upper belly keeps hurting, it's time to see a doctor.' board: Chubby holds his upper belly (pulsing), a doctor pops in ----
def doc_mirror(f, x, y, s, t, **k):
    chub(f, x, y, s, t=t, shirt=COAT, **k)
    hx2, hy2 = x + k.get("turn", 0.0) * 14 * s, y - 420 * s
    cv2.line(f, (int(hx2 - 96 * s), int(hy2 - 62 * s)), (int(hx2 + 96 * s), int(hy2 - 62 * s)), C(INKC), max(3, int(8 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C((214, 222, 230)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(30 * s), C(INKC), max(2, int(4 * s)), cv2.LINE_AA)
    cv2.circle(f, (int(hx2 - 20 * s), int(hy2 - 74 * s)), int(9 * s), C(INKC), -1, cv2.LINE_AA)


def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); td = T("c1", "doctor.") - 0.15; th = T("c1", "hurting,") - 0.1
    x, y, s = 330, 1820, 1.7
    chub(f, x, y, s, t=t, la=(25, -95), ra=(25, -95), hand_l="open", hand_r="open", mouth=0, expr="sad", brow="sad", look=(0.3, 0.5), lean=-3)
    pu = 0.6 + 0.4 * math.sin(t * 7)
    glow(f, x, y - 215 * s, 90 * s, (255, 90, 60), 0.5 * pu * ramp(t, th, 0.3))
    draw_ell_on(f, x, y - 215 * s, 95 * s, 60 * s, ramp(t, t0 + 0.4, 0.4), ACC_S, 6, seed=607)
    if t > td - 0.3:
        k = snap(t, td - 0.3, 4)
        doc_mirror(f, 810 + 300 * (1 - k), 1820, 1.6, t, la=(26, 14), ra=(70, 40), hand_r="point", mouth=talk(t), expr="happy", brow="up", look=(-0.8, 0), turn=-0.4)
    kw(f, "UPPER BELLY", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > th: kw(f, "KEEPS HURTING?", 540, 440, t, th, "shake", 84, col=ACC_S, amp=0.3)
    if t > td: kw(f, "SEE A DOCTOR", 540, 570, t, td, "pop", 96, col=OKG)
    src(f, SRC_UH, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


# ---- S7b: 'Just don't blame the chilli.' dhaba: Chubby happily bites the chilli again, the uncle gasps ----
def shot_S7b(t, n):
    f = set_dhaba(t); tb = T("c1", "chilli.") - 0.1
    uncle(f, UX, UY, US, t, la=(60, 100), ra=(60, 100), mouth="jaw" if t > tb else 0, expr="wow", brow="up", look=(-1, 0), turn=-0.5)
    chilli_bite(f, t, expr="happy", look=(1, -0.2), heat=0.6)
    dhaba_front(f)
    bowl_steam(f, t, seed=7)
    hook_band(f, 250, 640, 0.72)
    kw(f, "JUST DON'T BLAME", 540, 330, t, st_("S7b") + 0.05, "pop", 80, col=INKC)
    if t > tb: kw(f, "THE CHILLI", 540, 480, t, tb, "shake", 130, col=ACC_S, amp=0.3)
    return finish(f, n, look="golden")


# ---- S8: send line: the uncle slides the curry away, Chubby points at us ----
def shot_S8(t, n):
    f = set_dhaba(t); t0 = st_("S8"); tp = T("c2", "pushes") - 0.1
    u = ramp(t, tp, 0.8)
    uncle(f, UX, UY, US, t, la=(70 - 40 * u, 60 + 40 * u), ra=(26, 14), hand_l="open", mouth=0, expr="angry", brow="sus", look=(-1, 0.4), turn=-0.5)
    chub(f, CX, CY, CS, t=t, la=(26, 14), ra=(110, 110), hand_r="point", mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2))
    dhaba_front(f)
    bowl_steam(f, t, x=560 + 360 * u, seed=9)
    hook_band(f, 250, 600, 0.78)
    ui_word(f, "send this to the uncle who", "[PUSHES THE CHILLI AWAY]", 420, t, t0 + 0.05, col=INKC, acc=ACC_S, size=80, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S9: the logo beat ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_dhaba(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S10: the LOOP TAIL ----
def shot_S10(t, n):
    f = set_dhaba(t - END)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "stomach") - 0.12, 0.3, 12), (T("i2", "yes.") - 0.1, 0.3, 12), (T("i2", "isn't") - 0.1, 0.35, 14),
           (T("a1", "germ") - 0.1, 0.3, 10), (T("a1", "painkillers") - 0.1, 0.3, 10), (T("a2", "sting") - 0.1, 0.3, 12),
           (T("b1", "stress.") - 0.1, 0.3, 10), (T("b2", "drank") - 0.1, 0.3, 12), (T("b2", "purpose.") - 0.1, 0.35, 14),
           (T("b3", "inflamed.") - 0.1, 0.3, 12), (T("b3", "Nobel") - 0.1, 0.4, 16), (T("c1", "chilli.") - 0.1, 0.3, 10)]


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
