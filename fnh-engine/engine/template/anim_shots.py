# ================= shots: "Starbucks is secretly a bank" =================
def flip_h(el): return el[0][:, ::-1].copy(), el[1][:, ::-1].copy()


SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "That's") - 0.15, "punch"), ("S1", T("i3", "Here's") - 0.15, "whip"),
    ("S2a", T("a1", "Step") - 0.25, "whip"), ("S2b", T("a2", "Twenty-five") - 0.12, "focus"), ("S2c", T("a3", "So") - 0.12, "whip"),
    ("S3a", T("b1", "Step") - 0.25, "whip"), ("S3b", T("b2", "A") - 0.12, "focus"),
    ("S4a", T("c1", "Step") - 0.25, "whip"), ("S4b", T("c2", "Forgotten") - 0.12, "focus"), ("S4c", T("c3", "In") - 0.12, "zoom"),
    ("S4d", T("c4", "And") - 0.12, "whip"), ("S5", T("d1", "Today,") - 0.2, "whip"), ("S6", T("e1", "So") - 0.2, "focus"),
    ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


def title(f, sid, t, n_, big, col=WHITE, size=140):
    ui_word(f, f"STEP {n_}", big, 470, t, SHOT[sid]["start"] + 0.05, col=col, size=size, shadow=0.3, lead_col=WHITE)


def flipx(el, sx):
    sx = max(0.04, abs(sx)); pm, a = el
    w2 = max(2, int(a.shape[1] * sx))
    return cv2.resize(pm, (w2, a.shape[0]), interpolation=cv2.INTER_AREA), cv2.resize(a, (w2, a.shape[0]), interpolation=cv2.INTER_AREA)


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


def vault_cup(f, x, y, s, k_open, t):
    """coffee cup with a vault door; k_open 0..1 swings the door open and money glows inside."""
    comp(f, scale_el(coffee_el(), s), x, y)
    cx, cy, r = x, y + 40 * s, 128 * s
    if k_open > 0:
        cv2.circle(f, (int(cx), int(cy)), int(r * 0.98), C((30, 26, 22)), -1, cv2.LINE_AA)
        glow(f, cx, cy, r * 0.9, (255, 210, 80), 0.9 * k_open)
        for i in range(3):
            comp(f, scale_el(cash_el(), 0.32 * s), cx - 40 * s + 40 * s * i, cy + 30 * s - 18 * s * (i % 2), op=k_open)
    door = scale_el(vault_door_el(), 0.86 * s)
    sx = math.cos(k_open * math.pi * 0.47)
    dw = door[1].shape[1]
    comp(f, flipx(door, sx), cx - dw / 2 + dw * sx / 2 - (1 - sx) * 30 * s, cy)


# ---- S0: hook — the coffee cup is a vault full of your money ----
def shot_S0(t, n):
    f = stage("emerald", GOLD, 540, 1050, 440)
    ko = eo(clamp((t - 0.35) / 0.55))
    vault_cup(f, 540, 1010 + 6 * math.sin(t * 3), 1.15, ko, t)
    steam(f, 540, 640, t, 1.0, 0.5)
    to = T("i1", "one") - 0.15
    if ko > 0.6:
        for i in range(6):
            q = t - 0.75 - i * 0.12
            if q <= 0: continue
            rot_comp(f, scale_el(cash_el(), 0.42), 540 + (-1) ** i * (120 + 50 * i) * min(1, q * 1.6), 1050 - 900 * q + 1100 * q * q, (-1) ** i * 20 * q, 1.0, clamp(2.2 - q), 0.25)
    ui_word(f, "starbucks is sitting on", "$1.7 BILLION", 470, t, to, col=YEL_, size=180, shadow=0.4, lead_col=WHITE)
    ty = T("i1", "your") - 0.1
    if t >= ty:
        comp(f, chip("OF YOUR MONEY", INK, WHITE, 40), 540, 620, scale=pin(t, ty, 0.25))
        guy(f, 175, 1490, 0.8, la=(18, 8), ra=(150, 200), mouth=talk(t), expr="wow" if talk(t) == 0 else "n", brow="up", look=(1, -1),
            bob=-10 * math.exp(-(t - ty) * 4))
    return finish(cam(f, 1.0 + 0.02 * t, W / 2, 1000), n)


