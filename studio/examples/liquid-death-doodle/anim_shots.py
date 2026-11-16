# LIQUID DEATH "the ad came before the water" — real case study + 3 moves, SHORTS LENGTH (17 Nov 2026). DOODLE look, BLACK + YELLOW theme:
# yellow-washed graph paper, black ink, cream/white cards, red marker only for annotations; charcoal + yellow title cover on frame 0.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: the can is a plain grey tallboy with a tape label; Mike Cessario + band = plain doodles with name tapes.
# Two platform cuts: OMB_PLAT=ig (full frame) / OMB_PLAT=yt (scene scaled 0.85 about (450,250), strip + cover unscaled).
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_fest", "b1", "whip"), ("S_doors", "b3", "whip"), ("S_ad", "b5", "whip"),
         ("S_store", "b8", "whip"), ("S_map", "c1", "whip"), ("S_moves", "m1", "whip"), ("S_end", "e1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "water"), "pop"), (TW("i1", "Death?"), "stamp"), (TW("i2", "billion"), "chaching"), (TW("i3", "Three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "half"), "whoosh"), (TW("a1", "Gallup"), "pop"), (TW("b1", "Cessario"), "pop"), (TW("b1", "ads."), "ding"),
        (TW("b2", "festival,"), "pop"), (TW("b2", "water"), "ding"),
        (TW("b3", "pass.", 0, -0.3), "stamp"), (TW("b3", "pass."), "stamp"), (TW("b3", "pass.", 0, 0.3), "stamp"), (TW("b4", "check"), "click"),
        (TW("b5", "first:"), "stamp"), (TW("b5", "video,"), "pop"), (TW("b5", "fake"), "whoosh"), (TW("b7", "work?"), "pop"), (TW("b7", "views,"), "chaching"),
        (TW("b7", "sale."), "stamp"), (TW("b8", "checks,"), "chaching"), (TW("b8", "ship."), "pop"), (TW("b9", "quarter"), "ding"),
        (TW("c1", "catch?"), "stamp"), (TW("c1", "paused"), "stamp"), (TW("c1", "Britain"), "buzz"), (TW("c2", "all"), "click"),
        (TW("m1", "One:"), "stamp"), (TW("m2", "Two:"), "stamp"), (TW("m2", "proof."), "stamp"), (TW("m3", "Three:"), "stamp"), (TW("m3", "loud"), "pop"),
        (TW("e1", "joke."), "ding"), (L0("z1"), "whoosh"), (TW("z2", "Boring"), "stamp"), (TW("z2", "loud"), "stamp")]
def lt(t, sid): return t - SHOT[sid]["start"]



import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("THE AD CAME BEFORE THE WATER", "$1.4 BILLION FOR WATER IN A CAN?")   # (kicker, TITLE) on frame 0 = the grid cover (black + yellow)
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i2": "Investors valued it at $1.4 billion.", "i3": "You want your own brand? 3 moves at the end.",
        "b7": "Did it work? 1,000,000+ views, before it was even on sale.",
        "c1": "The catch? In 2025, it paused sales outside America, Britain included.",
        "m1": "Your moves. 1: test it with a video before making anything.", "m2": "2: count who asks where to buy. That's your proof.",
        "m3": "3: take a boring product, and give it a loud personality."}
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


