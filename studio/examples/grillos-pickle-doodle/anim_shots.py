# GRILLO'S PICKLES "Nike said no, so he sold pickles from a cart" — real case study + 3 moves, SHORTS LENGTH (23 Nov 2026). DOODLE look, LIGHT page.
# Upgrade: shortest doodle yet + famous brand in the first two words (cover: NIKE SAID NO / SO HE SOLD PICKLES FROM A CART?), no stat/date/place
# before ~16 s; the NO letter returns for the callback, where it turns into a pickle sneaker.
# One evolving set per section (_SECT), recurring YOU stick character, chunked highlighted subtitles (strip_chunk at y268).
# No brand art: generic tub/jar/cart/sneaker (no logo, swoosh, tub label or trade dress); real people = plain doodles + name tapes.
import os as _os
PLAT = _os.environ.get("OMB_PLAT", "ig")


def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SECT = [("S_hook", "i1", "cut"), ("S_cart", "b1", "whip"), ("S_cold", "c1", "whip"), ("S_push", "d1", "whip"), ("S_win", "e1", "whip"),
         ("S_trend", "a2", "whip"), ("S_moves", "m1", "whip"), ("S_end", "f1", "pop"), ("S_z", "z1", "whip")]
SHOTLIST = [(k, 0.0 if i == 0 else L0(l) - 0.06, tr) for i, (k, l, tr) in enumerate(_SECT)]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "turned"), "stamp"), (TW("i1", "instead?"), "boing"),
        (TW("i2", "Pickles."), "pop"), (TW("i2", "own?"), "ding"), (TW("i3", "Three"), "stamp"),
        (TW("b1", "Nike"), "buzz"), (TW("b1", "hundred-year-old"), "pop"),
        (TW("b3", "Two"), "chaching"), (TW("b3", "cart"), "pop"), (TW("b3", "Common."), "tick"),
        (L0("b4"), "boing"), (TW("b4", "Not"), "stamp"),
        (TW("c1", "surprising"), "pop"), (TW("c1", "aisle"), "buzz"), (TW("c1", "cold."), "whoosh"),
        (TW("c2", "fridge"), "slam"), (TW("c2", "jar"), "tick"),
        (TW("d1", "buyers"), "pop"), (TW("d1", "oil."), "buzz"),
        (TW("d2", "quality.\""), "stamp"), (TW("d2", "Good"), "ding"),
        (TW("e1", "work?"), "tick"), (TW("e1", "seven"), "chaching"),
        (TW("e2", "buys"), "slam"),
        (TW("a2", "now?"), "pop"), (TW("a2", "thirty"), "stamp"),
        (TW("m1", "One:"), "stamp"), (TW("m1", "Register"), "pop"),
        (TW("m2", "cold"), "whoosh"),
        (TW("m3", "Two:"), "stamp"), (TW("m3", "allows"), "tick"), (TW("m3", "doesn't."), "buzz"),
        (TW("m4", "Three:"), "stamp"), (TW("m4", "cart"), "pop"),
        (L0("f1"), "boing"), (TW("f1", "sneaker"), "pop"), (TW("f2", "pickles"), "ding"),
        (L0("z1"), "whoosh"), (TW("z2", "chips,"), "stamp"), (TW("z2", "beer?"), "stamp")]


import skia, runpy, re
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
COVER = ("NIKE SAID NO", "SO HE SOLD PICKLES FROM A CART?")   # (kicker, TITLE) on frame 0 = the grid cover
COVER_T = 2.6
_VLL = runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]
_VL = {l[0]: l[1] for l in _VLL}
_HL = {l[0]: {re.sub(r"[^a-z0-9$%€]", "", w.lower()) for w in l[6]} for l in _VLL}
DISP = {"i3": "3 moves at the end.",
        "b1": "No Nike job? So Travis Grillo grabs grandpa's 100-year-old pickle recipe.",
        "b3": "2 spears for $1, from a cart on Boston Common.",
        "e1": "Did it work? Years later, about 7,000 stores carry it.",
        "a2": "Why now? Circana says pickle-flavored snacks grew about 30% in a year.",
        "m1": "1: selling shelf-stable jars? Register and file your process with the FDA first.",
        "m3": "2: selling from home? Texas allows pickles, Michigan doesn't.",
        "m4": "3: rent a licensed kitchen, then try it at one cart."}
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


