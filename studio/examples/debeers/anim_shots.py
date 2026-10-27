# ================= shots: "Diamonds aren't as rare as their price: how De Beers sold 'forever'" =================
# Sources: Al Jazeera (14 Sep 2025): ~90% of world supply, stockpiling/controlled release, 1940 10% -> 1980 ~80% of US brides,
#          1980s "two months' salary" ads; National Geographic ("up to 90 percent"); De Beers (Feb 2026): slogan written 1947;
#          NPR (2013): Ad Age slogan of the century; Anglo American FY2025 results (Feb 2026): 21.7 Mct produced, underlying EBITDA -$511M;
#          JCK (Aug 2026, Edahn Golan): lab-grown wholesale index -96% since 2018; National Jeweler (May 2025): Lightbox $800/ct, closing;
#          CNBC Africa (Jul 2026): De Beers for sale since May 2024.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "Because") - 0.2, "punch"), ("S2", T("i3", "Here's") - 0.2, "whip"),
    ("S3", T("a1", "Move") - 0.2, "flash"), ("S4", T("a2", "At") - 0.2, "whip"), ("S5", T("a3", "It") - 0.2, "focus"),
    ("S5b", T("a3", "Scarcity") - 0.15, "punch"), ("S6", T("a4", "Even") - 0.2, "whip"), ("S6b", T("a4", "Not") - 0.15, "punch"),
    ("S7", T("b1", "Move") - 0.2, "flash"), ("S8", T("b2", "In") - 0.2, "focus"), ("S9", T("b3", "So") - 0.2, "whip"),
    ("S9b", T("b3", "And") - 0.15, "zoom"), ("S10", T("b4", "A") - 0.25, "focus"), ("S11", T("b5", "Ad") - 0.2, "punch"),
    ("S11b", T("b5", "By") - 0.15, "whip"), ("S12", T("c1", "And") - 0.2, "flash"), ("S12b", T("c1", "Tell") - 0.15, "punch"),
    ("S13", T("c2", "In") - 0.2, "whip"), ("S13b", T("c2", "two") - 0.15, "punch"), ("S14", T("c3", "A") - 0.2, "focus"),
    ("S15", T("d1", "But") - 0.2, "flash"), ("S16", T("d2", "Labs") - 0.2, "whip"), ("S16b", T("d2", "Same") - 0.15, "punch"),
    ("S17", T("d3", "And") - 0.2, "zoom"), ("S18", T("d4", "Even") - 0.2, "whip"), ("S18b", T("d4", "Then") - 0.15, "punch"),
    ("S19", T("d5", "Last") - 0.2, "focus"), ("S19b", T("d5", "Now") - 0.15, "whip"), ("S20", T("t1", "So") - 0.2, "flash"),
    ("S20b", T("t1", "Not") - 0.15, "punch"), ("S21", T("t2", "Before") - 0.2, "whip"), ("S22", T("e1", "Because") - 0.2, "focus"),
    ("S23", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_AJ = "Sources: Al Jazeera (Sep 2025), National Geographic"
SRC_AA = "Source: Anglo American 2025 results (Feb 2026)"


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", fp_big=None):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, fp_big=fp_big)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, out=None, col=YEL_, size=220, tail="", y=470):
    ui_word(f, lead, big, y, t, t0, col=col, size=size, shadow=0.45, lead_col=WHITE, out=out, tail=tail)


def iui(f, lead, big, t, t0, size=200, tail="", y=470, col=INK, acc=RED_):   # ink caption for cream / yellow sets
    ui_word(f, lead, big, y, t, t0, col=col, size=size, shadow=0.0, lead_col=INK, tail=tail, acc=acc)


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


def spot(f, x, y, rx, ry, amt=0.35):
    """theatre spotlight: darken outside an ellipse, lift inside a touch"""
    m = gcache(("spot", x, y, rx, ry), lambda: np.exp(-(((_xx - x) / rx) ** 2 + ((_yy - y) / ry) ** 2)).astype(np.float32)[..., None])
    f *= (1 - amt * 0.55 * (1 - m)); f += m * amt * 0.06


def brides(f, cx, cy, lit, t, t0=-9, s=1.0, cols=5, gap=172):
    for i in range(10):
        r, c = divmod(i, cols); x = cx + (c - (cols - 1) / 2) * gap * s; y = cy + r * 310 * s
        on = i < lit and t >= t0 + 0.12 * i
        bride_icon(f, x, y, 2.1 * s, on, t)


# ---- the hook composition (frame 1 and the loop-back frame): a ring on a velvet pillow under a spotlight, a price tag swinging ----
def hook_set(f, t, tag=True):
    spot(f, 540, 1150, 420, 520, 0.5)
    rays(f, 540, 1020, 620, (255, 250, 230), 0.22, t, 18)
    comp(f, pillow_el(600), 540, 1330)
    bob = 6 * math.sin(t * 2.0)
    rot_comp(f, ring_el(430), 540, 1080 + bob, 2 * math.sin(t * 1.3), 1.0, 1.0, 0.35)
    for j, (x, y, r) in enumerate(((430, 880, 34), (660, 930, 28), (600, 820, 22), (470, 1010, 18))):
        sparkle(f, x, y + bob, r, t, j * 1.7)
    if tag: swing_tag(f, hangtag_el("2 MONTHS'", "SALARY", 300), 760, 760, t, 7, 90)


def shot_S0(t, n):
    f = stage("purple", (255, 190, 80), 540, 1080, 360)
    hook_set(f, t)
    tt = T("i1", "two") - 0.2
    if t >= tt: rays(f, 840, 1000, 360, (255, 230, 120), 0.4 * clamp((t - tt) / 0.3), t)
    wui(f, "why does a tiny rock cost", "2 MONTHS' PAY?", t, -0.5, col=YEL_, size=190)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1080), n)


