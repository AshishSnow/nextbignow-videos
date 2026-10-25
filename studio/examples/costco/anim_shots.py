# ================= shots: "Costco's $1.50 hot dog" =================
def flip_h(el): return el[0][:, ::-1].copy(), el[1][:, ::-1].copy()


SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "And") - 0.15, "punch"), ("S1", T("i3", "So") - 0.15, "whip"), ("S1b", T("i4", "Here") - 0.15, "focus"),
    ("S2a", T("a1", "Secret") - 0.25, "whip"), ("S2b", T("a2", "When") - 0.12, "focus"), ("S2c", T("a3", "Because") - 0.12, "whip"),
    ("S3a", T("b1", "Secret") - 0.25, "whip"), ("S3b", T("b2", "Costco") - 0.12, "zoom"), ("S3c", T("b3", "And") - 0.12, "focus"),
    ("S4a", T("c1", "Secret") - 0.25, "whip"), ("S4b", T("c2", "Around") - 0.12, "focus"),
    ("S5a", T("d1", "And") - 0.25, "whip"), ("S5b", T("d2", "Costco's") - 0.12, "zoom"), ("S5c", T("d3", "Last") - 0.12, "whip"),
    ("S5d", T("d4", "And") - 0.12, "focus"), ("S6", T("e1", "So") - 0.2, "whip"), ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def title(f, sid, t, n_, big, col=WHITE, size=140):
    ui_word(f, f"SECRET {n_}", big, 470, t, SHOT[sid]["start"] + 0.05, col=col, size=size, shadow=0.3)


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


# ---- S0: hook — the $1.50 hot dog + soda ----
def shot_S0(t, n):
    f = stage("red", YEL_, 540, 960, 450)
    td = T("i1", "dollar") - 0.12
    cv2.rectangle(f, (150, 1170), (930, 1206), C((250, 250, 252)), -1, cv2.LINE_AA); cv2.rectangle(f, (150, 1200), (930, 1218), C((200, 204, 216)), -1)
    contact(f, 470, 1172, 600, 0.35)
    bob = 6 * math.sin(t * 3.2)
    comp(f, scale_el(cup_el(), 0.62), 820, 960 + bob * 0.5)
    comp(f, scale_el(hotdog_el(), 1.0), 455, 1065 + bob)
    steam(f, 455, 940, t, 1.1, 0.5)
    ui_word(f, "do you know…", "COSTCO", 470, t, T("i1", "Costco") - 0.12, col=WHITE, size=190, shadow=0.35)
    if t >= td:
        k = pin(t, td, 0.28)
        rot_comp(f, tag_el("$1.50", YEL_, INK, 150), 560, 760, -9, k * 1.05, 1.0, 0.35)
        comp(f, chip("HOT DOG + SODA", INK, WHITE, 34), 560, 880, op=clamp((t - td - 0.2) / 0.2))
        if t < td + 0.1: f = f + 0.3
    return finish(cam(f, 1.0 + 0.025 * t, W / 2, 1000), n)


# ---- S0b: same price for 40 years ----
def shot_S0b(t, n):
    f = stage("teal", (255, 255, 255), 600, 980, 420); u = lt(t, "S0b")
    k = clamp(u / 1.6) ** 0.55; yr = 1985 + int(round((2026 - 1985) * k))
    cx, cy = 640, 1010
    comp(f, scale_el(calendar_el("YEAR", str(yr)), 0.95), cx, cy, scale=pin(t, SHOT["S0b"]["start"], 0.25))
    if k < 1:
        fl = (u * 9) % 1
        cv2.ellipse(f, (cx, int(cy - 150 + 260 * fl)), (190, int(20 + 60 * (1 - fl))), 0, 180, 360, C((255, 255, 255)), -1, cv2.LINE_AA)
    rot_comp(f, tag_el("$1.50", YEL_, INK, 110), 780, 1300, 8, pin(t, SHOT["S0b"]["start"] + 0.15, 0.25), 1.0, 0.3)
    tf = T("i2", "forty") - 0.1
    if t >= tf: rot_comp(f, sign_el("SAME PRICE", RED_, WHITE, 52, False), 640, 1440, -6, pin(t, tf, 0.25), 1.0, 0.25)
    guy(f, 230, 1480, 0.85, la=(150, 165), ra=(150, 165), mouth=talk(t), expr="wow" if talk(t) == 0 else "n", brow="up", look=(1, -1),
        bob=-10 * abs(math.sin(t * 7)))
    ui_word(f, "same price for", "40 YEARS", 470, t, tf, col=WHITE, size=170, shadow=0.35)
    return finish(f, n)