def nike_letter(c, x, y, s, t, k=1.0, no_k=0.0):
    """the dream-job letter: plain sheet 'DREAM JOB' + 'NIKE' as plain text (no logo), red NO stamp."""
    letter(c, x, y, s, 5001, k, "DREAM JOB", 5, -4)
    if k > 0: text(c, "NIKE", x, y - 120 * s, 40 * s, INK, BLK_F)
    if no_k > 0: stamp(c, "NO", x + 10, y + 60 * s, 150 * s, -12, no_k, RED, 5002)


# ---------------------------------------------------------------- hook (i1-i3): the NO letter -> pickles -> YOU's own pickle
def S_hook(c, t, n):
    base(c)
    live = t > COVER_T
    pk_on = live and at(t, "i2", "Pickles.", -0.2)
    you(c, 230, 1440, t, 0.9, "shrug" if not pk_on else "point", "shock" if live and at(t, "i1", "turned", -0.1) and not pk_on else ("happy" if pk_on else "neutral"), (1, 0))
    if not live:   # frame 0 / cover: the letter with NO + a pickle peeking in
        nike_letter(c, 580, 1150, 0.85, t, 1.0, 1.0)
        char(c, "pickle", 840, 1440, 0.6, t, 0.0, (-1, 0), "happy", "wave", blink=False, seed=5003)
        return
    if not pk_on:
        nike_letter(c, 640, 1060, 0.95, t, pk(t, "i1", "dream"), sk(t, "i1", "turned", 0.1) if at(t, "i1", "turned", 0.1) else 0.0)
        if at(t, "i1", "instead?", -0.3):
            text(c, "?", 900, 760, 170, RED, MARK_F)
            tape(c, "SO HE SOLD...", 640, 1440, 44, 2, pk(t, "i1", "instead?"), seed=5004, col=WHITE)
        return
    char(c, "pickle", 620, 1440, 0.95, t, 0.0, (-1, 0), "happy", "up", blink=blink(t), seed=5005, shadow_w=0.8)
    for j in range(3):
        kk = pk(t, "i2", "Pickles.", 0.1 + j * 0.1)
        if kk > 0: pickle_spear(c, 780 + j * 50, 640 + j * 80, 0.8, 30 + j * 20, 5006 + j, kk)
    if at(t, "i2", "own?", -0.3):
        pickle_jar(c, 380, 1210, 0.55, 5010, pk(t, "i2", "own?"), "YOURS?")
        arrow(c, 300, 760, 360, 960, -40, RED, 8, 5011, pr(t, TW("i2", "own?"), 0.4))
    if at(t, "i3", "Three", -0.2):
        stamp(c, "3 MOVES AT THE END", 540, 520, 56, -3, sk(t, "i3", "Three", 0.1), RED, 5012)