# ---- S1: one company spent a century making it look rare — a RARE label stuck on the gem ----
def shot_S1(t, n):
    f = stage("teal", (255, 230, 150), 540, 1060, 430); u = lt(t, "S1")
    comp(f, gem_el(420), 600, 1120 + 6 * math.sin(t * 2), scale=pin(t, st_("S1"), 0.3))
    guy(f, 230, 1490, 0.72, la=(30, 20), ra=(100, 50), mouth=talk(t), blink=blink_at(t, 2), brow="sus", look=(1, -1),
        expr="sus" if talk(t) == 0 else "smirk", hold=scale_el(sign_el("100 YEARS", YEL_, INK, 44, pole=False), 0.9), hold_off=(40, -50))
    tr = T("i2", "rare") - 0.15
    if t >= tr:
        slam(f, stamp_el("RARE*", RED_, 96), 620, 1110, -12, t, tr)
        comp(f, chip("*marketing", INK, WHITE, 30), 700, 1330, op=clamp((t - tr - 0.5) / 0.3))
    wui(f, "a century of making it look", "RARE", t, st_("S1") + 0.06, col=YEL_, size=250)
    return finish(f, n)


# ---- S2: the trick in three moves — three cards flip in ----
def shot_S2(t, n):
    f = stage("orange", (255, 230, 140), 540, 1050, 430); u = lt(t, "S2")
    for i in range(3):
        k = clamp((u - 0.25 - 0.18 * i) / 0.3); sx = abs(math.cos(math.pi * (1 - k))) if k < 1 else 1.0
        if k <= 0: continue
        x = 240 + 300 * i
        el2 = scale_el(folder_el(str(i + 1), i == 2, "MOVE"), 0.95); pm, a = el2; w_ = max(2, int(a.shape[1] * sx))
        comp(f, (cv2.resize(pm, (w_, a.shape[0])), cv2.resize(a, (w_, a.shape[0]))), x, 1120 + 10 * math.sin(t * 3 + i))
    wui(f, "here's the trick, in", "3 MOVES", t, st_("S2") + 0.06, col=WHITE, size=250)
    return finish(f, n)


# ---- S3: move one: control the supply — an hourglass of diamonds ----
def shot_S3(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 420); u = lt(t, "S3")
    hourglass(f, 540, 1140, 600, 0.85, t)
    ts = T("a1", "Control") - 0.15
    if t >= ts: wui(f, "move one", "CONTROL SUPPLY", t, ts, col=WHITE, size=170)
    else: wui(f, "", "MOVE 1", t, st_("S3") + 0.04, col=YEL_, size=260)
    return finish(cam(f, 1.0 + 0.01 * u, W / 2, 1100), n)


