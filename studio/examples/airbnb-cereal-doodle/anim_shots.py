# REAL CASE STUDY — How $40 cereal saved Airbnb. DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = [k for k in LINES if k not in ("z2", "a5b", "b5b")]
_TR = {"i2": "pop", "a1": "whip", "a5": "pop", "b1": "whip", "b5": "pop", "b7": "pop", "c1": "whip", "c5": "pop", "c6": "pop", "d1": "whip",
       "d5": "pop", "d6": "pop", "t1": "cut", "e1": "pop", "z1": "pop"}
_MERGE = {"a2": None}   # every line gets its own shot
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "forty"), "chaching"), (TW("i2", "Airbnb"), "stamp"), (TW("i3", "no"), "buzz"), (TW("i3", "four"), "stamp"),
        (L0("a1"), "stamp"), (TW("a2", "rent"), "buzz"), (TW("a3", "crazy"), "pop"), (TW("a4", "air"), "inflate"), (TW("a4", "Eighty"), "pop"),
        (L0("a5"), "boing"), (TW("a6", "Three"), "ding"), (L0("b1"), "slide"), (TW("b2", "big"), "buzz"), (TW("b3", "twenty"), "stamp"),
        (TW("b4", "binder"), "pop"), (TW("b5b", "ridiculous"), "boing"), (TW("b6", "hand"), "pop"), (TW("b6", "forty"), "chaching"), (L0("b7"), "pop"),
        (TW("b8", "thousand"), "chaching"), (TW("b8", "alive"), "ding"), (L0("c1"), "stamp"), (TW("c2", "badly"), "buzz"), (TW("c3", "cereal"), "pop"),
        (TW("c4", "strangers'"), "ding"), (TW("c5", "cockroaches"), "boing"), (TW("c5", "twenty"), "chaching"), (L0("c6"), "pop"),
        (L0("d1"), "stamp"), (TW("d2", "stuck"), "buzz"), (TW("d3", "terrible"), "buzz"), (TW("d4", "shot"), "pop"), (TW("d6", "billions"), "chaching"), (TW("d5", "doubled"), "chaching"),
        (TW("t1", "hand"), "ding"), (TW("t2", "scale"), "stamp"), (TW("e1", "hand"), "tick"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i1": "Would you pay $40 for a box of cereal?", "i2": "Back in 2008, people actually did. And that weird cereal helped save Airbnb.",
        "a1": "First move. San Francisco, 2007.", "a4": "They blow up three air mattresses on the living room floor, and rent them out. $80 a night, breakfast included.",
        "b3": "By then, they owed over $20,000 on credit cards.", "b6": "Election-themed boxes, glued together by hand, sold for $40 each.",
        "b7": "I'm cheap cereal in a $40 box. Don't ask questions.", "b8": "They sold about 1,000 boxes. That brought in around $30,000, and kept the company alive.",
        "c4": "His point, as Chesky tells it? If people pay $40 for cheap cereal, maybe they'll sleep in strangers' homes too.",
        "c5": "He called them cockroaches. They just wouldn't die. So Y Combinator invested $20,000.", "d2": "Even after all that, the site was stuck at about $200 a week."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
MAT_L = {"a5", "a5b", "c6"}; BOX_L = {"b7"}
CEREAL = dict(col=(255, 200, 40), label="ELECTION\nCEREAL", fg=RED)


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


def person(c, x, y, s=1.0, seed=0, col=BLU, t=0.0, pose="stand", name=None, mood="neutral", look=(0, 0)):
    """plain doodle person (no likeness): round head with dot eyes, stick body; name on a tape."""
    hy = y - 230 * s
    wline(c, [(x, hy + 50 * s), (x, y - 90 * s)], seed, 9 * s)
    for sx in (-1, 1): limb(c, x, y - 90 * s, x + sx * 34 * s, y, 6 * sx * s, 8, False, seed + sx, foot=True, s=s)
    arms = {"stand": ((-50, 80), (50, 80)), "up": ((-80, -80), (80, -80)), "head": ((-40, -110), (40, -110)), "hold": ((60, 20), (90, 10)),
            "wave": ((-50, 80), (90, -60 + 20 * math.sin(t * 9)))}[pose]
    for (dx, dy), sd in zip(arms, (1, 2)): limb(c, x, y - 160 * s, x + dx * s, y - 160 * s + dy * s, 14 * s, 8, True, seed + sd, s=s)
    ink(c, wellipse(x, hy, 52 * s, 56 * s, seed + 4, 1.5), (255, 224, 196), 8 * s)
    eyes(c, x + look[0] * 6 * s, hy - 6 * s, s * 0.5, look, blink(t, seed), 40, 22, mood, seed + 5)
    mouth(c, x, hy + 26 * s, s * 0.45, 0, mood, seed + 6)
    ink(c, wpoly([(x - 54 * s, hy - 20 * s), (x - 40 * s, hy - 60 * s), (x, hy - 64 * s), (x + 44 * s, hy - 56 * s), (x + 54 * s, hy - 24 * s), (x + 30 * s, hy - 44 * s), (x - 30 * s, hy - 44 * s)], seed + 7, 1.2, True, 30), col, 6 * s)
    if name: tape(c, name, x, y + 46, 34, (-3, 3)[seed % 2], 1.0, seed=seed)


# ---------------------------------------------------------------- hook
def S_i1(c, t, n):
    base(c, tint=YEL)
    char(c, "box", 560, 1440, 1.2, t, 0, (-0.4, -0.3), "happy", "hips", blink=blink(t), **CEREAL)
    char(c, "tag", 860, 1440, 0.62, t, 0, (-0.6, -0.4), "happy", "point", blink=blink(t, 3), price="$40")
    char(c, "bill", 220 + slide_in(t, 0.0, 0.6, -500), 1440, 0.62, t, 0, (1, -0.3), "shock" if t > TW("i1", "forty") else "happy", "shrug", walk=t < 0.6)
    tape(c, "$40 CEREAL?!", 540, 620, 64, -3, pop_k(t, TW("i1", "forty") - 0.1, 0.25), seed=3)


def S_i2(c, t, n):
    base(c)
    char(c, "box", 300, 1440, 0.8, t, 0, (0.5, -0.3), "happy", "cheer", blink=blink(t), **CEREAL)
    k = pop_k(t, TW("i2", "Airbnb") - 0.15, 0.35)
    if k > 0:
        c.save(); c.translate(760, 1180); c.scale(k, k); ink(c, wpoly([(-170, 0), (0, -150), (170, 0), (130, 0), (130, 250), (-130, 250), (-130, 0)], 40, 2, True, 50), PNK, 9)
        ink(c, wrrect(-40, 110, 40, 250, 6, 41, 1), WHITE, 7); c.restore()
        tape(c, "AIRBNB", 760, 1100, 56, 4, k, seed=4)
    arrow(c, 430, 1150, 620, 1150, -60, RED, 10, 5, pr(t, TW("i2", "helped") - 0.1, 0.4))
    tape(c, "2008", 300, 640, 60, -5, pop_k(t, L0("i2"), 0.25), seed=6)


def S_i3(c, t, n):
    base(c, tint=RED)
    person(c, 260, 1440, 1.35, 1, BROWN, t, "head", mood="worried")
    person(c, 540, 1440, 1.35, 2, INK, t, "head", mood="worried")
    person(c, 820, 1440, 1.35, 3, ORG, t, "stand", mood="worried")
    for i, w_ in enumerate(("BROKE", "DEBT", "\"NO\"")):
        stamp(c, w_, 230 + i * 300, 640 + (i % 2) * 70, 66, (-8, 6, -4)[i], stamp_k(t, TW("i3", ("broke", "debt", "no")[i])), RED, 10 + i)
    title(c, "4 STRANGE MOVES", 540, 900, 96, INK, pop_k(t, TW("i3", "four"), 0.3))


# ---------------------------------------------------------------- move 1: the air mattress
def S_a1(c, t, n):
    base(c)
    stamp(c, "MOVE 1", 540, 620, 120, -6, stamp_k(t, L0("a1")), BLU, 21)
    tape(c, "SAN FRANCISCO, 2007", 540, 790, 52, 2, pop_k(t, TW("a1", "San") - 0.1, 0.25), seed=9)
    building(c, 300, 1440, 260, 460, SKY, 33); building(c, 560, 1440, 220, 380, (255, 186, 120), 34); building(c, 800, 1440, 260, 520, (180, 160, 255), 35)


def S_a2(c, t, n):
    base(c)
    person(c, 320, 1440, 1.6, 4, BROWN, t, "head", "BRIAN CHESKY", "worried", (0.5, 0))
    person(c, 760, 1440, 1.6, 5, INK, t, "head", "JOE GEBBIA", "worried", (-0.5, 0))
    k = pop_k(t, TW("a2", "rent") - 0.1, 0.3)
    if k > 0: c.save(); c.translate(540, 760); c.scale(k, k); ink(c, wrrect(-180, -110, 180, 110, 10, 61, 2), WHITE, 9)
    if k > 0: text(c, "RENT DUE", 0, -30, 54, RED, BLK_F); text(c, "$$$", 0, 50, 60, INK, BLK_F); c.restore()


def S_a3(c, t, n):
    base(c)
    tape(c, "DESIGN CONFERENCE", 540, 560, 54, -3, pop_k(t, TW("a3", "design") - 0.1, 0.25), seed=11)
    building(c, 540, 1440, 420, 600, (255, 120, 120), 36)
    tape(c, "HOTEL", 540, 860, 46, 2, 1.0, seed=12)
    for i, x in enumerate((170, 910)): stamp(c, "$$$", x, 900 + i * 60, 80, (-10, 10)[i], stamp_k(t, TW("a3", "crazy") + i * 0.15), RED, 13 + i)
    title(c, "???", 540, 700, 100, PUR, pop_k(t, TW("a3", "guess"), 0.3))


def S_a4(c, t, n):
    base(c, tint=SKY)
    k = pr(t, TW("a4", "air") - 0.1, 0.6)
    for i, x in enumerate((240, 540, 840)):
        kk = ease(min(1, max(0, k * 3 - i)))
        if kk > 0: ink(c, wrrect(x - 130, 1440 - 20 - 70 * kk, x + 130, 1440, 30, 70 + i, 2), (120, 190, 255), 8)
    laptop(c, 540, 1100, 0.9, k=pr(t, TW("a4", "rent") - 0.1, 0.3))
    tape(c, "$80 / NIGHT + BREAKFAST", 540, 600, 50, -3, pop_k(t, TW("a4", "Eighty") - 0.1, 0.25), seed=14)


def S_a5(c, t, n):
    base(c, tint=YEL)
    char(c, "mattress", 540, 1440, 1.25, t, mth(t, MAT_L), (0, -0.3), "happy", "wave", blink=blink(t))
    bubble(c, "Yep. That's me. The very first Airbnb was an air mattress.", 540, 640, pop_k(t, L0("a5"), 0.25), (-60, 240), 60, 760)


def S_a6(c, t, n):
    base(c)
    for i, (x, col) in enumerate(((230, PNK), (540, GRN), (850, ORG))):
        if t > TW("a6", "Three") - 0.2 + i * 0.15: person(c, x, 1300, 0.8, 20 + i, col, t, "wave", mood="happy")
    for i, x in enumerate((230, 540, 850)): ink(c, wrrect(x - 120, 1350, x + 120, 1440, 26, 80 + i, 2), (120, 190, 255), 8)
    stamp(c, "3 GUESTS", 540, 640, 90, -6, stamp_k(t, TW("a6", "Three")), DGRN, 15)
    tape(c, "IT WORKED", 540, 820, 54, 3, pop_k(t, TW("a6", "worked") - 0.1, 0.25), seed=16)


# ---------------------------------------------------------------- move 2: debt and cereal
def S_b1(c, t, n):
    base(c, tint=(120, 120, 140))
    stamp(c, "UH-OH", 540, 620, 120, 5, stamp_k(t, L0("b1")), ORG, 25)
    tape(c, "IT GETS UGLY", 540, 800, 56, -2, pop_k(t, TW("b1", "ugly") - 0.1, 0.25), seed=17)
    char(c, "mattress", 540, 1440, 0.8, t, 0, (0, 0.3), "worried", "down", blink=blink(t))


def S_b2(c, t, n):
    base(c)
    for i in range(3):
        k = pop_k(t, L0("b2") + 0.2 + i * 0.35, 0.3)
        if k > 0:
            c.save(); c.translate(250 + i * 290, 900 + (i % 2) * 80); c.rotate((-8, 5, -3)[i]); c.scale(k, k)
            ink(c, wrrect(-130, -90, 130, 90, 10, 90 + i, 2), WHITE, 8); text(c, "NO.", 0, 20, 70, RED, MARK_F); c.restore()
    bubble(c, "\"the market doesn't seem big enough\"", 540, 640, pop_k(t, TW("b2", "market") - 0.1, 0.25), (0, 160), 52, 760)
    person(c, 540, 1440, 1.1, 4, BROWN, t, "head", mood="worried")


def S_b3(c, t, n):
    base(c, tint=RED)
    title(c, "$20,000+ DEBT", 540, 720, 112, RED, pop_k(t, TW("b3", "twenty"), 0.3), -3, BLK_F)
    char(c, "card", 540, 1440, 0.9, t, 0, (0, 0.3), "worried", "shrug", blink=blink(t))
    stamp(c, "MAXED", 790, 1050, 70, 12, stamp_k(t, TW("b3", "credit")), RED, 18)


def S_b4(c, t, n):
    base(c)
    binder(c, 540, 1050, 1.25, k=pr(t, TW("b4", "binder") - 0.4, 0.8))
    tape(c, "THE BASEBALL CARD BINDER", 540, 600, 46, -3, pop_k(t, TW("b4", "baseball") - 0.1, 0.25), seed=19)


def S_b5(c, t, n):
    base(c, tint=YEL)
    person(c, 280, 1440, 1.3, 4, BROWN, t, "up" if t > TW("b5b", "ridiculous") else "head", mood="happy" if t > TW("b5b", "ridiculous") else "worried")
    stamp(c, "MOVE 2", 640, 640, 100, 5, stamp_k(t, TW("b5", "Move")), ORG, 26)
    title(c, "IDEA: CEREAL?!", 640, 840, 84, INK, pop_k(t, TW("b5b", "ridiculous"), 0.3))
    k = pop_k(t, TW("b5b", "cereal") - 0.2, 0.35)
    if k > 0: char(c, "box", 720, 1440, 0.95 * k, t, 0, (-0.5, -0.3), "happy", "cheer", blink=blink(t), **CEREAL)


def S_b6(c, t, n):
    base(c)
    for i, (x, col) in enumerate(((300, (255, 200, 40)), (760, (120, 200, 255)))):
        char(c, "box", x, 1440, 0.85, t, 0, ((0.5, -0.3), (-0.5, -0.3))[i], "happy", "hips", blink=blink(t, i), col=col, label="ELECTION\nCEREAL", fg=(RED, BLU)[i])
    tape(c, "GLUED BY HAND", 540, 600, 56, -3, pop_k(t, TW("b6", "glued") - 0.1, 0.25), seed=20)
    stamp(c, "$40 EACH", 540, 780, 90, -6, stamp_k(t, TW("b6", "forty")), RED, 21)


def S_b7(c, t, n):
    base(c, tint=YEL)
    char(c, "box", 540, 1440, 1.3, t, mth(t, BOX_L), (0, -0.3), "happy", "hips", blink=blink(t), **CEREAL)
    bubble(c, "I'm cheap cereal in a $40 box. Don't ask questions.", 540, 640, pop_k(t, L0("b7"), 0.25), (-40, 220), 60, 720)


def S_b8(c, t, n):
    base(c, tint=GRN)
    k = pr(t, TW("b8", "thousand") - 0.2, 0.8)
    for i in range(int(14 * k)):
        r, q = divmod(i, 7); x = 130 + q * 135 + (66 if r else 0); y = 1440 - r * 160
        char(c, "box", x, y, 0.3, t, 0, (0, -0.3), "happy", "down", blink=blink(t, i), col=((255, 200, 40), (120, 200, 255))[i % 2], label="CEREAL", fg=RED, shadow_w=0.6)
    title(c, "~1,000 BOXES", 540, 640, 96, INK, pop_k(t, TW("b8", "thousand"), 0.3))
    title(c, "~$30,000", 540, 820, 120, DGRN, pop_k(t, TW("b8", "thirty"), 0.3), 2, BLK_F)
    stamp(c, "STILL ALIVE", 540, 990, 70, -6, stamp_k(t, TW("b8", "alive")), DGRN, 22)


# ---------------------------------------------------------------- move 3: the interview
def S_c1(c, t, n):
    base(c)
    stamp(c, "MOVE 3", 540, 620, 120, -4, stamp_k(t, L0("c1")), RED, 29)
    tape(c, "THE INTERVIEW", 540, 790, 54, 3, pop_k(t, TW("c1", "interview") - 0.1, 0.25), seed=22)
    building(c, 540, 1440, 380, 460, (180, 160, 255), 37)


def S_c2(c, t, n):
    base(c)
    person(c, 260, 1440, 1.4, 4, BROWN, t, "stand", "BRIAN", "worried" if t > TW("c2", "badly") else "neutral", (1, 0))
    person(c, 800, 1440, 1.4, 8, GREY, t, "stand", "PAUL GRAHAM", "neutral", (-1, 0))
    tape(c, "Y COMBINATOR", 540, 580, 56, -3, pop_k(t, TW("c2", "Combinator") - 0.2, 0.25), seed=23)
    stamp(c, "WENT BADLY", 540, 800, 76, -6, stamp_k(t, TW("c2", "badly")), RED, 24)


def S_c3(c, t, n):
    base(c, tint=YEL)
    person(c, 820, 1440, 1.4, 8, GREY, t, "hold", "PAUL GRAHAM", "shock" if t > TW("c3", "cereal") else "neutral", (-1, 0))
    u = eout(pr(t, TW("c3", "handed") - 0.2, 0.7))
    char(c, "box", 220 + 320 * u, 1440 - 30 * math.sin(u * math.pi), 0.6, t, 0, (1, -0.2), "happy", "wave", blink=blink(t), **CEREAL)
    tape(c, "THE CEREAL MOVE", 540, 600, 56, -3, pop_k(t, L0("c3"), 0.25), seed=25)


def S_c4(c, t, n):
    base(c)
    person(c, 200, 1440, 1.2, 8, GREY, t, "hold", None, "happy", (1, 0))
    char(c, "box", 380, 1440, 0.5, t, 0, (1, -0.2), "happy", "hips", blink=blink(t), **CEREAL)
    k = pr(t, TW("c4", "maybe") - 0.1, 0.3)
    bubble(c, "Pay $40 for cheap cereal? Then maybe they'll sleep in strangers' homes too.", 600, 760, pop_k(t, TW("c4", "If") - 0.1, 0.25), (-260, 300), 54, 680)
    if k > 0: char(c, "mattress", 840, 1440, 0.55 * k, t, 0, (-0.5, -0.3), "happy", "cheer", blink=blink(t, 3))


def S_c5(c, t, n):
    base(c, tint=GRN)
    cockroach(c, 540, 1250, 1.5, t)
    tape(c, "\"COCKROACHES\"", 540, 600, 60, -3, pop_k(t, TW("c5", "cockroaches") - 0.1, 0.25), seed=26)
    tape(c, "THEY WOULDN'T DIE", 540, 720, 48, 3, pop_k(t, TW("c5", "die") - 0.1, 0.25), seed=27, col=PNK)
    stamp(c, "Y COMBINATOR\n+$20,000", 540, 900, 70, -6, stamp_k(t, TW("c5", "twenty")), DGRN, 28)


def S_c6(c, t, n):
    base(c, tint=PNK)
    char(c, "mattress", 380, 1440, 1.1, t, mth(t, MAT_L), (0.5, -0.3), "worried" if t < TW("c6", "fair") else "happy", "hips", blink=blink(t))
    cockroach(c, 800, 1380, 0.8, t)
    bubble(c, "Cockroaches? Wow, rude. But honestly... kind of fair.", 540, 660, pop_k(t, L0("c6"), 0.25), (-120, 220), 60, 720)


# ---------------------------------------------------------------- move 4: the photos
def S_d1(c, t, n):
    base(c)
    stamp(c, "MOVE 4", 540, 620, 120, 6, stamp_k(t, L0("d1")), PUR, 30)
    tape(c, "THE FIX NOBODY EXPECTED", 540, 790, 48, -2, pop_k(t, TW("d1", "fix") - 0.1, 0.25), seed=30)
    laptop(c, 540, 1380, 0.9, k=1.0)


def _chart(c, t, t0, pts, grow=1.0, col=GRN):
    wline(c, [(150, 1340), (150, 760)], 50, 8); wline(c, [(150, 1340), (930, 1340)], 51, 8)
    k = pr(t, t0, grow); m = max(2, int(len(pts) * k + 0.999)); wline(c, pts[:m], 52, 14, col, 1.4)


def S_d2(c, t, n):
    base(c)
    _chart(c, t, L0("d2"), [(170, 1200), (330, 1205), (490, 1195), (650, 1202), (810, 1198), (910, 1200)], 1.4, RED)
    text(c, "$ / WEEK", 270, 800, 44, INK, BLK_F)
    stamp(c, "STUCK AT ~$200", 560, 1000, 70, -6, stamp_k(t, TW("d2", "stuck")), RED, 31)


def S_d3(c, t, n):
    base(c, tint=(150, 150, 160))
    tape(c, "NEW YORK LISTINGS", 540, 560, 54, -3, pop_k(t, L0("d3"), 0.25), seed=32)
    for i, (x, y, r) in enumerate(((290, 900, -6), (770, 950, 5), (530, 1210, -2))):
        photo(c, x, y, 360, 240, False, r, 100 + i, pop_k(t, L0("d3") + 0.3 + i * 0.25, 0.3))
    stamp(c, "TERRIBLE", 540, 760, 90, -8, stamp_k(t, TW("d3", "terrible")), RED, 33)


def S_d4(c, t, n):
    base(c, tint=YEL)
    tape(c, "FLEW TO NEW YORK", 540, 560, 54, -3, pop_k(t, L0("d4"), 0.25), seed=34)
    camera(c, 300, 1050, 1.0, flash=max(0, 1 - abs(((t - TW("d4", "shot")) % 0.8) - 0.1) * 6) if t > TW("d4", "shot") else 0)
    k = pop_k(t, TW("d4", "shot"), 0.35)
    photo(c, 740, 1080, 380, 260, True, 4, 120, k)
    person(c, 560, 1440, 0.9, 5, INK, t, "hold", None, "happy")


def S_d5(c, t, n):
    base(c, tint=GRN)
    _chart(c, t, L0("d5"), [(170, 1220), (330, 1218), (490, 1222), (650, 1200), (780, 1000), (910, 820)], 1.0, GRN)
    if t > TW("d5", "doubled") - 0.1: arrow(c, 780, 1000, 910, 800, 0, GRN, 14, 53, 1.0, 46)
    stamp(c, "DOUBLED", 520, 900, 100, -8, stamp_k(t, TW("d5", "doubled")), DGRN, 35)
    text(c, "$ / WEEK", 270, 800, 44, INK, BLK_F)


def S_d6(c, t, n):
    base(c, tint=PNK)
    k = pop_k(t, L0("d6"), 0.35)
    if k > 0:
        c.save(); c.translate(540, 1300); c.scale(k, k); ink(c, wpoly([(-200, 0), (0, -170), (200, 0), (150, 0), (150, 140), (-150, 140), (-150, 0)], 40, 2, True, 50), PNK, 9)
        ink(c, wrrect(-45, 30, 45, 140, 6, 41, 1), WHITE, 7); c.restore()
    tape(c, "AIRBNB TODAY", 540, 600, 60, -3, pop_k(t, L0("d6"), 0.25), seed=36)
    title(c, "TENS OF BILLIONS", 540, 830, 100, DGRN, pop_k(t, TW("d6", "billions") - 0.15, 0.3), -2, BLK_F)
    char(c, "mattress", 220, 1440, 0.55, t, 0, (0.6, -0.5), "happy", "cheer", blink=blink(t))
    char(c, "box", 870, 1440, 0.5, t, 0, (-0.6, -0.5), "happy", "cheer", blink=blink(t, 3), **CEREAL)


# ---------------------------------------------------------------- lesson + CTA
def S_t1(c, t, n):
    base(c)
    for i, (w_, x, y) in enumerate((("NEW APP", 280, 700), ("AD CAMPAIGN", 760, 780))):
        k = pop_k(t, L0("t1") + i * 0.5, 0.25)
        if k > 0: tape(c, w_, x, y, 50, (-4, 4)[i], k, seed=40 + i, col=GREY); strike(c, x - 170, y, x + 170, pr(t, L0("t1") + 0.25 + i * 0.5, 0.25))
    photo(c, 540, 1130, 420, 280, True, -3, 130, pop_k(t, TW("t1", "photos") - 0.1, 0.3))
    tape(c, "JUST BETTER PHOTOS", 540, 920, 52, 2, pop_k(t, TW("t1", "photos") - 0.1, 0.25), seed=42, col=GRN)


def S_t2(c, t, n):
    base(c, tint=YEL)
    k = pop_k(t, TW("t2", "essay") - 0.15, 0.3)
    if k > 0:
        c.save(); c.translate(540, 1080); c.scale(k, k); ink(c, wrrect(-260, -300, 260, 300, 10, 140, 2), WHITE, 9)
        for j in range(9): wline(c, [(-210, -150 + j * 50), (210 - (j % 3) * 60, -150 + j * 50)], 141 + j, 5, GREY)
        f = font(BLK_F, 34); c.drawString("ESSAY", -f.measureText("ESSAY") / 2, -220, f, P(INK)); c.restore()
    title(c, "DO THINGS THAT", 540, 640, 84, INK, pop_k(t, TW("t2", "Do") - 0.1, 0.3))
    title(c, "DON'T SCALE", 540, 770, 104, RED, pop_k(t, TW("t2", "scale") - 0.2, 0.3))


def S_e1(c, t, n):
    base(c)
    tape(c, "TRY IT NEXT TIME", 540, 540, 58, -3, pop_k(t, TW("e1", "Try") - 0.1, 0.25), seed=43)
    checklist(c, 540, 620, ["Do one thing by hand", "...that big companies won't"], [pr(t, TW("e1", "hand") - 0.05, 0.4), pr(t, TW("e1", "won't") - 0.05, 0.4)])
    char(c, "mattress", 800, 1440, 0.5, t, 0, (-0.5, -0.5), "happy", "cheer", blink=blink(t))


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "mattress", 320, 1440, 0.95, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t))
    char(c, "box", 790, 1440, 0.8, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3), **CEREAL)
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=33)
        bubble(c, "the friend who has a stuck side hustle", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 60, 700)
    else:
        title(c, "WHICH STORY NEXT?", 540, 680, 96, RED, pop_k(t, L0("z2"), 0.3))
        tape(c, "COMMENT BELOW", 540, 840, 58, 3, pop_k(t, TW("z2", "Comment") - 0.1, 0.25), seed=34)


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
