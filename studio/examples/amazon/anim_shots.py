# ================= shots: "Amazon's real money machine is AWS" =================
def flip_h(el): return el[0][:, ::-1].copy(), el[1][:, ::-1].copy()


SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i2", "Nope!") - 0.12, "punch"), ("S1", T("i3", "Let's") - 0.15, "whip"),
    ("S2a", T("a1", "First,") - 0.25, "whip"), ("S2b", T("a2", "But") - 0.12, "focus"), ("S2c", T("a3", "That's") - 0.12, "zoom"),
    ("S3a", T("b1", "Now") - 0.25, "flash"), ("S3b", T("b2", "Amazon") - 0.12, "focus"), ("S3c", T("b3", "In") - 0.12, "whip"),
    ("S3d", T("b4", "That's") - 0.12, "zoom"), ("S4a", T("c1", "Here's") - 0.2, "flash"), ("S4b", T("c2", "The") - 0.12, "focus"),
    ("S5a", T("d1", "And") - 0.2, "whip"), ("S5b", T("d2", "Almost") - 0.12, "zoom"), ("S6", T("e1", "So") - 0.2, "whip"),
    ("S7", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC = "Source: Amazon Q2 2026 results (Apr-Jun 2026)"


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


# ---- S0: hook — parcels drop: does Amazon make money selling stuff? ----
def shot_S0(t, n):
    f = stage("sky", YEL_, 540, 980, 440)
    cv2.rectangle(f, (120, 1300), (960, 1330), C((255, 255, 255)), -1, cv2.LINE_AA)
    contact(f, 600, 1300, 600, 0.3)
    for x, y_end, s_, t0 in ((450, 1160, 1.0, 0.05), (770, 1195, 0.75, 0.2), (470, 940, 0.62, 0.38)):
        y = drop(t, t0, y_end)
        if y is not None: comp(f, scale_el(box_el(), s_), x, y)
    ts = T("i1", "selling") - 0.1
    if t >= ts:
        rot_comp(f, tag_el("$", YEL_, INK, 110), 720, 800, 10, pin(t, ts, 0.25), 1.0, 0.35)
        comp(f, ed_el("", "?", big_col=WHITE, big_size=150, shadow=0.3), 860, 800 + 10 * math.sin(t * 5), op=clamp((t - ts - 0.2) / 0.2))
    guy(f, 820, 1490, 0.62, la=(18, 8), ra=(40, 160), mouth=talk(t), blink=blink_at(t, 1), brow="sus", look=(-1, -1),
        expr="sus" if talk(t) == 0 else "n")
    ui_word(f, "does amazon make money by", "SELLING STUFF?", 470, t, T("i1", "Amazon") - 0.12, col=WHITE, size=140, shadow=0.35)
    return finish(cam(f, 1.0 + 0.02 * t, W / 2, 1000), n)


# ---- S0b: NOPE — profit comes from something hidden ----
def shot_S0b(t, n):
    f = stage("red", (255, 220, 120), 540, 1000, 430); u = lt(t, "S0b")
    tn = SHOT["S0b"]["start"] + 0.05
    comp(f, scale_el(box_el(), 0.85), 330, 1080)
    rot_comp(f, stamp_el("NOPE", WHITE, 100), 330, 1080, -12, 1.6 - 0.6 * eo(clamp((t - tn) / 0.18)), clamp((t - tn) / 0.1), 0.3)
    tm = T("i2", "never") - 0.15
    if t >= tm:
        k = pin(t, tm, 0.3)
        glow(f, 750, 1060, 230, (255, 230, 150), 0.5 * clamp((t - tm) / 0.3))
        comp(f, scale_el(cloud_el((40, 40, 56), 340, 200), 1.0), 750, 1070, scale=k)
        comp(f, ed_el("", "?", big_col=YEL_, big_size=130), 750, 1070, op=clamp((t - tm - 0.1) / 0.2))
    ui_word(f, "most of its profit comes from", "SOMETHING HIDDEN", 470, t, T("i2", "Most") - 0.1, col=WHITE, size=130, shadow=0.35)
    return finish(f, n)


# ---- S1: let's follow the money (cash trail + magnifier) ----
TRAIL = [(170, 1380), (330, 1240), (260, 1080), (470, 980), (690, 1080), (850, 950), (740, 800)]


def shot_S1(t, n):
    f = stage("emerald", GOLD, 540, 1000, 420); u = lt(t, "S1")
    k = eio(clamp(u / 1.3)); m = len(TRAIL) - 1; pos = k * m; i0 = min(int(pos), m - 1); r = pos - i0
    px = TRAIL[i0][0] + (TRAIL[i0 + 1][0] - TRAIL[i0][0]) * r; py = TRAIL[i0][1] + (TRAIL[i0 + 1][1] - TRAIL[i0][1]) * r
    for j, (x, y) in enumerate(TRAIL[:-1]):
        if j <= pos: comp(f, scale_el(cash_el(), 0.32), x, y, scale=pin(t, SHOT["S1"]["start"] + 0.18 * j, 0.2))
    comp(f, magnifier_el(), px + 40, py - 40)
    guy(f, 860, 1490, 0.7, la=(18, 8), ra=(40, 160), mouth=talk(t), blink=blink_at(t, 2), brow="up", look=(-1, -1), expr="smirk" if talk(t) == 0 else "n")
    ui_word(f, "let's follow the", "MONEY", 470, t, T("i3", "follow") - 0.15, col=YEL_, size=190, shadow=0.35, lead_col=WHITE)
    return finish(cam(f, 1.05 - 0.05 * eo(clamp(u / 1.4)), W / 2, 1000), n)


# ---- S2a: the shopping side — conveyor of parcels, $150B+ ----
def shot_S2a(t, n):
    f = stage("orange", YEL_, 540, 900, 400); u = lt(t, "S2a")
    cv2.rectangle(f, (0, 1180), (W, 1230), C((60, 62, 74)), -1, cv2.LINE_AA)
    for j in range(15): cv2.circle(f, (int(((j * 75 + u * 160) % 1125) - 20), 1205), 14, C((150, 154, 170)), -1, cv2.LINE_AA)
    for j in range(6):
        x = -150 + ((j * 230 + u * 160) % 1380)
        s_ = 0.5 + 0.08 * (j % 2)
        comp(f, scale_el(box_el(), s_), x, 1180 - 140 * s_)
    tb = T("a1", "hundred") - 0.15
    ui_word(f, "first,", "THE SHOPPING SIDE", 470, t, SHOT["S2a"]["start"] + 0.08, col=WHITE, size=120, shadow=0.35, out=tb - 0.05)
    if t >= tb:
        ui_word(f, "april to june, sales of over", "$150 BILLION", 470, t, tb, col=WHITE, size=160, shadow=0.35)
        comp(f, chip(SRC, INK, WHITE, 24), 540, 1430, op=clamp((t - tb - 0.3) / 0.3))
    return finish(f, n)


# ---- S2b: sales tower vs tiny profit ----
def shot_S2b(t, n):
    f = stage("cream", (255, 170, 60), 540, 1000, 420); u = lt(t, "S2b")
    base = 1340; hs = 560 * eo(clamp(u / 0.6)); tp = T("a2", "eleven") - 0.15
    cv2.rectangle(f, (220, int(base - hs)), (440, base), C((255, 140, 50)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (220, int(base - hs)), (440, base), C(INK), 6, cv2.LINE_AA)
    comp(f, chip("SALES $158B", INK, WHITE, 30), 330, base + 50)
    if t >= tp:
        hp = 39 * eo(clamp((t - tp) / 0.4))
        cv2.rectangle(f, (640, int(base - hp)), (860, base), C(GRN_), -1, cv2.LINE_AA)
        cv2.rectangle(f, (640, int(base - hp)), (860, base), C(INK), 6, cv2.LINE_AA)
        comp(f, chip("PROFIT $10.8B", GRN_, WHITE, 30), 750, base + 50, scale=pin(t, tp, 0.25))
        arrow(f, (750, base - 300), (750, base - 80), RED_, 16, 44)
    ui_word(f, "but the profit?", "ONLY $11B", 470, t, T("a2", "profit?") - 0.1, col=INK, size=170)
    return finish(f, n)


# ---- S2c: under 7 cents of every dollar (100-cent grid) ----
def shot_S2c(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1010, 420); u = lt(t, "S2c")
    ts = T("a3", "seven") - 0.15
    cents_grid(f, 540, 1010, 7, GRN_, 44, 8, eo(clamp((t - ts) / 0.4)) if t >= ts else 0, dim=(255, 250, 235))
    comp(f, chip("$1 = 100 CENTS", INK, WHITE, 30), 540, 1320, op=clamp(u / 0.2))
    ui_word(f, "profit: less than", "7 CENTS PER $1", 470, t, ts, col=INK, size=140)
    if t >= ts + 0.4: guy(f, 880, 1490, 0.55, la=(30, 20), ra=(30, 20), mouth=0, expr="wow", brow="up", look=(-1, -1))
    return finish(f, n)


# ---- S3a: the secret — AWS server racks rise in light ----
def shot_S3a(t, n):
    f = stage("purple", (120, 200, 255), 540, 1000, 450); u = lt(t, "S3a")
    rays(f, 540, 1040, 760, (140, 200, 255), 0.55 * clamp(u / 0.4), t)
    for i, x in enumerate((330, 540, 750)):
        k = eo(clamp((u - 0.1 - 0.12 * i) / 0.45))
        if k <= 0: continue
        comp(f, rack_el(int(t * 6) + i, 200, 460), x, 1460 - 340 * k, op=k)
    ui_word(f, "the secret", "AWS", 470, t, SHOT["S3a"]["start"] + 0.06, col=WHITE, size=220, shadow=0.4, lead_col=WHITE)
    tw = T("b1", "Web") - 0.2
    if t >= tw: comp(f, chip("AMAZON WEB SERVICES", INK, WHITE, 40), 540, 640, scale=pin(t, tw, 0.25))
    return finish(f, n)


# ---- S3b: rents computers to other companies over the internet ----
def shot_S3b(t, n):
    f = stage("sky", (255, 255, 255), 540, 930, 330); u = lt(t, "S3b")
    comp(f, scale_el(cloud_el(), 0.8), 540, 930 + 8 * math.sin(t * 2))
    for i, x in enumerate((390, 540, 690)): comp(f, rack_el(int(t * 5) + i, 140, 300), x, 1250)
    tw = T("b2", "warehouses") - 0.1
    if t >= tw: comp(f, chip("DATA CENTERS", INK, WHITE, 30), 540, 1440, scale=pin(t, tw, 0.25))
    to = T("b2", "other") - 0.15
    blds = [(170, 770, (240, 90, 80)), (890, 770, (60, 180, 120)), (170, 1200, (250, 170, 40)), (890, 1200, (130, 90, 230))]
    for i, (x, y, col) in enumerate(blds):
        t0 = to + 0.1 * i
        if t < t0: continue
        k = eo(clamp((t - t0) / 0.3)); p = (540 + (x - 540) * 0.3, 960 + (y - 960) * 0.3)
        for s in np.linspace(0, 0.75, 10):
            if s <= 0.75 * k: cv2.circle(f, (int(p[0] + (x - p[0]) * s), int(p[1] + (y - p[1]) * s)), 6, C(WHITE), -1, cv2.LINE_AA)
        comp(f, scale_el(building_el(col), 0.62), x, y, scale=pin(t, t0 + 0.2, 0.25))
    ui_word(f, "renting computers to", "OTHER COMPANIES", 470, t, T("b2", "rents") - 0.12, col=INK, size=130)
    return finish(f, n)


# ---- S3c: $42B sales, $16B+ profit ----
def shot_S3c(t, n):
    f = stage("teal", YEL_, 540, 1000, 430); u = lt(t, "S3c")
    t1 = T("b3", "forty-two") - 0.15; t2 = T("b3", "sixteen") - 0.15
    comp(f, rack_el(int(t * 6), 200, 460), 540, 1050, op=0.3)
    if t >= t1:
        comp(f, chip("AWS SALES", INK, WHITE, 34), 540, 800, op=clamp((t - t1) / 0.2))
        rot_comp(f, tag_el("$42.2B", WHITE, INK, 110), 540, 930, -4, pin(t, t1, 0.25), 1.0, 0.3)
    if t >= t2:
        comp(f, chip("AWS PROFIT", INK, WHITE, 34), 540, 1100, op=clamp((t - t2) / 0.2))
        rot_comp(f, tag_el("$16.6B", YEL_, INK, 130), 540, 1240, 5, pin(t, t2, 0.25), 1.0, 0.35)
        if t < t2 + 0.1: f = f + 0.2
        comp(f, chip(SRC, INK, WHITE, 24), 540, 1430, op=clamp((t - t2 - 0.3) / 0.3))
    ui_word(f, "same three months", "THE CLOUD", 470, t, SHOT["S3c"]["start"] + 0.05, col=WHITE, size=130, shadow=0.35, lead_col=WHITE)
    return finish(f, n)


# ---- S3d: split screen — store 7 cents vs cloud 39 cents ----
def shot_S3d(t, n):
    f = stage("cream", None); u = lt(t, "S3d")
    f[:, :540] = f[:, :540] * 0.35 + np.array(C((255, 140, 60)), np.float32) * 0.65
    f[:, 540:] = f[:, 540:] * 0.35 + np.array(C((40, 110, 230)), np.float32) * 0.65
    cv2.line(f, (540, 600), (540, 1480), C(WHITE), 8, cv2.LINE_AA)
    tf = T("b4", "forty") - 0.15
    cents_grid(f, 300, 1050, 7, GRN_, 26, 6, 1.0, dim=(255, 236, 214))
    cents_grid(f, 780, 1050, 39, YEL_, 26, 6, eo(clamp((t - tf) / 0.6)) if t >= tf else 0, dim=(200, 220, 255))
    comp(f, chip("STORE: 7 CENTS", INK, WHITE, 30), 300, 1290)
    if t >= tf: comp(f, chip("CLOUD: 39 CENTS", INK, YEL_, 30), 780, 1290, scale=pin(t, tf + 0.3, 0.25))
    comp(f, scale_el(box_el(), 0.42), 300, 800); comp(f, scale_el(cloud_el(), 0.4), 780, 800)
    ui_word(f, "profit per dollar:", "ALMOST 40 CENTS", 470, t, tf, col=WHITE, size=120, shadow=0.45, lead_col=WHITE)
    comp(f, chip("Operating income per $1 of sales, Q2 2026", INK, WHITE, 24), 540, 1430, op=clamp((t - tf - 0.4) / 0.3))
    return finish(f, n)


# ---- S4a: here's the twist ----
def shot_S4a(t, n):
    f = stage("yellow", RED_, 540, 1010, 370); u = lt(t, "S4a")
    rot_comp(f, ed_el("", "TWIST", big_col=WHITE, big_size=190, shadow=0.4), 540, 1000, -6 + 4 * math.sin(t * 18) * math.exp(-u * 3),
             pin(t, SHOT["S4a"]["start"] + 0.05, 0.3), 1.0, 0.0)
    guy(f, 540, 1490, 0.75, la=(150, 165), ra=(150, 165), mouth=talk(t), expr="wow" if talk(t) == 0 else "n", brow="up", look=(0, -1),
        bob=-12 * abs(math.sin(t * 8)))
    ui_word(f, "here's the", "", 540, t, SHOT["S4a"]["start"] + 0.05, col=INK, lead_col=INK)
    return finish(f, n)


# ---- S4b: two pies — 1/5 of sales, 6/10 of profit ----
def shot_S4b(t, n):
    f = stage("pink", (255, 255, 255), 540, 1000, 440); u = lt(t, "S4b")
    tf = T("c2", "fifth") - 0.15; ts = T("c3", "six") - 0.15
    comp(f, chip("SALES", INK, WHITE, 32), 300, 790)
    pie(f, 300, 1010, 170, 0.21, (40, 120, 230), (255, 255, 255), eio(clamp((t - tf) / 0.5)) if t >= tf else 0)
    if t >= tf: comp(f, chip("CLOUD 21%", (40, 120, 230), WHITE, 30), 300, 1230, scale=pin(t, tf + 0.3, 0.25))
    if t >= ts - 0.4:
        comp(f, chip("PROFIT", INK, WHITE, 32), 780, 790, op=clamp((t - ts + 0.4) / 0.2))
        pie(f, 780, 1010, 170, 0.605, (40, 120, 230), (255, 255, 255), eio(clamp((t - ts) / 0.6)) if t >= ts else 0)
        if t >= ts: comp(f, chip("CLOUD 60%", (40, 120, 230), WHITE, 30), 780, 1230, scale=pin(t, ts + 0.4, 0.25))
    ui_word(f, "the cloud is only", "1/5 OF SALES", 470, t, tf, col=WHITE, size=150, shadow=0.35, out=ts - 0.1)
    ui_word(f, "but", "60% OF PROFIT", 470, t, ts, col=YEL_, size=150, shadow=0.4, lead_col=WHITE)
    comp(f, chip("Q2 2026: AWS $42.2B of $200.6B sales; $16.6B of $27.5B op. income", INK, WHITE, 21), 540, 1430,
         op=clamp((t - ts - 0.4) / 0.3))
    return finish(f, n)


# ---- S5a: secret 2 — ads (search results marked SPONSORED) ----
def shot_S5a(t, n):
    f = stage("purple", (255, 120, 180), 540, 1000, 440); u = lt(t, "S5a")
    tsp = T("d1", "sponsored") - 0.1
    ph = scale_el(search_phone_el(), 0.78); px, py = 610, 1070
    comp(f, ph, px, py, scale=pin(t, SHOT["S5a"]["start"] + 0.05, 0.3))
    if t >= tsp:
        a = 0.5 + 0.5 * math.sin((t - tsp) * 10)
        for i in range(2):
            cx = int(px + (279 - 220) * 0.78); cy = int(py + (180 + i * 190 + 134 - 400) * 0.78)
            cv2.ellipse(f, (cx, cy), (90, 30), 0, 0, 360, C(RED_), int(4 + 4 * a), cv2.LINE_AA)
    ui_word(f, "secret number two", "ADS", 470, t, T("d1", "Ads!") - 0.12, col=YEL_, size=210, shadow=0.4, lead_col=WHITE)
    guy(f, 200, 1490, 0.62, la=(18, 8), ra=(70, 120), mouth=talk(t), blink=blink_at(t, 3), brow="sus", look=(1, -1),
        expr="smirk" if talk(t) == 0 else "n")
    return finish(f, n)


# ---- S5b: almost $20B in ad sales in three months ----
def shot_S5b(t, n):
    f = stage("orange", YEL_, 540, 1000, 430); u = lt(t, "S5b")
    coin_rain(f, t, SHOT["S5b"]["start"], 12, 540, 330, 1500, 3)
    tt = T("d2", "twenty") - 0.15
    if t >= tt:
        rot_comp(f, tag_el("$19.8B", WHITE, INK, 130), 540, 1040, -5, pin(t, tt, 0.25), 1.0, 0.35)
        comp(f, chip("AD SALES, APR-JUN 2026", INK, WHITE, 32), 540, 1190, op=clamp((t - tt - 0.2) / 0.2))
        comp(f, chip(SRC, INK, WHITE, 24), 540, 1430, op=clamp((t - tt - 0.4) / 0.3))
    ui_word(f, "in just three months", "ALMOST $20B", 470, t, tt, col=WHITE, size=160, shadow=0.35)
    return finish(f, n)


# ---- S6: the store brings you in, the cloud pays the bills ----
def shot_S6(t, n):
    f = stage("emerald", GOLD, 540, 980, 430); u = lt(t, "S6")
    tc = T("e1", "cloud") - 0.15; tb = T("e1", "bills.") - 0.15
    comp(f, scale_el(box_el(), 0.7), 300, 1150, scale=pin(t, SHOT["S6"]["start"] + 0.05, 0.25))
    comp(f, chip("THE STORE", INK, WHITE, 28), 300, 1300, op=clamp(u / 0.3))
    if t >= tc:
        k = eo(clamp((t - tc) / 0.4))
        if t >= tb:
            for i in range(6):
                q = t - tb - 0.1 * i
                if q > 0: rot_comp(f, scale_el(cash_el(), 0.32), 640 + 50 * i, 900 + (q * 500) % 420, 15 * math.sin(q * 6 + i), 1.0, 1.0, 0.2)
        comp(f, scale_el(cloud_el((240, 248, 255)), 0.7), 760, 870, scale=k)
        comp(f, chip("THE CLOUD", INK, WHITE, 28), 760, 1000, op=k)
    ui_word(f, "the store", "BRINGS YOU IN", 470, t, SHOT["S6"]["start"] + 0.1, col=WHITE, size=150, shadow=0.35, lead_col=WHITE, out=tc)
    ui_word(f, "the cloud", "PAYS THE BILLS", 470, t, tc, col=YEL_, size=150, shadow=0.35, lead_col=WHITE)
    guy(f, 820, 1490, 0.6, la=(18, 8), ra=(150, 170), mouth=talk(t), expr="smirk" if talk(t) == 0 else "n", brow="up", look=(-1, -1))
    return finish(f, n)


# ---- S7: send it + brand sting ----
def shot_S7(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S7")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("amazon is just a shop", "watch this lol", pr), 0.82), 600, 950, scale=pin(t, SHOT["S7"]["start"]))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(box_el(), 0.3), hold_off=(20, -30))
        ui_word(f, "send this to the friend who thinks", "IT'S JUST A SHOP", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=110, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "selling") - 0.1, 0.25, 10), (SHOT["S0b"]["start"] + 0.2, 0.3, 16), (T("a1", "hundred") - 0.15, 0.25, 8),
           (T("a2", "eleven") - 0.15, 0.25, 8), (SHOT["S3a"]["start"] + 0.1, 0.3, 12), (T("b3", "sixteen") - 0.15, 0.3, 14),
           (SHOT["S4a"]["start"] + 0.08, 0.3, 14), (T("c3", "six") - 0.15, 0.3, 12), (T("d1", "Ads!") - 0.12, 0.3, 12),
           (T("d2", "twenty") - 0.15, 0.25, 10), (T("e1", "bills.") - 0.15, 0.25, 10)]


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
