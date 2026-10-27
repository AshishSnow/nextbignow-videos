# ================= shots: "Your gas station barely makes money on gas" =================
# Sources: Casey's Q4 + fiscal 2026 results (SEC 8-K, Jun 9 2026): 2,944 stores, fuel margin 42.6c/gal excl. card fees, fuel sales $10.62B,
#          inside sales $6.34B, fuel gross profit $1.50B, inside gross profit $2.68B, inside margin 42.2%, prepared food & dispensed bev. margin 58.6%.
#          NACS State of the Industry (Apr 2026): fuel = 65.0% of 2025 sales dollars but 38.8% of gross profit dollars.
#          Fortune (Aug 29 2026): Casey's = 5th-largest US pizza chain by prepared food & beverage sales (BofA Research; confirmed by Casey's).
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Casey's,") - 0.2, "punch"), ("S1b", T("i2", "earns") - 0.15, "whip"),
    ("S2", T("a1", "Fill") - 0.2, "focus"), ("S3", T("a2", "So") - 0.2, "whip"), ("S4", T("a3", "Last") - 0.2, "zoom"),
    ("S5", T("a4", "But") - 0.2, "flash"), ("S6", T("b1", "Here's") - 0.2, "whip"), ("S7", T("b2", "Inside") - 0.2, "punch"),
    ("S8", T("b3", "And") - 0.2, "zoom"), ("S9", T("c1", "That's") - 0.2, "flash"), ("S10", T("c2", "But") - 0.2, "focus"),
    ("S11", T("c3", "Cheap") - 0.2, "whip"), ("S11b", T("c3", "The") - 0.12, "punch"), ("S12", T("d1", "Across") - 0.2, "zoom"),
    ("S13", T("d2", "So") - 0.2, "whip"), ("S13b", T("d2", "Every") - 0.15, "focus"), ("S14", T("e1", "Your") - 0.2, "whip"),
    ("S14b", T("e1", "It's") - 0.12, "punch"), ("S15", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_C = "Source: Casey's Q4 & fiscal 2026 results (SEC 8-K, Jun 2026)"
SRC_N = "Source: NACS State of the Industry report (Apr 2026)"
SRC_F = "Source: Fortune (Aug 2026), citing BofA Research"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, out=None, col=YEL_, size=220, tail="", y=470):
    ui_word(f, lead, big, y, t, t0, col=col, size=size, shadow=0.45, lead_col=WHITE, out=out, tail=tail)


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


def src(f, text, t, t0, y=1452, size=20):
    if t >= t0: comp(f, chip(text, INK, WHITE, size), 540, y, op=clamp((t - t0) / 0.3))


def ground(f, y, col=(70, 72, 84)):
    f[y:] = f[y:] * 0.35 + np.array(C(col), np.float32) * 0.65
    cv2.line(f, (0, y), (W, y), C(INK), 6, cv2.LINE_AA)


# ---- S0: hook — giant price sign, pump running, the station keeps pennies (frame 1 = the loop-back frame) ----
def shot_S0(t, n):
    f = stage("purple", (255, 150, 60), 540, 960, 470)
    tm = T("i1", "money…") - 0.15
    ground(f, 1460)
    rot_comp(f, price_sign_el(), 320, 1130, 0, 0.92 + 0.01 * t, 1.0, 0.35)
    kk = clamp((t + 1.2) / 4.0)
    comp(f, pump_el(amt=f"{46.65 * kk:.2f}", gal=f"{15.0 * kk:.3f}"), 770, 1150)
    guy(f, 600, 1470, 0.62, la=(30, 20), ra=(70, 20), mouth=talk(t), blink=blink_at(t, 1), brow="sus" if t >= tm else "up",
        look=(1, -1), expr="sus" if (t >= tm and talk(t) == 0) else "n", hold=scale_el(nozzle_el(), 0.6), hold_off=(40, -10))
    if t >= tm:
        q = t - tm; y = 760 + 420 * eo(clamp(q / 0.7))
        rot_comp(f, coin_el(40, abs(math.cos(q * 6))), 770, y, 0, 1.0, 1.0 - clamp((q - 1.4) / 0.3), 0.3)
        comp(f, tag_el("PENNIES?", YEL_, INK, 52), 780, 740, scale=pin(t, tm + 0.1, 0.25))
    wui(f, "your gas station barely makes money on", "GAS", t, -0.5, col=YEL_, size=260)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1100), n)


