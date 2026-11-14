# STANLEY CUP case study + 4 tricks to steal (15 Nov 2026). DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = [k for k in LINES if k not in ("z2",)]
_TR = {"i3": "whip", "a1": "whip", "a3": "pop", "b1": "whip", "b5": "pop", "b6": "pop", "c1": "whip", "c5": "pop", "d1": "whip", "d6": "pop", "t1": "whip",
       "s1": "pop", "s2": "pop", "s3": "pop", "s4": "pop", "e1": "pop", "z1": "pop"}
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.12, "chaching"), (TW("i1", "gave"), "stamp"), (TW("i2", "millions."), "pop"), (TW("i2", "four"), "stamp"), (TW("i3", "hundred"), "ding"),
        (TW("i4", "campers."), "pop"), (TW("i4", "Barely"), "buzz"), (TW("a1", "Quencher."), "pop"), (TW("a1", "barely"), "tick"),
        (TW("a2", "restocking"), "stamp"), (TW("a2", "marketing"), "stamp"), (L0("a3"), "boing"), (TW("b1", "three"), "pop"), (TW("b1", "loved"), "ding"),
        (TW("b2", "women."), "pop"), (TW("b3", "answer?"), "whoosh"), (TW("b3", "wholesale"), "stamp"), (TW("b4", "five"), "slam"),
        (TW("b4b", "penny"), "chaching"), (TW("b5", "Guess"), "tick"), (TW("b5", "Gone."), "stamp"), (L0("b6"), "boing"), (TW("c1", "Crocs."), "pop"),
        (TW("c2", "cool."), "ding"), (TW("c2", "forgotten"), "boing"), (TW("c3", "partners,"), "stamp"), (TW("c4", "colors"), "pop"), (TW("c4", "minutes."), "whoosh"),
        (TW("c5", "work?"), "tick"), (TW("c5", "seventy"), "chaching"), (TW("c6", "seven"), "chaching"), (TW("c6", "fifty"), "impact"),
        (TW("d1", "burned"), "slam"), (TW("d2", "ice"), "ding"), (TW("d3", "sixty"), "chaching"), (TW("d4", "replied."), "ding"), (TW("d4", "car."), "stamp"),
        (TW("d5", "never"), "pop"), (L0("d6"), "boing"), (TW("t1", "loved"), "ding"), (TW("s1", "one."), "stamp"), (TW("s1b", "didn't"), "boing"),
        (TW("s2", "two,"), "stamp"), (TW("s2", "link,"), "pop"), (TW("s2b", "clearly."), "stamp"), (TW("s3", "Third,"), "stamp"), (TW("s3", "leftovers."), "buzz"),
        (TW("s4", "last"), "stamp"), (TW("s4", "fast."), "whoosh"), (TW("e1", "ask"), "ding"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i1": "Would you pay $45 for a cup its own company almost gave up on?",
        "i2": "People bought millions. Here's how, then 4 tricks you can steal for your own product.",
        "i3": "Imagine you're running a bottle company that's over 100 years old.",
        "a1": "The cup's called the Quencher. It came out in 2016, and barely anyone noticed.",
        "a2": "By 2019, Stanley had stopped restocking it. Stopped marketing it too.",
        "a3": "Hello? Anyone? I hold 40 ounces of ice water, people.",
        "b4": "So they ordered 5,000 cups.",
        "b4b": "One founder's words: \"It took every penny that we had in the business account.\"",
        "c1": "In 2020, Stanley hired a new president from Crocs. Terence Reilly.",
        "c5": "Did it work? Before all this, Stanley sold about $70 million a year.",
        "c6": "Now jump to 2023. CNBC reported it was on track to top $750 million.",
        "d2": "Her words: \"It was in a fire yesterday and it still has ice in it.\"",
        "d3": "It got more than 60 million views. Honestly? You can't buy an ad like that.",
        "d5": "His words: \"We've never done this before and we'll probably never do this again.\"",
        "z2": "Would you pay $45 for one? Comment YES or NO."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
CUP_L = {"a3", "d6"}; FLASK_L = {"b6"}


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


def mth(t, ids):
    if not speaking(t, ids): return 0.0
    v = talk(t)
    return v / 3.0 if not isinstance(v, str) else (0.25 if v in ("vx", "rest", "vm") else 0.75)


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
    base(c, tint=MINT)
    char(c, "cup", 400, 1440, 1.2, t, 0, (0.5, -0.3), "worried" if t > TW("i1", "gave") - 0.1 else "happy", "shrug", blink=blink(t), col=MINT)
    tape(c, "$45", 740, 780, 110, 6, 1.0 + 0.06 * math.sin(t * 7) * (t < 1.5), seed=3, col=YEL)
    title(c, "FOR A CUP?!", 770, 950, 62, INK, 1.0, 4)
    stamp(c, "ALMOST GIVEN UP ON", 540, 600, 60, -4, stamp_k(t, TW("i1", "gave")), RED, 4)


def S_i2(c, t, n):
    base(c, tint=YEL)
    k = pr(t, TW("i2", "millions.") - 0.4, 0.9)
    cols = (MINT, LILAC, PEACH, PNK, SKY, MINT, LILAC, PEACH)
    for i in range(int(8 * k + 0.999)):
        char(c, "cup", 130 + i * 117, 1440 - (i % 2) * 30, 0.42, t + i * 0.2, 0, (0.3, -0.3), "happy", "cheer", walk=True, blink=blink(t, i), col=cols[i], shadow_w=0.5)
    title(c, "MILLIONS SOLD", 540, 640, 92, DGRN, pop_k(t, TW("i2", "millions.") - 0.1, 0.3), -3, BLK_F)
    tape(c, "THE STORY + 4 TRICKS", 540, 820, 54, 3, pop_k(t, TW("i2", "four") - 0.1, 0.25), seed=5)


def S_i3(c, t, n):
    base(c, tint=SKY)
    char(c, "flask", 330, 1440, 1.15, t, 0, (0.6, -0.2), "neutral", "hips", blink=blink(t))
    calendar(c, 760, 1060, "1913", 0.9, pop_k(t, TW("i3", "bottle") - 0.1, 0.3), 6, SLATE)
    tape(c, "100+ YEARS OLD", 700, 640, 58, -3, pop_k(t, TW("i3", "hundred") - 0.15, 0.25), seed=7)


def S_i4(c, t, n):
    base(c, tint=(200, 210, 220))
    char(c, "flask", 230, 1440, 0.9, t, 0, (0.6, 0), "happy", "down", blink=blink(t))
    k = pop_k(t, TW("i4", "workers") - 0.15, 0.3)
    if k > 0: c.save(); c.translate(560, 820); c.scale(k, k); hardhat(c, 0, 0, 0.9, 8); c.restore(); text(c, "WORKERS", 560, 900, 40, INK, BLK_F)
    k2 = pop_k(t, TW("i4", "campers.") - 0.15, 0.3)
    if k2 > 0: c.save(); c.translate(840, 860); c.scale(k2, k2); tent(c, 0, 0, 0.7, 9); c.restore(); text(c, "CAMPERS", 840, 920, 40, INK, BLK_F)
    if t > TW("i4", "new") - 0.2:
        char(c, "cup", 700, 1440, 0.75, t, 0, (-0.5, 0.3), "worried", "down", blink=blink(t, 2), col=MINT)
        stamp(c, "BARELY SELLING", 620, 620, 64, 5, stamp_k(t, TW("i4", "Barely")), RED, 10)


# ---------------------------------------------------------------- the forgotten cup
def S_a1(c, t, n):
    base(c, tint=MINT)
    char(c, "cup", 360, 1440, 1.05, t, 0, (0.4, -0.2), "happy", "hips", blink=blink(t), col=MINT)
    tape(c, "\"THE QUENCHER\" · 2016", 560, 600, 54, -3, pop_k(t, TW("a1", "Quencher.") - 0.2, 0.25), seed=11)
    k = pr(t, TW("a1", "barely") - 0.3, 0.9)
    if k > 0:
        wline(c, [(640, 1300), (640, 900)], 12, 7); wline(c, [(640, 1300), (950, 1300)], 13, 7)
        wline(c, [(660, 1270), (720, 1266), (790, 1272), (860, 1264), (930, 1268)][:max(2, int(5 * k))], 14, 10, RED, 1.2)
        text(c, "SALES", 790, 880, 38, INK, BLK_F)


def S_a2(c, t, n):
    base(c, tint=(200, 200, 206))
    ink(c, wrrect(120, 1180, 960, 1210, 8, 15, 1.4), BROWN, 8)
    char(c, "cup", 540, 1180, 0.65, t, 0, (0, 0.4), "worried", "down", blink=blink(t), col=MINT, shadow_w=0.0)
    tape(c, "2019", 540, 560, 64, 3, pop_k(t, TW("a2", "nineteen,") - 0.2, 0.25), seed=16, col=YEL)
    stamp(c, "NO RESTOCKS", 330, 760, 62, -6, stamp_k(t, TW("a2", "restocking")), RED, 17)
    stamp(c, "NO ADS", 760, 820, 66, 6, stamp_k(t, TW("a2", "marketing")), RED, 18)


def S_a3(c, t, n):
    base(c, tint=(190, 196, 210))
    char(c, "cup", 540, 1440, 1.2, t, mth(t, CUP_L), (0, -0.3), "worried", "wave", blink=blink(t), col=MINT, ice=True)
    bubble(c, "Hello? Anyone? I hold 40 ounces of ice water, people.", 540, 620, pop_k(t, L0("a3"), 0.25), (-60, 200), 54, 760)


# ---------------------------------------------------------------- the bloggers
def S_b1(c, t, n):
    base(c, tint=PNK)
    blog_window(c, 540, 840, 1.0, pop_k(t, TW("b1", "blog") - 0.2, 0.3), 20, t=t)
    for i in range(3):
        if t > TW("b1", "three") - 0.2 + i * 0.12: person(c, 220 + i * 320, 1440, 0.95, 21 + i, (PUR, ORG, BLU)[i], t, "up" if t > TW("b1", "loved") - 0.1 else "stand", None, "happy", (0, 0), "long")
    tape(c, "3 BLOGGERS", 540, 580, 52, -3, pop_k(t, TW("b1", "three"), 0.25), seed=24, col=YEL)


def S_b2(c, t, n):
    base(c, tint=PNK)
    pie(c, 360, 1080, 230, 0.977, pr(t, TW("b2", "following") - 0.2, 0.8), 25, (PNK, GREY))
    text(c, "WOMEN", 330, 1040, 46, WHITE, BLK_F) if t > TW("b2", "women.") - 0.2 else None
    tape(c, "RETAIL DIVE: ~ALL WOMEN", 540, 600, 46, -2, pop_k(t, TW("b2", "Retail") - 0.1, 0.25), seed=26)
    if t > TW("b2", "crowd") - 0.3:
        char(c, "flask", 800, 1440, 0.62, t, 0, (-1, 0), "worried", "shrug", blink=blink(t))
        tape(c, "NOT THEIR USUAL BUYER", 740, 780, 36, 3, pop_k(t, TW("b2", "crowd") - 0.1, 0.25), seed=27, col=YEL)


def S_b3(c, t, n):
    base(c, tint=SKY)
    person(c, 230, 1440, 1.05, 22, ORG, t, "hold", "THE BUY GUIDE", "happy", (1, 0), "long")
    char(c, "flask", 820, 1440, 0.85, t, 0, (-1, 0), "neutral", "point", blink=blink(t))
    bubble(c, "Keep making it?", 330, 680, pop_k(t, L0("b3"), 0.25), (-60, 200), 50, 420)
    bubble(c, "Order wholesale. Sell them yourselves.", 690, 900, pop_k(t, TW("b3", "answer?") - 0.1, 0.25), (120, 160), 46, 460)


def S_b4(c, t, n):
    base(c, tint=YEL)
    crates(c, 540, 1440, 5, 4, pr(t, L0("b4"), 1.4), 30)
    title(c, "5,000 CUPS", 540, 640, 110, INK, pop_k(t, TW("b4", "five") - 0.1, 0.3), -3, BLK_F)


def S_b4b(c, t, n):
    base(c, tint=YEL)
    person(c, 260, 1440, 1.25, 22, ORG, t, "head", "ONE CO-FOUNDER", "worried", (1, 0), "long")
    wallet(c, 760, 1250, 0.8, 31, open_=pr(t, TW("b4b", "penny") - 0.2, 0.4))
    bubble(c, "\"It took every penny that we had in the business account.\"", 640, 720, pop_k(t, L0("b4b") + 0.2, 0.25), (-220, 220), 46, 640)


def S_b5(c, t, n):
    base(c, tint=GRN)
    gone = int(20 * pr(t, TW("b5", "few") - 0.2, 1.0))
    crates(c, 540, 1440, 5, 4, 1.0, 30, gone=gone)
    stopwatch(c, 820, 760, 0.7, 32, t, pop_k(t, TW("b5", "Guess") - 0.1, 0.25))
    tape(c, "A FEW DAYS", 300, 640, 60, -4, pop_k(t, TW("b5", "few") - 0.1, 0.25), seed=33, col=YEL)
    stamp(c, "SOLD OUT", 540, 1000, 110, -7, stamp_k(t, TW("b5", "Gone.")), RED, 34)


def S_b6(c, t, n):
    base(c, tint=SKY)
    char(c, "flask", 540, 1440, 1.25, t, mth(t, FLASK_L), (0, -0.3), "shock", "shrug", blink=blink(t))
    bubble(c, "Wait. Women want our cups? Why didn't anybody tell me?", 540, 600, pop_k(t, L0("b6"), 0.25), (-40, 210), 54, 760)


# ---------------------------------------------------------------- the turnaround
def S_c1(c, t, n):
    base(c, tint=(150, 210, 120))
    person(c, 330, 1440, 1.35, 40, (60, 60, 70), t, "wave", "TERENCE REILLY", "happy", (1, 0))
    tape(c, "NEW PRESIDENT · 2020", 600, 600, 52, -3, pop_k(t, TW("c1", "twenty,") - 0.2, 0.25), seed=41)
    k = pop_k(t, TW("c1", "Crocs.") - 0.2, 0.3)
    if k > 0: c.save(); c.translate(760, 1200); c.scale(k, k); clog(c, 0, 0, 0.9, 42, ORG); c.restore(); tape(c, "FROM CROCS", 760, 1000, 44, 4, k, seed=43, col=YEL)


def S_c2(c, t, n):
    base(c, tint=(150, 210, 120))
    clog(c, 300, 1100, 1.0, 44, ORG)
    if t > TW("c2", "cool.") - 0.2:
        for j in range(4): a = j * math.pi / 2 + t * 2; wline(c, [(300 + 220 * math.cos(a), 1040 + 120 * math.sin(a)), (300 + 260 * math.cos(a), 1040 + 140 * math.sin(a))], 45 + j, 9, YEL)
        title(c, "COOL!", 300, 800, 96, DGRN, pop_k(t, TW("c2", "cool."), 0.3), -6)
    if t > TW("c2", "forgotten") - 0.3:
        char(c, "cup", 780, 1440, 0.7, t, 0, (-0.5, -0.3), "shock", "shrug", blink=blink(t), col=MINT)
        title(c, "?", 860, 860, 150, RED, pop_k(t, TW("c2", "forgotten"), 0.3), 8, BLK_F)


def S_c3(c, t, n):
    base(c, tint=YEL)
    person(c, 220, 1440, 1.0, 40, (60, 60, 70), t, "hold", None, "happy", (1, 0))
    for i in range(3): person(c, 560 + i * 170, 1440, 0.85, 21 + i, (PUR, ORG, BLU)[i], t, "hold" if i == 0 else "stand", None, "happy", (-1, 0), "long")
    stamp(c, "PARTNERS", 540, 640, 96, -5, stamp_k(t, TW("c3", "partners,")), DGRN, 47)
    tape(c, "NOT JUST CUSTOMERS", 540, 820, 46, 3, pop_k(t, TW("c3", "customers.") - 0.2, 0.25), seed=48, col=YEL)


def S_c4(c, t, n):
    base(c, tint=LILAC)
    swatch_fan(c, 300, 1250, (MINT, LILAC, PEACH, PNK, SKY, YEL, RED), pr(t, TW("c4", "colors") - 0.3, 1.0), 50)
    for i, col in enumerate((PEACH, PNK, SKY)):
        if t > TW("c4", "Limited") - 0.2 + i * 0.15: char(c, "cup", 640 + i * 130, 1440, 0.45, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t, i), col=col, shadow_w=0.5)
    tape(c, "LIMITED COLORS", 540, 600, 56, -3, pop_k(t, TW("c4", "colors") - 0.1, 0.25), seed=51)
    stamp(c, "OFTEN SOLD OUT IN MINUTES", 600, 820, 48, 4, stamp_k(t, TW("c4", "minutes.")), RED, 52)


