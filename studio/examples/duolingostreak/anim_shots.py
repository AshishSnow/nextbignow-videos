# ================= shots: "Duolingo is free — so how did it make $1B? The streak." =================
# Sources: Duolingo FY2025 10-K (streak DAUs, 9% paid, 7.7% ads, free + ad per lesson), Q4 FY2025 results 8-K ($1,037.6M revenue),
#          Q2 2026 results 8-K (12.7M paid subs, 15.4M revived streaks), Duolingo blog (Jan 2022: 7-day streak -> 3.6x course completion)
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "last") - 0.1, "punch"), ("S1", T("i2", "The") - 0.2, "flash"),
    ("S2", T("a1", "Every") - 0.2, "whip"), ("S2b", T("a1", "You") - 0.12, "focus"), ("S3", T("a2", "But") - 0.2, "zoom"),
    ("S4", T("a3", "The") - 0.2, "whip"), ("S5", T("a4", "By") - 0.2, "punch"), ("S6", T("b1", "So") - 0.2, "whip"),
    ("S7", T("b2", "That's") - 0.2, "focus"), ("S8", T("b3", "On") - 0.2, "whip"), ("S9", T("c0", "And") - 0.2, "flash"),
    ("S10", T("c1", "At") - 0.2, "zoom"), ("S11", T("c2", "And") - 0.2, "whip"), ("S12", T("c3", "In") - 0.2, "focus"),
    ("S13", T("d1", "Here's") - 0.2, "flash"), ("S14", T("d2", "The") - 0.2, "whip"), ("S15", T("d3", "But") - 0.2, "punch"),
    ("S15b", T("d3", "People") - 0.12, "zoom"), ("S16", T("e1", "So") - 0.2, "whip"), ("S17", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_K = "Source: Duolingo 2025 annual report (SEC 10-K)"
SRC_Q4 = "Source: Duolingo Q4 & full-year 2025 results (SEC 8-K)"
SRC_Q2 = "Source: Duolingo Q2 2026 results (SEC 8-K, Aug 2026)"
SRC_BLOG = "Source: Duolingo blog, \"The habit-building research behind your streak\" (2022)"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, out=None, col=YEL_, size=220, tail=""):
    """white lead + coloured big word with shadow (for dark/saturated sets)"""
    ui_word(f, lead, big, 470, t, t0, col=col, size=size, shadow=0.45, lead_col=WHITE, out=out, tail=tail)


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


def src(f, text, t, t0, y=1452, size=20):
    if t >= t0: comp(f, chip(text, INK, WHITE, size), 540, y, op=clamp((t - t0) / 0.3))


def fl_flick(t, i=0): return 1.0 + 0.04 * math.sin(t * 17 + i) + 0.02 * math.sin(t * 29 + 2 * i)


# ---- S0: hook — FREE lessons on a phone, but $1B+ ----
def shot_S0(t, n):
    f = stage("purple", (255, 200, 60), 540, 1010, 450)
    tf = T("i1", "free…") - 0.2; tb = T("i1", "billion") - 0.25
    coin_rain(f, t + 0.6, 0.0, 6, 540, 420, 1480, 9)
    rot_comp(f, app_phone("lesson", label="FREE!"), 540, 1060 + 8 * math.sin(t * 3), -6 + 2 * math.sin(t * 2), 0.92 + 0.06 * eo(clamp(t / 0.4)), 1.0, 0.4)
    slam(f, stamp_el("FREE", GRN_, 96), 540, 1200, -14, t, tf)
    if t >= tb:
        rays(f, 540, 1060, 720, (255, 240, 160), 0.45 * clamp((t - tb) / 0.3), t)
        coin_rain(f, t, tb, 12, 540, 390, 1480, 2)
        comp(f, chip("$1,037.6M revenue in 2025", INK, YEL_, 40), 540, 1385, scale=pin(t, tb + 0.15, 0.25))
        src(f, SRC_Q4, t, tb + 0.4)
    wui(f, "every lesson is", "FREE", t, -0.5, out=tb - 0.05, col=WHITE, size=240)
    wui(f, "yet last year it made over", "$1 BILLION", t, tb, size=165)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1000), n)


