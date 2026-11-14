# PROTEIN BOOM + RXBAR case study + how to start. DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = [k for k in LINES if k not in ("z2", "b5b")]
_TR = {"i2": "pop", "a1": "whip", "a4": "pop", "b1": "whip", "b8": "pop", "b10": "pop", "t1": "cut", "s1": "whip", "s3": "pop", "s5": "pop",
       "s6": "pop", "e1": "pop", "z1": "pop"}
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "protein?"), "boing"), (TW("i2", "Coffee,"), "pop"), (TW("i2", "sandwiches,"), "pop"), (TW("i2", "ice"), "pop"),
        (TW("i2", "small"), "ding"), (TW("i3", "Forty-four"), "stamp"), (TW("i3", "money?"), "chaching"), (TW("i4", "four"), "stamp"),
        (TW("a1", "Starbucks"), "pop"), (TW("a2", "Pockets."), "pop"), (TW("a2", "hundred"), "pop"), (TW("a3", "quadrupled"), "chaching"),
        (L0("a4"), "boing"), (L0("b1"), "whoosh"), (TW("b2", "ten"), "chaching"), (TW("b3", "thousand"), "pop"), (TW("b4", "skipped"), "buzz"),
        (TW("b4", "CrossFit"), "stamp"), (TW("b5b", "pretty."), "buzz"), (TW("b6", "simple"), "ding"), (TW("b7", "front"), "pop"), (TW("b7", "B.S."), "stamp"),
        (L0("b8"), "boing"), (TW("b9", "Wegmans"), "pop"), (TW("b9", "Whole"), "pop"), (TW("b10", "Six"), "chaching"), (TW("t1", "honest"), "ding"),
        (TW("s1", "Four"), "stamp"), (TW("s2", "runners,"), "pop"), (TW("s2", "nurses."), "pop"), (TW("s3", "legal."), "stamp"),
        (TW("s4", "commercial"), "pop"), (TW("s5", "ten"), "stamp"), (TW("s6", "listen."), "ding"), (TW("e1", "small"), "tick"),
        (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i3": "You're a home baker. 44% of Americans say they're trying to eat more protein. So who gets their money?", "a1": "First, the boom is real. In fall 2025, Starbucks rolled out protein cold foam and protein lattes.",
        "i4": "Here's one real story, then 4 steps to start your own.", "a2": "Subway launched Protein Pockets. Sweetgreen made a bowl with over 100 g of protein.",
        "a3": "Foods claiming high protein have quadrupled (4x) in just over 10 years.",
        "b1": "Now, the story. Back in 2012, two friends in Illinois started making protein bars in Peter's parents' kitchen.",
        "b2": "Their names? Peter Rahal and Jared Smith. And they started with just $10,000 between them.", "b3": "Peter's dad gave them a simple goal. Just sell 1,000 bars.",
        "b10": "Eventually, Kellogg came knocking with an offer. The price? $600 million.", "s1": "So how could you start your own protein product? 4 steps.",
        "s5": "Third, label it honestly. In the US, a serving needs about 10 g to be called high protein."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
TUB_L = {"a4"}; BAR_L = {"b8"}
BARLINES = ("SHORT", "INGREDIENT", "LIST")


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
def S_i1(c, t, n):
    base(c, tint=YEL)
    char(c, "tub", 540, 1440, 1.25, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t))
    tape(c, "WHY IS EVERYTHING PROTEIN?!", 540, 600, 52, -3, pop_k(t, 0.1, 0.25), seed=3)