def bars(c, t, k70, k750):
    wline(c, [(150, 1340), (150, 820)], 60, 8); wline(c, [(150, 1340), (940, 1340)], 61, 8)
    ink(c, wpoly([(240, 1340), (240, 1340 - 46 * k70), (440, 1340 - 46 * k70), (440, 1340)], 62, 2, True, 40), GREY, 9) if k70 > 0.02 else None
    text(c, "~$70M / YR", 340, 1280 - 46 * k70, 40, INK, BLK_F) if k70 > 0.5 else None
    text(c, "BEFORE", 340, 1400, 36, INK, BLK_F)
    if k750 > 0.02:
        h = 500 * ease(k750); ink(c, wpoly([(620, 1340), (620, 1340 - h), (820, 1340 - h), (820, 1340)], 63, 2, True, 40), MINT, 9)
        text(c, "2023", 720, 1400, 36, INK, BLK_F)


def S_c5(c, t, n):
    base(c, tint=GRN)
    bars(c, t, pr(t, TW("c5", "seventy") - 0.2, 0.5), 0)
    title(c, "DID IT WORK?", 540, 640, 92, INK, pop_k(t, L0("c5"), 0.3), -3, BLK_F)


def S_c6(c, t, n):
    base(c, tint=GRN)
    bars(c, t, 1.0, pr(t, TW("c6", "track") - 0.3, 0.9))
    title(c, "$750M+", 620, 760, 110, DGRN, pop_k(t, TW("c6", "seven") - 0.1, 0.3), -3, BLK_F)
    tape(c, "ON TRACK, SAYS CNBC", 540, 600, 46, 2, pop_k(t, TW("c6", "CNBC") - 0.1, 0.25), seed=64, col=YEL)


