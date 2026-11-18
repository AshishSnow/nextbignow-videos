# HUY FONG SRIRACHA "the hot sauce that never paid for an ad" — real case study + 3 moves, SHORTS LENGTH (19 Nov 2026). DOODLE look, LIGHT page.
# Upgrade: "Would you pay $70 for one bottle?" price hook on the cover + line 1 (the eBay listing card is the hero object on frame 0).
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: generic red squeeze bottle (white cap, no rooster, no green cap), generic listing card (no site branding),
# David Tran = plain doodle person with a name tape (no likeness). Single cut (IG + YT share one file).
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_ship", "b1", "whip"), ("S_van", "b3", "whip"), ("S_sauce", "b5", "pop"),
         ("S_work", "b7", "whip"), ("S_farm", "c1", "whip"), ("S_short", "c4", "whip"), ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "seventy"), "chaching"), (TW("i1", "hot"), "pop"), (TW("i2", "eBay"), "click"), (TW("i2", "twenty-three."), "stamp"),
        (L0("i3"), "whoosh"), (TW("i3", "Three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "spicy"), "pop"), (TW("a1", "ninety-five"), "stamp"),
        (L0("b1"), "whoosh"), (TW("b1", "freighter"), "honk"), (TW("b2", "Angeles,"), "pop"), (TW("b2", "ship."), "ding"),
        (L0("b3"), "whoosh"), (TW("b3", "blue"), "honk"), (TW("b4", "budget?"), "pop"), (TW("b4", "dime."), "stamp"),
        (L0("b5"), "boing"), (TW("b5", "ad."), "ding"),
        (TW("b7", "work?"), "tick"), (TW("b8", "twenty"), "chaching"), (TW("b8", "year."), "stamp"),
        (TW("c1", "one"), "pop"), (TW("c1", "farm."), "ding"), (TW("c2", "split,"), "buzz"), (TW("c2", "court."), "stamp"),
        (TW("c3", "jury"), "pop"), (TW("c3", "twenty-three"), "slam"),
        (TW("c4", "weather"), "whoosh"), (TW("c5", "scarce,"), "buzz"), (TW("c5", "seventy"), "chaching"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "acidified"), "ding"), (TW("m1b", "sell"), "buzz"), (TW("m1b", "yours."), "tick"),
        (TW("m2", "Two:"), "stamp"), (TW("m2", "authority."), "stamp"),
        (TW("m3", "Three:"), "stamp"), (TW("m3", "backup"), "ding"),
        (TW("e1", "Seventy"), "chaching"), (TW("e1", "never"), "stamp"), (L0("z1"), "whoosh"), (TW("z2", "Mild,"), "stamp"), (TW("z2", "hot?"), "stamp")]


def lt(t, sid): return t - SHOT[sid]["start"]



import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("THE SAUCE THAT NEVER PAID FOR ADS", "$70 FOR ONE BOTTLE?")   # (kicker, TITLE) on frame 0 = the grid cover (LIGHT page, listing card + sauce below)
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i1": "Would you pay $70 for one bottle of hot sauce?",
        "i2": "That's what eBay sellers asked in 2023.",
        "i3": "You want to bottle your own? 3 moves at the end.",
        "a1": "One menu tracker says spicy food is on 95% of American menus.",
        "b8": "Bloomberg reported it sold 20 million bottles in one year.",
        "c1": "But for almost 30 years, most of its peppers come from one farm.",
        "c3": "A jury awards the farm over $23 million from Huy Fong.",
        "c5": "The result? Bottles get scarce, and one hits $70 online.",
        "m1": "Your moves. 1: hot sauce usually counts as an acidified food.",
        "m2": "2: who signs off on your recipe? A process authority.",
        "m3": "3: never lean on one farm. Try a backup supplier.",
        "e1": "Honestly? $70, for a sauce that never paid for an ad."}
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