# ---------------------------------------------------------------- the cart (b1-b4): Travis + grandpa's recipe -> cart on Boston Common -> pickle says no shelf
def S_cart(c, t, n):
    base(c)
    b3 = at(t, "b3", None, -0.1); b4 = at(t, "b4", None, -0.1)
    if not b3:
        tape(c, "BOSTON · 2008", 540, 470, 52, -3, pk(t, "b1"), seed=5020, col=INK, fg=WHITE)
        person(c, 330, 1440, 1.0, 5021, BLU, t, "hold" if at(t, "b1", "grabs", -0.1) else "shrug", "TRAVIS GRILLO", "happy" if at(t, "b1", "grabs", -0.1) else "meh", (1, 0), "short", 1.0, 34)
        if not at(t, "b1", "grabs", -0.2):
            nike_letter(c, 760, 1000, 0.6, t, 1.0, 1.0)
        else:
            recipe_card(c, 700, 980, 0.95, 5022, pk(t, "b1", "grabs"))
            if at(t, "b1", "hundred-year-old", -0.2):
                tape(c, "ABOUT 100 YEARS OLD", 700, 1220, 40, 2, pk(t, "b1", "hundred-year-old"), seed=5023, col=YEL)
        return
    if not b4: park_sign(c, 230, 1440, 0.75, 5024, "BOSTON COMMON", pk(t, "b3", "Boston"))
    for j, (tx, th) in enumerate(((90, 360),)):
        wline(c, [(tx, 1440), (tx, 1440 - th)], 5025 + j, 14, BROWN)
        ink(c, wellipse(tx, 1440 - th - 80, 120, 110, 5027 + j, 3), (120, 196, 100), 8)
    if not b4: pickle_cart(c, 600, 1440, 0.95, 5030, pk(t, "b3", None, -0.05), "2 FOR $1", t)
    if not b4:
        if at(t, "b3", "dollar,", -0.2):
            stamp(c, "$1", 820, 700, 120, -8, sk(t, "b3", "dollar,"), RED, 5031)
            coin_rain(c, t, TW("b3", "dollar,"), 6, 5032, 1440)
        if at(t, "b3", "cart", -0.2): tape(c, "A WOODEN CART", 520, 560, 44, -2, pk(t, "b3", "cart"), seed=5033, col=WHITE)
        return
    shelf(c, 750, 1440, 12, 340, 5034, 2, 3, "PICKLES")
    char(c, "pickle", 320, 1440, 0.95, t, mth(t, ["b4"]), (1, -0.2), "happy", "point", blink=blink(t), seed=5035)
    bubble(c, "Shelf? Not for me.", 420, 600, pk(t, "b4"), (-60, 200), 52, 560)
    if at(t, "b4", "Not", -0.1):
        ink(c, wellipse(750, 1170, 200, 280, 5036, 2), None, 12, RED)
        wline(c, [(590, 950), (910, 1390)], 5037, 14, RED)


# ---------------------------------------------------------------- the move (c1-c2): skip the aisle, stay cold
def S_cold(c, t, n):
    base(c)
    tape(c, "THE SURPRISING MOVE", 540, 470, 52, -3, pk(t, "c1", "surprising"), seed=5040, col=INK, fg=WHITE)
    c2 = at(t, "c2", None, -0.1)
    if not c2:
        shelf(c, 340, 1440, 12, 420, 5041, 3, 4, "PICKLES")
        tape(c, "PICKLE AISLE", 340, 620, 40, 2, 1.0, seed=5042, col=WHITE)
        if at(t, "c1", "aisle", -0.1):
            wline(c, [(140, 700), (540, 1400)], 5043, 16, RED); wline(c, [(540, 700), (140, 1400)], 5044, 16, RED)
        if at(t, "c1", "cold.", -0.3):
            pickle_tub(c, 790, 1440, 1.0, 5045, pk(t, "c1", "cold."), "PICKLES", eout(pr(t, TW("c1", "cold."), 0.6)))
            tape(c, "STAY COLD", 790, 1010, 48, 3, pk(t, "c1", "cold.", 0.15), seed=5046, col=SKY)
        return
    shelves = fridge(c, 360, 1440, 520, 860, eout(pr(t, L0("c2") - 0.1, 0.5)), 5047)
    for r, sy in enumerate(shelves[:2]):
        for j in range(2):
            kk = pk(t, "c2", None, 0.1 + 0.1 * (r * 2 + j))
            if kk > 0: pickle_tub(c, 240 + j * 240, sy - 6, 0.62, 5050 + r * 2 + j, kk, "PICKLES", 1.0)
    if at(t, "c2", "fridge", -0.1): tape(c, "THE FRIDGE CASE", 360, 1500, 40, 1, pk(t, "c2", "fridge"), seed=5055, col=SKY)
    if at(t, "c2", "jar", -0.2):
        pickle_jar(c, 820, 1440, 0.8, 5056, pk(t, "c2", "jar"))
        wline(c, [(700, 1000), (950, 1420)], 5057, 14, RED); wline(c, [(950, 1000), (700, 1420)], 5058, 14, RED)
        tape(c, "MADE COLD · SHIPPED COLD · SOLD COLD", 540, 640, 30, -1, pk(t, "c2", "jar", 0.2), seed=5059, col=WHITE)


