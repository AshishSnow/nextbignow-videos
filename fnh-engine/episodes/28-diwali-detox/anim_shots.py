# ================= shots: FreshNestHub 28 — "Do you need a detox after Diwali?" (Chubby INK, ep 11 of the ink look) ===
# COLOUR SCRIPT: JUICE LIME (ACC) = the detox fad only (the drink, the posts, the products, the cleanse). The real organs keep natural ink colours (liver red-brown,
# kidneys rose), fat-soluble junk = greasy yellow, water-soluble = water blue. Morning-after kitchen = the story; the white BOARD = every explanation;
# NEW PLACE = inside the LIVER FACTORY (warm works hall + conveyor). Craft skill: the MORPH CUT (anim_fx.morph_mix) board <-> lit object, 3 times.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "right") - 0.1, "morph"),
    ("S1", T("i2", "No") - 0.15, "whip"), ("S1b", T("i2", "It") - 0.1, "erase"),
    ("S2", T("i3", "So") - 0.15, "whip"), ("S2b", T("i3", "Your") - 0.1, "punch"),
    ("S3", T("a1", "Back") - 0.15, "erase"), ("S3b", T("a1", "which") - 0.1, "punch"),
    ("S4", T("a2", "They") - 0.1, "erase"), ("S4b", T("a2", "not") - 0.1, "punch"),
    ("S5", T("a3", "And") - 0.12, "whip"),
    ("S6", T("a4", "One") - 0.1, "erase"), ("S6b", T("a4", "soap") - 0.2, "punch"),
    ("S7", T("b0", "So") - 0.15, "flash"),
    ("S8", T("b1", "Two") - 0.12, "erase"), ("S8b", T("b1", "It") - 0.1, "morph"),
    ("S9", T("b2", "A") - 0.1, "erase"), ("S9b", T("b2", "and") - 0.1, "punch"),
    ("S10", T("b3", "So") - 0.12, "whip"), ("S10b", T("b4", "Same") - 0.12, "punch"),
    ("S11", T("c0", "And") - 0.12, "flash"),
    ("S12", T("c1", "Each") - 0.1, "whip"), ("S12b", T("c1", "with") - 0.1, "zoom"),
    ("S13", T("c2", "Every") - 0.12, "erase"), ("S13b", T("c2", "Thats") - 0.1, "morph"),
    ("S14", T("c3", "And") - 0.12, "erase"), ("S14b", T("c3", "The") - 0.1, "punch"),
    ("S15", T("c4", "So") - 0.15, "whip"),
    ("S16", T("d0", "Okay") - 0.15, "flash"),
    ("S17", T("d1", "When") - 0.1, "erase"), ("S18", T("d2", "You") - 0.1, "erase"),
    ("S19", T("d3", "And") - 0.1, "whip"), ("S20", T("d4", "And") - 0.1, "erase"),
    ("S21", T("e0", "So") - 0.15, "flash"),
    ("S22", T("e1", "The") - 0.1, "punch"), ("S22b", T("e1", "A") - 0.1, "whip"), ("S22c", T("e1", "and") - 0.1, "whip"),
    ("S23", T("e2", "And") - 0.1, "erase"),
    ("S24", T("f1", "No") - 0.15, "erase"), ("S24b", T("f1", "working") - 0.1, "punch"),
    ("S25", T("f2", "Send") - 0.15, "whip"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
path_at = path_point
_write_on0 = write_on
# MORPH CUTS: (x, y, size) of the matching object in the outgoing shot -> in the incoming shot
MORPH = {"S0b": ((540, 1250, 300), (540, 1100, 470)),       # Chubby's belly (kitchen) -> the x-ray body on the board
         "S8b": ((470, 1010, 230), (540, 1000, 470)),       # the board liver -> the lit liver at the factory
         "S13b": ((540, 980, 420), (540, 1290, 900))}       # the 140-litre tank drawing -> the row of seven real water cans


def write_on(f, text, x, y, t, t0, size=56, col=BP_INK, cps=22.0, op=1.0):
    """phone-size hand lettering (ep 27: the kit default reads too small)."""
    _write_on0(f, text, x, y, t, t0, int(size * 1.3), col, cps, op)


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=420, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=ACC_L, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def t3(f, text, y, t, t0, size=200, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def cc(f, text, x, y, t, t0, bg=None, fg=None, size=34):
    if t >= t0: comp(f, chip(text, bg or INKC, fg or MILK, size), x, y, scale=pin(t, t0))


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def figure(f, k, cx=540, hy=560, col=BP_INK, w=7):
    """board drawing: a front-view head + torso outline (head first, then the body)."""
    draw_ell_on(f, cx, hy, 150, 160, clamp(k / 0.4), col, w, seed=11)
    kb = clamp((k - 0.4) / 0.6)
    for sg in (-1, 1):
        P = [(cx + sg * 52, hy + 152), (cx + sg * 58, hy + 205), (cx + sg * 210, hy + 250), (cx + sg * 250, hy + 330), (cx + sg * 240, hy + 760), (cx + sg * 150, hy + 830)]
        draw_on(f, P, kb, col, w, seed=12 + sg, tip=sg > 0)


def stamp_x(f, x, y, r, k, col=BLOOD_S if "BLOOD_S" in dir() else (150, 24, 34), w=22):
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


RED_X = (176, 40, 44)
LIV_B = (500, 1000)                      # where the liver sits in the board body (S0b, S8)
KID_B = ((370, 1175), (710, 1175))       # the two kidneys in the board body
SRC_SAS = "Source: Sense About Science (2009), via News-Medical + CTV"
SRC_KID = "Source: NIDDK (NIH) · Cleveland Clinic · National Kidney Foundation"
SRC_NCCIH = "Source: NCCIH (NIH, 2025) · Johns Hopkins · Cleveland Clinic"
TD = T("i1", "detox") - 0.05


def body_board(f, t, k=1.0, lit=1.0, work=True, labels=None):
    """the x-ray body on the board: outline + the liver and both kidneys as working characters."""
    figure(f, k, 540, 560)
    if k < 0.6: return
    pk = pin(t, -9) if k >= 1 else clamp((k - 0.6) / 0.4)
    bob = 6 * math.sin(t * 7) if work else 0
    comp(f, scale_el(liver_el("happy", arms="work" if work else None, hat=work), 0.95), LIV_B[0], LIV_B[1] + bob, op=pk)
    for i, (x, y) in enumerate(KID_B):
        comp(f, scale_el(kidney_el("happy", flip=i == 1, hat=work), 0.72), x, y - bob, op=pk)
    if work and lit > 0:
        for j in range(3):
            q = ((t * 0.7 + j / 3) % 1.0)
            x = LIV_B[0] + 60 + (KID_B[0][0] - LIV_B[0] - 60) * q; y = LIV_B[1] + 60 + 80 * q
            cv2.circle(f, (int(x), int(y)), 9, C(WATER_B), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 9, C(BP_INK), 3, cv2.LINE_AA)


# ---- S0: HOOK, frame 0: the morning after Diwali, Chubby is already chugging a giant green DETOX bottle; on 'detox' he SPITS it out (spit-take) ----
def spray(f, x, y, t, t0, n=26, seed=5, col=None):
    if t < t0: return
    rng = np.random.default_rng(seed); q = t - t0
    for j in range(n):
        a = math.radians(rng.uniform(-40, 25)); v = rng.uniform(500, 1300); r = rng.uniform(7, 18)
        px = x + math.cos(a) * v * q; py = y + math.sin(a) * v * q + 900 * q * q
        if py < 1700: cv2.circle(f, (int(px), int(py)), int(r), C(col or ACC), -1, cv2.LINE_AA); cv2.circle(f, (int(px), int(py)), int(r), C(INKC), 3, cv2.LINE_AA)


def shot_S0(t, n):
    f = set_worktop(t); tk = take(t, TD)
    spit = t >= TD
    hx, hy = 470, 1500 - 420 * 1.1
    chub(f, 470, 1500 + (tk["dy"] if spit else 0), 1.1, t=t, la=(30, 16), ra=(150, -130) if not spit else (70, 40), mouth=("jaw" if spit and t < TD + 0.5 else talk(t)) if spit else 0,
         expr="gross" if spit else "n", brow="up" if spit else "n", look=(0.3, -0.2) if spit else (0, -0.6), squash=(tk["squash"] if spit else 0.25 * (0.5 + 0.5 * math.sin(t * 14))),
         lean=(tk["lean"] if spit else -6), hand_r="grip", turn=0.4 if spit else 0)
    worktop_front(f, 1330)
    if not spit:
        rot_comp(f, detox_bottle_el(1.0 - 0.6 * ramp(t, 0, TD)), hx + 70, hy + 20, 118, 0.9, 1.0, 0.2)
        for j in range(3):                                                         # glug bubbles inside
            q = (t * 2.2 + j / 3) % 1.0; cv2.circle(f, (int(hx + 130 + 80 * q), int(hy - 40 - 50 * q)), 8, C(ACC_L), 3, cv2.LINE_AA)
    else:
        rot_comp(f, detox_bottle_el(0.4), 760, 1260, -8 + 6 * math.exp(-(t - TD) * 6) * math.sin((t - TD) * 30), 0.8, 1.0, 0.25)
        spray(f, hx + 40, hy + 70, t, TD)
    icap(f, "your body is running a", "[DETOX]?", t, 0.05, size=150, y=380)
    return finish(f, n, look="golden")


# ---- S0b: '...right now, while you watch this?' MORPH into the BOARD: an x-ray body where the liver + kidneys are already working (hard hats, little blue drops) ----
def shot_S0b(t, n):
    f = board_bg(); t0 = st_("S0b")
    body_board(f, t, 1.0)
    comp(f, chip("RIGHT NOW", ACC_S, MILK, 44), 540, 330, scale=pin(t, t0 + 0.2))
    write_on(f, "liver", 175, 860, t, t0 + 0.35, 48); draw_arrow_on(f, (230, 890), (330, 960), ramp(t, t0 + 0.4, 0.3), BP_INK, 5); write_on(f, "kidneys", 880, 1380, t, t0 + 0.5, 48)
    return finish(f, n, look="fresh")


# ---- S1: 'No juice, no special tea, no seven-day plan.' three things slam onto the worktop and each gets a red X on its word ----
def shot_S1(t, n):
    f = set_worktop(t); t0 = st_("S1")
    chub(f, 870, 1500, 0.95, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="smirk", brow="up", look=(-0.6, 0.3), lean=3, turn=-0.4)
    worktop_front(f, 1330)
    items = (("juice", 170, lambda: scale_el(detox_bottle_el(0.9), 0.5), 1200), ("tea", 400, lambda: scale_el(prod_el("tea"), 1.1), 1220), ("plan", 640, lambda: vstamp_el("7-DAY PLAN", ACC_S, 40), 1250))
    for w_, x, mk, y in items:
        tw = T("i2", w_) - 0.25
        if t >= tw - 0.3:
            comp(f, mk(), x, drop_land(t, tw - 0.3, 700, y, 0.25)[0])
            if t >= tw + 0.05: stamp_x(f, x, y, 90, snap(t, tw + 0.05, 3), RED_X, 18)
    return finish(f, n, look="golden")


# ---- S1b: 'It just does it, for free.' BOARD: the working organs; a price tag swings in: FREE ----
def shot_S1b(t, n):
    f = board_bg(); t0 = st_("S1b")
    body_board(f, t, 1.0)
    tf = T("i2", "free") - 0.1
    if t >= tf:
        slam(f, vstamp_el("FREE", ACC_S, 110), 800, 560, -10, t, tf)
    write_on(f, "already built in", 540, 300, t, t0 + 0.1, 50, ACC_S)
    return finish(f, n, look="fresh")


# ---- S2: 'So that green detox drink everyone's posting after Diwali?' Chubby scrolls a phone full of green-drink posts ----
def feed(f, box, t, t0):
    x0, y0, x1, y1 = box; off = 210 * ((t - t0) * 1.2)
    for j in range(-1, 6):
        yy = int(y0 + 20 + j * 210 - off % 210)
        if yy > y1 - 40 or yy + 190 < y0: continue
        cv2.rectangle(f, (x0 + 18, max(y0, yy)), (x1 - 18, min(y1, yy + 190)), C((236, 244, 222)), -1, cv2.LINE_AA)
        if y0 < yy + 95 < y1: comp(f, scale_el(glass2_el(ACC, 0.85), 0.42), x0 + 90, yy + 95)
        for k in range(2):
            ly = yy + 70 + k * 40
            if y0 < ly < y1: cv2.line(f, (x0 + 170, ly), (x1 - 50 - 60 * k, ly), C(ACC_S), 9, cv2.LINE_AA)


def shot_S2(t, n):
    f = set_worktop(t); t0 = st_("S2")
    chub(f, 260, 1500, 1.02, t=t, la=(24, 14), ra=(70, 60), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2), turn=0.5, hand_r="grip")
    worktop_front(f, 1330)
    box = phone_frame(f, 700, 960, 470, 780); feed(f, box, t, t0)
    cc(f, "#DETOX", 700, 600, t, T("i3", "posting") - 0.2, ACC_S, MILK, 40)
    return finish(f, n, look="golden")


# ---- S2b: 'Your liver is not impressed.' the LIVER, arms crossed, deadpan, slides the green glass away; ink title ----
def shot_S2b(t, n):
    f = ink_set("paper", (255, 255, 255), 540, 980, 560); t0 = st_("S2b"); ti = T("i3", "impressed") - 0.15
    spotlight(f, 480, 1050, 420, 0.35)
    q = ramp(t, ti, 0.45)
    comp(f, scale_el(glass2_el(ACC, 0.85), 1.0), 820 + 160 * q, 1230)
    comp(f, scale_el(liver_el("n", look=(0.6, 0), arms="cross"), 1.75), 450, 1080 + 4 * math.sin(t * 3))
    t3(f, "NOT IMPRESSED", 560, t, ti, 140)
    return finish(f, n, look="fresh")


# ---- S3: 'Back in 2009, a team of scientists asked detox companies one simple question' BOARD: 2009, a clipboard, a question mark ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3")
    write_on(f, "2009", 540, 420, t, t0 + 0.05, 110, ACC_S)
    draw_on(f, [(330, 600), (750, 600), (750, 1150), (330, 1150)], ramp(t, t0 + 0.3, 0.6), BP_INK, 7, seed=31, closed=True)
    draw_on(f, [(470, 590), (470, 560), (610, 560), (610, 590)], ramp(t, t0 + 0.6, 0.3), BP_INK, 7, seed=32)
    for j in range(4): draw_on(f, [(380, 700 + j * 100), (700, 700 + j * 100)], ramp(t, t0 + 0.8 + j * 0.15, 0.3), BP_GRID2, 5, seed=33 + j)
    write_on(f, "Q: which toxins?", 540, 800, t, T("a1", "question") - 0.2, 46, ACC_S)
    write_on(f, "scientists asked", 540, 1430, t, T("a1", "scientists") - 0.1, 50)
    for i, x in enumerate((300, 540, 780)):
        if t >= T("a1", "scientists") - 0.1 + i * 0.1: chub_head_only(f, x, 1270, 0.8, t, mouth=talk(t) if i == 1 else 0, expr="sus", brow="sus", look=(0, -0.6), turn=(i - 1) * 0.3)
    return finish(f, n, look="fresh")


def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b")
    for i, (k, x) in enumerate((("bottle", 230), ("tea", 540), ("pills", 850))):
        comp(f, scale_el(prod_el(k, "wow" if t > T("a1", "exactly") else "n"), 1.5), x, 1080, scale=snap(t, t0 + i * 0.1, 4))
    write_on(f, "which toxins,", 540, 520, t, t0 + 0.05, 72, BP_INK)
    write_on(f, "exactly?", 540, 640, t, T("a1", "exactly") - 0.1, 84, ACC_S)
    return finish(f, n, look="fresh")


# ---- S4: 'They checked fifteen products' BOARD: 15 products pop into a 5 x 3 grid with a count-up; S4b: NO PROOF stamps sweep across, 0 / 15 ----
KINDS = ["bottle", "tea", "patch", "pills", "powder"]
GRID = [(160 + c * 190, 640 + r * 230) for r in range(3) for c in range(5)]


def grid15(f, t, t0, kshow=1.0):
    for i, (x, y) in enumerate(GRID):
        ti = t0 + i * 0.07
        if t >= ti: comp(f, scale_el(prod_el(KINDS[i % 5]), 0.95), x, y, scale=snap(t, ti, 3))


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tf = T("a2", "fifteen") - 0.2
    grid15(f, t, t0 + 0.05)
    v = int(round(count_up(t, tf, 15, 0.7))) if t >= tf else 0
    if t >= tf: comp(f, hand_text_el(str(max(1, v)), 140, ACC_S), 540, 400)
    write_on(f, "products", 540, 1390, t, tf + 0.3, 50)
    return finish(f, n, look="fresh")


def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b")
    grid15(f, t, -9)
    tp = T("a2", "proof") - 0.3
    for i, (x, y) in enumerate(GRID):
        ti = tp + i * 0.05
        if t >= ti: rot_comp(f, vstamp_el("NO PROOF", RED_X, 27), x, y, -8, snap(t, ti, 3), 1.0)
    if t >= tp + 0.8: slam(f, hand_text_el("0 / 15", 150, RED_X), 540, 400, -4, t, tp + 0.8)
    return finish(f, n, look="fresh")


# ---- S5: 'Most couldn't even explain what they meant by detox.' Reporter Chubby holds a mic to a detox bottle that shrugs ----
def shot_S5(t, n):
    f = ink_set("mintp", (255, 255, 255), 540, 980, 600); t0 = st_("S5"); te = T("a3", "tell") - 0.1
    shr = 10 * math.sin(t * 8) if t >= te else 0
    contact(f, 720, 1290, 220, 0.3)
    comp(f, scale_el(detox_bottle_el(0.8, "ouch" if t >= te else "n", look=(-0.6, 0)), 1.1), 720, 1000 + shr)
    if t >= te:
        for sg in (-1, 1): cv2.line(f, (720 + sg * 70, 1000), (int(720 + sg * 140), int(930 - abs(shr))), C(INKC), 9, cv2.LINE_AA)
        write_on(f, "?", 860, 720, t, te, 110, ACC_S)
    chub(f, 260, 1500, 1.0, t=t, la=(24, 14), ra=(96, 70), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2), turn=0.5, hand_r="grip", shirt=(70, 110, 170))
    dress(f, 260, 1500, 1.0, "cousin")
    cv2.line(f, (430, 1180), (520, 1080), C(INKC), 10, cv2.LINE_AA); cv2.circle(f, (530, 1068), 26, C((60, 56, 60)), -1, cv2.LINE_AA)
    icap(f, "'detox' means...", "[ERM?]", t, te, size=130, y=400)
    return finish(f, n, look="fresh")


