# DUBAI CHOCOLATE case study + 4 tricks to steal. DOODLE look (graph paper, wobbly ink, object characters, transcript strip).
def L0(lid): return LINES[lid]["start"]


def L1(lid): return LINES[lid]["end"]


def TW(lid, w, nth=0, off=0.0):
    try: return T(lid, w, nth) + off
    except Exception: return L0(lid) + off


_SEQ = [k for k in LINES if k not in ("z2", "s2b")]
_TR = {"i2": "pop", "a1": "whip", "a6": "pop", "b1": "whip", "b3": "pop", "c1": "whip", "c4": "pop", "t1": "whip", "s1": "pop", "s2": "pop",
       "s3": "pop", "s4": "pop", "e1": "pop", "z1": "pop"}
SHOTLIST = [("S_i1", 0.0, "cut")] + [(f"S_{k}", L0(k) - 0.06, _TR.get(k, "cut")) for k in _SEQ[1:]]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr) for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
CUES = [(0.15, "impact"), (TW("i1", "shortage?"), "buzz"), (TW("i2", "pregnant"), "pop"), (TW("i3", "twenty"), "chaching"), (TW("i3", "nobody"), "buzz"),
        (TW("i4", "one"), "stamp"), (TW("i4", "four"), "stamp"), (L0("a1"), "pop"), (TW("a2", "stuffed"), "pop"), (TW("a3", "Pistachio"), "pop"),
        (TW("a3", "crunchy"), "tick"), (TW("a4", "themselves,"), "ding"), (TW("a5", "single"), "buzz"), (L0("a6"), "boing"),
        (TW("b1", "cracked"), "slam"), (TW("b2", "crunch,"), "tick"), (TW("b2", "green"), "pop"), (TW("b3", "hundred"), "chaching"),
        (TW("b4", "hundreds"), "chaching"), (TW("b5", "capped"), "stamp"), (TW("b5", "Gone"), "whoosh"), (TW("b6", "global."), "ding"),
        (TW("c1", "Lindt"), "pop"), (TW("c1", "Costco"), "pop"), (TW("c2", "twelve"), "chaching"), (TW("c3", "never"), "stamp"),
        (L0("c4"), "boing"), (TW("c5", "thirty-five"), "stamp"), (TW("t1", "break"), "slam"), (TW("s1", "one."), "stamp"),
        (TW("s2", "two."), "stamp"), (TW("s2b", "travels."), "whoosh"), (TW("s3", "Third,"), "stamp"), (TW("s4", "last"), "stamp"),
        (TW("s5", "copycats."), "boing"), (TW("e1", "crave"), "ding"), (L0("z1"), "whoosh"), (L0("z2"), "pop")]


def lt(t, sid): return t - SHOT[sid]["start"]


# ======================================================================== drawing
import skia, runpy
exec(open(f"{_D}/doodlekit.py").read())
SURF = skia.Surface(W, H)
_VL = {l[0]: l[1] for l in runpy.run_path(f"{B}/scripts/vo_lines.py")["LINES"]}
DISP = {"i3": "Imagine you're her. You charge about $20 a bar, and almost nobody will pay it.",
        "i4": "Then 1 video changes everything. I'll show you what happened, then 4 tricks you can steal for your own food business.",
        "a1": "Meet Sarah Hamouda. In 2021 she was pregnant in Dubai, and she craved something oddly specific.",
        "b3": "Guess how many people watched it? More than 100 million.", "b5": "They capped it at 500 a day, sold only in Dubai, through a delivery app. Gone in minutes.",
        "b6": "Her words: \"To be honest, not at any point did I think this was going to become global.\"",
        "c2": "Within about a year, US unit sales of pistachio-filled chocolate were up over 1,200%.",
        "c3": "Grocery boss Stew Leonard Jr. said he'd never seen a single item sell like this in 50 years.",
        "c5": "Pistachio kernel prices jumped about 35%. Chocolate makers grabbed every kernel they could, and the US crop came up short.",
        "s1": "Trick number one. Build around a single hero product, not a menu of 20.", "z1": "Send this to the friend who'd happily pay $20 for a chocolate bar."}
