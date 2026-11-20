# YANKEE CANDLE "too broke for a Christmas present" — real case study + 3 moves, SHORTS LENGTH (21 Nov 2026). DOODLE look, LIGHT page.
# Upgrade: SEASONAL object hook — the viewer is sixteen with empty pockets and a gift box with a '?' (Christmas-gift stake from frame 1), and the
# same pockets + crayon box come back for the callback ending, where the crayons turn into the candle.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: generic glass tumbler candles (no jar/lid/label shape, no brand colours), names as plain hand lettering, real people = plain doodles + name tapes.
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_kitchen", "b1", "whip"), ("S_mill", "b7", "whip"), ("S_score", "c1", "whip"),
         ("S_trim", "c4", "whip"), ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "broke"), "buzz"), (TW("i1", "present."), "pop"), (TW("i1", "what?"), "boing"),
        (TW("i2", "crayons."), "pop"), (TW("i2", "three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "third"), "stamp"), (TW("a1", "holidays."), "ding"),
        (TW("b1", "Kittredge."), "pop"), (TW("b1", "sixty-nine."), "stamp"),
        (TW("b2", "melts"), "slide"), (TW("b2", "candle."), "ding"),
        (TW("b3", "neighbor"), "pop"), (TW("b3", "wants"), "boing"),
        (TW("b4", "surprising"), "pop"), (TW("b4", "sells"), "chaching"),
        (L0("b5"), "boing"), (TW("b5", "still"), "ding"),
        (TW("b6", "wax"), "pop"), (TW("b6", "Mom,"), "pop"), (TW("b6", "sell."), "stamp"),
        (TW("b7", "seventy-three,"), "stamp"), (TW("b7", "mill"), "slam"), (TW("b7", "Yankee"), "chaching"),
        (TW("c1", "work?"), "tick"), (TW("c1", "ninety-eight."), "stamp"),
        (TW("c2", "five"), "chaching"), (TW("c3", "billion."), "chaching"), (TW("c3", "Mike."), "buzz"),
        (TW("c4", "trim"), "slide"), (TW("c4", "twenty"), "stamp"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "banned"), "buzz"),
        (TW("m2", "Two:"), "stamp"), (TW("m2", "label."), "pop"),
        (TW("m3", "Three:"), "stamp"), (TW("m3", "permit"), "stamp"),
        (L0("e1"), "boing"), (TW("e2", "exactly"), "ding"),
        (L0("z1"), "whoosh"), (TW("z2", "Pine,"), "stamp"), (TW("z2", "gingerbread?"), "stamp")]


def lt(t, sid): return t - SHOT[sid]["start"]


import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("TOO BROKE FOR A GIFT AT 16", "CRAYONS TO A $1.75 BILLION BRAND?")   # (kicker, TITLE) on frame 0 = the grid cover
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%€]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i1": "You're 16, and too broke to buy Mom a Christmas present. Now what?",
        "i2": "One kid melted crayons. Your 3 moves are at the end.",
        "b1": "Meet Mike Kittredge. Massachusetts, 1969.",
        "b7": "By 1973, there's an old mill and a name: Yankee Candle.",
        "c1": "Did it work? He sells most of it in 1998.",
        "c2": "The price? About $500 million.",
        "c3": "Later, a new owner pays $1.75 billion. Not to Mike.",
        "c4": "Big brands trim too. Owner Newell has announced about 20 store closures.",
        "m1": "Your moves. 1: lead-free wicks only, since America banned lead-core wicks.",
        "m2": "2: a fire-safety label. Burn within sight, away from kids.",
        "m3": "3: test a small batch at a craft fair. Check your state's permit rules."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
YOU = GRN


def _cur(t):
    cur = None
    for lid in _ORDER:
        if LINES[lid]["start"] - 0.05 <= t: cur = lid
    return cur