# ---- S0b: more than most banks in America have ----
def shot_S0b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 440); u = lt(t, "S0b")
    tb = T("i2", "banks") - 0.15
    m = int(min(10, 2 + u * 9)); rows = (m + 1) // 2
    for i in range(m):
        r_, c_ = divmod(i, 2)
        comp(f, scale_el(cash_el(), 0.55), 720 + (c_ - 0.5) * 150, 1310 - r_ * 70)
    comp(f, scale_el(coffee_el(), 0.55), 720, 1310 - (rows - 1) * 70 - 200)
    for i in range(3):
        if t >= tb + i * 0.1:
            comp(f, scale_el(bank_el(), 0.24), 170 + i * 120, 1300, scale=pin(t, tb + i * 0.1, 0.22))
    ui_word(f, "that's more than", "MOST BANKS", 470, t, T("i2", "more") - 0.12, col=INK, size=180, shadow=0.15, tail="in america have")
    if t >= tb + 0.4: comp(f, chip("FDIC: about 3 in 4 US banks have under $1B in total assets", INK, WHITE, 24), 540, 1430, op=clamp((t - tb - 0.4) / 0.3))
    return finish(f, n)


# ---- S1: how a coffee shop became a bank ----
def shot_S1(t, n):
    f = stage("purple", GOLD, 540, 1000, 440); u = lt(t, "S1")
    tb = T("i3", "became") - 0.2; k = eo(clamp((t - tb) / 0.45))
    if k < 1: comp(f, scale_el(coffee_el(), 1.0 - 0.4 * k), 540, 1030 + 40 * k, op=1 - k)
    if k > 0:
        comp(f, scale_el(bank_el("COFFEE BANK"), 1.0), 540, 1040, scale=0.4 + 0.6 * pin(t, tb, 0.35), op=clamp(k * 2))
        if t < tb + 0.12: f = f + 0.25
    sus = t >= T("i3", "secretly") - 0.1
    guy(f, 870, 1480, 0.78, la=(18, 8), ra=(18, 8), mouth=talk(t), blink=blink_at(t, 2), brow="sus" if sus else "n",
        expr="sus" if (sus and talk(t) == 0) else "n", look=(-1, -1))
    ui_word(f, "how a coffee shop became a", "BANK", 470, t, T("i3", "secretly") - 0.15, col=YEL_, size=220, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S2a: step 1 — load money into the app before you order ----
def shot_S2a(t, n):
    f = stage("teal", (255, 255, 255), 600, 1000, 420); u = lt(t, "S2a")
    title(f, "S2a", t, 1, "LOAD THE APP", WHITE, 160)
    tl = T("a1", "load") - 0.1
    bal = "$25.00" if t >= tl + 0.35 else "$0.00"
    comp(f, scale_el(app_phone_el(bal), 0.86), 630, 1040, scale=pin(t, SHOT["S2a"]["start"] + 0.05, 0.3))
    if tl <= t < tl + 0.6:
        q = (t - tl) / 0.6
        rot_comp(f, scale_el(cash_el(), 0.5), 300 + 330 * q, 1300 - 420 * q, -10, 1.0 - 0.6 * q, 1.0, 0.25)
    if t >= tl + 0.35: comp(f, tag_el("+$25", GRN_, WHITE, 60), 840, 760, scale=pin(t, tl + 0.35, 0.25))
    guy(f, 200, 1480, 0.82, la=(18, 8), ra=(70, 120) if t >= tl else (18, 8), mouth=talk(t), blink=blink_at(t, 3), brow="up", look=(1, 0))
    tb = T("a1", "before") - 0.1
    if t >= tb: rot_comp(f, sign_el("BEFORE YOU ORDER", YEL_, INK, 44, False), 600, 1440, -3, pin(t, tb, 0.25), 1.0, 0.25)
    return finish(f, n)


# ---- S2b: $25 here, $50 there, millions of people ----
def shot_S2b(t, n):
    f = stage("orange", YEL_, 540, 1000, 440); u = lt(t, "S2b")
    t25 = T("a2", "Twenty-five") - 0.1; t50 = T("a2", "Fifty") - 0.1; tm = T("a2", "Millions") - 0.12
    km = clamp((t - tm) / 0.3)
    bal = "$75.00" if t >= t50 + 0.35 else ("$25.00" if t >= t25 + 0.35 else "$0.00")
    comp(f, scale_el(app_phone_el(bal), 0.76), 540, 1050, op=1 - 0.75 * km)
    for tt_, side, lab in ((t25, -1, "+$25"), (t50, 1, "+$50")):
        if t >= tt_:
            q = clamp((t - tt_) / 0.4)
            rot_comp(f, scale_el(cash_el(), 0.48), 540 + side * (380 - 380 * q), 760 + 300 * q, side * 12, 1.0 - 0.5 * q, clamp(1.6 - q), 0.2)
            rot_comp(f, tag_el(lab, GRN_, WHITE, 66), 540 + side * 270, 760, side * 6, pin(t, tt_ + 0.15, 0.25), 1 - km, 0.25)
    if km > 0:
        for j in range(24):
            r_, c_ = divmod(j, 6); x = 540 + (c_ - 2.5) * 135; y = 780 + r_ * 150
            t0 = tm + 0.02 * ((j * 7) % 24)
            if t >= t0: comp(f, mini_head(52, True), x, y, scale=pin(t, t0, 0.2))
    ui_word(f, "of people do it", "MILLIONS", 470, t, tm, col=WHITE, size=200, shadow=0.35, lead_col=WHITE)
    return finish(f, n)


# ---- S2c: split screen — they get cash TODAY, you get coffee LATER ----
def shot_S2c(t, n):
    f = stage("cream", None); u = lt(t, "S2c")
    L_ = np.array(C((10, 120, 84)), np.float32); R_ = np.array(C((255, 112, 40)), np.float32)
    g = (0.85 + 0.25 * (1 - _yy / H))[..., None]
    f[:, :540] = (L_ * g[:, :540]); f[:, 540:] = (R_ * g[:, 540:])
    cv2.line(f, (540, 0), (540, H), (1, 1, 1), 8)
    tt_ = T("a3", "today…") - 0.25; tl = T("a3", "later.") - 0.25
    comp(f, chip("STARBUCKS", INK, WHITE, 34), 270, 700); comp(f, chip("YOU", INK, WHITE, 34), 810, 700)
    comp(f, scale_el(vault_door_el(), 1.0), 270, 1060)
    for i in range(5):
        q = u - 0.25 - 0.18 * i
        if q <= 0: continue
        q = min(q, 0.6) / 0.6
        rot_comp(f, scale_el(cash_el(), 0.5), 270 + (i - 2) * 20, 740 + 320 * q, (-1) ** i * 10, 1.0 - 0.4 * q, clamp(2 - 2 * q), 0.2)
    ui_word(f, "", "TODAY", 560, t, tt_, col=WHITE, size=120, shadow=0.35, x=270, maxw=430)
    kc = clamp((t - tl) / 0.4)
    comp(f, scale_el(coffee_el(), 0.8), 810, 1080, op=0.35 + 0.65 * kc, scale=1 + 0.1 * pin(t, tl, 0.3) * (t >= tl) - 0.1 * (t >= tl))
    ui_word(f, "", "LATER", 560, t, tl, col=WHITE, size=120, shadow=0.35, x=810, maxw=430)
    return finish(f, n)


# ---- S3a: step 2 — a loan with zero interest ----
def shot_S3a(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S3a")
    title(f, "S3a", t, 2, "A FREE LOAN", WHITE, 170)
    rot_comp(f, loan_doc_el(), 540, 1040, -4 + 2 * math.sin(t * 2), pin(t, SHOT["S3a"]["start"] + 0.05, 0.3) * 0.95, 1.0, 0.3)
    tz = T("b1", "zero") - 0.12
    if t >= tz:
        k = clamp((t - tz) / 0.18)
        rot_comp(f, stamp_el("0% INTEREST", RED_, 74), 540, 1110, -12, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.0)
        if t < tz + 0.1: f = f + 0.2
    return finish(f, n)


# ---- S3b: a bank pays you interest, Starbucks pays you nothing ----
def shot_S3b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3b")
    ti = T("b2", "interest") - 0.15; tn = T("b2", "nothing!") - 0.2
    comp(f, scale_el(counter_el("BANK", (60, 110, 220)), 0.82), 300, 1250)
    comp(f, scale_el(counter_el("COFFEE", (30, 160, 110)), 0.82), 780, 1250)
    if t >= ti:
        for i in range(5):
            q = t - ti - i * 0.08
            if q <= 0: continue
            comp(f, coin_el(46, math.cos(q * 7 + i)), 220 + i * 40, 1100 - 260 * min(q, 0.5) - 20 * i, scale=pin(t, ti + i * 0.08, 0.2))
        comp(f, chip("+ INTEREST", GRN_, WHITE, 34), 300, 790, scale=pin(t, ti + 0.2, 0.25))
    if t >= tn:
        rot_comp(f, sign_el("$0", WHITE, RED_, 120, False), 780, 940, 8 * math.sin((t - tn) * 10) * math.exp(-(t - tn) * 3), pin(t, tn, 0.25), 1.0, 0.3)
    ui_word(f, "a bank pays you", "INTEREST", 470, t, T("b2", "bank") - 0.1, col=INK, size=170, shadow=0.1, out=T("b2", "Starbucks") - 0.1)
    ui_word(f, "starbucks pays you", "NOTHING", 470, t, T("b2", "Starbucks") - 0.08, col=RED_, size=190, shadow=0.1)
    return finish(f, n)


# ---- S4a: step 3 — some money is never spent ----
def shot_S4a(t, n):
    f = stage("purple", (255, 120, 190), 540, 1000, 430); u = lt(t, "S4a")
    title(f, "S4a", t, 3, "NEVER SPENT", WHITE, 170)
    tn = T("c1", "never") - 0.15; kd = clamp((t - tn) / 0.8)
    rot_comp(f, giftcard_el(), 540, 1040 + 10 * math.sin(t * 2), -8 + 3 * math.sin(t * 1.5), 1.25 * pin(t, SHOT["S4a"]["start"] + 0.05, 0.3), 1.0, 0.3)
    if kd > 0:
        f[...] = f * (1 - 0.25 * kd) + np.array(C((60, 50, 80)), np.float32) * 0.25 * kd
        for i in range(30):
            ph = (u * 0.15 + i / 30) % 1
            x = 300 + (i * 97) % 480; y = 1300 - ph * 600
            cv2.circle(f, (int(x), int(y)), 3 + (i % 3), C((240, 230, 255)), -1, cv2.LINE_AA)
    return finish(f, n)


# ---- S4b: forgotten gift cards, a few dollars left in the app ----
def shot_S4b(t, n):
    f = stage("teal", (255, 255, 255), 540, 1020, 440); u = lt(t, "S4b")
    comp(f, scale_el(drawer_el(), 0.95), 520, 1150, scale=pin(t, SHOT["S4b"]["start"], 0.3))
    tf_ = T("c2", "few") - 0.15
    if t >= tf_: rot_comp(f, scale_el(app_phone_el("$3.47"), 0.5), 790, 840, 8, pin(t, tf_, 0.25), 1.0, 0.3)
    ui_word(f, "gift cards & app balances", "FORGOTTEN", 470, t, T("c2", "Forgotten") - 0.1, col=WHITE, size=170, shadow=0.35)
    return finish(f, n)


# ---- S4c: over $200 million in one year ----
def shot_S4c(t, n):
    f = stage("emerald", GOLD, 540, 1040, 430); u = lt(t, "S4c")
    tt_ = T("c3", "two") - 0.15
    m = int(clamp(u / 2.4) * 18)
    for i in range(m):
        r_, c_ = divmod(i, 3); x = 540 + (c_ - 1) * 190 + (r_ % 2) * 20; y = 1330 - r_ * 72
        comp(f, scale_el(cash_el(), 0.55), x, y)
    if t >= tt_: rays(f, 540, 1040, 640, (255, 236, 150), 0.4 * clamp((t - tt_) / 0.3), t)
    ui_word(f, "in one year:", "$200 MILLION+", 470, t, tt_, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    if t >= tt_ + 0.5: comp(f, chip("Starbucks FY2025: $222M recognized from unspent card balances", INK, WHITE, 24), 540, 1440, op=clamp((t - tt_ - 0.5) / 0.3))
    return finish(f, n)


# ---- S4d: counted as revenue — no coffee needed ----
def shot_S4d(t, n):
    f = stage("orange", (255, 214, 120), 540, 1000, 430); u = lt(t, "S4d")
    tr = T("c4", "revenue…") - 0.2; tn = T("c4", "no") - 0.12
    cv2.rectangle(f, (300, 980), (780, 1330), C((40, 40, 52)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (290, 960), (790, 1000), C((70, 70, 84)), -1, cv2.LINE_AA)
    comp(f, sign_el("REVENUE", WHITE, INK, 60, False), 540, 1170)
    for i in range(4):
        q = u - 0.2 - i * 0.22
        if q <= 0 or q > 0.6: continue
        rot_comp(f, scale_el(cash_el(), 0.4), 540 + (i - 1.5) * 60, 650 + 330 * (q / 0.6), (-1) ** i * 12, 1.0, 1.0, 0.2)
    if t >= tn:
        comp(f, scale_el(coffee_el(), 0.42), 860, 1260, op=0.9)
        comp(f, check_el(56, False), 880, 1170, scale=pin(t, tn, 0.25))
    ui_word(f, "counted as", "REVENUE", 470, t, tr, col=WHITE, size=190, shadow=0.35, out=tn - 0.05)
    ui_word(f, "", "NO COFFEE NEEDED", 470, t, tn, col=WHITE, size=140, shadow=0.35)
    return finish(f, n)


# ---- S5: 4 in 10 orders paid with a Starbucks card ----
def shot_S5(t, n):
    f = stage("pink", (255, 255, 255), 540, 1020, 440); u = lt(t, "S5")
    tf_ = T("d1", "four") - 0.15
    for j in range(10):
        r_, c_ = divmod(j, 5); x = 260 + c_ * 140; y = 950 + r_ * 250
        lit = j in (0, 3, 6, 9) and t >= tf_ + 0.08 * (j % 4)
        comp(f, scale_el(coffee_el(), 0.36), x, y, scale=pin(t, SHOT["S5"]["start"] + 0.03 * j, 0.2), op=1.0 if (lit or t < tf_) else 0.55)
        if lit: rot_comp(f, scale_el(giftcard_el(), 0.3), x + 30, y + 70, -10, pin(t, tf_ + 0.08 * (j % 4), 0.2), 1.0, 0.2)
    ui_word(f, "today,", "4 IN 10 ORDERS", 470, t, tf_, col=WHITE, size=150, shadow=0.35, tail="paid with a starbucks card")
    if t >= tf_ + 0.6: comp(f, chip("Starbucks Q3 FY2026: 42% of US store transactions", INK, WHITE, 26), 540, 1440, op=clamp((t - tf_ - 0.6) / 0.3))
    return finish(f, n)


# ---- S6: you're funding a bank ----
def shot_S6(t, n):
    f = stage("purple", GOLD, 540, 1000, 440); u = lt(t, "S6")
    tf_ = T("e1", "funding") - 0.2; k = eo(clamp((t - tf_) / 0.45))
    tap = t >= T("e1", "top") - 0.1
    guy(f, 230, 1480, 0.86, la=(18, 8), ra=(70, 110) if tap else (18, 8), mouth=talk(t), blink=blink_at(t, 5), brow="up", look=(1, 0),
        hold=scale_el(app_phone_el("$50.00"), 0.24), hold_off=(40, -40))
    if k < 1: comp(f, scale_el(coffee_el(), 0.85), 680, 1040, op=1 - k)
    if k > 0:
        comp(f, scale_el(bank_el("COFFEE BANK"), 0.78), 680, 1060, scale=0.5 + 0.5 * pin(t, tf_, 0.35), op=clamp(k * 2))
        for i in range(4):
            q = (t - tf_ - i * 0.2) % 0.8
            if t - tf_ - i * 0.2 < 0: continue
            rot_comp(f, scale_el(cash_el(), 0.3), 330 + 300 * q / 0.8, 1100 - 120 * math.sin(math.pi * q / 0.8), 0, 1.0, 1.0, 0.2)
    ui_word(f, "you're not just buying coffee", "", 470, t, T("e1", "remember…") - 0.1, col=WHITE, out=tf_ - 0.08)
    ui_word(f, "you're", "FUNDING A BANK", 470, t, tf_, col=YEL_, size=160, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("emerald", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("starbucks run?", "already loaded $50 lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(coffee_el(), 0.22), hold_off=(20, -40))
        ui_word(f, "send this to the friend who", "LIVES AT STARBUCKS", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=100, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(0.62, 0.3, 10), (T("i1", "one") - 0.15, 0.25, 10), (T("i2", "banks") - 0.15, 0.25, 8), (T("i3", "became") - 0.2, 0.3, 12),
           (T("b1", "zero") - 0.12 + 0.18, 0.35, 18), (T("b2", "nothing!") - 0.2, 0.3, 14), (T("c3", "two") - 0.15, 0.3, 10),
           (T("c4", "no") - 0.12, 0.25, 10), (T("e1", "funding") - 0.2, 0.3, 12)]


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
