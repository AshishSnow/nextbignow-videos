# HOW IT WORKS — "Sell me this pen" (BRIGHT EXPLAINER look + flat characters, American voices; 11 Nov 2026). Shots keyed to the VO lines.
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.06, "whip"), ("S_i3", L0("i3") - 0.06, "pop"), ("S_a1", L0("a1") - 0.08, "whip"),
            ("S_a2", L0("a2") - 0.06, "pop"), ("S_a3", L0("a3") - 0.06, "cut"), ("S_a4", L0("a4") - 0.06, "pop"), ("S_b0", L0("b0") - 0.08, "whip"),
            ("S_b1", L0("b1") - 0.06, "pop"), ("S_b2", L0("b2") - 0.06, "whip"), ("S_c1", L0("c1") - 0.08, "pop"), ("S_c3", L0("c3") - 0.06, "cut"),
            ("S_c5", L0("c5") - 0.06, "cut"), ("S_c6", L0("c6") - 0.06, "pop"), ("S_d1", L0("d1") - 0.08, "whip"), ("S_d2", L0("d2") - 0.06, "pop"),
            ("S_d3", L0("d3") - 0.06, "whip"), ("S_z1", L0("z1") - 0.08, "pop")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.2, "impact"), (L0("i2"), "whoosh"), (TW("i2", "job"), "buzz"), (TW("i3", "lose"), "buzz"), (TW("i3", "three"), "slam"),
        (L0("a1"), "whoosh"), (TW("a2", "smooth"), "pop"), (TW("a2", "smudges"), "pop"), (TW("a2", "three"), "pop"), (L0("a3"), "pop"),
        (L0("a4"), "buzz"), (L0("b0"), "whoosh"), (L0("b1"), "pop"), (TW("b2", "Watch"), "ding"), (L0("c1"), "pop"), (L0("c2"), "pop"),
        (TW("c3", "died"), "buzz"), (L0("c4"), "pop"), (L0("c5"), "pop"), (TW("c6", "take"), "chaching"), (L0("d1"), "whoosh"),
        (TW("d1", "need"), "ding"), (TW("d2", "noise"), "buzz"), (TW("d2", "answer"), "ding"), (TW("d3", "one"), "slam"), (TW("d3", "two"), "slam"),
        (TW("d3", "three"), "slam"), (L0("z1"), "whoosh")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia
exec(open(f"{_D}/brightkit.py").read())
SURF = skia.Surface(W, H)
A = f"{B}/assets"; PEN, CHAIR = f"{A}/pen.png", f"{A}/chair_clean.png"
BOSS_L = {"i1", "a3", "c2", "c4", "c6"}; YOUNG_L = {"a2", "c1", "c3", "c5"}


def mth(t): return talk(t) / 3.0


def speaking(t, ids):
    return any(LINES[i]["start"] <= t <= LINES[i]["end"] for i in ids if i in LINES)


def blink(t): return (int(t * 12) % 41) in (0, 1)


def bob(t, k=1.0): return 8 * k * math.sin(t * 2.2)


def office(c, t, top=(120, 200, 255), bot=(255, 214, 160)):
    """bright office: big window with a city, a wall, a desk edge"""
    c.drawRect(skia.Rect.MakeWH(W, H), lin(0, 0, 0, H, [(255, 236, 214), (255, 200, 160)]))
    c.drawRoundRect(skia.Rect.MakeLTRB(80, 260, 1000, 900), 30, 30, lin(0, 260, 0, 900, [top, bot]))
    r = np.random.default_rng(3); x = 90
    while x < 990:
        w_ = r.integers(60, 130); h_ = r.integers(150, 420); col = (90, 120, 200) if r.random() < 0.5 else (70, 100, 180)
        c.drawRect(skia.Rect.MakeLTRB(x, 890 - h_, min(990, x + w_), 890), P(col))
        for wy in range(int(890 - h_ + 20), 880, 34):
            for wx in range(int(x + 10), int(min(990, x + w_) - 14), 26): c.drawRect(skia.Rect.MakeXYWH(wx, wy, 12, 16), P((255, 236, 170), 0.8))
        x += w_ + 6
    c.drawRect(skia.Rect.MakeLTRB(530, 260, 550, 900), P(WHITE)); c.drawRect(skia.Rect.MakeLTRB(80, 570, 1000, 586), P(WHITE))
    c.drawRoundRect(skia.Rect.MakeLTRB(80, 260, 1000, 900), 30, 30, S(WHITE, 18))
    # plant
    c.drawRoundRect(skia.Rect.MakeLTRB(900, 1060, 990, 1180), 14, 14, P((240, 120, 60)))
    for a_ in (-50, -20, 10, 40): c.save(); c.translate(945, 1070); c.rotate(a_); c.drawOval(skia.Rect.MakeLTRB(-22, -150, 22, 0), P((40, 170, 100))); c.restore()


