# HOW THEY GOT SO BIG · EP 3 — Michelin (RETRO ANIME pilot, 8 Nov 2026). Host: KAI (animekit.py). Shots keyed to the VO lines.
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


SHOTLIST = [("S_i1", 0.0, "cut"), ("S_i2", L0("i2") - 0.08, "flash"), ("S_i3", L0("i3") - 0.08, "wipe"), ("S_s1", L0("s1") - 0.1, "wipe"),
            ("S_s2", L0("s2") - 0.08, "cut"), ("S_a1", L0("a1") - 0.1, "wipe"), ("S_a2", L0("a2") - 0.06, "flash"), ("S_a3", L0("a3") - 0.06, "flash"),
            ("S_a4", L0("a4") - 0.08, "cut"), ("S_a4b", TW("a4", "guess", off=-0.1), "flash"), ("S_b1", L0("b1") - 0.1, "wipe"), ("S_b2", L0("b2") - 0.06, "cut"),
            ("S_b2b", TW("b2", "workbench", off=-0.05), "flash"), ("S_b3", L0("b3") - 0.06, "cut"), ("S_b3b", TW("b3", "nineteen", off=-0.1), "cut"),
            ("S_c1", L0("c1") - 0.1, "wipe"), ("S_c2", L0("c2") - 0.06, "cut"), ("S_c3", L0("c3") - 0.06, "flash"), ("S_c4", L0("c4") - 0.06, "cut"),
            ("S_c5", L0("c5") - 0.06, "cut"), ("S_c5b", TW("c5", "Clever", off=-0.1), "flash"), ("S_d1", L0("d1") - 0.08, "wipe"), ("S_d2", L0("d2") - 0.06, "cut"),
            ("S_z1", L0("z1") - 0.08, "wipe")]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
# sound cues for mix.py: (time, kind)
CUES = [(0.05, "sparkle"), (TW("i1", "tyre", off=-0.1), "impact"), (L0("i2"), "slam"), (TW("i2", "free", off=-0.1), "slam"), (L0("i3"), "slam"),
        (TW("i3", "genius"), "sparkle"), (L0("s1") + 0.3, "car"), (TW("s1", "three"), "slam"), (TW("s2", "Nobody", 1), "impact"), (L0("a1"), "slam"),
        (TW("a1", "red"), "page"), (TW("a3", "free"), "stamp"), (L0("a4"), "car"), (TW("a4", "guess", off=0.1), "chaching"), (L0("b1"), "slam"),
        (TW("b1", "walks"), "bell"), (TW("b2", "workbench"), "impact"), (L0("b3"), "scratch"), (TW("b3", "nineteen"), "stamp"), (L0("c1"), "slam"),
        (TW("c1", "Secret"), "glint"), (TW("c2", "nobody"), "glint"), (TW("c3", "star"), "sparkle"), (TW("c3", "three"), "sparkle"),
        (TW("c4", "detour"), "slam"), (TW("c4", "journey"), "slam"), (L0("c5") + 0.4, "car"), (TW("c5", "Clever"), "sparkle"),
        (TW("d1", "ad"), "slam"), (L0("z1"), "whoosh")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia
exec(open(f"{_D}/animekit.py").read())
SURF = skia.Surface(W, H)
YEL, PINK, TEAL, CREAM2, RED2 = (255, 214, 60), (250, 70, 110), (24, 160, 160), (255, 250, 240), (230, 40, 50)


def mth(t): return talk(t) / 3.0


def blink(n): return 1.0 if (n // 2) % 23 == 0 else 0.0


def sunset(c, t, sun=True, city=True, top=(54, 26, 104), mid=(250, 86, 120), bot=(255, 196, 120)):
    sky(c, top, mid, bot)
    if sun: retro_sun(c, 540, 980 + 10 * math.sin(t * 0.5), 330)
    if city:
        skyline(c, 1300, (90, 40, 110), 3, hmin=160, hmax=420); skyline(c, 1380, (50, 24, 80), 1, windows=(255, 220, 120))
        c.drawRect(skia.Rect.MakeLTRB(0, 1380, W, H), P((40, 20, 64)))


def countryside(c, t, pan=0.0):
    sky(c, (70, 150, 240), (150, 210, 250), (255, 236, 200))
    for i, (cx, cy) in enumerate(((200, 420), (760, 330), (520, 560))):   # painted clouds
        x = (cx - pan * 0.2 + 1200) % 1400 - 160
        for k in range(4): c.drawCircle(x + k * 60, cy - (20 if k % 2 else 0), 60 - 6 * (k % 3), P((255, 255, 255), 0.95))
    c.save(); c.translate(-pan * 0.4 % 400, 0); hills(c, 1180, (120, 190, 130), 70, 4); c.restore()
    c.save(); c.translate(-pan * 0.7 % 400, 0); hills(c, 1300, (80, 160, 90), 50, 6); c.restore()
    c.drawPath(path([(0, 1420), (W, 1400), (W, 1560), (0, 1580)]), P((214, 180, 130)))      # dirt road
    for i in range(14):
        x = (i * 120 - pan * 1.0) % (W + 120) - 60; c.drawRect(skia.Rect.MakeLTRB(x, 1488, x + 50, 1496), P((190, 150, 100)))
    c.drawRect(skia.Rect.MakeLTRB(0, 1570, W, H), P((90, 150, 80)))


def shop_bg(c, t):
    sky(c, (90, 54, 40), (150, 96, 60), (210, 150, 90))
    for row in range(3):   # tyres on the back wall
        for i in range(6): tyre(c, 110 + i * 172, 420 + row * 230, 92, 0, a=0.85)
    c.drawRect(skia.Rect.MakeLTRB(0, 1180, W, H), P((120, 80, 52)))
    for i in range(8): c.drawLine(0, 1220 + i * 80, W, 1220 + i * 80, S((100, 64, 40), 4))


def noir_bg(c, t):
    sky(c, (16, 10, 30), (50, 24, 60), (24, 12, 36))
    g = skia.GradientShader.MakeRadial(skia.Point(540, 700), 700, [C((255, 210, 140), 0.45), C((255, 210, 140), 0.0)])
    p = skia.Paint(); p.setShader(g); c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), p)
    for i in range(7): c.drawRect(skia.Rect.MakeLTRB(i * 170 - 20, 0, i * 170 + 40, 1100), P((255, 220, 160), 0.05))   # blinds light


