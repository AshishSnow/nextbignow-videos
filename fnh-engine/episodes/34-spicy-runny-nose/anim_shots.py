# ================= shots: FreshNestHub 34 — "Why does spicy food make your nose run?" (Chubby INK, ep 15 of the ink look; FIRST 35-50 s episode) ===
# COLOUR SCRIPT: CHILLI RED (ACC) = heat / capsaicin / the alarm only (the flame buddy, the alarm bell, ON FIRE, the tap handle). Mucus = pale clear green.
# Story = lit places (NEW: THE CHAAT STALL at dusk; the morning worktop); every explanation = the white BOARD (a side-profile head with the HEAT SENSOR).
# METAPHOR: a fire alarm in your nose. Capsaicin trips the heat sensor -> the nose 'thinks it's on fire' -> it opens the taps (mucus) -> no fire: a false alarm.
# Craft skill (editing): the LOOP ENDING — the last line names the place of the first shot (the chaat stall), the tail shot rebuilds frame 0's composition
# and loop_seam() blends the last 0.33 s into frame 0, so the replay starts with no jump.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "when") - 0.1, "punch"),
    ("S1", T("i2", "Its") - 0.12, "erase"),
    ("S2", T("a1", "Chillies") - 0.12, "whip"),
    ("S3", T("a2", "And") - 0.1, "erase"), ("S4", T("a3", "Capsaicin") - 0.1, "cut"), ("S4b", T("a3", "so") - 0.1, "punch"),
    ("S5", T("a4", "So") - 0.1, "erase"), ("S5b", T("a4", "coming") - 0.12, "whip"),
    ("S6", T("b1", "Theres") - 0.1, "flash"),
    ("S7", T("b2", "It") - 0.1, "erase"),
    ("S8", T("b3", "Hot") - 0.1, "whip"),
    ("S9", T("b4", "It") - 0.1, "punch"), ("S9b", T("b4", "and") - 0.1, "erase"),
    ("S10", T("c1", "Send") - 0.1, "whip"),
    ("S11", LINES["c1"]["end"] + 0.12, "punch"), ("S12", LINES["c1"]["end"] + 0.85, "cut"),
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


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def kw(f, text, x, y, t, t0, mode="pop", size=130, col=None, **k):
    """kinetic word in hand lettering with an ink stroke (anim_fx.kin_word)."""
    kin_word(f, text, x, y, t, t0, mode, size, col or ACC_S, stroke=2, stroke_col=INKC, **k)


