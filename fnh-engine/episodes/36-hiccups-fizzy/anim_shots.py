# ================= shots: FreshNestHub 36 — "Why do fizzy drinks give you hiccups?" (Chubby INK; 35-50 s rule; ONE takeaway) ===
# COLOUR SCRIPT: FIZZ AQUA (ACC) = the drink, the gas, the stomach balloon. Red = the irritated nerve / the diaphragm (alarm). Story = THE HOUSE PARTY (new
# place, warm evening living room); every explanation = the white BOARD. METAPHOR: the stomach blows up like a BALLOON right under the diaphragm (a dome you
# breathe with); the nerves trip; the dome jerks down, air rushes in, and the vocal cords SLAM shut like two DOORS = 'hic'.
# Craft skill (ep 36): INVOLUNTARY ACTION — hic() fires with NO anticipation (a reflex has no wind-up), a 2-frame jolt, a still hold, a settle that sinks
# below rest, and every repeat varies. Compare: take() (a surprise) HAS anticipation; a hiccup must not.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "after") - 0.1, "punch"),
    ("S1", T("i2", "It's") - 0.12, "erase"), ("S1b", T("i2", "It's", 1) - 0.1, "whip"),
    ("S2", T("a1", "Right") - 0.12, "erase"), ("S2b", T("a1", "It") - 0.1, "cut"),
    ("S3", T("a2", "A") - 0.1, "whip"), ("S3b", T("a2", "so") - 0.1, "erase"),
    ("S4", T("a3", "The") - 0.1, "cut"), ("S4b", T("a3", "and") - 0.1, "cut"),
    ("S5", T("a4", "and") - 0.1, "erase"), ("S5b", T("a4", "Hic") - 0.12, "punch"),
    ("S6", T("b1", "Most") - 0.1, "whip"), ("S6b", T("b1", "If") - 0.1, "erase"),
    ("S7", T("c1", "Weird") - 0.1, "erase"),
    ("S8", T("c2", "Send") - 0.1, "whip"),
    ("S9", LINES["c2"]["end"] + 0.12, "punch"), ("S10", LINES["c2"]["end"] + 0.85, "cut"),
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


def stamp_x(f, x, y, r, k, col=(176, 40, 44), w=22):
    if k <= 0: return
    for sg in (-1, 1): cv2.line(f, (int(x - r * k), int(y - sg * r * k)), (int(x + r * k), int(y + sg * r * k)), C(col), w, cv2.LINE_AA)


def peek(f, t, x, y, s, expr="sus", look=(0, 0), brow=None, mouth=None, hics=()):
    h = hic(t, hics)
    s = s * 1.7
    chub_head_only(f, x, y + h["dy"] * 0.6, s, t, mouth=h["mouth"] or (talk(t) if mouth is None else mouth), expr=h["expr"] or expr,
                   brow=h["brow"] or brow or ("sus" if expr == "sus" else "up"), look=look, turn=clamp(look[0]) * 0.5, hair=h["hair"])


# ---- the party cast ----
CX, CY, CS = 380, 1660, 1.3            # Chubby behind the party table (bigger, ep 34 lesson)
TOP = 1420
DOME_C = (190, 60, 70)
HIC0 = [T("i1", "hiccups") - 0.02, T("i1", "fizzy") + 0.25]
HIC1 = [T("i2", "stomach") + 0.45]
HIC_BIG = T("a4", "Hic") - 0.04
HIC6 = [T("b1", "Most") + 0.05]
HIC_BABY = [T("c1", "hiccupping") - 0.05, T("c1", "hiccupping") + 0.75, T("c1", "born") - 0.05]
HIC_FRIEND = [T("c2", "third") - 0.05, T("c2", "party") - 0.1]