def night_bg(c, t):
    sky(c, (10, 14, 50), (40, 30, 100), (120, 60, 140))
    r = np.random.default_rng(5)
    for i in range(120):
        x, y = r.uniform(0, W), r.uniform(0, 1300); tw_ = 0.5 + 0.5 * math.sin(t * 3 + i)
        c.drawCircle(x, y, r.uniform(1.5, 4), P((255, 255, 255), 0.4 + 0.6 * tw_))


def icon(c, kind, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawCircle(0, 0, 92, P((255, 250, 240))); c.drawCircle(0, 0, 92, S(INK, 6))
    if kind == "map":
        cel(c, path([(0, -60), (40, -20), (0, 60), (-40, -20)], smooth=False), RED2, line=5); c.drawCircle(0, -24, 16, P((255, 255, 255)))
    elif kind == "fuel":
        cel(c, path([(-40, -56), (24, -56), (24, 60), (-40, 60)]), RED2, line=5); c.drawRect(skia.Rect.MakeLTRB(-28, -42, 12, -10), P((255, 255, 255)))
        h = skia.Path(); h.moveTo(24, -30); h.quadTo(56, -20, 50, 30); c.drawPath(h, S(INK, 7))
    elif kind == "wrench":
        c.rotate(-40); cel(c, path([(-14, -60), (14, -60), (14, 50), (-14, 50)]), (170, 176, 190), line=5)
        cel(c, ell(0, -66, 30, 26), (170, 176, 190), line=5); c.drawRect(skia.Rect.MakeLTRB(-10, -96, 10, -66), P((255, 250, 240)))
    elif kind == "eat":
        for fx in (-24, 24): c.drawLine(fx, -60, fx, 60, S((170, 176, 190), 12)); c.drawLine(fx, -60, fx, 60, S(INK, 3))
        c.drawPath(ell(-24, -40, 14, 26), P((170, 176, 190)))
    elif kind == "bed":
        cel(c, path([(-60, 0), (60, 0), (60, 30), (-60, 30)]), (40, 120, 200), line=5); cel(c, path([(-60, -40), (-26, -40), (-26, 0), (-60, 0)]), (255, 255, 255), line=5)
    c.restore()


# ---------------------------------------------------------------- shots
def S_i1(c, t, n):
    u = lt(t, "S_i1"); sunset(c, t, city=False, top=(40, 20, 90), mid=(240, 70, 120), bot=(255, 170, 110))
    speed_lines(c, 540, 900, (255, 240, 220), n=70, seed=n // 2, a=0.45)
    banner(c, t, [("HOW A TYRE COMPANY", 92), ("CREATED THE MICHELIN STAR", 92)], y=300)
    ks = 1.0 + 0.06 * math.sin(t * 5); kt = back(pr(t, TW("i1", "tyre", off=-0.2), 0.3)); sy = 880
    for i in range(10):
        a_ = i * math.tau / 10 + t * 1.5; star4(c, 540 + math.cos(a_) * 300, sy + math.sin(a_) * 300, 22 + 10 * math.sin(t * 6 + i), (255, 250, 210))
    if kt > 0: tyre(c, 540 - 900 * (1 - kt), sy, 260, t * 300 * (1 - kt))
    star5(c, 540, sy, 190 * ks, YEL, 8, rot=10 * math.sin(t * 2))
    kai(c, 860, 1360, 0.62, t, mth(t), "talk", "shock" if kt > 0 else "open", "up", look=(-0.6, -0.6), blink=blink(n))
    if kt > 0: caption(c, t, TW("i1", "tyre", off=-0.05), "", "A TYRE COMPANY?!", (255, 120, 120), y=1250, size=110)


def S_i2(c, t, n):
    u = lt(t, "S_i2"); sky(c, (255, 120, 160), (255, 190, 140), (255, 236, 170)); halftone(c, (0, 0, W, H), (255, 255, 255), 26, 8, 0.22)
    speed_lines(c, 540, 800, (255, 255, 255), n=60, seed=7, a=0.4)
    ta = TW("i2", "free", off=-0.15); tk = TW("i2", "Kai", off=-0.2)
    if t < ta:   # "to sell more tyres": a tower of tyres and coins raining
        for j in range(5):
            kk = back(pr(t, SHOT["S_i2"]["start"] + 0.08 * j, 0.25), 2.0)
            if kk > 0: tyre(c, 540 + (j % 2) * 30 - 15, 1010 - j * 120, 150 * kk, j * 20)
        for j in range(6):
            yy = ((t * 900 + j * 260) % 1300) + 300; coin(c, 150 + j * 150, yy, 46, t * 6 + j)
        caption(c, t, SHOT["S_i2"]["start"] + 0.1, "YEP.", "TO SELL MORE TYRES", YEL, y=420, size=120, t1=tk)
    kai(c, 860, 1350, 0.6, t, mth(t), "smirk" if u < 0.5 else "talk", "open", "smug", look=(-0.5, 0), blink=blink(n), arm="wave" if tk < t < ta else None)
    if tk < t < ta: c.save(); c.translate(-30, 60); nameplate(c, t, tk, "KAI", "BUSINESS DETECTIVE"); c.restore()
    k = ease(pr(t, ta, 0.25))
    if k > 0:   # the whole story in one picture: free tyre ad -> famous food award
        c.save(); c.translate(540, 820); c.scale(k, k)
        c.drawRoundRect(skia.Rect.MakeLTRB(-440, -300, 440, 300), 40, 40, P((40, 20, 70), 0.9)); c.drawRoundRect(skia.Rect.MakeLTRB(-440, -300, 440, 300), 40, 40, S(YEL, 8))
        red_book(c, -250, -20, 0.5, -6); outline_text(c, "FREE TYRE AD", -250, 230, 56, CREAM2, INK, 8)
        c.drawPath(path([(-90, -30), (50, -30), (50, -80), (120, 0), (50, 80), (50, 30), (-90, 30)]), P(YEL)); c.drawPath(path([(-90, -30), (50, -30), (50, -80), (120, 0), (50, 80), (50, 30), (-90, 30)]), S(INK, 5))
        for i in range(3): star5(c, 270 + (i - 1) * 95, -60 + (i == 1) * -30, 52, YEL, 5, rot=t * 40)
        plate(c, 270, 80, 0.45, t); outline_text(c, "FAMOUS FOOD AWARD", 270, 230, 48, CREAM2, INK, 8)
        c.restore()


def S_i3(c, t, n):
    u = lt(t, "S_i3"); sunset(c, t)
    title_card(c, t, SHOT["S_i3"]["start"], [("3 SNEAKY MOVES", 120)], bg=TEAL, y=420, rot=-4)
    for i, (lab, col) in enumerate((("FREE BOOK", CREAM2), ("A PRICE", CREAM2), ("SECRET EATERS", YEL))):
        k = back(pr(t, TW("i3", "three", off=0.1 + 0.25 * i), 0.3), 2.0)
        if k <= 0: continue
        y = 720 + i * 230; c.save(); c.translate(540, y); c.scale(k, k)
        c.drawRoundRect(skia.Rect.MakeLTRB(-420, -95, 420, 95), 30, 30, P((40, 20, 70), 0.88)); c.drawRoundRect(skia.Rect.MakeLTRB(-420, -95, 420, 95), 30, 30, S(col, 6))
        c.drawCircle(-330, 0, 62, P(col)); c.drawCircle(-330, 0, 62, S(INK, 6)); outline_text(c, str(i + 1), -330, 30, 90, PINK if i == 2 else INK, INK, 0.1, shadow=False)
        if i == 0: red_book(c, 290, 0, 0.3, -8)
        elif i == 1: price_tag(c, 290, 0, "1920", 0.6)
        else: magnifier(c, 290, -10, 0.5)
        outline_text(c, lab, -40, 26, 74, col, INK, 8)
        c.restore()
    kai(c, 880, 1340, 0.5, t, mth(t), "grin" if t > TW("i3", "genius", off=-0.1) else "talk", "open", "smug", blink=blink(n), arm="point")
    if t > TW("i3", "genius", off=-0.1): star4(c, 880, 1000, 50 * (0.6 + 0.4 * math.sin(t * 12)), (255, 255, 255))


def S_s1(c, t, n):
    u = lt(t, "S_s1"); countryside(c, t, pan=u * 140)
    old_car(c, 1300 - u * 210, 1420, 0.85, t, wheel_rot=-u * 300)
    title_card(c, t, SHOT["S_s1"]["start"] + 0.1, [("FRANCE · 1900", 120)], bg=(40, 90, 200), y=520, rot=-3)
    caption(c, t, TW("s1", "three", off=-0.1), "FEWER THAN", "3,000 CARS", YEL, y=820, size=150)


def S_s2(c, t, n):
    u = lt(t, "S_s2"); shop_bg(c, t)
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P((20, 10, 30), 0.35))
    tyre(c, 540, 1000, 240, math.sin(u * 2) * 3)
    for i in range(3):   # sparkles: still brand new
        k = (u * 1.5 + i * 0.33) % 1; star4(c, 400 + i * 150, 800 + i * 80, 40 * math.sin(k * math.pi), (255, 255, 255))
    for i in range(2):   # bored flies
        fx, fy = 540 + 280 * math.sin(u * 3 + i * 2), 640 + 80 * math.cos(u * 4 + i)
        c.drawCircle(fx, fy, 10, P(INK)); c.drawPath(ell(fx - 8, fy - 12, 10, 6), P((255, 255, 255), 0.8)); c.drawPath(ell(fx + 8, fy - 12, 10, 6), P((255, 255, 255), 0.8))
    caption(c, t, TW("s2", "barely", off=-0.1), "TYRES THAT BARELY MOVE", "BARELY WEAR OUT", (255, 120, 120), y=1420, size=120, t1=TW("s2", "Nobody", 1, off=-0.15))
    caption(c, t, TW("s2", "Nobody", 1, off=-0.1), "SO WHO BUYS NEW ONES?", "NOBODY.", (255, 120, 120), y=1420, size=170)


def S_a1(c, t, n):
    u = lt(t, "S_a1"); sky(c, (255, 200, 140), (255, 160, 110), (240, 100, 100)); halftone(c, (0, 1100, W, H), (120, 30, 40), 24, 8, 0.25)
    tb = TW("a1", "red", off=-0.25)
    gent(c, 290, 1000, 0.72, t, mth(t) if t < tb and (n // 6) % 2 else 0, 0, look=(0.6, 0)); gent(c, 800, 1030, 0.72, t, 0, 1, look=(-0.6, 0))
    caption(c, t, TW("a1", "Michelin", off=-0.1), "THE MICHELIN BROTHERS", "ANDRÉ & ÉDOUARD", CREAM2, y=1520, size=104)
    kb = back(pr(t, tb, 0.35), 2.2)
    if kb > 0: red_book(c, 540, 860, 0.85 * kb, -6 + 6 * math.sin(t * 3))
    title_card(c, t, SHOT["S_a1"]["start"], [("MOVE 1", 150)], sub="THE LITTLE RED BOOK", bg=PINK, y=480 if u > 0.8 else 900, rot=-4)


def S_a2(c, t, n):
    u = lt(t, "S_a2"); sky(c, (255, 236, 200), (255, 210, 170), (250, 160, 140))
    halftone(c, (0, 0, W, H), (240, 120, 120), 30, 9, 0.18)
    ko = ease(pr(t, L0("a2") - 0.1, 0.4)); kb = 1.0
    if kb > 0: red_book(c, 540, 1000, 1.1 * kb, -4 + 4 * ko, open_=ko)
    for i, (kind, w_) in enumerate((("map", "Maps"), ("fuel", "Petrol"), ("wrench", "flat"), ("eat", "eat"), ("bed", "sleep"))):
        ki = back(pr(t, TW("a2", w_, off=-0.1), 0.3))
        if ki > 0: icon(c, kind, 170 + i * 185, 1390 + (40 if i % 2 else 0), ki * 0.8)
    outline_text(c, "INSIDE THE FREE GUIDE", 540, 470, 90, YEL, INK, 10)


def S_a3(c, t, n):
    u = lt(t, "S_a3"); sky(c, (60, 30, 110), (140, 60, 160), (255, 120, 140)); speed_lines(c, 540, 1200, (255, 230, 255), n=60, seed=3, a=0.35)
    nb = int(3 + min(24, u * 16))
    for j, x in enumerate((300, 540, 780)): book_stack(c, x, 1650, max(1, nb - j * 3), 0.9)
    caption(c, t, SHOT["S_a3"]["start"] + 0.15, "NEARLY", "35,000 COPIES", YEL, y=520, size=140)
    tf_ = TW("a3", "free", off=-0.05)
    if t > tf_:
        k = back(pr(t, tf_, 0.18), 3.0); c.save(); c.translate(540, 900); c.rotate(-12); c.scale(k, k)
        c.drawRoundRect(skia.Rect.MakeLTRB(-330, -130, 330, 130), 30, 30, S(RED2, 22)); outline_text(c, "FREE!", 0, 70, 210, RED2, CREAM2, 10, shadow=False); c.restore()


def S_a4(c, t, n):
    u = lt(t, "S_a4"); sunset(c, t, sun=True, city=False, top=(255, 120, 80), mid=(255, 170, 110), bot=(255, 220, 160))
    hills(c, 1250, (200, 90, 110), 60, 8); c.drawRect(skia.Rect.MakeLTRB(0, 1380, W, H), P((80, 60, 70)))
    for i in range(8):
        x = (i * 180 - u * 1800) % (W + 180) - 90; c.drawRect(skia.Rect.MakeLTRB(x, 1600, x + 90, 1612), P((255, 230, 160)))
    flow_lines(c, (255, 255, 255), 30, seed=2, t=u, a=0.6)
    old_car(c, 540 + 10 * math.sin(u * 13), 1500, 1.0, t, wheel_rot=-u * 1100, body_col=(200, 40, 50))
    k1, k2 = pr(t, TW("a4", "wears", off=-0.1), 0.6), pr(t, TW("a4", "sells", off=-0.1), 0.3)
    tyre(c, 300, 560, 130, u * 200, worn=k1); outline_text(c, "WORN", 300, 760, 70, (255, 120, 120), INK, 9, a=min(1, k1 * 2))
    if k2 > 0: tyre(c, 780, 560, 130 * back(k2), -u * 200); outline_text(c, "NEW!", 780, 760, 70, YEL, INK, 9, a=k2)
    if k1 > 0: c.drawPath(path([(470, 540), (590, 540), (590, 520), (640, 560), (590, 600), (590, 580), (470, 580)]), P(CREAM2, min(1, k1 * 2)))
    caption(c, t, TW("a4", "drive", off=-0.1), "YOU", "DRIVE MORE", CREAM2, y=1080, size=120, t1=TW("a4", "wear", off=0.3))


def S_a4b(c, t, n):
    u = lt(t, "S_a4b"); shop_bg(c, t)
    c.drawRect(skia.Rect.MakeLTRB(0, 1180, W, 1260), P((150, 96, 60))); c.drawRect(skia.Rect.MakeLTRB(0, 1180, W, 1260), S(INK, 5))   # counter
    for j in range(4): tyre(c, 200 + j * 120, 1080 - (j % 2) * 20, 110, 0)
    price_tag(c, 330, 880, "NEW!", 0.8, -8)
    k = back(pr(t, TW("a4", "guess", off=0.2), 0.3), 2.2)
    if k > 0:
        gent(c, 760, 960, 0.5 * k, t, 0, 0); gent(c, 920, 990, 0.45 * k, t, 0, 1)
        caption(c, t, TW("a4", "guess", off=0.25), "GUESS WHO SELLS THEM?", "THE MICHELINS", YEL, y=560, size=120)
    kai(c, 170, 1340, 0.45, t, mth(t), "smirk" if mth(t) < 0.2 else "talk", "open", "smug", look=(0.6, 0), blink=blink(n))


def S_b1(c, t, n):
    u = lt(t, "S_b1"); shop_bg(c, t)
    door = ease(pr(t, TW("b1", "walks", off=-0.3), 0.5))
    c.drawRect(skia.Rect.MakeLTRB(60, 980, 420, 1600), P((255, 236, 180), 0.8 * door))
    gent(c, -200 + 600 * ease(pr(t, TW("b1", "walks", off=-0.2), 0.9)), 1160, 0.85, t, 0, 0, look=(0.7, 0))
    title_card(c, t, SHOT["S_b1"]["start"], [("MOVE 2", 150)], sub="AN OUCH MOMENT", bg=(240, 120, 30), y=520 if u > 0.9 else 900, rot=3)


def S_b2(c, t, n):
    u = lt(t, "S_b2"); shop_bg(c, t)
    z = 1.0 + 0.7 * ease(u / 1.6); c.save(); c.translate(540, 1000); c.scale(z, z); c.translate(-540 - 260 * ease(u / 1.6), -1000 - 160 * ease(u / 1.6))
    workbench(c, 540, 1100, 1.1, wobble=1.2 * math.sin(u * 6)); c.restore()
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P((20, 10, 20), 0.25 * ease(u)))


def S_b2b(c, t, n):
    u = lt(t, "S_b2b"); sky(c, (255, 255, 255), (255, 230, 230), (255, 200, 200))
    speed_lines(c, 540, 900, (40, 10, 20), n=110, seed=n // 2, a=0.85, wmax=12)
    gent(c, 540, 1000, 1.3, t, 0.9, 0, shock=True, sweat=True)
    caption(c, t, SHOT["S_b2b"]["start"] + 0.1, "HIS FREE GUIDES", "HOLDING UP A TABLE", RED2, y=1520, size=110)


def S_b3(c, t, n):
    u = lt(t, "S_b3"); sky(c, (120, 200, 255), (200, 235, 255), (255, 255, 255)); halftone(c, (0, 0, W, H), (90, 150, 220), 24, 7, 0.2)
    outline_text(c, "OUCH!", 540, 470, 200 * back(pr(u, 0, 0.2), 2.5), RED2, INK, 16)
    kw = pr(t, TW("b3", "worthless", off=-0.3), 0.3)
    red_book(c, 470, 820, 0.8 - 0.12 * kw, -10 + 30 * kw)
    if kw > 0:   # a big red cross through "FREE"
        c.save(); c.translate(470, 820); c.rotate(-8)
        outline_text(c, "FREE", 0, -250, 120, CREAM2, INK, 10)
        c.drawLine(-150, -330, 150, -230, S(RED2, 22 * kw)); c.drawLine(150, -330, -150, -230, S(RED2, 22 * kw)); c.restore()
        caption(c, t, TW("b3", "worthless", off=-0.25), "FREE STUFF CAN FEEL", "WORTHLESS", (120, 200, 255), y=1170, size=120)
    kai(c, 880, 1380, 0.5, t, max(mth(t), 0.6 if u < 0.5 else 0), "shout", "closed" if u < 0.4 else "open", "worried", sweat=True, tilt=-4)


def S_b3b(c, t, n):
    u = lt(t, "S_b3b"); sky(c, (255, 240, 200), (255, 220, 170), (255, 190, 140))
    red_book(c, 540, 950, 1.2, -6)
    price_tag(c, 760, 1180, "1920", 1.1 * back(pr(u, 0.05, 0.3), 2.2))
    caption(c, t, TW("b3", "respect", off=-0.1), "PEOPLE RESPECT", "WHAT THEY PAY FOR", YEL, y=1520, size=110)
    if u < 1.0: outline_text(c, "NOT FREE ANYMORE", 540, 500, 90, RED2, INK, 10, a=min(1, u * 4))


def S_c1(c, t, n):
    u = lt(t, "S_c1"); noir_bg(c, t)
    gl = 1.0 if 0 < t - TW("c1", "Secret") < 0.5 else 0.25
    inspector(c, 540, 950, 1.1, t, glint=gl)
    c.drawRect(skia.Rect.MakeLTRB(0, 1420, W, H), P((90, 40, 50))); c.drawRect(skia.Rect.MakeLTRB(0, 1420, W, 1440), P((255, 240, 220)))
    plate(c, 540, 1470, 0.9, t)
    caption(c, t, TW("c1", "Secret", off=-0.1), "SECRET", "INSPECTORS", YEL, y=600, size=150)
    title_card(c, t, SHOT["S_c1"]["start"], [("MOVE 3", 150)], sub="THE GENIUS ONE", bg=(120, 60, 200), y=900, rot=-3) if u < 1.1 else None


def S_c2(c, t, n):
    u = lt(t, "S_c2"); noir_bg(c, t)
    gl = 1.0 if 0 < t - TW("c2", "nobody", off=-0.1) < 0.5 else 0.25
    inspector(c, 540, 950, 1.1, t, glint=gl)
    c.drawRect(skia.Rect.MakeLTRB(0, 1420, W, H), P((90, 40, 50))); c.drawRect(skia.Rect.MakeLTRB(0, 1420, W, 1440), P((255, 240, 220)))
    plate(c, 540, 1470, 0.9, t)
    caption(c, t, TW("c2", "normal", off=-0.15), "THEY EAT LIKE", "NORMAL CUSTOMERS", CREAM2, y=600, size=120, t1=TW("c2", "pay", off=-0.15))
    caption(c, t, TW("c2", "pay", off=-0.1), "THEY PAY", "THEIR OWN BILL", YEL, y=600, size=130, t1=TW("c2", "nobody", off=-0.15))
    caption(c, t, TW("c2", "nobody", off=-0.1), "AND NOBODY", "KNOWS THEIR FACES", (255, 140, 140), y=600, size=120)


def S_c3(c, t, n):
    u = lt(t, "S_c3"); night_bg(c, t)
    c.drawRect(skia.Rect.MakeLTRB(240, 980, 840, 1620), P((120, 50, 40))); c.drawRect(skia.Rect.MakeLTRB(240, 980, 840, 1620), S(INK, 6))
    c.drawRect(skia.Rect.MakeLTRB(330, 1100, 750, 1620), P((255, 220, 140))); c.drawRect(skia.Rect.MakeLTRB(330, 1100, 750, 1620), S(INK, 6))   # lit door
    for i in range(7): c.drawRect(skia.Rect.MakeLTRB(200 + i * 97, 900, 297 + i * 97, 990), P((230, 40, 50) if i % 2 else (255, 250, 240))); 
    c.drawRect(skia.Rect.MakeLTRB(200, 900, 880, 990), S(INK, 6))
    outline_text(c, "RESTAURANT", 540, 1070, 70, (255, 220, 140), INK, 8)
    ks = ease(pr(t, TW("c3", "star", off=-0.6), 0.6)); y = 300 + 560 * ks
    if ks > 0:
        speed_lines(c, 540, y, (255, 240, 180), n=50, seed=4, a=0.4 * ks)
        star5(c, 540, y, 120, YEL, 6, rot=u * 120 * (1 - ks))
    outline_text(c, "1926", 540, 560, 170, CREAM2, INK, 14, a=1.0)
    k3 = pr(t, TW("c3", "three", off=-0.1), 0.3)
    if k3 > 0:
        for i in range(3): star5(c, 540 + (i - 1) * 230, 780, 90 * back(pr(t, TW("c3", "three", off=-0.1 + 0.12 * i), 0.3), 2.2), YEL, 5)


def S_c4(c, t, n):
    u = lt(t, "S_c4"); sky(c, (255, 220, 120), (255, 180, 100), (250, 120, 100)); halftone(c, (0, 0, W, H), (255, 255, 255), 26, 8, 0.2)
    k2, k3 = pr(t, TW("c4", "two", off=-0.1), 0.3), pr(t, TW("c4", "Three", 1, off=-0.1) if True else 0, 0.3)
    stars = 2 if t < TW("c4", "Three", off=-0.1) else 3
    for i in range(stars): star5(c, 540 + (i - (stars - 1) / 2) * 260, 540, 110 * back(pr(t, L0("c4") - 0.05 if i < 2 else TW("c4", "Three", off=-0.1), 0.3), 2.2), YEL, 6)
    if t > TW("c4", "detour", off=-0.2): road_sign(c, 540, 900, "WORTH A DETOUR", 1.1 * back(pr(t, TW("c4", "detour", off=-0.2), 0.3)), (255, 236, 120))
    if t > TW("c4", "journey", off=-0.4): road_sign(c, 540, 1180, "SPECIAL JOURNEY", 1.1 * back(pr(t, TW("c4", "journey", off=-0.4), 0.3)), (255, 160, 120))


def S_c5(c, t, n):
    u = lt(t, "S_c5"); sunset(c, t, city=False, top=(80, 30, 120), mid=(255, 100, 120), bot=(255, 200, 130))
    c.drawPath(path([(0, 1300), (W, 1300), (W, H), (0, H)]), P((70, 40, 80)))
    c.drawPath(path([(500, 1300), (580, 1300), (900, H), (180, H)]), P((110, 80, 110)))   # a long road to the horizon
    for i in range(6):
        k = ((u * 1.6 + i / 6) % 1); y = 1300 + (H - 1300) * k ** 2; w_ = 6 + 30 * k
        c.drawRect(skia.Rect.MakeLTRB(540 - w_, y, 540 + w_, y + 10 + 40 * k), P((255, 230, 160)))
    zt = TW("c5", "whose", off=-0.2); zk = ease(pr(t, zt, 0.4))
    old_car(c, 540 - 120 * zk, 1380 + 300 * zk, 0.9 + 1.4 * zk, t, wheel_rot=-u * 900, body_col=(200, 40, 50))
    if zk > 0.5: outline_text(c, "WHOSE TYRES?", 540, 700, 140, YEL, INK, 14)
    caption(c, t, SHOT["S_c5"]["start"] + 0.2, "A SPECIAL JOURNEY", "= A LONG DRIVE", CREAM2, y=640, size=120, t1=zt)


def S_c5b(c, t, n):
    u = lt(t, "S_c5b"); sky(c, (255, 120, 160), (255, 190, 140), (255, 236, 170)); speed_lines(c, 540, 900, (255, 255, 255), 80, seed=11, a=0.5)
    outline_text(c, "CLEVER!", 540, 470, 190 * back(pr(u, 0, 0.25), 2.4), YEL, INK, 16)
    old_car(c, 470, 1120, 0.75, t, wheel_rot=-u * 600, body_col=(200, 40, 50))
    for i in range(3): star5(c, 360 + i * 180, 760, 60 * back(pr(u, 0.1 + 0.1 * i, 0.25), 2.2), YEL, 5)
    outline_text(c, "STARS = MORE DRIVING = MORE TYRES", 540, 620, 56, CREAM2, INK, 8)
    kai(c, 870, 1340, 0.45, t, mth(t), "grin", "happy", "smug", sparkle=True, blush=True)


def S_d1(c, t, n):
    u = lt(t, "S_d1"); night_bg(c, t)
    for i, x in enumerate((240, 540, 840)):
        y = 820 + 30 * math.sin(t * 2 + i); chef_hat(c, x, y + 260, 0.7); star5(c, x, y, 70, YEL, 5, rot=t * 30 + i * 20)
        speed_lines(c, x, y, (255, 240, 180), n=14, seed=i, a=0.25, r0=90, wmax=8)
    caption(c, t, TW("d1", "chase", off=-0.15), "CHEFS EVERYWHERE", "CHASE THE STARS", YEL, y=520, size=120, t1=TW("d1", "started", off=-0.2))
    caption(c, t, TW("d1", "started", off=-0.1), "IT STARTED AS", "A FREE TYRE AD", (255, 140, 140), y=520, size=130)
    tyre(c, 540, 1460, 140 * ease(pr(t, TW("d1", "ad", off=-0.3), 0.3)), t * 100)


def S_d2(c, t, n):
    u = lt(t, "S_d2"); sunset(c, t, city=True)
    kg = back(pr(t, TW("d2", "useful", off=-0.2), 0.3), 2.0); kb = back(pr(t, TW("d2", "buy", off=-0.4), 0.3), 2.0)
    if kg > 0: gift_box(c, 260, 900, 1.0 * kg); outline_text(c, "GIVE IT FREE", 260, 1120, 64, CREAM2, INK, 8, a=min(1, kg))
    if kb > 0:
        c.drawPath(path([(440, 870), (580, 870), (580, 830), (650, 900), (580, 970), (580, 930), (440, 930)]), P(YEL)); c.drawPath(path([(440, 870), (580, 870), (580, 830), (650, 900), (580, 970), (580, 930), (440, 930)]), S(INK, 5))
        shop_bag(c, 820, 900, 1.0 * kb); outline_text(c, "THEY COME BACK", 820, 1120, 58, (120, 240, 220), INK, 8, a=min(1, kb))
    caption(c, t, TW("d2", "Try", off=-0.1), "", "TRY THIS", YEL, y=520, size=150)
    kai(c, 540, 1360, 0.48, t, mth(t), "talk", "open", "neutral", blink=blink(n), arm="point")


def S_z1(c, t, n):
    u = lt(t, "S_z1"); sunset(c, t, top=(40, 20, 90), mid=(240, 70, 120), bot=(255, 170, 110))
    k1 = back(pr(t, SHOT["S_z1"]["start"] + 0.1, 0.3), 2.0); k2 = back(pr(t, TW("z1", "Send"), 0.3), 2.0); k3 = back(pr(t, L0("z2"), 0.3), 2.0)
    if k1 > 0: bookmark(c, 250, 820, 1.1 * k1); outline_text(c, "SAVE", 250, 1020, 80, YEL, INK, 9, a=min(1, k1))
    if k2 > 0: share_arrow(c, 560, 820, 1.0 * k2); outline_text(c, "SEND", 560, 1020, 80, (120, 240, 220), INK, 9, a=min(1, k2))
    if k3 > 0: bubble(c, 850, 800, 0.75 * k3, "?"); outline_text(c, "COMMENT", 850, 1020, 70, CREAM2, INK, 9, a=min(1, k3))
    caption(c, t, L0("z2") + 0.2, "", "WHICH COMPANY NEXT?", (120, 240, 220), y=480, size=110)
    kai(c, 540, 1340, 0.55, t, mth(t), "talk" if mth(t) > 0.1 else "smile", "open", "up", blink=blink(n), arm="wave")


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}
HOLD = 12   # drawings per second (anime on twos)


def _draw(sid, t, n):
    c = SURF.getCanvas(); c.clear(skia.Color(0, 0, 0)); c.save()
    for ti, kind in CUES:   # camera shake on slams / impacts
        if kind in ("slam", "impact", "stamp") and 0 <= t - ti < 0.25:
            k = 1 - (t - ti) / 0.25; c.translate(14 * k * math.sin(t * 90), 10 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])   # slow push-in on every shot (camera never sits still)
    z = 1.0 + 0.06 * u; c.translate(W / 2, H * 0.46); c.scale(z, z); c.translate(-W / 2, -H * 0.46)
    RENDER[sid](c, t, n); c.restore()
    return SURF.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255


def compose(n):
    tq = math.floor(n / FPS * HOLD) / HOLD; nq = int(tq * HOLD)
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= tq < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; img = _draw(sh["id"], tq, nq); flash = 0.0; dt = tq - sh["start"]
    if i > 0 and sh["trans"] == "flash" and dt < 0.17: flash = 0.85 * (1 - dt / 0.17)
    if i > 0 and sh["trans"] == "wipe" and dt < 0.34:   # diagonal colour-bar wipe, the 80s eyecatch way
        prev = _draw(SHOTS[i - 1]["id"], sh["start"] - 1e-3, nq); p = ease(dt / 0.34)
        m = ((_xx * 0.5 + _yy * 0.28) / (W * 0.5 + H * 0.28) < p * 1.25 - 0.12).astype(np.float32)[..., None]
        band = (np.abs((_xx * 0.5 + _yy * 0.28) / (W * 0.5 + H * 0.28) - (p * 1.25 - 0.12)) < 0.05)[..., None]
        img = img * m + prev * (1 - m); img = np.where(band, np.array((0.98, 0.28, 0.43), np.float32), img)
    return (finish(img, nq, flash) * 255 + 0.5).astype(np.uint8)