# ---- S0b: so how? ----
def shot_S0b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S0b")
    th = st_("S0b") + 0.3
    comp(f, app_phone("lesson", label="FREE!", w=330, h=616), 330, 1020, scale=pin(t, st_("S0b") + 0.02, 0.3))
    comp(f, scale_el(cash_el(3), 1.0), 330, 1400 + 8 * math.sin(t * 6), scale=pin(t, th, 0.3))
    guy(f, 800, 1500, 0.82, la=(30, 20), ra=(150, 150), mouth=talk(t), blink=blink_at(t, 1), brow="sus", look=(-1, -1),
        expr="sus" if talk(t) == 0 else "n")
    comp(f, bubble_el("???", 60), 800, 860, scale=pin(t, th, 0.3))
    ui_word(f, "free app, $1 billion", "SO HOW?", 470, t, st_("S0b") + 0.06, col=RED_, size=200)
    return finish(f, n)


# ---- S1: one tiny number — your streak ----
def shot_S1(t, n):
    f = stage("orange", (255, 230, 120), 540, 1020, 440); u = lt(t, "S1")
    tt = T("i2", "tiny") - 0.2; ts = T("i2", "streak.") - 0.25
    k = eo(clamp((t - ts) / 0.5)) if t >= ts else 0.0
    if t >= ts: rays(f, 540, 1080, 760, (255, 250, 200), 0.4 * k, t)
    s = (0.7 + 0.3 * k) * fl_flick(t)
    comp(f, flame_el(500, 640, "1" if t < ts else "365"), 540, 1060, scale=s * pin(t, st_("S1") + 0.05, 0.3))
    wui(f, "the secret is one", "TINY NUMBER", t, st_("S1") + 0.06, out=ts - 0.05, col=WHITE, size=170)
    wui(f, "your", "STREAK", t, ts, size=250)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1050), n)