def desk(c, y=1330):
    p = path([(0, y), (W, y), (W, y + 300), (0, y + 300)]); c.drawPath(p, lin(0, y, 0, y + 300, [(196, 132, 80), (150, 96, 56)]))
    c.drawRect(skia.Rect.MakeLTRB(0, y, W, y + 18), P((226, 166, 110)))


def two_shot(c, t, boss_expr="neutral", young_expr="neutral", young_arm=None, boss_arm=None, zoom=1.0):
    office(c, t)
    bt = speaking(t, BOSS_L); yt = speaking(t, YOUNG_L)
    person(c, 280, 1000, 0.95, t, "boss", mth(t) if bt else 0, boss_expr, (0.6, 0), blink(t), boss_arm)
    person(c, 790, 1040, 0.95, t, "young", mth(t) if yt else 0, young_expr, (-0.6, 0), blink(t + 0.4), young_arm)
    desk(c)


def pen_obj(c, x, y, h=420, rot=0.0): obj(c, PEN, x, y, h, rot, shadow_=False)


# ---------------------------------------------------------------- shots
def S_i1(c, t, n):
    u = lt(t, "S_i1"); set_bg(c, (20, 110, 255), (100, 40, 230), YEL, 540, 980, 420, t, rays=True)
    big_word(c, "PEN", 1180, WHITE, 420, 0.2)
    c.save(); c.translate(540, 960); c.rotate(12 * math.sin(t * 1.6)); pen_obj(c, 0, 260 + bob(t, 1.5), 600); c.restore()
    tag(c, "THE FAMOUS SALES TEST", 540, 300, 46, YEL, NAVY)
    text(c, "SELL ME THIS PEN", 540, 420, 112, WHITE, BLACK_F, maxw=960)
    bubble_line(c, "Can you sell me this pen?", 560, 1470 - 120, back(pr(t, L0("i1") - 0.1, 0.3)), who="INTERVIEWER", tail="left", size=58)


def S_i2(c, t, n):
    two_shot(c, t, "skeptical", "surprised")
    headline(c, t, TW("i2", "costs", off=-0.2), "WHY THIS QUESTION", "COSTS PEOPLE THE JOB", y=420, col=WHITE, size=86, small_bg=RED, small_fg=WHITE)


def S_i3(c, t, n):
    u = lt(t, "S_i3"); set_bg(c, (255, 120, 40), (255, 60, 110), WHITE, 540, 1000, 0)
    tl = TW("i3", "three", off=-0.15)
    if t < tl:
        obj(c, CHAIR, 540, 1420 + bob(t, 0.4), 640)
        tag(c, "YOU", 540, 760, 70, NAVY, WHITE, k=back(pr(u, 0.05, 0.25)))
        headline(c, t, TW("i3", "bad", off=-0.15), "ONE BAD ANSWER", "= NO JOB", y=430, col=WHITE, size=130)
    else:
        headline(c, t, tl, "THE BEST ANSWER", "3 STEPS", y=430, col=YEL, size=150)
        for i, (lab, col) in enumerate((("ASK", YEL), ("FIND THE NEED", TEAL), ("THEIR WORDS", GRN))):
            k = back(pr(t, tl + 0.15 + 0.2 * i, 0.3), 2.0); x = 220 + i * 320
            badge(c, i + 1, x, 900, k * (1.15 if i == 2 and t > TW("i3", "smartest", off=-0.1) else 1.0), col, 120)
            if k > 0: text(c, lab, x, 1100, 52, WHITE, BLACK_F, a=min(1, k), maxw=300)


