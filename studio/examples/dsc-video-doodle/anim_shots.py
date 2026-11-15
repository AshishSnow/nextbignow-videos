# DOLLAR SHAVE CLUB "$4,500 video" — trend + case study + 4 moves to start. DOODLE look.
# 15 Nov upgrade (owner's reference reel): ONE SET PER SECTION that evolves beat by beat (props pop in, red-marker ticks/strikes/circles),
# a recurring plain "YOU" stick character, chunked highlighted subtitles, big title cover on frame 0.
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


# section sets: (shot id, first line, transition)
_SECT = [("S_hook", "i1", "cut"), ("S_dubin", "a1", "whip"), ("S_fancy", "a3", "pop"), ("S_how", "a4", "whip"), ("S_video", "b1", "whip"),
         ("S_dollar", "b4", "pop"), ("S_cost", "b5", "pop"), ("S_launch", "c1", "whip"), ("S_night", "c5", "pop"), ("S_result", "c7", "whip"),
         ("S_rich", "c9", "pop"), ("S_myth", "t1", "whip"), ("S_moves", "s1", "whip"), ("S_end", "e1", "whip"), ("S_z", "z1", "pop")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "billion-dollar"), "chaching"), (L0("i2"), "pop"), (TW("i2", "tiny"), "buzz"), (TW("i3", "Nobody"), "pop"),
        (TW("i3", "forty-five"), "chaching"), (TW("i4", "four"), "stamp"), (L0("a1"), "pop"), (TW("a1", "improv"), "ding"), (TW("a2", "party,"), "pop"),
        (TW("a2", "warehouse"), "ding"), (L0("a3"), "boing"), (TW("a4", "one,"), "stamp"), (TW("a4", "online."), "tick"), (TW("a5", "two,"), "stamp"),
        (TW("a5", "mailbox."), "whoosh"), (TW("a6", "dollar"), "chaching"), (TW("a6", "shipping."), "pop"), (TW("a7", "three"), "tick"),
        (TW("a7", "coffee."), "ding"), (TW("b1", "fortune?"), "buzz"), (TW("b2", "funny"), "pop"), (TW("b2", "himself."), "ding"),
        (TW("b3", "directed,"), "slam"), (TW("b3b", "eight"), "tick"), (L0("b4"), "boing"), (TW("b5", "forty-five"), "chaching"),
        (TW("c1", "March"), "stamp"), (TW("c1", "live."), "whoosh"), (TW("c2", "crashed"), "slam"), (TW("c3", "upside?"), "ding"),
        (TW("c3", "six"), "stamp"), (TW("c4", "catch?"), "buzz"), (TW("c5", "thousands"), "tick"), (TW("c6", "fence."), "whoosh"),
        (TW("c7", "twelve"), "chaching"), (TW("c8", "Unilever"), "stamp"), (TW("c8", "billion"), "chaching"), (TW("c8b", "three"), "pop"),
        (L0("c9"), "boing"), (TW("t1", "Nope."), "stamp"), (TW("t2", "clear"), "tick"), (TW("t2", "funny"), "tick"), (TW("t2", "guts"), "tick"),
        (TW("s2", "one."), "stamp"), (TW("s3", "two."), "stamp"), (TW("s4", "three."), "stamp"), (TW("s5", "four,"), "stamp"),
        (TW("s5b", "six"), "buzz"), (TW("e1", "shot."), "ding"), (TW("e2", "friend."), "whoosh"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("A $4,500 homemade video helped build a", "BILLION-DOLLAR RAZOR CLUB?")   # (kicker, TITLE) on frame 0 = the grid cover
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i3": "Imagine you're him. Nobody knows your name, and you bet your whole launch on one $4,500 video.",
        "i4": "Here's what happened. Then 4 moves you can steal for your own launch.",
        "a6": "The cheapest plan? $1 a month, plus $2 for shipping.", "a7": "So about $3. That's less than 1 fancy coffee.",
        "b3b": "Start to finish, in about 8 hours.", "b5": "Did it cost a fortune? Dubin told Fortune magazine, \"I spent about $4,500 on it.\"",
        "c1": "On March 6, 2012, the video went live.", "c3": "The upside? People wanted it, badly. They ran out of razors in 6 hours.",
        "c7": "Was it just a fluke? Within days, about 12,000 people had signed up.",
        "c8": "4 years later, Unilever bought the company. Reportedly for about $1 billion.", "c8b": "Members by then? Over 3 million.",
        "c9": "$1 billion, for a razor that costs $1? I'll take it.", "s1": "So how could you do this for your own launch? 4 moves.",
        "s2": "Move 1. Explain your idea in 1 sentence a 10-year-old gets.", "s2b": "His was simple. Good blades, $1 a month.",
        "s3": "Move 2. Be the face. You don't need actors, you need your own personality.",
        "s4": "Move 3. Shoot it cheap, in your real space, with friends who are funny.",
        "s5": "And move 4, the one everybody forgets. Get ready for it to actually work.",
        "s5b": "Stock up and plan your shipping first, because remember, they sold out in just 6 hours."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
FANCY_L = {"a3"}; DOLLAR_L = {"b4", "c9"}
YOU = (58, 196, 104)


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
        if a_ < n <= b_: hl = set(_HL.get(cur, set())) | {re.sub(r"[^a-z0-9$%]", "", x.lower()) for x in d if any(ch.isdigit() for ch in x)}; return d[a_:n], hl
    return [], set()


def speaking(t, ids): return any(LINES[i]["start"] <= t <= LINES[i]["end"] + 0.05 for i in ids if i in LINES)


def mth(t, ids): return talk(t) / 3.0 if speaking(t, ids) else 0.0


def blink(t, seed=0): return (int(t * 12 + seed * 7) % 43) in (0, 1)


def base(c, tint=None, gy=1440):
    page(c, tint); ground(c, gy)


def title(c, s, x, y, size, col=INK, k=1.0, rot=-2, fnt=MARK_F):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k); text(c, s, 0, 0, size, col, fnt, maxw=860); c.restore()


