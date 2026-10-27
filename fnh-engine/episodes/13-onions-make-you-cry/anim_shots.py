# ================= shots: FreshNestHub 13 — "Why do onions make you cry?" (the onion's booby trap) =================
# COLOUR SCRIPT (ep 13): warm KITCHEN sets (kitchen / yellow / cream / orange) = the everyday moment at your chopping board;
# ONION purple + pale cell green = inside the onion (the trap's rooms); sickly GAS green = the tear factor; TEAR blue = your
# eyes + tears; sky / steel = the scientists; back to warm kitchen for the takeaways.
# CRAFT (ep 13): progressive CHAIN MAP (anim_fx.chain_map) - the reaction CUT > MIX > ACID > GAS > NERVES > TEARS builds one
# link per shot at the bottom (past links dim, current ringed, future = empty slots) and lights up whole for the recap.
# Chubby really chops (2-bone IK grip + knife pivoting at the grip), slow-motion high-speed-camera look for the Cornell study.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "It's") - 0.15, "punch"), ("S1b", T("i2", "And") - 0.1, "zoom"),
    ("S2", T("i3", "Stick") - 0.15, "whip"),
    ("S3", T("a1", "Here's") - 0.2, "iris"), ("S4", T("a2", "Inside") - 0.2, "zoom"),
    ("S5", T("a3", "The") - 0.2, "whip"), ("S5b", T("a3", "Onions") - 0.15, "whip"),
    ("S6", T("a4", "The") - 0.2, "focus"), ("S6b", T("a5", "An") - 0.2, "whip"), ("S6c", T("a5", "It") - 0.1, "punch"),
    ("S7", T("a6", "As") - 0.2, "whip"),
    ("S8", T("b1", "But") - 0.2, "flash"), ("S9", T("b2", "The") - 0.2, "whip"),
    ("S10", T("b3", "First,") - 0.2, "whip"), ("S10b", T("b3", "into") - 0.1, "punch"),
    ("S11", T("b4", "That") - 0.2, "whip"), ("S11b", T("b4", "So") - 0.1, "zoom"),
    ("S12", T("b5", "and") - 0.15, "punch"), ("S12b", T("b5", "Scientists") - 0.15, "whip"),
    ("S13", T("b6", "The") - 0.2, "whip"), ("S14", T("b7", "Tiny") - 0.2, "iris"), ("S15", T("b8", "So") - 0.2, "whip"),
    ("S16", T("c1", "But") - 0.2, "focus"), ("S17", T("c2", "To") - 0.2, "whip"), ("S17b", T("c2", "To", 1) - 0.1, "whip"),
    ("S18", T("c3", "So") - 0.2, "zoom"),
    ("S19", T("d1", "Now,") - 0.2, "flash"), ("S20", T("d2", "In") - 0.2, "whip"), ("S20b", T("d2", "found") - 0.15, "punch"),
    ("S21", T("d3", "Then") - 0.2, "whip"), ("S21b", T("d3", "switched") - 0.15, "punch"), ("S22", T("d4", "They") - 0.2, "whip"),
    ("S23", T("e1", "So") - 0.2, "flash"), ("S24", T("e2", "Scientists") - 0.2, "whip"), ("S24b", T("e2", "super") - 0.1, "zoom"),
    ("S25", T("e3", "A") - 0.2, "whip"), ("S26", T("e4", "And") - 0.2, "punch"), ("S27", T("e5", "So") - 0.2, "whip"),
    ("S28", T("e6", "And") - 0.2, "whip"), ("S28b", T("e6", "The") - 0.1, "punch"),
    ("S29", T("f1", "Remember:") - 0.2, "focus"), ("S30", T("f2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
# iris match cuts: where the circle opens, in the PREVIOUS shot's picture (a round/central object)
IRIS = {"S3": (720, 1080), "S14": (330, 1060)}


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, acc=YEL_, size=170, y=470, out=None, tail=""):   # white caption on dark/colour sets
    ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.5, lead_col=WHITE, out=out, tail=tail)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / d))


def munch(t, rate=0.42):
    ph = (t / rate) % 1.0
    return (2 if ph < 0.5 else 0), int(t / rate)


def st_(sid): return SHOT[sid]["start"]


# ---------------- shared pieces ----------------
CHAIN = None


def chain_items():
    global CHAIN
    if CHAIN is None:
        CHAIN = [(scale_el(knife_el(), 0.5), "CUT"), (mix_icon_el(), "MIX"), (acid_icon_el(), "ACID"), (gas_el("sly"), "GAS"),
                 (sting_eye_el(), "NERVES"), (drop_el(), "TEARS")]
    return CHAIN


def chain(f, t, cur, t_cur, y=1395):
    chain_map(f, chain_items(), cur, t, t_cur, y=y, gap=146, r=48)


def chop_pose(t, t0, period=0.5, up=1140, down=1250, gx=560):
    """grip point for a vertical chop (fast down, slower up). returns (gx, gy, hit 0..1)."""
    if t < t0: return gx, up, 0.0
    ph = ((t - t0) % period) / period
    gy = up + (down - up) * (eo(ph / 0.35) if ph < 0.35 else 1 - eio((ph - 0.35) / 0.65))
    hit = math.exp(-((ph - 0.35) % 1.0) * 14) if ph >= 0.33 else 0.0
    return gx, gy, hit


def chopper(f, t, x=330, y=1470, s=1.0, period=0.5, t0=0.0, dull=False, ang=-6, gx=560, up=1140, down=1250, expr="happy", mouth=None,
            brow="up", look=(1, 0.4), la=(20, 10)):
    """Chubby holding a knife in his right hand (2-bone IK) and chopping. returns the hit strength (for squash/SFX)."""
    gx, gy, hit = chop_pose(t, t0, period, up, down, gx)
    sh = (x + 118 * s, y - 215 * s - 46 * s)
    a1, a2 = arm_ik(sh, (gx, gy), 76 * s, 70 * s)
    chub(f, x, y, s, la=la, ra=(a1, a2), mouth=talk(t) if mouth is None else mouth, expr=expr, brow=brow, look=look)
    knife_at(f, gx, gy, ang, 0.7 * s, dull)
    cv2.circle(f, (int(gx), int(gy)), int(19 * s), C(INK), -1, cv2.LINE_AA); cv2.circle(f, (int(gx), int(gy)), int(14 * s), C(CH_SKIN), -1, cv2.LINE_AA)
    return hit


def board_onion(f, t, x=760, y=1395, s=0.75, os_=0.7, face=False, mood="n", look=(0, 0)):
    comp(f, scale_el(board_el(), s), x - 40, y)
    oy = y - 30 - 126 * os_ / 0.7
    comp(f, scale_el(onion_el(face, mood, look), os_), x, oy)
    return x, oy


def zz(f, x, y, t, n=3, col=WHITE):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1.0
        comp(f, ed_el("", "Z", "", big_col=col, big_size=int(40 + 30 * ph)), x + 40 * ph + 10 * i, y - 160 * ph, op=math.sin(math.pi * ph))


def shield_el():
    def mk():
        w, h, sc = 220, 260, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        sh = lambda m: m.polygon(S(20, 30, 110, 10, 200, 30, 196, 140, 110, 246, 24, 140), fill=255)
        _outline(im, sh, 11); shape_grad(im, sh, (120, 180, 255), (40, 90, 200))
        d.polygon(S(110, 40, 172, 56, 168, 140, 110, 214, 52, 140, 48, 56), outline=(255, 255, 255, 255), width=6 * sc)
        d.line(S(110, 60, 110, 190), fill=(255, 255, 255, 255), width=8 * sc); d.line(S(66, 110, 154, 110), fill=(255, 255, 255, 255), width=8 * sc)
        return _done(im, w, h)
    return gcache("shield", mk)


def gland(f, x, y, s, lit=0.0):
    cv2.ellipse(f, (int(x), int(y)), (int(46 * s), int(24 * s)), -18, 0, 360, C(INK), -1, cv2.LINE_AA)
    col = tuple(int(a + (b - a) * clamp(lit)) for a, b in zip((255, 160, 180), (120, 210, 255)))
    cv2.ellipse(f, (int(x), int(y)), (int(40 * s), int(18 * s)), -18, 0, 360, C(col), -1, cv2.LINE_AA)


