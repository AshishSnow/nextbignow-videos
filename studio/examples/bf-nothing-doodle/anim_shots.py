# HOW IT WORKS — "They sold NOTHING for $5" (Black Friday stunts). DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = ["i1", "i2", "i3", "i4", "a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "c1", "c2", "c3", "c4", "c5", "c6", "t1", "t2", "d1", "z1"]
_TR = {"i2": "pop", "i4": "cut", "a1": "whip", "a3": "pop", "b1": "whip", "b3": "pop", "c1": "whip", "c3": "pop", "c4": "pop", "t1": "whip", "d1": "pop", "z1": "pop"}
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "nothing"), "boing"), (TW("i2", "Eleven"), "pop"), (TW("i2", "Black"), "stamp"),
        (TW("i3", "slashing"), "slide"), (TW("i4", "three"), "stamp"), (L0("a1"), "stamp"), (TW("a2", "raised"), "pop"), (TW("a2", "five"), "stamp"),
        (L0("a3"), "boing"), (TW("a4", "up"), "chaching"), (TW("a5", "joke"), "ding"), (L0("b1"), "stamp"), (TW("b1", "completely"), "whoosh"),
        (TW("b2", "poop"), "boing"), (TW("b3", "money"), "chaching"), (TW("b4", "sold"), "stamp"), (L0("c1"), "stamp"), (TW("c2", "nothing"), "pop"),
        (L0("c3"), "boing"), (TW("c4", "Seventy-one"), "chaching"), (TW("c5", "split"), "pop"), (TW("c6", "longbow"), "pop"), (TW("c6", "laser"), "pop"),
        (TW("t1", "sale"), "buzz"), (TW("t2", "everywhere"), "ding"), (TW("d1", "louder"), "tick"), (TW("d1", "talking"), "tick"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i1": "Would you pay $5 for absolutely nothing?", "i2": "11,000 people did. On Black Friday.",
        "a2": "Instead of a discount, they raised the price. By $5.", "b2": "In its place? A $6 box of actual bull poop.",
        "b4": "About 30,000 people bought one, and it sold out.", "c2": "Give us $5, get nothing back. That was the whole deal.",
        "c4": "The total? About $71,000. For nothing.", "c5": "And they didn't keep it. They split it between all 17 employees."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
BOX_L = {"a3", "c3"}; BILL_L = {"b3"}
GAMEBOX = PUR   # not black: keep clear of the real brand's black-box look


def spoken_words(t):
    cur = None
    for lid in _ORDER:
        if LINES[lid]["start"] - 0.05 <= t: cur = lid
    if cur is None: return []
    d = DISP.get(cur, _VL.get(cur, LINES[cur].get("text", ""))).split(); ts = _LW.get(cur, [])
    k = sum(1 for x in ts if x <= t + 0.04); K = max(1, len(ts))
    n = len(d) if t > LINES[cur]["end"] else max(1, math.ceil(k / K * len(d)))
    return d[:n]


def speaking(t, ids): return any(LINES[i]["start"] <= t <= LINES[i]["end"] + 0.05 for i in ids if i in LINES)


def mth(t, ids): return talk(t) / 3.0 if speaking(t, ids) else 0.0


def blink(t, seed=0): return (int(t * 12 + seed * 7) % 43) in (0, 1)


def base(c, tint=None, gy=1440):
    page(c, tint); ground(c, gy)


def title(c, s, x, y, size, col=INK, k=1.0, rot=-2, fnt=MARK_F):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); text(c, s, 0, 0, size, col, fnt, maxw=860); c.restore()


def slide_in(t, t0, d=0.45, frm=-700): return frm * (1 - eout(pr(t, t0, d)))


