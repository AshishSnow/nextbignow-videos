# HOKA "the clown shoes" — real case study + 3 moves, SHORTS LENGTH (18 Nov 2026). DOODLE look on the LIGHT page (upgrade vs the
# black + yellow Febreze / Liquid Death Shorts): white graph paper, black ink, orange tapes, red marker; white title card + hero shoe on frame 0.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: the shoe is a generic sneaker with a puffy white sole and a tape label; founders + Karl Meltzer = plain doodles with name tapes.
# Two platform cuts: OMB_PLAT=ig (full frame) / OMB_PLAT=yt (scene scaled 0.85 about (450,250), strip + cover unscaled).
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_mtn", "b1", "whip"), ("S_shoe", "b4", "pop"), ("S_quote", "b5", "whip"),
         ("S_tiny", "c1", "whip"), ("S_big", "c3", "whip"), ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "billions"), "chaching"), (TW("i1", "clown"), "honk"), (TW("i2", "running"), "whoosh"), (TW("i2", "Three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "clubs"), "pop"), (TW("a1", "half"), "ding"),
        (TW("b1", "France."), "pop"), (TW("b1", "Hoka."), "stamp"), (TW("b2", "huge,"), "boing"), (TW("b2", "downhill."), "whoosh"),
        (TW("b3", "Thin,"), "pop"), (TW("b3", "craze."), "tick"), (L0("b4"), "honk"), (TW("b4", "bold."), "boing"),
        (TW("b5", "Outside"), "pop"), (TW("b5", "clown"), "tick"), (TW("b6", "care."), "stamp"), (TW("b7", "ultrarunners"), "ding"),
        (TW("c1", "tiny."), "click"), (TW("c1", "three"), "pop"), (TW("c2", "buys"), "stamp"), (TW("c2", "undisclosed"), "buzz"),
        (TW("c3", "work?"), "pop"), (TW("c3", "six"), "chaching"), (TW("c4", "seven"), "chaching"), (TW("c4", "day."), "stamp"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "back."), "ding"), (TW("m2", "Two:"), "stamp"), (TW("m2", "permit."), "stamp"),
        (TW("m3", "Three:"), "stamp"), (TW("m3", "ultrarunners."), "ding"),
        (TW("e1", "Clown"), "honk"), (TW("e2", "laugh."), "chaching"), (L0("z1"), "whoosh"), (TW("z2", "Thick"), "stamp"), (TW("z2", "thin?"), "stamp")]


def lt(t, sid): return t - SHOT[sid]["start"]



import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("PEOPLE CALLED THEM CLOWN SHOES", "NOW: $2.6 BILLION A YEAR?")   # (kicker, TITLE) on frame 0 = the grid cover (LIGHT page, white card, hero shoe below)
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i2": "You want in on the running boom? 3 moves at the end.",
        "a1": "Running clubs on Strava grew 3.5x last year.",
        "c1": "In 2012, it's still tiny. Under $3 million in sales.",
        "c3": "Did it work? Hoka's last fiscal year: about $2.6 billion.",
        "c4": "That's about $7 million in sales. Every single day.",
        "m1": "Your moves. 1: start a weekly run club, and see who keeps coming back.",
        "m2": "2: going big? Big groups in some city parks need a permit.",
        "m3": "3: win one hard-core crowd first. Look at Hoka and its ultrarunners."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
YOU = GRN
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


def base(c, tint=None, a=0.0, gy=1440):
    page(c, tint, a); ground(c, gy)   # LIGHT page (18 Nov upgrade: no yellow wash)


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
    _tape0(c, s, x, y, size, rot, k, ORG if col is None else col, fg, seed)



