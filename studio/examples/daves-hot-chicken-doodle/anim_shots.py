# DAVE'S HOT CHICKEN "$900 and a parking lot" — real case study + 3 moves, SHORTS LENGTH (22 Nov 2026). DOODLE look, LIGHT page.
# Upgrade: PRICE-CONTRAST hook (pattern of our 3 best doodles) — YOU holds a fan of $900 in an empty parking space from frame 1, the cover
# says "$900 AND A PARKING LOT / TO A ~$1 BILLION DEAL?", the same $900 tag flips to "~$1 BILLION (REPORTED)" at e2, and the callback ending
# puts YOU back in the parking space with the $900 + a stamped health permit.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: generic tenders/fryer/store (no logo, box, mascot or red-white trade dress), founders = plain doodles + name tapes.
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_trend", "a1", "whip"), ("S_chef", "b1", "whip"), ("S_lot", "b3", "whip"), ("S_menu", "c2", "whip"),
         ("S_line", "d1", "whip"), ("S_deal", "e1", "whip"), ("S_catch", "e3", "whip"), ("S_moves", "m1", "whip"), ("S_end", "f1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "nine"), "chaching"), (TW("i1", "parking"), "pop"), (TW("i1", "restaurant?"), "boing"),
        (TW("i2", "crew"), "pop"), (TW("i2", "Three"), "stamp"),
        (L0("a1"), "pop"), (TW("a1", "five"), "stamp"), (TW("a2", "three."), "ding"),
        (TW("b1", "seventeen."), "stamp"), (TW("b1", "Michelin-starred"), "ding"),
        (TW("b2", "Odd"), "boing"), (TW("b2", "chicken.\""), "buzz"),
        (TW("b3", "pool"), "chaching"), (TW("b4", "fryer,"), "pop"), (TW("b4", "lamp,"), "pop"), (TW("b4", "tables"), "pop"),
        (TW("b5", "permits"), "buzz"), (TW("b5", "copy"), "stamp"),
        (TW("c1", "forty"), "chaching"), (TW("c1", "Four"), "pop"),
        (TW("c2", "surprising"), "pop"), (TW("c2", "One"), "stamp"),
        (L0("c3"), "boing"), (TW("c3", "waiver"), "tick"),
        (TW("d1", "work?"), "tick"), (TW("d1", "block."), "pop"), (TW("d2", "store"), "slam"), (TW("d2", "franchises."), "pop"),
        (TW("e1", "Roark"), "stamp"), (TW("e1", "majority"), "slam"), (TW("e2", "billion,"), "chaching"),
        (TW("e3", "catch?"), "buzz"), (TW("e3", "cooling"), "slide"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "permit."), "stamp"),
        (TW("m2", "Two:"), "stamp"), (TW("m2", "search"), "pop"),
        (TW("m3", "Three:"), "stamp"), (TW("m3", "two"), "stamp"),
        (L0("f1"), "boing"), (TW("f2", "check"), "stamp"),
        (L0("z1"), "whoosh"), (TW("z2", "Mild,"), "stamp"), (TW("z2", "Reaper?"), "stamp")]


import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("$900 AND A PARKING LOT", "TO A ~$1 BILLION DEAL?")   # (kicker, TITLE) on frame 0 = the grid cover
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%€]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i1": "You've got $900 and a parking lot. Want to open a restaurant?",
        "i2": "One crew did. 3 moves at the end.",
        "a1": "Technomic says chicken chain sales grew about 5% last year.",
        "a2": "Big chains overall? About 3%.",
        "b1": "Los Angeles, 2017. Dave Kopushyan had cooked in Michelin-starred kitchens.",
        "c1": "Opening night: $40. 4 meals, to a girlfriend and her friends.",
        "e1": "In 2025, Roark buys a majority stake.",
        "e2": "The deal's value? Pretty close to $1 billion, says the chain's CEO.",
        "m1": "Your moves. 1: even a pop-up needs a local health permit.",
        "m2": "2: search the name before you paint the sign.",
        "m3": "3: buying a franchise? Read its disclosure papers, due 2 weeks before you sign.",
        "f1": "So, a restaurant for $900?"}
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


