# HOW TO START — "The used office chair flip" (BRIGHT EXPLAINER look, 11 Nov 2026). Shots keyed to the VO lines.
def L0(lid): return LINES[lid]["start"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.06, "whip"), ("S_i3", L0("i3") - 0.06, "pop"), ("S_s1", L0("s1") - 0.08, "whip"),
            ("S_s2", L0("s2") - 0.06, "pop"), ("S_a1", L0("a1") - 0.08, "whip"), ("S_a2", L0("a2") - 0.06, "pop"), ("S_a3", L0("a3") - 0.06, "whip"),
            ("S_a4", L0("a4") - 0.06, "pop"), ("S_b1", L0("b1") - 0.08, "whip"), ("S_b2", L0("b2") - 0.06, "pop"), ("S_b3", L0("b3") - 0.06, "whip"),
            ("S_c1", L0("c1") - 0.08, "whip"), ("S_c2", L0("c2") - 0.06, "pop"), ("S_c3", L0("c3") - 0.06, "whip"), ("S_d1", L0("d1") - 0.08, "whip"),
            ("S_d2", L0("d2") - 0.06, "pop"), ("S_d3", L0("d3") - 0.06, "whip"), ("S_z1", L0("z1") - 0.08, "pop")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.25, "impact"), (TW("i1", "dump", off=-0.05), "whoosh"), (TW("i1", "twelve"), "pop"), (TW("i2", "Grab"), "pop"), (TW("i2", "fix"), "pop"),
        (TW("i2", "sell"), "pop"), (TW("i3", "three"), "slam"), (TW("i3", "win"), "ding"), (TW("s1", "eight"), "impact"), (L0("s1") + 0.3, "truck"),
        (TW("s2", "Wild"), "pop"), (L0("a1"), "slam"), (TW("a1", "dump"), "truck"), (TW("a2", "close"), "pop"), (TW("a2", "move"), "pop"),
        (TW("a2", "renovate"), "pop"), (TW("a2", "Fast"), "whoosh"), (TW("a3", "call"), "ring"), (TW("a4", "edge"), "ding"), (L0("b1"), "slam"),
        (TW("b2", "nine"), "pop"), (TW("b2", "bad"), "buzz"), (TW("b3", "clean"), "spray"), (TW("b3", "wheels"), "pop"), (TW("b3", "sell"), "ding"),
        (L0("c1"), "slam"), (TW("c2", "Startups"), "pop"), (TW("c2", "Clinics"), "pop"), (TW("c2", "co-working"), "pop"), (TW("c3", "half"), "chaching"),
        (TW("d1", "Herman"), "pop"), (TW("d1", "five-year"), "ding"), (TW("d2", "van"), "pop"), (TW("d2", "storage"), "pop"), (TW("d2", "time"), "pop"),
        (TW("d2", "lose"), "buzz"), (TW("d3", "buy"), "impact"), (L0("z1"), "whoosh")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia
exec(open(f"{_D}/brightkit.py").read())
SURF = skia.Surface(W, H)
A = f"{B}/assets"; CH_CLEAN, CH_WORN, CH_BLUE, CH_PILE = f"{A}/chair_clean.png", f"{A}/chair_worn.png", f"{A}/chair_blue.png", f"{A}/chair_pile.png"


def bob(t, k=1.0): return 8 * k * math.sin(t * 2.2)


def drop(t, t0, d=0.35): return (1 - eout(pr(t, t0, d))) * -900   # y offset for objects dropping in


def phone(c, x, y, s=1.0, t=0.0, ring=True):
    c.save(); c.translate(x, y); c.scale(s, s)
    if ring: c.rotate(8 * math.sin(t * 40))
    p = rrect(-80, -150, 80, 150, 26); shadow(c, p, 0, 14, 16, 0.3); c.drawPath(p, P(NAVY)); c.drawRoundRect(skia.Rect.MakeLTRB(-66, -124, 66, 110), 14, 14, P((80, 200, 255)))
    text(c, "CALLING", 0, -40, 26, WHITE, XB_F, shadow_=False); c.drawCircle(0, 40, 28, P(GRN))
    c.restore()
    if ring:
        for k in range(3): c.drawArc(skia.Rect.MakeLTRB(x + 70 + k * 26 - 60, y - 140 - k * 26, x + 70 + k * 26 + 60, y - 20 + k * 26), -60, 60, False, S(WHITE, 8, 0.8 - k * 0.2))


