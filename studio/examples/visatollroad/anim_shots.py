# ================= shots: "Visa never lends you a dollar — the toll road" (Visa FY2025 10-K + Q4 FY2025 8-K) =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "No") - 0.12, "punch"), ("S1", T("a1", "First,") - 0.2, "whip"),
    ("S1b", T("a2", "Your") - 0.12, "focus"), ("S1c", T("a3", "Visa") - 0.12, "zoom"), ("S2", T("b1", "Think") - 0.2, "flash"),
    ("S2b", T("b2", "On") - 0.12, "whip"), ("S3", T("b3", "Every") - 0.12, "focus"), ("S4", T("c1", "Now") - 0.2, "punch"),
    ("S4b", T("c2", "That's") - 0.12, "zoom"), ("S5", T("c3", "Tiny") - 0.12, "whip"), ("S6", T("d1", "And") - 0.2, "flash"),
    ("S7", T("e1", "So") - 0.2, "whip"), ("S8", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_K = "Source: Visa FY2025 annual report (SEC 10-K)"
SRC_8K = "Source: Visa Q4 & fiscal 2025 results (SEC 8-K, Oct 2025)"
CARD_A = ((120, 60, 230), (40, 190, 200)); CARD_B = ((255, 90, 120), (255, 170, 60))


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


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def coin_rain(f, t, t0, n=10, x0=540, spread=360, y1=1500, seed=0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = x0 + rng.uniform(-spread, spread); r0 = rng.uniform(-30, 30); q = t - t0 - 0.08 * i
        if q <= 0: continue
        y = 640 + 900 * ((q * 0.9) % 1.0)
        if y < y1: rot_comp(f, coin_el(46, abs(math.cos(q * 5 + i))), x, y, r0, 1.0, 1.0, 0.2)


def toll_coin(f, t, t0, x0, y0, x1, y1):
    """a coin arcs from (x0,y0) to (x1,y1) over 0.45 s"""
    q = (t - t0) / 0.45
    if 0 <= q <= 1:
        x = x0 + (x1 - x0) * q; y = y0 + (y1 - y0) * q - 260 * math.sin(math.pi * q)
        comp(f, coin_el(40, abs(math.cos(q * 9))), x, y)


# ---- S0: hook — a card, $0 lent, keeps ~half as profit ----
def shot_S0(t, n):
    f = stage("purple", (255, 200, 60), 540, 1000, 440)
    tn = T("i1", "never") - 0.15; th = T("i1", "half") - 0.2
    rot_comp(f, card_el(*CARD_A), 540, 1040 + 10 * math.sin(t * 3), -8 + 3 * math.sin(t * 2), pin(t, 0.0, 0.3) * 1.25, 1.0, 0.4)
    slam(f, stamp_el("$0 LENT", RED_, 80), 560, 1060, -12, t, tn + 0.25)
    if t >= th:
        rays(f, 540, 1040, 700, (255, 240, 160), 0.4 * clamp((t - th) / 0.3), t)
        coin_rain(f, t, th, 12, 540, 380, 1480, 2)
    ui_word(f, "Visa lends you", "$0", 470, t, 0.1, col=YEL_, size=230, shadow=0.45, lead_col=WHITE, out=th - 0.05)
    ui_word(f, "yet keeps as profit about", "HALF", 470, t, th, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1000), n)


# ---- S0b: no loans, no interest — what's the trick? ----
def shot_S0b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S0b")
    tl = T("i2", "loans.") - 0.25; ti = T("i2", "interest.") - 0.25; tq = T("i2", "trick?") - 0.3
    rot_comp(f, loan_doc_el(), 400, 1060, -5, pin(t, SHOT["S0b"]["start"] + 0.02, 0.3), 1.0, 0.35)
    slam(f, stamp_el("NO LOANS", RED_, 64), 400, 960, -14, t, tl)
    slam(f, stamp_el("NO INTEREST", RED_, 56), 400, 1170, 10, t, ti)
    guy(f, 820, 1500, 0.78, la=(30, 20), ra=(150, 150) if t >= tq else (18, 8), mouth=talk(t), blink=blink_at(t, 1),
        brow="sus" if t >= tq else "up", look=(-1, -1), expr="sus" if (t >= tq and talk(t) == 0) else "n")
    if t >= tq: comp(f, bubble_el("???", 60), 820, 880, scale=pin(t, tq, 0.3))
    ui_word(f, "no loans, no interest", "SO WHAT'S", 470, t, SHOT["S0b"]["start"] + 0.08, col=INK, size=170, out=tq - 0.05)
    ui_word(f, "so what's the", "TRICK?", 470, t, tq, col=RED_, size=230)
    return finish(f, n)


# ---- S1: your bank makes the card ----
def shot_S1(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S1")
    td = T("a1", "doesn't") - 0.2; tb = T("a1", "bank") - 0.25
    comp(f, bank_el("YOUR BANK", 560, 500), 540, 1180, scale=pin(t, SHOT["S1"]["start"] + 0.03, 0.3))
    if t >= tb:
        k = eo(clamp((t - tb) / 0.5))
        rot_comp(f, card_el(*CARD_A, w=440, h=276), 540, 1020 - 240 * k, -8 * (1 - k) + 4 * math.sin(t * 3), 0.6 + 0.4 * k, 1.0, 0.35)
        rays(f, 540, 790, 420, (255, 255, 255), 0.35 * clamp((t - tb) / 0.3), t)
    elif t >= td:
        comp(f, chip("NOT VISA", RED_, WHITE, 40), 540, 840, scale=pin(t, td, 0.25))
    ui_word(f, "Visa doesn't even", "MAKE IT", 470, t, SHOT["S1"]["start"] + 0.08, col=INK, size=190, out=tb - 0.05)
    ui_word(f, "your card comes from", "YOUR BANK", 470, t, tb, col=RED_, size=190)
    return finish(cam(f, 1.03 - 0.03 * eo(clamp(u / 1.5)), W / 2, 1050), n)


# ---- S1b: your bank lends, your bank takes the risk ----
def shot_S1b(t, n):
    f = stage("orange", YEL_, 540, 1000, 430); u = lt(t, "S1b")
    tl = T("a2", "lends") - 0.2; tr = T("a2", "risk") - 0.25
    comp(f, bank_el("YOUR BANK", 460, 410), 330, 1210, scale=pin(t, SHOT["S1b"]["start"] + 0.03, 0.3))
    if t >= tl:
        toll_coin(f, t, tl + 0.05, 330, 1050, 800, 1240)
        rot_comp(f, cash_el(), 800, 1180 + 6 * math.sin(t * 5), 8, pin(t, tl + 0.45, 0.25), 1.0, 0.3)
    guy(f, 800, 1500, 0.72, la=(30, 20), ra=(70, 40), mouth=talk(t), blink=blink_at(t, 2), brow="up", look=(-1, 0), expr="n")
    if t >= tr:
        y = 760 + 210 * eo(clamp((t - tr) / 0.3))
        rot_comp(f, tag_el("RISK", INK, WHITE, 90), 330, y, -6, 1.0, 1.0, 0.4)
        comp(f, chip("\"We do not issue cards, extend credit…\" — " + SRC_K[8:], INK, WHITE, 20), 540, 1450, op=clamp((t - tr - 0.3) / 0.3))
    ui_word(f, "the loan comes from", "YOUR BANK", 470, t, SHOT["S1b"]["start"] + 0.08, col=WHITE, size=190, shadow=0.4, lead_col=WHITE, out=tr - 0.05)
    ui_word(f, "and so does the", "RISK", 470, t, tr, col=YEL_, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S1c: Visa owns the road in the middle ----
def shot_S1c(t, n):
    f = stage("teal", (255, 214, 120), 540, 900, 400); u = lt(t, "S1c")
    road(f, 1180, 1340, t, 500)
    comp(f, bank_el("BANKS", 300, 280), 170, 1060, scale=pin(t, SHOT["S1c"]["start"] + 0.03, 0.3))
    comp(f, shop_el((255, 90, 120), 260, 260), 910, 1060, scale=pin(t, SHOT["S1c"]["start"] + 0.12, 0.3))
    for i in range(3):
        x = -200 + ((u * 420 + i * 430) % 1500); comp(f, scale_el(car_el(((60, 170, 255), (255, 120, 60), (120, 220, 90))[i]), 0.62), x, 1240)
    tr = T("a3", "road") - 0.2
    if t >= tr: comp(f, chip("VISA'S ROAD", INK, YEL_, 44), 540, 1410, scale=pin(t, tr, 0.25))
    ui_word(f, "Visa just owns the", "ROAD", 470, t, SHOT["S1c"]["start"] + 0.08, col=YEL_, size=240, shadow=0.45, lead_col=WHITE, tail="in the middle")
    return finish(f, n)


# ---- S2: a giant toll road — booth + barrier lifts ----
def shot_S2(t, n):
    f = stage("pink", (255, 240, 120), 540, 980, 420); u = lt(t, "S2")
    tt = T("b1", "toll") - 0.2
    road(f, 1260, 1420, t, 300)
    comp(f, tollbooth_el(), 300, 1020, scale=pin(t, SHOT["S2"]["start"] + 0.03, 0.3))
    ang = 0.0 if t < tt else 75 * eo(clamp((t - tt) / 0.4))
    barrier(f, 420, 1200, ang, 400)
    cx = 1250 - 900 * eo(clamp((u - 0.2) / 1.4))
    comp(f, scale_el(car_el((60, 170, 255)), 0.7), cx, 1330)
    ui_word(f, "think of it like a giant", "TOLL ROAD", 470, t, SHOT["S2"]["start"] + 0.1, col=WHITE, size=190, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: split screen — ~14,500 banks | 175M+ stores ----
def shot_S2b(t, n):
    f = stage("emerald", (0, 220, 200), 540, 1000, 430); u = lt(t, "S2b")
    tb = T("b2", "banks.") - 0.3; to = T("b2", "other,") - 0.2; tm = T("b2", "million") - 0.3
    f[700:1500, 480:600] = np.array(C(ASPH), np.float32)
    for y in range(700 + int((t * 300) % 100) - 100, 1500, 100):
        if y > 700: cv2.line(f, (540, y), (540, min(1500, y + 50)), C(LANE), 10, cv2.LINE_AA)
    for side, (x0, el, t0, n_) in enumerate(((70, bank_el("BANK", 100, 92), SHOT["S2b"]["start"] + 0.1, 12), (590, shop_el((255, 90, 120), 100, 100), to, 12))):
        for i in range(n_):
            r, c = divmod(i, 3); tq = t0 + 0.05 * i
            if t >= tq: comp(f, el, x0 + 70 + c * 120, 780 + r * 150, scale=pin(t, tq, 0.25))
    if t >= tb: comp(f, chip("~14,500 BANKS", INK, WHITE, 38), 260, 1400, scale=pin(t, tb, 0.25))
    if t >= tm: comp(f, chip("175M+ STORES", INK, YEL_, 38), 810, 1400, scale=pin(t, tm, 0.25))
    if t >= tm: comp(f, chip("Financial institutions & merchant locations — " + SRC_K[8:], INK, WHITE, 18), 540, 1470, op=clamp((t - tm - 0.3) / 0.3))
    ui_word(f, "banks on one side", "~14,500", 470, t, tb, col=WHITE, size=220, shadow=0.45, lead_col=WHITE, out=tm - 0.05)
    ui_word(f, "stores on the other", "175M+", 470, t, tm, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3: every crossing pays a tiny toll ----
def shot_S3(t, n):
    f = stage("red", (255, 200, 60), 540, 980, 420); u = lt(t, "S3")
    tt = T("b3", "tiny") - 0.25
    road(f, 1260, 1420, t, 300)
    comp(f, tollbooth_el(), 760, 1020, scale=pin(t, SHOT["S3"]["start"] + 0.03, 0.3))
    period = 0.9
    for i in range(6):
        q = u - i * period
        if q < 0: continue
        x = -200 + 900 * q
        if x < 1300: comp(f, scale_el(car_el(((60, 170, 255), (255, 199, 30), (120, 220, 90))[i % 3]), 0.6), x, 1340)
        if 0.75 < q < 1.25: toll_coin(f, t, SHOT["S3"]["start"] + i * period + 0.75, 475, 1260, 760, 1000)
    near = min(abs(u - i * period - 0.8) for i in range(6))
    barrier(f, 640, 1220, 70 if near < 0.25 else 0, 340)
    if t >= tt: comp(f, tag_el("TINY TOLL", YEL_, INK, 60), 330, 930, scale=pin(t, tt, 0.25))
    ui_word(f, "every crossing pays a tiny", "TOLL", 470, t, SHOT["S3"]["start"] + 0.08, col=YEL_, size=230, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S4: multiply — 257.5 billion transactions ----
def shot_S4(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S4")
    tb = T("c1", "billion") - 0.5; tm = T("c1", "multiply.") - 0.2
    k = eo(clamp((t - (tb - 1.4)) / 1.4)) if t >= tb - 1.4 else 0.0
    for i, (x, y, r) in enumerate(((180, 800, -14), (900, 820, 12), (170, 1340, 10), (910, 1330, -10))):
        rot_comp(f, card_el(*(CARD_A if i % 2 else CARD_B), w=280, h=176), x, y + 10 * math.sin(t * 4 + i), r + 6 * math.sin(t * 3 + i), pin(t, SHOT["S4"]["start"] + 0.1 * i, 0.3), 1.0, 0.3)
    odometer(f, 540, 1040, "257.5", k, (130, 190), seed=3)
    comp(f, chip("BILLION TRANSACTIONS", INK, YEL_, 44), 540, 1220, op=clamp((t - tb) / 0.25))
    if t >= tb: comp(f, chip("Total processed transactions, fiscal 2025 — " + SRC_8K[8:], INK, WHITE, 18), 540, 1460, op=clamp((t - tb - 0.3) / 0.3))
    ui_word(f, "now", "MULTIPLY", 470, t, tm, col=INK, size=220, out=tb - 0.05)
    ui_word(f, "transactions last fiscal year", "257.5B", 470, t, tb, col=RED_, size=230)
    return finish(f, n)


# ---- S4b: over 8,000 every second ----
def shot_S4b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S4b")
    te = T("c2", "eight") - 0.2
    rays(f, 540, 1080, 700, (255, 255, 255), 0.35, t)
    beat = int(u * 8)
    for i, (x, y) in enumerate(((250, 1010), (540, 1080), (830, 1010))):
        lit = (beat + i) % 3 == 0
        comp(f, terminal_el(240, 384, "PAID" if lit else "TAP", lit), x, y + (-10 if lit else 0), scale=pin(t, SHOT["S4b"]["start"] + 0.08 * i, 0.25))
        if lit: comp(f, check_el(36, True), x + 80, y - 200)
    if t >= te: comp(f, chip("EVERY 1 SECOND", INK, YEL_, 42), 540, 1340, scale=pin(t, te, 0.25))
    if t >= te: comp(f, chip("257.5B ÷ 31.5M seconds in a year", INK, WHITE, 22), 540, 1450, op=clamp((t - te - 0.3) / 0.3))
    ui_word(f, "swipes & taps, every single second", "8,000+", 470, t, te, col=RED_, size=240)
    return finish(f, n)


# ---- S5: tiny tolls x billions = $40.0B revenue ----
def shot_S5(t, n):
    f = stage("emerald", (255, 214, 90), 540, 1000, 430); u = lt(t, "S5")
    tf = T("c3", "forty") - 0.2
    k = eo(clamp((u - 0.2) / 2.2))
    for i in range(int(2 + 9 * k)):
        r, c = divmod(i, 3)
        rot_comp(f, scale_el(cash_el(), 0.75), 330 + c * 210, 1380 - r * 90, (-4, 3, -2)[c], 1.0, 1.0, 0.3)
    coin_rain(f, t, SHOT["S5"]["start"], 10, 540, 360, 1200, 5)
    if t >= tf:
        rays(f, 540, 1100, 700, (255, 240, 160), 0.4 * clamp((t - tf) / 0.3), t)
        comp(f, chip(SRC_8K, INK, WHITE, 22), 540, 1460, op=clamp((t - tf - 0.3) / 0.3))
    ui_word(f, "tiny tolls x", "BILLIONS", 470, t, SHOT["S5"]["start"] + 0.08, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=tf - 0.05)
    ui_word(f, "revenue, fiscal 2025", "$40.0B", 470, t, tf, col=YEL_, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S6: the twist — ~$20.1B pure profit, half of every dollar ----
def shot_S6(t, n):
    f = stage("purple", (0, 200, 255), 540, 1040, 400); u = lt(t, "S6")
    tp = T("d1", "profit.") - 0.4; th = T("d2", "Half") - 0.2; tc = T("d2", "cheap…") - 0.2
    k = eo(clamp((t - tp) / 0.7)) if t >= tp else 0.0
    ex = 40 * eo(clamp((t - th) / 0.4)) if t >= th else 0.0
    pie(f, 540, 1060, 270, 0.501, GRN_, (230, 232, 240), k, ex, start=-90)
    if k > 0.6: comp(f, chip("PROFIT $20.1B", GRN_, WHITE, 38), 760, 860, scale=pin(t, tp + 0.4, 0.25))
    if t >= th: comp(f, chip("COSTS & TAXES", INK, WHITE, 32), 300, 1290, scale=pin(t, th, 0.25))
    if t >= tc: slam(f, stamp_el("NO LOANS TO LOSE", YEL_, 52), 540, 1385, -6, t, tc)
    if t >= tp: comp(f, chip("Net income $20.1B on net revenue $40.0B — " + SRC_8K[8:], INK, WHITE, 18), 540, 1470, op=clamp((t - tp - 0.3) / 0.3))
    ui_word(f, "and here's the", "CRAZY PART", 470, t, SHOT["S6"]["start"] + 0.1, col=YEL_, size=190, shadow=0.45, lead_col=WHITE, out=tp - 0.05)
    ui_word(f, "pure profit, fiscal 2025", "$20.1B", 470, t, tp, col=YEL_, size=230, shadow=0.45, lead_col=WHITE, out=th - 0.05)
    ui_word(f, "of every dollar is profit", "~50¢", 470, t, th, col=YEL_, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S7: tap your card — you're paying its toll ----
def shot_S7(t, n):
    f = stage("pink", (255, 214, 120), 540, 1000, 430); u = lt(t, "S7")
    ttap = T("e1", "tap") - 0.15; tb = T("e1", "borrowing") - 0.2; tt = T("e1", "toll!") - 0.3
    comp(f, scale_el(tollbooth_el(), 0.7), 860, 1150, scale=pin(t, SHOT["S7"]["start"] + 0.1, 0.3))
    lit = t >= ttap + 0.25
    comp(f, terminal_el(260, 416, "PAID" if lit else "TAP", lit), 560, 1110, scale=pin(t, SHOT["S7"]["start"] + 0.03, 0.3))
    kt = eo(clamp((t - ttap) / 0.3)) if t >= ttap else 0.0
    guy(f, 210, 1500, 0.8, la=(18, 8), ra=(90 - 20 * kt, 70), mouth=talk(t), blink=blink_at(t, 3), brow="up", look=(1, 0),
        expr="smirk" if talk(t) == 0 else "n", hold=scale_el(card_el(*CARD_A, w=200, h=126), 1.0), hold_off=(60 + 120 * kt, -30))
    if lit and t < ttap + 0.8:
        rr = (t - ttap - 0.25) / 0.55; cv2.circle(f, (560, 1000), int(30 + 160 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
    if t >= tt: toll_coin(f, t, tt, 560, 1000, 860, 1000)
    ui_word(f, "next time you tap your card", "REMEMBER", 470, t, SHOT["S7"]["start"] + 0.1, col=WHITE, size=180, shadow=0.45, lead_col=WHITE, out=tb - 0.05)
    ui_word(f, "you're not borrowing from Visa", "NOPE", 470, t, tb, col=WHITE, size=200, shadow=0.45, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "you're paying its", "TOLL", 470, t, tt, col=YEL_, size=250, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S8: send it + brand sting ----
def shot_S8(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S8")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("you pay for gum with a card??", "every tap = a tiny toll lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S8"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(card_el(*CARD_B, w=180, h=114), 1.0), hold_off=(20, -10))
        ui_word(f, "send to the friend who pays for", "EVERYTHING", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=140, shadow=0.3, tail="with a card")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}


IMPACTS = [(T("i1", "never") + 0.1, 0.3, 12), (T("i1", "half") - 0.2, 0.3, 14), (T("i2", "loans.") - 0.15, 0.25, 12),
           (T("i2", "interest.") - 0.15, 0.25, 12), (T("a1", "bank") - 0.2, 0.25, 10), (T("a2", "risk") - 0.05, 0.3, 16),
           (T("b1", "toll") - 0.2, 0.25, 10), (T("b2", "banks.") - 0.3, 0.25, 10), (T("b2", "million") - 0.3, 0.3, 14),
           (T("b3", "tiny") - 0.25, 0.25, 10), (T("c1", "billion") - 0.5, 0.35, 16), (T("c2", "eight") - 0.2, 0.3, 12),
           (T("c3", "forty") - 0.2, 0.35, 16), (T("d1", "profit.") - 0.4, 0.4, 18), (T("d2", "Half") - 0.2, 0.3, 14),
           (T("d2", "cheap…") - 0.2, 0.25, 12), (T("e1", "toll!") - 0.3, 0.35, 16)]


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
