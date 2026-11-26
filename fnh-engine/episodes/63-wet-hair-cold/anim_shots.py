# ================= shots: FreshNestHub 63 — "Can going out with wet hair give you a cold?" (Chubby INK; 35-50 s rule; ONE takeaway) =================
# COLOUR SCRIPT: the winter-morning FRONT DOOR (warm peach hallway inside, a cold foggy blue morning through the open door = the 'cold' everyone blames)
# for the story; the white BOARD (blue ink + wet teal) for every explanation (no virus in a water drop, the icon array, the nose vessel that squeezes);
# the 2005 LAB (pale green tiles, fluorescent) for the Cardiff test. ONE accent = WET TEAL (water, towel). Virus = olive, blood = red, fighters = mint.
# Story: frame 0 = Chubby stepping out of the door with dripping wet hair, shivering, mom mid-yell behind him waving a towel -> the question.
# 'No.' (board: a magnified hair drop = just water, NO VIRUS) -> cold = VIRUS + YOU (equation) -> colds come from people (a neighbour sneezes at the
# door; a hand to the nose carries a virus) -> 'your mom might be half right' (mom, smug, towel) -> 2005 lab: feet in ice water 20 min -> icon array
# 3 in 10 vs 1 in 10 -> board nose: the vessel squeezes, fighters stuck, the sleeping virus wakes -> recap -> wash hands at the hall basin -> mom throws
# the towel over his head (send line) -> logo -> the tail rebuilds frame 0.
END = round(LINES["c2"]["end"] + 0.9, 3)               # 0.05 s air + 0.4 s logo + 0.45 s loop tail
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "can") - 0.12, "punch"),
    ("S1", T("i2", "Short") - 0.12, "whip"), ("S1b", T("i2", "A") - 0.1, "cut"),
    ("S2", T("a1", "Colds") - 0.12, "whip"), ("S2b", T("a1", "hands") - 0.1, "cut"),
    ("S3", T("a2", "But") - 0.1, "punch"),
    ("S4", T("a3", "In") - 0.1, "flash"), ("S4b", T("a3", "ice") - 0.1, "cut"),
    ("S5", T("a4", "Over") - 0.1, "erase"), ("S5b", T("a4", "With") - 0.1, "cut"),
    ("S6", T("a5", "Chilling") - 0.1, "erase"), ("S6b", T("a5", "so") - 0.1, "cut"), ("S6c", T("a5", "and") - 0.1, "punch"),
    ("S7", T("c1", "So") - 0.1, "erase"), ("S7b", T("c1", "Chilling") - 0.1, "cut"),
    ("S8", T("c2", "Wash") - 0.1, "whip"), ("S8b", T("c2", "send") - 0.1, "cut"),
    ("S9", LINES["c2"]["end"] + 0.05, "punch"), ("S10", round(LINES["c2"]["end"] + 0.45, 3), "cut"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
MORPH = {}
CLOCK = {}
CLOCK_D = 0.6
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
    kw(f, "WET HAIR", 540, 430, t, t0, "shiver", 130, col=ACC_S, op=op)
    kw(f, "= A COLD?", 540, 590, t, t0, "shake", 120, col=RED, amp=0.25, op=op)


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


# ---- the cast at the DOOR ----
CX, CY, CS = 720, 1760, 1.62          # Chubby in the doorway
MX, MY, MS = 250, 1720, 1.5           # mom inside


def mom_towel(f, t, x=MX, y=MY, s=MS, wave=1.0, expr="angry", brow="sus", mouth=None, look=(1, 0), lean=0.0, arm=None):
    """mom with the towel up in her screen-right hand; wave 0..1 = how hard she shakes it."""
    sw = wave * 14 * math.sin(t * 11)
    ra = arm or (150 + sw * 0.6, -150 + sw)
    mom58(f, x, y, s, t, la=(30, 30), ra=ra, hand_r="grip", mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look, turn=0.3, lean=lean)
    hx, hy = hand_xy(x, y, s, ra, 1, lean)
    rot_comp(f, scale_el(towel_el(), 0.95 * s / 1.5), hx + 8, hy + 110 * s / 1.5, -8 + sw * 0.8, 1.0, 1.0, 0.0)
    grip_hand(f, hx, hy, s * 0.9)


def wet_chub(f, t, x=CX, y=CY, s=CS, shiv=1.0, look=(-1, -0.1), expr=None, brow=None, mouth=None, la=(30, 40), ra=(30, 40), wet=1.0, lean=0.0,
             turn=-0.4, hand_l="open", hand_r="open", dy=0.0, squash=0.0, hair_dx=0.0, floor=DOOR_FLOOR + 380):
    sv = shiver(t, shiv, s, seed=3) if shiv > 0 else dict(dx=0, lean=0, squash=0, mouth=0, expr="n", brow="n", hair=(0, 0))
    xx = x + sv["dx"]; ln = lean + sv["lean"]; sq = squash + sv["squash"]
    hands = chub(f, xx, y + dy, s, t=t, la=la, ra=ra, hand_l=hand_l, hand_r=hand_r, mouth=sv["mouth"] if mouth is None else mouth,
                 expr=expr or sv["expr"], brow=brow or sv["brow"], look=look, lean=ln, squash=sq, turn=turn, hair=(sv["hair"][0] + hair_dx, 0))
    wet_hair(f, xx, y + dy, s, t, wet, ln, sq, floor=floor)
    if shiv > 0.3: tremble_marks(f, xx, y + dy, s, t)
    return hands, xx, ln


# ---- S0: HOOK at frame 0: Chubby stepping out of the door with dripping wet hair, shivering; mom mid-yell behind him with the towel ----
def scene0(f, t):
    mom_towel(f, t, mouth="o" if int(t * 5) % 2 else 3, expr="angry")
    wet_chub(f, t, look=(-0.8, 0), la=(26, 20), ra=(40, 50))
    mx, my = mouth_xy(CX, CY, CS, t) if "mouth_xy" in globals() else (CX, CY - 380 * CS)
    fog_puffs(f, mx + 20, my, t, period=1.5, dir_=1, s=1.0, t_start=0.2)


def shot_S0(t, n):
    f = set_door(t)
    scene0(f, t)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="cool")


