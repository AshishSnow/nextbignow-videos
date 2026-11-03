# ================= shots: FreshNestHub 22 — "Why does crispy namkeen go soft once you open the box?" (Chubby INK, ep 6 of the ink look) ===
# COLOUR SCRIPT: RANI PINK = gift box, titles, chips; WATER BLUE = water, always; namkeen = natural fried gold (goes pale when it has drunk). Dry stages = sandy, wet stages = blue: you can read the state by the background.
# Places: the NEW Diwali lane (4 parallax layers, set_lane + lane_front) and the NEW Diwali room (set_droom + table_front). CRAFT (ep 22): THE WALK CYCLE (anim_fx.walk: contact-down-passing-up, the planted foot never slides) + three-quarter head (turn=).
# The hero explaining device: THE THIRST METER (water activity) as a plank he WALKS on: 0.3 to the danger zone is literally two steps.
SHOTLIST = [
    ("S0", 0.0, "cut"), ("S1", T("i2", "It") - 0.2, "whip"), ("S1b", T("i2", "its") - 0.1, "punch"), ("S2", T("i3", "And") - 0.15, "whip"),
    ("S3", T("a1", "A") - 0.2, "flash"), ("S4", T("a2", "Thats") - 0.15, "punch"), ("S4b", T("a2", "Its") - 0.12, "whip"),
    ("S5", T("a3", "Your") - 0.2, "focus"), ("S6", T("a4", "And") - 0.15, "whip"),
    ("S7", T("b1", "Food") - 0.2, "flash"), ("S7b", T("b1", "The") - 0.12, "zoom"), ("S8", T("b2", "A") - 0.2, "punch"), ("S9", T("b3", "So") - 0.15, "whip"), ("S10", T("b4", "Breads") - 0.2, "whip"),
    ("S11", T("c1", "So") - 0.2, "flash"), ("S12", T("c2", "Dry") - 0.2, "whip"), ("S12b", T("c2", "Cooked") - 0.12, "whip"), ("S12c", T("c2", "Its") - 0.12, "zoom"),
    ("S13", T("c3", "Your") - 0.2, "punch"), ("S13b", T("c3", "like") - 0.12, "whip"), ("S14", T("c4", "A") - 0.15, "zoom"), ("S14b", T("c4", "Now") - 0.12, "punch"), ("S15", T("c5", "And") - 0.15, "whip"),
    ("S16", T("d1", "And") - 0.2, "flash"), ("S16b", T("d1", "chips") - 0.1, "zoom"), ("S17", T("d2", "A") - 0.15, "whip"),
    ("S18", T("e1", "But") - 0.2, "focus"), ("S19", T("e2", "Crispy") - 0.15, "whip"), ("S20", T("e3", "Bakers") - 0.2, "whip"), ("S20b", T("e3", "and") - 0.1, "punch"), ("S21", T("e4", "Your") - 0.15, "whip"),
    ("S22", T("f1", "So,") - 0.2, "flash"), ("S22b", T("f1", "Lid") - 0.15, "whip"), ("S23", T("f2", "Second,") - 0.2, "whip"),
    ("S24", T("f3", "And") - 0.2, "flash"), ("S24b", T("f3", "A") - 0.12, "whip"), ("S24c", T("f3", "or") - 0.1, "punch"), ("S25", T("f4", "The") - 0.2, "zoom"), ("S25b", T("f4", "Just") - 0.12, "whip"),
    ("S26", T("g1", "One") - 0.2, "flash"), ("S26b", T("g1", "but") - 0.1, "whip"), ("S26c", T("g1", "thats") - 0.1, "punch"), ("S26d", T("g1", "No") - 0.1, "whip"),
    ("S27", T("h1", "So") - 0.2, "flash"), ("S28", T("h2", "Send") - 0.2, "whip"),
]
SHOTS = [dict(id=k, start=round(st, 3), end=round(SHOTLIST[i + 1][1], 3) if i + 1 < len(SHOTLIST) else END, trans=tr)
         for i, (k, st, tr) in enumerate(SHOTLIST)]
SHOT = {s["id"]: s for s in SHOTS}
IRIS = {}
SRC_G = "Source: The Globe and Mail · ScienceABC"
SRC_W = "Source: Wageningen University (2008)"
SRC_K = "Source: Katz & Labuza 1981, via Wageningen"
SRC_B = "Source: J Food Sci Technol 2018 (barfi)"
SRC_C = "Source: King Arthur Baking · Exploratorium"
SRC_O = "Source: ScienceABC · Food Republic"
SRC_R = "Source: ScienceABC · Baking Business"
TOP = 1330
RED_I = (176, 52, 44)


def lt(t, sid): return t - SHOT[sid]["start"]


def st_(sid): return SHOT[sid]["start"]


def en_(sid): return SHOT[sid]["end"]


def ui_word(f, lead, big, y, t, t0, col=INKC, acc=ACC, size=170, out=None, shadow=0.0, lead_col=None, tail=""):
    el = ed_el(lead, big, tail, big_col=col, acc=acc, lead_col=lead_col or col, big_size=size, shadow=shadow)
    ed_show(f, el, W / 2, y, t, t0, 0.34, out)


def icap(f, lead, big, t, t0, acc=ACC_S, size=150, y=440, out=None, tail="", dark=False):
    if dark: ui_word(f, lead, big, y, t, t0, col=WHITE, acc=acc, size=size, shadow=0.6, lead_col=WHITE, out=out, tail=tail)
    else: ui_word(f, lead, big, y, t, t0, col=INKC, acc=acc, size=size, shadow=0.0, lead_col=INKC, out=out, tail=tail)


def ramp(t, t0, d=0.5): return eio(clamp((t - t0) / max(1e-3, d)))


def slam(f, el, x, y, rot, t, t0, s=1.0):
    if t >= t0: rot_comp(f, el, x, y, rot, s * (1.5 - 0.5 * eo(clamp((t - t0) / 0.18))), clamp((t - t0) / 0.1), 0.3)


def ichip(text, size=26, inv=False): return chip(text, INKC if not inv else MILK, MILK if not inv else INKC, size)


def achip(text, size=30): return chip(text, ACC_S, MILK, size)


def bchip(text, size=30): return chip(text, WATER_S, MILK, size)


def t3(f, text, y, t, t0, size=230, face=None, side=None, x=540):
    if t >= t0: title_ink(f, text, y, t, t0, size=size, face=face or ACC_L, side=side or ACC_S, depth=18, x=x)


def nolean(p): return {k: v for k, v in p.items() if k != "lean"}


def src(f, text, t, t0, y=1462):
    if t >= t0: comp(f, chip(text, INKC, MILK, 22), 540, y, op=clamp((t - t0) / 0.2))


def card(f, x, y, w, h, col=(252, 248, 238), edge=INKC, k=1.0):
    if k <= 0: return
    ww, hh = int(w * k / 2), int(h * k / 2)
    cv2.rectangle(f, (int(x - ww + 8), int(y - hh + 10)), (int(x + ww + 8), int(y + hh + 10)), C((120, 100, 80)), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(col), -1, cv2.LINE_AA)
    cv2.rectangle(f, (int(x - ww), int(y - hh)), (int(x + ww), int(y + hh)), C(edge), 6, cv2.LINE_AA)


def crumbs(f, x, y, t, t0, n=12, spread=240, col=None, seed=3):
    if t < t0 or t > t0 + 0.9: return
    d = t - t0; rng = np.random.default_rng(seed); c = col or N_G
    for i in range(n):
        vx = rng.uniform(-spread, spread); vy = rng.uniform(-420, -120); xx = x + vx * d; yy = y + vy * d + 900 * d * d; r_ = int(rng.uniform(7, 15))
        cv2.circle(f, (int(xx), int(yy)), r_ + 3, C(INKC), -1, cv2.LINE_AA); cv2.circle(f, (int(xx), int(yy)), r_, C(c), -1, cv2.LINE_AA)


def SP(t):
    """camera ground position for the hook walk: 300 px/s, easing to a stop on 'soft'."""
    ts = T("i1", "soft") - 0.25
    return 300 * t if t < ts else 300 * ts + 300 * 0.35 * (1 - (1 - clamp((t - ts) / 0.35)) ** 2) / 2