def stick(c, x, y, s=1.0, seed=0, col=BLU, t=0.0, wave=False):
    """tiny stick person (team / crowd)."""
    hy = y - 150 * s; ink(c, wellipse(x, hy, 26 * s, 26 * s, seed, 1), col, 6 * s)
    wline(c, [(x, hy + 26 * s), (x, y - 60 * s)], seed, 7 * s)
    for sx in (-1, 1): wline(c, [(x, y - 60 * s), (x + sx * 22 * s, y)], seed + sx, 7 * s)
    a = math.sin(t * 9 + seed) * 30 * s if wave else 0
    wline(c, [(x - 34 * s, y - 70 * s), (x, y - 100 * s), (x + 34 * s, y - 130 * s - a)], seed + 3, 7 * s)


# ---------------------------------------------------------------- hook
def S_i1(c, t, n):
    base(c)
    op = pr(t, TW("i1", "absolutely") - 0.1, 0.35)
    char(c, "box", 640, 1440, 1.1, t, 0, (-0.5, -0.3), "happy", "hips", blink=blink(t), col=ORG, label="$5\nDEAL", fg=INK, lid=op, empty=True)
    char(c, "bill", 250 + slide_in(t, 0.0, 0.6, -500), 1440, 0.72, t, 0, (1, -0.3), "shock" if t > TW("i1", "nothing") else "happy", "point", walk=t < 0.6, blink=False)
    tape(c, "$5 FOR... NOTHING?", 540, 600, 60, -3, pop_k(t, 0.05, 0.25), seed=3)
    scribble(c, 640, 1060, 200, 70, pr(t, TW("i1", "nothing"), 0.4), RED, 9, 4)
    if t > TW("i1", "nothing"): text(c, "EMPTY!", 900, 900, 54, RED, MARK_F, a=pr(t, TW("i1", "nothing"), 0.2))


def S_i2(c, t, n):
    base(c)
    k = pr(t, TW("i2", "Eleven") - 0.1, 1.2)
    for i in range(int(22 * k)):   # a crowd of tiny people walking up
        r, q = divmod(i, 11); x = 90 + q * 82 + (40 if r else 0); y = 1440 - r * 120
        stick(c, x, y, 0.78, i, (BLU, PNK, GRN, ORG, PUR)[i % 5], t, wave=True)
    title(c, "11,000+ PEOPLE", 540, 760, 104, INK, pop_k(t, TW("i2", "Eleven"), 0.3))
    stamp(c, "BLACK FRIDAY", 540, 960, 70, -6, stamp_k(t, TW("i2", "Black")), RED, 11)


def S_i3(c, t, n):
    base(c)
    tape(c, "YOU: THE STORE", 540, 560, 58, -3, pop_k(t, L0("i3"), 0.25), seed=7)
    store(c, 540, 1440, 640, 380, sign="YOUR STORE")
    sl = pr(t, TW("i3", "slashing") - 0.2, 0.4)
    for i, (x, y, r, w_) in enumerate(((210, 760, -12, "-50%"), (850, 800, 14, "-70%"), (520, 880, -4, "SALE!"))):
        stamp(c, w_, x, y, 64, r, stamp_k(t, TW("i3", "everybody") + i * 0.18), RED, 20 + i)
    if sl > 0:
        for i in range(3): wline(c, [(160 + i * 300, 1000), (300 + i * 300, 1100)], 30 + i, 12, RED, 1, sl)


