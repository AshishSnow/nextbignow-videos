# ================= shots: FreshNestHub 14 — "Coffee doesn't give you energy" (caffeine = a fake key for the sleepy signal) =================
# COLOUR SCRIPT (ep 14): warm CAFE browns/latte = the coffee moments; NEURO deep blue + mint cells = inside your brain; NIGHT /
# DUSK purple = sleep + sleepy keys (adenosine is purple everywhere); RED = the crash; HONEY yellow = the bees bonus.
# CRAFT (ep 14): CHARTS ON VIDEO (anim_fx.day_graph) - a graph of the day drawn while you watch: sleepy keys piling up, what you
# FEEL vs your REAL tiredness (the hidden gap), the crash, and caffeine halving toward bedtime. One finding per chart (title =
# the finding), direct labels on the lines, no legend, the line wipes left -> right with the voice, Chubby's head rides the
# 'now' point (presenter interacting with the chart). Chubby gets a new 'sleepy' expression (heavy lids + bags).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Not") - 0.15, "punch"), ("S1b", T("i2", "It") - 0.1, "whip"),
    ("S2", T("i3", "And") - 0.15, "whip"),
    ("S3", T("a1", "Here's") - 0.2, "flash"), ("S4", T("a2", "And") - 0.2, "whip"),
    ("S5", T("a3", "Think") - 0.2, "zoom"), ("S5b", T("a3", "The") - 0.15, "whip"),
    ("S6", T("a4", "Your") - 0.2, "focus"), ("S6b", T("a5", "When") - 0.2, "whip"), ("S6c", T("a5", "And") - 0.1, "punch"),
    ("S7", T("a6", "That's") - 0.2, "whip"),
    ("S8", T("b1", "Now,") - 0.2, "flash"), ("S9", T("b2", "The") - 0.2, "iris"),
    ("S10", T("b3", "And") - 0.2, "whip"), ("S11", T("b4", "So") - 0.2, "iris"),
    ("S12", T("b5", "It") - 0.2, "whip"), ("S13", T("b6", "The") - 0.2, "whip"), ("S13b", T("b6", "So") - 0.1, "punch"),
    ("S14", T("b7", "But") - 0.2, "focus"),
    ("S15", T("c1", "But") - 0.2, "flash"), ("S16", T("c2", "The") - 0.2, "whip"), ("S17", T("c3", "When") - 0.2, "whip"),
    ("S18", T("c4", "That's") - 0.15, "punch"), ("S18b", T("c4", "One") - 0.15, "whip"),
    ("S19", T("d1", "So") - 0.2, "flash"), ("S20", T("d2", "Your") - 0.2, "iris"), ("S21", T("d3", "So") - 0.2, "whip"),
    ("S22", T("d4", "In") - 0.2, "focus"), ("S23", T("d5", "They") - 0.2, "whip"), ("S23b", T("d5", "And") - 0.1, "punch"),
    ("S24", T("d6", "So") - 0.2, "whip"),
    ("S25", T("e1", "And") - 0.2, "flash"), ("S26", T("e2", "Your") - 0.2, "whip"), ("S26b", T("e2b", "So") - 0.1, "zoom"),
    ("S27", T("e3", "Here's") - 0.2, "flash"), ("S28", T("e4", "Coffee") - 0.2, "whip"), ("S29", T("e5", "Bees") - 0.2, "whip"),
    ("S30", T("e6", "So") - 0.2, "whip"), ("S30b", T("e6", "Sound") - 0.1, "punch"),
    ("S31", T("f1", "Remember:") - 0.2, "focus"), ("S32", T("f2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
# iris match cuts: where the circle opens, in the PREVIOUS shot's picture (a round/central object)
IRIS = {"S9": (470, 1020), "S11": (540, 1090), "S20": (690, 1030)}


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


def en_(sid): return SHOT[sid]["end"]


# ---------------- shared pieces ----------------
def real_tired(h): return 0.06 + 0.8 * clamp((h - 7) / 16) ** 1.1


TCOF, TOFF = 10.0, 15.6          # coffee at 10 AM; caffeine 'wears off' around 3-4 PM in the explainer graph


def felt_tired(h):
    if h < TCOF: return real_tired(h)
    low = 0.08
    if h < TCOF + 0.6: return real_tired(TCOF) + (low - real_tired(TCOF)) * eio((h - TCOF) / 0.6)
    plateau = low + 0.02 * (TOFF - TCOF - 0.6)
    if h < TOFF: return low + 0.02 * (h - TCOF - 0.6)
    k = eio(clamp((h - TOFF) / 0.7)); return plateau * (1 - k) + (real_tired(h) + 0.05 * math.exp(-max(0.0, h - TOFF - 0.7) * 2)) * k


def caf_left(h, h0=14.0, half=4.5): return 0.0 if h < h0 else 0.92 * 0.5 ** ((h - h0) / half)


def rider(f, head, s=0.5, expr="n", mouth=0, t=0.0, brow="n", dy=-70):
    """the presenter on the chart: Chubby's head rides the line's 'now' point."""
    if head is None: return
    chub_head_only(f, head[0], head[1] + dy, s, t, mouth=mouth, expr=expr, brow=brow)


def sip_pose(f, x, y, s, t, expr="happy", brow="up", look=(0.6, -0.2), gulp=True, la=(20, 10)):
    """Chubby drinking from a mug held at his mouth (hand to mouth + hold_front)."""
    m = "o" if gulp and (t * 3) % 1 < 0.5 else 0
    return chub(f, x, y, s, la=la, ra=(148, -128), mouth=m, expr=expr, brow=brow, look=look, bob=3 * math.sin(t * 6),
                hold=scale_el(mug_el(), 0.42), hold_off=(-40, -40), hold_front=True)


# ---- S0: HOOK — Chubby gulps a giant coffee, his ENERGY battery fills to 100%... at "doesn't" the charge was a sticker ----
TD = T("i1", "doesn't") - 0.1; TE = T("i1", "energy?") - 0.1


def shot_S0(t, n):
    f = stage("cafe", (255, 214, 150), 540, 980, 430)
    rays(f, 540, 980, 760, (255, 230, 190), 0.18, t)
    if t < TD:
        sip_pose(f, 400, 1480, 1.08, t, expr="happy")
        steam(f, 330, 930, t, 1.0)
    else:
        chub(f, 400, 1480, 1.08, la=(20, 10), ra=(70, 40), mouth="o", expr="wow", brow="up", look=(1, -0.6),
             hold=scale_el(mug_el(), 0.42), hold_off=(30, -20), hold_front=True, squash=0.3 * math.exp(-(t - TD) * 6))
    lv = clamp(0.2 + 0.8 * eo(clamp(t / max(0.4, TD - 0.25))))
    bx, by = 760, 800 + 6 * math.sin(t * 3)
    if t < TD:
        comp(f, scale_el(battery_el(lv), 0.82), bx, by)
        comp(f, chip("ENERGY", INK, (60, 210, 90), 30), bx, by - 120)
        sparkles(f, bx, by, t, 0.9, 10, 200, (200, 255, 200))
    else:
        comp(f, scale_el(battery_el(0.0, "0%"), 0.82), bx, by)
        comp(f, chip("NEW ENERGY", INK, RED_, 30), bx, by - 120)
        q = t - TD
        rot_comp(f, sticker_el("100%"), bx + 60 * q + 30, by + 600 * q * q + 80 * q, -40 * q - 5, 0.95, clamp(1 - (q - 0.5) / 0.4), 0.3)
        comp(f, burst_el("FAKE?!", RED_, WHITE, 52), 820, 1120, scale=pin(t, TD + 0.25, 0.22))
    ui_word(f, "do you know coffee gives you", "[NO] energy?", 470, t, 0.1, col=WHITE, acc=YEL_, size=210, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S1: not one bit (battery at 0, Chubby stares at it) ----
def shot_S1(t, n):
    f = stage("red", (255, 200, 170), 540, 1000, 420); u = lt(t, "S1")
    rot_comp(f, scale_el(battery_el(0.0, "0%"), 1.3), 560, 1000 + 6 * math.sin(t * 3), -4 + 2 * math.sin(t * 2), pin(t, st_("S1"), 0.3), 1.0, 0.35)
    chub(f, 230, 1490, 0.75, la=(20, 10), ra=(70, 40), mouth="o", expr="wow", brow="up", look=(1, -0.6), hold=scale_el(mug_el(), 0.32), hold_off=(30, -20), hold_front=True)
    tb = T("i2", "bit.") - 0.15
    if t >= tb: slam(f, stamp_el("NOT ONE BIT", INK, 46), 680, 1300, -6, t, tb)
    wui(f, "not one", "[BIT]", t, st_("S1") + 0.05, acc=YEL_, size=240)
    return finish(f, n)


# ---- S1b: it just HIDES how tired you are (big sleepy face; a smiley mask slides over it) ----
def shot_S1b(t, n):
    f = stage("dusk", (255, 190, 200), 540, 1000, 440); u = lt(t, "S1b")
    hx, hy = 540, 1050; s_ = 2.5
    chub_head_only(f, hx, hy, s_, t, mouth=0, expr="sleepy", brow="sad", look=(0, 0.4))
    th = T("i2", "hides") - 0.15
    k = ramp(t, th - 0.15, 0.35)
    rot_comp(f, mask_el(), hx + 600 * (1 - k) + 130, hy + 150 + 30 * (1 - k), 8 * (1 - k) + 6, 0.9, 1.0, 0.3)
    if t >= th + 0.3:
        label_at(f, "REALLY TIRED", 230, 700, t, th + 0.4, 400, 960, bg=ADE_D)
    wui(f, "it just", "[HIDES] it", t, st_("S1b") + 0.05, acc=(255, 220, 120), size=230)
    return finish(f, n)


# ---- S2: the tiredness comes back later... WITH INTEREST (a loan) — open loop, paid off at the crash ----
def shot_S2(t, n):
    f = stage("latte", (255, 246, 226), 540, 1000, 420); u = lt(t, "S2")
    rot_comp(f, loan_doc_el(), 690, 1040 + 6 * math.sin(t * 3), 5, 1.0 * pin(t, st_("S2"), 0.3), 1.0, 0.35)
    chub(f, 260, 1490, 0.85, la=(20, 10), ra=(20, 10), mouth=0, expr="sus", brow="sad", look=(1, -0.2))
    sweat(f, 330, 1000, t, 3, 0.8)
    tb = T("i3", "back") - 0.15; ti = T("i3", "interest.") - 0.2
    if t >= tb: slam(f, stamp_el("PAY IT BACK", RED_, 46), 690, 1180, -8, t, tb)
    if t >= ti:
        slam(f, tag_el("+ INTEREST", (40, 150, 70), WHITE, 48), 690, 760, 6, t, ti)
        comp(f, chip("COMING UP", INK, YEL_, 30), 540, 1440, op=clamp((t - ti - 0.3) / 0.3))
    ui_word(f, "the tiredness comes", "[BACK]", 470, t, st_("S2") + 0.05, col=INK, acc=RED_, size=230)
    return finish(f, n)


# ---- S3: PART 1 — all day, your brain cells use energy (push from Chubby's head into his busy brain cells) ----
def _s3_far(t):
    f = stage("sky", (236, 248, 255), 540, 980, 420)
    chub(f, 540, 1480, 1.15, la=(20, 10), ra=(20, 10), mouth=talk(t), expr="happy", brow="up", look=(0, -0.3))
    hx, hy = head_pos(540, 1480, 1.15)
    comp(f, scale_el(brain_el(), 0.32), hx, hy - 30, op=0.85)
    return f


def bolt(f, x, y, s=1.0, col=(255, 230, 60)):
    P = np.array([[x - 10 * s, y - 26 * s], [x + 8 * s, y - 4 * s], [x - 2 * s, y - 4 * s], [x + 10 * s, y + 26 * s], [x - 8 * s, y + 2 * s], [x + 2 * s, y + 2 * s]], np.int32)
    cv2.polylines(f, [P], True, C(INK), 5, cv2.LINE_AA); cv2.fillPoly(f, [P], C(col), cv2.LINE_AA)


def _s3_near(t):
    f = stage("neuro")
    for i, (cx, cy) in enumerate(((300, 880), (790, 1030), (430, 1260))):
        brain_cell(f, cx, cy, 300, t + i, (), 0.0, 170, seed=i)
        for j in range(3):
            a = t * 2.5 + j * 2.1 + i; bolt(f, cx + 190 * math.cos(a), cy + 120 * math.sin(a), 1.3)
    return f


def shot_S3(t, n):
    u = lt(t, "S3"); tz = T("a1", "All") - 0.25
    hx, hy = head_pos(540, 1480, 1.15)
    f = zoom_through(t, tz, 0.9, lambda: _s3_far(t), lambda: _s3_near(t), hx, hy - 30, 6.0)
    f = np.ascontiguousarray(f, np.float32)
    chapter_card(f, t, st_("S3") + 0.05, 1, "THE SLEEPY SIGNAL", y=1400, dur=1.4, col=ADE_L)
    if t >= tz + 0.9:
        label_at(f, "BRAIN CELLS", 760, 690, t, tz + 1.0, 400, 820, bg=NEU_D)
        comp(f, chip("WORKING = USING ENERGY", INK, YEL_, 28), 540, 1460, op=clamp((t - tz - 1.3) / 0.3))
    if t < tz + 0.5: ui_word(f, "here's how it", "[WORKS]", 470, t, st_("S3") + 0.1, col=INK, acc=RED_, size=230, out=tz + 0.4)
    else: wui(f, "brain cells use", "[ENERGY]", t, tz + 0.5, acc=YEL_, size=230)
    return finish(f, n)


# ---- S4: as they work, ADENOSINE builds up (purple keys float off the busy cell) ----
def shot_S4(t, n):
    f = stage("neuro", (120, 180, 255), 540, 1000, 380); u = lt(t, "S4")
    brain_cell(f, 540, 1200, 560, t, (), 0.0, 300, seed=2)
    bolt(f, 380, 1150, 1.4); bolt(f, 700, 1230, 1.4)
    nk = int(clamp(u / max(0.5, en_("S4") - st_("S4") - 0.3)) * 9) + 1
    rng = np.random.default_rng(5)
    for i in range(nk):
        a = rng.uniform(-2.6, -0.5); r0 = rng.uniform(220, 330); ph = t * 0.8 + i
        x = 540 + r0 * math.cos(a) * 1.4 + 20 * math.sin(ph); y = 1080 + r0 * math.sin(a) * 1.2 + 14 * math.cos(ph)
        rot_comp(f, scale_el(skey_el("sleepy"), 0.34), x, y, 20 * math.sin(ph), pin(t, st_("S4") + i * 0.18, 0.3))
    ta = T("a2", "adenosine") - 0.15
    if t >= ta: label_at(f, "ADENOSINE", 540, 1460, t, ta, 560, 1010, bg=ADE_D)
    wui(f, "a chemical called", "[ADENOSINE]", t, st_("S4") + 0.05, acc=ADE_L, size=170)
    return finish(f, n)


# ---- S5: think of it as SLEEPY KEYS (define on sight: name card) ----
def shot_S5(t, n):
    f = stage("night", (200, 170, 255), 540, 1000, 440); u = lt(t, "S5")
    rays(f, 540, 1040, 760, (220, 200, 255), 0.25, t)
    rot_comp(f, scale_el(skey_el("sleepy"), 1.7), 540, 1040 + 10 * math.sin(t * 3), -8 + 5 * math.sin(t * 2), pin(t, st_("S5") + 0.05, 0.3), 1.0, 0.35)
    zzs(f, 700, 900, t, 3, WHITE, 1.0)
    tk = T("a3", "keys.") - 0.2
    if t >= tk: comp(f, chip("ADENOSINE = SLEEPY KEY", INK, ADE_L, 36), 540, 1360, op=clamp((t - tk) / 0.2), scale=pin(t, tk, 0.3))
    wui(f, "think of it as", "[SLEEPY KEYS]", t, st_("S5") + 0.05, acc=ADE_L, size=170)
    return finish(f, n)


# ---- S5b: the longer you're awake, the more pile up (CHART: sleepy keys across the day; Chubby rides the line) ----
def shot_S5b(t, n):
    f = stage("cream", (240, 236, 255), 540, 980, 420); u = lt(t, "S5b")
    d_ = en_("S5b") - st_("S5b")
    now = 7 + 16.5 * eio(clamp((u - 0.2) / max(0.5, d_ - 0.4)))
    X, Y, heads = day_graph(f, t, now, [(real_tired, ADE, "SLEEPY KEYS", 7, (-200, -40))], y0=720, y1=1270,
                            title="AWAKE LONGER = MORE SLEEPY KEYS")
    sun_icon(f, X(8.2), 790, 28, t); moon_icon(f, X(23), 790, 28, (255, 252, 244))
    for j in range(int(max(0.0, now - 8) / 2.0)):
        hh = 8.6 + j * 2.0; rot_comp(f, scale_el(skey_el("sleepy"), 0.2), X(hh), Y(real_tired(hh)) + 60, 20 * math.sin(j), 1.0)
    rider(f, heads[0], 0.42, "sleepy" if now > 17 else "n", 0, t, "sad" if now > 17 else "n")
    return finish(f, n)


# ---- S6: your brain cells have tiny LOCKS for those keys (pre-training: name the lock) ----
LK = (-210, 0, 210)


def shot_S6(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S6")
    tl = T("a4", "locks") - 0.2
    locks = [(dx, None, 0, 0.0) for i, dx in enumerate(LK) if t >= tl + 0.15 * i - 0.6]
    brain_cell(f, 540, 1240, 820, t, locks, 0.0, 420, seed=3)
    rot_comp(f, scale_el(skey_el("sleepy"), 0.5), 860, 760 + 10 * math.sin(t * 3), -20, 1.0)
    if t >= tl:
        label_at(f, "LOCK", 230, 800, t, tl + 0.2, 330, 990, bg=LOCK_D)
        comp(f, chip("science name: receptor", INK, WHITE, 24), 540, 1462, op=clamp((t - tl - 0.4) / 0.3))
    wui(f, "brain cells have tiny", "[LOCKS]", t, st_("S6") + 0.05, acc=(140, 255, 230), size=220)
    return finish(f, n)


# ---- S6b: when a sleepy key CLICKS in, the cell slows down ----
def shot_S6b(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S6b")
    tc = T("a5", "clicks") - 0.12; ts = T("a5", "slows") - 0.15
    k = ramp(t, st_("S6b") + 0.1, max(0.3, tc - st_("S6b") - 0.1))
    turn = ramp(t, tc, 0.18)
    dim = ramp(t, ts, 0.5)
    locks = [(LK[0], None, 0, 0.0), (LK[1], "skey" if t >= tc else None, -90 * turn, turn), (LK[2], None, 0, 0.0)]
    pts = brain_cell(f, 540, 1240, 820, t, locks, 0.6 * dim, 420, seed=3, sleepy=dim > 0.5)
    if t < tc:
        x_ = 900 - 360 * k; y_ = 640 + (pts[1][1] - 60 - 640) * k - 160 * math.sin(math.pi * k)
        rot_comp(f, scale_el(skey_el("sleepy"), 0.5), x_, y_, 90 * k, 1.0)
    else:
        comp(f, burst_el("CLICK!", YEL_, INK, 50), 800, 760, scale=pin(t, tc, 0.22))
    if t >= ts:
        comp(f, chip("SLOW DOWN", ADE_D, WHITE, 36), 540, 1460, op=clamp((t - ts) / 0.2), scale=pin(t, ts, 0.3))
        zzs(f, 620, 1150, t, 3, WHITE, 0.8)
    wui(f, "the cell", "[SLOWS DOWN]", t, st_("S6b") + 0.05, acc=ADE_L, size=190)
    return finish(f, n)


# ---- S6c: and you feel TIRED (big Chubby yawns, lids heavy) ----
def shot_S6c(t, n):
    f = stage("dusk", (255, 200, 210), 540, 1000, 440); u = lt(t, "S6c")
    yawn = 3 if 0.15 < u < 1.3 else 0
    chub(f, 540, 1480, 1.15, la=(150, 175) if yawn else (20, 10), ra=(150, 175) if yawn else (20, 10), mouth=yawn, expr="sleepy", brow="sad", look=(0, 0.3),
         lean=-4 * math.sin(t * 1.5), bob=4 * math.sin(t * 2))
    zzs(f, 720, 900, t, 3, WHITE, 1.0)
    wui(f, "you feel", "[TIRED]", t, st_("S6c") + 0.05, acc=ADE_L, size=250)
    return finish(f, n)


# ---- S7: that's how your body knows it's time to sleep (Chubby in bed, nightcap, stars) ----
def shot_S7(t, n):
    f = stage("night", (255, 244, 200), 800, 760, 120); u = lt(t, "S7")
    for i in range(14):
        rng = np.random.default_rng(i); sx_, sy_ = rng.uniform(80, 1000), rng.uniform(300, 800)
        cv2.circle(f, (int(sx_), int(sy_)), int(3 + 2 * (math.sin(t * 3 + i) > 0.5)), C((255, 250, 220)), -1, cv2.LINE_AA)
    chub(f, 470, 1380, 1.0, la=(20, 10), ra=(20, 10), mouth=0, expr="happy" if u > 1.0 else "sleepy", brow="sad", look=(0, 0.3), sit=True, bob=3 * math.sin(t * 1.6))
    hx, hy = head_pos(470, 1380, 1.0); nightcap(f, hx, hy, 1.0)
    comp(f, bed_el(), 540, 1360)
    zzs(f, 640, 860, t, 3, WHITE, 1.1)
    wui(f, "time to", "[SLEEP]", t, st_("S7") + 0.05, acc=(255, 244, 200), size=250)
    return finish(f, n)


# ---- S8: PART 2 — now... you drink a COFFEE ----
def shot_S8(t, n):
    f = stage("cafe", (255, 214, 150), 540, 980, 430); u = lt(t, "S8")
    tc = T("b1", "coffee.") - 0.2
    if t < tc:
        chub(f, 470, 1480, 1.1, la=(20, 10), ra=(70, 40), mouth=0, expr="sleepy", brow="sad", look=(1, 0.2), hold=scale_el(mug_el(), 0.45), hold_off=(40, -20), hold_front=True)
        steam(f, 650, 1080, t, 1.0)
    else:
        sip_pose(f, 470, 1480, 1.1, t, expr="happy"); steam(f, 400, 900, t, 1.0)
        sparkles(f, 470, 1000, t, tc + 0.2, 10, 240)
    chapter_card(f, t, st_("S8") + 0.02, 2, "THE FAKE KEY", y=1420, dur=1.4, col=CAF_L)
    wui(f, "you drink a", "[COFFEE]", t, st_("S8") + 0.1, acc=(255, 214, 150), size=230)
    return finish(f, n)


# ---- S9: caffeine travels in your BLOOD, all the way to your BRAIN (route drawn up through Chubby) ----
def shot_S9(t, n):
    f = stage("red", (255, 210, 190), 540, 1000, 440); u = lt(t, "S9")
    chub(f, 540, 1500, 1.25, la=(20, 10), ra=(20, 10), mouth=0, expr="n", brow="n", look=(0, -0.5))
    hx, hy = head_pos(540, 1500, 1.25)
    comp(f, scale_el(brain_el(), 0.42), hx, hy - 40)
    P = [(540, 1310), (610, 1240), (500, 1160), (575, 1080), (540, 990), (hx, hy - 30)]
    cv2.polylines(f, [np.array(P, np.int32)], False, C(INK), 30, cv2.LINE_AA); cv2.polylines(f, [np.array(P, np.int32)], False, C((220, 40, 50)), 20, cv2.LINE_AA)
    for j in range(7):
        k = ((u * 0.55) + j / 7) % 1.0
        px, py = path_point(P, k); caf_dot(f, px, py, 12)
    tb = T("b2", "blood,") - 0.15; tr = T("b2", "brain.") - 0.15
    if t >= tb: label_at(f, "BLOOD", 820, 1280, t, tb, 620, 1220, bg=(170, 20, 30))
    if t >= tr:
        label_at(f, "BRAIN", 840, 760, t, tr, hx + 90, hy - 50, bg=BRAIN_D)
        glow(f, hx, hy - 40, 130, (255, 220, 160), 0.5 * ramp(t, tr, 0.3))
    comp(f, chip("CAFFEINE", CAF, WHITE, 28), 260, 1300, op=clamp((u - 0.3) / 0.3))
    if t < tr - 0.2: wui(f, "it travels in your", "[BLOOD]", t, st_("S9") + 0.05, acc=(255, 190, 180), size=230, out=tr - 0.25)
    else: wui(f, "all the way to your", "[BRAIN]", t, tr - 0.2, acc=(255, 214, 150), size=230)
    return finish(f, n)


# ---- S10: the trick — caffeine looks a lot LIKE adenosine (look-alike panels) ----
def shot_S10(t, n):
    f = stage("cream", (250, 244, 236), 540, 1000, 380); u = lt(t, "S10")
    tc = T("b3", "Caffeine") - 0.2; tl = T("b3", "like") - 0.15
    def L(g): rot_comp(g, scale_el(skey_el("sleepy"), 0.95), 330, 1040 + 8 * math.sin(t * 3), 60, 1.0)
    def R(g): rot_comp(g, scale_el(ckey_el("sly"), 0.95), 750, 1040 + 8 * math.sin(t * 3 + 1), 60, 1.0)
    split_contrast(f, t, st_("S10") + 0.05, L, R, "ADENOSINE", "CAFFEINE", ADE, CAF, 640, 1400, t_r=tc)
    if t >= tl:
        slam(f, stamp_el("LOOK-ALIKES", RED_, 48), 540, 1250, -6, t, tl)
        comp(f, chip("almost the same shape", INK, WHITE, 26), 540, 1462, op=clamp((t - tl - 0.3) / 0.3))
    if t < tc: ui_word(f, "here's the", "[TRICK]", 470, t, st_("S10") + 0.05, col=INK, acc=RED_, size=240, out=tc - 0.05)
    else: ui_word(f, "caffeine looks", "[LIKE] adenosine", 470, t, tc - 0.05, col=INK, acc=CAF, size=170)
    return finish(f, n)


# ---- S11: it slips into the same lock... but it CAN'T TURN it (close-up lock; key jiggles) ----
def shot_S11(t, n):
    f = stage("teal", (160, 240, 230), 540, 1000, 440); u = lt(t, "S11")
    tc = T("b4", "can't") - 0.15
    k = ramp(t, st_("S11") + 0.1, 0.6)
    comp(f, scale_el(lock_el(0.0), 1.7), 540, 1150)
    jig = 14 * math.sin(t * 28) * ramp(t, tc, 0.1) * (1 - ramp(t, tc + 0.9, 0.3))
    rot_comp(f, scale_el(ckey_el("sweat" if t >= tc else "sly"), 1.05), 540, 600 + 330 * k, 90 + jig, 1.0)
    if t >= tc:
        slam(f, chip("CAN'T TURN", RED_, WHITE, 40), 540, 1440, 0, t, tc + 0.1)
        comp(f, check_el(44, False), 820, 980, scale=pin(t, tc + 0.1, 0.25))
    if t < tc: wui(f, "it slips into the", "[SAME LOCKS]", t, st_("S11") + 0.05, acc=YEL_, size=180, out=tc - 0.05)
    else: wui(f, "but it", "[CAN'T] turn them", t, tc - 0.05, acc=(255, 160, 140), size=170)
    return finish(f, n)


# ---- S12: it just sits there — a FAKE KEY, BLOCKING the way ----
def shot_S12(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S12")
    locks = [(dx, ckey_el("sly"), 0, 0.0) for i, dx in enumerate(LK) if u >= 0.1 + 0.2 * i]
    brain_cell(f, 540, 1240, 820, t, locks, 0.0, 420, seed=3)
    tf = T("b5", "fake") - 0.15; tb = T("b5", "blocking") - 0.15
    if t >= tf: label_at(f, "FAKE KEY = CAFFEINE", 540, 700, t, tf, 330, 900, bg=CAF_D)
    if t >= tb: slam(f, stamp_el("BLOCKED", RED_, 52), 540, 1460, -4, t, tb)
    wui(f, "a", "[FAKE KEY]", t, st_("S12") + 0.05, acc=(255, 200, 140), size=230)
    return finish(f, n)


# ---- S13: the sleepy keys CAN'T GET IN (they bounce off the blocked locks) ----
def shot_S13(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S13")
    locks = [(dx, ckey_el("sly"), 0, 0.0) for dx in LK]
    pts = brain_cell(f, 540, 1240, 820, t, locks, 0.0, 420, seed=3)
    for i, (px, py) in enumerate(pts):
        ph = ((u * 0.9 + i * 0.33) % 1.0)
        rot_comp(f, scale_el(skey_el("sleepy" if ph < 0.5 else "wow"), 0.55), px + (ph - 0.5) * 140, py - 330 + 200 * (1 - abs(2 * ph - 1)) - 40, 90 + 40 * (ph - 0.5), 1.0)
        if abs(ph - 0.5) < 0.1: comp(f, chip("BOING", INK, WHITE, 22), px + 70, py - 190)
    wui(f, "sleepy keys", "[CAN'T GET IN]", t, st_("S13") + 0.05, acc=ADE_L, size=150)
    return finish(f, n)


# ---- S13b: so you feel AWAKE (wide eyes, twitchy) ----
def shot_S13b(t, n):
    f = stage("yellow", (255, 250, 210), 540, 1000, 440); u = lt(t, "S13b")
    jt = 4 * math.sin(t * 40)
    chub(f, 540 + jt, 1480, 1.15, la=(150, 175), ra=(150, 175), mouth=2, expr="wow", brow="up", look=(0, 0), bob=8 * abs(math.sin(t * 7)))
    hx, hy = head_pos(540, 1480, 1.15)
    for i in range(8):
        a = i * math.pi / 4 + 0.3; cv2.line(f, (int(hx + 160 * math.cos(a)), int(hy + 160 * math.sin(a))), (int(hx + 210 * math.cos(a)), int(hy + 210 * math.sin(a))), C(INK), 8, cv2.LINE_AA)
    ui_word(f, "so you feel", "[AWAKE]", 470, t, st_("S13b") + 0.05, col=INK, acc=(230, 120, 0), size=240)
    return finish(f, n)


# ---- S14: CHART — no new energy, the tiredness is just HIDDEN (real vs felt, the gap after the coffee) ----
def shot_S14(t, n):
    f = stage("cream", (255, 240, 220), 540, 980, 420); u = lt(t, "S14")
    d_ = en_("S14") - st_("S14")
    now = 7 + (15.2 - 7) * eio(clamp((u - 0.1) / max(0.5, d_ * 0.7)))
    lab_k = clamp((u - 0.6) / 0.3)
    X, Y, heads = day_graph(f, t, now, [(real_tired, ADE, "REAL TIREDNESS", 7, (-190, -50)), (felt_tired, (230, 120, 0), "WHAT YOU FEEL", 7, (-150, 56))],
                            y0=720, y1=1270, h1=18.5, ticks=((8, "8 AM"), (12, "NOON"), (16, "4 PM")), marks=[(TCOF, scale_el(mug_el(), 0.25), "COFFEE", st_("S14") + 0.25)],
                            title="HIDDEN, NOT GONE", label_k=lab_k)
    rider(f, heads[1], 0.4, "wow" if now > TCOF + 0.5 else "sleepy", 0, t)
    th = T("b7", "hidden.") - 0.2
    if t >= th and now > 13.5:
        xg = X(13.5); ya, yb = Y(real_tired(13.5)), Y(felt_tired(13.5))
        cv2.line(f, (int(xg), int(ya + 18)), (int(xg), int(yb - 18)), C(RED_), 8, cv2.LINE_AA)
        label_at(f, "HIDDEN", xg - 210, (ya + yb) / 2, t, th, xg - 12, (ya + yb) / 2, bg=RED_)
    return finish(f, n)


# ---- S15: PART 3 — but here's the WEIRD part ----
def shot_S15(t, n):
    f = stage("pink", (255, 220, 236), 540, 1000, 420); u = lt(t, "S15")
    chub(f, 420, 1480, 1.1, la=(-150, -150), ra=(70, 40), mouth=0, expr="sus", brow="sus", look=(0.3, -0.2), hold=scale_el(mug_el(), 0.42), hold_off=(30, -20), hold_front=True)
    comp(f, ed_el("", "?", "", big_col=RED_, big_size=170), 800 + 6 * math.sin(t * 4), 920)
    chapter_card(f, t, st_("S15") + 0.02, 3, "THE CRASH", y=760, dur=1.4, col=(255, 160, 160))
    ui_word(f, "here's the", "[WEIRD] part", 470, t, st_("S15") + 0.05, col=INK, acc=RED_, size=200)
    return finish(f, n)


# ---- S16: sleepy keys keep PILING UP behind the block ----
def shot_S16(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S16")
    d_ = en_("S16") - st_("S16")
    nk = int(4 + 26 * clamp(u / max(0.5, d_ - 0.2)))
    key_pile(f, 540, 940, nk, t, 700, 0.42)
    locks = [(dx, ckey_el("sweat"), 0, 0.0) for dx in LK]
    brain_cell(f, 540, 1290, 820, t, locks, 0.0, 380, seed=3)
    tp = T("c2", "piling") - 0.15
    if t >= tp: label_at(f, "STILL PILING UP", 540, 1462, t, tp, None, None, bg=ADE_D)
    wui(f, "they keep", "[PILING UP]", t, st_("S16") + 0.05, acc=ADE_L, size=210)
    return finish(f, n)


# ---- S17: when the caffeine wears off, they RUSH IN all at once ----
def shot_S17(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S17")
    tw = T("c3", "wears") - 0.15; tr = T("c3", "rush") - 0.15
    gone = ramp(t, tw, 0.5); rush = ramp(t, tr, 0.35)
    if rush < 1: key_pile(f, 540, 940 + 300 * rush, int(30 * (1 - rush)) + 1, t, 700, 0.42)
    locks = [(dx, "skey" if rush >= 1 else None, -90 if rush >= 1 else 0, 1.0 if rush >= 1 else 0.0) for dx in LK]
    pts = brain_cell(f, 540, 1290, 820, t, locks, 0.7 * rush, 380, seed=3, sleepy=rush > 0.5)
    for i, (px, py) in enumerate(pts):
        if gone < 1: rot_comp(f, scale_el(ckey_el("wow"), 0.5), px + (i - 1) * 260 * gone, py - 20 - 500 * gone, 90 + 120 * gone, 1.0, 1 - gone)
    if t >= tw: comp(f, chip("CAFFEINE WEARS OFF", CAF_D, WHITE, 28), 540, 1462, op=clamp((t - tw) / 0.2) * (1 - clamp((t - tr - 0.4) / 0.2)))
    if t >= tr:
        comp(f, burst_el("WHOOSH!", ADE_L, INK, 56), 820, 720, scale=pin(t, tr, 0.22))
        comp(f, chip("ALL AT ONCE", ADE_D, WHITE, 34), 540, 1462, op=clamp((t - tr - 0.4) / 0.2))
    wui(f, "they", "[RUSH IN]", t, st_("S17") + 0.05, acc=ADE_L, size=240)
    return finish(f, n)


# ---- S18: CHART — that's the CRASH (felt line shoots up to meet the real one; rider falls asleep) ----
def _s18_now(u, d_): return 15.2 + (17.6 - 15.2) * eio(clamp((u - 0.05) / max(0.4, d_ * 0.6)))


def shot_S18(t, n):
    f = stage("red", (255, 200, 190), 540, 980, 400); u = lt(t, "S18")
    d_ = en_("S18") - st_("S18")
    now = _s18_now(u, d_)
    X, Y, heads = day_graph(f, t, now, [(real_tired, ADE, "REAL TIREDNESS", 7, (-190, -50)), (felt_tired, (230, 120, 0), "WHAT YOU FEEL", 7, (-150, 56))], y0=720, y1=1270, h1=18.5, ticks=((8, "8 AM"), (12, "NOON"), (16, "4 PM")),
                            marks=[(TCOF, scale_el(mug_el(), 0.25), "COFFEE", -1)], title="THE CRASH")
    crash = now > TOFF + 0.35
    rider(f, heads[1], 0.4, "sleepy" if crash else "wow", 3 if crash else 0, t)
    if crash:
        tcr = next(st_("S18") + q / 24 for q in range(200) if _s18_now(q / 24, d_) > TOFF + 0.35)
        comp(f, burst_el("CRASH!", RED_, WHITE, 60), 760, 900, scale=pin(t, tcr, 0.22))
    return finish(f, n)


# ---- S18b: a food scientist calls coffee a LOAN, not new energy (pays off the 'with interest' loop) ----
def shot_S18b(t, n):
    f = stage("latte", (255, 246, 226), 540, 1000, 420); u = lt(t, "S18b")
    rot_comp(f, loan_doc_el(), 640, 1040 + 6 * math.sin(t * 3), -4, pin(t, st_("S18b"), 0.3), 1.0, 0.35)
    scientist(f, 230, 1490, 0.8, la=(20, 10), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", look=(1, 0))
    tl = T("c4", "lends") - 0.15
    if t >= tl + 0.3: slam(f, stamp_el("NOT NEW ENERGY", RED_, 40), 650, 1250, -8, t, tl + 0.3)
    comp(f, chip("Source: Dr Emma Beckett, University of Newcastle", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    ui_word(f, "coffee only", "[LENDS] it", 470, t, st_("S18b") + 0.1, col=INK, acc=RED_, size=250)
    return finish(f, n)


# ---- S19: PART 4 — so how LONG does the loan last? (clock spins) ----
def shot_S19(t, n):
    f = stage("sky", (236, 248, 255), 540, 1000, 440); u = lt(t, "S19")
    mm = int(u * 240) % 720
    comp(f, scale_el(clock_el(9 + mm // 60, (mm % 60) // 5 * 5), 1.2), 690, 1030, scale=pin(t, st_("S19"), 0.3))
    chub(f, 280, 1490, 0.85, la=(-150, -150), ra=(70, 40), mouth=0, expr="sus", brow="sus", look=(1, -0.3), hold=scale_el(mug_el(), 0.36), hold_off=(30, -20), hold_front=True)
    chapter_card(f, t, st_("S19") + 0.02, 4, "HOW LONG?", y=1420, dur=1.4, col=(150, 230, 255))
    ui_word(f, "how", "[LONG]?", 470, t, st_("S19") + 0.05, col=INK, acc=(30, 110, 220), size=250)
    return finish(f, n)


# ---- S20: 3 to 5 hours to clear just HALF of it (caffeine tank drains to half while the clock runs) ----
def shot_S20(t, n):
    f = stage("teal", (180, 250, 240), 540, 1000, 420); u = lt(t, "S20")
    th = T("d2", "half") - 0.3
    lv = 1.0 - 0.5 * ramp(t, st_("S20") + 0.4, max(0.5, th - st_("S20") - 0.2))
    x0, x1, y0, y1 = 220, 560, 720, 1340
    cv2.rectangle(f, (x0 - 12, y0 - 12), (x1 + 12, y1 + 12), C(INK), -1, cv2.LINE_AA)
    cv2.rectangle(f, (x0, y0), (x1, y1), C((240, 246, 250)), -1, cv2.LINE_AA)
    yl = int(y1 - (y1 - y0) * lv)
    cv2.rectangle(f, (x0, yl), (x1, y1), C(CAF), -1, cv2.LINE_AA)
    cv2.ellipse(f, (int((x0 + x1) / 2), yl), (int((x1 - x0) / 2), 14), 0, 0, 360, C(CAF_L), -1, cv2.LINE_AA)
    for j in range(5): caf_dot(f, x0 + 60 + 55 * j, yl + 60 + 30 * (j % 2) + 6 * math.sin(t * 3 + j), 14)
    ym = int((y0 + y1) / 2)
    for xx in range(x0 - 30, x1 + 30, 30): cv2.line(f, (xx, ym), (xx + 16, ym), C(RED_), 6, cv2.LINE_AA)
    comp(f, chip("HALF", RED_, WHITE, 26), x1 + 90, ym)
    comp(f, chip("CAFFEINE IN YOU", INK, WHITE, 26), (x0 + x1) / 2, y0 - 50)
    comp(f, scale_el(clock_el(int(2 + 4 * (1 - lv) * 2) % 12, 0), 0.7), 800, 900)
    if t >= th: comp(f, readout_el("3-5 HOURS", YEL_, INK, 50), 800, 1130, scale=pin(t, th, 0.3))
    comp(f, chip("Source: Northwestern Univ. via CSPI; Univ. of Newcastle", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.5) / 0.3))
    wui(f, "just to clear", "[HALF]", t, st_("S20") + 0.05, acc=YEL_, size=240)
    return finish(f, n)


# ---- S21: CHART — a 2 PM coffee: about a QUARTER is still there at bedtime ----
def shot_S21(t, n):
    f = stage("dusk", (255, 200, 210), 540, 980, 400); u = lt(t, "S21")
    d_ = en_("S21") - st_("S21")
    now = 14 + (23.3 - 14) * eio(clamp((u - 0.3) / max(0.5, d_ * 0.75)))
    X, Y, heads = day_graph(f, t, now, [(caf_left, CAF, "CAFFEINE LEFT", 14)], y0=720, y1=1270, h0=8,
                            marks=[(14, scale_el(mug_el(), 0.25), "2 PM", st_("S21") + 0.1), (23, None, "BEDTIME", st_("S21") + 0.4)],
                            title="A 2 PM COFFEE AT BEDTIME", ticks=((8, "8 AM"), (14, "2 PM"), (20, "8 PM"), (24, "12")))
    moon_icon(f, X(23), 640, 26, (60, 24, 90))
    tq = T("d3", "quarter") - 0.2
    if t >= tq and heads[0] is not None:
        comp(f, chip("1/4 STILL THERE", RED_, WHITE, 30), X(19.5), Y(0.62), scale=pin(t, tq, 0.3))
        draw_arrow(f, X(20.6), Y(0.56), heads[0][0] - 14, heads[0][1] - 22, eo(clamp((t - tq) / 0.3)), RED_, 8, 26)
    comp(f, chip("half-life about 3-5 h (drawn with 4.5 h)", INK, WHITE, 20), 540, 1462, op=clamp((u - 0.6) / 0.3))
    return finish(f, n)


# ---- S22: in one sleep study, people took caffeine SIX hours before bed ----
def shot_S22(t, n):
    f = stage("night", (230, 220, 255), 820, 700, 110); u = lt(t, "S22")
    sx = 810; cv2.rectangle(f, (sx - 130, 900), (sx + 130, 1080), C(INK), -1, cv2.LINE_AA); cv2.rectangle(f, (sx - 118, 912), (sx + 118, 1068), C((20, 40, 30)), -1, cv2.LINE_AA)
    P = [(sx - 110 + 6 * j, 990 + 30 * math.sin(j * 0.7 + t * 6) * (1 if j % 9 < 5 else 0.3)) for j in range(38)]
    cv2.polylines(f, [np.array(P, np.int32)], False, C((90, 255, 140)), 4, cv2.LINE_AA)
    comp(f, chip("SLEEP MONITOR", INK, WHITE, 22), sx, 1120)
    chub(f, 380, 1380, 0.95, la=(20, 10), ra=(20, 10), mouth=0, expr="sleepy", brow="sad", look=(0, 0.3), sit=True)
    hx, hy = head_pos(380, 1380, 0.95)
    cv2.ellipse(f, (int(hx), int(hy - 70)), (100, 26), 0, 180, 360, C(INK), 12, cv2.LINE_AA)
    cv2.line(f, (int(hx + 90), int(hy - 70)), (sx - 130, 990), C(INK), 5, cv2.LINE_AA)
    comp(f, bed_el(560), 400, 1370)
    ts = T("d4", "six") - 0.15
    if t >= ts:
        rot_comp(f, scale_el(capsule_el(), 1.0), 760, 760, 20, pin(t, ts, 0.3), 1.0, 0.2)
        comp(f, chip("CAFFEINE 6 HOURS BEFORE BED", YEL_, INK, 28), 640, 660, op=clamp((t - ts) / 0.2))
    comp(f, chip("Source: Drake et al., J Clin Sleep Med, 2013", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    wui(f, "", "[6 HOURS] before bed", t, st_("S22") + 0.05, acc=YEL_, size=150)
    return finish(f, n)


# ---- S23: they slept OVER AN HOUR LESS (sleep bars) ----
def shot_S23(t, n):
    f = stage("purple", (210, 190, 255), 540, 1000, 420); u = lt(t, "S23")
    th = T("d5", "hour") - 0.3
    k = ramp(t, st_("S23") + 0.1, 0.5); cut = ramp(t, th, 0.4)
    base = 1330
    bars2(f, base, [(330, 500, (120, 170, 255), "NO CAFFEINE"), (750, 500 - 75 * cut, (255, 150, 60), "CAFFEINE")], k, t)
    if t >= th:
        cv2.rectangle(f, (655, int(base - 500)), (845, int(base - 500 + 75 * cut)), C(RED_), 6, cv2.LINE_AA)
        slam(f, tag_el("-1 HOUR+", RED_, WHITE, 52), 750, 700, -6, t, th + 0.2)
    comp(f, chip("measured sleep time", INK, WHITE, 24), 540, 1462, op=clamp((u - 0.3) / 0.3))
    wui(f, "they lost over an", "[HOUR] of sleep", t, st_("S23") + 0.05, acc=(255, 200, 120), size=200)
    return finish(f, n)


# ---- S23b: and they didn't even NOTICE (tired Chubby: 'I slept fine!') ----
def shot_S23b(t, n):
    f = stage("pink", (255, 220, 236), 540, 1000, 420); u = lt(t, "S23b")
    chub(f, 400, 1480, 1.1, la=(20, 10), ra=(150, 175), mouth=2, expr="sleepy", brow="up", look=(0.5, -0.2), bob=4 * math.sin(t * 3))
    comp(f, bubble_el("I SLEPT FINE!", 44), 720, 800, scale=pin(t, st_("S23b") + 0.15, 0.3))
    if u > 0.6: label_at(f, "EYE BAGS", 840, 1200, t, st_("S23b") + 0.6, 480, 1070, bg=ADE_D)
    ui_word(f, "they didn't even", "[NOTICE]", 470, t, st_("S23b") + 0.05, col=INK, acc=RED_, size=220)
    return finish(f, n)


# ---- S24: takeaway — try your last cup EARLIER in the day (mug slides from night to morning on a day strip) ----
def shot_S24(t, n):
    f = stage("latte", (255, 240, 210), 540, 1000, 420); u = lt(t, "S24")
    x0, x1, yb = 130, 950, 1000
    for i in range(60):
        k = i / 59; col = tuple(int(a + (b - a) * k) for a, b in zip((255, 214, 90), (60, 40, 120)))
        cv2.rectangle(f, (int(x0 + (x1 - x0) * i / 60), yb - 40), (int(x0 + (x1 - x0) * (i + 1) / 60) + 1, yb + 40), C(col), -1)
    cv2.rectangle(f, (x0, yb - 40), (x1, yb + 40), C(INK), 6, cv2.LINE_AA)
    sun_icon(f, x0 + 40, yb - 110, 34, t); moon_icon(f, x1 - 40, yb - 110, 34, (255, 240, 210))
    comp(f, chip("MORNING", INK, WHITE, 22), x0 + 60, yb + 80); comp(f, chip("NIGHT", INK, WHITE, 22), x1 - 60, yb + 80)
    te = T("d6", "earlier") - 0.3
    k = ramp(t, te, 0.6)
    mx = x1 - 160 - (x1 - x0 - 380) * k
    comp(f, scale_el(mug_el(), 0.5), mx, yb - 10 - 60 * math.sin(math.pi * k))
    if k >= 1: comp(f, check_el(42, True), mx + 110, yb - 120, scale=pin(t, te + 0.6, 0.25)); sparkles(f, mx, yb, t, te + 0.6, 10, 180)
    chub(f, 540, 1490, 0.75, la=(20, 10), ra=(70, 40) if k < 1 else (150, 175), mouth=0 if k < 1 else 2, expr="n" if k < 1 else "happy", brow="up", look=(-1 if k > 0.3 else 1, -0.5))
    comp(f, chip("if sleep is hard", INK, WHITE, 26), 540, 760, op=clamp((u - 0.2) / 0.3))
    ui_word(f, "your last cup", "[EARLIER]", 470, t, st_("S24") + 0.05, col=INK, acc=(34, 140, 80), size=220)
    return finish(f, n)


# ---- S25: PART 5 — and if you drink it EVERY day? (calendar flips, mugs stack) ----
def shot_S25(t, n):
    f = stage("orange", (255, 220, 180), 540, 1000, 420); u = lt(t, "S25")
    day = 1 + int(u * 9) % 30
    comp(f, scale_el(calendar_el("DAY", str(day)), 0.9), 700, 1040, scale=pin(t, st_("S25"), 0.3))
    for j in range(min(5, 1 + int(u * 3))): comp(f, scale_el(mug_el(), 0.3), 260, 1390 - 80 * j)
    chapter_card(f, t, st_("S25") + 0.02, 5, "EVERY DAY", y=760, dur=1.3, col=(255, 200, 140))
    wui(f, "", "[EVERY] day?", t, st_("S25") + 0.05, acc=YEL_, size=230)
    return finish(f, n)


# ---- S26: your brain may build EXTRA LOCKS (more locks pop up on the cell) ----
LK5 = (-300, -150, 0, 150, 300)


def shot_S26(t, n):
    f = stage("neuro", (110, 200, 230), 540, 1000, 420); u = lt(t, "S26")
    te = T("e2", "extra") - 0.2
    base = [(dx, None, 0, 0.0) for dx in (-150, 0, 150)]
    extra = [(dx, None, 0, 0.75) for j, dx in enumerate((-300, 300)) if t >= te + 0.2 * j]
    brain_cell(f, 540, 1240, 820, t, base + extra, 0.0, 420, seed=3)
    if t >= te:
        comp(f, chip("+ EXTRA LOCKS", (40, 150, 70), WHITE, 34), 540, 720, scale=pin(t, te, 0.3))
        sparkles(f, 240, 1010, t, te, 10, 160); sparkles(f, 840, 1010, t, te + 0.2, 10, 160)
        comp(f, chip("seen in animal studies", INK, WHITE, 24), 540, 1462, op=clamp((t - te - 0.4) / 0.3))
    wui(f, "your brain may build", "[EXTRA LOCKS]", t, st_("S26") + 0.05, acc=(140, 255, 200), size=160)
    return finish(f, n)


# ---- S26b: so you need MORE caffeine to feel the same (mugs multiply) ----
def shot_S26b(t, n):
    f = stage("cafe", (255, 214, 150), 540, 980, 420); u = lt(t, "S26b")
    tm = T("e2b", "more") - 0.15
    nm = 1 + (2 if t >= tm else 0)
    cols = ((240, 80, 70), (60, 140, 240), (255, 190, 30))
    for j in range(nm): comp(f, scale_el(mug_el(cols[j]), 0.7), 600 + (j - (nm - 1) / 2) * 230, 1150, scale=pin(t, tm + 0.15 * j if j else st_("S26b"), 0.3))
    if t >= tm: comp(f, burst_el("MORE!", RED_, WHITE, 52), 820, 820, scale=pin(t, tm, 0.22))
    chub(f, 180, 1490, 0.7, la=(20, 10), ra=(20, 10), mouth=0, expr="sleepy", brow="sad", look=(1, -0.3))
    ui_word(f, "you need", "[MORE]", 470, t, st_("S26b") + 0.05, col=WHITE, acc=YEL_, size=250, shadow=0.6, lead_col=WHITE)
    return finish(f, n)


# ---- S27: BONUS — you're not the only one HOOKED (a bee buzzes around Chubby's mug) ----
def shot_S27(t, n):
    f = stage("honey", (255, 246, 200), 540, 1000, 440); u = lt(t, "S27")
    chub(f, 380, 1480, 1.0, la=(20, 10), ra=(70, 40), mouth=0, expr="wow", brow="up", look=(1, -0.5), hold=scale_el(mug_el(), 0.42), hold_off=(30, -20), hold_front=True)
    a = t * 3.0; bx, by = 730 + 150 * math.cos(a), 880 + 90 * math.sin(2 * a)
    comp(f, scale_el(bee_el(int(t * 18) % 2, "wow"), 0.8), bx, by)
    comp(f, chip("BONUS", INK, YEL_, 34), 540, 1440, op=clamp((u - 0.05) / 0.2))
    ui_word(f, "not the only one", "[HOOKED]", 470, t, st_("S27") + 0.05, col=INK, acc=(200, 120, 0), size=220)
    return finish(f, n)


# ---- S28: coffee and lemon flowers put a little caffeine in their NECTAR (magnified drop) ----
def shot_S28(t, n):
    f = stage("emerald", (210, 250, 220), 540, 1000, 420); u = lt(t, "S28")
    tc = T("e4", "caffeine") - 0.15
    gl = ramp(t, tc, 0.4)
    rot_comp(f, scale_el(flower_el("coffee", gl), 1.0), 300, 1100 + 6 * math.sin(t * 2), 5 * math.sin(t), pin(t, st_("S28"), 0.3))
    rot_comp(f, scale_el(flower_el("lemon", gl), 1.0), 780, 1100 + 6 * math.sin(t * 2 + 1), 5 * math.sin(t + 1), pin(t, st_("S28") + 0.15, 0.3))
    comp(f, lemon_el(), 900, 1320)
    comp(f, chip("COFFEE FLOWER", INK, WHITE, 26), 300, 1300); comp(f, chip("LEMON FLOWER", INK, WHITE, 26), 690, 1380)
    if t >= tc:
        def close(g):
            g[:] = np.array(C((255, 236, 170)), np.float32)
            cv2.circle(g, (540, 760), 100, C(INK), -1, cv2.LINE_AA); cv2.circle(g, (540, 760), 92, C((255, 200, 80)), -1, cv2.LINE_AA)
            for j in range(4): caf_dot(g, 495 + 30 * j, 750 + 20 * math.sin(t * 3 + j), 13)
        inset(f, 540, 760, 140, close, pin(t, tc, 0.3))
        comp(f, chip("NECTAR + A LITTLE CAFFEINE", CAF_D, WHITE, 26), 540, 935, op=clamp((t - tc - 0.3) / 0.2))
    wui(f, "caffeine in their", "[NECTAR]", t, st_("S28") + 0.05, acc=(255, 220, 120), size=210)
    return finish(f, n)


# ---- S29: bees that sip it are 3x more likely to REMEMBER that flower (bars + count-up) ----
def shot_S29(t, n):
    f = stage("honey", (255, 246, 200), 540, 1000, 420); u = lt(t, "S29")
    t3 = T("e5", "three") - 0.3
    k = ramp(t, st_("S29") + 0.1, 0.4); k3 = ramp(t, t3, 0.6)
    base = 1330
    bars2(f, base, [(330, 150 * k, (200, 200, 210), "PLAIN NECTAR"), (750, 150 * k + 300 * k3, CAF_L, "WITH CAFFEINE")], 1.0, t)
    comp(f, scale_el(bee_el(int(t * 18) % 2), 0.45), 330, base - 150 * k - 150)
    comp(f, scale_el(bee_el(int(t * 18 + 1) % 2, "happy"), 0.45), 750, base - (150 * k + 300 * k3) - 150)
    v = count_up(t, t3, 3, 0.5) if t >= t3 else 1
    comp(f, readout_el(f"{max(1, v)}x", YEL_, INK, 70), 540, 760)
    comp(f, chip("Source: Wright et al., Science, 2013 (Newcastle University)", INK, WHITE, 22), 540, 1462, op=clamp((u - 0.4) / 0.3))
    ui_word(f, "more likely to", "[REMEMBER]", 470, t, st_("S29") + 0.05, col=INK, acc=(200, 110, 0), size=200)
    return finish(f, n)


# ---- S30: so the bees keep COMING BACK (loops around the flower) ----
def shot_S30(t, n):
    f = stage("emerald", (210, 250, 220), 540, 1000, 420); u = lt(t, "S30")
    comp(f, scale_el(flower_el("coffee", 1.0), 1.1), 540, 1080)
    for i in range(3):
        a = t * 2.2 + i * 2.1; bx, by = 540 + 330 * math.cos(a), 1050 + 200 * math.sin(a)
        comp(f, scale_el(bee_el(int(t * 18 + i) % 2, "happy"), 0.5), bx, by)
    comp(f, chip("AGAIN AND AGAIN", INK, YEL_, 30), 540, 1440, op=clamp((u - 0.4) / 0.3))
    wui(f, "the bees keep", "[COMING BACK]", t, st_("S30") + 0.05, acc=YEL_, size=170)
    return finish(f, n)


# ---- S30b: sound FAMILIAR? (Chubby with his mug, caught, grins at camera) ----
def shot_S30b(t, n):
    f = stage("cafe", (255, 214, 150), 540, 980, 430); u = lt(t, "S30b")
    chub(f, 540, 1480, 1.15, la=(20, 10), ra=(70, 40), mouth=0, expr="smirk", brow="sus", look=(0, 0), hold=scale_el(mug_el(), 0.45), hold_off=(30, -20), hold_front=True,
         bob=3 * math.sin(t * 3))
    steam(f, 740, 1060, t, 0.9)
    comp(f, scale_el(bee_el(int(t * 18) % 2, "happy"), 0.4), 830 + 30 * math.sin(t * 4), 760 + 20 * math.cos(t * 5))
    wui(f, "sound", "[FAMILIAR]?", t, st_("S30b") + 0.05, acc=(255, 214, 150), size=220)
    return finish(f, n)


# ---- S31: RECAP — no new energy -> caffeine blocks the lock -> the tiredness waits ----
def shot_S31(t, n):
    f = stage("night", (210, 190, 255), 540, 1000, 420); u = lt(t, "S31")
    items = [(scale_el(battery_el(0.0, "0%"), 0.42), "NO NEW ENERGY"), (scale_el(ckey_el("sly"), 0.55), "BLOCKS THE LOCK"), (scale_el(skey_el("sleepy"), 0.55), "TIREDNESS WAITS")]
    ts = [T("f1", "add") - 0.15, T("f1", "blocks") - 0.15, T("f1", "waits") - 0.15]
    recap_steps(f, items, 1000, t, ts, 310, 1.3)
    if t >= ts[2] + 0.3: key_pile(f, 870, 1380, 6, t, 260, 0.3)
    wui(f, "", "[REMEMBER]", t, st_("S31") + 0.05, acc=YEL_, size=200)
    return finish(f, n)


# ---- S32: send it + FreshNestHub sting ----
def shot_S32(t, n):
    f = stage("cafe", (255, 214, 150), 540, 880, 420); u = lt(t, "S32")
    vend = LINES["f2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("f2", "Send") + 0.3
        comp(f, scale_el(phone2_el("why can't I sleep??", "your 6pm coffee. it's a LOAN", pr), 0.82), 650, 950, scale=pin(t, st_("S32")))
        if pr and t < T("f2", "Send") + 0.75:
            rr = (t - T("f2", "Send") - 0.3) / 0.45
            cv2.circle(f, (650, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, 250, 1480, 0.8, la=(20, 10), ra=(70, 40), mouth=2, expr="sleepy", brow="up", look=(1, 0), hold=scale_el(mug_el(), 0.32), hold_off=(30, -20), hold_front=True)
        ui_word(f, "send to the friend who drinks", "[COFFEE AT NIGHT]", 420, t, T("f2", "friend") - 0.1, col=WHITE, acc=YEL_, size=120, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=WHITE, lead_size=42), 540, 1080, op=clamp((t - vend - 0.5) / 0.3))
        sip_pose(f, 400, 1480, 0.7, t, expr="happy")
        comp(f, scale_el(bee_el(int(t * 18) % 2, "happy"), 0.35), 720 + 40 * math.sin(t * 3), 1300 + 20 * math.cos(t * 4))
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(TD, 0.45, 20), (TD + 0.25, 0.25, 10), (T("i2", "bit.") - 0.15, 0.35, 16), (T("i2", "hides") - 0.1, 0.25, 10),
           (T("i3", "back") - 0.15, 0.3, 14), (T("i3", "interest.") - 0.2, 0.3, 12),
           (T("a1", "All") + 0.65, 0.25, 10), (T("a5", "clicks") - 0.12, 0.35, 16), (T("a5", "slows") - 0.15, 0.2, 8),
           (T("b1", "coffee.") - 0.2, 0.25, 10), (T("b3", "like") - 0.15, 0.35, 16), (T("b4", "can't") - 0.15, 0.4, 16),
           (T("b5", "blocking") - 0.15, 0.4, 18), (T("c3", "rush") - 0.15, 0.6, 28), (T("c4", "lends") + 0.15, 0.35, 16),
           (T("d2", "half") - 0.3, 0.25, 10), (T("d3", "quarter") - 0.2, 0.3, 12), (T("d5", "hour") - 0.1, 0.35, 16),
           (T("d6", "earlier") + 0.3, 0.25, 10), (T("e2", "extra") - 0.2, 0.3, 12), (T("e2b", "more") - 0.15, 0.3, 14),
           (T("e5", "three") - 0.3, 0.35, 16), (T("c4", "crash.") - 0.1, 0.5, 24)]


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