# ---- S0: HOOK — a Diwali lane at dusk, parallax tracking shot: Chubby is already WALKING (frame 0), gift box under his arm, chakli held up; on 'soft' the chakli FLOPS, he stops dead, the take ----
def shot_S0(t, n):
    camx = SP(t); f = set_lane(t, camx + 300)
    ts = T("i1", "soft") - 0.25
    amt = 1 - ramp(t, ts, 0.3); tk = take(t, ts + 0.05)
    t3(f, "SOFT?", 780, t, ts + 0.05, 240)
    w = walk(t, 480, 1500, 1.08, speed=300, track=True, amt=amt)
    w.pop("ra"); w.pop("la"); lean = w.pop("lean"); turn = w.pop("turn"); look_ = w.pop("look"); hr = w.pop("hair")
    soft = ramp(t, ts, 0.18)
    wob = math.sin((t - ts) * 16) * 16 * math.exp(-(t - ts) * 2.5) if t > ts else 0
    hands = chub(f, w["x"], w["y"] + (tk["dy"] if t > ts else 0), 1.08, t=t, la=(30, 24), ra=(92 + 8 * math.sin(t * 5.8) * amt, 112), legs=w["legs"], bob=w["bob"], mouth=("jaw" if ts + 0.05 < t < ts + 0.8 else talk(t)), expr=tk["expr"] if t > ts else "happy", brow=tk["brow"] if t > ts else "up", look=(0.9, -0.3) if t < ts else (0.8, -0.2), lean=lean + (tk["lean"] if t > ts else 0), squash=tk["squash"] if t > ts else 0, turn=turn, hair=hr, hand_r="grip")
    hx, hy = hands[1]
    if t < ts + 0.8: comp(f, scale_el(chakli_el(None, soft), 0.72), hx + 40, hy - 80 + 40 * soft + wob * 0.5)
    else: comp(f, scale_el(chakli_el("sad", 1.0), 0.72), hx + 40, hy - 40)
    bx, by = hands[-1]; giftbox(f, bx - 30, by + 54, 0.42, ramp(t, T("i1", "open") - 0.05, 0.2), soft)
    lane_front(f, camx + 300)
    icap(f, "do you know why crispy namkeen", "goes [SOFT]", t, 0.1, acc=ACC_L, size=120, y=440, dark=True, out=ts + 0.05)
    if t >= T("i1", "second") - 0.15: icap(f, "the second you open", "the [BOX]?", t, T("i1", "second") - 0.15, acc=ACC_L, size=120, y=440, dark=True)
    return finish(f, n, look="warm")


# ---- S1: 'It isn't getting old' — the chakli on the table with an old man's stick; the idea gets crossed out ----
def shot_S1(t, n):
    f = set_droom(t); t0 = st_("S1"); to = T("i2", "getting") - 0.05
    t3(f, "OLD?", 760, t, t0 + 0.05, 240)
    chub(f, 250, 1500, 1.0, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="sus", brow="sus", look=(1, 0), lean=-3)
    table_front(f, TOP)
    comp(f, scale_el(chakli_el("sad", 0.3), 1.0), 700, 1160)
    cv2.line(f, (830, 1110), (870, 1320), C(INKC), 16, cv2.LINE_AA); cv2.line(f, (830, 1110), (870, 1320), C((150, 100, 60)), 9, cv2.LINE_AA)
    k = ramp(t, to + 0.2, 0.15)
    if k > 0: cv2.line(f, (200, 830), (int(200 + 680 * k), 690), C(RED_I), 22, cv2.LINE_AA)
    return finish(f, n, look="warm")


# ---- S1b: 'it's drinking the air in your kitchen' — the chakli has a STRAW; drops fly out of the air into it; Chubby double-takes ----
def shot_S1b(t, n):
    f = set_droom(t); t0 = st_("S1b"); td = T("i2", "drinking") - 0.1
    t3(f, "DRINKING", 760, t, td, 190)
    dt_ = double_take(t, td)
    chub(f, 210, 1500, 0.92, t=t, **nolean(POSE["shock"]), mouth=talk(t), expr=dt_[2], brow=dt_[3], look=(1, -0.3), lean=dt_[1], turn=0.5)
    table_front(f, TOP)
    gulp_ = 1 + 0.05 * math.sin(t * 15)
    comp(f, scale_el(chakli_el("hungry", 0.35, (0, -1)), 1.05), 660, 1140, scale=gulp_)
    rot_comp(f, scale_el(straw_el(), 1.0), 720, 900, -8, 1.0, 1.0, 0)
    if t >= td:
        fly_drops(f, (140, 620), (760, 760), t, 8, 0.8, 3, 0.3, -60); fly_drops(f, (1000, 560), (760, 760), t, 7, 0.9, 5, 0.3, -40); fly_drops(f, (560, 340), (760, 760), t, 5, 0.75, 7, 0.26, 20)
    comp(f, bchip("OUT OF THE AIR", 36), 780, 1420, scale=pin(t, T("i2", "air") - 0.1))
    return finish(f, n, look="warm")


# ---- S2: 'And that's the exact opposite of your bread' — two cards: bread HARD, namkeen SOFT ----
def shot_S2(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 480); to = T("i3", "opposite") - 0.1; tb = T("i3", "bread") - 0.15
    t3(f, "OPPOSITE", 610, t, to, 170)
    card(f, 290, 1050, 400, 500, k=pin(t, st_("S2") + 0.1)); card(f, 790, 1050, 400, 500, k=pin(t, st_("S2") + 0.1))
    comp(f, scale_el(chakli_el("sad", 1.0), 0.85), 290, 1040, scale=pin(t, st_("S2") + 0.15))
    comp(f, achip("GOES SOFT", 36), 290, 1250, scale=pin(t, st_("S2") + 0.25))
    if t >= tb:
        comp(f, scale_el(bread_slice_el(1.0, "angry"), 0.9), 790, 1030, scale=pin(t, tb))
        comp(f, ichip("GOES HARD", 36), 790, 1250, scale=pin(t, tb + 0.1))
    if t < tb: comp(f, chip("?", ACC_S, MILK, 90), 790, 1040, scale=pin(t, st_("S2") + 0.15))
    comp(f, chip("SAME KITCHEN", INKC, MILK, 34), 540, 1370, scale=pin(t, T("i3", "same") - 0.1))
    return finish(f, n, look="warm")


# ---- S3: 'A fresh chakli has been fried until there's almost no water left in it' — a kadai on the flames, water leaving the chakli as steam ----
def shot_S3(t, n):
    f = set_stove(t, on=0.9, flame_w=420); f = inkify(f, 0.08); t0 = st_("S3")
    tf = T("a1", "fried") - 0.15; ta = T("a1", "almost") - 0.1
    chub(f, 190, 1500, 0.86, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, 0.3), hand_r="point", turn=0.5)
    comp(f, scale_el(kadai_el(), 1.0), 620, 1160)
    k = ramp(t, tf, ta - tf + 0.5)
    comp(f, scale_el(chakli_el(None, 0), 0.72), 620, 1120 + 8 * math.sin(t * 5))
    rising_bubbles_x = [(450, 0.0), (530, 0.3), (720, 0.15), (790, 0.5), (620, 0.7)]
    for x_, ph in rising_bubbles_x:
        p = (t * 1.8 + ph) % 1; yy = 1230 - 90 * p; cv2.circle(f, (x_, int(yy)), 12, C(INKC), 3, cv2.LINE_AA)
    if t >= tf: fly_drops(f, (620, 1060), (640, 560), t, max(5, int(11 * (1 - k * 0.5))), 1.0, 4, 0.3, 0)
    comp(f, chip("WATER LEAVES", WATER_S, MILK, 30), 830, 760, scale=pin(t, tf + 0.1))
    icap(f, "fried until almost", "[NO WATER]", t, t0 + 0.2, size=130, y=440, acc=ACC_S, dark=False)
    return finish(f, n, look="warm")


# ---- S4: 'That's the crunch.' — a big bite, CRUNCH, crumbs ----
def shot_S4(t, n):
    f = set_droom(t); tb = T("a2", "crunch") - 0.2; tk = flinch(t, tb)
    t3(f, "CRUNCH", 760, t, tb, 230)
    bit = t > tb
    chub(f, 480, 1540, 1.25, t=t, la=(30, 14), ra=(148, -130), mouth=2 if bit and int(t * 12) % 2 else (talk(t) if not bit else 1), expr="happy" if bit else "n", brow="up", look=(0.4, 0), hold=scale_el(chakli_el(None, 0), 0.5), hold_off=(26, -30), hold_front=True, lean=tk[0], squash=tk[1])
    crumbs(f, 590, 1010, t, tb, 16)
    if tb <= t < tb + 0.5: comp(f, burst_el("KRRK!", ACC_L, INKC, 64), 860, 980, scale=pin(t, tb, 0.08))
    table_front(f, TOP + 60)
    return finish(f, n, look="warm")


# ---- S4b: 'It's also the problem, because now it's thirsty' — the desert: chakli with its tongue out ----
def shot_S4b(t, n):
    f = ink_set("dryp", (255, 240, 180), 800, 690, 170); tt = T("a2", "thirsty") - 0.1; t0 = st_("S4b")
    cv2.rectangle(f, (0, 1330), (W, H), C((226, 186, 120)), -1); cv2.line(f, (0, 1330), (W, 1330), C(INKC), 7, cv2.LINE_AA)
    for (x0, y0) in ((120, 1370), (420, 1410), (720, 1360), (900, 1430), (260, 1450)):
        P = [(x0 + j * 34, y0 + (j % 2) * 24) for j in range(6)]; cv2.polylines(f, [np.array(P, np.int32)], False, C(INKC), 4, cv2.LINE_AA)
    t3(f, "THIRSTY", 760, t, tt, 220)
    comp(f, scale_el(chakli_el("hungry" if t > tt else "sad", 0), 1.15), 540, 1140 + 8 * math.sin(t * 3))
    if t < tt: icap(f, "it's also the", "[PROBLEM]", t, t0 + 0.05, size=150, y=440)
    return finish(f, n, look="golden")