_ORDER = [l for l in LINES]
_LW = {}
for _w in WORDS: _LW.setdefault(_w["line"], []).append(_w["t"])
CHOC_L = {"a6"}; PIS_L = {"c4"}


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
    base(c, tint=(150, 200, 60))
    cr = pr(t, 0.2, 0.5)
    char(c, "choc", 380, 1440, 1.15, t, 0, (0.5, -0.3), "shock" if cr > 0.5 else "happy", "shrug", blink=blink(t), crack=cr)
    for i in range(3): char(c, "pista", 760 + (i - 1) * 110, 1440, 0.42, t, 0, (-0.5, -0.3), "shock", "up", walk=True, blink=False, shadow_w=0.6) if t > 0.6 + i * 0.2 else None
    tape(c, "1 BAR + A PISTACHIO SHORTAGE?!", 540, 600, 46, -3, pop_k(t, 0.05, 0.25), seed=3)


def S_i2(c, t, n):
    base(c, tint=PNK)
    person(c, 380, 1440, 1.45, 4, (60, 40, 30), t, "head", "SARAH, DUBAI", "happy", (1, 0), "long")
    bubble(c, "I just want a snack...", 720, 760, pop_k(t, TW("i2", "snack.") - 0.4, 0.25), (-220, 260), 54, 520, think=True)


def S_i3(c, t, n):
    base(c, tint=SKY)
    char(c, "choc", 540, 1440, 1.1, t, 0, (0, 0.3), "worried", "shrug", blink=blink(t))
    tape(c, "$20 A BAR", 300, 640, 56, -4, pop_k(t, TW("i3", "twenty") - 0.1, 0.25), seed=6)
    stamp(c, "ALMOST NOBODY BUYS", 700, 780, 56, 6, stamp_k(t, TW("i3", "nobody")), RED, 7)


def S_i4(c, t, n):
    base(c, tint=YEL)
    phone_video(c, 300, 1050, 0.9, t=t, views="▶", k=pop_k(t, TW("i4", "video") - 0.2, 0.3))
    title(c, "1 VIDEO", 300, 640, 90, RED, pop_k(t, TW("i4", "one"), 0.3))
    title(c, "+ 4 TRICKS", 760, 760, 90, DGRN, pop_k(t, TW("i4", "four"), 0.3), 3)
    char(c, "choc", 790, 1440, 0.6, t, 0, (-0.5, -0.3), "happy", "cheer", blink=blink(t))


# ---------------------------------------------------------------- the craving
def S_a1(c, t, n):
    base(c, tint=PNK)
    person(c, 330, 1440, 1.45, 4, (60, 40, 30), t, "stand", "SARAH HAMOUDA", "happy", (1, 0), "long")
    tape(c, "DUBAI · 2021", 720, 640, 56, 3, pop_k(t, TW("a1", "twenty") - 0.1, 0.25), seed=8)
    bubble(c, "Something oddly specific...", 740, 860, pop_k(t, TW("a1", "specific.") - 0.3, 0.25), (-260, 200), 46, 420, think=True)


def S_a2(c, t, n):
    base(c)
    char(c, "choc", 360, 1440, 1.0, t, 0, (0.5, -0.3), "happy", "hips", blink=blink(t))
    k = pop_k(t, TW("a2", "stuffed") - 0.1, 0.3)
    if k > 0: c.save(); c.translate(780, 1100); c.scale(k, k); ink(c, wellipse(0, 0, 150, 90, 20, 2), (230, 170, 90), 8); [wline(c, [(-120 + j * 30, -40), (-100 + j * 30, 50)], 21 + j, 5, (250, 220, 150)) for j in range(9)]; c.restore()
    tape(c, "+ THE DESSERTS SHE GREW UP WITH", 540, 640, 42, -2, pop_k(t, TW("a2", "grew") - 0.2, 0.25), seed=9)


def S_a3(c, t, n):
    base(c, tint=(150, 200, 60))
    for i, (w_, x, col, wd) in enumerate((("PISTACHIO CREAM", 270, (150, 200, 60), "Pistachio"), ("TAHINI", 540, (230, 200, 150), "tahini,"), ("SHREDDED PASTRY", 810, (230, 170, 90), "crunchy"))):
        k = pop_k(t, TW("a3", wd) - 0.15, 0.3)
        if k > 0:
            c.save(); c.translate(x, 1200); c.scale(k, k); ink(c, wpoly([(-120, -80), (120, -80), (100, 120), (-100, 120)], 30 + i, 2, True, 40), WHITE, 8)
            ink(c, wellipse(0, -60, 110, 40, 33 + i, 1.4), col, 6); c.restore()
            tape(c, w_, x, 1000 + (i % 2) * 70, 34, (-4, 3, -2)[i], k, seed=40 + i, col=YEL)
    tape(c, "LIKE THE DESSERT \"KNAFEH\"", 540, 640, 46, -3, pop_k(t, TW("a3", "knafeh.") - 0.2, 0.25), seed=43)


