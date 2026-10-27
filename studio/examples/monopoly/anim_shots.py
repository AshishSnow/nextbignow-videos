# ================= shots: "Monopoly was invented to warn against monopolies" (type D origin twist) =================
# Sources: Smithsonian (Mary Pilon, Jan 2015); Wikipedia + Wikimedia Commons patent US 748,626 (5 Jan 1904); NPR (Feb 2015);
#          UK IPO blog (Dec 2023); Wikipedia Anti-Monopoly + Charles Darrow. Generic board only: invented street names, no colour bands,
#          no GO arrow, no mascot, no deed/chance cards, no real box art.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "And") - 0.2, "punch"), ("S2", T("i3", "Here's") - 0.2, "whip"),
    ("S3", T("a1", "Nineteen") - 0.2, "flash"), ("S4", T("a1", "A") - 0.15, "whip"),
    ("S6", T("a3", "Her") - 0.2, "whip"), ("S7", T("a4", "She") - 0.2, "punch"), ("S8", T("a5", "She") - 0.2, "focus"),
    ("S9", T("b1", "So") - 0.2, "flash"), ("S10", T("b2", "In") - 0.2, "whip"), ("S11", T("b3", "In") - 0.2, "whip"),
    ("S12", T("b4", "Guess") - 0.2, "zoom"), ("S13", T("b5", "The") - 0.15, "punch"), ("S14", T("c1", "And") - 0.2, "flash"),
    ("S15", T("c2", "For") - 0.2, "whip"), ("S16", T("c2", "In") - 0.15, "focus"), ("S17", T("c3", "In") - 0.2, "whip"),
    ("S18", T("c4", "He") - 0.2, "punch"), ("S19", T("c4", "And") - 0.15, "whip"), ("S20", T("c5", "Who") - 0.2, "focus"),
    ("S21", T("c6", "Two") - 0.2, "zoom"), ("S21b", T("c6", "Over") - 0.15, "punch"), ("S22", T("c7", "Darrow") - 0.2, "whip"),
    ("S23", T("d1", "And") - 0.2, "flash"), ("S24", T("d1", "That") - 0.15, "focus"), ("S25", T("d2", "In") - 0.2, "whip"),
    ("S26", T("d3", "Her") - 0.15, "punch"), ("S27", T("f1", "Her") - 0.2, "flash"), ("S28", T("f2", "A") - 0.2, "whip"),
    ("S29", T("f3", "Digging") - 0.2, "focus"), ("S29b", T("f3", "The") - 0.15, "punch"), ("S30", T("t1", "So") - 0.2, "flash"),
    ("S31", T("t2", "The") - 0.2, "whip"), ("S31b", T("t2", "Patents") - 0.15, "punch"), ("S32", T("e1", "Because") - 0.2, "focus"),
    ("S33", T("e2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
SRC_SM = "Source: Smithsonian Magazine (Jan 2015)"
LIZ_P = (130, 60, 180)


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def ui_word(f, lead, big, y, t, t0, col=INK, acc=RED_, size=170, out=None, shadow=0.0, lead_col=None, tail="", fp_big=None):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow, fp_big=fp_big)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def wui(f, lead, big, t, t0, out=None, col=YEL_, size=220, tail="", y=470):
    ui_word(f, lead, big, y, t, t0, col=col, size=size, shadow=0.45, lead_col=WHITE, out=out, tail=tail)


def iui(f, lead, big, t, t0, size=200, tail="", y=470, col=INK, acc=RED_):   # ink caption for cream / yellow sets
    ui_word(f, lead, big, y, t, t0, col=col, size=size, shadow=0.0, lead_col=INK, tail=tail, acc=acc)


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def src(f, text, t, t0, y=1452, size=21):
    if t >= t0: comp(f, chip(text, INK, WHITE, size), 540, y, op=clamp((t - t0) / 0.3))


def spot(f, x, y, rx, ry, amt=0.35):
    m = gcache(("spot", x, y, rx, ry), lambda: np.exp(-(((_xx - x) / rx) ** 2 + ((_yy - y) / ry) ** 2)).astype(np.float32)[..., None])
    f *= (1 - amt * 0.55 * (1 - m)); f += m * amt * 0.06


def rays(f, x, y, r, col, amt, t, nr=14):
    if amt <= 0.01: return
    ov = np.zeros((H, W), np.float32); a0 = t * 0.25
    for i in range(nr):
        a = a0 + i * 2 * math.pi / nr; da = math.pi / nr * 0.5
        pts = np.array([[x, y], [x + r * math.cos(a - da), y + r * math.sin(a - da)], [x + r * math.cos(a + da), y + r * math.sin(a + da)]], np.int32)
        cv2.fillPoly(ov, [pts], 1.0, cv2.LINE_AA)
    ov = cv2.GaussianBlur(ov, (0, 0), 6) * np.clip(1 - np.hypot(_xx - x, _yy - y) / r, 0, 1)
    f += ov[..., None] * np.array(C(col), np.float32) * amt


def pencil_el():
    def mk():
        im = Image.new("RGBA", (60, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([12, 40, 48, 250], fill=(255, 200, 40, 255), outline=(22, 22, 28, 255), width=4)
        d.polygon([(12, 250), (48, 250), (30, 296)], fill=(240, 210, 160, 255), outline=(22, 22, 28, 255))
        d.polygon([(24, 282), (36, 282), (30, 296)], fill=(22, 22, 28, 255))
        d.rectangle([12, 10, 48, 40], fill=(240, 120, 140, 255), outline=(22, 22, 28, 255), width=4)
        return el_from(im)
    return gcache("pencil", mk)


def paper_el(j):
    def mk():
        im = Image.new("RGBA", (360, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 359, 469], fill=(238, 230, 208, 255), outline=(150, 136, 110, 255), width=4)
        for k in range(9): d.line([(36, 60 + 42 * k), (324 - (k * 37 % 90), 60 + 42 * k)], fill=(150, 140, 120, 255), width=6)
        return el_from(im)
    return gcache(("paper", j), mk)


PAWN_COLS = [(232, 60, 40), (90, 120, 220), (255, 214, 60), (240, 140, 40), (160, 90, 200)]


# ---- the hook composition (frame 1 + loop-back): board, houses piled up, a red pawn hopping round, WARNING stamp ----
def hook_set(f, t, warn=True):
    bw = 720; cx, cy = 540, 1130
    rot_comp(f, board_el(bw), cx, cy, -4, 1.0, 1.0, 0.35)
    for j, (dx, dy) in enumerate(((-150, -150), (-80, -150), (-10, -150), (-150, -80), (-150, -10))):
        comp(f, house_el(66, WOOD), cx + dx, cy + dy - 5 * math.sin(t * 3 + j))
    comp(f, house_el(70, WOOD_D, hotel=True), cx + 100, cy + 130 - 5 * math.sin(t * 3 + 2))
    k = (t * 1.5) % 4; idx = int(k); pk = k - idx; lift = -70 * math.sin(math.pi * min(1, pk / 0.6))
    p0 = board_xy(cx, cy, bw, 1 + idx); p1 = board_xy(cx, cy, bw, 2 + idx); q = eio(min(1, pk / 0.6))
    comp(f, pawn_el(110), p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q + lift - 55)
    if warn: rot_comp(f, stamp_el("WARNING", RED_, 120), 560, 1130, -12, 1.0, 0.95, 0.0)


def shot_S0(t, n):
    f = stage("teal", (255, 214, 90), 540, 1120, 470)
    hook_set(f, t)
    wui(f, "Monopoly was invented to warn against", "MONOPOLIES?", t, -0.5, col=YEL_, size=170)
    return finish(cam(f, 1.0 + 0.012 * t, W / 2, 1100), n)


# ---- S1: she sold her patent for $500 ----
def shot_S1(t, n):
    f = stage("purple", (255, 200, 90), 540, 1060, 430); u = lt(t, "S1")
    lizzie(f, 240, 1500, 0.78, la=(30, 20), ra=(90, 40), mouth=talk(t), blink=blink_at(t, 2), brow="sad", look=(1, 0), expr="n" if talk(t) else "sad")
    tf = T("i2", "five") - 0.2; k = eo(clamp(u / 0.45))
    rot_comp(f, oldcheque_el("$500" if t >= tf else "$ ???", 540), 670, 1100 + 160 * (1 - k), 6 - 4 * k + 2 * math.sin(t * 2), 1.0 + (0.15 * math.exp(-(t - tf) * 6) if t >= tf else 0.0), k, 0.3)
    wui(f, "she sold her patent for just", "$500" if t >= tf else "$???", t, st_("S1") + 0.06, col=YEL_, size=260)
    return finish(f, n)


# ---- S2: here's how her game got flipped — the board spins upside down ----
def shot_S2(t, n):
    f = stage("orange", (255, 230, 140), 540, 1080, 450)
    tf = T("i3", "flipped") - 0.3; k = eio(clamp((t - tf) / 0.5))
    rot_comp(f, board_el(640), 540, 1130, 180 * k, 1.0 - 0.15 * math.sin(math.pi * k), 1.0, 0.4)
    wui(f, "here's how her game got", "FLIPPED", t, st_("S2") + 0.06, col=WHITE, size=250)
    return finish(f, n)


# ---- S3: 1904 — split-flap year board ----
def shot_S3(t, n):
    f = stage("sky", (255, 255, 255), 540, 1000, 420); u = lt(t, "S3")
    flapboard(f, 540, 980, "1904", t, st_("S3") + 0.1, cell=(150, 220))
    lizzie(f, 540, 1560, 0.6, la=(20, 10), ra=(20, 10), mouth=talk(t), blink=blink_at(t, 1), brow="up", look=(0, -1))
    return finish(cam(f, 1.0 + 0.01 * u, W / 2, 1000), n)


# ---- S4: a woman named Lizzie gets a patent (the real patent number on paper) ----
def shot_S4(t, n):
    f = stage("cream", (255, 214, 120), 540, 1050, 440)
    tp = T("a1", "patent") - 0.3; k = eo(clamp((t - st_("S4") - 0.2) / 0.5))
    rot_comp(f, patent_el(520), 660, 1150 + 500 * (1 - k), -4 + 6 * (1 - k), 1.0 + (0.05 * math.exp(-(t - tp) * 6) if t >= tp else 0), clamp(k * 3), 0.35)
    lizzie(f, 210, 1500, 0.7, la=(30, 20), ra=(110, 70) if t >= tp else (30, 20), mouth=talk(t), blink=blink_at(t, 3), brow="up", look=(1, -1))
    if t >= tp + 0.3: comp(f, chip("Lizzie Magie: US patent 748,626 (Jan 5, 1904)", INK, WHITE, 22), 540, 1468, op=clamp((t - tp - 0.3) / 0.3))
    if t < tp: iui(f, "a woman named", "LIZZIE", t, st_("S4") + 0.04, size=220)
    else: iui(f, "gets a patent for a", "BOARD GAME", t, tp, size=170)
    return finish(f, n)


# ---- S5: fewer than 1 in 100 patents went to women — a 10x10 grid with ONE lit ----
def shot_S5(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 430)
    to = T("a2", "one") - 0.2
    cents_grid(f, 540, 1120, 1, LIZ_P, cell=50, gap=9, k=1.0 if t >= to else 0.0)
    src(f, "Source: NPR (Feb 2015)", t, to + 0.3, y=1500)
    iui(f, "back then, women got fewer than", "1 IN 100", t, st_("S5") + 0.04, size=200, tail="US patents")
    return finish(f, n)


# ---- S6: square board, rent to pay, a corner that says GO TO JAIL ----
def shot_S6(t, n):
    f = stage("emerald", (255, 230, 150), 540, 1100, 470)
    bw = 740; cx, cy = 540, 1150
    comp(f, board_el(bw), cx, cy, scale=pin(t, st_("S6"), 0.35))
    tr = T("a3", "rent") - 0.15; tj = T("a3", "jail") - 0.45
    for j in range(4):
        tj_ = tr + 0.12 * j
        if t >= tj_: comp(f, coin_el(40), 450 + 60 * j, 1110 - 30 * eo(clamp((t - tj_) / 0.25)))
    if t >= tj:
        jx, jy = board_xy(cx, cy, bw, 10)
        cv2.circle(f, (int(jx), int(jy)), int(76 + 12 * math.sin(t * 9)), C(YEL_), 12, cv2.LINE_AA)
    if t < tr: wui(f, "her game has a", "SQUARE BOARD", t, st_("S6") + 0.06, col=YEL_, size=190)
    elif t < tj: wui(f, "and", "RENT TO PAY", t, tr, col=YEL_, size=200)
    else: wui(f, "and a corner that says", "GO TO JAIL", t, tj, col=YEL_, size=200)
    return finish(f, n)


# ---- S7: she calls it the Landlord's Game — and it has a message ----
def shot_S7(t, n):
    f = stage("pink", (255, 236, 160), 540, 1050, 440)
    comp(f, board_el(560, centre="THE LANDLORD'S GAME"), 650, 1160)
    tm = T("a4", "message") - 0.3
    lizzie(f, 200, 1500, 0.7, la=(30, 20), ra=(120, 60), mouth=talk(t), blink=blink_at(t, 4), brow="up", look=(1, -1), expr="smirk" if t >= tm else "n")
    if t >= tm: slam(f, sign_el("IT HAS A MESSAGE", YEL_, INK, 50, pole=False), 640, 820, -4, t, tm)
    wui(f, "she calls it", "THE LANDLORD'S GAME", t, st_("S7") + 0.04, col=WHITE, size=120)
    return finish(f, n)


# ---- S8: a few grab all the wealth at everyone else's expense — see-saw ----
def shot_S8(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 430)
    te = T("a5", "everyone") - 0.25
    tilt = 14 * eo(clamp((t - T("a5", "grab") + 0.2) / 0.6))
    a = math.radians(tilt); cxp, cyp = 540, 1200
    lx, ly = cxp - 360 * math.cos(a), cyp + 360 * math.sin(a); rx, ry = cxp + 360 * math.cos(a), cyp - 360 * math.sin(a)
    cv2.fillPoly(f, [np.array([[cxp - 80, 1360], [cxp + 80, 1360], [cxp, 1205]], np.int32)], C(INK), cv2.LINE_AA)
    cv2.line(f, (int(lx), int(ly)), (int(rx), int(ry)), C((140, 92, 50)), 26, cv2.LINE_AA)
    for i in range(6): comp(f, scale_el(cash_el(1), 0.5), lx + 70, ly - 30 - 30 * i)
    comp(f, pawn_el(80, PAWN_COLS[0]), lx + 70, ly - 260)
    for j in range(5):
        xx = rx - 260 + 55 * j; yy = ry + (rx - xx) * math.tan(a)
        comp(f, pawn_el(54, PAWN_COLS[1]), xx, yy - 50)
    if t < te: wui(f, "what happens when", "A FEW GRAB IT ALL", t, st_("S8") + 0.06, col=WHITE, size=150)
    else: wui(f, "at", "EVERYONE ELSE'S", t, te, col=YEL_, size=170, tail="expense")
    return finish(f, n)


BOOK_A = ("MONOPOLIST", "win by crushing", (200, 40, 50), "fist")
BOOK_B = ("ANTI-MONOPOLIST", "everyone rewarded", (30, 150, 90), "hands")


# ---- S9: so she writes two sets of rules ----
def shot_S9(t, n):
    f = stage("cream", (255, 200, 120), 540, 1080, 440)
    for i, bk in enumerate((BOOK_A, BOOK_B)):
        k = pin(t, st_("S9") + 0.25 + 0.2 * i, 0.35)
        if t >= st_("S9") + 0.25 + 0.2 * i: rot_comp(f, book_el(*bk, 340), 300 + 480 * i, 1150 + 8 * math.sin(t * 2 + i), (-5 if i == 0 else 5), k, 1.0, 0.35)
    iui(f, "so she writes", "2 SETS OF RULES", t, st_("S9") + 0.04, size=170)
    return finish(f, n)


# ---- S10: rule set 1: win by crushing everyone (red side) ----
def shot_S10(t, n):
    f = stage("red", (255, 170, 120), 540, 1060, 420)
    rot_comp(f, book_el(*BOOK_A, 280), 250, 1160, -5, 1.0, 1.0, 0.3)
    tc = T("b2", "crushing") - 0.25
    comp(f, pawn_el(130, PAWN_COLS[2]), 700, 1000 + 10 * math.sin(t * 6))
    for j in range(4):
        fall = eo(clamp((t - tc - 0.08 * j) / 0.3)); x = 560 + 95 * j
        rot_comp(f, pawn_el(72, PAWN_COLS[1]), x + 20 * fall, 1240 + 30 * fall, -80 * fall, 1.0, 1.0, 0.2)
    if t >= tc: slam(f, stamp_el("BANKRUPT", WHITE, 64), 700, 1400, -8, t, tc + 0.2)
    wui(f, "rule set 1: you win by", "CRUSHING", t, st_("S10") + 0.04, col=YEL_, size=230, tail="everyone else")
    return finish(f, n)


# ---- S11: rule set 2: when wealth is created, everyone is rewarded (green side) ----
def shot_S11(t, n):
    f = stage("emerald", (255, 236, 150), 540, 1060, 420)
    rot_comp(f, book_el(*BOOK_B, 280), 800, 1160, 5, 1.0, 1.0, 0.3)
    te = T("b3", "everyone") - 0.25
    for j in range(5):
        x = 180 + 100 * j; comp(f, pawn_el(72, PAWN_COLS[j]), x, 1260)
        if t >= te:
            yy = 920 + 280 * eo(clamp((t - te - 0.07 * j) / 0.45))
            comp(f, coin_el(30), x, min(yy, 1180))
    if t < te: wui(f, "rule set 2: when wealth is created…", "", t, st_("S11") + 0.04, col=YEL_, size=200)
    else: wui(f, "when wealth is created", "EVERYONE WINS", t, te, col=YEL_, size=170)
    return finish(f, n)


# ---- S12: guess which one people loved? ----
def shot_S12(t, n):
    f = stage("purple", (255, 200, 90), 540, 1060, 420)
    for i, bk in enumerate((BOOK_A, BOOK_B)):
        rot_comp(f, book_el(*bk, 260), 300 + 480 * i, 1060 + 10 * math.sin(t * 3 + i * 2), (-6 if i == 0 else 6) + 3 * math.sin(t * 4 + i), 1.0, 1.0, 0.35)
    guy(f, 540, 1560, 0.62, la=(30, 20), ra=(150, 150), mouth=talk(t), blink=blink_at(t, 2), brow="sus", look=((1 if math.sin(t * 3) > 0 else -1), -1), expr="sus")
    comp(f, ed_el("", "?", "", big_col=YEL_, big_size=200, shadow=0.4), 700, 1200 - 10 * math.sin(t * 5))
    wui(f, "guess which one people", "LOVED?", t, st_("S12") + 0.04, col=YEL_, size=240)
    return finish(f, n)


# ---- S13: the crushing one ----
def shot_S13(t, n):
    f = stage("red", (255, 220, 120), 540, 1080, 480); u = lt(t, "S13")
    rays(f, 540, 1130, 640, (255, 230, 150), 0.35, t)
    rot_comp(f, book_el(*BOOK_A, 380), 540, 1150, -3, pin(t, st_("S13") + 0.05, 0.3) * 1.05, 1.0, 0.45)
    rot_comp(f, book_el(*BOOK_B, 200), 860, 1380 + 300 * eo(clamp(u / 0.8)), 25 + 40 * u, 1.0, clamp(1 - u / 0.9), 0.2)
    wui(f, "", "THE CRUSHING ONE", t, st_("S13") + 0.04, col=YEL_, size=170)
    return finish(f, n)


# ---- S14: re-hook: and then, the game escaped — the board grows legs and runs off ----
def shot_S14(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 440)
    te = T("c1", "escaped") - 0.3; run = max(0.0, t - te)
    x = 540 + 330 * eio(clamp(run / 0.9)); y = 1080 - 18 * abs(math.sin(t * 14)) * (run > 0)
    op = clamp(1 - (run - 0.7) / 0.4) if run > 0.7 else 1.0
    g = f.copy()
    ph = math.sin(t * 16) * (run > 0)
    for side in (-1, 1):
        hx = x + side * 110; ex = hx + 50 * ph * side
        cv2.line(g, (int(hx), int(y + 170)), (int(ex), int(y + 340)), C(INK), 14, cv2.LINE_AA)
        cv2.ellipse(g, (int(ex + 16), int(y + 344)), (28, 12), 0, 0, 360, C(INK), -1, cv2.LINE_AA)
    rot_comp(g, board_el(380), x, y, -8 * (run > 0) + 4 * math.sin(t * 2), 1.0, 1.0, 0.35)
    if run > 0:
        for j in range(3): cv2.line(g, (int(x - 250 - 50 * j), int(y - 60 + 60 * j)), (int(x - 320 - 50 * j), int(y - 60 + 60 * j)), C(INK), 8, cv2.LINE_AA)
    f[:] = f * (1 - op) + g * op
    guy(f, 230, 1520, 0.6, la=(30, 20), ra=(130, 100), blink=blink_at(t, 2), brow="up", look=(1, -1), expr="wow" if run > 0 else "n")
    iui(f, "and then, the game", "ESCAPED", t, st_("S14") + 0.04, size=250)
    return finish(f, n)


# ---- S15: for decades people drew their own boards by hand — copies multiply ----
def shot_S15(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 440)
    for i in range(9):
        r_, c_ = divmod(i, 3); t0 = st_("S15") + 0.15 + 0.2 * i
        if t < t0: continue
        x = 250 + 290 * c_; y = 870 + 270 * r_
        rot_comp(f, board_el(250, hand=1.0, seed=i + 1, corners=("", "JAIL", "PARK", "")), x, y, (i * 37 % 11) - 5, pin(t, t0, 0.3), 1.0, 0.3)
    wui(f, "for decades, people drew their own", "BY HAND", t, st_("S15") + 0.06, col=YEL_, size=230)
    return finish(f, n)


# ---- S16: Atlantic City Quakers added their own street names ----
SEA_NAMES = ["SHORE ST", "BEACH AVE", "PIER PL", "OCEAN DR", "SALT RD", "DUNE DR", "SEA LN", "TIDE TER", "SAND ST"] * 4


def shot_S16(t, n):
    f = stage("teal", (255, 230, 150), 540, 1080, 450)
    comp(f, sign_el("ATLANTIC CITY", (240, 240, 230), NAVY_, 56, pole=False), 540, 760)
    bw = 620; comp(f, board_el(bw, hand=1.0, names=SEA_NAMES, seed=0, corners=("", "JAIL", "PARK", "")), 540, 1170)
    px, py = board_xy(540, 1170, bw, 1 + int(clamp((t - st_("S16")) / 2.0) * 8))
    rot_comp(f, pencil_el(), px + 40, py - 70, 30, 1.0, 1.0, 0.3)
    src(f, "Sources: Smithsonian (2015), NPR (2015)", t, st_("S16") + 0.8, y=1468)
    wui(f, "Atlantic City Quakers add their own", "STREET NAMES", t, st_("S16") + 0.06, col=YEL_, size=180)
    return finish(f, n)


# ---- S17: the 1930s: an out-of-work salesman named Charles Darrow learns it from a friend ----
def shot_S17(t, n):
    f = stage("cream", (230, 210, 170), 540, 1050, 440)
    tf = T("c3", "friend") - 0.35; k = eo(clamp((t - tf) / 0.5))
    guy(f, 330, 1500, 0.72, la=(20, 10), ra=(80, 40) if t >= tf else (20, 10), blink=blink_at(t, 1), brow="sad" if t < tf else "up",
        look=(1, 0), expr="sad" if t < tf else "wow"); hat(f, 330, 1500, 0.72)
    guy(f, 800, 1500, 0.62, la=(20, 10), ra=(20, 10), blink=blink_at(t, 3), look=(-1, 0), expr="smirk")
    if t >= tf: rot_comp(f, board_el(230, hand=1.0, seed=4, corners=("", "JAIL", "PARK", "")), 760 - 300 * k, 1080, -6, 1.0, 1.0, 0.3)
    else: comp(f, sign_el("OUT OF WORK", (210, 200, 180), INK, 44, pole=False), 330, 900)
    pass
    if t < tf: iui(f, "the 1930s: a salesman named", "DARROW", t, st_("S17") + 0.04, size=200)
    else: iui(f, "learns the game", "FROM A FRIEND", t, tf, size=180)
    return finish(f, n)


# ---- S18: he made his own board ----
def shot_S18(t, n):
    f = stage("orange", (255, 230, 150), 540, 1060, 440); u = lt(t, "S18")
    bw = 540; comp(f, board_el(bw, seed=7), 640, 1140)
    k = clamp(u / 1.2)
    for j in range(int(k * 8) + 1):
        x, y = board_xy(640, 1140, bw, 31 + j); cv2.circle(f, (int(x), int(y)), 10, C(RED_), -1, cv2.LINE_AA)
    px, py = board_xy(640, 1140, bw, 31 + int(k * 8))
    rot_comp(f, pencil_el(), px + 40, py - 80, 30, 1.0, 1.0, 0.3)
    guy(f, 190, 1500, 0.66, la=(20, 10), ra=(110, 60), mouth=talk(t), blink=blink_at(t, 2), look=(1, -1), expr="smirk"); hat(f, 190, 1500, 0.66)
    wui(f, "he made his", "OWN BOARD", t, st_("S18") + 0.06, col=WHITE, size=240)
    return finish(f, n)


# ---- S19: 1935: he sold it to Parker Brothers (generic factory, plain-text name) ----
def shot_S19(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 430)
    ts = T("c4", "sold") - 0.25
    cv2.rectangle(f, (560, 900), (940, 1360), C((200, 70, 60)), -1, cv2.LINE_AA)
    for j in range(3):
        tri = np.array([[560 + 127 * j, 900], [687 + 127 * j, 900], [687 + 127 * j, 820]], np.int32)
        cv2.fillPoly(f, [tri], C((170, 50, 44)), cv2.LINE_AA); cv2.polylines(f, [tri], True, C(INK), 6, cv2.LINE_AA)
    cv2.rectangle(f, (560, 900), (940, 1360), C(INK), 8, cv2.LINE_AA)
    for r_ in range(2):
        for c_ in range(3): cv2.rectangle(f, (600 + 115 * c_, 1040 + 130 * r_), (675 + 115 * c_, 1110 + 130 * r_), C((255, 230, 140)), -1)
    comp(f, sign_el("PARKER BROTHERS", WHITE, INK, 30, pole=False), 750, 960)
    k = eo(clamp((t - ts) / 0.6))
    guy(f, 250, 1500, 0.66, la=(20, 10), ra=(90, 30), mouth=talk(t), blink=blink_at(t, 5), brow="up", look=(1, 0), expr="smirk"); hat(f, 250, 1500, 0.66)
    if k < 1: rot_comp(f, board_el(200, seed=7), 380 + 330 * k, 1190 - 140 * math.sin(math.pi * k), 360 * k, 1.0 - 0.5 * k, 1.0, 0.3)
    flapboard(f, 750, 1450, "1935", t, st_("S19") + 0.1, cell=(66, 96))
    wui(f, "and he sold it to", "PARKER BROTHERS", t, st_("S19") + 0.06, col=WHITE, size=150)
    return finish(f, n)


# ---- S20: who sold it to the world as Darrow's invention — a vintage ad ----
def shot_S20(t, n):
    f = stage("pink", (255, 230, 160), 540, 1060, 440)
    rot_comp(f, poster_el([("NEW!", 54, False), ("The property", 44, True), ("trading game", 44, True), ("INVENTED BY", 38, False), ("C. DARROW", 66, False)], 500, 700, ring=False),
             540, 1150, -3 + 2 * math.sin(t * 2), pin(t, st_("S20") + 0.1, 0.35), 1.0, 0.4)
    ti = T("c5", "invention") - 0.3
    if t >= ti: slam(f, stamp_el("THE STORY", RED_, 60), 720, 1440, -10, t, ti)
    wui(f, "sold to the world as", "DARROW'S INVENTION", t, st_("S20") + 0.04, col=WHITE, size=130)
    return finish(f, n)


# ---- S21: 278,000 copies in year one ----
def shot_S21(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 430)
    k = clamp((t - st_("S21") - 0.1) / 1.3)
    for i in range(int(12 * k)):
        r_, c_ = divmod(i, 4); comp(f, gamebox_el(180, NAVY_, "GAME"), 270 + 180 * c_, 1430 - 92 * r_)
    odometer(f, 540, 900, "278,000", k, cell=(84, 130), col=YEL_)
    src(f, SRC_SM, t, st_("S21") + 0.5, y=1468)
    iui(f, "copies sold in", "YEAR ONE", t, st_("S21") + 0.04, size=190)
    return finish(f, n)


# ---- S21b: over 1.7 million in year two — bars ----
def shot_S21b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 430)
    bars(f, 360, 1330, 200, int(640 * 278 / 1750), (255, 214, 60), 1.0, "YEAR 1", "278K")
    bars(f, 720, 1330, 200, 640, (255, 120, 60), clamp((t - st_("S21b") - 0.1) / 0.9), "YEAR 2", "1.7M+")
    src(f, SRC_SM, t, st_("S21b") + 0.2, y=1468)
    wui(f, "year two:", "1.7 MILLION+", t, st_("S21b") + 0.04, col=YEL_, size=190)
    return finish(f, n)


# ---- S22: Darrow got rich ----
def shot_S22(t, n):
    f = stage("emerald", (255, 230, 120), 540, 1060, 440); u = lt(t, "S22")
    cash_pile(f, 690, 1420, 15, clamp(u / 1.0), 0.95)
    b = -8 * abs(math.sin(t * 8))
    guy(f, 290, 1500, 0.72, la=(150, 160 + 15 * math.sin(t * 10)), ra=(150, 160 - 15 * math.sin(t * 10)), mouth=2, blink=blink_at(t, 1), brow="up", bob=b)
    hat(f, 290, 1500 + b * 0.72, 0.72)
    wui(f, "", "DARROW GOT RICH", t, st_("S22") + 0.04, col=YEL_, size=170)
    return finish(f, n)


# ---- S23: re-hook: and Lizzie? — spotlight, alone ----
def shot_S23(t, n):
    f = stage("purple", None)
    spot(f, 540, 1250, 300, 520, 0.9)
    lizzie(f, 540, 1500, 0.8, la=(20, 10), ra=(20, 10), blink=blink_at(t, 2), brow="sad", look=(0, -1), expr="sad")
    wui(f, "and", "LIZZIE?", t, st_("S23") + 0.04, col=YEL_, size=260)
    return finish(f, n)


# ---- S24: that same year Parker Brothers bought her patent for $500 — cheque vs mountain of boxes ----
def shot_S24(t, n):
    f = stage("teal", (255, 230, 150), 540, 1080, 440)
    rows = [5, 4, 3, 2, 1]
    for r_, m in enumerate(rows):
        for c_ in range(m): comp(f, gamebox_el(108, NAVY_, "GAME"), 440 + 54 * r_ + 108 * c_, 1420 - 56 * r_)
    tf = T("d1", "five") - 0.3; k = eo(clamp((t - tf) / 0.4))
    rot_comp(f, scale_el(oldcheque_el("$500" if t >= tf else "$ ???", 700), 0.6), 290, 1250, -6, 0.6 + 0.4 * k, 0.4 + 0.6 * k, 0.3)
    src(f, SRC_SM, t, tf + 0.3, y=1468)
    wui(f, "same year, her patent sold for", "$500" if t >= tf else "$???", t, st_("S24") + 0.04, col=YEL_, size=260)
    return finish(f, n)


def census_rows(f, k_job, zero_t=None, t=0.0):
    comp(f, ed_el("OCCUPATION", "", "", lead_col=(110, 96, 80), lead_size=30), 340, 1090)
    txt = "MAKER OF GAMES"[: int(len("MAKER OF GAMES") * clamp(k_job))]
    if txt: comp(f, ed_el("", txt, "", big_col=(30, 40, 90), big_size=54, fp_big=F_ANTON, maxw=600), 560, 1150)
    comp(f, ed_el("INCOME", "", "", lead_col=(110, 96, 80), lead_size=30), 310, 1250)


# ---- S25: 1940 census: job = maker of games (typed in) ----
def shot_S25(t, n):
    f = stage("cream", (230, 214, 180), 540, 1060, 440)
    comp(f, census_el(660), 540, 1180)
    tj = T("d2", "maker") - 0.3
    census_rows(f, (t - tj) / 0.9)
    src(f, SRC_SM, t, tj + 0.4, y=1468)
    iui(f, "1940 census, her job:", "MAKER OF GAMES", t, st_("S25") + 0.04, size=150)
    return finish(f, n)


# ---- S26: her income? zero ----
def shot_S26(t, n):
    f = stage("red", (255, 200, 140), 540, 1060, 460)
    comp(f, census_el(660), 540, 1180)
    census_rows(f, 1.0)
    tz = T("d3", "Zero") - 0.25
    if t >= tz: slam(f, ed_el("", "0", "", big_col=RED_, big_size=180, fp_big=F_ANTON), 560, 1300, -6, t, tz)
    src(f, SRC_SM, t, st_("S26") + 0.1, y=1468)
    wui(f, "her income?", "ZERO" if t >= tz else "…", t, st_("S26") + 0.04, col=YEL_, size=260)
    return finish(f, n)


# ---- S27: her story only came back in the 1970s ----
def shot_S27(t, n):
    f = stage("orange", (255, 230, 150), 540, 1000, 420); u = lt(t, "S27")
    flapboard(f, 540, 1010, "1970s", t, st_("S27") + 0.15, cell=(130, 200))
    lizzie(f, 540, 1560, 0.5, la=(20, 10), ra=(20, 10), blink=blink_at(t, 2), brow="up", look=(0, -1), op=0.35 + 0.65 * clamp(u / 1.5))
    wui(f, "her story only came back in the", "1970s", t, st_("S27") + 0.06, col=WHITE, size=240)
    return finish(f, n)


# ---- S28: a professor made a game called Anti-Monopoly; Parker Brothers took him to court ----
def shot_S28(t, n):
    f = stage("sky", (255, 255, 255), 540, 1050, 430)
    tc = T("f2", "court") - 0.3
    courthouse(f, 690, 1060, t)
    guy(f, 250, 1500, 0.7, la=(20, 10), ra=(100, 50), mouth=talk(t), blink=blink_at(t, 1), brow="n" if t < tc else "sad", look=(1, -1), expr="n" if t < tc else "wow",
        hold=scale_el(gamebox_el(380, (30, 150, 90), "ANTI-MONOPOLY"), 1.0), hold_off=(150, -40))
    if t >= tc:
        k = clamp((t - tc) / 0.2); ang = -40 + 40 * eo(k) + (10 * math.sin((t - tc) * 18) * math.exp(-(t - tc) * 4) if k >= 1 else 0)
        cv2.rectangle(f, (600, 1380), (900, 1420), C(WOOD_D), -1, cv2.LINE_AA); cv2.rectangle(f, (600, 1380), (900, 1420), C(INK), 5, cv2.LINE_AA)
        rot_comp(f, gavel_el(300), 730, 1290, ang, 1.0, 1.0, 0.35)
    if t < tc: wui(f, "a professor makes a game called", "ANTI-MONOPOLY", t, st_("S28") + 0.06, col=YEL_, size=150)
    else: wui(f, "Parker Brothers take him to", "COURT", t, tc, col=YEL_, size=260)
    return finish(f, n)


def courthouse(f, cx, cy, t):
    """generic courthouse: pediment + 4 columns + steps"""
    w = 340
    tri = np.array([[cx - w / 2 - 20, cy - 150], [cx + w / 2 + 20, cy - 150], [cx, cy - 270]], np.int32)
    cv2.fillPoly(f, [tri], C((240, 236, 226)), cv2.LINE_AA); cv2.polylines(f, [tri], True, C(INK), 7, cv2.LINE_AA)
    cv2.rectangle(f, (int(cx - w / 2 - 10), int(cy - 150)), (int(cx + w / 2 + 10), int(cy - 115)), C((226, 220, 206)), -1)
    cv2.rectangle(f, (int(cx - w / 2 - 10), int(cy - 150)), (int(cx + w / 2 + 10), int(cy - 115)), C(INK), 6)
    for j in range(4):
        x = cx - w / 2 + 40 + j * (w - 80) / 3
        cv2.rectangle(f, (int(x - 24), int(cy - 115)), (int(x + 24), int(cy + 150)), C((246, 242, 232)), -1); cv2.rectangle(f, (int(x - 24), int(cy - 115)), (int(x + 24), int(cy + 150)), C(INK), 5)
    for k in range(3):
        cv2.rectangle(f, (int(cx - w / 2 - 20 - 15 * k), int(cy + 150 + 22 * k)), (int(cx + w / 2 + 20 + 15 * k), int(cy + 172 + 22 * k)), C((214, 206, 190)), -1)
        cv2.rectangle(f, (int(cx - w / 2 - 20 - 15 * k), int(cy + 150 + 22 * k)), (int(cx + w / 2 + 20 + 15 * k), int(cy + 172 + 22 * k)), C(INK), 4)
    comp(f, ed_el("", "COURT", "", big_col=INK, big_size=40), cx, cy - 185)


# ---- S29: digging for his defense, he found her old patent ----
def shot_S29(t, n):
    f = stage("purple", (255, 200, 100), 540, 1060, 440)
    tf = T("f3", "found") - 0.3
    for j in range(6):
        rot_comp(f, paper_el(j), 540 + 70 * math.sin(j * 2.3), 1200 + 8 * j, (j * 23 % 17) - 8, 1.0, 1.0, 0.25)
    if t >= tf:
        k = eo(clamp((t - tf) / 0.5)); rays(f, 540, 1150, 560, (255, 230, 150), 0.4 * k, t)
        rot_comp(f, patent_el(440), 540, 1200 - 100 * k, -3, 0.85 + 0.15 * k, 1.0, 0.4)
    mx = 540 + 220 * math.sin(t * 2.4) if t < tf else 690
    rot_comp(f, scale_el(magnifier_el(), 0.7), mx, 1060 + 60 * math.cos(t * 3), -20, 1.0, 1.0, 0.3)
    if t < tf: wui(f, "digging for his", "DEFENSE", t, st_("S29") + 0.06, col=WHITE, size=220)
    else: wui(f, "he found her", "OLD PATENT", t, tf, col=YEL_, size=220)
    return finish(f, n)


# ---- S29b: the fight lasted about ten years — calendar pages fly ----
def shot_S29b(t, n):
    f = stage("yellow", (255, 255, 255), 540, 1080, 430); u = lt(t, "S29b")
    for j in range(5):
        kk = (u * 1.4 + j * 0.2) % 1
        rot_comp(f, scale_el(calendar_el("YEAR", str(1974 + 2 * j)), 0.42), 540 + 420 * kk * (1 if j % 2 else -1), 1060 - 260 * kk, 200 * kk, 1.0, 1 - kk, 0.0)
    comp(f, calendar_el("YEAR", str(1974 + int(clamp(u / 1.6) * 9))), 540, 1150)
    rot_comp(f, gavel_el(220), 840, 1400, 10 * math.sin(t * 8), 1.0, 1.0, 0.3)
    src(f, "Sources: NPR (2015), Wikipedia: Anti-Monopoly", t, st_("S29b") + 0.3, y=1468)
    iui(f, "the fight lasted about", "10 YEARS", t, st_("S29b") + 0.04, size=240)
    return finish(f, n)


# ---- S30: twist: built to warn against monopolies… became the game of winning one ----
def shot_S30(t, n):
    f = stage("teal", (255, 214, 90), 540, 1120, 470)
    tw = T("t1", "became") - 0.25; k = eio(clamp((t - tw) / 0.5))
    comp(f, board_el(640), 540, 1150)
    if k < 0.5: rot_comp(f, stamp_el("WARNING", RED_, 110), 540, 1130, -12, 1.0 - k * 2 * 0.9, 1.0 - k * 2, 0.0)
    else:
        rays(f, 540, 1130, 520, (255, 230, 120), 0.5 * (k - 0.5) * 2, t)
        rot_comp(f, stamp_el("WINNER!", (20, 130, 70), 120), 540, 1180, 8, 0.1 + 0.9 * eback(clamp((k - 0.5) * 2)), 1.0, 0.0)
        comp(f, pawn_el(130, PAWN_COLS[2]), 540, 960 - 10 * abs(math.sin(t * 6)))
    if t < tw: wui(f, "a game built to warn against", "MONOPOLIES", t, st_("S30") + 0.06, col=WHITE, size=170)
    else: wui(f, "became the game of", "WINNING ONE", t, tw, col=YEL_, size=210)
    return finish(f, n)


# ---- S31: takeaway: a lone-genius story? check who came first ----
def shot_S31(t, n):
    f = stage("emerald", (255, 240, 150), 540, 1080, 440)
    tf = T("t2", "first") - 0.35
    rot_comp(f, poster_el([("THE", 40, False), ("LONE", 80, False), ("GENIUS", 80, False), ("did it", 46, True), ("all alone!", 46, True)], 400, 560, ring=False),
             660, 1110, 3, 1.0, 1.0, 0.35)
    guy(f, 220, 1500, 0.7, la=(30, 20), ra=(90, 40), mouth=talk(t), blink=blink_at(t, 4), brow="sus", look=(1, -1), expr="sus" if talk(t) == 0 else "n",
        hold=scale_el(magnifier_el(), 0.45), hold_off=(40, -40))
    if t >= tf: slam(f, stamp_el("WHO WAS FIRST?", RED_, 50), 660, 1390, -8, t, tf)
    if t < tf: wui(f, "the takeaway: a", "LONE GENIUS?", t, st_("S31") + 0.06, col=YEL_, size=200)
    else: wui(f, "check who came", "FIRST", t, tf, col=YEL_, size=260)
    return finish(f, n)


# ---- S31b: patents are public and free to search ----
def shot_S31b(t, n):
    f = stage("sky", (255, 255, 255), 540, 1080, 430); u = lt(t, "S31b")
    rot_comp(f, patent_el(360), 300, 1170, -5, 1.0, 1.0, 0.35)
    q = "landlord's game 1904"; kq = clamp((u - 0.2) / 1.2)
    cv2.rectangle(f, (540, 1000), (960, 1090), C(WHITE), -1, cv2.LINE_AA); cv2.rectangle(f, (540, 1000), (960, 1090), C(INK), 6, cv2.LINE_AA)
    comp(f, ed_el(q[: int(len(q) * kq)] or " ", "", "", lead_col=INK, lead_size=32), 750, 1045)
    tfr = T("t2", "free") - 0.3
    if t >= tfr: slam(f, stamp_el("FREE", (20, 130, 70), 90), 750, 1240, -8, t, tfr)
    wui(f, "patents are", "PUBLIC", t, st_("S31b") + 0.04, col=WHITE, size=240, tail="and free to search")
    return finish(f, n)


# ---- S32: loop back to the exact frame-1 composition: "don't play like this" ----
def shot_S32(t, n):
    f = stage("teal", (255, 214, 90), 540, 1120, 470)
    hook_set(f, t)
    td = T("e1", "don't") - 0.15
    if t >= td: wui(f, "her game had one message:", "DON'T PLAY LIKE THIS", t, td, col=YEL_, size=150)
    else: wui(f, "her game had", "ONE MESSAGE", t, st_("S32") + 0.06, col=WHITE, size=200)
    return finish(cam(f, 1.0 + 0.012 * (t - st_("S32")), W / 2, 1100), n)


# ---- S33: send it + brand sting ----
def shot_S33(t, n):
    f = stage("sky", (255, 214, 120), 540, 880, 420)
    vend = LINES["e2"]["end"] + 0.15
    if t < vend + 0.2:
        pr = t >= T("e2", "Send") + 0.3
        comp(f, scale_el(phone2_el("who REALLY invented Monopoly?", "watch before game night", pr), 0.82), 600, 950, scale=pin(t, st_("S33")))
        if pr and t < T("e2", "Send") + 0.75:
            rr = (t - T("e2", "Send") - 0.3) / 0.45
            cv2.circle(f, (600, 1220), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        guy(f, 250, 1485, 0.9, la=(18, 8), ra=(60, -20), mouth=talk(t), blink=t % 2.0 < 0.12, expr="smirk", brow="up",
            hold=pawn_el(90), hold_off=(10, -60))
        ui_word(f, "send to the friend who always", "WINS", 400, t, T("e2", "friend") - 0.1, col=WHITE, size=190, shadow=0.3)
    else:
        k = pin(t, vend + 0.2, 0.4)
        comp(f, logo_el(), 540, 840, scale=k * 1.08)
        comp(f, ed_el("follow for more business secrets", "", lead_col=WHITE, lead_size=42), 540, 1120, op=clamp((t - vend - 0.5) / 0.3))
        guy(f, 540, 1490, 0.62, la=(18, 8), ra=(150, 170 + 18 * math.sin(t * 12)), mouth=2, expr="n", brow="up")
    return finish(f, n)


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i2", "five") - 0.2, 0.3, 12), (T("i3", "flipped") - 0.1, 0.3, 12), (T("a1", "patent") - 0.1, 0.25, 10),
           (T("a3", "jail") - 0.45, 0.3, 12), (T("a4", "message") - 0.3, 0.3, 12), (T("b2", "crushing") - 0.05, 0.35, 16),
           (st_("S13") + 0.05, 0.35, 16), (T("c1", "escaped") - 0.3, 0.3, 12), (T("c5", "invention") - 0.3, 0.3, 12),
           (T("d1", "five") - 0.3, 0.35, 14), (T("d3", "Zero") - 0.25, 0.4, 18), (T("f2", "court") - 0.1, 0.35, 16),
           (T("f3", "found") - 0.3, 0.3, 10), (T("t1", "became") - 0.25, 0.35, 14), (T("t2", "first") - 0.35, 0.3, 12),
           (T("t2", "free") - 0.3, 0.25, 10)]


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
