# ================= shots: "Chick-fil-A is closed every Sunday and still wins" =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "One") - 0.12, "punch"), ("S1", T("a1", "First,") - 0.2, "whip"),
    ("S1b", T("a2", "That's") - 0.12, "focus"), ("S2a", T("b1", "But") - 0.2, "flash"), ("S2b", T("b3", "So") - 0.12, "whip"),
    ("S3a", T("c1", "An") - 0.15, "zoom"), ("S3b", T("c2", "An") - 0.12, "punch"), ("S4a", T("d1", "Now") - 0.2, "flash"),
    ("S4b", T("d2", "But") - 0.12, "focus"), ("S4c", T("d3", "And") - 0.12, "whip"), ("S5a", T("f1", "So") - 0.2, "whip"),
    ("S5b", T("f1", "The") - 0.12, "focus"), ("S5c", T("f2", "And") - 0.12, "zoom"), ("S6", T("e1", "Closed") - 0.2, "flash"),
    ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_FDD = "Source: Chick-fil-A 2026 franchise disclosure, via QSR & Restaurant Business"


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


def arrow(f, p, q, col, th=22, head=46):
    cv2.line(f, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), C(col), th, cv2.LINE_AA)
    a = math.atan2(q[1] - p[1], q[0] - p[0])
    pts = np.array([[q[0] + head * 0.6 * math.cos(a), q[1] + head * 0.6 * math.sin(a)],
                    [q[0] + head * math.cos(a + 2.5), q[1] + head * math.sin(a + 2.5)],
                    [q[0] + head * math.cos(a - 2.5), q[1] + head * math.sin(a - 2.5)]], np.int32)
    cv2.fillPoly(f, [pts], C(col), cv2.LINE_AA)


def drop(t, t0, y_end, h=900, d=0.35):
    """fall from above with a small bounce"""
    if t < t0: return None
    q = (t - t0) / d
    if q < 1: return y_end - h * (1 - q * q)
    b = q - 1; return y_end - 40 * math.exp(-b * 4) * abs(math.sin(b * 9))


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



def stack(f, x, base, n_full, k, frac=0.0, s=0.8):
    """cash bundles stacked from base upward; k animates 0..1 over the count (n_full + frac)"""
    tot = n_full + frac; shown = tot * clamp(k); el = scale_el(bundle_el(), s); hh = 58 * s
    i = 0
    while i < shown:
        part = min(1.0, shown - i)
        if i >= n_full and frac > 0:
            pm, a = el; hcut = int(a.shape[0] * 0.5)
            comp(f, (pm[hcut:], a[hcut:]), x, base - i * hh - hh * 0.25)
        else:
            y = base - i * hh - (1 - eo(part)) * 160
            comp(f, el, x, y, op=clamp(part * 3))
        i += 1
    return base - tot * hh


# ---- S0: hook — closed door, padlock slams: closed every Sunday ----
def shot_S0(t, n):
    f = stage("red", YEL_, 540, 1000, 440)
    contact(f, 540, 1345, 620, 0.3)
    comp(f, store_el("CLOSED"), 540, 1080, scale=pin(t, 0.0, 0.3))
    tl = T("i1", "closed") - 0.1
    y = drop(t, tl, 1210, 700, 0.3)
    if y is not None: rot_comp(f, padlock_el(), 540, y, -6, 0.62, 1.0, 0.3)
    tb = T("i1", "beating") - 0.12
    if t >= tb:
        rays(f, 540, 760, 520, (255, 240, 160), 0.4 * clamp((t - tb) / 0.3), t)
        comp(f, scale_el(sandwich_el(), 0.55), 540, 760 + 6 * math.sin(t * 6), scale=pin(t, tb, 0.3))
    guy(f, 870, 1490, 0.55, la=(18, 8), ra=(40, 160), mouth=talk(t), blink=blink_at(t, 1), brow="sus", look=(-1, -1),
        expr="sus" if talk(t) == 0 else "n")
    ui_word(f, "chick-fil-a is closed every", "SUNDAY", 470, t, 0.15, col=WHITE, size=190, shadow=0.35, lead_col=WHITE, out=tb - 0.4)
    ui_word(f, "and still beating", "ALMOST EVERYONE", 470, t, tb - 0.3, col=YEL_, size=130, shadow=0.4, lead_col=WHITE)
    return finish(cam(f, 1.0 + 0.015 * t, W / 2, 1000), n)


