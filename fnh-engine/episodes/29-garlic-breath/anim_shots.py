# ================= shots: FreshNestHub 29 — "Why does garlic breath last so long?" (Chubby INK, ep 12 of the ink look) ===
# COLOUR SCRIPT: GARLIC MAUVE (ACC) = the SMELL only (stink clouds, the sulfur gases, AMS the sneaky gas, smelly words). Everything real keeps natural ink colours
# (garlic cream, lungs coral, blood red, apple red, lettuce + mint greens, milk white). Story = lit places (office = NEW PLACE, bathroom, worktop, dusk);
# every explanation = the white BOARD. Craft skill: KINETIC TYPOGRAPHY that reacts (anim_fx.kin_word: stink / sneak / blow / drop / shake / breathe).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "lungs") - 0.15, "morph"),
    ("S1", T("i2", "Thats") - 0.1, "whip"), ("S1b", T("i2", "and") - 0.1, "punch"),
    ("S2", T("a0", "Start") - 0.15, "flash"), ("S2b", T("a0", "Sitting") - 0.1, "punch"),
    ("S3", T("a1", "The") - 0.1, "whip"),
    ("S4", T("a2", "Crushing") - 0.1, "erase"), ("S4b", T("a2", "meet") - 0.15, "punch"),
    ("S5", T("a3", "In") - 0.1, "erase"), ("S5b", T("a3", "allicin", 1) - 0.1, "punch"),
    ("S6", T("b0", "But") - 0.15, "flash"),
    ("S7", T("b1", "Place") - 0.1, "erase"), ("S7b", T("b1", "Tiny") - 0.1, "punch"),
    ("S8", T("b2", "Brushing") - 0.1, "whip"),
    ("S9", T("b3", "Place") - 0.1, "erase"), ("S9b", T("b3", "called") - 0.1, "punch"),
    ("S10", T("b4", "Your") - 0.1, "erase"), ("S10b", T("b4", "so") - 0.1, "punch"),
    ("S11", T("b5", "It") - 0.1, "erase"), ("S11b", T("b5", "every") - 0.15, "morph"),
    ("S12", T("b6", "And") - 0.1, "whip"),
    ("S13", T("b7", "So") - 0.12, "erase"),
    ("S14", T("c0", "So") - 0.12, "flash"),
    ("S15", T("c1", "An") - 0.1, "erase"), ("S15b", T("c1", "Some") - 0.1, "punch"),
    ("S16", T("c2", "Thats") - 0.1, "whip"),
    ("S17", T("d0", "So") - 0.15, "flash"),
    ("S18", T("d1", "Her") - 0.1, "erase"), ("S18b", T("d1", "and") - 0.1, "punch"),
    ("S19", T("d2", "Raw") - 0.1, "erase"),
    ("S20", T("d3", "Fresh") - 0.1, "punch"),
    ("S21", T("d4", "Cooked") - 0.1, "erase"), ("S21b", T("d4", "because") - 0.1, "punch"),
    ("S22", T("d5", "And") - 0.1, "whip"), ("S22b", T("d5", "and", 1) - 0.1, "punch"),
    ("S23", T("e0", "So") - 0.15, "erase"), ("S23b", T("e0", "grab") - 0.1, "punch"),
    ("S24", T("e1", "And") - 0.1, "erase"),
    ("S25", T("f1", "Garlics") - 0.12, "flash"), ("S25b", T("f1", "Maybe") - 0.1, "whip"),
    ("S26", T("f2", "Send") - 0.15, "whip"),
]

SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
_write_on0 = write_on
# MORPH CUTS: (x, y, size) of the matching object in the outgoing shot -> in the incoming shot
MORPH = {"S0b": ((330, 1000, 260), (540, 1020, 440)),     # Chubby's chest in the office -> the board lungs
         "S11b": ((540, 1020, 380), (470, 1180, 260))}    # the board lungs -> Chubby's chest at the worktop


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


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    """kinetic word in hand lettering with an ink stroke (anim_fx.kin_word)."""
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def puff(f, x, y, t, t0, dur=1.2, s=0.6, dx=160, dy=-120, mood="n", seed=296):
    """a stink cloud blown out of a mouth: grows + drifts + fades."""
    if t < t0 or t > t0 + dur: return
    q = (t - t0) / dur
    rot_comp(f, gas_el2(mood, seed=seed), x + dx * eo(q), y + dy * eo(q) + 6 * math.sin(t * 6), 6 * math.sin(t * 3), s * (0.4 + 0.8 * eo(clamp(q * 2))), clamp((1 - q) * 3), 0.0)


def wisp(f, x, y, t, n=3, h=150, col=None, op=1.0):
    """little smell wisps rising (mauve)."""
    for i in range(n):
        ph = (t * 0.8 + i / n) % 1.0; bx = x + (i - (n - 1) / 2) * 40; by = y - h * ph
        P = np.array([(bx + 12 * math.sin(k * 0.9 + t * 4 + i * 2), by - k * 9) for k in range(8)], np.int32)
        cv2.polylines(f, [P], False, C(col or ACC), 6, cv2.LINE_AA)


def figure(f, k, cx=540, hy=560, col=BP_INK, w=7):
    """board drawing: a front-view head + torso outline (head first, then the body)."""
    draw_ell_on(f, cx, hy, 150, 160, clamp(k / 0.4), col, w, seed=11)
    kb = clamp((k - 0.4) / 0.6)
    for sg in (-1, 1):
        P = [(cx + sg * 52, hy + 152), (cx + sg * 58, hy + 205), (cx + sg * 210, hy + 250), (cx + sg * 250, hy + 330), (cx + sg * 240, hy + 760), (cx + sg * 150, hy + 830)]
        draw_on(f, P, kb, col, w, seed=12 + sg, tip=sg > 0)


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


RED_X = (176, 40, 44)
COLLEAGUE = (120, 150, 200); BOSSC = (70, 80, 110)
SRC_OSU = "Source: Mirondo & Barringer, Ohio State, J Food Sci (2016)"
SRC_MILK = "Source: Hansanugrum & Barringer, J Food Sci (2010), via Discover"


def board_lungs(f, t, x=540, y=1000, s=0.9, mood="happy", k=None):
    kk = 0.5 + 0.5 * math.sin(t * 2.6) if k is None else k
    comp(f, scale_el(lungs_el(mood, (0, -0.3), kk), s), x, y)