def chunk_now(t):
    """current 2-5 word subtitle chunk (breaks at punctuation), typed as spoken; returns (words, highlight set)."""
    cur = _cur(t)
    if cur is None: return [], set()
    d = DISP.get(cur, _VL.get(cur, LINES[cur].get("text", ""))).split(); ts = _LW.get(cur, [])
    k = sum(1 for x in ts if x <= t + 0.04); K = max(1, len(ts))
    n = len(d) if t > LINES[cur]["end"] else max(1, math.ceil(k / K * len(d)))
    chunks, c0 = [], 0
    for i, w in enumerate(d):
        if i - c0 + 1 >= 5 or w[-1:] in ".?!,:;\"" or i == len(d) - 1:
            chunks.append((c0, i + 1)); c0 = i + 1
    for a_, b_ in chunks:
        if a_ < n <= b_: hl = set(_HL.get(cur, set())) | {re.sub(r"[^a-z0-9$%€]", "", x.lower()) for x in d if any(ch.isdigit() for ch in x)}; return d[a_:n], hl
    return [], set()


def speaking(t, ids): return any(LINES[i]["start"] <= t <= LINES[i]["end"] + 0.05 for i in ids if i in LINES)


def mth(t, ids): return talk(t) / 3.0 if speaking(t, ids) else 0.0


def blink(t, seed=0): return (int(t * 12 + seed * 7) % 43) in (0, 1)


def base(c, tint=None, a=0.0, gy=1440):
    page(c, tint, a); ground(c, gy)


def title(c, s, x, y, size, col=INK, k=1.0, rot=-2, fnt=MARK_F):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); text(c, s, 0, 0, size, col, fnt, maxw=860); c.restore()


def at(t, lid, w=None, off=0.0): return t >= (TW(lid, w) if w else L0(lid)) + off


def pk(t, lid, w=None, off=-0.1, d=0.3): return pop_k(t, (TW(lid, w) if w else L0(lid)) + off, d)


def sk(t, lid, w=None, off=0.0): return stamp_k(t, (TW(lid, w) if w else L0(lid)) + off)


def person(c, x, y, s=1.0, seed=0, col=BLU, t=0.0, pose="stand", name=None, mood="neutral", look=(0, 0), hair="short", k=1.0, nsize=34):
    """plain doodle person (no likeness): round head with dot eyes, stick body; name on a tape. k = pop scale."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k); c.translate(-x, -y)
    hy = y - 230 * s
    wline(c, [(x, hy + 50 * s), (x, y - 90 * s)], seed, 9 * s)
    for sx in (-1, 1): limb(c, x, y - 90 * s, x + sx * 34 * s, y, 6 * sx * s, 8, False, seed + sx, foot=True, s=s)
    arms = {"stand": ((-50, 80), (50, 80)), "up": ((-80, -80), (80, -80)), "head": ((-40, -110), (40, -110)), "hold": ((60, 20), (90, 10)),
            "wave": ((-50, 80), (90, -60 + 20 * math.sin(t * 9))), "point": ((-50, 80), (110, -30)), "shrug": ((-80, -20), (80, -20)),
            "push": ((90, -10), (100, 20)), "lpoint": ((-110, -30), (50, 80))}[pose]
    for (dx, dy), sd in zip(arms, (1, 2)): limb(c, x, y - 160 * s, x + dx * s, y - 160 * s + dy * s, 14 * s, 8, True, seed + sd, s=s)
    if hair == "long": ink(c, wpoly([(x - 66 * s, hy - 20 * s), (x + 66 * s, hy - 20 * s), (x + 74 * s, hy + 110 * s), (x - 74 * s, hy + 110 * s)], seed + 9, 1.6, True, 40), col, 7 * s)
    ink(c, wellipse(x, hy, 52 * s, 56 * s, seed + 4, 1.5), (255, 224, 196), 8 * s)
    eyes(c, x + look[0] * 6 * s, hy - 6 * s, s * 0.5, look, blink(t, seed), 40, 22, mood, seed + 5)
    mouth(c, x, hy + 26 * s, s * 0.45, 0, mood, seed + 6)
    if hair == "short": ink(c, wpoly([(x - 54 * s, hy - 20 * s), (x - 40 * s, hy - 60 * s), (x, hy - 64 * s), (x + 44 * s, hy - 56 * s), (x + 54 * s, hy - 24 * s), (x + 30 * s, hy - 44 * s), (x - 30 * s, hy - 44 * s)], seed + 7, 1.2, True, 30), col, 6 * s)
    if name: tape(c, name, x, y + 46, nsize, (-3, 3)[seed % 2], 1.0, seed=seed)
    c.restore()


def you(c, x, y, t, s=1.0, pose="stand", mood="neutral", look=(0, 0), k=1.0):
    """the recurring viewer stand-in (green shirt, name tape YOU)."""
    person(c, x, y, s, 777, YOU, t, pose, "YOU", mood, look, "short", k)


_tape0 = tape


def tape(c, s, x, y, size=46, rot=-3, k=1.0, col=None, fg=INK, seed=1):
    _tape0(c, s, x, y, size, rot, k, ORG if col is None else col, fg, seed)




def pockets(c, x, y, k=1.0, seed=0):
    """two pulled-out empty trouser pockets (white flaps) + a moth, next to YOU."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    for sx in (-1, 1):
        ink(c, wpoly([(sx * 40, 0), (sx * 110, 0), (sx * 95, 90), (sx * 55, 90)], seed + sx, 1.2, True, 20), WHITE, 6)
    c.restore()


