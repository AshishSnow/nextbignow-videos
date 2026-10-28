# ================= shots: "Almost every banana you buy is the same clone" (type B — three reasons, the last one already happened) =================
# Generic props only: no banana-brand stickers, logos or packaging; variety names appear only as plain caption text.
FARMER = {"base": "worker", "hair": "hat", "hair_col": (214, 180, 110), "top": (236, 232, 218), "trim": (120, 92, 58),
          "pants": (120, 92, 58), "shoes": (80, 56, 36)}          # straw hat, white shirt, brown overalls (never the red-cap default)
BOSS = {"base": "exec", "top": (36, 70, 60), "tie": (255, 200, 40)}
SCI = {"base": "inventor", "top": (244, 246, 250), "trim": (60, 120, 200)}
GROCER = {"base": "oldman", "top": (240, 236, 226), "trim": (150, 60, 50)}
SHOPPER = "hero"

SHOTLIST = [
    ("S0", 0.0, "cut"), ("S0b", T("i1", "exact") - 0.15, "punch"),
    ("S1", T("i2", "That") - 0.12, "whip"), ("S2", T("i3", "Three") - 0.15, "zoom"),
    ("S3", T("a1", "Reason") - 0.2, "zoom"), ("S4", T("a2", "Those") - 0.15, "focus"),
    ("S5", T("a3", "So") - 0.12, "whip"), ("S5b", T("a3", "clone") - 0.3, "punch"),
    ("S6", T("a4", "Almost") - 0.15, "focus"), ("S7", T("a5", "nearly") - 0.35, "whip"),
    ("S8", T("a6", "Here's") - 0.15, "flash"), ("S8b", T("a6", "disease") - 0.25, "whip"),
    ("S9", T("b1", "Reason") - 0.2, "zoom"), ("S10", T("b2", "fungus") - 0.35, "whip"), ("S11", T("b3", "sneaks") - 0.25, "focus"),
    ("S12", T("b4", "There's") - 0.15, "whip"), ("S13", T("b5", "spores") - 0.35, "focus"),
    ("S14", T("b6", "Now") - 0.15, "whip"), ("S15", T("b7", "Colombia") - 0.2, "punch"),
    ("S16", T("b8", "Last") - 0.15, "flash"), ("S17", T("b9", "July") - 0.3, "whip"),
    ("S18", T("c0", "So") - 0.15, "whip"), ("S19", T("c1", "Reason") - 0.2, "zoom"),
    ("S20", T("c2", "Until") - 0.15, "focus"), ("S21", T("c3", "older") - 0.4, "whip"), ("S22", T("c4", "Companies") - 0.15, "whip"),
    ("S23", T("c5", "switched") - 0.35, "focus"),
    ("S24", T("t1", "Here's") - 0.15, "flash"), ("S25", T("t2", "new") - 0.3, "punch"),
    ("S26", T("e0", "Bananas") - 0.15, "whip"), ("S26b", T("e0", "But") - 0.15, "punch"),
    ("S27", T("e1", "Next") - 0.15, "focus"), ("S28", T("e2", "Send") - 0.2, "whip"),
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


def reason_label(f, t, t0, n_, text, col=WHITE):
    if t < t0: return
    comp(f, chip(f"REASON #{n_}", (255, 199, 30), INK, 46), 540, 380, scale=pin(t, t0, 0.25))
    say(f, text, 520, 150, col=col, t=t, t0=t0 + 0.1)


def copier_scene(f, t, lab="CLONE"):
    """frame-1 composition: a big photocopier printing identical bananas onto a conveyor belt"""
    title3d(f, "CLONES", 720, t, -1, size=270, face=(255, 214, 60), side=(150, 90, 10))
    cv2.rectangle(f, (150, 1480), (930, 1520), C((60, 64, 76)), -1, cv2.LINE_AA)
    for x in range(150, 931, 60):
        xx = int(930 - ((930 - x + t * 170) % 780)); cv2.line(f, (xx, 1482), (xx, 1518), C((120, 124, 136)), 4, cv2.LINE_AA)
    for x in (170, 910): cv2.circle(f, (x, 1500), 28, C((40, 42, 50)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (180, 1520), (900, 1580), C((40, 42, 50)), -1)
    comp(f, copier_el(600), 520, 1080)
    per = 0.85
    for i in range(9):
        q = (t + 8.0 - i * per) % (per * 9)
        if q < 0.4:
            u = q / 0.4; x, y, rot = 820 + 40 * u, 1040 + 390 * u * u, -20 + 20 * u
            op = 1.0
        else:
            x = 860 - (q - 0.4) * 170; y = 1430; op = clamp((x - 160) / 60); rot = 0
        if op > 0: rot_comp(f, banana_el(270, label=lab), x, y, rot, 1.0, op, 0.25)
    fl = (t % per) / per
    if fl < 0.25:
        _sglow(f, 470, 950, 300, (200, 255, 240), 0.6 * (1 - fl / 0.25))


def shot_S0(t, n):
    f = stage("teal", (120, 255, 220), 540, 1000, 440)
    copier_scene(f, t)
    ui_word(f, "why is almost every banana", "A COPY?", 470, t, -0.5, col=YEL_, size=190, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S0b(t, n):
    f = stage("purple", (255, 214, 60), 540, 1060, 430)
    for i, x in enumerate((220, 380, 540, 700, 860)):
        k = pin(t, st0("S0b") + 0.06 * i, 0.25)
        rot_comp(f, banana_el(250, label="#0001"), x, 1080 + 30 * math.sin(t * 3 + i), 90, k, 1.0, 0.3)
        comp(f, chip("#0001", WHITE, INK, 26), x, 1290, op=clamp(k))
    ui_word(f, "of the exact", "SAME PLANT", 470, t, T("i1", "exact") - 0.1, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S1(t, n):
    f = set_view("office", t, 1.15, 540, 1050, blur=2.0)
    tw = T("i2", "worried.") - 0.15
    for i, x in enumerate((300, 780)):
        person(f, x, 1770, 0.82, BOSS, la=(150, 200) if t >= tw else (18, 8), ra=(150, 200) if t >= tw else (60, -10),
               mouth=0, expr="wow" if t >= tw else "n", brow="sad" if t >= tw else "n", sweat=t >= tw, look=(1 - 2 * i, -1) if t < tw else (0, -1))
    comp(f, carton_el(240, "BANANAS", (210, 170, 80)), 540, 1640)
    comp(f, bunch_el(260), 540, 1430)
    say(f, "THE WHOLE BANANA BUSINESS", 560, 96, t=t, t0=T("i2", "whole") - 0.15)
    if t >= tw: say(f, "IS WORRIED", 700, 130, col=(255, 90, 80), t=t, t0=tw)
    return finish(f, n)


def shot_S2(t, n):
    f = stage("purple", (120, 140, 255), 540, 1050, 420)
    ui_word(f, "three reasons why", "3", 470, t, T("i3", "Three") - 0.1, col=YEL_, size=200, shadow=0.45, lead_col=WHITE)
    for i, (x, rot) in enumerate(((250, -8), (540, 0), (830, 8))):
        t0 = T("i3", "Three") + 0.12 * i
        rot_comp(f, numcard_el(i + 1, "REASON", (40, 110, 220), 250, i == 2), x, 1080 + (0 if i != 1 else -30), rot, pin(t, t0, 0.3), 1.0, 0.3)
    ta = T("i3", "already") - 0.1
    if t >= ta:
        k = clamp((t - ta) / 0.18)
        light_rays(f, 830, 1080, (255, 220, 160), 0.2)
        rot_comp(f, stamp_el("HAPPENED BEFORE", RED_, 58), 600, 1400, 6, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.0)
    return finish(f, n)


def shot_S3(t, n):
    f = set_view("study", t, 1.25, 540, 1050, blur=2.5)
    person(f, 540, 1900, 1.3, SHOPPER, la=(18, 8), ra=(120, 160), mouth=0, expr="wow" if t > T("a1", "seeds.") else "n",
           brow="up", look=(1, -1), hold=scale_el(banana_el(300), 0.9), hold_off=(40, -60))
    reason_label(f, t, T("a1", "Reason") - 0.1, 1, "NO SEEDS")
    return finish(f, n)


def shot_S4(t, n):
    f = stage("orange", (255, 230, 150), 540, 1060, 460)
    s0 = st0("S4")
    comp(f, slice_el(640), 540, 1080, scale=pin(t, s0, 0.3))
    for i, (a, rr_) in enumerate(((20, 0.14), (140, 0.09), (260, 0.14))):
        aa = math.radians(a); x, y = 536 + 640 * rr_ * math.cos(aa), 1076 + 640 * rr_ * math.sin(aa)
        if t >= s0 + 0.4 + 0.12 * i: cv2.circle(f, (int(x), int(y)), int(36 + 4 * math.sin(t * 6 + i)), C(RED_), 5, cv2.LINE_AA)
    tn = T("a2", "never") - 0.1
    if t >= tn:
        k = clamp((t - tn) / 0.5)
        cv2.line(f, (540, 1074), (540, int(1074 - 160 * k)), C((70, 170, 60)), 10, cv2.LINE_AA)
        if k > 0.5: cv2.ellipse(f, (556, int(1074 - 150 * k)), (30, 12), -30, 0, 360, C((70, 190, 60)), -1, cv2.LINE_AA)
        if t >= tn + 0.55:
            kk = clamp((t - tn - 0.55) / 0.18); rot_comp(f, stamp_el("WON'T GROW", RED_, 60), 540, 1500, -8, 1.5 - 0.5 * eo(kk), clamp(kk * 3), 0.0)
    ui_word(f, "those tiny black dots?", "NOT SEEDS", 470, t, T("a2", "Those") - 0.05, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S5(t, n):
    f = plantation_view(t, 1.12, 540, 1150)
    u = lt(t, "S5")
    comp(f, scale_el(plant_el(900, seed=3), 0.95), 330, 1800 - 430)
    xb = 690 + 40 * clamp(u / 2.5)
    person(f, xb + 80, 1800, 0.78, FARMER, la=(150, 140), ra=(150, 140), mouth=0, expr="smirk", look=(-1, 0),
           hold=scale_el(plant_el(900, fruit=False, seed=8), 0.28), hold_off=(-70, -60))
    tp = T("a3", "piece") - 0.1
    if t >= tp: say(f, "CUT FROM AN OLD ONE", 560, 110, t=t, t0=tp)
    else: say(f, "NO SEEDS = NO NEW PLANTS", 560, 96, t=t, t0=st0("S5") + 0.1)
    return finish(f, n)


def shot_S5b(t, n):
    f = plantation_view(t, 1.0, 540, 960, blur=1.5)
    t0 = st0("S5b") + 0.1
    for i, (x, y, s) in enumerate(((540, 1500, 0.6), (300, 1560, 0.5), (780, 1560, 0.5), (170, 1680, 0.62), (910, 1680, 0.62))):
        tt = t0 + 0.14 * i
        if t >= tt:
            comp(f, scale_el(plant_el(900, seed=3), s), x, y - 450 * s, scale=pin(t, tt, 0.25))
            if t < tt + 0.12: _sglow(f, x, int(y - 300), 220, (220, 255, 240), 0.8)
    say(f, "A CLONE", 560, 170, col=(255, 214, 60), t=t, t0=T("a3", "clone") - 0.1)
    return finish(f, n)


def shot_S6(t, n):
    f = stage("sky", (255, 240, 180), 540, 1060, 440)
    th = T("a4", "half") - 0.15
    k = clamp((t - th) / 0.8) if t >= th else 0.0
    pie_coin(f, 540, 1060, 300, 0.47 * max(0.02, k), BAN, "47%" if k > 0.5 else "?", 1.0, "")
    ui_word(f, "of all bananas grown", "ALMOST HALF", 470, t, th, col=WHITE, size=160, shadow=0.45, lead_col=WHITE)
    tc = T("a4", "Cavendish.") - 0.15
    if t >= tc: comp(f, chip("ONE TYPE: CAVENDISH", (255, 199, 30), INK, 46), 540, 1430, scale=pin(t, tc, 0.25))
    src(f, "Source: FAO — Cavendish ~47% of world banana output", t, th + 0.3, 1520)
    return finish(f, n)


def shot_S7(t, n):
    f = set_view("store", t, 1.12, 540, 1050, blur=1.5)
    comp(f, stand_el(760), 540, 1560)
    for i, x in enumerate((260, 400, 540, 680, 820)):
        comp(f, bunch_el(220), x, 1400 + (i % 2) * 20)
    person(f, 820, 1840, 0.72, SHOPPER, la=(18, 8), ra=(70, 40), mouth=0, look=(-1, 0), expr="n")
    comp(f, chip("CAVENDISH", WHITE, INK, 34), 540, 1260, op=clamp((t - st0("S7") - 0.3) / 0.3))
    say(f, "NEARLY EVERY ONE YOU BUY", 560, 110, t=t, t0=T("a5", "nearly") - 0.1)
    src(f, "FAO; The Conversation: ~99% of exports to rich countries", t, T("a5", "supermarket"), 700)
    return finish(f, n)


def shot_S8(t, n):
    f = stage("purple", (120, 255, 160), 540, 1050, 430)
    k = clamp((t - st0("S8")) / 0.8)
    helix(f, 330, 760, 1360, t, k=k); helix(f, 750, 760, 1360, t, k=k)
    if k > 0.5: say(f, "=", 1060, 200, col=(255, 214, 60))
    for x, lab in ((330, "BANANA IN LONDON"), (750, "BANANA IN NEW YORK")):
        comp(f, chip(lab, WHITE, INK, 26), x, 1440, op=clamp(k * 2 - 1))
    ui_word(f, "here's the problem:", "SAME GENES", 470, t, st0("S8") + 0.05, col=YEL_, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S8b(t, n):
    tk = T("a6", "kill") - 0.2
    sick = clamp((t - tk) / 1.6) if t >= tk else 0.0
    f = plantation_view(t, 1.3, 540, 1250, sick=sick)
    person(f, 540, 1880, 1.1, FARMER, la=(150, 200) if sick > 0.3 else (18, 8), ra=(150, 200) if sick > 0.3 else (18, 8), mouth=0,
           expr="wow" if sick > 0.2 else "n", brow="sad" if sick > 0.2 else "n", sweat=sick > 0.3, look=(0, -1))
    if t < T("a6", "all.") - 0.15: say(f, "ONE DISEASE…", 560, 140, t=t, t0=st0("S8b") + 0.05)
    else: say(f, "KILLS THEM ALL", 560, 150, col=(255, 90, 80), t=t, t0=T("a6", "all.") - 0.15)
    return finish(f, n)


def shot_S9(t, n):
    f = set_view("study", t, 1.2, 540, 1050, blur=2.5)
    person(f, 540, 1880, 1.15, SCI, la=(18, 8), ra=(120, 150), mouth=0, expr="n", brow="sad", look=(1, -1),
           hold=scale_el(flask_el(200, 0.5), 1.0), hold_off=(20, -60))
    reason_label(f, t, T("b1", "Reason") - 0.1, 2, "IT'S REAL")
    return finish(f, n)


def shot_S10(t, n):
    f = soil_view(t)
    comp(f, scale_el(plant_el(900, seed=2), 0.5), 540, 640 - 225)
    k = clamp((t - st0("S10")) / 1.5)
    hyphae(f, 540, 980, k, t, reach=330)
    spores(f, t, 30, k)
    say(f, "A SOIL FUNGUS", 460, 120, col=(255, 214, 60), t=t, t0=T("b2", "fungus") - 0.15)
    tt = T("b2", "Tropical") - 0.15
    if t >= tt: comp(f, chip("TROPICAL RACE 4  (TR4)", RED_, WHITE, 52), 540, 1480, scale=pin(t, tt, 0.3))
    return finish(f, n)


def shot_S11(t, n):
    f = stage("teal", (140, 230, 255), 540, 1000, 460)
    tb = T("b3", "blocks") - 0.15; tw = T("b3", "wilts") - 0.2
    sick = clamp((t - tw) / 1.2) if t >= tw else 0.0
    base_y = 1640
    comp(f, plant_el(900, sick=sick, seed=1), 540, base_y - 450)
    blk = clamp((t - tb) / 0.9) if t >= tb else 0.0
    for j in range(7):
        a = math.radians(20 + 140 * j / 6)
        cv2.line(f, (540, base_y), (int(540 + 160 * math.cos(a)), int(base_y + 120 * math.sin(a))), C((230, 210, 160)), 6, cv2.LINE_AA)
    for px in (522, 540, 558):
        y_top = base_y - 430; cut = base_y - (base_y - y_top) * blk
        cv2.line(f, (px, base_y), (px, int(y_top)), C((60, 160, 255)), 6, cv2.LINE_AA)
        if blk > 0: cv2.line(f, (px, base_y), (px, int(cut)), C((110, 70, 30)), 8, cv2.LINE_AA)
        for q in range(8):
            yy = base_y - ((t * 220 + q * 55 + px) % (base_y - y_top))
            if yy < cut - 6: cv2.circle(f, (px, int(yy)), 7, C((170, 230, 255)), -1, cv2.LINE_AA)
    tr = T("b3", "roots") - 0.2
    if t >= tr: hyphae(f, 540, base_y + 40, clamp((t - tr) / 1.2), t, seed=9, reach=200, col=(255, 120, 150))
    if t < tb: say(f, "IN THROUGH THE ROOTS", 470, 110, t=t, t0=max(st0("S11"), tr))
    elif t < tw: say(f, "BLOCKS THE WATER", 470, 130, col=(120, 200, 255), t=t, t0=tb)
    else: say(f, "WILTS AND DIES", 470, 140, col=(255, 90, 80), t=t, t0=tw)
    return finish(f, n)


def shot_S12(t, n):
    f = plantation_view(t, 1.15, 540, 1150, sick=0.8)
    u = lt(t, "S12")
    comp(f, scale_el(plant_el(900, sick=0.9, seed=4), 0.9), 330, 1780 - 405)
    person(f, 780, 1800, 0.78, FARMER, la=(110, 60), ra=(18, 8), mouth=0, expr="n", brow="sad", look=(-1, 0))
    rot_comp(f, spray_el(150), 640, 1290, -25, 1.0, 1.0, 0.2)
    ph = (u * 2.5) % 1
    if ph < 0.6:
        for i in range(10):
            q = ph + i * 0.03
            cv2.circle(f, (int(590 - 260 * q - i * 8), int(1250 - 40 * q + 10 * math.sin(i))), int(10 + 20 * q), C((230, 245, 255)), -1, cv2.LINE_AA)
    tn = T("b4", "No") - 0.1
    if t >= tn:
        k = clamp((t - tn) / 0.18); rot_comp(f, stamp_el("NO CURE", RED_, 110), 540, 960, -8, 1.6 - 0.6 * eo(k), clamp(k * 3), 0.0)
    say(f, "THERE'S NO CURE", 560, 130, t=t, t0=st0("S12") + 0.05)
    return finish(f, n)


def shot_S13(t, n):
    f = soil_view(t)
    spores(f, t, 46, 1.0)
    td = T("b5", "decades.") - 0.3
    flapboard(f, 540, 1140, "20+ YRS", t, T("b5", "wait") - 0.1)
    say(f, "SPORES WAIT", 460, 140, col=(255, 214, 60), t=t, t0=T("b5", "spores") - 0.15)
    if t >= td: comp(f, chip("FOR DECADES", RED_, WHITE, 60), 540, 1340, scale=pin(t, td, 0.3))
    src(f, "FAO (Sep 2026): stays in the soil for more than two decades", t, td, 1480)
    return finish(f, n)


MAP_PTS = dict(colombia=(-72.6, 11.3), peru=(-80.4, -5.0), venezuela=(-67.6, 10.1), ecuador=(-79.9, -3.4), ecuador2=(-80.15, -3.75),
               honduras=(-87.6, 15.4), costa=(-83.9, 10.2), panama=(-80.2, 8.6), guat=(-89.6, 15.4))


def shot_S14(t, n):
    f, cam_ = map_view(t, 1.0, 540, 1000)
    for i, key in enumerate(("ecuador", "colombia", "costa", "guat", "honduras")):
        x, y = map_pt(*MAP_PTS[key], cam_)
        comp(f, bunch_el(110), x, y - 20, scale=pin(t, st0("S14") + 0.12 * i, 0.25))
    k = clamp((t - st0("S14") - 0.6) / 1.0)
    if k > 0: arrow(f, map_pt(-79, 2, cam_), (860, 720), k, col=WHITE, th=10, bend=0.25)
    if k > 0.8: comp(f, chip("YOUR SHOP", WHITE, INK, 30), 860, 690)
    say(f, "NOW IT'S MOVING", 470, 140, col=(255, 214, 60), t=t, t0=T("b6", "moving") - 0.15)
    return finish(f, n)


def shot_S15(t, n):
    f, cam_ = map_view(t, 1.0, 540, 1000)
    for key, word, lab, yr, dx, dy in (("colombia", "Colombia,", "COLOMBIA", "2019", -150, -40), ("peru", "Peru,", "PERU", "2021", -40, 60),
                                       ("venezuela", "Venezuela,", "VENEZUELA", "2023", 150, 60)):
        tw = T("b7", word) - 0.1
        x, y = map_pt(*MAP_PTS[key], cam_)
        if t >= tw:
            blight(f, x, y, 46, (t - tw) / 0.8, t)
            map_pin(f, x, y, yr, None, t, tw)
            comp(f, chip(lab, INK, WHITE, 30), x + dx, y + dy, op=clamp((t - tw) / 0.25))
    say(f, "TR4 IS SPREADING", 470, 130, col=(255, 90, 80), t=t, t0=st0("S15") + 0.05)
    src(f, "ICA (Aug 2019) · SENASA (Apr 2021) · IPPC (Jan 2023)", t, st0("S15") + 0.4, 1560)
    return finish(f, n)


def _ecuador_map(t, zoom=2.0):
    f, cam_ = map_view(t, zoom, *map_xy(-79.0, -1.0))
    for key in ("colombia", "peru"):
        x, y = map_pt(*MAP_PTS[key], cam_); blight(f, x, y, 60, 1.0, t)
    return f, cam_


def shot_S16(t, n):
    f, cam_ = _ecuador_map(t, 2.0)
    te = T("b8", "Ecuador.") - 0.15
    x, y = map_pt(*MAP_PTS["ecuador"], cam_)
    if t >= te:
        blight(f, x, y, 70, (t - te) / 0.8, t)
        map_pin(f, x, y, "ECUADOR", "DEC 2025", t, te, big=True)
    tb = T("b8", "biggest") - 0.15
    say(f, "LAST DECEMBER", 470, 120, t=t, t0=st0("S16") + 0.05)
    if t >= tb: comp(f, chip("WORLD'S #1 BANANA EXPORTER", (255, 199, 30), INK, 46), 540, 1430, scale=pin(t, tb, 0.25))
    src(f, "Agrocalidad via Vistazo (18 Dec 2025); FreshPlaza (Feb 2026)", t, te + 0.3, 1530)
    return finish(f, n)


def shot_S17(t, n):
    f, cam_ = _ecuador_map(t, 2.6)
    x, y = map_pt(*MAP_PTS["ecuador"], cam_); blight(f, x, y, 80, 1.0, t)
    map_pin(f, x - 90, y, "FARM 1", None, t, -1)
    tj = T("b9", "July") - 0.2
    x2, y2 = map_pt(*MAP_PTS["ecuador2"], cam_)
    if t >= tj:
        blight(f, x2 + 110, y2 + 60, 80, (t - tj) / 0.6, t)
        map_pin(f, x2 + 110, y2 + 60, "FARM 2", "JULY 2026", t, tj, big=True)
    say(f, "A SECOND FARM", 470, 140, col=(255, 90, 80), t=t, t0=tj)
    src(f, "Agrocalidad via FreshFruitPortal (21 Jul 2026)", t, tj + 0.3, 1560)
    return finish(f, n)


def shot_S18(t, n):
    f = set_view("store", t, 1.2, 540, 1050, blur=2.0)
    ta = T("c0", "already") - 0.15
    person(f, 540, 1860, 0.95, SHOPPER, la=(120, 150), ra=(120, 150), mouth=0, expr="smirk" if t < ta else "wow", brow="up", look=(0, -1),
           hold=scale_el(banana_el(240, col=(200, 70, 70)), 0.8), hold_off=(-20, -40))
    if t < ta:
        say(f, "WHY NOT SWITCH?", 560, 140, t=t, t0=T("c0", "switch") - 0.15)
    else:
        k = clamp((t - ta) / 0.3)
        f[:] = f * (1 - 0.6 * k) + sepia_tone(f, 1.0) * 0.6 * k
        for i in range(10):
            yy = int((i * 197 + t * 2400) % H); cv2.line(f, (0, yy), (W, yy), C((255, 255, 255)), 3)
        for dx in (0, 70):
            cv2.fillPoly(f, [np.array([(470 + dx, 830), (530 + dx, 790), (530 + dx, 870)], np.int32)], C(WHITE), cv2.LINE_AA)
        say(f, "WE ALREADY DID", 600, 130, col=(255, 214, 60), t=t, t0=ta)
    return finish(f, n)


def _sep_stage(scheme):
    return sepia_tone(stage(scheme, (255, 230, 170), 540, 1050, 440), 1.0)


def shot_S19(t, n):
    f = _sep_stage("orange")
    flapboard(f, 540, 1080, "1950", t, st0("S19") + 0.15, col=(255, 230, 170))
    reason_label(f, t, T("c1", "Reason") - 0.1, 3, "IT HAPPENED BEFORE")
    return finish(f, n)


def shot_S20(t, n):
    f = set_view("store", t, 1.12, 540, 1050, blur=1.5)
    comp(f, stand_el(760), 540, 1560)
    for i, x in enumerate((280, 430, 580, 730)):
        comp(f, bunch_el(260, col=(250, 220, 70)), x, 1390 + (i % 2) * 18)
    person(f, 820, 1840, 0.74, GROCER, la=(18, 8), ra=(60, 30), mouth=0, look=(-1, 0), expr="smirk")
    f = sepia_tone(f, 0.85)
    hud_clock(f, "THE PAST", "1950s", None)
    if t < T("c2", "different") - 0.15: say(f, "BEFORE THE 1950s", 620, 120, col=(255, 230, 160), t=t, t0=st0("S20") + 0.05)
    else: say(f, "A DIFFERENT BANANA", 620, 120, col=(255, 230, 160), t=t, t0=T("c2", "different") - 0.15)
    comp(f, chip("GROS MICHEL", WHITE, INK, 40), 540, 1250, op=clamp((t - T("c2", "different")) / 0.3))
    return finish(f, n)


def _ca_map(t):
    return map_view(t, 2.0, *map_xy(-84.5, 12.5), sepia=True)


def shot_S21(t, n):
    f, cam_ = _ca_map(t)
    th = T("c3", "hit") - 0.15
    for i, key in enumerate(("honduras", "costa", "panama", "guat")):
        x, y = map_pt(*MAP_PTS[key], cam_)
        comp(f, bunch_el(110, col=(240, 214, 90)), x, y - 10, scale=pin(t, st0("S21") + 0.1 * i, 0.25))
        if t >= th + 0.25 * i: blight(f, x, y, 75, (t - th - 0.25 * i) / 0.7, t, col=(170, 40, 30))
    comp(f, chip("OLDER STRAIN: RACE 1", (170, 40, 30), WHITE, 44), 540, 1460, op=clamp((t - st0("S21") - 0.3) / 0.3))
    if t < T("c3", "Central") - 0.15: say(f, "SAME FUNGUS, OLDER STRAIN", 470, 100, col=(255, 230, 160), t=t, t0=st0("S21") + 0.05)
    else: say(f, "CENTRAL AMERICA", 470, 130, col=(255, 230, 160), t=t, t0=T("c3", "Central") - 0.15)
    return finish(f, n)


def shot_S22(t, n):
    f, cam_ = _ca_map(t)
    tf = T("c4", "followed") - 0.25
    hops = [(-87.6, 15.4), (-85.5, 14.0), (-83.6, 10.6), (-82.4, 9.0)]
    x, y = map_pt(*hops[0], cam_); blight(f, x, y, 70, 1.0, t, col=(170, 40, 30))
    for i in range(len(hops) - 1):
        a = map_pt(*hops[i], cam_); b = map_pt(*hops[i + 1], cam_)
        k = clamp((t - st0("S22") - 0.6 * i) / 0.5)
        if k > 0: arrow(f, a, b, k, col=(255, 240, 200), th=10, bend=0.3)
        if k >= 1: comp(f, bunch_el(100, col=(240, 214, 90)), b[0], b[1] - 10)
        if t >= tf + 0.35 * i: blight(f, b[0], b[1], 60, (t - tf - 0.35 * i) / 0.6, t, col=(170, 40, 30))
    say(f, "NEW LAND…", 470, 130, col=(255, 230, 160), t=t, t0=st0("S22") + 0.05)
    if t >= tf: say(f, "THE FUNGUS FOLLOWED", 1500, 110, col=(255, 120, 100), t=t, t0=tf)
    return finish(f, n)


def shot_S23(t, n):
    f = stage("emerald", (255, 230, 150), 540, 1050, 440)
    u = lt(t, "S23"); k = clamp(u / 1.2)
    cv2.rectangle(f, (380, 1330), (700, 1640), C((214, 208, 196)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (360, 1260), (720, 1330), C((240, 236, 226)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (360, 1260), (720, 1330), C(INK), 4, cv2.LINE_AA)
    rot_comp(f, bunch_el(380, col=(240, 214, 90), brown=0.5), 540 - 700 * eo(k), 1110, -20 * k, 1.0, 1 - k, 0.3)
    rot_comp(f, bunch_el(380), 540 + 700 * (1 - eo(k)), 1110, 0, 1.0, k, 0.3)
    tc = T("c5", "couldn't") - 0.15
    if t >= tc:
        kk = clamp((t - tc) / 0.18); rot_comp(f, stamp_el("RESISTANT", (30, 150, 70), 70), 770, 880, 10, 1.6 - 0.6 * eo(kk), clamp(kk * 3), 0.0)
    if t >= T("c5", "Cavendish.") - 0.2:
        light_rays(f, 540, 1100, (255, 236, 180), 0.25)
        say(f, "THE CAVENDISH", 520, 150, col=(255, 214, 60), t=t, t0=T("c5", "Cavendish.") - 0.2)
    else:
        say(f, "THE SWITCH", 520, 150, t=t, t0=st0("S23") + 0.05)
    if k < 1: f[:] = f * k + sepia_tone(f, 1.0) * (1 - k)
    return finish(f, n)


def shot_S24(t, n):
    f = stage("red", (255, 214, 120), 540, 1000, 440)
    copier_scene(f, t, lab="CLONE #2")
    ta = T("t1", "another") - 0.15
    if t < T("t1", "escape") - 0.1:
        say(f, "THE TWIST", 500, 150, col=(255, 214, 60), t=t, t0=st0("S24") + 0.05)
    elif t < ta:
        say(f, "TO ESCAPE ONE CLONE…", 500, 120, t=t, t0=T("t1", "escape") - 0.1)
    else:
        say(f, "…ANOTHER CLONE", 500, 150, col=(255, 214, 60), t=t, t0=ta)
    return finish(f, n)


def shot_S25(t, n):
    tk = T("t2", "kills") - 0.15
    br = clamp((t - tk) / 1.0) if t >= tk else 0.0
    f = plantation_view(t, 1.3, 540, 1100, blur=5.0, sick=0.3 + 0.7 * br)
    person_head_at(f, 540, 1080, 1.8, FARMER, mouth=0, expr="wow" if br > 0.3 else "n", brow="sad", look=(0, 1))
    rot_comp(f, banana_el(420, brown=0.9 * round(br * 5) / 5, spots=0.2), 540, 1560, -6, 1.0, 1.0, 0.3)
    spores(f, t, 18, br, y0=1440, y1=1700)
    say(f, "TR4 KILLS IT TOO", 520, 140, col=(255, 90, 80), t=t, t0=tk)
    return finish(f, n)


def shot_S26(t, n):
    f = set_view("store", t, 1.15, 540, 1050, blur=1.8)
    comp(f, stand_el(760), 540, 1560)
    cols = [BAN, (200, 70, 70), (150, 200, 70), (250, 230, 90), (230, 160, 60)]
    for i, (x, c) in enumerate(zip((250, 395, 540, 685, 830), cols)):
        comp(f, bunch_el(200, n=4 + i % 2, col=c), x, 1400 + (i % 2) * 18, scale=pin(t, st0("S26") + 0.08 * i, 0.25))
    say(f, "BANANAS WON'T VANISH", 560, 120, t=t, t0=st0("S26") + 0.05)
    comp(f, chip("OTHER KINDS STILL GROW", WHITE, INK, 34), 540, 720, op=clamp((t - st0("S26") - 0.6) / 0.3))
    return finish(f, n)


def shot_S26b(t, n):
    f = stage("orange", (255, 230, 150), 540, 1100, 440)
    th = T("e0", "hits") - 0.2
    tip = clamp((t - th) / 0.5) if t >= th else 0.0
    rot_comp(f, basket_el(520), 540 + 60 * tip, 1300 + 40 * tip, -24 * eo(tip), 1.0, 1.0, 0.3)
    for i, x in enumerate((420, 500, 580, 660)):
        q = max(0.0, t - th - 0.05 * i) if t >= th else 0.0
        rot_comp(f, bunch_el(180), x + 80 * tip + 260 * q * (1 if i % 2 else -0.6), 1170 + 40 * tip + 900 * q * q, 90 * q * (1 if i % 2 else -1), 1.0, 1.0, 0.2)
    if t >= th:
        k = clamp((t - th) / 0.18); rot_comp(f, stamp_el("ONE PROBLEM", RED_, 60), 540, 880, -8, 1.5 - 0.5 * eo(k), clamp(k * 3), 0.0)
    ui_word(f, "everything on", "ONE BET", 470, t, st0("S26b") + 0.05, col=WHITE, size=170, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S27(t, n):
    f = stage("teal", (120, 255, 220), 540, 1000, 440)
    copier_scene(f, t)
    ui_word(f, "next time you peel one:", "A COPY", 470, t, st0("S27") + 0.05, col=YEL_, size=190, shadow=0.45, lead_col=WHITE)
    return finish(f, n)


def shot_S28(t, n):
    f = stage("emerald", (255, 214, 120), 540, 880, 420)
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("ur banana is a clone", "wait WHAT", pr), 0.82), 600, 950, scale=pin(t, st0("S28")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=scale_el(banana_el(200), 0.6), hold_off=(20, -40))
        ui_word(f, "send this to the friend who", "EATS ONE EVERY DAY", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=96, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "exact") - 0.15, 0.25, 8), (T("i2", "worried.") - 0.15, 0.3, 10), (T("i3", "already") - 0.1, 0.3, 12),
           (T("a2", "never") + 0.45, 0.25, 8), (T("a6", "kill") - 0.2, 0.3, 10), (T("b4", "No") - 0.1, 0.3, 14),
           (T("b7", "Colombia,") - 0.1, 0.2, 8), (T("b7", "Peru,") - 0.1, 0.2, 8), (T("b7", "Venezuela,") - 0.1, 0.2, 8),
           (T("b8", "Ecuador.") - 0.15, 0.35, 14), (T("b9", "July") - 0.2, 0.25, 10), (T("c5", "couldn't") - 0.15, 0.25, 8),
           (T("t2", "kills") - 0.15, 0.35, 14), (T("e0", "hits") - 0.2, 0.3, 12)]


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