# ---- S1: Casey's — almost 3,000 stations ----
def shot_S1(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 440); u = lt(t, "S1")
    for i in range(16):
        r, c = divmod(i, 4); x = 210 + c * 220; y = 700 + r * 160
        tq = st_("S1") + 0.06 * i
        if t >= tq: comp(f, scale_el(store_el(), 0.24), x, y, scale=pin(t, tq, 0.2))
    if u > 0.8: comp(f, chip("2,944 STORES (APR 30, 2026)", INK, YEL_, 40), 540, 1380, scale=pin(t, st_("S1") + 0.8, 0.25))
    wui(f, "one chain, almost", "3,000 STATIONS", t, st_("S1") + 0.06, col=WHITE, size=170)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1000), n)


# ---- S1b: about 43 cents on a gallon ----
def shot_S1b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S1b")
    tf = T("i2", "forty") - 0.25
    rot_comp(f, gas_can_el(), 330, 1060 + 6 * math.sin(t * 4), -6, pin(t, st_("S1b") + 0.03, 0.3), 1.0, 0.3)
    if t >= tf:
        rays(f, 740, 1060, 520, (255, 255, 230), 0.35 * clamp((t - tf) / 0.3), t)
        rot_comp(f, coin_el(110, 1.0), 740, 1060, 0, pin(t, tf, 0.3), 1.0, 0.35)
        comp(f, ed_el("", "43¢", "", big_col=INK, big_size=96, maxw=200), 740, 1056, scale=pin(t, tf, 0.3))
        comp(f, chip("42.6¢ PER GALLON, BEFORE CARD FEES", RED_, WHITE, 36), 540, 1330, scale=pin(t, tf + 0.3, 0.25))
        src(f, SRC_C, t, tf + 0.5)
        ui_word(f, "earned on one gallon of gas", "≈ 43¢", 470, t, tf, col=RED_, size=250)
    else:
        ui_word(f, "on one gallon, it earns…", "?", 470, t, st_("S1b") + 0.06, col=INK, size=250)
    return finish(f, n)


# ---- S2: fill a 15-gallon tank = about $6 ----
def shot_S2(t, n):
    f = stage("teal", (255, 214, 120), 540, 980, 420); u = lt(t, "S2")
    ts = T("a1", "six") - 0.25
    k = clamp(u / 0.8)
    rows = [("FILL-UP", "15 GAL", False), ("× 42.6¢", "per gal", False)]
    if t >= ts: rows.append(("STATION", "≈ $6.39", True))
    pm, a = receipt_el(tuple(rows), h=420)
    hh = int(a.shape[0] * eo(k))
    if hh > 4: comp(f, (pm[:hh], a[:hh]), 630, 720 + hh * 1.2 / 2, scale=1.2)
    if t >= ts: slam(f, stamp_el("ABOUT $6", RED_, 80), 620, 1330, -10, t, ts)
    guy(f, 190, 1490, 0.6, la=(30, 20), ra=(60, 30), mouth=talk(t), blink=blink_at(t, 3), brow="up", look=(1, -1),
        expr="wow" if t >= ts and talk(t) == 0 else "n")
    if t >= ts: wui(f, "a full tank earns the station", "$6", t, ts, size=250)
    else: wui(f, "fill a", "15 GALLONS", t, st_("S2") + 0.06, col=WHITE, size=200)
    return finish(f, n)