def S_a4(c, t, n):
    base(c)
    stamp(c, "NOBODY SOLD IT", 540, 620, 76, -6, stamp_k(t, TW("a4", "Nobody")), RED, 44)
    person(c, 300, 1440, 1.2, 4, (60, 40, 30), t, "hold", None, "happy", (1, 0), "long")
    person(c, 780, 1440, 1.25, 12, BLU, t, "hold", "+ HUSBAND", "happy", (-1, 0))
    if t > TW("a4", "themselves,") - 0.2: char(c, "choc", 540, 1440, 0.5, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t))
    tape(c, "SIDE PROJECT", 540, 800, 50, 3, pop_k(t, TW("a4", "side") - 0.1, 0.25), seed=45, col=YEL)


def S_a5(c, t, n):
    base(c, tint=(170, 170, 180))
    char(c, "choc", 400, 1440, 1.0, t, 0, (0.4, 0.3), "worried", "down", blink=blink(t))
    tape(c, "\"CAN'T GET KNAFEH OF IT\"", 540, 620, 48, -3, pop_k(t, TW("a5", "called") - 0.1, 0.25), seed=46)
    k = pr(t, TW("a5", "single") - 0.2, 0.8)
    if k > 0:
        wline(c, [(640, 1300), (640, 900)], 47, 7); wline(c, [(640, 1300), (960, 1300)], 48, 7)
        wline(c, [(660, 1270), (720, 1268), (780, 1274), (860, 1266), (940, 1270)][:max(2, int(5 * k))], 49, 10, RED, 1.2)
        text(c, "ORDERS", 800, 880, 36, INK, BLK_F)


def S_a6(c, t, n):
    base(c, tint=YEL)
    char(c, "choc", 540, 1440, 1.25, t, mth(t, CHOC_L), (0, -0.3), "happy", "shrug", blink=blink(t))
    bubble(c, "I was the best-kept secret in Dubai. A little too well kept.", 540, 640, pop_k(t, L0("a6"), 0.25), (-40, 210), 58, 740)


# ---------------------------------------------------------------- the video
def S_b1(c, t, n):
    base(c, tint=SKY)
    ink(c, wrrect(160, 1050, 920, 1400, 60, 50, 2.4), RED, 9); ink(c, wrrect(240, 940, 840, 1090, 40, 51, 2), SKY, 8)
    for wx in (300, 780): ink(c, wellipse(wx, 1410, 60, 60, 52, 1.4), INK, 0)
    person(c, 540, 1180, 0.8, 30, PUR, t, "hold", None, "happy", (0, 0), "long")
    cr = pr(t, TW("b1", "cracked") - 0.1, 0.4)
    c.save(); c.translate(540, 1100); c.scale(0.4, 0.4); c.translate(-540, -1100); char(c, "choc", 540, 1100, 1.0, t, 0, (0, -0.3), "shock", "down", blink=False, crack=cr, shadow_w=0.0); c.restore()
    tape(c, "MARIA VEHERA · FOOD CREATOR", 540, 620, 44, -3, pop_k(t, TW("b1", "Maria") - 0.1, 0.25), seed=53)
    tape(c, "IN HER CAR", 540, 760, 46, 3, pop_k(t, TW("b1", "car,") - 0.1, 0.25), seed=54, col=YEL)


def S_b2(c, t, n):
    base(c, tint=(150, 200, 60))
    cr = pr(t, TW("b2", "crunch,") - 0.15, 0.3)
    char(c, "choc", 540, 1440, 1.35, t, 0, (0, -0.3), "shock", "shrug", blink=False, crack=cr)
    if t > TW("b2", "crunch,") - 0.05: title(c, "CRUNCH!", 300, 760, 110, ORG, pop_k(t, TW("b2", "crunch,"), 0.25), -8)
    if t > TW("b2", "green") - 0.1: title(c, "GREEN!", 800, 680, 100, DGRN, pop_k(t, TW("b2", "green"), 0.25), 8)


