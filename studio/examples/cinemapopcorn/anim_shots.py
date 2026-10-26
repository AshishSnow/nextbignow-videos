# ================= shots: "Why movie theaters really make money on popcorn" (AMC FY2025) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "Sounds") - 0.12, "punch"), ("S1", T("a1", "Step") - 0.2, "whip"),
    ("S1b", T("a2", "But") - 0.12, "focus"), ("S2", T("b1", "Step") - 0.2, "flash"), ("S2b", T("b2", "And") - 0.12, "zoom"),
    ("S3", T("c1", "Step") - 0.2, "whip"), ("S3b", T("c2", "But") - 0.12, "focus"), ("S4", T("d1", "So") - 0.2, "punch"),
    ("S5", T("f1", "And") - 0.2, "flash"), ("S5b", T("f2", "Rent,") - 0.12, "zoom"), ("S6", T("e1", "So") - 0.2, "whip"),
    ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_PR = "Source: AMC Q4 & full-year 2025 results (SEC 8-K, Feb 2026)"


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def coin_rain(f, t, t0, n=10, x0=540, spread=360, y1=1500, seed=0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = x0 + rng.uniform(-spread, spread); r0 = rng.uniform(-30, 30)
        q = t - t0 - 0.08 * i
        if q <= 0: continue
        y = 560 + 1000 * ((q * 0.9) % 1.0)
        if y < y1: rot_comp(f, scale_el(cash_el(), 0.5), x, y, r0 + 60 * q, 1.0, 1.0, 0.2)


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def bar(f, x, base, w, hgt, col, k=1.0):
    hh = max(2, int(hgt * clamp(k)))
    y0 = int(base - hh + 12); xs0, xs1 = int(x - w / 2 + 12), int(x + w / 2 + 12)
    f[y0:int(base), xs0:xs1] *= 0.7
    f[int(base - hh):int(base), int(x - w / 2):int(x + w / 2)] = np.array(C(col), np.float32)
    cv2.rectangle(f, (int(x - w / 2), int(base - hh)), (int(x + w / 2), int(base)), C(INK), 6, cv2.LINE_AA)
    return base - hh




def kernels(f, t, t0, n=12, x0=540, y0=1100, seed=0, spread=1.0):
    """popcorn kernels bursting up and falling with gravity"""
    if t < t0: return
    rng = np.random.default_rng(seed)
    for i in range(n):
        vx = rng.uniform(-420, 420) * spread; vy = rng.uniform(-1100, -700); q = (t - t0) - 0.04 * i
        if q <= 0: continue
        q = q % 1.6
        x = x0 + vx * q; y = y0 + vy * q + 900 * q * q
        if 260 < y < 1480 and 80 < x < 960: rot_comp(f, kernel_el(30, i % 5), x, y, 200 * q * (1 if i % 2 else -1), 1.0, 1.0, 0.2)


# ---- S0: hook — cinema, popcorn bucket vs ticket ----
def shot_S0(t, n):
    f = stage("red", (255, 200, 60), 540, 980, 440)
    tp = T("i1", "popcorn…") - 0.15; tt = T("i1", "ticket") - 0.15
    comp(f, scale_el(cinema_el(), 0.78), 540, 960, scale=pin(t, 0.0, 0.3))
    kernels(f, t, 0.15, 10, 390, 1150, 1)
    rot_comp(f, scale_el(popcorn_el(), 0.78), 380 + 6 * math.sin(t * 4), 1210, -6, pin(t, 0.05, 0.3) * (1 + 0.06 * math.exp(-max(0, t - tp) * 6) * (t >= tp)), 1.0, 0.35)
    if t >= tt:
        rot_comp(f, scale_el(ticket_el("ADMIT ONE", "MOVIE", YEL_), 0.72), 730, 1310 + 6 * math.sin(t * 5), 10, pin(t, tt, 0.25), 1.0, 0.35)
    ui_word(f, "AMC makes almost as much from", "POPCORN", 470, t, 0.12, col=YEL_, size=190, shadow=0.45, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "as from every movie", "TICKET", 470, t, tt, col=WHITE, size=210, shadow=0.45, lead_col=WHITE)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1000), n)