# ---------------------------------------------------------------- hook (i1-i2): start line, the chunky shoe, billions, YOU
def S_hook(c, t, n):
    base(c)
    start_line(c, 1330, 1300)
    nose = pop_k(t, TW("i1", "clown") - 0.05, 0.35) if t > COVER_T else 0.0
    rich = at(t, "i1", "billions", -0.1) and t > COVER_T
    char(c, "chunky", 600, 1440, 0.95, t, 0.0, (-0.3, -0.2), "happy" if rich else "neutral", "hips" if not rich else "cheer", blink=blink(t) and t > COVER_T, nose=nose, label="SHOE", seed=1300)
    if t < COVER_T + 0.1: return
    late = at(t, "i2", None, -0.1)
    if rich:
        hh = 520 * eout(pr(t, TW("i1", "billions") - 0.1, 0.7))
        ink(c, wrrect(820, 1100 - hh, 940, 1100, 8, 1301, 1.2), (140, 214, 140), 8); arrow(c, 880, 1080 - hh, 880, 990 - hh, 0, RED, 9, 1302, 1.0, 28)
        if not late: tape(c, "BILLIONS A YEAR", 360, 620, 52, -4, pk(t, "i1", "billions"), seed=1303)
    if at(t, "i1", "clown", -0.2) and not late:
        tape(c, "\"CLOWN SHOES\"", 380, 760, 50, 3, pk(t, "i1", "clown"), seed=1304, col=WHITE)
        text(c, "?", 890, 900, 150, RED, MARK_F)
    if at(t, "i2", None, -0.1):
        you(c, 170, 1440, t, 0.85, "point" if at(t, "i2", "Three", -0.2) else "wave", "happy", (1, 0), pk(t, "i2"))
        if at(t, "i2", "Three", -0.2):
            for j, x in enumerate((360, 540, 720)): cone(c, x, 640, 0.55, 1306 + j, str(j + 1), pk(t, "i2", "Three", j * 0.12))
            stamp(c, "3 MOVES AT THE END", 540, 780, 52, -3, sk(t, "i2", "Three", 0.3), RED, 1309)


# ---------------------------------------------------------------- the trend (a1): running clubs pile in, x3.5
def S_trend(c, t, n):
    base(c)
    tape(c, "THE TREND: RUN CLUBS", 540, 470, 56, -3, pk(t, "a1"), seed=1310, col=INK, fg=WHITE)
    k = pr(t, TW("a1", "clubs") - 0.2, 1.6)
    for j in range(7):
        kk = pop_k(t, TW("a1", "clubs") - 0.2 + j * 0.18, 0.3)
        runner(c, 140 + j * 120, 1440, t, 0.62, 1311 + j, (BLU, PNK, GRN, ORG, PUR, SKY, RED)[j], None, True, kk, 0.9)
    bars(c, 540, 1000, [0.18, 0.18 + 0.18 * 2.5 * min(1, k * 1.2)], 1.0, 1320, ORG, 150, 110, 380, ["2024", "2025"])
    if at(t, "a1", "half", -0.3):
        stamp(c, "x3.5", 760, 600, 96, 6, sk(t, "a1", "half"), RED, 1321)
        tape(c, "NUMBER OF RUNNING CLUBS ON STRAVA (2025)", 540, 1110, 30, 2, pk(t, "a1", "half", 0.2), seed=1322, col=WHITE)