def S_b3(c, t, n):
    base(c, tint=PNK)
    k = pr(t, TW("b3", "hundred") - 0.3, 0.6)
    for i in range(int(12 * k)):
        x = 140 + (i % 6) * 160; y = 1300 - (i // 6) * 300
        c.save(); c.translate(x, y); c.scale(0.32, 0.32); phone_video(c, 0, 0, 1.0, 400 + i, t=t + i * 0.3, play=False); c.restore()
    title(c, "100,000,000+ VIEWS", 540, 680, 72, RED, pop_k(t, TW("b3", "hundred"), 0.3), -3, BLK_F)


def S_b4(c, t, n):
    base(c, tint=GRN)
    wline(c, [(150, 1340), (150, 760)], 50, 8); wline(c, [(150, 1340), (930, 1340)], 51, 8)
    k = pr(t, TW("b4", "jumped") - 0.1, 1.0); pts = [(170, 1320), (330, 1316), (490, 1310), (650, 1200), (780, 980), (910, 800)]
    if k > 0: wline(c, pts[:max(2, int(len(pts) * k + 0.999))], 52, 14, GRN, 1.4)
    tape(c, "SINGLE DIGITS TO HUNDREDS A DAY", 540, 620, 42, -3, pop_k(t, TW("b4", "hundreds") - 0.2, 0.25), seed=55)
    tape(c, "STILL HANDMADE", 680, 1200, 44, 3, pop_k(t, TW("b4", "hand.") - 0.2, 0.25), seed=56, col=YEL)


def S_b5(c, t, n):
    base(c)
    stamp(c, "500 A DAY", 300, 640, 76, -6, stamp_k(t, TW("b5", "capped")), RED, 57)
    tape(c, "ONLY IN DUBAI", 760, 680, 48, 4, pop_k(t, TW("b5", "Dubai,") - 0.1, 0.25), seed=58, col=YEL)
    u = pr(t, TW("b5", "app.") - 0.3, 1.2); scooter(c, 120 + 760 * u, 1440, 1.0)
    stamp(c, "SOLD OUT", 540, 920, 96, -8, stamp_k(t, TW("b5", "Gone")), RED, 59)


def S_b6(c, t, n):
    base(c, tint=YEL)
    person(c, 300, 1440, 1.35, 4, (60, 40, 30), t, "up", "SARAH", "shock", (1, 0), "long")
    bubble(c, "\"Not at any point did I think this was going to become global.\"", 680, 760, pop_k(t, TW("b6", "Not") - 0.1, 0.25), (-280, 260), 50, 600)


# ---------------------------------------------------------------- the spread
def S_c1(c, t, n):
    base(c)
    tape(c, "EVERYONE JUMPED IN", 540, 600, 60, -3, pop_k(t, L0("c1"), 0.25), seed=60)
    for i, (sg, w_) in enumerate((("LINDT", "Lindt"), ("TRADER JOE'S", "Trader"), ("COSTCO", "Costco"))):
        k = pop_k(t, TW("c1", w_) - 0.15, 0.3)
        if k > 0: c.save(); c.translate(200 + i * 340, 1440); c.scale(k, k); store(c, 0, 0, 280, 220, 61 + i, sign=sg); c.restore()
        if k > 0: c.save(); c.translate(200 + i * 340, 1000); c.scale(k * 0.45, k * 0.45); c.translate(-(200 + i * 340), -1000); char(c, "choc", 200 + i * 340, 1000, 1.0, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t, i), crack=0.0, shadow_w=0.0); c.restore()


def S_c2(c, t, n):
    base(c, tint=GRN)
    k = pr(t, TW("c2", "jumped") - 0.3, 0.9)
    for i, (x, h_) in enumerate(((330, 60), (750, 560))):
        hh = h_ * (1 if i == 0 else ease(k)); col = GREY if i == 0 else (150, 200, 60)
        if hh > 2: ink(c, wpoly([(x - 110, 1440), (x - 110, 1440 - hh), (x + 110, 1440 - hh), (x + 110, 1440)], 70 + i, 2, True, 40), col, 9)
    text(c, "YEAR BEFORE", 330, 1500, 40, INK, BLK_F); text(c, "MID-2025", 750, 1500, 40, INK, BLK_F)
    title(c, "+1,234%", 640, 760, 140, DGRN, pop_k(t, TW("c2", "twelve"), 0.3), -3, BLK_F)
    tape(c, "US UNIT SALES · MID-2025", 540, 600, 38, -2, pop_k(t, L0("c2"), 0.25), seed=72)