def el_at(f, el, x, y, s=1.0, t=None, t0=None, rot=0.0, op=1.0):
    """place an element; with t/t0 it snaps in (4-frame overshoot)."""
    k = 1.0 if t0 is None else (snap(t, t0, 4) if t >= t0 else 0.0)
    if k > 0.01: rot_comp(f, scale_el(el, s), x, y, rot, k, op, 0.0)


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    if k <= 0: return
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None):
    s = s * 1.7
    chub_head_only(f, x, y, s, t, mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5)


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (already on screen at frame 0)."""
    kw(f, "DO YOU KNOW WHY", 540, 320, t, t0, "pop", 74, col=INKC, op=op)
    kw(f, "SPICY FOOD", 540, 440, t, t0, "shake", 132, col=ACC, amp=0.45, op=op)
    kw(f, "= RUNNY NOSE?", 540, 580, t, t0, "pop", 112, col=MUC_S, op=op)


STALL_X, STALL_Y, STALL_S = 540, 1520, 1.38
CART = 1360


def stall_chubby(f, t, k_spice=1.0, expr="n", brow="n", look=(0.2, -0.1), mouth=None, drip_amt=1.0, drip_t0=-0.6, lean=0.0, dy=0.0, squash=0.0):
    """Chubby behind the pani-puri cart, a golgappa at his mouth, cheeks flushed, a drip from his nose."""
    x, y, s = STALL_X, STALL_Y + dy, STALL_S
    chub(f, x, y, s, t=t, la=(26, 14), ra=(140, -128), hold=scale_el(golgappa_el(bite=True), 0.62), hold_off=(-6, -40), hold_front=True,
         mouth=mouth if mouth is not None else talk(t), expr=expr, brow=brow, look=look, lean=lean, squash=squash, hand_r="grip")
    flush(f, x, y, s, k_spice, t, lean)
    nx, ny = nose_xy(x, y, s, t, lean, squash)
    drip(f, nx, ny, s, t, drip_t0, 1.5, drip_amt)
    return nx, ny


# ---- S0: HOOK at frame 0: the chaat stall at dusk, Chubby mid-golgappa, already flushed, a drip already swelling; the question on screen ----
def shot_S0(t, n):
    f = set_chaat(t); kr = T("i1", "runs") - 0.15; k = take(t, kr)
    pre = t <= kr
    stall_chubby(f, t, 1.0, expr="n" if pre else k["expr"], brow="sad" if pre else k["brow"], look=(0.1, 0.5) if pre else k["look"],
                 dy=k["dy"], squash=k["squash"], lean=k["lean"], drip_amt=1.0 + 0.3 * ramp(t, kr, 0.3), drip_t0=-1.0)
    cart_front(f, CART)
    el_at(f, puri_stack_el(), 880, 1320, 0.9); el_at(f, matka_el(), 190, 1275, 0.95)
    hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S0b: '...when you eat spicy food?' CLOSE-UP: cheeks burning, the drip lets go; a tissue box slides in ----
def shot_S0b(t, n):
    f = set_chaat(t, blur=8); t0 = st_("S0b"); ts = T("i1", "spicy") - 0.2
    hx, hy, s = 540, 1080, 2.5
    chub_head_only(f, hx, hy, s, t, mouth="jaw" if t > ts else talk(t), expr="gross" if t > ts else "n", brow="sad", look=(0, 0.3))
    for sg in (-1, 1): glow(f, hx + sg * 56 * s, hy + 44 * s, 34 * s, (240, 70, 60), 0.35)
    heat_lines(f, hx, hy - 250, 1.4, t, 1.0)
    drip(f, hx + 8 * s, hy + 41 * s, s * 0.8, t, t0 - 0.9, 1.3, 1.0)
    q = ramp(t, ts, 0.35); el_at(f, tissue_box_el(), 1150 - 290 * q, 1330, 1.0)
    hook_words(f, t)
    return finish(f, n, look="golden")


# ---- S1: 'It's not a cold, and it's not an allergy either.' BOARD: a cold? (a germ) vs allergy? (a pollen flower); both crossed out ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tc = T("i2", "cold") - 0.1; ta = T("i2", "allergy") - 0.1
    draw_on(f, [(540, 700), (540, 1260)], ramp(t, t0, 0.3), BP_INK, 5, seed=3, tip=False)
    el_at(f, germ_el("n"), 300, 900, 1.25, t, t0 + 0.05)
    write_on(f, "a cold?", 300, 1200, t, t0 + 0.15, 54, BP_INK)
    stamp_x(f, 300, 940, 170, snap(t, tc + 0.2, 3) if t > tc + 0.2 else 0)
    el_at(f, flower_ink_el(), 780, 900, 1.15, t, ta - 0.6)
    write_on(f, "allergy?", 780, 1200, t, ta - 0.5, 54, BP_INK)
    stamp_x(f, 780, 940, 170, snap(t, ta + 0.25, 3) if t > ta + 0.25 else 0)
    kw(f, "NOPE.", 540, 420, t, tc + 0.25, "shake", 120, col=(176, 40, 44), amp=0.4)
    peek(f, t, 540, 1430, 0.6, expr="sus", look=(0, -0.4))
    return finish(f, n, look="fresh")


# ---- S2: 'Chillies have capsaicin, the stuff that makes them taste hot.' the stall, a big green chilli; little red flame buddies pop out of it ----
def shot_S2(t, n):
    f = set_chaat(t, blur=8); t0 = st_("S2"); tc = T("a1", "capsaicin") - 0.15; th = T("a1", "hot") - 0.2
    f = dof(f, 2)
    cart_front(f, CART)
    el_at(f, food_el("chilli", "n", (0.3, 0)), 540, 1060, 2.1, t, t0 + 0.02, rot=-18)
    if t > tc:
        for i, (dx, dy) in enumerate(((-280, -200), (250, -280), (-330, -420), (300, -20))):
            q = snap(t, tc + 0.12 * i, 5) if t > tc + 0.12 * i else 0
            if q > 0:
                el_at(f, caps_el("happy", (0, 0), 1.0 + 0.2 * math.sin(t * 9 + i)), 540 + dx * q, 980 + dy * q + 10 * math.sin(t * 7 + i), 0.75)
        write_on(f, "capsaicin", 540, 330, t, tc + 0.05, 70, ACC_S)
    if t > th:
        heat_lines(f, 540, 820, 1.6, t, ramp(t, th, 0.3), 4)
        kw(f, "HOT!", 540, 490, t, th, "shake", 140, col=ACC, amp=0.6)
    src(f, SRC_CC, t, t0 + 0.4)
    return finish(f, n, look="golden")


# ---- the BOARD head: a big side profile facing right, the nasal passage, the nerve up to a HEAT SENSOR (a fire-alarm bell) ----
PROFILE = [(470, 470), (560, 500), (612, 560), (630, 640), (650, 700), (700, 790), (740, 860), (706, 880), (660, 884), (668, 930), (650, 960),
           (672, 1000), (650, 1040), (620, 1090), (560, 1130), (470, 1150), (470, 1240)]
BACK = [(470, 470), (380, 470), (290, 520), (230, 620), (210, 760), (230, 900), (280, 1010), (330, 1080), (330, 1240)]
CAVITY = [(690, 866), (640, 836), (560, 790), (500, 770), (470, 800), (520, 840), (600, 870), (660, 882)]
NERVE = [(540, 785), (530, 745), (505, 712), (480, 670), (440, 630), (400, 600)]
BELL = (330, 560)


def board_head(f, t, t0, kd=None, nerve_t=None, bell_t=None, lit=False):
    k = ramp(t, t0, 0.55) if kd is None else kd
    draw_on(f, BACK, k, BP_INK, 7, seed=22, tip=False)
    draw_on(f, PROFILE, k, BP_INK, 7, seed=23)
    if k > 0.6:
        q = clamp((k - 0.6) / 0.4)
        cv2.fillPoly(f, [np.array(CAVITY, np.int32)], C(_mix((255, 255, 255), MUC, q)), cv2.LINE_AA)
        draw_on(f, CAVITY, q, MUC_S, 5, seed=24, tip=False, closed=True)
    if nerve_t is not None and t > nerve_t:
        draw_on(f, NERVE, ramp(t, nerve_t, 0.45), ACC if lit else ACC_S, 11, seed=25)
        if bell_t is not None and t > bell_t:
            rg = math.sin(t * 46) * 6 if lit else 0
            if lit: glow(f, BELL[0], BELL[1], 150, (255, 120, 90), 0.25)
            el_at(f, bell_el(lit=lit), BELL[0] + rg, BELL[1], 0.85, t, bell_t)
            if lit:
                for j in range(3):
                    r0 = 95 + 14 * math.sin(t * 20 + j); a = math.radians(-30 + 30 * j)
                    for sg in (-1, 1):
                        p0 = (BELL[0] + sg * r0 * math.cos(a), BELL[1] - r0 * math.sin(a)); p1 = (BELL[0] + sg * (r0 + 40) * math.cos(a), BELL[1] - (r0 + 40) * math.sin(a))
                        cv2.line(f, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), C(ACC), 7, cv2.LINE_AA)


# ---- S3: 'And inside your nose, there's a nerve that senses heat.' BOARD: the head draws on, the passage, the nerve, the HEAT SENSOR bell ----
def shot_S3(t, n):
    f = board_bg(); t0 = st_("S3"); tn = T("a2", "nerve") - 0.2; th = T("a2", "heat") - 0.25; tno = T("a2", "nose") - 0.1
    board_head(f, t, t0, nerve_t=tn, bell_t=tn + 0.35)
    write_on(f, "your nose", 830, 1010, t, tno, 50, BP_INK)
    draw_arrow_on(f, (790, 960), (720, 885), ramp(t, tno + 0.1, 0.3), BP_INK, 5, 18)
    write_on(f, "heat sensor", 330, 380, t, th, 56, ACC_S)
    if t > th: cv2.circle(f, (int(BELL[0]), int(BELL[1])), int(84 + 8 * math.sin(t * 6)), C(ACC_L), 5, cv2.LINE_AA)
    return finish(f, n, look="fresh")


# ---- S4: 'Capsaicin trips that same nerve,' the flame buddy slides up the passage and taps the nerve: the bell lights and rings ----
def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); tt = T("a3", "trips") - 0.05
    lit = t > tt + 0.15
    board_head(f, t, t0, kd=1.0, nerve_t=t0 - 1, bell_t=t0 - 1, lit=lit)
    write_on(f, "heat sensor", 330, 380, 99, 0, 56, ACC_S)
    q = ramp(t, t0, max(0.2, tt - t0))
    px, py = 860 + (580 - 860) * q, 1010 + (810 - 1010) * q
    el_at(f, caps_el("smirk" if not lit else "happy", (-1, -0.3), 1.0 + 0.2 * math.sin(t * 10)), px, py - 40, 0.55)
    write_on(f, "capsaicin", 840, 1150, t, t0 + 0.05, 50, ACC_S)
    if lit:
        kw(f, "ALARM!", 540, 1340, t, tt + 0.15, "shake", 120, col=ACC, amp=0.7)
        mood(f, (255, 60, 50), 0.18 + 0.08 * math.sin(t * 20))
    return finish(f, n, look="fresh")


# ---- S4b: '...so your nose thinks it's on fire.' the stall: a take, cartoon flames lick up round his head, ON FIRE! ----
def flames_ring(f, x, y, s, t, k):
    if k <= 0.02: return
    for i in range(7):
        a = math.pi * (0.08 + 0.84 * i / 6); fx = x + math.cos(a) * 175 * s; fy = y - math.sin(a) * 150 * s + 30 * s
        el_at(f, caps_el(None, k=1.0 + 0.4 * math.sin(t * 13 + i * 1.3)), fx, fy, 0.5 * s * k)


def shot_S4b(t, n):
    f = set_chaat(t); t0 = st_("S4b"); tf = T("a3", "fire") - 0.25; k = take(t, tf); pre = t <= tf
    mood(f, (255, 90, 40), 0.25 * ramp(t, tf, 0.3))
    x, y, s = STALL_X, STALL_Y, STALL_S
    chub(f, x, y + k["dy"], s, t=t, **nolean(POSE["shock"]), mouth=talk(t) if pre else "jaw", expr="gross" if pre else k["expr"],
         brow="sad" if pre else k["brow"], look=(0, -0.5), lean=k["lean"], squash=k["squash"])
    flush(f, x, y + k["dy"], s, 1.0, t, k["lean"])
    flames_ring(f, x, y - 436 * s + k["dy"], s, t, ramp(t, tf, 0.25))
    nx, ny = nose_xy(x, y + k["dy"], s, t, k["lean"], k["squash"]); drip(f, nx, ny, s, t, t0 - 0.4, 1.2, 1.2)
    cart_front(f, CART)
    f = crash_zoom(f, t, tf, 1.15, 540, 900)
    kw(f, "ON FIRE!", 540, 400, t, tf, "shake", 150, col=ACC, amp=0.8)
    return finish(f, n, look="golden")


# ---- S5: 'So it opens the taps. Mucus, coming right up.' BOARD: a tap at the nostril turns, mucus pours ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); to = T("a4", "opens") - 0.1; tm = T("a4", "Mucus") - 0.15
    board_head(f, t, t0, kd=1.0, nerve_t=t0 - 1, bell_t=t0 - 1, lit=True)
    ok = ramp(t, to, 0.35)
    el_at(f, tap_el(ok), 800, 900, 0.75)
    if ok > 0.5:
        L = 420 * ramp(t, to + 0.2, 0.8); x0, y0 = 873, 950
        P = [(x0 + 4 * math.sin(t * 9 + v * 5), y0 + v * L) for v in np.linspace(0, 1, 10)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C(MUC_S), 44, cv2.LINE_AA)
        cv2.polylines(f, [np.array(P, np.int32)], False, C(MUC), 34, cv2.LINE_AA)
        if L > 380:
            for j in range(5):
                u = ((t - to) * 1.4 + j / 5) % 1; yy = y0 + L + u * 120; xx = x0 + 10 * math.sin(j * 3)
                cv2.circle(f, (int(xx), int(yy)), 20, C(MUC), -1, cv2.LINE_AA); cv2.circle(f, (int(xx), int(yy)), 20, C(MUC_S), 5, cv2.LINE_AA)
    write_on(f, "mucus", 700, 1440, t, tm, 66, MUC_S)
    write_on(f, "open the taps", 600, 360, t, to - 0.05, 60, BP_INK)
    return finish(f, n, look="fresh")


# ---- S5b: '...coming right up.' the stall: Chubby yanks tissue after tissue out of the box, they fly on arcs ----
def shot_S5b(t, n):
    f = set_chaat(t); t0 = st_("S5b")
    x, y, s = 420, STALL_Y, STALL_S
    pull = (t - t0) / 0.32; ph = pull % 1
    chub(f, x, y, s, t=t, la=(30, 14), ra=(60 + 60 * ph, 30 + 90 * ph), mouth=talk(t), expr="gross", brow="sad", look=(0.8, 0.2), turn=0.5, hand_r="pinch")
    flush(f, x, y, s, 0.8, t)
    nx, ny = nose_xy(x, y, s, t); drip(f, nx, ny, s, t, t0 - 0.5, 1.0, 1.3); drip(f, nx - 18 * s, ny, s, t, t0 - 0.2, 1.1, 0.9, seed=2, side=-1)
    cart_front(f, CART)
    el_at(f, tissue_box_el(), 820, 1290, 1.0)
    for j in range(int(pull) + 1):                                              # every pull launches a tissue on an arc
        u = (t - t0 - j * 0.32) / 0.9
        if 0 < u < 1:
            tx = 800 - 60 * u + 260 * math.sin(j * 2.1) * u; ty = 1120 - 700 * u + 900 * u * u
            el_at(f, tissue_el(345 + j % 3), tx, ty, 0.8, rot=360 * u * (1 if j % 2 else -1))
    kw(f, "COMING RIGHT UP", 540, 380, t, t0 + 0.05, "pop", 96, col=INKC)
    return finish(f, n, look="golden")


# ---- S6: 'There's no real fire, it's just a false alarm.' lights down: Chubby in a fire helmet with an extinguisher looks left, right... nothing. FALSE ALARM ----
def shot_S6(t, n):
    t0 = st_("S6"); tfa = T("b1", "false") - 0.2
    f = set_chaat(t, dim=0.35 * (1 - ramp(t, tfa, 0.3)))
    e = eye_lead(t, t0 + 0.3, -1.0, 1.0) if t < tfa - 0.2 else eye_lead(t, tfa - 0.2, 1.0, 0.0)
    x, y, s = 540, STALL_Y, STALL_S
    chub(f, x, y, s, t=t, la=(60, 80), ra=(40, 60), mouth=talk(t), expr="sus" if t < tfa else "n", brow="sus" if t < tfa else "up", look=e["look"], turn=e["turn"], lean=e["lean"],
         hold=scale_el(ext_el(), 0.75), hold_off=(-20, -30), hold_front=True, hand_r="grip")
    el_at(f, helmet_el(), x, y - 436 * s - 70 * s + 4.5 * s * math.sin(t * 2.4), 0.82 * s)
    cart_front(f, CART)
    el_at(f, bell_el(lit=True), 900, 640 + 4 * math.sin(t * 40), 0.8)
    if t > tfa:
        q = snap(t, tfa, 3)
        rot_comp(f, scale_el(vstamp_el("FALSE ALARM", (176, 40, 44), 84), 1.0), 540, 470, -8, 1.6 - 0.6 * q, 1.0, 0.3)
    else:
        kw(f, "FIRE?", 540, 450, t, t0 + 0.05, "pop", 130, col=ACC)
    return finish(f, n, look="night" if t < tfa else "golden")


# ---- S7: 'It even has a name, gustatory rhinitis. Big name, runny nose.' BOARD: the name writes itself, each half defined; then a tiny runny nose ----
def shot_S7(t, n):
    f = board_bg(); tg = T("b2", "gustatory") - 0.15; tr = T("b2", "rhinitis") - 0.1; tb = T("b2", "Big") - 0.15; tn = T("b2", "runny") - 0.15
    sc = 1.0 + 0.2 * ramp(t, tb, 0.25) * (1 - ramp(t, tn, 0.3))
    write_on(f, "gustatory", 540, 540, t, tg, int(84 * sc), BP_INK, 30)
    write_on(f, "rhinitis", 540, 700, t, tr, int(84 * sc), ACC_S, 30)
    if tr + 0.4 < t < tn:
        write_on(f, "= when you eat", 540, 880, t, tr + 0.4, 46, BP_INK, 40)
        write_on(f, "= nose trouble", 540, 980, t, tr + 0.6, 46, BP_INK, 40)
    if t > tn:
        q = snap(t, tn, 5); hs = 1.9 * q
        if q > 0.05:
            chub_head_only(f, 540, 1010, hs, t, mouth="o", expr="gross", brow="sad", look=(0, 0.3))
            drip(f, 540 + 8 * hs, 1010 + 41 * hs, hs * 0.8, t, tn - 0.6, 1.1, 1.2)
        kw(f, "RUNNY NOSE", 540, 1330, t, tn, "pop", 104, col=INK_MINT_S)
    else:
        peek(f, t, 880, 1400, 0.55, expr="sus", look=(-0.5, -0.4))
    return finish(f, n, look="fresh")


# ---- S8: 'Hot soup can set it off too.' the morning worktop: a steaming bowl of soup, a spoonful, the drip starts again ----
def shot_S8(t, n):
    f = set_worktop(t); t0 = st_("S8"); ts = T("b3", "set") - 0.2
    x, y, s = 400, 1500, 1.05
    chub(f, x, y, s, t=t, la=(26, 14), ra=(130, -110), hold=scale_el(spoon_el(), 0.5), hold_front=True, mouth=talk(t),
         expr="happy" if t < ts else "gross", brow="up" if t < ts else "sad", look=(0.6, 0.4), turn=0.4, hand_r="grip")
    nx, ny = nose_xy(x, y, s, t); drip(f, nx, ny, s, t, ts, 1.2, ramp(t, ts, 0.4))
    worktop_front(f, 1330)
    el_at(f, bowl_soup_el(), 760, 1260, 1.05)
    steam_wisps(f, 740, 1190, t, 4, 240, 140, (255, 255, 255), 0.7)
    kw(f, "HOT SOUP", 540, 380, t, t0 + 0.05, "pop", 120, col=ACC)
    kw(f, "TOO", 540, 520, t, ts, "shake", 110, col=INKC, amp=0.4)
    return finish(f, n, look="golden")


# ---- S9: 'It stops a few minutes after you finish eating,' the stall: a clock's minute hand sweeps, the drip shrinks and stops ----
def shot_S9(t, n):
    f = set_chaat(t); t0 = st_("S9"); tf = T("b4", "few") - 0.2; t1 = T("b4", "eating") + 0.2
    dry = 1 - ramp(t, tf + 0.2, t1 - tf)
    x, y, s = 400, STALL_Y, STALL_S
    chub(f, x, y, s, t=t, **nolean(POSE["idle"]), mouth=talk(t), expr="n" if dry > 0.3 else "happy", brow="n" if dry > 0.3 else "up", look=(0.7, -0.3), turn=0.4)
    flush(f, x, y, s, dry, t)
    nx, ny = nose_xy(x, y, s, t); drip(f, nx, ny, s, t, t0 - 0.6, 1.3, dry)
    cart_front(f, CART)
    el_at(f, plate_el(), 800, 1345, 0.7)
    cx, cy = 800, 860
    el_at(f, clock_ink_el(120), cx, cy, 1.0)
    clock_hands(f, cx, cy, 6 + 1.6 * ramp(t, tf, t1 - tf), 120, 1.0)
    ui_word(f, "it stops in", "A FEW [MINUTES]", 420, t, tf, col=INKC, acc=ACC_S, size=110, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S9b: '...and if it bugs you all the time, see a doctor.' BOARD: tissues on every meal, an arrow, a stethoscope ----
def shot_S9b(t, n):
    f = board_bg(); t0 = st_("S9b"); ta = T("b4", "all") - 0.15; td = T("b4", "doctor") - 0.25
    for i in range(5):
        x = 180 + i * 180
        draw_on(f, [(x - 70, 620), (x + 70, 620), (x + 70, 760), (x - 70, 760)], ramp(t, t0 + 0.06 * i, 0.3), BP_INK, 5, seed=40 + i, tip=False, closed=True)
        if t > ta + 0.08 * i: el_at(f, tissue_el(345 + i % 3, crumpled=True), x, 690, 0.65, t, ta + 0.08 * i)
    write_on(f, "every meal?", 540, 470, t, ta - 0.1, 58, BP_INK)
    draw_arrow_on(f, (540, 820), (540, 980), ramp(t, td - 0.4, 0.3), BP_INK, 7, 26)
    el_at(f, steth_el(), 540, 1150, 1.0, t, td)
    write_on(f, "see a doctor", 540, 1350, t, td + 0.1, 60, ACC_S)
    return finish(f, n, look="fresh")


# ---- S10: 'Send this to the friend who needs a tissue at every chaat stall.' the stall: a friend sniffs, Chubby hands over the tissue box ----
FRIEND = (236, 150, 110)


def shot_S10(t, n):
    f = set_chaat(t); t0 = st_("S10"); tt = T("c1", "tissue") - 0.25
    chub(f, 280, STALL_Y, 1.2, t=t, la=(26, 12), ra=(80, 70) if t > tt else (30, 14), mouth=talk(t), expr="happy", brow="up", look=(1, 0), turn=0.5)
    fx, fy, fs = 790, STALL_Y, 1.25
    chub(f, fx, fy, fs, t=t, shirt=FRIEND, la=(30, 14), ra=(140, -128), hold=scale_el(golgappa_el(), 0.55), hold_off=(-6, -40), hold_front=True,
         mouth="o", expr="gross", brow="sad", look=(-0.5, 0.2), turn=-0.4)
    dress(f, fx, fy, fs, "cousin")
    flush(f, fx, fy, fs, 1.0, t)
    nx, ny = nose_xy(fx, fy, fs, t); drip(f, nx, ny, fs, t, t0 - 0.5, 1.2, 1.2)
    cart_front(f, CART)
    q = ramp(t, tt, 0.35); el_at(f, tissue_box_el(), 430 + 140 * q, 1290 - 60 * q, 0.85)
    ui_word(f, "send this to the friend who needs a", "[TISSUE]", 420, t, T("c1", "Send") - 0.05, col=INKC, acc=INK_MINT_S, size=130, lead_col=INKC)
    return finish(f, n, look="golden")


# ---- S11: the logo beat (0.7 s) ----
def shot_S11(t, n):
    t0 = st_("S11"); f = set_chaat(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.3) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.15) / 0.2))
    return finish(f, n, look="golden")


# ---- S12: the LOOP TAIL: back at the stall exactly like frame 0 (Chubby, the next golgappa, a fresh drip); loop_seam blends into frame 0 ----
def shot_S12(t, n):
    f = set_chaat(t)
    stall_chubby(f, t, 1.0, expr="n", brow="sad", look=(0.1, 0.5), mouth=0, drip_amt=1.0, drip_t0=-1.0)
    cart_front(f, CART)
    el_at(f, puri_stack_el(), 880, 1320, 0.9); el_at(f, matka_el(), 190, 1275, 0.95)
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "runs") - 0.15, 0.3, 10), (T("i1", "spicy") - 0.2, 0.25, 8), (T("i2", "cold") + 0.1, 0.25, 8), (T("i2", "allergy") + 0.15, 0.3, 10),
           (T("a1", "capsaicin") - 0.1, 0.25, 8), (T("a1", "hot") - 0.2, 0.3, 10), (T("a2", "heat") - 0.25, 0.25, 8),
           (T("a3", "trips") + 0.1, 0.4, 14), (T("a3", "fire") - 0.25, 0.5, 18), (T("a4", "opens") - 0.1, 0.25, 8), (T("a4", "Mucus") - 0.15, 0.3, 10),
           (T("b1", "false") - 0.2, 0.45, 16), (T("b2", "Big") - 0.15, 0.25, 8), (T("b2", "runny") - 0.15, 0.25, 8), (T("b3", "set") - 0.2, 0.25, 8),
           (T("b4", "doctor") - 0.25, 0.25, 8), (T("c1", "tissue") - 0.25, 0.3, 10)]


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