# ---- S0b: '...can give you a cold?' close-up: dripping, teeth chattering ----
def shot_S0b(t, n):
    f = set_door(t); f = dof(f, 6); t0 = st_("S0b")
    sv = shiver(t, 1.0, 2.6, seed=5)
    x = 560 + sv["dx"]
    chub(f, x, 2280, 2.6, t=t, la=(30, -50), ra=(30, -50), mouth=sv["mouth"], expr="ouch", brow="sad", look=(0.2, -0.3), lean=sv["lean"], squash=0.04,
         hair=sv["hair"])
    wet_hair(f, x, 2280, 2.6, t, 1.0, sv["lean"], 0.04)
    hook_band(f); hook_words(f, t)
    return finish(f, n, look="cool")


# ---- S1: 'Short answer? No.' board: a drop from his hair under a magnifier = just water; NO VIRUS stamp on 'No.' ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tn = T("i2", "No.") - 0.1
    peek(f, t, 250, 1230, 0.9, expr="sus", look=(0.8, -0.2))
    kk = ramp(t, t0 + 0.1, 0.45)
    if kk > 0:
        cv2.circle(f, (690, 960), int(230 * kk), C((236, 246, 252)), -1, cv2.LINE_AA)
        el_at(f, wdrop_el("n", (0, 0)), 690, 960, 1.7 * kk)
        draw_ell_on(f, 690, 960, 230, 230, kk, BP_INK, 9, seed=31)
        draw_on(f, [(855, 1125), (960, 1240)], kk, BP_INK, 20, seed=32, tip=False)
    write_on(f, "a drop from your hair", 690, 1330, t, t0 + 0.3, 40, BP_INK, cps=30)
    kw(f, "SHORT ANSWER?", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tn:
        kw(f, "NO.", 540, 470, t, tn, "shake", 160, col=RED, amp=0.3)
        el_at(f, vstamp_el("NO VIRUS", RED, 60), 700, 980, 1.0, t, tn + 0.2, rot=-12)
    return finish(f, n, look="fresh")


# ---- S1b: 'A cold needs a virus, and wet hair doesn't come with one.' board equation: VIRUS + YOU = COLD ; WET HAIR + YOU = just wet ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b"); tv = T("i2", "virus,") - 0.1; tw = T("i2", "wet") - 0.1
    y1, y2 = 860, 1240
    if t > tv - 0.25:
        el_at(f, virus_el("sly", (1, 0), int(t * 8) % 4), 220, y1, 0.95, t, tv - 0.2)
        write_on(f, "+", 375, y1 - 10, t, tv, 90, BP_INK)
        person_icon(f, 520, y1 - 30, 2.2, 0.0, t)
        write_on(f, "=", 670, y1 - 10, t, tv + 0.25, 90, BP_INK)
        person_icon(f, 840, y1 - 30, 2.2, 1.0 if t > tv + 0.4 else 0.0, t)
        write_on(f, "COLD", 840, y1 + 120, t, tv + 0.45, 44, RED)
    if t > tw - 0.2:
        el_at(f, wdrop_el("happy", (1, 0)), 220, y2, 1.2, t, tw - 0.15)
        write_on(f, "+", 375, y2 - 10, t, tw, 90, BP_INK)
        person_icon(f, 520, y2 - 30, 2.2, 0.0, t)
        write_on(f, "=", 670, y2 - 10, t, tw + 0.25, 90, BP_INK)
        if t > tw + 0.4:
            person_icon(f, 840, y2 - 30, 2.2, 0.0, t)
            for j in range(3): cv2.circle(f, (int(800 + 30 * j), int(y2 - 110 + 8 * math.sin(t * 6 + j))), 9, C(WATER), -1, cv2.LINE_AA)
            write_on(f, "just wet", 840, y2 + 120, t, tw + 0.45, 44, ACC_S)
    kw(f, "A COLD NEEDS", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > tv: kw(f, "A VIRUS", 540, 460, t, tv, "pop", 130, col=(92, 118, 40))
    src(f, SRC_MAYO, t, t0 + 0.4, y=1440)
    return finish(f, n, look="fresh")


# ---- S2: 'Colds come from other people, through sneezes, coughs...' at the door: the neighbour uncle sneezes a spray with viruses ----
NX, NY, NS_ = 860, 1700, 1.45


def neighbour(f, t, mouth=0, expr="n", lean=0.0, look=(-1, 0)):
    chub(f, NX, NY, NS_, t=t, shirt=(150, 110, 170), la=(30, 20), ra=(30, 20), mouth=mouth, expr=expr, brow="sad", look=look, lean=lean, turn=-0.5)
    dress(f, NX, NY, NS_, "boss", lean)


def shot_S2(t, n):
    f = set_door(t); t0 = st_("S2"); tz = T("a1", "sneezes,") - 0.1
    pre = t < tz
    neighbour(f, t, mouth="o" if pre else "jaw", expr="ouch" if pre else "gross", lean=-6 * ramp(t, t0, 0.6) + (8 if not pre else 0))
    wet_chub(f, t, x=340, y=1740, s=1.5, shiv=0.5, look=(1, 0), turn=0.4, expr="wow" if t > tz + 0.1 else None, brow="up" if t > tz + 0.1 else None)
    nx, ny = nose_xy(NX, NY, NS_, t, -8)
    sneeze_spray(f, nx - 10, ny + 10, t, tz + 0.05, dirx=-1, n=30, spd=900, seed=4)
    hook_band(f, 250, 600, 0.75)
    kw(f, "COLDS COME FROM", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > T("a1", "people,") - 0.1: kw(f, "OTHER PEOPLE", 540, 460, t, T("a1", "people,") - 0.1, "pop", 110, col=ACC_S)
    return finish(f, n, look="cool")


# ---- S2b: '...and hands that touch your nose.' close-up: Chubby rubs his nose; a tiny virus hops from his fingertip onto it ----
def shot_S2b(t, n):
    f = set_door(t); f = dof(f, 7); t0 = st_("S2b"); tn = T("a1", "nose.") - 0.1
    k = ramp(t, t0, 0.35)
    ra = (40 + 108 * k, 30 - 160 * k)
    hands = chub(f, 560, 2260, 2.5, t=t, la=(26, 14), ra=ra, hand_r="point", mouth=talk(t), expr="n", brow="n", look=(0.3, 0.2), turn=0.2)
    hx, hy = hands[1]
    nx, ny = nose_xy(560, 2260, 2.5, t)
    hop = ramp(t, tn - 0.3, 0.4)
    vx = hx + (nx - hx) * hop; vy = hy - 40 + (ny - hy - 30) * hop - 90 * math.sin(math.pi * hop)
    el_at(f, virus_el("sly", (1, 0), int(t * 8) % 4), vx, vy, 0.55)
    hook_band(f, 250, 560, 0.75)
    kw(f, "HANDS ON YOUR NOSE", 540, 360, t, t0 + 0.05, "pop", 84, col=INKC)
    return finish(f, n, look="cool")


# ---- S3: 'But wait, your mom might still be half right.' mom close with the towel, smug; HALF RIGHT? ----
def shot_S3(t, n):
    f = set_door(t); f = dof(f, 5); t0 = st_("S3"); th = T("a2", "half") - 0.1
    tk = take(t, t0 + 0.05, 0.6)
    mom_towel(f, t, x=560, y=2120, s=2.2, wave=0.4, expr="smirk" if t > th else "wow", brow="up", look=(0, 0), lean=tk["lean"])
    hook_band(f, 250, 600, 0.75)
    kw(f, "BUT WAIT...", 540, 320, t, t0 + 0.05, "pop", 84, col=INKC)
    if t > th: kw(f, "HALF RIGHT?", 540, 470, t, th, "shake", 130, col=ACC_S, amp=0.3)
    return finish(f, n, look="warm")


# ---- S4: 'In two thousand five, scientists put people's feet in ice water...' the 2005 LAB: Chubby (volunteer) sits, feet in an ice basin ----
def shot_S4(t, n):
    f = set_lab(t, top_y=1400); t0 = st_("S4"); ty = T("a3", "two") - 0.1; tf = T("a3", "feet") - 0.1
    cv2.rectangle(f, (0, 1400), (W, H), C((176, 186, 178)), -1)
    sv = shiver(t, 0.6 * ramp(t, tf, 0.5), 1.45, seed=9)
    chub(f, 380 + sv["dx"], 1560, 1.45, t=t, sit=True, la=(30, 10), ra=(30, 10), mouth=sv["mouth"] if t > tf else 0, expr="ouch" if t > tf else "n",
         brow="sad" if t > tf else "n", look=(0.5, 0.4), lean=sv["lean"], shirt=(214, 218, 226))
    el_at(f, footbowl_el(True), 380, 1560, 1.15)
    chub(f, 830, 1720, 1.45, t=t, shirt=COAT, la=(26, 14), ra=(150, -150), hand_r="grip", mouth=talk(t) if t < tf else 0, expr="sus", brow="sus",
         look=(-1, 0.2), turn=-0.4)
    glasses(f, 830, 1720, 1.45, 0, -0.4)
    hx, hy = hand_xy(830, 1720, 1.45, (150, -150), 1)
    el_at(f, clip_el(), hx - 10, hy + 40, 0.75)
    hook_band(f, 250, 600, 0.78)
    kw(f, "2005 TEST", 540, 320, t, ty, "pop", 120, col=ACC_S)
    if t > tf: kw(f, "FEET IN ICE WATER", 540, 470, t, tf, "shiver", 84, col=ACC_S)
    src(f, SRC_CDF, t, t0 + 0.4, y=1462)
    return finish(f, n, look="cool")


# ---- S4b: '...for twenty minutes.' close on the basin: ice cubes bob, a timer runs to 20 MIN; '(feet, not hair!)' ----
def shot_S4b(t, n):
    f = set_lab(t, top_y=1400); f = dof(f, 7); t0 = st_("S4b"); tm = T("a3", "twenty") - 0.1
    cv2.rectangle(f, (0, 1400), (W, H), C((176, 186, 178)), -1)
    el_at(f, footbowl_el(True), 540, 1180 + 6 * math.sin(t * 3), 1.9)
    el_at(f, timer_el(ramp(t, t0 + 0.1, 1.2), "20 MIN"), 830, 760, 0.95)
    hook_band(f, 250, 600, 0.78)
    kw(f, "FOR 20 MINUTES", 540, 330, t, tm, "pop", 100, col=INKC)
    write_on(f, "(feet, not hair!)", 360, 760, t, t0 + 0.3, 40, ACC_S, cps=30)
    return finish(f, n, look="cool")


# ---- S5 / S5b: board ICON ARRAY: CHILLED FEET row of 10 -> 3 catch cold symptoms (29 %); DRY FEET row -> 1 (9 %) ----
GAP = 82; X0 = 540 - 4.5 * GAP


def icon_board(f, t, row2=False):
    tl = [T("a4", "twenty-nine") - 0.1 + 0.15 * j for j in range(3)]
    write_on(f, "CHILLED FEET", 540, 720, t, st_("S5") + 0.1, 46, ACC_S, cps=30)
    icon_row(f, X0, 850, 10, [1, 5, 8], t, tl, gap=GAP, s=1.45)
    if t > tl[0]:
        v = count_up(t, tl[0], 29, 0.8)
        kin_word(f, f"{v}%", 540, 1030, t, tl[0], "pop", 120, col=RED, stroke=2, stroke_col=INKC)
    if row2:
        t2 = T("a4", "nine.") - 0.1
        write_on(f, "DRY FEET", 540, 1140, t, st_("S5b") + 0.05, 46, BP_INK, cps=30)
        icon_row(f, X0, 1250, 10, [6], t, [t2], gap=GAP, s=1.45)
        if t > t2: kin_word(f, "9%", 540, 1430, t, t2, "pop", 110, col=BP_INK, stroke=2, stroke_col=INKC)


def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5")
    icon_board(f, t)
    kw(f, "NEXT FEW DAYS:", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    if t > T("a4", "cold") - 0.1: kw(f, "COLD SYMPTOMS", 540, 450, t, T("a4", "cold") - 0.1, "pop", 96, col=RED)
    return finish(f, n, look="fresh")


def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b")
    icon_board(f, t, True)
    kw(f, "WITH DRY FEET?", 540, 320, t, t0 + 0.05, "pop", 90, col=BP_INK)
    if t > T("a4", "Just") - 0.1: kw(f, "JUST 9%", 540, 450, t, T("a4", "Just") - 0.1, "drop", 110, col=BP_INK, t1=T("a4", "nine.") + 0.5)
    src(f, SRC_CDF, t, t0 + 0.3, y=1520)
    return finish(f, n, look="fresh")


# ---- S6 / S6b / S6c: board NOSE: chilling squeezes the vessel -> fewer germ fighters get through -> the sleeping virus wakes and grows ----
NDY = 90


def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6"); tq = T("a5", "squeezes") - 0.1
    k = ramp(t, t0, 0.5)
    nose_board(f, t, k=k, sq=ramp(t, tq, 0.5), fighters=0.0, vir=0.0, dy=NDY, sc=1.12)
    if t > T("a5", "blood") - 0.1: label_at(f, "BLOOD VESSEL", 830, 1160, t, T("a5", "blood") - 0.1, 470, 800 + NDY, size=30)
    if t > T("a5", "nose,") - 0.1: write_on(f, "your nose", 840, 1010, t, T("a5", "nose,") - 0.1, 44, BP_INK)
    peek(f, t, 880, 1330, 0.75, expr="ouch", look=(-0.8, -0.3), mouth=talk(t))
    kw(f, "CHILLING", 540, 320, t, t0 + 0.05, "shiver", 100, col=ACC_S)
    if t > tq: kw(f, "SQUEEZES IT", 540, 450, t, tq, "pop", 100, col=BLOOD_S)
    src(f, SRC_CDF, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b")
    nose_board(f, t, k=1.0, sq=1.0, fighters=ramp(t, t0, 0.3), vir=0.2, dy=NDY, sc=1.12)
    if t > T("a5", "germ") - 0.1: label_at(f, "GERM FIGHTERS", 300, 1180, t, T("a5", "germ") - 0.1, 400, 760 + NDY - 40, size=30)
    peek(f, t, 880, 1330, 0.75, expr="sad", look=(-0.8, -0.3), mouth=talk(t))
    kw(f, "FEWER FIGHTERS", 540, 320, t, t0 + 0.05, "pop", 96, col=FIGHT_S)
    if t > T("a5", "there,") - 0.1: kw(f, "GET THERE", 540, 450, t, T("a5", "there,") - 0.1, "drop", 96, col=BP_INK, t1=T("a5", "there,") + 0.4)
    return finish(f, n, look="fresh")


def shot_S6c(t, n):
    f = board_bg(); t0 = st_("S6c"); th = T("a5", "head") - 0.1
    wake = ramp(t, T("a5", "already") - 0.1, 0.4)
    nose_board(f, t, k=1.0, sq=1.0, fighters=1.0, vir=0.2 + 0.8 * wake, dy=NDY, sc=1.12)
    if t > T("a5", "already") - 0.1: label_at(f, "ALREADY THERE", 860, 1120, t, T("a5", "already") - 0.1, 600, 800 + NDY, size=30)
    peek(f, t, 880, 1350, 0.7, expr="wow", look=(-0.8, -0.3), mouth=talk(t))
    kw(f, "A VIRUS YOU HAVE", 540, 320, t, t0 + 0.05, "pop", 84, col=(92, 118, 40))
    if t > th: kw(f, "GETS A HEAD START", 540, 450, t, th, "shake", 90, col=RED, amp=0.3)
    return finish(f, n, look="fresh")


# ---- S7: 'So wet hair can't give you a cold.' board: the drop + a red X; S7b: '...might help one you already caught.' recap row ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tc = T("c1", "can't") - 0.1
    el_at(f, wdrop_el("happy", (0, 0)), 540, 960, 2.3, t, t0 + 0.05)
    if t > tc:
        draw_on(f, [(330, 750), (750, 1170)], ramp(t, tc, 0.3), RED, 22, seed=71, tip=False)
        draw_on(f, [(750, 750), (330, 1170)], ramp(t, tc + 0.15, 0.3), RED, 22, seed=72, tip=False)
    write_on(f, "wet hair alone", 540, 1300, t, t0 + 0.2, 46, ACC_S, cps=30)
    kw(f, "WET HAIR", 540, 320, t, t0 + 0.05, "pop", 100, col=ACC_S)
    if t > tc: kw(f, "CAN'T GIVE A COLD", 540, 460, t, tc, "pop", 90, col=RED)
    src(f, SRC_UH, t, t0 + 0.4, y=1462)
    return finish(f, n, look="fresh")


def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b")
    items = [(scale_el(virus_el("sly", (1, 0), int(t * 8) % 4), 0.95), "VIRUS FIRST"), (scale_el(ice_cube_el(), 1.0), "+ A CHILL"),
             (scale_el(tissue_box_el(), 0.8), "= SYMPTOMS")]
    ts = [t0 + 0.1, T("c1", "might") - 0.1, T("c1", "already") - 0.1]
    recap_steps(f, items, 930, t, ts, gap=320, size=1.3)
    peek(f, t, 540, 1340, 0.7, expr="happy", look=(0, -0.4), mouth=talk(t))
    kw(f, "CHILLING MIGHT", 540, 320, t, t0 + 0.05, "pop", 90, col=ACC_S)
    if t > T("c1", "help") - 0.1: kw(f, "HELP ONE YOU HAVE", 540, 450, t, T("c1", "help") - 0.1, "pop", 84, col=BP_INK)
    return finish(f, n, look="fresh")


# ---- S8: 'Wash your hands,' the hall basin by the door: Chubby scrubs with foam; S8b: mom throws the towel over his head ----
def shot_S8(t, n):
    f = set_door(t); t0 = st_("S8")
    k = ramp(t, t0 + 0.1, 0.3)
    rub = 14 * math.sin(t * 16) * k
    hands = wet_chub(f, t, x=360, y=1830, s=1.55, shiv=0.0, look=(0, 0.6), turn=0.0, la=(60 - 20 * k + rub * 0.4, -80 * k - 10),
                     ra=(60 - 20 * k - rub * 0.4, -80 * k - 10), expr="happy", brow="up", mouth=talk(t), wet=0.6, floor=1500)[0]
    hx = (hands[-1][0] + hands[1][0]) / 2; hy = (hands[-1][1] + hands[1][1]) / 2
    el_at(f, sink_el(), hx, hy + 150, 1.15)
    for j in range(6):
        yy = hy - 150 + ((t * 700 + j * 37) % 160)
        cv2.circle(f, (int(hx - 4 + 4 * math.sin(j)), int(yy)), 7, C(WATER), -1, cv2.LINE_AA)
    soap_foam(f, hx, hy, t, n=14, rad=80, k=k)
    hook_band(f, 250, 600, 0.75)
    kw(f, "WASH YOUR HANDS", 540, 360, t, t0 + 0.05, "pop", 104, col=OKG)
    return finish(f, n, look="warm")


def shot_S8b(t, n):
    f = set_door(t); t0 = st_("S8b"); tt = T("c2", "yells,") - 0.1
    mom_towel(f, t, wave=0.0 if t > tt else 0.6, expr="angry" if t < tt + 0.3 else "smirk", mouth=talk(t), arm=(150, -150) if t < tt else (100, -40))
    k = snap(t, tt, 5) if t > tt else 0.0
    wet_chub(f, t, shiv=0.6 * (1 - min(1.0, k)), look=(-0.8, 0), la=(26, 20), ra=(40, 50), expr="wow" if k > 0.5 else None, wet=max(0.0, 1.0 - 0.8 * k))
    towel_head(f, CX, CY, CS, min(1.0, k), t)
    hook_band(f, 250, 640, 0.8)
    ui_word(f, "send this to the mom who yells", "[DRY YOUR HAIR!]", 430, t, t0 + 0.05, col=INKC, acc=ACC_S, size=96, lead_col=INKC)
    return finish(f, n, look="cool")


# ---- S9: the logo beat ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_door(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.2) * 0.95)
    comp(f, ed_el("follow for more food + health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.1) / 0.2))
    return finish(f, n, look="warm")


# ---- S10: the LOOP TAIL ----
def shot_S10(t, n):
    f = set_door(t - END)
    scene0(f, t - END)
    hook_band(f)
    return finish(f, n, look="cool")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "cold?") - 0.1, 0.3, 12), (T("i2", "No.") - 0.1, 0.35, 14), (T("a1", "sneezes,") - 0.05, 0.35, 14), (T("a2", "half") - 0.1, 0.3, 10),
           (T("a3", "feet") - 0.1, 0.25, 8), (T("a4", "twenty-nine") - 0.1, 0.3, 10), (T("a4", "nine.") - 0.1, 0.25, 8), (T("a5", "squeezes") - 0.1, 0.3, 12),
           (T("a5", "head") - 0.1, 0.35, 14), (T("c1", "can't") - 0.1, 0.3, 12), (T("c2", "yells,") - 0.1, 0.3, 10)]


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
    if i == len(SHOTS) - 1:
        if "f0" not in _FIRST: _FIRST["f0"] = rs(SHOTS[0]["id"], 0.0, 0)
        f = loop_seam(f, _FIRST["f0"], t, END, 0.33)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