# ---------------------------------------------------------------- the mountain (b1-b3): France, the big sole, the thin-shoe craze
def S_mtn(c, t, n):
    base(c)
    b3 = at(t, "b3", None, -0.1)
    if not b3:
        mountain(c, 620, 1440, 900, 760, 1330, True, pr(t, TW("b2", "downhill.") - 0.8, 0.9))
        if not at(t, "b2", None, -0.1):
            tape(c, "FRANCE", 300, 520, 60, -4, pk(t, "b1", "France."), seed=1331)
            calendar(c, 840, 560, "2009", 0.5, pk(t, "b1", "Hoka."), 1332, BLU)
        person(c, 140, 1440, 0.72, 1333, (60, 90, 160), t, "wave", "FOUNDER 1", "happy", (1, 0), "short", pk(t, "b1", "guys"))
        person(c, 380, 1440, 0.72, 1334, (160, 70, 60), t, "point" if at(t, "b2", None) else "stand", "FOUNDER 2", "happy", (1, 0), "bald", pk(t, "b1", "guys", 0.15))
        if at(t, "b1", "outdoor-gear", -0.2): tape(c, "OUTDOOR-GEAR GUYS", 260, 980, 34, 3, pk(t, "b1", "outdoor-gear"), seed=1335, col=WHITE)
        if at(t, "b2", None, -0.1):
            u = pr(t, TW("b2", "downhill.") - 0.6, 1.4)
            rx, ry = 560 + 380 * u, 760 + 560 * u
            runner(c, rx, ry, t, 0.6, 1336, ORG, None, True, pk(t, "b2", "huge,"), 1.3, "happy", 30)
            if u > 0.05: speed_lines(c, rx - 60, ry - 140, 4, 140, 1337, RED, min(1, u * 3))
            tape(c, "HUGE, SOFT SOLE", 540, 480, 52, 3, pk(t, "b2", "huge,"), seed=1338)
            if at(t, "b2", "downhill.", -0.3): tape(c, "BUILT FOR DOWNHILL", 540, 590, 42, -2, pk(t, "b2", "downhill.", -0.2), seed=1339, col=WHITE)
    else:
        tape(c, "THE CRAZE BACK THEN: THIN", 540, 480, 46, -3, pk(t, "b3"), seed=1340, col=WHITE)
        for j in range(4): thin_shoe(c, 200 + j * 225, 1000, 0.55, 1341 + j, rot=(-4, 3, -2, 5)[j], k=pop_k(t, L0("b3") + j * 0.15, 0.3))
        text(c, "EVERYONE ELSE", 540, 1060, 40, INK, MARK_F)
        if at(t, "b3", "craze.", -0.4):
            char(c, "chunky", 560, 1440, 0.62, t, 0, (0, -0.3), "neutral", "hips", blink=blink(t), label="HOKA", seed=1345)
            stamp(c, "THICK", 860, 1180, 64, 8, sk(t, "b3", "craze.", -0.2), RED, 1346)
            scribble(c, 560, 1290, 260, 140, pr(t, TW("b3", "craze."), 0.5), RED, 8, 1347)


# ---------------------------------------------------------------- the shoe talks (b4)
def S_shoe(c, t, n):
    base(c)
    char(c, "chunky", 560, 1440, 1.0, t, mth(t, ["b4"]), (-0.4, -0.2), "happy", "hips" if not at(t, "b4", "bold.", -0.2) else "cheer", blink=blink(t), nose=1.0, label="SHOE", seed=1350)
    bubble(c, "Clown shoes? I prefer BOLD.", 560, 640, pk(t, "b4"), (60, 280), 60, 700)
    if at(t, "b4", "bold.", -0.2): confetti(c, 560, 1000, t, TW("b4", "bold."), 18, 1351)


