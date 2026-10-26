# ================= shots: "Printer ink costs more than champagne" =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "That's") - 0.12, "punch"), ("S1", T("a1", "Step") - 0.2, "whip"),
    ("S1b", T("a2", "You") - 0.12, "focus"), ("S2", T("b1", "Step") - 0.2, "flash"), ("S3a", T("c1", "A") - 0.2, "zoom"),
    ("S3b", T("c2", "A") - 0.12, "punch"), ("S3c", T("c3", "So") - 0.12, "flash"), ("S4a", T("d1", "Step") - 0.2, "whip"),
    ("S4b", T("d2", "That's") - 0.12, "focus"), ("S4c", T("d3", "And") - 0.12, "zoom"), ("S5a", T("f1", "Even") - 0.2, "flash"),
    ("S5b", T("f2", "If") - 0.12, "focus"), ("S6", T("e1", "So") - 0.2, "flash"), ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_WHICH = "Source: Which? (UK), Sept 2022 - Epson ink set vs Dom Perignon"
SRC_HP = "Source: HP Inc. fiscal 2025 results (year to Oct 31, 2025)"


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


def pie(f, cx, cy, r, frac, col, base=(255, 255, 255), k=1.0):
    sh = f.copy(); cv2.circle(sh, (cx + 8, cy + 14), r, (0, 0, 0), -1, cv2.LINE_AA); f[:] = f * 0.75 + sh * 0.25
    cv2.circle(f, (cx, cy), r, C(base), -1, cv2.LINE_AA)
    if frac * k > 0.002: cv2.ellipse(f, (cx, cy), (r, r), -90, 0, 360 * frac * k, C(col), -1, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), r, C(INK), 8, cv2.LINE_AA)


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


def seesaw(f, ang, cx=540, cy=1240, L=320):
    """plank pivoting on a triangle; ang>0 tips the LEFT end down. returns end points (left, right) on its top surface"""
    a = math.radians(-ang); dx, dy = L * math.cos(a), L * math.sin(a)
    tri = np.array([[cx, cy + 6], [cx - 90, cy + 190], [cx + 90, cy + 190]], np.int32)
    contact(f, cx, cy + 196, 380, 0.3)
    cv2.fillPoly(f, [tri], C((70, 74, 86)), cv2.LINE_AA)
    p, q = (cx - dx, cy - dy), (cx + dx, cy + dy)
    cv2.line(f, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), C(INK), 40, cv2.LINE_AA)
    cv2.line(f, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), C((236, 186, 120)), 26, cv2.LINE_AA)
    nx, ny = math.sin(a), -math.cos(a)
    return (p[0] + nx * 20, p[1] + ny * 20), (q[0] + nx * 20, q[1] + ny * 20)


def drip(f, x, y0, y1, t, col=BLK_, n=3):
    for i in range(n):
        q = ((t * 1.6 + i / n) % 1.0)
        comp(f, scale_el(drop_el(col, 60), 0.5), x, y0 + (y1 - y0) * q * q, op=clamp((1 - q) * 4))