def S_i2(c, t, n):
    base(c, tint=PNK)
    k1 = pop_k(t, TW("i2", "Coffee,") - 0.1, 0.3); k2 = pop_k(t, TW("i2", "sandwiches,") - 0.1, 0.3); k3 = pop_k(t, TW("i2", "ice") - 0.1, 0.3)
    if k1 > 0: char(c, "soda", 220, 1440, 0.62 * k1, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t), col=BROWN, label="LATTE")
    if k2 > 0: c.save(); c.translate(540, 1420); c.scale(k2, k2); pocket(c, 0, 0, 0.9); c.restore()
    if k3 > 0: c.save(); c.translate(860, 1440); c.scale(k3, k3); pint(c, 0, 0, 0.9); c.restore()
    for i, (w_, x) in enumerate((("+PROTEIN", 220), ("+PROTEIN", 540), ("+PROTEIN", 860))):
        tape(c, w_, x, 1000 + (i % 2) * 60, 36, (-5, 4, -3)[i], (k1, k2, k3)[i], seed=10 + i, col=YEL)
    stamp(c, "ROOM FOR SMALL MAKERS", 540, 660, 64, -6, stamp_k(t, TW("i2", "small")), DGRN, 11)


def S_i3(c, t, n):
    base(c, tint=GRN)
    k = pr(t, TW("i3", "Almost") - 0.1, 0.9)
    for i in range(int(10 * k + 0.5)):
        x = 110 + i * 96; col = ORG if i < 4 else GREY
        c.save(); c.translate(x, 1440); c.scale(0.55, 0.55); c.translate(-x, -1440)
        wline(c, [(x, 1440 - 90), (x, 1440 - 190)], i, 12); ink(c, wellipse(x, 1440 - 240, 40, 44, i, 1.2), col, 9)
        for sx in (-1, 1): wline(c, [(x, 1440 - 90), (x + sx * 30, 1440)], i + sx, 12)
        c.restore()
    title(c, "44% WANT MORE PROTEIN", 540, 760, 76, INK, pop_k(t, TW("i3", "Forty-four"), 0.3), -2, BLK_F)
    stamp(c, "WHO GETS THE $$$?", 540, 960, 66, 5, stamp_k(t, TW("i3", "money?")), RED, 12)


def S_i4(c, t, n):
    base(c)
    tape(c, "1 REAL STORY", 540, 640, 64, -3, pop_k(t, TW("i4", "real") - 0.1, 0.25), seed=13)
    tape(c, "+ 4 STEPS TO START", 540, 780, 58, 3, pop_k(t, TW("i4", "four") - 0.1, 0.25), seed=14, col=GRN)
    char(c, "pbar", 540, 1440, 0.9, t, 0, (0, -0.3), "happy", "wave", blink=blink(t), lines_=BARLINES)


# ---------------------------------------------------------------- the boom
def S_a1(c, t, n):
    base(c)
    stamp(c, "THE BOOM IS REAL", 540, 600, 80, -5, stamp_k(t, TW("a1", "real.")), RED, 20)
    char(c, "soda", 380, 1440, 1.0, t, 0, (0.5, -0.3), "happy", "hips", blink=blink(t), col=BROWN, label="LATTE")
    tape(c, "STARBUCKS · FALL 2025", 600, 780, 44, 3, pop_k(t, TW("a1", "Starbucks") - 0.1, 0.25), seed=21)
    tape(c, "PROTEIN COLD FOAM", 760, 1000, 40, -4, pop_k(t, TW("a1", "foam") - 0.1, 0.25), seed=22, col=YEL)


def S_a2(c, t, n):
    base(c)
    pocket(c, 290, 1420, 1.0); tape(c, "SUBWAY: PROTEIN POCKETS", 330, 900, 40, -4, pop_k(t, TW("a2", "Subway") - 0.1, 0.25), seed=23)
    k = pop_k(t, TW("a2", "Sweetgreen") - 0.1, 0.3)
    if k > 0: c.save(); c.translate(790, 1420); c.scale(k, k); bowl(c, 0, 0, 0.9); c.restore()
    tape(c, "SWEETGREEN: 106 g BOWL", 740, 1060, 40, 3, k, seed=24, col=GRN)