def drinker(f, t, hics, x=CX, y=CY, s=CS, level=0.7, sip=1.0, expr="happy", brow="n", look=(0.3, -0.2), mouth=None, shirt=None, glass=True, la=(28, 14)):
    """Chubby (or a friend) with a fizzy glass in the right hand: sip 1 = glass at the mouth, 0 = held at chest; hics = hiccup times (involuntary jolts)."""
    h = hic(t, hics)
    ra = (150 - 70 * (1 - sip) + h["arm"], -128 + 150 * (1 - sip))          # sip 1 = glass at the mouth, 0 = at the chest
    la2 = (la[0] + h["arm"] * 0.8, la[1])
    gl = _rot_el(scale_el(fizzy_glass_el(level), 0.5), 32 * sip + 6 * h["k"]) if glass else None
    kw_ = dict(shirt=shirt) if shirt else {}
    chub(f, x, y + h["dy"], s, t=t, la=la2, ra=ra, hold=gl, hold_off=(-38 * sip - 6 * (1 - sip), -18 * sip - 24 * (1 - sip)), hold_front=True, hand_r="grip",
         mouth=h["mouth"] or (mouth if mouth is not None else (0 if sip > 0.5 else talk(t))), expr=h["expr"] or expr, brow=h["brow"] or brow,
         look=look, lean=h["lean"], squash=h["squash"], hair=h["hair"], turn=0.3, **kw_)
    if h["k"] > 0.3 and glass:                                                       # the drink splashes on the jolt
        rr = np.random.default_rng(int(h["k"] * 10))
        for j in range(6):
            a = -math.pi / 2 + rr.uniform(-0.9, 0.9); r_ = 40 + 50 * h["k"]
            gx = x + 100 * s; gy = y - 400 * s + h["dy"]
            cv2.circle(f, (int(gx + r_ * math.cos(a)), int(gy + r_ * math.sin(a))), int(7 * s), C(SODA_S), -1, cv2.LINE_AA)
    return h


def table_props(f, t, empties=0):
    el_at(f, soda_bottle_el(), 880, 1300, 0.8)
    el_at(f, chips_bowl_el(0.8), 710, 1390, 0.6)
    for j in range(empties): el_at(f, fizzy_glass_el(0.0), 560 + 70 * j, 1370, 0.42)


def hook_words(f, t, t0=-1.0, op=1.0):
    """the hook question as moving words (on screen at frame 0)."""
    kw(f, "DO YOU KNOW WHY", 540, 330, t, t0, "pop", 72, col=INKC, op=op)
    kw(f, "FIZZY DRINK", 540, 465, t, t0, "shake", 128, col=ACC_S, amp=0.3, op=op)
    kw(f, "= HICCUPS?", 540, 610, t, t0, "shake", 128, col=DOME_C, amp=0.5, op=op)


def dome_hatch(f, drop=0.0, bulge=0.0, k=1.0):
    hatch_on(f, dome_pts(drop, bulge) + [(880, 1040), (200, 1040)], k, DOME_C, gap=14, w=3)


# ---- S0: HOOK at frame 0: the party, Chubby already mid-gulp with a fizzy glass, the question on screen; the first HIC jolts him on 'hiccups' ----
def shot_S0(t, n):
    f = set_party(t)
    drinker(f, t, HIC0, sip=1.0 if t < HIC0[0] - 0.3 else 0.35, expr="happy", look=(0.3, -0.3) if t < HIC0[0] else (0.6, 0.0))
    party_front(f, TOP); table_props(f, t)
    hic_word(f, t, HIC0, CX + 200, CY - 600 * CS, 110, ACC_S)
    hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S0b: '...after a fizzy drink?' close-up: the glass fizzing at his face; a second HIC (different: bigger, head the other way) ----
def shot_S0b(t, n):
    f = set_party(t, blur=9); f = dof(f, 3)
    h = hic(t, HIC0[1:], 1.15)
    hx, hy = 470, 1060 + h["dy"] * 1.6
    chub_head_only(f, hx, hy, 2.5, t, mouth=h["mouth"] or 0, expr=h["expr"] or "sus", brow=h["brow"] or "sus", look=(0.7, 0.3), hair=(h["hair"][0], h["hair"][1] * 1.6), turn=0.3)
    gx, gy = 790, 1260 + h["dy"] * 0.8                                                # the glass in his fist, right of his face
    rot_comp(f, scale_el(fizzy_glass_el(0.6), 1.25), gx, gy, 4 + 6 * h["k"], 1.0, 1.0, 0.0)
    grip_hand(f, gx - 10, gy + 60, 1.9, kind="grip")
    for j in range(10):                                                               # bubbles rising off the glass
        u = (t * 1.2 + j / 10) % 1
        cv2.circle(f, (int(gx + 40 * math.sin(j * 3 + t * 4)), int(gy - 200 - 380 * u)), int(6 + 8 * (1 - u)), C(ACC_S), 3, cv2.LINE_AA)
    if h["k"] > 0.3:
        for j in range(7):
            a = -math.pi / 2 + (j - 3) * 0.25; r_ = 60 + 90 * h["k"]
            cv2.circle(f, (int(gx + r_ * math.cos(a)), int(gy - 200 + r_ * math.sin(a))), 12, C(SODA_S), -1, cv2.LINE_AA)
    hic_word(f, t, HIC0[1:], 250, 1380, 130, ACC_S)
    hook_words(f, t)
    return finish(f, n, look="warm")