# ---- S2: every course free ----
def shot_S2(t, n):
    f = stage("sky", (255, 230, 120), 540, 1000, 430); u = lt(t, "S2")
    tf = T("a1", "free.") - 0.25
    words = (("HOLA", (255, 90, 80)), ("BONJOUR", (90, 120, 255)), ("CIAO", (40, 180, 120)), ("HALLO", (255, 170, 30)),
             ("OLÁ", (180, 80, 230)), ("SALUT", (255, 110, 170)))
    for i, (w_, c_) in enumerate(words):
        r, cc = divmod(i, 2); x = 310 + cc * 460; y = 760 + r * 250
        rot_comp(f, course_el(w_, c_, 360, 200), x, y + 6 * math.sin(t * 3 + i), (-5, 4, -3, 6, -4, 3)[i], pin(t, st_("S2") + 0.08 * i, 0.3), 1.0, 0.3)
        if t >= tf + 0.06 * i: comp(f, tag_el("$0", GRN_, WHITE, 40), x + 120, y - 70, scale=pin(t, tf + 0.06 * i, 0.25))
    ui_word(f, "every course really is", "FREE", 470, t, st_("S2") + 0.08, col=WHITE, size=240, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S2b: you just watch an ad after each lesson ----
def shot_S2b(t, n):
    f = stage("teal", (255, 214, 120), 540, 980, 420); u = lt(t, "S2b")
    ta = T("a1", "ad") - 0.25
    if t < ta:
        comp(f, app_phone("lesson"), 540, 1080, scale=pin(t, st_("S2b") + 0.02, 0.3))
    else:
        k = clamp((t - ta) / 3.0)
        comp(f, app_phone("ad", ad_k=k), 540, 1080, scale=pin(t, ta, 0.25))
    guy(f, 170, 1500, 0.62, la=(30, 20), ra=(40, 30), mouth=talk(t), blink=blink_at(t, 2), brow="n", look=(1, 0), expr="n" if t < ta else "sus")
    wui(f, "lesson done…", "THEN", t, st_("S2b") + 0.06, out=ta - 0.05, col=WHITE, size=200)
    wui(f, "free users watch an", "AD", t, ta, size=260)
    if t >= ta: src(f, "\"Learners who use Duolingo for free see an ad at the end of each lesson\" — 10-K", t, ta + 0.4, size=21)
    return finish(f, n)


# ---- S3: ads = less than 8 cents of every dollar ----
def shot_S3(t, n):
    f = stage("cream", (255, 214, 90), 540, 1000, 440); u = lt(t, "S3")
    te = T("a2", "eight") - 0.25
    k = eo(clamp((t - te) / 0.6)) if t >= te else 0.0
    cents_grid(f, 540, 1060, 8, (255, 120, 20), 48, 10, k, dim=(235, 235, 240))
    if t >= te: comp(f, chip("ADS: ~7.7% OF 2025 REVENUE", INK, YEL_, 38), 540, 1390, scale=pin(t, te + 0.3, 0.25))
    src(f, SRC_K, t, te + 0.5)
    ui_word(f, "one dollar of revenue", "100¢", 470, t, st_("S3") + 0.06, col=INK, size=200, out=te - 0.05)
    ui_word(f, "from ads: less than", "8¢", 470, t, te, col=RED_, size=250)
    return finish(f, n)


# ---- S4: only ~9 in 100 monthly users pay ----
PAY_IDX = (3, 17, 24, 38, 46, 59, 63, 77, 92)


def shot_S4(t, n):
    f = stage("emerald", (0, 220, 200), 540, 1000, 430); u = lt(t, "S4")
    tn = T("a3", "nine") - 0.25
    people_grid(f, 540, 1060, clamp(u / 1.2), set(PAY_IDX), t, r=32, step=76, crown_k=clamp((t - tn) / 0.4) if t >= tn else 0.0)
    if t >= tn: src(f, "About 9% of monthly active users were paid subscribers (Dec 31, 2025) — 10-K", t, tn + 0.4, y=1462, size=21)
    wui(f, "the real money?", "WHO PAYS", t, st_("S4") + 0.06, out=tn - 0.05, col=WHITE, size=200)
    wui(f, "monthly users who pay", "9 IN 100", t, tn, size=220)
    return finish(f, n)


# ---- S5: 12.7 million subscribers by June ----
def shot_S5(t, n):
    f = stage("pink", (255, 240, 120), 540, 1000, 430); u = lt(t, "S5")
    tt = T("a4", "twelve") - 0.3
    k = eo(clamp((t - tt + 0.9) / 1.3))
    for i, (x, y, r) in enumerate(((190, 830, -12), (890, 840, 10), (200, 1300, 8), (880, 1290, -9))):
        rot_comp(f, scale_el(coin_el(60, abs(math.cos(t * 3 + i))), 1.0), x, y + 12 * math.sin(t * 4 + i), r, pin(t, st_("S5") + 0.1 * i, 0.3), 1.0, 0.3)
    odometer(f, 540, 1060, "12.7", k, (130, 190), seed=3)
    comp(f, chip("MILLION PAID SUBSCRIBERS", INK, YEL_, 42), 540, 1240, op=clamp((t - tt) / 0.25))
    src(f, SRC_Q2, t, tt + 0.4)
    ui_word(f, "paying subscribers, June 2026", "12.7M", 470, t, tt, col=INK, size=230)
    return finish(f, n)


# ---- S6: one job — get you back every single day ----
def shot_S6(t, n):
    f = stage("sky", (255, 255, 255), 540, 980, 420); u = lt(t, "S6")
    te = T("b1", "Every") - 0.2
    comp(f, app_phone("notif", w=380, h=700), 540, 1100, scale=pin(t, st_("S6") + 0.02, 0.3))
    for i, (txt, sub) in enumerate((("Time for today's lesson!", "Keep your streak alive"), ("Still there?", "Your streak is waiting"), ("Don't break it!", "Just one quick lesson"))):
        tq = st_("S6") + 0.35 + 0.55 * i
        if t >= tq:
            sh = 6 * math.sin((t - tq) * 60) * math.exp(-(t - tq) * 6)
            comp(f, notif_el(txt, sub, 660, 150), 540 + sh, 860 + 170 * i, scale=pin(t, tq, 0.25))
    if t >= te: comp(f, chip("EVERY. SINGLE. DAY.", RED_, WHITE, 46), 540, 1400, scale=pin(t, te, 0.25))
    wui(f, "one job: get you", "BACK", t, st_("S6") + 0.06, col=WHITE, size=240)
    return finish(f, n)


# ---- S7: miss one day -> back to zero ----
def shot_S7(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1000, 430); u = lt(t, "S7")
    tm = T("b2", "Miss") - 0.15; tz = T("b2", "zero.") - 0.3
    done = min(6, int(u / 0.32)) if t < tm else 6
    xk = clamp((t - tm) / 0.25) if t >= tm else 0.0
    week_strip(f, 540, 820, done if t < tz else 0, miss=6 if t >= tm else -1, cell=104, gap=12, x_k=xk)
    lit = 1.0 if t < tz else max(0.0, 1 - (t - tz) / 0.3)
    num = str(max(1, done)) if t < tz else "0"
    comp(f, flame_el(360, 460, num, max(0.0, lit)), 540, 1190, scale=fl_flick(t) if t < tz else 1.0)
    smoke(f, 540, 1050, t, tz)
    ui_word(f, "that's what the", "STREAK", 470, t, st_("S7") + 0.06, col=INK, size=230, out=tm - 0.05)
    ui_word(f, "miss one day…", "BACK TO 0", 470, t, tm, col=RED_, size=200)
    return finish(f, n)


# ---- S8: split screen — day 2 vs day 200 ----
def shot_S8(t, n):
    f = stage("red", (255, 200, 60), 540, 980, 420); u = lt(t, "S8")
    th = T("b3", "hundred,") - 0.3; tl = T("b3", "losing", 0) - 0.15
    cv2.rectangle(f, (80, 640), (500, 1470), C((255, 244, 225)), -1, cv2.LINE_AA); cv2.rectangle(f, (80, 640), (500, 1470), C(INK), 8, cv2.LINE_AA)
    cv2.rectangle(f, (540, 640), (960, 1470), C((255, 196, 170)), -1, cv2.LINE_AA); cv2.rectangle(f, (540, 640), (960, 1470), C(INK), 8, cv2.LINE_AA)
    comp(f, flame_el(170, 220, "2"), 290, 820, scale=pin(t, st_("S8") + 0.05, 0.3) * fl_flick(t))
    guy(f, 290, 1420, 0.62, la=(60, 40), ra=(60, 40), mouth=talk(t) if t < th else 0, blink=blink_at(t, 2), brow="n", expr="n")
    if t >= st_("S8") + 0.4: comp(f, bubble_el("meh", 44), 290, 1010, scale=pin(t, st_("S8") + 0.4, 0.25))
    if t >= th:
        comp(f, flame_el(320, 410, "200"), 750, 880, scale=pin(t, th, 0.3) * fl_flick(t, 1))
        guy(f, 750, 1420, 0.62, la=(150, 140), ra=(150, 140), mouth=3, blink=False, brow="up", expr="n", bob=4 * math.sin(t * 30))
        for i in range(3): cv2.circle(f, (int(680 + 70 * i), int(1080 - 30 * ((t * 2 + i * 0.3) % 1) * 4)), 10, C((140, 200, 255)), -1, cv2.LINE_AA)
    if t >= tl: comp(f, scale_el(cash_el(2), 0.9), 750, 1300 + 80 * clamp((t - tl) / 0.6), op=1 - clamp((t - tl - 0.4) / 0.5))
    wui(f, "day 2?", "WHO CARES", t, st_("S8") + 0.06, out=th - 0.05, col=WHITE, size=200)
    wui(f, "losing it feels like losing money", "DAY 200", t, th, size=220)
    return finish(f, n)


# ---- S9: re-hook — wait for this number ----
def shot_S9(t, n):
    f = stage("purple", (0, 200, 255), 540, 1000, 430); u = lt(t, "S9")
    tw = T("c0", "Wait") - 0.15
    ok = clamp((t - tw) / 0.9) if t >= tw else 0.0
    rot_comp(f, envelope_el(640, 440, round(ok * 10) / 10), 540, 1080 + 8 * math.sin(t * 5), 3 * math.sin(t * 7) * (1 - ok), pin(t, st_("S9") + 0.03, 0.3), 1.0, 0.35)
    if t >= tw: rays(f, 540, 1000, 700, (255, 240, 160), 0.35 * ok, t)
    wui(f, "and it works", "WAY BETTER", t, st_("S9") + 0.06, out=tw - 0.05, col=WHITE, size=190)
    wui(f, "wait for this", "NUMBER", t, tw, size=230)
    return finish(cam(f, 1.0 + 0.03 * u, W / 2, 1000), n)


# ---- S10: 43M daily users on a 7+ day streak ----
def shot_S10(t, n):
    f = stage("orange", (255, 230, 120), 540, 1000, 440); u = lt(t, "S10")
    tf = T("c1", "forty") - 0.3; tw = T("c1", "week") - 0.2
    for i in range(18):
        x = 165 + (i % 6) * 140 + (70 if (i // 6) % 2 else 0); y = 740 + (i // 6) * 140
        tq = st_("S10") + 0.05 * i
        if t >= tq:
            comp(f, mini_head(40, True), x, y, scale=pin(t, tq, 0.2))
            comp(f, flame_el(54, 68), x, y - 78, scale=fl_flick(t, i))
    k = eo(clamp((t - tf + 0.6) / 1.0))
    if t >= tf - 0.6:
        odometer(f, 540, 1360, "43M", k, (110, 150), seed=4)
    if t >= tw: comp(f, chip("DAILY USERS ON A 7+ DAY STREAK", INK, YEL_, 34), 540, 1180, scale=pin(t, tw, 0.25))
    src(f, "As of Dec 31, 2025 — " + SRC_K[8:], t, tf + 0.5, y=1468, size=21)
    wui(f, "open it every day, on a streak of a week+", "43 MILLION", t, tf, col=WHITE, size=190)
    return finish(f, n)


# ---- S11: 15M with a streak over a whole year — year heatmap ----
def shot_S11(t, n):
    f = stage("teal", (255, 214, 120), 540, 980, 420); u = lt(t, "S11")
    tf = T("c2", "fifteen") - 0.3; ty = T("c2", "year!") - 0.3
    if t >= ty: rays(f, 540, 1000, 700, (255, 250, 200), 0.3 * clamp((t - ty) / 0.3), t)
    heatmap(f, 540, 1000, clamp(u / max(0.5, ty - st_("S11"))), cols=26, rows=14, cell=26, gap=5)
    if t >= ty: comp(f, chip("365 DAYS IN A ROW", FLAME_O, WHITE, 44), 540, 1290, scale=pin(t, ty, 0.25))
    src(f, "About 15M daily users on a 365+ day streak (Dec 31, 2025) — 10-K", t, tf + 0.5, y=1440, size=21)
    wui(f, "on a streak longer than a year", "15 MILLION", t, tf, size=190)
    return finish(f, n)


# ---- S12: 15.4M revived a broken streak (June event) ----
def shot_S12(t, n):
    f = stage("emerald", (0, 220, 200), 540, 1000, 430); u = lt(t, "S12")
    tf = T("c3", "fifteen") - 0.3; tr = T("c3", "revived") - 0.2
    cv2.rectangle(f, (110, 640), (970, 1170), C((20, 30, 34)), -1, cv2.LINE_AA); cv2.rectangle(f, (110, 640), (970, 1170), C(INK), 10, cv2.LINE_AA)
    for gx in range(130, 970, 60): cv2.line(f, (gx, 650), (gx, 1160), C((30, 70, 60)), 2)
    lit = 0.0 if t < tr else clamp((t - tr) / 0.4)
    heart_line(f, 140, 940, 960, t, 1.0, col=(60, 230, 120) if t >= tr else (120, 120, 130), amp=150 if t >= tr else 4)
    comp(f, flame_el(240, 300, None, max(0.05, lit)), 390, 1300, scale=(0.8 + 0.2 * lit) * fl_flick(t))
    if t >= tr: comp(f, stamp_el("REVIVED", GRN_, 60), 690, 1320, scale=pin(t, tr, 0.25))
    src(f, "June 2026 \"Streak Revival\" event — " + SRC_Q2[8:], t, tf + 0.5, y=1470, size=21)
    wui(f, "people revived a broken streak", "15.4M", t, tf, col=WHITE, size=220)
    return finish(f, n)


# ---- S13: twist — every day back = another ad or another nudge to pay ----
def shot_S13(t, n):
    f = stage("red", (255, 200, 60), 540, 980, 420); u = lt(t, "S13")
    ta = T("d1", "ad…") - 0.25; tp = T("d1", "pay.") - 0.3
    sp = 1.2 * u; base_i = int(sp); off = (sp - base_i) * 260
    for i in range(-1, 6):
        x = 150 + i * 260 - off
        y = 1250
        op = clamp((x - 140) / 80) * clamp((930 - x) / 80)
        if op > 0: comp(f, chip(f"DAY {201 + base_i + i}", WHITE, INK, 46), x, y, op=op)
    cv2.rectangle(f, (60, 1310), (1020, 1330), C(INK), -1)
    w_ = walk(t, 1.0)
    guy(f, 640, 1180, 0.6, la=w_["la"], ra=(60, 30), ll=w_["ll"], rl=w_["rl"], bob=w_["bob"], mouth=talk(t), blink=blink_at(t, 4),
        brow="up", look=(-1, 0), expr="n", hold=scale_el(app_phone("streak", num="201"), 0.18), hold_off=(10, -20))
    if t >= ta: rot_comp(f, scale_el(app_phone("ad", ad_k=0.2), 0.62), 330, 900, -8, pin(t, ta, 0.25), 1.0, 0.3)
    if t >= tp: rot_comp(f, tag_el("UPGRADE?", YEL_, INK, 56), 770, 860, 8, pin(t, tp, 0.25), 1.0, 0.3)
    wui(f, "here's the", "TWIST", t, st_("S13") + 0.06, out=ta - 0.05, col=YEL_, size=250)
    wui(f, "every day back = another ad…", "OR A NUDGE", t, ta, col=WHITE, size=190, tail="to pay")
    return finish(f, n)


# ---- S14: streak costs nothing — your habit is the business (habit loop) ----
def shot_S14(t, n):
    f = stage("cream", (255, 214, 90), 540, 1020, 440); u = lt(t, "S14")
    th = T("d2", "habit") - 0.25
    if t < th:
        comp(f, flame_el(320, 410, None), 540, 1080, scale=pin(t, st_("S14") + 0.03, 0.3) * fl_flick(t))
        slam(f, tag_el("COSTS $0", GRN_, WHITE, 60), 600, 1320, -6, t, st_("S14") + 0.5)
    else:
        k = clamp((t - th) / 1.6)
        loop_diagram(f, 540, 1060, 300, ("OPEN APP", "LESSON", "AD / UPSELL", "TOMORROW"), k, t, (APPBLUE, FLAME_O, RED_, PURP))
        comp(f, flame_el(170, 220, None), 540, 1060, scale=pin(t, th, 0.3) * fl_flick(t))
    ui_word(f, "the streak costs you", "NOTHING", 470, t, st_("S14") + 0.06, col=GRN_, size=220, out=th - 0.05)
    ui_word(f, "your habit is", "THE BUSINESS", 470, t, th, col=RED_, size=190)
    return finish(f, n)


# ---- S15: steal the trick ----
def shot_S15(t, n):
    f = stage("purple", (255, 200, 60), 540, 1000, 430); u = lt(t, "S15")
    x = 280 + 260 * eo(clamp(u / 0.8))
    w_ = walk(t, 1.2)
    guy(f, x, 1450, 0.85, la=w_["la"], ra=(70, 40), ll=w_["ll"], rl=w_["rl"], bob=w_["bob"], mouth=talk(t), blink=blink_at(t, 3),
        brow="sus", look=(1, 0), expr="smirk" if talk(t) == 0 else "n", hold=swag_el(260, 280), hold_off=(70, -40))
    comp(f, flame_el(140, 180), 880, 820, scale=fl_flick(t))
    wui(f, "now you can", "STEAL IT", t, st_("S15") + 0.06, col=YEL_, size=230)
    return finish(f, n)


# ---- S15b: 7-day streak -> 3.6x more likely to finish the course ----
def shot_S15b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 430); u = lt(t, "S15b")
    tt = T("d3", "three") - 0.3
    base = 1330
    bars(f, 330, base, 220, 160, (200, 205, 215), clamp(u / 0.6), "NO STREAK", "1x")
    bars(f, 750, base, 220, 460, FLAME_O, clamp((t - tt) / 0.6) if t >= tt else 0.0, "7-DAY STREAK", "")
    if t >= tt + 0.5: comp(f, cap_el(), 750, base - 460 - 80, scale=pin(t, tt + 0.5, 0.25))
    src(f, SRC_BLOG, t, tt + 0.5, y=1462, size=21)
    ui_word(f, "people who hit a", "7-DAY STREAK", 470, t, st_("S15b") + 0.06, col=WHITE, size=170, shadow=0.45, lead_col=WHITE, out=tt - 0.05)
    ui_word(f, "more likely to finish their course", "3.6x", 470, t, tt, col=YEL_, size=250, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


# ---- S16: takeaway — start a streak, survive the first 7 days ----
def shot_S16(t, n):
    f = stage("pink", (255, 214, 120), 540, 1000, 430); u = lt(t, "S16")
    ts = T("e1", "Start") - 0.2; t7 = T("e1", "seven") - 0.3
    done = 0 if t < ts else min(7, 1 + int((t - ts) / max(0.2, (t7 - ts) / 6)))
    week_strip(f, 540, 900, done, cell=104, gap=12, labels="1234567")
    if done >= 7: comp(f, check_el(70, True), 540, 1120, scale=pin(t, t7 + 0.2, 0.3))
    for i, lab in enumerate(("GYM", "SAVING", "READING")):
        if t >= ts + 0.3 + 0.2 * i: comp(f, chip(lab, (INK, NAVY_, PURP)[i], WHITE, 40), 260 + 280 * i, 1320, scale=pin(t, ts + 0.3 + 0.2 * i, 0.25))
    wui(f, "want a habit to stick?", "START A STREAK", t, st_("S16") + 0.06, out=t7 - 0.05, col=WHITE, size=170)
    wui(f, "just survive the first", "7 DAYS", t, t7, size=250)
    return finish(f, n)


# ---- S17: send it + brand sting ----
def shot_S17(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S17")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("day 1,000 streak?? how", "ok I'm scared to miss a day", pr), 0.82), 600, 950, scale=pin(t, st_("S17")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=flame_el(120, 150), hold_off=(20, -30))
        ui_word(f, "send to the friend who's", "NEVER MISSED", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=140, shadow=0.3, tail="a day")
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "free…") - 0.15, 0.3, 12), (T("i1", "billion") - 0.25, 0.35, 16), (T("i2", "streak.") - 0.25, 0.35, 16),
           (T("a1", "ad") - 0.25, 0.25, 10), (T("a2", "eight") - 0.25, 0.3, 14), (T("a3", "nine") - 0.25, 0.3, 12),
           (T("a4", "twelve") - 0.3, 0.3, 14), (T("b2", "Miss") - 0.15, 0.25, 12), (T("b2", "zero.") - 0.3, 0.35, 16),
           (T("b3", "hundred,") - 0.3, 0.3, 14), (T("c1", "forty") - 0.3, 0.35, 16), (T("c2", "year!") - 0.3, 0.3, 14),
           (T("c3", "revived") - 0.2, 0.3, 14), (T("d1", "ad…") - 0.25, 0.25, 10), (T("d1", "pay.") - 0.3, 0.25, 10),
           (T("d2", "habit") - 0.25, 0.3, 12), (T("d3", "three") - 0.3, 0.35, 16), (T("e1", "seven") - 0.3, 0.3, 14)]


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