# ---------------------------------------------------------------- the car
def S_d1(c, t, n):
    base(c, tint=(255, 200, 150))
    car(c, 600, 1440, 1.0, 70, pr(t, TW("d1", "burned") - 0.3, 0.4), t)
    person(c, 170, 1440, 0.95, 71, PUR, t, "hold", "DANIELLE", "worried", (1, 0), "long")
    phone(c, 280, 1170, 0.28, 72)
    tape(c, "NOVEMBER 2023", 540, 600, 56, -3, pop_k(t, L0("d1"), 0.25), seed=73)


def S_d2(c, t, n):
    base(c, tint=(255, 200, 150))
    char(c, "cup", 330, 1440, 1.05, t, 0, (0.4, -0.3), "happy", "cheer", blink=blink(t), col=MINT, soot=1.0, ice=t > TW("d2", "ice") - 0.3)
    bubble(c, "\"It was in a fire yesterday and it still has ice in it.\"", 700, 760, pop_k(t, TW("d2", "it") - 0.1, 0.25), (-200, 240), 48, 560)


def S_d3(c, t, n):
    base(c, tint=PNK)
    k = pr(t, TW("d3", "sixty") - 0.4, 0.7)
    for i in range(int(12 * k)):
        x = 150 + (i % 6) * 156; y = 1330 - (i // 6) * 260
        phone(c, x, y, 0.42, 400 + i)
    title(c, "60,000,000+ VIEWS", 540, 640, 74, RED, pop_k(t, TW("d3", "sixty"), 0.3), -3, BLK_F)
    tape(c, "YOU CAN'T BUY THAT AD", 540, 800, 46, 3, pop_k(t, TW("d3", "Honestly?") - 0.1, 0.25), seed=75, col=YEL)


def S_d4(c, t, n):
    base(c, tint=SKY)
    person(c, 220, 1440, 1.1, 40, (60, 60, 70), t, "wave", "TERENCE REILLY", "happy", (1, 0))
    tape(c, "HIS OFFER", 600, 580, 56, -3, pop_k(t, TW("d4", "offered") - 0.1, 0.25), seed=76)
    for i, col in enumerate((MINT, PEACH)):
        if t > TW("d4", "cups,") - 0.2 + i * 0.1: char(c, "cup", 470 + i * 120, 1000, 0.36, t, 0, (0, -0.3), "happy", "cheer", blink=False, col=col, shadow_w=0.0)
    k = pop_k(t, TW("d4", "car.") - 0.2, 0.3)
    if k > 0: c.save(); c.translate(720, 1440); c.scale(0.62 * k, 0.62 * k); car(c, 0, 0, 1.0, 77, 0.0, t, PEACH); c.restore()
    title(c, "NEW CUPS + A NEW CAR", 600, 760, 56, DGRN, pop_k(t, TW("d4", "car."), 0.3), 2, BLK_F)


def S_d5(c, t, n):
    base(c, tint=SKY)
    person(c, 260, 1440, 1.3, 40, (60, 60, 70), t, "stand", "TERENCE REILLY", "happy", (1, 0))
    bubble(c, "\"We've never done this before and we'll probably never do this again.\"", 660, 740, pop_k(t, TW("d5", "we've") - 0.1, 0.25), (-240, 260), 46, 580)


def S_d6(c, t, n):
    base(c, tint=YEL)
    char(c, "cup", 540, 1440, 1.25, t, mth(t, CUP_L), (0, -0.3), "happy", "hips", blink=blink(t), col=MINT, soot=0.6, ice=True)
    bubble(c, "I just did my job, and kept the ice cold.", 540, 620, pop_k(t, L0("d6"), 0.25), (-40, 200), 58, 700)


def S_t1(c, t, n):
    base(c, tint=MINT)
    title(c, "WHAT SAVED IT?", 540, 600, 84, INK, pop_k(t, L0("t1"), 0.3), -3, BLK_F)
    char(c, "cup", 540, 1440, 0.8, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t), col=MINT)
    for i, x in enumerate((170, 330, 750, 910)):
        if t > TW("t1", "people") - 0.3 + i * 0.1: person(c, x, 1440, 0.7, 80 + i, (PUR, ORG, BLU, PNK)[i], t, "up", None, "happy", (0, 0), "long" if i % 2 else "short")
    tape(c, "THE PEOPLE WHO LOVED IT", 540, 780, 50, 3, pop_k(t, TW("t1", "loved") - 0.2, 0.25), seed=85, col=YEL)