# ---- S1: 'It's not the bubbles tickling your throat.' BOARD: a throat tube with bubbles tickling down it, then crossed out ----
def shot_S1(t, n):
    f = board_bg(); t0 = st_("S1"); tb = T("i2", "bubbles") - 0.1; tt = T("i2", "throat") - 0.1
    k = ramp(t, t0, 0.4)
    draw_on(f, [(430, 380), (430, 1320)], k, BP_INK, 9, seed=11, tip=False); draw_on(f, [(650, 380), (650, 1320)], k, BP_INK, 9, seed=12, tip=False)
    write_on(f, "your throat", 540, 300, t, t0 + 0.1, 46, BP_INK)
    if t > tb:
        for j in range(9):
            u = ((t - tb) * 0.5 + j / 9) % 1
            x = 540 + 70 * math.sin(j * 2.1 + u * 6); y = 420 + 880 * u
            cv2.circle(f, (int(x), int(y)), 22, C(ACC_XL), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y)), 22, C(ACC_S), 4, cv2.LINE_AA)
            if j % 3 == 0:                                                              # tickle marks
                for s_ in (-1, 1): cv2.line(f, (int(x + s_ * 34), int(y - 6)), (int(x + s_ * 52), int(y - 14)), C(ACC_S), 3, cv2.LINE_AA)
        kw(f, "THE BUBBLES?", 540, 1440, t, tb, "shake", 92, col=ACC_S, amp=0.4)
    stamp_x(f, 540, 850, 300, snap(t, tt, 3) if t > tt else 0)
    peek(f, t, 860, 1200, 0.5, expr="sus", look=(-0.6, -0.3))
    return finish(f, n, look="fresh")


# ---- S1b: '...It's your stomach.' the party: Chubby, hand on his belly, deadpan; an x-ray window shows the stomach; another hic jolts him ----
def x_belly(f, t, x, y, s, r_st, k=1.0, rr=118):
    """an x-ray window over Chubby's belly, drawn in the BOARD language (paper, blue ink): the red dome on top, the stomach as an aqua balloon
    with gas bubbles under it (it grows with r_st)."""
    cx, cy = x + 10 * s, y - 230 * s; R = rr * s / 1.1
    def draw(g):
        cv2.circle(g, (int(cx), int(cy)), int(R + 4), C(BP_PAPER), -1, cv2.LINE_AA)
        D = [(cx - R + 10 + (2 * R - 20) * u, cy - R * 0.45 - R * 0.28 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 24)]
        cv2.polylines(g, [np.int32(D)], False, C(DOME_C), 9, cv2.LINE_AA)
        sr = r_st * s / 1.1; sy = cy - R * 0.45 + sr + 10
        P = _arcpts(cx + 8, sy, sr * 1.15, sr, 0, 360, 36)[:-1]
        cv2.fillPoly(g, [np.array(P, np.int32)], C(ACC_XL), cv2.LINE_AA)
        hatch_on(g, P, 1.0, ACC, gap=14, w=3)
        cv2.polylines(g, [np.array(P, np.int32)], True, C(ACC_S), 6, cv2.LINE_AA)
        for j in range(int(r_st / 8)):
            u = (t * 0.8 + j * 0.37) % 1; a = j * 2.4
            bx = cx + 8 + 0.7 * sr * math.cos(a); by = sy + sr * 0.8 - 1.5 * sr * u
            cv2.circle(g, (int(bx), int(max(sy - sr + 8, by))), 6 + j % 4, C(ACC_S), 2, cv2.LINE_AA)
    inset(f, cx, cy, R, draw, k, ring=ACC_L, th=8)