# ---- S3: so where's the real money? look past the pump ----
def shot_S3(t, n):
    f = stage("orange", (255, 230, 140), 540, 1000, 430); u = lt(t, "S3")
    tl = T("a2", "Look") - 0.15
    ground(f, 1400, (90, 70, 60))
    comp(f, scale_el(pump_el(), 0.7), 220, 1170)
    so = clamp((t - tl) / 0.5) if t >= tl else 0.0
    if so > 0: rays(f, 720, 1120, 620, (255, 250, 210), 0.4 * so, t)
    comp(f, scale_el(store_el(door_open=so), 0.6), 720, 1235)
    w_ = walk(t, 1.0); x = 330 + 140 * eo(clamp(u / 1.6))
    guy(f, x, 1480, 0.62, la=w_["la"], ra=(80, 40), ll=w_["ll"], rl=w_["rl"], bob=w_["bob"], mouth=talk(t), blink=blink_at(t, 2),
        brow="sus", look=(1, 0), expr="sus" if talk(t) == 0 else "n", hold=scale_el(magnifier_el(), 0.4), hold_off=(40, -40))
    if t < tl: wui(f, "so where's the", "REAL MONEY?", t, st_("S3") + 0.06, col=WHITE, size=190)
    else: wui(f, "look past the", "PUMP", t, tl, size=250)
    return finish(f, n)


# ---- S4: $10.6B of gas vs $6.3B inside ----
def shot_S4(t, n):
    f = stage("cream", (255, 214, 90), 540, 1000, 440); u = lt(t, "S4")
    tt = T("a3", "ten") - 0.25; ti = T("a3", "inside") - 0.5
    base = 1330
    kg = clamp((t - tt) / 0.7) if t >= tt else 0.0; ks = clamp((t - ti) / 0.7) if t >= ti else 0.0
    bars(f, 330, base, 240, 440, PUMP_R, kg, "GAS SALES", "$10.6B")
    bars(f, 750, base, 240, 261, GRN_, ks, "INSIDE SALES", "$6.3B")
    comp(f, scale_el(pump_el(), 0.24), 322, base - 100)
    comp(f, scale_el(store_el(), 0.27), 750, base - 100)
    src(f, "Fiscal year ended Apr 30, 2026 — " + SRC_C[8:], t, tt + 0.5, y=1462, size=19)
    ui_word(f, "last year, Casey's sold", "GAS vs STORE", 470, t, st_("S4") + 0.06, col=INK, size=170)
    return finish(f, n)


# ---- S5: but the store made almost twice the profit ----
def shot_S5(t, n):
    f = stage("emerald", (0, 220, 160), 540, 1000, 430); u = lt(t, "S5")
    tw = T("a4", "twice") - 0.25
    base = 1250; k = clamp(u / 1.4)
    cash_pile(f, 300, base, 9, k, 0.95)
    cash_pile(f, 760, base, 16, k, 0.95)
    comp(f, chip("GAS  $1.50B", PUMP_R, WHITE, 44), 300, 1360)
    comp(f, chip("STORE  $2.68B", GRN_, WHITE, 44), 780, 1360)
    if t >= tw:
        rays(f, 780, 1050, 600, (255, 255, 200), 0.3 * clamp((t - tw) / 0.3), t)
        slam(f, stamp_el("ALMOST 2x", YEL_, 76), 600, 760, -8, t, tw)
    src(f, "Gross profit, fiscal 2026 — " + SRC_C[8:], t, st_("S5") + 0.6, y=1450, size=19)
    if t >= tw: wui(f, "but the store made", "2x THE PROFIT", t, tw, size=180)
    else: wui(f, "but the", "STORE…", t, st_("S5") + 0.06, col=WHITE, size=220)
    return finish(f, n)


# ---- S6-S8: cents kept per dollar — a scoreboard of three coins ----
COINS = ((0.141, PUMP_R, "14¢", "GAS"), (0.422, GRN_, "42¢", "STORE"), (0.586, (255, 140, 0), "59¢", "FOOD"))


def coin_row(f, upto, y=1330):
    for i in range(upto):
        x = (200, 400)[i]
        pie_coin(f, x, y, 80, COINS[i][0], COINS[i][1], COINS[i][2], 1.0)
        comp(f, chip(COINS[i][3], INK, WHITE, 26), x, y + 110)


