# ================= shots: HOW TO START · EP 4 — How to start a Christmas-light install business (line-art cast, clean look, two voices) =================
# Cast: hero (orange tie = the neighbor with a ladder), crew lead (girl: green shirt, red hair; second voice, lip-synced), homeowner (girl2), electrician (worker, navy cap).
# New vs EP 3: two-voice dialogue, bulbs that switch on in a wave along the roofline (the whole frame is a night street), tape measure along the roof = the price maths on the house,
# year strip of 12 month tiles, three glowing contact rings on the ladder, power-line clearance arrow, snow, jazz-waltz score with sleigh bells (original tune).
def L0(l): return LINES[l]["start"]


def L1(l): return LINES[l]["end"]


def Tw(l, w, d=0.0, nth=0):
    try: return T(l, w, nth) + d
    except Exception: return L0(l) + d


SERIES_T = "EP 4 · CHRISTMAS LIGHTS"
HERO = "hero"
CREW = {"base": "girl", "shirt": (24, 170, 100), "hair": (210, 66, 40)}
OWNER = {"base": "girl2", "shirt": (70, 150, 250), "hair": (60, 40, 30)}
SPARKY = {"base": "worker", "cap": (30, 50, 110), "shirt": (40, 90, 200)}
MLINES = ("m0", "a1", "b1", "c1", "d1", "e1")

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", L0("i2") - 0.2, "whip"), ("S2", L0("i3") - 0.2, "flash"), ("S3", L0("i4") - 0.2, "zoom"), ("S4", L0("i5") - 0.2, "whip"), ("S5", L0("m0") - 0.1, "punch"),
    ("S6", L0("a1") - 0.25, "whip"), ("S7", L0("a2") - 0.2, "focus"), ("S8", L0("a3") - 0.2, "zoom"), ("S9", Tw("a3", "Some", -0.15), "focus"),
    ("S10", L0("b1") - 0.25, "whip"), ("S11", L0("b2") - 0.2, "focus"), ("S12", L0("b3") - 0.2, "flash"),
    ("S13", L0("c1") - 0.25, "whip"), ("S14", L0("c2") - 0.2, "zoom"), ("S15", L0("c3") - 0.2, "focus"), ("S16", L0("c4") - 0.2, "whip"), ("S16b", L0("c5") - 0.2, "focus"),
    ("S17", L0("d1") - 0.25, "whip"), ("S18", L0("d2") - 0.2, "zoom"), ("S19", L0("d3") - 0.2, "focus"), ("S20", L0("d4") - 0.2, "flash"), ("S21", L0("d5") - 0.2, "zoom"),
    ("S22", L0("e1") - 0.25, "whip"), ("S23", L0("e2") - 0.2, "focus"), ("S24", L0("e3") - 0.2, "whip"), ("S24b", L0("e4") - 0.2, "zoom"), ("S25", L0("e5") - 0.2, "focus"),
    ("S26", L0("t1") - 0.2, "whip"), ("S26b", Tw("t1", "So", -0.2), "punch"), ("S27", L0("t3") - 0.2, "whip"), ("S28", L0("z1") - 0.2, "zoom"), ("S29", L0("z2") - 0.2, "punch"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


_TNOW = [0.0]
_person0 = person


def person(f, x, y, s=1.0, who="hero", la=(18, 8), ra=(18, 8), **k):   # noqa: F811 — idle life on the whole cast: breathing, blink, small arm sway
    t = _TNOW[0]; ph = x * 0.013
    k.setdefault("bob", 2.2 * math.sin(t * 2.3 + ph)); k.setdefault("blink", (t + ph) % 3.3 < 0.11)
    sw = 3.5 * math.sin(t * 1.9 + ph)
    return _person0(f, x, y, s, who, (la[0] + sw, la[1]), (ra[0] - sw, ra[1]), **k)


def step_card(f, t, sid, n, title, detail=None):
    mini_card(f, f"STEP {n} OF 5", title, op=clamp((t - st0(sid)) / 0.2))


def src(f, t, t0, text, y=1440):
    if t >= t0: comp(f, chip(text, (20, 20, 26), WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def mouth_m(t, lines=MLINES):
    return talk(t) if any(L0(l) <= t <= L1(l) for l in lines) else 0


def night_house(f, t, cx=540, cy=1040, w=840, lit=1.0, t_on=-0.55, win=1.0, roof=True, eave=True, speed=1400, r=13, step=44):
    comp(f, house_flat_el(w, win=win), cx, cy)
    if roof: bulb_string(f, roof_pts(cx, cy, w), t, t_on, speed, step, r, on=lit)
    if eave: bulb_string(f, eave_pts(cx, cy, w), t, t_on + 0.25, speed, step, r, on=lit, wire=True)


def step_pills(f, t, t0, y=1120, red=None, w=170):
    names = [("COVER", (40, 110, 220)), ("GEAR", (36, 160, 90)), ("LADDER", (240, 140, 20)), ("PRICE", (150, 60, 200)), ("SUPPLY", (220, 60, 70))]
    for i, (w_, c_) in enumerate(names):
        rot_comp(f, numcard_el(str(i + 1), w_, c_, w), 200 + 170 * i, y + (24 if i % 2 else -24), 0, pin(t, t0 + 0.14 * i, 0.3), 1.0, 0.3)


def rings3(f, pts, t, t0, gap=0.5):
    for i, (x, y) in enumerate(pts):
        k = clamp((t - t0 - i * gap) / 0.22)
        if k <= 0: continue
        cv2.circle(f, (int(x), int(y)), int(40 + 14 * math.sin(t * 5 + i)), (1.0, 0.86, 0.2), int(9 * k), cv2.LINE_AA)
        comp(f, chip(str(i + 1), (250, 200, 50), INK, 40), x, y - 74, op=k)


# ---- S0: frame 1 — night street, hero on the ladder, lights running along the roof, homeowner holds up cash ----
def shot_S0(t, n):
    f = set_view("wintry", t, zoom=1.0, drift=0)
    snow(f, t, 34)
    night_house(f, t, 560, 1030)
    ladder(f, 214, 1470, 182, 1000)
    person(f, 340, 1660, 0.86, HERO, la=(18, 8), ra=(100, 150), brow="up", look=(1, -1), expr="smirk")
    person(f, 830, 1650, 0.86, OWNER, la=(18, 8), ra=(120, 140), brow="up", look=(-1, -1), hold=scale_el(cash_el(), 0.34), hold_off=(10, -30))
    say(f, "PAY A STRANGER?", 560, 118, YEL_)
    mini_card(f, "NOVEMBER", "YOUR STREET")
    if t >= 1.5: series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S1: you, a ladder on your shoulder, a thought cloud with a lit house ----
def shot_S1(t, n):
    u = lt(t, "S1")
    f = set_view("wintry", t, zoom=1.08 + 0.01 * u, cy=1020)
    snow(f, t, 26)
    ladder(f, 90, 1500, 560, 1270, width=60)
    person(f, 320, 1660, 1.05, HERO, la=(18, 8), ra=(60, 110), brow="up", look=(1, -1), expr="wow" if t > Tw("i2", "Could") else "n")
    k = clamp((t - Tw("i2", "ladder", -0.2)) / 0.3)
    if k > 0: thought(f, 700, 860, 400, scale_el(house_flat_el(300), 0.92), op=k)
    if t >= Tw("i2", "Could", -0.1): say(f, "FOR MONEY?", 560, 130, YEL_, t=t, t0=Tw("i2", "Could", -0.1))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S2: why they pay: 15,000 ER visits ----
def shot_S2(t, n):
    u = lt(t, "S2")
    f = stage("cream"); snow(f, t, 20, 5)
    t0 = Tw("i3", "fifteen", -0.1)
    q = int(14900 * eo(clamp((t - t0) / 0.7))) if t >= t0 else 0
    td = Tw("i3", "decorating", -0.15)
    if t >= td: comp(f, sign_el("ER", (225, 45, 60), WHITE, 120, pole=False), 540, 1000, scale=pin(t, td))
    if t >= t0: say(f, f"~{q:,}" if q < 14900 else "NEARLY 15,000", 700, 170, YEL_, keep=True)
    say(f, "HOLIDAY DECORATING" if t >= td else "ONE LIKELY REASON", 560, 84 if t >= td else 100, WHITE)
    person(f, 540, 1640, 0.82, HERO, la=(30, 20), ra=(30, 20), brow="up", look=(0, -1), expr="wow", sweat=True)
    src(f, t, t0, "All US decorating injuries, 2022–23 season · CPSC")
    return finish(f, n)


# ---- S3: nearly half = falls ----
def shot_S3(t, n):
    f = stage("cream"); snow(f, t, 20, 5)
    t0 = Tw("i4", "half", -0.2)
    for i in range(10):
        x = 150 + 87 * i; y = 1060; k = clamp((t - t0 - i * 0.06) / 0.2) * (1.0 if i < 4 else (0.7 if i == 4 else 0.0))
        cv2.circle(f, (x, y), 36, (0.95, 0.95, 0.98), -1, cv2.LINE_AA)
        if k > 0:
            ov = f.copy(); cv2.circle(ov, (x, y), 36, (0.91, 0.25, 0.27), -1, cv2.LINE_AA); yy = int(y + 36 - 72 * k); f[yy:y + 37, x - 37:x + 37] = ov[yy:y + 37, x - 37:x + 37]
        cv2.circle(f, (x, y), 36, (0.09, 0.08, 0.13), 5, cv2.LINE_AA)
    say(f, "NEARLY HALF", 560, 140, YEL_, t=t, t0=st0("S3") + 0.05)
    say(f, "INVOLVED A FALL", 690, 84, WHITE, keep=True, t=t, t0=t0 + 0.2)
    src(f, t, t0, "CPSC, Nov 2024")
    return finish(f, n)


# ---- S4: you ask the crew lead ----
def shot_S4(t, n):
    u = lt(t, "S4")
    f = set_view("wintry", t, zoom=1.05, cy=1000)
    snow(f, t, 26)
    person(f, 270, 1650, 1.0, HERO, la=(18, 8), ra=(70, 50), brow="up", look=(1, 0), mouth=0)
    person(f, 760, 1650, 1.08, CREW, la=(18, 8), ra=(18, 8), brow="up", look=(-1, 0))
    comp(f, chip("CREW LEAD", (24, 170, 100), WHITE, 40), 760, 960, op=clamp(u / 0.3))
    say(f, "MEET THE CREW LEAD", 560, 96, WHITE)
    return finish(f, n)


# ---- S5: crew lead close-up: five steps ----
def shot_S5(t, n):
    u = lt(t, "S5")
    f = set_view("wintry", t, zoom=1.05, cy=1000, blur=2)
    person_head_at(f, 540, 1500, 1.35, CREW, mouth=mouth_m(t), brow="up", look=(0, 0))
    step_pills(f, t, st0("S5") + 0.15, y=860)
    say(f, "5 STEPS", 560, 130, YEL_)
    return finish(f, n)


# ---- STEP 1 ----
def shot_S6(t, n):
    f = set_view("office", t, zoom=1.04, cy=1000)
    person(f, 310, 1650, 1.0, HERO, la=(18, 8), ra=(18, 8), brow="up", look=(1, 0))
    person(f, 770, 1650, 1.0, CREW, la=(18, 8), ra=(110, 70), mouth=mouth_m(t), brow="up", look=(-1, 0))
    comp(f, shield_el(300, "INSURED", (30, 120, 240)), 540, 850, scale=pin(t, st0("S6") + 0.25))
    step_card(f, t, "S6", 1, "GET INSURED")
    return finish(f, n)


def shot_S7(t, n):
    u = lt(t, "S7")
    f = set_view("office", t, zoom=1.1, cy=1060, blur=2)
    comp(f, form_el(520, "LAWN / HANDYMAN POLICY"), 540, 1040, scale=pin(t, st0("S7") + 0.05))
    tw = Tw("a2", "won't", -0.15)
    if t >= tw: rot_comp(f, stamp_el("ROOF WORK?", RED_, 74), 540, 1090, -9, 1 + 0.6 * (1 - pin(t, tw, 0.2)), clamp((t - tw) / 0.12), 0.2)
    say(f, "OFTEN NOT COVERED", 560, 104, YEL_, t=t, t0=tw) if t >= tw else say(f, "YOUR USUAL POLICY?", 560, 104, WHITE)
    if t >= Tw("a2", "So", -0.1):
        comp(f, chip("CALL YOUR AGENT FIRST", (30, 120, 240), WHITE, 42), 540, 1370, op=clamp((t - Tw("a2", "So", -0.1)) / 0.2))
    src(f, t, tw + 0.3, "Turf Magazine, Dec 2025", y=1465)
    return finish(f, n)


def shot_S8(t, n):
    u = lt(t, "S8")
    f = set_view("wintry", t, zoom=1.06, cy=1040)
    night_house(f, t, 540, 1030, lit=0.8, eave=True)
    t1 = Tw("a3", "Electrical", -0.15)
    person(f, 250, 1650, 0.92, HERO, la=(18, 8), ra=(120, 130), brow="up", look=(1, -1), expr="smirk" if t < t1 else "n")
    if t >= t1:
        person(f, 830, 1650, 0.92, SPARKY, la=(18, 8), ra=(70, 40), brow="up", look=(-1, 0), op=clamp((t - t1) / 0.2))
    if t < t1: say(f, "YOU HANG LIGHTS", 560, 108, YEL_)
    else: say(f, "WIRING = ELECTRICIAN", 560, 92, WHITE, t=t, t0=t1)
    src(f, t, t1 + 0.2, "FindLaw, Jun 2025")
    return finish(f, n)


def shot_S9(t, n):
    f = stage("teal")
    comp(f, form_el(480, "CONTRACTOR LICENSE"), 540, 1110, scale=pin(t, st0("S9") + 0.05))
    comp(f, scale_el(magnifier_el(), 0.9), 740 + 26 * math.sin(t * 2.4), 1230)
    say(f, "CONTRACTOR LICENSE?", 560, 96, YEL_, t=t, t0=st0("S9") + 0.05)
    if t >= Tw("a3", "permit.", -0.2): say(f, "CHECK YOUR CITY", 690, 78, WHITE, keep=True, t=t, t0=Tw("a3", "permit.", -0.2))
    src(f, t, Tw("a3", "contractor"), "ZenBusiness, Aug 2026 · rules vary by place")
    return finish(f, n)


# ---- STEP 2 ----
def shot_S10(t, n):
    f = set_view("garage", t, zoom=1.04, cy=1000)
    comp(f, spool_el(380), 540, 1040, scale=pin(t, st0("S10") + 0.2))
    person(f, 860, 1650, 0.96, CREW, la=(120, 150), ra=(18, 8), mouth=mouth_m(t), brow="up", look=(-1, 0))
    person(f, 220, 1650, 0.96, HERO, la=(18, 8), ra=(70, 50), brow="up", look=(1, -1))
    step_card(f, t, "S10", 2, "PRO GEAR", "NOT STORE LIGHTS")
    return finish(f, n)


def shot_S11(t, n):
    u = lt(t, "S11")
    f = set_view("garage", t, zoom=1.1, cy=1000, blur=3)
    pts = [(110, 1000), (320, 1060), (540, 1010), (760, 1060), (970, 1000)]
    t_fail = Tw("b2", "fail", -0.1)
    deadk = clamp((t - t_fail) / 1.6)
    r = np.random.default_rng(4); order = r.permutation(30)
    bulb_string(f, pts, t, st0("S11") - 3, 2000, 60, 22, dead=lambda i: order[i % 30] < 30 * deadk)
    say(f, "STORE STRINGS", 560, 120, WHITE)
    if t >= t_fail: say(f, "FAIL FAST", 690, 120, YEL_, keep=True, t=t, t0=t_fail)
    person(f, 540, 1650, 0.92, HERO, la=(30, 30), ra=(30, 30), brow="sus", look=(0, -1), expr="sus")
    src(f, t, t_fail, "Turf Magazine, Dec 2025 · ZenBusiness, Aug 2026")
    return finish(f, n)


def shot_S12(t, n):
    f = stage("purple")
    t0 = Tw("b3", "two", -0.1); t1 = Tw("b3", "One", -0.1)
    sw = 6 * math.sin(t * 3)
    rot_comp(f, tag_el("ABOUT $2,000" if t < t1 else "ABOUT $5,000", RED_ if t < t1 else (230, 110, 20), WHITE, 92), 540, 900, -5 + sw, pin(t, st0("S12") + 0.05), 1.0, 0.3)
    say(f, "STARTUP BUDGET", 560, 108, YEL_)
    if t >= t1: comp(f, chip("VEHICLE NOT COUNTED", (20, 20, 26), WHITE, 34), 540, 1010, op=clamp((t - t1) / 0.2))
    comp(f, spool_el(280), 360, 1230); ladder(f, 650, 1380, 730, 1070, width=60)
    src(f, t, t0, "Our sums from Jobber (2024) + ZenBusiness (Aug 2026)")
    return finish(f, n)


# ---- STEP 3 ----
def shot_S13(t, n):
    f = set_view("ladderday", t, zoom=1.03, cy=980)
    ladder(f, 540, 1500, 540, 760, width=90)
    person(f, 830, 1650, 0.98, CREW, la=(120, 160), ra=(18, 8), mouth=mouth_m(t), brow="n", look=(-1, 0))
    person(f, 230, 1650, 0.96, HERO, la=(18, 8), ra=(18, 8), brow="up", look=(1, -1), sweat=True)
    step_card(f, t, "S13", 3, "THE LADDER", "RESPECT IT")
    return finish(f, n)


def shot_S14(t, n):
    u = lt(t, "S14")
    f = set_view("ladderday", t, zoom=1.12, cy=1000, blur=3)
    ladder(f, 540, 1680, 540, 650, width=120, rungs=13)
    s = 1.0; y = 1400
    h = person(f, 540, y, s, HERO, la=(170, 178), ra=(170, 178), back=True, shadow=False)
    pts = [tuple(h["l"]) if h and "l" in h else (470, y - 560), tuple(h["r"]) if h and "r" in h else (610, y - 560), (500, y - 10)]
    rings3(f, pts, t, Tw("c2", "Three", -0.1), 0.42)
    say(f, "3 POINTS TO CLIMB", 560, 104, YEL_)
    src(f, t, Tw("c2", "Both", -0.1), "OSHA portable ladder guidance", y=1465)
    return finish(f, n)


def shot_S15(t, n):
    f = set_view("ladderday", t, zoom=1.0, drift=0)
    power_line(f, y=790, x_pole=880, y_ground=1460)
    ladder(f, 300, 1470, 300, 1020, width=70)
    t0 = Tw("c3", "ten", -0.2); k = eo(clamp((t - t0) / 0.3))
    if k > 0: dim_arrow(f, 340, 1010, 340, 1010 - (1010 - 800) * k, (1, 1, 0.3), 8)
    if k > 0.8: comp(f, chip("10 FT MINIMUM", (250, 200, 50), INK, 44), 560, 905, op=clamp((k - 0.8) / 0.2))
    person(f, 180, 1650, 0.88, HERO, la=(18, 8), ra=(70, 60), brow="up", look=(1, -1))
    say(f, "STAY CLEAR", 560, 120, YEL_)
    if t >= Tw("c3", "Use", -0.1):
        comp(f, chip("FIBERGLASS OR WOOD", (30, 150, 90), WHITE, 34), 680, 1260, op=clamp((t - Tw("c3", "Use", -0.1)) / 0.2))
        comp(f, chip("NOT METAL", (225, 45, 60), WHITE, 34), 680, 1330, op=clamp((t - Tw("c3", "metal.", -0.2)) / 0.2))
    if k > 0.8 and t < Tw("c3", "Use", -0.1): comp(f, chip("CAN'T KEEP 10 FT? DON'T HANG THERE", (225, 45, 60), WHITE, 34), 640, 1120, op=clamp((k - 0.8) / 0.2))
    src(f, t, t0 + 0.3, "Electrical Safety Foundation (ESFI)", y=1465)
    return finish(f, n)


def shot_S16(t, n):
    u = lt(t, "S16"); f = set_view("ladderday", t, zoom=1.03, cy=980)
    comp(f, house_flat_el(900, wall=(240, 150, 90), roof=(90, 60, 90), win=0.0, snow_=False), 540, 1090)
    px, py = 800, 930; apx, apy = 560, 768
    person(f, px, py, 0.6, HERO, la=(30, 40), ra=(120, 140), brow="up", look=(-1, -1), shadow=False)
    cv2.line(f, (px, py - 200), (apx, apy), (0.09, 0.08, 0.13), 12, cv2.LINE_AA); cv2.line(f, (px, py - 200), (apx, apy), (1.0, 0.45, 0.1), 7, cv2.LINE_AA)
    cv2.circle(f, (apx, apy), 20, (0.09, 0.08, 0.13), -1, cv2.LINE_AA); cv2.circle(f, (apx, apy), 13, (0.9, 0.9, 0.92), -1, cv2.LINE_AA)
    say(f, "HARNESS + ANCHOR", 560, 108, YEL_, t=t, t0=st0("S16") + 0.1)
    src(f, t, Tw("c4", "harness", -0.1), "Turf Magazine, Dec 2025", y=1465)
    if u > 0: f = cam(f, 1.0 + 0.018 * u, 590, 900)
    return finish(f, n)


def shot_S16b(t, n):
    u = lt(t, "S16b"); f = set_view("ladderday", t, zoom=1.03, cy=980)
    ladder(f, 180, 1480, 190, 1000, width=70)
    person(f, 540, 1660, 1.05, HERO, la=(18, 8), ra=(90, 100), brow="n", look=(0, 0))
    t1 = Tw("c5", "Get", -0.1); t2 = Tw("c5", "Wet,", -0.1)
    if t < t1: say(f, "NO ROOF IS 'SAFE'", 560, 104, WHITE)
    else: say(f, "GET TRAINED FIRST", 560, 108, YEL_, t=t, t0=t1)
    if t >= t2: comp(f, chip("WET, ICY OR WINDY? STAY DOWN", (225, 45, 60), WHITE, 42), 540, 820, scale=pin(t, t2, 0.2))
    src(f, t, t1, "Training: Turf Magazine, Dec 2025", y=1465)
    return finish(f, n)


# ---- STEP 4 ----
RX, RY, RW = 540, 1040, 860


def shot_S17(t, n):
    f = set_view("roofday", t, zoom=1.0, drift=0)
    comp(f, house_flat_el(RW, wall=(240, 150, 90), roof=(90, 60, 90), win=0.0), RX, RY)
    person(f, 200, 1660, 0.96, HERO, la=(18, 8), ra=(70, 50), brow="up", look=(1, -1))
    person(f, 870, 1660, 0.96, CREW, la=(18, 8), ra=(120, 100), mouth=mouth_m(t), brow="up", look=(-1, -1))
    step_card(f, t, "S17", 4, "THE PRICE", "BY THE FOOT")
    return finish(f, n)


def shot_S18(t, n):
    f = set_view("roofday", t, zoom=1.0, drift=0)
    comp(f, house_flat_el(RW, wall=(240, 150, 90), roof=(90, 60, 90), win=0.0), RX, RY)
    t0 = Tw("d2", "two", -0.1); t1 = Tw("d2", "five,", -0.2)
    rot_comp(f, tag_el("$2 A FOOT" if t < t1 else "$2–$5 A FOOT", RED_, WHITE, 88), 540, 1120, -5 + 5 * math.sin(t * 3), pin(t, t0, 0.3), 1.0, 0.3)
    say(f, "WHAT US PROS CHARGE", 560, 96, YEL_)
    if t >= Tw("d2", "before", -0.1): comp(f, chip("LIGHTS EXTRA", (20, 20, 26), WHITE, 38), 540, 1270, op=clamp((t - Tw("d2", "before", -0.1)) / 0.2))
    src(f, t, t0 + 0.3, "Angi, 2025 data · HomeAdvisor, 2022", y=1465)
    return finish(f, n)


def shot_S19(t, n):
    u = lt(t, "S19")
    f = set_view("roofday", t, zoom=1.0, drift=0)
    comp(f, house_flat_el(RW, wall=(240, 150, 90), roof=(90, 60, 90), win=0.0), RX, RY)
    e = eave_pts(RX, RY, RW); k = clamp(u / max(0.5, (SHOT["S19"]["end"] - SHOT["S19"]["start"]) * 0.8))
    tape_run(f, e[0][0], e[0][1], e[1][0], e[1][1], eio(k))
    say(f, f"{int(150 * eio(k))} FT", 560, 170, YEL_)
    src(f, t, st0("S19") + 0.5, "Our example: about 150 ft per house (Jobber's kit guide)", y=1465)
    return finish(f, n)


def shot_S20(t, n):
    f = set_view("roofday", t, zoom=1.0, drift=0)
    comp(f, house_flat_el(RW, wall=(240, 150, 90), roof=(90, 60, 90), win=0.0), RX, RY)
    e = eave_pts(RX, RY, RW); tape_run(f, e[0][0], e[0][1], e[1][0], e[1][1], 1.0)
    t1 = Tw("d4", "Seven", -0.15)
    say(f, "150 FT × $2", 560, 110, WHITE) if t < t1 else say(f, "150 FT × $5", 560, 110, WHITE)
    rot_comp(f, tag_el("$300" if t < t1 else "$750", RED_ if t < t1 else (230, 110, 20), WHITE, 150), 540, 1200, -5 + 5 * math.sin(t * 3), pin(t, st0("S20") + 0.1, 0.3) if t < t1 else pin(t, t1, 0.25), 1.0, 0.3)
    return finish(f, n)


def shot_S21(t, n):
    f = set_view("roofday", t, zoom=1.08, cy=1040, blur=3)
    t0 = Tw("d5", "average", -0.1)
    person(f, 540, 1660, 1.04, HERO, la=(18, 8), ra=(100, 150), brow="up", look=(0, -1), expr="smirk")
    if t >= t0: say(f, "US AVERAGE: ABOUT $440", 560, 88, YEL_, t=t, t0=t0)
    else: say(f, "COMPARE", 560, 130, WHITE)
    if t >= Tw("d5", "That's", -0.1): comp(f, chip("THEIR BILL, NOT YOUR PROFIT", (225, 45, 60), WHITE, 42), 540, 860, op=clamp((t - Tw("d5", "That's", -0.1)) / 0.2))
    src(f, t, t0, "Angi, 2025 data: $443 average, typical range $219–$686", y=1465)
    return finish(f, n)


# ---- STEP 5 ----
def shot_S22(t, n):
    f = set_view("depot", t, zoom=1.03, cy=980)
    person(f, 540, 1660, 1.05, CREW, la=(18, 8), ra=(100, 150), mouth=mouth_m(t), brow="up", look=(0, 0), hold=None)
    comp(f, spool_el(250), 810, 1040, scale=pin(t, st0("S22") + 0.2))
    step_card(f, t, "S22", 5, "SUPPLY THE LIGHTS")
    return finish(f, n)


def shot_S23(t, n):
    f = stage("purple")
    tg = Tw("e2", "He", -0.1)
    q = "Don't ever, ever, ever install client-owned Christmas lights." if t < tg else "Don't ever, ever, ever install client-owned Christmas lights. It turns into a gong show."
    quote_card(f, q, "Dave Moerman, installer, via Jobber Academy (2024)", y=700, t=t, t0=st0("S23") + 0.05)
    person(f, 540, 1660, 0.92, HERO, la=(30, 30), ra=(60, 120), brow="sus", look=(0, -1), expr="wow" if t > Tw("e2", "gong", -0.1) else "n")
    return finish(f, n)


def shot_S24(t, n):
    f = set_view("depot", t, zoom=1.06, cy=1000, blur=2)
    t0 = Tw("e3", "sell", -0.15); t1 = Tw("e3", "lease", -0.15); tc = Tw("e3", "charge", -0.15)
    comp(f, spool_el(340), 540, 1060, scale=pin(t, st0("S24") + 0.05))
    say(f, "YOU SUPPLY THEM" if t < tc else "AND CHARGE FOR THEM", 560, 100, YEL_)
    if t >= t0: comp(f, chip("SELL", (225, 45, 60), WHITE, 70), 250, 790, scale=pin(t, t0, 0.2))
    if t >= t1: comp(f, chip("LEASE", (30, 150, 90), WHITE, 70), 830, 790, scale=pin(t, t1, 0.2))
    person(f, 540, 1680, 0.88, HERO, la=(70, 60), ra=(70, 60), brow="up", look=(0, -1))
    return finish(f, n)


def shot_S24b(t, n):
    f = set_view("depot", t, zoom=1.06, cy=1000, blur=2)
    comp(f, spool_el(300), 540, 1060)
    comp(f, chip("SELL", (225, 45, 60), WHITE, 70), 250, 790)
    say(f, "CLIENT KEEPS + REPAIRS", 560, 88, YEL_)
    person(f, 800, 1680, 0.9, OWNER, la=(70, 60), ra=(18, 8), brow="up", look=(-1, -1))
    person(f, 260, 1680, 0.9, HERO, la=(18, 8), ra=(70, 60), brow="up", look=(1, -1))
    src(f, t, st0("S24b") + 0.2, "Jobber Academy (2024)", y=1465)
    return finish(f, n)


def shot_S25(t, n):
    u = lt(t, "S25")
    f = set_view("wintry", t, zoom=1.0, drift=0)
    snow(f, t, 26)
    t0 = Tw("e5", "reuse", -0.2); t1 = Tw("e5", "next", -0.3)
    lit = 0.0 if t < t1 else clamp((t - t1) / 0.6)
    lit = max(lit, clamp(1 - u / 0.8) if t < t0 else 0)
    night_house(f, t, 540, 1190, w=700, lit=max(lit, 0.0), t_on=t1 if t >= t1 else -9, win=0.7)
    if t < t0:
        comp(f, chip("YOU STORE + REPAIR", (40, 110, 220), WHITE, 56), 540, 760, op=clamp((u - 0.2) / 0.2))
    if t >= t0:
        comp(f, calendar_el("NEXT", "YEAR"), 540, 800, scale=pin(t, t0, 0.3) * 0.62)
    say(f, "LEASE:", 560, 80, WHITE) if t < t0 else say(f, "SAME CLIENT AGAIN?", 560, 104, YEL_)
    if t >= t1: comp(f, chip("NOT GUARANTEED", (20, 20, 26), WHITE, 34), 840, 800, op=clamp((t - t1) / 0.2))
    src(f, t, st0("S25") + 0.2, "Jobber Academy (2024)", y=1465)
    return finish(f, n)


# ---- the catch ----
def shot_S26(t, n):
    f = stage("cream")
    comp(f, year_strip_el(840), 540, 1040, scale=pin(t, st0("S26") + 0.05))
    say(f, "ABOUT 2 MONTHS", 560, 120, YEL_, t=t, t0=Tw("t1", "season", -0.2)) if t >= Tw("t1", "season", -0.2) else say(f, "THE CATCH", 560, 140, WHITE)
    if t >= Tw("t1", "two", -0.1): comp(f, chip("NOVEMBER IS THE BUSIEST", (250, 200, 50), INK, 40), 540, 760, op=clamp((t - Tw("t1", "two", -0.1)) / 0.2))
    src(f, t, Tw("t1", "season"), "Jobber · ZenBusiness (Aug 2026) · Turf (Dec 2025)", y=1340)
    return finish(f, n)


def shot_S26b(t, n):
    f = set_view("january", t, zoom=1.03, cy=980)
    snow(f, t, 24, 9)
    person(f, 300, 1650, 1.0, {"base": "creator", "shirt": (60, 170, 60), "cap": (60, 170, 60)}, la=(18, 8), ra=(60, 40), brow="up", look=(1, 0))
    person(f, 760, 1650, 1.0, {"base": "worker", "cap": (30, 120, 210), "shirt": (30, 120, 210)}, la=(60, 40), ra=(18, 8), brow="up", look=(-1, 0))
    say(f, "SEASONAL WORK", 560, 120, YEL_)
    comp(f, chip("LAWN CREW", (60, 170, 60), WHITE, 40), 300, 1000); comp(f, chip("PRESSURE WASHER", (30, 120, 210), WHITE, 34), 760, 1000)
    src(f, t, st0("S26b") + 0.2, "Jobber Academy (2024)", y=1480)
    return finish(f, n)


# ---- take-away: one street ----
def shot_S27(t, n):
    f = set_view("wintry", t, zoom=1.0, drift=0)
    snow(f, t, 24)
    t0 = Tw("t3", "Price", -0.1)
    houses = [(190, 1240, (40, 56, 130)), (540, 1240, (60, 44, 120)), (890, 1240, (30, 76, 120))]
    for i, (x, y, c) in enumerate(houses):
        comp(f, house_flat_el(330, wall=c, win=0.3), x, y)
        bulb_string(f, roof_pts(x, y, 330), t, t0 + 0.18 * i, 1200, 26, 8, on=1.0 if t >= t0 else 0.0)
    if t < Tw("t3", "Forget", -0.05): say(f, "INSURED + STARTING?", 560, 96, WHITE)
    elif t < t0: say(f, "NOT THE WHOLE TOWN", 560, 96, WHITE)
    else: say(f, "PRICE ONE STREET", 560, 112, YEL_, t=t, t0=t0)
    person(f, 540, 1660, 0.82, HERO, la=(18, 8), ra=(100, 150), brow="up", look=(0, -1), expr="smirk")
    return finish(f, n)


# ---- end card = frame 1 ----
def shot_S28(t, n):
    f = set_view("wintry", t, zoom=1.0, drift=0)
    snow(f, t, 34)
    night_house(f, t, 560, 960, w=760, t_on=st0("S28"))
    person(f, 200, 1340, 0.72, HERO, la=(18, 8), ra=(100, 150), brow="up", look=(1, 0), expr="smirk")
    person(f, 880, 1340, 0.72, CREW, la=(18, 8), ra=(100, 120), brow="up", look=(-1, 0))
    tc = Tw("z1", "Your", -0.15)
    if t < tc: say(f, "SAVE THIS", 560, 150, YEL_)
    else: say(f, "COMMENT ONE WORD", 560, 96, YEL_)
    if t >= tc: choice_card(f, "YOUR ROOF?", "PAY", "DIY", y=1420, t=t, t0=tc)
    return finish(f, n)


def shot_S29(t, n):
    f = set_view("wintry", t, zoom=1.0, drift=0)
    snow(f, t, 34)
    night_house(f, t, 560, 960, w=760, t_on=st0("S28"))
    person(f, 200, 1340, 0.72, HERO, la=(18, 8), ra=(100, 150), brow="up", look=(1, 0), expr="smirk")
    person(f, 880, 1340, 0.72, CREW, la=(18, 8), ra=(100, 170 + 18 * math.sin(t * 9)), brow="up", look=(-1, 0))
    say(f, "SEND TO A CLIMBER", 560, 110, YEL_)
    choice_card(f, "YOUR ROOF?", "PAY", "DIY", y=1420)
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


def _tracked(fn):
    def g(t, n):
        _TNOW[0] = t
        return fn(t, n)
    return g


RENDER = {s["id"]: _tracked(globals()[f"shot_{s['id']}"]) for s in SHOTS}

IMPACTS = [(Tw("i3", "fifteen", -0.1), 0.25, 10), (Tw("a2", "won't", -0.15), 0.25, 8), (Tw("d4", "Seven", -0.15), 0.2, 8), (Tw("e2", "gong", -0.1), 0.25, 8)]
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
