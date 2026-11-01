# ================= shots: HOW TO START · EP 2 — How to start a vending machine business (line-art stick cast) =================
# Cast: hero (orange tie = you, first-time buyer), mentor = girl2 (purple, runs a small route), DEAL SELLER = exec re-dressed grey,
# spot owner = lady, the "singer" = oldman. New layout ideas vs EP 1: split-screen flashback (t1), sepia 1998 flashback block (e2–t1),
# 40 stamps raining (e3), price tag flip new→used (c2), part-by-part machine test (c3). Funk/clavinet score.
def L0(l): return LINES[l]["start"]


def L1(l): return LINES[l]["end"]


def Tw(l, w, d=0.0):
    try: return T(l, w) + d
    except Exception: return L0(l) + d


SERIES_T = "EP 2 · VENDING MACHINES"
MENTOR = "girl2"
SELLER = {"base": "exec", "jacket": (140, 144, 156), "tie": (90, 92, 104)}
SINGER = {"base": "oldman", "tie": (255, 200, 0)}

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", L0("i2") - 0.2, "whip"), ("S2", L0("i3") - 0.2, "zoom"), ("S2b", Tw("i3", "plan", -0.2), "punch"),
    ("S3", L0("i4") - 0.2, "flash"),
    ("S4", L0("a1") - 0.25, "whip"), ("S5", L0("a2") - 0.2, "focus"), ("S5b", Tw("a2", "count", -0.2), "whip"), ("S6", L0("a3") - 0.2, "zoom"),
    ("S7", L0("b1") - 0.25, "whip"), ("S8", L0("b2") - 0.2, "focus"), ("S8b", Tw("b2", "Then", -0.15), "punch"),
    ("S9", L0("c1") - 0.25, "whip"), ("S10", L0("c2") - 0.2, "focus"), ("S11", L0("c3") - 0.2, "zoom"),
    ("S12", L0("e1") - 0.25, "whip"), ("S13", L0("e2") - 0.2, "flash"), ("S14", L0("e3") - 0.2, "punch"), ("S15", L0("e4") - 0.2, "focus"),
    ("S16", L0("e5") - 0.2, "flash"), ("S16b", Tw("e5", "Sellers", -0.15), "zoom"),
    ("S17", L0("t1") - 0.2, "whip"), ("S18", L0("t2") - 0.2, "flash"),
    ("S19", L0("z1") - 0.2, "whip"), ("S20", Tw("z1", "Your", -0.15), "punch"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


def step_card(f, t, sid, n, detail):
    cold_open(f, f"STEP {n} OF 4", "HOW TO START", detail, op=clamp((t - st0(sid)) / 0.2))


def src(f, t, t0, text, y=1440):
    if t >= t0: comp(f, chip(text, (20, 20, 26), WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


def notes(f, x, y, t, n=3, op=1.0):
    for i in range(n):
        ph = (t * 0.9 + i / n) % 1.0
        comp(f, note_el(kind=i % 2), x + 60 * math.sin(ph * 6 + i), y - 220 * ph, scale=0.8, op=op * clamp(3 * (1 - ph)) * clamp(ph * 6))


def thought(f, x, y, w, inner, op=1.0):
    if op <= 0: return
    ov = f.copy()
    cv2.ellipse(ov, (int(x), int(y)), (int(w * 0.62), int(w * 0.62)), 0, 0, 360, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
    for i, r in enumerate((34, 22, 14)):
        cv2.circle(ov, (int(x - w * 0.3 - i * 40), int(y + w * 0.62 + 30 + i * 46)), r, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
    f[:] = f * (1 - op) + ov * op
    comp(f, inner, x, y, op=op)


def coin_rain(f, t, t0, x, y, n=7):
    for i in range(n):
        q = t - t0 - i * 0.09
        if q <= 0: continue
        rot_comp(f, coin_el(42), x + (i - n / 2) * 40 + 30 * math.sin(i * 2.1), y + 900 * q * q, 40 * q * (i % 3 - 1), 1.0, clamp(2.0 - q), 0.2)


def vend(w=600, **kw):
    if w >= 400: return vending_el(w, **kw)
    return scale_el(vending_el(400, **kw), w / 400)


def sepia(f, t, t0):
    k = clamp((t - t0) / 0.3)
    if k > 0: sepia_tone(f, 0.85 * k)


# ---- S0: frame 1 — the snack machine, you with your cash, the grey seller pushing a happy "reference" ----
def shot_S0(t, n):
    u = lt(t, "S0")
    f = set_view("store", t, zoom=1.04 + 0.012 * u, cy=980)
    comp(f, vend(560, fill=1.0, glow=0.9 + 0.1 * math.sin(t * 5)), 540, 1060)
    person(f, 230, 1520, 0.8, "hero", la=(20, 10), ra=(60, 40), brow="sus" if u > 1.0 else "up", look=(1, -1), expr="sus" if u > 1.4 else "n",
           hold=cash_el(), hold_off=(10, -10))
    person(f, 850, 1520, 0.78, SELLER, la=(18, 8), ra=(150, 120), mouth=2 if 0.4 < u < 1.4 else 0, brow="up", look=(-1, 0))
    comp(f, bubble_el("BEST DEAL EVER!", 40), 740, 640)
    notes(f, 900, 760, t, 3)
    say(f, "WHAT'S A \"SINGER\"?", 1440, 120, YEL_)
    cold_open(f, "US", "VENDING MACHINES", "YOU: FIRST-TIME BUYER")
    return finish(f, n)


# ---- S1: you dream of a snack machine side business ----
def shot_S1(t, n):
    u = lt(t, "S1")
    f = set_view("street", t, zoom=1.12, cy=1000)
    wk = walk(t, 1.0)
    person(f, 260 + 160 * eo(clamp(u / 2.6)), 1540, 0.84, "hero", **wk, brow="up", look=(1, -1), expr="wow")
    thought(f, 690, 760, 300, vend(220), op=clamp((u - 0.3) / 0.3))
    say(f, "SNACK MACHINE", 1260, 120, t=t, t0=Tw("i2", "snack", -0.1))
    say(f, "SIDE BUSINESS", 1390, 90, YEL_, t=t, t0=Tw("i2", "side", -0.1))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S2: the price — several thousand dollars ----
def shot_S2(t, n):
    u = lt(t, "S2")
    f = stage("sky", (255, 255, 255), 540, 1080, 470)
    comp(f, vend(470), 470, 1120, scale=pin(t, st0("S2"), 0.3))
    tk = Tw("i3", "thousand", -0.25)
    if t >= tk:
        k = clamp((t - tk) / 0.35); sw = 14 * math.sin((t - tk) * 7) * math.exp(-(t - tk) * 2)
        rot_comp(f, tag_el("$4K–$9K NEW", GRN_, WHITE, 70), 730, 700 + 120 * eback(k), -10 + sw, 1.0, k, 0.3)
    ui_word(f, "a new machine:", "$$$$", 470, t, st0("S2") + 0.1, col=YEL_, size=150, shadow=0.4, lead_col=WHITE)
    src(f, t, tk + 0.4, "Dealer price lists, 2026 (snack/drink/combo)")
    return finish(f, n)


# ---- S2b: the plan in four steps — cards pop ----
def shot_S2b(t, n):
    f = stage("purple", GOLD, 540, 1040, 470)
    names = [("SPOT", (40, 110, 220)), ("PAPERS", (36, 160, 90)), ("BUY", (240, 140, 20)), ("DEALS", (150, 60, 200))]
    for i, (w_, c_) in enumerate(names):
        comp(f, numcard_el(str(i + 1), w_, c_, 200), 225 + 210 * i, 1060, scale=pin(t, st0("S2b") + 0.12 * i, 0.3))
    ui_word(f, "the plan in", "4 STEPS", 470, t, st0("S2b") + 0.05, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    return finish(f, n)


# ---- S3: step four has cost some buyers thousands ----
def shot_S3(t, n):
    f = stage("red", (255, 220, 200), 540, 1000, 460)
    for i in range(3):
        comp(f, numcard_el(str(i + 1), "", (90, 90, 110), 150), 210 + 130 * i, 820, op=0.55)
    tf = Tw("i4", "four", -0.1)
    wob = 8 * math.sin(t * 18) * clamp(t - tf) if t >= tf else 0
    rot_comp(f, numcard_el("4", "DEALS", RED_, 280), 770, 960, wob, pin(t, st0("S3"), 0.3), 1.0, 0.3)
    person_head_at(f, 330, 1240, 1.8, "hero", brow="worry", mouth=1, sweat=True, look=(1, -1))
    th = Tw("i4", "thousands.", -0.1)
    coin_rain(f, t, th - 0.4, 330, 1350)
    say(f, "COST SOME BUYERS", 450, 70, t=t, t0=Tw("i4", "cost", -0.1))
    say(f, "THOUSANDS", 570, 130, YEL_, t=t, t0=th)
    return finish(f, n)


# ---- S4: STEP 1 — spot first ----
def shot_S4(t, n):
    u = lt(t, "S4")
    f = set_view("office", t, zoom=1.02 + 0.02 * u, cy=980)
    comp(f, vend(300, glow=0.6), 620 + 140 * eo(clamp(u / 1.6)), 1290)
    wk = walk(t, 1.0) if u < 1.6 else {}
    person(f, 260 + 140 * eo(clamp(u / 1.6)), 1540, 0.84, "hero", **wk, brow="up", look=(1 if (u % 1.4) < 0.7 else -1, 0))
    say(f, "SPOT FIRST", 700, 150, t=t, t0=st0("S4") + 0.1)
    step_card(f, t, "S4", 1, "THEN THE MACHINE")
    return finish(f, n)


# ---- S5: a dead hallway sells nothing ----
def shot_S5(t, n):
    f = set_view("office", t, zoom=1.25, cx=540, cy=1100, blur=1.5)
    f[:] = f * 0.78
    comp(f, vend(420, fill=1.0, glow=0.35), 560, 1180)
    for i in range(14):   # dust motes
        ph = (t * 0.15 + i * 0.137) % 1.0
        cv2.circle(f, (int(200 + 680 * ((i * 0.37) % 1)), int(700 + 700 * ph)), 3, (0.9, 0.85, 0.7), -1, cv2.LINE_AA)
    tn = Tw("a2", "nothing.", -0.2)
    if t >= tn: rot_comp(f, tag_el("0 SOLD", (90, 90, 100), WHITE, 60), 560, 760, -6, pin(t, tn, 0.3), 1.0, 0.3)
    say(f, "DEAD HALLWAY", 1440, 120, t=t, t0=Tw("a2", "dead", -0.1))
    return finish(f, n)


# ---- S5b: so count who walks past: morning, lunch, evening ----
def shot_S5b(t, n):
    f = set_view("airport", t, zoom=1.0, cy=1000)
    comp(f, vend(330), 180, 1260)
    for i, (who, sp, y0) in enumerate((("friend", 1.0, 1540), ("lady", 0.8, 1560), ("creator", 1.15, 1520), ("kid", 0.9, 1570))):
        x = (300 + 260 * i + 230 * sp * t) % 640 + 300
        person(f, x, y0, 0.7, who, **walk(t + i * 0.3, sp), look=(1, 0))
    for j, (w_, wd) in enumerate((("MORNING", "morning,"), ("LUNCH", "lunch"), ("EVENING", "evening."))):
        tj = Tw("a2", wd, -0.1)
        if t >= tj:
            comp(f, chip(w_, (40, 110, 220), WHITE, 34), 260 + 280 * j, 860, scale=pin(t, tj, 0.25))
            for m in range(min(5, int((t - tj) * 8))):
                x0 = 215 + 280 * j + 22 * m
                if m < 4: cv2.line(f, (x0, 920), (x0, 990), (1, 1, 1), 7, cv2.LINE_AA)
                else: cv2.line(f, (x0 - 96, 975), (x0 + 6, 930), (1, 1, 1), 7, cv2.LINE_AA)
    say(f, "COUNT PEOPLE", 640, 140, YEL_, t=t, t0=Tw("a2", "count", -0.1))
    return finish(f, n)


# ---- S6: the spot owner takes a cut — or a flat rent ----
def shot_S6(t, n):
    u = lt(t, "S6")
    f = set_view("airport", t, zoom=1.3, cx=540, cy=1150, blur=2.5)
    comp(f, vend(300), 540, 1180)
    sh = 0.2 < u < 1.4
    person(f, 270, 1640, 1.0, "hero", la=(18, 8), ra=(70, 80) if sh else (18, 8), brow="up", look=(1, 0), mouth=0)
    person(f, 810, 1640, 0.98, "lady", la=(70, 80) if sh else (18, 8), ra=(18, 8), mouth=talk(t) if u < 2.0 else 0, brow="up", look=(-1, 0))
    tc = Tw("a3", "cut", -0.15); tr = Tw("a3", "rent", -0.2)
    if tc <= t < tr:
        q = clamp((t - tc) / 0.7); rot_comp(f, cash_el(), 560 + 220 * eo(q), 1040 - 80 * math.sin(q * 3.1), 10 * q, 0.9, 1.0, 0.3)
        comp(f, chip("% OF SALES", GRN_, WHITE, 40), 760, 880, scale=pin(t, tc, 0.25))
    if t >= tr:
        rot_comp(f, form_el(260, "MONTHLY RENT"), 760, 1000, 6, pin(t, tr, 0.3), 1.0, 0.3)
    say(f, "A CUT · OR RENT", 640, 130, t=t, t0=tc)
    src(f, t, tc + 0.5, "Stripe vending guide, Aug 2026")
    return finish(f, n)


# ---- S7: STEP 2 — paperwork ----
def shot_S7(t, n):
    u = lt(t, "S7")
    f = set_view("office", t, zoom=1.15, cx=540, cy=1050, blur=1.0)
    for i in range(4):
        k = clamp((u - 0.15 * i) / 0.25)
        if k > 0: rot_comp(f, form_el(300, ["PERMIT", "LICENSE", "TAX ID", "INSURANCE"][i]), 700 + 10 * i, 1230 - 14 * i - 500 * (1 - eo(k)), -8 + 5 * i, 1.0, 1.0, 0.3)
    person(f, 260, 1560, 0.86, "hero", la=(60, 70), ra=(60, 70), brow="up", look=(1, 0))
    say(f, "PAPERWORK", 700, 160, t=t, t0=st0("S7") + 0.1)
    step_card(f, t, "S7", 2, "RULES VARY BY CITY")
    return finish(f, n)


# ---- S8: some cities want a vending license ----
def shot_S8(t, n):
    f = stage("teal", (255, 255, 255), 540, 1050, 450)
    rot_comp(f, form_el(440, "VENDING LICENSE"), 500, 1060, -4, pin(t, st0("S8"), 0.3), 1.0, 0.35)
    tc = Tw("b2", "check", -0.1)
    if t >= tc: rot_comp(f, stamp_el("CHECK YOUR CITY", RED_, 56), 500, 1180, -12, 1.6 - 0.6 * eo(clamp((t - tc) / 0.2)), clamp((t - tc) * 6), 0.0)
    person(f, 860, 1560, 0.7, MENTOR, la=(18, 8), ra=(120, 160), mouth=talk(t), brow="up", look=(-1, 0))
    say(f, "SOME CITIES", 520, 130, t=t, t0=Tw("b2", "cities", -0.1))
    src(f, t, tc + 0.3, "Stripe: some municipalities require a license", 1450)
    return finish(f, n)


# ---- S8b: then liability insurance — a shield wraps the machine ----
def shot_S8b(t, n):
    u = lt(t, "S8b")
    f = set_view("store", t, zoom=1.2, cx=540, cy=1100, blur=3)
    comp(f, vend(400), 560, 1120)
    ti = Tw("b2", "insurance.", -0.3)
    if t >= ti: comp(f, shield_el(520, "INSURED"), 560, 1080, scale=pin(t, ti, 0.35), op=0.9)
    person(f, 210, 1600, 0.8, "hero", la=(18, 8), ra=(150, 170), brow="up", look=(1, -1), expr="wow" if u > 0.8 else "n")
    say(f, "LIABILITY INSURANCE", 520, 110, YEL_, t=t, t0=Tw("b2", "liability", -0.1))
    return finish(f, n)


# ---- S9: STEP 3 — buy smart: the used-machine lot (a phone rings far off) ----
def shot_S9(t, n):
    u = lt(t, "S9")
    f = set_view("street", t, zoom=1.08, cy=1000)
    comp(f, vend(260, fill=0.6, glow=0.4), 230, 1280)
    rot_comp(f, vend(260, fill=0.2, glow=0.0, broken="coins"), 820, 1290, 4, 1.0, 1.0, 0.25)
    comp(f, vend(290, fill=0.9, glow=0.8), 520, 1270)
    person(f, 640, 1580, 0.8, "hero", la=(60, 90), ra=(40, 80), brow="up", look=(1, 0) if t < Tw("c1", "singers", -0.2) else (1, -1))
    tg = Tw("c1", "singers", -0.2)
    if t >= tg:
        comp(f, bubble_el("RING RING...", 30), 790, 1000, scale=pin(t, tg, 0.3)); notes(f, 860, 960, t, 2, 0.8)
    say(f, "BUY SMART", 700, 150, t=t, t0=st0("S9") + 0.1)
    step_card(f, t, "S9", 3, "NEW OR USED")
    return finish(f, n)


# ---- S10: used is cheaper, but still a few thousand — the tag flips ----
def shot_S10(t, n):
    f = stage("orange", YEL_, 540, 1050, 460)
    comp(f, vend(420, fill=0.8, glow=0.6), 420, 1150, scale=pin(t, st0("S10"), 0.3))
    tu = Tw("c2", "few", -0.2); fl = clamp((t - tu) / 0.3)
    sx = max(0.04, abs(math.cos(fl * math.pi)))
    el = tag_el("$4K–$9K NEW", GRN_, WHITE, 60) if fl < 0.5 else tag_el("$3K–$6K+ USED", (40, 110, 220), WHITE, 60)
    rot_comp(f, (cv2.resize(el[0], (max(2, int(el[0].shape[1] * sx)), el[0].shape[0])), cv2.resize(el[1], (max(2, int(el[1].shape[1] * sx)), el[1].shape[0]))),
             700, 760, -8, 1.0, 1.0, 0.3)
    say(f, "USED = CHEAPER", 470, 120, WHITE, t=t, t0=Tw("c2", "used", -0.1))
    src(f, t, tu + 0.4, "Dealer price lists, 2026 · Stripe, Aug 2026")
    return finish(f, n)


# ---- S11: test the coin slot, the bill reader, the cooler ----
def shot_S11(t, n):
    f = set_view("street", t, zoom=1.4, blur=5)
    tcn = Tw("c3", "coin", -0.15); tb = Tw("c3", "bill", -0.15); tco = Tw("c3", "cooler", -0.15)
    br = "bills" if tb <= t < tb + 0.6 else None
    comp(f, vend(760, broken=br), 470, 1110)
    for tt, yy in ((tcn, 1030), (tb + 0.45, 1100), (tco, 1190)):
        if t >= tt: comp(f, check_el(36, True), 930, yy, scale=pin(t, tt, 0.25))
    hud_rule(f, 3, "TEST BEFORE YOU PAY", y=430, t=t, t0=st0("S11") + 0.1)
    return finish(f, n)


# ---- S12: STEP 4 — the deal: machines + "prime spots, already found" ----
def shot_S12(t, n):
    u = lt(t, "S12")
    f = set_view("store", t, zoom=1.15, cx=540, cy=1080, blur=1.5)
    f[:] = f * np.array([0.82, 0.86, 1.0], np.float32)
    for i in range(3):
        k = clamp((u - 0.5 - 0.15 * i) / 0.3)
        if k > 0: rot_comp(f, form_el(170, ["MALL", "GYM", "OFFICE"][i]), 560 + 185 * (i - 1) * eo(k), 1040 - 20 * abs(i - 1), (i - 1) * 14 * eo(k), 1.0, 1.0, 0.3)
    if u > 0.9: comp(f, chip("PRIME SPOTS!", (240, 140, 20), WHITE, 40), 560, 880, scale=pin(t, st0("S12") + 0.9, 0.25))
    person(f, 830, 1600, 0.9, SELLER, la=(18, 8), ra=(150, 120), mouth=talk(t), brow="up", look=(-1, 0))
    person(f, 240, 1600, 0.86, "hero", la=(18, 8), ra=(60, 60), brow="up", look=(1, -1), expr="wow")
    say(f, "CHECK THE DEAL", 700, 120, t=t, t0=Tw("e1", "careful", -0.1))
    step_card(f, t, "S12", 4, "SPOTS INCLUDED?")
    return finish(f, n)


# ---- S13: back in 1998 — sepia flashback, calendar flips back ----
def shot_S13(t, n):
    u = lt(t, "S13")
    f = set_view("store", t, zoom=1.3, cx=540, cy=1100, blur=4)
    yr = "1998" if u > 0.7 else str(2026 - int(28 * clamp(u / 0.7)))
    comp(f, calendar_el("BACK IN", yr), 540, 1000, scale=1.5 * pin(t, st0("S13"), 0.3))
    sepia(f, t, st0("S13") + 0.2)
    say(f, "\"FRAUDULENT\"", 1360, 120, YEL_, t=t, t0=Tw("e2", "fraudulent.", -0.2))
    src(f, t, Tw("e2", "regulators", 0.0), "FTC + 10 states, Sep 1998", 1470)
    return finish(f, n)


# ---- S14: forty actions in one go — stamps rain ----
def shot_S14(t, n):
    f = stage("cream", (255, 230, 180), 540, 1050, 470)
    for i in range(6): rot_comp(f, form_el(260, "BIG PROFITS!"), 420 + 40 * i, 1180 - 6 * i, -10 + 4 * i, 1.0, 1.0, 0.3)
    tf = Tw("e3", "forty", -0.2)
    rng = np.random.default_rng(4)
    pos = [(rng.uniform(280, 800), rng.uniform(950, 1350), rng.uniform(-25, 25)) for _ in range(40)]
    m = int(clamp((t - tf) / 1.4) * 40)
    for i in range(m):
        x, y, r = pos[i]; ti = tf + i * 1.4 / 40
        rot_comp(f, stamp_el("FTC ACTION", RED_, 34), x, y, r, 1.4 - 0.4 * eo(clamp((t - ti) / 0.12)), 1.0, 0.0)
    if t >= tf: ui_word(f, "in one sweep", "40", 470, t, tf, col=RED_, size=200, shadow=0.4, lead_col=INK, tail="ACTIONS")
    src(f, t, tf + 0.6, "FTC press release, 3 Sep 1998", 1470)
    return finish(f, n)


# ---- S15: the charge — the "prime spot" photo peels off to an empty hallway ----
def shot_S15(t, n):
    f = set_view("office", t, zoom=1.3, cx=540, cy=1150, blur=2)
    f[:] = f * 0.75
    comp(f, vend(330, fill=1.0, glow=0.2), 700, 1240)
    tp = Tw("e4", "spots", -0.4); k = clamp((t - tp) / 0.5)
    if k < 1: rot_comp(f, form_el(400, "PRIME SPOT!"), 620 + 700 * k ** 2, 1150 - 200 * k, -30 * k, 1.0, 1.0 - k, 0.3)
    person(f, 270, 1620, 0.9, "hero", la=(18, 8), ra=(18, 8), brow="sus", expr="sus" if k > 0.5 else "n", look=(1, 0))
    quote_card(f, "misrepresenting the availability of profitable locations", "FTC charge vs. one seller, Sep 1998", y=640, t=t, t0=Tw("e4", "charged", -0.2))
    sepia(f, t, st0("S15") - 1)
    return finish(f, n)


# ---- S16: so what protects you today? sepia drains away ----
def shot_S16(t, n):
    u = lt(t, "S16")
    f = set_view("store", t, zoom=1.05, cy=1000)
    comp(f, vend(420), 540, 1120)
    person(f, 830, 1560, 0.82, MENTOR, la=(18, 8), ra=(150, 160), mouth=talk(t), brow="up", look=(-1, 0))
    person(f, 250, 1560, 0.82, "hero", la=(18, 8), ra=(18, 8), brow="up", look=(1, -1))
    k = 1 - clamp(u / 0.6)
    if k > 0: sepia_tone(f, 0.85 * k)
    say(f, "WHAT PROTECTS YOU", 640, 100, YEL_, t=t, t0=Tw("e5", "protects", -0.15))
    say(f, "TODAY?", 760, 130, t=t, t0=Tw("e5", "today?", -0.1))
    return finish(f, n)


# ---- S16b: the disclosure — past buyers, a week before you pay ----
def shot_S16b(t, n):
    f = stage("emerald", (255, 255, 255), 540, 1060, 460)
    rot_comp(f, form_el(420, "DISCLOSURE"), 420, 1100, -4, pin(t, st0("S16b"), 0.3), 1.0, 0.35)
    tb = Tw("e5", "buyers,", -0.3)
    for i in range(5):
        if t >= tb + 0.1 * i: comp(f, chip(f"PAST BUYER #{i + 1}", WHITE, INK, 26), 420, 1000 + 54 * i, scale=pin(t, tb + 0.1 * i, 0.2))
    tw = Tw("e5", "week", -0.2)
    if t >= tw:
        rot_comp(f, calendar_el("DAYS", "7"), 790, 860, 8, pin(t, tw, 0.3), 1.0, 0.3)
        say(f, "BEFORE YOU PAY", 1330, 90, YEL_, t=t, t0=tw)
    say(f, "PAST BUYERS", 470, 130, WHITE, t=t, t0=tb)
    src(f, t, tw + 0.4, "FTC Business Opportunity Rule (16 CFR 437)", 1450)
    return finish(f, n)


# ---- S17: back then — split screen: the happy reference sings / the seller pays him ----
def shot_S17(t, n):
    f = set_view("parlor", t, zoom=1.35, cx=540, cy=1150, blur=1.5)
    person(f, 300, 1640, 0.95, SINGER, la=(18, 8), ra=(150, 130), mouth=talk(t, True), brow="up", look=(1, 0))
    comp(f, bubble_el("BEST DEAL EVER!", 34), 330, 760, scale=pin(t, st0("S17") + 0.2, 0.3)); notes(f, 430, 900, t, 3)
    tp = Tw("t1", "paid", -0.2)
    if t >= tp:
        g = set_view("office", t, zoom=1.35, cx=540, cy=1150, blur=1.5)
        person(g, 640, 1640, 0.95, SINGER, la=(70, 70), ra=(18, 8), brow="up", look=(1, 0), mouth=2)
        person(g, 880, 1640, 0.95, SELLER, la=(18, 8), ra=(80, 70), brow="up", look=(-1, 0), mouth=2)
        rot_comp(g, cash_el(), 760, 1120, 10, 0.8, 1.0, 0.3)
        xs = int(W - (W // 2) * eo(clamp((t - tp) / 0.3)))
        f[:, xs:] = g[:, xs:]
        cv2.line(f, (xs, 0), (xs, H), (1, 1, 1), 8)
    sepia(f, t, st0("S17") - 1)
    say(f, "\"SINGERS\"", 600, 170, YEL_, t=t, t0=Tw("t1", "singers,", -0.15))
    say(f, "PAID TO PRAISE", 1400, 100, t=t, t0=tp)
    src(f, t, Tw("t1", "FTC", 0.0), "FTC, Sep 1998: phony references, \"singers\"", 1500)
    return finish(f, n)


# ---- S18: today — skip the seller's picks, call the list yourself ----
def shot_S18(t, n):
    f = set_view("street", t, zoom=1.2, cx=540, cy=1100, blur=2)
    rot_comp(f, form_el(300, "PAST BUYERS"), 800, 1080, 8, 1.0, 1.0, 0.3)
    td = Tw("t2", "Call", -0.2)
    person(f, 330, 1620, 0.95, "hero", la=(18, 8), ra=(150, 150) if t >= td else (18, 8), brow="up", look=(1, 0), mouth=0
)
    if t >= td: comp(f, chip("CALLING PAST BUYER #3...", (36, 160, 90), WHITE, 34), 540, 1000, scale=pin(t, td, 0.25))
    ts = Tw("t2", "skip", -0.1)
    if ts <= t < td: say(f, "SKIP THE SELLER'S PICKS", 700, 90, YEL_, t=t, t0=ts)
    hud_rule(f, 4, "CALL THE LIST YOURSELF", y=430, t=t, t0=td - 0.1)
    return finish(f, n)


# ---- S19: save this — loop back to the frame-1 store, mentor beside you ----
def shot_S19(t, n):
    u = lt(t, "S19")
    f = set_view("store", t, zoom=1.04, cy=980)
    comp(f, vend(560, fill=1.0), 540, 1060)
    person(f, 230, 1520, 0.8, "hero", la=(20, 8), ra=(160, 150), brow="up", look=(1, -1), mouth=2 if u < 0.8 else 0)
    person(f, 850, 1520, 0.78, MENTOR, la=(150, 160), ra=(18, 8), brow="up", look=(-1, 0))
    say(f, "SAVE THIS", 640, 160, YEL_, t=t, t0=Tw("z1", "Save", -0.1))
    say(f, "BEFORE YOU BUY", 1300, 90, t=t, t0=Tw("z1", "Save", 0.2))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S20: your move — gym or office? then send ----
def shot_S20(t, n):
    u = lt(t, "S20")
    f = stage("purple", GOLD, 540, 1000, 460)
    comp(f, vend(300, fill=1.0), 540, 1010)
    q = t - Tw("z2", "friend", -0.1)
    if q > 0: rot_comp(f, coin_el(40), 540, 820 + min(240, 700 * q * q), 30 * q, 1.0, clamp(1.6 - q), 0.2)
    person(f, 230, 1360, 0.6, "hero", la=(18, 8), ra=(80, 20), brow="up", look=(1, 0), mouth=2 if u < 0.6 else 0)
    person(f, 850, 1360, 0.6, MENTOR, la=(150, 170 + 18 * math.sin(t * 12)) if t >= L0("z2") else (18, 8), ra=(18, 8), brow="up", look=(-1, 0))
    choice_card(f, "YOUR FIRST SPOT?", "GYM", "OFFICE", y=600, t=t, t0=st0("S20") + 0.05, col_a=(36, 186, 88), col_b=(40, 110, 220))
    tf = Tw("z2", "friend", -0.15)
    if t >= tf: say(f, "SEND TO THAT FRIEND", 1460, 80, t=t, t0=tf)
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(Tw("i3", "thousand", -0.25), 0.25, 10), (Tw("i4", "thousands.", -0.1), 0.3, 14), (Tw("b2", "check", -0.1), 0.25, 10),
           (Tw("e3", "forty", -0.2), 0.3, 12), (Tw("t1", "singers,", -0.15), 0.35, 16), (Tw("c2", "few", -0.2), 0.2, 8)]


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