# ---------------------------------------------------------------- 4 tricks
def trick(c, t, t0, num, label, col):
    stamp(c, f"TRICK {num}", 540, 590, 90, (-5, 4, -3, 5)[num - 1], stamp_k(t, t0), col, 100 + num)
    tape(c, label, 540, 750, 48, (3, -3, 2, -2)[num - 1], pop_k(t, t0 + 0.25, 0.25), seed=101 + num)


def heart(c, x, y, r, col=RED):
    h = skia.Path(); h.moveTo(x, y); h.cubicTo(x - r, y - r, x - 2 * r, y + 0.3 * r, x, y + 1.3 * r); h.cubicTo(x + 2 * r, y + 0.3 * r, x + r, y - r, x, y); c.drawPath(h, P(col)); c.drawPath(h, S(INK, 5))


def S_s1(c, t, n):
    base(c, tint=YEL)
    trick(c, t, TW("s1", "one."), 1, "FIND YOUR SUPERFANS", BLU)
    for i in range(3):
        person(c, 230 + i * 310, 1440, 0.8, 21 + i, (PUR, ORG, BLU)[i], t, "up" if i == 1 else "stand", None, "happy", (0, 0), "long")
        if t > TW("s1", "obsessed") - 0.2 + i * 0.1: heart(c, 230 + i * 310, 1000 + 12 * math.sin(t * 4 + i), 34)
    tape(c, "AND LISTEN", 760, 900, 44, 4, pop_k(t, TW("s1", "listen") - 0.1, 0.25), seed=110, col=YEL) if "listen" in str(_VL.get("s1")) else None