# ---- S6: 'One said the toxins were dirt and oil,' BOARD: toxins = dirt + oil ; S6b: '...is exactly what soap is for.' a soap bar slams, Chubby smirks ----
def shot_S6(t, n):
    f = board_bg(); t0 = st_("S6")
    write_on(f, "toxins =", 540, 560, t, T("a4", "toxins") - 0.15, 80)
    td, to = T("a4", "dirt") - 0.1, T("a4", "oil") - 0.1
    if t >= td:
        for j in range(9): cv2.circle(f, (250 + (j * 47) % 190, 820 + (j * 61) % 150), 22 + j % 3 * 9, C((120, 96, 70)), -1, cv2.LINE_AA); cv2.circle(f, (250 + (j * 47) % 190, 820 + (j * 61) % 150), 22 + j % 3 * 9, C(INKC), 4, cv2.LINE_AA)
        write_on(f, "dirt", 340, 1040, t, td, 60)
    if t >= to - 0.2: write_on(f, "+", 540, 900, t, to - 0.2, 90, ACC_S)
    if t >= to:
        comp(f, scale_el(junk_el(None), 1.15), 790, 890, scale=snap(t, to, 4))
        write_on(f, "oil", 760, 1040, t, to, 60)
    return finish(f, n, look="fresh")