def ring_el():
    def mk():
        w, h, sc = 200, 160, 2; im, d = _canvas(w, h, sc); S = lambda *v: [x * sc for x in v]
        d.ellipse(S(10, 10, 190, 150), outline=INK + (255,), width=34 * sc)
        d.ellipse(S(16, 16, 184, 144), outline=(236, 176, 80, 255), width=22 * sc)
        return _done(im, w, h)
    return gcache("oring", mk)


# ---- S0: HOOK — Chubby chops an onion; green gas sneaks up; at "cry" his eyes gush tears; at "purpose" the onion grins ----
TC = T("i1", "cry...") - 0.1; TP = T("i1", "purpose?") - 0.1


def shot_S0(t, n):
    f = stage("kitchen", (255, 246, 214), 540, 900, 440); tiles(f, 250, 1100)
    x0, oy = board_onion(f, t, 760, 1395, 0.75, 0.7, face=t >= TP, mood="sly", look=(-1, -0.3))
    cv2.line(f, (760, int(oy - 110)), (760, int(oy + 120)), C(INK), 5, cv2.LINE_AA)
    wisps(f, 760, oy - 110, t, 0.0, 5, 520, 1.0, 0.7)
    k = ramp(t, 0.35, TC - 0.35)
    if t < TC + 0.4:
        gx_, gy_ = 760 + (395 - 760) * k, oy - 140 + (1060 - (oy - 140)) * k - 120 * math.sin(math.pi * k)
        gas(f, gx_, gy_, 0.42 + 0.1 * k, t, "sly", op=1.0 - clamp((t - TC) / 0.35))
    cry = t >= TC
    chopper(f, t, 330, 1470, 1.0, 0.5, 0.0, expr="wow" if cry else "happy", mouth=3 if cry else munch(t, 0.5)[0], brow="sad" if cry else "up",
            look=(1, 0.4) if not cry else (0, -0.3))
    hx, hy = head_pos(330, 1470, 1.0)
    if cry: tear_streams(f, hx, hy, 1.0, t, TC, 1.0, 1.0)
    if cry: comp(f, burst_el("CRY?!", TEAR, INK, 56), 650, 760, scale=pin(t, TC + 0.05, 0.22) * (1 - clamp((t - TP + 0.1) / 0.2)))
    if t >= TP: slam(f, chip("ON PURPOSE", RED_, WHITE, 40), 770, 980, -6, t, TP)
    ui_word(f, "do you know an onion makes you", "[CRY]...", 470, t, 0.1, col=INK, acc=TEAR_D, size=210, out=TP - 0.05)
    ui_word(f, "...on", "[PURPOSE]?", 470, t, TP - 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S1: it's a TRAP! (sly onion; Chubby, unaware, grins with his knife) ----
def shot_S1(t, n):
    f = stage("onion", (255, 200, 240), 640, 980, 400); u = lt(t, "S1")
    rays(f, 700, 1080, 760, (255, 220, 250), 0.25, t)
    rot_comp(f, scale_el(onion_el(True, "sly", (-0.8, 0)), 1.35), 720, 1080 + 8 * math.sin(t * 3), 4 * math.sin(t * 2), pin(t, st_("S1"), 0.3), 1.0, 0.35)
    chub(f, 230, 1480, 0.82, la=(20, 10), ra=(70, 40), mouth=0, expr="happy", brow="up", look=(1, 0), hold=scale_el(knife_el(), 0.4), hold_off=(40, -10), hold_front=True)
    tt = T("i2", "trap!") - 0.1
    if t >= tt: slam(f, burst_el("TRAP!", RED_, WHITE, 60), 780, 760, -8, t, tt)
    ui_word(f, "it's a", "[TRAP]!", 470, t, st_("S1") + 0.05, col=WHITE, acc=YEL_, size=230, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S1b: your knife sets it off (knife touches -> BOOM, a gas cloud bursts out) ----
def shot_S1b(t, n):
    f = stage("gas", (220, 255, 170), 540, 1000, 420); u = lt(t, "S1b")
    tk = T("i2", "knife") - 0.05
    k = ramp(t, st_("S1b"), max(0.2, tk - st_("S1b")))
    comp(f, scale_el(onion_el(True, "sly" if t < tk else "happy"), 1.2), 540, 1150)
    knife_at(f, 700 - 120 * k, 820 + 110 * k, 20, 0.75)
    if t >= tk:
        q = t - tk
        for i in range(7):
            a = 2 * math.pi * i / 7 + 0.4; rr = 120 + 260 * eo(clamp(q / 0.5))
            gas(f, 540 + rr * math.cos(a), 1100 + rr * math.sin(a) * 0.8, 0.45 + 0.1 * (i % 2), t + i, "sly", op=1 - clamp((q - 0.8) / 0.6))
        comp(f, burst_el("BOOM!", YEL_, INK, 64), 540, 800, scale=pin(t, tk, 0.22))
    ui_word(f, "and your", "[KNIFE] sets it off", 470, t, st_("S1b") + 0.05, col=WHITE, acc=YEL_, size=150, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S2: open loop — scientists made an onion that CAN'T (scientist + calm onion + COMING UP) ----
def shot_S2(t, n):
    f = stage("sky", (236, 248, 255), 540, 980, 420); u = lt(t, "S2")
    scientist(f, 300, 1480, 0.92, la=(20, 10), ra=(150, 175), mouth=talk(t), expr="happy", brow="up", look=(1, -0.3))
    rot_comp(f, scale_el(onion_el(True, "happy"), 0.85), 720, 1080 + 10 * math.sin(t * 3), 5 * math.sin(t * 2), pin(t, st_("S2") + 0.2, 0.3), 1.0, 0.3)
    tc = T("i3", "can't") - 0.1
    if t >= tc:
        slam(f, stamp_el("NO TEARS", (34, 160, 90), 54), 720, 1300, -6, t, tc)
        comp(f, chip("COMING UP", INK, YEL_, 30), 540, 1440, op=clamp((t - tc - 0.3) / 0.3))
        sparkles(f, 720, 1060, t, tc, 12, 220)
    ui_word(f, "scientists made an onion that", "[CAN'T]", 470, t, st_("S2") + 0.1, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S3: PART 1 — the secret: an onion is made of tiny cells (powers-of-ten push from the onion's rings into its cells) ----
def _s3_far(t):
    f = stage("cream", (255, 240, 220), 540, 1060, 420)
    comp(f, scale_el(onion_half_el(), 1.6), 540, 1060)
    return f


def _s3_near(t):
    f = stage("onion"); cell_grid(f, 540, 1000, 1080, 1200, 170, 80, t, hi=(540 + 85, 1000 + 0))
    return f


def shot_S3(t, n):
    u = lt(t, "S3"); tz = T("a1", "An") - 0.2
    f = zoom_through(t, tz, 0.9, lambda: _s3_far(t), lambda: _s3_near(t), 600, 980, 7.0)
    f = np.ascontiguousarray(f, np.float32)
    chapter_card(f, t, st_("S3") + 0.05, 1, "THE TRAP", y=1400, dur=1.4, col=(255, 200, 240))
    if t >= tz + 0.9:
        label_at(f, "ONE CELL", 820, 1260, t, tz + 1.0, 660, 1040, bg=INK)
        comp(f, chip("MAGNIFIED", YEL_, INK, 26), 540, 1440, op=clamp((t - tz - 1.1) / 0.3))
    if t < tz + 0.5: ui_word(f, "here's the", "[SECRET]", 470, t, st_("S3") + 0.1, col=INK, acc=RED_, size=220, out=tz + 0.4)
    else: ui_word(f, "an onion is made of tiny", "[CELLS]", 470, t, tz + 0.5, col=INK, acc=(150, 40, 140), size=210)
    return finish(f, n)


# ---- S4: inside each cell, two chemicals in separate rooms (big cut-away cell; ROOM 1 / ROOM 2) ----
def shot_S4(t, n):
    f = stage("onion", (255, 210, 245), 540, 1000, 440); u = lt(t, "S4")
    onion_cell(f, 540, 1040, 800, 640, t, 0.0, True, True, T("a2", "separate") - 0.2)
    tt = T("a2", "two") - 0.1
    if t >= tt:
        comp(f, scale_el(sulfur_el("n"), 0.9), 345, 1080 + 8 * math.sin(t * 3), scale=pin(t, tt, 0.3))
        comp(f, scale_el(enz_el(1, 0.3, "n"), 0.85), 740, 1080 + 8 * math.sin(t * 3 + 1), scale=pin(t, tt + 0.25, 0.3))
    label_at(f, "CELL WALL", 250, 1440, t, st_("S4") + 0.5, 160, 1330, bg=(110, 140, 40))
    wui(f, "two chemicals in", "[SEPARATE ROOMS]", t, st_("S4") + 0.1, acc=YEL_, size=140)
    return finish(f, n)


# ---- S5: room 1 is full of SULFUR stuff (push into room 1; sulfur molecules bounce) ----
def shot_S5(t, n):
    u = lt(t, "S5")
    g = stage("onion"); onion_cell(g, 540, 1040, 800, 640, t, 0.0, True, False)
    for i, (dx, dy) in enumerate(((-120, -120), (40, -40), (-90, 120), (60, 170), (-20, 20))):
        comp(g, scale_el(sulfur_el("happy" if i % 2 else "n", (0.5 if math.sin(t + i) > 0 else -0.5, 0)), 0.62), 340 + dx * 0.9 + 14 * math.sin(t * 3 + i), 1040 + dy * 0.9 + 12 * math.cos(t * 2.6 + i), scale=pin(t, st_("S5") + 0.1 + 0.08 * i, 0.3))
    k = ramp(t, st_("S5"), 0.6)
    f = np.ascontiguousarray(cam(g, 1 + 0.55 * k, 340, 1040, (540 - 340) * k, 0), np.float32)
    ts = T("a3", "sulfur.") - 0.15
    label_at(f, "SULFUR STUFF", 540, 1440, t, ts, 540, 1300, bg=SULF_D)
    comp(f, chip("ROOM 1", INK, WHITE, 28), 540, 650, op=clamp((u - 0.3) / 0.3))
    wui(f, "full of", "[SULFUR]", t, st_("S5") + 0.1, acc=SULF, size=230)
    return finish(f, n)


# ---- S5b: onions pull it from the soil (cut-away soil; sulfur dots climb the roots into the bulb) ----
def shot_S5b(t, n):
    f = stage("sky", (255, 246, 200), 820, 760, 160); u = lt(t, "S5b")
    soil_y = 1120
    cv2.rectangle(f, (0, soil_y), (W, H), C((120, 76, 40)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (0, soil_y), (W, soil_y + 26), C((70, 140, 50)), -1, cv2.LINE_AA)
    rng = np.random.default_rng(2)
    for i in range(40): cv2.circle(f, (int(rng.uniform(0, W)), int(rng.uniform(soil_y + 40, H))), int(rng.uniform(4, 10)), C((96, 58, 30)), -1, cv2.LINE_AA)
    bx, by = 540, 1080
    for k in range(-2, 3):
        P = [(bx + 10 * k, by - 120), (bx + 60 * k, by - 420 - 30 * abs(k))]
        cv2.line(f, (int(P[0][0]), int(P[0][1])), (int(P[1][0]), int(P[1][1])), C(INK), 26, cv2.LINE_AA)
        cv2.line(f, (int(P[0][0]), int(P[0][1])), (int(P[1][0]), int(P[1][1])), C((70, 170, 60)), 16, cv2.LINE_AA)
    roots = []
    for k in range(-3, 4):
        P = [(bx + 12 * k + 40 * k * j / 3 + (14 * math.sin(j + k) if j else 0), by + 110 + 70 * j) for j in range(5)]
        cv2.polylines(f, [np.array(P, np.int32)], False, C((230, 210, 170)), 6, cv2.LINE_AA); roots.append(P[::-1])
    comp(f, scale_el(onion_el(True, "happy"), 0.95), bx, by)
    for i, P in enumerate(roots):
        pulse_path(f, P, t, st_("S5b") + 0.15 + 0.12 * i, 0.9, SULF, 12, 2, 0.45, 5)
    label_at(f, "SULFUR FROM THE SOIL", 540, 1440, t, st_("S5b") + 0.4, 600, 1340, bg=SULF_D)
    wui(f, "pulled up from the", "[SOIL]", t, st_("S5b") + 0.05, acc=SULF, size=220)
    return finish(f, n)


# ---- S6: room 2 holds an ENZYME (it pops in, chomping) ----
def shot_S6(t, n):
    u = lt(t, "S6")
    g = stage("onion"); onion_cell(g, 540, 1040, 800, 640, t, 0.0, True, False)
    comp(g, scale_el(sulfur_el("n"), 0.6), 340, 1040 + 10 * math.sin(t * 3))
    te = T("a4", "enzyme.") - 0.2
    if t >= te - 0.3:
        comp(g, scale_el(enz_el(1, chomp(t), "n", (-0.6, 0)), 1.0), 740, 1040 + 10 * math.sin(t * 3 + 1), scale=pin(t, te - 0.3, 0.3))
    k = ramp(t, st_("S6"), 0.6); f = np.ascontiguousarray(cam(g, 1 + 0.5 * k, 740, 1040, (540 - 740) * k, 0), np.float32)
    comp(f, chip("ROOM 2", INK, WHITE, 28), 540, 650, op=clamp((u - 0.3) / 0.3))
    if t >= te: label_at(f, "ENZYME", 540, 1440, t, te, 540, 1300, bg=ENZ1_D)
    wui(f, "the second one: an", "[ENZYME]", t, st_("S6") + 0.1, acc=(140, 200, 255), size=210)
    return finish(f, n)


# ---- S6b: an enzyme is a tiny HELPER (big friendly enzyme, define-on-sight card) ----
def shot_S6b(t, n):
    f = stage("sky", (236, 248, 255), 540, 1000, 440); u = lt(t, "S6b")
    rot_comp(f, scale_el(enz_el(1, 0.35 + 0.15 * math.sin(t * 4), "happy"), 1.5), 540, 1040 + 10 * math.sin(t * 3), 4 * math.sin(t * 2), pin(t, st_("S6b") + 0.05, 0.3), 1.0, 0.35)
    th = T("a5", "helper.") - 0.15
    if t >= th:
        comp(f, chip("ENZYME = TINY HELPER", INK, YEL_, 36), 540, 1360, op=clamp((t - th) / 0.2), scale=pin(t, th, 0.3))
        sparkles(f, 540, 1000, t, th, 12, 280)
    ui_word(f, "an enzyme is a tiny", "[HELPER]", 470, t, st_("S6b") + 0.1, col=INK, acc=ENZ1_D, size=220)
    return finish(f, n)


# ---- S6c: it turns one chemical into another (conveyor: yellow molecule in -> purple blob out) ----
def shot_S6c(t, n):
    f = stage("yellow", (255, 250, 220), 540, 1000, 420); u = lt(t, "S6c")
    yb = 1120
    cv2.rectangle(f, (60, yb + 70), (1020, yb + 110), C(INK), -1, cv2.LINE_AA); cv2.rectangle(f, (66, yb + 76), (1014, yb + 104), C((120, 120, 130)), -1, cv2.LINE_AA)
    for k in range(14):
        xx = 66 + ((k * 72 + u * 160) % 948); cv2.line(f, (int(xx), yb + 78), (int(xx), yb + 102), C((80, 80, 90)), 4, cv2.LINE_AA)
    for j in range(4):
        x_ = 100 + ((u * 330 + j * 240) % 900)
        if x_ < 420: comp(f, scale_el(sulfur_el("n"), 0.72), x_, yb - 10)
        elif x_ > 660 and x_ < 960: acid(f, x_, yb - 10, 0.72, t, 0.6)
    comp(f, scale_el(enz_el(1, chomp(t, 0.5), "happy", (-1, 0)), 1.05), 540, yb - 40)
    comp(f, chip("IN", INK, WHITE, 30), 170, yb + 170); comp(f, chip("OUT", INK, WHITE, 30), 910, yb + 170)
    draw_arrow(f, 250, yb + 170, 420, yb + 170, 1.0, INK, 8, 26); draw_arrow(f, 660, yb + 170, 830, yb + 170, 1.0, INK, 8, 26)
    ui_word(f, "turns one chemical", "into [ANOTHER]", 470, t, st_("S6c") + 0.05, col=INK, acc=RED_, size=150)
    return finish(f, n)


# ---- S7: as long as they stay apart, NOTHING happens (sleeping in their rooms) ----
def shot_S7(t, n):
    f = stage("onion", (190, 170, 255), 540, 1000, 420); u = lt(t, "S7")
    onion_cell(f, 540, 1040, 800, 640, t, 0.0, True, False)
    comp(f, scale_el(sulfur_el("sleep"), 0.85), 340, 1080 + 6 * math.sin(t * 1.5))
    comp(f, scale_el(enz_el(1, 0.05, "sleep"), 0.85), 740, 1080 + 6 * math.sin(t * 1.5 + 1))
    zz(f, 380, 960, t); zz(f, 780, 960, t + 0.5)
    tn = T("a6", "nothing") - 0.15
    if t >= tn: comp(f, chip("NOTHING HAPPENS", INK, YEL_, 36), 540, 1440, op=clamp((t - tn) / 0.2), scale=pin(t, tn, 0.3))
    wui(f, "as long as they stay", "[APART]", t, st_("S7") + 0.1, acc=(255, 200, 240), size=220)
    return finish(f, n)


# ---- S8: PART 2 — but then... you CUT it (giant knife slams down; chain map starts: CUT) ----
TCUT = T("b1", "cut") - 0.08


def shot_S8(t, n):
    f = stage("kitchen", (255, 236, 200), 540, 980, 420); u = lt(t, "S8"); tiles(f, 250, 1000)
    comp(f, scale_el(board_el(800), 1.0), 540, 1290)
    k = ramp(t, TCUT - 0.25, 0.25)
    cut = clamp((t - TCUT) / 0.3)
    el = scale_el(onion_el(True, "wow" if t >= TCUT else "sly", (0, -1)), 1.2); pm, a = el; w2 = a.shape[1] // 2
    oy = 1050
    if cut <= 0: comp(f, el, 540, oy)
    else:
        comp(f, (pm[:, :w2], a[:, :w2]), 540 - w2 / 2 - 30 * cut, oy); comp(f, (pm[:, w2:], a[:, w2:]), 540 + w2 / 2 + 30 * cut, oy)
        wisps(f, 540, oy - 150, t, TCUT, 5, 420, 1.2, 0.8)
    gy = 650 + (830 - 650) * k - 40 * ramp(t, TCUT + 0.4, 0.4)
    knife_at(f, 200, gy, -4, 1.3)
    if t >= TCUT: comp(f, burst_el("CHOP!", YEL_, INK, 60), 830, 760, scale=pin(t, TCUT, 0.22))
    chapter_card(f, t, st_("S8") + 0.02, 2, "THE KNIFE", y=760, dur=1.2, col=YEL_)
    if t >= TCUT: chain(f, t, 0, TCUT)
    ui_word(f, "but then... you", "[CUT] it", 470, t, st_("S8") + 0.1, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S9: the knife breaks the walls and the two chemicals MIX ----
def shot_S9(t, n):
    f = stage("onion", (255, 200, 240), 540, 1000, 420); u = lt(t, "S9")
    tb = T("b2", "breaks") - 0.15; tm = T("b2", "mix.") - 0.3
    br = ramp(t, tb, 0.3)
    onion_cell(f, 540, 980, 800, 620, t, br, True, False)
    km = ramp(t, tb + 0.3, max(0.3, tm - tb - 0.3))
    comp(f, scale_el(sulfur_el("wow" if br > 0.5 else "n"), 0.85), 340 + 150 * km + 6 * br * math.sin(t * 30), 1010)
    comp(f, scale_el(enz_el(1, chomp(t), "sly", (-1, 0)), 0.85), 740 - 150 * km, 1010)
    if br > 0: knife_at(f, 120, 620 + 120 * ramp(t, tb - 0.2, 0.2), -38, 1.0, op=1 - ramp(t, tb + 0.4, 0.3))
    mixed = t >= tm + 0.25
    if mixed: comp(f, burst_el("MIX!", YEL_, INK, 56), 540, 760, scale=pin(t, tm + 0.25, 0.22))
    chain(f, t, 1 if mixed else 0, tm + 0.25 if mixed else -5)
    wui(f, "the walls break, the chemicals", "[MIX]", t, st_("S9") + 0.1, acc=YEL_, size=210)
    return finish(f, n)


# ---- S10: first, the enzyme SNIPS the sulfur stuff ----
def shot_S10(t, n):
    f = stage("cream", (230, 240, 255), 540, 1000, 420); u = lt(t, "S10")
    ts = T("b3", "snips") - 0.1
    k = ramp(t, st_("S10"), max(0.2, ts - st_("S10")))
    if t < ts + 0.05:
        comp(f, scale_el(sulfur_el("n"), 1.1), 660, 1040 + 6 * math.sin(t * 3))
    else:
        q = ramp(t, ts, 0.3)
        el = scale_el(sulfur_el("wow"), 1.1); pm, a = el; h2 = a.shape[0] // 2
        comp(f, (pm[:h2], a[:h2]), 660 + 20 * q, 1040 - h2 / 2 - 30 * q); comp(f, (pm[h2:], a[h2:]), 660 + 20 * q, 1040 + h2 / 2 + 30 * q)
    comp(f, scale_el(enz_el(1, chomp(t, 0.22) if t < ts + 0.6 else 0.1, "sly", (1, 0)), 1.1), 200 + 230 * k, 1040)
    if t >= ts:
        comp(f, burst_el("SNIP!", ENZ1, WHITE, 52), 840, 780, scale=pin(t, ts, 0.22))
    chain(f, t, 1, -5)
    ui_word(f, "first, the enzyme", "[SNIPS] it", 470, t, st_("S10") + 0.1, col=INK, acc=ENZ1_D, size=200)
    return finish(f, n)


# ---- S10b: ...into a new ACID (the pieces turn into a purple blob; chain: ACID) ----
def shot_S10b(t, n):
    f = stage("purple", (220, 190, 255), 540, 1000, 420); u = lt(t, "S10b")
    k = ramp(t, st_("S10b") + 0.05, 0.35)
    if k < 1:
        for j, dy in enumerate((-90, 90)):
            comp(f, scale_el(sulfur_el("wow"), 0.6), 640, 1040 + dy * (1 - k), op=1 - k)
    acid(f, 640, 1040, 1.0 * k + 0.01, t, 0.5)
    sparkles(f, 640, 1040, t, st_("S10b") + 0.1, 12, 240, (230, 200, 255))
    comp(f, scale_el(enz_el(1, 0.2, "happy", (1, 0)), 0.8), 240, 1060)
    label_at(f, "NEW ACID", 840, 1300, t, T("b3", "acid.") - 0.2, 700, 1140, bg=ACID_D)
    chain(f, t, 2, st_("S10b") + 0.3)
    wui(f, "into a new", "[ACID]", t, st_("S10b") + 0.05, acc=(220, 180, 255), size=240)
    return finish(f, n)


# ---- S11: that acid is WOBBLY (unstable) ----
def shot_S11(t, n):
    f = stage("onion", (230, 200, 255), 540, 1000, 420); u = lt(t, "S11")
    tw = T("b4", "wobbly.") - 0.15
    w_ = 0.6 + 2.2 * ramp(t, tw, 0.2)
    acid(f, 540 + 4 * w_ * math.sin(t * 40), 1040, 1.4, t, w_)
    if t >= tw:
        slam(f, stamp_el("UNSTABLE", RED_, 56), 540, 1260, -6, t, tw)
        for sg in (-1, 1):
            for j in range(3): cv2.line(f, (int(540 + sg * (200 + 30 * j)), 900 + 60 * j), (int(540 + sg * (240 + 30 * j)), 930 + 60 * j), C(WHITE), 6, cv2.LINE_AA)
    chain(f, t, 2, -5)
    wui(f, "that acid is", "[WOBBLY]", t, st_("S11") + 0.1, acc=(220, 180, 255), size=230)
    return finish(f, n)


# ---- S11b: so a SECOND enzyme grabs it (orange pac-man swoops in) ----
def shot_S11b(t, n):
    f = stage("orange", (255, 220, 180), 540, 1000, 420); u = lt(t, "S11b")
    tg = T("b4", "grabs") - 0.1
    k = ramp(t, st_("S11b"), max(0.2, tg - st_("S11b")))
    acid(f, 560, 1040, 1.0, t, 1.8 if t < tg else 0.4)
    comp(f, scale_el(enz_el(2, 0.8 if t < tg else 0.15, "sly", (-1, 0)), 1.15), 1200 - 470 * k, 1040 - 80 * math.sin(math.pi * k))
    if t >= tg: comp(f, burst_el("GOTCHA!", ENZ2, WHITE, 48), 820, 780, scale=pin(t, tg, 0.22))
    label_at(f, "ENZYME 2", 260, 1260, t, T("b4", "second") - 0.1, 420, 1120, bg=ENZ2_D)
    chain(f, t, 2, -5)
    wui(f, "a", "[SECOND] enzyme grabs it", t, st_("S11b") + 0.05, acc=(255, 190, 140), size=150)
    return finish(f, n)


# ---- S12: ...and turns it into a GAS (acid shrinks, the gas ghost puffs up; chain: GAS) ----
def shot_S12(t, n):
    f = stage("gas", (220, 255, 170), 540, 1000, 420); u = lt(t, "S12")
    tg = T("b5", "gas.") - 0.2
    k = ramp(t, st_("S12") + 0.1, max(0.3, tg - st_("S12")))
    comp(f, scale_el(enz_el(2, chomp(t, 0.35) * 0.4, "happy", (1, 0)), 0.85), 250, 1150)
    if k < 1: acid(f, 600, 1100, 1.0 * (1 - k) + 0.02, t, 1.0)
    gas(f, 600, 1100 - 140 * k, 0.2 + 1.0 * k, t, "sly")
    if t >= tg: sparkles(f, 600, 960, t, tg, 14, 300, (220, 255, 170))
    if t >= tg: chain(f, t, 3, tg)
    else: chain(f, t, 2, -5)
    wui(f, "and turns it into a", "[GAS]", t, st_("S12") + 0.05, acc=(220, 255, 140), size=250)
    return finish(f, n)


# ---- S12b: name card — the TEAR FACTOR ----
def shot_S12b(t, n):
    f = stage("gas", (200, 250, 150), 540, 980, 440); u = lt(t, "S12b")
    rays(f, 540, 1000, 760, (230, 255, 200), 0.25, t)
    gas(f, 540, 1000, 1.4, t, "sly", look=(0, 0.3))
    tf = T("b5", "tear") - 0.15
    if t >= tf: slam(f, tag_el("TEAR FACTOR", GAS_D, WHITE, 64), 540, 1320, -4, t, tf)
    comp(f, chip("science name: lachrymatory factor = tear-causing", INK, WHITE, 22), 540, 1462, op=clamp((t - tf - 0.4) / 0.3))
    wui(f, "scientists call it the", "[TEAR FACTOR]", t, st_("S12b") + 0.05, acc=(220, 255, 140), size=170)
    return finish(f, n)


# ---- S13: the gas floats up, right into your eyes (side view: the ghost rises along a curve to Chubby's eye) ----
def shot_S13(t, n):
    f = stage("kitchen", (255, 240, 200), 540, 900, 400); u = lt(t, "S13"); tiles(f, 250, 1000)
    comp(f, scale_el(board_el(), 0.75), 780, 1440)
    comp(f, scale_el(onion_half_el(260), 0.9), 780, 1330)
    te = T("b6", "eyes.") - 0.1
    k = ramp(t, st_("S13") + 0.1, max(0.3, te - st_("S13") - 0.1))
    hx, hy = head_pos(300, 1480, 1.05)
    P = [(780, 1220), (860, 1000), (720, 820), (500, 900), (hx + 60, hy)]
    for j in range(1, 30):
        if j / 30 > k: break
        px, py = path_point(P, j / 30); cv2.circle(f, (int(px), int(py)), 6, C(GAS_D), -1, cv2.LINE_AA)
    gx_, gy_ = path_point(P, k)
    hit = t >= te
    chub(f, 300, 1480, 1.05, la=(20, 10), ra=(20, 10), mouth="o" if hit else 0, expr="wow" if hit else "sus", brow="sad" if hit else "sus", look=(1, -0.6))
    gas(f, gx_, gy_, 0.55, t, "sly" if not hit else "happy", op=1 - clamp((t - te - 0.4) / 0.3))
    if hit: comp(f, burst_el("STING!", RED_, WHITE, 48), 640, 760, scale=pin(t, te, 0.22))
    wui(f, "it floats right into your", "[EYES]", t, st_("S13") + 0.1, acc=TEAR, size=220)
    return finish(f, n)


# ---- S14: tiny NERVES on the front of your eye feel the sting (eye close-up + magnified nerve endings; chain: NERVES) ----
def shot_S14(t, n):
    f = stage("tear", (200, 240, 255), 540, 1000, 440); u = lt(t, "S14")
    comp(f, scale_el(eye_el(0.15, 0.0, 1.0), 1.1), 540, 860)
    gas(f, 860, 700, 0.42, t, "sly", look=(-1, 0.3))
    tn = T("b7", "nerves") - 0.15; ts = T("b7", "sting.") - 0.15
    lit = ramp(t, ts, 0.2)
    def close(g):
        g[:] = np.array(C((255, 220, 210)), np.float32); nerve_endings(g, 540, 1150, 200, t, lit)
    inset(f, 540, 1130, 175, close, pin(t, tn, 0.3))
    if t >= tn:
        label_at(f, "NERVE ENDINGS", 840, 1250, t, tn + 0.3, 700, 1150, bg=(150, 110, 20))
        label_at(f, "FRONT OF THE EYE", 250, 640, t, tn + 0.1, 470, 800, bg=TEAR_D)
    if t >= ts: comp(f, burst_el("OUCH!", RED_, WHITE, 44), 220, 1100, scale=pin(t, ts, 0.22))
    chain(f, t, 4 if t >= tn else 3, tn if t >= tn else -5)
    wui(f, "tiny nerves feel the", "[STING]", t, st_("S14") + 0.1, acc=YEL_, size=210)
    return finish(f, n)


# ---- S15: tear glands FLOOD your eyes to wash it out (big face; gland lights up; gas washed away; chain: TEARS) ----
def shot_S15(t, n):
    f = stage("tear", (190, 236, 255), 540, 1000, 440); u = lt(t, "S15")
    tf = T("b8", "flood") - 0.15
    fl = ramp(t, tf, 0.25)
    hx, hy = 540, 1000; s_ = 2.6
    chub_head_only(f, hx, hy, s_, t, mouth="o" if fl > 0 else 0, expr="wow" if fl > 0 else "sus", brow="sad", look=(0, 0))
    for sg in (-1, 1): gland(f, hx + sg * 120, hy - 70, 1.0, fl)
    gas(f, 840 + 300 * fl, 760 - 200 * fl, 0.5, t, "sad" if fl > 0 else "sly", op=1 - fl * 0.6)
    if fl > 0: tear_streams(f, hx, hy, s_, t, tf, 1.0, 0.8)
    label_at(f, "TEAR GLAND", 820, 660, t, T("b8", "glands") - 0.15, hx + 120, hy - 90, bg=TEAR_D)
    chain(f, t, 5 if t >= tf else 4, tf if t >= tf else -5)
    wui(f, "tear glands", "[FLOOD] your eyes", t, st_("S15") + 0.1, acc=TEAR, size=170)
    return finish(f, n)


# ---- S16: PART 3 — but WHY would an onion do this? (Chubby scratches his head, onion in hand) ----
def shot_S16(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 420); u = lt(t, "S16")
    chub(f, 380, 1480, 1.0, la=(-150, -150), ra=(150, -120), mouth=0, expr="sus", brow="sus", look=(1, -0.3),
         hold=scale_el(onion_el(True, "sly"), 0.5), hold_off=(30, -60), hold_front=True)
    comp(f, ed_el("", "?", "", big_col=RED_, big_size=170), 780 + 6 * math.sin(t * 4), 920)
    chapter_card(f, t, st_("S16") + 0.02, 3, "WHY?", y=720, dur=1.4, col=YEL_)
    ui_word(f, "but", "[WHY]?", 470, t, st_("S16") + 0.05, col=INK, acc=RED_, size=250)
    return finish(f, n)


# ---- S17: to PROTECT itself (onion knight with a shield) ----
def shot_S17(t, n):
    f = stage("emerald", (200, 250, 220), 540, 1000, 430); u = lt(t, "S17")
    rays(f, 540, 1060, 760, (220, 255, 230), 0.25, t)
    rot_comp(f, scale_el(onion_el(True, "n", (0, -0.5)), 1.25), 600, 1080 + 6 * math.sin(t * 3), 0, pin(t, st_("S17"), 0.3), 1.0, 0.35)
    slam(f, shield_el(), 360, 1160, 8, t, T("c2", "protect") - 0.1, 0.95)
    wui(f, "to", "[PROTECT] itself", t, st_("S17") + 0.1, acc=YEL_, size=190)
    return finish(f, n)


# ---- S17b: to an onion, a bug's bite = your knife (contrast panels: same damage -> same gas) ----
def shot_S17b(t, n):
    f = stage("cream", (240, 250, 240), 540, 1000, 380); u = lt(t, "S17b")
    tb = T("c2", "bite") - 0.15; tk = T("c2", "knife.") - 0.15
    def L(g):
        comp(g, scale_el(onion_el(True, "wow"), 0.6), 330, 1180)
        comp(g, scale_el(bug_el(bite=True), 0.6), 240 + 15 * math.sin(t * 8), 1040)
        if t >= tb: gas(g, 330, 900, 0.32, t, "sly")
    def R(g):
        comp(g, scale_el(onion_el(True, "wow"), 0.6), 750, 1180)
        knife_at(g, 590, 1040 + 30 * math.sin(t * 8), -20, 0.5)
        if t >= tk: gas(g, 750, 900, 0.32, t, "sly")
    split_contrast(f, t, st_("S17b") + 0.05, L, R, "A BUG'S BITE", "YOUR KNIFE", (120, 200, 90), (255, 160, 80), 640, 1380, t_r=tk - 0.3)
    if t >= tk + 0.2: comp(f, chip("SAME DAMAGE = SAME GAS", INK, YEL_, 30), 540, 1440, op=clamp((t - tk - 0.2) / 0.3))
    ui_word(f, "a bug's bite =", "[YOUR KNIFE]", 470, t, st_("S17b") + 0.05, col=INK, acc=RED_, size=170)
    return finish(f, n)


# ---- S18: the gas is a DEFENSE against insects and germs (they flee the cloud) ----
def shot_S18(t, n):
    f = stage("gas", (220, 255, 170), 540, 1000, 420); u = lt(t, "S18")
    k = ramp(t, st_("S18") + 0.3, 1.0)
    for i in range(6):
        a = 2 * math.pi * i / 6 + t * 0.4; rr = 120 + 150 * k
        gas(f, 540 + rr * math.cos(a), 1080 + rr * 0.7 * math.sin(a), 0.3, t + i, "sly", op=0.85)
    comp(f, scale_el(onion_el(True, "happy"), 0.95), 540, 1080)
    ti = T("c3", "insects") - 0.15; tg = T("c3", "germs.") - 0.15
    if t >= ti:
        rot_comp(f, scale_el(bug_el(scared=True), 0.75), 240 - 200 * ramp(t, ti + 0.3, 0.8), 760, 10, 1.0, 1.0, 0.2)
        comp(f, chip("INSECTS", INK, WHITE, 28), 220, 1440, op=clamp((t - ti) / 0.2))
    if t >= tg:
        rot_comp(f, scale_el(germ_el("sad"), 0.6 * (1 - 0.5 * ramp(t, tg + 0.3, 0.6))), 840 + 80 * ramp(t, tg + 0.3, 0.8), 780, 0, 1.0, 1.0, 0.2)
        comp(f, chip("GERMS", INK, WHITE, 28), 860, 1440, op=clamp((t - tg) / 0.2))
    wui(f, "the gas is a", "[DEFENSE]", t, st_("S18") + 0.1, acc=YEL_, size=220)
    return finish(f, n)


# ---- S19: PART 4 — the TEAR-FREE onion I promised ----
def shot_S19(t, n):
    f = stage("sky", (240, 250, 255), 540, 1000, 440); u = lt(t, "S19")
    rays(f, 540, 1060, 800, (255, 255, 230), 0.35, t)
    rot_comp(f, scale_el(onion_el(True, "happy"), 1.3), 540, 1080 + 8 * math.sin(t * 3), 3 * math.sin(t * 2), pin(t, st_("S19"), 0.3), 1.0, 0.35)
    sparkles(f, 540, 1060, t, st_("S19") + 0.2, 14, 300)
    slam(f, stamp_el("NO TEARS", (34, 160, 90), 52), 540, 1350, -6, t, T("d1", "tear-free") - 0.1)
    chapter_card(f, t, st_("S19") + 0.02, 4, "TEAR-FREE ONION", y=760, dur=1.5, col=(150, 230, 255))
    ui_word(f, "the", "[TEAR-FREE] onion", 470, t, st_("S19") + 0.05, col=INK, acc=(34, 140, 80), size=170)
    return finish(f, n)


# ---- S20: 2002 — scientists in Japan ... ----
def shot_S20(t, n):
    f = stage("steel", (230, 236, 248), 540, 1000, 400); u = lt(t, "S20")
    scientist(f, 330, 1480, 0.95, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0),
              hold=magnifier_el(), hold_off=(40, -40), hold_front=True)
    tj = T("d2", "Japan") - 0.15
    if t >= tj: comp(f, chip("JAPAN", INK, WHITE, 34), 780, 1000, op=clamp((t - tj) / 0.3), scale=pin(t, tj, 0.3))
    comp(f, chip("Source: Imai et al., Nature, 2002", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "in", "[2002]", t, st_("S20") + 0.05, acc=YEL_, size=240)
    return finish(f, n)


# ---- S20b: ...FOUND that second enzyme (magnified: enzyme 2 caught under the lens) ----
def shot_S20b(t, n):
    f = stage("orange", (255, 220, 170), 540, 1000, 400); u = lt(t, "S20b")
    def close(g):
        g[:] = np.array(C(CELLF), np.float32); comp(g, scale_el(enz_el(2, chomp(t, 0.4) * 0.6, "wow", (0, 0)), 1.3), 540, 1000)
    inset(f, 540, 1000, 300, close, pin(t, st_("S20b") + 0.05, 0.3))
    slam(f, burst_el("FOUND IT!", YEL_, INK, 52), 820, 720, -8, t, st_("S20b") + 0.25)
    label_at(f, "ENZYME 2 = THE GAS MAKER", 540, 1420, t, st_("S20b") + 0.5, 540, 1300, bg=ENZ2_D)
    wui(f, "they found", "[ENZYME 2]", t, st_("S20b") + 0.05, acc=(255, 220, 160), size=200)
    return finish(f, n)


# ---- S21: then scientists in New Zealand + Japan... (DNA with the enzyme-2 gene highlighted) ----
def shot_S21(t, n):
    f = stage("purple", (200, 190, 255), 540, 1000, 420); u = lt(t, "S21")
    helix(f, 360, 1040, 760, t, (0.4, 0.62), ENZ2, 0.0)
    label_at(f, "GENE FOR ENZYME 2", 760, 880, t, st_("S21") + 0.4, 430, 1010, bg=ENZ2_D)
    tn = T("d3", "New") - 0.15
    if t >= tn: comp(f, chip("NEW ZEALAND + JAPAN", INK, WHITE, 30), 740, 1180, op=clamp((t - tn) / 0.3))
    comp(f, chip("Source: Eady et al., Plant Physiology, 2008", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "they found its", "[GENE]", t, st_("S21") + 0.05, acc=(255, 190, 140), size=230)
    return finish(f, n)


# ---- S21b: ...and SWITCHED it OFF (light switch flips; the gene greys out; enzyme 2 falls asleep) ----
def shot_S21b(t, n):
    f = stage("steel", (226, 232, 246), 540, 1000, 400); u = lt(t, "S21b")
    to = T("d3", "off.") - 0.2
    off = ramp(t, to, 0.25)
    helix(f, 260, 1040, 700, t, (0.4, 0.62), ENZ2, off)
    rot_comp(f, scale_el(switch_el(t < to), 1.0), 700, 940, 0, 1.0, 1.0, 0.3)
    if t >= to:
        comp(f, burst_el("CLICK!", WHITE, INK, 44), 870, 740, scale=pin(t, to, 0.22))
        comp(f, scale_el(enz_el(2, 0.05, "sleep"), 0.6), 720, 1290); zz(f, 770, 1230, t, 3, INK)
    wui(f, "and switched it", "[OFF]", t, st_("S21b") + 0.05, acc=(255, 140, 140), size=240)
    return finish(f, n)


# ---- S22: they crushed those onions... and the tears NEVER came (Chubby squeezes; dry eyes) ----
def shot_S22(t, n):
    f = stage("sky", (236, 248, 255), 540, 1000, 420); u = lt(t, "S22")
    tc = T("d4", "crushed") - 0.1; tn = T("d4", "never") - 0.15
    sq = 0.25 + 0.2 * math.sin(t * 9) if t >= tc else 0.0
    el = scale_el(onion_el(True, "happy"), 0.75); pm, a = el
    el2 = (cv2.resize(pm, (int(pm.shape[1] * (1 + sq)), int(pm.shape[0] * (1 - sq * 0.6)))), cv2.resize(a, (int(a.shape[1] * (1 + sq)), int(a.shape[0] * (1 - sq * 0.6)))))
    aa = arm_ik((540 + 118 * 1.05, 1480 - 261 * 1.05), (540 + 125 * (1 + sq), 1235), 76 * 1.05, 70 * 1.05)
    chub(f, 540, 1480, 1.05, la=aa, ra=aa, mouth=0 if t < tn else 2, expr="sus" if t < tn else "happy", brow="sus" if t < tn else "up", look=(0, 0.6))
    comp(f, el2, 540, 1230)
    if t >= tc: dust_puff(f, 540, 1300, t, tc, 7, 0.5)
    if t >= tn:
        slam(f, stamp_el("NO TEARS!", (34, 160, 90), 56), 540, 720, -6, t, tn)
        sparkles(f, 540, 1040, t, tn, 10, 200)
    wui(f, "the tears", "[NEVER CAME]", t, st_("S22") + 0.1, acc=YEL_, size=170)
    return finish(f, n)


# ---- S23: PART 5 — how do you BEAT the trap today? (hero pose with the knife) ----
def shot_S23(t, n):
    f = stage("kitchen", (255, 236, 190), 540, 1000, 430); u = lt(t, "S23"); tiles(f, 250, 1000)
    rays(f, 540, 1000, 780, (255, 250, 220), 0.3, t)
    chub(f, 540, 1480, 1.0, la=(20, 10), ra=(150, 175), mouth=2, expr="happy", brow="up", look=(0, -0.4), bob=6 * abs(math.sin(t * 5)),
         hold=scale_el(knife_el(), 0.55), hold_off=(110, -10), hold_front=True)
    chapter_card(f, t, st_("S23") + 0.02, 5, "BEAT THE TRAP", y=760, dur=1.4, col=YEL_)
    ui_word(f, "how do you", "[BEAT] the trap?", 470, t, st_("S23") + 0.05, col=INK, acc=RED_, size=170)
    return finish(f, n)


# ---- S24: Cornell filmed onion cutting in SLOW MOTION (high-speed camera look) ----
CUTP = (560, 1010)


def slowmo_scene(f, t, t0, slow=0.12, n=40, dull=False, spd=900):
    comp(f, scale_el(onion_el(False), 1.25), 560, 1150)
    k = clamp((t - t0) * slow * 3)
    knife_at(f, 120, 860 + 150 * k, -6, 1.2, dull)
    if k > 0.3: droplets(f, CUTP[0], CUTP[1], t, t0 + 0.3 / (slow * 3), n, spd, 70, 90, slow, 5, (226, 250, 190), 1600, 9)


def shot_S24(t, n):
    f = stage("steel", (210, 220, 240), 540, 1000, 380); u = lt(t, "S24")
    f *= 0.82
    slowmo_scene(f, t, st_("S24") + 0.1, 0.12)
    slowmo_ui(f, t, "SLOW MOTION")
    tc = T("e2", "Cornell") - 0.1
    if t >= tc: comp(f, chip("CORNELL, 2025", INK, YEL_, 30), 540, 1300, op=clamp((t - tc) / 0.3))
    comp(f, chip("Source: Wu et al., PNAS, 2025 (Cornell)", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "scientists filmed it in", "[SLOW MOTION]", t, st_("S24") + 0.1, acc=YEL_, size=150)
    return finish(f, n)


# ---- S24b: super slow motion — the juice droplets burst out of the cut ----
def shot_S24b(t, n):
    g = stage("tear", (200, 230, 255), 540, 1000, 380); u = lt(t, "S24b")
    g *= 0.8
    slowmo_scene(g, t, st_("S24") + 0.1, 0.12, 60)
    k = ramp(t, st_("S24b"), 1.2); f = np.ascontiguousarray(cam(g, 1 + 0.5 * k, CUTP[0], CUTP[1], 0, 80 * k), np.float32)
    slowmo_ui(f, t, "SUPER SLOW")
    label_at(f, "ONION JUICE DROPLETS", 760, 1290, t, st_("S24b") + 0.5, 620, 1000, bg=(60, 110, 40))
    wui(f, "", "[SUPER SLOW]", t, st_("S24b") + 0.05, acc=YEL_, size=200)
    return finish(f, n)


# ---- S25: a DULL knife squashes more cells -> more juice (contrast panels: dull vs sharp) ----
def shot_S25(t, n):
    f = stage("cream", (240, 246, 255), 540, 1000, 380); u = lt(t, "S25")
    t0 = st_("S25") + 0.2
    def L(g):
        comp(g, scale_el(onion_half_el(220), 0.85), 330, 1260)
        knife_at(g, 180, 1100 + 30 * math.sin(t * 6), -12, 0.5, True)
        droplets(g, 330, 1170, t, t0, 46, 700, 50, 90, 0.5, 3, (226, 250, 190), 1400, 9)
    def R(g):
        comp(g, scale_el(onion_half_el(220), 0.85), 750, 1260)
        knife_at(g, 600, 1100 + 30 * math.sin(t * 6), -12, 0.5, False)
        droplets(g, 750, 1170, t, t0, 7, 450, 40, 90, 0.5, 4, (226, 250, 190), 1400, 9)
    split_contrast(f, t, st_("S25") + 0.05, L, R, "DULL KNIFE", "SHARP KNIFE", (230, 80, 60), (40, 170, 110), 640, 1400)
    tj = T("e3", "juice") - 0.15
    if t >= tj: slam(f, chip("MORE JUICE", RED_, WHITE, 32), 330, 770, -6, t, tj)
    ui_word(f, "a dull knife sprays", "[MORE JUICE]", 470, t, st_("S25") + 0.05, col=INK, acc=RED_, size=170)
    return finish(f, n)


# ---- S26: fast chopping shoots drops at 40 metres a second (speed readout + streaking drop) ----
def shot_S26(t, n):
    f = stage("red", (255, 200, 170), 540, 1000, 400); u = lt(t, "S26")
    speed_lines(f, t, 1.0, 760, 1300, 18, 3)
    x_ = -100 + ((u * 1400) % 1400)
    for j in range(6): cv2.circle(f, (int(x_ - 40 * j), 1000), int(26 - 3 * j), C((226, 250, 190)), -1, cv2.LINE_AA)
    cv2.circle(f, (int(x_), 1000), 30, C(INK), 4, cv2.LINE_AA)
    tf = T("e4", "forty") - 0.5
    v = count_up(t, tf, 40, 0.6) if t >= tf else 0
    comp(f, readout_el(f"{v} m/s", YEL_, INK, 90), 540, 1220)
    if t >= tf + 0.6: comp(f, chip("about 144 km/h: faster than highway traffic", INK, WHITE, 24), 540, 1370, op=clamp((t - tf - 0.6) / 0.3))
    comp(f, chip("Source: Wu et al., PNAS 2025; Physics World", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "drops fly at up to", f"[{v} m/s]" if t >= tf else "[FULL SPEED]", t, st_("S26") + 0.05, acc=YEL_, size=210)
    return finish(f, n)


# ---- S27: use a SHARP knife and cut SLOWLY (Chubby chops slowly; checks pop) ----
def shot_S27(t, n):
    f = stage("kitchen", (255, 246, 214), 540, 900, 420); u = lt(t, "S27"); tiles(f, 250, 1000)
    board_onion(f, t, 760, 1395, 0.75, 0.7, face=True, mood="sad")
    chopper(f, t, 330, 1470, 1.0, 1.4, st_("S27"), expr="happy", mouth=0, look=(1, 0.5), up=1160, down=1250)
    ts = T("e5", "sharp") - 0.15; tl = T("e5", "slowly.") - 0.15
    if t >= ts:
        sparkles(f, 760, 1170, t, ts, 8, 120)
        comp(f, check_el(40, True), 700, 740, scale=pin(t, ts, 0.25)); comp(f, chip("SHARP", INK, WHITE, 30), 700, 820)
    if t >= tl: comp(f, check_el(40, True), 900, 740, scale=pin(t, tl, 0.25)); comp(f, chip("SLOW", INK, WHITE, 30), 900, 820)
    ui_word(f, "use a sharp knife,", "[CUT SLOWLY]", 470, t, st_("S27") + 0.05, col=INK, acc=(34, 140, 80), size=180)
    return finish(f, n)


# ---- S28: cooked onions? HEAT breaks the enzyme (pan on flames; dizzy enzyme) ----
def shot_S28(t, n):
    f = stage("orange", (255, 210, 150), 540, 1000, 420); u = lt(t, "S28")
    flames_row(f, 460, 1340, 520, t, 140)
    comp(f, scale_el(pan_el(), 1.0), 600, 1230)
    steam(f, 470, 1080, t, 1.2); steam(f, 620, 1060, t + 1, 1.0)
    th = T("e6", "Heat") - 0.15
    if t >= th:
        rot_comp(f, scale_el(enz_el(1, 0.1, "dizzy"), 0.75), 780, 850 + 10 * math.sin(t * 5), 20 * math.sin(t * 4), pin(t, th, 0.3), 1.0, 0.2)
        label_at(f, "ENZYME BROKEN", 330, 800, t, th + 0.3, 660, 850, bg=RED_)
    ui_word(f, "cooked onions?", "[HEAT] breaks the enzyme", 470, t, st_("S28") + 0.05, col=WHITE, acc=YEL_, size=140, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S28b: the trap can't fire (Chubby happily eats a cooked onion ring; TRAP OFF stamp) ----
def shot_S28b(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 420); u = lt(t, "S28b")
    m, c = munch(t, 0.3)
    chub(f, 380, 1480, 1.05, la=(20, 10), ra=(148, -130), mouth=m, expr="happy", brow="up", look=(1, 0), hold=scale_el(ring_el(), 0.7), hold_off=(-30, -10), hold_front=True)
    slam(f, stamp_el("TRAP OFF", (34, 160, 90), 56), 780, 900, -8, t, T("e6", "can't") - 0.1)
    wui(f, "the trap", "[CAN'T FIRE]", t, st_("S28b") + 0.05, acc=(34, 140, 80), size=200)
    return finish(f, n)


# ---- S29: RECAP — two chemicals kept apart -> your knife mixes them -> the gas finds your eyes (+ whole chain lights up) ----
def shot_S29(t, n):
    f = stage("onion", (255, 210, 245), 540, 1000, 420); u = lt(t, "S29")
    items = [(scale_el(mix_icon_el(), 0.9), "KEPT APART"), (scale_el(knife_el(), 0.42), "KNIFE MIXES"), (scale_el(gas_el("sly"), 0.62), "GAS FINDS EYES")]
    ts = [T("f1", "two") - 0.15, T("f1", "knife") - 0.15, T("f1", "gas") - 0.15]
    recap_steps(f, items, 960, t, ts, 330, 1.3)
    cur = min(5, int(max(0, t - ts[0]) / 0.5)) if t >= ts[0] else -1
    chain(f, t, cur, ts[0] + cur * 0.5)
    wui(f, "", "[REMEMBER]", t, st_("S29") + 0.05, acc=YEL_, size=200)
    return finish(f, n)


# ---- S30: send it + FreshNestHub sting ----
def shot_S30(t, n):
    f = stage("kitchen", (255, 236, 200), 540, 880, 420); u = lt(t, "S30")
    vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.3
        comp(f, scale_el(phone2_el("why do onions make me cry??", "it's a TRAP. sharp knife!", pr), 0.82), 650, 950, scale=pin(t, st_("S30")))
        if pr and t < T("f2", "Send") + 0.75:
            rr = (t - T("f2", "Send") - 0.3) / 0.45
            cv2.circle(f, (650, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        hx, hy = head_pos(250, 1480, 0.8)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(148, -130), mouth=2, expr="happy", brow="up", look=(1, 0),
             hold=scale_el(onion_el(True, "sly"), 0.3), hold_off=(-30, -16), hold_front=True)
        tear_streams(f, hx, hy, 0.8, t, st_("S30") + 0.3, 0.7, 0.7)
        ui_word(f, "send to the friend who", "[CRIES] at onions", 420, t, T("f2", "friend") - 0.1, col=INK, acc=TEAR_D, size=150)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INK, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, 400, 1480, 0.7, la=(20, 10), ra=(148, -130), mouth=munch(t, 0.3)[0], expr="happy", brow="up", hold=scale_el(ring_el(), 0.45), hold_off=(-20, -10), hold_front=True)
        comp(f, scale_el(onion_el(True, "happy"), 0.42), 700, 1380)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TC, 0.45, 20), (TP, 0.3, 12), (T("i2", "trap!") - 0.1, 0.35, 16), (T("i2", "knife") - 0.05, 0.5, 24), (T("i3", "can't") - 0.1, 0.3, 12),
           (T("a1", "An") + 0.6, 0.25, 10), (T("a4", "enzyme.") - 0.3, 0.25, 10),
           (TCUT, 0.5, 26), (T("b2", "breaks") - 0.15, 0.35, 16), (T("b2", "mix.") - 0.05, 0.3, 12), (T("b3", "snips") - 0.1, 0.3, 14),
           (T("b4", "wobbly.") - 0.15, 0.35, 14), (T("b4", "grabs") - 0.1, 0.3, 14), (T("b5", "gas.") - 0.2, 0.35, 16), (T("b5", "tear") - 0.15, 0.3, 12),
           (T("b6", "eyes.") - 0.1, 0.4, 18), (T("b7", "sting.") - 0.15, 0.35, 16), (T("b8", "flood") - 0.15, 0.4, 18),
           (T("c2", "protect") - 0.1, 0.3, 12), (T("d1", "tear-free") - 0.1, 0.3, 12), (st_("S20b") + 0.25, 0.3, 14),
           (T("d3", "off.") - 0.2, 0.35, 16), (T("d4", "never") - 0.15, 0.4, 18), (T("e4", "forty") + 0.1, 0.4, 18),
           (T("e3", "juice") - 0.15, 0.25, 10), (T("e6", "Heat") - 0.15, 0.25, 10), (T("e6", "can't") - 0.1, 0.35, 14)]


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
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "iris" and dt < 0.42:
            cx, cy = IRIS.get(sh["id"], (540, 1000))
            f = iris_mix(rs(SHOTS[i - 1]["id"], t, n), f, dt / 0.42, cx, cy)
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