def S_s1b(c, t, n):
    base(c, tint=YEL)
    for i in range(3):
        person(c, 200 + i * 220, 1440, 0.85, 21 + i, (PUR, ORG, BLU)[i], t, "stand", None, "happy", (1, 0), "long")
    megaphone(c, 760, 1100, 0.9, -10, 111, "", pop_k(t, L0("s1b"), 0.3), PNK)
    title(c, "BEST MARKETERS:", 540, 600, 70, INK, pop_k(t, TW("s1b", "marketers") - 0.1, 0.3), -3, BLK_F)
    stamp(c, "NOT ON STAFF", 540, 760, 70, 4, stamp_k(t, TW("s1b", "didn't")), RED, 112)


def S_s2(c, t, n):
    base(c, tint=PNK)
    trick(c, t, TW("s2", "two,"), 2, "LET FANS SELL IT", ORG)
    link_chain(c, 540, 1060, 1.0, 120, pop_k(t, TW("s2", "affiliate") - 0.1, 0.3))
    for i in range(4):
        u = pr(t, TW("s2", "share") - 0.2 + i * 0.1, 0.5)
        if u > 0: ink(c, wellipse(540 + (i - 1.5) * 200 * u, 1300, 44, 44, 121 + i, 1.4), YEL, 7); text(c, "$", 540 + (i - 1.5) * 200 * u, 1318, 46, INK, BLK_F)
    tape(c, "MY TIP: AFFILIATE LINKS", 540, 880, 40, -2, pop_k(t, TW("s2", "tip.") - 0.1, 0.25), seed=122, col=YEL)