# ---- S0b: the week — Sunday locked, yet more money ----
def shot_S0b(t, n):
    f = stage("purple", (255, 120, 180), 540, 1000, 440); u = lt(t, "S0b")
    wk = scale_el(week_el(), 0.85)
    comp(f, wk, 540, 980, scale=pin(t, SHOT["S0b"]["start"] + 0.03, 0.3))
    tl = T("i2", "locked.") - 0.15
    if t >= tl:
        rot_comp(f, padlock_el(), 873, 980, 8, 0.45 * (1.6 - 0.6 * eo(clamp((t - tl) / 0.18))), clamp((t - tl) / 0.1), 0.3)
    tm = T("i2", "more") - 0.15
    if t >= tm:
        k = eo(clamp((t - tm) / 0.4))
        arrow(f, (540, 1430), (540, 1430 - 230 * k), GRN_, 30, 70)
        for i in range(3): comp(f, scale_el(cash_el(), 0.4), 330 + i * 60, 1300 - 26 * i, scale=pin(t, tm + 0.08 * i, 0.25))
        for i in range(3): comp(f, scale_el(cash_el(), 0.4), 750 - i * 60, 1300 - 26 * i, scale=pin(t, tm + 0.1 + 0.08 * i, 0.25))
    ui_word(f, "one day a week, doors", "LOCKED", 470, t, T("i2", "One") - 0.05, col=WHITE, size=180, shadow=0.35, lead_col=WHITE, out=tm - 0.1)
    ui_word(f, "and they make", "MORE ANYWAY", 470, t, tm, col=YEL_, size=150, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S1: the size — $23.9B ----
def shot_S1(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S1")
    tt = T("a1", "twenty-four") - 0.15
    comp(f, scale_el(sandwich_el(), 0.9), 540, 1080 + 8 * math.sin(t * 4), scale=pin(t, SHOT["S1"]["start"] + 0.05, 0.3))
    if t >= tt:
        coin_rain(f, t, tt, 12, 540, 340, 1500, 5)
        rot_comp(f, tag_el("$23.9 BILLION", YEL_, INK, 84), 540, 1300, -4, pin(t, tt, 0.25), 1.0, 0.35)
        comp(f, chip(SRC_FDD, INK, WHITE, 22), 540, 1430, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "first, the", "SIZE", 470, t, SHOT["S1"]["start"] + 0.08, col=WHITE, size=200, shadow=0.35, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "u.s. sales in 2025", "ALMOST $24B", 470, t, tt, col=YEL_, size=160, shadow=0.4, lead_col=WHITE)
    return finish(cam(f, 1.04 - 0.04 * eo(clamp(u / 1.5)), W / 2, 1000), n)


# ---- S1b: podium — #3 behind McDonald's and Starbucks ----
def shot_S1b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 420); u = lt(t, "S1b")
    base = 1420; k = eo(clamp(u / 0.5))
    comp(f, podium_el(), 540, base - 210 + 260 * (1 - k))
    cw = 740 / 3; xs = [170 + cw * (i + 0.5) for i in range(3)]
    tops = [base - 260, base - 360, base - 200]
    t3 = T("a2", "three") - 0.12; to = T("a2", "Only") - 0.12
    if t >= t3:
        comp(f, chip("CHICK-FIL-A", RED_, WHITE, 30), xs[2], tops[2] - 60, scale=pin(t, t3, 0.25))
        comp(f, scale_el(sandwich_el(), 0.42), xs[2], tops[2] - 160, scale=pin(t, t3 + 0.1, 0.25))
    if t >= to:
        comp(f, chip("McDONALD'S", INK, WHITE, 30), xs[1], tops[1] - 60, scale=pin(t, to + 0.25, 0.25))
        comp(f, chip("STARBUCKS", INK, WHITE, 30), xs[0], tops[0] - 60, scale=pin(t, to + 0.6, 0.25))
    ui_word(f, "biggest u.s. restaurant chains", "NO. 3", 470, t, t3 - 0.1, col=INK, size=200)
    comp(f, chip("U.S. sales, 2025 - Restaurant Business, Fortune", INK, WHITE, 22), 540, 1460, op=clamp((t - to - 0.6) / 0.3))
    return finish(f, n)


# ---- S2a: split screen unit grid — 13,706 vs ~3,300 ----
def shot_S2a(t, n):
    f = stage("cream", None); u = lt(t, "S2a")
    f[:, :540] = f[:, :540] * 0.12 + np.array(C((236, 46, 40)), np.float32) * 0.88
    f[:, 540:] = f[:, 540:] * 0.12 + np.array(C((0, 150, 140)), np.float32) * 0.88
    cv2.line(f, (540, 620), (540, 1480), C(WHITE), 8, cv2.LINE_AA)
    t14 = T("b1", "fourteen") - 0.2; t3 = T("b2", "About") - 0.1
    if t < t14:
        rot_comp(f, ed_el("", "VS", big_col=YEL_, big_size=220, shadow=0.4), 540, 1000, -6, pin(t, SHOT["S2a"]["start"] + 0.15, 0.3), 1.0, 0.0)
        guy(f, 540, 1490, 0.6, la=(150, 165), ra=(150, 165), mouth=talk(t), expr="wow" if talk(t) == 0 else "n", brow="up", look=(0, -1))
    if t >= t14:
        for i in range(14):
            r_, c_ = divmod(i, 3)
            comp(f, mini_store_el((255, 200, 40)), 175 + 120 * c_, 690 + 118 * r_, scale=pin(t, t14 + 0.05 * i, 0.2))
        comp(f, chip("McDONALD'S: 13,706", INK, WHITE, 30), 295, 1320, op=clamp((t - t14 - 0.3) / 0.2))
    if t >= t3:
        for i in range(4):
            el = mini_store_el(AWN1)
            if i == 3:
                pm, a = el; wc = int(a.shape[1] * 0.3); el = (pm[:, :wc], a[:, :wc])
                x = 630 + 120 * i - 48 + wc / 2 - 360
                comp(f, el, 630 - 48 + wc / 2, 690 + 118, scale=pin(t, t3 + 0.1 * i, 0.2))
            else:
                comp(f, el, 630 + 120 * i, 690, scale=pin(t, t3 + 0.1 * i, 0.2))
        comp(f, chip("CHICK-FIL-A: 3,287", INK, WHITE, 30), 760, 1320, op=clamp((t - t3 - 0.3) / 0.2))
    if t >= t14:
        comp(f, chip("1 icon = 1,000 U.S. restaurants (end of 2025)", INK, WHITE, 24), 540, 1400, op=clamp((t - t14 - 0.5) / 0.3))
        comp(f, chip("Sources: McDonald's 10-K; Chick-fil-A FDD via Restaurant Business", INK, WHITE, 21), 540, 1458, op=clamp((t - t14 - 0.7) / 0.3))
    ui_word(f, "but here's the", "CRAZY PART", 470, t, SHOT["S2a"]["start"] + 0.1, col=WHITE, size=150, shadow=0.4, lead_col=WHITE, out=t14 - 0.05)
    ui_word(f, "mcdonald's u.s. restaurants", "ALMOST 14,000", 470, t, t14, col=WHITE, size=140, shadow=0.45, lead_col=WHITE, out=t3 - 0.1)
    ui_word(f, "chick-fil-a", "ABOUT 3,300", 470, t, t3, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: drive-thru line — each store works way harder ----
def shot_S2b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 980, 420); u = lt(t, "S2b")
    cv2.rectangle(f, (0, 1300), (W, 1420), C((70, 74, 86)), -1, cv2.LINE_AA)
    for j in range(12): cv2.rectangle(f, (j * 100 + int(u * 60) % 100 - 40, 1356), (j * 100 + int(u * 60) % 100 + 10, 1364), C((255, 230, 120)), -1)
    comp(f, scale_el(store_el("OPEN"), 0.82), 650, 1080)
    cols = [(240, 80, 70), (60, 140, 240), (40, 190, 120), (250, 170, 40), (150, 90, 230)]
    for i in range(6):
        x = 470 - i * 190 + 40 * eo(clamp(u / 1.2)) + 6 * math.sin(t * 8 + i)
        if -120 < x < 1200: comp(f, scale_el(car_el(cols[i % 5]), 0.95), x, 1330)
    td = T("b3", "does!") - 0.12
    if t >= td:
        rot_comp(f, stamp_el("BUSY", RED_, 80), 650, 860, -10, 1.5 - 0.5 * eo(clamp((t - td) / 0.18)), clamp((t - td) / 0.1), 0.3)
    ui_word(f, "so each one has to work", "WAY HARDER", 470, t, SHOT["S2b"]["start"] + 0.1, col=INK, size=160)
    return finish(f, n)


# ---- S3a: average McDonald's ~ $4M a year (cash stack) ----
def shot_S3a(t, n):
    f = stage("orange", YEL_, 540, 1000, 420); u = lt(t, "S3a")
    t4 = T("c1", "four") - 0.15; base = 1320
    contact(f, 320, base + 30, 300, 0.3); contact(f, 760, base + 30, 300, 0.3)
    stack(f, 320, base, 4, (t - t4) / 0.6 if t >= t4 else 0)
    comp(f, chip("AVG McDONALD'S", INK, WHITE, 28), 320, base + 70)
    comp(f, ed_el("", "?", big_col=WHITE, big_size=150, shadow=0.3), 760, base - 140 + 8 * math.sin(t * 5), op=clamp(u / 0.3))
    comp(f, chip("AVG CHICK-FIL-A", INK, WHITE, 28), 760, base + 70)
    ui_word(f, "average mcdonald's, per year", "~$4 MILLION", 470, t, T("c1", "average") - 0.1, col=WHITE, size=150, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S3b: average Chick-fil-A ~ $7.5M, in six days ----
def shot_S3b(t, n):
    f = stage("pink", (255, 255, 255), 540, 1000, 420); u = lt(t, "S3b")
    t7 = T("c2", "seven") - 0.15; t6 = T("c2", "six") - 0.15; base = 1320
    contact(f, 320, base + 30, 300, 0.3); contact(f, 760, base + 30, 300, 0.3)
    stack(f, 320, base, 4, 1.0)
    top = stack(f, 760, base, 7, (t - t7) / 0.8 if t >= t7 else 0, 0.5)
    comp(f, chip("AVG McDONALD'S", INK, WHITE, 28), 320, base + 70)
    comp(f, chip("AVG CHICK-FIL-A", RED_, WHITE, 28), 760, base + 70)
    if t >= t6:
        rot_comp(f, stamp_el("6 DAYS A WEEK", RED_, 50), 540, 760, -6, 1.5 - 0.5 * eo(clamp((t - t6) / 0.18)), clamp((t - t6) / 0.1), 0.3)
    comp(f, chip("U.S. avg per restaurant, 2025: McDonald's 10-K (calc.); Restaurant Business", INK, WHITE, 20), 540, 1450,
         op=clamp((t - t7 - 0.6) / 0.3))
    ui_word(f, "average chick-fil-a", "~$7.5 MILLION", 470, t, t7 - 0.2, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4a: the hidden deal — $10,000 to run one ----
def shot_S4a(t, n):
    f = stage("purple", GOLD, 540, 1000, 430); u = lt(t, "S4a")
    tw = T("d1", "Want") - 0.1; tt = T("d1", "ten") - 0.15
    if t < tw:
        comp(f, folder_el(1, True, "THE DEAL"), 540, 1050, scale=pin(t, SHOT["S4a"]["start"] + 0.05, 0.3))
    else:
        rays(f, 600, 1040, 600, (255, 220, 120), 0.35, t)
        guy(f, 330, 1490, 0.85, la=(18, 8), ra=(110, 60), mouth=talk(t), blink=blink_at(t, 2), brow="up", look=(1, -1),
            expr="wow" if talk(t) == 0 else "n")
        rot_comp(f, key_el(), 650, 980 + 10 * math.sin(t * 5), -20 + 6 * math.sin(t * 3), pin(t, tw, 0.3), 1.0, 0.3)
    if t >= tt:
        rot_comp(f, tag_el("$10,000", YEL_, INK, 100), 690, 1250, 6, pin(t, tt, 0.25), 1.0, 0.35)
        comp(f, chip("Fee to become an operator - Fox News, Sept 2026", INK, WHITE, 22), 540, 1440, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "now the", "HIDDEN DEAL", 470, t, SHOT["S4a"]["start"] + 0.08, col=WHITE, size=160, shadow=0.4, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "to run one, you pay just", "$10,000", 470, t, tt, col=YEL_, size=180, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S4b: but you don't own it ----
def shot_S4b(t, n):
    f = stage("cream", (255, 170, 60), 540, 1000, 420); u = lt(t, "S4b")
    contact(f, 660, 1345, 520, 0.3)
    comp(f, scale_el(store_el(), 0.85), 660, 1110)
    guy(f, 230, 1490, 0.7, la=(18, 8), ra=(70, 100), mouth=talk(t), blink=blink_at(t, 3), brow="sus", look=(1, 0),
        expr="sus" if talk(t) == 0 else "n")
    rot_comp(f, scale_el(key_el(), 0.45), 330, 1170, -30, 1.0, 1.0, 0.2)
    tk = T("d2", "keeps") - 0.12
    if t >= tk:
        rot_comp(f, stamp_el("OWNED BY CHICK-FIL-A", RED_, 44), 660, 1000, -8, 1.5 - 0.5 * eo(clamp((t - tk) / 0.18)), clamp((t - tk) / 0.1), 0.3)
    te = T("d2", "equipment.") - 0.15
    if t >= te: comp(f, chip("+ THE EQUIPMENT", INK, WHITE, 32), 660, 1420, scale=pin(t, te, 0.25))
    ui_word(f, "but you don't", "OWN IT", 470, t, T("d2", "don't") - 0.15, col=INK, size=200)
    return finish(f, n)


# ---- S4c: two pies — 15% of sales + half the profit ----
def shot_S4c(t, n):
    f = stage("teal", YEL_, 540, 1000, 430); u = lt(t, "S4c")
    tf = T("d3", "fifteen") - 0.15; th = T("d3", "half") - 0.15
    comp(f, chip("SALES", INK, WHITE, 32), 300, 790)
    pie(f, 300, 1010, 170, 0.15, RED_, (255, 255, 255), eio(clamp((t - tf) / 0.5)) if t >= tf else 0)
    if t >= tf: comp(f, chip("15% OF SALES", RED_, WHITE, 30), 300, 1230, scale=pin(t, tf + 0.3, 0.25))
    if t >= th - 0.4:
        comp(f, chip("PROFIT", INK, WHITE, 32), 780, 790, op=clamp((t - th + 0.4) / 0.2))
        pie(f, 780, 1010, 170, 0.5, RED_, (255, 255, 255), eio(clamp((t - th) / 0.6)) if t >= th else 0)
        if t >= th: comp(f, chip("HALF THE PROFIT", RED_, WHITE, 30), 780, 1230, scale=pin(t, th + 0.4, 0.25))
    ui_word(f, "reportedly, chick-fil-a takes", "15% + HALF", 470, t, tf, col=WHITE, size=170, shadow=0.4, lead_col=WHITE)
    comp(f, chip("As reported by Forbes and Business Insider", INK, WHITE, 24), 540, 1430, op=clamp((t - th - 0.4) / 0.3))
    return finish(f, n)


# ---- S5a: so why not open on Sundays? ----
def shot_S5a(t, n):
    f = stage("red", (255, 220, 120), 540, 1000, 430); u = lt(t, "S5a")
    glow(f, 873, 1080, 170, (255, 240, 150), 0.18 + 0.1 * math.sin(t * 8))
    comp(f, scale_el(week_el(), 0.85), 540, 1080)
    comp(f, ed_el("", "?", big_col=YEL_, big_size=200, shadow=0.35), 873, 860 + 10 * math.sin(t * 5), scale=pin(t, SHOT["S5a"]["start"] + 0.2, 0.3))
    ui_word(f, "so why not open on", "SUNDAYS?", 470, t, SHOT["S5a"]["start"] + 0.08, col=WHITE, size=180, shadow=0.4, lead_col=WHITE)
    guy(f, 220, 1490, 0.6, la=(150, 165), ra=(18, 8), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(1, -1), expr="n")
    return finish(f, n)


# ---- S5b: 1946 — first diner, a day of rest ----
def shot_S5b(t, n):
    f = stage("yellow", (255, 244, 214), 540, 1000, 430); u = lt(t, "S5b")
    tw = T("f1", "workers") - 0.15
    if t < tw + 0.3:
        op = 1 - clamp((t - tw) / 0.3)
        g = f.copy()
        comp(g, scale_el(store_el("CLOSED", sepia=True), 0.7), 360, 1150, scale=pin(t, SHOT["S5b"]["start"] + 0.05, 0.3))
        rot_comp(g, scale_el(calendar_el("SINCE", "1946"), 0.7), 780, 1040, 6, pin(t, T("f1", "nineteen") - 0.15, 0.3), 1.0, 0.3)
        f = f * (1 - op) + g * op
    if t >= tw:
        k = clamp((t - tw) / 0.3)
        g = f.copy(); hammock_scene(g, 540, 1180, t, 1.0); f = f * (1 - k) + g * k
    ui_word(f, "first diner, closed sundays in", "1946", 470, t, T("f1", "founder") - 0.15, col=INK, size=200, out=tw - 0.05)
    ui_word(f, "to give workers a", "DAY OF REST", 470, t, tw, col=INK, size=170)
    return finish(f, n)


# ---- S5c: never changed — years roll 1946 -> 2026 ----
def shot_S5c(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S5c")
    k = eio(clamp(u / 1.0)); yr = int(1946 + 80 * k)
    rot_comp(f, scale_el(calendar_el("STILL", str(yr)), 0.9), 540, 990, -3 + 2 * math.sin(t * 20) * (1 - k), 1.0, 1.0, 0.3)
    tc = T("f2", "changed") - 0.15
    if t >= tc:
        rot_comp(f, stamp_el("CLOSED SUNDAYS", RED_, 60), 540, 1330, -6, 1.5 - 0.5 * eo(clamp((t - tc) / 0.18)), clamp((t - tc) / 0.1), 0.3)
    ui_word(f, "and they", "NEVER CHANGED IT", 470, t, T("f2", "never") - 0.15, col=INK, size=130)
    return finish(f, n)


# ---- S6: payoff — busiest restaurant $20M+ a year ----
def shot_S6(t, n):
    f = stage("emerald", GOLD, 540, 980, 430); u = lt(t, "S6")
    tb = T("e1", "busiest") - 0.15; tt = T("e1", "twenty") - 0.15
    rays(f, 540, 1060, 700, (255, 230, 140), 0.45 * clamp((t - tb) / 0.3) if t >= tb else 0, t)
    comp(f, scale_el(store_el("CLOSED" if t < tb else "OPEN"), 0.8), 540, 1120, scale=pin(t, SHOT["S6"]["start"] + 0.05, 0.3))
    if t >= tt:
        coin_rain(f, t, tt, 12, 540, 360, 1500, 9)
        rot_comp(f, tag_el("$20M+ A YEAR", YEL_, INK, 90), 540, 1300, -5, pin(t, tt, 0.25), 1.0, 0.35)
        comp(f, chip("Top U.S. restaurant, 2025 - Restaurant Business, Fortune", INK, WHITE, 22), 540, 1440, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "closed one day a week", "STILL WINNING", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, size=150, shadow=0.4, lead_col=WHITE, out=tb - 0.05)
    ui_word(f, "their busiest restaurant", "$20M+ A YEAR", 470, t, tb, col=YEL_, size=150, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("craving it on a sunday", "watch this lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(sandwich_el(), 0.3), hold_off=(20, -30))
        ui_word(f, "send to the friend who craves it on a", "SUNDAY", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=150, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "closed") + 0.2, 0.3, 14), (SHOT["S0b"]["start"] + 0.05, 0.25, 10), (T("i2", "locked.") - 0.05, 0.3, 14),
           (T("a1", "twenty-four") - 0.15, 0.3, 12), (T("a2", "three") - 0.12, 0.25, 10), (T("b2", "About") - 0.1, 0.25, 8),
           (T("b3", "does!") - 0.05, 0.3, 12), (T("c2", "seven") - 0.15, 0.25, 10), (T("c2", "six") - 0.1, 0.3, 14),
           (T("d1", "ten") - 0.15, 0.3, 12), (T("d2", "keeps") - 0.05, 0.3, 14), (T("d3", "half") - 0.15, 0.25, 10),
           (T("f2", "changed") - 0.05, 0.3, 14), (T("e1", "twenty") - 0.15, 0.3, 14)]
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