# ---------------------------------------------------------------- the quote + first fans (b5-b7)
def S_quote(c, t, n):
    base(c)
    fans = at(t, "b7", None, -0.1)
    if not fans:
        magazine(c, 300, 1000, 0.75, 1360, "OUTSIDE", "DECEMBER 2013")
        tape(c, "OUTSIDE MAGAZINE, 2013", 300, 1280, 30, 3, pk(t, "b5", "Outside"), seed=1361, col=WHITE)
        runner(c, 790, 1440, t, 0.8, 1362, RED, None, True, 1.0, 1.0, "happy")
        tape(c, "KARL MELTZER, ULTRARUNNER", 760, 1475, 30, -2, pk(t, "b5", "Meltzer"), seed=1363)
        if at(t, "b5", "people", -0.2):
            bubble(c, "\"People thought they looked like clown shoes, but I didn't care.\"", 600, 560, pk(t, "b5", "people"), (180, 300), 46, 780)
        if at(t, "b5", "clown", -0.1): scribble(c, 600, 560, 120, 40, pr(t, TW("b5", "clown"), 0.4), RED, 6, 1364)
        if at(t, "b6", "care.", -0.2): stamp(c, "DIDN'T CARE", 760, 860, 60, -6, sk(t, "b6", "care."), RED, 1365)
    else:
        mountain(c, 540, 1440, 1100, 560, 1366, False, 1.0)
        for j in range(5): runner(c, 160 + j * 150, 1440 - j * 6, t, 0.62, 1367 + j, (RED, BLU, PUR, ORG, TEAL)[j], None, True, pop_k(t, L0("b7") + j * 0.12, 0.3), 1.0)
        tape(c, "FIRST BIG FANS: ULTRARUNNERS", 540, 560, 44, -3, pk(t, "b7", "first"), seed=1372)
        if at(t, "b7", "ultrarunners", -0.2): scribble(c, 460, 1260, 400, 170, pr(t, TW("b7", "ultrarunners"), 0.6), RED, 8, 1373)


# ---------------------------------------------------------------- tiny in 2012, then bought (c1-c2)
def S_tiny(c, t, n):
    base(c)
    bought = at(t, "c2", None, -0.1)
    if not bought: calendar(c, 820, 560, "2012", 0.5, pk(t, "c1"), 1380, BLU)
    lift = eout(pr(t, TW("c2", "buys") - 0.1, 0.8)) if bought else 0.0
    sx, sy = 300 + 200 * lift, 1440 - 160 * lift
    stall(c, sx, sy, 0.7 * (1 - 0.25 * lift), 1381, "SHOE STALL")
    money_stack(c, sx + 170, sy, 2, 0.7, 1382)
    if not bought:
        tape(c, "STILL TINY", 300, 620, 60, -4, pk(t, "c1", "tiny."), seed=1383)
        if at(t, "c1", "three", -0.2):
            tape(c, "UNDER $3M IN SALES (2012)", 400, 760, 44, 2, pk(t, "c1", "three"), seed=1384, col=WHITE)
            scribble(c, sx + 170, sy - 40, 120, 70, pr(t, TW("c1", "three"), 0.5), RED, 7, 1385)
    else:
        boot_tower(c, 760, 1440, 300, 560, 1386, "DECKERS")
        tape(c, "THE UGG BOOTS COMPANY", 680, 1475, 30, 2, pk(t, "c2", "Ugg"), seed=1387, col=WHITE)
        if at(t, "c2", "buys", -0.2): arrow(c, 680, 1000, sx + 60, sy - 330, -80, RED, 9, 1388, pr(t, TW("c2", "buys") - 0.2, 0.4))
        if at(t, "c2", "buys", -0.2): stamp(c, "BOUGHT IN 2012", 340, 560, 56, -6, sk(t, "c2", "buys"), RED, 1389)
        if at(t, "c2", "undisclosed", -0.2):
            char(c, "tag", 280, 1060, 0.5, t, 0, (0.3, 0), "shock", "shrug", blink=blink(t), price="$ ???", seed=1390)
            tape(c, "PRICE: UNDISCLOSED", 330, 720, 40, -2, pk(t, "c2", "undisclosed"), seed=1391)


