# ================= shots: "Your airline's real money machine is your credit card" =================
# Sources: Delta Q4 + full-year 2025 results (SEC 8-K, Jan 13 2026): Amex remuneration $8.2B (+11%), operating income $5.8B.
#          American Airlines Q4 + full-year 2025 results (SEC 8-K, Jan 2026): revenue $54.6B (record), net income $111M,
#          loyalty program liabilities $3,725M current + $6,839M noncurrent = $10.6B.
#          American Airlines FY2025 10-K: cash payments from co-branded credit card and other partners $6.2B (2025);
#          may "change the terms of the AAdvantage program at any time and without notice".
#          United 8-K (Jun 15 2020): MileagePlus valuation ~ $21.9B (12x 2019 EBITDA); Kirkland & Ellis (Jul 2020): $6.8B financing secured by MileagePlus.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "That's") - 0.2, "punch"), ("S2", T("a1", "Now") - 0.2, "whip"), ("S2b", T("a1", "Five") - 0.15, "punch"),
    ("S3", T("a2", "The") - 0.2, "focus"), ("S4", T("a3", "And") - 0.2, "whip"), ("S5", T("b1", "American") - 0.2, "zoom"),
    ("S6", T("b2", "It") - 0.2, "whip"), ("S7", T("b3", "But") - 0.2, "flash"), ("S8", T("c1", "So") - 0.2, "focus"),
    ("S8b", T("c1", "Your") - 0.15, "punch"), ("S9", T("c2", "Every") - 0.2, "whip"), ("S9b", T("c2", "That's") - 0.15, "zoom"),
    ("S10", T("c3", "You") - 0.2, "whip"), ("S10b", T("c3", "The") - 0.15, "punch"), ("S10c", T("c3", "And") - 0.15, "whip"),
    ("S11", T("d1", "But") - 0.2, "flash"), ("S12", T("d2", "Planes") - 0.2, "focus"), ("S12b", T("d2", "So") - 0.15, "whip"),
    ("S12c", T("d2", "and") - 0.1, "punch"), ("S13", T("d3", "United") - 0.2, "zoom"), ("S14", T("t1", "Here's") - 0.2, "whip"),
    ("S14b", T("t1", "The") - 0.15, "focus"), ("S14c", T("t1", "and") - 0.1, "punch"), ("S15", T("t2", "American") - 0.2, "zoom"),
    ("S16", T("t3", "So") - 0.2, "whip"), ("S16b", T("t3", "Earn") - 0.15, "punch"), ("S17", T("e1", "Because") - 0.2, "focus"),
    ("S17b", T("e1", "It's") - 0.15, "punch"), ("S18", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_D = "Source: Delta full-year 2025 results (SEC 8-K, Jan 2026)"
SRC_A = "Source: American Airlines 2025 results (SEC 8-K, Jan 2026)"
SRC_U = "Sources: United SEC 8-K (Jun 2020), Kirkland & Ellis (Jul 2020)"


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


def clouds(f, t, y0=760, sp=40, op=0.8):
    for i, (x, y, s) in enumerate(((180, y0, 1.0), (760, y0 + 260, 0.8), (420, y0 + 640, 1.2), (900, y0 + 760, 0.7))):
        xx = (x - sp * t * s) % 1400 - 180
        for dx, dy, r in ((0, 0, 60), (55, -22, 70), (115, 0, 55)):
            cv2.circle(f, (int(xx + dx * s), int(y + dy * s)), int(r * s), (op, op, op), -1, cv2.LINE_AA)


def _bez(p0, p1, u, bend):
    mx, my = (p0[0] + p1[0]) / 2 - bend * (p1[1] - p0[1]), (p0[1] + p1[1]) / 2 + bend * (p1[0] - p0[0])
    return (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0], (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1]


def along(p0, p1, u, bend=0.0): return _bez(p0, p1, u, bend)


def arrow(f, p0, p1, k, col=INK, th=12, bend=0.0):
    """animated curved arrow drawn k = 0..1"""
    if k <= 0.01: return
    n_ = 40; pts = [_bez(p0, p1, i / n_, bend) for i in range(int(n_ * k) + 1)]
    cv2.polylines(f, [np.array(pts, np.int32)], False, C(col), th, cv2.LINE_AA)
    if k > 0.95 and len(pts) > 2:
        (x0, y0), (x1, y1) = pts[-3], pts[-1]; a = math.atan2(y1 - y0, x1 - x0)
        tri = np.array([[x1 + 30 * math.cos(a), y1 + 30 * math.sin(a)], [x1 + 26 * math.cos(a + 2.3), y1 + 26 * math.sin(a + 2.3)],
                        [x1 + 26 * math.cos(a - 2.3), y1 + 26 * math.sin(a - 2.3)]], np.int32)
        cv2.fillPoly(f, [tri], C(col), cv2.LINE_AA)


def dial(f, cx, cy, r, v, lab="VALUE"):
    """semicircle gauge; v = 0..1 needle position (1 = high)"""
    cv2.ellipse(f, (cx, cy), (r + 16, r + 16), 0, 180, 360, C(INK), -1, cv2.LINE_AA)
    for i, col in enumerate(((232, 28, 36), (255, 199, 30), (22, 170, 76))):
        cv2.ellipse(f, (cx, cy), (r, r), 0, 180 + 60 * i, 240 + 60 * i, C(col), -1, cv2.LINE_AA)
    cv2.ellipse(f, (cx, cy), (int(r * 0.55), int(r * 0.55)), 0, 180, 360, C(INK), -1, cv2.LINE_AA)
    a = math.pi * (1 - v)
    cv2.line(f, (cx, cy), (int(cx + r * 0.92 * math.cos(a)), int(cy - r * 0.92 * math.sin(a))), C(WHITE), 14, cv2.LINE_AA)
    cv2.circle(f, (cx, cy), 26, C(WHITE), -1, cv2.LINE_AA)
    comp(f, chip(lab, INK, WHITE, 34), cx, cy + 60)


# ---- the hook composition (frame 1 and the loop-back frame): a giant card pumping cash into a jet ----
def hook_set(f, t, flow=1.0):
    clouds(f, t, 700, 50, 0.92)
    py = 960 + 8 * math.sin(t * 2.2)
    rot_comp(f, plane_el(820, tail=(232, 60, 40)), 560, py, 4, 1.0, 1.0, 0.35)
    cx, cy = 300, 1320
    for j in range(6):   # cash bundles stream from the card up into the plane's belly
        u = ((t * 0.55 + j / 6) % 1.0); x, y = along((cx + 60, cy - 90), (600, py + 40), u, 0.25)
        op = clamp(u / 0.15) * clamp((1 - u) / 0.2) * flow
        rot_comp(f, scale_el(cash_el(1), 0.55), x, y, -20 + 40 * u, 1.0, op, 0.0)
    rot_comp(f, card_el(520, foil=round((t * 0.4) % 1.3, 2)), cx + 40, cy, 14, 1.0, 1.0, 0.4)


def shot_S0(t, n):
    f = stage("sky", (255, 236, 150), 760, 760, 300)
    te = T("i1", "eight") - 0.2
    if t >= te: rays(f, 600, 1000, 640, (255, 255, 220), 0.35 * clamp((t - te) / 0.3), t)
    hook_set(f, t)
    if t >= te: slam(f, stamp_el("$8,000,000,000", RED_, 62), 700, 1330, -8, t, te)
    wui(f, "why would a credit card pay an airline", "$8 BILLION?", t, -0.5, col=YEL_, size=230)
    return finish(cam(f, 1.0 + 0.01 * t, W / 2, 1050), n)


# ---- S1: Amex -> Delta, the cheque ----
def shot_S1(t, n):
    f = stage("emerald", (255, 240, 170), 540, 1050, 440); u = lt(t, "S1")
    k = eo(clamp(u / 0.5))
    rot_comp(f, cheque_el("AMERICAN EXPRESS", "DELTA", "$8.2 BILLION", "Eight point two billion dollars", "full year 2025"), 540 + 700 * (1 - k), 1060, -4, 1.0, 1.0, 0.35)
    td = T("i2", "Delta") - 0.1
    if t >= td: slam(f, stamp_el("PAID", RED_, 90), 760, 1260, -14, t, td)
    src(f, SRC_D, t, st_("S1") + 0.6)
    wui(f, "American Express paid Delta", "$8.2B", t, st_("S1") + 0.06, size=250, tail="in 2025")
    return finish(f, n)


# ---- S2: Delta's entire profit? bars: card deal vs profit ----
def shot_S2(t, n):
    f = stage("sky", (255, 240, 170), 540, 1000, 440); u = lt(t, "S2")
    base = 1360
    bars(f, 330, base, 250, 620, (150, 110, 230), clamp(u / 0.6), "CARD DEAL", "$8.2B")
    rot_comp(f, plane_el(300, tail=(232, 60, 40)), 610 + 220 * clamp(u / 3.0), 700 - 30 * clamp(u / 3.0), 5, 1.0, 1.0, 0.25)
    bars(f, 750, base, 250, 438, RED_, 0.04, "DELTA PROFIT", "")
    comp(f, ed_el("", "?", "", big_col=RED_, big_size=200), 750, 1180 - 14 * abs(math.sin(t * 5)), scale=pin(t, st_("S2") + 0.4, 0.3))
    wui(f, "now look at Delta's", "ENTIRE PROFIT", t, st_("S2") + 0.06, col=WHITE, size=180)
    return finish(f, n)


def shot_S2b(t, n):
    f = stage("sky", (255, 240, 170), 540, 1000, 440); u = lt(t, "S2b")
    base = 1360
    bars(f, 330, base, 250, 620, (150, 110, 230), 1.0, "CARD DEAL", "$8.2B")
    bars(f, 750, base, 250, 438, RED_, 0.04 + 0.96 * clamp(u / 0.8), "DELTA PROFIT", "$5.8B" if u > 0.5 else "")
    src(f, "Operating income 2025 — Delta results (SEC 8-K, Jan 2026)", t, st_("S2b") + 0.5, y=1460, size=19)
    wui(f, "Delta's whole operating profit", "$5.8B", t, st_("S2b") + 0.04, size=250)
    return finish(cam(f, 1.0 + 0.015 * u, W / 2, 1100), n)


# ---- S3: the balance tips — the card deal outweighs the airline's profit ----
def shot_S3(t, n):
    f = stage("purple", (120, 80, 255), 540, 1000, 460); u = lt(t, "S3")
    tb = T("a2", "bigger") - 0.2
    tilt = 13 * eback(clamp((t - tb) / 0.6)) if t >= tb else 2 * math.sin(u * 5) * (1 - clamp(u / 1.0))
    left = scale_el(card_el(520), 0.5); right = scale_el(cash_el(3), 0.6)
    balance(f, 540, 760, tilt, left, right, t)
    comp(f, chip("CARD DEAL $8.2B", (120, 60, 220), WHITE, 34), 250, 1430)
    comp(f, chip("PROFIT $5.8B", RED_, WHITE, 34), 830, 1430)
    if t >= tb + 0.4: slam(f, stamp_el("BIGGER", YEL_, 80), 540, 1250, -6, t, tb + 0.4)
    tw = T("a2", "whole") - 0.15
    if t < tw: wui(f, "the card deal was", "BIGGER…", t, st_("S3") + 0.06, size=230)
    else: wui(f, "than the whole airline's", "PROFIT", t, tw, size=230)
    return finish(f, n)


# ---- S4: Delta isn't the only one — a fleet of generic jets ----
def shot_S4(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 380); u = lt(t, "S4")
    clouds(f, t, 760, 60, 0.95)
    for i, (tail, x, y) in enumerate((((232, 60, 40), 400, 820), ((40, 90, 220), 660, 1060), ((20, 160, 120), 420, 1300))):
        k = eo(clamp((u - 0.15 * i) / 0.5))
        rot_comp(f, plane_el(560, tail=tail), x + 700 * (1 - k), y + 6 * math.sin(t * 2 + i), 3, 1.0, k, 0.3)
    wui(f, "and Delta isn't the", "ONLY ONE", t, st_("S4") + 0.06, col=WHITE, size=210)
    return finish(f, n)


# ---- S5: American Airlines, record $54.6B ----
def shot_S5(t, n):
    f = stage("teal", (255, 214, 120), 540, 1000, 430); u = lt(t, "S5")
    clouds(f, t, 700, 70, 0.9)
    rot_comp(f, plane_el(560, tail=(40, 90, 220)), 260 + 520 * eio(clamp(u / 5.0)), 820 - 60 * eio(clamp(u / 5.0)), 6, 1.0, 1.0, 0.3)
    tf = T("b1", "fifty") - 0.25
    odometer(f, 540, 1130, "$54.6B", clamp((t - tf) / 1.0) if t >= tf else 0.0, cell=(118, 170), col=YEL_)
    if t >= tf + 0.6: comp(f, chip("RECORD REVENUE, 2025", INK, YEL_, 40), 540, 1320, scale=pin(t, tf + 0.6, 0.25))
    src(f, SRC_A, t, tf + 0.6)
    wui(f, "American Airlines brought in a", "RECORD", t, st_("S5") + 0.06, col=WHITE, size=220)
    return finish(cam(f, 1.0 + 0.008 * u, W / 2, 1100), n)


# ---- S6: ...and kept just $111M (the profit bar is a sliver) ----
def shot_S6(t, n):
    f = stage("orange", (255, 230, 140), 540, 1000, 440); u = lt(t, "S6")
    base = 1360; tm = T("b2", "million") - 0.3
    bars(f, 330, base, 250, 600, (40, 150, 255), 1.0, "SALES", "$54.6B")
    bars(f, 750, base, 250, 3, GRN_, 1.0, "PROFIT", "")
    if t >= tm:
        k = pin(t, tm, 0.35)
        cv2.circle(f, (750, base - 4), max(1, int(70 * k)), C(RED_), 8, cv2.LINE_AA)
        comp(f, tag_el("$111M", GRN_, WHITE, 70), 750, 1000, scale=k)
        comp(f, chip("= 0.2% OF SALES", INK, WHITE, 34), 750, 1110, op=clamp((t - tm - 0.4) / 0.3))
        src(f, "Net income 2025 — American Airlines results (SEC 8-K)", t, tm + 0.4, y=1460, size=19)
        wui(f, "kept as profit, just", "$111M", t, tm, col=WHITE, size=250)
    else: wui(f, "and it kept", "JUST…", t, st_("S6") + 0.06, col=WHITE, size=230)
    return finish(f, n)


# ---- S7: but card companies & partners paid it $6.2B — 56x its profit ----
def shot_S7(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 440); u = lt(t, "S7")
    base = 1360; ts = T("b3", "six") - 0.25
    bars(f, 330, base, 250, 11, GRN_, 1.0, "PROFIT", "$0.1B")
    kb = 0.25 * eo(clamp(u / 1.5)) + (0.75 * clamp((t - ts) / 0.7) if t >= ts else 0.0)
    bars(f, 750, base, 250, 520, (120, 60, 220), kb, "CARD PARTNERS", "$6.2B" if t >= ts + 0.4 else "")
    rot_comp(f, card_el(220), 510, 1150 + 6 * math.sin(t * 4), -8, 1.0, 1.0, 0.3)
    if t >= ts:
        slam(f, stamp_el("56x THE PROFIT", RED_, 56), 430, 900, -10, t, ts + 0.9)
        src(f, "Cash from co-brand cards & partners — AA 2025 10-K", t, ts + 0.5, y=1460, size=19)
        wui(f, "card companies & partners paid", "$6.2B", t, ts, col=WHITE, size=250)
    else: wui(f, "but card companies", "PAID IT…", t, st_("S7") + 0.06, col=WHITE, size=200)
    return finish(f, n)


# ---- S8: so what are they really paying for? ----
def shot_S8(t, n):
    f = stage("orange", (255, 230, 140), 540, 1000, 430); u = lt(t, "S8")
    rot_comp(f, card_el(520), 680, 1060 + 8 * math.sin(t * 3), -10, 0.9, 1.0, 0.35)
    guy(f, 300, 1480, 0.7, la=(30, 20), ra=(80, 40), mouth=talk(t), blink=blink_at(t, 2), brow="sus", look=(1, -1),
        expr="sus" if talk(t) == 0 else "n", hold=scale_el(magnifier_el(), 0.45), hold_off=(40, -40))
    comp(f, ed_el("", "?", "", big_col=WHITE, big_size=160, shadow=0.4), 800, 780, scale=pin(t, st_("S8") + 0.6, 0.3))
    wui(f, "so what are they really", "PAYING FOR?", t, st_("S8") + 0.06, col=WHITE, size=190)
    return finish(f, n)


def shot_S8b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 420); u = lt(t, "S8b")
    rays(f, 540, 1080, 700, (255, 255, 230), 0.35, t)
    rnd = np.random.default_rng(7)
    for i in range(16):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(200, 380) * eo(clamp(u / 0.6)); rr = int(rnd.choice([40, 50, 60]))
        x, y = 540 + r * math.cos(a), 1100 + r * math.sin(a) * 0.9
        comp(f, mile_el(rr), x, y + 10 * math.sin(t * 3 + i), op=clamp(u / 0.3))
    comp(f, mile_el(150), 540, 1100, scale=pin(t, st_("S8b"), 0.35))
    wui(f, "", "YOUR MILES", t, st_("S8b") + 0.03, size=240)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1080), n)