# ---------------------------------------------------------------- hook (i1-i3): the $70 listing card, YOU, 3 moves
def S_hook(c, t, n):
    base(c)
    live = t > COVER_T
    i3 = at(t, "i3", None, -0.1) and live
    lk = 1.0 if not i3 else 1.0 - 0.35 * eout(pr(t, L0("i3") - 0.1, 0.4))
    lx = 690 if not i3 else 760
    if not at(t, "i3", "Three", -0.3) or not live: listing(c, lx, (1130 if not live else 1060) if not i3 else 980, 0.95 * lk, 1300, "$70", 1.0)
    char(c, "sauce", 250, 1440, 0.72, t, 0.0, (0.5, -0.2), "shock" if live and at(t, "i1", "seventy", -0.1) else "neutral", "hips", blink=blink(t) and live, seed=1301)
    if not live: return
    if at(t, "i1", "seventy", -0.1) and not i3:
        scribble(c, lx - 57, 1236, 120, 70, pr(t, TW("i1", "seventy"), 0.5), RED, 8, 1302)
        text(c, "?!", 930, 760, 110, RED, MARK_F)
    if at(t, "i2", None, -0.1) and not i3:
        tape(c, "EBAY SELLERS ASKED THIS", 470, 600, 50, -3, pk(t, "i2", "eBay"), seed=1303)
        if at(t, "i2", "twenty-three.", -0.2): stamp(c, "2023", 300, 760, 80, -8, sk(t, "i2", "twenty-three."), RED, 1304)
    if i3:
        you(c, 470, 1440, t, 0.85, "point" if at(t, "i3", "Three", -0.2) else "wave", "happy", (1, 0), pk(t, "i3"))
        if at(t, "i3", "Three", -0.2):
            for j, x in enumerate((300, 520, 740)):
                chili(c, x, 640, 0.8, (-20, 10, 30)[j], 1306 + j, k=pk(t, "i3", "Three", j * 0.12)); text(c, str(j + 1), x + 40, 560, 56, INK, MARK_F)
            stamp(c, "3 MOVES AT THE END", 540, 820, 52, -3, sk(t, "i3", "Three", 0.3), RED, 1309)


# ---------------------------------------------------------------- the trend (a1): a menu fills with chilies, 95%
def S_trend(c, t, n):
    base(c)
    tape(c, "THE TREND: SPICY EVERYTHING", 540, 470, 50, -3, pk(t, "a1"), seed=1310, col=INK, fg=WHITE)
    nh = int(pr(t, TW("a1", "spicy") - 0.1, 1.6) * 7)
    menu(c, 330, 1060, 1.0, 1311, pk(t, "a1"), nh)
    you(c, 790, 1440, t, 0.8, "head" if at(t, "a1", "ninety-five", -0.2) else "stand", "shock" if at(t, "a1", "ninety-five", -0.2) else "neutral", (-1, 0))
    if at(t, "a1", "ninety-five", -0.3):
        stamp(c, "95%", 760, 700, 120, 6, sk(t, "a1", "ninety-five"), RED, 1312)
        tape(c, "OF US RESTAURANT MENUS (DATASSENTIAL, 2025)", 540, 1490, 28, 1, pk(t, "a1", "ninety-five", 0.2), seed=1313, col=WHITE)


# ---------------------------------------------------------------- the ship (b1-b2): freighter crosses, lands in LA, names the company
def S_ship(c, t, n):
    base(c, gy=1500)
    b2 = at(t, "b2", None, -0.1)
    u = pr(t, L0("b1"), (L1("b1") - L0("b1")) + 0.4)
    if not b2:
        tape(c, "VIETNAM", 230, 520, 54, -4, pk(t, "b1", "Vietnam"), seed=1320, col=WHITE)
        arrow(c, 300, 600, 820, 600, -60, RED, 8, 1321, pr(t, TW("b1", "Vietnam"), 1.2))
        freighter(c, 200 + 520 * eout(u), 1150, 0.82, t, 1322, "HUY FONG", 1.0)
        person(c, 200 + 520 * eout(u) + 200, 1150 - 270 * 0.82 - 10, 0.42, 1323, (60, 90, 160), t, "wave", None, "worried", (1, 0), "short", 1.0)
        tape(c, "DAVID TRAN", 540, 1330, 40, 2, pk(t, "b1", "Tran"), seed=1324)
        if at(t, "b1", "freighter", -0.2): scribble(c, 200 + 520 * eout(u), 1110, 160, 50, pr(t, TW("b1", "freighter") + 0.3, 0.5), RED, 7, 1325)
    else:
        building(c, 700, 1500, 380, 560, SKY, 1326, None, True)
        tape(c, "LOS ANGELES", 300, 520, 58, -4, pk(t, "b2", "Angeles,"), seed=1327)
        person(c, 260, 1500, 0.8, 1323, (60, 90, 160), t, "point" if at(t, "b2", "ship.", -0.3) else "stand", "DAVID TRAN", "happy", (1, 0), "short", pk(t, "b2"))
        if at(t, "b2", "names", -0.2):
            tape(c, "HUY FONG FOODS", 700, 900, 46, 3, pk(t, "b2", "names"), seed=1328, col=WHITE)
        if at(t, "b2", "ship.", -0.2):
            freighter(c, 700, 640, 0.28, t, 1329, "", 1.0)
            text(c, "= THE SHIP'S NAME", 700, 760, 34, RED, MARK_F)