# ---- S5: 'Your kitchen air is full of water. You just can't see it.' — Chubby sweeps a magnifier through the air: drops only show through the lens ----
def shot_S5(t, n):
    f = set_droom(t); tf = T("a3", "full") - 0.12; tc = T("a3", "cant") - 0.1
    hs5 = chub(f, 240, 1500, 1.0, t=t, la=(30, 14), ra=(100, 110), mouth=talk(t), expr="sus" if t < tf else "wow", brow="sus" if t < tf else "up", look=(1, -0.5), hand_r="grip", turn=0.5)
    table_front(f, TOP)
    a = (t - st_("S5")) * 1.1; lx = 660 + 210 * math.cos(a); ly = 840 + 200 * math.sin(a * 1.3)     # the lens moves on an arc
    g = f.copy(); rng = np.random.default_rng(9); el = scale_el(drop_el("happy"), 0.32)
    for i in range(34):
        x_, y_ = rng.uniform(40, 1040), rng.uniform(300, 1320); x_ += 18 * math.sin(t * 0.8 + i); y_ += 14 * math.cos(t * 0.7 + i * 2); comp(g, el, x_, y_)
    allk = ramp(t, tf, 0.2) * (1 - ramp(t, tc, 0.35)); yy, xx = np.ogrid[:H, :W]; m = ((xx - lx) ** 2 + (yy - ly) ** 2 < 170 ** 2).astype(np.float32)
    m = np.maximum(m, allk)[..., None]; f[:] = f * (1 - m) + g * m
    cv2.circle(f, (int(lx), int(ly)), 170, C(INKC), 15, cv2.LINE_AA); cv2.circle(f, (int(lx), int(ly)), 160, C((226, 200, 120)), 7, cv2.LINE_AA)
    hx5, hy5 = hs5[1]; ang5 = math.atan2(hy5 - ly, hx5 - lx); ex5 = (int(lx + 170 * math.cos(ang5)), int(ly + 170 * math.sin(ang5)))
    cv2.line(f, ex5, (int(hx5), int(hy5)), C(INKC), 26, cv2.LINE_AA); cv2.line(f, ex5, (int(hx5), int(hy5)), C((150, 100, 60)), 16, cv2.LINE_AA); grip_hand(f, hx5, hy5, 1.0)
    if t < tc: icap(f, "the air is", "[FULL] of water", t, tf, size=110, y=440, acc=WATER_S)
    else: icap(f, "you just can't", "[SEE IT]", t, tc, size=140, y=440, acc=WATER_S)
    return finish(f, n, look="warm")


# ---- S6: 'water moves from where there's more to where there's less, until both sides even out' — two tanks and a pipe ----
def shot_S6(t, n):
    f = ink_set("wetp", (255, 255, 255), 540, 1000, 500); tm = T("a4", "more") - 0.1; tl = T("a4", "less") - 0.1; te = T("a4", "even") - 0.1
    k = ramp(t, T("a4", "moves") - 0.05, te - T("a4", "moves") + 0.3)
    xa, xb, y0 = tank_pair(f, t, k, 540, 1020)
    if t >= tm: comp(f, chip("MORE", WATER_S, MILK, 44), xa, y0 - 50, scale=pin(t, tm))
    if t >= tl: comp(f, chip("LESS", N_S, MILK, 44), xb, y0 - 50, scale=pin(t, tl))
    if t >= te: comp(f, chip("EVEN", INKC, MILK, 44), 540, 1330, scale=pin(t, te))
    icap(f, "water has", "[ONE HABIT]", t, st_("S6") + 0.1, size=130, y=440, acc=WATER_S)
    return finish(f, n, look="fresh")


# ---- S7: 'Food scientists even measure this, on a thirst meter from zero to one' — Chubby WALKS onto the plank ----
def shot_S7(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); t0 = st_("S7"); tm = T("b1", "meter") - 0.1
    X = thirst_meter(f, t, labels=t > T("b1", "from") - 0.1)
    t3(f, "THIRST METER", 660, t, tm, 120)
    stop = t0 + 2.2; wk = min(t, stop); amt = 1 - ramp(t, stop - 0.25, 0.25)
    w = walk(t, -60 + 280 * max(0.0, min(t - t0, stop - t0)), 1270, 0.82, speed=280, t0=t0, amt=amt, track=True)
    if t >= stop - 0.25: w["look"] = (0, -0.1)
    chub(f, s=0.82, t=t, mouth=talk(t), expr="happy", brow="up", **w)
    comp(f, chip("REAL NAME: WATER ACTIVITY", INKC, MILK, 30), 540, 1440, scale=pin(t, T("b1", "zero") - 0.1))
    icap(f, "food scientists even", "[MEASURE] this", t, t0 + 0.2, size=100, y=440)
    return finish(f, n, look="warm")


# ---- S7b: 'The lower the number, the thirstier it is.' ----
def shot_S7b(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); tt = T("b1", "thirstier") - 0.12
    X = thirst_meter(f, t)
    chub(f, 556, 1270, 0.82, t=t, **nolean({**POSE["point"], "la": POSE["point"]["ra"], "ra": POSE["point"]["la"]}), mouth=talk(t), expr="n", brow="up", look=(-1, 0.2), hand_l="point", turn=-0.5, lean=-3)
    if t >= T("b1", "lower") - 0.1: draw_arrow(f, 420, 1200, 170, 1200, ramp(t, T("b1", "lower") - 0.1, 0.4), ACC_S, 14, 44)
    if t >= tt: comp(f, scale_el(chakli_el("hungry", 0), 0.62), X(0.1), 1040, scale=pin(t, tt)); comp(f, achip("THIRSTIER", 36), X(0.2), 860, scale=pin(t, tt))
    icap(f, "lower number =", "[THIRSTIER]", t, st_("S7b") + 0.1, size=120, y=440)
    return finish(f, n, look="warm")


# ---- S8: 'A cracker sits around zero point three. Humid air sits around zero point seven.' — he walks from one flag to the other ----
def flag(f, x, y, el, txt, col, k=1.0, h=270):
    cv2.line(f, (int(x), int(y)), (int(x), int(y - h * k)), C(INKC), 7, cv2.LINE_AA)
    comp(f, el, x, y - h - 90, scale=k); comp(f, chip(txt, col, MILK, 36), x, y - h + 4, scale=k)


def shot_S8(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); X = thirst_meter(f, t)
    t3_ = T("b2", "three") - 0.25; tH = T("b2", "Humid") - 0.05; t7 = T("b2", "seven") - 0.2
    if t >= t3_: flag(f, X(0.3), 1270, scale_el(cracker_el("hungry"), 0.72), "0.3", ACC_S, pin(t, t3_))
    if t >= T("b2", "air") - 0.3: flag(f, X(0.7), 1270, scale_el(cloud_el("happy"), 0.62), "0.7", WATER_S, pin(t, T("b2", "air") - 0.3))
    dur_ = max(0.5, min(1.5, en_("S8") - tH - 0.2)); k_ = clamp((t - tH) / dur_); xw = X(0.1) + (X(0.5) - X(0.1)) * k_; am_ = 1.0 if 0 < k_ < 0.85 else (0.0 if k_ <= 0 else 1 - clamp((k_ - 0.85) / 0.15))
    wk_ = walk(t, xw, 1270, 0.82, speed=(X(0.5) - X(0.1)) / dur_, t0=tH, amt=am_, track=True); wk_.pop("la"); wk_.pop("ra")
    if k_ <= 0: chub(f, s=0.82, t=t, la=(20, 10), ra=(72, 42), mouth=talk(t), expr="n", brow="up", hand_r="point", **wk_)
    else: chub(f, s=0.82, t=t, la=(28, 14), ra=(40, 30), mouth=talk(t), expr="happy", brow="up", **wk_)
    icap(f, "cracker", "[0.3]", t, t3_, size=140, y=440, acc=ACC_S, out=t7)
    if t >= t7: icap(f, "humid air", "[0.7]", t, t7, size=140, y=440, acc=WATER_S)
    return finish(f, n, look="warm")