def S_a1(c, t, n):
    u = lt(t, "S_a1"); set_bg(c, (60, 60, 80), (30, 30, 50), (90, 90, 120), 540, 1000, 420)
    pen_obj(c, 540, 1300, 520, -20)
    headline(c, t, L0("a1"), "FIRST", "THE MOVE MOST PEOPLE MAKE", y=430, col=WHITE, size=80)


def S_a2(c, t, n):
    two_shot(c, t, "neutral", "happy" if not speaking(t, YOUNG_L) else "smile", young_arm="pen")
    pen_obj(c, 575, 1250 + bob(t), 240, -25)
    bubble_line(c, "This pen writes super smooth, it never smudges, and it's only $3!", 600, 420, back(pr(t, L0("a2"), 0.3)), tail="right", who="YOU", who_bg=TEAL, size=46)
    for i, (lab, w_) in enumerate((("SMOOTH", "smooth"), ("NO SMUDGE", "smudges"), ("$3", "three"))):
        tag(c, lab, 230 + i * 310, 740, 40, YEL, NAVY, (-1) ** i * 6, back(pr(t, TW("a2", w_, off=-0.1), 0.25), 2.2))


def S_a3(c, t, n):
    two_shot(c, t, "skeptical", "neutral", young_arm="pen")
    pen_obj(c, 575, 1250, 240, -25)
    bubble_line(c, "I don't need a pen.", 420, 520, back(pr(t, L0("a3"), 0.25)), tail="left", who="INTERVIEWER", size=58)


def S_a4(c, t, n):
    u = lt(t, "S_a4"); set_bg(c, (240, 52, 60), (150, 20, 40), (255, 120, 120), 540, 1000, 0)
    k = 0.82 * back(pr(u, 0, 0.25), 2.4); c.save(); c.translate(540, 760); c.rotate(-6); c.scale(k, k)
    c.drawRoundRect(skia.Rect.MakeLTRB(-430, -150, 430, 110), 30, 30, S(WHITE, 18)); text(c, "GAME OVER", 0, 40, 150, WHITE, BLACK_F); c.restore()
    headline(c, t, TW("a4", "nobody", off=-0.1), "HE TALKED ABOUT THE PEN", "NOBODY ASKED", y=1200, col=YEL, size=110)


def S_b0(c, t, n):
    u = lt(t, "S_b0"); set_bg(c, (20, 30, 70), (60, 30, 120), PUR, 540, 1000, 0, t, rays=True)
    def body(cc):   # a film clapperboard drawn as an icon + the film title in plain text (no film imagery)
        cc.drawRect(skia.Rect.MakeLTRB(-120, -150, 120, -20), P(NAVY))
        for i in range(5): cc.drawPath(path([(-120 + i * 52, -150), (-94 + i * 52, -150), (-120 + i * 52 + 50, -190), (-146 + i * 52 + 50, -190)]), P(WHITE if i % 2 else NAVY))
        text(cc, "THE WOLF OF", 0, 70, 66, NAVY, BLACK_F, shadow_=False); text(cc, "WALL STREET", 0, 150, 76, RED, BLACK_F, shadow_=False)
        text(cc, "2013 FILM", 0, 220, 40, (120, 130, 160), XB_F, shadow_=False)
    card(c, 540, 860, 760, 600, WHITE, back(pr(u, 0, 0.3)), tilt=0.6, body=body)
    tag(c, "MADE FAMOUS BY", 540, 460, 50, YEL, NAVY, k=back(pr(u, 0.1, 0.25)))


