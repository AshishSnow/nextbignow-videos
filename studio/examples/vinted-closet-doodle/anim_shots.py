# VINTED "too many clothes to move" — real case study + 3 moves, SHORTS LENGTH (20 Nov 2026). DOODLE look, LIGHT page.
# Upgrade: the hook is the viewer's own closet (money already in your life) and the closet is the recurring set: it bulges on line 1,
# bursts on 'did.', and comes back for the callback with little price tags on every hanger.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: no app logo, no brand teal, no app UI; the name VINTED only as plain hand lettering; real people = plain doodles + name tapes.
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_flat", "b1", "whip"), ("S_map", "c1", "whip"), ("S_fee", "c5", "whip"),
         ("S_score", "d1", "whip"), ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "close."), "boing"), (TW("i1", "billion-euro"), "chaching"),
        (TW("i2", "did."), "slam"), (TW("i2", "did.", 0, 0.25), "whoosh"), (TW("i2", "Three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "secondhand"), "slide"), (TW("a1", "four"), "stamp"),
        (TW("b1", "eight,"), "stamp"), (TW("b1", "Lithuania."), "pop"),
        (TW("b2", "moving,"), "slam"), (TW("b2", "many"), "boing"),
        (TW("b3", "Justas"), "pop"), (TW("b3", "website."), "click"),
        (TW("b4", "Pass"), "whoosh"), (TW("b4", "friends."), "ding"),
        (TW("c1", "Vinted,"), "stamp"), (TW("c1", "abroad,"), "pop"), (TW("c1", "Francisco."), "whoosh"),
        (TW("c2", "burning"), "buzz"), (TW("c2", "fast."), "stamp"),
        (TW("c3", "dead"), "slam"), (TW("c3", "nine"), "tick"),
        (TW("c4", "third"), "whoosh"), (TW("c4", "offices"), "stamp"),
        (TW("c5", "surprising"), "pop"), (TW("c5", "fee"), "stamp"),
        (L0("b7"), "boing"), (TW("b7", "respect."), "ding"),
        (TW("d1", "work?"), "tick"), (TW("d1", "billion"), "chaching"),
        (TW("d2", "catch?"), "pop"), (TW("d2", "slipped,"), "slide"), (TW("d2", "sixty-two"), "stamp"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "honest"), "click"),
        (TW("m2", "Two:"), "stamp"), (TW("m2", "no"), "ding"),
        (TW("m3", "Three:"), "stamp"), (TW("m3", "busy"), "whoosh"),
        (L0("e1"), "boing"), (TW("e1", "Check"), "pop"), (TW("e2", "one"), "ding"),
        (L0("z1"), "whoosh"), (TW("z2", "sell,"), "stamp"), (TW("z2", "keep?"), "stamp")]


def lt(t, sid): return t - SHOT[sid]["start"]


import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("SHE HAD TOO MANY CLOTHES TO MOVE", "€1.1 BILLION REVENUE FROM OLD CLOTHES?")   # (kicker, TITLE) on frame 0 = the grid cover
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%€]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i1": "You've got a closet you can't close. Could it start a €1 billion company?",
        "i2": "One woman's did. 3 moves to sell yours at the end.",
        "a1": "Last year, secondhand clothes in America grew nearly 4x faster than regular clothing.",
        "b1": "It's 2008, in Lithuania.",
        "c4": "He cuts over a third of the staff and shuts offices abroad.",
        "d1": "Did it work? Last year, revenue passed €1 billion.",
        "d2": "The catch? Profit actually slipped, to €62 million.",
        "m1": "1: start with your own closet. Shoot honest photos.",
        "m2": "2: sell your own old stuff for less than you paid. Usually no tax.",
        "m3": "3: log every sale. Apps report busy sellers to the tax office."}
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