# ---- S9: the money map — you swipe, the bank pays the airline, miles come back ----
P_YOU, P_BANK, P_AIR = (300, 1340), (790, 1030), (330, 780)


def money_map(f, t, sw, pay, back):
    rot_comp(f, plane_el(420, tail=(232, 60, 40)), P_AIR[0] + 20, P_AIR[1] + 6 * math.sin(t * 2), 3, 1.0, 1.0, 0.3)
    comp(f, scale_el(bank_el("BANK"), 0.48), P_BANK[0], P_BANK[1])
    ok = t >= sw + 0.3
    comp(f, terminal_el(170, "APPROVED" if ok else "TAP", ok), P_YOU[0] + 170, P_YOU[1] - 90)
    guy(f, P_YOU[0] - 80, 1500, 0.55, la=(30, 20), ra=(100, 60), mouth=talk(t), blink=blink_at(t, 4), brow="up", look=(1, -1),
        expr="n", hold=scale_el(card_el(300), 0.5), hold_off=(50, -30))
    if t >= sw:
        k = clamp((t - sw - 0.2) / 0.6); arrow(f, (P_YOU[0] + 270, P_YOU[1] - 170), (P_BANK[0] - 120, P_BANK[1] + 100), k, INK, 12, 0.15)
        comp(f, chip("YOU SPEND", INK, WHITE, 30), 560, 1350, op=k)
    if t >= pay:
        k = clamp((t - pay) / 0.6); arrow(f, (P_BANK[0] - 40, P_BANK[1] - 150), (P_AIR[0] + 220, P_AIR[1] + 30), k, GRN_, 14, 0.2)
        for j in range(4):
            u = ((t - pay) * 0.7 + j / 4) % 1.0
            if t - pay > 0.5:
                x, y = along((P_BANK[0] - 40, P_BANK[1] - 150), (P_AIR[0] + 220, P_AIR[1] + 30), u, 0.2)
                rot_comp(f, scale_el(cash_el(1), 0.4), x, y, 0, 1.0, clamp(u / 0.15) * clamp((1 - u) / 0.2), 0.0)
        comp(f, chip("BANK PAYS $", GRN_, WHITE, 32), 760, 780, op=k)
    if back is not None and t >= back:
        k = clamp((t - back) / 0.6); arrow(f, (P_AIR[0] - 140, P_AIR[1] + 120), (P_YOU[0] - 120, P_YOU[1] - 330), k, MILEB, 14, 0.25)
        for j in range(4):
            u = ((t - back) * 0.7 + j / 4) % 1.0
            if t - back > 0.5:
                x, y = along((P_AIR[0] - 140, P_AIR[1] + 120), (P_YOU[0] - 120, P_YOU[1] - 330), u, 0.25)
                comp(f, mile_el(34), x, y, op=clamp(u / 0.15) * clamp((1 - u) / 0.2))
        comp(f, chip("MILES", MILEB, WHITE, 32), 160, 1000, op=k)