def lt(t, sid): return t - SHOT[sid]["start"]


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




def cash_fan(c, x, y, s=1.0, seed=0, k=1.0, rot=0.0):
    """a fan of 5 green bills (no portraits) held up; (x, y) = grip."""
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    for j in range(5):
        c.save(); c.rotate(-40 + j * 20)
        ink(c, wrrect(-40, -230, 40, -20, 8, seed + j, 1.0), (150, 220, 150), 6)
        c.drawCircle(0, -125, 18, P(DGRN))
        c.restore()
    c.restore()


def price_tag(c, x, y, s, k, seed, word, col=YEL, rot=-8):
    if k <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * k, s * k)
    f = font(ANTON_F, 84); tw = f.measureText(word); w2 = tw / 2 + 50
    ink(c, wpoly([(-w2 - 50, 0), (-w2, -70), (w2, -70), (w2, 70), (-w2, 70)], seed, 1.4, True, 30), col, 8)
    c.drawCircle(-w2 - 14, 0, 12, P(WHITE)); c.drawCircle(-w2 - 14, 0, 12, S(INK, 5))
    c.drawString(word, -tw / 2 + 10, 30, f, P(INK))
    c.restore()


def friends3(c, x0, y, t, s=0.8, k=1.0, pose="stand", mood="happy", names=None):
    for j, col in enumerate((BLU, ORG, PUR)):
        person(c, x0 + j * 170, y, s, 4100 + j, col, t, pose, names[j] if names else None, mood, (0, 0), "short", pop_k(t, 0, 0.01) * k if k > 0 else 0, 26)


# ---------------------------------------------------------------- hook (i1-i2): YOU + $900 in an empty parking space -> the crew
def S_hook(c, t, n):
    base(c)
    live = t > COVER_T
    parking_lot(c, 1440, 4001, 1.0, t, 0.0)
    crew = live and at(t, "i2", "crew", -0.3)
    you(c, 330, 1440, t, 0.95, "hold" if not crew else "point", "happy" if live else "neutral", (1, 0))
    cash_fan(c, 430, 1230, 0.8, 4002, 1.0 if not live else max(0.6, pk(t, "i1", "nine")), 10)
    price_tag(c, 780, 860 if live else 1040, 1.0, 1.0 if not live else pk(t, "i1", "nine"), 4003, "$900")
    if not live: return
    if at(t, "i1", "parking", -0.2):
        tape(c, "AN EMPTY PARKING SPACE", 700, 1500, 34, 2, pk(t, "i1", "parking"), seed=4004, col=WHITE)
    if at(t, "i1", "restaurant?", -0.3) and not crew:
        store_front(c, 760, 1380, 0.8, 4005, pk(t, "i1", "restaurant?"), "RESTAURANT?")
        text(c, "?", 960, 900, 150, RED, MARK_F)
    if crew:
        friends3(c, 600, 1440, t, 0.7, pk(t, "i2", "crew"), "up", "happy")
        arrow(c, 760, 700, 760, 940, 20, RED, 8, 4006, pr(t, TW("i2", "crew"), 0.4))
    if at(t, "i2", "Three", -0.2):
        stamp(c, "3 MOVES AT THE END", 540, 520, 56, -3, sk(t, "i2", "Three", 0.2), RED, 4007)