# ---------------------------------------------------------------- the push (d1-d2): buyers want garlic oil; he keeps fresh garlic
def S_push(c, t, n):
    base(c)
    d2 = at(t, "d2", None, -0.1)
    person(c, 300, 1440, 0.95, 5021, BLU, t, "shrug" if not d2 else "up", "TRAVIS", "worried" if not d2 else "happy", (1, 0), "short", 1.0, 32)
    if not d2:
        for j in range(2):
            person(c, 620 + j * 190, 1440, 0.8, 5060 + j, (PUR, ORG)[j], t, "push", "BUYER", "neutral", (-1, 0), "short", pk(t, "d1", None, j * 0.12), 28)
        pickle_tub(c, 470, 1440, 0.6, 5059, 1.0, "PICKLES", 0.6)
        if at(t, "d1", "cheaper", -0.2):
            stamp(c, "SAVE $", 760, 640, 80, -6, sk(t, "d1", "cheaper"), RED, 5062)
        if at(t, "d1", "oil.", -0.3):
            oil_bottle(c, 560, 1150, 0.75, 5063, pk(t, "d1", "oil."))
            arrow(c, 700, 900, 620, 980, 30, INK, 7, 5064, pr(t, TW("d1", "oil."), 0.3))
        return
    oil_bottle(c, 780, 1440, 0.8, 5063, 1.0)
    wline(c, [(680, 1080), (880, 1430)], 5065, 14, RED); wline(c, [(880, 1080), (680, 1430)], 5066, 14, RED)
    garlic(c, 520, 1440, 1.0, 5067, pk(t, "d2"))
    bubble(c, "\"I kept my eye on quality.\"", 540, 620, pk(t, "d2", "kept", -0.2), (-180, 220), 50, 760)
    if at(t, "d2", "quality.\"", -0.1): tape(c, "TRAVIS GRILLO TO CCSU, 2019", 540, 860, 28, 1, pk(t, "d2", "quality.\""), seed=5068, col=WHITE)
    if at(t, "d2", "Good", -0.2): stamp(c, "GOOD CALL", 700, 1000, 60, -5, sk(t, "d2", "Good"), DGRN, 5069)