def at(t, lid, w=None, off=0.0): return t >= (TW(lid, w) if w else L0(lid)) + off


def pk(t, lid, w=None, off=-0.1, d=0.3): return pop_k(t, (TW(lid, w) if w else L0(lid)) + off, d)


def sk(t, lid, w=None, off=0.0): return stamp_k(t, (TW(lid, w) if w else L0(lid)) + off)


def person(c, x, y, s=1.0, seed=0, col=BLU, t=0.0, pose="stand", name=None, mood="neutral", look=(0, 0), hair="short", k=1.0):
    """plain doodle person (no likeness): round head with dot eyes, stick body; name on a tape. k = pop scale."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k); c.translate(-x, -y)
    hy = y - 230 * s
    wline(c, [(x, hy + 50 * s), (x, y - 90 * s)], seed, 9 * s)
    for sx in (-1, 1): limb(c, x, y - 90 * s, x + sx * 34 * s, y, 6 * sx * s, 8, False, seed + sx, foot=True, s=s)
    arms = {"stand": ((-50, 80), (50, 80)), "up": ((-80, -80), (80, -80)), "head": ((-40, -110), (40, -110)), "hold": ((60, 20), (90, 10)),
            "wave": ((-50, 80), (90, -60 + 20 * math.sin(t * 9))), "point": ((-50, 80), (110, -30)), "shrug": ((-80, -20), (80, -20))}[pose]
    for (dx, dy), sd in zip(arms, (1, 2)): limb(c, x, y - 160 * s, x + dx * s, y - 160 * s + dy * s, 14 * s, 8, True, seed + sd, s=s)
    if hair == "long": ink(c, wpoly([(x - 66 * s, hy - 20 * s), (x + 66 * s, hy - 20 * s), (x + 74 * s, hy + 110 * s), (x - 74 * s, hy + 110 * s)], seed + 9, 1.6, True, 40), col, 7 * s)
    ink(c, wellipse(x, hy, 52 * s, 56 * s, seed + 4, 1.5), (255, 224, 196), 8 * s)
    eyes(c, x + look[0] * 6 * s, hy - 6 * s, s * 0.5, look, blink(t, seed), 40, 22, mood, seed + 5)
    mouth(c, x, hy + 26 * s, s * 0.45, 0, mood, seed + 6)
    if hair == "short": ink(c, wpoly([(x - 54 * s, hy - 20 * s), (x - 40 * s, hy - 60 * s), (x, hy - 64 * s), (x + 44 * s, hy - 56 * s), (x + 54 * s, hy - 24 * s), (x + 30 * s, hy - 44 * s), (x - 30 * s, hy - 44 * s)], seed + 7, 1.2, True, 30), col, 6 * s)
    elif hair == "bald": pass
    if name: tape(c, name, x, y + 46, 34, (-3, 3)[seed % 2], 1.0, seed=seed)
    c.restore()


def you(c, x, y, t, s=1.0, pose="stand", mood="neutral", look=(0, 0), k=1.0):
    """the recurring viewer stand-in (green shirt, name tape YOU)."""
    person(c, x, y, s, 777, YOU, t, pose, "YOU", mood, look, "short", k)


def dubin(c, x, y, t, s=1.0, pose="stand", mood="happy", look=(0, 0), name="MICHAEL DUBIN", k=1.0):
    person(c, x, y, s, 12, (90, 60, 40), t, pose, name, mood, look, "short", k)


def crate(c, x, y, s=1.0, seed=700, label="BLADES"):
    c.save(); c.translate(x, y); c.scale(s, s)
    ink(c, wrrect(-120, -180, 120, 0, 8, seed, 1.6), TAN, 8)
    for j in range(2): wline(c, [(-110, -120 + j * 60), (110, -120 + j * 60)], seed + j, 5, shade(TAN, 0.7))
    if label: text(c, label, 0, -78, 30, INK, BLK_F)
    c.restore()


def warehouse_bg(c, seed=710, empty=False):
    """big warehouse wall with roller door + stacked crates (one evolving backdrop)."""
    ink(c, wpoly([(90, 1440), (90, 760), (540, 620), (990, 760), (990, 1440)], seed, 2.4, True, 60), (226, 220, 206), 9)
    ink(c, wrrect(330, 1040, 750, 1440, 10, seed + 1, 1.6), GREY, 8)
    for j in range(7): wline(c, [(345, 1080 + j * 50), (735, 1080 + j * 50)], seed + 2 + j, 4, shade(GREY, 0.75))
    if not empty:
        for i, (x, y) in enumerate(((200, 1440), (200, 1260), (880, 1440), (880, 1260), (880, 1080))): crate(c, x, y, 0.8, seed + 10 + i)


# ---------------------------------------------------------------- hook (i1-i4): one evolving set
def S_hook(c, t, n):
    base(c, tint=YEL)
    # camcorder on a tripod (the cheap video), right; YOU joins on i2; crates + wallet on i3
    c.save(); c.translate(740, 1440)
    for dx in (-90, 0, 90): wline(c, [(0, -330), (dx, 0)], 720 + dx, 8)
    c.restore(); camera(c, 740, 1060, 1.1, 721, 1.0 if 0.2 < (t % 2.4) < 0.3 else 0.0)
    if t < COVER_T + 0.2:
        return
    stamp(c, "$1 BILLION?", 740, 760, 80, -6, sk(t, "i1", "billion-dollar", 0.2) if t < L0("i2") else 1.0, RED, 722)
    if at(t, "i2", None, -0.1):
        you(c, 300, 1440, t, 1.25, "shrug" if t < L0("i3") else "head", "worried", (1, 0), pk(t, "i2"))
        if not at(t, "i3", "Nobody", -0.2): bubble(c, "On a tiny budget?", 330, 760, pk(t, "i2", "tiny", -0.2), (-20, 200), 50, 420, think=True)
    if at(t, "i3", "Nobody", -0.2):
        tape(c, "NOBODY KNOWS YOU", 370, 800, 42, 3, pk(t, "i3", "Nobody"), seed=723, col=GREY)
    if at(t, "i3", "forty-five", -0.2):
        tape(c, "1 VIDEO · $4,500", 740, 900, 46, 4, pk(t, "i3", "forty-five"), seed=724)
    if at(t, "i4", "four", -0.2):
        title(c, "+ 4 MOVES TO STEAL", 540, 560, 74, DGRN, pk(t, "i4", "four"), -3)


# ---------------------------------------------------------------- Dubin + the blades (a1-a2)
def S_dubin(c, t, n):
    base(c, tint=SKY)
    dubin(c, 300, 1440, t, 1.4, "wave" if t < TW("a1", "improv") else "up", "happy", (1, 0))
    party = at(t, "a2", None, -0.1)
    if not party: tape(c, "MARKETING BY DAY", 720, 640, 44, -3, pk(t, "a1", "marketing,"), seed=730)
    if at(t, "a1", "improv", -0.2) and not party:
        k = pk(t, "a1", "improv")
        c.save(); c.translate(720, 1000); c.scale(k, k)
        ink(c, wpoly([(-200, 120), (200, 120), (170, 60), (-170, 60)], 731, 2, True, 40), BROWN, 8)
        ink(c, wpoly([(-40, -200), (40, -200), (160, 60), (-160, 60)], 732, 2, True, 40), YEL, 0, INK, 0.35)
        mic(c, 0, 20, 0.6); c.restore()
        tape(c, "IMPROV BY NIGHT", 720, 800, 44, 3, k, seed=733, col=YEL)
    if party:     # party: balloons pop in, the father-in-law + thought bubble of a warehouse
        c.save(); c.translate(0, 0)
        for i, (bx, col) in enumerate(((140, RED), (220, PUR), (940, GRN))): balloon(c, bx, 600 + (i % 2) * 60, 46, "", 734 + i, col, t)
        c.restore()
        person(c, 720, 1440, 1.15, 8, GREY, t, "point", "FRIEND'S FATHER-IN-LAW", "happy", (-1, 0), "bald", pk(t, "a2", "father-in-law"))
        k = pk(t, "a2", "warehouse", -0.25)
        if k > 0:
            c.save(); c.translate(720, 700); c.scale(0.3 * k, 0.3 * k); c.translate(-540, -1100)
            warehouse_bg(c, 740); c.restore()
            bubble(c, "a whole warehouse of razor blades!", 720, 860, k, (40, 200), 44, 420, think=True)


def S_fancy(c, t, n):
    base(c, tint=(200, 206, 216))
    char(c, "razor", 540, 1440, 1.25, t, mth(t, FANCY_L), (0, -0.3), "neutral", "hips", blink=blink(t), fancy=True, case=True)
    for i, (w_, wd, x, y) in enumerate((("FANCY", "fancy,", 250, 700), ("LOCKED UP", "locked", 820, 760), ("$$$", "expensive.", 540, 560))):
        stamp(c, w_, x, y, 64, (-6, 5, -3)[i], sk(t, "a3", wd), RED if i == 2 else BLU, 750 + i)


# ---------------------------------------------------------------- here's how it works (a4-a7): step board evolving
def S_how(c, t, n):
    base(c, tint=GRN)
    tape(c, "HERE'S HOW IT WORKS", 540, 560, 54, -3, pk(t, "a4"), seed=760)
    # step 1: laptop sign-up, left
    if at(t, "a4", "one,", -0.2):
        k = pk(t, "a4", "one,"); stamp(c, "STEP 1", 270, 660, 50, -5, sk(t, "a4", "one,"), BLU, 761)
        c.save(); c.translate(270, 960); c.scale(k * 0.6, k * 0.6); c.translate(-270, -960); laptop(c, 270, 960, 1.0, 762, "SIGN UP"); c.restore()
        if at(t, "a4", "online.", 0.1): scribble(c, 270, 930, 140, 80, pr(t, TW("a4", "online.") + 0.1, 0.4), RED, 7, 763)
    # step 2: mailbox + envelope flying in, right
    if at(t, "a5", "two,", -0.2):
        stamp(c, "STEP 2", 790, 660, 50, 5, sk(t, "a5", "two,"), BLU, 764)
        mailbox(c, 800, 1090, 0.7, pr(t, TW("a5", "mailbox."), 0.3), 765)
        u = eout(pr(t, TW("a5", "fresh") - 0.1, 0.8))
        if u < 1: envelope(c, 300 + 480 * u, 850 + 30 * math.sin(u * 3), 0.5, 766, False)
        tape(c, "EVERY MONTH", 800, 1130, 36, 3, pk(t, "a5", "month."), seed=767, col=YEL)
    # the price math (a6-a7) slides up over the middle
    if at(t, "a6", None, -0.1):
        k = pk(t, "a6")
        c.save(); c.translate(400, 1300); c.scale(0.8 * k, 0.8 * k)
        ink(c, wrrect(-300, -150, 300, 150, 18, 768, 2), WHITE, 9)
        text(c, "$1 / MONTH", -110, -50, 52, INK, BLK_F) if at(t, "a6", "dollar", -0.1) else None
        text(c, "+ $2 SHIPPING", -70, 30, 46, INK, BLK_F) if at(t, "a6", "shipping.", -0.3) else None
        if at(t, "a7", "three", -0.1):
            wline(c, [(-260, 70), (120, 70)], 769, 6); title(c, "= $3", 200, 10, 80, RED, pk(t, "a7", "three"), -4, BLK_F)
        c.restore()
    if at(t, "a7", "coffee.", -0.4):
        k = pk(t, "a7", "coffee.", -0.3); c.save(); c.translate(850, 1440); c.scale(k, k); coffee(c, 0, 0, 0.55); c.restore()
        tape(c, "LESS THAN 1 FANCY COFFEE", 540, 1480, 34, -2, k, seed=770)


# ---------------------------------------------------------------- the video (b1-b3b)
def S_video(c, t, n):
    base(c)
    on_b2 = at(t, "b2", None, -0.05)
    # b1: three giant billboards loom over tiny Dubin; red X when he writes his own video
    for i, (x, w_) in enumerate(((220, "ADS $$$"), (540, "TV $$$"), (860, "ADS $$$"))):
        k = pk(t, "b1", None, 0.1 * i)
        if k > 0 and not at(t, "b3", None, -0.1):
            c.save(); c.translate(x, 1100); c.scale(0.62 * k, 0.62 * k); billboard(c, 0, 0, 1.0, w_, 780 + i); c.restore()
            if on_b2: strike(c, x - 120, 900, x + 120, pr(t, L0("b2") + 0.15 * i, 0.3))
    if not at(t, "b3", None, -0.1):
        dubin(c, 540, 1440, t, 0.8 if not on_b2 else 1.0, "shrug" if not on_b2 else "hold", "worried" if not on_b2 else "happy", (0, 0), "DUBIN")
        if not on_b2: bubble(c, "?", 700, 1150, pk(t, "b1", "noticed,"), (-60, 120), 70, 140)
        if on_b2:
            k = pk(t, "b2", "funny")
            c.save(); c.translate(780, 1160); c.scale(k, k); ink(c, wrrect(-110, -140, 110, 140, 8, 783, 1.4), WHITE, 7)
            for j in range(6): wline(c, [(-80, -100 + j * 40), (80 - (j % 2) * 40, -100 + j * 40)], 784 + j, 4, GREY)
            text(c, "HA!", 0, -150, 40, RED, MARK_F); c.restore()
            tape(c, "HE WROTE IT. HE STARS IN IT.", 540, 640, 44, -3, pk(t, "b2", "himself."), seed=785)
    else:   # b3-b3b: the warehouse shoot
        warehouse_bg(c, 790)
        dubin(c, 380, 1440, t, 1.05, "up", "happy", (1, 0), "DUBIN")
        person(c, 760, 1440, 1.0, 21, PUR, t, "hold", "IMPROV FRIEND · DIRECTOR", "happy", (-1, 0), "long", pk(t, "b3", "directed,"))
        if at(t, "b3", "directed,", -0.1): camera(c, 690, 1150, 0.6, 791)
        clapper(c, 560, 820, 0.8, 1 - pr(t, TW("b3", "warehouse.") - 0.1, 0.15), 792)
        if at(t, "b3b", None, -0.1):
            k = pk(t, "b3b", "eight", -0.2)
            c.save(); c.translate(860, 640); c.scale(k, k); ink(c, wellipse(0, 0, 90, 90, 793, 1.6), WHITE, 8)
            a = t * 6; wline(c, [(0, 0), (60 * math.sin(a), -60 * math.cos(a))], 794, 7, RED); wline(c, [(0, 0), (0, -40)], 795, 7); c.restore()
            tape(c, "ABOUT 8 HOURS", 860, 770, 40, 3, k, seed=796, col=YEL)


def S_dollar(c, t, n):
    base(c, tint=ORG)
    char(c, "razor", 540, 1440, 1.3, t, mth(t, DOLLAR_L), (0, -0.3), "happy", "cheer", blink=blink(t))
    tape(c, "$1", 690, 1000, 56, 8, 1.0, seed=800, col=YEL)
    for i, (w_, wd) in enumerate((("1 WAREHOUSE", "warehouse,"), ("1 CAMERA", "camera,"), ("1 CONFIDENT MAN", "confident"))):
        tape(c, w_, 540, 560 + i * 90, 44, (-3, 3, -2)[i], pk(t, "b4", wd), seed=801 + i, col=(WHITE, WHITE, YEL)[i])


def S_cost(c, t, n):
    base(c, tint=YEL)
    dubin(c, 300, 1440, t, 1.3, "point", "happy", (1, 0), "DUBIN")
    k = pk(t, "b5", "forty-five", -0.3)
    if k > 0:   # receipt slides out
        c.save(); c.translate(760, 1150); c.scale(k, k); ink(c, wpoly([(-150, -260), (150, -260), (150, 250), (110, 230), (70, 250), (30, 230), (-10, 250), (-50, 230), (-90, 250), (-150, 230)], 810, 1.6, True, 40), WHITE, 8)
        text(c, "RECEIPT", 0, -200, 34, GREY, BLK_F)
        for j in range(4): wline(c, [(-110, -140 + j * 50), (110, -140 + j * 50)], 811 + j, 4, GREY)
        text(c, "TOTAL", -60, 110, 38, INK, BLK_F); text(c, "$4,500", 60, 170, 54, RED, BLK_F); c.restore()
    bubble(c, "\"I spent about $4,500 on it.\"", 540, 700, pk(t, "b5", "Dubin"), (-200, 200), 50, 640)
    tape(c, "FORTUNE, 2015", 540, 860, 32, 2, pk(t, "b5", "Dubin", 0.2), seed=815, col=GREY)


# ---------------------------------------------------------------- launch day (c1-c4): evolving
def S_launch(c, t, n):
    base(c, tint=SKY if not at(t, "c4", None, -0.05) else (255, 190, 180))
    if not at(t, "c3", None, -0.1):
        calendar(c, 260, 760, "2012", 0.8, pk(t, "c1", "March"), 820); tape(c, "MARCH 6", 260, 600, 40, -4, pk(t, "c1", "March"), seed=819)
    # laptop with upload bar then crash
    c.save(); c.translate(560, 1180); laptop(c, 0, 0, 1.0, 821, "LAUNCH VIDEO"); c.restore()
    u = pr(t, TW("c1", "video") - 0.2, 0.9); ink(c, wrrect(400, 1040, 400 + 320 * u + 1, 1080, 10, 822, 0.8), GRN, 0)
    if at(t, "c2", "crashed", -0.15): crash_window(c, 600, 1060, 0.8, t, 823, pk(t, "c2", "crashed", -0.15), "WEBSITE")
    if at(t, "c3", "upside?", -0.15) and not at(t, "c4", None, -0.1):
        tape(c, "THE UPSIDE?", 540, 620, 52, 4, pk(t, "c3", "upside?"), seed=824, col=GRN)
        stamp(c, "SOLD OUT IN 6 HOURS", 540, 780, 64, -5, sk(t, "c3", "six"), RED, 825)
    if at(t, "c4", "catch?", -0.15):
        tape(c, "THE CATCH?", 540, 620, 52, -4, pk(t, "c4", "catch?"), seed=826, col=RED, fg=WHITE)
        k = pr(t, TW("c4", "ship") - 0.2, 0.8)
        for i in range(int(9 * k)): ink(c, wrrect(120 + (i % 3) * 100, 1300 - (i // 3) * 90, 210 + (i % 3) * 100, 1384 - (i // 3) * 90, 6, 827 + i, 1.2), TAN, 6)
        if k > 0.3: text(c, "SHIP THEM ALL?!", 540, 790, 60, RED, MARK_F)


def S_night(c, t, n):
    night = at(t, "c6", None, -0.1)
    base(c, tint=(40, 50, 100) if night else None)
    if not night:   # c5: office printer spitting labels
        ink(c, wrrect(330, 1000, 750, 1260, 20, 830, 2), GREY, 9); ink(c, wrrect(380, 960, 700, 1010, 6, 831, 1), WHITE, 6)
        k = pr(t, L0("c5"), 1.8)
        for i in range(int(10 * k)): label_stack(c, 230 + (i % 5) * 160, 1420 - (i // 5) * 70, 3, 0.7, 832 + i, (-8, 5, -3, 7, -6)[i % 5])
        tape(c, "THOUSANDS OF LABELS", 540, 700, 50, -3, pk(t, "c5", "thousands"), seed=840)
        you(c, 900, 1440, t, 0.8, "head", "shock", (-1, 0))
    else:           # c6: toss them over the warehouse fence at night
        c.save(); c.translate(540, 1100); c.scale(0.9, 0.9); c.translate(-540, -1100); warehouse_bg(c, 841, True); c.restore()
        fence(c, 120, 960, 1440, 380, 842)
        c.drawCircle(860, 560, 60, P((255, 244, 200)))
        person(c, 200, 1440, 0.9, 30, BLU, t, "up", "THE TEAM", "happy", (1, 0))
        for i in range(3):
            u = ((t - L0("c6")) * 0.9 + i * 0.33) % 1.0
            label_stack(c, 240 + 560 * u, 1180 - 420 * math.sin(math.pi * u), 3, 0.5, 850 + i, 360 * u)
        tape(c, "OVER THE FENCE, AT NIGHT", 540, 680, 44, -3, pk(t, "c6", "fence."), seed=853, col=YEL)


# ---------------------------------------------------------------- results (c7-c8b)
def S_result(c, t, n):
    base(c, tint=GRN)
    big = at(t, "c8b", None, -0.1)
    k = pr(t, L0("c7"), max(0.5, TW("c7", "twelve") - L0("c7") + 0.6)) if not big else pr(t, L0("c8b"), 0.8) * 0.33 + 0.67
    crowd(c, 540, 1390, 36 if not big else 48, 12, k, 860, 0.75)
    if at(t, "c7", "fluke?", -0.2) and not at(t, "c8", None, -0.1):
        bubble(c, "A fluke?", 240, 640, pk(t, "c7", "fluke?"), (40, 180), 50, 300, think=True)
    if at(t, "c7", "twelve", -0.2) and not at(t, "c8", None, -0.1):
        title(c, "12,000 SIGN-UPS", 600, 760, 80, DGRN, pk(t, "c7", "twelve"), -3, BLK_F)
        tape(c, "WITHIN DAYS", 600, 880, 40, 3, pk(t, "c7", "days,"), seed=861, col=YEL)
    if at(t, "c8", None, -0.1):
        calendar(c, 240, 700, "2016", 0.7, pk(t, "c8"), 862)
        building(c, 760, 1000, 300, 380, PUR, 863, None)
        tape(c, "UNILEVER", 760, 590, 44, 3, pk(t, "c8", "Unilever"), seed=864)
        stamp(c, "SOLD · ~$1 BILLION (REPORTED)", 540, 1090, 46, -5, sk(t, "c8", "billion"), RED, 865)
    if at(t, "c8b", None, -0.1):
        tape(c, "3 MILLION+ MEMBERS", 540, 520, 46, -2, pk(t, "c8b", "three"), seed=866, col=YEL)


def S_rich(c, t, n):
    base(c, tint=YEL)
    for i in range(14): ink(c, wellipse(300 + (i % 7) * 80, 1430 - (i // 7) * 30, 44, 16, 870 + i, 1), (240, 196, 60), 5)
    char(c, "razor", 540, 1390, 1.25, t, mth(t, DOLLAR_L), (0, -0.3), "happy", "hips", blink=False, shades=True)
    bubble(c, "I'll take it.", 760, 680, pk(t, "c9", "take", -0.2), (-140, 200), 56, 360)
    coin_rain(c, t, L0("c9"), 10, 871, 1400)


# ---------------------------------------------------------------- kill the myth (t1-t2)
def S_myth(c, t, n):
    base(c)
    k = pk(t, "t1")
    c.save(); c.translate(540, 820); c.scale(0.62 * k, 0.62 * k); billboard(c, 0, 0, 1.0, "BIG BUDGET?", 880, RED); c.restore()
    if at(t, "t1", "Nope.", -0.1): scribble(c, 540, 620, 220, 110, pr(t, TW("t1", "Nope."), 0.4), RED, 10, 881); stamp(c, "NOPE", 800, 540, 90, 8, sk(t, "t1", "Nope."), RED, 882)
    if at(t, "t2", None, -0.1):
        items = [("A CLEAR IDEA", "clear"), ("A FUNNY FRIEND", "funny"), ("GUTS ON CAMERA", "guts")]
        ks = [pr(t, TW("t2", wd) - 0.1, 0.25) for _, wd in items]
        checklist(c, 540, 870, [w for w, _ in items], ks, 883, 760)


# ---------------------------------------------------------------- 4 moves (s1-s5b): one evolving board
def S_moves(c, t, n):
    base(c, tint=(255, 236, 200))
    tape(c, "4 MOVES FOR YOUR LAUNCH", 540, 560, 50, -3, pk(t, "s1"), seed=890)
    moves = [("s2", "one.", "1 SENTENCE"), ("s3", "two.", "BE THE FACE"), ("s4", "three.", "SHOOT IT CHEAP"), ("s5", "four,", "GET READY")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=-1)
    # rail of move tapes (top), ticks on done ones
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            x = (300, 780)[i % 2]; y = 680 + (i // 2) * 80; tape(c, f"{i + 1}. {lab}", x, y, 32, (-3, 3, -2, 2)[i], pk(t, l, w), seed=891 + i, col=YEL if i == cur else WHITE)
            if i < cur: wline(c, [(x + 150, y - 5), (x + 170, y + 15), (x + 210, y - 25)], 895 + i, 8, DGRN)
    if cur == -1:
        you(c, 540, 1440, t, 1.3, "up", "happy")
    elif cur == 0:   # one sentence
        you(c, 300, 1440, t, 1.2, "point", "happy", (1, 0))
        bubble(c, "Good blades, $1 a month.", 720, 960, pk(t, "s2b", "simple.", -0.1), (-200, 200), 52, 440)
        if not at(t, "s2b", None, -0.1): bubble(c, "1 sentence a 10-year-old gets", 720, 960, pk(t, "s2", "sentence", -0.2), (-200, 200), 46, 440, think=True)
    elif cur == 1:   # be the face
        you(c, 360, 1440, t, 1.25, "wave", "happy", (1, 0))
        camera(c, 800, 1150, 0.9, 900, 1.0 if (t % 1.6) < 0.08 else 0.0)
        if at(t, "s3", "actors,", -0.1): tape(c, "ACTORS", 800, 900, 44, 4, 1.0, seed=901, col=GREY); strike(c, 690, 900, 910, pr(t, TW("s3", "actors,"), 0.3))
        if at(t, "s3", "personality.", -0.3): stamp(c, "YOUR PERSONALITY", 560, 840, 52, -4, sk(t, "s3", "personality.", -0.2), DGRN, 902)
    elif cur == 2:   # shoot it cheap with friends
        you(c, 300, 1440, t, 1.1, "up", "happy", (1, 0))
        person(c, 760, 1440, 1.0, 40, PUR, t, "hold", "FUNNY FRIEND", "happy", (-1, 0), "long", pk(t, "s4", "friends"))
        clapper(c, 540, 900, 0.7, 1 - pr(t, TW("s4", "cheap,"), 0.15), 903)
        tape(c, "YOUR REAL SPACE", 540, 1080, 40, 3, pk(t, "s4", "real"), seed=904, col=YEL)
    else:            # get ready: boxes stacked + shipping + 6 hours
        for i in range(6): ink(c, wrrect(200 + (i % 3) * 150, 1440 - (i // 3 + 1) * 130, 330 + (i % 3) * 150, 1440 - (i // 3) * 130 - 6, 6, 905 + i, 1.4), TAN, 7)
        you(c, 820, 1440, t, 1.1, "hold", "happy", (-1, 0))
        if at(t, "s5b", None, -0.1):
            tape(c, "STOCK UP + PLAN SHIPPING", 540, 880, 42, -3, pk(t, "s5b", "shipping"), seed=911)
            stamp(c, "SOLD OUT IN 6 HOURS", 540, 1000, 52, 5, sk(t, "s5b", "six"), RED, 912)


# ---------------------------------------------------------------- callback ending (e1-e2)
def S_end(c, t, n):
    base(c, tint=YEL)
    you(c, 300, 1440, t, 1.3, "head" if t < TW("e1", "clear") else "up", "worried" if t < TW("e1", "clear") else "happy", (1, 0))
    title(c, "COULD YOU PULL IT OFF?", 540, 640, 70, INK, pk(t, "e1"), -2)
    if at(t, "e1", "promises.", -0.2): tape(c, "NO PROMISES", 760, 820, 44, 4, 1.0, seed=920, col=GREY)
    if at(t, "e1", "clear", -0.2): stamp(c, "CLEAR IDEA = REAL SHOT", 700, 960, 56, -4, sk(t, "e1", "clear"), DGRN, 921)
    if at(t, "e2", None, -0.1):
        tape(c, "TRY IT NEXT TIME", 760, 1120, 40, 3, pk(t, "e2"), seed=922)
        phone(c, 780, 1330, 0.55, 923)
        if at(t, "e2", "friend.", -0.4): arrow(c, 820, 1250, 960, 1100, 40, RED, 8, 924, pr(t, TW("e2", "friend.") - 0.4, 0.4))


def S_z(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "razor", 260, 1440, 0.9, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t))
    char(c, "razor", 820, 1440, 0.9, t, 0, (-0.4, -0.3), "worried", "shrug", blink=blink(t, 3), fancy=True)
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pk(t, "z1"), seed=930)
        bubble(c, "the friend who pays way too much for razors", 540, 780, pk(t, "z1", "friend"), (-180, 200), 54, 720)
    else:
        you(c, 540, 1440, t, 1.0, "shrug", "happy")
        title(c, "YOUR FACE IN YOUR 1ST AD?", 540, 640, 66, INK, pk(t, "z2"))
        stamp(c, "YES", 360, 820, 90, -6, sk(t, "z2", "YES"), DGRN, 931)
        stamp(c, "NO", 720, 820, 90, 6, sk(t, "z2", "NO."), RED, 932)


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
    if COVER and t < COVER_T:   # big hook title on frame 0 = the grid cover
        kk = 1.0 if t < COVER_T - 0.35 else 1.0 - ease((t - (COVER_T - 0.35)) / 0.35)
        cover_title(c, COVER[0], COVER[1], kk, 700)
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