def S_i4(c, t, n):
    base(c)
    char(c, "box", 540, 1440, 0.95, t, 0, (0, -0.4), "happy", "cheer", blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")
    stamp(c, "THE OPPOSITE", 540, 600, 76, -5, stamp_k(t, L0("i4") + 0.4), PUR, 13)
    for i, x in enumerate((240, 540, 840)):
        stamp(c, str(i + 1), x, 790, 90, (-8, 4, -5)[i], stamp_k(t, TW("i4", "three") + i * 0.16), (BLU, ORG, RED)[i], 14 + i)
    scribble(c, 840, 790, 90, 90, pr(t, TW("i4", "weirder"), 0.4), RED, 8, 5)


# ---------------------------------------------------------------- stunt one: raise the price
def S_a1(c, t, n):
    base(c)
    stamp(c, "STUNT 1", 540, 620, 120, -6, stamp_k(t, L0("a1")), BLU, 21)
    tape(c, "CARDS AGAINST HUMANITY", 540, 800, 50, 2, pop_k(t, TW("a1", "Cards") - 0.1, 0.25), seed=9)
    char(c, "box", 540, 1440, 0.95, t, 0, (0, -0.3), "happy", "wave", blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")


def S_a2(c, t, n):
    base(c)
    for i, (x, w_) in enumerate(((180, "-40%"), (900, "-60%"))): stamp(c, w_, x, 640 + i * 60, 56, (-10, 12)[i], 1.0, GREY, 40 + i)
    rz = pr(t, TW("a2", "raised"), 0.4)
    char(c, "tag", 540, 1440, 0.95, t, 0, (0, -0.4), "happy", "cheer" if rz > 0 else "hips", blink=blink(t), price="+$5" if t > TW("a2", "five") - 0.1 else "PRICE", col=YEL)
    if rz > 0: arrow(c, 820, 1300, 820, 900, 30, GRN, 12, 5, rz); title(c, "UP!", 860, 860, 90, GRN, pop_k(t, TW("a2", "raised") + 0.3, 0.3), 6)
    tape(c, "INSTEAD OF A DISCOUNT", 540, 560, 50, -3, pop_k(t, L0("a2"), 0.25), seed=12)


def S_a3(c, t, n):
    base(c, tint=YEL)
    sh = 6 * math.sin(t * 60) * (1 - pr(t, L0("a3"), 0.4))
    char(c, "box", 540 + sh, 1440, 1.2, t, mth(t, BOX_L), (0, -0.4), "shock", "shrug", blink=False, col=GAMEBOX, label="PARTY\nGAME")
    bubble(c, "We're charging people MORE... on Black Friday?!", 540, 680, pop_k(t, L0("a3"), 0.25), (-40, 260), 62, 760)


def S_a4(c, t, n):
    base(c)
    tape(c, "TERRIBLE IDEA?", 300, 560, 54, -4, pop_k(t, L0("a4"), 0.25), seed=13)
    k = pr(t, TW("a4", "But"), 1.0)
    pts = [(160, 1300), (330, 1250), (470, 1180), (620, 1010), (780, 820), (900, 700)]
    ink(c, wpoly([(140, 1320), (140, 650)], 50, 1.5, False), None, 8); ink(c, wpoly([(140, 1320), (940, 1320)], 51, 1.5, False), None, 8)
    if k > 0:
        m = max(2, int(len(pts) * k + 0.999)); wline(c, pts[:m], 52, 14, GRN, 1.4)
        if k >= 1: arrow(c, 780, 820, 920, 680, 0, GRN, 14, 53, 1.0, 46)
    text(c, "SALES", 220, 700, 46, INK, BLK_F)
    stamp(c, "SALES\nWENT UP", 680, 1180, 64, -8, stamp_k(t, TW("a4", "up")), DGRN, 14)


def S_a5(c, t, n):
    base(c, tint=PNK)
    char(c, "box", 330, 1440, 0.9, t, 0, (0.6, -0.3), "happy", "cheer", blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")
    char(c, "bill", 790, 1440, 0.75, t, 0, (-0.6, -0.3), "happy", "wave", blink=blink(t, 3))
    tape(c, "NOT A GAME...", 400, 580, 56, -3, pop_k(t, L0("a5"), 0.25), seed=15)
    tape(c, "...THE JOKE", 660, 700, 64, 3, pop_k(t, TW("a5", "joke") - 0.1, 0.25), seed=16)
    if t > TW("a5", "joke"): text(c, "HA HA HA", 560, 900, 70, ORG, MARK_F, a=pr(t, TW("a5", "joke"), 0.2))


# ---------------------------------------------------------------- stunt two: the poop box
def S_b1(c, t, n):
    base(c)
    stamp(c, "STUNT 2", 540, 620, 120, 5, stamp_k(t, L0("b1")), ORG, 25)
    out = pr(t, TW("b1", "pulled") - 0.1, 1.0)
    char(c, "box", 540 + 700 * ease(out), 1440, 0.9, t, 0, (1, 0), "happy", "wave", walk=out > 0, blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")
    tape(c, "OFF THE ONLINE STORE", 540, 800, 56, -2, pop_k(t, TW("b1", "completely") - 0.2, 0.25), seed=17)


def S_b2(c, t, n):
    base(c, tint=(180, 130, 90))
    k = pop_k(t, TW("b2", "place") - 0.1, 0.35)
    if k > 0: char(c, "box", 540, 1440, 1.0 * k, t, 0, (0, -0.3), "happy", "hips", blink=blink(t), col=(206, 160, 104), label="100%\nBULL POOP", fg=BROWN, lid=1.0, poop=True)
    tape(c, "IN ITS PLACE...", 540, 560, 56, -3, pop_k(t, L0("b2"), 0.25), seed=18)
    char(c, "tag", 860, 1440, 0.55, t, 0, (-0.5, -0.3), "happy", "hips", blink=blink(t, 2), price="$6")


def S_b3(c, t, n):
    base(c, tint=GRN)
    char(c, "bill", 380, 1440, 1.15, t, mth(t, BILL_L), (0.6, -0.3), "happy", "cheer", blink=blink(t))
    char(c, "box", 840, 1440, 0.5, t, 0, (-0.5, -0.3), "happy", "down", blink=blink(t, 3), col=(206, 160, 104), label="POOP", fg=BROWN, lid=1.0, poop=True)
    bubble(c, "Real poop? Shut up and take my money!", 520, 680, pop_k(t, L0("b3"), 0.25), (-120, 260), 64, 700)


def S_b4(c, t, n):
    base(c)
    k = pr(t, TW("b4", "thirty") - 0.2, 1.0)
    for i in range(int(12 * k)):
        r, q = divmod(i, 6); x = 140 + q * 160 + (80 if r else 0); y = 1440 - r * 170
        char(c, "box", x, y, 0.32, t, 0, (0, -0.3), "happy", "down", blink=blink(t, i), col=(206, 160, 104), label="POOP", fg=BROWN, shadow_w=0.6)
    title(c, "30,000 SOLD", 540, 700, 110, BROWN, pop_k(t, TW("b4", "thirty"), 0.3))
    stamp(c, "SOLD OUT", 540, 900, 96, -8, stamp_k(t, TW("b4", "sold")), RED, 19)


# ---------------------------------------------------------------- stunt three: nothing
def S_c1(c, t, n):
    base(c)
    stamp(c, "STUNT 3", 540, 620, 120, -4, stamp_k(t, L0("c1")), RED, 29)
    tape(c, "THE WEIRDEST ONE", 540, 790, 54, 3, pop_k(t, TW("c1", "weirdest") - 0.1, 0.25), seed=22)
    char(c, "box", 540, 1440, 0.95, t, 0, (0, -0.3), "neutral", "hips", blink=blink(t), col=WHITE, label="?", fg=INK)
    title(c, "???", 840, 1000, 110, PUR, pop_k(t, L0("c1") + 0.3, 0.3), 8)


def S_c2(c, t, n):
    base(c)
    tape(c, "GIVE US $5", 330, 580, 60, -4, pop_k(t, TW("c2", "Give") - 0.1, 0.25), seed=23)
    tape(c, "GET: NOTHING", 720, 700, 60, 3, pop_k(t, TW("c2", "nothing") - 0.1, 0.25), seed=24, col=PNK)
    char(c, "bill", 300, 1440, 0.8, t, 0, (1, -0.2), "happy", "point", blink=blink(t))
    char(c, "box", 760, 1440, 0.9, t, 0, (-0.6, -0.2), "happy", "hips", blink=blink(t, 3), col=WHITE, label="NOTHING", fg=INK, lid=pr(t, TW("c2", "nothing"), 0.4), empty=True)
    if t > TW("c2", "whole"): stamp(c, "THAT'S IT", 540, 930, 64, -6, stamp_k(t, TW("c2", "whole")), RED, 25)


def S_c3(c, t, n):
    base(c, tint=SKY)
    char(c, "box", 540, 1440, 1.25, t, mth(t, BOX_L), (0, -0.4), "happy", "shrug", blink=blink(t), col=WHITE, label="NOTHING", fg=INK, lid=1.0, empty=True)
    bubble(c, "Hi! I'm the product. There's absolutely nothing inside me.", 540, 640, pop_k(t, L0("c3"), 0.25), (-40, 230), 58, 740)
    scribble(c, 580, 905, 240, 70, pr(t, TW("c3", "nothing"), 0.4), RED, 8, 6)


def S_c4(c, t, n):
    base(c, tint=GRN)
    coin_rain(c, t, TW("c4", "Seventy-one") - 0.1, 16, 9, 1430)
    title(c, "$71,145", 540, 820, 170, DGRN, pop_k(t, TW("c4", "total") + 0.1, 0.3), -3, BLK_F)
    tape(c, "FOR NOTHING", 540, 960, 60, 3, pop_k(t, TW("c4", "nothing") - 0.1, 0.25), seed=26)
    char(c, "box", 540, 1440, 0.55, t, 0, (0, -0.4), "shock", "cheer", blink=False, col=WHITE, label="NOTHING", fg=INK, lid=1.0, empty=True)


def S_c5(c, t, n):
    base(c)
    tape(c, "SPLIT 17 WAYS", 540, 580, 60, -3, pop_k(t, TW("c5", "split") - 0.1, 0.25), seed=27)
    k = pr(t, TW("c5", "seventeen") - 0.2, 0.9)
    for i in range(int(17 * k + 0.5)):
        r, q = divmod(i, 9); x = 110 + q * 107 + (54 if r else 0); y = 1440 - r * 230
        stick(c, x, y, 0.9, i + 3, (BLU, PNK, GRN, ORG, PUR, TEAL)[i % 6], t, wave=True)
        c.save(); c.translate(x + 30, y - 200 - r * 0); c.rotate(-10); ink(c, wrrect(-26, -14, 26, 14, 4, i, 1), (140, 214, 140), 4); c.restore()
    title(c, "ALL 17 EMPLOYEES", 540, 760, 84, INK, pop_k(t, TW("c5", "employees") - 0.1, 0.3))


def S_c6(c, t, n):
    base(c, tint=YEL)
    stick(c, 540, 1440, 1.6, 7, TEAL, t, wave=True); tape(c, "EMPLOYEE PERKS", 540, 520, 46, 2, pop_k(t, L0("c6") - 0.1, 0.25), seed=35)
    k1 = pop_k(t, TW("c6", "longbow") - 0.15, 0.3)
    if k1 > 0: c.save(); c.translate(250, 1050); c.scale(k1, k1); longbow(c, 0, 0, 1.0); c.restore()
    tape(c, "A LONGBOW", 260, 700, 54, -4, k1, seed=28)
    k2 = pop_k(t, TW("c6", "laser") - 0.15, 0.3)
    if k2 > 0: c.save(); c.translate(800, 1080); c.scale(k2, k2); glasses_eye(c, 0, 0, 1.0, t=t); c.restore()
    tape(c, "LASER EYE SURGERY", 740, 840, 46, 3, k2, seed=29)


# ---------------------------------------------------------------- the trick + takeaway
def S_t1(c, t, n):
    base(c, tint=RED)
    tape(c, "THE TRICK", 540, 560, 64, -3, pop_k(t, L0("t1"), 0.25), seed=30)
    k = 0.34 + 0.66 * pr(t, TW("t1", "every") - 0.1, 0.6)
    for i, (x, rot) in enumerate(((190, -20), (540, 0), (880, 20))):
        if k * 3 > i:
            store(c, x, 1440, 300, 240, 60 + i)
            megaphone(c, x, 1050 - 40 * (i == 1), 0.6, -60 + rot, 70 + i, "SALE!", pr(t, TW("t1", "sale") - 0.2 + i * 0.05, 0.2) * (0.7 + 0.3 * math.sin(t * 20 + i)))
    if t > TW("t1", "sale"): text(c, "\"SALE!\" \"SALE!\"", 540, 820, 74, RED, MARK_F, a=0.85)


def S_t2(c, t, n):
    base(c, tint=YEL)
    for i, (x, y, r, h_) in enumerate(((240, 760, -10, "$5 FOR NOTHING?!"), (820, 700, 12, "GAME SELLS POOP"), (560, 640, -3, "WEIRDEST SALE"))):
        k = pop_k(t, TW("t2", "headlines") - 0.3 + i * 0.18, 0.3)
        if k > 0: c.save(); c.translate(x, y); c.scale(k * 0.62, k * 0.62); newspaper(c, 0, 0, 1.0, r, h_, 80 + i); c.restore()
    char(c, "box", 540, 1440, 0.85, t, 0, (0, -0.4), "happy", "cheer", blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")
    stamp(c, "HEADLINES", 540, 1010, 76, -6, stamp_k(t, TW("t2", "everywhere")), DGRN, 31)


def S_d1(c, t, n):
    base(c)
    tape(c, "TRY IT NEXT SALE", 540, 540, 58, -3, pop_k(t, L0("d1"), 0.25), seed=32)
    ks = [pr(t, TW("d1", w) - 0.05, 0.4) for w in ("louder", "talking")]
    checklist(c, 540, 620, ["Don't just yell louder", "Do the thing people can't stop talking about"], ks)
    char(c, "box", 790, 1440, 0.55, t, 0, (-0.5, -0.5), "happy", "cheer", blink=blink(t), col=GAMEBOX, label="PARTY\nGAME")


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "box", 320, 1440, 0.9, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t), col=WHITE, label="NOTHING", fg=INK, lid=1.0, empty=True)
    char(c, "bill", 790, 1440, 0.78, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3))
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=33)
        bubble(c, "the friend who lives for Black Friday", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 62, 700)
    else:
        title(c, "WOULD YOU HAVE PAID?", 540, 680, 92, RED, pop_k(t, L0("z2"), 0.3))
        tape(c, "COMMENT BELOW", 540, 840, 58, 3, pop_k(t, TW("z2", "Comment") - 0.1, 0.25), seed=34)
        arrow(c, 540, 910, 540, 1010, 30, INK, 9, 8, pr(t, TW("z2", "below"), 0.3))


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    global BOIL
    BOIL = int(t * 12)
    c = SURF.getCanvas(); c.clear(skia.Color(*PAPER)); c.save()
    for ti, kind in CUES:
        if kind in ("slam", "impact", "stamp") and 0 <= t - ti < 0.24:
            k = 1 - (t - ti) / 0.24; amp = 14 if kind != "stamp" else 7; c.translate(amp * k * math.sin(t * 90), amp * 0.8 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z = 1.0 + 0.03 * u; c.translate(W / 2, H * 0.55); c.scale(z, z); c.translate(-W / 2, -H * 0.55)
    RENDER[sid](c, t, n); c.restore()
    strip(c, spoken_words(t), True, 262, 50, t)
    return SURF.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[..., :3].astype(np.float32) / 255


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; img = _draw(sh["id"], t, n); dt = t - sh["start"]
    if i > 0 and sh["trans"] == "whip" and dt < 0.22:
        p = eout(dt / 0.22); prev = _draw(SHOTS[i - 1]["id"], sh["start"] - 1e-3, n)
        off = int(W * p); out = np.empty_like(img); out[:, :W - off] = prev[:, off:]; out[:, W - off:] = img[:, :off]
        kx = max(1, int(90 * (1 - abs(2 * p - 1)))); img = cv2.blur(out, (kx * 2 + 1, 1))
    if i > 0 and sh["trans"] == "pop" and dt < 0.14:
        z = 1.08 - 0.08 * eout(dt / 0.14); M = cv2.getRotationMatrix2D((540, 960), 0, z); img = cv2.warpAffine(img, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    return (finish(img, 0.0) * 255 + 0.5).astype(np.uint8)