# ---- S4: ~90% of the world's diamonds ----
def shot_S4(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 420); u = lt(t, "S4")
    tn = T("a2", "ninety") - 0.25
    k = clamp((t - tn) / 0.9) if t >= tn else 0.0
    cv2.circle(f, (540, 1120), 300, C((255, 255, 255)), -1, cv2.LINE_AA)
    pie_coin(f, 540, 1120, 290, 0.9 * eo(k), (60, 140, 240), "", 1.0, "")
    cv2.circle(f, (540, 1120), 300, C(INK), 8, cv2.LINE_AA)
    for j in range(8):
        a = -math.pi / 2 + (j + 0.5) * 2 * math.pi * 0.9 / 8
        comp(f, gem_el(70), 540 + 190 * math.cos(a), 1120 + 190 * math.sin(a) + 6 * math.sin(t * 3 + j), scale=pin(t, st_("S4") + 0.1 + 0.08 * j, 0.25))
    if k > 0.95: comp(f, chip("DE BEERS", INK, WHITE, 40), 540, 1120, scale=pin(t, tn + 0.9, 0.25))
    src(f, SRC_AJ, t, tn + 0.5)
    if t >= tn: iui(f, "at its peak, De Beers controlled about", "90%", t, tn, size=260, tail="of the world's diamonds")
    else: iui(f, "at its", "PEAK", t, st_("S4") + 0.06, size=240)
    return finish(f, n)


# ---- S5: kept the stones locked away, let them out slowly ----
def shot_S5(t, n):
    f = stage("emerald", (255, 240, 170), 540, 1080, 440); u = lt(t, "S5")
    tsl = T("a3", "slowly") - 0.25
    k_open = 0.0 if t < tsl else 0.12 * clamp((t - tsl) / 0.6)
    vault_wall(f, 540, 1120, 5, 4, 150, k_open, t)
    if t < tsl: slam(f, stamp_el("LOCKED", RED_, 80), 540, 1120, -8, t, T("a3", "locked") - 0.1)
    if t >= tsl: wui(f, "and let them out", "SLOWLY", t, tsl, size=250)
    else: wui(f, "it kept the stones", "LOCKED AWAY", t, st_("S5") + 0.06, size=200)
    return finish(f, n)


# ---- S5b: scarcity on demand — one gem drips through ----
def shot_S5b(t, n):
    f = stage("purple", (120, 80, 255), 540, 1080, 440); u = lt(t, "S5b")
    hourglass(f, 540, 1140, 600, 0.92, t * 0.6)
    wui(f, "scarcity,", "ON DEMAND", t, st_("S5b") + 0.04, size=230)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1100), n)


# ---- S6: last year De Beers dug up ~22 million carats ----
def shot_S6(t, n):
    f = stage("orange", (255, 230, 140), 540, 1080, 430); u = lt(t, "S6")
    runway(f, 1420, (90, 60, 40))
    xk = eo(clamp(u / 0.8)); comp(f, minecart_el(560, 1.0), 540 + 600 * (1 - xk), 1220 + 3 * math.sin(t * 20) * (1 - xk))
    tw = T("a4", "twenty") - 0.25
    odometer(f, 540, 880, "21.7M" if t >= tw else "00.0M", clamp((t - tw) / 1.0) if t >= tw else 1.0, cell=(104, 150), col=YEL_)
    comp(f, chip("CARATS DUG UP IN 2025", INK, WHITE, 34), 540, 1000, op=clamp((t - tw - 0.6) / 0.3) if t >= tw else 0)
    src(f, SRC_AA, t, tw + 0.6, y=1460)
    if t >= tw: wui(f, "last year De Beers dug up about", "22 MILLION", t, tw, col=WHITE, size=200, tail="carats", y=440)
    else: wui(f, "even", "LAST YEAR", t, st_("S6") + 0.06, col=WHITE, size=220, y=440)
    return finish(f, n)


def shot_S6b(t, n):
    f = stage("orange", (255, 230, 140), 540, 1080, 430); u = lt(t, "S6b")
    runway(f, 1420, (90, 60, 40))
    comp(f, minecart_el(560, 1.0), 540, 1220)
    for j in range(6):
        q = clamp((u - 0.1 * j) / 0.7); x = 540 + (j - 2.5) * 70 + 160 * q * (j - 2.5) / 2.5; y = 1050 - 300 * q + 500 * q * q
        if 0 < q < 1: comp(f, gem_el(70), x, y)
    slam(f, stamp_el("NOT RARE", RED_, 96), 540, 900, -8, t, T("a4", "rare") - 0.15)
    wui(f, "not exactly", "RARE", t, st_("S6b") + 0.04, col=WHITE, size=260, y=440)
    return finish(f, n)