def moth(c, x, y, t, seed=0, k=1.0):
    if k <= 0: return
    yy = y + 14 * math.sin(t * 6 + seed); fl = abs(math.sin(t * 18))
    for sx in (-1, 1): ink(c, wellipse(x + sx * 24, yy, 26, 18 + 10 * fl, seed + sx, 1), GREY, 5)
    ink(c, wellipse(x, yy, 8, 22, seed + 3, 0.6), INK, 0)


# ---------------------------------------------------------------- hook (i1-i2): YOU, 16, empty pockets, gift box with a '?', then the crayon box
def S_hook(c, t, n):
    base(c)
    live = t > COVER_T
    crayons = live and at(t, "i2", "crayons.", -0.3)
    you(c, 300, 1440, t, 0.95, "shrug" if live and at(t, "i1", "broke", -0.1) and not crayons else ("point" if crayons else "stand"),
        "worried" if live and not crayons else ("happy" if crayons else "neutral"), (1, 0))
    gift_box(c, 760, 1440, 1.15, 3001, pk(t, "i1", "present.") if live else 1.0, RED, YEL, q=True)
    if not live: return
    if at(t, "i1", "sixteen,", -0.2): tape(c, "AGE 16", 300, 1500, 40, 2, pk(t, "i1", "sixteen,"), seed=3002, col=WHITE)
    if at(t, "i1", "broke", -0.1) and not crayons:
        pockets(c, 300, 1250, pk(t, "i1", "broke"), 3003)
        moth(c, 180 + 40 * math.sin(t * 2), 980, t, 3004)
        stamp(c, "$0", 520, 720, 130, -8, sk(t, "i1", "broke", 0.1), RED, 3005)
    if at(t, "i1", "Mom", -0.2) and not crayons:
        tape(c, "MOM'S CHRISTMAS PRESENT?", 680, 560, 44, 3, pk(t, "i1", "Mom"), seed=3006)
    if crayons:
        crayon_box(c, 560, 1000, 1.0, 3007, pk(t, "i2", "crayons."))
        for j in range(5):
            u = pr(t, TW("i2", "crayons.") + j * 0.08, 0.6)
            if u > 0: crayon(c, 560 + (j - 2) * 110 * eout(u), 760 - 220 * eout(u) + 260 * u * u, 0.7, (j - 2) * 30 + 300 * u, CRAYON_COLS[j], 3010 + j)
    if at(t, "i2", "three", -0.2):
        stamp(c, "3 MOVES AT THE END", 540, 450, 56, -3, sk(t, "i2", "three", 0.2), RED, 3020)


# ---------------------------------------------------------------- the timing (a1): over a third of candle sales over the holidays
def S_trend(c, t, n):
    base(c)
    tape(c, "THE TIMING: THE HOLIDAYS", 540, 470, 50, -3, pk(t, "a1"), seed=3030, col=INK, fg=WHITE)
    g = eout(pr(t, TW("a1", "third") - 0.3, 1.0))
    pie(c, 380, 900, 210, 0.35, g, 3031, (RED, CREAM))
    if g > 0.5: text(c, "~35%", 380, 1180, 70, RED, MARK_F)
    for j, col in enumerate((RED, GRN, YEL)):
        jar_candle(c, 760 + (j - 1) * 120, 1200 - (j % 2) * 30, 0.55, col, t, 3032 + j, pk(t, "a1", "candle", j * 0.12))
    if at(t, "a1", "holidays.", -0.2):
        stamp(c, "OVER A THIRD", 760, 760, 70, 6, sk(t, "a1", "holidays."), RED, 3036)
        tape(c, "OF YEARLY CANDLE SALES (NATIONAL CANDLE ASSOCIATION)", 540, 1300, 26, 1, pk(t, "a1", "holidays.", 0.2), seed=3037, col=WHITE)
    you(c, 900, 1440, t, 0.6, "head" if at(t, "a1", "holidays.", -0.2) else "stand", "shock" if at(t, "a1", "holidays.", -0.2) else "neutral", (-1, 0))