def S_a3(c, t, n):
    base(c, tint=GRN)
    k = pr(t, TW("a3", "quadrupled") - 0.3, 0.9)
    for i, (x, h_) in enumerate(((330, 140), (750, 560))):
        hh = h_ * (1 if i == 0 else ease(k)); col = GREY if i == 0 else GRN
        if hh > 2: ink(c, wpoly([(x - 110, 1440), (x - 110, 1440 - hh), (x + 110, 1440 - hh), (x + 110, 1440)], 30 + i, 2, True, 40), col, 9)
        text(c, ("2013", "2024")[i], x, 1500, 52, INK, BLK_F)
    title(c, "4x", 750, 820, 150, DGRN, pop_k(t, TW("a3", "quadrupled"), 0.3), -4, BLK_F)
    tape(c, "\"HIGH PROTEIN\" PRODUCTS", 540, 600, 50, -3, pop_k(t, L0("a3"), 0.25), seed=25)


def S_a4(c, t, n):
    base(c, tint=YEL)
    kettlebell(c, 200, 1440, 0.9)
    char(c, "tub", 560, 1440, 1.2, t, mth(t, TUB_L), (0, -0.3), "happy", "shrug", blink=blink(t))
    char(c, "soda", 880, 1440, 0.5, t, 0, (-0.5, -0.3), "happy", "wave", blink=blink(t, 3), col=BROWN, label="LATTE")
    bubble(c, "I used to only hang out at the gym. Now I'm in your latte.", 540, 650, pop_k(t, L0("a4"), 0.25), (0, 220), 60, 740)


# ---------------------------------------------------------------- case study: the bar
def S_b1(c, t, n):
    base(c, tint=SKY)
    tape(c, "THE STORY · 2012", 540, 580, 58, -3, pop_k(t, L0("b1"), 0.25), seed=30)
    ink(c, wpoly([(160, 1440), (160, 900), (540, 700), (920, 900), (920, 1440)], 31, 2, True, 60), (255, 236, 200), 9)
    ink(c, wrrect(450, 1260, 630, 1440, 8, 32, 1.2), BROWN, 7)
    person(c, 330, 1440, 1.0, 4, BLU, t, "hold", None, "happy", (1, 0))
    person(c, 750, 1440, 1.0, 5, ORG, t, "hold", None, "happy", (-1, 0))
    tape(c, "ILLINOIS · PARENTS' KITCHEN", 540, 1000, 40, 2, pop_k(t, TW("b1", "kitchen.") - 0.2, 0.25), seed=33, col=YEL)


def S_b2(c, t, n):
    base(c)
    person(c, 300, 1440, 1.3, 4, BLU, t, "stand", "PETER RAHAL", "happy", (1, 0))
    person(c, 780, 1440, 1.3, 5, ORG, t, "stand", "JARED SMITH", "happy", (-1, 0))
    title(c, "$10,000", 540, 720, 140, DGRN, pop_k(t, TW("b2", "ten"), 0.3), -3, BLK_F)
    tape(c, "STARTING MONEY", 540, 560, 52, -3, pop_k(t, TW("b2", "started") - 0.1, 0.25), seed=34)


def S_b3(c, t, n):
    base(c, tint=YEL)
    person(c, 260, 1440, 1.3, 8, GREY, t, "stand", "PETER'S DAD", "happy", (1, 0))
    bubble(c, "Just sell a thousand bars.", 640, 720, pop_k(t, TW("b3", "Just") - 0.1, 0.25), (-260, 280), 62, 600)
    title(c, "GOAL: 1,000", 660, 1120, 80, INK, pop_k(t, TW("b3", "thousand"), 0.3), 3, BLK_F)


def S_b4(c, t, n):
    base(c)
    gone = t > TW("b4", "skipped") - 0.1
    store(c, 290, 1440, 380, 300, 60, sign="GROCERY")
    if gone: stamp(c, "SKIP", 290, 1180, 80, -10, stamp_k(t, TW("b4", "skipped")), RED, 35)
    k = pop_k(t, TW("b4", "CrossFit") - 0.2, 0.3)
    if k > 0:
        c.save(); c.translate(790, 1440); c.scale(k, k); building(c, 0, 0, 300, 380, (255, 120, 80), 36, None, False); kettlebell(c, 0, -60, 0.6); c.restore()
        tape(c, "CROSSFIT GYMS · CHICAGO", 700, 920, 42, 3, k, seed=37, col=YEL)