# ---- S7: move two: sell a feeling ----
def shot_S7(t, n):
    f = stage("pink", (255, 230, 150), 540, 1080, 430); u = lt(t, "S7")
    for i in range(9):
        x = 540 + 360 * math.sin(i * 2.3); y = 1500 - ((u * 220 + i * 140) % 900); s = 30 + 12 * (i % 3)
        pts = [(x + s * 16 * math.sin(a) ** 3 / 16, y - s * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 16) for a in np.linspace(0, 2 * math.pi, 40)]
        cv2.fillPoly(f, [np.array(pts, np.int32)], C((232, 28, 60)), cv2.LINE_AA)
    guy(f, 540, 1480, 0.85, la=(40, 30), ra=(130, 150 + 10 * math.sin(t * 6)), mouth=talk(t), blink=blink_at(t, 1), brow="up", expr="wow" if talk(t) == 0 else "n",
        hold=scale_el(ring_el(300), 0.6), hold_off=(10, -70))
    tf = T("b1", "Sell") - 0.15
    if t >= tf: wui(f, "move two", "SELL A FEELING", t, tf, col=WHITE, size=170)
    else: wui(f, "", "MOVE 2", t, st_("S7") + 0.04, col=YEL_, size=260)
    return finish(f, n)


# ---- S8: 1940: one bride in ten ----
def shot_S8(t, n):
    f = stage("cream", (236, 210, 160), 540, 1080, 440); u = lt(t, "S8")
    comp(f, chip("1940", SEPIA, WHITE, 48), 540, 760, scale=pin(t, st_("S8") + 0.1, 0.3))
    tt = T("b2", "ten") - 0.2
    brides(f, 540, 950, 1 if t >= tt else 0, t, tt, 0.95)
    src(f, "Source: Al Jazeera (Sep 2025)", t, tt + 0.4, y=1500)
    if t >= tt: iui(f, "in 1940, only about", "1 IN 10", t, tt, size=240, tail="brides got a diamond ring")
    else: iui(f, "in", "1940", t, st_("S8") + 0.06, size=240)
    return finish(f, n)


# ---- S9: so De Beers hired an ad agency — vintage posters go up ----
def shot_S9(t, n):
    f = stage("cream", (236, 210, 160), 540, 1080, 440); u = lt(t, "S9")
    for i, (x, y, r, ln) in enumerate(((300, 1120, -6, [("Her ring", 40, False), ("will shine", 40, False)]),
                                       (780, 1150, 5, [("The gift", 40, False), ("of a lifetime", 36, True)]),
                                       (540, 1100, -1, [("DIAMONDS", 48, False), ("for every bride", 34, True)]))):
        t0 = st_("S9") + 0.2 + 0.25 * i
        if t >= t0: rot_comp(f, scale_el(poster_el(ln, 460, 620), 0.92 if i == 2 else 0.78), x, y, r, pin(t, t0, 0.3), 1.0, 0.35)
    iui(f, "so De Beers hired an", "AD AGENCY", t, st_("S9") + 0.06, size=210)
    return finish(f, n)


# ---- S9b/S10: 1947, a young copywriter types four words ----
TYPED = "A DIAMOND\nIS FOREVER"


def shot_S9b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1100, 430); u = lt(t, "S9b")
    typewriter(f, 540, 1220, TYPED, 0.0, t, 700)
    comp(f, calendar_el("YEAR", "1947"), 860, 780, scale=0.55 * pin(t, st_("S9b") + 0.1, 0.3))
    tf = T("b3", "four") - 0.2
    if t >= tf: iui(f, "a young copywriter wrote", "4 WORDS", t, tf, size=240)
    else: iui(f, "and in", "1947", t, st_("S9b") + 0.06, size=240)
    return finish(f, n)


def shot_S10(t, n):
    f = stage("cream", (236, 210, 160), 540, 1100, 430); u = lt(t, "S10")
    t0 = T("b4", "A") - 0.05; t1 = T("b4", "forever") + 0.45
    k = clamp((t - t0) / max(0.5, t1 - t0))
    typewriter(f, 540, 1300, TYPED, k, t, 700)
    if k >= 1: ui_word(f, "", "A Diamond Is Forever", 520, t, t1, col=(170, 30, 40), size=110, fp_big=F_PFI)
    return finish(cam(f, 1.0 + 0.02 * u, W / 2, 1000), n)