def shot_S6(t, n):
    f = stage("red", (255, 200, 60), 540, 980, 420); u = lt(t, "S6")
    tf = T("b1", "fourteen") - 0.25
    comp(f, scale_el(pump_el(), 0.55), 220, 1040 + 6 * math.sin(t * 3))
    if t < tf - 0.2: pie_coin(f, 640, 1020, 230, 0.0, PUMP_R, "?", clamp((t - st_("S6")) / 0.5))
    else: pie_coin(f, 640, 1020, 230, 0.141, PUMP_R, "14¢", 0.7 + 0.3 * clamp((t - tf + 0.2) / 0.5))
    if t >= tf:
        src(f, "Fuel: $1.50B gross profit on $10.62B sales — Casey's FY2026 (SEC 8-K)", t, tf + 0.4, y=1400, size=19)
        wui(f, "kept from every gas dollar", "14¢", t, tf, size=250)
    else: wui(f, "here's", "WHY", t, st_("S6") + 0.06, col=WHITE, size=260)
    return finish(f, n)


def shot_S7(t, n):
    f = stage("emerald", (255, 230, 120), 540, 980, 420); u = lt(t, "S7")
    tf = T("b2", "Forty") - 0.25
    comp(f, scale_el(store_el(), 0.5), 690, 860, scale=pin(t, st_("S7") + 0.02, 0.3))
    pie_coin(f, 690, 1150, 160, 0.422, GRN_, "42¢", clamp((t - tf) / 0.5) if t >= tf else 0.0)
    coin_row(f, 1)
    if t >= tf:
        src(f, "Inside margin 42.2% — Casey's fiscal 2026 (SEC 8-K)", t, tf + 0.4, y=1480, size=20)
        wui(f, "inside the store?", "42¢", t, tf, size=250)
    else: wui(f, "inside the", "STORE?", t, st_("S7") + 0.06, col=WHITE, size=230)
    return finish(f, n)


def shot_S8(t, n):
    f = stage("yellow", (255, 255, 255), 540, 980, 430); u = lt(t, "S8")
    tp = T("b3", "pizza") - 0.2; tc = T("b3", "fountain") - 0.2; tf = T("b3", "fifty") - 0.25
    if t < tf:
        if t >= tp: rot_comp(f, pizza_el(200), 560, 960, 20 * u, pin(t, tp, 0.3), 1.0, 0.3)
        if t >= tc: rot_comp(f, fountain_cup_el(), 830, 1080, 6, pin(t, tc, 0.3), 1.0, 0.3)
        ui_word(f, "and on fresh food…", "PIZZA", 470, t, st_("S8") + 0.06, col=INK, size=220)
    else:
        rays(f, 690, 1060, 700, (255, 255, 230), 0.4 * clamp((t - tf) / 0.3), t)
        pie_coin(f, 690, 1060, 200, 0.586, (255, 140, 0), "59¢", clamp((t - tf) / 0.5))
        rot_comp(f, scale_el(slice_el(), 0.8), 600, 790, -18, pin(t, tf + 0.2, 0.25), 1.0, 0.3)
        rot_comp(f, scale_el(fountain_cup_el(), 0.6), 860, 800, 12, pin(t, tf + 0.3, 0.25), 1.0, 0.3)
        src(f, "Food & fountain margin 58.6% — Casey's fiscal 2026 (SEC 8-K)", t, tf + 0.4, y=1480, size=20)
        ui_word(f, "fresh food & fountain drinks", "59¢", 470, t, tf, col=RED_, size=250)
    coin_row(f, 2)
    return finish(f, n)