# ---- S0: HOOK, frame 0: the meeting room, Chubby mid-sentence leaning in to a colleague; a mauve garlic cloud is ALREADY rolling out of his mouth and the colleague recoils ----
def shot_S0(t, n):
    f = set_office(t)
    ln = 10 + 8 * eo(clamp(t / 0.5))
    chub(f, 780, 1500, 1.0, t=t, shirt=COLLEAGUE, la=(30, 14), ra=(150, -128), mouth=0, expr="gross", brow="sad", look=(-0.8, 0), lean=ln, turn=-0.5, hand_r="pinch")
    dress(f, 780, 1500, 1.0, "cousin", ln)
    chub(f, 300, 1500, 1.05, t=t, **nolean(POSE["present"]), mouth=talk(t), expr="happy", brow="up", look=(0.8, -0.1), lean=-8, turn=0.5)
    office_front(f, 1330)
    for j in range(3): puff(f, 380, 1000, t, -0.6 + j * 0.8, 1.5, 0.95 + 0.15 * j, 330, -80 - 50 * j, "n", 296 + j)
    kw(f, "GARLIC", 540, 330, t, 0.0, "stink", 150, amp=1.0); kw(f, "BREATH?", 540, 500, t, 0.25, "stink", 150, amp=1.0)
    return finish(f, n, look="golden")


# ---- S0b: '...lungs, not just your mouth?' MORPH into the BOARD: a body outline with the lungs; mauve puffs leave the mouth FROM the lungs ----
def shot_S0b(t, n):
    f = board_bg(); t0 = st_("S0b")
    figure(f, 1.0, 540, 470)
    board_lungs(f, t, 540, 1030, 0.85)
    draw_arrow_on(f, (540, 820), (540, 650), ramp(t, t0 + 0.2, 0.4), ACC_S, 8)
    for j in range(3): puff(f, 580, 560, t, t0 + 0.3 + j * 0.45, 1.2, 0.45, 220, -120, "n", 296 + j)
    write_on(f, "lungs", 880, 1320, t, t0 + 0.2, 52)
    write_on(f, "not just your mouth", 540, 300, t, T("i1", "mouth") - 0.4, 46, ACC_S)
    return finish(f, n, look="fresh")


# ---- S1: 'That's why you can brush twice' BATHROOM: Chubby brushes like mad in front of the mirror; a x2 chip ----
def brushing(f, t, x, y, s, fast=1.0, expr="n"):
    chub(f, x, y, s, t=t, la=(24, 12), ra=(140, -112 + 14 * math.sin(t * 30 * fast)), mouth=1, expr=expr, brow="sus", look=(0, 0.2), hand_r="grip")
    hx, hy = x, y - 420 * s
    rot_comp(f, brush_el(), hx + 40 * s + 12 * math.sin(t * 30 * fast), hy + 36 * s, 8, 0.55 * s, 1.0, 0.0)
    for j in range(5):
        q = (t * 1.6 + j / 5) % 1.0; cv2.circle(f, (int(hx - 40 * s + 45 * j * s), int(hy + 60 * s + 80 * q)), int(8 * (1 - q) + 3), C((250, 252, 255)), -1, cv2.LINE_AA)


def shot_S1(t, n):
    f = set_bathroom(t); t0 = st_("S1")
    brushing(f, t, 540, 1720, 1.45, 1.0, "sus")
    cc(f, "BRUSH x2", 540, 330, t, T("i2", "twice") - 0.2, ACC_S, MILK, 56)
    return finish(f, n, look="cool")


# ---- S1b: '...and your friend still backs away the next morning.' OFFICE morning: the colleague walks BACKWARDS away, holding his nose ----
def shot_S1b(t, n):
    f = set_office(t); t0 = st_("S1b"); q = ramp(t, t0 + 0.1, 1.4)
    chub(f, 700 + 200 * q, 1500, 0.95, t=t, shirt=COLLEAGUE, la=(30, 14), ra=(150, -128), mouth=0, expr="gross", brow="sad", look=(-1, 0), lean=10, turn=-0.5, hand_r="pinch")
    dress(f, 700 + 200 * q, 1500, 0.95, "cousin", 10)
    chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="sad", brow="sad", look=(1, 0), turn=0.4)
    office_front(f, 1330)
    puff(f, 380, 1000, t, t0 + 0.2, 1.6, 0.6, 300, -40, "n")
    icap(f, "still there the next", "MORNING", t, T("i2", "next") - 0.1, size=140, y=380)
    return finish(f, n, look="golden")


# ---- S2: 'Start with a whole clove of garlic.' WORKTOP: a whole bulb lands on the board, a clove pops off ----
def shot_S2(t, n):
    f = set_worktop(t); t0 = st_("S2")
    chub(f, 280, 1500, 1.0, t=t, la=(24, 12), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0.3), turn=0.5, hand_r="point")
    worktop_front(f, 1330)
    comp(f, board_ink_el(560), 720, 1330)
    y, sx, sy = drop_land(t, t0 + 0.05, 700, 1180, 0.35)
    comp(f, scale_el(garlic_bulb_el("happy"), 0.7), 680, y)
    tc = T("a0", "clove") - 0.1
    if t > tc: comp(f, scale_el(clove_el("n"), 0.5), 900, 1230, scale=snap(t, tc, 4))
    cc(f, "1 CLOVE", 900, 1060, t, tc + 0.05, ACC_S, MILK, 40)
    return finish(f, n, look="golden")


# ---- S2b: '...Sitting on the counter, it barely smells.' close: Chubby sniffs the clove: barely anything; ONE tiny wisp ----
def shot_S2b(t, n):
    f = set_worktop(t); t0 = st_("S2b"); f = dof(f, 3); tb = T("a0", "barely") - 0.3
    chub_head_only(f, 360, 980, 1.9, t, mouth=talk(t) if t > tb else 0, expr="sus" if t < tb else "n", brow="up", look=(1, 0.4), turn=0.5)
    worktop_front(f, 1330)
    comp(f, scale_el(clove_el("n", (-0.6, -0.2)), 0.95), 790, 1180)
    if t > tb + 0.2: wisp(f, 790, 1030, t, 1, 90, ACC_L)
    kw(f, "barely...", 540, 400, t, tb + 0.15, "pop", 110, col=INKC)
    return finish(f, n, look="golden")