# ---- S11: Ad Age: slogan of the century ----
def shot_S11(t, n):
    f = stage("purple", (255, 190, 80), 540, 1080, 440); u = lt(t, "S11")
    rot_comp(f, poster_el([("A Diamond", 60, True), ("Is Forever", 60, True)], 560, 760), 540, 1140, -3, 1.0, 1.0, 0.35)
    tc = T("b5", "century") - 0.3
    if t >= tc - 0.4: slam(f, medal_el(), 760, 1300, 8, t, tc - 0.4, 0.8)
    src(f, "Ad Age (1999), via NPR · De Beers (2026)", t, tc, y=1560)
    wui(f, "Ad Age later called it the", "SLOGAN OF THE CENTURY", t, st_("S11") + 0.06, size=120)
    return finish(f, n)


# ---- S11b: by 1980, about eight in ten ----
def shot_S11b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 440); u = lt(t, "S11b")
    comp(f, chip("1980", INK, WHITE, 48), 540, 760, scale=pin(t, st_("S11b") + 0.05, 0.3))
    te = T("b5", "eight") - 0.25
    brides(f, 540, 950, 8 if t >= te else 1, t, te, 0.95)
    src(f, "Source: Al Jazeera (Sep 2025)", t, te + 0.6, y=1500)
    if t >= te: wui(f, "by 1980, about", "8 IN 10", t, te, size=250, tail="brides got a diamond")
    else: wui(f, "by", "1980", t, st_("S11b") + 0.04, col=WHITE, size=250)
    return finish(f, n)


# ---- S12: re-hook — move three is the sneakiest (gold secret folder) ----
def shot_S12(t, n):
    f = stage("red", (255, 200, 60), 540, 1080, 440); u = lt(t, "S12")
    rays(f, 540, 1120, 650, (255, 230, 150), 0.3, t)
    rot_comp(f, scale_el(folder_el("3", True, "SNEAKIEST"), 1.45), 600, 1120 + 8 * math.sin(t * 3), -4, pin(t, st_("S12") + 0.15, 0.35), 1.0, 0.4)
    guy(f, 210, 1490, 0.65, la=(30, 20), ra=(110, 60), mouth=talk(t), blink=blink_at(t, 3), brow="sus", look=(1, -1), expr="smirk" if talk(t) == 0 else "n")
    ts = T("c1", "sneakiest") - 0.2
    if t >= ts: wui(f, "and move three is the", "SNEAKIEST", t, ts, size=220)
    else: wui(f, "and", "MOVE 3…", t, st_("S12") + 0.06, col=WHITE, size=240)
    return finish(f, n)


def shot_S12b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 420); u = lt(t, "S12b")
    comp(f, ring_el(300), 540, 1330 + 5 * math.sin(t * 2.2))
    swing_tag(f, hangtag_el("$ ? ? ?", "YOU PAY", 480), 540, 690, t, 7, 70)
    iui(f, "tell people", "WHAT TO PAY", t, st_("S12b") + 0.04, size=200)
    return finish(cam(f, 1.0 + 0.015 * u, W / 2, 1000), n)


# ---- S13: 1980s ad: how can you make two months' salary last forever? ----
AD80 = [("1980s", 34, False), ("How can you make", 44, False), ("two months' salary", 54, True), ("last forever?", 48, False)]


def shot_S13(t, n):
    f = stage("teal", (255, 230, 150), 540, 1080, 440); u = lt(t, "S13")
    rot_comp(f, poster_el(AD80, 600, 820), 540 + 500 * (1 - eo(clamp(u / 0.4))), 1150, -3, 1.0, 1.0, 0.35)
    src(f, "Source: De Beers ad line, via NPR (2013), Al Jazeera (2025)", t, st_("S13") + 0.5, y=1610, size=19)
    wui(f, "in the 1980s, its ads asked", "HOW CAN YOU…", t, st_("S13") + 0.06, col=WHITE, size=170)
    return finish(f, n)


def shot_S13b(t, n):
    f = stage("emerald", (255, 240, 150), 540, 1080, 440); u = lt(t, "S13b")
    for i in range(2):
        k = pin(t, st_("S13b") + 0.1 + 0.25 * i, 0.3)
        rot_comp(f, scale_el(calendar_el("MONTH", str(i + 1)), 0.7), 330 + 120 * i, 1000 + 40 * i, -8 + 10 * i, k, 1.0, 0.3)
    tf = T("c2", "forever") - 0.2
    for j in range(6):
        q = clamp((u - 0.4 - 0.12 * j) / 0.8); x, y = along((380, 1050), (760, 1250), q, 0.3)
        if 0 < q < 1: rot_comp(f, scale_el(cash_el(1), 0.45), x, y, 20 - 40 * q, 1.0, clamp(q / 0.1) * clamp((1 - q) / 0.15), 0.0)
    comp(f, ring_el(320), 770, 1260 + 6 * math.sin(t * 2.4))
    if t >= tf: sparkle(f, 820, 1110, 40, t)
    wui(f, "make two months' salary", "LAST FOREVER?", t, st_("S13b") + 0.04, size=180)
    return finish(f, n)