# ---------------------------------------------------------------- 1969 kitchen (b1-b6): crayons -> candle -> neighbor -> sold -> wax for two
def S_kitchen(c, t, n):
    base(c)
    b2 = at(t, "b2", None, -0.1); b3 = at(t, "b3", None, -0.1); b4 = at(t, "b4", None, -0.1); b5 = at(t, "b5", None, -0.1); b6 = at(t, "b6", None, -0.1)
    if not b2:
        calendar(c, 760, 860, 1969, 1.0, pk(t, "b1", "sixty-nine."), 3040)
        tape(c, "MASSACHUSETTS", 330, 560, 56, -4, pk(t, "b1", "Massachusetts,"), seed=3041, col=WHITE)
        person(c, 330, 1440, 0.95, 3042, BLU, t, "wave", "MIKE KITTREDGE, 16", "happy", (1, 0), "short", pk(t, "b1", "Kittredge."), 30)
        return
    if not b6:
        stove(c, 300, 1440, 1.0, 3043)
        melt_pot(c, 300, 960, 0.6, t, 3044, pr(t, TW("b2", "melts") - 0.1, 1.2), 1.0)
        if not b4:
            person(c, 660, 1440, 0.8, 3042, BLU, t, "hold", "MIKE", "happy", (-1, 0), "short", 1.0, 30)
        if at(t, "b2", "candle.", -0.3) and not b4:
            jar_candle(c, 800, 1440, 0.6, RED, t, 3045, pk(t, "b2", "candle."), True, None)
        if not b3: tape(c, "USE REAL CANDLE WAX + AN ADULT NEARBY", 540, 1490, 28, 1, pk(t, "b2", "stove", 0.2), seed=3046, col=WHITE)
        if b3:
            person(c, 930, 1440, 0.8, 3047, PNK, t, "point", "NEIGHBOR", "happy", (-1, 0), "long", pk(t, "b3", "neighbor"), 30)
            if at(t, "b3", "wants", -0.2) and not b4: bubble(c, "I want one!", 820, 760, pk(t, "b3", "wants"), (60, 200), 54, 420)
        if b4 and not b5:
            u = eout(pr(t, TW("b4", "sells") - 0.2, 0.6))
            person(c, 620, 1440, 0.8, 3042, BLU, t, "point", "MIKE", "happy", (1, 0), "short", 1.0, 30)
            jar_candle(c, 780 + 60 * u, 1440, 0.6, RED, t, 3045, 1.0, True, None)
            tape(c, "THE SURPRISING MOVE", 560, 470, 50, -3, pk(t, "b4", "surprising"), seed=3048, col=INK, fg=WHITE)
            if at(t, "b4", "sells", -0.1):
                stamp(c, "SOLD!", 640, 760, 110, -6, sk(t, "b4", "sells"), RED, 3049)
                text(c, "$", 560, 1080 - 60 * pr(t, TW("b4", "sells"), 0.5), 90, DGRN, MARK_F)
        if b5:
            person(c, 620, 1440, 0.7, 3042, BLU, t, "stand", "MIKE", "happy", (1, 0), "short", 1.0, 28)
            char(c, "candle", 850, 1440, 0.7, t, mth(t, ["b5"]), (-0.4, -0.2), "happy", "wave", blink=blink(t), seed=3050, col=GRN)
            bubble(c, "Relax. Mom still gets a candle.", 560, 600, pk(t, "b5"), (220, 220), 52, 640)
        return
    # b6: cash -> wax for two -> MOM + TO SELL
    money_stack(c, 200, 1300, 2, 1.0, 3051)
    arrow(c, 300, 1180, 430, 1100, -40, RED, 8, 3052, pr(t, TW("b6", "wax") - 0.3, 0.4))
    for j in range(2):
        kk = pk(t, "b6", "wax", j * 0.12)
        if kk > 0: ink(c, wrrect(470 + j * 130 - 50, 1060 - 40 * kk, 470 + j * 130 + 50, 1100, 10, 3053 + j, 1.2), CREAM, 7)
    if at(t, "b6", "wax", -0.2): tape(c, "WAX FOR TWO", 540, 980, 40, 2, pk(t, "b6", "wax"), seed=3055, col=WHITE)
    jar_candle(c, 380, 1400, 0.75, GRN, t, 3056, pk(t, "b6", "Mom,"), True, "MOM")
    jar_candle(c, 760, 1400, 0.75, RED, t, 3057, pk(t, "b6", "sell."), True, "TO SELL")
    if at(t, "b6", "sell.", -0.1): stamp(c, "1 FOR MOM, 1 TO SELL", 560, 600, 60, -4, sk(t, "b6", "sell."), RED, 3058)