# ---- S3: 'The smell only shows up when you cut it or crush it.' knife slices, then the flat blade SMASHES the clove: a mauve cloud bursts ----
def shot_S3(t, n):
    f = set_worktop(t); t0 = st_("S3"); tc = T("a1", "cut") - 0.1; tk = T("a1", "crush") - 0.15
    worktop_front(f, 1330)
    comp(f, board_ink_el(700), 540, 1330)
    crushed = t >= tk
    comp(f, scale_el(clove_el("wow" if t > tc else "n", crush=ramp(t, tk, 0.08) if crushed else 0.0), 1.15), 540, 1160 + (40 if crushed else 0))
    if not crushed:
        a = -20 + 40 * ramp(t, tc - 0.3, 0.3); rot_comp(f, knife_ink_el(), 620, 960 + 80 * ramp(t, tc - 0.2, 0.2), a, 0.9, 1.0, 0.0)
    else:
        rot_comp(f, knife_ink_el(), 560, 1090, 0, 1.0, 1.0, 0.0)
        cv2.circle(f, (690, 1070), 46, C(INK_SKIN), -1, cv2.LINE_AA); cv2.circle(f, (690, 1070), 46, C(INKC), 6, cv2.LINE_AA)
        for j in range(4): puff(f, 540, 1080, t, tk + j * 0.12, 1.4, 0.7, (-1) ** j * (180 + 40 * j), -260 - 60 * j, "n", 296 + j)
    kw(f, "CUT", 540, 360, t, tc, "pop", 130, col=INKC)
    kw(f, "CRUSH!", 540, 540, t, tk, "shake", 170, amp=1.4)
    return finish(f, n, look="golden")


# ---- S4: 'Crushing breaks the cells open, so two things that were kept apart...' BOARD: a cell as a ROOM; alliin in one corner, the enzyme in the other ----
CELL = (540, 1000)


def cell_room(f, t, broken, gap):
    comp(f, scale_el(cell_el(broken, True, 7, 720, 440), 1.25), CELL[0], CELL[1])
    comp(f, scale_el(alliin_el("n" if gap > 0.5 else "happy", (1, 0)), 1.35), CELL[0] - 120 - 130 * gap, CELL[1] + 8 * math.sin(t * 4))
    comp(f, scale_el(enzyme_el("n" if gap > 0.5 else "happy", (-1, 0), 0.3 + 0.3 * abs(math.sin(t * 6))), 1.35), CELL[0] + 120 + 130 * gap, CELL[1] + 8 * math.sin(t * 4 + 1))


def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tb = T("a2", "breaks") - 0.1
    cell_room(f, t, ramp(t, tb, 0.25), 1.0)
    write_on(f, "a garlic cell", 540, 330, t, t0 + 0.1, 56)
    write_on(f, "kept apart", 540, 680, t, T("a2", "apart") - 0.2, 46, ACC_S)
    return finish(f, n, look="fresh")


def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b")
    cell_room(f, t, 1.0, 1.0 - ramp(t, t0 + 0.05, 0.35))
    write_on(f, "a compound", 300, 1330, t, T("a2", "compound") - 0.2, 44)
    write_on(f, "+ an enzyme", 790, 1330, t, T("a2", "enzyme") - 0.2, 44)
    kw(f, "MEET", 540, 420, t, t0 + 0.1, "pop", 150)
    return finish(f, n, look="fresh")


# ---- S5: 'In seconds they make allicin,' BOARD: a stopwatch flicks, ALLICIN pops out; S5b: '...falls apart into smelly sulfur gases' it CRACKS into 5 mauve gas buddies ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); ta = T("a3", "allicin") - 0.1
    draw_ell_on(f, 860, 450, 80, 80, ramp(t, t0, 0.3), BP_INK, 7, seed=21)
    a = math.radians(-90 + 360 * ramp(t, t0 + 0.1, 0.6)); cv2.line(f, (860, 450), (int(860 + 60 * math.cos(a)), int(450 + 60 * math.sin(a))), C(BP_INK), 7, cv2.LINE_AA)
    write_on(f, "seconds", 860, 590, t, T("a3", "seconds") - 0.2, 40)
    comp(f, scale_el(alliin_el("happy", (1, 0)), 1.2), 300 + 120 * ramp(t, t0, 0.4), 1000)
    comp(f, scale_el(enzyme_el("happy", (-1, 0), 0.5), 1.2), 780 - 120 * ramp(t, t0, 0.4), 1000)
    if t > ta: comp(f, scale_el(allicin_el("wow"), 1.3), 540, 1010 - 60 * eo(clamp((t - ta) / 0.3)), scale=snap(t, ta, 4))
    write_on(f, "allicin", 540, 1260, t, ta + 0.1, 58, ACC_S)
    return finish(f, n, look="fresh")


GAS_POS = [(250, 760), (830, 720), (290, 1180), (800, 1180), (540, 640)]


def shot_S5b(t, n):
    f = board_bg(); t0 = st_("S5b"); tf = T("a3", "apart") - 0.15
    if t < tf + 0.1: rot_comp(f, scale_el(allicin_el("wow"), 1.3), 540 + 6 * math.sin(t * 60), 950, 4 * math.sin(t * 50), 1.0, 1.0)
    if t >= tf:
        for i, (x, y) in enumerate(GAS_POS):
            q = eo(clamp((t - tf) / 0.5)); xx = 540 + (x - 540) * q; yy = 950 + (y - 950) * q + 10 * math.sin(t * 4 + i)
            comp(f, scale_el(gas_el2(("happy", "n", "wow", "n", "happy")[i], (0, 0), 296 + i), 0.75), xx, yy)
    kw(f, "SMELLY", 540, 380, t, T("a3", "smelly") - 0.15, "stink", 150)
    write_on(f, "sulfur gases", 540, 1420, t, T("a3", "sulfur") - 0.1, 52)
    return finish(f, n, look="fresh")


# ---- S6: 'But the part nobody tells you is this: garlic breath comes from two places.' close: Chubby leans in, whispering; a big ink title 2 PLACES ----
def shot_S6(t, n):
    f = set_worktop(t); t0 = st_("S6"); tt = T("b0", "two") - 0.1
    f = dof(f, 3)
    t3(f, "2 PLACES", 520, t, tt, 190)
    chub(f, 540, 1600, 1.25, t=t, **nolean(POSE["whisper"]), lean=8, mouth=talk(t), expr="smirk", brow="up", look=(-0.6, 0.2), turn=-0.3)
    worktop_front(f, 1420)
    return finish(f, n, look="golden")


# ---- S7: 'Place one is your mouth.' BOARD: a big open mouth; S7b: 'Tiny bits of garlic stuck to your teeth and tongue keep giving off those gases.' ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7")
    comp(f, scale_el(tongue_teeth_el(0.0), 1.2), 540, 1000, scale=snap(t, t0 + 0.05, 4))
    kw(f, "1. MOUTH", 540, 420, t, t0 + 0.1, "pop", 130, col=BP_INK)
    return finish(f, n, look="fresh")