# ---------------------------------------------------------------- the blue van + no ads (b3-b4)
def S_van(c, t, n):
    base(c)
    u = pr(t, L0("b3"), 1.4)
    vx = -300 + 820 * eout(u)
    van(c, vx, 1440, 1.0, t, 1330, BLU, 1.0, 1 - u if u < 1 else 0.0)
    tape(c, "DELIVERS IT HIMSELF", 400, 520, 50, -3, pk(t, "b3", "himself,"), seed=1331, col=WHITE)
    if at(t, "b3", "blue", -0.2): tape(c, "THE BLUE VAN", 420, 640, 46, 3, pk(t, "b3", "blue"), seed=1332)
    if at(t, "b4", None, -0.1):
        billboard(c, 760, 1060, 0.7, "ADS $$$", 1333, RED)
        if at(t, "b4", "dime.", -0.3):
            strike(c, 560, 1000, 960, pr(t, TW("b4", "dime.") - 0.3, 0.3), RED, 14, 1334)
            stamp(c, "$0 ON ADS", 700, 800, 70, 6, sk(t, "b4", "dime."), RED, 1335)


# ---------------------------------------------------------------- the bottle talks (b5)
def S_sauce(c, t, n):
    base(c)
    char(c, "sauce", 540, 1440, 1.15, t, mth(t, ["b5"]), (-0.3, -0.2), "happy", "hips" if not at(t, "b5", "ad.", -0.2) else "cheer", blink=blink(t), seed=1340)
    bubble(c, "Ads? Sweetie, I'm the ad.", 560, 580, pk(t, "b5"), (40, 260), 60, 700)
    if at(t, "b5", "ad.", -0.2): confetti(c, 540, 1000, t, TW("b5", "ad."), 18, 1341)


# ---------------------------------------------------------------- did it work? (b7-b8): bottles pile up, 20 million
def S_work(c, t, n):
    base(c)
    tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "b7"), seed=1350, col=INK, fg=WHITE)
    if not at(t, "b8", "twenty", -0.6):
        char(c, "sauce", 420, 1440, 0.8, t, 0, (0.4, -0.3), "worried", "hips", blink=blink(t), seed=1349)
        for j in range(3): text(c, "?", 640 + j * 90, 900 - j * 60, 120 - j * 20, RED, MARK_F, a=min(1.0, pr(t, L0("b7") + j * 0.25, 0.3)))
    g = pr(t, TW("b8", "twenty") - 0.6, 1.6)
    nb = int(g * 21)
    for j in range(nb):
        r_, cpos = divmod(j, 6)
        bx = 250 + cpos * 100 + (r_ % 2) * 50; by = 1440 - r_ * 150
        ink(c, wpoly([(bx - 34, by), (bx - 38, by - 90), (bx - 20, by - 130), (bx + 20, by - 130), (bx + 38, by - 90), (bx + 34, by)], 1351 + j, 1.4, True, 30), (226, 46, 38), 6)
        ink(c, wrrect(bx - 20, by - 150, bx + 20, by - 126, 5, 1380 + j, 0.8), WHITE, 5)
    if at(t, "b8", "twenty", -0.2):
        stamp(c, "20 MILLION BOTTLES", 540, 640, 74, -4, sk(t, "b8", "twenty"), RED, 1352)
        tape(c, "IN ONE YEAR (2012, BLOOMBERG)", 540, 760, 40, 2, pk(t, "b8", "year."), seed=1353, col=WHITE)
    you(c, 870, 1440, t, 0.7, "head" if at(t, "b8", "million", -0.2) else "stand", "shock" if at(t, "b8", "million", -0.2) else "neutral", (-1, 0))