# ---- S9: 'So the moment that lid comes off, the water only goes one way.' — the gift box, lid lifts; drops rush in ----
def shot_S9(t, n):
    f = set_droom(t); tl = T("b3", "lid") - 0.1; to = T("b3", "one") - 0.1
    t3(f, "ONE WAY", 700, t, to, 190)
    chub(f, 190, 1500, 0.88, t=t, **nolean(POSE["whisper"]), mouth=talk(t), expr="wow" if t > tl else "n", brow="up", look=(1, -0.2), turn=0.5)
    table_front(f, TOP)
    lk = ramp(t, tl, 0.3); giftbox(f, 640, 1340, 0.86, lk, ramp(t, to, 1.0) * 0.7)
    if lk > 0.6:
        fly_drops(f, (100, 480), (620, 1060), t, 9, 0.9, 3, 0.3, -30); fly_drops(f, (1020, 400), (660, 1060), t, 9, 1.0, 5, 0.3, 40); fly_drops(f, (640, 330), (640, 1060), t, 6, 1.1, 8, 0.26, 0)
    icap(f, "the moment that", "[LID] comes off", t, st_("S9") + 0.1, size=110, y=440, out=to)
    return finish(f, n, look="warm")


# ---- S10: 'Bread's already full of water, so it isn't thirsty. Your namkeen is.' — the cloud offers a drop: the loaf says no thanks, the chakli gulps ----
def shot_S10(t, n):
    f = ink_set("wetp", (255, 255, 255), 540, 1000, 500); tn = T("b4", "Your") - 0.12
    comp(f, scale_el(cloud_el("happy"), 0.9), 540, 740 + 8 * math.sin(t * 2))
    k = pin(t, st_("S10") + 0.1); comp(f, scale_el(loaf_el(0, "happy"), 0.82), 280, 1180, scale=k); comp(f, chip("0.95  FULL", WATER_S, MILK, 34), 280, 1370, scale=k)
    p = ((t - st_("S10")) * 1.1) % 1
    if t < tn: comp(f, scale_el(drop_el("sad"), 0.34), 480 - 220 * p, 800 + 170 * p - 400 * p * (1 - p) * (1 if p < 0.8 else 0))
    if t >= tn - 0.2:
        comp(f, scale_el(chakli_el("hungry", 0.2), 0.9), 800, 1160, scale=pin(t, tn - 0.2) * (1 + 0.05 * math.sin(t * 16))); comp(f, chip("0.3  THIRSTY", ACC_S, MILK, 34), 800, 1370, scale=pin(t, tn))
        fly_drops(f, (620, 780), (800, 1060), t, 9, 1.2, 3, 0.3, -30)
    else: comp(f, ichip("NO THANKS", 28), 280, 1000, scale=pin(t, T("b4", "isnt") - 0.1))
    icap(f, "bread isn't", "[THIRSTY]", t, st_("S10") + 0.15, size=120, y=440, acc=WATER_S, out=tn)
    if t >= tn: icap(f, "your namkeen", "[IS]", t, tn, size=140, y=440)
    src(f, SRC_G, t, st_("S10") + 0.3, 1450)
    return finish(f, n, look="fresh")


# ---- S11: 'So why would a tiny bit of water kill the crunch? Picture this.' — one drop falls, a lights-drop; R.I.P. CRUNCH ----
def shot_S11(t, n):
    f = set_droom(t, dim=0.35); t0 = st_("S11"); tk_ = T("c1", "kill") - 0.1
    spotlight(f, 540, 1150, 330, 0.5)
    t3(f, "KILL?", 720, t, tk_, 210)
    comp(f, scale_el(chakli_el("wow", 0.1 * (t > tk_)), 1.0), 540, 1180)
    table_front(f, TOP + 60)
    ydrop = drop_land(t, t0 + 0.2, 300, 1030, 0.6)[0] if t0 + 0.2 <= t < tk_ + 0.2 else None
    if ydrop is not None: comp(f, scale_el(drop_el("angry"), 0.6), 540, ydrop)
    if t >= T("c1", "Picture") - 0.1: comp(f, chip("PICTURE THIS", INKC, MILK, 40), 540, 1420, scale=pin(t, T("c1", "Picture") - 0.1))
    icap(f, "one tiny bit of", "[WATER]?", t, t0 + 0.1, size=130, y=440, dark=True, acc=(150, 210, 250), out=tk_ + 0.8)
    return finish(f, n, look="night")


# ---- S12: 'Dry spaghetti snaps.' — he holds a dry bundle in both hands; SNAP ----
def shot_S12(t, n):
    f = ink_set("dryp", (255, 240, 180), 540, 980, 460); ts = T("c2", "snaps") - 0.12; k = ramp(t, st_("S12"), ts - st_("S12")); sn = t >= ts; d = t - ts
    tk = take(t, ts)
    hs = chub(f, 540, 1500 + (tk["dy"] if sn else 0), 1.05, t=t, la=(92, 60), ra=(92, 60), mouth=talk(t) if not sn else "jaw", expr=tk["expr"] if sn else "n", brow="up", look=(0, -0.3), squash=tk["squash"] if sn else 0)
    xl, yl = hs[-1]; xr, yr = hs[1]
    for j in range(5):
        dy_ = -44 + j * 22
        if not sn:
            P = [(xl + (xr - xl) * q / 8, yl + dy_ - 42 * k * math.sin(q / 8 * 3.14)) for q in range(9)]; strand(f, P, 10)
        else:
            mid = (xl + xr) / 2; yy0 = yl + dy_
            strand(f, [(xl, yy0), (mid - 8 - 40 * eo(clamp(d / 0.2)), yy0 - 60 * eo(clamp(d / 0.2)))], 10); strand(f, [(xr, yy0), (mid + 8 + 40 * eo(clamp(d / 0.2)), yy0 - 60 * eo(clamp(d / 0.2)))], 10)
    crumbs(f, 540, yl - 30, t, ts, 14, 300, (244, 214, 120))
    if sn and d < 0.55: comp(f, burst_el("SNAP!", ACC_L, INKC, 66), 540, 660, scale=pin(t, ts, 0.08))
    icap(f, "dry spaghetti", "", t, st_("S12") + 0.05, size=100, y=440)
    return finish(f, n, look="golden")


# ---- S12b: 'Cooked spaghetti bends.' — limp strands hanging from his hand, wobbling ----
def shot_S12b(t, n):
    f = ink_set("wetp", (255, 255, 255), 540, 980, 460); tb = T("c2", "bends") - 0.1
    hs = chub(f, 420, 1500, 1.05, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="smirk", brow="up", look=(0.8, -0.2), hand_r="pinch", turn=0.5)
    hx, hy = hs[1]
    for j in range(5):
        P = [(hx + (j - 2) * 12 + 90 * (q / 16) * math.sin(q * 0.5 + t * 4 + j), hy + q * 34) for q in range(17)]
        strand(f, P, 10, (240, 226, 170))
    t3(f, "BENDS", 700, t, tb, 180, (190, 224, 250), WATER_S, x=600)
    icap(f, "cooked spaghetti", "", t, st_("S12b") + 0.05, size=100, y=440)
    return finish(f, n, look="fresh")


# ---- S12c: 'It's the same starch, and the only difference is water.' — side by side + one blue drop ----
def shot_S12c(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 480); ts = T("c2", "starch") - 0.1; tw = T("c2", "water") - 0.12
    card(f, 290, 1040, 400, 480); card(f, 790, 1040, 400, 480)
    for j in range(4): strand(f, [(150 + j * 8, 900 + j * 44), (430 + j * 4, 880 + j * 44)], 11)
    for j in range(4):
        P = [(660 + q * 20, 900 + j * 56 + 28 * math.sin(q * 0.8 + t * 3 + j)) for q in range(14)]; strand(f, P, 11, (240, 226, 170))
    if t >= ts: comp(f, chip("SAME STARCH", INKC, MILK, 40), 540, 690, scale=pin(t, ts))
    comp(f, ichip("DRY", 34), 290, 1210); comp(f, bchip("+ WATER", 34), 790, 1210)
    if t >= tw:
        comp(f, scale_el(drop_el("wow"), 1.1 * pin(t, tw)), 540, 1040); t3(f, "ONLY WATER", 1340, t, tw, 120, (190, 224, 250), WATER_S)
    return finish(f, n, look="warm")


# ---- S13: 'Your namkeen's the same. Dry, its starch is brittle' — lens into the chakli: the starch as stiff rows ----
def shot_S13(t, n):
    f = ink_set("dryp", (255, 240, 180), 540, 1000, 500); tb = T("c3", "brittle") - 0.1; t0 = st_("S13")
    comp(f, scale_el(chakli_el(None, 0), 0.62), 200, 700, scale=pin(t, t0))
    k = pin(t, t0 + 0.5); glass_rubber(f, 540, 1090, 0.0, t, 700, 340, shake=4.0 * (t > tb and t < tb + 0.5))
    cv2.line(f, (280, 780), (300, 900), C(INKC), 6, cv2.LINE_AA)
    comp(f, achip("STARCH, UP CLOSE", 30), 620, 690)
    icap(f, "dry, it's", "[BRITTLE]", t, tb - 0.2, size=150, y=440)
    src(f, SRC_W, t, tb, 1320)
    return finish(f, n, look="golden")