# ---------------------------------------------------------------- the trend (a1-a2)
def S_trend(c, t, n):
    base(c)
    tape(c, "THE TREND: CHICKEN CHAINS", 540, 470, 50, -3, pk(t, "a1"), seed=4010, col=INK, fg=WHITE)
    g1 = eout(pr(t, TW("a1", "five") - 0.4, 0.8)); g2 = eout(pr(t, TW("a2", "overall?") - 0.2, 0.8))
    bars(c, 540, 1300, [0.95 * g1 + 0.001, 0.54 * g2 + 0.001], 1.0, 4011, ORG, 220, 120, 520)
    text(c, "CHICKEN", 370, 1360, 36, INK, BLK_F); text(c, "INDUSTRY", 710, 1360, 36, INK, BLK_F)
    if g1 > 0.6: stamp(c, "+5.3%", 370, 720, 84, -6, sk(t, "a1", "five", 0.2), RED, 4012)
    if g2 > 0.6: text(c, "~3%", 710, 940, 70, INK, MARK_F)
    if at(t, "a2", "three.", -0.2):
        wline(c, [(300, 640), (330, 680), (400, 600)], 4013, 12, RED)
        tape(c, "2025 SALES GROWTH (TECHNOMIC)", 600, 1530, 30, 1, pk(t, "a2", "three."), seed=4014, col=WHITE)
    you(c, 150, 1440, t, 0.5, "head" if at(t, "a1", "five", -0.2) else "stand", "shock" if at(t, "a1", "five", -0.2) else "neutral", (1, 0))


# ---------------------------------------------------------------- the chef (b1-b2)
def S_chef(c, t, n):
    base(c)
    b2 = at(t, "b2", None, -0.1)
    for j, (bx, bw, bh) in enumerate(((150, 160, 380), (330, 140, 520), (880, 180, 450), (1000, 120, 300))):
        building(c, bx, 1440, bw, bh, (214, 222, 236), 4020 + j, None, False)
    tape(c, "LOS ANGELES · 2017", 540, 470, 52, -3, pk(t, "b1", "seventeen."), seed=4025, col=INK, fg=WHITE)
    person(c, 540, 1440, 1.05, 4026, BLU, t, "shrug" if b2 else "wave", "DAVE KOPUSHYAN", "meh" if b2 else "happy", (0, 0), "short", pk(t, "b1", "Kopushyan."), 34)
    chef_hat(c, 540, 1440 - 230 * 1.05 - 50, 1.05, 4027, pk(t, "b1", "Kopushyan.", 0.1))
    if at(t, "b1", "Michelin-starred", -0.2) and not b2:
        for j in range(3):
            kk = pk(t, "b1", "Michelin-starred", j * 0.1)
            if kk > 0: text(c, "*", 400 + j * 140, 760 + (j % 2) * 30, 150 * kk, YEL, MARK_F)
        tape(c, "MICHELIN-STARRED KITCHENS", 540, 920, 40, 2, pk(t, "b1", "Michelin-starred", 0.2), seed=4028, col=WHITE)
    if b2:
        text(c, "?!", 840, 760, 110, RED, MARK_F)
        tender_box(c, 820, 1440, 1.0, 4029, pk(t, "b2", "Odd"))
        if at(t, "b2", "chicken.\"", -0.6):
            bubble(c, "\"I don't even like chicken.\"", 460, 640, pk(t, "b2", "saying,"), (60, 200), 52, 620)
            tape(c, "AS A COFOUNDER RECALLS (CNBC)", 460, 860, 30, 1, pk(t, "b2", "saying,", 0.3), seed=4030, col=WHITE)