def shot_S1b(t, n):
    f = set_party(t); ts = T("i2", "stomach") - 0.15
    h = hic(t, HIC1)
    chub(f, CX, CY + h["dy"], CS, t=t, la=(26 + h["arm"], -112), ra=(70 + h["arm"], 40), mouth=h["mouth"] or talk(t), expr=h["expr"] or "n", brow=h["brow"] or "n",
         look=(0.4, -0.1), lean=h["lean"], squash=h["squash"], hair=h["hair"], turn=0.2)
    x_belly(f, t, CX, CY + h["dy"], CS, 52, snap(t, ts, 4) if t > ts else 0.0)
    party_front(f, TOP); table_props(f, t)
    if t > ts: kw(f, "YOUR STOMACH.", 540, 420, t, ts, "drop", 104, col=INKC, t1=ts + 1.4)
    hic_word(f, t, HIC1, CX + 200, CY - 600 * CS, 100, ACC_S)
    return finish(f, n, look="warm")


# ---- S2: 'Right under your lungs sits a dome of muscle, your diaphragm.' BOARD: the body draws on, lungs on 'lungs', the dome on 'dome' ----
def shot_S2(t, n):
    f = board_bg(); t0 = st_("S2"); tl = T("a1", "lungs") - 0.2; td = T("a1", "dome") - 0.15; tdi = T("a1", "diaphragm") - 0.15
    k = clamp(ramp(t, t0, 0.5) * 0.3 + (0.3 * ramp(t, tl, 0.4) if t > tl else 0) + (0.4 * ramp(t, td, 0.5) if t > td else 0))
    board_torso(f, t, t0, k=k)
    if t > tl: write_on(f, "lungs", 300, 560, t, tl + 0.2, 46, BP_INK)
    if t > tdi:
        dome_hatch(f, k=ramp(t, tdi, 0.4))
        write_on(f, "diaphragm", 540, 1110, t, tdi, 60, DOME_C)
    peek(f, t, 880, 1440, 0.42, expr="sus", look=(-0.6, -0.5))
    return finish(f, n, look="fresh")


# ---- S2b: 'It pulls down every time you breathe in.' BOARD: the dome breathes (down = in), lungs swell, air arrow in ----
def breath(t, t0, period=1.5): return 0.5 - 0.5 * math.cos(2 * math.pi * max(0.0, t - t0) / period)


def shot_S2b(t, n):
    f = board_bg(); t0 = st_("S2b"); tp = T("a1", "pulls") - 0.1
    b = breath(t, tp)
    board_torso(f, t, t0, k=1.0, lung_k=b, drop=0.5 * b)
    dome_hatch(f, 0.5 * b)
    write_on(f, "diaphragm", 540, 1110, 99, 0, 60, DOME_C)
    if t > tp:
        draw_arrow_on(f, (540, 260), (540, 420), 0.3 + 0.7 * b, ACC_S, 8, 30)
        for x in (330, 750): draw_arrow_on(f, (x, 870), (x, 990), 0.3 + 0.7 * b, DOME_C, 7, 26)
        kw(f, "DOWN = BREATHE IN", 540, 1290, t, tp, "breathe", 74, col=BP_INK)
    peek(f, t, 880, 1440, 0.42, expr="n", look=(-0.6, -0.5), mouth="o" if b > 0.6 else 0)
    return finish(f, n, look="fresh")


# ---- S3: 'A fizzy drink fills your stomach with gas,' the party: Chubby chugs; the x-ray window: the stomach fills with gas bubbles ----
def shot_S3(t, n):
    f = set_party(t); t0 = st_("S3"); tg = T("a2", "gas") - 0.15
    drinker(f, t, [], sip=1.0, level=max(0.15, 0.8 - 0.4 * ramp(t, t0, 2.0)), expr="happy", look=(0.2, -0.4))
    x_belly(f, t, CX, CY, CS, 46 + 26 * ramp(t, t0 + 0.3, 1.8), snap(t, t0 + 0.2, 4) if t > t0 + 0.2 else 0)
    party_front(f, TOP); table_props(f, t)
    if t > tg: kw(f, "GAS", 540, 470, t, tg, "breathe", 190, col=ACC_S)
    return finish(f, n, look="warm")


