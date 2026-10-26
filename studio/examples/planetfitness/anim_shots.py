# ================= shots: "Planet Fitness: $15 a month, $220M profit" =================
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "The") - 0.12, "punch"), ("S1", T("a1", "Secret") - 0.2, "whip"),
    ("S1b", T("a2", "Fifteen") - 0.12, "focus"), ("S2", T("b1", "Secret") - 0.2, "flash"), ("S2b", T("b2", "But") - 0.12, "zoom"),
    ("S2c", T("b3", "If") - 0.12, "punch"), ("S3a", T("c1", "Secret") - 0.2, "whip"), ("S3b", T("c2", "A") - 0.12, "focus"),
    ("S4a", T("d1", "And") - 0.2, "flash"), ("S4b", T("d2", "They") - 0.12, "zoom"), ("S4c", T("d3", "When") - 0.12, "punch"),
    ("S4d", T("d4", "Eighty") - 0.15, "focus"), ("S5", T("f1", "Last") - 0.2, "whip"), ("S6", T("e1", "So") - 0.2, "flash"),
    ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_PF = "Source: Planet Fitness FY2025 annual report (10-K)"
SRC_PR = "Source: Planet Fitness Q4 2025 results, Feb 2026"
SRC_STUDY = "Source: DellaVigna & Malmendier, American Economic Review, 2006"


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


# ---- S0: hook — gym with a tiny $15 tag, then a money pile ----
def shot_S0(t, n):
    f = stage("teal", (255, 150, 60), 540, 980, 440)
    tf = T("i1", "fifteen") - 0.12; tm = T("i1", "million") - 0.2
    comp(f, scale_el(gym_el(), 0.95), 540, 1170, scale=pin(t, 0.0, 0.35))
    if t >= tf:
        rot_comp(f, tag_el("$15 / MONTH", YEL_, INK, 64), 600, 860 + 6 * math.sin(t * 5), 8, pin(t, tf, 0.25), 1.0, 0.35)
    if t >= tm:
        coin_rain(f, t, tm, 7, 540, 400, 1500, 3)
        rot_comp(f, tag_el("$200M+ PROFIT", GRN_, WHITE, 76), 520, 1390, -5, pin(t, tm, 0.25), 1.0, 0.35)
    ui_word(f, "planet fitness charges just", "$15 A MONTH", 470, t, 0.12, col=WHITE, size=170, shadow=0.4, lead_col=WHITE, out=tm - 0.05)
    ui_word(f, "and still makes", "$200M+", 470, t, tm, col=YEL_, size=210, shadow=0.4, lead_col=WHITE)
    return finish(cam(f, 1.0 + 0.015 * t, W / 2, 1000), n)


# ---- S0b: kind of genius — and it involves YOU ----
def shot_S0b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S0b")
    ty = T("i2", "you!") - 0.2
    rays(f, 540, 1080, 700, (255, 255, 255), 0.35, t)
    if t < ty:
        guy(f, 540, 1500, 1.0, la=(120, 160), ra=(150, 170), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(0, -1),
            expr="wow" if talk(t) == 0 else "n")
        comp(f, bubble_el("GENIUS!", 56), 760, 830, scale=pin(t, T("i2", "genius.") - 0.2, 0.3))
    else:
        # mascot points straight at the viewer, zooming in
        z = 1.0 + 0.25 * eo(clamp((t - ty) / 0.4))
        guy(f, 540, 1500 + 120 * (z - 1), z, la=(18, 8), ra=(95, 95), mouth=talk(t), blink=False, brow="sus", look=(0, 0),
            expr="smirk" if talk(t) == 0 else "n")
    ui_word(f, "the answer is kind of", "GENIUS", 470, t, SHOT["S0b"]["start"] + 0.05, col=INK, size=200, out=ty - 0.05)
    ui_word(f, "and it involves", "YOU", 470, t, ty, col=RED_, size=240)
    return finish(f, n)