# ---------------------------------------------------------------- the parking lot (b3-c1): pool the cash, fryer, lamp, tables, no permit, $40 night
def S_lot(c, t, n):
    base(c)
    c1 = at(t, "c1", None, -0.1)
    parking_lot(c, 1440, 4040, 1.0, t, eout(pr(t, L0("c1") - 0.1, 0.8)) if c1 else 0.0)
    if c1: c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), P((40, 40, 90), 0.12 * min(1, pr(t, L0("c1") - 0.1, 0.5))))
    if not at(t, "b4", None, -0.1):
        friends3(c, 250, 1440, t, 0.8, 1.0, "point", "happy")
        u = pr(t, TW("b3", "pool") - 0.2, 0.9)
        ink(c, wpoly([(700, 1300), (900, 1300), (870, 1440), (730, 1440)], 4041, 1.4, True, 20), INK, 7)   # hat on the ground
        for j in range(3):
            v = eout(pr(t, TW("b3", "pool") - 0.2 + j * 0.15, 0.4))
            if v > 0: cash_fan(c, 520 + j * 140 + (800 - 520 - j * 140) * v, 1000 + 260 * v, 0.35, 4042 + j, 1.0, 20 * j)
        if at(t, "b3", "pool", -0.1): price_tag(c, 800, 1100, 0.8, pk(t, "b3", "pool", 0.3), 4046, "~$900")
        if at(t, "b3", "cash.", -0.1): tape(c, "POOLED", 800, 1220, 40, 3, pk(t, "b3", "cash."), seed=4047, col=WHITE)
        return
    folding_table(c, 540, 1440, 560, 4050, pk(t, "b4", "tables"), WHITE, "BORROWED FROM PARENTS" if at(t, "b4", "parents.", -0.2) else None)
    fryer(c, 430, 1440 - 170, 0.75, 4051, pk(t, "b4", "fryer,"), t)
    heat_lamp(c, 880, 1440, 0.9, 4052, pk(t, "b4", "lamp,"), True, t)
    if at(t, "b4", "parents.", -0.2) and not at(t, "b5", None, -0.1):
        for j, (l, w) in enumerate((("b4", "fryer,"), ("b4", "lamp,"), ("b4", "tables"))):
            wline(c, [(250 + j * 260, 700), (270 + j * 260, 730), (310 + j * 260, 670)], 4053 + j, 10, RED)
    if at(t, "b5", None, -0.1) and not c1:
        clipboard(c, 760, 860, 0.8, 4056, "PERMIT", pk(t, "b5", "permits"), 0)
        if at(t, "b5", "permits", 0.1):
            wline(c, [(660, 720), (860, 1000)], 4057, 16, RED); wline(c, [(860, 720), (660, 1000)], 4058, 16, RED)
        if at(t, "b5", "copy", -0.2): stamp(c, "DON'T COPY THIS", 400, 640, 70, -6, sk(t, "b5", "copy"), RED, 4059)
    if c1:
        tape(c, "OPENING NIGHT", 540, 470, 56, -3, pk(t, "c1"), seed=4060, col=INK, fg=WHITE)
        for j in range(4):
            kk = pk(t, "c1", "Four", j * 0.12)
            if kk > 0: tender_box(c, 230 + j * 150, 1060 - 12 * math.sin(t * 3 + j), 0.6, 4061 + j, kk)
        if at(t, "c1", "forty", -0.2):
            stamp(c, "$40", 820, 800, 110, -6, sk(t, "c1", "forty"), RED, 4067)
        if at(t, "c1", "girlfriend", -0.2):
            tape(c, "4 MEALS: A COFOUNDER'S GIRLFRIEND + 3 FRIENDS", 540, 1500, 28, 1, pk(t, "c1", "girlfriend"), seed=4068, col=WHITE)


# ---------------------------------------------------------------- one item (c2) + the tender (c3)
def S_menu(c, t, n):
    base(c)
    c3 = at(t, "c3", None, -0.1)
    if not c3:
        tape(c, "THE SURPRISING MOVE", 540, 470, 52, -3, pk(t, "c2", "surprising"), seed=4070, col=INK, fg=WHITE)
        k0 = pk(t, "c2", None, 0.0)
        if k0 > 0:
            c.save(); c.translate(540, 1000); c.scale(k0, k0)
            ink(c, wrrect(-300, -330, 300, 330, 18, 4071, 2), INK, 9)
            text(c, "MENU", 0, -250, 64, WHITE, MARK_F)
            items = ["BURGERS", "TACOS", "SALADS", "WINGS", "PIZZA"]
            for j, it in enumerate(items):
                text(c, it, 0, -150 + j * 90, 46, (200, 200, 200), BLK_F)
                kx = pr(t, TW("c2", "only:") - 0.2 + j * 0.08, 0.25)
                if kx > 0: wline(c, [(-170, -165 + j * 90), (-170 + 340 * kx, -165 + j * 90)], 4072 + j, 12, RED)
            c.restore()
        if at(t, "c2", "plate.", -0.4):
            tape(c, "1 ITEM: HOT CHICKEN PLATE", 540, 1400, 48, 2, pk(t, "c2", "plate."), seed=4078, col=YEL)
            ink(c, wellipse(540, 1400, 360, 70, 4079, 2), None, 10, RED)
        return
    tape(c, "TODAY", 760, 470, 56, -3, pk(t, "c3"), seed=4080, col=WHITE)
    heat_meter(c, 540, 900, 0.95, 4081, pk(t, "c3"), eout(pr(t, L0("c3"), 0.9)))
    char(c, "tender", 300, 1440, 0.8, t, mth(t, ["c3"]), (1, -0.2), "worried", "wave", blink=blink(t), seed=4082)
    clipboard(c, 780, 1260, 0.75, 4083, "WAIVER", pk(t, "c3", "waiver", -0.2), 0)
    if at(t, "c3", "waiver", -0.1):
        tape(c, "SIGN HERE", 780, 1500, 36, 2, pk(t, "c3", "waiver"), seed=4084, col=ORG)
        wline(c, [(680, 1440), (880, 1430)], 4085, 8, RED)