# ---------------------------------------------------------------- the mill (b7): 1973, an old paper mill and a name
def S_mill(c, t, n):
    base(c)
    mill(c, 520, 1440, 0.9, 3060, pk(t, "b7", None, 0.1), t)
    calendar(c, 860, 720, 1973, 0.6, pk(t, "b7", "seventy-three,"), 3061)
    if at(t, "b7", "mill", -0.2): tape(c, "AN OLD PAPER MILL, HOLYOKE", 520, 1490, 36, 1, pk(t, "b7", "mill"), seed=3062, col=WHITE)
    if at(t, "b7", "Yankee", -0.3):
        title(c, "YANKEE CANDLE", 470, 560, 92, INK, pk(t, "b7", "Yankee"), -3)
        wline(c, [(170, 610), (770, 600)], 3063, 10, YEL)


# ---------------------------------------------------------------- did it work? (c1-c3)
def S_score(c, t, n):
    base(c)
    tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "c1"), seed=3070, col=INK, fg=WHITE)
    c3 = at(t, "c3", None, -0.1)
    if not c3:
        calendar(c, 300, 820, 1998, 0.7, pk(t, "c1", "ninety-eight."), 3071)
        person(c, 300, 1440, 0.8, 3072, BLU, t, "point" if at(t, "c2", None) else "stand", "MIKE", "happy", (1, 0), "short", 1.0, 30)
        if at(t, "c1", "most", -0.2):
            pie(c, 760, 760, 150, 0.9, eout(pr(t, TW("c1", "most") - 0.2, 0.8)), 3073, (ORG, CREAM))
            tape(c, "~90% SOLD", 760, 960, 40, 2, pk(t, "c1", "most", 0.3), seed=3074, col=WHITE)
        if at(t, "c2", "five", -0.3):
            money_stack(c, 760, 1440, int(1 + 7 * pr(t, TW("c2", "five") - 0.3, 0.8)), 1.1, 3075)
            stamp(c, "~$500M", 760, 1120, 90, -6, sk(t, "c2", "five"), RED, 3076)
        return
    money_stack(c, 300, 1440, 8, 1.0, 3075); text(c, "1998", 300, 1490, 34, INK, BLK_F)
    g = eout(pr(t, TW("c3", "billion.") - 0.4, 1.0))
    money_stack(c, 720, 1440, int(1 + 20 * g), 1.2, 3077)
    if at(t, "c3", "billion.", -0.2):
        stamp(c, "$1.75B", 330, 700, 110, -5, sk(t, "c3", "billion."), RED, 3078)
        tape(c, "2013: JARDEN BUYS IT FROM MADISON DEARBORN", 540, 1490, 28, 1, pk(t, "c3", "billion.", 0.2), seed=3079, col=WHITE)
    if at(t, "c3", "Mike.", -0.2):
        tape(c, "NOT TO MIKE", 300, 1000, 46, -4, pk(t, "c3", "Mike."), seed=3080)
        tape(c, "ONE RARE OUTCOME, NOT TYPICAL", 540, 640, 32, 2, pk(t, "c3", "Mike.", 0.3), seed=3081, col=WHITE)