# ---------------------------------------------------------------- hook (i1-i2): YOU's closet bulges, bursts, 3 moves
def S_hook(c, t, n):
    base(c)
    live = t > COVER_T
    burst = live and at(t, "i2", "did.", -0.05)
    bul = 0.35 if not live else (0.35 + 0.65 * pr(t, L0("i1"), 1.4))
    closet(c, 600, 1440, 440, 740, 2001, 0.0 if burst else bul, 0.85 * eout(pr(t, TW("i2", "did."), 0.25)) if burst else 0.0, t,
           pr(t, TW("i2", "did.") + 0.05, 0.9) if burst else 0.0)
    if not burst:
        you(c, 290, 1440, t, 0.85, "push", "worried" if live else "neutral", (1, 0))
    else:
        you(c, 200, 1440, t, 0.8, "head", "shock", (1, -0.2))
    if not live: return
    if at(t, "i1", "billion-euro", -0.2) and not at(t, "i2", "Three", -0.3):
        fee_tag(c, 560, 560, 0.85, 2002, "€1 BILLION?", pk(t, "i1", "billion-euro"), -5)
        text(c, "?", 930, 720, 120, RED, MARK_F)
    if not burst and at(t, "i1", "close.", -0.2):
        tape(c, "YOUR CLOSET", 600, 1500, 40, 2, pk(t, "i1", "close."), seed=2003, col=WHITE)
    if burst: tape(c, "ONE WOMAN'S DID", 560, 1500, 40, -2, pk(t, "i2", "did."), seed=2004, col=WHITE)
    if at(t, "i2", "Three", -0.2):
        for j, x in enumerate((300, 540, 780)):
            moving_box(c, x, 650, 0.55, 2005 + j, str(j + 1), 0.0, pk(t, "i2", "Three", j * 0.12))
        stamp(c, "3 MOVES AT THE END", 540, 450, 56, -3, sk(t, "i2", "Three", 0.3), RED, 2009)


# ---------------------------------------------------------------- the trend (a1): secondhand bar races, regular clothing crawls
def S_trend(c, t, n):
    base(c)
    tape(c, "THE TREND: SECONDHAND", 540, 470, 50, -3, pk(t, "a1"), seed=2010, col=INK, fg=WHITE)
    g1 = eout(pr(t, L0("a1") + 0.2, 2.2)); g2 = eout(pr(t, L0("a1") + 0.2, 3.2))
    wline(c, [(140, 1300), (720, 1300)], 2011, 8)
    ink(c, wrrect(180, 1300 - 640 * g1, 390, 1300, 8, 2012, 1.4), GRN, 8)
    ink(c, wrrect(470, 1300 - 160 * g2, 680, 1300, 8, 2013, 1.4), GREY, 8)
    text(c, "SECONDHAND", 285, 1360, 34, INK, BLK_F); text(c, "ALL CLOTHING", 575, 1360, 34, INK, BLK_F)
    if g1 > 0.4: tee(c, 285, 1300 - 640 * g1 - 70, 0.6, BLU, -8, 2014, min(1.0, (g1 - 0.4) * 3), "jacket")
    you(c, 860, 1440, t, 0.7, "head" if at(t, "a1", "four", -0.2) else "stand", "shock" if at(t, "a1", "four", -0.2) else "neutral", (-1, 0))
    if at(t, "a1", "four", -0.3):
        stamp(c, "~4X FASTER", 660, 820, 90, 6, sk(t, "a1", "four"), RED, 2015)
        scribble(c, 285, 1300 - 640 * g1 + 40, 140, 70, pr(t, TW("a1", "four") + 0.2, 0.5), RED, 7, 2016)
        tape(c, "US RESALE, 2025 (THREDUP REPORT)", 540, 1490, 30, 1, pk(t, "a1", "four", 0.2), seed=2017, col=WHITE)