# ---- S1: secret 1 — so cheap that cancelling feels pointless ----
def shot_S1(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S1")
    tp = T("a1", "pointless.") - 0.2
    pr = t >= tp
    comp(f, scale_el(cancel_phone_el(pr), 0.95), 620, 1080, scale=pin(t, SHOT["S1"]["start"] + 0.03, 0.3))
    guy(f, 230, 1500, 0.8, la=(18, 8), ra=(70, 40) if not pr else (40, 10), mouth=talk(t), blink=blink_at(t, 2), brow="n" if not pr else "sus",
        look=(1, 0), expr="sus" if pr and talk(t) == 0 else "n")
    if pr: slam(f, stamp_el("WHY BOTHER?", RED_, 60), 620, 1380, -8, t, tp)
    ui_word(f, "secret 1", "SO CHEAP", 470, t, SHOT["S1"]["start"] + 0.08, col=INK, size=190, out=tp - 0.05)
    ui_word(f, "cancelling feels", "POINTLESS", 470, t, tp, col=RED_, size=170)
    return finish(cam(f, 1.04 - 0.04 * eo(clamp(u / 1.5)), W / 2, 1100), n)


# ---- S1b: $15/month + $49/year ----
def shot_S1b(t, n):
    f = stage("pink", (255, 230, 120), 540, 1000, 430); u = lt(t, "S1b")
    ty = T("a2", "yearly") - 0.2
    comp(f, scale_el(member_card_el(), 1.0), 540, 1000, scale=pin(t, SHOT["S1b"]["start"] + 0.03, 0.3))
    rot_comp(f, tag_el("$15 / MONTH", YEL_, INK, 70), 560, 1290, -4, pin(t, T("a2", "Fifteen") - 0.05, 0.25), 1.0, 0.35)
    if t >= ty:
        rot_comp(f, tag_el("+ $49 / YEAR", RED_, WHITE, 66), 560, 760, 5, pin(t, ty, 0.25), 1.0, 0.35)
    comp(f, chip(SRC_PF, INK, WHITE, 22), 540, 1430, op=clamp((u - 0.6) / 0.3))
    ui_word(f, "fifteen bucks a month", "+ $49 A YEAR", 470, t, SHOT["S1b"]["start"] + 0.1, col=WHITE, size=150, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S2: secret 2 — pack in the members (crowd fills) ----
def shot_S2(t, n):
    f = stage("emerald", (0, 220, 200), 540, 1000, 430); u = lt(t, "S2")
    tt = T("b1", "twenty-one") - 0.2
    k = 0.08 + 0.92 * clamp((t - SHOT["S2"]["start"]) / max(0.3, tt + 0.3 - SHOT["S2"]["start"]))
    crowd(f, 540, 1050, 8, 7, k, 46, 8, t, 5, jitter=3.0)
    if t >= tt:
        rot_comp(f, tag_el("20.8 MILLION", YEL_, INK, 84), 540, 1400, -4, pin(t, tt, 0.25), 1.0, 0.4)
    ui_word(f, "secret 2", "PACK THEM IN", 470, t, SHOT["S2"]["start"] + 0.08, col=WHITE, size=160, shadow=0.4, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "members, end of 2025", "~21 MILLION", 470, t, tt, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: 2,896 clubs -> 7,000+ members per gym ----
def shot_S2b(t, n):
    f = stage("orange", YEL_, 540, 1000, 430); u = lt(t, "S2b")
    ts = T("b2", "seven") - 0.2
    if t < ts:
        for i in range(9):
            r_, c_ = divmod(i, 3)
            comp(f, scale_el(gym_el(), 0.34), 300 + c_ * 240, 830 + r_ * 210, scale=pin(t, SHOT["S2b"]["start"] + 0.05 * i, 0.25))
        comp(f, chip("2,896 CLUBS", INK, WHITE, 40), 540, 1420, scale=pin(t, T("b2", "clubs.") - 0.25, 0.25))
    else:
        comp(f, scale_el(gym_el(), 0.7), 540, 1120)
        crowd(f, 540, 830, 9, 2, clamp((t - ts) / 0.5), 40, 6, t, 9, jitter=2.0)
        rot_comp(f, tag_el("7,000+ PER GYM", RED_, WHITE, 72), 540, 1410, -4, pin(t, ts + 0.1, 0.25), 1.0, 0.35)
        comp(f, chip("20.8M members / 2,896 clubs (FY2025)", INK, WHITE, 22), 540, 1475, op=clamp((t - ts - 0.4) / 0.3))
    ui_word(f, "but under 3,000", "CLUBS", 470, t, SHOT["S2b"]["start"] + 0.1, col=WHITE, size=200, shadow=0.4, lead_col=WHITE, out=ts - 0.05)
    ui_word(f, "members per gym", "7,000+", 470, t, ts, col=YEL_, size=210, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2c: if they all showed up — gym bursting ----
def shot_S2c(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S2c")
    tc = T("b3", "chaos!") - 0.2
    sq = 1.0 + (0.04 * math.sin(t * 30) if t >= tc else 0.0)
    comp(f, scale_el(gym_el(), 0.85), 540, 1130, scale=sq)
    k = clamp(u / max(0.4, tc - SHOT["S2c"]["start"]))
    crowd(f, 540, 1090, 6, 3, k, 40, 6, t, 13, jitter=4.0 + (8 if t >= tc else 0))
    if t >= tc:
        rng = np.random.default_rng(int(t * 8))
        for j in range(8):
            q = (t - tc) * 1.4 + j * 0.13
            a = j * 0.8; rr = 260 + 260 * (q % 1.0)
            comp(f, mini_head(36, True), 540 + rr * math.cos(a), 1050 - abs(rr * math.sin(a)) * 0.7)
        slam(f, stamp_el("CHAOS!", WHITE, 90), 540, 1420, -8, t, tc)
    ui_word(f, "if they all showed up on the", "SAME DAY", 470, t, SHOT["S2c"]["start"] + 0.1, col=WHITE, size=170, shadow=0.4, lead_col=WHITE, out=tc - 0.05)
    ui_word(f, "total", "CHAOS", 470, t, tc, col=YEL_, size=220, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S3a: secret 3 — they know; it's in the annual report ----
def shot_S3a(t, n):
    f = stage("cream", (255, 120, 200), 540, 1000, 430); u = lt(t, "S3a")
    tr = T("c1", "report.") - 0.25
    comp(f, scale_el(treadmill_el(webs=clamp((u - 0.5) / 1.2)), 0.95), 560, 1150)
    if t >= tr:
        rot_comp(f, scale_el(report_el(("", "", ""), -1), 0.55), 300, 1080, 8, pin(t, tr, 0.3), 1.0, 0.35)
    guy(f, 860, 1500, 0.6, la=(18, 8), ra=(40, 150), mouth=talk(t), blink=blink_at(t, 3), brow="sus", look=(-1, 0), expr="sus" if talk(t) == 0 else "n")
    ui_word(f, "secret 3", "THEY KNOW", 470, t, SHOT["S3a"]["start"] + 0.08, col=INK, size=200, out=tr - 0.05)
    ui_word(f, "it's in their", "ANNUAL REPORT", 470, t, tr, col=RED_, size=140)
    return finish(f, n)


# ---- S3b: the 10-K quote, highlighted ----
def shot_S3b(t, n):
    f = stage("teal", (255, 214, 120), 540, 1000, 430); u = lt(t, "S3b")
    ql = ["“A PORTION OF OUR", "MEMBER BASE DOES", "NOT REGULARLY USE", "OUR CLUBS.”"]
    marks = [T("c2", "A"), T("c2", "member"), T("c2", "not"), T("c2", "our", 1)]
    ns = sum(1 for m in marks if t >= m - 0.1)
    tr = T("c2", "regularly") - 0.1
    kh = clamp((t - tr) / 0.4) if t >= tr else 0.0
    comp(f, report_el(tuple(ql[:ns] + [""] * (4 - ns)), 2, round(kh * 10) / 10), 540, 1020, scale=pin(t, SHOT["S3b"]["start"] + 0.03, 0.3))
    comp(f, chip(SRC_PF + ", risk factors", INK, WHITE, 22), 540, 1450, op=clamp(u / 0.4))
    ui_word(f, "planet fitness, in its own words", "", 470, t, SHOT["S3b"]["start"] + 0.1, col=WHITE, lead_col=WHITE)
    return finish(f, n)


# ---- S4a: Berkeley economists studied $70+/month members ----
def shot_S4a(t, n):
    f = stage("purple", (0, 200, 255), 540, 1000, 430); u = lt(t, "S4a")
    ts = T("d1", "seventy") - 0.2
    comp(f, scale_el(report_el(("GYM MEMBERS", "VS. THEIR", "CONTRACTS"), -1, 1.0, title="STUDY", year="BERKELEY ECONOMISTS"), 0.7),
         380, 1060, scale=pin(t, SHOT["S4a"]["start"] + 0.05, 0.3))
    comp(f, scale_el(magnifier_el(), 0.9), 540 + 20 * math.sin(t * 2), 1000 + 15 * math.cos(t * 2.4))
    guy(f, 860, 1500, 0.6, la=(18, 8), ra=(110, 70), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(-1, -1), expr="wow" if talk(t) == 0 else "n")
    if t >= ts:
        rot_comp(f, tag_el("$70+ / MONTH", YEL_, INK, 70), 560, 1400, -4, pin(t, ts, 0.25), 1.0, 0.35)
    ui_word(f, "berkeley economists", "STUDIED", 470, t, SHOT["S4a"]["start"] + 0.1, col=WHITE, size=190, shadow=0.4, lead_col=WHITE, out=ts - 0.05)
    ui_word(f, "members paying over", "$70 A MONTH", 470, t, ts, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S4b: under 5 visits -> $17+ per visit ----
def shot_S4b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S4b")
    tsv = T("d2", "seventeen") - 0.2
    days = (2, 9, 15, 22, 27)
    nd = sum(1 for i in range(5) if t >= SHOT["S4b"]["start"] + 0.25 + 0.22 * i)
    comp(f, scale_el(month_el(days[:nd]), 0.95), 540, 1040)
    if t >= tsv:
        rot_comp(f, tag_el("$17+ PER VISIT", RED_, WHITE, 74), 540, 1400, -4, pin(t, tsv, 0.25), 1.0, 0.35)
    comp(f, chip(SRC_STUDY, INK, WHITE, 22), 540, 1478, op=clamp((u - 0.8) / 0.3))
    ui_word(f, "average visits a month", "UNDER 5", 470, t, SHOT["S4b"]["start"] + 0.1, col=INK, size=200, out=tsv - 0.05)
    ui_word(f, "so each visit cost", "$17+", 470, t, tsv, col=RED_, size=230)
    return finish(f, n)


# ---- S4c: a $10 pass was right there ----
def shot_S4c(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S4c")
    base = 1420; k = eo(clamp((u - 0.1) / 0.6))
    cv2.line(f, (180, base), (900, base), C(INK), 8, cv2.LINE_AA)
    t1 = bar(f, 360, base, 200, 10 * 22, YEL_, k)
    t2 = bar(f, 720, base, 200, 17 * 22, RED_, k)
    comp(f, chip("PAY PER VISIT $10", INK, WHITE, 28), 360, t1 - 40, op=clamp(k * 2 - 1))
    comp(f, chip("MEMBERSHIP $17+", RED_, WHITE, 28), 720, t2 - 40, op=clamp(k * 2 - 1))
    tt = T("d3", "there.") - 0.25
    if t >= tt: rot_comp(f, scale_el(ticket_el(), 0.7), 360, 830, -8, pin(t, tt, 0.3), 1.0, 0.35)
    ui_word(f, "when a", "$10 PASS", 470, t, SHOT["S4c"]["start"] + 0.1, col=WHITE, size=200, shadow=0.4, lead_col=WHITE, tail="was right there")
    return finish(f, n)


# ---- S4d: 80% would have saved ----
def shot_S4d(t, n):
    f = stage("pink", (120, 40, 200), 540, 1000, 430); u = lt(t, "S4d")
    tsv = T("d4", "saved") - 0.2
    for i in range(10):
        r_, c_ = divmod(i, 5); x = 260 + c_ * 140; y = 900 + r_ * 220
        on = i < 8 and t >= tsv + 0.06 * i
        comp(f, mini_head(62, not on if t >= tsv else True), x, y, scale=pin(t, SHOT["S4d"]["start"] + 0.04 * i, 0.25))
        if on: comp(f, chip("OVERPAID", RED_, WHITE, 20), x, y + 90, scale=pin(t, tsv + 0.06 * i, 0.2))
    comp(f, chip(SRC_STUDY, INK, WHITE, 22), 540, 1450, op=clamp((u - 0.6) / 0.3))
    ui_word(f, "would have saved paying per visit", "80%", 470, t, SHOT["S4d"]["start"] + 0.1, col=WHITE, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S5: the money — $1.3B revenue, $220M profit ----
def shot_S5(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S5")
    tb = T("f1", "billion") - 0.2; tp = T("f1", "twenty") - 0.2
    base = 1360; sc_ = 0.42
    cv2.line(f, (180, base), (900, base), C(INK), 8, cv2.LINE_AA)
    k1 = eo(clamp((u - 0.1) / 0.5)) * (0.35 + 0.65 * eo(clamp((t - tb + 0.2) / 0.5))); k2 = eo(clamp((t - tp + 0.2) / 0.6))
    if t >= tp: rays(f, 720, base - 220 * sc_, 320, (255, 255, 220), 0.6 * clamp((t - tp) / 0.3), t)
    t1 = bar(f, 360, base, 220, 1324 * sc_, (120, 130, 150), k1)
    t2 = bar(f, 720, base, 220, 220 * sc_, GRN_, k2)
    if k1 > 0.5: comp(f, chip("REVENUE $1.3B", INK, WHITE, 30), 360, t1 - 40)
    if k2 > 0.5: comp(f, chip("PROFIT $220M", GRN_, WHITE, 32), 720, t2 - 40)
    comp(f, chip("REVENUE, 2025", INK, WHITE, 26), 360, base + 40); comp(f, chip("NET INCOME, 2025", INK, WHITE, 26), 720, base + 40)
    comp(f, chip(SRC_PR, INK, WHITE, 22), 540, 1460, op=clamp((t - tb - 0.3) / 0.3))
    ui_word(f, "planet fitness revenue, last year", "$1.3 BILLION", 470, t, SHOT["S5"]["start"] + 0.1, col=INK, size=160, out=tp - 0.05)
    ui_word(f, "and profit", "$220 MILLION", 470, t, tp, col=GRN_, size=160)
    return finish(f, n)


# ---- S6: payoff — not selling workouts, selling the plan ----
def shot_S6(t, n):
    f = stage("red", YEL_, 540, 1000, 430); u = lt(t, "S6")
    tp = T("e1", "plan") - 0.2
    if t < tp:
        comp(f, scale_el(dumbbell_el(), 1.0), 540, 1100, scale=pin(t, SHOT["S6"]["start"] + 0.05, 0.3))
        slam(f, stamp_el("NOT THE PRODUCT", WHITE, 56), 540, 1100, -8, t, T("e1", "workouts.") - 0.15)
    else:
        rays(f, 540, 1060, 700, (255, 240, 160), 0.5 * clamp((t - tp) / 0.3), t)
        rot_comp(f, scale_el(clipboard_el(), 0.95), 540, 1080 + 8 * math.sin(t * 5), -4, pin(t, tp, 0.3), 1.0, 0.35)
        comp(f, tag_el("THE PRODUCT", YEL_, INK, 60), 640, 1440 + 6 * math.sin(t * 5), scale=pin(t, tp + 0.15, 0.3))
    ui_word(f, "the cheap gym isn't really selling", "WORKOUTS", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, size=170, shadow=0.4, lead_col=WHITE, out=tp - 0.05)
    ui_word(f, "it's selling", "THE PLAN", 470, t, tp, col=YEL_, size=210, shadow=0.4, lead_col=WHITE, tail="to work out")
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("your gym is HOW cheap??", "ok i'll go monday lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(dumbbell_el(), 0.3), hold_off=(20, -10))
        ui_word(f, "send to the friend who never goes to", "THE GYM", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=150, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "fifteen") - 0.05, 0.25, 10), (T("i1", "million") - 0.15, 0.3, 14), (SHOT["S0b"]["start"] + 0.05, 0.25, 10),
           (T("i2", "you!") - 0.15, 0.3, 14), (T("a1", "pointless.") - 0.15, 0.3, 12), (T("a2", "yearly") - 0.15, 0.25, 10),
           (T("b1", "twenty-one") - 0.15, 0.3, 14), (T("b2", "seven") - 0.15, 0.3, 14), (T("b3", "chaos!") - 0.15, 0.5, 18),
           (T("c1", "report.") - 0.2, 0.25, 10), (T("d1", "seventy") - 0.15, 0.25, 10), (T("d2", "seventeen") - 0.15, 0.3, 14),
           (T("d4", "saved") - 0.15, 0.3, 12), (T("f1", "twenty") - 0.15, 0.3, 14), (T("e1", "workouts.") - 0.1, 0.3, 12),
           (T("e1", "plan") - 0.2, 0.3, 14)]


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