# ---------------------------------------------------------------- one farm -> split -> court (c1-c3)
def S_farm(c, t, n):
    base(c)
    court = at(t, "c3", None, -0.1)
    if not court:
        farm(c, 400, 1440, 640, 1360, "ONE PEPPER FARM", pk(t, "c1"), 4, True)
        building(c, 850, 1440, 220, 380, SKY, 1361, "SAUCE", True)
        split = at(t, "c2", "split,", -0.2)
        if not split:
            arrow(c, 620, 1000, 780, 1000, -40, RED, 9, 1362, pr(t, TW("c1", "farm."), 0.5))
            tape(c, "~28 YEARS OF PEPPERS", 540, 620, 50, -3, pk(t, "c1", "thirty"), seed=1363)
            text(c, "(MOST OF THEM)", 540, 720, 36, INK, MARK_F)
        else:
            wline(c, [(700, 860), (680, 940), (720, 1000), (690, 1080), (720, 1160)], 1364, 12, RED)
            stamp(c, "SPLIT", 540, 640, 90, -6, sk(t, "c2", "split,"), RED, 1365)
            if at(t, "c2", "court.", -0.2): tape(c, "SEE YOU IN COURT", 540, 780, 46, 3, pk(t, "c2", "court."), seed=1366, col=WHITE)
    else:
        jury_box(c, 380, 1440, 0.95, 1367, t, pk(t, "c3", "jury"))
        gavel(c, 790, 1260, 0.9, 1368, pr(t, TW("c3", "twenty-three") - 0.25, 0.25), 1.0)
        tape(c, "JURY AWARD TO THE FARM", 540, 520, 46, -3, pk(t, "c3", "awards"), seed=1369)
        if at(t, "c3", "twenty-three", -0.2):
            stamp(c, "$23M+", 700, 700, 110, 6, sk(t, "c3", "twenty-three"), RED, 1370)
            tape(c, "2019, UPHELD ON APPEAL 2021", 380, 820, 32, -2, pk(t, "c3", "twenty-three", 0.3), seed=1371, col=WHITE)


# ---------------------------------------------------------------- shortage (c4-c5): storm over the field, empty shelf, $70 is back
def S_short(c, t, n):
    base(c)
    c5 = at(t, "c5", "scarce,", -0.2)
    if not at(t, "c5", "seventy", -0.3):
        farm(c, 540, 1440, 760, 1380, None, 1.0, 4, True, pr(t, TW("c4", "weather") - 0.2, 0.8))
        raincloud(c, 560, 860, 1.1, t, 1381, pk(t, "c4", "weather", -0.3))
        tape(c, "HUY FONG: BAD WEATHER HURT THE CHILIES", 540, 520, 36, -3, pk(t, "c4"), seed=1382, col=WHITE)
        if c5: stamp(c, "SHORTAGE (2022-23)", 540, 650, 64, -5, sk(t, "c5", "scarce,"), RED, 1383)
    else:
        shelf(c, 330, 1300, 0, 520, 1384, 2, 4, "HOT SAUCE")
        tape(c, "EMPTY SHELVES", 330, 700, 44, -3, 1.0, seed=1385, col=WHITE)
        listing(c, 760, 1020, 0.7, 1386, "$70", pk(t, "c5", "seventy"))
        scribble(c, 718, 1143, 100, 60, pr(t, TW("c5", "seventy") + 0.2, 0.5), RED, 8, 1387)
        you(c, 160, 1440, t, 0.7, "head", "shock", (1, -0.3))