# ---------------------------------------------------------------- did it work? (c3-c4)
def S_big(c, t, n):
    base(c)
    day = at(t, "c4", None, -0.1)
    if not day:
        tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "c3", "work?", -0.2), seed=1400, col=INK, fg=WHITE)
        g = pr(t, TW("c3", "six") - 0.8, 1.2)
        bars(c, 540, 1300, [0.012, 1.0], ease(max(0.02, g)), 1401, ORG, 180, 160, 620, ["2012", "FY2026"])
        if at(t, "c3", "six", -0.2):
            stamp(c, "$2.6 BILLION", 720, 600, 74, -5, sk(t, "c3", "six"), RED, 1402)
            tape(c, "NET SALES, YEAR TO MARCH 2026 (DECKERS)", 540, 1395, 28, 1, pk(t, "c3", "six", 0.2), seed=1403, col=WHITE)
            text(c, "UNDER $3M", 360, 1220, 34, RED, MARK_F)
    else:
        u = pr(t, L0("c4"), 3.0); pages = int(u * 6)
        calendar(c, 300, 820, ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][min(6, pages)], 0.6, pk(t, "c4"), 1405, RED)
        money_stack(c, 760, 1440, 2 + int(u * 14), 1.1, 1406)
        if at(t, "c4", "seven", -0.2):
            stamp(c, "$7M", 760, 600, 100, 6, sk(t, "c4", "seven"), RED, 1407)
            tape(c, "IN SALES, EVERY DAY", 300, 1020, 40, -3, pk(t, "c4", "day."), seed=1408)
            text(c, "$2.6B / 365", 760, 760, 40, INK, MARK_F)
        you(c, 180, 1440, t, 0.8, "head", "shock", (1, -0.3), pk(t, "c4", "every"))


# ---------------------------------------------------------------- 3 moves (m1-m3): one evolving park board
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 460, 52, -3, pk(t, "m1"), seed=1420, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. WEEKLY RUN CLUB"), ("m2", "Two:", "2. BIG GROUP? CHECK PERMITS"), ("m3", "Three:", "3. ONE HARD-CORE CROWD FIRST")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=-1)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 560 + i * 78; tape(c, lab, 540, y, 36, (-2, 2, -1)[i], pk(t, l, w), seed=1421 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(880, y - 5), (900, y + 15), (940, y - 25)], 1425 + i, 8, RED)
    if cur <= 0:
        you(c, 190, 1440, t, 0.95, "wave", "happy", (1, 0))
        wk = min(2, int(pr(t, TW("m1", "weekly") - 0.1, 2.4) * 3))
        calendar(c, 820, 900, ["WEEK 1", "WEEK 2", "WEEK 3"][wk], 0.42, pk(t, "m1", "weekly"), 1428, ORG)
        nr = 2 + wk * 2
        for j in range(nr): runner(c, 380 + j * 90, 1440, t, 0.5, 1430 + j, (RED, BLU, PUR, ORG, TEAL, PNK)[j], None, True, pop_k(t, TW("m1", "weekly") + j * 0.3, 0.3), 0.8)
        if at(t, "m1", "back.", -0.3): arrow(c, 900, 1150, 420, 1100, 120, RED, 8, 1436, pr(t, TW("m1", "back.") - 0.3, 0.5))
    elif cur == 1:
        park_sign(c, 230, 1440, 0.8, 1440, "CITY PARK")
        clipboard(c, 790, 1000, 0.8, 1441, "PERMIT", pk(t, "m2", "permit.", -0.3), int(pr(t, TW("m2", "permit."), 1.0) * 4))
        crowd(c, 560, 1380, 24, 8, pr(t, TW("m2", "groups") - 0.2, 1.2), 1442, 0.62)
        if at(t, "m2", "groups", -0.1): tape(c, "E.G. NYC'S HUDSON RIVER PARK: 20+ PEOPLE", 540, 1480, 28, 1, pk(t, "m2", "groups"), seed=1443, col=WHITE)
        if at(t, "m2", "permit.", -0.2): scribble(c, 790, 1000, 160, 210, pr(t, TW("m2", "permit."), 0.5), RED, 8, 1444)
    else:
        for j in range(4): runner(c, 330 + j * 120, 1440, t, 0.6, 1450 + j, (RED, BLU, PUR, ORG)[j], None, True, 1.0, 1.0)
        tape(c, "ULTRARUNNERS", 510, 1475, 32, -2, 1.0, seed=1455, col=WHITE)
        crowd(c, 540, 960, 16, 8, 0.0 if not at(t, "m3", "Hoka", -0.2) else pr(t, TW("m3", "Hoka"), 0.8), 1456, 0.5)
        if at(t, "m3", "first.", -0.3): scribble(c, 510, 1280, 290, 170, pr(t, TW("m3", "first.") - 0.3, 0.5), RED, 8, 1457)
        if at(t, "m3", "Hoka", -0.2): arrow(c, 540, 1100, 540, 1010, 0, RED, 8, 1458, pr(t, TW("m3", "Hoka"), 0.4)); text(c, "THEN EVERYONE ELSE", 540, 830, 36, INK, MARK_F)
        you(c, 140, 1440, t, 0.8, "point", "happy", (1, 0))