def box3(c, x, y, s=1.0, col=(214, 160, 100)):
    c.save(); c.translate(x, y); c.scale(s, s)
    p = path([(-120, -180), (120, -180), (120, 0), (-120, 0)]); shadow(c, p, 6, 12, 14, 0.25); c.drawPath(p, lin(-120, 0, 120, 0, [shade(col, 1.1), shade(col, 0.85)]))
    c.drawRect(skia.Rect.MakeLTRB(-20, -180, 20, 0), P(shade(col, 0.75))); c.restore()


def clock(c, x, y, r=90, t=0.0):
    cp = skia.Path(); cp.addCircle(x, y, r); shadow(c, cp, 0, 10, 14, 0.3); c.drawCircle(x, y, r, P(WHITE)); c.drawCircle(x, y, r, S(NAVY, 12))
    for a_, L in ((t * 2.0, r * 0.7), (t * 0.3, r * 0.5)): c.drawLine(x, y, x + L * math.sin(a_), y - L * math.cos(a_), S(NAVY, 10))


def ui_icon(c, kind, x, y, s=1.0, col=YEL):
    c.save(); c.translate(x, y); c.scale(s, s)
    cp = skia.Path(); cp.addCircle(0, 0, 100); shadow(c, cp, 0, 12, 16, 0.3); c.drawCircle(0, 0, 100, rad(-30, -30, 160, [shade(col, 1.2), col, shade(col, 0.85)]))
    if kind == "save": c.drawPath(path([(-40, -56), (40, -56), (40, 60), (0, 30), (-40, 60)]), P(NAVY))
    elif kind == "send": c.drawPath(path([(-56, 40), (-56, 0), (-10, -40), (20, -40), (20, -70), (70, -20), (20, 30), (20, 0), (-10, 0), (-30, 20)]), P(NAVY))
    elif kind == "comment":
        b = rrect(-62, -50, 62, 30, 26); b = skia.Op(b, path([(-30, 20), (0, 20), (-40, 60)]), skia.PathOp.kUnion_PathOp); c.drawPath(b, P(NAVY))
    c.restore()


def tick(c, x, y, s=1.0, col=GRN):
    c.save(); c.translate(x, y); c.scale(s, s); c.drawCircle(0, 0, 34, P(col)); c.drawPath(path([(-16, 0), (-4, 14), (18, -14)], False), S(WHITE, 9)); c.restore()


def cross(c, x, y, s=1.0, col=RED):
    c.save(); c.translate(x, y); c.scale(s, s); c.drawCircle(0, 0, 34, P(col)); c.drawLine(-14, -14, 14, 14, S(WHITE, 9)); c.drawLine(14, -14, -14, 14, S(WHITE, 9)); c.restore()