# ---- S0b: sounds crazy — grab a snack, here's the math ----
def shot_S0b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S0b")
    tc = T("i2", "crazy.") - 0.2; tm = T("i2", "math!") - 0.25
    rays(f, 540, 1080, 700, (255, 255, 255), 0.35, t)
    guy(f, 540, 1500, 1.0, la=(130, 150), ra=(60, 30), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(1, -1),
        expr="wow" if talk(t) == 0 else "n", hold=scale_el(popcorn_el(), 0.34), hold_off=(10, -40))
    if t >= tc and t < tm: comp(f, bubble_el("CRAZY?!", 56), 780, 860, scale=pin(t, tc, 0.3))
    if t >= tm:
        for i, s_ in enumerate(("+", "=", "%", "$")):
            comp(f, chip(s_, INK, WHITE, 64), [260, 820, 250, 830][i], [820, 820, 1100, 1100][i] + 8 * math.sin(t * 6 + i), scale=pin(t, tm + 0.06 * i, 0.25))
    ui_word(f, "sounds", "CRAZY", 470, t, SHOT["S0b"]["start"] + 0.05, col=INK, size=210, out=tm - 0.05)
    ui_word(f, "grab a snack, here's the", "MATH", 470, t, tm, col=RED_, size=240)
    return finish(f, n)