# ---------------------------------------------------------------- big brands trim too (c4)
def S_trim(c, t, n):
    base(c)
    tape(c, "BIG BRANDS TRIM TOO", 540, 470, 54, -3, pk(t, "c4", "trim"), seed=3090, col=INK, fg=WHITE)
    for j in range(6):
        x = 220 + (j % 3) * 320; y = 1000 if j < 3 else 1400
        mini_shop(c, x, y, t, 3091 + j)
        if j in (1, 3, 5) and at(t, "c4", "twenty", -0.3):
            kx = pr(t, TW("c4", "twenty") - 0.3 + j * 0.06, 0.3)
            wline(c, [(x - 100, y - 220), (x - 100 + 200 * kx, y - 220 + 200 * kx)], 3100 + j, 14, RED)
            if kx >= 1: wline(c, [(x + 100, y - 220), (x - 100, y - 20)], 3110 + j, 14, RED)
    if at(t, "c4", "Newell", -0.2): tape(c, "OWNER: NEWELL BRANDS", 540, 600, 40, 2, pk(t, "c4", "Newell"), seed=3120, col=WHITE)
    if at(t, "c4", "twenty", -0.2): tape(c, "DEC 2025: ~20 STORES TO CLOSE (US + CANADA)", 540, 1490, 28, 1, pk(t, "c4", "twenty", 0.2), seed=3121, col=WHITE)


def mini_shop(c, x, y, t, seed):
    """small generic candle shop front (no brand): box, striped awning, window with one candle, door. (x, y) = bottom centre."""
    ink(c, wrrect(x - 120, y - 210, x + 120, y, 8, seed, 1.4), CREAM, 8)
    ink(c, wpoly([(x - 135, y - 210), (x + 135, y - 210), (x + 120, y - 160), (x - 120, y - 160)], seed + 1, 1.2, True, 30), RED, 7)
    for q in range(3): c.drawRect(skia.Rect.MakeLTRB(x - 110 + q * 80, y - 205, x - 70 + q * 80, y - 165), P(WHITE, 0.85))
    text(c, "CANDLES", x, y - 225, 30, INK, BLK_F)
    ink(c, wrrect(x - 100, y - 140, x + 10, y - 50, 6, seed + 2, 1.0), SKY, 6)
    jar_candle(c, x - 45, y - 56, 0.3, (230, 70, 70), t, seed + 3)
    ink(c, wrrect(x + 30, y - 140, x + 95, y, 6, seed + 4, 1.0), BROWN, 6)


# ---------------------------------------------------------------- 3 moves (m1-m3): one evolving board
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 450, 52, -3, pk(t, "m1"), seed=3130, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. LEAD-FREE WICKS ONLY"), ("m2", "Two:", "2. A FIRE-SAFETY LABEL"), ("m3", "Three:", "3. SMALL BATCH + PERMIT")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=0)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 550 + i * 74; tape(c, lab, 500, y, 34, (-2, 2, -1)[i], pk(t, l, w), seed=3131 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(800, y - 5), (820, y + 15), (860, y - 25)], 3135 + i, 8, RED)
    if cur == 0:
        wick(c, 330, 1300, 1.0, 3140, 1.0, True, t)
        text(c, "LEAD CORE", 330, 880, 40, INK, BLK_F)
        if at(t, "m1", "banned", -0.2):
            ink(c, wellipse(330, 1140, 190, 190 * ease(pr(t, TW("m1", "banned") - 0.2, 0.3)), 3141, 2), None, 18, RED)
            wline(c, [(200, 1010), (460, 1270)], 3142, 18, RED)
            tape(c, "US BAN SINCE 2003 (CPSC)", 330, 1490, 32, 1, pk(t, "m1", "banned"), seed=3143, col=WHITE)
        wick(c, 750, 1300, 1.0, 3144, pk(t, "m1", "lead-free"), False, t)
        if at(t, "m1", "lead-free", -0.2):
            text(c, "LEAD-FREE", 750, 880, 40, DGRN, BLK_F)
            wline(c, [(700, 1360), (740, 1400), (820, 1320)], 3145, 12, GRN)
    elif cur == 1:
        safety_label(c, 540, 1000, 1.25, 3150, pk(t, "m2", "label."), 1 + int(at(t, "m2", "sight,", -0.2)) + int(at(t, "m2", "kids.", -0.2)))
        jar_candle(c, 860, 1440, 0.7, RED, t, 3151, 1.0)
        if at(t, "m2", "label.", -0.2): tape(c, "INDUSTRY STANDARD: ASTM F2058", 540, 1490, 32, 1, pk(t, "m2", "label.", 0.2), seed=3152, col=WHITE)
    else:
        stall(c, 400, 1440, 0.95, 3160, "CRAFT FAIR")
        for j, col in enumerate((RED, GRN, YEL)): jar_candle(c, 300 + j * 100, 1230, 0.42, col, t, 3161 + j, pk(t, "m3", "small", j * 0.1))
        if at(t, "m3", "small", -0.2): tape(c, "SMALL BATCH FIRST", 400, 880, 40, -2, pk(t, "m3", "small"), seed=3165, col=WHITE)
        permit_doc(c, 830, 1200, 0.8, 3166, pk(t, "m3", "permit", -0.3), pr(t, TW("m3", "permit"), 0.4))
        if at(t, "m3", "permit", -0.2): tape(c, "RULES VARY BY STATE", 540, 1490, 32, 1, pk(t, "m3", "permit", 0.2), seed=3167, col=WHITE)