# ---------------------------------------------------------------- callback ending (e1-e2)
def S_end(c, t, n):
    base(c)
    start_line(c, 1330, 1300)
    laugh = at(t, "e2", None, -0.1)
    char(c, "chunky", 560, 1440, 0.95, t, mth(t, ["e2"]) if laugh else 0.0, (-0.3, -0.2), "happy", "cheer" if laugh else "hips", blink=blink(t), nose=1.0, label="SHOE", seed=1300)
    title(c, "\"CLOWN SHOES,\" THEY SAID.", 540, 520, 64, INK, pk(t, "e1"), -2)
    if laugh:
        hh = 520
        ink(c, wrrect(840, 1100 - hh, 960, 1100, 8, 1301, 1.2), (140, 214, 140), 8)
        stamp(c, "LAST LAUGH", 300, 760, 70, -6, sk(t, "e2", "last"), RED, 1460)
        for j, (x, y) in enumerate(((300, 900), (420, 980), (240, 1020))):
            if at(t, "e2", "laugh.", -0.3 + j * 0.1): text(c, "HA", x, y, 60, RED, MARK_F)
        coin_rain(c, t, TW("e2", "laugh."), 8, 1461, 1300)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=1470, col=INK, fg=WHITE)
        bubble(c, "the friend who just joined a run club", 540, 680, pk(t, "z1", "friend"), (-180, 200), 54, 720)
        phone(c, 300, 1220, 0.55, 1471)
        runner(c, 800, 1440, t, 0.8, 1472, PNK, "FRIEND", True, 1.0, 0.7)
        arrow(c, 380, 1120, 700, 1020, 60, RED, 8, 1473, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "THICK OR THIN?", 540, 560, 84, INK, pk(t, "z2"))
        char(c, "chunky", 330, 1440, 0.5, t, 0, (0.4, 0), "happy", "cheer", blink=blink(t), label="THICK", seed=1474)
        thin_shoe(c, 790, 1300, 1.1, 1475)
        stamp(c, "THICK", 300, 880, 64, -6, sk(t, "z2", "Thick"), RED, 1476)
        stamp(c, "THIN", 790, 880, 64, 6, sk(t, "z2", "thin?"), INK, 1477)
        text(c, "?", 560, 1080, 140, RED, MARK_F)
        tape(c, "TELL ME IN THE COMMENTS", 540, 1480, 34, 2, pk(t, "z2", "comments."), seed=1478, col=WHITE)


RENDER = {k: globals()[k] for k, _, _ in SHOTLIST}


def _draw(sid, t, n):
    global BOIL
    BOIL = int(t * 12)
    c = SURF.getCanvas(); c.clear(skia.Color(*PAPER))
    if PLAT == "yt":   # YouTube cut: whole scene scaled 0.85 about (450,250) so nothing sits under the Shorts title row / button column
        page(c, None); c.save(); c.translate(450, 250); c.scale(0.85, 0.85); c.translate(-450, -250); c.clipRect(skia.Rect.MakeWH(W, H))
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
        cover_title(c, COVER[0], COVER[1], kk, 640)
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