# ---------------------------------------------------------------- 2008, Lithuania (b1-b4): too many clothes -> a website -> friends
def S_flat(c, t, n):
    base(c)
    b2 = at(t, "b2", None, -0.1); b3 = at(t, "b3", None, -0.1); b4 = at(t, "b4", None, -0.1)
    if not b2:
        calendar(c, 720, 880, 2008, 1.0, pk(t, "b1", "eight,"), 2020)
        tape(c, "LITHUANIA", 330, 560, 60, -4, pk(t, "b1", "Lithuania."), seed=2021, col=WHITE)
        for j in range(3): building(c, 200 + j * 150, 1440, 120, 300 + 80 * (j % 2), (200, 214, 230), 2022 + j, None, j != 1)
        you(c, 880, 1440, t, 0.6, "stand", "neutral", (-1, 0))
        return
    if not b3:
        pile = pr(t, L0("b2"), 1.2)
        for j in range(int(4 + 10 * pile)):
            tee(c, 560 + (h01(j, 2030) - 0.5) * 300, 1400 - (j // 3) * 70 - h01(j, 2031) * 30, 0.75, _CLOTH_COLS[j % 9], (h01(j, 2032) - 0.5) * 70, 2033 + j, 1.0,
                ("tee", "jeans", "dress", "sock", "jacket")[j % 5])
        moving_box(c, 860, 1440, 0.62, 2050, "MOVING", 1.0, pk(t, "b2", "moving,"))
        person(c, 230, 1440, 0.85, 2051, PNK, t, "head" if at(t, "b2", "many", -0.2) else "stand", "MILDA MITKUTE", "worried", (1, 0), "long", 1.0, 32)
        if at(t, "b2", "many", -0.2):
            scribble(c, 560, 1180, 240, 230, pr(t, TW("b2", "many"), 0.5), RED, 8, 2052)
            stamp(c, "WAY TOO MANY", 600, 760, 70, -5, sk(t, "b2", "many"), RED, 2053)
        return
    person(c, 250, 1440, 0.8, 2060, BLU, t, "point", "JUSTAS JANAUSKAS", "happy", (1, 0), "short", pk(t, "b3", "Justas"), 28)
    nth = pr(t, TW("b3", "website.") - 0.3, 1.2) * 6
    browser(c, 620, 800, 560, 470, 2061, pk(t, "b3", "builds"), nth, None, 0.0)
    if at(t, "b3", "website.", -0.2) and not b4: tape(c, "A SIMPLE WEBSITE", 620, 500, 46, -3, pk(t, "b3", "website."), seed=2062, col=WHITE)
    if b4:
        for j, x in enumerate((540, 700, 860)):
            kk = pk(t, "b4", "Pass", j * 0.15)
            person(c, x, 1440, 0.5, 2063 + j, (ORG, PUR, TEAL)[j], t, "hold", None, "happy", (-1, 0), ("long", "short", "long")[j], kk)
            if kk > 0: tee(c, x + 40, 1440 - 0.5 * 160, 0.4, _CLOTH_COLS[j + 2], 0, 2066 + j, kk, ("tee", "dress", "jacket")[j])
            arrow(c, 620, 1040, x, 1180, 40 - j * 30, RED, 6, 2070 + j, pr(t, TW("b4", "Pass") + j * 0.15, 0.4), 24)
        stamp(c, "PASS ON TO FRIENDS", 600, 500, 56, -4, sk(t, "b4", "friends."), RED, 2073)


# ---------------------------------------------------------------- the map that burns (c1-c4)
def S_map(c, t, n):
    base(c)
    c3 = at(t, "c3", None, -0.1); c4 = at(t, "c4", None, -0.1)
    if not c3 or c4:
        pins = 4.0 if c4 else pr(t, TW("c1", "abroad,") - 0.3, 1.0) * 4
        sf = 1.0 if c4 else pr(t, TW("c1", "Francisco.") - 0.6, 0.6)
        gone = pr(t, TW("c4", "offices") - 0.3, 1.0) if c4 else 0.0
        euro_map(c, 520, 980, 0.86, 2080, t, pins, sf, gone, 1.0)
        title(c, "VINTED", 540, 520, 96, INK, pk(t, "c1", "Vinted,"), -3)
    if not c3:
        if at(t, "c2", None, -0.1):
            money_fire(c, 820, 1440, 0.9, t, 2081, pr(t, TW("c2", "burning") - 0.2, 1.0), 1.0)
            tape(c, "2016: STRUGGLING", 300, 1490, 40, -2, pk(t, "c2", "burning"), seed=2082)
            if at(t, "c2", "fast.", -0.2): text(c, "!", 950, 1100, 150, RED, MARK_F)
        return
    if not c4:
        person(c, 320, 1440, 0.9, 2090, (60, 60, 70), t, "point", "THOMAS PLANTENGA · NEW BOSS", "angry" if at(t, "c3", "dead", -0.2) else "neutral", (1, 0), "short", 1.0, 28)
        bubble(c, "\"If you continue like this, you'll be dead in nine months.\"", 560, 660, pk(t, "c3"), (-200, 260), 50, 760)
        for j in range(3): person(c, 640 + j * 120, 1440, 0.45, 2091 + j, (BLU, ORG, PUR, GRN)[j], t, "head" if at(t, "c3", "dead", -0.1) else "stand", None, "shock" if at(t, "c3", "dead", -0.1) else "neutral", (-1, 0), "short")
        if at(t, "c3", "nine", -0.2):
            wline(c, [(380, 800), (760, 800)], 2096, 8, RED)
            tape(c, "CITY AM INTERVIEW, 2024", 620, 900, 30, 2, pk(t, "c3", "nine", 0.3), seed=2097, col=WHITE)
        return
    walk = pr(t, TW("c4", "third") - 0.2, 1.4)
    for j in range(8):
        off = 700 * eout(walk) if j >= 5 else 0
        person(c, 140 + j * 100 + off, 1440, 0.36, 2100 + j, _CLOTH_COLS[j], t, "stand", None, "neutral", (1, 0), "short")
    if at(t, "c4", "third", -0.2): tape(c, "STAFF: 240 TO 150 (TECHCRUNCH)", 540, 1490, 32, 1, pk(t, "c4", "third"), seed=2110, col=WHITE)
    if at(t, "c4", "offices", -0.1): stamp(c, "OFFICES ABROAD: CLOSED", 540, 660, 50, -5, sk(t, "c4", "offices", 0.3), RED, 2111)


# ---------------------------------------------------------------- the fee (c5) + the hoodie (b7)
def S_fee(c, t, n):
    base(c)
    b7 = at(t, "b7", None, -0.1)
    if not b7:
        tape(c, "THE SURPRISING MOVE", 540, 470, 52, -3, pk(t, "c5"), seed=2120, col=INK, fg=WHITE)
        fee_tag(c, 520, 860, 1.25, 2121, "SELLER FEE", pk(t, "c5", "Sellers"), -6)
        if at(t, "c5", "fee", -0.2):
            strike(c, 260, 860, 780, pr(t, TW("c5", "fee") - 0.2, 0.3), RED, 16, 2122)
            stamp(c, "€0 TO SELL", 560, 1120, 90, 5, sk(t, "c5", "fee", 0.1), RED, 2123)
        you(c, 860, 1440, t, 0.65, "point" if at(t, "c5", "fee", -0.2) else "stand", "happy" if at(t, "c5", "fee", -0.2) else "neutral", (-1, -0.3))
        return
    fee_tag(c, 230, 1230, 0.5, 2121, "SELLER FEE", 1.0, -12); strike(c, 130, 1230, 340, 1.0, RED, 10, 2122)
    char(c, "hoodie", 620, 1440, 0.95, t, mth(t, ["b7"]), (-0.3, -0.2), "happy", "hips" if not at(t, "b7", "respect.", -0.2) else "cheer", blink=blink(t), seed=2124)
    bubble(c, "Free to list me? Finally, some respect.", 540, 560, pk(t, "b7"), (60, 200), 56, 720)
    if at(t, "b7", "respect.", -0.2): confetti(c, 620, 900, t, TW("b7", "respect."), 16, 2125)


# ---------------------------------------------------------------- did it work? (d1-d2) the scoreboard
def S_score(c, t, n):
    base(c)
    tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "d1"), seed=2130, col=INK, fg=WHITE)
    g = eout(pr(t, TW("d1", "revenue") - 0.2, 1.2))
    wline(c, [(120, 1360), (560, 1360)], 2131, 8)
    ink(c, wrrect(200, 1360 - 640 * g, 420, 1360, 8, 2132, 1.4), YEL, 8)
    wline(c, [(150, 1360 - 580), (520, 1360 - 580)], 2133, 6, RED, a=0.9)
    text(c, "€1 BILLION", 340, 1360 - 600, 34, RED, BLK_F)
    text(c, "REVENUE 2025", 310, 1410, 32, INK, BLK_F)
    if at(t, "d1", "billion", -0.2):
        wline(c, [(440, 820), (470, 850), (530, 760)], 2134, 12, RED)
        tape(c, "€1.1B (+38%)", 330, 640, 40, 2, pk(t, "d1", "billion"), seed=2135, col=WHITE)
    if at(t, "d2", None, -0.1):
        tape(c, "THE CATCH", 790, 640, 46, 3, pk(t, "d2", "catch?"), seed=2136)
        h1, h2 = 300, int(300 * 62 / 77 * 1.0)
        gg = eout(pr(t, TW("d2", "slipped,") - 0.2, 0.8))
        wline(c, [(620, 1360), (960, 1360)], 2137, 8)
        ink(c, wrrect(650, 1360 - h1, 770, 1360, 6, 2138, 1.2), GREY, 7)
        ink(c, wrrect(820, 1360 - (h1 - (h1 - h2) * gg), 940, 1360, 6, 2139, 1.2), ORG, 7)
        text(c, "2024", 710, 1410, 30, INK, BLK_F); text(c, "2025", 880, 1410, 30, INK, BLK_F)
        text(c, "€77M", 710, 1360 - h1 - 20, 32, INK, BLK_F)
        if at(t, "d2", "sixty-two", -0.2):
            text(c, "€62M", 880, 1360 - h2 - 20, 34, RED, BLK_F)
            arrow(c, 760, 900, 900, 1010, -30, RED, 8, 2140, pr(t, TW("d2", "sixty-two") - 0.2, 0.4))
            text(c, "NET PROFIT", 800, 820, 36, RED, MARK_F)
    else:
        you(c, 820, 1440, t, 0.75, "head" if at(t, "d1", "billion", -0.2) else "stand", "shock" if at(t, "d1", "billion", -0.2) else "neutral", (-1, 0))