def S_b5(c, t, n):
    base(c)
    char(c, "pbar", 300, 1440, 0.9, t, 0, (0.6, -0.3), "worried" if t > TW("b5b", "pretty.") else "happy", "shrug", blink=blink(t), col=(200, 200, 220), lines_=("CLIP-ART", "WORD", "ART"))
    k = pop_k(t, TW("b5", "PowerPoint,") - 0.2, 0.3)
    if k > 0:
        c.save(); c.translate(760, 980); c.scale(k, k); ink(c, wrrect(-200, -140, 200, 140, 8, 40, 1.6), WHITE, 8)
        c.drawRect(skia.Rect.MakeLTRB(-200, -140, 200, -100), P((200, 80, 40))); text(c, "SLIDE 1", 0, -110, 28, WHITE, BLK_F)
        text(c, "PROTEIN BAR!!!", 0, 10, 40, (0, 120, 255), "Kalam-Bold.ttf"); text(c, "best bar ever", 0, 70, 32, (255, 0, 160), "Kalam-Bold.ttf"); c.restore()
    stamp(c, "NOT PRETTY", 760, 1220, 70, 8, stamp_k(t, TW("b5b", "pretty.")), RED, 41)
    tape(c, "GYMS BOUGHT IN", 540, 600, 48, -3, pop_k(t, TW("b5", "Gyms") - 0.1, 0.25), seed=42, col=GRN)


def S_b6(c, t, n):
    base(c, tint=GRN)
    stall(c, 540, 1440, 1.0, sign="FREE SAMPLES")
    for i, (x, col) in enumerate(((180, PNK), (900, PUR))): person(c, x, 1440, 0.9, 50 + i, col, t, "wave", None, "happy", ((1, 0), (-1, 0))[i])
    title(c, "SHORT, SIMPLE INGREDIENTS", 540, 700, 66, DGRN, pop_k(t, TW("b6", "Short,") - 0.1, 0.3), -2, BLK_F)


def S_b7(c, t, n):
    base(c, tint=YEL)
    u = ease(pr(t, TW("b7", "front") - 0.3, 0.6))
    char(c, "pbar", 540, 1440, 1.25, t, 0, (0, -0.3), "happy", "hips", blink=blink(t), lines_=BARLINES if u > 0.5 else ("", "", ""))
    tape(c, "INGREDIENTS ON THE FRONT", 540, 600, 50, -3, pop_k(t, TW("b7", "front") - 0.1, 0.25), seed=43)
    stamp(c, "NO FANCY CLAIMS", 540, 760, 66, 5, stamp_k(t, TW("b7", "fancy")), RED, 44)


def S_b8(c, t, n):
    base(c, tint=PNK)
    char(c, "pbar", 540, 1440, 1.3, t, mth(t, BAR_L), (0, -0.3), "happy", "cheer", blink=blink(t), lines_=BARLINES)
    bubble(c, "My whole recipe fits right here on my face. People love that.", 540, 600, pop_k(t, L0("b8"), 0.25), (-40, 220), 58, 740)


def S_b9(c, t, n):
    base(c)
    for i, (x, sg) in enumerate(((290, "WEGMANS"), (790, "WHOLE FOODS"))):
        k = pop_k(t, TW("b9", ("Wegmans", "Whole")[i]) - 0.15, 0.3)
        if k > 0: c.save(); c.translate(x, 1440); c.scale(k, k); store(c, 0, 0, 420, 300, 70 + i, sign=sg); c.restore()
    tape(c, "THEN CAME...", 540, 620, 54, -3, pop_k(t, L0("b9"), 0.25), seed=45)
    stamp(c, "THE BIG GROCERS", 540, 800, 64, 5, stamp_k(t, TW("b9", "big")), DGRN, 46)