# ---- S13b: 'like glass, and scientists really do call that glassy.' — a pane of glass cracks; GLASSY ----
def shot_S13b(t, n):
    f = ink_set("wetp", (255, 255, 255), 540, 1000, 500); tg = T("c3", "glassy") - 0.12; t0 = st_("S13b")
    x0, y0, x1, y1 = 330, 760, 960, 1340
    ov = f.copy(); cv2.rectangle(ov, (x0, y0), (x1, y1), C((214, 238, 250)), -1, cv2.LINE_AA); f[:] = f * 0.55 + ov * 0.45; cv2.rectangle(f, (x0, y0), (x1, y1), C(INKC), 9, cv2.LINE_AA)
    cv2.line(f, (x0 + 60, y0 + 60), (x0 + 20, y0 + 220), C((255, 255, 255)), 8, cv2.LINE_AA)
    kc = ramp(t, t0 + 0.12, 0.2)
    for a in (10, 62, 120, 170, 225, 290, 340):
        P = [(640, 1050)]; aa = math.radians(a)
        for j in range(1, 5): r_ = 70 * j * kc; P.append((640 + r_ * math.cos(aa) + 12 * (-1) ** j * math.sin(aa), 1050 + r_ * math.sin(aa) + 12 * (-1) ** j * math.cos(aa)))
        cv2.polylines(f, [np.array(P, np.int32)], False, C(INKC), 5, cv2.LINE_AA)
    t3(f, "GLASSY", 650, t, tg, 230, (190, 224, 250), WATER_S)
    chub(f, 180, 1500, 0.88, t=t, **nolean(POSE["cheek"]), mouth=talk(t), expr="smirk", brow="up", look=(1, -0.1), turn=0.5)
    icap(f, "brittle, like", "[GLASS]", t, t0 + 0.05, size=140, y=440, acc=WATER_S, out=tg)
    return finish(f, n, look="fresh")


# ---- S14: 'A little water slips in between the starch molecules and loosens them up.' — the same diagram, it loosens ----
def shot_S14(t, n):
    f = ink_set("wetp", (255, 255, 255), 540, 1000, 500); ts = T("c4", "slips") - 0.1; tl = T("c4", "loosens") - 0.1
    k = ramp(t, ts, tl - ts + 0.6)
    glass_rubber(f, 540, 1060, k, t, 700, 460)
    if k < 0.9: fly_drops(f, (140, 640), (420, 860), t, 5, 1.0, 3, 0.28, 0); fly_drops(f, (940, 640), (660, 860), t, 5, 1.1, 5, 0.28, 0)
    icap(f, "water", "[SLIPS IN]", t, ts - 0.1, size=140, y=440, acc=WATER_S, out=tl)
    if t >= tl: icap(f, "and", "[LOOSENS] it", t, tl, size=130, y=440, acc=WATER_S)
    comp(f, ichip("STARCH + WATER", 28), 540, 1400)
    return finish(f, n, look="fresh")


# ---- S14b: 'Now it's rubbery.' — the chakli stretches like a rubber toy between his hands ----
def shot_S14b(t, n):
    f = set_droom(t); tr = T("c4", "rubbery") - 0.15
    t3(f, "RUBBERY", 720, t, tr, 200)
    ex = 0.5 + 0.5 * math.sin((t - tr) * 9)
    chub(f, 540, 1500, 1.05, t=t, la=(70, 64 + 16 * ex), ra=(70, 64 + 16 * ex), mouth=talk(t), expr="wow", brow="up", look=(0, 0.2))
    comp(f, scale_xy(scale_el(chakli_el(None, 0.8), 0.92), 1.0 + 0.32 * ex, 1.0 - 0.14 * ex), 540, 1120)
    table_front(f, TOP + 70)
    return finish(f, n, look="warm")


# ---- S15: 'And a snack that bends can't snap. No snap, no crunch.' — he tries; nothing; sad bite ----
def shot_S15(t, n):
    f = set_droom(t); tb = T("c5", "bends") - 0.1; tn = T("c5", "No") - 0.1; tc = T("c5", "crunch") - 0.12
    ben = ramp(t, tb, 0.5)
    chub(f, 540, 1500, 1.08, t=t, la=(88, 70 - 30 * ben), ra=(88, 70 - 30 * ben), mouth=talk(t), expr="sad" if t > tn else "sus", brow="sad" if t > tn else "sus", look=(0, 0.5))
    rot_comp(f, scale_el(chakli_el("sad", 1.0), 0.72), 540, 1080 + 70 * ben, 0, 1.0)
    table_front(f, TOP + 70)
    if t >= tn: slam(f, stamp_el("NO SNAP", RED_I, 56), 300, 780, 7, t, tn)
    if t >= tc: slam(f, stamp_el("NO CRUNCH", RED_I, 64), 700, 700, -6, t, tc)
    icap(f, "a snack that", "[BENDS]", t, st_("S15") + 0.1, size=130, y=440, out=tn)
    return finish(f, n, look="warm")


# ---- S16: 'And it barely takes anything.' — he looks at a single tiny drop on the plank; S16b: the classic study — the red danger band spreads ----
def shot_S16(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); X = thirst_meter(f, t)
    chub(f, X(0.3), 1270, 0.72, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="n", brow="up", look=(0.6, 0.3))
    comp(f, scale_el(drop_el("happy"), 0.3), X(0.42), 1234, scale=pin(t, T("d1", "barely") - 0.1))
    icap(f, "it", "[BARELY] takes anything", t, st_("S16") + 0.1, size=100, y=440, acc=WATER_S)
    return finish(f, n, look="warm")


def shot_S16b(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); tb = T("d1", "rejected") - 0.1
    X = thirst_meter(f, t, band=ramp(t, T("d1", "zero") - 0.1, 1.6))
    flag(f, X(0.3), 1270, scale_el(cracker_el("n"), 0.6), "0.3", ACC_S, 1.0, 130)
    k = ramp(t, T("d1", "zero") - 0.1, 1.6)
    if k > 0.02: comp(f, chip("0.35 - 0.5", RED_I, MILK, 44), (X(0.35) + X(0.5)) / 2 + 50, 1040, scale=pin(t, T("d1", "zero") - 0.1))
    if t >= tb: slam(f, stamp_el("REJECTED", RED_I, 74), 620, 800, -6, t, tb)
    comp(f, scale_el(sev_el(0), 0.7), 840, 1180, scale=pin(t, st_("S16b") + 0.1)); comp(f, ichip("CHIPS + CRACKERS", 28), 830, 1060, scale=pin(t, st_("S16b") + 0.1))
    icap(f, "in the classic", "[STUDY]", t, st_("S16b") + 0.05, size=120, y=440, out=tb)
    src(f, SRC_K, t, st_("S16b") + 0.2, 1450)
    return finish(f, n, look="warm")


# ---- S17: 'A cracker starts at zero point three. That's only a couple of steps away.' — close on the plank: he literally walks it in TWO STEPS, the chakli flops ----
def shot_S17(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480); ts = T("d2", "only") - 0.05; ta = T("d2", "away") + 0.15
    x_a, x_b = 300, 800; X = lambda v: x_a + (v - 0.3) * (x_b - x_a) / 0.2
    y = 1280; n_ = 30
    for i in range(n_):
        v = 0.2 + 0.5 * i / n_; c = _mix22((240, 198, 120), WATER, v); cv2.rectangle(f, (int(X(v)), y), (int(X(v + 0.5 / n_)) + 1, y + 70), C(c), -1)
    ov = f.copy(); cv2.rectangle(ov, (int(X(0.35)), y - 8), (int(X(0.5)), y + 78), C((206, 50, 60)), -1, cv2.LINE_AA); f[:] = f * 0.3 + ov * 0.7
    cv2.line(f, (0, y), (W, y), C(INKC), 7, cv2.LINE_AA); cv2.line(f, (0, y + 70), (W, y + 70), C(INKC), 7, cv2.LINE_AA)
    for v, txt, c in ((0.3, "0.3", INKC), (0.5, "0.5", RED_I)):
        cv2.line(f, (int(X(v)), y + 70), (int(X(v)), y + 100), C(INKC), 6, cv2.LINE_AA); comp(f, chip(txt, c, MILK, 34), X(v), y + 130)
    comp(f, chip("REJECTED ZONE", RED_I, MILK, 30), (X(0.35) + X(0.5)) / 2, y + 36)
    per = 1.08; walk_d = per; kk = clamp((t - ts) / walk_d); stopk = 1 - ramp(t, ts + walk_d - 0.12, 0.12) if t > ts else 0.0
    tk = t if t < ts + walk_d else ts + walk_d
    wx_ = X(0.3) - 30 + (x_b - 150 - X(0.3)) * kk
    w = walk(tk, wx_, y, 1.0, speed=(x_b - 120 - X(0.3)) / walk_d, t0=ts, amt=stopk, period=per, track=True)
    w.pop("la"); w.pop("ra")
    soft = ramp(t, ts + 0.3, 0.7)
    hs = chub(f, s=1.0, t=t, la=(30, 14), ra=(120, 150), mouth=talk(t) if t < ta else "jaw", expr="n" if kk < 1 else "wow", brow="up", hand_r="grip", **w)
    comp(f, scale_el(chakli_el("wow" if kk >= 1 else None, soft), 0.62), hs[1][0] + 40, hs[1][1] - 60)
    if t >= ts + 0.5: comp(f, chip("1 STEP", INKC, MILK, 40), 300, 640, scale=pin(t, ts + 0.5))
    if t >= ts + 1.05: comp(f, chip("2 STEPS", RED_I, MILK, 52), 760, 640, scale=pin(t, ts + 1.05))
    icap(f, "only a couple of", "[STEPS]", t, T("d2", "Thats") - 0.1, size=140, y=440)
    return finish(f, n, look="warm")