# ---------------------------------------------------------------- 3 moves (m1-m3): one evolving board
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 450, 52, -3, pk(t, "m1"), seed=2150, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. START WITH YOUR OWN CLOSET"), ("m2", "Two:", "2. SOLD AT A LOSS? USUALLY NO TAX"), ("m3", "Three:", "3. LOG EVERY SALE")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=0)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 550 + i * 74; tape(c, lab, 500, y, 34, (-2, 2, -1)[i], pk(t, l, w), seed=2151 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(880, y - 5), (900, y + 15), (940, y - 25)], 2155 + i, 8, RED)
    if cur == 0:
        hanger(c, 330, 840, 1.6, 2160); tee(c, 330, 1010, 1.25, BLU, 0, 2161, 1.0, "jacket")
        you(c, 820, 1440, t, 0.8, "hold", "happy", (-1, 0))
        phone(c, 700, 1120, 0.38, 2162)
        fl = 1 - pr(t, TW("m1", "honest"), 0.3) if at(t, "m1", "honest", -0.02) else 0.0
        if fl > 0: c.drawCircle(700, 1080, 160 * fl, P(YEL, 0.6 * fl))
        if at(t, "m1", "honest", -0.2): tape(c, "HONEST PHOTOS: SHOW THE FLAWS", 470, 1490, 32, 1, pk(t, "m1", "honest"), seed=2163, col=WHITE)
        if at(t, "m1", "own", -0.2): scribble(c, 330, 1010, 170, 160, pr(t, TW("m1", "own"), 0.5), RED, 7, 2164)
    elif cur == 1:
        fee_tag(c, 330, 930, 0.7, 2170, "PAID $60", pk(t, "m2", "paid."), -6)
        fee_tag(c, 330, 1130, 0.7, 2171, "SOLD $25", pk(t, "m2", "less"), 4)
        you(c, 800, 1440, t, 0.8, "shrug" if at(t, "m2", "no", -0.2) else "stand", "happy", (-1, 0))
        if at(t, "m2", "no", -0.2):
            stamp(c, "USUALLY NO TAX", 620, 820, 56, 6, sk(t, "m2", "no"), GRN, 2172)
            tape(c, "US: OWN STUFF SOLD AT A LOSS (IRS) · UK: NOT TRADING (HMRC)", 540, 1490, 26, 1, pk(t, "m2", "no", 0.2), seed=2173, col=WHITE)
    else:
        ledger(c, 320, 1080, 0.8, 2180, pr(t, TW("m3", "log") - 0.1, 1.4) * 5, pk(t, "m3", "Three:"))
        building(c, 790, 1440, 280, 400, (220, 220, 230), 2181, None, False)
        text(c, "TAX OFFICE", 790, 1010, 40, INK, MARK_F)
        if at(t, "m3", "busy", -0.2):
            u = eout(pr(t, TW("m3", "busy") - 0.2, 0.8))
            envelope(c, 480 + 300 * u, 900 - 60 * math.sin(math.pi * u), 0.6, 2182, False)
            tape(c, "US: OVER $20,000 AND 200+ SALES · UK: 30+ SALES OR £1,700+", 540, 1490, 26, 1, pk(t, "m3", "busy", 0.3), seed=2183, col=WHITE)