# ---- S14: a price rule, written by the seller ----
def shot_S14(t, n):
    f = stage("orange", (255, 230, 140), 540, 1080, 430); u = lt(t, "S14")
    rot_comp(f, rulebook_el(560, round((u * 1.4) % 1.0, 2)), 540, 1100, -3, 1.0, 1.0, 0.3)
    comp(f, chip("RULE: SPEND 2 MONTHS' PAY", INK, YEL_, 36), 540, 1400, op=clamp((u - 0.2) / 0.3))
    tsel = T("c3", "seller") - 0.2
    if t >= tsel: slam(f, stamp_el("WRITTEN BY THE SELLER", RED_, 52), 540, 1120, -9, t, tsel)
    wui(f, "a price rule, written by", "THE SELLER", t, st_("S14") + 0.06, col=WHITE, size=220)
    return finish(f, n)


# ---- S15: but now the trick is breaking — the gem cracks ----
def shot_S15(t, n):
    f = stage("purple", (90, 60, 160), 540, 1080, 400); u = lt(t, "S15")
    tb = T("d1", "breaking") - 0.2
    cr = clamp((t - tb) / 0.5) if t >= tb else 0.0
    shake = 8 * math.sin(t * 60) * clamp((t - tb) / 0.05) * clamp((tb + 0.5 - t) / 0.3) if t >= tb else 0
    comp(f, gem_el(520, ICE, round(cr * 4) / 4), 540 + shake, 1120)
    if t >= tb: wui(f, "but now, the trick is", "BREAKING", t, tb, size=240)
    else: wui(f, "but", "NOW…", t, st_("S15") + 0.06, col=WHITE, size=260)
    return finish(f, n)


# ---- S16: labs can grow real diamonds ----
def shot_S16(t, n):
    f = stage("teal", (200, 240, 255), 540, 1080, 430); u = lt(t, "S16")
    comp(f, flask_el(460, 0.6), 540, 1150)
    g = 0.15 + 0.85 * eo(clamp((u - 0.2) / 1.4))
    comp(f, gem_el(220), 540, 1170, scale=g)
    for j in range(5): sparkle(f, 540 + 150 * math.cos(j * 1.3 + t), 1170 + 150 * math.sin(j * 1.3 + t), 18, t, j)
    wui(f, "labs can", "GROW DIAMONDS", t, st_("S16") + 0.06, col=WHITE, size=180)
    return finish(f, n)


def shot_S16b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 440); u = lt(t, "S16b")
    for i, (x, lab) in enumerate(((290, "MINED"), (790, "LAB-GROWN"))):
        comp(f, gem_el(300), x, 1120 + 8 * math.sin(t * 2 + i), scale=pin(t, st_("S16b") + 0.1 * i, 0.3))
        comp(f, chip(lab, INK, WHITE, 36), x, 1330)
        sparkle(f, x + 90, 1020, 30, t, i * 2)
    comp(f, ed_el("", "=", "", big_col=WHITE, big_size=200, shadow=0.4), 540, 1110, scale=pin(t, st_("S16b") + 0.35, 0.3))
    ts = T("d2", "sparkle") - 0.2
    if t >= ts: wui(f, "same carbon,", "SAME SPARKLE", t, ts, size=190)
    else: wui(f, "", "SAME CARBON", t, st_("S16b") + 0.04, col=WHITE, size=200)
    return finish(f, n)


# ---- S17: lab-grown wholesale prices -96% since 2018 ----
def shot_S17(t, n):
    f = stage("orange", (255, 230, 140), 540, 1170, 380); u = lt(t, "S17")
    tn = T("d3", "ninety") - 0.25
    k = clamp(u / max(0.6, tn - st_("S17") + 0.8))
    pts = [(0, 1.0), (0.14, 0.82), (0.28, 0.62), (0.42, 0.44), (0.57, 0.27), (0.71, 0.15), (0.86, 0.08), (1.0, 0.04)]
    end = line_chart(f, 160, 860, 920, 1380, pts, k, RED_, 14, [(0, "2018"), (1, "2026")])
    if t >= tn + 0.6:
        comp(f, tag_el("-96%", RED_, WHITE, 70), 640, 1150, scale=pin(t, tn + 0.6, 0.3))
    comp(f, chip("LAB-GROWN WHOLESALE PRICE INDEX", INK, WHITE, 28), 600, 900, op=clamp(u / 0.3))
    src(f, "Source: Edahn Golan index, via JCK (Aug 2026)", t, tn + 0.4, y=1490)
    if t >= tn: wui(f, "lab diamond wholesale prices", "-96%", t, tn, size=250, tail="since 2018", y=500)
    else: wui(f, "and their wholesale price", "FELL…", t, st_("S17") + 0.06, col=WHITE, size=240, y=500)
    return finish(f, n)