def mini_chairs(c, x, y, n, h=150, k=1.0):
    for i in range(n):
        ki = back(pr(k, i * 0.06, 0.3), 2.0)
        if ki > 0: obj(c, CH_CLEAN, x + (i % 5 - 2) * 150, y + (i // 5) * 170, h * ki, shadow_=False)


# ---------------------------------------------------------------- shots
def S_i1(c, t, n):
    u = lt(t, "S_i1"); set_bg(c, (20, 110, 255), (100, 40, 230), YEL, 540, 1000, 430, t, rays=True)
    big_word(c, "$1,200", 1150, WHITE, 300, 0.22)
    tb = TW("i1", "dump", off=-0.1); kb = eout(pr(t, tb, 0.35))
    if kb > 0: icon_bin(c, 1260 - 380 * kb, 1380, 0.9, lid=ease(pr(t, tb + 0.3, 0.3)))
    rot = -18 * ease(pr(t, tb + 0.3, 0.5))
    obj(c, CH_CLEAN, 470 - 60 * ease(pr(t, tb + 0.3, 0.5)), 1390 + drop(t, -0.12, 0.3) + bob(t, 0.3), 720, rot)
    sticker(c, "$1,200", 690, 820, 84, RED, WHITE, -10, back(pr(t, TW("i1", "twelve", off=-0.1), 0.3), 2.2))
    # the title: on screen from the very first frame
    tag(c, "BUSINESS IDEA", 540, 300, 46, YEL, NAVY)
    text(c, "THE OFFICE CHAIR FLIP", 540, 420, 92, WHITE, BLACK_F, maxw=960)


def S_i2(c, t, n):
    set_bg(c, (255, 120, 40), (255, 60, 110), WHITE, 540, 980, 0)
    steps = (("GRAB", "Grab", CH_WORN, ORG), ("FIX", "fix", None, TEAL), ("SELL x10", "sell", CH_CLEAN, GRN))
    for i, (lab, w_, img, col) in enumerate(steps):
        k = back(pr(t, TW("i2", w_, off=-0.1), 0.3), 1.8); y = 620 + i * 330
        if k <= 0: continue
        def body(cc, img=img, lab=lab, col=col, i=i):
            if img: obj(cc, img, -240, 130, 250, shadow_=False)
            else: icon_wrench(cc, -270, -10, 0.55); icon_spray(cc, -170, 100, 0.55, t)
            text(cc, lab, 90, 34, 96, col, BLACK_F, shadow_=False)
        card(c, 540, y, 860, 280, WHITE, k, tilt=(-1) ** i * 0.6, body=body)
        if i < 2 and pr(t, TW("i2", steps[i + 1][1], off=-0.1), 0.01) > 0: c.drawPath(path([(520, y + 150), (560, y + 150), (540, y + 185)]), P(WHITE))
    headline(c, t, L0("i2"), "", "A WHOLE BUSINESS", y=330, col=WHITE, size=96)


def S_i3(c, t, n):
    set_bg(c, (110, 40, 230), (30, 20, 90), PUR, 540, 980, 0, t, rays=True)
    headline(c, t, L0("i3") - 0.05, "HOW IT WORKS", "3 STEPS", y=420, col=YEL, size=150)
    for i, (lab, col) in enumerate((("FIND", YEL), ("FIX", TEAL), ("SELL", GRN))):
        k = back(pr(t, TW("i3", "three", off=0.05 + 0.18 * i), 0.3), 2.0); x = 220 + i * 320
        badge(c, i + 1, x, 900, k * (1.15 if i == 0 and t > TW("i3", "win", off=-0.1) else 1.0), col, 120)
        if k > 0: text(c, lab, x, 1110, 70, WHITE, BLACK_F, a=min(1, k))
    if t > TW("i3", "win", off=-0.1):
        tag(c, "WIN OR LOSE HERE", 300, 1250, 44, RED, WHITE, -4, back(pr(t, TW("i3", "win", off=-0.1), 0.25), 2.2))


def S_s1(c, t, n):
    u = lt(t, "S_s1"); set_bg(c, (120, 200, 255), (60, 140, 230), (255, 236, 200), 540, 1150, 520)
    big_word(c, "LANDFILL", 1160, WHITE, 260, 0.35)
    obj(c, CH_PILE, 540, 1400, 640 * (0.6 + 0.4 * eout(pr(u, 0, 0.6))))
    icon_truck(c, -260 + 540 * eout(pr(u, 0.1, 0.9)), 1500, 0.8, GRN, t, "")
    headline(c, t, TW("s1", "eight", off=-0.15), "EVERY YEAR · USA", "8.5 MILLION TONS", y=430, col=WHITE, size=118, small_bg=RED, small_fg=WHITE)
    if t > TW("s1", "furniture", off=-0.1): tag(c, "OFFICE FURNITURE & GEAR", 540, 640, 46, WHITE, NAVY, k=back(pr(t, TW("s1", "furniture", off=-0.1), 0.25)))


def S_s2(c, t, n):
    set_bg(c, (120, 200, 255), (60, 140, 230), (255, 236, 200), 540, 1150, 520)
    def body(cc):
        text(cc, "SOURCE", 0, -110, 44, (120, 130, 160), XB_F, shadow_=False)
        text(cc, "US ENVIRONMENTAL", 0, -20, 66, NAVY, BLACK_F, shadow_=False); text(cc, "PROTECTION AGENCY", 0, 60, 66, NAVY, BLACK_F, shadow_=False)
        text(cc, "ESTIMATE", 0, 140, 48, BLU, XB_F, shadow_=False)
    card(c, 540, 880, 900, 380, WHITE, back(pr(lt(t, "S_s2"), 0, 0.3)), tilt=0.5, body=body)
    sticker(c, "WILD.", 760, 1220, 110, PNK, WHITE, 8, back(pr(t, TW("s2", "Wild", off=-0.05), 0.25), 2.4))


def S_a1(c, t, n):
    u = lt(t, "S_a1"); set_bg(c, (255, 200, 0), (255, 120, 0), WHITE, 540, 1000, 0)
    badge(c, 1, 540, 560, back(pr(u, 0, 0.3), 2.0), WHITE, 130)
    headline(c, t, L0("a1") + 0.2, "", "FIND THE CHAIRS", y=820, col=NAVY, size=100)
    td = TW("a1", "dump", off=-0.3)
    if t > td:   # the race: your van vs the dump truck
        k = eout(pr(t, td, 1.6)); c.drawRect(skia.Rect.MakeLTRB(0, 1380, W, 1400), P(NAVY, 0.25))
        icon_truck(c, -200 + 700 * k, 1360, 0.55, (90, 100, 110), t, "DUMP"); icon_van(c, -100 + 1000 * k, 1180, 0.55, WHITE, t)
        tag(c, "BEFORE THE DUMP TRUCK", 540, 1000, 44, NAVY, WHITE, k=back(pr(t, td, 0.25)))


def S_a2(c, t, n):
    u = lt(t, "S_a2"); set_bg(c, (40, 200, 190), (10, 110, 160), (255, 240, 220), 540, 1100, 470)
    icon_building(c, 540, 1460, 1.25, BLU, lit=0.9 - 0.6 * ease(pr(u, 0.5, 2)))
    for i, (w_, lab, col) in enumerate((("close", "CLOSING", RED), ("move", "MOVING", ORG), ("renovate", "RENOVATING", PUR))):
        tag(c, lab, 270 + (i % 2) * 540, 700 + i * 140, 48, col, WHITE, (-1) ** i * 5, back(pr(t, TW("a2", w_, off=-0.1), 0.25), 2.2))
    headline(c, t, TW("a2", "empty", off=-0.15), "THEY NEED THE FLOOR", "EMPTY. FAST.", y=420, col=WHITE, size=118)
    if t > TW("a2", "Fast", off=-0.1): clock(c, 880, 1150, 80, t * 8)


def S_a3(c, t, n):
    u = lt(t, "S_a3"); set_bg(c, (255, 90, 120), (160, 40, 160), WHITE, 540, 1000, 0, t, rays=True)
    def body(cc):
        text(cc, "FURNITURE DEALER", 0, -40, 60, NAVY, BLACK_F, shadow_=False); text(cc, "TEXAS, USA", 0, 40, 46, PNK, XB_F, shadow_=False)
    card(c, 540, 560, 820, 230, WHITE, back(pr(u, 0, 0.3)), body=body)
    phone(c, 540, 1000, 1.1 * back(pr(t, TW("a3", "call", off=-0.3), 0.3)), t, ring=t > TW("a3", "call", off=-0.1))
    for i, (lab, w_) in enumerate((("LANDLORDS", "landlords"), ("BROKERS", "brokers"))):
        tag(c, lab, 300 + i * 480, 1250, 50, YEL, NAVY, (-1) ** i * 4, back(pr(t, TW("a3", w_, off=-0.1), 0.25)))
    headline(c, t, TW("a3", "want", off=-0.1), "", "\"CLEAR IT OUT\"", y=1420, col=WHITE, size=92)


def S_a4(c, t, n):
    u = lt(t, "S_a4"); set_bg(c, (20, 30, 80), (60, 30, 140), BLU, 540, 1000, 0)
    headline(c, t, L0("a4") + 0.05, "COST PER CHAIR", "ONE vs THIRTY", y=400, col=WHITE, size=110)
    k = pr(t, L0("a4") + 0.4, 1.4)
    bars(c, 540, 1240, [100, 35], [RED, GRN], ["ONE AT A TIME", "30 FROM ONE FLOOR"], k, 520, 220, 160)
    if t > TW("a4", "thirty", off=-0.1): mini_chairs(c, 690, 700, 0)
    sticker(c, "YOUR EDGE", 690, 680, 70, GRN, WHITE, 6, back(pr(t, TW("a4", "edge", off=-0.1), 0.25), 2.2))


def S_b1(c, t, n):
    u = lt(t, "S_b1"); set_bg(c, (0, 200, 200), (0, 120, 170), WHITE, 540, 1000, 0)
    badge(c, 2, 540, 560, back(pr(u, 0, 0.3), 2.0), WHITE, 130)
    headline(c, t, L0("b1") + 0.2, "", "MAKE THEM LOOK GOOD", y=830, col=NAVY, size=92)
    obj(c, CH_CLEAN, 540, 1470 + bob(t), 560);
    for i in range(4):
        a_ = (t * 2 + i * 0.25) % 1; r_ = 26 * math.sin(a_ * math.pi)
        x, y = 360 + i * 120, 1000 + (i % 2) * 140; c.drawPath(path([(x, y - r_), (x + r_ * 0.25, y - r_ * 0.25), (x + r_, y), (x + r_ * 0.25, y + r_ * 0.25), (x, y + r_), (x - r_ * 0.25, y + r_ * 0.25), (x - r_, y), (x - r_ * 0.25, y - r_ * 0.25)]), P(WHITE))


def S_b2(c, t, n):
    u = lt(t, "S_b2"); set_bg(c, (90, 90, 110), (50, 50, 70), (150, 150, 170), 540, 1100, 460)
    big_word(c, "UGLY", 1230, WHITE, 320, 0.18)
    obj(c, CH_WORN, 540, 1460, 640, -3)
    sticker(c, "$400", 300, 820, 90, NAVY, WHITE, -10, back(pr(u, 0.1, 0.3), 2.0))
    k9 = back(pr(t, TW("b2", "nine", off=-0.1), 0.25), 2.4)
    if k9 > 0:
        c.drawLine(200, 760, 400, 840, S(RED, 14)); sticker(c, "$9.99", 780, 880, 96, RED, WHITE, 8, k9)
    headline(c, t, TW("b2", "bad", off=-0.3), "STILL DIDN'T SELL", "IF IT LOOKS BAD", y=430, col=WHITE, size=100, small_bg=RED, small_fg=WHITE)


def S_b3(c, t, n):
    u = lt(t, "S_b3"); set_bg(c, (40, 210, 140), (0, 140, 120), WHITE, 540, 1050, 0)
    kc = ease(pr(t, TW("b3", "clean", off=0.2), 1.2))   # the worn chair turns clean under a wipe line
    c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, W * (1 - kc), H)); obj(c, CH_WORN, 540, 1420, 600, shadow_=True); c.restore()
    c.save(); c.clipRect(skia.Rect.MakeLTRB(W * (1 - kc), 0, W, H)); obj(c, CH_CLEAN, 540, 1420, 600, shadow_=False); c.restore()
    if 0 < kc < 1: c.drawRect(skia.Rect.MakeLTRB(W * (1 - kc) - 6, 600, W * (1 - kc) + 6, 1480), P(WHITE, 0.9))
    icon_spray(c, 150 if kc < 1 else -400, 900, 0.7, t)
    for i, (lab, w_) in enumerate((("CLEAN THE FABRIC", "clean"), ("SWAP BROKEN WHEELS", "wheels"), ("TIGHTEN EVERY BOLT", "tighten"))):
        k = back(pr(t, TW("b3", w_, off=-0.1), 0.25))
        if k > 0: tick(c, 120, 400 + i * 110, k); text(c, lab, 180, 418 + i * 110, 52, WHITE, BLACK_F, "l", a=min(1, k))
    headline(c, t, TW("b3", "Looks", off=-0.1), "", "LOOKS SELL.", y=1560 - 120, col=YEL, size=120)