def shot_S7b(t, n):
    f = board_bg(); t0 = st_("S7b")
    comp(f, scale_el(tongue_teeth_el(1.0), 1.2), 540, 1000)
    for (x, y) in ((402, 770), (530, 774), (620, 1150)): wisp(f, x, y, t, 2, 160)
    for w_, x, y, lx, ly in (("teeth", 410, 800, 220, 600), ("tongue", 600, 1180, 840, 1400)):
        tw = T("b1", w_) - 0.2
        if t > tw: draw_arrow_on(f, (lx, ly + (40 if ly < 900 else -40)), (x, y), ramp(t, tw, 0.3), BP_INK, 6); write_on(f, w_, lx, ly, t, tw, 48)
    write_on(f, "garlic bits", 540, 380, t, t0 + 0.1, 56, ACC_S)
    return finish(f, n, look="fresh")


# ---- S8: 'Brushing and flossing really do help with that part.' BATHROOM: brush, then floss; the mouth puffs POP; a stamp: HELPS ----
def shot_S8(t, n):
    f = set_bathroom(t); t0 = st_("S8"); tf = T("b2", "flossing") - 0.1
    if t < tf: brushing(f, t, 540, 1720, 1.45, 0.8, "n")
    else:
        chub(f, 540, 1720, 1.45, t=t, la=(140, -112 + 10 * math.sin(t * 20)), ra=(140, -112 - 10 * math.sin(t * 20)), mouth=1, expr="n", brow="up", look=(0, 0.2), hand_r="pinch", hand_l="pinch")
        hy = int(1720 - 420 * 1.45 + 55)
        cv2.line(f, (int(440 + 10 * math.sin(t * 20)), hy), (int(640 - 10 * math.sin(t * 20)), hy), C((250, 250, 250)), 4, cv2.LINE_AA)
    for j, tp in enumerate((t0 + 0.3, t0 + 0.9, tf + 0.3)):
        if tp < t < tp + 0.25: cv2.circle(f, (int(380 + 150 * j), 820), int(20 + 160 * (t - tp)), C(ACC), 6, cv2.LINE_AA)
        elif t < tp: comp(f, scale_el(gas_el2("sad", seed=296 + j), 0.45), 380 + 150 * j, 820 + 6 * math.sin(t * 5 + j))
    tr = T("b2", "really") - 0.1
    if t > tr: slam(f, vstamp_el("HELPS", INK_MINT_S, 90), 540, 380, -6, t, tr)
    return finish(f, n, look="cool")


# ---- S9: 'Place two is sneakier.' BOARD: SNEAKIER tiptoes in letter by letter, AMS in a bandit mask sneaks after it; S9b: its name, AMS ----
def shot_S9(t, n):
    f = board_bg(); t0 = st_("S9")
    kw(f, "2.", 170, 420, t, t0 + 0.05, "pop", 130, col=BP_INK)
    kw(f, "SNEAKIER", 590, 420, t, T("b3", "sneakier") - 0.25, "sneak", 140, stagger=0.06)
    q = ramp(t, t0 + 0.2, 1.2)
    rot_comp(f, scale_el(ams_el("sly", (1, 0)), 1.3), -150 + 690 * q, 1000 - 50 * abs(math.sin(t * 7)), 6 * math.sin(t * 7), 1.0, 1.0)
    return finish(f, n, look="fresh")


def shot_S9b(t, n):
    f = board_bg(); t0 = st_("S9b"); to = T("b3", "others") - 0.3
    comp(f, scale_el(ams_el("sly", (0.6, 0)), 1.3), 540, 900 + 8 * math.sin(t * 4))
    write_on(f, "allyl methyl sulfide", 540, 1220, t, t0 + 0.1, 46, ACC_S)
    cc(f, "AMS", 540, 1360, t, t0 + 0.8, ACC_S, MILK, 50)
    if t > to:
        for i, x in enumerate((180, 900)): comp(f, scale_el(gas_el2("sad", seed=300 + i), 0.5), x, 640 + 20 * i, scale=snap(t, to + 0.1 * i, 4))
        write_on(f, "the others get broken down", 540, 420, t, to, 40)
    return finish(f, n, look="fresh")


# ---- S10: 'Your gut and your liver just can't deal with it,' BOARD: stomach + liver gobble the other gases; AMS ducks past; S10b: '...so it slips into your blood.' ----
def shot_S10(t, n):
    f = board_bg(); t0 = st_("S10"); tl = T("b4", "liver") - 0.1; tcd = T("b4", "cant") - 0.2
    comp(f, scale_el(stomach_ink_el("happy", (0.6, -0.4)), 1.25), 300, 960)
    if t > tl: comp(f, scale_el(liver_el("ouch" if t > tcd else "happy", (0.5, 0), arms="shrug" if t > tcd else "work"), 1.05), 780, 980, scale=snap(t, tl, 4))
    for i in range(3):
        tg = t0 + 0.2 + i * 0.35; q = clamp((t - tg) / 0.5)
        if q < 1: comp(f, scale_el(gas_el2("wow", seed=296 + i), 0.4), 300 + 40 * i, 640 + 360 * eo(q), op=1 - q * q)
    q = ramp(t, t0 + 0.6, 2.0)
    rot_comp(f, scale_el(ams_el("sly", (1, 0.5)), 0.8), 160 + 760 * q, 1400 - 60 * math.sin(math.pi * q), 0, 1.0, 1.0)
    write_on(f, "gut", 300, 1210, t, t0 + 0.2, 48); write_on(f, "liver", 780, 1200, t, tl, 48)
    kw(f, "can't deal", 540, 420, t, tcd, "drop", 110, col=INKC, t1=tcd + 1.0)
    return finish(f, n, look="fresh")


VESSEL = [(80, 1340), (300, 1300), (540, 1240), (780, 1290), (1000, 1250)]


def shot_S10b(t, n):
    f = board_bg(); t0 = st_("S10b"); ts = T("b4", "slips") - 0.2
    for w_, c in ((60, BP_INK), (46, (232, 120, 120))): cv2.polylines(f, [np.int32(VESSEL)], False, C(c), w_, cv2.LINE_AA)
    for j in range(6):
        q = (t * 0.5 + j / 6) % 1.0; x, y = path_point(VESSEL, q)
        cv2.circle(f, (int(x), int(y)), 14, C(BLOOD), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 14, C(INKC), 3, cv2.LINE_AA)
    if t < ts + 0.4:
        q = ramp(t, t0, max(0.2, ts + 0.4 - t0)); comp(f, scale_el(ams_el("sly", (0, 1)), 0.9), 540, 800 + 400 * q * q)
    else:
        q = ((t - ts - 0.4) * 0.4) % 1.0; x, y = path_point(VESSEL, 0.5 + 0.5 * q)
        comp(f, scale_el(ams_el("happy", (1, 0)), 0.42), x, y - 6)
    write_on(f, "your blood", 540, 1430, t, ts, 52, (176, 40, 44))
    kw(f, "slips in", 540, 420, t, ts, "sneak", 120)
    return finish(f, n, look="fresh")