def S_c3(c, t, n):
    base(c)
    person(c, 280, 1440, 1.35, 8, GREY, t, "stand", "STEW LEONARD JR.", "shock", (1, 0))
    bubble(c, "Never seen a single item sell like this.", 680, 760, pop_k(t, TW("c3", "never") - 0.1, 0.25), (-260, 260), 54, 560)
    stamp(c, "50 YEARS IN GROCERY", 680, 1100, 54, 6, stamp_k(t, TW("c3", "fifty")), RED, 73)


def S_c4(c, t, n):
    base(c, tint=YEL)
    char(c, "pista", 540, 1440, 1.4, t, mth(t, PIS_L), (0, -0.3), "happy", "hips", blink=blink(t))
    bubble(c, "And me? Suddenly I'm expensive. Thanks a lot, chocolate.", 540, 640, pop_k(t, L0("c4"), 0.25), (-40, 200), 60, 700)


def S_c5(c, t, n):
    base(c, tint=RED)
    wline(c, [(150, 1340), (150, 760)], 80, 8); wline(c, [(150, 1340), (930, 1340)], 81, 8)
    k = pr(t, TW("c5", "jumped") - 0.1, 1.0); pts = [(170, 1250), (400, 1240), (600, 1180), (780, 980), (910, 900)]
    if k > 0: wline(c, pts[:max(2, int(len(pts) * k + 0.999))], 82, 14, RED, 1.4)
    text(c, "$7.65/lb", 260, 1210, 38, INK, BLK_F)
    if k >= 1: text(c, "$10.30/lb", 820, 860, 42, RED, BLK_F)
    title(c, "+35%", 540, 680, 130, RED, pop_k(t, TW("c5", "thirty-five"), 0.3), -3, BLK_F)
    tape(c, "PISTACHIO KERNELS", 540, 560, 44, 2, pop_k(t, L0("c5"), 0.25), seed=83, col=YEL)
    for i in range(3): char(c, "pista", 760 + i * 70, 1440, 0.3, t, 0, (1, 0), "shock", "up", walk=True, shadow_w=0.5) if t > TW("c5", "grabbed") - 0.3 + i * 0.15 else None


def S_t1(c, t, n):
    base(c)
    for i, (w_, x, y, wd) in enumerate((("ADS", 260, 640, "ads."), ("BIG FACTORY", 760, 700, "factory."))):
        k = pop_k(t, TW("t1", wd) - 0.2, 0.25)
        if k > 0: tape(c, w_, x, y, 50, (-4, 4)[i], k, seed=90 + i, col=GREY); strike(c, x - 150, y, x + 150, pr(t, TW("t1", wd) + 0.1, 0.3))
    cr = pr(t, TW("t1", "break") - 0.15, 0.3)
    char(c, "choc", 540, 1440, 1.05, t, 0, (0, -0.3), "happy", "cheer", blink=blink(t), crack=cr)
    tape(c, "ONE WEIRD, SPECIFIC PRODUCT", 540, 860, 46, -2, pop_k(t, TW("t1", "specific") - 0.1, 0.25), seed=92, col=YEL)


# ---------------------------------------------------------------- 4 tricks
def trick(c, t, t0, num, label, col):
    stamp(c, f"TRICK {num}", 540, 590, 90, (-5, 4, -3, 5)[num - 1], stamp_k(t, t0), col, 100 + num)
    tape(c, label, 540, 750, 48, (3, -3, 2, -2)[num - 1], pop_k(t, t0 + 0.25, 0.25), seed=101 + num)


def S_s1(c, t, n):
    base(c, tint=YEL)
    trick(c, t, TW("s1", "one."), 1, "ONE HERO PRODUCT", BLU)
    char(c, "choc", 330, 1440, 1.0, t, 0, (0.4, -0.3), "happy", "cheer", blink=blink(t))
    k = pop_k(t, TW("s1", "menu") - 0.1, 0.3)
    if k > 0:
        c.save(); c.translate(790, 1150); c.scale(k, k); ink(c, wrrect(-150, -220, 150, 220, 10, 110, 2), WHITE, 8)
        for j in range(8): wline(c, [(-110, -170 + j * 48), (110 - (j % 3) * 30, -170 + j * 48)], 111 + j, 4, GREY)
        c.restore(); strike(c, 640, 1150, 940, pr(t, TW("s1", "twenty.") - 0.1, 0.3))