# ---- S3b: '...so it stretches fast, like a balloon, right under your diaphragm.' BOARD: the stomach balloon inflates up into the dome ----
def shot_S3b(t, n):
    f = board_bg(); t0 = st_("S3b"); tst = T("a2", "stretches") - 0.1; tb = T("a2", "balloon") - 0.15; tu = T("a2", "right") - 0.1
    r = 50 + 100 * ramp(t, tst, max(0.3, tb - tst + 0.3))
    bul = ramp(t, tu, 0.5)
    board_torso(f, t, t0, k=1.0, st_r=r, bulge=bul)
    dome_hatch(f, 0, bul)
    write_on(f, "stomach", 880, 1430, t, t0 + 0.1, 44, ACC_S)
    if t > tb: kw(f, "LIKE A BALLOON", 540, 290, t, tb, "breathe", 92, col=ACC_S)
    if t > tu: draw_arrow_on(f, (560, 1240), (640, 960), ramp(t, tu, 0.3), ACC_S, 7, 26)
    return finish(f, n, look="fresh")


# ---- S4: 'The nerves there get irritated,' BOARD: the nerve draws up the body, turns red, alarm pulses run up it ----
def shot_S4(t, n):
    f = board_bg(); t0 = st_("S4"); ti = T("a3", "irritated") - 0.15
    nk = ramp(t, t0, 0.6)
    board_torso(f, t, t0, k=1.0, st_r=150, bulge=1.0, nerve_k=nk, nerve_t=ti)
    write_on(f, "nerve", 200, 690, t, t0 + 0.3, 46, NERVE)
    if t > ti:
        kw(f, "IRRITATED!", 540, 290, t, ti, "shake", 116, col=NERVE, amp=0.6)
        for j in range(5):                                                              # alarm sparks on the dome
            x = 300 + 120 * j; y = 880 + 10 * math.sin(t * 20 + j)
            cv2.line(f, (x, int(y)), (x + 14, int(y - 22)), C(NERVE), 4, cv2.LINE_AA)
    return finish(f, n, look="fresh")


# ---- S4b: '...and your diaphragm jerks down. Air rushes in,' BOARD: the dome SNAPS down in 2 frames (no anticipation), air rushes down the pipe ----
def shot_S4b(t, n):
    f = board_bg(); t0 = st_("S4b"); tj = T("a3", "jerks") - 0.08; ta = T("a3", "Air") - 0.1
    q = (t - tj) * FPS
    drop = 0.0 if q < 0 else (eo(min(1.0, q / 2)) if q < 2 else 1.0 + 0.08 * math.sin(q * 1.3) * math.exp(-q / 6))
    board_torso(f, t, t0, k=1.0, st_r=150, drop=drop, nerve_k=1.0)
    dome_hatch(f, drop)
    if t > tj: kw(f, "JERK!", 540, 1290, t, tj, "shake", 110, col=DOME_C, amp=0.7)
    if t > ta:
        for j, dx in enumerate((-10, 10, 0)):
            u = ((t - ta) * 2.2 + j / 3) % 1
            y0 = 250 + 330 * u
            draw_arrow_on(f, (TX + dx, y0), (TX + dx, y0 + 110), 1.0, ACC_S, 7, 24)
        kw(f, "AIR RUSHES IN", 540, 1420, t, ta, "pop", 76, col=ACC_S)
    return finish(f, n, look="fresh")


# ---- S5: '...and your vocal cords slam shut, like a door.' BOARD close-up: the windpipe with two vocal-cord DOORS; air flows; SLAM ----
def shot_S5(t, n):
    f = board_bg(); t0 = st_("S5"); tv = T("a4", "vocal") - 0.1; ts = T("a4", "slam") - 0.06; td = T("a4", "door") - 0.1
    q = (t - ts) * FPS
    shut = 0.0 if q < 0 else (eo(min(1.0, q / 2)) if q < 2 else 1.0)
    cord_doors(f, t, 540, 860, shut)
    if shut < 0.9:
        for j in range(3):
            u = ((t - t0) * 1.8 + j / 3) % 1
            draw_arrow_on(f, (540 + (j - 1) * 50, 400 + 300 * u), (540 + (j - 1) * 50, 500 + 300 * u), 1.0, ACC_S, 7, 24)
    if shut > 0.9:
        for j in range(8):                                                              # slam lines
            a = 2 * math.pi * j / 8; r0 = 60 + 120 * ramp(t, ts, 0.2)
            cv2.line(f, (int(540 + r0 * math.cos(a)), int(860 + r0 * math.sin(a))), (int(540 + (r0 + 40) * math.cos(a)), int(860 + (r0 + 40) * math.sin(a))), C(BP_INK), 6, cv2.LINE_AA)
        kw(f, "SLAM!", 540, 1290, t, ts, "shake", 140, col=DOME_C, amp=0.8)
    write_on(f, "vocal cords", 540, 300, t, tv, 56, BP_INK)
    write_on(f, "windpipe", 210, 1180, t, t0 + 0.15, 40, BP_INK)
    if t > td: write_on(f, "= a door", 810, 1180, t, td, 46, DOME_C)
    return finish(f, n, look="fresh")