# ---- S11: 'It rides around your whole body, reaches your lungs' BOARD: AMS rides a red loop into the lungs; S11b: '...every breath you breathe out.' lit, morph ----
RIDE = [(540, 1300), (330, 1400), (250, 1200), (300, 900), (420, 820), (540, 900)]


def shot_S11(t, n):
    f = board_bg(); t0 = st_("S11"); tl = T("b5", "lungs") - 0.2
    figure(f, 1.0, 540, 470)
    board_lungs(f, t, 540, 1040, 0.95, "n" if t < tl else "wow")
    draw_on(f, RIDE, ramp(t, t0 + 0.1, 1.2), (200, 60, 60), 9, seed=40)
    q = ramp(t, t0 + 0.2, max(0.3, tl - t0 - 0.2))
    x, y = path_point(RIDE, q); comp(f, scale_el(ams_el("sly", (0.4, -0.4)), 0.4), x, y)
    write_on(f, "whole body", 540, 300, t, T("b5", "whole") - 0.2, 50)
    return finish(f, n, look="fresh")


def shot_S11b(t, n):
    f = set_worktop(t); t0 = st_("S11b")
    chub(f, 470, 1500, 1.1, t=t, **nolean(POSE["cheek"]), lean=-4, mouth="o" if (t * 0.8) % 1 < 0.5 else 1, expr="sus", brow="sus", look=(0.6, 0.2), turn=0.4)
    worktop_front(f, 1330)
    for j in range(3): puff(f, 520, 880, t, t0 + j * 0.8, 1.4, 0.5, 300, -100, "n", 296 + j)
    kw(f, "every breath", 540, 400, t, T("b5", "every") - 0.1, "breathe", 120, amp=1.5)
    return finish(f, n, look="golden")


# ---- S12: 'Some of it even comes out through your sweat.' DUSK: Chubby walks home warm, sweat drops with mauve wisps ----
def shot_S12(t, n):
    t0 = st_("S12"); f = inkify(set_dusk(t))
    w = walk(t, 380, 1520, 1.2, speed=70, t0=t0, period=1.08)
    w.pop("look", None); wx = w["x"]
    chub(f, s=1.2, t=t, mouth=talk(t), expr="sad", brow="sad", look=(0.7, 0.2), **w)
    for i, (dx, ph) in enumerate(((-90, 0.0), (80, 0.5))):
        q = (t * 0.6 + ph) % 1.0
        comp(f, scale_el(sweat_drop_el("sad" if i == 0 else "n"), 0.45), wx + dx * 1.2, 1520 - 560 + 120 * q)
        wisp(f, wx + dx * 1.2, 1520 - 600 + 120 * q, t, 1, 70)
    kw(f, "SWEAT", 540, 400, t, T("b6", "sweat") - 0.25, "drop", 150, t1=T("b6", "sweat") + 0.7)
    return finish(f, n, look="golden")


# ---- S13: 'So your mouth can be squeaky clean while your lungs keep doing the talking.' BOARD split: a sparkling mouth vs the lungs with a stinky speech bubble ----
def shot_S13(t, n):
    f = board_bg(); t0 = st_("S13"); tl = T("b7", "lungs") - 0.2
    cv2.line(f, (540, 560), (540, 1420), C(BP_GRID2), 6, cv2.LINE_AA)
    comp(f, scale_el(tongue_teeth_el(0.0), 0.75), 285, 1020)
    for j in range(3):
        a = t * 4 + j * 2.1; x, y = 285 + 150 * math.cos(a), 1020 + 100 * math.sin(a)
        cv2.line(f, (int(x - 16), int(y)), (int(x + 16), int(y)), C(INK_MINT_S), 5, cv2.LINE_AA); cv2.line(f, (int(x), int(y - 16)), (int(x), int(y + 16)), C(INK_MINT_S), 5, cv2.LINE_AA)
    kw(f, "clean", 285, 700, t, T("b7", "clean") - 0.2, "pop", 100, col=INK_MINT_S)
    if t > tl:
        board_lungs(f, t, 790, 1120, 0.72, "happy")
        comp(f, scale_el(gas_el2("happy"), 0.75), 790, 800 + 6 * math.sin(t * 5), scale=pin(t, tl + 0.2))
        kw(f, "talking", 760, 560, t, T("b7", "talking") - 0.15, "shake", 100)
    return finish(f, n, look="fresh")


# ---- S14: 'How long can that last?' the office wall clock spins its hands, Chubby looks up at it ----
def shot_S14(t, n):
    f = set_office(t, dim=0.15); t0 = st_("S14")
    comp(f, clock_ink_el(150), 540, 640); clock_hands(f, 540, 640, 9 + 30 * (t - t0), 150)
    chub(f, 540, 1580, 1.05, t=t, **nolean(POSE["think"]), lean=-4, mouth=talk(t), expr="sus", brow="sus", look=(0, -1))
    office_front(f, 1420)
    kw(f, "HOW LONG?", 540, 330, t, t0 + 0.05, "pop", 120)
    return finish(f, n, look="cool")


# ---- S15: '...you can still smell it twenty-four hours later.' BOARD: a 2-day ruler (sun, moon, sun, moon); the stink bar runs to 24 h; S15b: dashed to 2 days ----
RX0, RX1, RY = 140, 940, 900


def ruler(f, t, t0, upto, dashed_to=None):
    draw_on(f, [(RX0, RY), (RX1, RY)], ramp(t, t0, 0.4), BP_INK, 8, seed=50)
    for h_ in range(0, 49, 6):
        x = RX0 + (RX1 - RX0) * h_ / 48; cv2.line(f, (int(x), RY - 18), (int(x), RY + 18), C(BP_INK), 5, cv2.LINE_AA)
    for i, (h_, lab) in enumerate(((0, "0"), (24, "24 h"), (48, "48 h"))):
        x = RX0 + (RX1 - RX0) * h_ / 48; write_on(f, lab, x, RY + 80, t, t0 + 0.2 + i * 0.1, 34)
    for i, h_ in enumerate((6, 18, 30, 42)):
        x = RX0 + (RX1 - RX0) * h_ / 48
        if i % 2 == 0: cv2.circle(f, (int(x), RY - 140), 34, C((250, 200, 70)), -1, cv2.LINE_AA); cv2.circle(f, (int(x), RY - 140), 34, C(INKC), 4, cv2.LINE_AA)
        else: moon_icon(f, int(x), RY - 140, 30, BP_PAPER)
    xe = RX0 + (RX1 - RX0) * upto / 48
    if xe > RX0 + 2:
        cv2.rectangle(f, (RX0, RY - 70), (int(xe), RY - 30), C(ACC), -1, cv2.LINE_AA); cv2.rectangle(f, (RX0, RY - 70), (int(xe), RY - 30), C(INKC), 4, cv2.LINE_AA)
    if dashed_to:
        xd = RX0 + (RX1 - RX0) * dashed_to / 48
        for x in range(int(xe), int(xd), 40): cv2.rectangle(f, (x, RY - 62), (min(int(xd), x + 22), RY - 38), C(ACC_L), -1, cv2.LINE_AA)