def S_s2(c, t, n):
    base(c, tint=PNK)
    trick(c, t, TW("s2", "two."), 2, "DESIGN THE FILMABLE MOMENT", ORG)
    phone_video(c, 300, 1150, 0.85, t=t)
    for i, (w_, wd) in enumerate((("CRACK", "crack,"), ("PULL", "pull,"), ("DRIP", "drip."))):
        tape(c, w_, 780, 950 + i * 130, 48, (-4, 3, -2)[i], pop_k(t, TW("s2", wd) - 0.1, 0.25), seed=120 + i, col=YEL)


def S_s3(c, t, n):
    base(c, tint=(150, 200, 60))
    trick(c, t, TW("s3", "Third,"), 3, "USE WHAT YOU KNOW", RED)
    person(c, 330, 1440, 1.3, 4, (60, 40, 30), t, "up", None, "happy", (1, 0), "long")
    bubble(c, "Grandma's recipe?", 760, 1000, pop_k(t, TW("s3", "edge?") - 0.1, 0.25), (-200, 180), 50, 400, think=True)


def S_s4(c, t, n):
    base(c, tint=SKY)
    trick(c, t, TW("s4", "last"), 4, "START SMALL + LEGAL", DGRN)
    k = pop_k(t, TW("s4", "rules") - 0.1, 0.3)
    if k > 0:
        c.save(); c.translate(320, 1150); c.scale(k, k); ink(c, wrrect(-220, -170, 220, 170, 10, 130, 2), WHITE, 9)
        text(c, "HOME FOOD RULES", 0, -100, 34, INK, BLK_F)
        for j, w_ in enumerate(("STATE A: OK", "STATE B: LIMITS", "STATE C: NO")): text(c, w_, 0, -30 + j * 60, 36, (DGRN, ORG, RED)[j], "Kalam-Bold.ttf")
        c.restore()
    if t > TW("s4", "test") - 0.2: scooter(c, 780, 1440, 0.8)
    tape(c, "TEST LOCALLY FIRST", 780, 1000, 40, 3, pop_k(t, TW("s4", "test") - 0.1, 0.25), seed=131, col=YEL)


def S_s5(c, t, n):
    base(c)
    for i in range(4):
        if t > TW("s5", "copycats.") - 0.3 + i * 0.12: char(c, "choc", 160 + i * 250, 1440, 0.55, t, 0, (0, -0.3), "happy", "hips", blink=blink(t, i))
    tape(c, "EXPECT COPYCATS", 540, 620, 56, -3, pop_k(t, TW("s5", "copycats.") - 0.1, 0.25), seed=140)
    stamp(c, "STORY + QUALITY", 540, 800, 66, 5, stamp_k(t, TW("s5", "story")), DGRN, 141)


def S_e1(c, t, n):
    base(c, tint=YEL)
    tape(c, "TRY IT NEXT TIME", 540, 560, 58, -3, pop_k(t, TW("e1", "Try") - 0.1, 0.25), seed=150)
    title(c, "WHAT DO YOU CRAVE", 540, 760, 76, INK, pop_k(t, TW("e1", "crave") - 0.1, 0.3))
    title(c, "THAT NOBODY SELLS?", 540, 870, 76, RED, pop_k(t, TW("e1", "nobody") - 0.1, 0.3))
    person(c, 540, 1440, 1.1, 151, ORG, t, "head", None, "happy")


def S_z1(c, t, n):
    base(c, tint=PNK)
    z2 = t >= L0("z2") - 0.05
    char(c, "choc", 300, 1440, 0.85, t, 0, (0.4, -0.3), "happy", "wave", blink=blink(t))
    char(c, "pista", 790, 1440, 0.9, t, 0, (-0.4, -0.3), "happy", "wave", blink=blink(t, 3))
    if not z2:
        tape(c, "SEND THIS TO...", 540, 560, 58, -3, pop_k(t, L0("z1"), 0.25), seed=33)
        bubble(c, "the friend who'd pay $20 for a chocolate bar", 540, 780, pop_k(t, TW("z1", "friend") - 0.1, 0.25), (-180, 200), 56, 720)
    else:
        title(c, "WOULD YOU PAY $20?", 540, 660, 84, INK, pop_k(t, L0("z2"), 0.3))
        stamp(c, "YES", 360, 840, 90, -6, stamp_k(t, TW("z2", "YES")), DGRN, 160)
        stamp(c, "NO", 720, 840, 90, 6, stamp_k(t, TW("z2", "NO.")), RED, 161)


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