# ---------------------------------------------------------------- callback (e1-e2): the same closet, now with price tags
def S_end(c, t, n):
    base(c)
    op = eout(pr(t, TW("e1", "Check") - 0.1, 0.4)) if at(t, "e1", "Check", -0.1) else 0.0
    closet(c, 600, 1440, 440, 740, 2001, 0.8 * (1 - op), op * 0.85, t, 0.0, pr(t, TW("e1", "Check") + 0.3, 1.2))
    you(c, 230, 1440, t, 0.85, "point" if op > 0 else "push", "happy" if op > 0.5 else "worried", (1, 0))
    if not op: text(c, "?", 900, 620, 130, RED, MARK_F)
    if at(t, "e2", None, -0.1):
        tape(c, "2008: IT STARTED WITH ONE LIKE THIS", 560, 560, 40, -3, pk(t, "e2"), seed=2190)
        wline(c, [(860, 760), (880, 790), (930, 720)], 2191, 10, RED)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=2200, col=INK, fg=WHITE)
        bubble(c, "the friend whose closet won't shut", 540, 680, pk(t, "z1", "friend"), (-180, 200), 52, 740)
        phone(c, 260, 1200, 0.5, 2201)
        moving_box(c, 760, 1440, 0.7, 2202, "STUFF", 1.0)
        person(c, 760, 1240, 0.55, 2203, PNK, t, "up", "FRIEND", "worried", (-1, 0), "long", 1.0, 30)
        arrow(c, 330, 1100, 640, 1040, 60, RED, 8, 2204, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "SELL OR KEEP?", 540, 540, 86, INK, pk(t, "z2"))
        hanger(c, 540, 820, 1.6, 2210); tee(c, 540, 990, 1.25, BLU, 0, 2161, 1.0, "jacket")
        stamp(c, "SELL", 250, 1100, 80, -6, sk(t, "z2", "sell,"), GRN, 2211)
        stamp(c, "KEEP", 840, 1100, 80, 6, sk(t, "z2", "keep?"), RED, 2212)
        tape(c, "COMMENT BELOW", 540, 1480, 36, 2, pk(t, "z2", "Comment"), seed=2213, col=WHITE)


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