def S_s2b(c, t, n):
    base(c, tint=PNK)
    k = pop_k(t, L0("s2b"), 0.3)
    if k > 0:
        c.save(); c.translate(540, 1150); c.scale(k, k); ink(c, wrrect(-300, -230, 300, 230, 16, 123, 2), WHITE, 9)
        text(c, "US RULE (FTC)", 0, -150, 44, INK, BLK_F); text(c, "PAID? GIFTED?", 0, -60, 58, INK, BLK_F); text(c, "SAY SO, CLEARLY", 0, 20, 58, RED, BLK_F)
        text(c, "\"I earn from this link\"", 0, 120, 40, INK, HAND_F); c.restore()
    stamp(c, "#AD", 820, 700, 90, 8, stamp_k(t, TW("s2b", "clearly.")), RED, 124)


def S_s3(c, t, n):
    base(c, tint=(150, 200, 230))
    trick(c, t, TW("s3", "Third,"), 3, "SMALL BATCHES", RED)
    for i, col in enumerate((PEACH, LILAC)):
        char(c, "cup", 220 + i * 160, 1440, 0.45, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t, i), col=col, shadow_w=0.5)
    stamp(c, "SOLD OUT", 300, 1000, 56, -6, stamp_k(t, TW("s3", "sells") + 0.1), DGRN, 130)
    if t > TW("s3", "warehouse") - 0.3:
        crates(c, 760, 1440, 2, 4, 1.0, 131, "LEFT")
        strike(c, 600, 1180, 920, pr(t, TW("s3", "leftovers.") - 0.1, 0.3))