# ---- S5b: 'Hic! That slam is the sound.' the party: the BIG hiccup (punch-in), HIC! bursts out; then a deadpan look to camera ----
def shot_S5b(t, n):
    f = set_party(t); tt = T("a4", "That") - 0.1
    drinker(f, t, [HIC_BIG], x=500, y=1760, s=1.6, sip=0.0, level=0.4, expr="n" if t > tt else "sus", brow="n", look=(0, 0) if t > tt else (0.3, -0.3))
    party_front(f, TOP + 90)
    if t > HIC_BIG: kw(f, "HIC!", 540, 450, t, HIC_BIG, "shake", 230, col=ACC_S, amp=0.9)
    if t > tt: kw(f, "= THE SLAM", 540, 640, t, tt, "pop", 96, col=INKC)
    return finish(f, n, look="warm")


# ---- S6: 'Most hiccups stop in a few minutes.' the party: the wall clock's minute hand sweeps; one last small hic, then relief ----
def shot_S6(t, n):
    f = set_party(t); t0 = st_("S6"); tm = T("b1", "minutes") - 0.15
    comp(f, clock_ink_el(90), 800, 820)
    clock_hands(f, 800, 820, 8.0 + 0.25 * clamp((t - t0) / 1.8), 90)
    h = hic(t, HIC6, 0.6)
    rel = ramp(t, tm, 0.4)
    chub(f, CX, CY + h["dy"], CS, t=t, la=(26, -112), ra=(30 + 120 * rel, 20 + 140 * rel), mouth=h["mouth"] or ("o" if 0 < t - tm < 0.6 else talk(t)),
         expr=h["expr"] or ("happy" if rel > 0.5 else "n"), brow=h["brow"] or "up", look=(0.6, -0.4), lean=h["lean"] - 4 * rel, squash=h["squash"], hair=h["hair"], turn=0.3)
    party_front(f, TOP); table_props(f, t)
    if t > tm: kw(f, "A FEW MINUTES", 540, 420, t, tm, "pop", 100, col=INKC)
    return finish(f, n, look="warm")


# ---- S6b: 'If they last more than two days, see a doctor.' BOARD: DAY 1, DAY 2 tick by, then an arrow to a stethoscope ----
def shot_S6b(t, n):
    f = board_bg(); t0 = st_("S6b"); tt = T("b1", "two") - 0.15; td = T("b1", "doctor") - 0.25
    for i, x in enumerate((340, 740)):
        ti = t0 + 0.2 if i == 0 else tt
        if t > ti:
            P = [(x - 150, 560), (x + 150, 560), (x + 150, 860), (x - 150, 860)]
            cv2.rectangle(f, (x - 150, 560), (x + 150, 625), C(_mix(NERVE, (255, 255, 255), 0.55)), -1, cv2.LINE_AA)
            draw_on(f, P, ramp(t, ti, 0.3), BP_INK, 7, seed=60 + i, tip=False, closed=True)
            write_on(f, f"DAY {i + 1}", x, 740, t, ti + 0.1, 56, BP_INK)
    if t > tt: write_on(f, "more than 2 days?", 540, 400, t, tt, 52, DOME_C)
    if t > td:
        draw_arrow_on(f, (540, 900), (540, 1040), ramp(t, td, 0.25), BP_INK, 8, 28)
        el_at(f, steth_el(), 330, 1180, 0.8, t, td + 0.1)
        write_on(f, "see a doctor", 660, 1180, t, td + 0.15, 50, BP_INK)
    src(f, SRC_CC, t, t0 + 0.4, 1440)
    return finish(f, n, look="fresh")