# ---- S1: step 1 — the ticket, about $12 ----
def shot_S1(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S1")
    tw = T("a1", "twelve") - 0.2
    big = "$12.09" if t >= tw else "?"
    rot_comp(f, scale_el(ticket_el("AVG TICKET", big, YEL_, 620, 300), 1.0), 540, 1040 + 8 * math.sin(t * 3), -4 + 2 * math.sin(t * 2), pin(t, SHOT["S1"]["start"] + 0.05, 0.3) * (1 + 0.08 * math.exp(-max(0, t - tw) * 7) * (t >= tw)), 1.0, 0.4)
    guy(f, 220, 1500, 0.7, la=(18, 8), ra=(110, 60), mouth=talk(t), blink=blink_at(t, 2), brow="up", look=(1, -1), expr="n")
    if t >= tw: comp(f, chip(SRC_PR, INK, WHITE, 22), 560, 1300, op=clamp((t - tw - 0.3) / 0.3))
    ui_word(f, "step 1", "THE TICKET", 470, t, SHOT["S1"]["start"] + 0.08, col=INK, size=180, out=tw - 0.05)
    ui_word(f, "average AMC ticket, 2025", "~$12", 470, t, tw, col=RED_, size=230)
    return finish(cam(f, 1.03 - 0.03 * eo(clamp(u / 1.5)), W / 2, 1050), n)


# ---- S1b: nearly half goes to the studio -> theater keeps 52c ----
def shot_S1b(t, n):
    f = stage("purple", (0, 200, 255), 540, 1040, 400); u = lt(t, "S1b")
    th = T("a2", "half") - 0.2; ts = T("a2", "studio!") - 0.25; tk = T("a3", "keeps") - 0.2
    k = eo(clamp((t - th) / 0.6)) if t >= th else 0.0
    ex = 60 * eo(clamp((t - ts) / 0.4)) if t >= ts else 0.0
    pie(f, 540, 1040, 260, 0.481, RED_, YEL_, k, ex, start=-90 - 0.481 * 360 + 180 - 90)
    rot_comp(f, scale_el(reel_el(), 0.55), 200, 1420, -t * 90, pin(t, ts, 0.3) if t >= ts else 0.0, 1.0, 0.3)
    if k > 0.6: comp(f, chip("48¢ TO THE STUDIO", RED_, WHITE, 32), 330, 760, scale=pin(t, th + 0.4, 0.25))
    if t >= tk:
        comp(f, chip("52¢ KEPT", GRN_, WHITE, 40), 700, 1040, scale=pin(t, tk, 0.25))
        comp(f, chip("Film costs = 48% of admissions revenue, AMC 2025", INK, WHITE, 22), 540, 1450, op=clamp((t - tk - 0.3) / 0.3))
    ui_word(f, "nearly half goes to the", "STUDIO", 470, t, SHOT["S1b"]["start"] + 0.1, col=WHITE, size=200, shadow=0.4, lead_col=WHITE, out=tk - 0.05)
    ui_word(f, "the theater keeps about", "52¢", 470, t, tk, col=YEL_, size=230, shadow=0.45, lead_col=WHITE, tail="of every ticket dollar")
    return finish(f, n)


# ---- S2: step 2 — the snack bar, $7.62 per guest ----
def shot_S2(t, n):
    f = stage("orange", YEL_, 540, 1000, 430); u = lt(t, "S2")
    ts = T("b1", "sixty") - 0.25
    # counter
    cv2.rectangle(f, (90, 1240), (990, 1420), C((120, 60, 30)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (90, 1240), (990, 1420), C(INK), 6, cv2.LINE_AA)
    cv2.rectangle(f, (80, 1220), (1000, 1250), C((250, 240, 220)), -1, cv2.LINE_AA)
    comp(f, scale_el(popcorn_el(), 0.72), 380, 1010, scale=pin(t, SHOT["S2"]["start"] + 0.05, 0.3))
    comp(f, scale_el(cup_el(), 0.62), 720, 1035, scale=pin(t, SHOT["S2"]["start"] + 0.2, 0.3))
    kernels(f, t, SHOT["S2"]["start"] + 0.3, 6, 380, 880, 4, 0.6)
    if t >= ts:
        rot_comp(f, tag_el("$7.62 PER GUEST", RED_, WHITE, 70), 540, 1330, -4, pin(t, ts, 0.25), 1.0, 0.35)
        comp(f, chip(SRC_PR, INK, WHITE, 22), 540, 1470, op=clamp((t - ts - 0.3) / 0.3))
    ui_word(f, "step 2", "SNACK BAR", 470, t, SHOT["S2"]["start"] + 0.08, col=WHITE, size=190, shadow=0.4, lead_col=WHITE, out=ts - 0.05)
    ui_word(f, "food & drinks per guest, 2025", "$7.62", 470, t, ts, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: x-ray the bucket — under 20c food cost, 80c stays ----
def shot_S2b(t, n):
    f = stage("emerald", (0, 220, 200), 540, 1000, 430); u = lt(t, "S2b")
    tx = T("b2", "itself?") - 0.25; tt = T("b2", "twenty") - 0.2; te = T("b3", "eighty") - 0.2
    sp = eo(clamp((t - tx) / 0.4)) if t >= tx else 0.0
    if t >= te: rays(f, 540, 1080, 650, (255, 255, 200), 0.5 * clamp((t - te) / 0.3), t)
    comp(f, scale_el(popcorn_el(split=round(sp * 10) / 10 if sp > 0 else 0.0), 1.0), 520, 1070, scale=pin(t, SHOT["S2b"]["start"] + 0.03, 0.3))
    if t >= tt: comp(f, chip("FOOD COST <20¢", RED_, WHITE, 32), 790, 1300, scale=pin(t, tt, 0.25))
    if t >= te: comp(f, chip("KEPT ~80¢", GRN_, WHITE, 40), 800, 960, scale=pin(t, te, 0.25))
    if t >= tt: comp(f, chip("F&B costs = 19.6% of F&B revenue, AMC 2025", INK, WHITE, 22), 540, 1460, op=clamp((t - tt - 0.3) / 0.3))
    ui_word(f, "the food itself costs", "<20¢", 470, t, SHOT["S2b"]["start"] + 0.1, col=WHITE, size=230, shadow=0.45, lead_col=WHITE, tail="per snack dollar", out=te - 0.05)
    ui_word(f, "of every snack dollar stays", "80¢", 470, t, te, col=YEL_, size=250, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3: step 3 — sales bars, snacks = 1/3 ----
def shot_S3(t, n):
    f = stage("cream", (255, 120, 200), 540, 1000, 430); u = lt(t, "S3")
    tt = T("c1", "third") - 0.2
    base = 1330; sc_ = 0.24
    cv2.line(f, (150, base), (930, base), C(INK), 8, cv2.LINE_AA)
    data = [("TICKETS", 2653, (120, 130, 150), "$2.65B"), ("SNACKS", 1671, RED_, "$1.67B"), ("OTHER", 525, (170, 170, 190), "$0.52B")]
    for i, (lb, v, col, s_) in enumerate(data):
        x = 290 + i * 250; k = eo(clamp((u - 0.2 - 0.15 * i) / 0.5))
        if i == 1 and t >= tt: rays(f, x, base - v * sc_, 300, (255, 230, 140), 0.6 * clamp((t - tt) / 0.3), t)
        top = bar(f, x, base, 190, v * sc_, col, k)
        if k > 0.5: comp(f, chip(s_, INK, WHITE, 30), x, top - 40)
        comp(f, chip(lb, INK, WHITE, 26), x, base + 40)
    comp(f, chip("AMC revenue, 2025 — " + SRC_PR[8:], INK, WHITE, 20), 540, 1460, op=clamp((u - 0.8) / 0.3))
    ui_word(f, "step 3", "ADD IT UP", 470, t, SHOT["S3"]["start"] + 0.08, col=INK, size=190, out=tt - 0.05)
    ui_word(f, "snacks are only about", "1/3", 470, t, tt, col=RED_, size=240, tail="of AMC's sales")
    return finish(f, n)


# ---- S3b: balance scale — after costs, snacks $1.34B vs tickets $1.38B ----
def shot_S3b(t, n):
    f = stage("teal", (255, 214, 120), 540, 980, 420); u = lt(t, "S3b")
    tsn = T("c2", "billion") - 0.4; ttk = T("c3", "Tickets?") - 0.1; tb = T("c3", "billion") - 0.3; tie = T("c3", "tie!") - 0.3
    # starts tipped hard toward tickets (right), snacks' value swings it, ending almost level
    ang = 14.0
    if t >= tsn: ang = 14.0 - 12.5 * eo(clamp((t - tsn) / 0.7))
    if t >= tie: ang = 1.5 + 2.5 * math.sin((t - tie) * 9) * math.exp(-(t - tie) * 3)
    ends = balance(f, 540, 860, ang, scale_el(popcorn_el(), 0.36), scale_el(ticket_el("ADMIT ONE", "MOVIE", YEL_), 0.42), arm=300)
    if t >= tsn: comp(f, chip("SNACKS $1.34B", RED_, WHITE, 34), ends[0][0], ends[0][1] + 300, scale=pin(t, tsn, 0.25))
    if t >= tb: comp(f, chip("TICKETS $1.38B", INK, WHITE, 34), ends[1][0], ends[1][1] + 300, scale=pin(t, tb, 0.25))
    comp(f, chip("Revenue minus film / food costs, AMC 2025", INK, WHITE, 22), 540, 1460, op=clamp((u - 0.6) / 0.3))
    ui_word(f, "after films & food, snacks bring in", "$1.34B", 470, t, SHOT["S3b"]["start"] + 0.1, col=YEL_, size=200, shadow=0.45, lead_col=WHITE, out=ttk - 0.05)
    ui_word(f, "tickets", "$1.38B", 470, t, ttk, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=tie - 0.05)
    ui_word(f, "almost a", "TIE", 470, t, tie, col=YEL_, size=250, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4: movie gets you in the door, popcorn pays the bills ----
def shot_S4(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S4")
    tb = T("d1", "popcorn") - 0.2
    if t < tb:
        comp(f, scale_el(door_el(), 0.95), 620, 1080, scale=pin(t, SHOT["S4"]["start"] + 0.03, 0.3))
        rot_comp(f, scale_el(ticket_el("ADMIT ONE", "MOVIE", (255, 255, 255)), 0.5), 620, 1440, -6, pin(t, SHOT["S4"]["start"] + 0.2, 0.25), 1.0, 0.3)
        guy(f, 260, 1500, 0.8, la=(18, 8), ra=(80, 60), mouth=talk(t), blink=blink_at(t, 1), brow="n", look=(1, 0), expr="n")
    else:
        comp(f, scale_el(popcorn_el(), 0.8), 540, 1110, scale=pin(t, tb, 0.3))
        for i in range(3):
            tq = tb + 0.25 + 0.18 * i
            if t >= tq:
                el = bill_el(("RENT", "STAFF", "POWER")[i], 280, 150)
                rot_comp(f, el, (250, 540, 830)[i], 790 + 20 * (i == 1), (-8, 3, 9)[i], pin(t, tq, 0.25), 1.0, 0.3)
                slam(f, stamp_el("PAID", GRN_, 34), (250, 540, 830)[i], 850 + 20 * (i == 1), -12, t, tq + 0.3)
    ui_word(f, "the movie gets you in the", "DOOR", 470, t, SHOT["S4"]["start"] + 0.1, col=INK, size=220, out=tb - 0.05)
    ui_word(f, "the popcorn pays the", "BILLS", 470, t, tb, col=RED_, size=230)
    return finish(f, n)


# ---- S5: the twist — AMC still lost ~$632M ----
def shot_S5(t, n):
    f = stage("red", (40, 10, 20), 540, 1000, 430); u = lt(t, "S5")
    tl = T("f1", "lost") - 0.2
    if t < tl:
        comp(f, scale_el(popcorn_el(), 0.7), 540, 1080 + 10 * math.sin(t * 5), scale=pin(t, SHOT["S5"]["start"] + 0.05, 0.3))
        kernels(f, t, SHOT["S5"]["start"] + 0.2, 12, 540, 950, 9)
    else:
        # crashing arrow
        k = eo(clamp((t - tl) / 0.6))
        pts = [(180, 820), (360, 900), (480, 860), (640, 1080), (760, 1040), (880, 1320)]
        m_ = max(2, int(2 + k * (len(pts) - 1)))
        for a_, b_ in zip(pts[:m_ - 1], pts[1:m_]): cv2.line(f, a_, b_, C(WHITE), 26, cv2.LINE_AA)
        slam(f, stamp_el("NET LOSS", WHITE, 70), 540, 1180, -8, t, tl + 0.3)
        guy(f, 220, 1500, 0.7, la=(150, 170), ra=(150, 170), mouth=talk(t), blink=False, brow="up", look=(1, -1), expr="wow" if talk(t) == 0 else "n")
        comp(f, chip(SRC_PR, INK, WHITE, 22), 540, 1460, op=clamp((t - tl - 0.4) / 0.3))
    ui_word(f, "and the", "TWIST", 470, t, SHOT["S5"]["start"] + 0.1, col=YEL_, size=230, shadow=0.45, lead_col=WHITE, out=tl - 0.05)
    ui_word(f, "AMC still lost, 2025", "-$632M", 470, t, tl, col=WHITE, size=220, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S5b: rent, staff and debt eat the rest ----
def shot_S5b(t, n):
    f = stage("pink", (120, 40, 200), 540, 1000, 430); u = lt(t, "S5b")
    items = [("RENT $887M", "Rent,"), ("OPERATING $1.79B", "staff"), ("DEBT INTEREST $460M", "debt")]
    for i, (lb, w_) in enumerate(items):
        tq = T("f2", w_) - 0.15
        if t >= tq:
            y = 770 + i * 210
            rot_comp(f, bill_el(lb.split(" ")[0] if i != 2 else "DEBT", 420, 170), 360, y, (-6, 5, -4)[i], pin(t, tq, 0.25), 1.0, 0.3)
            comp(f, chip(lb, INK, WHITE, 30), 720, y, scale=pin(t, tq + 0.1, 0.25))
    comp(f, chip("AMC full-year 2025 — " + SRC_PR[8:], INK, WHITE, 20), 540, 1460, op=clamp((u - 0.5) / 0.3))
    ui_word(f, "rent, staff and debt eat", "THE REST", 470, t, SHOT["S5b"]["start"] + 0.1, col=WHITE, size=200, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S6: you're the real blockbuster ----
def shot_S6(t, n):
    f = stage("purple", (255, 200, 60), 540, 1000, 440); u = lt(t, "S6")
    tb = T("e1", "blockbuster!") - 0.3
    comp(f, scale_el(cinema_el(glow=1.0, label="STARRING: YOU" if t >= tb else ""), 0.8), 540, 980, scale=pin(t, SHOT["S6"]["start"] + 0.03, 0.3))
    if t >= tb: rays(f, 540, 900, 700, (255, 240, 160), 0.45 * clamp((t - tb) / 0.3), t)
    guy(f, 540, 1500, 0.75, la=(18, 8), ra=(150, 160) if t >= tb else (60, 30), mouth=talk(t), blink=blink_at(t, 3), brow="up", look=(0, -1),
        expr="smirk" if talk(t) == 0 else "n", hold=scale_el(popcorn_el(), 0.3), hold_off=(0, -30))
    ui_word(f, "next time you buy the", "LARGE", 470, t, SHOT["S6"]["start"] + 0.1, col=YEL_, size=220, shadow=0.45, lead_col=WHITE, tail="popcorn", out=tb - 0.05)
    ui_word(f, "you're the real", "BLOCKBUSTER", 470, t, tb, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("LARGE popcorn again??", "it pays their rent lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(popcorn_el(), 0.22), hold_off=(20, -10))
        ui_word(f, "send to the friend who buys the", "GIANT POPCORN", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=130, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}


IMPACTS = [(T("i1", "popcorn…") - 0.1, 0.25, 10), (T("i1", "ticket") - 0.1, 0.3, 14), (SHOT["S0b"]["start"] + 0.05, 0.25, 10),
           (T("i2", "math!") - 0.2, 0.3, 12), (T("a1", "twelve") - 0.15, 0.3, 14), (T("a2", "studio!") - 0.2, 0.3, 12),
           (T("a3", "keeps") - 0.15, 0.25, 10), (T("b1", "sixty") - 0.2, 0.3, 14), (T("b2", "twenty") - 0.15, 0.25, 10),
           (T("b3", "eighty") - 0.15, 0.3, 14), (T("c1", "third") - 0.15, 0.3, 12), (T("c2", "billion") - 0.35, 0.25, 10),
           (T("c3", "tie!") - 0.25, 0.4, 16), (T("d1", "popcorn") - 0.15, 0.3, 12), (T("f1", "lost") - 0.15, 0.5, 18),
           (T("e1", "blockbuster!") - 0.25, 0.3, 14)]

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