def S_b1(c, t, n):
    u = lt(t, "S_b1"); set_bg(c, (255, 206, 0), (255, 140, 0), WHITE, 540, 1000, 0)
    def body(cc):
        f = font(BLACK_F, 200); cc.drawString("“", -330, -90, f, P(ORG))
        for i, l_ in enumerate(("Before I'm even going to", "sell a pen to anybody,", "I need to know", "about the person.")):
            text(cc, l_, 0, -60 + i * 78, 56, NAVY, XB_F, shadow_=False)
        text(cc, "JORDAN BELFORT", 0, 300, 44, RED, BLACK_F, shadow_=False); text(cc, "via The Globe and Mail", 0, 350, 34, (120, 130, 160), SB_F, shadow_=False)
    card(c, 540, 880, 900, 860, WHITE, back(pr(u, 0, 0.3)), tilt=-0.4, body=body)
    tag(c, "THE REAL BROKER BEHIND THE MOVIE", 540, 360, 40, NAVY, WHITE, k=back(pr(u, 0.1, 0.25)))


def S_b2(c, t, n):
    u = lt(t, "S_b2"); set_bg(c, (0, 200, 200), (0, 120, 170), WHITE, 540, 1000, 0, t, rays=True)
    for i in range(7):
        x = 160 + i * 130; y = 1300 - ((t * 160 + i * 140) % 700)
        text(c, "?", x, y, 120 + 30 * (i % 3), WHITE, BLACK_F, a=0.85)
    headline(c, t, L0("b2"), "SO THE PROS", "ASK QUESTIONS", y=520, col=NAVY, size=120)
    if t > TW("b2", "Watch", off=-0.1): sticker(c, "WATCH THIS", 540, 820, 90, RED, WHITE, -5, back(pr(t, TW("b2", "Watch", off=-0.1), 0.25), 2.2))


def S_c1(c, t, n):
    tb = L0("c2") - 0.05
    two_shot(c, t, "neutral" if t < tb else "smile", "smile", young_arm=None)
    if t < tb: bubble_line(c, "When did you last use a pen?", 620, 470, back(pr(t, L0("c1"), 0.25)), tail="right", who="YOU", who_bg=TEAL, size=56)
    else:
        bubble_line(c, "This morning. I signed a big contract.", 440, 470, back(pr(t, tb, 0.25)), tail="left", who="INTERVIEWER", size=54)
        tag(c, "QUESTION 1", 800, 720, 40, TEAL, WHITE, 5)


def S_c3(c, t, n):
    tb = L0("c4") - 0.05
    two_shot(c, t, "surprised" if t < tb else "skeptical", "neutral")
    if t < tb:
        bubble_line(c, "And what if your pen had died right then?", 620, 470, back(pr(t, L0("c3"), 0.25)), tail="right", who="YOU", who_bg=TEAL, size=52)
        k = pr(t, TW("c3", "died", off=-0.1), 0.6)
        if k > 0:   # a dead pen: a scribble that fades out
            p_ = skia.Path(); p_.moveTo(200, 760)
            for i in range(14): p_.lineTo(220 + i * 40, 740 + (40 if i % 2 else -10) * (1 - i / 14))
            m = skia.PathMeasure(p_, False); ln = m.getLength(); pt = S(NAVY, 10, 1 - 0.7 * k); pt.setPathEffect(skia.DashPathEffect.Make([ln * k, ln], 0)); c.drawPath(p_, pt)
            cross(c, 840, 740, back(pr(t, TW("c3", "died"), 0.25)))
    else:
        bubble_line(c, "Honestly? That would've been pretty embarrassing.", 440, 470, back(pr(t, tb, 0.25)), tail="left", who="INTERVIEWER", size=50)
        tag(c, "QUESTION 2", 800, 720, 40, TEAL, WHITE, 5)


def S_c5(c, t, n):
    two_shot(c, t, "neutral", "smile", young_arm="pen")
    pen_obj(c, 575, 1250 + bob(t), 240, -25)
    bubble_line(c, "So you need one that never lets you down. This one's yours for $3.", 600, 470, back(pr(t, L0("c5"), 0.25)), tail="right", who="YOU", who_bg=TEAL, size=48)
    tag(c, "THEIR OWN WORDS", 300, 720, 42, GRN, WHITE, -5, back(pr(t, TW("c5", "never", off=-0.1), 0.25)))