# ---------------------------------------------------------------- hook (i1-i3): fridge, one plain tall can, $1.4B, YOU
def S_hook(c, t, n):
    base(c, a=0.30)
    op = pr(t, 0.2, 0.6) if t > COVER_T - 0.4 else 1.0
    shelves = fridge(c, 760, 1400, 520, 820, 1.0, 1100)
    for j, x in enumerate((560, 640, 720, 800)): bottle(c, x, shelves[0], 0.7, 1101 + j)
    for j, x in enumerate((570, 690, 810, 930)):
        if j != 3: bottle(c, x, shelves[1], 0.7, 1105 + j, (58, 160, 90))
    mood = "happy" if at(t, "i2", "billion", -0.1) else "neutral"
    char(c, "tallcan", 760, 1440, 0.9, t, 0.0, (-0.5, -0.2), mood, "hips" if not at(t, "i2", None) else "up", blink=blink(t))
    if t < COVER_T + 0.2: return
    tape(c, "PLAIN WATER?", 300, 720, 52, -4, pk(t, "i1", "water"), seed=1110, col=WHITE)
    if at(t, "i1", "Death?", -0.3): tape(c, "\"LIQUID DEATH\"", 330, 860, 50, 4, pk(t, "i1", "Death?", -0.3), seed=1111)
    if at(t, "i1", "can", -0.2) and not at(t, "i3", None, -0.1): scribble(c, 760, 1150, 170, 250, pr(t, TW("i1", "can") - 0.2, 0.5), RED, 9, 1112)
    if at(t, "i2", None, -0.1):
        stamp(c, "$1.4 BILLION\n(2024 VALUATION)", 270, 1040, 46, -6, sk(t, "i2", "billion"), RED, 1113)
        coin_rain(c, t, TW("i2", "billion"), 8, 1114, 1300)
    if at(t, "i3", None, -0.1):
        you(c, 200, 1440, t, 0.95, "head", "worried" if not at(t, "i3", "Three", -0.1) else "happy", (1, 0), pk(t, "i3"))
        if at(t, "i3", "Three", -0.2): stamp(c, "3 MOVES AT THE END", 540, 470, 56, -3, sk(t, "i3", "Three"), INK, 1115)


# ---------------------------------------------------------------- the trend (a1): a fridge shelf of drinks, half struck out
def S_trend(c, t, n):
    base(c, a=0.18)
    tape(c, "THE TREND", 540, 560, 64, -3, pk(t, "a1"), seed=1120, col=INK, fg=BY)
    cut = pr(t, TW("a1", "half") - 0.1, 0.6)
    for j in range(8):
        x = 160 + j * 108; bottle(c, x, 1100, 0.95, 1121 + j, (150, 96, 60) if j % 2 else (58, 160, 90), pk(t, "a1", None, j * 0.06), 1.0 if j < 4 else 1 - 0.65 * cut)
    if cut > 0: strike(c, 560, 970, 1000, cut, RED, 14, 1130); strike(c, 560, 1030, 1000, pr(t, TW("a1", "half"), 0.6), RED, 14, 1131)
    if at(t, "a1", "Gallup", -0.1): tape(c, "UNDER 35: ONLY HALF DRINK", 540, 700, 46, 2, pk(t, "a1", "Gallup"), seed=1132, col=WHITE)
    if at(t, "a1", "Gallup", -0.1): tape(c, "GALLUP 2025", 760, 790, 32, -3, pk(t, "a1", "Gallup", 0.2), seed=1133)
    you(c, 540, 1440, t, 0.8, "shrug" if at(t, "a1", "now.", -0.3) else "stand", "neutral", (0, 0), pk(t, "a1", "young"))


# ---------------------------------------------------------------- the festival (b1-b2)
def S_fest(c, t, n):
    base(c, a=0.14)
    stage(c, 540, 1180, t, 1140)
    drum(c, 660, 1060, 0.9, 1141)
    person(c, 420, 1060, 0.62, 1142, (40, 40, 52), t, "hold" if at(t, "b2", "drinking", -0.2) else "wave", "BAND", "happy", (1, 0), "long")
    person(c, 220, 1440, 1.0, 1143, (90, 60, 40), t, "point" if at(t, "b2", "sees", -0.1) else "stand", "MIKE CESSARIO", "neutral", (1, -0.3), "short", pk(t, "b1", "Cessario"))
    crowd(c, 640, 1440, 10, 5, pk(t, "b1", None), 1144, 0.8)
    tape(c, "AD MAN", 220, 870, 44, -5, pk(t, "b1", "ads."), seed=1145, col=WHITE)
    calendar(c, 880, 640, "2009", 0.6, pk(t, "b1", "ads."), 1146, INK)
    if at(t, "b2", None, -0.1): tape(c, "MUSIC FESTIVAL", 460, 560, 52, -3, pk(t, "b2", "festival,"), seed=1147)
    if at(t, "b2", "drinking", -0.2):
        c.save(); c.translate(500, 960); c.scale(0.28, 0.28); _tallcan(c, 0, 0, 1.0, t, 0, (0, 0), "neutral", "down", False, False, 1148, label="ENERGY"); c.restore()
        bubble(c, "...it's water!", 740, 800, pk(t, "b2", "water"), (-200, 140), 44, 360)
        if at(t, "b2", "cans.", -0.2): scribble(c, 500, 900, 70, 110, pr(t, TW("b2", "cans.") - 0.2, 0.4), RED, 7, 1149)