def S_s4(c, t, n):
    base(c, tint=SKY)
    trick(c, t, TW("s4", "last"), 4, "ANSWER FAST", DGRN)
    phone(c, 330, 1180, 0.7, 140)
    stopwatch(c, 760, 1150, 0.9, 141, t * 2, pop_k(t, TW("s4", "viral,") - 0.1, 0.3))
    tape(c, "DAYS, NOT MONTHS", 560, 1460 - 60, 44, 3, pop_k(t, TW("s4", "days.") - 0.1, 0.25), seed=142, col=YEL)


def S_e1(c, t, n):
    base(c, tint=YEL)
    tape(c, "TRY IT NEXT TIME", 540, 560, 58, -3, pop_k(t, TW("e1", "Try") - 0.1, 0.25), seed=150)
    title(c, "WHO ALREADY", 540, 740, 80, INK, pop_k(t, TW("e1", "Who") - 0.1, 0.3))
    title(c, "LOVES YOUR THING?", 540, 850, 76, RED, pop_k(t, TW("e1", "loves") - 0.1, 0.3))
    person(c, 330, 1440, 1.0, 151, ORG, t, "wave", None, "happy", (1, 0))
    if t > TW("e1", "ask") - 0.2: bubble(c, "Go ask them!", 760, 1080, pop_k(t, TW("e1", "ask") - 0.1, 0.25), (-160, 140), 50, 360)


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "cup", 300, 1440, 0.85, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t), col=MINT)
    char(c, "flask", 790, 1440, 0.8, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3))
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=160)
        bubble(c, "the friend who never leaves home without a giant cup", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 52, 720)
    else:
        title(c, "WOULD YOU PAY $45?", 520, 660, 70, INK, pop_k(t, L0("z2"), 0.3))
        stamp(c, "YES", 360, 840, 90, -6, stamp_k(t, TW("z2", "YES")), DGRN, 161)
        stamp(c, "NO", 720, 840, 90, 6, stamp_k(t, TW("z2", "NO.")), RED, 162)


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
    strip(c, spoken_words(t), True, 262, 42, t)
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