def S_c6(c, t, n):
    two_shot(c, t, "happy", "happy", young_arm="pen")
    pen_obj(c, 575, 1250, 240, -25)
    bubble_line(c, "Okay, you got me. I'll take it, and I might grab a spare for the car.", 440, 470, back(pr(t, L0("c6"), 0.25)), tail="left", who="INTERVIEWER", size=56)
    sticker(c, "SOLD!", 760, 760, 110, GRN, WHITE, 8, back(pr(t, TW("c6", "take", off=-0.05), 0.25), 2.4))


def S_d1(c, t, n):
    u = lt(t, "S_d1"); set_bg(c, (20, 30, 80), (60, 30, 140), BLU, 540, 1000, 0)
    headline(c, t, L0("d1"), "", "SAME PEN. SAME PRICE.", y=400, col=WHITE, size=96)
    for i, (lab, good) in enumerate((("PITCH FEATURES", False), ("ASK QUESTIONS", True))):
        k = back(pr(t, L0("d1") + 0.3 + 0.3 * i, 0.3))
        def body(cc, lab=lab, good=good):
            pen_obj(cc, 0, 120, 260, -20); text(cc, lab, 0, 210, 46, NAVY, BLACK_F, shadow_=False, maxw=380)
        card(c, 290 + i * 500, 880, 440, 560, WHITE, k, tilt=(-1) ** i * 0.6, body=body)
        if k > 0: (tick if good else cross)(c, 290 + i * 500, 590, k * 1.4)
    headline(c, t, TW("d1", "found", off=-0.1), "THE DIFFERENCE", "HE FOUND THE NEED FIRST", y=1330, col=YEL, size=80)


def S_d2(c, t, n):
    u = lt(t, "S_d2"); set_bg(c, (255, 70, 150), (130, 40, 220), WHITE, 540, 1000, 0, t, rays=True)
    tag(c, "WORKS IN ANY BUSINESS", 540, 420, 50, YEL, NAVY, k=back(pr(u, 0.05, 0.25)))
    def b1(cc): text(cc, "LIST FEATURES", 0, -10, 70, NAVY, BLACK_F, shadow_=False); text(cc, "= JUST NOISE", 0, 80, 70, RED, BLACK_F, shadow_=False)
    def b2(cc): text(cc, "FIND THEIR PROBLEM", 0, -10, 64, NAVY, BLACK_F, shadow_=False); text(cc, "= THE ANSWER", 0, 80, 72, GRN, BLACK_F, shadow_=False)
    card(c, 540, 760, 900, 300, WHITE, back(pr(t, TW("d2", "List", off=-0.1), 0.3)), tilt=0.5, body=b1)
    card(c, 540, 1150, 900, 300, WHITE, back(pr(t, TW("d2", "Find", off=-0.1), 0.3)), tilt=-0.5, body=b2)


def S_d3(c, t, n):
    u = lt(t, "S_d3"); set_bg(c, (110, 40, 230), (30, 20, 90), PUR, 540, 980, 0, t, rays=True)
    headline(c, t, L0("d3"), "TRY IT NEXT TIME", "3 STEPS", y=420, col=YEL, size=150)
    for i, (lab, w_, col) in enumerate((("ASK", "one", YEL), ("FIND THE NEED", "two", TEAL), ("THEIR WORDS", "three", GRN))):
        k = back(pr(t, TW("d3", w_, off=-0.1), 0.3), 2.0); x = 220 + i * 320
        badge(c, i + 1, x, 880, k, col, 120)
        if k > 0: text(c, lab, x, 1080, 52, WHITE, BLACK_F, a=min(1, k), maxw=300)
    pen_obj(c, 540, 1460, 300, -60)