# ---------------------------------------------------------------- callback (e1-e2): YOU broke again, crayons -> candle
def S_end(c, t, n):
    base(c)
    e2 = at(t, "e2", None, -0.1)
    you(c, 300, 1440, t, 0.95, "shrug" if not e2 else "point", "worried" if not e2 else "happy", (1, 0))
    if not e2:
        pockets(c, 300, 1250, 1.0, 3003); moth(c, 200, 980, t, 3004)
        gift_box(c, 760, 1440, 1.15, 3001, 1.0, RED, YEL, q=True)
        return
    u = pr(t, L0("e2"), 0.8)
    crayon_box(c, 760, 1000, 0.8, 3007, 1.0 - u)
    jar_candle(c, 760, 1440, 1.1, RED, t, 3170, eout(pr(t, L0("e2") + 0.4, 0.5)), True, "FOR MOM")
    if at(t, "e2", "exactly", -0.2):
        tape(c, "1969: IT STARTED LIKE THIS", 560, 560, 44, -3, pk(t, "e2", "exactly"), seed=3171)
        wline(c, [(880, 760), (900, 790), (950, 720)], 3172, 10, RED)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=3180, col=INK, fg=WHITE)
        bubble(c, "the friend who buys a candle every December", 540, 690, pk(t, "z1", "friend"), (-180, 200), 50, 760)
        phone(c, 260, 1200, 0.5, 3181)
        person(c, 760, 1440, 0.75, 3182, PNK, t, "hold", "FRIEND", "happy", (-1, 0), "long", 1.0, 30)
        jar_candle(c, 860, 1250, 0.45, GRN, t, 3183, pk(t, "z1", "December."))
        arrow(c, 330, 1100, 640, 1040, 60, RED, 8, 3184, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "PINE OR GINGERBREAD?", 540, 560, 74, INK, pk(t, "z2"))
        jar_candle(c, 300, 1300, 1.0, DGRN, t, 3190, 1.0, True)
        jar_candle(c, 780, 1300, 1.0, BROWN, t, 3191, 1.0, True)
        stamp(c, "PINE", 300, 900, 80, -6, sk(t, "z2", "Pine,"), GRN, 3192)
        stamp(c, "GINGERBREAD", 780, 900, 64, 6, sk(t, "z2", "gingerbread?"), RED, 3193)
        tape(c, "COMMENT BELOW", 540, 1480, 36, 2, pk(t, "z2", "comments."), seed=3194, col=WHITE)


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    global BOIL
    BOIL = int(t * 12)
    c = SURF.getCanvas(); c.clear(skia.Color(*PAPER))
    c.save()
    for ti, kind in CUES:
        if kind in ("slam", "impact", "stamp") and 0 <= t - ti < 0.24:
            k = 1 - (t - ti) / 0.24; amp = 14 if kind != "stamp" else 7; c.translate(amp * k * math.sin(t * 90), amp * 0.8 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z = 1.0 + 0.03 * u; c.translate(W / 2, H * 0.55); c.scale(z, z); c.translate(-W / 2, -H * 0.55)
    RENDER[sid](c, t, n); c.restore()
    if COVER and t < COVER_T:   # big hook title on frame 0 = the grid cover
        kk = 1.0 if t < COVER_T - 0.35 else 1.0 - ease((t - (COVER_T - 0.35)) / 0.35)
        cover_title(c, COVER[0], COVER[1], kk, 640)
    if not (COVER and t < COVER_T - 0.35):
        _cw, _hl = chunk_now(t); strip_chunk(c, _cw, _hl, 268, 40, t)
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