# ---------------------------------------------------------------- did it work (d1-d2): line around the block -> store -> franchises
def S_line(c, t, n):
    base(c)
    d2 = at(t, "d2", None, 0.0)
    tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "d1"), seed=4090, col=INK, fg=WHITE)
    if not d2:
        heat_lamp(c, 900, 1440, 0.7, 4091, 1.0, True, t)
        folding_table(c, 880, 1440, 260, 4092, 1.0)
        wline(c, [(0, 1100), (1080, 1100)], 4089, 6, GREY)
        m = int(16 * pr(t, L0("d1"), 1.6))
        for j in range(m):
            row = j // 8; xx = 780 - (j % 8) * 92 if row == 0 else 80 + (j % 8) * 92
            yy = 1440 if row == 0 else 1100
            person(c, xx, yy, 0.42, 4100 + j, (BLU, ORG, PUR, PNK, GRN)[j % 5], t, "stand", None, "happy", (1 if row == 0 else -1, 0), "short", 1.0)
        if at(t, "d1", "block.", -0.3):
            arrow(c, 760, 1180, 120, 1180, 80, RED, 9, 4093, pr(t, TW("d1", "block.") - 0.3, 0.5))
            tape(c, "AROUND THE BLOCK", 540, 760, 50, 2, pk(t, "d1", "block."), seed=4094, col=WHITE)
        return
    store_front(c, 540, 1440, 1.2, 4095, pk(t, "d2", None, 0.0, 0.25), "HOT CHICKEN", t)
    if at(t, "d2", "store", -0.1): tape(c, "2018: A REAL STORE", 540, 640, 46, 2, pk(t, "d2", "store", 0.1), seed=4096, col=WHITE)
    if at(t, "d2", "franchises.", -0.3):
        for j, (x, y) in enumerate(((180, 1100), (900, 1100), (180, 1440), (900, 1440))):
            kk = pk(t, "d2", "franchises.", j * 0.1)
            store_front(c, x, y, 0.5, 4097 + j, kk, "HOT CHICKEN")
        tape(c, "FRANCHISING FROM 2019", 540, 1500, 36, 1, pk(t, "d2", "franchises.", 0.3), seed=4102, col=ORG)