def shot_S15(t, n):
    f = board_bg(); t0 = st_("S15"); tt = T("c1", "twentyfour") - 0.2
    ruler(f, t, t0, 24 * ramp(t, t0 + 0.4, max(0.3, tt - t0 - 0.2)))
    if t > tt: ui_word(f, "you can still smell it", str(count_up(t, tt, 24)) + " [HOURS]", 1180, t, tt, col=INKC, acc=ACC_S, size=130)
    write_on(f, "an Ohio State food scientist", 540, 380, t, t0 + 0.1, 40)
    src(f, "Source: Sheryl Barringer, Ohio State, via Popular Science (2016)", t, t0 + 0.4)
    return finish(f, n, look="fresh")


def shot_S15b(t, n):
    f = board_bg(); t0 = st_("S15b")
    ruler(f, t, t0 - 2, 24, 24 + 24 * ramp(t, t0 + 0.2, 1.0))
    kw(f, "up to 2 DAYS", 540, 1180, t, T("c1", "two") - 0.2, "pop", 120)
    write_on(f, "some sources", 540, 380, t, t0 + 0.05, 44)
    src(f, "Source: BBC Science Focus", t, t0 + 0.3)
    return finish(f, n, look="fresh")


# ---- S16: 'That's a whole day of meetings, smelling like last night's dinner.' OFFICE: Chubby presents; three colleagues lean away, one fans the air ----
def shot_S16(t, n):
    f = set_office(t); t0 = st_("S16")
    chub(f, 830, 1500, 0.95, t=t, **nolean(POSE["point"]), lean=-2, mouth=talk(t), expr="happy", brow="up", look=(-0.4, 0), turn=-0.5, hand_r="point")
    for i, (x, kind, col) in enumerate(((150, "boss", BOSSC), (340, "cousin", COLLEAGUE), (530, "aunty", (190, 120, 150)))):
        ln = -10 - 6 * ramp(t, t0 + 0.2 + i * 0.25, 0.3)
        chub(f, x, 1560, 0.8, t=t, shirt=col, la=(30, 14), ra=(150, -128) if i != 1 else (110, 80 + 30 * math.sin(t * 14)), mouth=0, expr="gross", brow="sad", look=(1, 0), lean=ln, turn=0.4, hand_r="pinch")
        dress(f, x, 1560, 0.8, kind, ln)
    office_front(f, 1400)
    puff(f, 760, 900, t, t0 + 0.1, 2.0, 0.6, -420, -40, "happy")
    tdn = T("c2", "dinner") - 0.3
    icap(f, "a whole day of", "MEETINGS", t, T("c2", "meetings") - 0.2, size=110, y=380, out=tdn - 0.05)
    kw(f, "DINNER", 540, 400, t, tdn, "stink", 140)
    return finish(f, n, look="golden")


# ---- S17: 'So can you actually fight it?' Chubby takes a fighting stance (cartoon take) ----
def shot_S17(t, n):
    f = set_worktop(t); t0 = st_("S17"); tk = take(t, T("d0", "fight") - 0.2)
    chub(f, 540, 1500 + tk["dy"], 1.15, t=t, la=(70, 130), ra=(70, 130), mouth=talk(t), expr="smirk", brow="up", look=(0, 0.2), lean=tk["lean"], squash=tk["squash"], hand_r="grip", hand_l="grip")
    worktop_front(f, 1330)
    kw(f, "FIGHT IT?", 540, 380, t, T("d0", "fight") - 0.2, "shake", 140, amp=1.2)
    return finish(f, n, look="golden")


# ---- S18: 'Her team tested it. People chewed raw garlic, then ate different foods,' BOARD lab bench; S18b: '...a machine measured their breath.' ----
FOODS = (("apple", lambda: red_apple(), 0.5), ("lettuce", lambda: lettuce_el(), 0.5), ("mint", lambda: mint_sprig_el(), 0.45), ("tea", lambda: mug_el((120, 170, 90), 0.8), 0.6), ("water", lambda: glass2_el((200, 226, 246), 0.8), 0.45))


def shot_S18(t, n):
    f = board_bg(); t0 = st_("S18"); tc = T("d1", "chewed") - 0.2; tf = T("d1", "foods") - 0.3
    write_on(f, "Ohio State, 2016", 540, 330, t, t0 + 0.05, 50, ACC_S)
    if t > tc: comp(f, scale_el(clove_el("n"), 0.7), 540, 700, scale=snap(t, tc, 4)); write_on(f, "raw garlic, chewed", 540, 880, t, tc + 0.1, 44)
    for i, (nm, mk, s_) in enumerate(FOODS):
        ti = tf + i * 0.12
        if t > ti: x = 150 + i * 195; comp(f, scale_el(mk(), s_ * 1.4), x, 1150, scale=snap(t, ti, 4)); write_on(f, nm, x, 1320, t, ti + 0.05, 40)
    return finish(f, n, look="fresh")


def shot_S18b(t, n):
    f = board_bg(); t0 = st_("S18b")
    comp(f, scale_el(breath_meter_el(0.95 + 0.03 * math.sin(t * 8)), 1.5), 620, 980, scale=snap(t, t0 + 0.05, 4))
    chub_head_only(f, 190, 760, 1.2, t, mouth="o", expr="n", brow="up", look=(1, 0), turn=0.6)
    for j in range(2): puff(f, 260, 790, t, t0 + 0.2 + j * 0.6, 0.9, 0.3, 100, 20)
    write_on(f, "breath meter", 620, 1300, t, T("d1", "machine") - 0.2, 50)
    return finish(f, n, look="fresh")


# ---- S19: 'Raw apple and raw lettuce cut the smelly gases by half or more, for the first thirty minutes.' BOARD bars ----
BAR_X = (150, 330, 510, 690, 870); BAR_Y0 = 1200; BAR_H = 520


def bar(f, i, v, lab, icon, s_, crown=False):
    x = BAR_X[i]; top = BAR_Y0 - BAR_H * v
    cv2.rectangle(f, (x - 60, int(top)), (x + 60, BAR_Y0), C(ACC_L if i else (226, 222, 214)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x - 60, int(top)), (x + 60, BAR_Y0), C(INKC), 5, cv2.LINE_AA)
    comp(f, scale_el(icon, s_), x, BAR_Y0 + 70)
    comp(f, hand_text_el(lab, 52, BP_INK), x, BAR_Y0 + 160)
    if crown: comp(f, scale_el(medal_el("BEST"), 0.4), x, top - 70)