def S_b10(c, t, n):
    base(c, tint=GRN)
    coin_rain(c, t, TW("b10", "Six") - 0.1, 16, 9, 1430)
    tape(c, "KELLOGG · 2017", 540, 600, 60, -3, pop_k(t, TW("b10", "Kellogg") - 0.1, 0.25), seed=47)
    title(c, "$600 MILLION", 540, 820, 130, DGRN, pop_k(t, TW("b10", "Six"), 0.3), -3, BLK_F)
    char(c, "pbar", 540, 1440, 0.7, t, 0, (0, -0.4), "shock", "cheer", blink=False, lines_=BARLINES)


def S_t1(c, t, n):
    base(c)
    k = pop_k(t, TW("t1", "fancier") - 0.1, 0.25)
    if k > 0: tape(c, "FANCIER BAR", 300, 700, 52, -4, k, seed=48, col=GREY); strike(c, 150, 700, 450, pr(t, TW("t1", "fancier") + 0.2, 0.3))
    tape(c, "HONEST LABEL", 760, 760, 54, 3, pop_k(t, TW("t1", "honest") - 0.1, 0.25), seed=49, col=GRN)
    tape(c, "+ THE RIGHT CROWD FIRST", 540, 900, 50, -2, pop_k(t, TW("t1", "crowd") - 0.2, 0.25), seed=50, col=YEL)
    char(c, "pbar", 540, 1440, 0.8, t, 0, (0, -0.3), "happy", "hips", blink=blink(t), lines_=BARLINES)


# ---------------------------------------------------------------- how to start
def step_badge(c, t, t0, num, label, col):
    stamp(c, f"STEP {num}", 540, 590, 96, (-5, 4, -3, 5)[num - 1], stamp_k(t, t0), col, 60 + num)
    tape(c, label, 540, 760, 52, (3, -3, 2, -2)[num - 1], pop_k(t, t0 + 0.25, 0.25), seed=61 + num)


def S_s1(c, t, n):
    base(c, tint=YEL)
    title(c, "HOW YOU START", 540, 660, 100, INK, pop_k(t, L0("s1"), 0.3))
    for i, x in enumerate((210, 430, 650, 870)): stamp(c, str(i + 1), x, 860, 80, (-8, 4, -5, 6)[i], stamp_k(t, TW("s1", "Four") + i * 0.12), (BLU, ORG, RED, DGRN)[i], 70 + i)
    char(c, "tub", 540, 1440, 0.75, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t))


def S_s2(c, t, n):
    base(c)
    step_badge(c, t, L0("s2"), 1, "ONE PRODUCT, ONE CROWD", BLU)
    k1 = pop_k(t, TW("s2", "cookie") - 0.1, 0.3); k2 = pop_k(t, TW("s2", "nurses.") - 0.2, 0.3)
    if k1 > 0:
        c.save(); c.translate(300, 1080); c.scale(k1, k1); cookie(c, 0, 0, 1.0); c.restore()
        person(c, 300, 1440, 0.9, 80, ORG, t, "wave", "RUNNERS", "happy")
    if k2 > 0:
        c.save(); c.translate(780, 1100); c.scale(k2, k2); ink(c, wrrect(-110, -50, 110, 50, 20, 81, 1.4), (255, 200, 120), 8); c.restore()
        person(c, 780, 1440, 0.9, 82, TEAL, t, "stand", "NIGHT NURSES", "happy")


def S_s3(c, t, n):
    base(c)
    step_badge(c, t, TW("s3", "Make"), 2, "MAKE IT LEGAL", ORG)
    k = pop_k(t, TW("s3", "Rules") - 0.1, 0.3)
    if k > 0:
        c.save(); c.translate(540, 1150); c.scale(k, k); ink(c, wrrect(-300, -200, 300, 200, 10, 90, 2), WHITE, 9)
        text(c, "HOMEMADE FOOD RULES", 0, -120, 40, INK, BLK_F)
        for j, w_ in enumerate(("STATE A: OK", "STATE B: LIMITS", "STATE C: NO")): text(c, w_, 0, -40 + j * 70, 40, (DGRN, ORG, RED)[j], "Kalam-Bold.ttf")
        c.restore()
    stamp(c, "CHECK YOURS", 800, 1380, 56, 8, stamp_k(t, TW("s3", "yours.")), RED, 91)