def shot_S9(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1050, 420)
    tp = T("c2", "pays") - 0.1
    money_map(f, t, T("c2", "swipe") - 0.1, tp, None)
    if t < tp: wui(f, "every time you", "SWIPE", t, st_("S9") + 0.06, col=WHITE, size=240)
    else: wui(f, "the bank", "PAYS THE AIRLINE", t, tp, col=WHITE, size=150)
    return finish(f, n)


def shot_S9b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1050, 420)
    money_map(f, t, -9, -9, st_("S9b") + 0.1)
    wui(f, "that's where your", "MILES COME FROM", t, st_("S9b") + 0.04, col=WHITE, size=140)
    return finish(f, n)


# ---- S10: three winners — you feel rewarded / the bank gets your spending / the airline gets paid for a number ----
def shot_S10(t, n):
    f = stage("pink", (255, 230, 120), 540, 1050, 430); u = lt(t, "S10")
    for i in range(14):
        x = 540 + 360 * math.sin(i * 2.1); y = 700 + ((u * 300 + i * 97) % 760)
        cv2.rectangle(f, (int(x), int(y)), (int(x + 22), int(y + 12)), C(((255, 199, 30), (60, 140, 240), (232, 28, 36))[i % 3]), -1, cv2.LINE_AA)
    guy(f, 540, 1480, 0.85, la=(150, 160 + 12 * math.sin(t * 9)), ra=(150, 160 + 12 * math.cos(t * 9)), mouth=2, blink=blink_at(t, 1), brow="up", expr="wow")
    for j, (x, y) in enumerate(((300, 900), (780, 930), (540, 760))):
        comp(f, mile_el(54), x, y + 10 * math.sin(t * 4 + j), scale=pin(t, st_("S10") + 0.15 * j, 0.25))
    wui(f, "you feel", "REWARDED", t, st_("S10") + 0.06, col=WHITE, size=230)
    return finish(f, n)