# ---------------------------------------------------------------- 3 moves (m1-m3): one evolving board
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 450, 52, -3, pk(t, "m1"), seed=1400, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. KNOW THE ACIDIFIED-FOOD RULES"), ("m2", "Two:", "2. GET A PROCESS AUTHORITY"), ("m3", "Three:", "3. TWO SUPPLIERS, NOT ONE")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=-1)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 550 + i * 74; tape(c, lab, 520, y, 34, (-2, 2, -1)[i], pk(t, l, w), seed=1401 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(900, y - 5), (920, y + 15), (960, y - 25)], 1405 + i, 8, RED)
    if cur <= 0:
        if not at(t, "m1b", None, -0.1):
            char(c, "sauce", 330, 1440, 0.8, t, 0, (0.4, -0.2), "neutral", "hips", blink=blink(t), seed=1410)
            tape(c, "pH 4.6 OR LESS = ACIDIFIED", 690, 900, 36, 3, pk(t, "m1", "acidified"), seed=1411, col=WHITE)
            text(c, "FDA RULES: 21 CFR 114", 690, 1010, 34, INK, MARK_F)
            you(c, 790, 1440, t, 0.75, "stand", "neutral", (-1, 0))
        else:
            stove(c, 380, 1440, 0.95, 1412, 1.0, pr(t, TW("m1b", "sell") - 0.1, 0.4))
            tape(c, "E.G. CONNECTICUT: NO HOT SAUCE AS A COTTAGE FOOD", 540, 1490, 26, 1, pk(t, "m1b", "kitchen."), seed=1413, col=WHITE)
            you(c, 790, 1440, t, 0.8, "point" if at(t, "m1b", "yours.", -0.2) else "head", "worried", (-1, 0))
            if at(t, "m1b", "yours.", -0.2): stamp(c, "CHECK YOUR STATE", 720, 860, 50, 6, sk(t, "m1b", "yours."), RED, 1414)
    elif cur == 1:
        clipboard(c, 330, 1100, 0.9, 1420, "RECIPE", pk(t, "m2", "Two:"), int(pr(t, TW("m2", "authority.") - 0.2, 1.0) * 4))
        person(c, 730, 1440, 0.8, 1421, PUR, t, "point", "PROCESS AUTHORITY", "happy", (-1, 0), "bald", pk(t, "m2", "authority."))
        if at(t, "m2", "authority.", -0.1): stamp(c, "APPROVED", 330, 860, 60, -6, sk(t, "m2", "authority.", 0.4), GRN, 1422)
        if at(t, "m2", "authority.", 0.6):
            tape(c, "SOME CO-PACKERS CAN HELP", 700, 780, 34, 3, pk(t, "m2", "authority.", 0.6), seed=1424, col=WHITE)
    else:
        farm(c, 300, 1440, 440, 1430, "FARM A", pk(t, "m3", "Three:"), 3, True)
        farm(c, 780, 1440, 440, 1431, "FARM B", pk(t, "m3", "backup", -0.1), 3, True)
        if at(t, "m3", "backup", -0.2): stamp(c, "BACKUP", 780, 900, 70, 6, sk(t, "m3", "backup"), RED, 1432)
        if at(t, "m3", "farm.", -0.2) and not at(t, "m3", "backup", -0.2): scribble(c, 300, 1300, 240, 140, pr(t, TW("m3", "farm."), 0.5), RED, 8, 1433)


# ---------------------------------------------------------------- callback ending (e1)
def S_end(c, t, n):
    base(c)
    listing(c, 720, 1020, 0.75, 1300, "$70", 1.0)
    char(c, "sauce", 270, 1440, 0.85, t, 0, (0.5, -0.2), "happy", "cheer" if at(t, "e1", "never", -0.2) else "hips", blink=blink(t), seed=1301)
    title(c, "HONESTLY?", 540, 520, 80, INK, pk(t, "e1"), -2)
    if at(t, "e1", "never", -0.2):
        stamp(c, "$0 ON ADS", 700, 680, 80, -6, sk(t, "e1", "never"), RED, 1440)
        coin_rain(c, t, TW("e1", "never"), 8, 1441, 1300)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=1450, col=INK, fg=WHITE)
        bubble(c, "the friend who puts hot sauce on everything", 540, 690, pk(t, "z1", "friend"), (-180, 200), 52, 740)
        phone(c, 300, 1220, 0.55, 1451)
        person(c, 780, 1440, 0.8, 1452, PNK, t, "hold", "FRIEND", "happy", (-1, 0), "long")
        char(c, "sauce", 900, 1440, 0.32, t, 0, (-0.5, 0), "happy", "down", seed=1453)
        arrow(c, 380, 1120, 680, 1040, 60, RED, 8, 1454, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "MILD OR EXTRA HOT?", 540, 540, 78, INK, pk(t, "z2"))
        chili(c, 320, 1100, 1.2, -15, 1455, (120, 200, 90))
        for j in range(3): chili(c, 700 + j * 90, 1100 + (j % 2) * 40, 1.1, 10 + j * 10, 1456 + j)
        stamp(c, "MILD", 320, 860, 64, -6, sk(t, "z2", "Mild,"), GRN, 1460)
        stamp(c, "EXTRA HOT", 790, 860, 64, 6, sk(t, "z2", "hot?"), RED, 1461)
        tape(c, "TELL ME IN THE COMMENTS", 540, 1480, 34, 2, pk(t, "z2", "comments."), seed=1462, col=WHITE)



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