def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); ts = T("a4", "soap") - 0.1
    write_on(f, "dirt + oil", 540, 560, t, -9, 70)
    draw_arrow_on(f, (540, 640), (540, 760), ramp(t, t0, 0.3), ACC_S, 7)
    slam(f, soap_bar_el(), 540, 950, -6, t, ts, 1.2)
    peek(f, t, 840, 1300, 0.6, "smirk", (-0.5, -0.4))
    if t >= ts + 0.2: write_on(f, "that's just soap", 540, 1180, t, ts + 0.2, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S7: 'So who's really doing the cleaning?' PART 1: Chubby with a broom looks left-right, then at the viewer ----
def shot_S7(t, n):
    f = set_worktop(t); t0 = st_("S7"); e = eye_lead(t, t0 + 0.3, -1.0, 1.0)
    chub(f, 540, 1500, 1.08, t=t, la=(30, 16), ra=(120, 100), hold=scale_el(broom_el(), 0.75), hold_off=(0, 40), mouth=talk(t), expr="sus", brow="sus", look=e["look"], turn=e["turn"], blink=e["blink"])
    worktop_front(f, 1330)
    t3(f, "WHO CLEANS?", 560, t, T("b0", "cleaning") - 0.2, 150)
    chapter_card(f, t, t0 + 0.05, 1, "THE REAL CLEANERS", 1420, 1.8, ACC_L)
    return finish(f, n, look="golden")


# ---- S8: 'Two organs you've already got, and the first one is your liver.' BOARD: the body draws itself, the liver + kidneys light up with labels ----
def shot_S8(t, n):
    f = board_bg(); t0 = st_("S8"); tl = T("b1", "liver") - 0.15
    k = ramp(t, t0, 0.9)
    figure(f, k, 540, 560)
    if k > 0.7:
        for i, (x, y) in enumerate(KID_B): comp(f, scale_el(kidney_el("n", flip=i == 1), 0.72), x, y, op=0.55 if t >= tl else 1.0)
        if t >= tl: glow(f, LIV_B[0], LIV_B[1], 260, (255, 210, 180), 0.35)
        comp(f, scale_el(liver_el("happy" if t >= tl else "n"), 0.95), LIV_B[0], LIV_B[1], scale=snap(t, tl, 4) if t >= tl else 1.0)
    if t >= tl:
        label_at(f, "LIVER", 210, 820, t, tl, LIV_B[0] - 130, LIV_B[1] - 60, INKC, MILK, 44)
    label_at(f, "2 ORGANS", 540, 330, t, T("b1", "organs") - 0.1, None, None, ACC_S, MILK, 40)
    return finish(f, n, look="fresh")


# ---- S8b: 'It works like a sorting factory.' MORPH into the NEW PLACE: inside the liver factory, the liver (hard hat) runs a conveyor ----
def factory_scene(t, lit=0, liver_mood="happy", belt=True, dim=0.0):
    f = set_factory(t, dim=dim)
    comp(f, machine_el(lit), 790, 960)
    if belt: conveyor(f, t, 1230)
    comp(f, scale_el(liver_el(liver_mood, look=(0.6, 0), arms="work", hat=True), 1.0), 300, 1000 + 5 * math.sin(t * 6))
    return f


def shot_S8b(t, n):
    t0 = st_("S8b"); f = factory_scene(t)
    for j in range(3):
        x = (t - t0) * 160 + j * 300 - 200
        if -100 < x < 640: comp(f, scale_el(junk_el("n"), 0.5), x, 1170)
    t3(f, "SORTING FACTORY", 540, t, T("b1", "sorting") - 0.15, 120)
    return finish(f, n, look="warm")


# ---- S9: 'A lot of the stuff your body wants gone dissolves in fat, not in water,' BOARD: oil beaker swallows the blob, water beaker rejects it ----
def shot_S9(t, n):
    f = board_bg(); t0 = st_("S9"); tf = T("b2", "fat") - 0.15; tw = T("b2", "water") - 0.15
    comp(f, scale_el(beaker_el("fat"), 1.55), 290, 1080); comp(f, scale_el(beaker_el("water"), 1.55), 790, 1080)
    comp(f, scale_el(junk_el("happy" if t < tf else "love"), 0.85), 290, (700 if t < tf else drop_land(t, tf, 700, 1080, 0.3)[0]), op=1 - ramp(t, tf + 0.35, 0.5) * 0.85)
    if t >= tw:
        y = drop_land(t, tw, 700, 860, 0.3)[0]
        bx = 790 + 150 * ramp(t, tw + 0.3, 0.5)
        comp(f, scale_el(junk_el("ouch"), 0.85), bx, y if t < tw + 0.3 else 860 - 80 * math.sin(math.pi * ramp(t, tw + 0.3, 0.5)))
        stamp_x(f, 790, 1120, 90, snap(t, tw + 0.25, 3), RED_X, 16)
    write_on(f, "dissolves in fat", 540, 470, t, T("b2", "dissolves") - 0.1, 62)
    if t >= tw: write_on(f, "not in water", 540, 580, t, tw, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S9b: '...and you can't pee out fat.' BOARD: the kidney's filter; the yellow blob bounces off the sieve; Chubby's queasy peek ----
def shot_S9b(t, n):
    f = board_bg(); t0 = st_("S9b"); tp = T("b2", "pee") - 0.2
    comp(f, scale_el(kidney_el("n"), 1.45), 330, 960)
    cx, cy = 720, 980
    for r in range(4):
        for c in range(5): draw_ell_on(f, cx - 120 + c * 60, cy - 90 + r * 60, 14, 14, 1.0, BP_INK, 4, seed=40 + r * 5 + c)
    draw_on(f, [(cx - 170, cy - 140), (cx + 170, cy - 140), (cx + 170, cy + 140), (cx - 170, cy + 140)], 1.0, BP_INK, 6, seed=60, closed=True)
    q = clamp((t - t0) / 0.8)
    y = 560 + (cy - 230 - 560) * eio(clamp(q * 1.4)) - 120 * math.sin(math.pi * clamp((q - 0.7) / 0.3)) * (q > 0.7)
    comp(f, scale_el(junk_el("ouch" if q > 0.7 else "n"), 0.8), cx + 40 * (q > 0.7) * (q - 0.7) * 3, y)
    if t >= tp: write_on(f, "can't pee out fat", 540, 1320, t, tp, 60, ACC_S)
    peek(f, t, 200, 560, 0.5, "gross", (0.5, 0.3), "sad")
    return finish(f, n, look="fresh")


# ---- S10: 'So the liver changes it, one step at a time, into something that dissolves in water.' the factory: blob in, step 1, step 2, a blue box out ----
def shot_S10(t, n):
    t0 = st_("S10"); t1, t2 = T("b3", "one") - 0.1, T("b3", "time") - 0.1
    lit = 2 if t >= t2 else (1 if t >= t1 else 0)
    f = factory_scene(t, lit)
    xb = 300 + 560 * ramp(t, t0, t1 - t0 + 0.2)
    if t < t2 + 0.1: comp(f, scale_el(junk_el("n"), 0.55), min(xb, 640), 1170 if xb < 640 else 1170 - 300 * ramp(t, t1, 0.3), op=1 - ramp(t, t2 - 0.2, 0.3))
    if t >= t2:
        ox = 960 + 40 * ramp(t, t2, 0.4)
        comp(f, scale_el(junk_el("happy", packed=True), 0.62), ox, drop_land(t, t2, 1050, 1150, 0.3)[0])
    cc(f, "STEP 1", 700, 620, t, t1, INKC, MILK, 36); cc(f, "STEP 2", 880, 620, t, t2, INKC, MILK, 36)
    icap(f, "into something that dissolves in", "[WATER]", t, T("b3", "water") - 0.15, size=130, y=400, dark=False)
    return finish(f, n, look="warm")


# ---- S10b: 'Same junk, new packaging, and now it can actually leave.' the packed junk waves and walks out the EXIT door ----
def shot_S10b(t, n):
    t0 = st_("S10b"); tl = T("b4", "leave") - 0.2
    f = set_factory(t)
    comp(f, scale_el(door_el(ramp(t, tl - 0.4, 0.4)), 0.7), 860, 1000)
    cc(f, "EXIT: KIDNEYS", 860, 640, t, t0 + 0.1, INKC, MILK, 32)
    conveyor(f, t, 1230)
    x = 420 + 420 * ramp(t, tl, 0.6)
    comp(f, scale_el(junk_el("happy", packed=True), 0.9 * (1 - 0.4 * ramp(t, tl + 0.3, 0.3))), x, 1110 - 20 * abs(math.sin(t * 9)) * (t > tl))
    comp(f, scale_el(liver_el("happy", arms="up", hat=True), 0.75), 220, 1050)
    icap(f, "same junk,", "[NEW PACKAGING]", t, t0 + 0.05, size=110, y=400)
    return finish(f, n, look="warm")


# ---- S11: 'And that's where your kidneys take over.' PART 2: two kidney workers snap in on the worktop ----
def shot_S11(t, n):
    f = set_worktop(t); t0 = st_("S11"); tk = T("c0", "kidneys") - 0.2
    worktop_front(f, 1330)
    for i, x in enumerate((360, 720)):
        if t >= tk + i * 0.12: comp(f, scale_el(kidney_el("happy", flip=i == 1, hat=True), 1.15), x, 1150 + 6 * math.sin(t * 6 + i), scale=snap(t, tk + i * 0.12, 4))
    t3(f, "KIDNEYS", 560, t, tk, 190)
    chapter_card(f, t, t0 + 0.05, 2, "THE FILTERS", 1440, 1.8, ACC_L)
    return finish(f, n, look="golden")


# ---- S12: 'Each one is about the size of your fist,' Chubby holds his fist up next to a kidney: same size ----
def shot_S12(t, n):
    f = set_worktop(t); t0 = st_("S12"); tf = T("c1", "fist") - 0.2
    chub(f, 250, 1500, 1.0, t=t, **nolean(POSE["point"]), hand_r="point", mouth=talk(t), expr="wow" if t >= tf else "happy", brow="up", look=(1, -0.3), turn=0.5)
    worktop_front(f, 1330)
    cv2.circle(f, (700, 950), 270, C((252, 248, 238)), -1, cv2.LINE_AA); cv2.circle(f, (700, 950), 270, C(INKC), 8, cv2.LINE_AA)
    comp(f, scale_el(kidney_el("happy", flip=True), 0.8), 590, 950, scale=pin(t, t0 + 0.1))
    if t >= tf:
        grip_hand(f, 830, 950, 3.6)
        write_on(f, "=", 715, 950, t, tf, 60, ACC_S)
        cc(f, "ABOUT THE SIZE OF A FIST", 540, 1450, t, tf, ACC_S, MILK, 36)
    return finish(f, n, look="golden")


# ---- S12b: '...with around a million tiny filters packed inside.' an inset zooms into the kidney: a field of tiny filter funnels + a count-up ----
def tiny_filters(f, cx, cy, r, t):
    for j in range(-6, 7):
        for i in range(-6, 7):
            x, y = cx + i * 34 + (j % 2) * 17, cy + j * 30
            if (x - cx) ** 2 + (y - cy) ** 2 < (r - 20) ** 2:
                cv2.circle(f, (int(x), int(y)), 11, C((246, 210, 206)), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 11, C(KID_S), 3, cv2.LINE_AA)
                if (i + j + int(t * 6)) % 7 == 0: cv2.circle(f, (int(x), int(y + 14)), 4, C(WATER_B), -1, cv2.LINE_AA)


def shot_S12b(t, n):
    f = board_bg(); t0 = st_("S12b"); tm = T("c1", "million") - 0.3
    comp(f, scale_el(kidney_el("n"), 0.8), 260, 760)
    draw_arrow_on(f, (330, 760), (420, 860), ramp(t, t0, 0.3), BP_INK, 6)
    cv2.circle(f, (640, 1000), 300, C((252, 236, 232)), -1, cv2.LINE_AA)
    tiny_filters(f, 640, 1000, 300, t)
    cv2.circle(f, (640, 1000), 300, C(BP_INK), 10, cv2.LINE_AA)
    if t >= tm:
        v = count_up(t, tm, 1000000, 0.8)
        comp(f, hand_text_el(f"~{int(v):,}", 110, ACC_S), 540, 470)
        write_on(f, "tiny filters, in EACH", 540, 1400, t, tm + 0.3, 50)
    return finish(f, n, look="fresh")


# ---- S13: 'Every day, they filter more than a hundred and forty litres.' BOARD: a big tank fills while the counter climbs ----
def shot_S13(t, n):
    f = board_bg(); t0 = st_("S13"); tc = T("c2", "hundred") - 0.3
    x0, y0, x1, y1 = 340, 760, 740, 1200
    k = ramp(t, t0 + 0.2, (T("c2", "litres") if any(w["w"].lower().startswith("litre") for w in WORDS if w["line"] == "c2") else tc + 0.8) - t0)
    lv = y1 - (y1 - y0 - 30) * k
    cv2.rectangle(f, (x0, int(lv)), (x1, y1), C((200, 226, 248)), -1, cv2.LINE_AA)
    draw_on(f, [(x0, y0 - 40), (x0, y1), (x1, y1), (x1, y0 - 40)], ramp(t, t0, 0.4), BP_INK, 8, seed=70)
    for j in range(5): draw_on(f, [(x0 + 4, y1 - j * 90), (x0 + 40, y1 - j * 90)], 1.0, BP_INK, 4, seed=71 + j)
    if t >= tc: comp(f, hand_text_el(f"{int(count_up(t, tc, 140, 0.8))}+ L", 140, ACC_S), 540, 520)
    write_on(f, "every day", 540, 1320, t, t0 + 0.1, 60)
    src(f, SRC_KID, t, t0 + 0.4, 1466)
    return finish(f, n, look="fresh")


# ---- S13b: 'That's about seven big water cans.' MORPH: the tank becomes a row of seven real 20-litre cans on the kitchen floor; Chubby's double take ----
def shot_S13b(t, n):
    f = set_worktop(t); t0 = st_("S13b"); ts = T("c2", "seven") - 0.25
    look, lean, ex, br = double_take(t, ts)
    chub(f, 900, 1500, 0.85, t=t, **nolean(POSE["shock"]) if t >= ts + 0.3 else dict(la=(24, 14), ra=(24, 14)), mouth="jaw" if ts + 0.3 < t < ts + 1.0 else talk(t), expr=ex, brow=br, look=look, lean=lean, turn=-0.4)
    for i in range(7):
        ti = t0 + 0.05 + i * 0.09
        if t >= ti: comp(f, scale_el(jerrycan_el(), 0.56), 80 + i * 98, 1300, scale=snap(t, ti, 3))
    cc(f, "7 x 20 L", 380, 1110, t, ts, ACC_S, MILK, 56)
    return finish(f, n, look="golden")


# ---- S14: 'And only a litre or two of it ends up as pee.' BOARD: a funnel, 140 L in at the top, a little jug out at the bottom ----
def shot_S14(t, n):
    f = board_bg(); t0 = st_("S14"); tj = T("c3", "litre") - 0.2 if any(w["w"].lower().startswith("litre") for w in WORDS if w["line"] == "c3") else t0 + 0.6
    write_on(f, "140+ L in", 540, 430, t, t0 + 0.05, 60)
    draw_on(f, [(240, 540), (840, 540), (600, 900), (600, 1040), (480, 1040), (480, 900), (240, 540)], ramp(t, t0 + 0.1, 0.6), BP_INK, 8, seed=80)
    for j in range(6):
        q = (t * 1.2 + j / 6) % 1.0; cv2.circle(f, (int(300 + j * 90 + (540 - 300 - j * 90) * q), int(580 + 420 * q)), 10, C(WATER_B), -1, cv2.LINE_AA)
    if t >= tj:
        comp(f, scale_el(jug_el(0.45), 0.9), 540, 1210, scale=snap(t, tj, 4))
        write_on(f, "1 to 2 L out", 540, 1390, t, tj + 0.1, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S14b: 'The rest goes straight back into you.' BOARD: the body again; a big loop arrow sends the clean water back into the blood ----
def shot_S14b(t, n):
    f = board_bg(); t0 = st_("S14b")
    body_board(f, t, 1.0, work=False)
    comp(f, scale_el(heart_el(), 1.4), 620, 860, scale=pin(t, t0 + 0.1))
    for P in ([(KID_B[0][0], KID_B[0][1] - 90), (330, 980), (440, 870), (560, 850)], [(KID_B[1][0], KID_B[1][1] - 90), (760, 1000), (720, 900), (680, 870)]):
        draw_arrow_on(f, P[0], P[-1], ramp(t, t0 + 0.2, 0.5), WATER_BS, 9, bend=0.3)
        for j in range(3):
            q = ((t - t0) * 0.7 + j / 3) % 1.0
            if t > t0 + 0.7: x, y = path_at(P, q); cv2.circle(f, (int(x), int(y)), 12, C(WATER_B), -1, cv2.LINE_AA)
    write_on(f, "back into your blood", 540, 330, t, T("c3", "back") - 0.2, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S15: 'So the detox is already running, all day, every day, and it doesn't need a subscription.' night room: the workers keep going under a lamp, the clock spins ----
def shot_S15(t, n):
    f = set_droom(t, dim=0.25); t0 = st_("S15"); ts = T("c4", "subscription") - 0.3
    comp(f, scale_el(clock_ink_el(90, 15), 1.0), 820, 560); clock_hands(f, 820, 560, 8 + 30 * (t - t0), 90, 1.0)
    table_front(f, 1330)
    comp(f, scale_el(liver_el("happy", arms="work", hat=True), 0.8), 380, 1210 + 5 * math.sin(t * 7))
    for i, x in enumerate((690, 860)): comp(f, scale_el(kidney_el("happy", flip=i == 1, hat=True), 0.62), x, 1220 - 5 * math.sin(t * 7 + i))
    cc(f, "24/7", 540, 400, t, T("c4", "running") - 0.2, ACC_S, MILK, 60)
    if t >= ts: slam(f, vstamp_el("NO SUBSCRIPTION", INKC, 60), 540, 780, -5, t, ts)
    return finish(f, n, look="night")


# ---- S16: 'Okay, but what about a three-day juice cleanse?' PART 3: the fridge door swings open on DAY 1 / 2 / 3 bottles; Chubby squints ----
def shot_S16(t, n):
    f = set_worktop(t); t0 = st_("S16"); tj = T("d0", "juice") - 0.2
    comp(f, scale_el(fridge_ink_el(True, eggs=False, milk=False), 1.0), 700, 990)
    for i, y in enumerate((800, 1010, 1220)):
        if t >= t0 + 0.2 + i * 0.12:
            comp(f, scale_el(detox_bottle_el(0.9), 0.3), 700, y - 20, scale=snap(t, t0 + 0.2 + i * 0.12, 3))
            cc(f, f"DAY {i + 1}", 820, y, t, t0 + 0.3 + i * 0.12, ACC_S, MILK, 26)
    chub(f, 240, 1500, 1.0, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="sus", look=(1, -0.2), turn=0.5)
    t3(f, "JUICE CLEANSE?", 470, t, tj, 130)
    chapter_card(f, t, t0 + 0.05, 3, "THE CLEANSE", 1440, 1.8, ACC_L)
    return finish(f, n, look="golden")


# ---- S17: 'When researchers went through the studies, they found no good proof...' BOARD: the stack of studies under a magnifier, NO GOOD PROOF ----
def shot_S17(t, n):
    f = board_bg(); t0 = st_("S17"); tp = T("d1", "proof") - 0.2
    comp(f, scale_el(papers_el(6), 2.0), 540, 980, scale=snap(t, t0 + 0.05, 4))
    q = ramp(t, t0 + 0.3, 1.2); comp(f, scale_el(magnifier_ink_el(), 1.0), 380 + 300 * q, 900 + 60 * math.sin(q * 6))
    write_on(f, "the studies", 540, 560, t, T("d1", "studies") - 0.15, 62)
    if t >= tp: slam(f, vstamp_el("NO GOOD PROOF", RED_X, 80), 540, 1260, -6, t, tp)
    src(f, SRC_NCCIH, t, t0 + 0.4, 1466)
    return finish(f, n, look="fresh")


# ---- S18: 'You might lose a little weight at first, but it tends to come back...' BOARD: the weight line dips during the cleanse and climbs back ----
def shot_S18(t, n):
    f = board_bg(); t0 = st_("S18"); tb = T("d2", "back") - 0.3
    draw_on(f, [(140, 640), (140, 1200), (960, 1200)], ramp(t, t0, 0.3), BP_INK, 6, seed=101)
    x0c, x1c = 300, 520
    hatch_on(f, [(x0c, 660), (x1c, 660), (x1c, 1190), (x0c, 1190)], ramp(t, t0 + 0.2, 0.4), ACC, 18, 45, 4, 0.5)
    write_on(f, "cleanse", 410, 1260, t, t0 + 0.3, 44, ACC_S)
    def wv(u): return 800 + 140 * math.exp(-((u - 0.42) / 0.12) ** 2) * (1 if u < 0.42 else 0) + (140 * math.exp(-((u - 0.42) / 0.2) ** 2) if u >= 0.42 else 0) * 1.0
    P = [(140 + 820 * u, 820 + 150 * math.sin(math.pi * clamp((u - 0.18) / 0.45)) * (0.18 < u < 0.63)) for u in np.linspace(0, 1, 60)]
    kk = 0.6 * ramp(t, t0 + 0.2, T("d2", "first") - t0) + 0.4 * ramp(t, tb, 0.8)
    draw_on(f, P, kk, BP_INK, 9, seed=102, wob=0.5)
    write_on(f, "weight", 260, 600, t, t0 + 0.1, 46)
    if t >= tb: write_on(f, "comes back", 780, 700, t, tb + 0.3, 56, RED_X)
    return finish(f, n, look="fresh")


# ---- S19: 'And some cleanses aren't harmless. Laxatives can leave you dehydrated.' CAUTION: the light drops, a pill, a water drop shrinks + wilts ----
def shot_S19(t, n):
    t0 = st_("S19"); td = T("d3", "dehydrated") - 0.3; k = ramp(t, td, 0.8)
    f = set_worktop(t); f *= (1 - 0.25 * ramp(t, t0, 0.4))
    chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["sick"]), mouth=talk(t), expr="gross" if t >= td else "sus", brow="sad", look=(1, 0), turn=0.5)
    worktop_front(f, 1330)
    comp(f, scale_el(pill_el(), 1.2), 700, 1270, scale=pin(t, T("d3", "Laxatives") - 0.1))
    comp(f, scale_el(drop_el("sad" if t >= td else "n"), 1.4 * (1 - 0.55 * k)), 760, 980 + 60 * k)
    mood(f, (255, 190, 90), 0.25 * ramp(t, t0, 0.4))
    if t >= td: cc(f, "DEHYDRATED", 760, 760, t, td, INKC, MILK, 44)
    return finish(f, n, look="warm")


# ---- S20: 'And juice that isn't pasteurized can carry germs that make you sick.' BOARD: a magnifier over a juice bottle finds germs ----
def shot_S20(t, n):
    f = board_bg(); t0 = st_("S20"); tg = T("d4", "germs") - 0.2
    comp(f, scale_el(detox_bottle_el(0.85), 0.9), 400, 1000)
    write_on(f, "not pasteurized", 540, 480, t, T("d4", "pasteurized") - 0.3, 60)
    cv2.circle(f, (680, 960), 200, C((252, 250, 236)), -1, cv2.LINE_AA)
    if t >= tg:
        for j in range(5):
            a = j * 1.25 + t * 1.5; comp(f, scale_el(germ_el("n" if j % 2 else "sly", ph=j), 0.55), 680 + 90 * math.cos(a), 960 + 80 * math.sin(a), scale=snap(t, tg + j * 0.06, 3))
    cv2.circle(f, (680, 960), 200, C(BP_INK), 12, cv2.LINE_AA); cv2.line(f, (820, 1100), (940, 1240), C(BP_INK), 26, cv2.LINE_AA)
    src(f, "Source: NCCIH (NIH) · US FDA", t, t0 + 0.4, 1466)
    return finish(f, n, look="fresh")


# ---- S21: 'So after Diwali, what actually helps your liver and kidneys?' PART 4: the organs wait on the worktop, Chubby thinks ----
def shot_S21(t, n):
    f = set_worktop(t); t0 = st_("S21"); th = T("e0", "helps") - 0.2
    chub(f, 260, 1500, 1.02, t=t, **nolean(POSE["think"]), mouth=talk(t), expr="sus", brow="up", look=(1, -0.3), turn=0.5)
    worktop_front(f, 1330)
    comp(f, scale_el(liver_el("wow" if t >= th else "n", look=(-0.6, 0)), 0.8), 640, 1200)
    for i, x in enumerate((860, 970)): comp(f, scale_el(kidney_el("wow" if t >= th else "n", flip=i == 1), 0.42), x, 1220)
    t3(f, "WHAT HELPS?", 560, t, th, 160)
    chapter_card(f, t, t0 + 0.05, 4, "WHAT HELPS", 1440, 1.8, ACC_L)
    return finish(f, n, look="golden")


# ---- S22: 'The boring stuff.' a BORING stamp; Chubby deadpan ; S22b: 'A proper night's sleep,' head on the pillow ; S22c: '...normal meals with vegetables, fruit and whole grains.' ----
def shot_S22(t, n):
    f = set_worktop(t); t0 = st_("S22")
    chub(f, 540, 1500, 1.05, t=t, **POSE["shrug"], mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2))
    worktop_front(f, 1330)
    slam(f, vstamp_el("BORING (AND IT WORKS)", INKC, 64), 540, 560, -5, t, T("e1", "boring") - 0.1)
    return finish(f, n, look="golden")


def shot_S22b(t, n):
    f = set_droom(t, dim=0.55); t0 = st_("S22b")
    moon_icon(f, 270, 700, 70, (40, 30, 80))
    comp(f, pillow_el(), 560, 1080)
    chub_head_only(f, 520, 1020, 1.25, t, mouth=0, expr="sleepy", brow="sad", blink=True)
    comp(f, blanket_el(900), 560, 1330)
    zzs(f, 700, 860, t, 3, WHITE, 1.1)
    icap(f, "a proper night's", "[SLEEP]", t, T("e1", "sleep") - 0.2, size=150, y=420, dark=True)
    return finish(f, n, look="night")


def shot_S22c(t, n):
    f = set_worktop(t); t0 = st_("S22c")
    chub(f, 540, 1500, 1.05, t=t, la=(60, 100), ra=(130, -120 + 10 * math.sin(t * 9)), mouth=2 if math.sin(t * 9) > 0 else 0, expr="happy", brow="up", look=(0, 0.6))
    worktop_front(f, 1330)
    comp(f, scale_el(thali_el("small"), 0.75), 540, 1372, scale=pin(t, t0 + 0.05))
    for i, (w_, lab, x) in enumerate((("vegetables", "VEG", 220), ("fruit", "FRUIT", 540), ("whole", "WHOLE GRAINS", 860))):
        cc(f, lab, x, 400 + (i % 2) * 70, t, T("e1", w_) - 0.15, ACC_S if i == 1 else INKC, MILK, 40)
    comp(f, scale_el(apple_el(), 0.5), 860, 1240, scale=pin(t, T("e1", "fruit") - 0.1))
    return finish(f, n, look="golden")


# ---- S23: 'And go easy on the alcohol, because your liver has to deal with every single drop.' BOARD: a tipping glass, the liver catches EVERY drop in a bucket ----
def shot_S23(t, n):
    f = board_bg(); t0 = st_("S23"); te = T("e2", "every") - 0.2
    rot_comp(f, glass2_el((236, 176, 80), 0.6), 300, 640, -40, 1.0, 1.0, 0.0)
    comp(f, scale_el(liver_el("ouch" if t >= te else "n", look=(-0.5, -0.6), arms="up"), 0.9), 600, 1150)
    for j in range(6):
        q = ((t - t0) * 1.1 + j / 6) % 1.0
        cv2.circle(f, (int(350 + 220 * q), int(700 + 360 * q * q)), 11, C((236, 176, 80)), -1, cv2.LINE_AA); cv2.circle(f, (int(350 + 220 * q), int(700 + 360 * q * q)), 11, C(BP_INK), 3, cv2.LINE_AA)
    write_on(f, "go easy", 540, 380, t, T("e2", "easy") - 0.2, 70, ACC_S)
    if t >= te: write_on(f, "every single drop", 540, 1400, t, te, 56)
    return finish(f, n, look="fresh")


# ---- S24: 'No detox kit needed.' BOARD recap: LIVER sorts + KIDNEYS filter + sleep + food = no kit ; S24b: '...the night shift, and the day shift.' moon -> sun ----
def shot_S24(t, n):
    f = board_bg(); t0 = st_("S24")
    comp(f, chip("SAVE THIS", INKC, ACC_L, 34), 540, 330, op=clamp((t - t0) / 0.2))
    rows = ((lambda: scale_el(liver_el("happy"), 0.6), "liver: sorts it"), (lambda: scale_el(kidney_el("happy"), 0.6), "kidneys: flush it"), (lambda: scale_el(pillow_el(), 0.45), "sleep + real meals"))
    for i, (mk, lab) in enumerate(rows):
        ti = t0 + 0.1 + i * 0.25; y = 560 + i * 220
        if t >= ti:
            comp(f, mk(), 260, y, scale=snap(t, ti, 4)); write_on(f, lab, 640, y, t, ti + 0.05, 48)
    if t >= T("f1", "needed") - 0.2:
        comp(f, scale_el(detox_bottle_el(0.9), 0.5), 540, 1260); stamp_x(f, 540, 1260, 130, snap(t, T("f1", "needed") - 0.1, 3), RED_X, 20)
    return finish(f, n, look="fresh")


def shot_S24b(t, n):
    t0 = st_("S24b"); td = T("f1", "day", 0) - 0.2 if True else 0
    day = t >= td
    f = set_worktop(t) if day else set_droom(t, dim=0.4)
    if day: sun_x = 220; comp(f, scale_el(sun_ink_el("happy"), 0.8), 220, 560, scale=snap(t, td, 4))
    else: moon_icon(f, 220, 560, 70, (40, 30, 80))
    (worktop_front if day else table_front)(f, 1330)
    comp(f, scale_el(liver_el("happy", arms="work", hat=True), 0.85), 420, 1210 + 5 * math.sin(t * 8))
    for i, x in enumerate((720, 890)): comp(f, scale_el(kidney_el("happy", flip=i == 1, hat=True), 0.6), x, 1220 - 5 * math.sin(t * 8 + i))
    cc(f, "DAY SHIFT" if day else "NIGHT SHIFT", 540, 420, t, t0 if not day else td, ACC_S if day else INKC, MILK, 50)
    return finish(f, n, look="golden" if day else "night")


# ---- S25: 'Send this to whoever just sent you a detox juice recipe.' Chubby + phone, then the logo ----
def shot_S25(t, n):
    t0 = st_("S25"); f = set_worktop(t); vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.25
        comp(f, scale_el(phone2_el("my liver: already on it", "detox juice? no thanks", pr), 0.82), 760, 960, scale=pin(t, t0))
        if pr and t < T("f2", "Send") + 0.7:
            rr = (t - T("f2", "Send") - 0.25) / 0.45; cv2.circle(f, (760, 1230), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 290, 1500, 1.05, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), hand_r="point", turn=0.5, expr="smirk", brow="up", look=(1, -0.1))
        worktop_front(f, 1400)
        ui_word(f, "send this to whoever sent you", "A [DETOX] RECIPE", 440, t, T("f2", "Send") - 0.05, col=INKC, acc=ACC_S, size=90)
    else:
        f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32); k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 760, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.62, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TD, 0.45, 18), (T("i2", "plan") - 0.2, 0.25, 8), (T("i2", "free") - 0.1, 0.25, 8), (T("i3", "impressed") - 0.15, 0.35, 12),
           (T("a1", "exactly") - 0.1, 0.25, 8), (T("a2", "proof") + 0.5, 0.4, 14), (T("a4", "soap") - 0.1, 0.4, 14),
           (T("b0", "cleaning") - 0.2, 0.3, 10), (T("b1", "liver") - 0.15, 0.25, 8), (T("b2", "water") - 0.15, 0.3, 10), (T("b3", "time") - 0.1, 0.3, 10),
           (T("b4", "leave") - 0.2, 0.25, 8), (T("c0", "kidneys") - 0.2, 0.35, 12), (T("c1", "million") - 0.3, 0.3, 10), (T("c2", "seven") - 0.25, 0.4, 14),
           (T("c4", "subscription") - 0.3, 0.35, 12), (T("d0", "juice") - 0.2, 0.3, 10), (T("d1", "proof") - 0.2, 0.4, 14),
           (T("e0", "helps") - 0.2, 0.3, 10), (T("e1", "boring") - 0.1, 0.35, 12), (T("f1", "needed") - 0.1, 0.3, 10), (T("f2", "Send") + 0.25, 0.2, 8)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


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
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