def shot_S10b(t, n):
    f = stage("teal", (255, 255, 255), 540, 1050, 420); u = lt(t, "S10b")
    comp(f, scale_el(bank_el("BANK"), 0.8), 540, 1120, scale=pin(t, st_("S10b"), 0.3))
    for j in range(5):
        q = (u * 0.9 + j / 5) % 1.0; x = 170 + 370 * q; y = 900 - 120 * math.sin(q * math.pi)
        rot_comp(f, scale_el(cash_el(1), 0.45), x, y, 20, 1.0, clamp(q / 0.15) * clamp((1 - q) / 0.25), 0.0)
    comp(f, chip("EVERY SWIPE RUNS THROUGH ITS CARD", INK, WHITE, 30), 540, 1440, op=clamp(u / 0.4))
    wui(f, "the bank gets your", "SPENDING", t, st_("S10b") + 0.04, col=WHITE, size=230)
    return finish(f, n)


def shot_S10c(t, n):
    f = stage("red", (255, 200, 60), 540, 1050, 430); u = lt(t, "S10c")
    ta = T("c3", "adds") - 0.15; tn = T("c3", "number") - 0.2
    rot_comp(f, plane_el(460, tail=(255, 199, 30)), 330, 790 + 6 * math.sin(t * 2), 3, 1.0, 1.0, 0.3)
    for j in range(3):
        q = (u * 0.8 + j / 3) % 1.0; x, y = along((880, 700), (440, 780), q, -0.2)
        rot_comp(f, scale_el(cash_el(1), 0.4), x, y, 0, 1.0, clamp(q / 0.15) * clamp((1 - q) / 0.2), 0.0)
    cv2.rectangle(f, (170, 1010), (910, 1270), C(INK), -1, cv2.LINE_AA)
    comp(f, ed_el("YOUR ACCOUNT · MILES", "", "", lead_col=WHITE, lead_size=36), 540, 1050)
    odometer(f, 540, 1175, "25,000" if t >= ta else "00,000", clamp((t - ta) / 0.8) if t >= ta else 1.0, cell=(80, 120), col=(120, 190, 255))
    if t >= ta: comp(f, chip("+25,000 MILES", MILEB, WHITE, 40), 540, 1350, scale=pin(t, ta + 0.5, 0.25))
    if t >= tn: wui(f, "the airline gets paid for", "A NUMBER", t, tn, size=230)
    else: wui(f, "and the airline", "GETS PAID…", t, st_("S10c") + 0.04, col=WHITE, size=200)
    return finish(f, n)