def chart(f, t, vals, crown=False):
    cv2.line(f, (60, BAR_Y0), (1020, BAR_Y0), C(BP_INK), 6, cv2.LINE_AA)
    for i, (nm, mk, s_) in enumerate((FOODS[4], FOODS[0], FOODS[1], FOODS[2], FOODS[3])):
        if vals[i] is not None: bar(f, i, vals[i], nm, mk(), s_ * 0.8, crown and i == 3)


def shot_S19(t, n):
    f = board_bg(); t0 = st_("S19"); th = T("d2", "half") - 0.3
    v = 1.0 - 0.55 * ramp(t, th, 0.5)
    chart(f, t, [1.0, v, v, None, None])
    write_on(f, "garlic smell left", 540, 330, t, t0 + 0.05, 44)
    if t > th:
        cv2.line(f, (60, int(BAR_Y0 - BAR_H * 0.5)), (1020, int(BAR_Y0 - BAR_H * 0.5)), C(ACC_S), 4, cv2.LINE_AA)
        kw(f, "-50%", 800, 560, t, th + 0.2, "pop", 120)
    cc(f, "first 30 minutes", 800, 680, t, T("d2", "thirty") - 0.2, INKC, MILK, 34)
    src(f, SRC_OSU, t, t0 + 0.3)
    return finish(f, n, look="fresh")


def shot_S20(t, n):
    f = board_bg(); t0 = st_("S20"); tm = T("d3", "mint") - 0.2; tt = T("d3", "tea") - 0.2
    vm = 1.0 - 0.75 * ramp(t, tm, 0.5)
    chart(f, t, [1.0, 0.45, 0.45, vm if t > tm else None, 1.0 if t > tt else None], crown=t > T("d3", "better") - 0.1)
    kw(f, "MINT WINS", 540, 360, t, T("d3", "better") - 0.15, "pop", 100)
    if t > tt: kw(f, "NOTHING", 770, 600, t, tt + 0.15, "drop", 80, col=INKC, t1=T("d3", "all") + 0.1)
    src(f, SRC_OSU, t, t0)
    return finish(f, n, look="fresh")


# ---- S21: 'Cooked apple helped too, but raw won,' BOARD: steaming cooked apple vs raw, a medal on raw; S21b: '...an enzyme plus plant compounds that break the gases down.' ----
def shot_S21(t, n):
    f = board_bg(); t0 = st_("S21"); tw = T("d4", "won") - 0.2
    comp(f, scale_el(red_apple("n"), 0.9), 300, 1000)
    wisp(f, 300, 840, t, 3, 140, (150, 170, 200))
    write_on(f, "cooked", 300, 1220, t, t0 + 0.1, 50)
    comp(f, scale_el(red_apple("happy" if t > tw else "n"), 0.9), 780, 1000)
    write_on(f, "raw", 780, 1220, t, t0 + 0.4, 50)
    if t > tw: slam(f, medal_el("RAW"), 780, 740, -8, t, tw)
    kw(f, "helped too", 300, 420, t, T("d4", "helped") - 0.2, "pop", 80, col=INKC)
    return finish(f, n, look="fresh")


def shot_S21b(t, n):
    f = board_bg(); t0 = st_("S21b"); te = T("d4", "enzyme") - 0.2; tp = T("d4", "plant") - 0.2; td = T("d4", "down") - 0.3
    comp(f, scale_el(red_apple("happy", cut=True), 0.75), 540, 1240)
    if t > te: comp(f, scale_el(enzyme_el("happy", (0, -1), 0.5 + 0.5 * abs(math.sin(t * 9))), 0.8), 330, 900, scale=snap(t, te, 4)); write_on(f, "enzyme", 330, 1060, t, te, 42)
    if t > tp:
        for j in range(5):
            a = t * 2 + j * 1.25; x, y = int(760 + 70 * math.cos(a)), int(900 + 70 * math.sin(a))
            cv2.circle(f, (x, y), 18, C(MNT), -1, cv2.LINE_AA); cv2.circle(f, (x, y), 18, C(INKC), 4, cv2.LINE_AA)
        write_on(f, "plant compounds", 760, 1060, t, tp, 42)
    for i, x in enumerate((330, 760)):
        if t < td + 0.3: comp(f, scale_el(gas_el2("wow", seed=296 + i), 0.5), x, 660 + 60 * ramp(t, td - 0.6, 0.6))
        elif t < td + 0.6: cv2.circle(f, (x, 720), int(40 + 300 * (t - td - 0.3)), C(ACC), 6, cv2.LINE_AA)
    kw(f, "GASES", 540, 400, t, t0 + 0.05, "blow", 120, src=(540, 1000), t1=td + 0.3)
    return finish(f, n, look="fresh")


# ---- S22: 'And an older study from the same lab found milk helps too, especially whole milk,' WORKTOP: garlic naan + a big glass of milk; S22b: '...better WITH the meal than after it.' ----
def shot_S22(t, n):
    f = set_worktop(t); t0 = st_("S22"); tm = T("d5", "milk") - 0.2
    chub(f, 340, 1500, 1.05, t=t, la=(24, 12), ra=(120, 20), mouth=talk(t), expr="happy", brow="up", look=(1, 0.4), turn=0.5, hand_r="grip")
    worktop_front(f, 1330)
    comp(f, scale_el(naan_el(), 0.8), 780, 1300)
    if t > tm: comp(f, scale_el(glass2_el(MILK, 0.85), 0.9), 640, 1190, scale=snap(t, tm, 4))
    cc(f, "WHOLE MILK", 640, 960, t, T("d5", "whole") - 0.2, ACC_S, MILK, 44)
    src(f, SRC_MILK, t, t0 + 0.3)
    return finish(f, n, look="golden")


def shot_S22b(t, n):
    f = board_bg(); t0 = st_("S22b"); tw = T("d5", "with") - 0.2; ta = T("d5", "after") - 0.2
    comp(f, scale_el(thali_el("full"), 0.7), 300, 1000)
    comp(f, scale_el(glass2_el(MILK, 0.8), 0.6), 440, 920)
    if t > tw: slam(f, chip("WITH THE MEAL", INK_MINT_S, MILK, 42), 320, 1250, -4, t, tw)
    if t > ta:
        comp(f, scale_el(thali_el("empty"), 0.55), 780, 1020); comp(f, scale_el(glass2_el(MILK, 0.8), 0.5), 880, 930)
        write_on(f, "after", 780, 1230, t, ta, 48); stamp_x(f, 800, 1000, 120, snap(t, ta + 0.3, 3), RED_X, 14)
    kw(f, "BETTER", 540, 420, t, T("d5", "better") - 0.2, "pop", 120)
    return finish(f, n, look="fresh")