# ---- S18: even De Beers sold lab diamonds at $800 a carat ----
def shot_S18(t, n):
    f = stage("pink", (255, 230, 150), 540, 1080, 430); u = lt(t, "S18")
    comp(f, flask_el(300, 0.5), 300, 1210)
    comp(f, gem_el(170), 300, 1230)
    te = T("d4", "eight") - 0.25
    if t >= te - 0.3: swing_tag(f, hangtag_el("$800", "PER CARAT", 330), 720, 920, t, 7, 70)
    src(f, "Source: National Jeweler (May 2025)", t, te + 0.4, y=1500)
    if t >= te: wui(f, "even De Beers sold lab diamonds at", "$800/CARAT", t, te, col=WHITE, size=200)
    else: wui(f, "even", "DE BEERS", t, st_("S18") + 0.06, col=WHITE, size=240)
    return finish(f, n)


def shot_S18b(t, n):
    f = stage("red", (255, 200, 60), 540, 1080, 440); u = lt(t, "S18b")
    comp(f, flask_el(300, 0.5), 540, 1230)
    ts = T("d4", "shut") - 0.2
    if t >= ts:
        k = eback(clamp((t - ts) / 0.35)); comp(f, closed_sign_el("SHUT DOWN", 520), 540, 760 + 300 * k)
    wui(f, "then it shut that brand", "DOWN", t, st_("S18b") + 0.04, size=260)
    return finish(f, n)


# ---- S19: last year a core loss of ~$0.5B ----
def shot_S19(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 430); u = lt(t, "S19")
    th = T("d5", "half") - 0.25
    zero = 960
    cv2.line(f, (170, zero), (910, zero), C(INK), 6, cv2.LINE_AA)
    comp(f, chip("2024", INK, WHITE, 32), 360, zero - 50); comp(f, chip("2025", INK, WHITE, 32), 720, zero - 50)
    k1 = clamp(u / 0.5)
    cv2.rectangle(f, (290, zero), (430, int(zero + 15 * k1)), C(RED_), -1, cv2.LINE_AA)   # 2024: -$25M
    k2 = clamp((t - th) / 0.8) if t >= th else 0.0
    if k2 > 0: cv2.rectangle(f, (650, zero), (790, int(zero + 340 * eo(k2))), C(RED_), -1, cv2.LINE_AA)
    else: comp(f, ed_el("", "?", "", big_col=RED_, big_size=200), 720, 1120 - 14 * abs(math.sin(t * 5)), scale=pin(t, st_("S19") + 0.3, 0.3))
    comp(f, gem_el(150), 360, 1210 + 6 * math.sin(t * 2.4), scale=pin(t, st_("S19") + 0.1, 0.3))
    if t >= th + 0.6:
        comp(f, tag_el("-$511M", RED_, WHITE, 60), 720, zero + 420, scale=pin(t, th + 0.6, 0.3))
        comp(f, chip("-$25M", INK, WHITE, 30), 360, zero + 60)
    src(f, "Underlying EBITDA — Anglo American 2025 results", t, th + 0.5, y=1530, size=19)
    if t >= th: wui(f, "De Beers' core loss last year", "≈ $0.5B", t, th, size=230, y=440)
    else: wui(f, "last year,", "DE BEERS…", t, st_("S19") + 0.06, col=WHITE, size=220, y=440)
    return finish(f, n)


def shot_S19b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 430); u = lt(t, "S19b")
    vault_wall(f, 540, 1160, 4, 3, 150, 0.0, t)
    tsl = T("d5", "selling") - 0.25
    if t >= tsl - 0.2: slam(f, sign_el("FOR SALE", RED_, WHITE, 90, pole=False), 540, 1000, -6, t, tsl - 0.2)
    src(f, "De Beers for sale since May 2024 — CNBC Africa (Jul 2026)", t, tsl + 0.2, y=1460, size=19)
    iui(f, "now its owner is", "SELLING IT", t, st_("S19b") + 0.04, size=220)
    return finish(f, n)