# ---- S11: re-hook — departures board flips to 2020 ----
def shot_S11(t, n):
    f = stage("purple", (255, 140, 60), 540, 1000, 440); u = lt(t, "S11")
    comp(f, chip("DEPARTURES", YEL_, INK, 44), 540, 830)
    flapboard(f, 540, 1010, "PROOF", t, st_("S11") + 0.1, cell=(120, 170))
    tt = T("d1", "twenty") - 0.3
    flapboard(f, 540, 1250, "2020", t, tt, cell=(120, 170), col=(255, 255, 255))
    if t >= tt: wui(f, "but the wildest proof came in", "2020", t, tt, col=YEL_, size=240)
    else: wui(f, "but the", "WILDEST PROOF", t, st_("S11") + 0.06, col=WHITE, size=180)
    return finish(f, n)


# ---- S12: planes parked ----
def shot_S12(t, n):
    f = stage("purple", (90, 60, 160), 540, 900, 380); u = lt(t, "S12")
    runway(f, 1300)
    for i, (x, y, s) in enumerate(((330, 1050, 0.5), (760, 1100, 0.5), (520, 1230, 0.62))):
        comp(f, plane_el(int(820 * s), tail=(150, 150, 160), grey=0.6, gear=True), x, y)
    tp = T("d2", "parked") - 0.2
    if t >= tp: slam(f, stamp_el("PARKED", RED_, 90), 540, 880, -8, t, tp)
    wui(f, "planes were", "PARKED", t, st_("S12") + 0.06, col=WHITE, size=240)
    return finish(f, n)