# ---- S9: America's 5th-biggest pizza chain ----
def shot_S9(t, n):
    f = stage("purple", (255, 200, 60), 540, 1000, 430); u = lt(t, "S9")
    t5 = T("c1", "fifth") - 0.25
    for i in range(5):
        y = 700 + i * 140; tq = st_("S9") + 0.15 + 0.12 * i
        if t < tq: continue
        hl = i == 4; on = hl and t >= t5
        sh = int(8 * math.sin((t - t5) * 40) * math.exp(-max(0, t - t5) * 5)) if on else 0
        x0, x1 = 150, 930; col = YEL_ if on else (255, 255, 255)
        cv2.rectangle(f, (x0 + 10 + sh, y - 52 + 10), (x1 + 10 + sh, y + 52 + 10), (0, 0, 0), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x0 + sh, y - 52), (x1 + sh, y + 52), C(col), -1, cv2.LINE_AA)
        cv2.rectangle(f, (x0 + sh, y - 52), (x1 + sh, y + 52), C(INK), 6, cv2.LINE_AA)
        comp(f, ed_el("", f"#{i + 1}", "", big_col=RED_, big_size=66, maxw=140), x0 + 80 + sh, y)
        lab = "PIZZA CHAIN" if not hl else ("A GAS STATION!" if on else "???")
        comp(f, ed_el("", lab, "", big_col=INK, big_size=54, maxw=520), 520 + sh, y)
        if on: comp(f, scale_el(pump_el(), 0.15), 870 + sh, y)
        elif not hl: comp(f, scale_el(slice_el(), 0.34), 870, y)
    if t >= t5:
        src(f, SRC_F, t, t5 + 0.4, y=1440)
        wui(f, "a gas station chain became the", "#5 PIZZA CHAIN", t, t5, size=170)
    else: wui(f, "that's how", "PIZZA WON", t, st_("S9") + 0.06, col=WHITE, size=200)
    return finish(f, n)


# ---- S10: re-hook — the sneakiest part: curtains open on the giant price sign ----
def shot_S10(t, n):
    f = stage("teal", (255, 230, 140), 540, 980, 470); u = lt(t, "S10")
    tg = T("c2", "giant") - 0.2
    ok = clamp((t - tg) / 0.7) if t >= tg else 0.0
    if ok > 0: rays(f, 540, 980, 760, (255, 250, 200), 0.45 * ok, t)
    ground(f, 1460)
    rot_comp(f, price_sign_el(), 540, 1110, 0, 0.86 + 0.06 * eo(ok), 1.0, 0.35)
    curtain(f, ok)
    if ok < 0.3: comp(f, ed_el("", "?", "", big_col=YEL_, big_size=420, maxw=400, shadow=0.4), 540, 1040 + 10 * math.sin(t * 6), op=1 - ok / 0.3)
    if t < tg: wui(f, "but the sneakiest part?", "WAIT…", t, st_("S10") + 0.06, col=WHITE, size=220)
    else: wui(f, "the giant", "PRICE SIGN", t, tg, size=200)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1000), n)


# ---- S11: cheap gas pulls you in (car on the road turns toward the sign) ----
def shot_S11(t, n):
    f = stage("sky", (255, 230, 120), 760, 820, 300); u = lt(t, "S11")
    ti = T("c3", "in.") - 0.3
    cv2.rectangle(f, (0, 1200), (W, 1360), C(ROAD), -1); cv2.line(f, (0, 1200), (W, 1200), C(INK), 6); cv2.line(f, (0, 1360), (W, 1360), C(INK), 6)
    for x in range(-160, W + 320, 160):
        xx = int((x - u * 400) % (W + 320)) - 160
        cv2.rectangle(f, (xx, 1274), (xx + 80, 1286), C((250, 250, 240)), -1)
    for j in range(3):
        rr = 90 + ((t * 1.4 + j / 3) % 1) * 230
        cv2.circle(f, (760, 860), int(rr), C((255, 255, 255)), 4, cv2.LINE_AA)
    rot_comp(f, scale_el(price_sign_el(("2.99", "3.19", "3.39")), 0.6), 760, 900, 0, 1.0, 1.0, 0.3)
    x = 230 + 330 * eo(clamp(u / 1.2)); y = 1250 - (70 * eo(clamp((t - ti) / 0.5)) if t >= ti else 0)
    rot_comp(f, scale_el(car_el(), 0.7), x, y, 6 * clamp((t - ti) / 0.3) if t >= ti else 0, 1.0, 1.0, 0.3)
    wui(f, "cheap gas", "PULLS YOU IN", t, st_("S11") + 0.06, col=WHITE, size=180)
    return finish(f, n)