# ---- S18: 'But the real trap is your Diwali gift box.' — lights drop, spotlight, the box glows innocently ----
def shot_S18(t, n):
    f = set_droom(t, dim=0.42); tt = T("e1", "trap") - 0.1; tD = T("e1", "Diwali") - 0.1
    spotlight(f, 540, 1130, 360, 0.5)
    t3(f, "TRAP", 660, t, tt, 260)
    giftbox(f, 540, 1340, 0.98, 0.0)
    table_front(f, TOP + 10)
    sparkles(f, 540, 1000, t, tD, 10, 260, (255, 214, 120))
    if t >= tD: f = crash_zoom(f, t, tD, 1.06, 540, 950)
    return finish(f, n, look="night")


# ---- S19: 'Crispy namkeen, tucked right next to soft barfi, and barfi sits around zero point eight.' — top view of the box, the two neighbours ----
def shot_S19(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); tb = T("e2", "barfi") - 0.12; te = T("e2", "zero") - 0.1
    (lx, ly), (rx, ry) = gift_top(f, 540, 1000, 880, 500, moods=("happy", "happy"))
    comp(f, achip("CRISPY: 0.3", 36), lx, 680, scale=pin(t, st_("S19") + 0.2))
    if t >= tb: comp(f, chip("SOFT", WATER_S, MILK, 36), rx, 680, scale=pin(t, tb))
    if t >= te: comp(f, chip("SOFT: 0.8", WATER_S, MILK, 38), rx, 680, scale=pin(t, te, 0.2))
    icap(f, "tucked right", "[NEXT DOOR]", t, st_("S19") + 0.1, size=130, y=440)
    src(f, SRC_B, t, te, 1330)
    return finish(f, n, look="warm")


# ---- S20: 'Bakers know this from cookies: store soft ones with crisp ones' / S20b: 'and the crisp go soft while the soft dry out' ----
def shot_S20(t, n):
    f = ink_set("dryp", (255, 240, 180), 540, 1000, 500); tb = T("e3", "soft") - 0.1
    comp(f, scale_el(jar_ink_el(1.0, "none"), 1.3), 540, 1040, scale=pin(t, st_("S20")))
    comp(f, scale_el(cookie_el("crisp", "happy"), 0.8), 450, 1120, scale=pin(t, T("e3", "crisp") - 0.12))
    comp(f, scale_el(cookie_el("soft", "happy"), 0.8), 640, 1140, scale=pin(t, tb))
    icap(f, "bakers know this", "[COOKIES]", t, st_("S20") + 0.1, size=130, y=440)
    src(f, SRC_C, t, st_("S20") + 0.3, 1450)
    return finish(f, n, look="golden")


def shot_S20b(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); tc = T("e3", "soft", 1) - 0.1; td = T("e3", "dry") - 0.1; t0 = st_("S20b")
    k1 = ramp(t, t0, tc - t0 + 0.5); k2 = ramp(t, td - 0.2, 0.6)
    card(f, 290, 1040, 420, 520); card(f, 790, 1040, 420, 520)
    comp(f, scale_el(cookie_el("crisp", "sad" if k1 > 0.5 else "happy", k1), 1.2), 290, 1030); comp(f, scale_el(cookie_el("soft", "sad" if k2 > 0.5 else "happy", k2), 1.2), 790, 1030)
    fly_drops(f, (700, 960), (380, 960), t, 7, 0.9, 3, 0.3, -100)
    if t >= tc: comp(f, achip("CRISP GOES SOFT", 30), 290, 1250, scale=pin(t, tc))
    if t >= td: comp(f, chip("SOFT DRIES OUT", N_S, MILK, 30), 790, 1250, scale=pin(t, td))
    return finish(f, n, look="warm")