# ---- S12b/c: United borrows $6.8B against its miles chest, which gets chained ----
def shot_S12b(t, n):
    f = stage("teal", (255, 230, 140), 540, 1050, 440); u = lt(t, "S12b")
    ts = T("d2", "six") - 0.25
    comp(f, chest_el(440, open_=1.0), 680, 1130)
    comp(f, chip("MILES PROGRAM", MILEB, WHITE, 36), 680, 1400)
    comp(f, scale_el(bank_el("LENDERS"), 0.42), 260, 880)
    if t >= ts:
        cash_pile(f, 260, 1330, 7, clamp((t - ts) / 0.9), 0.6)
        comp(f, tag_el("$6.8B", GRN_, WHITE, 76), 260, 1100, scale=pin(t, ts + 0.3, 0.3))
        src(f, SRC_U, t, ts + 0.5, y=1470, size=19)
        wui(f, "United borrowed", "$6.8B", t, ts, size=250)
    else: wui(f, "so United", "BORROWED", t, st_("S12b") + 0.04, col=WHITE, size=220)
    return finish(f, n)


def shot_S12c(t, n):
    f = stage("red", (255, 200, 60), 540, 1050, 440); u = lt(t, "S12c")
    tsec = T("d2", "security") - 0.2
    kc = clamp(u / max(0.3, tsec - st_("S12c")))
    comp(f, chest_el(460, open_=round(1.0 - clamp(u / 0.4), 2), chained=1.0 if t >= tsec else round(0.98 * kc, 2)), 540, 1130)
    comp(f, chip("MILES PROGRAM", MILEB, WHITE, 36), 540, 1420)
    if t >= tsec: slam(f, stamp_el("COLLATERAL", RED_, 70), 540, 850, -8, t, tsec)
    wui(f, "and put up its miles as", "SECURITY", t, st_("S12c") + 0.04, size=230)
    return finish(f, n)