# ---------------------------------------------------------------- the deal (e1-e2): majority stake, the $900 tag flips to ~$1 billion
def S_deal(c, t, n):
    base(c)
    e2 = at(t, "e2", None, -0.1)
    store_front(c, 300, 1440, 0.9, 4110, 1.0, "HOT CHICKEN", t)
    if at(t, "e1", "Roark", -0.2): tape(c, "2025 · ROARK CAPITAL", 540, 470, 52, -3, pk(t, "e1", "Roark"), seed=4111, col=INK, fg=WHITE)
    if at(t, "e1", "majority", -0.2):
        kk = pk(t, "e1", "majority")
        wline(c, [(360, 1100), (360, 1100 - 260 * kk)], 4112, 10)
        if kk > 0.5: ink(c, wpoly([(360, 840), (560, 870), (360, 920)], 4113, 1.2, True, 20), RED, 7)
        tape(c, "MAJORITY STAKE", 560, 760, 40, 3, pk(t, "e1", "majority", 0.2), seed=4114, col=WHITE)
    flip = pr(t, TW("e2", "billion,") - 0.25, 0.4)
    sx = abs(math.cos(flip * math.pi))
    if not e2:
        price_tag(c, 790, 1200, 0.9, pk(t, "e1"), 4115, "$900")
    else:
        c.save(); c.translate(780, 1200); c.scale(max(0.02, sx), 1); c.translate(-780, -1200)
        price_tag(c, 740, 1200, 0.75, 1.0, 4115, "$900" if flip < 0.5 else "~$1 BILLION")
        c.restore()
        if flip >= 1:
            coin_rain(c, t, TW("e2", "billion,"), 14, 4116, 1440)
            tape(c, "CEO: \"PRETTY CLOSE\" · TERMS NOT DISCLOSED", 540, 1500, 28, 1, pk(t, "e2", "billion,", 0.2), seed=4117, col=WHITE)
        if at(t, "e2", "value?", -0.2) and flip < 1: text(c, "?", 900, 900, 130, RED, MARK_F)


# ---------------------------------------------------------------- the catch (e3)
def S_catch(c, t, n):
    base(c)
    tape(c, "THE CATCH", 540, 470, 60, -3, pk(t, "e3", "catch?"), seed=4120, col=INK, fg=WHITE)
    g = eout(pr(t, L0("e3"), 0.6)); g2 = eout(pr(t, TW("e3", "cooling") - 0.3, 0.6))
    bars(c, 540, 1300, [0.9 * g + 0.001, 0.53 * g2 + 0.001], 1.0, 4121, ORG, 220, 120, 560, None)
    text(c, "2024", 370, 1360, 38, INK, BLK_F); text(c, "2025", 710, 1360, 38, INK, BLK_F)
    if g > 0.7: text(c, "+9.1%", 370, 700, 64, INK, MARK_F)
    if g2 > 0.7:
        text(c, "+5.3%", 710, 900, 64, INK, MARK_F)
        arrow(c, 420, 640, 760, 900, -30, RED, 10, 4122, pr(t, TW("e3", "cooling"), 0.4))
        tape(c, "CHICKEN CHAIN SALES GROWTH (TECHNOMIC)", 540, 1460, 30, 1, 1.0, seed=4123, col=WHITE)


# ---------------------------------------------------------------- 3 moves (m1-m3): YOU's own pop-up
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 450, 52, -3, pk(t, "m1"), seed=4130, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. A LOCAL HEALTH PERMIT"), ("m2", "Two:", "2. SEARCH THE NAME"), ("m3", "Three:", "3. FRANCHISE? READ THE FDD")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=0)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 550 + i * 74; tape(c, lab, 500, y, 34, (-2, 2, -1)[i], pk(t, l, w), seed=4131 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(820, y - 5), (840, y + 15), (880, y - 25)], 4135 + i, 8, RED)
    if cur == 0:
        you(c, 250, 1440, t, 0.8, "point", "happy", (1, 0))
        folding_table(c, 520, 1440, 320, 4140, 1.0)
        fryer(c, 520, 1270, 0.5, 4141, 1.0, t)
        health_permit(c, 830, 1150, 0.75, 4142, pk(t, "m1", "permit.", -0.4), pr(t, TW("m1", "permit."), 0.4))
        if at(t, "m1", "permit.", -0.2):
            stamp(c, "HEALTH PERMIT", 740, 880, 52, -6, sk(t, "m1", "permit."), DGRN, 4143)
            tape(c, "ASK YOUR LOCAL OR STATE HEALTH DEPT (SBA)", 540, 1500, 28, 1, pk(t, "m1", "permit.", 0.2), seed=4144, col=WHITE)
    elif cur == 1:
        you(c, 250, 1440, t, 0.8, "hold", "neutral", (1, 0))
        ink(c, wrrect(480, 860, 980, 1060, 12, 4150, 1.4), WHITE, 8)
        text(c, "YOUR NAME HERE", 730, 980, 46, GREY, MARK_F)
        if at(t, "m2", "search", -0.2):
            magnifier(c, 700, 1000, 0.8, 4151, pk(t, "m2", "search"))
            ink(c, wellipse(700, 1000, 110, 110, 4152, 2), None, 10, RED)
        if at(t, "m2", "sign.", -0.3):
            text(c, "THEN PAINT", 730, 1200, 44, INK, BLK_F)
            tape(c, "CLEARANCE SEARCH FIRST (USPTO)", 540, 1500, 32, 1, pk(t, "m2", "sign."), seed=4153, col=WHITE)
    else:
        doc_stack(c, 330, 1440, 1.0, 4160, pk(t, "m3", "disclosure", -0.3), "FDD")
        tape(c, "DISCLOSURE DOC (FDD)", 340, 960, 34, -3, pk(t, "m3", "disclosure"), seed=4161, col=WHITE)
        calendar(c, 790, 1040, 14, 0.8, pk(t, "m3", "two", -0.3), 4162)
        if at(t, "m3", "two", -0.1):
            ink(c, wellipse(790, 1040, 180, 200, 4163, 2), None, 10, RED)
            tape(c, "14+ DAYS BEFORE YOU SIGN OR PAY (FTC)", 540, 1500, 30, 1, pk(t, "m3", "two", 0.2), seed=4164, col=ORG)