# ---- S21: 'Your gift box does the same thing, and a closed lid can't save it.' — drops cross the divider, the lid slides shut over it all ----
def shot_S21(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); ts = T("e4", "same") - 0.1; tc = T("e4", "closed") - 0.1; t0 = st_("S21")
    k = ramp(t, t0, tc - t0 + 0.4)
    (lx, ly), (rx, ry) = gift_top(f, 540, 1000, 880, 500, k, k, moods=("sad" if k > 0.4 else "happy", "sad" if k > 0.4 else "happy"))
    fly_drops(f, (rx, 980), (lx, 980), t, 9, 1.0, 3, 0.3, -150)
    if t >= tc:
        lk = ramp(t, tc, 0.35); xx = int(-900 + (980 - -900) * eo(lk)); ww = 930
        cv2.rectangle(f, (xx - ww + 18, 736), (xx + 18, 1270), C((120, 80, 80)), -1, cv2.LINE_AA); cv2.rectangle(f, (xx - ww, 722), (xx, 1256), C(ACC), -1, cv2.LINE_AA); cv2.rectangle(f, (xx - ww, 722), (xx, 1256), C(INKC), 9, cv2.LINE_AA)
        cv2.rectangle(f, (xx - 60 - ww // 2, 722), (xx + 60 - ww // 2, 1256), C((248, 206, 110)), -1, cv2.LINE_AA); cv2.rectangle(f, (xx - ww, 960), (xx, 1020), C((248, 206, 110)), -1, cv2.LINE_AA)
        if lk >= 1:
            fly_drops(f, (rx, 980), (lx, 980), t, 7, 1.0, 3, 0.26, -30, op=0.75)
            slam(f, stamp_el("STILL HAPPENING", RED_I, 58), 540, 1370, -3, t, tc + 0.4)
    icap(f, "doing the", "[SAME THING]", t, ts - 0.05, size=120, y=440, out=tc)
    if t >= tc: icap(f, "a closed lid", "[CAN'T SAVE IT]", t, tc, size=100, y=440)
    return finish(f, n, look="warm")


# ---- S22: 'So, three things.' ----
def shot_S22(t, n):
    f = set_droom(t); t0 = st_("S22"); tt = T("f1", "three") - 0.1
    chub(f, 540, 1500, 1.15, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="happy", brow="up", look=(0.3, -0.2), hand_r="point", lean=4)
    table_front(f, TOP + 70)
    for j, (x_, c) in enumerate(((220, ACC_S), (540, WATER_S), (860, N_S))):
        if t >= tt + j * 0.1: comp(f, chip(str(j + 1), c, MILK, 74), x_, 620, scale=pin(t, tt + j * 0.1))
    return finish(f, n, look="golden")


# ---- S22b: 'Lid on right after you grab a handful, in an airtight jar.' — the jar: clip SNAPS shut, drops bounce off ----
def shot_S22b(t, n):
    f = set_droom(t); tl = T("f1", "Lid") + 0.05; ta = T("f1", "airtight") - 0.1
    hs = chub(f, 220, 1500, 0.98, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="n", brow="up", look=(1, 0), hand_r="pinch", turn=0.5)
    table_front(f, TOP)
    ton = T("f1", "on") + 0.05
    comp(f, scale_el(jar_ink_el(1.0 if t >= ton else 0.0), 1.0), 700, 1090)
    if t >= ton:
        for j in range(8):
            p = ((t * 1.1) + j / 8) % 1; a = -2.6 + j * 0.28; r_ = 340 - 130 * (1 - abs(2 * p - 1))
            comp(f, scale_el(drop_el("sad"), 0.24), 700 + r_ * math.cos(a), 1020 + r_ * math.sin(a))
    if t >= ta: comp(f, chip("AIRTIGHT", ACC_S, MILK, 46), 700, 1420, scale=pin(t, ta))
    comp(f, chip("1", ACC_S, MILK, 62), 90, 640, scale=pin(t, st_("S22b") + 0.05))
    icap(f, "lid", "[ON]", t, st_("S22b") + 0.05, size=170, y=440)
    src(f, SRC_O, t, ta, 1470)
    return finish(f, n, look="warm")


# ---- S23: 'Second, keep the crispy stuff and the soft sweets in separate boxes.' — they slide apart, a wall drops between ----
def shot_S23(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 1000, 500); ts = T("f2", "separate") - 0.1
    k = ramp(t, ts, 0.3); dx = 130 * k
    card(f, 390 - dx, 1040, 320, 440, (252, 240, 214)); card(f, 690 + dx, 1040, 320, 440, (252, 240, 214))
    comp(f, scale_el(chakli_el("happy", 0), 0.72), 390 - dx, 1020); comp(f, scale_el(barfi_ink_el("happy"), 0.86), 690 + dx, 1020)
    comp(f, achip("CRISPY", 34), 390 - dx, 1200); comp(f, chip("SOFT", WATER_S, MILK, 34), 690 + dx, 1200)
    if k > 0.8:
        yy = int(720 + 0 * k); cv2.line(f, (540, 760), (540, 1290), C(INKC), 14, cv2.LINE_AA)
    comp(f, chip("2", WATER_S, MILK, 62), 90, 640, scale=pin(t, st_("S23") + 0.05))
    icap(f, "", "[SEPARATE] boxes", t, ts - 0.4, size=110, y=440, acc=ACC_S)
    return finish(f, n, look="warm")


# ---- S24: 'And if it's already soft, don't throw it.' — he's about to bin it, stops himself ----
def shot_S24(t, n):
    f = set_droom(t); td = T("f3", "dont") - 0.1; tk = take(t, td)
    t3(f, "DON'T", 700, t, td, 220)
    comp(f, scale_el(bin_ink_el(0.8), 0.72), 840, 1330)
    p = POSE["stop"] if t > td else POSE["point"]
    chub(f, 380, 1500 + (tk["dy"] if t > td else 0), 1.05, t=t, **nolean(p), mouth=talk(t), expr=tk["expr"] if t > td else "sad", brow="up", look=(1, 0.3), lean=tk["lean"] if t > td else 6, hold=scale_el(chakli_el("sad", 1.0), 0.5), hold_off=(50, -20), turn=0.5, hand_r="pinch")
    comp(f, chip("3", N_S, MILK, 62), 90, 640, scale=pin(t, st_("S24") + 0.05))
    return finish(f, n, look="warm")


# ---- S24b: 'A few minutes in a low oven' / S24c: 'or short bursts in the microwave' ----
def shot_S24b(t, n):
    f = set_droom(t); t0 = st_("S24b")
    comp(f, scale_el(oven_ink_el(ramp(t, t0 + 0.1, 0.4)), 1.25), 540, 1050)
    comp(f, scale_el(chakli_el("sad", 1.0), 0.55), 400, 1060); comp(f, scale_el(mathri_el(1.0), 0.55), 600, 1090)
    icap(f, "a few minutes in a", "[LOW OVEN]", t, t0 + 0.05, size=130, y=440)
    comp(f, chip("ABOUT 120-150 C, 5-10 MIN", INKC, MILK, 34), 540, 1380, scale=pin(t, t0 + 0.2))
    src(f, "Source: ScienceABC", t, t0 + 0.3)
    return finish(f, n, look="warm")


def shot_S24c(t, n):
    f = set_droom(t); t0 = st_("S24c")
    comp(f, scale_el(microwave_el(True, "0:20"), 1.3), 540, 1000, scale=pin(t, t0, 0.2))
    icap(f, "or", "[SHORT BURSTS]", t, t0 + 0.05, size=120, y=440)
    comp(f, chip("20-30 SECONDS AT A TIME", INKC, MILK, 34), 540, 1380, scale=pin(t, t0 + 0.2))
    return finish(f, n, look="warm")


# ---- S25: 'The heat drives the water back out.' — inside the oven: drops flee, the chakli stiffens, goes gold ----
def shot_S25(t, n):
    f = inkify(stage("toastp", (255, 214, 140), 540, 1040, 480), 0.1); t0 = st_("S25"); tb = T("f4", "back") - 0.1
    k = ramp(t, t0 + 0.1, en_("S25") - t0 - 0.3)
    flames(f, 540, 1370, t, 800, 14, 0.6)
    comp(f, scale_el(chakli_el("happy" if k > 0.5 else "sad", 1 - k), 1.2), 540, 1050)
    fly_drops(f, (540, 960), (130, 560), t, 6, 0.9, 3, 0.32, 0, end_shrink=False); fly_drops(f, (540, 960), (950, 560), t, 6, 0.8, 5, 0.32, 0, end_shrink=False)
    icap(f, "the water goes", "[BACK OUT]", t, tb - 0.2, size=130, y=440, acc=WATER_S)
    return finish(f, n, look="golden")


# ---- S25b: 'Just let it cool before the lid goes on.' — he holds the lid back with a finger; a clock; steam thins out ----
def shot_S25b(t, n):
    f = set_droom(t); tc = T("f4", "cool") - 0.1; t0 = st_("S25b")
    chub(f, 240, 1500, 1.0, t=t, **nolean(POSE["stop"]), mouth=talk(t), expr="n", brow="up", look=(1, 0), turn=0.5)
    table_front(f, TOP)
    comp(f, scale_el(jar_ink_el(0.0), 0.72), 840, 1140)
    comp(f, scale_el(chakli_el(None, 0), 0.62), 540, 1210)
    steam_wisps(f, 540, 1090, t, 4, 170, 150, (255, 250, 236), 0.75 * (1 - ramp(t, t0 + 0.3, 1.6)), 6)
    comp(f, scale_el(clock_ink_el(), 0.5), 540, 770); clock_hands(f, 540, 770, 8 + (t - t0) * 6, 110, 0.5)
    icap(f, "let it", "[COOL] first", t, tc - 0.2, size=140, y=440, acc=WATER_S)
    return finish(f, n, look="warm")


# ---- S26: 'One honest catch. Soft is just a texture problem' ----
def shot_S26(t, n):
    f = set_droom(t); t0 = st_("S26"); tx = T("g1", "texture") - 0.1
    chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["shrug"]), mouth=talk(t), expr="n", brow="up", look=(1, 0), turn=0.5)
    table_front(f, TOP)
    comp(f, scale_el(chakli_el("n", 1.0), 0.86), 780, 1150)
    comp(f, chip("ONE HONEST CATCH", INKC, MILK, 44), 540, 440, scale=pin(t, t0 + 0.05))
    if t >= tx: comp(f, chip("JUST TEXTURE", WATER_S, MILK, 44), 780, 900, scale=pin(t, tx))
    return finish(f, n, look="warm")


# ---- S26b: 'but if it smells sharp, like paint or crayons' — he sniffs: stink lines, a paint tin + crayons pop ----
def shot_S26b(t, n):
    f = set_droom(t); mood(f, (120, 170, 60), 0.2); ts = T("g1", "smells") - 0.1; tp = T("g1", "paint") - 0.1; tc = T("g1", "crayons") - 0.1
    chub(f, 280, 1500, 1.02, t=t, la=(30, 14), ra=(120, 150), mouth=talk(t) if t < ts + 0.3 else "wavy", expr="gross" if t > ts + 0.3 else "sus", brow="sus", look=(1, 0), turn=0.5, lean=-5)
    table_front(f, TOP)
    comp(f, scale_el(chakli_el("sad", 0.3), 0.7), 500, 1210)
    stink(f, 500, 1080, t, 3, 300)
    if t >= tp: comp(f, scale_el(paint_el(), 0.95), 760, 1190, scale=pin(t, tp))
    if t >= tc:
        rot_comp(f, scale_el(crayon_el((236, 120, 60)), 0.9), 930, 1180, 14, pin(t, tc)); rot_comp(f, scale_el(crayon_el((96, 150, 214)), 0.9), 1000, 1200, -10, pin(t, tc + 0.05))
    icap(f, "if it smells", "[SHARP]", t, ts, size=150, y=440, acc=(96, 130, 40))
    return finish(f, n, look="warm")


# ---- S26c: 'that's the oil going off.' — an oil drop character turns ----
def shot_S26c(t, n):
    f = ink_set("moss", (255, 255, 255), 540, 1000, 480); to = T("g1", "oil") - 0.1
    comp(f, scale_el(chakli_el("sad", 0.2), 1.0), 540, 1100)
    stink(f, 540, 950, t, 3, 200)
    icap(f, "the oil is", "[GOING OFF]", t, to, size=120, y=440, acc=(96, 130, 40))
    src(f, SRC_R, t, to + 0.1, 1400)
    return finish(f, n, look="cool")