# ---------------------------------------------------------------- did it work (e1-e2): fridges fill up -> a buyer for the company
def S_win(c, t, n):
    base(c)
    e2 = at(t, "e2", None, -0.1)
    tape(c, "DID IT WORK?", 540, 470, 60, -3, pk(t, "e1"), seed=5070, col=INK, fg=WHITE)
    if not e2:
        m = int(24 * pr(t, L0("e1"), max(0.6, TW("e1", "seven") - L0("e1"))))
        for j in range(m):
            xx = 180 + (j % 6) * 140; yy = 780 + (j // 6) * 150
            pickle_tub(c, xx, yy, 0.42, 5071 + j, 1.0, "", 0.0)
        if at(t, "e1", "seven", -0.1):
            stamp(c, "~7,000 STORES", 540, 1390, 76, -4, sk(t, "e1", "seven", 0.1), RED, 5099)
            tape(c, "MID-2019", 820, 640, 40, 4, pk(t, "e1", "stores"), seed=5100, col=WHITE)
        return
    pickle_cart(c, 330, 1440, 0.7, 5030, 1.0, "2 FOR $1", t)
    person(c, 720, 1440, 0.9, 5101, ORG, t, "push", "KING'S HAWAIIAN", "happy", (-1, 0), "short", pk(t, "e2", "Hawaiian"), 28)
    if at(t, "e2", "buys", -0.2):
        stamp(c, "SOLD", 360, 860, 110, -8, sk(t, "e2", "buys"), RED, 5102)
        tape(c, "2021 · BUYS GRILLO'S", 540, 660, 44, 2, pk(t, "e2", "company."), seed=5103, col=YEL)


# ---------------------------------------------------------------- why now (a2): the pickle craze
def S_trend(c, t, n):
    base(c)
    tape(c, "WHY NOW?", 540, 470, 60, -3, pk(t, "a2"), seed=5110, col=INK, fg=WHITE)
    g1 = eout(pr(t, L0("a2") + 0.3, max(0.6, TW("a2", "thirty") - L0("a2") - 0.3))); g2 = eout(pr(t, TW("a2", "thirty") - 0.1, 0.8))
    bars(c, 540, 1300, [0.95 * g1 + 0.001, 0.14 * g2 + 0.001], 1.0, 5111, PKL, 220, 120, 560)
    text(c, "PICKLE", 370, 1360, 34, INK, BLK_F); text(c, "ALL SNACKS", 710, 1360, 34, INK, BLK_F)
    if g1 > 0.6: stamp(c, "+30%", 370, 680, 90, -6, sk(t, "a2", "thirty", 0.2), RED, 5112)
    if g2 > 0.6: text(c, "+3.8%", 710, 1150, 60, INK, MARK_F)
    chips_bag(c, 850, 800, 0.42, 5113, pk(t, "a2", "pickle-flavored"))
    if at(t, "a2", "year.", -0.3):
        tape(c, "SALES, PAST YEAR · CIRCANA VIA WSJ, 2026", 600, 585, 26, 2, pk(t, "a2", "year."), seed=5114, col=WHITE)
    you(c, 140, 1440, t, 0.5, "head" if at(t, "a2", "thirty", -0.2) else "stand", "shock" if at(t, "a2", "thirty", -0.2) else "neutral", (1, 0))


# ---------------------------------------------------------------- 3 moves (m1-m4)
def S_moves(c, t, n):
    base(c)
    tape(c, "3 MOVES YOU CAN STEAL", 540, 450, 52, -3, pk(t, "m1"), seed=5120, col=INK, fg=WHITE)
    moves = [("m1", "One:", "1. SHELF JARS? REGISTER + FILE"), ("m3", "Two:", "2. HOME KITCHEN? CHECK STATE"), ("m4", "Three:", "3. LICENSED KITCHEN + 1 CART")]
    cur = max([i for i, (l, w, _) in enumerate(moves) if at(t, l, w, -0.2)], default=0)
    for i, (l, w, lab) in enumerate(moves):
        if i <= cur:
            y = 550 + i * 74; tape(c, lab, 500, y, 32, (-2, 2, -1)[i], pk(t, l, w), seed=5121 + i, col=ORG if i == cur else WHITE)
            if i < cur: wline(c, [(850, y - 5), (870, y + 15), (910, y - 25)], 5125 + i, 8, RED)
    if cur == 0:
        m2 = at(t, "m2", None, -0.1)
        if not m2:
            pickle_jar(c, 300, 1440, 1.1, 5130, 1.0, "SHELF JAR")
            doc_stack(c, 740, 1440, 0.9, 5131, pk(t, "m1", "Register", -0.2), "FDA FILING")
            if at(t, "m1", "process", -0.2):
                tape(c, "REGISTER + FILE YOUR PROCESS BEFORE YOU PACK", 540, 1485, 26, 1, pk(t, "m1", "process"), seed=5132, col=WHITE)
                tape(c, "ACIDIFIED FOODS · 21 CFR 108 / 114", 740, 920, 26, 3, pk(t, "m1", "FDA", 0.1), seed=5133, col=YEL)
        else:
            shelves = fridge(c, 330, 1440, 460, 760, 0.0, 5134)
            for j in range(2): pickle_tub(c, 230 + j * 200, shelves[0] - 6, 0.55, 5135 + j, 1.0, "PICKLES", 1.0)
            stamp(c, "SKIPS THAT RULE", 760, 960, 52, -6, sk(t, "m2", "skip"), DGRN, 5137)
            tape(c, "COLD PLANT TO STORE · STATE RULES STILL APPLY", 540, 1490, 26, 1, pk(t, "m2"), seed=5138, col=SKY)
    elif cur == 1:
        stove(c, 540, 1440, 0.6, 5140, 1.0, 0.0)
        state_card(c, 270, 1000, 0.85, 5141, pk(t, "m3", "Texas"), "TEXAS", True, "PH 4.6 OR LESS · DIRECT SALES", pr(t, TW("m3", "allows"), 0.4))
        state_card(c, 810, 1000, 0.85, 5142, pk(t, "m3", "Michigan"), "MICHIGAN", False, "NO HOME PICKLES", pr(t, TW("m3", "doesn't."), 0.4))
        tape(c, "COTTAGE FOOD RULES DIFFER BY STATE", 540, 1485, 28, 1, pk(t, "m3", "home?"), seed=5143, col=WHITE)
    else:
        you(c, 200, 1440, t, 0.8, "point", "happy", (1, 0))
        health_permit(c, 760, 1100, 0.6, 5150, pk(t, "m4"), pr(t, TW("m4", "kitchen,"), 0.4), ("LICENSED", "KITCHEN"))
        if at(t, "m4", "cart", -0.3):
            pickle_cart(c, 480, 1440, 0.55, 5151, pk(t, "m4", "cart"), "TEST", t)
            tape(c, "LOCAL VENDOR PERMIT REQUIRED", 540, 1485, 30, 1, pk(t, "m4", "cart", 0.2), seed=5152, col=ORG)


# ---------------------------------------------------------------- callback (f1-f2): the Nike dream -> a pickle sneaker
def S_end(c, t, n):
    base(c)
    f2 = at(t, "f2", None, -0.1)
    person(c, 250, 1440, 0.95, 5021, BLU, t, "up" if f2 else "shrug", "TRAVIS", "happy", (1, 0), "short", 1.0, 32)
    if not at(t, "f1", "later", -0.2):
        nike_letter(c, 680, 1000, 0.75, t, 1.0, 1.0)
        text(c, "?", 900, 720, 130, RED, MARK_F)
        return
    sneaker(c, 640, 1300, 0.95, 5160, pk(t, "f1", "later"), f2)
    bubble(c, "\"Now I own my own sneaker line...\"", 600, 620, pk(t, "f1", "later"), (-200, 220), 44, 720)
    if f2:
        for j in range(3):
            kk = pk(t, "f2", "pickles", j * 0.1)
            if kk > 0: pickle_spear(c, 560 + j * 150, 1060 - (j % 2) * 40, 0.8, 70, 5161 + j, kk)
        tape(c, "A PICKLE SNEAKER COLLAB · 2019", 600, 880, 32, 1, pk(t, "f2", "pickles", 0.2), seed=5165, col=WHITE)


def S_z(c, t, n):
    base(c)
    z2 = t >= L0("z2") - 0.05
    if not z2:
        tape(c, "SEND THIS TO...", 540, 480, 58, -3, pk(t, "z1"), seed=5170, col=INK, fg=WHITE)
        bubble(c, "the friend who puts pickles on everything", 540, 690, pk(t, "z1", "friend"), (-180, 200), 48, 760)
        phone(c, 260, 1200, 0.5, 5171)
        person(c, 760, 1440, 0.75, 5172, PNK, t, "hold", "FRIEND", "happy", (-1, 0), "long", 1.0, 30)
        for j in range(4):
            kk = pk(t, "z1", "everything.", j * 0.08)
            if kk > 0: pickle_spear(c, 640 + j * 80, 980 + (j % 2) * 40, 0.6, 20 + j * 30, 5173 + j, kk)
        arrow(c, 330, 1100, 640, 1040, 60, RED, 8, 5178, pr(t, TW("z1", "friend") - 0.2, 0.5))
    else:
        title(c, "CHIPS OR BEER?", 540, 560, 80, INK, pk(t, "z2"))
        chips_bag(c, 300, 1400, 1.1, 5180, 1.0)
        char(c, "tallcan", 780, 1440, 0.8, t, 0.0, (-1, 0), "happy", "wave", blink=blink(t), seed=5181, label="PICKLE BEER", col=(190, 220, 150))
        stamp(c, "CHIPS", 300, 880, 80, -6, sk(t, "z2", "chips,"), DGRN, 5182)
        stamp(c, "BEER", 780, 880, 80, 6, sk(t, "z2", "beer?"), RED, 5183)
        tape(c, "COMMENT BELOW", 540, 1485, 36, 2, pk(t, "z2", "comments."), seed=5184, col=WHITE)

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