# ---- S11b: the snacks do the rest ----
def shot_S11b(t, n):
    f = stage("pink", (255, 214, 120), 540, 980, 430); u = lt(t, "S11b")
    ground(f, 1300, (90, 70, 80))
    comp(f, scale_el(store_el(), 0.7), 540, 1110)
    guy(f, 540, 1470, 0.78, la=(120, 60), ra=(120, 60), mouth=talk(t), blink=blink_at(t, 5), brow="up", look=(0, 0), expr="smirk" if talk(t) == 0 else "n")
    items = ((chips_el((255, 170, 30)), -120, -40, -14), (fountain_cup_el(), 0, -110, 4), (slice_el(), 120, -40, 16),
             (chips_el((120, 80, 230), label="CANDY"), 60, 40, -8), (coffee_el(), -60, 40, 6))
    sc_ = (0.6, 0.55, 0.5, 0.55, 0.22)
    for i, (el, dx, dy, r) in enumerate(items):
        tq = st_("S11b") + 0.12 + 0.18 * i
        if t >= tq: rot_comp(f, scale_el(el, sc_[i]), 540 + dx, 1290 + dy * 0.6 - 40 * (1 - eo(clamp((t - tq) / 0.25))), r, pin(t, tq, 0.25), 1.0, 0.25)
    wui(f, "then the snacks", "DO THE REST", t, st_("S11b") + 0.06, col=YEL_, size=190)
    return finish(f, n)


# ---- S12: the whole industry — share of sales vs share of profit ----
def shot_S12(t, n):
    f = stage("cream", (255, 214, 90), 540, 1000, 440); u = lt(t, "S12")
    ts = T("d1", "industry") - 0.1; t6 = T("d1", "sixty") - 0.3; tu = T("d1", "under") - 0.25
    top = 700; hh = 560
    stack_bar(f, 330, top, 250, hh, 0.65, clamp((t - ts) / 0.7) if t >= ts else 0.0, PUMP_R, GRN_, "65%", "35%", "SALES")
    stack_bar(f, 750, top, 250, hh, 0.388, clamp((t - tu) / 0.7) if t >= tu else 0.0, PUMP_R, GRN_, "39%", "61%", "PROFIT")
    comp(f, chip("GAS", PUMP_R, WHITE, 34), 440, 1390); comp(f, chip("STORE", GRN_, WHITE, 34), 640, 1390)
    src(f, "Gross profit, all US convenience stores, 2025 — " + SRC_N[8:], t, ts + 0.4, y=1460, size=18)
    if t < t6: ui_word(f, "and it's not just one chain", "THE WHOLE INDUSTRY", 470, t, st_("S12") + 0.06, col=INK, size=130)
    elif t < tu: ui_word(f, "all US convenience stores, 2025", "GAS = 65% OF SALES", 470, t, t6, col=INK, size=120)
    else: ui_word(f, "but of the profit, gas is", "UNDER 40%", 470, t, tu, col=RED_, size=170)
    return finish(f, n)


# ---- S13: takeaway — only need gas? pay at the pump ----
def shot_S13(t, n):
    f = stage("emerald", (255, 230, 120), 540, 1000, 430); u = lt(t, "S13")
    tp = T("d2", "pay") - 0.2
    ground(f, 1470)
    cin = clamp((t - tp) / 0.5) if t >= tp else 0.0
    comp(f, pump_el(card=cin >= 1.0), 640, 1130)
    if 0 < cin < 1.0: rot_comp(f, scale_el(pay_card_el(), 0.5), 640, 1000 + 180 * eo(cin), 0, 1.0, 1.0, 0.2)
    if cin >= 1.0: comp(f, check_el(60, True), 860, 760, scale=pin(t, tp + 0.55, 0.25))
    guy(f, 250, 1470, 0.7, la=(30, 20), ra=(70, 50), mouth=talk(t), blink=blink_at(t, 6), brow="up", look=(1, 0), expr="smirk" if talk(t) == 0 else "n",
        hold=scale_el(pay_card_el(), 0.35) if cin == 0 else None, hold_off=(30, -10))
    wui(f, "only need gas?", "PAY AT THE PUMP", t, st_("S13") + 0.06, col=YEL_, size=160)
    return finish(f, n)