# ---- S7: 'Weird bonus: you were hiccupping in the womb, before you were even born.' BOARD: an ultrasound fan; a tiny baby hiccups inside ----
def shot_S7(t, n):
    f = board_bg(); t0 = st_("S7"); tw = T("c1", "womb") - 0.15
    ultrasound(f, t, 540, 1050, ramp(t, t0 + 0.1, 0.5), HIC_BABY)
    kw(f, "WEIRD BONUS", 540, 320, t, t0 + 0.05, "pop", 84, col=BP_INK)
    for ti in HIC_BABY:
        if 0 <= t - ti < 0.7: kw(f, "hic", 720 + 30 * (t - ti), 760 - 100 * (t - ti), t, ti, "pop", 70, col=ACC_L, stagger=0.02, op=clamp(1.4 - 2 * (t - ti)))
    if t > tw: kw(f, "IN THE WOMB", 540, 1250, t, tw, "pop", 100, col=ACC_S)
    write_on(f, "as early as 9 weeks", 540, 1370, t, tw + 0.5, 40, BP_INK)
    src(f, SRC_WOMB, t, t0 + 0.5, 1462)
    return finish(f, n, look="fresh")


# ---- S8: 'Send this to the friend on their third fizzy drink at this party.' the party: the friend with glass #3 hiccups; two empties; Chubby points ----
FRIEND = (236, 150, 110)


def shot_S8(t, n):
    f = set_party(t)
    chub(f, 250, 1650, 1.15, t=t, **POSE["point"], mouth=talk(t), expr="happy", brow="up", look=(1, 0), turn=0.5)
    drinker(f, t, HIC_FRIEND, x=750, y=1650, s=1.2, sip=0.55, level=0.8, expr="happy", look=(-0.6, -0.1), mouth=0, shirt=FRIEND)
    dress(f, 750, 1650, 1.2, "cousin")
    party_front(f, TOP); el_at(f, fizzy_glass_el(0.0), 470, 1370, 0.42); el_at(f, fizzy_glass_el(0.0), 545, 1380, 0.42); el_at(f, soda_bottle_el(), 940, 1300, 0.7)
    hic_word(f, t, HIC_FRIEND, 900, 1650 - 600 * 1.2, 100, ACC_S)
    ui_word(f, "send this to the friend on their", "[3RD] FIZZY DRINK", 420, t, T("c2", "Send") - 0.05, col=INKC, acc=ACC_S, size=92, lead_col=INKC)
    return finish(f, n, look="warm")


# ---- S9: the logo beat (0.7 s) ----
def shot_S9(t, n):
    t0 = st_("S9"); f = set_party(t); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
    comp(f, logo_el(), 540, 760, scale=pin(t, t0, 0.3) * 0.95)
    comp(f, ed_el("follow for more food facts", "", lead_col=INKC, lead_size=42), 540, 980, op=clamp((t - t0 - 0.15) / 0.2))
    return finish(f, n, look="golden")


# ---- S10: the LOOP TAIL: back at the party exactly like frame 0 (no caption); loop_seam blends into frame 0 ----
def shot_S10(t, n):
    f = set_party(t)
    drinker(f, t, [], sip=1.0, expr="happy", look=(0.3, -0.3))
    party_front(f, TOP); table_props(f, t)
    return finish(f, n, look="warm")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(HIC0[0], 0.25, 8), (HIC0[1], 0.3, 10), (T("i2", "throat") - 0.1, 0.3, 10), (T("i2", "stomach") - 0.15, 0.25, 8), (HIC1[0], 0.25, 8),
           (T("a1", "diaphragm") - 0.15, 0.25, 8), (T("a2", "gas") - 0.15, 0.25, 8), (T("a2", "balloon") - 0.15, 0.3, 10), (T("a3", "irritated") - 0.15, 0.3, 10),
           (T("a3", "jerks") - 0.08, 0.4, 16), (T("a4", "slam") - 0.06, 0.45, 18), (HIC_BIG, 0.5, 22), (T("b1", "doctor") - 0.25, 0.25, 8),
           (T("c1", "womb") - 0.15, 0.3, 10), (T("c2", "third") - 0.05, 0.25, 8)]


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