def S_c1(c, t, n):
    u = lt(t, "S_c1"); set_bg(c, (40, 140, 255), (20, 60, 200), WHITE, 540, 1000, 0)
    badge(c, 3, 540, 560, back(pr(u, 0, 0.3), 2.0), WHITE, 130)
    headline(c, t, L0("c1") + 0.2, "", "SELL IN BULK", y=830, col=YEL, size=120)
    mini_chairs(c, 540, 1080, 10, 150, pr(u, 0.4, 1.2) * 1.6)


def S_c2(c, t, n):
    u = lt(t, "S_c2"); set_bg(c, (255, 150, 30), (255, 80, 60), WHITE, 540, 1000, 0)
    for i, (kind, lab, w_, col) in enumerate((("startup", "STARTUPS", "Startups", BLU), ("tutor", "TUTORING", "tutoring", GRN), ("clinic", "CLINICS", "Clinics", RED), ("cowork", "CO-WORKING", "co-working", PUR))):
        k = back(pr(t, TW("c2", w_, off=-0.1), 0.3), 2.0)
        if k <= 0: continue
        x, y = 300 + (i % 2) * 480, 640 + (i // 2) * 360; people_icon(c, kind, x, y, k, col); text(c, lab, x, y + 170, 52, WHITE, BLACK_F, a=min(1, k))
    headline(c, t, TW("c2", "lots", off=-0.15), "THEY NEED", "LOTS OF SEATS", y=1360, col=WHITE, size=104, t1=TW("c2", "full", off=-0.15))
    headline(c, t, TW("c2", "full", off=-0.1), "THEY HATE PAYING", "FULL PRICE", y=1360, col=YEL, size=120)


def S_c3(c, t, n):
    u = lt(t, "S_c3"); set_bg(c, (20, 30, 80), (40, 120, 120), GRN, 540, 1000, 0)
    headline(c, t, L0("c3") + 0.05, "ONE REAL BUYER", "SAVED AT LEAST HALF", y=430, col=YEL, size=96)
    bars(c, 540, 1260, [100, 50], [RED, GRN], ["OTHER STORES", "USED"], pr(t, L0("c3") + 0.3, 1.2), 520, 240, 180)
    if t > TW("c3", "half", off=-0.1):
        for i in range(6): icon_coin(c, 300 + i * 100, 640 + ((t * 600 + i * 90) % 300), 40, t * 6 + i)
        sticker(c, "-50%", 780, 760, 100, GRN, WHITE, 8, back(pr(t, TW("c3", "half", off=-0.1), 0.25), 2.4))


def S_d1(c, t, n):
    u = lt(t, "S_d1"); set_bg(c, (255, 70, 150), (130, 40, 220), YEL, 540, 1080, 420, t, rays=True)
    kn = pr(t, L0("d1"), 0.3)
    if t < TW("d1", "Herman", off=-0.1):
        text(c, "TINY NICHE?", 540, 520, 120, WHITE, BLACK_F, a=kn)
    else:
        text(c, "TINY NICHE?", 540, 520, 120, WHITE, BLACK_F, a=0.5); c.drawLine(160, 480, 920, 500, S(RED, 16))
    big_word(c, "REFURB", 1200, WHITE, 250, 0.25)
    obj(c, CH_BLUE, 540, 1430 + bob(t, 0.5), 640)
    tag(c, "HERMAN MILLER · AERON REFURBISHED", 540, 700, 40, WHITE, NAVY, k=back(pr(t, TW("d1", "Herman", off=-0.1), 0.25)))
    sticker(c, "5-YEAR WARRANTY", 540, 1580 - 120, 64, GRN, WHITE, -4, back(pr(t, TW("d1", "five-year", off=-0.1), 0.25), 2.2))
    if t > TW("d1", "US", off=-0.1): tag(c, "US & CANADA", 820, 830, 40, NAVY, WHITE, 6, back(pr(t, TW("d1", "US", off=-0.1), 0.25)))


def S_d2(c, t, n):
    u = lt(t, "S_d2"); set_bg(c, (40, 40, 70), (20, 20, 40), (60, 60, 100), 540, 1000, 0)
    headline(c, t, L0("d2") + 0.05, "HONESTLY", "NOT FREE MONEY", y=420, col=YEL, size=110)
    items = (("A VAN", "van", True), ("STORAGE", "storage", True), ("TIME", "time", True), ("PRICES VARY BY CITY", "city", False), ("YOU CAN LOSE MONEY", "lose", False))
    for i, (lab, w_, need) in enumerate(items):
        k = back(pr(t, TW("d2", w_, off=-0.1), 0.25))
        if k <= 0: continue
        y = 640 + i * 150; (tick if need else cross)(c, 170, y, k, GRN if need else RED)
        text(c, lab, 240, y + 22, 60, WHITE, BLACK_F, "l", a=min(1, k))
    icon_van(c, 860, 1500 - 120, 0.5, WHITE, 0)


def S_d3(c, t, n):
    u = lt(t, "S_d3"); set_bg(c, (255, 206, 0), (255, 140, 0), WHITE, 540, 1000, 0, t, rays=True)
    tag(c, "THE FLIPPER'S RULE", 540, 520, 50, NAVY, WHITE, k=back(pr(u, 0.05, 0.25)))
    def body(cc):
        text(cc, "PROFIT IS MADE", 0, -40, 84, NAVY, BLACK_F, shadow_=False); text(cc, "WHEN YOU BUY", 0, 60, 96, RED, BLACK_F, shadow_=False)
    card(c, 540, 820, 900, 300, WHITE, back(pr(t, TW("d3", "profit", off=-0.1), 0.3)), tilt=-0.5, body=body)
    if t > TW("d3", "sell", off=-0.2): text(c, "NOT WHEN YOU SELL", 540, 1110, 64, NAVY, BLACK_F, a=pr(t, TW("d3", "sell", off=-0.2), 0.2))
    obj(c, CH_CLEAN, 540, 1490 + bob(t), 380)


def S_z1(c, t, n):
    u = lt(t, "S_z1"); set_bg(c, (20, 110, 255), (100, 40, 230), YEL, 540, 1100, 400, t, rays=True)
    obj(c, CH_CLEAN, 540, 1440 + bob(t), 560)
    for i, (kind, lab, tt_, col) in enumerate((("save", "SAVE", L0("z1"), YEL), ("send", "SEND", TW("z1", "Send"), TEAL), ("comment", "COMMENT", L0("z2"), PNK))):
        k = back(pr(t, tt_, 0.3), 2.0)
        if k > 0: ui_icon(c, kind, 240 + i * 300, 640, k * 0.9, col); text(c, lab, 240 + i * 300, 800, 50, WHITE, BLACK_F, a=min(1, k))
    headline(c, t, L0("z2") + 0.3, "", "WHICH BUSINESS NEXT?", y=420, col=WHITE, size=86)


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    c = SURF.getCanvas(); c.clear(skia.Color(0, 0, 0)); c.save()
    for ti, kind in CUES:   # screen shake on impacts
        if kind in ("slam", "impact") and 0 <= t - ti < 0.28:
            k = 1 - (t - ti) / 0.28; c.translate(16 * k * math.sin(t * 90), 12 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z = 1.0 + 0.045 * u; c.translate(W / 2, H * 0.5); c.scale(z, z); c.translate(-W / 2, -H * 0.5)   # slow push-in, never still
    RENDER[sid](c, t, n); c.restore()
    return SURF.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; img = _draw(sh["id"], t, n); dt = t - sh["start"]; flash = 0.0
    if i > 0 and sh["trans"] == "whip" and dt < 0.22:   # whip pan: old frame flies left, new one in from the right, motion-blurred
        p = eout(dt / 0.22); prev = _draw(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n)
        off = int(W * p); out = np.empty_like(img); out[:, :W - off] = prev[:, off:]; out[:, W - off:] = img[:, :off]
        kx = max(1, int(90 * (1 - abs(2 * p - 1)))); img = cv2.blur(out, (kx * 2 + 1, 1))
    if i > 0 and sh["trans"] == "pop" and dt < 0.16:   # zoom punch + a soft white flash
        z = 1.12 - 0.12 * eout(dt / 0.16); M = cv2.getRotationMatrix2D((540, 960), 0, z); img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        flash = 0.35 * (1 - dt / 0.16)
    return (finish(img, flash) * 255 + 0.5).astype(np.uint8)