# ---- S26d: 'No oven fixes that, so bin it.' — oven crossed out, chakli drops in the bin ----
def shot_S26d(t, n):
    f = set_droom(t); tb = T("g1", "bin") - 0.12
    comp(f, scale_el(oven_ink_el(0), 0.42), 240, 760)
    cv2.line(f, (120, 660), (360, 860), C(RED_I), 20, cv2.LINE_AA); cv2.line(f, (360, 660), (120, 860), C(RED_I), 20, cv2.LINE_AA)
    t3(f, "BIN IT", 560, t, tb, 240)
    chub(f, 300, 1500, 1.0, t=t, **nolean(POSE["point"]), mouth=talk(t), expr="gross" if t > tb else "sus", brow="sus", look=(1, 0.4), hand_r="point", turn=0.5)
    comp(f, scale_el(bin_ink_el(1.0), 0.95), 760, 1300)
    if t >= tb:
        yy = drop_land(t, tb, 720, 1130, 0.35)[0]
        comp(f, scale_el(chakli_el("sad", 0.2), 0.5), 760, yy)
    return finish(f, n, look="warm")


# ---- S27: 'So remember: lid on, sweets apart, and a little heat if it's gone soft.' — the takeaway as three cards ----
def shot_S27(t, n):
    f = ink_set("rosep", (255, 255, 255), 540, 980, 480)
    ts = [T("h1", "lid") - 0.2, T("h1", "sweets") - 0.2, T("h1", "heat") - 0.3]
    icap(f, "so", "[REMEMBER]", t, st_("S27") + 0.05, size=120, y=430, out=ts[0])
    if t < ts[0] + 0.15: chub(f, 540, 1500 + 340 * ramp(t, ts[0] - 0.15, 0.3), 1.2, t=t, **nolean(POSE["hold_up"]), mouth=talk(t), expr="smirk", brow="up", look=(0.2, -0.3), hand_r="point", lean=4)
    for j, (tt, y_) in enumerate(zip(ts, (640, 900, 1160))):
        if t < tt: continue
        k = pin(t, tt); card(f, 540, y_, 840, 230, k=k)
        if j == 0:
            comp(f, scale_el(jar_ink_el(1.0), 0.34), 240, y_); comp(f, chip("LID ON", ACC_S, MILK, 60), 640, y_)
        if j == 1:
            comp(f, scale_el(chakli_el(None, 0), 0.36), 190, y_); comp(f, scale_el(barfi_ink_el(), 0.42), 320, y_); comp(f, chip("SWEETS APART", WATER_S, MILK, 50), 660, y_)
        if j == 2:
            comp(f, scale_el(oven_ink_el(1.0), 0.32), 240, y_); comp(f, chip("A LITTLE HEAT", N_S, MILK, 50), 660, y_)
    f = push_in(f, t, st_("S27") + 0.3, en_("S27"), 1.03, 540, 950)
    return finish(f, n, look="warm")


# ---- S28: send it — back on the lane, walking on, phone + logo sting ----
def shot_S28(t, n):
    t0 = st_("S28"); camx = 300 * (t - t0); f = set_lane(t, camx + 900)
    vend = LINES["h2"]["end"] + 0.15
    w = walk(t, 300, 1500, 1.0, speed=300, t0=t0, track=True); w.pop("ra"); w.pop("la")
    if t < vend + 0.2:
        pr = t >= T("h2", "Send") + 0.3
        comp(f, scale_el(phone2_el("your namkeen box is open", "lid on! now!", pr), 0.82), 740, 930, scale=pin(t, t0))
        if pr and t < T("h2", "Send") + 0.75:
            rr = (t - T("h2", "Send") - 0.3) / 0.45
            cv2.circle(f, (740, 1200), int(30 + 140 * rr), (1, 1, 1), max(1, int(10 * (1 - rr))), cv2.LINE_AA)
        chub(f, s=1.0, t=t, la=(20, 12), ra=(70, 40), mouth=talk(t), expr="happy", brow="up", hand_r="point", **{k: v for k, v in w.items()})
        lane_front(f, camx + 900)
        ui_word(f, "the friend who leaves the box", "[OPEN]", 420, t, T("h2", "friend") - 0.1, col=WHITE, acc=ACC_L, size=120, shadow=0.6, lead_col=WHITE)
    else:
        k = pin(t, vend + 0.2, 0.4); f = f * 0.22 + 0.78 * np.array(C((252, 244, 228)), np.float32)
        comp(f, logo_el(), 540, 820, scale=k * 0.95)
        comp(f, ed_el("follow for more health facts", "", lead_col=INKC, lead_size=42), 540, 1030, op=clamp((t - vend - 0.5) / 0.3))
        chub(f, s=0.7, t=t, la=(150, 170), ra=(150, 170), mouth=3, expr="happy", brow="up", **{k_: v for k_, v in walk(t, 540, 1500, 0.7, speed=300, t0=t0, track=True, amt=0.0).items() if k_ not in ("la", "ra", "look", "turn")})
    return finish(f, n, look="golden")


RENDER = {s["id"]: globals()[f"shot_{s['id']}"] for s in SHOTS}

IMPACTS = [(T("i1", "soft") - 0.2, 0.4, 16), (T("i2", "drinking") - 0.1, 0.35, 14), (T("i3", "opposite") - 0.1, 0.3, 12), (T("a2", "crunch") - 0.2, 0.4, 18), (T("a2", "thirsty") - 0.1, 0.3, 10),
           (T("a3", "full") - 0.12, 0.3, 10), (T("b1", "meter") - 0.1, 0.3, 10), (T("b1", "thirstier") - 0.12, 0.25, 8), (T("b3", "lid") - 0.1, 0.3, 12), (T("b3", "one") - 0.1, 0.35, 14), (T("c1", "kill") - 0.1, 0.35, 14),
           (T("c2", "snaps") - 0.12, 0.4, 18), (T("c2", "water") - 0.12, 0.3, 10), (T("c3", "like") + 0.0, 0.3, 12), (T("c3", "glassy") - 0.12, 0.3, 12), (T("c4", "rubbery") - 0.15, 0.3, 12), (T("c5", "crunch") - 0.12, 0.35, 14),
           (T("d1", "rejected") - 0.1, 0.35, 14), (T("d2", "away") + 0.15, 0.35, 14), (T("e1", "trap") - 0.1, 0.4, 16), (T("e4", "closed") + 0.25, 0.35, 14), (T("f1", "on") + 0.05, 0.25, 10), (T("f3", "dont") - 0.1, 0.35, 12), (T("g1", "bin") - 0.12, 0.4, 16), (T("h1", "heat") - 0.3, 0.2, 8), (T("h2", "Send") + 0.3, 0.2, 8)]


def rs(sid, t, n):
    s = SHOT[sid]; tt = min(max(t, s["start"]), s["end"] - 1e-3)
    f = RENDER[sid](tt, n).astype(np.float32)
    dx = dy = 0.0; z = 1.0
    for ti, d, a in IMPACTS:
        if s["start"] - 0.05 <= ti < s["end"] and ti <= tt < ti + d:
            k = 1 - (tt - ti) / d; dx += a * k * math.sin(tt * 97); dy += a * k * math.cos(tt * 83); z += 0.03 * k
    if dx or dy or abs(z - 1) > 1e-4: f = cam(f, z, W / 2, H / 2, dx, dy)
    return f


def _bl(x, s_):
    if s_ < 0.5: return x
    sm = cv2.resize(x, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    return cv2.resize(cv2.GaussianBlur(sm, (0, 0), s_ / 4), (W, H), interpolation=cv2.INTER_LINEAR)


def compose(n):
    t = n / FPS
    i = next((k for k, s in enumerate(SHOTS) if s["start"] <= t < s["end"]), len(SHOTS) - 1)
    sh = SHOTS[i]; f = rs(sh["id"], t, n); k = sh["trans"]; dt = t - sh["start"]
    if i > 0:
        if k == "focus" and dt < 0.34:
            p = dt / 0.34; prv = rs(SHOTS[i - 1]["id"], t, n); m = eio(p)
            f = _bl(prv, 40 * m) * (1 - m) + _bl(f, 40 * (1 - m)) * m
        elif k == "whip" and dt < 0.22:
            p = 1 - dt / 0.22; M = np.float32([[1, 0, -360 * p * p], [0, 1, 0]])
            f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
        elif k == "zoom" and dt < 0.2:
            p = 1 - dt / 0.2; acc = np.zeros_like(f)
            for q in range(5): acc += cam(f, 1 + 0.06 * q * p)
            f = acc / 5
        elif k == "flash" and dt < 0.14: f = f + 0.8 * (1 - dt / 0.14) ** 1.5
        elif k == "punch" and dt < 0.16: f = cam(f, 1 + 0.08 * (1 - dt / 0.16)) + 0.12 * (1 - dt / 0.16)
    nx = SHOTS[i + 1] if i + 1 < len(SHOTS) else None
    if nx is not None and nx["trans"] == "whip" and sh["end"] - t < 0.14:
        p = 1 - (sh["end"] - t) / 0.14; M = np.float32([[1, 0, 360 * p * p], [0, 1, 0]])
        f = cv2.blur(cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT), (int(2 + 120 * p), 1))
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)
