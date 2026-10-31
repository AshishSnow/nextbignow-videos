# ================= shots: HOW TO START · EP 1 — How to start a drone business (colourful stick cast) =================
# Cast: hero (orange beginner = you), MAYA = `girl` (pink pro pilot / mentor), proctor = `inventor` (teal, glasses),
# clients = exec (agent), worker (roofer), girl2 (planner). New layout ideas: drone-camera POV with viewfinder HUD (aerial_view),
# the 5-step roadmap as a flight route (route_map), UK/EU split cards.
def L0(l): return LINES[l]["start"]


def L1(l): return LINES[l]["end"]


def Tw(l, w, d=0.0):
    try: return T(l, w) + d
    except Exception: return L0(l) + d


SERIES_T = "EP 1 · DRONE BUSINESS"
MAYA = "girl"

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", L0("i2") - 0.2, "zoom"), ("S1b", Tw("i2", "One", -0.15), "flash"), ("S2", L0("i3") - 0.25, "whip"),
    ("S3", L0("a1") - 0.25, "whip"), ("S4", L0("a2") - 0.2, "focus"), ("S5", L0("a3") - 0.2, "whip"), ("S5b", Tw("a3", "Then", -0.15), "punch"),
    ("S6", L0("a4") - 0.2, "zoom"), ("S7", L0("a5") - 0.2, "whip"), ("S8", L0("a6") - 0.2, "whip"),
    ("S9", L0("b1") - 0.25, "whip"), ("S10", L0("b2") - 0.2, "punch"), ("S11", L0("b3") - 0.2, "focus"),
    ("S12", L0("c1") - 0.25, "whip"), ("S13", L0("c2") - 0.2, "focus"), ("S13b", Tw("c2", "Drones", -0.15), "punch"), ("S14", L0("c3") - 0.2, "zoom"),
    ("S15", L0("d1") - 0.25, "whip"), ("S16", L0("d2") - 0.2, "focus"), ("S17", L0("d3") - 0.2, "whip"), ("S18", L0("d4") - 0.2, "zoom"),
    ("S19", L0("d5") - 0.25, "whip"), ("S20", L0("t1") - 0.2, "flash"), ("S21", L0("t2") - 0.2, "focus"),
    ("S22", L0("e1") - 0.2, "whip"), ("S23", L0("e2") - 0.2, "punch"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


def step_card(f, t, sid, n, title, detail):
    cold_open(f, f"STEP {n} OF 5", "HOW TO START", detail, op=clamp((t - st0(sid)) / 0.2))


def src(f, t, t0, text, y=1440):
    if t >= t0: comp(f, chip(text, (20, 20, 26), WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def hover(t, a=10.0, w=3.0): return a * math.sin(t * w)


# ---- S0: hook — the drone is already over a house for sale; you fly it ----
def shot_S0(t, n):
    u = lt(t, "S0")
    f = set_view("street", t, zoom=1.05 + 0.015 * u, cy=1000)
    comp(f, home_el(460, sign="FOR SALE"), 560, 1270)
    dx = 720 - 180 * eo(clamp((u + 0.6) / 2.2)); dy = 990 + hover(t, 14)
    rot_comp(f, drone_el(420, t), dx, dy, -6 + 4 * math.sin(t * 2), 1.0, 1.0, 0.25)
    person(f, 250, 1500, 0.78, "hero", la=(20, 8), ra=(70, 60), mouth=talk(t) if u > 99 else 0, brow="up", look=(1, -1), expr="wow" if u > 1.2 else "n",
           hold=controller_el(150), hold_off=(-20, -10))
    person(f, 840, 1500, 0.74, MAYA, la=(18, 8), ra=(160, 170), brow="up", look=(-1, -1), mouth=2 if 0.8 < u < 1.4 else 0)
    say(f, "1 DRONE = A BUSINESS?", 730, 110, YEL_)
    cold_open(f, "EP 1", "DRONE BUSINESS", "HOW TO START")
    return finish(f, n)


# ---- S1: what the drone sees — aerial photo of the home ----
def shot_S1(t, n):
    u = lt(t, "S1")
    f = aerial_view(t, 1.18 - 0.05 * u, 540, 900, rot=2 * u)
    viewfinder(f, t)
    say(f, "AERIAL PHOTOS", 520, 120, t=t, t0=Tw("i2", "aerial", -0.1))
    say(f, "OF HOMES FOR SALE", 1390, 80, YEL_, t=t, t0=Tw("i2", "homes", -0.1))
    return finish(f, n)


# ---- S1b: click — the shot becomes money ----
def shot_S1b(t, n):
    u = lt(t, "S1b")
    f = aerial_view(t, 1.0, 540, 900, rot=0)
    f[:] = cv2.GaussianBlur(f, (0, 0), 6) * 0.75
    rot_comp(f, photo_el("home", 420), 400, 1020, -7, pin(t, st0("S1b"), 0.3), 1.0, 0.35)
    tc = Tw("i2", "three", -0.15)
    for i in range(6):
        q = t - tc - i * 0.1
        if q <= 0: continue
        rot_comp(f, scale_el(cash_el(), 0.5), 700 + (-1) ** i * 60 * min(1, q * 2), 1240 - 380 * q + 300 * q * q, (-1) ** i * 18 * q, 1.0, clamp(2.4 - q), 0.2)
    if t >= tc: comp(f, tag_el("~$300", GRN_, WHITE, 96), 740, 860, scale=pin(t, tc, 0.25))
    say(f, "PER SHOOT", 520, 130, t=t, t0=tc)
    src(f, t, tc + 0.5, "Example rate: TheDroneU cost guide (May 2026)")
    return finish(f, n)


# ---- S2: the plan in five steps — a flight route; step 5 is red ----
def shot_S2(t, n):
    u = lt(t, "S2")
    f = stage("sky", (255, 255, 255), 540, 1100, 480)
    tf = Tw("i3", "five", -0.1); tl = Tw("i3", "lose", -0.1)
    k = clamp((t - tf - 1.3) / 1.6) * 5
    route_map(f, t, k, 5 if t >= Tw("i3", "Step", -0.1) else 0, y0=800, y1=1430, t_pop=st0("S2") + 0.05)
    ui_word(f, "the whole plan in", "5 STEPS", 470, t, st0("S2") + 0.1, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    if t >= tl: rot_comp(f, stamp_el("LOSE $$$", RED_, 62), 610, 640, -10, 1.5 - 0.5 * eo(clamp((t - tl) / 0.2)), clamp((t - tl) * 6), 0.0)
    return finish(f, n)


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


# ---- S3: STEP 1 — get licensed: you walk into a testing centre ----
def shot_S3(t, n):
    u = lt(t, "S3")
    f = set_view("office", t, zoom=1.0 + 0.02 * u, cy=980)
    wk = walk(t, 1.0) if u < 1.6 else {}
    person(f, 180 + 230 * eo(clamp(u / 1.8)), 1500, 0.8, "hero", **wk, brow="up", look=(1, 0))
    person(f, 820, 1500, 0.76, "inventor", la=(18, 8), ra=(120, 160), mouth=0, brow="n", look=(-1, 0))
    comp(f, chip("TESTING CENTER", (40, 110, 220), WHITE, 34), 820, 860)
    say(f, "GET LICENSED", 700, 150, t=t, t0=st0("S3") + 0.1)
    step_card(f, t, "S3", 1, "GET LICENSED", "FAA PART 107")
    return finish(f, n)


# ---- S4: the licence is called Part 107 ----
def shot_S4(t, n):
    u = lt(t, "S4")
    f = set_view("office", t, zoom=1.5, cx=540, cy=1150, blur=6)
    rot_comp(f, form_el(520, "FAA REMOTE PILOT", None), 400, 1060, -4, pin(t, st0("S4") + 0.05, 0.3) * 1.25, 1.0, 0.35)
    tp = Tw("a2", "Part", -0.12)
    if t >= tp: rot_comp(f, stamp_el("PART 107", RED_, 80), 400, 1150, -12, 1.6 - 0.6 * eo(clamp((t - tp) / 0.2)), clamp((t - tp) * 6), 0.0)
    person(f, 860, 1560, 0.82, "inventor", la=(18, 8), ra=(70, -60), mouth=0, brow="up", look=(-1, 0))
    say(f, "FLYING FOR MONEY?", 520, 110, t=t, t0=Tw("a2", "flying", -0.1))
    src(f, t, tp + 0.4, "FAA: commercial flying needs a Part 107 certificate")
    return finish(f, n)


# ---- S5: age 16+ ----
def shot_S5(t, n):
    u = lt(t, "S5")
    f = stage("orange", YEL_, 540, 1000, 440)
    ts = Tw("a3", "sixteen", -0.15)
    person_head_at(f, 540, 1150, 1.6, "hero", brow="up", expr="wow" if t >= ts else "n", look=(0, -1))
    if t >= ts: rot_comp(f, tag_el("AGE 16+", (40, 110, 220), WHITE, 120), 540, 700, -6, pin(t, ts, 0.25), 1.0, 0.3)
    say(f, "AT LEAST", 470, 90, t=t, t0=Tw("a3", "least", -0.2))
    return finish(f, n)


# ---- S5b: then a 60-question test at a testing centre ----
def shot_S5b(t, n):
    u = lt(t, "S5b")
    f = set_view("office", t, zoom=1.35, cx=540, cy=1100, blur=4)
    tq = Tw("a3", "sixty", -0.12); k = clamp((t - tq) / 2.4)
    qn = max(1, int(1 + 59 * k))
    comp(f, pc_el(620, k, f"QUESTION {qn} / 60"), 540, 1000, scale=pin(t, st0("S5b"), 0.3))
    person(f, 170, 1600, 0.75, "hero", la=(18, 8), ra=(60, 40), brow="sus", expr="sus", look=(1, -1), sweat=k > 0.5)
    say(f, "60 QUESTIONS", 470, 140, t=t, t0=tq)
    src(f, t, tq + 0.5, "Pass mark 70% · FAA-approved test centre")
    return finish(f, n)


# ---- S6: the test costs about $175 ----
def shot_S6(t, n):
    u = lt(t, "S6")
    f = stage("emerald", GOLD, 540, 1000, 440)
    rot_comp(f, form_el(500, "PART 107 TEST", None), 540, 1080, -3, 1.15, 1.0, 0.35)
    tc = Tw("a4", "seventy", -0.25)
    if t >= tc:
        k = clamp((t - tc) / 0.25); rot_comp(f, tag_el("~$175", RED_, WHITE, 120), 600, 760 + 220 * eo(k), 8 - 14 * k, 1.0, 1.0, 0.3)
    person(f, 880, 1560, 0.7, "hero", la=(150, 200), ra=(150, 200), expr="wow" if t >= tc + 0.2 else "n", brow="up", look=(-1, -1))
    say(f, "THE TEST COSTS", 470, 100, t=t, t0=st0("S6") + 0.1)
    src(f, t, tc + 0.6, "Knowledge test fee ~$175 (PSI testing, 2026)")
    return finish(f, n)


# ---- S7: every two years a free online refresher ----
def shot_S7(t, n):
    u = lt(t, "S7")
    f = stage("purple", (255, 120, 190), 540, 1020, 440)
    comp(f, calendar_el("EVERY", "2 YRS"), 330, 1050, scale=0.85 * pin(t, st0("S7") + 0.05, 0.3))
    comp(f, pc_el(460, 1.0, "ONLINE REFRESHER"), 760, 1080, scale=pin(t, st0("S7") + 0.25, 0.3))
    tf = Tw("a5", "free", -0.12)
    if t >= tf: rot_comp(f, stamp_el("FREE", GRN_, 90), 760, 820, -10, 1.6 - 0.6 * eo(clamp((t - tf) / 0.2)), clamp((t - tf) * 6), 0.0)
    tcur = Tw("a5", "current.", -0.1)
    if t >= tcur: comp(f, check_el(70, True), 540, 1420, scale=pin(t, tcur, 0.25))
    say(f, "STAY CURRENT", 470, 130, t=t, t0=tcur - 0.6)
    return finish(f, n)


# ---- S8: UK / Europe: registration + online test ----
def shot_S8(t, n):
    u = lt(t, "S8")
    f = stage("teal", (255, 255, 255), 540, 1000, 460)
    tu = Tw("a6", "UK", -0.12); te = Tw("a6", "Europe,", -0.12)
    if t >= tu: rot_comp(f, uk_eu_card_el("UK", ("OPERATOR ID", "+ FLYER ID TEST"), (30, 90, 200), 400), 300, 960, -4, pin(t, tu, 0.3), 1.0, 0.3)
    if t >= te: rot_comp(f, uk_eu_card_el("EU", ("REGISTER", "+ A1/A3 TEST"), (110, 60, 210), 400), 780, 960, 4, pin(t, te, 0.3), 1.0, 0.3)
    person(f, 540, 1560, 0.7, "girl2", la=(18, 8), ra=(150, 170 + 20 * math.sin(t * 10)), mouth=talk(t), brow="up")
    say(f, "IN THE UK OR EUROPE", 470, 100, t=t, t0=st0("S8") + 0.05)
    src(f, t, Tw("a6", "online", 0.2), "UK CAA: Operator ID £12.34/yr · EASA: A1/A3 online test", 610)
    return finish(f, n)


# ---- S9: STEP 2 — register your drone (workbench) ----
def shot_S9(t, n):
    u = lt(t, "S9")
    f = set_view("study", t, zoom=1.05, cy=1000)
    up = eo(clamp((u - 0.3) / 0.6))
    person(f, 540, 1520, 0.85, "hero", la=(150, 190), ra=(150, 190), brow="up", expr="wow" if up > 0.8 else "n", look=(0, -1))
    rot_comp(f, drone_el(360, t), 540, 1040 - 230 * up + hover(t, 4 * up), 0, 1.0, 1.0, 0.25)
    say(f, "REGISTER IT", 700, 150, t=t, t0=st0("S9") + 0.1)
    step_card(f, t, "S9", 2, "REGISTER IT", "FAA DRONEZONE")
    return finish(f, n)


# ---- S10: $5 per drone, lasts three years ----
def shot_S10(t, n):
    u = lt(t, "S10")
    f = stage("yellow", (255, 255, 255), 540, 1000, 460)
    rot_comp(f, drone_el(560, t), 540, 1050 + hover(t, 8), -3, pin(t, st0("S10"), 0.3), 1.0, 0.3)
    comp(f, chip("FAA DRONEZONE · REGISTER", (30, 90, 200), WHITE, 40), 540, 640, scale=pin(t, st0("S10") + 0.15, 0.25))
    t5 = Tw("b2", "five", -0.15); t3 = Tw("b2", "three", -0.15)
    if t >= t5: rot_comp(f, tag_el("$5", RED_, WHITE, 130), 380, 900, -12, 1.7 - 0.7 * eo(clamp((t - t5) / 0.18)), clamp((t - t5) * 6), 0.3)
    if t >= t3: rot_comp(f, calendar_el("LASTS", "3 YRS"), 760, 1330, 6, 0.6 * pin(t, t3, 0.3), 1.0, 0.3)
    say(f, "PER DRONE", 470, 130, YEL_, t=t, t0=t5 + 0.1)
    src(f, t, t3 + 0.6, "FAA drone registration: $5, valid 3 years", 1490)
    return finish(f, n)


# ---- S11: Remote ID — a digital licence plate ----
def shot_S11(t, n):
    u = lt(t, "S11")
    f = sky_bg(t)
    tr = Tw("b3", "Remote", -0.15); k = eo(clamp((t - tr) / 0.35))
    dx, dy = 540 + 40 * math.sin(t * 0.8), 980 + hover(t, 12)
    if t >= tr: waves(f, dx, dy, t, op=0.8)
    rot_comp(f, drone_el(520, t), dx, dy, 3 * math.sin(t * 1.3), 1.0, 1.0, 0.3)
    if k > 0: comp(f, remote_id_el(430), dx, dy + 230 - 120 * (1 - k), op=k, scale=0.7 + 0.3 * k)
    say(f, "BROADCASTS", 470, 120, t=t, t0=Tw("b3", "broadcast", -0.12))
    tl = Tw("b3", "digital", -0.15)
    if t >= tl: comp(f, chip("like a digital license plate", (30, 110, 230), WHITE, 40), 540, 1460, scale=pin(t, tl, 0.25))
    return finish(f, n)


# ---- S12: STEP 3 — pick your gear (store) ----
def shot_S12(t, n):
    u = lt(t, "S12")
    f = set_view("store", t, zoom=1.08 + 0.02 * u, cy=980)
    for i, (x, col) in enumerate(((300, (245, 245, 250)), (540, (60, 62, 72)), (780, (255, 210, 60)))):
        comp(f, drone_el(270, t * 0.0 + i, col=col, accent=((40, 110, 220), (255, 80, 80), (30, 160, 80))[i]), x, 1000 + 8 * math.sin(t * 2 + i))
        comp(f, chip(("$", "$$", "$$$")[i], INK, WHITE, 30), x, 1110)
    person(f, 220 + 120 * eo(clamp(u / 1.5)), 1520, 0.78, "hero", la=(18, 8), ra=(80, 40), brow="up", look=(1, -1), expr="n")
    say(f, "PICK YOUR GEAR", 700, 150, t=t, t0=st0("S12") + 0.1)
    step_card(f, t, "S12", 3, "PICK YOUR GEAR", "RULES AS OF OCT 2026")
    return finish(f, n)


# ---- S13: heads up — new models can't get FCC approval ----
def shot_S13(t, n):
    u = lt(t, "S13")
    f = set_view("store", t, zoom=1.2, cx=540, cy=1000, blur=3)
    tn = Tw("c2", "new", -0.1); k = eo(clamp((t - tn) / 0.4))
    comp(f, drone_el(300, 0.0, col=(60, 62, 72)), 540, 1050, op=1 - 0.5 * k)
    if k > 0: rot_comp(f, sign_el("NEW MODELS: NO FCC OK", RED_, WHITE, 52, False), 540, 520 + 300 * k, -4 + 3 * math.sin(t * 6) * (1 - k), 1.0, 1.0, 0.3)
    person(f, 230, 1560, 0.78, "hero", la=(150, 200), ra=(40, -40), brow="sus", expr="sus", look=(1, -1))
    person(f, 850, 1560, 0.76, MAYA, la=(18, 8), ra=(70, 120), mouth=talk(t), brow="up", look=(-1, 0))
    say(f, "HEADS UP", 470, 120, YEL_, t=t, t0=st0("S13") + 0.05)
    src(f, t, Tw("c2", "approval", 0.0), "FCC Covered List (Dec 2025) · DJI appeal pending · Oct 2026", 1240)
    return finish(f, n)


# ---- S13b: drones you already own still fly ----
def shot_S13b(t, n):
    u = lt(t, "S13b")
    f = set_view("street", t, zoom=1.15, cy=900)
    dx, dy = 540 + 120 * math.sin(u * 1.4), 820 + hover(t, 16)
    rot_comp(f, drone_el(400, t), dx, dy, 6 * math.cos(u * 1.4), 1.0, 1.0, 0.3)
    person(f, 360, 1560, 0.82, "hero", la=(20, 8), ra=(70, 60), brow="up", expr="smirk", look=(1, -1), hold=controller_el(150), hold_off=(-20, -10))
    person(f, 820, 1560, 0.78, MAYA, la=(18, 8), ra=(150, 175), brow="up", mouth=2 if u < 0.6 else 0)
    ts = Tw("c2", "still", -0.15)
    if t >= ts: comp(f, check_el(70, True), 760, 650, scale=pin(t, ts, 0.25))
    say(f, "YOURS STILL FLIES", 520, 120, GRN_ if False else WHITE, t=t, t0=ts)
    return finish(f, n)


# ---- S14: liability insurance — often under $1,200 a year ----
def shot_S14(t, n):
    u = lt(t, "S14")
    f = stage("sky", (255, 255, 255), 540, 1020, 460)
    ti = Tw("c3", "insurance.", -0.2); k = eo(clamp((t - ti) / 0.4))
    if k > 0: comp(f, shield_el(560), 540, 1060, scale=0.6 + 0.4 * k, op=0.9 * k)
    rot_comp(f, drone_el(400, t), 540, 980 + hover(t, 8), 0, 1.0, 1.0, 0.3)
    say(f, "LIABILITY INSURANCE", 470, 110, t=t, t0=Tw("c3", "liability", -0.1))
    tw_ = Tw("c3", "twelve", -0.2)
    if t >= tw_: comp(f, tag_el("often < $1,200/yr", GRN_, WHITE, 70), 540, 1430, scale=pin(t, tw_, 0.25))
    src(f, t, tw_ + 0.6, "Typical $1M cover: ~$500–1,200/yr (Unmanned Aerial, Aug 2026)", 600)
    return finish(f, n)


# ---- S15: STEP 4 — find your first clients (street) ----
def shot_S15(t, n):
    u = lt(t, "S15")
    f = set_view("street", t, zoom=1.0 + 0.02 * u, cy=1000)
    person(f, 260, 1500, 0.8, "hero", la=(18, 8), ra=(110, 150), mouth=talk(t), brow="up", look=(1, 0),
           hold=photo_el("home", 120), hold_off=(10, -50))
    for i, (who, x) in enumerate((("exec", 560), ("worker", 720), ("girl2", 880))):
        if u > 0.3 + 0.2 * i:
            person(f, x, 1500, 0.66, who, la=(18, 8), ra=(150, 170 + 15 * math.sin(t * 9 + i)), brow="up", look=(-1, 0), op=clamp((u - 0.3 - 0.2 * i) * 4))
    say(f, "FIRST CLIENTS", 700, 150, t=t, t0=st0("S15") + 0.1)
    step_card(f, t, "S15", 4, "FIRST CLIENTS", "WHO PAYS FOR SKY SHOTS")
    return finish(f, n)


# ---- S16: agents, roofers, event planners ----
def shot_S16(t, n):
    u = lt(t, "S16")
    f = stage("teal", YEL_, 540, 1000, 470)
    for i, (who, x, lab, w_) in enumerate((("exec", 240, "AGENT", "agents,"), ("worker", 540, "ROOFER", "roofers"), ("girl2", 840, "PLANNER", "planners"))):
        tw_ = Tw("d2", w_, -0.12); on = t >= tw_
        k = pin(t, tw_, 0.3) if on else 0.0
        person(f, x, 1440 - 30 * (k - 1) * on, 0.68, who, la=(18, 8), ra=(150, 175) if on else (18, 8), mouth=2 if on and t < tw_ + 0.5 else 0,
               brow="up" if on else "n", op=1.0 if on else 0.45)
        if on: comp(f, chip(lab, (30, 30, 40), WHITE, 34), x, 1490, scale=k)
    tsky = Tw("d2", "sky.", -0.2)
    if t >= tsky: rot_comp(f, drone_el(300, t), 540, 640 + hover(t, 10), 0, pin(t, tsky, 0.3), 1.0, 0.3)
    say(f, "WHO NEEDS SKY SHOTS?", 470 if t < tsky else 470, 100, t=t, t0=st0("S16") + 0.1)
    return finish(f, n)


# ---- S17: what they pay — rates vary ----
def shot_S17(t, n):
    u = lt(t, "S17")
    f = stage("orange", YEL_, 540, 1000, 460)
    tv = Tw("d3", "vary", -0.15); th = Tw("d3", "home", -0.12); tr = Tw("d3", "roof", -0.12)
    rot_comp(f, photo_el("home", 320), 300, 1000, -6, pin(t, st0("S17") + 0.05, 0.3) * (1.0 + 0.08 * pin(t, th, 0.25) * (t >= th)), 1.0, 0.3)
    rot_comp(f, photo_el("roof", 320), 780, 1000, 6, pin(t, st0("S17") + 0.2, 0.3) * (1.0 + 0.08 * pin(t, tr, 0.25) * (t >= tr)), 1.0, 0.3)
    if t >= th: comp(f, chip("$150–300", GRN_, WHITE, 54), 300, 1240, scale=pin(t, th + 0.2, 0.25))
    if t >= tr: comp(f, chip("$150–400", GRN_, WHITE, 54), 780, 1240, scale=pin(t, tr + 0.2, 0.25))
    say(f, "RATES VARY BY CITY", 470, 110, t=t, t0=tv - 0.3)
    src(f, t, Tw("d3", "hundred", 0.0), "Typical ranges: TheDroneU (May 2026), SkyeBrowse (Mar 2026)", 1400)
    return finish(f, n)


# ---- S18: shoot three free samples -> portfolio ----
def shot_S18(t, n):
    u = lt(t, "S18")
    f = stage("emerald", GOLD, 540, 1000, 460)
    rot_comp(f, drone_el(300, t), 540 + 200 * math.sin(u * 1.2), 700 + hover(t, 10), 0, 1.0, 1.0, 0.3)
    tp = Tw("d4", "portfolio.", -0.3); kp = eo(clamp((t - tp) / 0.5))
    for i, kind in enumerate(("home", "roof", "party")):
        ti = st0("S18") + 0.15 + 0.5 * i
        if t < ti: continue
        x0, y0 = 260 + 280 * i, 1060
        x, y = x0 + (540 - x0) * kp, y0 + (1120 - y0) * kp + i * 10 * kp
        rot_comp(f, photo_el(kind, 250), x, y, (-8 + 8 * i) * (1 - kp) + (i - 1) * 4 * kp, pin(t, ti, 0.25), 1.0, 0.3)
        if t < ti + 0.15: f[:] = f + 0.18
    if kp > 0.9: comp(f, chip("YOUR PORTFOLIO", (30, 30, 40), WHITE, 44), 540, 1360, scale=pin(t, tp + 0.45, 0.25))
    hud_rule(f, 4, "SHOOT 3 FREE SAMPLES", 470, t=t, t0=Tw("d4", "free", -0.3))
    return finish(f, n)


# ---- S19: STEP 5 — the big mistake: dusk, the drone drifts into a no-fly zone ----
def shot_S19(t, n):
    u = lt(t, "S19")
    f = set_view("dusk", t, zoom=1.05, cy=1000)
    ta = Tw("d5", "flying", -0.2); ka = eo(clamp((t - ta) / 1.6))
    if t >= ta - 0.4: nofly_ring(f, 700, 1300, 260, t, op=clamp((t - ta + 0.4) * 3))
    rot_comp(f, drone_el(300, t), 380 + 330 * ka, 820 + hover(t, 10), 10 * ka, 1.0, 1.0, 0.3)
    panic = t >= Tw("d5", "allowed.", -0.3)
    person(f, 220, 1540, 0.8, "hero", la=(150, 200) if panic else (20, 8), ra=(150, 200) if panic else (70, 60), brow="sad" if panic else "up",
           expr="wow" if panic else "n", sweat=panic, look=(1, -1), hold=None if panic else controller_el(150), hold_off=(-20, -10))
    if t >= ta + 0.3: comp(f, chip("NO-FLY ZONE", RED_, WHITE, 40), 700, 1180, scale=pin(t, ta + 0.3, 0.25))
    say(f, "THE BIG MISTAKE", 700, 140, RED_ if False else WHITE, t=t, t0=st0("S19") + 0.1)
    step_card(f, t, "S19", 5, "THE BIG MISTAKE", "WHERE YOU FLY")
    return finish(f, n)


# ---- S20: fines up to $75,000 per violation ----
def shot_S20(t, n):
    u = lt(t, "S20")
    f = stage("red", YEL_, 540, 1000, 460)
    rot_comp(f, drone_el(380, 0.0), 540, 1120, -12, 1.0, 1.0, 0.3)
    tv = Tw("t1", "seventy", -0.2)
    if t >= tv:
        k = clamp((t - tv) / 0.18); rot_comp(f, stamp_el("FINE", WHITE, 80), 540, 860, -10, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.0)
    ui_word(f, "FAA fines up to", "$75,000", 470, t, Tw("t1", "fines", -0.15), col=YEL_, size=190, shadow=0.4, lead_col=WHITE, tail="per violation")
    src(f, t, tv + 0.8, "FAA newsroom, Feb 2026: up to $75,000 per violation", 1440)
    return finish(f, n)


# ---- S21: check the airspace app before every flight ----
def shot_S21(t, n):
    u = lt(t, "S21")
    f = set_view("street", t, zoom=1.35, cx=540, cy=1000, blur=6)
    te = Tw("t2", "every", -0.2); ok = t >= te
    comp(f, airspace_phone_el(ok, 400), 600, 1000, scale=pin(t, st0("S21"), 0.3))
    if ok and t < te + 0.5:
        rr = (t - te) / 0.5; cv2.circle(f, (600, 1320), int(30 + 160 * rr), C((255, 255, 255)), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
    person(f, 210, 1600, 0.8, MAYA, la=(18, 8), ra=(70, 100), mouth=talk(t), brow="up", look=(1, -1))
    say(f, "CHECK FIRST", 470, 150, t=t, t0=Tw("t2", "check", -0.1))
    src(f, t, te + 0.4, "FAA B4UFLY app · LAANC approval apps", 1450)
    return finish(f, n)


# ---- S22: save this — loop back to frame 1 (same street, same house) ----
def shot_S22(t, n):
    u = lt(t, "S22")
    f = set_view("street", t, zoom=1.05, cy=1000)
    comp(f, home_el(460, sign="FOR SALE"), 560, 1270)
    rot_comp(f, drone_el(420, t), 540, 990 + hover(t, 14), -4, 1.0, 1.0, 0.25)
    hi = 0.6 < u < 1.6
    person(f, 360 if hi else 250, 1500, 0.78, "hero", la=(20, 8), ra=(170, 160) if hi else (70, 60), brow="up", expr="n", look=(1, 0), mouth=2 if hi else 0)
    person(f, 720 if hi else 840, 1500, 0.74, MAYA, la=(170, 160) if hi else (18, 8), ra=(18, 8), brow="up", look=(-1, 0), mouth=2 if hi else 0)
    say(f, "SAVE THIS", 590, 150, YEL_, t=t, t0=Tw("e1", "Save", -0.1))
    say(f, "BEFORE YOUR FIRST DRONE", 710, 80, t=t, t0=Tw("e1", "before", -0.1))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S23: your move end card — which step scares you? then send + follow ----
def shot_S23(t, n):
    u = lt(t, "S23")
    f = stage("purple", GOLD, 540, 1000, 460)
    rot_comp(f, drone_el(300, t), 540 + 260 * max(0, u - 3.2) ** 1.5, 900 + hover(t, 10), 8 * max(0, u - 3.2), 1.0, 1.0, 0.3)
    person(f, 300, 1300, 0.62, "hero", la=(18, 8), ra=(80, 20), brow="up", look=(1, 0), mouth=2 if u < 0.6 else 0)
    person(f, 780, 1300, 0.6, MAYA, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)) if t >= L0("e3") else (18, 8), brow="up", look=(-1, 0))
    choice_card(f, "WHICH STEP SCARES YOU?", "STEP 1", "STEP 5", y=660, t=t, t0=st0("S23") + 0.05, col_a=(40, 110, 220), col_b=(226, 52, 52))
    tf = Tw("e3", "friend", -0.15)
    if t >= tf: say(f, "SEND TO A DRONE FRIEND", 1440, 80, t=t, t0=tf)
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(Tw("i2", "three", -0.15), 0.25, 10), (Tw("i3", "lose", -0.1), 0.3, 12), (Tw("a2", "Part", -0.12), 0.25, 10),
           (Tw("a4", "seventy", 0.0), 0.3, 12), (Tw("b2", "five", -0.15), 0.25, 10), (Tw("c2", "new", 0.25), 0.3, 12),
           (Tw("t1", "seventy", -0.2), 0.4, 20), (Tw("d5", "allowed.", -0.3), 0.3, 12)]


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