# ---- S20: takeaway — price tag vs worth ----
def shot_S20(t, n):
    f = stage("emerald", (255, 240, 150), 540, 1080, 440); u = lt(t, "S20")
    tw = T("t1", "wants") - 0.2
    swing_tag(f, hangtag_el("$$$$", "ASKING PRICE", 380), 600, 680, t, 6, 80)
    guy(f, 230, 1490, 0.7, la=(30, 20), ra=(110, 70), mouth=talk(t), blink=blink_at(t, 4), brow="up", look=(1, -1), expr="n")
    if t >= tw: wui(f, "a price tag tells you what someone", "WANTS", t, tw, size=240, tail="you to pay")
    else: wui(f, "here's the", "TAKEAWAY", t, st_("S20") + 0.06, size=240)
    return finish(f, n)


def shot_S20b(t, n):
    f = stage("teal", (255, 230, 150), 540, 1080, 440); u = lt(t, "S20b")
    comp(f, hangtag_el("PRICE", "", 300), 280, 1150)
    comp(f, gem_el(260), 800, 1160)
    comp(f, chip("WORTH", INK, WHITE, 40), 800, 1340)
    slam(f, ed_el("", "≠", "", big_col=YEL_, big_size=260, shadow=0.4), 540, 1130, 0, t, st_("S20b") + 0.15)
    wui(f, "not what a thing is", "WORTH", t, st_("S20b") + 0.04, size=260)
    return finish(f, n)


# ---- S21: before you pay for rare, ask: what would it sell for tomorrow? ----
def shot_S21(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 430); u = lt(t, "S21")
    tq = T("t2", "What") - 0.2
    comp(f, ring_el(360), 640, 1150 + 6 * math.sin(t * 2.2))
    guy(f, 230, 1490, 0.72, la=(30, 20), ra=(90, 40), mouth=talk(t), blink=blink_at(t, 5), brow="sus", look=(1, -1), expr="sus" if talk(t) == 0 else "n",
        hold=scale_el(magnifier_el(), 0.45), hold_off=(40, -40))
    if t >= tq:
        swing_tag(f, hangtag_el("$ ?", "TOMORROW", 300), 770, 800, t, 8, 60)
        wui(f, "what would it sell for", "TOMORROW?", t, tq, size=220)
    else: wui(f, "before you pay for", "RARE", t, st_("S21") + 0.06, col=WHITE, size=260)
    return finish(f, n)


# ---- S22: the rarest thing about a diamond was the story (exact frame-1 composition = seamless loop) ----
def shot_S22(t, n):
    f = stage("purple", (255, 190, 80), 540, 1080, 360)
    hook_set(f, t)
    ts = T("e1", "story") - 0.2
    if t >= ts: wui(f, "the rarest thing about a diamond was", "THE STORY", t, ts, size=210)
    else: wui(f, "because the", "RAREST THING…", t, st_("S22") + 0.06, col=WHITE, size=170)
    return finish(cam(f, 1.0 + 0.012 * (t - st_("S22")), W / 2, 1080), n)


# ---- S23: send it + brand sting ----
def shot_S23(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420); u = lt(t, "S23")
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("is a diamond really rare?", "watch this before you buy", pr), 0.82), 600, 950, scale=pin(t, st_("S23")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(ring_el(300), 0.6), hold_off=(20, -60))
        ui_word(f, "send to the friend who's shopping for a", "RING", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=170, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "two") - 0.2, 0.3, 12), (T("i2", "rare") - 0.15, 0.35, 14), (T("a2", "ninety") - 0.25, 0.3, 12),
           (T("a3", "locked") - 0.1, 0.3, 12), (T("a4", "twenty") - 0.25, 0.25, 10), (T("a4", "rare") - 0.15, 0.35, 16),
           (T("b2", "ten") - 0.2, 0.25, 8), (T("b5", "century") - 0.7, 0.3, 12), (T("b5", "eight") - 0.25, 0.3, 12),
           (T("c1", "sneakiest") - 0.2, 0.3, 12), (T("c3", "seller") - 0.2, 0.35, 16), (T("d1", "breaking") - 0.2, 0.4, 18),
           (T("d3", "ninety") - 0.25, 0.3, 12), (T("d4", "shut") - 0.2 + 0.2, 0.35, 16), (T("d5", "half") - 0.25, 0.3, 12),
           (T("d5", "selling") - 0.45, 0.3, 12), (T("t1", "Not") - 0.15 + 0.15, 0.3, 12)]


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
