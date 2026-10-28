# ================= shots: "One company behind your glasses, the shop and your eye insurance" (type C hidden giant — four doors) =================
# Generic props only: no real logos, frame designs or store trade dress; company/brand names appear only as plain caption/sign text.
LUX = {"base": "exec", "top": (40, 40, 52), "tie": (200, 160, 60)}                    # the big eyewear group's boss (dark suit, gold tie)
OAK = {"base": "creator", "top": (230, 120, 30), "hair": "curly"}                     # the rival sunglass maker (orange jacket)
SHOPPER = "hero"
FRIEND = {"base": "friend", "top": (60, 150, 220)}
OPTO = {"base": "inventor", "top": (244, 246, 250), "trim": (40, 140, 160)}           # optometrist in a white coat
GREEN_D = (36, 150, 90); BLUE_D = (40, 110, 220); PURP_D = (130, 70, 200); ORG_D = (240, 120, 30)
DOORS = [(1, "FRAME", BLUE_D), (2, "LENS", GREEN_D), (3, "SHOP", ORG_D), (4, "INSURANCE", PURP_D)]

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "It's") - 0.12, "whip"), ("S1b", T("i2", "most") - 0.2, "punch"),
    ("S2", T("i3", "It") - 0.12, "zoom"),
    ("S3", T("a1", "Door") - 0.2, "zoom"), ("S4", T("a2", "Ray-Ban.") - 0.2, "whip"), ("S4b", T("a2", "All") - 0.15, "punch"),
    ("S5", T("a3", "And") - 0.12, "focus"), ("S6", T("a4", "It") - 0.12, "whip"), ("S7", T("a5", "So") - 0.12, "whip"),
    ("S8", T("b1", "Door") - 0.2, "zoom"), ("S9", T("b2", "In") - 0.12, "whip"), ("S10", T("b3", "So") - 0.12, "focus"),
    ("S11", T("c1", "Door") - 0.2, "zoom"), ("S12", T("c2", "Sunglass") - 0.15, "whip"), ("S13", T("c3", "By") - 0.12, "punch"),
    ("S14", T("c4", "And") - 0.12, "flash"),
    ("S15", T("s1", "Back") - 0.15, "whip"), ("S16", T("s2", "That") - 0.12, "whip"), ("S17", T("s3", "So") - 0.12, "focus"),
    ("S18", T("s4", "In") - 0.12, "punch"), ("S19", T("s5", "Six") - 0.12, "whip"),
    ("S20", T("d1", "Door") - 0.2, "zoom"), ("S21", T("d2", "In") - 0.12, "whip"), ("S22", T("d3", "And") - 0.12, "punch"),
    ("S23", T("d4", "And") - 0.12, "whip"), ("S23b", T("d4", "bought") - 0.2, "punch"),
    ("S24", T("t1", "So") - 0.12, "flash"),
    ("S25", T("e0", "Here's") - 0.12, "whip"), ("S26", T("e1", "Take") - 0.12, "focus"), ("S27", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}


def lt(t, sid): return t - SHOT[sid]["start"]


def st0(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", x=W / 2, maxw=800):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, maxw=maxw)
    ed_show(f, el, x, y, t, t0, 0.34, out)


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INK, WHITE, 24), 540, y, op=clamp((t - t0) / 0.3))


def stamp_at(f, text, x, y, t, t0, col=RED_, size=60, rot=-8):
    if t < t0: return
    k = clamp((t - t0) / 0.18); rot_comp(f, stamp_el(text, col, size), x, y, rot, 1.5 - 0.5 * eo(k), clamp(k * 3), 0.0)


def door_label(f, t, t0, n_, text, col):
    if t < t0: return
    comp(f, chip(f"DOOR #{n_}", col, WHITE, 46), 540, 380, scale=pin(t, t0, 0.25))
    say(f, text, 520, 150, t=t, t0=t0 + 0.1)