# ---- S23: 'So brush for the mouth part,' BOARD recap 1; S23b: 'and grab an apple, some lettuce or a few mint leaves for the rest.' ----
def shot_S23(t, n):
    f = board_bg(); t0 = st_("S23")
    comp(f, chip("SAVE THIS", INKC, ACC_L, 34), 540, 330, op=clamp((t - t0) / 0.2))
    rot_comp(f, brush_el(), 540, 600, 0, 1.3, 1.0)
    write_on(f, "brush = the mouth part", 540, 780, t, T("e0", "brush") - 0.1, 46)
    return finish(f, n, look="fresh")


def shot_S23b(t, n):
    f = board_bg(); t0 = st_("S23b")
    comp(f, chip("SAVE THIS", INKC, ACC_L, 34), 540, 330)
    rot_comp(f, brush_el(), 540, 600, 0, 1.3, 1.0); write_on(f, "brush = the mouth part", 540, 780, t, t0 - 5, 46)
    for w_, mk, x in (("apple", lambda: red_apple("happy"), 240), ("lettuce", lambda: lettuce_el("happy"), 540), ("mint", lambda: mint_sprig_el("happy"), 840)):
        tw = T("e0", w_) - 0.2
        if t > tw: comp(f, scale_el(mk(), 0.85), x, 1060, scale=snap(t, tw, 4))
    write_on(f, "= the rest", 540, 1290, t, T("e0", "rest") - 0.2, 52, ACC_S)
    return finish(f, n, look="fresh")


# ---- S24: 'And the part in your lungs? That one mostly just needs time.' BOARD: the lungs breathe out smaller and smaller puffs while a clock runs ----
def shot_S24(t, n):
    f = board_bg(); t0 = st_("S24"); tt = T("e1", "time") - 0.2
    board_lungs(f, t, 540, 1080, 1.05, "happy")
    comp(f, clock_ink_el(90), 860, 640); clock_hands(f, 860, 640, 3 + 6 * (t - t0), 90)
    for j in range(4): puff(f, 540, 820, t, t0 + j * 0.9, 1.0, 0.5 * (1 - 0.2 * j), 0, -200, "n", 296 + j)
    kw(f, "time", 540, 420, t, tt, "breathe", 150, amp=1.5)
    return finish(f, n, look="fresh")


# ---- S25: 'Garlic's still worth it, by the way.' Chubby hugs the bulb; S25b: '...Maybe just not right before a job interview.' ----
def shot_S25(t, n):
    f = set_worktop(t); t0 = st_("S25")
    chub(f, 540, 1500, 1.1, t=t, la=(60, 100), ra=(60, 100), mouth=talk(t), expr="happy", brow="up", look=(0, 0.5), lean=4 * math.sin(t * 3))
    comp(f, scale_el(garlic_bulb_el("love"), 0.6), 540, 1270)
    worktop_front(f, 1330)
    kw(f, "WORTH IT", 540, 380, t, T("f1", "worth") - 0.2, "pop", 140)
    return finish(f, n, look="golden")


def shot_S25b(t, n):
    f = set_office(t); t0 = st_("S25b"); ti = T("f1", "interview") - 0.3
    chub(f, 790, 1560, 0.95, t=t, shirt=BOSSC, la=(30, 14), ra=(40, 30), mouth=0, expr="sus", brow="sus", look=(-1, 0), turn=-0.5)
    dress(f, 790, 1560, 0.95, "boss")
    chub(f, 290, 1560, 1.0, t=t, la=(24, 12), ra=(150, -128), mouth=talk(t), expr="sad", brow="sad", look=(1, 0), turn=0.4)
    office_front(f, 1400)
    comp(f, papers_el(2), 560, 1370)
    kw(f, "JOB INTERVIEW", 540, 380, t, ti, "pop", 110, col=INKC)
    return finish(f, n, look="cool")


# ---- S26: 'Send this to the friend who had the garlic naan and is standing way too close.' the friend leans way too close; then the logo ----
def shot_S26(t, n):
    t0 = st_("S26"); f = set_office(t); vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        z = 1.0 + 0.35 * ramp(t, T("f2", "close") - 0.6, 0.6)
        yb = 1500 + 300 * (z - 1)
        chub(f, 700, yb, 1.05 * z, t=t, shirt=COLLEAGUE, la=(24, 12), ra=(90, 60), mouth=3, expr="happy", brow="up", look=(-0.5, 0.3), turn=-0.3, hand_r="grip")
        dress(f, 700, yb, 1.05 * z, "cousin")
        rot_comp(f, scale_el(naan_el(), 0.6 * z), 880, 1160, 20, 1.0, 1.0)
        puff(f, 640, 1000, t, t0 + 0.3, 2.0, 0.6, -300, -40, "happy")
        comp(f, scale_el(phone2_el("garlic naan tonight?", "stand back pls", t > T("f2", "Send") + 0.3), 0.6), 250, 1000, scale=pin(t, t0))
        ui_word(f, "send this to the friend", "WAY TOO [CLOSE]", 380, t, T("f2", "Send") - 0.05, col=INKC, acc=ACC_S, size=96)
    else:
        f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32); k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 760, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 540, 1500, 0.62, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up")
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(0.3, 0.3, 8), (T("i1", "lungs") - 0.1, 0.3, 10), (T("i2", "morning") - 0.1, 0.3, 10), (T("a1", "crush") - 0.15, 0.45, 18),
           (T("a2", "breaks") - 0.1, 0.35, 12), (T("a2", "meet") - 0.1, 0.3, 10), (T("a3", "apart") - 0.15, 0.4, 14), (T("b0", "two") - 0.1, 0.35, 12),
           (T("b2", "really") - 0.1, 0.3, 10), (T("b4", "cant") - 0.2, 0.25, 8), (T("b4", "slips") - 0.2, 0.25, 8), (T("b5", "lungs") - 0.2, 0.3, 10),
           (T("b7", "talking") - 0.15, 0.3, 10), (T("c1", "twentyfour") - 0.2, 0.35, 12), (T("c2", "dinner") - 0.3, 0.3, 10), (T("d0", "fight") - 0.2, 0.4, 14),
           (T("d2", "half") - 0.3, 0.3, 10), (T("d3", "better") - 0.1, 0.3, 10), (T("d4", "won") - 0.2, 0.35, 12), (T("d4", "down"), 0.3, 10),
           (T("d5", "with") - 0.2, 0.3, 10), (T("e1", "time") - 0.2, 0.25, 8), (T("f1", "interview") - 0.3, 0.3, 10), (T("f2", "close") - 0.1, 0.3, 10)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


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
