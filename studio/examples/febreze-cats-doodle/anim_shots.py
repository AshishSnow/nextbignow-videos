# FEBREZE "nine cats" — real case study + 3 moves, SHORTS LENGTH (16 Nov 2026). DOODLE look in the BLACK + YELLOW theme (owner 15 Nov):
# yellow-washed graph paper, black ink, cream/white cards, red marker only for annotations; charcoal + yellow title cover on frame 0.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# Two platform cuts (IMPROVEMENTS 15 Nov): OMB_PLAT=ig (full frame) / OMB_PLAT=yt (scene scaled 0.85 about (450,250), strip + cover unscaled).
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_lab", "a1", "whip"), ("S_cats", "b1", "whip"), ("S_bed", "c1", "whip"), ("S_fix", "d1", "whip"),
         ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "spray"), "spray"), (TW("i1", "nothing?"), "pop"), (TW("i2", "millions"), "chaching"), (TW("i2", "dud."), "stamp"),
        (TW("i3", "you're"), "pop"), (TW("i3", "three"), "stamp"), (L0("a1"), "pop"), (TW("a1", "wipe"), "spray"), (TW("a1", "Febreze."), "ding"),
        (TW("b1", "homes."), "pop"), (TW("b1", "nine"), "pop"), (TW("b1", "cats."), "pop"), (TW("b2", "smell?"), "pop"), (TW("b3", "wonderful?"), "ding"),
        (TW("b4", "noticing"), "click"), (TW("b5", "brutal"), "stamp"), (TW("c1", "four."), "pop"), (TW("c1", "bed,"), "whoosh"), (TW("c1", "sprays"), "spray"),
        (TW("c3", "celebration"), "ding"), (TW("c4", "turn?"), "stamp"), (TW("c4", "end"), "tick"), (TW("d1", "perfume."), "ding"),
        (TW("d1", "relaunch,"), "stamp"), (TW("d2", "doubled."), "chaching"), (TW("d3", "billion-dollar-a-year"), "chaching"),
        (TW("m1", "One:"), "stamp"), (TW("m2", "Two:"), "stamp"), (TW("m2", "Three:"), "stamp"), (TW("e1", "Nope."), "buzz"),
        (TW("e1", "celebration."), "ding"), (L0("z1"), "whoosh"), (TW("z2", "Spray,"), "stamp"), (TW("z2", "skip"), "stamp")]
def lt(t, sid): return t - SHOT[sid]["start"]



import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("FEBREZE ALMOST FLOPPED.", "WOULD YOU PAY FOR NOTHING?")   # (kicker, TITLE) on frame 0 = the grid cover (black + yellow)
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i3": "Imagine you're on that team. Here's the fix, plus 3 moves to steal.",
        "a1": "Mid-1990s. A clear spray built to wipe out bad smells, called Febreze.",
        "b1": "So researchers visit homes. One, outside Phoenix, belongs to a neat freak with 9 cats.",
        "b3": "\"Isn't it wonderful? They hardly smell at all!\"",
        "c1": "Then they visit a mom of 4. She makes the bed, then sprays the comforter.",
        "c3": "Her words: \"Spraying feels like a little minicelebration when I'm done with a room.\"",
        "d1": "More perfume. Then a relaunch, in 1998.", "d2": "Did it work? Within 2 months, sales doubled.",
        "d3": "By 2011? Febreze had become a $1-billion-a-year brand.",
        "m1": "3 moves. 1: watch real customers use your product, at home.", "m2": "2: tie it to a habit they have. 3: make it a treat."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
YOU = (255, 214, 0)
BY = (255, 214, 0); CHAR = (34, 34, 38)


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


def base(c, tint=BY, a=0.22, gy=1440):
    page(c, tint, a); ground(c, gy)


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




_tape0 = tape


def tape(c, s, x, y, size=46, rot=-3, k=1.0, col=None, fg=INK, seed=1):
    """theme tape: yellow by default (black + yellow), cream/white/black variants passed explicitly."""
    _tape0(c, s, x, y, size, rot, k, BY if col is None else col, fg, seed)