# ---------------------------------------------------------------- investors pass (b3-b4)
def S_doors(c, t, n):
    base(c, a=0.20)
    ts = [TW("b3", "pass.", 0, -0.3), TW("b3", "pass.", 0, 0.0), TW("b3", "pass.", 0, 0.3)]
    for j, x in enumerate((230, 540, 850)):
        door(c, x, 1440, 190, 360, pr(t, ts[j], 0.12), 1150 + j)
        tape(c, "INVESTOR", x, 1040, 30, (-3, 2, -2)[j], 1.0, seed=1153 + j, col=WHITE)
        if t >= ts[j]: stamp(c, "NO", x, 1250, 80, (-8, 6, -4)[j], stamp_k(t, ts[j]), RED, 1156 + j)
    if at(t, "b4", None, -0.1):
        bubble(c, "\"Nobody was going to just write a check for that idea...\"", 540, 690, pk(t, "b4"), (0, 260), 56, 820)
        tape(c, "MIKE CESSARIO TO CNBC, 2022", 540, 900, 30, 2, pk(t, "b4", "nobody"), seed=1159, col=WHITE)
        if at(t, "b4", "check", -0.2): scribble(c, 540, 700, 330, 130, pr(t, TW("b4", "check") - 0.2, 0.5), RED, 7, 1160)
    else:
        tape(c, "INVESTORS? THEY PASS.", 540, 620, 52, -3, pk(t, "b3"), seed=1161)


# ---------------------------------------------------------------- the ad first (b5-b7)
def S_ad(c, t, n):
    base(c, a=0.16)
    worked = at(t, "b7", None, -0.1)
    def img(cc):
        cc.drawRect(skia.Rect.MakeLTRB(-226, -226, 226, 166), P((255, 214, 0)))
        cc.save(); cc.translate(0, 150); cc.scale(0.62, 0.62); _tallcan(cc, 0, 0, 1.0, t, mth(t, ["b5", "b7"]), (0, 0), "happy", "up", False, blink(t), 1170); cc.restore()
    vf = pr(t, TW("b7", "views,") - 0.9, 1.0) if worked else 0.0
    views = None if not worked else f"{int(1000000 * ease(vf)):,}" + ("+" if vf >= 1 else "")
    post_card(c, 640 if not worked else 690, 1000, 0.95 if not worked else 0.9, 1171, views, pk(t, "b5", "video,"), t, img, likes=vf)
    if not worked:
        person(c, 120, 1440, 0.8, 1143, (90, 60, 40), t, "point", "MIKE", "happy", (1, 0), "short")
        tape(c, "AD FIRST", 300, 600, 60, -4, pk(t, "b5", "first:"), seed=1172)
        if at(t, "b5", "fake", -0.3):
            render_can(c, 300, 1250, 0.6, 0.0, 1173)
            tape(c, "3D RENDER", 300, 1310, 34, 3, pk(t, "b5", "fake"), seed=1174, col=WHITE)
        tape(c, "POSTED ONLINE, 2018", 690, 1385, 34, 3, pk(t, "b5", "video,"), seed=1175, col=WHITE)
    else:
        store(c, 150, 1440, 260, 300, 1176, "SHOP")
        tape(c, "NOT ON SALE YET", 170, 1000, 30, -4, 1.0, seed=1177, col=WHITE)
        if at(t, "b7", "views,", -0.2): scribble(c, 800, 1240, 150, 46, pr(t, TW("b7", "views,"), 0.5), RED, 8, 1178)
        tape(c, "DID IT WORK?", 690, 560, 50, -3, pk(t, "b7", "work?", -0.3), seed=1179, col=WHITE)
        if at(t, "b7", "sale.", -0.4): stamp(c, "BEFORE IT WAS\nON SALE", 300, 770, 50, -6, sk(t, "b7", "sale.", -0.3), RED, 1180)