def tree_scene(f, t, card=True, shop=True, k=1.0, title=True):
    """frame-1 composition: a tree whose branches grow glasses, plus a hanging shop sign and a vision-plan card"""
    if title: title3d(f, "EYEWEAR", 740, t, -1, size=200, face=(255, 214, 60), side=(150, 90, 10))
    cv2.ellipse(f, (540, 1660), (400, 50), 0, 0, 360, C((40, 90, 50)), -1, cv2.LINE_AA)
    glasses_tree(f, 540, 1650, t, k=k, n=11, scale=1.3)
    if shop:
        sw = math.sin(t * 1.7) * 5
        rot_comp(f, chip("THE SHOP", ORG_D, WHITE, 40), 230, 1330, sw, 1.0, 1.0, 0.2)
    if card:
        sw = math.sin(t * 1.9 + 1) * 6
        cv2.line(f, (850, 1250), (850 + int(sw), 1300), C((60, 60, 60)), 2, cv2.LINE_AA)
        rot_comp(f, plan_card_el(250, "VISION PLAN"), 850 + sw, 1370, sw, 1.0, 1.0, 0.25)


def shot_S0(t, n):
    f = stage("teal", (120, 255, 220), 540, 1000, 440)
    tree_scene(f, t, card=t >= T("i1", "insurance") - 0.25, shop=t >= T("i1", "shop,") - 0.2)
    ui_word(f, "your sunglasses, the shop, your insurance:", "ONE COMPANY?", 470, t, -0.5, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S1(t, n):
    f = set_view("office", t, 1.15, 540, 1050, blur=2.0)
    person(f, 300, 1800, 0.82, SHOPPER, la=(18, 8), ra=(120, 160), mouth=0, look=(1, -1), expr="n", brow="up")
    person(f, 780, 1800, 0.82, LUX, la=(150, 200), ra=(18, 8), mouth=0, look=(-1, 0), expr="smirk")
    k = pin(t, st0("S1") + 0.15, 0.3)
    comp(f, chip("ESSILORLUXOTTICA", INK, WHITE, 56), 540, 760, scale=k)
    say(f, "ONE EYEWEAR GIANT", 600, 110, col=(255, 214, 60), t=t, t0=st0("S1") + 0.05)
    return finish(f, n)


def shot_S1b(t, n):
    f = set_view("street", t, 1.0, 540, 1000, blur=2.0)
    for i, (x, who) in enumerate(((240, FRIEND), (540, SHOPPER), (840, {"base": "lady", "top": (220, 80, 120)}))):
        person(f, x, 1780, 0.72, who, la=(18, 8), ra=(150, 200), mouth=0, look=(0, -1), expr="n", brow="up")
    for i, x in enumerate((240, 540, 840)):
        if t > st0("S1b") + 0.2 + 0.15 * i: comp(f, ed_el("?", "", lead_col=(255, 214, 60), lead_size=110), x, 1000)
    say(f, "NEVER HEARD OF IT", 620, 110, t=t, t0=T("i2", "never") - 0.1)
    return finish(f, n)


def shot_S2(t, n):
    f = stage("purple", (120, 140, 255), 540, 1050, 420)
    t4 = T("i3", "four") - 0.15
    if t >= t4:
        for i in range(4):
            tt = t4 + 0.12 * i
            if t >= tt:
                num, lab, col = DOORS[i]
                comp(f, door_el(200, 400, num, lab, col, 0.0, 0.0), 540 + (i - 1.5) * 225, 1120, scale=pin(t, tt, 0.25))
    ts = T("i3", "fourth") - 0.15
    if t >= ts:
        _sglow(f, 540 + 1.5 * 225, 1120, 200, (255, 220, 120), 0.6 + 0.2 * math.sin(t * 8))
        stamp_at(f, "SNEAKIEST", 700, 1440, t, T("i3", "sneakiest") - 0.15, RED_, 58, -6)
    ui_word(f, "it owns", "4 DOORS", 470, t, t4, col=YEL_, size=190, shadow=0.45, lead_col=WHITE, tail="to your eyes")
    return finish(f, n)


def door_open_shot(f, t, t0, num, col):
    _, lab, _ = DOORS[num - 1]
    k = clamp((t - t0 - 0.2) / 0.6)
    z = 1.0 + 0.5 * eio(clamp((t - t0 - 0.5) / 0.9))
    comp(f, door_el(320, 640, num, lab, col, eo(k), k), 540, 1150, scale=z)
    if k > 0.3: light_rays(f, 540, 1150, (255, 236, 190), 0.25 * k)


def shot_S3(t, n):
    f = stage("sky", (255, 240, 180), 540, 1100, 460)
    door_open_shot(f, t, st0("S3"), 1, BLUE_D)
    if t > st0("S3") + 0.8:
        k = clamp((t - st0("S3") - 0.8) / 0.5)
        rot_comp(f, glasses_el(420, "round", (22, 22, 28), (40, 60, 90)), 540, 1150 - 120 * eo(k), 0, 0.4 + 0.6 * eo(k), k, 0.3)
    door_label(f, t, T("a1", "Door") - 0.1, 1, "THE FRAME", BLUE_D)
    return finish(f, n)


def shot_S4(t, n):
    f = stage("sky", (255, 240, 180), 540, 1050, 460)
    brands = [("RAY-BAN", 0), ("OAKLEY", 3), ("PERSOL", 1), ("OLIVER PEOPLES", 4)]
    for i, (nm, si) in enumerate(brands):
        tb = T("a2", ["Ray-Ban.", "Oakley.", "Persol.", "Oliver"][i]) - 0.15
        if i == 0: tb = min(tb, st0("S4") + 0.05)
        if t < tb: continue
        x, y = (300, 780, 300, 780)[i], (900, 900, 1300, 1300)[i]
        k = pin(t, tb, 0.25)
        comp(f, glasses_el(360, **gl_style(si)), x, y, scale=k)
        comp(f, chip(nm, WHITE, INK, 36), x, y + 120, scale=k)
    return finish(f, n)


def shot_S4b(t, n):
    f = stage("orange", (255, 230, 150), 540, 1050, 460)
    ta = st0("S4b")
    for i in range(4):
        x, y = (300, 780, 300, 780)[i], (900, 900, 1300, 1300)[i]
        k = clamp((t - ta - 0.2) / 0.6)
        xx, yy = x + (540 - x) * 0.25 * eo(k), y + (1100 - y) * 0.25 * eo(k)
        cv2.line(f, (int(xx), int(yy + 40)), (540, 1470), C(INK), 4, cv2.LINE_AA)
        comp(f, glasses_el(330, **gl_style((0, 3, 1, 4)[i])), xx, yy)
    cv2.circle(f, (540, 1470), 46, C(YEL_), -1, cv2.LINE_AA); cv2.circle(f, (540, 1470), 46, C(INK), 5, cv2.LINE_AA)
    comp(f, ed_el("1", "", lead_col=INK, lead_size=56), 540, 1470)
    ui_word(f, "all owned by", "ONE COMPANY", 470, t, ta + 0.05, col=WHITE, size=160, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S5(t, n):
    f = stage("pink", (255, 214, 230), 540, 1080, 440)
    names = ["CHANEL", "PRADA", "ARMANI", "VERSACE", "MICHAEL KORS"]
    keys = ["Chanel,", "Prada,", "Armani,", "Versace,", "Michael"]
    rot_comp(f, glasses_el(520, "cat", (22, 22, 28), (90, 40, 60)), 540, 1100, 0, pin(t, st0("S5") + 0.05, 0.3), 1.0, 0.3)
    sparkle(f, 760, 1030, 30, t)
    for i, (nm, kw) in enumerate(zip(names, keys)):
        tt = T("a3", kw) - 0.12
        if t < tt: continue
        a = math.radians(-90 + 72 * i + 36)
        x, y = 540 + 330 * math.cos(a), 1150 + 300 * math.sin(a)
        comp(f, chip(nm, INK, WHITE, 38), x, y, scale=pin(t, tt, 0.22))
    say(f, "THE DESIGNER ONES?", 520, 120, t=t, t0=st0("S5") + 0.05)
    return finish(f, n)


def shot_S6(t, n):
    f = set_view("office", t, 1.25, 540, 1050, blur=2.5)
    person(f, 300, 1900, 1.15, {"base": "lady", "top": (20, 20, 24)}, la=(60, 40), ra=(18, 8), mouth=0, look=(1, 0), expr="smirk")
    person(f, 780, 1900, 1.15, LUX, la=(18, 8), ra=(60, 40), mouth=0, look=(-1, 0), expr="smirk")
    comp(f, form_el(300, "LICENCE", "SIGNED" if t > T("a4", "licence") else None), 540, 1010, scale=pin(t, st0("S6") + 0.1, 0.3))
    say(f, "MADE UNDER LICENCE", 1480, 110, col=(255, 214, 60), t=t, t0=T("a4", "licence") - 0.25)
    say(f, "THEY MAKE THOSE TOO", 540, 96, t=t, t0=st0("S6") + 0.05)
    return finish(f, n)


def shot_S7(t, n):
    f = set_view("optician", t, 1.0, 540, 960)
    optician_dressing(f, t)
    to = T("a5", "one") - 0.2
    if t >= to:
        k = clamp((t - to) / 0.5)
        for j in range(5):
            for q in range(2):
                x, y = 160 + q * 160, 350 + j * 125
                cv2.line(f, (x, y), (int(x + (760 - x) * k), int(y + (1000 - y) * k)), C(RED_), 4, cv2.LINE_AA)
        if k > 0.9:
            cv2.circle(f, (760, 1000), 56, C(YEL_), -1, cv2.LINE_AA); cv2.circle(f, (760, 1000), 56, C(INK), 5, cv2.LINE_AA)
            comp(f, ed_el("1", "", lead_col=INK, lead_size=60), 760, 1000)
    person(f, 640, 1880, 0.95, SHOPPER, la=(18, 8), ra=(150, 120), mouth=0, look=(-1, -1), expr="wow" if t >= to else "n", brow="up")
    if t < to: say(f, "RIVAL BRANDS?", 1180, 130, t=t, t0=st0("S7") + 0.05)
    else: say(f, "ONE PLACE", 1180, 150, col=(255, 214, 60), t=t, t0=to)
    return finish(f, n)


def shot_S8(t, n):
    f = stage("emerald", (180, 255, 210), 540, 1100, 460)
    door_open_shot(f, t, st0("S8"), 2, GREEN_D)
    if t > st0("S8") + 0.8:
        k = clamp((t - st0("S8") - 0.8) / 0.5)
        comp(f, lens_el(380), 540, 1150 - 100 * eo(k), scale=0.4 + 0.6 * eo(k), op=k)
    door_label(f, t, T("b1", "Door") - 0.1, 2, "THE LENS", GREEN_D)
    return finish(f, n)


def shot_S9(t, n):
    f = stage("sky", (255, 240, 180), 540, 1100, 460)
    flapboard(f, 540, 760, "2018", t, st0("S9") + 0.05)
    tj = T("b2", "joined") - 0.15
    k = clamp((t - tj) / 0.7) if t >= tj else 0.0
    xl, xr = 300 + 150 * eo(k), 780 - 150 * eo(k)
    comp(f, glasses_el(420, "rect", (22, 22, 28), (200, 220, 240), clear=True), xl, 1120)
    comp(f, lens_el(280), xr, 1120)
    comp(f, chip("LUXOTTICA: FRAMES", BLUE_D, WHITE, 30), 300, 1330)
    comp(f, chip("ESSILOR: LENSES", GREEN_D, WHITE, 30), 780, 1330)
    tg = T("b2", "Transitions") - 0.15
    if t >= tg:
        comp(f, chip("VARILUX", WHITE, INK, 32), 380, 1440, scale=pin(t, tg, 0.22))
        tt2 = tg + 0.15
        if t >= tt2: comp(f, chip("TRANSITIONS", WHITE, INK, 32), 720, 1440, scale=pin(t, tt2, 0.22))
    if k >= 1: _sglow(f, 540, 1120, 200, (255, 255, 220), 0.4 * clamp(1 - (t - tj - 0.7) / 0.4))
    return finish(f, n)


def shot_S10(t, n):
    f = stage("teal", (120, 255, 220), 540, 1100, 460)
    s0 = st0("S10")
    k = clamp((t - s0 - 0.2) / 0.8)
    comp(f, glasses_el(600, "oval", (22, 22, 28), (190, 215, 245), clear=True), 540, 1180)
    for dx in (-162, 162):
        comp(f, lens_el(200), 540 + dx, 760 + (1180 - 760) * eo(k), op=1.0 - 0.6 * clamp((k - 0.9) * 10))
    stamp_at(f, "SAME COMPANY", 540, 1430, t, T("b3", "same") - 0.15, RED_, 60, -6)
    ui_word(f, "frame + lens", "ONE MAKER", 470, t, s0 + 0.05, col=YEL_, size=160, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S11(t, n):
    f = stage("orange", (255, 230, 150), 540, 1100, 460)
    door_open_shot(f, t, st0("S11"), 3, ORG_D)
    if t > st0("S11") + 0.8:
        k = clamp((t - st0("S11") - 0.8) / 0.5)
        comp(f, shopfront_el("SHOP", ORG_D, 260, 360), 540, 1150 - 60 * eo(k), scale=0.4 + 0.6 * eo(k), op=k)
    door_label(f, t, T("c1", "Door") - 0.1, 3, "THE SHOP", ORG_D)
    return finish(f, n)


def shot_S12(t, n):
    f = set_view("mall", t, 1.0, 540, 960)
    u = lt(t, "S12")
    mall_dressing(f, t, y=900, cam_x=-30 * clamp(u / 3))
    person(f, 300 + 120 * clamp(u / 3), 1820, 0.78, SHOPPER, la=(18, 8), ra=(60, 30), mouth=0, look=(1, -1), expr="n")
    to = T("c2", "same") - 0.15
    if t >= to: say(f, "SAME OWNER", 1380, 150, col=(255, 214, 60), t=t, t0=to)
    return finish(f, n)


def shot_S13(t, n):
    f = stage("orange", (255, 230, 150), 540, 1050, 460)
    s0 = st0("S13"); tt = T("c3", "twenty") - 0.15
    k = clamp((t - tt) / 1.2) if t >= tt else 0.0
    val = int(19709 * eo(k))
    odometer(f, 540, 1080, f"{val:06,}".replace(",", ","), 1.0)
    comp(f, chip("STORES", INK, WHITE, 50), 540, 1290)
    ui_word(f, "by this September:", "ALMOST 20,000", 470, t, s0 + 0.05, col=WHITE, size=150, shadow=0.45, lead_col=WHITE)
    src(f, "Source: EssilorLuxottica Q3 2026 (19,709 stores)", t, tt + 0.4, 1440)
    return finish(f, n)


def shot_S14(t, n):
    f = set_view("dusk", t, 1.1, 540, 1000, blur=1.0)
    _sglow(f, 540, 1150, 380, (255, 240, 200), 0.45)
    rot_comp(f, glasses_el(560, "sport", (230, 120, 30), (60, 40, 90)), 540, 1150, -4 + 3 * math.sin(t * 2), pin(t, st0("S14") + 0.1, 0.3), 1.0, 0.3)
    say(f, "OWNING THE SHOPS = POWER", 620, 96, t=t, t0=st0("S14") + 0.05)
    to = T("c4", "Oakley.") - 0.2
    if t >= to: say(f, "JUST ASK OAKLEY", 1390, 130, col=(255, 214, 60), t=t, t0=to)
    return finish(f, n)


def shot_S15(t, n):
    f = set_view("street", t, 1.15, 540, 1050, blur=2.0)
    flapboard(f, 540, 700, "2001", t, st0("S15") + 0.05)
    tr = T("s1", "rival") - 0.15
    person(f, 290, 1800, 0.85, OAK, la=(18, 8), ra=(120, 150), mouth=0, look=(1, 0), expr="smirk",
           hold=scale_el(glasses_el(200, "sport", (230, 120, 30), (60, 40, 90)), 0.9), hold_off=(30, -50))
    person(f, 790, 1800, 0.85, LUX, la=(18, 8), ra=(18, 8), mouth=0, look=(-1, 0), expr="n", brow="sad" if t >= tr else "n")
    if t >= tr:
        comp(f, chip("OAKLEY", ORG_D, WHITE, 40), 290, 1060, scale=pin(t, tr, 0.25))
        comp(f, chip("LUXOTTICA", INK, WHITE, 40), 790, 1060, scale=pin(t, tr + 0.1, 0.25))
        say(f, "RIVALS", 920, 120, col=(255, 90, 80), t=t, t0=tr)
    return finish(f, n)


def shot_S16(t, n):
    f = set_view("mall", t, 1.2, 540, 1000)
    shopfront(f, "SUNGLASS HUT", 540, 940, (232, 60, 40), 440, 640, t, seed=2)
    tb = T("s2", "bought") - 0.15
    stamp_at(f, "BOUGHT BY LUXOTTICA", 540, 1000, t, tb, RED_, 50, -8)
    person(f, 800, 1860, 0.8, LUX, la=(150, 200), ra=(18, 8), mouth=0, look=(-1, -1), expr="smirk")
    tg = T("s2", "biggest") - 0.15
    if t >= tg: comp(f, chip("19% OF OAKLEY'S SALES", ORG_D, WHITE, 40), 540, 1360, scale=pin(t, tg, 0.25))
    src(f, "Source: Forbes, 3 Aug 2001", t, tg + 0.3, 1450)
    return finish(f, n)


def shot_S17(t, n):
    f = stage("sky", (255, 240, 180), 540, 1100, 440)
    tf = T("s3", "fewer") - 0.2
    k = clamp((t - tf) / 0.6) if t >= tf else 0.0
    bars(f, 330, 1480, 220, 640, ORG_D, 1.0, "EXPECTED", "")
    bars(f, 750, 1480, 220, 640 * (1 - 5 / 6 * eo(k)), RED_, 1.0, "ORDERED", "~1/6" if k > 0.8 else "")
    ui_word(f, "guess what happened next?", "FAR FEWER", 470, t, st0("S17") + 0.05, col=YEL_, size=160, shadow=0.45, lead_col=WHITE)
    src(f, "Source: FundingUniverse (Oakley company history)", t, tf + 0.6, 660)
    return finish(f, n)


def shot_S18(t, n):
    f = stage("red", (255, 200, 160), 540, 1100, 440)
    s0 = st0("S18"); tf = T("s4", "fell") - 0.15
    k = clamp((t - s0 - 0.1) / max(0.4, tf + 0.5 - s0 - 0.1))
    stock_crash(f, 160, 820, 920, 1360, k, t)
    if t >= tf: ui_word(f, "Oakley stock, in one day", "-35%", 470, t, tf, col=WHITE, size=200, shadow=0.45, lead_col=WHITE)
    else: ui_word(f, "in a", "SINGLE DAY", 470, t, s0 + 0.05, col=WHITE, size=160, shadow=0.45, lead_col=WHITE)
    src(f, "Source: Forbes, 3 Aug 2001", t, tf + 0.3, 1440)
    return finish(f, n)


def shot_S19(t, n):
    f = stage("emerald", (255, 230, 150), 540, 1100, 440)
    flapboard(f, 540, 720, "2007", t, st0("S19") + 0.05)
    tb = T("s5", "billion") - 0.25
    tbo = T("s5", "bought") - 0.15
    comp(f, cheque_el("LUXOTTICA", "OAKLEY", "$2.1B" if t >= tb else "$ ???", "two point one billion", "buying a rival", w=860, h=400, year="2007"),
         540, 1130, scale=pin(t, min(tbo, st0("S19") + 0.3), 0.3))
    if t >= tb:
        light_rays(f, 540, 1130, (255, 236, 180), 0.25)
        say(f, "$2.1 BILLION", 1420, 120, col=(255, 214, 60), t=t, t0=tb)
    src(f, "Source: Orange County Business Journal, Jun 2007", t, tb + 0.4, 845)
    return finish(f, n)


def shot_S20(t, n):
    f = stage("purple", (200, 140, 255), 540, 1100, 460)
    door_open_shot(f, t, st0("S20"), 4, PURP_D)
    if t > st0("S20") + 0.9:
        k = clamp((t - st0("S20") - 0.9) / 0.5)
        comp(f, plan_card_el(460), 540, 1180 - 60 * eo(k), scale=0.4 + 0.6 * eo(k), op=k)
    door_label(f, t, T("d1", "Door") - 0.1, 4, "YOUR EYE INSURANCE", PURP_D)
    return finish(f, n)


def shot_S21(t, n):
    f = set_view("optician", t, 1.2, 540, 1000, blur=2.5)
    optician_dressing(f, t)
    person(f, 540, 1900, 1.25, FRIEND, la=(18, 8), ra=(120, 160), mouth=0, look=(0, -1), expr="n", hold=scale_el(plan_card_el(300), 1.0), hold_off=(40, -80))
    tm = T("d2", "millions") - 0.25
    say(f, "EYEMED", 560, 150, col=(255, 214, 60), t=t, t0=T("d2", "EyeMed") - 0.15)
    if t >= tm: say(f, "TENS OF MILLIONS OF PEOPLE", 720, 90, t=t, t0=tm)
    src(f, "EyeMed (2022): 68M+ members", t, tm + 0.3, 1440)
    return finish(f, n)


def shot_S22(t, n):
    f = stage("teal", (120, 255, 220), 540, 1000, 440)
    tree_scene(f, t, card=True, shop=True, title=False)
    tp = T("d3", "parent") - 0.15
    if t >= tp: ui_word(f, "its parent company?", "THE SAME ONE", 470, t, tp, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    stamp_at(f, "SAME OWNER", 760, 1430, t, T("d3", "same") - 0.1, RED_, 48, 8)
    return finish(f, n)


def shot_S23(t, n):
    f = set_view("street", t, 1.25, 540, 1000, blur=3.0)
    led = 0.5 + 0.5 * math.sin(t * 9) if t > T("d4", "smart") - 0.1 else 0.0
    person_head_at(f, 540, 1040, 2.4, SHOPPER, mouth=0, expr="smirk", look=(0, 0))
    comp(f, glasses_el(520, "rect", (22, 22, 28), (40, 60, 90), smart=True, led=led), 540, 1000)
    say(f, "SMART GLASSES", 1390, 120, t=t, t0=T("d4", "smart") - 0.15)
    tm = T("d4", "Meta") - 0.15
    if t >= tm: comp(f, chip("META × RAY-BAN", INK, WHITE, 40), 540, 600, scale=pin(t, tm, 0.25))
    return finish(f, n)


def shot_S23b(t, n):
    f = stage("sky", (255, 240, 180), 540, 1060, 440)
    th = T("d4", "three") - 0.15
    kk = clamp((t - th) / 0.6) if t >= th else 0.0
    pie_coin(f, 540, 1080, 300, max(0.003, 0.03 * kk), (60, 110, 230), "3%" if kk > 0.5 else "?", 1.0, "")
    ui_word(f, "Meta bought about", "3%", 470, t, st0("S23b") + 0.05, col=WHITE, size=190, shadow=0.45, lead_col=WHITE, tail="of the company")
    src(f, "Source: Reuters, Jul 2025 (~3% stake)", t, th + 0.3, 1430)
    return finish(f, n)


def shot_S24(t, n):
    f = stage("purple", (200, 160, 255), 540, 1050, 460)
    words = ["frame,", "lens,", "shop,", "plan"]
    tk = [T("t1", w) - 0.2 for w in words]
    k = 0.0
    for i, tw in enumerate(tk):
        if t >= tw: k = (i + clamp((t - tw) / 0.4)) / 4
    spokes = [("FRAME", glasses_el(150, "round")), ("LENS", lens_el(120)),
              ("SHOP", shopfront_el("SHOP", ORG_D, 110, 150)), ("PLAN", plan_card_el(150))]
    hub_map(f, 540, 1130, k, t, center="ONE\nCOMPANY", spokes=spokes, r=320)
    say(f, "THE TWIST", 500, 140, col=(255, 214, 60), t=t, t0=st0("S24") + 0.05)
    tp = T("t1", "pays.") - 0.15
    if t >= tp: say(f, "FRAME · LENS · SHOP · PLAN", 660, 64, col=(255, 214, 60), t=t, t0=tp)
    return finish(f, n)


def shot_S25(t, n):
    f = set_view("optician", t, 1.15, 540, 1000, blur=2.0)
    optician_dressing(f, t)
    person(f, 300, 1900, 1.1, OPTO, la=(18, 8), ra=(60, 30), mouth=0, look=(1, 0), expr="smirk")
    person(f, 790, 1900, 1.1, SHOPPER, la=(120, 150), ra=(18, 8), mouth=0, look=(-1, 0), expr="wow" if t > T("e0", "free") else "n", brow="up",
           hold=scale_el(rx_el(260), 1.0), hold_off=(-40, -90))
    say(f, "YOUR MOVE", 560, 130, col=(255, 214, 60), t=t, t0=st0("S25") + 0.05)
    tf = T("e0", "free") - 0.15
    if t >= tf: say(f, "FREE COPY OF YOUR Rx", 720, 96, t=t, t0=tf)
    src(f, "US law: FTC Eyeglass Rule", t, tf + 0.3, 860)
    return finish(f, n)


def shot_S26(t, n):
    f = stage("teal", (120, 255, 220), 540, 1000, 440)
    if t < T("e1", "That") - 0.15:
        comp(f, rx_el(300), 540, 1120, scale=pin(t, st0("S26") + 0.05, 0.3))
        for i, (x, y) in enumerate(((240, 900), (840, 900), (240, 1400), (840, 1400))):
            ta = T("e1", "anywhere") - 0.1 + 0.1 * i
            if t >= ta:
                arrow(f, (540, 1120), (x + (540 - x) * 0.35, y + (1120 - y) * 0.35), clamp((t - ta) / 0.3), col=WHITE, th=10)
                comp(f, glasses_el(200, **gl_style(i * 2 + 1), clear=True), x, y, scale=pin(t, ta + 0.2, 0.25))
        ui_word(f, "take it anywhere and", "COMPARE", 470, t, st0("S26") + 0.05, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    else:
        tree_scene(f, t, card=True, shop=True)
        ui_word(f, "that wall of choices?", "ONE COMPANY", 470, t, T("e1", "That") - 0.15, col=YEL_, size=150, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S27(t, n):
    f = stage("emerald", (255, 214, 120), 540, 880, 420)
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("ur glasses = 1 company", "wait WHAT", pr), 0.82), 600, 950, scale=pin(t, st0("S27")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(glasses_el(200, "round"), 0.8), hold_off=(20, -40))
        ui_word(f, "send this to the friend who", "PAID TOO MUCH", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=110, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "one") - 0.1, 0.25, 8), (T("i3", "sneakiest") - 0.15, 0.3, 10), (T("a2", "All") - 0.1, 0.25, 8),
           (T("a5", "one") - 0.2, 0.25, 8), (T("b2", "joined") + 0.55, 0.3, 10), (T("b3", "same") - 0.15, 0.25, 8),
           (T("c2", "same") - 0.15, 0.3, 10), (T("s2", "bought") - 0.15, 0.3, 12), (T("s4", "fell") - 0.15, 0.35, 14),
           (T("s5", "billion") - 0.25, 0.3, 10), (T("d3", "same") - 0.1, 0.3, 12), (T("t1", "pays.") - 0.15, 0.3, 12)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0 + 0.035 * clamp((tt - s["start"]) / max(0.5, s["end"] - s["start"]))
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