def researcher(c, x, y, t, s=1.0, k=1.0, look=(1, 0), pose="hold", name="RESEARCHER", seed=31):
    person(c, x, y, s, seed, (90, 60, 40), t, pose, name, "neutral", look, "short", k)
    if k > 0 and pose == "hold":
        cx, cy = x + 92 * s * look[0] if look[0] else x + 92 * s, y - 150 * s
        ink(c, wrrect(cx - 40 * s, cy - 54 * s, cx + 40 * s, cy + 54 * s, 6, seed + 3, 1.2), WHITE, 6)
        for j in range(3): wline(c, [(cx - 24 * s, cy - 24 * s + j * 22 * s), (cx + 24 * s, cy - 24 * s + j * 22 * s)], seed + 4 + j, 3, GREY)


def nothing_cloud(c, x, y, k=1.0, seed=950, dotted=True):
    """the empty 'smell of nothing' — a dashed cloud outline with NOTHING inside."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.scale(k, k)
    pts = [(math.cos(a) * (150 + 26 * math.sin(a * 5)), math.sin(a) * (95 + 18 * math.sin(a * 5))) for a in np.linspace(0, math.tau, 40, endpoint=False)]
    pth = _smooth(pts, True)
    pnt = S(INK, 7); pnt.setPathEffect(skia.DashPathEffect.Make([22, 16], 0)) if dotted else None
    c.drawPath(pth, P(WHITE, 0.85)); c.drawPath(pth, pnt)
    text(c, "NOTHING", 0, 16, 50, INK, MARK_F); c.restore()


# ---------------------------------------------------------------- hook (i1-i3): spray + stink -> nothing; P&G bets; YOU
def S_hook(c, t, n):
    base(c, a=0.30)
    mist = ((t - TW("i1", "spray")) * 1.4) % 1.0 if TW("i1", "spray") - 0.1 < t < TW("i1", "nothing?") + 0.8 else 0.0
    sad = at(t, "i2", "dud.", -0.1)
    char(c, "spray", 690, 1440, 1.15, t, 0.0, (-0.5, -0.2), "worried" if sad else "happy", "hips" if not sad else "down", blink=blink(t), mist=mist)
    if t < COVER_T + 0.2: return
    gone = at(t, "i1", "nothing?", -0.1)
    if not gone: stink(c, 300, 1080, 1.0, 951, t=t, w=11)
    elif not at(t, "i3", None, -0.1): nothing_cloud(c, 300, 980, pk(t, "i1", "nothing?") if not at(t, "i2", None) else 1.0)
    tape(c, "$?", 470, 760, 64, 6 + 6 * math.sin(t * 3), pk(t, "i1", "pay"), seed=952, col=WHITE)
    if at(t, "i2", None, -0.1) and not at(t, "i3", None, -0.1):
        tape(c, "PROCTER & GAMBLE BETS MILLIONS", 540, 600, 44, -3, pk(t, "i2"), seed=953)
        coin_rain(c, t, TW("i2", "millions"), 8, 954, 1300)
        if sad: stamp(c, "DUD", 300, 760, 110, -10, sk(t, "i2", "dud."), RED, 955)
    if at(t, "i3", None, -0.1):
        stamp(c, "DUD", 300, 760, 110, -10, 1.0, RED, 955)
        you(c, 230, 1440, t, 1.1, "head" if not at(t, "i3", "fix,", -0.1) else "point", "worried" if not at(t, "i3", "fix,", -0.1) else "happy", (1, 0), pk(t, "i3", "you're"))
        tape(c, "YOU'RE ON THE TEAM", 540, 600, 44, -3, pk(t, "i3", "Imagine"), seed=956, col=WHITE)
        if at(t, "i3", "three", -0.2): stamp(c, "THE FIX + 3 MOVES", 330, 980, 52, -4, sk(t, "i3", "three"), INK, 957)


# ---------------------------------------------------------------- the lab (a1): smells get wiped out, name tape
def S_lab(c, t, n):
    base(c, a=0.14)
    calendar(c, 250, 930, "1990s", 0.72, pk(t, "a1"), 960, INK)
    tape(c, "MID-", 250, 735, 40, -4, pk(t, "a1"), seed=961, col=WHITE)
    k = 1 - pr(t, TW("a1", "wipe") - 0.1, 0.9)
    stink(c, 300, 1320, k, 962, t=t, w=10); stink(c, 880, 1320, k, 965, t=t, w=10)
    mist = ((t - TW("a1", "wipe")) * 1.6) % 1.0 if TW("a1", "wipe") - 0.1 < t < TW("a1", "wipe") + 1.4 else 0.0
    char(c, "spray", 600, 1440, 1.1, t, 0.0, (0.3, -0.2), "happy", "up" if at(t, "a1", "Febreze.", -0.2) else "hips", blink=blink(t), mist=mist)
    tape(c, "CLEAR. NO SMELL. KILLS ODORS.", 600, 640, 40, 3, pk(t, "a1", "clear"), seed=966, col=WHITE)
    if at(t, "a1", "Febreze.", -0.2): tape(c, "FEBREZE", 760, 800, 64, -5, pk(t, "a1", "Febreze."), seed=967)


# ---------------------------------------------------------------- the nine-cat house (b1-b5)
CAT_COLS = [(150, 150, 156), CHAR, (255, 214, 0), WHITE, (210, 180, 120), (150, 150, 156), CHAR, WHITE, (255, 214, 0)]


def S_cats(c, t, n):
    base(c, a=0.16)
    late = at(t, "b4", None, -0.1)
    wins = house(c, 540, 1440, 600, 420, 970, WHITE, CHAR, BY)
    if not late: tape(c, "OUTSIDE PHOENIX", 540, 560, 44, -3, pk(t, "b1", "Phoenix,"), seed=971, col=WHITE)
    researcher(c, 120, 1440, t, 0.8, pk(t, "b1", "homes."), (1, 0), "hold", None, 972)
    # nine cats pop in one by one from "nine"
    t9 = TW("b1", "nine") - 0.25; slots = wins + [(300, 1440), (930, 1440), (660, 1440), (790, 1440), (700, 900)]
    nshow = 0
    for i in range(9):
        kk = pop_k(t, t9 + i * 0.11, 0.25)
        if kk <= 0: continue
        nshow = i + 1; x, y = slots[i]
        if i < 4: c.save(); c.translate(x, y + 52); c.scale(0.36 * kk, 0.36 * kk); char(c, "cat", 0, 0, 1.0, t, 0, (0, 0), "happy", blink=blink(t, i), seed=980 + i, col=CAT_COLS[i], smug=late); c.restore()
        elif i < 8: c.save(); c.translate(x, y); c.scale(0.5 * kk, 0.5 * kk); char(c, "cat", 0, 0, 1.0, t, 0, ((-1, 1)[i % 2] * 0.5, 0), "happy", blink=blink(t, i), seed=980 + i, col=CAT_COLS[i], smug=late); c.restore()
        else: c.save(); c.translate(700, 905); c.scale(0.42 * kk, 0.42 * kk); char(c, "cat", 0, 0, 1.0, t, 0, (0, 0), "happy", blink=blink(t, i), seed=988, col=CAT_COLS[i], smug=late); c.restore()
    if nshow and not late and not at(t, "b3", None, -0.1): text(c, f"{nshow} CAT{'S' if nshow > 1 else ''}", 800, 700, 60, RED, MARK_F)
    # stink over the house, fading on b4 as the nose dial turns down
    lvl = 1 - pr(t, TW("b4", "noticing") - 0.6, 1.0) if late else 1.0
    if nshow >= 5:
        for j, x in enumerate((300, 540, 780)): stink(c, x, 1000 - (j % 2) * 40, lvl * pr(t, t9 + 0.6, 0.5), 990 + j * 3, t=t, h=180)
    if not late:
        if at(t, "b1", "neat", -0.2): tape(c, "NEAT FREAK", 330, 980, 40, 4, pk(t, "b1", "neat"), seed=999, col=WHITE)
        if at(t, "b2", None, -0.1) and not at(t, "b3", None, -0.1):
            bubble(c, "The smell?", 260, 800, pk(t, "b2", "smell?", -0.3), (-120, 340), 50, 320)
        if at(t, "b3", None, -0.1):
            bubble(c, "\"Isn't it wonderful? They hardly smell at all!\"", 540, 690, pk(t, "b3"), (0, 600), 48, 600)
            tape(c, "AS REPORTED BY THE NYT, 2012", 540, 870, 30, 2, pk(t, "b3", "hardly"), seed=1001, col=WHITE)
    else:
        nose_dial(c, 270, 700, 0.75, lvl, 1002)
        tape(c, "YOU STOP NOTICING IT", 540, 470, 44, -3, pk(t, "b4", "noticing"), seed=1003)
        if at(t, "b5", "brutal", -0.2):
            stamp(c, "CAN'T SMELL\nTHE PROBLEM", 720, 640, 54, 6, sk(t, "b5", "brutal"), RED, 1004)


# ---------------------------------------------------------------- the made bed (c1-c4)
def S_bed(c, t, n):
    base(c, a=0.12)
    tuck = pr(t, TW("c1", "bed,") - 0.2, 0.6)
    bed(c, 600, 1440, 0.9, tuck, 1010, WHITE, BY)
    q = at(t, "c3", None, -0.1); turn = at(t, "c4", None, -0.1)
    person(c, 250, 1440, 1.0, 1011, (90, 60, 40), t, "point" if at(t, "c1", "sprays", -0.2) else "stand", "MOM OF 4", "happy", (1, 0), "long", pk(t, "c1", "mom"))
    if not q:
        kk = pk(t, "c1", "four.")
        if kk > 0: tape(c, "4 KIDS", 250, 860, 40, -5, kk, seed=1012, col=WHITE)
        researcher(c, 930, 1440, t, 0.85, pk(t, "c1", "visit"), (-1, 0), "hold", None, 1013)
        tape(c, "NEAR SCOTTSDALE", 540, 600, 44, -3, pk(t, "c1", "visit"), seed=1009, col=WHITE)
    if at(t, "c1", "sprays", -0.25) and not q:
        mist = ((t - TW("c1", "sprays")) * 1.5) % 1.0 if t < TW("c1", "sprays") + 1.6 else 0.0
        c.save(); c.translate(470, 1100); c.scale(0.45, 0.45); char(c, "spray", 0, 0, 1.0, t, 0, (0.4, 0), "happy", "hips", blink=blink(t), mist=mist); c.restore()
    if q and not turn:
        bubble(c, "\"Spraying feels like a little minicelebration when I'm done with a room.\"", 600, 700, pk(t, "c3"), (-300, 300), 44, 720)
        tape(c, "AS REPORTED BY THE NYT, 2012", 600, 900, 30, -2, pk(t, "c3", "words:"), seed=1014, col=WHITE)
        confetti(c, 600, 1100, t, TW("c3", "celebration") - 0.1, 22, 1015, 380)
    if turn:
        stamp(c, "THE TURN", 300, 640, 70, -6, sk(t, "c4", "turn?"), RED, 1016)
        items = [("MAKE THE BED", "Spraying"), ("TUCK CORNERS", "becomes"), ("SPRAY = CELEBRATE!", "end")]
        ks = [pr(t, TW("c4", wd) - 0.1, 0.25) for _, wd in items]
        c.save(); c.translate(640, 720); c.scale(0.62, 0.62); c.translate(-640, -720); checklist(c, 640, 720, [w for w, _ in items], ks, 1017, 820); c.restore()
        if at(t, "c4", "cleaning.", -0.3): scribble(c, 640, 1000, 230, 60, pr(t, TW("c4", "cleaning.") - 0.3, 0.4), RED, 8, 1018)
        if at(t, "c4", "end", -0.2): tape(c, "LAST STEP OF CLEANING", 640, 1170, 38, 2, pk(t, "c4", "end"), seed=1019)


# ---------------------------------------------------------------- the fix + results (d1-d3)
def S_fix(c, t, n):
    base(c, a=0.30)
    perf = at(t, "d1", "perfume.", -0.2)
    chart = at(t, "d2", None, -0.1); big = at(t, "d3", None, -0.1)
    sx = 250 if chart else 540
    char(c, "spray", sx, 1440, 0.95 if chart else 1.15, t, 0.0, (0.4, -0.2), "happy", "up" if big else "hips", blink=blink(t), flower=perf)
    if perf and not chart:
        for j in range(3):
            a = t * 2 + j * 2.1; px, py = 540 + 260 * math.cos(a), 900 + 80 * math.sin(a)
            ink(c, wellipse(px, py, 22, 22, 1020 + j, 1), WHITE, 5); ink(c, wellipse(px, py, 8, 8, 1023 + j, 0.5), BY, 3)
        tape(c, "+ MORE PERFUME", 760, 760, 46, 4, pk(t, "d1", "perfume."), seed=1026, col=WHITE)
    if at(t, "d1", "relaunch,", -0.2) and not chart:
        calendar(c, 250, 760, "1998", 0.62, pk(t, "d1", "relaunch,"), 1027, INK)
        stamp(c, "RELAUNCH", 760, 600, 64, -5, sk(t, "d1", "relaunch,"), RED, 1028)
    if chart:
        k = pr(t, TW("d2", "doubled.") - 0.5, 0.7)
        bars(c, 700, 1300, [0.35, 0.35 + 0.35 * k], 1.0, 1029, BY, 140, 70, 480, ["BEFORE", "2 MONTHS"])
        if not big: tape(c, "DID IT WORK?", 700, 620, 46, -3, pk(t, "d2", "work?"), seed=1030, col=WHITE)
        if not big: stamp(c, "SALES x2", 780, 760, 66, 6, sk(t, "d2", "doubled."), RED, 1031)
    if big:
        stamp(c, "$1 BILLION A YEAR\n(2011)", 640, 720, 62, -5, sk(t, "d3", "billion-dollar-a-year", -0.1), RED, 1032)
        coin_rain(c, t, TW("d3", "billion-dollar-a-year"), 10, 1033, 1400)


# ---------------------------------------------------------------- 3 moves (m1-m2): one evolving board
def S_moves(c, t, n):
    base(c, a=0.14)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 580, 52, -3, pk(t, "m1"), seed=1040, col=INK, fg=BY)
    moves = [("m1", "One:", "1. WATCH THEM AT HOME"), ("m2", "Two:", "2. TIE IT TO A HABIT"), ("m2", "Three:", "3. MAKE IT A TREAT")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=-1)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 690 + i * 86; tape(c, lab, 540, y, 38, (-2, 2, -1)[i], pk(t, l, w), seed=1041 + i, col=BY if i == cur else WHITE)
            if i < cur: wline(c, [(800, y - 5), (820, y + 15), (860, y - 25)], 1045 + i, 8, RED)
    if cur <= 0:
        you(c, 230, 1440, t, 1.05, "point" if cur == 0 else "up", "happy", (1, 0))
        if cur == 0:
            wins = house(c, 700, 1440, 400, 300, 1050, WHITE, CHAR, BY)
            researcher(c, 700, 1440, t, 0.6, 1.0, (1, 0), "hold", None, 1051)
            text(c, "WATCH", 700, 1020, 40, RED, MARK_F)
    elif cur == 1:
        you(c, 200, 1440, t, 1.0, "point", "happy", (1, 0))
        bed(c, 620, 1440, 0.7, 1.0, 1052, WHITE, BY)
        arrow(c, 420, 1050, 560, 1200, 30, RED, 8, 1053, pr(t, TW("m2", "habit") - 0.2, 0.4))
        tape(c, "SOMETHING THEY ALREADY DO", 620, 1000, 34, 3, pk(t, "m2", "habit"), seed=1054, col=WHITE)
    else:
        you(c, 300, 1440, t, 1.1, "up", "happy", (1, 0))
        c.save(); c.translate(760, 1440); c.scale(0.7, 0.7); char(c, "spray", 0, 0, 1.0, t, 0, (-0.4, 0), "happy", "up", blink=blink(t), flower=True); c.restore()
        confetti(c, 600, 1100, t, TW("m2", "treat.") - 0.2, 22, 1055, 360)


# ---------------------------------------------------------------- callback ending (e1)
def S_end(c, t, n):
    base(c, a=0.30)
    nothing_cloud(c, 290, 860, 0.9 * pk(t, "e1"), 1060)
    if at(t, "e1", "Nope.", -0.1): strike(c, 150, 870, 430, pr(t, TW("e1", "Nope."), 0.3), RED, 14, 1061)
    if at(t, "e1", "celebration.", -0.4):
        tape(c, "THE LITTLE CELEBRATION", 700, 1060, 42, 4, pk(t, "e1", "celebration.", -0.3), seed=1062, col=WHITE)
        confetti(c, 700, 980, t, TW("e1", "celebration.") - 0.3, 26, 1063, 380)
    you(c, 540, 1440, t, 1.0, "shrug" if not at(t, "e1", "pay", 0, ) else "up", "happy", (0, 0))
    title(c, "WOULD YOU PAY FOR NOTHING?", 540, 620, 64, INK, pk(t, "e1"), -2)


def S_z(c, t, n):
    base(c, a=0.30)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 600, 58, -3, pk(t, "z1"), seed=1070, col=INK, fg=BY)
        bubble(c, "the friend who sprays after every clean", 540, 800, pk(t, "z1", "friend"), (-180, 200), 54, 720)
        phone(c, 300, 1250, 0.55, 1071)
        person(c, 800, 1440, 0.9, 1072, (90, 60, 40), t, "wave", "FRIEND", "happy", (-1, 0), "short")
        arrow(c, 380, 1150, 700, 1050, 60, RED, 8, 1073, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        you(c, 540, 1440, t, 1.0, "shrug", "happy")
        title(c, "AFTER CLEANING?", 540, 640, 76, INK, pk(t, "z2"))
        stamp(c, "SPRAY", 330, 860, 90, -6, sk(t, "z2", "Spray,"), INK, 1074)
        stamp(c, "SKIP IT", 760, 860, 90, 6, sk(t, "z2", "skip"), RED, 1075)


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    global BOIL
    BOIL = int(t * 12)
    c = SURF.getCanvas(); c.clear(skia.Color(*PAPER))
    if PLAT == "yt":   # YouTube cut: whole scene scaled 0.85 about (450,250) so nothing sits under the Shorts title row / button column
        page(c, BY, 0.30); c.save(); c.translate(450, 250); c.scale(0.85, 0.85); c.translate(-450, -250); c.clipRect(skia.Rect.MakeWH(W, H))
    c.save()
    for ti, kind in CUES:
        if kind in ("slam", "impact", "stamp") and 0 <= t - ti < 0.24:
            k = 1 - (t - ti) / 0.24; amp = 14 if kind != "stamp" else 7; c.translate(amp * k * math.sin(t * 90), amp * 0.8 * k * math.cos(t * 77))
    sh = SHOT[sid]; u = (t - sh["start"]) / max(0.5, sh["end"] - sh["start"])
    z = 1.0 + 0.03 * u; c.translate(W / 2, H * 0.55); c.scale(z, z); c.translate(-W / 2, -H * 0.55)
    RENDER[sid](c, t, n); c.restore()
    if PLAT == "yt":
        c.restore(); ink(c, wrrect(450 - 450 * 0.85, 250 - 250 * 0.85, 450 + 630 * 0.85, 250 + 1670 * 0.85, 14, 77, 1.6), None, 7)
    if COVER and t < COVER_T:   # big hook title on frame 0 = the grid cover
        kk = 1.0 if t < COVER_T - 0.35 else 1.0 - ease((t - (COVER_T - 0.35)) / 0.35)
        cover_by(c, COVER[0], COVER[1], kk, 700)
    if not (COVER and t < COVER_T - 0.35):   # frame 0 / grid cover = the title alone
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