# ---------------------------------------------------------------- callback (f1-f2): YOU back in the parking space with the $900
def S_end(c, t, n):
    base(c)
    parking_lot(c, 1440, 4001, 1.0, t, 1.0)
    f2 = at(t, "f2", None, -0.1)
    you(c, 330, 1440, t, 0.95, "hold" if not f2 else "point", "happy", (1, 0))
    cash_fan(c, 430, 1230, 0.8, 4002, 1.0, 10)
    price_tag(c, 780, 860, 0.9, 1.0, 4003, "$900")
    if not f2:
        store_front(c, 760, 1440, 0.75, 4170, pk(t, "f1", "restaurant"), "RESTAURANT?")
        return
    tender_box(c, 760, 1440, 1.0, 4171, pk(t, "f2", "done."))
    if at(t, "f2", "done.", -0.2): stamp(c, "IT'S BEEN DONE", 600, 600, 70, -5, sk(t, "f2", "done."), RED, 4172)
    if at(t, "f2", "check", -0.2):
        health_permit(c, 860, 1160, 0.6, 4173, pk(t, "f2", "check"), pr(t, TW("f2", "check") + 0.1, 0.4))
        tape(c, "PERMIT FIRST", 860, 1350, 36, 3, pk(t, "f2", "check", 0.2), seed=4174, col=ORG)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=4180, col=INK, fg=WHITE)
        bubble(c, "the friend who orders the hottest level", 540, 690, pk(t, "z1", "friend"), (-180, 200), 50, 760)
        phone(c, 260, 1200, 0.5, 4181)
        person(c, 760, 1440, 0.75, 4182, PNK, t, "hold", "FRIEND", "shock", (-1, 0), "long", 1.0, 30)
        heat_meter(c, 800, 1000, 0.45, 4183, pk(t, "z1", "hottest"), 1.0)
        arrow(c, 330, 1100, 640, 1040, 60, RED, 8, 4184, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "MILD OR REAPER?", 540, 560, 80, INK, pk(t, "z2"))
        for j, (x, nfl, word, col) in enumerate(((300, 1, "MILD", GRN), (780, 5, "REAPER", RED))):
            tender_box(c, x, 1400, 1.1, 4190 + j, 1.0)
            for q in range(nfl): flame(c, x - (nfl - 1) * 30 + q * 60, 1150, 0.9, t, 4192 + q + j * 9)
            stamp(c, word, x, 900, 80, (-6, 6)[j], sk(t, "z2", ("Mild,", "Reaper?")[j]), col, 4195 + j)
        tape(c, "COMMENT BELOW", 540, 1500, 36, 2, pk(t, "z2", "comments."), seed=4199, col=WHITE)

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