# ---- S0: hook — ink cartridge vs champagne on a seesaw; the ink side slams down ----
def shot_S0(t, n):
    f = stage("purple", (255, 120, 200), 540, 980, 440)
    ts = T("i1", "seven") - 0.12; tc = T("i1", "champagne?") - 0.15
    k = eback(clamp((t - ts) / 0.45)) if t >= ts else 0.0
    ang = (-2 + 2 * math.sin(t * 3)) * (1 - clamp(k)) + 16 * k
    pl, pr = seesaw(f, ang)
    rot_comp(f, cartridge_el(BLK_, 1.0, label="INK"), pl[0], pl[1] - 122, ang, 1.0, 1.0, 0.3)
    rot_comp(f, scale_el(bottle_el(), 0.62), pr[0], pr[1] - 196, ang, 1.0, 1.0, 0.3)
    if t >= ts:
        rot_comp(f, tag_el("$$$$$", RED_, WHITE, 60), pl[0] + 90, pl[1] - 300, -8, pin(t, ts + 0.1, 0.25), 1.0, 0.3)
    if t >= tc:
        rot_comp(f, tag_el("$", GRN_, WHITE, 60), pr[0] - 40, pr[1] - 470, 6, pin(t, tc, 0.25), 1.0, 0.3)
    ui_word(f, "printer ink can cost", "7X MORE", 470, t, 0.12, col=WHITE, size=200, shadow=0.35, lead_col=WHITE, out=tc - 0.05)
    ui_word(f, "than fancy", "CHAMPAGNE", 470, t, tc, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    return finish(cam(f, 1.0 + 0.015 * t, W / 2, 1000), n)


# ---- S0b: not a mistake — it's the plan ----
def shot_S0b(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S0b")
    tm = T("i2", "mistake.") - 0.15; tp = T("i2", "plan!") - 0.15
    if t < tp:
        comp(f, scale_el(printer_el(), 0.85), 540, 1080, scale=pin(t, SHOT["S0b"]["start"] + 0.03, 0.3))
        slam(f, stamp_el("MISTAKE?", WHITE, 70), 540, 1060, -8, t, tm)
    else:
        rays(f, 540, 1060, 620, (255, 240, 160), 0.4, t)
        rot_comp(f, scale_el(folder_el("$", True, "THE PLAN"), 1.5), 540, 1060, -4 + 3 * math.sin(t * 4), pin(t, tp, 0.3), 1.0, 0.35)
    guy(f, 860, 1490, 0.55, la=(18, 8), ra=(40, 160), mouth=talk(t), blink=blink_at(t, 1), brow="sus", look=(-1, -1),
        expr="sus" if talk(t) == 0 else "n")
    ui_word(f, "that's not a", "MISTAKE", 470, t, SHOT["S0b"]["start"] + 0.05, col=WHITE, size=190, shadow=0.35, lead_col=WHITE, out=tp - 0.05)
    ui_word(f, "it's the whole", "PLAN", 470, t, tp, col=YEL_, size=220, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S1: step 1 — the printer is the bait (on a trap), cheap price tag ----
def shot_S1(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S1")
    tc = T("a1", "cheap.") - 0.15
    comp(f, mousetrap_el(), 540, 1360)
    y = 1150 - 600 * (1 - eo(clamp(u / 0.35)))
    comp(f, scale_el(printer_el(), 0.95), 540, y)
    if t >= tc:
        rot_comp(f, tag_el("CHEAP!", YEL_, INK, 90), 700, 880 + 6 * math.sin(t * 5), 10, pin(t, tc, 0.25), 1.0, 0.35)
    ui_word(f, "step 1", "SELL IT CHEAP", 470, t, SHOT["S1"]["start"] + 0.08, col=INK, size=150)
    return finish(cam(f, 1.04 - 0.04 * eo(clamp(u / 1.5)), W / 2, 1100), n)


# ---- S1b: you think "what a deal" and carry it home ----
def shot_S1b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 980, 420); u = lt(t, "S1b")
    th = T("a2", "carry") - 0.15
    if t < th:
        guy(f, 400, 1490, 0.95, la=(150, 165), ra=(150, 165), mouth=talk(t), blink=blink_at(t, 2), brow="up", look=(1, -1),
            expr="wow" if talk(t) == 0 else "n")
        comp(f, scale_el(printer_el(), 0.55), 760, 1360)
        comp(f, bubble_el("WHAT A DEAL!", 50), 620, 820, scale=pin(t, T("a2", "deal!") - 0.25, 0.3))
    else:
        w = walk(t, 1.2); x = 300 + 330 * eo(clamp((t - th) / 1.4))
        cv2.rectangle(f, (780, 1190), (960, 1490), C((250, 246, 236)), -1, cv2.LINE_AA)
        cv2.fillPoly(f, [np.array([[760, 1200], [870, 1070], [980, 1200]], np.int32)], C(RED_), cv2.LINE_AA)
        cv2.rectangle(f, (835, 1350), (905, 1490), C((120, 72, 40)), -1, cv2.LINE_AA)
        guy(f, x, 1490, 0.8, la=(150, 40), ra=(150, 40), ll=w["ll"], rl=w["rl"], bob=w["bob"], mouth=talk(t), expr="smirk", brow="up")
        comp(f, scale_el(printer_el(), 0.42), x, 1010 + w["bob"] * 0.8)
    ui_word(f, "wow, what a", "DEAL!", 470, t, T("a2", "wow,") - 0.1, col=INK, size=200)
    return finish(f, n)


# ---- S2: step 2 — cartridge drains, buy more, receipt grows ----
def shot_S2(t, n):
    f = stage("teal", (0, 220, 255), 540, 1000, 430); u = lt(t, "S2")
    to = T("b1", "out.") - 0.2; tm = T("b1", "more.") - 0.15
    ta1 = T("b1", "again.", 0) - 0.15; ta2 = T("b1", "again.", 1) - 0.15
    if t < tm:
        lvl = 1 - clamp((t - SHOT["S2"]["start"]) / max(0.3, to + 0.2 - SHOT["S2"]["start"]))
        comp(f, scale_el(cartridge_el(BLK_, round(lvl * 20) / 20, label="INK"), 1.6), 540, 1100)
        if lvl <= 0.01:
            slam(f, stamp_el("EMPTY", RED_, 80), 540, 1100, -10, t, to + 0.15)
            comp(f, chip("LOW INK!", RED_, WHITE, 40), 540, 1380, op=0.5 + 0.5 * math.sin(t * 14))
    else:
        nrows = 1 + (1 if t >= ta1 else 0) + (1 if t >= ta2 else 0)
        rc = receipt_el(nrows * 2)
        comp(f, rc, 360, 690 + rc[1].shape[0] / 2, scale=pin(t, tm, 0.25) if t < ta1 else 1.0)
        for i, tt_ in enumerate((tm, ta1, ta2)):
            if t >= tt_:
                rot_comp(f, cartridge_el([CYAN_, MAG_, YELI][i], 1.0, label="INK"), 780, 1340 - i * 230, -8 + 8 * i, pin(t, tt_, 0.25), 1.0, 0.3)
        if t >= ta1: slam(f, stamp_el("AGAIN", RED_, 60), 360, 1290, -8, t, ta1)
        if t >= ta2: slam(f, stamp_el("AND AGAIN", RED_, 60), 360, 1410, 6, t, ta2)
    ui_word(f, "step 2", "THE INK RUNS OUT", 470, t, SHOT["S2"]["start"] + 0.08, col=WHITE, size=130, shadow=0.4, lead_col=WHITE, out=tm - 0.05)
    ui_word(f, "so you buy", "MORE", 470, t, tm, col=YEL_, size=200, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S3a: price per ml — ink £1.78 ----
def shot_S3a(t, n):
    f = stage("cream", (255, 120, 200), 540, 1000, 430); u = lt(t, "S3a")
    te = T("c1", "eighty,") - 0.2
    k = clamp((t - SHOT["S3a"]["start"] - 0.3) / 1.6)
    rot_comp(f, scale_el(cartridge_el(BLK_, 1.0 - 0.6 * k, label="INK"), 0.8), 640, 760, 150, pin(t, SHOT["S3a"]["start"] + 0.05, 0.3), 1.0, 0.3)
    drip(f, 600, 870, 1040, t, BLK_)
    comp(f, beaker_el(round(0.05 + 0.25 * k, 2), BLK_), 540, 1180)
    comp(f, chip("1 ML", INK, WHITE, 30), 360, 1240, op=clamp(u / 0.4))
    if t >= te:
        rot_comp(f, tag_el("£1.78 / ML", RED_, WHITE, 80), 540, 1330, -4, pin(t, te, 0.25), 1.0, 0.35)
        comp(f, chip(SRC_WHICH, INK, WHITE, 22), 540, 1450, op=clamp((t - te - 0.4) / 0.3))
    ui_word(f, "a uk consumer group", "CHECKED", 470, t, SHOT["S3a"]["start"] + 0.1, col=INK, size=170, out=te - 0.05)
    ui_word(f, "one ink set, per milliliter", "£1.78", 470, t, te, col=RED_, size=200)
    return finish(f, n)


# ---- S3b: champagne 24p per ml ----
def shot_S3b(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S3b")
    tt = T("c2", "twenty-four") - 0.2
    rays(f, 540, 1080, 620, (255, 230, 140), 0.25, t)
    comp(f, scale_el(bottle_el(), 0.9), 380, 1130, scale=pin(t, SHOT["S3b"]["start"] + 0.03, 0.3))
    comp(f, flute_el(), 700, 1200, scale=pin(t, SHOT["S3b"]["start"] + 0.15, 0.3))
    if t >= tt:
        rot_comp(f, tag_el("24p / ML", YEL_, INK, 80), 660, 900, 6, pin(t, tt, 0.25), 1.0, 0.35)
        comp(f, chip("Which?, 2022: £180 bottle = 24p per ml", INK, WHITE, 24), 540, 1450, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "dom perignon champagne", "24p PER ML", 470, t, SHOT["S3b"]["start"] + 0.1, col=WHITE, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S3c: bar chart — ink 7x pricier ----
def shot_S3c(t, n):
    f = stage("orange", YEL_, 540, 1000, 430); u = lt(t, "S3c")
    base = 1420; k = eo(clamp((u - 0.1) / 0.7))
    cv2.line(f, (180, base), (900, base), C(INK), 8, cv2.LINE_AA)
    t1 = bar(f, 360, base, 200, 100, YEL_, k)
    t2 = bar(f, 720, base, 200, 100 * 7.4, BLK_, k)
    comp(f, chip("CHAMPAGNE 24p", INK, WHITE, 28), 360, t1 - 40)
    comp(f, chip("INK £1.78", RED_, WHITE, 30), 720, t2 - 40)
    ts = T("c3", "seven") - 0.15
    slam(f, stamp_el("7X", WHITE, 110), 360, 1000, -10, t, ts)
    ui_word(f, "per milliliter, the ink was", "7X PRICIER", 470, t, SHOT["S3c"]["start"] + 0.1, col=WHITE, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S4a: step 3 — the money: $10.9B of supplies ----
def shot_S4a(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S4a")
    te = T("d1", "eleven") - 0.15
    cols = [CYAN_, MAG_, YELI, BLK_]
    for i in range(8):
        r_, c_ = divmod(i, 4)
        rot_comp(f, scale_el(cartridge_el(cols[c_], 1.0, label="INK"), 0.7), 270 + c_ * 180, 860 + r_ * 200, -4 + 3 * ((i * 7) % 3),
                 pin(t, SHOT["S4a"]["start"] + 0.05 * i, 0.25), 1.0, 0.25)
    if t >= te:
        coin_rain(f, t, te, 12, 540, 360, 1500, 7)
        rot_comp(f, tag_el("$10.9 BILLION", YEL_, INK, 84), 540, 1310, -4, pin(t, te, 0.25), 1.0, 0.35)
        comp(f, chip(SRC_HP + ", supplies", INK, WHITE, 22), 540, 1450, op=clamp((t - te - 0.4) / 0.3))
    ui_word(f, "step 3", "THE MONEY", 470, t, SHOT["S4a"]["start"] + 0.08, col=WHITE, size=190, shadow=0.35, lead_col=WHITE, out=te - 0.05)
    ui_word(f, "hp printer supplies, last year", "~$11 BILLION", 470, t, te, col=YEL_, size=150, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S4b: pie — supplies = about two thirds of printing sales ----
def shot_S4b(t, n):
    f = stage("pink", (120, 40, 200), 540, 1000, 430); u = lt(t, "S4b")
    tt = T("d2", "two") - 0.2
    k = eio(clamp((t - tt) / 0.7)) if t >= tt else 0
    pie(f, 540, 1020, 250, 0.654, BLK_, YEL_, k)
    if t >= tt + 0.5:
        comp(f, chip("SUPPLIES $10.9B", BLK_, WHITE, 32), 540, 1320, scale=pin(t, tt + 0.5, 0.25))
        comp(f, chip("PRINTERS + OTHER $5.8B", YEL_, INK, 28), 540, 1390, scale=pin(t, tt + 0.7, 0.25))
    comp(f, chip(SRC_HP, INK, WHITE, 22), 540, 1460, op=clamp((t - tt - 0.9) / 0.3))
    ui_word(f, "of hp's printing sales", "ABOUT 2/3", 470, t, SHOT["S4b"]["start"] + 0.1, col=WHITE, size=190, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S4c: profit bars — printing vs computers ----
def shot_S4c(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S4c")
    tf = T("d3", "fifty") - 0.2; th = T("d3", "half") - 0.2
    base = 1330; k = eo(clamp((u - 0.1) / 0.7)); sc_ = 0.17
    cv2.line(f, (180, base), (900, base), C(INK), 8, cv2.LINE_AA)
    t1 = bar(f, 360, base, 210, 2054 * sc_, (120, 130, 150), k)
    t2 = bar(f, 720, base, 210, 3118 * sc_, BLK_, k)
    comp(f, chip("$2.1B profit", INK, WHITE, 30), 360, t1 - 40, op=clamp(k * 2 - 1))
    comp(f, chip("$3.1B profit", RED_, WHITE, 32), 720, t2 - 40, op=clamp(k * 2 - 1))
    comp(f, chip("COMPUTERS", INK, WHITE, 28), 360, base + 40); comp(f, chip("PRINTING", INK, WHITE, 28), 720, base + 40)
    if t >= th:
        comp(f, chip("sales $38.5B", WHITE, INK, 28), 360, base - 70, scale=pin(t, th, 0.25))
        comp(f, chip("sales $16.7B", YEL_, INK, 28), 720, base - 70, scale=pin(t, th + 0.12, 0.25))
    comp(f, chip(SRC_HP + ", segment profit", INK, WHITE, 22), 540, 1450, op=clamp((t - tf - 0.4) / 0.3))
    ui_word(f, "printing profit vs computers", "+50%", 470, t, SHOT["S4c"]["start"] + 0.1, col=INK, size=200, out=th - 0.05)
    ui_word(f, "with less than", "HALF THE SALES", 470, t, th, col=RED_, size=150)
    return finish(f, n)


# ---- S5a: even HP's boss said it on TV ----
def shot_S5a(t, n):
    f = stage("purple", (0, 200, 255), 540, 1000, 430); u = lt(t, "S5a")
    comp(f, scale_el(tv_el(["", "", "ON AIR"], sub="BUSINESS TV"), 0.8), 620, 1060, scale=pin(t, SHOT["S5a"]["start"] + 0.05, 0.3))
    guy(f, 190, 1490, 0.6, la=(18, 8), ra=(110, 70), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(1, -1), expr="wow" if talk(t) == 0 else "n")
    ui_word(f, "even hp's", "BOSS SAID IT", 470, t, SHOT["S5a"]["start"] + 0.08, col=WHITE, size=160, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S5b: the quote on the TV ----
def shot_S5b(t, n):
    f = stage("cream", (255, 170, 60), 540, 1000, 430); u = lt(t, "S5b")
    ql = ["IF THIS CUSTOMER DOESN'T", "PRINT ENOUGH OR DOESN'T", "USE OUR SUPPLIES, IT'S", "A BAD INVESTMENT."]
    marks = [T("f2", "If"), T("f2", "print"), T("f2", "use"), T("f2", "bad")]
    nshow = sum(1 for m in marks if t >= m - 0.1)
    comp(f, tv_el(ql[:nshow] + [""] * (4 - nshow), sub="HP CEO, CNBC 2024"), 540, 1000)
    tb = T("f2", "bad") - 0.12
    slam(f, stamp_el("BAD INVESTMENT", RED_, 56), 540, 1380, -6, t, tb + 0.4)
    comp(f, chip("HP CEO Enrique Lores on CNBC, Jan 2024 (via Ars Technica)", INK, WHITE, 22), 540, 1470, op=clamp(u / 0.4))
    ui_word(f, "hp's ceo, on customers", "WHO SKIP HP INK", 470, t, SHOT["S5b"]["start"] + 0.1, col=INK, size=120)
    return finish(f, n)


# ---- S6: payoff — the ink is the product ----
def shot_S6(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S6")
    ti = T("e1", "ink") - 0.2
    if t < ti:
        comp(f, scale_el(printer_el(smile=False), 0.9), 540, 1100, scale=pin(t, SHOT["S6"]["start"] + 0.05, 0.3))
        slam(f, stamp_el("NOT THE PRODUCT", WHITE, 56), 540, 1100, -8, t, T("e1", "product.") - 0.15)
    else:
        rays(f, 600, 1060, 700, (255, 240, 160), 0.5 * clamp((t - ti) / 0.3), t)
        comp(f, scale_el(printer_el(), 0.4), 260, 1390)
        rot_comp(f, scale_el(cartridge_el(BLK_, 1.0, label="INK"), 1.5), 600, 1080 + 8 * math.sin(t * 5), -5, pin(t, ti, 0.3), 1.0, 0.35)
        comp(f, tag_el("THE PRODUCT", YEL_, INK, 60), 640, 820 + 6 * math.sin(t * 5), scale=pin(t, ti + 0.15, 0.3))
    ui_word(f, "the printer was never", "THE PRODUCT", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, size=160, shadow=0.4, lead_col=WHITE, out=ti - 0.05)
    ui_word(f, "the real product", "IS THE INK", 470, t, ti, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("ink is HOW much??", "watch this lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(cartridge_el(MAG_, 1.0, label="INK"), 0.4), hold_off=(20, -30))
        ui_word(f, "send to the friend who just paid for", "NEW INK", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=150, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "seven") + 0.05, 0.3, 14), (SHOT["S0b"]["start"] + 0.05, 0.25, 10), (T("i2", "mistake.") - 0.05, 0.3, 12),
           (T("i2", "plan!") - 0.1, 0.3, 14), (T("a1", "cheap.") - 0.12, 0.25, 10), (T("b1", "out.") + 0.0, 0.3, 12),
           (T("b1", "again.", 0) - 0.1, 0.25, 10), (T("b1", "again.", 1) - 0.1, 0.25, 12), (T("c1", "eighty,") - 0.2, 0.3, 12),
           (T("c3", "seven") - 0.12, 0.3, 14), (T("d1", "eleven") - 0.15, 0.3, 14), (T("d3", "fifty") - 0.15, 0.25, 10),
           (T("f2", "bad") + 0.3, 0.3, 14), (T("e1", "product.") - 0.1, 0.3, 12), (T("e1", "ink") - 0.2, 0.3, 14)]


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