# ---------------------------------------------------------------- the store (b8-b9)
def S_store(c, t, n):
    base(c, a=0.24)
    big = at(t, "b9", None, -0.1)
    fill = pr(t, TW("b8", "real") - 0.1, 0.8)
    if not big:
        render_can(c, 300, 1380, 0.8, fill, 1190)
        calendar(c, 820, 800, "2019", 0.6, pk(t, "b8"), 1191, INK)
        tape(c, "INVESTORS WRITE CHECKS", 540, 560, 44, -3, pk(t, "b8", "checks,"), seed=1192)
        coin_rain(c, t, TW("b8", "checks,"), 7, 1193, 1300)
        if at(t, "b8", "ship.", -0.3):
            char(c, "box", 760, 1440, 0.6, t, 0, (-0.4, 0), "happy", "up", blink=blink(t), label="CANS", seed=1194)
            tape(c, "CANS SHIP", 600, 1000, 46, 4, pk(t, "b8", "ship."), seed=1195, col=WHITE)
    else:
        nf = 12 * pr(t, L0("b9"), 2.2)
        shelf(c, 540, 1440, nf, 820, 1196, 2, 6)
        tape(c, "2023 · $263M RETAIL SCANNED SALES", 540, 640, 38, -2, pk(t, "b9", "stores"), seed=1197, col=WHITE)
        tape(c, "THE COMPANY'S OWN FIGURE", 540, 740, 30, 2, pk(t, "b9", "company"), seed=1198)
        if at(t, "b9", "quarter", -0.2): stamp(c, "$263M", 540, 840, 84, -5, sk(t, "b9", "quarter"), RED, 1209)
        if at(t, "b9", "quarter", -0.2): scribble(c, 540, 640, 400, 60, pr(t, TW("b9", "quarter") - 0.2, 0.5), RED, 7, 1199)


# ---------------------------------------------------------------- the catch (c1-c2)
def S_map(c, t, n):
    base(c, a=0.14)
    two_lands(c, t, 1200)
    text(c, "AMERICA", 240, 900, 44, INK, MARK_F)
    text(c, "BRITAIN", 690, 740, 36, INK, MARK_F); text(c, "EUROPE", 890, 960, 40, INK, MARK_F)
    tape(c, "THE CATCH", 300, 580, 60, -4, pk(t, "c1", "catch?", -0.3), seed=1201, col=INK, fg=BY)
    calendar(c, 840, 600, "2025", 0.55, pk(t, "c1", "twenty-five,"), 1202, INK)
    if at(t, "c1", "paused", -0.2):
        stamp(c, "PAUSED", 860, 1150, 80, 8, sk(t, "c1", "paused"), RED, 1203)
    if at(t, "c1", "Britain", -0.2):
        k = pr(t, TW("c1", "Britain") - 0.1, 0.3)
        wline(c, [(650, 760), (650 + 100 * k, 760 + 180 * k)], 1204, 14, RED); wline(c, [(750, 760), (750 - 100 * k, 760 + 180 * k)], 1205, 14, RED)
    if at(t, "c2", None, -0.1):
        factory(c, 230, 1370, t, 0.45, 1206)
        tape(c, "REASON GIVEN: ALL PRODUCTION MOVED TO THE US", 540, 1475, 30, 2, pk(t, "c2", "reason"), seed=1207, col=WHITE)
        if at(t, "c2", "all", -0.2): scribble(c, 230, 1290, 130, 110, pr(t, TW("c2", "all") - 0.2, 0.4), RED, 8, 1208)