# ---- S1: so how does Costco make billions? ----
def shot_S1(t, n):
    f = stage("emerald", GOLD, 540, 980, 420); u = lt(t, "S1")
    for i in range(7):
        q = u - 0.12 * i
        if q <= 0: continue
        y = min(1260 - (i // 2) * 70, -200 + 1500 * q * q * 1.6) if i < 6 else -200 + 1700 * ((q * 1.2) % 1)
        x = 540 + (-90 if i % 2 else 90) * (i < 6)
        rot_comp(f, scale_el(cash_el(), 0.7), x, y, (-1) ** i * 6, 1.0, 1.0, 0.25)
    guy(f, 860, 1480, 0.82, la=(18, 8), ra=(150, 175), mouth=talk(t), blink=blink_at(t, 1), brow="sus", look=(-1, -1),
        expr="sus" if talk(t) == 0 else "n")
    comp(f, ed_el("", "?", big_col=WHITE, big_size=150, shadow=0.3), 900, 1050 + 10 * math.sin(t * 5), op=clamp((u - 0.2) / 0.2))
    ui_word(f, "how does costco make", "BILLIONS?", 470, t, T("i3", "make") - 0.15, col=YEL_, size=180, shadow=0.35, lead_col=WHITE)
    return finish(cam(f, 1.04 - 0.04 * eo(clamp(u / 1.2)), W / 2, 1000), n)


# ---- S1b: 4 secret files, #4 is genius ----
FOLD = [(220, 880, -10), (430, 830, -3), (650, 830, 4), (860, 880, 11)]


def shot_S1b(t, n):
    f = stage("sky", YEL_, 540, 960, 400); u = lt(t, "S1b")
    tg = T("i4", "genius.") - 0.15
    ui_word(f, "", "4 SECRETS", 470, t, T("i4", "four") - 0.12, col=WHITE, size=180, shadow=0.35, out=T("i4", "last") - 0.1)
    ui_word(f, "and the last one is", "GENIUS", 470, t, tg, col=YEL_, size=180, shadow=0.4, lead_col=WHITE)
    kg = clamp((t - tg) / 0.3)
    if kg > 0: rays(f, 840 - 300 * eo(kg), 860 + 120 * eo(kg), 520, (255, 240, 150), 0.55 * kg, t)
    for i, (x, y, r) in enumerate(FOLD):
        t0 = T("i4", "four") - 0.05 + i * 0.12
        if t < t0: continue
        s_ = pin(t, t0, 0.28)
        if i == 3:
            gold = kg > 0.3
            rot_comp(f, folder_el(4, gold, "GENIUS" if gold else "TOP SECRET"), x - 300 * eo(kg), y + 120 * eo(kg),
                     r * (1 - kg) + 5 * math.sin(t * 24) * kg * math.exp(-max(0, t - tg) * 2), s_ * (0.95 + 0.45 * eo(kg)), 1.0, 0.3)
        else:
            rot_comp(f, folder_el(i + 1), x, y, r, s_ * 0.95, 1.0 - 0.6 * kg, 0.25)
    sus = t >= tg + 0.2
    guy(f, 540, 1490, 0.85, la=(18, 8), ra=(60, 150) if t > T("i4", "four") else (18, 8), mouth=talk(t), blink=blink_at(t, 2),
        look=(1, -1) if sus else (0, -1), brow="up" if sus else "n", expr="smirk" if (sus and talk(t) == 0) else "n")
    return finish(f, n)


# ---- S2a: secret 1 — the hot dog loses money on purpose ----
def shot_S2a(t, n):
    f = stage("orange", YEL_, 540, 980, 430); u = lt(t, "S2a")
    title(f, "S2a", t, 1, "LOSES MONEY", WHITE, 150)
    comp(f, scale_el(hotdog_el(), 0.9), 500, 1000 + 6 * math.sin(t * 3), scale=pin(t, SHOT["S2a"]["start"] + 0.05, 0.3))
    tl = T("a1", "loses") - 0.1
    if t >= tl:
        k = eo(clamp((t - tl) / 0.4))
        arrow(f, (500, 1180), (500, 1180 + 200 * k + 1), RED_, 26, 60)
        comp(f, ed_el("", "-$", big_col=WHITE, big_size=110, shadow=0.3), 500, 790, op=k, scale=pin(t, tl, 0.25))
        for i in range(5):
            q = t - tl - i * 0.09
            if q <= 0: continue
            comp(f, coin_el(30, math.cos(q * 8 + i)), 430 + 50 * i, 1120 + 700 * q * q, op=clamp(1.4 - q))
    tp = T("a1", "purpose.") - 0.05
    wink = t >= tp
    guy(f, 840, 1480, 0.82, la=(18, 8), ra=(40, -40) if wink else (18, 8), mouth=talk(t), blink=False, brow="up" if wink else "n",
        expr="smirk" if (wink and talk(t) == 0) else "n", look=(-1, 0))
    if wink: comp(f, chip("ON PURPOSE", INK, YEL_, 40), 800, 960, scale=pin(t, tp, 0.25))
    return finish(f, n)


# ---- S2b: the founder: "raise it and I'll kill you" ----
def shot_S2b(t, n):
    f = stage("cream", RED_, 540, 1030, 430); u = lt(t, "S2b")
    tr = T("a2", "raise") - 0.1; tf = T("a2", "founder") - 0.1; ti = T("a2", "if") - 0.1; tk = T("a2", "kill") - 0.15
    angry = t >= tf; boom = t >= tk
    sign = scale_el(sign_el("$1.75?", WHITE, INK, 60), 0.9) if t >= tr and not boom else None
    shake = 6 * math.sin(t * 60) * math.exp(-max(0, t - tk) * 5) if boom else 0
    guy(f, 300, 1450, 0.92, la=(18, 8), ra=(70, 150) if sign else (18, 8), mouth=0 if t < tk else 0, blink=blink_at(t, 3),
        expr="wow" if boom else "n", brow="up" if boom else "n", look=(1, 0), hold=sign, hold_off=(20, -90))
    if boom:
        q = t - tk
        rot_comp(f, scale_el(sign_el("$1.75?", WHITE, INK, 60), 0.9), 420 + 80 * q, 1000 + 900 * q * q, 30 * q * 6, 1.0, clamp(1.5 - q), 0.2)
        cv2.circle(f, (250, 990), 9, C((120, 200, 255)), -1, cv2.LINE_AA)
    guy(f, 780 + shake, 1450, 0.98, la=(60, 130) if boom else (18, 8), ra=(18, 8), mouth=talk(t) if t >= ti else 0, blink=False,
        brow="sus" if angry else "n", expr="sus" if (angry and talk(t) == 0) else "n", look=(-1, 0))
    comp(f, chip("CEO", NAVY_, WHITE, 34), 300, 940, op=clamp(u / 0.2))
    comp(f, chip("CO-FOUNDER", INK, WHITE, 34), 780, 920, op=clamp(u / 0.2))
    if t >= ti and not boom:
        comp(f, bubble_el("raise the hot dog price…", 44), 620, 760, scale=pin(t, ti, 0.25))
    ui_word(f, "the ceo wanted to", "RAISE THE PRICE", 470, t, tr, col=INK, size=120, out=ti - 0.05)
    if boom:
        ui_word(f, "if you raise it…", "I WILL KILL YOU!", 470, t, tk, col=RED_, size=150, shadow=0.15)
        if t < tk + 0.12: f = f + np.array(C((255, 60, 40)), np.float32) * 0.35 * (1 - (t - tk) / 0.12)
    return finish(f, n)


# ---- S2c: cheap hot dog -> you trust every price ----
def shot_S2c(t, n):
    f = stage("sky", (255, 255, 255), 600, 980, 430); u = lt(t, "S2c")
    comp(f, scale_el(shelf_el(3, 560, 600), 0.92), 640, 1000, scale=pin(t, SHOT["S2c"]["start"], 0.3))
    tt = T("a3", "trust") - 0.1
    spots = [(470, 860), (690, 860), (520, 1010), (760, 1010), (470, 1160), (700, 1160)]
    for i, (x, y) in enumerate(spots):
        comp(f, tag_el(["$9", "$24", "$5", "$12", "$7", "$30"][i], WHITE, INK, 30), x, y)
        if t >= tt + i * 0.12: comp(f, check_el(26), x + 60, y - 30, scale=pin(t, tt + i * 0.12, 0.2))
    guy(f, 210, 1480, 0.85, la=(18, 8), ra=(60, 150), mouth=talk(t), blink=blink_at(t, 1), expr="n", brow="up", look=(1, -1),
        hold=scale_el(hotdog_el(), 0.3), hold_off=(30, -20))
    ui_word(f, "so you", "TRUST EVERY PRICE", 470, t, tt, col=WHITE, size=140, shadow=0.35)
    return finish(f, n)


# ---- S3a: secret 2 — the $4.99 chicken ----
def shot_S3a(t, n):
    f = stage("purple", (255, 255, 255), 540, 1000, 440); u = lt(t, "S3a")
    title(f, "S3a", t, 2, "THE $4.99 CHICKEN", WHITE, 130)
    comp(f, scale_el(chicken_el(), 1.05), 540, 1010, scale=pin(t, SHOT["S3a"]["start"] + 0.08, 0.3))
    steam(f, 540, 820, t, 1.0, 0.45)
    tf = T("b1", "four") - 0.1
    if t >= tf:
        rot_comp(f, tag_el("$4.99", YEL_, INK, 120), 760, 1260, 8, pin(t, tf, 0.25), 1.0, 0.3)
        if t < tf + 0.1: f = f + 0.2
    return finish(f, n)


# ---- S3b: 150 million a year ----
def shot_S3b(t, n):
    f = stage("purple", YEL_, 540, 1060, 430); u = lt(t, "S3b")
    th = T("b2", "hundred") - 0.15
    ch = scale_el(chicken_el(False), 0.3)
    for j in range(20):
        r_, c_ = divmod(j, 5)
        x = 540 + (c_ - 2) * 160 + (r_ % 2) * 30 - 15; y = 800 + r_ * 135
        t0 = th - 0.5 + 0.04 * (j * 7 % 20)
        if t < t0: continue
        comp(f, ch, x, y, scale=pin(t, t0, 0.2))
    ui_word(f, "costco sells over", "150 MILLION", 470, t, th, col=WHITE, size=170, shadow=0.35, tail="chickens a year")
    if t >= th + 0.4: comp(f, chip("Costco reported 157 million sold in 2025", INK, WHITE, 26), 540, 1420, op=clamp((t - th - 0.4) / 0.3))
    return finish(f, n)


# ---- S3c: store map — the chicken is at the very back ----
AISLES = [250, 420, 590, 760]
PATH = [(540, 1420), (540, 1290), (335, 1290), (335, 760), (505, 760), (505, 1230), (675, 1230), (675, 760), (845, 760), (845, 690)]


def _path_pt(k):
    seg = [math.hypot(PATH[i + 1][0] - PATH[i][0], PATH[i + 1][1] - PATH[i][1]) for i in range(len(PATH) - 1)]
    L = sum(seg) * clamp(k)
    for i, s in enumerate(seg):
        if L <= s: r = L / max(s, 1e-6); return (PATH[i][0] + (PATH[i + 1][0] - PATH[i][0]) * r, PATH[i][1] + (PATH[i + 1][1] - PATH[i][1]) * r), i
        L -= s
    return PATH[-1], len(seg) - 1


def shot_S3c(t, n):
    f = stage("cream", None); u = lt(t, "S3c")
    cv2.rectangle(f, (130, 600), (950, 1400), C((255, 255, 255)), -1, cv2.LINE_AA); cv2.rectangle(f, (130, 600), (950, 1400), C(INK), 8, cv2.LINE_AA)
    cv2.rectangle(f, (470, 1392), (610, 1410), C((255, 255, 255)), -1)
    comp(f, chip("ENTRANCE", INK, WHITE, 26), 540, 1450)
    cols = [(232, 60, 50), (40, 130, 230), (40, 180, 110), (250, 170, 30)]
    for i, x in enumerate(AISLES):
        cv2.rectangle(f, (x - 34, 820), (x + 34, 1200), C(cols[i]), -1, cv2.LINE_AA)
        for yy in range(840, 1200, 40): cv2.line(f, (x - 34, yy), (x + 34, yy), C(tuple(int(v * 0.75) for v in cols[i])), 3)
    tb = T("b3", "back") - 0.12
    glow(f, 845, 670, 90, (255, 220, 120), 0.6 * clamp((t - tb) / 0.3))
    comp(f, scale_el(chicken_el(False), 0.25), 845, 660, scale=1 + 0.15 * math.sin(t * 8) * (t >= tb))
    tw = T("b3", "walk") - 0.3; k = eio(clamp((t - tw) / max(0.5, LINES["b3"]["end"] - tw - 0.1)))
    (px, py), si = _path_pt(k)
    pts = PATH[:si + 1] + [(px, py)]
    for i in range(len(pts) - 1):
        p, q = pts[i], pts[i + 1]; L = math.hypot(q[0] - p[0], q[1] - p[1])
        for s in np.arange(0, L, 26): cv2.circle(f, (int(p[0] + (q[0] - p[0]) * s / L), int(p[1] + (q[1] - p[1]) * s / L)), 6, C(INK), -1, cv2.LINE_AA)
    comp(f, mini_head(46), px, py - 10)
    ui_word(f, "it's way at the", "BACK", 430, t, tb, col=INK, size=170, out=T("b3", "everything") - 0.15)
    ui_word(f, "so you walk past", "EVERYTHING", 430, t, T("b3", "everything") - 0.12, col=RED_, size=150)
    return finish(f, n)


# ---- S4a: secret 3 — markup cap ----
def shot_S4a(t, n):
    f = stage("teal", YEL_, 540, 1000, 430); u = lt(t, "S4a")
    title(f, "S4a", t, 3, "MARKUP CAP", WHITE, 160)
    tc = T("c1", "caps") - 0.12
    grow = eo(clamp(u / 1.0)); top = 1360 - 520 * grow
    if t >= tc: top = max(top, 1360 - 520 * eo(clamp((tc - SHOT["S4a"]["start"]) / 1.0)) + 10)
    arrow(f, (540, 1380), (540, top), GRN_, 60, 120)
    comp(f, chip("PRICE", INK, WHITE, 30), 540, 1420)
    if t >= tc:
        q = clamp((t - tc) / 0.22); y = -150 + (top - 150 + 150) * eo(q)
        comp(f, scale_el(bottlecap_el("MAX"), 0.9), 540, y)
        if q >= 1 and t < tc + 0.32: f = f + 0.15
    return finish(f, n)


# ---- S4b: ~14% on brands, 15% on its own brand -> always a deal ----
def shot_S4b(t, n):
    f = stage("teal", (255, 255, 255), 540, 980, 420); u = lt(t, "S4b")
    t1 = T("c2", "fourteen") - 0.12; t2 = T("c2", "fifteen") - 0.12; td = T("c2", "deal.") - 0.2
    if t >= t1:
        comp(f, chip("BRANDS", INK, WHITE, 32), 300, 700, op=clamp((t - t1) / 0.2))
        rot_comp(f, tag_el("14%", RED_, WHITE, 76), 300, 800, -6, pin(t, t1, 0.25), 1.0, 0.3)
    if t >= t2:
        comp(f, chip("OWN BRAND", INK, WHITE, 32), 780, 700, op=clamp((t - t2) / 0.2))
        rot_comp(f, tag_el("15%", NAVY_, WHITE, 76), 780, 800, 6, pin(t, t2, 0.25), 1.0, 0.3)
    happy = t >= td
    guy(f, 540, 1450, 0.95, la=(150, 165) if happy else (18, 8), ra=(150, 165) if happy else (18, 8), mouth=talk(t), blink=blink_at(t, 2),
        brow="up", expr="n", bob=-18 * abs(math.sin(t * 8)) if happy else 0)
    if happy: rot_comp(f, sign_el("DEAL!", YEL_, INK, 70, False), 540, 860, -5, pin(t, td, 0.25), 1.0, 0.3)
    ui_word(f, "markups capped at", "14-15%", 470, t, t1, col=WHITE, size=170, shadow=0.35, out=td - 0.05)
    ui_word(f, "you always feel like you're getting a", "DEAL", 470, t, td, col=YEL_, size=190, shadow=0.35, lead_col=WHITE)
    return finish(f, n)


# ---- S5a: secret 4 — the genius one ----
def shot_S5a(t, n):
    f = stage("emerald", GOLD, 540, 1000, 430); u = lt(t, "S5a")
    rays(f, 540, 1000, 700, (255, 236, 150), 0.5 * clamp(u / 0.3), t)
    tg = T("d1", "genius") - 0.1
    k = clamp((t - tg) / 0.3)
    rot_comp(f, folder_el(4, True, "GENIUS"), 540, 1010, 4 * math.sin(t * 20) * math.exp(-max(0, t - tg) * 3) * (t >= tg),
             pin(t, SHOT["S5a"]["start"] + 0.05, 0.3) * (1.25 + 0.15 * k), 1.0, 0.35)
    for i in range(8):
        a = i * math.pi / 4 + t * 1.5; r = 380 + 30 * math.sin(t * 4 + i)
        cv2.circle(f, (int(540 + r * math.cos(a)), int(1010 + r * math.sin(a))), 7, C((255, 250, 210)), -1, cv2.LINE_AA)
    ui_word(f, "SECRET 4", "THE GENIUS ONE", 470, t, SHOT["S5a"]["start"] + 0.05, col=YEL_, size=150, shadow=0.35, lead_col=WHITE)
    return finish(f, n)


# ---- S5b: the real product isn't in the store — it's this card ----
def shot_S5b(t, n):
    f = stage("purple", None); u = lt(t, "S5b")
    ti = T("d2", "isn't") - 0.1; tc = T("d2", "card.") - 0.25
    ko = eio(clamp((t - ti) / 0.5))
    sh = scale_el(shelf_el(5, 460, 640), 0.95)
    comp(f, sh, 250 - 420 * ko, 1000, op=1 - 0.6 * ko); comp(f, flip_h(sh), 830 + 420 * ko, 1000, op=1 - 0.6 * ko)
    if t >= ti and t < tc + 0.1:
        comp(f, check_el(70, False), 540, 1000, scale=pin(t, ti, 0.25), op=clamp((tc + 0.1 - t) / 0.15))
    if t >= tc:
        q = clamp((t - tc) / 0.45)
        rays(f, 540, 1000, 760, (255, 220, 120), 0.6 * q, t)
        el = flipx(member_card_el(), math.cos((1 - eo(q)) * math.pi * 2))
        comp(f, el, 540, 1000, scale=0.6 + 0.55 * eo(q))
    ui_word(f, "costco's real product", "ISN'T IN THE STORE", 470, t, SHOT["S5b"]["start"] + 0.05, col=WHITE, size=120, shadow=0.3, out=tc - 0.05)
    ui_word(f, "it's", "THIS CARD", 470, t, tc, col=YEL_, size=190, shadow=0.35, lead_col=WHITE)
    return finish(f, n)


# ---- S5c: ~$5.9B in fees ≈ half of operating profit ----
def shot_S5c(t, n):
    f = stage("emerald", GOLD, 540, 1020, 420); u = lt(t, "S5c")
    ts = T("d3", "six") - 0.15; th = T("d3", "half") - 0.2; tthat = T("d3", "That's") - 0.1
    if t < tthat + 0.1:
        op = clamp((tthat + 0.1 - t) / 0.2)
        comp(f, scale_el(member_card_el(), 0.5), 540, 1290, op=op)
        for i in range(10):
            q = u - 0.1 * i
            if q <= 0: continue
            y = min(1120 - (i // 2) * 60, -200 + 1800 * q * q); x = 540 + (-110 if i % 2 else 110)
            rot_comp(f, scale_el(cash_el(), 0.62), x, y, (-1) ** i * 5, 1.0, op, 0.25)
        ui_word(f, "membership fees: almost", "$6 BILLION", 470, t, ts, col=YEL_, size=180, shadow=0.35, lead_col=WHITE, out=tthat)
    else:
        k = eio(clamp((t - th) / 0.6)); cx, cy, r = 540, 1030, 300
        cv2.circle(f, (cx + 8, cy + 14), r, C((0, 40, 20)), -1, cv2.LINE_AA)
        cv2.circle(f, (cx, cy), r, C((60, 190, 110)), -1, cv2.LINE_AA)
        if k > 0: cv2.ellipse(f, (cx, cy), (r, r), -90, 0, 182 * k, C(YEL_), -1, cv2.LINE_AA)
        cv2.circle(f, (cx, cy), r, C((255, 255, 255)), 8, cv2.LINE_AA)
        if k > 0.6:
            comp(f, ed_el("FEES", "", lead_col=INK, lead_size=56), cx + 140, cy, op=clamp((k - 0.6) / 0.3))
            comp(f, ed_el("everything else", "", lead_col=WHITE, lead_size=36), cx - 150, cy, op=clamp((k - 0.6) / 0.3))
        ui_word(f, "that's about", "HALF THE PROFIT", 470, t, th, col=YEL_, size=150, shadow=0.35, lead_col=WHITE)
        comp(f, chip("Costco FY2026: $5.9B fees vs $11.7B operating income", INK, WHITE, 24), 540, 1420, op=clamp((t - th - 0.3) / 0.3))
    return finish(f, n)


# ---- S5d: 9 in 10 renew ----
def shot_S5d(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 440); u = lt(t, "S5d")
    tn = T("d4", "nine") - 0.15
    for j in range(10):
        r_, c_ = divmod(j, 5); x = 260 + c_ * 140; y = 900 + r_ * 200
        lit = j != 7
        t0 = tn + 0.06 * j
        on = t >= t0
        comp(f, mini_head(60, lit or not on), x, y, scale=pin(t, SHOT["S5d"]["start"] + 0.04 * j, 0.2))
        if on: comp(f, check_el(24, lit), x + 46, y - 50, scale=pin(t, t0, 0.2))
    if t >= tn + 0.6:
        a = (t - tn) * 220; cv2.ellipse(f, (540, 1000), (400, 300), 0, a, a + 300, C(GRN_), 14, cv2.LINE_AA)
    ui_word(f, "every year,", "9 IN 10 RENEW", 470, t, tn, col=WHITE, size=160, shadow=0.35)
    return finish(f, n)


# ---- S6: the hot dog is an ad... for the card ----
def shot_S6(t, n):
    f = stage("red", YEL_, 540, 1000, 440); u = lt(t, "S6")
    ta = T("e1", "ad…") - 0.15; tc = T("e1", "card.") - 0.2
    hx = 540 - 170 * eo(clamp((t - tc) / 0.4))
    if t >= ta: rot_comp(f, sign_el("AD", WHITE, RED_, 110), hx + 10, 880, -8 + 6 * math.sin((t - ta) * 9) * math.exp(-(t - ta) * 3), pin(t, ta, 0.3), 1.0, 0.3)
    comp(f, scale_el(hotdog_el(), 0.95 - 0.25 * eo(clamp((t - tc) / 0.4))), hx, 1080 + 6 * math.sin(t * 3))
    if t >= tc:
        q = eo(clamp((t - tc) / 0.4))
        arrow(f, (hx + 120, 1080), (hx + 120 + 140 * q, 1080), INK, 16, 40)
        comp(f, scale_el(member_card_el(), 0.55), 760 + 400 * (1 - q), 1080)
    ui_word(f, "that hot dog isn't food", "", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, out=ta - 0.05)
    ui_word(f, "it's an", "AD", 470, t, ta, col=WHITE, size=200, shadow=0.35, out=tc - 0.05)
    ui_word(f, "an ad for", "THE CARD", 470, t, tc, col=WHITE, size=180, shadow=0.35)
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("orange", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("costco run?", "already here lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(hotdog_el(), 0.32), hold_off=(20, -30))
        ui_word(f, "send this to the friend who", "LIVES AT COSTCO", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=110, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "dollar") - 0.12, 0.3, 14), (T("i2", "forty") - 0.1, 0.25, 8), (T("i4", "genius.") - 0.15, 0.3, 10),
           (T("a2", "kill") - 0.15, 0.4, 22), (T("b1", "four") - 0.1, 0.25, 8), (T("c1", "caps") + 0.1, 0.3, 14),
           (T("d2", "card.") - 0.05, 0.3, 10), (T("d3", "half") - 0.2, 0.25, 8), (T("e1", "ad…") - 0.15, 0.3, 12)]


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