def S_z1(c, t, n):
    u = lt(t, "S_z1"); set_bg(c, (20, 110, 255), (100, 40, 230), YEL, 540, 1100, 400, t, rays=True)
    c.save(); c.translate(540, 1100); c.rotate(10 * math.sin(t * 1.6)); pen_obj(c, 0, 260 + bob(t, 1.5), 520); c.restore()
    for i, (kind, lab, tt_, col) in enumerate((("save", "SAVE", L0("z1"), YEL), ("send", "SEND", TW("z1", "Send"), TEAL), ("comment", "COMMENT", L0("z2"), PNK))):
        k = back(pr(t, tt_, 0.3), 2.0)
        if k > 0: ui_icon(c, kind, 240 + i * 300, 620, k * 0.9, col); text(c, lab, 240 + i * 300, 780, 50, WHITE, BLACK_F, a=min(1, k))
    headline(c, t, L0("z2") + 0.2, "", "WHAT SHOULD I SELL NEXT?", y=420, col=WHITE, size=80)


def ui_icon(c, kind, x, y, s=1.0, col=YEL):
    c.save(); c.translate(x, y); c.scale(s, s)
    cp = skia.Path(); cp.addCircle(0, 0, 100); shadow(c, cp, 0, 12, 16, 0.3); c.drawCircle(0, 0, 100, rad(-30, -30, 160, [shade(col, 1.2), col, shade(col, 0.85)]))
    if kind == "save": c.drawPath(path([(-40, -56), (40, -56), (40, 60), (0, 30), (-40, 60)]), P(NAVY))
    elif kind == "send": c.drawPath(path([(-56, 40), (-56, 0), (-10, -40), (20, -40), (20, -70), (70, -20), (20, 30), (20, 0), (-10, 0), (-30, 20)]), P(NAVY))
    else:
        b = rrect(-62, -50, 62, 30, 26); b = skia.Op(b, path([(-30, 20), (0, 20), (-40, 60)]), skia.PathOp.kUnion_PathOp); c.drawPath(b, P(NAVY))
    c.restore()


def tick(c, x, y, s=1.0, col=GRN):
    c.save(); c.translate(x, y); c.scale(s, s); c.drawCircle(0, 0, 34, P(col)); c.drawPath(path([(-16, 0), (-4, 14), (18, -14)], False), S(WHITE, 9)); c.restore()


def cross(c, x, y, s=1.0, col=RED):
    c.save(); c.translate(x, y); c.scale(s, s); c.drawCircle(0, 0, 34, P(col)); c.drawLine(-14, -14, 14, 14, S(WHITE, 9)); c.drawLine(14, -14, -14, 14, S(WHITE, 9)); c.restore()


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    c = SURF.getCanvas(); c.clear(skia.Color(0, 0, 0)); c.save()
    for ti, kind in CUES:
        if kind in ("slam", "impact") and 0 <= t - ti < 0.28:
            k = 1 - (t - ti) / 0.28; c.translate(16 * k * math.sin(t * 90), 12 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z = 1.0 + 0.045 * u; c.translate(W / 2, H * 0.5); c.scale(z, z); c.translate(-W / 2, -H * 0.5)
    RENDER[sid](c, t, n); c.restore()
    return SURF.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; img = _draw(sh["id"], t, n); dt = t - sh["start"]; flash = 0.0
    if i > 0 and sh["trans"] == "whip" and dt < 0.22:
        p = eout(dt / 0.22); prev = _draw(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n)
        off = int(W * p); out = np.empty_like(img); out[:, :W - off] = prev[:, off:]; out[:, W - off:] = img[:, :off]
        kx = max(1, int(90 * (1 - abs(2 * p - 1)))); img = cv2.blur(out, (kx * 2 + 1, 1))
    if i > 0 and sh["trans"] == "pop" and dt < 0.16:
        z = 1.12 - 0.12 * eout(dt / 0.16); M = cv2.getRotationMatrix2D((540, 960), 0, z); img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
        flash = 0.35 * (1 - dt / 0.16)
    return (finish(img, flash) * 255 + 0.5).astype(np.uint8)