# ---- S13: United valued those miles at ~$22B ----
def shot_S13(t, n):
    f = stage("emerald", (255, 240, 150), 540, 1100, 450); u = lt(t, "S13")
    tt = T("d3", "twenty") - 0.25
    rays(f, 540, 1150, 700, (255, 255, 220), 0.3, t)
    comp(f, chest_el(460, open_=1.0), 540, 1150, scale=1.0 + 0.02 * u)
    if t >= tt:
        slam(f, tag_el("≈ $22 BILLION", RED_, WHITE, 70), 560, 880, -6, t, tt)
        src(f, "≈ 12x 2019 earnings (EBITDA) — United SEC 8-K, Jun 2020", t, tt + 0.5, y=1460, size=19)
        wui(f, "United itself valued its miles at", "≈ $22B", t, tt, size=250)
    else: wui(f, "United itself", "VALUED THEM…", t, st_("S13") + 0.06, col=WHITE, size=190)
    return finish(f, n)


# ---- S14: here's the catch for you ----
def shot_S14(t, n):
    f = stage("red", (255, 200, 60), 540, 1000, 430); u = lt(t, "S14")
    rot_comp(f, sign_el("THE CATCH", YEL_, INK, 90), 640, 1150, -4, pin(t, st_("S14") + 0.1, 0.3), 1.0, 0.3)
    guy(f, 250, 1480, 0.7, la=(30, 20), ra=(110, 60), mouth=talk(t), blink=blink_at(t, 3), brow="sus", look=(1, -1), expr="sus" if talk(t) == 0 else "n")
    wui(f, "here's the catch", "FOR YOU", t, st_("S14") + 0.06, col=WHITE, size=230)
    return finish(f, n)


def shot_S14b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 420); u = lt(t, "S14b")
    tw = T("t1", "worth") - 0.2
    v = 0.8 - 0.55 * eo(clamp((t - tw) / 0.8)) if t >= tw else 0.8 + 0.05 * math.sin(t * 3)
    dial(f, 540, 1290, 280, v, "VALUE OF 1 MILE")
    comp(f, mile_el(110), 540, 840 + 8 * math.sin(t * 3), scale=pin(t, st_("S14b"), 0.3))
    comp(f, chip("SET BY THE AIRLINE", INK, YEL_, 34), 540, 990, op=clamp((u - 0.4) / 0.3))
    wui(f, "the airline decides what a", "MILE IS WORTH", t, st_("S14b") + 0.04, col=WHITE, size=150)
    return finish(f, n)


def shot_S14c(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1050, 420); u = lt(t, "S14c")
    ta = T("t1", "any") - 0.2
    rot_comp(f, rulebook_el(560, round((u * 1.6) % 1.0, 2)), 540, 1060, -3, 1.0, 1.0, 0.3)
    if t >= ta: slam(f, stamp_el("SUBJECT TO CHANGE", RED_, 52), 540, 1100, -10, t, ta)
    src(f, '"...at any time and without notice" — American Airlines 10-K', t, st_("S14c") + 0.4, y=1400, size=20)
    wui(f, "and it can change the rules", "ANY TIME", t, st_("S14c") + 0.04, col=INK, size=230)
    return finish(f, n)


# ---- S15: $10.6B of miles not used yet ----
def shot_S15(t, n):
    f = stage("purple", (90, 160, 255), 540, 1050, 430); u = lt(t, "S15")
    rnd = np.random.default_rng(3); k = clamp(u / 1.6)
    for i in range(int(66 * k)):
        row = int((math.sqrt(8 * i + 1) - 1) / 2); col = i - row * (row + 1) // 2
        x = 540 + (col - row / 2) * 66 + rnd.uniform(-6, 6); y = 760 + row * 50 + rnd.uniform(-4, 4)
        comp(f, mile_el(38), x, y)
    tt = T("t2", "ten") - 0.25
    if t >= tt:
        comp(f, chip("$10.6B OF MILES NOT USED YET", YEL_, INK, 40), 540, 1380, scale=pin(t, tt, 0.3))
        src(f, "Loyalty liabilities, end of 2025 — AA results (SEC 8-K)", t, tt + 0.5, y=1470, size=19)
        wui(f, "American alone is holding", "$10.6B", t, tt, size=250, tail="in unused miles")
    else: wui(f, "American", "ALONE", t, st_("S15") + 0.06, col=WHITE, size=240)
    return finish(f, n)