def shot_S13b(t, n):
    f = stage("purple", (255, 200, 60), 540, 980, 430); u = lt(t, "S13b")
    store_map(f, 540, 1010, clamp(u / 2.2), t)
    wui(f, "every step inside is", "THE PLAN", t, st_("S13b") + 0.06, col=YEL_, size=170, y=400)
    return finish(f, n)


# ---- S14: your gas station isn't a gas station... it's a snack shop with a giant price sign (loops to frame 1) ----
def shot_S14(t, n):
    f = stage("orange", (255, 230, 140), 540, 1000, 430); u = lt(t, "S14")
    ground(f, 1420, (90, 70, 60))
    comp(f, scale_el(store_el(awning="GAS?"), 0.86), 540, 1180, scale=pin(t, st_("S14") + 0.03, 0.3))
    wui(f, "your gas station isn't really a", "GAS STATION", t, st_("S14") + 0.06, col=WHITE, size=170)
    return finish(f, n)


def shot_S14b(t, n):
    tg = T("e1", "giant") - 0.2
    if t < tg:
        f = stage("orange", (255, 230, 140), 540, 1000, 430)
        ground(f, 1420, (90, 70, 60))
        rays(f, 540, 1000, 700, (255, 250, 200), 0.35, t)
        comp(f, scale_el(store_el(awning="SNACK SHOP"), 0.86), 540, 1180, scale=pin(t, st_("S14b") - 0.15, 0.3))
        wui(f, "it's a", "SNACK SHOP", t, st_("S14b") + 0.06, size=210)
        return finish(f, n)
    # ...with a giant price sign: same composition as frame 1 -> seamless rewatch loop
    f = stage("purple", (255, 150, 60), 540, 960, 470)
    k = eo(clamp((t - tg) / 0.5))
    ground(f, 1460)
    rot_comp(f, price_sign_el(), 320, 1130 + 500 * (1 - k), 0, 0.92, 1.0, 0.35)
    comp(f, pump_el(amt="0.00", gal="0.000"), 770, 1150)
    wui(f, "…with a giant", "PRICE SIGN", t, tg, size=200)
    return finish(f, n)


# ---- S15: send it + brand sting ----
def shot_S15(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S15")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("why do you ALWAYS buy snacks", "it's literally the business model", pr), 0.82), 600, 950, scale=pin(t, st_("S15")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(chips_el(), 0.7), hold_off=(20, -30))
        ui_word(f, "send to the friend who never skips", "THE SNACKS", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=140, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "money…") - 0.15, 0.25, 10), (T("i1", "gas?") - 0.2, 0.3, 12), (T("i2", "forty") - 0.25, 0.35, 16),
           (T("a1", "six") - 0.25, 0.35, 16), (T("a3", "ten") - 0.25, 0.25, 10), (T("a4", "twice") - 0.25, 0.4, 18),
           (T("b1", "fourteen") - 0.25, 0.3, 12), (T("b2", "Forty") - 0.25, 0.3, 14), (T("b3", "fifty") - 0.25, 0.35, 16),
           (T("c1", "fifth") - 0.25, 0.35, 16), (T("c2", "giant") - 0.2, 0.35, 14), (T("d1", "under") - 0.25, 0.3, 14),
           (T("d2", "pay") + 0.3, 0.2, 8), (T("e1", "snack") - 0.2, 0.3, 12), (T("e1", "giant") - 0.2, 0.3, 12)]


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
