# ================= shots: HOW TO START · EP 3 — How to start a food truck in NYC (line-art stick cast) =================
# Cast: hero (orange tie, white paper cap from step 2 = first-time owner), mentor = veteran truck owner (teal apron shirt), permit holder = grey-tie exec (never shown next to the
# arrests), inspector = navy cap. New vs EP 2: first city-specific how-to, velvet rope = the cap, truck queue = 2022 lists, ticket printer, hand-slide under the table, PRIVATE LOT way out,
# lip sync (talk() = visemes) with real mentor close-ups, doo-wop street-corner score (new genre).
def L0(l): return LINES[l]["start"]


def L1(l): return LINES[l]["end"]


def Tw(l, w, d=0.0, nth=0):
    try: return T(l, w, nth) + d
    except Exception: return L0(l) + d


SERIES_T = "EP 3 · FOOD TRUCK NYC"
HERO = "hero"
HCAP = {"base": "hero", "style": "cap", "cap": (255, 255, 255)}
MENTOR = {"base": "girl", "shirt": (0, 150, 140), "hair": (40, 30, 30)}
HOLDER = {"base": "exec", "tie": (150, 152, 160)}
INSP = {"base": "worker", "cap": (30, 50, 110)}
TEAL = (0, 150, 140)

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", L0("i2") - 0.2, "whip"), ("S2", L0("i3") - 0.2, "zoom"), ("S2b", Tw("i3", "So", -0.2), "punch"),
    ("S3", L0("a1") - 0.25, "whip"), ("S4", L0("a2") - 0.2, "focus"), ("S4b", Tw("a2", "must", -0.2), "punch"), ("S5", L0("a3") - 0.2, "zoom"),
    ("S6", L0("b1") - 0.25, "whip"), ("S7", L0("b2") - 0.2, "focus"), ("S8", L0("b3") - 0.2, "zoom"),
    ("S9", L0("c1") - 0.25, "whip"), ("S10", L0("c2") - 0.2, "flash"), ("S11", L0("c3") - 0.2, "focus"),
    ("S12", L0("e1") - 0.25, "whip"), ("S13", L0("e2") - 0.2, "zoom"), ("S13b", Tw("e2", "capped", -0.5), "punch"), ("S14", L0("e3") - 0.2, "whip"),
    ("S15", L0("e4") - 0.2, "focus"), ("S16", L0("e5") - 0.2, "flash"), ("S17", L0("e6") - 0.2, "whip"),
    ("S18", L0("e7") - 0.2, "flash"), ("S19", L0("t1") - 0.2, "whip"), ("S19b", Tw("t1", "Not", -0.2), "punch"),
    ("S20", L0("t2") - 0.2, "whip"), ("S21", L0("z1") - 0.2, "zoom"), ("S22", Tw("z1", "Still", -0.2), "punch"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


def step_card(f, t, sid, n, title, detail):
    cold_open(f, f"STEP {n} OF 4", title, detail, op=clamp((t - st0(sid)) / 0.2))


def src(f, t, t0, text, y=1440):
    if t >= t0: comp(f, chip(text, (20, 20, 26), WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


def sepia(f, t, t0):
    k = clamp((t - t0) / 0.3)
    if k > 0: f[:] = sepia_tone(f, 0.85 * k)


def truck(w=800, **kw):
    if w >= 260: return foodtruck_el(w, **kw)
    return scale_el(foodtruck_el(260, **kw), w / 260)


def steam(f, x, y, t, n=4, s=1.0):
    for i in range(n):
        ph = (t * 0.55 + i / n) % 1.0; r = int((14 + 40 * ph) * s)
        ov = f.copy(); cv2.circle(ov, (int(x + 30 * math.sin(ph * 5 + i)), int(y - 240 * ph * s)), r, (1.0, 1.0, 1.0), -1, cv2.LINE_AA)
        a = 0.28 * clamp(ph * 6) * clamp(2.2 * (1 - ph)); f[:] = f * (1 - a) + ov * a


def rope(f, x0, x1, y, t, t_close=None, h=170):
    """velvet rope between two brass posts; t_close = the hook clicks across the gap at that moment"""
    k = 1.0 if t_close is None else eback(clamp((t - t_close) / 0.25))
    xm = x0 + (x1 - x0) * k
    for x in (x0, x1):
        cv2.rectangle(f, (int(x - 9), int(y - h)), (int(x + 9), int(y)), (0.72, 0.56, 0.18), -1, cv2.LINE_AA)
        cv2.rectangle(f, (int(x - 9), int(y - h)), (int(x + 9), int(y)), (0.1, 0.08, 0.1), 3, cv2.LINE_AA)
        cv2.circle(f, (int(x), int(y - h)), 17, (0.9, 0.72, 0.25), -1, cv2.LINE_AA); cv2.circle(f, (int(x), int(y - h)), 17, (0.1, 0.08, 0.1), 3, cv2.LINE_AA)
        cv2.ellipse(f, (int(x), int(y)), (46, 13), 0, 0, 360, (0.72, 0.56, 0.18), -1, cv2.LINE_AA)
    pts = np.array([[x0 + (xm - x0) * q, y - h + 8 + 70 * math.sin(q * math.pi) * (0.6 + 0.4 * k)] for q in np.linspace(0, 1, 24)], np.int32)
    cv2.polylines(f, [pts], False, (0.1, 0.06, 0.08), 22, cv2.LINE_AA); cv2.polylines(f, [pts], False, (0.72, 0.1, 0.16), 15, cv2.LINE_AA)


def truck_queue(f, t, y=1290, n=6, x0=120, dx=250, w=270, shift=0.0, col=None):
    for i in reversed(range(n)):
        cols = [(255, 196, 40), (60, 170, 230), (240, 110, 90), (120, 200, 110), (190, 120, 220), (250, 150, 50)]
        comp(f, truck(w, open_=False, menu=None, glow=0.0, permit=False, col=cols[i % 6]), x0 + dx * i + shift, y)


def pills(f, t, t0, y=1040, red=None, w=200):
    names = [("YOU", (40, 110, 220)), ("BASE", (36, 160, 90)), ("TRUCK", (240, 140, 20)), ("PERMIT", (150, 60, 200))]
    for i, (w_, c_) in enumerate(names):
        wob = 8 * math.sin(t * 18) if red == i else 0
        rot_comp(f, numcard_el(str(i + 1), w_, RED_ if red == i else c_, w), 225 + 210 * i, y, wob, pin(t, t0 + 0.12 * i, 0.3), 1.0, 0.3)


# ---- S0: frame 1 — the shut truck, the $200 permit held up, a giant "$$$$$" tag ----
def shot_S0(t, n):
    u = lt(t, "S0")
    f = set_view("street", t, zoom=1.04 + 0.01 * u, cy=980)
    comp(f, truck(800, open_=False, menu=None, permit=False), 560, 1180)
    person(f, 185, 1610, 0.82, HERO, la=(20, 10), ra=(60, 40), brow="sus" if u > 1.0 else "up", look=(1, -1), expr="sus" if u > 1.4 else "n")
    person(f, 890, 1610, 0.8, HOLDER, la=(18, 8), ra=(150, 120), brow="up", look=(-1, 0))
    comp(f, permit_el(340, price="$200"), 370, 880)
    sw = 9 * math.sin(t * 3.6)
    tk = Tw("i1", "thousands", -0.25)
    if t >= tk:
        k = clamp((t - tk) / 0.35)
        rot_comp(f, tag_el("$$$$$", RED_, WHITE, 84), 730, 730 + 150 * eback(k), -8 + sw, 1.0, k, 0.3)
    say(f, "$200 PERMIT", 650, 110) if t < tk else say(f, "RENTED FOR $$$$$?", 650, 92, YEL_, t=t, t0=tk)
    cold_open(f, "2026", "NEW YORK CITY", "YOU: FIRST-TIME OWNER")
    if t >= 1.5: series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S1: you want to sell tacos — dream bubble with truck + queue ----
def shot_S1(t, n):
    u = lt(t, "S1")
    f = set_view("street", t, zoom=1.12 + 0.012 * u, cy=1000)
    person(f, 300, 1600, 1.0, HERO, la=(18, 8), ra=(150, 150), brow="up", look=(1, -1), expr="wow" if u > 1.2 else "n", mouth=0)
    tt = Tw("i2", "tacos", -0.3)
    k = clamp((t - tt) / 0.3)
    if k > 0:
        g = truck(320, menu="TACOS"); thought(f, 690, 800, 360, g, op=k)
        for i in range(3): person(f, 590 + 90 * i, 980, 0.2, ("friend", "lady", "creator")[i], op=k, shadow=False)
    say(f, "NYC · TACOS · A TRUCK", 1440, 80, YEL_, t=t, t0=Tw("i2", "New", -0.1))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S2: the order matters — no permit, no serving ----
def shot_S2(t, n):
    u = lt(t, "S2")
    f = set_view("street", t, zoom=1.2, cx=560, cy=1100, blur=2)
    comp(f, truck(760, open_=False, menu=None, permit=False), 560, 1120)
    tl = Tw("i3", "legally", -0.2)
    if t >= tl: rot_comp(f, sign_el("NOT ALLOWED TO SERVE", RED_, WHITE, 62, pole=False), 560, 1080, -5, pin(t, tl, 0.3), 1.0, 0.3)
    person(f, 170, 1640, 0.82, HERO, la=(18, 8), ra=(40, 70), brow="worry", look=(1, -1), sweat=t >= tl)
    say(f, "WRONG ORDER?", 640, 130, t=t, t0=Tw("i3", "wrong", -0.15))
    return finish(f, n)


def shot_S2b(t, n):
    f = stage("purple", GOLD, 540, 1040, 470)
    pills(f, t, st0("S2b"))
    ui_word(f, "the plan in", "4 STEPS", 470, t, st0("S2b") + 0.05, col=YEL_, size=170, shadow=0.4, lead_col=WHITE)
    tn = Tw("a1", "you", 0)
    return finish(f, n)


# ---- S3: STEP 1 — you, not the truck ----
def shot_S3(t, n):
    u = lt(t, "S3")
    f = set_view("office", t, zoom=1.08 + 0.015 * u, cy=1000)
    tt = Tw("a1", "truck", -0.2)
    comp(f, truck(300, menu=None, open_=False, permit=False), 790, 1330, op=0.9)
    if t >= tt: rot_comp(f, tag_el("NOT YET", RED_, WHITE, 58), 760, 1130, -5, 1.4 - 0.4 * eo(clamp((t - tt) / 0.2)), clamp((t - tt) * 6), 0.3)
    person(f, 320, 1600, 1.0, HERO, la=(150, 40), ra=(18, 8), brow="up", look=(0, 0), mouth="o" if u < 0.9 else 0, expr="smirk" if u > 1.2 else "n")
    say(f, "YOU FIRST", 700, 150, t=t, t0=st0("S3") + 0.1)
    step_card(f, t, "S3", 1, "HOW TO START", "LICENSE YOU")
    return finish(f, n)


# ---- S4: the mentor explains (close-up, real mouth shapes) — vendor license form ----
def shot_S4(t, n):
    u = lt(t, "S4")
    f = set_view("office", t, zoom=1.4, cx=540, cy=1050, blur=6)
    person_head_at(f, 300, 1120, 1.55, MENTOR, la=(18, 8), ra=(18, 8), mouth=talk(t), brow="up", look=(1, 0))
    rot_comp(f, form_el(400, "VENDOR LICENSE"), 730, 960, 5, pin(t, st0("S4") + 0.1, 0.3), 1.0, 0.35)
    say(f, "YOU NEED A LICENSE", 560, 96, YEL_, t=t, t0=Tw("a2", "needs", -0.1))
    src(f, t, Tw("a2", "license", 0.2), "NYC Health Dept., 2026", 1450)
    return finish(f, n)


def shot_S4b(t, n):
    u = lt(t, "S4b")
    f = stage("teal", (255, 255, 255), 540, 1040, 450)
    rot_comp(f, form_el(430, "FOOD SAFETY COURSE"), 500, 1040, -4, pin(t, st0("S4b"), 0.3), 1.0, 0.35)
    tc = Tw("a2", "course", -0.1)
    if t >= tc: comp(f, check_el(70, True), 720, 1190, scale=pin(t, tc, 0.25))
    person(f, 880, 1560, 0.7, INSP, la=(18, 8), ra=(100, 150), brow="up", look=(-1, 0))
    hud_rule(f, 1, "LICENSE YOU FIRST", y=430, t=t, t0=st0("S4b") + 0.05)
    say(f, "+ PASS A COURSE", 640, 110, WHITE, t=t, t0=Tw("a2", "pass", -0.1))
    return finish(f, n)


# ---- S5: no waiting list for this one — hero strolls past an empty rope line ----
def shot_S5(t, n):
    u = lt(t, "S5")
    f = set_view("office", t, zoom=1.12, cy=1040)
    for i in range(3): rope(f, 200 + 240 * i, 200 + 240 * (i + 1), 1500, t)
    wk = walk(t, 1.0) if u < 2.2 else {}
    person(f, 180 + 320 * eo(clamp(u / 2.2)), 1660, 0.92, HERO, **wk, brow="up", look=(1, 0), expr="smirk")
    person(f, 880, 1660, 0.8, INSP, la=(70, 80), ra=(18, 8), brow="up", look=(-1, 0))
    tn = Tw("a3", "no", -0.15)
    say(f, "NO WAITING LIST", 650, 125, YEL_, t=t, t0=tn)
    say(f, "FOR THIS ONE", 780, 80, t=t, t0=Tw("a3", "this", -0.1))
    src(f, t, tn + 0.4, "NYC Health Dept., Mar 2026", 900)
    return finish(f, n)


# ---- S6: STEP 2 — the commissary: roll-up door rises, mentor waves him in ----
def shot_S6(t, n):
    u = lt(t, "S6")
    f = set_view("commissary", t, zoom=1.03 + 0.012 * u, cy=1000)
    d = eo(clamp(u / 0.9))
    person(f, 780, 1620, 0.86, MENTOR, la=(18, 8), ra=(150, 180 + 18 * math.sin(t * 9)), mouth=talk(t), brow="up", look=(-1, 0))
    wk = walk(t, 1.0) if d < 0.98 else {}
    person(f, 120 + 260 * d, 1620, 0.86, HCAP, **wk, brow="up", look=(1, 0))
    say(f, "FIND A BASE", 700, 150, t=t, t0=st0("S6") + 0.1)
    step_card(f, t, "S6", 2, "THE COMMISSARY", "NO BASE, NO TRUCK")
    return finish(f, n)


# ---- S7: stored → cleaned → serviced ----
def shot_S7(t, n):
    u = lt(t, "S7")
    f = set_view("commissary", t, zoom=1.22, cx=540, cy=1120, blur=2)
    comp(f, truck(640, open_=False, menu=None), 520, 1200)
    ts = Tw("b2", "stored", -0.15); tc = Tw("b2", "cleaned", -0.15); tv = Tw("b2", "serviced", -0.15)
    if ts <= t: comp(f, chip("STORED", (40, 110, 220), WHITE, 44), 250, 620, scale=pin(t, ts, 0.25))
    if tc <= t:
        comp(f, chip("CLEANED", (36, 160, 90), WHITE, 44), 540, 620, scale=pin(t, tc, 0.25))
        if t < tv + 0.3:
            for i in range(26):
                ph = (t * 1.8 + i * 0.077) % 1.0
                cv2.circle(f, (int(860 - 460 * ph), int(860 + 260 * ph + 90 * math.sin(i * 1.7) * ph)), 5 + i % 4, (0.72, 0.9, 1.0), -1, cv2.LINE_AA)
            person(f, 900, 1540, 0.62, HCAP, la=(120, 170), ra=(120, 170), brow="up", look=(-1, 0))
    if tv <= t:
        comp(f, chip("SERVICED", (240, 140, 20), WHITE, 44), 830, 620, scale=pin(t, tv, 0.25))
        person(f, 190, 1600, 0.72, MENTOR, la=(18, 8), ra=(110, 60), brow="up", look=(1, 0))
    say(f, "YOUR TRUCK'S HOME", 780, 92, t=t, t0=Tw("b2", "base", -0.1))
    return finish(f, n)


# ---- S8: the daily rule — dotted loop back to base, calendar flips ----
def shot_S8(t, n):
    u = lt(t, "S8")
    f = stage("emerald", (255, 255, 255), 540, 1100, 440)
    a = 2 * math.pi * clamp(u / 2.6); cx, cy, rx, ry = 540, 1180, 320, 170
    for i in range(30):
        q = i / 30 * 2 * math.pi
        if q <= a: cv2.circle(f, (int(cx + rx * math.cos(q + math.pi)), int(cy + ry * math.sin(q + math.pi))), 7, (1, 1, 1), -1, cv2.LINE_AA)
    comp(f, truck(220, menu=None), cx + rx * math.cos(a + math.pi), cy + ry * math.sin(a + math.pi) - 40)
    comp(f, chip("BASE", INK, WHITE, 36), cx - rx, cy + 110)
    comp(f, chip("STREET", INK, WHITE, 36), cx + rx, cy + 110)
    td = Tw("b3", "every", -0.2)
    if t >= td: comp(f, calendar_el("EVERY", "DAY"), 540, 900, scale=1.15 * pin(t, td, 0.3))
    hud_rule(f, 2, "BACK AT LEAST ONCE A DAY", y=430, t=t, t0=st0("S8") + 0.1)
    src(f, t, td + 0.4, "NYC Health Dept., 2026", 1450)
    return finish(f, n)


# ---- S9: STEP 3 — used-truck lot, hands behind the back ----
def shot_S9(t, n):
    u = lt(t, "S9")
    f = set_view("street", t, zoom=1.06, cy=1000)
    comp(f, truck(320, open_=False, menu=None, permit=False, col=(120, 200, 110)), 200, 1230)
    comp(f, truck(320, open_=False, menu=None, permit=False, col=(60, 170, 230)), 880, 1230)
    rot_comp(f, truck(360, open_=False, menu=None, permit=False, col=(190, 170, 150)), 540, 1240, 2, 1.0, 1.0, 0.25)
    wk = walk(t, 0.8) if u < 1.8 else {}
    person(f, 260 + 320 * eo(clamp(u / 1.8)), 1640, 0.84, HCAP, **wk, brow="sus", look=(1, -1))
    say(f, "PRICE IT.", 650, 150, t=t, t0=st0("S9") + 0.1)
    say(f, "DON'T BUY YET", 790, 100, YEL_, t=t, t0=Tw("c1", "don't", -0.1))
    step_card(f, t, "S9", 3, "THE TRUCK", "WALLET STAYS SHUT")
    return finish(f, n)


# ---- S10: the used price tag swings down ----
def shot_S10(t, n):
    f = stage("orange", YEL_, 540, 1060, 460)
    rot_comp(f, truck(620, open_=False, menu=None, permit=False, col=(190, 170, 150)), 500, 1130, 2, pin(t, st0("S10"), 0.3), 1.0, 0.3)
    tu = Tw("c2", "thousands", -0.3)
    if t >= tu:
        k = clamp((t - tu) / 0.35); sw = 12 * math.sin((t - tu) * 7) * math.exp(-(t - tu) * 2)
        rot_comp(f, tag_el("$30K–$100K USED", GRN_, WHITE, 66), 560, 660 + 120 * eback(k), -6 + sw, 1.0, k, 0.3)
    say(f, "A USED ONE", 470, 110, WHITE, t=t, t0=Tw("c2", "used", -0.1))
    src(f, t, tu + 0.4, "DoorDash guide: commonly cited ranges, Sep 2026", 1450)
    return finish(f, n)


# ---- S11: mentor stops him: step 4 decides ----
def shot_S11(t, n):
    u = lt(t, "S11")
    f = set_view("street", t, zoom=1.35, cx=540, cy=1080, blur=5)
    person_head_at(f, 760, 1160, 1.5, MENTOR, la=(18, 8), ra=(150, 110), mouth=talk(t), brow="up", look=(-1, 0))
    person(f, 260, 1660, 1.05, HCAP, la=(18, 8), ra=(70, 40), brow="worry", look=(1, -1), hold=cash_el(), hold_off=(10, -10))
    rot_comp(f, numcard_el("4", "PERMIT", RED_, 220), 540, 780, 8 * math.sin(t * 18) * clamp(u * 2), pin(t, st0("S11"), 0.3), 1.0, 0.3)
    hud_rule(f, 3, "DON'T BUY BEFORE THE CALL", y=430, t=t, t0=Tw("c3", "four", -0.1))
    return finish(f, n)


# ---- S12: STEP 4 — the giant $200 card on the counter ----
def shot_S12(t, n):
    u = lt(t, "S12")
    f = set_view("office", t, zoom=1.2, cx=540, cy=1080, blur=2)
    f[:] = f * np.array([0.92, 0.9, 1.0], np.float32)
    rot_comp(f, permit_el(680, price="$200"), 540, 1080, -3, pin(t, st0("S12") + 0.05, 0.3), 1.0, 0.35)
    person(f, 180, 1660, 0.82, HCAP, la=(18, 8), ra=(40, 70), brow="up", look=(1, -1), expr="wow")
    person(f, 900, 1660, 0.8, INSP, la=(18, 8), ra=(18, 8), brow="n", look=(-1, 0))
    say(f, "THE HARD ONE", 700, 120, YEL_, t=t, t0=st0("S12") + 0.1)
    step_card(f, t, "S12", 4, "THE TRUCK PERMIT", "ITS OWN PERMIT")
    return finish(f, n)


# ---- S13: the truck needs its own permit — sticker slaps on ----
def shot_S13(t, n):
    f = set_view("street", t, zoom=1.15, cx=540, cy=1080, blur=1.5)
    comp(f, truck(780, open_=False, menu=None, permit=False), 540, 1160)
    to = Tw("e2", "own", -0.15)
    if t >= to: rot_comp(f, permit_el(300, price=None), 700, 830, 6, pin(t, to, 0.25), 1.0, 0.3)
    say(f, "ONE TRUCK, ONE PERMIT", 620, 88, t=t, t0=st0("S13") + 0.1)
    return finish(f, n)


# ---- S13b: capped by law — the rope clicks shut ----
def shot_S13b(t, n):
    u = lt(t, "S13b")
    f = set_view("office", t, zoom=1.08, cy=1020)
    tc = Tw("e2", "capped", -0.1)
    for i in range(5): rot_comp(f, permit_el(300, price=None), 540 + 8 * i, 1200 - 22 * i, -3 + i, 1.0, 1.0, 0.25)
    rope(f, 210, 870, 1500, t, t_close=tc)
    person(f, 880, 1660, 0.8, INSP, la=(18, 8), ra=(18, 8), brow="n", look=(-1, 0))
    if t >= tc + 0.2: rot_comp(f, sign_el("CAPPED BY LAW", RED_, WHITE, 70, pole=False), 540, 800, -3, pin(t, tc + 0.2, 0.3), 1.0, 0.35)
    src(f, t, tc + 0.5, "NYC Health Dept., 2026", 1450)
    return finish(f, n)


# ---- S14: the 2022 lists — a queue of trucks to the horizon ----
def shot_S14(t, n):
    u = lt(t, "S14")
    f = set_view("street", t, zoom=1.0, cy=1000)
    truck_queue(f, t, y=1250, shift=-60 * u)
    td = Tw("e3", "twenty", -0.25)
    if t >= td: rot_comp(f, calendar_el("LISTS FROM", "2022"), 560, 900, 4, 1.0 * pin(t, td, 0.3), 1.0, 0.35)
    person(f, 170, 1660, 0.86, HCAP, la=(18, 8), ra=(60, 60), brow="worry", look=(1, -1), mouth="o" if u > 1.4 else 0)
    say(f, "STILL WORKING THROUGH", 560, 76, YEL_, t=t, t0=Tw("e3", "still", -0.1))
    return finish(f, n)


# ---- S15: dim side street — a hand slides a permit across (the holder's face never shown) ----
def shot_S15(t, n):
    u = lt(t, "S15")
    f = set_view("street", t, zoom=1.35, cx=540, cy=1080, blur=5)
    f[:] = f * np.array([0.42, 0.46, 0.62], np.float32)
    cv2.rectangle(f, (0, 1320), (1080, 1920), (0.2, 0.15, 0.13), -1, cv2.LINE_AA); cv2.line(f, (0, 1320), (1080, 1320), (0.08, 0.06, 0.06), 8, cv2.LINE_AA)
    person_head_at(f, 300, 1000 - 14 * u, 1.25 + 0.035 * u, HCAP, la=(18, 8), ra=(18, 8), brow="worry" if u < 2.6 else "sus", look=(1, 1) if u < 2.6 else (0, -1), sweat=u > 1.4)
    cv2.rectangle(f, (0, 1320), (1080, 1920), (0.2, 0.15, 0.13), -1, cv2.LINE_AA)
    k = eo(clamp(u / 3.2)); x = 950 - 370 * k
    fg_hand(f, x + 330, 1470, 1.05, ang=-90, who=HOLDER, blur=1.0)
    rot_comp(f, permit_el(340, price="$200"), x, 1430, -4, 1.0, 1.0, 0.3)
    say(f, "RENT ONE?", 520, 130, YEL_, t=t, t0=Tw("e4", "rent", -0.15))
    say(f, "OUTSIDE THE SYSTEM", 640, 76, t=t, t0=Tw("e4", "outside", -0.1))
    return finish(f, n)


# ---- S16: the tag grows: $200 → UP TO $25,000, hero jaw-drop close-up ----
def shot_S16(t, n):
    u = lt(t, "S16")
    f = stage("red", (255, 220, 200), 540, 1000, 470)
    tq = Tw("e5", "twenty-five", -0.25)
    k = clamp((t - tq) / 0.4)
    if t < tq: rot_comp(f, tag_el("$200", GRN_, WHITE, 90), 540, 760, -6, pin(t, st0("S16"), 0.3), 1.0, 0.35)
    else: rot_comp(f, tag_el("UP TO $25,000", (232, 36, 44), WHITE, 92), 540, 760, -4 + 3 * math.sin(t * 12) * (1 - k), 0.7 + 0.3 * eback(k), 1.0, 0.35)
    person_head_at(f, 540, 1200, 1.7, HCAP, la=(18, 8), ra=(18, 8), brow="up", look=(0, -1), mouth="o" if t >= tq else 0, expr="wow" if t >= tq else "n", sweat=t >= tq)
    src(f, t, tq + 0.3, "Vendors to Queens Daily Eagle, Apr 2025", 500)
    return finish(f, n)


# ---- S17: risky — sepia 2009, the file lands, six arrests (no characters) ----
def shot_S17(t, n):
    u = lt(t, "S17")
    f = set_view("office", t, zoom=1.3, cx=540, cy=1100, blur=5)
    for i in range(6): rot_comp(f, permit_el(280, price=None), 400 + 50 * i, 1270 - 10 * i, -8 + 3 * i, 1.0, 1.0, 0.25)
    yr = "2009" if u > 0.5 else str(2026 - int(17 * clamp(u / 0.5)))
    comp(f, calendar_el("BACK IN", yr), 760, 880, scale=1.05 * pin(t, st0("S17"), 0.3))
    tu = Tw("e6", "undercover", -0.2); ts = Tw("e6", "six", -0.2)
    if t >= tu: rot_comp(f, form_el(360, "UNDERCOVER PROBE"), 330, 900, -5, pin(t, tu, 0.3), 1.0, 0.35)
    if t >= ts: rot_comp(f, tag_el("6 ARRESTS", RED_, WHITE, 96), 540, 1240, -6, 1.5 - 0.5 * eo(clamp((t - ts) / 0.2)), clamp((t - ts) * 6), 0.35)
    sepia(f, t, st0("S17") + 0.2)
    say(f, "RISKY", 560, 140, YEL_, t=t, t0=Tw("e6", "risky", -0.1))
    src(f, t, tu + 0.3, "NYC Dept. of Investigation, Jun 2009 · accusations", 1450)
    return finish(f, n)


# ---- S18: since July — sepia drains, the printer spits applications ----
def shot_S18(t, n):
    u = lt(t, "S18")
    f = set_view("street", t, zoom=1.05, cy=1000)
    x0, y0 = 540, 1190
    cv2.rectangle(f, (x0 - 230, y0 - 40), (x0 + 230, y0 + 190), (0.82, 0.84, 0.88), -1, cv2.LINE_AA); cv2.rectangle(f, (x0 - 230, y0 - 40), (x0 + 230, y0 + 190), (0.05, 0.05, 0.07), 7, cv2.LINE_AA)
    cv2.rectangle(f, (x0 - 170, y0 - 56), (x0 + 170, y0 - 30), (0.1, 0.1, 0.14), -1, cv2.LINE_AA)
    comp(f, chip("CITY OFFICE", (40, 110, 220), WHITE, 38), x0, y0 + 90)
    tp = Tw("e7", "offers", -0.2)
    if t >= tp:
        rng = np.random.default_rng(7); xs = rng.uniform(190, 890, 12); rots = rng.uniform(-30, 30, 12)
        for i in range(12):
            ph = ((t - tp) * 0.9 + i / 12) % 1.0
            rot_comp(f, form_el(170, "APPLY"), x0 + (xs[i] - x0) * ph, y0 - 40 - 330 * ph, rots[i] * ph, 1.0, clamp(4 * (1 - ph)) * clamp(ph * 10), 0.2)
    person(f, 170, 1660, 0.82, HCAP, la=(18, 8), ra=(120, 160), brow="up", look=(1, -1), expr="wow")
    tn = Tw("e7", "hundred", -0.3)
    if t < tn: say(f, "SINCE JULY...", 620, 130, t=t, t0=st0("S18") + 0.1)
    else: say(f, "+2,200 A YEAR", 620, 130, YEL_, t=t, t0=tn)
    if t >= tn + 0.5: say(f, "SUPERVISORY LICENSE · 5 YEARS", 740, 62, t=t, t0=tn + 0.5)
    k = 1 - clamp(u / 0.5)
    if k > 0: f[:] = sepia_tone(f, 0.85 * k)
    src(f, t, tn + 0.3, "NYC Health Dept., Mar 2026", 1450)
    return finish(f, n)


# ---- S19: the twist — every application flies to the 2022 trucks; the hero has no ticket ----
def shot_S19(t, n):
    u = lt(t, "S19")
    f = set_view("street", t, zoom=1.0, cy=1000)
    truck_queue(f, t, y=1200, n=4, x0=330, dx=250)
    for i in range(7):
        q = clamp((u - 0.1 - i * 0.14) / 0.6)
        if 0 < q < 1: rot_comp(f, form_el(130, "APPLY"), 120 + (300 + i * 100) * q, 700 + 280 * q - 200 * math.sin(q * 3.1), 20 * q, 1.0, 1.0, 0.2)
    comp(f, chip("2022 LISTS", (20, 20, 26), WHITE, 40), 660, 1000, scale=pin(t, Tw("t1", "lists", -0.2), 0.25))
    person(f, 150, 1660, 0.86, HCAP, la=(40, 40), ra=(40, 40), brow="worry", look=(1, -1))
    to = Tw("t1", "only", -0.1)
    if t < to: say(f, "THE TWIST", 640, 150, t=t, t0=st0("S19") + 0.05)
    else: say(f, "ONLY THOSE LISTS", 640, 120, YEL_, t=t, t0=to)
    return finish(f, n)


# ---- S19b: not on one? work a truck first ----
def shot_S19b(t, n):
    u = lt(t, "S19b")
    f = set_view("street", t, zoom=1.1, cy=1030)
    comp(f, truck(760, menu=None), 560, 1180)
    steam(f, 300, 800, t)
    tw = Tw("t1", "working", -0.2); k = eo(clamp((t - tw) / 0.8))
    person(f, 400, 1270, 0.5, MENTOR, la=(18, 8), ra=(150, 170), brow="up", look=(1, 0), shadow=False)
    person(f, 140 + (360 * k), 1660 - 60 * k, 0.86, HCAP, **(walk(t, 1.0) if 0 < k < 1 else {}), brow="up", look=(1, -1), expr="wow" if k >= 1 else "n")
    hud_rule(f, 4, "NO SPOT? WORK ONE FIRST", y=430, t=t, t0=tw - 0.05)
    say(f, "NOT ON A LIST?", 620, 110, t=t, t0=Tw("t1", "Not", -0.05))
    src(f, t, tw + 0.3, "NYC Health Dept.: vendor license lets you work a truck", 1450)
    return finish(f, n)


# ---- S20: or stay on private property — a parking lot with its own sign ----
def shot_S20(t, n):
    u = lt(t, "S20")
    f = set_view("street", t, zoom=1.06, cy=1000)
    cv2.rectangle(f, (0, 1250), (1080, 1920), (0.34, 0.35, 0.39), -1, cv2.LINE_AA)
    for i in range(5):
        x = 120 + 210 * i; cv2.line(f, (x, 1280), (x - 60 + 15 * i, 1560), (0.98, 0.98, 0.92), 9, cv2.LINE_AA)
    comp(f, truck(620, menu="TACOS"), 560, 1220)
    steam(f, 340, 930, t, s=0.8)
    rot_comp(f, sign_el("PRIVATE LOT", (40, 110, 220), WHITE, 52, pole=False), 720, 860, 0, pin(t, Tw("t2", "private", -0.2), 0.3), 1.0, 0.3)
    person(f, 180, 1660, 0.86, HCAP, la=(150, 40), ra=(18, 8), brow="up", look=(1, 0), expr="smirk")
    tn = Tw("t2", "no", -0.25)
    if t >= tn: rot_comp(f, tag_el("NO WAITING LIST", GRN_, WHITE, 66), 600, 1440, -3, 1.4 - 0.4 * eo(clamp((t - tn) / 0.2)), clamp((t - tn) * 6), 0.35)
    say(f, "PRIVATE PROPERTY", 640, 104, YEL_, t=t, t0=Tw("t2", "private", -0.15))
    src(f, t, tn + 0.3, "NYC Health Dept.: Restricted Area permit", 760)
    return finish(f, n)


# ---- S21: save this — loop back to frame-1 street, truck now open ----
def shot_S21(t, n):
    u = lt(t, "S21")
    f = set_view("street", t, zoom=1.04, cy=980)
    comp(f, truck(800, menu=None), 560, 1180); steam(f, 280, 860, t)
    person(f, 185, 1610, 0.82, HCAP, la=(20, 8), ra=(160, 150), brow="up", look=(1, -1), mouth=2 if u < 0.6 else 0)
    person(f, 890, 1610, 0.8, MENTOR, la=(150, 160), ra=(18, 8), brow="up", look=(-1, 0))
    say(f, "SAVE THIS", 640, 170, YEL_, t=t, t0=Tw("z1", "Save", -0.1))
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


# ---- S22: your move — stay or move? then send ----
def shot_S22(t, n):
    u = lt(t, "S22")
    f = stage("purple", GOLD, 540, 1000, 460)
    comp(f, truck(600, menu="TACOS"), 540, 1060); steam(f, 300, 800, t, s=0.8)
    person(f, 170, 1500, 0.6, HCAP, la=(18, 8), ra=(80, 20), brow="up", look=(1, 0))
    person(f, 910, 1500, 0.6, MENTOR, la=(150, 170 + 18 * math.sin(t * 12)) if t >= L0("z2") else (18, 8), ra=(18, 8), brow="up", look=(-1, 0))
    for i, who in enumerate(("friend", "lady", "creator")):
        ti = st0("S22") + 1.2 + 0.9 * i; kq = eo(clamp((t - ti) / 0.7))
        if kq > 0: person(f, 960 - 60 * i * 1.0 - (0 if kq >= 1 else 0) - 240 * kq, 1320 + 12 * i, 0.32, who, **(walk(t, 1.0) if kq < 1 else {}), brow="up", look=(-1, 0), op=clamp(kq * 3), shadow=False)
    choice_card(f, "STILL NYC?", "STAY", "MOVE", y=600, t=t, t0=st0("S22") + 0.05, col_a=(36, 186, 88), col_b=(40, 110, 220))
    tf = Tw("z2", "friend", -0.15)
    if t >= tf: say(f, "SEND TO THAT FRIEND", 1460, 80, t=t, t0=tf)
    series_badge(f, "HOW TO START", SERIES_T)
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(Tw("i1", "thousands", -0.25), 0.25, 10), (Tw("e2", "capped", -0.1), 0.3, 14), (Tw("e5", "twenty-five", -0.25), 0.35, 16),
           (Tw("e6", "six", -0.2), 0.3, 12), (Tw("c2", "thousands", -0.3), 0.2, 8), (Tw("t2", "no", -0.25), 0.2, 8)]
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