def S_s4(c, t, n):
    base(c, tint=SKY)
    building(c, 540, 1440, 520, 420, (230, 230, 236), 92, None, False)
    tape(c, "COMMERCIAL KITCHEN", 540, 990, 50, -3, pop_k(t, TW("s4", "commercial") - 0.1, 0.25), seed=93)
    tape(c, "RENT BY THE HOUR", 540, 640, 50, 3, pop_k(t, TW("s4", "Rent") - 0.1, 0.25), seed=94, col=YEL)
    char(c, "tub", 860, 1440, 0.5, t, 0, (-0.5, -0.3), "happy", "wave", blink=blink(t))


def S_s5(c, t, n):
    base(c)
    step_badge(c, t, TW("s5", "label"), 3, "LABEL IT HONESTLY", RED)
    nutrition(c, 400, 1160, 0.85, hl=pr(t, TW("s5", "ten"), 0.5))
    title(c, "~10 g", 820, 1080, 110, DGRN, pop_k(t, TW("s5", "ten"), 0.3), -4, BLK_F)
    tape(c, "= \"HIGH PROTEIN\"", 820, 1200, 40, 3, pop_k(t, TW("s5", "high") - 0.1, 0.25), seed=95, col=GRN)


def S_s6(c, t, n):
    base(c, tint=GRN)
    step_badge(c, t, TW("s6", "sell"), 4, "SELL WHERE THEY ARE", DGRN)
    stall(c, 540, 1440, 0.85, sign="TRY ONE!")
    for i, (x, col) in enumerate(((170, PNK), (910, ORG))): person(c, x, 1440, 0.85, 100 + i, col, t, "wave", None, "happy", ((1, 0), (-1, 0))[i])
    if t > TW("s6", "listen.") - 0.2: bubble(c, "Needs more chocolate!", 300, 1000, pop_k(t, TW("s6", "listen.") - 0.2, 0.25), (-60, 200), 44, 360)


def S_s7(c, t, n):
    base(c)
    stamp(c, "NO GET-RICH PROMISES", 540, 660, 66, -5, stamp_k(t, L0("s7") + 0.2), RED, 110)
    tape(c, "A CHEAP WAY TO TEST AN IDEA", 540, 840, 46, 3, pop_k(t, TW("s7", "test") - 0.1, 0.25), seed=111, col=GRN)
    char(c, "pbar", 380, 1440, 0.75, t, 0, (0.5, -0.3), "happy", "hips", blink=blink(t), lines_=BARLINES)
    cookie(c, 760, 1300, 0.9)


def S_e1(c, t, n):
    base(c)
    tape(c, "TRY IT NEXT TIME", 540, 540, 58, -3, pop_k(t, TW("e1", "Try") - 0.1, 0.25), seed=112)
    checklist(c, 540, 620, ["Don't copy the giants", "Find the small crowd they ignore"], [pr(t, TW("e1", "Don't") - 0.05, 0.4), pr(t, TW("e1", "small") - 0.05, 0.4)])
    char(c, "tub", 820, 1440, 0.5, t, 0, (-0.5, -0.5), "happy", "cheer", blink=blink(t))


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "tub", 300, 1440, 0.85, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t))
    char(c, "pbar", 790, 1440, 0.8, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3), lines_=BARLINES)
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=33)
        bubble(c, "the friend who lives on protein shakes", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 60, 700)
    else:
        title(c, "WHICH WOULD YOU START?", 540, 660, 76, INK, pop_k(t, L0("z2"), 0.3))
        stamp(c, "COOKIE", 330, 840, 76, -6, stamp_k(t, TW("z2", "COOKIE")), ORG, 120)
        stamp(c, "COFFEE", 750, 840, 76, 6, stamp_k(t, TW("z2", "COFFEE.")), BROWN, 121)


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