# ---------------------------------------------------------------- 3 moves (m1-m3): one evolving board
def S_moves(c, t, n):
    base(c, a=0.14)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 560, 52, -3, pk(t, "m1"), seed=1240, col=INK, fg=BY)
    moves = [("m1", "One:", "1. VIDEO BEFORE PRODUCT"), ("m2", "Two:", "2. COUNT WHO ASKS"), ("m3", "Three:", "3. BORING THING, LOUD BRAND")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=-1)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 670 + i * 80; tape(c, lab, 540, y, 36, (-2, 2, -1)[i], pk(t, l, w), seed=1241 + i, col=BY if i == cur else WHITE)
            if i < cur: wline(c, [(860, y - 5), (880, y + 15), (920, y - 25)], 1245 + i, 8, RED)
    if cur <= 0:
        you(c, 230, 1440, t, 1.0, "hold", "happy", (1, 0))
        phone(c, 380, 1200, 0.6, 1250, screen=lambda cc: (cc.drawCircle(0, -60, 34, P(RED, 0.6 + 0.4 * math.sin(t * 6))), text(cc, "REC", 0, 60, 44, INK, BLK_F)))
        render_can(c, 780, 1420, 0.85, 0.0, 1251)
        text(c, "NOT MADE YET", 780, 1030, 40, RED, MARK_F)
    elif cur == 1:
        you(c, 200, 1440, t, 1.0, "point", "happy", (1, 0))
        t0 = TW("m2", "asks") - 0.2
        for j in range(5):
            kk = pop_k(t, t0 + j * 0.22, 0.25)
            if kk > 0: bubble(c, "WHERE CAN I BUY?", 620 + (j % 2) * 150, 900 + j * 105, kk, (-60, 40), 38, 400, seed=1252 + j)
        nt = sum(1 for j in range(5) if t >= t0 + j * 0.22 + 0.1)
        for j in range(nt): wline(c, [(160 + j * 26, 860), (160 + j * 26, 930)], 1258 + j, 7, RED)
        if at(t, "m2", "proof.", -0.2): stamp(c, "PROOF", 330, 1010, 70, -8, sk(t, "m2", "proof."), RED, 1263)
    else:
        you(c, 230, 1440, t, 1.0, "point", "happy", (1, 0))
        loud = at(t, "m3", "loud", -0.2)
        char(c, "box", 700, 1440, 0.75, t, 0, (-0.4, 0), "angry" if loud else "neutral", "up" if loud else "down", blink=blink(t), label="RICE", seed=1264)
        if loud: tape(c, "NOW WITH ATTITUDE", 700, 960, 38, 4, pk(t, "m3", "loud"), seed=1265, col=WHITE); scribble(c, 700, 1180, 190, 230, pr(t, TW("m3", "personality."), 0.4), RED, 7, 1266)
        else: tape(c, "BORING", 700, 960, 40, 4, pk(t, "m3", "boring"), seed=1267, col=WHITE)


# ---------------------------------------------------------------- callback ending (e1)
def S_end(c, t, n):
    base(c, a=0.30)
    shelves = fridge(c, 760, 1400, 520, 820, 1.0, 1100)
    for j, x in enumerate((560, 640, 720, 800)): bottle(c, x, shelves[0], 0.7, 1101 + j)
    char(c, "tallcan", 760, 1440, 0.9, t, 0.0, (-0.5, -0.2), "happy", "up" if at(t, "e1", "joke.", -0.3) else "hips", blink=blink(t), loud=at(t, "e1", "joke.", -0.3))
    title(c, "PLAIN WATER IN A CAN?", 540, 450, 60, INK, pk(t, "e1"), -2)
    you(c, 240, 1440, t, 0.95, "shrug" if not at(t, "e1", "joke.", -0.3) else "up", "happy", (1, 0))
    if at(t, "e1", "joke.", -0.3):
        tape(c, "PEOPLE PAY FOR THE JOKE", 540, 540, 46, 3, pk(t, "e1", "joke.", -0.3), seed=1270, col=WHITE)
        wline(c, [(330, 900), (370, 950), (450, 840)], 1271, 12, RED)


def S_z(c, t, n):
    base(c, a=0.30)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 600, 58, -3, pk(t, "z1"), seed=1280, col=INK, fg=BY)
        bubble(c, "the friend who buys drinks for the can", 540, 800, pk(t, "z1", "friend"), (-180, 200), 54, 720)
        phone(c, 300, 1250, 0.55, 1281)
        person(c, 800, 1440, 0.9, 1282, (90, 60, 40), t, "wave", "FRIEND", "happy", (-1, 0), "short")
        arrow(c, 380, 1150, 700, 1050, 60, RED, 8, 1283, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "BORING OR LOUD?", 540, 620, 80, INK, pk(t, "z2"))
        char(c, "tallcan", 300, 1440, 0.8, t, 0, (0.4, 0), "neutral", "down", blink=blink(t), label="BORING", col=(190, 190, 196), seed=1284)
        char(c, "tallcan", 780, 1440, 0.8, t, 0, (-0.4, 0), "happy", "up", blink=blink(t, 3), label="LOUD", loud=True, seed=1285)
        stamp(c, "BORING", 300, 830, 70, -6, sk(t, "z2", "Boring"), INK, 1286)
        stamp(c, "LOUD", 780, 830, 80, 6, sk(t, "z2", "loud"), RED, 1287)
        text(c, "?", 540, 1100, 140, RED, MARK_F)


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
