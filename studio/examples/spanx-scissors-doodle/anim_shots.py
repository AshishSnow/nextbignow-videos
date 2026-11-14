# REAL CASE STUDY — Spanx: scissors, $5,000 and a ladies'-room demo. DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = [k for k in LINES if k not in ("z2", "i4")]
_TR = {"i2": "pop", "a1": "whip", "a2": "pop", "a5": "pop", "b1": "whip", "b4": "pop", "c1": "whip", "d1": "whip", "d3": "pop", "e1": "whip",
       "f1": "whip", "f3": "pop", "t1": "cut", "g1": "pop", "z1": "pop"}
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "feet"), "boing"), (TW("i2", "snip"), "pop"), (TW("i2", "billionaire"), "chaching"), (TW("i4", "five"), "stamp"),
        (L0("a1"), "pop"), (L0("a2"), "boing"), (TW("a3", "white"), "pop"), (TW("a4", "scissors"), "tick"), (TW("a4", "feet"), "boing"),
        (L0("a5"), "pop"), (TW("a6", "exist"), "ding"), (L0("b1"), "stamp"), (TW("b2", "Five"), "chaching"), (TW("b3", "same"), "buzz"),
        (TW("b4", "two"), "stamp"), (TW("b4", "herself"), "tick"), (TW("b5", "seven"), "pop"), (L0("c1"), "stamp"), (TW("c1", "brushed"), "buzz"),
        (TW("c2", "drove"), "slide"), (TW("c3", "Still"), "buzz"), (TW("c3", "in"), "ding"), (L0("d1"), "stamp"), (TW("d2", "own"), "whoosh"),
        (TW("d3", "ladies'"), "boing"), (TW("d4", "seven"), "stamp"), (L0("e1"), "stamp"), (TW("e2", "friends"), "chaching"),
        (TW("e3", "registers"), "pop"), (TW("e4", "handwritten"), "pop"), (TW("e5", "favorite"), "ding"), (TW("e6", "four"), "chaching"),
        (TW("f1", "billionaire"), "stamp"), (TW("f2", "ten"), "chaching"), (TW("f3", "anywhere"), "whoosh"), (TW("t1", "showed"), "ding"),
        (TW("g1", "Show"), "tick"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i3": "You're betting $5,000 of savings with no business experience, and you could lose it all.", "i4": "Here's how she won anyway, in 5 bold moves.",
        "b2": "$5,000. That was everything.", "b5": "The lawyer only got $750, to finish it.",
        "c3": "Still no. But about 2 weeks later, one owner called her back. He was in.",
        "d2": "She paid for her own flight to Dallas, for a 10-minute meeting with Neiman Marcus.",
        "e6": "The first year brought in about $4 million.",
        "f2": "Years later, an investment firm bought a majority stake. She gave every employee $10,000."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
FAX_L = {"a2"}; SCI_L = {"a5"}


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


def person(c, x, y, s=1.0, seed=0, col=BLU, t=0.0, pose="stand", name=None, mood="neutral", look=(0, 0), hair="short"):
    """plain doodle person (no likeness): round head with dot eyes, stick body; name on a tape."""
    hy = y - 230 * s
    wline(c, [(x, hy + 50 * s), (x, y - 90 * s)], seed, 9 * s)
    for sx in (-1, 1): limb(c, x, y - 90 * s, x + sx * 34 * s, y, 6 * sx * s, 8, False, seed + sx, foot=True, s=s)
    arms = {"stand": ((-50, 80), (50, 80)), "up": ((-80, -80), (80, -80)), "head": ((-40, -110), (40, -110)), "hold": ((60, 20), (90, 10)),
            "wave": ((-50, 80), (90, -60 + 20 * math.sin(t * 9)))}[pose]
    for (dx, dy), sd in zip(arms, (1, 2)): limb(c, x, y - 160 * s, x + dx * s, y - 160 * s + dy * s, 14 * s, 8, True, seed + sd, s=s)
    if hair == "long": ink(c, wpoly([(x - 66 * s, hy - 20 * s), (x + 66 * s, hy - 20 * s), (x + 74 * s, hy + 110 * s), (x - 74 * s, hy + 110 * s)], seed + 9, 1.6, True, 40), col, 7 * s)
    ink(c, wellipse(x, hy, 52 * s, 56 * s, seed + 4, 1.5), (255, 224, 196), 8 * s)
    eyes(c, x + look[0] * 6 * s, hy - 6 * s, s * 0.5, look, blink(t, seed), 40, 22, mood, seed + 5)
    mouth(c, x, hy + 26 * s, s * 0.45, 0, mood, seed + 6)
    ink(c, wpoly([(x - 54 * s, hy - 20 * s), (x - 40 * s, hy - 60 * s), (x, hy - 64 * s), (x + 44 * s, hy - 56 * s), (x + 54 * s, hy - 24 * s), (x + 30 * s, hy - 44 * s), (x - 30 * s, hy - 44 * s)], seed + 7, 1.2, True, 30), col, 6 * s)
    if name: tape(c, name, x, y + 46, 34, (-3, 3)[seed % 2], 1.0, seed=seed)


# ---------------------------------------------------------------- hook
SARA = dict(col=(250, 200, 70), hair="long")


def sara(c, x, y, s, t, pose="stand", mood="neutral", look=(0, 0), name=None):
    person(c, x, y, s, 4, t=t, pose=pose, name=name, mood=mood, look=look, **SARA)


def S_i1(c, t, n):
    base(c, tint=PNK)
    cut = pr(t, TW("i1", "feet") - 0.1, 0.6)
    stockings(c, 380, 1100, 1.3, cut=cut)
    char(c, "scissors", 790, 1440, 1.0, t, 0, (-0.6, -0.3), "happy", "point", blink=blink(t), snip=0.5 + 0.5 * math.sin(t * 14) if 0 < cut < 1 else 0.2)
    tape(c, "WHY CUT THE FEET OFF?!", 540, 600, 56, -3, pop_k(t, 0.1, 0.25), seed=3)


def S_i2(c, t, n):
    base(c)
    char(c, "fax", 270, 1440, 0.8, t, 0, (0.6, -0.3), "happy", "down", blink=blink(t))
    arrow(c, 450, 1150, 640, 1150, -60, RED, 10, 5, pr(t, TW("i2", "turned") - 0.1, 0.4))
    k = pop_k(t, TW("i2", "billionaire") - 0.2, 0.35)
    if k > 0: c.save(); c.translate(820, 1440); c.scale(k, k); sara(c, 0, 0, 1.2, t, "up", "happy"); c.restore()
    if k > 0: c.save(); c.translate(820, 1000); c.scale(k, k); text(c, "$1,000,000,000", 0, 0, 58, DGRN, BLK_F); c.restore()
    tape(c, "ONE SNIP", 300, 640, 60, -5, pop_k(t, TW("i2", "snip") - 0.1, 0.25), seed=6)


def S_i3(c, t, n):
    base(c, tint=RED)
    sara(c, 540, 1440, 1.5, t, "head", "worried")
    for i, w_ in enumerate(("$5,000", "NO EXPERIENCE", "COULD LOSE IT")):
        stamp(c, w_, (230, 540, 850)[i], 640 + (i % 2) * 80, 56, (-8, 6, -4)[i], stamp_k(t, TW("i3", ("five", "experience", "lose")[i])), RED, 10 + i)
    title(c, "5 BOLD MOVES", 540, 920, 100, INK, pop_k(t, TW("i4", "five"), 0.3))


def S_a1(c, t, n):
    base(c)
    sara(c, 300, 1440, 1.4, t, "hold", "neutral", (1, 0), "SARA BLAKELY")
    char(c, "fax", 760, 1440, 0.75, t, 0, (-0.6, -0.3), "neutral", "down", blink=blink(t))
    tape(c, "7 YEARS: FAX MACHINES", 540, 600, 52, -3, pop_k(t, TW("a1", "seven") - 0.1, 0.25), seed=9)
    tape(c, "DOOR TO DOOR", 540, 720, 46, 3, pop_k(t, TW("a1", "door") - 0.1, 0.25), seed=10, col=YEL)


def S_a2(c, t, n):
    base(c, tint=YEL)
    char(c, "fax", 540, 1440, 1.3, t, mth(t, FAX_L), (0, -0.3), "worried", "shrug", blink=blink(t))
    bubble(c, "Seven years with me? Honestly, I'd have quit too.", 540, 650, pop_k(t, L0("a2"), 0.25), (-60, 230), 62, 740)


def S_a3(c, t, n):
    base(c, tint=SKY)
    pants(c, 330, 1180, 1.0)
    sara(c, 760, 1440, 1.3, t, "head", "worried", (-1, 0))
    tape(c, "WHITE PANTS", 330, 640, 56, -3, pop_k(t, TW("a3", "white") - 0.1, 0.25), seed=11)
    stamp(c, "NOT SMOOTH", 560, 820, 66, -6, stamp_k(t, TW("a3", "smooth")), RED, 12)


def S_a4(c, t, n):
    base(c)
    cut = pr(t, TW("a4", "feet") - 0.15, 0.7)
    stockings(c, 360, 1120, 1.3, cut=cut)
    char(c, "scissors", 800, 1440, 0.95, t, 0, (-0.6, -0.3), "happy", "point", blink=blink(t), snip=0.5 + 0.5 * math.sin(t * 16) if t > TW("a4", "scissors") else 0.1)
    tape(c, "SNIP", 360, 620, 70, -5, pop_k(t, TW("a4", "feet"), 0.25), seed=12, col=PNK)


def S_a5(c, t, n):
    base(c, tint=PNK)
    char(c, "scissors", 540, 1440, 1.35, t, mth(t, SCI_L), (0, -0.3), "happy", "hips", blink=blink(t), snip=0.5 + 0.5 * math.sin(t * 16))
    bubble(c, "Snip, snip. You're welcome.", 540, 640, pop_k(t, L0("a5"), 0.25), (-40, 200), 66, 700)


def S_a6(c, t, n):
    base(c)
    pants(c, 300, 1180, 0.85)
    sara(c, 770, 1440, 1.3, t, "up" if t > TW("a6", "exist") else "stand", "happy", (-1, 0))
    stamp(c, "IT WORKED", 540, 640, 84, -6, stamp_k(t, TW("a6", "worked")), DGRN, 13)
    title(c, "WHY DOESN'T THIS EXIST?", 540, 820, 70, INK, pop_k(t, TW("a6", "exist") - 0.2, 0.3))


# ---------------------------------------------------------------- move 1-2: secret + savings, the patent
def S_b1(c, t, n):
    base(c)
    stamp(c, "MOVE 1", 540, 620, 120, -6, stamp_k(t, L0("b1")), BLU, 21)
    sara(c, 540, 1440, 1.4, t, "hold", "happy", (0.5, 0))
    tape(c, "SECRET FOR A YEAR", 540, 800, 52, 2, pop_k(t, TW("b1", "secret") - 0.1, 0.25), seed=14)
    tape(c, "ALL-IN", 540, 920, 52, -3, pop_k(t, TW("b1", "savings") - 0.1, 0.25), seed=15, col=YEL)


def S_b2(c, t, n):
    base(c, tint=GRN)
    title(c, "$5,000", 540, 800, 170, DGRN, pop_k(t, TW("b2", "Five"), 0.3), -3, BLK_F)
    char(c, "bill", 540, 1440, 0.9, t, 0, (0, -0.4), "worried", "shrug", blink=blink(t))
    tape(c, "EVERYTHING", 540, 960, 56, 3, pop_k(t, TW("b2", "everything") - 0.1, 0.25), seed=15)


def S_b3(c, t, n):
    base(c)
    person(c, 300, 1440, 1.4, 8, GREY, t, "stand", "PATENT LAWYER", "neutral", (1, 0))
    bubble(c, "That'll be about $5,000.", 640, 760, pop_k(t, TW("b3", "quoted") - 0.1, 0.25), (-220, 260), 60, 600)
    stamp(c, "SAME AMOUNT", 700, 1060, 66, 8, stamp_k(t, TW("b3", "same")), RED, 16)


def S_b4(c, t, n):
    base(c, tint=YEL)
    stamp(c, "MOVE 2", 540, 600, 110, 5, stamp_k(t, TW("b4", "two")), ORG, 25)
    book(c, 300, 1100, 1.0)
    sara(c, 760, 1440, 1.3, t, "hold", "happy", (-1, 0))
    k = pr(t, TW("b4", "wrote") - 0.1, 1.2)
    if k > 0:
        c.save(); c.translate(560, 820); ink(c, wrrect(-90, -110, 90, 110, 8, 70, 1.4), WHITE, 7)
        for j in range(int(6 * k)): wline(c, [(-70, -70 + j * 28), (70 - (j % 2) * 30, -70 + j * 28)], 71 + j, 4, GREY)
        c.restore()


def S_b5(c, t, n):
    base(c)
    person(c, 300, 1440, 1.3, 8, GREY, t, "stand", "PATENT LAWYER", "happy", (1, 0))
    title(c, "$750", 680, 820, 150, DGRN, pop_k(t, TW("b5", "seven"), 0.3), -3, BLK_F)
    tape(c, "JUST TO FINISH IT", 680, 960, 48, 3, pop_k(t, TW("b5", "finish") - 0.1, 0.25), seed=17)
    strike(c, 560, 1060, 820, pr(t, TW("b5", "seven") + 0.3, 0.3)); text(c, "$5,000", 690, 1070, 60, GREY, BLK_F)


# ---------------------------------------------------------------- move 3: the factory
def S_c1(c, t, n):
    base(c, tint=(150, 150, 160))
    factory(c, 470, 1440, t, 0.95, run=False)
    for i in range(3):
        k = pop_k(t, TW("c1", "brushed") - 0.3 + i * 0.2, 0.25)
        if k > 0: c.save(); c.translate(230 + i * 300, 700 + (i % 2) * 70); c.rotate((-8, 5, -3)[i]); c.scale(k, k); ink(c, wrrect(-110, -70, 110, 70, 10, 90 + i, 2), WHITE, 8); text(c, "NO.", 0, 20, 64, RED, MARK_F); c.restore()


def S_c2(c, t, n):
    base(c, tint=SKY)
    u = eout(pr(t, TW("c2", "drove") - 0.2, 1.2))
    cx = -200 + 640 * u
    ink(c, wrrect(cx - 170, 1290, cx + 170, 1390, 40, 80, 2), RED, 9); ink(c, wrrect(cx - 100, 1220, cx + 90, 1300, 30, 81, 2), RED, 9)
    ink(c, wrrect(cx - 80, 1235, cx + 70, 1290, 10, 82, 1), SKY, 6)
    for wx in (cx - 100, cx + 100): ink(c, wellipse(wx, 1395, 40, 40, 83, 1.2), INK, 0)
    tape(c, "NORTH CAROLINA", 540, 600, 58, -3, pop_k(t, TW("c2", "Carolina") - 0.2, 0.25), seed=18)
    tape(c, "IN PERSON", 540, 720, 52, 3, pop_k(t, TW("c2", "person") - 0.1, 0.25), seed=19, col=YEL)
    if t > TW("c2", "old") - 0.3: char(c, "fax", 860, 1440, 0.5, t, 0, (-0.6, -0.4), "happy", "cheer", blink=blink(t))


def S_c3(c, t, n):
    base(c)
    yes = t > TW("c3", "called") - 0.1
    factory(c, 360, 1440, t, 0.8, run=yes)
    if not yes: stamp(c, "STILL NO", 540, 700, 80, -6, stamp_k(t, TW("c3", "Still")), RED, 20)
    else:
        tape(c, "2 WEEKS LATER...", 540, 600, 52, -3, pop_k(t, TW("c3", "weeks") - 0.2, 0.25), seed=20)
        stamp(c, "HE WAS IN", 540, 780, 84, 5, stamp_k(t, TW("c3", "in")), DGRN, 21)
    sara(c, 860, 1440, 1.1, t, "up" if yes else "head", "happy" if yes else "worried", (-1, 0))


# ---------------------------------------------------------------- move 4: the ladies' room
def S_d1(c, t, n):
    base(c)
    stamp(c, "MOVE 4", 540, 640, 120, 6, stamp_k(t, L0("d1")), PUR, 30)
    tape(c, "THE ONE PEOPLE STILL TALK ABOUT", 540, 820, 42, -2, pop_k(t, TW("d1", "talk") - 0.2, 0.25), seed=30)
    sara(c, 540, 1440, 1.3, t, "stand", "happy")


def S_d2(c, t, n):
    base(c, tint=SKY)
    u = pr(t, L0("d2"), 2.2)
    plane(c, 140 + 800 * u, 1000 - 200 * u, 0.9)
    tape(c, "DALLAS", 300, 600, 60, -4, pop_k(t, TW("d2", "Dallas") - 0.1, 0.25), seed=31)
    stamp(c, "10 MINUTES", 760, 700, 70, 6, stamp_k(t, TW("d2", "ten")), RED, 31)
    store(c, 540, 1440, 600, 300, 60, sign="NEIMAN MARCUS")


def S_d3(c, t, n):
    base(c, tint=PNK)
    walk = pr(t, TW("d3", "walked") - 0.1, 1.0)
    restroom_door(c, 820, 1440, 0.9)
    sara(c, 220 + 360 * ease(walk), 1440, 1.2, t, "wave", "happy", (1, 0))
    person(c, 120 + 330 * ease(walk), 1440, 1.2, 12, PUR, t, "stand", None, "neutral" if t < TW("d3", "after") else "shock", (1, 0), "long")
    tape(c, "THE BUYER", 300, 620, 50, -3, pop_k(t, L0("d3"), 0.25), seed=32)
    if t > TW("d3", "before") - 0.1:
        for i, (w_, col) in enumerate((("BEFORE", GREY), ("AFTER", GRN))): tape(c, w_, 380 + i * 320, 760, 52, (-4, 4)[i], pop_k(t, TW("d3", ("before", "after")[i]) - 0.1, 0.25), seed=33 + i, col=col)


def S_d4(c, t, n):
    base(c, tint=GRN)
    k = pr(t, TW("d4", "seven") - 0.3, 0.9)
    for i in range(int(7 * k + 0.5)):
        x = 130 + i * 136; store(c, x, 1440 - (i % 2) * 0, 120, 120, 90 + i)
    stamp(c, "7 STORES", 540, 760, 110, -6, stamp_k(t, TW("d4", "seven")), DGRN, 34)
    tape(c, "ORDER PLACED", 540, 930, 52, 3, pop_k(t, TW("d4", "result") - 0.1, 0.25), seed=35)


# ---------------------------------------------------------------- move 5: make it sell
def S_e1(c, t, n):
    base(c)
    stamp(c, "MOVE 5", 540, 640, 120, -4, stamp_k(t, L0("e1")), RED, 40)
    tape(c, "MAKE IT SELL", 540, 820, 56, 3, pop_k(t, TW("e1", "sells") - 0.2, 0.25), seed=40)
    register(c, 540, 1440, 1.0)


def S_e2(c, t, n):
    base(c)
    for i, (x, col) in enumerate(((230, PNK), (540, GRN), (850, ORG))):
        if t > TW("e2", "friends") - 0.2 + i * 0.15: person(c, x, 1440, 1.1, 20 + i, col, t, "wave", None, "happy", (0, 0), "long" if i != 1 else "short")
    tape(c, "PAID FRIENDS TO BUY IT", 540, 640, 50, -3, pop_k(t, TW("e2", "friends") - 0.1, 0.25), seed=41)
    stamp(c, "NO FLOP", 540, 820, 76, 5, stamp_k(t, TW("e2", "flop")), DGRN, 42)


def S_e3(c, t, n):
    base(c, tint=YEL)
    register(c, 720, 1440, 0.9)
    u = ease(pr(t, TW("e3", "moved") - 0.1, 0.9))
    c.save(); c.translate(160 + 400 * u, 1100 - 60 * math.sin(u * math.pi)); ink(c, wrrect(-60, -80, 60, 80, 10, 50, 1.4), PNK, 7)
    text(c, "SPANX", 0, 10, 28, WHITE, BLK_F); c.restore()
    sara(c, 260, 1440, 1.1, t, "hold", "happy", (1, 0))
    tape(c, "SNUCK IN", 300, 620, 56, -4, pop_k(t, TW("e3", "snuck") - 0.1, 0.25), seed=43)
    tape(c, "NEXT TO THE REGISTER", 640, 760, 46, 3, pop_k(t, TW("e3", "registers") - 0.2, 0.25), seed=44, col=YEL)


def S_e4(c, t, n):
    base(c, tint=PNK)
    k = pop_k(t, TW("e4", "sample") - 0.1, 0.35)
    if k > 0: c.save(); c.translate(540, 1000); c.scale(k, k); envelope(c, 0, 0, 1.2); c.restore()
    tape(c, "TO: OPRAH", 540, 640, 60, -3, pop_k(t, TW("e4", "Oprah") - 0.1, 0.25), seed=45)
    tape(c, "+ HANDWRITTEN NOTE", 540, 1260, 48, 3, pop_k(t, TW("e4", "handwritten") - 0.1, 0.25), seed=46, col=YEL)


def S_e5(c, t, n):
    base(c, tint=PNK)
    stamp(c, "FAVORITE THINGS", 540, 700, 80, -6, stamp_k(t, TW("e5", "favorite")), PUR, 47)
    tape(c, "NOVEMBER 2000", 540, 560, 52, 3, pop_k(t, TW("e5", "November") - 0.1, 0.25), seed=48)
    sara(c, 540, 1440, 1.3, t, "up" if t > TW("e5", "favorite") else "stand", "happy")


def S_e6(c, t, n):
    base(c, tint=GRN)
    pts = [(170, 1300), (330, 1290), (490, 1260), (650, 1150), (780, 980), (910, 820)]
    wline(c, [(150, 1340), (150, 760)], 50, 8); wline(c, [(150, 1340), (930, 1340)], 51, 8)
    k = pr(t, TW("e6", "first") - 0.2, 1.0); m = max(2, int(len(pts) * k + 0.999))
    if k > 0: wline(c, pts[:m], 52, 14, GRN, 1.4)
    title(c, "~$4 MILLION, YEAR ONE", 540, 830, 70, DGRN, pop_k(t, TW("e6", "four"), 0.3), -2, BLK_F)


# ---------------------------------------------------------------- payoff + lesson
def S_f1(c, t, n):
    base(c, tint=YEL)
    magazine(c, 540, 1020, 1.0, head="FORBES", line2="YOUNGEST SELF-MADE")
    stamp(c, "BILLIONAIRE", 540, 640, 90, -6, stamp_k(t, TW("f1", "billionaire")), DGRN, 48)
    char(c, "fax", 880, 1440, 0.45, t, 0, (-0.6, -0.5), "shock", "cheer", blink=False)


def S_f2(c, t, n):
    base(c)
    tape(c, "MAJORITY STAKE SOLD", 540, 600, 50, -3, pop_k(t, TW("f2", "majority") - 0.1, 0.25), seed=49)
    k = pr(t, TW("f2", "every") - 0.2, 0.8)
    for i in range(int(8 * k)):
        x = 130 + i * 116; person(c, x, 1440, 0.62, 30 + i, (BLU, PNK, GRN, ORG)[i % 4], t, "up", None, "happy")
    title(c, "$10,000 EACH", 540, 860, 110, DGRN, pop_k(t, TW("f2", "ten"), 0.3), -3, BLK_F)


def S_f3(c, t, n):
    base(c, tint=SKY)
    for i in range(2):
        k = pop_k(t, TW("f3", "first-class") - 0.1 + i * 0.2, 0.3)
        if k > 0: c.save(); c.translate(360 + i * 340, 900 + i * 60); c.scale(k, k); ticket(c, 0, 0, 1.0, (-8, 6)[i], 60 + i); c.restore()
    plane(c, 180 + 760 * pr(t, TW("f3", "anywhere") - 0.2, 1.5), 1250, 0.7, -10)
    tape(c, "ANYWHERE IN THE WORLD", 540, 620, 50, -3, pop_k(t, TW("f3", "anywhere") - 0.1, 0.25), seed=61)


def S_t1(c, t, n):
    base(c)
    for i, (w_, x, y) in enumerate((("FACTORY", 220, 760), ("BUYER", 540, 700), ("STORES", 860, 760))):
        k = pop_k(t, L0("t1") + 0.6 + i * 0.35, 0.25)
        if k > 0: tape(c, w_, x, y, 48, (-4, 3, -2)[i], k, seed=70 + i, col=GREY)
    sara(c, 540, 1440, 1.35, t, "up", "happy")
    stamp(c, "SHOWED UP", 540, 920, 84, -6, stamp_k(t, TW("t1", "showed")), RED, 71)


def S_g1(c, t, n):
    base(c)
    tape(c, "TRY IT NEXT TIME", 540, 540, 58, -3, pop_k(t, TW("g1", "Try") - 0.1, 0.25), seed=72)
    checklist(c, 540, 620, ["Ignored? Show up in person", "Let them SEE it work"], [pr(t, TW("g1", "Show") - 0.05, 0.4), pr(t, TW("g1", "see") - 0.05, 0.4)])
    char(c, "scissors", 820, 1440, 0.55, t, 0, (-0.5, -0.5), "happy", "cheer", blink=blink(t), snip=0.3)


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "fax", 300, 1440, 0.7, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t))
    char(c, "scissors", 800, 1440, 0.8, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3), snip=0.3)
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=33)
        bubble(c, "the friend who's sitting on a great idea", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 60, 700)
    else:
        title(c, "WOULD YOU DO THE BATHROOM DEMO?", 540, 680, 60, RED, pop_k(t, L0("z2"), 0.3))
        stamp(c, "YES", 360, 860, 90, -6, stamp_k(t, TW("z2", "YES")), DGRN, 80)
        stamp(c, "NO", 720, 860, 90, 6, stamp_k(t, TW("z2", "NO")), RED, 81)


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