# ---- S16: treat miles like cash that can shrink ----
def shot_S16(t, n):
    f = stage("teal", (200, 240, 255), 540, 1050, 420); u = lt(t, "S16")
    tsh = T("t3", "shrink") - 0.2
    s = 1.0 - 0.45 * eo(clamp((t - tsh) / 1.0)) if t >= tsh else 1.0
    cv2.ellipse(f, (540, 1340), (int(260 * (1.6 - s)), int(40 * (1.6 - s))), 0, 0, 360, C((150, 200, 255)), -1, cv2.LINE_AA)
    comp(f, mile_el(220), 540, 1340 - 230 * s, scale=s)
    if t >= tsh:
        for j in range(3): cv2.circle(f, (int(420 + 120 * j), int(1180 + ((t * 300 + j * 80) % 140))), 12, C((150, 200, 255)), -1, cv2.LINE_AA)
        wui(f, "treat miles like cash that can", "SHRINK", t, tsh, size=250)
    else: wui(f, "treat miles", "LIKE CASH", t, st_("S16") + 0.06, col=WHITE, size=230)
    return finish(f, n)


def shot_S16b(t, n):
    f = stage("emerald", (255, 240, 150), 540, 1050, 430)
    items = (("EARN", True, T("t3", "Earn") - 0.1), ("USE", True, T("t3", "use") - 0.1), ("HOARD", False, T("t3", "hoard") - 0.15))
    for i, (lab, ok, t0) in enumerate(items):
        if t < t0: continue
        y = 800 + i * 200; k = pin(t, t0, 0.3)
        comp(f, chip(lab, INK if ok else RED_, WHITE, 80), 440, y, scale=k)
        comp(f, check_el(56, ok), 740, y, scale=k)
    wui(f, "the takeaway", "USE THEM", t, st_("S16b") + 0.04, size=240)
    return finish(f, n)


# ---- S17: the most valuable thing you carry isn't your suitcase... ----
def shot_S17(t, n):
    f = stage("orange", (255, 230, 140), 540, 1050, 430); u = lt(t, "S17")
    ti = T("e1", "isn't") - 0.1
    rot_comp(f, suitcase_el(440), 540, 1130, -3, pin(t, st_("S17") + 0.05, 0.3), 1.0, 0.35)
    if t >= ti:
        k = clamp((t - ti) / 0.3); k2 = clamp((t - ti - 0.3) / 0.3)
        cv2.line(f, (330, 900), (int(330 + 420 * k), int(900 + 460 * k)), C(RED_), 30, cv2.LINE_AA)
        if k2 > 0: cv2.line(f, (750, 900), (int(750 - 420 * k2), int(900 + 460 * k2)), C(RED_), 30, cv2.LINE_AA)
    wui(f, "the most valuable thing you carry isn't your", "SUITCASE", t, st_("S17") + 0.06, col=WHITE, size=200)
    return finish(f, n)


# ---- S17b: ...it's the card in your wallet (exact frame-1 composition = seamless loop) ----
def shot_S17b(t, n):
    f = stage("sky", (255, 236, 150), 760, 760, 300)
    hook_set(f, t)
    wui(f, "it's the card in your", "WALLET", t, st_("S17b") + 0.04, size=240)
    return finish(cam(f, 1.0 + 0.01 * (t - st_("S17b")), W / 2, 1050), n)


# ---- S18: send it + brand sting ----
def shot_S18(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S18")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("how many miles do you have saved up?", "spend them before the rules change", pr), 0.82), 600, 950, scale=pin(t, st_("S18")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(card_el(300), 0.6), hold_off=(20, -30))
        ui_word(f, "send to the friend saving miles for", "10 YEARS", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=150, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "eight") - 0.2, 0.35, 16), (T("i2", "Delta") - 0.1, 0.3, 12), (T("a1", "Five") - 0.15, 0.3, 12),
           (T("a2", "bigger") - 0.2 + 0.4, 0.35, 16), (T("b1", "fifty") - 0.25, 0.25, 10), (T("b2", "million") - 0.3, 0.3, 12),
           (T("b3", "six") - 0.25 + 0.9, 0.35, 16), (T("c1", "Your") - 0.15, 0.3, 12), (T("c2", "swipe") - 0.1, 0.2, 8),
           (T("d1", "twenty") - 0.3, 0.3, 12), (T("d2", "parked") - 0.2, 0.35, 16), (T("d2", "security") - 0.2, 0.35, 16),
           (T("d3", "twenty") - 0.25, 0.35, 16), (T("t1", "any") - 0.2, 0.35, 14), (T("t2", "ten") - 0.25, 0.3, 12),
           (T("t3", "hoard") - 0.15, 0.25, 10), (T("e1", "isn't") - 0.1, 0.25, 10)]


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
